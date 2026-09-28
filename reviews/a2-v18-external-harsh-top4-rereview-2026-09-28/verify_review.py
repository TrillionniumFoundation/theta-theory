#!/usr/bin/env python3
"""Independent finite diagnostics for the external A2 v18 rereview.

The exact suite uses only the Python standard library and imports no author
verification module.  ``--geometry`` adds nonlinear stationary-ray tests and
requires NumPy and SciPy.  Neither mode is a proof certificate or a TeX build.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
from itertools import product
import json
import math

REVIEWED_COMMIT = "0708f67908355e9881d1993b42bcc698b0c350c6"
CHECKS: Counter[str] = Counter()


def check(condition: bool, group: str, detail: str = "") -> None:
    if not condition:
        raise RuntimeError(f"{group}: {detail}")
    CHECKS[group] += 1


# ---------------------------------------------------------------------------
# Local Schur-complement geometry
# ---------------------------------------------------------------------------

def exact_local_geometry() -> None:
    gaps = [F(1, 4), F(2, 5), F(3, 4), F(1), F(7, 4), F(5, 2)]
    source_curvatures = [F(1, 7), F(1, 3), F(3, 5), F(1), F(11, 6)]
    opposite_curvatures = [F(1, 8), F(2, 7), F(4, 5), F(3, 2), F(7, 3)]
    slopes = [F(0), F(1, 11), F(-1, 9), F(2, 9), F(-1, 4), F(3, 10)]

    for gap, source_k, opposite_k, slope in product(
        gaps, source_curvatures, opposite_curvatures, slopes
    ):
        # Rational parametrization a^2+v^2=1 with v>0.
        a = 2 * slope / (1 + slope * slope)
        v = (1 - slope * slope) / (1 + slope * slope)

        d_ss = v * v / gap + source_k * v
        d_su = -v / gap
        d_uu = 1 / gap + opposite_k

        w_st = -(d_su * d_su) / (2 * d_uu)
        w_ss = d_ss + w_st

        recovered_source = (w_ss - w_st - v * v / gap) / v
        recovered_opposite = (v * v / (-2 * gap * w_st) - 1) / gap
        recovered_speed = -d_su / d_uu

        check(
            recovered_source == source_k,
            "source_curvature",
            str((gap, source_k, opposite_k, slope)),
        )
        check(
            recovered_opposite == opposite_k,
            "opposite_curvature",
            str((gap, source_k, opposite_k, slope)),
        )
        check(
            recovered_speed == v / (1 + gap * opposite_k),
            "foot_speed",
            str((gap, source_k, opposite_k, slope)),
        )
        check(
            w_st < 0 and v > 0 and d_uu > 0,
            "margins",
            str((gap, source_k, opposite_k, slope)),
        )


# ---------------------------------------------------------------------------
# Truncated bivariate jets for the two-window quotient
# ---------------------------------------------------------------------------

KEYS = [(i, j) for i in range(4) for j in range(4 - i)]


def add(a: dict[tuple[int, int], F], b: dict[tuple[int, int], F]) -> dict:
    return {key: a.get(key, F(0)) + b.get(key, F(0)) for key in KEYS}


def scale(a: dict[tuple[int, int], F], scalar: F) -> dict:
    return {key: scalar * a.get(key, F(0)) for key in KEYS}


def multiply(a: dict[tuple[int, int], F], b: dict[tuple[int, int], F]) -> dict:
    result = {key: F(0) for key in KEYS}
    for (i, j), x in a.items():
        for (p, q), y in b.items():
            key = (i + p, j + q)
            if key in result:
                result[key] += x * y
    return result


def reciprocal(a: dict[tuple[int, int], F]) -> dict:
    constant = a.get((0, 0), F(0))
    if constant == 0:
        raise ZeroDivisionError("zero constant term")
    z = scale(a, 1 / constant)
    z[(0, 0)] -= 1
    one = {(0, 0): F(1)}
    z2 = multiply(z, z)
    z3 = multiply(z2, z)
    # (1+z)^(-1) = 1-z+z^2-z^3 through total degree three.
    series = add(add(one, scale(z, -1)), add(z2, scale(z3, -1)))
    return scale(series, 1 / constant)


def reflect(poly: dict[tuple[int, int], F]) -> dict:
    return {
        key: (-1) ** (key[0] + key[1]) * value
        for key, value in poly.items()
    }


def exact_two_window_jets() -> None:
    for index in range(1, 301):
        action = {
            (i, j): F(
                ((7 * index + 11 * i + 13 * j) % 41) - 20,
                23 + i + 2 * j,
            )
            for i, j in KEYS
        }
        action[(0, 0)] = F(2 + index % 5, 7)

        flux = {
            (i, j): F(
                ((5 * index + 17 * i + 19 * j) % 37) - 18,
                31 + 2 * i + j,
            )
            for i, j in KEYS
        }
        flux[(0, 0)] = F(3 + index % 7, 9)

        time_1 = F(5 + index % 4, 2)
        time_2 = time_1 + F(2 + index % 5, 13)

        density_1 = multiply(
            flux, add({(0, 0): time_1}, scale(action, -1))
        )
        density_2 = multiply(
            flux, add({(0, 0): time_2}, scale(action, -1))
        )
        difference = add(density_2, scale(density_1, -1))

        recovered = multiply(
            add(scale(density_2, time_1), scale(density_1, -time_2)),
            reciprocal(difference),
        )
        for key in KEYS:
            check(
                recovered[key] == action[key],
                "two_window_C3_identity",
                str((index, key)),
            )

        check(
            scale(difference, 1 / (time_2 - time_1)) == flux,
            "flux_recovery",
            str(index),
        )

        recovered_reflected = multiply(
            add(
                scale(reflect(density_2), time_1),
                scale(reflect(density_1), -time_2),
            ),
            reciprocal(reflect(difference)),
        )
        check(
            recovered_reflected == reflect(action),
            "reversal_equivariance",
            str(index),
        )


# ---------------------------------------------------------------------------
# Cell averages and histogram balance
# ---------------------------------------------------------------------------

def inverse_matrix(matrix: list[list[F]]) -> list[list[F]]:
    size = len(matrix)
    rows = [
        [F(value) for value in row] + [F(i == j) for j in range(size)]
        for i, row in enumerate(matrix)
    ]
    for column in range(size):
        pivot = next(i for i in range(column, size) if rows[i][column])
        rows[column], rows[pivot] = rows[pivot], rows[column]
        value = rows[column][column]
        rows[column] = [entry / value for entry in rows[column]]
        for row in range(size):
            if row == column:
                continue
            value = rows[row][column]
            rows[row] = [
                x - value * y for x, y in zip(rows[row], rows[column])
            ]
    return [row[size:] for row in rows]


def exact_cell_averages() -> None:
    nodes = [-1, 0, 1]
    matrix = [[F(1), F(node), F(node * node) + F(1, 12)] for node in nodes]
    inverse = inverse_matrix(matrix)

    for i, j in product(range(3), repeat=2):
        check(
            sum(inverse[i][k] * matrix[k][j] for k in range(3)) == F(i == j),
            "cell_matrix_inverse",
        )

    for p, q in product(range(3), repeat=2):
        values = [
            [matrix[i][p] * matrix[j][q] for j in range(3)]
            for i in range(3)
        ]
        for a, b in product(range(3), repeat=2):
            recovered = sum(
                inverse[a][i] * inverse[b][j] * values[i][j]
                for i, j in product(range(3), repeat=2)
            )
            check(
                recovered == F(a == p and b == q),
                "tensor_reproduction",
                str((p, q, a, b)),
            )

    for beta in [F(1, 4), F(1, 3), F(1, 2), F(2, 3), F(3, 4), F(1)]:
        exponent = 1 / (beta + 4)
        check(
            beta * exponent == 1 - 4 * exponent,
            "rate_balance",
            str(beta),
        )


# ---------------------------------------------------------------------------
# Marked lattice recovery and the displayed asymmetric support example
# ---------------------------------------------------------------------------

def determinant_2x2(matrix: list[list[F]]) -> F:
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def inverse_2x2(matrix: list[list[F]]) -> list[list[F]]:
    determinant = determinant_2x2(matrix)
    return [
        [matrix[1][1] / determinant, -matrix[0][1] / determinant],
        [-matrix[1][0] / determinant, matrix[0][0] / determinant],
    ]


def multiply_2x2(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [
        [sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)]
        for i in range(2)
    ]


def exact_network_checks() -> None:
    lattices = [
        [[F(3, 2), F(1, 3)], [F(-2, 5), F(7, 4)]],
        [[F(2), F(-1, 2)], [F(1, 4), F(5, 3)]],
    ]

    for a, b, c, d in product(range(-3, 4), repeat=4):
        cycle_matrix = [[F(a), F(b)], [F(c), F(d)]]
        if determinant_2x2(cycle_matrix) == 0:
            continue
        cycle_inverse = inverse_2x2(cycle_matrix)
        for lattice in lattices:
            displacements = multiply_2x2(lattice, cycle_matrix)
            check(
                multiply_2x2(displacements, cycle_inverse) == lattice,
                "lattice_recovery",
                str((cycle_matrix, lattice)),
            )

    # For p(theta)=1+eps cos(2 theta)+eps cos(3 theta+pi/4), a reflection
    # compatible with the second harmonic has a=m*pi/2.  The third harmonic
    # would then require 3m/2+1/4 to be an integer, which never occurs.
    for m in range(4):
        obstruction = F(3 * m, 2) + F(1, 4)
        check(
            obstruction.denominator != 1,
            "reflection_obstruction",
            str(m),
        )
    check(math.gcd(2, 3) == 1, "rotation_obstruction")


# ---------------------------------------------------------------------------
# Optional nonlinear geometry diagnostics
# ---------------------------------------------------------------------------

def nonlinear_geometry() -> dict[str, float | int]:
    import numpy as np
    from scipy.integrate import quad
    from scipy.optimize import brentq

    families = [
        (0.7, 0.4, 0.11, -0.07, 0.03, 0.06, 1.1),
        (1.3, 0.8, -0.16, 0.13, 0.08, 0.04, 0.7),
        (0.5, 0.5, 0.09, -0.12, 0.02, 0.07, 1.4),
        (0.9, 1.6, 0.20, -0.15, 0.05, 0.09, 0.85),
        (1.8, 0.35, -0.12, 0.18, 0.04, 0.03, 1.7),
    ]

    errors: list[float] = []

    for k0, k1, c0, c1, d0, d1, gap in families:
        def graph(y: float, side: int) -> float:
            k, c, d = (k0, c0, d0) if side == 0 else (k1, c1, d1)
            return k * y * y / 2 + c * y**3 / 6 + d * y**4 / 24

        def graph_prime(y: float, side: int) -> float:
            k, c, d = (k0, c0, d0) if side == 0 else (k1, c1, d1)
            return k * y + c * y * y / 2 + d * y**3 / 6

        def graph_second(y: float, side: int) -> float:
            k, c, d = (k0, c0, d0) if side == 0 else (k1, c1, d1)
            return k + c * y + d * y * y / 2

        def arclength(y: float, side: int) -> float:
            return quad(
                lambda z: math.sqrt(1 + graph_prime(z, side) ** 2),
                0,
                y,
                epsabs=1e-13,
                epsrel=1e-13,
            )[0]

        def transverse(arclength_value: float, side: int) -> float:
            return brentq(
                lambda y: arclength(y, side) - arclength_value,
                -0.5,
                0.5,
                xtol=1e-14,
            )

        def source_point(s: float):
            y = transverse(s, 0)
            return np.array([-graph(y, 0), y])

        def opposite_point(u: float):
            return np.array([gap + graph(u, 1), u])

        def action(s: float, t: float, return_foot: bool = False):
            x = source_point(s)
            z = source_point(t)

            def stationarity(u: float) -> float:
                point = opposite_point(u)
                tangent = np.array([graph_prime(u, 1), 1.0])
                return (
                    np.dot(point - x, tangent) / np.linalg.norm(point - x)
                    + np.dot(point - z, tangent) / np.linalg.norm(point - z)
                )

            foot = brentq(stationarity, -0.5, 0.5, xtol=1e-14)
            value = np.linalg.norm(x - opposite_point(foot)) + np.linalg.norm(
                z - opposite_point(foot)
            )
            return (value, foot) if return_foot else value

        for s in np.linspace(-0.18, 0.18, 9):
            base, foot = action(float(s), float(s), True)

            def finite_differences(step: float):
                first = (action(s + step, s) - action(s - step, s)) / (2 * step)
                second = (
                    action(s + step, s) - 2 * base + action(s - step, s)
                ) / step**2
                mixed = (
                    action(s + step, s + step)
                    - action(s + step, s - step)
                    - action(s - step, s + step)
                    + action(s - step, s - step)
                ) / (4 * step**2)
                return np.array([first, second, mixed])

            first, second, mixed = (
                4 * finite_differences(0.0004) - finite_differences(0.0008)
            ) / 3

            ell = base / 2
            v = math.sqrt(max(0.0, 1 - first * first))
            recovered_source = (second - mixed - v * v / ell) / v
            recovered_opposite = (v * v / (-2 * ell * mixed) - 1) / ell

            source_y = transverse(float(s), 0)
            true_source = graph_second(source_y, 0) / (
                1 + graph_prime(source_y, 0) ** 2
            ) ** 1.5
            true_opposite = graph_second(foot, 1) / (
                1 + graph_prime(foot, 1) ** 2
            ) ** 1.5

            errors.extend(
                [
                    abs(recovered_source - true_source),
                    abs(recovered_opposite - true_opposite),
                ]
            )

    maximum = max(errors)
    if maximum >= 2e-6:
        raise RuntimeError(f"nonlinear curvature diagnostic: {maximum}")
    return {
        "comparisons": len(errors),
        "maximum_absolute_curvature_error": maximum,
        "mean_absolute_curvature_error": sum(errors) / len(errors),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--geometry", action="store_true")
    args = parser.parse_args()

    exact_local_geometry()
    exact_two_window_jets()
    exact_cell_averages()
    exact_network_checks()

    result: dict[str, object] = {
        "schema": "a2-v18-independent-review-diagnostics-1",
        "reviewed_commit": REVIEWED_COMMIT,
        "status": "passed",
        "exact_checks": dict(sorted(CHECKS.items())),
        "total_exact_checks": sum(CHECKS.values()),
        "scope": "finite algebra for the new v18 local inverse, histogram stencil, and marked lattice assembly",
        "imports_author_verification_code": False,
        "formal_proof_certificate": False,
        "full_tex_build": False,
        "editorial_decision": False,
    }
    if args.geometry:
        result["nonlinear_geometry"] = nonlinear_geometry()

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
