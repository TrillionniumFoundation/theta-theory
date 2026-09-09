#!/usr/bin/env python3
"""Independent finite diagnostics for the pinned A2 v6 referee report.
Not imported from the author's or previous referees' code. Exact symbolic
identities and ordinary floating-point quadrature are distinguished.
These checks are not a proof assistant, interval arithmetic, or billiard CI.
Run: python independent_checks.py [--output result.json]
"""
from __future__ import annotations
import argparse
import json
import math
import platform
from collections import Counter
from pathlib import Path
import scipy
from scipy.integrate import quad
import sympy as S

RECORDS: list[dict[str, str]] = []

def exact(name: str, residual: S.Expr) -> None:
    if S.simplify(residual) != 0:
        raise RuntimeError(f"Exact identity failed: {name}: {residual}")
    RECORDS.append({"name": name, "type": "exact", "status": "pass"})

def positive(name: str, value: S.Expr) -> None:
    if S.simplify(value).is_positive is not True:
        raise RuntimeError(f"Exact positivity failed: {name}: {value}")
    RECORDS.append({"name": name, "type": "exact", "status": "pass"})

def close(name: str, lhs: float, rhs: float, tol: float = 2e-11) -> None:
    if not (math.isfinite(lhs) and math.isfinite(rhs)):
        raise RuntimeError(f"Nonfinite numerical diagnostic: {name}")
    if abs(lhs-rhs) > tol * max(1.0, abs(lhs), abs(rhs)):
        raise RuntimeError(f"Numerical identity failed: {name}: {lhs}, {rhs}")
    RECORDS.append({"name": name, "type": "ordinary_float", "status": "pass"})

