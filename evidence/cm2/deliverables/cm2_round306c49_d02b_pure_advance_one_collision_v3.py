#!/usr/bin/env python3
"""Authenticated, pure, fail-closed D02-B one-collision kernel, v3.

Version 2 accepted digest-only history rows and cached numeric authorities in
module globals.  Version 3 supersedes that contract.  Every public call takes
a complete source-binding preimage and complete evidence preimages for every
historical collision.  It authenticates the recursive step self-hashes,
candidate/owner/root-order bindings, evidence hashes, handoff links, occurrence
identity, and exact dyadic refinement geometry before any numeric continuation.

The numeric context is local to one call or one adaptive invocation.  No cache
or other module global is written.  Inputs are deep-copied before validation
and outputs are deep-copied before sealing, so later caller mutation cannot
alter a returned certificate.

The absent global cemetery/disconnected and codimension-owner oracles remain a
hard PENDING_GLOBAL_ORACLE state.  No v3 result grants formal or D02 credit.
"""

from __future__ import annotations

import argparse
from collections import Counter
import copy
from fractions import Fraction as Q
import hashlib
import json
import math
from pathlib import Path
import re
import sys
from typing import Any, Callable

from flint import arb, ctx
import flint


sys.dont_write_bytecode = True
SELF = Path(__file__).absolute()
DELIVERABLES = SELF.parent
if str(DELIVERABLES) not in sys.path:
    sys.path.insert(0, str(DELIVERABLES))

import cm2_round306c49_d02b_pure_advance_one_collision_v2 as v2
import cm2_round306c45_d02b_pair_preserving_batch_runner_planner_v1 as c45


SCHEMA = "cm2.round306c49.d02-b-pure-advance-one-collision.v3"
ORIGINAL_BOX_SCHEMA = SCHEMA + ".original-box"
SOURCE_BINDING_SCHEMA = SCHEMA + ".source-binding"
GENESIS_SCHEMA = SCHEMA + ".genesis-collision-evidence"
STEP_SCHEMA = SCHEMA + ".step"
HANDOFF_SCHEMA = SCHEMA + ".next-handoff"
SOURCE_CHART_ID = v2.SOURCE_CHART_ID
COLLISION1_OWNER = v2.COLLISION1_OWNER
PAIR_INDEX = v2.PAIR_INDEX
PAIR9_PATH = v2.PAIR9_PATH
SIDE_ORDER = v2.SIDE_ORDER
QUEUE_PINS = v2.QUEUE_PINS
EXPECTED_C44_SIDE_CENSUS = v2.EXPECTED_C44_SIDE_CENSUS
MISSING_GLOBAL_ORACLES = v2.MISSING_GLOBAL_ORACLES
ALLOWED_TERMINALS = v2.ALLOWED_TERMINALS
HEX64 = re.compile(r"[0-9a-f]{64}\Z")

# Filled from the exact C45 pair-9 source envelopes and then frozen.  These
# hashes make a self-rehashed forged source preimage insufficient.
PAIR9_SOURCE_BINDING_PINS = {
    "REFLECTED": "d9d1ad4f4bf856764733d8f1f8360e51f8f003572104e868eb445e90c6073482",
    "REPRESENTATIVE": "486f959429f2b69440e0c68349c308eb07060303185536e3c771188658ab5dab",
}

RR = v2.RR
TIME = v2.TIME
BASE = v2.BASE


class Rejected(RuntimeError):
    """Authentication, enclosure, or adversarial-test rejection."""


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


def close_object(value: dict[str, Any]) -> dict[str, Any]:
    """Deep-copy before sealing so no output aliases a caller-owned object."""

    sealed = copy.deepcopy(value)
    need("object_sha256" not in sealed, "object hash absent before sealing")
    sealed["object_sha256"] = digest(sealed)
    return sealed


def verify_closed(value: Any, label: str) -> None:
    need(type(value) is dict, label + " object")
    claimed = value.get("object_sha256")
    need(type(claimed) is str and HEX64.fullmatch(claimed) is not None,
         label + " object SHA-256")
    body = copy.deepcopy(value)
    del body["object_sha256"]
    need(digest(body) == claimed, label + " self hash")


def normalized_box(raw: dict[str, Any]) -> dict[str, list[str]]:
    return {axis: list(raw[axis]) for axis in ("t", "p", "s")}


def validate_box(value: Any, label: str) -> None:
    need(type(value) is dict and set(value) == {"t", "p", "s"},
         label + " exact keys")
    for axis in ("t", "p", "s"):
        pair = value[axis]
        need(type(pair) is list and len(pair) == 2
             and all(type(item) is str for item in pair), label + ":" + axis)
        need(Q(pair[0]) <= Q(pair[1]), label + " ordered:" + axis)
    need(Q(value["s"][0]) == Q(value["s"][1]) == 0, label + " s=0")


def power_two_exponent(value: Q) -> int | None:
    if value <= 0 or value.denominator != 1:
        return None
    integer = value.numerator
    if integer & (integer - 1):
        return None
    return integer.bit_length() - 1


