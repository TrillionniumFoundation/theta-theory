#!/usr/bin/env python3
"""Independent exact diagnostics for the external A2 v22 referee report.

The script imports no author verification module.  It checks only finite
arithmetic used by the new completion certificate, reference-free subgroup
recovery, hidden-area testing calculation, and histogram-rate balance.
It is not a proof certificate, a TeX build, or a journal decision.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as F
from itertools import product
from math import gcd
import json
import random

CHECKS: Counter[str] = Counter()


def check(condition: bool, group: str, detail: str = "") -> None:
    if not condition:
        raise RuntimeError(f"{group}: {detail}")
    CHECKS[group] += 1


def det2(a: tuple[tuple[int, int], tuple[int, int]]) -> int:
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def matmul2(a, b):
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2))
        for i in range(2)
    )


def adjugate2(a):
    return ((a[1][1], -a[0][1]), (-a[1][0], a[0][0]))


def gcd_minors(vectors: list[tuple[int, int]]) -> int:
    value = 0
    for i in range(len(vectors)):
        for j in range(i + 1, len(vectors)):
            value = gcd(
                value,
                abs(
                    vectors[i][0] * vectors[j][1]
                    - vectors[i][1] * vectors[j][0]
                ),
            )
    return value


def completion_checks() -> None:
    covolumes = [
        F(1, 2),
        F(2, 3),
        F(1),
        F(7, 4),
        F(5, 2),
        F(11, 3),
        F(9, 2),
    ]
    body_areas = [F(1, 10), F(1, 6), F(1, 4), F(2, 5), F(3, 4)]
    for covol, index, unseen_count, body_area in product(
        covolumes, range(1, 14), range(0, 10), body_areas
    ):
        hidden = unseen_count * body_area
        defect_left = (index - 1) * covol + hidden
        defect_right = index * covol - covol + hidden
        check(defect_left == defect_right, "completion_identity")
        check(defect_left >= 0, "completion_nonnegative")
        check(
            (defect_left == 0) == (index == 1 and unseen_count == 0),
            "completion_zero_iff",
        )


def subgroup_checks() -> None:
    rng = random.Random(20260929)
    # Construct random full-rank integer lattices Lambda=B Z^2 and cycle
    # subgroups Gamma=B M Z^2. The observed vectors are additional integer
    # combinations of the subgroup generators. A selected pair D may generate
    # a further finite-index subgroup of Gamma; D^{-1}d_e must therefore have
    # bounded rational coordinates, and the gcd of 2x2 minors recovers the index.
    for _sample in range(700):
        while True:
            b = (
                (rng.randint(-5, 5), rng.randint(-5, 5)),
                (rng.randint(-5, 5), rng.randint(-5, 5)),
            )
            if det2(b) != 0:
                break
        while True:
            m = (
                (rng.randint(-4, 4), rng.randint(-4, 4)),
                (rng.randint(-4, 4), rng.randint(-4, 4)),
            )
            if det2(m) != 0:
                break
        gamma_basis = matmul2(b, m)
        coeffs = [(1, 0), (0, 1)]
        coeffs += [
            (rng.randint(-6, 6), rng.randint(-6, 6)) for _ in range(5)
        ]
        vectors = [
            (
                gamma_basis[0][0] * x + gamma_basis[0][1] * y,
                gamma_basis[1][0] * x + gamma_basis[1][1] * y,
            )
            for x, y in coeffs
        ]

        # Select the largest determinant pair, as in the manuscript.
        best = None
        best_det = 0
        for i in range(len(vectors)):
            for j in range(i + 1, len(vectors)):
                value = abs(
                    vectors[i][0] * vectors[j][1]
                    - vectors[i][1] * vectors[j][0]
                )
                if value > best_det:
                    best_det = value
                    best = (vectors[i], vectors[j])
        check(best is not None and best_det > 0, "reference_free_group_index")
        assert best is not None
        d = ((best[0][0], best[1][0]), (best[0][1], best[1][1]))
        ddet = det2(d)
        adj = adjugate2(d)

        # Coordinates are adj(D)d_e/det(D), with reduced denominator dividing
        # |det(D)|/covol(Gamma). We check exact rational recovery and the common
        # denominator bound.
        gamma_index_in_d = abs(ddet) // abs(det2(gamma_basis))
        check(gamma_index_in_d >= 1, "denominator_bound")
        for vector in vectors:
            num0 = adj[0][0] * vector[0] + adj[0][1] * vector[1]
            num1 = adj[1][0] * vector[0] + adj[1][1] * vector[1]
            c0, c1 = F(num0, ddet), F(num1, ddet)
            check(
                d[0][0] * c0 + d[0][1] * c1 == vector[0]
                and d[1][0] * c0 + d[1][1] * c1 == vector[1],
                "rational_coordinate",
            )
            check(
                c0.denominator <= gamma_index_in_d
                and c1.denominator <= gamma_index_in_d,
                "denominator_bound",
            )

        # The gcd of all pair determinants is the covolume of Gamma in the
        # ambient coordinates. This is the two-dimensional determinantal-index
        # identity used by Hermite/Smith reduction.
        check(
            gcd_minors(vectors) == abs(det2(gamma_basis)),
            "reference_free_group_index",
        )

        # Unimodular changes of the selected pair do not change the recovered
        # subgroup index.
        for u in [
            ((1, 1), (0, 1)),
            ((1, 0), (1, 1)),
            ((0, -1), (1, 0)),
        ]:
            transformed = matmul2(d, u)
            check(
                abs(det2(transformed)) == abs(ddet),
                "unimodular_invariance",
            )

    # Farey-type separation: distinct reduced rationals with denominators <=Q
    # are separated by at least Q^{-2}.
    for q_bound in range(2, 15):
        rationals = sorted(
            {
                F(p, q)
                for q in range(1, q_bound + 1)
                for p in range(-2 * q_bound, 2 * q_bound + 1)
            }
        )
        for left, right in zip(rationals, rationals[1:]):
            check(
                right - left >= F(1, q_bound * q_bound),
                "rational_separation",
            )


def hidden_area_checks() -> None:
    # Fixed-window experiment: adding hidden area a changes every selected
    # probability by p_A-p_{A+a}=K a/[A(A+a)]. Invert this signal exactly and
    # check a Bernoulli-KL quadratic upper bound on a compact margin.
    for area, hidden, kernel in product(
        [F(1, 2), F(3, 4), F(1), F(3, 2)],
        [F(1, 200), F(1, 100), F(1, 40), F(1, 20)],
        [F(1, 50), F(1, 25), F(1, 10), F(1, 8)],
    ):
        p0 = kernel / area
        p1 = kernel / (area + hidden)
        signal = p0 - p1
        check(
            signal == kernel * hidden / (area * (area + hidden)),
            "hidden_area_linear_signal",
        )
        recovered = signal * area * (area + hidden) / kernel
        check(recovered == hidden, "hidden_area_inversion")

        # Elementary bound KL(Ber(p0)||Ber(p1)) <=
        # (p0-p1)^2/[p1(1-p1)]. We do not evaluate logarithms; this exact upper
        # envelope is the bound used in the two-point argument.
        upper = signal * signal / (p1 * (1 - p1))
        check(upper >= 0, "KL_nonnegative")
        check(upper <= 20 * hidden * hidden, "Bernoulli_KL_upper")


def histogram_balance_checks() -> None:
    for beta in [F(1, 5), F(1, 4), F(1, 3), F(1, 2), F(2, 3), F(1)]:
        # h=r^{1/(2 beta+6)} balances h^beta and sqrt(r)h^{-3}.
        exponent = F(1, 1) / (2 * beta + 6)
        check(
            beta * exponent == F(1, 2) - 3 * exponent,
            "histogram_bias_variance_balance",
        )
        # The Bernstein linear term r h^{-4} is smaller at that choice.
        check(
            1 - 4 * exponent >= beta * exponent,
            "histogram_linear_term_smaller",
        )


def main() -> None:
    completion_checks()
    subgroup_checks()
    hidden_area_checks()
    histogram_balance_checks()
    result = {
        "schema": "a2-v22-independent-review-diagnostics-1",
        "scope": (
            "exact finite arithmetic for the completion defect, reference-free "
            "cycle subgroup, hidden-area decision, and histogram balance only"
        ),
        "status": "passed",
        "checks": dict(sorted(CHECKS.items())),
        "total_checks": sum(CHECKS.values()),
        "imports_author_verification_code": False,
        "formal_proof_certificate": False,
        "full_tex_build": False,
        "editorial_decision": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
