#!/usr/bin/env python3
"""Interval implicit-curve certification for Round-78 time-two tangencies."""
from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as step1
from cm2_round76_r2_numeric_fields_generator import Jet, center, collision, normal


HERE = Path(__file__).resolve().parent
COMPONENTS = HERE / "cm2-round78-carrier-components-2026-07-21.json"
GRID = 1024


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def aq(value: Q | int) -> arb:
    return step1.arbq(Q(value))


def interval(lower: Q, upper: Q) -> arb:
    return core_cert.first_hit.arb_interval(lower, upper)


def parse_candidate(carrier: str) -> str:
    prefix = "SECOND_CANDIDATE:"
    suffix = ":unresolved_discriminant"
    if not carrier.startswith(prefix) or not carrier.endswith(suffix):
        raise RuntimeError("not a tangency carrier")
    return carrier[len(prefix):-len(suffix)]


def tangency_jet(
    source: Any, candidate: str, t0: Q, t1: Q, p0: Q, p1: Q
) -> Jet:
    t = Jet.variable(interval(t0, t1), 0)
    p = Jet.variable(interval(p0, p1), 1)
    parameter = Jet(arb(0))
    normal_x, normal_y = normal(source.chart_id.split(":")[1], t)
    velocity_radial = (arb(1) - p * p).sqrt()
    velocity_x = velocity_radial * normal_x - p * normal_y
    velocity_y = velocity_radial * normal_y + p * normal_x
    source_x, source_y = center(f"{source.source}[0,0]", parameter)
    source_radius = Q(9, 25) if source.source == "G" else Q(4, 25)
    point_x = source_x + aq(source_radius) * normal_x
    point_y = source_y + aq(source_radius) * normal_y
    first_x, first_y = center(source.target_id, parameter)
    first_radius = Q(9, 25) if source.target_id[0] == "G" else Q(4, 25)
    hit_x, hit_y, first_normal_x, first_normal_y, first_p = collision(
        point_x, point_y, velocity_x, velocity_y,
        first_x, first_y, first_radius,
    )
    outgoing_radial = (arb(1) - first_p * first_p).sqrt()
    outgoing_x = outgoing_radial * first_normal_x - first_p * first_normal_y
    outgoing_y = outgoing_radial * first_normal_y + first_p * first_normal_x
    candidate_x, candidate_y = center(candidate, parameter)
    dx, dy = candidate_x - hit_x, candidate_y - hit_y
    transverse = -outgoing_y * dx + outgoing_x * dy
    candidate_radius = Q(9, 25) if candidate[0] == "G" else Q(4, 25)
    return aq(candidate_radius * candidate_radius) - transverse * transverse


def sign(value: arb) -> int:
    if bool(value > 0):
        return 1
    if bool(value < 0):
        return -1
    return 0


def coordinate(core: Any, axis: str, index: int) -> Q:
    lower, upper = (core.t0, core.t1) if axis == "t" else (core.p0, core.p1)
    return lower + (upper - lower) * Q(index, GRID)


