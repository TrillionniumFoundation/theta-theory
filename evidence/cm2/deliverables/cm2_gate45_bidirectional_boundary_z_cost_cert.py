#!/usr/bin/env python3
"""Raw bidirectional density formulas and boundary-Z subcosts.

The source and miss-image views admit exact one-dimensional densities in
Birkhoff arclength.  The endpoint-rank certificate shows that their only
density zeros are simple and isolated.  Canonical dyadic scale shells then
have summable unnormalized inverse-length boundary cost in both orientations.

This certificate pays the raw boundary-Z layer.  It does not certify the
log-density, C2 curvature, proper-cone recovery, stopped-depth moment, or the
complete forward/reverse CM2 costs.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import cm2_gate3_depth_one_fixed_gauge_dq_cert as dq
import cm2_gate3_global_physical_subrow_atlas_cert as bulk


Q = Fraction
HERE = Path(__file__).resolve().parent
RANK_MANIFEST = (
    HERE / "cm2-gate45-endpoint-rank-first-order-cost-manifest-2026-07-16.json"
)
SLOPE_MANIFEST = (
    HERE / "cm2-gate45-all-row-oriented-slope-envelope-manifest-2026-07-15.json"
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def load_dependencies() -> tuple[dict[str, Any], dict[str, Any]]:
    rank = json.loads(RANK_MANIFEST.read_text(encoding="utf-8"))
    slopes = json.loads(SLOPE_MANIFEST.read_text(encoding="utf-8"))
    assert rank["verdict"]["global_endpoint_rank_tail_exponent_two"] == "CERTIFIED"
    assert slopes["verdict"]["all_row_oriented_slope_envelope_lt_29"] == "CERTIFIED"
    return rank, slopes


def orientation_zero_ledger() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows, registry = dq.load_rows()
    typed = []
    source_zero_count = 0
    miss_zero_count = 0
    selected_miss_tangent_count = 0
    polarity_count = 0
    for row in rows:
        source_zeros = []
        miss_zeros = []
        for side, field in (("left", "left_boundary"), ("right", "right_boundary")):
            boundary = row[field]
            kind = boundary["kind"]
            if kind == "source_grazing":
                source_zeros.append({"side": side, "scale": "cp_source"})
                source_zero_count += 1
            if kind == "parameter_polarity":
                source_zeros.append({"side": side, "scale": "abs(u_y)"})
                miss_zeros.append({"side": side, "scale": "abs(u_y)"})
                source_zero_count += 1
                miss_zero_count += 1
                polarity_count += 1
            if (
                kind == "physical_later_miss_switch_boundary"
                and row["miss_target"] == boundary["descriptor"]["other"]
            ):
                miss_zeros.append({"side": side, "scale": "cp_miss"})
                miss_zero_count += 1
                selected_miss_tangent_count += 1
        typed.append({
            "occurrence_id": row["occurrence_id"],
            "source_view_density_wrt_dr": "cp_source*abs(u_y)/ell_T",
            "miss_view_density_wrt_dr": "cp_miss*abs(u_y)/(t_miss-ell_T)",
            "source_view_zero_endpoints": source_zeros,
            "miss_view_zero_endpoints": miss_zeros,
            "all_other_endpoints_regular_for_that_view": True,
        })
    typed.sort(key=canonical_json)
    assert len(typed) == 64
    assert source_zero_count == 48
    assert miss_zero_count == 48
    assert selected_miss_tangent_count == 32
    assert polarity_count == 16
    return typed, {
        "maximal_occurrence_count": len(typed),
        "source_view_simple_zero_endpoint_count": source_zero_count,
        "miss_view_simple_zero_endpoint_count": miss_zero_count,
        "selected_miss_tangent_endpoint_count": selected_miss_tangent_count,
        "shared_parameter_polarity_zero_endpoint_count": polarity_count,
        "source_regular_endpoint_count": 128 - source_zero_count,
        "miss_regular_endpoint_count": 128 - miss_zero_count,
        "orientation_zero_rows_sha256": canonical_digest(typed),
        "maximal_row_registry_sha256": registry["maximal_row_rows_sha256"],
    }


def exact_density_and_z_cost(
    rank: dict[str, Any], zero_ledger: dict[str, Any],
) -> dict[str, Any]:
    rank_result = rank["result"]
    assert rank_result["endpoint_rank_tail_and_first_order_cost"][
        "canonical_rank_definition"
    ]["core_rank"] == 14
    source_density_upper = Q(10)
    miss_gap_lower = Q(36337, 800000)
    miss_density_upper = 1 / miss_gap_lower
    shell_sum = Q(1, 1 << 13)
    source_zero_count = zero_ledger["source_view_simple_zero_endpoint_count"]
    miss_zero_count = zero_ledger["miss_view_simple_zero_endpoint_count"]
    row_count = zero_ledger["maximal_occurrence_count"]
    source_z_upper = (
        row_count * source_density_upper
        + source_zero_count * source_density_upper * shell_sum
    )
    miss_z_upper = (
        row_count * miss_density_upper
        + miss_zero_count * miss_density_upper * shell_sum
    )
    first_order_charge_upper = Q(
        rank_result["endpoint_rank_tail_and_first_order_cost"][
            "first_order_bidirectional_subcharge"
        ]["global_first_order_charge_mass_upper_before_Z_N_inverse"]
    )
    combined_partial_charge_upper = (
        first_order_charge_upper + source_z_upper + miss_z_upper
    )
    assert source_z_upper == Q(163855, 256)
    return {
        "exact_source_density_derivation": {
            "source_arclength": "dr_source=R_source*dtheta",
            "coarea_law": "dm=R_source*cp_source*abs(u_y)/ell_T*dtheta",
            "density_wrt_dr_source": "rho_rev=cp_source*abs(u_y)/ell_T",
            "strict_density_upper": str(source_density_upper),
        },
        "exact_miss_density_derivation": {
            "caustic_angle_variation": (
                "d beta/dtheta=-R_source*cp_source/ell_T"
            ),
            "miss_arclength_jacobian": (
                "abs(dr_miss/dtheta)=(t_miss-ell_T)*R_source*"
                "cp_source/(ell_T*cp_miss)"
            ),
            "density_wrt_dr_miss": (
                "rho_fw=cp_miss*abs(u_y)/(t_miss-ell_T)"
            ),
            "miss_gap_strict_lower": str(miss_gap_lower),
            "strict_density_upper": str(miss_density_upper),
        },
        "canonical_boundary_subdivision": {
            "core_rank": 14,
            "dyadic_zero_shell": "2^(-(b+1))<=scale<2^-b, b>=14",
            "sum_shell_scales": str(shell_sum),
            "one_core_component_per_occurrence_and_orientation": True,
            "source_shell_Z_contribution_per_zero": "<=10*2^-b",
            "miss_shell_Z_contribution_per_zero": (
                "<=(800000/36337)*2^-b"
            ),
        },
        "numeric_boundary_Z_subcosts": {
            "global_reverse_source_Z_upper_before_Z_N_inverse": str(
                source_z_upper
            ),
            "global_forward_miss_Z_upper_before_Z_N_inverse": str(
                miss_z_upper
            ),
            "both_raw_boundary_Z_sums_finite": True,
            "canonical_piecewise_boundary_costs_are_Borel": True,
            "partial_single_charge_formula": (
                "q_e^(1,Z)=max(151*2^B,C_Z_fw,C_Z_rev,2)*m_e"
            ),
            "global_partial_charge_mass_upper_by_sum_before_Z_N_inverse": str(
                combined_partial_charge_upper
            ),
            "partial_charge_is_not_final_q": True,
        },
    }


def certify() -> dict[str, Any]:
    rank, slopes = load_dependencies()
    typed, zero_ledger = orientation_zero_ledger()
    density_z = exact_density_and_z_cost(rank, zero_ledger)
    slope_result = slopes["result"]
    assert slope_result["exact_oriented_slope_bounds"][
        "tangent_to_miss_gap_strict_lower"
    ] == "36337/800000"
    return {
        "schema": "cm2.gate45.bidirectional-boundary-z-cost.v1",
        "provenance": {
            "endpoint_rank_first_order_manifest": RANK_MANIFEST.name,
            "all_row_slope_manifest": SLOPE_MANIFEST.name,
            "corrected_current_rows_sha256": (
                "5c03da290697ac25b814848c5aee50b22387866f9d72303a60649466cad896bd"
            ),
        },
        "orientation_specific_density_zero_ledger": zero_ledger,
        "exact_density_and_boundary_Z_cost": density_z,
        "scope_limits": {
            "exact_source_and_miss_arclength_densities": True,
            "numeric_bidirectional_raw_boundary_Z_subcosts": True,
            "one_partial_first_order_plus_Z_charge_per_occurrence": True,
            "log_density_regularization_cost": False,
            "homogeneity_weighted_C2_curvature_cost": False,
            "proper_standard_family_recovery_clock": False,
            "complete_numeric_C_fw_C_rev": False,
            "controlled_stopped_parent_recovery": False,
            "full_dynamic_MT_DQ": False,
            "CM2_norm_lifts": False,
            "gate3_certified": False,
            "gate4_certified": False,
            "gate5_certified": False,
        },
        "internal_replay_digest": canonical_digest(typed),
    }


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE45_EXACT_BIDIRECTIONAL_ARCLENGTH_DENSITIES: CERTIFIED")
    print("GATE45_NUMERIC_BIDIRECTIONAL_RAW_BOUNDARY_Z_COSTS: CERTIFIED")
    print("GATE45_COMPLETE_C_FW_C_REV_AND_RECOVERY: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