def axis_refinement_bits(parent: list[str], child: list[str], label: str) -> str:
    p0, p1 = Q(parent[0]), Q(parent[1])
    c0, c1 = Q(child[0]), Q(child[1])
    need(p0 <= c0 <= c1 <= p1, label + " nested")
    if p0 == p1:
        need(c0 == c1 == p0, label + " point preserved")
        return ""
    parent_width, child_width = p1 - p0, c1 - c0
    need(child_width > 0, label + " nondegenerate descendant")
    exponent = power_two_exponent(parent_width / child_width)
    need(exponent is not None, label + " dyadic width ratio")
    index = (c0 - p0) / child_width
    need(index.denominator == 1 and 0 <= index.numerator < 2**exponent,
         label + " dyadic offset")
    need(c1 == c0 + child_width, label + " exact child endpoint")
    return format(index.numerator, f"0{exponent}b") if exponent else ""


def is_shuffle(sequence: str, left: str, right: str) -> bool:
    states = {(0, 0)}
    for token in sequence:
        next_states: set[tuple[int, int]] = set()
        for i, j in states:
            if i < len(left) and left[i] == token:
                next_states.add((i + 1, j))
            if j < len(right) and right[j] == token:
                next_states.add((i, j + 1))
        states = next_states
        if not states:
            return False
    return (len(left), len(right)) in states


def verify_refinement(
    parent_box: dict[str, Any], parent_suffix: str, extension: str,
    child_box: dict[str, Any], child_suffix: str, label: str,
) -> None:
    validate_box(parent_box, label + " parent box")
    validate_box(child_box, label + " child box")
    need(type(parent_suffix) is str and set(parent_suffix) <= {"0", "1"},
         label + " parent suffix")
    need(type(extension) is str and set(extension) <= {"0", "1"},
         label + " extension")
    need(child_suffix == parent_suffix + extension,
         label + " suffix concatenation")
    t_bits = axis_refinement_bits(parent_box["t"], child_box["t"], label + " t")
    p_bits = axis_refinement_bits(parent_box["p"], child_box["p"], label + " p")
    need(len(extension) == len(t_bits) + len(p_bits)
         and is_shuffle(extension, t_bits, p_bits),
         label + " exact t/p dyadic shuffle")
    need(child_box["s"] == parent_box["s"], label + " s preserved")


def source_binding_body(source: dict[str, Any], handoff: dict[str, Any]) -> dict[str, Any]:
    raw_box = normalized_box(source[handoff["box_key"]])
    occurrence = copy.deepcopy(handoff["collision2_occurrence_owner_binding"])
    return {
        "schema": SOURCE_BINDING_SCHEMA,
        "pair_index": source["pair_index"],
        "C41_path": source["path"],
        "side": handoff["side"],
        "source_chart_id": SOURCE_CHART_ID,
        "closed_source_box": raw_box,
        "C41_ambient_cell_id": source["c41_ambient_cell_id"],
        "C41_row_sha256": source["row_sha256"],
        "C45_handoff_id": handoff["handoff_id"],
        "C45_occurrence_owner_binding": occurrence,
        "incoming_collision2_owner": handoff["occurrence_incoming_owner"],
        "queue_pins": copy.deepcopy(QUEUE_PINS),
        "formal_credit": 0,
    }


def verify_occurrence_binding(value: dict[str, Any]) -> None:
    need(type(value) is dict and type(value.get("binding_id")) is str,
         "C45 occurrence binding")
    body = copy.deepcopy(value)
    claimed = body.pop("binding_id")
    need(claimed == "c45-collision2-occurrence-owner:" + digest(body),
         "C45 occurrence binding id")
    need(body.get("formal_credit") == 0, "C45 occurrence zero credit")


def verify_source_binding(value: Any) -> None:
    verify_closed(value, "source binding")
    expected_keys = {
        "schema", "pair_index", "C41_path", "side", "source_chart_id",
        "closed_source_box", "C41_ambient_cell_id", "C41_row_sha256",
        "C45_handoff_id", "C45_occurrence_owner_binding",
        "incoming_collision2_owner", "queue_pins", "formal_credit",
        "object_sha256",
    }
    need(set(value) == expected_keys and value["schema"] == SOURCE_BINDING_SCHEMA,
         "source binding exact schema/keys")
    need(value["pair_index"] == PAIR_INDEX and value["C41_path"] == PAIR9_PATH,
         "pinned pair9 source")
    need(value["side"] in SIDE_ORDER and value["source_chart_id"] == SOURCE_CHART_ID,
         "source side/chart")
    need(value["object_sha256"] == PAIR9_SOURCE_BINDING_PINS[value["side"]],
         "pinned authoritative source binding preimage")
    validate_box(value["closed_source_box"], "source closed box")
    need(value["queue_pins"] == QUEUE_PINS and value["formal_credit"] == 0,
         "source queue/credit pins")
    verify_occurrence_binding(value["C45_occurrence_owner_binding"])
    occurrence = value["C45_occurrence_owner_binding"]
    need(occurrence["physical_side"] == value["side"]
         and occurrence["incoming_owner"] == value["incoming_collision2_owner"]
         and occurrence["c41_ambient_cell_id"] == value["C41_ambient_cell_id"]
         and occurrence["c41_row_sha256"] == value["C41_row_sha256"],
         "source occurrence cross binding")


