#!/usr/bin/env python3
"""Independent hostile-semantic verifier for CM2 Round 80."""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "cm2-round80-rank3-symmetry-cell-ledger-manifest-2026-07-21.json"


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
    require(document["schema"] == "cm2.round80.rank3-symmetry-cell-ledger.v1", "schema")
    require(document["result_sha256"] == digest(document["result"]), "digest")
    result = document["result"]
    atlas = result["rank3_carrier_component_atlas"]
    require(atlas["physical_third_tangency_component_count"] == 1536, "components")
    symmetry = result["exact_symmetry_quotient"]
    require(symmetry["representative_orbit_count"] == 552, "orbits")
    require(symmetry["orbit_size_histogram"] == {"2": 480, "8": 72}, "orbit histogram")
    require(symmetry["D4_orbits"] == 72 and symmetry["radial_C2_orbits"] == 480, "sector orbits")
    continuation = result["rank3_physical_continuation"]
    require(continuation["second_owner_outgoing_branch_count"] == 14, "branches")
    require(continuation["globally_graph_certified_symmetry_expanded_curves"] == 532, "global curves")
    require(continuation["adaptively_proved_false_tube_components_expanded"] == 336, "false tubes")
    require(continuation["additional_root_bearing_components_expanded"] == 508, "root components")
    require(continuation["remaining_unresolved_components_expanded"] == 668, "unresolved components")
    require(continuation["additional_unique_root_slabs"] == 16996, "root slabs")
    cells = result["complete_depth2_cell_ledger"]
    require(cells["cell_count"] == 164, "cells")
    require(cells["cell_label_histogram"] == {"Q2": 132, "R1": 16, "R2": 16}, "cell labels")
    require(cells["two_sided_strict_Q2_incidence_count"] == 92, "Q2 incidence")
    require(cells["owner_switching_tangency_face_count"] == 4, "owner switches")
    rn = result["RN_frontier"]
    require(rn["certified_rank12_return_face_rows"] == 64, "RN rows")
    require(rn["rank3_return_face_RN_rows"] == 0, "rank3 RN")
    require(result["strict_state"]["CM2"] == "NO-GO_FOR_CLAIM", "CM2 state")
    if pins:
        file_map = {
            "round79": "cm2-round79-complete-quotient-rank3-manifest-2026-07-21.json",
            "components": "cm2-round80-time3-carrier-components-2026-07-21.json",
            "symmetry": "cm2-round80-time3-dihedral-quotient-2026-07-21.json",
            "geometry": "cm2-round80-time3-carrier-geometry-2026-07-21.json",
            "curves": "cm2-round80-time3-tangency-curves-2026-07-21.json",
            "adaptive": "cm2-round80-time3-adaptive-carrier-resolution-2026-07-21.json",
            "cell_ledger": "cm2-round80-depth2-cell-label-ledger-2026-07-21.json",
            "rn_rank12": "cm2-round77-rn-weighted-finite-face-sum-2026-07-21.json",
        }
        for name, expected in document["pins"].items():
            require(hashlib.sha256((HERE / file_map[name]).read_bytes()).hexdigest() == expected, f"pin {name}")


def main() -> int:
    document = strict_text(MANIFEST.read_text())
    validate(document)
    paths = [
        ("rank3_carrier_component_atlas", "physical_third_tangency_component_count"),
        ("exact_symmetry_quotient", "representative_orbit_count"),
        ("exact_symmetry_quotient", "D4_orbits"),
        ("exact_symmetry_quotient", "radial_C2_orbits"),
        ("rank3_physical_continuation", "second_owner_outgoing_branch_count"),
        ("rank3_physical_continuation", "globally_graph_certified_symmetry_expanded_curves"),
        ("rank3_physical_continuation", "adaptively_proved_false_tube_components_expanded"),
        ("rank3_physical_continuation", "additional_root_bearing_components_expanded"),
        ("rank3_physical_continuation", "remaining_unresolved_components_expanded"),
        ("rank3_physical_continuation", "additional_unique_root_slabs"),
        ("complete_depth2_cell_ledger", "cell_count"),
        ("complete_depth2_cell_ledger", "two_sided_strict_Q2_incidence_count"),
        ("complete_depth2_cell_ledger", "owner_switching_tangency_face_count"),
        ("RN_frontier", "certified_rank12_return_face_rows"),
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
        "schema": "cm2.round80.rank3-symmetry-cell-ledger-audit.v1",
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
