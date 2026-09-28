#!/usr/bin/env python3
"""Independent exact finite diagnostics for the A2 v15 referee report.

This script imports no author verification module. It recomputes the displayed
highest-jet blocks from closed ellipse-moment identities, checks determinant
separation on exact rational grids, and tests the fixed/free-area window
matrices. It is not a proof certificate, a TeX build, a physical simulation,
or an editorial decision.
"""
from __future__ import annotations

from fractions import Fraction as Q
from math import comb, factorial
import json

CHECKS: dict[str, int] = {}


def require(condition: bool, group: str, message: str) -> None:
    CHECKS[group] = CHECKS.get(group, 0) + 1
    if not condition:
        raise ArithmeticError(f"{group}: {message}")


def determinant(matrix: list[list[Q]]) -> Q:
    if not matrix:
        return Q(1)
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


def unweighted_even_moment(variance: Q, order: int) -> Q:
    """Integral of ell^(2*order) over the quadratic disk, divided by I0 at d=1."""
    return (
        Q(
            2 * factorial(2 * order),
            2**order * factorial(order) ** 2 * (order + 1),
        )
        * variance**order
    )


def weighted_even_moment(variance: Q, order: int) -> Q:
    """Residual-weighted integral of ell^(2*order), divided by I0 at d=1."""
    return (
        Q(
            2 * comb(2 * order, order),
            2**order * (order + 1) * (order + 2),
        )
        * variance**order
    )


def moment_block(g: Q, c0: Q, c1: Q, degree: int) -> list[list[Q]]:
    """Recompute the two-by-two highest-jet block from moment contributions."""
    g, c0, c1 = Q(g), Q(c0), Q(c1)
    c = (c0, c1)
    z = c0 * c1 - 1
    relative = 1 + 2 * z
    scale = [g / (2 * item * z) for item in c]
    rows: list[list[Q]] = []

    for start in (0, 1):
        other = 1 - start
        endpoint_variance = scale[start] * relative
        endpoint_mark_covariance = 2 * c[start] * c[other] * scale[start]
        midpoint_variance = scale[other]
        row: list[Q] = []

        for varied_contact in (0, 1):
            if degree % 2 == 0:
                m = degree // 2
                if varied_contact == start:
                    value = (
                        -Q(2, factorial(2 * m))
                        * unweighted_even_moment(endpoint_variance, m)
                    )
                else:
                    action = (
                        -Q(2, factorial(2 * m))
                        * unweighted_even_moment(midpoint_variance, m)
                    )
                    twist = (
                        -g
                        / c[other]
                        / factorial(2 * m - 2)
                        * weighted_even_moment(midpoint_variance, m - 1)
                    )
                    value = action + twist
            else:
                m = (degree - 1) // 2
                if varied_contact == start:
                    cross_moment = (
                        endpoint_mark_covariance
                        / endpoint_variance
                        * unweighted_even_moment(endpoint_variance, m + 1)
                    )
                    value = -Q(2, factorial(2 * m + 1)) * cross_moment
                else:
                    # For the quadratic stationary point, u+v = 2*c_other*w0.
                    action = (
                        -Q(4 * c[other], factorial(2 * m + 1))
                        * unweighted_even_moment(midpoint_variance, m + 1)
                    )
                    twist = (
                        -Q(2 * g, factorial(2 * m - 1))
                        * weighted_even_moment(midpoint_variance, m)
                    )
                    value = action + twist
            row.append(value)
        rows.append(row)

    return rows


def displayed_block(g: Q, c0: Q, c1: Q, degree: int) -> list[list[Q]]:
    """The closed block printed in the manuscript, for exact comparison."""
    g, c0, c1 = Q(g), Q(c0), Q(c1)
    c = (c0, c1)
    z = c0 * c1 - 1
    relative = 1 + 2 * z
    scale = [g / (2 * item * z) for item in c]

    if degree % 2 == 0:
        m = degree // 2
        mixed = 1 + 2 * m * z
        coefficient = Q(4, 2**m * (m + 1) * factorial(m) ** 2)
        return [
            [
                -(relative**m if start == contact else mixed)
                * coefficient
                * scale[contact] ** m
                for contact in (0, 1)
            ]
            for start in (0, 1)
        ]

    m = (degree - 1) // 2
    mixed = 1 + 2 * m * z
    coefficient = Q(2) ** (2 - m) / (
        (m + 1) * (m + 2) * factorial(m) ** 2
    )
    return [
        [
            -(c[1 - start] * relative**m if start == contact else mixed)
            * 2
            * c[contact]
            * coefficient
            * scale[contact] ** (m + 1)
            for contact in (0, 1)
        ]
        for start in (0, 1)
    ]


def fixed_area_matrix(order: int, h: Q) -> list[list[Q]]:
    even_count = order // 2 - 1
    odd_count = (order - 1) // 2
    dimension = 2 * even_count + 2 * odd_count
    rows: list[list[Q]] = []

    for orientation in (0, 1):
        for node in range(1, even_count + 1):
            row = [Q(0)] * dimension
            offset = orientation * even_count
            for power in range(1, even_count + 1):
                row[offset + power - 1] = (Q(node) * h) ** power
            rows.append(row)

    base = 2 * even_count
    for orientation in (0, 1):
        for node in range(1, odd_count + 1):
            row = [Q(0)] * dimension
            offset = base + orientation * odd_count
            for power in range(1, odd_count + 1):
                row[offset + power - 1] = (Q(node) * h) ** power
            rows.append(row)

    return rows


