#!/usr/bin/env python3
"""Integrate the Round-83 outgoing-line common-tangent intersection frontier."""
from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
FILES = {
    "round82": HERE / "cm2-round82-rank3-join-endpoint-frontier-manifest-2026-07-21.json",
    "primary": HERE / "cm2-round83-common-tangent-line-krawczyk-2026-07-22.json",
    "centered": HERE / "cm2-round83-centered-line-refinement-2026-07-22.json",
    "degenerate": HERE / "cm2-round83-degenerate-interface-resolution-2026-07-22.json",
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
    round82 = load("round82")
    primary = load("primary")
    centered = load("centered")
    degenerate = load("degenerate")
    if primary["input_residual_box_count"] != 37876:
        raise RuntimeError("primary residual count")
    if primary["box_status_histogram"] != {
        "CERTIFIED_DISJOINT": 21154,
        "DEGENERATE_INTERFACE_BOX": 16108,
        "UNRESOLVED_COMMON_TANGENT_LINE": 614,
    }:
        raise RuntimeError("primary status ledger")
    if degenerate["certified_disjoint_degenerate_box_count"] != 16108 or degenerate["unresolved_leaf_count"] != 0:
        raise RuntimeError("degenerate ledger")
    if centered["input_hard_box_count"] != 614 or centered["raw_krawczyk_root_count"] != 0:
        raise RuntimeError("centered hard ledger")
    input_area = Q(centered["input_hard_box_area"])
    unresolved_area = Q(centered["unresolved_area"])
    ratio = unresolved_area / input_area
    if ratio != Q(19743, 4603904):
        raise RuntimeError("centered area ratio")
    total_overlap_boxes = round82["different_candidate_intersection_frontier"]["unique_root_box_overlap_count"]
    prefilter_excluded = round82["different_candidate_intersection_frontier"]["strictly_excluded_overlap_box_count"]
    if prefilter_excluded + 21154 + 16108 + 614 != total_overlap_boxes:
        raise RuntimeError("complete overlap partition")
    result = {
        "fixed_parameter": "s=0",
        "common_tangent_coordinate_change": {
            "original_two_discriminant_residual_box_count": primary["input_residual_box_count"],
            "common_tangent_targets_per_candidate_pair": 8,
            "outgoing_line_coordinates": ["normal_x_or_normal_y", "line_offset_h"],
            "primary_interval_line_box_test_count": primary["interval_line_box_test_count"],
            "maximum_primary_depth": primary["maximum_depth"],
            "raw_certified_intersection_root_count": primary["raw_krawczyk_root_count"],
        },
        "complete_overlap_box_partition": {
            "all_unique_different_candidate_overlap_boxes": total_overlap_boxes,
            "round82_prefilter_strictly_excluded": prefilter_excluded,
            "round83_positive_area_common_tangent_strictly_disjoint": 21154,
            "round83_degenerate_interface_strictly_disjoint": degenerate["certified_disjoint_degenerate_box_count"],
            "remaining_hard_positive_area_boxes": centered["input_hard_box_count"],
            "identity": f"{total_overlap_boxes}={prefilter_excluded}+21154+16108+614",
        },
        "degenerate_interface_atlas": {
            "input_component_pair_count": degenerate["input_degenerate_component_pair_count"],
            "input_box_count": degenerate["input_degenerate_box_count"],
            "interval_line_test_count": degenerate["interval_line_test_count"],
            "certified_disjoint_box_count": degenerate["certified_disjoint_degenerate_box_count"],
            "unresolved_component_pair_count": degenerate["unresolved_component_pair_count"],
            "unresolved_leaf_count": degenerate["unresolved_leaf_count"],
        },
        "hard_area_centered_refinement": {
            "hard_component_pair_count": centered["input_hard_component_pair_count"],
            "hard_initial_box_count": centered["input_hard_box_count"],
            "hard_initial_area": centered["input_hard_box_area"],
            "centered_line_box_test_count": centered["centered_line_box_test_count"],
            "raw_krawczyk_root_count": centered["raw_krawczyk_root_count"],
            "unresolved_leaf_count": centered["unresolved_leaf_count"],
            "unresolved_area": centered["unresolved_area"],
            "unresolved_to_initial_area_ratio": str(ratio),
            "status": "NOT_CLOSED",
        },
        "rank3_quotient_and_RN_eligibility": {
            "certified_different_candidate_intersection_count": 0,
            "unresolved_hard_component_pair_count": centered["input_hard_component_pair_count"],
            "complete_rank3_intersection_atlas": "NOT_CERTIFIED",
            "complete_physical_rank3_face_rows": 0,
            "rank3_F8_F9_F10_F13_F16_rows": 0,
            "rank3_return_face_RN_rows": 0,
        },
        "gate4_and_tail_frontier": round82["gate4_and_tail_frontier"],
        "RN_frontier": round82["RN_frontier"],
        "strict_state": round82["strict_state"],
        "strict_nonclaims": [
            "zero certified common-tangent roots is not a proof of disjointness on the 614 hard boxes",
            "area contraction of the hard frontier is not a physical rank-transition contraction",
            "rank-three joined root components are not renamed complete faces before the 42 hard pairs close",
            "rank-three tangency roots are not renamed return-face RN rows",
            "fixed-depth cellular commutation is not an all-depth Gate-4 crosswalk",
        ],
    }
    return {
        "schema": "cm2.round83.common-tangent-frontier.v1",
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
