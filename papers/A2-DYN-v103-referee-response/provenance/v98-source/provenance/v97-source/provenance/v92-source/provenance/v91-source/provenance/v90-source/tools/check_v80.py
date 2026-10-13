#!/usr/bin/env python3
"""Finite regression fixtures; not a proof certificate for continuum estimates."""
from __future__ import annotations
from fractions import Fraction as F
import itertools
import json
import math
from check_v77 import require


def checks() -> dict:
    counts=dict(strip_lengths=0,interpolation_exponents=0,capped_layer_cake=0,
                depth_summation=0,optical_variation=0,coarea_orientation=0,
                flow_box_exhaustion=0,optical_normalization=0,limit_order=0)
    for k in range(2,100):
        width=F(1,k*k)-F(1,(k+1)*(k+1))
        require(F(1,k**3)<=width<=F(3,k**3),'quadratic-strip cubic width')
        # At the grazing edge s=(k+1)^-2, width <= 6*s^(3/2).
        require(width<=F(6,(k+1)**3),'edge-crossing homogeneous width')
        counts['strip_lengths']+=2
    require(F(3,2)-F(1,16)==F(23,16),'projected physical weak exponent')
    require(F(3,2)*F(7,8)==F(21,16),'long-left exponent')
    require(F(23,16)*F(7,8)==F(161,128)>F(5,4),'long-right strict exponent')
    require(F(3,2)*F(1,24)==F(1,16),'fixed peak refinement loss')
    require(F(31,32)>F(7,8),'strict interpolation logarithm allowance')
    counts['interpolation_exponents']+=5
    for s,d in itertools.product((F(1,100),F(1,8),F(1,3),F(3,4)),repeat=2):
        D=d*d
        if s<=d:
            boundary=s
            integral=s
        else:
            boundary=D/s
            integral=d+D*(1/d-1/s)
        require(boundary+integral==2*min(s,d),'exact a=1 capped layer integral')
        counts['capped_layer_cake']+=1
    require(1+F(1,1)/(F(5,4)-1)==5,'leading a=1 layer constant')
    counts['capped_layer_cake']+=1
    q=F(47,53)
    for m in range(2,64):
        weights=sum((q**min(i,m-i) for i in range(1,m)),F(0))
        require(weights<=2*q/(1-q),'complete additive depth sum')
        counts['depth_summation']+=1
    grid=(F(0),F(1,10),F(1,2),F(1),F(3))
    for seq in itertools.product(grid,repeat=4):
        neg=sum((max(F(0),a-b) for a,b in zip(seq,seq[1:])),F(0))
        require(max(F(0),seq[0]-seq[-1])<=neg,'survivor optical variation')
        require(seq[0]<=seq[-1]+neg,'nongrazing pullback plus drift')
        if seq[-1]==0:
            require(seq[0]<=neg,'grazing starting mass paid, not deleted')
            counts['optical_variation']+=1
        counts['optical_variation']+=2
    for w0,w1,c0,c1 in itertools.product((F(1,4),F(1),F(4)),repeat=4):
        source=w0/c0; target=w1/c1
        J=(w1/w0)*(c0/c1)
        require(J*source==target,'physical target Jacobian direction')
        require((w1/w0)*source <=16*J*source,
                'bounded chi ratio comparison')
        counts['coarea_orientation']+=2
    # Nested precompact boxes; overlaps are not absorbing seams.
    intervals=[(F(-1)+F(1,n),F(2)-F(1,n)) for n in range(2,20)]
    for t,h in itertools.product((F(-1,2),F(0),F(1,2),F(1)),(F(1,8),F(1,2),F(3,2))):
        killed=[int(not(lo<t and t+h<hi)) for lo,hi in intervals]
        require(all(a>=b for a,b in zip(killed,killed[1:])),'nested exit indicator monotonicity')
        counts['flow_box_exhaustion']+=1
    require(F(0)<F(1,2)<F(1)<F(3,2),'overlapping flowbox coverage fixture')
    counts['flow_box_exhaustion']+=1
    for R,l0,l1,c in itertools.product((F(9,20),F(47,100)),(F(3,50),F(2,5)),
                                       (F(3,50),F(4,5)),(F(1,10),F(1))):
        V=2/(R*c)
        y2=l0+l1+V*l0*l1
        det=1/l0+1/l1+V
        require(y2==l0*l1*det,'two-flight optical continuant')
        for ce0,cem in ((F(1),F(1)),(F(1,2),F(3,4))):
            corner=R*R*ce0*cem/y2
            require(corner/R==R*ce0*cem/y2,'single endpoint conversion factor R')
            counts['optical_normalization']+=1
    # Widths depend only on outer parameters, never on collision count.
    for gamma,alpha in ((F(3),F(1)),(F(4),F(1,2)),(F(5),F(2))):
        require(gamma-alpha>0 and gamma/2-1>0,'outer width powers')
        counts['limit_order']+=1
    return {'counts':counts,'total_checks':sum(counts.values()),
            'scope':'finite rational identities and discrete source/Jacobian fixtures only',
            'full_raw_return_LLT_proved':False,
            'complete_critical_initial_defect_height_decay_proved':False,
            'complete_nongrazing_outgoing_flux_height_decay_proved':False,
            'independent_human_review':False,'formal_proof_certificate':False}


if __name__=='__main__':
    print(json.dumps(checks(),indent=2,sort_keys=True))