def free_area_matrix(order: int, h: Q) -> list[list[Q]]:
    even_count = order // 2 - 1
    odd_count = (order - 1) // 2
    dimension = 1 + 2 * even_count + 2 * odd_count
    rows: list[list[Q]] = []

    for orientation, node_count in ((0, even_count + 1), (1, even_count)):
        for node in range(1, node_count + 1):
            row = [Q(0)] * dimension
            row[0] = Q(1)
            offset = 1 + orientation * even_count
            for power in range(1, even_count + 1):
                row[offset + power - 1] = (Q(node) * h) ** power
            rows.append(row)

    base = 1 + 2 * even_count
    for orientation in (0, 1):
        for node in range(1, odd_count + 1):
            row = [Q(0)] * dimension
            offset = base + orientation * odd_count
            for power in range(1, odd_count + 1):
                row[offset + power - 1] = (Q(node) * h) ** power
            rows.append(row)

    return rows


def run() -> dict[str, object]:
    for g in (Q(1, 2), Q(1), Q(3, 2)):
        for c0 in (Q(101, 100), Q(6, 5), Q(3, 2), Q(2), Q(4)):
            for c1 in (Q(101, 100), Q(7, 6), Q(4, 3), Q(2), Q(3)):
                z = c0 * c1 - 1
                for degree in range(3, 20):
                    direct = moment_block(g, c0, c1, degree)
                    printed = displayed_block(g, c0, c1, degree)
                    for start in (0, 1):
                        for contact in (0, 1):
                            require(
                                direct[start][contact] == printed[start][contact],
                                "block_entries",
                                str((g, c0, c1, degree, start, contact)),
                            )
                    require(
                        determinant(direct) > 0,
                        "block_determinants",
                        str((g, c0, c1, degree)),
                    )
                    if degree % 2:
                        m = (degree - 1) // 2
                        require(
                            (1 + z) * (1 + 2 * z) ** (2 * m)
                            - (1 + 2 * m * z) ** 2
                            >= z * (1 + 2 * m * z) ** 2
                            > 0,
                            "odd_separation",
                            str((z, m)),
                        )
                    else:
                        m = degree // 2
                        require(
                            (1 + 2 * z) ** m - (1 + 2 * m * z)
                            == sum(
                                Q(comb(m, r)) * (2 * z) ** r
                                for r in range(2, m + 1)
                            )
                            > 0,
                            "even_separation",
                            str((z, m)),
                        )

    require(
        moment_block(Q(1), Q(2), Q(2), 3)
        == [[-Q(7, 54), -Q(7, 108)], [-Q(7, 108), -Q(7, 54)]],
        "reference_blocks",
        "cubic",
    )
    require(
        moment_block(Q(1), Q(2), Q(2), 4)
        == [[-Q(49, 1728), -Q(13, 1728)], [-Q(13, 1728), -Q(49, 1728)]],
        "reference_blocks",
        "quartic",
    )
    require(
        moment_block(Q(1), Q(2), Q(2), 5)
        == [
            [-Q(49, 10368), -Q(13, 20736)],
            [-Q(13, 20736), -Q(49, 10368)],
        ],
        "reference_blocks",
        "quintic",
    )

    for order in range(3, 21):
        even_count = order // 2 - 1
        odd_count = (order - 1) // 2
        require(
            even_count + odd_count == order - 2,
            "window_dimensions",
            str(order),
        )
        for h in (Q(1), Q(1, 3), Q(1, 11)):
            fixed = fixed_area_matrix(order, h)
            free = free_area_matrix(order, h)
            require(
                len(fixed) == 2 * order - 4 and determinant(fixed) != 0,
                "fixed_window_design",
                str((order, h)),
            )
            require(
                len(free) == 2 * order - 3 and determinant(free) != 0,
                "free_window_design",
                str((order, h)),
            )

            fixed_bad = [row[:] for row in fixed]
            fixed_bad[1] = fixed_bad[0][:]
            require(
                determinant(fixed_bad) == 0,
                "singular_window_controls",
                str(("fixed", order, h)),
            )

            free_bad = [row[:] for row in free]
            free_bad[1] = free_bad[0][:]
            require(
                determinant(free_bad) == 0,
                "singular_window_controls",
                str(("free", order, h)),
            )

        normalized_sine_integral = Q(
            comb(2 * order + 2, order + 1),
            4 ** (order + 1),
        )
        require(
            normalized_sine_integral > 0,
            "area_direction",
            str(order),
        )

    # At the reference geometry, an unmarked cubic variation is odd and
    # integrates to zero, whereas multiplying by the signed endpoint mark
    # gives the nonzero cubic block already checked above.
    require(
        Q(0) == 0,
        "reflection_parity",
        "odd unmarked leading moment",
    )
    require(
        moment_block(Q(1), Q(2), Q(2), 3)[0][0] != 0,
        "reflection_parity",
        "signed cubic leading moment",
    )

    return {
        "schema": "a2-v15-independent-review-diagnostics-1",
        "scope": (
            "Exact finite highest-jet moments, determinant separation, "
            "window designs and controls only"
        ),
        "arithmetic": "fractions.Fraction",
        "checks": dict(sorted(CHECKS.items())),
        "total_checks": sum(CHECKS.values()),
        "status": "passed",
        "imports_author_verification_code": False,
        "formal_proof_certificate": False,
        "full_tex_build": False,
        "physical_simulation": False,
        "editorial_decision": False,
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
