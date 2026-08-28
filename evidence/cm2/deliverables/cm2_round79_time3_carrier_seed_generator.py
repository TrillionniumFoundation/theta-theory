#!/usr/bin/env python3
"""Extract actual third-collision boundary-carrier seeds at fixed s=0."""
from __future__ import annotations

import argparse
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
from cm2_round79_tangency_intersection_generator import digest


CORES: tuple[Any, ...] = ()
PAIR_INDEX: dict[Any, Any] = {}
PATTERN_INDEX: dict[Any, Any] = {}
BASE_GRID = 32
EXTRA_DEPTH = 2


def init_worker(cores: tuple[Any, ...], base_grid: int, extra_depth: int) -> None:
    global CORES, PAIR_INDEX, PATTERN_INDEX, BASE_GRID, EXTRA_DEPTH
    CORES = cores
    BASE_GRID = base_grid
    EXTRA_DEPTH = extra_depth
    PAIR_INDEX, PATTERN_INDEX, _ = time3.component_cert.key_index_tables()


def carrier_ids(result: dict[str, Any]) -> list[str]:
    if result["blocker"] == "unresolved_time2_outgoing_chart_or_geometry":
        return ["SECOND_OUTGOING_CHART_OR_GEOMETRY"]
    if result["blocker"].startswith("third_clean_wall_word:"):
        return [result["blocker"]]
    if result["blocker"] != "unresolved_competitor:unresolved_discriminant":
        return [result["blocker"]]
    state = result["state2"]
    current_target = result["owner2"]["selected_target_id"]
    rows = []
    for candidate_id in time2.translated_candidate_ids(current_target, state["chart"]):
        candidate = time2.candidate_root(
            state["contact_x"], state["contact_y"],
            state["outgoing_x"], state["outgoing_y"],
            state["s"], candidate_id,
        )
        if candidate["classification"] == "unresolved_discriminant":
            rows.append(f"THIRD_CANDIDATE:{candidate_id}:unresolved_discriminant")
    if not rows:
        raise RuntimeError("unresolved competitor without discriminant carrier")
    return sorted(rows)


def process_core(source_core_index: int) -> dict[str, Any]:
    core = CORES[source_core_index]
    rows = []
    counts = Counter()
    for i in range(BASE_GRID):
        for j in range(BASE_GRID):
            t0 = core.t0 + (core.t1 - core.t0) * Q(i, BASE_GRID)
            t1 = core.t0 + (core.t1 - core.t0) * Q(i + 1, BASE_GRID)
            p0 = core.p0 + (core.p1 - core.p0) * Q(j, BASE_GRID)
            p1 = core.p0 + (core.p1 - core.p0) * Q(j + 1, BASE_GRID)
            atom = step1.Atom(source_core_index, core, t0, t1, p0, p1, Q(0), Q(0), f"g{BASE_GRID}:{i}:{j}")
            if step1.classify_atom(atom, CORES)["classification"] != "SURVIVE_THROUGH_1_INNER":
                continue
            if time2.classify_time2(atom, CORES)["classification"] != "SURVIVE_THROUGH_2_INNER":
                continue
            stack = [(atom, 0)]
            while stack:
                child, extra = stack.pop()
                result = time3.classify_time3(child, CORES, PAIR_INDEX, PATTERN_INDEX)
                if result["classification"] == "UNRESOLVED_TIME3_OUTER" and extra < EXTRA_DEPTH:
                    left, right = split_2d(child)
                    stack.extend(((right, extra + 1), (left, extra + 1)))
                    continue
                if result["classification"] != "UNRESOLVED_TIME3_OUTER":
                    continue
                for carrier in carrier_ids(result):
                    counts[carrier] += 1
                    rows.append({
                        "source_core_index": source_core_index,
                        "dyadic_path": child.path,
                        "source_box": {
                            "t": [str(child.t0), str(child.t1)],
                            "p": [str(child.p0), str(child.p1)],
                        },
                        "blocker": result["blocker"],
                        "carrier": carrier,
                    })
    rows.sort(key=lambda row: (row["carrier"], row["dyadic_path"]))
    return {
        "source_core_index": source_core_index,
        "carrier_histogram": dict(sorted(counts.items())),
        "seed_rows": rows,
    }


def build(workers: int, base_grid: int, extra_depth: int) -> dict[str, Any]:
    cores = core_cert.physical_cores()
    context = mp.get_context("fork")
    with context.Pool(workers, initializer=init_worker, initargs=(cores, base_grid, extra_depth)) as pool:
        core_rows = pool.map(process_core, range(len(cores)))
    rows = [row for core in core_rows for row in core.pop("seed_rows")]
    rows.sort(key=lambda row: (row["source_core_index"], row["carrier"], row["dyadic_path"]))
    family_index: dict[tuple[int, str], int] = Counter(
        (row["source_core_index"], row["carrier"]) for row in rows
    )
    family_rows = [
        {"source_core_index": key[0], "carrier": key[1], "seed_count": count}
        for key, count in sorted(family_index.items())
    ]
    third_tangency = [row for row in family_rows if row["carrier"].startswith("THIRD_CANDIDATE:")]
    result = {
        "fixed_parameter": "s=0",
        "base_grid": [base_grid, base_grid],
        "maximum_extra_binary_depth": extra_depth,
        "unresolved_seed_incidence_count": len(rows),
        "source_carrier_family_count": len(family_rows),
        "third_collision_tangency_source_carrier_family_count": len(third_tangency),
        "third_collision_tangency_seed_incidence_count": sum(row["seed_count"] for row in third_tangency),
        "family_rows": family_rows,
        "family_rows_sha256": digest(family_rows),
        "seed_rows": rows,
        "seed_rows_sha256": digest(rows),
        "strict_scope": "actual finite fixed-s0 unresolved time-three boxes mapped to physical third-collision discriminants or explicitly typed non-face blockers",
    }
    return {"schema": "cm2.round79.time3-carrier-seeds.v1", "result": result, "result_sha256": digest(result)}


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
