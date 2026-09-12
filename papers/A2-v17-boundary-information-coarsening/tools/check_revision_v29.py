#!/usr/bin/env python3
"""Exact finite diagnostics for A2 v29; not a substitute for its proofs."""
from __future__ import annotations
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json

COUNTS: dict[str, int] = {}

def check(name: str, condition: bool) -> None:
    if not condition:
        raise RuntimeError('Failed diagnostic: ' + name)
    COUNTS[name] = COUNTS.get(name, 0) + 1

def ratio(f, u: Q, v: Q) -> Q:
    return f(u, v) * f(Q(0), Q(0)) / (f(u, Q(0)) * f(Q(0), v))

def poly(coefficients: tuple[Q, ...], x: Q) -> Q:
    result = Q(0)
    for coefficient in reversed(coefficients):
        result = result * x + coefficient
    return result

def main() -> None:
    grid = tuple(Q(n, 24) for n in range(-7, 8))
    anchors = (Q(1, 6), Q(1, 4))
    # Asymmetric exact models. Positive quadratic coefficients, small odd jets,
    # and positive amplitudes on the interior square are checked explicitly.
    for cubic in (Q(-1, 7), Q(0), Q(1, 5)):
        def s(u):
            return u*u + cubic*u**3 + Q(1, 8)*u**4
        def b(u):
            return 1 + Q(1, 9)*u + Q(1, 10)*u*u
        def f(u, v):
            return b(u)*b(v)*(1-s(u)-s(v))
        def fr(u, v):
            return f(-u, -v)
        for a in anchors:
            for sign in (-1, 1):
                alpha = sign*a
                qa = s(alpha)/(1-s(alpha))
                check('exact_positive_anchor', qa > 0)
                check('exact_anchor_radical', 1-ratio(f,alpha,alpha) == qa*qa)
                for u in grid:
                    t = (1-ratio(f,u,alpha))/qa
                    tr = (1-ratio(fr,u,-alpha))/qa
                    expected = s(u)/(1-s(u))
                    check('exact_action_recovery', t/(1+t) == s(u))
                    check('exact_amplitude_recovery', f(u,0)/f(0,0)*(1+t) == b(u)/b(0))
                    check('exact_rank_one_slice', t == expected)
                    check('exact_transport_action', tr/(1+tr) == s(-u))
                    for v in grid:
                        check('exact_positive_interior', f(u,v)>0)
                        check('exact_rank_one_identity', 1-ratio(f,u,v) == expected*s(v)/(1-s(v)))
    # General polynomial perturbations: no rank-one identity is imposed.
    # Equality of the radicals and numerators, without taking floating-point
    # square roots, proves equality of the formula outputs on these samples.
    for zeta in (Q(1,100), Q(-1,100), Q(1,1000)):
        def f(u,v):
            return (1-u*u-v*v)*(1+zeta*u*v*(u+v))
        def fr(u,v):
            return f(-u,-v)
        for a in anchors:
            for sign in (-1,1):
                alpha=sign*a
                d=1-ratio(f,alpha,alpha)
                dr=1-ratio(fr,-alpha,-alpha)
                check('off_model_radical_positive', d>0)
                check('off_model_radical_transport', d==dr)
                for u in grid:
                    n=1-ratio(f,-u,alpha)
                    nr=1-ratio(fr,u,-alpha)
                    check('off_model_numerator_transport', n==nr)
                    check('off_model_axis_transport', fr(u,0)/fr(0,0)==f(-u,0)/f(0,0))
                    # n/sqrt(d) > -1, tested exactly by its equivalent alternatives.
                    check('off_model_formula_denominator', n>=0 or n*n<d)
                    for v in grid:
                        check('off_model_positive_interior', f(u,v)>0)
                        check('off_model_ratio_transport', ratio(fr,u,v)==ratio(f,-u,-v))
    # The referee's witness is independently recomputed, not assumed.
    a,zeta=Q(1,4),Q(1,100)
    D=(a*a/(1-a*a))**2
    h=2*zeta*a**3*Q(224,225)
    left,right=D+h,D*D/(D-h)
    check('witness_exact_values', (D,h,left,right)==(Q(1,225),Q(7,22500),Q(107,22500),Q(4,837)))
    check('witness_nonzero_difference', left-right==-Q(49,2092500))
    check('witness_arbitrarily_small', all(-h0*h0/(D-h0)!=0 for h0 in (h,h/10,h/100)))
    # Finite-jet projection and reflection, including nonzero spurious anchors.
    for degree in range(2,13):
        coefficients=tuple(Q((-1)**n,n+1) for n in range(degree+1))
        reflected=tuple((-1)**n*c for n,c in enumerate(coefficients))
        projected=(Q(0),Q(0))+coefficients[2:]
        reflected_projected=(Q(0),Q(0))+reflected[2:]
        for u in grid:
            check('projection_commutes_with_reflection', poly(reflected_projected,u)==poly(projected,-u))
            check('jet_parity', poly(reflected,u)==poly(coefficients,-u))
    # Forgetting maps on a finite stopped-history fixture with a terminal
    # censored failure run. This checks encoding, not an asymptotic theorem.
    full=((('channel-a',12),None),(('channel-a',12),(Q(1,5),Q(-1,7),Q(1,9))),
          (('channel-b',14),None))
    et=full
    ce=tuple((design,None if mark is None else mark[:2]) for design,mark in et)
    successes=tuple(i for i,(_,mark) in enumerate(ce) if mark is not None)
    counts=(successes[0]+1,len(ce)-successes[-1]-1)
    restored=(False,)*(counts[0]-1)+(True,)+(False,)*counts[-1]
    check('terminal_censoring_encoding', restored==tuple(mark is not None for _,mark in ce))
    check('endpoint_output_factorization', tuple(mark for _,mark in ce if mark is not None)==
          tuple(mark[:2] for _,mark in et if mark is not None))
    script=Path(__file__).read_bytes()
    result={'revision':'A2 v29','status':'passed','arithmetic':'exact rational',
            'script_sha256':hashlib.sha256(script).hexdigest(),
            'checks_by_family':COUNTS,'total_checks':sum(COUNTS.values()),
            'fixed_anchor_witness':{'left_square':str(left),'right_square':str(right),
                                    'difference':str(left-right)},
            'scope':'Finite algebraic diagnostics only. No certification of infinite half-line convergence, full native compilation, or global statistical theorems.'}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
