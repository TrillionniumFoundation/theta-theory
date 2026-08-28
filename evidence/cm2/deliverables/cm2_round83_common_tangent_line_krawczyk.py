#!/usr/bin/env python3
"""Resolve rank-three candidate intersections in outgoing-line common-tangent coordinates."""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import sys
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
from cm2_round79_tangency_intersection_generator import aq, digest, interval, strict_sign
from cm2_round83_graph_difference_resolver import Dual, dual_center, dual_collision, dual_normal


HERE = Path(__file__).resolve().parent
PREFILTER = HERE / "cm2-round82-rank3-intersection-prefilter-2026-07-21.json"
JOINS = HERE / "cm2-round82-rank3-cross-tube-joins-2026-07-21.json"
MAXIMUM_DEPTH = 12
WORK_CORES: tuple[Any, ...] = ()
WORK_METADATA: dict[str, dict[str, Any]] = {}


def init_worker(cores: tuple[Any, ...], metadata: dict[str, dict[str, Any]]) -> None:
    global WORK_CORES, WORK_METADATA
    WORK_CORES, WORK_METADATA = cores, metadata
    ctx.prec = 384


def center_q(identifier: str) -> tuple[Q, Q]:
    obstacle = identifier[0]
    ix, iy = map(int, identifier[2:-1].split(","))
    offset = Q(0) if obstacle == "G" else Q(1, 2)
    return Q(ix) + offset, Q(iy) + offset


def radius_q(identifier: str) -> Q:
    return Q(9, 25) if identifier[0] == "G" else Q(4, 25)


def common_tangent_targets(left_candidate: str, right_candidate: str) -> list[dict[str, Any]]:
    left_center, right_center = center_q(left_candidate), center_q(right_candidate)
    dx, dy = left_center[0] - right_center[0], left_center[1] - right_center[1]
    norm2 = dx * dx + dy * dy
    if norm2 == 0:
        raise RuntimeError("coincident candidate centers")
    rows = []
    for left_sign in (-1, 1):
        for right_sign in (-1, 1):
            delta = left_sign * radius_q(left_candidate) - right_sign * radius_q(right_candidate)
            radicand = aq(norm2 - delta * delta).sqrt()
            for branch_sign in (-1, 1):
                nx = aq(delta * dx / norm2) + branch_sign * radicand * aq(-dy / norm2)
                ny = aq(delta * dy / norm2) + branch_sign * radicand * aq(dx / norm2)
                h = nx * aq(left_center[0]) + ny * aq(left_center[1]) - aq(left_sign * radius_q(left_candidate))
                rows.append({
                    "left_signed_distance": left_sign,
                    "right_signed_distance": right_sign,
                    "normal_branch": branch_sign,
                    "nx": nx,
                    "ny": ny,
                    "h": h,
                })
    return rows


def outgoing_line(source: Any, second: str, t_value: arb, p_value: arb) -> tuple[Dual, Dual, Dual]:
    t, p = Dual.variable(t_value, 0), Dual.variable(p_value, 1)
    normal_x, normal_y = dual_normal(source.chart_id.split(":")[1], t)
    radial = (arb(1) - p * p).sqrt()
    velocity_x, velocity_y = radial * normal_x - p * normal_y, radial * normal_y + p * normal_x
    source_x, source_y = dual_center(f"{source.source}[0,0]")
    source_radius = Q(9, 25) if source.source == "G" else Q(4, 25)
    point_x, point_y = source_x + aq(source_radius) * normal_x, source_y + aq(source_radius) * normal_y
    first_x, first_y = dual_center(source.target_id)
    first_radius = Q(9, 25) if source.target_id[0] == "G" else Q(4, 25)
    hit1_x, hit1_y, normal1_x, normal1_y, first_p = dual_collision(
        point_x, point_y, velocity_x, velocity_y, first_x, first_y, first_radius
    )
    radial1 = (arb(1) - first_p * first_p).sqrt()
    outgoing1_x, outgoing1_y = radial1 * normal1_x - first_p * normal1_y, radial1 * normal1_y + first_p * normal1_x
    second_x, second_y = dual_center(second)
    second_radius = Q(9, 25) if second[0] == "G" else Q(4, 25)
    hit2_x, hit2_y, normal2_x, normal2_y, second_p = dual_collision(
        hit1_x, hit1_y, outgoing1_x, outgoing1_y, second_x, second_y, second_radius
    )
    radial2 = (arb(1) - second_p * second_p).sqrt()
    outgoing2_x, outgoing2_y = radial2 * normal2_x - second_p * normal2_y, radial2 * normal2_y + second_p * normal2_x
    nx, ny = -outgoing2_y, outgoing2_x
    h = nx * hit2_x + ny * hit2_y
    return nx, ny, h


