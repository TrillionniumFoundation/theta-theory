#!/usr/bin/env python3
"""Exact chord-diagram DCEL and cyclic boundary words for the depth-two quotient."""
from __future__ import annotations

import json
import math
import sys
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round79_tangency_endpoint_separation_generator import tangency_endpoints
from cm2_round79_tangency_intersection_generator import digest


HERE = Path(__file__).resolve().parent
R1 = HERE / "cm2-round73-base-r1-quotient-vertices-2026-07-21.json"
R2 = HERE / "cm2-round75-r2-physical-curves-2026-07-21.json"
TANGENCIES = HERE / "cm2-round78-time2-tangency-curves-2026-07-21.json"
SIDE_ORDER = {"p_lower": 0, "t_upper": 1, "p_upper": 2, "t_lower": 3}


def midpoint(interval: list[str] | tuple[str, str]) -> Q:
    lower, upper = map(Q, interval)
    return (lower + upper) / 2


def boundary_position(side: str, t: Q, p: Q) -> tuple[int, Q]:
    if side == "p_lower":
        return 0, t
    if side == "t_upper":
        return 1, p
    if side == "p_upper":
        return 2, -t
    if side == "t_lower":
        return 3, -p
    raise RuntimeError(side)


def endpoint_catalog() -> tuple[dict[int, list[dict[str, Any]]], list[dict[str, Any]], dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    by_core: dict[int, list[dict[str, Any]]] = defaultdict(list)
    chords = []
    r1_cells = {}
    r2_cells = {}
    r1_document = json.loads(R1.read_text())["result"]["rows"]
    for row in r1_document:
        endpoint_ids = []
        for endpoint in row["endpoint_vertices"]:
            identifier = f"R1-endpoint:{endpoint['candidate_family_id']}"
            t, p = midpoint(endpoint["t_interval"]), midpoint(endpoint["p_interval"])
            side = endpoint["stationary_side"]
            by_core[row["source_core_index"]].append({"vertex_id": identifier, "side": side, "t": t, "p": p, "family": "R1"})
            endpoint_ids.append(identifier)
        chord_id = f"R1-return-crosscut:{row['source_core_index']}"
        interior_id = f"R1-interior:{row['source_core_index']}"
        chords.append({
            "chord_id": chord_id,
            "source_core_index": row["source_core_index"],
            "endpoint_ids": endpoint_ids,
            "interior_vertex_id": interior_id,
            "family": "R1",
        })
        r1_cells[chord_id] = {
            "destination_core_index": row["destination_core_index"],
            "return_corner": row["return_corner"],
            "return_corner_sides": row["return_corner_sides"],
        }
    r2_document = json.loads(R2.read_text())["result"]
    curve_index = {}
    for curve in r2_document["curve_rows"]:
        source = curve["source_core_index"]
        p_side = next(side for side in curve["source_stationary_sides"] if side.startswith("p_"))
        t_side = next(side for side in curve["source_stationary_sides"] if side.startswith("t_"))
        p_endpoint_id = f"R2-endpoint:{curve['curve_id']}:p-side"
        t_endpoint_id = f"R2-endpoint:{curve['curve_id']}:t-side"
        p_endpoint = curve["endpoint_on_source_p_side"]
        t_endpoint = curve["endpoint_on_source_t_side"]
        by_core[source].append({
            "vertex_id": p_endpoint_id, "side": p_side,
            "t": midpoint(p_endpoint["t_interval"]), "p": Q(p_endpoint["p"]), "family": "R2",
        })
        by_core[source].append({
            "vertex_id": t_endpoint_id, "side": t_side,
            "t": Q(t_endpoint["t"]), "p": midpoint(t_endpoint["p_interval"]), "family": "R2",
        })
        chords.append({
            "chord_id": curve["curve_id"],
            "source_core_index": source,
            "endpoint_ids": [p_endpoint_id, t_endpoint_id],
            "interior_vertex_id": None,
            "family": "R2",
        })
        curve_index[curve["curve_id"]] = curve
    for rank, component in enumerate(r2_document["component_rows"]):
        r2_cells[f"R2-component:{rank}"] = {
            "source_core_index": component["source_core_index"],
            "destination_core_index": component["destination_core_index"],
            "chord_ids": sorted(component["physical_curve_ids"]),
            "branch": component["branch"],
        }
    tangency_curve_index = {row["curve_id"]: row for row in json.loads(TANGENCIES.read_text())["result"]["curve_rows"]}
    tangent_endpoints = tangency_endpoints()
    tangent_endpoint_ids: dict[str, list[str]] = defaultdict(list)
    for endpoint in tangent_endpoints:
        curve = tangency_curve_index[endpoint["curve_id"]]
        source = endpoint["source_core_index"]
        identifier = endpoint["endpoint_id"]
        varying = sum(endpoint["varying_interval"], Q()) / 2
        if endpoint["fixed_axis"] == "t":
            t, p = endpoint["fixed_coordinate"], varying
        else:
            t, p = varying, endpoint["fixed_coordinate"]
        by_core[source].append({"vertex_id": identifier, "side": endpoint["fixed_side"], "t": t, "p": p, "family": "tangency"})
        tangent_endpoint_ids[endpoint["curve_id"]].append(identifier)
    for curve_id, endpoint_ids in sorted(tangent_endpoint_ids.items()):
        curve = tangency_curve_index[curve_id]
        if len(endpoint_ids) != 2:
            raise RuntimeError("tangency endpoint count")
        chords.append({
            "chord_id": curve_id,
            "source_core_index": curve["source_core_index"],
            "endpoint_ids": sorted(endpoint_ids),
            "interior_vertex_id": None,
            "family": "tangency",
        })
    return by_core, chords, r1_cells, r2_cells


def alternating(a: int, b: int, c: int, d: int) -> bool:
    if a > b:
        a, b = b, a
    if c > d:
        c, d = d, c
    return (a < c < b < d) or (c < a < d < b)


def add_edge(edges: list[dict[str, Any]], left: str, right: str, edge_id: str, kind: str, chord_id: str | None = None) -> None:
    edges.append({"edge_id": edge_id, "vertices": [left, right], "kind": kind, "chord_id": chord_id})


def core_dcel(source_index: int, endpoints: list[dict[str, Any]], chords: list[dict[str, Any]], r1_cells: dict[str, dict[str, Any]], r2_cells: dict[str, dict[str, Any]]) -> dict[str, Any]:
    corner_ids = [f"corner:{source_index}:{name}" for name in ("BL", "BR", "TR", "TL")]
    side_endpoints: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for endpoint in endpoints:
        side_endpoints[endpoint["side"]].append(endpoint)
    for side, rows in side_endpoints.items():
        rows.sort(key=lambda row: boundary_position(side, row["t"], row["p"])[1])
        positions = [boundary_position(side, row["t"], row["p"])[1] for row in rows]
        if len(set(positions)) != len(positions):
            raise RuntimeError(f"duplicate boundary position {source_index}:{side}")
    boundary_vertices = [corner_ids[0]]
    boundary_vertices += [row["vertex_id"] for row in side_endpoints["p_lower"]]
    boundary_vertices += [corner_ids[1]]
    boundary_vertices += [row["vertex_id"] for row in side_endpoints["t_upper"]]
    boundary_vertices += [corner_ids[2]]
    boundary_vertices += [row["vertex_id"] for row in side_endpoints["p_upper"]]
    boundary_vertices += [corner_ids[3]]
    boundary_vertices += [row["vertex_id"] for row in side_endpoints["t_lower"]]
    boundary_index = {vertex: index for index, vertex in enumerate(boundary_vertices)}
    core_chords = [row for row in chords if row["source_core_index"] == source_index]
    for left_index in range(len(core_chords)):
        for right_index in range(left_index + 1, len(core_chords)):
            left, right = core_chords[left_index], core_chords[right_index]
            a, b = map(boundary_index.__getitem__, left["endpoint_ids"])
            c, d = map(boundary_index.__getitem__, right["endpoint_ids"])
            if alternating(a, b, c, d):
                raise RuntimeError(f"alternating certified-nonintersecting chords {left['chord_id']} {right['chord_id']}")
    vertex_count = len(boundary_vertices)
    coordinates = {
        vertex: (
            math.cos(2 * math.pi * index / vertex_count),
            math.sin(2 * math.pi * index / vertex_count),
        )
        for index, vertex in enumerate(boundary_vertices)
    }
    edges = []
    for index, left in enumerate(boundary_vertices):
        right = boundary_vertices[(index + 1) % vertex_count]
        add_edge(edges, left, right, f"stationary:{source_index}:{index}", "stationary")
    for chord in core_chords:
        left, right = chord["endpoint_ids"]
        if chord["interior_vertex_id"] is None:
            add_edge(edges, left, right, f"crosscut:{chord['chord_id']}", chord["family"], chord["chord_id"])
        else:
            interior = chord["interior_vertex_id"]
            coordinates[interior] = (
                (coordinates[left][0] + coordinates[right][0]) / 2,
                (coordinates[left][1] + coordinates[right][1]) / 2,
            )
            add_edge(edges, left, interior, f"crosscut:{chord['chord_id']}:0", chord["family"], chord["chord_id"])
            add_edge(edges, interior, right, f"crosscut:{chord['chord_id']}:1", chord["family"], chord["chord_id"])
    neighbors: dict[str, list[str]] = defaultdict(list)
    edge_lookup = {}
    for edge in edges:
        left, right = edge["vertices"]
        neighbors[left].append(right)
        neighbors[right].append(left)
        edge_lookup[frozenset((left, right))] = edge
    for vertex, rows in neighbors.items():
        x0, y0 = coordinates[vertex]
        rows.sort(key=lambda other: math.atan2(coordinates[other][1] - y0, coordinates[other][0] - x0))
    visited = set()
    cycles = []
    for edge in edges:
        for start in ((edge["vertices"][0], edge["vertices"][1]), (edge["vertices"][1], edge["vertices"][0])):
            if start in visited:
                continue
            cycle_vertices = []
            cycle_edges = []
            current = start
            while current not in visited:
                visited.add(current)
                left, right = current
                cycle_vertices.append(left)
                item = edge_lookup[frozenset((left, right))]
                direction = 1 if item["vertices"] == [left, right] else -1
                cycle_edges.append({"edge_id": item["edge_id"], "direction": direction, "kind": item["kind"], "chord_id": item["chord_id"]})
                around = neighbors[right]
                incoming_index = around.index(left)
                next_vertex = around[(incoming_index - 1) % len(around)]
                current = (right, next_vertex)
            if current != start:
                raise RuntimeError("half-edge traversal merged cycles")
            area = 0.0
            for index, vertex in enumerate(cycle_vertices):
                x1, y1 = coordinates[vertex]
                x2, y2 = coordinates[cycle_vertices[(index + 1) % len(cycle_vertices)]]
                area += x1 * y2 - y1 * x2
            cycles.append({"vertices": cycle_vertices, "edges": cycle_edges, "signed_area": area / 2})
    exterior = max(range(len(cycles)), key=lambda index: abs(cycles[index]["signed_area"]))
    faces = [cycle for index, cycle in enumerate(cycles) if index != exterior]
    expected_faces = len(core_chords) + 1
    if len(faces) != expected_faces:
        raise RuntimeError(f"face count {source_index}:{len(faces)} != {expected_faces}")
    corner_by_coordinate = {
        ("t_lower", "p_lower"): corner_ids[0],
        ("t_upper", "p_lower"): corner_ids[1],
        ("t_upper", "p_upper"): corner_ids[2],
        ("t_lower", "p_upper"): corner_ids[3],
    }
    face_rows = []
    for rank, face in enumerate(faces):
        chord_ids = sorted({edge["chord_id"] for edge in face["edges"] if edge["chord_id"] is not None})
        label = "Q2"
        destination = None
        source_record = None
        for chord_id, record in r1_cells.items():
            if chord_id not in chord_ids:
                continue
            t_side = next(side for side in record["return_corner_sides"] if side.startswith("t_"))
            p_side = next(side for side in record["return_corner_sides"] if side.startswith("p_"))
            if corner_by_coordinate[(t_side, p_side)] in face["vertices"]:
                label, destination, source_record = "R1", record["destination_core_index"], chord_id
        for component_id, record in r2_cells.items():
            if record["source_core_index"] == source_index and all(chord_id in chord_ids for chord_id in record["chord_ids"]):
                if label != "Q2":
                    raise RuntimeError("cell received R1 and R2 labels")
                label, destination, source_record = "R2", record["destination_core_index"], component_id
        boundary_word = [
            ("+" if edge["direction"] == 1 else "-") + edge["edge_id"]
            for edge in face["edges"]
        ]
        identity = {"source": source_index, "boundary_word": boundary_word}
        face_rows.append({
            "cell_id": "physical-s0-depth2-dcel-cell:" + digest(identity),
            "source_core_index": source_index,
            "source_local_face_rank": rank,
            "label": label,
            "destination_core_index": destination,
            "label_source_record": source_record,
            "cyclic_boundary_word": boundary_word,
            "boundary_word_sha256": digest(boundary_word),
        })
    histogram = Counter(row["label"] for row in face_rows)
    return {
        "source_core_index": source_index,
        "boundary_vertex_count": len(boundary_vertices),
        "interior_vertex_count": len(coordinates) - len(boundary_vertices),
        "stationary_edge_count": len(boundary_vertices),
        "crosscut_count": len(core_chords),
        "edge_count": len(edges),
        "edge_rows": edges,
        "edge_rows_sha256": digest(edges),
        "face_count": len(face_rows),
        "label_histogram": dict(sorted(histogram.items())),
        "boundary_vertices_ccw": boundary_vertices,
        "face_rows": face_rows,
    }


def build() -> dict[str, Any]:
    by_core, chords, r1_cells, r2_cells = endpoint_catalog()
    core_rows = [core_dcel(index, by_core[index], chords, r1_cells, r2_cells) for index in range(24)]
    face_rows = [row for core in core_rows for row in core.pop("face_rows")]
    face_rows.sort(key=lambda row: row["cell_id"])
    histogram = Counter(row["label"] for row in face_rows)
    vertices = sum(row["boundary_vertex_count"] + row["interior_vertex_count"] for row in core_rows)
    edges = sum(row["edge_count"] for row in core_rows)
    if (vertices, edges, len(face_rows)) != (392, 532, 164):
        raise RuntimeError(f"global f-vector {(vertices, edges, len(face_rows))}")
    if histogram != Counter({"Q2": 132, "R1": 16, "R2": 16}):
        raise RuntimeError(f"global labels {histogram}")
    result = {
        "fixed_parameter": "s=0",
        "f_vector": [vertices, edges, len(face_rows)],
        "euler_identity": f"{vertices}-{edges}+{len(face_rows)}=24",
        "cell_label_histogram": dict(sorted(histogram.items())),
        "exact_cyclic_boundary_word_count": len(face_rows),
        "exact_Q2_cyclic_boundary_word_count": histogram["Q2"],
        "core_rows": core_rows,
        "core_rows_sha256": digest(core_rows),
        "cell_rows": face_rows,
        "cell_rows_sha256": digest(face_rows),
        "strict_scope": "exact planar rotation system from certified boundary endpoint order and certified pairwise-nonintersecting crosscuts",
    }
    return {"schema": "cm2.round81.depth2-dcel.v1", "result": result, "result_sha256": digest(result)}


def main() -> int:
    json.dump(build(), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
