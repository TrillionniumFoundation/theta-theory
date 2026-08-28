#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import shutil
import sys
from collections import Counter, defaultdict, deque
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterable


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

ROOT = Path(__file__).resolve().parent.parent
DELIVERABLES = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"
SCHEMA = "cm2.round306c34.d02-seed-event-component-frontier.v1"
TERMINAL_ROW_SCHEMA = "cm2.round306c34.round144-terminal-frontier-row.v1"
EVENT_ROW_SCHEMA = "cm2.round306c34.typed-first-event-binding-row.v1"
COMPONENT_ROW_SCHEMA = "cm2.round306c34.ordinary-component-row.v1"
EXPECTED_C32_OBJECT = "32ff9e0f90a12f17b16f67086eabda0986a0d52d185bea0c5c16e20518ca1474"
EXPECTED_C33_OBJECT = "82dedeace982db89763e8a7e318fa6605d18cadc6bf390d6b23585d0922b87a0"

AUTHORITY_FILES = {
    "round140_bridge": (
        "cm2-round140-fixed-s-adaptive-component-identity-bridge-2026-07-24.json",
        "60a364ec21cc1bedf83f7287a7e8f4e9a90a2be431d04cec8fed3f9c0102496b",
    ),
    "round140_bridge_verification": (
        "cm2-round140-fixed-s-adaptive-component-identity-bridge-verification-2026-07-24.json",
        "c9b36397f28a63f5408fc82ee474617fe54e73774382c607dc10bc3e9b6dd746",
    ),
    "round140_materialization": (
        "cm2-round140-round35-parent-w-r1648-materialization-audit-2026-07-24.json",
        "7988f4c9588894ec964e2c6efec4dd07dd28d5011c0bf004ad73f99414534eed",
    ),
    "round140_materialization_verification": (
        "cm2-round140-round35-parent-w-r1648-materialization-audit-verification-2026-07-24.json",
        "9d898c0cea05069511732acd2be74f04d66f416d10f4ca72cd6e6bccf8b9cf33",
    ),
    "round165": (
        "cm2_round165_adaptive_typed_seam_census_certificate.json",
        "93e2899d0a9a79a82e1b193158f3733e891e2c5b4c9ce83f970aff40bf75c270",
    ),
    "round165_verification": (
        "cm2_round165_adaptive_typed_seam_census_verification.json",
        "86356b4b778fc8e2f74ab1edec30c96346027a9c17ade38c6f5aef269d6e5786",
    ),
    "round175": (
        "cm2_round175_dimension_safe_tangency_arrangement_certificate.json",
        "827d6f674dd4a5291bf08f5ffd65b31187faa1c9fe977e1b7e7da10cd1166d72",
    ),
    "round175_verification": (
        "cm2_round175_dimension_safe_tangency_arrangement_verification.json",
        "ed5fd96874a65b49a1e05d5589e2dd9711f224d08a99123e582bc54bce294f6a",
    ),
    "round177": (
        "cm2_round177_tangency_boundary_and_source_seam_ledger_certificate.json",
        "9352f036325bc6e884fc6d31da2e1e2a04532d45fb11de90b3e5051103f56a9f",
    ),
    "round177_verification": (
        "cm2_round177_tangency_boundary_and_source_seam_ledger_verification.json",
        "6968d5b50037457e546c06fbe2f7f620fbbfbb73f354f78b7035afb23426934e",
    ),
}


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def strict_json(path: Path) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, f"duplicate key:{path}:{key}")
            result[key] = value
        return result

    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=unique,
        parse_float=lambda value: (_ for _ in ()).throw(ValueError(value)),
        parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)),
    )
    require(type(value) is dict, f"top object:{path}")
    return value


def validate_object(value: dict[str, Any], field: str, expected: str, label: str) -> None:
    copy = dict(value)
    object_sha = copy.pop(field, None)
    require(object_sha == expected == digest(copy), f"object hash:{label}")


def validate_envelope(value: dict[str, Any], expected: str, label: str) -> None:
    require(value.get("result_sha256") == expected, f"expected result:{label}")
    require(value.get("result_sha256") == digest(value.get("result")), f"self hash:{label}")