def validate_original_box(value: Any) -> None:
    expected = {
        "schema", "occurrence_id", "side", "source_chart_id", "closed_box",
        "adaptive_suffix", "source_binding_sha256", "source_binding_preimage",
        "parent_handoff_id", "refinement_parent_box",
        "refinement_parent_adaptive_suffix", "refinement_path_extension",
    }
    need(type(value) is dict and set(value) == expected,
         "original box exact keys")
    need(value["schema"] == ORIGINAL_BOX_SCHEMA, "original box schema")
    need(type(value["occurrence_id"]) is str and value["occurrence_id"] != "",
         "occurrence id")
    need(value["side"] in SIDE_ORDER and value["source_chart_id"] == SOURCE_CHART_ID,
         "original side/chart")
    need(type(value["parent_handoff_id"]) is str
         and value["parent_handoff_id"] != "", "parent handoff id")
    verify_source_binding(value["source_binding_preimage"])
    source = value["source_binding_preimage"]
    need(value["source_binding_sha256"] == source["object_sha256"],
         "source binding digest/preimage")
    need(value["side"] == source["side"]
         and value["occurrence_id"] == source["C45_handoff_id"],
         "original occurrence/source binding")
    verify_refinement(
        value["refinement_parent_box"],
        value["refinement_parent_adaptive_suffix"],
        value["refinement_path_extension"],
        value["closed_box"], value["adaptive_suffix"],
        "original refinement",
    )


def genesis_history(original_box: dict[str, Any]) -> list[dict[str, Any]]:
    source = original_box["source_binding_preimage"]
    collision1_handoff_identity = {
        "schema": SCHEMA + ".genesis-collision1-to-2-handoff",
        "source_binding_sha256": source["object_sha256"],
        "occurrence_id": original_box["occurrence_id"],
        "collision_index": 2,
    }
    collision1_handoff = "c49v3-genesis-collision2:" + digest(
        collision1_handoff_identity
    )
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
        "next_handoff_id": collision1_handoff,
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
        "previous_handoff_id": collision1_handoff,
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
        "handoff_id": "c49v3-next-collision:" + digest(identity),
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


def verify_candidate_binding(step: dict[str, Any], label: str) -> None:
    required = {
        "exact_owner", "discriminant", "root_order", "official_word", "chart",
        "wall", "homogeneity", "incidence", "core",
        "structured_terminal_decision_margin", "full_candidate_table",
    }
    need(all(step.get(key) is not None for key in required),
         label + " complete numeric fields")
    table = step["full_candidate_table"]
    rows = table.get("candidate_rows")
    need(type(rows) is list and len(rows) == table.get("candidate_count"),
         label + " candidate count")
    need([row["candidate_id"] for row in rows]
         == table.get("candidate_ids_in_frozen_order"),
         label + " candidate order")
    need(digest(rows) == table.get("candidate_rows_sha256"),
         label + " candidate table hash")
    need(table.get("strict_unique_owner") is True
         and table.get("selected_owner")
         == step["exact_owner"]["selected_target_id"],
         label + " unique owner binding")
    need(table.get("selected_discriminant") == step["discriminant"]
         and table.get("root_order") == step["root_order"]
         and type(step["root_order"]) is dict
         and step["root_order"].get("strict") is True,
         label + " discriminant/root-order binding")
    decision = step["structured_terminal_decision_margin"]
    need(step.get("status") == decision.get("status") == "PENDING_GLOBAL_ORACLE"
         and decision.get("missing_global_oracles") == list(MISSING_GLOBAL_ORACLES)
         and step.get("formal_credit") == step.get("D02_credit") == 0,
         label + " pending oracle/zero credit")


def verify_handoff(step: dict[str, Any], label: str) -> None:
    handoff = step.get("next_handoff")
    need(type(handoff) is dict, label + " next handoff")
    identity = handoff_identity(step, step["step_evidence_sha256"])
    need({key: handoff[key] for key in identity} == identity,
         label + " handoff identity")
    need(handoff.get("handoff_id")
         == "c49v3-next-collision:" + digest(identity),
         label + " handoff id")
    need(handoff.get("appended_history_row") == {
        "collision_index": step["collision_index"],
        "selected_owner": step["exact_owner"]["selected_target_id"],
        "evidence_sha256": step["step_evidence_sha256"],
    }, label + " handoff history stub")


