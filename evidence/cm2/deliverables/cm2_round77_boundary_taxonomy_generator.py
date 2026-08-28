#!/usr/bin/env python3
"""Classify every frozen depth-20 outer leaf by its first failed strict test."""
from __future__ import annotations

import argparse
import hashlib
import json
import multiprocessing as mp
import sys
from collections import Counter, defaultdict
from fractions import Fraction as Q
from typing import Any

import cm2_gate34_full_core_return_adaptive_frontier_cert as step1
import cm2_gate34_round26_q1_time2_frontier_cert as time2
from cm2_round74_s0_depth2_adaptive_generator import split_2d


SCHEMA = "cm2.round77.boundary-taxonomy.v1"
CORES: tuple[Any, ...] = ()
MAX_DEPTH = 20


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def init_worker(cores: tuple[Any, ...], maximum_depth: int) -> None:
    global CORES, MAX_DEPTH
    CORES, MAX_DEPTH = cores, maximum_depth


def time1_reason(first: dict[str, Any]) -> str:
    witnesses = first["witness_rows"]
    if witnesses == [{"kind": "unresolved_collision_geometry"}]:
        return "TIME1_COLLISION_GEOMETRY"
    unresolved = sorted(
        row["core_id"] for row in witnesses if row["kind"] == "unresolved"
    )
    if unresolved:
        return "TIME1_DESTINATION_FACE:" + ",".join(unresolved)
    return "TIME1_OTHER_STRICTNESS"


def time2_reason(second: dict[str, Any]) -> str:
    owner_status = second["owner_status"]
    if owner_status != "strict_unique_second_collision_owner":
        return "TIME2_OWNER:" + owner_status
    if second["selected_target_id"] is not None:
        return "TIME2_DESTINATION_FACE:" + second["selected_target_id"]
    return "TIME2_OTHER_STRICTNESS"


def time2_carriers(atom: Any, second: dict[str, Any]) -> list[str]:
    state = time2.first_collision_outgoing(atom)
    if state is None:
        return ["OUTGOING_CHART_OR_GEOMETRY"]
    qx, qy = state["contact_x"], state["contact_y"]
    ux, uy, parameter = state["outgoing_x"], state["outgoing_y"], state["s"]
    chart = state["chart"]
    unresolved = []
    for candidate_id in time2.translated_candidate_ids(atom.source_core.target_id, chart):
        row = time2.candidate_root(qx, qy, ux, uy, parameter, candidate_id)
        if row["classification"].startswith("unresolved_"):
            unresolved.append(
                "SECOND_CANDIDATE:" + candidate_id + ":" + row["classification"]
            )
    if unresolved:
        return sorted(unresolved)
    owner, status = time2.strict_second_owner(atom)
    if owner is None:
        return ["SECOND_OWNER:" + status]
    normal_x, normal_y, p = owner["normal_x"], owner["normal_y"], owner["p"]
    destination_faces = []
    for destination in CORES:
        if destination.source != owner["selected_target_id"][0]:
            continue
        identifier = step1.core_id(destination)
        cell = destination.chart_id.split(":")[1]
        t, inside_chart_tests, outside_chart_tests = step1.chart_tests(
            cell, normal_x, normal_y
        )
        inside_tests = inside_chart_tests + [
            ("t_gt_t0", bool(t > step1.arbq(destination.t0))),
            ("t_lt_t1", bool(t < step1.arbq(destination.t1))),
            ("p_gt_p0", bool(p > step1.arbq(destination.p0))),
            ("p_lt_p1", bool(p < step1.arbq(destination.p1))),
        ]
        if all(value for _name, value in inside_tests):
            continue
        separators = outside_chart_tests + [
            ("t_lt_t0", bool(t < step1.arbq(destination.t0))),
            ("t_gt_t1", bool(t > step1.arbq(destination.t1))),
            ("p_lt_p0", bool(p < step1.arbq(destination.p0))),
            ("p_gt_p1", bool(p > step1.arbq(destination.p1))),
        ]
        if not any(value for _name, value in separators):
            destination_faces.append("TIME2_DESTINATION_CORE:" + identifier)
    return sorted(destination_faces) or ["TIME2_OTHER_STRICTNESS"]


def compact(
    atom: Any, stage: str, reason: str, carriers: list[str]
) -> dict[str, Any]:
    return {
        "source_core_index": atom.source_core_index,
        "dyadic_path": atom.path,
        "stage": stage,
        "reason": reason,
        "carriers": carriers,
    }


def process_core(source_core_index: int) -> dict[str, Any]:
    core = CORES[source_core_index]
    root = step1.Atom(
        source_core_index, core, core.t0, core.t1, core.p0, core.p1,
        Q(0), Q(0), "",
    )
    stack = [root]
    outer_rows: list[dict[str, Any]] = []
    terminal_counts = Counter()
    tests = Counter()
    while stack:
        atom = stack.pop()
        first = step1.classify_atom(atom, CORES)
        tests["step1"] += 1
        if first["classification"] == "RETURN_AT_1_INNER":
            terminal_counts["R1_INNER"] += 1
            continue
        if first["classification"] == "SURVIVE_THROUGH_1_INNER":
            second = time2.classify_time2(atom, CORES)
            tests["step2"] += 1
            if second["classification"] == "RETURN_AT_2_INNER":
                terminal_counts["R2_INNER"] += 1
                continue
            if second["classification"] == "SURVIVE_THROUGH_2_INNER":
                terminal_counts["Q2_INNER"] += 1
                continue
            stage = "time2"
            reason = time2_reason(second)
            carriers = time2_carriers(atom, second)
        else:
            stage = "time1"
            reason = time1_reason(first)
            carriers = [reason]
        if atom.depth < MAX_DEPTH:
            left, right = split_2d(atom)
            stack.extend((right, left))
        else:
            terminal_counts["DEPTH2_OUTER"] += 1
            outer_rows.append(compact(atom, stage, reason, carriers))
    outer_rows.sort(key=lambda row: row["dyadic_path"])
    return {
        "source_core_index": source_core_index,
        "source_core_id": time2.step1.core_id(core),
        "terminal_counts": dict(sorted(terminal_counts.items())),
        "test_counts": dict(sorted(tests.items())),
        "outer_rows": outer_rows,
    }


