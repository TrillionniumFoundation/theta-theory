#!/usr/bin/env python3
"""Independent finite rational checks for A2 v69; no author code is imported.

These are diagnostics, not a proof of the billiard inverse, a concentration
inequality, an infinite-dimensional limit, or a minimax lower bound.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
from math import comb, prod
import json

def require(ok:bool,message:str)->None:
    if not ok: raise ValueError(message)

def solve(matrix:list[list[F]],rhs:list[F])->list[F]:
    n=len(rhs); a=[row[:]+[rhs[i]] for i,row in enumerate(matrix)]
    for j in range(n):
        k=next((i for i in range(j,n) if a[i][j]),None)
        require(k is not None,'singular moment matrix')
        a[j],a[k]=a[k],a[j]; pivot=a[j][j]
        a[j]=[x/pivot for x in a[j]]
        for i in range(n):
            if i!=j:
                v=a[i][j]; a[i]=[x-v*y for x,y in zip(a[i],a[j])]
    return [row[-1] for row in a]

def checks()->dict:
    # Finite algebraic analogue of the smooth-bump moment construction.
    # This polynomial weight itself is NOT the manuscript's C-infinity kernel.
    def moment(k:int)->F:
        return F(0) if k%2 else sum((F((-1)**j*comb(4,j)*2,k+2*j+1) for j in range(5)),F(0))
    moments=0; tensor=0
    for s in range(1,9):
        c=solve([[moment(i+j) for j in range(s)] for i in range(s)],[F(int(i==0)) for i in range(s)])
        vals=[sum((c[j]*moment(i+j) for j in range(s)),F(0)) for i in range(s)]
        for i,v in enumerate(vals):require(v==int(i==0),'moment cancellation');moments+=1
        for i in range(s):
            for j in range(s-i):
                require(vals[i]*vals[j]==int(i+j==0),'tensor moment');tensor+=1
    rate_cases=0
    for m,s,omega,Gamma in product((3,4,8,20,38),(1,2,3,5,9),(F(1,3),F(1),F(5,2)),(F(1,2),F(1),F(4))):
        d=2*(m+s)+2;alpha=F(s,d);gamma=F(s,m+s+3);beta=alpha*omega/(omega+alpha*Gamma)
        require(F(1,2)-F(m+1,d)==alpha,'dimension-two square-root balance')
        require(1-F(m+2,d)==F(m+2*s,d)>=alpha,'linear Bernstein term')
        require(1-F(m+3,m+s+3)==gamma,'readout balance')
        k=alpha/(omega+alpha*Gamma)
        require(omega*k==alpha*(1-Gamma*k)==beta,'charged budget balance')
        require(0<beta<alpha,'rarity must cost a positive exponent')
        require(alpha-F(s,2*(m+s)+1)!=0,'dimension-one negative control')
        require(omega*(alpha/omega)!=alpha*(1-Gamma*(alpha/omega)),'free-success negative control')
        rate_cases+=1
    mixture_equalities=0; probability_sums=0
    for B,p,q in product(range(2,7),(F(1,5),F(1,2),F(4,5)),(F(1,3),F(3,4))):
        probs=(1-p,p*(1-q),p*q) # failure, mark zero, mark one
        sequences=[(seq,prod((probs[x] for x in seq),start=F(1))) for seq in product(range(3),repeat=B)]
        require(sum((w for _,w in sequences),F(0))==1,'probability normalization');probability_sums+=1
        for n in range(1,min(B,3)+1):
            tail=sum((F(comb(B,k))*p**k*(1-p)**(B-k) for k in range(n,B+1)),F(0))
            actual={marks:F(0) for marks in product((0,1),repeat=n)}
            for seq,w in sequences:
                marks=tuple(x-1 for x in seq if x)
                if len(marks)>=n:actual[marks[:n]]+=w
            for marks,w in actual.items():
                expected=tail*prod((q if x else 1-q for x in marks),start=F(1))
                require(w==expected,'first accepted marks depend on count');mixture_equalities+=1
    offset_cases=0
    for d1,d2,H,Z1,Z2,Bz in product((F(1),F(2)),(F(4),F(5)),(F(-1,3),F(0),F(1,2)),(F(2),F(7)),(F(3),F(11)),(F(1,2),F(3))):
        # The common amplitude at the anchor is one; normalizers are arbitrary.
        f1=Bz*(d1-H)/Z1;f2=Bz*(d2-H)/Z2
        Q=f1*(d2/Z2)/(f2*(d1/Z1))
        recovered=d1*d2*(1-Q)/(d2-d1*Q)
        require(recovered==H,'two-offset extraction');offset_cases+=1
    thresholds=[]
    for a in (F(1,2),F(3,4),F(9,10),F(19,20)):
        m=next(j for j in range(3,1000) if 6*a**j/(1-a**j)<1)
        thresholds.append(dict(a=str(a),first_m_at_least_three=m,theta=str(6*a**m/(1-a**m))))
    examples=[]
    for m in (3,38):
        alpha=F(1,2*(m+1)+2)
        examples.append(dict(m=m,s=1,Gamma_over_omega='1',alpha=str(alpha),beta=str(alpha/(1+alpha)),gamma=str(F(1,m+4))))
    return dict(status='passed',scope=__doc__.strip(),moment_equalities=moments,tensor_equalities=tensor,rate_parameter_cases=rate_cases,dimension_and_free_success_negative_controls_detected=2*rate_cases,mixture_probability_normalizations=probability_sums,conditional_mark_equalities=mixture_equalities,two_offset_cases=offset_cases,weighted_thresholds=thresholds,illustrative_not_optimal_rates=examples)

if __name__=='__main__':
    print(json.dumps(checks(),indent=2,sort_keys=True))
