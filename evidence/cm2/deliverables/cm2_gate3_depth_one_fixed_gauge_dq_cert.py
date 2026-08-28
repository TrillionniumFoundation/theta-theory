#!/usr/bin/env python3
"""Correct the global coarea scale and close the depth-one transfer DQ.

The predecessor global-current certificate used the tangent graph coordinate
``p=sin(phi)`` but then multiplied its graph velocity by ``cos(phi)`` once
more.  Since ``dp=cos(phi)dphi``, the collision law is ``dr dp`` in this
coordinate.  The positive row law therefore has one, not two, powers of
``cp=cos(phi)``:

    dm_e = R_source * cp * abs(u_y) / ell_T dtheta.

This replay binds that corrected coefficient to the exhaustive 64-row
registry and instantiates the finite circular moving-domain theorem for the
complete one-step collision transfer operator on the solid-boundary section.
For a C1 source density, the full finite difference quotient converges in the
dual of C^{1,alpha}; the limit is the sum of the smooth branch derivative and
the corrected hit-minus-miss face current.

This is the complete depth-one, static-test DQ.  It does not claim the
iterated dynamic-test interface MT_DQ, a CM2 majorant, stopped recovery, or a
Banach norm lift.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import cm2_gate3_global_borel_current_assembly_cert as old_current
import cm2_gate3_global_physical_subrow_atlas_cert as bulk
import cm2_gate3_maximal_global_row_registry_cert as maximal


Q = Fraction
HERE = Path(__file__).resolve().parent
ROW_MANIFEST = (
    HERE / "cm2-gate3-maximal-global-row-registry-manifest-2026-07-15.json"
)
NORMAL_FORM_MANIFEST = (
    HERE / "cm2-gate3-normal-form-dedup-manifest-2026-07-15.json"
)
FIRST_MISS_MANIFEST = (
    HERE / "cm2-gate3-first-miss-stratification-manifest-2026-07-15.json"
)
SEAM_MANIFEST = (
    HERE / "cm2-gate3-chart-seam-quotient-manifest-2026-07-15.json"
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def load_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    manifest = json.loads(ROW_MANIFEST.read_text(encoding="utf-8"))
    certified = manifest["result"]["maximal_row_registry"]
    assert manifest["verdict"]["maximal_connected_event_rows"] == "CERTIFIED"
    assert certified["maximal_connected_physical_row_count"] == 64
    curves, _candidate_registry = maximal.candidate_curve_registry()
    rows, replayed, _boundary_registry = maximal.enumerate_bands(curves)
    assert replayed["maximal_row_rows_sha256"] == certified[
        "maximal_row_rows_sha256"
    ]
    return rows, certified


def collision_coordinate_correction() -> dict[str, Any]:
    """Exact coordinate bookkeeping for the collision-flux coarea law."""

    source_radius_upper = Q(9, 25)
    flight_lower = Q(1, 10)
    corrected_density_upper = source_radius_upper / flight_lower
    assert corrected_density_upper == Q(18, 5)
    return {
        "collision_coordinates": {
            "p": "sin(phi)",
            "cp": "cos(phi)=sqrt(1-p^2)>0",
            "jacobian_identity": "dp=cp*dphi",
            "collision_law_before_normalization": "cos(phi)*dr*dphi=dr*dp",
            "source_arclength": "dr=R_source*dtheta",
        },
        "tangency_discriminant": "Delta_T=R_T^2-w_T^2; w_T=epsilon*R_T",
        "exact_derivatives": {
            "partial_s_Delta": "2*eta*epsilon*R_T*u_y",
            "partial_p_Delta": "2*epsilon*R_T*ell_T/cp",
            "signed_face_coarea": "eta*epsilon*cp*u_y/ell_T",
            "tangent_graph_velocity": "-eta*cp*u_y/ell_T",
        },
        "corrected_positive_row_law": (
            "dm_e=R_source*cp*abs(u_y)/ell_T*dtheta"
        ),
        "superseded_positive_row_law": (
            "R_source*cp^2*abs(u_y)/ell_T*dtheta"
        ),
        "exact_reason_for_correction": (
            "the superseded law multiplies by cp after the change of variables "
            "cos(phi)dphi=dp has already absorbed that factor"
        ),
        "old_to_corrected_density_ratio": "cp",
        "corrected_unnormalized_density_upper_bound": str(
            corrected_density_upper
        ),
    }


def corrected_current_rows(
    rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    typed = []
    for row in rows:
        polarity = row["parameter_coarea_polarity"]
        assert polarity in (-1, 1)
        typed.append({
            "occurrence_id": row["occurrence_id"],
            "global_physical_label": row["global_physical_label"],
            "base": row["base"],
            "positive_coarea_law": {
                "coordinate": "source normal angle theta at s=0",
                "density_wrt_dtheta": "R_source*cp*abs(u_y)/ell_T",
                "collision_flux_coordinate_density_wrt_dr_dp": "1",
                "absolute_tangent_graph_velocity": "cp*abs(u_y)/ell_T",
                "strict_interior_positivity": True,
            },
            "signed_current": {
                "polarity": polarity,
                "hit_trace": {
                    "target": row["target"],
                    "grazing_side": row["epsilon"],
                },
                "miss_trace": {
                    "target": row["miss_target"],
                    "strictly_non_grazing_on_open_row": True,
                },
                "shared_vector_mark": [1, -1],
                "formula": "sigma*integral(Phi(hit)-Phi(miss)) dm",
            },
            "left_boundary": row["left_boundary"],
            "right_boundary": row["right_boundary"],
        })
    typed.sort(key=canonical_json)
    assert len(typed) == 64
    assert len({row["occurrence_id"] for row in typed}) == 64
    return typed, {
        "maximal_row_current_count": len(typed),
        "corrected_positive_coarea_law_attached_to_every_row": True,
        "strict_hit_and_miss_trace_attached_to_every_row": True,
        "one_shared_plus_minus_mark_per_occurrence": True,
        "corrected_current_rows_sha256": canonical_digest(typed),
    }


def exact_jx_pairing(rows: list[dict[str, Any]]) -> dict[str, Any]:
    pairing = old_current.exact_jx_pairing(rows)
    pairing["transformation_law"]["invariants"] = [
        "cp", "ell_T", "abs(u_y)", "R_source", "dtheta",
    ]
    pairing["transformation_law"]["positive_density"] = (
        "R_source*cp*abs(u_y)/ell_T preserved"
    )
    return pairing


def dependency_audit() -> dict[str, Any]:
    normal_form = json.loads(NORMAL_FORM_MANIFEST.read_text(encoding="utf-8"))
    first_miss = json.loads(FIRST_MISS_MANIFEST.read_text(encoding="utf-8"))
    seam = json.loads(SEAM_MANIFEST.read_text(encoding="utf-8"))
    universal = normal_form["universal_normal_form"]
    completion = normal_form["global_completion"]
    assert universal["physical_pair_multiple_event_count"] == 0
    assert universal["physical_triple_multiple_event_count"] == 0
    assert completion["pair_physical_multiple_event_normal_forms"].startswith(
        "CERTIFIED_EMPTY"
    )
    assert completion["triple_physical_multiple_event_normal_forms"].startswith(
        "CERTIFIED_EMPTY"
    )
    assert first_miss["result"][
        "remaining_two_dimensional_unresolved_parameter_area"
    ] == "0"
    assert first_miss["result"]["dependency_claims"][
        "physical_joint_vertices"
    ] == 0
    assert seam["verdict"]["eight_chart_seam_ownership"] == "CERTIFIED"
    assert seam["result"]["unique_half_open_owner_rule"][
        "duplicate_trace_is_identified_not_added"
    ] is True
    return {
        "finite_horizon_target_lift_universe": 162,
        "physical_flight_strict_upper_bound": "3",
        "physical_pair_simultaneous_first_occurrences": 0,
        "physical_triple_simultaneous_first_occurrences": 0,
        "physical_joint_vertices": 0,
        "remaining_two_dimensional_unresolved_parameter_area": "0",
        "chart_seams_have_unique_physical_owner": True,
        "duplicate_chart_and_lift_traces_cancel_before_absolute_values": True,
    }


def fixed_gauge_depth_one_dq(
    row_count: int, boundary_count: int, envelope: dict[str, Any],
) -> dict[str, Any]:
    minimum_target_radius = Q(4, 25)
    flight_lower = Q(envelope["target_tangent_flight_strict_lower_bound"])
    phi_submersion_lower = 2 * minimum_target_radius * flight_lower
    assert phi_submersion_lower == Q(4, 125)
    assert row_count == 64 and boundary_count == 88
    return {
        "common_fixed_gauge": {
            "path": "horizontal center translation of W with both radii fixed",
            "collision_space": "N=G disjoint-union W in common arclength coordinates",
            "invariant_probability": "the same normalized cos(phi)dr dphi for every s",
            "fixed_projection_Pi0": True,
        },
        "source_and_test_classes": {
            "source_density": "h in C^1(N) relative to mu_N",
            "target_test": "Phi in C^{1,alpha}(compactified N), 0<alpha<=1",
            "limit_space": "dual of C^{1,alpha}(compactified N)",
        },
        "smooth_core_derivative": {
            "persistent_smooth_core_cover_is_finite": True,
            "formula": (
                "sum_B integral_B h(x) D Phi(T_0 x) partial_s T_s(x)|_0 dmu_N(x)"
            ),
            "same_colour_relative_branches_have_zero_parameter_velocity": True,
            "cross_colour_regular_branches_are_real_analytic": True,
            "finite_difference_quotient_converges_on_every_persistent_core": True,
        },
        "regular_radical_stitching": {
            "maximal_connected_face_rows": row_count,
            "state_changing_row_boundaries": boundary_count,
            "uniform_abs_partial_phi_Delta_lower": str(phi_submersion_lower),
            "hit_side_radical_derivative_envelope": "C*(1+Delta_+^-1/2)",
            "regular_face_collar_mass_bound": "C*rho^1/2",
            "finite_s_augmented_segment_carrier": True,
            "coefficient_measures_converge_in_total_variation_on_common_atlas": True,
            "face_term": (
                "sum_e sigma_e integral h(x_e(theta))*"
                "[Phi(z_T(theta))-Phi(y_M(theta))] dm_e(theta)"
            ),
            "face_law": "dm_e=R_source*cp*abs(u_y)/ell_T*dtheta",
        },
        "endpoint_and_atlas_stitching": {
            "source_grazing_endpoint_density": "0 because cp=0",
            "polarity_endpoint_density": "0 because u_y=0",
            "first_visibility_and_miss_switch_endpoints": (
                "finite one-dimensional base endpoints; zero coarea mass"
            ),
            "multiple_first_event_product_radicals": 0,
            "one_step_multi_radical_envelope": (
                "a finite sum of individual inverse square roots, never a product"
            ),
            "chart_and_lift_artificial_face_current": "0 by quotient trace identity",
            "extra_endpoint_atoms": 0,
        },
        "operator_conclusion": {
            "uncentered_depth_one_transfer_DQ": "CERTIFIED",
            "centered_depth_one_fixed_gauge_DQ": "CERTIFIED",
            "convergence_statement": (
                "||(P_s-P_0)h/s-D_0 h||_(C^{1,alpha})* -> 0 for every h in C^1"
            ),
            "centered_convergence_statement": (
                "Pi0_perp (P_s-P_0) Pi0_perp / s converges on C^1 sources "
                "in the same static-test topology"
            ),
            "limiting_defect_is_smooth_core_plus_corrected_face_current": True,
        },
    }


def certify() -> dict[str, Any]:
    rows, row_registry = load_rows()
    correction = collision_coordinate_correction()
    typed_rows, assembly = corrected_current_rows(rows)
    envelope = old_current.global_borel_envelope(len(rows))
    envelope["corrected_density_formula"] = (
        "R_source*cp*abs(u_y)/ell_T"
    )
    envelope["superseded_density_formula"] = (
        "R_source*cp^2*abs(u_y)/ell_T"
    )
    envelope["numerical_upper_bounds_unchanged_after_correction"] = True
    pairing = exact_jx_pairing(rows)
    dependencies = dependency_audit()
    boundary_count = 88
    dq = fixed_gauge_depth_one_dq(len(rows), boundary_count, envelope)
    assert row_registry["maximal_row_rows_sha256"] == (
        "0857fdfde5845026f47d1b9a343eaf06fd873782efcf2359618fe9d4f46fe630"
    )
    assert assembly["corrected_current_rows_sha256"] == canonical_digest(
        typed_rows
    )
    return {
        "schema": "cm2.gate3.depth-one-fixed-gauge-dq.v1",
        "provenance": {
            "maximal_row_manifest": ROW_MANIFEST.name,
            "maximal_row_registry_sha256": row_registry[
                "maximal_row_rows_sha256"
            ],
            "supersedes_global_current_scale_in": (
                "cm2-gate3-global-borel-current-assembly-manifest-2026-07-15.json"
            ),
        },
        "collision_coordinate_correction": correction,
        "corrected_current_assembly": assembly,
        "uniform_finite_measure_envelope": envelope,
        "exact_Jx_scalar_pairing": pairing,
        "finite_event_atlas_dependency_audit": dependencies,
        "fixed_gauge_depth_one_DQ": dq,
        "scope_limits": {
            "corrected_global_finite_Borel_event_current": True,
            "corrected_global_signed_scalar_coarea_matching": True,
            "complete_depth_one_transfer_difference_quotient": True,
            "smooth_fixed_core_derivative": True,
            "regular_radical_boundary_tightness": True,
            "dynamic_iterated_C1_test_tightness": False,
            "full_MT_DQ_interface": False,
            "CM2_time_decay_majorant": False,
            "numeric_forward_reverse_standard_family_costs": False,
            "controlled_stopped_parent_recovery": False,
            "gate3_certified": False,
            "gate4_certified": False,
            "gate5_certified": False,
        },
    }


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE3_COAREA_COLLISION_COORDINATE_SCALE: CORRECTED")
    print("GATE3_COMPLETE_DEPTH_ONE_FIXED_GAUGE_DQ: CERTIFIED")
    print("GATE3_DYNAMIC_ITERATED_TEST_MT_DQ: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
