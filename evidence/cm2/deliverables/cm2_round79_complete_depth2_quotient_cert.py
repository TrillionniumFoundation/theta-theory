#!/usr/bin/env python3
"""Complete fixed-s=0 depth-two physical boundary quotient certificate."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from cm2_round79_tangency_intersection_generator import digest


HERE = Path(__file__).resolve().parent
ROUND75 = HERE / "cm2-round75-r2-physical-subquotient-manifest-2026-07-21.json"
ROUND78 = HERE / "cm2-round78-physical-boundary-rank3-manifest-2026-07-21.json"
TANGENCY = HERE / "cm2-round79-tangency-intersections-2026-07-21.json"
MIXED = HERE / "cm2-round79-mixed-carrier-intersections-2026-07-21.json"
ENDPOINTS = HERE / "cm2-round79-tangency-endpoint-separation-2026-07-21.json"
SCHEMA = "cm2.round79.complete-depth2-quotient.v1"


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build() -> dict[str, Any]:
    round75 = load(ROUND75)["result"]
    round78 = load(ROUND78)["result"]
    tangency = load(TANGENCY)["result"]
    mixed = load(MIXED)["result"]
    endpoints = load(ENDPOINTS)["result"]
    base = round75["depth_two_physical_subquotient"]
    if base["f_vector"] != [208, 256, 72]:
        raise RuntimeError("Round75 base f-vector")
    if round78["physical_boundary_carrier_atlas"]["family_histogram"] != {
        "R1_destination": 32,
        "R2_destination": 32,
        "time2_tangency": 92,
    }:
        raise RuntimeError("Round78 carrier histogram")
    if tangency["same_source_pair_count"] != 244 or tangency["unresolved_pair_count"]:
        raise RuntimeError("tangency pair coverage")
    if tangency["certified_transverse_intersection_count"]:
        raise RuntimeError("unexpected tangency intersection")
    if mixed["mixed_family_pair_count"] != 224 or mixed["unresolved_pair_count"]:
        raise RuntimeError("mixed pair coverage")
    if mixed["certified_transverse_intersection_count"]:
        raise RuntimeError("unexpected mixed intersection")
    if not endpoints["all_new_endpoints_are_distinct_from_each_other_and_old_depth2_vertices"]:
        raise RuntimeError("endpoint separation")
    new_curves = 92
    new_vertices = endpoints["tangency_endpoint_count"]
    new_stationary_segments = new_vertices
    new_pullback_edges = new_curves
    vertices = base["f_vector"][0] + new_vertices
    edges = base["f_vector"][1] + new_stationary_segments + new_pullback_edges
    cells = base["f_vector"][2] + new_curves
    if (vertices, edges, cells) != (392, 532, 164):
        raise RuntimeError("complete quotient f-vector")
    if vertices - edges + cells != 24:
        raise RuntimeError("Euler identity")
    result = {
        "fixed_parameter": "s=0",
        "physical_boundary_curve_histogram": {
            "R1_destination": 32,
            "R2_destination": 32,
            "time2_tangency": 92,
        },
        "physical_boundary_curve_count": 156,
        "all_tangency_pairs_certified_disjoint": True,
        "all_tangency_to_R1_R2_pairs_certified_disjoint": True,
        "all_tangency_endpoints_new_and_distinct": True,
        "base_R1_R2_subquotient_f_vector": base["f_vector"],
        "inserted_tangency_crosscuts": new_curves,
        "new_stationary_endpoint_vertices": new_vertices,
        "new_stationary_segments": new_stationary_segments,
        "new_pullback_edges": new_pullback_edges,
        "complete_depth2_boundary_quotient_f_vector": [vertices, edges, cells],
        "connected_physical_core_rectangles": 24,
        "euler_identity": "392-532+164=24",
        "physical_open_cell_count": cells,
        "open_cell_label_scope": "every open cell is strict off the complete Round77 failure-carrier set; an explicit 164-row R1/R2/Q2 cell-label ledger is not asserted here",
        "oriented_internal_trace_pairs": 156,
        "duplicate_trace_cost_before_total_variation": 0,
        "status": "CERTIFIED_COMPLETE_FIXED_S0_DEPTH2_PHYSICAL_BOUNDARY_QUOTIENT",
        "gate4_commuting_square": "NOT_PROMOTED__CELLWISE_LABEL_AND_MAP_INCIDENCE_LEDGER_STILL_REQUIRED",
    }
    return {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}


def main() -> int:
    json.dump(build(), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
