#!/usr/bin/env python3
"""Integrate the Round-81 centered-Taylor and depth-two DCEL certificates."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
FILES = {
    "round80": HERE / "cm2-round80-rank3-symmetry-cell-ledger-manifest-2026-07-21.json",
    "components": HERE / "cm2-round80-time3-carrier-components-2026-07-21.json",
    "curves": HERE / "cm2-round80-time3-tangency-curves-2026-07-21.json",
    "resolution": HERE / "cm2-round81-time3-monotone-corner-resolution-2026-07-21.json",
    "patches": HERE / "cm2-round81-rank3-root-patches-2026-07-21.json",
    "dcel": HERE / "cm2-round81-depth2-dcel-2026-07-21.json",
    "chain": HERE / "cm2-round81-depth2-cellular-chain-2026-07-21.json",
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
    round80 = load("round80")
    components = load("components")
    curves = load("curves")
    resolution = load("resolution")
    patches = load("patches")
    dcel = load("dcel")
    chain = load("chain")

    physical_components = components["physical_third_tangency_component_count"]
    direct_curves = curves["symmetry_expanded_certified_curve_count"]
    root_components = resolution["symmetry_expanded_root_bearing_component_count"]
    false_components = patches["false_tube_component_count_symmetry_expanded"]
    if physical_components != 1536:
        raise RuntimeError("physical component count")
    if direct_curves + root_components + false_components != physical_components:
        raise RuntimeError("rank-three component partition")
    if resolution["remaining_unresolved_representative_component_count"] != 0:
        raise RuntimeError("unresolved representative")
    if resolution["total_unresolved_leaves"] != 0:
        raise RuntimeError("unresolved leaf")
    if patches["fully_resolved_input_representative_count"] != 373:
        raise RuntimeError("resolved representative count")
    if dcel["f_vector"] != [392, 532, 164]:
        raise RuntimeError("DCEL f-vector")
    if dcel["cell_label_histogram"] != {"Q2": 132, "R1": 16, "R2": 16}:
        raise RuntimeError("DCEL labels")
    if chain["cellwise_boundary_squared_zero_count"] != 164:
        raise RuntimeError("cellular boundary square")
    if chain["oppositely_oriented_internal_trace_pair_count"] != 156:
        raise RuntimeError("trace cancellation")

    result = {
        "fixed_parameter": "s=0",
        "rank3_centered_taylor_resolution": {
            "physical_seed_component_count": physical_components,
            "previously_complete_graph_component_count": direct_curves,
            "centered_taylor_input_representative_count": resolution["input_failed_representative_component_count"],
            "centered_taylor_fully_resolved_representative_count": resolution["fully_resolved_representative_component_count"],
            "root_bearing_representative_count": resolution["representatives_with_physical_root_slabs"],
            "false_tube_representative_count": resolution["representatives_proved_entirely_false_tube"],
            "root_bearing_component_count_symmetry_expanded": root_components,
            "false_tube_component_count_symmetry_expanded": false_components,
            "all_root_bearing_component_count": direct_curves + root_components,
            "remaining_unresolved_representative_count": resolution["remaining_unresolved_representative_component_count"],
            "remaining_unresolved_leaf_count": resolution["total_unresolved_leaves"],
            "interval_box_test_count": resolution["total_interval_box_tests"],
            "unique_root_slab_count": resolution["total_unique_root_slabs"],
            "maximum_depth": resolution["global_maximum_depth"],
        },
        "rank3_local_root_patch_atlas": {
            "local_connected_patch_count_representatives": patches["local_connected_root_patch_count"],
            "local_connected_patch_count_symmetry_expanded": patches["local_connected_root_patch_count_symmetry_expanded"],
            "boundary_side_count_histogram": patches["boundary_side_count_histogram"],
            "strict_scope": patches["strict_scope"],
            "cross_tube_joining": "NOT_CERTIFIED",
            "physical_endpoint_and_intersection_atlas": "NOT_CERTIFIED",
        },
        "complete_fixed_s0_depth2_DCEL": {
            "f_vector": dcel["f_vector"],
            "euler_identity": dcel["euler_identity"],
            "cell_label_histogram": dcel["cell_label_histogram"],
            "exact_cyclic_boundary_word_count": dcel["exact_cyclic_boundary_word_count"],
            "exact_Q2_cyclic_boundary_word_count": dcel["exact_Q2_cyclic_boundary_word_count"],
            "cellwise_partial1_partial2_zero_count": chain["cellwise_boundary_squared_zero_count"],
            "stationary_exterior_edge_count": chain["stationary_exterior_edge_count"],
            "internal_crosscut_edge_count": chain["internal_crosscut_edge_count"],
            "internal_crosscut_family_histogram": chain["internal_crosscut_family_histogram"],
            "oppositely_oriented_internal_trace_pair_count": chain["oppositely_oriented_internal_trace_pair_count"],
            "duplicate_trace_cost_before_total_variation": chain["duplicate_trace_cost_before_total_variation"],
            "finite_depth_cellular_commuting_square": "CERTIFIED",
        },
        "official_gate4_frontier": {
            "fixed_s0_depth2_cellular_square": "CERTIFIED",
            "all_depth_same_key_stable_material_crosswalk": "NOT_CERTIFIED",
            "all_depth_commuting_square_family": "NOT_CERTIFIED",
            "gate4_promoted": False,
        },
        "RN_frontier": round80["RN_frontier"],
        "strict_state": round80["strict_state"],
        "strict_nonclaims": [
            "local root patches are not renamed complete rank-three physical faces",
            "rank-three tangency subdivision faces are not renamed return faces",
            "finite fixed-s=0 depth-two cellular commutation is not an all-depth Gate-4 family",
            "finite depth-six R3=0 is not extrapolated to limiting emptiness",
            "uniform rank-tail contraction and all-rank RN summability remain uncertified",
        ],
    }
    return {
        "schema": "cm2.round81.centered-taylor-dcel.v1",
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
