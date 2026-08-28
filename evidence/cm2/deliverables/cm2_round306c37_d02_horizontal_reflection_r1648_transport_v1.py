#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import shutil
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
RUNTIME = ROOT / ".cm2-runtime"
SCHEMA = "cm2.round306c37.d02-horizontal-reflection-r1648-transport.v1"
CELL_PAIR_SCHEMA = "cm2.round306c37.ordinary-cell-horizontal-reflection-pair.v1"
COMPONENT_PAIR_SCHEMA = (
    "cm2.round306c37.ordinary-component-horizontal-reflection-pair.v1"
)
OCCURRENCE_SCHEMA = "cm2.round306c37.reflected-r1648-occurrence.v1"
TEMPLATE_SCHEMA = "cm2.round306c37.reflected-template-margin-atlas-row.v1"
WORD_SCHEMA = "cm2.round306c37.reflected-word-stratum-margin-atlas-row.v1"

EXPECTED_C36_OBJECT = "9251693da7d6cc0ff6011fb965276ac64be2b79be8f245ab8954291a43fb4167"
EXPECTED_C36_AUDIT_OBJECT = (
    "bc87269deb385ec19fe94003512c7d15e5b4fbf2fc0e5d20af4cc07adeaab273"
)
EXPECTED_C35_OBJECT = "cb524ae587390a578683c88d933125e041ab2a906f0351370d58f3b0d67aa752"
EXPECTED_C34_OBJECT = "1c75d245a20bac35a0e33249f921ee862ad3c1397e78817189699dcc28552d2e"
EXPECTED_C32_OBJECT = "32ff9e0f90a12f17b16f67086eabda0986a0d52d185bea0c5c16e20518ca1474"
EXPECTED_C33_OBJECT = "82dedeace982db89763e8a7e318fa6605d18cadc6bf390d6b23585d0922b87a0"
EXPECTED_R173_SOURCE = "bdbf794a99dc9276b11b7680818994d63f52fe0e5a857948701f64e8d5d16a0f"
EXPECTED_GATE5_MANIFEST = (
    "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866"
)
EXPECTED_GATE3_SOURCE = "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da"
EXPECTED_GATE3_MANIFEST = (
    "f8fda665edbb7d8b39ce495188f90ecb2b5ec4384c1eb958949627df167c4987"
)
GATE5_MANIFEST = DELIVERABLES / (
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
)
GATE3_SOURCE = DELIVERABLES / "cm2_gate3_eight_cell_symmetry_atlas_cert.py"
GATE3_MANIFEST = DELIVERABLES / (
    "cm2-gate3-eight-cell-symmetry-atlas-manifest-2026-07-15.json"
)
RETURN_DEPTH = 1648
ORIGINAL_SOURCE_CORE = (
    "core:90398e9ab632e57b027266bc7c34461a0a6a6d308c35fbeacc41432a3d7f48f7"
)
ORIGINAL_DESTINATION_CORE = (
    "core:e47f553e056452faa012129434cdbbb6a55cd9671a19ea04e6b8a9f43054c4c2"
)
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
    value: dict[str, Any], field: str, expected: str, label: str,
) -> None:
    semantic = dict(value)
    recorded = semantic.pop(field, None)
    require(recorded == expected == digest(semantic), f"object:{label}")


def validate_manifest(directory: Path) -> None:
    rows = (directory / "root_manifest.sha256").read_text(
        encoding="utf-8"
    ).splitlines()
    names: list[str] = []
    for row in rows:
        expected, name = row.split("  ", 1)
        require(name not in names, f"manifest duplicate:{name}")
        names.append(name)
        require(
            (directory / name).is_file()
            and file_sha256(directory / name) == expected,
            f"manifest member:{directory / name}",
        )
    require(names == sorted(names), f"manifest order:{directory}")


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


class LedgerWriter:
    def __init__(self, path: Path, order: str) -> None:
        self.path = path
        self.order = order
        self.count = 0
        self.sequence = hashlib.sha256()
        self.raw: Any = None
        self.stream: Any = None

    def __enter__(self) -> LedgerWriter:
        self.raw = self.path.open("wb")
        self.stream = gzip.GzipFile(
            filename="", mode="wb", fileobj=self.raw, mtime=0
        )
        return self

    def write(self, row: dict[str, Any]) -> None:
        require("row_sha256" not in row, "writer row open")
        row_sha = digest(row)
        self.stream.write(canonical({**row, "row_sha256": row_sha}) + b"\n")
        self.sequence.update((row_sha + "\n").encode("ascii"))
        self.count += 1

    def __exit__(self, *_args: Any) -> None:
        self.stream.close()
        self.raw.close()

    def descriptor(self) -> dict[str, Any]:
        return {
            "filename": self.path.name,
            "order": self.order,
            "row_count": self.count,
            "row_hash_line_sequence_sha256": self.sequence.hexdigest(),
            "sha256": file_sha256(self.path),
            "size": self.path.stat().st_size,
        }


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
        cell["compact_chart"],
        coordinate_value(t0),
        coordinate_value(t1),
        p0,
        p1,
    )


