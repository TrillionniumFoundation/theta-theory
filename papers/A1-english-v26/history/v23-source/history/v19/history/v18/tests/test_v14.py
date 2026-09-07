#!/usr/bin/env python3
"""Exact-rational diagnostics for the new directional-ambiguity derivation.

No compiler, legacy test helper, floating-point quadrature or random sampling
is imported. Functions are finite sums of t**a * log(t)**k. Their Lebesgue
integrals, confluent divided differences, covariance matrices and posterior
tilt identities are evaluated as fractions. This is author-added finite
algebraic evidence, not independent peer review or a formal proof.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
from math import factorial
from pathlib import Path
import json
import sys

Fun = dict[tuple[F, int], F]
COUNTS: Counter[str] = Counter()
H = F(16)
ONE: Fun = {(F(0), 0): F(1)}


def check(condition: bool, category: str) -> None:
    if not condition:
        raise AssertionError(category)
    COUNTS[category] += 1


def add(*functions: Fun) -> Fun:
    result: Fun = {}
    for function in functions:
        for key, value in function.items():
            result[key] = result.get(key, F(0)) + value
    return {key: value for key, value in result.items() if value}


def scale(function: Fun, value: F) -> Fun:
    return {key: value * coefficient for key, coefficient in function.items()
            if value * coefficient}


def mul(left: Fun, right: Fun) -> Fun:
    result: Fun = {}
    for (a, k), c in left.items():
        for (b, j), d in right.items():
            key = (a + b, k + j)
            result[key] = result.get(key, F(0)) + c * d
    return {key: value for key, value in result.items() if value}


def monomial(exponent: F) -> Fun:
    return {(exponent, 0): F(1)}


def integral(function: Fun) -> F:
    return sum((coefficient * (-1)**k * factorial(k) / (a + 1)**(k + 1)
                for (a, k), coefficient in function.items()), F(0))


@lru_cache(maxsize=None)
def divided_difference(nodes: tuple[F, ...]) -> Fun:
    nodes = tuple(sorted(nodes))
    if nodes[0] == nodes[-1]:
        k = len(nodes) - 1
        return {(H * nodes[0], k): H**k / factorial(k)}
    return scale(add(divided_difference(nodes[1:]),
                     scale(divided_difference(nodes[:-1]), F(-1))),
                 1 / (nodes[-1] - nodes[0]))


def product_fraction(values) -> F:
    result = F(1)
    for value in values:
        result *= value
    return result


def leja(nodes: list[F]):
    remaining = list(enumerate(nodes))
    first = min(remaining, key=lambda pair: (pair[1], pair[0]))
    ordered = [first]
    remaining.remove(first)
    pivots = [F(1)]
    while remaining:
        def value(pair):
            return product_fraction(abs(pair[1] - previous[1]) for previous in ordered)
        chosen = max(remaining, key=lambda pair: (value(pair), -pair[0]))
        pivots.append(value(chosen))
        ordered.append(chosen)
        remaining.remove(chosen)
    xs = [pair[1] for pair in ordered]
    matrix = [[product_fraction(x - y for y in xs[:j]) / pivots[j]
               if pivots[j] else F(0) for j in range(len(xs))] for x in xs]
    return xs, pivots, matrix


def positive_inverse(matrix: list[list[F]]) -> list[list[F]]:
    """Exact elimination; positive Schur pivots also check Sylvester positivity."""
    q = len(matrix)
    work = [row[:] + [F(i == j) for j in range(q)]
            for i, row in enumerate(matrix)]
    for j in range(q):
        pivot = work[j][j]
        check(pivot > 0, 'strict_covariance_Schur_pivot')
        work[j] = [v / pivot for v in work[j]]
        for i in range(q):
            if i != j:
                multiplier = work[i][j]
                work[i] = [a - multiplier * b for a, b in zip(work[i], work[j])]
    return [row[q:] for row in work]


def matvec(matrix, vector):
    return [sum((a * b for a, b in zip(row, vector)), F(0)) for row in matrix]


def one_case(theta: F, history_kind: str) -> dict:
    exponents = [F(1), F(2), F(2) + theta, F(3) + theta, F(4) + 2 * theta]
    nodes, pivots, L = leja([a / H for a in exponents])
    q = len(nodes)
    phi = [divided_difference(tuple(nodes[:j + 1])) for j in range(q)]
    for i, node in enumerate(nodes):
        recovered = add(*(scale(phi[j], L[i][j] * pivots[j]) for j in range(q)))
        check(recovered == monomial(H * node), 'exact_Newton_identity_including_confluence')
    check(all(pivots[j] >= pivots[j + 1] for j in range(q - 1)), 'decreasing_pivots')
    check(all(abs(v) <= 1 for row in L for v in row), 'bounded_Leja_matrix')
    volumes = []
    for ell in range(1, q + 1):
        volume = max(product_fraction(abs(a - b) for a, b in combinations(group, 2))
                     for group in combinations(nodes, ell))
        leading = product_fraction(pivots[:ell])
        check(leading <= volume <= factorial(ell) * leading, 'exterior_volume_comparison')
        volumes.append(volume)
    check((pivots[-1] == 0) == (theta == 0), 'exact_collision_zero_axis')
    check(all(v > 0 for v in pivots[:4]), 'four_separated_future_axes')

    if history_kind == 'empty':
        likelihood = ONE
    elif history_kind == 'constant_failure':
        likelihood = scale(ONE, F(1, 2))
    elif history_kind == 'nonconstant_failure':
        likelihood = add(scale(ONE, F(1, 2)), scale(monomial(F(2) + theta), F(1, 100)))
    else:
        raise ValueError('unknown history fixture')
    evidence = integral(likelihood)
    def nu(function):
        return integral(mul(likelihood, function)) / evidence
    means = [nu(function) for function in phi]
    centered = [add(function, scale(ONE, -mean)) for function, mean in zip(phi, means)]
    covariance = [[nu(mul(a, b)) for b in centered] for a in centered]
    inverse = positive_inverse(covariance)
    # Hermite--Genocchi and exp(x)>=x^k/k! give this gap-independent test bound.
    B = max((H / min(exponents))**j for j in range(q))
    C0 = max(F(1), 2 * B * sum((abs(v) for row in inverse for v in row), F(0)))
    epsilon = F(1, 5)
    s = epsilon / (4 * C0)
    vectors = [[F(sign) if j == k else F(0) for j in range(q)]
               for k in range(q) for sign in (-1, 1)] + [[F(1)] * q]
    missing_normalization_detected = False
    query_factors = [scale(ONE, F(1, 2)),
                     add(scale(ONE, F(1, 2)), scale(monomial(F(1)), F(1, 100))),
                     add(scale(ONE, F(1, 2)), scale(monomial(F(2) + theta), F(1, 100)))]
    queries = [mul(a, b) for a, b in product(query_factors, repeat=2)]
    for v in vectors:
        coefficients = matvec(inverse, v)
        f = add(*(scale(function, c) for function, c in zip(centered, coefficients)))
        check(nu(f) == 0, 'dual_posterior_mean_zero')
        for j in range(q):
            check(nu(mul(phi[j], f)) == v[j], 'simultaneous_exact_duality')
        check(abs(integral(f)) <= C0, 'prior_mean_bound')
        denominator = 1 + s * integral(f)
        prior_density = scale(add(ONE, scale(f, s)), 1 / denominator)
        check(integral(prior_density) == 1, 'pulled_back_prior_mass_one')
        check(2 * s * C0 / (1 - s * C0) <= epsilon, 'rigorous_relative_envelope_bound')
        tilted_evidence = integral(mul(likelihood, prior_density))
        def nu_prime(function):
            return integral(mul(mul(likelihood, prior_density), function)) / tilted_evidence
        for j in range(q):
            check(nu_prime(phi[j]) - means[j] == s * v[j], 'exact_posterior_coordinate_shift')
        raw_shift = [nu_prime(monomial(H * node)) - nu(monomial(H * node)) for node in nodes]
        expected = matvec(L, [s * d * vv for d, vv in zip(pivots, v)])
        for actual, wanted in zip(raw_shift, expected):
            check(actual == wanted, 'physical_raw_shift_including_zero_pivots')
        first = next((j for j in range(q) if v[j]), q)
        for j in range(first):
            check(raw_shift[j] == 0, 'exact_prefix_advice_preserved')
        if first == 4 and theta == 0:
            check(all(value == 0 for value in raw_shift), 'fifth_direction_physically_zero_at_collision')
            check(all(nu_prime(query) == nu(query) for query in queries), 'all_physical_queries_zero_tail')
        for query in queries:
            value = nu_prime(query)
            check(0 <= value <= 1, 'physical_query_probability_range')
        if integral(f) != 0:
            check(integral(add(ONE, scale(f, s))) != 1, 'omitted_prior_normalization_fault_detected')
            missing_normalization_detected = True
    if history_kind == 'nonconstant_failure':
        check(missing_normalization_detected, 'nonconstant_history_requires_prior_normalization')
    else:
        check(not missing_normalization_detected, 'constant_history_normalization_special_case')
    if theta == 0:
        check(volumes[-1] == 0, 'zero_final_exterior_volume')
    return {'theta': str(theta), 'history': history_kind,
            'pivots': [str(v) for v in pivots],
            'last_pivot_over_abs_theta': str(pivots[-1] / abs(theta)) if theta else None,
            'tested_dual_vectors': len(vectors),
            'prior_normalization_fault_detected': missing_normalization_detected}


def main() -> None:
    thetas = [F(-1, 10), F(-1, 100), F(-1, 10000), F(0), F(1, 10000), F(1, 100), F(1, 10)]
    rows = [one_case(theta, kind) for theta in thetas
            for kind in ('empty', 'constant_failure', 'nonconstant_failure')]
    report = {'status': 'passed', 'arithmetic': 'exact fractions', 'assertions': sum(COUNTS.values()),
              'categories': dict(COUNTS), 'cases': rows,
              'scope': 'Finite algebraic diagnostics of complete confluence, bounded-dual construction, prior normalization and all raw/query shifts. Not a proof certificate, continuum enumeration or independent referee judgment.'}
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parents[1] / 'validation/V14_DIRECTIONAL_DIAGNOSTICS.json'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': report['status'], 'assertions': report['assertions'], 'cases': len(rows), 'categories': report['categories']}, indent=2))


if __name__ == '__main__':
    main()
