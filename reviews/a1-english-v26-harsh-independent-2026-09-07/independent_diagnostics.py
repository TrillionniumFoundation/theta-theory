#!/usr/bin/env python3
"""Independent finite diagnostics for the pinned A1 v26 referee assessment.

Only the standard library is used. No author/prior-referee implementation is
imported or executed. Exact finite calculations are not a proof certificate.
Run: python independent_diagnostics.py > DIAGNOSTICS.json
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from fractions import Fraction as R
from functools import lru_cache
from itertools import combinations, permutations, product
from math import factorial
from pathlib import Path

COUNTS: Counter[str] = Counter()


def check(ok: bool, group: str) -> None:
    COUNTS[group] += 1
    if not ok:
        raise RuntimeError(f"Failed {group} check {COUNTS[group]}")


def mul(a: tuple[R, ...], b: tuple[R, ...]) -> tuple[R, ...]:
    c = [R(0)] * (len(a) + len(b) - 1)
    for i in range(len(a)):
        for j in range(len(b)):
            c[i + j] += a[i] * b[j]
    return tuple(c)


def integral(poly: tuple[R, ...], moment: int = 0) -> R:
    return sum((x / (i + moment + 1) for i, x in enumerate(poly)), R(0))


def prefixes(order: tuple[int, ...]) -> tuple[int, ...]:
    visited = 0
    result = []
    for vertex in order[:-1]:
        visited |= 1 << vertex
        result.append(visited)
    return tuple(result)


@lru_cache(None)
def paths(n: int) -> tuple[tuple[int, ...], ...]:
    return tuple(prefixes(p) for p in permutations(range(n)))


def bottleneck(cost: list[R]) -> R:
    n = (len(cost) - 1).bit_length()

    @lru_cache(None)
    def from_set(mask: int) -> R:
        if mask == len(cost) - 1:
            return R(0)
        return min(max(cost[mask | (1 << v)], from_set(mask | (1 << v)))
                   for v in range(n) if not mask & (1 << v))
    return from_set(0)


def crossing(n: int, edges: list[tuple[int, int, R]]) -> list[R]:
    return [sum((w for u, v, w in edges
                 if ((s >> u) & 1) != ((s >> v) & 1)), R(0))
            for s in range(1 << n)]


@lru_cache(None)
def separators(n: int) -> tuple[tuple[int, ...], ...]:
    vertex_count = (1 << n) - 2
    path_masks = [sum(1 << (x - 1) for x in p) for p in paths(n)]
    return tuple(tuple(i + 1 for i in range(vertex_count) if c & (1 << i))
                 for c in range(1 << vertex_count)
                 if all(c & pm for pm in path_masks))


def minimum_separator(capacities: list[R]) -> R:
    n = (len(capacities) - 1).bit_length()
    return min(sum((capacities[x] for x in c), R(0)) for c in separators(n))


def maximum_vertex_flow(caps: list[R]) -> R:
    """Dense rational residual-network calculation, separate from enumeration."""
    size = len(caps)
    n = (size - 1).bit_length()
    count = 2 * size
    residual = [[R(0) for _ in range(count)] for _ in range(count)]
    large = 1 + sum(caps, R(0))
    for mask in range(size):
        residual[2 * mask][2 * mask + 1] = large if mask in (0, size - 1) else caps[mask]
        for bit in range(n):
            if not mask & (1 << bit):
                residual[2 * mask + 1][2 * (mask | (1 << bit))] = large
    source, sink = 0, count - 1
    value = R(0)
    while True:
        pred = [-1] * count
        pred[source] = source
        stack = [source]
        while stack and pred[sink] == -1:
            u = stack.pop()
            for v, capacity in enumerate(residual[u]):
                if capacity > 0 and pred[v] == -1:
                    pred[v] = u
                    stack.append(v)
        if pred[sink] == -1:
            return value
        v = sink
        delta = large
        while v != source:
            delta = min(delta, residual[pred[v]][v])
            v = pred[v]
        v = sink
        while v != source:
            u = pred[v]
            residual[u][v] -= delta
            residual[v][u] += delta
            v = u
        value += delta


def star_costs(s: R) -> list[R]:
    return crossing(4, [(0, 1, 7*s), (0, 2, max(6*s, 9*s-3)), (0, 3, s)])


def star_optimum(s: R) -> R:
    c = star_costs(s)
    return min(max(c[x] for x in p) for p in paths(4))


def star_arrangement() -> tuple[list[R], list[dict]]:
    """All affine intersections, not a numerical grid of resolution values."""
    breaks = {R(0), R(1)}
    phase_data = []
    for lo, hi, w in [(R(0), R(1), [(7, 0), (6, 0), (1, 0)]),
                       (R(1), None, [(7, 0), (9, -3), (1, 0)])]:
        forms = {}
        for mask in range(1, 15):
            a = b = 0
            for leaf, (m, k) in enumerate(w, start=1):
                if bool(mask & 1) != bool(mask & (1 << leaf)):
                    a += m
                    b += k
            forms[mask] = (a, b)
        points = {lo}
        if hi is not None:
            points.add(hi)
        for (a, b), (c, d) in combinations(set(forms.values()), 2):
            if a != c:
                x = R(d-b, a-c)
                if x > lo and (hi is None or x < hi):
                    points.add(x)
        breaks.update(points)
        finite = sorted(points)
        ends = finite[1:] + ([hi] if hi is None else [])
        for left, right in zip(finite, ends):
            mid = (left + right)/2 if right is not None else left + 1
            candidates = []
            for p in paths(4):
                form = max((forms[x] for x in p), key=lambda z: z[0]*mid + z[1])
                candidates.append(form)
            chosen = min(candidates, key=lambda z: z[0]*mid + z[1])
            for s in ([mid, (2*left + right)/3] if right is not None else [mid, mid+3]):
                check(star_optimum(s) == chosen[0]*s + chosen[1], 'star_affine_arrangement')
            if phase_data and phase_data[-1]['form'] == chosen and phase_data[-1]['end'] == left:
                phase_data[-1]['end'] = right
            else:
                phase_data.append({'start': left, 'end': right, 'form': chosen})
    return sorted(breaks), phase_data


def capped_coefficients(blocks: list[list[R]]) -> list[R]:
    answer = [R(0)] * (1 + sum(len(b)-1 for b in blocks))
    for indexes in product(*(range(len(b)) for b in blocks)):
        value = R(1)
        for b, i in zip(blocks, indexes):
            value *= b[i]
        answer[sum(indexes)] = max(answer[sum(indexes)], value)
    return answer


def run() -> dict:
    graph_count = 0
    for n in range(2, 5):
        possible = list(combinations(range(n), 2))
        for selector in range(1 << len(possible)):
            for s in (R(1, 2), R(1), R(3, 2), R(2)):
                edge_costs = (7*s, max(6*s, 9*s-3), s)
                edges = [(u, v, edge_costs[i % 3])
                         for i, (u, v) in enumerate(possible) if selector & (1 << i)]
                costs = crossing(n, edges)
                check(bottleneck(costs) == min(max(costs[x] for x in p) for p in paths(n)),
                      'graph_bottleneck')
            graph_count += 1
        for seed in range(15):
            costs = [R((mask*mask + seed*7) % 29, 7) for mask in range(1 << n)]
            costs[0] = costs[-1] = R(0)
            check(bottleneck(costs) == min(max(costs[x] for x in p) for p in paths(n)),
                  'nonadditive_bottleneck')
    for n in (3, 4, 5):
        costs = crossing(n, [(0, 1, R(1)), (0, 1, R(2)), (1, 2, R(1, 3))])
        check(bottleneck(costs) == min(max(costs[x] for x in p) for p in paths(n)),
              'multigraph_isolated_vertices')

    flow_cases = 0
    for n in (2, 3):
        for entries in product((R(0), R(1, 3), R(1)), repeat=(1 << n)-2):
            caps = [R(0), *entries, R(0)]
            check(maximum_vertex_flow(caps) == minimum_separator(caps), 'exact_flow_separator')
            flow_cases += 1
    for seed in range(8):
        caps = [R((mask*7 + seed*11) % 17, 16) for mask in range(16)]
        caps[0] = caps[-1] = R(0)
        check(maximum_vertex_flow(caps) == minimum_separator(caps), 'exact_flow_separator')
        flow_cases += 1

    # Finite selected-path law. Capacities bound unconditioned subprobabilities.
    selection_witness = []
    for seed in range(3):
        observations = [(paths(3)[(i*i + 3*i + seed) % 6],
                         (R((i*7 + seed) % 9, 3), R((i*5 + 2*seed) % 7, 2)))
                        for i in range(36)]
        event = [i for i in range(36) if i % 5 not in (1, 4)]
        beta = R(len(event), 36)
        levels = sorted({R(0)} | {x for _, loss in observations for x in loss})
        lower_integral = R(0)
        for ix, t in enumerate(levels):
            caps = [R(0)]*8
            for node in range(1, 7):
                caps[node] = R(sum(node in observations[i][0] and
                                  observations[i][1][node.bit_count()-1] <= t
                                  for i in event), len(event))
            H = minimum_separator(caps)
            tail = R(sum(max(observations[i][1]) > t for i in event), 36)
            check(tail >= beta*max(R(0), 1-H), 'selected_path_tail')
            if ix + 1 < len(levels):
                lower_integral += beta*max(R(0), 1-H)*(levels[ix+1]-t)/2
        max_expected = max(sum((loss[j] for _, loss in observations), R(0))/36 for j in (0, 1))
        check(max_expected >= lower_integral, 'selected_path_integral')
        selection_witness.append({'seed': seed, 'beta': str(beta),
                                  'bound': str(lower_integral), 'max_expected_loss': str(max_expected)})

    # Actual retention detector, with uniform commands integrated analytically.
    # k0=1/2+t/4, k1=1/2-t/4; full command cube [1/4,3/4]^2.
    # First block restriction Omega=[1/4,3/8] x [5/8,3/4].
    # Its command mass is 1/16 and averaged failure likelihood is 1/2+3t/32.
    restricted_failure = (R(1, 32), R(3, 512))
    report_laws = [(R(1, 2),), (R(1, 4), R(1, 8)), (R(1, 4), R(-1, 8))]
    beta_first = integral(restricted_failure)
    first_moment = integral(restricted_failure, 1)
    evidence_cases = []
    for completion_length in range(1, 6):
        total = numerator = R(0)
        for word in product(range(3), repeat=completion_length):
            p = restricted_failure
            for r in word:
                p = mul(p, report_laws[r])
            mass = integral(p)
            check(mass > 0, 'actual_report_word_mass')
            total += mass
            numerator += integral(p, 1)
        check(total == beta_first and numerator == first_moment, 'completion_marginalization')
        check(beta_first / 2**completion_length < total, 'first_block_vs_complete_word')
        evidence_cases.append({'completion_length': completion_length, 'first_block_mass': str(total),
                               'all_failures_mass': str(beta_first/2**completion_length)})
    check(beta_first == R(35, 1024) and first_moment/beta_first == R(18, 35), 'actual_command_integral')

    # Exact Vandermonde polynomials for actual formal sums of {0,1,2+theta^h}.
    labels = sorted((i+2*j, j) for j in range(4) for i in range(4-j) if i+j)
    eta_by_contact = {}
    for contact in (1, 2, 4):
        eta = []
        for ell in range(1, 10):
            orders = []
            for selected in combinations(labels, ell):
                p = (R(1),)
                expected_order = 0
                for (a, b), (c, d) in combinations(selected, 2):
                    factor = [R(c-a)] + [R(0)]*(contact-1) + [R(d-b)]
                    p = mul(p, tuple(factor))
                    expected_order += contact if c == a else 0
                actual_order = next(i for i, coefficient in enumerate(p) if coefficient != 0)
                check(actual_order == expected_order, 'vandermonde_polynomial_orders')
                orders.append(actual_order)
            eta.append(min(orders))
            check(eta[-1] == contact*max(0, ell-6), 'maximal_volume_orders')
        eta_by_contact[str(contact)] = eta
    for theta in (R(0), R(1, 16), R(1, 256), R(1, 65536)):
        raw = [(a + b*theta)/18 for a, b in labels]
        unused = list(range(9))
        picked = []
        scales = []
        while unused:
            scores = {}
            for i in unused:
                value = R(1)
                for j in picked:
                    value *= abs(raw[i]-raw[j])
                scores[i] = value
            best = max(unused, key=lambda i: (scores[i], -i))
            scales.append(scores[best])
            picked.append(best)
            unused.remove(best)
        check(all(scales[i] >= scales[i+1] for i in range(8)), 'leja_monotonicity')
        D = R(1)
        for ell in range(1, 10):
            D *= scales[ell-1]
            V = R(0)
            for selected in combinations(raw, ell):
                value = R(1)
                for a, b in combinations(selected, 2):
                    value *= abs(a-b)
                V = max(V, value)
            check(D <= V <= factorial(ell)*D, 'leja_volume_bound')
            check((V > 0) == (theta > 0 or ell <= 6), 'collision_positive_indices')

    breaks, phase = star_arrangement()
    expected = [(R(0), R(1), (7, 0)), (R(1), R(3, 2), (10, -3)),
                (R(3, 2), R(3), (8, 0)), (R(3), None, (9, -3))]
    check([(r['start'], r['end'], r['form']) for r in phase] == expected, 'four_exact_phases')
    interval_points = sorted({R(1, 2), R(2)} | {s for s in breaks if R(1, 2) <= s <= 2})
    def regrets(points: list[R]) -> list[R]:
        return [max(max(star_costs(s)[x] for x in p)-star_optimum(s) for s in points)
                for p in paths(4)]
    interval_regret = min(regrets(interval_points))
    endpoint_regret = min(regrets([R(1, 2), R(2)]))
    check(interval_regret == 1 and endpoint_regret == R(1, 2), 'interval_vs_endpoint_regret')
    check(star_optimum(R(3, 2)) > (star_optimum(R(1))+star_optimum(R(2)))/2,
          'nonconvexity_witness')

    cap_cases = 0
    for a, b, c in product((R(0), R(1, 16), R(1, 4), R(1)), repeat=3):
        blocks = [[R(1), R(1), a], [R(1), b, c]]
        coeff = capped_coefficients(blocks)
        for x in (R(1), R(2), R(4)):
            lhs = max(v*x**i for i, v in enumerate(coeff))
            rhs = R(1)
            for block in blocks:
                rhs *= max(v*x**i for i, v in enumerate(block))
            check(lhs == rhs, 'capped_profile_factorization')
            for M in (1, 2, 3, 7, 16):
                check(all(v*x**k <= M for k, v in enumerate(coeff)) == (rhs <= M),
                      'integer_budget_inversion')
            cap_cases += 1
    valid = capped_coefficients([[R(1), R(1)], [R(1), R(1), R(1, 4)]])
    invalid = capped_coefficients([[R(1), R(1), R(1, 16)], [R(1), R(1)]])
    check(len(valid) == len(invalid) == 4 and valid[3] == R(1, 4) and invalid[3] == R(1, 16),
          'individual_cap_negative_control')
    matrix = [(R(1), R(0)), (R(0), R(1))]
    emax = sum(map(max, matrix), R(0))/2
    maxe = max(sum(row[j] for row in matrix)/2 for j in (0, 1))
    infmax = min(map(max, matrix))
    maxinf = max(min(row[j] for row in matrix) for j in (0, 1))
    check((emax, maxe, infmax, maxinf) == (1, R(1, 2), 1, 0), 'quantifier_negative_controls')

    return {
        'status': 'passed', 'reviewed_commit': 'a2e5d3737085241137211f1cf21393d5bcafa1ce',
        'checks': sum(COUNTS.values()), 'categories': dict(sorted(COUNTS.items())),
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'simple_graphs': graph_count, 'flow_capacity_vectors': flow_cases,
        'witnesses': {
            'phase_pieces': [{'from': str(x['start']), 'to': str(x['end']) if x['end'] is not None else 'infinity',
                              'slope': x['form'][0], 'intercept': x['form'][1]} for x in phase],
            'complete_interval_regret': str(interval_regret), 'endpoint_regret': str(endpoint_regret),
            'resolution_test_points_from_all_affine_intersections': list(map(str, interval_points)),
            'contact_orders': eta_by_contact, 'selected_path_bounds': selection_witness,
            'actual_uniform_command_first_block_mass': str(beta_first),
            'posterior_first_moment_after_marginalization': str(first_moment/beta_first),
            'completion_mass_records': evidence_cases,
            'expectation_of_max': str(emax), 'max_of_expectations': str(maxe),
            'inf_max': str(infmax), 'max_inf': str(maxinf)},
        'scope': 'Executed independent finite exact arithmetic. No continuum proof certification, native LaTeX build, author-suite execution, or exhaustive companion audit is claimed.'}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
