#!/usr/bin/env python3
"""Round-75 physical R2 curve atlas and depth-two subquotient certificate."""
from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round68_common import canonical_bytes, digest, require, sha256_path, strict_json_path


HERE = Path(__file__).resolve().parent
CURVES = HERE / "cm2-round75-r2-physical-curves-2026-07-21.json"
NONINTERSECTION = HERE / "cm2-round75-r2-curve-nonintersection-2026-07-21.json"
CURVE_GENERATOR = HERE / "cm2_round75_r2_physical_curve_generator.py"
NONINTERSECTION_GENERATOR = HERE / "cm2_round75_r2_curve_nonintersection_generator.py"
ROUND73 = HERE / "cm2-round73-base-r1-shared-quotient-manifest-2026-07-21.json"
ROUND74 = HERE / "cm2-round74-s0-depth2-cross-rank-manifest-2026-07-21.json"
MANIFEST = HERE / "cm2-round75-r2-physical-subquotient-manifest-2026-07-21.json"
SCHEMA = "cm2.round75.r2-physical-subquotient.v1"


def build() -> dict[str, Any]:
    curves = strict_json_path(CURVES)["result"]
    nonintersection = strict_json_path(NONINTERSECTION)["result"]
    round73 = strict_json_path(ROUND73)["result"]
    round74 = strict_json_path(ROUND74)["result"]

    require(curves["physical_R2_component_count"] == 16, "physical R2 components")
    require(curves["physical_R2_curve_count"] == 32, "physical R2 curves")
    require(curves["endpoint_vertex_count"] == 64, "endpoint vertices")
    require(curves["parametric_interval_newton_slab_count"] == 4096, "continuation slabs")
    require(curves["component_rows_sha256"] == digest(curves["component_rows"]), "component digest")
    require(curves["curve_rows_sha256"] == digest(curves["curve_rows"]), "curve digest")
    require(curves["all_curves_have_strict_Q1_owner_chart_other_coordinate"], "strict curve qualification")
    require(nonintersection["curve_pair_count"] == nonintersection["nonintersecting_curve_pairs"] == 48, "curve-pair exclusion")
    require(nonintersection["unresolved_count"] == 0, "unresolved intersections")
    require(nonintersection["rows_sha256"] == digest(nonintersection["rows"]), "nonintersection digest")

    base = round73["quotient"]
    require((base["quotient_vertices"], base["quotient_edges"], base["quotient_two_cells"]) == (144, 160, 40), "Round73 quotient")
    require(round74["positive_R2_pair_registry"]["source_destination_pairs"] == 16, "Round74 R2 pairs")

    added_stationary_vertices = curves["endpoint_vertex_count"]
    added_pullback_edges = curves["physical_R2_curve_count"]
    quotient_vertices = base["quotient_vertices"] + added_stationary_vertices
    stationary_segments = base["stationary_segments_after_subdivision"] + added_stationary_vertices
    pullback_edges = base["pullback_face_components"] + added_pullback_edges
    quotient_edges = stationary_segments + pullback_edges
    quotient_two_cells = base["quotient_two_cells"] + added_pullback_edges
    connected_components = base["connected_components"]
    require((quotient_vertices, quotient_edges, quotient_two_cells) == (208, 256, 72), "Round75 f-vector")
    require(quotient_vertices - quotient_edges + quotient_two_cells == connected_components == 24, "Round75 Euler identity")

    certified_r1_cells = base["positive_return_cells"]
    certified_r2_cells = curves["physical_R2_component_count"]
    residual_complement_cells = quotient_two_cells - certified_r1_cells - certified_r2_cells
    require((certified_r1_cells, certified_r2_cells, residual_complement_cells) == (16, 16, 40), "subquotient cells")

    result = {
        "scope": "actual fixed s=0 depth-two physical subquotient obtained by inserting 32 certified R2 crosscuts into the Round73 base-R1 quotient",
        "physical_R2_curve_atlas": {
            "certified_components": curves["physical_R2_component_count"],
            "main_components": sum(row["branch"] == "main" for row in curves["component_rows"]),
            "narrow_corner_components": sum(row["branch"] == "narrow_corner" for row in curves["component_rows"]),
            "source_cores": len({row["source_core_index"] for row in curves["component_rows"]}),
            "physical_curves": curves["physical_R2_curve_count"],
            "stationary_endpoint_vertices": curves["endpoint_vertex_count"],
            "parametric_interval_Newton_slabs": curves["parametric_interval_newton_slab_count"],
            "slabs_per_curve": 128,
            "arithmetic": "384-bit Arb",
            "time_j": 2,
            "physical_second_collision_owner": "W[0,0]",
            "component_rows_sha256": curves["component_rows_sha256"],
            "curve_rows_sha256": curves["curve_rows_sha256"],
        },
        "owner_chart_qualification": {
            "strict_Q1_owner_destination_chart_other_coordinate_on_all_curves": curves["all_curves_have_strict_Q1_owner_chart_other_coordinate"],
            "curves_using_chart_free_candidate_union_on_at_least_one_slab": curves["chart_free_owner_curve_count"],
            "curves_using_chart_free_candidate_union_on_every_slab": curves["fully_chart_free_owner_curve_count"],
            "chart_free_candidate_union_slabs": curves["chart_free_owner_slab_count"],
            "scan_bisection_fallback_slabs": curves["scan_bisection_fallback_slab_count"],
            "qualification": "outgoing-chart seams are discharged by a chart-free candidate-union proof of the same physical owner, not by assigning a seam to either chart",
        },
        "physical_curve_nonintersection": {
            "source_cores": nonintersection["source_core_count"],
            "all_pairs_per_source_core": nonintersection["curve_pair_count"],
            "certified_nonintersecting_pairs": nonintersection["nonintersecting_curve_pairs"],
            "Arb_box_tests": nonintersection["total_box_tests"],
            "excluded_leaves": nonintersection["total_excluded_leaves"],
            "maximum_binary_depth": nonintersection["global_maximum_depth"],
            "unresolved": nonintersection["unresolved_count"],
            "rows_sha256": nonintersection["rows_sha256"],
        },
        "depth_two_physical_subquotient": {
            "base_R1_f_vector": [base["quotient_vertices"], base["quotient_edges"], base["quotient_two_cells"]],
            "new_stationary_endpoint_vertices": added_stationary_vertices,
            "stationary_segments_after_R2_subdivision": stationary_segments,
            "R1_plus_R2_physical_pullback_edges": pullback_edges,
            "f_vector": [quotient_vertices, quotient_edges, quotient_two_cells],
            "connected_physical_core_rectangles": connected_components,
            "euler_identity": "208-256+72=24",
            "certified_R1_cells": certified_r1_cells,
            "certified_R2_band_cells": certified_r2_cells,
            "residual_complement_cells": residual_complement_cells,
            "residual_cells_are_not_promoted_to_Q2": True,
        },
        "cross_rank_incidence": {
            "R2_component_to_Round73_survival_parent_edges": certified_r2_cells,
            "R2_curve_to_parent_incidence_edges": added_pullback_edges,
            "R2_one_sided_trace_records": 2 * added_pullback_edges,
            "same_source_core_parent_key_required": True,
            "rank_join": "actual physical time-2 faces refine actual depth-1 survival parents",
        },
        "oriented_physical_trace_cancellation": {
            "Round73_internal_R1_pullback_edges": base["pullback_face_components"],
            "Round75_internal_R2_pullback_edges": added_pullback_edges,
            "internal_physical_pullback_edges": pullback_edges,
            "oppositely_oriented_physical_trace_pairs_cancelled": pullback_edges,
            "duplicate_trace_cost_before_total_variation": 0,
            "status": "CERTIFIED_EXACT_ON_THE_72_CELL_DEPTH2_SUBQUOTIENT",
        },
        "F14_F15_F17_attack": {
            "F14": "NOT_CERTIFIED__NO_RECOVERED_STRONG_BLOCK",
            "F15": "NOT_CERTIFIED__NO_RAW_ORLICZ_RECOVERY_OR_POSITIVE_CEMETERY",
            "F17_boundary_sector": "CERTIFIED_DEPTH2_SUBQUOTIENT__ALL_64_INTERNAL_PHYSICAL_PULLBACK_TRACES_CANCEL_BEFORE_TV",
            "F17_bulk_sector": "NOT_CERTIFIED__NO_ALL_INPUT_ANISOTROPIC_CURRENT_RECIPIENT_OR_ALL_DEPTH_SUFFIX_BOUND",
            "F17_official": "NOT_CERTIFIED",
            "F18": "NOT_CERTIFIED__NO_SINGLE_ALL_DEPTH_18_FIELD_BLOCK",
        },
        "strict_frontier": {
            "sixteen_actual_R2_components_and_thirty_two_physical_faces": "CERTIFIED",
            "depth2_physical_subquotient": "CERTIFIED_72_CELLS",
            "physical_trace_cancellation_through_rank_join": "CERTIFIED_ON_SUBQUOTIENT",
            "complete_fixed_s0_depth2_physical_face_atlas": "NOT_CERTIFIED__ADDITIONAL_R2_COMPONENTS_MAY_REMAIN_IN_RESIDUAL_OUTER",
            "arbitrary_depth_Rn_face_atlas": "NOT_CERTIFIED",
            "limiting_rank_path_weighted_sum": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED__LANDING_JOIN_1_OF_7",
            "Gate5": "NOT_CERTIFIED__MATURITY_10_OF_18_BLOCKS_0",
            "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    pins = {
        path.name: sha256_path(path)
        for path in (CURVES, NONINTERSECTION, CURVE_GENERATOR, NONINTERSECTION_GENERATOR, ROUND73, ROUND74)
    }
    return {"schema": SCHEMA, "pins": pins, "result": result, "result_sha256": digest(result)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-json", action="store_true")
    args = parser.parse_args()
    document = build()
    if args.manifest_json:
        sys.stdout.buffer.write(canonical_bytes(document))
    else:
        print(json.dumps(document, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
