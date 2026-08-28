#!/usr/bin/env python3
"""Certify source-core boundary endpoints of joined rank-three root components."""
from __future__ import annotations

import json
import sys
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
from cm2_round79_tangency_intersection_generator import digest
from cm2_round80_time3_adaptive_carrier_resolver import strict_sign, third_tangency_jet


HERE = Path(__file__).resolve().parent
ATLAS = HERE / "cm2-round82-rank3-physical-patch-atlas-2026-07-21.json"
JOINS = HERE / "cm2-round82-rank3-cross-tube-joins-2026-07-21.json"
MAXIMUM_DEPTH = 28
ROOT_REFINEMENT_STEPS = 80
ctx.prec = 512


def merge_intervals(intervals: list[tuple[Q, Q]]) -> list[tuple[Q, Q]]:
    result = []
    for lower, upper in sorted(intervals):
        if result and lower <= result[-1][1]:
            result[-1] = result[-1][0], max(result[-1][1], upper)
        else:
            result.append((lower, upper))
    return result


def evaluate(source: Any, second: str, candidate: str, side: str, lower: Q, upper: Q) -> tuple[Any, Any]:
    if side == "t_lower":
        jet = third_tangency_jet(source, second, candidate, source.t0, source.t0, lower, upper)
        return jet.value, jet.gradient[1]
    if side == "t_upper":
        jet = third_tangency_jet(source, second, candidate, source.t1, source.t1, lower, upper)
        return jet.value, jet.gradient[1]
    if side == "p_lower":
        jet = third_tangency_jet(source, second, candidate, lower, upper, source.p0, source.p0)
        return jet.value, jet.gradient[0]
    jet = third_tangency_jet(source, second, candidate, lower, upper, source.p1, source.p1)
    return jet.value, jet.gradient[0]


def point_value(source: Any, second: str, candidate: str, side: str, value: Q) -> Any:
    if side == "t_lower":
        return third_tangency_jet(source, second, candidate, source.t0, source.t0, value, value).value
    if side == "t_upper":
        return third_tangency_jet(source, second, candidate, source.t1, source.t1, value, value).value
    if side == "p_lower":
        return third_tangency_jet(source, second, candidate, value, value, source.p0, source.p0).value
    return third_tangency_jet(source, second, candidate, value, value, source.p1, source.p1).value


def refine_root(
    source: Any,
    second: str,
    candidate: str,
    side: str,
    lower: Q,
    upper: Q,
    lower_sign: int,
    upper_sign: int,
) -> tuple[Q, Q, int, int]:
    for _step in range(ROOT_REFINEMENT_STEPS):
        middle = (lower + upper) / 2
        middle_sign = strict_sign(point_value(source, second, candidate, side, middle))
        if middle_sign == 0:
            raise RuntimeError("endpoint bisection lost strict midpoint sign")
        if middle_sign == lower_sign:
            lower, lower_sign = middle, middle_sign
        else:
            upper, upper_sign = middle, middle_sign
    return lower, upper, lower_sign, upper_sign


def isolate(source: Any, second: str, candidate: str, side: str, initial: tuple[Q, Q]) -> dict[str, Any]:
    stack = [(initial, 0)]
    roots = []
    excluded = 0
    tests = 0
    maximum_depth = 0
    unresolved = []
    while stack:
        (lower, upper), depth = stack.pop()
        maximum_depth = max(maximum_depth, depth)
        value, derivative = evaluate(source, second, candidate, side, lower, upper)
        tests += 1
        if strict_sign(value):
            excluded += 1
            continue
        derivative_sign = strict_sign(derivative)
        lower_sign = strict_sign(point_value(source, second, candidate, side, lower))
        upper_sign = strict_sign(point_value(source, second, candidate, side, upper))
        if derivative_sign and lower_sign * upper_sign == -1:
            lower, upper, lower_sign, upper_sign = refine_root(
                source, second, candidate, side, lower, upper, lower_sign, upper_sign
            )
            roots.append({
                "parameter_interval": [str(lower), str(upper)],
                "derivative_sign": derivative_sign,
                "endpoint_signs": [lower_sign, upper_sign],
                "subdivision_depth": depth,
                "directed_bisection_refinement_steps": ROOT_REFINEMENT_STEPS,
            })
            continue
        if depth == MAXIMUM_DEPTH:
            unresolved.append([str(lower), str(upper)])
            continue
        middle = (lower + upper) / 2
        stack.extend((((middle, upper), depth + 1), ((lower, middle), depth + 1)))
    roots.sort(key=lambda row: row["parameter_interval"])
    return {
        "interval_box_tests": tests,
        "excluded_interval_count": excluded,
        "maximum_depth": maximum_depth,
        "unique_root_count": len(roots),
        "root_rows": roots,
        "unresolved_interval_count": len(unresolved),
        "unresolved_intervals_sha256": digest(unresolved),
    }


