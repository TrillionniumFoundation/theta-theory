#!/usr/bin/env python3
"""Exact finite checks for the R74 contracting/instrument research draft.

These execute explicit data and identities, not the universally quantified
theorems, infinite-memory proof, novelty judgment, or a proof assistant.
Every check remains active under python -O.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
from itertools import combinations, permutations, product
import json
from pathlib import Path

COUNTS = {}


def check(ok, group, message):
    if not ok:
        raise RuntimeError(f"{group}: {message}")
    COUNTS[group] = COUNTS.get(group, 0) + 1


def matrix(rows):
    return tuple(tuple(F(x) for x in row) for row in rows)


def eye(n):
    return matrix([[int(i == j) for j in range(n)] for i in range(n)])


def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(len(b)))
                       for j in range(len(b[0]))) for i in range(len(a)))


def mv(a, x):
    return tuple(sum(ai * xi for ai, xi in zip(row, x)) for row in a)


def vm(x, a):
    return tuple(sum(x[i] * a[i][j] for i in range(len(x)))
                 for j in range(len(a[0])))


def transpose(a):
    return tuple(zip(*a))


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def combine(terms):
    return tuple(tuple(sum(t * a[i][j] for t, a in terms)
                       for j in range(len(terms[0][1][0])))
                 for i in range(len(terms[0][1])))


def det(a):
    n = len(a)
    total = F(0)
    for p in permutations(range(n)):
        inversions = sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n))
        term = F((-1) ** inversions)
        for i in range(n):
            term *= a[i][p[i]]
        total += term
    return total


W = matrix([[2, -1], [1, 2]])
TAU = matrix([[1, 0], [0, 0]])
I2 = eye(2)
STATIONARY = combine([(F(1, 2), I2)])


def depolarize(x):
    return combine([(trace(x) / 2, I2)])


def branch(s, x):
    p0 = combine([(F(1, 40), mm(mm(W, x), transpose(W)))])
    p1 = combine([((3 * x[0][0] + x[1][1]) / 16, TAU)])
    if s == 0:
        return p0
    if s == 1:
        return p1
    return combine([(1, depolarize(x)), (-1, p0), (-1, p1)])


def state(word, x=STATIONARY):
    for s in word:
        x = branch(s, x)
    return x


def probability(word):
    return trace(state(word))


def choi(s):
    out = [[F(0) for _ in range(4)] for _ in range(4)]
    for i, j in product(range(2), repeat=2):
        e = matrix([[int(k == i and l == j) for l in range(2)] for k in range(2)])
        b = branch(s, e)
        for k, l in product(range(2), repeat=2):
            out[2 * i + k][2 * j + l] = b[k][l]
    return matrix(out)


def instrument_checks():
    ch = [choi(s) for s in range(3)]
    check(combine([(1, c) for c in ch]) == combine([(F(1, 2), eye(4))]),
          "instrument_choi", "total Choi matrix is exactly depolarizing")
    shifted = combine([(1, ch[2]), (F(-1, 16), eye(4))])
    for i, c in enumerate(ch[:2] + [shifted]):
        check(c == transpose(c), "instrument_choi", f"Hermitian matrix {i}")
        for k in range(1, 5):
            for idx in combinations(range(4), k):
                minor = tuple(tuple(c[j][l] for l in idx) for j in idx)
                check(det(minor) >= 0, "instrument_choi", f"principal minor {i} {idx}")
    check(mm(ch[0], ch[0]) == combine([(F(1, 4), ch[0])]),
          "instrument_choi", "unitary branch nonzero Choi eigenvalue is 1/4")
    check(ch[1] == matrix([[F(3, 16), 0, 0, 0], [0, 0, 0, 0],
                          [0, 0, F(1, 16), 0], [0, 0, 0, 0]]),
          "instrument_choi", "reset branch Choi spectrum is explicit")
    sample_words = [w for n in range(7) for w in product(range(3), repeat=n)]
    bounds = [(F(1, 8), F(1, 8)), (F(1, 16), F(3, 16)),
              (F(11, 16), F(13, 16))]
    for w in sample_words:
        x = state(w)
        p = trace(x)
        check(p > 0, "finite_branch_probabilities", "all sampled cylinders positive")
        check(sum(trace(branch(s, x)) for s in range(3)) == p,
              "finite_branch_probabilities", "prefix consistency")
        for s, (lo, hi) in enumerate(bounds):
            ps = trace(branch(s, x))
            check(lo * p <= ps <= hi * p, "finite_branch_probabilities",
                  "exact conditional outcome bounds")
    small_words = [w for n in range(3) for w in product(range(3), repeat=n)]
    for u, v in product(small_words, repeat=2):
        joint = sum(probability(u + (s,) + v) for s in range(3))
        check(joint == probability(u) * probability(v), "one_dependence",
              "block independence with one unobserved outcome")
    for n in range(5):
        for w in product(range(3), repeat=n):
            check(sum(probability((s,) + w) for s in range(3)) == probability(w),
                  "stationarity", "left consistency at stationary start")
    c0, c1 = F(1), F(3, 5)
    cosines = [c0, c1]
    for n in range(2, 49):
        cosines.append(F(6, 5) * cosines[-1] - cosines[-2])
    for n, cn in enumerate(cosines):
        target = F(1, 64) * F(1, 8) ** n * (1 + cn / 2)
        check(probability((1,) + (0,) * n + (1,)) == target,
              "conditioned_oscillation", "closed cylinder formula")
    hankel = tuple(tuple(probability((1,) + (0,) * (i + j) + (1,))
                         for j in range(3)) for i in range(3))
    check(det(hankel) != 0, "conditioned_oscillation", "exact rank-three Hankel minor")
    check(F(6, 5).denominator != 1, "conditioned_oscillation",
          "rational trace obstruction is nonintegral; root-of-unity argument is analytic")
    return {"hilbert_dimension": 2, "outcomes": 3, "word_hankel_rank": 3,
            "longest_sampled_cylinder": 50,
            "full_cylinder_tree_maximum_length": 6,
            "total_channel": "X -> tr(X) I/2",
            "residual_branch_choi_lower": "I_4/16",
            "infinite_memory_statement": "proved in prose, not inferred from a finite check"}


def contraction_checks():
    fs = [matrix([[F(1, 2), F(1, 4)], [0, F(1, 2)]]),
          matrix([[F(1, 3), F(-1, 3)], [F(1, 6), F(1, 2)]])]
    rho, radius = F(3, 4), F(1, 2)
    x0 = (F(1), F(-1))
    p = (F(1, 3),) * 3
    ell = matrix([[F(1, 8), F(1, 8)], [F(-1, 8), 0], [0, F(-1, 8)]])
    check(mm(fs[0], fs[1]) != mm(fs[1], fs[0]), "common_contraction",
          "commands do not commute")
    for f in fs:
        check(max(sum(abs(x) for x in row) for row in f) <= rho,
              "common_contraction", "common infinity norm contraction")
    for pc, lc in zip(p, ell):
        check(sum(abs(x) for x in lc) <= pc, "common_contraction",
              "all actual orbit vectors in unit ball have legal output")
        check(radius * sum(abs(x) for x in lc) <= pc, "common_contraction",
              "entire core ball is decoder-valid")
    depth = 4
    check(rho ** (depth - 1) <= radius, "common_contraction", "certified entry depth")
    prefixes = [w for n in range(depth) for w in product(range(2), repeat=n)]
    corners = list(product((-radius, radius), repeat=2))
    vectors = []
    for w in prefixes:
        x = x0
        for a in w:
            x = mv(fs[a], x)
        vectors.append(x)
    vectors += corners
    positions = {w: i for i, w in enumerate(prefixes)}
    size = len(vectors)
    tables = []
    for a in range(2):
        table = []
        for i, x in enumerate(vectors):
            row = [F(0)] * size
            if i < len(prefixes) and len(prefixes[i]) < depth - 1:
                row[positions[prefixes[i] + (a,)]] = 1
            else:
                y = mv(fs[a], x)
                check(max(abs(t) for t in y) <= radius, "common_contraction",
                      "core/entry image lies in square")
                for j, corner in enumerate(corners):
                    row[len(prefixes) + j] = ((1 + corner[0] * y[0] / radius ** 2)
                                             * (1 + corner[1] * y[1] / radius ** 2) / 4)
            check(min(row) >= 0 and sum(row) == 1, "common_contraction",
                  "exact stochastic transition row")
            check(vm(row, vectors) == mv(fs[a], x), "common_contraction",
                  "exact coordinate intertwining, sufficient for all words in this model")
            table.append(row)
        tables.append(matrix(table))
    decoder = matrix([[pc + sum(t * xi for t, xi in zip(lc, x))
                       for pc, lc in zip(p, ell)] for x in vectors])
    for row in decoder:
        check(min(row) >= 0 and sum(row) == 1, "common_contraction", "legal decoder")
    initial = tuple(F(i == 0) for i in range(size))
    for n in range(9):
        for w in product(range(2), repeat=n):
            row, x = initial, x0
            for a in w:
                row = vm(row, tables[a])
                x = mv(fs[a], x)
            target = tuple(pc + sum(t * xi for t, xi in zip(lc, x))
                           for pc, lc in zip(p, ell))
            check(vm(row, decoder) == target, "common_contraction_words",
                  "all sampled mixed command words")
    return {"dimension": 2, "commands": 2, "outcomes": 3,
            "common_norm": "infinity", "rho": "3/4", "core_radius": "1/2",
            "prefix_depth": depth, "prefix_labels": len(prefixes),
            "core_labels": len(corners), "total_labels": size,
            "sampled_word_length": 8,
            "exact_all_word_certificate": "stochastic rows and coordinate/output intertwining"}


def period_four_checks():
    cycle = matrix([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
    threshold = combine([(F(1, 3), eye(3)), (F(2, 3), cycle)])
    uniform = matrix([[F(1, 3)] * 3] * 3)
    d = (F(1), F(1, 4), F(1, 4))
    for t in (F(1, 10), F(1, 3), F(1, 2), F(1)):
        q = combine([(t, threshold), (1 - t, uniform)])
        row = (F(1), F(0), F(0))
        for n in range(25):
            oscillation = F(0) if n % 2 else t ** n * F(-1, 3) ** (n // 2)
            target = (1 + oscillation) / 2
            check(sum(x * y for x, y in zip(row, d)) == target,
                  "inherited_period_four", "exact realization at alpha=t/sqrt(3)")
            row = vm(row, q)
    check(trace(threshold) == 1 and det(threshold) == F(1, 3),
          "inherited_period_four", "threshold spectrum polynomial")
    return {"status": "inherited corollary, not newly proved priority claim",
            "positive_alpha_three_label_interval": "(0,1/sqrt(3)]",
            "four_label_interval": "(1/sqrt(3),1]", "zero_alpha_labels": 2}


def solve(a, b):
    n = len(b)
    aug = [list(row) + [F(v)] for row, v in zip(a, b)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if aug[i][j]), None)
        if pivot is None:
            return None
        aug[j], aug[pivot] = aug[pivot], aug[j]
        scale = aug[j][j]
        aug[j] = [v / scale for v in aug[j]]
        for i in range(n):
            if i != j:
                scale = aug[i][j]
                aug[i] = [v - scale * u for v, u in zip(aug[i], aug[j])]
    return tuple(row[-1] for row in aug)


def finite_order_instruments():
    # q=3,6 use coordinates (z,x/sqrt(3)); q=4 uses (z,x).
    # Thus every branch and controller entry checked below is rational,
    # although the physical states for q=3,6 have algebraic entries.
    polygons = {
        3: (matrix([[1, 0], [F(-1, 2), F(1, 2)], [F(-1, 2), F(-1, 2)]]),
            matrix([[F(-1, 2), F(-3, 2)], [F(1, 2), F(-1, 2)]])),
        4: (matrix([[1, 0], [0, 1], [-1, 0], [0, -1]]),
            matrix([[0, -1], [1, 0]])),
        6: (matrix([[1, 0], [F(1, 2), F(1, 2)], [F(-1, 2), F(1, 2)],
                    [-1, 0], [F(-1, 2), F(-1, 2)], [F(1, 2), F(-1, 2)]]),
            matrix([[F(1, 2), F(-3, 2)], [F(1, 2), F(1, 2)]])),
    }

    def decompose(vertices, target):
        for idx in combinations(range(len(vertices)), 3):
            a = tuple(tuple(vertices[j][i] for j in idx) for i in range(3))
            sol = solve(a, target)
            if sol is not None and min(sol) >= 0:
                row = [F(0)] * len(vertices)
                for j, value in zip(idx, sol):
                    row[j] = value
                return tuple(row)
        raise RuntimeError("no nonnegative triangle decomposition")

    def evolve(s, v, rot):
        t, z, y = v
        rz, ry = mv(rot, (z, y))
        first = (t / 8, rz / 8, ry / 8)
        h = (2 * t + z) / 16
        second = (h, h, F(0))
        if s == 0:
            return first
        if s == 1:
            return second
        return (t - first[0] - second[0], -first[1] - second[1], -first[2])

    cases = []
    for q, (points, generator) in polygons.items():
        for power in (1, q - 1):
            rot = eye(2)
            for _ in range(power):
                rot = mm(rot, generator)
            check(all(mv(rot, points[j]) == points[(j + power) % q]
                      for j in range(q)), "finite_order_instrument", "root action permutes q vertices")
            vertices = tuple((F(1),) + v for v in points)
            mixed_tables = []
            pure_tables = []
            expanded = vertices + ((F(1), F(0), F(0)),)
            for s in range(3):
                table = []
                for v in expanded:
                    target = evolve(s, v, rot)
                    row = decompose(vertices, target)
                    check(vm(row, vertices) == target, "finite_order_instrument",
                          "exact unnormalized branch-state intertwining")
                    check(min(row) >= 0, "finite_order_instrument", "outcome row nonnegative")
                    table.append(row)
                mixed_tables.append(matrix(table[:q]))
                pure_tables.append(matrix([row + (F(0),) for row in table]))
            for i in range(q + 1):
                check(sum(sum(table[i]) for table in pure_tables) == 1,
                      "finite_order_instrument", "three outcome rows sum to one")
            uniform = tuple(F(1, q) for _ in range(q))
            pure = tuple(F(i == q) for i in range(q + 1))
            for n in range(6):
                for w in product(range(3), repeat=n):
                    r, t, v = uniform, pure, (F(1), F(0), F(0))
                    for s in w:
                        r = vm(r, mixed_tables[s])
                        t = vm(t, pure_tables[s])
                        v = evolve(s, v, rot)
                    check(sum(r) == v[0] and sum(t) == v[0],
                          "finite_order_instrument_words", "mixed/pure models reproduce same cylinder")
            cases.append({"order": q, "angle_power": power, "mixed_labels": q,
                          "pure_labels": q + 1, "sampled_word_length": 5})
    return {"cases": cases,
            "scope": "Exact finite constructions; minimality and arbitrary-order law are proved in the manuscript.",
            "arithmetic": "rational coordinate change for orders 3,4,6"}


def run():
    details = {"instrument": instrument_checks(),
               "contracting_common_machine": contraction_checks(),
               "inherited_period_four": period_four_checks(),
               "finite_order_instruments": finite_order_instruments()}
    total = sum(COUNTS.values())
    return {"schema": "gtf-r74-noisy-diagnostics-v1", "status": "passed",
            "arithmetic": "exact integers and fractions.Fraction",
            "total_checks": total, "exact_checks": total, "floating_probes": 0,
            "checks_by_group": dict(sorted(COUNTS.items())), "details": details,
            "diagnostic_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "limits": ["Finite identities do not replace quantified theorem proofs.",
                       "The infinite-memory statement is proved analytically, not by these finite probes.",
                       "No general quantifier elimination, proof assistant, human referee approval, or journal decision is claimed.",
                       "All explicit checks remain active under python -O."]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    encoded = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
