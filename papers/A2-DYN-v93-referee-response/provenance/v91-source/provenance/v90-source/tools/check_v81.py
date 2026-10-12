#!/usr/bin/env python3
"""Exact finite regression fixtures; not a continuum proof certificate."""
from __future__ import annotations
from fractions import Fraction as F
import itertools
import json
from check_v77 import require


def capped_integral(s: F, d: F, root: F) -> F:
    """s^-1 min(d,s^2)+ integral_0^s v^-2 min(d,v^2) dv."""
    require(root*root==d and s>0 and d>0, 'exact square-root fixture')
    if s<=root:
        return 2*s
    return d/s+root+d*(1/root-1/s)


def checks() -> dict:
    counts={'exponents':0,'cap_integrals':0,'strong_vector_scaling':0,
            'terminal_interpolation':0,'truncated_layer_cake':0,
            'fractional_integrability':0,'optical_flux':0,
            'limit_order_diagnostic':0}
    theta=F(31,32); alpha=F(129,128); beta=F(17,16)
    left_a=F(63,64)+F(7,8)*(1-theta)
    left_s=F(3,2)*theta
    right_a=F(7,8)*(1-theta)+theta+F(1,32)
    right_s=F(47,32)*theta*F(3,4)
    for actual,expected in [(left_a,F(259,256)),(left_s,F(93,64)),
                            (right_a,F(263,256)),(right_s,F(4371,4096))]:
        require(actual==expected,'exact chronological exponent')
        counts['exponents']+=1
    for a,s in [(left_a,left_s),(right_a,right_s)]:
        require(a>alpha>1 and s>beta>1,'strict integrability margin')
        counts['exponents']+=1
    require(alpha-1==F(1,128),'critical gain')
    counts['exponents']+=1
    grid=(F(1,100),F(1,20),F(1,4),F(1,2),F(1))
    for s,root in itertools.product(grid,repeat=2):
        actual=capped_integral(s,root*root,root)
        require(actual==2*min(s,root),'capped inverse incidence integral')
        counts['cap_integrals']+=1
    # After raising to the eighth power the stable-vector inequality is rational.
    for length,width in itertools.product(grid,repeat=2):
        require(min(length,width)**8/length<=width**7,'strong stable vector scaling')
        counts['strong_vector_scaling']+=1
    for a,s in itertools.product(grid,repeat=2):
        # min(A,B) <= A^(1/4) B^(3/4); check fourth powers exactly.
        require(min(a,s)**4<=a*s**3,'terminal geometric interpolation')
        counts['terminal_interpolation']+=1
    for lower,upper,z in itertools.product(grid,repeat=3):
        if lower>=upper: continue
        lhs=1/z if lower<=z<upper else F(0)
        rhs=F(0)
        if z<upper:
            rhs=1/upper+(1/max(lower,z)-1/upper)
        require(lhs<=rhs,'positive first-inverse majorant')
        counts['truncated_layer_cake']+=1
    for eta in (F(1,100),F(1,8),F(1,4),F(49,100)):
        require(alpha-eta>0 and F(1,2)-eta>0,'both fractional layer cakes integrable')
        counts['fractional_integrability']+=1
    require(F(1,2)-F(1)==-F(1,2),'first inverse finite-count error cannot be integrated to zero')
    counts['fractional_integrability']+=1
    for w0,w1,w2 in itertools.product((F(0),F(1,8),F(1,2),F(1),F(2)),repeat=3):
        negative=max(F(0),w0-w1)+max(F(0),w1-w2)
        require(max(F(0),w0-w2)<=negative,'survivor optical variation')
        require(w0<=w2+negative,'nongrazing boundary weight plus paid drift')
        if w2==0: require(w0<=negative,'grazing starting weight paid')
        counts['optical_flux']+=1
    # Finite samples illustrate, but do not prove, the noncommuting-limit warning.
    for cutoff in (F(1,2),F(1,4),F(1,10)):
        n=1+2*cutoff.denominator
        require(F(1,n)<cutoff,'a shrinking critical shell can lie below a fixed cutoff')
        counts['limit_order_diagnostic']+=1
    return {'counts':counts,'total_checks':sum(counts.values()),
            'alpha':str(alpha),'beta':str(beta),'delta':str(alpha-1),
            'scope':'finite rational identities, cap integrals and positive-variation fixtures only',
            'formal_proof_certificate':False,'independent_human_review':False,
            'untruncated_first_inverse_gradient_concentration_proved':False,
            'full_raw_return_LLT_proved':False}


if __name__=='__main__':
    print(json.dumps(checks(),indent=2,sort_keys=True))