def reflected_cell_signature(
    signature: tuple[str, str, str, str, str],
) -> tuple[str, str, str, str, str]:
    chart, t0, t1, p0, p1 = signature
    if chart in {"E", "W"}:
        t0, t1 = negate_coordinate(t1), negate_coordinate(t0)
    return (
        reflected_chart(chart),
        t0,
        t1,
        negate_coordinate(p1),
        negate_coordinate(p0),
    )


def parse_target(value: str) -> tuple[str, int, int]:
    obstacle = value[0]
    ix, iy = map(int, value[2:-1].split(","))
    return obstacle, ix, iy


def target_id(obstacle: str, ix: int, iy: int) -> str:
    return f"{obstacle}[{ix},{iy}]"


def reflect_absolute_target(value: str) -> str:
    obstacle, ix, iy = parse_target(value)
    iy = 1 - iy if obstacle == "G" else -iy
    return target_id(obstacle, ix, iy)


def reflect_local_target(source: str, value: str) -> str:
    obstacle, ix, iy = parse_target(value)
    if source == "G":
        iy = -iy if obstacle == "G" else -iy - 1
    else:
        iy = 1 - iy if obstacle == "G" else -iy
    return target_id(obstacle, ix, iy)


def reflect_token(token: str) -> str:
    require(token in {"X-", "X+", "Y-", "Y+"}, "wall token")
    return {"Y-": "Y+", "Y+": "Y-"}.get(token, token)


def core_payload_id(payload: dict[str, Any]) -> str:
    return "core:" + digest(payload)


def reflected_terminal_core() -> dict[str, Any]:
    original = {
        "chart_id": "G:S",
        "t": ["69/100", "7/10"],
        "p": ["-1/50", "1/50"],
        "target_id": "W[0,-1]",
        "crossings": [],
    }
    reflected = {
        "chart_id": "G:N",
        "t": ["69/100", "7/10"],
        "p": ["-1/50", "1/50"],
        "target_id": "W[0,0]",
        "crossings": [],
    }
    require(
        core_payload_id(original) == ORIGINAL_DESTINATION_CORE
        and core_payload_id(reflected) == REFLECTED_DESTINATION_CORE,
        "terminal core reflection",
    )
    return {
        "generator": "Jy",
        "original_core_id": ORIGINAL_DESTINATION_CORE,
        "original_core_payload": original,
        "reflected_core_id": REFLECTED_DESTINATION_CORE,
        "reflected_core_payload": reflected,
        "chart_map": "S_TO_N",
        "t_map": "t",
        "p_map": "-p",
        "target_map": "W[0,-1]_TO_W[0,0]",
        "coefficientwise_core_payload_transport": True,
    }


def build_gate5_registry() -> dict[str, Any]:
    require(
        file_sha256(Path(r173.__file__)) == EXPECTED_R173_SOURCE,
        "Round173 source pin",
    )
    require(
        file_sha256(GATE5_MANIFEST) == EXPECTED_GATE5_MANIFEST
        and file_sha256(GATE3_SOURCE) == EXPECTED_GATE3_SOURCE
        and file_sha256(GATE3_MANIFEST) == EXPECTED_GATE3_MANIFEST,
        "reflection authority pins",
    )
    gate5 = strict_json(GATE5_MANIFEST)
    registry = gate5["result"]["immutable_candidate_key_registry"]
    patterns = r173.crossing_patterns()
    pairs = tuple(
        (chart, target)
        for chart in r173.SOURCE_CHARTS
        for target in r173.candidate_ids(chart)
    )
    require(
        len(patterns) == 985
        and len(pairs) == 448
        and digest(pairs) == registry["chart_target_pair_rows_sha256"],
        "Gate5 pair-pattern registry",
    )
    stream = hashlib.sha256()
    count = 0
    for chart, target in pairs:
        for pattern in patterns:
            row = [chart, target, list(pattern), len(pattern) + 1]
            stream.update(canonical(row) + b"\n")
            count += 1
    require(
        count == registry["candidate_return_word_key_count"] == 441280
        and stream.hexdigest() == registry["candidate_word_key_rows_sha256"],
        "Gate5 full registry digest",
    )
    return {
        "patterns": patterns,
        "pattern_index": {pattern: index for index, pattern in enumerate(patterns)},
        "pairs": pairs,
        "pair_index": {pair: index for index, pair in enumerate(pairs)},
        "candidate_word_key_rows_sha256": stream.hexdigest(),
    }


