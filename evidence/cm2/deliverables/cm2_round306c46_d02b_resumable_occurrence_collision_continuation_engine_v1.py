#!/usr/bin/env python3
"""Zero-credit resumable D02-B occurrence continuation engine.

The engine freezes the complete C45 pair-preserving queue: 7,463 C41
representative rows and both physical sides of every row.  It can evaluate the
frozen C44 collision-3 exact-recenter primitive for a bounded, pair-preserving
selection and materialize every resulting leaf as an occurrence-bound record.

C44 does not provide a frozen occurrence-level collision-4-through-1648 proof
primitive.  This version therefore emits a verifiable continuation interface
and hard PENDING_RESUMABLE states for every live collision-4 handoff.  It never
uses C35--C37 template rows as occurrence proofs, never invents later collision
evidence, never grants terminal or D02 credit, and never writes an authority
pointer, receipt, seal, or canonical status.

Diagnostic shard files are canonical, self-hashed, immutable after creation,
and published with O_EXCL/O_NOFOLLOW plus renameat2(RENAME_NOREPLACE).  A resume
creates a new file linked to its predecessor; no prior shard is overwritten.
"""

from __future__ import annotations

import argparse
from collections import Counter
import copy
import ctypes
import errno
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import stat
import sys
import tempfile
from typing import Any

from flint import ctx
import flint


sys.dont_write_bytecode = True
SELF = Path(__file__).absolute()
ROOT = SELF.parent.parent
DELIVERABLES = SELF.parent
if str(DELIVERABLES) not in sys.path:
    sys.path.insert(0, str(DELIVERABLES))

import cm2_round306c43_collision3_ready_inventory_planner_v1 as c43
import cm2_round306c44_d02b_pair9_collision3_exact_recenter_adaptive_pilot_v1 as c44
import cm2_round306c45_d02b_pair_preserving_batch_runner_planner_v1 as c45


SCHEMA = "cm2.round306c46.d02-b-resumable-occurrence-continuation-engine.v1"
C43_SOURCE_SHA256 = (
    "8519aa02e80ddda01953db9f48c641d88244f264ea67de59307a674c77194b48"
)
C44_SOURCE_SHA256 = (
    "18ba0d94ab8875c2cbbf8c03f727e5fc606dd8f17953df63b480dee766872d28"
)
C45_SOURCE_SHA256 = (
    "bd8937fe5c88b4a77e0eea14ef7fa4fc5e3356458e389a5d4d91e5ae8fb288f6"
)

REPRESENTATIVE_ROWS = 7_463
PHYSICAL_SIDES = 14_926
FIRST_CONTINUATION_COLLISION = 4
LAST_REQUIRED_COLLISION = 1_648
MAX_DIAGNOSTIC_ROWS = 64
MAX_DRY_RUN_ROWS = 2
SIDE_ORDER = ("REFLECTED", "REPRESENTATIVE")
ALLOWED_TERMINALS = (
    "STRICT_EXCLUDED",
    "KNOWN_COMPONENT",
    "STRICT_CEMETERY_OR_DISCONNECTED",
)
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
SAFE_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]*\Z")
ZERO_CREDIT_KEYS = frozenset(("formal_credit", "D02_credit", "terminal_credit"))

SHARD_KEYS = frozenset((
    "schema", "status", "producer_source_sha256", "source_pins",
    "python_flint_version", "arb_precision_bits", "official_registry_sha256",
    "full_queue_manifest", "selection", "predecessor", "execution_bounds",
    "rows", "row_sequence_sha256", "chunk_census", "resume_token",
    "primitive_registry", "allowed_terminal_classes",
    "collision4_through_1648_proof_steps_emitted",
    "template_sampling_used_as_occurrence_proof", "terminal_credit",
    "D02_credit", "formal_credit", "producer_output_is_authority",
    "authority_pointer_installed", "runtime_authority_pointer_touched",
    "writes_performed", "object_sha256",
))

EXECUTION_BOUND_KEYS = frozenset((
    "row_budget", "processed_start_representative_ordinal",
    "processed_stop_representative_ordinal_exclusive",
    "C44_maximum_additional_depth", "C44_maximum_nodes_per_side",
    "full_run_started", "bounded_diagnostic_only",
))

SELECTION_COMPUTED_KEYS = frozenset((
    "selected_physical_sides", "selection_identity_sequence_sha256",
    "first_identity", "last_identity",
    "selection_preserves_both_physical_sides", "side_order",
    "selection_descriptor_sha256",
))

SELECTION_RANGE_KEYS = SELECTION_COMPUTED_KEYS | frozenset((
    "mode", "start_representative_ordinal",
    "stop_representative_ordinal_exclusive", "selected_representative_rows",
))

SELECTION_SHARD_KEYS = SELECTION_RANGE_KEYS | frozenset((
    "shard_index_zero_based", "shard_count",
))

REQUIRED_STEP_FIELDS = (
    "exact_owner",
    "discriminant",
    "root_order",
    "official_word",
    "chart",
    "wall",
    "homogeneity",
    "incidence",
    "core",
    "terminal_margin",
)

MISSING_COLLISION4_PLUS_PRIMITIVES = (
    "FORMAL_ARBITRARY_HISTORY_FULL_BOX_AD_RECENTER_WRAPPER_COLLISION_4_TO_1648",
    "FORMAL_OCCURRENCE_CANDIDATE_DISCRIMINANT_ROOT_ORDER_BINDINGS_COLLISION_4_TO_1648",
    "FORMAL_OCCURRENCE_OFFICIAL_WORD_CHART_WALL_BINDINGS_COLLISION_4_TO_1648",
    "FORMAL_UNBOUNDED_HOMOGENEITY_INCIDENCE_CORE_MARGIN_BINDINGS_COLLISION_4_TO_1648",
    "GLOBAL_CEMETERY_DISCONNECTED_EXTERIOR_TERMINAL_ORACLE",
    "GLOBAL_ADAPTIVE_CODIMENSION_FACE_ENDPOINT_CORNER_OWNER_CLOSURE_COLLISION_4_TO_1648",
)


class Rejected(RuntimeError):
    """Fail-closed diagnostic rejection."""


class PublicationError(Rejected):
    """Publication failure with an explicit durable commit-state bit."""

    def __init__(self, message: str, *, committed: bool) -> None:
        super().__init__(message)
        self.publication_committed = committed


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Rejected(label)


def require_exact_keys(value: Any, expected: frozenset[str], label: str) -> None:
    need(type(value) is dict and set(value) == expected, label + " exact keys")


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def bytes_sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def census(values: list[str]) -> dict[str, int]:
    return dict(sorted(Counter(values).items()))


def line_sequence_sha256(values: list[str]) -> str:
    state = hashlib.sha256()
    for value in values:
        state.update(value.encode("ascii") + b"\n")
    return state.hexdigest()


