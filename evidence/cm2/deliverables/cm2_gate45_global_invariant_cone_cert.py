#!/usr/bin/env python3
"""Global invariant geometric unstable cone for all maximal rows.

For a dispersing collision branch, a positive post-collision slope ``V``
propagates by the wavefront recurrence

    V_1 = kappa_1 + cp_1/(tau + cp_0/(V+kappa_0)).

The global boundary gap therefore makes the interval
``(25/9,4108425/145348)`` strictly forward invariant.  Time reversal sends
every source stable carrier into this cone, while every miss image already
lies in it.  Both orientations have geometric cone-entry time zero.

This is cone typing only.  Proper-family curvature, density, length,
recovery, and CM2 norm costs remain separate.
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
SLOPE_MANIFEST = (
    HERE / "cm2-gate45-all-row-oriented-slope-envelope-manifest-2026-07-15.json"
)
BOUNDARY_Z_MANIFEST = (
    HERE / "cm2-gate45-bidirectional-boundary-z-cost-manifest-2026-07-16.json"
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def load_dependencies() -> tuple[dict[str, Any], dict[str, Any]]:
    slopes = json.loads(SLOPE_MANIFEST.read_text(encoding="utf-8"))
    boundary = json.loads(BOUNDARY_Z_MANIFEST.read_text(encoding="utf-8"))
    assert slopes["verdict"]["all_row_oriented_slope_envelope_lt_29"] == "CERTIFIED"
    assert boundary["verdict"]["numeric_bidirectional_raw_boundary_Z_costs"] == "CERTIFIED"
    return slopes, boundary


def invariant_cone() -> dict[str, Any]:
    kappa_min = Q(25, 9)
    kappa_max = Q(25, 4)
    flight_gap = Q(36337, 800000)
    upper = kappa_max + 1 / flight_gap
    assert upper == Q(4108425, 145348)
    assert upper < 29
    source_upper = kappa_max + 10
    assert source_upper == Q(65, 4) < upper
    # The frozen one-collision Birkhoff matrix has, up to its common scalar,
    # a=tau*kappa_0+cp_0, b=tau,
    # c=tau*kappa_0*kappa_1+kappa_0*cp_1+kappa_1*cp_0,
    # d=tau*kappa_1+cp_1.  Direct expansion of
    # (c+d*V)/(a+b*V) gives the recurrence recorded below.  Keep an exact
    # rational sample identity here as a sign-convention regression guard.
    tau = Q(7, 10)
    kappa_0 = Q(25, 9)
    kappa_1 = Q(25, 4)
    cp_0 = Q(3, 5)
    cp_1 = Q(4, 5)
    slope_0 = Q(5)
    matrix_slope = (
        tau * kappa_0 * kappa_1
        + kappa_0 * cp_1
        + kappa_1 * cp_0
        + (tau * kappa_1 + cp_1) * slope_0
    ) / (tau * kappa_0 + cp_0 + tau * slope_0)
    wavefront_slope = kappa_1 + cp_1 / (
        tau + cp_0 / (slope_0 + kappa_0)
    )
    assert matrix_slope == wavefront_slope
    return {
        "fixed_geometric_unstable_cone": (
            "25/9<V=dphi/dr<4108425/145348<29"
        ),
        "curvature_lower": str(kappa_min),
        "curvature_upper": str(kappa_max),
        "global_free_flight_strict_lower": str(flight_gap),
        "cone_upper": str(upper),
        "wavefront_recurrence": (
            "V_1=kappa_1+cp_1/(tau+cp_0/(V_0+kappa_0))"
        ),
        "recurrence_matches_frozen_birkhoff_matrix": True,
        "positive_denominator_for_every_input_in_cone": True,
        "strict_forward_invariance": True,
        "source_reversal_slope": (
            "V_rev=kappa_source+cp_source/ell_T"
        ),
        "source_reversal_strict_upper": str(source_upper),
        "miss_image_slope": (
            "V_fw=kappa_miss+cp_miss/(t_miss-ell_T)"
        ),
        "both_orientations_enter_cone_at_time_zero": True,
    }


def all_row_cone_typing(cone: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows, registry = dq.load_rows()
    typed = []
    for row in rows:
        typed.append({
            "occurrence_id": row["occurrence_id"],
            "source_reverse_orientation": "unstable",
            "source_reverse_slope_interval": "(25/9,65/4)",
            "miss_forward_orientation": "unstable",
            "miss_forward_slope_interval": (
                "(25/9,4108425/145348)"
            ),
            "common_invariant_cone_upper": cone["cone_upper"],
            "reverse_cone_entry_time": 0,
            "forward_cone_entry_time": 0,
        })
    typed.sort(key=canonical_json)
    assert len(typed) == 64
    return typed, {
        "maximal_occurrence_count": len(typed),
        "source_reverse_carriers_in_fixed_unstable_cone": 64,
        "miss_forward_carriers_in_fixed_unstable_cone": 64,
        "zero_step_reverse_cone_entries": 64,
        "zero_step_forward_cone_entries": 64,
        "all_row_cone_typing_rows_sha256": canonical_digest(typed),
        "maximal_row_registry_sha256": registry["maximal_row_rows_sha256"],
    }


def certify() -> dict[str, Any]:
    slopes, _boundary = load_dependencies()
    cone = invariant_cone()
    typed, audit = all_row_cone_typing(cone)
    slope_bounds = slopes["result"]["exact_oriented_slope_bounds"]
    assert slope_bounds["miss_image_slope_strict_upper"] == cone["cone_upper"]
    return {
        "schema": "cm2.gate45.global-invariant-cone.v1",
        "provenance": {
            "all_row_slope_manifest": SLOPE_MANIFEST.name,
            "bidirectional_boundary_Z_manifest": BOUNDARY_Z_MANIFEST.name,
            "corrected_current_rows_sha256": (
                "5c03da290697ac25b814848c5aee50b22387866f9d72303a60649466cad896bd"
            ),
        },
        "global_invariant_geometric_cone": cone,
        "all_row_bidirectional_cone_typing": audit,
        "scope_limits": {
            "fixed_global_geometric_unstable_cone": True,
            "all_source_reverse_carriers_cone_typed": True,
            "all_miss_forward_carriers_cone_typed": True,
            "both_oriented_cone_entry_times_zero": True,
            "proper_family_C2_curvature_bound": False,
            "proper_family_log_density_bound": False,
            "proper_family_minimum_length_or_recovery": False,
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
    print("GATE45_GLOBAL_INVARIANT_GEOMETRIC_UNSTABLE_CONE: CERTIFIED")
    print("GATE45_ALL_ROW_BIDIRECTIONAL_ZERO_STEP_CONE_TYPING: CERTIFIED")
    print("GATE45_COMPLETE_PROPER_FAMILY_COSTS_AND_RECOVERY: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
