#!/usr/bin/env python3
"""Exact regression checks for saturation, integer covers, and risk ordering.

These finite rational checks do not prove density or covering theorems.
No assert statements: optimized execution must give an identical receipt.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
from itertools import product,combinations
from pathlib import Path
import hashlib,json,sys
COUNTS=Counter()
def check(group,condition):
    COUNTS[group]+=1
    if not condition: raise ValueError(f'{group}: check {COUNTS[group]} failed')
def rank(rows):
    a=[list(map(F,row)) for row in rows];r=0
    for j in range(len(a[0]) if a else 0):
        p=next((i for i in range(r,len(a)) if a[i][j]),None)
        if p is None:continue
        a[r],a[p]=a[p],a[r];v=a[r][j];a[r]=[x/v for x in a[r]]
        for i in range(len(a)):
            if i!=r:
                v=a[i][j];a[i]=[x-v*y for x,y in zip(a[i],a[r])]
        r+=1
    return r
def prod(xs):
    out=F(1)
    for x in xs:out*=x
    return out
def root_upper(x,j):
    if not x:return F(0)
    lo,hi=F(0),max(F(1),x)
    for _ in range(56):
        mid=(lo+hi)/2
        if mid**j>=x:hi=mid
        else:lo=mid
    return hi
def ceil(x):return -(-x.numerator//x.denominator)
def saturation():
    cases=0
    for d in range(1,5):
        for tau in product((F(0),F(1,17),F(1)),repeat=d):
            vals=[(F(0),)*d]+[tuple(tau[j] if i==j else F(0) for j in range(d)) for i in range(d)]
            for mask in range(1,1<<(d+1)):
                weights=[F((i+1) if (mask>>i)&1 else 0) for i in range(d+1)]
                p=[x/sum(weights) for x in weights]
                mean=[sum(p[i]*vals[i][j] for i in range(d+1)) for j in range(d)]
                cov=[[sum(p[i]*(vals[i][j]-mean[j])*(vals[i][k]-mean[k]) for i in range(d+1)) for k in range(d)] for j in range(d)]
                supported={vals[i] for i in range(d+1) if p[i]}
                t=len(supported)
                check('observable_quotient_rank',rank(cov)==t-1)
                check('affine_evaluation_rank',rank([[F(1),*x] for x in supported])==t)
                cases+=1
    return cases
def covers_and_profiles():
    cases=0
    for d in range(1,5):
        for scales in combinations((F(0),F(1,1024),F(1,32),F(1,3),F(1)),d):
            lam=sorted(scales,reverse=True);k=sum(x>0 for x in lam);lam=lam[:k]
            V=[F(1)]+[prod(lam[:j]) for j in range(1,k+1)]
            for M in (1,2,3,7,31,128,1025):
                if not k:
                    check('zero_rank_exact',len(lam)==0);continue
                e=max(root_upper(V[j]/M,j) for j in range(1,k+1))
                A=F(8*d*d);eps=A*e
                check('profile_branches',all(V[j]<=M*e**j for j in range(1,k+1)))
                if M==1:
                    check('one_label_radius',e>=lam[0])
                else:
                    # Coordinate side eps/d has Euclidean diameter <= eps.
                    cells=prod(max(1,ceil(2*d*x/eps)) for x in lam)
                    check('integer_reachable_grid_cardinality',cells<=M)
                    grid_bound=prod(1+2*d*x/eps for x in lam)
                    check('grid_bound',cells<=grid_bound)
                    check('integer_constant_term',grid_bound<=1+F(M,2)<=M)
                cases+=1
            for j in range(1,k+1):
                M0=V[j]/lam[j-1]**j
                check('integer_inverse_budget',M0>=1)
                check('integer_inverse_branches',all(V[i]<=M0*lam[j-1]**i for i in range(1,k+1)))
                check('integer_inverse_rounding',ceil(M0)*lam[j-1]**j<=2*V[j])
    return cases
def risk_order_and_collision_example():
    # Generic decision table, not a claim that these are a particular experiment's optima.
    rows=[(F(i,20),1-F(i,20)) for i in range(21)]
    inf_max=min(max(row) for row in rows)
    max_inf=max(min(row[j] for row in rows) for j in range(2))
    check('infimum_maximum_negative_control',inf_max==F(1,2) and max_inf==0)
    A=(0,1,3);future={x+y for x in A for y in A}
    check('acquired_dimension_example',len(future)-1==5 and min(len(A)-1,len(future)-1)==2)
    # Physical menu identity tested exactly, with no square-root covariance scaling.
    for d in range(1,5):
        delta=F(1,4*d)
        for s in range(1,6):
            v=[F(i,2*d) for i in range(d)];w=[-x for x in v]
            errors=[F(0)]+[F(1,2**s)*delta*(x-y) for x,y in zip(v,w)]
            lhs=sum(x*x for x in errors)/(d+1)
            rhs=F(1,2**(2*s))*delta**2*sum((x-y)**2 for x,y in zip(v,w))/(d+1)
            check('physical_metric_identity',lhs==rhs)
def main():
    model_cases=saturation();grid_cases=covers_and_profiles();risk_order_and_collision_example()
    report={'version':23,'passed':True,'assertions':sum(COUNTS.values()),
       'groups':dict(sorted(COUNTS.items())),'observable_models':model_cases,
       'integer_grid_cases':grid_cases,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
       'scope':'Finite exact rational author regression tests, not proof or independent referee certification.'}
    text=json.dumps(report,indent=2)+'\n'
    if len(sys.argv)>1:Path(sys.argv[1]).write_text(text)
    print(text,end='')
if __name__=='__main__':main()
