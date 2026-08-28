#!/usr/bin/env python3
"""C55-B: reconstruct the compact-atlas component graph and known-sheet anchors.

This producer consumes frozen artefacts as inert bytes.  It never imports or
executes an upstream producer and it never writes below .cm2-runtime.  The
result is deliberately fail-closed: a strict open collar is an anchor, not a
whole-component connectivity proof.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import stat
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"

SCHEMA = "cm2.round306c55b.global-component-adjacency-known-sheet-ledger.v1"
CELL_SCHEMA = SCHEMA + ".cell-component-crosswalk-row"
GLUE_SCHEMA = SCHEMA + ".component-edge-and-glue-row"
COMPONENT_SCHEMA = SCHEMA + ".ordinary-component-row"

PREFIX = "cm2_round306c55b_global_component_adjacency_known_sheet"
CELL_FILE = PREFIX + "_cell_component_crosswalk_v1.jsonl.gz"
GLUE_FILE = PREFIX + "_component_edges_and_glue_v1.jsonl.gz"
COMPONENT_FILE = PREFIX + "_ordinary_components_v1.jsonl.gz"
RESULT_FILE = PREFIX + "_result_v1.json"

C32 = ROOT / ".cm2-runtime/candidates/c32-four-chart-atlas-20260810T133217Z-3c4d0dff259783c9"
C33 = ROOT / ".cm2-runtime/candidates/c33-row-crosswalk-20260810T135223Z-eb0796f41e16d927"
C34 = ROOT / ".cm2-runtime/candidates/c34-seed-event-frontier-20260810T142445Z-6ec6dac7de032cdb"
C35 = ROOT / ".cm2-runtime/candidates/c35-transition-registry-20260810T145204Z-43f2cb35f9817ae2"
C36 = ROOT / ".cm2-runtime/candidates/c36-template-margin-atlas-20260810T153254Z-f37f908cf93d924c"
C37 = ROOT / ".cm2-runtime/candidates/c37-horizontal-reflection-20260810T154802Z-be0d65d5e1cc3c38"
C42 = ROOT / ".cm2-runtime/candidates/c42-p391-formal-producer-20260811T044500Z-f1"
C34_AUDIT = ROOT / ".cm2-runtime/audit/c34-independent-audit-20260810T142619Z-f0b7a1c124a4ae9d/independent_audit.json"
C35_AUDIT = ROOT / ".cm2-runtime/audit/c35-independent-audit-20260810T145205Z-1583ed4d15344427/independent_audit.json"
C36_AUDIT = ROOT / ".cm2-runtime/audit/c36-independent-audit-20260810T153315Z-5d214e67a8100871/independent_audit.json"
C37_AUDIT = ROOT / ".cm2-runtime/audit/c37-independent-audit-20260810T155248Z-49ba0249b7685f58/independent_audit.json"
C53_AUDIT = OUT / "cm2_round306c53_d02a_pair1_pair_level_successor_independent_audit_v1.json"
C53_HEAD = ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"

C29 = OUT / "cm2_round306c29_source_g_maximal_component_official_key_fibre_exhaustion_and_global_disposition_result.json"
C30 = ROOT / ".cm2-runtime/audit/c30q10-publication-20260810t123152z-b5341aceb44b735f-ledger/source_w_formal_ledger.json"
ROUND101 = OUT / "cm2-round101-rank3-eight-ray-source-grazing-closure-2026-07-22.json"
ROUND102 = OUT / "cm2-round102-rank3-corrected-face-quotient-2026-07-22.json"
ROUND140 = OUT / "cm2-round140-fixed-s-adaptive-component-identity-bridge-2026-07-24.json"
C55P0_CONTRACT = OUT / "cm2_round306c55p0_global_strict_decider_input_contract_v1.json"

EXPECTED = {
    "C32": "32ff9e0f90a12f17b16f67086eabda0986a0d52d185bea0c5c16e20518ca1474",
    "C33": "82dedeace982db89763e8a7e318fa6605d18cadc6bf390d6b23585d0922b87a0",
    "C34": "1c75d245a20bac35a0e33249f921ee862ad3c1397e78817189699dcc28552d2e",
    "C35": "cb524ae587390a578683c88d933125e041ab2a906f0351370d58f3b0d67aa752",
    "C36": "9251693da7d6cc0ff6011fb965276ac64be2b79be8f245ab8954291a43fb4167",
    "C37": "d6333d60d045dd60d93560b75f6332324c8a8bc131024e7e8100704aa2d89d2b",
    "C42": "a50914a266aff3396054d7f16e91d69db7fa735ad15f01cbf07eee8e708d99d2",
    "C34_AUDIT": "6cf20bd4915731e41be5da6cc4f8599ec4a4dbed8243bc3e17c15497b980b9f8",
    "C35_AUDIT": "914b1440a311a922819e488e4ed4ef39cb87df74b884f2fe7821336f7cb8d33a",
    "C36_AUDIT": "bc87269deb385ec19fe94003512c7d15e5b4fbf2fc0e5d20af4cc07adeaab273",
    "C37_AUDIT": "b5be1e8d97337ff90f514695f06bbb1156c606324a50b05766ed080a261d8044",
    "C53_AUDIT": "a7bee7e57b6527c7bf9ea7f17966379c62a722fe9ce2ce2009f19f85a5afaa7c",
    "C53_HEAD_FILE": "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3",
    "C53_HEAD_OBJECT": "cb90ab914c3b6518384669f42d05df33c21a717596190131c6a0f5683934cbfb",
    "C53_CHECKPOINT": "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab",
    "C55P0_CONTRACT_FILE": "0e2a7b713f3c4c007c65a27a42079ca33b024b8489b5dfd149312fcd5702333b",
}


class FailClosed(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise FailClosed(message)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def strict_json(path: Path) -> dict[str, Any]:
    def hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, f"duplicate JSON key:{path}:{key}")
            result[key] = value
        return result
    with path.open("r", encoding="utf-8") as stream:
        value = json.load(stream, object_pairs_hook=hook)
    require(isinstance(value, dict), f"JSON object required:{path}")
    return value


def validate_object(value: dict[str, Any], expected: str, label: str) -> None:
    copy = dict(value)
    claimed = copy.pop("object_sha256", None)
    require(claimed == expected and digest(copy) == expected, f"{label} object")


def validate_result(directory: Path, expected: str, label: str) -> dict[str, Any]:
    result = strict_json(directory / "result.json")
    validate_object(result, expected, label)
    return result


def read_ledger(directory: Path, descriptor: dict[str, Any]) -> list[dict[str, Any]]:
    path = directory / descriptor["filename"]
    require(file_sha(path) == descriptor["sha256"], f"ledger file hash:{path}")
    rows: list[dict[str, Any]] = []
    seq = hashlib.sha256()
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        for line in stream:
            row = json.loads(line)
            require(isinstance(row, dict) and "row_sha256" in row, f"row schema:{path}")
            claimed = row.pop("row_sha256")
            require(digest(row) == claimed, f"row hash:{path}")
            row["row_sha256"] = claimed
            seq.update((claimed + "\n").encode("ascii"))
            rows.append(row)
    require(len(rows) == descriptor["row_count"], f"row count:{path}")
    require(seq.hexdigest() == descriptor["row_hash_line_sequence_sha256"], f"row sequence:{path}")
    return rows


def object_pin(path: Path, object_sha256: str, capability: str, use: str) -> dict[str, Any]:
    return {
        "path": str(path.relative_to(ROOT)),
        "file_sha256": file_sha(path),
        "object_sha256": object_sha256,
        "capability": capability,
        "C55B_use": use,
    }


class LedgerWriter:
    def __init__(self, path: Path, order: str):
        self.path = path
        self.order = order
        self.count = 0
        self.sequence = hashlib.sha256()
        self._raw: Any = None
        self._gz: Any = None

    def __enter__(self) -> "LedgerWriter":
        self._raw = self.path.open("wb")
        self._gz = gzip.GzipFile(filename="", mode="wb", fileobj=self._raw, mtime=0)
        return self

    def write(self, row: dict[str, Any]) -> dict[str, Any]:
        require("row_sha256" not in row, "row must be open")
        row_hash = digest(row)
        complete = {**row, "row_sha256": row_hash}
        self._gz.write(canonical(complete) + b"\n")
        self.sequence.update((row_hash + "\n").encode("ascii"))
        self.count += 1
        return complete

    def __exit__(self, *_: Any) -> None:
        self._gz.close()
        self._raw.close()

    def descriptor(self) -> dict[str, Any]:
        return {
            "filename": self.path.name,
            "order": self.order,
            "row_count": self.count,
            "row_hash_line_sequence_sha256": self.sequence.hexdigest(),
            "sha256": file_sha(self.path),
            "size": self.path.stat().st_size,
        }


def status_for(cell_id: str, ordinary: set[str], events: set[str], crosswalk: dict[str, dict[str, Any]], current: dict[str, str]) -> str:
    if cell_id in ordinary:
        return current[cell_id]
    if cell_id in events:
        return "TYPED_EVENT_GRAPH"
    return "EARLIEST_PREFIX_EXCLUDED"


def build() -> dict[str, Any]:
    # Frozen inputs.
    c32 = validate_result(C32, EXPECTED["C32"], "C32")
    c33 = validate_result(C33, EXPECTED["C33"], "C33")
    c34 = validate_result(C34, EXPECTED["C34"], "C34")
    c35 = validate_result(C35, EXPECTED["C35"], "C35")
    c36 = validate_result(C36, EXPECTED["C36"], "C36")
    c37 = validate_result(C37, EXPECTED["C37"], "C37")
    c42 = validate_result(C42, EXPECTED["C42"], "C42")
    audits = {}
    for label, path in (("C34_AUDIT", C34_AUDIT), ("C35_AUDIT", C35_AUDIT), ("C36_AUDIT", C36_AUDIT), ("C37_AUDIT", C37_AUDIT)):
        audits[label] = strict_json(path)
        validate_object(audits[label], EXPECTED[label], label)
        require(str(audits[label]["status"]).startswith("PASS_INDEPENDENT"), f"{label} status")

    c53_audit = strict_json(C53_AUDIT)
    validate_object(c53_audit, EXPECTED["C53_AUDIT"], "C53 audit")
    head = strict_json(C53_HEAD)
    require(file_sha(C53_HEAD) == EXPECTED["C53_HEAD_FILE"], "C53 head file")
    require(head["authority_seal_object_sha256"] == EXPECTED["C53_HEAD_OBJECT"], "C53 head object claim")
    head_copy = dict(head)
    claimed_head = head_copy.pop("authority_seal_object_sha256")
    require(digest(head_copy) == claimed_head, "C53 head object reconstruction")
    require(head["post_seal_effective_checkpoint_object_sha256"] == EXPECTED["C53_CHECKPOINT"], "C53 checkpoint")
    require(head["authority_role"] == "GLOBAL_COMPOSITE" and head["semantic_commit"]["this_predecessor_keyed_global_head_is_only_semantic_commit"], "C53 committed global head")

    cells_rows = read_ledger(C32, c32["ledgers"]["cells"])
    adjacency = read_ledger(C32, c32["ledgers"]["intra_chart_adjacency"])
    seams = read_ledger(C32, c32["ledgers"]["source_chart_seams"])
    grazing = read_ledger(C32, c32["ledgers"]["grazing"])
    corners = read_ledger(C32, c32["ledgers"]["corners"])
    event_faces = read_ledger(C32, c32["ledgers"]["inherited_event_faces"])
    cross_rows = read_ledger(C33, c33["row_level_crosswalk"])
    event_bindings = read_ledger(C34, c34["ledgers"]["typed_first_event_bindings"])
    c34_components = read_ledger(C34, c34["ledgers"]["ordinary_components"])
    reflection_pairs = read_ledger(C37, c37["ledgers"]["ordinary_cell_reflection_pairs"])
    component_pairs = read_ledger(C37, c37["ledgers"]["ordinary_component_reflection_pairs"])
    c42_parents = read_ledger(C42, c42["ledgers"]["parent_conservation"])

    require(len(cells_rows) == len(cross_rows) == 76832, "full source-W universe")
    cells = {row["cell_id"]: row for row in cells_rows}
    crosswalk = {row["cell_id"]: row for row in cross_rows}
    require(len(cells) == len(crosswalk) == 76832 and set(cells) == set(crosswalk), "cell/crosswalk bijection")
    live = {key for key, row in crosswalk.items() if row["formal_source_W_disposition"] == "RESOLVED_NONEXCLUDED"}
    events = {row["cell_id"] for row in event_bindings}
    ordinary = live - events
    require(len(live) == 2020 and len(events) == 296 and len(ordinary) == 1724, "base live census")

    # Reconstruct the ordinary graph using explicit face atoms and chart seams.
    graph: dict[str, set[str]] = defaultdict(set)
    live_edge_census: Counter[str] = Counter()
    ordinary_edge_source: list[tuple[str, dict[str, Any], str, str]] = []
    for kind, rows, left, right in (
        ("INTRA_CHART_FACE", adjacency, "negative_cell_id", "positive_cell_id"),
        ("SOURCE_CHART_TRANSITION", seams, "left_cell_id", "right_cell_id"),
    ):
        for row in rows:
            first, second = row[left], row[right]
            if first in live and second in live:
                graph[first].add(second)
                graph[second].add(first)
                live_edge_census[kind] += 1
            if first in ordinary or second in ordinary:
                ordinary_edge_source.append((kind, row, first, second))
    require(live_edge_census == Counter({"INTRA_CHART_FACE": 3978, "SOURCE_CHART_TRANSITION": 38}), "live edge census")

    seed_record = strict_json(C34 / c34["R1648_seed_crosswalk"]["filename"])
    require(file_sha(C34 / c34["R1648_seed_crosswalk"]["filename"]) == c34["R1648_seed_crosswalk"]["sha256"], "seed crosswalk file")
    seed_id = seed_record["cell_id"]
    visited: set[str] = set()
    components: list[set[str]] = []
    for start in sorted(ordinary):
        if start in visited:
            continue
        component = {start}
        visited.add(start)
        queue = deque([start])
        while queue:
            here = queue.popleft()
            for neighbour in graph[here]:
                if neighbour in ordinary and neighbour not in visited:
                    visited.add(neighbour)
                    component.add(neighbour)
                    queue.append(neighbour)
        components.append(component)
    components.sort(key=lambda value: (seed_id not in value, -len(value), min(value)))
    require(Counter(map(len, components)) == Counter({850: 2, 1: 24}), "component size census")
    component_of = {cell_id: index for index, component in enumerate(components) for cell_id in component}
    require(len(component_of) == 1724, "component partition")

    for index, (component, frozen) in enumerate(zip(components, c34_components, strict=True)):
        ids = sorted(component)
        require(frozen["component_index"] == index and frozen["component_id"] == "c34-ordinary-component:" + digest(ids), f"C34 component:{index}")
        require(frozen["cell_ids_sha256"] == digest(ids) and frozen["cell_count"] == len(ids), f"C34 membership:{index}")

    # Exact C37 quotient and current C53 formal projection.
    projections = c53_audit["post_seal_promotion_derivation"]["parent_projections"]
    require(len(reflection_pairs) == len(c42_parents) == len(projections) == 862, "pair projection census")
    current: dict[str, str] = {}
    pair_info: dict[str, dict[str, Any]] = {}
    for pair, parent, projection in zip(reflection_pairs, c42_parents, projections, strict=True):
        index = pair["pair_index"]
        require(parent["pair_index"] == projection["pair_index"] == index, f"pair order:{index}")
        require(projection["C42_parent_row_sha256"] == parent["row_sha256"], f"C42 projection:{index}")
        classification = "EARLIEST_PREFIX_EXCLUDED" if projection["after_whole_representative"] else "UNRESOLVED_R1648_CONTINUATION"
        for side, partner in (("representative", "reflected"), ("reflected", "representative")):
            cell_id = pair[side + "_cell_id"]
            partner_id = pair[partner + "_cell_id"]
            require(cell_id in ordinary and cell_id not in current, f"C37 ordinary pair:{cell_id}")
            current[cell_id] = classification
            pair_info[cell_id] = {
                "pair_index": index,
                "reflection_partner_cell_id": partner_id,
                "C37_pair_row_sha256": pair["row_sha256"],
                "C42_parent_row_sha256": parent["row_sha256"],
                "C53_parent_projection_object_sha256": projection["projection_object_sha256"],
                "whole_pair_terminal_after_C53": projection["after_whole_representative"],
                "newly_whole_by_C53_pair_seal": projection["newly_whole_by_C53_pair_seal"],
            }
    require(set(current) == ordinary, "current projection covers ordinary cells")
    require(Counter(current.values()) == Counter({"EARLIEST_PREFIX_EXCLUDED": 576, "UNRESOLVED_R1648_CONTINUATION": 1148}), "C53 effective ordinary census")

    component_ids = {index: c34_components[index]["component_id"] for index in range(26)}
    reflected_seed = c37["reflected_seed_crosswalk"]
    anchor_by_component: dict[int, dict[str, Any]] = {
        0: {
            "anchor_type": "ROUND140_STRICT_OPEN_ADAPTIVE_CONNECTED_CELL",
            "anchor_cell_id": seed_id,
            "anchor_origin_key": seed_record["origin_key"],
            "adaptive_path_cell_id": seed_record["adaptive_path_cell_id"],
            "positive_area_open_support": True,
            "proof_path": [
                "Round140.fixed_s_adaptive_path_cell.open_support_connected",
                "C34.R1648_seed_crosswalk.adaptive_open_cell_strictly_inside_coarse_cell",
                "C34.ordinary_component.membership",
            ],
            "whole_component_connected_credit": 0,
        },
        1: {
            "anchor_type": "C37_JY_REFLECTED_STRICT_OPEN_CONNECTED_COLLAR",
            "anchor_cell_id": reflected_seed["reflected_seed_cell_id"],
            "anchor_origin_key": reflected_seed["reflected_seed_origin_key"],
            "adaptive_path_cell_id": seed_record["adaptive_path_cell_id"],
            "positive_area_open_support": True,
            "proof_path": [
                "Round140.fixed_s_adaptive_path_cell.open_support_connected",
                "C34.R1648_seed_crosswalk",
                "C37.reflection_authority.Jy",
                "C37.reflected_seed_crosswalk.reflected_open_collar_strictly_inside_coarse_cell",
                "C34.ordinary_component.membership",
            ],
            "whole_component_connected_credit": 0,
        },
    }
    require(component_of[seed_id] == 0 and component_of[reflected_seed["reflected_seed_cell_id"]] == 1, "anchor component identity")

    # Cell crosswalk, including exact boxes and current formal status.
    cell_rows_by_component: dict[int, list[dict[str, Any]]] = defaultdict(list)
    cell_writer = LedgerWriter(OUT / CELL_FILE, "COMPONENT_INDEX_THEN_CELL_ID")
    with cell_writer:
        for component_index, component in enumerate(components):
            for cell_id in sorted(component):
                cell = cells[cell_id]
                row = {
                    "schema": CELL_SCHEMA,
                    "cell_id": cell_id,
                    "origin_key": cell["origin_key"],
                    "compact_chart": cell["compact_chart"],
                    "gate3_chart": cell["gate3_chart"],
                    "physical_slice": cell["physical_slice"],
                    "physical_t_interval": cell["physical_t_interval"],
                    "physical_p_interval": cell["physical_p_interval"],
                    "gate3_product_box": cell["gate3_product_box"],
                    "C32_cell_row_sha256": cell["row_sha256"],
                    "C33_crosswalk_row_sha256": crosswalk[cell_id]["row_sha256"],
                    "component_index": component_index,
                    "component_id": component_ids[component_index],
                    "C34_component_row_sha256": c34_components[component_index]["row_sha256"],
                    **pair_info[cell_id],
                    "current_effective_disposition": current[cell_id],
                    "known_sheet_anchor_role": (
                        "ANCHOR_CELL_CONTAINS_STRICT_OPEN_COLLAR"
                        if component_index in anchor_by_component and anchor_by_component[component_index]["anchor_cell_id"] == cell_id
                        else "NO_CELL_LEVEL_ANCHOR"
                    ),
                    "coordinate_or_key_coincidence_used": False,
                    "whole_cell_connected_to_known_credit": 0,
                    "D02_gate_credit": 0,
                }
                complete = cell_writer.write(row)
                cell_rows_by_component[component_index].append(complete)

    # Explicit face, chart-transition, grazing, corner and event-face glue.
    glue_rows_by_component: dict[int, list[str]] = defaultdict(list)
    glue_counts: Counter[str] = Counter()
    glue_writer = LedgerWriter(OUT / GLUE_FILE, "GLUE_KIND_THEN_UPSTREAM_ROW_SHA256")
    glue_source_rows: list[dict[str, Any]] = []
    for kind, source, first, second in ordinary_edge_source:
        first_kind = status_for(first, ordinary, events, crosswalk, current)
        second_kind = status_for(second, ordinary, events, crosswalk, current)
        if first in ordinary and second in ordinary:
            scope = "ORDINARY_INTERNAL"
        elif first in events or second in events:
            scope = "ORDINARY_TO_TYPED_EVENT_BOUNDARY"
        else:
            scope = "ORDINARY_TO_FORMAL_EXCLUSION_BOUNDARY"
        geometry = ({
            "compact_chart": source["compact_chart"], "axis": source["axis"],
            "coordinate": source["coordinate"], "span": source["span"],
        } if kind == "INTRA_CHART_FACE" else {
            "seam_id": source["seam_id"], "left_chart": source["left_chart"],
            "right_chart": source["right_chart"],
            "left_compact_endpoint": source["left_compact_endpoint"],
            "right_compact_endpoint": source["right_compact_endpoint"],
            "physical_p_span": source["physical_p_span"],
            "exact_state_gluing_inherited_from_round162": source["exact_state_gluing_inherited_from_round162"],
        })
        glue_source_rows.append({
            "schema": GLUE_SCHEMA, "glue_kind": kind, "scope": scope,
            "face_or_corner_id": source["face_id"], "dimension": source["dimension"],
            "left_cell_id": first, "right_cell_id": second,
            "left_disposition": first_kind, "right_disposition": second_kind,
            "ordinary_component_indices": sorted({component_of[x] for x in (first, second) if x in ordinary}),
            "exact_geometry": geometry,
            "upstream_row_sha256": source["row_sha256"],
            "gluing_proof_kind": "EXPLICIT_COMMON_FACE_WITH_EXACT_COORDINATE_AND_SPAN",
            "coordinate_or_key_coincidence_used": False, "terminal_credit": 0,
        })
    for source in grazing:
        cell_id = source["incident_cell_id"]
        glue_source_rows.append({
            "schema": GLUE_SCHEMA, "glue_kind": "SOURCE_GRAZING_FACE", "scope": "GLOBAL_GRAZING_INVENTORY",
            "face_or_corner_id": source["face_id"], "dimension": source["dimension"],
            "left_cell_id": cell_id, "right_cell_id": None,
            "left_disposition": status_for(cell_id, ordinary, events, crosswalk, current), "right_disposition": None,
            "ordinary_component_indices": ([component_of[cell_id]] if cell_id in ordinary else []),
            "exact_geometry": {"compact_chart": source["compact_chart"], "compact_q": source["compact_q"], "physical_p": source["physical_p"], "physical_t_span": source["physical_t_span"]},
            "upstream_row_sha256": source["row_sha256"],
            "gluing_proof_kind": "EXPLICIT_C32_GRAZING_FACE_GEOMETRY_ONLY",
            "coordinate_or_key_coincidence_used": False,
            "terminal_credit": source["round144_dynamic_cemetery_credit"],
        })
    for source in corners:
        left, right = source["left_cell_id"], source["right_cell_id"]
        glue_source_rows.append({
            "schema": GLUE_SCHEMA, "glue_kind": "SOURCE_GRAZING_SEAM_CORNER", "scope": "GLOBAL_CORNER_INVENTORY",
            "face_or_corner_id": source["corner_id"], "dimension": source["dimension"],
            "left_cell_id": left, "right_cell_id": right,
            "left_disposition": status_for(left, ordinary, events, crosswalk, current),
            "right_disposition": status_for(right, ordinary, events, crosswalk, current),
            "ordinary_component_indices": sorted({component_of[x] for x in (left, right) if x in ordinary}),
            "exact_geometry": {"seam_id": source["seam_id"], "compact_q": source["compact_q"], "physical_p": source["physical_p"]},
            "upstream_row_sha256": source["row_sha256"],
            "gluing_proof_kind": "EXPLICIT_C32_ZERO_DIMENSIONAL_SEAM_GRAZING_GLUE",
            "coordinate_or_key_coincidence_used": False,
            "terminal_credit": source["round144_dynamic_cemetery_credit"],
        })
    binding_by_cell = {row["cell_id"]: row for row in event_bindings}
    for source in event_faces:
        cell_id = source["incident_cell_id"]
        live_binding = binding_by_cell.get(cell_id)
        glue_source_rows.append({
            "schema": GLUE_SCHEMA, "glue_kind": "INHERITED_FIRST_EVENT_FACE", "scope": ("LIVE_TYPED_EVENT" if live_binding else "EXCLUDED_EVENT_CANDIDATE"),
            "face_or_corner_id": source["event_face_id"], "dimension": source["dimension"],
            "left_cell_id": cell_id, "right_cell_id": None,
            "left_disposition": status_for(cell_id, ordinary, events, crosswalk, current), "right_disposition": None,
            "ordinary_component_indices": [],
            "exact_geometry": {"compact_chart": source["compact_chart"], "origin_key": source["origin_key"], "event_payload": source["event_payload"]},
            "upstream_row_sha256": source["row_sha256"],
            "typed_event_binding_row_sha256": (live_binding["row_sha256"] if live_binding else None),
            "gluing_proof_kind": "EXPLICIT_INHERITED_EVENT_FACE_WITH_C34_BINDING_IF_LIVE",
            "coordinate_or_key_coincidence_used": False,
            "terminal_credit": (1 if live_binding else 0),
        })
    glue_source_rows.sort(key=lambda row: (row["glue_kind"], row["upstream_row_sha256"]))
    with glue_writer:
        for row in glue_source_rows:
            complete = glue_writer.write(row)
            glue_counts[row["glue_kind"] + ":" + row["scope"]] += 1
            for index in row["ordinary_component_indices"]:
                glue_rows_by_component[index].append(complete["row_sha256"])

    # Closed component rows bind membership, explicit edge/glue provenance and anchors.
    component_writer = LedgerWriter(OUT / COMPONENT_FILE, "COMPONENT_INDEX_ASCENDING")
    with component_writer:
        for index, component in enumerate(components):
            cell_rows = cell_rows_by_component[index]
            unresolved_ids = sorted(row["cell_id"] for row in cell_rows if row["current_effective_disposition"] == "UNRESOLVED_R1648_CONTINUATION")
            excluded_ids = sorted(row["cell_id"] for row in cell_rows if row["current_effective_disposition"] == "EARLIEST_PREFIX_EXCLUDED")
            anchor = anchor_by_component.get(index)
            row = {
                "schema": COMPONENT_SCHEMA,
                "component_index": index, "component_id": component_ids[index],
                "C34_component_row_sha256": c34_components[index]["row_sha256"],
                "cell_count": len(component), "member_cell_ids": sorted(component),
                "member_cell_ids_sha256": digest(sorted(component)),
                "member_cell_row_sha256s": [row["row_sha256"] for row in cell_rows],
                "member_cell_row_sequence_sha256": digest([row["row_sha256"] for row in cell_rows]),
                "internal_face_connected": True,
                "edge_and_glue_row_sha256s": sorted(glue_rows_by_component[index]),
                "edge_and_glue_row_sequence_sha256": digest(sorted(glue_rows_by_component[index])),
                "known_sheet_anchor": anchor,
                "anchor_is_strict_subset_not_whole_component": anchor is not None,
                "positive_area_anchor_proof_present": anchor is not None and anchor["positive_area_open_support"],
                "common_refinement_status": "NOT_MATERIALIZED_FOR_WHOLE_COMPONENT",
                "current_excluded_cell_count": len(excluded_ids),
                "current_excluded_cell_ids_sha256": digest(excluded_ids),
                "current_unresolved_cell_count": len(unresolved_ids),
                "current_unresolved_cell_ids_sha256": digest(unresolved_ids),
                "whole_component_terminal_class": None,
                "whole_component_connected_to_known_credit": 0,
                "unresolved_reason": (
                    "STRICT_OPEN_CONNECTED_COLLAR_DOES_NOT_COVER_WHOLE_COMPONENT_AND_FULL_R1648_COMMON_REFINEMENT_IS_ABSENT"
                    if anchor else
                    "NO_KNOWN_SHEET_ANCHOR_AND_COMPLETE_EVENT_EXTERIOR_CLOSURE_IS_ABSENT"
                ),
                "singleton_isolation_promoted": False,
                "coordinate_or_key_coincidence_used": False,
                "D02_gate_credit": 0,
            }
            component_writer.write(row)

    # Inventory older and current capabilities without conflating scopes.
    c29 = strict_json(C29)
    c30 = strict_json(C30)
    r101, r102, r140 = strict_json(ROUND101), strict_json(ROUND102), strict_json(ROUND140)
    c55p0 = strict_json(C55P0_CONTRACT)
    require(file_sha(C55P0_CONTRACT) == EXPECTED["C55P0_CONTRACT_FILE"], "C55p0 contract file")
    require(c55p0["authority_input"]["effective_checkpoint_object_sha256"] == EXPECTED["C53_CHECKPOINT"], "C55p0 checkpoint")
    require(c55p0["strict_nonpromotion"]["component_isolation_is_not_cemetery"] is True, "C55p0 isolation lock")
    require(c55p0["strict_nonpromotion"]["reflection_pairing_is_not_terminal_credit"] is True, "C55p0 reflection lock")
    inventory = [
        object_pin(C29, c29["result_sha256"], "502204 Source-G member dispositions / 57876 maximal components", "PROVENANCE_ONLY_DIFFERENT_UNIVERSE"),
        object_pin(C30, c30["object_sha256"], "76832 Source-W formal disposition ledger; remainder=0", "C33_FORMAL_SOURCE_W_PIN"),
        object_pin(ROUND101, r101["result_sha256"], "eight immutable rank-three exterior rays to source grazing", "GRAZING_PRECEDENT_NOT_GLOBAL_C32_TERMINAL_DECIDER"),
        object_pin(ROUND102, r102["result_sha256"], "twelve corrected rank-three physical faces and endpoint quotient", "FACE_QUOTIENT_PRECEDENT_NOT_C32_COMMON_REFINEMENT"),
        object_pin(ROUND140, r140["result_sha256"], "one fixed-s positive-area connected adaptive open cell", "KNOWN_SHEET_OPEN_COLLAR_ANCHOR_ONLY"),
    ]
    authority_pins = {
        "C32": object_pin(C32 / "result.json", EXPECTED["C32"], "four-chart compact atlas", "PRIMARY_GEOMETRY"),
        "C33": object_pin(C33 / "result.json", EXPECTED["C33"], "row-level Source-W crosswalk", "PRIMARY_DISPOSITION"),
        "C34": object_pin(C34 / "result.json", EXPECTED["C34"], "seed/event/component frontier", "PRIMARY_COMPONENT_PARTITION"),
        "C34_independent_audit": object_pin(C34_AUDIT, EXPECTED["C34_AUDIT"], "independent C34 reconstruction", "AUDIT_PIN"),
        "C35": object_pin(C35 / "result.json", EXPECTED["C35"], "R1648 transition registry", "OBLIGATION_PROVENANCE"),
        "C35_independent_audit": object_pin(C35_AUDIT, EXPECTED["C35_AUDIT"], "independent C35 reconstruction", "AUDIT_PIN"),
        "C36": object_pin(C36 / "result.json", EXPECTED["C36"], "dual-collar margin atlas", "COMMON_REFINEMENT_GAP_PIN"),
        "C36_independent_audit": object_pin(C36_AUDIT, EXPECTED["C36_AUDIT"], "independent C36 reconstruction", "AUDIT_PIN"),
        "C37": object_pin(C37 / "result.json", EXPECTED["C37"], "exact Jy reflection quotient", "PRIMARY_QUOTIENT"),
        "C37_independent_audit": object_pin(C37_AUDIT, EXPECTED["C37_AUDIT"], "independent C37 reconstruction", "AUDIT_PIN"),
        "C42": object_pin(C42 / "result.json", EXPECTED["C42"], "862 parent formal projections", "FORMAL_PREDECESSOR_PROJECTION"),
        "C53_independent_audit": object_pin(C53_AUDIT, EXPECTED["C53_AUDIT"], "post-seal 862 parent derivation", "CURRENT_EFFECTIVE_PROJECTION"),
        "C55p0_input_contract": {
            "path": str(C55P0_CONTRACT.relative_to(ROOT)),
            "file_sha256": EXPECTED["C55P0_CONTRACT_FILE"],
            "schema": c55p0["schema"],
            "capability": "frozen global strict-decider closed-row contract",
            "C55B_use": "MANDATORY_INPUT_CONTRACT",
        },
    }

    result: dict[str, Any] = {
        "schema": SCHEMA,
        "status": "PASS_RECONSTRUCTED_COMPONENT_ADJACENCY_AND_TWO_STRICT_OPEN_KNOWN_SHEET_COLLARS__FAIL_CLOSED_1148_CURRENT_UNRESOLVED_CELLS",
        "C53_effective_authority": {
            "head_path": str(C53_HEAD.relative_to(ROOT)),
            "head_file_sha256": EXPECTED["C53_HEAD_FILE"],
            "head_object_sha256": EXPECTED["C53_HEAD_OBJECT"],
            "effective_checkpoint_object_sha256": EXPECTED["C53_CHECKPOINT"],
            "authority_role": "GLOBAL_COMPOSITE",
            "current_four_class_census": head["formal_scope"]["D02_four_class_after"],
        },
        "authority_pins": authority_pins,
        "inventory": inventory,
        "ledgers": {
            "cell_component_crosswalk": cell_writer.descriptor(),
            "component_edges_and_glue": glue_writer.descriptor(),
            "ordinary_components": component_writer.descriptor(),
        },
        "base_atlas_census": {
            "source_W_cells": 76832, "formal_excluded": 74812, "live_cells": 2020,
            "typed_event_cells": 296, "ordinary_cells": 1724,
            "ordinary_components": 26, "component_size_census": {"1": 24, "850": 2},
            "reflection_pairs": 13, "ordinary_cell_reflection_pairs": 862,
            "live_intra_chart_faces": 3978, "live_source_chart_seams": 38,
            "C32_global_grazing_faces": 1024, "C32_global_grazing_corners": 8,
        },
        "current_effective_census": {
            "ordinary_cells_formally_excluded": 576,
            "ordinary_cells_unresolved": 1148,
            "whole_representatives": 288,
            "representatives_remaining": 574,
            "four_class_census": head["formal_scope"]["D02_four_class_after"],
        },
        "known_sheet_anchor_census": {
            "components_with_strict_open_connected_collar": 2,
            "components_with_whole_component_connected_proof": 0,
            "unanchored_singleton_components": 24,
            "anchor_credit": 0,
        },
        "exact_unresolved_partition": {
            "ANCHORED_COMPONENT_WITHOUT_WHOLE_COMMON_REFINEMENT": {"component_count": 2, "current_unresolved_cell_count": 1124},
            "UNANCHORED_SINGLETON_WITHOUT_COMPLETE_EVENT_EXTERIOR_CLOSURE": {"component_count": 24, "current_unresolved_cell_count": 24},
            "total_component_count": 26,
            "total_current_unresolved_cell_count": 1148,
            "partition_disjoint_and_exhaustive": True,
        },
        "reconstruction_invariants": {
            "all_76832_C32_C33_rows_hash_verified": True,
            "components_rebuilt_from_explicit_C32_face_and_seam_rows": True,
            "C34_component_rows_reproduced": 26,
            "C37_reflection_pairs_reproduced": 862,
            "C42_C53_parent_projection_rows_correlated": 862,
            "explicit_chart_transition_glue_used": True,
            "explicit_face_grazing_corner_inventory_used": True,
            "full_R1648_common_refinement_materialized": False,
            "C55p0_input_contract_bound": True,
        },
        "forbidden_shortcuts": {
            "coordinate_coincidence_as_adjacency": False,
            "origin_key_coincidence_as_component_identity": False,
            "strict_subset_anchor_promoted_to_whole_component": False,
            "singleton_isolation_promoted_to_disconnected_exterior": False,
            "geometric_grazing_face_promoted_without_dynamic_decider": False,
        },
        "global_closure_proved": False,
        "unresolved_zero": False,
        "strict_decider_eligible": False,
        "credit_locks": {"formal_credit": 0, "D02_gate_credit": 0, "D03_credit": 0, "D04_credit": 0, "Gate5_credit": 0},
        "required_next": "common-refine every current unresolved cell against the full four-chart R1648 transition atlas; prove whole-component anchor or exact event/exterior disposition, including face/corner/source-grazing glue; require unresolved=0 under an independent no-producer decider",
    }
    result["object_sha256"] = digest(result)
    (OUT / RESULT_FILE).write_bytes(canonical(result) + b"\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", action="store_true")
    args = parser.parse_args()
    require(args.build, "use --build")
    result = build()
    print(json.dumps({"status": result["status"], "object_sha256": result["object_sha256"], "ledgers": result["ledgers"]}, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except FailClosed as exc:
        print(json.dumps({"status": "FAIL_CLOSED", "reason": str(exc)}, sort_keys=True, separators=(",", ":")))
        raise SystemExit(1)
