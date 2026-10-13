#!/usr/bin/env python3
"""Exact finite identities and counterchecks; not a continuum proof certificate."""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
import json


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def integral_affine(a: F, c: F, f0: F, slope: F, lo: F, hi: F) -> F:
    x, y = max(a, lo), min(c, hi)
    if y <= x:
        return F(0)
    return f0*(y-x) + slope*((y-a)**2-(x-a)**2)/2


def ramp_current(a: F, c: F, f0: F, slope: F, t: F, r: F,
                 removed_fraction: F = F(0)) -> F:
    left = t-r
    value = F(0)
    if left < a <= t:
        value += (a-left)*f0/r
    if left < c <= t:
        value -= (c-left)*(f0+slope*(c-a))/r
    x, y = max(a,left), min(c,t)
    if y > x:
        bulk = ((y-left)**2-(x-left)**2)/(2*r)
        value += (slope-removed_fraction*max(slope,F(0)))*bulk
    return value


def checks() -> dict:
    counts = dict(stieltjes=0, signed_domination=0, interval_persistence=0,
                  entrance_anchor=0, radial_shell=0, exponents=0,
                  geometric_sum=0, cancellation_scope=0)
    for a,length,f0,slope,t,r,removed in product(
            (F(-1),F(0),F(1,2)),(F(1,4),F(1),F(2)),
            (F(0),F(1),F(3)),(F(-1),F(0),F(2)),
            (F(-1,2),F(1,8),F(3,4),F(3,2),F(3)),
            (F(1,4),F(1),F(2)),(F(0),F(1,3),F(1))):
        c=a+length
        if f0+slope*length < 0 or t in (a,c):
            continue
        current=f0+slope*(t-a) if a<t<c else F(0)
        average=integral_affine(a,c,f0,slope,t-r,t)/r
        pure=ramp_current(a,c,f0,slope,t,r)
        require(pure==current-average,'exact Stieltjes ramp')
        counts['stieltjes']+=1
        net=ramp_current(a,c,f0,slope,t,r,removed)
        gain=pure-net
        require(gain>=0 and max(net,F(0))<=current,'signed forcing dominated by actual source')
        require(current<=average+max(net,F(0))+gain,'signed pointwise comparison')
        if c<=t:
            require(net<=0,'completed prefixes cannot create positive forcing')
        counts['signed_domination']+=1
        for fraction in (F(1,5),F(1,2),F(4,5)):
            s=t-r*fraction
            if s in (a,c):
                continue
            earlier=f0+slope*(s-a) if a<s<c else F(0)
            x,y=max(a,s),min(c,t)
            ng=removed*max(slope,F(0))*max(y-x,F(0))
            signed=current-earlier-ng
            require(max(signed,F(0))<=current,'interval signed forcing')
            require(earlier>=current-max(signed,F(0))-ng,'full-interval persistence')
            counts['interval_persistence']+=1
    for length,f0,slope in product((F(1,8),F(1,2),F(1),F(3)),
                                 (F(0),F(1),F(4)),(F(-1),F(0),F(2))):
        if f0+slope*length<0:
            continue
        mass=f0*length+slope*length**2/2
        require(f0<=mass/length+abs(slope)*length,'complete incoming anchor')
        require(f0<=2*mass/length+abs(slope)*length,'residence-band incoming anchor')
        counts['entrance_anchor']+=2
    Lambda=F(4)
    for b,zratio,speed,extra,f0,slope in product(
            (F(1,8),F(1,2),F(1)),(F(0),F(1,4),F(3,4)),
            (F(1),F(2),F(4),F(8)),(F(0),F(1,2),F(1)),
            (F(1),F(4)),(F(-1),F(0),F(2))):
        z0sq=zratio*b*b
        ub=(b*b-z0sq)/speed
        u2=(4*b*b-z0sq)/speed
        t=u2+extra*b*b; r=t+b*b/10
        if f0+slope*t<0:
            continue
        require(u2-ub>=3*b*b/(2*Lambda),'radial shell roof length')
        require(z0sq+speed*t < b*b+2*Lambda*r,'target upper gradient')
        mean=integral_affine(F(0),t,f0,slope,ub,u2)/(u2-ub)
        value=f0+slope*t
        require(value<=mean+max(slope,F(0))*(t-ub),'whole radial-transit target estimate')
        counts['radial_shell']+=3
    alpha=F(129,128)
    for got,expected in ((alpha/2,F(129,256)),((alpha+1)/2,F(257,256)),
                         (alpha-1,F(1,128)),(F(1,12)*F(1,16),F(1,192)),
                         (2*(alpha+1)/2-1,F(129,128))):
        require(got==expected,'legal exponent arithmetic');counts['exponents']+=1
    for q,n in product((F(1,2),F(3,4),F(31,32)),range(1,24)):
        value=sum((q**j for j in range(n)),F(0))
        require(value==(1-q**n)/(1-q) and value<=1/(1-q),'finite band sum before collision limit')
        counts['geometric_sum']+=1
    for d in (F(1,8),F(1,32),F(1,128)):
        # A completed pulse has a positive entrance budget but no positive net forcing.
        require(ramp_current(F(0),d,F(1),F(0),F(1,2),F(1))==-d,'completed-pulse cancellation')
        # A live narrow pulse still has height one: no false charge-zero certificate.
        require(ramp_current(F(0),d,F(1),F(0),d/2,F(1))==1-d/2,'live pulse retains signed forcing')
        counts['cancellation_scope']+=2
    return {'counts':counts,'total_checks':sum(counts.values()),
            'scope':'finite exact-rational identities, shell inequalities and cancellation counterchecks only',
            'full_raw_return_LLT_proved':False,'independent_human_review':False,
            'formal_proof_certificate':False}


if __name__=='__main__':
    print(json.dumps(checks(),indent=2,sort_keys=True))
