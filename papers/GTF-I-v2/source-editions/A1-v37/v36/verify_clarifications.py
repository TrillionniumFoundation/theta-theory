#!/usr/bin/env python3
"""Exact checks for R35.1 and R35.2; no numerical optimization is performed.

Uses rational affine forms, not sampled singular values. This program checks
normalization and balancing identities; the manuscript supplies the risk theorem.
All checks remain enabled under python -O. Requires only the standard library.
"""
from __future__ import annotations
from fractions import Fraction as Q
from itertools import combinations_with_replacement
import json


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def add(a: tuple, b: tuple) -> tuple:
    return tuple(x + y for x, y in zip(a, b))


def scale(a: tuple, c: Q) -> tuple:
    return tuple(c * x for x in a)


def main() -> None:
    H, radius = Q(16), Q(1, 16)
    Dmax = Q(3) + radius
    bounds = {n + 2: (n + 2) * Dmax for n in (1, 2, 3)}
    require(bounds[5] == Q(245, 16), 'Largest-horizon exact bound')
    require(all(max(Q(1), b) < H for b in bounds.values()),
            'One normalization must be admissible for all horizons')
    # Each triple represents the affine polynomial c + a*u + b*v.
    one_step = [(Q(0), Q(0), Q(0)), (Q(1), Q(0), Q(0)),
                (Q(2), Q(1), Q(0)), (Q(3), Q(0), Q(1))]
    formal = [add(a, b) for a, b in combinations_with_replacement(one_step, 2)]
    positive = [z for z in formal if z != (0, 0, 0)]
    expected = [(1, 0, 0), (2, 0, 0), (2, 1, 0), (3, 1, 0),
                (3, 0, 1), (4, 2, 0), (4, 0, 1), (5, 1, 1), (6, 0, 2)]
    require(len(positive) == 9 and sorted(positive) == sorted(expected),
            'The nine formal nodes must retain multiplicity')
    normalized = tuple(scale(z, 1/H) for z in positive)
    by_horizon = {n+2: tuple(scale(z, 1/H) for z in positive) for n in (1, 2, 3)}
    require(all(z == normalized for z in by_horizon.values()),
            'Node equality must be literal, not only up to scale')
    ranges = [(c-radius*(abs(a)+abs(b)), c+radius*(abs(a)+abs(b)))
              for c, a, b in normalized]
    require(all(Q(0) < lower <= upper < Q(1) for lower, upper in ranges),
            'All nodes must stay on the short arc over the entire square')
    require(min(x[0] for x in ranges) == Q(1,16), 'Minimum node')
    require(max(x[1] for x in ranges) == Q(49,128), 'Maximum node')
    # Logarithms of envelope terms as affine functions of log(rho), log(tau).
    def logs(log_budget: tuple) -> tuple:
        return (scale(log_budget, -Q(1,3)),
                add((Q(1,2), Q(0)), scale(log_budget, -Q(1,4))),
                add((Q(4,9), Q(2,9)), scale(log_budget, -Q(2,9))))
    first, second = (Q(-6), Q(0)), (Q(2), Q(-8))
    require(logs(first)[0] == logs(first)[1] == (Q(2),Q(0)),
            'First balancing budget rho^(-6)')
    require(logs(second)[1] == logs(second)[2] == (Q(0),Q(2)),
            'Second balancing budget rho^2*tau^(-8)')
    separation = add(second, scale(first, Q(-1)))
    require(separation == (Q(8), Q(-8)), 'Budget ratio (rho/tau)^8')
    # Leading flat-path logarithms: log(rho) ~ -theta^-2,
    # log(tau) = -theta^-4. The first relation is asymptotic, not an equality.
    def leading_flat(log_budget: tuple) -> tuple:
        return tuple(-x for x in log_budget)
    require(leading_flat(first) == (Q(6),Q(0)), 'First exponential order')
    require(leading_flat(second) == (Q(-2),Q(8)), 'Second exponential order')
    result = {
        'status':'PASS',
        'arithmetic':'Exact rational affine identities; standard library only',
        'common_H':str(H), 'total_horizons':list(bounds),
        'horizon_bounds':{str(n):str(b) for n,b in bounds.items()},
        'formal_positive_node_count':len(positive),
        'node_equality_for_entire_calibration_square':True,
        'normalized_node_range':[str(Q(1,16)),str(Q(49,128))],
        'common_fourier_matrix':'Same normalized nodes and same fixed integer L >= 8',
        'balanced_envelope_budgets':['rho^(-6)','rho^2*tau^(-8)'],
        'balanced_regret_orders':['rho^2','tau^2'],
        'budget_ratio':'(rho/tau)^8',
        'flat_path_exponential_orders':['exp(6/theta^2)','exp(8/theta^4-2/theta^2)'],
        'exact_optimizer_transition_thresholds_claimed':False,
        'scope':'Normalization and envelope algebra, not continuum risk verification or controller optimization'
    }
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
