#!/usr/bin/env python3
"""Independent exact finite diagnostics for the A2 v16 referee report.

The script imports no author verification code and uses only the Python standard
library. It checks finite calibration identities, the formal arclength variation,
registered-lattice linear algebra and dimension counts. It is not a proof
certificate, a nonlinear billiard simulation, a TeX build or an editorial
judgment.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from math import factorial
import json

REVIEWED_COMMIT = "9b0f76a32d1296b4035b52e43a38b3e3ffb50f18"
REVIEWED_TREE = "db18329d561f7f2011e668a7517fe53938331859"
CHECKS: Counter[str] = Counter()


def require(condition: bool, group: str, message: str = "") -> None:
    if not condition:
        raise RuntimeError(f"{group}: {message}")
    CHECKS[group] += 1


def det2(matrix: list[list[Q]]) -> Q:
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def inv2(matrix: list[list[Q]]) -> list[list[Q]]:
    determinant = det2(matrix)
    if determinant == 0:
        raise ValueError("singular two-by-two matrix")
    return [
        [matrix[1][1] / determinant, -matrix[0][1] / determinant],
        [-matrix[1][0] / determinant, matrix[0][0] / determinant],
    ]


def mul2(left: list[list[Q]], right: list[list[Q]]) -> list[list[Q]]:
    return [
        [sum(left[i][k] * right[k][j] for k in range(2)) for j in range(2)]
        for i in range(2)
    ]


def series_multiply(left: list[Q], right: list[Q], order: int) -> list[Q]:
    result = [Q(0)] * (order + 1)
    for i, left_value in enumerate(left[: order + 1]):
        if left_value == 0:
            continue
        for j, right_value in enumerate(right[: order + 1 - i]):
            result[i + j] += left_value * right_value
    return result


def one_plus_series_power(series: list[Q], exponent: Q, order: int) -> list[Q]:
    """Return (1 + series)^exponent modulo x^(order+1), with series[0]=0."""
    if series[0] != 0:
        raise ValueError("the nonconstant series must have zero constant term")
    result = [Q(1)] + [Q(0)] * order
    power = [Q(1)] + [Q(0)] * order
    coefficient = Q(1)
    for degree in range(1, order + 1):
        power = series_multiply(power, series, order)
        coefficient *= Q(exponent - degree + 1, degree)
        for index in range(order + 1):
            result[index] += coefficient * power[index]
    return result


def calibration_checks() -> None:
    gaps = [Q(1, 3), Q(1, 2), Q(1), Q(3, 2), Q(2)]
    c_values = [Q(6, 5), Q(3, 2), Q(2), Q(5, 2), Q(4)]
    areas = [Q(1), Q(7, 3), Q(5), Q(11)]

    for gap in gaps:
        for c_zero in c_values:
            for c_one in c_values:
                c = [c_zero, c_one]
                z = c_zero * c_one - 1
                relative_factor = 1 + 2 * z
                inverse_scales = [
                    gap / (2 * c_zero * z),
                    gap / (2 * c_one * z),
                ]
                for orientation in (0, 1):
                    own = c[orientation]
                    other = c[1 - orientation]
                    hessian = [
                        [
                            (own - Q(1, 2 * other)) / gap,
                            -Q(1, 2 * other * gap),
                        ],
                        [
                            -Q(1, 2 * other * gap),
                            (own - Q(1, 2 * other)) / gap,
                        ],
                    ]
                    inverse_hessian = inv2(hessian)
                    expected_inverse = [
                        [
                            inverse_scales[orientation] * relative_factor,
                            inverse_scales[orientation],
                        ],
                        [
                            inverse_scales[orientation],
                            inverse_scales[orientation] * relative_factor,
                        ],
                    ]
                    require(
                        inverse_hessian == expected_inverse,
                        "hessian_inverse",
                    )

                    difference_moment = (
                        inverse_hessian[0][0]
                        + inverse_hessian[1][1]
                        - 2 * inverse_hessian[0][1]
                    ) / 3
                    sum_moment = (
                        inverse_hessian[0][0]
                        + inverse_hessian[1][1]
                        + 2 * inverse_hessian[0][1]
                    ) / 3
                    require(
                        difference_moment == 2 * gap / (3 * own),
                        "beta",
                    )
                    require(
                        sum_moment == 2 * gap / (3 * (own - 1 / other)),
                        "beta_plus",
                    )
                    require(
                        2 / (3 * difference_moment) - 1 / gap
                        == (own - 1) / gap,
                        "kappa_recovery",
                    )

                for area in areas:
                    # Avoid square roots by checking the square of the area formula.
                    alpha_squared = Q(
                        1,
                        16 * area * area * c_zero * c_one * z,
                    )
                    require(
                        Q(1, 16 * alpha_squared * c_zero * c_one * z)
                        == area * area,
                        "area_recovery_squared",
                    )

                    # Determinant of (T0,beta0,beta1,alpha) with alpha divided out.
                    diagonal_product = (
                        2
                        * (-2 * gap * gap / (3 * c_zero * c_zero))
                        * (-2 * gap * gap / (3 * c_one * c_one))
                        * (-1 / area)
                    )
                    require(
                        diagonal_product
                        == -8
                        * gap**4
                        / (9 * area * c_zero * c_zero * c_one * c_one),
                        "leading_jacobian_over_alpha",
                    )


def arclength_checks() -> None:
    # Insert arbitrary exact lower coefficients in psi'. Independently expand
    # psi'/sqrt(1+psi'^2) and differentiate the arclength integral with respect
    # to the degree-r graph coefficient.
    for seed in range(1, 10):
        curvature = Q(seed + 2, seed + 1)
        for degree in range(3, 17):
            order = degree + 4
            derivative_of_graph = [Q(0)] * (order + 1)
            derivative_of_graph[1] = curvature
            for power in range(2, order + 1):
                derivative_of_graph[power] = Q(
                    ((-1) ** (power + seed)) * (seed + 2 * power),
                    factorial(power),
                )

            square = series_multiply(
                derivative_of_graph,
                derivative_of_graph,
                order,
            )
            inverse_square_root = one_plus_series_power(square, Q(-1, 2), order)
            amplitude = series_multiply(
                derivative_of_graph,
                inverse_square_root,
                order,
            )

            arclength_variation = [Q(0)] * (order + 2)
            for power in range(order + 1):
                resulting_degree = power + degree
                if resulting_degree <= order + 1:
                    arclength_variation[resulting_degree] += amplitude[power] / (
                        factorial(degree - 1) * resulting_degree
                    )

            require(
                all(
                    arclength_variation[index] == 0
                    for index in range(degree + 1)
                ),
                "arc_variation_vanish",
            )
            require(
                arclength_variation[degree + 1]
                == curvature / Q((degree + 1) * factorial(degree - 1)),
                "arc_variation_lead",
            )

            square_root = one_plus_series_power(square, Q(1, 2), order)
            require(
                square_root[2] / 3 == curvature * curvature / 6,
                "arc_cubic",
            )


def network_checks() -> None:
    # Four invertible integer markings, including nonunimodular examples.
    markings = [
        [[Q(1), Q(0)], [Q(0), Q(1)]],
        [[Q(2), Q(1)], [Q(0), Q(3)]],
        [[Q(-1), Q(2)], [Q(2), Q(1)]],
        [[Q(3), Q(-1)], [Q(1), Q(2)]],
    ]

    # Forty-eight exact shear values: the observed first period and covolume
    # stay fixed while the unobserved second direction varies.
    shears = [Q(index - 24, 101) for index in range(48)]
    for shear in shears:
        lattice = [[Q(3), shear], [Q(0), Q(4)]]
        require(det2(lattice) == 12, "covolume")
        require(
            lattice[0][0] == 3 and lattice[1][0] == 0,
            "observed_period_fixed",
        )
        for marking in markings:
            displacements = mul2(lattice, marking)
            require(
                mul2(displacements, inv2(marking)) == lattice,
                "lattice_recovery",
            )
            require(
                det2(displacements) == det2(lattice) * det2(marking),
                "lattice_det",
            )

    for shear in [Q(1, 5), Q(1, 4), Q(1, 3), Q(1, 2)]:
        independent_squared_lengths = []
        for first_coefficient in range(-5, 6):
            for second_coefficient in range(-5, 6):
                if second_coefficient == 0:
                    continue
                independent_squared_lengths.append(
                    (3 * first_coefficient + shear * second_coefficient) ** 2
                    + (4 * second_coefficient) ** 2
                )
        require(
            min(independent_squared_lengths) > 16,
            "shear_shortest_independent",
        )

    # A three-vertex spanning-tree gauge and two independent fundamental cycles.
    gauge = [(0, 0), (2, 1), (1, 3)]
    edges = [
        (0, 1, (2, 1)),
        (1, 2, (-1, 2)),
        (2, 0, (0, -3)),
        (2, 0, (-1, -1)),
    ]
    transformed = [
        (
            label[0] + gauge[source][0] - gauge[target][0],
            label[1] + gauge[source][1] - gauge[target][1],
        )
        for source, target, label in edges
    ]
    require(transformed[0] == (0, 0), "tree_gauge")
    require(transformed[1] == (0, 0), "tree_gauge")
    require(transformed[2] == (1, 0), "cycle_labels")
    require(transformed[3] == (0, 2), "cycle_labels")


def dimension_and_symmetry_checks() -> None:
    for maximum_degree in range(3, 51):
        even_count = maximum_degree // 2 - 1
        odd_count = (maximum_degree - 1) // 2
        require(
            even_count + odd_count == maximum_degree - 2,
            "jet_count",
        )
        require(
            4 + 2 * (even_count + odd_count) == 2 * maximum_degree,
            "calibrated_dimension",
        )
        require(
            2 * even_count + 2 * odd_count == 2 * maximum_degree - 4,
            "fixed_window_count",
        )
        require(
            (2 * even_count + 1) + 2 * odd_count
            == 2 * maximum_degree - 3,
            "free_window_count",
        )

    for order in range(2, 31):
        domain_dimension = 2 * (2 * order - 2)
        count_constraints = 2 * (order - 1)
        require(
            domain_dimension - count_constraints == 2 * order - 2,
            "count_fiber_dimension",
        )

    for degree in range(3, 31):
        reflection_sign = Q(-1) ** degree
        require(
            reflection_sign * reflection_sign == 1
            and (
                reflection_sign == -1
                if degree % 2
                else reflection_sign == 1
            ),
            "reflection_parity",
        )


def main() -> None:
    calibration_checks()
    arclength_checks()
    network_checks()
    dimension_and_symmetry_checks()
    result = {
        "schema": "a2-v16-independent-review-diagnostics-1",
        "reviewed_commit": REVIEWED_COMMIT,
        "reviewed_tree": REVIEWED_TREE,
        "status": "passed",
        "checks": dict(sorted(CHECKS.items())),
        "total_checks": sum(CHECKS.values()),
        "scope": (
            "Finite exact calibration algebra, formal arclength coefficients, "
            "registered-lattice linear algebra, dimensions and reflection parity only"
        ),
        "imports_author_code": False,
        "formal_proof_certificate": False,
        "full_tex_build": False,
        "editorial_decision": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
