#!/usr/bin/env python3
"""Finite diagnostics for A2 v7. Printed proofs, not these tests, justify theorems.
No billiard simulation, network, proof assistant, or interval arithmetic is used.
Run normally and with python -O; the checks use explicit exceptions.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
from itertools import product
import json
import math
from pathlib import Path
import platform
from collections import Counter
import scipy
from scipy.integrate import quad
from scipy.stats import binom
import sympy as S

checks: list[dict] = []

def check(name: str, condition: bool, kind: str = 'exact') -> None:
    if not condition:
        raise RuntimeError(f'Check failed: {name}')
    checks.append({'name': name, 'kind': kind, 'status': 'pass'})

def exact(name: str, expression: S.Expr) -> None:
    check(name, S.simplify(expression) == 0)

def close(name: str, x: float, y: float, tol: float = 2e-11) -> None:
    check(name, math.isfinite(x) and math.isfinite(y)
          and abs(x-y) <= tol*max(1.0, abs(x), abs(y)), 'ordinary_float')

def discrete_tv(p: list[F], q: list[F]) -> F:
    return sum((abs(x-y) for x,y in zip(p,q)), F(0))/2

def product_law(marginals: list[list[F]]) -> list[F]:
    return [math.prod(row) for row in product(*marginals)]

def main() -> dict:
    q = S.symbols('q', positive=True)
    ch, sh = (1+q*q)/(1-q*q), 2*q/(1-q*q)
    M = S.Matrix([[ch,-sh],[-sh,ch]])
    exact('hyperbolic_determinant', M.det()-1)
    exact('lower_eigenvalue', ch-sh-(1-q)/(1+q))
    exact('upper_eigenvalue', ch+sh-(1+q)/(1-q))
    lam = (1-q)/(1+q)
    exact('overlap_angle_identity', (1-lam)/(1+lam)-q)
    r = S.symbols('r', nonnegative=True)
    exact('quadratic_residual_volume',
          S.integrate(2*S.pi*r*(1-r*r/2),(r,0,S.sqrt(2)))-S.pi)
    exact('raw_mass_from_twist',
          (2*q/(1-q*q))/2-q/(1-q*q))
    for q0,c0 in [(S.Rational(1,5),S.Rational(2)),
                  (S.Rational(1,3),S.Rational(3,2)),
                  (S.Rational(1,7),S.Rational(3))]:
        c=(q0+1/q0)/2; c1=c*c/c0; sg=(1/q0-q0)/2
        check(f'physical_unequal_contacts_{q0}', c0>1 and c1>1 and c0!=c1)
        for j in (1,2,3,8):
            a0=c*sg/c1; ab=c*sg/(c1 if j%2==0 else c0)
            D=S.diag(S.sqrt(a0),S.sqrt(ab))
            Hj=D*M.subs(q,q0**j)*D
            exact(f'whiten_det_q{q0}_j{j}',Hj.det()-a0*ab)
            for i,k in ((0,0),(0,1),(1,1)):
                exact(f'whiten_entry_q{q0}_j{j}_{i}{k}',
                      (D.inv()*Hj*D.inv()-M.subs(q,q0**j))[i,k])
    # Compare an independent polar overlap integral, not the same closed formula.
    for qf in (.02,.15,.4,.8):
        lf=(1-qf)/(1+qf); crossing=math.atan(math.sqrt(lf))
        integral,err=quad(lambda th: min(1.0,1/(lf*math.cos(th)**2+
                            math.sin(th)**2/lf)),0,math.pi/2,
                            points=[crossing],epsabs=1e-12,epsrel=1e-12)
        tv=1-2*integral/math.pi
        close(f'polar_overlap_q{qf}',tv,2*math.asin(qf)/math.pi)
        check(f'quadrature_finite_q{qf}',err<1e-9,'ordinary_float')
    # Exact product support calculations, with nonidentical marginals and failures.
    for n in range(1,6):
        ds=[F(i+1,10+i) for i in range(n)]
        P=[[1-x,x,F(0)] for x in ds]; Q=[[1-x,F(0),x] for x in ds]
        tv=discrete_tv(product_law(P),product_law(Q))
        check(f'conditional_product_{n}',tv==1-math.prod(1-x for x in ds))
        if n<=4:
            ps=[F(i+1,12+i) for i in range(n)]
            P=[[1-p,p*(1-x),p*x,F(0)] for p,x in zip(ps,ds)]
            Q=[[1-p,p*(1-x),F(0),p*x] for p,x in zip(ps,ds)]
            tv=discrete_tv(product_law(P),product_law(Q))
            check(f'raw_product_{n}',tv==1-math.prod(1-p*x for p,x in zip(ps,ds)))
            # Reverse erasure kernel on the complete discrete transcript.
            a,b=product_law(P),product_law(Q)
            common=[min(x,y) for x,y in zip(a,b)]; mass=sum(common)
            exclusive=[x-y for x,y in zip(a,common)]
            rebuilt=[mass*(c/mass)+(1-mass)*(e/(1-mass)) for c,e in zip(common,exclusive)]
            check(f'erasure_reverse_kernel_{n}',rebuilt==a)
    for qf in (1e-2,1e-3,1e-4):
        b=.8; k=round(b/qf); delta=2*math.asin(qf)/math.pi
        actual=-math.expm1(k*math.log1p(-delta)); limit=-math.expm1(-2*b/math.pi)
        check(f'conditional_critical_profile_{qf}',abs(actual-limit)<2*qf,'ordinary_float')
        # General smooth joint scale d=q^3: k sqrt(d) tends to zero.
        check(f'positive_offset_joint_remainder_{qf}',k*math.sqrt(qf**3)<math.sqrt(qf),
              'ordinary_float')
    beta,zeta=S.symbols('beta zeta', real=True)
    Rot=S.Matrix([[-S.Rational(1,2),-S.sqrt(3)/2],
                  [S.sqrt(3)/2,-S.Rational(1,2)]])
    exact('physical_rotation_order_three',(Rot**3-S.eye(2)).norm())
    exact('no_fixed_linear_direction',(Rot-S.eye(2)).det()-3)
    v=Rot*S.Matrix([beta,zeta])
    exact('quadratic_rotation_invariance',v.dot(v)-beta**2-zeta**2)
    R,s=S.symbols('R s', positive=True)
    radii=[R+36*s,R-18*s,R-18*s]
    exact('radius_sum_common',sum(radii)-3*R)
    exact('radius_square_common',sum(x*x for x in radii)-(3*R*R+1944*s*s))
    exact('radius_cubic_odd_term',sum((x-R)**3 for x in radii)-34992*s**3)
    exact('middle_root_separation',1/(R-18*s)-1/(R+18*s)-36*s/(R*R-324*s*s))
    for ss in (F(1,2000),F(1,4000),F(1,8000)):
        rr=F(1,4); ka=sorted(1/(rr+x*ss) for x in (36,-18,-18))
        kb=sorted(1/(rr-x*ss) for x in (36,-18,-18))
        check(f'exact_curvature_matching_{ss}',max(abs(x-y) for x,y in zip(ka,kb))
              ==36*ss/(rr*rr-324*ss*ss))
    for p in (.001,.02,.15):
        for qf in (.002,.05,.2):
            kl=p*math.log(p/qf)+(1-p)*math.log((1-p)/(1-qf))
            check(f'bernoulli_kl_upper_{p}_{qf}',kl<=(p-qf)**2/(qf*(1-qf))+1e-14,
                  'ordinary_float')
            check(f'binary_pinsker_{p}_{qf}',kl+1e-14>=2*(p-qf)**2,'ordinary_float')
    # Exhaust all binary bracket histories at modest finite resolutions.
    # This checks interval arithmetic and cost, not statistical coverage of a billiard.
    for h in (F(1,4),F(1,8),F(1,16),F(1,32)):
        stack=[(F(0),F(1),F(0),0)]; terminals=[]; edges=[]
        while stack:
            L,U,cost,depth=stack.pop(); w=U-L
            if w<=h/2:
                terminals.append((L,U,cost,depth));continue
            t=(L+U)/2
            for nL,nU in ((L,t),(t-w/4,U)):
                edges.append((L,U,nL,nU))
                stack.append((nL,nU,cost+1/(w*w),depth+1))
        check(f'bracket_all_widths_{h}',all(U-L<=h/2 for L,U,_,_ in terminals))
        check(f'bracket_all_history_cost_{h}',all(cost<=F(64,7)/(h*h) for _,_,cost,_ in terminals))
        check(f'bracket_nested_{h}',all(L<=nL<nU<=U for L,U,nL,nU in edges))
        # A no-success update can discard a currently bracketed g only at d>w/4.
        good=True
        for L,U,nL,nU in edges:
            w=U-L;t=(L+U)/2
            if nL>L:
                for a in range(9):
                    gg=L+w*F(a,8)
                    if gg<nL:good=good and t-gg>w/4
        check(f'bracket_discard_requires_positive_margin_{h}',good)
    for n,p,r0 in ((200,.1,10),(400,.05,10),(800,.025,10),(120,.4,20)):
        tail=float(binom.cdf(r0-1,n,p)); bound=math.exp(-n*p/8)
        check(f'capped_wait_tail_{n}_{p}_{r0}',n*p>=2*r0 and tail<=bound,'ordinary_float')
    h,m,eps=S.symbols('h m eps', positive=True)
    exact('fixed_m_cost_substitution',S.expand((6+6/m)-(2*m+2)*3/m))
    exact('weighted_information_power',S.expand((6+6/m)-(6+2*3/m)))
    return {'schema':'a2-v7-finite-diagnostics-v1','status':'pass',
            'counts':{'total':len(checks),**dict(Counter(x['kind'] for x in checks))},
            'environment':{'python':platform.python_version(),'sympy':S.__version__,
                           'scipy':scipy.__version__},'checks':checks,
            'limits':['Finite exact algebra and ordinary noninterval floating-point tests.',
                      'Not a numerical simulation of billiard probabilities.',
                      'No formal certification of uniform operator estimates or all-order results.',
                      'No remote CI, journal endorsement, or priority certificate.']}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path)
    args=parser.parse_args();out=json.dumps(main(),indent=2,sort_keys=True)+'\n'
    if args.output:args.output.write_text(out,encoding='utf-8')
    print(out)