def run() -> dict:
    r, g, A, c = S.symbols("r g A c", positive=True)
    phi1 = r / S.sqrt(g*(g+2*r))
    phis = [phi1, phi1/(2*(1+g/r)), phi1/(4*(1+g/r)**2-1)]
    expected = [[S.Rational(1,4), S.Rational(3,4), -S.Rational(5,4), S.Rational(21,4)],
                [S.Rational(1,24), S.Rational(17,72), S.Rational(35,216), -S.Rational(491,216)],
                [S.Rational(1,140), S.Rational(297,4900), S.Rational(36243,171500), -S.Rational(4458537,6002500)]]
    rows = []
    for j, phi in enumerate(phis, 1):
        vals = [S.simplify(S.diff(phi,r,k).subs({r:S.Rational(1,4),g:S.Rational(1,2)})) for k in range(4)]
        for k, value in enumerate(vals):
            exact(f"three_amplitude_derivative_j{j}_k{k}", value/S.sqrt(2)-expected[j-1][k])
        rows.append([(vals[1]+S.pi*vals[0]/(72*A))/A,
                     (-vals[2]+5*S.pi*vals[0]/(144*A))/A, vals[3]/(2*A)])
    target = -2*S.sqrt(2)*(15804720*A+64253*S.pi)/(72930375*A**4)
    exact("physical_three_amplitude_determinant", S.Matrix(rows).det()-target)
    fs = [S.Integer(1),1/(2*c),1/(4*c*c-1),1/(4*c*(2*c*c-1))]
    wr = S.Matrix([[S.diff(f,c,k) for k in range(4)] for f in fs]).det()
    wr_target = 12*(64*c**8+32*c**6+116*c**4+4*c*c+1)/(c**4*(4*c*c-1)**4*(2*c*c-1)**4)
    exact("four_amplitude_wronskian", wr-wr_target)
    e1,e2,R = S.symbols("e1 e2 R")
    al=e1/108; bz=e1**2/2916-e2/972
    area = S.sqrt(3)/2-S.pi*(R**2+2*R*al-S.Rational(33,2)*al**2-S.Rational(45,4)*bz)
    exact("physical_area_constraint", area-(S.sqrt(3)/2-S.pi*R**2-S.pi*R*e1/54+41*S.pi*e1**2/7776-5*S.pi*e2/432))

    # Rational exp(-gamma) makes all the finite Green computations exact.
    for lam in [S.Rational(1,3),S.Rational(2,3)]:
        sh=lambda n:(lam**(-n)-lam**n)/2
        ch=lambda n:(lam**(-n)+lam**n)/2
        a=sh(1)  # g=1
        for j in [1,2,3,5,8]:
            H=a*S.Matrix([[ch(j)/sh(j),-1/sh(j)],[-1/sh(j),ch(j)/sh(j)]])
            Hi=H.inv()
            nus=[]
            for i in range(j+1):
                L=S.Matrix([[sh(j-i)/sh(j),sh(i)/sh(j)]])
                nu=S.simplify((L*Hi*L.T)[0]); nus.append(nu)
                exact(f"finite_metric_lam{lam}_j{j}_i{i}",nu-ch(j-2*i)/(a*sh(j)))
            for m in range(2,6):
                alpha=S.Rational(2,2**m*(m+1)*math.factorial(m)**2)
                action=nus[0]**m+nus[j]**m+2*sum(x**m for x in nus[1:j])
                det=4*m*sum(sh(i)*sh(j-i)/(a*sh(j))*nus[i]**(m-1) for i in range(1,j))
                diagonal=S.simplify(alpha*(action+det))
                positive(f"uniform_diagonal_bound_lam{lam}_j{j}_m{m}",diagonal-2*alpha/a**m)
                if j==1:
                    exact(f"one_flight_reduction_lam{lam}_m{m}",diagonal-2*alpha*(ch(1)/sh(1)**2)**m)
        for m in range(2,7):
            D=lam**(2*(m-1))/(1-lam**(2*(m-1)))-lam**(2*m)/(1-lam**(2*m))
            ratio=(sh(1)/ch(1))**m*(ch(m)/sh(m)+2*m*D)
            positive(f"sensitivity_positive_lam{lam}_m{m}",ratio)

    for m in range(1,8):
        omega=[(-1)**(l-1)*S.binomial(m,l) for l in range(1,m+1)]
        exact(f"extrapolation_mass_m{m}",sum(omega)-1)
        for k in range(1,m):
            exact(f"extrapolation_cancellation_m{m}_k{k}",sum(w*S.Integer(l)**k for l,w in enumerate(omega,1)))
        exact(f"harmonic_timing_m{m}",sum(w/S.Integer(l) for l,w in enumerate(omega,1))-S.harmonic(m))
    for J in [3,4]:
        positive(f"all_outcome_window_safety_J{J}", S.Integer(J+1)-3*S.Rational(J,4)-1)

    rotation=S.Matrix([[-S.Rational(1,2),-S.sqrt(3)/2],[S.sqrt(3)/2,-S.Rational(1,2)]])
    exact("count_symmetry_rotation_order_three",sum((rotation**3-S.eye(2)).applyfunc(lambda x:x*x)))
    exact("count_symmetry_no_invariant_linear_form",(rotation-S.eye(2)).det()-3)
    ss=S.symbols("s")
    phi=phis[0].subs(g,S.Rational(1,2))
    num=phi.subs(r,S.Rational(1,4)+36*ss)+2*phi.subs(r,S.Rational(1,4)-18*ss)
    exact("physical_path_first_derivative_zero",S.diff(num,ss).subs(ss,0))
    exact("physical_path_cubic_difference",S.diff(num,ss,3).subs(ss,0)/3-11664*S.diff(phi,r,3).subs(r,S.Rational(1,4)))

    tv_values=[]
    for eps in [0.02,0.1,0.3,0.65,0.9]:
        lam=(1-eps)/(1+eps); theta=math.atan(math.sqrt(lam))
        # Integrate exact polar disk/ellipse intersection, split at crossing.
        integ1=quad(lambda t:1.0,0,theta,epsabs=1e-13)[0]
        integ2=quad(lambda t:1/(lam*math.cos(t)**2+math.sin(t)**2/lam),theta,math.pi/2,epsabs=1e-13)[0]
        delta=1-2*(integ1+integ2)/math.pi
        formula=2*math.asin(eps)/math.pi
        close(f"quadratic_TV_polar_integral_eps{eps}",delta,formula)
        close(f"quadratic_TV_angle_identity_eps{eps}",1-4*theta/math.pi,formula)
        tv_values.append({"exp_minus_j_gamma":eps,"TV":formula})
        for k in [1,3,12]:
            # Probability of at least one point outside the common support.
            binomial_sum=sum(math.comb(k,l)*delta**l*(1-delta)**(k-l) for l in range(1,k+1))
            close(f"product_support_TV_eps{eps}_k{k}",binomial_sum,1-(1-delta)**k)
    for p,q in [(0.002,0.003),(0.11,0.13),(0.25,0.21)]:
        kl=p*math.log(p/q)+(1-p)*math.log((1-p)/(1-q))
        bound=(p-q)**2/(q*(1-q))
        if kl<0 or kl>bound+1e-14:
            raise RuntimeError("Bernoulli KL bound failed")
        RECORDS.append({"name":f"Bernoulli_KL_bound_{p}_{q}","type":"ordinary_float","status":"pass"})
    counts=Counter(x["type"] for x in RECORDS)
    return {"status":"pass","reviewed_commit":"4ca186258c92dcbc75accc4eb576e307cc612189",
            "python":platform.python_version(),"sympy":S.__version__,"scipy":scipy.__version__,
            "counts":{"total":len(RECORDS),**dict(counts)},"quadratic_TV_examples":tv_values,
            "limitations":["Finite symbolic and numerical diagnostics, not formal verification.",
                           "No author or earlier referee diagnostic code imported.",
                           "No simulation of the physical billiard and no manuscript PDF rebuild.",
                           "KL checks illustrate an elementary inequality; the lower-bound proof is in the report."],
            "checks":RECORDS}

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    result=run()
    text=json.dumps(result,indent=2,sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(text,encoding="utf-8")
    print(text)
