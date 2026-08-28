#!/usr/bin/env python3
"""Certify all overlapping cross-tube joins in the physical rank-three patch atlas."""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
from cm2_round79_tangency_intersection_generator import digest
from cm2_round80_time3_adaptive_carrier_resolver import centered_taylor, root_slab, strict_sign, third_tangency_jet
from cm2_round81_rank3_root_patch_component_generator import overlaps


HERE = Path(__file__).resolve().parent
ATLAS = HERE / "cm2-round82-rank3-physical-patch-atlas-2026-07-21.json"
ctx.prec = 512


def intersection(left: tuple[Q, Q, Q, Q], right: tuple[Q, Q, Q, Q]) -> tuple[Q, Q, Q, Q] | None:
    result = max(left[0], right[0]), min(left[1], right[1]), max(left[2], right[2]), min(left[3], right[3])
    return result if result[0] <= result[1] and result[2] <= result[3] else None


def classify_overlap(source: Any, second: str, candidate: str, box: tuple[Q, Q, Q, Q]) -> str:
    t0, t1, p0, p1 = box
    if t0 < t1 and p0 < p1:
        try:
            if root_slab(source, second, candidate, box) is not None:
                return "JOIN_AREA_UNIQUE_ROOT_SLAB"
        except Exception:
            pass
        try:
            _value, gradient = centered_taylor(source, second, candidate, box)
            dt_sign, dp_sign = strict_sign(gradient[0]), strict_sign(gradient[1])
            if dt_sign and dp_sign:
                minimum_t, maximum_t = (t0, t1) if dt_sign > 0 else (t1, t0)
                minimum_p, maximum_p = (p0, p1) if dp_sign > 0 else (p1, p0)
                minimum = third_tangency_jet(source, second, candidate, minimum_t, minimum_t, minimum_p, minimum_p).value
                maximum = third_tangency_jet(source, second, candidate, maximum_t, maximum_t, maximum_p, maximum_p).value
                if strict_sign(minimum) == -1 and strict_sign(maximum) == 1:
                    return "JOIN_AREA_STRICT_MONOTONE_CORNER_ROOT"
        except Exception:
            pass
    elif t0 < t1:
        full = third_tangency_jet(source, second, candidate, t0, t1, p0, p0)
        left = third_tangency_jet(source, second, candidate, t0, t0, p0, p0).value
        right = third_tangency_jet(source, second, candidate, t1, t1, p0, p0).value
        if strict_sign(full.gradient[0]) and strict_sign(left) * strict_sign(right) == -1:
            return "JOIN_HORIZONTAL_INTERFACE_UNIQUE_ROOT"
    elif p0 < p1:
        full = third_tangency_jet(source, second, candidate, t0, t0, p0, p1)
        lower = third_tangency_jet(source, second, candidate, t0, t0, p0, p0).value
        upper = third_tangency_jet(source, second, candidate, t0, t0, p1, p1).value
        if strict_sign(full.gradient[1]) and strict_sign(lower) * strict_sign(upper) == -1:
            return "JOIN_VERTICAL_INTERFACE_UNIQUE_ROOT"
    try:
        if strict_sign(third_tangency_jet(source, second, candidate, t0, t1, p0, p1).value):
            return "SEPARATE_STRICT_NO_ROOT_ON_OVERLAP"
        if strict_sign(centered_taylor(source, second, candidate, box)[0]):
            return "SEPARATE_CENTERED_STRICT_NO_ROOT_ON_OVERLAP"
    except Exception:
        pass
    return "UNRESOLVED_OVERLAP"


