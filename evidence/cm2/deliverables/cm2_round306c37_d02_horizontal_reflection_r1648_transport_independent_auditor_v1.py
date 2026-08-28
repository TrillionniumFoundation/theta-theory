#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import json
import os
import sys
from collections import defaultdict, deque
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterable

import cm2_round173_source_g_exact_return_signature_transport as r173


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

ROOT = Path(__file__).resolve().parent.parent
DELIVERABLES = ROOT / "deliverables"
SCHEMA = "cm2.round306c37.d02-horizontal-reflection-r1648-transport.v1"
AUDIT_SCHEMA = (
    "cm2.round306c37.d02-horizontal-reflection-r1648-transport-independent-audit.v1"
)
EXPECTED_STATUS = (
    "PASS_C37_EXACT_HORIZONTAL_REFLECTION_TRANSPORT__"
    "26_COMPONENTS_TO_13_PAIRS__1724_CELLS_TO_862_PAIRS__"
    "REFLECTED_R1648_1648_OF_1648__146_GEOMETRY__214_WORDS__"
    "ZERO_COMMON_REFINEMENT_CREDIT"
)
EXPECTED_C36_OBJECT = "9251693da7d6cc0ff6011fb965276ac64be2b79be8f245ab8954291a43fb4167"
EXPECTED_C35_OBJECT = "cb524ae587390a578683c88d933125e041ab2a906f0351370d58f3b0d67aa752"
EXPECTED_C34_OBJECT = "1c75d245a20bac35a0e33249f921ee862ad3c1397e78817189699dcc28552d2e"
EXPECTED_C32_OBJECT = "32ff9e0f90a12f17b16f67086eabda0986a0d52d185bea0c5c16e20518ca1474"
EXPECTED_C33_OBJECT = "82dedeace982db89763e8a7e318fa6605d18cadc6bf390d6b23585d0922b87a0"
EXPECTED_R173_SOURCE = "bdbf794a99dc9276b11b7680818994d63f52fe0e5a857948701f64e8d5d16a0f"
GATE5_MANIFEST = DELIVERABLES / (
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
)
EXPECTED_GATE5_MANIFEST = (
    "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866"
)
RETURN_DEPTH = 1648
REFLECTED_DESTINATION_CORE = (
    "core:918cc822d8c651e9204626b632ad4178ef695ba5a5c66db972823eff8508aee3"
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
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


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
        parse_float=lambda item: (_ for _ in ()).throw(ValueError(item)),
        parse_constant=lambda item: (_ for _ in ()).throw(ValueError(item)),
    )
    require(type(value) is dict, f"top object:{path}")
    return value


def validate_object(
    value: dict[str, Any], field: str, expected: str | None, label: str,
) -> str:
    semantic = dict(value)
    recorded = semantic.pop(field, None)
    require(type(recorded) is str and recorded == digest(semantic), f"object:{label}")
    if expected is not None:
        require(recorded == expected, f"expected object:{label}")
    return recorded


def validate_manifest(directory: Path, expected_names: set[str] | None = None) -> None:
    rows = (directory / "root_manifest.sha256").read_text(
        encoding="utf-8"
    ).splitlines()
    names: list[str] = []
    for row in rows:
        expected, name = row.split("  ", 1)
        require(name not in names, f"duplicate manifest member:{name}")
        names.append(name)
        require(
            (directory / name).is_file()
            and file_sha256(directory / name) == expected,
            f"manifest member:{directory / name}",
        )
    require(names == sorted(names), f"manifest order:{directory}")
    if expected_names is not None:
        require(set(names) == expected_names, "manifest inventory")