def verify_prior_step(
    preimage: dict[str, Any], row: dict[str, Any],
    expected_prefix: list[dict[str, Any]], source_binding: dict[str, Any],
    label: str,
) -> None:
    verify_closed(preimage, label)
    need(preimage.get("schema") == STEP_SCHEMA
         and preimage.get("collision_index") == row["collision_index"],
         label + " schema/index")
    need(preimage.get("owner_history") == expected_prefix,
         label + " exact recursive history prefix")
    original = preimage.get("original_box")
    validate_original_box(original)
    need(original["source_binding_preimage"] == source_binding,
         label + " source preimage continuity")
    need(preimage.get("step_evidence_sha256") == row["evidence_sha256"]
         == digest(step_evidence_body(preimage)),
         label + " step evidence hash")
    verify_candidate_binding(preimage, label)
    need(preimage["exact_owner"]["selected_target_id"]
         == row["selected_owner"], label + " row owner binding")
    verify_handoff(preimage, label)


def validate_history_and_chain(
    original_box: dict[str, Any], owner_history: Any,
) -> None:
    need(type(owner_history) is list and len(owner_history) >= 2,
         "authenticated owner history")
    expected_row_keys = {
        "collision_index", "selected_owner", "evidence_sha256",
        "evidence_preimage",
    }
    for index, row in enumerate(owner_history, 1):
        need(type(row) is dict and set(row) == expected_row_keys,
             "history row exact keys")
        need(row["collision_index"] == index
             and type(row["selected_owner"]) is str
             and type(row["evidence_sha256"]) is str
             and HEX64.fullmatch(row["evidence_sha256"]) is not None,
             "history row index/owner/hash")
    expected_genesis = genesis_history(original_box)
    need(owner_history[:2] == expected_genesis,
         "exact authenticated genesis evidence preimages")
    source = original_box["source_binding_preimage"]
    expected_handoff = expected_genesis[1]["evidence_preimage"]["next_handoff_id"]
    expected_parent_box = source["closed_source_box"]
    expected_parent_suffix = ""
    for offset, row in enumerate(owner_history[2:], 3):
        preimage = row["evidence_preimage"]
        verify_prior_step(
            preimage, row, owner_history[:offset - 1], source,
            f"history collision {offset}",
        )
        prior_original = preimage["original_box"]
        need(prior_original["parent_handoff_id"] == expected_handoff,
             f"history collision {offset} parent handoff")
        need(prior_original["refinement_parent_box"] == expected_parent_box
             and prior_original["refinement_parent_adaptive_suffix"]
             == expected_parent_suffix,
             f"history collision {offset} parent geometry")
        expected_handoff = preimage["next_handoff"]["handoff_id"]
        expected_parent_box = prior_original["closed_box"]
        expected_parent_suffix = prior_original["adaptive_suffix"]
    need(original_box["parent_handoff_id"] == expected_handoff,
         "current parent handoff continuity")
    need(original_box["refinement_parent_box"] == expected_parent_box
         and original_box["refinement_parent_adaptive_suffix"]
         == expected_parent_suffix,
         "current previous-to-next box/suffix continuity")


