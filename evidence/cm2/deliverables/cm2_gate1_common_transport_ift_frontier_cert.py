#!/usr/bin/env python3
"""Common-plaque transport reduction for the coupled Gate-1 equations."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from typing import Any


Q = Fraction
HERE = Path(__file__).resolve().parent

DEPENDENCIES = {
    "cm2-gate1-biprojective-half-density-frontier-manifest-2026-07-17.json": (
        "6c6e8465161a64785ae07b3bd7a229820c93bacd9d07a2cd10c4691686722d6b"
    ),
}

Vector = tuple[Q, Q]
Matrix = tuple[tuple[Q, Q], tuple[Q, Q]]


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def wedge(left: Vector, right: Vector) -> Q:
    return left[0] * right[1] - left[1] * right[0]


def determinant(value: Matrix) -> Q:
    return value[0][0] * value[1][1] - value[0][1] * value[1][0]


def matrix_multiply(left: Matrix, right: Matrix) -> Matrix:
    return (
        (
            left[0][0] * right[0][0] + left[0][1] * right[1][0],
            left[0][0] * right[0][1] + left[0][1] * right[1][1],
        ),
        (
            left[1][0] * right[0][0] + left[1][1] * right[1][0],
            left[1][0] * right[0][1] + left[1][1] * right[1][1],
        ),
    )


def matrix_inverse(value: Matrix) -> Matrix:
    det = determinant(value)
    assert det != 0
    return (
        (value[1][1] / det, -value[0][1] / det),
        (-value[1][0] / det, value[0][0] / det),
    )


def matrix_vector(value: Matrix, vector: Vector) -> Vector:
    return (
        value[0][0] * vector[0] + value[0][1] * vector[1],
        value[1][0] * vector[0] + value[1][1] * vector[1],
    )


def matrix_from_anchor_images(
    anchor_1: Vector,
    anchor_2: Vector,
    image_1: Vector,
    image_2: Vector,
) -> Matrix:
    source: Matrix = (
        (anchor_1[0], anchor_2[0]),
        (anchor_1[1], anchor_2[1]),
    )
    target: Matrix = (
        (image_1[0], image_2[0]),
        (image_1[1], image_2[1]),
    )
    return matrix_multiply(target, matrix_inverse(source))


def load_dependencies() -> None:
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        assert path.is_file()
        assert sha256_path(path) == expected
        manifest = json.loads(path.read_text(encoding="utf-8"))
        assert manifest["verdict"]["biprojective_off_diagonal_cross_terms"] == (
            "ELIMINATED_EXACTLY"
        )
        assert manifest["verdict"]["coupled_half_density_groupoid_solution"] == (
            "NOT_CERTIFIED"
        )


def exact_column_replay() -> dict[str, Any]:
    ux, vx, sqrt_qx = Q(7, 8), Q(1, 2), Q(3, 4)
    uy, vy, sqrt_qy = Q(5, 8), Q(8, 9), Q(2, 3)
    ax = (1 / sqrt_qx, ux / sqrt_qx)
    ay = (1 / sqrt_qy, uy / sqrt_qy)
    bx = (vx / sqrt_qx, 1 / sqrt_qx)
    by = (vy / sqrt_qy, 1 / sqrt_qy)
    stable_coordinate = wedge(ax, ay)
    unstable_coordinate = wedge(by, bx)
    assert wedge(ax, bx) == wedge(ay, by) == 1
    assert stable_coordinate == (uy - ux) / (sqrt_qy * sqrt_qx)
    assert unstable_coordinate == (vy - vx) / (sqrt_qy * sqrt_qx)
    return {
        "determinant_one_frame_at_x": str(wedge(ax, bx)),
        "determinant_one_frame_at_y": str(wedge(ay, by)),
        "stable_half_density_is_first_column_wedge": str(stable_coordinate),
        "unstable_half_density_is_reversed_second_column_wedge": str(
            unstable_coordinate
        ),
        "stable_wedge_orientation": "det(a(x),a(y))=c_s(x,y)",
        "unstable_wedge_orientation": "det(b(y),b(x))=c_u(x,y)",
    }


def common_transport_replay() -> dict[str, Any]:
    vectors: tuple[Vector, ...] = (
        (Q(1), Q(0)),
        (Q(0), Q(1)),
        (Q(2), Q(3)),
        (Q(-1), Q(4)),
    )
    transport: Matrix = ((Q(2, 3), Q(1, 3)), (Q(1, 3), Q(2, 3)))
    ratio = determinant(transport)
    images = tuple(matrix_vector(transport, value) for value in vectors)
    for left, right in combinations(range(len(vectors)), 2):
        assert wedge(images[left], images[right]) == (
            ratio * wedge(vectors[left], vectors[right])
        )
    reconstructed = matrix_from_anchor_images(
        vectors[0], vectors[1], images[0], images[1]
    )
    assert reconstructed == transport
    assert all(
        matrix_vector(reconstructed, value) == image
        for value, image in zip(vectors, images, strict=True)
    )
    perturbed = list(images)
    perturbed[3] = (perturbed[3][0] + Q(1, 100), perturbed[3][1])
    failed_pairs = [
        [left, right]
        for left, right in combinations(range(len(vectors)), 2)
        if wedge(perturbed[left], perturbed[right])
        != ratio * wedge(vectors[left], vectors[right])
    ]
    assert failed_pairs
    assert matrix_vector(reconstructed, vectors[3]) != perturbed[3]
    return {
        "plaque_point_count": len(vectors),
        "common_transport_matrix": [
            [str(entry) for entry in row] for row in transport
        ],
        "common_transport_determinant": str(ratio),
        "all_pair_wedges_scale_by_common_determinant": True,
        "two_noncollinear_anchor_images_reconstruct_unique_transport": True,
        "all_other_images_forced_by_anchor_wedge_data": True,
        "perturbed_nontransport_image_breaks_pair_equations": True,
        "failed_pair_indices_after_perturbation": failed_pairs,
    }


def half_density_small_amplitude_audit() -> dict[str, Any]:
    epsilon = Q(1, 10)
    square = epsilon * epsilon
    fourth = square * square
    source_product = (1 - square) * (1 - 2 * square)
    shifted_product = (1 - 3 * square) * (1 - 5 * square)
    product_difference = shifted_product - source_product
    assert product_difference == -5 * square + 13 * fourth
    assert source_product > 0 and shifted_product > 0
    assert product_difference != 0

    critical_ratio = Q(1, 16)
    plaque_rate = Q(1, 2)
    amplitude = Q(1, 100)
    amplification_ratio = plaque_rate / critical_ratio
    normalized_at_8 = amplitude**3 * amplification_ratio**8
    assert amplification_ratio == 8
    assert normalized_at_8 > 1
    return {
        "sample_epsilon": str(epsilon),
        "source_q_product": str(source_product),
        "shifted_q_product": str(shifted_product),
        "exact_product_mismatch": str(product_difference),
        "half_density_factor_is_generically_not_one": True,
        "first_epsilon_derivative_at_zero": "0",
        "first_generic_scalar_coupling_order": "epsilon^2",
        "critical_equation_residual_after_multiplying_du": "epsilon^3",
        "amplitude_alone_does_not_change_decay_exponent_model": {
            "critical_ratio_r": str(critical_ratio),
            "plaque_residual_rate_theta": str(plaque_rate),
            "theta_over_r": str(amplification_ratio),
            "normalized_residual_formula": "epsilon^3*(theta/r)^n",
            "epsilon": str(amplitude),
            "normalized_residual_at_n=8": str(normalized_at_8),
            "diverges_for_every_nonzero_epsilon_when_theta_over_r_gt_1": True,
        },
        "model_is_not_an_obstruction_for_every_possible_physical_gauge": True,
    }


def structural_reduction() -> dict[str, Any]:
    return {
        "frame_columns": (
            "a=q^-1/2(1,u)^T, b=q^-1/2(v,1)^T, det(a,b)=1"
        ),
        "stable_pair_equation": (
            "det(a(sigma x),a(sigma y))="
            "r(x)det(a(x),a(y)) on each stable plaque"
        ),
        "unstable_pair_equation": (
            "the time-reversed common-determinant equation for b on each "
            "unstable plaque"
        ),
        "anchor_lemma": (
            "if one plaque contains two noncollinear a-columns, all pair "
            "equations are equivalent to a unique common linear transport "
            "M_s carrying every a(x) to a(sigma x), with det(M_s)=r"
        ),
        "symmetric_unstable_anchor_lemma": True,
        "new_unknowns_exposed": [
            "future-plaque common transports M_s",
            "past-plaque common transports M_u",
            "one determinant-one frame [a,b] shared by both systems",
            "uniform q lower bound and selected twisting",
        ],
        "shortest_constructive_route": (
            "solve the common-transport frame compatibility rather than "
            "independent scalar pair residuals"
        ),
    }


def literature_and_ift_audit() -> dict[str, Any]:
    return {
        "arxiv_api_checked_at": "2026-07-17",
        "butler_park_1909_11548": (
            "assumes convergence and Holder regularity of canonical "
            "holonomies; it does not construct this combined gauge"
        ),
        "kalinin_sadovskaya_2604_13401": (
            "Theorem 1.3 requires conjugate periodic data, a Holder periodic "
            "conjugacy at one periodic point, and sufficiently narrow "
            "periodic spectrum; those hypotheses are not installed here"
        ),
        "direct_nonfiber_bunched_half_density_solver_found": False,
        "plain_small_amplitude_ift_has_bounded_right_inverse_certified": False,
        "why_not": (
            "the all-pair range must satisfy common-plaque transport "
            "compatibility, while critical residual decay must beat diagonal "
            "amplification in the actual Holder or anisotropic norm"
        ),
        "rescues_that_would_be_sufficient": [
            "exact common-transport compatibility",
            "a proved bounded Green inverse in the chosen anisotropic norm",
            "true fiber bunching",
            "an exact support or cohomology identity making the residual zero",
        ],
    }


def build_result() -> dict[str, Any]:
    load_dependencies()
    result: dict[str, Any] = {
        "schema": "cm2.gate1.common-transport-ift-frontier.v1",
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
        },
        "exact_column_replay": exact_column_replay(),
        "common_transport_anchor_lemma_replay": common_transport_replay(),
        "small_amplitude_half_density_audit": half_density_small_amplitude_audit(),
        "structural_reduction": structural_reduction(),
        "literature_and_ift_audit": literature_and_ift_audit(),
        "strict_nonpromotion": {
            "small_amplitude_by_itself_closes_combined_class_H": False,
            "common_transport_reduction_supplies_physical_solution": False,
            "uniform_big_cell_q_lower_bound": "NOT_CERTIFIED",
            "coupled_half_density_groupoid_solution": "NOT_CERTIFIED",
            "same_representative_class_H_plus_twisting": "NOT_CERTIFIED",
            "Gate1": "NOT_CERTIFIED",
        },
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def main() -> None:
    print(json.dumps(build_result(), indent=2, sort_keys=True))
    print("COMMON_PLAQUE_TRANSPORT_REDUCTION: CERTIFIED")
    print("PLAIN_SMALL_AMPLITUDE_IFT_PROMOTION: REJECTED")
    print("COUPLED_HALF_DENSITY_SOLUTION: NOT_CERTIFIED")
    print("GATE1: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
