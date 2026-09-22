#!/usr/bin/env python3
"""Exact, finite diagnostics for the new v21 arguments.

This module imports no author theorem/geometry implementation. Its explicit
predicates remain active under python -O. It is neither a proof verifier nor
an optimization over all encoders or continuous measures.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
from math import prod
from pathlib import Path
import hashlib
import json
import platform
import random
import sys
import sympy as S

CHECKS: Counter[str]=Counter()
CASES: Counter[str]=Counter()

def check(value, group: str):
    if value is not True and value != S.true:
        raise AssertionError(f'{group}: predicate failed ({value})')
    CHECKS[group]+=1

def case(group: str):
    CASES[group]+=1

def newton_extensions():
    group='collision_safe_ambient_extension'
    rng=random.Random(210907)
    configurations=[(0,), (0,0,0), (0,1), (0,1,1), (0,1,2,3),
                    (0,1,1,4,4), (0,1,8,9,20), (0,1,99,100)]
    configurations += [tuple(rng.randrange(7) for _ in range(rng.randrange(1,7)))
                       for _ in range(28)]
    for integers in configurations:
        case(group);H=max(integers)+1
        values=[S.Rational(x+1,H+1) for x in integers]
        remaining=list(range(len(values)));order=[];ds=[]
        first=min(remaining,key=lambda i:(values[i],i));order.append(first);remaining.remove(first);ds.append(S.Integer(1))
        while remaining:
            pivot=max(remaining,key=lambda i:(prod(abs(values[i]-values[j]) for j in order),-i))
            ds.append(prod(abs(values[pivot]-values[j]) for j in order))
            order.append(pivot);remaining.remove(pivot)
        x=[values[i] for i in order];q=len(x);s=len(set(x))
        L=S.zeros(q)
        for j in range(q):
            if ds[j]!=0:
                for i in range(q):
                    L[i,j]=prod(x[i]-x[k] for k in range(j))/ds[j]
        check(all(abs(v)<=1 for v in L),group)
        check(all(ds[i]>=ds[i+1]>=0 for i in range(q-1)),group)
        A=L[:s,:s];B=L[s:,:s]
        T=S.eye(q);T[:s,:s]=A.inv();T[s:,:s]=-B*A.inv()
        inv=S.eye(q);inv[:s,:s]=A;inv[s:,:s]=B
        check(T*inv==S.eye(q) and inv*T==S.eye(q),group)
        check(max(abs(v) for v in T)<=q*2**q,group)
        check(max(abs(v) for v in inv)<=1,group)
        D=S.diag(*ds)
        check(T*L*D==D,group)
        for weights in [(S.Rational(1,3),S.Rational(1,3),S.Rational(1,3)),
                        (S.Rational(1,7),S.Rational(2,7),S.Rational(4,7))]:
            raw=S.Matrix([sum(weights[k]*t**(z*(H+1)) for k,t in
                              enumerate([S.Integer(0),S.Rational(1,2),S.Integer(1)])) for z in x])
            coef=[]
            for j in range(s):
                div=raw[:j+1,:]
                # Distinct first s nodes: ordinary Newton divided differences.
                temp=list(div)
                for level in range(1,j+1):
                    temp=[(temp[i+1]-temp[i])/(x[i+level]-x[i]) for i in range(len(temp)-1)]
                coef.append(temp[0])
            scaled=S.Matrix([ds[i]*coef[i] if i<s else 0 for i in range(q)])
            check(T*raw==scaled,group)
        for ell in range(1,q+1):
            v=max(prod(abs(x[i]-x[j]) for i,j in combinations(J,2)) for J in combinations(range(q),ell))
            p=prod(ds[:ell]);check(p<=v<=S.factorial(ell)*p,group)

def common_independence():
    group='finite_common_independence_and_cauchy_binet';rng=random.Random(200921)
    models=[(S.zeros(1,2),S.Matrix([[1,2]])),
            (S.Matrix([[1,1,1,1],[1,0,0,0],[0,1,0,0]]),
             S.Matrix([[1,1,1,1],[0,0,1,0],[0,0,0,1]]))]
    for n,d,k in [(3,2,2),(4,2,3),(4,3,2),(5,3,3),(2,1,2),(3,3,1)]:
        models.append((S.Matrix(d,n,[rng.randrange(-2,3) for _ in range(d*n)]),
                       S.Matrix(k,n,[rng.randrange(-2,3) for _ in range(k*n)])))
    for A,B in models:
        case(group);n=A.cols;w=S.symbols(f'w0:{n}');H=A*S.diag(*w)*B.T
        common=0
        for ell in range(1,min(A.rows,B.rows,n)+1):
            independent=any(A[:,list(J)].rank()==ell and B[:,list(J)].rank()==ell
                            for J in combinations(range(n),ell))
            if independent:common=ell
            for I in combinations(range(A.rows),ell):
                for J in combinations(range(B.rows),ell):
                    rhs=sum(A.extract(I,T).det()*B.extract(J,T).det()*prod(w[i] for i in T)
                            for T in combinations(range(n),ell))
                    check(S.expand(H.extract(I,J).det()-rhs)==0,group)
        check(H.rank()==common,group)
        attained=False
        for trial in range(10):
            positive=[S.Integer(rng.randrange(1,12)) for _ in range(n)];total=sum(positive)
            rank=(A*S.diag(*positive)*B.T).rank()
            normalized=[v/total for v in positive]
            check((A*S.diag(*normalized)*B.T).rank()==rank,group)
            check(rank<=common,group)
            attained |= rank==common
        check(attained,group)

def moving_kernel():
    group='square_moving_kernel_physical_covariance'
    pairings=[]
    for total in range(4,10):
        for a,b,c in product(range(1,total-2),repeat=3):
            d=total-a-b-c
            if d<=0:continue
            case(group);p=list(map(lambda v:S.Rational(v,total),(a,b,c,d)))
            p1,p2,p3,p4=p
            H=S.Matrix([[1,p3,p4],[p1,0,0],[p2,0,0]])
            check(H.det()==0 and H.rank()==2,group)
            check(H*S.Matrix([0,p4,-p3])==S.zeros(3,1),group)
            if len(pairings)<2 and (not pairings or p3/p4!=pairings[0][1]):
                pairings.append((H,p3/p4))
            f=S.Matrix([[S.Rational(1,4),0],[0,S.Rational(1,4)],[0,0],[0,0]])
            g=S.Matrix([[S.Rational(1,2),S.Rational(1,2)],
                        [S.Rational(1,2),S.Rational(1,2)],
                        [S.Rational(3,4),S.Rational(1,2)],
                        [S.Rational(1,2),S.Rational(3,4)]])
            D=S.diag(*p);meanf=S.Matrix(1,4,p)*f;meang=S.Matrix(1,4,p)*g
            # Work in sqrt(2)-rescaled units to keep all arithmetic rational.
            C=g.T*D*f-meang.T*meanf
            expected=-S.Matrix([p3,p4])*S.Matrix([[p1,p2]])/16
            check(C==expected and C.rank()==1,group)
            scale_sq=(p1*p1+p2*p2)*(p3*p3+p4*p4)/512
            check(S.trace(C*C.T)/2==scale_sq,group)
            u=S.Matrix([S.Rational(2,3),-S.Rational(1,3)])
            m=(meanf*u)[0]
            likelihood=S.ones(4,1)/2+f*u/2
            check(all(S.Rational(3,8)<=v<=S.Rational(5,8) for v in likelihood),group)
            posterior=S.Matrix(1,4,[p[i]*likelihood[i] for i in range(4)])/(S.Matrix(1,4,p)*likelihood)[0]
            prediction=posterior*g
            check(prediction.T==meang.T+C*u/(1+m),group)
    check(len(pairings)==2 and pairings[0][0].col_join(pairings[1][0]).rank()==3,group)

def feasibility_and_remaining_updates():
    group='dimension_free_feasibility'
    G=S.Matrix([[-1,0],[1,0],[0,-1],[0,1]])
    for numerator in [(1,1,1,1),(1,2,3,4),(6,2,1,3),(1,7,3,8)]:
        case(group);p=S.Matrix(1,4,[S.Rational(x,sum(numerator)) for x in numerator])
        delta=S.Rational(1,8);z=-delta*(p*G)/(1-delta)
        nu=S.Matrix([[S.Rational(1,4)-z[0]/2,S.Rational(1,4)+z[0]/2,
                      S.Rational(1,4)-z[1]/2,S.Rational(1,4)+z[1]/2]])
        mu=delta*p+(1-delta)*nu
        check(all(x>0 for x in nu) and sum(nu)==1,group)
        check(mu*G==S.zeros(1,2) and sum(mu)==1 and all(x>0 for x in mu),group)
        # W=0 and F larger than E are valid feasibility configurations.
        check(p*S.zeros(4,0)==S.zeros(1,0),group)
    group='raw_remaining_moment_updates'
    xs=[S.Integer(0),S.Rational(1,4),S.Rational(1,2),S.Integer(1)]
    p=[S.Rational(1,10),S.Rational(2,10),S.Rational(3,10),S.Rational(4,10)]
    q=list(reversed(p));coef=[S.Rational(1,2),S.Rational(1,16),-S.Rational(1,16)]
    def indices(m):return [I for I in product(range(m+1),repeat=3) if sum(I)==m]
    for a in [(0,1,2),(0,1,3),(0,2,4)]:
        likelihood=[sum(coef[i]*x**a[i] for i in range(3)) for x in xs]
        for m in range(2,5):
            case(group);idx=indices(m);lower=indices(m-1)
            def moments(weights):return {I:sum(weights[j]*xs[j]**sum(I[i]*a[i] for i in range(3)) for j in range(4)) for I in idx}
            def update(v):
                denom=sum(coef[i]*v[tuple((m-1 if k==0 else 0)+(k==i) for k in range(3))] for i in range(3))
                return {I:sum(coef[i]*v[tuple(I[k]+(k==i) for k in range(3))] for i in range(3))/denom for I in lower},denom
            for t in [S.Integer(0),S.Rational(1,3),S.Rational(1,2),S.Integer(1)]:
                weights=[(1-t)*p[i]+t*q[i] for i in range(4)]
                v=moments(weights);got,denom=update(v)
                evidence=sum(weights[i]*likelihood[i] for i in range(4))
                check(denom==evidence and denom>=S.Rational(7,16),group)
                post=[weights[i]*likelihood[i]/evidence for i in range(4)]
                for I in lower:
                    direct=sum(post[j]*xs[j]**sum(I[i]*a[i] for i in range(3)) for j in range(4))
                    check(got[I]==direct,group)
            vp,vq=moments(p),moments(q);up,_=update(vp);uq,_=update(vq)
            norm=max(abs(vp[I]-vq[I]) for I in idx)
            # Uniform quotient-rule infinity norm bound with kappa=7/16.
            c=sum(abs(v) for v in coef);kap=S.Rational(7,16)
            check(max(abs(up[I]-uq[I]) for I in lower)<=(c/kap+c*c/kap**2)*norm,group)

def causal_recurrence():
    group='unequal_budget_causal_recurrence'
    schedules=[([F(1),F(1,2),F(3,4),F(1)], [F(1),F(1,3),F(1,4),F(0)], [1,2,3,5]),
               ([F(0),F(1),F(0),F(1,2)], [F(1),F(0),F(0),F(1,5)], [4,1,7,2]),
               ([F(1),F(0),F(1),F(1)], [F(0),F(1,2),F(0),F(1,10)], [2,3,1,4])]
    inputs=(F(-1),F(-1,3),F(0),F(1,3),F(1))
    for lambdas,bs,budgets in schedules:
        radii=[];R=F(0);codebooks=[]
        for L,b,M in zip(lambdas,bs,budgets):
            R=L*R+b;radii.append(R)
            codebooks.append([F(0)] if R==0 else [-R+F(2*j+1,M)*R for j in range(M)])
        for us in product(inputs,repeat=4):
            case(group);true=F(0);retained=F(0);e=F(0);steps=[]
            for n,(L,b,M,u,R,codebook) in enumerate(zip(lambdas,bs,budgets,us,radii,codebooks)):
                true=L*true+b*u
                # This transition sees the representative and current input only.
                candidate=L*retained+b*u
                retained=min(codebook,key=lambda z:(abs(z-candidate),z))
                r=R/M;steps.append(r);e=L*e+r
                convolution=sum(steps[j]*prod(lambdas[i] for i in range(j+1,n+1)) for j in range(n+1))
                check(e==convolution,group)
                check(abs(candidate)<=R and abs(retained)<=R,group)
                check(abs(retained-candidate)<=r,group)
                check(abs(true-retained)<=e,group)
                check(len(codebook)<=M,group)
                check(e<=(n+1)*max(steps),group)

def main():
    newton_extensions();common_independence();moving_kernel()
    feasibility_and_remaining_updates();causal_recurrence()
    receipt={'version':21,'passed':True,'python':platform.python_version(),
        'sympy':S.__version__,'assertions':sum(CHECKS.values()),'cases':sum(CASES.values()),
        'groups':{g:{'cases':CASES[g],'explicit_checks':CHECKS[g]} for g in CHECKS},
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'scope':'Executed exact finite diagnostics. No imported author theorem code; not proof verification or exhaustive minimax optimization.'}
    output=Path(sys.argv[1]) if len(sys.argv)>1 else Path('V21_CHECK_RESULTS.json')
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))

if __name__=='__main__':main()
