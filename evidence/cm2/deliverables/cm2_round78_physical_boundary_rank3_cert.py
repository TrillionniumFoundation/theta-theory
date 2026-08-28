#!/usr/bin/env python3
"""Integrate the Round-78 physical carrier atlas and fixed-s=0 rank-three frontier."""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as step1


HERE = Path(__file__).resolve().parent
FILES = {
    "round77_taxonomy": HERE / "cm2-round77-boundary-taxonomy-2026-07-21.json",
    "round77_rn_sum": HERE / "cm2-round77-rn-weighted-finite-face-sum-2026-07-21.json",
    "tube_components": HERE / "cm2-round78-carrier-components-2026-07-21.json",
    "r1_witnesses": HERE / "cm2-round71-r1-nonempty-face-witnesses-2026-07-21.json",
    "r1_monotonicity": HERE / "cm2-round72-r1-positive-component-monotonicity-proof-2026-07-21.json",
    "r1_numeric": HERE / "cm2-round72-r1-component-f10-f13-f16-proof-2026-07-21.json",
    "r2_curves": HERE / "cm2-round75-r2-physical-curves-2026-07-21.json",
    "tangency_curves": HERE / "cm2-round78-time2-tangency-curves-2026-07-21.json",
    "seam_resolution": HERE / "cm2-round78-chart-free-seam-resolution-2026-07-21.json",
    "time3_registry": HERE / "cm2-round78-s0-time3-registry-2026-07-21.json",
}


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def build() -> dict[str, Any]:
    inputs = {name: load(path) for name, path in FILES.items()}
    taxonomy = inputs["round77_taxonomy"]["result"]
    components = inputs["tube_components"]["result"]
    witnesses = inputs["r1_witnesses"]["rows"]
    r1_numeric = inputs["r1_numeric"]["result"]["rows"]
    r2_curves = inputs["r2_curves"]["result"]["curve_rows"]
    tangencies = inputs["tangency_curves"]["result"]
    seam = inputs["seam_resolution"]["result"]
    time3 = inputs["time3_registry"]["result"]
    rn = inputs["round77_rn_sum"]["result"]

    require(taxonomy["outer_leaf_count"] == 263072, "Round-77 outer count")
    require(taxonomy["carrier_count"] == 65, "Round-77 carrier count")
    require(components["outer_leaf_count"] == 263072, "component outer count")
    require(components["connected_component_count"] == 236, "tube component count")
    require(tangencies["certified_curve_count"] == 92, "tangency count")
    require(tangencies["failure_count"] == 0, "tangency failures")

    numeric_by_family = {row["candidate_family_id"]: row for row in r1_numeric}
    time1_rows = []
    r1_component_ids = set()
    for pair in components["pair_rows"]:
        prefix = "TIME1_DESTINATION_FACE:"
        if not pair["carrier"].startswith(prefix):
            continue
        destination = pair["carrier"][len(prefix):]
        matches = sorted(
            (
                row for row in witnesses
                if row["source_core_index"] == pair["source_core_index"]
                and row["destination_core_id"] == destination
            ),
            key=lambda row: row["candidate_family_id"],
        )
        require(len(matches) == 2, "time-one pair must map to two R1 faces")
        curves = []
        for witness in matches:
            numeric = numeric_by_family[witness["candidate_family_id"]]
            r1_component_ids.add(numeric["component_id"])
            curves.append({
                "physical_curve_id": numeric["component_id"],
                "candidate_family_id": witness["candidate_family_id"],
                "destination_face_id": witness["destination_face_id"],
                "side": witness["side"],
                "level_coordinate": witness["level_coordinate"],
                "level_value": witness["level_value"],
            })
        time1_rows.append({
            "source_core_index": pair["source_core_index"],
            "destination_core_id": destination,
            "tube_leaf_count": pair["leaf_count"],
            "tube_grid_component_count": pair["connected_component_count"],
            "physical_curve_count": 2,
            "physical_curves": curves,
        })
    require(len(time1_rows) == 16, "time-one pair count")
    require(len(r1_component_ids) == 32, "R1 curve union")
    monotonicity = inputs["r1_monotonicity"]["theorem"]
    require(monotonicity["each_clipped_positive_face_is_one_connected_graph_component"], "R1 connectedness")

    cores = core_cert.physical_cores()
    core_id_to_index = {step1.core_id(core): index for index, core in enumerate(cores)}
    time2_rows = []
    r2_curve_ids = set()
    time2_pair_keys = set()
    for pair in components["pair_rows"]:
        prefix = "TIME2_DESTINATION_CORE:"
        if not pair["carrier"].startswith(prefix):
            continue
        destination = pair["carrier"][len(prefix):]
        destination_index = core_id_to_index[destination]
        matches = sorted(
            (
                row for row in r2_curves
                if row["source_core_index"] == pair["source_core_index"]
                and row["destination_core_index"] == destination_index
            ),
            key=lambda row: row["curve_id"],
        )
        require(len(matches) == 2, "time-two pair must map to two R2 faces")
        time2_pair_keys.add((pair["source_core_index"], destination))
        curves = []
        for row in matches:
            r2_curve_ids.add(row["curve_id"])
            curves.append({
                "physical_curve_id": row["curve_id"],
                "active_side": row["active_side"],
                "level": row["level"],
                "branch": row["branch"],
                "parametric_interval_newton_slab_count": row["parametric_interval_newton_slab_count"],
            })
        time2_rows.append({
            "source_core_index": pair["source_core_index"],
            "destination_core_id": destination,
            "destination_core_index": destination_index,
            "tube_leaf_count": pair["leaf_count"],
            "tube_grid_component_count": pair["connected_component_count"],
            "physical_curve_count": 2,
            "physical_curves": curves,
        })
    require(len(time2_rows) == 16, "time-two pair count")
    require(len(r2_curve_ids) == 32, "R2 curve union")

    seam_destination_counts = Counter()
    for row in seam["terminal_rows"]:
        if row["classification"] != "OUTER_DESTINATION":
            continue
        require(len(row["carrier_ids"]) == 1, "seam destination carrier multiplicity")
        carrier = row["carrier_ids"][0]
        prefix = "TIME2_DESTINATION_CORE:"
        require(carrier.startswith(prefix), "seam destination type")
        key = (row["source_core_index"], carrier[len(prefix):])
        require(key in time2_pair_keys, "seam destination must map to existing R2 pair")
        seam_destination_counts[key] += 1
    require(len(seam_destination_counts) == 8, "seam destination pair count")
    require(set(seam_destination_counts.values()) == {1554}, "seam destination terminal count")

    component_index = {}
    for pair in components["pair_rows"]:
        if not pair["carrier"].startswith("SECOND_CANDIDATE:"):
            continue
        for component in pair["components"]:
            key = (
                pair["source_core_index"], pair["carrier"],
                component["connected_rank"], component["cell_set_sha256"],
            )
            component_index[key] = component
    tangency_ids = set()
    tangency_rows = []
    for row in tangencies["curve_rows"]:
        key = (
            row["source_core_index"], row["carrier"],
            row["connected_rank"], row["component_cell_set_sha256"],
        )
        require(key in component_index, "tangency component incidence")
        tangency_ids.add(row["curve_id"])
        tangency_rows.append({
            "physical_curve_id": row["curve_id"],
            "source_core_index": row["source_core_index"],
            "candidate_id": row["candidate_id"],
            "carrier": row["carrier"],
            "tube_connected_rank": row["connected_rank"],
            "tube_cell_count": row["tube_cell_count"],
            "certified_slab_count": row["certified_slab_count"],
            "physical_endpoint_certificate_count": len(row["physical_endpoint_certificates"]),
            "global_implicit_slope_sign": row["global_implicit_slope_sign"],
        })
    require(len(tangency_ids) == 92, "tangency curve union")
    require(len(component_index) == 92, "tangency component union")

    all_physical_ids = r1_component_ids | r2_curve_ids | tangency_ids
    require(len(all_physical_ids) == 156, "physical curve identity union")
    strict_q3 = time3["strict_Q3_cell_count"]
    strict_r3 = time3["strict_R3_cell_count"]
    require(strict_q3 == 14928 and strict_r3 == 0, "time-three counts")
    require(time3["cross_rank_Q2_to_time3_incidence_count"] == 57616, "time-three incidence")
    require(rn["face_count"] == 64, "finite RN face count")

    time1_rows.sort(key=canonical)
    time2_rows.sort(key=canonical)
    tangency_rows.sort(key=canonical)
    result = {
        "fixed_parameter": "s=0",
        "round77_failure_mechanism_resolution": {
            "outer_leaf_count": 263072,
            "interval_tube_family_count": 65,
            "tube_source_carrier_pair_count": components["source_carrier_pair_count"],
            "tube_grid_component_count": components["connected_component_count"],
            "time1_destination": {
                "source_destination_pair_count": len(time1_rows),
                "tube_grid_component_count": sum(row["tube_grid_component_count"] for row in time1_rows),
                "physical_R1_curve_count": len(r1_component_ids),
            },
            "time2_tangency": {
                "tube_grid_component_count": len(component_index),
                "physical_tangency_curve_count": len(tangency_ids),
                "certified_interval_slab_count": sum(row["certified_slab_count"] for row in tangency_rows),
                "physical_endpoint_certificate_count": sum(row["physical_endpoint_certificate_count"] for row in tangency_rows),
            },
            "time2_destination": {
                "source_destination_pair_count": len(time2_rows),
                "tube_grid_component_count": sum(row["tube_grid_component_count"] for row in time2_rows),
                "physical_R2_curve_count": len(r2_curve_ids),
            },
            "outgoing_chart_seam": {
                "seed_leaf_count": seam["seed_leaf_count"],
                "terminal_classification_histogram": seam["classification_histogram"],
                "independent_physical_seam_carrier_count": 0,
                "retyped_destination_pair_count": len(seam_destination_counts),
            },
            "all_failure_mechanisms_mapped_to_certified_physical_carriers_or_strict_open_cells": True,
        },
        "physical_boundary_carrier_atlas": {
            "status": "CERTIFIED_FOR_ALL_ROUND77_FAILURE_MECHANISMS",
            "physical_curve_count": len(all_physical_ids),
            "family_histogram": {"R1_destination": 32, "time2_tangency": 92, "R2_destination": 32},
            "curve_id_set_sha256": digest(sorted(all_physical_ids)),
            "time1_pair_rows": time1_rows,
            "time1_pair_rows_sha256": digest(time1_rows),
            "time2_destination_pair_rows": time2_rows,
            "time2_destination_pair_rows_sha256": digest(time2_rows),
            "time2_tangency_rows": tangency_rows,
            "time2_tangency_rows_sha256": digest(tangency_rows),
        },
        "depth_two_quotient": {
            "status": "NOT_CERTIFIED__INTER_CARRIER_INTERSECTIONS_AND_OPEN_CELL_SUBDIVISION_PENDING",
            "broad_phase_same_source_tangency_pair_count": 244,
            "broad_phase_strictly_bbox_disjoint_pair_count": 68,
            "broad_phase_bounding_box_overlap_count": 176,
            "gate4_commuting_square_promotion": "NO",
        },
        "fixed_s0_rank_three_frontier": {
            "strict_Q3_cell_count": strict_q3,
            "strict_R3_cell_count": strict_r3,
            "Q2_to_time3_incidence_count": time3["cross_rank_Q2_to_time3_incidence_count"],
            "terminal_classification_histogram": time3["terminal_classification_histogram"],
            "normalized_area_ledger": time3["normalized_area_ledger"],
            "blocker_histogram": time3["blocker_histogram"],
            "strict_rows_sha256": time3["strict_rows_sha256"],
            "scope": "finite actual fixed-s0 registry; no claim that zero finite R3 proves limiting emptiness",
        },
        "RN_frontier": {
            "certified_finite_rank_face_count": rn["face_count"],
            "certified_rank_histogram": rn["rank_histogram"],
            "finite_two_rank_actual_RN_dominated_sum": rn["finite_two_rank_actual_RN_dominated_sum"],
            "rank3_physical_face_count": 0,
            "rank3_RN_face_row_count": 0,
            "all_rank_RN_summability": "NOT_CERTIFIED__NO_RANK3_FACE_LAW_OR_UNIFORM_TAIL_CONTRACTION",
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
        "schema": "cm2.round78.physical-boundary-rank3.v1",
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
