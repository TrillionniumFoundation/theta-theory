#!/usr/bin/env python3
"""Finite exact-identity checks. These are not proofs of the continuum theorems."""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product, combinations
from collections import defaultdict
import json

checks=0
negative_controls=0

def require(condition: bool, message: str) -> None:
    global checks
    checks+=1
    if not condition:
        raise RuntimeError(message)

def reject(condition: bool, message: str) -> None:
    global negative_controls
    if condition:
        raise RuntimeError('Negative control was incorrectly accepted: '+message)
    negative_controls+=1

def ell(n: int) -> F:
    a=F(1)
    for k in range(1,n+1):
        a*=F(1,3 if (k//3)%2==0 else 5)
    return a

def scale(k: int) -> F:
    return ell(max(0,k.bit_length()-1))

def center(word: tuple[int,...]) -> F:
    out=F(0);a=F(1)
    for k,bit in enumerate(word,1):
        r=F(1,3 if (k//3)%2==0 else 5)
        out+=(1-r)*a*bit;a*=r
    return out+a/2

# Raw marked-edge second moments include repeatable expanding self loops.
require(F(4095,4096)/9+F(225,4096)==F(85,512),'full-tail marked gain average')
require(F(4095,4096)*F(4,9)+F(900,4096)==F(85,128),'posterior marked gain average')
# Raw matrix inequalities, including the limiting alpha=0 identity.
for den in range(1,31):
    for num in range(den+1):
        alpha=F(num,den)
        require(F(19125,256)*(1-alpha)+225*alpha<=F(17,20)*450,'full-tail mode-zero drift')
        require(F(131,162)<=F(17,20),'full-tail mode-one drift')
        require(F(19125,16)*(1-alpha)+900*alpha<=F(17,20)*1800,'posterior mode-zero drift')
        require(F(3600,59049)+F(1,2)<=F(17,20),'posterior mode-one drift')
        if num:
            # Replacing the contracting return edge by a copy destroys this certificate.
            reject(F(1,2)*1800+F(1,2)<=F(17,20),'nonreset return contraction removed')

# Exact suspension: mix squared branch norms, not Minkowski over branches.
for q in (F(0),F(1,7),F(1),F(11,3)):
    radius=4*q
    for j in range(21):
        a=radius*F(j,20)
        for k in range(21):
            theta=F(k,20)
            energy=(1-theta)*a*a+theta*(F(3,4)*a+q)**2
            require(energy<=radius*radius,'suspension invariant ball')
for ticks in range(1,65):
    reject(ticks*F(1,100)<=0,'spurious new error on an all-hold zero-error run')

# Nonstationary actual masses comparable to a reference with arbitrarily rare strata.
for power in range(1,10):
    alpha=F(1,10**power);beta=F(1,2)
    pi=(beta/(alpha+beta),alpha/(alpha+beta))
    mu=(pi[0]*(1+pi[1]/2),pi[1]*(1-pi[0]/2))
    seeds=[mu];candidates=[]
    for theta in (F(0),F(1,100),F(1,2),F(1),F(0),F(2,3),F(1)):
        cand=(mu[0]*(1-alpha)+mu[1]*beta,mu[0]*alpha+mu[1]*(1-beta))
        candidates.append(cand)
        mu=tuple((1-theta)*x+theta*y for x,y in zip(mu,cand))
        require(sum(mu)==1,'actual forward normalization')
        for i in range(2):
            require(pi[i]/2<=mu[i]<=3*pi[i]/2,'reference density bounds')
    for earlier in seeds+candidates:
        for i in range(2):
            require(earlier[i]<=3*mu[i],'occupation bound without rare division')

# Dyadic regularity and finite-overlap allocation coarsening.
for mult in range(1,9):
    power=(2*mult-1).bit_length()
    for k in range(257):
        require(scale(k//mult)**2<=25**power*scale(k)**2,'overlap coarsening')
        if k>=2:
            require(scale(k-1)**2<=25*scale(k)**2,'one-label regularity')

# Actual K* coordinates: all short cylinder centers, not just infinite Cantor endpoints.
words=[w for n in range(6) for w in product((0,1),repeat=n)]
coordinates={w:center(w) for w in words}
for u,w in combinations(words,2):
    d=abs(coordinates[u]-coordinates[w])
    require(d>0,'centers are distinct')
    require(abs(center(u[1:])-center(w[1:]))<=30*d,'posterior deletion gain')
    require(abs(center((0,0)+u)-center((0,0)+w))<=F(2,3)*d,'posterior prepend-two gain')
    require(abs(center((0,)*6+u)-center((0,)*6+w))<=F(2,243)*d,'posterior prepend-six gain')

# Full-history acquired depth laws at finite horizons, including no observations.
for alpha in (F(1,1000),F(1,2),F(1)):
    beta=F(1,2);pi=(beta/(alpha+beta),alpha/(alpha+beta))
    for B in (0,1,4):
        dist={(0,B):pi[0],(1,B):pi[1]}
        for t in range(10):
            require(sum(dist.values())==1,'mode-height law normalization')
            for M in (6,8,17,64):
                n=M.bit_length()-1
                acq=sum(p*ell(h)**2 for (i,h),p in dist.items())
                phi=sum(p*ell(min(h,n))**2 for (i,h),p in dist.items())
                require(max(acq,ell(n)**2)<=phi<=acq+ell(n)**2,'actual-depth profile sandwich')
                m=(M+2).bit_length()-3
                require(2**(m+2)-2<=M,'mode and length charged in alphabet')
                require(n-m<=2,'finite-prefix depth overhead')
            theta=(F(0),F(1,2),F(1))[t%3]
            nxt=defaultdict(F)
            for (i,h),p in dist.items():
                nxt[i,h]+=p*(1-theta)
                if i==0:
                    nxt[0,h+2]+=p*theta*(1-alpha)*F(4095,4096)
                    nxt[0,max(0,h-1)]+=p*theta*(1-alpha)*F(1,4096)
                    nxt[1,max(0,h-1)]+=p*theta*alpha
                else:
                    nxt[0,h+6]+=p*theta*beta
                    nxt[1,h]+=p*theta*(1-beta)
            dist=dict(nxt)

# Finite prefix conditional means: unknown bit origins are not retained secretly.
for B in range(4):
    for m in range(1,4):
        for op in ('copy','delete','prepend2','prepend6'):
            total=defaultdict(F);count=defaultdict(int)
            L=5
            new_depth=2 if op=='prepend2' else 6 if op=='prepend6' else 0
            for word in product((0,1),repeat=L):
                saved=word[:min(B,m)]
                for new in product((0,1),repeat=new_depth):
                    if op=='delete':
                        actual=word[1:];stored=saved[1:]
                    elif new_depth:
                        actual=new+word;stored=(new+saved)[:m]
                    else:
                        actual=word;stored=saved
                    total[stored]+=center(actual);count[stored]+=1
            for stored in total:
                require(total[stored]/count[stored]==center(stored),'retained-prefix decoder unbiasedness')

# Calibration signs share the oracle and have an exact squared ambiguity floor.
for alpha in (F(1,20),F(1,2),F(1)):
    pi1=alpha/(alpha+F(1,2))
    samples=[]
    for i,pi_i in ((0,1-pi1),(1,pi1)):
        for word in product((0,1),repeat=3):
            x=center(word);decoded=center(word[:1])
            p=F(1,2)+F(1,4)*(i-pi1)+F(1,8)*(x-F(1,2))
            a=F(1,2)+F(1,4)*(i-pi1)+F(1,8)*(decoded-F(1,2))
            samples.append((pi_i/8,p,a))
    require(sum(w*p for w,p,a in samples)==F(1,2),'physical score mean is one half')
    for delta in (F(0),F(1,100),F(1,16)):
        D=sum(w*(p-a)**2 for w,p,a in samples)
        for sign in (-1,1):
            require(sum(w*(p+sign*delta-a)**2 for w,p,a in samples)==D+delta**2,'common calibration risk')
        if delta:
            bias=F(1,100)
            plus=sum(w*(p+delta-a-bias)**2 for w,p,a in samples)
            minus=sum(w*(p-delta-a-bias)**2 for w,p,a in samples)
            reject(plus==minus,'biased arithmetic cannot claim sign cancellation')

print(json.dumps({'status':'success','exact_checks':checks,'rejected_negative_controls':negative_controls,
                  'arithmetic':'fractions.Fraction','continuum_proof_by_tests':False},sort_keys=True))
