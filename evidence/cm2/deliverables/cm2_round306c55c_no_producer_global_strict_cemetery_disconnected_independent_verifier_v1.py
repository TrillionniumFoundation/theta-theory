#!/usr/bin/env python3
"""Cold, no-producer boundary for the C55 global strict decider.

The verifier consumes the C55-A leaf/glue ledgers and the C55-B
component/known-sheet ledger strictly as inert JSON.  It never imports or
executes either producer.  A positive strict result is possible only after an
independent row census, glue reconstruction, component reconstruction and
anchor/exterior reconstruction all agree over exactly 76,832 rows with zero
unresolved rows.  Every incomplete real input therefore fails closed.

This file is evidence tooling only.  It never writes runtime state, installs
an authority, or grants formal/D02 credit.
"""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
from typing import Any, Callable, Iterable
import zlib


sys.dont_write_bytecode = True
SELF = Path(__file__).absolute()
WORKSPACE = SELF.parent.parent
DELIVERABLES = SELF.parent

SCHEMA = (
    "cm2.round306c55c.no-producer-global-strict-cemetery-disconnected-"
    "independent-verifier.v1"
)
CONTRACT_SCHEMA = SCHEMA + ".closed-input-contract"
VERIFICATION_SCHEMA = SCHEMA + ".verification"
ROW_PROJECTION_SCHEMA = SCHEMA + ".independent-row-projection"
REQUESTED_TERMINAL = "STRICT_CEMETERY_OR_DISCONNECTED"

UNIVERSE_SIZE = 76_832
EFFECTIVE_CHECKPOINT = (
    "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
)
PREDECESSOR_ID = (
    "10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41"
)
C53_HEAD_BASENAME = "predecessor-" + PREDECESSOR_ID + ".seal"
C53_HEAD_PATH = (
    WORKSPACE / ".cm2-runtime" / "cm2-global-authority-heads" /
    C53_HEAD_BASENAME
)
C53_HEAD_FILE_SHA256 = (
    "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3"
)
C53_HEAD_OBJECT_SHA256 = (
    "cb90ab914c3b6518384669f42d05df33c21a717596190131c6a0f5683934cbfb"
)

A_LEAF_BASENAME = (
    "cm2_round306c55a_four_chart_fundamental_domain_bnb_leaf_ledger_v1.json"
)
A_GLUE_BASENAME = (
    "cm2_round306c55a_four_chart_fundamental_domain_exact_glue_ledger_v1.json"
)
B_RESULT_BASENAME = (
    "cm2_round306c55b_global_component_adjacency_known_sheet_result_v1.json"
)
P0_CONTRACT_BASENAME = "cm2_round306c55p0_global_strict_decider_input_contract_v1.json"
A_LEAF_PATH = DELIVERABLES / A_LEAF_BASENAME
A_GLUE_PATH = DELIVERABLES / A_GLUE_BASENAME
B_RESULT_PATH = DELIVERABLES / B_RESULT_BASENAME
P0_CONTRACT_PATH = DELIVERABLES / P0_CONTRACT_BASENAME
P0_CONTRACT_FILE_SHA256 = (
    "0e2a7b713f3c4c007c65a27a42079ca33b024b8489b5dfd149312fcd5702333b"
)
A_LEAF_FILE_SHA256 = "e80c012e3260e8f9e68d5858ba5d9dafd94611e2a1c1200d787a20e3842d8db6"
A_LEAF_OBJECT_SHA256 = "7dd4c19cfb2b9f8cd30a4a9a23e30f11734e856cc6cc5a04e9a169c051059d90"
A_GLUE_FILE_SHA256 = "d91dbc92c76fc8f004ff795c008d3a7b3e5716e6e6287a39798ba7331ecae00b"
A_GLUE_OBJECT_SHA256 = "b9a9a3fd6a18ac50d7141cc9e351364d5fe35edb6bdcb4b2126aaeec5c745cef"
B_RESULT_FILE_SHA256 = "6bf9cae7b4b422c5c2121f95828e1508700fe1a5d1b1128598c8617f65032a93"
B_RESULT_OBJECT_SHA256 = "1ce396e9746d3c0364325e8308e94c9dcd4a3bfbba8c17a9c9961915e807cc56"
B_CELL_FILE_SHA256 = "123a742ed553d89fd1026cf65c64879d9a92916492b5b583888c3312551ca2ce"
B_EDGE_FILE_SHA256 = "23ea0b4419f155f62d32b6b73c5a16c6f402884d333c222ff803899a58da29a0"
B_COMPONENT_FILE_SHA256 = "bebc49f66efb01c0b980ec10258a60d7aead9d4d2006d28bdd169c9a9ae38a04"
B_CELL_BASENAME = (
    "cm2_round306c55b_global_component_adjacency_known_sheet_"
    "cell_component_crosswalk_v1.jsonl.gz"
)
B_EDGE_BASENAME = (
    "cm2_round306c55b_global_component_adjacency_known_sheet_"
    "component_edges_and_glue_v1.jsonl.gz"
)
B_COMPONENT_BASENAME = (
    "cm2_round306c55b_global_component_adjacency_known_sheet_"
    "ordinary_components_v1.jsonl.gz"
)
B_CELL_PATH = DELIVERABLES / B_CELL_BASENAME
B_EDGE_PATH = DELIVERABLES / B_EDGE_BASENAME
B_COMPONENT_PATH = DELIVERABLES / B_COMPONENT_BASENAME

LEGAL_DISPOSITIONS = (
    "EARLIEST_PREFIX_EXCLUDED",
    "TYPED_EVENT_GRAPH",
    "CONNECTED_TO_KNOWN",
    "SOURCE_GRAZING_OR_CEMETERY",
)
UNRESOLVED_CLASS = "UNRESOLVED_R1648_CONTINUATION"
HEX64 = re.compile(r"[0-9a-f]{64}\Z")

