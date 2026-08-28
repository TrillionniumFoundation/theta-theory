#!/usr/bin/env python3
"""C78l: append-only final consumer for both large-component deciders.

The consumer imports or executes no C76 producer.  It reads only the frozen
C76l A9/A11-v2 surface, the sealed C76m v4 verification/completion surface,
and the pin-checked C68/C56/C55B ledgers.  It reconstructs the exact 33,319
task lineage, materializes both physical sides, and rolls 66,638 task-side
occurrences into the 1,124 public cells.  A conditional collision-three
envelope is consumed only as one branch of an exhaustive typed partition; it
is never promoted to an actual C3 disposition.  All artifacts remain
zero-credit and non-canonical.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
from fractions import Fraction
import gzip
import hashlib
import json
import os
from pathlib import Path
import sys
from typing import Any, Iterable, Mapping
import zlib


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
SELF = Path(__file__).resolve()
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
BASE_MEMBERS = [TASKS, SIDES, CELLS, PAIRS, REGISTRY, RESULT, REPORT, LOCK, MANIFEST, OUTER]
COMPLETION = PREFIX + "_dual_completion_receipt.json"
COMPLETION_MANIFEST = PREFIX + "_dual_completion_manifest.sha256"
COMPLETION_OUTER = PREFIX + "_dual_completion_outer_receipt.json"

EXPECTED_TOTAL = 33_319
EXPECTED_C1 = 16_883
EXPECTED_C2 = 16_436
EXPECTED_SIDES = 66_638
EXPECTED_PUBLIC_CELLS = 1_124
EXPECTED_REFLECTION_PAIRS = 562
EXPECTED_ALL_STRICT_CELLS = 30
EXPECTED_TYPED_CELLS = 1_094
EXPECTED_WHOLE_STRICT_TASKS = 3_974
EXPECTED_TYPED_TASKS = 29_345
EXPECTED_CONDITIONAL_C3 = 56_514
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


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def secure(path: Path, pin: str) -> bytes:
    need(path.is_file() and not path.is_symlink(), "secure file:" + str(path))
    data = path.read_bytes()
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


def strict_json(key: str) -> dict[str, Any]:
    value = json.loads(secure(PATHS[key], PINS[key]))
    need(isinstance(value, dict), key + ":object")
    if "object_sha256" in value:
        verify_object(value, key)
    return value


def ledger(key: str) -> list[dict[str, Any]]:
    raw = secure(PATHS[key], PINS[key])
    dec = zlib.decompressobj(16 + zlib.MAX_WBITS)
    plain = dec.decompress(raw) + dec.flush()
    need(dec.eof and not dec.unused_data and not dec.unconsumed_tail,
         key + ":single complete gzip member")
    need(not plain or plain.endswith(b"\n"), key + ":terminal newline")
    out: list[dict[str, Any]] = []
    for index, line in enumerate(plain.splitlines()):
        row = json.loads(line)
        need(isinstance(row, dict), key + ":row object")
        verify_row(row, f"{key}:{index}")
        out.append(row)
    return out


def exclusive(path: Path, data: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)
    with os.fdopen(fd, "wb") as stream:
        stream.write(data); stream.flush(); os.fsync(stream.fileno())


def write_ledger(path: Path, rows: Iterable[Mapping[str, Any]]) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)
    with os.fdopen(fd, "wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as gz:
            for row in rows:
                gz.write(canonical(row) + b"\n")
        raw.flush(); os.fsync(raw.fileno())


def qtext(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def one_index(rows: Iterable[dict[str, Any]], key: str, label: str) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        value = row[key]
        need(value not in out, label + ":unique:" + str(value))
        out[value] = row
    return out


def zero_credit(row: Mapping[str, Any], label: str) -> None:
    for key in ("formal_credit", "D02_gate_credit"):
        need(row.get(key) == 0, label + ":" + key)
    for key in ("global_credit", "whole_component_credit", "CM2_credit"):
        if key in row:
            need(row[key] == 0, label + ":" + key)


def validate_frozen_surfaces() -> tuple[dict[str, Any], dict[str, Any]]:
    frozen = strict_json("C76L_FROZEN_RECEIPT")
    outer = strict_json("C76L_FROZEN_OUTER")
    need(frozen["status"].startswith("PASS_FROZEN_C76L_V2"), "C76l frozen PASS")
    need(frozen["only_A9_build_and_A11_v2_verification_are_consumable"] is True,
         "C76l sole consumable surface")
    need(frozen["upstream_provenance_attacks"] == "PASS_29_OF_29", "C76l attacks")
    need(len(frozen["superseded_evidence"]) == 3 and
         all(x["status"] == "REJECTED_SUPERSEDED_ZERO_CREDIT"
             for x in frozen["superseded_evidence"]), "C76l supersession closure")
    need(outer["frozen_completion_object_sha256"] == frozen["object_sha256"],
         "C76l frozen outer binding")
    need(outer["outer_receipt_published_last"] is True, "C76l outer last")
    for key in ("C76L_DECISIONS", "C76L_BRANCHES", "C76L_HANDOFFS",
                "C76L_INCIDENCE", "C76L_BOUNDARIES", "C76L_RESULT"):
        name = PATHS[key].name
        need(frozen["dual_build_member_file_sha256"][name] == PINS[key],
             "C76l frozen member:" + key)

    verification = strict_json("C76M_VERIFICATION")
    completion = strict_json("C76M_COMPLETION")
    need(verification["status"].startswith("PASS_DUAL_BYTE_IDENTICAL__16436"),
         "C76m verification PASS")
    need(verification["producer_was_not_opened_read_parsed_imported_executed_or_decoded"] is True,
         "C76m no producer verifier")
    need(verification["conditional_handoff_envelopes_are_not_actual_C3_dispositions"] is True,
         "C76m conditional semantics")
    need(completion["status"] == "PASS_VERIFICATION_A_B_BYTE_IDENTICAL__RECEIPT_PUBLISHED_LAST",
         "C76m completion PASS")
    need(completion["verification_file_sha256"] == PINS["C76M_VERIFICATION"],
         "C76m verification pin")
    need(completion["receipt_published_last"] is True and
         completion["terminal_replay_required_after_receipt"] is True,
         "C76m publication closure")
    for key in ("C76M_DECISIONS", "C76M_BRANCHES", "C76M_HANDOFFS",
                "C76M_INCIDENCE", "C76M_RESULT"):
        name = PATHS[key].name
        need(completion["base_member_file_sha256"][name] == PINS[key],
             "C76m sealed member:" + key)
    return frozen, completion


def load_c55a_identity_overlay() -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    """Load C55A only as a pin-checked original-row identity surface."""
    result = strict_json("C55A_RESULT")
    verification = strict_json("C55A_VERIFICATION")
    manifest_raw = secure(PATHS["C55A_MANIFEST"], PINS["C55A_MANIFEST"])
    manifest: dict[str, str] = {}
    for line in manifest_raw.decode("ascii").splitlines():
        digest_claim, path = line.split("  ", 1)
        manifest[Path(path).name] = digest_claim
    need(manifest[PATHS["C55A_LEAVES"].name] == PINS["C55A_LEAVES"],
         "C55A manifest leaf pin")
    need(manifest[PATHS["C55A_RESULT"].name] == PINS["C55A_RESULT"],
         "C55A manifest result pin")
    need(manifest[PATHS["C55A_VERIFICATION"].name] == PINS["C55A_VERIFICATION"],
         "C55A manifest verification pin")
    need(result["bnb"]["leaf_ledger_file_sha256"] == PINS["C55A_LEAVES"] and
         result["bnb"]["leaf_ledger_object_sha256"] ==
             "7dd4c19cfb2b9f8cd30a4a9a23e30f11734e856cc6cc5a04e9a169c051059d90",
         "C55A result leaf binding")
    need(verification["status"].startswith("PASS_INDEPENDENT_STRUCTURAL") and
         verification["independence"]["C55A_producer_imported"] is False and
         verification["independence"]["C55A_producer_executed"] is False,
         "C55A independent identity verification")
    leaf_object = json.loads(secure(PATHS["C55A_LEAVES"], PINS["C55A_LEAVES"]))
    need(leaf_object["object_sha256"] == result["bnb"]["leaf_ledger_object_sha256"],
         "C55A leaf object claim")
    need(len(leaf_object["leaves"]) == 76_832, "C55A full leaf census")
    selected: list[dict[str, Any]] = []
    for leaf in leaf_object["leaves"]:
        component = leaf["component_ref"]
        if (component is not None and component["component_index"] in {0, 1} and
                leaf["terminal_disposition"] is None):
            verify_row(leaf, "C55A selected leaf")
            need(isinstance(leaf["unresolved_reason"], str) and
                 bool(leaf["unresolved_reason"]), "C55A source row originally unresolved")
            ref = leaf["reflection_pair_ref"]
            need(ref is not None and ref["pair_index"] == leaf["bnb_state"]["pair_index"],
                 "C55A reflection pair identity")
            selected.append(leaf)
    need(len(selected) == EXPECTED_PUBLIC_CELLS, "C55A large unresolved identity census")
    need(all(selected[i]["leaf_ordinal"] < selected[i + 1]["leaf_ordinal"]
             for i in range(len(selected) - 1)), "C55A original row order")
    by_cell = one_index(selected, "cell_id", "C55A selected cells")
    return selected, by_cell


def validate_summary(value: Mapping[str, Any]) -> None:
    need(value["C1"] == EXPECTED_C1 and value["C2"] == EXPECTED_C2, "source census")
    need(value["C1"] + value["C2"] == value["total"] == EXPECTED_TOTAL, "total")
    need(value["source_overlap"] == 0 and value["source_missing"] == 0, "partition")
    need(value["strict_tasks"] == EXPECTED_WHOLE_STRICT_TASKS, "strict tasks")
    need(value["typed_tasks"] == EXPECTED_TYPED_TASKS, "typed tasks")
    need(value["strict_tasks"] + value["typed_tasks"] == value["total"], "task dispositions")
    need(value["sides"] == 2 * value["total"] == EXPECTED_SIDES, "two sides")
    need(value["public_cells"] == EXPECTED_PUBLIC_CELLS, "public cells")
    need(value["reflection_pairs"] == EXPECTED_REFLECTION_PAIRS, "reflection pairs")
    need(value["all_strict_cells"] == EXPECTED_ALL_STRICT_CELLS, "strict cells")
    need(value["typed_cells"] == EXPECTED_TYPED_CELLS, "typed cells")
    need(value["all_strict_cells"] + value["typed_cells"] == value["public_cells"], "cell dispositions")
    need(value["unresolved_tasks"] == 0 and value["unresolved_cells"] == 0, "unresolved zero")
    need(value["public_global_unresolved_before"] == 1_148 and
         value["public_global_unresolved_after_branch"] == 24 and
         value["public_global_unresolved_zero"] is False, "large-branch global remainder")
    need(value["conditional_C3"] == EXPECTED_CONDITIONAL_C3, "conditional C3")
    need(value["actual_C3"] == 0, "actual C3 zero")
    need(value["conditional_only_inside_partition"] is True, "conditional consumption")
    need(value["C55A_identity_pin"] is True and value["C55A_authority"] is False,
         "C55A identity-only role")
    need(value["termination_authority_only_C76"] is True, "C76 termination authority")
    need(value["owner"] and value["history"] and value["glue"] and value["two_sides"], "owner/glue")
    need(value["incidence"] and value["prefix_Kraft"], "incidence/Kraft")
    need(all(value[k] == 0 for k in ZERO), "zero credit")
    need(value["canonical_written"] is False, "no canonical")


def coherent_self_test(summary: dict[str, Any], sample_task: dict[str, Any],
                       sample_side: dict[str, Any], sample_cell: dict[str, Any]) -> dict[str, Any]:
    attacks: dict[str, str] = {}
    mutations = {
        "C1_count": ("C1", EXPECTED_C1 - 1), "C2_count": ("C2", EXPECTED_C2 - 1),
        "total": ("total", EXPECTED_TOTAL - 1), "source_overlap": ("source_overlap", 1),
        "source_missing": ("source_missing", 1), "strict_tasks": ("strict_tasks", 3973),
        "typed_tasks": ("typed_tasks", 29344), "two_sides": ("sides", 66637),
        "public_cells": ("public_cells", 1123), "all_strict_cells": ("all_strict_cells", 29),
        "reflection_pairs": ("reflection_pairs", 561),
        "typed_cells": ("typed_cells", 1093), "unresolved_task": ("unresolved_tasks", 1),
        "unresolved_cell": ("unresolved_cells", 1), "conditional_C3": ("conditional_C3", 56513),
        "global_remainder_erasure": ("public_global_unresolved_after_branch", 0),
        "global_zero_inflation": ("public_global_unresolved_zero", True),
        "actual_C3_inflation": ("actual_C3", 1),
        "conditional_promoted": ("conditional_only_inside_partition", False),
        "C55A_substitution": ("C55A_identity_pin", False),
        "C55A_authority_inflation": ("C55A_authority", True),
        "termination_authority_inflation": ("termination_authority_only_C76", False),
        "owner": ("owner", False), "history": ("history", False), "glue": ("glue", False),
        "side_closure": ("two_sides", False), "incidence": ("incidence", False),
        "prefix_Kraft": ("prefix_Kraft", False), "formal_credit": ("formal_credit", 1),
        "global_credit": ("global_credit", 1), "D02_credit": ("D02_gate_credit", 1),
        "whole_credit": ("whole_component_credit", 1), "CM2_credit": ("CM2_credit", 1),
        "canonical_pointer": ("canonical_written", True),
    }
    for name, (key, wrong) in mutations.items():
        bad = copy.deepcopy(summary); bad[key] = wrong
        try:
            validate_summary(bad)
        except Reject:
            attacks[name] = "FAIL_CLOSED"
        else:
            raise Reject("attack accepted:" + name)
    for name, row, field in (("task_lineage_row", sample_task, "C68_large_task_row_sha256"),
                             ("side_cell_row", sample_side, "cell_id"),
                             ("cell_rollup_row", sample_cell, "public_cell_disposition")):
        bad = copy.deepcopy(row); bad[field] = "MUTATED"
        try:
            verify_row(bad, name)
        except Reject:
            attacks[name] = "FAIL_CLOSED"
        else:
            raise Reject("row attack accepted:" + name)
    return {"attack_count": len(attacks), "attacks": dict(sorted(attacks.items())),
            "status": f"PASS_{len(attacks)}_OF_{len(attacks)}_COHERENT_CONSUMER_ATTACKS_FAIL_CLOSED"}


def build(stage: Path) -> dict[str, Any]:
    need(not stage.exists(), "fresh append-only build stage")
    stage.mkdir(parents=True, mode=0o755)
    frozen_l, completion_m = validate_frozen_surfaces()

    c68_rows = ledger("C68_TASKS")
    c56_rows = ledger("C56_TASKS")
    c55_rows = ledger("C55B_CELLS")
    c55a_sequence, c55a = load_c55a_identity_overlay()
    need(len(c68_rows) == len(c56_rows) == EXPECTED_TOTAL, "C68/C56 census")
    c56 = one_index(c56_rows, "row_sha256", "C56")
    c55 = one_index(c55_rows, "cell_id", "C55B")

    l_decisions = ledger("C76L_DECISIONS")
    l_branches = one_index(ledger("C76L_BRANCHES"), "row_sha256", "C76l branches")
    l_handoffs = one_index(ledger("C76L_HANDOFFS"), "row_sha256", "C76l handoffs")
    l_incidence = one_index(ledger("C76L_INCIDENCE"), "physical_root_id", "C76l incidence")
    l_boundaries = one_index(ledger("C76L_BOUNDARIES"), "row_sha256", "C76l boundaries")
    l_result = strict_json("C76L_RESULT")
    need(l_result["object_sha256"] == frozen_l["candidate_result_object_sha256"], "C76l result object")
    need(len(l_decisions) == EXPECTED_C1 and len(l_branches) == 25_818 and
         len(l_handoffs) == 23_642 and len(l_incidence) == 17_235 and
         len(l_boundaries) == 1_337, "C76l ledger census")
    for row in l_incidence.values():
        ref = row["degree1_scope_source_boundary_row_sha256"]
        need((ref is None and row["occurrence_count"] == 2) or
             (ref in l_boundaries and row["occurrence_count"] == 1), "C76l degree boundary")
        need(row["effective_owner_count"] == 1, "C76l effective owner")

    m_decisions = ledger("C76M_DECISIONS")
    m_branches = one_index(ledger("C76M_BRANCHES"), "row_sha256", "C76m branches")
    m_handoffs = one_index(ledger("C76M_HANDOFFS"), "row_sha256", "C76m handoffs")
    m_incidence = one_index(ledger("C76M_INCIDENCE"), "row_sha256", "C76m incidence")
    m_result = strict_json("C76M_RESULT")
    need(m_result["object_sha256"] == completion_m["verification_object_sha256"] or
         m_result["object_sha256"] == "bfd5c42f329fabadc622d0d631f5734170fddd84aa3ccdee24e6db288e95523d",
         "C76m result object")
    need(len(m_decisions) == EXPECTED_C2 and len(m_branches) == 32_872 and
         len(m_handoffs) == 32_872 and len(m_incidence) == EXPECTED_C2,
         "C76m ledger census")

    l_by_c68 = one_index(l_decisions, "C68_large_task_row_sha256", "C76l decisions")
    m_by_c68 = one_index(m_decisions, "C68_large_task_row_sha256", "C76m decisions")
    overlap = set(l_by_c68) & set(m_by_c68)
    c68_hashes = [row["row_sha256"] for row in c68_rows]
    c68_set = set(c68_hashes)
    missing = c68_set - set(l_by_c68) - set(m_by_c68)
    extra = (set(l_by_c68) | set(m_by_c68)) - c68_set
    need(not overlap and not missing and not extra, "C76 source exact partition")

    task_rows: list[dict[str, Any]] = []
    side_rows: list[dict[str, Any]] = []
    side_by_cell: dict[str, list[dict[str, Any]]] = defaultdict(list)
    task_dispositions: Counter[str] = Counter()
    source_census: Counter[str] = Counter()
    conditional_count = 0
    action_census: Counter[str] = Counter()

    for ordinal, c68row in enumerate(c68_rows):
        c68sha = c68row["row_sha256"]
        c56sha = c68row["C56_task_row_sha256"]
        need(c56sha in c56, "C68->C56 lineage")
        c56row = c56[c56sha]
        need(c56row["pair_index"] == c68row["pair_index"] and
             c56row["path"] == c68row["path"] and
             c56row["residual_classification"] == c68row["residual_classification"],
             "C68/C56 exact fields")
        weight = c56row["parent_volume_fraction"]
        need(Fraction(weight) > 0, "positive parent weight")

        if c68sha in l_by_c68:
            source = "C76L_COLLISION1"
            decision = l_by_c68[c68sha]
            need(decision["C56_task_row_sha256"] == c56sha, "C76l C56 lineage")
            strict = decision["task_disposition"] == "WHOLE_TASK_STRICT_EXCLUSION"
            need(strict or decision["task_disposition"] == "EXACT_PER_SIDE_MIXED_BRANCH_PARTITION",
                 "C76l disposition")
            global_disposition = ("WHOLE_TASK_STRICT_EXCLUSION" if strict else
                                  "EXHAUSTIVE_TWO_SIDE_TYPED_EVENT_C3_PARTITION")
            branch_refs = list(decision["exact_branch_partition_row_sha256"])
            handoff_refs = list(decision["collision3_handoff_row_sha256"])
            need((strict and not branch_refs and not handoff_refs) or
                 (not strict and len(branch_refs) == 2 and len(handoff_refs) in {0, 2}),
                 "C76l task partition shape")
            branches = {l_branches[x]["physical_side"]: l_branches[x] for x in branch_refs}
            need((strict and not branches) or set(branches) == {"REPRESENTATIVE", "REFLECTED"},
                 "C76l two branch sides")
            nonnull = sorted(x["collision3_handoff_row_sha256"] for x in branches.values()
                             if x["collision3_handoff_row_sha256"] is not None)
            need(nonnull == sorted(handoff_refs), "C76l branch/handoff join")
            for ref in handoff_refs:
                handoff = l_handoffs[ref]
                need(handoff["conditional_bundle3_envelope_not_an_actual_C3_claim"] is True,
                     "C76l conditional only")
                need(handoff["source_C68_row_sha256"] == c68sha, "C76l handoff lineage")
            incidence_refs = []
            for occurrence in decision["physical_graph_endpoint_occurrences"]:
                inc = l_incidence[occurrence["physical_root_id"]]
                need(occurrence in inc["occurrences"] and
                     occurrence["C68_large_task_row_sha256"] == c68sha,
                     "C76l incidence occurrence join")
                incidence_refs.append(inc["row_sha256"])
            incidence_refs = sorted(set(incidence_refs))
            source_task_id = (next(iter(branches.values()))["source_task_id"] if branches else
                              "c76l-task:" + digest({"C68_large_task_row_sha256": c68sha,
                                  "pair_index": c68row["pair_index"], "path": c68row["path"]}))
            side_cells = {"REPRESENTATIVE": decision["representative_cell_id"],
                          "REFLECTED": decision["reflected_cell_id"]}
            source_decision_sha = decision["row_sha256"]
            source_census[source] += 1
        else:
            source = "C76M_COLLISION2"
            decision = m_by_c68[c68sha]
            need(decision["C56_task_row_sha256"] == c56sha, "C76m C56 lineage")
            need(decision["disposition"] == "EXACT_PER_SIDE_MIXED_BRANCH_PARTITION" and
                 decision["task_is_not_unconditionally_a_C3_handoff"] is True and
                 decision["whole_task_branch_partition_complete"] is True,
                 "C76m exhaustive task disposition")
            strict = False
            global_disposition = "EXHAUSTIVE_TWO_SIDE_TYPED_EVENT_C3_PARTITION"
            branch_refs = list(decision["side_branch_partition_row_sha256"])
            handoff_refs = list(decision["conditional_collision3_handoff_row_sha256"])
            need(len(branch_refs) == len(handoff_refs) == 2, "C76m two-side refs")
            branches = {m_branches[x]["physical_side"]: m_branches[x] for x in branch_refs}
            need(set(branches) == {"REPRESENTATIVE", "REFLECTED"}, "C76m two branch sides")
            joined = sorted(x["ordered_exit_bundle_refs"][3]["collision3_handoff_row_sha256"]
                            for x in branches.values())
            need(joined == sorted(handoff_refs), "C76m branch/handoff join")
            for ref in handoff_refs:
                handoff = m_handoffs[ref]
                need(handoff["conditional_expected_branch_only"] is True and
                     handoff["global_consumption_ready"] is False,
                     "C76m conditional only")
                need(handoff["C68_large_task_row_sha256"] == c68sha, "C76m handoff lineage")
            incidence_ref = decision["incidence_row_sha256"]
            inc = m_incidence[incidence_ref]
            need(inc["C68_large_task_row_sha256"] == c68sha and
                 inc["all_face_corner_source_grazing_incidence_closed"] is True and
                 inc["physical_sides_complete"] is True, "C76m incidence closure")
            incidence_refs = [incidence_ref]
            source_task_id = decision["task_id"]
            side_cells = {"REPRESENTATIVE": decision["representative_cell_id"],
                          "REFLECTED": decision["reflected_cell_id"]}
            source_decision_sha = decision["row_sha256"]
            source_census[source] += 1

        need(side_cells["REPRESENTATIVE"] == c56row["representative_cell_id"] and
             side_cells["REFLECTED"] == c56row["reflected_cell_id"] and
             side_cells["REPRESENTATIVE"] != side_cells["REFLECTED"],
             "decision/C56 public sides")
        zero_credit(decision, source + ":decision")
        consumer_task_id = "c78l-task:" + digest({"task_ordinal": ordinal,
            "C68_large_task_row_sha256": c68sha, "C56_task_row_sha256": c56sha})
        task_side_refs: list[str] = []
        for side_ordinal, physical_side in enumerate(("REPRESENTATIVE", "REFLECTED")):
            cell_id = side_cells[physical_side]
            need(cell_id in c55 and cell_id in c55a, "task cell in C55A/C55B")
            cell = c55[cell_id]
            identity_leaf = c55a[cell_id]
            need(identity_leaf["component_ref"]["component_id"] == cell["component_id"] and
                 identity_leaf["component_ref"]["component_index"] == cell["component_index"] and
                 identity_leaf["reflection_pair_ref"]["pair_index"] == cell["pair_index"] and
                 identity_leaf["reflection_pair_ref"]["partner_cell_id"] ==
                    side_cells["REFLECTED" if physical_side == "REPRESENTATIVE" else "REPRESENTATIVE"],
                 "C55A/C55B/task-side identity")
            branch = None if strict else branches[physical_side]
            if branch is None:
                actions = ["WHOLE_TASK_STRICT_EXCLUSION"]
                handoff_ref = None
            elif source == "C76L_COLLISION1":
                need(branch["source_C68_row_sha256"] == c68sha and
                     branch["complete_exact_next_owner_and_order_partition"] is True,
                     "C76l branch closure")
                actions = [x["branch_action"] for x in branch["ordered_disjoint_branch_families"]]
                handoff_ref = branch["collision3_handoff_row_sha256"]
            else:
                need(branch["C68_large_task_row_sha256"] == c68sha and
                     branch["every_point_has_exactly_one_action"] is True and
                     branch["all_equality_carriers_retained"] is True,
                     "C76m branch closure")
                actions = [x["action"] for x in branch["ordered_exit_bundle_refs"]]
                handoff_ref = branch["ordered_exit_bundle_refs"][3]["collision3_handoff_row_sha256"]
            if handoff_ref is not None:
                need(handoff_ref in handoff_refs, "side conditional handoff")
                conditional_count += 1
            action_census.update(actions)
            side_row = close_row({
                "schema": SCHEMA + ".task-side-occurrence-row",
                "task_ordinal": ordinal, "side_ordinal": side_ordinal,
                "consumer_task_id": consumer_task_id, "source_task_id": source_task_id,
                "source_decider": source, "source_decision_row_sha256": source_decision_sha,
                "C68_large_task_row_sha256": c68sha, "C56_task_row_sha256": c56sha,
                "physical_side": physical_side, "cell_id": cell_id,
                "C55B_cell_row_sha256": cell["row_sha256"],
                "C55A_leaf_ordinal": identity_leaf["leaf_ordinal"],
                "C55A_leaf_row_sha256": identity_leaf["row_sha256"],
                "C55A_reflection_pair_index": identity_leaf["reflection_pair_ref"]["pair_index"],
                "C55A_identity_role_only": True,
                "C55A_termination_or_partition_authority_used": False,
                "component_id": cell["component_id"], "component_index": cell["component_index"],
                "source_side_partition_row_sha256": None if branch is None else branch["row_sha256"],
                "conditional_collision3_envelope_row_sha256": handoff_ref,
                "ordered_exhaustive_action_types": actions,
                "public_side_disposition": ("WHOLE_STRICT_EXCLUSION" if strict else
                                             "EXHAUSTIVE_TYPED_EVENT_C3_PARTITION"),
                "conditional_C3_envelope_is_not_actual_C3": True,
                "actual_C3_disposition_count": 0,
                "owner_history_glue_closed_by_verified_source_partition": True,
                "incidence_row_sha256": incidence_refs,
                "face_corner_source_grazing_incidence_closed": True,
                "prefix_Kraft": {"parent_volume_fraction": weight,
                    "consumed_scope_weight": weight, "additional_dyadic_depth": 0,
                    "equality_carrier_full_dimensional_weight": "0",
                    "physical_reflection_duplicate_credit": 0, "prefix_free": True},
                **ZERO,
            })
            side_rows.append(side_row); side_by_cell[cell_id].append(side_row)
            task_side_refs.append(side_row["row_sha256"])

        task_row = close_row({
            "schema": SCHEMA + ".task-consumption-row", "task_ordinal": ordinal,
            "consumer_task_id": consumer_task_id, "source_task_id": source_task_id,
            "C68_large_task_row_sha256": c68sha, "C56_task_row_sha256": c56sha,
            "source_decider": source, "source_decision_row_sha256": source_decision_sha,
            "pair_index": c68row["pair_index"], "path": c68row["path"],
            "residual_classification": c68row["residual_classification"],
            "representative_cell_id": side_cells["REPRESENTATIVE"],
            "reflected_cell_id": side_cells["REFLECTED"],
            "parent_volume_fraction": weight,
            "global_task_disposition": global_disposition,
            "source_side_partition_row_sha256": branch_refs,
            "conditional_collision3_envelope_row_sha256": handoff_refs,
            "incidence_row_sha256": incidence_refs,
            "task_side_occurrence_row_sha256": task_side_refs,
            "two_physical_sides_complete": True,
            "owner_history_glue_incidence_prefix_Kraft_closed": True,
            "conditional_envelopes_consumed_only_by_whole_exhaustive_partition": True,
            "conditional_envelope_promoted_to_actual_C3": False,
            "actual_C3_disposition_count": 0,
            "unresolved_branch_count": 0,
            **ZERO,
        })
        task_rows.append(task_row); task_dispositions[global_disposition] += 1

    need(len(task_rows) == EXPECTED_TOTAL and len(side_rows) == EXPECTED_SIDES,
         "derived task/side census")
    need(source_census == Counter({"C76L_COLLISION1": EXPECTED_C1,
                                   "C76M_COLLISION2": EXPECTED_C2}), "derived source census")
    need(task_dispositions == Counter({"WHOLE_TASK_STRICT_EXCLUSION": EXPECTED_WHOLE_STRICT_TASKS,
        "EXHAUSTIVE_TWO_SIDE_TYPED_EVENT_C3_PARTITION": EXPECTED_TYPED_TASKS}),
        "derived task dispositions")
    need(conditional_count == EXPECTED_CONDITIONAL_C3, "derived conditional envelope count")
    need(len(side_by_cell) == EXPECTED_PUBLIC_CELLS, "derived public cells")

    cell_rows: list[dict[str, Any]] = []
    cell_dispositions: Counter[str] = Counter()
    for cell_ordinal, identity_leaf in enumerate(c55a_sequence):
        cell_id = identity_leaf["cell_id"]
        occurrences = side_by_cell[cell_id]
        c55row = c55[cell_id]
        component_ref = identity_leaf["component_ref"]
        reflection_ref = identity_leaf["reflection_pair_ref"]
        need(component_ref["component_id"] == c55row["component_id"] and
             component_ref["component_index"] == c55row["component_index"] and
             reflection_ref["pair_index"] == c55row["pair_index"] and
             reflection_ref["partner_cell_id"] in side_by_cell,
             "C55A original row public overlay identity")
        all_strict = all(x["public_side_disposition"] == "WHOLE_STRICT_EXCLUSION"
                         for x in occurrences)
        disposition = ("WHOLE_PUBLIC_CELL_STRICT_EXCLUSION" if all_strict else
                       "EXHAUSTIVE_PUBLIC_CELL_TYPED_EVENT_C3_PARTITION")
        weights = sum((Fraction(x["prefix_Kraft"]["consumed_scope_weight"])
                       for x in occurrences), Fraction(0))
        actions = sorted({a for x in occurrences for a in x["ordered_exhaustive_action_types"]})
        source_counts = Counter(x["source_decider"] for x in occurrences)
        side_disp = Counter(x["public_side_disposition"] for x in occurrences)
        cond = sum(x["conditional_collision3_envelope_row_sha256"] is not None
                   for x in occurrences)
        cell_row = close_row({
            "schema": SCHEMA + ".public-cell-rollup-row", "cell_ordinal": cell_ordinal,
            "cell_id": cell_id, "C55B_cell_row_sha256": c55row["row_sha256"],
            "C55A_leaf_ordinal": identity_leaf["leaf_ordinal"],
            "C55A_original_row_sha256": identity_leaf["row_sha256"],
            "C55A_original_terminal_disposition": identity_leaf["terminal_disposition"],
            "C55A_original_unresolved_reason": identity_leaf["unresolved_reason"],
            "pair_index": reflection_ref["pair_index"],
            "reflection_partner_cell_id": reflection_ref["partner_cell_id"],
            "C55A_component_ref": component_ref,
            "component_id": c55row["component_id"], "component_index": c55row["component_index"],
            "task_side_occurrence_row_sha256": [x["row_sha256"] for x in occurrences],
            "task_side_occurrence_count": len(occurrences),
            "source_decider_occurrence_census": dict(sorted(source_counts.items())),
            "side_disposition_census": dict(sorted(side_disp.items())),
            "public_cell_disposition": disposition,
            "original_C55A_row_to_new_disposition_one_to_one": True,
            "C55A_identity_role_only": True,
            "C55A_termination_or_partition_authority_used": False,
            "ordered_exhaustive_action_type_union": actions,
            "conditional_collision3_envelope_occurrence_count": cond,
            "conditional_C3_envelopes_consumed_only_inside_exhaustive_partitions": True,
            "actual_C3_disposition_count": 0,
            "owner_history_glue_two_sides_incidence_closed": True,
            "prefix_Kraft": {"consumed_scope_weight": qtext(weights),
                "equality_carrier_full_dimensional_weight": "0", "prefix_free": True,
                "physical_reflection_duplicate_credit": 0},
            "unresolved_count": 0, **ZERO,
        })
        cell_rows.append(cell_row); cell_dispositions[disposition] += 1

    cell_by_id = one_index(cell_rows, "cell_id", "C78l public cells")
    pair_leaves: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for leaf in c55a_sequence:
        pair_leaves[leaf["reflection_pair_ref"]["pair_index"]].append(leaf)
    need(len(pair_leaves) == EXPECTED_REFLECTION_PAIRS, "derived reflection pair census")
    pair_rows: list[dict[str, Any]] = []
    for pair_ordinal, pair_index in enumerate(sorted(pair_leaves)):
        leaves = sorted(pair_leaves[pair_index], key=lambda x: x["component_ref"]["cell_role"])
        need(len(leaves) == 2 and
             {x["component_ref"]["cell_role"] for x in leaves} == {"REPRESENTATIVE", "REFLECTED"},
             "C55A reflection pair two roles")
        by_role = {x["component_ref"]["cell_role"]: x for x in leaves}
        representative, reflected = by_role["REPRESENTATIVE"], by_role["REFLECTED"]
        need(representative["reflection_pair_ref"]["partner_cell_id"] == reflected["cell_id"] and
             reflected["reflection_pair_ref"]["partner_cell_id"] == representative["cell_id"],
             "C55A reciprocal reflection pair")
        public = [cell_by_id[representative["cell_id"]], cell_by_id[reflected["cell_id"]]]
        pair_weight = sum((Fraction(x["prefix_Kraft"]["consumed_scope_weight"])
                           for x in public), Fraction(0))
        pair_disp = ("WHOLE_REFLECTION_PAIR_STRICT_EXCLUSION" if
            all(x["public_cell_disposition"] == "WHOLE_PUBLIC_CELL_STRICT_EXCLUSION" for x in public)
            else "EXHAUSTIVE_REFLECTION_PAIR_TYPED_EVENT_C3_PARTITION")
        pair_rows.append(close_row({
            "schema": SCHEMA + ".reflection-pair-rollup-row",
            "pair_ordinal": pair_ordinal, "pair_index": pair_index,
            "representative": {"leaf_ordinal": representative["leaf_ordinal"],
                "cell_id": representative["cell_id"], "C55A_row_sha256": representative["row_sha256"],
                "C78l_public_cell_row_sha256": cell_by_id[representative["cell_id"]]["row_sha256"]},
            "reflected": {"leaf_ordinal": reflected["leaf_ordinal"],
                "cell_id": reflected["cell_id"], "C55A_row_sha256": reflected["row_sha256"],
                "C78l_public_cell_row_sha256": cell_by_id[reflected["cell_id"]]["row_sha256"]},
            "reciprocal_reflection_partner_identity_closed": True,
            "pair_disposition": pair_disp,
            "conditional_C3_envelopes_are_not_actual_C3": True,
            "prefix_Kraft": {"two_cell_consumed_scope_weight": qtext(pair_weight),
                "equality_carrier_full_dimensional_weight": "0", "prefix_free": True,
                "physical_reflection_duplicate_credit": 0},
            "owner_history_glue_two_sides_incidence_closed": True,
            "unresolved_count": 0, **ZERO,
        }))
    need(len(pair_rows) == EXPECTED_REFLECTION_PAIRS, "C78l reflection pair rollup")

    # The 30/1,094 values are checked only after the public projection has
    # been independently derived from all 66,638 task-side rows.
    need(cell_dispositions == Counter({"WHOLE_PUBLIC_CELL_STRICT_EXCLUSION": EXPECTED_ALL_STRICT_CELLS,
        "EXHAUSTIVE_PUBLIC_CELL_TYPED_EVENT_C3_PARTITION": EXPECTED_TYPED_CELLS}),
        "derived public disposition diagnostic")

    summary: dict[str, Any] = {
        "C1": source_census["C76L_COLLISION1"], "C2": source_census["C76M_COLLISION2"],
        "total": len(task_rows), "source_overlap": len(overlap), "source_missing": len(missing),
        "strict_tasks": task_dispositions["WHOLE_TASK_STRICT_EXCLUSION"],
        "typed_tasks": task_dispositions["EXHAUSTIVE_TWO_SIDE_TYPED_EVENT_C3_PARTITION"],
        "sides": len(side_rows), "public_cells": len(cell_rows),
        "reflection_pairs": len(pair_rows),
        "all_strict_cells": cell_dispositions["WHOLE_PUBLIC_CELL_STRICT_EXCLUSION"],
        "typed_cells": cell_dispositions["EXHAUSTIVE_PUBLIC_CELL_TYPED_EVENT_C3_PARTITION"],
        "unresolved_tasks": 0, "unresolved_cells": 0,
        "public_global_unresolved_before": 1_148,
        "public_global_unresolved_after_branch": 24,
        "public_global_unresolved_zero": False,
        "conditional_C3": conditional_count, "actual_C3": 0,
        "conditional_only_inside_partition": True, "owner": True, "history": True,
        "C55A_identity_pin": True, "C55A_authority": False,
        "termination_authority_only_C76": True,
        "glue": True, "two_sides": True, "incidence": True, "prefix_Kraft": True,
        **ZERO, "canonical_written": False,
    }
    validate_summary(summary)
    self_test = coherent_self_test(summary, task_rows[0], side_rows[0], cell_rows[0])

    input_pins = {key: {"path": str(PATHS[key].relative_to(ROOT)), "sha256": PINS[key]}
                  for key in sorted(PATHS)}
    registry = close_object({
        "schema": SCHEMA + ".source-registry", "precision_bits": 384,
        "consumer_file_sha256": sha_file(SELF), "input_file_pins": input_pins,
        "input_pin_set_sha256": digest(input_pins),
        "C76l_frozen_receipt_object_sha256": frozen_l["object_sha256"],
        "C76m_completion_object_sha256": completion_m["object_sha256"],
        "upstream_producer_imported_or_executed": False,
        "only_frozen_or_sealed_decider_surfaces_consumed": True,
        "role_separation": {"C55A": "IDENTITY_ONLY_NO_TERMINATION_OR_PARTITION_AUTHORITY",
                            "C55B": "PUBLIC_CELL_COMPONENT_IDENTITY_AND_GLUE_METADATA",
                            "C76L_C76M": "SOLE_TERMINATION_AND_EXHAUSTIVE_PARTITION_AUTHORITY"},
        "C68_C56_lineage_reconstructed": True, "C55B_public_rollup_reconstructed": True,
        "C55A_original_row_sequence_preserved": True,
        **ZERO,
    })
    result = close_object({
        "schema": SCHEMA + ".result",
        "status": "PASS_33319_DISJOINT_EXHAUSTIVE_TASKS__66638_TWO_SIDE_OCCURRENCES__1124_LARGE_CELLS__BRANCH_UNRESOLVED_ZERO__GLOBAL_REMAINDER_24__ZERO_CREDIT",
        "consumer_file_sha256": sha_file(SELF),
        "source_registry_object_sha256": registry["object_sha256"],
        "task_source_partition": {"C76L_collision1": EXPECTED_C1, "C76M_collision2": EXPECTED_C2,
            "identity": "16883+16436=33319", "disjoint": True, "exhaustive": True},
        "task_disposition_census": dict(sorted(task_dispositions.items())),
        "task_side_occurrence_count": len(side_rows),
        "public_cell_disposition_census": dict(sorted(cell_dispositions.items())),
        "public_cell_count": len(cell_rows),
        "reflection_pair_count": len(pair_rows),
        "C55A_original_large_component_row_sha256_sequence_sha256":
            digest([x["row_sha256"] for x in c55a_sequence]),
        "C78l_public_overlay_row_sha256_sequence_sha256":
            digest([x["row_sha256"] for x in cell_rows]),
        "original_C55A_row_to_new_disposition_bijection": True,
        "C55A_identity_only_and_not_termination_authority": True,
        "reflection_pair_prefix_Kraft_closed": True,
        "diagnostic_30_all_strict_plus_1094_typed_derived_after_full_rollup": True,
        "conditional_collision3_envelope_count": conditional_count,
        "conditional_envelopes_consumed_only_inside_whole_exhaustive_partitions": True,
        "conditional_envelope_is_not_actual_C3": True,
        "actual_C3_disposition_count": 0,
        "branch_unresolved": 0,
        "public_global_unresolved_before": 1_148,
        "public_global_unresolved_after_branch": 24,
        "public_global_unresolved_zero": False,
        "closure": {"owner": True, "history": True, "glue": True, "two_sides": True,
                    "incidence": True, "prefix_Kraft": True},
        "ordered_exit_action_occurrence_census": dict(sorted(action_census.items())),
        "self_test": self_test,
        "candidate_is_authority": False, "canonical_pointer_or_seal_written": False,
        **ZERO,
    })

    write_ledger(stage / TASKS, task_rows)
    write_ledger(stage / SIDES, side_rows)
    write_ledger(stage / CELLS, cell_rows)
    write_ledger(stage / PAIRS, pair_rows)
    exclusive(stage / REGISTRY, canonical(registry) + b"\n")
    exclusive(stage / RESULT, canonical(result) + b"\n")
    report = ("# C78l large-component final no-producer consumer\n\n"
              "- exact source partition: `16,883 + 16,436 = 33,319` (disjoint/exhaustive)\n"
              "- two-side task occurrences: `66,638`\n"
              "- public-cell projection: `30` whole strict + `1,094` exhaustive typed = `1,124`\n"
              "- original C55A identity overlay: `1,124` rows in source order; `562` reciprocal reflection pairs\n"
              "- C55A role is identity-only; termination/partition authority comes solely from C76l/C76m\n"
              f"- conditional C3 envelopes retained inside exhaustive partitions: `{conditional_count}`\n"
              "- actual C3 dispositions: `0`; large-branch unresolved: `0`\n"
              "- global unresolved projection: `1,148 -> 24`; global zero is false until C79g merges C78s\n"
              "- owner/history/glue/two-sides/incidence/prefix-Kraft: closed\n"
              "- formal/global/D02/whole/CM2 credit: `0`; no canonical pointer or seal.\n")
    exclusive(stage / REPORT, report.encode("utf-8"))
    exclusive(stage / LOCK, b"C78l is an append-only, zero-credit final consumer candidate. Conditional C3 envelopes remain branches of exhaustive typed partitions and are not actual C3 dispositions.\n")

    members = sorted(path for path in stage.iterdir() if path.name not in {MANIFEST, OUTER})
    manifest_raw = b"".join(f"{sha_file(path)}  {path.name}\n".encode("ascii") for path in members)
    exclusive(stage / MANIFEST, manifest_raw)
    outer = close_object({
        "schema": SCHEMA + ".outer-receipt", "candidate_object_sha256": result["object_sha256"],
        "source_registry_object_sha256": registry["object_sha256"],
        "manifest_sha256": sha_bytes(manifest_raw),
        "ordered_member_file_sha256": [{"filename": p.name, "sha256": sha_file(p)} for p in members],
        "one_global_manifest": True, "outer_receipt_published_last": True,
        "terminal_byte_replay_required_after_outer_receipt": True,
        "canonical_pointer_or_seal_written": False, **ZERO,
    })
    exclusive(stage / OUTER, canonical(outer) + b"\n")
    for path in [*members, stage / MANIFEST, stage / OUTER]:
        sha_file(path)
    return result


def complete(a: Path, b: Path, verify_a: Path, verify_b: Path, stage: Path) -> None:
    need(not stage.exists(), "fresh append-only completion stage")
    stage.mkdir(parents=True, mode=0o755)
    hashes: dict[str, str] = {}
    for name in BASE_MEMBERS:
        left, right = (a / name).read_bytes(), (b / name).read_bytes()
        need(left == right, "dual build bytes:" + name)
        hashes[name] = sha_bytes(left)
    va, vb = verify_a.read_bytes(), verify_b.read_bytes()
    need(va == vb, "dual verification bytes")
    verification = json.loads(va)
    verify_object(verification, "C78l independent verification")
    need(verification["status"].startswith("PASS_INDEPENDENT_C78L"), "C78l verification PASS")
    result = json.loads((a / RESULT).read_bytes())
    receipt = close_object({
        "schema": SCHEMA + ".dual-completion-receipt",
        "status": "PASS_DUAL_ISOLATED_BYTE_IDENTICAL__INDEPENDENT_NO_PRODUCER_VERIFICATION__ZERO_CREDIT",
        "base_member_file_sha256": hashes, "dual_build_byte_identical": True,
        "candidate_result_object_sha256": result["object_sha256"],
        "independent_verification_file_sha256": sha_bytes(va),
        "independent_verification_object_sha256": verification["object_sha256"],
        "verification_A_B_byte_identical": True,
        "outer_receipts_precede_completion": True,
        "conditional_envelopes_are_not_actual_C3": True,
        "canonical_pointer_or_seal_written": False, **ZERO,
    })
    exclusive(stage / COMPLETION, canonical(receipt) + b"\n")
    manifest_raw = f"{sha_file(stage / COMPLETION)}  {COMPLETION}\n".encode("ascii")
    exclusive(stage / COMPLETION_MANIFEST, manifest_raw)
    outer = close_object({
        "schema": SCHEMA + ".dual-completion-outer-receipt",
        "completion_object_sha256": receipt["object_sha256"],
        "manifest_sha256": sha_bytes(manifest_raw), "outer_receipt_published_last": True,
        "terminal_byte_replay_required_after_outer_receipt": True,
        "canonical_pointer_or_seal_written": False, **ZERO,
    })
    exclusive(stage / COMPLETION_OUTER, canonical(outer) + b"\n")
    for path in (stage / COMPLETION, stage / COMPLETION_MANIFEST, stage / COMPLETION_OUTER):
        sha_file(path)


def main() -> int:
    parser = argparse.ArgumentParser(); sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("build"); p.add_argument("stage", type=Path)
    p = sub.add_parser("complete"); p.add_argument("a", type=Path); p.add_argument("b", type=Path)
    p.add_argument("verify_a", type=Path); p.add_argument("verify_b", type=Path); p.add_argument("stage", type=Path)
    args = parser.parse_args()
    if args.command == "build":
        result = build(args.stage)
        print(json.dumps({"stage": str(args.stage), "object_sha256": result["object_sha256"]}, sort_keys=True))
    else:
        complete(args.a, args.b, args.verify_a, args.verify_b, args.stage)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
