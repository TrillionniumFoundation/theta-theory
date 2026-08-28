#!/usr/bin/env python3
"""Fail-closed global cemetery/disconnected-exterior oracle contract.

This module is deliberately zero-credit.  It accepts a complete physical-side
occurrence binding (frozen original box, authenticated owner history, current
numeric step, and an independent-replay attestation), verifies every available
structural commitment, and then refuses to manufacture a terminal conclusion.

The checked repository has no pinned implementation of the global four-chart
fundamental-domain branch-and-bound/component theorem required to distinguish
a genuinely disconnected exterior/cemetery component from a bounded interval
with no current contact.  Therefore ``evaluate_query`` can only return either
an input/shortcut rejection or a hard missing-oracle result.  In particular,
no status emitted by this file grants terminal, formal, or D02 credit.
"""

from __future__ import annotations

import argparse
import copy
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
from typing import Any, Callable


sys.dont_write_bytecode = True
SELF = Path(__file__).absolute()

SCHEMA = "cm2.round306c50b.d02-b-global-cemetery-disconnected-exterior-oracle.v1"
QUERY_SCHEMA = SCHEMA + ".query"
BINDING_SCHEMA = SCHEMA + ".physical-side-occurrence-binding"
ATTESTATION_SCHEMA = SCHEMA + ".independent-numeric-replay-attestation"
RESULT_SCHEMA = SCHEMA + ".result"
CONTRACT_SCHEMA = SCHEMA + ".missing-oracle-contract"
SELF_TEST_SCHEMA = SCHEMA + ".executed-hostile-self-test"
REQUESTED_TERMINAL = "STRICT_CEMETERY_OR_DISCONNECTED"
GLOBAL_ORACLE_NAME = "GLOBAL_CEMETERY_DISCONNECTED_EXTERIOR_ORACLE"

HEX64 = re.compile(r"[0-9a-f]{64}\Z")
OWNER_ID = re.compile(r"[A-Z]+\[-?\d+,-?\d+\]\Z")
ORIGINAL_KEYS = frozenset((
    "schema", "occurrence_id", "side", "source_chart_id", "closed_box",
    "adaptive_suffix", "source_binding_sha256", "source_binding_preimage",
    "parent_handoff_id", "refinement_parent_box",
    "refinement_parent_adaptive_suffix", "refinement_decision_chain",
))
HISTORY_ROW_KEYS = frozenset((
    "collision_index", "selected_owner", "evidence_sha256",
    "evidence_preimage",
))
EXACT_FIELDS = (
    "exact_owner", "discriminant", "root_order", "official_word", "chart",
    "wall", "homogeneity", "incidence", "core",
    "structured_terminal_decision_margin",
)
MISSING_GLOBAL_CONTRACT = (
    "PINNED_NO_PRODUCER_IMPORT_ARBITRARY_HISTORY_NUMERIC_REPLAY_AUTHORITY",
    "GLOBAL_FOUR_CHART_FUNDAMENTAL_DOMAIN_ATLAS_WITH_EXACT_QUOTIENT",
    "GLOBAL_FACE_CORNER_SOURCE_GRAZING_GLUE_AND_OWNER_LEDGER",
    "GLOBAL_EXTERIOR_BRANCH_AND_BOUND_LEAF_LEDGER_WITH_UNRESOLVED_ZERO",
    "GLOBAL_COMPONENT_ADJACENCY_RECONSTRUCTION_AND_KNOWN_SHEET_ANCHOR",
    "INDEPENDENT_RECONSTRUCTION_OF_STRICT_CEMETERY_OR_DISCONNECTED_DECISION",
)
FORBIDDEN_SHORTCUT_TOKENS = (
    "BOUNDED_NO_CONTACT",
    "BOUNDED_PILOT",
    "FINITE_HORIZON_NO_CONTACT",
    "NO_CURRENT_CONTACT",
    "NO_CONTACT_WITHIN",
    "CURRENTLY_DISCONNECTED",
    "ENDPOINT_OUTSIDE",
    "LOCAL_CHART_EXIT",
    "CHART_FACE_EXIT",
)
ZERO_CREDIT_KEYS = frozenset(("formal_credit", "D02_credit", "terminal_credit"))


class Rejected(RuntimeError):
    """Fail-closed input, commitment, or publication-boundary rejection."""


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
    answer = copy.deepcopy(value)
    need("object_sha256" not in answer, "object hash absent before close")
    answer["object_sha256"] = digest(answer)
    return answer


def verify_closed(value: Any, label: str) -> None:
    need(
        type(value) is dict
        and type(value.get("object_sha256")) is str
        and HEX64.fullmatch(value["object_sha256"]) is not None,
        label + " closed object",
    )
    body = copy.deepcopy(value)
    claimed = body.pop("object_sha256")
    need(digest(body) == claimed, label + " self hash")


def reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    answer: dict[str, Any] = {}
    for key, value in pairs:
        if key in answer:
            raise Rejected("duplicate JSON key:" + key)
        answer[key] = value
    return answer


def parse_json(raw: bytes, label: str) -> Any:
    need(0 < len(raw) <= 32 << 20, label + " bounded nonempty bytes")
    need(not raw.startswith(b"\xef\xbb\xbf"), label + " no BOM")
    try:
        text = raw.decode("utf-8", "strict")
        return json.loads(
            text,
            object_pairs_hook=reject_duplicate_pairs,
            parse_constant=lambda token: (_ for _ in ()).throw(
                Rejected(label + " non-finite token:" + token)
            ),
        )
    except Rejected:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Rejected(label + " strict JSON:" + str(exc)) from exc


def stable_read(
    path: Path, maximum: int = 32 << 20,
    mutation_hook: Callable[[], None] | None = None,
) -> bytes:
    """Read one regular single-link file and detect name/inode TOCTOU."""

    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    try:
        before = os.fstat(descriptor)
        need(
            stat.S_ISREG(before.st_mode)
            and before.st_nlink == 1
            and 0 < before.st_size <= maximum,
            "query regular single-link bounded file",
        )
        chunks: list[bytes] = []
        remaining = maximum + 1
        while remaining:
            block = os.read(descriptor, min(4 << 20, remaining))
            if not block:
                break
            chunks.append(block)
            remaining -= len(block)
        raw = b"".join(chunks)
        need(len(raw) <= maximum, "query size limit")
        if mutation_hook is not None:
            mutation_hook()
        after = os.fstat(descriptor)
        named = os.stat(path, follow_symlinks=False)

        def fingerprint(item: os.stat_result) -> tuple[int, ...]:
            return (
                item.st_dev, item.st_ino, item.st_mode, item.st_nlink,
                item.st_size, item.st_mtime_ns,
            )

        need(
            fingerprint(before) == fingerprint(after) == fingerprint(named),
            "query TOCTOU/inode/byte stability",
        )
        return raw
    finally:
        os.close(descriptor)


def require_zero_credit_tree(value: Any, label: str, path: str = "$") -> None:
    if type(value) is dict:
        for key, nested in value.items():
            if key in ZERO_CREDIT_KEYS:
                need(nested == 0, label + " zero credit:" + path + "." + key)
            require_zero_credit_tree(nested, label, path + "." + key)
    elif type(value) is list:
        for index, nested in enumerate(value):
            require_zero_credit_tree(nested, label, path + f"[{index}]")


def validate_box(value: Any, label: str) -> None:
    need(type(value) is dict and set(value) == {"t", "p", "s"}, label + " exact box")
    for axis in ("t", "p", "s"):
        interval = value[axis]
        need(
            type(interval) is list and len(interval) == 2
            and all(type(endpoint) is str for endpoint in interval),
            label + " rational interval:" + axis,
        )
        try:
            lower, upper = map(Fraction, interval)
        except (ValueError, ZeroDivisionError) as exc:
            raise Rejected(label + " rational endpoint:" + axis) from exc
        need(lower <= upper, label + " ordered interval:" + axis)


def validate_original_box(value: Any) -> None:
    need(type(value) is dict and set(value) == ORIGINAL_KEYS, "original box exact keys")
    need(
        type(value["schema"]) is str and value["schema"].endswith(".original-box"),
        "original box schema",
    )
    need(
        type(value["occurrence_id"]) is str and value["occurrence_id"] != ""
        and type(value["side"]) is str and value["side"] != ""
        and type(value["source_chart_id"]) is str and value["source_chart_id"] != "",
        "original occurrence/physical-side/chart",
    )
    need(
        type(value["adaptive_suffix"]) is str
        and set(value["adaptive_suffix"]) <= {"0", "1"}
        and type(value["refinement_parent_adaptive_suffix"]) is str
        and set(value["refinement_parent_adaptive_suffix"]) <= {"0", "1"},
        "original adaptive suffixes",
    )
    need(
        type(value["parent_handoff_id"]) is str
        and value["parent_handoff_id"] != ""
        and type(value["refinement_decision_chain"]) is list,
        "original handoff/refinement chain",
    )
    validate_box(value["closed_box"], "original closed")
    validate_box(value["refinement_parent_box"], "original refinement parent")
    source = value["source_binding_preimage"]
    verify_closed(source, "source binding preimage")
    need(
        value["source_binding_sha256"] == source["object_sha256"]
        and source.get("side") == value["side"]
        and source.get("C45_handoff_id") == value["occurrence_id"],
        "original source/side/occurrence binding",
    )
    for ordinal, row in enumerate(value["refinement_decision_chain"]):
        verify_closed(row, f"refinement decision {ordinal}")
        need(row.get("formal_credit") == row.get("D02_credit") == 0,
             f"refinement decision {ordinal} zero credit")


