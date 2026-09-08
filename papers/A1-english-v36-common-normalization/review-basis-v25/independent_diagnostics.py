#!/usr/bin/env python3
"""Independent finite diagnostics for the A1 v25 referee assessment.

Designed after reading the submission; imports no author implementation.
Uses exact Fraction arithmetic, explicit exceptions, and deterministic output.
It does not prove the continuum theorem or certify the manuscript build.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement, permutations, product
from pathlib import Path
from math import factorial
import hashlib
import json

COUNTS = Counter()
WITNESSES = {}


def check(ok, category):
    COUNTS[category] += 1
    if not ok:
        raise ArithmeticError(category)


def mul(values):
    out = F(1)
    for value in values:
        out *= value
    return out


def allocated_profiles(profiles):
    best = [F(0)] * (1 + sum(len(p) - 1 for p in profiles))
    for indices in product(*(range(len(p)) for p in profiles)):
        k = sum(indices)
        best[k] = max(best[k], mul(p[i] for p, i in zip(profiles, indices)))
    return best


def profile_tests():
    catalog = ((F(1),), (F(1), F(1)), (F(1), F(1), F(0)),
               (F(1), F(1), F(1, 5)), (F(1), F(1), F(1, 4), F(1, 40)))
    for profiles in product(catalog, repeat=3):
        combined = allocated_profiles(profiles)
        for radius in (F(1), F(1, 2), F(1, 3), F(1, 8)):
            separated = mul(max(v / radius**i for i, v in enumerate(p)) for p in profiles)
            joined = max(v / radius**k for k, v in enumerate(combined))
            check(separated == joined, 'capped_profile_threshold_factorization')
            for budget in (1, 2, 3, 4, 8, 17, 32):
                # Equivalent to max_k(A_k/M)^(2/k) <= radius^2; no roots used.
                inequalities = all(v <= budget * radius**k
                                   for k, v in enumerate(combined) if k)
                check(inequalities == (F(budget) >= separated),
                      'all_integer_budget_inverse_witnesses')
    capped = allocated_profiles(((F(1), F(1)), (F(1), F(1), F(1, 16))))
    wrong = allocated_profiles(((F(1), F(1), F(1)), (F(1), F(1))))
    check(capped[3] == F(1, 16) and wrong[3] == 1,
          'negative_control_redistributing_an_individual_cap')
    WITNESSES['cap_violation_at_same_total_cap'] = {
        'correct_A3': str(capped[3]), 'wrong_A3': str(wrong[3])}


def crossing(order, edges):
    visited = set()
    loads = []
    for vertex in order[:-1]:
        visited.add(vertex)
        loads.append(sum((w for u, v, w in edges if (u in visited) != (v in visited)), F(0)))
    return max(loads, default=F(0))


def subset_dp(n, edges):
    costs = {0: F(0)}
    for size in range(1, n + 1):
        for chosen in combinations(range(n), size):
            mask = sum(1 << x for x in chosen)
            load = sum((w for u, v, w in edges if bool(mask & (1 << u)) != bool(mask & (1 << v))), F(0))
            costs[mask] = min(max(costs[mask ^ (1 << x)], load) for x in chosen)
    return costs[(1 << n) - 1]


def graph_tests():
    for n in (2, 3, 4):
        pairs = list(combinations(range(n), 2))
        for mask in range(1 << len(pairs)):
            edges = [(u, v, F(i + 1, i % 3 + 1))
                     for i, (u, v) in enumerate(pairs) if mask & (1 << i)]
            brute = min(crossing(order, edges) for order in permutations(range(n)))
            check(brute == subset_dp(n, edges), 'weighted_cutwidth_all_small_graphs')
        edges = [(0, 1, F(2, 5)), (0, 1, F(3, 5))]
        check(subset_dp(n, edges) == 1, 'parallel_edges_and_isolates')
        check(subset_dp(n, []) == 0, 'empty_graph')
    low = (F(7, 2), F(3), F(1, 2))
    high = (F(14), F(15), F(2))
    low_edges = [(0, i + 1, w) for i, w in enumerate(low)]
    high_edges = [(0, i + 1, w) for i, w in enumerate(high)]
    rows = [(order, crossing(order, low_edges), crossing(order, high_edges))
            for order in permutations(range(4))]
    check(min(x for _, x, _ in rows) == F(7, 2), 'star_low_optimum')
    check(min(y for _, _, y in rows) == 16, 'star_high_optimum')
    penalties = [max(x - F(7, 2), y - 16) for _, x, y in rows]
    for value in penalties:
        check(value >= F(1, 2), 'every_star_order_two_accuracy_penalty')
    check(min(penalties) == F(1, 2), 'sharp_minimum_star_penalty_coefficient')
    for weights in product((F(0), F(1, 2), F(1), F(3)), repeat=3):
        edges = [(0, i + 1, w) for i, w in enumerate(weights)]
        partitions = [max(sum((weights[i] for i in range(3) if mask & (1 << i)), F(0)),
                          sum((weights[i] for i in range(3) if not mask & (1 << i)), F(0)))
                      for mask in range(8)]
        check(min(partitions) == min(crossing(order, edges) for order in permutations(range(4))),
              'star_partition_formula')
    WITNESSES['star'] = {'orders': len(rows), 'low_slope': '7/2',
                         'high_slope': '16', 'minimum_worst_penalty': '1/2'}


def volumes(nodes):
    return [F(1)] + [max(mul(abs(x - y) for x, y in combinations(chosen, 2))
                          for chosen in combinations(nodes, size))
                     for size in range(1, len(nodes) + 1)]


def leja_scales(nodes):
    left = sorted(enumerate(nodes), key=lambda pair: (pair[1], pair[0]))
    first = left.pop(0)
    selected, scales = [first[1]], [F(1)]
    while left:
        pos = max(range(len(left)), key=lambda j: mul(abs(left[j][1] - x) for x in selected))
        _, value = left.pop(pos)
        scales.append(mul(abs(value - x) for x in selected))
        selected.append(value)
    return scales


def collision_tests():
    base = ((0, 0), (1, 0), (2, 1))
    labels = []
    for indices in combinations_with_replacement(range(3), 3):
        value = tuple(sum(base[i][j] for i in indices) for j in range(2))
        if value != (0, 0):
            labels.append(value)
    check(len(labels) == 9 and len(set(labels)) == 9, 'nine_formal_future_labels')
    orders = []
    for size in range(1, 10):
        best = min(sum(a == c for (a, b), (c, d) in combinations(selected, 2))
                   for selected in combinations(labels, size))
        orders.append(best)
        check(best == max(0, size - 6), 'exact_subset_collision_orders')
    for theta in (F(0), F(1, 16), F(1, 256), F(1, 4096)):
        nodes = [(a + theta * b) / 32 for a, b in labels]
        value = volumes(nodes)
        scale = leja_scales(nodes)
        for k in range(1, 10):
            prod_scale = mul(scale[:k])
            check(prod_scale <= value[k] <= factorial(k) * prod_scale,
                  'leja_volume_comparisons_including_exact_collision')
            check((value[k] > 0) == (theta > 0 or k <= 6), 'collision_positive_indices')
        check(all(x >= y for x, y in zip(scale, scale[1:])), 'monotone_leja_scales')
    WITNESSES['collision_orders_l1_to_l9'] = orders


def poly_product(p, q):
    out = [F(0)] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            out[i + j] += x * y
    return out


def integral(p):
    return sum((c / (i + 1) for i, c in enumerate(p)), F(0))


def measure_tests():
    # Genuine positive binary-detector report law with uniform latent prior.
    # Cell likelihoods are k0=1/2+t/4, k1=1/2-t/4; commands are both 1/2.
    likelihoods = ((F(1, 4), F(1, 8)), (F(1, 4), F(-1, 8)), (F(1, 2),))
    for horizon in range(1, 6):
        total = F(0)
        failure = None
        for word in product(range(3), repeat=horizon):
            p = [F(1)]
            for letter in word:
                p = poly_product(p, likelihoods[letter])
            mass = integral(p)
            check(mass >= F(1, 8)**horizon, 'actual_report_word_evidence_lower_bound')
            total += mass
            if word == (2,) * horizon:
                failure = mass
        check(total == 1, 'complete_report_law_normalization')
        check(failure == F(1, 2)**horizon and failure != 1,
              'negative_control_dropping_failure_evidence')
    # Lebesgue measure on [0,1]; a restricted subprobability is dominated
    # even for a disconnected chosen set. No conditioning is performed.
    pieces = ((F(0), F(1, 8)), (F(1, 2), F(5, 8)))
    event_mass = sum((b - a for a, b in pieces), F(0))
    for i in range(17):
        for j in range(i, 17):
            lo, hi = F(i, 16), F(j, 16)
            hit = sum((max(F(0), min(hi, b) - max(lo, a)) for a, b in pieces), F(0))
            check(hit <= hi - lo, 'restricted_subprobability_density_domination')
    interval_mass = F(1, 8)
    conditional = interval_mass / event_mass
    check(conditional > interval_mass, 'negative_control_conditioning_inflates_density')
    WITNESSES['restricted_vs_conditional_interval_mass'] = {
        'restricted': str(interval_mass), 'conditional': str(conditional)}
    # This is an actual matrix of losses, not merely the inequality 1>1/2.
    losses = ((F(1), F(0)), (F(0), F(1)))
    probabilities = (F(1, 2), F(1, 2))
    expected_max = sum((probabilities[i] * max(row) for i, row in enumerate(losses)), F(0))
    max_expected = max(sum((probabilities[i] * losses[i][j] for i in range(2)), F(0)) for j in range(2))
    check(expected_max == 1 and max_expected == F(1, 2), 'negative_control_expectation_maximum')
    check(max_expected >= expected_max / 2, 'valid_boundary_sum_loss_factor')
    inf_max = min(max(row) for row in losses)
    max_inf = max(min(row[j] for row in losses) for j in range(2))
    check(inf_max == 1 and max_inf == 0, 'negative_control_common_controller_quantifiers')
    error = F(0)
    stages = ((F(2), F(1, 10)), (F(3), F(0)), (F(1), F(1, 100)))
    for lipschitz, quantization in stages:
        error = lipschitz * error + quantization
    check(error == F(31, 100) and error > stages[-1][1], 'negative_control_causal_error_accumulation')
    WITNESSES['risk_quantifiers'] = {'E_max': str(expected_max), 'max_E': str(max_expected),
                                    'inf_max': str(inf_max), 'max_inf': str(max_inf)}


def main():
    profile_tests()
    graph_tests()
    collision_tests()
    measure_tests()
    output = {
        'assessment': 'A1 English v25 independent referee diagnostics',
        'submission_commit': '8a84075ee518035069d38fd9262bd455aff4ac86',
        'status': 'passed', 'checks': sum(COUNTS.values()),
        'categories': dict(sorted(COUNTS.items())), 'witnesses': WITNESSES,
        'arithmetic': 'Exact fractions.Fraction; no floating-point comparisons.',
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'scope': ['Finite diagnostics designed after source reading; no author code imported.',
                  'No continuum theorem, arbitrary-prior assertion or journal significance is certified.',
                  'No manuscript build, GitHub Actions run or exhaustive companion audit is claimed.']}
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
