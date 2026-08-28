#!/usr/bin/env python3
"""Interval-prefilter all different-candidate rank-three root-box overlaps."""
from __future__ import annotations

import json
import multiprocessing as mp
import sys
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
from cm2_round79_tangency_intersection_generator import digest
from cm2_round80_time3_adaptive_carrier_resolver import centered_taylor, strict_sign, third_tangency_jet


HERE = Path(__file__).resolve().parent
ATLAS = HERE / "cm2-round82-rank3-physical-patch-atlas-2026-07-21.json"
JOINS = HERE / "cm2-round82-rank3-cross-tube-joins-2026-07-21.json"
WORK_CORES: tuple[Any, ...] = ()


def init_worker(cores: tuple[Any, ...]) -> None:
    global WORK_CORES
    WORK_CORES = cores
    ctx.prec = 384


def intersection(left: tuple[Q, Q, Q, Q], right: tuple[Q, Q, Q, Q]) -> tuple[Q, Q, Q, Q] | None:
    result = max(left[0], right[0]), min(left[1], right[1]), max(left[2], right[2]), min(left[3], right[3])
    return result if result[0] <= result[1] and result[2] <= result[3] else None


def process_chunk(tasks: list[tuple[str, str, int, str, str, str, tuple[Q, Q, Q, Q]]]) -> list[tuple[str, str, str, list[str]]]:
    output = []
    for left_id, right_id, source_index, second, left_candidate, right_candidate, box in tasks:
        source = WORK_CORES[source_index]
        left = third_tangency_jet(source, second, left_candidate, *box).value
        if strict_sign(left):
            output.append((left_id, right_id, "LEFT_STRICT_EXCLUSION", []))
            continue
        right = third_tangency_jet(source, second, right_candidate, *box).value
        if strict_sign(right):
            output.append((left_id, right_id, "RIGHT_STRICT_EXCLUSION", []))
            continue
        try:
            left_centered = centered_taylor(source, second, left_candidate, box)[0]
            if strict_sign(left_centered):
                output.append((left_id, right_id, "LEFT_CENTERED_EXCLUSION", []))
                continue
            right_centered = centered_taylor(source, second, right_candidate, box)[0]
            if strict_sign(right_centered):
                output.append((left_id, right_id, "RIGHT_CENTERED_EXCLUSION", []))
                continue
        except Exception:
            pass
        output.append((left_id, right_id, "REQUIRES_TWO_EQUATION_KRAWCZYK", list(map(str, box))))
    return output


def build(workers: int = 24) -> dict[str, Any]:
    patches = json.loads(ATLAS.read_text())["result"]["physical_patch_rows"]
    components = json.loads(JOINS.read_text())["result"]["component_rows"]
    component_by_patch = {
        patch_id: row["physical_root_component_id"]
        for row in components for patch_id in row["physical_patch_ids"]
    }
    metadata = {
        row["physical_root_component_id"]: {
            "source_core_index": row["source_core_index"],
            "second_selected_target_id": row["second_selected_target_id"],
            "third_candidate_id": row["third_candidate_id"],
        }
        for row in components
    }
    boxes_by_core: dict[int, list[tuple[tuple[Q, Q, Q, Q], str]]] = defaultdict(list)
    for patch in patches:
        component_id = component_by_patch[patch["physical_patch_id"]]
        for raw_box in patch["boxes"]:
            boxes_by_core[patch["source_core_index"]].append((tuple(map(Q, raw_box)), component_id))
    unique_tasks = set()
    raw_overlap_count = 0
    for source_index, boxes in boxes_by_core.items():
        boxes.sort(key=lambda item: item[0][0])
        active = []
        for box, component_id in boxes:
            active = [item for item in active if item[0][1] >= box[0]]
            current = metadata[component_id]
            for other_box, other_id in active:
                if other_id == component_id or other_box[3] < box[2] or box[3] < other_box[2]:
                    continue
                other = metadata[other_id]
                if other["third_candidate_id"] == current["third_candidate_id"]:
                    continue
                if other["second_selected_target_id"] != current["second_selected_target_id"]:
                    raise RuntimeError("overlapping physical boxes disagree on second owner")
                overlap = intersection(other_box, box)
                if overlap is None:
                    continue
                raw_overlap_count += 1
                left_id, right_id = sorted((other_id, component_id))
                left, right = metadata[left_id], metadata[right_id]
                unique_tasks.add((
                    left_id, right_id, source_index, left["second_selected_target_id"],
                    left["third_candidate_id"], right["third_candidate_id"], overlap,
                ))
            active.append((box, component_id))
    tasks = sorted(unique_tasks)
    chunk_size = (len(tasks) + workers - 1) // workers
    chunks = [tasks[index:index + chunk_size] for index in range(0, len(tasks), chunk_size)]
    context = mp.get_context("fork")
    cores = core_cert.physical_cores()
    with context.Pool(workers, initializer=init_worker, initargs=(cores,)) as pool:
        chunks_output = pool.map(process_chunk, chunks)
    rows = [row for chunk in chunks_output for row in chunk]
    pair_counts: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    residual_boxes: dict[tuple[str, str], list[list[str]]] = defaultdict(list)
    status_histogram = Counter()
    for left_id, right_id, status, raw_box in rows:
        pair_counts[(left_id, right_id)][status] += 1
        status_histogram[status] += 1
        if raw_box:
            residual_boxes[(left_id, right_id)].append(raw_box)
    pair_rows = []
    for pair, counts in sorted(pair_counts.items()):
        residual = sorted(residual_boxes[pair])
        pair_rows.append({
            "left_physical_root_component_id": pair[0],
            "right_physical_root_component_id": pair[1],
            "overlap_box_count": sum(counts.values()),
            "status_histogram": dict(sorted(counts.items())),
            "residual_box_count": len(residual),
            "residual_boxes": residual,
            "residual_boxes_sha256": digest(residual),
        })
    result = {
        "different_candidate_raw_root_box_overlap_count": raw_overlap_count,
        "different_candidate_unique_overlap_box_count": len(tasks),
        "different_candidate_component_pair_count": len(pair_rows),
        "interval_prefilter_status_histogram": dict(sorted(status_histogram.items())),
        "strictly_excluded_overlap_box_count": len(tasks) - status_histogram["REQUIRES_TWO_EQUATION_KRAWCZYK"],
        "residual_two_equation_box_count": status_histogram["REQUIRES_TWO_EQUATION_KRAWCZYK"],
        "residual_component_pair_count": sum(row["residual_box_count"] > 0 for row in pair_rows),
        "pair_rows": pair_rows,
        "pair_rows_sha256": digest(pair_rows),
        "strict_scope": "one-pass interval exclusion on all certified different-candidate root-box overlaps; residual boxes require two-equation interval-Krawczyk subdivision",
    }
    return {"schema": "cm2.round82.rank3-intersection-prefilter.v1", "result": result, "result_sha256": digest(result)}


def main() -> int:
    json.dump(build(), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
