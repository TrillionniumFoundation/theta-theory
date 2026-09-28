#!/usr/bin/env python3
"""Finite diagnostics for the compact-experiment revision, not a proof audit.
Uses explicit exceptions so that python -O executes the same checks.
"""
from __future__ import annotations
from decimal import Decimal, localcontext
from fractions import Fraction
import json
import math


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def triangular_affinity(left: Decimal, right: Decimal) -> Decimal:
    """Affinity of 2*(L-x)_+/L**2 on [0,2], for 0 < L < 2."""
    a, b = sorted((left, right))
    require(Decimal(0) < a <= b < Decimal(2), 'invalid triangle length')
    d = b-a
    if not d:
        return Decimal(1)
    root = (a*b).sqrt()
    integral = (a+d/2)*root/2-d*d/8*((a+d/2+root)/(d/2)).ln()
    return 2*integral/(a*b)


def run_checks() -> dict:
    cases = 0
    for p in (Fraction(1, 2), Fraction(1, 3), Fraction(9, 25)):
        mean_t, var_t = 1/p, (1-p)/(p*p)
        mean_score = (1-p*mean_t)/(1-p)
        info = p*p*var_t/((1-p)*(1-p))
        require(mean_score == 0, 'geometric score is not centered')
        require(info == 1/(1-p), 'geometric log-probability information')
        cases += 2
    affinity = (Fraction(3, 5)*Fraction(5, 13))/(1-Fraction(4, 5)*Fraction(12, 13))
    require(affinity == Fraction(15, 17), 'exact geometric affinity')
    require(2-2*affinity == Fraction(4, 17), 'Hellinger convention')
    triangle = []
    with localcontext() as context:
        context.prec = 70
        for exponent in (2, 3, 4, 5, 6):
            shift = Decimal(10) ** (-exponent)
            affinity_t = triangular_affinity(Decimal(1), 1+shift)
            hellinger = 2-2*affinity_t
            ratio = hellinger/(shift*shift*(1/shift).ln())
            require(0 < hellinger < 10*shift*shift*(Decimal(1)/shift).ln(),
                    'triangular Hellinger diagnostic')
            require(Decimal('0.35') < ratio < Decimal('0.65'),
                    'boundary leading coefficient diagnostic')
            triangle.append({'shift':str(shift), 'scaled_H2':format(ratio,'.12f')})
    rates = []
    for k in (10**4, 10**6, 10**8):
        low, high = 0.0, 0.1
        for _ in range(160):
            mid = (low+high)/2
            if k*mid*mid*math.log(1/mid) < 1:
                low = mid
            else:
                high = mid
        delta = (low+high)/2
        j = 2*math.ceil(math.log(k))
        eta = 1/(j*math.sqrt(k))
        require(abs(k*delta*delta*math.log(1/delta)-1) < 1e-12,
                'critical scale root')
        rates.append({'k':k, 'j':j, 'delta':delta,
                      'j_delta':j*delta,
                      'fast_endpoint_bound':k*eta*eta*math.log(1/eta),
                      'finite_bridge_bound':k*(0.5**j)})
    require(all(rates[i+1]['j_delta'] < rates[i]['j_delta'] for i in range(2)),
            'illustrative slow-count rate ordering')
    require(all(rates[i+1]['fast_endpoint_bound'] < rates[i]['fast_endpoint_bound']
                for i in range(2)), 'illustrative fast-endpoint rate ordering')
    # An exact finite-space instance of the finite-net triangle inequality.
    p, p0 = (Fraction(1, 3),Fraction(2, 3)), (Fraction(2, 5),Fraction(3, 5))
    q0, q = (Fraction(1, 2),Fraction(1, 2)), (Fraction(3, 5),Fraction(2, 5))
    tv = lambda x,y: sum(abs(a-b) for a,b in zip(x,y))/2
    require(tv(p,q) <= tv(p,p0)+tv(p0,q0)+tv(q0,q), 'finite-net triangle')
    return {'revision':'A2 v32','status':'passed',
            'scope':'Exact scalar identities, a closed-form moving-boundary diagnostic, and illustrative rate sequences only; not a billiard realization, full theorem certification, or native-main build.',
            'exact_geometric_score_checks':cases,'exact_geometric_affinity':str(affinity),
            'triangular_boundary_diagnostic':triangle,'illustrative_rates':rates,
            'finite_net_triangle':'passed'}


if __name__ == '__main__':
    print(json.dumps(run_checks(),indent=2,sort_keys=True))
