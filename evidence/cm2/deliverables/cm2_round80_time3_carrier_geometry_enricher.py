#!/usr/bin/env python3
"""Attach the actual second owner and outgoing chart to time-three carrier seeds."""
from __future__ import annotations

import json
import multiprocessing as mp
import sys
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as step1
import cm2_gate34_round29_q2_time3_anchor_registry_cert as time3
from cm2_round79_tangency_intersection_generator import digest


HERE = Path(__file__).resolve().parent
SEEDS = HERE / "cm2-round79-time3-carrier-seeds-2026-07-21.json"
CORES: tuple[Any, ...] = ()
PAIR_INDEX: dict[Any, Any] = {}
PATTERN_INDEX: dict[Any, Any] = {}


def init_worker(cores: tuple[Any, ...]) -> None:
    global CORES, PAIR_INDEX, PATTERN_INDEX
    CORES = cores
    PAIR_INDEX, PATTERN_INDEX, _ = time3.component_cert.key_index_tables()


def enrich_core(payload: tuple[int, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_index, rows = payload
    core = CORES[source_index]
    geometry_by_path = {}
    output = []
    for row in rows:
        path = row["dyadic_path"]
        if path not in geometry_by_path:
            box = row["source_box"]
            atom = step1.Atom(
                source_index, core,
                Q(box["t"][0]), Q(box["t"][1]),
                Q(box["p"][0]), Q(box["p"][1]),
                Q(0), Q(0), path,
            )
            result = time3.classify_time3(atom, CORES, PAIR_INDEX, PATTERN_INDEX)
            if result["classification"] != "UNRESOLVED_TIME3_OUTER":
                raise RuntimeError(f"seed became strict {source_index}:{path}")
            owner2 = result.get("owner2")
            state2 = result.get("state2")
            geometry_by_path[path] = {
                "second_selected_target_id": None if owner2 is None else owner2["selected_target_id"],
                "second_outgoing_chart": None if state2 is None else state2["chart"],
            }
        output.append({**row, **geometry_by_path[path]})
    return output


def build(workers: int = 16) -> dict[str, Any]:
    document = json.loads(SEEDS.read_text())["result"]
    grouped: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in document["seed_rows"]:
        grouped[row["source_core_index"]].append(row)
    cores = core_cert.physical_cores()
    context = mp.get_context("fork")
    with context.Pool(workers, initializer=init_worker, initargs=(cores,)) as pool:
        chunks = pool.map(enrich_core, sorted(grouped.items()))
    rows = [row for chunk in chunks for row in chunk]
    rows.sort(key=lambda row: (row["source_core_index"], row["carrier"], row["dyadic_path"]))
    branch_histogram = Counter(
        (row["second_selected_target_id"], row["second_outgoing_chart"])
        for row in rows if row["carrier"].startswith("THIRD_CANDIDATE:")
    )
    branch_rows = [
        {
            "second_selected_target_id": key[0],
            "second_outgoing_chart": key[1],
            "seed_incidence_count": count,
        }
        for key, count in sorted(branch_histogram.items())
    ]
    result = {
        "seed_incidence_count": len(rows),
        "physical_seed_incidence_count": sum(row["carrier"].startswith("THIRD_CANDIDATE:") for row in rows),
        "second_owner_outgoing_branch_count": len(branch_rows),
        "branch_rows": branch_rows,
        "branch_rows_sha256": digest(branch_rows),
        "seed_rows": rows,
        "seed_rows_sha256": digest(rows),
    }
    return {"schema": "cm2.round80.time3-carrier-geometry.v1", "result": result, "result_sha256": digest(result)}


def main() -> int:
    json.dump(build(), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