def step_evidence_body(step: dict[str, Any]) -> dict[str, Any]:
    return {
        key: copy.deepcopy(value)
        for key, value in step.items()
        if key not in {"object_sha256", "step_evidence_sha256", "next_handoff"}
    }


def validate_candidate_binding(step: dict[str, Any], label: str) -> None:
    need(all(step.get(field) is not None for field in EXACT_FIELDS),
         label + " all exact fields")
    owner = step["exact_owner"]
    need(
        type(owner) is dict
        and type(owner.get("selected_target_id")) is str
        and OWNER_ID.fullmatch(owner["selected_target_id"]) is not None,
        label + " exact owner",
    )
    root = step["root_order"]
    need(type(root) is dict and root.get("strict") is True, label + " strict root order")
    table = step.get("full_candidate_table")
    rows = table.get("candidate_rows") if type(table) is dict else None
    need(
        type(rows) is list
        and len(rows) == table.get("candidate_count")
        and [row.get("candidate_id") for row in rows]
        == table.get("candidate_ids_in_frozen_order")
        and digest(rows) == table.get("candidate_rows_sha256"),
        label + " candidate count/order/hash",
    )
    need(
        table.get("strict_unique_owner") is True
        and table.get("selected_owner") == owner["selected_target_id"]
        and table.get("selected_discriminant") == step["discriminant"]
        and table.get("root_order") == root,
        label + " owner/discriminant/root-order cross-binding",
    )


def validate_step(step: Any, label: str, *, current: bool) -> None:
    verify_closed(step, label)
    need(
        type(step.get("step_evidence_sha256")) is str
        and HEX64.fullmatch(step["step_evidence_sha256"]) is not None
        and digest(step_evidence_body(step)) == step["step_evidence_sha256"],
        label + " step evidence hash",
    )
    validate_candidate_binding(step, label)
    need(step.get("formal_credit") == step.get("D02_credit") == 0,
         label + " zero credit")
    if current:
        decision = step["structured_terminal_decision_margin"]
        need(
            step.get("status") == decision.get("status") == "PENDING_GLOBAL_ORACLE"
            and decision.get("local_disposition") == "LIVE_CONTINUE"
            and GLOBAL_ORACLE_NAME in decision.get("missing_global_oracles", []),
            label + " live pending global cemetery oracle",
        )


def validate_owner_history(value: Any, original: dict[str, Any]) -> None:
    need(type(value) is list and len(value) >= 2, "owner history length")
    source = original["source_binding_preimage"]
    for index, row in enumerate(value, 1):
        need(type(row) is dict and set(row) == HISTORY_ROW_KEYS,
             f"owner history row {index} exact keys")
        need(
            row["collision_index"] == index
            and type(row["selected_owner"]) is str
            and OWNER_ID.fullmatch(row["selected_owner"]) is not None,
            f"owner history row {index} index/owner",
        )
        preimage = row["evidence_preimage"]
        verify_closed(preimage, f"owner history evidence {index}")
        need(
            preimage.get("collision_index") == index
            and preimage.get("formal_credit") == 0,
            f"owner history evidence {index} binding",
        )
        if index <= 2:
            need(
                row["evidence_sha256"] == preimage["object_sha256"]
                and preimage.get("selected_owner") == row["selected_owner"]
                and preimage.get("source_binding_sha256") == source["object_sha256"]
                and preimage.get("occurrence_id") == original["occurrence_id"],
                f"owner history genesis {index} source continuity",
            )
        else:
            need(
                row["evidence_sha256"] == preimage.get("step_evidence_sha256"),
                f"owner history numeric evidence digest {index}",
            )
            need(preimage.get("owner_history") == value[:index - 1],
                 f"owner history recursive prefix {index}")
            prior_original = preimage.get("original_box")
            validate_original_box(prior_original)
            need(prior_original["source_binding_preimage"] == source,
                 f"owner history source continuity {index}")
            validate_step(preimage, f"owner history numeric step {index}", current=False)
            need(
                preimage["exact_owner"]["selected_target_id"] == row["selected_owner"],
                f"owner history numeric owner {index}",
            )


