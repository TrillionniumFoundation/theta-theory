#!/usr/bin/env python3
"""Independent, no-producer verifier for the C55-B component ledger."""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import json
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
PREFIX = "cm2_round306c55b_global_component_adjacency_known_sheet"
RESULT_PATH = OUT / (PREFIX + "_result_v1.json")
VERIFY_PATH = OUT / (PREFIX + "_independent_verification_v1.json")
SELF_TEST_PATH = OUT / (PREFIX + "_independent_self_test_v1.json")
PRODUCER_PATH = OUT / (PREFIX + "_ledger_v1.py")

SCHEMA = "cm2.round306c55b.global-component-adjacency-known-sheet-ledger.v1"
CELL_SCHEMA = SCHEMA + ".cell-component-crosswalk-row"
GLUE_SCHEMA = SCHEMA + ".component-edge-and-glue-row"
COMPONENT_SCHEMA = SCHEMA + ".ordinary-component-row"
VERIFY_SCHEMA = SCHEMA + ".independent-verification.v1"

C32 = ROOT / ".cm2-runtime/candidates/c32-four-chart-atlas-20260810T133217Z-3c4d0dff259783c9"
C33 = ROOT / ".cm2-runtime/candidates/c33-row-crosswalk-20260810T135223Z-eb0796f41e16d927"
C34 = ROOT / ".cm2-runtime/candidates/c34-seed-event-frontier-20260810T142445Z-6ec6dac7de032cdb"
C37 = ROOT / ".cm2-runtime/candidates/c37-horizontal-reflection-20260810T154802Z-be0d65d5e1cc3c38"
C42 = ROOT / ".cm2-runtime/candidates/c42-p391-formal-producer-20260811T044500Z-f1"
C53_AUDIT = OUT / "cm2_round306c53_d02a_pair1_pair_level_successor_independent_audit_v1.json"
C53_HEAD = ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"
C55P0 = OUT / "cm2_round306c55p0_global_strict_decider_input_contract_v1.json"

EXPECTED = {
    "C32": "32ff9e0f90a12f17b16f67086eabda0986a0d52d185bea0c5c16e20518ca1474",
    "C33": "82dedeace982db89763e8a7e318fa6605d18cadc6bf390d6b23585d0922b87a0",
    "C34": "1c75d245a20bac35a0e33249f921ee862ad3c1397e78817189699dcc28552d2e",
    "C37": "d6333d60d045dd60d93560b75f6332324c8a8bc131024e7e8100704aa2d89d2b",
    "C42": "a50914a266aff3396054d7f16e91d69db7fa735ad15f01cbf07eee8e708d99d2",
    "C53_AUDIT": "a7bee7e57b6527c7bf9ea7f17966379c62a722fe9ce2ce2009f19f85a5afaa7c",
    "HEAD_FILE": "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3",
    "HEAD_OBJECT": "cb90ab914c3b6518384669f42d05df33c21a717596190131c6a0f5683934cbfb",
    "CHECKPOINT": "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab",
    "CONTRACT_FILE": "0e2a7b713f3c4c007c65a27a42079ca33b024b8489b5dfd149312fcd5702333b",
}