def official_word_id(registry: dict[str, Any], row: list[Any]) -> str:
    pair_index = registry["pair_index"][(row[0], row[1])]
    pattern_index = registry["pattern_index"][tuple(row[2])]
    ordinal = pair_index * len(registry["patterns"]) + pattern_index
    require(row[3] == len(row[2]) + 1, "roof grammar")
    return f"gate5-word:{ordinal:06d}:{digest(row)}"


def reconstruct_components(
    cells: dict[str, dict[str, Any]], crosswalk: dict[str, dict[str, Any]],
    adjacency: Iterable[dict[str, Any]], seams: Iterable[dict[str, Any]],
    event_ids: set[str], seed_id: str,
) -> tuple[list[set[str]], set[frozenset[str]]]:
    live = {
        cell_id
        for cell_id, row in crosswalk.items()
        if row["formal_source_W_disposition"] == "RESOLVED_NONEXCLUDED"
    }
    require(len(live) == 2020 and len(event_ids) == 296, "live cell census")
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
    visited: set[str] = set()
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
        len(components) == 26
        and sorted(map(len, components)) == [1] * 24 + [850, 850],
        "ordinary component census",
    )
    return components, edges


def build_symmetry_rows(
    c32: Path, c32_result: dict[str, Any], c33: Path,
    c33_result: dict[str, Any], c34: Path, c34_result: dict[str, Any],
) -> tuple[
    list[dict[str, Any]], list[dict[str, Any]], dict[str, Any], dict[str, Any]
]:
    cells_rows = read_ledger(c32, c32_result["ledgers"]["cells"])
    adjacency = read_ledger(c32, c32_result["ledgers"]["intra_chart_adjacency"])
    seams = read_ledger(c32, c32_result["ledgers"]["source_chart_seams"])
    crosswalk_rows = read_ledger(c33, c33_result["row_level_crosswalk"])
    event_rows = read_ledger(
        c34, c34_result["ledgers"]["typed_first_event_bindings"]
    )
    component_source = read_ledger(
        c34, c34_result["ledgers"]["ordinary_components"]
    )
    cells = {row["cell_id"]: row for row in cells_rows}
    crosswalk = {row["cell_id"]: row for row in crosswalk_rows}
    event_ids = {row["cell_id"] for row in event_rows}
    seed = strict_json(c34 / "r1648_seed_crosswalk.json")
    components, live_edges = reconstruct_components(
        cells, crosswalk, adjacency, seams, event_ids, seed["cell_id"]
    )
    for source, component in zip(component_source, components, strict=True):
        ids = sorted(component)
        require(
            source["component_index"] == component_source.index(source)
            and source["component_id"] == "c34-ordinary-component:" + digest(ids)
            and source["cell_ids_sha256"] == digest(ids),
            "C34 component reconstruction",
        )

    signature_index: dict[tuple[str, str, str, str, str], str] = {}
    for cell in cells_rows:
        signature = cell_signature(cell)
        require(signature not in signature_index, "unique C32 cell signature")
        signature_index[signature] = cell["cell_id"]
    reflection: dict[str, str] = {}
    for cell_id, cell in cells.items():
        mapped = signature_index.get(reflected_cell_signature(cell_signature(cell)))
        require(mapped is not None, f"closed cell reflection:{cell_id}")
        reflection[cell_id] = mapped
    require(
        all(reflection[reflection[cell_id]] == cell_id for cell_id in reflection),
        "cell reflection involution",
    )
    ordinary_ids = set().union(*components)
    require(
        {reflection[cell_id] for cell_id in ordinary_ids} == ordinary_ids
        and {reflection[cell_id] for cell_id in event_ids} == event_ids,
        "ordinary and event reflection closure",
    )
    for edge in live_edges:
        mapped = frozenset(reflection[cell_id] for cell_id in edge)
        require(mapped in live_edges, "live graph reflection")

    component_index = {
        cell_id: index for index, component in enumerate(components)
        for cell_id in component
    }
    component_pairs: list[dict[str, Any]] = []
    seen_components: set[int] = set()
    for index, component in enumerate(components):
        partner_set = {reflection[cell_id] for cell_id in component}
        partner_indices = {component_index[cell_id] for cell_id in partner_set}
        require(len(partner_indices) == 1, "component reflection image")
        partner = partner_indices.pop()
        require(partner_set == components[partner], "whole component reflection")
        if index in seen_components:
            continue
        require(partner != index, "no fixed ordinary component")
        representative, image = sorted((index, partner))
        seen_components.update((representative, image))
        component_pairs.append({
            "schema": COMPONENT_PAIR_SCHEMA,
            "pair_index": len(component_pairs),
            "representative_component_index": representative,
            "representative_component_id":
                component_source[representative]["component_id"],
            "reflected_component_index": image,
            "reflected_component_id": component_source[image]["component_id"],
            "cell_count_per_component": len(components[representative]),
            "representative_cell_ids_sha256": digest(
                sorted(components[representative])
            ),
            "reflected_cell_ids_sha256": digest(sorted(components[image])),
            "reflection_is_bijective_involution": True,
            "ordinary_graph_adjacency_preserved": True,
            "C34_common_refinement_credit": 0,
            "D02_credit": 0,
        })
    require(len(component_pairs) == 13, "component pair count")

    cell_pairs: list[dict[str, Any]] = []
    seen_cells: set[str] = set()
    for cell_id in sorted(ordinary_ids):
        if cell_id in seen_cells:
            continue
        partner = reflection[cell_id]
        require(partner != cell_id, "no fixed ordinary cell")
        representative, image = sorted((cell_id, partner))
        seen_cells.update((representative, image))
        left, right = cells[representative], cells[image]
        cell_pairs.append({
            "schema": CELL_PAIR_SCHEMA,
            "pair_index": len(cell_pairs),
            "representative_cell_id": representative,
            "representative_origin_key": left["origin_key"],
            "representative_component_index": component_index[representative],
            "representative_signature": list(cell_signature(left)),
            "reflected_cell_id": image,
            "reflected_origin_key": right["origin_key"],
            "reflected_component_index": component_index[image],
            "reflected_signature": list(cell_signature(right)),
            "expected_reflected_signature": list(
                reflected_cell_signature(cell_signature(left))
            ),
            "reflection_formula": {
                "physical": "(x,y,p)->(x,1-y,-p)",
                "chart": "E->E,W->W,N<->S",
                "t_by_chart": "-t_on_E_W__t_on_N_S",
                "p": "-p",
            },
            "cell_row_sha256_pair": [left["row_sha256"], right["row_sha256"]],
            "reflection_is_bijective_involution": True,
            "C34_common_refinement_credit": 0,
            "D02_credit": 0,
        })
    require(len(cell_pairs) == 862, "ordinary cell pair count")
    reflected_seed_id = reflection[seed["cell_id"]]
    mirror_seed = cells[reflected_seed_id]
    mirror = {
        "original_seed_cell_id": seed["cell_id"],
        "original_seed_origin_key": seed["origin_key"],
        "reflected_seed_cell_id": reflected_seed_id,
        "reflected_seed_origin_key": mirror_seed["origin_key"],
        "original_component_index": component_index[seed["cell_id"]],
        "reflected_component_index": component_index[reflected_seed_id],
        "reflected_open_collar_strictly_inside_coarse_cell": True,
        "coarse_cell_is_not_promoted_to_connected": True,
    }
    graph_summary = {
        "live_edge_count": len(live_edges),
        "ordinary_component_count": len(components),
        "ordinary_cell_count": len(ordinary_ids),
        "typed_event_cell_count": len(event_ids),
        "ordinary_component_reflection_pair_count": len(component_pairs),
        "ordinary_cell_reflection_pair_count": len(cell_pairs),
        "typed_event_reflection_pair_count": len(event_ids) // 2,
        "all_live_edges_reflection_closed": True,
    }
    return cell_pairs, component_pairs, mirror, graph_summary


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


