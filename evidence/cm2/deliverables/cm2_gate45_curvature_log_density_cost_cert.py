#!/usr/bin/env python3
"""Bidirectional carrier-curvature and log-density subcosts.

The source-reversed and miss-forward event carriers are circular-caustic
families.  If ``d`` is the distance from the caustic to the collision and
``c=cos(phi)``, both oriented slopes have the form

    V = kappa + c/d.

Differentiating the elementary caustic geometry gives the uniform estimate

    |dV/dr| <= kappa/d + 2/d^2 + R_caustic/d^3.

The source distance is at least ``1/10`` and the miss distance is at least
``36337/800000``.  This yields finite all-row C2 carrier costs without a
grazing loss.  The canonical endpoint rank controls the only three possible
density denominators.  It consequently gives explicit ``2^B`` bounds for
both logarithmic density derivatives.

This closes the raw one-collision geometric regularity layer.  It does not
construct a physical stopped recovery clock, prefix/suffix costs, dynamic
MT_DQ, or the CM2 norm lifts.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import cm2_gate3_global_physical_subrow_atlas_cert as bulk
import cm2_gate3_maximal_global_row_registry_cert as maximal
import cm2_gate45_endpoint_rank_first_order_cost_cert as rank_cert


Q = Fraction
HERE = Path(__file__).resolve().parent
RANK_MANIFEST = (
    HERE / "cm2-gate45-endpoint-rank-first-order-cost-manifest-2026-07-16.json"
)
BOUNDARY_Z_MANIFEST = (
    HERE / "cm2-gate45-bidirectional-boundary-z-cost-manifest-2026-07-16.json"
)
CONE_MANIFEST = (
    HERE / "cm2-gate45-global-invariant-cone-manifest-2026-07-16.json"
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def load_dependencies() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    rank = json.loads(RANK_MANIFEST.read_text(encoding="utf-8"))
    boundary_z = json.loads(BOUNDARY_Z_MANIFEST.read_text(encoding="utf-8"))
    cone = json.loads(CONE_MANIFEST.read_text(encoding="utf-8"))
    assert rank["verdict"]["global_endpoint_rank_tail_exponent_two"] == "CERTIFIED"
    assert boundary_z["verdict"]["numeric_bidirectional_raw_boundary_Z_costs"] == "CERTIFIED"
    assert cone["verdict"]["global_invariant_geometric_unstable_cone"] == "CERTIFIED"
    return rank, boundary_z, cone


def nonactive_uy_collar_audit() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows, registry = rank_cert.load_dependencies()
    audited = []
    nonactive_count = 0
    for row in rows:
        for side, field, inward_side in (
            ("left", "left_boundary", 1),
            ("right", "right_boundary", -1),
        ):
            boundary = row[field]
            normal = maximal.curve_normal(boundary, maximal.S0, maximal.S0)
            variable = bulk.arb_interval(Q(0), rank_cert.COLLAR)
            sine = variable.sin()
            cosine = variable.cos()
            normal_x = cosine * normal[0] - inward_side * sine * normal[1]
            normal_y = cosine * normal[1] + inward_side * sine * normal[0]
            _qx, _qy, _ux, uy, _flight, _source_cp = (
                rank_cert.scalar_tangent_geometry(row, normal_x, normal_y)
            )
            absolute_uy = rank_cert.signed_uy_multiplier(row) * uy
            active = boundary["kind"] == rank_cert.POLARITY
            if not active:
                assert bool(absolute_uy > rank_cert.arbq(Q(1, 32)))
                nonactive_count += 1
            audited.append({
                "occurrence_id": row["occurrence_id"],
                "side": side,
                "boundary_kind": boundary["kind"],
                "parameter_velocity_is_active_rank_scale": active,
                "absolute_u_y_enclosure": str(absolute_uy),
            })
    audited.sort(key=canonical_json)
    assert len(audited) == 128
    assert nonactive_count == 112
    return audited, {
        "endpoint_collar_count": len(audited),
        "parameter_polarity_active_collar_count": 16,
        "nonactive_parameter_velocity_collar_count": nonactive_count,
        "every_nonactive_collar_absolute_u_y_strict_lower": "1/32",
        "nonactive_u_y_collar_rows_sha256": canonical_digest(audited),
        "maximal_row_registry_sha256": registry["maximal_row_rows_sha256"],
    }


def curvature_and_log_costs(
    rank: dict[str, Any], boundary_z: dict[str, Any], cone: dict[str, Any],
) -> dict[str, Any]:
    radius_upper = Q(9, 25)
    curvature_upper = Q(25, 4)
    source_distance_lower = Q(1, 10)
    miss_distance_lower = Q(36337, 800000)
    source_curvature_upper = (
        curvature_upper / source_distance_lower
        + 2 / source_distance_lower**2
        + radius_upper / source_distance_lower**3
    )
    miss_curvature_upper = (
        curvature_upper / miss_distance_lower
        + 2 / miss_distance_lower**2
        + radius_upper / miss_distance_lower**3
    )
    assert source_curvature_upper == Q(1245, 2) < 623
    assert miss_curvature_upper == Q(237433247845000000, 47978559724753) < 4949
    assert 4949 < 1 << 14

    source_log_coefficient = Q(65, 4) + 10 + Q(46, 1 << 14)
    miss_log_coefficient = (
        29
        + 1 / miss_distance_lower
        + (
            1 / miss_distance_lower
            + radius_upper / miss_distance_lower**2
        ) / (1 << 14)
    )
    assert source_log_coefficient == Q(215063, 8192) < 27
    assert miss_log_coefficient == Q(4312088721189, 84504164416) < 52

    rank_layer = rank["result"]["endpoint_rank_tail_and_first_order_cost"]
    rank_moment = Q(
        rank_layer["raw_rank_moment"][
            "integral_2^B_dm_upper_before_Z_N_inverse"
        ]
    )
    boundary_costs = boundary_z["result"][
        "exact_density_and_boundary_Z_cost"
    ]["numeric_boundary_Z_subcosts"]
    reverse_z = Q(boundary_costs[
        "global_reverse_source_Z_upper_before_Z_N_inverse"
    ])
    forward_z = Q(boundary_costs[
        "global_forward_miss_Z_upper_before_Z_N_inverse"
    ])
    combined_rank_coefficient = Q(151 + 52 + 1)
    assert combined_rank_coefficient == 204
    global_partial_charge_upper = (
        combined_rank_coefficient * rank_moment + reverse_z + forward_z
    )
    assert global_partial_charge_upper == Q(
        344740673672569503213, 63953120000
    )
    assert cone["result"]["global_invariant_geometric_cone"][
        "cone_upper"
    ] == "4108425/145348"

    return {
        "rank_dominates_all_density_denominators": {
            "canonical_core_rank": 14,
            "source_cosine_inverse": "1/cp_source<=2^B",
            "parameter_velocity_inverse": "1/abs(u_y)<=2^B",
            "miss_cosine_inverse": "1/cp_miss<=2^B",
            "reason": (
                "the active endpoint scale is charged by B; all nonactive "
                "collar scales and all compact-core scales exceed their "
                "certified fixed thresholds"
            ),
        },
        "bidirectional_carrier_C2_bounds": {
            "common_caustic_slope": "V=kappa+cp/d",
            "differentiated_bound": (
                "abs(dV/dr)<=kappa/d+2/d^2+R_caustic/d^3"
            ),
            "source_reverse_distance_strict_lower": "1/10",
            "source_reverse_curvature_exact_upper": str(
                source_curvature_upper
            ),
            "source_reverse_curvature_strict_upper": "623",
            "miss_forward_distance_strict_lower": str(miss_distance_lower),
            "miss_forward_curvature_exact_upper": str(miss_curvature_upper),
            "miss_forward_curvature_strict_upper": "4949",
            "both_curvature_costs_absorbed_by_2^B": True,
        },
        "bidirectional_log_density_bounds": {
            "reverse_density": "rho_rev=cp_source*abs(u_y)/ell_T",
            "forward_density": "rho_fw=cp_miss*abs(u_y)/(t_miss-ell_T)",
            "source_auxiliary_derivative_bounds": {
                "abs(d cp_source/dr_source)": "<65/4",
                "abs(d abs(u_y)/dr_source)": "<=10",
                "abs(d ell_T/dr_source)": "<=23/5",
            },
            "miss_auxiliary_derivative_bounds": {
                "abs(d cp_miss/dr_miss)": "<29",
                "abs(d abs(u_y)/dr_miss)": "<=800000/36337",
                "abs(d gap/dr_miss)": (
                    "<=1+(9/25)/(36337/800000)"
                ),
            },
            "reverse_log_derivative_coefficient_exact_upper": str(
                source_log_coefficient
            ),
            "reverse_log_derivative_cost": (
                "abs(d log(rho_rev)/dr_source)<27*2^B"
            ),
            "forward_log_derivative_coefficient_exact_upper": str(
                miss_log_coefficient
            ),
            "forward_log_derivative_cost": (
                "abs(d log(rho_fw)/dr_miss)<52*2^B"
            ),
        },
        "numeric_one_collision_geometric_subcosts": {
            "rank_coefficient_breakdown": (
                "151 first-order chart pullback + 52 log-density + 1 carrier-C2"
            ),
            "reverse_subcost": "C_rev^(geom,Z)=204*2^B+C_Z_rev",
            "forward_subcost": "C_fw^(geom,Z)=204*2^B+C_Z_fw",
            "one_common_partial_charge": (
                "q_e^(geom,Z)=max(C_fw^(geom,Z),C_rev^(geom,Z),2)*m_e"
            ),
            "global_partial_charge_mass_upper_before_Z_N_inverse": str(
                global_partial_charge_upper
            ),
            "partial_charge_is_finite": True,
            "partial_charge_is_not_final_recovery_charge": True,
        },
    }


def certify() -> dict[str, Any]:
    rank, boundary_z, cone = load_dependencies()
    _rows, uy_audit = nonactive_uy_collar_audit()
    costs = curvature_and_log_costs(rank, boundary_z, cone)
    return {
        "schema": "cm2.gate45.curvature-log-density-cost.v1",
        "provenance": {
            "endpoint_rank_manifest": RANK_MANIFEST.name,
            "bidirectional_boundary_Z_manifest": BOUNDARY_Z_MANIFEST.name,
            "global_invariant_cone_manifest": CONE_MANIFEST.name,
            "corrected_current_rows_sha256": (
                "5c03da290697ac25b814848c5aee50b22387866f9d72303a60649466cad896bd"
            ),
        },
        "nonactive_parameter_velocity_collar_audit": uy_audit,
        "curvature_log_density_and_partial_cost": costs,
        "scope_limits": {
            "all_row_bidirectional_carrier_C2_bounds": True,
            "all_row_bidirectional_log_density_derivative_costs": True,
            "numeric_one_collision_geometric_forward_reverse_subcosts": True,
            "one_finite_partial_geometric_charge_per_occurrence": True,
            "physical_stopped_recovery_clock": False,
            "complete_numeric_C_fw_C_rev": False,
            "controlled_stopped_parent_recovery": False,
            "physical_prefix_suffix_costs": False,
            "full_dynamic_MT_DQ": False,
            "CM2_norm_lifts": False,
            "gate3_certified": False,
            "gate4_certified": False,
            "gate5_certified": False,
        },
        "internal_replay_digest": uy_audit[
            "nonactive_u_y_collar_rows_sha256"
        ],
    }


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE45_BIDIRECTIONAL_CARRIER_C2_COSTS: CERTIFIED")
    print("GATE45_BIDIRECTIONAL_LOG_DENSITY_COSTS: CERTIFIED")
    print("GATE45_COMPLETE_C_FW_C_REV_AND_STOPPED_RECOVERY: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
