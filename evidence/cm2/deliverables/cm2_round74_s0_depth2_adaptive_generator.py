#!/usr/bin/env python3
"""Fixed-s=0 two-dimensional Arb registry through collision time two."""
from __future__ import annotations

import argparse
import hashlib
import json
import multiprocessing as mp
import sys
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate34_full_core_return_adaptive_frontier_cert as step1
import cm2_gate34_round26_q1_time2_frontier_cert as time2


SCHEMA = "cm2.round74.s0-depth2-adaptive.v1"
CORES: tuple[Any, ...] = ()
MAX_DEPTH = 12


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def init_worker(cores: tuple[Any, ...], maximum_depth: int) -> None:
    global CORES, MAX_DEPTH
    CORES, MAX_DEPTH = cores, maximum_depth


def split_2d(atom: Any) -> tuple[Any, Any]:
    core = atom.source_core
    t_scale = (atom.t1 - atom.t0) / (core.t1 - core.t0)
    p_scale = (atom.p1 - atom.p0) / (core.p1 - core.p0)
    if t_scale >= p_scale:
        middle = (atom.t0 + atom.t1) / 2
        return (
            step1.Atom(atom.source_core_index, core, atom.t0, middle, atom.p0, atom.p1, Q(0), Q(0), atom.path + "0"),
            step1.Atom(atom.source_core_index, core, middle, atom.t1, atom.p0, atom.p1, Q(0), Q(0), atom.path + "1"),
        )
    middle = (atom.p0 + atom.p1) / 2
    return (
        step1.Atom(atom.source_core_index, core, atom.t0, atom.t1, atom.p0, middle, Q(0), Q(0), atom.path + "0"),
        step1.Atom(atom.source_core_index, core, atom.t0, atom.t1, middle, atom.p1, Q(0), Q(0), atom.path + "1"),
    )


def compact(atom: Any, classification: str, destination: str | None, owner_status: str) -> dict[str, Any]:
    return {
        "source_core_index": atom.source_core_index,
        "dyadic_path": atom.path,
        "depth": atom.depth,
        "t": [str(atom.t0), str(atom.t1)],
        "p": [str(atom.p0), str(atom.p1)],
        "classification": classification,
        "destination_core_id": destination,
        "owner_status": owner_status,
        "normalized_coordinate_area": str(
            (atom.t1 - atom.t0) * (atom.p1 - atom.p0)
            / ((atom.source_core.t1 - atom.source_core.t0) * (atom.source_core.p1 - atom.source_core.p0))
        ),
    }


def process_core(source_core_index: int) -> dict[str, Any]:
    core = CORES[source_core_index]
    root = step1.Atom(source_core_index, core, core.t0, core.t1, core.p0, core.p1, Q(0), Q(0), "")
    stack = [root]
    rows: list[dict[str, Any]] = []
    tests = Counter()
    while stack:
        atom = stack.pop()
        first = step1.classify_atom(atom, CORES)
        tests["step1"] += 1
        if first["classification"] == "RETURN_AT_1_INNER":
            rows.append(compact(atom, "R1_INNER", first["destination_core_id"], "strict_time1_return"))
            continue
        if first["classification"] == "SURVIVE_THROUGH_1_INNER":
            second = time2.classify_time2(atom, CORES)
            tests["step2"] += 1
            if second["classification"] == "RETURN_AT_2_INNER":
                rows.append(compact(atom, "R2_INNER", second["destination_core_id"], second["owner_status"]))
                continue
            if second["classification"] == "SURVIVE_THROUGH_2_INNER":
                rows.append(compact(atom, "Q2_INNER", None, second["owner_status"]))
                continue
        if atom.depth < MAX_DEPTH:
            left, right = split_2d(atom)
            stack.extend((right, left))
        else:
            rows.append(compact(atom, "DEPTH2_OUTER", None, "unresolved_at_frozen_depth"))
    rows.sort(key=lambda row: row["dyadic_path"])
    areas = Counter()
    counts = Counter()
    destinations = Counter()
    for row in rows:
        counts[row["classification"]] += 1
        areas[row["classification"]] += Q(row["normalized_coordinate_area"])
        if row["classification"] == "R2_INNER":
            destinations[row["destination_core_id"]] += 1
    if sum(areas.values(), Q(0)) != 1:
        raise RuntimeError("core normalized area not conserved")
    return {
        "source_core_index": source_core_index,
        "source_core_id": time2.step1.core_id(core),
        "terminal_leaf_count": len(rows),
        "classification_histogram": dict(sorted(counts.items())),
        "normalized_area_ledger": {key: str(value) for key, value in sorted(areas.items())},
        "R2_destination_leaf_histogram": dict(sorted(destinations.items())),
        "test_counts": dict(sorted(tests.items())),
        "maximum_terminal_depth": max(row["depth"] for row in rows),
        "rows_sha256": digest(rows),
        "R2_rows": [row for row in rows if row["classification"] == "R2_INNER"],
    }


