#!/usr/bin/env python3
"""Separate all tangency endpoints from the existing depth-two quotient vertices."""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
from typing import Any

from flint import ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
from cm2_round72_r1_positive_component_monotonicity_generator import output as r1_output
from cm2_round79_tangency_intersection_generator import aq, digest, strict_sign


HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "cm2-round78-physical-boundary-rank3-manifest-2026-07-21.json"
R1_WITNESSES = HERE / "cm2-round71-r1-nonempty-face-witnesses-2026-07-21.json"
R2_CURVES = HERE / "cm2-round75-r2-physical-curves-2026-07-21.json"
TANGENCIES = HERE / "cm2-round78-time2-tangency-curves-2026-07-21.json"
SCHEMA = "cm2.round79.tangency-endpoint-separation.v1"


def tangency_endpoints() -> list[dict[str, Any]]:
    rows = []
    curves = json.loads(TANGENCIES.read_text())["result"]["curve_rows"]
    for curve in curves:
        for index, endpoint in enumerate(curve["physical_endpoint_certificates"]):
            if endpoint["endpoint_type"] == "unique_parameter_axis_boundary_endpoint":
                fixed_axis = curve["parameter_axis"]
                fixed_coordinate = Q(endpoint["parameter_coordinate"])
                varying_axis = curve["root_axis"]
                varying_interval = tuple(map(Q, endpoint["root_bracket"]))
                fixed_side = f"{fixed_axis}_{endpoint['parameter_boundary']}"
            else:
                fixed_axis = curve["root_axis"]
                fixed_coordinate = Q(endpoint["root_coordinate"])
                varying_axis = curve["parameter_axis"]
                varying_interval = tuple(map(Q, endpoint["parameter_bracket"]))
                fixed_side = f"{fixed_axis}_{endpoint['root_boundary']}"
            rows.append({
                "endpoint_id": f"{curve['curve_id']}:endpoint:{index}",
                "curve_id": curve["curve_id"],
                "source_core_index": curve["source_core_index"],
                "fixed_side": fixed_side,
                "fixed_axis": fixed_axis,
                "fixed_coordinate": fixed_coordinate,
                "varying_axis": varying_axis,
                "varying_interval": varying_interval,
            })
    return rows


def r2_endpoints() -> list[dict[str, Any]]:
    rows = []
    curves = json.loads(R2_CURVES.read_text())["result"]["curve_rows"]
    for curve in curves:
        p_endpoint = curve["endpoint_on_source_p_side"]
        rows.append({
            "endpoint_id": f"{curve['curve_id']}:p-side",
            "source_core_index": curve["source_core_index"],
            "fixed_side": next(side for side in curve["source_stationary_sides"] if side.startswith("p_")),
            "varying_interval": tuple(map(Q, p_endpoint["t_interval"])),
        })
        t_endpoint = curve["endpoint_on_source_t_side"]
        rows.append({
            "endpoint_id": f"{curve['curve_id']}:t-side",
            "source_core_index": curve["source_core_index"],
            "fixed_side": next(side for side in curve["source_stationary_sides"] if side.startswith("t_")),
            "varying_interval": tuple(map(Q, t_endpoint["p_interval"])),
        })
    return rows


def disjoint(left: tuple[Q, Q], right: tuple[Q, Q]) -> bool:
    return left[1] < right[0] or right[1] < left[0]


