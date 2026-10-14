#!/usr/bin/env python3
"""Finite algebra and norm fixtures; not a continuum proof certificate."""
from __future__ import annotations
from fractions import Fraction as F
import itertools
import json
import math


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def checks() -> dict:
    counts = dict(gluing=0, domination=0, surface_scaling=0,
                  potential_scaling=0, exponents=0, topology=0)
    gamma, Q = F(1,32), F(32,31)
    require(1-1/Q == gamma, 'critical normalization')
    for n in range(1,6):
        for parts in itertools.product((0.,.01,.25,1.),repeat=n):
            total=sum(parts)
            if total == 0: continue
            lhs=sum(x**float(gamma) for x in parts)
            rhs=n**float(1/Q)*total**float(gamma)
            require(lhs <= rhs*(1+1e-12), 'finite measurable-set gluing')
            counts['gluing']+=1
    for mu,D,x in itertools.product((F(0),F(1,100),F(1),F(3)),
                                     (F(0),F(1,7),F(2)),
                                     (F(1,1000),F(1,10),F(1),F(9))):
        val=float(min(mu,D*x))/float(x)**float(gamma)
        bound=float(D)**float(gamma)*float(mu)**float(1/Q)
        require(val <= bound*(1+1e-12)+1e-13,'bounded-reference domination')
        counts['domination']+=1
    for L,r in itertools.product((F(1,10),F(1),F(11,3)),
                                (F(1,100),F(1,8),F(1,3))):
        n=math.ceil(L/r)
        require(n <= (L+r)/r,'ceiling cover')
        lhs=n**float(1/Q)*float(r)
        rhs=float(L+r)**float(1/Q)*float(r)**float(gamma)
        require(lhs <= rhs*(1+1e-12),'matched-window power survives gluing')
        counts['surface_scaling']+=1
    require(F(3,8)*Q == F(12,31),'potential kernel integrable at Q')
    require(1/Q-F(3,8) == F(19,32),'local potential exponent')
    require(1+1/Q-F(3,8)-1/Q == F(5,8),'glued potential exponent')
    counts['potential_scaling']=3
    require(F(1,128)/Q == F(31,4096),'cofinal critical norm exponent')
    require(F(31,4096)*Q == F(1,128),'maximal exceptional measure exponent')
    require(F(129,128)/8 > F(1,128),'short-residence term dominates')
    require(F(1,12)*F(1,16)==F(1,192),'reconstruction exponent')
    require(F(4)*gamma>F(1,16) and F(4,2)-1>0,'legal outer width')
    require(F(1,2)/Q == F(31,64),'diffusive norm Jacobian')
    counts['exponents']=6
    # Shrinking pulses: finite critical convergence is not height convergence.
    for d in (F(1,10),F(1,100),F(1,1000)):
        norm=float(d)**float(1/Q)
        require(0<norm<1,'pulse finite norm vanishes, height stays one')
        counts['topology']+=1
    return {'counts':counts,'total_checks':sum(counts.values()),
            'formal_proof_certificate':False,'independent_human_review':False,
            'full_raw_return_LLT_proved':False,
            'scope':'finite inequalities, exponent arithmetic and topology fixtures only'}

if __name__=='__main__':
    print(json.dumps(checks(),indent=2,sort_keys=True))
