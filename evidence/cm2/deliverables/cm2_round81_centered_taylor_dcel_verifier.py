#!/usr/bin/env python3
"""Independent hostile-semantic verifier for CM2 Round 81."""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "cm2-round81-centered-taylor-dcel-manifest-2026-07-21.json"
FILE_MAP = {
    "round80": "cm2-round80-rank3-symmetry-cell-ledger-manifest-2026-07-21.json",
    "components": "cm2-round80-time3-carrier-components-2026-07-21.json",
    "curves": "cm2-round80-time3-tangency-curves-2026-07-21.json",
    "resolution": "cm2-round81-time3-monotone-corner-resolution-2026-07-21.json",
    "patches": "cm2-round81-rank3-root-patches-2026-07-21.json",
    "dcel": "cm2-round81-depth2-dcel-2026-07-21.json",
    "chain": "cm2-round81-depth2-cellular-chain-2026-07-21.json",
}


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def strict_text(text: str) -> Any:
    def pairs(rows: list[tuple[str, Any]]) -> dict[str, Any]:
        result = {}
        for key, value in rows:
            if key in result:
                raise ValueError("duplicate key")
            result[key] = value
        return result
    return json.loads(text, object_pairs_hook=pairs, parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def validate(document: dict[str, Any], *, pins: bool = True) -> None:
    require(document["schema"] == "cm2.round81.centered-taylor-dcel.v1", "schema")
    require(document["result_sha256"] == digest(document["result"]), "digest")
    result = document["result"]
    resolution = result["rank3_centered_taylor_resolution"]
    require(resolution["physical_seed_component_count"] == 1536, "physical components")
    require(resolution["previously_complete_graph_component_count"] == 532, "direct components")
    require(resolution["centered_taylor_fully_resolved_representative_count"] == 373, "resolved representatives")
    require(resolution["root_bearing_component_count_symmetry_expanded"] == 664, "root components")
    require(resolution["false_tube_component_count_symmetry_expanded"] == 340, "false components")
    require(resolution["all_root_bearing_component_count"] == 1196, "all root components")
    require(resolution["remaining_unresolved_representative_count"] == 0, "unresolved representatives")
    require(resolution["remaining_unresolved_leaf_count"] == 0, "unresolved leaves")
    require(resolution["interval_box_test_count"] == 26922, "box tests")
    require(resolution["unique_root_slab_count"] == 9912, "root slabs")
    patches = result["rank3_local_root_patch_atlas"]
    require(patches["local_connected_patch_count_representatives"] == 417, "local patches")
    require(patches["local_connected_patch_count_symmetry_expanded"] == 1248, "expanded patches")
    dcel = result["complete_fixed_s0_depth2_DCEL"]
    require(dcel["f_vector"] == [392, 532, 164], "f-vector")
    require(dcel["cell_label_histogram"] == {"Q2": 132, "R1": 16, "R2": 16}, "cell labels")
    require(dcel["exact_cyclic_boundary_word_count"] == 164, "boundary words")
    require(dcel["exact_Q2_cyclic_boundary_word_count"] == 132, "Q2 boundary words")
    require(dcel["cellwise_partial1_partial2_zero_count"] == 164, "boundary square")
    require(dcel["oppositely_oriented_internal_trace_pair_count"] == 156, "trace pairs")
    require(dcel["duplicate_trace_cost_before_total_variation"] == 0, "trace cost")
    frontier = result["official_gate4_frontier"]
    require(frontier["fixed_s0_depth2_cellular_square"] == "CERTIFIED", "finite square")
    require(frontier["all_depth_commuting_square_family"] == "NOT_CERTIFIED", "all-depth square")
    require(frontier["gate4_promoted"] is False, "Gate 4 promotion")
    require(result["strict_state"]["CM2"] == "NO-GO_FOR_CLAIM", "CM2 state")
    if pins:
        for name, expected in document["pins"].items():
            require(hashlib.sha256((HERE / FILE_MAP[name]).read_bytes()).hexdigest() == expected, f"pin {name}")


def main() -> int:
    document = strict_text(MANIFEST.read_text())
    validate(document)
    paths = [
        ("rank3_centered_taylor_resolution", "physical_seed_component_count"),
        ("rank3_centered_taylor_resolution", "previously_complete_graph_component_count"),
        ("rank3_centered_taylor_resolution", "centered_taylor_fully_resolved_representative_count"),
        ("rank3_centered_taylor_resolution", "root_bearing_component_count_symmetry_expanded"),
        ("rank3_centered_taylor_resolution", "false_tube_component_count_symmetry_expanded"),
        ("rank3_centered_taylor_resolution", "all_root_bearing_component_count"),
        ("rank3_centered_taylor_resolution", "remaining_unresolved_representative_count"),
        ("rank3_centered_taylor_resolution", "remaining_unresolved_leaf_count"),
        ("rank3_centered_taylor_resolution", "interval_box_test_count"),
        ("rank3_centered_taylor_resolution", "unique_root_slab_count"),
        ("rank3_local_root_patch_atlas", "local_connected_patch_count_representatives"),
        ("rank3_local_root_patch_atlas", "local_connected_patch_count_symmetry_expanded"),
        ("complete_fixed_s0_depth2_DCEL", "exact_cyclic_boundary_word_count"),
        ("complete_fixed_s0_depth2_DCEL", "exact_Q2_cyclic_boundary_word_count"),
        ("complete_fixed_s0_depth2_DCEL", "cellwise_partial1_partial2_zero_count"),
        ("complete_fixed_s0_depth2_DCEL", "oppositely_oriented_internal_trace_pair_count"),
    ]
    rejected = 0
    for section, key in paths:
        mutation = copy.deepcopy(document)
        mutation["result"][section][key] += 1
        mutation["result_sha256"] = digest(mutation["result"])
        try:
            validate(mutation, pins=False)
        except Exception:
            rejected += 1
    strict_cases = ['{"a":1,"a":2}', '{"a":NaN}', '{"a":Infinity}', '{"a":-Infinity}']
    strict_rejected = 0
    for text in strict_cases:
        try:
            strict_text(text)
        except Exception:
            strict_rejected += 1
    audit = {
        "schema": "cm2.round81.centered-taylor-dcel-audit.v1",
        "result": {
            "manifest_valid": True,
            "hostile_semantic_mutation_count": len(paths),
            "hostile_semantic_mutations_rejected": rejected,
            "strict_json_case_count": len(strict_cases),
            "strict_json_rejections": strict_rejected,
            "all_pins_verified": True,
        },
    }
    json.dump(audit, sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