def validate_attestation(
    value: Any, original_sha: str, history_sha: str,
    current_step: dict[str, Any],
) -> None:
    expected = {
        "schema", "verifier_source_sha256", "verification_object_sha256",
        "original_box_sha256", "owner_history_sha256",
        "current_step_object_sha256", "exact_field_commitments",
        "every_prior_step_numeric_body_replayed",
        "every_split_decision_preimage_replayed", "formal_credit",
        "D02_credit", "object_sha256",
    }
    verify_closed(value, "numeric replay attestation")
    need(set(value) == expected and value["schema"] == ATTESTATION_SCHEMA,
         "numeric replay attestation exact schema/keys")
    need(
        HEX64.fullmatch(value["verifier_source_sha256"]) is not None
        and HEX64.fullmatch(value["verification_object_sha256"]) is not None,
        "numeric replay attestation verifier hashes",
    )
    commitments = value["exact_field_commitments"]
    need(
        type(commitments) is dict and set(commitments) == set(EXACT_FIELDS)
        and all(commitments[field] == digest(current_step[field]) for field in EXACT_FIELDS),
        "numeric replay attestation exact-field commitments",
    )
    need(
        value["original_box_sha256"] == original_sha
        and value["owner_history_sha256"] == history_sha
        and value["current_step_object_sha256"] == current_step["object_sha256"]
        and value["every_prior_step_numeric_body_replayed"] is True
        and value["every_split_decision_preimage_replayed"] is True
        and value["formal_credit"] == value["D02_credit"] == 0,
        "numeric replay attestation occurrence binding",
    )


def validate_occurrence_binding(value: Any) -> None:
    expected = {
        "schema", "occurrence_id", "physical_side", "source_chart_id",
        "original_box", "original_box_sha256", "owner_history",
        "owner_history_sha256", "current_step", "current_step_object_sha256",
        "numeric_replay_attestation",
        "numeric_replay_attestation_object_sha256", "binding_sha256",
    }
    need(type(value) is dict and set(value) == expected and value["schema"] == BINDING_SCHEMA,
         "occurrence binding exact schema/keys")
    body = copy.deepcopy(value)
    claimed = body.pop("binding_sha256")
    need(type(claimed) is str and digest(body) == claimed, "occurrence binding hash")
    original = value["original_box"]
    history = value["owner_history"]
    step = value["current_step"]
    validate_original_box(original)
    validate_owner_history(history, original)
    validate_step(step, "current numeric step", current=True)
    need(
        value["occurrence_id"] == original["occurrence_id"]
        and value["physical_side"] == original["side"]
        and value["source_chart_id"] == original["source_chart_id"],
        "occurrence binding identity echoes",
    )
    original_sha = digest(original)
    history_sha = digest(history)
    need(
        value["original_box_sha256"] == original_sha
        and value["owner_history_sha256"] == history_sha
        and value["current_step_object_sha256"] == step["object_sha256"]
        and step.get("original_box") == original
        and step.get("original_box_sha256") == original_sha
        and step.get("owner_history") == history
        and step.get("owner_history_sha256") == history_sha
        and step.get("collision_index") == len(history) + 1,
        "occurrence original/history/current-step binding",
    )
    attestation = value["numeric_replay_attestation"]
    validate_attestation(attestation, original_sha, history_sha, step)
    need(
        value["numeric_replay_attestation_object_sha256"]
        == attestation["object_sha256"],
        "occurrence attestation hash echo",
    )


def validate_query(value: Any) -> None:
    expected = {
        "schema", "occurrence_binding", "requested_terminal_class",
        "proposed_terminal_certificate", "formal_credit", "D02_credit",
        "object_sha256",
    }
    verify_closed(value, "oracle query")
    need(set(value) == expected and value["schema"] == QUERY_SCHEMA,
         "oracle query exact schema/keys")
    need(
        value["requested_terminal_class"] == REQUESTED_TERMINAL
        and value["formal_credit"] == value["D02_credit"] == 0,
        "oracle query requested class/zero credit",
    )
    validate_occurrence_binding(value["occurrence_binding"])
    certificate = value["proposed_terminal_certificate"]
    if certificate is not None:
        verify_closed(certificate, "proposed terminal certificate")
        require_zero_credit_tree(certificate, "proposed terminal certificate")


def flattened_strings(value: Any) -> list[str]:
    if type(value) is str:
        return [value.upper().replace("-", "_").replace(" ", "_")]
    if type(value) is dict:
        answer: list[str] = []
        for key, nested in value.items():
            answer.extend(flattened_strings(key))
            answer.extend(flattened_strings(nested))
        return answer
    if type(value) is list:
        answer = []
        for nested in value:
            answer.extend(flattened_strings(nested))
        return answer
    return []


def shortcut_tokens(certificate: dict[str, Any] | None) -> list[str]:
    if certificate is None:
        return []
    haystack = "\n".join(flattened_strings(certificate))
    return sorted(token for token in FORBIDDEN_SHORTCUT_TOKENS if token in haystack)


