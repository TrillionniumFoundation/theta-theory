#!/usr/bin/env python3
"""Finite exact diagnostics for the R75 nonabelian author revision.

Rational/integer checks use the standard library; exact algebraic and
symbolic checks use SymPy. These computations check specified finite
identities and examples; they are not formal proofs of the general
theorems, independent expert review, or editorial approval.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from math import factorial
from pathlib import Path

import sympy as sp


COUNTS: dict[str, int] = {}
GROUP = "initialization"


def check(condition, message):
    if not condition:
        raise RuntimeError(f"{GROUP}: {message}")
    COUNTS[GROUP] = COUNTS.get(GROUP, 0) + 1


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
    global GROUP
    GROUP = "subgroup_partition_indices_S5_to_S30"
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
            check(index >= n * m, ("ordinary multiplicity bound", n, parts, index))
            if not (r == 2 and parts[0] == 1):
                check(index >= n * (m + 1), ("extra n cost", n, parts, index))
            else:
                # Full point stabilizer is the single exception. Every
                # proper subgroup of it has at least twice this index.
                check(index == n, "point stabilizer degree")
                check(2 * index == n * (m + 1), "proper point stabilizer subgroup cost")
            if r >= 3:
                concentrated = factorial(n) // factorial(n - r + 1)
                check(index >= concentrated >= n * r, "concentrated partition bound")
            count += 1
        per_n.append({"n": n, "orbit_partitions_checked": count})
        total += count
    return {"n_range": [5, 30], "total_partitions_checked": total,
            "by_n": per_n}


def symmetric_checks():
    global GROUP
    output = []
    for n in range(3, 7):
        GROUP = f"symmetric_S{n}"
        group = list(permutations(range(n)))
        check(len(group) == factorial(n), "full symmetric group enumerated")
        characters = [fixed(g) for g in group]
        check(sum(characters) == len(group), "permutation character group mean")
        table = [F(c, n) for c in characters]
        block = fourier_standard(group, table)
        target = [[F(int(i == j), n * (n - 1))
                   for j in range(n - 1)] for i in range(n - 1)]
        check(block == target, "exact standard Fourier coefficient matrix")
        check(rank(block) == n - 1, "full standard Fourier rank")
        # All standard matrices distinct: a finite check of faithfulness.
        check(len({tuple(map(tuple, standard_matrix(g))) for g in group}) == len(group),
              "all standard representation matrices distinct")
        for t in (F(0), F(1, 2 * (n - 1)), F(1, n - 1)):
            decoders = [[F(1, n) + F(n - 1, n) * t *
                         (int(j == i) - int(j == n - 1))
                         for j in range(n)] for i in range(n - 1)]
            check(all(0 <= d <= 1 for row in decoders for d in row), "bounded low-contrast decoders")
            for g in group:
                actual = sum(decoders[i][g[i]] for i in range(n - 1)) / (n - 1)
                expected = F(1, n) + F(fixed(g) - 1, n) * t
                check(actual == expected, "low-contrast response identity")
        for g in group:
            full_controller = sum(F(int(g[i] == i), n) for i in range(n))
            check(full_controller == F(fixed(g), n), "full-contrast response identity")
            # Count the n prepared |ii> basis states surviving the diagonal
            # terminal projector after U_g: independent physical evaluation.
            physical = sum(F(int((g[i], i)[0] == (g[i], i)[1]), n)
                           for i in range(n))
            check(physical == full_controller, "prepared quantum basis calculation")
        equations = [[int(k == i or k == j) for k in range(n)]
                     for i, j in combinations(range(n), 2)]
        check(rank(equations) == n, "transposition rigidity system full column rank")
        check(all(sum(F(x, n) for x in row) == F(2, n)
                  for row in equations), "uniform unique return-law weights")
        residual_rank = None
        residual_count = None
        if n <= 5:
            residuals = [[fixed(compose(g, h)) for h in group] for g in group]
            residual_rank = rank(residuals)
            residual_count = len(set(map(tuple, residuals)))
            check(residual_rank == 1 + (n - 1) ** 2, "exact full residual matrix rank")
            check(residual_count == factorial(n), "all full residual rows distinct")
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
    global GROUP
    GROUP = "normality_all_S3_subgroups"
    group = list(permutations(range(3)))
    identity = tuple(range(3))
    subgroups = []
    for mask in range(1 << len(group)):
        h = {group[i] for i in range(len(group)) if (mask >> i) & 1}
        if identity not in h:
            continue
        if all(compose(a, b) in h for a in h for b in h):
            subgroups.append(h)
    check(len(subgroups) == 6, "all S3 subgroups enumerated")
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
        check(sum(witness) / len(group) == F(1, d), "coset character mean")
        m_standard = rank(average_matrix(standard_matrix(a) for a in h))
        partial = 0 < m_standard < 2
        check(normal == (not partial), "normality versus partial multiplicity")
        wblock = fourier_standard(group, witness)
        expected = [[F(m_standard * int(i == j), 2 * d)
                     for j in range(2)] for i in range(2)]
        check(wblock == expected, "coset character standard Fourier block")
        for row in return_tables:
            check(rank(fourier_standard(group, row)) <= m_standard, "single return-law rank bound")
        if not normal:
            check(rank(wblock) == 2 > m_standard, "character mixture rank obstruction")
            for t in (F(1, 100), F(1, 10), F(1)):
                contrasted = [F(1, d) + t * (p - F(1, d)) for p in witness]
                check(rank(fourier_standard(group, contrasted)) == 2, "positive-contrast rank persistence")
        records.append({"subgroup_order": len(h), "orbit_degree": d,
                        "normal": normal, "standard_multiplicity": m_standard,
                        "witness_standard_rank": rank(wblock)})
    return records


def s3_margin_checks():
    global GROUP
    GROUP = "S3_supnorm_margin_grid"
    group = list(permutations(range(3)))
    preparations = [(F(i, 3), F(j, 3), F(3 - i - j, 3))
                    for i in range(4) for j in range(4 - i)]
    decoders = list(product((F(0), F(1, 2), F(1)), repeat=3))
    contrasts = (F(1, 100), F(1, 10), F(1))
    for lam in preparations:
        for decoder in decoders:
            candidate = [sum(lam[i] * decoder[g[i]] for i in range(3))
                         for g in group]
            for t in contrasts:
                witness = [F(1, 3) + t * F(fixed(g) - 1, 3) for g in group]
                distance = max(abs(f - a) for f, a in zip(witness, candidate))
                check(distance >= t / 6, "certified sup-norm margin on specified exact grid")
    return {"preparations": len(preparations), "decoders": len(decoders),
            "contrasts": [str(t) for t in contrasts],
            "certified_lower_bound": "t/6",
            "scope": "finite grid diagnostic, not optimization over all preparations and decoders"}


def permutation_sign(g):
    inversions = sum(g[i] > g[j] for i in range(len(g))
                     for j in range(i + 1, len(g)))
    return -1 if inversions % 2 else 1


def constant_extra_orbit_absorption():
    """Two sign orbits cancel to a constant and disappear without a label."""
    global GROUP
    GROUP = "constant_extra_orbit_absorption_S5_S6"
    for n in (5, 6):
        group = list(permutations(range(n)))
        s = F(1, n - 1)
        natural_decoder = [[F(1, n) + F(n - 1, n) * s *
                            (int(j == i) - int(j == n - 1))
                            for j in range(n)] for i in range(n - 1)]
        for mass in (F(1, 3), F(1, 2), F(2, 3)):
            compressed = [[mass * d + (1 - mass) / n for d in row]
                          for row in natural_decoder]
            check(all(0 <= d <= 1 for row in compressed for d in row),
                  "compressed decoder is bounded")
            for g in group:
                parity = int(permutation_sign(g) < 0)
                extra_one = (F(0), F(2, n))[parity]
                extra_two = (F(2, n), F(0))[parity]
                extra_total = (1 - mass) * (extra_one + extra_two) / 2
                check(extra_total == (1 - mass) / n,
                      "two nonconstant sign-orbit contributions aggregate to a constant")
                natural = sum(natural_decoder[i][g[i]] for i in range(n - 1)) / (n - 1)
                original = mass * natural + extra_total
                reduced = sum(compressed[i][g[i]] for i in range(n - 1)) / (n - 1)
                target = F(1, n) + mass * s * F(fixed(g) - 1, n)
                check(original == reduced == target,
                      "constant extras absorbed into existing natural decoders")
    return {"groups": ["S5", "S6"], "extra_orbits": "two two-point sign actions",
            "natural_masses": ["1/3", "1/2", "2/3"],
            "before_core_sizes": [24, 34], "after_core_sizes": [20, 30],
            "scope": "finite exact examples of the general Fourier-support absorption proof"}


def multioutput_stacked_rank():
    """Each output alone has Fourier rank1; their common-action rank is2."""
    global GROUP
    GROUP = "multioutput_vertical_stack_negative_control"
    group = list(permutations(range(3)))
    u, v, s = (1, -1, 0), (1, 1, -2), (1, -1, 0)
    preparation_directions = (u, v, tuple(-a - b for a, b in zip(u, v)))
    columns = [[F(1, 3) + F(1, 24) * sum(a[i] * s[g[i]] for i in range(3))
                for g in group] for a in preparation_directions]
    for j in range(len(group)):
        check(sum(column[j] for column in columns) == 1 and
              all(0 <= column[j] <= 1 for column in columns),
              "three-output response is a probability table")
    blocks = [fourier_standard(group, column) for column in columns]
    check([rank(block) for block in blocks] == [1, 1, 1],
          "individual output Fourier ranks all one")
    stacked = [row for block in blocks for row in block]
    check(rank(stacked) == 2, "vertical stack has larger rank than every individual output")
    index = {g: i for i, g in enumerate(group)}
    residuals = [[columns[c][index[compose(g, h)]]
                  for h in group for c in range(3)] for g in group]
    check(rank(residuals) == 5, "full observable module is trivial plus two standard copies")
    return {"group": "S3", "outputs": 3, "individual_standard_ranks": [1, 1, 1],
            "stacked_standard_rank": 2, "observable_dimension": 5,
            "reason": "taking maximum individual output rank would give a false common-action criterion"}


def sharp_lower_algebra():
    """Exact expression checks for the sharp inequality, not a proof search."""
    global GROUP
    GROUP = "sharp_singular_coefficient_symbolic_algebra"
    n, m, maximum = sp.symbols("n m M", positive=True)
    lower = (1 + m) / (n - 1)
    upper = 1 + m / (n - 1)
    base = (1 - maximum + m) / (n - 2)
    raw = base + (n - 1) * maximum + maximum * (base + 1 - maximum) / m
    quadratic = ((1 + m) / (n - 2) + (n - 1) * maximum +
                 (n - 1) * (maximum - maximum ** 2) / (m * (n - 2)))
    check(sp.factor(raw - quadratic) == 0, "null-vector lower bound expands to F(M)")
    check(sp.factor(quadratic.subs(maximum, lower) -
                    (1 + m) * (n + 1 / m) / (n - 1)) == 0,
          "lower concavity endpoint identity")
    check(sp.factor(quadratic.subs(maximum, upper) - (n * upper - 1)) == 0,
          "upper concavity endpoint identity")
    check(sp.factor(sp.diff(quadratic, maximum, 2) +
                    2 * (n - 1) / (m * (n - 2))) == 0,
          "strict-concavity coefficient identity")
    check(sp.factor(upper - lower - (n - 2) / (n - 1)) == 0,
          "ordered endpoint interval length")
    root = sp.sqrt(n)
    optimum = (root + 1) ** 2 / (n - 1)
    check(sp.simplify((1 + m) * (n + 1 / m) / (n - 1) - optimum -
                      (root * m - 1) ** 2 / (m * (n - 1))) == 0,
          "AM-GM gap is an explicit square")
    check(sp.simplify(1 / optimum - (root - 1) / (root + 1)) == 0,
          "reciprocal sharp threshold identity")
    samples = []
    for dim in (5, 6, 9, 16):
        for minimum_magnitude in (sp.Rational(1, 10), sp.Rational(1, 2),
                                  sp.Integer(1), sp.Integer(3)):
            lo = lower.subs({n: dim, m: minimum_magnitude})
            hi = upper.subs({n: dim, m: minimum_magnitude})
            values = [quadratic.subs({n: dim, m: minimum_magnitude,
                                     maximum: lo + theta * (hi - lo)})
                      for theta in (sp.Integer(0), sp.Rational(1, 3),
                                    sp.Rational(2, 3), sp.Integer(1))]
            endpoint_minimum = min(values[0], values[-1])
            check(all(value >= endpoint_minimum for value in values),
                  "sampled concavity lower bound")
            check(sp.simplify(endpoint_minimum - optimum.subs(n, dim)).is_nonnegative,
                  "sampled endpoint lower bound against sharp constant")
        samples.append({"n": dim, "m": ["1/10", "1/2", "1", "3"],
                        "interpolation_fractions": ["0", "1/3", "2/3", "1"]})
    return {"symbolic_expression_checks": 7, "finite_lower_bound_grids": samples,
            "scope": "identities and specified exact samples; the interval and equality proof is in the manuscript"}


def sharp_threshold_checks():
    """Finite exact quadratic-field checks, aggregated per matrix or table."""
    global GROUP
    records = []
    for n in (5, 6, 9, 16):
        GROUP = f"sharp_threshold_and_rigidity_S{n}"
        root = sp.sqrt(n)
        r = n - 1
        a, b = 1 - root / n, root / n
        tau = sp.radsimp((root - 1) / (root + 1))
        rows = sp.zeros(r, n)
        for i in range(r):
            rows[i, i], rows[i, n - 1] = a, b
        centered = rows - sp.ones(r, n) / n
        coefficient = (rows.T * rows / r).applyfunc(sp.simplify)
        projection = sp.eye(n) - sp.ones(n) / n
        check((centered * centered.T - a ** 2 * sp.eye(r)).applyfunc(sp.simplify)
              == sp.zeros(r), "centered preparation rows are orthogonal with stated norm")
        check(sp.simplify(sum(coefficient) - 1) == 0 and
              all(entry.is_nonnegative for entry in coefficient),
              "extremal coefficient is nonnegative with total mass one")
        check((projection * coefficient * projection - tau * projection / n)
              .applyfunc(sp.simplify) == sp.zeros(n),
              "sharp centered coefficient identity")
        magnitude = root / n
        maximum = (1 + magnitude) / r
        null_vector = sp.Matrix([maximum] * r + [-magnitude])
        c = sp.Matrix([maximum] * r + [maximum + maximum / magnitude])
        check((coefficient * null_vector).applyfunc(sp.simplify) == sp.zeros(n, 1) and
              coefficient[:r, :r] == (a ** 2 / r * sp.eye(r)).applyfunc(sp.simplify),
              "null vector plus nonsingular leading minor certify rank n-1")
        check(sp.simplify(sum(null_vector) - 1) == 0 and
              sp.simplify(null_vector.dot(c)) == 0,
              "equality left-null normalization and orthogonality")
        canonical = tau / n * (sp.eye(n) + c * sp.ones(1, n) -
                               sp.ones(n, 1) * null_vector.T)
        check((canonical - coefficient).applyfunc(sp.simplify) == sp.zeros(n),
              "canonical equality matrix agrees with positive Gram construction")
        check(sp.simplify(tau * sum(c) - 1) == 0 and
              sp.simplify(n - 1 - sum(c)).is_positive,
              "sharp sum bound and strict exclusion of other equality branch")

        if n <= 6:
            elements = list(permutations(range(n)))
            enumeration_scope = "all group elements"
        else:
            transposition = (1, 0) + tuple(range(2, n))
            cycle = tuple(range(1, n)) + (0,)
            double_transposition = (1, 0, 3, 2) + tuple(range(4, n))
            elements = [tuple(range(n)), transposition, cycle, double_transposition]
            enumeration_scope = "identity, transposition, full cycle, double transposition"
        for theta in (sp.Integer(0), sp.Rational(1, 2), sp.Integer(1)):
            decoder = theta * rows + (1 - theta) * sp.ones(r, n) / n
            contrast_coefficient = (rows.T * decoder / r).applyfunc(sp.expand)
            check(all(sp.expand(sum(contrast_coefficient[i, g[i]] for i in range(n)) -
                                (1 + theta * tau * (fixed(g) - 1)) / n) == 0
                      for g in elements),
                  "complete specified response table at sharp contrast or its mixtures")

        uniform = [sp.Rational(1, r)] * r
        boundary = [a / r + b] + [a / r] * (r - 1)
        interior = [(x + y) / 2 for x, y in zip(uniform, boundary)]
        for weights in (uniform, boundary, interior):
            decoders = sp.zeros(r, n)
            for i in range(r):
                for j in range(n):
                    decoders[i, j] = sp.simplify(rows[i, j] / (r * weights[i]))
            check(sp.simplify(sum(weights) - 1) == 0 and
                  all(sp.simplify(weight - a / r).is_nonnegative for weight in weights) and
                  all(entry.is_nonnegative and (1 - entry).is_nonnegative for entry in decoders),
                  "classified uniform, boundary, or interior weights give valid decoders")
            weighted = sp.zeros(n)
            for i in range(r):
                weighted += weights[i] * rows[i, :].T * decoders[i, :]
            check((weighted - coefficient).applyfunc(sp.simplify) == sp.zeros(n),
                  "classified nonuniform factorization preserves the unique coefficient matrix")
        forbidden_weight = a / (2 * r)
        check(sp.simplify(a / (r * forbidden_weight) - 2) == 0,
              "below-bound weight forces an illegal decoder value two")

        # A nonsymmetric singular example verifies the relaxed lemma's scope:
        # no symmetry or positive-semidefiniteness premise is silently used.
        vertex = sp.zeros(n, 1)
        vertex[0] = 1
        unequal_c = sp.ones(n, 1)
        unequal_c[0], unequal_c[1] = 0, 2
        small_t = sp.Rational(1, n)
        nonsymmetric = small_t / n * (sp.eye(n) + unequal_c * sp.ones(1, n) -
                                       sp.ones(n, 1) * vertex.T)
        check(nonsymmetric != nonsymmetric.T and
              all(entry.is_nonnegative for entry in nonsymmetric) and
              sum(nonsymmetric) == 1 and vertex.T * nonsymmetric == sp.zeros(1, n) and
              projection * nonsymmetric * projection == small_t * projection / n,
              "nonsymmetric nonnegative singular control satisfies all lemma hypotheses")
        records.append({
            "n": n, "threshold_exact": str(tau), "core_below_and_at_threshold": n * r,
            "core_above_threshold": n * n, "elements_checked": len(elements),
            "element_scope": enumeration_scope, "contrast_multipliers": ["0", "1/2", "1"],
            "weight_families": ["uniform", "one larger weight and all others at lower bound",
                                "midpoint of those two"],
            "negative_control": "one weight below a/(n-1) gives a decoder entry equal to2",
            "relaxed_matrix_control": "nonsymmetric entrywise nonnegative singular matrix"
        })
    return records


def main():
    global GROUP
    COUNTS.clear()
    parser = argparse.ArgumentParser()
    sibling = Path(__file__).with_name("42-nonabelian-memory.tex")
    default_source = sibling if sibling.exists() else Path(__file__).parent / "sections" / sibling.name
    parser.add_argument("--source", type=Path,
                        default=default_source)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    checks = {
        "symmetric_group_enumeration": symmetric_checks(),
        "subgroup_orbit_partition_bounds": partition_checks(),
        "all_S3_subgroups_and_normality_witness": s3_subgroup_checks(),
        "S3_supnorm_margin": s3_margin_checks(),
        "constant_extra_orbit_absorption": constant_extra_orbit_absorption(),
        "multioutput_vertical_stack": multioutput_stacked_rank(),
        "sharp_singular_coefficient_algebra": sharp_lower_algebra(),
        "closed_threshold_and_extremal_rigidity": sharp_threshold_checks(),
    }
    total = sum(COUNTS.values())
    result = {
        "schema": "general-theta.r75.nonabelian-diagnostics.v1",
        "status": "PASS",
        "total_checks": total,
        "exact_checks": total,
        "floating_checks": 0,
        "checks_by_group": COUNTS,
        "groups": COUNTS,
        "kind": "finite exact rational/integer/algebraic diagnostics and symbolic identity checks",
        "not": ["formal proof", "independent human referee report", "editorial decision",
                "exhaustive enumeration of all symmetric-group subgroups",
                "a proof of universal assertions from finite samples"],
        "arithmetic": ["Q", "Z", "Q(sqrt(n))", "symbolic rational and radical identities"],
        "sympy_version": sp.__version__,
        "matrix_conventions": {
            "permutation": "P_g[i,j]=1 iff i.g=j; P_g P_h=P_gh",
            "standard_basis": "e_i-e_n as row vectors",
            "fourier": "|G|^-1 sum_g f(g) rho(g^-1)",
            "quantum": "U_g=P_g^T tensor I; U_g|x,y>=|x.g,y>"
        },
        "inherited_R74_source_commit": "29b999abf11c43709e64be58765aa1984d13ac91",
        "source_file": args.source.name,
        "source_sha256": sha256(args.source.read_bytes()).hexdigest(),
        "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "checks": checks,
    }
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
