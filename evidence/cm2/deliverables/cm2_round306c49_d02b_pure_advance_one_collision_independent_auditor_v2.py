#!/usr/bin/env python3
"""Independent structural/replay auditor for the C49 D02-B v2 kernel.

The auditor never imports C44 output as occurrence proof.  It freezes the v2
producer source, independently checks closed hashes and exact candidate-table
commitments, verifies the pair-9 census and the collision 3 -> 4 -> 5 history
links, scans the AST for mutation APIs, and replays the complete regression a
second time to require byte-identical deterministic output.
"""

from __future__ import annotations

import argparse
import ast
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


sys.dont_write_bytecode = True
SELF = Path(__file__).absolute()
DELIVERABLES = SELF.parent
if str(DELIVERABLES) not in sys.path:
    sys.path.insert(0, str(DELIVERABLES))

import cm2_round306c49_d02b_pure_advance_one_collision_v2 as producer


SCHEMA = "cm2.round306c49.d02-b-pure-advance-one-collision-independent-audit.v2"
PRODUCER_SHA256 = "25d87f0ae27b7946ab9f55dbe8a5f50c353eb9f05dd4a6e50810d92e438700df"
EXPECTED_REGRESSION_SHA256 = "e82085e0b463dc3d38dccc9e4d58b4d0f20aa120bab0ccd7025b61e6de688fc3"
EXPECTED_COLLISION3_STEP_SHA256 = "03e2d72d5528f88a004cb981ff89dd505d0a122b9c2787c7133a316b87ec3172"
EXPECTED_COLLISION4_STEP_SHA256 = "f8626355f519cef4a8bfff44d3be35b944a8aa21ad9b5fb0f86c8ffffbb62429"
EXPECTED_COLLISION5_STEP_SHA256 = "00bf54e317c9af90cdefbf53890d449afddbdb9d6335af9acece971649a701bf"
EXPECTED_COLLISION4_TREE_SHA256 = "963dfb04aca9e4b0ac62e22867783e7b214469cf6ea24c0bf095db606e97ea1f"

REQUIRED_STEP_FIELDS = {
    "exact_owner", "discriminant", "root_order", "official_word", "chart",
    "wall", "homogeneity", "incidence", "core",
    "structured_terminal_decision_margin", "full_candidate_table",
}
MUTATING_CALL_NAMES = {
    "write", "write_bytes", "write_text", "unlink", "rename", "replace",
    "mkdir", "rmdir", "remove", "link", "symlink", "chmod", "chown",
    "truncate", "fsync",
}