def result_body(
    query: dict[str, Any], status: str, reason: str,
    rejected_shortcuts: list[str],
) -> dict[str, Any]:
    binding = query["occurrence_binding"]
    return {
        "schema": RESULT_SCHEMA,
        "status": status,
        "disposition": "UNRESOLVED",
        "terminal_class": None,
        "strict_terminal_certificate_accepted": False,
        "reason": reason,
        "producer_source_sha256": file_sha(SELF),
        "query_object_sha256": query["object_sha256"],
        "occurrence_binding_sha256": binding["binding_sha256"],
        "occurrence_id": binding["occurrence_id"],
        "physical_side": binding["physical_side"],
        "original_box_sha256": binding["original_box_sha256"],
        "owner_history_sha256": binding["owner_history_sha256"],
        "current_step_object_sha256": binding["current_step_object_sha256"],
        "rejected_nonterminal_shortcuts": rejected_shortcuts,
        "missing_global_oracle_contract": list(MISSING_GLOBAL_CONTRACT),
        "positive_terminal_enabled": False,
        "approved_global_decider_source_sha256": None,
        "bounded_or_no_current_contact_is_terminal": False,
        "formal_credit": 0,
        "D02_credit": 0,
        "terminal_credit": 0,
        "producer_output_is_authority": False,
        "authority_pointer_installed": False,
        "canonical_status_touched": False,
        "writes_performed": False,
    }


def evaluate_query(query: dict[str, Any]) -> dict[str, Any]:
    owned = copy.deepcopy(query)
    validate_query(owned)
    shortcuts = shortcut_tokens(owned["proposed_terminal_certificate"])
    if shortcuts:
        return close_object(result_body(
            owned,
            "REJECTED_NONTERMINAL_SHORTCUT_FAIL_CLOSED",
            "bounded, finite-horizon, local-chart, endpoint, or no-current-contact evidence is not a strict cemetery/disconnected terminal",
            shortcuts,
        ))
    return close_object(result_body(
        owned,
        "PENDING_MISSING_GLOBAL_MATHEMATICAL_ORACLE_FAIL_CLOSED",
        "no pinned independent four-chart exterior BnB/component decider exists; structural hashes and local continuation margins cannot prove global cemetery/disconnection",
        [],
    ))


def contract_document() -> dict[str, Any]:
    return close_object({
        "schema": CONTRACT_SCHEMA,
        "status": "MISSING_GLOBAL_MATHEMATICAL_ORACLE_FAIL_CLOSED",
        "oracle_name": GLOBAL_ORACLE_NAME,
        "producer_source_sha256": file_sha(SELF),
        "accepted_input_scope": (
            "one fully bound physical-side occurrence: frozen original_box + contiguous owner_history + current exact numeric step + independent replay attestation"
        ),
        "structurally_checked_exact_fields": list(EXACT_FIELDS),
        "missing_global_oracle_contract": list(MISSING_GLOBAL_CONTRACT),
        "positive_terminal_enabled": False,
        "approved_global_decider_source_sha256": None,
        "allowed_positive_terminal_class_after_future_decider": REQUESTED_TERMINAL,
        "forbidden_nonterminal_shortcuts": list(FORBIDDEN_SHORTCUT_TOKENS),
        "bounded_or_no_current_contact_is_terminal": False,
        "templates_are_occurrence_proof": False,
        "C35_C36_C37_role": "TEMPLATE_AND_MARGIN_REGRESSION_ONLY",
        "C46_C49_role": "OCCURRENCE_BINDING_AND_LOCAL_CONTINUATION_ONLY",
        "global_decider_minimum_obligations": {
            "four_chart_fundamental_domain_complete": True,
            "face_corner_source_grazing_gluing_complete": True,
            "all_branch_and_bound_leaves_strictly_typed": True,
            "unresolved_leaf_count": 0,
            "component_adjacency_independently_reconstructed": True,
            "known_connected_sheet_anchor_cross_bound": True,
            "every_positive_decision_recomputed_not_boolean_trusted": True,
        },
        "formal_credit": 0,
        "D02_credit": 0,
        "terminal_credit": 0,
        "producer_output_is_authority": False,
        "authority_pointer_installed": False,
        "canonical_status_touched": False,
        "writes_performed": False,
    })


