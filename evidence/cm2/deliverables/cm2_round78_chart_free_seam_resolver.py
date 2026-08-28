#!/usr/bin/env python3
"""Resolve Round-77 outgoing-chart tubes with a chart-free candidate union."""
from __future__ import annotations

import argparse
import hashlib
import json
import multiprocessing as mp
import sys
from collections import Counter
from fractions import Fraction as Q
from typing import Any

from flint import arb

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as step1
import cm2_gate34_round26_q1_time2_frontier_cert as time2
import cm2_round77_boundary_taxonomy_generator as taxonomy
from cm2_round74_s0_depth2_adaptive_generator import split_2d


CORES: tuple[Any, ...] = ()
MAX_DEPTH = 24
SOURCE_INDICES = (12, 13, 15, 16, 18, 19, 21, 22)


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def init_worker(cores: tuple[Any, ...], maximum_depth: int) -> None:
    global CORES, MAX_DEPTH
    CORES, MAX_DEPTH = cores, maximum_depth
    taxonomy.init_worker(cores, 20)


def outgoing_without_chart(atom: Any) -> dict[str, Any] | None:
    qx, qy, ux, uy, parameter = core_cert.first_hit.phase_geometry(atom.phase_box)
    ax, ay = time2.target_center(atom.source_core.target_id, parameter)
    dx, dy = ax - qx, ay - qy
    longitudinal = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    radius = step1.arbq(core_cert.first_hit.RADIUS[atom.source_core.target_id[0]])
    discriminant = radius * radius - transverse * transverse
    if not bool(discriminant > 0):
        return None
    radical = discriminant.sqrt()
    root = longitudinal - radical
    if not bool(root > 0) or not bool(root < step1.arbq(core_cert.first_hit.TAU_MAX)):
        return None
    normal_x = (-radical * ux + transverse * uy) / radius
    normal_y = (-radical * uy - transverse * ux) / radius
    momentum = transverse / radius
    radial_square = 1 - momentum * momentum
    if not bool(radial_square > 0):
        return None
    radial = radial_square.sqrt()
    outgoing_x = radial * normal_x - momentum * normal_y
    outgoing_y = radial * normal_y + momentum * normal_x
    return {
        "contact_x": ax + radius * normal_x,
        "contact_y": ay + radius * normal_y,
        "outgoing_x": outgoing_x,
        "outgoing_y": outgoing_y,
        "parameter": parameter,
    }


def chart_free_classify(atom: Any) -> dict[str, Any]:
    state = outgoing_without_chart(atom)
    if state is None:
        return {"classification": "OUTER_GEOMETRY", "carrier_ids": ["OUTGOING_GEOMETRY"]}
    candidate_ids = sorted({
        candidate
        for chart in ("E", "W", "N", "S")
        for candidate in time2.translated_candidate_ids(atom.source_core.target_id, chart)
    })
    future = []
    unresolved = []
    for candidate in candidate_ids:
        row = time2.candidate_root(
            state["contact_x"], state["contact_y"],
            state["outgoing_x"], state["outgoing_y"],
            state["parameter"], candidate,
        )
        kind = row["classification"]
        if kind == "strict_future_near_root":
            future.append((candidate, row))
        elif kind.startswith("unresolved_"):
            unresolved.append(f"SECOND_CANDIDATE:{candidate}:{kind}")
    if unresolved:
        return {"classification": "OUTER_TANGENCY", "carrier_ids": sorted(unresolved)}
    winners = []
    for candidate, row in future:
        if all(candidate == other or bool(row["near"] < other_row["near"]) for other, other_row in future):
            winners.append((candidate, row))
    if len(winners) != 1:
        return {"classification": "OUTER_OWNER_ORDER", "carrier_ids": ["SECOND_OWNER_ORDER"]}
    selected_id, selected = winners[0]
    root = selected["near"]
    if not bool(root < step1.arbq(core_cert.first_hit.TAU_MAX)):
        return {"classification": "OUTER_TAU_MAX", "carrier_ids": ["SECOND_TAU_MAX"]}
    radius = selected["radius"]
    transverse = selected["transverse"]
    radical = selected["radical"]
    ux, uy = state["outgoing_x"], state["outgoing_y"]
    normal_x = (-radical * ux + transverse * uy) / radius
    normal_y = (-radical * uy - transverse * ux) / radius
    momentum = transverse / radius
    inside = []
    unresolved_destinations = []
    for destination in CORES:
        if destination.source != selected_id[0]:
            continue
        identifier = step1.core_id(destination)
        cell = destination.chart_id.split(":")[1]
        coordinate, inside_chart, outside_chart = step1.chart_tests(cell, normal_x, normal_y)
        inside_tests = inside_chart + [
            ("t_gt_t0", bool(coordinate > step1.arbq(destination.t0))),
            ("t_lt_t1", bool(coordinate < step1.arbq(destination.t1))),
            ("p_gt_p0", bool(momentum > step1.arbq(destination.p0))),
            ("p_lt_p1", bool(momentum < step1.arbq(destination.p1))),
        ]
        if all(value for _name, value in inside_tests):
            inside.append(identifier)
            continue
        separators = outside_chart + [
            ("t_lt_t0", bool(coordinate < step1.arbq(destination.t0))),
            ("t_gt_t1", bool(coordinate > step1.arbq(destination.t1))),
            ("p_lt_p0", bool(momentum < step1.arbq(destination.p0))),
            ("p_gt_p1", bool(momentum > step1.arbq(destination.p1))),
        ]
        if not any(value for _name, value in separators):
            unresolved_destinations.append("TIME2_DESTINATION_CORE:" + identifier)
    if unresolved_destinations or len(inside) > 1:
        return {"classification": "OUTER_DESTINATION", "carrier_ids": sorted(unresolved_destinations)}
    if len(inside) == 1:
        return {"classification": "R2_INNER", "destination_core_id": inside[0], "selected_target_id": selected_id}
    return {"classification": "Q2_INNER", "destination_core_id": None, "selected_target_id": selected_id}