def load_authorities() -> dict[str, dict[str, Any]]:
    values: dict[str, dict[str, Any]] = {}
    for label, (name, expected) in AUTHORITY_FILES.items():
        path = DELIVERABLES / name
        value = strict_json(path)
        validate_envelope(value, expected, label)
        if label.endswith("verification"):
            require(value["result"].get("status") == "PASS", f"verification status:{label}")
        values[label] = value
    require(
        values["round140_bridge_verification"]["result"].get(
            "certificate_result_sha256"
        ) == values["round140_bridge"]["result_sha256"],
        "Round140 bridge verification binding",
    )
    require(
        values["round140_materialization_verification"]["result"].get("status") == "PASS",
        "Round140 materialization verification",
    )
    for round_name in ("round165", "round175", "round177"):
        verification = values[f"{round_name}_verification"]["result"]
        require(
            verification.get("certificate_result_sha256")
            == values[round_name]["result_sha256"],
            f"verification binding:{round_name}",
        )
    return values


def validate_manifest(directory: Path) -> None:
    rows = (directory / "root_manifest.sha256").read_text(encoding="utf-8").splitlines()
    require(rows, f"manifest nonempty:{directory}")
    names: list[str] = []
    for row in rows:
        expected, filename = row.split("  ", 1)
        names.append(filename)
        path = directory / filename
        require(path.is_file() and file_sha256(path) == expected, f"manifest member:{filename}")
    require(names == sorted(names) and len(names) == len(set(names)), f"manifest order:{directory}")


def read_ledger(directory: Path, descriptor: dict[str, Any]) -> list[dict[str, Any]]:
    path = directory / descriptor["filename"]
    require(
        path.is_file()
        and path.stat().st_size == descriptor["size"]
        and file_sha256(path) == descriptor["sha256"],
        f"ledger file:{path}",
    )
    rows: list[dict[str, Any]] = []
    sequence = hashlib.sha256()
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        for line in stream:
            row = json.loads(line)
            copy = dict(row)
            row_sha = copy.pop("row_sha256", None)
            require(row_sha == digest(copy), f"ledger row hash:{path}")
            rows.append(row)
            sequence.update((row_sha + "\n").encode("ascii"))
    require(len(rows) == descriptor["row_count"], f"ledger count:{path}")
    require(
        sequence.hexdigest() == descriptor["row_hash_line_sequence_sha256"],
        f"ledger sequence:{path}",
    )
    return rows


class LedgerWriter:
    def __init__(self, path: Path, order: str) -> None:
        self.path = path
        self.order = order
        self.row_count = 0
        self.sequence = hashlib.sha256()
        self.raw: Any = None
        self.gz: Any = None
        self.stream: Any = None

    def __enter__(self) -> LedgerWriter:
        self.raw = self.path.open("wb")
        self.gz = gzip.GzipFile(filename="", mode="wb", fileobj=self.raw, mtime=0)
        self.stream = self.gz
        return self

    def write(self, row: dict[str, Any]) -> None:
        require("row_sha256" not in row, "writer row hash absent")
        row_sha = digest(row)
        complete = {**row, "row_sha256": row_sha}
        self.stream.write(canonical(complete) + b"\n")
        self.row_count += 1
        self.sequence.update((row_sha + "\n").encode("ascii"))

    def __exit__(self, *args: Any) -> None:
        self.gz.close()
        self.raw.close()

    def descriptor(self) -> dict[str, Any]:
        return {
            "filename": self.path.name,
            "order": self.order,
            "row_count": self.row_count,
            "row_hash_line_sequence_sha256": self.sequence.hexdigest(),
            "sha256": file_sha256(self.path),
            "size": self.path.stat().st_size,
        }


