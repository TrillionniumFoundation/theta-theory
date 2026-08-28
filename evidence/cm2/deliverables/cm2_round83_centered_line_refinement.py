#!/usr/bin/env python3
"""Second-order centered outgoing-line refinement on the 614 hard area boxes."""
from __future__ import annotations

import json
import multiprocessing as mp
import sys
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
from cm2_round76_r2_numeric_fields_generator import Jet, center, collision, normal
from cm2_round79_tangency_intersection_generator import aq, digest, interval, strict_sign
from cm2_round83_common_tangent_line_krawczyk import common_tangent_targets, split


HERE = Path(__file__).resolve().parent
PRIMARY = HERE / "cm2-round83-common-tangent-line-krawczyk-2026-07-22.json"
JOINS = HERE / "cm2-round82-rank3-cross-tube-joins-2026-07-21.json"
MAXIMUM_DEPTH = 12
WORK_CORES: tuple[Any, ...] = ()
WORK_METADATA: dict[str, dict[str, Any]] = {}


def init_worker(cores: tuple[Any, ...], metadata: dict[str, dict[str, Any]]) -> None:
    global WORK_CORES, WORK_METADATA
    WORK_CORES, WORK_METADATA = cores, metadata
    ctx.prec = 384


def outgoing_line_jet(source: Any, second: str, t0: Q, t1: Q, p0: Q, p1: Q) -> tuple[Jet, Jet, Jet]:
    t, p = Jet.variable(interval(t0, t1), 0), Jet.variable(interval(p0, p1), 1)
    parameter = Jet(arb(0))
    normal_x, normal_y = normal(source.chart_id.split(":")[1], t)
    radial = (arb(1) - p * p).sqrt()
    velocity_x, velocity_y = radial * normal_x - p * normal_y, radial * normal_y + p * normal_x
    source_x, source_y = center(f"{source.source}[0,0]", parameter)
    source_radius = Q(9, 25) if source.source == "G" else Q(4, 25)
    point_x, point_y = source_x + aq(source_radius) * normal_x, source_y + aq(source_radius) * normal_y
    first_x, first_y = center(source.target_id, parameter)
    first_radius = Q(9, 25) if source.target_id[0] == "G" else Q(4, 25)
    hit1_x, hit1_y, normal1_x, normal1_y, first_p = collision(
        point_x, point_y, velocity_x, velocity_y, first_x, first_y, first_radius
    )
    radial1 = (arb(1) - first_p * first_p).sqrt()
    outgoing1_x, outgoing1_y = radial1 * normal1_x - first_p * normal1_y, radial1 * normal1_y + first_p * normal1_x
    second_x, second_y = center(second, parameter)
    second_radius = Q(9, 25) if second[0] == "G" else Q(4, 25)
    hit2_x, hit2_y, normal2_x, normal2_y, second_p = collision(
        hit1_x, hit1_y, outgoing1_x, outgoing1_y, second_x, second_y, second_radius
    )
    radial2 = (arb(1) - second_p * second_p).sqrt()
    outgoing2_x, outgoing2_y = radial2 * normal2_x - second_p * normal2_y, radial2 * normal2_y + second_p * normal2_x
    nx, ny = -outgoing2_y, outgoing2_x
    return nx, ny, nx * hit2_x + ny * hit2_y


def centered_line(source: Any, second: str, box: tuple[Q, Q, Q, Q]) -> tuple[tuple[arb, list[arb]], ...]:
    t0, t1, p0, p1 = box
    tc, pc = (t0 + t1) / 2, (p0 + p1) / 2
    full = outgoing_line_jet(source, second, t0, t1, p0, p1)
    point = outgoing_line_jet(source, second, tc, tc, pc, pc)
    delta = interval(t0 - tc, t1 - tc), interval(p0 - pc, p1 - pc)
    output = []
    for full_coordinate, point_coordinate in zip(full, point):
        value = point_coordinate.value
        for axis in range(2):
            value += point_coordinate.gradient[axis] * delta[axis]
        for left in range(2):
            for right in range(2):
                value += arb("0.5") * full_coordinate.hessian[left][right] * delta[left] * delta[right]
        gradient = []
        for axis in range(2):
            entry = point_coordinate.gradient[axis]
            for other in range(2):
                entry += full_coordinate.hessian[axis][other] * delta[other]
            gradient.append(entry)
        output.append((value, gradient))
    return tuple(output)