def build(workers: int, maximum_depth: int) -> dict[str, Any]:
    cores = time2.core_cert.physical_cores()
    context = mp.get_context("fork")
    with context.Pool(
        workers, initializer=init_worker, initargs=(cores, maximum_depth)
    ) as pool:
        core_rows = pool.map(process_core, range(len(cores)))

    terminal_counts = Counter()
    reason_counts = Counter()
    stage_counts = Counter()
    per_core_reason_counts: dict[str, dict[str, int]] = {}
    all_outer_ids: list[dict[str, Any]] = []
    reason_ids: dict[str, list[dict[str, Any]]] = defaultdict(list)
    samples: dict[str, list[dict[str, Any]]] = defaultdict(list)
    carrier_counts = Counter()
    carrier_leaf_ids: dict[str, list[dict[str, Any]]] = defaultdict(list)
    uncovered_outer_count = 0
    for core in core_rows:
        terminal_counts.update(core["terminal_counts"])
        local = Counter(row["reason"] for row in core["outer_rows"])
        per_core_reason_counts[str(core["source_core_index"])] = dict(sorted(local.items()))
        for row in core.pop("outer_rows"):
            identifier = {
                "source_core_index": row["source_core_index"],
                "dyadic_path": row["dyadic_path"],
            }
            all_outer_ids.append(identifier)
            reason_ids[row["reason"]].append(identifier)
            reason_counts[row["reason"]] += 1
            stage_counts[row["stage"]] += 1
            if not row["carriers"]:
                uncovered_outer_count += 1
            for carrier in row["carriers"]:
                carrier_counts[carrier] += 1
                carrier_leaf_ids[carrier].append(identifier)
            if len(samples[row["reason"]]) < 3:
                samples[row["reason"]].append(identifier)

    all_outer_ids.sort(key=canonical)
    reason_rows = []
    for reason in sorted(reason_ids):
        identifiers = sorted(reason_ids[reason], key=canonical)
        count = len(identifiers)
        reason_rows.append({
            "reason": reason,
            "leaf_count": count,
            "normalized_area": str(Q(count, 2 ** maximum_depth)),
            "leaf_id_set_sha256": digest(identifiers),
            "samples": samples[reason],
        })
    outer_count = len(all_outer_ids)
    if outer_count != terminal_counts["DEPTH2_OUTER"]:
        raise RuntimeError("outer row count mismatch")
    if sum(reason_counts.values()) != outer_count:
        raise RuntimeError("reason partition mismatch")
    carrier_rows = []
    for carrier in sorted(carrier_leaf_ids):
        identifiers = sorted(carrier_leaf_ids[carrier], key=canonical)
        carrier_rows.append({
            "carrier": carrier,
            "covered_leaf_count": carrier_counts[carrier],
            "covered_leaf_id_set_sha256": digest(identifiers),
        })
    return {
        "schema": SCHEMA,
        "result": {
            "fixed_parameter": "s=0",
            "maximum_binary_depth": maximum_depth,
            "source_core_count": len(cores),
            "terminal_counts": dict(sorted(terminal_counts.items())),
            "outer_leaf_count": outer_count,
            "outer_normalized_area": str(Q(outer_count, 2 ** maximum_depth)),
            "stage_counts": dict(sorted(stage_counts.items())),
            "reason_count": len(reason_rows),
            "reason_rows": reason_rows,
            "carrier_count": len(carrier_rows),
            "carrier_rows": carrier_rows,
            "uncovered_outer_leaf_count": uncovered_outer_count,
            "every_outer_leaf_has_at_least_one_carrier": uncovered_outer_count == 0,
            "per_core_reason_counts": per_core_reason_counts,
            "all_outer_leaf_id_set_sha256": digest(all_outer_ids),
            "reason_partition_count_exact": sum(reason_counts.values()) == outer_count,
            "carrier_interpretation": {
                "TIME1_COLLISION_GEOMETRY": "time-one discriminant/root/radial strictness tube",
                "TIME1_DESTINATION_FACE:*": "time-one destination chart/core face tube",
                "TIME2_OWNER:unresolved_time1_outgoing_chart_or_geometry": "outgoing-chart seam or time-one outgoing geometry tube",
                "TIME2_OWNER:unresolved_competitor:*": "second-collision tangency/root-sign tube",
                "TIME2_OWNER:unresolved_strict_root_order": "second-owner competition tube",
                "TIME2_OWNER:selected_root_not_strictly_below_tau_max": "time-two cutoff face tube",
                "TIME2_DESTINATION_FACE:*": "time-two destination chart/core face tube",
            },
            "actual_codimension_one_carrier_atlas": "NOT_CERTIFIED__INTERVAL_TUBE_COVER_ONLY",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=16)
    parser.add_argument("--maximum-depth", type=int, default=20)
    args = parser.parse_args()
    json.dump(build(args.workers, args.maximum_depth), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
