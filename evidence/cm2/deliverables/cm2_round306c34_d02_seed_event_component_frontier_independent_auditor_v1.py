#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import json
import os
import sys
from collections import Counter, defaultdict, deque
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

ROOT = Path(__file__).resolve().parent.parent
DELIVERABLES = ROOT / "deliverables"
SCHEMA = "cm2.round306c34.d02-seed-event-component-frontier.v1"
AUDIT_SCHEMA = "cm2.round306c34.d02-seed-event-component-frontier-independent-audit.v1"
EXPECTED_C32_OBJECT = "32ff9e0f90a12f17b16f67086eabda0986a0d52d185bea0c5c16e20518ca1474"
EXPECTED_C33_OBJECT = "82dedeace982db89763e8a7e318fa6605d18cadc6bf390d6b23585d0922b87a0"
EXPECTED_STATUS = (
    "PASS_C34_EXACT_R1648_SEED_CROSSWALK__296_TYPED_FIRST_EVENT_"
    "TERMINALS__26_ORDINARY_COMPONENTS__1724_R1648_CONTINUATIONS_"
    "UNRESOLVED__D02_STILL_BLOCKED"
)


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
        value: dict[str, Any] = {}
        for key, item in pairs:
            require(key not in value, f"duplicate key:{path}:{key}")
            value[key] = item
        return value

    result = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=unique,
        parse_float=lambda value: (_ for _ in ()).throw(ValueError(value)),
        parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)),
    )
    require(type(result) is dict, f"top object:{path}")
    return result


def validate_manifest(directory: Path, expected_names: set[str] | None = None) -> None:
    rows = (directory / "root_manifest.sha256").read_text(encoding="utf-8").splitlines()
    require(rows, "manifest nonempty")
    names: set[str] = set()
    ordered_names: list[str] = []
    for row in rows:
        expected, name = row.split("  ", 1)
        require(name not in names, f"duplicate manifest member:{name}")
        names.add(name)
        ordered_names.append(name)
        path = directory / name
        require(path.is_file() and file_sha256(path) == expected, f"manifest:{name}")
    require(ordered_names == sorted(ordered_names), "manifest order")
    if expected_names is not None:
        require(names == expected_names, "manifest members")


def validate_object(value: dict[str, Any], field: str, expected: str | None, label: str) -> str:
    copy_value = dict(value)
    object_sha = copy_value.pop(field, None)
    require(type(object_sha) is str and object_sha == digest(copy_value), f"object:{label}")
    if expected is not None:
        require(object_sha == expected, f"expected object:{label}")
    return object_sha


def read_ledger(directory: Path, descriptor: dict[str, Any]) -> list[dict[str, Any]]:
    path = directory / descriptor["filename"]
    require(
        path.stat().st_size == descriptor["size"]
        and file_sha256(path) == descriptor["sha256"],
        f"ledger bytes:{path}",
    )
    rows: list[dict[str, Any]] = []
    sequence = hashlib.sha256()
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        for line in stream:
            row = json.loads(line)
            semantic = dict(row)
            row_sha = semantic.pop("row_sha256", None)
            require(row_sha == digest(semantic), f"row hash:{path}")
            rows.append(row)
            sequence.update((row_sha + "\n").encode("ascii"))
    require(len(rows) == descriptor["row_count"], f"row count:{path}")
    require(sequence.hexdigest() == descriptor["row_hash_line_sequence_sha256"], f"row sequence:{path}")
    return rows


def load_envelope(name: str) -> dict[str, Any]:
    value = strict_json(DELIVERABLES / name)
    require(value.get("result_sha256") == digest(value.get("result")), f"envelope:{name}")
    return value


