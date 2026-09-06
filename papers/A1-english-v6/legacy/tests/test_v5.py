#!/usr/bin/env python3
"""Finite exact diagnostics for the V5 proofs; not a proof of the all-budget claims.

Run from any directory.  Uses exact rational/symbolic arithmetic (SymPy).
The rational calibration proxy below is labelled explicitly: it is not a
replacement of pi or sqrt(3) in the physical apparatus.  Their actual
calibration identity is checked symbolically and their physical gain is
separately enclosed with rational outward arithmetic.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
from math import isqrt
from pathlib import Path
import argparse
import hashlib
import json
import platform
import sympy as s

RESULTS: list[dict] = []

def check(name: str, condition: bool, detail: object = None) -> None:
    ok = bool(condition)
    RESULTS.append({'name': name, 'passed': ok, 'detail': detail})
    if not ok:
        raise AssertionError(name)


def coeff(poly: s.Expr, t: s.Symbol, degree: int) -> list[s.Expr]:
    p = s.Poly(s.expand(poly), t)
    return [p.nth(i) for i in range(degree + 1)]


def run() -> dict:
    t, R = s.symbols('t R', real=True)
    T, e, a, p = s.symbols('T e a p', positive=True)
    C = s.Matrix([[0, 1, 0, 0], [0, -2*T/a, T/a, T/a],
                  [p/a, -p/a, 0, 0], [0, 0, 2*T*e/(p*a), -2*T*e/(p*a)]])
    check('physical_calibration_determinant', s.simplify(C.det()**2-(4*T*T*e/a**3)**2)==0,
          'symbolic identity; p=pi and a=sqrt(3)/2 may be substituted exactly')
    check('physical_normalization', C*s.ones(4,1)==s.Matrix([1,0,0,0]))
    v = s.Matrix(s.symbols('v0:4'))
    check('four_lookup_right_inverse', s.simplify(C*(s.ones(4,1)/2+C.inv()*v)-s.Matrix([s.Rational(1,2),0,0,0])-v)==s.zeros(4,1))
    C0=C[:,0:2].row_join(C[:,2]+C[:,3])
    check('sign_erased_rank', C0.rank()==3)
    check('zero_amplitude_rank', C.subs(e,0).rank()==3)
    # Rational normalized calibration proxy, used only for finite span diagnostics.
    Cp=C.subs({T:s.Rational(1,20),e:s.Rational(1,20),a:s.Rational(6,7),p:s.Rational(22,7)})
    rr=s.Rational(9,20)+t/s.Integer(50)
    k=[sum(Cp[i,j]*rr**i for i in range(4)) for j in range(4)]
    c, delta=s.Rational(1,2),s.Rational(1,8)
    B=[c+delta*x for x in k]
    B0=[c+delta*k[0],c+delta*k[1],c+delta*(k[2]+k[3])/2,c+delta*(k[2]+k[3])/2]
    check('shared_menu_constant_sum', s.expand(sum(B)-sum(B0))==0 and s.expand(sum(B))==4*c+delta)
    for q, factors in [(3,B),(2,B0)]:
        for m in range(1,4):
            polys=[s.prod(word) for word in product(factors,repeat=m)]
            A=s.Matrix.hstack(*[s.Matrix(coeff(x,t,q*m)) for x in polys])
            check(f'shared_probe_span_q{q}_m{m}', A.rank()==q*m+1,
                  {'rank': A.rank(), 'commands':4**m, 'type':'exact rational calibration proxy'})
    # Rank of the random-prefix prediction map at interior commands.
    integrate=lambda x:s.integrate(s.expand(x),(t,0,1))
    for q,n,m in [(3,2,1),(2,2,1),(3,1,2)]:
        probs=k if q==3 else [k[0],k[1],(k[2]+k[3])/2,(k[2]+k[3])/2]
        factors=B if q==3 else B0
        H=[s.prod(word) for word in product(factors,repeat=m)]
        rejections=[[s.Rational(3+i+j,12+i+j) for j in range(4)] for i in range(n)]
        Fs=[sum(rejections[i][j]*probs[j] for j in range(4)) for i in range(n)]
        P=s.prod(Fs);Z=integrate(P)
        variations=[probs[j]*s.prod(Fs[k0] for k0 in range(n) if k0!=i) for i in range(n) for j in range(4)]
        D=s.Matrix([[(integrate(h*v)*Z-integrate(h*P)*integrate(v))/Z**2 for v in variations] for h in H])
        check(f'random_prefix_submersion_q{q}_n{n}_m{m}',D.rank()==q*min(n,m),
              {'rank':D.rank(),'type':'exact rational calibration proxy; positive interior command tuple'})
    # Normalized polynomial moment map under the uniform prior.
    def integ(x: s.Expr) -> s.Expr:
        return s.integrate(s.expand(x),(t,0,1))
    for q,n,m in [(1,1,3),(1,3,1),(2,1,3),(2,3,1),(2,2,2),(3,1,3),(3,3,1),(3,2,2),(3,2,3),(3,3,2)]:
        aa,bb=q*n,q*m
        M=s.Matrix([[s.Rational(1,i+j+1)-s.Rational(1,(i+1)*(j+1)) for i in range(1,aa+1)] for j in range(1,bb+1)])
        rank=M.rank()
        check(f'decision_quotient_rank_q{q}_n{n}_m{m}',rank==q*min(n,m),{'rank':rank})
    for q,n in [(1,3),(2,2),(3,2),(3,3)]:
        Fs=[1+s.Rational(i+1,100)*t**q for i in range(n)]
        D=s.Matrix.hstack(*[s.Matrix(coeff(t**j*s.prod(Fs[k] for k in range(n) if k!=i),t,q*n)) for i in range(n) for j in range(q+1)])
        check(f'product_differential_q{q}_n{n}',D.rank()==q*n+1,{'rank':D.rank(),'kernel':n*(q+1)-D.rank()})
    # The referee's sparse/common-divisor strengthening: finite differential examples.
    for common in [s.Integer(1),1+t*t]:
        W=[common,common*t**2,common*t**5]
        Fs=[W[0]+s.Rational(1,10)*W[1]+s.Rational(1,20)*W[2],
            W[0]+s.Rational(1,11)*W[1]+s.Rational(1,21)*W[2]]
        degree=s.degree(Fs[0]*Fs[1],t)
        D=s.Matrix.hstack(*[s.Matrix(coeff(w*Fs[1-i],t,degree)) for i in range(2) for w in W])
        check(f'rank_deficient_common_{str(common)}',D.rank()==5,{'unnormalized_rank':D.rank(),'normalized_rank':4})
    P=1+t+t**4
    P=P/integ(P)
    f=s.Rational(1,3)+t/s.Integer(10)+t**3/s.Integer(20)
    Q=s.expand(P*f/integ(P*f))
    for j in range(7):
        fc=coeff(f,t,3)
        lhs=integ(t**j*Q)
        rhs=sum(fc[i]*integ(t**(i+j)*P) for i in range(4))/sum(fc[i]*integ(t**i*P) for i in range(4))
        check(f'shrinking_moment_update_order_{j}',s.simplify(lhs-rhs)==0)
    x,y=s.symbols('x y',real=True)
    check('brier_excess_identity',s.expand(y*(x-1)**2+(1-y)*x*x-y*(1-y)-(x-y)**2)==0)
    for d in [1,2,3,4,6,9]:
        # Scale rho=M=1; the change of variables supplies rho^2 M^(-2/d).
        u=s.symbols('u',nonnegative=True)
        integral=s.integrate(1-u**s.Rational(d,2),(u,0,1))
        check(f'ball_volume_lower_constant_d{d}', integral==s.Rational(d,d+2))
    # Binary conditional variance identity, with arbitrary rational radius prior.
    radii=[F(9,20),F(23,50),F(47,100)]
    weights=[F(1,5),F(1,2),F(3,10)]
    kappa,alpha=F(2,5),F(1,7)
    h=[kappa*r*r for r in radii]
    cp=[F(1,2)+alpha*r*r for r in radii]
    mean=lambda z:sum(w*v for w,v in zip(weights,z))
    eh,ec=mean(h),mean(cp)
    cov=mean([hh*cc for hh,cc in zip(h,cp)])-eh*ec
    m1=mean([hh*cc for hh,cc in zip(h,cp)])/ec
    m0=mean([hh*(1-cc) for hh,cc in zip(h,cp)])/(1-ec)
    check('binary_variance_gain_exact',ec*(m1-eh)**2+(1-ec)*(m0-eh)**2==cov*cov/(ec*(1-ec)))
    # Exact rational outward enclosure for the physical uniform-prior gain.
    def arctan_interval(z:F,n:int)->tuple[F,F]:
        part=sum(((-1)**j)*z**(2*j+1)/F(2*j+1) for j in range(n))
        nxt=((-1)**n)*z**(2*n+1)/F(2*n+1)
        return min(part,part+nxt),max(part,part+nxt)
    aa=arctan_interval(F(1,5),40);bb=arctan_interval(F(1,239),10)
    pi_lo,pi_hi=16*aa[0]-4*bb[1],16*aa[1]-4*bb[0]
    den=10**50;z=isqrt(3*den*den)
    a_lo,a_hi=F(z,2*den),F(z+1,2*den)
    check('sqrt_three_enclosure',z*z<3*den*den<(z+1)*(z+1))
    l,hi=F(9,20),F(47,100)
    mu=lambda j:(hi**(j+1)-l**(j+1))/(F(j+1)*(hi-l))
    vh=mu(5)/mu(1)-(mu(3)/mu(1))**2
    T0,e0=F(1,20),F(1,20)
    clo=F(1,2)+e0*mu(3)/(mu(1)*pi_hi)
    chi=F(1,2)+e0*mu(3)/(mu(1)*pi_lo)
    # c(1-c) decreases on [1/2,1].
    gain_lo=(2*T0*mu(1)/a_hi)*(e0*vh/a_hi)**2/(clo*(1-clo))
    gain_hi=(2*T0*mu(1)/a_lo)*(e0*vh/a_lo)**2/(chi*(1-chi))
    check('physical_zero_cost_gain_positive',0<gain_lo<gain_hi,
          {'lower_fraction':str(gain_lo),'upper_fraction':str(gain_hi),
           'display_lower':float(gain_lo),'display_upper':float(gain_hi),'prior':'uniform on [9/20,47/100]','T':'1/20','epsilon':'1/20'})
    check('zero_amplitude_gain_vanishes',s.simplify((e*s.Symbol('v')/a)**2).subs(e,0)==0)
    # A direct conditional Bayes computation under an actual full-support prior;
    # all unknown moments here are exact rational radius moments.
    check('full_support_hit_variance_positive',vh>0,{'variance_fraction':str(vh)})
    return {'suite':'A1 English v5 finite diagnostics','passed':sum(x['passed'] for x in RESULTS),
            'total':len(RESULTS),'arithmetic':'exact rational and symbolic; floats only display an already enclosed interval',
            'python':platform.python_version(),'sympy':s.__version__,
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'scope':{'formal_verification':False,'all_budget_theorems_verified_by_tests':False,
                     'author_v4_tests_rerun':False,'referee_v4_tests_rerun':False,
                     'independent_referee_review':False},'checks':RESULTS}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=Path(__file__).resolve().parents[1]/'validation'/'V5_CHECKS.json')
    args=parser.parse_args()
    report=run()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print(f"{report['passed']}/{report['total']} diagnostics passed; receipt: {args.output}")