def normalized_area(atom: Any) -> Q:
    core = atom.source_core
    return (atom.t1 - atom.t0) * (atom.p1 - atom.p0) / ((core.t1 - core.t0) * (core.p1 - core.p0))


def process_source(source_core_index: int) -> dict[str, Any]:
    frozen = taxonomy.process_core(source_core_index)
    seeds = []
    for row in frozen["outer_rows"]:
        if row["carriers"] != ["OUTGOING_CHART_OR_GEOMETRY"]:
            continue
        path = row["dyadic_path"]
        i, j = int(path[0::2], 2), int(path[1::2], 2)
        core = CORES[source_core_index]
        t0 = core.t0 + (core.t1 - core.t0) * Q(i, 1024)
        t1 = core.t0 + (core.t1 - core.t0) * Q(i + 1, 1024)
        p0 = core.p0 + (core.p1 - core.p0) * Q(j, 1024)
        p1 = core.p0 + (core.p1 - core.p0) * Q(j + 1, 1024)
        seeds.append(step1.Atom(source_core_index, core, t0, t1, p0, p1, Q(0), Q(0), path))
    rows = []
    stack = list(reversed(seeds))
    tests = 0
    while stack:
        atom = stack.pop()
        result = chart_free_classify(atom)
        tests += 1
        if result["classification"].startswith("OUTER_") and atom.depth < MAX_DEPTH:
            left, right = split_2d(atom)
            stack.extend((right, left))
            continue
        rows.append({
            "source_core_index": source_core_index,
            "dyadic_path": atom.path,
            "depth": atom.depth,
            "normalized_area": str(normalized_area(atom)),
            **result,
        })
    rows.sort(key=lambda row: row["dyadic_path"])
    return {"source_core_index": source_core_index, "seed_count": len(seeds), "test_count": tests, "rows": rows}


def build(workers: int, maximum_depth: int) -> dict[str, Any]:
    cores = core_cert.physical_cores()
    context = mp.get_context("fork")
    with context.Pool(workers, initializer=init_worker, initargs=(cores, maximum_depth)) as pool:
        source_rows = pool.map(process_source, SOURCE_INDICES)
    histogram = Counter()
    areas = Counter()
    carrier_histogram = Counter()
    terminal_rows = []
    for source in source_rows:
        for row in source.pop("rows"):
            histogram[row["classification"]] += 1
            areas[row["classification"]] += Q(row["normalized_area"])
            for carrier in row.get("carrier_ids", []):
                carrier_histogram[carrier] += 1
            terminal_rows.append(row)
    terminal_rows.sort(key=canonical)
    return {
        "schema": "cm2.round78.chart-free-seam-resolution.v1",
        "result": {
            "seed_depth": 20,
            "maximum_depth": maximum_depth,
            "seed_leaf_count": sum(row["seed_count"] for row in source_rows),
            "terminal_leaf_count": len(terminal_rows),
            "classification_histogram": dict(sorted(histogram.items())),
            "normalized_area_ledger": {key: str(value) for key, value in sorted(areas.items())},
            "remaining_carrier_histogram": dict(sorted(carrier_histogram.items())),
            "source_rows": source_rows,
            "terminal_rows": terminal_rows,
            "terminal_rows_sha256": digest(terminal_rows),
            "outgoing_chart_seam_is_not_a_physical_carrier": "CERTIFIED_WHERE_CHART_FREE_UNION_CLASSIFIES; ANY_REMAINDER_IS_RETYPED_TO_PHYSICAL_GEOMETRY/TANGENCY/DESTINATION_CARRIERS",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--maximum-depth", type=int, default=24)
    args = parser.parse_args()
    json.dump(build(args.workers, args.maximum_depth), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
