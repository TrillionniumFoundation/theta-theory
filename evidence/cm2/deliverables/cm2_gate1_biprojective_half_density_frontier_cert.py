#!/usr/bin/env python3
"""Biprojective half-density reformulation of the combined Gate-1 gauge.

The product of the separate lower and upper Green shears leaves a cubic
critical cross term. This certificate introduces the determinant-one gauge

    D(u,v)=(1-u*v)^(-1/2) [[1,v],[u,1]].

Its two off-diagonal relative coordinates are simultaneously the clean
differences dv and du. The noncommutative obstruction is transferred to a
scalar terminal half-density q^(-1/2), where q=1-u*v. The certificate derives
exact stable and unstable pair equations sufficient for one combined class-H
representative. No physical solution of those coupled equations is asserted.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


Q = Fraction
HERE = Path(__file__).resolve().parent

DEPENDENCIES = {
    "cm2-gate1-variable-diagonal-groupoid-frontier-manifest-2026-07-17.json": (
        "dacbae6255707086bc7486e4933d8c890ede1547a9e545995800a5fc18698f83"
    ),
    "cm2-gate1-global-coding-class-h-separation-frontier-manifest-2026-07-16.json": (
        "1e61f6f600300d15a15cf04179ee6e889ceb09edcf3d3b26f0d6f735afd6bdec"
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
    determinant_value = determinant(value)
    assert determinant_value != 0
    return (
        (value[1][1] / determinant_value, -value[0][1] / determinant_value),
        (-value[1][0] / determinant_value, value[0][0] / determinant_value),
    )


def determinant(value: Matrix) -> Q:
    return value[0][0] * value[1][1] - value[0][1] * value[1][0]


def biprojective(u: Q, v: Q, sqrt_q: Q) -> Matrix:
    q = 1 - u * v
    assert q == sqrt_q**2 and q > 0
    return (
        (1 / sqrt_q, v / sqrt_q),
        (u / sqrt_q, 1 / sqrt_q),
    )


def load_dependencies() -> dict[str, dict[str, Any]]:
    loaded: dict[str, dict[str, Any]] = {}
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        assert path.is_file()
        assert sha256_path(path) == expected
        value = json.loads(path.read_text(encoding="utf-8"))
        assert isinstance(value, dict)
        loaded[name] = value

    variable = loaded[
        "cm2-gate1-variable-diagonal-groupoid-frontier-manifest-2026-07-17.json"
    ]
    coding = loaded[
        "cm2-gate1-global-coding-class-h-separation-frontier-manifest-2026-07-16.json"
    ]
    assert variable["verdict"][
        "stable_variable_diagonal_groupoid_equation"
    ] == "SOLVED_SEPARATELY"
    assert variable["verdict"][
        "unstable_variable_diagonal_groupoid_equation"
    ] == "SOLVED_SEPARATELY"
    assert variable["verdict"]["combined_all_plaque_third_gauge"] == (
        "NOT_CERTIFIED"
    )
    assert coding["result"]["scope_limits"][
        "faithful_diagonal_class_H_representative_on_clean_horseshoe"
    ] is True
    return loaded


def exact_biprojective_replay() -> dict[str, Any]:
    ux, vx, sqrt_qx = Q(7, 8), Q(1, 2), Q(3, 4)
    uy, vy, sqrt_qy = Q(5, 8), Q(8, 9), Q(2, 3)
    qx = 1 - ux * vx
    qy = 1 - uy * vy
    dx = biprojective(ux, vx, sqrt_qx)
    dy = biprojective(uy, vy, sqrt_qy)
    relative = matrix_multiply(dy, matrix_inverse(dx))
    expected: Matrix = (
        (
            (1 - vy * ux) / (sqrt_qy * sqrt_qx),
            (vy - vx) / (sqrt_qy * sqrt_qx),
        ),
        (
            (uy - ux) / (sqrt_qy * sqrt_qx),
            (1 - uy * vx) / (sqrt_qy * sqrt_qx),
        ),
    )
    assert qx == Q(9, 16)
    assert qy == Q(4, 9)
    assert determinant(dx) == determinant(dy) == 1
    assert relative == expected
    return {
        "sample_x": {
            "u": str(ux), "v": str(vx), "q": str(qx),
            "sqrt_q": str(sqrt_qx),
        },
        "sample_y": {
            "u": str(uy), "v": str(vy), "q": str(qy),
            "sqrt_q": str(sqrt_qy),
        },
        "D_x_determinant": str(determinant(dx)),
        "D_y_determinant": str(determinant(dy)),
        "relative_matrix": [[str(value) for value in row] for row in relative],
        "exact_relative_formula": (
            "D_y D_x^-1=(q_y q_x)^-1/2"
            "[[1-v_y u_x,v_y-v_x],[u_y-u_x,1-u_y v_x]]"
        ),
        "upper_off_diagonal_is_clean_dv": True,
        "lower_off_diagonal_is_clean_du": True,
        "cubic_base_value_cross_terms_present": False,
    }


def canonical_limit_reduction() -> dict[str, Any]:
    return {
        "notation": {
            "q": "q(x)=1-u(x)v(x)",
            "R_n": "R_n(x)=product_{j=0}^{n-1} r(sigma^j x)",
            "R_minus_n": (
                "the time-reversed diagonal critical product in the common "
                "diagonal trivialisation"
            ),
        },
        "uniform_big_cell_requirement": (
            "q(x)>=q_*>0 on the entire finite clean SFT"
        ),
        "stable_pair_half_density_coordinate": (
            "c_s(x,y)=(u(y)-u(x))/sqrt(q(y)q(x))"
        ),
        "unstable_pair_half_density_coordinate": (
            "c_u(x,y)=(v(y)-v(x))/sqrt(q(y)q(x))"
        ),
        "exact_stable_pair_equation": (
            "u(sigma y)-u(sigma x)=r(x)"
            "sqrt(q(sigma y)q(sigma x)/(q(y)q(x)))"
            "[u(y)-u(x)]"
        ),
        "exact_unstable_pair_equation": (
            "v(sigma^-1 y)-v(sigma^-1 x)=R_minus_1(x)"
            "sqrt(q(sigma^-1 y)q(sigma^-1 x)/(q(y)q(x)))"
            "[v(y)-v(x)]"
        ),
        "iterated_stable_consequence": (
            "R_n(x)^-1 [u(sigma^n y)-u(sigma^n x)]/"
            "sqrt(q(sigma^n y)q(sigma^n x))=c_s(x,y)"
        ),
        "iterated_unstable_consequence": (
            "R_minus_n(x)^-1 [v(sigma^-n y)-v(sigma^-n x)]/"
            "sqrt(q(sigma^-n y)q(sigma^-n x))=c_u(x,y)"
        ),
        "stable_conjugated_relative_limit": "I+c_s(x,y)E_21",
        "unstable_conjugated_relative_limit": "I+c_u(x,y)E_12",
        "why_diagonal_entries_converge_to_one": (
            "on a local plaque the iterated endpoints coalesce, so the two "
            "diagonal numerators and the denominator approach q"
        ),
        "why_noncritical_off_diagonal_vanishes": (
            "the opposite off-diagonal is multiplied by the contracting "
            "diagonal ratio after conjugation"
        ),
        "sufficient_Holder_clause": (
            "q^-1, c_s and c_u are uniformly Holder on all local plaques; "
            "finite tails give the global families"
        ),
        "combined_class_H_if_all_clauses_hold": True,
    }


def comparison_with_shear_product() -> dict[str, Any]:
    return {
        "old_product_gauge": "D=U_v L_u",
        "old_unstable_cross_term": "-v_y(u_y-u_x)v_x",
        "new_biprojective_gauge": (
            "D=(1-uv)^-1/2[[1,v],[u,1]]"
        ),
        "new_off_diagonal_cross_term": "0 exactly",
        "new_scalar_terminal_factor": "(q_y q_x)^-1/2",
        "obstruction_removed": (
            "base-value cubic contamination of the critical off-diagonal"
        ),
        "obstruction_remaining": (
            "solve the coupled stable/unstable half-density groupoid "
            "equations with q=1-uv>=q_*>0"
        ),
        "this_is_an_equivalent_nonlinear_compatibility_target_not_a_solution": True,
    }


def build_result() -> dict[str, Any]:
    load_dependencies()
    result: dict[str, Any] = {
        "schema": "cm2.gate1.biprojective-half-density-frontier.v1",
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "technology_check": (
                "official arXiv abstracts for Butler-Park 1909.11548 and "
                "Kalinin-Sadovskaya 2604.13401 checked on 2026-07-17; no "
                "theorem supplies the coupled half-density solution"
            ),
            "old_artifacts_modified": False,
        },
        "exact_biprojective_algebra": exact_biprojective_replay(),
        "canonical_limit_reduction": canonical_limit_reduction(),
        "comparison_with_shear_product": comparison_with_shear_product(),
        "strict_nonpromotion": {
            "clean_off_diagonals_imply_half_density_equations_solved": False,
            "formal_sufficient_criterion_implies_actual_physical_solution": False,
            "uniform_big_cell_q_lower_bound": "NOT_CERTIFIED",
            "coupled_half_density_groupoid_solution": "NOT_CERTIFIED",
            "combined_all_plaque_class_H_representative": "NOT_CERTIFIED",
            "same_representative_class_H_plus_twisting": "NOT_CERTIFIED",
            "Gate1": "NOT_CERTIFIED",
        },
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def main() -> None:
    print(json.dumps(build_result(), indent=2, sort_keys=True))
    print("BIPROJECTIVE_OFF_DIAGONAL_CROSS_TERMS: ELIMINATED_EXACTLY")
    print("COUPLED_HALF_DENSITY_GROUPOID_EQUATIONS: NOT_CERTIFIED")
    print("GATE1: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