def build() -> dict[str, Any]:
    ctx.prec = 384
    cores = core_cert.physical_cores()
    tangency = tangency_endpoints()
    r2 = r2_endpoints()
    side_groups: dict[tuple[int, str], list[dict[str, Any]]] = defaultdict(list)
    for endpoint in tangency:
        side_groups[(endpoint["source_core_index"], endpoint["fixed_side"])].append(endpoint)
    pair_rows = []
    for key, endpoints in sorted(side_groups.items()):
        for left, right in combinations(endpoints, 2):
            if not disjoint(left["varying_interval"], right["varying_interval"]):
                raise RuntimeError(f"overlapping tangency endpoints {left['endpoint_id']} {right['endpoint_id']}")
            pair_rows.append({
                "source_core_index": key[0],
                "fixed_side": key[1],
                "left_endpoint_id": left["endpoint_id"],
                "right_endpoint_id": right["endpoint_id"],
                "strict_interval_separation": True,
            })
    r2_index: dict[tuple[int, str], list[dict[str, Any]]] = defaultdict(list)
    for endpoint in r2:
        r2_index[(endpoint["source_core_index"], endpoint["fixed_side"])].append(endpoint)
    r2_rows = []
    for endpoint in tangency:
        for old in r2_index[(endpoint["source_core_index"], endpoint["fixed_side"])]:
            if not disjoint(endpoint["varying_interval"], old["varying_interval"]):
                raise RuntimeError(f"tangency/R2 endpoint overlap {endpoint['endpoint_id']} {old['endpoint_id']}")
            r2_rows.append({
                "source_core_index": endpoint["source_core_index"],
                "fixed_side": endpoint["fixed_side"],
                "tangency_endpoint_id": endpoint["endpoint_id"],
                "R2_endpoint_id": old["endpoint_id"],
                "strict_interval_separation": True,
            })
    manifest = json.loads(MANIFEST.read_text())["result"]["physical_boundary_carrier_atlas"]
    witness_index = {
        row["candidate_family_id"]: row
        for row in json.loads(R1_WITNESSES.read_text())["rows"]
    }
    r1_by_source: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for pair in manifest["time1_pair_rows"]:
        for curve in pair["physical_curves"]:
            r1_by_source[pair["source_core_index"]].append({
                **witness_index[curve["candidate_family_id"]],
                "physical_curve_id": curve["physical_curve_id"],
            })
    r1_rows = []
    for endpoint in tangency:
        source = cores[endpoint["source_core_index"]]
        varying_lower, varying_upper = endpoint["varying_interval"]
        if endpoint["fixed_axis"] == "t":
            box = (endpoint["fixed_coordinate"], endpoint["fixed_coordinate"], varying_lower, varying_upper)
        else:
            box = (varying_lower, varying_upper, endpoint["fixed_coordinate"], endpoint["fixed_coordinate"])
        for old in r1_by_source[endpoint["source_core_index"]]:
            destination = cores[old["destination_core_index"]]
            coordinate_index = 0 if old["level_coordinate"] == "t" else 1
            function = r1_output(source, destination, *box)[coordinate_index]
            function.value -= aq(Q(old["level_value"]))
            function_sign = strict_sign(function.value)
            if function_sign == 0:
                raise RuntimeError(f"tangency/R1 endpoint unresolved {endpoint['endpoint_id']} {old['physical_curve_id']}")
            r1_rows.append({
                "source_core_index": endpoint["source_core_index"],
                "fixed_side": endpoint["fixed_side"],
                "tangency_endpoint_id": endpoint["endpoint_id"],
                "R1_curve_id": old["physical_curve_id"],
                "R1_level_function_sign_on_endpoint_bracket": function_sign,
            })
    corner_rows = [
        {
            "endpoint_id": endpoint["endpoint_id"],
            "strictly_inside_open_stationary_side": True,
            "reason": "unique endpoint root lies strictly between opposite-sign bracket endpoints, including when one bracket endpoint is a rectangle corner",
        }
        for endpoint in tangency
    ]
    serial_endpoints = [
        {**row, "fixed_coordinate": str(row["fixed_coordinate"]), "varying_interval": list(map(str, row["varying_interval"]))}
        for row in tangency
    ]
    serial_endpoints.sort(key=lambda row: row["endpoint_id"])
    result = {
        "tangency_endpoint_count": len(tangency),
        "tangency_endpoints_strictly_inside_stationary_sides": len(corner_rows),
        "same_side_tangency_endpoint_pair_tests": len(pair_rows),
        "tangency_to_R2_endpoint_pair_tests": len(r2_rows),
        "tangency_endpoint_to_R1_curve_tests": len(r1_rows),
        "all_new_endpoints_are_distinct_from_each_other_and_old_depth2_vertices": True,
        "endpoint_rows": serial_endpoints,
        "endpoint_rows_sha256": digest(serial_endpoints),
        "same_side_pair_rows_sha256": digest(pair_rows),
        "R2_pair_rows_sha256": digest(r2_rows),
        "R1_test_rows_sha256": digest(r1_rows),
    }
    return {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}


def main() -> int:
    json.dump(build(), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