A_LEAF_TOP_KEYS = frozenset((
    "authority_binding", "blocker_partition", "blocker_rows", "census",
    "leaf_order", "leaves", "object_sha256", "proof_policy", "schema",
    "source_assets", "status",
))
A_LEAF_KEYS = frozenset((
    "anchor_or_exterior_proof", "bnb_state", "c34_frontier_row_sha256",
    "cell_id", "component_ref", "exact_box", "glue_refs", "leaf_ordinal",
    "origin_key", "physical_chart", "proof_ref", "reflection_pair_ref",
    "row_sha256", "schema", "source_cell_row_sha256",
    "terminal_disposition", "unresolved_reason",
))
A_GLUE_REF_KEYS = frozenset((
    "intra_face_ordinals", "source_grazing_corner_ordinals",
    "source_grazing_face_ordinals", "source_seam_ordinals",
))
A_GLUE_TOP_KEYS = frozenset((
    "authority_binding", "coverage", "exact_gluing_model", "glue_rows",
    "object_sha256", "row_order", "schema", "source_assets", "status",
))
A_GLUE_FAMILIES = (
    "intra_faces", "source_grazing_corners", "source_grazing_faces",
    "source_seams",
)
A_AUTHORITY_KEYS = frozenset((
    "C32_object_sha256", "C33_object_sha256", "C34_object_sha256",
    "C37_object_sha256", "C53_effective_checkpoint_object_sha256",
    "C53_global_head_file_sha256", "C53_global_head_object_sha256",
    "C53_global_head_path", "C53_independent_audit_object_sha256",
))
A_CENSUS_KEYS = frozenset((*LEGAL_DISPOSITIONS, UNRESOLVED_CLASS, "total", "unresolved_zero"))
A_BLOCKER_PARTITION_KEYS = frozenset((
    "by_primary_residual_classification", "global_requirement_blockers",
    "new_terminals_by_C55A", "remaining_unresolved",
))
A_PROOF_POLICY_KEYS = frozenset((
    "allowed_terminal_dispositions", "depth_cap_terminal_forbidden",
    "geometric_grazing_is_dynamic_cemetery_credit", "local_chart_exit_is_terminal",
    "null_disposition_rule", "positive_exterior_requires_unresolved_zero",
    "reusable_rule_order", "reusable_rule_sequence_sha256",
))
A_EXACT_BOX_KEYS = frozenset((
    "physical_p_interval", "physical_slice", "physical_t_interval",
))
A_ANCHOR_PROOF_KEYS = frozenset((
    "C34_seed_crosswalk_sha256", "C50b_contract_object_sha256", "kind",
    "known_anchor_status", "strict_exterior_decider_object_sha256",
))
A_BNB_STATE_KEYS = frozenset((
    "base_leaf_is_full_continuation_proof", "blocker_row_id",
    "current_after_nonterminal_leaf_count", "current_after_unresolved_parent_volume",
    "depth_cap_terminal_used", "pair_index", "reusable_rule_sequence_sha256",
))
A_PROOF_REF_KEYS = frozenset((
    "C34_typed_event_row_sha256", "C53_parent_projection_object_sha256",
    "authority", "primary_evidence_row_sha256",
))
A_COMPONENT_REF_KEYS = frozenset((
    "cell_role", "component_id", "component_index", "component_row_sha256",
))
A_REFLECTION_REF_KEYS = frozenset((
    "C37_row_sha256", "pair_index", "partner_cell_id", "role",
))
A_BLOCKER_ROW_KEYS = frozenset((
    "blocker_row_id", "c37_reflection_row_sha256", "c42_parent_row_sha256",
    "c53_projection_object_sha256", "current_nonterminal_leaf_count",
    "current_unresolved_parent_volume", "global_missing_requirement_ids",
    "pair_index", "primary_residual_classification", "reflected_cell_id",
    "representative_cell_id", "residual_classification_census",
    "residual_source_row_sha256s", "row_sha256", "schema",
))
A_GLUE_COVERAGE_KEYS = frozenset((
    "all_corner_cells_exist", "all_face_cells_exist", "cell_count",
    "corner_count", "grazing_face_count", "intra_face_count",
    "leaf_glue_refs_bidirectional", "source_grazing_boundary_complete",
    "source_seam_count", "source_seam_cyclic_span_complete",
    "unexpected_or_missing_cell_reference_count",
))
A_GLUE_ROW_KEYS = {
    "intra_faces": frozenset((
        "axis", "classification", "compact_chart", "coordinate", "dimension",
        "face_id", "negative_cell_id", "ordinal", "positive_cell_id",
        "row_sha256", "source_row_sha256", "span",
    )),
    "source_seams": frozenset((
        "classification", "dimension", "exact_state_gluing_inherited_from_round162",
        "face_id", "left_cell_id", "left_chart", "left_compact_endpoint",
        "ordinal", "physical_p_span", "right_cell_id", "right_chart",
        "right_compact_endpoint", "row_sha256", "seam_id", "source_row_sha256",
        "terminal",
    )),
    "source_grazing_faces": frozenset((
        "classification", "compact_chart", "compact_q", "dimension", "face_id",
        "incident_cell_id", "ordinal", "physical_p", "physical_t_span",
        "round144_dynamic_cemetery_credit", "row_sha256", "source_row_sha256",
        "terminal_for_compact_geometry",
    )),
    "source_grazing_corners": frozenset((
        "classification", "compact_q", "corner_id", "dimension", "left_cell_id",
        "ordinal", "physical_p", "right_cell_id",
        "round144_dynamic_cemetery_credit", "row_sha256", "seam_id",
        "source_row_sha256", "terminal_for_compact_geometry",
    )),
}
B_TOP_KEYS = frozenset((
    "C53_effective_authority", "authority_pins", "base_atlas_census",
    "credit_locks", "current_effective_census", "exact_unresolved_partition",
    "forbidden_shortcuts", "global_closure_proved", "inventory",
    "known_sheet_anchor_census", "ledgers", "object_sha256",
    "reconstruction_invariants", "required_next", "schema", "status",
    "strict_decider_eligible", "unresolved_zero",
))
B_C53_KEYS = frozenset((
    "authority_role", "current_four_class_census",
    "effective_checkpoint_object_sha256", "head_file_sha256",
    "head_object_sha256", "head_path",
))
B_LEDGER_NAMES = (
    "cell_component_crosswalk", "component_edges_and_glue", "ordinary_components",
)
B_LEDGER_DESCRIPTOR_KEYS = frozenset((
    "filename", "order", "row_count", "row_hash_line_sequence_sha256",
    "sha256", "size",
))
B_CELL_KEYS = frozenset((
    "C32_cell_row_sha256", "C33_crosswalk_row_sha256",
    "C34_component_row_sha256", "C37_pair_row_sha256",
    "C42_parent_row_sha256", "C53_parent_projection_object_sha256",
    "D02_gate_credit", "cell_id", "compact_chart", "component_id",
    "component_index", "coordinate_or_key_coincidence_used",
    "current_effective_disposition", "gate3_chart", "gate3_product_box",
    "known_sheet_anchor_role", "newly_whole_by_C53_pair_seal", "origin_key",
    "pair_index", "physical_p_interval", "physical_slice", "physical_t_interval",
    "reflection_partner_cell_id", "row_sha256", "schema",
    "whole_cell_connected_to_known_credit", "whole_pair_terminal_after_C53",
))
B_EDGE_KEYS = frozenset((
    "coordinate_or_key_coincidence_used", "dimension", "exact_geometry",
    "face_or_corner_id", "glue_kind", "gluing_proof_kind", "left_cell_id",
    "left_disposition", "ordinary_component_indices", "right_cell_id",
    "right_disposition", "row_sha256", "schema", "scope", "terminal_credit",
    "typed_event_binding_row_sha256", "upstream_row_sha256",
))
B_EDGE_BASE_KEYS = B_EDGE_KEYS - {"typed_event_binding_row_sha256"}
B_COMPONENT_KEYS = frozenset((
    "C34_component_row_sha256", "D02_gate_credit",
    "anchor_is_strict_subset_not_whole_component", "cell_count",
    "common_refinement_status", "component_id", "component_index",
    "coordinate_or_key_coincidence_used", "current_excluded_cell_count",
    "current_excluded_cell_ids_sha256", "current_unresolved_cell_count",
    "current_unresolved_cell_ids_sha256", "edge_and_glue_row_sequence_sha256",
    "edge_and_glue_row_sha256s", "internal_face_connected", "known_sheet_anchor",
    "member_cell_ids", "member_cell_ids_sha256", "member_cell_row_sequence_sha256",
    "member_cell_row_sha256s", "positive_area_anchor_proof_present", "row_sha256",
    "schema", "singleton_isolation_promoted", "unresolved_reason",
    "whole_component_connected_to_known_credit", "whole_component_terminal_class",
))


class Rejected(RuntimeError):
    """Fail-closed structural, semantic, or publication-boundary rejection."""


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def bytes_sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def verifier_source_sha256() -> str:
    return bytes_sha(SELF.read_bytes())


def close_object(value: dict[str, Any], hash_key: str = "object_sha256") -> dict[str, Any]:
    answer = copy.deepcopy(value)
    need(hash_key not in answer, "hash absent before close:" + hash_key)
    answer[hash_key] = digest(answer)
    return answer


def verify_closed(value: Any, label: str, hash_key: str = "object_sha256") -> None:
    need(type(value) is dict, label + " object")
    claimed = value.get(hash_key)
    need(type(claimed) is str and HEX64.fullmatch(claimed) is not None,
         label + " closed hash")
    body = copy.deepcopy(value)
    body.pop(hash_key)
    need(digest(body) == claimed, label + " self hash")


def exact_keys(value: Any, keys: frozenset[str], label: str) -> None:
    need(type(value) is dict and frozenset(value) == keys, label + " closed keys")


def reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    answer: dict[str, Any] = {}
    for key, value in pairs:
        if key in answer:
            raise Rejected("duplicate JSON key:" + key)
        answer[key] = value
    return answer


def parse_json(
    raw: bytes, label: str, maximum: int = 256 << 20,
    require_canonical: bool = True,
) -> Any:
    need(0 < len(raw) <= maximum, label + " bounded nonempty bytes")
    need(not raw.startswith(b"\xef\xbb\xbf"), label + " no BOM")
    try:
        value = json.loads(
            raw.decode("utf-8", "strict"),
            object_pairs_hook=reject_duplicate_pairs,
            parse_constant=lambda token: (_ for _ in ()).throw(
                Rejected(label + " non-finite token:" + token)
            ),
        )
    except Rejected:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Rejected(label + " strict JSON:" + str(exc)) from exc
    if require_canonical:
        need(raw == canonical(value) + b"\n", label + " canonical ASCII bytes")
    return value


def _stat_fingerprint(item: os.stat_result) -> tuple[int, ...]:
    return (
        item.st_dev, item.st_ino, item.st_mode, item.st_nlink, item.st_uid,
        item.st_gid, item.st_size, item.st_mtime_ns, item.st_ctime_ns,
    )


def stable_read_bundle(
    paths: Iterable[Path], maximum: int = 256 << 20,
    mutation_hook: Callable[[], None] | None = None,
) -> dict[Path, bytes]:
    """Hold every descriptor while reading and detect file/directory swaps."""

    ordered = tuple(paths)
    need(bool(ordered) and len(set(ordered)) == len(ordered), "unique bundle paths")
    directory_fds: dict[Path, int] = {}
    directory_before: dict[Path, os.stat_result] = {}
    file_fds: dict[Path, int] = {}
    file_before: dict[Path, os.stat_result] = {}
    try:
        for path in ordered:
            need(path.is_absolute(), "bundle path absolute")
            parent = path.parent
            if parent not in directory_fds:
                flags = (
                    os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) |
                    getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
                )
                directory_fds[parent] = os.open(parent, flags)
                before = os.fstat(directory_fds[parent])
                need(stat.S_ISDIR(before.st_mode), "bundle parent directory")
                directory_before[parent] = before
            need(path.name not in ("", ".", "..") and "/" not in path.name,
                 "strict bundle basename")
            flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
            descriptor = os.open(path.name, flags, dir_fd=directory_fds[parent])
            before = os.fstat(descriptor)
            need(
                stat.S_ISREG(before.st_mode) and before.st_nlink == 1
                and 0 < before.st_size <= maximum
                and before.st_uid == os.getuid()
                and before.st_mode & stat.S_IWOTH == 0,
                "bundle regular owner-controlled single-link bounded file",
            )
            file_fds[path] = descriptor
            file_before[path] = before

        raw_by_path: dict[Path, bytes] = {}
        for path in ordered:
            descriptor = file_fds[path]
            chunks: list[bytes] = []
            remaining = maximum + 1
            while remaining:
                block = os.read(descriptor, min(4 << 20, remaining))
                if not block:
                    break
                chunks.append(block)
                remaining -= len(block)
            raw = b"".join(chunks)
            need(len(raw) <= maximum, "bundle read size")
            raw_by_path[path] = raw

        if mutation_hook is not None:
            mutation_hook()

        for path in ordered:
            parent = path.parent
            after = os.fstat(file_fds[path])
            named = os.stat(path.name, dir_fd=directory_fds[parent], follow_symlinks=False)
            need(
                _stat_fingerprint(file_before[path])
                == _stat_fingerprint(after)
                == _stat_fingerprint(named),
                "bundle file TOCTOU/inode/byte stability",
            )
        for parent, descriptor in directory_fds.items():
            after = os.fstat(descriptor)
            named = os.stat(parent, follow_symlinks=False)
            need(
                _stat_fingerprint(directory_before[parent])
                == _stat_fingerprint(after)
                == _stat_fingerprint(named),
                "bundle directory TOCTOU/inode stability",
            )
        return raw_by_path
    finally:
        for descriptor in file_fds.values():
            os.close(descriptor)
        for descriptor in directory_fds.values():
            os.close(descriptor)


