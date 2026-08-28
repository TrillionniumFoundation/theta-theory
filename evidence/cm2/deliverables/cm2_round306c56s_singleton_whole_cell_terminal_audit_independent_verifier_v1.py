#!/usr/bin/env python3
"""Independent cold verifier for the C56s singleton audit.

No C56s producer is imported or executed.  The verifier reconstructs the 24
cells, their 96 boundary faces, the C35/C36/C37 R1648 chain and all terminal
locks directly from frozen inert artefacts.
"""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import json
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c56s_singleton_whole_cell_terminal_audit"
RESULT_PATH = OUT / (BASE + "_result_v1.json")
HISTORY_PATH = OUT / (BASE + "_r1648_history_v1.jsonl.gz")
SINGLETON_PATH = OUT / (BASE + "_singleton_ledger_v1.jsonl.gz")
VERIFY_PATH = OUT / (BASE + "_independent_verification_v1.json")
SELFTEST_PATH = OUT / (BASE + "_independent_self_test_v1.json")

C33 = ROOT / ".cm2-runtime/candidates/c33-row-crosswalk-20260810T135223Z-eb0796f41e16d927"
C34 = ROOT / ".cm2-runtime/candidates/c34-seed-event-frontier-20260810T142445Z-6ec6dac7de032cdb"
C35 = ROOT / ".cm2-runtime/candidates/c35-transition-registry-20260810T145204Z-43f2cb35f9817ae2"
C36 = ROOT / ".cm2-runtime/candidates/c36-template-margin-atlas-20260810T153254Z-f37f908cf93d924c"
C37 = ROOT / ".cm2-runtime/candidates/c37-horizontal-reflection-20260810T154802Z-be0d65d5e1cc3c38"
C55_RESULT = OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_result_v1.json"
C55_CELLS = OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_cell_component_crosswalk_v1.jsonl.gz"
C55_GLUE = OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_component_edges_and_glue_v1.jsonl.gz"
C55_COMPONENTS = OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_ordinary_components_v1.jsonl.gz"
C55P0 = OUT / "cm2_round306c55p0_global_strict_decider_input_contract_v1.json"
C50B = OUT / "cm2_round306c50b_d02b_global_cemetery_disconnected_exterior_oracle_contract_v1.json"

PIN = {
    "result_file": "7479c162a7e408bf17ae1f8fc36cbaa41281b8899116549d79010afdfceccc3c",
    "result_object": "c0e90419a49ca4054897b0985933478bea5d6893ae33048176c4c46194e1f6da",
    "history_file": "5b655e71027aa2764c6d16dc9e152fa0444ad0cd541aefdf8812da4cdbd33cd7",
    "history_sequence": "8d521541f6ea68531f7fc432902b2d80d0b1f1d06077b046aff6a39545fc29e8",
    "singleton_file": "077cca660b0ce5b2dfaf5f3bffd7302b88e19cb3839d1d094f5b34489ab7714c",
    "singleton_sequence": "ae9c8a08d137e1bb11d37ae569ae0492701f3aa73355dfaa83d6108f02945af3",
    "C55_result_file": "6bf9cae7b4b422c5c2121f95828e1508700fe1a5d1b1128598c8617f65032a93",
    "C55_result_object": "1ce396e9746d3c0364325e8308e94c9dcd4a3bfbba8c17a9c9961915e807cc56",
    "C55p0_file": "0e2a7b713f3c4c007c65a27a42079ca33b024b8489b5dfd149312fcd5702333b",
    "C50b_file": "25248a20e5a81f5119b204d856ef61ce18c2307412f3b304f2bb35213729ce1e",
}
UPSTREAM_OBJECT = {
    "C33": "82dedeace982db89763e8a7e318fa6605d18cadc6bf390d6b23585d0922b87a0",
    "C34": "1c75d245a20bac35a0e33249f921ee862ad3c1397e78817189699dcc28552d2e",
    "C35": "cb524ae587390a578683c88d933125e041ab2a906f0351370d58f3b0d67aa752",
    "C36": "9251693da7d6cc0ff6011fb965276ac64be2b79be8f245ab8954291a43fb4167",
    "C37": "d6333d60d045dd60d93560b75f6332324c8a8bc131024e7e8100704aa2d89d2b",
}


