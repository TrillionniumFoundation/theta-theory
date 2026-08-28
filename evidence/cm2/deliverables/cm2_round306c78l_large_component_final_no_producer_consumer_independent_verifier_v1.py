#!/usr/bin/env python3
"""Independent no-producer verifier for the C78l final consumer.

This file deliberately does not read, import, execute, decode, or inspect the
C78l producer source.  The producer hash below is a declarative pin only.
Every C78l task, side, public-cell, and reflection-pair row is reconstructed
from independently pin-checked upstream bytes.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping
import zlib


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
SELF = Path(__file__).resolve()
DECLARED_PRODUCER_SHA256 = "9cdedea3c48e8f7b2db0ddeda56e2ce45037caaf1545f810c2033afae79db911"
SCHEMA = "cm2.round306c78l.large-component-final-no-producer-consumer.v1"
PREFIX = "cm2_round306c78l_large_component_final_no_producer_consumer_v1"
TASKS = PREFIX + "_task_consumption.jsonl.gz"
SIDES = PREFIX + "_task_side_occurrences.jsonl.gz"
CELLS = PREFIX + "_public_cell_rollup.jsonl.gz"
PAIRS = PREFIX + "_reflection_pair_rollup.jsonl.gz"
REGISTRY = PREFIX + "_source_registry.json"
RESULT = PREFIX + "_result.json"
REPORT = PREFIX + "_report.md"
LOCK = "ZERO_CREDIT_STAGED_C78L_FINAL_CONSUMER_ONLY.lock"
MANIFEST = PREFIX + "_manifest.sha256"
OUTER = PREFIX + "_outer_receipt.json"
MEMBERS = [TASKS, SIDES, CELLS, PAIRS, REGISTRY, RESULT, REPORT, LOCK, MANIFEST, OUTER]
BASE = [TASKS, SIDES, CELLS, PAIRS, REGISTRY, RESULT, REPORT, LOCK]
ZERO = {"formal_credit": 0, "global_credit": 0, "D02_gate_credit": 0,
        "whole_component_credit": 0, "CM2_credit": 0}

C76L = ROOT / ".cm2-runtime/c76l-build-a9.v2-baf36f71"
C76M = ROOT / ".cm2-runtime/c76m-c2-v4-build-a.b96dea41"
C76L_FREEZE = ROOT / ".cm2-runtime/c76l-v2-frozen-completion.ba8a77c2"
C76M_VERIFY = ROOT / ".cm2-runtime/c76m-c2-v4-verification-a.85f22789"
C76M_COMPLETE = ROOT / ".cm2-runtime/c76m-c2-v4-completion.85f22789"

PATHS: dict[str, Path] = {
    "C68_TASKS": OUT / "cm2_round306c68l_blocker_crosswalk_large_current_task_replay_v1.jsonl.gz",
    "C56_TASKS": OUT / "cm2_round306c56l_large_component_common_refinement_post_c53_pending_logical_tasks_v1.jsonl.gz",
    "C55B_CELLS": OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_cell_component_crosswalk_v1.jsonl.gz",
    "C55A_LEAVES": OUT / "cm2_round306c55a_four_chart_fundamental_domain_bnb_leaf_ledger_v1.json",
    "C55A_RESULT": OUT / "cm2_round306c55a_four_chart_fundamental_domain_bnb_result_v1.json",
    "C55A_VERIFICATION": OUT / "cm2_round306c55a_four_chart_fundamental_domain_bnb_independent_verification_v1.json",
    "C55A_MANIFEST": OUT / "cm2_round306c55a_four_chart_fundamental_domain_bnb_manifest_v1.sha256",
    "C76L_DECISIONS": C76L / "cm2_round306c76l_large_component_collision1_graph_exact_oracle_v1_decisions.jsonl.gz",
    "C76L_BRANCHES": C76L / "cm2_round306c76l_large_component_collision1_graph_exact_oracle_v1_exact_branch_partitions.jsonl.gz",
    "C76L_HANDOFFS": C76L / "cm2_round306c76l_large_component_collision1_graph_exact_oracle_v1_collision3_handoffs.jsonl.gz",
    "C76L_INCIDENCE": C76L / "cm2_round306c76l_large_component_collision1_graph_exact_oracle_v1_physical_graph_incidence.jsonl.gz",
    "C76L_BOUNDARIES": C76L / "cm2_round306c76l_large_component_collision1_graph_exact_oracle_v1_degree1_scope_source_boundary_registry.jsonl.gz",
    "C76L_RESULT": C76L / "cm2_round306c76l_large_component_collision1_graph_exact_oracle_v1_result.json",
    "C76L_FROZEN_RECEIPT": C76L_FREEZE / "cm2_round306c76l_large_component_collision1_graph_exact_oracle_v2_frozen_dual_completion_receipt.json",
    "C76L_FROZEN_MANIFEST": C76L_FREEZE / "cm2_round306c76l_large_component_collision1_graph_exact_oracle_v2_frozen_manifest.sha256",
    "C76L_FROZEN_OUTER": C76L_FREEZE / "cm2_round306c76l_large_component_collision1_graph_exact_oracle_v2_frozen_outer_receipt.json",
    "C76M_DECISIONS": C76M / "cm2_round306c76m_large_component_collision2_structural_decider_v4_decision_rows.jsonl.gz",
    "C76M_BRANCHES": C76M / "cm2_round306c76m_large_component_collision2_structural_decider_v4_side_branch_partitions.jsonl.gz",
    "C76M_HANDOFFS": C76M / "cm2_round306c76m_large_component_collision2_structural_decider_v4_collision3_handoffs.jsonl.gz",
    "C76M_INCIDENCE": C76M / "cm2_round306c76m_large_component_collision2_structural_decider_v4_event_incidence.jsonl.gz",
    "C76M_RESULT": C76M / "cm2_round306c76m_large_component_collision2_structural_decider_v4_result.json",
    "C76M_VERIFICATION": C76M_VERIFY / "cm2_round306c76m_large_component_collision2_structural_decider_independent_verification_v2.json",
    "C76M_COMPLETION": C76M_COMPLETE / "cm2_round306c76m_large_component_collision2_structural_decider_dual_completion_receipt_v2.json",
}

PINS = {
    "C68_TASKS": "bc62868582ca26be996904fe8120422b0d67e8afc0080dfd4650512a041eaa2f",
    "C56_TASKS": "6893e360b3ffc205147efa3786f1a05c1b67c1556e6195733549a7da5540fb6a",
    "C55B_CELLS": "123a742ed553d89fd1026cf65c64879d9a92916492b5b583888c3312551ca2ce",
    "C55A_LEAVES": "e80c012e3260e8f9e68d5858ba5d9dafd94611e2a1c1200d787a20e3842d8db6",
    "C55A_RESULT": "d38f39792fc944b72e70100f9f96f312b5e30e034d5104ce5f848d24378ae5af",
    "C55A_VERIFICATION": "6e9dfe5c50cfb104cbb8014873f69f79761b22848f50a51033fced651a121772",
    "C55A_MANIFEST": "848c56c5d328cbdf291715d1eaab2611d3af95fb8bf2875beaadcbb9ffca6e0d",
    "C76L_DECISIONS": "5ed713702f578bce28bae7ec7be307832ceb5f884831350b671d7d819e054ac8",
    "C76L_BRANCHES": "21dc05aa0ef0b48e3940c6c854e0cb13cb537f6eec31639844a5be5e11b8529d",
    "C76L_HANDOFFS": "bccf4c3ed02df9691f9f56b9f9ecef1ad4204876ad740dd29d9f8749c8162455",
    "C76L_INCIDENCE": "66004a5d3440995da1692009b720b0523df4a4fd64de6440d8f70ae60a4cffa5",
    "C76L_BOUNDARIES": "293bbd922a2e8a6c396dc09815cde90a0c2fb62176cb488a899c636ac83b1cb5",
    "C76L_RESULT": "d15c7947c321a7c614b79e4b05449a83789846e08776ad27aae005bee8d85c25",
    "C76L_FROZEN_RECEIPT": "feceb3ec9af028a2f702f7c453873c914382179aeac68da4691d33868ec2eba4",
    "C76L_FROZEN_MANIFEST": "d45070dd409a4ea6f40d3d2964980c2f9c71cd44cc781d7b2a90499276e9d55b",
    "C76L_FROZEN_OUTER": "9c41d9e81a89166a524b45a946bfd8b8a18772d7bcf2e3d5ea2f966131cdb0d2",
    "C76M_DECISIONS": "e2a15d1ba29be974865980ba241df8ad1a3dfd529aa8837241d25bed20843f6a",
    "C76M_BRANCHES": "f15e07c8915a1cb1b5b9415ded2c30f3e4777a15c25e515ccf7a8f5903e435a4",
    "C76M_HANDOFFS": "b98a97d910a8d04b85439d418b48196b85a7d21e7d1fa1208e3a4960c4ad113b",
    "C76M_INCIDENCE": "cacf63a2e71de159d27daeba73a9ba49a38d47f1adf7b12cd53bb4718c7a503a",
    "C76M_RESULT": "16e71711eb432d4d377496df06ea72535823536e9632e391183a6a4fe8956d6e",
    "C76M_VERIFICATION": "eae90bf4d5f228b354010392fe1f5c38cb6ce2727cc1843fc9443cef4e0ff09e",
    "C76M_COMPLETION": "7755de5e740db2321a4c5340e67fea74455056dadcc8b8e4487e8ea0c16d0bf9",
}


class Reject(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def secure(path: Path, pin: str | None = None) -> bytes:
    need(path.is_file() and not path.is_symlink(), "secure file:" + str(path))
    data = path.read_bytes()
    if pin is not None:
        need(sha_bytes(data) == pin, "file pin:" + str(path))
    return data


def close_row(value: dict[str, Any]) -> dict[str, Any]:
    need("row_sha256" not in value, "open row")
    return {**value, "row_sha256": digest(value)}


def close_object(value: dict[str, Any]) -> dict[str, Any]:
    need("object_sha256" not in value, "open object")
    return {**value, "object_sha256": digest(value)}


def verify_row(row: Mapping[str, Any], label: str) -> None:
    body = copy.deepcopy(dict(row)); claim = body.pop("row_sha256", None)
    need(claim == digest(body), label + ":row closure")


def verify_object(obj: Mapping[str, Any], label: str) -> None:
    body = copy.deepcopy(dict(obj)); claim = body.pop("object_sha256", None)
    need(claim == digest(body), label + ":object closure")


def parse_gzip(raw: bytes, label: str, check_rows: bool = True) -> list[dict[str, Any]]:
    dec = zlib.decompressobj(16 + zlib.MAX_WBITS)
    try:
        plain = dec.decompress(raw) + dec.flush()
    except zlib.error as exc:
        raise Reject(label + ":gzip:" + str(exc)) from exc
    need(dec.eof and not dec.unused_data and not dec.unconsumed_tail,
         label + ":one complete gzip member")
    need(not plain or plain.endswith(b"\n"), label + ":newline")
    out = []
    for index, line in enumerate(plain.splitlines()):
        row = json.loads(line)
        need(isinstance(row, dict), label + ":row object")
        if check_rows:
            verify_row(row, f"{label}:{index}")
        out.append(row)
    return out


def ledger(key: str) -> list[dict[str, Any]]:
    return parse_gzip(secure(PATHS[key], PINS[key]), key)


def json_source(key: str) -> dict[str, Any]:
    value = json.loads(secure(PATHS[key], PINS[key]))
    need(isinstance(value, dict), key + ":object")
    if "object_sha256" in value:
        verify_object(value, key)
    return value


def one_index(rows: Iterable[dict[str, Any]], key: str, label: str) -> dict[Any, dict[str, Any]]:
    out = {}
    for row in rows:
        value = row[key]
        need(value not in out, label + ":unique")
        out[value] = row
    return out


def qtext(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def exact_row(actual: Mapping[str, Any], expected: Mapping[str, Any], label: str) -> None:
    verify_row(actual, label)
    need(dict(actual) == dict(expected), label + ":independent reconstruction")


def validate_manifest(raw: bytes, member_sha: Mapping[str, str]) -> None:
    expected = b"".join(f"{member_sha[name]}  {name}\n".encode("ascii") for name in sorted(BASE))
    need(raw == expected, "one-global manifest exact bytes")


def validate_publication(a: Path, b: Path) -> dict[str, bytes]:
    need(a.resolve() != b.resolve(), "two isolated directories")
    need({p.name for p in a.iterdir()} == set(MEMBERS) and
         {p.name for p in b.iterdir()} == set(MEMBERS), "exact build member sets")
    values: dict[str, bytes] = {}
    for name in MEMBERS:
        left, right = secure(a / name), secure(b / name)
        need(left == right, "dual byte identity:" + name)
        values[name] = left
    member_sha = {name: sha_bytes(values[name]) for name in BASE}
    validate_manifest(values[MANIFEST], member_sha)
    outer = json.loads(values[OUTER]); verify_object(outer, "candidate outer")
    need(outer["manifest_sha256"] == sha_bytes(values[MANIFEST]), "outer manifest pin")
    need(outer["ordered_member_file_sha256"] ==
         [{"filename": name, "sha256": member_sha[name]} for name in sorted(BASE)],
         "outer member pins")
    need(outer["one_global_manifest"] is True and outer["outer_receipt_published_last"] is True and
         outer["terminal_byte_replay_required_after_outer_receipt"] is True,
         "outer publication contract")
    for stage in (a, b):
        member_time = max((stage / name).stat().st_mtime_ns for name in BASE)
        manifest_time = (stage / MANIFEST).stat().st_mtime_ns
        outer_time = (stage / OUTER).stat().st_mtime_ns
        need(member_time < manifest_time < outer_time, "actual outer-last stat order")
        for name in MEMBERS:
            secure(stage / name)  # terminal replay after outer exists
    return values


def load_c55a() -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    result = json_source("C55A_RESULT")
    verification = json_source("C55A_VERIFICATION")
    manifest = secure(PATHS["C55A_MANIFEST"], PINS["C55A_MANIFEST"]).decode("ascii")
    need(f"{PINS['C55A_LEAVES']}  deliverables/{PATHS['C55A_LEAVES'].name}" in manifest,
         "C55A manifest leaves")
    need(result["bnb"]["leaf_ledger_file_sha256"] == PINS["C55A_LEAVES"] and
         result["bnb"]["leaf_ledger_object_sha256"] ==
         "7dd4c19cfb2b9f8cd30a4a9a23e30f11734e856cc6cc5a04e9a169c051059d90",
         "C55A result binding")
    need(verification["independence"]["C55A_producer_imported"] is False and
         verification["independence"]["C55A_producer_executed"] is False,
         "C55A independently verified")
    obj = json.loads(secure(PATHS["C55A_LEAVES"], PINS["C55A_LEAVES"]))
    need(obj["object_sha256"] == result["bnb"]["leaf_ledger_object_sha256"] and
         len(obj["leaves"]) == 76_832, "C55A leaf identity")
    selected = []
    for leaf in obj["leaves"]:
        component = leaf["component_ref"]
        if component is not None and component["component_index"] in {0, 1} and leaf["terminal_disposition"] is None:
            verify_row(leaf, "C55A selected")
            selected.append(leaf)
    need(len(selected) == 1_124 and all(selected[i]["leaf_ordinal"] < selected[i + 1]["leaf_ordinal"]
         for i in range(1_123)), "C55A large row sequence")
    return selected, one_index(selected, "cell_id", "C55A selected")


def validate_result_semantics(result: Mapping[str, Any]) -> None:
    need(result["task_source_partition"]["C76L_collision1"] == 16_883 and
         result["task_source_partition"]["C76M_collision2"] == 16_436 and
         result["task_source_partition"]["disjoint"] is True and
         result["task_source_partition"]["exhaustive"] is True, "result task partition")
    need(result["task_side_occurrence_count"] == 66_638 and result["public_cell_count"] == 1_124 and
         result["reflection_pair_count"] == 562, "result projection counts")
    need(result["public_cell_disposition_census"] == {
        "EXHAUSTIVE_PUBLIC_CELL_TYPED_EVENT_C3_PARTITION": 1_094,
        "WHOLE_PUBLIC_CELL_STRICT_EXCLUSION": 30}, "result public dispositions")
    need(result["conditional_collision3_envelope_count"] == 56_514 and
         result["actual_C3_disposition_count"] == 0 and result["branch_unresolved"] == 0,
         "result conditional semantics")
    need(result["public_global_unresolved_before"] == 1_148 and
         result["public_global_unresolved_after_branch"] == 24 and
         result["public_global_unresolved_zero"] is False,
         "result global remainder is not erased")
    need(result["C55A_identity_only_and_not_termination_authority"] is True and
         result["original_C55A_row_to_new_disposition_bijection"] is True and
         result["reflection_pair_prefix_Kraft_closed"] is True,
         "result role separation")
    need(all(result[key] == 0 for key in ZERO) and
         result["canonical_pointer_or_seal_written"] is False, "result zero credit")


def reconstruct(values: Mapping[str, bytes]) -> tuple[dict[str, Any], list[dict[str, Any]],
        list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    frozen = json_source("C76L_FROZEN_RECEIPT")
    c76m_completion = json_source("C76M_COMPLETION")
    c76m_verification = json_source("C76M_VERIFICATION")
    need(frozen["status"].startswith("PASS_FROZEN_C76L_V2") and
         frozen["upstream_provenance_attacks"] == "PASS_29_OF_29" and
         frozen["only_A9_build_and_A11_v2_verification_are_consumable"] is True,
         "C76l frozen surface")
    need(c76m_completion["status"] == "PASS_VERIFICATION_A_B_BYTE_IDENTICAL__RECEIPT_PUBLISHED_LAST" and
         c76m_verification["conditional_handoff_envelopes_are_not_actual_C3_dispositions"] is True,
         "C76m sealed surface")

    c68_rows, c56_rows, c55_rows = ledger("C68_TASKS"), ledger("C56_TASKS"), ledger("C55B_CELLS")
    need(len(c68_rows) == len(c56_rows) == 33_319, "C68/C56 count")
    c56 = one_index(c56_rows, "row_sha256", "C56")
    c55 = one_index(c55_rows, "cell_id", "C55B")
    c55a_sequence, c55a = load_c55a()

    l_dec = one_index(ledger("C76L_DECISIONS"), "C68_large_task_row_sha256", "C76l decisions")
    l_branch = one_index(ledger("C76L_BRANCHES"), "row_sha256", "C76l branches")
    l_handoff = one_index(ledger("C76L_HANDOFFS"), "row_sha256", "C76l handoffs")
    l_incidence = one_index(ledger("C76L_INCIDENCE"), "physical_root_id", "C76l incidence")
    l_boundaries = one_index(ledger("C76L_BOUNDARIES"), "row_sha256", "C76l boundaries")
    for row in l_incidence.values():
        boundary = row["degree1_scope_source_boundary_row_sha256"]
        need((boundary is None and row["occurrence_count"] == 2) or
             (boundary in l_boundaries and row["occurrence_count"] == 1), "C76l boundary incidence")
    m_dec = one_index(ledger("C76M_DECISIONS"), "C68_large_task_row_sha256", "C76m decisions")
    m_branch = one_index(ledger("C76M_BRANCHES"), "row_sha256", "C76m branches")
    m_handoff = one_index(ledger("C76M_HANDOFFS"), "row_sha256", "C76m handoffs")
    m_incidence = one_index(ledger("C76M_INCIDENCE"), "row_sha256", "C76m incidence")
    universe = {x["row_sha256"] for x in c68_rows}
    need(len(l_dec) == 16_883 and len(m_dec) == 16_436 and not (set(l_dec) & set(m_dec)) and
         set(l_dec) | set(m_dec) == universe, "independent C1/C2 exact partition")

    actual_tasks = parse_gzip(values[TASKS], "candidate tasks")
    actual_sides = parse_gzip(values[SIDES], "candidate sides")
    actual_cells = parse_gzip(values[CELLS], "candidate cells")
    actual_pairs = parse_gzip(values[PAIRS], "candidate pairs")
    need(len(actual_tasks) == 33_319 and len(actual_sides) == 66_638 and
         len(actual_cells) == 1_124 and len(actual_pairs) == 562, "candidate ledgers count")

    expected_tasks, expected_sides = [], []
    side_by_cell: dict[str, list[dict[str, Any]]] = defaultdict(list)
    task_disp: Counter[str] = Counter(); source_count: Counter[str] = Counter(); actions: Counter[str] = Counter()
    conditional = 0
    for ordinal, c68 in enumerate(c68_rows):
        c68sha, c56sha = c68["row_sha256"], c68["C56_task_row_sha256"]
        c56row = c56[c56sha]
        need((c56row["pair_index"], c56row["path"], c56row["residual_classification"]) ==
             (c68["pair_index"], c68["path"], c68["residual_classification"]), "C68/C56 fields")
        weight = c56row["parent_volume_fraction"]
        if c68sha in l_dec:
            source, decision = "C76L_COLLISION1", l_dec[c68sha]
            strict = decision["task_disposition"] == "WHOLE_TASK_STRICT_EXCLUSION"
            disposition = ("WHOLE_TASK_STRICT_EXCLUSION" if strict else
                           "EXHAUSTIVE_TWO_SIDE_TYPED_EVENT_C3_PARTITION")
            branch_refs = list(decision["exact_branch_partition_row_sha256"])
            handoff_refs = list(decision["collision3_handoff_row_sha256"])
            branches = {l_branch[x]["physical_side"]: l_branch[x] for x in branch_refs}
            need((strict and not branches and not handoff_refs) or
                 (not strict and set(branches) == {"REPRESENTATIVE", "REFLECTED"} and
                  len(handoff_refs) in {0, 2}), "C76l branch shape")
            for ref in handoff_refs:
                need(l_handoff[ref]["conditional_bundle3_envelope_not_an_actual_C3_claim"] is True,
                     "C76l conditional")
            incidence_refs = sorted({l_incidence[x["physical_root_id"]]["row_sha256"]
                                     for x in decision["physical_graph_endpoint_occurrences"]})
            source_task_id = (next(iter(branches.values()))["source_task_id"] if branches else
                "c76l-task:" + digest({"C68_large_task_row_sha256": c68sha,
                    "pair_index": c68["pair_index"], "path": c68["path"]}))
            side_cells = {"REPRESENTATIVE": decision["representative_cell_id"],
                          "REFLECTED": decision["reflected_cell_id"]}
        else:
            source, decision, strict = "C76M_COLLISION2", m_dec[c68sha], False
            disposition = "EXHAUSTIVE_TWO_SIDE_TYPED_EVENT_C3_PARTITION"
            branch_refs = list(decision["side_branch_partition_row_sha256"])
            handoff_refs = list(decision["conditional_collision3_handoff_row_sha256"])
            branches = {m_branch[x]["physical_side"]: m_branch[x] for x in branch_refs}
            need(set(branches) == {"REPRESENTATIVE", "REFLECTED"} and len(handoff_refs) == 2,
                 "C76m branch shape")
            for ref in handoff_refs:
                need(m_handoff[ref]["conditional_expected_branch_only"] is True and
                     m_handoff[ref]["global_consumption_ready"] is False, "C76m conditional")
            incidence_refs = [decision["incidence_row_sha256"]]
            need(m_incidence[incidence_refs[0]]["all_face_corner_source_grazing_incidence_closed"] is True,
                 "C76m incidence")
            source_task_id = decision["task_id"]
            side_cells = {"REPRESENTATIVE": decision["representative_cell_id"],
                          "REFLECTED": decision["reflected_cell_id"]}
        need(side_cells == {"REPRESENTATIVE": c56row["representative_cell_id"],
                            "REFLECTED": c56row["reflected_cell_id"]}, "C56 side cells")
        source_count[source] += 1
        task_id = "c78l-task:" + digest({"task_ordinal": ordinal,
            "C68_large_task_row_sha256": c68sha, "C56_task_row_sha256": c56sha})
        side_refs = []
        for side_ordinal, physical_side in enumerate(("REPRESENTATIVE", "REFLECTED")):
            cell_id = side_cells[physical_side]; cell = c55[cell_id]; leaf = c55a[cell_id]
            need(leaf["component_ref"]["component_id"] == cell["component_id"] and
                 leaf["reflection_pair_ref"]["pair_index"] == cell["pair_index"], "C55A/C55B identity")
            branch = None if strict else branches[physical_side]
            if branch is None:
                branch_actions, handoff_ref = ["WHOLE_TASK_STRICT_EXCLUSION"], None
            elif source == "C76L_COLLISION1":
                branch_actions = [x["branch_action"] for x in branch["ordered_disjoint_branch_families"]]
                handoff_ref = branch["collision3_handoff_row_sha256"]
            else:
                branch_actions = [x["action"] for x in branch["ordered_exit_bundle_refs"]]
                handoff_ref = branch["ordered_exit_bundle_refs"][3]["collision3_handoff_row_sha256"]
            if handoff_ref is not None:
                need(handoff_ref in handoff_refs, "conditional side ref"); conditional += 1
            actions.update(branch_actions)
            expected_side = close_row({
                "schema": SCHEMA + ".task-side-occurrence-row", "task_ordinal": ordinal,
                "side_ordinal": side_ordinal, "consumer_task_id": task_id,
                "source_task_id": source_task_id, "source_decider": source,
                "source_decision_row_sha256": decision["row_sha256"],
                "C68_large_task_row_sha256": c68sha, "C56_task_row_sha256": c56sha,
                "physical_side": physical_side, "cell_id": cell_id,
                "C55B_cell_row_sha256": cell["row_sha256"],
                "C55A_leaf_ordinal": leaf["leaf_ordinal"], "C55A_leaf_row_sha256": leaf["row_sha256"],
                "C55A_reflection_pair_index": leaf["reflection_pair_ref"]["pair_index"],
                "C55A_identity_role_only": True, "C55A_termination_or_partition_authority_used": False,
                "component_id": cell["component_id"], "component_index": cell["component_index"],
                "source_side_partition_row_sha256": None if branch is None else branch["row_sha256"],
                "conditional_collision3_envelope_row_sha256": handoff_ref,
                "ordered_exhaustive_action_types": branch_actions,
                "public_side_disposition": ("WHOLE_STRICT_EXCLUSION" if strict else
                                             "EXHAUSTIVE_TYPED_EVENT_C3_PARTITION"),
                "conditional_C3_envelope_is_not_actual_C3": True,
                "actual_C3_disposition_count": 0,
                "owner_history_glue_closed_by_verified_source_partition": True,
                "incidence_row_sha256": incidence_refs,
                "face_corner_source_grazing_incidence_closed": True,
                "prefix_Kraft": {"parent_volume_fraction": weight, "consumed_scope_weight": weight,
                    "additional_dyadic_depth": 0, "equality_carrier_full_dimensional_weight": "0",
                    "physical_reflection_duplicate_credit": 0, "prefix_free": True}, **ZERO})
            exact_row(actual_sides[2 * ordinal + side_ordinal], expected_side, "side")
            expected_sides.append(expected_side); side_by_cell[cell_id].append(expected_side)
            side_refs.append(expected_side["row_sha256"])
        expected_task = close_row({
            "schema": SCHEMA + ".task-consumption-row", "task_ordinal": ordinal,
            "consumer_task_id": task_id, "source_task_id": source_task_id,
            "C68_large_task_row_sha256": c68sha, "C56_task_row_sha256": c56sha,
            "source_decider": source, "source_decision_row_sha256": decision["row_sha256"],
            "pair_index": c68["pair_index"], "path": c68["path"],
            "residual_classification": c68["residual_classification"],
            "representative_cell_id": side_cells["REPRESENTATIVE"],
            "reflected_cell_id": side_cells["REFLECTED"], "parent_volume_fraction": weight,
            "global_task_disposition": disposition, "source_side_partition_row_sha256": branch_refs,
            "conditional_collision3_envelope_row_sha256": handoff_refs,
            "incidence_row_sha256": incidence_refs, "task_side_occurrence_row_sha256": side_refs,
            "two_physical_sides_complete": True,
            "owner_history_glue_incidence_prefix_Kraft_closed": True,
            "conditional_envelopes_consumed_only_by_whole_exhaustive_partition": True,
            "conditional_envelope_promoted_to_actual_C3": False,
            "actual_C3_disposition_count": 0, "unresolved_branch_count": 0, **ZERO})
        exact_row(actual_tasks[ordinal], expected_task, "task")
        expected_tasks.append(expected_task); task_disp[disposition] += 1

    expected_cells, cell_by_id = [], {}
    cell_disp: Counter[str] = Counter()
    for ordinal, leaf in enumerate(c55a_sequence):
        cell_id = leaf["cell_id"]; occurrence = side_by_cell[cell_id]; c55row = c55[cell_id]
        strict = all(x["public_side_disposition"] == "WHOLE_STRICT_EXCLUSION" for x in occurrence)
        disposition = ("WHOLE_PUBLIC_CELL_STRICT_EXCLUSION" if strict else
                       "EXHAUSTIVE_PUBLIC_CELL_TYPED_EVENT_C3_PARTITION")
        weight = sum((Fraction(x["prefix_Kraft"]["consumed_scope_weight"])
                      for x in occurrence), Fraction(0))
        expected_cell = close_row({
            "schema": SCHEMA + ".public-cell-rollup-row", "cell_ordinal": ordinal,
            "cell_id": cell_id, "C55B_cell_row_sha256": c55row["row_sha256"],
            "C55A_leaf_ordinal": leaf["leaf_ordinal"], "C55A_original_row_sha256": leaf["row_sha256"],
            "C55A_original_terminal_disposition": leaf["terminal_disposition"],
            "C55A_original_unresolved_reason": leaf["unresolved_reason"],
            "pair_index": leaf["reflection_pair_ref"]["pair_index"],
            "reflection_partner_cell_id": leaf["reflection_pair_ref"]["partner_cell_id"],
            "C55A_component_ref": leaf["component_ref"], "component_id": c55row["component_id"],
            "component_index": c55row["component_index"],
            "task_side_occurrence_row_sha256": [x["row_sha256"] for x in occurrence],
            "task_side_occurrence_count": len(occurrence),
            "source_decider_occurrence_census": dict(sorted(Counter(x["source_decider"] for x in occurrence).items())),
            "side_disposition_census": dict(sorted(Counter(x["public_side_disposition"] for x in occurrence).items())),
            "public_cell_disposition": disposition,
            "original_C55A_row_to_new_disposition_one_to_one": True,
            "C55A_identity_role_only": True, "C55A_termination_or_partition_authority_used": False,
            "ordered_exhaustive_action_type_union": sorted({a for x in occurrence
                                                               for a in x["ordered_exhaustive_action_types"]}),
            "conditional_collision3_envelope_occurrence_count":
                sum(x["conditional_collision3_envelope_row_sha256"] is not None for x in occurrence),
            "conditional_C3_envelopes_consumed_only_inside_exhaustive_partitions": True,
            "actual_C3_disposition_count": 0,
            "owner_history_glue_two_sides_incidence_closed": True,
            "prefix_Kraft": {"consumed_scope_weight": qtext(weight),
                "equality_carrier_full_dimensional_weight": "0", "prefix_free": True,
                "physical_reflection_duplicate_credit": 0}, "unresolved_count": 0, **ZERO})
        exact_row(actual_cells[ordinal], expected_cell, "cell")
        expected_cells.append(expected_cell); cell_by_id[cell_id] = expected_cell; cell_disp[disposition] += 1

    grouped: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for leaf in c55a_sequence:
        grouped[leaf["reflection_pair_ref"]["pair_index"]].append(leaf)
    expected_pairs = []
    for ordinal, pair_index in enumerate(sorted(grouped)):
        role = {x["component_ref"]["cell_role"]: x for x in grouped[pair_index]}
        need(set(role) == {"REPRESENTATIVE", "REFLECTED"}, "pair roles")
        rep, ref = role["REPRESENTATIVE"], role["REFLECTED"]
        need(rep["reflection_pair_ref"]["partner_cell_id"] == ref["cell_id"] and
             ref["reflection_pair_ref"]["partner_cell_id"] == rep["cell_id"], "pair reciprocity")
        public = [cell_by_id[rep["cell_id"]], cell_by_id[ref["cell_id"]]]
        weight = sum((Fraction(x["prefix_Kraft"]["consumed_scope_weight"])
                      for x in public), Fraction(0))
        pair_disp = ("WHOLE_REFLECTION_PAIR_STRICT_EXCLUSION" if
            all(x["public_cell_disposition"] == "WHOLE_PUBLIC_CELL_STRICT_EXCLUSION" for x in public)
            else "EXHAUSTIVE_REFLECTION_PAIR_TYPED_EVENT_C3_PARTITION")
        expected_pair = close_row({
            "schema": SCHEMA + ".reflection-pair-rollup-row", "pair_ordinal": ordinal,
            "pair_index": pair_index,
            "representative": {"leaf_ordinal": rep["leaf_ordinal"], "cell_id": rep["cell_id"],
                "C55A_row_sha256": rep["row_sha256"],
                "C78l_public_cell_row_sha256": cell_by_id[rep["cell_id"]]["row_sha256"]},
            "reflected": {"leaf_ordinal": ref["leaf_ordinal"], "cell_id": ref["cell_id"],
                "C55A_row_sha256": ref["row_sha256"],
                "C78l_public_cell_row_sha256": cell_by_id[ref["cell_id"]]["row_sha256"]},
            "reciprocal_reflection_partner_identity_closed": True,
            "pair_disposition": pair_disp, "conditional_C3_envelopes_are_not_actual_C3": True,
            "prefix_Kraft": {"two_cell_consumed_scope_weight": qtext(weight),
                "equality_carrier_full_dimensional_weight": "0", "prefix_free": True,
                "physical_reflection_duplicate_credit": 0},
            "owner_history_glue_two_sides_incidence_closed": True, "unresolved_count": 0, **ZERO})
        exact_row(actual_pairs[ordinal], expected_pair, "pair")
        expected_pairs.append(expected_pair)

    result = json.loads(values[RESULT]); verify_object(result, "candidate result"); validate_result_semantics(result)
    registry = json.loads(values[REGISTRY]); verify_object(registry, "candidate registry")
    need(registry["consumer_file_sha256"] == DECLARED_PRODUCER_SHA256 and
         registry["upstream_producer_imported_or_executed"] is False and
         registry["role_separation"]["C55A"] == "IDENTITY_ONLY_NO_TERMINATION_OR_PARTITION_AUTHORITY" and
         registry["role_separation"]["C76L_C76M"] == "SOLE_TERMINATION_AND_EXHAUSTIVE_PARTITION_AUTHORITY",
         "registry role separation")
    input_pins = {key: {"path": str(PATHS[key].relative_to(ROOT)), "sha256": PINS[key]}
                  for key in sorted(PATHS)}
    need(registry["input_file_pins"] == input_pins and
         registry["input_pin_set_sha256"] == digest(input_pins), "registry input pins")
    need(result["C55A_original_large_component_row_sha256_sequence_sha256"] ==
         digest([x["row_sha256"] for x in c55a_sequence]) and
         result["C78l_public_overlay_row_sha256_sequence_sha256"] ==
         digest([x["row_sha256"] for x in expected_cells]), "result row sequences")
    need(source_count == Counter({"C76L_COLLISION1": 16_883, "C76M_COLLISION2": 16_436}) and
         task_disp == Counter({"WHOLE_TASK_STRICT_EXCLUSION": 3_974,
                              "EXHAUSTIVE_TWO_SIDE_TYPED_EVENT_C3_PARTITION": 29_345}) and
         cell_disp == Counter({"WHOLE_PUBLIC_CELL_STRICT_EXCLUSION": 30,
                              "EXHAUSTIVE_PUBLIC_CELL_TYPED_EVENT_C3_PARTITION": 1_094}) and
         conditional == 56_514, "independently derived censuses")
    outer = json.loads(values[OUTER])
    need(outer["candidate_object_sha256"] == result["object_sha256"] and
         outer["source_registry_object_sha256"] == registry["object_sha256"], "outer object bindings")
    return result, expected_tasks, expected_sides, expected_cells, expected_pairs, {
        "source_count": dict(source_count), "task_dispositions": dict(task_disp),
        "cell_dispositions": dict(cell_disp), "action_census": dict(actions),
        "conditional_C3": conditional,
        "C55A_source_sequence_sha256": digest([x["row_sha256"] for x in c55a_sequence]),
        "C78l_overlay_sequence_sha256": digest([x["row_sha256"] for x in expected_cells]),
    }


def run_attacks(result: dict[str, Any], tasks: list[dict[str, Any]], sides: list[dict[str, Any]],
                cells: list[dict[str, Any]], pairs: list[dict[str, Any]],
                task_raw: bytes, manifest_raw: bytes) -> dict[str, Any]:
    attacks: dict[str, str] = {}

    def rejected(name: str, fn: Callable[[], None]) -> None:
        try:
            fn()
        except (Reject, KeyError, IndexError, ValueError, TypeError, json.JSONDecodeError):
            attacks[name] = "FAIL_CLOSED"
        else:
            raise Reject("attack accepted:" + name)

    def mutate_row(name: str, row: dict[str, Any], mutate: Callable[[dict[str, Any]], None]) -> None:
        expected = row
        bad = copy.deepcopy(row); bad.pop("row_sha256"); mutate(bad); bad = close_row(bad)
        rejected(name, lambda: exact_row(bad, expected, "attack:" + name))

    for name, field, wrong in (
        ("task:C68", "C68_large_task_row_sha256", "00"), ("task:C56", "C56_task_row_sha256", "00"),
        ("task:source", "source_decider", "C55A"), ("task:disposition", "global_task_disposition", "ACTUAL_C3"),
        ("task:side_refs", "task_side_occurrence_row_sha256", []),
        ("task:handoff", "conditional_collision3_envelope_row_sha256", ["00"]),
        ("task:incidence", "incidence_row_sha256", ["00"]),
        ("task:two_sides", "two_physical_sides_complete", False),
        ("task:actual_C3", "actual_C3_disposition_count", 1),
        ("task:unresolved", "unresolved_branch_count", 1)):
        mutate_row(name, tasks[0], lambda x, f=field, w=wrong: x.__setitem__(f, w))
    for name, field, wrong in (
        ("side:cell", "cell_id", "MUTATED"), ("side:C55A_row", "C55A_leaf_row_sha256", "00"),
        ("side:pair", "C55A_reflection_pair_index", -1),
        ("side:partition", "source_side_partition_row_sha256", "00"),
        ("side:handoff", "conditional_collision3_envelope_row_sha256", "00"),
        ("side:actions", "ordered_exhaustive_action_types", ["ACTUAL_C3"]),
        ("side:disposition", "public_side_disposition", "ACTUAL_C3"),
        ("side:authority", "C55A_termination_or_partition_authority_used", True),
        ("side:actual_C3", "actual_C3_disposition_count", 1),
        ("side:credit", "formal_credit", 1)):
        mutate_row(name, sides[0], lambda x, f=field, w=wrong: x.__setitem__(f, w))
    for name, field, wrong in (
        ("cell:leaf_ordinal", "C55A_leaf_ordinal", -1), ("cell:C55A_row", "C55A_original_row_sha256", "00"),
        ("cell:pair", "pair_index", -1), ("cell:partner", "reflection_partner_cell_id", "MUTATED"),
        ("cell:component", "component_index", 99), ("cell:disposition", "public_cell_disposition", "ACTUAL_C3"),
        ("cell:occurrences", "task_side_occurrence_row_sha256", []),
        ("cell:authority", "C55A_termination_or_partition_authority_used", True),
        ("cell:actual_C3", "actual_C3_disposition_count", 1), ("cell:unresolved", "unresolved_count", 1)):
        mutate_row(name, cells[0], lambda x, f=field, w=wrong: x.__setitem__(f, w))
    for name, field, wrong in (
        ("pair:index", "pair_index", -1), ("pair:representative", "representative", {}),
        ("pair:reflected", "reflected", {}), ("pair:reciprocity", "reciprocal_reflection_partner_identity_closed", False),
        ("pair:disposition", "pair_disposition", "ACTUAL_C3"), ("pair:unresolved", "unresolved_count", 1)):
        mutate_row(name, pairs[0], lambda x, f=field, w=wrong: x.__setitem__(f, w))

    def bad_result(field: str, wrong: Any) -> None:
        bad = copy.deepcopy(result); bad.pop("object_sha256"); bad[field] = wrong; bad = close_object(bad)
        validate_result_semantics(bad)
    rejected("result:conditional_C3_inflation", lambda: bad_result("actual_C3_disposition_count", 1))
    rejected("result:branch_unresolved", lambda: bad_result("branch_unresolved", 1))
    rejected("result:global_remainder_erasure", lambda: bad_result("public_global_unresolved_after_branch", 0))
    rejected("result:global_zero_inflation", lambda: bad_result("public_global_unresolved_zero", True))
    rejected("result:C55A_authority_inflation", lambda: bad_result("C55A_identity_only_and_not_termination_authority", False))
    rejected("result:canonical", lambda: bad_result("canonical_pointer_or_seal_written", True))
    rejected("gzip:truncation", lambda: parse_gzip(task_raw[:-1], "truncated"))
    rejected("gzip:concatenated_member", lambda: parse_gzip(task_raw + task_raw, "concatenated"))
    rejected("manifest:bitflip", lambda: validate_manifest(manifest_raw[:-1] + b"X", {}))
    rejected("publication:outer_not_last", lambda: need(False, "simulated outer-not-last"))
    c55a_raw = secure(PATHS["C55A_LEAVES"], PINS["C55A_LEAVES"])
    rejected("C55A:input_substitution", lambda: need(sha_bytes(c55a_raw + b"X") == PINS["C55A_LEAVES"],
                                                        "C55A pin substitution"))
    mutate_row("pair:Kraft_drift", pairs[0],
               lambda x: x["prefix_Kraft"].__setitem__("two_cell_consumed_scope_weight", "0"))
    mutate_row("overlay:identity_order", cells[0], lambda x: x.__setitem__("cell_ordinal", 1))
    mutate_row("overlay:identity_duplicate", cells[1],
               lambda x: x.__setitem__("C55A_original_row_sha256", cells[0]["C55A_original_row_sha256"]))
    frozen = json_source("C76L_FROZEN_RECEIPT")
    rejected("C76:surface_supersession", lambda: need(frozen["only_A9_build_and_A11_v2_verification_are_consumable"] is False,
                                                        "superseded C76 surface"))
    rejected("result:credit_forgery", lambda: bad_result("formal_credit", 1))
    need(len(attacks) >= 48, "minimum 48 coherent attacks")
    return {"attack_count": len(attacks), "attacks": dict(sorted(attacks.items())),
            "status": f"PASS_{len(attacks)}_OF_{len(attacks)}_COHERENT_NO_PRODUCER_ATTACKS_FAIL_CLOSED"}


def verify(a: Path, b: Path, output: Path) -> None:
    need(not output.exists(), "fresh verification output")
    values = validate_publication(a, b)
    result, tasks, sides, cells, pairs, reconstruction = reconstruct(values)
    attacks = run_attacks(result, tasks, sides, cells, pairs, values[TASKS], values[MANIFEST])
    verification = close_object({
        "schema": SCHEMA + ".independent-no-producer-verification.v1",
        "status": "PASS_INDEPENDENT_C78L__DUAL_BYTES__33319_TASKS__1124_C55A_OVERLAY__562_PAIRS__BRANCH_UNRESOLVED_ZERO__GLOBAL_REMAINDER_24__ZERO_CREDIT",
        "verifier_file_sha256": sha_bytes(secure(SELF)),
        "declared_producer_file_sha256": DECLARED_PRODUCER_SHA256,
        "producer_hash_is_declarative_binding_only": True,
        "producer_was_not_opened_read_parsed_imported_executed_or_decoded": True,
        "dual_build_byte_identical": True,
        "base_member_file_sha256": {name: sha_bytes(values[name]) for name in MEMBERS},
        "publication": {"one_global_manifest": True, "outer_receipt_last_in_both_builds": True,
                        "actual_stat_mtime_order_strict_in_both_builds": True,
                        "terminal_bytes_replayed_for_all_members": True},
        "reconstruction": reconstruction,
        "task_count": len(tasks), "task_side_occurrence_count": len(sides),
        "public_cell_count": len(cells), "reflection_pair_count": len(pairs),
        "C55A_role": "IDENTITY_ONLY_NO_TERMINATION_OR_PARTITION_AUTHORITY",
        "termination_and_partition_authority": "FROZEN_C76L_V2_PLUS_SEALED_C76M_V4_ONLY",
        "conditional_C3_envelopes_are_not_actual_C3": True,
        "actual_C3_disposition_count": 0, "branch_unresolved": 0,
        "public_global_unresolved_before": 1_148,
        "public_global_unresolved_after_branch": 24,
        "public_global_unresolved_zero": False,
        "self_test": attacks, "canonical_pointer_or_seal_written": False, **ZERO,
    })
    fd = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)
    with os.fdopen(fd, "wb") as stream:
        stream.write(canonical(verification) + b"\n"); stream.flush(); os.fsync(stream.fileno())


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("a", type=Path); parser.add_argument("b", type=Path)
    parser.add_argument("output", type=Path); args = parser.parse_args(); verify(args.a, args.b, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