def verify_c53_head(value: Any, raw: bytes) -> None:
    need(bytes_sha(raw) == C53_HEAD_FILE_SHA256, "C53 head file pin")
    verify_closed(value, "C53 head", "authority_seal_object_sha256")
    need(value["authority_seal_object_sha256"] == C53_HEAD_OBJECT_SHA256,
         "C53 head object pin")
    need(value.get("authority_role") == "GLOBAL_COMPOSITE", "C53 global role")
    need(value.get("predecessor_identity_sha256") == PREDECESSOR_ID,
         "C53 predecessor pin")
    need(value.get("post_seal_effective_checkpoint_object_sha256") == EFFECTIVE_CHECKPOINT,
         "C53 effective checkpoint pin")
    need(value.get("semantic_commit", {}).get("this_predecessor_keyed_global_head_is_only_semantic_commit") is True,
         "C53 semantic commit")
    scope = value.get("formal_scope")
    need(type(scope) is dict and scope.get("D02_gate_credit") == 0,
         "C53 zero D02 gate credit")
    after = scope.get("D02_four_class_after")
    need(type(after) is dict and after == {
        "CONNECTED_TO_KNOWN": 0,
        "EARLIEST_PREFIX_EXCLUDED": 75_388,
        "SOURCE_GRAZING_OR_CEMETERY": 0,
        "TYPED_EVENT_GRAPH": 296,
        UNRESOLVED_CLASS: 1_148,
        "total": UNIVERSE_SIZE,
    }, "C53 exact four-class census")


def verify_p0_contract(value: Any, raw: bytes) -> None:
    need(bytes_sha(raw) == P0_CONTRACT_FILE_SHA256, "P0 contract file pin")
    need(type(value) is dict, "P0 contract object")
    need(value.get("schema") == "cm2.round306c55p0.global-strict-decider-input-contract.v1",
         "P0 contract schema")
    authority = value.get("authority_input")
    need(type(authority) is dict, "P0 authority input")
    need(authority.get("head_file_sha256") == C53_HEAD_FILE_SHA256,
         "P0 C53 head file pin")
    need(authority.get("head_object_sha256") == C53_HEAD_OBJECT_SHA256,
         "P0 C53 head object pin")
    need(authority.get("effective_checkpoint_object_sha256") == EFFECTIVE_CHECKPOINT,
         "P0 C53 checkpoint pin")
    census = value.get("formal_input_census")
    need(census == {
        "EARLIEST_PREFIX_EXCLUDED": 75_388,
        "TYPED_EVENT_GRAPH": 296,
        "CONNECTED_TO_KNOWN": 0,
        "SOURCE_GRAZING_OR_CEMETERY": 0,
        UNRESOLVED_CLASS: 1_148,
        "total": UNIVERSE_SIZE,
    }, "P0 formal census")
    row_contract = value.get("closed_row_contract")
    need(type(row_contract) is dict and row_contract.get("row_count") == UNIVERSE_SIZE,
         "P0 exact row universe")
    need(row_contract.get("legal_terminal_dispositions") == list(LEGAL_DISPOSITIONS),
         "P0 legal disposition order")
    positive = row_contract.get("positive_acceptance")
    need(type(positive) is dict and positive.get("unresolved_zero") is True,
         "P0 unresolved-zero gate")
    nonpromotion = value.get("strict_nonpromotion")
    need(type(nonpromotion) is dict
         and nonpromotion.get("formal_credit") == 0
         and nonpromotion.get("D02_gate_credit") == 0
         and nonpromotion.get("CM2") == "NO-GO_FOR_CLAIM",
         "P0 zero-credit nonpromotion")


def authority_checkpoint(value: Any, label: str) -> str | None:
    """Extract only an explicit C53 effective-checkpoint binding."""

    if type(value) is not dict:
        return None
    candidates: list[Any] = []
    for key in (
        "effective_checkpoint_object_sha256",
        "post_seal_effective_checkpoint_object_sha256",
        "C53_effective_checkpoint_object_sha256",
    ):
        if key in value:
            candidates.append(value[key])
    nested = value.get("C53_global_composite")
    if type(nested) is dict:
        for key in (
            "effective_checkpoint_object_sha256",
            "post_seal_effective_checkpoint_object_sha256",
        ):
            if key in nested:
                candidates.append(nested[key])
    if not candidates:
        return None
    need(all(item == candidates[0] for item in candidates), label + " checkpoint agreement")
    return candidates[0] if type(candidates[0]) is str else None


def validate_row_hash(row: Any, label: str) -> None:
    verify_closed(row, label, "row_sha256")


def ordered_unique_ints(value: Any, label: str) -> tuple[int, ...]:
    need(type(value) is list and all(type(item) is int and item >= 0 for item in value),
         label + " nonnegative integer list")
    answer = tuple(value)
    need(answer == tuple(sorted(set(answer))), label + " ordered unique")
    return answer


def row_projection(row: dict[str, Any]) -> dict[str, Any]:
    exact_keys(row, A_LEAF_KEYS, "A leaf row")
    validate_row_hash(row, "A leaf row")
    need(type(row["leaf_ordinal"]) is int and row["leaf_ordinal"] >= 0,
         "A leaf ordinal")
    need(type(row["cell_id"]) is str and row["cell_id"] != "", "A cell id")
    need(type(row["physical_chart"]) is str and row["physical_chart"] != "",
         "A physical chart")
    exact_keys(row["exact_box"], A_EXACT_BOX_KEYS, "A exact box")
    refs = row["glue_refs"]
    exact_keys(refs, A_GLUE_REF_KEYS, "A glue refs")
    normalized_refs = {
        key: list(ordered_unique_ints(refs[key], "A glue refs " + key))
        for key in sorted(A_GLUE_REF_KEYS)
    }
    disposition = row["terminal_disposition"]
    reason = row["unresolved_reason"]
    if disposition is None:
        need(type(reason) is str and reason.strip() == reason and reason != "",
             "A unresolved iff explicit reason")
    else:
        need(disposition in LEGAL_DISPOSITIONS, "A legal terminal disposition")
        need(reason is None, "A terminal iff unresolved reason null")
    component_ref = row["component_ref"]
    need(component_ref is None or type(component_ref) is dict, "A component ref shape")
    if component_ref is not None:
        exact_keys(component_ref, A_COMPONENT_REF_KEYS, "A component ref")
        need(type(component_ref["component_id"]) is str and component_ref["component_id"] != "",
             "A component id")
        need(type(component_ref["component_index"]) is int and component_ref["component_index"] >= 0,
             "A component index")
        need(type(component_ref["component_row_sha256"]) is str
             and HEX64.fullmatch(component_ref["component_row_sha256"]) is not None,
             "A component row hash")

    anchor = row["anchor_or_exterior_proof"]
    exact_keys(anchor, A_ANCHOR_PROOF_KEYS, "A anchor/exterior proof")
    need(anchor["kind"] in {
        "KNOWN_ANCHOR_STRICT_SUBSET_ONLY", "NO_POSITIVE_ANCHOR_OR_EXTERIOR_PROOF",
    }, "A anchor/exterior proof enum")

    bnb = row["bnb_state"]
    exact_keys(bnb, A_BNB_STATE_KEYS, "A bnb state")
    need(bnb["depth_cap_terminal_used"] is False, "A depth cap never terminal")

    proof_ref = row["proof_ref"]
    exact_keys(proof_ref, A_PROOF_REF_KEYS, "A proof ref")
    need(proof_ref["authority"] in ("C34_FRONTIER", "C53_GLOBAL_COMPOSITE", None),
         "A proof authority enum")

    reflection = row["reflection_pair_ref"]
    need(reflection is None or type(reflection) is dict, "A reflection ref shape")
    if reflection is not None:
        exact_keys(reflection, A_REFLECTION_REF_KEYS, "A reflection ref")
        need(reflection["role"] in ("REPRESENTATIVE", "REFLECTED"),
             "A reflection role")
    for key in ("c34_frontier_row_sha256", "source_cell_row_sha256"):
        need(type(row[key]) is str and HEX64.fullmatch(row[key]) is not None,
             "A leaf hash field:" + key)
    projection = close_object({
        "schema": ROW_PROJECTION_SCHEMA,
        "leaf_ordinal": row["leaf_ordinal"],
        "cell_id": row["cell_id"],
        "physical_chart": row["physical_chart"],
        "exact_box_sha256": digest(row["exact_box"]),
        "glue_refs": normalized_refs,
        "component_ref": component_ref,
        "terminal_disposition": disposition,
        "unresolved_reason": reason,
        "proof_ref_sha256": digest(proof_ref),
        "anchor_or_exterior_proof_sha256": digest(anchor),
        "anchor_or_exterior_kind": anchor["kind"],
        "known_anchor_status": anchor["known_anchor_status"],
        "strict_exterior_decider_object_sha256": anchor["strict_exterior_decider_object_sha256"],
        "source_row_sha256": row["row_sha256"],
    })
    return projection


