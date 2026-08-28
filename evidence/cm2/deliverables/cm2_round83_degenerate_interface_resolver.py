#!/usr/bin/env python3
"""One-dimensional common-tangent exclusion on degenerate residual interfaces."""
from __future__ import annotations

import json
import multiprocessing as mp
import sys
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
from cm2_round79_tangency_intersection_generator import aq, digest, interval, strict_sign
from cm2_round83_common_tangent_line_krawczyk import common_tangent_targets, outgoing_line


HERE = Path(__file__).resolve().parent
PREFILTER = HERE / "cm2-round82-rank3-intersection-prefilter-2026-07-21.json"
JOINS = HERE / "cm2-round82-rank3-cross-tube-joins-2026-07-21.json"
MAXIMUM_DEPTH = 30
WORK_CORES: tuple[Any, ...] = ()
WORK_METADATA: dict[str, dict[str, Any]] = {}


def init_worker(cores: tuple[Any, ...], metadata: dict[str, dict[str, Any]]) -> None:
    global WORK_CORES, WORK_METADATA
    WORK_CORES, WORK_METADATA = cores, metadata
    ctx.prec = 384


def split_interval(box: tuple[Q, Q, Q, Q]) -> tuple[tuple[Q, Q, Q, Q], tuple[Q, Q, Q, Q]]:
    t0, t1, p0, p1 = box
    if t0 < t1:
        middle = (t0 + t1) / 2
        return (t0, middle, p0, p1), (middle, t1, p0, p1)
    if p0 < p1:
        middle = (p0 + p1) / 2
        return (t0, t1, p0, middle), (t0, t1, middle, p1)
    return box, box


def target_excluded(line: Any, target: dict[str, Any]) -> bool:
    return strict_sign(line[0].value - target["nx"]) != 0 or strict_sign(line[1].value - target["ny"]) != 0 or strict_sign(line[2].value - target["h"]) != 0


def resolve(source: Any, second: str, targets: list[dict[str, Any]], initial: tuple[Q, Q, Q, Q]) -> dict[str, Any]:
    stack = [(initial, 0, tuple(range(len(targets))))]
    tests = 0
    maximum_depth = 0
    unresolved = []
    while stack:
        box, depth, active = stack.pop()
        maximum_depth = max(maximum_depth, depth)
        line = outgoing_line(source, second, interval(box[0], box[1]), interval(box[2], box[3]))
        tests += 1
        survivors = tuple(index for index in active if not target_excluded(line, targets[index]))
        if not survivors:
            continue
        if box[0] == box[1] and box[2] == box[3]:
            unresolved.append(list(map(str, box)))
            continue
        if depth == MAXIMUM_DEPTH:
            unresolved.append(list(map(str, box)))
            continue
        first, second_box = split_interval(box)
        stack.extend(((second_box, depth + 1, survivors), (first, depth + 1, survivors)))
    return {
        "interval_line_test_count": tests,
        "maximum_depth": maximum_depth,
        "unresolved_leaf_count": len(unresolved),
        "unresolved_sha256": digest(sorted(unresolved)),
    }


def process_pair(row: dict[str, Any]) -> dict[str, Any]:
    left_id, right_id = row["left_physical_root_component_id"], row["right_physical_root_component_id"]
    left, right = WORK_METADATA[left_id], WORK_METADATA[right_id]
    source = WORK_CORES[left["source_core_index"]]
    targets = common_tangent_targets(left["third_candidate_id"], right["third_candidate_id"])
    boxes = [tuple(map(Q, box)) for box in row["residual_boxes"] if Q(box[0]) == Q(box[1]) or Q(box[2]) == Q(box[3])]
    tests = unresolved = 0
    maximum_depth = 0
    for box in boxes:
        result = resolve(source, left["second_selected_target_id"], targets, box)
        tests += result["interval_line_test_count"]
        unresolved += result["unresolved_leaf_count"]
        maximum_depth = max(maximum_depth, result["maximum_depth"])
    return {
        "left_physical_root_component_id": left_id,
        "right_physical_root_component_id": right_id,
        "input_degenerate_box_count": len(boxes),
        "interval_line_test_count": tests,
        "unresolved_leaf_count": unresolved,
        "maximum_depth": maximum_depth,
    }


def build(workers: int = 24) -> dict[str, Any]:
    rows = [row for row in json.loads(PREFILTER.read_text())["result"]["pair_rows"] if row["residual_box_count"]]
    components = json.loads(JOINS.read_text())["result"]["component_rows"]
    metadata = {row["physical_root_component_id"]: row for row in components}
    context = mp.get_context("fork")
    with context.Pool(workers, initializer=init_worker, initargs=(core_cert.physical_cores(), metadata)) as pool:
        pair_rows = pool.map(process_pair, rows)
    pair_rows = [row for row in pair_rows if row["input_degenerate_box_count"]]
    pair_rows.sort(key=lambda row: (row["left_physical_root_component_id"], row["right_physical_root_component_id"]))
    result = {
        "input_degenerate_component_pair_count": len(pair_rows),
        "input_degenerate_box_count": sum(row["input_degenerate_box_count"] for row in pair_rows),
        "interval_line_test_count": sum(row["interval_line_test_count"] for row in pair_rows),
        "certified_disjoint_degenerate_box_count": sum(row["input_degenerate_box_count"] for row in pair_rows if row["unresolved_leaf_count"] == 0),
        "unresolved_component_pair_count": sum(row["unresolved_leaf_count"] > 0 for row in pair_rows),
        "unresolved_leaf_count": sum(row["unresolved_leaf_count"] for row in pair_rows),
        "maximum_depth": max(row["maximum_depth"] for row in pair_rows),
        "pair_rows": pair_rows,
        "pair_rows_sha256": digest(pair_rows),
        "strict_scope": "one-dimensional outgoing-line common-tangent exclusion on all degenerate residual interface boxes",
    }
    return {"schema": "cm2.round83.degenerate-interface-resolution.v1", "result": result, "result_sha256": digest(result)}


def main() -> int:
    json.dump(build(), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