def target_excluded(line: tuple[Dual, Dual, Dual], target: dict[str, Any]) -> bool:
    return strict_sign(line[0].value - target["nx"]) != 0 or strict_sign(line[1].value - target["ny"]) != 0 or strict_sign(line[2].value - target["h"]) != 0


def krawczyk(
    source: Any,
    second: str,
    target: dict[str, Any],
    box: tuple[Q, Q, Q, Q],
) -> dict[str, Any] | None:
    t0, t1, p0, p1 = box
    tc, pc = (t0 + t1) / 2, (p0 + p1) / 2
    full = outgoing_line(source, second, interval(t0, t1), interval(p0, p1))
    point = outgoing_line(source, second, aq(tc), aq(pc))
    coordinate_options = [
        (0, target["nx"], "nx_h"),
        (1, target["ny"], "ny_h"),
    ]
    best = None
    for coordinate, target_normal, label in coordinate_options:
        a = float(point[coordinate].gradient[0].mid())
        b = float(point[coordinate].gradient[1].mid())
        c = float(point[2].gradient[0].mid())
        d = float(point[2].gradient[1].mid())
        determinant = a * d - b * c
        if determinant != 0.0 and (best is None or abs(determinant) > abs(best[0])):
            best = determinant, coordinate, target_normal, label, a, b, c, d
    if best is None:
        return None
    determinant, coordinate, target_normal, label, a, b, c, d = best
    inverse = (
        (arb(str(d / determinant)), arb(str(-b / determinant))),
        (arb(str(-c / determinant)), arb(str(a / determinant))),
    )
    functions = point[coordinate].value - target_normal, point[2].value - target["h"]
    jacobian = full[coordinate].gradient, full[2].gradient
    displacement = interval(t0 - tc, t1 - tc), interval(p0 - pc, p1 - pc)
    values = []
    for output_coordinate in range(2):
        value = aq((tc, pc)[output_coordinate])
        value -= sum(inverse[output_coordinate][row] * functions[row] for row in range(2))
        for input_coordinate in range(2):
            coefficient = arb(1 if output_coordinate == input_coordinate else 0)
            coefficient -= sum(inverse[output_coordinate][row] * jacobian[row][input_coordinate] for row in range(2))
            value += coefficient * displacement[input_coordinate]
        values.append(value)
    if not (
        bool(values[0] > aq(t0)) and bool(values[0] < aq(t1))
        and bool(values[1] > aq(p0)) and bool(values[1] < aq(p1))
    ):
        return None
    determinant_interval = (
        jacobian[0][0] * jacobian[1][1]
        - jacobian[0][1] * jacobian[1][0]
    )
    determinant_sign = strict_sign(determinant_interval)
    if determinant_sign == 0:
        return None
    return {
        "box": list(map(str, box)),
        "center": [str(tc), str(pc)],
        "line_coordinate_chart": label,
        "jacobian_determinant_sign": determinant_sign,
        "left_signed_distance": target["left_signed_distance"],
        "right_signed_distance": target["right_signed_distance"],
        "normal_branch": target["normal_branch"],
    }


def split(source: Any, box: tuple[Q, Q, Q, Q]) -> tuple[tuple[Q, Q, Q, Q], tuple[Q, Q, Q, Q]]:
    t0, t1, p0, p1 = box
    if (t1 - t0) / (source.t1 - source.t0) >= (p1 - p0) / (source.p1 - source.p0):
        middle = (t0 + t1) / 2
        return (t0, middle, p0, p1), (middle, t1, p0, p1)
    middle = (p0 + p1) / 2
    return (t0, t1, p0, middle), (t0, t1, middle, p1)


def resolve_box(source: Any, second: str, targets: list[dict[str, Any]], initial: tuple[Q, Q, Q, Q]) -> dict[str, Any]:
    if initial[0] == initial[1] or initial[2] == initial[3]:
        return {"status": "DEGENERATE_INTERFACE_BOX", "tests": 0, "roots": [], "unresolved": 0, "maximum_depth": 0}
    stack = [(initial, 0, tuple(range(len(targets))))]
    roots = []
    unresolved = []
    excluded = 0
    tests = 0
    maximum_depth = 0
    while stack:
        box, depth, active_targets = stack.pop()
        maximum_depth = max(maximum_depth, depth)
        line = outgoing_line(source, second, interval(box[0], box[1]), interval(box[2], box[3]))
        tests += 1
        survivors = tuple(index for index in active_targets if not target_excluded(line, targets[index]))
        if not survivors:
            excluded += 1
            continue
        certified = []
        for index in survivors:
            root = krawczyk(source, second, targets[index], box)
            if root is not None:
                certified.append(root)
        if certified:
            roots.extend(certified)
            continue
        if depth == MAXIMUM_DEPTH:
            unresolved.append(list(map(str, box)))
            continue
        first, second_box = split(source, box)
        stack.extend(((second_box, depth + 1, survivors), (first, depth + 1, survivors)))
    if unresolved:
        status = "UNRESOLVED_COMMON_TANGENT_LINE"
    elif roots:
        status = "CERTIFIED_INTERSECTING"
    else:
        status = "CERTIFIED_DISJOINT"
    return {
        "status": status,
        "tests": tests,
        "excluded": excluded,
        "roots": roots,
        "unresolved": len(unresolved),
        "unresolved_sha256": digest(sorted(unresolved)),
        "maximum_depth": maximum_depth,
    }