class Reject(RuntimeError):
    pass


def must(value: bool, reason: str) -> None:
    if not value:
        raise Reject(reason)


def canon(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def objhash(value: Any) -> str:
    return hashlib.sha256(canon(value)).hexdigest()


def filesha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, val in items:
            must(key not in out, f"duplicate key:{path}:{key}")
            out[key] = val
        return out
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle, object_pairs_hook=pairs)
    must(isinstance(value, dict), f"JSON object:{path}")
    return value


def check_object(value: dict[str, Any], expected: str, label: str) -> None:
    body = dict(value)
    claim = body.pop("object_sha256", body.pop("result_sha256", None))
    must(claim == expected and objhash(body) == expected, f"object:{label}")


def upstream_result(directory: Path, expected: str, label: str) -> dict[str, Any]:
    value = load_json(directory / "result.json")
    check_object(value, expected, label)
    return value


def closed_rows(path: Path, descriptor: dict[str, Any]) -> list[dict[str, Any]]:
    must(filesha(path) == descriptor["sha256"], f"ledger file:{path}")
    rows: list[dict[str, Any]] = []
    sequence = hashlib.sha256()
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            claim = row.pop("row_sha256", None)
            must(claim is not None and objhash(row) == claim, f"ledger row:{path}")
            row["row_sha256"] = claim
            rows.append(row)
            sequence.update((claim + "\n").encode("ascii"))
    must(len(rows) == descriptor["row_count"], f"ledger count:{path}")
    must(sequence.hexdigest() == descriptor["row_hash_line_sequence_sha256"], f"ledger sequence:{path}")
    return rows


def rat(value: Any) -> Fraction:
    if isinstance(value, dict):
        must(value.get("kind") == "RATIONAL", "coordinate type")
        value = value["value"]
    return Fraction(str(value))


def boundary_side(cell: dict[str, Any], glue: dict[str, Any]) -> str:
    geometry = glue["exact_geometry"]
    axis = geometry["axis"]
    must(axis in {"t", "p"}, "face axis")
    if axis == "t":
        endpoints = [rat(x) for x in cell["physical_t_interval"]]
        expected_span = [rat(x) for x in cell["physical_p_interval"]]
    else:
        endpoints = [rat(x) for x in cell["physical_p_interval"]]
        expected_span = [rat(x) for x in cell["physical_t_interval"]]
    must(endpoints[0] < endpoints[1], "positive interval")
    must([rat(x) for x in geometry["span"]] == expected_span, "complete face span")
    coordinate = rat(geometry["coordinate"])
    must(coordinate in endpoints, "boundary coordinate")
    return axis.upper() + ("_MINUS" if coordinate == endpoints[0] else "_PLUS")


def event_projection(row: dict[str, Any]) -> dict[str, Any]:
    keys = ("row_sha256", "origin_key", "compact_chart", "event_kind", "event_payload_sha256", "authority", "earliest_first_collision_event", "round144_terminal_class", "round144_terminal_credit", "strict_nonpromotion")
    return {key: row[key] for key in keys}


def exclusion_projection(row: dict[str, Any]) -> dict[str, Any]:
    keys = ("row_sha256", "origin_key", "compact_chart", "formal_source_W_disposition", "disposition_stage", "round144_terminal_class", "round144_terminal_credit", "scope_binding", "strict_nonpromotion")
    return {key: row[key] for key in keys}


