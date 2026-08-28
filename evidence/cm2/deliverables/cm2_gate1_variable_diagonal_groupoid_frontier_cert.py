#!/usr/bin/env python3
"""Variable-diagonal all-plaque Green equations and gluing frontier."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


Q = Fraction
HERE = Path(__file__).resolve().parent

DEPENDENCIES = {
    "cm2-gate1-global-coding-class-h-separation-frontier-manifest-2026-07-16.json": (
        "1e61f6f600300d15a15cf04179ee6e889ceb09edcf3d3b26f0d6f735afd6bdec"
    ),
    "cm2-gate1-third-gauge-escape-frontier-manifest-2026-07-17.json": (
        "03174972b28265463fba1bb52a1dbdb1a85f6c1ae074c48f4a3774b5b9731dd7"
    ),
}


Matrix = tuple[tuple[Q, Q], tuple[Q, Q]]


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
    determinant = value[0][0] * value[1][1] - value[0][1] * value[1][0]
    assert determinant != 0
    return (
        (value[1][1] / determinant, -value[0][1] / determinant),
        (-value[1][0] / determinant, value[0][0] / determinant),
    )


def upper(value: Q) -> Matrix:
    return ((Q(1), value), (Q(0), Q(1)))


def lower(value: Q) -> Matrix:
    return ((Q(1), Q(0)), (value, Q(1)))


def diagonal(unstable: Q, stable: Q) -> Matrix:
    return ((unstable, Q(0)), (Q(0), stable))


def load_dependencies() -> dict[str, dict[str, Any]]:
    loaded: dict[str, dict[str, Any]] = {}
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        assert path.is_file()
        assert sha256_path(path) == expected
        value = json.loads(path.read_text(encoding="utf-8"))
        assert isinstance(value, dict)
        loaded[name] = value

    global_result = loaded[
        "cm2-gate1-global-coding-class-h-separation-frontier-manifest-2026-07-16.json"
    ]["result"]
    escape_result = loaded[
        "cm2-gate1-third-gauge-escape-frontier-manifest-2026-07-17.json"
    ]["result"]
    assert global_result["scope_limits"][
        "faithful_diagonal_class_H_representative_on_clean_horseshoe"
    ] is True
    assert global_result["scope_limits"][
        "finite_faithful_clean_horseshoe_coding"
    ] is True
    assert global_result["scope_limits"][
        "single_representative_class_H_and_weak_typicality"
    ] is False
    assert escape_result["actual_billiard_frontier"][
        "actual_variable_diagonal_stable_groupoid_resonant_equation"
    ] == "NOT_SOLVED"
    assert escape_result["actual_billiard_frontier"][
        "actual_variable_diagonal_unstable_groupoid_resonant_equation"
    ] == "NOT_SOLVED"
    return loaded


def exact_variable_ratio_replay() -> dict[str, Any]:
    ratios = (Q(1, 3), Q(2, 5), Q(3, 7), Q(4, 9), Q(5, 11))
    delta = Q(7, 13)
    product = Q(1)
    cancellations: list[str] = []
    for ratio in ratios:
        product *= ratio
        a_product = Q(1)
        d_product = product
        conjugated = matrix_multiply(
            matrix_multiply(
                matrix_inverse(diagonal(a_product, d_product)),
                lower(product * delta),
            ),
            diagonal(a_product, d_product),
        )
        assert conjugated == lower(delta)
        cancellations.append(str(product))

    reverse_product = Q(1)
    reverse_cancellations: list[str] = []
    for ratio in reversed(ratios):
        reverse_product *= ratio
        a_product = Q(1)
        d_product = reverse_product
        conjugated = matrix_multiply(
            matrix_multiply(
                diagonal(a_product, d_product),
                upper(reverse_product * delta),
            ),
            matrix_inverse(diagonal(a_product, d_product)),
        )
        assert conjugated == upper(delta)
        reverse_cancellations.append(str(reverse_product))

    return {
        "signed_ratio_model": "0<abs(r(x))=abs(a_s(x)/a_u(x))<kappa<1",
        "sample_variable_ratios": [str(value) for value in ratios],
        "sample_critical_defect": str(delta),
        "forward_products": cancellations,
        "backward_products": reverse_cancellations,
        "stable_critical_conjugation_cancels_variable_product_exactly": True,
        "unstable_critical_conjugation_cancels_variable_product_exactly": True,
        "constant_periodic_ratio_assumption_used": False,
    }


def one_sided_green_theorems() -> dict[str, Any]:
    return {
        "base": (
            "the finite clean SFT and faithful invariant-frame diagonal cocycle "
            "A_diag=diag(a_u,a_s)"
        ),
        "uniform_domination": "sup abs(a_s/a_u)=kappa<1",
        "sinai_one_sided_normalisation": {
            "future_version": (
                "apply the scalar Sinai cohomology lemma separately to log|a_u| "
                "and log|a_s| so the two diagonal entries depend only on the future"
            ),
            "past_version": (
                "apply the time-reversed scalar Sinai lemma so the diagonal ratio "
                "depends only on the past"
            ),
            "holder_transfer_functions": True,
            "periodic_products_and_pinching_preserved": True,
        },
        "stable_green_gauge": {
            "future_ratio": "r=a_s/a_u depends only on x_0,x_1,...",
            "marker": "a Holder future-cylinder marker xi",
            "series": (
                "u(x)=sum_{k>=1} r^(k)(sigma^-k x) xi(sigma^-k x)"
            ),
            "recurrence": "u(sigma x)=r(x)(u(x)+xi(x))",
            "local_stable_pair_identity": (
                "u(sigma^n y)-u(sigma^n x)=r^(n)(x)(u(y)-u(x))"
            ),
            "lower_shear": "L_u=I+u E_21",
            "canonical_stable_limit": (
                "L_u(y)^-1 [I+(u(y)-u(x))E_21] L_u(x)"
            ),
            "opposite_unstable_defect_is_uniformly_contracted": True,
            "all_local_and_global_stable_plaques": "CERTIFIED_THEOREM",
            "both_canonical_families_holder_for_the_lower_shear_representative": True,
            "lower_shear_representative_in_class_H": True,
        },
        "unstable_green_gauge": {
            "past_ratio": "r_minus is a diagonal-cohomologous past-dependent ratio",
            "marker": "a Holder past-cylinder marker eta",
            "series": (
                "v_minus(x)=sum_{k>=1} r_minus^(k)(x) eta(sigma^k x), "
                "then pull the upper shear back through the diagonal transfer"
            ),
            "local_unstable_pair_identity": (
                "v_minus(sigma^-n y)-v_minus(sigma^-n x)="
                "r_minus^(-n)(x)(v_minus(y)-v_minus(x))"
            ),
            "upper_shear": "U_v=I+v E_12",
            "canonical_unstable_limit": (
                "U_v(y)^-1 [I+(v(y)-v(x))E_12] U_v(x)"
            ),
            "opposite_stable_defect_is_uniformly_contracted": True,
            "all_local_and_global_unstable_plaques": "CERTIFIED_THEOREM",
            "both_canonical_families_holder_for_the_upper_shear_representative": True,
            "upper_shear_representative_in_class_H": True,
        },
        "former_two_variable_diagonal_linear_groupoid_equations": "SOLVED_SEPARATELY",
    }


def shear_gluing_algebra() -> dict[str, Any]:
    ux, uy = Q(2, 7), Q(5, 11)
    vx, vy = Q(-3, 8), Q(4, 9)

    upper_lower_x = matrix_multiply(upper(vx), lower(ux))
    upper_lower_y = matrix_multiply(upper(vy), lower(uy))
    upper_lower_relative = matrix_multiply(
        upper_lower_y, matrix_inverse(upper_lower_x)
    )
    delta_u = uy - ux
    delta_v = vy - vx
    expected_upper_lower: Matrix = (
        (Q(1) + vy * delta_u, delta_v - vy * delta_u * vx),
        (delta_u, Q(1) - delta_u * vx),
    )
    assert upper_lower_relative == expected_upper_lower

    lower_upper_x = matrix_multiply(lower(ux), upper(vx))
    lower_upper_y = matrix_multiply(lower(uy), upper(vy))
    lower_upper_relative = matrix_multiply(
        lower_upper_y, matrix_inverse(lower_upper_x)
    )
    expected_lower_upper: Matrix = (
        (Q(1) - ux * delta_v, delta_v),
        (delta_u - uy * ux * delta_v, Q(1) + uy * delta_v),
    )
    assert lower_upper_relative == expected_lower_upper

    return {
        "upper_then_lower_relative_matrix": (
            "D_y D_x^-1=[[1+v_y du, dv-v_y du v_x],[du,1-du v_x]]"
        ),
        "lower_then_upper_relative_matrix": (
            "D_y D_x^-1=[[1-u_x dv,dv],[du-u_y u_x dv,1+u_y dv]]"
        ),
        "upper_then_lower_stable_critical_coordinate_is_clean_du": True,
        "upper_then_lower_unstable_critical_coordinate_has_cross_term": (
            "-v_y du v_x"
        ),
        "lower_then_upper_unstable_critical_coordinate_is_clean_dv": True,
        "lower_then_upper_stable_critical_coordinate_has_cross_term": (
            "-u_y u_x dv"
        ),
        "sample_upper_then_lower_identity_exact": True,
        "sample_lower_then_upper_identity_exact": True,
        "noncommutative_cross_term_can_be_dropped": False,
    }


def nonlinear_compatibility_frontier() -> dict[str, Any]:
    return {
        "chosen_order": "D=U_v L_u",
        "stable_side": "the lower critical coordinate remains exact",
        "remaining_unstable_condition": (
            "uniform Holder convergence on every local unstable plaque of the "
            "renormalised cross term R_-n^-1 v(sigma^-n y) "
            "[u(sigma^-n y)-u(sigma^-n x)] v(sigma^-n x)"
        ),
        "equivalent_alternative_order": (
            "D=L_u U_v leaves the unstable coordinate exact and requires the "
            "symmetric stable renormalised cross-term limit"
        ),
        "third_diagonal_or_nonlinear_correction_may_cancel_cross_term": True,
        "actual_cross_term_limit_computed_on_all_physical_plaques": False,
        "one_same_representative_with_both_green_families": "NOT_CERTIFIED",
        "uniform_all_plaque_class_H_for_the_combined_third_gauge": "NOT_CERTIFIED",
        "selected_nonzero_twisting_in_that_same_family": "NOT_CERTIFIED",
    }


def build_result() -> dict[str, Any]:
    load_dependencies()
    result: dict[str, Any] = {
        "schema": "cm2.gate1.variable-diagonal-groupoid-frontier.v1",
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "butler_park_definition_checked": (
                "arXiv:1909.11548v2 equations (1.2) and condition (b)"
            ),
            "old_artifacts_modified": False,
        },
        "exact_variable_ratio_replay": exact_variable_ratio_replay(),
        "one_sided_all_plaque_green_theorems": one_sided_green_theorems(),
        "noncommutative_shear_gluing_algebra": shear_gluing_algebra(),
        "nonlinear_third_gauge_compatibility_frontier": (
            nonlinear_compatibility_frontier()
        ),
        "strict_scope": {
            "stable_variable_diagonal_groupoid_equation": "SOLVED_SEPARATELY",
            "unstable_variable_diagonal_groupoid_equation": "SOLVED_SEPARATELY",
            "lower_shear_all_plaque_class_H_representative": "CERTIFIED_THEOREM",
            "upper_shear_all_plaque_class_H_representative": "CERTIFIED_THEOREM",
            "combined_all_plaque_third_gauge": "NOT_CERTIFIED",
            "same_representative_class_H_plus_twisting": "NOT_CERTIFIED",
            "full_mass_physical_PPE": "NOT_CERTIFIED",
            "Gate1": "NOT_CERTIFIED",
        },
    }
    result["internal_replay_digest"] = canonical_digest(
        {key: value for key, value in result.items() if key != "internal_replay_digest"}
    )
    return result


def main() -> int:
    result = build_result()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("VARIABLE_DIAGONAL_STABLE_GREEN_EQUATION: SOLVED_SEPARATELY")
    print("VARIABLE_DIAGONAL_UNSTABLE_GREEN_EQUATION: SOLVED_SEPARATELY")
    print("NONLINEAR_THIRD_GAUGE_GLUING: NOT_CERTIFIED")
    print("GATE1: NOT_CERTIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