def simple_numeric_inputs(
    original_box: dict[str, Any], owner_history: list[dict[str, Any]],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    original = {
        "schema": v2.ORIGINAL_BOX_SCHEMA,
        "occurrence_id": original_box["occurrence_id"],
        "side": original_box["side"],
        "source_chart_id": original_box["source_chart_id"],
        "closed_box": copy.deepcopy(original_box["closed_box"]),
        "adaptive_suffix": original_box["adaptive_suffix"],
        "source_binding_sha256": original_box["source_binding_sha256"],
    }
    history = [
        {
            "collision_index": row["collision_index"],
            "selected_owner": row["selected_owner"],
            "evidence_sha256": row["evidence_sha256"],
        }
        for row in owner_history
    ]
    return original, history


def local_numeric_context() -> dict[str, Any]:
    """Fresh local authorities; intentionally no cache read or write."""

    pair_table, pattern_table, registry_sha = RR.component_cert.key_index_tables()
    return {
        "pair_table": pair_table,
        "pattern_table": pattern_table,
        "registry_sha": registry_sha,
        "cores": tuple(RR.core_cert.physical_cores()),
    }


def numeric_step(
    original_box: dict[str, Any], owner_history: list[dict[str, Any]],
    numeric_context: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    numeric_original, numeric_history = simple_numeric_inputs(
        original_box, owner_history
    )
    box = v2.atlas_box(numeric_original)
    collision_index = len(owner_history) + 1
    result: dict[str, Any] = {
        "schema": STEP_SCHEMA,
        "status": "UNRESOLVED_FAIL_CLOSED",
        "collision_index": collision_index,
        "collision_index_derivation": "len(owner_history)+1",
        "original_box": copy.deepcopy(original_box),
        "original_box_sha256": digest(original_box),
        "owner_history": copy.deepcopy(owner_history),
        "owner_history_sha256": digest(owner_history),
        "exact_owner": None,
        "discriminant": None,
        "root_order": None,
        "official_word": None,
        "chart": None,
        "wall": None,
        "homogeneity": None,
        "incidence": None,
        "core": None,
        "structured_terminal_decision_margin": None,
        "full_candidate_table": None,
        "global_oracle_available": False,
        "formal_credit": 0,
        "D02_credit": 0,
    }
    state, replay = v2.geometry_after_history(
        box, numeric_history, original_box["source_chart_id"]
    )
    result["history_replay"] = replay
    internal: dict[str, Any] = {
        "box": box, "state": state,
        "numeric_original": numeric_original,
        "numeric_history": numeric_history,
    }
    if state is None:
        result["blocker"] = replay.get("status", "UNRESOLVED_HISTORY_STATE")
        return result, internal
    result["chart"] = {
        "incoming_chart": state["chart"],
        "incoming_chart_margin": {
            "normal_x": replay["normal_x"],
            "normal_y": replay["normal_y"],
            "nx2_minus_ny2": replay["chart_factor_nx2_minus_ny2"],
        },
        "outgoing_chart": None,
        "outgoing_chart_margin": None,
    }
    current_target = owner_history[-1]["selected_owner"]
    table, candidate_internal = v2.candidate_table(box, state, current_target)
    result["full_candidate_table"] = table
    result["discriminant"] = table["selected_discriminant"]
    result["root_order"] = table["root_order"]
    internal["candidate_internal"] = candidate_internal
    if not table["strict_unique_owner"]:
        result["blocker"] = "NEXT_OWNER_OR_ROOT_ORDER_UNRESOLVED"
        return result, internal
    selected = next(row for row in candidate_internal
                    if row["candidate_id"] == table["selected_owner"])
    owner_public, owner_internal = v2.exact_owner(state, selected)
    result["exact_owner"] = owner_public
    internal["owner_internal"] = owner_internal
    owner_for_word = {
        "selected_target_id": selected["candidate_id"], **owner_internal,
    }
    word, error = RR.translation_normalized_official_word(
        state, current_target, owner_for_word,
        numeric_context["pair_table"], numeric_context["pattern_table"],
    )
    if word is None:
        result["blocker"] = "OFFICIAL_WORD_UNRESOLVED:" + str(error)
        return result, internal
    result["official_word"] = {
        **RR.compact_key(word["key"]),
        "absolute_selected_target_id": word["absolute_selected_target_id"],
        "relative_frozen_target_id": word["relative_frozen_target_id"],
        "ordered_clean_wall_record": word["ordered_clean_wall_record"],
        "absolute_lattice_translation_removed":
            word["absolute_lattice_translation_removed"],
        "official_registry_sha256": numeric_context["registry_sha"],
    }
    try:
        result["wall"] = v2.wall_audit(state, current_target, owner_internal)
    except v2.Rejected as exc:
        result["blocker"] = "WALL_OR_ORDER_UNRESOLVED:" + str(exc)
        return result, internal
    next_state = v2.outgoing_state(selected["candidate_id"], state, owner_internal)
    if next_state is None:
        result["blocker"] = "OUTGOING_CHART_UNRESOLVED"
        return result, internal
    if next_state["chart"] in {"E", "W"}:
        chart_value = abs(next_state["normal_x"]) - abs(next_state["normal_y"])
    else:
        chart_value = abs(next_state["normal_y"]) - abs(next_state["normal_x"])
    if not bool(chart_value > 0):
        result["blocker"] = "OUTGOING_CHART_MARGIN_UNRESOLVED"
        return result, internal
    result["chart"]["outgoing_chart"] = next_state["chart"]
    result["chart"]["outgoing_chart_margin"] = v2.positive_margin(chart_value)
    result["homogeneity"] = v2.homogeneity(owner_internal["cosine"])
    tangential = state["incoming_tangential"]
    cosine_square = arb(1) - tangential * tangential
    if not bool(cosine_square > 0):
        result["blocker"] = "INCOMING_INCIDENCE_COSINE_UNRESOLVED"
        return result, internal
    source_rank, source_margin = v2.incidence_rank(cosine_square.sqrt())
    target_rank, target_margin = v2.incidence_rank(owner_internal["cosine"])
    if source_rank is not None and target_rank is not None:
        result["incidence"] = {
            "rank_B": max(14, source_rank, target_rank),
            "source_rank": source_rank,
            "target_rank": target_rank,
            "source_rank_margin": source_margin,
            "target_rank_margin": target_margin,
            "codimension_owner_status": "PENDING_GLOBAL_ORACLE",
        }
    classification, destination, witnesses = TIME.core_classification(
        owner_for_word, numeric_context["cores"]
    )
    margin = None
    if classification != "UNRESOLVED_TIME3_OUTER":
        margin = v2.core_margin(
            selected["candidate_id"], owner_internal,
            classification, destination, numeric_context["cores"],
        )
    result["core"] = {
        "classification": classification,
        "destination_core_id": destination,
        "witness_count": len(witnesses),
        "witnesses_sha256": digest(witnesses),
        "minimum_inside_or_exclusion_margin": margin,
    }
    if result["homogeneity"] is None or result["incidence"] is None or margin is None:
        result["blocker"] = "AUXILIARY_STRATUM_UNRESOLVED"
        return result, internal
    result["structured_terminal_decision_margin"] = v2.pending_terminal_decision(
        collision_index, classification, destination, margin
    )
    result["status"] = "PENDING_GLOBAL_ORACLE"
    internal["local_complete"] = True
    return result, internal


def authenticated_numeric_step(
    original_box: dict[str, Any], owner_history: list[dict[str, Any]],
    numeric_context: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    validate_original_box(original_box)
    validate_history_and_chain(original_box, owner_history)
    return numeric_step(original_box, owner_history, numeric_context)


def advance_one_collision(
    original_box: dict[str, Any], owner_history: list[dict[str, Any]],
) -> dict[str, Any]:
    """Public pure kernel with complete authenticated history preimages."""

    owned_box = copy.deepcopy(original_box)
    owned_history = copy.deepcopy(owner_history)
    context = local_numeric_context()
    result, _internal = authenticated_numeric_step(
        owned_box, owned_history, context
    )
    return seal_step(result)


def append_authenticated_history(
    owner_history: list[dict[str, Any]], step: dict[str, Any],
) -> list[dict[str, Any]]:
    verify_closed(step, "appended prior step")
    verify_handoff(step, "appended prior step")
    stub = step["next_handoff"]["appended_history_row"]
    return copy.deepcopy(owner_history) + [{
        **copy.deepcopy(stub),
        "evidence_preimage": copy.deepcopy(step),
    }]


def next_stage_original(step: dict[str, Any]) -> dict[str, Any]:
    verify_handoff(step, "next-stage source step")
    original = step["original_box"]
    return {
        **copy.deepcopy(original),
        "parent_handoff_id": step["next_handoff"]["handoff_id"],
        "refinement_parent_box": copy.deepcopy(original["closed_box"]),
        "refinement_parent_adaptive_suffix": original["adaptive_suffix"],
        "refinement_path_extension": "",
    }


def child_original_box(parent: dict[str, Any], child: Any) -> dict[str, Any]:
    answer = copy.deepcopy(parent)
    answer["closed_box"] = v2.public_box(child)
    answer["adaptive_suffix"] = child.path
    prefix = answer["refinement_parent_adaptive_suffix"]
    need(child.path.startswith(prefix), "child suffix prefix")
    answer["refinement_path_extension"] = child.path[len(prefix):]
    return answer


def adaptive_advance(
    original_box: dict[str, Any], owner_history: list[dict[str, Any]],
    maximum_additional_depth: int, maximum_nodes: int,
) -> dict[str, Any]:
    owned_box = copy.deepcopy(original_box)
    owned_history = copy.deepcopy(owner_history)
    validate_original_box(owned_box)
    validate_history_and_chain(owned_box, owned_history)
    need(type(maximum_additional_depth) is int and maximum_additional_depth >= 0,
         "adaptive depth")
    need(type(maximum_nodes) is int and maximum_nodes > 0, "adaptive node bound")
    context = local_numeric_context()
    numeric_original, _simple_history = simple_numeric_inputs(owned_box, owned_history)
    root = v2.atlas_box(numeric_original)
    root_depth = root.depth
    stack = [root]
    leaves: list[dict[str, Any]] = []
    nodes = splits = 0
    while stack:
        box = stack.pop()
        nodes += 1
        need(nodes <= maximum_nodes, "adaptive node bound exhausted")
        current = child_original_box(owned_box, box)
        # Source/history authentication is replayed for each emitted numeric
        # occurrence; numeric authorities remain call-local and immutable.
        result, internal = authenticated_numeric_step(
            current, owned_history, context
        )
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
        numeric_current, numeric_history = simple_numeric_inputs(
            current, owned_history
        )
        decision = v2.sensitivity_split(
            numeric_current, numeric_history, result, internal
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
             "adaptive split replay")
        splits += 1
        stack.append(right)
        stack.append(left)
    paths = sorted(row["adaptive_suffix"] for row in leaves)
    need(not any(right.startswith(left) for left, right in zip(paths, paths[1:])),
         "adaptive prefix free")
    need(sum(Q(row["relative_Kraft_fraction"]) for row in leaves) == 1,
         "adaptive Kraft conservation")
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


def pair9_source_inputs_unvalidated() -> tuple[
    dict[str, Any], list[tuple[dict[str, Any], list[dict[str, Any]]]]
]:
    _planner, ordered, bundle = v2.frozen_queue()
    matches = [row for row in ordered
               if row["pair_index"] == PAIR_INDEX and row["path"] == PAIR9_PATH]
    need(len(matches) == 1, "unique pair9 row")
    source = matches[0]
    handoffs = c45.build_handoffs(source, bundle)
    need([row["side"] for row in handoffs] == list(SIDE_ORDER),
         "canonical pair9 side order")
    inputs = []
    for handoff in handoffs:
        source_binding = close_object(source_binding_body(source, handoff))
        original = {
            "schema": ORIGINAL_BOX_SCHEMA,
            "occurrence_id": source_binding["C45_handoff_id"],
            "side": source_binding["side"],
            "source_chart_id": SOURCE_CHART_ID,
            "closed_box": copy.deepcopy(source_binding["closed_source_box"]),
            "adaptive_suffix": "",
            "source_binding_sha256": source_binding["object_sha256"],
            "source_binding_preimage": source_binding,
            "parent_handoff_id": source_binding["C45_handoff_id"],
            "refinement_parent_box": copy.deepcopy(
                source_binding["closed_source_box"]
            ),
            "refinement_parent_adaptive_suffix": "",
            "refinement_path_extension": "",
        }
        inputs.append((original, genesis_history(original)))
    return source, inputs


def pair9_inputs() -> tuple[
    dict[str, Any], list[tuple[dict[str, Any], list[dict[str, Any]]]]
]:
    source, inputs = pair9_source_inputs_unvalidated()
    for original, history in inputs:
        validate_original_box(original)
        validate_history_and_chain(original, history)
    return source, inputs


def first_live_leaf(tree: dict[str, Any]) -> dict[str, Any]:
    rows = [row for row in tree["leaves"]
            if (row["step"].get("structured_terminal_decision_margin") or {}).get(
                "local_disposition"
            ) == "LIVE_CONTINUE"]
    need(len(rows) > 0, "canonical live leaf")
    return min(rows, key=lambda row: row["adaptive_suffix"])


def build_regression() -> dict[str, Any]:
    need(flint.__version__ == "0.9.0" and ctx.prec == 384, "Arb runtime pin")
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
             "exact C44 census:" + original["side"])
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
          step5["collision_index"]] == [3, 4, 5], "generic indices 3/4/5")
    for label, step in (("collision3", step3), ("collision4", step4),
                        ("collision5", step5)):
        verify_closed(step, label)
        verify_candidate_binding(step, label)
        need(step["formal_credit"] == step["D02_credit"] == 0,
             label + " zero credit")
    return close_object({
        "schema": SCHEMA + ".pair9-regression",
        "status": "PASS_AUTHENTICATED_PAIR9_COLLISION3_4_5_ZERO_CREDIT_REGRESSION",
        "producer_source_sha256": file_sha(SELF),
        "v2_superseded_source_sha256": file_sha(Path(v2.__file__).absolute()),
        "queue_pins": copy.deepcopy(QUEUE_PINS),
        "pair_index": PAIR_INDEX,
        "C41_path": PAIR9_PATH,
        "C41_row_sha256": source["row_sha256"],
        "source_binding_pins": copy.deepcopy(PAIR9_SOURCE_BINDING_PINS),
        "collision3_both_physical_sides": collision3,
        "first_canonical_live_leaf_policy":
            "C45_SIDE_ORDER_THEN_BINARY_ADAPTIVE_SUFFIX",
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
        "collision_index_hard_code_absent": True,
        "authenticated_history_preimages_verified": True,
        "global_state_cache_writes": 0,
        "global_oracle_status": "PENDING_GLOBAL_ORACLE",
        "missing_global_oracles": list(MISSING_GLOBAL_ORACLES),
        "formal_credit": 0,
        "D02_credit": 0,
        "authority_pointer_touched": False,
        "canonical_status_touched": False,
        "writes_performed": False,
    })


