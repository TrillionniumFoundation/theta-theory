#!/usr/bin/env python3
"""Numeric-replay-authenticated D02-B one-collision kernel, v4.

V3 authenticated internally consistent, self-hashed history objects, but an
attacker could coherently edit and re-sign numeric evidence.  V4 treats hashes
only as integrity commitments.  Authenticity comes from independently
recomputing every prior non-genesis numeric step with a fresh local numeric
context and requiring its entire evidence body to match byte-for-byte.

Adaptive refinement is also authenticated numerically.  Every split carries a
closed decision preimage, and validation recomputes the unresolved parent step,
the sensitivity-selected axis/coordinate, and the chosen child.  Arbitrary
dyadic descendants are no longer accepted merely because their suffix can be
interpreted as a t/p shuffle.

Inputs and outputs cross deep-copy boundaries.  Numeric contexts are local;
no module/global cache is read or written.  Both missing global oracles remain
hard pending and every result has zero formal/D02 credit.
"""

from __future__ import annotations

import argparse
from collections import Counter
import copy
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys
from typing import Any, Callable

from flint import ctx
import flint


sys.dont_write_bytecode = True
SELF = Path(__file__).absolute()
DELIVERABLES = SELF.parent
if str(DELIVERABLES) not in sys.path:
    sys.path.insert(0, str(DELIVERABLES))

import cm2_round306c49_d02b_pure_advance_one_collision_v3 as v3
import cm2_round306c49_d02b_pure_advance_one_collision_v2 as v2


SCHEMA = "cm2.round306c49.d02-b-pure-advance-one-collision.v4"
ORIGINAL_BOX_SCHEMA = SCHEMA + ".original-box"
GENESIS_SCHEMA = SCHEMA + ".genesis-collision-evidence"
STEP_SCHEMA = SCHEMA + ".step"
HANDOFF_SCHEMA = SCHEMA + ".next-handoff"
SPLIT_SCHEMA = SCHEMA + ".adaptive-split-decision-preimage"
V3_SOURCE_SHA256 = "2f603c17f634ac1d5dca9763235f41e7a0259e0b384daa7d7c95cea63704a705"
V2_SOURCE_SHA256 = "25d87f0ae27b7946ab9f55dbe8a5f50c353eb9f05dd4a6e50810d92e438700df"

SOURCE_CHART_ID = v3.SOURCE_CHART_ID
COLLISION1_OWNER = v3.COLLISION1_OWNER
PAIR_INDEX = v3.PAIR_INDEX
PAIR9_PATH = v3.PAIR9_PATH
SIDE_ORDER = v3.SIDE_ORDER
QUEUE_PINS = v3.QUEUE_PINS
SOURCE_BINDING_PINS = v3.PAIR9_SOURCE_BINDING_PINS
EXPECTED_C44_SIDE_CENSUS = v3.EXPECTED_C44_SIDE_CENSUS
MISSING_GLOBAL_ORACLES = v3.MISSING_GLOBAL_ORACLES
HEX64 = v3.HEX64


class Rejected(RuntimeError):
    """Authentication or numeric replay rejection."""


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
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def verify_numeric_authority_pins() -> None:
    need(flint.__version__ == "0.9.0" and ctx.prec == 384,
         "v4 Arb runtime pin")
    need(file_sha(Path(v3.__file__).absolute()) == V3_SOURCE_SHA256,
         "frozen v3 numeric authority source")
    need(file_sha(Path(v2.__file__).absolute()) == V2_SOURCE_SHA256,
         "frozen v2 primitive source")


def close_object(value: dict[str, Any]) -> dict[str, Any]:
    answer = copy.deepcopy(value)
    need("object_sha256" not in answer, "hash absent before close")
    answer["object_sha256"] = digest(answer)
    return answer


def verify_closed(value: Any, label: str) -> None:
    need(type(value) is dict and type(value.get("object_sha256")) is str
         and HEX64.fullmatch(value["object_sha256"]) is not None,
         label + " closed object")
    body = copy.deepcopy(value)
    claimed = body.pop("object_sha256")
    need(digest(body) == claimed, label + " self hash")


def validate_original_structure(value: Any) -> None:
    expected = {
        "schema", "occurrence_id", "side", "source_chart_id", "closed_box",
        "adaptive_suffix", "source_binding_sha256", "source_binding_preimage",
        "parent_handoff_id", "refinement_parent_box",
        "refinement_parent_adaptive_suffix", "refinement_decision_chain",
    }
    need(type(value) is dict and set(value) == expected,
         "v4 original exact keys")
    need(value["schema"] == ORIGINAL_BOX_SCHEMA, "v4 original schema")
    need(type(value["occurrence_id"]) is str and value["occurrence_id"] != ""
         and value["side"] in SIDE_ORDER
         and value["source_chart_id"] == SOURCE_CHART_ID,
         "v4 occurrence/side/chart")
    need(type(value["parent_handoff_id"]) is str
         and value["parent_handoff_id"] != "", "v4 parent handoff")
    need(type(value["adaptive_suffix"]) is str
         and set(value["adaptive_suffix"]) <= {"0", "1"}, "v4 suffix")
    need(type(value["refinement_parent_adaptive_suffix"]) is str
         and set(value["refinement_parent_adaptive_suffix"]) <= {"0", "1"},
         "v4 parent suffix")
    need(type(value["refinement_decision_chain"]) is list,
         "v4 decision chain list")
    v3.verify_source_binding(value["source_binding_preimage"])
    source = value["source_binding_preimage"]
    need(value["source_binding_sha256"] == source["object_sha256"]
         and source["object_sha256"] == SOURCE_BINDING_PINS[value["side"]]
         and value["occurrence_id"] == source["C45_handoff_id"]
         and value["side"] == source["side"],
         "v4 source preimage authority binding")
    v3.validate_box(value["closed_box"], "v4 closed box")
    v3.validate_box(value["refinement_parent_box"], "v4 refinement parent box")