def certify_box(
    source: Any,
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
        full = tangency_jet(source, candidate, root_lower, root_upper, parameter_lower, parameter_upper)
        left = tangency_jet(source, candidate, root_lower, root_lower, parameter_lower, parameter_upper).value
        right = tangency_jet(source, candidate, root_upper, root_upper, parameter_lower, parameter_upper).value
        derivative = full.gradient[0]
        parameter_derivative = full.gradient[1]
    else:
        full = tangency_jet(source, candidate, parameter_lower, parameter_upper, root_lower, root_upper)
        left = tangency_jet(source, candidate, parameter_lower, parameter_upper, root_lower, root_lower).value
        right = tangency_jet(source, candidate, parameter_lower, parameter_upper, root_upper, root_upper).value
        derivative = full.gradient[1]
        parameter_derivative = full.gradient[0]
    left_sign, right_sign = sign(left), sign(right)
    derivative_sign = sign(derivative)
    parameter_derivative_sign = sign(parameter_derivative)
    if (
        left_sign * right_sign == -1
        and derivative_sign != 0
        and parameter_derivative_sign != 0
    ):
        return [{
            "parameter_interval": [str(parameter_lower), str(parameter_upper)],
            "root_interval": [str(root_lower), str(root_upper)],
            "endpoint_signs": [left_sign, right_sign],
            "root_derivative_sign": derivative_sign,
            "parameter_derivative_sign": parameter_derivative_sign,
            "implicit_slope_sign": -derivative_sign * parameter_derivative_sign,
            "subdivision_depth": recursion,
        }]
    if recursion >= 8:
        return None
    middle = (parameter_lower + parameter_upper) / 2
    left_rows = certify_box(
        source, candidate, root_axis, root_lower_index, root_upper_index,
        parameter_lower, middle, recursion + 1,
    )
    if left_rows is None:
        return None
    right_rows = certify_box(
        source, candidate, root_axis, root_lower_index, root_upper_index,
        middle, parameter_upper, recursion + 1,
    )
    if right_rows is None:
        return None
    return left_rows + right_rows


def attempt_orientation(
    source: Any, candidate: str, root_axis: str, envelopes: list[list[int]]
) -> dict[str, Any] | None:
    parameter_axis = "p" if root_axis == "t" else "t"
    slabs = []
    for parameter_index, raw_lower, raw_upper, _count in envelopes:
        certified = None
        used_expansion = None
        for expansion in range(1, 17):
            root_lower_index = raw_lower - expansion
            root_upper_index = raw_upper + expansion
            try:
                rows = certify_box(
                    source, candidate, root_axis,
                    root_lower_index, root_upper_index,
                    coordinate(source, parameter_axis, parameter_index),
                    coordinate(source, parameter_axis, parameter_index + 1),
                )
            except Exception:
                rows = None
            if rows is not None:
                certified = rows
                used_expansion = expansion
                break
        if certified is None:
            return None
        slabs.extend(
            {"parameter_grid_index": parameter_index, "root_grid_envelope": [raw_lower, raw_upper], "root_grid_expansion": used_expansion, **row}
            for row in certified
        )
    root_signs = {row["root_derivative_sign"] for row in slabs}
    parameter_signs = {row["parameter_derivative_sign"] for row in slabs}
    slope_signs = {row["implicit_slope_sign"] for row in slabs}
    if len(root_signs) != 1 or len(parameter_signs) != 1 or len(slope_signs) != 1:
        return None
    return {
        "root_axis": root_axis,
        "parameter_axis": parameter_axis,
        "input_slice_count": len(envelopes),
        "certified_slab_count": len(slabs),
        "maximum_parameter_subdivision_depth": max(row["subdivision_depth"] for row in slabs),
        "maximum_root_grid_expansion": max(row["root_grid_expansion"] for row in slabs),
        "global_root_derivative_sign": next(iter(root_signs)),
        "global_parameter_derivative_sign": next(iter(parameter_signs)),
        "global_implicit_slope_sign": next(iter(slope_signs)),
        "parameter_grid_span_half_open": [envelopes[0][0], envelopes[-1][0] + 1],
        "slabs": slabs,
        "slabs_sha256": digest(slabs),
    }


def level_function(
    source: Any,
    candidate: str,
    root_axis: str,
    root_coordinate: Q,
    parameter_lower: Q,
    parameter_upper: Q,
) -> Jet:
    if root_axis == "t":
        return tangency_jet(
            source, candidate, root_coordinate, root_coordinate,
            parameter_lower, parameter_upper,
        )
    return tangency_jet(
        source, candidate, parameter_lower, parameter_upper,
        root_coordinate, root_coordinate,
    )


def certify_root_boundary_endpoint(
    source: Any,
    candidate: str,
    root_axis: str,
    root_boundary_index: int,
    parameter_cell_index: int,
) -> dict[str, Any] | None:
    parameter_axis = "p" if root_axis == "t" else "t"
    root_coordinate = coordinate(source, root_axis, root_boundary_index)
    for expansion in range(0, 9):
        lower_index = max(0, parameter_cell_index - expansion)
        upper_index = min(GRID, parameter_cell_index + 1 + expansion)
        lower = coordinate(source, parameter_axis, lower_index)
        upper = coordinate(source, parameter_axis, upper_index)
        function = level_function(
            source, candidate, root_axis, root_coordinate, lower, upper
        )
        derivative = function.gradient[1 if root_axis == "t" else 0]
        left = level_function(source, candidate, root_axis, root_coordinate, lower, lower).value
        right = level_function(source, candidate, root_axis, root_coordinate, upper, upper).value
        left_sign, right_sign, derivative_sign = sign(left), sign(right), sign(derivative)
        if left_sign * right_sign == -1 and derivative_sign != 0:
            return {
                "endpoint_type": "unique_root_axis_boundary_crossing",
                "root_boundary": "lower" if root_boundary_index == 0 else "upper",
                "root_coordinate": str(root_coordinate),
                "parameter_bracket": [str(lower), str(upper)],
                "parameter_endpoint_signs": [left_sign, right_sign],
                "parameter_derivative_sign": derivative_sign,
                "parameter_grid_expansion": expansion,
            }
    return None


def certify_parameter_boundary_endpoint(
    source: Any,
    candidate: str,
    root_axis: str,
    parameter_boundary_index: int,
    raw_root_lower: int,
    raw_root_upper: int,
) -> dict[str, Any] | None:
    parameter_axis = "p" if root_axis == "t" else "t"
    parameter = coordinate(source, parameter_axis, parameter_boundary_index)
    for expansion in range(1, 17):
        lower_index = max(0, raw_root_lower - expansion)
        upper_index = min(GRID, raw_root_upper + expansion)
        lower = coordinate(source, root_axis, lower_index)
        upper = coordinate(source, root_axis, upper_index)
        if root_axis == "t":
            function = tangency_jet(source, candidate, lower, upper, parameter, parameter)
            left = tangency_jet(source, candidate, lower, lower, parameter, parameter).value
            right = tangency_jet(source, candidate, upper, upper, parameter, parameter).value
            derivative = function.gradient[0]
        else:
            function = tangency_jet(source, candidate, parameter, parameter, lower, upper)
            left = tangency_jet(source, candidate, parameter, parameter, lower, lower).value
            right = tangency_jet(source, candidate, parameter, parameter, upper, upper).value
            derivative = function.gradient[1]
        left_sign, right_sign, derivative_sign = sign(left), sign(right), sign(derivative)
        if left_sign * right_sign == -1 and derivative_sign != 0:
            return {
                "endpoint_type": "unique_parameter_axis_boundary_endpoint",
                "parameter_boundary": "lower" if parameter_boundary_index == 0 else "upper",
                "parameter_coordinate": str(parameter),
                "root_bracket": [str(lower), str(upper)],
                "root_endpoint_signs": [left_sign, right_sign],
                "root_derivative_sign": derivative_sign,
                "root_grid_expansion": expansion,
            }
    return None


def endpoint_certificates(
    source: Any,
    candidate: str,
    proof: dict[str, Any],
    envelopes: list[list[int]],
) -> list[dict[str, Any]] | None:
    root_axis = proof["root_axis"]
    rows = []
    first_parameter = envelopes[0][0]
    last_parameter = envelopes[-1][0]
    for side, parameter_index, envelope in (
        ("start", first_parameter, envelopes[0]),
        ("end", last_parameter, envelopes[-1]),
    ):
        parameter_boundary = (
            0 if side == "start" and parameter_index == 0
            else GRID if side == "end" and parameter_index + 1 == GRID
            else None
        )
        if parameter_boundary is not None:
            row = certify_parameter_boundary_endpoint(
                source, candidate, root_axis, parameter_boundary,
                envelope[1], envelope[2],
            )
        else:
            touching = [index for index in (0, GRID) if envelope[1] == index or envelope[2] == index]
            if len(touching) != 1:
                return None
            row = certify_root_boundary_endpoint(
                source, candidate, root_axis, touching[0], parameter_index
            )
        if row is None:
            return None
        rows.append({"component_side": side, **row})
    return rows


def build() -> dict[str, Any]:
    document = json.loads(COMPONENTS.read_text())["result"]
    cores = core_cert.physical_cores()
    rows = []
    failures = []
    for pair in document["pair_rows"]:
        if not pair["carrier"].startswith("SECOND_CANDIDATE:"):
            continue
        source = cores[pair["source_core_index"]]
        candidate = parse_candidate(pair["carrier"])
        for component in pair["components"]:
            options = []
            for root_axis, envelopes in (
                ("t", component["p_slice_envelopes"]),
                ("p", component["t_slice_envelopes"]),
            ):
                proof = attempt_orientation(source, candidate, root_axis, envelopes)
                if proof is not None:
                    options.append(proof)
            identifier = {
                "source_core_index": pair["source_core_index"],
                "carrier": pair["carrier"],
                "connected_rank": component["connected_rank"],
            }
            if not options:
                failures.append(identifier)
                continue
            proof = min(
                options,
                key=lambda row: (
                    row["certified_slab_count"],
                    row["maximum_parameter_subdivision_depth"],
                    row["maximum_root_grid_expansion"],
                ),
            )
            envelopes = (
                component["p_slice_envelopes"]
                if proof["root_axis"] == "t"
                else component["t_slice_envelopes"]
            )
            endpoints = endpoint_certificates(
                source, candidate, proof, envelopes
            )
            if endpoints is None:
                failures.append({**identifier, "failure_stage": "physical_endpoint_clipping"})
                continue
            rows.append({
                **identifier,
                "candidate_id": candidate,
                "tube_cell_count": component["cell_count"],
                "component_cell_set_sha256": component["cell_set_sha256"],
                "curve_id": "physical-s0-time2-tangency:" + digest(identifier),
                "existence_for_every_parameter_in_certified_slab": True,
                "uniqueness_from_strict_root_derivative": True,
                "connected_by_unique_overlap_at_shared_parameter_endpoints": True,
                "physical_source_rectangle_intersection_connected_by_global_monotone_slope": True,
                "physical_endpoint_certificates": endpoints,
                **proof,
            })
    rows.sort(key=lambda row: row["curve_id"])
    failures.sort(key=canonical)
    return {
        "schema": "cm2.round78.time2-tangency-curves.v1",
        "result": {
            "input_tangency_tube_component_count": len(rows) + len(failures),
            "certified_curve_count": len(rows),
            "failure_count": len(failures),
            "failures": failures,
            "curve_rows": rows,
            "curve_rows_sha256": digest(rows),
            "scope": "implicit discriminant-zero curves inside the connected Round-77 tangency tubes; endpoint clipping and incidence with other physical carriers are audited separately",
        },
    }


def main() -> int:
    json.dump(build(), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