def synthetic_query() -> dict[str, Any]:
    box = {"t": ["0", "1/8"], "p": ["-1/16", "1/16"], "s": ["0", "0"]}
    source = close_object({
        "schema": SCHEMA + ".synthetic-source-binding",
        "C45_handoff_id": "synthetic-physical-side-occurrence",
        "side": "REPRESENTATIVE",
        "closed_source_box": copy.deepcopy(box),
        "formal_credit": 0,
        "D02_credit": 0,
    })
    original = {
        "schema": SCHEMA + ".synthetic.original-box",
        "occurrence_id": source["C45_handoff_id"],
        "side": source["side"],
        "source_chart_id": "W:E",
        "closed_box": copy.deepcopy(box),
        "adaptive_suffix": "",
        "source_binding_sha256": source["object_sha256"],
        "source_binding_preimage": source,
        "parent_handoff_id": source["C45_handoff_id"],
        "refinement_parent_box": copy.deepcopy(box),
        "refinement_parent_adaptive_suffix": "",
        "refinement_decision_chain": [],
    }
    evidence1 = close_object({
        "schema": SCHEMA + ".synthetic-genesis",
        "kind": "FROZEN_COLLISION1_OWNER_AUTHORITY",
        "collision_index": 1,
        "selected_owner": "W[1,0]",
        "source_binding_sha256": source["object_sha256"],
        "occurrence_id": original["occurrence_id"],
        "formal_credit": 0,
        "D02_credit": 0,
    })
    evidence2 = close_object({
        "schema": SCHEMA + ".synthetic-genesis",
        "kind": "COLLISION2_OCCURRENCE_OWNER_BINDING",
        "collision_index": 2,
        "selected_owner": "G[0,0]",
        "source_binding_sha256": source["object_sha256"],
        "occurrence_id": original["occurrence_id"],
        "formal_credit": 0,
        "D02_credit": 0,
    })
    history = [
        {
            "collision_index": 1,
            "selected_owner": evidence1["selected_owner"],
            "evidence_sha256": evidence1["object_sha256"],
            "evidence_preimage": evidence1,
        },
        {
            "collision_index": 2,
            "selected_owner": evidence2["selected_owner"],
            "evidence_sha256": evidence2["object_sha256"],
            "evidence_preimage": evidence2,
        },
    ]
    root_order = {
        "strict": True,
        "ordered_candidate_ids": ["G[0,0]"],
        "minimum_gap": "1/32",
    }
    discriminant = {"target_id": "G[0,0]", "strict_lower_bound": "1/64"}
    candidates = [{
        "candidate_id": "G[0,0]",
        "classification": "STRICT_FUTURE_ROOT",
    }]
    table = {
        "candidate_rows": candidates,
        "candidate_count": 1,
        "candidate_ids_in_frozen_order": ["G[0,0]"],
        "candidate_rows_sha256": digest(candidates),
        "strict_unique_owner": True,
        "selected_owner": "G[0,0]",
        "selected_discriminant": discriminant,
        "root_order": root_order,
    }
    step = {
        "schema": SCHEMA + ".synthetic-step",
        "status": "PENDING_GLOBAL_ORACLE",
        "collision_index": 3,
        "original_box": copy.deepcopy(original),
        "original_box_sha256": digest(original),
        "owner_history": copy.deepcopy(history),
        "owner_history_sha256": digest(history),
        "exact_owner": {"selected_target_id": "G[0,0]"},
        "discriminant": discriminant,
        "root_order": root_order,
        "official_word": {"owner_sequence": ["W[1,0]", "G[0,0]", "G[0,0]"]},
        "chart": {"incoming_chart": "E", "outgoing_chart": "N", "strict": True},
        "wall": {"wall_id": "N", "strict_margin": "1/128"},
        "homogeneity": {"label": "H0_CENTRAL", "strict_margin": "1/256"},
        "incidence": {"incidence_count": 14, "strict": True},
        "core": {"classification": "OUTSIDE_ALL_KNOWN_CORES", "strict": True},
        "structured_terminal_decision_margin": {
            "status": "PENDING_GLOBAL_ORACLE",
            "local_disposition": "LIVE_CONTINUE",
            "local_strict_decision_margin": "1/512",
            "missing_global_oracles": [GLOBAL_ORACLE_NAME],
        },
        "full_candidate_table": table,
        "formal_credit": 0,
        "D02_credit": 0,
        "next_handoff": None,
    }
    step["step_evidence_sha256"] = digest(step_evidence_body(step))
    prior_step = close_object(step)
    history.append({
        "collision_index": 3,
        "selected_owner": prior_step["exact_owner"]["selected_target_id"],
        "evidence_sha256": prior_step["step_evidence_sha256"],
        "evidence_preimage": prior_step,
    })
    step = copy.deepcopy(prior_step)
    step.pop("object_sha256")
    step["collision_index"] = 4
    step["owner_history"] = copy.deepcopy(history)
    step["owner_history_sha256"] = digest(history)
    step["step_evidence_sha256"] = digest(step_evidence_body(step))
    step = close_object(step)
    attestation = close_object({
        "schema": ATTESTATION_SCHEMA,
        "verifier_source_sha256": "a" * 64,
        "verification_object_sha256": "b" * 64,
        "original_box_sha256": digest(original),
        "owner_history_sha256": digest(history),
        "current_step_object_sha256": step["object_sha256"],
        "exact_field_commitments": {
            field: digest(step[field]) for field in EXACT_FIELDS
        },
        "every_prior_step_numeric_body_replayed": True,
        "every_split_decision_preimage_replayed": True,
        "formal_credit": 0,
        "D02_credit": 0,
    })
    binding = {
        "schema": BINDING_SCHEMA,
        "occurrence_id": original["occurrence_id"],
        "physical_side": original["side"],
        "source_chart_id": original["source_chart_id"],
        "original_box": original,
        "original_box_sha256": digest(original),
        "owner_history": history,
        "owner_history_sha256": digest(history),
        "current_step": step,
        "current_step_object_sha256": step["object_sha256"],
        "numeric_replay_attestation": attestation,
        "numeric_replay_attestation_object_sha256": attestation["object_sha256"],
    }
    binding["binding_sha256"] = digest(binding)
    return close_object({
        "schema": QUERY_SCHEMA,
        "occurrence_binding": binding,
        "requested_terminal_class": REQUESTED_TERMINAL,
        "proposed_terminal_certificate": None,
        "formal_credit": 0,
        "D02_credit": 0,
    })


