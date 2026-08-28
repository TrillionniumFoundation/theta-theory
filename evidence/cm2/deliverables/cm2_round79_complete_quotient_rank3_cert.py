#!/usr/bin/env python3
"""Round-79 integration certificate: complete depth-two quotient and rank-three frontier."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from cm2_round79_tangency_intersection_generator import digest


HERE = Path(__file__).resolve().parent
FILES = {
    "round78": HERE / "cm2-round78-physical-boundary-rank3-manifest-2026-07-21.json",
    "tangency_intersections": HERE / "cm2-round79-tangency-intersections-2026-07-21.json",
    "mixed_intersections": HERE / "cm2-round79-mixed-carrier-intersections-2026-07-21.json",
    "endpoint_separation": HERE / "cm2-round79-tangency-endpoint-separation-2026-07-21.json",
    "complete_quotient": HERE / "cm2-round79-complete-depth2-quotient-2026-07-21.json",
    "time3_depth6": HERE / "cm2-round79-s0-time3-depth6-registry-2026-07-21.json",
    "time3_carrier_seeds": HERE / "cm2-round79-time3-carrier-seeds-2026-07-21.json",
    "rn_rank12": HERE / "cm2-round77-rn-weighted-finite-face-sum-2026-07-21.json",
}


def load(name: str) -> dict[str, Any]:
    return json.loads(FILES[name].read_text())


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build() -> dict[str, Any]:
    tangency = load("tangency_intersections")["result"]
    mixed = load("mixed_intersections")["result"]
    endpoints = load("endpoint_separation")["result"]
    quotient = load("complete_quotient")["result"]
    time3 = load("time3_depth6")["result"]
    carriers = load("time3_carrier_seeds")["result"]
    rn = load("rn_rank12")["result"]
    if tangency["unresolved_pair_count"] or mixed["unresolved_pair_count"]:
        raise RuntimeError("unresolved depth-two intersections")
    if tangency["certified_transverse_intersection_count"] or mixed["certified_transverse_intersection_count"]:
        raise RuntimeError("unexpected depth-two carrier crossing")
    if quotient["complete_depth2_boundary_quotient_f_vector"] != [392, 532, 164]:
        raise RuntimeError("depth-two quotient")
    if time3["strict_Q3_cell_count"] != 200408 or time3["strict_R3_cell_count"] != 0:
        raise RuntimeError("time-three depth-six counts")
    if carriers["third_collision_tangency_source_carrier_family_count"] != 408:
        raise RuntimeError("rank-three carrier family count")
    if rn["face_count"] != 64:
        raise RuntimeError("RN rank-one/two face count")
    result = {
        "fixed_parameter": "s=0",
        "complete_depth2_physical_boundary_quotient": {
            "physical_curve_count": quotient["physical_boundary_curve_count"],
            "family_histogram": quotient["physical_boundary_curve_histogram"],
            "same_source_tangency_pair_count": tangency["same_source_pair_count"],
            "tangency_pairs_bbox_disjoint": tangency["strict_bbox_disjoint_pair_count"],
            "tangency_pairs_interval_excluded": tangency["certified_disjoint_after_interval_subdivision_count"],
            "mixed_tangency_R1_R2_pair_count": mixed["mixed_family_pair_count"],
            "mixed_pairs_bbox_disjoint": mixed["strict_bbox_disjoint_pair_count"],
            "mixed_pairs_interval_excluded": mixed["certified_disjoint_after_interval_subdivision_count"],
            "new_distinct_stationary_endpoints": endpoints["tangency_endpoint_count"],
            "f_vector": quotient["complete_depth2_boundary_quotient_f_vector"],
            "euler_identity": quotient["euler_identity"],
            "oriented_internal_trace_pairs": quotient["oriented_internal_trace_pairs"],
            "duplicate_trace_cost_before_total_variation": 0,
            "status": quotient["status"],
            "cellwise_label_ledger": "NOT_CERTIFIED__164_OPEN_CELLS_NOT_YET_EXPLICITLY_ENUMERATED_AND_LABELLED",
            "gate4_commuting_square": quotient["gate4_commuting_square"],
        },
        "fixed_s0_rank3_depth6_registry": {
            "strict_Q3_cell_count": time3["strict_Q3_cell_count"],
            "strict_R3_cell_count": time3["strict_R3_cell_count"],
            "Q2_to_time3_incidence_count": time3["cross_rank_Q2_to_time3_incidence_count"],
            "terminal_classification_histogram": time3["terminal_classification_histogram"],
            "normalized_area_ledger": time3["normalized_area_ledger"],
            "blocker_histogram": time3["blocker_histogram"],
            "depth2_unresolved_area": "667/64",
            "depth6_unresolved_area": time3["normalized_area_ledger"]["UNRESOLVED_TIME3_OUTER"],
            "four_refinement_level_unresolved_area_ratio": "71101/170752",
            "finite_R3_zero_is_not_limiting_emptiness": True,
        },
        "rank3_physical_boundary_seed_registry": {
            "source_carrier_family_count": carriers["source_carrier_family_count"],
            "third_collision_tangency_source_carrier_family_count": carriers["third_collision_tangency_source_carrier_family_count"],
            "third_collision_tangency_seed_incidence_count": carriers["third_collision_tangency_seed_incidence_count"],
            "typed_nonface_source_carrier_family_count": carriers["source_carrier_family_count"] - carriers["third_collision_tangency_source_carrier_family_count"],
            "physical_rank3_face_rows": "NOT_CERTIFIED__CONNECTED_COMPONENT_CONTINUATION_AND_ENDPOINT_INTERSECTION_ATLAS_REQUIRED",
        },
        "RN_frontier": {
            "certified_rank12_face_count": rn["face_count"],
            "rank_histogram": rn["rank_histogram"],
            "finite_rank12_actual_RN_dominated_sum": rn["finite_two_rank_actual_RN_dominated_sum"],
            "rank3_RN_face_rows": 0,
            "uniform_rank_tail_contraction": "NOT_CERTIFIED",
            "reason": "depth refinement contracts certification remainder, not physical rank survival or RN face charge; 408 rank-three tangency source/carrier families still require connected physical face rows",
            "all_rank_RN_summability": "NOT_CERTIFIED",
        },
        "strict_state": {
            "gate4": "1/7",
            "gate5": "10/18",
            "gate5_complete_blocks": 0,
            "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    return {
        "schema": "cm2.round79.complete-quotient-rank3.v1",
        "pins": {name: file_digest(path) for name, path in sorted(FILES.items())},
        "result": result,
        "result_sha256": digest(result),
    }


def main() -> int:
    json.dump(build(), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
