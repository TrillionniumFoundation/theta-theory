#!/usr/bin/env python3
"""One-dimensional graph-difference resolver for rank-three intersection boxes."""
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


HERE = Path(__file__).resolve().parent
PREFILTER = HERE / "cm2-round83-residual-graph-geometry-2026-07-22.json"
JOINS = HERE / "cm2-round82-rank3-cross-tube-joins-2026-07-21.json"
MAXIMUM_PARAMETER_DEPTH = 4
ROOT_NEWTON_STEPS = 4
WORK_CORES: tuple[Any, ...] = ()
WORK_METADATA: dict[str, dict[str, Any]] = {}


def init_worker(cores: tuple[Any, ...], metadata: dict[str, dict[str, Any]]) -> None:
    global WORK_CORES, WORK_METADATA
    WORK_CORES, WORK_METADATA = cores, metadata
    ctx.prec = 384


class Dual:
    def __init__(self, value: arb, gradient: tuple[arb, arb] | None = None):
        self.value = value
        self.gradient = gradient or (arb(0), arb(0))

    @staticmethod
    def variable(value: arb, index: int) -> "Dual":
        return Dual(value, (arb(1), arb(0)) if index == 0 else (arb(0), arb(1)))

    def __add__(self, other: Any) -> "Dual":
        other = other if isinstance(other, Dual) else Dual(other)
        return Dual(self.value + other.value, tuple(self.gradient[i] + other.gradient[i] for i in range(2)))

    __radd__ = __add__

    def __neg__(self) -> "Dual":
        return Dual(-self.value, tuple(-value for value in self.gradient))

    def __sub__(self, other: Any) -> "Dual":
        return self + (-other if isinstance(other, Dual) else -other)

    def __rsub__(self, other: Any) -> "Dual":
        return Dual(other) - self

    def __mul__(self, other: Any) -> "Dual":
        other = other if isinstance(other, Dual) else Dual(other)
        return Dual(
            self.value * other.value,
            tuple(self.gradient[i] * other.value + self.value * other.gradient[i] for i in range(2)),
        )

    __rmul__ = __mul__

    def inverse(self) -> "Dual":
        return Dual(1 / self.value, tuple(-value / (self.value * self.value) for value in self.gradient))

    def __truediv__(self, other: Any) -> "Dual":
        return self * (other.inverse() if isinstance(other, Dual) else 1 / other)

    def __rtruediv__(self, other: Any) -> "Dual":
        return Dual(other) * self.inverse()

    def sqrt(self) -> "Dual":
        root = self.value.sqrt()
        return Dual(root, tuple(value / (2 * root) for value in self.gradient))


def dual_normal(side: str, coordinate: Dual) -> tuple[Dual, Dual]:
    radial = (arb(1) - coordinate * coordinate).sqrt()
    if side == "E":
        return radial, coordinate
    if side == "W":
        return -radial, coordinate
    if side == "N":
        return coordinate, radial
    return coordinate, -radial


def dual_center(identifier: str) -> tuple[Dual, Dual]:
    obstacle = identifier[0]
    ix, iy = map(int, identifier[2:-1].split(","))
    if obstacle == "G":
        return Dual(arb(ix)), Dual(arb(iy))
    return Dual(arb(ix) + aq(Q(1, 2))), Dual(arb(iy) + aq(Q(1, 2)))


def dual_collision(
    point_x: Dual,
    point_y: Dual,
    velocity_x: Dual,
    velocity_y: Dual,
    target_x: Dual,
    target_y: Dual,
    radius: Q,
) -> tuple[Dual, Dual, Dual, Dual, Dual]:
    radius_ball = aq(radius)
    dx, dy = target_x - point_x, target_y - point_y
    longitudinal = velocity_x * dx + velocity_y * dy
    transverse = -velocity_y * dx + velocity_x * dy
    radical = (radius_ball * radius_ball - transverse * transverse).sqrt()
    flight = longitudinal - radical
    hit_x, hit_y = point_x + flight * velocity_x, point_y + flight * velocity_y
    normal_x, normal_y = (hit_x - target_x) / radius_ball, (hit_y - target_y) / radius_ball
    return hit_x, hit_y, normal_x, normal_y, transverse / radius_ball


