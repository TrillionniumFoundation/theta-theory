#!/usr/bin/env python3
"""Finite exact diagnostics for the R75 nonabelian author revision.

Only Python's standard library is used. These computations check specified
finite identities and examples; they are not formal proofs of the general
theorems, independent expert review, or editorial approval.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, permutations
import json
from math import factorial
from pathlib import Path


def compose(g, h):
    """Right-action chronological product: first g, then h."""
    return tuple(h[g[i]] for i in range(len(g)))


def inverse(g):
    out = [0] * len(g)
    for i, j in enumerate(g):
        out[j] = i
    return tuple(out)


def fixed(g):
    return sum(i == j for i, j in enumerate(g))


def standard_matrix(g):
    """Natural zero-sum row representation in basis e_i-e_n."""
    n = len(g)
    return [[int(g[i] == j) - int(g[n - 1] == j)
             for j in range(n - 1)] for i in range(n - 1)]


def rank(matrix):
    a = [[F(x) for x in row] for row in matrix]
    if not a:
        return 0
    r = 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        scale = a[r][c]
        a[r] = [x / scale for x in a[r]]
        for i in range(r + 1, len(a)):
            if a[i][c]:
                scale = a[i][c]
                a[i] = [x - scale * y for x, y in zip(a[i], a[r])]
        r += 1
        if r == min(len(a), len(a[0])):
            break
    return r


def average_matrix(matrices):
    matrices = list(matrices)
    n, m = len(matrices[0]), len(matrices[0][0])
    return [[sum(F(a[i][j]) for a in matrices) / len(matrices)
             for j in range(m)] for i in range(n)]


def fourier_standard(group, table):
    n = len(group[0]) - 1
    out = [[F(0) for _ in range(n)] for _ in range(n)]
    for g, value in zip(group, table):
        rg = standard_matrix(inverse(g))
        for i in range(n):
            for j in range(n):
                out[i][j] += value * rg[i][j] / len(group)
    return out


def partitions(n, minimum=1):
    if n == 0:
        yield ()
    else:
        for first in range(minimum, n + 1):
            for rest in partitions(n - first, first):
                yield (first,) + rest


def partition_checks():
    total = 0
    per_n = []
    for n in range(5, 31):
        count = 0
        for parts in partitions(n):
            r = len(parts)
            if r < 2:
                continue
            index = factorial(n)
            for a in parts:
                index //= factorial(a)
            m = r - 1
            assert index >= n * m, (n, parts, index)
            if not (r == 2 and parts[0] == 1):
                assert index >= n * (m + 1), (n, parts, index)
            else:
                # Full point stabilizer is the single exception. Every
                # proper subgroup of it has at least twice this index.
                assert index == n
                assert 2 * index == n * (m + 1)
            if r >= 3:
                concentrated = factorial(n) // factorial(n - r + 1)
                assert index >= concentrated >= n * r
            count += 1
        per_n.append({"n": n, "orbit_partitions_checked": count})
        total += count
    return {"n_range": [5, 30], "total_partitions_checked": total,
            "by_n": per_n}


def symmetric_checks():
    output = []
    for n in range(3, 7):
        group = list(permutations(range(n)))
        assert len(group) == factorial(n)
        characters = [fixed(g) for g in group]
        assert sum(characters) == len(group)
        table = [F(c, n) for c in characters]
        block = fourier_standard(group, table)
        target = [[F(int(i == j), n * (n - 1))
                   for j in range(n - 1)] for i in range(n - 1)]
        assert block == target
        assert rank(block) == n - 1
        # All standard matrices distinct: a finite check of faithfulness.
        assert len({tuple(map(tuple, standard_matrix(g))) for g in group}) == len(group)
        for t in (F(0), F(1, 2 * (n - 1)), F(1, n - 1)):
            decoders = [[F(1, n) + F(n - 1, n) * t *
                         (int(j == i) - int(j == n - 1))
                         for j in range(n)] for i in range(n - 1)]
            assert all(0 <= d <= 1 for row in decoders for d in row)
            for g in group:
                actual = sum(decoders[i][g[i]] for i in range(n - 1)) / (n - 1)
                expected = F(1, n) + F(fixed(g) - 1, n) * t
                assert actual == expected
        for g in group:
            full_controller = sum(F(int(g[i] == i), n) for i in range(n))
            assert full_controller == F(fixed(g), n)
            # Count the n prepared |ii> basis states surviving the diagonal
            # terminal projector after U_g: independent physical evaluation.
            physical = sum(F(int((g[i], i)[0] == (g[i], i)[1]), n)
                           for i in range(n))
            assert physical == full_controller
        equations = [[int(k == i or k == j) for k in range(n)]
                     for i, j in combinations(range(n), 2)]
        assert rank(equations) == n
        assert all(sum(F(x, n) for x in row) == F(2, n)
                   for row in equations)
        residual_rank = None
        residual_count = None
        if n <= 5:
            residuals = [[fixed(compose(g, h)) for h in group] for g in group]
            residual_rank = rank(residuals)
            residual_count = len(set(map(tuple, residuals)))
            assert residual_rank == 1 + (n - 1) ** 2
            assert residual_count == factorial(n)
        output.append({
            "n": n, "group_elements_enumerated": len(group),
            "standard_fourier_diagonal": str(F(1, n * (n - 1))),
            "standard_fourier_rank": n - 1,
            "residual_rank_exact": residual_rank,
            "residual_count_exact": residual_count,
            "low_interval_endpoint_checked": str(F(1, n - 1)),
            "low_controller_core_size": n * (n - 1),
            "full_controller_core_size": n * n,
            "transposition_system_rank": n,
            "note": "Unrestricted optimum theorem applies only when n>=5."
        })
    return output


def s3_subgroup_checks():
    group = list(permutations(range(3)))
    identity = tuple(range(3))
    subgroups = []
    for mask in range(1 << len(group)):
        h = {group[i] for i in range(len(group)) if (mask >> i) & 1}
        if identity not in h:
            continue
        if all(compose(a, b) in h for a in h for b in h):
            subgroups.append(h)
    assert len(subgroups) == 6
    records = []
    for h in subgroups:
        normal = all(compose(compose(inverse(g), a), g) in h
                     for a in h for g in group)
        cosets = sorted({frozenset(compose(a, g) for a in h)
                         for g in group}, key=lambda s: sorted(s))
        coset_index = {c: i for i, c in enumerate(cosets)}
        actions = {}
        for g in group:
            actions[g] = tuple(coset_index[frozenset(compose(a, g) for a in c)]
                               for c in cosets)
        d = len(cosets)
        return_tables = [[F(int(actions[g][x] == x)) for g in group]
                         for x in range(d)]
        witness = [sum(row[j] for row in return_tables) / d
                   for j in range(len(group))]
        assert sum(witness) / len(group) == F(1, d)
        m_standard = rank(average_matrix(standard_matrix(a) for a in h))
        partial = 0 < m_standard < 2
        assert normal == (not partial)
        wblock = fourier_standard(group, witness)
        expected = [[F(m_standard * int(i == j), 2 * d)
                     for j in range(2)] for i in range(2)]
        assert wblock == expected
        for row in return_tables:
            assert rank(fourier_standard(group, row)) <= m_standard
        if not normal:
            assert rank(wblock) == 2 > m_standard
            for t in (F(1, 100), F(1, 10), F(1)):
                contrasted = [F(1, d) + t * (p - F(1, d)) for p in witness]
                assert rank(fourier_standard(group, contrasted)) == 2
        records.append({"subgroup_order": len(h), "orbit_degree": d,
                        "normal": normal, "standard_multiplicity": m_standard,
                        "witness_standard_rank": rank(wblock)})
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path,
                        default=Path(__file__).with_name("42-nonabelian-memory.tex"))
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("nonabelian_exact_results.json"))
    args = parser.parse_args()
    checks = {
        "symmetric_group_enumeration": symmetric_checks(),
        "subgroup_orbit_partition_bounds": partition_checks(),
        "all_S3_subgroups_and_normality_witness": s3_subgroup_checks(),
    }
    result = {
        "status": "PASS",
        "kind": "finite exact rational/integer diagnostics",
        "not": ["formal proof", "independent human referee report", "editorial decision",
                "exhaustive enumeration of all symmetric-group subgroups",
                "exact determination of intermediate contrast transitions"],
        "completed_utc": datetime.now(timezone.utc).isoformat(),
        "arithmetic": "Python standard-library fractions.Fraction and integers",
        "inherited_R74_source_commit": "29b999abf11c43709e64be58765aa1984d13ac91",
        "source_file": str(args.source),
        "source_sha256": sha256(args.source.read_bytes()).hexdigest(),
        "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "checks": checks,
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "source_sha256": result["source_sha256"],
                      "output": str(args.output),
                      "permutations_enumerated": sum(r["group_elements_enumerated"]
                                                     for r in checks["symmetric_group_enumeration"]),
                      "partitions_checked": checks["subgroup_orbit_partition_bounds"]
                                              ["total_partitions_checked"]}, indent=2))


if __name__ == "__main__":
    main()