def validate_a_leaf_ledger(value: Any) -> dict[str, Any]:
    exact_keys(value, A_LEAF_TOP_KEYS, "A leaf ledger")
    verify_closed(value, "A leaf ledger")
    exact_keys(value["authority_binding"], A_AUTHORITY_KEYS, "A authority binding")
    checkpoint = authority_checkpoint(value["authority_binding"], "A authority")
    need(checkpoint == EFFECTIVE_CHECKPOINT, "A C53 effective checkpoint")
    need(value["authority_binding"]["C53_global_head_file_sha256"] == C53_HEAD_FILE_SHA256,
         "A C53 head file pin")
    need(value["authority_binding"]["C53_global_head_object_sha256"] == C53_HEAD_OBJECT_SHA256,
         "A C53 head object pin")
    exact_keys(value["census"], A_CENSUS_KEYS, "A census")
    exact_keys(value["blocker_partition"], A_BLOCKER_PARTITION_KEYS,
               "A blocker partition")
    exact_keys(value["proof_policy"], A_PROOF_POLICY_KEYS, "A proof policy")
    need(type(value["proof_policy"]["allowed_terminal_dispositions"]) is list
         and set(value["proof_policy"]["allowed_terminal_dispositions"])
         == set(LEGAL_DISPOSITIONS)
         and len(value["proof_policy"]["allowed_terminal_dispositions"])
         == len(LEGAL_DISPOSITIONS), "A exact legal disposition set")
    need(value["proof_policy"]["depth_cap_terminal_forbidden"] is True,
         "A depth cap forbidden")
    need(value["proof_policy"]["local_chart_exit_is_terminal"] is False,
         "A local chart exit nonterminal")
    blocker_rows = value["blocker_rows"]
    need(type(blocker_rows) is list, "A blocker rows list")
    blocker_ids: list[Any] = []
    for row in blocker_rows:
        exact_keys(row, A_BLOCKER_ROW_KEYS, "A blocker row")
        validate_row_hash(row, "A blocker row")
        blocker_ids.append(row["blocker_row_id"])
    need(len(blocker_ids) == len(set(blocker_ids)), "A unique blocker row ids")
    leaves = value["leaves"]
    need(type(leaves) is list, "A leaves list")
    projections = [row_projection(row) for row in leaves]
    ordinals = [item["leaf_ordinal"] for item in projections]
    need(ordinals == list(range(len(projections))), "A exact leaf ordinal order")
    ids = [item["cell_id"] for item in projections]
    need(len(ids) == len(set(ids)), "A unique cell ids")
    derived: dict[str, int] = {name: 0 for name in LEGAL_DISPOSITIONS}
    unresolved = 0
    for item in projections:
        disposition = item["terminal_disposition"]
        if disposition is None:
            unresolved += 1
        else:
            derived[disposition] += 1
    derived[UNRESOLVED_CLASS] = unresolved
    derived["total"] = len(projections)
    reported_census = {
        key: value["census"][key]
        for key in (*LEGAL_DISPOSITIONS, UNRESOLVED_CLASS, "total")
    }
    need(value["census"]["unresolved_zero"] is (unresolved == 0),
         "A unresolved-zero flag reconstructed")
    return {
        "checkpoint": checkpoint,
        "file_object_sha256": value["object_sha256"],
        "projections": projections,
        "derived_census": derived,
        "reported_census": reported_census,
        "blocker_rows": blocker_rows,
        "blocker_partition": value["blocker_partition"],
        "status": value["status"],
    }


def validate_a_glue_ledger(value: Any) -> dict[str, Any]:
    exact_keys(value, A_GLUE_TOP_KEYS, "A glue ledger")
    verify_closed(value, "A glue ledger")
    exact_keys(value["authority_binding"], A_AUTHORITY_KEYS, "A glue authority binding")
    checkpoint = authority_checkpoint(value["authority_binding"], "A glue authority")
    need(checkpoint == EFFECTIVE_CHECKPOINT, "A glue C53 effective checkpoint")
    need(value["authority_binding"]["C53_global_head_file_sha256"] == C53_HEAD_FILE_SHA256,
         "A glue C53 head file pin")
    need(value["authority_binding"]["C53_global_head_object_sha256"] == C53_HEAD_OBJECT_SHA256,
         "A glue C53 head object pin")
    exact_keys(value["coverage"], A_GLUE_COVERAGE_KEYS, "A glue coverage")
    rows = value["glue_rows"]
    need(type(rows) is dict and set(rows) == set(A_GLUE_FAMILIES),
         "A exact glue families")
    family_ordinals: dict[str, set[int]] = {}
    row_hashes: dict[str, tuple[str, ...]] = {}
    for family in A_GLUE_FAMILIES:
        items = rows[family]
        need(type(items) is list, "A glue family list:" + family)
        ordinals: list[int] = []
        hashes: list[str] = []
        for item in items:
            exact_keys(item, A_GLUE_ROW_KEYS[family], "A glue row:" + family)
            validate_row_hash(item, "A glue row:" + family)
            need(type(item["ordinal"]) is int and item["ordinal"] >= 0,
                 "A glue ordinal:" + family)
            ordinals.append(item["ordinal"])
            hashes.append(item["row_sha256"])
        need(ordinals == list(range(len(items))), "A glue ordinal order:" + family)
        family_ordinals[family] = set(ordinals)
        row_hashes[family] = tuple(hashes)
    return {
        "checkpoint": checkpoint,
        "file_object_sha256": value["object_sha256"],
        "family_ordinals": family_ordinals,
        "row_hashes": row_hashes,
        "coverage": value["coverage"],
        "status": value["status"],
    }


def parse_single_member_gzip_jsonl(
    raw: bytes, label: str, maximum_uncompressed: int = 256 << 20,
) -> list[dict[str, Any]]:
    need(raw.startswith(b"\x1f\x8b\x08"), label + " gzip header")
    decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
    try:
        expanded = decoder.decompress(raw, maximum_uncompressed + 1)
        expanded += decoder.flush()
    except zlib.error as exc:
        raise Rejected(label + " gzip integrity:" + str(exc)) from exc
    need(decoder.eof, label + " complete gzip member")
    need(decoder.unused_data == b"" and decoder.unconsumed_tail == b"",
         label + " exactly one gzip member and no trailing data")
    need(0 < len(expanded) <= maximum_uncompressed, label + " bounded expansion")
    need(expanded.endswith(b"\n"), label + " final newline")
    lines = expanded.splitlines(keepends=True)
    need(bool(lines) and all(line not in (b"", b"\n", b"\r\n") for line in lines),
         label + " no blank rows")
    answer: list[dict[str, Any]] = []
    for index, line in enumerate(lines):
        value = parse_json(line, label + f" row {index}", maximum=8 << 20)
        need(type(value) is dict, label + " JSON object row")
        answer.append(value)
    return answer


def hash_line_sequence(hashes: list[str]) -> str:
    need(all(type(item) is str and HEX64.fullmatch(item) is not None for item in hashes),
         "hash line sequence members")
    return bytes_sha(("\n".join(hashes) + "\n").encode("ascii"))


def validate_b_descriptor(
    descriptor: Any, expected_basename: str, raw: bytes,
    rows: list[dict[str, Any]], label: str,
) -> None:
    exact_keys(descriptor, B_LEDGER_DESCRIPTOR_KEYS, label + " descriptor")
    need(descriptor["filename"] == expected_basename, label + " filename pin")
    need(descriptor["sha256"] == bytes_sha(raw), label + " file hash")
    need(descriptor["size"] == len(raw), label + " file size")
    need(descriptor["row_count"] == len(rows), label + " row count")
    hashes = [row.get("row_sha256") for row in rows]
    need(descriptor["row_hash_line_sequence_sha256"] == hash_line_sequence(hashes),
         label + " row sequence")