def load_context() -> dict[str, Any]:
    c33 = upstream_result(C33, UPSTREAM_OBJECT["C33"], "C33")
    c34 = upstream_result(C34, UPSTREAM_OBJECT["C34"], "C34")
    c35 = upstream_result(C35, UPSTREAM_OBJECT["C35"], "C35")
    c36 = upstream_result(C36, UPSTREAM_OBJECT["C36"], "C36")
    c37 = upstream_result(C37, UPSTREAM_OBJECT["C37"], "C37")

    must(filesha(C55_RESULT) == PIN["C55_result_file"], "C55 result file")
    c55 = load_json(C55_RESULT)
    check_object(c55, PIN["C55_result_object"], "C55")
    cells = closed_rows(C55_CELLS, c55["ledgers"]["cell_component_crosswalk"])
    glue = closed_rows(C55_GLUE, c55["ledgers"]["component_edges_and_glue"])
    components = closed_rows(C55_COMPONENTS, c55["ledgers"]["ordinary_components"])
    cross = closed_rows(C33 / c33["row_level_crosswalk"]["filename"], c33["row_level_crosswalk"])
    events = closed_rows(C34 / c34["ledgers"]["typed_first_event_bindings"]["filename"], c34["ledgers"]["typed_first_event_bindings"])
    obligations = closed_rows(C36 / c36["ledgers"]["component_refinement_obligations"]["filename"], c36["ledgers"]["component_refinement_obligations"])
    pairs = closed_rows(C37 / c37["ledgers"]["ordinary_cell_reflection_pairs"]["filename"], c37["ledgers"]["ordinary_cell_reflection_pairs"])
    a = closed_rows(C35 / c35["ledgers"]["path_occurrences"]["filename"], c35["ledgers"]["path_occurrences"])
    b = closed_rows(C36 / c36["ledgers"]["occurrence_margin_bindings"]["filename"], c36["ledgers"]["occurrence_margin_bindings"])
    c = closed_rows(C37 / c37["ledgers"]["reflected_r1648_occurrences"]["filename"], c37["ledgers"]["reflected_r1648_occurrences"])
    must(filesha(C55P0) == PIN["C55p0_file"], "C55p0 file")
    p0 = load_json(C55P0)
    must(p0["strict_nonpromotion"]["component_isolation_is_not_cemetery"] and p0["strict_nonpromotion"]["reflection_pairing_is_not_terminal_credit"], "P0 locks")
    must(filesha(C50B) == PIN["C50b_file"], "C50b file")
    c50 = load_json(C50B)
    must(c50["positive_terminal_enabled"] is False and c50["terminal_credit"] == 0, "C50b lock")
    return {
        "c55": c55,
        "cells": {row["component_index"]: row for row in cells if row["component_index"] >= 2},
        "glue": glue,
        "components": {row["component_index"]: row for row in components},
        "cross": {row["cell_id"]: row for row in cross},
        "events": {row["cell_id"]: row for row in events},
        "obligations": {row["component_index"]: row for row in obligations},
        "pairs": {row["pair_index"]: row for row in pairs},
        "occurrences": (a, b, c),
        "c50": c50,
    }