def third_tangency_dual(source: Any, second: str, candidate: str, t_value: arb, p_value: arb) -> Dual:
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
    candidate_x, candidate_y = dual_center(candidate)
    dx, dy = candidate_x - hit2_x, candidate_y - hit2_y
    transverse = -outgoing2_y * dx + outgoing2_x * dy
    radius = Q(9, 25) if candidate[0] == "G" else Q(4, 25)
    return aq(radius * radius) - transverse * transverse


def root_enclosure(
    source: Any,
    second: str,
    candidate: str,
    root_axis: str,
    parameter: Q,
    lower: Q,
    upper: Q,
) -> arb | None:
    root = interval(lower, upper)
    parameter_ball = aq(parameter)
    for _step in range(ROOT_NEWTON_STEPS):
        center = root.mid()
        if root_axis == "p":
            point = third_tangency_dual(source, second, candidate, parameter_ball, center)
            full = third_tangency_dual(source, second, candidate, parameter_ball, root)
            derivative = full.gradient[1]
        else:
            point = third_tangency_dual(source, second, candidate, center, parameter_ball)
            full = third_tangency_dual(source, second, candidate, root, parameter_ball)
            derivative = full.gradient[0]
        if strict_sign(derivative) == 0:
            return None
        try:
            root = root.intersection(center - point.value / derivative)
        except Exception:
            return None
    return root


def interval_difference_sign(left: arb, right: arb) -> int:
    return strict_sign(left - right)


def graph_data(
    source: Any,
    second: str,
    candidate: str,
    root_axis: str,
    box: tuple[Q, Q, Q, Q],
) -> dict[str, Any] | None:
    t0, t1, p0, p1 = box
    full = third_tangency_dual(source, second, candidate, interval(t0, t1), interval(p0, p1))
    if root_axis == "p":
        derivative = full.gradient[1]
        lower = third_tangency_dual(source, second, candidate, interval(t0, t1), aq(p0)).value
        upper = third_tangency_dual(source, second, candidate, interval(t0, t1), aq(p1)).value
        slope = -full.gradient[0] / derivative
    else:
        derivative = full.gradient[0]
        lower = third_tangency_dual(source, second, candidate, aq(t0), interval(p0, p1)).value
        upper = third_tangency_dual(source, second, candidate, aq(t1), interval(p0, p1)).value
        slope = -full.gradient[1] / derivative
    derivative_sign = strict_sign(derivative)
    lower_sign, upper_sign = strict_sign(lower), strict_sign(upper)
    if derivative_sign == 0 or lower_sign * upper_sign != -1:
        return None
    return {"root_derivative_sign": derivative_sign, "graph_slope": slope}


def graph_test(
    source: Any,
    second: str,
    left_candidate: str,
    right_candidate: str,
    root_axis: str,
    left_box: tuple[Q, Q, Q, Q],
    right_box: tuple[Q, Q, Q, Q],
    parameter_interval: tuple[Q, Q],
) -> dict[str, Any] | None:
    if root_axis == "p":
        left_box = parameter_interval[0], parameter_interval[1], left_box[2], left_box[3]
        right_box = parameter_interval[0], parameter_interval[1], right_box[2], right_box[3]
    else:
        left_box = left_box[0], left_box[1], parameter_interval[0], parameter_interval[1]
        right_box = right_box[0], right_box[1], parameter_interval[0], parameter_interval[1]
    left = graph_data(source, second, left_candidate, root_axis, left_box)
    right = graph_data(source, second, right_candidate, root_axis, right_box)
    if left is None or right is None:
        return None
    slope_difference_sign = strict_sign(left["graph_slope"] - right["graph_slope"])
    parameter_lower, parameter_upper = parameter_interval
    left_root_lower, left_root_upper = (left_box[2], left_box[3]) if root_axis == "p" else (left_box[0], left_box[1])
    right_root_lower, right_root_upper = (right_box[2], right_box[3]) if root_axis == "p" else (right_box[0], right_box[1])
    left_lower = root_enclosure(source, second, left_candidate, root_axis, parameter_lower, left_root_lower, left_root_upper)
    right_lower = root_enclosure(source, second, right_candidate, root_axis, parameter_lower, right_root_lower, right_root_upper)
    left_upper = root_enclosure(source, second, left_candidate, root_axis, parameter_upper, left_root_lower, left_root_upper)
    right_upper = root_enclosure(source, second, right_candidate, root_axis, parameter_upper, right_root_lower, right_root_upper)
    if None in (left_lower, right_lower, left_upper, right_upper):
        return {"status": "SUBDIVIDE_PARAMETER", "root_axis": root_axis}
    lower_sign = interval_difference_sign(left_lower, right_lower)
    upper_sign = interval_difference_sign(left_upper, right_upper)
    if slope_difference_sign and lower_sign and upper_sign:
        if lower_sign == upper_sign:
            return {
                "status": "CERTIFIED_DISJOINT_GRAPH_ORDER",
                "root_axis": root_axis,
                "slope_difference_sign": slope_difference_sign,
                "endpoint_difference_signs": [lower_sign, upper_sign],
            }
        return {
            "status": "CERTIFIED_UNIQUE_TRANSVERSE_INTERSECTION",
            "root_axis": root_axis,
            "slope_difference_sign": slope_difference_sign,
            "endpoint_difference_signs": [lower_sign, upper_sign],
            "parameter_interval": [str(parameter_lower), str(parameter_upper)],
        }
    return {"status": "SUBDIVIDE_PARAMETER", "root_axis": root_axis}