def build() -> dict[str, Any]:
    cores = core_cert.physical_cores()
    patch_rows = json.loads(ATLAS.read_text())["result"]["physical_patch_rows"]
    patch_by_id = {row["physical_patch_id"]: row for row in patch_rows}
    components = json.loads(JOINS.read_text())["result"]["component_rows"]
    endpoint_rows = []
    component_rows = []
    for component in components:
        source = cores[component["source_core_index"]]
        side_intervals = {"t_lower": [], "t_upper": [], "p_lower": [], "p_upper": []}
        for patch_id in component["physical_patch_ids"]:
            for raw_box in patch_by_id[patch_id]["boxes"]:
                t0, t1, p0, p1 = map(Q, raw_box)
                if t0 == source.t0:
                    side_intervals["t_lower"].append((p0, p1))
                if t1 == source.t1:
                    side_intervals["t_upper"].append((p0, p1))
                if p0 == source.p0:
                    side_intervals["p_lower"].append((t0, t1))
                if p1 == source.p1:
                    side_intervals["p_upper"].append((t0, t1))
        local_endpoints = []
        tests = 0
        for side, intervals in side_intervals.items():
            for interval_rank, interval in enumerate(merge_intervals(intervals)):
                result = isolate(
                    source, component["second_selected_target_id"], component["third_candidate_id"], side, interval
                )
                tests += result["interval_box_tests"]
                if result["unresolved_interval_count"]:
                    raise RuntimeError(f"unresolved endpoint {component['physical_root_component_id']} {side}")
                for root_rank, root in enumerate(result["root_rows"]):
                    identity = {
                        "component": component["physical_root_component_id"],
                        "side": side,
                        "interval_rank": interval_rank,
                        "root_rank": root_rank,
                    }
                    endpoint = {
                        "physical_endpoint_id": "physical-s0-rank3-boundary-endpoint:" + digest(identity),
                        "physical_root_component_id": component["physical_root_component_id"],
                        "source_core_index": component["source_core_index"],
                        "second_selected_target_id": component["second_selected_target_id"],
                        "third_candidate_id": component["third_candidate_id"],
                        "source_boundary_side": side,
                        **root,
                    }
                    endpoint_rows.append(endpoint)
                    local_endpoints.append(endpoint["physical_endpoint_id"])
        component_rows.append({
            "physical_root_component_id": component["physical_root_component_id"],
            "source_boundary_endpoint_count": len(local_endpoints),
            "source_boundary_endpoint_ids_sha256": digest(sorted(local_endpoints)),
            "interval_box_tests": tests,
        })
    endpoint_rows.sort(key=lambda row: row["physical_endpoint_id"])
    component_rows.sort(key=lambda row: row["physical_root_component_id"])
    endpoint_histogram = Counter(row["source_boundary_endpoint_count"] for row in component_rows)
    result = {
        "joined_physical_root_component_count": len(components),
        "component_source_boundary_endpoint_count_histogram": {
            str(key): value for key, value in sorted(endpoint_histogram.items())
        },
        "certified_source_boundary_endpoint_count": len(endpoint_rows),
        "total_interval_box_tests": sum(row["interval_box_tests"] for row in component_rows),
        "unresolved_source_boundary_interval_count": 0,
        "endpoint_rows": endpoint_rows,
        "endpoint_rows_sha256": digest(endpoint_rows),
        "component_rows": component_rows,
        "component_rows_sha256": digest(component_rows),
        "strict_scope": "unique zeros on source-core boundary intervals touched by certified root boxes; internal endpoints and uncovered-gap continuation are not asserted",
    }
    return {"schema": "cm2.round82.rank3-boundary-endpoints.v1", "result": result, "result_sha256": digest(result)}


def main() -> int:
    json.dump(build(), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
