#!/usr/bin/env python3
"""Finite regression fixtures for v86; these are not continuum proof certificates."""
from __future__ import annotations
from fractions import Fraction as F
import itertools
import json
import math
import random
from check_v77 import require


def checks() -> dict:
    counts=dict(cap=0,jensen=0,threshold=0,exponents=0,dyadic=0,
                exponential=0,reachability=0,trace_payment=0,scope=0)
    for p,D,s in itertools.product((.5,1.,33/32,1.2,1.8),(.0001,.02,.5,1.),(.001,.01,.1,.7,1.)):
        split=min(s,math.sqrt(D))
        val=s**(-p)*min(D,s*s)+p*split**(2-p)/(2-p)
        if s>split:val+=D*(split**(-p)-s**(-p))
        expected=2/(2-p)*min(s**(2-p),D**(1-p/2))
        require(abs(val-expected)<=1e-10*(1+expected),'capped power integral')
        counts['cap']+=1
    rng=random.Random(860199)
    for n,p in itertools.product((1,2,5,12,31),(33/32,67/64)):
        for _ in range(30):
            w=[1.]+[(47/53)**min(i,n+1-i) for i in range(1,n+1)]
            x=[1.]+[10**rng.uniform(0,7) for _ in range(n)]
            lhs=sum(a*b for a,b in zip(w,x))**p
            rhs=sum(w)**(p-1)*sum(a*b**p for a,b in zip(w,x))
            require(lhs<=rhs*(1+1e-12),'complete additive Jensen')
            counts['jensen']+=1
    for p,gamma,ell in itertools.product((33/32,67/64),(16,24),(.8,.4,.01,.0001)):
        for ratio,offset in itertools.product((.5,1.,2.,10.),(.50001,.75,1.)):
            I=ratio*ell**(-gamma);s=offset*ell
            marked=I if I>s**(-gamma) else 0.
            require(marked<=ell**(gamma*(p-1))*I**p*(1+1e-12),'shrinking mark direction')
            counts['threshold']+=1
    alpha=F(129,128);beta=F(17,16)
    for p,eta in itertools.product((F(33,32),F(67,64)),(F(1,8),F(1,4),F(3,8))):
        sigma=1-p/2;kappa=(1-eta)/2
        require(1<p<beta and 0<eta<sigma and alpha>eta,'two layer-cake ranges')
        counts['exponents']+=1
        for gamma in (F(16),F(24)):
            d=gamma*(p-1)-kappa
            require(d>0,'microscopic summability')
            counts['exponents']+=1
    require(16*(F(33,32)-1)-(1-F(1,4))/2==F(1,8),'explicit microscopic exponent')
    require(F(1,8)+1==F(9,8),'explicit ordered exponent');counts['exponents']+=2
    for h,d,N in itertools.product((.9,.1,.002),(.125,.4,.9),(0,1,4,30)):
        tail=sum((h*2.**(-j))**d for j in range(N,N+2000))
        exact=(h*2.**(-N))**d/(1-2.**(-d))
        require(abs(tail-exact)<=1e-11*(1+exact),'entire positive dyadic tail')
        counts['dyadic']+=1
    for rho,sigma,m in itertools.product((.1,.5,.95,.999),(.4,31/64),(2,5,30,500,5000)):
        a=-sigma*.5*math.log(rho)
        require(m*m*math.exp(-a*m)<=max(4.,4*math.exp(-2)/(a*a))*(1+1e-12),
                'finite exponential remainder supremum')
        counts['exponential']+=1
    # A segment selector is physical: a<t<t+s<b. No later reentry is admitted.
    for a,b,t,s in itertools.product((F(-2),F(0),F(1)),(F(2),F(4)),
                                    (F(-1),F(0),F(1),F(2),F(3)),(F(1,4),F(1),F(2))):
        if a>=b:continue
        u=t+s
        kernel=(a<u<b and u-a>s)
        segment=(a<t<u<b)
        require(kernel==segment,'same-segment backward lifetime')
        if kernel:
            z=math.sqrt(float(2*(u-a)))
            eta=.25;kappa=(1-eta)/2
            require(1/z<=2**(-kappa)*float(s)**(-kappa)*z**(-eta)*(1+1e-12),
                    'radial reachable-fiber bound')
        counts['reachability']+=1
    for w0,w1,v in itertools.product((F(0),F(1,4),F(1),F(3)),repeat=3):
        if v>=abs(w1-w0):
            require(w0<=w1+v and max(F(0),w0-w1)<=v,'initial trace paid by variation')
            counts['trace_payment']+=1
    # This fixture prevents accidental conflation of a selected-sector estimate
    # with a height theorem for all nonnegative sources.
    for m in (4,16,64):
        width=1/m**2;normalized_height=1.
        require(width*normalized_height<.1 and normalized_height==1.,'mass is not height')
        counts['scope']+=1
    return {'counts':counts,'total_checks':sum(counts.values()),
            'scope':'finite algebraic, exponent, summability, selector and source-payment fixtures only',
            'full_raw_return_LLT_proved':False,'independent_human_review':False,
            'formal_proof_certificate':False}


if __name__=='__main__':print(json.dumps(checks(),indent=2,sort_keys=True))
