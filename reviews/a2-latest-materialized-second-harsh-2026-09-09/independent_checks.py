#!/usr/bin/env python3
"""Independent finite checks for the A2 second review; no repository imports.
Run: python independent_checks.py > DIAGNOSTICS.json
Dependencies: numpy, scipy, sympy. Floating checks are not interval certificates.
"""
from __future__ import annotations
import json
import math
import platform
from collections import Counter
import numpy as np
import scipy
import sympy as sp

checks: list[dict[str, object]] = []

def check(name: str, condition: object, kind: str) -> None:
    if not bool(condition):
        raise RuntimeError(f"Check failed: {name}")
    checks.append({"name": name, "kind": kind, "passed": True})

def exact(name: str, expression: sp.Expr) -> None:
    check(name, sp.simplify(expression) == 0, "exact")

# The area-preserving support family, tested at the non-ground vertical channel.
I4, I6 = sp.Rational(3, 4)*sp.pi, sp.Rational(5, 8)*sp.pi
zp = -I4/I6
hp, rp = 1+zp, -3-5*zp
vgp, vkp = -2*hp, -rp
vcp = vgp+2*vkp
vlogp = -3*vcp/(3**2-1)
for name, value, expected in [
    ("area_compensator",zp,sp.Rational(-6,5)),
    ("vertical_support",hp,sp.Rational(-1,5)),
    ("vertical_radius",rp,sp.Integer(3)),
    ("vertical_gap",vgp,sp.Rational(2,5)),
    ("vertical_curvature",vkp,sp.Integer(-3)),
    ("vertical_c",vcp,sp.Rational(-28,5)),
    ("vertical_log_leading_amplitude",vlogp,sp.Rational(21,10))]:
    exact(name, value-expected)

# Recompute the four-amplitude Wronskian from the displayed rational functions.
c = sp.symbols("c", positive=True)
fs = [sp.Integer(1), 1/(2*c), 1/(4*c*c-1), 1/(4*c*(2*c*c-1))]
wr = sp.det(sp.Matrix([[sp.diff(f,c,k) for k in range(4)] for f in fs]))
wr_expected = 12*(64*c**8+32*c**6+116*c**4+4*c*c+1)/(c**4*(4*c*c-1)**4*(2*c*c-1)**4)
exact("four_function_wronskian", wr-wr_expected)

# All-order finite-bridge diagonal: rational Schur complements at g=kappa=1.
finite_examples = []
for j in range(1,9):
    H = sp.zeros(j+1)
    for i in range(j+1):
        H[i,i] = 2 if i in (0,j) else 4
    for i in range(j):
        H[i,i+1] = H[i+1,i] = -1
    endpoints = [0,j]
    inner = list(range(1,j))
    B = H.extract(inner,endpoints)
    G = H.extract(inner,inner).inv() if inner else sp.zeros(0)
    He = H.extract(endpoints,endpoints)-B.T*G*B
    Hi = He.inv()
    L = sp.zeros(j+1,2)
    L[0,0],L[j,1] = 1,1
    if inner:
        Li = -G*B
        for i in inner:
            L[i,0],L[i,1] = Li[i-1,0],Li[i-1,1]
    exact(f"endpoint_determinant_j{j}", sp.det(He)-3)
    nu = [(L[i,:]*Hi*L[i,:].T)[0] for i in range(j+1)]
    for m in range(2,9):
        alpha = sp.Rational(2,2**m*(m+1)*math.factorial(m)**2)
        action = sum((1 if i in endpoints else 2)*nu[i]**m for i in range(j+1))
        determinant = sum(G[i-1,i-1]*nu[i]**(m-1) for i in inner)
        diagonal = -alpha*(action+4*m*determinant)
        check(f"finite_diagonal_negative_j{j}_m{m}",diagonal<0,"exact")
        if j == 1:
            target = -4*sp.Rational(2,3)**m/(2**m*(m+1)*math.factorial(m)**2)
            exact(f"one_flight_reduction_m{m}",diagonal-target)
        if j in (1,2,4,8) and m in (2,3):
            finite_examples.append({"j":j,"m":m,"diagonal":str(diagonal)})

# Exact identities used by the calibration experiment, not a simulation of it.
for m in range(1,9):
    weights = [(-1)**(l-1)*sp.binomial(m,l) for l in range(1,m+1)]
    exact(f"richardson_constant_m{m}",sum(weights)-1)
    exact(f"harmonic_timing_m{m}",sum(weights[l-1]/l for l in range(1,m+1))-sp.harmonic(m))
    for k in range(1,m):
        exact(f"richardson_cancel_m{m}_k{k}",sum(weights[l-1]*l**k for l in range(1,m+1)))

# Finite-bridge formula versus the author's limiting diagonal (ordinary floats).
gamma = math.acosh(2)
a = math.sinh(gamma)
def finite_diagonal(j: int, m: int) -> float:
    sj = math.sinh(j*gamma)
    Hi = np.array([[math.cosh(j*gamma)/sj,1/sj],[1/sj,math.cosh(j*gamma)/sj]])/a
    action = determinant = 0.0
    for i in range(j+1):
        row = np.array([math.sinh((j-i)*gamma)/sj,math.sinh(i*gamma)/sj])
        nu = float(row@Hi@row)
        action += (1 if i in (0,j) else 2)*nu**m
        if 0 < i < j:
            Gii = math.sinh(i*gamma)*math.sinh((j-i)*gamma)/(a*sj)
            determinant += Gii*nu**(m-1)
    alpha = 2/(2**m*(m+1)*math.factorial(m)**2)
    return -alpha*(action+4*m*determinant)

