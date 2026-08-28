#!/usr/bin/env python3
"""Round-74 fixed-s0 depth-two/cross-rank certificate producer."""
from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round68_common import canonical_bytes, digest, require, sha256_path, strict_json_path


HERE = Path(__file__).resolve().parent
LEGACY = HERE / "cm2-round74-s0-depth2-registry-2026-07-21.json"
ADAPTIVE = HERE / "cm2-round74-s0-depth2-adaptive-2026-07-21.json"
WITNESSES = HERE / "cm2-round74-s0-r2-pair-witnesses-2026-07-21.json"
ROUND73 = HERE / "cm2-round73-base-r1-shared-quotient-manifest-2026-07-21.json"
MANIFEST = HERE / "cm2-round74-s0-depth2-cross-rank-manifest-2026-07-21.json"
SCHEMA = "cm2.round74.s0-depth2-cross-rank.v1"


def build() -> dict[str, Any]:
    legacy = strict_json_path(LEGACY)["result"]
    adaptive = strict_json_path(ADAPTIVE)["result"]
    witnesses = strict_json_path(WITNESSES)["result"]
    round73 = strict_json_path(ROUND73)["result"]
    require(legacy["Q1_boxes_with_s0_strictly_in_open_s_interval"] == 32, "legacy legal parents")
    require(legacy["Q1_boxes_touching_s0_only_at_adaptive_endpoint_rejected"] == 772, "legacy endpoint exclusion")
    require(legacy["strict_s0_Q2_inner_cell_count"] == 4, "legacy fixed-s0 cells")
    require(adaptive["terminal_leaf_count"] == 153508 and adaptive["binary_split_count"] == 153484, "adaptive tree")
    require(adaptive["classification_histogram"]["R2_INNER"] == 2432, "R2 leaves")
    require(adaptive["normalized_24_core_area_ledger"]["R2_INNER"] == "19/512", "R2 area")
    require(witnesses["positive_R2_witness_boxes"] == 16 and witnesses["source_destination_pair_count"] == 16, "R2 pairs")
    require(round73["quotient"]["quotient_two_cells"] == 40, "Round73 parent quotient")
    parent_map = adaptive["cross_rank_parent_map"]
    certified_children = parent_map["R1_INNER_to_Round73_return_parent"] + parent_map["Q2_or_R2_INNER_to_Round73_survival_parent"]
    outer_area = Q(adaptive["normalized_24_core_area_ledger"]["DEPTH2_OUTER"])
    result = {
        "scope": "actual fixed s=0 two-dimensional 24-core tree through collision time two",
        "legacy_3D_registry_slice_diagnosis": {
            "Q1_boxes_touching_s0_closed": legacy["Q1_boxes_touching_s0_closed"],
            "strict_open_s0_Q1_parents": legacy["Q1_boxes_with_s0_strictly_in_open_s_interval"],
            "adaptive_s_endpoint_only_boxes_rejected": legacy["Q1_boxes_touching_s0_only_at_adaptive_endpoint_rejected"],
            "strict_open_s0_Q2_cells_surviving_legacy_registry": legacy["strict_s0_Q2_inner_cell_count"],
            "conclusion": "legacy 3D adaptive registry is not a complete fixed-s0 depth-two atlas",
        },
        "fixed_s0_depth16_registry": {
            "source_cores": adaptive["source_core_count"],
            "terminal_leaves": adaptive["terminal_leaf_count"],
            "classification_histogram": adaptive["classification_histogram"],
            "normalized_area_ledger": adaptive["normalized_24_core_area_ledger"],
            "normalized_area_total": adaptive["normalized_area_conservation"],
            "certified_inner_normalized_area": str(Q(24) - outer_area),
            "outer_normalized_area": str(outer_area),
            "R2_strict_leaf_count": adaptive["R2_strict_leaf_count"],
            "R2_strict_normalized_area_lower": adaptive["normalized_24_core_area_ledger"]["R2_INNER"],
            "R2_dyadic_source_core_count": adaptive["R2_source_core_count"],
            "R2_dyadic_source_destination_pair_count": adaptive["R2_source_destination_pair_count"],
        },
        "positive_R2_pair_registry": {
            "positive_boxes": witnesses["positive_R2_witness_boxes"],
            "source_cores": witnesses["source_core_count"],
            "source_destination_pairs": witnesses["source_destination_pair_count"],
            "main_pairs": witnesses["main_pair_count"],
            "narrow_corner_pairs": witnesses["narrow_corner_pair_count"],
            "all_have_strict_Q1_parent": witnesses["all_boxes_have_strict_Q1_parent"],
            "all_are_strict_R2": witnesses["all_boxes_are_strict_R2"],
            "rows_sha256": witnesses["rows_sha256"],
        },
        "cross_rank_incidence": {
            "Round73_parent_two_cells": round73["quotient"]["quotient_two_cells"],
            "strict_child_to_parent_incidence_edges": certified_children,
            "R1_children_to_return_parent": parent_map["R1_INNER_to_Round73_return_parent"],
            "Q2_R2_children_to_survival_parent": parent_map["Q2_or_R2_INNER_to_Round73_survival_parent"],
            "outer_children_without_promoted_parent_edge": parent_map["DEPTH2_OUTER_parent_not_promoted"],
            "positive_R2_box_to_survival_parent_edges": witnesses["positive_R2_witness_boxes"],
            "same_source_core_key_required": True,
        },
        "oriented_trace_test": {
            "binary_split_internal_faces": adaptive["binary_split_count"],
            "oppositely_oriented_artificial_face_pairs_cancelled": adaptive["artificial_internal_face_cancellation_pairs"],
            "artificial_dyadic_trace_cancellation_across_rank_join": "CERTIFIED_EXACT",
            "physical_R2_pullback_trace_cancellation_across_rank_join": "NOT_CERTIFIED__PHYSICAL_FACES_REMAIN_IN_DEPTH2_OUTER",
            "test_outcome": "artificial subdivision cancellation survives rank join; physical pullback cancellation not yet promoted",
        },
        "strict_frontier": {
            "actual_fixed_s0_depth2_inner_registry": "CERTIFIED_PARTIAL_DEPTH16",
            "actual_positive_R2_cells": "CERTIFIED_2432_DYADIC_PLUS_16_PAIR_WITNESSES",
            "cross_rank_child_parent_incidence": f"CERTIFIED_{certified_children}",
            "complete_fixed_s0_depth2_physical_face_atlas": "NOT_CERTIFIED",
            "physical_cross_rank_trace_cancellation": "NOT_CERTIFIED",
            "limiting_rank_path_weighted_sum": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED__LANDING_JOIN_1_OF_7",
            "Gate5": "NOT_CERTIFIED__MATURITY_10_OF_18_BLOCKS_0",
            "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    return {
        "schema": SCHEMA,
        "pins": {path.name: sha256_path(path) for path in (LEGACY, ADAPTIVE, WITNESSES, ROUND73)},
        "result": result,
        "result_sha256": digest(result),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-json", action="store_true")
    args = parser.parse_args()
    document = build()
    if args.manifest_json:
        sys.stdout.buffer.write(canonical_bytes(document))
    else:
        print(json.dumps(document, sort_keys=True, indent=2))
