#!/usr/bin/env python3
"""Finite exact identities and non-interval diagnostics for A2 v6.
Run from the manuscript directory: python tools-v6/verify_revision.py.
These checks supplement the printed proofs; they are not certificates.
"""
from __future__ import annotations
import json
import math
import platform
from collections import Counter
import numpy as np
import scipy
from scipy.integrate import quad
import sympy as sp

checks: list[dict[str, object]] = []
def check(name: str, ok: object, kind: str = "exact") -> None:
    if not bool(ok):
        raise RuntimeError(f"Failed: {name}")
    checks.append({"name": name, "kind": kind, "passed": True})
def exact(name: str, expr: sp.Expr) -> None:
    check(name, sp.simplify(expr) == 0)

# Derive the physical area constraint from the original support coefficients.
R,e1,e2,alpha,beta,zeta=sp.symbols("R e1 e2 alpha beta zeta",real=True)
x=[36*(alpha+beta),36*(alpha-beta/2+sp.sqrt(3)*zeta/2),
   36*(alpha-beta/2-sp.sqrt(3)*zeta/2)]
exact("radius_sum",sum(x)-108*alpha)
exact("radius_square_sum",sum(v*v for v in x)-3888*alpha**2-1944*(beta**2+zeta**2))
area0=sp.sqrt(3)/2-sp.pi*R**2
area=area0-2*sp.pi*R*e1/108+sp.pi*sp.Rational(33,2)*(e1/108)**2+sp.pi*sp.Rational(45,4)*(e1**2/2916-e2/972)
expected_area=area0-sp.pi*R*e1/54+41*sp.pi*e1**2/7776-5*sp.pi*e2/432
exact("physical_area_polynomial",area-expected_area)

# Direct derivatives before substituting the physical reference radius.
r=sp.symbols("r",positive=True);g=sp.Rational(1,2);ref=sp.Rational(1,4)
c=1+g/r;phi1=r/sp.sqrt(g*(g+2*r));phis=[phi1,phi1/(2*c),phi1/(4*c*c-1)]
values=sp.Matrix([[sp.simplify(sp.diff(p,r,k).subs(r,ref)/sp.sqrt(2)) for k in range(4)] for p in phis])
table=sp.Matrix([[sp.Rational(1,4),sp.Rational(3,4),sp.Rational(-5,4),sp.Rational(21,4)],
 [sp.Rational(1,24),sp.Rational(17,72),sp.Rational(35,216),sp.Rational(-491,216)],
 [sp.Rational(1,140),sp.Rational(297,4900),sp.Rational(36243,171500),sp.Rational(-4458537,6002500)]])
for j in range(3):
    for k in range(4):exact(f"three_amplitude_derivative_{j+1}_{k}",values[j,k]-table[j,k])
A=sp.symbols("A",positive=True)
V=sp.sqrt(2)*values
Jac=sp.Matrix([[ (V[j,1]+sp.pi/(72*A)*V[j,0])/A,
                 (-V[j,2]+5*sp.pi/(144*A)*V[j,0])/A,V[j,3]/(2*A)] for j in range(3)])
det=sp.factor(Jac.det())
expected=-2*sp.sqrt(2)*(15804720*A+64253*sp.pi)/(72930375*A**4)
exact("physical_three_amplitude_jacobian",det-expected)
check("physical_reference_free_area_positive",float(area0.subs(R,ref))>0,"floating_noninterval")

# Uniform-in-j finite diagonal lower bound checked on rational Schur models.
for j in range(1,9):
    H=sp.zeros(j+1)
    for i in range(j+1):H[i,i]=2 if i in (0,j) else 4
    for i in range(j):H[i,i+1]=H[i+1,i]=-1
    inner=list(range(1,j));ends=[0,j]
    G=H.extract(inner,inner).inv() if inner else sp.zeros(0)
    B=H.extract(inner,ends);He=H.extract(ends,ends)-B.T*G*B;Hi=He.inv()
    L=sp.zeros(j+1,2);L[0,0]=L[j,1]=1
    if inner:
        Li=-G*B
        for i in inner:
            for k in range(2):L[i,k]=Li[i-1,k]
    nu=[(L[i,:]*Hi*L[i,:].T)[0] for i in range(j+1)]
    check(f"endpoint_metric_lower_bound_j{j}",nu[0]>0 and nu[0]**2>=sp.Rational(1,3))
    for m in range(2,7):
        S=sum((1 if i in ends else 2)*nu[i]**m for i in range(j+1))
        S+=4*m*sum(G[i-1,i-1]*nu[i]**(m-1) for i in inner)
        check(f"diagonal_retains_two_endpoint_bound_j{j}_m{m}",S>=2*nu[0]**m)