def genesis_history(original_box: dict[str, Any]) -> list[dict[str, Any]]:
    source = original_box["source_binding_preimage"]
    first_handoff_identity = {
        "schema": SCHEMA + ".genesis-collision1-to-2-handoff",
        "source_binding_sha256": source["object_sha256"],
        "occurrence_id": original_box["occurrence_id"],
        "collision_index": 2,
    }
    first_handoff = "c49v4-genesis-collision2:" + digest(first_handoff_identity)
    evidence1 = close_object({
        "schema": GENESIS_SCHEMA,
        "kind": "FROZEN_COLLISION1_OWNER_AUTHORITY",
        "collision_index": 1,
        "selected_owner": COLLISION1_OWNER,
        "source_binding_sha256": source["object_sha256"],
        "occurrence_id": original_box["occurrence_id"],
        "closed_source_box": copy.deepcopy(source["closed_source_box"]),
        "adaptive_suffix": "",
        "previous_evidence_sha256": None,
        "previous_handoff_id": None,
        "next_handoff_id": first_handoff,
        "formal_credit": 0,
    })
    evidence2 = close_object({
        "schema": GENESIS_SCHEMA,
        "kind": "C45_COLLISION2_OCCURRENCE_OWNER_BINDING",
        "collision_index": 2,
        "selected_owner": source["incoming_collision2_owner"],
        "source_binding_sha256": source["object_sha256"],
        "occurrence_id": original_box["occurrence_id"],
        "closed_source_box": copy.deepcopy(source["closed_source_box"]),
        "adaptive_suffix": "",
        "previous_evidence_sha256": evidence1["object_sha256"],
        "previous_handoff_id": first_handoff,
        "next_handoff_id": source["C45_handoff_id"],
        "C45_occurrence_owner_binding": copy.deepcopy(
            source["C45_occurrence_owner_binding"]
        ),
        "formal_credit": 0,
    })
    return [
        {
            "collision_index": 1,
            "selected_owner": COLLISION1_OWNER,
            "evidence_sha256": evidence1["object_sha256"],
            "evidence_preimage": evidence1,
        },
        {
            "collision_index": 2,
            "selected_owner": source["incoming_collision2_owner"],
            "evidence_sha256": evidence2["object_sha256"],
            "evidence_preimage": evidence2,
        },
    ]


def step_evidence_body(step: dict[str, Any]) -> dict[str, Any]:
    return {
        key: copy.deepcopy(value)
        for key, value in step.items()
        if key not in {"object_sha256", "step_evidence_sha256", "next_handoff"}
    }


def handoff_identity(step: dict[str, Any], evidence_sha256: str) -> dict[str, Any]:
    return {
        "schema": HANDOFF_SCHEMA,
        "step_evidence_sha256": evidence_sha256,
        "completed_collision_index": step["collision_index"],
        "next_collision_index": step["collision_index"] + 1,
        "occurrence_id": step["original_box"]["occurrence_id"],
        "output_original_box_sha256": digest(step["original_box"]),
        "output_closed_box": copy.deepcopy(step["original_box"]["closed_box"]),
        "output_adaptive_suffix": step["original_box"]["adaptive_suffix"],
        "selected_owner": step["exact_owner"]["selected_target_id"],
        "formal_credit": 0,
    }


def build_next_handoff(step: dict[str, Any], evidence_sha256: str) -> dict[str, Any]:
    identity = handoff_identity(step, evidence_sha256)
    return {
        **identity,
        "handoff_id": "c49v4-next-collision:" + digest(identity),
        "appended_history_row": {
            "collision_index": step["collision_index"],
            "selected_owner": step["exact_owner"]["selected_target_id"],
            "evidence_sha256": evidence_sha256,
        },
    }


def seal_step(value: dict[str, Any]) -> dict[str, Any]:
    step = copy.deepcopy(value)
    step["step_evidence_sha256"] = digest(step_evidence_body(step))
    decision = step.get("structured_terminal_decision_margin") or {}
    if (step.get("status") == "PENDING_GLOBAL_ORACLE"
            and decision.get("local_disposition") == "LIVE_CONTINUE"):
        step["next_handoff"] = build_next_handoff(
            step, step["step_evidence_sha256"]
        )
    else:
        step["next_handoff"] = None
    return close_object(step)


