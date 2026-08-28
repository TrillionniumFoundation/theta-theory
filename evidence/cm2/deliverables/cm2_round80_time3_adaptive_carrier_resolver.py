#!/usr/bin/env python3
"""Adaptive strict-open/root-slab resolution of difficult rank-three carrier tubes."""
from __future__ import annotations

import json
import multiprocessing as mp
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate25_physical_return_core_registry_cert as core_cert
from cm2_round79_tangency_intersection_generator import aq, digest, interval, strict_sign
from cm2_round80_time3_tangency_curve_generator import third_tangency_jet, candidate_from_carrier


HERE = Path(__file__).resolve().parent
COMPONENTS = HERE / "cm2-round80-time3-carrier-components-2026-07-21.json"
QUOTIENT = HERE / "cm2-round80-time3-dihedral-quotient-2026-07-21.json"
GEOMETRY = HERE / "cm2-round80-time3-carrier-geometry-2026-07-21.json"
CURVES = HERE / "cm2-round80-time3-tangency-curves-2026-07-21.json"
GRID = 64
MAXIMUM_DEPTH = 10
WORK_CORES: tuple[Any, ...] = ()
WORK_COMPONENTS: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}
WORK_BRANCHES: dict[tuple[int, str, tuple[int, int]], tuple[str, str]] = {}
WORK_ORBITS: dict[str, dict[str, Any]] = {}


def centered_taylor(
    source: Any,
    second_target: str,
    candidate: str,
    box: tuple[Q, Q, Q, Q],
) -> tuple[Any, tuple[Any, Any]]:
    t0, t1, p0, p1 = box
    tc, pc = (t0 + t1) / 2, (p0 + p1) / 2
    point = third_tangency_jet(source, second_target, candidate, tc, tc, pc, pc)
    full = third_tangency_jet(source, second_target, candidate, *box)
    displacement = (interval(t0 - tc, t1 - tc), interval(p0 - pc, p1 - pc))
    value = point.value
    for index in range(2):
        value += point.gradient[index] * displacement[index]
    for left in range(2):
        for right in range(2):
            value += full.hessian[left][right] * displacement[left] * displacement[right] / 2
    gradients = []
    for left in range(2):
        gradient = point.gradient[left]
        for right in range(2):
            gradient += full.hessian[left][right] * displacement[right]
        gradients.append(gradient)
    return value, (gradients[0], gradients[1])


def coordinate(core: Any, axis: str, index: int) -> Q:
    lower, upper = (core.t0, core.t1) if axis == "t" else (core.p0, core.p1)
    return lower + (upper - lower) * Q(index, GRID)


def root_slab(
    source: Any,
    second_target: str,
    candidate: str,
    box: tuple[Q, Q, Q, Q],
) -> dict[str, Any] | None:
    t0, t1, p0, p1 = box
    full = third_tangency_jet(source, second_target, candidate, *box)
    _centered_value, centered_gradient = centered_taylor(source, second_target, candidate, box)
    dt_sign, dp_sign = strict_sign(centered_gradient[0]), strict_sign(centered_gradient[1])
    if dt_sign:
        left = centered_taylor(source, second_target, candidate, (t0, t0, p0, p1))[0]
        right = centered_taylor(source, second_target, candidate, (t1, t1, p0, p1))[0]
        endpoint_signs = [strict_sign(left), strict_sign(right)]
        if endpoint_signs[0] * endpoint_signs[1] == -1:
            return {
                "root_axis": "t",
                "parameter_axis": "p",
                "box": list(map(str, box)),
                "root_derivative_sign": dt_sign,
                "parameter_derivative_sign": dp_sign,
                "endpoint_signs": endpoint_signs,
            }
    if dp_sign:
        lower = centered_taylor(source, second_target, candidate, (t0, t1, p0, p0))[0]
        upper = centered_taylor(source, second_target, candidate, (t0, t1, p1, p1))[0]
        endpoint_signs = [strict_sign(lower), strict_sign(upper)]
        if endpoint_signs[0] * endpoint_signs[1] == -1:
            return {
                "root_axis": "p",
                "parameter_axis": "t",
                "box": list(map(str, box)),
                "root_derivative_sign": dp_sign,
                "parameter_derivative_sign": dt_sign,
                "endpoint_signs": endpoint_signs,
            }
    if dt_sign:
        middle = (t0 + t1) / 2
        center_slice = third_tangency_jet(source, second_target, candidate, middle, middle, p0, p1)
        newton = aq(middle) - center_slice.value / centered_gradient[0]
        if bool(newton > aq(t0)) and bool(newton < aq(t1)):
            return {
                "root_axis": "t",
                "parameter_axis": "p",
                "box": list(map(str, box)),
                "root_derivative_sign": dt_sign,
                "parameter_derivative_sign": dp_sign,
                "parameterized_interval_newton_strict_interior": True,
            }
    if dp_sign:
        middle = (p0 + p1) / 2
        center_slice = third_tangency_jet(source, second_target, candidate, t0, t1, middle, middle)
        newton = aq(middle) - center_slice.value / centered_gradient[1]
        if bool(newton > aq(p0)) and bool(newton < aq(p1)):
            return {
                "root_axis": "p",
                "parameter_axis": "t",
                "box": list(map(str, box)),
                "root_derivative_sign": dp_sign,
                "parameter_derivative_sign": dt_sign,
                "parameterized_interval_newton_strict_interior": True,
            }
    if dt_sign and dp_sign:
        minimum_t, maximum_t = (t0, t1) if dt_sign > 0 else (t1, t0)
        minimum_p, maximum_p = (p0, p1) if dp_sign > 0 else (p1, p0)
        minimum = third_tangency_jet(source, second_target, candidate, minimum_t, minimum_t, minimum_p, minimum_p).value
        maximum = third_tangency_jet(source, second_target, candidate, maximum_t, maximum_t, maximum_p, maximum_p).value
        if strict_sign(minimum) == -1 and strict_sign(maximum) == 1:
            return {
                "root_axis": "corner_monotone_patch",
                "parameter_axis": "local",
                "box": list(map(str, box)),
                "root_derivative_signs": [dt_sign, dp_sign],
                "opposite_extreme_corner_signs": [-1, 1],
                "unique_connected_root_patch_from_strict_coordinate_monotonicity": True,
            }
    return None


