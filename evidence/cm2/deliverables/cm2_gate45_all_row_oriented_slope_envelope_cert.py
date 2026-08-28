#!/usr/bin/env python3
"""Exact all-row source/image slope orientation and crude numeric envelope.

For a source curve whose outgoing rays are tangent to the selected target,
differentiating the tangency equation gives

    dphi_source/dr_source = -kappa_source - cp_source/ell_T.

At the first strict miss collision, reflection changes the corresponding
reversed stable slope into

    dphi_miss/dr_miss = kappa_miss + cp_miss/(t_miss-ell_T).

The global disk separation margin and the physical horizon give a uniform
positive lower bound for the tangent-to-miss gap.  Thus every one of the 64
rows is stable-oriented at the source and unstable-oriented at the miss
image, with an exact common broad slope envelope strictly below 29.

This is a geometric slope cost, not a proper-standard-family recovery cost.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

import cm2_gate3_depth_one_fixed_gauge_dq_cert as dq
import cm2_gate3_global_physical_subrow_atlas_cert as bulk


Q = Fraction
HERE = Path(__file__).resolve().parent
ALGEBRA_MANIFEST = (
    HERE / "cm2-gate45-controlled-stopped-interval-algebra-manifest-2026-07-15.json"
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def global_disk_separation() -> dict[str, Any]:
    gg = Q(1) - (2 * bulk.R["G"]) ** 2
    ww = Q(1) - (2 * bulk.R["W"]) ** 2
    cross_center_squared = Q(199, 400) ** 2 + Q(1, 2) ** 2
    gw = cross_center_squared - (bulk.R["G"] + bulk.R["W"]) ** 2
    assert gg == Q(301, 625)
    assert ww == Q(561, 625)
    assert gw == Q(36337, 160000)
    margin = min(gg, ww, gw)
    assert margin == gw

    maximum_radius_sum = 2 * bulk.R["G"]
    assert maximum_radius_sum == Q(18, 25)
    # Both physical boundary points lie before time 3 on the same ray.
    # Therefore D_centres <= 3+R_1+R_2 and
    # D_centres+(R_1+R_2) < 3+2*(18/25) < 5.
    center_plus_radius_sum_upper = Q(5)
    boundary_gap_lower = margin / center_plus_radius_sum_upper
    assert boundary_gap_lower == Q(36337, 800000)
    return {
        "same_G_squared_separation_margin": str(gg),
        "same_W_squared_separation_margin": str(ww),
        "cross_colour_squared_separation_margin": str(gw),
        "global_squared_separation_margin": str(margin),
        "physical_center_distance_plus_radius_sum_strict_upper": str(
            center_plus_radius_sum_upper
        ),
        "tangent_to_miss_boundary_gap_strict_lower": str(boundary_gap_lower),
    }


def slope_bounds(separation: dict[str, Any]) -> dict[str, Any]:
    kappa_min = min(1 / bulk.R["G"], 1 / bulk.R["W"])
    kappa_max = max(1 / bulk.R["G"], 1 / bulk.R["W"])
    tangent_flight_lower = Q(1, 10)
    miss_gap_lower = Q(separation["tangent_to_miss_boundary_gap_strict_lower"])
    source_abs_upper = kappa_max + 1 / tangent_flight_lower
    miss_upper = kappa_max + 1 / miss_gap_lower
    assert kappa_min == Q(25, 9)
    assert kappa_max == Q(25, 4)
    assert source_abs_upper == Q(65, 4) < 17
    assert miss_upper == Q(4108425, 145348) < 29
    common = Q(29)
    return {
        "curvature_min": str(kappa_min),
        "curvature_max": str(kappa_max),
        "target_tangent_flight_strict_lower": str(tangent_flight_lower),
        "tangent_to_miss_gap_strict_lower": str(miss_gap_lower),
        "exact_source_slope_formula": (
            "dphi_source/dr_source=-kappa_source-cp_source/ell_T"
        ),
        "exact_miss_image_slope_formula": (
            "dphi_miss/dr_miss=kappa_miss+cp_miss/(t_miss-ell_T)"
        ),
        "source_slope_interval": "(-65/4,-25/9)",
        "miss_image_slope_interval": "(25/9,4108425/145348)",
        "source_absolute_slope_strict_upper": str(source_abs_upper),
        "miss_image_slope_strict_upper": str(miss_upper),
        "common_broad_oriented_slope_envelope": str(common),
        "stable_source_orientation": True,
        "unstable_miss_image_orientation": True,
    }


def all_row_slope_contracts(bounds: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows, registry = dq.load_rows()
    contracts = []
    obstacle_pairs = Counter()
    for row in rows:
        source = row["source"]
        miss = row["miss_target"]
        miss_obstacle = bulk.TARGET_BY_ID[miss].obstacle
        obstacle_pairs[(source, miss_obstacle)] += 1
        contracts.append({
            "occurrence_id": row["occurrence_id"],
            "source_obstacle": source,
            "miss_target": miss,
            "miss_obstacle": miss_obstacle,
            "source_curvature": str(1 / bulk.R[source]),
            "miss_curvature": str(1 / bulk.R[miss_obstacle]),
            "source_carrier_orientation": "stable",
            "miss_image_carrier_orientation": "unstable",
            "source_slope_formula": bounds["exact_source_slope_formula"],
            "miss_image_slope_formula": bounds[
                "exact_miss_image_slope_formula"
            ],
            "common_absolute_slope_envelope": bounds[
                "common_broad_oriented_slope_envelope"
            ],
        })
    contracts.sort(key=canonical_json)
    assert len(contracts) == 64
    assert len({row["occurrence_id"] for row in contracts}) == 64
    return contracts, {
        "maximal_row_count": len(contracts),
        "all_source_carriers_stable_oriented": True,
        "all_miss_image_carriers_unstable_oriented": True,
        "all_raw_slopes_strictly_bounded_by": bounds[
            "common_broad_oriented_slope_envelope"
        ],
        "source_miss_obstacle_pair_counts": {
            f"{left}->{right}": count
            for (left, right), count in sorted(obstacle_pairs.items())
        },
        "row_slope_contracts_sha256": canonical_digest(contracts),
        "maximal_row_registry_sha256": registry["maximal_row_rows_sha256"],
    }


def slope_only_charge(bounds: dict[str, Any]) -> dict[str, Any]:
    common = Q(bounds["common_broad_oriented_slope_envelope"])
    positive_mass_upper = Q(8064, 5)
    slope_charge_mass_upper = common * positive_mass_upper
    slope_current_tv_upper = 2 * slope_charge_mass_upper
    assert slope_charge_mass_upper == Q(233856, 5)
    assert slope_current_tv_upper == Q(467712, 5)
    return {
        "slope_only_occurrence_envelope": "q_e^slope=29*m_e",
        "one_slope_charge_per_occurrence": True,
        "global_slope_charge_mass_upper_before_Z_N_inverse": str(
            slope_charge_mass_upper
        ),
        "global_slope_weighted_current_TV_upper_before_Z_N_inverse": str(
            slope_current_tv_upper
        ),
        "slope_only_charge_is_not_final_q": True,
    }


def remaining_cost_boundary() -> dict[str, Any]:
    return {
        "broad_orientation_is_not_invariant_standard_cone_typing": True,
        "compact_mass_trim_makes_each_fixed_row_cost_finite": True,
        "still_missing_numeric_costs": [
            "homogeneity-rank weighted curvature and second-derivative marks",
            "log-density and boundary-Z marks on every trimmed atom",
            "inverse-chart and physical-test pullback norms",
            "iterations needed to enter the fixed proper-family cone",
            "forward and reverse recovery-clock exponential moments",
        ],
        "numeric_C_fw_C_rev_complete": False,
        "controlled_stopped_recovery": False,
        "gate4_certified": False,
        "gate5_certified": False,
    }


def certify() -> dict[str, Any]:
    algebra = json.loads(ALGEBRA_MANIFEST.read_text(encoding="utf-8"))
    assert algebra["verdict"][
        "controlled_dyadic_stopped_interval_algebra"
    ] == "CERTIFIED"
    separation = global_disk_separation()
    bounds = slope_bounds(separation)
    contracts, audit = all_row_slope_contracts(bounds)
    charge = slope_only_charge(bounds)
    boundary = remaining_cost_boundary()
    return {
        "schema": "cm2.gate45.all-row-oriented-slope-envelope.v1",
        "provenance": {
            "controlled_interval_algebra_manifest": ALGEBRA_MANIFEST.name,
            "corrected_current_rows_sha256": (
                "5c03da290697ac25b814848c5aee50b22387866f9d72303a60649466cad896bd"
            ),
        },
        "global_disk_separation": separation,
        "exact_oriented_slope_bounds": bounds,
        "all_maximal_row_slope_audit": audit,
        "slope_only_single_charge": charge,
        "remaining_cost_boundary": boundary,
        "scope_limits": {
            "all_row_source_stable_orientation": True,
            "all_row_miss_image_unstable_orientation": True,
            "global_numeric_broad_slope_envelope": True,
            "one_numeric_slope_only_charge_per_occurrence": True,
            "proper_standard_family_cone_typing": False,
            "complete_numeric_C_fw_C_rev": False,
            "controlled_stopped_recovery": False,
            "CM2_norm_lifts": False,
            "gate4_certified": False,
            "gate5_certified": False,
        },
        "internal_replay_digest": canonical_digest(contracts),
    }


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE45_ALL_ROW_ORIENTED_SLOPE_ENVELOPE_LT_29: CERTIFIED")
    print("GATE45_SLOPE_ONLY_SINGLE_CHARGE_q_29m: CERTIFIED")
    print("GATE45_COMPLETE_C_FW_C_REV_AND_RECOVERY: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