def build_reflected_path(
    c36: Path, c36_result: dict[str, Any], c35: Path,
    c35_result: dict[str, Any], registry: dict[str, Any],
) -> tuple[
    list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]],
    dict[str, Any]
]:
    bindings = read_ledger(
        c36, c36_result["ledgers"]["occurrence_margin_bindings"]
    )
    original_templates = read_ledger(
        c36, c36_result["ledgers"]["template_margin_atlas"]
    )
    original_words = read_ledger(
        c36, c36_result["ledgers"]["word_stratum_margin_atlas"]
    )
    c35_occurrences = read_ledger(
        c35, c35_result["ledgers"]["path_occurrences"]
    )
    c35_words = read_ledger(
        c35, c35_result["ledgers"]["official_word_variants"]
    )
    words_by_id = {row["official_word_variant_id"]: row for row in c35_words}
    original_template_ids = {row["geometry_template_id"] for row in original_templates}
    original_word_ids = {row["official_word_variant_id"] for row in original_words}
    reflected: list[dict[str, Any]] = []
    previous_owner = "W[0,0]"
    for index, (binding, occurrence) in enumerate(
        zip(bindings, c35_occurrences, strict=True), start=1
    ):
        source_word = words_by_id[occurrence["official_word_variant_id"]]
        source_registry = source_word["official_registry_row"]
        source = occurrence["incoming_absolute_owner_id"][0]
        incoming_chart = reflected_chart(occurrence["incoming_chart"])
        outgoing_chart = reflected_chart(occurrence["outgoing_chart"])
        relative_target = reflect_local_target(
            source, occurrence["relative_frozen_target_id"]
        )
        reflected_registry = [
            f"{source}:{incoming_chart}",
            relative_target,
            [reflect_token(token) for token in source_registry[2]],
            source_registry[3],
        ]
        reflected_word_key_id = official_word_id(registry, reflected_registry)
        geometry_key = [source, incoming_chart, relative_target, outgoing_chart]
        word_key = [*geometry_key, canonical(reflected_registry).decode("utf-8")]
        incoming_owner = reflect_absolute_target(
            occurrence["incoming_absolute_owner_id"]
        )
        selected_owner = reflect_absolute_target(
            occurrence["selected_absolute_owner_id"]
        )
        require(incoming_owner == previous_owner, f"reflected recurrence:{index}")
        destination = (
            REFLECTED_DESTINATION_CORE
            if occurrence["destination_core_id"] == ORIGINAL_DESTINATION_CORE
            else None
        )
        require(
            (index < RETURN_DEPTH and destination is None)
            or (index == RETURN_DEPTH and destination == REFLECTED_DESTINATION_CORE),
            f"reflected core classification:{index}",
        )
        reflected.append({
            "schema": OCCURRENCE_SCHEMA,
            "collision_index": index,
            "original_occurrence_row_sha256": occurrence["row_sha256"],
            "original_C36_margin_binding_row_sha256": binding["row_sha256"],
            "incoming_absolute_owner_id": incoming_owner,
            "selected_absolute_owner_id": selected_owner,
            "incoming_chart": incoming_chart,
            "outgoing_chart": outgoing_chart,
            "relative_frozen_target_id": relative_target,
            "geometry_template_id":
                "c35-r1648-geometry-template:" + digest(geometry_key),
            "official_word_variant_id":
                "c35-r1648-official-word-variant:" + digest(word_key),
            "official_word_key_id": reflected_word_key_id,
            "official_registry_row": reflected_registry,
            "official_registry_row_sha256": digest(reflected_registry),
            "C24_classification": occurrence["C24_classification"],
            "destination_core_id": destination,
            "collar_candidate_census": binding["collar_candidate_census"],
            "collar_margin_vectors": binding["collar_margin_vectors"],
            "collar_margin_vectors_sha256":
                binding["collar_margin_vectors_sha256"],
            "horizontal_reflection_preserves_all_strict_margin_values": True,
            "owner_discriminant_root_order_word_chart_core_map_status":
                "MATERIALIZED_ON_REFLECTED_DUAL_R139_SEED_COLLARS",
            "C34_common_refinement_credit": 0,
            "D02_credit": 0,
        })
        previous_owner = selected_owner
    require(previous_owner == "G[-7,14]", "reflected terminal owner")

    by_template: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_word: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in reflected:
        by_template[row["geometry_template_id"]].append(row)
        by_word[row["official_word_variant_id"]].append(row)
    template_rows: list[dict[str, Any]] = []
    for template_id in sorted(by_template):
        rows = by_template[template_id]
        first = rows[0]
        indices = [row["collision_index"] for row in rows]
        variant_ids = sorted({row["official_word_variant_id"] for row in rows})
        original_ids = sorted({
            c35_occurrences[index - 1]["geometry_template_id"] for index in indices
        })
        require(len(original_ids) == 1, "reflected template source uniqueness")
        template_rows.append({
            "schema": TEMPLATE_SCHEMA,
            "geometry_template_id": template_id,
            "original_geometry_template_id": original_ids[0],
            "source_obstacle": first["incoming_absolute_owner_id"][0],
            "incoming_chart": first["incoming_chart"],
            "relative_frozen_target_id": first["relative_frozen_target_id"],
            "outgoing_chart": first["outgoing_chart"],
            "occurrence_count": len(rows),
            "occurrence_indices": indices,
            "occurrence_indices_sha256": digest(indices),
            "official_word_variant_count": len(variant_ids),
            "official_word_variant_ids_sha256": digest(variant_ids),
            "contains_collision_2": 2 in indices,
            "margin_field_census_by_collar": {
                collar: margin_summary(rows, collar)
                for collar in ("exact_half_open_graph", "positive_area_rectangle")
            },
            "atlas_scope": "HORIZONTAL_REFLECTION_OF_DUAL_R139_SEED_COLLARS",
            "template_atlas_status": "MATERIALIZED_BY_EXACT_JY_TRANSPORT",
            "C34_common_refinement_credit": 0,
            "D02_credit": 0,
        })
    word_rows: list[dict[str, Any]] = []
    for word_id in sorted(by_word):
        rows = by_word[word_id]
        first = rows[0]
        indices = [row["collision_index"] for row in rows]
        registries = {canonical(row["official_registry_row"]) for row in rows}
        original_ids = sorted({
            c35_occurrences[index - 1]["official_word_variant_id"]
            for index in indices
        })
        require(
            len(registries) == len(original_ids) == 1,
            "reflected word source uniqueness",
        )
        word_rows.append({
            "schema": WORD_SCHEMA,
            "official_word_variant_id": word_id,
            "original_official_word_variant_id": original_ids[0],
            "geometry_template_id": first["geometry_template_id"],
            "official_registry_row": first["official_registry_row"],
            "official_registry_row_sha256":
                first["official_registry_row_sha256"],
            "occurrence_count": len(rows),
            "occurrence_indices": indices,
            "occurrence_indices_sha256": digest(indices),
            "margin_field_census_by_collar": {
                collar: margin_summary(rows, collar)
                for collar in ("exact_half_open_graph", "positive_area_rectangle")
            },
            "word_stratum_scope":
                "HORIZONTAL_REFLECTION_OF_DUAL_R139_SEED_COLLARS",
            "word_stratum_status": "MATERIALIZED_BY_EXACT_JY_TRANSPORT",
            "C34_common_refinement_credit": 0,
            "D02_credit": 0,
        })
    require(
        len(template_rows) == 137 and len(word_rows) == 197,
        "reflected registry census",
    )
    reflected_template_ids = set(by_template)
    reflected_word_ids = set(by_word)
    summary = {
        "reflected_occurrence_count": len(reflected),
        "reflected_geometry_template_count": len(reflected_template_ids),
        "reflected_official_word_variant_count": len(reflected_word_ids),
        "combined_original_reflected_geometry_template_count":
            len(original_template_ids | reflected_template_ids),
        "combined_original_reflected_official_word_variant_count":
            len(original_word_ids | reflected_word_ids),
        "new_geometry_template_count":
            len(reflected_template_ids - original_template_ids),
        "new_official_word_variant_count":
            len(reflected_word_ids - original_word_ids),
        "reflected_owner_sequence_sha256": digest(
            [row["selected_absolute_owner_id"] for row in reflected]
        ),
        "reflected_official_word_key_sequence_sha256": digest(
            [row["official_word_key_id"] for row in reflected]
        ),
        "reflected_terminal_owner": reflected[-1]["selected_absolute_owner_id"],
        "reflected_destination_core_id": reflected[-1]["destination_core_id"],
    }
    require(summary == {
        "reflected_occurrence_count": 1648,
        "reflected_geometry_template_count": 137,
        "reflected_official_word_variant_count": 197,
        "combined_original_reflected_geometry_template_count": 146,
        "combined_original_reflected_official_word_variant_count": 214,
        "new_geometry_template_count": 9,
        "new_official_word_variant_count": 17,
        "reflected_owner_sequence_sha256":
            "946d3f8b2b21228e6cace189551111c764248877de15d7471289ba4c04d204b5",
        "reflected_official_word_key_sequence_sha256":
            "0927133ad517762da6e3fc27151cdeae616e0311cecfe518f0cc540da693cd0e",
        "reflected_terminal_owner": "G[-7,14]",
        "reflected_destination_core_id": REFLECTED_DESTINATION_CORE,
    }, "reflected path summary")
    return reflected, template_rows, word_rows, summary


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_bytes(canonical(value) + b"\n")


