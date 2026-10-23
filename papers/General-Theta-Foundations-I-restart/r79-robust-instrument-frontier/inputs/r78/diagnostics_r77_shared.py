#!/usr/bin/env python3
"""Exact rational finite diagnostics for the shared-preparation theorems.

Uses no third-party packages and does not claim to verify arbitrary groups,
all word lengths, theorem proofs, priority, or journal significance.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import itertools
import json


CHECK_COUNTS = {}
ACTIVE_GROUP = None


def require(ok, message):
    if ACTIVE_GROUP is None:
        raise RuntimeError("diagnostic requirement executed outside a named group")
    CHECK_COUNTS[ACTIVE_GROUP] += 1
    if not ok:
        raise RuntimeError(message)


def run_group(name, function):
    global ACTIVE_GROUP
    if ACTIVE_GROUP is not None or name in CHECK_COUNTS:
        raise RuntimeError("diagnostic group must be unique and unnested")
    ACTIVE_GROUP = name
    CHECK_COUNTS[name] = 0
    try:
        return function()
    finally:
        ACTIVE_GROUP = None


def mm(a, b):
    return [[sum((x*y for x, y in zip(row, col)), F(0))
             for col in zip(*b)] for row in a]


def rank(a):
    a = [[F(x) for x in row] for row in a]
    r = 0
    for c in range(len(a[0]) if a else 0):
        p = next((j for j in range(r, len(a)) if a[j][c]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        z = a[r][c]
        a[r] = [v/z for v in a[r]]
        for j in range(len(a)):
            if j != r:
                z = a[j][c]
                a[j] = [v-z*w for v, w in zip(a[j], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def stochastic(a):
    return all(all(x >= 0 for x in row) and sum(row) == 1 for row in a)


def unit(n, i):
    return [F(j == i) for j in range(n)]


def shared_involutions():
    records = []
    for q in range(1, 9):
        eps = F(1, 4*(q+1))
        pi = [F(1, q+1)]*(q+1)
        vs = [[F(c == i)-F(c == 0) for c in range(q+1)]
              for i in range(1, q+1)]
        d = []
        for v in vs:
            d += [[p+eps*x for p, x in zip(pi, v)],
                  [p-eps*x for p, x in zip(pi, v)]]
        transition = [unit(2*q, i ^ 1) for i in range(2*q)]
        require(stochastic(d) and stochastic(transition), "invalid C2 controller")
        require(all(x > 0 for row in d for x in row), "nonpositive decoder")
        checks = 0
        for i in range(q):
            row = unit(2*q, 2*i)
            for length in range(9):
                target = [p + (1 if length % 2 == 0 else -1)*eps*x
                          for p, x in zip(pi, vs[i])]
                require(mm([row], d)[0] == target, "C2 finite-word mismatch")
                row = mm([row], transition)[0]
                checks += 1
        block = [[eps*vs[i][c] for i in range(q)] for c in range(q+1)]
        require(rank(block) == q, "joint sign multiplicity mismatch")
        gram = mm([list(col) for col in zip(*block)], block)
        require(gram == [[eps*eps*(1+int(i == j)) for j in range(q)]
                         for i in range(q)], "Gram spectral certificate mismatch")
        records.append({"q": q, "memory": 2*q, "individual_memory": 2,
                        "sign_block_rank": q, "finite_word_checks": checks,
                        "epsilon": str(eps), "gram": "epsilon^2 (I+J)"})
    return records


def many_initializers():
    records = []
    for r in range(1, 10):
        ts = [F(i, 2*(r+1)) for i in range(1, r+1)]
        maximum = ts[-1]
        d = [[F(1, 2)+maximum, F(1, 2)-maximum],
             [F(1, 2)-maximum, F(1, 2)+maximum]]
        d += [[F(1, 2)+t, F(1, 2)-t] for t in ts[:-1]]
        size = r+1
        transition = [unit(size, 1), unit(size, 0)]
        for t in ts[:-1]:
            positive = F(1, 2)+t/(2*maximum)
            transition.append([1-positive, positive]+[F(0)]*(size-2))
        starts = list(range(2, size))+[0]
        require(stochastic(d) and stochastic(transition), "invalid initializer rows")
        require(len(starts) == r and len(d) == size, "initializer count")
        checks = 0
        for start, t in zip(starts, ts):
            row = unit(size, start)
            for length in range(9):
                v = F(1, 2)+(1 if length % 2 == 0 else -1)*t
                require(mm([row], d)[0] == [v, 1-v], "initializer word mismatch")
                row = mm([row], transition)[0]
                checks += 1
        require(len({tuple(d[i]) for i in starts}) == r, "distinct initial laws")
        require(all(d[i][0] > F(1, 2) for i in starts), "lower-bound sign premise")
        require(all(F(1, 2)-t < F(1, 2) for t in ts), "opposite sign premise")
        records.append({"r": r, "mixed_core": 2, "pure_labels": size,
                        "distinct_initializers": r-1, "finite_word_checks": checks})
    return records


def common_mean_obstruction():
    b = [[F(i == j or j == (i+1) % 4, 2) for j in range(4)]
         for i in range(4)]
    require(stochastic(b) and rank(b) == 3, "mean obstruction rank")
    require(all(b[i][i] > 0 for i in range(4)), "diagonal witness")
    require(all(b[i][j]*b[j][i] == 0 for i in range(4) for j in range(i+1, 4)),
            "fooling-set cross support")
    return {"linear_rank": 3, "nonnegative_rank_lower_certificate": 4,
            "realization_upper": 4, "positive_diagonal_fooling_set": True}


def s3_joint_fourier():
    group = list(itertools.permutations(range(3)))
    inv = {g: tuple(g.index(i) for i in range(3)) for g in group}
    basis = [[F(1), F(0), F(-1)], [F(0), F(1), F(-1)]]
    matrices = {g: [unit(3, g[i]) for i in range(3)] for g in group}
    rho = {g: [row[:2] for row in mm(basis, matrices[g])] for g in group}
    for g in group:
        for h in group:
            product = tuple(h[g[i]] for i in range(3))
            require(mm(rho[g], rho[h]) == rho[product], "standard representation convention")
    lefts = [[1, -1, 0], [1, -1, 0], [1, 0, -1]]
    rights = [[1, -1, 0], [1, 0, -1], [1, -1, 0]]
    decoders = [[[F(1, 3)+F(lefts[i][x]*rights[i][c], 12)
                  for c in range(3)] for x in range(3)] for i in range(3)]
    targets = [{g: decoders[i][g[0]] for g in group} for i in range(3)]
    for table in targets:
        mean = [sum(table[g][c] for g in group)/6 for c in range(3)]
        require(mean == [F(1, 3)]*3, "S3 common mean")
    blocks = []
    for table in targets:
        block = []
        for c in range(3):
            for a in range(2):
                block.append([sum(table[g][c]*rho[inv[g]][a][b] for g in group)/6
                              for b in range(2)])
        blocks.append(block)
    joint = [sum((block[row] for block in blocks), []) for row in range(6)]
    individual = [rank(block) for block in blocks]
    require(individual == [1, 1, 1], "S3 separate multiplicities")
    require(rank(joint) == 3, "S3 joint multiplicity larger than degree")
    residuals = []
    for table in targets:
        for h in group:
            residuals.append(sum((table[tuple(g[h[i]] for i in range(3))]
                                  for g in group), []))
    require(rank(residuals) == 7, "S3 direct residual rank vs joint Fourier rank")
    return {"group": "S3", "irreducible_degree": 2,
            "individual_standard_multiplicities": individual,
            "joint_standard_multiplicity": 3,
            "direct_joint_residual_rank": 7, "common_realization_labels": 9}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path)
    parser.add_argument("--source", type=Path, default=(Path(__file__).resolve().parent / "sections" / "49-shared-preparation.tex"))
    args = parser.parse_args()
    CHECK_COUNTS.clear()
    findings = {
        "shared_involution_families": run_group("shared_involutions", shared_involutions),
        "initializer_families": run_group("many_initializers", many_initializers),
        "different_mean_obstruction": run_group("common_mean_obstruction", common_mean_obstruction),
        "nonabelian_joint_block": run_group("s3_joint_fourier", s3_joint_fourier),
    }
    total_checks = sum(CHECK_COUNTS.values())
    report = {
        "schema": "theta.r77.shared-exact-diagnostics.v1",
        "status": "PASS",
        "evidence_type": "finite exact rational diagnostics; not a theorem proof or priority assessment",
        "check_counting_convention": "One check per executed require() call, including aggregated exact predicates; counters remain active under python -O.",
        "total_checks": total_checks,
        "checks_by_group": dict(CHECK_COUNTS),
        "exact_checks": total_checks,
        "floating_checks": 0,
        "source_sha256": hashlib.sha256(args.source.read_bytes()).hexdigest(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        **findings,
    }
    payload = json.dumps(report, indent=2, sort_keys=True)+"\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload)
    print(payload)


if __name__ == "__main__":
    main()