class Rejected(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def close_object(value: dict[str, Any]) -> dict[str, Any]:
    return {**value, "object_sha256": digest(value)}


def verify_closed(value: Any, label: str) -> None:
    need(type(value) is dict, label + " object")
    claimed = value.get("object_sha256")
    need(type(claimed) is str and len(claimed) == 64, label + " claimed hash")
    body = {key: item for key, item in value.items() if key != "object_sha256"}
    need(digest(body) == claimed, label + " self hash")


def find_step_by_sha(tree: dict[str, Any], sha256: str) -> dict[str, Any]:
    matches = [row["step"] for row in tree["leaves"]
               if row["step"].get("object_sha256") == sha256]
    need(len(matches) == 1, "unique step:" + sha256)
    return matches[0]


def verify_candidate_table(step: dict[str, Any], label: str) -> None:
    table = step["full_candidate_table"]
    need(type(table) is dict, label + " candidate table")
    rows = table["candidate_rows"]
    need(type(rows) is list and len(rows) == table["candidate_count"],
         label + " candidate count")
    need([row["candidate_id"] for row in rows]
         == table["candidate_ids_in_frozen_order"],
         label + " frozen candidate order")
    need(digest(rows) == table["candidate_rows_sha256"],
         label + " candidate table hash")
    need(table["strict_unique_owner"] is True
         and table["selected_owner"] == step["exact_owner"]["selected_target_id"],
         label + " selected owner binding")
    need(table["selected_discriminant"] == step["discriminant"]
         and table["root_order"] == step["root_order"],
         label + " discriminant/root order binding")


def verify_pending_step(step: dict[str, Any], collision: int, label: str) -> None:
    verify_closed(step, label)
    need(step["collision_index"] == collision
         and step["collision_index_derivation"] == "len(owner_history)+1"
         and len(step["owner_history"]) + 1 == collision,
         label + " collision index derivation")
    need(all(step.get(key) is not None for key in REQUIRED_STEP_FIELDS),
         label + " exact evidence fields")
    verify_candidate_table(step, label)
    decision = step["structured_terminal_decision_margin"]
    margin = decision["local_strict_decision_margin"]
    need(step["status"] == decision["status"] == "PENDING_GLOBAL_ORACLE",
         label + " pending status")
    need(decision["global_oracle_available"] is False
         and decision["missing_global_oracles"]
         == list(producer.MISSING_GLOBAL_ORACLES),
         label + " exact missing oracle set")
    need(decision["terminal_class_issued"] is None
         and decision["terminal_credit"] == decision["formal_credit"] == 0
         and step["formal_credit"] == step["D02_credit"] == 0,
         label + " zero credit lock")
    need(Q(margin["strict_lower_bound"]) > 0,
         label + " positive structured terminal-decision margin")
    need(step["incidence"]["codimension_owner_status"]
         == "PENDING_GLOBAL_ORACLE", label + " incidence owner pending")


def verify_next_link(step: dict[str, Any], next_step: dict[str, Any], label: str) -> None:
    handoff = step["next_handoff"]
    appended = handoff["appended_history_row"]
    evidence_body = {
        key: value for key, value in step.items()
        if key not in {"next_handoff", "object_sha256"}
    }
    need(digest(evidence_body) == handoff["step_evidence_sha256"]
         == appended["evidence_sha256"], label + " evidence hash link")
    need(appended["collision_index"] == step["collision_index"]
         and appended["selected_owner"]
         == step["exact_owner"]["selected_target_id"],
         label + " appended owner row")
    need(next_step["owner_history"] == step["owner_history"] + [appended],
         label + " exact history continuation")


def verify_ast_purity() -> dict[str, Any]:
    source_path = Path(producer.__file__).absolute()
    source = source_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(source_path))
    parents = {
        child: parent
        for parent in ast.walk(tree)
        for child in ast.iter_child_nodes(parent)
    }
    mutating: list[str] = []
    advance_args = None
    collision_derivations = 0
    forbidden_collision_branches: list[int] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name == "advance_one_collision":
                advance_args = [arg.arg for arg in node.args.args]
        if isinstance(node, ast.Call):
            name = None
            if isinstance(node.func, ast.Attribute):
                name = node.func.attr
            elif isinstance(node.func, ast.Name):
                name = node.func.id
            if name in MUTATING_CALL_NAMES:
                ancestor: ast.AST | None = node
                while ancestor is not None and not isinstance(
                    ancestor, (ast.FunctionDef, ast.AsyncFunctionDef)
                ):
                    ancestor = parents.get(ancestor)
                # CLI serialization is the sole write and is outside the pure
                # kernel.  All proof functions remain mutation-free.
                if not (name == "write" and isinstance(ancestor, ast.FunctionDef)
                        and ancestor.name == "emit"):
                    mutating.append(name)
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            if (isinstance(node.left, ast.Call)
                    and isinstance(node.left.func, ast.Name)
                    and node.left.func.id == "len"
                    and isinstance(node.right, ast.Constant)
                    and node.right.value == 1):
                collision_derivations += 1
        if isinstance(node, ast.If):
            constants = [child.value for child in ast.walk(node.test)
                         if isinstance(child, ast.Constant)
                         and type(child.value) is int]
            if any(value in {3, 4, 5} for value in constants):
                names = [child.id for child in ast.walk(node.test)
                         if isinstance(child, ast.Name)]
                if "collision_index" in names:
                    forbidden_collision_branches.extend(constants)
    need(advance_args == ["original_box", "owner_history"],
         "exact public pure-kernel signature")
    need(not mutating, "no mutating call APIs in producer AST")
    need(collision_derivations >= 2, "history-length collision derivation present")
    need(not forbidden_collision_branches, "no collision-index special branches")
    return {
        "advance_one_collision_positional_args": advance_args,
        "mutating_call_names": mutating,
        "history_length_plus_one_AST_witness_count": collision_derivations,
        "collision_index_3_4_5_special_branches": forbidden_collision_branches,
    }


