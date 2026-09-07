#!/usr/bin/env python3
"""Exact finite diagnostics for v19; not formal verification of the theorems.

Uses SymPy 1.14.0 for symbolic identities. Assertions remain enabled under
python -O because check() explicitly raises on a failed condition.
"""
from __future__ import annotations
from collections import Counter
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import platform
import random
import sys
import sympy as S

COUNTS=Counter()
def check(condition, group):
    if condition is not True and condition != S.true:
        raise AssertionError(group+': '+str(condition))
    COUNTS[group]+=1

def same(a,b,group):
    check(S.cancel(S.together(a-b))==0,group)

def moment_witnesses():
    X=(-1,0,1)
    for c in (S.Rational(1,7),S.Rational(1,2),S.Rational(4,5)):
        mu=[c/3+(1-c)/2,c/3,c/3+(1-c)/2]
        same(sum(mu),1,'full_support_kernel_witness')
        check(all(w>0 for w in mu),'full_support_kernel_witness')
        for k in (1,3):
            same(sum(w*x**k for x,w in zip(X,mu)),0,'full_support_kernel_witness')
    # Entire two-dimensional kernel, not merely one selected vector.
    signs=list(product((-1,1),repeat=2))
    E=S.Matrix([[1 for _ in signs],[x for x,z in signs]])
    F=S.Matrix([[z for x,z in signs],[x*z for x,z in signs]])
    H=E*F.T/4
    check(H==S.zeros(2),'simultaneous_kernel_moments')
    check(E.rank()==F.rank()==2,'simultaneous_kernel_moments')
    # Exact dominated-margin formula for a scalar positive integrand.
    for c in (S.Rational(1,8),S.Rational(1,2),S.Integer(1)):
        vertices=[2*c+(1-c)*x for x in (1,2,3)]
        same(min(vertices),1+c,'dominated_margin_identity')

PTS=[(0,0),(2,0),(3,1),(1,3),(-1,1)]
def pentagon():
    separators=[(1,3,-1),(0,2,-1),(-1,1,-1),(-2,0,-1)]
    for j,(a,b,c) in enumerate(separators):
        vals=[a*x+b*y+c for x,y in PTS]
        check(all(v<0 for v in vals[:j+1]),'rectangular_separators')
        check(all(v>0 for v in vals[j+1:]),'rectangular_separators')
        for threshold in (S.Rational(2*j+1,2),S.Integer(j),S.Integer(j+1)):
            prods=[(i-threshold)*v for i,v in enumerate(vals)]
            check(all(z>=0 for z in prods) and any(z>0 for z in prods),
                  'rectangular_separators')
    E=S.Matrix([[1]*5,[x for x,y in PTS],[y for x,y in PTS]])
    F=S.Matrix([[1]*5,list(range(5))])
    for w0 in product((1,2,3),repeat=5):
        w=[S.Rational(z,sum(w0)) for z in w0]
        H=E*S.diag(*w)*F.T
        check(H.rank()==2,'positive_weight_rectangular_rank')
        mh=sum(w[i]*i for i in range(5))
        cov=[sum(w[i]*i*PTS[i][j] for i in range(5))-
             mh*sum(w[i]*PTS[i][j] for i in range(5)) for j in range(2)]
        check(any(v!=0 for v in cov),'normalized_rectangular_rank')
        for j in range(2):
            # Actual posterior derivative, with acquisition f=z/8 and query g=1/4+h/8.
            g=[S.Rational(1,4)+S.Rational(i,8) for i in range(5)]
            mean=sum(wi*gi for wi,gi in zip(w,g))
            derivative=(sum(w[i]*g[i]*PTS[i][j]/8 for i in range(5))-
                        mean*sum(w[i]*PTS[i][j]/8 for i in range(5)))
            same(derivative,cov[j]/64,'normalized_rectangular_rank')
    for a,b in product(range(-6,7),repeat=2):
        differences=[2*a,a+b,-2*a+2*b,-2*a-2*b]
        monotone=all(z>=0 for z in differences) or all(z<=0 for z in differences)
        check(monotone==(a==b==0),'evidence_preserving_square_check')
    for x,y in PTS:
        check(abs(x)+abs(y)<=4,'physical_pentagon_positivity')
        for ux,uy in product((-1,1),repeat=2):
            for report in (-1,1):
                check((1+report*S.Rational(ux*x+uy*y,8))/2>=S.Rational(1,4),
                      'physical_pentagon_positivity')

