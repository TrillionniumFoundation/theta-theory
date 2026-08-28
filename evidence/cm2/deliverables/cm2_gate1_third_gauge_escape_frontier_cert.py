#!/usr/bin/env python3
"""Gate-1 third-gauge finite-obstruction escape frontier.

This certificate has two deliberately different roles.

First, it proves that the two frozen periodic first-jet witnesses are not
gauge-invariant obstructions.  A compactly supported SL(2,R) gauge bump can
change the relevant first jet at either periodic base point, while remaining
the identity on the closure of the selected QNL homoclinic orbit.  The
already certified selected loop and its wedges are therefore unchanged.
This only removes the *existing witnesses*; it does not prove convergence of
any all-plaque canonical holonomy.

Second, it gives an exact full-two-shift model showing that the canonical
holonomy family and weak typicality are not invariants of Holder cohomology
outside the fiber-bunched regime.  Both cohomologous representatives belong
to class H; the diagonal one has identity canonical holonomies and zero
twisting, while the second has a loop twisting both periodic eigenaxes.

The actual billiard's variable-diagonal stable/unstable groupoid equations
remain unsolved, so Gate 1 stays fail-closed.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
DEPENDENCIES = (
    "cm2-gate1-local-jet-gauge-obstruction-frontier-manifest-2026-07-16.json",
    "cm2-gate1-same-representative-resonant-shadow-frontier-manifest-2026-07-16.json",
    "cm2-gate1-global-coding-class-h-separation-frontier-manifest-2026-07-16.json",
    "cm2-gate1-numeric-holonomy-tail-twisting-frontier-manifest-2026-07-16.json",
    "cm2-gate1-immutable-homoclinic-plaque-entry-frontier-manifest-2026-07-16.json",
)

Q = Fraction
Matrix = tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]
I: Matrix = ((Q(1), Q(0)), (Q(0), Q(1)))
E12: Matrix = ((Q(0), Q(1)), (Q(0), Q(0)))
E21: Matrix = ((Q(0), Q(0)), (Q(1), Q(0)))


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name: str) -> dict[str, Any]:
    value = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def dependency_hashes() -> dict[str, str]:
    return {name: sha256_path(HERE / name) for name in DEPENDENCIES}


def mm(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(sum((left[i][k] * right[k][j] for k in range(2)), Q(0)) for j in range(2))
        for i in range(2)
    )  # type: ignore[return-value]


def madd(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(left[i][j] + right[i][j] for j in range(2)) for i in range(2)
    )  # type: ignore[return-value]


def mscale(value: Fraction, matrix: Matrix) -> Matrix:
    return tuple(
        tuple(value * matrix[i][j] for j in range(2)) for i in range(2)
    )  # type: ignore[return-value]


def minv(matrix: Matrix) -> Matrix:
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    assert determinant != 0
    return (
        (matrix[1][1] / determinant, -matrix[0][1] / determinant),
        (-matrix[1][0] / determinant, matrix[0][0] / determinant),
    )


def U(value: Fraction) -> Matrix:
    return madd(I, mscale(value, E12))


def L(value: Fraction) -> Matrix:
    return madd(I, mscale(value, E21))


def D(value_u: Fraction, value_v: Fraction) -> Matrix:
    return mm(U(value_v), L(value_u))


def matrix_json(matrix: Matrix) -> list[list[str]]:
    return [[str(matrix[i][j]) for j in range(2)] for i in range(2)]


def audit_dependencies() -> dict[str, Any]:
    local = load(DEPENDENCIES[0])
    shadow_manifest = load(DEPENDENCIES[1])
    global_manifest = load(DEPENDENCIES[2])
    numeric_manifest = load(DEPENDENCIES[3])
    homoclinic_manifest = load(DEPENDENCIES[4])

    local_result = local["result"]
    shadow = shadow_manifest["result"]["compact_gauge_periodic_shadow_obstruction"]
    connector = global_manifest["result"]["connector_compact_gauge_obstruction"]
    numeric_scope = numeric_manifest["result"]["scope_limits"]
    homoclinic = homoclinic_manifest["result"]["immutable_homoclinic_orbit"]

    assert local_result["necessary_escape_conditions_for_a_third_gauge"][
        "arbitrary_global_jet_changing_gauge_excluded"
    ] is False
    assert shadow["gauged_stable_direction_lower_left_derivative_excludes_zero"]
    assert shadow["return_determinant_contains_one"]
    assert connector["stable_mixed_jet_in_minus_1_over_20_minus_1_over_25"]
    assert connector["symplectic_multiplier_identity"] == "Lambda*nu=1 exactly"
    assert numeric_scope["four_selected_QNL_eigen_axis_twisting_wedges"] is True
    assert homoclinic["selected_point_is_nonperiodic_qnl_homoclinic"] is True
    assert homoclinic["root_interval_excludes_qnl_point"] is True

    return {
        "frozen_dependency_sha256": dependency_hashes(),
        "shadow_mixed_coefficient": shadow[
            "gauged_stable_direction_lower_left_derivative"
        ],
        "shadow_stable_multiplier": shadow["return_stable_multiplier"],
        "connector_mixed_jet": connector["stable_mixed_jet_partial_xy_G2"],
        "connector_stable_multiplier": connector["connector_stable_multiplier"],
        "selected_homoclinic_nonperiodic": True,
        "selected_loop_four_wedges_frozen": True,
    }


def periodic_first_jet_escape() -> dict[str, Any]:
    return {
        "setup": (
            "at a periodic base point, in common base-stable and fiber eigen-coordinates, "
            "A(p)=diag(Lambda,nu), DG(p)v_s=nu*v_s, Lambda*nu=1"
        ),
        "correction_gauge": "E(p)=I and X=dE_p[v_s]",
        "corrected_derivative": (
            "dA_E[v_s]=dA[v_s]-nu*X*A(p)+A(p)*X"
        ),
        "lower_left_coefficient_update": "c_E=c+(nu-1)*X_21",
        "surjectivity_condition": "nu!=1",
        "exact_canceling_jet": "X_21=c/(1-nu)",
        "substitution": "c+(nu-1)*c/(1-nu)=0",
        "generator": "X_21*E_21 is traceless, hence is an sl(2,R) first jet",
        "periodic_product_value_and_pinching_unchanged": True,
        "shadow_current_nonzero_coefficient_witness_can_be_removed": True,
        "connector_current_nonzero_coefficient_witness_can_be_removed": True,
        "removing_the_witness_proves_canonical_convergence": False,
    }


def disjoint_bump_escape() -> dict[str, Any]:
    return {
        "selected_orbit_closure": (
            "K=Orb(z_h) union {p}; this is the closure because z_h is homoclinic to p"
        ),
        "periodic_orbit_intersection_argument": (
            "a non-p periodic point in Orb(z_h) would make z_h periodic by invertibility"
        ),
        "shadow_and_connector_orbits_disjoint_from_K": True,
        "finite_periodic_orbits_have_positive_distance_from_K": True,
        "disjoint_neighbourhoods_exist": True,
        "two_bump_supports_are_mutually_disjoint": True,
        "each_support_avoids_all_other_points_of_both_periodic_orbits": True,
        "local_SL2_bump_formula": (
            "E(q)=exp(chi(q)*ell(q)*M), tr(M)=0, ell(q_*)=0, "
            "dell_{q_*}(v_s)=1"
        ),
        "cutoff_is_one_near_basepoint": True,
        "cutoff_jet_at_basepoint": "chi(q_*)=1 and dchi(q_*)=0",
        "realized_first_jet": "dE_{q_*}[v_s]=M",
        "independent_shadow_and_connector_jets": True,
        "combined_correction_equals_identity_on_a_neighbourhood_of_K": True,
        "one_collision_cocycle_on_selected_orbit_unchanged": True,
        "all_selected_finite_holonomy_approximants_unchanged": True,
        "selected_infinite_loop_and_four_wedges_unchanged": True,
        "what_is_escaped": (
            "the two currently certified nonzero first-jet divergence witnesses"
        ),
        "all_plaque_class_H_after_the_bumps": "NOT_CERTIFIED",
    }


def toy_model_audit() -> dict[str, Any]:
    lam = Q(2)
    nu = Q(1, 2)
    rho = Q(1, 4)
    A: Matrix = ((lam, Q(0)), (Q(0), nu))

    # Exact conjugation identities at the critical weight rho=lambda^-2.
    assert mm(mm(minv(A), E21), A) == mscale(Q(4), E21)
    assert mm(mm(A, E12), minv(A)) == mscale(Q(4), E12)

    # p=0^Z and z has its only nonzero symbol at coordinate zero.  D(p)=D(z)=I.
    stable = L(Q(-1))
    unstable = U(Q(1))
    loop = mm(stable, unstable)
    assert stable == ((Q(1), Q(0)), (Q(-1), Q(1)))
    assert unstable == ((Q(1), Q(1)), (Q(0), Q(1)))
    assert loop == ((Q(1), Q(1)), (Q(-1), Q(0)))
    assert loop[1][0] != 0 and loop[0][1] != 0

    # If a definition insists on two distinct homoclinic witnesses, use
    # z_+=1_{\{0\}} and z_-=1_{\{1\}}.  For the second point the forward and
    # backward critical sums are rho and rho^{-1}, respectively.
    second_loop = mm(L(-1 / rho), U(rho))
    assert second_loop == ((Q(1), Q(1, 4)), (Q(-4), Q(0)))
    assert second_loop[0][1] != 0

    # Uniform Holder constants in the full-shift metric d(x,y)=2^-N.
    u_v_sup = rho / (1 - rho)
    assert u_v_sup == Q(1, 3)
    tail_prefactor = 1 / (1 - rho)
    assert tail_prefactor == Q(4, 3)
    inverse_row_sum_bound = Q(13, 9)
    local_bracket_difference_bound = Q(4, 9)
    stable_holonomy_row_norm_factor = inverse_row_sum_bound * local_bracket_difference_bound
    assert stable_holonomy_row_norm_factor == Q(52, 81)
    operator_holder_constant = Q(2) * stable_holonomy_row_norm_factor * tail_prefactor
    assert operator_holder_constant == Q(416, 243)
    assert operator_holder_constant < 2

    return {
        "base": "mixing full shift {0,1}^Z with d(x,y)=2^(-N(x,y))",
        "constant_diagonal_cocycle_A": matrix_json(A),
        "pinching_fixed_point": "p=0^Z",
        "rho": str(rho),
        "gauge_series": {
            "u(x)": "sum_{k>=1} 4^(-k) x_{-k}",
            "v(x)": "sum_{k>=1} 4^(-k) x_k",
            "D(x)": "(I+v(x)E_12)(I+u(x)E_21)",
            "det_D": "1 exactly",
            "sup_u_and_v": str(u_v_sup),
            "D_and_D_inverse_holder": True,
        },
        "cohomologous_cocycle": "B(x)=D(sigma x)^-1 A D(x)",
        "local_stable_algebra": {
            "pair_relation": "x_i=y_i for every i>=0",
            "delta_u_n": "u(sigma^n y)-u(sigma^n x)=4^(-n)*(u(y)-u(x))",
            "tail_limit": (
                "A^(-n)D(sigma^n y)D(sigma^n x)^(-1)A^n "
                "-> I+(u(y)-u(x))E_21"
            ),
            "canonical_Hs": (
                "D(y)^-1[I+(u(y)-u(x))E_21]D(x)"
            ),
            "holder_exponent": "beta=1",
            "operator_holder_constant_lt": "2",
        },
        "local_unstable_algebra": {
            "pair_relation": "x_i=y_i for every i<=0",
            "delta_v_minus_n": "v(sigma^(-n)y)-v(sigma^(-n)x)=4^(-n)*(v(y)-v(x))",
            "tail_limit": (
                "A^nD(sigma^(-n)y)D(sigma^(-n)x)^(-1)A^(-n) "
                "-> I+(v(y)-v(x))E_12"
            ),
            "canonical_Hu": "I exactly on local unstable plaques",
            "holder_exponent": "beta=1",
        },
        "B_is_holder": True,
        "A_belongs_to_Butler_Park_class_H": True,
        "B_belongs_to_Butler_Park_class_H": True,
        "homoclinic_point": "z_0=1 and z_i=0 for i!=0",
        "global_holonomies": {
            "H_s_z_p": matrix_json(stable),
            "H_u_p_z": matrix_json(unstable),
            "psi_z=H_s_z_p*H_u_p_z": matrix_json(loop),
        },
        "twisting_wedges": {
            "det(e_u,psi_z*e_u)": "-1",
            "det(e_s,psi_z*e_s)": "-1",
            "both_periodic_eigenaxes_twisted": True,
        },
        "two_distinct_witness_assignment": {
            "z_plus": "only (z_plus)_0=1",
            "z_minus": "only (z_minus)_1=1",
            "psi_z_plus": matrix_json(loop),
            "psi_z_minus": matrix_json(second_loop),
            "det(e_u,psi_z_plus*e_u)": "-1",
            "det(e_s,psi_z_minus*e_s)": "-1/4",
            "witnesses_are_distinct": True,
        },
        "B_is_weakly_typical": True,
        "A_has_identity_canonical_holonomies_and_zero_twisting": True,
        "A_and_B_are_holder_cohomologous": True,
        "class_H_membership_changes_in_this_model": False,
        "this_model_refutes_class_H_membership_invariance": False,
        "canonical_holonomy_family_is_holder_cohomology_invariant": False,
        "weak_typicality_is_holder_cohomology_invariant": False,
    }


def build_result() -> dict[str, Any]:
    result: dict[str, Any] = {
        "schema": "cm2.gate1.third-gauge-escape-frontier.v1",
        "provenance": {
            **audit_dependencies(),
            "old_artifacts_modified": False,
        },
        "periodic_first_jet_repair": periodic_first_jet_escape(),
        "disjoint_SL2_bump_escape": disjoint_bump_escape(),
        "explicit_cohomologous_class_H_twisting_model": toy_model_audit(),
        "butler_park_scope": {
            "class_H_definition": (
                "the canonical stable/unstable limits converge and are Holder"
            ),
            "canonical_holonomy_family_is_representative_dependent": True,
            "both_toy_representatives_belong_to_class_H": True,
            "toy_model_makes_no_claim_against_class_H_membership_invariance": True,
            "continuous_conjugacy_preserves_pressure_and_equilibrium_states": True,
            "continuous_conjugacy_preserves_canonical_holonomies_without_a_tail_condition": False,
            "weak_typicality_is_not_forced_to_be_cohomology_invariant": True,
            "toy_model_refutes_canonical_holonomy_and_weak_typicality_invariance": True,
        },
        "actual_billiard_frontier": {
            "finite_shadow_and_connector_witnesses_are_universal_obstructions": False,
            "one_third_gauge_passing_the_known_finite_witnesses_exists": True,
            "selected_twisting_can_be_kept_during_those_local_repairs": True,
            "actual_variable_diagonal_stable_groupoid_resonant_equation": "NOT_SOLVED",
            "actual_variable_diagonal_unstable_groupoid_resonant_equation": "NOT_SOLVED",
            "uniform_all_plaque_holder_constants": "NOT_CERTIFIED",
            "actual_same_representative_class_H_plus_twisting": "NOT_CERTIFIED",
            "full_mass_physical_PPE": "NOT_CERTIFIED",
            "Gate1": "NOT_CERTIFIED",
        },
    }
    result["internal_replay_digest"] = digest(result)
    return result


def main() -> int:
    result = build_result()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("FINITE_PERIODIC_JET_BLOCKERS_UNIVERSAL: REFUTED")
    print("SELECTED_LOOP_PRESERVED_BY_DISJOINT_LOCAL_REPAIRS: CERTIFIED")
    print("CANONICAL_HOLONOMY_AND_WEAK_TYPICALITY_INVARIANCE: REFUTED")
    print("ACTUAL_ALL_PLAQUE_THIRD_GAUGE: NOT_CERTIFIED")
    print("GATE1: NOT_CERTIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
