#!/usr/bin/env python3
"""Interval continuation of symmetry-reduced third-collision tangency carriers."""
from __future__ import annotations

import json
import multiprocessing as mp
import re
import sys
from collections import defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as step1
from cm2_round76_r2_numeric_fields_generator import Jet, center, collision, normal
from cm2_round79_tangency_intersection_generator import aq, digest, interval, strict_sign
from cm2_round80_time3_carrier_component_generator import grid_cell


HERE = Path(__file__).resolve().parent
COMPONENTS = HERE / "cm2-round80-time3-carrier-components-2026-07-21.json"
QUOTIENT = HERE / "cm2-round80-time3-dihedral-quotient-2026-07-21.json"
GEOMETRY = HERE / "cm2-round80-time3-carrier-geometry-2026-07-21.json"
GRID = 64
WORK_CORES: tuple[Any, ...] = ()
WORK_COMPONENT_INDEX: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}
WORK_BRANCH_BY_CELL: dict[tuple[int, str, tuple[int, int]], tuple[str, str]] = {}


def candidate_from_carrier(carrier: str) -> str:
    match = re.fullmatch(r"THIRD_CANDIDATE:(.+):unresolved_discriminant", carrier)
    if match is None:
        raise RuntimeError("not a third tangency carrier")
    return match.group(1)


def third_tangency_jet(
    source: Any,
    second_target: str,
    candidate: str,
    t0: Q,
    t1: Q,
    p0: Q,
    p1: Q,
) -> Jet:
    t = Jet.variable(interval(t0, t1), 0)
    p = Jet.variable(interval(p0, p1), 1)
    parameter = Jet(arb(0))
    normal_x, normal_y = normal(source.chart_id.split(":")[1], t)
    radial = (arb(1) - p * p).sqrt()
    velocity_x = radial * normal_x - p * normal_y
    velocity_y = radial * normal_y + p * normal_x
    source_x, source_y = center(f"{source.source}[0,0]", parameter)
    source_radius = Q(9, 25) if source.source == "G" else Q(4, 25)
    point_x = source_x + aq(source_radius) * normal_x
    point_y = source_y + aq(source_radius) * normal_y
    first_x, first_y = center(source.target_id, parameter)
    first_radius = Q(9, 25) if source.target_id[0] == "G" else Q(4, 25)
    hit1_x, hit1_y, normal1_x, normal1_y, first_p = collision(
        point_x, point_y, velocity_x, velocity_y,
        first_x, first_y, first_radius,
    )
    radial1 = (arb(1) - first_p * first_p).sqrt()
    outgoing1_x = radial1 * normal1_x - first_p * normal1_y
    outgoing1_y = radial1 * normal1_y + first_p * normal1_x
    second_x, second_y = center(second_target, parameter)
    second_radius = Q(9, 25) if second_target[0] == "G" else Q(4, 25)
    hit2_x, hit2_y, normal2_x, normal2_y, second_p = collision(
        hit1_x, hit1_y, outgoing1_x, outgoing1_y,
        second_x, second_y, second_radius,
    )
    radial2 = (arb(1) - second_p * second_p).sqrt()
    outgoing2_x = radial2 * normal2_x - second_p * normal2_y
    outgoing2_y = radial2 * normal2_y + second_p * normal2_x
    candidate_x, candidate_y = center(candidate, parameter)
    dx, dy = candidate_x - hit2_x, candidate_y - hit2_y
    transverse = -outgoing2_y * dx + outgoing2_x * dy
    candidate_radius = Q(9, 25) if candidate[0] == "G" else Q(4, 25)
    return aq(candidate_radius * candidate_radius) - transverse * transverse


def coordinate(core: Any, axis: str, index: int) -> Q:
    lower, upper = (core.t0, core.t1) if axis == "t" else (core.p0, core.p1)
    return lower + (upper - lower) * Q(index, GRID)


