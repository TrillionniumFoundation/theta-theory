#!/usr/bin/env python3
"""Rigorous mixed-family intersection audit for the depth-two carrier atlas."""
from __future__ import annotations

import hashlib
import json
import sys
from collections import defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Callable

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as step1
from cm2_round72_r1_positive_component_monotonicity_generator import output as r1_output
from cm2_round76_r2_numeric_fields_generator import t2_jet
from cm2_round78_tangency_curve_generator import tangency_jet
from cm2_round79_tangency_intersection_generator import (
    MAXIMUM_DEPTH,
    aq,
    canonical,
    curve_bbox,
    digest,
    interval,
    overlap,
    split,
    strict_sign,
)


HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "cm2-round78-physical-boundary-rank3-manifest-2026-07-21.json"
R1_WITNESSES = HERE / "cm2-round71-r1-nonempty-face-witnesses-2026-07-21.json"
R2_CURVES = HERE / "cm2-round75-r2-physical-curves-2026-07-21.json"
TANGENCIES = HERE / "cm2-round78-time2-tangency-curves-2026-07-21.json"
SCHEMA = "cm2.round79.mixed-carrier-intersections.v1"


Evaluator = Callable[[tuple[Q, Q, Q, Q]], Any]


def r2_bbox(row: dict[str, Any]) -> tuple[Q, Q, Q, Q]:
    t_values: list[Q] = []
    p_values: list[Q] = []
    for slab in row["slabs"]:
        t_values.extend(map(Q, slab["physical_clipped_t_interval"]))
        p_values.extend(map(Q, slab["p_interval"]))
    return min(t_values), max(t_values), min(p_values), max(p_values)


def gradient(function: Any) -> tuple[arb, arb]:
    if hasattr(function, "gradient"):
        return function.gradient[0], function.gradient[1]
    return function.dt, function.dp


