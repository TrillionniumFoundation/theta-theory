#!/usr/bin/env python3
"""C56s: audit the 24 singleton ordinary components as whole cells.

The program consumes frozen JSON/JSONL artefacts as inert bytes.  It does not
import or execute an upstream producer and writes only new C56s deliverables.
Boundary adjacency is recorded exhaustively but is never promoted to a
dynamic continuation or whole-cell terminal proof.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
PREFIX = "cm2_round306c56s_singleton_whole_cell_terminal_audit"
HISTORY_FILE = PREFIX + "_r1648_history_v1.jsonl.gz"
SINGLETON_FILE = PREFIX + "_singleton_ledger_v1.jsonl.gz"
RESULT_FILE = PREFIX + "_result_v1.json"

SCHEMA = "cm2.round306c56s.singleton-whole-cell-terminal-audit.v1"
HISTORY_SCHEMA = SCHEMA + ".r1648-history-row"
SINGLETON_SCHEMA = SCHEMA + ".singleton-row"

C33 = ROOT / ".cm2-runtime/candidates/c33-row-crosswalk-20260810T135223Z-eb0796f41e16d927"
C34 = ROOT / ".cm2-runtime/candidates/c34-seed-event-frontier-20260810T142445Z-6ec6dac7de032cdb"
C35 = ROOT / ".cm2-runtime/candidates/c35-transition-registry-20260810T145204Z-43f2cb35f9817ae2"
C36 = ROOT / ".cm2-runtime/candidates/c36-template-margin-atlas-20260810T153254Z-f37f908cf93d924c"
C37 = ROOT / ".cm2-runtime/candidates/c37-horizontal-reflection-20260810T154802Z-be0d65d5e1cc3c38"
C55B_RESULT = OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_result_v1.json"
C55B_CELLS = OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_cell_component_crosswalk_v1.jsonl.gz"
C55B_GLUE = OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_component_edges_and_glue_v1.jsonl.gz"
C55B_COMPONENTS = OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_ordinary_components_v1.jsonl.gz"
C55P0 = OUT / "cm2_round306c55p0_global_strict_decider_input_contract_v1.json"
C50B_CONTRACT = OUT / "cm2_round306c50b_d02b_global_cemetery_disconnected_exterior_oracle_contract_v1.json"
C50B_VERIFY = OUT / "cm2_round306c50b_d02b_global_cemetery_disconnected_exterior_oracle_independent_verification_v1.json"

EXPECTED_OBJECT = {
    "C33": "82dedeace982db89763e8a7e318fa6605d18cadc6bf390d6b23585d0922b87a0",
    "C34": "1c75d245a20bac35a0e33249f921ee862ad3c1397e78817189699dcc28552d2e",
    "C35": "cb524ae587390a578683c88d933125e041ab2a906f0351370d58f3b0d67aa752",
    "C36": "9251693da7d6cc0ff6011fb965276ac64be2b79be8f245ab8954291a43fb4167",
    "C37": "d6333d60d045dd60d93560b75f6332324c8a8bc131024e7e8100704aa2d89d2b",
    "C55B": "1ce396e9746d3c0364325e8308e94c9dcd4a3bfbba8c17a9c9961915e807cc56",
    "C50B_CONTRACT": "ddd1776bc133cac340b872f03325e97e8526a545e3e1a3fb11d56a159a4f9d97",
    "C50B_VERIFY": "b782d342c306d102f056d94af01797a8a08d717bd0562f680f0a375bbdf23ebf",
}
EXPECTED_FILE = {
    "C33": "5a69edde0723525b052934b7522628d90da61f40c71fbbc9ae49a072a506a11f",
    "C34": "bca9d948f86733d75a9f84c7b4b2f11b2617a71b0c6acea14a6d7d7692d3d69d",
    "C35": "3122c977e47c1b1f685f7c97f3b9d68e9ff79d477916cb8bd4556f4b518c17ad",
    "C36": "7922139708dc486232ec79b29d6339bdca7e00999bddf63d5b9a83b3f4cfbbd1",
    "C37": "5b968d957cbca2a4f8aec855a44643f5add7fe0244d933401dfdef9ad7be61f3",
    "C55B": "6bf9cae7b4b422c5c2121f95828e1508700fe1a5d1b1128598c8617f65032a93",
    "C55P0": "0e2a7b713f3c4c007c65a27a42079ca33b024b8489b5dfd149312fcd5702333b",
    "C50B_CONTRACT": "25248a20e5a81f5119b204d856ef61ce18c2307412f3b304f2bb35213729ce1e",
    "C50B_VERIFY": "5fbaa3a171cf26650b8ee3179b4acbe5107d58707923aa6288058e1475db2bdb",
}
EXPECTED_C55_LEDGER = {
    "cell_component_crosswalk": "123a742ed553d89fd1026cf65c64879d9a92916492b5b583888c3312551ca2ce",
    "component_edges_and_glue": "23ea0b4419f155f62d32b6b73c5a16c6f402884d333c222ff803899a58da29a0",
    "ordinary_components": "bebc49f66efb01c0b980ec10258a60d7aead9d4d2006d28bdd169c9a9ae38a04",
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
    require(isinstance(value, dict), f"object required:{path}")
    return value


def validate_object(value: dict[str, Any], expected: str, label: str) -> None:
    copy = dict(value)
    claimed = copy.pop("object_sha256", copy.pop("result_sha256", None))
    require(claimed == expected and digest(copy) == expected, f"object pin:{label}")


def validate_result(directory: Path, label: str) -> dict[str, Any]:
    path = directory / "result.json"
    require(file_sha(path) == EXPECTED_FILE[label], f"file pin:{label}")
    value = strict_json(path)
    validate_object(value, EXPECTED_OBJECT[label], label)
    return value


def read_ledger(path: Path, descriptor: dict[str, Any]) -> list[dict[str, Any]]:
    require(file_sha(path) == descriptor["sha256"], f"ledger file hash:{path}")
    rows: list[dict[str, Any]] = []
    sequence = hashlib.sha256()
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        for line in stream:
            value = json.loads(line)
            require(isinstance(value, dict) and "row_sha256" in value, f"ledger row:{path}")
            claimed = value.pop("row_sha256")
            require(digest(value) == claimed, f"ledger row hash:{path}")
            value["row_sha256"] = claimed
            rows.append(value)
            sequence.update((claimed + "\n").encode("ascii"))
    require(len(rows) == descriptor["row_count"], f"ledger row count:{path}")
    require(sequence.hexdigest() == descriptor["row_hash_line_sequence_sha256"], f"ledger sequence:{path}")
    return rows


class LedgerWriter:
    def __init__(self, path: Path, order: str):
        self.path, self.order = path, order
        self.count = 0
        self.sequence = hashlib.sha256()
        self._raw: Any = None
        self._gzip: Any = None

    def __enter__(self) -> "LedgerWriter":
        self._raw = self.path.open("wb")
        self._gzip = gzip.GzipFile(filename="", mode="wb", fileobj=self._raw, mtime=0)
        return self

    def write(self, row: dict[str, Any]) -> dict[str, Any]:
        require("row_sha256" not in row, "open output row required")
        row_hash = digest(row)
        closed = {**row, "row_sha256": row_hash}
        self._gzip.write(canonical(closed) + b"\n")
        self.sequence.update((row_hash + "\n").encode("ascii"))
        self.count += 1
        return closed

    def __exit__(self, *_: Any) -> None:
        self._gzip.close()
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


def q(value: Any) -> Fraction:
    if isinstance(value, dict):
        require(value.get("kind") == "RATIONAL", "rational coordinate kind")
        value = value["value"]
    return Fraction(str(value))


def side_for(cell: dict[str, Any], face: dict[str, Any]) -> str:
    geometry = face["exact_geometry"]
    axis = geometry["axis"]
    coordinate = q(geometry["coordinate"])
    if axis == "t":
        endpoints = [q(x) for x in cell["physical_t_interval"]]
        span = [q(x) for x in geometry["span"]]
        require(span == [q(x) for x in cell["physical_p_interval"]], "t-face exact p span")
    else:
        require(axis == "p", "face axis")
        endpoints = [q(x) for x in cell["physical_p_interval"]]
        span = [q(x) for x in geometry["span"]]
        require(span == [q(x) for x in cell["physical_t_interval"]], "p-face exact t span")
    require(endpoints[0] < endpoints[1] and coordinate in endpoints, "face endpoint")
    return axis.upper() + ("_MINUS" if coordinate == endpoints[0] else "_PLUS")


def projected_event(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "row_sha256": row["row_sha256"],
        "origin_key": row["origin_key"],
        "compact_chart": row["compact_chart"],
        "event_kind": row["event_kind"],
        "event_payload_sha256": row["event_payload_sha256"],
        "authority": row["authority"],
        "earliest_first_collision_event": row["earliest_first_collision_event"],
        "round144_terminal_class": row["round144_terminal_class"],
        "round144_terminal_credit": row["round144_terminal_credit"],
        "strict_nonpromotion": row["strict_nonpromotion"],
    }


def projected_exclusion(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "row_sha256": row["row_sha256"],
        "origin_key": row["origin_key"],
        "compact_chart": row["compact_chart"],
        "formal_source_W_disposition": row["formal_source_W_disposition"],
        "disposition_stage": row["disposition_stage"],
        "round144_terminal_class": row["round144_terminal_class"],
        "round144_terminal_credit": row["round144_terminal_credit"],
        "scope_binding": row["scope_binding"],
        "strict_nonpromotion": row["strict_nonpromotion"],
    }


def build() -> dict[str, Any]:
    c33, c34, c35, c36, c37 = (
        validate_result(C33, "C33"), validate_result(C34, "C34"),
        validate_result(C35, "C35"), validate_result(C36, "C36"),
        validate_result(C37, "C37"),
    )
    require(file_sha(C55B_RESULT) == EXPECTED_FILE["C55B"], "C55B file pin")
    c55b = strict_json(C55B_RESULT)
    validate_object(c55b, EXPECTED_OBJECT["C55B"], "C55B")
    require(c55b["exact_unresolved_partition"]["UNANCHORED_SINGLETON_WITHOUT_COMPLETE_EVENT_EXTERIOR_CLOSURE"] == {"component_count": 24, "current_unresolved_cell_count": 24}, "C55B singleton partition")
    for key, value in EXPECTED_C55_LEDGER.items():
        require(c55b["ledgers"][key]["sha256"] == value, f"C55B ledger descriptor:{key}")

    require(file_sha(C55P0) == EXPECTED_FILE["C55P0"], "C55p0 pin")
    c55p0 = strict_json(C55P0)
    require(c55p0["strict_nonpromotion"]["component_isolation_is_not_cemetery"] is True, "isolation lock")
    require(c55p0["strict_nonpromotion"]["reflection_pairing_is_not_terminal_credit"] is True, "reflection lock")
    require(file_sha(C50B_CONTRACT) == EXPECTED_FILE["C50B_CONTRACT"], "C50B contract file")
    c50b = strict_json(C50B_CONTRACT)
    validate_object(c50b, EXPECTED_OBJECT["C50B_CONTRACT"], "C50B contract")
    require(c50b["positive_terminal_enabled"] is False and c50b["terminal_credit"] == 0, "C50B positive terminal lock")
    require(file_sha(C50B_VERIFY) == EXPECTED_FILE["C50B_VERIFY"], "C50B verification file")
    c50bv = strict_json(C50B_VERIFY)
    validate_object(c50bv, EXPECTED_OBJECT["C50B_VERIFY"], "C50B verification")

    cells = read_ledger(C55B_CELLS, c55b["ledgers"]["cell_component_crosswalk"])
    glue = read_ledger(C55B_GLUE, c55b["ledgers"]["component_edges_and_glue"])
    components = read_ledger(C55B_COMPONENTS, c55b["ledgers"]["ordinary_components"])
    singleton_cells = sorted((row for row in cells if row["component_index"] >= 2), key=lambda row: row["component_index"])
    require(len(singleton_cells) == 24 and [row["component_index"] for row in singleton_cells] == list(range(2, 26)), "24 singleton cells")
    require(all(row["current_effective_disposition"] == "UNRESOLVED_R1648_CONTINUATION" for row in singleton_cells), "singleton current status")

    cross_rows = read_ledger(C33 / c33["row_level_crosswalk"]["filename"], c33["row_level_crosswalk"])
    event_rows = read_ledger(C34 / c34["ledgers"]["typed_first_event_bindings"]["filename"], c34["ledgers"]["typed_first_event_bindings"])
    obligations = read_ledger(C36 / c36["ledgers"]["component_refinement_obligations"]["filename"], c36["ledgers"]["component_refinement_obligations"])
    pair_rows = read_ledger(C37 / c37["ledgers"]["ordinary_cell_reflection_pairs"]["filename"], c37["ledgers"]["ordinary_cell_reflection_pairs"])
    cross_by_cell = {row["cell_id"]: row for row in cross_rows}
    event_by_cell = {row["cell_id"]: row for row in event_rows}
    pair_by_index = {row["pair_index"]: row for row in pair_rows}
    require(len(cross_by_cell) == 76832 and len(event_by_cell) == 296 and len(pair_by_index) == 862, "upstream indexing")

    c35_occurrences = read_ledger(C35 / c35["ledgers"]["path_occurrences"]["filename"], c35["ledgers"]["path_occurrences"])
    c36_occurrences = read_ledger(C36 / c36["ledgers"]["occurrence_margin_bindings"]["filename"], c36["ledgers"]["occurrence_margin_bindings"])
    c37_occurrences = read_ledger(C37 / c37["ledgers"]["reflected_r1648_occurrences"]["filename"], c37["ledgers"]["reflected_r1648_occurrences"])
    require(len(c35_occurrences) == len(c36_occurrences) == len(c37_occurrences) == 1648, "R1648 row counts")

    history_writer = LedgerWriter(OUT / HISTORY_FILE, "COLLISION_INDEX_ASCENDING")
    history_rows: list[dict[str, Any]] = []
    shared_keys = (
        "collision_index", "C24_classification", "destination_core_id", "geometry_template_id",
        "incoming_absolute_owner_id", "incoming_chart", "official_word_key_id",
        "official_word_variant_id", "outgoing_chart", "relative_frozen_target_id",
        "selected_absolute_owner_id",
    )
    with history_writer:
        for expected_index, (a, b, c) in enumerate(zip(c35_occurrences, c36_occurrences, c37_occurrences), 1):
            require(a["collision_index"] == b["collision_index"] == c["collision_index"] == expected_index, "collision sequence")
            for key in shared_keys:
                require(a[key] == b[key], f"C35/C36 occurrence field agreement:{expected_index}:{key}")
            require(c["original_occurrence_row_sha256"] == a["row_sha256"], f"C37/C35 binding:{expected_index}")
            require(c["original_C36_margin_binding_row_sha256"] == b["row_sha256"], f"C37/C36 binding:{expected_index}")
            require(c["collar_margin_vectors_sha256"] == b["collar_margin_vectors_sha256"], f"C37/C36 strict margin transport:{expected_index}")
            require(b["owner_discriminant_root_order_word_chart_core_map_status"] == "MATERIALIZED_ON_DUAL_R139_SEED_COLLARS", "C36 scope")
            require(c["owner_discriminant_root_order_word_chart_core_map_status"] == "MATERIALIZED_ON_REFLECTED_DUAL_R139_SEED_COLLARS", "C37 scope")
            row = {
                "schema": HISTORY_SCHEMA,
                "collision_index": expected_index,
                "original_history_tuple": {key: a[key] for key in shared_keys if key != "collision_index"},
                "C35_occurrence_row_sha256": a["row_sha256"],
                "C35_graph_row_sha256": a["graph_row_sha256"],
                "C35_positive_area_row_sha256": a["positive_area_row_sha256"],
                "C36_margin_binding_row_sha256": b["row_sha256"],
                "C36_collar_margin_vectors_sha256": b["collar_margin_vectors_sha256"],
                "C36_scope": b["owner_discriminant_root_order_word_chart_core_map_status"],
                "C36_common_refinement_credit": b["C34_common_refinement_credit"],
                "C37_reflected_occurrence_row_sha256": c["row_sha256"],
                "reflected_history_tuple": {key: c[key] for key in shared_keys if key != "collision_index"},
                "C37_scope": c["owner_discriminant_root_order_word_chart_core_map_status"],
                "horizontal_reflection_preserves_all_strict_margin_values": c["horizontal_reflection_preserves_all_strict_margin_values"],
                "scope_is_seed_collars_not_any_singleton_whole_cell": True,
                "singleton_specific_common_refinement_row_present": False,
                "terminal_credit": 0,
                "D02_gate_credit": 0,
            }
            history_rows.append(history_writer.write(row))
    history_descriptor = history_writer.descriptor()
    history_binding = {
        "ledger_sha256": history_descriptor["sha256"],
        "row_count": 1648,
        "collision_index_range": [1, 1648],
        "row_hash_line_sequence_sha256": history_descriptor["row_hash_line_sequence_sha256"],
        "all_rows_scope_seed_collars_only": True,
        "singleton_specific_materialized_row_count": 0,
        "missing_singleton_collision_index_count": 1648,
        "missing_singleton_collision_index_set_sha256": digest(list(range(1, 1649))),
    }

    glue_by_component: dict[int, list[dict[str, Any]]] = defaultdict(list)
    special_by_component: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in glue:
        for index in row["ordinary_component_indices"]:
            glue_by_component[index].append(row)
            if row["glue_kind"] != "INTRA_CHART_FACE":
                special_by_component[index].append(row)

    singleton_writer = LedgerWriter(OUT / SINGLETON_FILE, "COMPONENT_INDEX_ASCENDING")
    typed_face_total = excluded_face_total = 0
    event_kind_census: Counter[str] = Counter()
    pair_census: Counter[int] = Counter()
    blocker_rows: list[dict[str, Any]] = []
    with singleton_writer:
        for cell in singleton_cells:
            index = cell["component_index"]
            component = components[index]
            obligation = obligations[index]
            require(component["component_index"] == obligation["component_index"] == index, "component index alignment")
            require(component["cell_count"] == obligation["cell_count"] == 1 and component["member_cell_ids"] == [cell["cell_id"]], "singleton membership")
            require(obligation["R1648_occurrence_count"] == obligation["cell_occurrence_refinement_obligation_count"] == 1648, "singleton R1648 obligations")
            require(obligation["geometry_template_count"] == obligation["cell_geometry_template_obligation_count"] == 137, "singleton template obligations")
            require(obligation["official_word_variant_count"] == obligation["cell_word_variant_obligation_count"] == 197, "singleton word obligations")
            require(obligation["common_refinement_status"] == "NOT_MATERIALIZED" and obligation["terminal_typing_status"] == "UNRESOLVED_R1648_CONTINUATION", "singleton obligation open")
            pair = pair_by_index[cell["pair_index"]]
            require(cell["cell_id"] in {pair["representative_cell_id"], pair["reflected_cell_id"]}, "reflection pair membership")
            pair_census[cell["pair_index"]] += 1

            faces = glue_by_component[index]
            require(len(faces) == 4 and not special_by_component[index], "exactly four intra-chart faces and no special glue")
            face_evidence: list[dict[str, Any]] = []
            sides: set[str] = set()
            typed_count = excluded_count = 0
            for face in sorted(faces, key=lambda row: side_for(cell, row)):
                require(face["glue_kind"] == "INTRA_CHART_FACE" and face["dimension"] == 1, "singleton face kind")
                side = side_for(cell, face)
                sides.add(side)
                if face["left_cell_id"] == cell["cell_id"]:
                    neighbor = face["right_cell_id"]
                else:
                    require(face["right_cell_id"] == cell["cell_id"], "singleton incident face")
                    neighbor = face["left_cell_id"]
                evidence: dict[str, Any] = {
                    "boundary_side": side,
                    "neighbor_cell_id": neighbor,
                    "C55B_glue_row_sha256": face["row_sha256"],
                    "C32_upstream_face_row_sha256": face["upstream_row_sha256"],
                    "scope": face["scope"],
                    "exact_geometry": face["exact_geometry"],
                    "gluing_proof_kind": face["gluing_proof_kind"],
                    "dynamic_continuation_credit": 0,
                }
                if face["scope"] == "ORDINARY_TO_TYPED_EVENT_BOUNDARY":
                    event = event_by_cell.get(neighbor)
                    require(event is not None and "TYPED_EVENT_GRAPH" in {face["left_disposition"], face["right_disposition"]}, "typed neighbor")
                    evidence["neighbor_terminal_class"] = "TYPED_EVENT_GRAPH"
                    evidence["typed_event_binding"] = projected_event(event)
                    evidence["boundary_event_is_not_whole_cell_event"] = True
                    typed_count += 1
                    event_kind_census[event["event_kind"]] += 1
                else:
                    require(face["scope"] == "ORDINARY_TO_FORMAL_EXCLUSION_BOUNDARY", "face scope")
                    excluded = cross_by_cell[neighbor]
                    require(excluded["formal_source_W_disposition"] == "EXCLUDED" and excluded["round144_terminal_class"] == "EARLIEST_PREFIX_EXCLUDED", "excluded neighbor")
                    evidence["neighbor_terminal_class"] = "EARLIEST_PREFIX_EXCLUDED"
                    evidence["formal_exclusion_binding"] = projected_exclusion(excluded)
                    evidence["boundary_exclusion_is_not_singleton_continuation_proof"] = True
                    excluded_count += 1
                face_evidence.append(evidence)
            require(sides == {"T_MINUS", "T_PLUS", "P_MINUS", "P_PLUS"}, "closed face inventory")
            require((typed_count, excluded_count) in {(3, 1), (2, 2)}, "singleton face census")
            typed_face_total += typed_count
            excluded_face_total += excluded_count

            exact_blocker = {
                "cell_id": cell["cell_id"],
                "component_index": index,
                "missing_oracle": "GLOBAL_SINGLETON_WHOLE_CELL_DYNAMIC_CONTINUATION_AND_EXTERIOR_DECIDER",
                "missing_singleton_specific_R1648_occurrence_bindings": 1648,
                "missing_collision_index_range": [1, 1648],
                "missing_collision_index_set_sha256": history_binding["missing_singleton_collision_index_set_sha256"],
                "C36_component_common_refinement_status": obligation["common_refinement_status"],
                "C36_component_obligation_row_sha256": obligation["row_sha256"],
                "boundary_typed_event_face_count": typed_count,
                "boundary_formal_exclusion_face_count": excluded_count,
                "source_seam_face_count": 0,
                "source_grazing_face_count": 0,
                "source_grazing_seam_corner_count": 0,
                "reason": "NO_SINGLETON_SPECIFIC_WHOLE_CELL_R1648_COMMON_REFINEMENT_OR_GLOBAL_EXTERIOR_DECISION; BOUNDARY_NEIGHBOR_TERMINALS_DO_NOT_TYPE_THE_CELL_INTERIOR",
            }
            row = {
                "schema": SINGLETON_SCHEMA,
                "component_index": index,
                "component_id": cell["component_id"],
                "cell_id": cell["cell_id"],
                "origin_key": cell["origin_key"],
                "compact_chart": cell["compact_chart"],
                "gate3_chart": cell["gate3_chart"],
                "physical_slice": cell["physical_slice"],
                "physical_t_interval": cell["physical_t_interval"],
                "physical_p_interval": cell["physical_p_interval"],
                "gate3_product_box": cell["gate3_product_box"],
                "C55B_cell_row_sha256": cell["row_sha256"],
                "C55B_component_row_sha256": component["row_sha256"],
                "C36_component_obligation_row_sha256": obligation["row_sha256"],
                "reflection_pair": {
                    "pair_index": cell["pair_index"],
                    "partner_cell_id": cell["reflection_partner_cell_id"],
                    "C37_pair_row_sha256": pair["row_sha256"],
                    "reflection_is_bijective_involution": pair["reflection_is_bijective_involution"],
                    "reflection_pairing_is_not_terminal_credit": True,
                },
                "boundary_face_evidence": face_evidence,
                "boundary_face_census": {"typed_event": typed_count, "formal_exclusion": excluded_count, "total": 4},
                "source_seam_grazing_corner_evidence": [],
                "global_special_glue_inventory_searched": {
                    "C55B_glue_ledger_sha256": c55b["ledgers"]["component_edges_and_glue"]["sha256"],
                    "C55B_glue_ledger_row_count": c55b["ledgers"]["component_edges_and_glue"]["row_count"],
                    "singleton_incident_SOURCE_CHART_TRANSITION_rows": 0,
                    "singleton_incident_SOURCE_GRAZING_FACE_rows": 0,
                    "singleton_incident_SOURCE_GRAZING_SEAM_CORNER_rows": 0,
                },
                "R1648_occurrence_history_binding": history_binding,
                "whole_cell_TYPED_EVENT_GRAPH_proved": False,
                "whole_cell_SOURCE_GRAZING_OR_CEMETERY_proved": False,
                "whole_cell_strict_terminal_class": None,
                "terminal_decision": "UNRESOLVED_R1648_CONTINUATION",
                "exact_blocker": exact_blocker,
                "graph_isolation_used_as_dynamic_continuation": False,
                "boundary_adjacency_used_as_dynamic_continuation": False,
                "formal_credit": 0,
                "D02_gate_credit": 0,
            }
            blocker_rows.append(singleton_writer.write(row))

    require(typed_face_total == 54 and excluded_face_total == 42, "global singleton face census")
    require(sorted(pair_census.values()) == [2] * 12, "12 reflected singleton pairs")
    require(Counter(row["boundary_face_census"]["typed_event"] for row in blocker_rows) == Counter({2: 18, 3: 6}), "typed face distribution")

    singleton_descriptor = singleton_writer.descriptor()
    result: dict[str, Any] = {
        "schema": SCHEMA,
        "status": "PASS_EXACT_AUDIT_24_SINGLETONS__ZERO_WHOLE_CELL_TERMINALS__FAIL_CLOSED_24_UNRESOLVED",
        "authority_pins": {
            "C33_object_sha256": EXPECTED_OBJECT["C33"],
            "C34_object_sha256": EXPECTED_OBJECT["C34"],
            "C35_object_sha256": EXPECTED_OBJECT["C35"],
            "C36_object_sha256": EXPECTED_OBJECT["C36"],
            "C37_object_sha256": EXPECTED_OBJECT["C37"],
            "C55B_file_sha256": EXPECTED_FILE["C55B"],
            "C55B_object_sha256": EXPECTED_OBJECT["C55B"],
            "C55p0_file_sha256": EXPECTED_FILE["C55P0"],
            "C50B_contract_file_sha256": EXPECTED_FILE["C50B_CONTRACT"],
            "C50B_contract_object_sha256": EXPECTED_OBJECT["C50B_CONTRACT"],
            "C50B_independent_verification_object_sha256": EXPECTED_OBJECT["C50B_VERIFY"],
            "C53_effective_checkpoint_object_sha256": c55b["C53_effective_authority"]["effective_checkpoint_object_sha256"],
        },
        "ledgers": {"R1648_history": history_descriptor, "singletons": singleton_descriptor},
        "scope": {
            "input_partition": "C55B.exact_unresolved_partition.UNANCHORED_SINGLETON_WITHOUT_COMPLETE_EVENT_EXTERIOR_CLOSURE",
            "singleton_component_indices": list(range(2, 26)),
            "singleton_cell_count": 24,
            "reflection_pair_indices": sorted(pair_census),
            "reflection_pair_count": 12,
        },
        "R1648_audit": {
            "shared_occurrence_history_rows": 1648,
            "C35_C36_C37_exact_row_chain_verified": True,
            "C36_original_scope": "MATERIALIZED_ON_DUAL_R139_SEED_COLLARS",
            "C37_reflected_scope": "MATERIALIZED_ON_REFLECTED_DUAL_R139_SEED_COLLARS",
            "singleton_specific_common_refinement_rows": 0,
            "per_singleton_missing_occurrences": 1648,
            "total_open_cell_occurrence_obligations": 39552,
        },
        "boundary_census": {
            "complete_intra_chart_faces": 96,
            "typed_event_boundary_faces": typed_face_total,
            "formal_exclusion_boundary_faces": excluded_face_total,
            "singletons_with_3_event_1_exclusion_faces": 6,
            "singletons_with_2_event_2_exclusion_faces": 18,
            "source_chart_transition_faces": 0,
            "source_grazing_faces": 0,
            "source_grazing_seam_corners": 0,
            "typed_event_kind_census": dict(sorted(event_kind_census.items())),
        },
        "terminal_census": {
            "whole_cell_TYPED_EVENT_GRAPH": 0,
            "whole_cell_SOURCE_GRAZING_OR_CEMETERY": 0,
            "UNRESOLVED_R1648_CONTINUATION": 24,
            "closed_singletons": 0,
            "remaining_singletons": 24,
        },
        "per_singleton_exact_blockers": [row["exact_blocker"] for row in blocker_rows],
        "common_shortest_missing_oracle": {
            "name": "GLOBAL_SINGLETON_WHOLE_CELL_DYNAMIC_CONTINUATION_AND_EXTERIOR_DECIDER",
            "minimum_obligations": [
                "COMMON_REFINE_EACH_CLOSED_SINGLETON_CELL_AGAINST_ALL_1648_ORDERED_OCCURRENCE_HISTORIES",
                "RECOMPUTE_EARLIEST_TYPED_EVENT_OR_EXACT_EXTERIOR_SHEET_DECISION_ON_EVERY_RESULTING_LEAF",
                "GLUE_ALL_FACE_CORNER_AND_SOURCE_GRAZING_LEAVES_WITH_EXACT_OWNER_HISTORY",
                "CROSS_BIND_EXTERIOR_COMPONENTS_TO_A_KNOWN_SHEET_OR_STRICT_CEMETERY_CLASS",
                "REQUIRE_SINGLETON_UNRESOLVED_LEAF_COUNT_ZERO_UNDER_INDEPENDENT_NO_PRODUCER_REPLAY",
            ],
            "boundary_event_adjacency_is_not_substitute": True,
            "graph_isolation_is_not_substitute": True,
            "positive_cemetery_decision_currently_disabled_by_C50B": True,
        },
        "strict_nonpromotion": {
            "C50B_positive_terminal_enabled": c50b["positive_terminal_enabled"],
            "component_isolation_promoted": False,
            "boundary_adjacency_promoted": False,
            "reflection_pairing_promoted": False,
            "runtime_writes_performed": False,
            "canonical_writes_performed": False,
        },
        "unresolved_zero": False,
        "strict_decider_eligible": False,
        "credit_locks": {"formal_credit": 0, "D02_gate_credit": 0, "D03_credit": 0, "D04_credit": 0, "Gate5_credit": 0},
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