def validate_b_result(
    value: Any, raw_result: bytes, raw_cells: bytes, raw_edges: bytes,
    raw_components: bytes,
) -> dict[str, Any]:
    exact_keys(value, B_TOP_KEYS, "B result")
    verify_closed(value, "B result")
    need(bytes_sha(raw_result) == B_RESULT_FILE_SHA256, "B result exact file pin")
    need(value["object_sha256"] == B_RESULT_OBJECT_SHA256, "B result exact object pin")
    exact_keys(value["C53_effective_authority"], B_C53_KEYS, "B C53 authority")
    authority = value["C53_effective_authority"]
    need(authority["authority_role"] == "GLOBAL_COMPOSITE", "B C53 role")
    need(authority["effective_checkpoint_object_sha256"] == EFFECTIVE_CHECKPOINT,
         "B C53 checkpoint")
    need(authority["head_file_sha256"] == C53_HEAD_FILE_SHA256,
         "B C53 head file")
    need(authority["head_object_sha256"] == C53_HEAD_OBJECT_SHA256,
         "B C53 head object")
    need(value["authority_pins"].get("C55p0_input_contract", {}).get("file_sha256")
         == P0_CONTRACT_FILE_SHA256, "B P0 contract pin")
    need(type(value["credit_locks"]) is dict
         and all(item == 0 for item in value["credit_locks"].values()),
         "B all credit locks zero")
    ledgers = value["ledgers"]
    need(type(ledgers) is dict and set(ledgers) == set(B_LEDGER_NAMES),
         "B exact ledger descriptors")

    cells = parse_single_member_gzip_jsonl(raw_cells, "B cell ledger")
    edges = parse_single_member_gzip_jsonl(raw_edges, "B edge ledger")
    components = parse_single_member_gzip_jsonl(raw_components, "B component ledger")
    validate_b_descriptor(
        ledgers["cell_component_crosswalk"], B_CELL_BASENAME, raw_cells, cells,
        "B cell",
    )
    need(bytes_sha(raw_cells) == B_CELL_FILE_SHA256, "B cell exact file pin")
    need(bytes_sha(raw_edges) == B_EDGE_FILE_SHA256, "B edge exact file pin")
    need(bytes_sha(raw_components) == B_COMPONENT_FILE_SHA256,
         "B component exact file pin")
    validate_b_descriptor(
        ledgers["component_edges_and_glue"], B_EDGE_BASENAME, raw_edges, edges,
        "B edge",
    )
    validate_b_descriptor(
        ledgers["ordinary_components"], B_COMPONENT_BASENAME, raw_components,
        components, "B component",
    )
    need(len(cells) == 1_724 and len(edges) == 5_358 and len(components) == 26,
         "B exact inventory sizes")

    cell_by_id: dict[str, dict[str, Any]] = {}
    cell_row_hash_by_id: dict[str, str] = {}
    pair_members: dict[int, list[str]] = {}
    derived_cell_census = {"EARLIEST_PREFIX_EXCLUDED": 0, UNRESOLVED_CLASS: 0}
    for row in cells:
        exact_keys(row, B_CELL_KEYS, "B cell row")
        validate_row_hash(row, "B cell row")
        need(row["schema"].endswith(".cell-component-crosswalk-row"),
             "B cell schema")
        cell_id = row["cell_id"]
        need(type(cell_id) is str and cell_id not in cell_by_id, "B unique cell id")
        need(type(row["component_index"]) is int and 0 <= row["component_index"] < 26,
             "B component index")
        need(type(row["pair_index"]) is int and 0 <= row["pair_index"] < 862,
             "B pair index")
        need(row["current_effective_disposition"] in derived_cell_census,
             "B legal current cell disposition")
        need(row["D02_gate_credit"] == 0
             and row["whole_cell_connected_to_known_credit"] == 0,
             "B cell zero credits")
        need(row["coordinate_or_key_coincidence_used"] is False,
             "B no coordinate shortcut")
        need(type(row["physical_p_interval"]) is list
             and type(row["physical_t_interval"]) is list
             and row["physical_slice"] == "s=0", "B physical exact box")
        cell_by_id[cell_id] = row
        cell_row_hash_by_id[cell_id] = row["row_sha256"]
        pair_members.setdefault(row["pair_index"], []).append(cell_id)
        derived_cell_census[row["current_effective_disposition"]] += 1
    need(len(pair_members) == 862 and all(len(item) == 2 for item in pair_members.values()),
         "B exact reflected pairs")
    for row in cells:
        partner = row["reflection_partner_cell_id"]
        need(partner in cell_by_id
             and cell_by_id[partner]["reflection_partner_cell_id"] == row["cell_id"]
             and cell_by_id[partner]["pair_index"] == row["pair_index"],
             "B symmetric reflection pairing")
    need(derived_cell_census == {
        "EARLIEST_PREFIX_EXCLUDED": 576, UNRESOLVED_CLASS: 1_148,
    }, "B independently reconstructed cell census")

    edge_by_hash: dict[str, dict[str, Any]] = {}
    incident_hashes: dict[int, list[str]] = {index: [] for index in range(26)}
    adjacency: dict[str, set[str]] = {cell_id: set() for cell_id in cell_by_id}
    for row in edges:
        expected_edge_keys = (
            B_EDGE_KEYS if row.get("glue_kind") == "INHERITED_FIRST_EVENT_FACE"
            else B_EDGE_BASE_KEYS
        )
        exact_keys(row, expected_edge_keys, "B edge row")
        validate_row_hash(row, "B edge row")
        row_hash = row["row_sha256"]
        need(row_hash not in edge_by_hash, "B unique edge row hash")
        need(row["coordinate_or_key_coincidence_used"] is False,
             "B edge no coordinate shortcut")
        left = row["left_cell_id"]
        right = row["right_cell_id"]
        need(type(left) is str, "B edge left cell")
        indices = sorted({
            cell_by_id[item]["component_index"]
            for item in (left, right) if item in cell_by_id
        })
        need(row["ordinary_component_indices"] == indices,
             "B independently derived edge component indices")
        for index in indices:
            incident_hashes[index].append(row_hash)
        if left in cell_by_id and right in cell_by_id:
            need(cell_by_id[left]["component_index"] == cell_by_id[right]["component_index"],
                 "B no edge crosses listed components")
            adjacency[left].add(right)
            adjacency[right].add(left)
        edge_by_hash[row_hash] = row

    component_by_index: dict[int, dict[str, Any]] = {}
    member_partition: set[str] = set()
    for row in components:
        exact_keys(row, B_COMPONENT_KEYS, "B component row")
        validate_row_hash(row, "B component row")
        index = row["component_index"]
        need(type(index) is int and index not in component_by_index and 0 <= index < 26,
             "B unique component index")
        expected_members = sorted(
            cell_id for cell_id, cell in cell_by_id.items()
            if cell["component_index"] == index
        )
        need(row["member_cell_ids"] == expected_members, "B component member reconstruction")
        expected_member_hashes = [cell_row_hash_by_id[item] for item in expected_members]
        need(row["member_cell_row_sha256s"] == expected_member_hashes,
             "B component member row-hash reconstruction")
        need(row["member_cell_ids_sha256"] == digest(expected_members),
             "B component member ids hash")
        need(row["member_cell_row_sequence_sha256"] == digest(expected_member_hashes),
             "B component member row sequence")
        expected_edges = sorted(incident_hashes[index])
        need(row["edge_and_glue_row_sha256s"] == expected_edges,
             "B component incident edge reconstruction")
        need(row["edge_and_glue_row_sequence_sha256"] == digest(expected_edges),
             "B component edge sequence")
        need(row["cell_count"] == len(expected_members), "B component cell count")
        excluded = sorted(
            item for item in expected_members
            if cell_by_id[item]["current_effective_disposition"]
            == "EARLIEST_PREFIX_EXCLUDED"
        )
        unresolved = sorted(
            item for item in expected_members
            if cell_by_id[item]["current_effective_disposition"] == UNRESOLVED_CLASS
        )
        need(row["current_excluded_cell_count"] == len(excluded)
             and row["current_excluded_cell_ids_sha256"] == digest(excluded),
             "B component excluded reconstruction")
        need(row["current_unresolved_cell_count"] == len(unresolved)
             and row["current_unresolved_cell_ids_sha256"] == digest(unresolved),
             "B component unresolved reconstruction")
        need(row["D02_gate_credit"] == 0
             and row["whole_component_connected_to_known_credit"] == 0
             and row["whole_component_terminal_class"] is None
             and row["singleton_isolation_promoted"] is False,
             "B component fail-closed locks")
        need(type(row["unresolved_reason"]) is str and bool(row["unresolved_reason"]),
             "B component explicit unresolved reason")
        if len(expected_members) > 1:
            seen = {expected_members[0]}
            frontier = [expected_members[0]]
            while frontier:
                current = frontier.pop()
                for neighbor in adjacency[current]:
                    if neighbor in expected_members and neighbor not in seen:
                        seen.add(neighbor)
                        frontier.append(neighbor)
            need(seen == set(expected_members), "B component graph connected")
        member_partition.update(expected_members)
        component_by_index[index] = row
    need(set(component_by_index) == set(range(26)), "B exact component indices")
    need(member_partition == set(cell_by_id), "B component partition exhaustive")

    reported = value["current_effective_census"]["four_class_census"]
    need(reported == authority["current_four_class_census"], "B census internal agreement")
    need(reported == {
        "CONNECTED_TO_KNOWN": 0,
        "EARLIEST_PREFIX_EXCLUDED": 75_388,
        "SOURCE_GRAZING_OR_CEMETERY": 0,
        "TYPED_EVENT_GRAPH": 296,
        UNRESOLVED_CLASS: 1_148,
        "total": UNIVERSE_SIZE,
    }, "B exact effective census")
    need(value["exact_unresolved_partition"]["total_current_unresolved_cell_count"] == 1_148,
         "B unresolved partition total")
    base = value["base_atlas_census"]
    need(base["formal_excluded"] == 74_812 and base["typed_event_cells"] == 296,
         "B independently usable base census")
    derived_full_census = {
        "EARLIEST_PREFIX_EXCLUDED": base["formal_excluded"]
        + derived_cell_census["EARLIEST_PREFIX_EXCLUDED"],
        "TYPED_EVENT_GRAPH": base["typed_event_cells"],
        "CONNECTED_TO_KNOWN": 0,
        "SOURCE_GRAZING_OR_CEMETERY": 0,
        UNRESOLVED_CLASS: derived_cell_census[UNRESOLVED_CLASS],
        "total": UNIVERSE_SIZE,
    }
    need(derived_full_census == reported, "B full census reconstructed from cell rows")
    return {
        "result_file_sha256": bytes_sha(raw_result),
        "result_object_sha256": value["object_sha256"],
        "cell_file_sha256": bytes_sha(raw_cells),
        "edge_file_sha256": bytes_sha(raw_edges),
        "component_file_sha256": bytes_sha(raw_components),
        "cell_by_id": cell_by_id,
        "component_by_index": component_by_index,
        "derived_cell_census": derived_cell_census,
        "derived_full_census": derived_full_census,
        "global_closure_proved": value["global_closure_proved"],
        "unresolved_zero": value["unresolved_zero"],
        "strict_decider_eligible": value["strict_decider_eligible"],
        "status": value["status"],
    }