def build() -> dict[str, Any]:
    cores = core_cert.physical_cores()
    document = json.loads(ATLAS.read_text())["result"]
    rows = document["physical_patch_rows"]
    row_by_id = {row["physical_patch_id"]: row for row in rows}
    grouped: dict[tuple[int, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(row["source_core_index"], row["second_selected_target_id"], row["third_candidate_id"])].append(row)
    pair_rows = []
    for key, branch_rows in grouped.items():
        source = cores[key[0]]
        for left_index, left in enumerate(branch_rows):
            left_bbox = tuple(map(Q, left["bbox"]))
            left_boxes = [tuple(map(Q, box)) for box in left["boxes"]]
            for right in branch_rows[left_index + 1:]:
                if left["member_component_id"] == right["member_component_id"]:
                    continue
                if not overlaps(left_bbox, tuple(map(Q, right["bbox"]))):
                    continue
                right_boxes = [tuple(map(Q, box)) for box in right["boxes"]]
                intersections = [
                    overlap for left_box in left_boxes for right_box in right_boxes
                    if (overlap := intersection(left_box, right_box)) is not None
                ]
                if not intersections:
                    continue
                classifications = [classify_overlap(source, key[1], key[2], box) for box in intersections]
                join_classes = sorted({value for value in classifications if value.startswith("JOIN_")})
                unresolved = sum(value == "UNRESOLVED_OVERLAP" for value in classifications)
                separation_classes = sorted({value for value in classifications if value.startswith("SEPARATE_")})
                if join_classes:
                    status = "CERTIFIED_JOIN"
                elif unresolved == 0 and separation_classes:
                    status = "CERTIFIED_NO_JOIN_ON_SHARED_BOX_CLOSURE"
                else:
                    status = "UNRESOLVED"
                pair_rows.append({
                    "left_patch_id": left["physical_patch_id"],
                    "right_patch_id": right["physical_patch_id"],
                    "source_core_index": key[0],
                    "second_selected_target_id": key[1],
                    "third_candidate_id": key[2],
                    "overlap_box_count": len(intersections),
                    "join_certification_modes": join_classes,
                    "separation_certification_modes": separation_classes,
                    "unresolved_overlap_box_count": unresolved,
                    "status": status,
                })
    pair_rows.sort(key=lambda row: (row["left_patch_id"], row["right_patch_id"]))
    parent = {identifier: identifier for identifier in row_by_id}

    def find(identifier: str) -> str:
        while parent[identifier] != identifier:
            parent[identifier] = parent[parent[identifier]]
            identifier = parent[identifier]
        return identifier

    def union(left: str, right: str) -> None:
        left_root, right_root = find(left), find(right)
        if left_root != right_root:
            parent[max(left_root, right_root)] = min(left_root, right_root)

    for row in pair_rows:
        if row["status"] == "CERTIFIED_JOIN":
            union(row["left_patch_id"], row["right_patch_id"])
    members: dict[str, list[str]] = defaultdict(list)
    for identifier in sorted(parent):
        members[find(identifier)].append(identifier)
    component_rows = []
    for patch_ids in members.values():
        first = row_by_id[patch_ids[0]]
        identity = {"physical_patch_ids": patch_ids}
        component_rows.append({
            "physical_root_component_id": "physical-s0-rank3-root-component:" + digest(identity),
            "source_core_index": first["source_core_index"],
            "second_selected_target_id": first["second_selected_target_id"],
            "third_candidate_id": first["third_candidate_id"],
            "physical_patch_count": len(patch_ids),
            "physical_patch_ids": patch_ids,
            "physical_patch_ids_sha256": digest(patch_ids),
        })
    component_rows.sort(key=lambda row: row["physical_root_component_id"])
    status_histogram = Counter(row["status"] for row in pair_rows)
    mode_histogram = Counter(mode for row in pair_rows for mode in row["join_certification_modes"])
    result = {
        "input_physical_patch_count": len(rows),
        "cross_tube_shared_closure_pair_count": len(pair_rows),
        "pair_status_histogram": dict(sorted(status_histogram.items())),
        "join_certification_mode_histogram": dict(sorted(mode_histogram.items())),
        "certified_join_pair_count": status_histogram["CERTIFIED_JOIN"],
        "certified_no_join_pair_count": status_histogram["CERTIFIED_NO_JOIN_ON_SHARED_BOX_CLOSURE"],
        "unresolved_pair_count": status_histogram["UNRESOLVED"],
        "joined_physical_root_component_count": len(component_rows),
        "multi_patch_joined_component_count": sum(row["physical_patch_count"] > 1 for row in component_rows),
        "maximum_patch_count_per_joined_component": max(row["physical_patch_count"] for row in component_rows),
        "pair_rows": pair_rows,
        "pair_rows_sha256": digest(pair_rows),
        "component_rows": component_rows,
        "component_rows_sha256": digest(component_rows),
        "strict_scope": "joins are asserted only where the same physical discriminant has a certified unique root on a shared certified box closure; uncovered gaps and distinct discriminants are not joined",
    }
    if len(pair_rows) != 128 or status_histogram["UNRESOLVED"]:
        raise RuntimeError("cross-tube overlap ledger")
    return {"schema": "cm2.round82.rank3-cross-tube-joins.v1", "result": result, "result_sha256": digest(result)}


def main() -> int:
    json.dump(build(), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