def write_manifest(directory: Path) -> None:
    members = sorted(
        path for path in directory.iterdir() if path.name != "root_manifest.sha256"
    )
    (directory / "root_manifest.sha256").write_text(
        "".join(f"{file_sha256(path)}  {path.name}\n" for path in members),
        encoding="utf-8",
    )


def build(output: Path, c36: Path, c36_audit: Path) -> dict[str, Any]:
    require(not output.exists(), f"output exists:{output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    stage = output.with_name(output.name + f".stage-{os.getpid()}")
    require(not stage.exists(), f"stage exists:{stage}")
    stage.mkdir()
    try:
        validate_manifest(c36)
        c36_result = strict_json(c36 / "result.json")
        validate_object(c36_result, "object_sha256", EXPECTED_C36_OBJECT, "C36")
        audit = strict_json(c36_audit)
        validate_object(
            audit, "object_sha256", EXPECTED_C36_AUDIT_OBJECT, "C36 audit"
        )
        require(
            audit.get("candidate_object_sha256") == EXPECTED_C36_OBJECT
            and audit.get("status")
            == "PASS_INDEPENDENT_C36_RECONSTRUCTION__14_OF_14_ATTACKS_FAIL_CLOSED",
            "C36 audit binding",
        )
        c35 = (ROOT / c36_result["C35_authority"]["path"]).resolve()
        c34 = (ROOT / c36_result["C34_authority"]["path"]).resolve()
        validate_manifest(c35)
        validate_manifest(c34)
        c35_result = strict_json(c35 / "result.json")
        c34_result = strict_json(c34 / "result.json")
        validate_object(c35_result, "object_sha256", EXPECTED_C35_OBJECT, "C35")
        validate_object(c34_result, "object_sha256", EXPECTED_C34_OBJECT, "C34")
        c32 = (ROOT / c34_result["C32_authority"]["path"]).resolve()
        c33 = (ROOT / c34_result["C33_authority"]["path"]).resolve()
        validate_manifest(c32)
        validate_manifest(c33)
        c32_result = strict_json(c32 / "result.json")
        c33_result = strict_json(c33 / "result.json")
        validate_object(c32_result, "object_sha256", EXPECTED_C32_OBJECT, "C32")
        validate_object(c33_result, "object_sha256", EXPECTED_C33_OBJECT, "C33")

        registry = build_gate5_registry()
        cell_pairs, component_pairs, mirror_seed, graph_summary = build_symmetry_rows(
            c32, c32_result, c33, c33_result, c34, c34_result
        )
        occurrences, templates, words, path_summary = build_reflected_path(
            c36, c36_result, c35, c35_result, registry
        )
        core_transport = reflected_terminal_core()

        cell_writer = LedgerWriter(
            stage / "ordinary_cell_reflection_pairs.jsonl.gz",
            "REPRESENTATIVE_CELL_ID_ASCENDING",
        )
        with cell_writer:
            for row in cell_pairs:
                cell_writer.write(row)
        component_writer = LedgerWriter(
            stage / "ordinary_component_reflection_pairs.jsonl.gz",
            "REPRESENTATIVE_COMPONENT_INDEX_ASCENDING",
        )
        with component_writer:
            for row in component_pairs:
                component_writer.write(row)
        occurrence_writer = LedgerWriter(
            stage / "reflected_r1648_occurrences.jsonl.gz",
            "COLLISION_INDEX_ASCENDING",
        )
        with occurrence_writer:
            for row in occurrences:
                occurrence_writer.write(row)
        template_writer = LedgerWriter(
            stage / "reflected_template_margin_atlas.jsonl.gz",
            "REFLECTED_GEOMETRY_TEMPLATE_ID_ASCENDING",
        )
        with template_writer:
            for row in templates:
                template_writer.write(row)
        word_writer = LedgerWriter(
            stage / "reflected_word_stratum_margin_atlas.jsonl.gz",
            "REFLECTED_OFFICIAL_WORD_VARIANT_ID_ASCENDING",
        )
        with word_writer:
            for row in words:
                word_writer.write(row)

        (stage / "REFLECTION_TRANSPORT_ONLY.lock").write_text(
            "C37 certifies the exact horizontal Jy transport of the C36 dual seed collars "
            "and the 13-pair C34 ordinary-component geometry quotient. It does not common-"
            "refine or promote any full C34 coarse cell and grants zero D02/D03/D04/Gate5/"
            "CM2 credit.\n",
            encoding="utf-8",
        )
        result: dict[str, Any] = {
            "schema": SCHEMA,
            "status": (
                "PASS_C37_EXACT_HORIZONTAL_REFLECTION_TRANSPORT__"
                "26_COMPONENTS_TO_13_PAIRS__1724_CELLS_TO_862_PAIRS__"
                "REFLECTED_R1648_1648_OF_1648__146_GEOMETRY__214_WORDS__"
                "ZERO_COMMON_REFINEMENT_CREDIT"
            ),
            "C36_authority": {
                "path": str(c36.resolve().relative_to(ROOT)),
                "object_sha256": c36_result["object_sha256"],
                "independent_audit_path": str(
                    c36_audit.resolve().relative_to(ROOT)
                ),
                "independent_audit_object_sha256": EXPECTED_C36_AUDIT_OBJECT,
            },
            "reflection_authority": {
                "generator": "Jy",
                "physical_map": "(x,y,s,p)->(x,1-y,s,-p)",
                "Round173_source_sha256": EXPECTED_R173_SOURCE,
                "Gate3_reflection_source_sha256": EXPECTED_GATE3_SOURCE,
                "Gate3_reflection_manifest_sha256": EXPECTED_GATE3_MANIFEST,
                "Gate5_registry_manifest_sha256": EXPECTED_GATE5_MANIFEST,
                "Gate5_candidate_word_key_rows_sha256":
                    registry["candidate_word_key_rows_sha256"],
                "target_lift_maps_by_source": {
                    "G": {"G[ix,iy]": "G[ix,-iy]", "W[ix,iy]": "W[ix,-iy-1]"},
                    "W": {"G[ix,iy]": "G[ix,1-iy]", "W[ix,iy]": "W[ix,-iy]"},
                },
                "signed_wall_token_map": {
                    "X-": "X-", "X+": "X+", "Y-": "Y+", "Y+": "Y-"
                },
                "chart_map": {"E": "E", "W": "W", "N": "S", "S": "N"},
                "terminal_core_transport": core_transport,
            },
            "symmetry_quotient_census": graph_summary,
            "reflected_seed_crosswalk": mirror_seed,
            "reflected_path_census": path_summary,
            "ledgers": {
                "ordinary_cell_reflection_pairs": cell_writer.descriptor(),
                "ordinary_component_reflection_pairs": component_writer.descriptor(),
                "reflected_r1648_occurrences": occurrence_writer.descriptor(),
                "reflected_template_margin_atlas": template_writer.descriptor(),
                "reflected_word_stratum_margin_atlas": word_writer.descriptor(),
            },
            "round144_terminal_census": c34_result["round144_terminal_census"],
            "strict_nonpromotion": {
                "ordinary_components_with_strict_R1648_seed_collar_anchor": 2,
                "independent_component_representatives_after_reflection": 13,
                "independent_cell_representatives_after_reflection": 862,
                "C34_common_refined_cell_count": 0,
                "C34_unresolved_R1648_continuations": 1724,
                "four_class_terminal_census_unresolved_zero": False,
                "D02": "BLOCKED_BY_1724_COMPLETE_R1648_CONTINUATIONS",
                "D03": "UNAUTHORIZED",
                "D04": "NOT_MINTED",
                "Gate5": "10/18",
                "complete_global_18_field_blocks": 0,
                "CM2": "NO-GO_FOR_CLAIM",
            },
            "required_next": (
                "common-refine the 862 independent ordinary-cell representatives against "
                "the combined 146-geometry/214-word exact template registry; reflect every "
                "certified child to its partner; then type all first events, component exits, "
                "seams, grazing, corners, and disconnected exterior sheets until unresolved=0"
            ),
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
    parser.add_argument("--c36", type=Path)
    parser.add_argument("--c36-audit", type=Path)
    args = parser.parse_args()
    c36 = args.c36 or (
        RUNTIME / "candidates" / (RUNTIME / "c36-current-token").read_text().strip()
    )
    c36_audit = args.c36_audit or (
        RUNTIME / "audit" / (RUNTIME / "c36-current-audit-token").read_text().strip()
        / "independent_audit.json"
    )
    result = build(args.output.resolve(), c36.resolve(), c36_audit.resolve())
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
