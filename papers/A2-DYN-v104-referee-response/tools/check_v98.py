#!/usr/bin/env python3
"""Finite algebra fixtures; neither billiard realization nor a proof certificate."""
from __future__ import annotations
from fractions import Fraction as F
import itertools
import json
import math
import random


def require(test: bool, message: str) -> None:
    if not test:
        raise RuntimeError(message)


def checks() -> dict:
    counts = dict(optical_cap=0, area_jacobian=0, two_cap_layer_cake=0,
                  residual_partition=0, clock_compression=0,
                  paired_trace=0, exact_exponents=0)
    tau, R, q = F(3, 50), F(47, 100), F(47, 53)
    v = 2*tau/R
    copt = R/tau*(1+(1+v)/v*2*q/(1-q))
    rng = random.Random(980235)
    for m in range(1, 10):
        for _ in range(12):
            lengths = [tau+F(rng.randrange(100), 100) for _ in range(m)]
            cosines = [F(1, rng.choice([1, 2, 3, 10, 1000])) for _ in range(m-1)]
            yy, ff = lengths[0], F(1)
            for i, ci in enumerate(cosines, 1):
                ff += 2*yy/(R*ci)
                yy += lengths[i]*ff
            prod = math.prod((1+v/ci for ci in cosines), start=F(1))
            require(yy >= tau*prod, 'positive optical denominator')
            insertion = 1+sum((q**min(i,m-i)/ci for i,ci in enumerate(cosines,1)), F(0))
            require(insertion*R/yy <= copt*(1+v)**(-(m-1)), 'full incidence cancellation')
            counts['optical_cap'] += 2
            for i, ci in enumerate(cosines):
                lhs = 1/(ci*prod)
                require(lhs <= (1/v)*(1+v)**(-(m-2)), 'selected incidence cancellation')
                counts['optical_cap'] += 1
    for radius, aa, bb, cc in itertools.product([F(9,20), R], [F(2),F(3)], [F(-1,4),F(-1,2)], [F(2),F(4)]):
        detk = aa*cc-bb*bb
        omega = abs(bb)/radius
        # dx/dq has rows (1,0),(-K00/R,-K0m/R).
        detx = -bb/radius
        require(detk > 0 and abs(detk/detx) == detk/omega, 'physical area normalization')
        counts['area_jacobian'] += 1
    for H, t, rootb in itertools.product([F(1,7),F(1),F(23)],
                                         [F(1,100),F(1,3),F(1),F(4)],
                                         [F(1,1000),F(1,20),F(1,3),F(1),F(5)]):
        E, b, crossing = H*t**3, rootb**2, t**2
        exact = 2*H*b if b <= crossing else 3*H*t*t-E/rootb
        upper = 3*min(H*b,H*t*t)
        require(0 <= exact <= upper, 'complete two-cap integral')
        # Independent split integration of E v^(-3/2) and H.
        endpoint = min(E*rootb,H*b*b)/b
        integral = H*b if b <= crossing else H*crossing+2*E*(1/t-1/rootb)
        require(endpoint+integral == exact, 'two-cap split identity')
        counts['two_cap_layer_cake'] += 2
    d, a = F(1,10), F(1,5)
    for back, forward, z, lowclock in itertools.product(
            [F(1,100),d,2*d,3*d], [F(1,100),d,2*d,4*d], [a/2,a,2*a], [False,True]):
        protected = back > 2*d or (back <= 2*d and z >= a and forward > d)
        residual = lowclock and not protected
        short = residual and back+forward <= 3*d
        critical = residual and back+forward > 3*d
        require(int(residual) == int(short)+int(critical), 'disjoint original residual')
        require(not critical or (back <= 2*d and z<a and forward>d), 'critical forward interval')
        counts['residual_partition'] += 2
    for vals in itertools.product([F(1,4),F(1,2),F(1),F(2)], repeat=4):
        clock = F(1,4)*sum(min(F(1), x) for x in vals)
        if all(x>=F(1,2) for x in vals):
            require(clock>=F(1,2), 'full available interval clock lower bound')
        if min(vals)<F(1,2):
            chain=[F(1),*vals]
            require(sum(abs(y-x) for x,y in zip(chain,chain[1:]))>F(1,2), 'running loss pays initial density')
        counts['clock_compression'] += 1
    for vals in itertools.product([F(0),F(1,4),F(1),F(3)], repeat=5):
        variation=sum(abs(y-x) for x,y in zip(vals,vals[1:]))
        paired=min(vals[0],vals[-1])
        for x in vals:
            require(abs(x-paired)<=variation, 'both physical endpoint traces retained')
            counts['paired_trace'] += 1
        require(not (vals[0]==0 or vals[-1]==0) or paired==0, 'grazing end has zero paired trace')
        counts['paired_trace'] += 1
    alpha=F(129,128)
    require(alpha-1==F(1,128), 'first inverse-gradient leading exponent')
    require(1+(alpha-1)/2==F(257,256), 'critical target-height exponent')
    require(4*F(257,256)==F(257,64) and 4-1==3, 'legal reconstruction schedule')
    require(F(2,3)+F(1,3)==1 and 3*F(2,3)==2, 'spectral-geometric cube powers')
    counts['exact_exponents'] += 4
    return {'counts':counts,'total_checks':sum(counts.values()),
            'scope':'finite exact algebra and deterministic sequences; not physical orbit realization',
            'spectral_capacity_condition_verified':False,
            'full_raw_return_LLT_proved':False,
            'independent_human_review':False,'formal_proof_certificate':False}


if __name__=='__main__':
    print(json.dumps(checks(),indent=2,sort_keys=True))