def target_excluded(line: tuple[tuple[arb, list[arb]], ...], target: dict[str, Any]) -> bool:
    return strict_sign(line[0][0] - target["nx"]) != 0 or strict_sign(line[1][0] - target["ny"]) != 0 or strict_sign(line[2][0] - target["h"]) != 0


def krawczyk(source: Any, second: str, target: dict[str, Any], box: tuple[Q, Q, Q, Q]) -> bool:
    t0, t1, p0, p1 = box
    tc, pc = (t0 + t1) / 2, (p0 + p1) / 2
    full = centered_line(source, second, box)
    point_jets = outgoing_line_jet(source, second, tc, tc, pc, pc)
    options = [(0, target["nx"]), (1, target["ny"])]
    best = None
    for coordinate, target_normal in options:
        a = float(point_jets[coordinate].gradient[0].mid())
        b = float(point_jets[coordinate].gradient[1].mid())
        c = float(point_jets[2].gradient[0].mid())
        d = float(point_jets[2].gradient[1].mid())
        determinant = a * d - b * c
        if determinant != 0 and (best is None or abs(determinant) > abs(best[0])):
            best = determinant, coordinate, target_normal, a, b, c, d
    if best is None:
        return False
    determinant, coordinate, target_normal, a, b, c, d = best
    inverse = (
        (arb(str(d / determinant)), arb(str(-b / determinant))),
        (arb(str(-c / determinant)), arb(str(a / determinant))),
    )
    functions = point_jets[coordinate].value - target_normal, point_jets[2].value - target["h"]
    jacobian = full[coordinate][1], full[2][1]
    displacement = interval(t0 - tc, t1 - tc), interval(p0 - pc, p1 - pc)
    values = []
    for output_axis in range(2):
        value = aq((tc, pc)[output_axis])
        value -= sum(inverse[output_axis][row] * functions[row] for row in range(2))
        for input_axis in range(2):
            coefficient = arb(1 if output_axis == input_axis else 0)
            coefficient -= sum(inverse[output_axis][row] * jacobian[row][input_axis] for row in range(2))
            value += coefficient * displacement[input_axis]
        values.append(value)
    if not (
        bool(values[0] > aq(t0)) and bool(values[0] < aq(t1))
        and bool(values[1] > aq(p0)) and bool(values[1] < aq(p1))
    ):
        return False
    determinant_interval = jacobian[0][0] * jacobian[1][1] - jacobian[0][1] * jacobian[1][0]
    return strict_sign(determinant_interval) != 0


def interval_newton_excluded(source: Any, second: str, target: dict[str, Any], box: tuple[Q, Q, Q, Q]) -> bool:
    t0, t1, p0, p1 = box
    tc, pc = (t0 + t1) / 2, (p0 + p1) / 2
    full = centered_line(source, second, box)
    point = outgoing_line_jet(source, second, tc, tc, pc, pc)
    for coordinate, target_normal in ((0, target["nx"]), (1, target["ny"])):
        a, b = full[coordinate][1]
        c, d = full[2][1]
        determinant = a * d - b * c
        if strict_sign(determinant) == 0:
            continue
        first = point[coordinate].value - target_normal
        second_value = point[2].value - target["h"]
        newton_t = aq(tc) - (d * first - b * second_value) / determinant
        newton_p = aq(pc) - (-c * first + a * second_value) / determinant
        if bool(newton_t < aq(t0)) or bool(newton_t > aq(t1)) or bool(newton_p < aq(p0)) or bool(newton_p > aq(p1)):
            return True
    return False


