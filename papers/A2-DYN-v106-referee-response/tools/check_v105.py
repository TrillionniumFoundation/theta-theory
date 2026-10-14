#!/usr/bin/env python3
"""Exact finite rational fixtures; no continuum proof certification."""
from fractions import Fraction as F
from itertools import product
import math,json
from check_v104 import require,overlap
def checks():
    counts={'residence_persistence':0,'adaptive_reach':0,
            'paid_positive_deficit':0,'outer_exponents':0}
    v=(F(1,128),F(1,16),F(1,4),F(1),F(2),F(7,2))
    for a,l,h in product((F(-2),F(0),F(3,5)),v,v):
        if l<h:continue
        for j in range(1,16):
            t=a+l*F(j,16)
            require(overlap(t-h,t+h,a,a+l)>=h,
                    'uniform finite-count residence persistence')
            counts['residence_persistence']+=1
    for k,rho,d in product((1,2,3,5,9,23),(.001,.01,.1,.5,1.),
                             (0.,.2,.5)):
        x1=(rho/8)**(1/k);x2=(rho/2)**(1/k);x3=(3*rho/4)**(1/k)
        require(x1<x2<x3,'real reached levels')
        require(d+rho/8<1 and d+3*rho/4<4,
                'original short source and short comparator')
        require(3*rho/8>rho/4,'actual forward interval')
        require(x3-x2>=x1*math.log(1.5)/k*(1-1e-11),
                'adaptive elastic width')
        counts['adaptive_reach']+=4
    for P,E,kappa in product((F(0),F(1,4),F(1),F(4)),repeat=3):
        if E>P:continue
        for C in (F(0),kappa*P/2,kappa*P):
            require(max(F(0),C-kappa*(P-E))<=kappa*E,
                    'complete outgoing trace shortage')
            counts['paid_positive_deficit']+=1
    require(F(1,16)-F(1,32)==F(1,32),'balance budget')
    require(F(1,12)*F(1,32)==F(1,384),'growing cost B exponent')
    require(F(1,12)*F(1,16)==F(1,192),'fixed residence B exponent')
    counts['outer_exponents']+=3
    return {'counts':counts,'total_checks':sum(counts.values()),
      'formal_proof_certificate':False,'independent_human_review':False,
      'full_raw_return_LLT_proved':False}
if __name__=='__main__':print(json.dumps(checks(),indent=2,sort_keys=True))
