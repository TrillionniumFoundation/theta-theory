#!/usr/bin/env python3
"""Exact finite regression fixtures; no continuum or uniform pressure certification."""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
from math import ceil, sqrt
import json

def require(ok: bool, message: str) -> None:
    if not ok: raise RuntimeError(message)

def dot(a,b): return sum(x*y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def mul(a,b): return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)) for i in range(2))
def normal(t): return ((1-t*t)/(1+t*t),2*t/(1+t*t))
def tangent(n): return (-n[1],n[0])
def flight(k,kp,c,cp,t): return (((t*k+c)/cp,t/cp),((t*k*kp+k*cp+kp*c)/cp,(t*kp+cp)/cp))

def checks() -> dict:
    counts={k:0 for k in ('circle_convexity_pairing','flight_matrix','product_columns','marked_cocycle','pressure_concatenation','block_growth','spectral_margin','retained_exponents')}
    ts=tuple(F(i,4) for i in range(-6,7))
    for t,s in product(ts,repeat=2):
        n,nh=normal(t),normal(s);d=sub(n,nh);tt,th=tangent(n),tangent(nh)
        require(dot(n,n)==1 and dot(nh,nh)==1,'rational circle')
        require(dot(sub(tt,th),d)==0,'skew tangential cancellation');counts['circle_convexity_pairing']+=2
        for p,c in ((F(0),F(1)),(F(3,5),F(4,5)),(F(-5,13),F(12,13))):
            for sign in (-1,1):
                a=tuple(-c*n[i]+sign*p*tt[i] for i in range(2));b=tuple(-c*nh[i]+sign*p*th[i] for i in range(2))
                require(dot(sub(a,b),d)==-c*dot(d,d),'endpoint normal coercivity');counts['circle_convexity_pairing']+=1
        for c,ch in ((F(1),F(1,1000)),(F(2,3),F(3,7))):
            dS=tuple(-2*c*n[i]+2*ch*nh[i] for i in range(2))
            require(dot(dS,d)==-(c+ch)*dot(d,d),'internal reflected coercivity');counts['circle_convexity_pairing']+=1
    mats=[];klo=F(100,47);khi=F(20,9);tau=F(3,50);upper=khi+1/tau
    for k,kp,c,cp,t in product((klo,khi),(klo,khi),(F(1),F(2,5),F(1,1000)),(F(1),F(3,5),F(1,10000)),(tau,F(1,2),F(2))):
        a=flight(k,kp,c,cp,t);mats.append(a)
        require(a[0][0]*a[1][1]-a[0][1]*a[1][0]==c/cp,'collision area determinant');counts['flight_matrix']+=1
        for row in a:
            require(klo*row[1]<=row[0]<=upper*row[1],'one-step column ratio');counts['flight_matrix']+=1
    a=((F(1),F(0)),(F(0),F(1)))
    for j in range(24):
        a=mul(mats[(j*17)%len(mats)],a)
        for row in a:
            require(klo*row[1]<=row[0]<=upper*row[1],'nonaccumulating product comparison');counts['product_columns']+=1
    q=F(47,53);cs=(F(1),F(1,2),F(1,5));stable=tuple(c/(2+c) for c in cs);D=len(cs)
    for m in range(2,7):
        unmarked=F(0);marked=[F(0)]*(m-1)
        for w in product(range(D),repeat=m):
            factors=[stable[i] for i in w];prod=F(1)
            for f in factors:prod*=f
            unmarked+=prod
            for i in range(1,m):
                missing=F(1)
                for j,f in enumerate(factors):
                    if j!=i:missing*=f
                require(prod/cs[w[i]]<=missing,'remove one stable factor');counts['marked_cocycle']+=1
                marked[i-1]+=prod/cs[w[i]]
        S=sum(stable)
        require(unmarked==S**m,'complete itinerary pressure sum');counts['pressure_concatenation']+=1
        for i in range(1,m):
            require(marked[i-1]<=D*S**i*S**(m-i-1),'coarse middle alphabet bound');counts['pressure_concatenation']+=1
        require(sum((q**min(i,m-i) for i in range(1,m)),F(0))<=2*q/(1-q),'depth summability');counts['pressure_concatenation']+=1
    seq=[F(1)]+[F(2**ceil(sqrt(j))) for j in range(1,121)]
    for j,k in product(range(1,31),repeat=2):
        require(seq[j+k]<=seq[j]*seq[k],'finite block submultiplicativity');counts['block_growth']+=1
    for L in range(1,13):
        rate=1
        while F(rate)**L<seq[L]:rate+=1
        C=max(seq[j]/F(rate)**j for j in range(L))
        for m in range(1,121):
            require(seq[m]<=C*F(rate)**m,'block remainder constant');counts['block_growth']+=1
    for rho,theta in ((F(1),F(9,10)),(F(2),F(1,2)),(F(9,8),F(4,5))):
        x=rho*theta**2;require(x<1,'strict block spectral margin')
        n=1
        while F(n+1,n)**6*x>=1:n+=1
        require(F(n+1,n)**6*x<1,'eventual geometric ratio after polynomial factor');counts['spectral_margin']+=2
    alpha=F(129,128)
    require(alpha-1==F(1,128),'inverse-gradient leading exponent')
    require(1+(alpha-1)/2==F(257,256),'critical certificate exponent')
    require(4*F(257,256)==F(257,64),'outer epsilon critical power')
    require(F(4)-1==3,'guard comparison power');counts['retained_exponents']+=4
    return {'counts':counts,'total_checks':sum(counts.values()),
            'scope':'finite exact circle, matrix, cocycle, itinerary and block fixtures only',
            'uniform_spectral_capacity_certified':False,'positive_paired_trace_decay_certified':False,
            'independent_human_review':False,'formal_proof_certificate':False}
if __name__=='__main__':print(json.dumps(checks(),indent=2,sort_keys=True))