def split_parameter(parameter_interval: tuple[Q, Q]) -> tuple[tuple[Q, Q], tuple[Q, Q]]:
    lower, upper = parameter_interval
    middle = (lower + upper) / 2
    return (lower, middle), (middle, upper)


def resolve_box(
    source: Any,
    second: str,
    left_candidate: str,
    right_candidate: str,
    left_box: tuple[Q, Q, Q, Q],
    right_box: tuple[Q, Q, Q, Q],
    overlap_box: tuple[Q, Q, Q, Q],
) -> dict[str, Any]:
    if overlap_box[0] == overlap_box[1] or overlap_box[2] == overlap_box[3]:
        return {"status": "DEGENERATE_INTERFACE_BOX", "tests": 0, "maximum_depth": 0, "intersections": []}
    tests = 0
    maximum_depth = 0
    intersections = []
    unresolved = []
    initial_outcomes = []
    for root_axis in ("p", "t"):
        parameter_interval = (overlap_box[0], overlap_box[1]) if root_axis == "p" else (overlap_box[2], overlap_box[3])
        try:
            outcome = graph_test(
                source, second, left_candidate, right_candidate, root_axis,
                left_box, right_box, parameter_interval,
            )
        except Exception:
            outcome = None
        if outcome is not None:
            initial_outcomes.append((root_axis, parameter_interval, outcome))
    terminal = next((item for item in initial_outcomes if item[2]["status"].startswith("CERTIFIED_")), None)
    if terminal is not None:
        outcome = terminal[2]
        if outcome["status"] == "CERTIFIED_UNIQUE_TRANSVERSE_INTERSECTION":
            intersections.append({**outcome, "overlap_box": list(map(str, overlap_box)), "depth": 0})
            status = "CERTIFIED_INTERSECTING"
        else:
            status = "CERTIFIED_DISJOINT"
        return {"status": status, "tests": 1, "maximum_depth": 0, "intersections": intersections, "unresolved_count": 0, "unresolved_sha256": digest([])}
    if not initial_outcomes:
        return {"status": "UNRESOLVED_GRAPH_DIFFERENCE", "tests": 1, "maximum_depth": 0, "intersections": [], "unresolved_count": 1, "unresolved_sha256": digest([list(map(str, overlap_box))])}
    root_axis, initial_parameter, _outcome = initial_outcomes[0]
    stack = [(initial_parameter, 0)]
    while stack:
        parameter_interval, depth = stack.pop()
        maximum_depth = max(maximum_depth, depth)
        tests += 1
        try:
            outcome = graph_test(
                source, second, left_candidate, right_candidate, root_axis,
                left_box, right_box, parameter_interval,
            )
        except Exception:
            outcome = None
        if outcome is not None and outcome["status"].startswith("CERTIFIED_"):
            if outcome["status"] == "CERTIFIED_UNIQUE_TRANSVERSE_INTERSECTION":
                intersections.append({**outcome, "overlap_box": list(map(str, overlap_box)), "depth": depth})
            continue
        if depth == MAXIMUM_PARAMETER_DEPTH or outcome is None:
            unresolved.append([str(parameter_interval[0]), str(parameter_interval[1])])
            continue
        first, second_interval = split_parameter(parameter_interval)
        stack.extend(((second_interval, depth + 1), (first, depth + 1)))
    if unresolved:
        status = "UNRESOLVED_GRAPH_DIFFERENCE"
    elif intersections:
        status = "CERTIFIED_INTERSECTING"
    else:
        status = "CERTIFIED_DISJOINT"
    return {
        "status": status,
        "tests": tests,
        "maximum_depth": maximum_depth,
        "intersections": intersections,
        "unresolved_count": len(unresolved),
        "unresolved_sha256": digest(sorted(unresolved)),
    }


