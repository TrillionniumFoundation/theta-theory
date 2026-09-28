#!/usr/bin/env python3
"""Exact finite diagnostics for the A2 v30 referee report.

These checks do NOT prove measurable-kernel existence, continuum estimates,
half-line convergence, statistical limit theorems, or whole-paper correctness.
They test finite analogues and explicit regression examples without third-party
packages. Checks use explicit exceptions and remain enabled under python -O.
"""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import sys

ZERO = F(0)
ONE = F(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def tv(p: dict, q: dict) -> F:
    return sum((abs(p.get(x, ZERO) - q.get(x, ZERO))
                for x in p.keys() | q.keys()), ZERO) / 2


def push(p: dict, mapping) -> dict:
    out = defaultdict(F)
    for x, value in p.items():
        out[mapping(x)] += value
    return dict(out)


def coupling(p: tuple[F, ...], q: tuple[F, ...]) -> list[list[F]]:
    require(len(p) == len(q) and sum(p) == sum(q) == 1,
            'Invalid finite probability vectors')
    require(min(p + q) >= 0, 'Negative probability')
    h = tuple(min(x, y) for x, y in zip(p, q))
    m = sum(h)
    n = len(p)
    return [[(h[i] if i == j else ZERO) +
             ((p[i] - h[i]) * (q[j] - h[j]) / (1 - m)
              if m < 1 else ZERO)
             for j in range(n)] for i in range(n)]


def check_couplings() -> dict:
    vectors = [tuple(F(i, 4) for i in v)
               for v in product(range(5), repeat=4) if sum(v) == 4]
    m_zero = m_one = 0
    for p, q in product(vectors, repeat=2):
        c = coupling(p, q)
        overlap = sum(min(a, b) for a, b in zip(p, q))
        m_zero += overlap == 0
        m_one += overlap == 1
        require(sum(map(sum, c)) == 1, 'Coupling mass')
        require(all(x >= 0 for row in c for x in row), 'Coupling positivity')
        require(tuple(map(sum, c)) == p, 'First coupling marginal')
        require(tuple(sum(c[i][j] for i in range(4)) for j in range(4)) == q,
                'Second coupling marginal')
        disagree = sum(c[i][j] for i in range(4) for j in range(4) if i != j)
        pd, qd = dict(enumerate(p)), dict(enumerate(q))
        require(disagree == tv(pd, qd) == 1 - overlap, 'Maximality')
        for theta in (-2, 0, 3):
            embedding = lambda i: ('failure',) if i == 0 else (i, theta * i * i)
            require(tv(push(pd, embedding), push(qd, embedding)) == disagree,
                    'Injective physical pushforward')
        require(tv(push(pd, lambda i: i % 2), push(qd, lambda i: i % 2))
                <= disagree, 'Noninjective contraction')

    # Equality must not be asserted after a noninjective observation map.
    p, q = {0: ONE}, {1: ONE}
    require(tv(p, q) == 1 and tv(push(p, lambda _: 0), push(q, lambda _: 0)) == 0,
            'Noninjective equality counterexample')
    # The same scalar law can have disjoint images at different parameters.
    scalar = {1: F(1, 2), 2: F(1, 2)}
    flat = push(scalar, lambda i: (i, 0))
    curved = push(scalar, lambda i: (i, i * i))
    require(tv(flat, curved) == 1, 'Cross-parameter comparison guard')
    return {'probability_vectors': len(vectors), 'ordered_pairs': len(vectors)**2,
            'overlap_zero_pairs': m_zero, 'overlap_one_pairs': m_one,
            'injective_embeddings_per_pair': 3,
            'noninjective_equality_counterexample': {'before': '1', 'after': '0'},
            'cross_parameter_same_scalar_law_physical_tv': '1'}


TAU = F(1, 2)
FLIGHTS = (2, 4, 6)
SUCCESS = (F(1, 5), F(1, 9), F(1, 17))
P = tuple((1 - p, p / 3, 2 * p / 3) for p in SUCCESS)
Q = []
for p, j in zip(SUCCESS, FLIGHTS):
    eta = TAU**j
    q = p * (1 + eta / 8)
    left = F(1, 3) + eta / 2
    Q.append((1 - q, q * left, q * (1 - left)))
Q = tuple(Q)
ERROR = tuple(tv(dict(enumerate(p)), dict(enumerate(q))) for p, q in zip(P, Q))
for a in range(3):
    require(ERROR[a] <= SUCCESS[a] * TAU**FLIGHTS[a], 'One-step weighted budget')


def transcript_law(kernels: tuple, cap: int, kth: int, selector: int) -> dict:
    """Retains seed, every chosen design/outcome, and terminal preparation count."""
    out = defaultdict(F)

    def visit(seed: int, history: tuple, mass: F) -> None:
        successes = sum(y != 0 for _, y in history)
        failures = len(history) - successes
        early_stop = (selector == 1 and len(history) >= 3 and failures >= 2
                      and history[-1][1] == 2)
        if len(history) == cap or successes == kth or early_stop:
            out[(seed, history, len(history))] += mass
            return
        last = history[-1][1] if history else 0
        a = ((seed + last + len(history)) % 3 if selector == 0
             else (seed + 2 * last + failures) % 3)
        for outcome, prob in enumerate(kernels[a]):
            if prob:
                visit(seed, history + ((a, outcome),), mass * prob)

    for seed in (0, 1):
        visit(seed, (), F(1, 2))
    require(sum(out.values()) == 1, 'Stopped law normalization')
    return dict(out)


def expectation(law: dict, statistic) -> F:
    return sum((p * statistic(x) for x, p in law.items()), ZERO)


def check_adaptive() -> dict:
    cases = 0
    max_ratio = ZERO
    representative = None
    for cap, kth, selector in product(range(1, 7), range(1, 4), range(2)):
        lp = transcript_law(P, cap, kth, selector)
        lq = transcript_law(Q, cap, kth, selector)
        distance = tv(lp, lq)
        error_sum = lambda x: sum((ERROR[a] for a, _ in x[1]), ZERO)
        bp = expectation(lp, error_sum)
        bq = expectation(lq, error_sum)
        require(distance <= min(ONE, bp, bq), 'Stopped coupling bound')
        predicted = expectation(lp, lambda x: sum(
            (SUCCESS[a] * TAU**FLIGHTS[a] for a, _ in x[1]), ZERO))
        realized = expectation(lp, lambda x: sum(
            (TAU**FLIGHTS[a] for a, y in x[1] if y != 0), ZERO))
        require(predicted == realized, 'Predictable success identity')
        require(bp <= realized <= kth * TAU**min(FLIGHTS), 'Kth-success budget')
        require(all(sum(y != 0 for _, y in x[1]) <= kth for x in lp),
                'Pathwise success cap')
        cost = expectation(lp, lambda x: F(x[2]))
        nsuccess = expectation(lp, lambda x: F(sum(y != 0 for _, y in x[1])))
        require(cost >= nsuccess, 'Failures must remain charged')
        coarsen = lambda x: tuple(y for _, y in x[1] if y != 0)
        coarse_distance = tv(push(lp, coarsen), push(lq, coarsen))
        require(coarse_distance <= distance, 'Stopped output contraction')
        max_ratio = max(max_ratio, distance / min(bp, bq))
        cases += 1
        if (cap, kth, selector) == (6, 2, 1):
            representative = {
                'cap': cap, 'success_cap': kth, 'policy': selector,
                'physical_transcripts': len(lp), 'boundary_transcripts': len(lq),
                'tv': str(distance), 'expected_error_physical': str(bp),
                'expected_error_boundary': str(bq),
                'expected_success_weight': str(realized),
                'expected_preparation_cost': str(cost),
                'expected_successes': str(nsuccess),
                'coarsened_tv': str(coarse_distance)}

    # An exact retained pilot with an arbitrary bad-pilot continuation.
    cap, kth, selector = 5, 2, 1
    lp = transcript_law(P, cap, kth, selector)
    lq = transcript_law(Q, cap, kth, selector)
    bad_q = transcript_law(((ONE, ZERO, ZERO),) * 3, cap, kth, selector)
    eta0 = F(1, 7)
    pilot_p, pilot_q = {}, {}
    for x, mass in lp.items():
        pilot_p[('good', x)] = (1 - eta0) * mass
        pilot_p[('bad', x)] = eta0 * mass
    for x, mass in lq.items():
        pilot_q[('good', x)] = (1 - eta0) * mass
    for x, mass in bad_q.items():
        pilot_q[('bad', x)] = eta0 * mass
    good_error = expectation(lp, lambda x: sum((ERROR[a] for a, _ in x[1]), ZERO))
    pilot_distance = tv(pilot_p, pilot_q)
    require(pilot_distance <= eta0 + (1 - eta0) * good_error,
            'Good-pilot/bad-pilot bound')
    # Deleting an old observation does not delete information in a chosen design.
    # First record r selects the next design a=r; the later mark is constant.
    info_p = {(0, 0, 'constant'): F(3, 4), (1, 1, 'constant'): F(1, 4)}
    info_q = {(0, 0, 'constant'): F(1, 4), (1, 1, 'constant'): F(3, 4)}
    design_kept = lambda x: (x[1], x[2])
    only_later_mark = lambda x: x[2]
    require(tv(push(info_p, design_kept), push(info_q, design_kept)) == F(1, 2),
            'Deleted first record remains encoded in the retained design')
    require(tv(push(info_p, only_later_mark), push(info_q, only_later_mark)) == 0,
            'Different output map deletes the adaptive design information')
    return {'cases': cases, 'largest_tv_to_min_expected_error_ratio': str(max_ratio),
            'representative': representative,
            'pilot': {'bad_probability': str(eta0), 'tv': str(pilot_distance),
                      'bound': str(eta0 + (1 - eta0) * good_error)},
            'one_step_errors': [str(x) for x in ERROR],
            'adaptive_design_information_guard': {'design_retained_tv': '1/2',
                                                 'design_deleted_tv': '0'}}


def check_anchor_regression() -> dict:
    a, zeta, D = F(1, 4), F(1, 100), F(1, 225)
    h = 2 * zeta * a**3 * F(224, 225)
    wrong_left, wrong_right = D + h, D**2 / (D - h)
    require(wrong_left == F(107, 22500) and wrong_right == F(4, 837),
            'Old fixed-anchor witness values')
    require(wrong_left - wrong_right == F(-49, 2092500), 'Old witness difference')

    checks = 0
    for zeta in (F(-1, 100), F(1, 100)):
        def f(u: F, v: F) -> F:
            return (1 - u*u - v*v) * (1 + zeta*u*v*(u+v) + zeta*(u-2*v))
        def fr(u: F, v: F) -> F:
            return f(-u, -v)
        def ratio(density, u: F, v: F) -> F:
            return density(u, v)*density(ZERO, ZERO)/(density(u, ZERO)*density(ZERO, v))
        for alpha in (a, -a):
            require(1-ratio(f, alpha, alpha) > 0, 'Anchor radical positive')
            require(1-ratio(fr, -alpha, -alpha) == 1-ratio(f, alpha, alpha),
                    'Transported anchor radicand')
            for u in (F(i, 8) for i in range(-2, 3)):
                require(1-ratio(fr, u, -alpha) == 1-ratio(f, -u, alpha),
                        'Transported reconstruction numerator')
                require(fr(u, ZERO)/fr(ZERO, ZERO) == f(-u, ZERO)/f(ZERO, ZERO),
                        'Transported amplitude axis ratio')
                checks += 1
    return {'transported_slice_cases': checks,
            'fixed_anchor_squared_outputs': [str(wrong_left), str(wrong_right)],
            'fixed_anchor_difference': str(wrong_left - wrong_right)}


def main() -> None:
    result = {
        'source_commit': '46f4b1dc2f9609963cae6a80b3a0f458d88250e1',
        'python': sys.version.split()[0],
        'script_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'couplings': check_couplings(),
        'adaptive': check_adaptive(),
        'anchor_regression': check_anchor_regression(),
        'status': 'PASS',
        'limitations': [
            'Finite exact checks, not continuum measurable-kernel proofs.',
            'Finite probability vectors and policies are not physical billiard simulations.',
            'No whole-manuscript build, asymptotic theorem, or global rigidity certification.'
        ]}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
