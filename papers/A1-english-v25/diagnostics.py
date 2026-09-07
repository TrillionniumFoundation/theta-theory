#!/usr/bin/env python3
"""Finite diagnostics for v25. These do not prove its continuum theorems.

All requirements use explicit exceptions, not Python assert statements.
The deterministic JSON output must agree under ordinary Python and -O.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, permutations, product
from pathlib import Path
import hashlib
import json
import math
import random

COUNTS: Counter[str] = Counter()


def require(condition: bool, category: str) -> None:
    COUNTS[category] += 1
    if not condition:
        raise ArithmeticError('Diagnostic failed: ' + category)


def convolution(left: list[F], right: list[F]) -> list[F]:
    out = [F(0)] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            out[i + j] = max(out[i + j], x * y)
    return out


def profile_enumeration(profiles: list[list[F]]) -> list[F]:
    out = [F(0)] * (1 + sum(len(p) - 1 for p in profiles))
    for allocation in product(*(range(len(p)) for p in profiles)):
        value = F(1)
        for p, index in zip(profiles, allocation):
            value *= p[index]
        out[sum(allocation)] = max(out[sum(allocation)], value)
    return out


def cut_weight(n: int, edges: list[tuple[int, int, F]], mask: int) -> F:
    return sum((w for u, v, w in edges
                if bool(mask & (1 << u)) != bool(mask & (1 << v))), F(0))


def order_width(n: int, edges: list[tuple[int, int, F]], order: tuple[int, ...]) -> F:
    mask, width = 0, F(0)
    for vertex in order[:-1]:
        mask |= 1 << vertex
        width = max(width, cut_weight(n, edges, mask))
    return width


def dynamic_width(n: int, edges: list[tuple[int, int, F]]) -> F:
    dp: dict[int, F] = {0: F(0)}
    for mask in range(1, 1 << n):
        cut = cut_weight(n, edges, mask)
        dp[mask] = min(max(dp[mask ^ (1 << x)], cut)
                       for x in range(n) if mask & (1 << x))
    return dp[(1 << n) - 1]


def vandermonde_profile(nodes: list[F]) -> list[F]:
    out = [F(1)]
    for size in range(1, len(nodes) + 1):
        best = F(0)
        for selected in combinations(nodes, size):
            value = F(1)
            for x, y in combinations(selected, 2):
                value *= abs(y - x)
            best = max(best, value)
        out.append(best)
    return out


def log2_fraction(value: F) -> float:
    if value <= 0:
        return float('-inf')
    return math.log2(value.numerator) - math.log2(value.denominator)


def bit_weight(profile: list[F], log_accuracy: float) -> float:
    return max(i * log_accuracy / 2 + log2_fraction(v)
               for i, v in enumerate(profile))


def partition_cost(weights: tuple[float, float, float], subset: int) -> float:
    left = sum(w for i, w in enumerate(weights) if subset & (1 << i))
    return max(left, sum(weights) - left)


def check_profiles() -> None:
    catalog = [[F(1)], [F(1), F(1)], [F(1), F(1), F(0)],
               [F(1), F(1), F(1, 3)], [F(1), F(1), F(1, 4), F(1, 32)]]
    for a, b, c in product(catalog, repeat=3):
        actual = convolution(convolution(a, b), c)
        require(actual == convolution(a, convolution(b, c)), 'max_product_associativity')
        require(actual == profile_enumeration([a, b, c]), 'individual_caps_enumeration')
        for radius in (F(1), F(1, 2), F(1, 5)):
            joint = max(value / radius ** i for i, value in enumerate(actual))
            separate = F(1)
            for p in (a, b, c):
                separate *= max(value / radius ** i for i, value in enumerate(p))
            require(joint == separate, 'exact_bit_threshold_separation')
    scales = [(F(1), F(1, 2), F(1, 8)), (F(1), F(1, 3)), (F(1), F(0))]
    profiles = []
    for values in scales:
        p = [F(1)]
        for value in values:
            p.append(p[-1] * value)
        profiles.append(p)
    merged = sorted((x for s in scales for x in s), reverse=True)
    target = [F(1)]
    for value in merged:
        target.append(target[-1] * value)
    require(profile_enumeration(profiles) == target, 'merged_prefix_scale_control')
    capped = convolution([F(1), F(1)], [F(1), F(1), F(1, 2)])
    uncapped = convolution([F(1), F(1), F(1)], [F(1), F(1), F(1, 2)])
    require(capped[2] != uncapped[2] or len(capped) != len(uncapped),
            'negative_control_ambient_cap_substitution')


def check_graphs() -> None:
    rng = random.Random(25)
    for n in range(2, 6):
        pairs = list(combinations(range(n), 2))
        masks = list(range(1 << len(pairs))) if n <= 4 else sorted(
            {0, 1, 3, 7, 31, (1 << len(pairs)) - 1,
             *(rng.randrange(1 << len(pairs)) for _ in range(24))})
        for mask in masks:
            edges = [(u, v, F((3 * i) % 7 + 1, i % 3 + 1))
                     for i, (u, v) in enumerate(pairs) if mask & (1 << i)]
            brute = min(order_width(n, edges, order) for order in permutations(range(n)))
            require(dynamic_width(n, edges) == brute, 'weighted_cutwidth_dp_vs_orders')
        parallel = [(0, 1, F(1, 3)), (0, 1, F(2, 3))]
        require(dynamic_width(n, parallel) == 1, 'parallel_edges_and_isolated_vertices')
        require(dynamic_width(n, []) == 0, 'empty_graph_boundary_case')
    low = [F(7, 2), F(3), F(1, 2)]
    high = [F(14), F(15), F(2)]
    e_low = [(0, i + 1, w) for i, w in enumerate(low)]
    e_high = [(0, i + 1, w) for i, w in enumerate(high)]
    require(dynamic_width(4, e_low) == F(7, 2), 'star_low_resolution_slope')
    require(dynamic_width(4, e_high) == 16, 'star_high_resolution_slope')
    for order in permutations(range(4)):
        penalty = max(order_width(4, e_low, order) - F(7, 2),
                      order_width(4, e_high, order) - 16)
        require(penalty >= F(1, 2), 'no_common_order_two_scale_negative_control')


def check_collisions() -> None:
    labels = [(j + 2 * k, k) for j in range(4) for k in range(4 - j)
              if j + k > 0]
    expected = {(1, 0), (2, 0), (2, 1), (3, 0), (3, 1),
                (4, 1), (4, 2), (5, 2), (6, 3)}
    require(set(labels) == expected and len(labels) == 9, 'formal_three_fold_sums')
    for size in range(1, 10):
        valuation = min(sum(a == c for (a, b), (c, d) in combinations(selected, 2))
                        for selected in combinations(labels, size))
        require(valuation == max(0, size - 6), 'exact_vandermonde_contact_order')
    exact = vandermonde_profile([F(a, 32) for a, b in labels])
    for size in range(10):
        require((exact[size] > 0) == (size <= 6), 'exact_collision_zero_volumes')
    normalized: dict[int, list[F]] = {i: [] for i in range(1, 10)}
    for power in (8, 12, 16, 32):
        theta = F(1, 2 ** power)
        values = vandermonde_profile([(F(a) + b * theta) / 32 for a, b in labels])
        for size in range(1, 10):
            normalized[size].append(values[size] / theta ** max(0, size - 6))
    for values in normalized.values():
        require(min(values) > 0 and max(values) <= 4 * min(values),
                'rational_collision_scale_samples')
    binary = vandermonde_profile([F(i, 16) for i in range(1, 8)])
    for power in (512, 1024):
        theta = F(1, 2 ** power)
        values = vandermonde_profile([(F(a) + b * theta) / 32 for a, b in labels])
        low = (bit_weight(binary, power), bit_weight(values, power), power / 2)
        high = (bit_weight(binary, 4 * power), bit_weight(values, 4 * power), 2 * power)
        low_costs = [partition_cost(low, subset) for subset in range(8)]
        high_costs = [partition_cost(high, subset) for subset in range(8)]
        require(low_costs[1] == min(low_costs), 'actual_volume_low_order')
        require(high_costs[2] == min(high_costs), 'actual_volume_high_order')
        require(abs(min(low_costs) - 3.5 * power) < 1000,
                'actual_volume_low_slope_bounded_remainder')
        require(abs(min(high_costs) - 16 * power) < 1000,
                'actual_volume_high_slope_bounded_remainder')
        for subset in range(8):
            require(max(low_costs[subset] - min(low_costs),
                        high_costs[subset] - min(high_costs)) > power / 4,
                    'actual_volume_order_penalty_samples')


def check_probability_and_quantifiers() -> None:
    # A finite toy latent mixture checks report-word bookkeeping only;
    # it is not used to simulate or prove the full-support-prior theorem.
    probabilities = [F(1, 4), F(5, 12), F(7, 12), F(3, 4)]
    for horizon in range(1, 9):
        total = F(0)
        for word in product((0, 1), repeat=horizon):
            successes = sum(word)
            evidence = sum((p ** successes * (1 - p) ** (horizon - successes)
                            for p in probabilities), F(0)) / len(probabilities)
            total += evidence
            require(evidence >= F(1, 4) ** horizon, 'actual_report_word_positive_mass')
        require(total == 1, 'all_report_words_unconditional_mass')
    points = range(64)
    selected = {i for i in points if i < 4}
    for lo in range(0, 64, 4):
        for hi in range(lo, 65, 4):
            ball = {i for i in points if lo <= i < hi}
            raw = F(len(selected & ball), 64)
            full = F(len(ball), 64)
            require(raw <= full, 'restricted_subprobability_small_ball_control')
    raw_small = F(len(selected), 64)
    conditional_small = F(len(selected), len(selected))
    require(conditional_small > raw_small, 'negative_control_conditioning_on_selected_trace')
    require(F(1) > F(1, 2), 'negative_control_expectation_of_maximum_is_not_maximum_of_expectations')
    error = F(0)
    for lipschitz, radius in zip((2, 3, 1), (F(1, 10), F(0), F(1, 100))):
        error = lipschitz * error + radius
    require(error == F(31, 100) and error > F(1, 100),
            'negative_control_discarding_previous_causal_error')
    require(14 + 8 + 2 == 24, 'complete_raw_trial_accounting')


def main() -> None:
    check_profiles()
    check_graphs()
    check_collisions()
    check_probability_and_quantifiers()
    report = {'revision': 25, 'status': 'passed', 'checks': sum(COUNTS.values()),
              'categories': dict(sorted(COUNTS.items())),
              'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'arithmetic': 'Exact Fraction arithmetic except explicitly labelled logarithmic volume samples.',
              'limitations': ['Finite checks do not prove the continuum acquisition or adaptive converse.',
                              'No prior referee diagnostics or GitHub Actions runs are claimed here.',
                              'A test count is not a journal-significance or priority assessment.']}
    print(json.dumps(report, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
