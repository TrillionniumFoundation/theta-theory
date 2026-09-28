#!/usr/bin/env python3
"""Independent exact finite diagnostics for the A2 v14 referee report.

The script imports no author verification code.  It checks only finite algebra
used in the new normal-form projection, free-area direction, and shared-intercept
window design.  It is not a proof certificate, a TeX build, or an editorial
judgment.
"""
from __future__ import annotations

from fractions import Fraction as Q
from math import comb, factorial
import json

COUNTS: dict[str, int] = {}


def check(group: str, condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(f"{group}: {message}")
    COUNTS[group] = COUNTS.get(group, 0) + 1


def determinant(matrix: list[list[Q]]) -> Q:
    a = [[Q(x) for x in row] for row in matrix]
    n = len(a)
    if any(len(row) != n for row in a):
        raise ValueError("expected a square matrix")
    value = Q(1)
    for k in range(n):
        pivot_row = next((i for i in range(k, n) if a[i][k] != 0), None)
        if pivot_row is None:
            return Q(0)
        if pivot_row != k:
            a[k], a[pivot_row] = a[pivot_row], a[k]
            value = -value
        pivot = a[k][k]
        value *= pivot
        for i in range(k + 1, n):
            factor = a[i][k] / pivot
            for j in range(k + 1, n):
                a[i][j] -= factor * a[k][j]
            a[i][k] = Q(0)
    return value


def node_matrix(left: list[Q], right: list[Q]) -> list[list[Q]]:
    n = len(right)
    if len(left) != n + 1:
        raise ValueError("need n+1 left nodes and n right nodes")
    return (
        [[Q(1)] + [x**k for k in range(1, n + 1)] + [Q(0)] * n for x in left]
        + [[Q(1)] + [Q(0)] * n + [x**k for k in range(1, n + 1)] for x in right]
    )


def vandermonde(nodes: list[Q]) -> Q:
    value = Q(1)
    for j in range(len(nodes)):
        for i in range(j):
            value *= nodes[j] - nodes[i]
    return value


def run_checks() -> None:
    # Shared-intercept two-orientation design.
    for n in range(1, 11):
        left = [Q(i) for i in range(1, n + 2)]
        right = [Q(i) for i in range(1, n + 1)]
        expected = Q(1)
        for k in range(1, n + 1):
            expected *= factorial(k) ** 2
        check(
            "joint_window_matrix",
            determinant(node_matrix(left, right)) == expected,
            f"equispaced n={n}",
        )
        for h in (Q(1, 2), Q(1, 3), Q(1, 7)):
            actual = determinant(
                node_matrix([h * x for x in left], [h * x for x in right])
            )
            check(
                "joint_window_matrix",
                actual == h ** (n * (n + 1)) * expected,
                f"scaling n={n}, h={h}",
            )
        left_nonuniform = [Q(i * i + 1, i + 2) for i in range(1, n + 2)]
        right_nonuniform = [Q(2 * i + 1, i + 3) for i in range(1, n + 1)]
        expected_nonuniform = vandermonde(left_nonuniform) * vandermonde(
            right_nonuniform
        )
        for x in right_nonuniform:
            expected_nonuniform *= x
        check(
            "joint_window_matrix",
            expected_nonuniform != 0
            and determinant(node_matrix(left_nonuniform, right_nonuniform))
            == expected_nonuniform,
            f"nonuniform n={n}",
        )
        repeated = list(left)
        repeated[-1] = repeated[0]
        check(
            "joint_window_matrix",
            determinant(node_matrix(repeated, right)) == 0,
            f"repeated node n={n}",
        )

    # Exact mixed-boundary derivative identity at an algebraic solution.
    for n in range(1, 26):
        delta = Q(3, 4)
        delta_prime = Q(2, 15)
        invariant = Q(1, 1000)
        stable = Q(1, 7)
        terminal = invariant / (stable * delta**n)
        denominator = 1 - n * invariant * delta_prime / delta
        invariant_t = stable * delta**n / denominator
        direct = (
            delta**n
            + terminal * n * delta ** (n - 1) * delta_prime * invariant_t
        )
        check(
            "normal_form_mixed_derivative",
            direct == delta**n / denominator,
            f"n={n}",
        )

    # Canonical shear projection: pull back du wedge dP and compute the flux.
    for a in (Q(-1, 3), Q(0), Q(1, 5), Q(2, 7)):
        for b in (Q(-1, 4), Q(0), Q(1, 6), Q(3, 8)):
            for stable, terminal in (
                (Q(0), Q(0)),
                (Q(1, 20), Q(-1, 30)),
                (Q(-1, 25), Q(1, 40)),
            ):
                for n in (1, 2, 5, 9, 17):
                    scale = Q(1, 2) ** n
                    u_s = 1 + 2 * a * stable
                    u_t = scale
                    p_s = -Q(1, 2) + a * stable
                    p_t = scale / 2
                    v_s = scale
                    v_t = 1 + 2 * b * terminal
                    jacobian = u_s * v_t - u_t * v_s
                    wedge_numerator = u_s * p_t - u_t * p_s
                    check(
                        "physical_projection",
                        wedge_numerator == scale,
                        f"wedge a={a}, b={b}, n={n}",
                    )
                    check(
                        "physical_projection",
                        wedge_numerator / jacobian
                        == scale
                        / (
                            (1 + 2 * a * stable)
                            * (1 + 2 * b * terminal)
                            - scale**2
                        ),
                        f"flux a={a}, b={b}, n={n}",
                    )

    # At the unit disk, the normalized derivative of the free billiard area
    # in the sin^(2M+2) support direction is strictly negative.
    for order in range(2, 21):
        m = order + 1
        integral_over_pi = Q(2 * comb(2 * m, m), 4**m)
        check(
            "free_area_direction",
            -integral_over_pi < 0,
            f"M={order}",
        )


def main() -> None:
    run_checks()
    result = {
        "schema": "a2-v14-independent-review-diagnostics-1",
        "scope": "finite_exact_algebra_for_new_v14_arguments_only",
        "checks": dict(sorted(COUNTS.items())),
        "total_checks": sum(COUNTS.values()),
        "mathematical_proof_certificate": False,
        "full_tex_build": False,
        "editorial_decision": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