def certify_box(
    source: Any,
    second_target: str,
    candidate: str,
    root_axis: str,
    root_lower_index: int,
    root_upper_index: int,
    parameter_lower: Q,
    parameter_upper: Q,
    recursion: int = 0,
) -> list[dict[str, Any]] | None:
    root_lower = coordinate(source, root_axis, root_lower_index)
    root_upper = coordinate(source, root_axis, root_upper_index)
    if root_axis == "t":
        full = third_tangency_jet(source, second_target, candidate, root_lower, root_upper, parameter_lower, parameter_upper)
        left = third_tangency_jet(source, second_target, candidate, root_lower, root_lower, parameter_lower, parameter_upper).value
        right = third_tangency_jet(source, second_target, candidate, root_upper, root_upper, parameter_lower, parameter_upper).value
        derivative, parameter_derivative = full.gradient[0], full.gradient[1]
    else:
        full = third_tangency_jet(source, second_target, candidate, parameter_lower, parameter_upper, root_lower, root_upper)
        left = third_tangency_jet(source, second_target, candidate, parameter_lower, parameter_upper, root_lower, root_lower).value
        right = third_tangency_jet(source, second_target, candidate, parameter_lower, parameter_upper, root_upper, root_upper).value
        derivative, parameter_derivative = full.gradient[1], full.gradient[0]
    left_sign, right_sign = strict_sign(left), strict_sign(right)
    derivative_sign, parameter_derivative_sign = strict_sign(derivative), strict_sign(parameter_derivative)
    if left_sign * right_sign == -1 and derivative_sign and parameter_derivative_sign:
        return [{
            "parameter_interval": [str(parameter_lower), str(parameter_upper)],
            "root_interval": [str(root_lower), str(root_upper)],
            "endpoint_signs": [left_sign, right_sign],
            "root_derivative_sign": derivative_sign,
            "parameter_derivative_sign": parameter_derivative_sign,
            "implicit_slope_sign": -derivative_sign * parameter_derivative_sign,
            "subdivision_depth": recursion,
        }]
    if recursion >= 6:
        return None
    middle = (parameter_lower + parameter_upper) / 2
    left_rows = certify_box(
        source, second_target, candidate, root_axis,
        root_lower_index, root_upper_index,
        parameter_lower, middle, recursion + 1,
    )
    if left_rows is None:
        return None
    right_rows = certify_box(
        source, second_target, candidate, root_axis,
        root_lower_index, root_upper_index,
        middle, parameter_upper, recursion + 1,
    )
    if right_rows is None:
        return None
    return left_rows + right_rows


def attempt_orientation(
    source: Any,
    second_target: str,
    candidate: str,
    root_axis: str,
    envelopes: list[list[int]],
) -> dict[str, Any] | None:
    parameter_axis = "p" if root_axis == "t" else "t"
    slabs = []
    for parameter_index, raw_lower, raw_upper, _count in envelopes:
        certified = None
        expansion_used = None
        for expansion in range(1, 17):
            lower_index = max(0, raw_lower - expansion)
            upper_index = min(GRID, raw_upper + expansion)
            if lower_index == upper_index:
                continue
            try:
                rows = certify_box(
                    source, second_target, candidate, root_axis,
                    lower_index, upper_index,
                    coordinate(source, parameter_axis, parameter_index),
                    coordinate(source, parameter_axis, parameter_index + 1),
                )
            except Exception:
                rows = None
            if rows is not None:
                certified, expansion_used = rows, expansion
                break
        if certified is None:
            return None
        slabs.extend({
            "parameter_grid_index": parameter_index,
            "root_grid_envelope": [raw_lower, raw_upper],
            "root_grid_expansion": expansion_used,
            **row,
        } for row in certified)
    root_signs = {row["root_derivative_sign"] for row in slabs}
    parameter_signs = {row["parameter_derivative_sign"] for row in slabs}
    slope_signs = {row["implicit_slope_sign"] for row in slabs}
    parameter_indices = sorted({row["parameter_grid_index"] for row in slabs})
    if parameter_indices != list(range(parameter_indices[0], parameter_indices[-1] + 1)):
        return None
    return {
        "root_axis": root_axis,
        "parameter_axis": parameter_axis,
        "certified_slab_count": len(slabs),
        "maximum_parameter_subdivision_depth": max(row["subdivision_depth"] for row in slabs),
        "maximum_root_grid_expansion": max(row["root_grid_expansion"] for row in slabs),
        "global_root_derivative_sign": next(iter(root_signs)) if len(root_signs) == 1 else None,
        "global_parameter_derivative_sign": next(iter(parameter_signs)) if len(parameter_signs) == 1 else None,
        "global_implicit_slope_sign": next(iter(slope_signs)) if len(slope_signs) == 1 else None,
        "piecewise_root_derivative_sign_histogram": {str(sign): sum(row["root_derivative_sign"] == sign for row in slabs) for sign in sorted(root_signs)},
        "piecewise_parameter_derivative_sign_histogram": {str(sign): sum(row["parameter_derivative_sign"] == sign for row in slabs) for sign in sorted(parameter_signs)},
        "piecewise_implicit_slope_sign_histogram": {str(sign): sum(row["implicit_slope_sign"] == sign for row in slabs) for sign in sorted(slope_signs)},
        "connected_parameter_grid_span_half_open": [parameter_indices[0], parameter_indices[-1] + 1],
        "slabs": slabs,
        "slabs_sha256": digest(slabs),
    }