def load_inputs(c32: Path, c33: Path) -> tuple[
    dict[str, Any], dict[str, Any], list[dict[str, Any]], list[dict[str, Any]],
    list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]],
]:
    validate_manifest(c32)
    validate_manifest(c33)
    c32_result = strict_json(c32 / "result.json")
    c33_result = strict_json(c33 / "result.json")
    validate_object(c32_result, "object_sha256", EXPECTED_C32_OBJECT, "C32")
    validate_object(c33_result, "object_sha256", EXPECTED_C33_OBJECT, "C33")
    cells = read_ledger(c32, c32_result["ledgers"]["cells"])
    adjacency = read_ledger(c32, c32_result["ledgers"]["intra_chart_adjacency"])
    seams = read_ledger(c32, c32_result["ledgers"]["source_chart_seams"])
    events = read_ledger(c32, c32_result["ledgers"]["inherited_event_faces"])
    crosswalk = read_ledger(c33, c33_result["row_level_crosswalk"])
    return c32_result, c33_result, cells, adjacency, seams, events, crosswalk


def seed_crosswalk(
    cells: list[dict[str, Any]], crosswalk: dict[str, dict[str, Any]],
    authorities: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    materialization = authorities["round140_materialization"]["result"]
    root = materialization["fixed_parameter_and_exact_implicit_leaf"]
    t_lower, t_upper = map(Q, root["deep_D0_root_bracket"])
    p_star = Q(root["fixed_p_star"])
    seed_cells: list[dict[str, Any]] = []
    for cell in cells:
        if cell["gate3_chart"] != "W:E":
            continue
        t0, t1 = map(Q, cell["gate3_product_box"]["t"])
        p0, p1 = map(Q, cell["physical_p_interval"])
        if t0 < t_lower and t_upper < t1 and p0 < p_star < p1:
            seed_cells.append(cell)
    require(len(seed_cells) == 1, "unique exact R1648 seed cell")
    cell = seed_cells[0]
    require(cell["origin_key"] == "W:E:04.07.0t0", "seed origin key")
    disposition = crosswalk[cell["cell_id"]]
    require(
        disposition["formal_source_W_disposition"] == "RESOLVED_NONEXCLUDED"
        and cell["inherited_event_graph"] is None,
        "seed disposition",
    )
    adaptive = authorities["round140_bridge"]["result"]["fixed_s_adaptive_path_cell"]
    at0, at1 = map(Q, adaptive["t_open_interval"])
    ap0, ap1 = map(Q, adaptive["p_open_interval"])
    t0, t1 = map(Q, cell["gate3_product_box"]["t"])
    p0, p1 = map(Q, cell["physical_p_interval"])
    require(t0 < at0 < at1 < t1 and p0 < ap0 < ap1 < p1, "adaptive cell containment")
    require(
        adaptive["closure_first_return_is_exactly_R1648"] is True
        and adaptive["closure_has_one_strict_ordinary_owner_path"] is True
        and adaptive["open_support_connected"] is True,
        "adaptive connected path authority",
    )
    return {
        "origin_key": cell["origin_key"],
        "cell_id": cell["cell_id"],
        "compact_chart": cell["compact_chart"],
        "gate3_chart": cell["gate3_chart"],
        "coarse_t_interval": cell["gate3_product_box"]["t"],
        "coarse_p_interval": cell["physical_p_interval"],
        "t_star_isolating_bracket_sha256": digest(root["deep_D0_root_bracket"]),
        "p_star": root["fixed_p_star"],
        "adaptive_path_cell_id": adaptive["adaptive_path_cell_id"],
        "adaptive_t_open_interval_sha256": digest(adaptive["t_open_interval"]),
        "adaptive_p_open_interval_sha256": digest(adaptive["p_open_interval"]),
        "adaptive_open_cell_strictly_inside_coarse_cell": True,
        "coarse_cell_is_not_promoted_to_connected": True,
        "reason": "the Round140 connected open cell is a strict subset of this C32 cell",
    }


def event_bindings(
    cells: dict[str, dict[str, Any]], crosswalk: dict[str, dict[str, Any]],
    event_rows: list[dict[str, Any]], authorities: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    round165_rows = {
        row["leaf_key"]: row
        for row in authorities["round165"]["result"]["adaptive_seam_census"]["terminal_rows"]
        if row.get("typed_seam") is not None
    }
    require(len(round165_rows) == 280, "Round165 typed rows")
    round175_rows = {
        row["ambient_leaf_key"]: row
        for row in authorities["round175"]["result"]["parent_arrangement_census"]["all_22_parent_rows"]
    }
    round177_rows = {
        row["ambient_leaf_key"]: row
        for row in authorities["round177"]["result"]["exact_parent_rows"]
    }
    require(len(round177_rows) == 16, "Round177 exact rows")
    bindings: list[dict[str, Any]] = []
    seen: set[str] = set()
    for event in sorted(event_rows, key=lambda row: row["origin_key"]):
        cell = cells[event["incident_cell_id"]]
        require(cell["origin_key"] == event["origin_key"], "event cell origin")
        disposition = crosswalk[cell["cell_id"]]
        if disposition["formal_source_W_disposition"] != "RESOLVED_NONEXCLUDED":
            continue
        payload = event["event_payload"]
        kind = payload["event_kind"]
        if kind == "ROUND165_TYPED_OUTGOING_CHART_SEAM_GRAPH":
            source = round165_rows[cell["origin_key"]]
            typed = source["typed_seam"]
            require(
                digest(source) == cell["source_lineage"]["source_row_sha256"]
                and digest(typed) == payload["typed_seam_sha256"]
                and typed["three_stratum_partition_materialized"] is True
                and typed["whole_parent_leaf_excluded"] is False
                and typed["diagonal_half_open_owner"] == "W",
                f"Round165 event binding:{cell['origin_key']}",
            )
            authority = {
                "certificate": "Round165",
                "source_row_sha256": digest(source),
                "typed_graph_sha256": digest(typed),
                "graph_kind": typed["graph_kind"],
                "seam_id": typed["seam_id"],
                "stratum_count": len(typed["strata"]),
            }
        else:
            require(kind == "GATE3_PHYSICAL_FIRST_TANGENCY_GRAPH", "event kind")
            source175 = round175_rows[cell["origin_key"]]
            source177 = round177_rows[cell["origin_key"]]
            require(
                source175["classification"] == "MIXED_COMPOSITE"
                and source175["conservative_live_composite"] is True
                and source177["parent_classification"] == "MIXED_BOUNDED_RESIDUAL"
                and source177["whole_parent_new_integer_exclusion"] is False
                and source177["distinguished_intersections"]["Delta_intersect_H"]["status"].startswith("EMPTY_CERTIFIED")
                and source177["later_frozen_prefix_processing"]["eligible_open_component_count"] == 1,
                f"Round177 tangency binding:{cell['origin_key']}",
            )
            authority = {
                "certificate": "Round175+Round177",
                "round175_row_sha256": source175["row_sha256"],
                "round177_row_sha256": source177["row_sha256"],
                "tangency_target": source177["Round175_tangency_target"],
                "open_sign_stratum_count": source177["three_dimensional_sign_strata"][
                    "connected_open_3D_stratum_count"
                ],
                "Delta_graph_dimension": source177["Delta_zero_graph"]["dimension"],
                "H_graph_dimension": source177["H_zero_graph"]["dimension"],
            }
        require(cell["cell_id"] not in seen, "duplicate event binding")
        seen.add(cell["cell_id"])
        bindings.append({
            "schema": EVENT_ROW_SCHEMA,
            "cell_id": cell["cell_id"],
            "origin_key": cell["origin_key"],
            "compact_chart": cell["compact_chart"],
            "event_kind": kind,
            "event_payload_sha256": digest(payload),
            "authority": authority,
            "earliest_first_collision_event": True,
            "round144_terminal_class": "TYPED_EVENT_GRAPH",
            "round144_terminal_credit": 1,
            "strict_nonpromotion": {
                "connected_to_known_credit": 0,
                "D02_credit": 0,
                "D03_credit": 0,
            },
        })
    require(
        Counter(row["event_kind"] for row in bindings)
        == Counter({
            "ROUND165_TYPED_OUTGOING_CHART_SEAM_GRAPH": 280,
            "GATE3_PHYSICAL_FIRST_TANGENCY_GRAPH": 16,
        }),
        "live event binding census",
    )
    return bindings


def graph_components(
    cells: dict[str, dict[str, Any]], crosswalk: dict[str, dict[str, Any]],
    adjacency_rows: Iterable[dict[str, Any]], seam_rows: Iterable[dict[str, Any]],
    event_ids: set[str], seed_id: str,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    live = {
        cell_id for cell_id, row in crosswalk.items()
        if row["formal_source_W_disposition"] == "RESOLVED_NONEXCLUDED"
    }
    require(len(live) == 2020 and event_ids <= live and len(event_ids) == 296, "live graph inputs")
    graph: dict[str, set[str]] = defaultdict(set)
    edge_counts: Counter[str] = Counter()
    for kind, rows, left, right in (
        ("INTRA_CHART", adjacency_rows, "negative_cell_id", "positive_cell_id"),
        ("SOURCE_CHART_SEAM", seam_rows, "left_cell_id", "right_cell_id"),
    ):
        for row in rows:
            first, second = row[left], row[right]
            if first in live and second in live:
                graph[first].add(second)
                graph[second].add(first)
                edge_counts[kind] += 1
    reached = {seed_id}
    queue = deque([seed_id])
    distance = {seed_id: 0}
    while queue:
        current = queue.popleft()
        for neighbour in graph[current]:
            if neighbour not in reached:
                reached.add(neighbour)
                distance[neighbour] = distance[current] + 1
                queue.append(neighbour)
    require(reached == live and max(distance.values()) == 89, "coarse live connectivity")

    ordinary = live - event_ids
    visited: set[str] = set()
    components: list[set[str]] = []
    for start in sorted(ordinary):
        if start in visited:
            continue
        component = {start}
        visited.add(start)
        queue = deque([start])
        while queue:
            current = queue.popleft()
            for neighbour in graph[current]:
                if neighbour in ordinary and neighbour not in visited:
                    visited.add(neighbour)
                    component.add(neighbour)
                    queue.append(neighbour)
        components.append(component)
    require(
        len(components) == 26
        and Counter(map(len, components)) == Counter({850: 2, 1: 24}),
        "ordinary component census",
    )
    components.sort(key=lambda value: (seed_id not in value, -len(value), min(value)))
    rows: list[dict[str, Any]] = []
    for index, component in enumerate(components):
        event_neighbours = {
            neighbour
            for cell_id in component
            for neighbour in graph[cell_id]
            if neighbour in event_ids
        }
        grazing_cells = {
            cell_id for cell_id in component
            if cells[cell_id]["physical_p_interval"][0] == "-1"
            or cells[cell_id]["physical_p_interval"][1] == "1"
        }
        cell_ids = sorted(component)
        rows.append({
            "schema": COMPONENT_ROW_SCHEMA,
            "component_index": index,
            "component_id": "c34-ordinary-component:" + digest(cell_ids),
            "cell_count": len(component),
            "cell_ids_sha256": digest(cell_ids),
            "origin_keys_sha256": digest(sorted(cells[cell_id]["origin_key"] for cell_id in component)),
            "chart_census": dict(sorted(Counter(cells[cell_id]["compact_chart"] for cell_id in component).items())),
            "contains_R1648_seed_coarse_cell": seed_id in component,
            "adjacent_typed_event_cell_count": len(event_neighbours),
            "adjacent_event_kind_census": dict(sorted(Counter(
                cells[cell_id]["inherited_event_graph"]["event_kind"]
                for cell_id in event_neighbours
            ).items())),
            "source_grazing_touch_cell_count": len(grazing_cells),
            "round144_terminal_class": "UNRESOLVED_R1648_CONTINUATION",
            "round144_terminal_credit": 0,
            "reason": (
                "C32 face connectivity does not certify the complete 1648-collision "
                "owner/word/chart/core path on the full ordinary cell"
            ),
        })
    return rows, {
        "live_cell_count": len(live),
        "live_event_cell_count": len(event_ids),
        "live_ordinary_cell_count": len(ordinary),
        "live_intra_chart_edge_count": edge_counts["INTRA_CHART"],
        "live_source_seam_edge_count": edge_counts["SOURCE_CHART_SEAM"],
        "coarse_live_component_count": 1,
        "coarse_seed_eccentricity": max(distance.values()),
        "ordinary_component_count_after_event_removal": len(components),
        "ordinary_component_size_census": {
            str(size): count for size, count in sorted(Counter(map(len, components)).items())
        },
    }


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_bytes(canonical(value) + b"\n")


def write_manifest(directory: Path) -> None:
    members = sorted(path for path in directory.iterdir() if path.name != "root_manifest.sha256")
    text = "".join(f"{file_sha256(path)}  {path.name}\n" for path in members)
    (directory / "root_manifest.sha256").write_text(text, encoding="utf-8")


def build(output: Path, c32: Path, c33: Path) -> dict[str, Any]:
    require(not output.exists(), f"output exists:{output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    stage = output.with_name(output.name + f".stage-{os.getpid()}")
    require(not stage.exists(), f"stage exists:{stage}")
    stage.mkdir()
    try:
        authorities = load_authorities()
        (
            c32_result, c33_result, cell_rows, adjacency_rows, seam_rows,
            event_rows, crosswalk_rows,
        ) = load_inputs(c32.resolve(), c33.resolve())
        cells = {row["cell_id"]: row for row in cell_rows}
        crosswalk = {row["cell_id"]: row for row in crosswalk_rows}
        require(len(cells) == len(crosswalk) == 76832, "cell/crosswalk cardinality")
        seed = seed_crosswalk(cell_rows, crosswalk, authorities)
        bindings = event_bindings(cells, crosswalk, event_rows, authorities)
        event_ids = {row["cell_id"] for row in bindings}
        component_rows, graph_census = graph_components(
            cells, crosswalk, adjacency_rows, seam_rows, event_ids, seed["cell_id"],
        )

        event_writer = LedgerWriter(
            stage / "typed_first_event_binding_ledger.jsonl.gz",
            "LEXICOGRAPHIC_SOURCE_W_ORIGIN_KEY",
        )
        with event_writer:
            for row in sorted(bindings, key=lambda value: value["origin_key"]):
                event_writer.write(row)

        component_writer = LedgerWriter(
            stage / "ordinary_component_ledger.jsonl.gz",
            "SEED_FIRST_THEN_SIZE_DESCENDING_THEN_CELL_ID",
        )
        with component_writer:
            for row in component_rows:
                component_writer.write(row)

        terminal_counts: Counter[str] = Counter()
        terminal_writer = LedgerWriter(
            stage / "round144_terminal_frontier.jsonl.gz",
            "LEXICOGRAPHIC_SOURCE_W_ORIGIN_KEY",
        )
        with terminal_writer:
            for cell in sorted(cell_rows, key=lambda value: value["origin_key"]):
                disposition = crosswalk[cell["cell_id"]]
                if disposition["formal_source_W_disposition"] == "EXCLUDED":
                    terminal_class = "EARLIEST_PREFIX_EXCLUDED"
                    credit = 1
                    authority = disposition["disposition_stage"]
                elif cell["cell_id"] in event_ids:
                    terminal_class = "TYPED_EVENT_GRAPH"
                    credit = 1
                    authority = cell["inherited_event_graph"]["event_kind"]
                else:
                    terminal_class = "UNRESOLVED_R1648_CONTINUATION"
                    credit = 0
                    authority = "NONE"
                terminal_counts[terminal_class] += 1
                terminal_writer.write({
                    "schema": TERMINAL_ROW_SCHEMA,
                    "origin_key": cell["origin_key"],
                    "cell_id": cell["cell_id"],
                    "compact_chart": cell["compact_chart"],
                    "terminal_class": terminal_class,
                    "terminal_credit": credit,
                    "authority": authority,
                    "strict_nonpromotion": {
                        "D02_credit": 0,
                        "D03_credit": 0,
                        "D04_credit": 0,
                    },
                })
        require(
            terminal_counts == Counter({
                "EARLIEST_PREFIX_EXCLUDED": 74812,
                "TYPED_EVENT_GRAPH": 296,
                "UNRESOLVED_R1648_CONTINUATION": 1724,
            }),
            "terminal frontier census",
        )

        write_json(stage / "r1648_seed_crosswalk.json", seed)
        (stage / "FRONTIER_ONLY.lock").write_text(
            "C34 does not authorize D02, D03, D04, Gate5, or CM2.\n",
            encoding="utf-8",
        )
        authority_pins = {
            label: {
                "path": str((DELIVERABLES / name).relative_to(ROOT)),
                "file_sha256": file_sha256(DELIVERABLES / name),
                "result_sha256": expected,
            }
            for label, (name, expected) in AUTHORITY_FILES.items()
        }
        result: dict[str, Any] = {
            "schema": SCHEMA,
            "status": (
                "PASS_C34_EXACT_R1648_SEED_CROSSWALK__296_TYPED_FIRST_EVENT_"
                "TERMINALS__26_ORDINARY_COMPONENTS__1724_R1648_CONTINUATIONS_"
                "UNRESOLVED__D02_STILL_BLOCKED"
            ),
            "C32_authority": {
                "path": str(c32.resolve().relative_to(ROOT)),
                "object_sha256": c32_result["object_sha256"],
            },
            "C33_authority": {
                "path": str(c33.resolve().relative_to(ROOT)),
                "object_sha256": c33_result["object_sha256"],
            },
            "R1648_seed_crosswalk": {
                "filename": "r1648_seed_crosswalk.json",
                "sha256": file_sha256(stage / "r1648_seed_crosswalk.json"),
                "seed_cell_id": seed["cell_id"],
                "seed_origin_key": seed["origin_key"],
                "adaptive_path_cell_id": seed["adaptive_path_cell_id"],
                "coarse_cell_connected_credit": 0,
            },
            "ledgers": {
                "typed_first_event_bindings": event_writer.descriptor(),
                "ordinary_components": component_writer.descriptor(),
                "terminal_frontier": terminal_writer.descriptor(),
            },
            "graph_census": graph_census,
            "round144_terminal_census": {
                "CONNECTED_TO_KNOWN": 0,
                "TYPED_EVENT_GRAPH": 296,
                "EARLIEST_PREFIX_EXCLUDED": 74812,
                "SOURCE_GRAZING_OR_CEMETERY": 0,
                "UNRESOLVED_R1648_CONTINUATION": 1724,
                "terminal_total": 76832,
                "unresolved_zero": False,
            },
            "strict_nonpromotion": {
                "D02": "BLOCKED_BY_1724_COMPLETE_R1648_CONTINUATIONS",
                "D03": "UNAUTHORIZED",
                "D04": "NOT_MINTED",
                "Gate5": "10/18",
                "complete_global_18_field_blocks": 0,
                "CM2": "NO-GO_FOR_CLAIM",
            },
            "required_next": (
                "common-refine the 1724 ordinary cells by every collision-2-through-1648 "
                "owner, discriminant, root-order, word, chart, wall, homogeneity, incidence, "
                "preterminal-core and terminal margin; attach regular strata to the Round140/161 "
                "component and type every first zero before any cemetery or D02 credit"
            ),
            "authority_pins": authority_pins,
        }
        result["object_sha256"] = digest(result)
        write_json(stage / "result.json", result)
        write_manifest(stage)
        stage.rename(output)
        return result
    except Exception:
        shutil.rmtree(stage, ignore_errors=True)
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--c32", type=Path)
    parser.add_argument("--c33", type=Path)
    args = parser.parse_args()
    c32 = args.c32 or (
        RUNTIME / "candidates" / (RUNTIME / "c32-current-token").read_text().strip()
    )
    c33 = args.c33 or (
        RUNTIME / "candidates" / (RUNTIME / "c33-current-token").read_text().strip()
    )
    result = build(args.output, c32, c33)
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
