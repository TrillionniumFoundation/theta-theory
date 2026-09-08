#!/usr/bin/env python3
"""Exact finite diagnostics for the second A1 v30 referee assessment.

Python standard library only. No repository code is imported. Failure tests
use explicit exceptions, so running with python -O does not remove them.
The 16-atom scope control is NOT a counterexample to v30's regenerative theorem.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from fractions import Fraction as F
from pathlib import Path
from typing import Iterable, Sequence

SUBMISSION = "dc8c1bd475b870cd222627c0cfd6d784363e1728"
COUNTS: dict[str, int] = {}


def check(ok: bool, family: str) -> None:
    COUNTS[family] = COUNTS.get(family, 0) + 1
    if not ok:
        raise ArithmeticError(f"Failed exact check: {family}")


def text(x: F | int) -> str:
    return str(F(x))


def cube_law(epsilon: F) -> None:
    """Verify a strictly positive latent experiment giving the scope control."""
    words = list(itertools.product((-1, 1), repeat=4))
    for report in words:
        evidence = F(0)
        targets = [F(0), F(0)]
        for hidden in words:
            likelihood = F(1)
            for h, x in zip(hidden, report):
                likelihood *= F(3, 4) if h == x else F(1, 4)
            check(likelihood >= F(1, 256), "positive_acquisition_likelihood")
            weight = likelihood / 16
            evidence += weight
            for j in range(2):
                score_mean = F(1, 2) + F(1, 4) * hidden[j] + 2 * epsilon * hidden[j + 2]
                check(F(1, 8) <= score_mean <= F(7, 8), "positive_scored_mean")
                targets[j] += weight * score_mean
        check(evidence == F(1, 16), "uniform_report_evidence")
        for j in range(2):
            expected = F(1, 2) + F(1, 8) * report[j] + epsilon * report[j + 2]
            check(targets[j] / evidence == expected, "posterior_mean_identity")


def partitions_two(points: Sequence[tuple[int, ...]]) -> Iterable[tuple[int, list[int]]]:
    """Enumerate unordered <=2-cell partitions by fixing the last point outside A.

    Gray-code traversal changes one membership at a time. Includes the one-cell
    partition. N=16 therefore gives exactly 2**15 partitions, not 2**16 codes.
    """
    dimension = len(points[0])
    sums = [0] * dimension
    size = 0
    previous = 0
    yield size, sums.copy()
    for index in range(1, 1 << (len(points) - 1)):
        gray = index ^ (index >> 1)
        changed = (gray ^ previous).bit_length() - 1
        direction = 1 if (gray >> changed) & 1 else -1
        size += direction
        for j in range(dimension):
            sums[j] += direction * points[changed][j]
        previous = gray
        yield size, sums.copy()


def scope_control(k: int) -> dict[str, object]:
    """epsilon=1/(8k), and q_j-1/2=epsilon*(k X_j+U_j)."""
    if k < 2:
        raise ValueError("k must be at least 2")
    epsilon = F(1, 8 * k)
    cube_law(epsilon)
    points = [(x,) for x in (-k - 1, -k + 1, k - 1, k + 1)]
    local_best = F(0)
    local_count = 0
    for size, sums in partitions_two(points):
        gain = F(0) if size == 0 else F(sums[0] ** 2, size * (4 - size))
        local_best = max(local_best, gain)
        local_count += 1
    local_error = epsilon ** 2 * (k * k + 1 - local_best)
    check(local_error == epsilon ** 2, "positive_local_distortion")

    grid = list(itertools.product((-k - 1, -k + 1, k - 1, k + 1), repeat=2))
    best_gain = F(0)
    count = 0
    for size, sums in partitions_two(grid):
        gain = F(0) if size == 0 else F(sum(s * s for s in sums), size * (16 - size))
        best_gain = max(best_gain, gain)
        count += 1
    check(count == 32768, "exhaustive_partition_count")
    check(best_gain == k * k, "best_two_center_explained_variance")
    minimum_sum = epsilon ** 2 * (2 * (k * k + 1) - best_gain)
    # Symmetrize an optimal partition by a fair public coordinate-swap seed.
    # This matches the general max >= half-sum lower bound exactly.
    common_risk = minimum_sum / 2
    check(common_risk == F(1, 128) + epsilon ** 2, "two_checkpoint_minimax")
    return {
        "k": k, "epsilon": text(epsilon), "local_distortion": text(local_error),
        "fresh_schedule_risk": text(local_error), "delayed_schedule_risk": text(common_risk),
        "delayed_to_local_ratio": text(common_risk / local_error),
        "local_partitions": local_count, "joint_partitions": count,
    }


def parameter_uniform_certificate() -> dict[str, object]:
    """Exhaustive integer certificate for the 16-atom control for all real k>=2.

    For each cell A, sums of X1,X2,U1,U2 give explained-variance numerator
    (k Sx1+Su1)^2+(k Sx2+Su2)^2, denominator n(16-n).
    Bound it by k^2 using P(k)=Ak^2+Bk+C. The conditions A>=0,
    P(2)>=0, P'(2)>=0 imply P(k)>=0 for every real k>=2.
    This is a finite computational certificate for this control only.
    """
    words = list(itertools.product((-1, 1), repeat=4))
    nonconstant = 0
    for size, sums in partitions_two(words):
        if not size:
            continue
        a = size * (16 - size) - sums[0] ** 2 - sums[1] ** 2
        b = -2 * (sums[0] * sums[2] + sums[1] * sums[3])
        c = -sums[2] ** 2 - sums[3] ** 2
        check(a >= 0, "uniform_partition_quadratic_leading")
        check(4 * a + 2 * b + c >= 0, "uniform_partition_quadratic_at_two")
        check(4 * a + b >= 0, "uniform_partition_quadratic_derivative_at_two")
        nonconstant += 1
    check(nonconstant == 32767, "uniform_certificate_exhaustion")
    return {
        "nonconstant_unordered_partitions": nonconstant,
        "domain": "all real k >= 2; epsilon=1/(8k)",
        "certified_control_formula": "R_delayed=1/128+epsilon^2",
        "not_a_certificate_for": "the A1 manuscript's continuum theorems",
    }


def scalar_constants() -> dict[str, str]:
    h = F(26)
    l_squared = F(128)
    denominator = 96 * h ** 2 * l_squared
    check(denominator == 8306688, "v30_atom_constant")
    bound = denominator / 64800
    check(bound < 129, "v30_all_budget_ratio_bound")
    # Antiderivatives of f(z) dz in u=48(z-1/2), separately on each side.
    def left(u: F) -> F:
        return F(512, 48) * (F(27, 10) / (8 - 5 * u) ** 2 + F(1, 6) / (8 + 3 * u) ** 2)
    def right(u: F) -> F:
        return F(512, 48) * (-F(27, 6) / (8 + 3 * u) ** 2 - F(1, 10) / (8 - 5 * u) ** 2)
    mass = left(F(0)) - left(F(-8, 7)) + right(F(8, 9)) - right(F(0))
    check(mass == F(1, 2), "full_continuous_acquired_mass")
    check(F(5, 16) + F(3, 16) + mass == 1, "full_acquired_mass")
    for s in (F(1), F(1, 2), F(1, 7)):
        for m in (1, 2, 9):
            b_squared = 4 * h ** 2 * l_squared * m ** 2 / s ** 2
            check(F(1, 24) / b_squared == s ** 2 / (8306688 * m ** 2), "atom_unit_occupation_cost")
    return {"continuous_mass": text(mass), "unit_cost_denominator": text(denominator), "all_budget_ratio_upper": text(bound)}


def finite_games() -> dict[str, object]:
    witnesses = []
    for j in range(2, 17):
        off = F(1, j * j)
        value = F(1, j) + F(1, j * j) - F(1, j ** 3)
        primal = off + (1 - off) / j
        dual = (1 + (j - 1) * off) / j
        check(primal == value == dual, "v30_symmetric_game_primal_dual")
        check(value / off == j + 1 - F(1, j), "v30_checkpoint_design_ratio")
        if j in (2, 3, 8, 16):
            witnesses.append({"J": j, "value": text(value), "ratio": text(value / off)})
    return {"symmetric_designs_checked": 15, "examples": witnesses}


def leja_flags() -> dict[str, int]:
    grid = tuple(F(i, 4) for i in range(5))
    configurations = 0
    for nodes in itertools.combinations_with_replacement(grid, 5):
        remaining = list(nodes)
        selected = [remaining.pop(0)]
        scales = [F(1)]
        while remaining:
            products = []
            for node in remaining:
                value = F(1)
                for old in selected:
                    value *= abs(node - old)
                products.append(value)
            index = max(range(len(remaining)), key=lambda i: products[i])
            selected.append(remaining.pop(index))
            scales.append(products[index])
        check(all(a >= b for a, b in zip(scales, scales[1:])), "leja_decreasing_scales")
        prefix = F(1)
        factorial = 1
        for ell in range(1, 6):
            prefix *= scales[ell - 1]
            factorial *= ell
            volume = F(0)
            for indices in itertools.combinations(range(5), ell):
                product = F(1)
                for i, j in itertools.combinations(indices, 2):
                    product *= abs(nodes[i] - nodes[j])
                volume = max(volume, product)
            check(prefix <= volume <= factorial * prefix, "leja_prefix_volume_inequality")
        configurations += 1
    return {"five_node_multisets_including_collisions": configurations}


def main() -> None:
    payload: dict[str, object] = {
        "reviewed_submission": SUBMISSION,
        "method": "independent standard-library exact rational and exhaustive finite calculations",
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "positive_local_risk_scope_controls": [scope_control(k) for k in (2, 4, 8, 16)],
        "parameter_uniform_control_certificate": parameter_uniform_certificate(),
        "manuscript_scalar_constants": scalar_constants(),
        "manuscript_finite_games": finite_games(),
        "manuscript_leja_flags": leja_flags(),
        "check_counts_by_family": COUNTS,
        "scope_limitations": [
            "Finite flags do not prove the uniform attainable-mass or semialgebraic covering results.",
            "The scope-control certificate covers its 16-atom model only, not v30's general theorems.",
            "The author's diagnostic suites and native TeX build were not rerun.",
            "No PDF inspection or exhaustive literature priority search is claimed.",
        ],
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