def process_orbit(orbit: dict[str, Any]) -> dict[str, Any] | None:
    identifier = orbit["representative_component_id"]
    pair, component = WORK_COMPONENT_INDEX[identifier]
    source_index = pair["source_core_index"]
    source = WORK_CORES[source_index]
    branches = {
        WORK_BRANCH_BY_CELL[(source_index, pair["carrier"], tuple(cell))]
        for cell in component["cell_set"]
    }
    if len(branches) != 1:
        raise RuntimeError(f"nonunique second branch {identifier}")
    second_target, outgoing_chart = next(iter(branches))
    candidate = candidate_from_carrier(pair["carrier"])
    orientation = attempt_orientation(
        source, second_target, candidate, "t", component["p_slice_envelopes"]
    )
    if orientation is None:
        orientation = attempt_orientation(
            source, second_target, candidate, "p", component["t_slice_envelopes"]
        )
    if orientation is None:
        return None
    row = {
        "representative_component_id": identifier,
        "orbit_rank": orbit["orbit_rank"],
        "orbit_size": orbit["orbit_size"],
        "sector_symmetry": orbit["sector_symmetry"],
        "source_core_index": source_index,
        "second_selected_target_id": second_target,
        "second_outgoing_chart": outgoing_chart,
        "third_candidate_id": candidate,
        "tube_cell_count": component["cell_count"],
        **orientation,
    }
    row["physical_curve_id"] = "physical-s0-rank3-tangency:" + digest({
        "component": identifier,
        "second_target": second_target,
        "candidate": candidate,
    })
    return row


def build() -> dict[str, Any]:
    global WORK_CORES, WORK_COMPONENT_INDEX, WORK_BRANCH_BY_CELL
    ctx.prec = 384
    cores = core_cert.physical_cores()
    components_document = json.loads(COMPONENTS.read_text())["result"]
    quotient = json.loads(QUOTIENT.read_text())["result"]
    geometry = json.loads(GEOMETRY.read_text())["result"]["seed_rows"]
    branch_by_cell: dict[tuple[int, str, tuple[int, int]], tuple[str, str]] = {}
    for row in geometry:
        if not row["carrier"].startswith("THIRD_CANDIDATE:"):
            continue
        branch_by_cell[(row["source_core_index"], row["carrier"], grid_cell(row["dyadic_path"]))] = (
            row["second_selected_target_id"], row["second_outgoing_chart"],
        )
    component_index = {}
    for pair in components_document["pair_rows"]:
        for component in pair["components"]:
            identifier = f"rank3-carrier-component:{pair['source_core_index']}:{pair['carrier']}:{component['connected_rank']}"
            component_index[identifier] = (pair, component)
    WORK_CORES = cores
    WORK_COMPONENT_INDEX = component_index
    WORK_BRANCH_BY_CELL = branch_by_cell
    context = mp.get_context("fork")
    with context.Pool(16) as pool:
        processed = pool.map(process_orbit, quotient["orbit_rows"])
    rows = [row for row in processed if row is not None]
    failures = [
        orbit["representative_component_id"]
        for orbit, row in zip(quotient["orbit_rows"], processed)
        if row is None
    ]
    rows.sort(key=lambda row: row["orbit_rank"])
    result = {
        "fixed_parameter": "s=0",
        "symmetry_representative_count": len(quotient["orbit_rows"]),
        "certified_representative_curve_count": len(rows),
        "failed_representative_component_count": len(failures),
        "failed_representative_component_ids": failures,
        "symmetry_expanded_certified_curve_count": sum(row["orbit_size"] for row in rows),
        "certified_slab_count": sum(row["certified_slab_count"] for row in rows),
        "curve_rows": rows,
        "curve_rows_sha256": digest(rows),
        "strict_scope": "symmetry-reduced physical equality-curve continuation; failed tube components are not classified as false or physical",
    }
    return {"schema": "cm2.round80.time3-tangency-curves.v1", "result": result, "result_sha256": digest(result)}


def main() -> int:
    json.dump(build(), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
