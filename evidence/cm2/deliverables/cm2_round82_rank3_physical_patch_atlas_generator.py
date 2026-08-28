#!/usr/bin/env python3
"""Expand every certified rank-three root patch to the physical symmetry atlas."""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_round80_time3_dihedral_quotient_generator as symmetry
from cm2_round79_tangency_intersection_generator import digest
from cm2_round81_rank3_root_patch_component_generator import connected_components, overlaps


HERE = Path(__file__).resolve().parent
QUOTIENT = HERE / "cm2-round80-time3-dihedral-quotient-2026-07-21.json"
COMPONENTS = HERE / "cm2-round80-time3-carrier-components-2026-07-21.json"
CURVES = HERE / "cm2-round80-time3-tangency-curves-2026-07-21.json"
RESOLUTION = HERE / "cm2-round81-time3-monotone-corner-resolution-2026-07-21.json"


def transform_interval(lower: Q, upper: Q, sign: int) -> tuple[Q, Q]:
    return (lower, upper) if sign == 1 else (-upper, -lower)


def transform_box(box: tuple[Q, Q, Q, Q], t_sign: int, p_sign: int) -> tuple[Q, Q, Q, Q]:
    t0, t1 = transform_interval(box[0], box[1], t_sign)
    p0, p1 = transform_interval(box[2], box[3], p_sign)
    return t0, t1, p0, p1


def slab_box(row: dict[str, Any], root_axis: str) -> tuple[Q, Q, Q, Q]:
    root = tuple(map(Q, row["root_interval"]))
    parameter = tuple(map(Q, row["parameter_interval"]))
    return (*root, *parameter) if root_axis == "t" else (*parameter, *root)


def physical_action_names(cores: tuple[Any, ...]) -> dict[tuple[str, str], list[str]]:
    document = json.loads(COMPONENTS.read_text())["result"]
    records = {}
    lookup = {}
    for pair in document["pair_rows"]:
        if not pair["carrier"].startswith("THIRD_CANDIDATE:"):
            continue
        for component in pair["components"]:
            identifier = symmetry.component_id(pair["source_core_index"], pair["carrier"], component["connected_rank"])
            cells = frozenset(map(tuple, component["cell_set"]))
            records[identifier] = (pair["source_core_index"], pair["carrier"], cells)
            lookup[(pair["source_core_index"], pair["carrier"], cells)] = identifier
    core_actions = symmetry.core_action()
    action_names: dict[tuple[str, str], list[str]] = defaultdict(list)
    for identifier, (source_index, carrier, cells) in records.items():
        source_type = cores[source_index].source
        candidate = symmetry.candidate_from_carrier(carrier)
        source_target_type = cores[source_index].target_id[0]
        names = list(symmetry.MATRICES) if source_type != source_target_type else ["identity", "reflect_diag"]
        for name in names:
            matrix = symmetry.MATRICES[name]
            target_source, t_sign, p_sign = core_actions[(source_index, name)]
            target_candidate = symmetry.transform_obstacle(candidate, source_type, matrix)
            target_carrier = f"THIRD_CANDIDATE:{target_candidate}:unresolved_discriminant"
            transformed_cells = frozenset(
                (i if t_sign == 1 else 63 - i, j if p_sign == 1 else 63 - j)
                for i, j in cells
            )
            member = lookup[(target_source, target_carrier, transformed_cells)]
            action_names[(identifier, member)].append(name)
    return action_names


