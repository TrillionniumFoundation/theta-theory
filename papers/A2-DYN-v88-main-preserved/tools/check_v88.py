#!/usr/bin/env python3
"""Finite regression fixtures for displayed identities, not a continuum proof."""
from __future__ import annotations
from fractions import Fraction as F
import itertools
import json
import math
import mpmath as mp
from check_v77 import require

def checks() -> dict:
    counts={k:0 for k in ['interpolation_parameters','capped_layer_cake','physical_cap','exponent_family','trace_fixtures','weighted_variation','source_union','remainder_bound']}
    for k in [F(1,8),F(1),F(5,4),F(41,28),F(149,100),F(1499,1000)]:
        loss=(F(3,2)-k)/4
        theta=(1+k/(F(3,2)-loss))/2
        require(0<theta<1 and 0<loss<F(3,2),'strict interpolation domain')
        require((F(3,2)-loss)*theta>k and F(3,2)*theta>k,'two chronological amplitudes')
        gamma=(1-theta)/2
        require(1-gamma>theta,'logarithmic interpolation slack')
        counts['interpolation_parameters']+=3
    mp.mp.dps=45
    for pf,Df,sf in itertools.product([F(33,32),F(10,7),F(149,100)],[F(1,1024),F(1,16),F(1)],[F(1,128),F(1,8),F(1)]):
        p=mp.mpf(pf.numerator)/pf.denominator;D=mp.mpf(Df.numerator)/Df.denominator;s=mp.mpf(sf.numerator)/sf.denominator
        cut=mp.sqrt(D)
        if s<=cut: integ=s**(2-p)/(2-p)
        else: integ=cut**(2-p)/(2-p)+D*(cut**(-p)-s**(-p))/p
        lhs=s**(-p)*min(D,s*s)+p*integ
        rhs=2/(2-p)*min(s**(2-p),D**(1-p/2))
        require(abs(lhs-rhs)<mp.mpf('1e-37')*max(1,abs(rhs)),'full capped layer cake')
        counts['capped_layer_cake']+=1
    vals=[F(0),F(1,4),F(1),F(3)]
    for A,D,V in itertools.product(vals,repeat=3):
        require(min(A+D,V)<=A+min(D,V),'cap retained only on remainder')
        counts['physical_cap']+=1
    p=F(10,7);e=1-1/p
    require(-F(1,8)+e*(1-F(1,4))==F(1,10),'expanded optical exponent')
    require(F(1,2)-F(1,4)==F(1,4),'weighted finite-count exponent')
    require(F(1,4)*F(1,32)==F(1,128),'short residence mass exponent')
    counts['exponent_family']+=3
    for xi in [F(1,128),F(1,8),F(19,100),F(199,1000)]:
        required=xi/(1-2*xi)
        e=(required+F(1,3))/2;p=1/(1-e)
        require(1<p<F(3,2) and e*(1-2*xi)-xi>0,'strict xi<1/5 family')
        counts['exponent_family']+=1
    require(F(3,10)*(1-F(1,4))-F(1,8)>F(31,1408),'improved explicit exponent')
    counts['exponent_family']+=1
    # Check the positive trace estimate on analytic positive densities.
    # A=scale exp(rate*u), I=max(1,abs(rate)), D=1 satisfies |A'|<=DAI.
    for p,rate,scale,d in itertools.product([1.05,10/7,1.49],[-2.,-.1,0.,.4,3.],[.03,1.,20.],[.05,.3,1.]):
        I=max(1.,abs(rate));lo=-3*d;hi=d
        energy=scale*I**p*((math.exp(rate*hi)-math.exp(rate*lo))/rate if rate else hi-lo)
        trace=scale*max(math.exp(rate*lo),math.exp(rate*hi))
        bound=2**(p-1)*(d**-1+(8*d)**(p-1)/p**p)*energy
        require(trace<=bound*(1+1e-12),'positive density trace fixture')
        counts['trace_fixtures']+=1
    for w0,wh,a0,ah in itertools.product([F(0),F(1,4),F(1)], [F(0),F(3,4),F(1)], [F(1,8),F(1),F(4)], [F(1,8),F(1),F(4)]):
        require(abs(wh*ah-w0*a0)<=abs(ah-a0)+ah*abs(wh-w0),'full weighted variation split')
        counts['weighted_variation']+=1
    for z,l,a,d,w in itertools.product(vals,vals,[F(1,4),F(1)], [F(1,4),F(1)], [F(0),F(1,3),F(1)]):
        residual=w*int(z<a or l<d)
        require(0<=residual<=w,'original union domination')
        require(residual<=w*(int(z<a)+int(l<d)),'mass upper comparison')
        counts['source_union']+=2
    for rho,p in itertools.product([.2,.8,.98],[33/32,10/7,1.49]):
        c=(2-p)/4*math.log(1/rho)
        exact_sup=(2/c)**2*math.exp(-2)
        for m in [2,3,10,100,1000]:
            require(m*m*math.exp(-c*m)<=exact_sup*(1+1e-12),'uniform exponential polynomial envelope')
            counts['remainder_bound']+=1
    return {'counts':counts,'total_checks':sum(counts.values()),'scope':'finite parameter arithmetic, exact caps and source splits, analytic trace examples only; no continuum or spectral certification','full_raw_return_LLT_proved':False,'formal_proof_certificate':False,'independent_human_review':False}

if __name__=='__main__':print(json.dumps(checks(),indent=2,sort_keys=True))