RESULT_KEYS = {
    "schema", "status", "C53_effective_authority", "authority_pins", "inventory",
    "ledgers", "base_atlas_census", "current_effective_census",
    "known_sheet_anchor_census", "exact_unresolved_partition",
    "reconstruction_invariants", "forbidden_shortcuts", "global_closure_proved",
    "unresolved_zero", "strict_decider_eligible", "credit_locks", "required_next",
    "object_sha256",
}
CELL_KEYS = {
    "schema", "cell_id", "origin_key", "compact_chart", "gate3_chart",
    "physical_slice", "physical_t_interval", "physical_p_interval", "gate3_product_box",
    "C32_cell_row_sha256", "C33_crosswalk_row_sha256", "component_index",
    "component_id", "C34_component_row_sha256", "pair_index",
    "reflection_partner_cell_id", "C37_pair_row_sha256", "C42_parent_row_sha256",
    "C53_parent_projection_object_sha256", "whole_pair_terminal_after_C53",
    "newly_whole_by_C53_pair_seal", "current_effective_disposition",
    "known_sheet_anchor_role", "coordinate_or_key_coincidence_used",
    "whole_cell_connected_to_known_credit", "D02_gate_credit", "row_sha256",
}
COMPONENT_KEYS = {
    "schema", "component_index", "component_id", "C34_component_row_sha256",
    "cell_count", "member_cell_ids", "member_cell_ids_sha256",
    "member_cell_row_sha256s", "member_cell_row_sequence_sha256",
    "internal_face_connected", "edge_and_glue_row_sha256s",
    "edge_and_glue_row_sequence_sha256", "known_sheet_anchor",
    "anchor_is_strict_subset_not_whole_component", "positive_area_anchor_proof_present",
    "common_refinement_status", "current_excluded_cell_count",
    "current_excluded_cell_ids_sha256", "current_unresolved_cell_count",
    "current_unresolved_cell_ids_sha256", "whole_component_terminal_class",
    "whole_component_connected_to_known_credit", "unresolved_reason",
    "singleton_isolation_promoted", "coordinate_or_key_coincidence_used",
    "D02_gate_credit", "row_sha256",
}
GLUE_COMMON = {
    "schema", "glue_kind", "scope", "face_or_corner_id", "dimension",
    "left_cell_id", "right_cell_id", "left_disposition", "right_disposition",
    "ordinary_component_indices", "exact_geometry", "upstream_row_sha256",
    "gluing_proof_kind", "coordinate_or_key_coincidence_used", "terminal_credit",
    "row_sha256",
}


class FailClosed(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise FailClosed(message)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


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
        out: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in out, f"duplicate key:{path}:{key}")
            out[key] = value
        return out
    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=hook)
    require(isinstance(value, dict), f"object required:{path}")
    return value


def validate_object(value: dict[str, Any], expected: str, label: str) -> None:
    body = dict(value)
    claimed = body.pop("object_sha256", None)
    require(claimed == expected and digest(body) == expected, f"object:{label}")


def validate_result(directory: Path, expected: str, label: str) -> dict[str, Any]:
    value = strict_json(directory / "result.json")
    validate_object(value, expected, label)
    return value


def read_rows(path: Path, descriptor: dict[str, Any], closed_keys: set[str] | None = None) -> list[dict[str, Any]]:
    require(path.name == descriptor["filename"] and file_sha(path) == descriptor["sha256"], f"ledger file:{path}")
    rows: list[dict[str, Any]] = []
    sequence = hashlib.sha256()
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        for line in stream:
            row = json.loads(line)
            require(isinstance(row, dict) and "row_sha256" in row, f"row:{path}")
            if closed_keys is not None:
                require(set(row) == closed_keys, f"closed row schema:{path}")
            body = dict(row)
            claimed = body.pop("row_sha256")
            require(digest(body) == claimed, f"row hash:{path}")
            sequence.update((claimed + "\n").encode("ascii"))
            rows.append(row)
    require(len(rows) == descriptor["row_count"], f"row count:{path}")
    require(sequence.hexdigest() == descriptor["row_hash_line_sequence_sha256"], f"row sequence:{path}")
    return rows


def upstream_rows(directory: Path, descriptor: dict[str, Any]) -> list[dict[str, Any]]:
    return read_rows(directory / descriptor["filename"], descriptor)