def walsh():
    for b,q in ((1,1),(1,2),(2,2),(2,3),(3,2)):
        symbols=S.symbols('a0:'+str(b*q))
        A=S.Matrix(q,b,symbols)
        points=list(product((-1,1),repeat=b+q))
        def mean(fun):
            return S.expand(sum(fun(p)*(1+sum(A[j,i]*p[i]*p[b+j]
                for j in range(q) for i in range(b))) for p in points)/len(points))
        same(mean(lambda p:1),1,'symbolic_walsh_normalization')
        for i in range(b):
            same(mean(lambda p:p[i]),0,'symbolic_walsh_means')
        for j in range(q):
            same(mean(lambda p:p[b+j]),0,'symbolic_walsh_means')
            for i in range(b):
                same(mean(lambda p:p[i]*p[b+j]),A[j,i],'symbolic_walsh_cross_moments')
                g=lambda p:S.Rational(1,2)+S.Rational(1,4)*p[b+j]
                f=lambda p:S.Rational(p[i],2*b)
                cov=mean(lambda p:g(p)*f(p))-mean(g)*mean(f)
                same(cov/S.sqrt(q),A[j,i]/(8*b*S.sqrt(q)),
                     'physical_weighted_covariance')
        vals=[S.Rational((-1)**i,2*b*q) for i in range(b*q)]
        for p in points:
            density=1+sum(vals[j*b+i]*p[i]*p[b+j] for j in range(q) for i in range(b))
            check(S.Rational(1,2)<=density<=S.Rational(3,2),'uniform_prior_density')
            for u in product((-1,1),repeat=b):
                for report in (-1,1):
                    likelihood=(1+report*sum(S.Rational(u[i]*p[i],2*b) for i in range(b)))/2
                    check(S.Rational(1,4)<=likelihood<=S.Rational(3,4),'fixed_physical_positivity')

def order(poly,t):
    p=S.Poly(S.expand(poly),t)
    return S.oo if p.is_zero else min(m[0] for m,c in p.terms() if c!=0)

def determinantal_orders():
    t=S.Symbol('t')
    C=S.Matrix([[t,t**2],[t**2,t**3+t**5]])
    same(C.det(),t**6,'two_scale_exact_determinant')
    U=S.Matrix([[1,0],[-t,1]]);V=S.Matrix([[1,-t],[0,1]])
    check(U*C*V==S.diag(t,t**5),'two_scale_explicit_smith')
    rng=random.Random(190907)
    for q,b in ((2,3),(3,2),(3,3)):
        for alpha in ((0,2),(1,5),(0,0),(2,2)):
            D=S.zeros(q,b)
            for i,a in enumerate(alpha):D[i,i]=t**a
            L=S.eye(q);R=S.eye(b)
            # Unit triangular multipliers with polynomial off-diagonals.
            for i in range(q-1):L[i,i+1]=rng.randint(-2,2)*t+t*t
            for i in range(b-1):R[i+1,i]=rng.randint(-2,2)+t
            B=L*D*R
            same(L.det(),1,'analytic_unit_multipliers')
            same(R.det(),1,'analytic_unit_multipliers')
            for ell in range(1,min(q,b)+1):
                orders=[order(B.extract(I,J).det(),t)
                        for I in combinations(range(q),ell)
                        for J in combinations(range(b),ell)]
                expected=sum(alpha[:ell]) if ell<=len(alpha) else S.oo
                check(min(orders)==expected,'rectangular_minor_valuation')
            check(B.subs(t,0).rank()==sum(a==0 for a in alpha),'rank_zero_endpoint')

def phases():
    for length in range(1,5):
        for alpha in product(range(4),repeat=length):
            if tuple(sorted(alpha))!=alpha:continue
            A=[sum(alpha[:ell]) for ell in range(1,length+1)]
            beta=[ell*alpha[ell]-A[ell-1] for ell in range(1,length)]
            check(beta==sorted(beta) and all(x>=0 for x in beta),'ordered_phase_breaks')
            for i in range(len(beta)-1):
                same(beta[i+1]-beta[i],(i+2)*(alpha[i+2]-alpha[i+1]),'phase_break_differences')
            for gamma in [S.Rational(k,2) for k in range(25)]:
                vals=[2*(S.Integer(A[i])+gamma)/(i+1) for i in range(length)]
                for i in range(length):
                    lower=0 if i==0 else beta[i-1]
                    upper=S.oo if i==length-1 else beta[i]
                    if lower<=gamma<=upper:
                        check(vals[i]==min(vals),'all_phase_branches')
    same(1*5-1,4,'two_scale_crossover')
    for t in (S.Rational(1,2),S.Rational(1,3),S.Rational(1,7)):
        M=t**-4
        same(t**2/M**2,t**6/M,'two_scale_crossover')
        for m in (1,2,3,8,15):
            # This is an exact profile check, not optimization over all encoders.
            check(max(t**2/m**2,t**6/m)>0,'integer_budget_profile')

def main():
    moment_witnesses();pentagon();walsh();determinantal_orders();phases()
    report={'version':19,'passed':True,'python':platform.python_version(),
            'sympy':S.__version__,'arithmetic':'exact rational and symbolic',
            'assertions':sum(COUNTS.values()),'groups':dict(sorted(COUNTS.items())),
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'scope':'Finite identities and selected exact examples only. Does not certify universal quantifiers, compactness constants, minimax optimization, or journal significance.'}
    target=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/'validation/V19_DIAGNOSTICS.json'
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
