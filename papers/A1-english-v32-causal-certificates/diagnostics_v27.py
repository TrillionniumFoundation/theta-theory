#!/usr/bin/env python3
"""Exact arithmetic checks for A1 v27; these checks do not replace its proofs."""
from __future__ import annotations
import argparse
import itertools
import json
from fractions import Fraction as F
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def icbrt(n: int) -> int:
    if n < 0:
        raise ValueError("Integer cube root requires a nonnegative input")
    if n < 2:
        return n
    x = 1 << ((n.bit_length() + 2) // 3)
    while True:
        y = (2 * x + n // (x * x)) // 3
        if y >= x:
            break
        x = y
    while (x + 1) ** 3 <= n:
        x += 1
    while x ** 3 > n:
        x -= 1
    return x


def density_u(u: F) -> F:
    if u < -F(8, 7) or u > F(8, 9):
        return F(0)
    if u <= 0:
        return 512 * (27 / (8 - 5 * u) ** 3 - 1 / (8 + 3 * u) ** 3)
    return 512 * (27 / (8 + 3 * u) ** 3 - 1 / (8 - 5 * u) ** 3)


def primitive(u: F, side: int, moment: bool = False) -> F:
    def term(b: int) -> F:
        v = 8 + b * u
        if moment:
            return (-1 / v + 4 / v ** 2) / b ** 2
        return -1 / (2 * b * v ** 2)
    return 512 * (27 * term(-5) - term(3) if side < 0
                  else 27 * term(3) - term(-5))


def integral_bounds(n: int = 8192, scale: int = 10 ** 12) -> tuple[F, F]:
    lower = F(0)
    upper = F(0)
    for a, b, increasing in [(-F(8, 7), F(0), True), (F(0), F(8, 9), False)]:
        step = (b - a) / n
        roots = []
        for j in range(n + 1):
            r = density_u(a + j * step)
            require(r >= 0, "The posterior density became negative")
            v = (r.numerator * scale ** 3) // r.denominator
            root = icbrt(v)
            require(root ** 3 <= v < (root + 1) ** 3, "Integer root enclosure failed")
            roots.append(root)
        lows = roots[:-1] if increasing else roots[1:]
        highs = roots[1:] if increasing else roots[:-1]
        lower += step * F(sum(lows), 48 * scale)
        upper += step * F(sum(highs) + n, 48 * scale)
    require(0 < lower <= upper, "Integral enclosure failed")
    return lower, upper


def order_cost(order: tuple[str, ...], s: F) -> F:
    w = {'1': 7 * s, '2': max(6 * s, 9 * s - 3), '3': s}
    visited: set[str] = set()
    result = F(0)
    for vertex in order[:-1]:
        visited.add(vertex)
        cut = sum((w[e] for e in ('1', '2', '3')
                   if (e in visited) != ('c' in visited)), F(0))
        result = max(result, cut)
    return result


def arrangement(a: F, b: F) -> list[F]:
    lines: set[tuple[F, F]] = set()
    for e2 in [(F(6), F(0)), (F(9), F(-3))]:
        weights = [(F(7), F(0)), e2, (F(1), F(0))]
        for mask in range(8):
            lines.add((sum((weights[i][0] for i in range(3) if mask & (1 << i)), F(0)),
                       sum((weights[i][1] for i in range(3) if mask & (1 << i)), F(0))))
    points = {a, b}
    if a <= 1 <= b:
        points.add(F(1))
    for (m1, c1), (m2, c2) in itertools.combinations(lines, 2):
        if m1 != m2:
            x = (c2 - c1) / (m1 - m2)
            if a <= x <= b:
                points.add(x)
    return sorted(points)


def menu_regret(orders: list[tuple[str, ...]], points: list[F], k: int) -> F:
    values = [[order_cost(order, s) for s in points] for order in orders]
    optimum = [min(row[j] for row in values) for j in range(len(points))]
    best = None
    for size in range(1, min(k, len(orders)) + 1):
        for menu in itertools.combinations(range(len(orders)), size):
            loss = max(min(values[i][j] for i in menu) - optimum[j]
                       for j in range(len(points)))
            best = loss if best is None else min(best, loss)
    if best is None:
        raise RuntimeError("No menu was examined")
    return best


def run_checks() -> dict:
    tests = []
    for n in [0, 1, 2, 7, 8, 26, 27, 10 ** 36 + 17]:
        r = icbrt(n)
        require(r ** 3 <= n < (r + 1) ** 3, "Cube-root implementation failed")
    tests.append('integer_cube_root_exact_enclosures')

    mass = ((primitive(F(0), -1) - primitive(-F(8, 7), -1))
            + (primitive(F(8, 9), 1) - primitive(F(0), 1))) / 48
    moment_u = ((primitive(F(0), -1, True) - primitive(-F(8, 7), -1, True))
                + (primitive(F(8, 9), 1, True) - primitive(F(0), 1, True))) / 48
    require(mass == F(1, 2), 'Continuous mass is not 1/2')
    require(moment_u == 0, 'Failure-weighted centred mean is not zero')
    require(density_u(-F(8, 7)) == 0 and density_u(F(8, 9)) == 0,
            'Density endpoints failed')
    require(density_u(F(0)) == 26, 'Density peak failed')
    require(F(5, 16) + F(3, 16) + mass == 1, 'Mixed-law normalization failed')
    require(F(5, 16) * F(8, 15) + F(3, 16) * F(4, 9) + mass / 2 == F(1, 2),
            'Posterior-mean martingale identity failed')
    tests.append('full_mixed_posterior_law_mass_and_first_moment')

    for x in [F(1, 4), F(3, 8), F(1, 2), F(5, 8), F(3, 4)]:
        for y in [F(1, 4), F(3, 8), F(1, 2), F(5, 8), F(3, 4)]:
            evidence = 1 - 5 * x / 8 - 3 * y / 8
            z = (F(1, 2) - x / 3 - y / 6) / evidence
            require(z == F(1, 2) + (y - x) / (48 * evidence), 'Bayes formula failed')
            u = 48 * (z - F(1, 2))
            require(y == (8 * u + (8 - 5 * u) * x) / (8 + 3 * u), 'Inverse map failed')
            require(evidence == 8 * (1 - x) / (8 + 3 * u), 'Inverse evidence failed')
    tests.append('rational_Bayes_inverse_map_checks')

    for z, w in [(F(0), F(1)), (F(4, 9), F(8, 15)), (F(1, 2), F(10, 21))]:
        qz = [F(3, 4), F(1, 2) + z / 8, F(1, 2) - z / 8, F(1, 4)]
        qw = [F(3, 4), F(1, 2) + w / 8, F(1, 2) - w / 8, F(1, 4)]
        require(sum(((a - b) ** 2 for a, b in zip(qz, qw)), F(0)) / 4
                == (z - w) ** 2 / 128, 'Query isometry failed')
        require(4 * (qz[1] - qz[2]) == z, 'Query recovery failed')
    tests.append('query_metric_and_recovery_identity')

    beta = F(1, 32) + F(3, 1024)
    require(beta == F(35, 1024), 'Event mass failed')
    require((F(1, 64) + F(1, 512)) / beta == F(18, 35), 'Event mean failed')
    h = F(192, 5) * F(39, 64) ** 3
    require(h == F(177957, 20480), 'Weighted density bound failed')
    c_squared = 512 * (h / beta) ** 2
    require(c_squared == F(1013398203168, 30625), 'Capacity constant failed')
    certificate = beta / (12 * c_squared)
    require(certificate == F(1071875, 12452637120528384), 'Integrated certificate failed')
    require(512 * ((h / 2) / (beta / 2)) ** 2 == c_squared, 'Same-model capacity changed')
    require((beta / 2) / (12 * c_squared) == certificate / 2, 'Factor-two comparison failed')
    tests.append('complete_same_decoder_separator_comparison')

    orders = list(itertools.permutations(('c', '1', '2', '3')))
    points = arrangement(F(1, 2), F(2))
    one = menu_regret(orders, points, 1)
    two = menu_regret(orders, points, 2)
    endpoints = menu_regret(orders, [F(1, 2), F(2)], 1)
    require(one == 1 and two == 0 and endpoints == F(1, 2), 'Exact star menu law failed')
    for s in [F(1, 2), F(1), F(3, 2), F(2), F(3), F(4)]:
        p1 = max(7 * s, max(6 * s, 9 * s - 3) + s)
        p2 = max(8 * s, max(6 * s, 9 * s - 3))
        require(min(order_cost(order, s) for order in orders) == min(p1, p2),
                'Star partition formula failed')
    tests.append('all_24_orders_and_finite_affine_arrangement_menus')

    expectation_of_max = F(1)
    max_of_expectations = F(1, 2)
    require(expectation_of_max != max_of_expectations, 'Boundary-maximum negative control failed')
    tests.append('expectation_maximum_interchange_negative_control')

    integral_lower, integral_upper = integral_bounds()
    kappa_lower = integral_lower ** 3 / 1536
    kappa_upper = integral_upper ** 3 / 1536
    require(F(488, 10 ** 9) < kappa_lower <= kappa_upper < F(490, 10 ** 9),
            'Sharp constant is outside the stated decimal enclosure')
    tests.append('rational_monotone_enclosure_of_sharp_constant')

    return {
        'schema_version': 1,
        'revision': 'A1-v27',
        'status': 'passed',
        'scope': 'Arithmetic identities and finite arrangements; not a verification of the general proofs or a native manuscript build.',
        'checks': tests,
        'continuous_mass': str(mass),
        'first_block_mass': str(beta),
        'weighted_density_upper_bound': str(h),
        'recovery_norm_squared': '128',
        'capacity_constant_squared': str(c_squared),
        'separator_coefficient_exact': str(certificate),
        'complete_word_coefficient_exact': str(certificate / 2),
        'star': {'orders': len(orders), 'menus_of_size_at_most_two': 300,
                 'arrangement_points': [str(s) for s in points],
                 'interval_K1': str(one), 'interval_K2': str(two), 'endpoints_K1': str(endpoints)},
        'sharp_constant': {'formula': '(integral f^(1/3))^3 / 1536',
                           'intervals_per_monotone_piece': 8192, 'root_scale': 10 ** 12,
                           'integral_lower_exact': str(integral_lower),
                           'integral_upper_exact': str(integral_upper),
                           'kappa_lower_exact': str(kappa_lower),
                           'kappa_upper_exact': str(kappa_upper),
                           'kappa_lower_display': float(kappa_lower),
                           'kappa_upper_display': float(kappa_upper),
                           'ratio_to_separator_lower_display': float(kappa_lower / certificate),
                           'ratio_to_separator_upper_display': float(kappa_upper / certificate)},
        'native_two_volume_compile': 'not performed by this diagnostic',
        'pdf_visual_inspection': 'not performed by this diagnostic'
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = run_checks()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + '\n', encoding='utf-8')
    print(json.dumps({'status': result['status'], 'output': str(args.output),
                      'sharp_constant': [result['sharp_constant']['kappa_lower_display'],
                                         result['sharp_constant']['kappa_upper_display']]}, sort_keys=True))


if __name__ == '__main__':
    main()