def load_upstream(result: dict[str, Any]) -> tuple[
    Path, Path, dict[str, Any], dict[str, Any], list[dict[str, Any]],
    list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]],
    list[dict[str, Any]],
]:
    c32 = ROOT / result["C32_authority"]["path"]
    c33 = ROOT / result["C33_authority"]["path"]
    validate_manifest(c32)
    validate_manifest(c33)
    c32_result = strict_json(c32 / "result.json")
    c33_result = strict_json(c33 / "result.json")
    validate_object(c32_result, "object_sha256", EXPECTED_C32_OBJECT, "C32")
    validate_object(c33_result, "object_sha256", EXPECTED_C33_OBJECT, "C33")
    require(
        result["C32_authority"]["object_sha256"] == EXPECTED_C32_OBJECT
        and result["C33_authority"]["object_sha256"] == EXPECTED_C33_OBJECT,
        "upstream result bindings",
    )
    cells = read_ledger(c32, c32_result["ledgers"]["cells"])
    adjacency = read_ledger(c32, c32_result["ledgers"]["intra_chart_adjacency"])
    seams = read_ledger(c32, c32_result["ledgers"]["source_chart_seams"])
    events = read_ledger(c32, c32_result["ledgers"]["inherited_event_faces"])
    crosswalk = read_ledger(c33, c33_result["row_level_crosswalk"])
    return c32, c33, c32_result, c33_result, cells, adjacency, seams, events, crosswalk


def reconstruct_seed(
    cells: list[dict[str, Any]], crosswalk: dict[str, dict[str, Any]], candidate: Path,
) -> dict[str, Any]:
    materialization = load_envelope(
        "cm2-round140-round35-parent-w-r1648-materialization-audit-2026-07-24.json"
    )["result"]
    bridge = load_envelope(
        "cm2-round140-fixed-s-adaptive-component-identity-bridge-2026-07-24.json"
    )["result"]
    root = materialization["fixed_parameter_and_exact_implicit_leaf"]
    t_lower, t_upper = map(Q, root["deep_D0_root_bracket"])
    p_star = Q(root["fixed_p_star"])
    matches = []
    for cell in cells:
        if cell["gate3_chart"] != "W:E":
            continue
        t0, t1 = map(Q, cell["gate3_product_box"]["t"])
        p0, p1 = map(Q, cell["physical_p_interval"])
        if t0 < t_lower and t_upper < t1 and p0 < p_star < p1:
            matches.append(cell)
    require(len(matches) == 1 and matches[0]["origin_key"] == "W:E:04.07.0t0", "seed cell")
    cell = matches[0]
    require(
        crosswalk[cell["cell_id"]]["formal_source_W_disposition"] == "RESOLVED_NONEXCLUDED",
        "seed crosswalk disposition",
    )
    adaptive = bridge["fixed_s_adaptive_path_cell"]
    t0, t1 = map(Q, cell["gate3_product_box"]["t"])
    p0, p1 = map(Q, cell["physical_p_interval"])
    at0, at1 = map(Q, adaptive["t_open_interval"])
    ap0, ap1 = map(Q, adaptive["p_open_interval"])
    require(t0 < at0 < at1 < t1 and p0 < ap0 < ap1 < p1, "adaptive containment")
    recorded = strict_json(candidate / "r1648_seed_crosswalk.json")
    require(
        recorded["cell_id"] == cell["cell_id"]
        and recorded["origin_key"] == cell["origin_key"]
        and recorded["adaptive_path_cell_id"] == adaptive["adaptive_path_cell_id"]
        and recorded["coarse_cell_is_not_promoted_to_connected"] is True,
        "recorded seed crosswalk",
    )
    return recorded