def audit() -> dict[str, Any]:
    need(file_sha(Path(producer.__file__).absolute()) == PRODUCER_SHA256,
         "producer source pin")
    ast_audit = verify_ast_purity()
    first = producer.build_regression()
    second = producer.build_regression()
    need(canonical(first) == canonical(second), "byte-identical second replay")
    verify_closed(first, "regression")
    need(first["object_sha256"] == EXPECTED_REGRESSION_SHA256,
         "regression result pin")
    need(first["queue_pins"] == producer.QUEUE_PINS,
         "exact frozen queue pins")
    need(first["canonical_side_order"] == list(producer.SIDE_ORDER),
         "canonical side order")
    need(len(first["collision3_both_physical_sides"]) == 2,
         "both collision3 physical sides")
    for side in first["collision3_both_physical_sides"]:
        need(side["exact_match"] is True
             and side["observed_census"] == producer.EXPECTED_C44_SIDE_CENSUS,
             "exact collision3 C44 census:" + side["side"])
        verify_closed(side["adaptive_result"], "collision3 tree:" + side["side"])
    need(first["selected_collision3_live_leaf"]["step_object_sha256"]
         == EXPECTED_COLLISION3_STEP_SHA256, "collision3 step pin")
    need(first["selected_collision4_live_child"]["step_object_sha256"]
         == EXPECTED_COLLISION4_STEP_SHA256, "collision4 step pin")
    tree4 = first["collision4_adaptive_result"]
    verify_closed(tree4, "collision4 adaptive tree")
    need(tree4["object_sha256"] == EXPECTED_COLLISION4_TREE_SHA256
         and tree4["collision_index"] == 4
         and tree4["node_count"] == 233
         and tree4["split_count"] == 116
         and tree4["leaf_count"] == 117
         and tree4["relative_Kraft_sum"] == "1"
         and tree4["leaf_status_census"] == {
             "BOUNDED_PILOT_UNRESOLVED_WITH_EXACT_NEXT_DECISION": 56,
             "PASS_STRICT_COLLISION4_LIVE_TO_COLLISION5_ZERO_CREDIT": 61,
         }, "collision4 adaptive census pin")
    step3 = find_step_by_sha(
        first["collision3_both_physical_sides"][0]["adaptive_result"],
        EXPECTED_COLLISION3_STEP_SHA256,
    )
    step4 = find_step_by_sha(tree4, EXPECTED_COLLISION4_STEP_SHA256)
    step5 = first["collision5_first_live_child_step"]
    need(step5["object_sha256"] == EXPECTED_COLLISION5_STEP_SHA256,
         "collision5 step pin")
    verify_pending_step(step3, 3, "collision3")
    verify_pending_step(step4, 4, "collision4")
    verify_pending_step(step5, 5, "collision5")
    verify_next_link(step3, step4, "collision3-to-4")
    verify_next_link(step4, step5, "collision4-to-5")
    need(step4["structured_terminal_decision_margin"]
         ["local_strict_decision_margin"]["strict_lower_bound"] == "1/4"
         and step5["structured_terminal_decision_margin"]
         ["local_strict_decision_margin"]["strict_lower_bound"] == "1/4",
         "collision4 and collision5 positive margin pins")
    need(step4["full_candidate_table"]["candidate_count"] == 55
         and step5["full_candidate_table"]["candidate_count"] == 57,
         "collision4 and collision5 full candidate census")
    need(first["authority_pointer_touched"] is False
         and first["canonical_status_touched"] is False
         and first["writes_performed"] is False,
         "nonmutation claims")
    return close_object({
        "schema": SCHEMA,
        "status": "PASS_INDEPENDENT_REPLAY_AND_FAIL_CLOSED_AUDIT",
        "auditor_source_sha256": file_sha(SELF),
        "producer_source_sha256": PRODUCER_SHA256,
        "regression_object_sha256": EXPECTED_REGRESSION_SHA256,
        "second_replay_byte_identical": True,
        "AST_purity_audit": ast_audit,
        "pair9_collision3_both_sides_exact_C44_census": True,
        "collision_indices_replayed": [3, 4, 5],
        "collision3_step_sha256": EXPECTED_COLLISION3_STEP_SHA256,
        "collision4_tree_sha256": EXPECTED_COLLISION4_TREE_SHA256,
        "collision4_step_sha256": EXPECTED_COLLISION4_STEP_SHA256,
        "collision5_step_sha256": EXPECTED_COLLISION5_STEP_SHA256,
        "collision4_structured_margin_strict_lower_bound": "1/4",
        "collision5_structured_margin_strict_lower_bound": "1/4",
        "global_oracle_status": "PENDING_GLOBAL_ORACLE",
        "formal_credit": 0,
        "D02_credit": 0,
        "authority_pointer_touched": False,
        "canonical_status_touched": False,
        "writes_performed": False,
    })


def emit(value: dict[str, Any]) -> None:
    sys.stdout.buffer.write(canonical(value) + b"\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", action="store_true", required=True)
    parser.parse_args()
    try:
        emit(audit())
        return 0
    except (Rejected, RuntimeError, ValueError, KeyError, AssertionError) as exc:
        emit(close_object({
            "schema": SCHEMA + ".rejection",
            "status": "REJECTED_FAIL_CLOSED",
            "reason": str(exc),
            "formal_credit": 0,
            "writes_performed": False,
        }))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