def validate_fail_closed_model(result: dict[str, Any], components: list[dict[str, Any]], glues: list[dict[str, Any]]) -> None:
    require(set(result) == RESULT_KEYS and result["schema"] == SCHEMA, "result schema")
    require(result["global_closure_proved"] is False, "global closure must remain false")
    require(result["unresolved_zero"] is False, "unresolved-zero must remain false")
    require(result["strict_decider_eligible"] is False, "strict decider must remain ineligible")
    require(set(result["credit_locks"].values()) == {0}, "credit locks")
    require(result["known_sheet_anchor_census"] == {
        "components_with_strict_open_connected_collar": 2,
        "components_with_whole_component_connected_proof": 0,
        "unanchored_singleton_components": 24,
        "anchor_credit": 0,
    }, "anchor census")
    part = result["exact_unresolved_partition"]
    require(part["partition_disjoint_and_exhaustive"] is True and part["total_component_count"] == 26 and part["total_current_unresolved_cell_count"] == 1148, "unresolved partition")
    require(part["ANCHORED_COMPONENT_WITHOUT_WHOLE_COMMON_REFINEMENT"] == {"component_count": 2, "current_unresolved_cell_count": 1124}, "anchored partition")
    require(part["UNANCHORED_SINGLETON_WITHOUT_COMPLETE_EVENT_EXTERIOR_CLOSURE"] == {"component_count": 24, "current_unresolved_cell_count": 24}, "singleton partition")
    require(len(components) == 26, "component count")
    for row in components:
        require(row["whole_component_terminal_class"] is None, "no whole component terminal")
        require(row["whole_component_connected_to_known_credit"] == row["D02_gate_credit"] == 0, "component credit")
        require(row["singleton_isolation_promoted"] is False and row["coordinate_or_key_coincidence_used"] is False, "component shortcut")
        require(row["common_refinement_status"] == "NOT_MATERIALIZED_FOR_WHOLE_COMPONENT", "common refinement")
    for row in glues:
        require(row["coordinate_or_key_coincidence_used"] is False, "glue shortcut")
        if row["glue_kind"] in {"SOURCE_GRAZING_FACE", "SOURCE_GRAZING_SEAM_CORNER"}:
            require(row["terminal_credit"] == 0, "geometric grazing is zero-credit")