def build(workers: int, maximum_depth: int) -> dict[str, Any]:
    cores = time2.core_cert.physical_cores()
    context = mp.get_context("fork")
    with context.Pool(workers, initializer=init_worker, initargs=(cores, maximum_depth)) as pool:
        core_rows = pool.map(process_core, range(len(cores)))
    global_counts = Counter()
    global_areas = Counter()
    all_r2 = []
    for core in core_rows:
        for key, value in core["classification_histogram"].items():
            global_counts[key] += value
        for key, value in core["normalized_area_ledger"].items():
            global_areas[key] += Q(value)
        all_r2.extend(core.pop("R2_rows"))
    all_r2.sort(key=canonical)
    terminal_count = sum(global_counts.values())
    result = {
        "fixed_parameter": "s=0",
        "source_core_count": len(cores),
        "maximum_binary_depth": maximum_depth,
        "terminal_leaf_count": terminal_count,
        "binary_split_count": terminal_count - len(cores),
        "artificial_internal_face_cancellation_pairs": terminal_count - len(cores),
        "classification_histogram": dict(sorted(global_counts.items())),
        "normalized_24_core_area_ledger": {key: str(value) for key, value in sorted(global_areas.items())},
        "normalized_area_conservation": str(sum(global_areas.values(), Q(0))),
        "R2_strict_leaf_count": len(all_r2),
        "R2_source_core_count": len({row["source_core_index"] for row in all_r2}),
        "R2_source_destination_pair_count": len({(row["source_core_index"], row["destination_core_id"]) for row in all_r2}),
        "R2_rows": all_r2,
        "R2_rows_sha256": digest(all_r2),
        "core_rows": core_rows,
        "core_rows_sha256": digest(core_rows),
        "cross_rank_parent_map": {
            "R1_INNER_to_Round73_return_parent": global_counts["R1_INNER"],
            "Q2_or_R2_INNER_to_Round73_survival_parent": global_counts["Q2_INNER"] + global_counts["R2_INNER"],
            "DEPTH2_OUTER_parent_not_promoted": global_counts["DEPTH2_OUTER"],
            "rule": "strict R1 leaves map to the return two-cell; strict Q2/R2 leaves map to the survival two-cell on the same source core",
        },
        "oriented_artificial_trace_cancellation": "every binary split face occurs once with each orientation in the sum of child boundaries",
        "strict_scope": "finite depth-2 inner/outer registry; physical R2 boundary components inside DEPTH2_OUTER are not yet resolved",
    }
    return {"schema": SCHEMA, "construction": {"arithmetic": "384-bit Arb", "workers": workers}, "result": result}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=16)
    parser.add_argument("--maximum-depth", type=int, default=12)
    args = parser.parse_args()
    json.dump(build(args.workers, args.maximum_depth), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
