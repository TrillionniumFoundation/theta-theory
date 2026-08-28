#!/usr/bin/env python3
"""Structural/byte-replay auditor for C49 authenticated kernel v3.

This auditor deliberately imports the frozen producer.  It independently
checks serialization hashes, recursive evidence/handoff structure, exact
dyadic box refinement, candidate-table bindings, AST purity properties, the
executed negative-attack result, and a second deterministic producer replay.
It is NOT a no-producer-import numeric implementation and is NOT the D02-C
independent implementation required for promotion.
"""

from __future__ import annotations

import argparse
import ast
import copy
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

import cm2_round306c49_d02b_pure_advance_one_collision_v3 as producer


SCHEMA = "cm2.round306c49.d02-b-pure-advance-one-collision-structural-replay-audit.v3"
PRODUCER_SHA256 = "2f603c17f634ac1d5dca9763235f41e7a0259e0b384daa7d7c95cea63704a705"
REGRESSION_SHA256 = "eeb5e1cc3c25f23f6701348400b611a94a48095789c6ca76c95038bef40bbcfc"
SELF_TEST_SHA256 = "3410953c101dca1c615ef52189c65f6209a979db23ce4666c1b952a28bd4850c"
C3_STEP_SHA256 = "d28a82c071af1cb320b666ddd7b7fba4526e4368aa6cb13947dea5afd856a526"
C4_STEP_SHA256 = "65477f591f021368091964ba4a3105d24f77cc1da53f141142befd94110f2906"
C5_STEP_SHA256 = "53eda4b79e050c9de1e5a90e2146cf8c149802daec187b41eb45283f619f854e"
C4_TREE_SHA256 = "3243b49587d20303b7b2e42a892aef6b0b96a9a92a4ce3e0f4d2aa8fb66526ff"
C3_TREE_SHA256 = {
    "REFLECTED": "db39c8173aaad00558c525ebe64bef15407caf8b6522e9b77595d37d6ae8d02f",
    "REPRESENTATIVE": "308d51793a9e1770a9adfdcb909f00f077c6cdc96bd09abda204ce51c1483231",
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
    answer = copy.deepcopy(value)
    answer["object_sha256"] = digest(answer)
    return answer


def verify_closed(value: Any, label: str) -> None:
    need(type(value) is dict and type(value.get("object_sha256")) is str,
         label + " closed object")
    body = copy.deepcopy(value)
    claimed = body.pop("object_sha256")
    need(digest(body) == claimed, label + " self hash")


def power_two_exponent(value: Q) -> int | None:
    if value <= 0 or value.denominator != 1:
        return None
    integer = value.numerator
    return integer.bit_length() - 1 if not integer & (integer - 1) else None


def axis_bits(parent: list[str], child: list[str], label: str) -> str:
    p0, p1, c0, c1 = Q(parent[0]), Q(parent[1]), Q(child[0]), Q(child[1])
    need(p0 <= c0 <= c1 <= p1, label + " nesting")
    if p0 == p1:
        need(c0 == c1 == p0, label + " point")
        return ""
    width = c1 - c0
    need(width > 0, label + " positive width")
    exponent = power_two_exponent((p1 - p0) / width)
    need(exponent is not None, label + " power-two ratio")
    index = (c0 - p0) / width
    need(index.denominator == 1 and 0 <= index.numerator < 2**exponent,
         label + " dyadic index")
    return format(index.numerator, f"0{exponent}b") if exponent else ""


def shuffled(sequence: str, left: str, right: str) -> bool:
    states = {(0, 0)}
    for token in sequence:
        following = set()
        for i, j in states:
            if i < len(left) and left[i] == token:
                following.add((i + 1, j))
            if j < len(right) and right[j] == token:
                following.add((i, j + 1))
        states = following
    return (len(left), len(right)) in states


def verify_refinement(original: dict[str, Any], label: str) -> None:
    parent = original["refinement_parent_box"]
    child = original["closed_box"]
    extension = original["refinement_path_extension"]
    need(original["adaptive_suffix"]
         == original["refinement_parent_adaptive_suffix"] + extension,
         label + " suffix chain")
    t_bits = axis_bits(parent["t"], child["t"], label + " t")
    p_bits = axis_bits(parent["p"], child["p"], label + " p")
    need(shuffled(extension, t_bits, p_bits)
         and len(extension) == len(t_bits) + len(p_bits),
         label + " exact refinement shuffle")
    need(parent["s"] == child["s"], label + " s continuity")


def evidence_body(step: dict[str, Any]) -> dict[str, Any]:
    return {
        key: copy.deepcopy(value)
        for key, value in step.items()
        if key not in {"object_sha256", "step_evidence_sha256", "next_handoff"}
    }


def verify_candidate(step: dict[str, Any], label: str) -> None:
    table = step["full_candidate_table"]
    rows = table["candidate_rows"]
    need(len(rows) == table["candidate_count"], label + " candidate count")
    need([row["candidate_id"] for row in rows]
         == table["candidate_ids_in_frozen_order"],
         label + " candidate order")
    need(digest(rows) == table["candidate_rows_sha256"],
         label + " candidate hash")
    need(table["strict_unique_owner"] is True
         and table["selected_owner"]
         == step["exact_owner"]["selected_target_id"],
         label + " unique owner")
    need(table["selected_discriminant"] == step["discriminant"]
         and table["root_order"] == step["root_order"]
         and step["root_order"]["strict"] is True,
         label + " root-order/discriminant binding")


def verify_step(step: dict[str, Any], collision: int, label: str) -> None:
    verify_closed(step, label)
    need(step["schema"] == producer.STEP_SCHEMA
         and step["collision_index"] == len(step["owner_history"]) + 1 == collision,
         label + " schema/history index")
    need(step["step_evidence_sha256"] == digest(evidence_body(step)),
         label + " evidence hash")
    verify_candidate(step, label)
    verify_refinement(step["original_box"], label)
    decision = step["structured_terminal_decision_margin"]
    need(step["status"] == decision["status"] == "PENDING_GLOBAL_ORACLE"
         and decision["missing_global_oracles"]
         == list(producer.MISSING_GLOBAL_ORACLES)
         and step["formal_credit"] == step["D02_credit"] == 0,
         label + " pending/zero credit")
    handoff = step["next_handoff"]
    identity = producer.handoff_identity(step, step["step_evidence_sha256"])
    need({key: handoff[key] for key in identity} == identity
         and handoff["handoff_id"]
         == "c49v3-next-collision:" + digest(identity),
         label + " handoff")


def find_step(tree: dict[str, Any], sha256: str, label: str) -> dict[str, Any]:
    matches = [row["step"] for row in tree["leaves"]
               if row["step"].get("object_sha256") == sha256]
    need(len(matches) == 1, label + " unique")
    return matches[0]


def verify_recursive_chain(step3: dict[str, Any], step4: dict[str, Any],
                           step5: dict[str, Any]) -> None:
    for step, expected_length, label in (
        (step3, 2, "c3"), (step4, 3, "c4"), (step5, 4, "c5")
    ):
        need(len(step["owner_history"]) == expected_length,
             label + " recursive history length")
        for index, row in enumerate(step["owner_history"], 1):
            need(row["collision_index"] == index
                 and type(row["evidence_preimage"]) is dict,
                 label + " full history preimage")
            verify_closed(row["evidence_preimage"],
                          label + f" history preimage {index}")
    row3 = step4["owner_history"][2]
    need(row3["evidence_preimage"] == step3
         and row3["evidence_sha256"] == step3["step_evidence_sha256"]
         and row3["selected_owner"] == step3["exact_owner"]["selected_target_id"],
         "collision3 full preimage append")
    row4 = step5["owner_history"][3]
    need(row4["evidence_preimage"] == step4
         and row4["evidence_sha256"] == step4["step_evidence_sha256"]
         and row4["selected_owner"] == step4["exact_owner"]["selected_target_id"],
         "collision4 full preimage append")
    need(step4["original_box"]["parent_handoff_id"]
         == step3["next_handoff"]["handoff_id"]
         and step5["original_box"]["parent_handoff_id"]
         == step4["next_handoff"]["handoff_id"],
         "previous-to-next handoff chain")
    need(step4["original_box"]["refinement_parent_box"]
         == step3["original_box"]["closed_box"]
         and step5["original_box"]["refinement_parent_box"]
         == step4["original_box"]["closed_box"],
         "previous-to-next box geometry")
    need(step4["original_box"]["occurrence_id"]
         == step3["original_box"]["occurrence_id"]
         == step5["original_box"]["occurrence_id"],
         "occurrence continuity")


def ast_audit() -> dict[str, Any]:
    source = Path(producer.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    functions = {
        node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)
    }
    public = functions["advance_one_collision"]
    args = [arg.arg for arg in public.args.args]
    public_text = ast.get_source_segment(source, public) or ""
    runtime_names = {
        "advance_one_collision", "authenticated_numeric_step", "numeric_step",
        "local_numeric_context", "seal_step", "close_object",
    }
    global_statements = []
    forbidden_cache_calls = []
    mutation_assignments = []
    for name in runtime_names:
        node = functions[name]
        for child in ast.walk(node):
            if isinstance(child, ast.Global):
                global_statements.extend(child.names)
            if isinstance(child, ast.Call):
                called = None
                if isinstance(child.func, ast.Attribute):
                    called = child.func.attr
                elif isinstance(child.func, ast.Name):
                    called = child.func.id
                if called in {"immutable_registry_context", "immutable_cores"}:
                    forbidden_cache_calls.append(called)
            if isinstance(child, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
                targets = []
                if isinstance(child, ast.Assign):
                    targets = child.targets
                else:
                    targets = [child.target]
                if any(isinstance(target, ast.Attribute) for target in targets):
                    mutation_assignments.append(name)
    need(args == ["original_box", "owner_history"], "public signature")
    need("copy.deepcopy(original_box)" in public_text
         and "copy.deepcopy(owner_history)" in public_text,
         "public deep-copy ownership transfer")
    need(not global_statements and not forbidden_cache_calls
         and not mutation_assignments, "runtime global/cache purity AST")
    return {
        "public_args": args,
        "public_deep_copies_both_inputs": True,
        "runtime_global_statements": global_statements,
        "runtime_forbidden_cache_calls": forbidden_cache_calls,
        "runtime_attribute_mutation_assignments": mutation_assignments,
    }


def audit() -> dict[str, Any]:
    need(file_sha(Path(producer.__file__)) == PRODUCER_SHA256,
         "producer source pin")
    structure = ast_audit()
    attacks = producer.self_test()
    verify_closed(attacks, "executed adversarial self-test")
    need(attacks["object_sha256"] == SELF_TEST_SHA256
         and attacks["status"] == "PASS_10_OF_10_EXECUTED_ADVERSARIAL_TESTS"
         and all(attacks["attacks"].values()), "10 executed attacks")
    first = producer.build_regression()
    second = producer.build_regression()
    verify_closed(first, "regression")
    need(first["object_sha256"] == second["object_sha256"] == REGRESSION_SHA256
         and canonical(first) == canonical(second),
         "cold second regression byte replay")
    need(first["source_binding_pins"] == producer.PAIR9_SOURCE_BINDING_PINS,
         "source-binding preimage pins")
    for side in first["collision3_both_physical_sides"]:
        tree = side["adaptive_result"]
        verify_closed(tree, "collision3 tree:" + side["side"])
        need(tree["object_sha256"] == C3_TREE_SHA256[side["side"]]
             and side["observed_census"] == producer.EXPECTED_C44_SIDE_CENSUS,
             "collision3 tree/census:" + side["side"])
    tree3 = first["collision3_both_physical_sides"][0]["adaptive_result"]
    tree4 = first["collision4_adaptive_result"]
    verify_closed(tree4, "collision4 tree")
    need(tree4["object_sha256"] == C4_TREE_SHA256
         and tree4["node_count"] == 233
         and tree4["split_count"] == 116
         and tree4["leaf_count"] == 117
         and tree4["leaf_status_census"] == {
             "BOUNDED_PILOT_UNRESOLVED_WITH_EXACT_NEXT_DECISION": 56,
             "PASS_STRICT_COLLISION4_LIVE_TO_COLLISION5_ZERO_CREDIT": 61,
         }, "collision4 tree census")
    step3 = find_step(tree3, C3_STEP_SHA256, "collision3 step")
    step4 = find_step(tree4, C4_STEP_SHA256, "collision4 step")
    step5 = first["collision5_first_live_child_step"]
    need(step5["object_sha256"] == C5_STEP_SHA256, "collision5 step pin")
    verify_step(step3, 3, "collision3")
    verify_step(step4, 4, "collision4")
    verify_step(step5, 5, "collision5")
    verify_recursive_chain(step3, step4, step5)
    need(step4["structured_terminal_decision_margin"]
         ["local_strict_decision_margin"]["strict_lower_bound"] == "1/4"
         and step5["structured_terminal_decision_margin"]
         ["local_strict_decision_margin"]["strict_lower_bound"] == "1/4",
         "collision4/5 margin pins")
    need(first["formal_credit"] == first["D02_credit"] == 0
         and first["global_state_cache_writes"] == 0
         and first["missing_global_oracles"]
         == list(producer.MISSING_GLOBAL_ORACLES),
         "regression zero-credit/oracle locks")
    return close_object({
        "schema": SCHEMA,
        "status": "PASS_STRUCTURAL_AND_BYTE_REPLAY_AUDIT_ZERO_CREDIT",
        "audit_scope": (
            "STRUCTURAL_AND_PRODUCER_BYTE_REPLAY_ONLY_NOT_AN_INDEPENDENT_"
            "NUMERIC_IMPLEMENTATION_NOT_D02_C"
        ),
        "auditor_imports_producer": True,
        "auditor_source_sha256": file_sha(SELF),
        "producer_source_sha256": PRODUCER_SHA256,
        "producer_AST_audit": structure,
        "executed_adversarial_self_test_sha256": SELF_TEST_SHA256,
        "regression_object_sha256": REGRESSION_SHA256,
        "second_regression_byte_identical": True,
        "collision_indices_replayed": [3, 4, 5],
        "recursive_full_history_preimages_verified": True,
        "source_binding_preimages_verified": True,
        "previous_next_box_suffix_occurrence_handoff_chain_verified": True,
        "global_oracle_status": "PENDING_GLOBAL_ORACLE",
        "missing_global_oracles": list(producer.MISSING_GLOBAL_ORACLES),
        "formal_credit": 0,
        "D02_credit": 0,
        "D02_C_independent_implementation": False,
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
    except (Rejected, producer.Rejected, RuntimeError, ValueError, KeyError,
            AssertionError) as exc:
        emit(close_object({
            "schema": SCHEMA + ".rejection",
            "status": "REJECTED_FAIL_CLOSED",
            "reason": str(exc),
            "formal_credit": 0,
            "D02_credit": 0,
            "writes_performed": False,
        }))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