def expected_face_evidence(cell: dict[str, Any], ctx: dict[str, Any]) -> list[dict[str, Any]]:
    incident = [g for g in ctx["glue"] if cell["component_index"] in g["ordinary_component_indices"]]
    must(len(incident) == 4 and all(g["glue_kind"] == "INTRA_CHART_FACE" for g in incident), "singleton incident faces")
    out: list[dict[str, Any]] = []
    for face in sorted(incident, key=lambda g: boundary_side(cell, g)):
        side = boundary_side(cell, face)
        neighbor = face["right_cell_id"] if face["left_cell_id"] == cell["cell_id"] else face["left_cell_id"]
        value: dict[str, Any] = {
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
            event = ctx["events"].get(neighbor)
            must(event is not None and event["round144_terminal_class"] == "TYPED_EVENT_GRAPH", "event neighbor")
            value.update({"neighbor_terminal_class": "TYPED_EVENT_GRAPH", "typed_event_binding": event_projection(event), "boundary_event_is_not_whole_cell_event": True})
        else:
            must(face["scope"] == "ORDINARY_TO_FORMAL_EXCLUSION_BOUNDARY", "boundary scope")
            excluded = ctx["cross"][neighbor]
            must(excluded["formal_source_W_disposition"] == "EXCLUDED", "excluded neighbor")
            value.update({"neighbor_terminal_class": "EARLIEST_PREFIX_EXCLUDED", "formal_exclusion_binding": exclusion_projection(excluded), "boundary_exclusion_is_not_singleton_continuation_proof": True})
        out.append(value)
    must({x["boundary_side"] for x in out} == {"T_MINUS", "T_PLUS", "P_MINUS", "P_PLUS"}, "four sides")
    return out


def check_closed_row(row: dict[str, Any], label: str) -> None:
    body = dict(row)
    claim = body.pop("row_sha256", None)
    must(claim is not None and objhash(body) == claim, f"closed row:{label}")


def semantic_check(result: dict[str, Any], histories: list[dict[str, Any]], singletons: list[dict[str, Any]], ctx: dict[str, Any]) -> None:
    body = dict(result)
    claim = body.pop("object_sha256", None)
    must(claim is not None and objhash(body) == claim, "result object closure")
    must(len(histories) == 1648 and len(singletons) == 24, "output row counts")
    a_rows, b_rows, c_rows = ctx["occurrences"]
    original_keys = ("C24_classification", "destination_core_id", "geometry_template_id", "incoming_absolute_owner_id", "incoming_chart", "official_word_key_id", "official_word_variant_id", "outgoing_chart", "relative_frozen_target_id", "selected_absolute_owner_id")
    for index, (row, a, b, c) in enumerate(zip(histories, a_rows, b_rows, c_rows), 1):
        check_closed_row(row, f"history:{index}")
        must(row["collision_index"] == a["collision_index"] == b["collision_index"] == c["collision_index"] == index, "history collision")
        must(row["original_history_tuple"] == {key: a[key] for key in original_keys}, "original history tuple")
        must(row["reflected_history_tuple"] == {key: c[key] for key in original_keys}, "reflected history tuple")
        must(row["C35_occurrence_row_sha256"] == a["row_sha256"] and row["C36_margin_binding_row_sha256"] == b["row_sha256"] and row["C37_reflected_occurrence_row_sha256"] == c["row_sha256"], "R1648 row chain")
        must(c["original_occurrence_row_sha256"] == a["row_sha256"] and c["original_C36_margin_binding_row_sha256"] == b["row_sha256"], "upstream R1648 links")
        must(row["C36_collar_margin_vectors_sha256"] == b["collar_margin_vectors_sha256"] == c["collar_margin_vectors_sha256"], "margin transport")
        must(row["C36_scope"] == "MATERIALIZED_ON_DUAL_R139_SEED_COLLARS" and row["C37_scope"] == "MATERIALIZED_ON_REFLECTED_DUAL_R139_SEED_COLLARS", "collar-only scopes")
        must(row["scope_is_seed_collars_not_any_singleton_whole_cell"] is True and row["singleton_specific_common_refinement_row_present"] is False, "history scope lock")
        must(row["terminal_credit"] == row["D02_gate_credit"] == 0, "history credit")

    missing_hash = objhash(list(range(1, 1649)))
    event_faces = exclusion_faces = 0
    seen_pairs: Counter[int] = Counter()
    blockers: list[dict[str, Any]] = []
    for expected_index, row in zip(range(2, 26), singletons):
        check_closed_row(row, f"singleton:{expected_index}")
        cell = ctx["cells"][expected_index]
        component = ctx["components"][expected_index]
        obligation = ctx["obligations"][expected_index]
        must(row["component_index"] == expected_index and row["cell_id"] == cell["cell_id"] and row["component_id"] == cell["component_id"], "singleton identity")
        for key in ("origin_key", "compact_chart", "gate3_chart", "physical_slice", "physical_t_interval", "physical_p_interval", "gate3_product_box"):
            must(row[key] == cell[key], f"singleton geometry:{key}")
        must(row["C55B_cell_row_sha256"] == cell["row_sha256"] and row["C55B_component_row_sha256"] == component["row_sha256"], "C55 row binding")
        must(row["C36_component_obligation_row_sha256"] == obligation["row_sha256"], "C36 obligation binding")
        must(obligation["cell_occurrence_refinement_obligation_count"] == 1648 and obligation["common_refinement_status"] == "NOT_MATERIALIZED", "open refinement obligation")
        pair = ctx["pairs"][cell["pair_index"]]
        must(row["reflection_pair"] == {"pair_index": cell["pair_index"], "partner_cell_id": cell["reflection_partner_cell_id"], "C37_pair_row_sha256": pair["row_sha256"], "reflection_is_bijective_involution": True, "reflection_pairing_is_not_terminal_credit": True}, "reflection binding")
        expected_faces = expected_face_evidence(cell, ctx)
        must(row["boundary_face_evidence"] == expected_faces, "exact face evidence")
        typed = sum(x["scope"] == "ORDINARY_TO_TYPED_EVENT_BOUNDARY" for x in expected_faces)
        excluded = 4 - typed
        must(row["boundary_face_census"] == {"typed_event": typed, "formal_exclusion": excluded, "total": 4}, "face census")
        event_faces += typed
        exclusion_faces += excluded
        seen_pairs[cell["pair_index"]] += 1
        must(row["source_seam_grazing_corner_evidence"] == [], "empty special glue")
        inventory = row["global_special_glue_inventory_searched"]
        must(inventory["singleton_incident_SOURCE_CHART_TRANSITION_rows"] == inventory["singleton_incident_SOURCE_GRAZING_FACE_rows"] == inventory["singleton_incident_SOURCE_GRAZING_SEAM_CORNER_rows"] == 0, "no special glue")
        history = row["R1648_occurrence_history_binding"]
        must(history["row_count"] == 1648 and history["collision_index_range"] == [1, 1648] and history["missing_singleton_collision_index_count"] == 1648, "singleton history range")
        must(history["missing_singleton_collision_index_set_sha256"] == missing_hash and history["singleton_specific_materialized_row_count"] == 0 and history["all_rows_scope_seed_collars_only"] is True, "singleton history gap")
        must(row["whole_cell_TYPED_EVENT_GRAPH_proved"] is False and row["whole_cell_SOURCE_GRAZING_OR_CEMETERY_proved"] is False and row["whole_cell_strict_terminal_class"] is None, "no whole-cell terminal")
        must(row["terminal_decision"] == "UNRESOLVED_R1648_CONTINUATION", "unresolved decision")
        must(row["graph_isolation_used_as_dynamic_continuation"] is False and row["boundary_adjacency_used_as_dynamic_continuation"] is False, "shortcut locks")
        must(row["formal_credit"] == row["D02_gate_credit"] == 0, "singleton credits")
        blocker = row["exact_blocker"]
        must(blocker["cell_id"] == cell["cell_id"] and blocker["component_index"] == expected_index, "blocker identity")
        must(blocker["missing_oracle"] == "GLOBAL_SINGLETON_WHOLE_CELL_DYNAMIC_CONTINUATION_AND_EXTERIOR_DECIDER" and blocker["missing_singleton_specific_R1648_occurrence_bindings"] == 1648, "blocker oracle")
        must(blocker["C36_component_common_refinement_status"] == "NOT_MATERIALIZED" and blocker["boundary_typed_event_face_count"] == typed and blocker["boundary_formal_exclusion_face_count"] == excluded, "blocker exact counts")
        must(blocker["source_seam_face_count"] == blocker["source_grazing_face_count"] == blocker["source_grazing_seam_corner_count"] == 0, "blocker special counts")
        blockers.append(blocker)
    must(event_faces == 54 and exclusion_faces == 42 and sorted(seen_pairs.values()) == [2] * 12, "singleton global reconstruction")
    must(result["status"] == "PASS_EXACT_AUDIT_24_SINGLETONS__ZERO_WHOLE_CELL_TERMINALS__FAIL_CLOSED_24_UNRESOLVED", "result status")
    must(result["terminal_census"] == {"whole_cell_TYPED_EVENT_GRAPH": 0, "whole_cell_SOURCE_GRAZING_OR_CEMETERY": 0, "UNRESOLVED_R1648_CONTINUATION": 24, "closed_singletons": 0, "remaining_singletons": 24}, "terminal census")
    must(result["boundary_census"]["complete_intra_chart_faces"] == 96 and result["boundary_census"]["typed_event_boundary_faces"] == 54 and result["boundary_census"]["formal_exclusion_boundary_faces"] == 42, "result boundary census")
    must(result["R1648_audit"]["singleton_specific_common_refinement_rows"] == 0 and result["R1648_audit"]["total_open_cell_occurrence_obligations"] == 39552, "result R1648 census")
    must(result["per_singleton_exact_blockers"] == blockers, "result blockers")
    must(result["common_shortest_missing_oracle"]["name"] == "GLOBAL_SINGLETON_WHOLE_CELL_DYNAMIC_CONTINUATION_AND_EXTERIOR_DECIDER", "common missing oracle")
    must(result["common_shortest_missing_oracle"]["boundary_event_adjacency_is_not_substitute"] is True and result["common_shortest_missing_oracle"]["graph_isolation_is_not_substitute"] is True, "common shortcut locks")
    must(result["strict_nonpromotion"]["C50B_positive_terminal_enabled"] is False and result["strict_nonpromotion"]["runtime_writes_performed"] is False and result["strict_nonpromotion"]["canonical_writes_performed"] is False, "nonpromotion")
    must(result["unresolved_zero"] is False and result["strict_decider_eligible"] is False and all(x == 0 for x in result["credit_locks"].values()), "global credit locks")


def load_bundle(check_pins: bool = True) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    if check_pins:
        must(filesha(RESULT_PATH) == PIN["result_file"], "result file pin")
        must(filesha(HISTORY_PATH) == PIN["history_file"], "history file pin")
        must(filesha(SINGLETON_PATH) == PIN["singleton_file"], "singleton file pin")
    result = load_json(RESULT_PATH)
    if check_pins:
        check_object(result, PIN["result_object"], "C56s result")
        must(result["ledgers"]["R1648_history"]["row_hash_line_sequence_sha256"] == PIN["history_sequence"], "history sequence pin")
        must(result["ledgers"]["singletons"]["row_hash_line_sequence_sha256"] == PIN["singleton_sequence"], "singleton sequence pin")
    histories = closed_rows(HISTORY_PATH, result["ledgers"]["R1648_history"])
    singletons = closed_rows(SINGLETON_PATH, result["ledgers"]["singletons"])
    return result, histories, singletons


def reclose(row: dict[str, Any]) -> None:
    row.pop("row_sha256", None)
    row["row_sha256"] = objhash(row)


def reclose_result(result: dict[str, Any]) -> None:
    result.pop("object_sha256", None)
    result["object_sha256"] = objhash(result)


def self_test(ctx: dict[str, Any], baseline: tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]) -> dict[str, Any]:
    attacks: list[tuple[str, Callable[[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]], None]]] = []
    attacks.append(("DROP_HISTORY_ROW", lambda r, h, s: h.pop()))
    attacks.append(("REORDER_HISTORY_ROWS", lambda r, h, s: h.__setitem__(slice(0, 2), [h[1], h[0]])))
    attacks.append(("MUTATE_COLLISION_INDEX", lambda r, h, s: h[0].__setitem__("collision_index", 2)))
    attacks.append(("MUTATE_C35_BINDING", lambda r, h, s: h[0].__setitem__("C35_occurrence_row_sha256", "0" * 64)))
    attacks.append(("MUTATE_C36_BINDING", lambda r, h, s: h[0].__setitem__("C36_margin_binding_row_sha256", "1" * 64)))
    attacks.append(("MUTATE_C37_BINDING", lambda r, h, s: h[0].__setitem__("C37_reflected_occurrence_row_sha256", "2" * 64)))
    attacks.append(("PROMOTE_HISTORY_SCOPE", lambda r, h, s: h[0].__setitem__("singleton_specific_common_refinement_row_present", True)))
    attacks.append(("PROMOTE_HISTORY_CREDIT", lambda r, h, s: h[0].__setitem__("terminal_credit", 1)))
    attacks.append(("DROP_SINGLETON", lambda r, h, s: s.pop()))
    attacks.append(("DUPLICATE_COMPONENT", lambda r, h, s: s[1].__setitem__("component_index", 2)))
    attacks.append(("REMOVE_BOUNDARY_FACE", lambda r, h, s: s[0]["boundary_face_evidence"].pop()))
    attacks.append(("MUTATE_FACE_GEOMETRY", lambda r, h, s: s[0]["boundary_face_evidence"][0]["exact_geometry"].__setitem__("coordinate", {"kind": "RATIONAL", "value": "0"})))
    attacks.append(("MUTATE_FACE_NEIGHBOR", lambda r, h, s: s[0]["boundary_face_evidence"][0].__setitem__("neighbor_cell_id", "forged")))
    attacks.append(("PROMOTE_BOUNDARY_EVENT_TO_WHOLE", lambda r, h, s: s[0].__setitem__("whole_cell_TYPED_EVENT_GRAPH_proved", True)))
    attacks.append(("PROMOTE_CEMETERY_WITHOUT_DECIDER", lambda r, h, s: s[0].__setitem__("whole_cell_SOURCE_GRAZING_OR_CEMETERY_proved", True)))
    attacks.append(("INJECT_STRICT_TERMINAL_CLASS", lambda r, h, s: s[0].__setitem__("whole_cell_strict_terminal_class", "TYPED_EVENT_GRAPH")))
    attacks.append(("USE_BOUNDARY_ADJACENCY_SHORTCUT", lambda r, h, s: s[0].__setitem__("boundary_adjacency_used_as_dynamic_continuation", True)))
    attacks.append(("USE_GRAPH_ISOLATION_SHORTCUT", lambda r, h, s: s[0].__setitem__("graph_isolation_used_as_dynamic_continuation", True)))
    attacks.append(("FORGE_MISSING_OCCURRENCE_COUNT", lambda r, h, s: s[0]["R1648_occurrence_history_binding"].__setitem__("missing_singleton_collision_index_count", 1647)))
    attacks.append(("FORGE_C36_MATERIALIZATION", lambda r, h, s: s[0]["exact_blocker"].__setitem__("C36_component_common_refinement_status", "MATERIALIZED")))
    attacks.append(("FORGE_SINGLETON_CREDIT", lambda r, h, s: s[0].__setitem__("D02_gate_credit", 1)))
    attacks.append(("FORGE_TERMINAL_CENSUS", lambda r, h, s: r["terminal_census"].__setitem__("closed_singletons", 1)))
    attacks.append(("FORGE_UNRESOLVED_ZERO", lambda r, h, s: r.__setitem__("unresolved_zero", True)))
    attacks.append(("FORGE_STRICT_DECIDER_ELIGIBLE", lambda r, h, s: r.__setitem__("strict_decider_eligible", True)))
    attacks.append(("REMOVE_COMMON_ORACLE", lambda r, h, s: r["common_shortest_missing_oracle"].__setitem__("name", None)))
    attacks.append(("PROMOTE_GLOBAL_CREDIT", lambda r, h, s: r["credit_locks"].__setitem__("D02_gate_credit", 1)))

    passed: list[dict[str, Any]] = []
    for name, mutation in attacks:
        result, histories, singletons = copy.deepcopy(baseline)
        mutation(result, histories, singletons)
        for row in histories:
            reclose(row)
        for row in singletons:
            reclose(row)
        reclose_result(result)
        try:
            semantic_check(result, histories, singletons, ctx)
        except Reject as exc:
            passed.append({"attack": name, "status": "PASS_FAIL_CLOSED", "rejection": str(exc)})
        else:
            raise Reject(f"attack accepted:{name}")
    output: dict[str, Any] = {
        "schema": "cm2.round306c56s.singleton-whole-cell-terminal-audit.v1.independent-self-test",
        "status": f"PASS_{len(passed)}_OF_{len(attacks)}_COHERENT_ATTACKS_FAIL_CLOSED",
        "attack_count": len(attacks),
        "passed_count": len(passed),
        "attacks": passed,
        "producer_imported_or_executed": False,
    }
    output["object_sha256"] = objhash(output)
    return output


