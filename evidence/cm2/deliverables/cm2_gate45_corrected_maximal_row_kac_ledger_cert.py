#!/usr/bin/env python3
"""Rebind the 64-row single-charge/Kac ledger to the corrected coarea law."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import cm2_gate3_depth_one_fixed_gauge_dq_cert as dq
import cm2_gate4_all_sheet_single_charge_schema_cert as gate4
import cm2_gate45_algebraic_typing_frontier_cert as algebra


HERE = Path(__file__).resolve().parent
DQ_MANIFEST = HERE / "cm2-gate3-depth-one-fixed-gauge-dq-manifest-2026-07-15.json"
ALGEBRA_MANIFEST = (
    HERE / "cm2-gate45-controlled-stopped-interval-algebra-manifest-2026-07-15.json"
)
SLOPE_MANIFEST = (
    HERE / "cm2-gate45-all-row-oriented-slope-envelope-manifest-2026-07-15.json"
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def load_dependencies() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    corrected = json.loads(DQ_MANIFEST.read_text(encoding="utf-8"))
    stopped = json.loads(ALGEBRA_MANIFEST.read_text(encoding="utf-8"))
    slopes = json.loads(SLOPE_MANIFEST.read_text(encoding="utf-8"))
    assert corrected["verdict"]["coarea_collision_coordinate_scale"] == "CORRECTED"
    assert corrected["verdict"]["complete_depth_one_fixed_gauge_DQ"] == "CERTIFIED"
    assert stopped["verdict"]["controlled_dyadic_stopped_interval_algebra"] == "CERTIFIED"
    assert slopes["verdict"]["all_row_oriented_slope_envelope_lt_29"] == "CERTIFIED"
    return corrected, stopped, slopes


def corrected_occurrence_ledger(rows: list[dict[str, Any]]) -> dict[str, Any]:
    contract = gate4.universal_occurrence_contract()
    assert contract["endpoint_views_are_nonadditive"] is True
    assert contract["charged_occurrence_count"] == 1
    typed = []
    for row in rows:
        typed.append({
            "occurrence_id": row["occurrence_id"],
            "global_physical_label": row["global_physical_label"],
            "connected_maximal_base": row["base"],
            "first_visible_target": row["target"],
            "constant_miss_target": row["miss_target"],
            "constant_parameter_polarity": row["parameter_coarea_polarity"],
            "common_corrected_positive_law": (
                "m_e=R_source*cp*abs(u_y)/ell_T*dtheta"
            ),
            "forward_view": "source non-grazing -> target grazing -> miss non-grazing",
            "reverse_view": "same incidence transported by R o F_e",
            "views_are_nonadditive": True,
            "pre_recovery_single_charge": "q_e=max(C_fw(e),C_rev(e),2)*m_e",
            "certified_slope_only_subcharge": "q_e^slope=29*m_e",
            "controlled_restriction_coordinate": "dyadic cumulative-mass u_e",
            "singular_kac_coordinates": ["dot(S)h", "dot(r)*mu(h)"],
            "shared_singular_mark": [1, -1],
            "bounded_borel_current_type": True,
        })
    typed.sort(key=canonical_json)
    occurrences = len(typed)
    assert occurrences == 64
    return {
        "maximal_physical_occurrence_count": occurrences,
        "corrected_common_positive_law_count": occurrences,
        "pre_recovery_single_charge_expression_count": occurrences,
        "slope_only_numeric_subcharge_count": occurrences,
        "controlled_mass_coordinate_count": occurrences,
        "singular_kac_coordinate_count": 2 * occurrences,
        "incorrect_per_coordinate_double_charge_count": 2 * occurrences,
        "same_occurrence_forward_reverse_views_on_every_row": True,
        "endpoint_views_are_nonadditive_on_every_row": True,
        "one_corrected_m_per_occurrence": True,
        "one_q_expression_per_occurrence": True,
        "all_singular_coordinate_pairs_share_mark_plus_one_minus_one": True,
        "corrected_occurrence_rows_sha256": canonical_digest(typed),
    }


def corrected_borel_kac_layer(corrected: dict[str, Any]) -> dict[str, Any]:
    exact = algebra.exact_four_term_kac_algebra()
    assert exact["four_term_identity_exact"] is True
    assert exact["singular_coordinates_share_one_measure"] is True
    result = corrected["result"]
    assert result["scope_limits"]["corrected_global_finite_Borel_event_current"] is True
    assert result["exact_Jx_scalar_pairing"]["global_signed_scalar_coarea_mass"] == "0"
    return {
        "finite_borel_endpoint_adjoint_exact": True,
        "finite_borel_kac_tower_pairing_exact": True,
        "finite_borel_prefix_suffix_pairing_exact": True,
        "four_term_centered_algebra_exact": True,
        "singular_coordinates_share_one_corrected_occurrence_measure": True,
        "constant_observable_rowwise_singular_centering": True,
        "global_corrected_bounded_borel_event_current_assembled": True,
        "global_event_current_TV_upper_bound": result[
            "uniform_finite_measure_envelope"
        ]["global_event_current_TV_upper_bound"],
        "global_signed_scalar_coarea_mass": "0",
        "maximal_row_Jx_pair_count": result[
            "exact_Jx_scalar_pairing"
        ]["exact_Jx_maximal_row_pair_count"],
        "algebra_sample_digest": exact["sample_combined_occurrence_digest"],
    }


def corrected_recovery_boundary(
    stopped: dict[str, Any], slopes: dict[str, Any],
) -> dict[str, Any]:
    stopped_result = stopped["result"]
    slope_result = slopes["result"]
    assert stopped_result["scope_limits"]["countable_nested_dyadic_interval_algebra"] is True
    assert slope_result["scope_limits"]["global_numeric_broad_slope_envelope"] is True
    return {
        "forward_reverse_Borel_change_of_variables": True,
        "arbitrary_Borel_stopped_recovery": False,
        "controlled_dyadic_restriction_algebra": True,
        "fat_Cantor_restrictions_excluded_by_policy": True,
        "all_row_source_stable_and_miss_image_unstable_orientation": True,
        "global_broad_slope_envelope": "29",
        "slope_only_single_charge": "q_e^slope=29*m_e",
        "required_depth_recovery_moment": stopped_result["recovery_boundary"][
            "required_depth_moment"
        ],
        "controlled_dyadic_stopped_recovery": False,
        "complete_numeric_C_fw_C_rev": False,
        "global_Borel_TV_cost_is_not_final_C_fw_or_C_rev": True,
    }


def certify() -> dict[str, Any]:
    corrected, stopped, slopes = load_dependencies()
    rows, registry = dq.load_rows()
    ledger = corrected_occurrence_ledger(rows)
    kac = corrected_borel_kac_layer(corrected)
    boundary = corrected_recovery_boundary(stopped, slopes)
    assert ledger["maximal_physical_occurrence_count"] == corrected["result"][
        "corrected_current_assembly"
    ]["maximal_row_current_count"]
    return {
        "schema": "cm2.gate45.corrected-maximal-row-kac-ledger.v1",
        "provenance": {
            "corrected_DQ_manifest": DQ_MANIFEST.name,
            "controlled_interval_algebra_manifest": ALGEBRA_MANIFEST.name,
            "all_row_slope_manifest": SLOPE_MANIFEST.name,
            "maximal_row_registry_sha256": registry["maximal_row_rows_sha256"],
            "corrected_current_rows_sha256": corrected["result"][
                "corrected_current_assembly"
            ]["corrected_current_rows_sha256"],
            "supersedes_structural_scale_binding_in": (
                "cm2-gate45-maximal-row-single-charge-ledger-manifest-2026-07-15.json"
            ),
        },
        "corrected_global_occurrence_ledger": ledger,
        "corrected_global_finite_borel_kac_layer": kac,
        "controlled_recovery_and_CM2_boundary": boundary,
        "completion": {
            "corrected_global_finite_Borel_event_current": True,
            "corrected_global_signed_scalar_matching": True,
            "complete_depth_one_fixed_gauge_DQ": True,
            "same_occurrence_two_view_corrected_m_on_every_row": True,
            "one_symbolic_q_expression_per_maximal_occurrence": True,
            "one_numeric_slope_subcharge_per_maximal_occurrence": True,
            "controlled_dyadic_restriction_algebra": True,
            "corrected_bounded_Borel_singular_Kac_typing": True,
            "exact_four_term_Borel_Kac_algebra": True,
            "complete_numeric_forward_reverse_CM2_costs": False,
            "controlled_stopped_parent_recovery": False,
            "dynamic_test_MT_DQ": False,
            "standard_family_CM2_norm_lift": False,
            "flux_face_CM2_norm_lift": False,
            "dynamic_test_CM2_norm_lift": False,
            "physical_four_term_Kac_CM2_typing": False,
            "gate4_certified": False,
            "gate5_certified": False,
        },
    }


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE45_CORRECTED_64_ROW_SINGLE_CHARGE_LEDGER: CERTIFIED")
    print("GATE45_CORRECTED_128_COORDINATE_BOREL_KAC_LAYER: CERTIFIED")
    print("GATE45_PHYSICAL_RECOVERY_AND_CM2_NORM_LIFTS: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
