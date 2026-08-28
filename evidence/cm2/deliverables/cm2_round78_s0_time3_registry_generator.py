#!/usr/bin/env python3
"""Actual fixed-s=0 adaptive Q2-to-time3 registry."""
from __future__ import annotations

import argparse
import hashlib
import json
import multiprocessing as mp
import sys
from collections import Counter
from fractions import Fraction as Q
from typing import Any

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as step1
import cm2_gate34_round26_q1_time2_frontier_cert as time2
import cm2_gate34_round29_q2_time3_anchor_registry_cert as time3
from cm2_round74_s0_depth2_adaptive_generator import split_2d


CORES: tuple[Any, ...] = ()
PAIR_INDEX: dict[Any, Any] = {}
PATTERN_INDEX: dict[Any, Any] = {}
BASE_GRID = 32
EXTRA_DEPTH = 2


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def init_worker(cores: tuple[Any, ...], base_grid: int, extra_depth: int) -> None:
    global CORES, PAIR_INDEX, PATTERN_INDEX, BASE_GRID, EXTRA_DEPTH
    CORES = cores
    BASE_GRID = base_grid
    EXTRA_DEPTH = extra_depth
    PAIR_INDEX, PATTERN_INDEX, _ = time3.component_cert.key_index_tables()


def normalized_area(atom: Any) -> Q:
    core = atom.source_core
    return (atom.t1 - atom.t0) * (atom.p1 - atom.p0) / ((core.t1 - core.t0) * (core.p1 - core.p0))


def compact(atom: Any, result: dict[str, Any], parent_id: str) -> dict[str, Any]:
    identity = {
        "source_core_index": atom.source_core_index,
        "dyadic_path": atom.path,
        "classification": result["classification"],
    }
    return {
        "time3_cell_id": "physical-s0-time3-cell:" + digest(identity),
        "Q2_parent_id": parent_id,
        "source_core_index": atom.source_core_index,
        "dyadic_path": atom.path,
        "depth": atom.depth,
        "source_box": {
            "t": [str(atom.t0), str(atom.t1)],
            "p": [str(atom.p0), str(atom.p1)],
        },
        "classification": result["classification"],
        "destination_core_id": result.get("destination_core_id"),
        "third_selected_target_id": None if result.get("owner3") is None else result["owner3"]["selected_target_id"],
        "normalized_area": str(normalized_area(atom)),
        "third_word_key_id": None if result.get("word3") is None else result["word3"]["key"]["word_key_id"],
    }


def process_core(source_core_index: int) -> dict[str, Any]:
    core = CORES[source_core_index]
    terminal = []
    counters = Counter()
    blocker_histogram = Counter()
    for i in range(BASE_GRID):
        for j in range(BASE_GRID):
            t0 = core.t0 + (core.t1 - core.t0) * Q(i, BASE_GRID)
            t1 = core.t0 + (core.t1 - core.t0) * Q(i + 1, BASE_GRID)
            p0 = core.p0 + (core.p1 - core.p0) * Q(j, BASE_GRID)
            p1 = core.p0 + (core.p1 - core.p0) * Q(j + 1, BASE_GRID)
            path = f"g{BASE_GRID}:{i}:{j}"
            atom = step1.Atom(source_core_index, core, t0, t1, p0, p1, Q(0), Q(0), path)
            first = step1.classify_atom(atom, CORES)
            counters["time1_tests"] += 1
            if first["classification"] != "SURVIVE_THROUGH_1_INNER":
                continue
            second = time2.classify_time2(atom, CORES)
            counters["time2_tests"] += 1
            if second["classification"] != "SURVIVE_THROUGH_2_INNER":
                continue
            parent_id = "physical-s0-Q2-parent:" + digest({
                "source_core_index": source_core_index,
                "base_i": i,
                "base_j": j,
            })
            stack = [(atom, 0)]
            while stack:
                child, extra = stack.pop()
                result = time3.classify_time3(child, CORES, PAIR_INDEX, PATTERN_INDEX)
                counters["time3_tests"] += 1
                if result["classification"] == "UNRESOLVED_TIME3_OUTER" and extra < EXTRA_DEPTH:
                    left, right = split_2d(child)
                    stack.extend(((right, extra + 1), (left, extra + 1)))
                    continue
                if result["classification"] == "UNRESOLVED_TIME3_OUTER":
                    blocker_histogram[str(result["blocker"])] += 1
                terminal.append(compact(child, result, parent_id))
    terminal.sort(key=lambda row: row["time3_cell_id"])
    return {
        "source_core_index": source_core_index,
        "source_core_id": step1.core_id(core),
        "test_counts": dict(sorted(counters.items())),
        "blocker_histogram": dict(sorted(blocker_histogram.items())),
        "terminal_rows": terminal,
    }


def build(workers: int, base_grid: int, extra_depth: int) -> dict[str, Any]:
    cores = core_cert.physical_cores()
    context = mp.get_context("fork")
    with context.Pool(
        workers, initializer=init_worker,
        initargs=(cores, base_grid, extra_depth),
    ) as pool:
        core_rows = pool.map(process_core, range(len(cores)))
    histogram = Counter()
    areas = Counter()
    rows = []
    blocker_histogram = Counter()
    for core in core_rows:
        blocker_histogram.update(core["blocker_histogram"])
        for row in core.pop("terminal_rows"):
            histogram[row["classification"]] += 1
            areas[row["classification"]] += Q(row["normalized_area"])
            rows.append(row)
    rows.sort(key=lambda row: row["time3_cell_id"])
    strict_rows = [row for row in rows if row["classification"] != "UNRESOLVED_TIME3_OUTER"]
    return {
        "schema": "cm2.round78.s0-time3-registry.v1",
        "result": {
            "fixed_parameter": "s=0",
            "base_grid": [base_grid, base_grid],
            "maximum_extra_binary_depth": extra_depth,
            "source_core_count": len(cores),
            "terminal_classification_histogram": dict(sorted(histogram.items())),
            "normalized_area_ledger": {key: str(value) for key, value in sorted(areas.items())},
            "blocker_histogram": dict(sorted(blocker_histogram.items())),
            "strict_Q3_cell_count": histogram["SURVIVE_THROUGH_3_INNER"],
            "strict_R3_cell_count": histogram["RETURN_AT_3_INNER"],
            "cross_rank_Q2_to_time3_incidence_count": len(rows),
            "strict_rows": strict_rows,
            "strict_rows_sha256": digest(strict_rows),
            "all_terminal_rows_sha256": digest(rows),
            "core_rows": core_rows,
            "strict_scope": "actual fixed-s0 finite rank-three registry; unresolved remainder and zero finite R3 count are not promoted to limiting emptiness",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=16)
    parser.add_argument("--base-grid", type=int, default=32)
    parser.add_argument("--extra-depth", type=int, default=2)
    args = parser.parse_args()
    json.dump(build(args.workers, args.base_grid, args.extra_depth), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