def verify() -> tuple[dict[str, Any], dict[str, Any]]:
    ctx = load_context()
    bundle = load_bundle(True)
    semantic_check(*bundle, ctx)
    tests = self_test(ctx, bundle)
    verification: dict[str, Any] = {
        "schema": "cm2.round306c56s.singleton-whole-cell-terminal-audit.v1.independent-verification",
        "status": "PASS_INDEPENDENT_NO_PRODUCER_RECONSTRUCTION__24_SINGLETONS__96_FACES__1648_HISTORY_ROWS__ZERO_TERMINALS",
        "verified_C56s_result_file_sha256": PIN["result_file"],
        "verified_C56s_result_object_sha256": PIN["result_object"],
        "verified_history_file_sha256": PIN["history_file"],
        "verified_singleton_file_sha256": PIN["singleton_file"],
        "reconstruction": {
            "R1648_rows": 1648,
            "singleton_rows": 24,
            "boundary_faces": 96,
            "typed_event_boundary_faces": 54,
            "formal_exclusion_boundary_faces": 42,
            "reflection_pairs": 12,
            "whole_cell_TYPED_EVENT_GRAPH": 0,
            "whole_cell_SOURCE_GRAZING_OR_CEMETERY": 0,
            "UNRESOLVED_R1648_CONTINUATION": 24,
        },
        "hostile_tests": {"passed": tests["passed_count"], "total": tests["attack_count"], "self_test_object_sha256": tests["object_sha256"]},
        "producer_imported_or_executed": False,
        "runtime_writes_performed": False,
        "canonical_writes_performed": False,
        "formal_credit": 0,
        "D02_gate_credit": 0,
    }
    verification["object_sha256"] = objhash(verification)
    return verification, tests


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    must(args.verify or args.self_test, "use --verify and/or --self-test")
    verification, tests = verify()
    if args.self_test or args.verify:
        SELFTEST_PATH.write_bytes(canon(tests) + b"\n")
    if args.verify:
        VERIFY_PATH.write_bytes(canon(verification) + b"\n")
        print(json.dumps({"status": verification["status"], "object_sha256": verification["object_sha256"], "hostile_tests": verification["hostile_tests"]}, sort_keys=True, separators=(",", ":")))
    else:
        print(json.dumps({"status": tests["status"], "object_sha256": tests["object_sha256"]}, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Reject as exc:
        print(json.dumps({"status": "FAIL_CLOSED", "reason": str(exc)}, sort_keys=True, separators=(",", ":")))
        raise SystemExit(1)