def cross_validate_a_b(a_leaf: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    cell_by_id = b["cell_by_id"]
    component_by_index = b["component_by_index"]
    mapped: set[str] = set()
    anchor_rows = 0
    for row in a_leaf["projections"]:
        reference = row["component_ref"]
        if reference is None:
            need(row["cell_id"] not in cell_by_id,
                 "A null component ref only outside B ordinary universe")
            continue
        cell_id = row["cell_id"]
        need(cell_id in cell_by_id and cell_id not in mapped,
             "A/B unique ordinary cell crosswalk")
        cell = cell_by_id[cell_id]
        index = cell["component_index"]
        component = component_by_index[index]
        need(reference["component_index"] == index
             and reference["component_id"] == cell["component_id"]
             and reference["component_row_sha256"]
             == component["C34_component_row_sha256"],
             "A/B component row binding")
        need(row["physical_chart"] == cell["compact_chart"], "A/B physical chart")
        b_box = {
            "physical_p_interval": cell["physical_p_interval"],
            "physical_slice": cell["physical_slice"],
            "physical_t_interval": cell["physical_t_interval"],
        }
        need(row["exact_box_sha256"] == digest(b_box), "A/B exact physical box")
        if cell["current_effective_disposition"] == "EARLIEST_PREFIX_EXCLUDED":
            need(row["terminal_disposition"] == "EARLIEST_PREFIX_EXCLUDED",
                 "A/B ordinary excluded disposition")
        else:
            need(row["terminal_disposition"] is None
                 and type(row["unresolved_reason"]) is str,
                 "A/B ordinary unresolved disposition")
        need(row["strict_exterior_decider_object_sha256"] is None,
             "A/B no invented strict exterior decider")
        if row["anchor_or_exterior_kind"] == "KNOWN_ANCHOR_STRICT_SUBSET_ONLY":
            need(cell["known_sheet_anchor_role"] == "ANCHOR_CELL_CONTAINS_STRICT_OPEN_COLLAR",
                 "A anchor is contained in B anchor reconstruction")
            anchor_rows += 1
        elif cell["known_sheet_anchor_role"] == "NO_CELL_LEVEL_ANCHOR":
            need(row["anchor_or_exterior_kind"] == "NO_POSITIVE_ANCHOR_OR_EXTERIOR_PROOF",
                 "A/B no positive anchor/exterior proof")
        mapped.add(cell_id)
    need(mapped == set(cell_by_id), "A/B ordinary cell crosswalk exhaustive")
    need(anchor_rows == 1, "A exact strict-subset anchor seed")
    b_anchor_rows = sum(
        cell["known_sheet_anchor_role"] == "ANCHOR_CELL_CONTAINS_STRICT_OPEN_COLLAR"
        for cell in cell_by_id.values()
    )
    need(b_anchor_rows == 2, "B reflected strict-subset anchor reconstruction")
    need(a_leaf["derived_census"] == b["derived_full_census"],
         "A/B independently reconstructed full census agrees")
    return {
        "ordinary_cell_crosswalk_count": len(mapped),
        "A_strict_subset_anchor_seed_count": anchor_rows,
        "B_reflected_strict_subset_anchor_row_count": b_anchor_rows,
        "full_census_agrees": True,
        "exact_physical_box_crosswalk_agrees": True,
        "component_row_crosswalk_agrees": True,
    }


def cross_validate_leaf_glue(a_leaf: dict[str, Any], a_glue: dict[str, Any]) -> None:
    map_key = {
        "intra_face_ordinals": "intra_faces",
        "source_grazing_corner_ordinals": "source_grazing_corners",
        "source_grazing_face_ordinals": "source_grazing_faces",
        "source_seam_ordinals": "source_seams",
    }
    for row in a_leaf["projections"]:
        for ref_key, ordinals in row["glue_refs"].items():
            need(set(ordinals) <= a_glue["family_ordinals"][map_key[ref_key]],
                 "A leaf glue reference exists")


def default_contract() -> dict[str, Any]:
    return close_object({
        "schema": CONTRACT_SCHEMA,
        "verifier_source_sha256": verifier_source_sha256(),
        "C53_binding": {
            "head_path": str(C53_HEAD_PATH.relative_to(WORKSPACE)),
            "head_file_sha256": C53_HEAD_FILE_SHA256,
            "head_object_sha256": C53_HEAD_OBJECT_SHA256,
            "effective_checkpoint_object_sha256": EFFECTIVE_CHECKPOINT,
        },
        "inert_inputs": {
            "C55_P0_contract": "deliverables/" + P0_CONTRACT_BASENAME,
            "C55_A_leaf_ledger": "deliverables/" + A_LEAF_BASENAME,
            "C55_A_glue_ledger": "deliverables/" + A_GLUE_BASENAME,
            "C55_B_component_ledger": "deliverables/" + B_RESULT_BASENAME,
            "C55_B_cell_rows": "deliverables/" + B_CELL_BASENAME,
            "C55_B_edge_rows": "deliverables/" + B_EDGE_BASENAME,
            "C55_B_component_rows": "deliverables/" + B_COMPONENT_BASENAME,
        },
        "exact_input_pins": {
            "C55_P0_contract_file_sha256": P0_CONTRACT_FILE_SHA256,
            "C55_A_leaf_file_sha256": A_LEAF_FILE_SHA256,
            "C55_A_leaf_object_sha256": A_LEAF_OBJECT_SHA256,
            "C55_A_glue_file_sha256": A_GLUE_FILE_SHA256,
            "C55_A_glue_object_sha256": A_GLUE_OBJECT_SHA256,
            "C55_B_result_file_sha256": B_RESULT_FILE_SHA256,
            "C55_B_result_object_sha256": B_RESULT_OBJECT_SHA256,
            "C55_B_cell_file_sha256": B_CELL_FILE_SHA256,
            "C55_B_edge_file_sha256": B_EDGE_FILE_SHA256,
            "C55_B_component_file_sha256": B_COMPONENT_FILE_SHA256,
        },
        "producer_import_or_execution_allowed": False,
        "exact_universe_size": UNIVERSE_SIZE,
        "legal_terminal_dispositions": list(LEGAL_DISPOSITIONS),
        "unresolved_class": UNRESOLVED_CLASS,
        "row_rule": (
            "terminal_disposition is one legal enum iff unresolved_reason is null; otherwise terminal_disposition is null and unresolved_reason is explicit"
        ),
        "positive_gate": {
            "A_and_B_exact_file_and_object_pins": True,
            "per_row_independent_reconstruction": True,
            "leaf_glue_component_anchor_dual_reconstruction_agrees": True,
            "census_total": UNIVERSE_SIZE,
            "unresolved_count": 0,
            "all_blocker_sets_empty": True,
        },
        "synthetic_positive_path_is_authority": False,
        "result_is_authority": False,
        "terminal_credit": 0,
        "formal_credit": 0,
        "D02_credit": 0,
        "runtime_writes_performed": False,
        "canonical_pointer_or_seal_touched": False,
    })


def producer_source_independence() -> dict[str, Any]:
    tree = ast.parse(SELF.read_text(encoding="utf-8"), filename=SELF.name)
    forbidden_names = {
        "cm2_round306c55a_four_chart_fundamental_domain_bnb",
        "cm2_round306c55b_global_component_adjacency_known_sheet_ledger",
    }
    imported: list[str] = []
    dynamic_calls: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.append(node.module or "")
        elif isinstance(node, ast.Call):
            name = ""
            if isinstance(node.func, ast.Name):
                name = node.func.id
                if name in {"exec", "eval", "compile", "__import__"}:
                    dynamic_calls.append(name)
            elif isinstance(node.func, ast.Attribute):
                name = node.func.attr
                if name in {"run_path", "run_module"}:
                    dynamic_calls.append(name)
    need(not any(any(token in item for token in forbidden_names) for item in imported),
         "no A/B producer import")
    need(not dynamic_calls, "no dynamic producer execution primitives")
    loaded = sorted(
        name for name in sys.modules
        if any(token in name for token in forbidden_names)
    )
    need(not loaded, "A/B producer absent from sys.modules")
    return {
        "A_or_B_producer_imported": False,
        "A_or_B_producer_executed": False,
        "dynamic_execution_primitives": [],
    }


def unavailable_result(blockers: list[str], input_state: dict[str, Any]) -> dict[str, Any]:
    unique = sorted(set(blockers))
    need(bool(unique), "fail-closed result has blockers")
    return close_object({
        "schema": VERIFICATION_SCHEMA,
        "verifier_source_sha256": verifier_source_sha256(),
        "status": "FAIL_CLOSED_GLOBAL_STRICT_DECIDER_NOT_ENABLED",
        "requested_terminal_class": REQUESTED_TERMINAL,
        "terminal_class": None,
        "positive_terminal_enabled": False,
        "blockers": unique,
        "input_state": input_state,
        "exact_universe_size": UNIVERSE_SIZE,
        "producer_independence": producer_source_independence(),
        "result_is_authority": False,
        "synthetic_positive_path_is_authority": False,
        "terminal_credit": 0,
        "formal_credit": 0,
        "D02_credit": 0,
        "runtime_writes_performed": False,
        "canonical_pointer_or_seal_touched": False,
    })


def eligibility_gate(state: dict[str, Any]) -> tuple[bool, list[str]]:
    """Pure positive gate used by real reconstruction and synthetic attacks.

    The object hash is verified, but no boolean inside the object is trusted:
    every gate is recomputed from the supplied independent projections.
    """

    keys = frozenset((
        "A_file_pin_matches", "A_object_pin_matches", "A_row_count",
        "A_derived_census", "A_reported_census", "A_row_sequence_sha256",
        "B_file_pin_matches", "B_object_pin_matches", "B_row_count",
        "B_derived_census", "B_reported_census", "B_row_sequence_sha256",
        "C53_checkpoint_matches", "C53_head_matches", "A_B_glue_agrees",
        "A_B_components_agree", "A_B_anchor_or_exterior_proofs_agree",
        "all_row_dispositions_legal_or_null", "all_row_hashes_valid",
        "all_proofs_reconstructed", "A_blockers", "B_blockers",
        "object_sha256",
    ))
    exact_keys(state, keys, "eligibility state")
    verify_closed(state, "eligibility state")
    blockers: list[str] = []

    def require_true(key: str) -> None:
        need(type(state[key]) is bool, "eligibility boolean:" + key)
        if not state[key]:
            blockers.append(key.upper() + "_FALSE")

    for key in (
        "A_file_pin_matches", "A_object_pin_matches", "B_file_pin_matches",
        "B_object_pin_matches", "C53_checkpoint_matches", "C53_head_matches",
        "A_B_glue_agrees", "A_B_components_agree",
        "A_B_anchor_or_exterior_proofs_agree",
        "all_row_dispositions_legal_or_null", "all_row_hashes_valid",
        "all_proofs_reconstructed",
    ):
        require_true(key)
    for side in ("A", "B"):
        count = state[side + "_row_count"]
        need(type(count) is int and count >= 0, side + " row count")
        if count != UNIVERSE_SIZE:
            blockers.append(side + "_ROW_COUNT_NOT_76832")
        derived = state[side + "_derived_census"]
        reported = state[side + "_reported_census"]
        census_keys = set(LEGAL_DISPOSITIONS) | {UNRESOLVED_CLASS, "total"}
        need(type(derived) is dict and set(derived) == census_keys,
             side + " derived census keys")
        need(type(reported) is dict and set(reported) == census_keys,
             side + " reported census keys")
        need(all(type(value) is int and value >= 0 for value in derived.values()),
             side + " nonnegative derived census")
        need(all(type(value) is int and value >= 0 for value in reported.values()),
             side + " nonnegative reported census")
        if derived != reported:
            blockers.append(side + "_REPORTED_CENSUS_MISMATCH")
        if derived["total"] != sum(derived[key] for key in census_keys - {"total"}):
            blockers.append(side + "_DERIVED_CENSUS_SUM_MISMATCH")
        if derived["total"] != count:
            blockers.append(side + "_CENSUS_TOTAL_DIFFERS_FROM_ROW_COUNT")
        if derived[UNRESOLVED_CLASS] != 0:
            blockers.append(side + "_UNRESOLVED_NONZERO:" + str(derived[UNRESOLVED_CLASS]))
        sequence = state[side + "_row_sequence_sha256"]
        need(type(sequence) is str and HEX64.fullmatch(sequence) is not None,
             side + " row sequence hash")
        side_blockers = state[side + "_blockers"]
        need(type(side_blockers) is list and all(type(item) is str and item for item in side_blockers),
             side + " blocker list")
        if side_blockers:
            blockers.append(side + "_BLOCKERS_NONEMPTY")
    if state["A_row_sequence_sha256"] != state["B_row_sequence_sha256"]:
        blockers.append("A_B_ROW_SEQUENCE_MISMATCH")
    if state["A_derived_census"] != state["B_derived_census"]:
        blockers.append("A_B_DERIVED_CENSUS_MISMATCH")
    return not blockers, sorted(set(blockers))


def synthetic_eligible_state() -> dict[str, Any]:
    census = {
        "EARLIEST_PREFIX_EXCLUDED": 75_388,
        "TYPED_EVENT_GRAPH": 296,
        "CONNECTED_TO_KNOWN": 574,
        "SOURCE_GRAZING_OR_CEMETERY": 574,
        UNRESOLVED_CLASS: 0,
        "total": UNIVERSE_SIZE,
    }
    sequence = digest({
        "schema": SCHEMA + ".synthetic-row-sequence",
        "count": UNIVERSE_SIZE,
        "note": "self-test-only-not-evidence",
    })
    return close_object({
        "A_file_pin_matches": True,
        "A_object_pin_matches": True,
        "A_row_count": UNIVERSE_SIZE,
        "A_derived_census": census,
        "A_reported_census": copy.deepcopy(census),
        "A_row_sequence_sha256": sequence,
        "B_file_pin_matches": True,
        "B_object_pin_matches": True,
        "B_row_count": UNIVERSE_SIZE,
        "B_derived_census": copy.deepcopy(census),
        "B_reported_census": copy.deepcopy(census),
        "B_row_sequence_sha256": sequence,
        "C53_checkpoint_matches": True,
        "C53_head_matches": True,
        "A_B_glue_agrees": True,
        "A_B_components_agree": True,
        "A_B_anchor_or_exterior_proofs_agree": True,
        "all_row_dispositions_legal_or_null": True,
        "all_row_hashes_valid": True,
        "all_proofs_reconstructed": True,
        "A_blockers": [],
        "B_blockers": [],
    })


def reclose_after_mutation(value: dict[str, Any], mutation: Callable[[dict[str, Any]], None]) -> dict[str, Any]:
    answer = copy.deepcopy(value)
    answer.pop("object_sha256")
    mutation(answer)
    return close_object(answer)


def verify_real_inputs() -> dict[str, Any]:
    required = (
        C53_HEAD_PATH, P0_CONTRACT_PATH, A_LEAF_PATH, A_GLUE_PATH,
        B_RESULT_PATH, B_CELL_PATH, B_EDGE_PATH, B_COMPONENT_PATH,
    )
    missing = [str(path.relative_to(WORKSPACE)) for path in required if not path.exists()]
    if missing:
        return unavailable_result(
            ["MISSING_EXACT_INPUT:" + item for item in missing],
            {"present_paths": [str(path.relative_to(WORKSPACE)) for path in required if path.exists()]},
        )
    raw = stable_read_bundle(required)
    head = parse_json(raw[C53_HEAD_PATH], "C53 head")
    verify_c53_head(head, raw[C53_HEAD_PATH])
    p0_contract = parse_json(
        raw[P0_CONTRACT_PATH], "P0 contract", require_canonical=False,
    )
    verify_p0_contract(p0_contract, raw[P0_CONTRACT_PATH])
    a_leaf_value = parse_json(raw[A_LEAF_PATH], "A leaf ledger")
    a_glue_value = parse_json(raw[A_GLUE_PATH], "A glue ledger")
    b_value = parse_json(raw[B_RESULT_PATH], "B component ledger")
    a_leaf = validate_a_leaf_ledger(a_leaf_value)
    a_glue = validate_a_glue_ledger(a_glue_value)
    need(bytes_sha(raw[A_LEAF_PATH]) == A_LEAF_FILE_SHA256,
         "A leaf exact file pin")
    need(a_leaf_value["object_sha256"] == A_LEAF_OBJECT_SHA256,
         "A leaf exact object pin")
    need(bytes_sha(raw[A_GLUE_PATH]) == A_GLUE_FILE_SHA256,
         "A glue exact file pin")
    need(a_glue_value["object_sha256"] == A_GLUE_OBJECT_SHA256,
         "A glue exact object pin")
    cross_validate_leaf_glue(a_leaf, a_glue)
    b = validate_b_result(
        b_value, raw[B_RESULT_PATH], raw[B_CELL_PATH], raw[B_EDGE_PATH],
        raw[B_COMPONENT_PATH],
    )
    cross = cross_validate_a_b(a_leaf, b)

    # The B adapter is deliberately closed only after C55-B freezes its exact
    # schema.  Before then, the correct real-input result is a named blocker;
    # no self-asserted `strict_decider_eligible` boolean is consumed.
    blockers: list[str] = []
    if len(a_leaf["projections"]) != UNIVERSE_SIZE:
        blockers.append("A_LEAF_UNIVERSE_NOT_76832")
    if a_leaf["derived_census"].get(UNRESOLVED_CLASS) != 0:
        blockers.append(
            "A_UNRESOLVED_NONZERO:" + str(a_leaf["derived_census"].get(UNRESOLVED_CLASS))
        )
    if a_leaf["reported_census"] != a_leaf["derived_census"]:
        blockers.append("A_REPORTED_CENSUS_DIFFERS_FROM_ROW_RECONSTRUCTION")
    if a_leaf["blocker_rows"] not in ([], {}):
        blockers.append("A_BLOCKER_ROWS_NONEMPTY")
    if b["derived_cell_census"][UNRESOLVED_CLASS] != 0:
        blockers.append(
            "B_UNRESOLVED_NONZERO:" + str(b["derived_cell_census"][UNRESOLVED_CLASS])
        )
    if b["global_closure_proved"] is not True:
        blockers.append("B_GLOBAL_CLOSURE_NOT_PROVED")
    if b["unresolved_zero"] is not True:
        blockers.append("B_UNRESOLVED_ZERO_FALSE")
    if b["strict_decider_eligible"] is not True:
        blockers.append("B_STRICT_DECIDER_ELIGIBLE_FALSE")
    blockers.append("B_NO_INERT_76832_PER_ROW_PROJECTION_FOR_SECOND_FULL_RECONSTRUCTION")
    return unavailable_result(blockers, {
        "C53_head_file_sha256": bytes_sha(raw[C53_HEAD_PATH]),
        "C53_head_object_sha256": head["authority_seal_object_sha256"],
        "effective_checkpoint_object_sha256": EFFECTIVE_CHECKPOINT,
        "P0_contract_file_sha256": bytes_sha(raw[P0_CONTRACT_PATH]),
        "A_leaf_file_sha256": bytes_sha(raw[A_LEAF_PATH]),
        "A_leaf_object_sha256": a_leaf_value["object_sha256"],
        "A_glue_file_sha256": bytes_sha(raw[A_GLUE_PATH]),
        "A_glue_object_sha256": a_glue_value["object_sha256"],
        "B_file_sha256": bytes_sha(raw[B_RESULT_PATH]),
        "B_object_sha256": b_value.get("object_sha256"),
        "B_cell_file_sha256": bytes_sha(raw[B_CELL_PATH]),
        "B_edge_file_sha256": bytes_sha(raw[B_EDGE_PATH]),
        "B_component_file_sha256": bytes_sha(raw[B_COMPONENT_PATH]),
        "independent_B_cell_census": b["derived_cell_census"],
        "A_B_cross_reconstruction": cross,
        "independent_A_census": a_leaf["derived_census"],
    })


def _expect_rejected(name: str, action: Callable[[], Any], results: dict[str, bool]) -> None:
    try:
        action()
    except (Rejected, OSError):
        results[name] = True
    else:
        raise Rejected("hostile test did not reject:" + name)


def run_self_test() -> dict[str, Any]:
    """Execute parser/filesystem attacks without importing either producer."""

    results: dict[str, bool] = {}
    baseline = close_object({"schema": "synthetic", "value": 1})
    baseline_raw = canonical(baseline) + b"\n"
    need(parse_json(baseline_raw, "synthetic") == baseline, "baseline strict JSON")
    results["canonical_JSON_accepted"] = True

    _expect_rejected(
        "duplicate_JSON_key_rejected",
        lambda: parse_json(b'{"a":1,"a":2}\n', "duplicate"), results,
    )
    _expect_rejected(
        "UTF8_BOM_rejected",
        lambda: parse_json(b'\xef\xbb\xbf{"a":1}\n', "BOM"), results,
    )
    _expect_rejected(
        "NaN_rejected",
        lambda: parse_json(b'{"a":NaN}\n', "NaN"), results,
    )
    _expect_rejected(
        "noncanonical_pretty_JSON_rejected",
        lambda: parse_json(b'{"a": 1}\n', "pretty"), results,
    )
    forged = copy.deepcopy(baseline)
    forged["value"] = 2
    _expect_rejected(
        "closed_object_mutation_rejected",
        lambda: verify_closed(forged, "forged"), results,
    )

    with tempfile.TemporaryDirectory(prefix="cm2-c55c-") as temporary:
        root = Path(temporary)
        target = root / "target.json"
        target.write_bytes(baseline_raw)
        need(stable_read_bundle((target,))[target] == baseline_raw,
             "baseline stable read")
        results["regular_single_link_stable_read_accepted"] = True

        symlink = root / "symlink.json"
        symlink.symlink_to(target.name)
        _expect_rejected(
            "symlink_rejected",
            lambda: stable_read_bundle((symlink,)), results,
        )

        hardlink = root / "hardlink.json"
        os.link(target, hardlink)
        _expect_rejected(
            "hardlink_rejected",
            lambda: stable_read_bundle((target,)), results,
        )
        hardlink.unlink()

        replacement = root / "replacement.json"
        replacement.write_bytes(canonical(close_object({"schema": "synthetic", "value": 2})) + b"\n")

        def swap_file() -> None:
            os.replace(replacement, target)

        _expect_rejected(
            "same_name_file_TOCTOU_swap_rejected",
            lambda: stable_read_bundle((target,), mutation_hook=swap_file), results,
        )

        target.write_bytes(baseline_raw)
        moved = root.with_name(root.name + "-moved")

        def swap_directory() -> None:
            os.rename(root, moved)
            os.mkdir(root)
            (root / target.name).write_bytes(baseline_raw)

        _expect_rejected(
            "parent_directory_TOCTOU_swap_rejected",
            lambda: stable_read_bundle((target,), mutation_hook=swap_directory), results,
        )
        # TemporaryDirectory owns the replacement path now; remove the moved
        # tree explicitly so cleanup remains deterministic.
        for child in moved.iterdir():
            child.unlink()
        moved.rmdir()

    synthetic = synthetic_eligible_state()
    eligible, blockers = eligibility_gate(synthetic)
    need(eligible and blockers == [], "synthetic self-test positive gate")
    results["synthetic_exact_76832_zero_unresolved_path_exercises_positive_gate"] = True

    def set_unresolved_one(state: dict[str, Any]) -> None:
        for side in ("A", "B"):
            for census_key in (side + "_derived_census", side + "_reported_census"):
                state[census_key]["SOURCE_GRAZING_OR_CEMETERY"] -= 1
                state[census_key][UNRESOLVED_CLASS] = 1

    coherent_attacks: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("coherent_A_file_pin_forgery_denied", lambda item: item.__setitem__("A_file_pin_matches", False)),
        ("coherent_A_object_pin_forgery_denied", lambda item: item.__setitem__("A_object_pin_matches", False)),
        ("coherent_B_file_pin_forgery_denied", lambda item: item.__setitem__("B_file_pin_matches", False)),
        ("coherent_B_object_pin_forgery_denied", lambda item: item.__setitem__("B_object_pin_matches", False)),
        ("coherent_row_count_76831_denied", lambda item: item.__setitem__("A_row_count", UNIVERSE_SIZE - 1)),
        ("coherent_nonzero_unresolved_denied", set_unresolved_one),
        ("coherent_row_sequence_divergence_denied", lambda item: item.__setitem__("B_row_sequence_sha256", "0" * 64)),
        ("coherent_C53_head_forgery_denied", lambda item: item.__setitem__("C53_head_matches", False)),
        ("coherent_C53_checkpoint_forgery_denied", lambda item: item.__setitem__("C53_checkpoint_matches", False)),
        ("coherent_glue_divergence_denied", lambda item: item.__setitem__("A_B_glue_agrees", False)),
        ("coherent_component_divergence_denied", lambda item: item.__setitem__("A_B_components_agree", False)),
        ("coherent_anchor_or_exterior_divergence_denied", lambda item: item.__setitem__("A_B_anchor_or_exterior_proofs_agree", False)),
        ("coherent_illegal_disposition_denied", lambda item: item.__setitem__("all_row_dispositions_legal_or_null", False)),
        ("coherent_row_hash_forgery_denied", lambda item: item.__setitem__("all_row_hashes_valid", False)),
        ("coherent_proof_shortcut_denied", lambda item: item.__setitem__("all_proofs_reconstructed", False)),
        ("coherent_A_blocker_denied", lambda item: item["A_blockers"].append("MISSING_GLOBAL_DECIDER")),
        ("coherent_B_blocker_denied", lambda item: item["B_blockers"].append("MISSING_KNOWN_SHEET_ANCHOR")),
        ("coherent_A_reported_census_resign_denied", lambda item: item["A_reported_census"].__setitem__("CONNECTED_TO_KNOWN", 575)),
    ]
    for name, mutation in coherent_attacks:
        attacked = reclose_after_mutation(synthetic, mutation)
        try:
            accepted, _ = eligibility_gate(attacked)
        except Rejected:
            accepted = False
        need(not accepted, "coherent semantic attack denied:" + name)
        results[name] = True

    independence = producer_source_independence()
    results["A_B_producers_not_imported_or_executed"] = (
        independence["A_or_B_producer_imported"] is False
        and independence["A_or_B_producer_executed"] is False
    )
    need(all(results.values()), "all hostile tests pass")
    return close_object({
        "schema": SCHEMA + ".self-test",
        "verifier_source_sha256": verifier_source_sha256(),
        "status": "PASS_EXECUTED_HOSTILE_IO_AND_JSON_TESTS",
        "tests": results,
        "test_count": len(results),
        "producer_independence": independence,
        "synthetic_positive_path_is_authority": False,
        "terminal_credit": 0,
        "formal_credit": 0,
        "D02_credit": 0,
        "runtime_writes_performed": False,
    })


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--contract", action="store_true")
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    try:
        if args.contract:
            output = default_contract()
        elif args.self_test:
            output = run_self_test()
        else:
            output = verify_real_inputs()
        sys.stdout.buffer.write(canonical(output) + b"\n")
        return 0
    except (Rejected, OSError) as exc:
        failure = close_object({
            "schema": SCHEMA + ".fail-closed-exception",
            "verifier_source_sha256": verifier_source_sha256(),
            "status": "FAIL_CLOSED_REJECTED",
            "reason": str(exc),
            "terminal_class": None,
            "positive_terminal_enabled": False,
            "result_is_authority": False,
            "terminal_credit": 0,
            "formal_credit": 0,
            "D02_credit": 0,
            "runtime_writes_performed": False,
        })
        sys.stdout.buffer.write(canonical(failure) + b"\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