def known_reflected_collision3_leaf(
    original: dict[str, Any],
) -> dict[str, Any]:
    leaf = copy.deepcopy(original)
    leaf["closed_box"] = {
        "t": ["-16107/32000", "-2061519/4096000"],
        "p": ["585/1024", "9361/16384"],
        "s": ["0", "0"],
    }
    leaf["adaptive_suffix"] = "000000"
    leaf["refinement_path_extension"] = "000000"
    return leaf


def rejected_attack(action: Callable[[], Any]) -> bool:
    try:
        action()
    except (Rejected, v2.Rejected, ValueError, KeyError, AssertionError):
        return bool(1)
    return bool(0)


def reclose(value: dict[str, Any]) -> dict[str, Any]:
    body = copy.deepcopy(value)
    body.pop("object_sha256", None)
    return close_object(body)


def forged_binding_step(step: dict[str, Any]) -> dict[str, Any]:
    forged = copy.deepcopy(step)
    forged.pop("object_sha256", None)
    forged["exact_owner"]["selected_target_id"] = "G[99,99]"
    forged["step_evidence_sha256"] = digest(step_evidence_body(forged))
    forged["next_handoff"] = build_next_handoff(
        forged, forged["step_evidence_sha256"]
    )
    return close_object(forged)


def build_self_test_fixture() -> tuple[
    dict[str, Any], list[dict[str, Any]], dict[str, Any]
]:
    _source, inputs = pair9_inputs()
    original, history = copy.deepcopy(inputs[0])
    leaf = known_reflected_collision3_leaf(original)
    step3 = advance_one_collision(leaf, history)
    need(step3["status"] == "PENDING_GLOBAL_ORACLE"
         and step3["next_handoff"] is not None, "live collision3 fixture")
    return leaf, history, step3