def stable_read(path: Path, maximum: int, label: str) -> bytes:
    flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    descriptor = os.open(path, flags)
    try:
        before = os.fstat(descriptor)
        need(
            stat.S_ISREG(before.st_mode)
            and before.st_nlink == 1
            and 0 < before.st_size <= maximum,
            "regular single-link bounded:" + label,
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
        after = os.fstat(descriptor)
        named = os.stat(path, follow_symlinks=False)
        fingerprint = lambda item: (
            item.st_dev,
            item.st_ino,
            item.st_mode,
            item.st_nlink,
            item.st_size,
            item.st_mtime_ns,
            item.st_ctime_ns,
        )
        need(
            fingerprint(before) == fingerprint(after) == fingerprint(named)
            and len(raw) == before.st_size <= maximum,
            "stable fd/path read:" + label,
        )
        return raw
    finally:
        os.close(descriptor)


def file_sha(path: Path) -> str:
    return bytes_sha(stable_read(path, 64 << 20, "source:" + str(path)))


def strict_json_bytes(raw: bytes, label: str) -> dict[str, Any]:
    need(raw == raw.strip() + b"\n", "canonical newline:" + label)

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        answer: dict[str, Any] = {}
        for key, value in items:
            need(key not in answer, "duplicate JSON key:" + label + ":" + key)
            answer[key] = value
        return answer

    value = json.loads(
        raw,
        object_pairs_hook=pairs,
        parse_float=lambda token: (_ for _ in ()).throw(
            Rejected("float JSON:" + label + ":" + token)
        ),
        parse_constant=lambda token: (_ for _ in ()).throw(
            Rejected("constant JSON:" + label + ":" + token)
        ),
    )
    need(
        type(value) is dict and canonical(value) + b"\n" == raw,
        "canonical JSON object:" + label,
    )
    return value


def close_object(value: dict[str, Any]) -> dict[str, Any]:
    answer = copy.deepcopy(value)
    need("object_sha256" not in answer, "object not already closed")
    answer["object_sha256"] = digest(answer)
    return answer


def validate_self_hash(value: dict[str, Any], label: str) -> None:
    claimed = value.get("object_sha256")
    body = copy.deepcopy(value)
    body.pop("object_sha256", None)
    need(
        type(claimed) is str
        and HEX64.fullmatch(claimed) is not None
        and claimed == digest(body),
        "self hash:" + label,
    )


def validate_source_pins() -> dict[str, str]:
    observed = {
        "C43_inventory_planner_source_sha256":
            file_sha(Path(c43.__file__).absolute()),
        "C44_collision3_engine_source_sha256":
            file_sha(Path(c44.__file__).absolute()),
        "C45_pair_queue_source_sha256":
            file_sha(Path(c45.__file__).absolute()),
    }
    need(
        observed == {
            "C43_inventory_planner_source_sha256": C43_SOURCE_SHA256,
            "C44_collision3_engine_source_sha256": C44_SOURCE_SHA256,
            "C45_pair_queue_source_sha256": C45_SOURCE_SHA256,
        },
        "frozen C43/C44/C45 source pins",
    )
    return observed


def primitive_registry() -> dict[str, Any]:
    return {
        "collision3_exact_recenter": {
            "status": "AVAILABLE_FROZEN_C44_DIAGNOSTIC_ZERO_CREDIT",
            "source_sha256": C44_SOURCE_SHA256,
            "maximum_collision_index": 3,
        },
        "collision4_through_1648": {
            "status": "MISSING_FORMAL_OCCURRENCE_ENGINE_HARD_PENDING",
            "first_missing_collision_index": FIRST_CONTINUATION_COLLISION,
            "last_required_collision_index": LAST_REQUIRED_COLLISION,
            "missing_primitives": list(MISSING_COLLISION4_PLUS_PRIMITIVES),
            "mathematical_kernels_available_but_not_formal_occurrence_engine": [
                "full_box_AD_and_recenter",
                "candidate_discriminant_and_root_order",
                "official_word_chart_and_wall",
                "most_homogeneity_incidence_core_margin_kernels",
            ],
            "genuinely_missing_global_oracles": [
                "cemetery_disconnected_exterior_terminal_oracle",
                "arbitrary_history_codimension_owner_closure",
            ],
            "existing_kernels_are_unwrapped_unpinned_and_not_occurrence_evidence": True,
            "low_level_callable_functions_are_not_accepted_as_proof": True,
            "templates_cannot_fill_missing_occurrence_evidence": True,
        },
        "terminal_oracles": {
            "KNOWN_COMPONENT_kernel": "AVAILABLE_WITH_STRICT_UNIQUE_CORE_MARGIN",
            "STRICT_EXCLUDED_kernel":
                "TARGET_BOUND_PREFIX_MISMATCH_AVAILABLE_BUT_NOT_WRAPPED",
            "STRICT_CEMETERY_OR_DISCONNECTED":
                "GENUINELY_MISSING_GLOBAL_ORACLE",
        },
        "formal_credit": 0,
        "D02_credit": 0,
    }


def full_queue_context() -> tuple[
    dict[str, Any], list[dict[str, Any]], dict[str, Any], dict[str, Any]
]:
    planner, ordered, bundle = c45.build_queue()
    need(
        planner["representative_ready_rows"] == REPRESENTATIVE_ROWS
        and planner["physical_side_branches"] == PHYSICAL_SIDES
        and planner["all_physical_handoff_ids_unique"] is True
        and planner[
            "every_representative_has_adjacent_complete_two_side_pair"
        ] is True,
        "full C45 queue census and pair preservation",
    )
    c35_result = c43.closed_result(c43.C35)
    c36_result = c43.closed_result(c43.C36)
    c37_result = c43.closed_result(c43.C37)
    template_sequences = {
        "C35_collision_1_to_1648_row_hash_line_sequence_sha256":
            c35_result["ledgers"]["path_occurrences"][
                "row_hash_line_sequence_sha256"
            ],
        "C36_collision_1_to_1648_margin_row_hash_line_sequence_sha256":
            c36_result["ledgers"]["occurrence_margin_bindings"][
                "row_hash_line_sequence_sha256"
            ],
        "C37_reflected_collision_1_to_1648_row_hash_line_sequence_sha256":
            c37_result["ledgers"]["reflected_r1648_occurrences"][
                "row_hash_line_sequence_sha256"
            ],
    }
    need(all(
        type(value) is str and HEX64.fullmatch(value) is not None
        for value in template_sequences.values()
    ), "complete template sequence pins")
    queue_manifest = {
        "schema": SCHEMA + ".full-queue-manifest",
        "representative_ready_rows": REPRESENTATIVE_ROWS,
        "physical_side_branches": PHYSICAL_SIDES,
        "stable_queue_key": [
            "pair_index", "c41_ambient_cell_id", "side", "collision_index"
        ],
        "side_order": list(SIDE_ORDER),
        "representative_key_sequence_sha256":
            planner["representative_key_sequence_sha256"],
        "physical_queue_sequence_sha256":
            planner["physical_queue_sequence_sha256"],
        "physical_handoff_id_line_sequence_sha256":
            planner["physical_handoff_id_line_sequence_sha256"],
        "inventory_authority_inputs": planner["inventory_authority_inputs"],
        "collision3_template_pins": planner["template_pins"],
        "collision_1_to_1648_template_sequence_pins": template_sequences,
        "every_occurrence_requires_independent_exact_binding": True,
        "template_sampling_or_template_credit_forbidden": True,
        "formal_credit": 0,
    }
    queue_manifest["full_queue_manifest_sha256"] = digest(queue_manifest)
    return planner, ordered, bundle, queue_manifest


def selection_descriptor(
    ordered: list[dict[str, Any]],
    start: int,
    stop: int,
    selector: dict[str, Any],
) -> dict[str, Any]:
    base = c45.selected_descriptor(ordered, start, stop, selector)
    answer = {
        **base,
        "selection_preserves_both_physical_sides": True,
        "side_order": list(SIDE_ORDER),
    }
    answer["selection_descriptor_sha256"] = digest(answer)
    return answer


def terminal_margin_evidence(leaf: dict[str, Any]) -> dict[str, Any]:
    certified = leaf.get("terminal_margin")
    if certified is not None:
        return {
            "status": "AVAILABLE_STRICT_TERMINAL_MARGIN",
            "certified_terminal_margin": certified,
            "available_nonterminal_bound": leaf.get("outgoing_chart_margin"),
            "pending_reason": None,
        }
    live_to_collision4 = str(leaf.get("status", "")).startswith(
        "PASS_STRICT_COLLISION3_LIVE_TO_COLLISION4"
    )
    return {
        "status": "PENDING_MARGIN_EVIDENCE",
        "certified_terminal_margin": None,
        "available_nonterminal_bound": leaf.get("outgoing_chart_margin"),
        "pending_reason": (
            "TERMINAL_MARGIN_REQUIRES_COLLISION4_CONTINUATION"
            if live_to_collision4 else
            "TERMINAL_MARGIN_REQUIRES_COLLISION3_ADAPTIVE_CONTINUATION"
        ),
        "next_collision_index": 4 if live_to_collision4 else 3,
        "collision4_handoff_id": leaf.get("collision4_handoff_id"),
        "exact_next_split_decision": leaf.get("next_decision"),
    }


def exact_step_evidence(leaf: dict[str, Any]) -> dict[str, Any]:
    candidate = leaf.get("collision3_candidate_audit", {})
    return {
        "exact_owner": leaf.get("selected_owner"),
        "discriminant": candidate.get("selected_discriminant"),
        "root_order": {
            "certificate": candidate.get("strict_root_order_certificate"),
            "root_order_margin": candidate.get("root_order_margin"),
            "selected_root_isolating_interval":
                leaf.get("selected_root_isolating_interval"),
            "minimum_candidate_decision_margin":
                candidate.get("minimum_candidate_decision_margin"),
        },
        "official_word": leaf.get("official_word"),
        "chart": {
            "incoming_recenter_chart":
                leaf.get("exact_recenter", {}).get("strict_chart"),
            "outgoing_chart": leaf.get("outgoing_chart"),
            "outgoing_chart_margin": leaf.get("outgoing_chart_margin"),
        },
        "wall": leaf.get("wall_and_order_margin"),
        "homogeneity": leaf.get("homogeneity"),
        "incidence": leaf.get("incidence"),
        "core": leaf.get("C24"),
        "terminal_margin": terminal_margin_evidence(leaf),
    }


def missing_exact_fields(evidence: dict[str, Any]) -> list[str]:
    missing = []
    for field in REQUIRED_STEP_FIELDS:
        value = evidence[field]
        if value is None:
            missing.append(field)
    chart = evidence["chart"]
    if chart.get("incoming_recenter_chart") is None:
        missing.append("chart.incoming_recenter_chart")
    if chart.get("outgoing_chart") is None:
        missing.append("chart.outgoing_chart")
    if chart.get("outgoing_chart_margin") is None:
        missing.append("chart.outgoing_chart_margin")
    root = evidence["root_order"]
    if root.get("certificate") is None:
        missing.append("root_order.certificate")
    if root.get("selected_root_isolating_interval") is None:
        missing.append("root_order.selected_root_isolating_interval")
    margin = evidence["terminal_margin"]
    if type(margin) is not dict:
        missing.append("terminal_margin.structured_evidence")
    elif margin.get("status") == "AVAILABLE_STRICT_TERMINAL_MARGIN":
        if margin.get("certified_terminal_margin") is None:
            missing.append("terminal_margin.certified_terminal_margin")
    elif margin.get("status") == "PENDING_MARGIN_EVIDENCE":
        if type(margin.get("pending_reason")) is not str:
            missing.append("terminal_margin.pending_reason")
        if margin.get("available_nonterminal_bound") is None:
            missing.append("terminal_margin.available_nonterminal_bound")
    else:
        missing.append("terminal_margin.status")
    return sorted(set(missing))


def replay_c44_evidence(leaf: dict[str, Any]) -> dict[str, Any]:
    names = leaf.get("collision3_evidence_field_names")
    claimed = leaf.get("collision3_evidence_sha256")
    need(
        type(names) is list
        and all(type(name) is str and name in leaf for name in names)
        and type(claimed) is str
        and HEX64.fullmatch(claimed) is not None,
        "C44 collision3 evidence inventory",
    )
    evidence = {name: leaf[name] for name in names}
    need(digest(evidence) == claimed, "C44 collision3 evidence replay")
    return evidence


def pending_state(
    *,
    queue_manifest_sha256: str,
    selection_sha256: str,
    ordinal: int,
    source: dict[str, Any],
    handoff: dict[str, Any],
    leaf: dict[str, Any],
    margin_evidence: dict[str, Any],
    reason: str,
) -> dict[str, Any]:
    collision_index = (
        FIRST_CONTINUATION_COLLISION
        if leaf.get("collision4_handoff_id") is not None else 3
    )
    history = [
        {
            "collision_index": 1,
            "selected_owner": c44.COLLISION1_OWNER,
            "binding": "FROZEN_C44_INITIAL_COLLISION_OWNER",
        },
        {
            "collision_index": 2,
            "selected_owner": handoff["occurrence_incoming_owner"],
            "binding": handoff[
                "collision2_occurrence_owner_binding_id"
            ],
        },
    ]
    if leaf.get("selected_owner") is not None:
        history.append({
            "collision_index": 3,
            "selected_owner": leaf["selected_owner"],
            "binding": leaf.get("collision3_occurrence_binding_id"),
            "evidence_sha256": leaf.get("collision3_evidence_sha256"),
        })
    identity = {
        "schema": SCHEMA + ".pending-occurrence-identity",
        "full_queue_manifest_sha256": queue_manifest_sha256,
        "selection_descriptor_sha256": selection_sha256,
        "representative_ordinal_zero_based": ordinal,
        "pair_index": source["pair_index"],
        "c41_ambient_cell_id": source["c41_ambient_cell_id"],
        "c41_row_sha256": source["row_sha256"],
        "side": handoff["side"],
        "collision3_handoff_id": handoff["handoff_id"],
        "adaptive_suffix": leaf["adaptive_suffix"],
        "closed_box": leaf["closed_box"],
        "next_collision_index": collision_index,
        "last_required_collision_index": LAST_REQUIRED_COLLISION,
        "collision_owner_history": history,
        "collision4_handoff_id": leaf.get("collision4_handoff_id"),
        "collision4_handoff": leaf.get("collision4_handoff"),
        "exact_next_split_decision": leaf.get("next_decision"),
        "terminal_margin_evidence": margin_evidence,
        "pending_reason": reason,
        "formal_credit": 0,
    }
    return {
        **identity,
        "pending_occurrence_id":
            "c46-pending-occurrence:" + digest(identity),
        "status": "PENDING_RESUMABLE",
        "terminal_class": None,
        "terminal_credit": 0,
        "D02_credit": 0,
    }


def collision3_record(
    *,
    queue_manifest: dict[str, Any],
    selection: dict[str, Any],
    ordinal: int,
    source: dict[str, Any],
    handoff: dict[str, Any],
    leaf: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    status = leaf["status"]
    strict = status.startswith(("STRICT_EARLY_TERMINAL_", "PASS_STRICT_"))
    evidence = exact_step_evidence(leaf)
    c44_replay: dict[str, Any] | None = None
    if strict:
        c44_replay = replay_c44_evidence(leaf)
    live = status.startswith(
        "PASS_STRICT_COLLISION3_LIVE_TO_COLLISION4"
    )
    known = status == "STRICT_EARLY_TERMINAL_KNOWN_COMPONENT"
    need(not strict or live or known, "only recognized strict C44 endpoints")
    missing = missing_exact_fields(evidence)
    if strict:
        need(not missing, "strict C44 step has every required exact field")

    identity = {
        "schema": SCHEMA + ".collision-step-occurrence-identity",
        "full_queue_manifest_sha256":
            queue_manifest["full_queue_manifest_sha256"],
        "selection_descriptor_sha256":
            selection["selection_descriptor_sha256"],
        "representative_ordinal_zero_based": ordinal,
        "pair_index": source["pair_index"],
        "c41_ambient_cell_id": source["c41_ambient_cell_id"],
        "c41_row_sha256": source["row_sha256"],
        "side": handoff["side"],
        "collision_index": 3,
        "adaptive_suffix": leaf["adaptive_suffix"],
        "closed_box": leaf["closed_box"],
        "collision3_handoff_id": handoff["handoff_id"],
    }
    record: dict[str, Any] = {
        **identity,
        "occurrence_step_id": "c46-collision-step:" + digest(identity),
        "C45_collision2_occurrence_owner_binding_id":
            handoff["collision2_occurrence_owner_binding_id"],
        "C44_status": status,
        "C44_collision3_occurrence_binding_id":
            leaf.get("collision3_occurrence_binding_id"),
        "C44_collision3_evidence_sha256":
            leaf.get("collision3_evidence_sha256"),
        "C44_collision3_evidence": c44_replay,
        "exact_step_evidence": evidence,
        "required_exact_step_fields": list(REQUIRED_STEP_FIELDS),
        "missing_exact_step_fields": missing,
        "template_comparison": leaf.get("template_comparison"),
        "template_role":
            "DIAGNOSTIC_HINT_ONLY_NEVER_OCCURRENCE_PROOF",
        "template_sampling_used_as_occurrence_proof": False,
        "formal_credit": 0,
        "terminal_credit": 0,
        "D02_credit": 0,
    }
    pending: dict[str, Any] | None = None
    if known:
        record.update({
            "status": "STRICT_TERMINAL_ZERO_CREDIT",
            "terminal_class": "KNOWN_COMPONENT",
            "terminal_reason": leaf["terminal_reason"],
            "terminal_margin": leaf["terminal_margin"],
        })
    elif live:
        record.update({
            "status": "PENDING_RESUMABLE",
            "terminal_class": None,
            "pending_reason":
                "COLLISION4_TO_1648_OCCURRENCE_PRIMITIVE_MISSING",
        })
        pending = pending_state(
            queue_manifest_sha256=
                queue_manifest["full_queue_manifest_sha256"],
            selection_sha256=selection["selection_descriptor_sha256"],
            ordinal=ordinal,
            source=source,
            handoff=handoff,
            leaf=leaf,
            margin_evidence=evidence["terminal_margin"],
            reason="COLLISION4_TO_1648_OCCURRENCE_PRIMITIVE_MISSING",
        )
    else:
        need(
            status == "BOUNDED_PILOT_UNRESOLVED_WITH_EXACT_NEXT_DECISION"
            and leaf.get("next_decision", {}).get("decision")
            == "SPLIT_AND_RECENTER"
            and type(
                leaf["next_decision"].get("exact_rational_coordinate")
            ) is str,
            "bounded collision3 leaf exact resume decision",
        )
        record.update({
            "status": "PENDING_RESUMABLE",
            "terminal_class": None,
            "pending_reason":
                "COLLISION3_ADAPTIVE_BUDGET_EXHAUSTED_WITH_EXACT_NEXT_DECISION",
        })
        pending = pending_state(
            queue_manifest_sha256=
                queue_manifest["full_queue_manifest_sha256"],
            selection_sha256=selection["selection_descriptor_sha256"],
            ordinal=ordinal,
            source=source,
            handoff=handoff,
            leaf=leaf,
            margin_evidence=evidence["terminal_margin"],
            reason=(
                "COLLISION3_ADAPTIVE_BUDGET_EXHAUSTED_"
                "WITH_EXACT_NEXT_DECISION"
            ),
        )
    return record, pending


def process_row(
    *,
    queue_manifest: dict[str, Any],
    selection: dict[str, Any],
    ordinal: int,
    source: dict[str, Any],
    bundle: dict[str, Any],
    max_depth: int,
    max_nodes: int,
    cores: tuple[Any, ...],
    pair_table: dict[Any, Any],
    pattern_table: dict[Any, Any],
) -> dict[str, Any]:
    handoffs = c45.build_handoffs(source, bundle)
    need(
        [row["side"] for row in handoffs] == list(SIDE_ORDER),
        "complete side handoffs",
    )
    steps: list[dict[str, Any]] = []
    pending: list[dict[str, Any]] = []
    for handoff in handoffs:
        full = c44.pilot_side(
            handoff,
            source,
            max_depth,
            max_nodes,
            cores,
            pair_table,
            pattern_table,
        )
        need(
            full["adaptive_paths_prefix_free"] is True
            and full["relative_Kraft_sum"] == "1",
            "C44 side prefix-free Kraft one",
        )
        for leaf in sorted(
            full["leaves"], key=lambda row: row["adaptive_suffix"]
        ):
            record, resume = collision3_record(
                queue_manifest=queue_manifest,
                selection=selection,
                ordinal=ordinal,
                source=source,
                handoff=handoff,
                leaf=leaf,
            )
            steps.append(record)
            if resume is not None:
                pending.append(resume)
    steps.sort(key=lambda row: (
        row["side"], row["adaptive_suffix"], row["collision_index"]
    ))
    pending.sort(key=lambda row: (
        row["side"], row["adaptive_suffix"], row["next_collision_index"]
    ))
    need(
        {row["side"] for row in steps} == set(SIDE_ORDER),
        "both physical sides materialized",
    )
    terminal = [
        row for row in steps if row["status"] == "STRICT_TERMINAL_ZERO_CREDIT"
    ]
    need(
        all(row["terminal_class"] in ALLOWED_TERMINALS for row in terminal),
        "only three allowed strict terminal classes",
    )
    identity = {
        "representative_ordinal_zero_based": ordinal,
        "pair_index": source["pair_index"],
        "c41_ambient_cell_id": source["c41_ambient_cell_id"],
        "c41_row_sha256": source["row_sha256"],
        "C41_path": source["path"],
    }
    return {
        **identity,
        "row_occurrence_identity_sha256": digest(identity),
        "physical_sides": list(SIDE_ORDER),
        "collision3_step_records": steps,
        "collision3_step_record_sequence_sha256": digest(steps),
        "pending_states": pending,
        "pending_state_id_line_sequence_sha256": line_sequence_sha256([
            row["pending_occurrence_id"] for row in pending
        ]),
        "terminal_records": terminal,
        "terminal_class_census": census([
            row["terminal_class"] for row in terminal
        ]),
        "terminal_credit": 0,
        "D02_credit": 0,
        "formal_credit": 0,
    }


def require_zero_credit_tree(value: Any, label: str, path: str = "$") -> None:
    if type(value) is dict:
        for key, nested in value.items():
            if key in ZERO_CREDIT_KEYS:
                need(nested == 0, label + " nested zero credit:" + path + "." + key)
            if key in {
                "producer_output_is_authority",
                "authority_pointer_installed",
                "runtime_authority_pointer_touched",
                "template_sampling_used_as_occurrence_proof",
            }:
                need(nested is False, label + " nested false lock:" + path + "." + key)
            require_zero_credit_tree(nested, label, path + "." + key)
    elif type(value) is list:
        for index, nested in enumerate(value):
            require_zero_credit_tree(nested, label, path + "[" + str(index) + "]")


def selection_selector(selection: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value for key, value in selection.items()
        if key not in {
            "selected_physical_sides",
            "selection_identity_sequence_sha256",
            "first_identity",
            "last_identity",
            "selection_preserves_both_physical_sides",
            "side_order",
            "selection_descriptor_sha256",
        }
    }


def replay_selection(
    ordered: list[dict[str, Any]], selection: dict[str, Any]
) -> dict[str, Any]:
    need(type(selection) is dict, "resume selection object")
    mode = selection.get("mode")
    if mode == "CONTIGUOUS_PAIR_PRESERVING_RANGE":
        require_exact_keys(selection, SELECTION_RANGE_KEYS, "range selection")
    elif mode == "BALANCED_CONTIGUOUS_PAIR_PRESERVING_SHARD":
        require_exact_keys(selection, SELECTION_SHARD_KEYS, "shard selection")
    else:
        raise Rejected("resume selection mode")
    start = selection.get("start_representative_ordinal")
    stop = selection.get("stop_representative_ordinal_exclusive")
    selected_rows = selection.get("selected_representative_rows")
    need(
        type(start) is int and type(stop) is int
        and 0 <= start < stop <= len(ordered),
        "resume selection bounds",
    )
    need(
        type(selected_rows) is int and selected_rows == stop - start,
        "resume selected representative row count",
    )
    if mode == "BALANCED_CONTIGUOUS_PAIR_PRESERVING_SHARD":
        shard_index = selection.get("shard_index_zero_based")
        shard_count = selection.get("shard_count")
        need(
            type(shard_index) is int and type(shard_count) is int,
            "resume balanced shard integer selector",
        )
        expected_start, expected_stop = c45.balanced_shard_bounds(
            len(ordered), shard_index, shard_count
        )
        need(
            (start, stop) == (expected_start, expected_stop),
            "resume balanced shard exact recomputed bounds",
        )
    replayed = selection_descriptor(
        ordered, start, stop, selection_selector(selection)
    )
    need(replayed == selection, "exact resume selection replay")
    return replayed


RESUME_SUMMARY_FIELDS = (
    "pending_state_chain_sha256",
    "coverage_chain_sha256",
    "cumulative_processed_start_representative_ordinal",
    "cumulative_processed_stop_representative_ordinal_exclusive",
    "cumulative_chunk_count",
)


def resume_summary(token: dict[str, Any]) -> dict[str, Any]:
    summary = {key: token[key] for key in RESUME_SUMMARY_FIELDS}
    need(
        all(
            type(summary[key]) is str
            and HEX64.fullmatch(summary[key]) is not None
            for key in ("pending_state_chain_sha256", "coverage_chain_sha256")
        )
        and type(summary[
            "cumulative_processed_start_representative_ordinal"
        ]) is int
        and type(summary[
            "cumulative_processed_stop_representative_ordinal_exclusive"
        ]) is int
        and type(summary["cumulative_chunk_count"]) is int
        and summary["cumulative_chunk_count"] > 0,
        "resume summary field types",
    )
    return summary


def expected_predecessor_binding(
    predecessor: dict[str, Any], predecessor_file_sha256: str
) -> dict[str, Any]:
    need(
        type(predecessor_file_sha256) is str
        and HEX64.fullmatch(predecessor_file_sha256) is not None,
        "actual predecessor file hash",
    )
    return {
        "object_sha256": predecessor["object_sha256"],
        "file_sha256": predecessor_file_sha256,
        "resume_key_sha256": predecessor["resume_token"][
            "resume_key_sha256"
        ],
        "resume_summary": resume_summary(predecessor["resume_token"]),
    }


def validate_predecessor_link(
    declared: Any,
    *,
    actual_predecessor: dict[str, Any] | None,
    actual_predecessor_file_sha256: str | None,
    actual_predecessor_cursor: int | None,
    declared_start: int,
    selection_start: int,
) -> tuple[str | None, dict[str, Any] | None]:
    if actual_predecessor is None:
        need(
            declared is None
            and actual_predecessor_file_sha256 is None
            and actual_predecessor_cursor is None
            and declared_start == selection_start,
            "explicit resume chain begins with real selection-prefix shard",
        )
        return None, None
    need(
        type(actual_predecessor_file_sha256) is str
        and type(actual_predecessor_cursor) is int,
        "explicit actual predecessor inputs",
    )
    expected = expected_predecessor_binding(
        actual_predecessor, actual_predecessor_file_sha256
    )
    need(
        declared == expected
        and declared_start == actual_predecessor_cursor,
        "declared predecessor exactly matches prior chain file without gap",
    )
    return (
        actual_predecessor["object_sha256"],
        resume_summary(actual_predecessor["resume_token"]),
    )


def read_resume_chain(
    paths: list[Path],
    *,
    ordered: list[dict[str, Any]],
    bundle: dict[str, Any],
    queue_manifest: dict[str, Any],
    source_pins: dict[str, str],
) -> tuple[dict[str, Any], str, int]:
    need(type(paths) is list and bool(paths), "explicit nonempty resume chain")
    seen_paths: set[str] = set()
    seen_file_hashes: set[str] = set()
    seen_object_hashes: set[str] = set()
    predecessor: dict[str, Any] | None = None
    predecessor_file_sha: str | None = None
    predecessor_cursor: int | None = None
    for index, path in enumerate(paths):
        absolute_text = str(path.absolute())
        need(absolute_text not in seen_paths,
             "resume chain path unique:" + str(index))
        seen_paths.add(absolute_text)
        raw = stable_read(path, 512 << 20, "resume chain shard:" + str(index))
        value = strict_json_bytes(raw, "resume chain shard:" + str(index))
        validate_self_hash(value, "resume chain shard:" + str(index))
        file_sha = bytes_sha(raw)
        need(
            file_sha not in seen_file_hashes
            and value["object_sha256"] not in seen_object_hashes,
            "resume chain file and object unique:" + str(index),
        )
        cursor = validate_resume_value(
            value,
            ordered=ordered,
            bundle=bundle,
            queue_manifest=queue_manifest,
            source_pins=source_pins,
            actual_predecessor=predecessor,
            actual_predecessor_file_sha256=predecessor_file_sha,
            actual_predecessor_cursor=predecessor_cursor,
        )
        need(
            value["resume_token"]["cumulative_chunk_count"] == index + 1,
            "resume chain cumulative chunk count equals supplied files",
        )
        seen_file_hashes.add(file_sha)
        seen_object_hashes.add(value["object_sha256"])
        predecessor = value
        predecessor_file_sha = file_sha
        predecessor_cursor = cursor
    need(
        predecessor is not None
        and predecessor_file_sha is not None
        and predecessor_cursor is not None,
        "validated resume chain terminal shard",
    )
    return predecessor, predecessor_file_sha, predecessor_cursor


def build_resume_token(
    *,
    queue_manifest: dict[str, Any],
    selection: dict[str, Any],
    predecessor_object_sha256: str | None,
    predecessor_summary: dict[str, Any] | None,
    process_start_ordinal: int,
    next_ordinal: int,
    stop_ordinal: int,
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    pending_ids = [
        state["pending_occurrence_id"]
        for row in rows for state in row["pending_states"]
    ]
    row_ordinals = [
        row["representative_ordinal_zero_based"] for row in rows
    ]
    need(
        row_ordinals == list(range(process_start_ordinal, next_ordinal)),
        "resume token exact contiguous row ordinals",
    )
    selection_start = selection["start_representative_ordinal"]
    if predecessor_summary is None:
        need(
            predecessor_object_sha256 is None
            and process_start_ordinal == selection_start,
            "resume chain begins exactly at selection start",
        )
        predecessor_pending_chain_sha256 = None
        predecessor_coverage_chain_sha256 = None
        cumulative_start = selection_start
        cumulative_chunks = 1
    else:
        need(
            type(predecessor_object_sha256) is str
            and HEX64.fullmatch(predecessor_object_sha256) is not None,
            "resume predecessor object hash",
        )
        predecessor_summary = resume_summary(predecessor_summary)
        predecessor_pending_chain_sha256 = predecessor_summary[
            "pending_state_chain_sha256"
        ]
        predecessor_coverage_chain_sha256 = predecessor_summary[
            "coverage_chain_sha256"
        ]
        cumulative_start = predecessor_summary[
            "cumulative_processed_start_representative_ordinal"
        ]
        need(
            cumulative_start == selection_start
            and predecessor_summary[
                "cumulative_processed_stop_representative_ordinal_exclusive"
            ] == process_start_ordinal,
            "resume predecessor cumulative coverage is continuous",
        )
        cumulative_chunks = predecessor_summary["cumulative_chunk_count"] + 1
    chain = {
        "predecessor_pending_chain_sha256":
            predecessor_pending_chain_sha256,
        "new_pending_state_ids": pending_ids,
    }
    pending_chain_sha = digest(chain)
    coverage = {
        "predecessor_coverage_chain_sha256":
            predecessor_coverage_chain_sha256,
        "current_processed_start_representative_ordinal":
            process_start_ordinal,
        "current_processed_stop_representative_ordinal_exclusive":
            next_ordinal,
        "current_processed_row_ordinal_line_sequence_sha256":
            line_sequence_sha256([str(value) for value in row_ordinals]),
        "current_row_sequence_sha256": digest(rows),
    }
    coverage_chain_sha = digest(coverage)
    key = {
        "schema": SCHEMA + ".resume-key",
        "full_inventory_physical_queue_sequence_sha256":
            queue_manifest["physical_queue_sequence_sha256"],
        "full_queue_manifest_sha256":
            queue_manifest["full_queue_manifest_sha256"],
        "selection_descriptor_sha256":
            selection["selection_descriptor_sha256"],
        "predecessor_object_sha256": predecessor_object_sha256,
        "predecessor_coverage_chain_sha256":
            predecessor_coverage_chain_sha256,
        "current_processed_start_representative_ordinal":
            process_start_ordinal,
        "next_representative_ordinal_zero_based": next_ordinal,
        "selection_stop_representative_ordinal_exclusive": stop_ordinal,
        "new_pending_state_id_line_sequence_sha256":
            line_sequence_sha256(pending_ids),
        "pending_state_chain_sha256": pending_chain_sha,
        "coverage_chain_sha256": coverage_chain_sha,
        "cumulative_processed_start_representative_ordinal":
            cumulative_start,
        "cumulative_processed_stop_representative_ordinal_exclusive":
            next_ordinal,
        "cumulative_chunk_count": cumulative_chunks,
        "current_processed_row_ordinal_line_sequence_sha256":
            coverage["current_processed_row_ordinal_line_sequence_sha256"],
        "current_row_sequence_sha256": coverage[
            "current_row_sequence_sha256"
        ],
        "collision4_plus_primitive_available": False,
    }
    return {
        **key,
        "resume_key_sha256": digest(key),
    }


def validate_resume_value(
    value: dict[str, Any],
    *,
    ordered: list[dict[str, Any]],
    bundle: dict[str, Any],
    queue_manifest: dict[str, Any],
    source_pins: dict[str, str],
    actual_predecessor: dict[str, Any] | None,
    actual_predecessor_file_sha256: str | None,
    actual_predecessor_cursor: int | None,
) -> int:
    require_exact_keys(value, SHARD_KEYS, "resume shard")
    need(value.get("schema") == SCHEMA, "resume schema")
    need(value.get("status") == "PENDING_RESUMABLE", "resume pending status")
    need(
        value.get("producer_source_sha256") == file_sha(SELF)
        and value.get("source_pins") == source_pins,
        "resume producer and frozen source pins",
    )
    require_zero_credit_tree(value, "resume shard")
    need(
        value.get("formal_credit") == 0
        and value.get("D02_credit") == 0
        and value.get("terminal_credit") == 0
        and value.get("producer_output_is_authority") is False
        and value.get("authority_pointer_installed") is False
        and value.get("runtime_authority_pointer_touched") is False
        and value.get("writes_performed") is True,
        "resume zero-credit published nonauthority",
    )
    need(
        value.get("python_flint_version") == flint.__version__
        and value.get("arb_precision_bits") == ctx.prec,
        "resume arithmetic runtime",
    )
    manifest = value.get("full_queue_manifest")
    need(type(manifest) is dict, "resume queue manifest object")
    manifest_body = copy.deepcopy(manifest)
    claimed_manifest_sha = manifest_body.pop("full_queue_manifest_sha256", None)
    need(
        claimed_manifest_sha == digest(manifest_body)
        and manifest == queue_manifest,
        "resume full queue manifest exact replay",
    )
    selection = replay_selection(ordered, value.get("selection"))
    bounds = value.get("execution_bounds")
    rows = value.get("rows")
    need(type(bounds) is dict and type(rows) is list and bool(rows),
         "resume bounds and nonempty rows")
    require_exact_keys(bounds, EXECUTION_BOUND_KEYS, "resume execution bounds")
    row_budget = bounds.get("row_budget")
    declared_start = bounds.get(
        "processed_start_representative_ordinal"
    )
    declared_stop = bounds.get(
        "processed_stop_representative_ordinal_exclusive"
    )
    max_depth = bounds.get("C44_maximum_additional_depth")
    max_nodes = bounds.get("C44_maximum_nodes_per_side")
    need(
        type(row_budget) is int and 0 < row_budget <= MAX_DIAGNOSTIC_ROWS
        and type(declared_start) is int and type(declared_stop) is int
        and type(max_depth) is int and 0 <= max_depth <= c44.MAX_PILOT_DEPTH
        and type(max_nodes) is int and 2 <= max_nodes <= c44.MAX_PILOT_NODES
        and bounds.get("full_run_started") is False
        and bounds.get("bounded_diagnostic_only") is True,
        "resume exact execution bounds",
    )
    ordinals = [row.get("representative_ordinal_zero_based") for row in rows]
    need(
        all(type(ordinal) is int for ordinal in ordinals)
        and ordinals == list(range(declared_start, declared_stop))
        and declared_stop == min(
            selection["stop_representative_ordinal_exclusive"],
            declared_start + row_budget,
        )
        and selection["start_representative_ordinal"]
        <= declared_start < declared_stop
        <= selection["stop_representative_ordinal_exclusive"],
        "resume actual rows derive exact contiguous cursor",
    )
    predecessor = value.get("predecessor")
    if actual_predecessor is not None:
        need(
            actual_predecessor["selection"] == selection
            and actual_predecessor["full_queue_manifest"] == manifest,
            "resume chain preserves exact selection and full queue",
        )
    (
        predecessor_object_sha256,
        predecessor_resume_summary,
    ) = validate_predecessor_link(
        predecessor,
        actual_predecessor=actual_predecessor,
        actual_predecessor_file_sha256=actual_predecessor_file_sha256,
        actual_predecessor_cursor=actual_predecessor_cursor,
        declared_start=declared_start,
        selection_start=selection["start_representative_ordinal"],
    )
    cores = tuple(c44.RR.core_cert.physical_cores())
    pair_table, pattern_table, registry_sha = (
        c44.RR.component_cert.key_index_tables()
    )
    need(value.get("official_registry_sha256") == registry_sha,
         "resume official registry replay")
    replayed_rows = [
        process_row(
            queue_manifest=queue_manifest,
            selection=selection,
            ordinal=ordinal,
            source=ordered[ordinal],
            bundle=bundle,
            max_depth=max_depth,
            max_nodes=max_nodes,
            cores=cores,
            pair_table=pair_table,
            pattern_table=pattern_table,
        )
        for ordinal in ordinals
    ]
    need(rows == replayed_rows, "resume rows exact frozen-engine replay")
    pending_reasons = [
        state["pending_reason"]
        for row in rows for state in row["pending_states"]
    ]
    expected_census = {
        "representative_rows": len(rows),
        "physical_sides": 2 * len(rows),
        "collision3_occurrence_steps": sum(
            len(row["collision3_step_records"]) for row in rows
        ),
        "strict_allowed_terminals": sum(
            len(row["terminal_records"]) for row in rows
        ),
        "pending_states": sum(
            len(row["pending_states"]) for row in rows
        ),
        "pending_reason_census": census(pending_reasons),
    }
    need(
        value.get("row_sequence_sha256") == digest(rows)
        and value.get("chunk_census") == expected_census,
        "resume row sequence and census replay",
    )
    expected_token = validate_resume_token_against_rows(
        value.get("resume_token"),
        queue_manifest=queue_manifest,
        selection=selection,
        predecessor_object_sha256=predecessor_object_sha256,
        predecessor_summary=predecessor_resume_summary,
        process_start_ordinal=declared_start,
        next_ordinal=declared_stop,
        stop_ordinal=selection["stop_representative_ordinal_exclusive"],
        rows=rows,
    )
    need(
        value.get("primitive_registry") == primitive_registry()
        and value.get("allowed_terminal_classes") == list(ALLOWED_TERMINALS)
        and value.get("collision4_through_1648_proof_steps_emitted") == 0
        and value.get("template_sampling_used_as_occurrence_proof") is False,
        "resume primitive and hard-pending locks",
    )
    return declared_stop


def validate_resume_token_against_rows(
    token: Any,
    *,
    queue_manifest: dict[str, Any],
    selection: dict[str, Any],
    predecessor_object_sha256: str | None,
    predecessor_summary: dict[str, Any] | None,
    process_start_ordinal: int,
    next_ordinal: int,
    stop_ordinal: int,
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    expected = build_resume_token(
        queue_manifest=queue_manifest,
        selection=selection,
        predecessor_object_sha256=predecessor_object_sha256,
        predecessor_summary=predecessor_summary,
        process_start_ordinal=process_start_ordinal,
        next_ordinal=next_ordinal,
        stop_ordinal=stop_ordinal,
        rows=rows,
    )
    need(token == expected,
         "resume token derived only from actual processed rows")
    return expected


def build_plan(
    *,
    queue_manifest: dict[str, Any],
    selection: dict[str, Any],
    source_pins: dict[str, str],
) -> dict[str, Any]:
    return close_object({
        "schema": SCHEMA + ".plan",
        "status": "READY_FOR_BOUNDED_DIAGNOSTIC_SHARDS_ZERO_CREDIT",
        "producer_source_sha256": file_sha(SELF),
        "source_pins": source_pins,
        "full_queue_manifest": queue_manifest,
        "selection": selection,
        "resume_contract": {
            "append_only_predecessor_chain": True,
            "complete_chronological_predecessor_file_chain_required": True,
            "every_predecessor_file_stable_read_and_exact_row_replayed": True,
            "embedded_predecessor_summary_alone_is_never_trusted": True,
            "prior_shards_are_never_modified": True,
            "resume_key_fields": [
                "full_inventory_physical_queue_sequence_sha256",
                "full_queue_manifest_sha256",
                "selection_descriptor_sha256",
                "predecessor_object_sha256",
                "next_representative_ordinal_zero_based",
                "selection_stop_representative_ordinal_exclusive",
                "new_pending_state_id_line_sequence_sha256",
                "pending_state_chain_sha256",
            ],
            "pending_is_not_a_terminal": True,
        },
        "primitive_registry": primitive_registry(),
        "allowed_terminal_classes": list(ALLOWED_TERMINALS),
        "full_run_started": False,
        "terminal_credit": 0,
        "D02_credit": 0,
        "formal_credit": 0,
        "producer_output_is_authority": False,
        "runtime_authority_pointer_touched": False,
        "writes_performed": False,
    })


def build_diagnostic_shard(
    *,
    ordered: list[dict[str, Any]],
    bundle: dict[str, Any],
    queue_manifest: dict[str, Any],
    selection: dict[str, Any],
    source_pins: dict[str, str],
    row_budget: int,
    max_depth: int,
    max_nodes: int,
    predecessor: dict[str, Any] | None,
    predecessor_file_sha256: str | None,
    predecessor_validated_cursor: int | None,
) -> dict[str, Any]:
    selection_start = selection["start_representative_ordinal"]
    selection_stop = selection["stop_representative_ordinal_exclusive"]
    predecessor_object = None
    predecessor_resume_summary = None
    if predecessor is None:
        need(predecessor_validated_cursor is None,
             "no predecessor cursor without predecessor")
        process_start = selection_start
    else:
        need(
            predecessor["full_queue_manifest"][
                "full_queue_manifest_sha256"
            ] == queue_manifest["full_queue_manifest_sha256"]
            and predecessor["selection"]["selection_descriptor_sha256"]
            == selection["selection_descriptor_sha256"],
            "resume queue and selection binding",
        )
        token = predecessor["resume_token"]
        actual_predecessor_cursor = (
            predecessor["rows"][-1]["representative_ordinal_zero_based"] + 1
        )
        need(
            predecessor_validated_cursor == actual_predecessor_cursor
            == token["next_representative_ordinal_zero_based"],
            "resume cursor derives from validated predecessor rows",
        )
        process_start = actual_predecessor_cursor
        predecessor_object = predecessor["object_sha256"]
        predecessor_resume_summary = resume_summary(token)
    need(
        selection_start <= process_start <= selection_stop,
        "resume cursor within selection",
    )
    process_stop = min(selection_stop, process_start + row_budget)
    need(process_start < process_stop, "diagnostic shard has new queue work")

    cores = tuple(c44.RR.core_cert.physical_cores())
    pair_table, pattern_table, registry_sha = (
        c44.RR.component_cert.key_index_tables()
    )
    need(type(registry_sha) is str and HEX64.fullmatch(registry_sha) is not None,
         "official registry hash")
    rows = [
        process_row(
            queue_manifest=queue_manifest,
            selection=selection,
            ordinal=ordinal,
            source=ordered[ordinal],
            bundle=bundle,
            max_depth=max_depth,
            max_nodes=max_nodes,
            cores=cores,
            pair_table=pair_table,
            pattern_table=pattern_table,
        )
        for ordinal in range(process_start, process_stop)
    ]
    pending_count = sum(len(row["pending_states"]) for row in rows)
    terminal_count = sum(len(row["terminal_records"]) for row in rows)
    need(
        all(
            record["formal_credit"] == 0
            for row in rows for record in row["collision3_step_records"]
        ),
        "all occurrence records zero credit",
    )
    resume_token = build_resume_token(
        queue_manifest=queue_manifest,
        selection=selection,
        predecessor_object_sha256=predecessor_object,
        predecessor_summary=predecessor_resume_summary,
        process_start_ordinal=process_start,
        next_ordinal=process_stop,
        stop_ordinal=selection_stop,
        rows=rows,
    )
    pending_reasons = [
        state["pending_reason"]
        for row in rows for state in row["pending_states"]
    ]
    result = {
        "schema": SCHEMA,
        "status": "PENDING_RESUMABLE",
        "producer_source_sha256": file_sha(SELF),
        "source_pins": source_pins,
        "python_flint_version": flint.__version__,
        "arb_precision_bits": ctx.prec,
        "official_registry_sha256": registry_sha,
        "full_queue_manifest": queue_manifest,
        "selection": selection,
        "predecessor": (
            None if predecessor is None else expected_predecessor_binding(
                predecessor, predecessor_file_sha256
            )
        ),
        "execution_bounds": {
            "row_budget": row_budget,
            "processed_start_representative_ordinal": process_start,
            "processed_stop_representative_ordinal_exclusive": process_stop,
            "C44_maximum_additional_depth": max_depth,
            "C44_maximum_nodes_per_side": max_nodes,
            "full_run_started": False,
            "bounded_diagnostic_only": True,
        },
        "rows": rows,
        "row_sequence_sha256": digest(rows),
        "chunk_census": {
            "representative_rows": len(rows),
            "physical_sides": 2 * len(rows),
            "collision3_occurrence_steps": sum(
                len(row["collision3_step_records"]) for row in rows
            ),
            "strict_allowed_terminals": terminal_count,
            "pending_states": pending_count,
            "pending_reason_census": census(pending_reasons),
        },
        "resume_token": resume_token,
        "primitive_registry": primitive_registry(),
        "allowed_terminal_classes": list(ALLOWED_TERMINALS),
        "collision4_through_1648_proof_steps_emitted": 0,
        "template_sampling_used_as_occurrence_proof": False,
        "terminal_credit": 0,
        "D02_credit": 0,
        "formal_credit": 0,
        "producer_output_is_authority": False,
        "authority_pointer_installed": False,
        "runtime_authority_pointer_touched": False,
        "writes_performed": False,
    }
    return close_object(result)


def rename_noreplace_at(
    old_directory_fd: int,
    old_name: str,
    new_directory_fd: int,
    new_name: str,
) -> None:
    libc = ctypes.CDLL(None, use_errno=True)
    renameat2 = getattr(libc, "renameat2", None)
    need(renameat2 is not None, "renameat2 available")
    renameat2.argtypes = (
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_uint,
    )
    renameat2.restype = ctypes.c_int
    ctypes.set_errno(0)
    result = renameat2(
        old_directory_fd,
        old_name.encode("ascii"),
        new_directory_fd,
        new_name.encode("ascii"),
        1,
    )
    if result == 0:
        return
    error = ctypes.get_errno()
    if error in (errno.EEXIST, errno.ENOTEMPTY):
        raise Rejected("append-only output already exists")
    raise OSError(error, os.strerror(error), new_name)


def inode_fingerprint(item: os.stat_result) -> tuple[int, ...]:
    return (
        item.st_dev,
        item.st_ino,
        item.st_mode,
        item.st_uid,
        item.st_gid,
        item.st_nlink,
        item.st_size,
        item.st_mtime_ns,
        item.st_ctime_ns,
    )


def read_open_fd(descriptor: int, maximum: int, label: str) -> bytes:
    before = os.fstat(descriptor)
    need(
        stat.S_ISREG(before.st_mode)
        and before.st_nlink == 1
        and 0 < before.st_size <= maximum,
        "regular singleton open fd:" + label,
    )
    os.lseek(descriptor, 0, os.SEEK_SET)
    chunks: list[bytes] = []
    remaining = maximum + 1
    while remaining:
        block = os.read(descriptor, min(4 << 20, remaining))
        if not block:
            break
        chunks.append(block)
        remaining -= len(block)
    raw = b"".join(chunks)
    after = os.fstat(descriptor)
    need(
        inode_fingerprint(before) == inode_fingerprint(after)
        and len(raw) == before.st_size <= maximum,
        "stable open-fd replay:" + label,
    )
    return raw


def publish_append_only(
    path: Path,
    value: dict[str, Any],
    *,
    _post_rename_test_hook: Any | None = None,
) -> dict[str, Any]:
    """Publish one immutable diagnostic shard.

    The staged inode descriptor remains open across renameat2, and fd/path
    identity is replayed immediately before and after that commit point.  The
    engine never unlinks a stage by name: a pre-commit failure deliberately
    leaves a forensic orphan rather than risking name-replacement deletion.
    Every exception observed after rename, including fd/dir close failures, is
    normalized to PublicationError(publication_committed=True).
    """
    absolute = path.absolute()
    need(
        SAFE_NAME.fullmatch(absolute.name) is not None
        and absolute.suffix == ".json",
        "safe JSON shard basename",
    )
    parent = absolute.parent
    root_flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_DIRECTORY", 0)
    )
    directory_fd: int | None = None
    stage_fd: int | None = None
    stage_name: str | None = None
    committed = False
    result: dict[str, Any] | None = None
    failure: BaseException | None = None
    try:
        directory_fd = os.open(parent, root_flags)
        opened = os.fstat(directory_fd)
        named = os.stat(parent, follow_symlinks=False)
        parent_identity = (opened.st_dev, opened.st_ino)
        need(
            stat.S_ISDIR(opened.st_mode)
            and opened.st_uid == os.getuid()
            and (opened.st_mode & 0o022) == 0
            and inode_fingerprint(opened) == inode_fingerprint(named),
            "private owned output parent fd/path identity",
        )
        try:
            os.stat(absolute.name, dir_fd=directory_fd, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            raise Rejected("append-only output absent")
        validate_self_hash(value, "published shard")
        raw = canonical(value) + b"\n"
        for _attempt in range(8):
            proposed = ".c46-stage-" + secrets.token_hex(24)
            flags = (
                os.O_RDWR
                | os.O_CREAT
                | os.O_EXCL
                | getattr(os, "O_CLOEXEC", 0)
                | getattr(os, "O_NOFOLLOW", 0)
            )
            try:
                stage_fd = os.open(
                    proposed, flags, 0o600, dir_fd=directory_fd
                )
            except FileExistsError:
                continue
            stage_name = proposed
            created = os.fstat(stage_fd)
            need(
                stat.S_ISREG(created.st_mode)
                and created.st_uid == os.getuid()
                and created.st_nlink == 1,
                "fresh owned singleton shard stage",
            )
            view = memoryview(raw)
            while view:
                written = os.write(stage_fd, view)
                need(written > 0, "shard write progress")
                view = view[written:]
            os.fchmod(stage_fd, 0o444)
            os.fsync(stage_fd)
            break
        need(stage_name is not None and stage_fd is not None,
             "fresh shard stage allocated")
        os.fsync(directory_fd)
        replay = read_open_fd(stage_fd, 512 << 20, "staged shard")
        need(replay == raw, "staged shard byte replay")
        staged_fd = os.fstat(stage_fd)
        staged_path = os.stat(
            stage_name, dir_fd=directory_fd, follow_symlinks=False
        )
        need(
            inode_fingerprint(staged_fd) == inode_fingerprint(staged_path)
            and stat.S_ISREG(staged_fd.st_mode)
            and staged_fd.st_nlink == 1
            and staged_fd.st_uid == os.getuid()
            and (staged_fd.st_mode & 0o777) == 0o444,
            "precommit stage fd/path singleton immutable identity",
        )
        terminal_parent = os.stat(parent, follow_symlinks=False)
        need(
            parent_identity
            == (terminal_parent.st_dev, terminal_parent.st_ino),
            "precommit output parent identity",
        )
        try:
            os.stat(
                absolute.name,
                dir_fd=directory_fd,
                follow_symlinks=False,
            )
        except FileNotFoundError:
            pass
        else:
            raise Rejected("precommit append-only output absent")
        rename_noreplace_at(
            directory_fd, stage_name,
            directory_fd, absolute.name,
        )
        committed = True
        final_fd = os.fstat(stage_fd)
        final_path = os.stat(
            absolute.name, dir_fd=directory_fd, follow_symlinks=False
        )
        need(
            inode_fingerprint(final_fd) == inode_fingerprint(final_path)
            and (final_fd.st_dev, final_fd.st_ino)
            == (staged_fd.st_dev, staged_fd.st_ino),
            "postcommit final path is retained stage fd inode",
        )
        need(
            read_open_fd(stage_fd, 512 << 20, "committed shard") == raw,
            "postcommit retained-fd byte replay",
        )
        os.fsync(directory_fd)
        if _post_rename_test_hook is not None:
            _post_rename_test_hook()
        result = {
            "publication_committed": True,
            "commit_point": "renameat2_RENAME_NOREPLACE",
            "output_path": str(absolute),
            "output_file_sha256": bytes_sha(raw),
            "output_object_sha256": value["object_sha256"],
            "committed_inode": {
                "device": final_fd.st_dev,
                "inode": final_fd.st_ino,
            },
            "directory_fsync_after_commit": True,
            "stage_fd_held_across_commit": True,
            "precommit_stage_fd_path_identity": True,
            "postcommit_stage_fd_final_path_identity": True,
            "precommit_and_postcommit_byte_replay": True,
            "precommit_stage_mode": "0444",
            "precommit_failure_stage_policy":
                "LEAVE_FORENSIC_ORPHAN_NEVER_UNLINK_BY_NAME",
            "committed_output_never_removed_by_engine": True,
        }
    except BaseException as error:
        failure = error

    close_failures: list[str] = []
    if stage_fd is not None:
        try:
            os.close(stage_fd)
        except BaseException as error:
            close_failures.append("stage_fd_close:" + repr(error))
    if directory_fd is not None:
        try:
            os.close(directory_fd)
        except BaseException as error:
            close_failures.append("directory_fd_close:" + repr(error))
    if close_failures:
        suffix = ";".join(close_failures)
        if failure is None:
            failure = OSError(suffix)
        else:
            failure = OSError(repr(failure) + ";" + suffix)
    if failure is not None:
        if committed:
            if (
                isinstance(failure, PublicationError)
                and failure.publication_committed
            ):
                raise failure
            raise PublicationError(
                "failure after append-only shard commit:" + repr(failure),
                committed=True,
            ) from failure
        raise failure
    if result is None or not committed:
        raise PublicationError(
            "publication state missing after append-only commit",
            committed=committed,
        )
    return result


def synthetic_pending(side: str) -> dict[str, Any]:
    identity = {
        "schema": SCHEMA + ".pending-occurrence-identity",
        "full_queue_manifest_sha256": "1" * 64,
        "selection_descriptor_sha256": "2" * 64,
        "representative_ordinal_zero_based": 7,
        "pair_index": 9,
        "c41_ambient_cell_id": "ambient",
        "c41_row_sha256": "3" * 64,
        "side": side,
        "collision3_handoff_id": "handoff:" + side,
        "adaptive_suffix": "01",
        "closed_box": {"t": ["0", "1"], "p": ["0", "1"], "s": ["0", "0"]},
        "next_collision_index": 4,
        "last_required_collision_index": LAST_REQUIRED_COLLISION,
        "collision_owner_history": [
            {"collision_index": 1, "selected_owner": "W[1,0]"},
            {"collision_index": 2, "selected_owner": "G[0,1]"},
            {"collision_index": 3, "selected_owner": "G[1,1]"},
        ],
        "collision4_handoff_id": "collision4:" + side,
        "collision4_handoff": {"collision_index": 4},
        "exact_next_split_decision": None,
        "terminal_margin_evidence": {
            "status": "PENDING_MARGIN_EVIDENCE",
            "certified_terminal_margin": None,
            "available_nonterminal_bound": "1/1024",
            "pending_reason":
                "TERMINAL_MARGIN_REQUIRES_COLLISION4_CONTINUATION",
            "next_collision_index": 4,
        },
        "pending_reason": "COLLISION4_TO_1648_OCCURRENCE_PRIMITIVE_MISSING",
        "formal_credit": 0,
    }
    return {
        **identity,
        "pending_occurrence_id":
            "c46-pending-occurrence:" + digest(identity),
        "status": "PENDING_RESUMABLE",
        "terminal_class": None,
        "terminal_credit": 0,
        "D02_credit": 0,
}


def rejects(action: Any) -> bool:
    try:
        action()
    except Rejected:
        return True
    return False


def self_test() -> dict[str, Any]:
    left = synthetic_pending("REFLECTED")
    right = synthetic_pending("REPRESENTATIVE")
    queue = {
        "physical_queue_sequence_sha256": "4" * 64,
        "full_queue_manifest_sha256": "5" * 64,
    }
    selection = {
        "start_representative_ordinal": 7,
        "stop_representative_ordinal_exclusive": 10,
        "selection_descriptor_sha256": "6" * 64,
    }
    rows = [{
        "representative_ordinal_zero_based": 7,
        "pending_states": [left, right],
    }]
    first = build_resume_token(
        queue_manifest=queue,
        selection=selection,
        predecessor_object_sha256=None,
        predecessor_summary=None,
        process_start_ordinal=7,
        next_ordinal=8,
        stop_ordinal=10,
        rows=rows,
    )
    second_rows = [{
        "representative_ordinal_zero_based": 8,
        "pending_states": [left, right],
    }]
    second = build_resume_token(
        queue_manifest=queue,
        selection=selection,
        predecessor_object_sha256="7" * 64,
        predecessor_summary=resume_summary(first),
        process_start_ordinal=8,
        next_ordinal=9,
        stop_ordinal=10,
        rows=second_rows,
    )
    validate_resume_token_against_rows(
        second,
        queue_manifest=queue,
        selection=selection,
        predecessor_object_sha256="7" * 64,
        predecessor_summary=resume_summary(first),
        process_start_ordinal=8,
        next_ordinal=9,
        stop_ordinal=10,
        rows=second_rows,
    )
    nested_credit = copy.deepcopy(rows)
    nested_credit[0]["pending_states"][0]["D02_credit"] = 1
    nested_credit_rejected = rejects(
        lambda: require_zero_credit_tree(nested_credit, "hostile nested credit")
    )
    cursor_skip_rejected = rejects(lambda: build_resume_token(
        queue_manifest=queue,
        selection=selection,
        predecessor_object_sha256=None,
        predecessor_summary=None,
        process_start_ordinal=8,
        next_ordinal=9,
        stop_ordinal=10,
        rows=second_rows,
    ))
    forged_cursor = copy.deepcopy(first)
    forged_cursor["next_representative_ordinal_zero_based"] = 9
    forged_cursor["resume_key_sha256"] = digest({
        key: value for key, value in forged_cursor.items()
        if key != "resume_key_sha256"
    })
    forged_cursor_rejected = rejects(
        lambda: validate_resume_token_against_rows(
            forged_cursor,
            queue_manifest=queue,
            selection=selection,
            predecessor_object_sha256=None,
            predecessor_summary=None,
            process_start_ordinal=7,
            next_ordinal=8,
            stop_ordinal=10,
            rows=rows,
        )
    )
    forged_predecessor = copy.deepcopy(second)
    forged_predecessor["predecessor_object_sha256"] = "8" * 64
    forged_predecessor["resume_key_sha256"] = digest({
        key: value for key, value in forged_predecessor.items()
        if key != "resume_key_sha256"
    })
    forged_predecessor_rejected = rejects(
        lambda: validate_resume_token_against_rows(
            forged_predecessor,
            queue_manifest=queue,
            selection=selection,
            predecessor_object_sha256="7" * 64,
            predecessor_summary=resume_summary(first),
            process_start_ordinal=8,
            next_ordinal=9,
            stop_ordinal=10,
            rows=second_rows,
        )
    )
    forged_summary_skip_rejected = rejects(
        lambda: validate_predecessor_link(
            {
                "object_sha256": "9" * 64,
                "file_sha256": "a" * 64,
                "resume_key_sha256": first["resume_key_sha256"],
                "resume_summary": resume_summary(first),
            },
            actual_predecessor=None,
            actual_predecessor_file_sha256=None,
            actual_predecessor_cursor=None,
            declared_start=8,
            selection_start=7,
        )
    )
    pending_margin = terminal_margin_evidence({
        "status": "PASS_STRICT_COLLISION3_LIVE_TO_COLLISION4_ZERO_CREDIT",
        "terminal_margin": None,
        "outgoing_chart_margin": "1/4096",
        "collision4_handoff_id": "collision4:self-test",
    })
    closed = close_object({
        "schema": SCHEMA + ".synthetic",
        "status": "PENDING_RESUMABLE",
        "formal_credit": 0,
    })
    validate_self_hash(closed, "synthetic")
    primitive = primitive_registry()
    publication_value = close_object({
        "schema": SCHEMA + ".self-test-published-shard",
        "status": "PENDING_RESUMABLE",
        "terminal_credit": 0,
        "D02_credit": 0,
        "formal_credit": 0,
        "producer_output_is_authority": False,
    })
    publication_committed = False
    publication_conflict_rejected_uncommitted = False
    postcommit_failure_classified_committed = False
    retained_fd_identity_replayed = False
    committed_bytes_replayed = False
    temporary_root: Path | None = None
    with tempfile.TemporaryDirectory(prefix="c46-self-test-") as directory:
        temporary_root = Path(directory)
        os.chmod(temporary_root, 0o700)
        first_path = temporary_root / "published.json"
        publication = publish_append_only(first_path, publication_value)
        publication_committed = publication["publication_committed"] is True
        retained_fd_identity_replayed = (
            publication["stage_fd_held_across_commit"] is True
            and publication["precommit_stage_fd_path_identity"] is True
            and publication[
                "postcommit_stage_fd_final_path_identity"
            ] is True
        )
        committed_bytes_replayed = (
            stable_read(first_path, 1 << 20, "self-test committed shard")
            == canonical(publication_value) + b"\n"
        )
        try:
            publish_append_only(first_path, publication_value)
        except Rejected as error:
            publication_conflict_rejected_uncommitted = not bool(
                getattr(error, "publication_committed", False)
            )
        postcommit_path = temporary_root / "postcommit-failure.json"

        def fail_after_rename() -> None:
            raise OSError("injected post-rename self-test failure")

        try:
            publish_append_only(
                postcommit_path,
                publication_value,
                _post_rename_test_hook=fail_after_rename,
            )
        except PublicationError as error:
            postcommit_failure_classified_committed = (
                error.publication_committed is True
                and postcommit_path.exists()
                and stable_read(
                    postcommit_path, 1 << 20,
                    "self-test postcommit retained shard",
                ) == canonical(publication_value) + b"\n"
            )
    temporary_outputs_removed = (
        temporary_root is not None and not temporary_root.exists()
    )

    def persisted_shard(value: dict[str, Any]) -> dict[str, Any]:
        validate_self_hash(value, "self-test shard before persistence")
        need(value["writes_performed"] is False,
             "self-test shard starts as unwritten")
        stored = copy.deepcopy(value)
        stored["writes_performed"] = True
        stored.pop("object_sha256")
        return close_object(stored)

    def reclose_mutation(value: dict[str, Any]) -> dict[str, Any]:
        mutated = copy.deepcopy(value)
        mutated.pop("object_sha256", None)
        return close_object(mutated)

    _, e2e_ordered, e2e_bundle, e2e_queue_manifest = full_queue_context()
    e2e_source_pins = validate_source_pins()
    e2e_start, e2e_stop, e2e_selector = c45.select_bounds(
        len(e2e_ordered), 0, 2, None, None
    )
    e2e_selection = selection_descriptor(
        e2e_ordered, e2e_start, e2e_stop, e2e_selector
    )
    e2e_shard1 = persisted_shard(build_diagnostic_shard(
        ordered=e2e_ordered,
        bundle=e2e_bundle,
        queue_manifest=e2e_queue_manifest,
        selection=e2e_selection,
        source_pins=e2e_source_pins,
        row_budget=1,
        max_depth=0,
        max_nodes=2,
        predecessor=None,
        predecessor_file_sha256=None,
        predecessor_validated_cursor=None,
    ))
    e2e_shard1_roundtrip = False
    e2e_two_shard_chain_roundtrip = False
    missing_prefix_rejected = False
    reversed_chain_rejected = False
    duplicate_chain_rejected = False
    coherent_row_mutation_rejected = False
    coherent_cursor_skip_rejected = False
    top_alias_rejected = False
    bounds_alias_rejected = False
    selection_alias_rejected = False
    range_selected_count_rejected = False
    balanced_shard_index_rejected = False
    balanced_shard_count_rejected = False
    symlink_rejected = False
    hardlink_rejected = False
    e2e_terminal_cursor: int | None = None
    e2e_shard2: dict[str, Any] | None = None
    e2e_temporary_root: Path | None = None
    with tempfile.TemporaryDirectory(prefix="c46-e2e-self-test-") as directory:
        e2e_temporary_root = Path(directory)
        os.chmod(e2e_temporary_root, 0o700)
        shard1_path = e2e_temporary_root / "shard-0001.json"
        shard2_path = e2e_temporary_root / "shard-0002.json"
        publish_append_only(shard1_path, e2e_shard1)

        def read_e2e_chain(
            paths: list[Path],
        ) -> tuple[dict[str, Any], str, int]:
            return read_resume_chain(
                paths,
                ordered=e2e_ordered,
                bundle=e2e_bundle,
                queue_manifest=e2e_queue_manifest,
                source_pins=e2e_source_pins,
            )

        def e2e_chain_rejects(paths: list[Path]) -> bool:
            try:
                read_e2e_chain(paths)
            except (Rejected, OSError):
                return True
            return False

        loaded1, loaded1_file_sha, loaded1_cursor = read_e2e_chain([
            shard1_path
        ])
        e2e_shard1_roundtrip = (
            loaded1 == e2e_shard1
            and loaded1_cursor == 1
            and loaded1["rows"][0][
                "representative_ordinal_zero_based"
            ] == 0
            and loaded1["resume_token"]["cumulative_chunk_count"] == 1
        )
        e2e_shard2 = persisted_shard(build_diagnostic_shard(
            ordered=e2e_ordered,
            bundle=e2e_bundle,
            queue_manifest=e2e_queue_manifest,
            selection=e2e_selection,
            source_pins=e2e_source_pins,
            row_budget=1,
            max_depth=0,
            max_nodes=2,
            predecessor=loaded1,
            predecessor_file_sha256=loaded1_file_sha,
            predecessor_validated_cursor=loaded1_cursor,
        ))
        publish_append_only(shard2_path, e2e_shard2)
        loaded2, loaded2_file_sha, loaded2_cursor = read_e2e_chain([
            shard1_path, shard2_path
        ])
        e2e_terminal_cursor = loaded2_cursor
        e2e_two_shard_chain_roundtrip = (
            loaded2 == e2e_shard2
            and type(loaded2_file_sha) is str
            and HEX64.fullmatch(loaded2_file_sha) is not None
            and loaded2_cursor == 2
            and loaded2["rows"][0][
                "representative_ordinal_zero_based"
            ] == 1
            and loaded2["resume_token"]["cumulative_chunk_count"] == 2
            and loaded2["predecessor"]
            == expected_predecessor_binding(loaded1, loaded1_file_sha)
        )
        missing_prefix_rejected = e2e_chain_rejects([shard2_path])
        reversed_chain_rejected = e2e_chain_rejects([
            shard2_path, shard1_path
        ])
        duplicate_chain_rejected = e2e_chain_rejects([
            shard1_path, shard1_path
        ])

        coherent_row = copy.deepcopy(e2e_shard1)
        coherent_row["rows"][0]["C41_path"] += "0"
        row_identity = {
            "representative_ordinal_zero_based":
                coherent_row["rows"][0][
                    "representative_ordinal_zero_based"
                ],
            "pair_index": coherent_row["rows"][0]["pair_index"],
            "c41_ambient_cell_id":
                coherent_row["rows"][0]["c41_ambient_cell_id"],
            "c41_row_sha256":
                coherent_row["rows"][0]["c41_row_sha256"],
            "C41_path": coherent_row["rows"][0]["C41_path"],
        }
        coherent_row["rows"][0][
            "row_occurrence_identity_sha256"
        ] = digest(row_identity)
        coherent_row_sha = digest(coherent_row["rows"])
        coherent_row["row_sequence_sha256"] = coherent_row_sha
        coherent_row_token = coherent_row["resume_token"]
        coherent_row_token["current_row_sequence_sha256"] = coherent_row_sha
        coherent_row_coverage = {
            "predecessor_coverage_chain_sha256": None,
            "current_processed_start_representative_ordinal": 0,
            "current_processed_stop_representative_ordinal_exclusive": 1,
            "current_processed_row_ordinal_line_sequence_sha256":
                coherent_row_token[
                    "current_processed_row_ordinal_line_sequence_sha256"
                ],
            "current_row_sequence_sha256": coherent_row_sha,
        }
        coherent_row_token["coverage_chain_sha256"] = digest(
            coherent_row_coverage
        )
        coherent_row_token["resume_key_sha256"] = digest({
            key: value for key, value in coherent_row_token.items()
            if key != "resume_key_sha256"
        })
        coherent_row = reclose_mutation(coherent_row)
        coherent_row_path = e2e_temporary_root / "hostile-row.json"
        publish_append_only(coherent_row_path, coherent_row)
        coherent_row_mutation_rejected = e2e_chain_rejects([
            coherent_row_path
        ])

        coherent_cursor = copy.deepcopy(e2e_shard2)
        coherent_cursor["predecessor"] = None
        cursor_rows = coherent_cursor["rows"]
        cursor_pending_ids = [
            state["pending_occurrence_id"]
            for row in cursor_rows for state in row["pending_states"]
        ]
        cursor_row_sha = digest(cursor_rows)
        cursor_ordinal_sha = line_sequence_sha256(["1"])
        cursor_pending_chain_sha = digest({
            "predecessor_pending_chain_sha256": None,
            "new_pending_state_ids": cursor_pending_ids,
        })
        cursor_coverage_sha = digest({
            "predecessor_coverage_chain_sha256": None,
            "current_processed_start_representative_ordinal": 1,
            "current_processed_stop_representative_ordinal_exclusive": 2,
            "current_processed_row_ordinal_line_sequence_sha256":
                cursor_ordinal_sha,
            "current_row_sequence_sha256": cursor_row_sha,
        })
        cursor_token = coherent_cursor["resume_token"]
        cursor_token.update({
            "predecessor_object_sha256": None,
            "predecessor_coverage_chain_sha256": None,
            "current_processed_start_representative_ordinal": 1,
            "next_representative_ordinal_zero_based": 2,
            "new_pending_state_id_line_sequence_sha256":
                line_sequence_sha256(cursor_pending_ids),
            "pending_state_chain_sha256": cursor_pending_chain_sha,
            "coverage_chain_sha256": cursor_coverage_sha,
            "cumulative_processed_start_representative_ordinal": 0,
            "cumulative_processed_stop_representative_ordinal_exclusive": 2,
            "cumulative_chunk_count": 1,
            "current_processed_row_ordinal_line_sequence_sha256":
                cursor_ordinal_sha,
            "current_row_sequence_sha256": cursor_row_sha,
        })
        cursor_token["resume_key_sha256"] = digest({
            key: value for key, value in cursor_token.items()
            if key != "resume_key_sha256"
        })
        coherent_cursor = reclose_mutation(coherent_cursor)
        coherent_cursor_path = e2e_temporary_root / "hostile-cursor.json"
        publish_append_only(coherent_cursor_path, coherent_cursor)
        coherent_cursor_skip_rejected = e2e_chain_rejects([
            coherent_cursor_path
        ])

        top_alias = copy.deepcopy(e2e_shard1)
        top_alias["unresolved_zero"] = True
        top_alias = reclose_mutation(top_alias)
        top_alias_path = e2e_temporary_root / "hostile-top-alias.json"
        publish_append_only(top_alias_path, top_alias)
        top_alias_rejected = e2e_chain_rejects([top_alias_path])

        bounds_alias = copy.deepcopy(e2e_shard1)
        bounds_alias["execution_bounds"]["is_authority"] = True
        bounds_alias = reclose_mutation(bounds_alias)
        bounds_alias_path = e2e_temporary_root / "hostile-bounds-alias.json"
        publish_append_only(bounds_alias_path, bounds_alias)
        bounds_alias_rejected = e2e_chain_rejects([bounds_alias_path])

        selection_alias = copy.deepcopy(e2e_shard1)
        selection_alias["selection"]["start_row_alias"] = 0
        selection_alias["selection"].pop("selection_descriptor_sha256")
        selection_alias["selection"][
            "selection_descriptor_sha256"
        ] = digest(selection_alias["selection"])
        selection_alias = reclose_mutation(selection_alias)
        selection_alias_path = (
            e2e_temporary_root / "hostile-selection-alias.json"
        )
        publish_append_only(selection_alias_path, selection_alias)
        selection_alias_rejected = e2e_chain_rejects([
            selection_alias_path
        ])

        range_count = copy.deepcopy(e2e_shard1)
        range_count["selection"]["selected_representative_rows"] = 999
        range_count["selection"].pop("selection_descriptor_sha256")
        range_count["selection"][
            "selection_descriptor_sha256"
        ] = digest(range_count["selection"])
        range_count = reclose_mutation(range_count)
        range_count_path = (
            e2e_temporary_root / "hostile-range-count.json"
        )
        publish_append_only(range_count_path, range_count)
        range_selected_count_rejected = e2e_chain_rejects([
            range_count_path
        ])

        balanced_shard_count = (len(e2e_ordered) - 1) // 2
        balanced_selection = copy.deepcopy(e2e_selection)
        balanced_selection.update({
            "mode": "BALANCED_CONTIGUOUS_PAIR_PRESERVING_SHARD",
            "shard_index_zero_based": 0,
            "shard_count": balanced_shard_count,
        })
        balanced_selection.pop("selection_descriptor_sha256")
        balanced_selection[
            "selection_descriptor_sha256"
        ] = digest(balanced_selection)
        need(
            c45.balanced_shard_bounds(
                len(e2e_ordered), 0, balanced_shard_count
            ) == (e2e_start, e2e_stop)
            and replay_selection(e2e_ordered, balanced_selection)
            == balanced_selection,
            "self-test coherent balanced selection baseline",
        )

        balanced_index = copy.deepcopy(e2e_shard1)
        balanced_index["selection"] = copy.deepcopy(balanced_selection)
        balanced_index["selection"]["shard_index_zero_based"] = 1
        balanced_index["selection"].pop("selection_descriptor_sha256")
        balanced_index["selection"][
            "selection_descriptor_sha256"
        ] = digest(balanced_index["selection"])
        balanced_index = reclose_mutation(balanced_index)
        balanced_index_path = (
            e2e_temporary_root / "hostile-balanced-index.json"
        )
        publish_append_only(balanced_index_path, balanced_index)
        balanced_shard_index_rejected = e2e_chain_rejects([
            balanced_index_path
        ])

        balanced_count = copy.deepcopy(e2e_shard1)
        balanced_count["selection"] = copy.deepcopy(balanced_selection)
        balanced_count["selection"]["shard_count"] = (
            balanced_shard_count + 1
        )
        balanced_count["selection"].pop("selection_descriptor_sha256")
        balanced_count["selection"][
            "selection_descriptor_sha256"
        ] = digest(balanced_count["selection"])
        balanced_count = reclose_mutation(balanced_count)
        balanced_count_path = (
            e2e_temporary_root / "hostile-balanced-count.json"
        )
        publish_append_only(balanced_count_path, balanced_count)
        balanced_shard_count_rejected = e2e_chain_rejects([
            balanced_count_path
        ])

        symlink_path = e2e_temporary_root / "hostile-symlink.json"
        symlink_path.symlink_to(shard1_path.name)
        symlink_rejected = e2e_chain_rejects([symlink_path])
        hardlink_path = e2e_temporary_root / "hostile-hardlink.json"
        os.link(shard1_path, hardlink_path)
        hardlink_rejected = e2e_chain_rejects([hardlink_path])
        os.unlink(hardlink_path)
    e2e_temporary_outputs_removed = (
        e2e_temporary_root is not None and not e2e_temporary_root.exists()
    )
    temporary_outputs_removed = (
        temporary_outputs_removed and e2e_temporary_outputs_removed
    )
    tests = {
        "full_queue_census_constants":
            REPRESENTATIVE_ROWS == 7_463 and PHYSICAL_SIDES == 14_926,
        "pair_preserving_side_order":
            list(SIDE_ORDER) == sorted(SIDE_ORDER),
        "resume_key_contains_full_queue":
            first["full_inventory_physical_queue_sequence_sha256"]
            == queue["physical_queue_sequence_sha256"],
        "resume_key_self_hash":
            first["resume_key_sha256"] == digest({
                key: value for key, value in first.items()
                if key != "resume_key_sha256"
            }),
        "resume_chain_changes_with_predecessor":
            first["resume_key_sha256"] != second["resume_key_sha256"],
        "resume_chain_contiguous_from_actual_rows":
            second["current_processed_start_representative_ordinal"] == 8
            and second[
                "cumulative_processed_start_representative_ordinal"
            ] == 7
            and second[
                "cumulative_processed_stop_representative_ordinal_exclusive"
            ] == 9
            and second["cumulative_chunk_count"] == 2,
        "nested_credit_forgery_rejected": nested_credit_rejected,
        "first_shard_cursor_skip_rejected": cursor_skip_rejected,
        "self_hashed_cursor_mutation_rejected": forged_cursor_rejected,
        "self_hashed_predecessor_mutation_rejected":
            forged_predecessor_rejected,
        "forged_predecessor_summary_cannot_replace_real_chain_file":
            forged_summary_skip_rejected,
        "physical_sides_have_distinct_occurrence_ids":
            left["pending_occurrence_id"] != right["pending_occurrence_id"],
        "collision4_hard_pending":
            left["status"] == right["status"] == "PENDING_RESUMABLE",
        "pending_is_not_terminal":
            left["terminal_class"] is None
            and right["terminal_class"] is None,
        "collision4_plus_primitive_explicitly_missing":
            primitive["collision4_through_1648"]["status"]
            == "MISSING_FORMAL_OCCURRENCE_ENGINE_HARD_PENDING",
        "all_missing_primitives_named":
            len(primitive["collision4_through_1648"]["missing_primitives"])
            == len(MISSING_COLLISION4_PLUS_PRIMITIVES) == 6,
        "registry_distinguishes_math_kernels_from_missing_global_oracles":
            len(primitive["collision4_through_1648"][
                "mathematical_kernels_available_but_not_formal_occurrence_engine"
            ]) == 4
            and len(primitive["collision4_through_1648"][
                "genuinely_missing_global_oracles"
            ]) == 2
            and primitive["collision4_through_1648"][
                "existing_kernels_are_unwrapped_unpinned_and_not_occurrence_evidence"
            ] is True,
        "low_level_callable_not_proof":
            primitive["collision4_through_1648"][
                "low_level_callable_functions_are_not_accepted_as_proof"
            ] is True,
        "template_sampling_forbidden":
            primitive["collision4_through_1648"][
                "templates_cannot_fill_missing_occurrence_evidence"
            ] is True,
        "only_three_terminal_classes":
            ALLOWED_TERMINALS == (
                "STRICT_EXCLUDED",
                "KNOWN_COMPONENT",
                "STRICT_CEMETERY_OR_DISCONNECTED",
            ),
        "required_step_field_contract_complete":
            set(REQUIRED_STEP_FIELDS) == {
                "exact_owner", "discriminant", "root_order",
                "official_word", "chart", "wall", "homogeneity",
                "incidence", "core", "terminal_margin",
            },
        "live_terminal_margin_is_explicit_pending_evidence":
            pending_margin["status"] == "PENDING_MARGIN_EVIDENCE"
            and pending_margin["available_nonterminal_bound"] == "1/4096"
            and pending_margin["pending_reason"]
            == "TERMINAL_MARGIN_REQUIRES_COLLISION4_CONTINUATION",
        "collision_range_exact":
            FIRST_CONTINUATION_COLLISION == 4
            and LAST_REQUIRED_COLLISION == 1_648,
        "append_only_filename_policy":
            SAFE_NAME.fullmatch("shard-0001.json") is not None
            and SAFE_NAME.fullmatch("../bad.json") is None,
        "self_hash_replay": closed["object_sha256"] == digest({
            key: value for key, value in closed.items()
            if key != "object_sha256"
        }),
        "credit_locked_zero":
            left["formal_credit"] == left["terminal_credit"]
            == left["D02_credit"] == 0,
        "authority_fields_absent_from_pending":
            all("authority" not in key.lower() for key in left),
        "append_only_publication_committed": publication_committed,
        "append_only_conflict_rejected_uncommitted":
            publication_conflict_rejected_uncommitted,
        "postcommit_failure_classified_committed":
            postcommit_failure_classified_committed,
        "stage_fd_and_inode_identity_replayed": retained_fd_identity_replayed,
        "committed_bytes_replayed": committed_bytes_replayed,
        "e2e_full_queue_shard1_publish_and_resume":
            e2e_shard1_roundtrip,
        "e2e_full_queue_two_shard_chain_publish_and_resume":
            e2e_two_shard_chain_roundtrip,
        "e2e_missing_prefix_shard_rejected": missing_prefix_rejected,
        "e2e_reversed_chain_rejected": reversed_chain_rejected,
        "e2e_duplicate_chain_rejected": duplicate_chain_rejected,
        "e2e_coherent_row_mutation_rejected":
            coherent_row_mutation_rejected,
        "e2e_coherent_cursor_skip_rejected":
            coherent_cursor_skip_rejected,
        "e2e_top_unknown_semantic_alias_rejected": top_alias_rejected,
        "e2e_bounds_unknown_semantic_alias_rejected":
            bounds_alias_rejected,
        "e2e_selection_unknown_semantic_alias_rejected":
            selection_alias_rejected,
        "e2e_range_selected_row_count_mismatch_rejected":
            range_selected_count_rejected,
        "e2e_balanced_shard_index_bounds_mismatch_rejected":
            balanced_shard_index_rejected,
        "e2e_balanced_shard_count_bounds_mismatch_rejected":
            balanced_shard_count_rejected,
        "e2e_symlink_rejected": symlink_rejected,
        "e2e_hardlink_rejected": hardlink_rejected,
        "temporary_publication_outputs_removed": temporary_outputs_removed,
    }
    need(len(tests) == 48 and all(tests.values()), "48 hostile contract tests")
    return close_object({
        "schema": SCHEMA + ".self-test",
        "status": "PASS_48_OF_48_END_TO_END_HOSTILE_RESUME_AND_PUBLICATION_TESTS",
        "source_pins": validate_source_pins(),
        "tests": tests,
        "end_to_end": {
            "selection_representative_rows": 2,
            "published_shards": 2,
            "terminal_cursor": e2e_terminal_cursor,
            "first_shard_object_sha256": e2e_shard1["object_sha256"],
            "second_shard_object_sha256": (
                None if e2e_shard2 is None else e2e_shard2["object_sha256"]
            ),
            "full_queue_manifest_sha256": e2e_queue_manifest[
                "full_queue_manifest_sha256"
            ],
            "temporary_outputs_removed": e2e_temporary_outputs_removed,
        },
        "primitive_registry": primitive,
        "full_run_started": False,
        "terminal_credit": 0,
        "D02_credit": 0,
        "formal_credit": 0,
        "producer_output_is_authority": False,
        "runtime_authority_pointer_touched": False,
        "temporary_self_test_writes_performed": True,
        "temporary_self_test_outputs_removed": temporary_outputs_removed,
        "persistent_writes_performed": False,
        "writes_performed": True,
    })


def emit(value: dict[str, Any]) -> None:
    sys.stdout.buffer.write(canonical(value) + b"\n")
    sys.stdout.buffer.flush()


def rejection_payload(
    error: Exception, output: Path | None = None
) -> dict[str, Any]:
    committed = bool(getattr(error, "publication_committed", False))
    return close_object({
        "schema": SCHEMA + ".rejection",
        "status": "REJECTED_FAIL_CLOSED_ZERO_CREDIT",
        "error_type": type(error).__name__,
        "error": str(error),
        "publication_committed": committed,
        "committed_output_path": (
            str(output.absolute()) if committed and output is not None else None
        ),
        "full_run_started": False,
        "terminal_credit": 0,
        "D02_credit": 0,
        "formal_credit": 0,
        "producer_output_is_authority": False,
        "runtime_authority_pointer_touched": False,
        "writes_performed": committed,
    })


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--plan", action="store_true")
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--run-shard", action="store_true")
    parser.add_argument("--start-row", type=int)
    parser.add_argument("--row-count", type=int)
    parser.add_argument("--shard-index", type=int)
    parser.add_argument("--shard-count", type=int)
    parser.add_argument("--row-budget", type=int, default=1)
    parser.add_argument("--max-depth", type=int, default=0)
    parser.add_argument("--max-nodes", type=int, default=2)
    parser.add_argument(
        "--resume-from",
        type=Path,
        nargs="+",
        metavar="SHARD",
        help=(
            "complete chronological predecessor shard chain; every file is "
            "stable-read and replayed, ending at the shard to resume"
        ),
    )
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    publication_committed = False
    publication_metadata: dict[str, Any] | None = None
    try:
        need(
            flint.__version__ == "0.9.0" and ctx.prec == 384,
            "python-flint 0.9.0 at 384 bits",
        )
        source_pins = validate_source_pins()
        if arguments.self_test:
            need(
                all(value is None for value in (
                    arguments.start_row,
                    arguments.row_count,
                    arguments.shard_index,
                    arguments.shard_count,
                    arguments.resume_from,
                    arguments.output,
                )),
                "self-test takes no selection, resume, or output",
            )
            emit(self_test())
            return 0

        need(
            0 <= arguments.max_depth <= c44.MAX_PILOT_DEPTH,
            "bounded C44 max depth",
        )
        need(
            2 <= arguments.max_nodes <= c44.MAX_PILOT_NODES,
            "bounded C44 max nodes",
        )
        need(
            type(arguments.row_budget) is int
            and 0 < arguments.row_budget <= MAX_DIAGNOSTIC_ROWS,
            "bounded positive row budget",
        )
        planner, ordered, bundle, queue_manifest = full_queue_context()
        predecessor = None
        predecessor_file_sha = None
        predecessor_validated_cursor = None
        if arguments.resume_from is not None:
            need(
                all(value is None for value in (
                    arguments.start_row,
                    arguments.row_count,
                    arguments.shard_index,
                    arguments.shard_count,
                )),
                "resume derives selection from predecessor",
            )
            (
                predecessor,
                predecessor_file_sha,
                predecessor_validated_cursor,
            ) = read_resume_chain(
                arguments.resume_from,
                ordered=ordered,
                bundle=bundle,
                queue_manifest=queue_manifest,
                source_pins=source_pins,
            )
            prior_selection = predecessor["selection"]
            start = prior_selection["start_representative_ordinal"]
            stop = prior_selection["stop_representative_ordinal_exclusive"]
            selector = selection_selector(prior_selection)
        else:
            start, stop, selector = c45.select_bounds(
                len(ordered),
                arguments.start_row,
                arguments.row_count,
                arguments.shard_index,
                arguments.shard_count,
            )
        selection = selection_descriptor(
            ordered, start, stop, selector
        )
        if predecessor is not None:
            need(
                selection == predecessor["selection"],
                "exact predecessor selection replay",
            )

        if arguments.plan:
            need(
                arguments.resume_from is None
                and arguments.output is None,
                "plan has no resume or output",
            )
            emit(build_plan(
                queue_manifest=queue_manifest,
                selection=selection,
                source_pins=source_pins,
            ))
            return 0

        if arguments.dry_run:
            need(arguments.output is None, "dry-run writes no output")
            need(
                min(stop, start + arguments.row_budget) - start
                <= MAX_DRY_RUN_ROWS,
                "dry-run maximum two representative rows",
            )
        else:
            need(arguments.output is not None, "run-shard output required")

        result = build_diagnostic_shard(
            ordered=ordered,
            bundle=bundle,
            queue_manifest=queue_manifest,
            selection=selection,
            source_pins=source_pins,
            row_budget=arguments.row_budget,
            max_depth=arguments.max_depth,
            max_nodes=arguments.max_nodes,
            predecessor=predecessor,
            predecessor_file_sha256=predecessor_file_sha,
            predecessor_validated_cursor=predecessor_validated_cursor,
        )
        if arguments.dry_run:
            emit(result)
        else:
            stored = copy.deepcopy(result)
            stored["writes_performed"] = True
            stored.pop("object_sha256")
            stored["object_sha256"] = digest(stored)
            need(
                validate_source_pins() == source_pins
                and stored["producer_source_sha256"] == file_sha(SELF),
                "terminal source reattestation before publication",
            )
            publication_metadata = publish_append_only(
                arguments.output, stored
            )
            publication_committed = True
            emit(close_object({
                "schema": SCHEMA + ".publication-receipt",
                "status": "COMMITTED_APPEND_ONLY_DIAGNOSTIC_ZERO_CREDIT",
                "published_shard": {
                    "path": str(arguments.output.absolute()),
                    "file_sha256": publication_metadata[
                        "output_file_sha256"
                    ],
                    "object_sha256": stored["object_sha256"],
                },
                "publication": publication_metadata,
                "terminal_credit": 0,
                "D02_credit": 0,
                "formal_credit": 0,
                "producer_output_is_authority": False,
                "runtime_authority_pointer_touched": False,
                "writes_performed": True,
            }))
        return 0
    except Exception as error:
        committed = publication_committed or bool(
            getattr(error, "publication_committed", False)
        )
        if committed and not bool(
            getattr(error, "publication_committed", False)
        ):
            error = PublicationError(
                "failure after append-only shard commit:" + repr(error),
                committed=True,
            )
        payload = rejection_payload(error, arguments.output)
        try:
            emit(payload)
        except Exception:
            try:
                os.write(2, canonical(payload) + b"\n")
            except Exception:
                pass
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