def krawczyk(
    left_evaluator: Evaluator,
    right_evaluator: Evaluator,
    box: tuple[Q, Q, Q, Q],
) -> dict[str, Any] | None:
    t0, t1, p0, p1 = box
    tc, pc = (t0 + t1) / 2, (p0 + p1) / 2
    left_full, right_full = left_evaluator(box), right_evaluator(box)
    point = (tc, tc, pc, pc)
    left_point, right_point = left_evaluator(point), right_evaluator(point)
    left_point_gradient = gradient(left_point)
    right_point_gradient = gradient(right_point)
    a, b = map(lambda value: float(value.mid()), left_point_gradient)
    c, d = map(lambda value: float(value.mid()), right_point_gradient)
    determinant = a * d - b * c
    if determinant == 0.0:
        return None
    inverse = (
        (arb(str(d / determinant)), arb(str(-b / determinant))),
        (arb(str(-c / determinant)), arb(str(a / determinant))),
    )
    functions = (left_point.value, right_point.value)
    jacobian = (gradient(left_full), gradient(right_full))
    displacement = (interval(t0 - tc, t1 - tc), interval(p0 - pc, p1 - pc))
    values = []
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
        values.append(value)
    if not (
        bool(values[0] > aq(t0))
        and bool(values[0] < aq(t1))
        and bool(values[1] > aq(p0))
        and bool(values[1] < aq(p1))
    ):
        return None
    determinant_interval = (
        jacobian[0][0] * jacobian[1][1] - jacobian[0][1] * jacobian[1][0]
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


def certify_pair(
    source: Any,
    left: dict[str, Any],
    right: dict[str, Any],
    initial_box: tuple[Q, Q, Q, Q],
) -> dict[str, Any]:
    left_evaluator: Evaluator = left["evaluator"]
    right_evaluator: Evaluator = right["evaluator"]
    stack = [(initial_box, 0)]
    excluded = tests = maximum_depth = 0
    roots = []
    unresolved = []
    while stack:
        box, depth = stack.pop()
        maximum_depth = max(maximum_depth, depth)
        left_function = left_evaluator(box)
        tests += 1
        if strict_sign(left_function.value):
            excluded += 1
            continue
        right_function = right_evaluator(box)
        if strict_sign(right_function.value):
            excluded += 1
            continue
        if depth >= 6:
            root = krawczyk(left_evaluator, right_evaluator, box)
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
        "left_family": left["family"],
        "right_family": right["family"],
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


def build_specs() -> dict[int, dict[str, list[dict[str, Any]]]]:
    cores = core_cert.physical_cores()
    core_index = {step1.core_id(core): index for index, core in enumerate(cores)}
    manifest = json.loads(MANIFEST.read_text())["result"]["physical_boundary_carrier_atlas"]
    witness_index = {
        row["candidate_family_id"]: row
        for row in json.loads(R1_WITNESSES.read_text())["rows"]
    }
    groups: dict[int, dict[str, list[dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    for pair in manifest["time1_pair_rows"]:
        source_index = pair["source_core_index"]
        source = cores[source_index]
        for curve in pair["physical_curves"]:
            witness = witness_index[curve["candidate_family_id"]]
            destination = cores[witness["destination_core_index"]]
            coordinate_index = 0 if witness["level_coordinate"] == "t" else 1
            level = Q(witness["level_value"])
            def evaluator(box: tuple[Q, Q, Q, Q], source=source, destination=destination, coordinate_index=coordinate_index, level=level) -> Any:
                function = r1_output(source, destination, *box)[coordinate_index]
                function.value -= aq(level)
                return function
            groups[source_index]["R1"].append({
                "source_core_index": source_index,
                "family": "R1_destination",
                "curve_id": curve["physical_curve_id"],
                "bbox": (source.t0, source.t1, source.p0, source.p1),
                "evaluator": evaluator,
            })
    for curve in json.loads(R2_CURVES.read_text())["result"]["curve_rows"]:
        source_index = curve["source_core_index"]
        source = cores[source_index]
        destination = cores[curve["destination_core_index"]]
        coordinate_index = 0 if curve["active_side"].startswith("t_") else 1
        level = Q(curve["level"])
        def evaluator(box: tuple[Q, Q, Q, Q], source=source, destination=destination, coordinate_index=coordinate_index, level=level) -> Any:
            function = t2_jet(source, destination, *box)[coordinate_index]
            function.value -= aq(level)
            return function
        groups[source_index]["R2"].append({
            "source_core_index": source_index,
            "family": "R2_destination",
            "curve_id": curve["curve_id"],
            "bbox": r2_bbox(curve),
            "evaluator": evaluator,
        })
    for curve in json.loads(TANGENCIES.read_text())["result"]["curve_rows"]:
        source_index = curve["source_core_index"]
        source = cores[source_index]
        candidate = curve["candidate_id"]
        def evaluator(box: tuple[Q, Q, Q, Q], source=source, candidate=candidate) -> Any:
            return tangency_jet(source, candidate, *box)
        groups[source_index]["T"].append({
            "source_core_index": source_index,
            "family": "time2_tangency",
            "curve_id": curve["curve_id"],
            "bbox": curve_bbox(curve),
            "evaluator": evaluator,
        })
    return groups


def build() -> dict[str, Any]:
    ctx.prec = 384
    cores = core_cert.physical_cores()
    groups = build_specs()
    rows = []
    bbox_disjoint = 0
    family_pair_histogram: dict[str, int] = defaultdict(int)
    for source_index, families in sorted(groups.items()):
        for left_key, right_key in (("T", "R1"), ("T", "R2")):
            for left in families.get(left_key, []):
                for right in families.get(right_key, []):
                    family_pair_histogram[f"{left_key}:{right_key}"] += 1
                    initial_box = overlap(left["bbox"], right["bbox"])
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
            "left_family": row["left_family"],
            "right_family": row["right_family"],
            "left_curve_id": row["left_curve_id"],
            "right_curve_id": row["right_curve_id"],
            **root,
        }
        for row in rows
        for root in row["certified_intersections"]
    ]
    result = {
        "fixed_parameter": "s=0",
        "family_pair_histogram": dict(sorted(family_pair_histogram.items())),
        "mixed_family_pair_count": sum(family_pair_histogram.values()),
        "strict_bbox_disjoint_pair_count": bbox_disjoint,
        "interval_processed_pair_count": len(rows),
        "certified_disjoint_after_interval_subdivision_count": sum(
            row["certified_intersection_count"] == 0 for row in rows
        ),
        "intersecting_pair_count": sum(row["certified_intersection_count"] > 0 for row in rows),
        "certified_transverse_intersection_count": len(intersections),
        "unresolved_pair_count": 0,
        "pair_rows": rows,
        "pair_rows_sha256": digest(rows),
        "intersection_rows": intersections,
        "intersection_rows_sha256": digest(intersections),
        "strict_scope": "all same-source tangency-to-R1 and tangency-to-R2 physical carrier pairs",
    }
    return {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}


def main() -> int:
    json.dump(build(), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