def self_test() -> dict[str, Any]:
    leaf, history, step3 = build_self_test_fixture()
    baseline = advance_one_collision(leaf, history)
    warm = advance_one_collision(leaf, history)

    forged_evidence_history = copy.deepcopy(history)
    forged_evidence_history[0]["evidence_preimage"]["selected_owner"] = "G[9,9]"

    binding_mismatch_source = copy.deepcopy(leaf)
    source = binding_mismatch_source["source_binding_preimage"]
    source["incoming_collision2_owner"] = "G[9,9]"
    source = reclose(source)
    binding_mismatch_source["source_binding_preimage"] = source
    binding_mismatch_source["source_binding_sha256"] = source["object_sha256"]

    spliced_history = [copy.deepcopy(history[1]), copy.deepcopy(history[0])]

    malformed_box = copy.deepcopy(leaf)
    malformed_box["closed_box"]["t"] = ["1", "0"]
    malformed_suffix = copy.deepcopy(leaf)
    malformed_suffix["adaptive_suffix"] = "00000x"

    forged_step = forged_binding_step(step3)
    forged_history = append_authenticated_history(history, forged_step)
    forged_next = next_stage_original(forged_step)

    mutation_box = copy.deepcopy(leaf)
    mutation_history = copy.deepcopy(history)
    mutation_result = advance_one_collision(mutation_box, mutation_history)
    mutation_snapshot = canonical(mutation_result)
    mutation_box["closed_box"]["t"][0] = "999"
    mutation_history[0]["selected_owner"] = "G[99,99]"
    mutation_isolated = canonical(mutation_result) == mutation_snapshot

    prior_registry_cache = v2._REGISTRY_CACHE
    prior_cores_cache = v2._CORES_CACHE
    poison_registry = {"POISON": object()}
    poison_cores = (object(),)
    try:
        v2._REGISTRY_CACHE = poison_registry
        v2._CORES_CACHE = poison_cores
        poisoned = advance_one_collision(leaf, history)
        cache_unchanged = (
            v2._REGISTRY_CACHE is poison_registry
            and v2._CORES_CACHE is poison_cores
        )
    finally:
        v2._REGISTRY_CACHE = prior_registry_cache
        v2._CORES_CACHE = prior_cores_cache

    attacks = {
        "forged_evidence_preimage_rejected": rejected_attack(
            lambda: advance_one_collision(leaf, forged_evidence_history)
        ),
        "self_rehashed_source_binding_mismatch_rejected": rejected_attack(
            lambda: advance_one_collision(binding_mismatch_source, history)
        ),
        "history_splice_rejected": rejected_attack(
            lambda: advance_one_collision(leaf, spliced_history)
        ),
        "candidate_owner_binding_mismatch_rejected": rejected_attack(
            lambda: advance_one_collision(forged_next, forged_history)
        ),
        "malformed_box_rejected": rejected_attack(
            lambda: advance_one_collision(malformed_box, history)
        ),
        "malformed_suffix_rejected": rejected_attack(
            lambda: advance_one_collision(malformed_suffix, history)
        ),
        "cold_warm_byte_identical": canonical(baseline) == canonical(warm),
        "cache_poison_output_byte_identical": canonical(baseline) == canonical(poisoned),
        "cache_poison_state_unchanged_by_kernel": cache_unchanged,
        "caller_input_mutation_cannot_change_sealed_output": mutation_isolated,
    }
    need(len(attacks) == 10 and all(attacks.values()),
         "executed 10/10 adversarial tests")
    return close_object({
        "schema": SCHEMA + ".executed-adversarial-self-test",
        "status": "PASS_10_OF_10_EXECUTED_ADVERSARIAL_TESTS",
        "attacks": attacks,
        "baseline_step_sha256": baseline["object_sha256"],
        "cache_globals_restored_by_test_harness": (
            v2._REGISTRY_CACHE is prior_registry_cache
            and v2._CORES_CACHE is prior_cores_cache
        ),
        "kernel_global_cache_writes": 0,
        "formal_credit": 0,
        "D02_credit": 0,
        "writes_performed": False,
    })


def emit(value: dict[str, Any]) -> None:
    sys.stdout.buffer.write(canonical(value) + b"\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--source-binding-pins", action="store_true")
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--regression", action="store_true")
    args = parser.parse_args()
    try:
        if args.source_binding_pins:
            _source, inputs = pair9_source_inputs_unvalidated()
            emit(close_object({
                "schema": SCHEMA + ".source-binding-pin-builder",
                "pins": {
                    original["side"]: original["source_binding_sha256"]
                    for original, _history in inputs
                },
                "writes_performed": False,
                "formal_credit": 0,
            }))
        else:
            emit(self_test() if args.self_test else build_regression())
        return 0
    except (Rejected, v2.Rejected, RuntimeError, ValueError, KeyError,
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
