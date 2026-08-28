#!/usr/bin/env python3
"""Independent structural and hostile-semantic audit for CM2 Round 79."""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "cm2-round79-complete-quotient-rank3-manifest-2026-07-21.json"


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
    return json.loads(
        text,
        object_pairs_hook=pairs,
        parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)),
    )


def strict_load(path: Path) -> dict[str, Any]:
    return strict_text(path.read_text())


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def validate(manifest: dict[str, Any], *, pins: bool = True) -> None:
    require(manifest["schema"] == "cm2.round79.complete-quotient-rank3.v1", "schema")
    require(manifest["result_sha256"] == digest(manifest["result"]), "result digest")
    result = manifest["result"]
    quotient = result["complete_depth2_physical_boundary_quotient"]
    require(quotient["physical_curve_count"] == 156, "curve count")
    require(quotient["same_source_tangency_pair_count"] == 244, "tangency pair count")
    require(quotient["mixed_tangency_R1_R2_pair_count"] == 224, "mixed pair count")
    require(quotient["new_distinct_stationary_endpoints"] == 184, "endpoint count")
    require(quotient["f_vector"] == [392, 532, 164], "f-vector")
    require(392 - 532 + 164 == 24, "Euler")
    require(quotient["duplicate_trace_cost_before_total_variation"] == 0, "trace cost")
    rank3 = result["fixed_s0_rank3_depth6_registry"]
    require(rank3["strict_Q3_cell_count"] == 200408, "Q3 count")
    require(rank3["strict_R3_cell_count"] == 0, "R3 count")
    require(rank3["normalized_area_ledger"] == {
        "SURVIVE_THROUGH_3_INNER": "211971/16384",
        "UNRESOLVED_TIME3_OUTER": "71101/16384",
    }, "rank3 area ledger")
    require(rank3["four_refinement_level_unresolved_area_ratio"] == "71101/170752", "area ratio")
    carriers = result["rank3_physical_boundary_seed_registry"]
    require(carriers["source_carrier_family_count"] == 412, "carrier count")
    require(carriers["third_collision_tangency_source_carrier_family_count"] == 408, "tangency carrier count")
    require(carriers["third_collision_tangency_seed_incidence_count"] == 91052, "seed count")
    rn = result["RN_frontier"]
    require(rn["certified_rank12_face_count"] == 64, "RN rank12 faces")
    require(rn["rank3_RN_face_rows"] == 0, "RN rank3 rows")
    require(rn["uniform_rank_tail_contraction"] == "NOT_CERTIFIED", "RN tail status")
    require(result["strict_state"] == {
        "gate4": "1/7",
        "gate5": "10/18",
        "gate5_complete_blocks": 0,
        "complete_composite_gates": "0/5",
        "CM2": "NO-GO_FOR_CLAIM",
    }, "strict state")
    if pins:
        for name, expected in manifest["pins"].items():
            path_map = {
                "round78": "cm2-round78-physical-boundary-rank3-manifest-2026-07-21.json",
                "tangency_intersections": "cm2-round79-tangency-intersections-2026-07-21.json",
                "mixed_intersections": "cm2-round79-mixed-carrier-intersections-2026-07-21.json",
                "endpoint_separation": "cm2-round79-tangency-endpoint-separation-2026-07-21.json",
                "complete_quotient": "cm2-round79-complete-depth2-quotient-2026-07-21.json",
                "time3_depth6": "cm2-round79-s0-time3-depth6-registry-2026-07-21.json",
                "time3_carrier_seeds": "cm2-round79-time3-carrier-seeds-2026-07-21.json",
                "rn_rank12": "cm2-round77-rn-weighted-finite-face-sum-2026-07-21.json",
            }
            actual = hashlib.sha256((HERE / path_map[name]).read_bytes()).hexdigest()
            require(actual == expected, f"pin {name}")


def main() -> int:
    manifest = strict_load(MANIFEST)
    validate(manifest)
    mutation_paths = [
        ("result", "complete_depth2_physical_boundary_quotient", "physical_curve_count"),
        ("result", "complete_depth2_physical_boundary_quotient", "same_source_tangency_pair_count"),
        ("result", "complete_depth2_physical_boundary_quotient", "mixed_tangency_R1_R2_pair_count"),
        ("result", "complete_depth2_physical_boundary_quotient", "new_distinct_stationary_endpoints"),
        ("result", "fixed_s0_rank3_depth6_registry", "strict_Q3_cell_count"),
        ("result", "fixed_s0_rank3_depth6_registry", "strict_R3_cell_count"),
        ("result", "rank3_physical_boundary_seed_registry", "source_carrier_family_count"),
        ("result", "rank3_physical_boundary_seed_registry", "third_collision_tangency_source_carrier_family_count"),
        ("result", "rank3_physical_boundary_seed_registry", "third_collision_tangency_seed_incidence_count"),
        ("result", "RN_frontier", "certified_rank12_face_count"),
        ("result", "RN_frontier", "rank3_RN_face_rows"),
        ("result", "strict_state", "gate5_complete_blocks"),
    ]
    rejected = 0
    for path in mutation_paths:
        mutation = copy.deepcopy(manifest)
        target = mutation
        for key in path[:-1]:
            target = target[key]
        value = target[path[-1]]
        target[path[-1]] = value + 1 if isinstance(value, int) else f"MUTATED:{value}"
        mutation["result_sha256"] = digest(mutation["result"])
        try:
            validate(mutation, pins=False)
        except Exception:
            rejected += 1
    strict_cases = [
        '{"a":1,"a":2}',
        '{"a":NaN}',
        '{"a":Infinity}',
        '{"a":-Infinity}',
    ]
    strict_rejected = 0
    for text in strict_cases:
        try:
            strict_text(text)
        except Exception:
            strict_rejected += 1
    audit = {
        "schema": "cm2.round79.complete-quotient-rank3-audit.v1",
        "result": {
            "manifest_valid": True,
            "hostile_semantic_mutations_rejected": rejected,
            "hostile_semantic_mutation_count": len(mutation_paths),
            "strict_json_rejections": strict_rejected,
            "strict_json_case_count": len(strict_cases),
            "all_pins_verified": True,
        },
    }
    json.dump(audit, sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
