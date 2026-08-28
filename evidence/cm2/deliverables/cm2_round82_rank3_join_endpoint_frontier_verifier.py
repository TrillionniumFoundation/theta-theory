#!/usr/bin/env python3
"""Independent hostile-semantic verifier for CM2 Round 82."""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "cm2-round82-rank3-join-endpoint-frontier-manifest-2026-07-21.json"
FILE_MAP = {
    "round81": "cm2-round81-centered-taylor-dcel-manifest-2026-07-21.json",
    "patch_atlas": "cm2-round82-rank3-physical-patch-atlas-2026-07-21.json",
    "joins": "cm2-round82-rank3-cross-tube-joins-2026-07-21.json",
    "endpoints": "cm2-round82-rank3-boundary-endpoints-2026-07-21.json",
    "endpoint_separation": "cm2-round82-rank3-boundary-endpoint-separation-2026-07-21.json",
    "intersection_prefilter": "cm2-round82-rank3-intersection-prefilter-2026-07-21.json",
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
    require(document["schema"] == "cm2.round82.rank3-join-endpoint-frontier.v1", "schema")
    require(document["result_sha256"] == digest(document["result"]), "digest")
    result = document["result"]
    patches = result["physical_rank3_patch_expansion"]
    require(patches["physical_patch_count"] == 1780, "patches")
    joins = result["certified_cross_tube_join"]
    require(joins["shared_closure_pair_count"] == 128, "shared closures")
    require(joins["certified_join_pair_count"] == 108, "joins")
    require(joins["certified_no_join_pair_count"] == 20, "no joins")
    require(joins["unresolved_pair_count"] == 0, "join unresolved")
    require(joins["joined_physical_root_component_count"] == 1672, "components")
    endpoints = result["source_boundary_endpoint_atlas"]
    require(endpoints["certified_endpoint_count"] == 1004, "endpoints")
    require(endpoints["same_boundary_side_pair_count"] == 14944, "endpoint pairs")
    require(endpoints["strictly_disjoint_endpoint_pair_count"] == 14944, "endpoint separation")
    require(endpoints["unresolved_endpoint_pair_count"] == 0, "endpoint unresolved")
    intersections = result["different_candidate_intersection_frontier"]
    require(intersections["unique_root_box_overlap_count"] == 165608, "overlap boxes")
    require(intersections["strictly_excluded_overlap_box_count"] == 127732, "excluded boxes")
    require(intersections["residual_two_equation_box_count"] == 37876, "residual boxes")
    require(intersections["residual_component_pair_count"] == 1836, "residual pairs")
    eligibility = result["rank3_face_and_RN_eligibility"]
    require(eligibility["two_source_boundary_endpoint_component_count"] == 404, "two endpoint components")
    require(eligibility["complete_physical_rank3_face_rows"] == 0, "face rows")
    require(eligibility["rank3_return_face_RN_rows"] == 0, "RN rows")
    require(result["strict_state"]["CM2"] == "NO-GO_FOR_CLAIM", "CM2")
    if pins:
        for name, expected in document["pins"].items():
            require(hashlib.sha256((HERE / FILE_MAP[name]).read_bytes()).hexdigest() == expected, f"pin {name}")


def main() -> int:
    document = strict_text(MANIFEST.read_text())
    validate(document)
    paths = [
        ("physical_rank3_patch_expansion", "physical_patch_count"),
        ("certified_cross_tube_join", "shared_closure_pair_count"),
        ("certified_cross_tube_join", "certified_join_pair_count"),
        ("certified_cross_tube_join", "certified_no_join_pair_count"),
        ("certified_cross_tube_join", "unresolved_pair_count"),
        ("certified_cross_tube_join", "joined_physical_root_component_count"),
        ("source_boundary_endpoint_atlas", "certified_endpoint_count"),
        ("source_boundary_endpoint_atlas", "same_boundary_side_pair_count"),
        ("source_boundary_endpoint_atlas", "strictly_disjoint_endpoint_pair_count"),
        ("source_boundary_endpoint_atlas", "unresolved_endpoint_pair_count"),
        ("different_candidate_intersection_frontier", "unique_root_box_overlap_count"),
        ("different_candidate_intersection_frontier", "strictly_excluded_overlap_box_count"),
        ("different_candidate_intersection_frontier", "residual_two_equation_box_count"),
        ("different_candidate_intersection_frontier", "residual_component_pair_count"),
        ("rank3_face_and_RN_eligibility", "two_source_boundary_endpoint_component_count"),
        ("rank3_face_and_RN_eligibility", "complete_physical_rank3_face_rows"),
        ("rank3_face_and_RN_eligibility", "rank3_return_face_RN_rows"),
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
        "schema": "cm2.round82.rank3-join-endpoint-frontier-audit.v1",
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
