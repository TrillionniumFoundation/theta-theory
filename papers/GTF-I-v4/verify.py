#!/usr/bin/env python3
"""Finite regressions for the displayed formulas; not a proof verifier."""
from __future__ import annotations
import argparse
from fractions import Fraction as Q
import itertools
import json
import math

CHECKS: dict[str,int] = {}

def require(ok: bool, group: str, detail: str='') -> None:
    CHECKS[group] = CHECKS.get(group,0)+1
    if not ok:
        raise SystemExit('FAILED '+group+': '+detail)

def close(x: float,y: float,rel: float=1e-10,absolute: float=1e-12) -> bool:
    return abs(x-y)<=absolute+rel*max(abs(x),abs(y))

def psi(v: list, n: int, b: int):
    return sum(v[k]*Q(1,b**(2*(n-k))) for k in range(min(n,len(v))))+sum(v[n:])

def sinc_loss(t: float) -> float:
    z=math.pi*t
    if abs(z)<1e-3:
        return z*z/3-2*z**4/45+z**6/315
    return 1-(math.sin(z)/z)**2

def moments(roots: list[Q], d: int) -> list[Q]:
    return [sum(x**j for x in roots) for j in range(1,d+1)]

def elementary(p: list[Q]) -> list[Q]:
    e=[Q(1)]
    for j in range(1,len(p)+1):
        e.append(sum((-1)**(i-1)*e[j-i]*p[i-1] for i in range(1,j+1))/j)
    return e

def det(a: list[list[Q]]) -> Q:
    a=[row[:] for row in a]; answer=Q(1)
    for i in range(len(a)):
        j=next((j for j in range(i,len(a)) if a[j][i]),None)
        if j is None:return Q(0)
        if j!=i:a[i],a[j]=a[j],a[i];answer=-answer
        pivot=a[i][i];answer*=pivot
        for j in range(i+1,len(a)):
            c=a[j][i]/pivot
            for k in range(i,len(a)):a[j][k]-=c*a[i][k]
    return answer

