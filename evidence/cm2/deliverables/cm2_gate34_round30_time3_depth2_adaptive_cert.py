#!/usr/bin/env python3
"""Round-30 depth-two adaptive time-three certificate on every Q2 anchor."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from collections import Counter
from fractions import Fraction as Q
from multiprocessing import get_context
from pathlib import Path
from typing import Any

import cm2_gate34_round29_q2_time3_anchor_registry_cert as r29


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate34.round30-time3-depth2-adaptive.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = HERE / "cm2-gate34-round30-time3-depth2-adaptive-manifest-2026-07-19.json"
MAX_EXTRA_DEPTH = 2
CHUNK_SIZE = 1000
DEPENDENCIES = {
    "cm2_gate34_round29_q2_time3_anchor_registry_cert.py":
        "399ea86401e97d2679fb3f3f7a0a9328266d8d583e73fd5c5ed2bc811c14475b",
    "cm2-gate34-round29-q2-time3-anchor-registry-manifest-2026-07-18.json":
        "0a22b9081bd82a8d67d712c500eda38e7941aeda12f4a1c3deeeb7b51b1b49e2",
}

FROZEN_LEDGER = {
    "Q2_anchor_count": 114006,
    "root_Q3_inner_count": 4088,
    "root_unresolved_count": 109918,
    "terminal_Q3_inner_count": 38972,
    "terminal_R3_inner_count": 0,
    "terminal_unresolved_count": 388890,
    "terminal_depth_histogram": {"0": 4088, "1": 15898, "2": 407876},
    "terminal_blocker_histogram": {
        "unresolved_competitor:unresolved_discriminant": 373816,
        "unresolved_time2_outgoing_chart_or_geometry": 15074,
    },
    "Q3_coordinate_base_mass": "84093/2048000000",
    "R3_coordinate_base_mass": "0",
    "unresolved_coordinate_base_mass": "10095133/10240000000",
    "total_Q2_coordinate_base_mass": "5257799/5120000000",
}

GLOBAL_ROWS: list[dict[str, Any]] = []
GLOBAL_Q1: dict[str, dict[str, Any]] = {}
GLOBAL_CORES: tuple[Any, ...] = ()
GLOBAL_PAIR_INDEX: dict[Any, int] = {}
GLOBAL_PATTERN_INDEX: dict[Any, int] = {}


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def verify_dependencies() -> None:
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        require(path.is_file(), f"missing dependency: {name}")
        require(not path.is_symlink(), f"symlink dependency: {name}")
        require(path.resolve().parent == HERE, f"unsafe dependency: {name}")
        require(sha256_path(path) == expected, f"dependency hash: {name}")


def frozen_result() -> dict[str, Any]:
    ledger = dict(FROZEN_LEDGER)
    ledger["Q3_gain_over_round29"] = (
        ledger["terminal_Q3_inner_count"] - ledger["root_Q3_inner_count"]
    )
    ledger["terminal_leaf_count"] = (
        ledger["terminal_Q3_inner_count"]
        + ledger["terminal_R3_inner_count"]
        + ledger["terminal_unresolved_count"]
    )
    require(
        Q(ledger["Q3_coordinate_base_mass"])
        + Q(ledger["R3_coordinate_base_mass"])
        + Q(ledger["unresolved_coordinate_base_mass"])
        == Q(ledger["total_Q2_coordinate_base_mass"]),
        "mass conservation",
    )
    return {
        "schema": RESULT_SCHEMA,
        "adaptive_protocol": {
            "root_family": "all 114006 round-29 certified Q2 anchors",
            "split_rule": "longest normalized (t,p,s) side, binary midpoint",
            "maximum_additional_depth": MAX_EXTRA_DEPTH,
            "arithmetic": "384-bit Arb interval classification plus exact rational mass",
            "coverage": "complete",
        },
        "time3_depth2_ledger": ledger,
        "strict_nonpromotion": {
            "finite_unresolved_outer_promoted_to_null": False,
            "finite_R3_count_promoted_to_physical_R3_emptiness": False,
            "finite_depth_histogram_promoted_to_uniform_termination_rate": False,
            "complete_limiting_R3_Q3_component_enumeration": "NOT_CERTIFIED",
            "uniform_adaptive_time3_termination_rate": "NOT_CERTIFIED",
            "survivor_conditioned_recovery": "NOT_CERTIFIED",
            "strong_q_weighted_tail": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }


def classify_chunk(bounds: tuple[int, int]) -> dict[str, Any]:
    classes: Counter[str] = Counter()
    blockers: Counter[str] = Counter()
    depths: Counter[int] = Counter()
    masses: Counter[str] = Counter()
    root_unresolved = 0
    for row in GLOBAL_ROWS[bounds[0]:bounds[1]]:
        parent = GLOBAL_Q1[row["Q1_parent_atom_id"]]
        root = r29.atom_from_time2_row(row, parent, GLOBAL_CORES)
        stack = [(root, 0)]
        while stack:
            atom, depth = stack.pop()
            geometry = r29.classify_time3(
                atom, GLOBAL_CORES, GLOBAL_PAIR_INDEX, GLOBAL_PATTERN_INDEX
            )
            kind = geometry["classification"]
            if kind == "UNRESOLVED_TIME3_OUTER" and depth < MAX_EXTRA_DEPTH:
                if depth == 0:
                    root_unresolved += 1
                left, right = r29.time2_cert.step1.split_atom(atom)
                stack.extend(((right, depth + 1), (left, depth + 1)))
                continue
            classes[kind] += 1
            depths[depth] += 1
            masses[kind] += r29.time2_cert.step1.base_mass(atom)
            if kind == "UNRESOLVED_TIME3_OUTER":
                blockers[str(geometry["blocker"])] += 1
    return {
        "root_unresolved": root_unresolved,
        "classes": classes,
        "blockers": blockers,
        "depths": depths,
        "masses": masses,
    }


def replay(workers: int) -> dict[str, Any]:
    global GLOBAL_ROWS, GLOBAL_Q1, GLOBAL_CORES
    global GLOBAL_PAIR_INDEX, GLOBAL_PATTERN_INDEX
    verify_dependencies()
    pair_index, pattern_index, _ = r29.component_cert.key_index_tables()
    cores = r29.core_cert.physical_cores()
    source = r29.time2_cert.load_step1_manifest()
    q1_rows = sorted(
        (row for row in source["result"]["adaptive_full_core_step1_raw_leaf_rows"]
         if row["classification"] == "SURVIVE_THROUGH_1_INNER"),
        key=lambda row: row["atom_id"],
    )
    q1_by_id = {row["atom_id"]: row for row in q1_rows}
    rows2 = r29.time2_cert.adaptive_time2_rows(q1_rows, cores)
    q2_rows = [row for row in rows2
               if row["classification"] == "SURVIVE_THROUGH_2_INNER"]
    require(len(q2_rows) == FROZEN_LEDGER["Q2_anchor_count"], "Q2 count")
    GLOBAL_ROWS, GLOBAL_Q1, GLOBAL_CORES = q2_rows, q1_by_id, cores
    GLOBAL_PAIR_INDEX, GLOBAL_PATTERN_INDEX = pair_index, pattern_index
    totals = {
        "root_unresolved": 0,
        "classes": Counter(), "blockers": Counter(),
        "depths": Counter(), "masses": Counter(),
    }
    bounds = [(start, min(start + CHUNK_SIZE, len(q2_rows)))
              for start in range(0, len(q2_rows), CHUNK_SIZE)]
    with get_context("fork").Pool(workers) as pool:
        for part in pool.imap(classify_chunk, bounds):
            totals["root_unresolved"] += part["root_unresolved"]
            for key in ("classes", "blockers", "depths", "masses"):
                totals[key].update(part[key])
    observed = {
        "Q2_anchor_count": len(q2_rows),
        "root_Q3_inner_count": FROZEN_LEDGER["root_Q3_inner_count"],
        "root_unresolved_count": totals["root_unresolved"],
        "terminal_Q3_inner_count": totals["classes"]["SURVIVE_THROUGH_3_INNER"],
        "terminal_R3_inner_count": totals["classes"]["RETURN_AT_3_INNER"],
        "terminal_unresolved_count": totals["classes"]["UNRESOLVED_TIME3_OUTER"],
        "terminal_depth_histogram": {str(k): v for k, v in sorted(totals["depths"].items())},
        "terminal_blocker_histogram": dict(sorted(totals["blockers"].items())),
        "Q3_coordinate_base_mass": str(totals["masses"]["SURVIVE_THROUGH_3_INNER"]),
        "R3_coordinate_base_mass": str(totals["masses"]["RETURN_AT_3_INNER"]),
        "unresolved_coordinate_base_mass": str(totals["masses"]["UNRESOLVED_TIME3_OUTER"]),
        "total_Q2_coordinate_base_mass": str(sum(totals["masses"].values(), Q(0))),
    }
    require(observed == FROZEN_LEDGER, "full replay differs from frozen ledger")
    return frozen_result()


def write_manifest(path: Path, verifier: Path) -> None:
    result = frozen_result()
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier.resolve()),
        "dependencies": DEPENDENCIES,
        "result": result,
        "verdict": result["strict_nonpromotion"],
    }
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument("--verifier", type=Path, default=HERE / "cm2_gate34_round30_time3_depth2_adaptive_verifier.py")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--workers", type=int, default=min(16, os.cpu_count() or 1))
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    result = replay(args.workers) if args.replay else frozen_result()
    ledger = result["time3_depth2_ledger"]
    print("TIME3_DEPTH2_ADAPTIVE: CERTIFIED")
    print(f"Q3_COMPONENTS: {ledger['terminal_Q3_inner_count']}")
    print("GATE3: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if not args.replay else 0


if __name__ == "__main__":
    raise SystemExit(main())