def read_ledger(directory: Path, descriptor: dict[str, Any]) -> list[dict[str, Any]]:
    path = directory / descriptor["filename"]
    require(
        path.is_file()
        and path.stat().st_size == descriptor["size"]
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
            require(row_sha == digest(semantic), f"row closure:{path}")
            rows.append(row)
            sequence.update((row_sha + "\n").encode("ascii"))
    require(
        len(rows) == descriptor["row_count"]
        and sequence.hexdigest() == descriptor["row_hash_line_sequence_sha256"],
        f"ledger descriptor:{path}",
    )
    return rows


def coordinate_value(value: Any) -> str:
    text = value["value"] if type(value) is dict else value
    return "1/sqrt(2)" if text == "+1/sqrt(2)" else text


def negate_coordinate(value: str) -> str:
    value = coordinate_value(value)
    if value == "1/sqrt(2)":
        return "-1/sqrt(2)"
    if value == "-1/sqrt(2)":
        return "1/sqrt(2)"
    return str(-Q(value))


def reflected_chart(chart: str) -> str:
    return {"E": "E", "W": "W", "N": "S", "S": "N"}[chart]


def cell_signature(cell: dict[str, Any]) -> tuple[str, str, str, str, str]:
    t0, t1 = cell["physical_t_interval"]
    p0, p1 = cell["physical_p_interval"]
    return (
        cell["compact_chart"], coordinate_value(t0), coordinate_value(t1), p0, p1
    )


def reflect_signature(
    value: tuple[str, str, str, str, str],
) -> tuple[str, str, str, str, str]:
    chart, t0, t1, p0, p1 = value
    if chart in {"E", "W"}:
        t0, t1 = negate_coordinate(t1), negate_coordinate(t0)
    return (
        reflected_chart(chart), t0, t1,
        negate_coordinate(p1), negate_coordinate(p0),
    )


def parse_target(value: str) -> tuple[str, int, int]:
    obstacle = value[0]
    ix, iy = map(int, value[2:-1].split(","))
    return obstacle, ix, iy


def target_id(obstacle: str, ix: int, iy: int) -> str:
    return f"{obstacle}[{ix},{iy}]"


def reflect_absolute(value: str) -> str:
    obstacle, ix, iy = parse_target(value)
    return target_id(obstacle, ix, 1 - iy if obstacle == "G" else -iy)


def reflect_local(source: str, value: str) -> str:
    obstacle, ix, iy = parse_target(value)
    if source == "G":
        iy = -iy if obstacle == "G" else -iy - 1
    else:
        iy = 1 - iy if obstacle == "G" else -iy
    return target_id(obstacle, ix, iy)


def reflect_token(token: str) -> str:
    return {"Y-": "Y+", "Y+": "Y-"}.get(token, token)


def gate5_registry() -> dict[str, Any]:
    require(
        file_sha256(Path(r173.__file__)) == EXPECTED_R173_SOURCE
        and file_sha256(GATE5_MANIFEST) == EXPECTED_GATE5_MANIFEST,
        "registry source pins",
    )
    gate5 = strict_json(GATE5_MANIFEST)
    frozen = gate5["result"]["immutable_candidate_key_registry"]
    patterns = r173.crossing_patterns()
    pairs = tuple(
        (chart, target)
        for chart in r173.SOURCE_CHARTS
        for target in r173.candidate_ids(chart)
    )
    require(
        len(patterns) == 985
        and len(pairs) == 448
        and digest(pairs) == frozen["chart_target_pair_rows_sha256"],
        "registry pair census",
    )
    stream = hashlib.sha256()
    for chart, target in pairs:
        for pattern in patterns:
            stream.update(
                canonical([chart, target, list(pattern), len(pattern) + 1]) + b"\n"
            )
    require(stream.hexdigest() == frozen["candidate_word_key_rows_sha256"], "registry")
    return {
        "patterns": patterns,
        "pattern_index": {value: index for index, value in enumerate(patterns)},
        "pair_index": {value: index for index, value in enumerate(pairs)},
    }


def official_word_id(registry: dict[str, Any], row: list[Any]) -> str:
    pair = registry["pair_index"][(row[0], row[1])]
    pattern = registry["pattern_index"][tuple(row[2])]
    ordinal = pair * len(registry["patterns"]) + pattern
    require(row[3] == len(row[2]) + 1, "roof")
    return f"gate5-word:{ordinal:06d}:{digest(row)}"


def reconstruct_components(
    cells: dict[str, dict[str, Any]], crosswalk: dict[str, dict[str, Any]],
    adjacency: Iterable[dict[str, Any]], seams: Iterable[dict[str, Any]],
    event_ids: set[str], seed_id: str,
) -> tuple[list[set[str]], set[frozenset[str]]]:
    live = {
        cell_id for cell_id, row in crosswalk.items()
        if row["formal_source_W_disposition"] == "RESOLVED_NONEXCLUDED"
    }
    graph: dict[str, set[str]] = defaultdict(set)
    edges: set[frozenset[str]] = set()
    for rows, left, right in (
        (adjacency, "negative_cell_id", "positive_cell_id"),
        (seams, "left_cell_id", "right_cell_id"),
    ):
        for row in rows:
            first, second = row[left], row[right]
            if first in live and second in live:
                graph[first].add(second)
                graph[second].add(first)
                edges.add(frozenset((first, second)))
    ordinary = live - event_ids
    components: list[set[str]] = []
    seen: set[str] = set()
    for start in sorted(ordinary):
        if start in seen:
            continue
        component = {start}
        seen.add(start)
        queue = deque([start])
        while queue:
            current = queue.popleft()
            for neighbour in graph[current]:
                if neighbour in ordinary and neighbour not in seen:
                    seen.add(neighbour)
                    component.add(neighbour)
                    queue.append(neighbour)
        components.append(component)
    components.sort(key=lambda value: (seed_id not in value, -len(value), min(value)))
    require(len(components) == 26 and len(ordinary) == 1724, "component census")
    return components, edges


def validate_symmetry(
    result: dict[str, Any], cell_pairs: list[dict[str, Any]],
    component_pairs: list[dict[str, Any]],
) -> dict[str, Any]:
    c34 = ROOT / result["C36_authority"]["path"]
    c36_result = strict_json(c34 / "result.json")
    c34 = ROOT / c36_result["C34_authority"]["path"]
    c34_result = strict_json(c34 / "result.json")
    c32 = ROOT / c34_result["C32_authority"]["path"]
    c33 = ROOT / c34_result["C33_authority"]["path"]
    c32_result = strict_json(c32 / "result.json")
    c33_result = strict_json(c33 / "result.json")
    validate_object(c32_result, "object_sha256", EXPECTED_C32_OBJECT, "C32")
    validate_object(c33_result, "object_sha256", EXPECTED_C33_OBJECT, "C33")
    cells_rows = read_ledger(c32, c32_result["ledgers"]["cells"])
    adjacency = read_ledger(c32, c32_result["ledgers"]["intra_chart_adjacency"])
    seams = read_ledger(c32, c32_result["ledgers"]["source_chart_seams"])
    crosswalk_rows = read_ledger(c33, c33_result["row_level_crosswalk"])
    event_rows = read_ledger(
        c34, c34_result["ledgers"]["typed_first_event_bindings"]
    )
    cells = {row["cell_id"]: row for row in cells_rows}
    crosswalk = {row["cell_id"]: row for row in crosswalk_rows}
    event_ids = {row["cell_id"] for row in event_rows}
    seed = strict_json(c34 / "r1648_seed_crosswalk.json")
    components, edges = reconstruct_components(
        cells, crosswalk, adjacency, seams, event_ids, seed["cell_id"]
    )
    signature_index = {cell_signature(row): row["cell_id"] for row in cells_rows}
    require(len(signature_index) == len(cells_rows), "cell signature uniqueness")
    reflection = {
        cell_id: signature_index[reflect_signature(cell_signature(cell))]
        for cell_id, cell in cells.items()
    }
    require(
        all(reflection[reflection[cell_id]] == cell_id for cell_id in reflection),
        "reflection involution",
    )
    ordinary = set().union(*components)
    require(
        {reflection[cell_id] for cell_id in ordinary} == ordinary
        and {reflection[cell_id] for cell_id in event_ids} == event_ids
        and all(
            frozenset(reflection[cell_id] for cell_id in edge) in edges
            for edge in edges
        ),
        "graph reflection",
    )
    component_index = {
        cell_id: index for index, component in enumerate(components)
        for cell_id in component
    }
    expected_cell_pairs: set[tuple[str, str]] = set()
    for cell_id in ordinary:
        expected_cell_pairs.add(tuple(sorted((cell_id, reflection[cell_id]))))
    require(len(expected_cell_pairs) == 862 and len(cell_pairs) == 862, "cell pairs")
    candidate_cell_pairs: set[tuple[str, str]] = set()
    for row in cell_pairs:
        pair = (row["representative_cell_id"], row["reflected_cell_id"])
        require(
            pair == tuple(sorted(pair))
            and list(cell_signature(cells[pair[0]])) == row["representative_signature"]
            and list(cell_signature(cells[pair[1]])) == row["reflected_signature"]
            and list(reflect_signature(cell_signature(cells[pair[0]])))
            == row["expected_reflected_signature"]
            and row["representative_component_index"] == component_index[pair[0]]
            and row["reflected_component_index"] == component_index[pair[1]]
            and row["C34_common_refinement_credit"] == row["D02_credit"] == 0,
            "cell pair row",
        )
        candidate_cell_pairs.add(pair)
    require(candidate_cell_pairs == expected_cell_pairs, "cell pair exact cover")

    expected_component_pairs: set[tuple[int, int]] = set()
    for index, component in enumerate(components):
        partner = {
            component_index[reflection[cell_id]] for cell_id in component
        }
        require(len(partner) == 1, "component image")
        expected_component_pairs.add(tuple(sorted((index, partner.pop()))))
    require(
        len(expected_component_pairs) == len(component_pairs) == 13,
        "component pairs",
    )
    candidate_component_pairs = {
        (
            row["representative_component_index"],
            row["reflected_component_index"],
        )
        for row in component_pairs
    }
    require(candidate_component_pairs == expected_component_pairs, "component pair cover")
    mirror = result["reflected_seed_crosswalk"]
    require(
        mirror["original_seed_cell_id"] == seed["cell_id"]
        and mirror["reflected_seed_cell_id"] == reflection[seed["cell_id"]]
        and mirror["original_component_index"] == 0
        and mirror["reflected_component_index"] == 1
        and mirror["coarse_cell_is_not_promoted_to_connected"] is True,
        "mirror seed",
    )
    return {
        "live_edges": len(edges),
        "components": len(components),
        "component_pairs": len(expected_component_pairs),
        "ordinary_cells": len(ordinary),
        "cell_pairs": len(expected_cell_pairs),
        "event_cells": len(event_ids),
        "event_pairs": len(event_ids) // 2,
    }


def margin_summary(
    rows: list[dict[str, Any]], collar: str,
) -> dict[str, Any]:
    fields = tuple(rows[0]["collar_margin_vectors"][collar])
    result: dict[str, Any] = {}
    for field in fields:
        values = [row["collar_margin_vectors"][collar][field] for row in rows]
        finite = [value for value in values if value is not None]
        result[field] = {
            "finite_occurrence_count": len(finite),
            "null_inapplicable_occurrence_count": len(values) - len(finite),
            "minimum_dyadic_depth": min(finite) if finite else None,
            "maximum_dyadic_depth": max(finite) if finite else None,
        }
    return result


def validate_path(
    result: dict[str, Any], occurrences: list[dict[str, Any]],
    templates: list[dict[str, Any]], words: list[dict[str, Any]],
) -> dict[str, Any]:
    c36 = ROOT / result["C36_authority"]["path"]
    c36_result = strict_json(c36 / "result.json")
    validate_object(c36_result, "object_sha256", EXPECTED_C36_OBJECT, "C36")
    c35 = ROOT / c36_result["C35_authority"]["path"]
    c35_result = strict_json(c35 / "result.json")
    validate_object(c35_result, "object_sha256", EXPECTED_C35_OBJECT, "C35")
    bindings = read_ledger(
        c36, c36_result["ledgers"]["occurrence_margin_bindings"]
    )
    original_templates = read_ledger(
        c36, c36_result["ledgers"]["template_margin_atlas"]
    )
    original_words = read_ledger(
        c36, c36_result["ledgers"]["word_stratum_margin_atlas"]
    )
    source_occurrences = read_ledger(
        c35, c35_result["ledgers"]["path_occurrences"]
    )
    source_words = read_ledger(
        c35, c35_result["ledgers"]["official_word_variants"]
    )
    source_words_by_id = {
        row["official_word_variant_id"]: row for row in source_words
    }
    registry = gate5_registry()
    previous_owner = "W[0,0]"
    reflected_template_ids: set[str] = set()
    reflected_word_ids: set[str] = set()
    by_template: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_word: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for index, (candidate, source, binding) in enumerate(
        zip(occurrences, source_occurrences, bindings, strict=True), start=1
    ):
        word = source_words_by_id[source["official_word_variant_id"]]
        source_registry = word["official_registry_row"]
        obstacle = source["incoming_absolute_owner_id"][0]
        incoming_chart = reflected_chart(source["incoming_chart"])
        outgoing_chart = reflected_chart(source["outgoing_chart"])
        relative_target = reflect_local(obstacle, source["relative_frozen_target_id"])
        registry_row = [
            f"{obstacle}:{incoming_chart}",
            relative_target,
            [reflect_token(token) for token in source_registry[2]],
            source_registry[3],
        ]
        geometry_key = [obstacle, incoming_chart, relative_target, outgoing_chart]
        word_key = [*geometry_key, canonical(registry_row).decode("utf-8")]
        expected_geometry = "c35-r1648-geometry-template:" + digest(geometry_key)
        expected_word = "c35-r1648-official-word-variant:" + digest(word_key)
        incoming_owner = reflect_absolute(source["incoming_absolute_owner_id"])
        selected_owner = reflect_absolute(source["selected_absolute_owner_id"])
        destination = REFLECTED_DESTINATION_CORE if index == RETURN_DEPTH else None
        require(
            candidate["collision_index"] == index
            and candidate["original_occurrence_row_sha256"] == source["row_sha256"]
            and candidate["original_C36_margin_binding_row_sha256"]
            == binding["row_sha256"]
            and candidate["incoming_absolute_owner_id"] == incoming_owner == previous_owner
            and candidate["selected_absolute_owner_id"] == selected_owner
            and candidate["incoming_chart"] == incoming_chart
            and candidate["outgoing_chart"] == outgoing_chart
            and candidate["relative_frozen_target_id"] == relative_target
            and candidate["geometry_template_id"] == expected_geometry
            and candidate["official_word_variant_id"] == expected_word
            and candidate["official_registry_row"] == registry_row
            and candidate["official_registry_row_sha256"] == digest(registry_row)
            and candidate["official_word_key_id"]
            == official_word_id(registry, registry_row)
            and candidate["destination_core_id"] == destination
            and candidate["collar_margin_vectors"] == binding["collar_margin_vectors"]
            and candidate["collar_margin_vectors_sha256"]
            == binding["collar_margin_vectors_sha256"]
            and candidate["C34_common_refinement_credit"]
            == candidate["D02_credit"] == 0,
            f"reflected occurrence:{index}",
        )
        previous_owner = selected_owner
        reflected_template_ids.add(expected_geometry)
        reflected_word_ids.add(expected_word)
        by_template[expected_geometry].append(candidate)
        by_word[expected_word].append(candidate)
    require(previous_owner == "G[-7,14]", "terminal owner")
    require(len(templates) == len(by_template) == 137, "template census")
    require(len(words) == len(by_word) == 197, "word census")
    for row in templates:
        members = by_template[row["geometry_template_id"]]
        require(
            row["occurrence_indices"]
            == [member["collision_index"] for member in members]
            and row["margin_field_census_by_collar"] == {
                collar: margin_summary(members, collar)
                for collar in ("exact_half_open_graph", "positive_area_rectangle")
            }
            and row["C34_common_refinement_credit"] == row["D02_credit"] == 0,
            "template atlas row",
        )
    for row in words:
        members = by_word[row["official_word_variant_id"]]
        require(
            row["occurrence_indices"]
            == [member["collision_index"] for member in members]
            and row["official_registry_row"] == members[0]["official_registry_row"]
            and row["margin_field_census_by_collar"] == {
                collar: margin_summary(members, collar)
                for collar in ("exact_half_open_graph", "positive_area_rectangle")
            }
            and row["C34_common_refinement_credit"] == row["D02_credit"] == 0,
            "word atlas row",
        )
    original_template_ids = {
        row["geometry_template_id"] for row in original_templates
    }
    original_word_ids = {row["official_word_variant_id"] for row in original_words}
    return {
        "occurrences": len(occurrences),
        "reflected_templates": len(reflected_template_ids),
        "reflected_words": len(reflected_word_ids),
        "combined_templates": len(original_template_ids | reflected_template_ids),
        "combined_words": len(original_word_ids | reflected_word_ids),
        "new_templates": len(reflected_template_ids - original_template_ids),
        "new_words": len(reflected_word_ids - original_word_ids),
        "owner_sha256": digest(
            [row["selected_absolute_owner_id"] for row in occurrences]
        ),
        "word_sha256": digest([row["official_word_key_id"] for row in occurrences]),
    }


def validate_summary(summary: dict[str, Any]) -> None:
    require(summary["components"] == 26, "summary components")
    require(summary["component_pairs"] == 13, "summary component pairs")
    require(summary["ordinary_cells"] == 1724, "summary cells")
    require(summary["cell_pairs"] == 862, "summary cell pairs")
    require(summary["event_cells"] == 296, "summary events")
    require(summary["event_pairs"] == 148, "summary event pairs")
    require(summary["live_edges"] == 4016, "summary edges")
    require(summary["occurrences"] == 1648, "summary occurrences")
    require(summary["reflected_templates"] == 137, "summary reflected templates")
    require(summary["reflected_words"] == 197, "summary reflected words")
    require(summary["combined_templates"] == 146, "summary combined templates")
    require(summary["combined_words"] == 214, "summary combined words")
    require(summary["new_templates"] == 9, "summary new templates")
    require(summary["new_words"] == 17, "summary new words")
    require(summary["anchors"] == 2, "summary anchors")
    require(summary["common_refined"] == 0, "summary common refinement")
    require(summary["unresolved"] == 1724, "summary unresolved")
    require(summary["unresolved_zero"] is False, "summary unresolved zero")
    require(
        summary["D02"] == "BLOCKED_BY_1724_COMPLETE_R1648_CONTINUATIONS",
        "summary D02",
    )


def hostile_attacks(summary: dict[str, Any]) -> dict[str, str]:
    mutations = {
        "component_count_tamper": ("components", 25),
        "component_pair_tamper": ("component_pairs", 12),
        "ordinary_cell_tamper": ("ordinary_cells", 1723),
        "cell_pair_tamper": ("cell_pairs", 861),
        "event_cell_tamper": ("event_cells", 295),
        "event_pair_tamper": ("event_pairs", 147),
        "live_edge_tamper": ("live_edges", 4015),
        "occurrence_tamper": ("occurrences", 1647),
        "reflected_template_tamper": ("reflected_templates", 136),
        "reflected_word_tamper": ("reflected_words", 196),
        "combined_template_tamper": ("combined_templates", 145),
        "combined_word_tamper": ("combined_words", 213),
        "new_template_tamper": ("new_templates", 8),
        "new_word_tamper": ("new_words", 16),
        "false_anchor_whole_cell": ("anchors", 26),
        "false_common_refinement": ("common_refined", 1724),
        "false_unresolved_zero": ("unresolved_zero", True),
        "illegal_D02_promotion": ("D02", "AUTHORIZED"),
    }
    results: dict[str, str] = {}
    for name, (field, value) in mutations.items():
        mutated = copy.deepcopy(summary)
        mutated[field] = value
        try:
            validate_summary(mutated)
        except Exception:
            results[name] = "FAIL_CLOSED"
        else:
            raise RuntimeError(f"attack accepted:{name}")
    return results


def audit(candidate: Path, output: Path) -> dict[str, Any]:
    expected_names = {
        "REFLECTION_TRANSPORT_ONLY.lock",
        "ordinary_cell_reflection_pairs.jsonl.gz",
        "ordinary_component_reflection_pairs.jsonl.gz",
        "reflected_r1648_occurrences.jsonl.gz",
        "reflected_template_margin_atlas.jsonl.gz",
        "reflected_word_stratum_margin_atlas.jsonl.gz",
        "result.json",
    }
    validate_manifest(candidate, expected_names)
    result = strict_json(candidate / "result.json")
    object_sha = validate_object(result, "object_sha256", None, "C37")
    require(result.get("schema") == SCHEMA and result.get("status") == EXPECTED_STATUS, "C37")
    lock = (candidate / "REFLECTION_TRANSPORT_ONLY.lock").read_text(
        encoding="utf-8"
    )
    require("zero D02" in lock and "does not common-refine" in lock, "C37 lock")
    c36 = ROOT / result["C36_authority"]["path"]
    c36_result = strict_json(c36 / "result.json")
    validate_object(c36_result, "object_sha256", EXPECTED_C36_OBJECT, "C36")
    c34 = ROOT / c36_result["C34_authority"]["path"]
    c34_result = strict_json(c34 / "result.json")
    validate_object(c34_result, "object_sha256", EXPECTED_C34_OBJECT, "C34")

    cell_pairs = read_ledger(
        candidate, result["ledgers"]["ordinary_cell_reflection_pairs"]
    )
    component_pairs = read_ledger(
        candidate, result["ledgers"]["ordinary_component_reflection_pairs"]
    )
    occurrences = read_ledger(
        candidate, result["ledgers"]["reflected_r1648_occurrences"]
    )
    templates = read_ledger(
        candidate, result["ledgers"]["reflected_template_margin_atlas"]
    )
    words = read_ledger(
        candidate, result["ledgers"]["reflected_word_stratum_margin_atlas"]
    )
    graph = validate_symmetry(result, cell_pairs, component_pairs)
    path = validate_path(result, occurrences, templates, words)
    strict = result["strict_nonpromotion"]
    summary = {
        **graph,
        **path,
        "anchors": strict["ordinary_components_with_strict_R1648_seed_collar_anchor"],
        "common_refined": strict["C34_common_refined_cell_count"],
        "unresolved": strict["C34_unresolved_R1648_continuations"],
        "unresolved_zero": strict["four_class_terminal_census_unresolved_zero"],
        "D02": strict["D02"],
    }
    validate_summary(summary)
    require(
        path["owner_sha256"]
        == "946d3f8b2b21228e6cace189551111c764248877de15d7471289ba4c04d204b5"
        and path["word_sha256"]
        == "0927133ad517762da6e3fc27151cdeae616e0311cecfe518f0cc540da693cd0e",
        "path identity",
    )
    attacks = hostile_attacks(summary)
    require(len(attacks) == 18 and set(attacks.values()) == {"FAIL_CLOSED"}, "attacks")
    receipt: dict[str, Any] = {
        "schema": AUDIT_SCHEMA,
        "status": "PASS_INDEPENDENT_C37_RECONSTRUCTION__18_OF_18_ATTACKS_FAIL_CLOSED",
        "candidate_path": str(candidate.resolve().relative_to(ROOT)),
        "candidate_object_sha256": object_sha,
        "candidate_status": result["status"],
        "independently_reconstructed_summary": summary,
        "hostile_attacks": attacks,
        "strict_nonpromotion": strict,
    }
    receipt["object_sha256"] = digest(receipt)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(output.name + f".stage-{os.getpid()}")
    temporary.write_bytes(canonical(receipt) + b"\n")
    temporary.replace(output)
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.candidate.resolve(), args.output.resolve())
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
