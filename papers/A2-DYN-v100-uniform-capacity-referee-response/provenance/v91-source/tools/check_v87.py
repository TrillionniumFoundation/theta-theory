#!/usr/bin/env python3
"""Finite rational, numerical and selector regressions; not continuum certification."""
from __future__ import annotations
from fractions import Fraction as F
import itertools,json,math,random
from check_v77 import require


def checks() -> dict:
    counts=dict(anchor_geometry=0,radial_margin=0,positive_trace=0,
                holder_sum=0,microscopic_exponents=0,finite_remainder=0,
                source_partition=0,ordered_squeeze=0)
    rng=random.Random(870202)
    # Longer-side anchor and target paths remain in the actual segment.
    Lam=F(47,6)
    for a,delta in itertools.product((F(1),F(1,2),F(1,16),F(1,100)),
                                     (F(1),F(1,3),F(1,100))):
        d=min(delta/16,a*a/(32*Lam),F(1,16))
        require(d<=a and d<=delta/16 and 8*Lam*d<=a*a/4,'trace collar')
        counts['radial_margin']+=1
        for ell,f in itertools.product((delta,2*delta,17*delta),
                                       (F(1,1000),F(1,4),F(1,2),F(3,4),F(999,1000))):
            left=-f*ell;right=(1-f)*ell
            anchor=(-3*d,-2*d) if -left>=delta/2 else (2*d,3*d)
            require(left<anchor[0]<anchor[1]<right,'Borel longer-side anchor')
            for v in (F(0),min(d,right)/2,min(d,right)*F(999,1000)):
                lo=min(anchor[0],v);hi=max(anchor[1],v)
                require(left<lo<=hi<right and hi-lo<=8*d,'joining interval')
                require(a*a-2*Lam*abs(lo)>=3*a*a/4,'lower radial margin')
                counts['anchor_geometry']+=1
    # Direct trace calculation on exponential densities with a matching drift.
    # These examples test constants and do not certify the general Sobolev proof.
    for p,D,d,k in itertools.product((33/32,1.5,2.),(.2,1.,3.),(.01,.2,1.),(-3.,-.1,0.,.4,2.)):
        I=max(1.,abs(k)/D)
        def integ(l,r):
            return r-l if k==0 else (math.exp(k*r)-math.exp(k*l))/k
        anchor_mean=integ(0,d)/d
        energy=I**p*integ(0,4*d)
        bound=2**(p-1)*(anchor_mean+(D/p)**p*(8*d)**(p-1)*energy)
        actual=max(1.,math.exp(4*k*d))
        require(actual<=bound*(1+1e-11),'positive density trace fixture')
        counts['positive_trace']+=1
    # Disjoint physical sheets: two Holder steps, then one complete energy.
    for p,n in itertools.product((33/32,1.1,2.),(1,2,7,31)):
        e=1-1/p
        for _ in range(30):
            traces=[10**rng.uniform(-3,3) for _ in range(n)]
            energies=[10**rng.uniform(-3,3) for _ in range(n)]
            weights=[.1+rng.random() for _ in range(n)]
            lhs=sum(w*s**e*q**(1/p) for w,s,q in zip(weights,traces,energies))
            rhs=sum(w*s for w,s in zip(weights,traces))**e*sum(w*q for w,q in zip(weights,energies))**(1/p)
            require(lhs<=rhs*(1+1e-12),'complete angular Holder')
            counts['holder_sum']+=1
    p=F(33,32);e=1-1/p;xi=F(1,128);beta=F(1,64)
    require(e==F(1,33) and e*(1-beta)-xi==F(31,1408),'explicit envelope exponent')
    counts['microscopic_exponents']+=1
    c=min(1/16,1/(32*float(Lam)))
    for h in (1e-3,1e-5,1e-10,1e-30,1e-90):
        a=h**float(xi);delta=h**float(beta);d=c*delta
        require(h<=d and math.isclose(d,min(delta/16,a*a/(32*float(Lam)),1/16),rel_tol=1e-12),'moving collar')
        lhs=a**(-1)*(h/d)**float(e)
        rhs=c**(-float(e))*h**float(F(31,1408))
        require(abs(lhs/rhs-1)<1e-12,'finite-count power balance')
        counts['microscopic_exponents']+=1
    for rho,m in itertools.product((.1,.5,.9,.999),(2,5,20,100,1000,10000)):
        alpha=-.5*float(1-p/2)*math.log(rho)
        require(m*m*math.exp(-alpha*m)<=4*math.exp(-2)/alpha**2*(1+1e-12),'full exponential supremum')
        counts['finite_remainder']+=1
    for w,ratio,ex,critical,short in itertools.product((F(0),F(1,3),F(1)),
            (F(0),F(1,2),F(1),F(7)),(False,True),(False,True),(False,True)):
        exceptional=critical or short
        defect=w if ex else w*max(F(0),1-ratio)
        require(defect*exceptional<=w*exceptional,'original source exceptional payment')
        require(int(exceptional)+int(not exceptional)==1,'union is not double counted')
        counts['source_partition']+=1
    for b,R,e0,e1 in itertools.product((F(0),F(1),F(4)),(F(0),F(1),F(4)),
                                      (F(0),F(1,10)),(F(0),F(1,5))):
        if R<=b<=R+e0:
            for E in (max(F(0),b-e1),b,b+e1):
                require(R<=E+e1 and E<=R+e0+e1,'ordered original-source squeeze')
                counts['ordered_squeeze']+=1
    return {'counts':counts,'total_checks':sum(counts.values()),
            'scope':'finite selector, trace, Holder, exponent and source-payment fixtures only',
            'original_critical_residence_source_charge_zero_proved':False,
            'full_raw_return_LLT_proved':False,'formal_proof_certificate':False,
            'independent_human_review':False}

if __name__=='__main__':print(json.dumps(checks(),sort_keys=True,indent=2))