def resolve(source: Any, second: str, targets: list[dict[str, Any]], initial: tuple[Q, Q, Q, Q]) -> dict[str, Any]:
    stack = [(initial, 0, tuple(range(len(targets))))]
    roots = 0
    unresolved = []
    tests = 0
    maximum_depth = 0
    while stack:
        box, depth, active = stack.pop()
        maximum_depth = max(maximum_depth, depth)
        line = centered_line(source, second, box)
        tests += 1
        survivors = tuple(index for index in active if not target_excluded(line, targets[index]))
        if not survivors:
            continue
        survivors = tuple(index for index in survivors if not interval_newton_excluded(source, second, targets[index], box))
        if not survivors:
            continue
        certified = sum(krawczyk(source, second, targets[index], box) for index in survivors)
        if certified:
            roots += certified
            continue
        if depth == MAXIMUM_DEPTH:
            unresolved.append(list(map(str, box)))
            continue
        first, second_box = split(source, box)
        stack.extend(((second_box, depth + 1, survivors), (first, depth + 1, survivors)))
    return {
        "tests": tests,
        "raw_root_count": roots,
        "unresolved_leaf_count": len(unresolved),
        "unresolved_area": str(sum((Q(box[1]) - Q(box[0])) * (Q(box[3]) - Q(box[2])) for box in unresolved)),
        "unresolved_sha256": digest(sorted(unresolved)),
        "maximum_depth": maximum_depth,
    }


def process_pair(row: dict[str, Any]) -> dict[str, Any]:
    left_id, right_id = row["left_physical_root_component_id"], row["right_physical_root_component_id"]
    left, right = WORK_METADATA[left_id], WORK_METADATA[right_id]
    source = WORK_CORES[left["source_core_index"]]
    targets = common_tangent_targets(left["third_candidate_id"], right["third_candidate_id"])
    tests = roots = unresolved = 0
    input_area = Q(0)
    unresolved_area = Q(0)
    maximum_depth = 0
    for raw_box in row["unresolved_initial_boxes"]:
        parsed_box = tuple(map(Q, raw_box))
        input_area += (parsed_box[1] - parsed_box[0]) * (parsed_box[3] - parsed_box[2])
        result = resolve(source, left["second_selected_target_id"], targets, parsed_box)
        tests += result["tests"]
        roots += result["raw_root_count"]
        unresolved += result["unresolved_leaf_count"]
        unresolved_area += Q(result["unresolved_area"])
        maximum_depth = max(maximum_depth, result["maximum_depth"])
    return {
        "left_physical_root_component_id": left_id,
        "right_physical_root_component_id": right_id,
        "input_hard_box_count": len(row["unresolved_initial_boxes"]),
        "centered_line_box_test_count": tests,
        "raw_krawczyk_root_count": roots,
        "unresolved_leaf_count": unresolved,
        "input_hard_box_area": str(input_area),
        "unresolved_area": str(unresolved_area),
        "maximum_depth": maximum_depth,
    }


def build(workers: int = 24) -> dict[str, Any]:
    rows = [row for row in json.loads(PRIMARY.read_text())["result"]["pair_rows"] if row["unresolved_initial_box_count"]]
    components = json.loads(JOINS.read_text())["result"]["component_rows"]
    metadata = {row["physical_root_component_id"]: row for row in components}
    context = mp.get_context("fork")
    with context.Pool(workers, initializer=init_worker, initargs=(core_cert.physical_cores(), metadata)) as pool:
        pair_rows = pool.map(process_pair, rows)
    pair_rows.sort(key=lambda row: (row["left_physical_root_component_id"], row["right_physical_root_component_id"]))
    result = {
        "input_hard_component_pair_count": len(pair_rows),
        "input_hard_box_count": sum(row["input_hard_box_count"] for row in pair_rows),
        "centered_line_box_test_count": sum(row["centered_line_box_test_count"] for row in pair_rows),
        "raw_krawczyk_root_count": sum(row["raw_krawczyk_root_count"] for row in pair_rows),
        "unresolved_leaf_count": sum(row["unresolved_leaf_count"] for row in pair_rows),
        "input_hard_box_area": str(sum(Q(row["input_hard_box_area"]) for row in pair_rows)),
        "unresolved_area": str(sum(Q(row["unresolved_area"]) for row in pair_rows)),
        "maximum_depth": max(row["maximum_depth"] for row in pair_rows),
        "pair_rows": pair_rows,
        "pair_rows_sha256": digest(pair_rows),
        "strict_scope": "second-order centered outgoing-line refinement on the 614 hard positive-area boxes",
    }
    return {"schema": "cm2.round83.centered-line-refinement.v1", "result": result, "result_sha256": digest(result)}


def main() -> int:
    json.dump(build(), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
