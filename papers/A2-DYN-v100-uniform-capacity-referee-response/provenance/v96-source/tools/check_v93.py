#!/usr/bin/env python3
"""Exact finite fixtures for optical cancellation and signed source accounting.
No continuum proof or independent-review certification is implied.
"""
from __future__ import annotations
from fractions import Fraction as F
import itertools
import json
import random

def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)

def integral_poly(coeff: list[F], lo: F, hi: F) -> F:
    return sum((a*(hi**(j+1)-lo**(j+1))/F(j+1)
                for j,a in enumerate(coeff)), F(0))

def checks() -> dict:
    counts = dict(optical_cancellation=0, depth_sum=0, root_modulus=0,
                  signed_prefix=0, prescribed_scale=0, ancestral_selection=0,
                  critical_split=0, upper_spike=0)
    R, tau, q = F(47,100), F(3,50), F(47,53)
    C0, C1 = R/tau, R*R/(2*tau*tau)
    rng=random.Random(93220)
    for m in (1,2,3,7,13,25):
        for _ in range(20):
            ell=[tau+F(rng.randrange(0,200),100) for j in range(m)]
            ci=[F(rng.randrange(1,100),100) for j in range(m+1)]
            y, flux=ell[0], F(1)
            for i in range(1,m):
                flux += 2*y/(R*ci[i]); y += ell[i]*flux
            omega=R*ci[0]*ci[m]/y
            require(omega<=C0,'absolute optical constant')
            counts['optical_cancellation']+=1
            for i in range(1,m):
                require(y>=2*tau*tau/(R*ci[i]),'selected potential in positive recurrence')
                require(omega/ci[i]<=C1,'absolute inverse incidence cancelled')
                counts['optical_cancellation']+=2
            weights=sum((q**min(i,m-i) for i in range(1,m)),F(0))
            I=1+sum((q**min(i,m-i)/ci[i] for i in range(1,m)),F(0))
            require(weights<=2*q/(1-q),'complete depth sum')
            require(omega*I<=C0+2*q*C1/(1-q),'absolute optical insertion')
            counts['depth_sum']+=2
    for u,v in itertools.combinations(range(31),2):
        require(F((v-u)**2)<=F(v*v-u*u),'square-root time modulus')
        counts['root_modulus']+=1
    # f(u)=b+d*u on (a,c), with its genuine birth at a and negative cut at c.
    for a,length,b,d in itertools.product((F(-1),F(0),F(2)),
                       (F(1,4),F(1),F(3)),(F(2),F(7)),(F(0),F(1,3),F(-1,4))):
        c=a+length
        require(min(b+d*a,b+d*c)>0,'fixture positivity')
        for degree in range(1,5):
            left=-degree*integral_poly([F(0)]*(degree-1)+[b,d],a,c)
            right=(b+d*a)*a**degree-(b+d*c)*c**degree
            right+=d*(c**(degree+1)-a**(degree+1))/F(degree+1)
            require(left==right,'signed trace formula')
            counts['signed_prefix']+=1
        for portion,r in itertools.product((F(1,4),F(1,2),F(3,4)),(F(1,8),F(1),F(4))):
            t=a+portion*length; start=t-r; lo=max(a,start)
            average=integral_poly([b,d],lo,t)/r
            birth=(a-start)/r*(b+d*a) if a>start else F(0)
            signed=d*((t-start)**2-(lo-start)**2)/(2*r)
            gain=max(d,F(0))*((t-start)**2-(lo-start)**2)/(2*r)
            require(b+d*t==average+birth+signed,'exact ancestral ramp')
            require(b+d*t<=average+birth+gain,'pointwise upper sign')
            counts['prescribed_scale']+=2
            sharpbirth=b+d*a if a>start else F(0)
            sharpgain=max(d,F(0))*(t-lo)
            for frac in (F(1,7),F(4,7),F(6,7)):
                s=start+frac*r
                past=b+d*s if a<s else F(0)
                require(past>=b+d*t-sharpbirth-sharpgain,'all earlier roofs persist')
                counts['upper_spike']+=1
            # The intermediate gradient cutoff splits exactly at a rational roof.
            crossing=a+length/3
            below=max(F(0),min(t,crossing)-lo)
            above=max(F(0),t-max(lo,crossing))
            require(below+above==t-lo,'critical/noncritical disjoint split')
            counts['critical_split']+=1
    # Earlier prefixes that have ended must not create a positive ancestor at t.
    sheets=[(F(0),F(2),F(1)),(F(-1),F(1,2),F(8)),(F(3),F(4),F(5))]
    t=F(1); r=F(2); active=[x for x in sheets if x[0]<t<x[1]]
    require(len(active)==1 and sum(x[2] for x in active)==1,'target ancestors only')
    for a,c,w in sheets:
        value=w if a<t<c else F(0)
        avg=w*max(F(0),min(t,c)-max(t-r,a))/r
        active_birth=(a-t+r)/r*w if a<t<c and a>t-r else F(0)
        require(value<=avg+active_birth,'ended prefix counted only in earlier mass')
        counts['ancestral_selection']+=1
    for length in (F(1,1000),F(1,100),F(1,2)):
        # A unit-height narrow pulse needs its unit positive entrance trace.
        require(length>0 and F(1)-F(0)==1,'birth charge of narrow pulse')
        counts['upper_spike']+=1
    return {'counts':counts,'total_checks':sum(counts.values()),
            'scope':'finite exact rational fixtures; no continuum or independent proof certification',
            'full_raw_return_LLT_proved':False,'formal_proof_certificate':False,
            'independent_human_review':False}

if __name__=='__main__':
    print(json.dumps(checks(),indent=2,sort_keys=True))