def main() -> None:
    ap=argparse.ArgumentParser();ap.add_argument('--mutant',choices=['uncharged-age','erase-critical-log','omit-noise-floor','regularize-collision']);args=ap.parse_args()
    for b in [2,3,5]:
        for d in [1,2,3]:
            a=b**d
            for n in range(5):
                count=sum(a**k for k in range(n+1))
                require(count==(a**(n+1)-1)//(a-1),'state-counts')
                if n and args.mutant=='uncharged-age':count=a**n
                require(count==1+sum(a**k for k in range(1,n+1)),'charged-age')
                for M in [count,count+1,max(count,(a**(n+2)-1)//(a-1)-1)]:
                    nm=0
                    while sum(a**k for k in range(nm+2))<=M:nm+=1
                    kh=int(math.floor(math.log(2*M)/math.log(a)+1e-12))
                    require(kh<=nm+2,'small-ball-budget')
            if a<=9:
                words=[w for k in range(4) for w in itertools.product(range(a),repeat=k)]
                wordset=set(words)
                require(len(words)==sum(a**k for k in range(4)),'suffix-closure')
                for w in words:require(w[1:] in wordset,'suffix-closure')
    # Nongeometric laws: exact rational tails and all profile inequalities.
    for length_law in [[Q(1)], [Q(1,3),Q(1,3),Q(1,3)], [Q(1,2),Q(1,4),Q(0),Q(1,4)]]:
        mean=sum((k+1)*p for k,p in enumerate(length_law))
        w=[sum(length_law[k:])/mean for k in range(len(length_law))]
        require(sum(w)==1,'renewal-weights')
        A=max(sum(w[k:])/w[k] for k in range(len(w)) if w[k])
        for b in [2,3]:
            for decay in [Q(1),Q(2,3),Q(1,4)]:
                v=[w[k]*decay**(2*k) for k in range(len(w))]
                for n in range(len(w)+3):
                    p0,p1=psi(v,n,b),psi(v,n+1,b)
                    require(p0>=p1>=p0/(b*b),'profile-monotonicity')
                    if n<len(v):require(sum(v[n:])<=A*v[n],'posterior-tail')
                    floor=sum(w[k]-v[k] for k in range(len(w)))
                    require(0<=psi(w,n,b)-p0<=floor,'noise-floor-comparison')
    for j in range(1,501):
        t=j/1000
        value=sinc_loss(t)
        require(4*t*t/3-1e-13<=value<=math.pi**2*t*t/3+1e-13,'sinc-bounds')
    # Exact posterior risk decomposition and the noise-independent upper bound.
    for q in [.1,.25,.65,.9]:
        for sigma in [0.,.002,.1,1.]:
            b,d=2,2;w=[(1-q)*q**k for k in range(500)]
            a=[math.exp(-2*math.pi**2*(sigma*2**k)**2) if sigma and k<500 else 1. for k in range(500)]
            B=d*sum(w[k]*(1-a[k]**2) for k in range(500))
            for n in [0,1,4,10]:
                v=[w[k]*a[k]**2 for k in range(500)]
                excess=d*sum(v[k]*(sinc_loss(2**(-(n-k))) if k<n else 1) for k in range(500))
                raw=d*sum(w[k]*(1-a[k]**2*(1-sinc_loss(2**(-(n-k)))) if k<n else 1) for k in range(500))
                reported=excess if args.mutant=='omit-noise-floor' else B+excess
                require(close(raw,reported),'posterior-orthogonality')
                pv=float(psi(v,n,b));pw=float(psi(w,n,b))
                require(excess<=d*math.pi**2/3*pv+1e-12,'suffix-upper')
                blind=d*sum(w[k]*(1+(1-2*a[k])*(1-sinc_loss(2**(-(n-k)))) if k<n else 1) for k in range(500))
                require(blind<=4*B+2*d*math.pi**2/3*pw+1e-12,'noise-independent-decoder')
    for b in [2,3,5]:
        for x in [-3.,-1.,0.,1.,3.]:
            H=math.expm1(x)/x if x else 1.
            limit=(1-b**-2)*H
            for n in [80,160,320]:
                q=b**-2*math.exp(x/n)
                profile=(1-q)*sum(math.exp(x*k/n) for k in range(n))/n+math.exp(x)/n
                if args.mutant=='erase-critical-log':profile/=n
                require(abs(profile-limit)<30/n,'critical-window')
                # Stable expression b^(2n) U/n, avoiding exponential overflow.
                scaled=(1-q)*sum(math.exp(x*k/n)*(sinc_loss(b**(-(n-k)))*b**(2*(n-k)) if n-k<30 else math.pi**2/3) for k in range(n))/n+math.exp(x)/n
                require(abs(scaled-math.pi**2/3*limit)<90/n,'suffix-crossover')
    # Newton identities and the changing-rank determinant are exact rational checks.
    for d in range(1,7):
        roots=[Q(j+1,d+2) for j in range(d)]
        e=elementary(moments(roots,d))
        for j in range(d+1):
            direct=sum((math.prod(c) for c in itertools.combinations(roots,j)),Q(0))
            require(e[j]==direct,'newton-identities')
        jac=[[Q(j)*x**(j-1) for x in roots] for j in range(1,d+1)]
        vand=math.factorial(d)*math.prod(roots[j]-roots[i] for i in range(d) for j in range(i+1,d))
        require(det(jac)==vand,'vandermonde-rank')
        if d>=2:
            collided=roots[:];collided[1]=collided[0]
            require(det([[Q(j)*x**(j-1) for x in collided] for j in range(1,d+1)])==0,'collision-rank-loss')
    # Numerical root bracketing for the constant-polynomial perturbation construction.
    for r in range(1,6):
        aa=[-.2+.4*(j+1)/(r+1) for j in range(r)]
        eps=.05/(r+1)
        def pol(x):return math.prod(x-y for y in aa)
        c=min(abs(pol(x+sgn*eps)) for x in aa for sgn in [-1,1])/8
        bb=[]
        for x in aa:
            lo,hi=x-eps,x+eps
            for _ in range(80):
                mid=(lo+hi)/2
                if (pol(lo)+c)*(pol(mid)+c)<=0:hi=mid
                else:lo=mid
            bb.append((lo+hi)/2)
        for j in range(r):
            require(close(sum(x**j for x in aa),sum(x**j for x in bb),absolute=2e-13),'moment-cancellation')
        diff=abs(sum(x**r for x in aa)-sum(x**r for x in bb))
        require(close(diff,r*c,rel=1e-6,absolute=1e-18),'first-distinguishing-moment')
        if r>=2:
            h1,h2=.1,.05
            delta1=diff*h1**r;delta2=diff*h2**r
            predicted=2**(-1 if args.mutant=='regularize-collision' else -r)
            require(close(delta2/delta1,predicted),'collision-scaling')
    # One-state boundary example: zero orbit quantization but positive causal risk.
    for p in [Q(1,4),Q(1,2),Q(3,4)]:
        require(p*(1-p)>0,'same-cardinality-boundary')
        require(p*(1-p)**2+(1-p)*p*p==p*(1-p),'same-cardinality-boundary')
    print(json.dumps({'status':'passed','checks':CHECKS,'total_checks':sum(CHECKS.values()),'scope':'Finite deterministic identities and regressions; not formal proof verification.'},sort_keys=True,indent=2))

if __name__=='__main__':main()
