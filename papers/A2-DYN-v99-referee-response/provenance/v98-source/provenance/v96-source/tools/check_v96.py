#!/usr/bin/env python3
"""Finite rational transfer fixtures. Not a continuum or billiard proof certificate."""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
import json


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def checks() -> dict:
    c = {k: 0 for k in ('weighted_transfer','unweighted_transfer','same_label',
        'jacobian_direction','packet_variation','failure_partition','radial_core',
        'exponents','reentry_count')}
    weights = (F(0), F(1,4), F(1,2), F(3,4), F(1))
    # Each row represents one physical transverse sheet. Occupation is time,
    # not a number of returns; rows are not duplicated at sampled roofs.
    for a0,D,w0,kappa in product((F(1,4),F(1),F(3)),(F(1),F(2),F(4)),weights,weights):
        anchors = [a0/D,a0,2*a0,a0/(2*D)]
        valid = [i for i,a in enumerate(anchors) if a0 <= D*a]
        for wp in weights:
            if abs(w0-wp)>kappa: continue
            for mask in product((False,True),repeat=4):
                chosen=[i for i in valid if mask[i]]
                if not chosen: continue
                beta=F(len(chosen),4)
                rhs=D/beta*sum((anchors[i]*(wp+kappa)/4 for i in chosen),F(0))
                require(a0*w0<=rhs,'weighted occupation inequality')
                c['weighted_transfer']+=1
                unweighted=D/beta*sum((anchors[i]/4 for i in chosen),F(0))
                require(a0<=unweighted,'unweighted occupation inequality')
                c['unweighted_transfer']+=1
    for labels in product(range(3),repeat=5):
        for target in range(3):
            beta=F(sum(x==target for x in labels),5)
            require(beta<=1 and beta>=0,'occupation probability range')
            if all(x!=target for x in labels):
                require(beta==0,'neighboring labels cannot provide anchors')
            c['same_label']+=1
    a0,au,D=F(4),F(1),F(2)
    require(au/a0<=D and not a0/au<=D,'inverse-Jacobian direction negative control')
    c['jacobian_direction']+=1
    for vals in product(weights,repeat=5):
        M=min(vals[0],vals[-1]);V=sum(abs(b-a) for a,b in zip(vals,vals[1:]))
        require(abs(vals[2]-M)<=V,'same-segment packet error')
        require((vals[0]-M)+(vals[-1]-M)==abs(vals[0]-vals[-1]),'two-ended minimum identity')
        c['packet_variation']+=2
    for available in product((False,True),repeat=2):
        for compression in product((False,True),repeat=2):
            for occupied in product((False,True),repeat=2):
                bounded=[a and d for a,d in zip(available,compression)]
                admitted=any(b and o for b,o in zip(bounded,occupied))
                parts=(not any(available), any(available) and not any(bounded),
                       any(bounded) and not admitted)
                require(sum(parts)==int(not admitted),'disjoint failure partition')
                c['failure_partition']+=1
    Lambda=F(47,6)
    for a in (F(1,100),F(1,10),F(1,2)):
        r=a*a/(8*Lambda)
        require(a*a/4+2*Lambda*r==a*a/2,'inner-core forward radial cap')
        c['radial_core']+=1
    alpha,gamma=F(129,128),F(1,32)
    require(alpha/8==F(129,1024) and gamma/4==F(1,128),'original cofinal exponents')
    c['exponents']+=1
    for tau in (F(0),F(1,64),F(1,32),F(3,64)):
        N=2*(1+tau)+F(1,2)
        require(F(1,16)-tau>0 and N/2-1-tau>0,'outer schedule positive powers')
        c['exponents']+=1
    # Recurrent selector: split a fixed amount of occupation into arbitrarily
    # many tiny components. The bound depends on their total length only.
    for n in (1,2,4,8,32,128,1024):
        lengths=[F(1,4*n)]*n
        beta=sum(lengths,F(0))
        require(beta==F(1,4) and sum(lengths,F(0))/beta==1,'no return-count factor')
        c['reentry_count']+=1
    return {'counts':c,'total_checks':sum(c.values()),
        'scope':'finite rational transfer, same-label selection, coarea-direction, packet and parameter fixtures',
        'full_raw_return_LLT_proved':False,'formal_proof_certificate':False,
        'independent_human_review':False}

if __name__=='__main__':
    print(json.dumps(checks(),indent=2,sort_keys=True))
