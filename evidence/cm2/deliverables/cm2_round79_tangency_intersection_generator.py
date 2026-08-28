#!/usr/bin/env python3
"""Rigorous pairwise intersection registry for Round-78 tangency carriers."""
from __future__ import annotations

import hashlib
import json
import sys
from collections import defaultdict
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as step1
from cm2_round78_tangency_curve_generator import tangency_jet


HERE = Path(__file__).resolve().parent
CURVES = HERE / "cm2-round78-time2-tangency-curves-2026-07-21.json"
SCHEMA = "cm2.round79.tangency-intersections.v1"
MAXIMUM_DEPTH = 34


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def aq(value: Q | int) -> arb:
    return step1.arbq(Q(value))


def interval(lower: Q, upper: Q) -> arb:
    return core_cert.first_hit.arb_interval(lower, upper)


def strict_sign(value: arb) -> int:
    if bool(value > 0):
        return 1
    if bool(value < 0):
        return -1
    return 0


def curve_bbox(row: dict[str, Any]) -> tuple[Q, Q, Q, Q]:
    t_values: list[Q] = []
    p_values: list[Q] = []
    for slab in row["slabs"]:
        parameter = tuple(map(Q, slab["parameter_interval"]))
        root = tuple(map(Q, slab["root_interval"]))
        if row["parameter_axis"] == "t":
            t_values.extend(parameter)
            p_values.extend(root)
        else:
            t_values.extend(root)
            p_values.extend(parameter)
    return min(t_values), max(t_values), min(p_values), max(p_values)


def overlap(
    left: tuple[Q, Q, Q, Q], right: tuple[Q, Q, Q, Q]
) -> tuple[Q, Q, Q, Q] | None:
    box = (
        max(left[0], right[0]),
        min(left[1], right[1]),
        max(left[2], right[2]),
        min(left[3], right[3]),
    )
    return box if box[0] < box[1] and box[2] < box[3] else None


def evaluate(source: Any, candidate: str, box: tuple[Q, Q, Q, Q]) -> Any:
    return tangency_jet(source, candidate, *box)


def krawczyk(
    source: Any,
    left_candidate: str,
    right_candidate: str,
    box: tuple[Q, Q, Q, Q],
) -> dict[str, Any] | None:
    t0, t1, p0, p1 = box
    tc, pc = (t0 + t1) / 2, (p0 + p1) / 2
    left_full = evaluate(source, left_candidate, box)
    right_full = evaluate(source, right_candidate, box)
    left_point = evaluate(source, left_candidate, (tc, tc, pc, pc))
    right_point = evaluate(source, right_candidate, (tc, tc, pc, pc))
    a = float(left_point.gradient[0].mid())
    b = float(left_point.gradient[1].mid())
    c = float(right_point.gradient[0].mid())
    d = float(right_point.gradient[1].mid())
    determinant = a * d - b * c
    if determinant == 0.0:
        return None
    inverse = (
        (arb(str(d / determinant)), arb(str(-b / determinant))),
        (arb(str(-c / determinant)), arb(str(a / determinant))),
    )
    functions = (left_point.value, right_point.value)
    jacobian = (left_full.gradient[:2], right_full.gradient[:2])
    displacement = (interval(t0 - tc, t1 - tc), interval(p0 - pc, p1 - pc))
    krawczyk_values = []
    for coordinate in range(2):
        value = aq((tc, pc)[coordinate])
        value -= sum(inverse[coordinate][row] * functions[row] for row in range(2))
        for column in range(2):
            coefficient = arb(1 if coordinate == column else 0)
            coefficient -= sum(
                inverse[coordinate][row] * jacobian[row][column]
                for row in range(2)
            )
            value += coefficient * displacement[column]
        krawczyk_values.append(value)
    if not (
        bool(krawczyk_values[0] > aq(t0))
        and bool(krawczyk_values[0] < aq(t1))
        and bool(krawczyk_values[1] > aq(p0))
        and bool(krawczyk_values[1] < aq(p1))
    ):
        return None
    determinant_interval = (
        left_full.gradient[0] * right_full.gradient[1]
        - left_full.gradient[1] * right_full.gradient[0]
    )
    determinant_sign = strict_sign(determinant_interval)
    if determinant_sign == 0:
        return None
    return {
        "box": [str(value) for value in box],
        "center": [str(tc), str(pc)],
        "krawczyk_strict_interior": True,
        "jacobian_determinant_sign": determinant_sign,
    }


