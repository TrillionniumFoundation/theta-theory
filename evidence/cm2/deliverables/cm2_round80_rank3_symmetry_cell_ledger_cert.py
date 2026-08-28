#!/usr/bin/env python3
"""Round-80 integration: rank-three symmetry/continuation and depth-two cell ledger."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from cm2_round79_tangency_intersection_generator import digest


HERE = Path(__file__).resolve().parent
FILES = {
    "round79": HERE / "cm2-round79-complete-quotient-rank3-manifest-2026-07-21.json",
    "components": HERE / "cm2-round80-time3-carrier-components-2026-07-21.json",
    "symmetry": HERE / "cm2-round80-time3-dihedral-quotient-2026-07-21.json",
    "geometry": HERE / "cm2-round80-time3-carrier-geometry-2026-07-21.json",
    "curves": HERE / "cm2-round80-time3-tangency-curves-2026-07-21.json",
    "adaptive": HERE / "cm2-round80-time3-adaptive-carrier-resolution-2026-07-21.json",
    "cell_ledger": HERE / "cm2-round80-depth2-cell-label-ledger-2026-07-21.json",
    "rn_rank12": HERE / "cm2-round77-rn-weighted-finite-face-sum-2026-07-21.json",
}


def load(name: str) -> dict[str, Any]:
    return json.loads(FILES[name].read_text())["result"]


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build() -> dict[str, Any]:
    components = load("components")
    symmetry = load("symmetry")
    geometry = load("geometry")
    curves = load("curves")
    adaptive = load("adaptive")
    cells = load("cell_ledger")
    rn = load("rn_rank12")
    if components["physical_third_tangency_component_count"] != 1536:
        raise RuntimeError("physical component count")
    if symmetry["component_orbit_count"] != 552:
        raise RuntimeError("symmetry orbit count")
    if geometry["second_owner_outgoing_branch_count"] != 14:
        raise RuntimeError("second branch count")
    if curves["symmetry_expanded_certified_curve_count"] != 532:
        raise RuntimeError("certified curve count")
    false_expanded = sum(
        row["orbit_size"] for row in adaptive["component_rows"]
        if row["unique_root_slab_count"] == 0 and row["unresolved_leaf_count"] == 0
    )
    unresolved_expanded = sum(
        row["orbit_size"] for row in adaptive["component_rows"]
        if row["unresolved_leaf_count"] > 0
    )
    if (false_expanded, unresolved_expanded) != (336, 668):
        raise RuntimeError("adaptive expanded ledger")
    if cells["cell_label_histogram"] != {"Q2": 132, "R1": 16, "R2": 16}:
        raise RuntimeError("depth-two cell labels")
    result = {
        "fixed_parameter": "s=0",
        "rank3_carrier_component_atlas": {
            "source_carrier_family_count": components["source_carrier_family_count"],
            "all_connected_component_count": components["connected_component_count"],
            "physical_third_tangency_component_count": components["physical_third_tangency_component_count"],
            "grid_shape_per_core": components["grid_shape_per_core"],
        },
        "exact_symmetry_quotient": {
            "action": symmetry["symmetry_group"],
            "physical_component_count": symmetry["physical_component_count"],
            "representative_orbit_count": symmetry["component_orbit_count"],
            "orbit_size_histogram": symmetry["orbit_size_histogram"],
            "D4_orbits": sum(row["sector_symmetry"] == "D4" for row in symmetry["orbit_rows"]),
            "radial_C2_orbits": sum(row["sector_symmetry"] == "C2_diagonal_reflection" for row in symmetry["orbit_rows"]),
            "all_grid_sets_mapped_exactly": symmetry["all_component_grid_sets_mapped_exactly"],
        },
        "rank3_physical_continuation": {
            "second_owner_outgoing_branch_count": geometry["second_owner_outgoing_branch_count"],
            "branch_homogeneous_physical_components": 1536,
            "globally_graph_certified_representative_curves": curves["certified_representative_curve_count"],
            "globally_graph_certified_symmetry_expanded_curves": curves["symmetry_expanded_certified_curve_count"],
            "global_graph_interval_slabs": curves["certified_slab_count"],
            "adaptively_proved_false_tube_representatives": adaptive["representatives_proved_entirely_false_tube"],
            "adaptively_proved_false_tube_components_expanded": false_expanded,
            "additional_root_bearing_representatives": adaptive["representatives_with_physical_root_slabs"],
            "additional_root_bearing_components_expanded": adaptive["symmetry_expanded_root_bearing_component_count"],
            "additional_unique_root_slabs": adaptive["total_unique_root_slabs"],
            "adaptive_interval_box_tests": adaptive["total_interval_box_tests"],
            "remaining_unresolved_representatives": adaptive["remaining_unresolved_representative_component_count"],
            "remaining_unresolved_components_expanded": unresolved_expanded,
            "remaining_unresolved_leaves": adaptive["total_unresolved_leaves"],
            "strict_status": "PARTIAL__532_COMPLETE_GRAPH_CURVES_PLUS_508_ROOT_BEARING_COMPONENTS__668_COMPONENTS_STILL_HAVE_UNRESOLVED_LEAVES",
        },
        "complete_depth2_cell_ledger": {
            "cell_count": cells["cell_count"],
            "cell_label_histogram": cells["cell_label_histogram"],
            "tangency_face_incidence_count": cells["tangency_face_incidence_count"],
            "two_sided_strict_Q2_incidence_count": cells["two_sided_strict_Q2_incidence_count"],
            "same_owner_both_sides_count": cells["same_owner_both_sides_count"],
            "owner_switching_tangency_face_count": cells["tangency_face_incidence_count"] - cells["same_owner_both_sides_count"],
            "exact_Q2_cyclic_boundary_words": "NOT_CERTIFIED",
            "gate4_commuting_square": cells["gate4_commuting_square"],
        },
        "RN_frontier": {
            "certified_rank12_return_face_rows": rn["face_count"],
            "finite_rank12_actual_RN_dominated_sum": rn["finite_two_rank_actual_RN_dominated_sum"],
            "finite_depth6_strict_R3_cells": 0,
            "rank3_return_face_RN_rows": 0,
            "rank3_tangency_subdivision_faces_are_not_renamed_return_faces": True,
            "uniform_rank_tail_contraction": "NOT_CERTIFIED",
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
        "schema": "cm2.round80.rank3-symmetry-cell-ledger.v1",
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