def monotone_corner_sign(
    source: Any,
    second_target: str,
    candidate: str,
    box: tuple[Q, Q, Q, Q],
) -> int:
    t0, t1, p0, p1 = box
    _value, gradient = centered_taylor(source, second_target, candidate, box)
    dt_sign, dp_sign = strict_sign(gradient[0]), strict_sign(gradient[1])
    if not dt_sign or not dp_sign:
        return 0
    minimum_t, maximum_t = (t0, t1) if dt_sign > 0 else (t1, t0)
    minimum_p, maximum_p = (p0, p1) if dp_sign > 0 else (p1, p0)
    minimum = third_tangency_jet(source, second_target, candidate, minimum_t, minimum_t, minimum_p, minimum_p).value
    maximum = third_tangency_jet(source, second_target, candidate, maximum_t, maximum_t, maximum_p, maximum_p).value
    if strict_sign(minimum) == 1:
        return 1
    if strict_sign(maximum) == -1:
        return -1
    return 0


def split(source: Any, box: tuple[Q, Q, Q, Q]) -> tuple[tuple[Q, Q, Q, Q], tuple[Q, Q, Q, Q]]:
    t0, t1, p0, p1 = box
    if (t1 - t0) / (source.t1 - source.t0) >= (p1 - p0) / (source.p1 - source.p0):
        middle = (t0 + t1) / 2
        return (t0, middle, p0, p1), (middle, t1, p0, p1)
    middle = (p0 + p1) / 2
    return (t0, t1, p0, middle), (t0, t1, middle, p1)