def build() -> dict[str, Any]:
    cores = core_cert.physical_cores()
    orbit_document = json.loads(QUOTIENT.read_text())["result"]
    orbits = {row["representative_component_id"]: row for row in orbit_document["orbit_rows"]}
    action_names = physical_action_names(cores)
    core_actions = symmetry.core_action()
    physical_rows = []

    def expand(
        representative_component_id: str,
        representative_patch_rank: int,
        source_index: int,
        second_target: str,
        outgoing_chart: str,
        candidate: str,
        boxes: list[tuple[Q, Q, Q, Q]],
        certification_source: str,
    ) -> None:
        orbit = orbits[representative_component_id]
        source_type = cores[source_index].source
        for member in orbit["member_component_ids"]:
            name = min(action_names[(representative_component_id, member)])
            matrix = symmetry.MATRICES[name]
            target_source, t_sign, p_sign = core_actions[(source_index, name)]
            transformed_boxes = sorted(transform_box(box, t_sign, p_sign) for box in boxes)
            transformed_second = symmetry.transform_obstacle(second_target, source_type, matrix)
            transformed_candidate = symmetry.transform_obstacle(candidate, source_type, matrix)
            transformed_chart, _chart_sign = symmetry.chart_action(outgoing_chart, matrix)
            identity = {
                "member_component_id": member,
                "representative_patch_rank": representative_patch_rank,
                "symmetry": name,
                "certification_source": certification_source,
            }
            physical_rows.append({
                "physical_patch_id": "physical-s0-rank3-patch:" + digest(identity),
                "member_component_id": member,
                "representative_component_id": representative_component_id,
                "representative_patch_rank": representative_patch_rank,
                "certification_source": certification_source,
                "symmetry": name,
                "source_core_index": target_source,
                "second_selected_target_id": transformed_second,
                "second_outgoing_chart": transformed_chart,
                "third_candidate_id": transformed_candidate,
                "box_count": len(transformed_boxes),
                "boxes": [list(map(str, box)) for box in transformed_boxes],
                "boxes_sha256": digest([list(map(str, box)) for box in transformed_boxes]),
                "bbox": list(map(str, (
                    min(box[0] for box in transformed_boxes), max(box[1] for box in transformed_boxes),
                    min(box[2] for box in transformed_boxes), max(box[3] for box in transformed_boxes),
                ))),
            })

    curves = json.loads(CURVES.read_text())["result"]
    for row in curves["curve_rows"]:
        boxes = [slab_box(slab, row["root_axis"]) for slab in row["slabs"]]
        expand(
            row["representative_component_id"], 0, row["source_core_index"],
            row["second_selected_target_id"], row["second_outgoing_chart"],
            row["third_candidate_id"], boxes, "ROUND80_COMPLETE_GRAPH",
        )

    resolution = json.loads(RESOLUTION.read_text())["result"]
    for row in resolution["component_rows"]:
        boxes = [tuple(map(Q, slab["box"])) for slab in row["root_slabs"]]
        for rank, indices in enumerate(connected_components(boxes)):
            expand(
                row["representative_component_id"], rank, row["source_core_index"],
                row["second_selected_target_id"], row["second_outgoing_chart"],
                row["third_candidate_id"], [boxes[index] for index in indices],
                "ROUND81_CENTERED_TAYLOR_LOCAL_PATCH",
            )

    physical_rows.sort(key=lambda row: row["physical_patch_id"])
    by_branch: dict[tuple[int, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in physical_rows:
        by_branch[(row["source_core_index"], row["second_selected_target_id"], row["third_candidate_id"])].append(row)
    bbox_overlap_pairs = 0
    certified_box_overlap_pairs = 0
    cross_tube_certified_box_overlap_pairs = 0
    for rows in by_branch.values():
        for left_index in range(len(rows)):
            left = rows[left_index]
            left_bbox = tuple(map(Q, left["bbox"]))
            left_boxes = [tuple(map(Q, box)) for box in left["boxes"]]
            for right in rows[left_index + 1:]:
                if not overlaps(left_bbox, tuple(map(Q, right["bbox"]))):
                    continue
                bbox_overlap_pairs += 1
                right_boxes = [tuple(map(Q, box)) for box in right["boxes"]]
                if any(overlaps(a, b) for a in left_boxes for b in right_boxes):
                    certified_box_overlap_pairs += 1
                    if left["member_component_id"] != right["member_component_id"]:
                        cross_tube_certified_box_overlap_pairs += 1
    source_histogram = Counter(row["source_core_index"] for row in physical_rows)
    certification_histogram = Counter(row["certification_source"] for row in physical_rows)
    result = {
        "fixed_parameter": "s=0",
        "physical_patch_count": len(physical_rows),
        "physical_patch_certification_histogram": dict(sorted(certification_histogram.items())),
        "source_core_patch_count_histogram": {str(key): value for key, value in sorted(source_histogram.items())},
        "physical_branch_key_count": len(by_branch),
        "same_branch_bbox_overlap_pair_count": bbox_overlap_pairs,
        "same_branch_certified_box_overlap_pair_count": certified_box_overlap_pairs,
        "cross_tube_certified_box_overlap_pair_count": cross_tube_certified_box_overlap_pairs,
        "physical_patch_rows": physical_rows,
        "physical_patch_rows_sha256": digest(physical_rows),
        "strict_scope": "symmetry-expanded certified rank-three root boxes; absence of certified box overlap does not by itself certify global face separation across uncovered gaps",
    }
    if len(physical_rows) != 1780:
        raise RuntimeError("physical patch count")
    if certification_histogram != {"ROUND80_COMPLETE_GRAPH": 532, "ROUND81_CENTERED_TAYLOR_LOCAL_PATCH": 1248}:
        raise RuntimeError("physical patch source histogram")
    return {"schema": "cm2.round82.rank3-physical-patch-atlas.v1", "result": result, "result_sha256": digest(result)}


def main() -> int:
    json.dump(build(), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