def reconstruct_events(
    cells: dict[str, dict[str, Any]], crosswalk: dict[str, dict[str, Any]],
    event_rows: list[dict[str, Any]], bindings: list[dict[str, Any]],
) -> set[str]:
    round165 = load_envelope(
        "cm2_round165_adaptive_typed_seam_census_certificate.json"
    )["result"]
    round177 = load_envelope(
        "cm2_round177_tangency_boundary_and_source_seam_ledger_certificate.json"
    )["result"]
    typed = {
        row["leaf_key"]: row
        for row in round165["adaptive_seam_census"]["terminal_rows"]
        if row.get("typed_seam") is not None
    }
    tangency = {row["ambient_leaf_key"]: row for row in round177["exact_parent_rows"]}
    source_events = {row["incident_cell_id"]: row for row in event_rows}
    require(len(source_events) == 336 and len(bindings) == 296, "event cardinality")
    ids: set[str] = set()
    kinds: Counter[str] = Counter()
    for binding in bindings:
        cell_id = binding["cell_id"]
        require(cell_id not in ids and cell_id in source_events, "event identity")
        ids.add(cell_id)
        cell = cells[cell_id]
        source = source_events[cell_id]
        require(
            crosswalk[cell_id]["formal_source_W_disposition"] == "RESOLVED_NONEXCLUDED"
            and binding["origin_key"] == cell["origin_key"] == source["origin_key"]
            and binding["event_payload_sha256"] == digest(source["event_payload"])
            and binding["round144_terminal_class"] == "TYPED_EVENT_GRAPH"
            and binding["round144_terminal_credit"] == 1,
            "event semantics",
        )
        kind = binding["event_kind"]
        kinds[kind] += 1
        if kind == "ROUND165_TYPED_OUTGOING_CHART_SEAM_GRAPH":
            row = typed[cell["origin_key"]]
            require(
                binding["authority"]["source_row_sha256"] == digest(row)
                and binding["authority"]["typed_graph_sha256"] == digest(row["typed_seam"])
                and row["typed_seam"]["three_stratum_partition_materialized"] is True,
                "Round165 binding",
            )
        else:
            require(kind == "GATE3_PHYSICAL_FIRST_TANGENCY_GRAPH", "tangency kind")
            row = tangency[cell["origin_key"]]
            require(
                binding["authority"]["round177_row_sha256"] == row["row_sha256"]
                and row["parent_classification"] == "MIXED_BOUNDED_RESIDUAL"
                and row["distinguished_intersections"]["Delta_intersect_H"]["status"].startswith(
                    "EMPTY_CERTIFIED"
                ),
                "Round177 binding",
            )
    require(
        kinds == Counter({
            "ROUND165_TYPED_OUTGOING_CHART_SEAM_GRAPH": 280,
            "GATE3_PHYSICAL_FIRST_TANGENCY_GRAPH": 16,
        }),
        "event kind census",
    )
    return ids


def reconstruct_components(
    cells: dict[str, dict[str, Any]], crosswalk: dict[str, dict[str, Any]],
    adjacency: list[dict[str, Any]], seams: list[dict[str, Any]], event_ids: set[str],
    seed_id: str, recorded: list[dict[str, Any]],
) -> dict[str, Any]:
    live = {
        cell_id for cell_id, row in crosswalk.items()
        if row["formal_source_W_disposition"] == "RESOLVED_NONEXCLUDED"
    }
    graph: dict[str, set[str]] = defaultdict(set)
    edge_counts: Counter[str] = Counter()
    for kind, rows, left, right in (
        ("INTRA_CHART", adjacency, "negative_cell_id", "positive_cell_id"),
        ("SOURCE_CHART_SEAM", seams, "left_cell_id", "right_cell_id"),
    ):
        for row in rows:
            first, second = row[left], row[right]
            if first in live and second in live:
                graph[first].add(second)
                graph[second].add(first)
                edge_counts[kind] += 1
    reached = {seed_id}
    distance = {seed_id: 0}
    queue = deque([seed_id])
    while queue:
        current = queue.popleft()
        for neighbour in graph[current]:
            if neighbour not in reached:
                reached.add(neighbour)
                distance[neighbour] = distance[current] + 1
                queue.append(neighbour)
    require(reached == live and max(distance.values()) == 89, "coarse connectivity")
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
    components.sort(key=lambda value: (seed_id not in value, -len(value), min(value)))
    require(
        len(components) == len(recorded) == 26
        and Counter(map(len, components)) == Counter({850: 2, 1: 24}),
        "component sizes",
    )
    for index, (component, row) in enumerate(zip(components, recorded, strict=True)):
        ids = sorted(component)
        neighbours = {
            neighbour for cell_id in component for neighbour in graph[cell_id]
            if neighbour in event_ids
        }
        require(
            row["component_index"] == index
            and row["cell_count"] == len(component)
            and row["cell_ids_sha256"] == digest(ids)
            and row["origin_keys_sha256"] == digest(sorted(cells[cell_id]["origin_key"] for cell_id in component))
            and row["contains_R1648_seed_coarse_cell"] == (seed_id in component)
            and row["adjacent_typed_event_cell_count"] == len(neighbours)
            and row["round144_terminal_credit"] == 0,
            f"component row:{index}",
        )
    return {
        "live_cell_count": 2020,
        "live_event_cell_count": 296,
        "live_ordinary_cell_count": 1724,
        "live_intra_chart_edge_count": edge_counts["INTRA_CHART"],
        "live_source_seam_edge_count": edge_counts["SOURCE_CHART_SEAM"],
        "coarse_live_component_count": 1,
        "coarse_seed_eccentricity": 89,
        "ordinary_component_count_after_event_removal": 26,
        "ordinary_component_size_census": {"1": 24, "850": 2},
    }