def process_component(identifier: str) -> dict[str, Any]:
    pair, component = WORK_COMPONENTS[identifier]
    source_index = pair["source_core_index"]
    source = WORK_CORES[source_index]
    branches = {
        WORK_BRANCHES[(source_index, pair["carrier"], tuple(cell))]
        for cell in component["cell_set"]
    }
    if len(branches) != 1:
        raise RuntimeError("branch uniqueness")
    second_target, outgoing_chart = next(iter(branches))
    candidate = candidate_from_carrier(pair["carrier"])
    stack = []
    for i, j in map(tuple, component["cell_set"]):
        stack.append(((
            coordinate(source, "t", i), coordinate(source, "t", i + 1),
            coordinate(source, "p", j), coordinate(source, "p", j + 1),
        ), 0))
    excluded = []
    roots = []
    unresolved = []
    tests = 0
    maximum_depth = 0
    while stack:
        box, depth = stack.pop()
        maximum_depth = max(maximum_depth, depth)
        try:
            function = third_tangency_jet(source, second_target, candidate, *box)
            tests += 1
            function_sign = strict_sign(function.value)
            if function_sign == 0:
                function_sign = strict_sign(centered_taylor(source, second_target, candidate, box)[0])
            if function_sign == 0:
                function_sign = monotone_corner_sign(source, second_target, candidate, box)
        except Exception:
            function_sign = 0
        if function_sign:
            excluded.append({"box": list(map(str, box)), "function_sign": function_sign, "depth": depth})
            continue
        try:
            slab = root_slab(source, second_target, candidate, box)
        except Exception:
            slab = None
        if slab is not None:
            roots.append({**slab, "depth": depth})
            continue
        if depth == MAXIMUM_DEPTH:
            unresolved.append(list(map(str, box)))
            continue
        left, right = split(source, box)
        stack.extend(((right, depth + 1), (left, depth + 1)))
    roots.sort(key=lambda row: row["box"])
    excluded.sort(key=lambda row: row["box"])
    unresolved.sort()
    orbit = WORK_ORBITS[identifier]
    return {
        "representative_component_id": identifier,
        "orbit_rank": orbit["orbit_rank"],
        "orbit_size": orbit["orbit_size"],
        "sector_symmetry": orbit["sector_symmetry"],
        "source_core_index": source_index,
        "second_selected_target_id": second_target,
        "second_outgoing_chart": outgoing_chart,
        "third_candidate_id": candidate,
        "seed_cell_count": component["cell_count"],
        "interval_box_tests": tests,
        "excluded_open_leaf_count": len(excluded),
        "unique_root_slab_count": len(roots),
        "unresolved_leaf_count": len(unresolved),
        "maximum_depth": maximum_depth,
        "root_slabs": roots,
        "unresolved_leaves": unresolved,
        "root_slabs_sha256": digest(roots),
        "excluded_leaves_sha256": digest(excluded),
        "unresolved_leaves_sha256": digest(unresolved),
    }


def build() -> dict[str, Any]:
    global WORK_CORES, WORK_COMPONENTS, WORK_BRANCHES, WORK_ORBITS
    WORK_CORES = core_cert.physical_cores()
    component_document = json.loads(COMPONENTS.read_text())["result"]
    WORK_COMPONENTS = {
        f"rank3-carrier-component:{pair['source_core_index']}:{pair['carrier']}:{component['connected_rank']}": (pair, component)
        for pair in component_document["pair_rows"]
        for component in pair["components"]
        if pair["carrier"].startswith("THIRD_CANDIDATE:")
    }
    geometry = json.loads(GEOMETRY.read_text())["result"]["seed_rows"]
    from cm2_round80_time3_carrier_component_generator import grid_cell
    WORK_BRANCHES = {
        (row["source_core_index"], row["carrier"], grid_cell(row["dyadic_path"])):
        (row["second_selected_target_id"], row["second_outgoing_chart"])
        for row in geometry if row["carrier"].startswith("THIRD_CANDIDATE:")
    }
    quotient = json.loads(QUOTIENT.read_text())["result"]
    WORK_ORBITS = {row["representative_component_id"]: row for row in quotient["orbit_rows"]}
    failed = json.loads(CURVES.read_text())["result"]["failed_representative_component_ids"]
    context = mp.get_context("fork")
    with context.Pool(16) as pool:
        rows = pool.map(process_component, failed)
    rows.sort(key=lambda row: row["orbit_rank"])
    result = {
        "input_failed_representative_component_count": len(failed),
        "fully_resolved_representative_component_count": sum(row["unresolved_leaf_count"] == 0 for row in rows),
        "representatives_with_physical_root_slabs": sum(row["unique_root_slab_count"] > 0 for row in rows),
        "representatives_proved_entirely_false_tube": sum(row["unique_root_slab_count"] == 0 and row["unresolved_leaf_count"] == 0 for row in rows),
        "remaining_unresolved_representative_component_count": sum(row["unresolved_leaf_count"] > 0 for row in rows),
        "symmetry_expanded_root_bearing_component_count": sum(row["orbit_size"] for row in rows if row["unique_root_slab_count"] > 0),
        "total_interval_box_tests": sum(row["interval_box_tests"] for row in rows),
        "total_unique_root_slabs": sum(row["unique_root_slab_count"] for row in rows),
        "total_unresolved_leaves": sum(row["unresolved_leaf_count"] for row in rows),
        "global_maximum_depth": max(row["maximum_depth"] for row in rows),
        "component_rows": rows,
        "component_rows_sha256": digest(rows),
    }
    return {"schema": "cm2.round80.time3-adaptive-carrier-resolution.v1", "result": result, "result_sha256": digest(result)}


def main() -> int:
    json.dump(build(), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
