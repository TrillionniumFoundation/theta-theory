#!/usr/bin/env python3
"""Finite regression fixtures only; not a continuum or journal proof certificate."""
from __future__ import annotations
from fractions import Fraction as F
import itertools
import json
from check_v77 import require


def checks() -> dict:
    counts=dict(residence_kernel=0,long_persistence=0,integrated_long=0,
                angular_variation=0,radial_cutoff=0,labels=0,
                dyadic_identity=0,exponents=0,negative_controls=0)
    zero=F(0)
    def kernel(t,a,b,r):
        return max(zero,1-(b-t)/r) if a<t<b else zero
    def integral(a,b,r,lo,hi):
        lo=max(lo,a,b-r);hi=min(hi,b)
        if hi<=lo:return zero
        return (1-b/r)*(hi-lo)+(hi*hi-lo*lo)/(2*r)
    for r in (F(1,8),F(1,2),F(1),F(3,2)):
        for depth in (F(1,16),F(1,4),F(1,2),F(1),F(2),F(3)):
            b=F(7,3);a=b-depth*r
            for q in range(-3,20):
                t=b-F(q,8)*r;s=b-t
                averaged=max(zero,r-max(zero,s))/r if 0<s<b-a else zero
                require(kernel(t,a,b,r)==averaged,'exact lifetime/roof average')
                counts['residence_kernel']+=1
                if b-a>2*r:
                    for j in range(1,16):
                        u=F(j,16)*r
                        require(kernel(t,a,b,r)<=2*kernel(t-u,a,b,2*r),
                                'long-residence persistence on the same face')
                        counts['long_persistence']+=1
                    require(kernel(t,a,b,r)<=2*integral(a,b,2*r,t-r,t)/r,
                            'exact integrated long-residence comparison')
                    counts['integrated_long']+=1
    # The same exact label is held on each side of the comparison.
    faces=[('n1',F(-3),F(0),F(2)),('n1',F(-4),F(1),F(3)),
           ('n2',F(-2),F(2),F(9)),('n2',F(0),F(1,8),F(11))]
    for label,t in itertools.product(('n1','n2'),(F(j,8) for j in range(-16,17))):
        r=F(1,2)
        lhs=sum((w*kernel(t,a,b,r) for n,a,b,w in faces if n==label and b-a>2*r),zero)
        rhs=2/r*sum((w*integral(a,b,2*r,t-r,t) for n,a,b,w in faces if n==label),zero)
        require(lhs<=rhs,'no neighboring exact-label pooling')
        counts['labels']+=1
    for w,c,dw,dc in itertools.product((F(1,8),F(1),F(3)),(F(1,3),F(2)),
                                      (F(-3),F(0),F(5)),(F(-2),F(0),F(4))):
        derivative=dw/c-w*dc/(c*c)
        require(abs(derivative)<=abs(dw)/c+w*abs(dc)/(c*c),
                'both angular normalization derivatives retained')
        counts['angular_variation']+=1
    for lam,r,ell,z2 in itertools.product((F(1,4),F(47,6)),(F(1,64),F(1,2)),
                                         (F(1,3),F(1),F(2)),(F(8),F(10),F(20))):
        length=ell*r;zb2=z2*lam*r
        for q in range(9):
            elapsed=length*F(q,8)
            require(zb2-2*lam*elapsed>=4*lam*r,'positive fixed-width lower gradient')
            counts['radial_cutoff']+=1
    for r,n in itertools.product((F(1,3),F(1,8),F(3)),range(8)):
        left=[(r/2/(2**j)/2,r/2/(2**j)) for j in range(n,n+8)]
        right=[(r/(2**j)/2,r/(2**j)) for j in range(n+1,n+9)]
        require(left==right,'exact dyadic offset shift, no second roof translation')
        counts['dyadic_identity']+=1
    alpha=F(129,128)
    require(1+alpha/2==F(385,256),'critical surface starting exponent')
    require(1+(1+alpha)/2==F(513,256),'critical optical variation exponent')
    counts['exponents']+=2
    for eta in (F(1,8),F(1,4),F(3,8),F(7,16)):
        k=(1-eta)/2
        require(F(1,4)<k<F(1,2) and 1-k>F(1,32),'legal fractional range')
        require(1+(1+eta)/2+(alpha-eta)/2==F(513,256),'eta cancels in critical mass')
        counts['exponents']+=2
    # Abstract short segments can have small mass but fixed height.
    for m in (4,8,16,32):
        length=F(1,m**4);r=F(1,2);t=length/2
        require(kernel(t,zero,length,r)>F(9,10),'short-residence height is not erased')
        require(integral(zero,length,r,zero,length)<=length,'small mass is not height')
        counts['negative_controls']+=2
    # A moving source pulse has mass d^k but nonvanishing d^{-k}-weighted tail.
    # Choose d=2^{-8m}, k=3/8 so every tested expression is rational.
    for m in (1,2,3,4):
        d=F(1,2**(8*m));mass=F(1,2**(3*m));weight=F(2**(3*m))
        require(mass*weight==1 and mass<1,'fixed-scale mass does not pay microscopic charge')
        counts['negative_controls']+=1
    return {'counts':counts,'total_checks':sum(counts.values()),
            'scope':'finite rational identities and explicit source-model negative controls only',
            'full_raw_return_LLT_proved':False,'independent_human_review':False,
            'formal_proof_certificate':False}

if __name__=='__main__':print(json.dumps(checks(),indent=2,sort_keys=True))
