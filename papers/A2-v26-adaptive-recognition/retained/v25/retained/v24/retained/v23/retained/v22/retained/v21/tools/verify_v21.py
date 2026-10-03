#!/usr/bin/env python3
"""Finite v21 diagnostics. These computations are not proofs of the theorems.

Use a fixed seed, exact arithmetic for lattice/graph identities and explicit
checks rather than assert, so the same diagnostics run under python -O.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
import hashlib
import itertools as it
import json
import math
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parents[1]
COUNTS: Counter[str] = Counter()
RNG = random.Random(20260929)


def check(value: bool, group: str) -> None:
    if not value:
        raise RuntimeError(group)
    COUNTS[group] += 1


def det(u, v):
    return u[0]*v[1] - u[1]*v[0]


def index(columns) -> int:
    return math.gcd(*(abs(det(u, v)) for u, v in it.combinations(columns, 2)))


def sparse_saturation() -> None:
    families = [[(1, 0), (1, 2), (-1, 3)]]
    for _ in range(300):
        cols = [(RNG.randint(-15, 15), RNG.randint(-15, 15))
                for _ in range(RNG.randint(3, 11))] + [(1, 0), (0, 1)]
        RNG.shuffle(cols)
        families.append(cols)
    for cols in families:
        pair = next((list(uv) for uv in it.combinations(cols, 2) if det(*uv)), None)
        if pair is None:
            raise RuntimeError('constructed family lacks independent pair')
        n = abs(det(*pair)); selected = list(pair); old = n; steps = 0
        for v in cols:
            q = index(selected + [v])
            if q < old:
                check(old % q == 0, 'proper_index_divisor')
                check(q*2 <= old, 'factor_two_decrease')
                selected.append(v); old = q; steps += 1
            if old == 1:
                break
        check(index(selected) == 1 == index(cols), 'sparse_saturation')
        check(steps <= n.bit_length()-1, 'logarithmic_adjoining_bound')
        for r in range(1, 7):
            check((r-1)+len(selected) <= r+1+n.bit_length()-1,
                  'witness_edge_count')
        # A moving real period basis does not change the integer index.
        L = ((F(3, 2), F(1, 7)), (F(-1, 5), F(4, 3)))
        move = lambda v: (L[0][0]*v[0]+L[0][1]*v[1],
                          L[1][0]*v[0]+L[1][1]*v[1])
        volume = det((L[0][0], L[1][0]), (L[0][1], L[1][1]))
        for u, v in it.combinations(selected, 2):
            check(det(move(u), move(v))/volume == det(u, v),
                  'persistence_of_normalized_cycle_minors')
    check([abs(det(u, v)) for u, v in it.combinations(families[0], 2)] == [2, 3, 5],
          'nonprimitive_pair_example')


def components(n: int, edges) -> list[tuple[int, ...]]:
    adjacency = [set() for _ in range(n)]
    for i, j in edges:
        adjacency[i].add(j); adjacency[j].add(i)
    unseen = set(range(n)); out = []
    while unseen:
        stack = [min(unseen)]; seen = set()
        while stack:
            v = stack.pop()
            if v in seen:
                continue
            seen.add(v); stack.extend(adjacency[v]-seen)
        unseen -= seen; out.append(tuple(sorted(seen)))
    return sorted(out)


def relative_gap_descent() -> None:
    # Arbitrary positive symmetric gaps: no triangle inequality is used.
    for _ in range(130):
        n = RNG.randint(3, 10)
        gaps = [[0]*n for _ in range(n)]
        for i, j in it.combinations(range(n), 2):
            gaps[i][j] = gaps[j][i] = RNG.randint(1, 30)
        for cutoff in (5, 12, 20, 31):
            full = {(i, j) for i, j in it.combinations(range(n), 2)
                    if gaps[i][j] < cutoff}
            reduced = {(i, j) for i, j in full
                       if not any(gaps[i][k] < gaps[i][j] and
                                  gaps[k][j] < gaps[i][j]
                                  for k in range(n) if k not in (i, j))}
            check(components(n, full) == components(n, reduced),
                  'gap_relative_components')
            cache = {}
            def path(i, j):
                if (i, j) in cache:
                    return cache[i, j]
                if tuple(sorted((i, j))) in reduced:
                    result = [i, j]
                else:
                    k = next(k for k in range(n) if k not in (i, j)
                             and gaps[i][k] < gaps[i][j]
                             and gaps[k][j] < gaps[i][j])
                    check(gaps[i][k] < cutoff and gaps[k][j] < cutoff,
                          'strict_descent_within_cutoff')
                    result = path(i, k)[:-1] + path(k, j)
                cache[i, j] = result
                return result
            for i, j in full:
                p = path(i, j)
                check(p[0] == i and p[-1] == j, 'descent_preserves_endpoints')
                check(all(tuple(sorted((a, b))) in reduced for a, b in zip(p, p[1:])),
                      'descent_uses_relative_edges')
    check(F(9) > F(1)+F(1), 'nonmetric_gap_control')


def aperture_models() -> None:
    # Exact rational rectangular-lattice coset coverage by rounding.
    for sx, sy, r in it.product((F(1), F(3, 2), F(2)),
                               (F(1), F(5, 3)), range(1, 6)):
        rho = (sx+sy)/2  # a deliberately conservative obstacle-cover upper bound
        diameter = F(1, 5); cutoff = 2*rho + F(1, 3)
        L0 = rho+diameter+(r-1)*(cutoff+2*diameter)
        B = L0+F(1, 11)
        for a, b in it.product(range(-8, 9), range(-7, 8)):
            x, y = F(a, 7)*sx, F(b, 9)*sy
            ix = (x/sx+F(1, 2)).numerator//(x/sx+F(1, 2)).denominator
            iy = (y/sy+F(1, 2)).numerator//(y/sy+F(1, 2)).denominator
            ex, ey = x-ix*sx, y-iy*sy
            check(ex*ex+ey*ey < B*B, 'midpoint_coset_in_aperture')
        for distance in (F(0), B/2, B-F(1, 100)):
            endpoint = distance + (cutoff-F(1, 100))/2
            Q = B+cutoff/2+diameter
            check(endpoint+diameter < Q, 'padded_endpoint_body_bound')
        for separation in (F(1, 10), F(1, 3), F(1)):
            Q = B+cutoff/2+diameter
            check((Q+separation/2)**2/(separation/2)**2 == (1+2*Q/separation)**2,
                  'packing_area_bound_identity')


def key_for_pair(i: int, j: int, source, target):
    d = (target[0]-source[0], target[1]-source[1])
    forward = (i, j, d[0], d[1])
    backward = (j, i, -d[0], -d[1])
    return min(forward, backward)


def orbit_and_remainder_models() -> None:
    # Abstract asymmetric shape identities and positioned pairs. This tests
    # orbit bookkeeping, not recovery/congruence of analytic support functions.
    edges = [(0, 0, (1, 0)), (0, 0, (0, 1)), (0, 0, (1, 2)),
             (0, 1, (0, 0)), (1, 1, (2, -1)), (1, 2, (1, 1))]
    expected = {key_for_pair(i, j, (0, 0), d) for i, j, d in edges}
    records = []
    for i, j, d in edges:
        for shift in it.product(range(-3, 4), repeat=2):
            target = (shift[0]+d[0], shift[1]+d[1])
            a = key_for_pair(i, j, shift, target)
            b = key_for_pair(j, i, target, shift)
            check(a == b == key_for_pair(i, j, (0, 0), d),
                  'pair_key_translation_and_reverse')
            records.extend([a, b, a])
    check(set(records) == expected, 'deduplication_preserves_all_orbits')
    for _ in range(30):
        RNG.shuffle(records)
        check(sorted(set(records)) == sorted(expected), 'record_permutation_invariance')
    witness = [(1, 0), (0, 1)]
    extras = [(1, 2), (-2, 3), (4, 1), (2, 1)]
    for mask in it.product((False, True), repeat=4):
        current = witness+[v for v, keep in zip(extras, mask) if keep]
        check(index(current) == 1, 'all_remainder_birth_death_patterns')
        for removed in range(len(extras)):
            subset = witness+[v for i, v in enumerate(extras) if mask[i] and i != removed]
            check(index(subset) == 1, 'unused_tangency_erasure')
    # Disk limit of the actual analytic perturbation example; numerical control
    # only. The open-family conclusion is established in the manuscript proof.
    radius = .04; eps = .001
    cutoff = math.sqrt(5)-2*radius
    check(cutoff > math.sqrt(2), 'cutoff_above_cover_bound')
    check(math.sqrt(5)-2*(radius-eps) > cutoff, 'extra_channel_absent')
    check(math.sqrt(5)-2*(radius+eps) < cutoff, 'extra_channel_present')
    check(1-2*(radius-eps) < cutoff, 'basis_channels_below_cutoff')
    check(2*(radius+eps) < 1/math.sqrt(5), 'extra_channel_center_clearance')
    # Bernstein's variance balance and subdominant linear concentration term.
    for beta in (F(1), F(1, 2), F(1, 3), F(2, 3)):
        h_exp = 1/(2*beta+6)
        check(beta*h_exp == F(1, 2)-3*h_exp, 'witness_rate_bias_variance')
        check(1-4*h_exp >= beta*h_exp, 'witness_rate_linear_term')


def preserved_sources() -> None:
    expected = {
        '01_setting.tex': '30899e3f5008fa7a5eeb9e1cb93646d3db4cf745',
        '02_local.tex': 'f389f30844487e78137752faf4f79bbbbd6797ed',
        '03_descent.tex': 'e8306a346b12211755e7bb04388d1c6c48957116',
        '04_stability.tex': '94cd77010d2c797114319b9b7421cb2e528acbff',
        '05_comparison.tex': '447e8bec209bb431b3cc674e8f093bf1b52a682f',
        '06_canonical.tex': 'd7de0bd052ce9a50ef3176efb1a851c6f1de5dbe'}
    for name, value in expected.items():
        data = (ROOT/'core'/name).read_bytes()
        actual = hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()
        check(actual == value, 'retained_v20_core_blob')


def main() -> None:
    sparse_saturation(); relative_gap_descent(); aperture_models()
    orbit_and_remainder_models(); preserved_sources()
    print(json.dumps({'schema': 'a2-v21-finite-diagnostics-1', 'status': 'passed',
        'total_checks': sum(COUNTS.values()), 'groups': dict(sorted(COUNTS.items())),
        'random_seed': 20260929, 'formal_proof_certificate': False,
        'scope': 'Finite lattice, abstract weighted-graph, aperture, orbit and persistence models; six retained source identities. Not infinite-geometry or statistical proof certification.'},
        indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
