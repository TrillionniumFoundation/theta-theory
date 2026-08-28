#!/usr/bin/env python3
"""Arb exclusion of intersections between each R2 band's two faces."""
from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as step1
from cm2_round75_r2_physical_curve_generator import t2_output


HERE = Path(__file__).resolve().parent
CURVES = HERE / "cm2-round75-r2-physical-curves-2026-07-21.json"
SCHEMA = "cm2.round75.r2-curve-nonintersection.v1"


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def excluded(value: Any, level: Q) -> bool:
    ball = value.value
    target = step1.arbq(level)
    return bool(ball < target) or bool(ball > target)


def split(core: Any, box: tuple[Q, Q, Q, Q, str, int]) -> tuple[tuple[Q, Q, Q, Q, str, int], ...]:
    t0, t1, p0, p1, path, depth = box
    if (t1 - t0) / (core.t1 - core.t0) >= (p1 - p0) / (core.p1 - core.p0):
        middle = (t0 + t1) / 2
        return ((t0, middle, p0, p1, path + "0", depth + 1), (middle, t1, p0, p1, path + "1", depth + 1))
    middle = (p0 + p1) / 2
    return ((t0, t1, p0, middle, path + "0", depth + 1), (t0, t1, middle, p1, path + "1", depth + 1))


def build() -> dict[str, Any]:
    document = json.loads(CURVES.read_text())["result"]
    curves = {row["curve_id"]: row for row in document["curve_rows"]}
    cores = core_cert.physical_cores()
    rows = []
    source_groups: dict[int, list[dict[str, Any]]] = {}
    for curve in curves.values():
        source_groups.setdefault(curve["source_core_index"], []).append(curve)
    for source_index, source_curves in sorted(source_groups.items()):
      source_curves.sort(key=canonical)
      if len(source_curves) != 4:
        raise RuntimeError("expected four R2 curves per source core")
      for left_index in range(len(source_curves)):
       for right_index in range(left_index + 1, len(source_curves)):
        left_curve, right_curve = source_curves[left_index], source_curves[right_index]
        source = cores[source_index]
        left_destination = cores[left_curve["destination_core_index"]]
        right_destination = cores[right_curve["destination_core_index"]]
        left_coordinate = "target_t" if left_curve["active_side"].startswith("t_") else "target_p"
        right_coordinate = "target_t" if right_curve["active_side"].startswith("t_") else "target_p"
        left_level, right_level = Q(left_curve["level"]), Q(right_curve["level"])
        stack = [(source.t0, source.t1, source.p0, source.p1, "", 0)]
        leaves = []
        tests = 0
        unresolved = []
        while stack:
            box = stack.pop()
            t0, t1, p0, p1, path, depth = box
            left_values = t2_output(source, left_destination, t0, t1, p0, p1)
            right_values = t2_output(source, right_destination, t0, t1, p0, p1)
            tests += 1
            if excluded(left_values[left_coordinate], left_level):
                leaves.append({"dyadic_path": path, "depth": depth, "separator": "left_curve"})
            elif excluded(right_values[right_coordinate], right_level):
                leaves.append({"dyadic_path": path, "depth": depth, "separator": "right_curve"})
            elif depth < 24:
                stack.extend(reversed(split(source, box)))
            else:
                unresolved.append({"dyadic_path": path, "depth": depth})
        if unresolved:
            raise RuntimeError(f"unresolved curve intersection {source_index}:{left_curve['curve_id']}:{right_curve['curve_id']}:{len(unresolved)}")
        leaves.sort(key=lambda row: row["dyadic_path"])
        rows.append({
            "source_core_index": source_index,
            "left_curve_id": left_curve["curve_id"],
            "right_curve_id": right_curve["curve_id"],
            "left_destination_core_index": left_curve["destination_core_index"],
            "right_destination_core_index": right_curve["destination_core_index"],
            "levels": [str(left_level), str(right_level)],
            "box_tests": tests,
            "excluded_leaf_count": len(leaves),
            "maximum_depth": max(row["depth"] for row in leaves),
            "unresolved_count": 0,
            "leaves_sha256": digest(leaves),
        })
    rows.sort(key=canonical)
    result = {
        "source_core_count": len(source_groups),
        "curve_pair_count": len(rows),
        "nonintersecting_curve_pairs": sum(row["unresolved_count"] == 0 for row in rows),
        "total_box_tests": sum(row["box_tests"] for row in rows),
        "total_excluded_leaves": sum(row["excluded_leaf_count"] for row in rows),
        "global_maximum_depth": max(row["maximum_depth"] for row in rows),
        "unresolved_count": sum(row["unresolved_count"] for row in rows),
        "rows": rows,
        "rows_sha256": digest(rows),
    }
    return {"schema": SCHEMA, "construction": {"arithmetic": "384-bit Arb", "maximum_binary_depth": 24}, "result": result}


if __name__ == "__main__":
    json.dump(build(), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
