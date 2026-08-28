#!/usr/bin/env python3
"""Exact D4 quotient of fixed-s=0 third-collision carrier components."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as step1
from cm2_round79_tangency_intersection_generator import digest


HERE = Path(__file__).resolve().parent
COMPONENTS = HERE / "cm2-round80-time3-carrier-components-2026-07-21.json"
GRID = 64
MATRICES = {
    "identity": (1, 0, 0, 1),
    "rotate90": (0, -1, 1, 0),
    "rotate180": (-1, 0, 0, -1),
    "rotate270": (0, 1, -1, 0),
    "reflect_x": (1, 0, 0, -1),
    "reflect_y": (-1, 0, 0, 1),
    "reflect_diag": (0, 1, 1, 0),
    "reflect_antidiag": (0, -1, -1, 0),
}
SIDE_VECTOR = {"E": (1, 0), "N": (0, 1), "W": (-1, 0), "S": (0, -1)}
VECTOR_SIDE = {value: key for key, value in SIDE_VECTOR.items()}
TANGENT_VECTOR = {"E": (0, 1), "W": (0, 1), "N": (1, 0), "S": (1, 0)}


def apply(matrix: tuple[int, int, int, int], point: tuple[int, int]) -> tuple[int, int]:
    a, b, c, d = matrix
    return a * point[0] + b * point[1], c * point[0] + d * point[1]


def determinant(matrix: tuple[int, int, int, int]) -> int:
    a, b, c, d = matrix
    return a * d - b * c


def parse_obstacle(identifier: str) -> tuple[str, tuple[int, int]]:
    match = re.fullmatch(r"([GW])\[(-?\d+),(-?\d+)\]", identifier)
    if match is None:
        raise RuntimeError(f"bad obstacle {identifier}")
    obstacle, i, j = match.group(1), int(match.group(2)), int(match.group(3))
    return obstacle, (2 * i + (obstacle == "W"), 2 * j + (obstacle == "W"))


def obstacle_id(obstacle: str, doubled_center: tuple[int, int]) -> str:
    offset = 1 if obstacle == "W" else 0
    x, y = doubled_center
    if (x - offset) % 2 or (y - offset) % 2:
        raise RuntimeError("transformed obstacle left lattice")
    return f"{obstacle}[{(x - offset) // 2},{(y - offset) // 2}]"


def transform_obstacle(
    identifier: str,
    source_obstacle: str,
    matrix: tuple[int, int, int, int],
) -> str:
    obstacle, center = parse_obstacle(identifier)
    transformed = apply(matrix, center)
    source_center = apply(matrix, (0, 0) if source_obstacle == "G" else (1, 1))
    desired = (0, 0) if source_obstacle == "G" else (1, 1)
    translation = (desired[0] - source_center[0], desired[1] - source_center[1])
    return obstacle_id(obstacle, (transformed[0] + translation[0], transformed[1] + translation[1]))


def chart_action(side: str, matrix: tuple[int, int, int, int]) -> tuple[str, int]:
    new_side = VECTOR_SIDE[apply(matrix, SIDE_VECTOR[side])]
    mapped_tangent = apply(matrix, TANGENT_VECTOR[side])
    target_tangent = TANGENT_VECTOR[new_side]
    sign = 1 if mapped_tangent == target_tangent else -1
    if mapped_tangent != (sign * target_tangent[0], sign * target_tangent[1]):
        raise RuntimeError("invalid tangent action")
    return new_side, sign


def core_action() -> dict[tuple[int, str], tuple[int, int, int]]:
    cores = core_cert.physical_cores()
    index = {}
    for core_index, core in enumerate(cores):
        side = core.chart_id.split(":")[1]
        index[(core.source, side, core.target_id, core.t0, core.t1, core.p0, core.p1)] = core_index
    result = {}
    for source_index, core in enumerate(cores):
        side = core.chart_id.split(":")[1]
        for name, matrix in MATRICES.items():
            new_side, t_sign = chart_action(side, matrix)
            target = transform_obstacle(core.target_id, core.source, matrix)
            t0, t1 = (core.t0, core.t1) if t_sign == 1 else (-core.t1, -core.t0)
            p_sign = determinant(matrix)
            p0, p1 = (core.p0, core.p1) if p_sign == 1 else (-core.p1, -core.p0)
            key = (core.source, new_side, target, t0, t1, p0, p1)
            if key in index:
                result[(source_index, name)] = (index[key], t_sign, p_sign)
    return result


def candidate_from_carrier(carrier: str) -> str:
    prefix = "THIRD_CANDIDATE:"
    suffix = ":unresolved_discriminant"
    if not carrier.startswith(prefix) or not carrier.endswith(suffix):
        raise RuntimeError("not a physical third tangency carrier")
    return carrier[len(prefix):-len(suffix)]


def component_id(source: int, carrier: str, rank: int) -> str:
    return f"rank3-carrier-component:{source}:{carrier}:{rank}"


def build() -> dict[str, Any]:
    cores = core_cert.physical_cores()
    document = json.loads(COMPONENTS.read_text())["result"]
    actions = core_action()
    components = {}
    lookup = {}
    for pair in document["pair_rows"]:
        if not pair["carrier"].startswith("THIRD_CANDIDATE:"):
            continue
        for component in pair["components"]:
            identifier = component_id(pair["source_core_index"], pair["carrier"], component["connected_rank"])
            cells = frozenset(map(tuple, component["cell_set"]))
            components[identifier] = {
                "source_core_index": pair["source_core_index"],
                "carrier": pair["carrier"],
                "connected_rank": component["connected_rank"],
                "cell_count": component["cell_count"],
                "cells": cells,
            }
            lookup[(pair["source_core_index"], pair["carrier"], cells)] = identifier
    action_rows = []
    action_map = {}
    component_symmetries = {}
    for identifier, component in sorted(components.items()):
        source_index = component["source_core_index"]
        source_type = cores[source_index].source
        candidate = candidate_from_carrier(component["carrier"])
        source_target_type = cores[source_index].target_id[0]
        symmetry_names = list(MATRICES) if source_type != source_target_type else ["identity", "reflect_diag"]
        component_symmetries[identifier] = symmetry_names
        for name in symmetry_names:
            matrix = MATRICES[name]
            target_source, t_sign, p_sign = actions[(source_index, name)]
            target_candidate = transform_obstacle(candidate, source_type, matrix)
            target_carrier = f"THIRD_CANDIDATE:{target_candidate}:unresolved_discriminant"
            transformed_cells = frozenset(
                (
                    i if t_sign == 1 else GRID - 1 - i,
                    j if p_sign == 1 else GRID - 1 - j,
                )
                for i, j in component["cells"]
            )
            target_identifier = lookup.get((target_source, target_carrier, transformed_cells))
            if target_identifier is None:
                raise RuntimeError(f"component action missing {identifier} under {name}")
            action_map[(identifier, name)] = target_identifier
            action_rows.append({
                "component_id": identifier,
                "symmetry": name,
                "image_component_id": target_identifier,
            })
    remaining = set(components)
    orbit_rows = []
    while remaining:
        representative = min(remaining)
        symmetry_names = component_symmetries[representative]
        orbit = sorted({action_map[(representative, name)] for name in symmetry_names})
        for member in orbit:
            if member not in remaining:
                raise RuntimeError("D4 orbit overlap")
            remaining.remove(member)
        stabilizer = sorted(name for name in symmetry_names if action_map[(representative, name)] == representative)
        orbit_rows.append({
            "orbit_rank": len(orbit_rows),
            "representative_component_id": representative,
            "orbit_size": len(orbit),
            "stabilizer": stabilizer,
            "member_component_ids": orbit,
            "common_cell_count": components[representative]["cell_count"],
            "sector_symmetry": "D4" if len(symmetry_names) == 8 else "C2_diagonal_reflection",
        })
    orbit_histogram = Counter(row["orbit_size"] for row in orbit_rows)
    action_rows.sort(key=lambda row: (row["component_id"], row["symmetry"]))
    result = {
        "symmetry_group": "stratified exact action: D4 on 16 cross-obstacle cores; diagonal C2 on 8 radial cores",
        "cross_obstacle_symmetry_order": 8,
        "radial_symmetry_order": 2,
        "physical_component_count": len(components),
        "component_orbit_count": len(orbit_rows),
        "orbit_size_histogram": {str(key): value for key, value in sorted(orbit_histogram.items())},
        "all_component_grid_sets_mapped_exactly": True,
        "action_row_count": len(action_rows),
        "action_rows_sha256": digest(action_rows),
        "orbit_rows": orbit_rows,
        "orbit_rows_sha256": digest(orbit_rows),
    }
    return {"schema": "cm2.round80.time3-dihedral-quotient.v1", "result": result, "result_sha256": digest(result)}


def main() -> int:
    json.dump(build(), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