# Extrapolation identities and the all-outcome timing safety margin.
for m in range(1,9):
    w=[(-1)**(l-1)*sp.binomial(m,l) for l in range(1,m+1)]
    exact(f"weight_sum_m{m}",sum(w)-1)
    for k in range(1,m):exact(f"cancel_m{m}_degree{k}",sum(w[l-1]*l**k for l in range(1,m+1)))
    exact(f"harmonic_m{m}",sum(w[l-1]/sp.Integer(l) for l in range(1,m+1))-sp.harmonic(m))
for J in (3,4):check(f"safe_window_J{J}",sp.Rational(J+1)-sp.Rational(3*J,4)>1)
m=sp.symbols("m",positive=True)
exact("count_only_accuracy_exponent",3*(2*m+2)/m-(6+6/m))
z,t,C,b,j=sp.symbols("z t C b j",positive=True)
prob=lambda y:C*y*y+b*y**3
exact("leading_count_timing_derivative",sp.diff((prob(z+j*t)-prob(z))/z**2,t).subs(t,0)-(2*C*j/z+3*b*j))

# Nonlinear square-root interpolation: a population check, not noisy trials.
pilot=[]
for m in range(1,5):
    for h in (.04,.02,.01):
        tau=.13*h;nodes=np.arange(1,m+2,dtype=float);d=h*nodes-tau
        vals=d*np.sqrt(1+.4*d)
        coef=np.polynomial.polynomial.polyfit(nodes,vals,m)
        roots=np.polynomial.polynomial.polyroots(coef)
        roots=[float(q.real*h) for q in roots if abs(q.imag)<1e-9 and -.5<q.real<.5]
        check(f"pilot_unique_zero_m{m}_h{h}",len(roots)==1,"floating_noninterval")
        err=abs(roots[0]-tau)
        check(f"pilot_order_bound_m{m}_h{h}",err<2*h**(m+1),"floating_noninterval")
        pilot.append({"m":m,"h":h,"error":err,"scaled_error":err/h**(m+1)})

# Exact radial integration leaves this one-dimensional angular TV quadrature
# for the quadratic reference experiment. This is not a global billiard simulation.
gamma=math.acosh(2);tvs=[]
for j in (1,2,4,8,12):
    z=j*gamma;ch=1/math.tanh(z);sh=1/math.sinh(z)
    angle=.5*math.asin(math.exp(-z))
    points=[angle,math.pi/2-angle,math.pi+angle,3*math.pi/2-angle]
    val,error=quad(lambda th:abs(1/(ch-sh*math.sin(2*th))-1),0,2*math.pi,
                   points=points,epsabs=1e-12,epsrel=1e-10,limit=100)
    tv=val/(4*math.pi)
    check(f"quadratic_tv_positive_j{j}",0<tv<1,"floating_noninterval")
    check(f"quadratic_tv_relative_rate_j{j}",tv<2*math.exp(-z),"floating_noninterval")
    tvs.append({"j":j,"conditional_tv":tv,"tv_over_exp_minus_j_gamma":tv/math.exp(-z),"quad_error":error})

out={"scope":"Finite checks supplement printed proofs. No interval, proof-assistant, exhaustive novelty, or minimax certificate.",
     "environment":{"python":platform.python_version(),"numpy":np.__version__,"scipy":scipy.__version__,"sympy":sp.__version__},
     "summary":{"passed":len(checks),"by_kind":dict(Counter(str(x['kind']) for x in checks))},
     "three_amplitude_determinant":str(det),"pilot_population_checks":pilot,"quadratic_experiment_tv":tvs,"checks":checks}
print(json.dumps(out,indent=2,sort_keys=True))