def validate_summary(summary: dict[str, Any]) -> None:
    require(summary["seed_origin_key"] == "W:E:04.07.0t0", "summary seed")
    require(summary["excluded"] == 74812, "summary excluded")
    require(summary["typed_events"] == 296, "summary typed events")
    require(summary["typed_seams"] == 280 and summary["tangencies"] == 16, "summary event split")
    require(summary["unresolved"] == 1724, "summary unresolved")
    require(summary["component_sizes"] == {"1": 24, "850": 2}, "summary components")
    require(summary["unresolved_zero"] is False, "summary unresolved flag")
    require(summary["D02"] == "BLOCKED_BY_1724_COMPLETE_R1648_CONTINUATIONS", "summary D02")


def hostile_attacks(summary: dict[str, Any]) -> dict[str, Any]:
    mutations = {
        "seed_origin_swap": ("seed_origin_key", "W:E:04.07.0"),
        "excluded_count_tamper": ("excluded", 74811),
        "typed_event_count_tamper": ("typed_events", 295),
        "typed_seam_count_tamper": ("typed_seams", 279),
        "tangency_count_tamper": ("tangencies", 15),
        "unresolved_count_tamper": ("unresolved", 1723),
        "false_zero_unresolved": ("unresolved_zero", True),
        "illegal_D02_promotion": ("D02", "AUTHORIZED"),
    }
    passed: list[str] = []
    for name, (field, value) in mutations.items():
        candidate = copy.deepcopy(summary)
        candidate[field] = value
        try:
            validate_summary(candidate)
        except RuntimeError:
            passed.append(name)
        else:
            raise RuntimeError(f"attack accepted:{name}")
    return {"attack_count": len(mutations), "fail_closed_count": len(passed), "labels": passed}


