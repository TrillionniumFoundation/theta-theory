#!/usr/bin/env python3
"""Generate the actual fixed-s=0 depth-two registry from strict Q1 parents."""
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

import cm2_gate34_round26_q1_time2_frontier_cert as time2


SCHEMA = "cm2.round74.s0-depth2-registry.v1"
CORES: tuple[Any, ...] = ()


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def init_worker(cores: tuple[Any, ...]) -> None:
    global CORES
    CORES = cores


def process_parent(row: dict[str, Any]) -> list[dict[str, Any]]:
    return time2.adaptive_time2_rows([row], CORES)


def strict_s0(row: dict[str, Any]) -> bool:
    lower, upper = map(Q, row["source_box"]["s"])
    return lower < 0 < upper


def build(workers: int) -> dict[str, Any]:
    manifest = time2.load_step1_manifest()
    cores = time2.core_cert.physical_cores()
    all_q1 = [
        row for row in manifest["result"]["adaptive_full_core_step1_raw_leaf_rows"]
        if row["classification"] == "SURVIVE_THROUGH_1_INNER"
    ]
    touching = [
        row for row in all_q1
        if Q(row["source_box"]["s"][0]) <= 0 <= Q(row["source_box"]["s"][1])
    ]
    parents = [row for row in touching if strict_s0(row)]
    endpoint_only = [row for row in touching if not strict_s0(row)]
    if len(parents) != 32 or len(endpoint_only) != 772:
        raise RuntimeError("frozen s=0 parent split changed")
    context = mp.get_context("fork")
    with context.Pool(processes=workers, initializer=init_worker, initargs=(cores,)) as pool:
        blocks = pool.map(process_parent, parents)
    rows = sorted((row for block in blocks for row in block), key=lambda row: (row["Q1_parent_atom_id"], row["refinement_suffix"]))
    q2 = [row for row in rows if row["classification"] == "SURVIVE_THROUGH_2_INNER" and strict_s0(row)]
    unresolved = [row for row in rows if row["classification"] == "UNRESOLVED_TIME2_OUTER" and strict_s0(row)]
    result = {
        "fixed_parameter": "s=0",
        "all_frozen_Q1_parents": len(all_q1),
        "Q1_boxes_touching_s0_closed": len(touching),
        "Q1_boxes_with_s0_strictly_in_open_s_interval": len(parents),
        "Q1_boxes_touching_s0_only_at_adaptive_endpoint_rejected": len(endpoint_only),
        "terminal_time2_leaf_count_from_32_legal_parents": len(rows),
        "terminal_classification_histogram": dict(sorted(Counter(row["classification"] for row in rows).items())),
        "strict_s0_Q2_inner_cell_count": len(q2),
        "strict_s0_unresolved_outer_cell_count": len(unresolved),
        "strict_s0_Q2_source_core_histogram": {str(k): v for k, v in sorted(Counter(row["source_core_index"] for row in q2).items())},
        "strict_s0_Q2_rows": q2,
        "strict_s0_Q2_rows_sha256": digest(q2),
        "strict_s0_unresolved_rows_sha256": digest(unresolved),
        "all_terminal_rows_sha256": digest(rows),
        "scope": "whole-box strict fixed-s0 slices only; adaptive s-endpoint boxes excluded",
    }
    return {"schema": SCHEMA, "construction": {"workers": workers, "arithmetic": "384-bit Arb inherited exact replay"}, "result": result}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=16)
    args = parser.parse_args()
    json.dump(build(args.workers), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
