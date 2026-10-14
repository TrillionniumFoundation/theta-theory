#!/usr/bin/env python3
"""Exact finite diagnostics for v107; not a continuum proof certificate."""
from fractions import Fraction as F
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def checks():
    algebra = envelope = geometry = 0
    for left in range(9):
        for right in range(9):
            p, c, e = max(left, right), min(left, right), abs(left-right)
            require(p == c+e, 'two-ended envelope identity')
            envelope += 1
    for C in range(11):
        for D in range(8):
            for E in range(8):
                for kappa in (F(1,3), F(1), F(3), F(7,2)):
                    P = D+E
                    beta = min(F(1), kappa*P/C) if C else F(0)
                    alpha = min(beta, kappa*D/C) if C else F(0)
                    require(0 <= alpha <= beta <= 1, 'fractions')
                    require(beta*C <= kappa*P, 'capacity')
                    require((beta-alpha)*C <= kappa*E, 'full trace-loss payment')
                    require((1-beta)*C == max(F(0), C-kappa*P), 'exact capacity residual')
                    require(beta*C+(1-beta)*C == C, 'positive original split')
                    algebra += 1
    r = F(1,2)
    for a in (F(-2), F(-1), F(0)):
        for length in (F(1,4), F(1), F(3,2)):
            b = a+length
            for pad in (F(0), F(1,3), F(2)):
                ca, cb = a-pad, b+r+pad
                delta = cb-ca+F(1,7)
                for fraction in (F(1,9), F(1,2), F(8,9)):
                    t = a+fraction*length
                    require(ca < t and t+r < cb, 'actual translated source inclusion')
                    require(t-delta < ca and cb < t+delta, 'entire moving comparison in window')
                    require(-cb < -t-r and -t < -ca, 'negative-orientation reflection')
                    geometry += 1
    good = (F(1,3), F(2,3))
    bad = (F(1), F(1), F(1))
    require(sum(good) == 1 and sum(bad) == 3, 'physical comparison overlap')
    for m in (2, 10, 100, 1000):
        width, height = F(1,m), F(1)
        require(width/2 == F(1,2*m) and height == 1, 'limit-order diagnostic')
    return {'endpoint_envelope_cases': envelope, 'exact_capacity_cases': algebra,
            'moving_window_cases': geometry, 'overlap_diagnostics': 2,
            'limit_order_diagnostics': 4, 'formal_proof_certificate': False,
            'global_lorentz_coverage_tested': False}


if __name__ == '__main__':
    print(json.dumps(checks(), indent=2, sort_keys=True))