def local_numeric_context() -> dict[str, Any]:
    """Fresh, call-local context.  No cache helper or global assignment."""

    return v3.local_numeric_context()


def numeric_step(
    original_box: dict[str, Any], owner_history: list[dict[str, Any]],
    numeric_context: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    result, internal = v3.numeric_step(
        original_box, owner_history, numeric_context
    )
    result["schema"] = STEP_SCHEMA
    return result, internal


def numeric_projection(result: dict[str, Any]) -> dict[str, Any]:
    """Exact numeric evidence, excluding only authenticated input echoes."""

    return {
        key: copy.deepcopy(value)
        for key, value in result.items()
        if key not in {
            "original_box", "original_box_sha256",
            "owner_history", "owner_history_sha256",
        }
    }


def numeric_split_decision(
    original: dict[str, Any], history: list[dict[str, Any]],
    result: dict[str, Any], internal: dict[str, Any],
) -> dict[str, Any]:
    numeric_original, numeric_history = v3.simple_numeric_inputs(original, history)
    return v2.sensitivity_split(
        numeric_original, numeric_history, result, internal
    )


def split_preimage(
    parent_original: dict[str, Any], owner_history: list[dict[str, Any]],
    result: dict[str, Any], decision: dict[str, Any], child_bit: str,
    child_box: Any, ordinal: int,
) -> dict[str, Any]:
    need(child_bit in {"0", "1"}, "split child bit")
    return close_object({
        "schema": SPLIT_SCHEMA,
        "split_ordinal_zero_based": ordinal,
        "collision_index": len(owner_history) + 1,
        "source_binding_sha256": parent_original["source_binding_sha256"],
        "owner_history_sha256": digest(owner_history),
        "parent_handoff_id": parent_original["parent_handoff_id"],
        "parent_closed_box": copy.deepcopy(parent_original["closed_box"]),
        "parent_adaptive_suffix": parent_original["adaptive_suffix"],
        "numeric_evidence_projection": numeric_projection(result),
        "split_decision": copy.deepcopy(decision),
        "selected_child_bit": child_bit,
        "child_closed_box": v2.public_box(child_box),
        "child_adaptive_suffix": child_box.path,
        "formal_credit": 0,
        "D02_credit": 0,
    })


def original_at_chain_prefix(
    final_original: dict[str, Any], current_box: dict[str, Any],
    current_suffix: str, prefix: list[dict[str, Any]],
) -> dict[str, Any]:
    answer = copy.deepcopy(final_original)
    answer["closed_box"] = copy.deepcopy(current_box)
    answer["adaptive_suffix"] = current_suffix
    answer["refinement_decision_chain"] = copy.deepcopy(prefix)
    return answer


def verify_split_chain(
    original: dict[str, Any], owner_history: list[dict[str, Any]],
    label: str,
) -> None:
    current_box = copy.deepcopy(original["refinement_parent_box"])
    current_suffix = original["refinement_parent_adaptive_suffix"]
    chain = original["refinement_decision_chain"]
    context = local_numeric_context()
    prefix: list[dict[str, Any]] = []
    for ordinal, row in enumerate(chain):
        verify_closed(row, label + f" split {ordinal}")
        expected_keys = {
            "schema", "split_ordinal_zero_based", "collision_index",
            "source_binding_sha256", "owner_history_sha256",
            "parent_handoff_id", "parent_closed_box",
            "parent_adaptive_suffix", "numeric_evidence_projection",
            "split_decision", "selected_child_bit", "child_closed_box",
            "child_adaptive_suffix", "formal_credit", "D02_credit",
            "object_sha256",
        }
        need(set(row) == expected_keys and row["schema"] == SPLIT_SCHEMA,
             label + f" split {ordinal} exact schema/keys")
        need(row["split_ordinal_zero_based"] == ordinal
             and row["collision_index"] == len(owner_history) + 1
             and row["source_binding_sha256"] == original["source_binding_sha256"]
             and row["owner_history_sha256"] == digest(owner_history)
             and row["parent_handoff_id"] == original["parent_handoff_id"]
             and row["parent_closed_box"] == current_box
             and row["parent_adaptive_suffix"] == current_suffix
             and row["formal_credit"] == row["D02_credit"] == 0,
             label + f" split {ordinal} bindings")
        parent_original = original_at_chain_prefix(
            original, current_box, current_suffix, prefix
        )
        recomputed, internal = numeric_step(
            parent_original, owner_history, context
        )
        need(internal.get("local_complete") is not True,
             label + f" split {ordinal} parent must be unresolved")
        decision = numeric_split_decision(
            parent_original, owner_history, recomputed, internal
        )
        need(row["numeric_evidence_projection"] == numeric_projection(recomputed)
             and row["split_decision"] == decision,
             label + f" split {ordinal} exact numeric decision replay")
        numeric_original, _numeric_history = v3.simple_numeric_inputs(
            parent_original, owner_history
        )
        parent_atlas = v2.atlas_box(numeric_original)
        left, right, coordinate = v2.split_box(parent_atlas, decision["axis"])
        need(v2.qstr(coordinate) == decision["exact_rational_coordinate"],
             label + f" split {ordinal} coordinate")
        need(row["selected_child_bit"] in {"0", "1"},
             label + f" split {ordinal} selected child bit enum")
        child = left if row["selected_child_bit"] == "0" else right
        need(row["child_closed_box"] == v2.public_box(child)
             and row["child_adaptive_suffix"] == child.path,
             label + f" split {ordinal} exact selected child")
        current_box = copy.deepcopy(row["child_closed_box"])
        current_suffix = row["child_adaptive_suffix"]
        prefix.append(copy.deepcopy(row))
    need(current_box == original["closed_box"]
         and current_suffix == original["adaptive_suffix"],
         label + " split-chain terminal box/suffix")


def verify_candidate_binding(step: dict[str, Any], label: str) -> None:
    table = step.get("full_candidate_table")
    need(type(table) is dict and type(table.get("candidate_rows")) is list,
         label + " candidate table")
    rows = table["candidate_rows"]
    need(len(rows) == table.get("candidate_count")
         and [row["candidate_id"] for row in rows]
         == table.get("candidate_ids_in_frozen_order")
         and digest(rows) == table.get("candidate_rows_sha256"),
         label + " candidate count/order/hash")
    need(table.get("strict_unique_owner") is True
         and table.get("selected_owner")
         == step["exact_owner"]["selected_target_id"]
         and table.get("selected_discriminant") == step["discriminant"]
         and table.get("root_order") == step["root_order"]
         and step["root_order"].get("strict") is True,
         label + " owner/discriminant/root-order binding")


def verify_handoff(step: dict[str, Any], label: str) -> None:
    handoff = step.get("next_handoff")
    need(type(handoff) is dict, label + " live handoff")
    identity = handoff_identity(step, step["step_evidence_sha256"])
    need({key: handoff[key] for key in identity} == identity
         and handoff["handoff_id"]
         == "c49v4-next-collision:" + digest(identity)
         and handoff["appended_history_row"] == {
             "collision_index": step["collision_index"],
             "selected_owner": step["exact_owner"]["selected_target_id"],
             "evidence_sha256": step["step_evidence_sha256"],
         }, label + " exact handoff")


def verify_prior_step_numeric(
    preimage: dict[str, Any], row: dict[str, Any],
    prefix: list[dict[str, Any]], source_binding: dict[str, Any], label: str,
) -> None:
    verify_closed(preimage, label)
    need(preimage.get("schema") == STEP_SCHEMA
         and preimage.get("collision_index") == row["collision_index"]
         and preimage.get("owner_history") == prefix,
         label + " schema/index/recursive prefix")
    original = preimage.get("original_box")
    validate_original_structure(original)
    need(original["source_binding_preimage"] == source_binding,
         label + " source continuity")
    need(preimage.get("step_evidence_sha256") == row["evidence_sha256"]
         == digest(step_evidence_body(preimage)),
         label + " evidence digest")
    verify_candidate_binding(preimage, label)
    verify_handoff(preimage, label)
    need(preimage["exact_owner"]["selected_target_id"] == row["selected_owner"],
         label + " history-row owner")

    # Authenticity: use a fresh local context and recompute the entire body.
    fresh_context = local_numeric_context()
    recomputed, internal = numeric_step(original, prefix, fresh_context)
    need(internal.get("local_complete") is True,
         label + " prior live step recomputes complete")
    need(step_evidence_body(preimage) == recomputed,
         label + " COMPLETE NUMERIC EVIDENCE BODY BYTE REPLAY")


def validate_history_and_chain(
    original: dict[str, Any], owner_history: Any,
) -> None:
    need(type(owner_history) is list and len(owner_history) >= 2,
         "v4 authenticated history")
    row_keys = {
        "collision_index", "selected_owner", "evidence_sha256",
        "evidence_preimage",
    }
    for index, row in enumerate(owner_history, 1):
        need(type(row) is dict and set(row) == row_keys
             and row["collision_index"] == index
             and type(row["selected_owner"]) is str
             and type(row["evidence_sha256"]) is str
             and HEX64.fullmatch(row["evidence_sha256"]) is not None,
             "v4 history row exact/contiguous")
    genesis = genesis_history(original)
    need(owner_history[:2] == genesis, "v4 exact genesis preimages")
    source = original["source_binding_preimage"]
    expected_handoff = genesis[1]["evidence_preimage"]["next_handoff_id"]
    expected_parent_box = source["closed_source_box"]
    expected_parent_suffix = ""
    for offset, row in enumerate(owner_history[2:], 3):
        preimage = row["evidence_preimage"]
        verify_prior_step_numeric(
            preimage, row, owner_history[:offset - 1], source,
            f"v4 history collision {offset}",
        )
        prior_original = preimage["original_box"]
        need(prior_original["parent_handoff_id"] == expected_handoff
             and prior_original["refinement_parent_box"] == expected_parent_box
             and prior_original["refinement_parent_adaptive_suffix"]
             == expected_parent_suffix,
             f"v4 history collision {offset} previous chain")
        verify_split_chain(
            prior_original, owner_history[:offset - 1],
            f"v4 history collision {offset} refinement",
        )
        expected_handoff = preimage["next_handoff"]["handoff_id"]
        expected_parent_box = prior_original["closed_box"]
        expected_parent_suffix = prior_original["adaptive_suffix"]
    need(original["parent_handoff_id"] == expected_handoff
         and original["refinement_parent_box"] == expected_parent_box
         and original["refinement_parent_adaptive_suffix"]
         == expected_parent_suffix,
         "v4 current previous chain")
    verify_split_chain(original, owner_history, "v4 current refinement")


def authenticated_numeric_step(
    original: dict[str, Any], history: list[dict[str, Any]],
    context: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    validate_original_structure(original)
    validate_history_and_chain(original, history)
    return numeric_step(original, history, context)


def advance_one_collision(
    original_box: dict[str, Any], owner_history: list[dict[str, Any]],
) -> dict[str, Any]:
    """Public v4 kernel: authenticate by numeric replay, then advance once."""

    owned_box = copy.deepcopy(original_box)
    owned_history = copy.deepcopy(owner_history)
    verify_numeric_authority_pins()
    result, _internal = authenticated_numeric_step(
        owned_box, owned_history, local_numeric_context()
    )
    return seal_step(result)


def append_authenticated_history(
    history: list[dict[str, Any]], step: dict[str, Any],
) -> list[dict[str, Any]]:
    verify_closed(step, "v4 append step")
    verify_handoff(step, "v4 append step")
    return copy.deepcopy(history) + [{
        **copy.deepcopy(step["next_handoff"]["appended_history_row"]),
        "evidence_preimage": copy.deepcopy(step),
    }]


def next_stage_original(step: dict[str, Any]) -> dict[str, Any]:
    verify_handoff(step, "v4 next-stage step")
    prior = step["original_box"]
    return {
        **copy.deepcopy(prior),
        "parent_handoff_id": step["next_handoff"]["handoff_id"],
        "refinement_parent_box": copy.deepcopy(prior["closed_box"]),
        "refinement_parent_adaptive_suffix": prior["adaptive_suffix"],
        "refinement_decision_chain": [],
    }


def root_atlas_box(original: dict[str, Any]) -> Any:
    numeric_original, _history = v3.simple_numeric_inputs(original, [])
    return v2.atlas_box(numeric_original)


def child_original(
    root_original: dict[str, Any], child_box: Any,
    chain: list[dict[str, Any]],
) -> dict[str, Any]:
    answer = copy.deepcopy(root_original)
    answer["closed_box"] = v2.public_box(child_box)
    answer["adaptive_suffix"] = child_box.path
    answer["refinement_decision_chain"] = copy.deepcopy(chain)
    return answer


def adaptive_advance(
    original_box: dict[str, Any], owner_history: list[dict[str, Any]],
    maximum_additional_depth: int, maximum_nodes: int,
) -> dict[str, Any]:
    owned_box = copy.deepcopy(original_box)
    owned_history = copy.deepcopy(owner_history)
    verify_numeric_authority_pins()
    validate_original_structure(owned_box)
    validate_history_and_chain(owned_box, owned_history)
    need(type(maximum_additional_depth) is int and maximum_additional_depth >= 0
         and type(maximum_nodes) is int and maximum_nodes > 0,
         "v4 adaptive bounds")
    context = local_numeric_context()
    root = root_atlas_box(owned_box)
    root_depth = root.depth
    stack: list[tuple[Any, list[dict[str, Any]]]] = [
        (root, copy.deepcopy(owned_box["refinement_decision_chain"]))
    ]
    base_chain_length = len(owned_box["refinement_decision_chain"])
    leaves = []
    nodes = splits = 0
    while stack:
        box, chain = stack.pop()
        nodes += 1
        need(nodes <= maximum_nodes, "v4 adaptive node bound")
        current = child_original(owned_box, box, chain)
        result, internal = numeric_step(current, owned_history, context)
        if internal.get("local_complete") is True:
            step = seal_step(result)
            disposition = step["structured_terminal_decision_margin"]["local_disposition"]
            status = (
                "STRICT_EARLY_TERMINAL_KNOWN_COMPONENT"
                if disposition == "KNOWN_COMPONENT" else
                f"PASS_STRICT_COLLISION{step['collision_index']}_LIVE_TO_COLLISION"
                f"{step['collision_index'] + 1}_ZERO_CREDIT"
            )
            leaves.append({
                "adaptive_suffix": box.path,
                "relative_Kraft_fraction": v2.qstr(Q(
                    1, 2 ** (box.depth - root_depth)
                )),
                "regression_status": status,
                "step": step,
            })
            continue
        decision = numeric_split_decision(
            current, owned_history, result, internal
        )
        depth = box.depth - root_depth
        if depth >= maximum_additional_depth:
            bounded = copy.deepcopy(result)
            bounded["next_decision"] = decision
            leaves.append({
                "adaptive_suffix": box.path,
                "relative_Kraft_fraction": v2.qstr(Q(1, 2**depth)),
                "regression_status":
                    "BOUNDED_PILOT_UNRESOLVED_WITH_EXACT_NEXT_DECISION",
                "step": seal_step(bounded),
            })
            continue
        left, right, coordinate = v2.split_box(box, decision["axis"])
        need(v2.qstr(coordinate) == decision["exact_rational_coordinate"],
             "v4 adaptive coordinate")
        ordinal = len(chain) - base_chain_length
        left_row = split_preimage(
            current, owned_history, result, decision, "0", left, ordinal
        )
        right_row = split_preimage(
            current, owned_history, result, decision, "1", right, ordinal
        )
        splits += 1
        stack.append((right, chain + [right_row]))
        stack.append((left, chain + [left_row]))
    paths = sorted(row["adaptive_suffix"] for row in leaves)
    need(not any(right.startswith(left) for left, right in zip(paths, paths[1:])),
         "v4 adaptive prefix free")
    need(sum(Q(row["relative_Kraft_fraction"]) for row in leaves) == 1,
         "v4 adaptive Kraft")
    return close_object({
        "schema": SCHEMA + ".adaptive-one-collision",
        "collision_index": len(owned_history) + 1,
        "collision_index_derivation": "len(owner_history)+1",
        "original_box_sha256": digest(owned_box),
        "owner_history_sha256": digest(owned_history),
        "maximum_additional_depth": maximum_additional_depth,
        "maximum_nodes": maximum_nodes,
        "node_count": nodes,
        "split_count": splits,
        "leaf_count": len(leaves),
        "leaf_status_census": dict(sorted(Counter(
            row["regression_status"] for row in leaves
        ).items())),
        "adaptive_paths_prefix_free": True,
        "relative_Kraft_sum": "1",
        "leaves": leaves,
        "formal_credit": 0,
        "D02_credit": 0,
    })


def pair9_inputs() -> tuple[
    dict[str, Any], list[tuple[dict[str, Any], list[dict[str, Any]]]]
]:
    verify_numeric_authority_pins()
    source, v3_inputs = v3.pair9_source_inputs_unvalidated()
    inputs = []
    for old_original, _old_history in v3_inputs:
        original = {
            "schema": ORIGINAL_BOX_SCHEMA,
            "occurrence_id": old_original["occurrence_id"],
            "side": old_original["side"],
            "source_chart_id": old_original["source_chart_id"],
            "closed_box": copy.deepcopy(old_original["closed_box"]),
            "adaptive_suffix": "",
            "source_binding_sha256": old_original["source_binding_sha256"],
            "source_binding_preimage": copy.deepcopy(
                old_original["source_binding_preimage"]
            ),
            "parent_handoff_id": old_original["parent_handoff_id"],
            "refinement_parent_box": copy.deepcopy(
                old_original["refinement_parent_box"]
            ),
            "refinement_parent_adaptive_suffix": "",
            "refinement_decision_chain": [],
        }
        history = genesis_history(original)
        validate_original_structure(original)
        validate_history_and_chain(original, history)
        inputs.append((original, history))
    return source, inputs


def first_live_leaf(tree: dict[str, Any]) -> dict[str, Any]:
    rows = [row for row in tree["leaves"]
            if (row["step"].get("structured_terminal_decision_margin") or {}).get(
                "local_disposition"
            ) == "LIVE_CONTINUE"]
    need(len(rows) > 0, "v4 live leaf")
    return min(rows, key=lambda row: row["adaptive_suffix"])


def build_regression() -> dict[str, Any]:
    need(flint.__version__ == "0.9.0" and ctx.prec == 384,
         "v4 Arb runtime")
    source, inputs = pair9_inputs()
    collision3 = []
    for original, history in inputs:
        tree = adaptive_advance(original, history, 6, 1024)
        observed = {
            key: tree[key] for key in (
                "node_count", "split_count", "leaf_count",
                "relative_Kraft_sum", "leaf_status_census",
            )
        }
        need(observed == EXPECTED_C44_SIDE_CENSUS,
             "v4 exact C44 census:" + original["side"])
        collision3.append({
            "side": original["side"],
            "observed_census": observed,
            "expected_C44_census": copy.deepcopy(EXPECTED_C44_SIDE_CENSUS),
            "exact_match": True,
            "adaptive_result": tree,
        })
    first3 = first_live_leaf(collision3[0]["adaptive_result"])
    step3 = first3["step"]
    history4 = append_authenticated_history(inputs[0][1], step3)
    original4 = next_stage_original(step3)
    tree4 = adaptive_advance(original4, history4, 8, 4096)
    first4 = first_live_leaf(tree4)
    step4 = first4["step"]
    history5 = append_authenticated_history(history4, step4)
    original5 = next_stage_original(step4)
    step5 = advance_one_collision(original5, history5)
    need([step3["collision_index"], step4["collision_index"],
          step5["collision_index"]] == [3, 4, 5], "v4 collision indices")
    for label, step in (("collision3", step3), ("collision4", step4),
                        ("collision5", step5)):
        verify_closed(step, label)
        verify_candidate_binding(step, label)
        need(step["status"] == "PENDING_GLOBAL_ORACLE"
             and step["structured_terminal_decision_margin"]
             ["missing_global_oracles"] == list(MISSING_GLOBAL_ORACLES)
             and step["formal_credit"] == step["D02_credit"] == 0,
             label + " v4 pending zero credit")
    return close_object({
        "schema": SCHEMA + ".pair9-regression",
        "status": "PASS_NUMERIC_REPLAY_AUTHENTICATED_PAIR9_3_4_5_ZERO_CREDIT",
        "producer_source_sha256": file_sha(SELF),
        "v3_rejected_source_sha256": V3_SOURCE_SHA256,
        "v2_primitive_source_sha256": V2_SOURCE_SHA256,
        "queue_pins": copy.deepcopy(QUEUE_PINS),
        "source_binding_pins": copy.deepcopy(SOURCE_BINDING_PINS),
        "pair_index": PAIR_INDEX,
        "C41_path": PAIR9_PATH,
        "C41_row_sha256": source["row_sha256"],
        "collision3_both_physical_sides": collision3,
        "selected_collision3_live_leaf": {
            "side": inputs[0][0]["side"],
            "adaptive_suffix": first3["adaptive_suffix"],
            "step_object_sha256": step3["object_sha256"],
            "step_evidence_sha256": step3["step_evidence_sha256"],
            "selected_owner": step3["exact_owner"]["selected_target_id"],
        },
        "collision4_adaptive_result": tree4,
        "selected_collision4_live_child": {
            "adaptive_suffix": first4["adaptive_suffix"],
            "step_object_sha256": step4["object_sha256"],
            "step_evidence_sha256": step4["step_evidence_sha256"],
            "selected_owner": step4["exact_owner"]["selected_target_id"],
        },
        "collision5_first_live_child_step": step5,
        "collision_indices_observed": [3, 4, 5],
        "every_prior_step_full_numeric_body_replayed": True,
        "every_split_decision_preimage_replayed": True,
        "global_state_cache_writes": 0,
        "global_oracle_status": "PENDING_GLOBAL_ORACLE",
        "missing_global_oracles": list(MISSING_GLOBAL_ORACLES),
        "formal_credit": 0,
        "D02_credit": 0,
        "authority_pointer_touched": False,
        "canonical_status_touched": False,
        "writes_performed": False,
    })


def rejected_attack(action: Callable[[], Any]) -> bool:
    try:
        action()
    except (Rejected, v3.Rejected, v2.Rejected, RuntimeError, ValueError,
            KeyError, AssertionError):
        return bool(1)
    return bool(0)


def forge_live_step(
    step: dict[str, Any], mutator: Callable[[dict[str, Any]], None],
) -> dict[str, Any]:
    forged = copy.deepcopy(step)
    forged.pop("object_sha256", None)
    mutator(forged)
    forged["step_evidence_sha256"] = digest(step_evidence_body(forged))
    forged["next_handoff"] = build_next_handoff(
        forged, forged["step_evidence_sha256"]
    )
    return close_object(forged)


def forged_continuation_rejected(
    history: list[dict[str, Any]], step: dict[str, Any],
    mutator: Callable[[dict[str, Any]], None],
) -> bool:
    forged = forge_live_step(step, mutator)
    forged_history = append_authenticated_history(history, forged)
    forged_original = next_stage_original(forged)
    return rejected_attack(
        lambda: advance_one_collision(forged_original, forged_history)
    )


def mutate_official_word(step: dict[str, Any]) -> None:
    step["official_word"] = {"FORGED": True}


def mutate_wall(step: dict[str, Any]) -> None:
    step["wall"] = {"FORGED": True}


def mutate_core(step: dict[str, Any]) -> None:
    step["core"] = {"FORGED": True}


def mutate_margin(step: dict[str, Any]) -> None:
    step["structured_terminal_decision_margin"] = {
        **step["structured_terminal_decision_margin"],
        "local_strict_decision_margin": {"FORGED": True},
    }


def mutate_candidate_rows(step: dict[str, Any]) -> None:
    table = step["full_candidate_table"]
    table["candidate_rows"][0]["classification"] = "FORGED_CLASSIFICATION"
    table["candidate_rows_sha256"] = digest(table["candidate_rows"])


def mutate_all_numeric(step: dict[str, Any]) -> None:
    mutate_official_word(step)
    mutate_wall(step)
    mutate_core(step)
    mutate_margin(step)
    mutate_candidate_rows(step)


def self_test() -> dict[str, Any]:
    _source, inputs = pair9_inputs()
    original, history = copy.deepcopy(inputs[0])
    tree = adaptive_advance(original, history, 6, 1024)
    live = first_live_leaf(tree)
    step3 = live["step"]
    baseline_original = next_stage_original(step3)
    baseline_history = append_authenticated_history(history, step3)
    baseline = advance_one_collision(baseline_original, baseline_history)
    warm = advance_one_collision(baseline_original, baseline_history)

    forged_evidence = copy.deepcopy(history)
    forged_evidence[0]["evidence_preimage"]["selected_owner"] = "G[9,9]"
    spliced_history = [copy.deepcopy(history[1]), copy.deepcopy(history[0])]
    malformed_box = copy.deepcopy(original)
    malformed_box["closed_box"]["t"] = ["1", "0"]
    malformed_suffix = copy.deepcopy(original)
    malformed_suffix["adaptive_suffix"] = "x"

    forged_split_original = copy.deepcopy(step3["original_box"])
    forged_split = forged_split_original["refinement_decision_chain"][0]
    forged_split.pop("object_sha256")
    forged_split["split_decision"]["axis"] = (
        "p" if forged_split["split_decision"]["axis"] == "t" else "t"
    )
    forged_split["object_sha256"] = digest(forged_split)

    forged_child_bit_original = copy.deepcopy(step3["original_box"])
    forged_child_bit = forged_child_bit_original[
        "refinement_decision_chain"
    ][0]
    forged_child_bit.pop("object_sha256")
    forged_child_bit["selected_child_bit"] = "NOT_A_BIT"
    forged_child_bit["object_sha256"] = digest(forged_child_bit)

    mutation_original = copy.deepcopy(baseline_original)
    mutation_history = copy.deepcopy(baseline_history)
    mutation_result = advance_one_collision(mutation_original, mutation_history)
    mutation_snapshot = canonical(mutation_result)
    mutation_original["closed_box"]["t"][0] = "999"
    mutation_history[0]["selected_owner"] = "G[99,99]"

    prior_registry_cache = v2._REGISTRY_CACHE
    prior_cores_cache = v2._CORES_CACHE
    poison_registry = {"POISON": object()}
    poison_cores = (object(),)
    try:
        v2._REGISTRY_CACHE = poison_registry
        v2._CORES_CACHE = poison_cores
        poisoned = advance_one_collision(baseline_original, baseline_history)
        cache_unchanged = (
            v2._REGISTRY_CACHE is poison_registry
            and v2._CORES_CACHE is poison_cores
        )
    finally:
        v2._REGISTRY_CACHE = prior_registry_cache
        v2._CORES_CACHE = prior_cores_cache

    prior_precision = ctx.prec
    try:
        ctx.prec = 128
        wrong_precision_rejected = rejected_attack(
            lambda: advance_one_collision(baseline_original, baseline_history)
        )
    finally:
        ctx.prec = prior_precision

    attacks = {
        "forged_genesis_evidence_rejected": rejected_attack(
            lambda: advance_one_collision(original, forged_evidence)
        ),
        "history_splice_rejected": rejected_attack(
            lambda: advance_one_collision(original, spliced_history)
        ),
        "malformed_box_rejected": rejected_attack(
            lambda: advance_one_collision(malformed_box, history)
        ),
        "malformed_suffix_rejected": rejected_attack(
            lambda: advance_one_collision(malformed_suffix, history)
        ),
        "coherent_reseal_official_word_rejected": forged_continuation_rejected(
            history, step3, mutate_official_word
        ),
        "coherent_reseal_wall_rejected": forged_continuation_rejected(
            history, step3, mutate_wall
        ),
        "coherent_reseal_core_rejected": forged_continuation_rejected(
            history, step3, mutate_core
        ),
        "coherent_reseal_margin_rejected": forged_continuation_rejected(
            history, step3, mutate_margin
        ),
        "coherent_reseal_candidate_rows_rejected": forged_continuation_rejected(
            history, step3, mutate_candidate_rows
        ),
        "coherent_reseal_all_numeric_fields_rejected": forged_continuation_rejected(
            history, step3, mutate_all_numeric
        ),
        "coherent_reseal_split_decision_rejected": rejected_attack(
            lambda: advance_one_collision(forged_split_original, history)
        ) and rejected_attack(
            lambda: advance_one_collision(forged_child_bit_original, history)
        ),
        "cold_warm_byte_identical": canonical(baseline) == canonical(warm),
        "cache_poison_output_byte_identical": canonical(baseline) == canonical(poisoned),
        "cache_poison_state_unchanged_and_wrong_precision_rejected": (
            cache_unchanged and wrong_precision_rejected
        ),
        "caller_mutation_cannot_change_output":
            canonical(mutation_result) == mutation_snapshot,
    }
    need(len(attacks) == 15 and all(attacks.values()),
         "v4 executed 15/15 adversarial tests")
    return close_object({
        "schema": SCHEMA + ".executed-adversarial-self-test",
        "status": "PASS_15_OF_15_EXECUTED_ADVERSARIAL_TESTS",
        "attacks": attacks,
        "reproduced_v3_official_word_exploit_now_rejected": True,
        "baseline_collision4_step_sha256": baseline["object_sha256"],
        "kernel_global_cache_writes": 0,
        "cache_globals_restored_by_test_harness": (
            v2._REGISTRY_CACHE is prior_registry_cache
            and v2._CORES_CACHE is prior_cores_cache
        ),
        "formal_credit": 0,
        "D02_credit": 0,
        "writes_performed": False,
    })


def emit(value: dict[str, Any]) -> None:
    sys.stdout.buffer.write(canonical(value) + b"\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--regression", action="store_true")
    args = parser.parse_args()
    try:
        emit(self_test() if args.self_test else build_regression())
        return 0
    except (Rejected, v3.Rejected, v2.Rejected, RuntimeError, ValueError,
            KeyError, AssertionError) as exc:
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