def audit(candidate: Path) -> dict[str, Any]:
    validate_manifest(candidate, {
        "FRONTIER_ONLY.lock",
        "ordinary_component_ledger.jsonl.gz",
        "r1648_seed_crosswalk.json",
        "result.json",
        "round144_terminal_frontier.jsonl.gz",
        "typed_first_event_binding_ledger.jsonl.gz",
    })
    result = strict_json(candidate / "result.json")
    object_sha = validate_object(result, "object_sha256", None, "C34")
    require(result.get("schema") == SCHEMA and result.get("status") == EXPECTED_STATUS, "C34 identity")
    (
        _c32, _c33, _c32_result, _c33_result, cell_rows, adjacency, seams,
        event_rows, crosswalk_rows,
    ) = load_upstream(result)
    cells = {row["cell_id"]: row for row in cell_rows}
    crosswalk = {row["cell_id"]: row for row in crosswalk_rows}
    require(len(cells) == len(crosswalk) == 76832, "upstream cardinality")
    bindings = read_ledger(candidate, result["ledgers"]["typed_first_event_bindings"])
    components = read_ledger(candidate, result["ledgers"]["ordinary_components"])
    terminal = read_ledger(candidate, result["ledgers"]["terminal_frontier"])
    seed = reconstruct_seed(cell_rows, crosswalk, candidate)
    event_ids = reconstruct_events(cells, crosswalk, event_rows, bindings)
    graph_census = reconstruct_components(
        cells, crosswalk, adjacency, seams, event_ids, seed["cell_id"], components,
    )
    require(graph_census == result["graph_census"], "graph census result")

    terminal_counts = Counter(row["terminal_class"] for row in terminal)
    require(
        len(terminal) == 76832
        and terminal_counts == Counter({
            "EARLIEST_PREFIX_EXCLUDED": 74812,
            "TYPED_EVENT_GRAPH": 296,
            "UNRESOLVED_R1648_CONTINUATION": 1724,
        }),
        "terminal rows",
    )
    terminal_by_id = {row["cell_id"]: row for row in terminal}
    require(len(terminal_by_id) == 76832, "terminal unique IDs")
    for cell_id, disposition in crosswalk.items():
        row = terminal_by_id[cell_id]
        if disposition["formal_source_W_disposition"] == "EXCLUDED":
            expected = ("EARLIEST_PREFIX_EXCLUDED", 1)
        elif cell_id in event_ids:
            expected = ("TYPED_EVENT_GRAPH", 1)
        else:
            expected = ("UNRESOLVED_R1648_CONTINUATION", 0)
        require((row["terminal_class"], row["terminal_credit"]) == expected, "terminal assignment")
    require(
        result["round144_terminal_census"] == {
            "CONNECTED_TO_KNOWN": 0,
            "TYPED_EVENT_GRAPH": 296,
            "EARLIEST_PREFIX_EXCLUDED": 74812,
            "SOURCE_GRAZING_OR_CEMETERY": 0,
            "UNRESOLVED_R1648_CONTINUATION": 1724,
            "terminal_total": 76832,
            "unresolved_zero": False,
        },
        "terminal result census",
    )
    require(
        result["strict_nonpromotion"] == {
            "D02": "BLOCKED_BY_1724_COMPLETE_R1648_CONTINUATIONS",
            "D03": "UNAUTHORIZED",
            "D04": "NOT_MINTED",
            "Gate5": "10/18",
            "complete_global_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "strict nonpromotion",
    )
    summary = {
        "seed_origin_key": seed["origin_key"],
        "excluded": terminal_counts["EARLIEST_PREFIX_EXCLUDED"],
        "typed_events": terminal_counts["TYPED_EVENT_GRAPH"],
        "typed_seams": sum(row["event_kind"] == "ROUND165_TYPED_OUTGOING_CHART_SEAM_GRAPH" for row in bindings),
        "tangencies": sum(row["event_kind"] == "GATE3_PHYSICAL_FIRST_TANGENCY_GRAPH" for row in bindings),
        "unresolved": terminal_counts["UNRESOLVED_R1648_CONTINUATION"],
        "component_sizes": graph_census["ordinary_component_size_census"],
        "unresolved_zero": result["round144_terminal_census"]["unresolved_zero"],
        "D02": result["strict_nonpromotion"]["D02"],
    }
    validate_summary(summary)
    attacks = hostile_attacks(summary)
    audit_result: dict[str, Any] = {
        "schema": AUDIT_SCHEMA,
        "status": "PASS_INDEPENDENT_C34_RECONSTRUCTION__8_OF_8_ATTACKS_FAIL_CLOSED",
        "candidate_path": str(candidate.resolve().relative_to(ROOT)),
        "candidate_object_sha256": object_sha,
        "candidate_root_manifest_sha256": file_sha256(candidate / "root_manifest.sha256"),
        "reconstructed_summary": summary,
        "graph_census": graph_census,
        "hostile_attacks": attacks,
        "strict_conclusion": {
            "D02": "BLOCKED_BY_1724_COMPLETE_R1648_CONTINUATIONS",
            "D03": "UNAUTHORIZED",
            "D04": "NOT_MINTED",
            "Gate5": "10/18",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    audit_result["object_sha256"] = digest(audit_result)
    return audit_result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.candidate.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_name(args.output.name + f".tmp-{os.getpid()}")
    require(not temporary.exists(), "temporary output absent")
    temporary.write_bytes(canonical(result) + b"\n")
    temporary.rename(args.output)
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
