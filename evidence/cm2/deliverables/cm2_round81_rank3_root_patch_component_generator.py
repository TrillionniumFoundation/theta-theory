#!/usr/bin/env python3
"""Connected local root-patch registry for fully resolved rank-three carrier tubes."""
from __future__ import annotations

import json
import sys
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate25_physical_return_core_registry_cert as core_cert
from cm2_round79_tangency_intersection_generator import digest


HERE = Path(__file__).resolve().parent
RESOLUTION = HERE / "cm2-round81-time3-monotone-corner-resolution-2026-07-21.json"


def overlaps(left: tuple[Q, Q, Q, Q], right: tuple[Q, Q, Q, Q]) -> bool:
    return max(left[0], right[0]) <= min(left[1], right[1]) and max(left[2], right[2]) <= min(left[3], right[3])


def connected_components(boxes: list[tuple[Q, Q, Q, Q]]) -> list[list[int]]:
    adjacency = [[] for _ in boxes]
    for left in range(len(boxes)):
        for right in range(left + 1, len(boxes)):
            if overlaps(boxes[left], boxes[right]):
                adjacency[left].append(right)
                adjacency[right].append(left)
    remaining = set(range(len(boxes)))
    rows = []
    while remaining:
        seed = min(remaining)
        remaining.remove(seed)
        stack = [seed]
        component = []
        while stack:
            current = stack.pop()
            component.append(current)
            for neighbor in adjacency[current]:
                if neighbor in remaining:
                    remaining.remove(neighbor)
                    stack.append(neighbor)
        component.sort()
        rows.append(component)
    rows.sort(key=lambda row: row[0])
    return rows


def build() -> dict[str, Any]:
    cores = core_cert.physical_cores()
    document = json.loads(RESOLUTION.read_text())["result"]
    patch_rows = []
    false_rows = []
    for component in document["component_rows"]:
        if component["unique_root_slab_count"] == 0:
            false_rows.append({
                "representative_component_id": component["representative_component_id"],
                "orbit_size": component["orbit_size"],
                "strictly_false_tube": True,
            })
            continue
        boxes = [tuple(map(Q, row["box"])) for row in component["root_slabs"]]
        source = cores[component["source_core_index"]]
        for rank, indices in enumerate(connected_components(boxes)):
            selected = [boxes[index] for index in indices]
            sides = set()
            for t0, t1, p0, p1 in selected:
                if t0 == source.t0:
                    sides.add("t_lower")
                if t1 == source.t1:
                    sides.add("t_upper")
                if p0 == source.p0:
                    sides.add("p_lower")
                if p1 == source.p1:
                    sides.add("p_upper")
            identity = {"component": component["representative_component_id"], "patch_rank": rank}
            patch_rows.append({
                "patch_id": "physical-s0-rank3-root-patch:" + digest(identity),
                "representative_component_id": component["representative_component_id"],
                "source_core_index": component["source_core_index"],
                "second_selected_target_id": component["second_selected_target_id"],
                "third_candidate_id": component["third_candidate_id"],
                "patch_rank_within_tube": rank,
                "orbit_size": component["orbit_size"],
                "root_slab_count": len(indices),
                "source_boundary_sides_touched": sorted(sides),
                "source_boundary_side_count": len(sides),
                "root_slab_indices_sha256": digest(indices),
            })
    patch_rows.sort(key=lambda row: row["patch_id"])
    false_rows.sort(key=lambda row: row["representative_component_id"])
    side_histogram = Counter(row["source_boundary_side_count"] for row in patch_rows)
    result = {
        "fully_resolved_input_representative_count": document["fully_resolved_representative_component_count"],
        "false_tube_representative_count": len(false_rows),
        "false_tube_component_count_symmetry_expanded": sum(row["orbit_size"] for row in false_rows),
        "root_bearing_tube_representative_count": document["representatives_with_physical_root_slabs"],
        "local_connected_root_patch_count": len(patch_rows),
        "local_connected_root_patch_count_symmetry_expanded": sum(row["orbit_size"] for row in patch_rows),
        "boundary_side_count_histogram": {str(key): value for key, value in sorted(side_histogram.items())},
        "patch_rows": patch_rows,
        "patch_rows_sha256": digest(patch_rows),
        "false_rows_sha256": digest(false_rows),
        "strict_scope": "connected components of certified local root slabs inside each symmetry representative tube; cross-tube joining and physical endpoint certification are not asserted",
    }
    return {"schema": "cm2.round81.rank3-root-patches.v1", "result": result, "result_sha256": digest(result)}


def main() -> int:
    json.dump(build(), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