def split(
    source: Any, box: tuple[Q, Q, Q, Q]
) -> tuple[tuple[Q, Q, Q, Q], tuple[Q, Q, Q, Q]]:
    t0, t1, p0, p1 = box
    relative_t = (t1 - t0) / (source.t1 - source.t0)
    relative_p = (p1 - p0) / (source.p1 - source.p0)
    if relative_t >= relative_p:
        middle = (t0 + t1) / 2
        return (t0, middle, p0, p1), (middle, t1, p0, p1)
    middle = (p0 + p1) / 2
    return (t0, t1, p0, middle), (t0, t1, middle, p1)


def certify_pair(
    source: Any,
    left: dict[str, Any],
    right: dict[str, Any],
    initial_box: tuple[Q, Q, Q, Q],
) -> dict[str, Any]:
    stack = [(initial_box, 0)]
    excluded = 0
    tests = 0
    maximum_depth = 0
    roots = []
    unresolved = []
    while stack:
        box, depth = stack.pop()
        maximum_depth = max(maximum_depth, depth)
        left_function = evaluate(source, left["candidate_id"], box)
        tests += 1
        if strict_sign(left_function.value):
            excluded += 1
            continue
        right_function = evaluate(source, right["candidate_id"], box)
        if strict_sign(right_function.value):
            excluded += 1
            continue
        if depth >= 6:
            root = krawczyk(
                source,
                left["candidate_id"],
                right["candidate_id"],
                box,
            )
            if root is not None:
                roots.append(root)
                continue
        if depth == MAXIMUM_DEPTH:
            unresolved.append([str(value) for value in box])
            continue
        first, second = split(source, box)
        stack.extend(((second, depth + 1), (first, depth + 1)))
    return {
        "source_core_index": left["source_core_index"],
        "left_curve_id": left["curve_id"],
        "right_curve_id": right["curve_id"],
        "initial_overlap_box": [str(value) for value in initial_box],
        "interval_box_tests": tests,
        "excluded_leaf_count": excluded,
        "maximum_depth": maximum_depth,
        "certified_intersection_count": len(roots),
        "certified_intersections": roots,
        "unresolved_count": len(unresolved),
        "unresolved_boxes_sha256": digest(unresolved),
    }


def build() -> dict[str, Any]:
    ctx.prec = 384
    document = json.loads(CURVES.read_text())["result"]
    cores = core_cert.physical_cores()
    groups: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in document["curve_rows"]:
        groups[row["source_core_index"]].append(row)
    rows = []
    bbox_disjoint = 0
    for source_index, curves in sorted(groups.items()):
        curves.sort(key=lambda row: row["curve_id"])
        for left, right in combinations(curves, 2):
            initial_box = overlap(curve_bbox(left), curve_bbox(right))
            if initial_box is None:
                bbox_disjoint += 1
                continue
            row = certify_pair(cores[source_index], left, right, initial_box)
            if row["unresolved_count"]:
                raise RuntimeError(
                    f"unresolved pair {left['curve_id']} {right['curve_id']}: "
                    f"{row['unresolved_count']} boxes"
                )
            rows.append(row)
    rows.sort(key=lambda row: (row["source_core_index"], row["left_curve_id"], row["right_curve_id"]))
    intersections = [
        {
            "source_core_index": row["source_core_index"],
            "left_curve_id": row["left_curve_id"],
            "right_curve_id": row["right_curve_id"],
            **root,
        }
        for row in rows
        for root in row["certified_intersections"]
    ]
    result = {
        "fixed_parameter": "s=0",
        "same_source_pair_count": bbox_disjoint + len(rows),
        "strict_bbox_disjoint_pair_count": bbox_disjoint,
        "interval_processed_pair_count": len(rows),
        "certified_disjoint_after_interval_subdivision_count": sum(
            row["certified_intersection_count"] == 0 for row in rows
        ),
        "intersecting_pair_count": sum(
            row["certified_intersection_count"] > 0 for row in rows
        ),
        "certified_transverse_intersection_count": len(intersections),
        "unresolved_pair_count": 0,
        "pair_rows": rows,
        "pair_rows_sha256": digest(rows),
        "intersection_rows": intersections,
        "intersection_rows_sha256": digest(intersections),
        "strict_scope": "all same-source Round-78 time-two tangency carrier pairs",
    }
    return {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}


def main() -> int:
    json.dump(build(), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
