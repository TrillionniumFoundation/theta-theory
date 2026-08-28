#!/usr/bin/env python3
"""Integrate the Round-82 rank-three join, endpoint, and intersection frontier."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
FILES = {
    "round81": HERE / "cm2-round81-centered-taylor-dcel-manifest-2026-07-21.json",
    "patch_atlas": HERE / "cm2-round82-rank3-physical-patch-atlas-2026-07-21.json",
    "joins": HERE / "cm2-round82-rank3-cross-tube-joins-2026-07-21.json",
    "endpoints": HERE / "cm2-round82-rank3-boundary-endpoints-2026-07-21.json",
    "endpoint_separation": HERE / "cm2-round82-rank3-boundary-endpoint-separation-2026-07-21.json",
    "intersection_prefilter": HERE / "cm2-round82-rank3-intersection-prefilter-2026-07-21.json",
}


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name: str) -> dict[str, Any]:
    return json.loads(FILES[name].read_text())["result"]


def build() -> dict[str, Any]:
    round81 = load("round81")
    atlas = load("patch_atlas")
    joins = load("joins")
    endpoints = load("endpoints")
    separation = load("endpoint_separation")
    intersections = load("intersection_prefilter")
    if atlas["physical_patch_count"] != 1780:
        raise RuntimeError("patch count")
    if joins["certified_join_pair_count"] != 108 or joins["unresolved_pair_count"] != 0:
        raise RuntimeError("join ledger")
    if joins["joined_physical_root_component_count"] != 1672:
        raise RuntimeError("joined component count")
    if endpoints["certified_source_boundary_endpoint_count"] != 1004:
        raise RuntimeError("endpoint count")
    if endpoints["unresolved_source_boundary_interval_count"] != 0:
        raise RuntimeError("endpoint unresolved")
    if separation["strictly_interval_disjoint_pair_count"] != 14944:
        raise RuntimeError("endpoint separation")
    if intersections["different_candidate_unique_overlap_box_count"] != 165608:
        raise RuntimeError("intersection overlap count")
    if intersections["strictly_excluded_overlap_box_count"] != 127732:
        raise RuntimeError("intersection exclusion count")
    result = {
        "fixed_parameter": "s=0",
        "physical_rank3_patch_expansion": {
            "physical_patch_count": atlas["physical_patch_count"],
            "certification_histogram": atlas["physical_patch_certification_histogram"],
            "physical_branch_key_count": atlas["physical_branch_key_count"],
        },
        "certified_cross_tube_join": {
            "shared_closure_pair_count": joins["cross_tube_shared_closure_pair_count"],
            "certified_join_pair_count": joins["certified_join_pair_count"],
            "certified_no_join_pair_count": joins["certified_no_join_pair_count"],
            "unresolved_pair_count": joins["unresolved_pair_count"],
            "joined_physical_root_component_count": joins["joined_physical_root_component_count"],
            "multi_patch_joined_component_count": joins["multi_patch_joined_component_count"],
            "maximum_patch_count_per_joined_component": joins["maximum_patch_count_per_joined_component"],
            "join_certification_mode_histogram": joins["join_certification_mode_histogram"],
        },
        "source_boundary_endpoint_atlas": {
            "joined_physical_root_component_count": endpoints["joined_physical_root_component_count"],
            "component_endpoint_count_histogram": endpoints["component_source_boundary_endpoint_count_histogram"],
            "certified_endpoint_count": endpoints["certified_source_boundary_endpoint_count"],
            "interval_box_test_count": endpoints["total_interval_box_tests"],
            "directed_bisection_steps_per_endpoint": separation["directed_bisection_refinement_steps_per_endpoint"],
            "same_boundary_side_pair_count": separation["same_source_boundary_side_pair_count"],
            "strictly_disjoint_endpoint_pair_count": separation["strictly_interval_disjoint_pair_count"],
            "unresolved_endpoint_pair_count": separation["unresolved_or_overlapping_pair_count"],
        },
        "different_candidate_intersection_frontier": {
            "raw_root_box_overlap_count": intersections["different_candidate_raw_root_box_overlap_count"],
            "unique_root_box_overlap_count": intersections["different_candidate_unique_overlap_box_count"],
            "component_pair_count": intersections["different_candidate_component_pair_count"],
            "strictly_excluded_overlap_box_count": intersections["strictly_excluded_overlap_box_count"],
            "residual_two_equation_box_count": intersections["residual_two_equation_box_count"],
            "residual_component_pair_count": intersections["residual_component_pair_count"],
            "status": "TWO_EQUATION_NEAR_COTANGENCY_FRONTIER_NOT_CLOSED",
        },
        "rank3_face_and_RN_eligibility": {
            "two_source_boundary_endpoint_component_count": int(endpoints["component_source_boundary_endpoint_count_histogram"]["2"]),
            "one_source_boundary_endpoint_component_count": int(endpoints["component_source_boundary_endpoint_count_histogram"]["1"]),
            "zero_source_boundary_endpoint_component_count": int(endpoints["component_source_boundary_endpoint_count_histogram"]["0"]),
            "complete_physical_rank3_face_rows": 0,
            "rank3_F8_F9_F10_F13_F16_rows": 0,
            "rank3_return_face_RN_rows": 0,
            "reason": "different-candidate interior intersections and internal/uncovered-gap endpoints remain uncertified",
        },
        "gate4_and_tail_frontier": {
            "fixed_s0_depth2_cellular_square": "CERTIFIED_ROUND81",
            "same_key_all_depth_stable_material_crosswalk": "NOT_CERTIFIED",
            "all_depth_commuting_square_family": "NOT_CERTIFIED",
            "uniform_physical_rank_transition_contraction": "NOT_CERTIFIED",
            "all_rank_RN_summability": "NOT_CERTIFIED",
        },
        "RN_frontier": round81["RN_frontier"],
        "strict_state": round81["strict_state"],
        "strict_nonclaims": [
            "1672 joined root components are not renamed complete physical rank-three faces",
            "404 components with two source-boundary endpoints are not promoted before the interior intersection atlas closes",
            "one-pass interval exclusion is not a two-equation Krawczyk solution of the 37876 residual boxes",
            "rank-three subdivision roots are not renamed return-face RN rows",
            "fixed-depth cellular commutation is not an all-depth Gate-4 crosswalk",
        ],
    }
    return {
        "schema": "cm2.round82.rank3-join-endpoint-frontier.v1",
        "pins": {name: file_digest(path) for name, path in FILES.items()},
        "result": result,
        "result_sha256": digest(result),
    }


def main() -> int:
    json.dump(build(), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