def process_pair(row: dict[str, Any]) -> dict[str, Any]:
    left_id, right_id = row["left_physical_root_component_id"], row["right_physical_root_component_id"]
    left, right = WORK_METADATA[left_id], WORK_METADATA[right_id]
    source = WORK_CORES[left["source_core_index"]]
    second = left["second_selected_target_id"]
    targets = common_tangent_targets(left["third_candidate_id"], right["third_candidate_id"])
    histogram = Counter()
    tests = 0
    excluded = 0
    roots = []
    unresolved = 0
    unresolved_initial_boxes = []
    degenerate_interface_boxes = []
    maximum_depth = 0
    for raw_box in row["residual_boxes"]:
        result = resolve_box(source, second, targets, tuple(map(Q, raw_box)))
        histogram[result["status"]] += 1
        tests += result["tests"]
        excluded += result.get("excluded", 0)
        roots.extend(result["roots"])
        unresolved += result["unresolved"]
        if result["status"] == "UNRESOLVED_COMMON_TANGENT_LINE":
            unresolved_initial_boxes.append(raw_box)
        if result["status"] == "DEGENERATE_INTERFACE_BOX":
            degenerate_interface_boxes.append(raw_box)
        maximum_depth = max(maximum_depth, result["maximum_depth"])
    roots.sort(key=lambda root: (root["box"], root["left_signed_distance"], root["right_signed_distance"], root["normal_branch"]))
    return {
        "left_physical_root_component_id": left_id,
        "right_physical_root_component_id": right_id,
        "input_residual_box_count": len(row["residual_boxes"]),
        "box_status_histogram": dict(sorted(histogram.items())),
        "interval_line_box_test_count": tests,
        "excluded_leaf_count": excluded,
        "raw_krawczyk_root_count": len(roots),
        "root_rows_sha256": digest(roots),
        "unresolved_leaf_count": unresolved,
        "unresolved_initial_box_count": len(unresolved_initial_boxes),
        "unresolved_initial_boxes": sorted(unresolved_initial_boxes),
        "unresolved_initial_boxes_sha256": digest(sorted(unresolved_initial_boxes)),
        "degenerate_interface_box_count": len(degenerate_interface_boxes),
        "degenerate_interface_boxes_sha256": digest(sorted(degenerate_interface_boxes)),
        "maximum_depth": maximum_depth,
    }


def build(workers: int = 24, pair_limit: int | None = None) -> dict[str, Any]:
    rows = [row for row in json.loads(PREFILTER.read_text())["result"]["pair_rows"] if row["residual_box_count"]]
    if pair_limit is not None:
        rows = rows[:pair_limit]
    components = json.loads(JOINS.read_text())["result"]["component_rows"]
    metadata = {row["physical_root_component_id"]: row for row in components}
    context = mp.get_context("fork")
    with context.Pool(workers, initializer=init_worker, initargs=(core_cert.physical_cores(), metadata)) as pool:
        pair_rows = pool.map(process_pair, rows)
    pair_rows.sort(key=lambda row: (row["left_physical_root_component_id"], row["right_physical_root_component_id"]))
    histogram = Counter()
    for row in pair_rows:
        histogram.update(row["box_status_histogram"])
    result = {
        "input_component_pair_count": len(pair_rows),
        "input_residual_box_count": sum(row["input_residual_box_count"] for row in pair_rows),
        "box_status_histogram": dict(sorted(histogram.items())),
        "interval_line_box_test_count": sum(row["interval_line_box_test_count"] for row in pair_rows),
        "raw_krawczyk_root_count": sum(row["raw_krawczyk_root_count"] for row in pair_rows),
        "unresolved_leaf_count": sum(row["unresolved_leaf_count"] for row in pair_rows),
        "unresolved_initial_box_count": sum(row["unresolved_initial_box_count"] for row in pair_rows),
        "maximum_depth": max(row["maximum_depth"] for row in pair_rows),
        "pair_limit": pair_limit,
        "pair_rows": pair_rows,
        "pair_rows_sha256": digest(pair_rows),
        "strict_scope": "common-tangent outgoing-line Krawczyk on Round-82 residual boxes; degenerate interface boxes are handled separately",
    }
    return {"schema": "cm2.round83.common-tangent-line-krawczyk.v1", "result": result, "result_sha256": digest(result)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=24)
    parser.add_argument("--pair-limit", type=int)
    args = parser.parse_args()
    json.dump(build(args.workers, args.pair_limit), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