limits = []
for m in range(2,7):
    D = 1/math.expm1(2*(m-1)*gamma)-1/math.expm1(2*m*gamma)
    target = -4*(1/math.tanh(m*gamma)+2*m*D)/(2**m*(m+1)*math.factorial(m)**2*a**m)
    errors = []
    for j in (8,16,32,64):
        got = finite_diagonal(j,m)
        err = abs(got/target-1)
        errors.append({"j":j,"relative_error":err})
        check(f"finite_to_limit_j{j}_m{m}",err<(1e-5 if j==8 else 1e-11),"floating_noninterval")
    limits.append({"m":m,"limiting_diagonal":target,"errors":errors})

# Actual nonlinear stationary length/twist calculation, not the diagonal formula.
def edge(u: float, v: float) -> tuple[float,float,float,float,float,float]:
    # psi(y)=y^2/2+y^4/24 is a local polynomial graph, not a global periodic table.
    psi = lambda x: x*x/2+x**4/24
    dp = lambda x: x+x**3/6
    ddp = lambda x: 1+x*x/2
    gap, diff = 1+psi(u)+psi(v),v-u
    length = math.hypot(gap,diff)
    du,dv = (gap*dp(u)-diff)/length,(gap*dp(v)+diff)/length
    huu = (dp(u)**2+gap*ddp(u)+1-du*du)/length
    hvv = (dp(v)**2+gap*ddp(v)+1-dv*dv)/length
    huv = (dp(u)*dp(v)-1-du*dv)/length
    excess = psi(u)+psi(v)+diff*diff/(length+gap)
    return excess,du,dv,huu,hvv,huv

def solve_chain(j: int, u: float, v: float) -> dict[str,float|int]:
    y = np.array([(math.sinh((j-i)*gamma)*u+math.sinh(i*gamma)*v)/math.sinh(j*gamma) for i in range(j+1)])
    for iteration in range(20):
        grad,H = np.zeros(j+1),np.zeros((j+1,j+1))
        E,logproduct = 0.0,0.0
        for i in range(j):
            ee,du,dv,huu,hvv,huv = edge(float(y[i]),float(y[i+1]))
            E += ee
            if huv >= 0:
                raise RuntimeError("Nonnegative edge mixed derivative")
            logproduct += math.log(-huv)
            grad[i] += du
            grad[i+1] += dv
            H[i,i] += huu
            H[i+1,i+1] += hvv
            H[i,i+1] = H[i+1,i] = huv
        residual = float(np.max(np.abs(grad[1:j]))) if j>1 else 0.0
        if residual < 1e-14:
            break
        y[1:j] -= np.linalg.solve(H[1:j,1:j],grad[1:j])
    else:
        raise RuntimeError("Newton iteration failed")
    sign,logdet = np.linalg.slogdet(H[1:j,1:j]) if j>1 else (1.0,0.0)
    if sign <= 0:
        raise RuntimeError("Nonpositive interior determinant")
    logb = logproduct-logdet-(math.log(a)-math.log(math.sinh(j*gamma)))
    return {"j":j,"excess_action":E,"log_normalized_twist":float(logb),"stationary_residual":residual,"newton_steps":iteration}

chains=[]
for j in (1,2,4,8,16,32,64):
    atzero = solve_chain(j,0.0,0.0)
    check(f"nonlinear_normalization_at_zero_j{j}",abs(atzero["log_normalized_twist"])<2e-12,"floating_noninterval")
    result = solve_chain(j,0.06,-0.035)
    check(f"nonlinear_stationarity_j{j}",result["stationary_residual"]<1e-13,"floating_noninterval")
    check(f"nonlinear_positive_excess_j{j}",result["excess_action"]>0,"floating_noninterval")
    chains.append(result)
check("nonlinear_action_32_vs_64",abs(chains[-2]["excess_action"]-chains[-1]["excess_action"])<1e-12,"floating_noninterval")
check("nonlinear_log_twist_32_vs_64",abs(chains[-2]["log_normalized_twist"]-chains[-1]["log_normalized_twist"])<2e-12,"floating_noninterval")

output={
    "scope":"Independent finite diagnostics; not a proof certificate, author test suite, global billiard simulation, or PDF build.",
    "environment":{"python":platform.python_version(),"numpy":np.__version__,"scipy":scipy.__version__,"sympy":sp.__version__},
    "summary":{"passed":len(checks),"by_kind":dict(Counter(str(x["kind"]) for x in checks))},
    "vertical_channel":{"z_prime":str(zp),"gap_prime":str(vgp),"curvature_prime":str(vkp),"log_leading_amplitude_prime":str(vlogp)},
    "finite_diagonal_examples":finite_examples,
    "finite_to_limit":limits,
    "nonlinear_stationary_chains":chains,
    "checks":checks
}
print(json.dumps(output,indent=2,sort_keys=True))