def process_pair(row: dict[str, Any]) -> dict[str, Any]:
    left_id = row["left_physical_root_component_id"]
    right_id = row["right_physical_root_component_id"]
    left, right = WORK_METADATA[left_id], WORK_METADATA[right_id]
    source = WORK_CORES[left["source_core_index"]]
    second = left["second_selected_target_id"]
    statuses = Counter()
    tests = 0
    maximum_depth = 0
    intersections = []
    unresolved = 0
    for geometry in row["residual_graph_geometry_rows"]:
        result = resolve_box(
            source, second, left["third_candidate_id"], right["third_candidate_id"],
            tuple(map(Q, geometry["left_graph_box"])),
            tuple(map(Q, geometry["right_graph_box"])),
            tuple(map(Q, geometry["overlap_box"])),
        )
        statuses[result["status"]] += 1
        tests += result["tests"]
        maximum_depth = max(maximum_depth, result["maximum_depth"])
        unresolved += result.get("unresolved_count", 0)
        intersections.extend(result["intersections"])
    intersections.sort(key=lambda item: item["box"])
    return {
        "left_physical_root_component_id": left_id,
        "right_physical_root_component_id": right_id,
        "input_residual_box_count": len(row["residual_graph_geometry_rows"]),
        "status_histogram": dict(sorted(statuses.items())),
        "interval_graph_test_count": tests,
        "maximum_parameter_depth": maximum_depth,
        "raw_certified_intersection_box_count": len(intersections),
        "intersection_rows_sha256": digest(intersections),
        "unresolved_leaf_count": unresolved,
    }


def build(workers: int = 24, pair_limit: int | None = None) -> dict[str, Any]:
    prefilter = json.loads(PREFILTER.read_text())["result"]
    rows = [row for row in prefilter["pair_rows"] if row["residual_graph_geometry_count"]]
    if pair_limit is not None:
        rows = rows[:pair_limit]
    components = json.loads(JOINS.read_text())["result"]["component_rows"]
    metadata = {row["physical_root_component_id"]: row for row in components}
    context = mp.get_context("fork")
    with context.Pool(workers, initializer=init_worker, initargs=(core_cert.physical_cores(), metadata)) as pool:
        pair_rows = pool.map(process_pair, rows)
    pair_rows.sort(key=lambda row: (row["left_physical_root_component_id"], row["right_physical_root_component_id"]))
    status_histogram = Counter()
    for row in pair_rows:
        status_histogram.update(row["status_histogram"])
    result = {
        "input_component_pair_count": len(pair_rows),
        "input_residual_box_count": sum(row["input_residual_box_count"] for row in pair_rows),
        "box_status_histogram": dict(sorted(status_histogram.items())),
        "interval_graph_test_count": sum(row["interval_graph_test_count"] for row in pair_rows),
        "raw_certified_intersection_box_count": sum(row["raw_certified_intersection_box_count"] for row in pair_rows),
        "unresolved_leaf_count": sum(row["unresolved_leaf_count"] for row in pair_rows),
        "maximum_parameter_depth": max(row["maximum_parameter_depth"] for row in pair_rows),
        "pair_limit": pair_limit,
        "pair_rows": pair_rows,
        "pair_rows_sha256": digest(pair_rows),
        "strict_scope": "one-dimensional graph-difference tests on Round-82 residual boxes; degenerate interface boxes are not resolved here",
    }
    return {"schema": "cm2.round83.graph-difference-resolution.v1", "result": result, "result_sha256": digest(result)}


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