def rejected(action: Callable[[], Any]) -> bool:
    try:
        action()
    except (Rejected, KeyError, ValueError, TypeError, OSError):
        return True
    return False


def reclose_step_query(
    query: dict[str, Any], mutator: Callable[[dict[str, Any]], None],
) -> dict[str, Any]:
    answer = copy.deepcopy(query)
    answer.pop("object_sha256")
    binding = answer["occurrence_binding"]
    binding.pop("binding_sha256")
    step = binding["current_step"]
    step.pop("object_sha256")
    mutator(step)
    step["step_evidence_sha256"] = digest(step_evidence_body(step))
    step["object_sha256"] = digest({
        key: value for key, value in step.items() if key != "object_sha256"
    })
    binding["current_step_object_sha256"] = step["object_sha256"]
    binding["binding_sha256"] = digest(binding)
    return close_object(answer)


def set_certificate(query: dict[str, Any], certificate: dict[str, Any]) -> dict[str, Any]:
    answer = copy.deepcopy(query)
    answer.pop("object_sha256")
    answer["proposed_terminal_certificate"] = close_object(certificate)
    return close_object(answer)


def self_test() -> dict[str, Any]:
    baseline = synthetic_query()
    validate_query(baseline)
    baseline_result = evaluate_query(baseline)

    history_attack = copy.deepcopy(baseline)
    history_attack.pop("object_sha256")
    binding = history_attack["occurrence_binding"]
    binding.pop("binding_sha256")
    binding["owner_history"][0], binding["owner_history"][1] = (
        binding["owner_history"][1], binding["owner_history"][0]
    )
    binding["owner_history_sha256"] = digest(binding["owner_history"])
    binding["binding_sha256"] = digest(binding)
    history_attack = close_object(history_attack)

    owner_attack = reclose_step_query(
        baseline,
        lambda step: step["exact_owner"].__setitem__("selected_target_id", "G[9,9]"),
    )
    root_attack = reclose_step_query(
        baseline,
        lambda step: step["root_order"].__setitem__("minimum_gap", "0"),
    )
    word_attack = reclose_step_query(
        baseline,
        lambda step: step.__setitem__("official_word", {"FORGED": True}),
    )
    chart_attack = reclose_step_query(
        baseline,
        lambda step: step.__setitem__("chart", {"FORGED": True}),
    )
    wall_attack = reclose_step_query(
        baseline,
        lambda step: step.__setitem__("wall", {"FORGED": True}),
    )
    core_attack = reclose_step_query(
        baseline,
        lambda step: step.__setitem__("core", {"FORGED": True}),
    )

    original_attack = copy.deepcopy(baseline)
    original_attack.pop("object_sha256")
    original_binding = original_attack["occurrence_binding"]
    original_binding.pop("binding_sha256")
    original_binding["original_box"]["closed_box"]["t"][0] = "-999"
    original_binding["original_box_sha256"] = digest(original_binding["original_box"])
    original_binding["binding_sha256"] = digest(original_binding)
    original_attack = close_object(original_attack)

    side_attack = copy.deepcopy(baseline)
    side_attack.pop("object_sha256")
    side_binding = side_attack["occurrence_binding"]
    side_binding.pop("binding_sha256")
    side_binding["physical_side"] = "REFLECTED"
    side_binding["binding_sha256"] = digest(side_binding)
    side_attack = close_object(side_attack)

    bounded = set_certificate(baseline, {
        "schema": SCHEMA + ".synthetic-candidate-certificate",
        "claim": "BOUNDED_NO_CONTACT",
        "maximum_checked_collision": 1648,
        "formal_credit": 0,
        "D02_credit": 0,
    })
    no_current = set_certificate(baseline, {
        "schema": SCHEMA + ".synthetic-candidate-certificate",
        "claim": "NO_CURRENT_CONTACT",
        "formal_credit": 0,
        "D02_credit": 0,
    })
    coherent_but_unapproved = set_certificate(baseline, {
        "schema": SCHEMA + ".synthetic-candidate-certificate",
        "claim": "STRICT_GLOBAL_COMPONENT_DISCONNECTION",
        "all_four_charts_claimed": True,
        "unresolved_leaf_count_claimed": 0,
        "formal_credit": 0,
        "D02_credit": 0,
    })
    bounded_result = evaluate_query(bounded)
    no_current_result = evaluate_query(no_current)
    coherent_result = evaluate_query(coherent_but_unapproved)

    toctou_rejected = False
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        path = root / "query.json"
        replacement = root / "replacement.json"
        displaced = root / "displaced.json"
        path.write_bytes(canonical(baseline))
        replacement.write_bytes(canonical(side_attack))

        def swap_name() -> None:
            os.replace(path, displaced)
            os.replace(replacement, path)

        toctou_rejected = rejected(lambda: stable_read(path, mutation_hook=swap_name))

    attacks = {
        "baseline_full_occurrence_binding_validated": True,
        "baseline_terminal_denied_missing_global_math": (
            baseline_result["status"]
            == "PENDING_MISSING_GLOBAL_MATHEMATICAL_ORACLE_FAIL_CLOSED"
            and baseline_result["terminal_class"] is None
        ),
        "history_order_mutation_rejected": rejected(lambda: validate_query(history_attack)),
        "owner_mutation_rejected": rejected(lambda: validate_query(owner_attack)),
        "root_order_mutation_rejected": rejected(lambda: validate_query(root_attack)),
        "official_word_mutation_rejected": rejected(lambda: validate_query(word_attack)),
        "chart_mutation_rejected": rejected(lambda: validate_query(chart_attack)),
        "wall_mutation_rejected": rejected(lambda: validate_query(wall_attack)),
        "core_mutation_rejected": rejected(lambda: validate_query(core_attack)),
        "original_box_mutation_rejected": rejected(lambda: validate_query(original_attack)),
        "physical_side_mutation_rejected": rejected(lambda: validate_query(side_attack)),
        "bounded_no_contact_not_terminal": (
            bounded_result["status"] == "REJECTED_NONTERMINAL_SHORTCUT_FAIL_CLOSED"
            and bounded_result["terminal_class"] is None
        ),
        "no_current_contact_not_terminal": (
            no_current_result["status"] == "REJECTED_NONTERMINAL_SHORTCUT_FAIL_CLOSED"
            and no_current_result["terminal_class"] is None
        ),
        "coherent_unapproved_global_claim_not_terminal": (
            coherent_result["status"]
            == "PENDING_MISSING_GLOBAL_MATHEMATICAL_ORACLE_FAIL_CLOSED"
            and coherent_result["terminal_class"] is None
        ),
        "query_path_TOCTOU_swap_rejected": toctou_rejected,
    }
    need(len(attacks) == 15 and all(attacks.values()), "executed 15/15 hostile tests")
    return close_object({
        "schema": SELF_TEST_SCHEMA,
        "status": "PASS_15_OF_15_EXECUTED_HOSTILE_TESTS_FAIL_CLOSED",
        "producer_source_sha256": file_sha(SELF),
        "attacks": attacks,
        "positive_terminal_enabled": False,
        "terminal_credit": 0,
        "formal_credit": 0,
        "D02_credit": 0,
        "writes_performed": False,
    })


def rejection_result(reason: str) -> dict[str, Any]:
    return close_object({
        "schema": RESULT_SCHEMA,
        "status": "REJECTED_FAIL_CLOSED",
        "disposition": "UNRESOLVED",
        "terminal_class": None,
        "reason": reason,
        "producer_source_sha256": file_sha(SELF),
        "positive_terminal_enabled": False,
        "terminal_credit": 0,
        "formal_credit": 0,
        "D02_credit": 0,
        "producer_output_is_authority": False,
        "authority_pointer_installed": False,
        "canonical_status_touched": False,
        "writes_performed": False,
    })


def emit(value: dict[str, Any]) -> None:
    sys.stdout.buffer.write(canonical(value) + b"\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--contract", action="store_true")
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--query", type=Path)
    args = parser.parse_args()
    try:
        if args.contract:
            emit(contract_document())
        elif args.self_test:
            emit(self_test())
        else:
            query = parse_json(stable_read(args.query), "oracle query")
            emit(evaluate_query(query))
        return 0
    except (Rejected, KeyError, ValueError, TypeError, OSError) as exc:
        emit(rejection_result(str(exc)))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
