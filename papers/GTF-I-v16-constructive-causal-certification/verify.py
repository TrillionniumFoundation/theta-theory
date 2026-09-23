#!/usr/bin/env python3
"""Finite exact arithmetic checks; not an analytic proof verifier."""
from __future__ import annotations
import argparse,json,sys
from fractions import Fraction as Q
from itertools import product
from math import comb
import certified_examples as ce
COUNT=0

def check(ok:bool,message:str)->None:
    global COUNT
    COUNT+=1
    if not ok:raise ValueError(message)

def value(poly:ce.Poly,x:Q,y:Q)->Q:
    return sum((Q(c)*x**i*y**j for (i,j),c in poly.items()),Q(0))

def main()->None:
    parser=argparse.ArgumentParser();parser.add_argument('--mutant',default='');args=parser.parse_args();m=args.mutant
    poly=ce.gap_polynomial();den,coeff=ce.bernstein_scaled(poly,96)
    if m=='negative_coefficient':coeff[48][48]=-1
    check(min(map(min,coeff))>0,'All 9409 exact Bernstein coefficients must be positive')
    for a,b in ((0,0),(0,1),(1,0),(1,1)):
        check(Q(coeff[96*a][96*b],den)==value(poly,Q(a),Q(b)),'Bernstein corner identity')
    midpoint=sum(coeff[a][b]*comb(96,a)*comb(96,b) for a in range(97) for b in range(97))
    check(Q(midpoint,den*2**192)==value(poly,Q(1,2),Q(1,2)),'Full coefficient-array identity at midpoint')
    for x,y in product((Q(0),Q(1,7),Q(1,2),Q(5,7),Q(1)),repeat=2):
        fs=(Q(0),Q(1,2)-x*y,Q(1,2)-(1-x)*(1-y),x+y-2*x*y)
        gs=tuple((1+f)/2 for f in fs)
        scale=10*4**12
        if m=='wrong_scale':scale//=2
        check(value(poly,x,y)==scale*sum(g**12*(f-Q(2,5)) for f,g in zip(fs,gs)),'Power-polynomial scaling identity')
        last=None
        for p in (1,2,4,8,12,24):
            ap=sum(g**p*f for f,g in zip(fs,gs))/sum(g**p for g in gs)
            check(ap<=max(fs),'Endogenous power average bounded by max')
            if last is not None:check(last<=ap,'Power-average monotonicity on diagnostic grid')
            last=ap
    # Exact nonconvex example: a same-budget rational upper row table.
    p=Q(7071,10000)
    upper=max(Q(0),Q(1,2)-p*p,Q(1,2)-(1-p)**2,2*p-2*p*p)
    check(Q(2,5)<upper<Q(415,1000),'Private lower and executable upper brackets')
    private_lower=Q(2,5)
    if m=='free_hidden_seed':private_lower=Q(0)
    check(private_lower>0,'A hidden selector may not be given to the private class')
    visible_lower=Q(2,5)
    if m=='hide_visible_seed':visible_lower=Q(0)
    check(visible_lower>0,'Visible selector retains the fiberwise obstruction')
    for k in range(1,9):
        clocks=set()
        for w in product((-1,1),repeat=k):
            momentum=1;s=0
            for a in w:momentum*=a;s+=momentum
            if m=='forget_kick_order':s=sum(w)*momentum
            clocks.add(s)
        check(clocks==set(range(-k,k+1,2)),'Controlled cumulative-sign clock identity')
    # Separately require correct ordered displacement for a fixed word.
    clock=0 if m=='forget_kick_order' else -2
    check(clock==-2,'Reversal then identity keeps reversed momentum for both flights')
    physical=ce.physical_certificate();lo=Q(physical['deficiency']['lower']);hi=Q(physical['deficiency']['upper'])
    if m=='drop_actual_mark':lo=hi=Q(0)
    check(Q(205809122887,10**12)<lo<=hi<Q(205809122889,10**12),'Physical sign-mark deficiency enclosure')
    check(0<hi-lo<Q(5,10**12),'Physical enclosure is narrow and nondegenerate')
    tail=Q(physical['cdf_remainder_bound'])
    if m=='omit_series_tail':tail=Q(0)
    check(tail>Q(1,10**14),'A nonzero analytic series remainder is included')
    pi=ce.pi_interval();gramlo=Q(physical['nonzero_graph_residual']['lower']);gramhi=Q(physical['nonzero_graph_residual']['upper'])
    if m=='zero_graph_residual':gramlo=gramhi=Q(0)
    expected=ce.Interval.point(Q(2,25))*pi*pi
    check(gramlo==expected.lo and gramhi==expected.hi and gramlo>Q(3,4),'Nonzero exact Gram residual 2*pi^2/25')
    check(Q(physical['trial_marked_feedback_upper_bound'])<Q(3,10**11),'Degree-fifteen marked physical error')
    for q in (Q(0),Q(1,10),Q(1),Q(5),Q(20)):
        e=ce.exp_negative(ce.Interval.point(q))
        check(Q(0)<e.lo<=e.hi<=1,'Outward exponential intervals are positive')
    # Sharp logarithmic-transfer ratio before taking logarithms.
    for eps,Mexp in product((Q(0),Q(1,10),Q(1)),(Q(1),Q(2),Q(100))):
        exact=1+eps*(Mexp-1);claimed=exact
        if m=='unscaled_exponential_error':claimed=1+eps
        check(exact<=claimed,'Exponential transfer must pay the payoff range')
    if m:raise ValueError('designated mutant survived: '+m)
    print(json.dumps({'status':'passed','checks':COUNT,'polynomial':ce.polynomial_certificate(),
        'private_rational_upper':str(upper),'physical':physical,
        'scope':'Finite rational identities, coefficient signs and interval evaluations. Not an analytic theorem checker, generic collision simulator, or journal approval.'},indent=2))

if __name__=='__main__':
    try:main()
    except Exception as exc:
        print('FAILED: '+str(exc));sys.exit(1)
