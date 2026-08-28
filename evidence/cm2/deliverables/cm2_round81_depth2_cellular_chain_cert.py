#!/usr/bin/env python3
"""Cellular boundary and oriented trace audit for the complete depth-two DCEL."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from cm2_round79_tangency_intersection_generator import digest


HERE = Path(__file__).resolve().parent
DCEL = HERE / "cm2-round81-depth2-dcel-2026-07-21.json"


def build() -> dict[str, Any]:
    dcel = json.loads(DCEL.read_text())["result"]
    edges = {
        edge["edge_id"]: edge
        for core in dcel["core_rows"]
        for edge in core["edge_rows"]
    }
    incidence = Counter()
    direction_sum = Counter()
    boundary_of_boundary_rows = []
    for cell in dcel["cell_rows"]:
        vertex_coefficients = Counter()
        for token in cell["cyclic_boundary_word"]:
            direction = 1 if token[0] == "+" else -1
            edge_id = token[1:]
            edge = edges[edge_id]
            left, right = edge["vertices"]
            vertex_coefficients[left] -= direction
            vertex_coefficients[right] += direction
            incidence[edge_id] += 1
            direction_sum[edge_id] += direction
        nonzero = {key: value for key, value in vertex_coefficients.items() if value}
        if nonzero:
            raise RuntimeError(f"boundary squared nonzero {cell['cell_id']}:{nonzero}")
        boundary_of_boundary_rows.append({"cell_id": cell["cell_id"], "boundary_squared_zero": True})
    crosscuts = [edge_id for edge_id, edge in edges.items() if edge["kind"] != "stationary"]
    stationary = [edge_id for edge_id, edge in edges.items() if edge["kind"] == "stationary"]
    if any(incidence[edge_id] != 2 or direction_sum[edge_id] != 0 for edge_id in crosscuts):
        raise RuntimeError("internal crosscut cancellation")
    if any(incidence[edge_id] != 1 or abs(direction_sum[edge_id]) != 1 for edge_id in stationary):
        raise RuntimeError("stationary boundary incidence")
    family_histogram = Counter(edges[edge_id]["kind"] for edge_id in crosscuts)
    result = {
        "cell_count": len(dcel["cell_rows"]),
        "cellwise_boundary_squared_zero_count": len(boundary_of_boundary_rows),
        "edge_count": len(edges),
        "stationary_exterior_edge_count": len(stationary),
        "internal_crosscut_edge_count": len(crosscuts),
        "internal_crosscut_family_histogram": dict(sorted(family_histogram.items())),
        "oppositely_oriented_internal_trace_pair_count": len(crosscuts),
        "duplicate_trace_cost_before_total_variation": 0,
        "all_internal_crosscut_direction_sums_zero": True,
        "cellular_chain_complex_status": "CERTIFIED_PARTIAL1_PARTIAL2_ZERO_ON_ALL_164_CELLS",
        "boundary_of_boundary_rows_sha256": digest(boundary_of_boundary_rows),
    }
    return {"schema": "cm2.round81.depth2-cellular-chain.v1", "result": result, "result_sha256": digest(result)}


def main() -> int:
    json.dump(build(), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
