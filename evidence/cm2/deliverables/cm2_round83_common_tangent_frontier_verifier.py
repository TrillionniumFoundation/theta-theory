#!/usr/bin/env python3
"""Independent hostile-semantic verifier for CM2 Round 83."""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "cm2-round83-common-tangent-frontier-manifest-2026-07-22.json"
FILE_MAP = {
    "round82": "cm2-round82-rank3-join-endpoint-frontier-manifest-2026-07-21.json",
    "primary": "cm2-round83-common-tangent-line-krawczyk-2026-07-22.json",
    "centered": "cm2-round83-centered-line-refinement-2026-07-22.json",
    "degenerate": "cm2-round83-degenerate-interface-resolution-2026-07-22.json",
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
    require(document["schema"] == "cm2.round83.common-tangent-frontier.v1", "schema")
    require(document["result_sha256"] == digest(document["result"]), "digest")
    result = document["result"]
    change = result["common_tangent_coordinate_change"]
    require(change["original_two_discriminant_residual_box_count"] == 37876, "input boxes")
    require(change["raw_certified_intersection_root_count"] == 0, "roots")
    partition = result["complete_overlap_box_partition"]
    require(partition["all_unique_different_candidate_overlap_boxes"] == 165608, "all boxes")
    require(partition["round82_prefilter_strictly_excluded"] == 127732, "prefilter")
    require(partition["round83_positive_area_common_tangent_strictly_disjoint"] == 21154, "area disjoint")
    require(partition["round83_degenerate_interface_strictly_disjoint"] == 16108, "interface disjoint")
    require(partition["remaining_hard_positive_area_boxes"] == 614, "hard boxes")
    degenerate = result["degenerate_interface_atlas"]
    require(degenerate["unresolved_leaf_count"] == 0, "degenerate unresolved")
    centered = result["hard_area_centered_refinement"]
    require(centered["hard_component_pair_count"] == 42, "hard pairs")
    require(centered["hard_initial_box_count"] == 614, "hard input")
    require(centered["unresolved_to_initial_area_ratio"] == "19743/4603904", "area ratio")
    require(centered["status"] == "NOT_CLOSED", "hard status")
    eligibility = result["rank3_quotient_and_RN_eligibility"]
    require(eligibility["complete_physical_rank3_face_rows"] == 0, "faces")
    require(eligibility["rank3_return_face_RN_rows"] == 0, "RN rows")
    require(result["strict_state"]["CM2"] == "NO-GO_FOR_CLAIM", "CM2")
    if pins:
        for name, expected in document["pins"].items():
            require(hashlib.sha256((HERE / FILE_MAP[name]).read_bytes()).hexdigest() == expected, f"pin {name}")


def main() -> int:
    document = strict_text(MANIFEST.read_text())
    validate(document)
    paths = [
        ("common_tangent_coordinate_change", "original_two_discriminant_residual_box_count"),
        ("common_tangent_coordinate_change", "raw_certified_intersection_root_count"),
        ("complete_overlap_box_partition", "all_unique_different_candidate_overlap_boxes"),
        ("complete_overlap_box_partition", "round82_prefilter_strictly_excluded"),
        ("complete_overlap_box_partition", "round83_positive_area_common_tangent_strictly_disjoint"),
        ("complete_overlap_box_partition", "round83_degenerate_interface_strictly_disjoint"),
        ("complete_overlap_box_partition", "remaining_hard_positive_area_boxes"),
        ("degenerate_interface_atlas", "unresolved_leaf_count"),
        ("hard_area_centered_refinement", "hard_component_pair_count"),
        ("hard_area_centered_refinement", "hard_initial_box_count"),
        ("rank3_quotient_and_RN_eligibility", "complete_physical_rank3_face_rows"),
        ("rank3_quotient_and_RN_eligibility", "rank3_return_face_RN_rows"),
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
        "schema": "cm2.round83.common-tangent-frontier-audit.v1",
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
