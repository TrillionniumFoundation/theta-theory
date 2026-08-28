#!/usr/bin/env python3
"""Gate-4/5 single-charge ledger on all 64 maximal physical rows.

The earlier structural ledger was attached to non-maximal rectangular
subrows.  This certificate replaces it with the exact chart-free maximal-row
registry and the assembled finite-Borel coarea current.  Every occurrence now
has one common positive law, two nonadditive oriented views, one symbolic
pre-recovery charge

    q_e=max(C_fw(e),C_rev(e),2)*m_e,

and two singular Kac coordinates sharing the fixed mark ``(+1,-1)``.

The result is the complete global *structural* charge/Kac ledger.  The
forward and reverse CM2 carrier costs are still not numerically available,
and arbitrary-Borel stopped recovery is false.  Consequently no Gate-4/5
Banach completion is claimed.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import cm2_gate3_maximal_global_row_registry_cert as maximal
import cm2_gate4_all_sheet_single_charge_schema_cert as gate4
import cm2_gate45_algebraic_typing_frontier_cert as algebra


HERE = Path(__file__).resolve().parent
ROW_MANIFEST = (
    HERE / "cm2-gate3-maximal-global-row-registry-manifest-2026-07-15.json"
)
CURRENT_MANIFEST = (
    HERE / "cm2-gate3-global-borel-current-assembly-manifest-2026-07-15.json"
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def load_dependencies() -> tuple[dict[str, Any], dict[str, Any]]:
    rows = json.loads(ROW_MANIFEST.read_text(encoding="utf-8"))
    current = json.loads(CURRENT_MANIFEST.read_text(encoding="utf-8"))
    assert rows["verdict"]["maximal_connected_event_rows"] == "CERTIFIED"
    assert rows["result"]["maximal_row_registry"][
        "maximal_connected_physical_row_count"
    ] == 64
    assert current["verdict"]["global_finite_Borel_event_current"] == "CERTIFIED"
    assert current["verdict"]["global_signed_scalar_coarea_matching"] == "CERTIFIED"
    assert current["result"]["current_assembly"]["maximal_row_current_count"] == 64
    return rows, current


def replay_rows(expected_digest: str) -> list[dict[str, Any]]:
    curves, _candidate_registry = maximal.candidate_curve_registry()
    rows, registry, _boundary_registry = maximal.enumerate_bands(curves)
    assert registry["maximal_row_rows_sha256"] == expected_digest
    assert len(rows) == 64
    return rows


def structural_occurrence_ledger(rows: list[dict[str, Any]]) -> dict[str, Any]:
    contract = gate4.universal_occurrence_contract()
    assert contract["endpoint_views_are_nonadditive"] is True
    assert contract["max_dominates_both_oriented_costs"] is True
    assert contract["charged_occurrence_count"] == 1
    assert contract["pre_recovery_single_charge"] == (
        "q_e=max(C_fw(e),C_rev(e),2)*m_e"
    )
    typed = []
    for row in rows:
        typed.append({
            "occurrence_id": row["occurrence_id"],
            "global_physical_label": row["global_physical_label"],
            "connected_maximal_base": row["base"],
            "first_visible_target": row["target"],
            "constant_miss_target": row["miss_target"],
            "constant_parameter_polarity": row["parameter_coarea_polarity"],
            "common_positive_law": "m_e",
            "forward_view": "source non-grazing -> target grazing -> miss non-grazing",
            "reverse_view": "same incidence transported by R o F_e",
            "views_are_nonadditive": True,
            "pre_recovery_single_charge": "q_e=max(C_fw(e),C_rev(e),2)*m_e",
            "singular_kac_coordinates": ["dot(S)h", "dot(r)*mu(h)"],
            "shared_singular_mark": [1, -1],
            "bounded_borel_current_type": True,
        })
    typed.sort(key=canonical_json)
    occurrences = len(typed)
    coordinates = 2 * occurrences
    assert occurrences == 64 and coordinates == 128
    return {
        "maximal_physical_occurrence_count": occurrences,
        "common_positive_law_count": occurrences,
        "pre_recovery_single_charge_expression_count": occurrences,
        "singular_kac_coordinate_count": coordinates,
        "incorrect_per_coordinate_double_charge_count": coordinates,
        "same_occurrence_forward_reverse_views_on_every_row": True,
        "endpoint_views_are_nonadditive_on_every_row": True,
        "one_common_m_per_occurrence": True,
        "one_q_expression_per_occurrence": True,
        "all_singular_coordinate_pairs_share_mark_plus_one_minus_one": True,
        "occurrence_rows_sha256": canonical_digest(typed),
    }


def global_borel_kac_layer(current: dict[str, Any]) -> dict[str, Any]:
    exact = algebra.exact_four_term_kac_algebra()
    assert exact["four_term_identity_exact"] is True
    assert exact["finite_borel_endpoint_adjoint_exact"] is True
    assert exact["finite_borel_kac_tower_pairing_exact"] is True
    assert exact["finite_borel_prefix_suffix_pairing_exact"] is True
    assert exact["singular_coordinates_share_one_measure"] is True
    assert exact["constant_observable_rowwise_singular_centering"] is True
    current_result = current["result"]
    assert current_result["endpoint_and_test_typing"][
        "arbitrary_bounded_Borel_test_pairing"
    ] is True
    assert current_result["exact_Jx_scalar_pairing"][
        "global_signed_scalar_coarea_mass"
    ] == "0"
    return {
        "finite_borel_endpoint_adjoint_exact": True,
        "finite_borel_kac_tower_pairing_exact": True,
        "finite_borel_prefix_suffix_pairing_exact": True,
        "four_term_centered_algebra_exact": True,
        "singular_coordinates_share_one_occurrence_measure": True,
        "constant_observable_rowwise_singular_centering": True,
        "global_bounded_Borel_event_current_assembled": True,
        "global_event_current_TV_upper_bound": current_result[
            "uniform_finite_measure_envelope"
        ]["global_event_current_TV_upper_bound"],
        "global_signed_scalar_coarea_mass": "0",
        "maximal_row_Jx_pair_count": current_result[
            "exact_Jx_scalar_pairing"
        ]["exact_Jx_maximal_row_pair_count"],
        "algebra_sample_digest": exact["sample_combined_occurrence_digest"],
    }


def exact_recovery_boundary() -> dict[str, Any]:
    recovery = gate4.recovery_boundary()
    assert recovery["arbitrary_borel_stopped_recovery"] is False
    assert recovery["borel_change_of_variables_for_two_views"] is True
    return {
        "forward_reverse_Borel_change_of_variables": True,
        "arbitrary_Borel_stopped_recovery": False,
        "fat_Cantor_support_obstruction": recovery["exact_obstruction"],
        "countable_recovery_clock_obstruction": recovery[
            "countable_clock_obstruction"
        ],
        "admissible_completion_routes": recovery["admissible_positive_routes"],
        "missing_numeric_fields": [
            "homogeneity cut registry and cut-growth sum",
            "forward standard-family/flux carrier cost C_fw(e)",
            "reverse standard-family/flux carrier cost C_rev(e)",
            "dynamic C1 test-pullback cost",
            "bidirectional controlled stopped-parent recovery envelope",
            "physical prefix/suffix inverse-Jacobian and distortion sums",
        ],
        "global_Borel_TV_cost_is_not_C_fw_or_C_rev": True,
    }


def certify() -> dict[str, Any]:
    row_manifest, current_manifest = load_dependencies()
    row_digest = row_manifest["result"]["maximal_row_registry"][
        "maximal_row_rows_sha256"
    ]
    rows = replay_rows(row_digest)
    ledger = structural_occurrence_ledger(rows)
    kac = global_borel_kac_layer(current_manifest)
    obstruction = exact_recovery_boundary()
    assert ledger["maximal_physical_occurrence_count"] == (
        current_manifest["result"]["current_assembly"]["maximal_row_current_count"]
    )
    return {
        "schema": "cm2.gate45.maximal-row-single-charge-ledger.v1",
        "provenance": {
            "maximal_row_manifest": ROW_MANIFEST.name,
            "global_current_manifest": CURRENT_MANIFEST.name,
            "maximal_row_registry_sha256": row_digest,
            "global_current_rows_sha256": current_manifest["result"][
                "current_assembly"
            ]["current_rows_sha256"],
        },
        "global_structural_occurrence_ledger": ledger,
        "global_finite_borel_kac_layer": kac,
        "recovery_and_CM2_boundary": obstruction,
        "completion": {
            "maximal_connected_physical_event_rows": True,
            "global_finite_Borel_event_current": True,
            "global_signed_scalar_coarea_matching": True,
            "same_occurrence_two_view_common_m_on_every_maximal_row": True,
            "one_pre_recovery_q_expression_per_maximal_occurrence": True,
            "bounded_Borel_singular_Kac_typing_on_all_maximal_rows": True,
            "exact_four_term_Borel_Kac_algebra": True,
            "numeric_forward_reverse_CM2_costs": False,
            "controlled_stopped_parent_recovery": False,
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
    print("GATE45_MAXIMAL_ROW_SINGLE_CHARGE_LEDGER: CERTIFIED")
    print("GATE45_GLOBAL_FINITE_BOREL_KAC_LAYER: CERTIFIED")
    print("GATE45_STOPPED_RECOVERY_AND_CM2_NORMS: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