def verify() -> dict[str, Any]:
    before = {"head_file_sha256": file_sha(C53_HEAD), "head_size": C53_HEAD.stat().st_size}
    result = strict_json(RESULT_PATH)
    body = dict(result)
    claimed = body.pop("object_sha256", None)
    require(claimed == digest(body), "C55-B result object")
    require(result["C53_effective_authority"] == {
        "head_path": str(C53_HEAD.relative_to(ROOT)),
        "head_file_sha256": EXPECTED["HEAD_FILE"],
        "head_object_sha256": EXPECTED["HEAD_OBJECT"],
        "effective_checkpoint_object_sha256": EXPECTED["CHECKPOINT"],
        "authority_role": "GLOBAL_COMPOSITE",
        "current_four_class_census": {"CONNECTED_TO_KNOWN": 0, "EARLIEST_PREFIX_EXCLUDED": 75388, "SOURCE_GRAZING_OR_CEMETERY": 0, "TYPED_EVENT_GRAPH": 296, "UNRESOLVED_R1648_CONTINUATION": 1148, "total": 76832},
    }, "C53 authority binding")
    require(file_sha(C55P0) == EXPECTED["CONTRACT_FILE"], "input contract")

    cells_out = read_rows(OUT / result["ledgers"]["cell_component_crosswalk"]["filename"], result["ledgers"]["cell_component_crosswalk"], CELL_KEYS)
    components_out = read_rows(OUT / result["ledgers"]["ordinary_components"]["filename"], result["ledgers"]["ordinary_components"], COMPONENT_KEYS)
    glues_out = read_rows(OUT / result["ledgers"]["component_edges_and_glue"]["filename"], result["ledgers"]["component_edges_and_glue"])
    for row in glues_out:
        allowed = GLUE_COMMON | ({"typed_event_binding_row_sha256"} if row["glue_kind"] == "INHERITED_FIRST_EVENT_FACE" else set())
        require(set(row) == allowed and row["schema"] == GLUE_SCHEMA, "glue closed schema")
    validate_fail_closed_model(result, components_out, glues_out)

    c32 = validate_result(C32, EXPECTED["C32"], "C32")
    c33 = validate_result(C33, EXPECTED["C33"], "C33")
    c34 = validate_result(C34, EXPECTED["C34"], "C34")
    c37 = validate_result(C37, EXPECTED["C37"], "C37")
    c42 = validate_result(C42, EXPECTED["C42"], "C42")
    c53 = strict_json(C53_AUDIT)
    validate_object(c53, EXPECTED["C53_AUDIT"], "C53 audit")
    head = strict_json(C53_HEAD)
    require(file_sha(C53_HEAD) == EXPECTED["HEAD_FILE"] and head["authority_seal_object_sha256"] == EXPECTED["HEAD_OBJECT"] and head["post_seal_effective_checkpoint_object_sha256"] == EXPECTED["CHECKPOINT"], "installed C53 head")

    c32_cells = {row["cell_id"]: row for row in upstream_rows(C32, c32["ledgers"]["cells"])}
    cross = {row["cell_id"]: row for row in upstream_rows(C33, c33["row_level_crosswalk"])}
    adjacency = upstream_rows(C32, c32["ledgers"]["intra_chart_adjacency"])
    seams = upstream_rows(C32, c32["ledgers"]["source_chart_seams"])
    grazing = upstream_rows(C32, c32["ledgers"]["grazing"])
    corners = upstream_rows(C32, c32["ledgers"]["corners"])
    event_faces = upstream_rows(C32, c32["ledgers"]["inherited_event_faces"])
    event_bindings = upstream_rows(C34, c34["ledgers"]["typed_first_event_bindings"])
    frozen_components = upstream_rows(C34, c34["ledgers"]["ordinary_components"])
    pairs = upstream_rows(C37, c37["ledgers"]["ordinary_cell_reflection_pairs"])
    parents = upstream_rows(C42, c42["ledgers"]["parent_conservation"])
    projections = c53["post_seal_promotion_derivation"]["parent_projections"]
    require(len(c32_cells) == len(cross) == 76832, "full universe")
    live = {cell_id for cell_id, row in cross.items() if row["formal_source_W_disposition"] == "RESOLVED_NONEXCLUDED"}
    event_ids = {row["cell_id"] for row in event_bindings}
    ordinary = live - event_ids
    require(len(ordinary) == 1724, "ordinary universe")

    expected_current: dict[str, str] = {}
    expected_pair: dict[str, tuple[int, str, str, str]] = {}
    for pair, parent, projection in zip(pairs, parents, projections, strict=True):
        require(pair["pair_index"] == parent["pair_index"] == projection["pair_index"], "pair order")
        status = "EARLIEST_PREFIX_EXCLUDED" if projection["after_whole_representative"] else "UNRESOLVED_R1648_CONTINUATION"
        for side, other in (("representative", "reflected"), ("reflected", "representative")):
            cell_id = pair[side + "_cell_id"]
            expected_current[cell_id] = status
            expected_pair[cell_id] = (pair["pair_index"], pair[other + "_cell_id"], pair["row_sha256"], parent["row_sha256"])
    require(set(expected_current) == ordinary and Counter(expected_current.values()) == Counter({"EARLIEST_PREFIX_EXCLUDED": 576, "UNRESOLVED_R1648_CONTINUATION": 1148}), "effective ordinary census")

    cell_map = {row["cell_id"]: row for row in cells_out}
    require(len(cell_map) == 1724 and set(cell_map) == ordinary, "C55-B cell coverage")
    component_by_cell: dict[str, int] = {}
    for row in cells_out:
        source = c32_cells[row["cell_id"]]
        require(row["schema"] == CELL_SCHEMA and row["C32_cell_row_sha256"] == source["row_sha256"] and row["C33_crosswalk_row_sha256"] == cross[row["cell_id"]]["row_sha256"], "cell provenance")
        for field in ("origin_key", "compact_chart", "gate3_chart", "physical_slice", "physical_t_interval", "physical_p_interval", "gate3_product_box"):
            require(row[field] == source[field], f"cell geometry:{field}")
        pair_index, partner, pair_hash, parent_hash = expected_pair[row["cell_id"]]
        require((row["pair_index"], row["reflection_partner_cell_id"], row["C37_pair_row_sha256"], row["C42_parent_row_sha256"]) == (pair_index, partner, pair_hash, parent_hash), "cell pair provenance")
        require(row["current_effective_disposition"] == expected_current[row["cell_id"]], "cell disposition")
        require(row["whole_cell_connected_to_known_credit"] == row["D02_gate_credit"] == 0 and row["coordinate_or_key_coincidence_used"] is False, "cell credit lock")
        component_by_cell[row["cell_id"]] = row["component_index"]

    # Rebuild connected components from the emitted explicit face/seam rows.
    graph: dict[str, set[str]] = defaultdict(set)
    glue_by_hash = {row["row_sha256"]: row for row in glues_out}
    require(len(glue_by_hash) == len(glues_out) == 5358, "glue uniqueness")
    glue_counts = Counter((row["glue_kind"], row["scope"]) for row in glues_out)
    require(glue_counts[("INTRA_CHART_FACE", "ORDINARY_INTERNAL")] == 3248, "ordinary internal faces")
    require(glue_counts[("SOURCE_CHART_TRANSITION", "ORDINARY_INTERNAL")] == 28, "ordinary internal seams")
    require(glue_counts[("INTRA_CHART_FACE", "ORDINARY_TO_TYPED_EVENT_BOUNDARY")] == 394, "event boundary faces")
    require(glue_counts[("SOURCE_CHART_TRANSITION", "ORDINARY_TO_TYPED_EVENT_BOUNDARY")] == 10, "event boundary seams")
    require(glue_counts[("INTRA_CHART_FACE", "ORDINARY_TO_FORMAL_EXCLUSION_BOUNDARY")] == 310, "excluded boundary faces")
    require(glue_counts[("SOURCE_GRAZING_FACE", "GLOBAL_GRAZING_INVENTORY")] == 1024, "grazing inventory")
    require(glue_counts[("SOURCE_GRAZING_SEAM_CORNER", "GLOBAL_CORNER_INVENTORY")] == 8, "corner inventory")
    require(glue_counts[("INHERITED_FIRST_EVENT_FACE", "LIVE_TYPED_EVENT")] == 296 and glue_counts[("INHERITED_FIRST_EVENT_FACE", "EXCLUDED_EVENT_CANDIDATE")] == 40, "event face inventory")

    upstream_hashes = {
        "INTRA_CHART_FACE": {row["row_sha256"] for row in adjacency},
        "SOURCE_CHART_TRANSITION": {row["row_sha256"] for row in seams},
        "SOURCE_GRAZING_FACE": {row["row_sha256"] for row in grazing},
        "SOURCE_GRAZING_SEAM_CORNER": {row["row_sha256"] for row in corners},
        "INHERITED_FIRST_EVENT_FACE": {row["row_sha256"] for row in event_faces},
    }
    component_glue_refs: dict[int, list[str]] = defaultdict(list)
    for row in glues_out:
        require(row["upstream_row_sha256"] in upstream_hashes[row["glue_kind"]], "glue upstream row")
        expected_indices = sorted({component_by_cell[cell_id] for cell_id in (row["left_cell_id"], row["right_cell_id"]) if cell_id in ordinary})
        require(row["ordinary_component_indices"] == expected_indices, "glue component incidence")
        for index in expected_indices:
            component_glue_refs[index].append(row["row_sha256"])
        if row["scope"] == "ORDINARY_INTERNAL":
            first, second = row["left_cell_id"], row["right_cell_id"]
            require(first in ordinary and second in ordinary, "internal endpoints")
            graph[first].add(second); graph[second].add(first)

    require(len(components_out) == len(frozen_components) == 26, "components")
    anchored = 0
    all_members: set[str] = set()
    for index, (row, frozen) in enumerate(zip(components_out, frozen_components, strict=True)):
        require(set(row) == COMPONENT_KEYS and row["schema"] == COMPONENT_SCHEMA and row["component_index"] == index, "component closed row")
        members = row["member_cell_ids"]
        require(members == sorted(members) and not (all_members & set(members)), "component member partition")
        all_members.update(members)
        require(row["component_id"] == frozen["component_id"] and row["C34_component_row_sha256"] == frozen["row_sha256"], "C34 component pin")
        require(row["cell_count"] == len(members) == frozen["cell_count"] and row["member_cell_ids_sha256"] == digest(members) == frozen["cell_ids_sha256"], "component membership")
        require(all(component_by_cell[cell_id] == index for cell_id in members), "cell/component crosswalk")
        require(row["member_cell_row_sha256s"] == [cell_map[cell_id]["row_sha256"] for cell_id in members], "component cell row refs")
        require(row["edge_and_glue_row_sha256s"] == sorted(component_glue_refs[index]), "component glue refs")
        reached = {members[0]}; queue = deque([members[0]])
        while queue:
            for neighbour in graph[queue.popleft()]:
                if neighbour in set(members) and neighbour not in reached:
                    reached.add(neighbour); queue.append(neighbour)
        require(reached == set(members), "component internal connectivity")
        unresolved = [cell_id for cell_id in members if expected_current[cell_id] == "UNRESOLVED_R1648_CONTINUATION"]
        excluded = [cell_id for cell_id in members if expected_current[cell_id] == "EARLIEST_PREFIX_EXCLUDED"]
        require(row["current_unresolved_cell_count"] == len(unresolved) and row["current_unresolved_cell_ids_sha256"] == digest(sorted(unresolved)), "component unresolved projection")
        require(row["current_excluded_cell_count"] == len(excluded) and row["current_excluded_cell_ids_sha256"] == digest(sorted(excluded)), "component excluded projection")
        if row["known_sheet_anchor"] is not None:
            anchored += 1
            require(index in (0, 1) and row["known_sheet_anchor"]["whole_component_connected_credit"] == 0 and row["anchor_is_strict_subset_not_whole_component"] is True, "strict anchor")
        else:
            require(index >= 2 and len(members) == 1, "unanchored singleton")
        expected_counts = (288, 562) if index in (0, 1) else (0, 1)
        require((len(excluded), len(unresolved)) == expected_counts, "per-component current partition")
    require(all_members == ordinary and anchored == 2, "component/anchor coverage")

    # Coherent fail-closed attacks against the semantic validator.
    attacks: list[dict[str, Any]] = []
    attack_specs = [
        ("global_closure_true", lambda r, c, g: r.__setitem__("global_closure_proved", True)),
        ("unresolved_zero_true", lambda r, c, g: r.__setitem__("unresolved_zero", True)),
        ("strict_decider_eligible_true", lambda r, c, g: r.__setitem__("strict_decider_eligible", True)),
        ("formal_credit_one", lambda r, c, g: r["credit_locks"].__setitem__("formal_credit", 1)),
        ("anchor_credit_one", lambda r, c, g: r["known_sheet_anchor_census"].__setitem__("anchor_credit", 1)),
        ("whole_component_proof_one", lambda r, c, g: r["known_sheet_anchor_census"].__setitem__("components_with_whole_component_connected_proof", 1)),
        ("unresolved_total_1147", lambda r, c, g: r["exact_unresolved_partition"].__setitem__("total_current_unresolved_cell_count", 1147)),
        ("anchored_unresolved_1123", lambda r, c, g: r["exact_unresolved_partition"]["ANCHORED_COMPONENT_WITHOUT_WHOLE_COMMON_REFINEMENT"].__setitem__("current_unresolved_cell_count", 1123)),
        ("component_terminal_fabricated", lambda r, c, g: c[0].__setitem__("whole_component_terminal_class", "CONNECTED_TO_KNOWN")),
        ("component_credit_fabricated", lambda r, c, g: c[0].__setitem__("whole_component_connected_to_known_credit", 1)),
        ("component_common_refinement_fabricated", lambda r, c, g: c[0].__setitem__("common_refinement_status", "COMPLETE")),
        ("singleton_isolation_promoted", lambda r, c, g: c[2].__setitem__("singleton_isolation_promoted", True)),
        ("component_key_coincidence", lambda r, c, g: c[0].__setitem__("coordinate_or_key_coincidence_used", True)),
        ("grazing_credit_one", lambda r, c, g: next(x for x in g if x["glue_kind"] == "SOURCE_GRAZING_FACE").__setitem__("terminal_credit", 1)),
        ("corner_credit_one", lambda r, c, g: next(x for x in g if x["glue_kind"] == "SOURCE_GRAZING_SEAM_CORNER").__setitem__("terminal_credit", 1)),
        ("glue_coordinate_shortcut", lambda r, c, g: g[0].__setitem__("coordinate_or_key_coincidence_used", True)),
    ]
    for name, mutate in attack_specs:
        rr, cc, gg = copy.deepcopy(result), copy.deepcopy(components_out), copy.deepcopy(glues_out)
        mutate(rr, cc, gg)
        rejected = False
        try:
            validate_fail_closed_model(rr, cc, gg)
        except FailClosed:
            rejected = True
        require(rejected, f"attack accepted:{name}")
        attacks.append({"attack": name, "fail_closed": True})

    after = {"head_file_sha256": file_sha(C53_HEAD), "head_size": C53_HEAD.stat().st_size}
    require(before == after, "C53 head stable")
    verification: dict[str, Any] = {
        "schema": VERIFY_SCHEMA,
        "status": "PASS_INDEPENDENT_C55B_RECONSTRUCTION__16_OF_16_ATTACKS_FAIL_CLOSED__GLOBAL_CLOSURE_FALSE",
        "result_path": str(RESULT_PATH.relative_to(ROOT)),
        "result_file_sha256": file_sha(RESULT_PATH),
        "result_object_sha256": result["object_sha256"],
        "producer_source_sha256": file_sha(PRODUCER_PATH),
        "verifier_source_sha256": file_sha(Path(__file__).resolve()),
        "reconstruction": {
            "source_W_rows": 76832, "ordinary_cell_rows": len(cells_out),
            "component_rows": len(components_out), "edge_and_glue_rows": len(glues_out),
            "ordinary_components": 26, "reflection_pairs": 862,
            "strict_open_known_sheet_collars": 2, "whole_component_known_sheet_proofs": 0,
            "current_excluded_ordinary_cells": 576, "current_unresolved_ordinary_cells": 1148,
            "global_closure_proved": False, "unresolved_zero": False,
        },
        "attacks": attacks,
        "attack_count": len(attacks),
        "all_attacks_fail_closed": True,
        "independence_boundary": {
            "producer_imported_or_executed": False,
            "producer_consumed_as_source_bytes_only": True,
            "upstream_producers_imported_or_executed": False,
            "all_upstream_results_and_ledgers_consumed_as_inert_bytes": True,
            "runtime_writes_performed": False,
        },
        "C53_head_pre_post_snapshot_equal": True,
        "C53_head_snapshot": after,
        "formal_credit": 0,
        "D02_gate_credit": 0,
    }
    verification["object_sha256"] = digest(verification)
    VERIFY_PATH.write_bytes(canonical(verification) + b"\n")
    self_test = {
        "schema": VERIFY_SCHEMA + ".self-test",
        "status": "PASS_16_OF_16_COHERENT_ATTACKS_FAIL_CLOSED",
        "attacks": attacks,
        "attack_count": len(attacks),
        "all_attacks_fail_closed": True,
        "verification_object_sha256": verification["object_sha256"],
    }
    self_test["object_sha256"] = digest(self_test)
    SELF_TEST_PATH.write_bytes(canonical(self_test) + b"\n")
    return verification


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    require(args.verify, "use --verify")
    result = verify()
    print(json.dumps({"status": result["status"], "object_sha256": result["object_sha256"], "attack_count": result["attack_count"]}, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except FailClosed as exc:
        print(json.dumps({"status": "FAIL_CLOSED", "reason": str(exc)}, sort_keys=True, separators=(",", ":")))
        raise SystemExit(1)
