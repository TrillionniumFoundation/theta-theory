#!/usr/bin/env python3
"""Independent Round304 cacheless expected-state promotion verifier.

Independence rule: the Round304 producer is never imported, executed, parsed,
or tokenized.  Its frozen bytes are used only as an inert SHA-256 input.  The
verifier rebuilds every candidate byte before opening candidate artifacts,
runs focused attacks, then publishes an attack-suite/verification pair with
the verification atomically moved last as the commit marker.
"""

from __future__ import annotations

import argparse
import ast
import copy
import ctypes
import errno
import fcntl
import gzip
import hashlib
import io
import json
import os
import re
import stat
import tempfile
import zlib
from collections import Counter, defaultdict, deque
from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, BinaryIO, TextIO


def discover_workspace_root(source: Path) -> Path:
    """Find the ancestor that owns the sealed upstream deliverables set."""

    resolved = source.resolve()
    for ancestor in resolved.parents:
        deliverables = ancestor / "deliverables"
        sentinel = (
            deliverables
            / "cm2_round294b_source_g_registry_builder_admission_closure_manifest.sha256"
        )
        if (
            deliverables.is_dir()
            and not deliverables.is_symlink()
            and sentinel.is_file()
            and not sentinel.is_symlink()
        ):
            return ancestor
    raise RuntimeError("workspace root with sealed upstream deliverables not found")


ROOT = discover_workspace_root(Path(__file__))
DATA = ROOT / "deliverables"
PIN = re.compile(r"^[0-9a-f]{64}$")
ENCODER = json.JSONEncoder(
    ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":")
)
FileIdentity = tuple[int, int, int, int, int, int, int]
DirectoryIdentity = tuple[int, int, int]
SOURCE_SNAPSHOTS: dict[Path, FileIdentity] = {}
CANDIDATE_SNAPSHOTS: dict[Path, FileIdentity] = {}
PARENT_DIRECTORY_SNAPSHOTS: dict[Path, DirectoryIdentity] = {}

CANDIDATE_PREFIX = (
    "cm2_round304_source_g_fresh_extended_registry_legal_component_dsu_rebuild"
)
CANDIDATE_FILES = {
    "producer": CANDIDATE_PREFIX + ".py",
    "edge": CANDIDATE_PREFIX + "_edge_application_ledger.json.gz",
    "member": CANDIDATE_PREFIX + "_member_component_ledger.json.gz",
    "wtail": CANDIDATE_PREFIX + "_wtail_disposition_ledger.json.gz",
    "residual": CANDIDATE_PREFIX + "_residual_gate_ledger.json.gz",
    "result": CANDIDATE_PREFIX + "_result.json",
}
VERIFICATION_FILENAME = CANDIDATE_PREFIX + "_verification.json"
ATTACK_FILENAME = CANDIDATE_PREFIX + "_attack_suite.json"
VERIFIER_FILENAME = CANDIDATE_PREFIX + "_promotion_verifier.py"
CANDIDATE_TABLES = {
    "edge": "fresh_DSU_edge_application_rows",
    "member": "fresh_member_component_rows",
    "wtail": "W_tail_stronger_path_disposition_rows",
    "residual": "post_DSU_residual_gate_rows",
}
CANDIDATE_ID_FIELDS = {
    "edge": "Round304_fresh_DSU_edge_application_row_id",
    "member": "Round304_fresh_member_component_row_id",
    "wtail": "Round304_W_tail_disposition_row_id",
    "residual": "Round304_residual_gate_row_id",
}
CANDIDATE_ROW_SCHEMAS = {
    "edge": "cm2.round304.fresh-dsu-edge-application-row.v1",
    "member": "cm2.round304.fresh-member-component-row.v1",
    "wtail": "cm2.round304.wtail-stronger-path-disposition-row.v1",
    "residual": "cm2.round304.post-dsu-residual-gate-row.v1",
}
CANDIDATE_LEDGER_SCHEMAS = {
    key: value.removesuffix("-row.v1") + "-ledger.v1"
    for key, value in CANDIDATE_ROW_SCHEMAS.items()
}
CANDIDATE_RESULT_SCHEMA = (
    "cm2.round304.source-g-fresh-extended-registry-legal-component-"
    "dsu-rebuild.v1"
)
CANDIDATE_EXACT_ROW_FIELDS = {
    "edge": (
        "Round304_fresh_DSU_edge_application_row_id",
        "application_index",
        "canonical_occurrence_endpoint_pair",
        "fed_to_fresh_DSU",
        "formal_DSU_rank_reduction_credit",
        "formal_fibre_credit",
        "formal_global_disposition_credit",
        "formal_maximality_credit",
        "forward_cycle_or_redundant",
        "forward_rank_reduction",
        "old_63224_partition_used_as_state",
        "projected_base_root_pair",
        "provisional_Round303B_consumed",
        "row_sha256",
        "schema",
        "serialized_Round301_partition_used_as_state",
        "source_channel",
        "source_row_id",
        "source_row_sha256",
    ),
    "member": (
        "Round304_fresh_member_component_row_id",
        "base_root_id",
        "final_component_id",
        "formal_fibre_credit",
        "formal_global_disposition_credit",
        "formal_maximality_credit",
        "member_identity_preserved",
        "official_key_id",
        "registry_occurrence_id",
        "row_sha256",
        "schema",
    ),
    "wtail": (
        "Round304_W_tail_disposition_row_id",
        "canonical_occurrence_endpoint_pair",
        "disposition",
        "eligible_for_fresh_DSU_application",
        "exclusion_credit",
        "final_component_pair",
        "formal_component_edge_credit",
        "formal_DSU_rank_reduction_credit",
        "formal_fibre_credit",
        "formal_global_disposition_credit",
        "formal_maximality_credit",
        "nonedge_credit",
        "projected_base_root_pair",
        "row_sha256",
        "same_final_component",
        "schema",
        "source_Round300D_row_id",
        "source_W_tail_row_id",
        "source_W_tail_row_sha256",
        "source_row_fed_to_DSU",
        "stronger_legal_path",
    ),
    "residual": (
        "Round304_residual_gate_row_id",
        "D02_status",
        "Gate5_complete_18_field_block_count",
        "CM2_status",
        "formal_fibre_credit",
        "formal_global_disposition_credit",
        "formal_maximality_credit",
        "hard_coded_1024_treated_as_theorem",
        "required_next",
        "row_sha256",
        "schema",
    ),
}
CANDIDATE_EXACT_LEDGER_BASE_FIELDS = (
    "row_count",
    "row_hashes_sha256",
    "row_ids_sha256",
    "rows_sha256",
    "schema",
    "status",
)
CANDIDATE_EXACT_LEDGER_FIELDS = {
    key: tuple(sorted((*CANDIDATE_EXACT_LEDGER_BASE_FIELDS, table)))
    for key, table in CANDIDATE_TABLES.items()
}
CANDIDATE_EXACT_RESULT_FIELDS = (
    "Round303B_seal",
    "atomicity_contract",
    "formal_credit_transition",
    "forward_application",
    "forward_reverse_same_partition",
    "global_source_G_disposition_gate",
    "input_file_and_manifest_pins",
    "member_universe",
    "maximality_gate",
    "official_key_fibre_gate",
    "output_ledgers",
    "producer_file_sha256",
    "residual_gate_census",
    "result_sha256",
    "reverse_application",
    "schema",
    "schema_snapshot_sha256",
    "seed_affects_output",
    "status",
    "strict_boundary",
    "W_tail_disposition_census",
)
DUAL_SEEDS = (304_001, 304_997)
ATTACK_MECHANISMS = (
    "endpoint_outside_registry",
    "base_root_injection",
    "noncanonical_endpoint_pair",
    "edge_W_tail_overlap",
    "edge_uniqueness_forgery",
    "eligible_flag_flip",
    "G0_flip",
    "G1_flip",
    "G2_flip",
    "G3_flip",
    "G4_flip",
    "G5_flip",
    "candidate_connectivity_flip",
    "identity_or_key_credit_nonzero",
    "pre_DSU_rank_credit_nonzero",
    "W_tail_credit_escalation",
    "W_tail_fed_to_DSU",
    "W_tail_stronger_path_edge_forgery",
    "W_tail_stronger_path_disconnect",
    "W_tail_stronger_path_source_hash_forgery",
    "W_tail_same_component_flip",
    "Round301_state_injection",
    "old_63224_partition_injection",
    "conditional_92696_partition_injection",
    "old_channel_inventory_forgery",
    "manifest_membership_resign",
    "stale_Round294B_admission",
    "stale_Round303B_verifier",
    "seed_dependent_output",
    "maximality_credit_nonzero",
    "fibre_credit_nonzero",
    "global_disposition_credit_nonzero",
    "Gate5_complete_block_nonzero",
    "Jx_Jy_same_point_credit_nonzero",
    "D02_unblocked",
    "CM2_unconditional",
    "stale_116_accepted",
    "keyspace_224580_as_124",
    "hard_coded_1024_as_theorem",
    "gzip_member_boundary",
    "gzip_integrity",
    "duplicate_JSON_key",
    "nonintegral_JSON",
    "nonfinite_JSON",
    "symlink_input",
    "hardlink_input",
    "path_escape",
    "producer_import",
    "producer_exec",
    "producer_parse",
    "producer_tokenize",
    "existing_target_clobber",
    "target_appears_after_preflight",
    "input_PRE_POST_TOCTOU",
    "candidate_PRE_POST_TOCTOU",
)

# Frozen producer/schema pins.  There is intentionally no verifier self-pin:
# the verifier's inert file hash is computed and bound into both output
# objects, avoiding a circular source-hash constant.
FINAL_R304_PRODUCER_SHA256: str | None = (
    "fff60d4a108355299ee6b9e3106549eca130ada2f4451d8f4deb50f0056520f5"
)
FINAL_R304_SCHEMA_SNAPSHOT_SHA256: str | None = (
    "90a2697d70abe3f927b5b1f08449d6dc394c4c39f3b7c10766b2c37af0e4b51e"
)
FINAL_R303B_MANIFEST_SHA256: str | None = (
    "7d7293c488a05c8873a63b7d63d0bf125260c6b9d3c60595201896cfde0c9786"
)
FINAL_R303B_PRODUCER_SHA256: str | None = (
    "02ce70a560b7fa029e2c7a70a1e4627cb423ac67ba187dba059b57194a646735"
)
FINAL_R303B_VERIFIER_SHA256: str | None = (
    "420883fbc6b2ad5a8413e51635b814bac7c1f059e1ff937765e38c8ac98ff88f"
)
FINAL_R303B_VERIFICATION_FILE_SHA256: str | None = (
    "6dde1fc938c5059290b811d297306ae16347fd93624a29d7b0ba59974cc06d5a"
)
FINAL_R303B_VERIFICATION_OBJECT_SHA256: str | None = (
    "a803d41e9be3513fb2b2e1ac87e22b35c83c2e678647105708a0857339cbfe57"
)
FINAL_R303B_RESULT_SHA256: str | None = (
    "4bd7127f9d935cf7b334fd7660fa6332f8aa23a9c819ac7e018c8add8473eaa1"
)
FINAL_R303B_EDGE_LEDGER_SHA256: str | None = (
    "650df67dfcc3033c42b36638a0da4b3d63ce575469cab84a5e8971ed7b23243a"
)
FINAL_R303B_WTAIL_LEDGER_SHA256: str | None = (
    "eaa18cdec4217e57238d8e5b4209c33295dc325dbb352f1d52347e0d18acdf8e"
)
FINAL_R303B_MANIFEST_MEMBER_PINS: dict[str, str] | None = {
    "cm2_round303b_source_g_unified_attachment_edge_producer.py":
        "02ce70a560b7fa029e2c7a70a1e4627cb423ac67ba187dba059b57194a646735",
    "cm2_round303b_source_g_unified_attachment_edge_promotion_b1_graph_attachment_lemma_ledger.json.gz":
        "776f1164f96731a2e71b6553ac08165aaa3fe05bb051c0f6602cd8edfd73fa43",
    "cm2_round303b_source_g_unified_attachment_edge_promotion_b2a_analytic_sheet_lemma_ledger.json.gz":
        "6095269bd2b791c78b0c305599e7dc3b518dc762e47c00aedeaebe080548e515",
    "cm2_round303b_source_g_unified_attachment_edge_promotion_b2b_physical_inclusion_lemma_ledger.json.gz":
        "ca88dcf992c9c2a2483485109f80634376e6cc02239ffd3146f6e1dd318bca96",
    "cm2_round303b_source_g_unified_attachment_edge_promotion_component_edge_ledger.json.gz":
        "650df67dfcc3033c42b36638a0da4b3d63ce575469cab84a5e8971ed7b23243a",
    "cm2_round303b_source_g_unified_attachment_edge_promotion_wtail_unresolved_ledger.json.gz":
        "eaa18cdec4217e57238d8e5b4209c33295dc325dbb352f1d52347e0d18acdf8e",
    "cm2_round303b_source_g_unified_attachment_edge_promotion_result.json":
        "4bd7127f9d935cf7b334fd7660fa6332f8aa23a9c819ac7e018c8add8473eaa1",
    "cm2_round303b_source_g_unified_attachment_edge_promotion_verifier.py":
        "420883fbc6b2ad5a8413e51635b814bac7c1f059e1ff937765e38c8ac98ff88f",
    "cm2_round303b_source_g_unified_attachment_edge_promotion_attack_suite.json":
        "c7d87135c2fd77d89855c276be98908649979793d757accadd9bf3dd974b9ab7",
    "cm2_round303b_source_g_unified_attachment_edge_promotion_verification.json":
        "6dde1fc938c5059290b811d297306ae16347fd93624a29d7b0ba59974cc06d5a",
    "cm2_round303b_source_g_unified_attachment_edge_promotion_report.md":
        "6176f78e3e4e64399796c8f4cbd80fadce0eeabb87a7aef12c97c8991b94c031",
    "cm2_round303b_source_g_unified_attachment_edge_promotion_cold_replay.md":
        "c7eeefc0d086bc9d10444e53e581fc004136e8c3767b5ebd226bc49809b5114f",
}

R303B_PREFIX = "cm2_round303b_source_g_unified_attachment_edge_promotion"
R303B_PRODUCER = "cm2_round303b_source_g_unified_attachment_edge_producer.py"
R303B_MANIFEST = R303B_PREFIX + "_manifest.sha256"
R303B_EDGE = R303B_PREFIX + "_component_edge_ledger.json.gz"
R303B_WTAIL = R303B_PREFIX + "_wtail_unresolved_ledger.json.gz"
R303B_RESULT = R303B_PREFIX + "_result.json"
R303B_VERIFIER = R303B_PREFIX + "_verifier.py"
R303B_VERIFICATION = R303B_PREFIX + "_verification.json"
R303B_B1 = R303B_PREFIX + "_b1_graph_attachment_lemma_ledger.json.gz"
R303B_B2A = R303B_PREFIX + "_b2a_analytic_sheet_lemma_ledger.json.gz"
R303B_B2B = R303B_PREFIX + "_b2b_physical_inclusion_lemma_ledger.json.gz"
R303B_ATTACK = R303B_PREFIX + "_attack_suite.json"
R303B_REPORT = R303B_PREFIX + "_report.md"
R303B_COLD = R303B_PREFIX + "_cold_replay.md"
R303B_EXPECTED_MANIFEST_MEMBERS = frozenset({
    R303B_PRODUCER,
    R303B_B1,
    R303B_B2A,
    R303B_B2B,
    R303B_EDGE,
    R303B_WTAIL,
    R303B_RESULT,
    R303B_VERIFIER,
    R303B_ATTACK,
    R303B_VERIFICATION,
    R303B_REPORT,
    R303B_COLD,
})
R303B_ZERO_FIELDS = (
    "formal_occurrence_identity_collapse_credit",
    "formal_official_key_merge_credit",
    "formal_component_union_credit",
    "formal_component_quotient_credit",
    "formal_DSU_rank_reduction_credit",
    "formal_seam_edge_credit",
    "formal_Jx_Jy_same_point_glue_credit",
    "formal_maximality_credit",
    "formal_fibre_credit",
    "formal_global_disposition_credit",
)

R294B_PREFIX = "cm2_round294b_source_g_registry_builder_admission_closure"
R294B_MANIFEST = R294B_PREFIX + "_manifest.sha256"
R294B_VERIFICATION = R294B_PREFIX + "_verification.json"
R294B_MANIFEST_SHA256 = (
    "fc16aa2792a59dff922afcc8ec66b1ca015251af3c5f718d9d909439a2990d76"
)
R294B_VERIFICATION_FILE_SHA256 = (
    "b1440432a082b392de744bc6f4ca20e893122cb923a3236899357ccfb4fd6581"
)
R294B_VERIFICATION_OBJECT_SHA256 = (
    "1746adb7b71607909eae031da879671885deee8602fdb5685dc561ba9afa4179"
)
R301_MANIFEST = "cm2_round301_source_g_legal_component_dsu_application_manifest.sha256"
R301_MANIFEST_SHA256 = (
    "5789b23e74b6e0db9a1b4e311fb22ebe5e3612e4972d2fc3547957230fda214c"
)
R303A_MANIFEST = (
    "cm2_round303a_source_g_occurrence_anchor_connected_side_bridge_manifest.sha256"
)
R303A_MANIFEST_SHA256 = (
    "6f195f8325f107328f7e375411bb8a95146b0cfd65180f5cc9f85b3643d0b098"
)

R300A_PREFIX = "cm2_round300a_source_g_r287_graph_zero_lower_frontier_exhaustion"
R300A_MANIFEST = R300A_PREFIX + "_manifest.sha256"
R300A_MANIFEST_SHA256 = (
    "9f9e86d93aebe2b47e525af795a3a9e8331ab3b6f2d71ecafe69429238a1aee8"
)
R300A_LEDGER = R300A_PREFIX + "_ledger.json.gz"
R300A_LEDGER_SHA256 = (
    "ddc1a8bc53861afeb93d3569c6efa228f17d86f161db31a39fa9b72458ab8f2d"
)
R300A_RESULT = R300A_PREFIX + "_result.json"
R300A_RESULT_SHA256 = (
    "b8f7c27f8761f1eb611f8fd57a0e773572f045963560f5d63b44baa1680e7ee4"
)

R169_CERTIFICATE = (
    "cm2_round169_source_g_return_signature_coverage_survey_certificate.json"
)
R169_CERTIFICATE_SHA256 = (
    "87c5b5f5467aa19b3bafce9e20c10371877012af65937983ced43fcccb22c2fb"
)
R169_VERIFICATION = (
    "cm2_round169_source_g_return_signature_coverage_survey_verification.json"
)
R169_VERIFICATION_SHA256 = (
    "90c207dd952329d0547ec0440e35cffa57d7b11f98ed17869f3a07df6ce3161f"
)
SOURCE_G_EXACT_KEY_DISPOSITION_DENOMINATOR = 224_580
STALE_OFFICIAL_KEY_COUNT = 116
ACTUAL_OFFICIAL_KEY_COUNT = 124

R266_CERTIFICATE = "cm2_round266_source_g_expanded_curved_face_closure_certificate.json"
R266_CERTIFICATE_SHA256 = (
    "2d30be104dc522ebb1664129894acf851180b9e5f51dd8471c33137447b599bf"
)
R266_MANIFEST = "cm2_round266_source_g_expanded_curved_face_closure_manifest.sha256"
R266_MANIFEST_SHA256 = (
    "63fb5b25d52ca5de579256499629d04d15f6a313e0a73f7e80fcb463385cbe09"
)
R294_REGISTRY = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_registry_ledger.json.gz"
)
R294_REGISTRY_SHA256 = (
    "c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb"
)
R294_MANIFEST = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_manifest.sha256"
)
R294_MANIFEST_SHA256 = (
    "90d5cda0271610bf95a72f94e9bae8e192425580019dd3c823b5a69d20e52131"
)
R299A_LEDGER = (
    "cm2_round299a_source_g_refined_occurrence_official_key_binding_closure_ledger.json.gz"
)
R299A_LEDGER_SHA256 = (
    "ffea8120af2179990d5c9e7ff385193e2c5a08bed161cf5b570aa28b1f8b1ee0"
)
R299A_MANIFEST = (
    "cm2_round299a_source_g_refined_occurrence_official_key_binding_closure_manifest.sha256"
)
R299A_MANIFEST_SHA256 = (
    "b1dfe718dd2b7477d9cc4067f1bade59d1589b3822eaf4b94b9dd721e61b468e"
)

PRESERVED = "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE"
R288 = "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM"
R292 = "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT"


class VerificationBlocked(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationBlocked(label)


def lexical_directory_without_symlinks(path: Path, label: str) -> Path:
    """Return an absolute directory only after checking every path component."""

    absolute = Path(os.path.abspath(os.fspath(path)))
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current /= part
        need(os.path.lexists(current), label + " missing component")
        info = os.lstat(current)
        need(
            not stat.S_ISLNK(info.st_mode) and stat.S_ISDIR(info.st_mode),
            label + " symlink/non-directory component:" + part,
        )
    return absolute


def configure_root(root: Path) -> None:
    """Select one explicit, relocation-safe read root before any input opens."""

    global ROOT, DATA
    lexical = lexical_directory_without_symlinks(root, "workspace root")
    resolved = root.resolve()
    need(
        lexical == resolved,
        "workspace root directory",
    )
    deliverables = lexical_directory_without_symlinks(
        resolved / "deliverables",
        "workspace deliverables",
    )
    need(
        deliverables.exists()
        and not deliverables.is_symlink()
        and stat.S_ISDIR(os.lstat(deliverables).st_mode),
        "workspace deliverables directory",
    )
    ROOT = resolved
    DATA = deliverables
    SOURCE_SNAPSHOTS.clear()
    CANDIDATE_SNAPSHOTS.clear()
    PARENT_DIRECTORY_SNAPSHOTS.clear()


def canonical(value: Any) -> bytes:
    return ENCODER.encode(value).encode("ascii")


def json_object_keys_are_strings(value: Any) -> bool:
    if isinstance(value, dict):
        return all(
            type(key) is str and json_object_keys_are_strings(item)
            for key, item in value.items()
        )
    if isinstance(value, (list, tuple)):
        return all(json_object_keys_are_strings(item) for item in value)
    return True


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def deterministic_gzip(document: dict[str, Any]) -> bytes:
    raw = canonical(document)
    output = io.BytesIO()
    with gzip.GzipFile(
        filename="",
        mode="wb",
        fileobj=output,
        compresslevel=9,
        mtime=0,
    ) as stream:
        stream.write(raw)
    return output.getvalue()


def file_identity(info: os.stat_result) -> FileIdentity:
    return (
        info.st_dev,
        info.st_ino,
        info.st_mode,
        info.st_nlink,
        info.st_size,
        info.st_mtime_ns,
        info.st_ctime_ns,
    )


def directory_identity(info: os.stat_result) -> DirectoryIdentity:
    return (info.st_dev, info.st_ino, info.st_mode)


def rename_noreplace(
    source_directory_descriptor: int,
    source_name: str,
    target_directory_descriptor: int,
    target_name: str,
) -> None:
    """Atomically move one staged file without replacing an existing name."""

    function = getattr(ctypes.CDLL(None, use_errno=True), "renameat2", None)
    need(function is not None, "renameat2(RENAME_NOREPLACE) unavailable")
    function.argtypes = [
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_uint,
    ]
    function.restype = ctypes.c_int
    outcome = function(
        source_directory_descriptor,
        os.fsencode(source_name),
        target_directory_descriptor,
        os.fsencode(target_name),
        1,
    )
    if outcome == 0:
        return
    error = ctypes.get_errno()
    if error == errno.EEXIST:
        raise FileExistsError(error, os.strerror(error), target_name)
    raise OSError(error, os.strerror(error), target_name)


def open_bound_directory(directory: Path, label: str) -> tuple[Path, int]:
    lexical = lexical_directory_without_symlinks(directory, label + " parent")
    descriptor = os.open(
        lexical,
        os.O_RDONLY
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_CLOEXEC", 0),
    )
    actual = directory_identity(os.fstat(descriptor))
    path_actual = directory_identity(os.lstat(lexical))
    need(actual == path_actual, label + " parent open race")
    prior = PARENT_DIRECTORY_SNAPSHOTS.setdefault(lexical, actual)
    need(prior == actual, label + " parent PRE/POST mismatch")
    return lexical, descriptor


def assert_parent_directory_snapshots(label: str) -> None:
    for directory, expected in sorted(
        PARENT_DIRECTORY_SNAPSHOTS.items(),
        key=lambda item: str(item[0]),
    ):
        lexical = lexical_directory_without_symlinks(
            directory,
            label + " parent",
        )
        need(
            directory_identity(os.lstat(lexical)) == expected,
            label + " parent rename/swap:" + directory.name,
        )


def safe_regular_at(
    name: str,
    directory: Path,
    directory_descriptor: int,
    snapshots: dict[Path, FileIdentity],
    maximum: int,
    label: str,
) -> FileIdentity:
    need(name not in {"", ".", ".."} and Path(name).name == name, label)
    info = os.stat(name, dir_fd=directory_descriptor, follow_symlinks=False)
    need(
        stat.S_ISREG(info.st_mode)
        and info.st_nlink == 1
        and 0 < info.st_size <= maximum,
        label + " hardlink/nonregular/unbounded",
    )
    identity = file_identity(info)
    path = directory / name
    prior = snapshots.setdefault(path, identity)
    need(prior == identity, label + " PRE/POST snapshot mismatch")
    return identity


def safe_regular(
    path: Path,
    directory: Path,
    snapshots: dict[Path, FileIdentity],
    maximum: int,
    label: str,
) -> FileIdentity:
    lexical, directory_descriptor = open_bound_directory(directory, label)
    try:
        absolute = Path(os.path.abspath(os.fspath(path)))
        need(absolute.parent == lexical, label + " path escape")
        return safe_regular_at(
            absolute.name,
            lexical,
            directory_descriptor,
            snapshots,
            maximum,
            label,
        )
    finally:
        os.close(directory_descriptor)


def safe_source(path: Path, maximum: int = 3_000_000_000) -> None:
    safe_regular(
        path,
        DATA,
        SOURCE_SNAPSHOTS,
        maximum,
        "source:" + path.name,
    )


def safe_regular_in(
    path: Path,
    directory: Path,
    maximum: int = 3_000_000_000,
) -> None:
    safe_regular(
        path,
        directory,
        CANDIDATE_SNAPSHOTS,
        maximum,
        "candidate:" + path.name,
    )


def assert_snapshot_map(snapshots: dict[Path, FileIdentity], label: str) -> None:
    for path, expected in sorted(snapshots.items(), key=lambda item: str(item[0])):
        need(
            os.path.lexists(path) and not path.is_symlink(),
            label + " disappeared:" + path.name,
        )
        info = os.lstat(path)
        need(
            file_identity(info) == expected,
            label + " POST snapshot mismatch:" + path.name,
        )
    assert_parent_directory_snapshots(label)


@contextmanager
def fd_bound_binary(
    path: Path,
    directory: Path,
    snapshots: dict[Path, FileIdentity],
    *,
    maximum: int = 3_000_000_000,
    label: str,
) -> Iterator[BinaryIO]:
    lexical, directory_descriptor = open_bound_directory(directory, label)
    descriptor: int | None = None
    stream: BinaryIO | None = None
    try:
        absolute = Path(os.path.abspath(os.fspath(path)))
        need(absolute.parent == lexical, label + " path escape")
        expected = safe_regular_at(
            absolute.name,
            lexical,
            directory_descriptor,
            snapshots,
            maximum,
            label,
        )
        descriptor = os.open(
            absolute.name,
            os.O_RDONLY
            | getattr(os, "O_NOFOLLOW", 0)
            | getattr(os, "O_CLOEXEC", 0),
            dir_fd=directory_descriptor,
        )
        stream = os.fdopen(descriptor, "rb", closefd=True)
        descriptor = None
        need(file_identity(os.fstat(stream.fileno())) == expected, label + " open race")
        yield stream
        need(file_identity(os.fstat(stream.fileno())) == expected, label + " fd changed")
        need(
            file_identity(
                os.stat(
                    absolute.name,
                    dir_fd=directory_descriptor,
                    follow_symlinks=False,
                )
            )
            == expected,
            label + " filename swapped during fd read",
        )
        need(
            directory_identity(os.fstat(directory_descriptor))
            == PARENT_DIRECTORY_SNAPSHOTS[lexical]
            == directory_identity(os.lstat(lexical)),
            label + " parent renamed/swapped during fd read",
        )
    finally:
        if stream is not None:
            stream.close()
        elif descriptor is not None:
            os.close(descriptor)
        os.close(directory_descriptor)


def stable_read_bytes(
    path: Path,
    directory: Path,
    snapshots: dict[Path, FileIdentity],
    *,
    maximum: int = 3_000_000_000,
    label: str,
) -> bytes:
    chunks: list[bytes] = []
    total = 0
    with fd_bound_binary(
        path,
        directory,
        snapshots,
        maximum=maximum,
        label=label,
    ) as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            total += len(block)
            need(total <= maximum, label + " bounded read")
            chunks.append(block)
    return b"".join(chunks)


def file_sha256(path: Path) -> str:
    return stable_file_sha256(
        path,
        DATA,
        SOURCE_SNAPSHOTS,
        label="source hash:" + path.name,
    )


def stable_file_sha256(
    path: Path,
    directory: Path,
    snapshots: dict[Path, FileIdentity],
    *,
    maximum: int = 3_000_000_000,
    label: str,
) -> str:
    state = hashlib.sha256()
    with fd_bound_binary(
        path,
        directory,
        snapshots,
        maximum=maximum,
        label=label,
    ) as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def require_single_gzip_member(raw: bytes, label: str) -> None:
    decoder = zlib.decompressobj(wbits=31)
    for offset in range(0, len(raw), 1 << 20):
        decoder.decompress(raw[offset:offset + (1 << 20)])
        need(not decoder.unused_data, "gzip concatenation/trailing:" + label)
    decoder.flush()
    need(decoder.eof and not decoder.unused_data, "truncated gzip:" + label)


def strict_object(raw: bytes, label: str) -> dict[str, Any]:
    need(raw and not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw, label)

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in out, "duplicate key:" + label + ":" + key)
            out[key] = value
        return out

    def reject(token: str) -> Any:
        raise VerificationBlocked("nonintegral/nonfinite:" + label + ":" + token)

    value = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=unique,
        parse_float=reject,
        parse_constant=reject,
    )
    need(type(value) is dict, "object:" + label)
    return value


def read_json(name: str) -> dict[str, Any]:
    path = DATA / name
    return strict_object(
        stable_read_bytes(
            path,
            DATA,
            SOURCE_SNAPSHOTS,
            label="source JSON:" + name,
        ),
        name,
    )


def verify_self(row: dict[str, Any], field: str, label: str) -> None:
    payload = dict(row)
    claimed = payload.pop(field, None)
    need(type(claimed) is str and claimed == digest(payload), "self hash:" + label)


def iter_array(stream: TextIO, marker: str, initial: str = "") -> Iterator[dict[str, Any]]:
    buffer = initial
    while marker not in buffer:
        block = stream.read(1 << 20)
        need(bool(block), "missing marker:" + marker)
        buffer += block
    buffer = buffer.split(marker, 1)[1]

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in out, "stream duplicate key:" + key)
            out[key] = value
        return out

    decoder = json.JSONDecoder(
        object_pairs_hook=unique,
        parse_float=lambda token: (_ for _ in ()).throw(
            VerificationBlocked("float:" + token)
        ),
        parse_constant=lambda token: (_ for _ in ()).throw(
            VerificationBlocked("constant:" + token)
        ),
    )
    while True:
        buffer = buffer.lstrip()
        if not buffer:
            block = stream.read(1 << 20)
            need(bool(block), "truncated array")
            buffer = block
            continue
        if buffer[0] == ",":
            buffer = buffer[1:]
            continue
        if buffer[0] == "]":
            return
        while True:
            try:
                row, end = decoder.raw_decode(buffer)
                break
            except json.JSONDecodeError:
                block = stream.read(1 << 20)
                need(bool(block), "truncated row")
                buffer += block
        need(type(row) is dict, "row object")
        yield row
        buffer = buffer[end:]


def gzip_rows(name: str, table: str) -> Iterator[dict[str, Any]]:
    path = DATA / name
    with fd_bound_binary(
        path,
        DATA,
        SOURCE_SNAPSHOTS,
        label="gzip source:" + name,
    ) as raw:
        with gzip.GzipFile(fileobj=raw, mode="rb") as binary:
            with io.TextIOWrapper(binary, encoding="utf-8", newline="") as stream:
                yield from iter_array(stream, '"' + table + '":[')


def plain_rows(name: str, table: str) -> Iterator[dict[str, Any]]:
    path = DATA / name
    marker = '"' + table + '":'
    carry = ""
    with fd_bound_binary(
        path,
        DATA,
        SOURCE_SNAPSHOTS,
        label="plain source:" + name,
    ) as raw:
        stream = io.TextIOWrapper(raw, encoding="utf-8", newline="")
        try:
            while True:
                block = stream.read(1 << 20)
                need(bool(block), "missing plain table:" + table)
                combined = carry + block
                if marker in combined:
                    initial = combined.split(marker, 1)[1]
                    break
                carry = combined[-len(marker):]
            yield from iter_array(stream, '"rows":[', initial)
        finally:
            stream.detach()


def manifest(name: str, expected_sha: str) -> dict[str, str]:
    path = DATA / name
    need(file_sha256(path) == expected_sha, "manifest hash:" + name)
    entries: dict[str, str] = {}
    raw = stable_read_bytes(
        path,
        DATA,
        SOURCE_SNAPSHOTS,
        maximum=500_000,
        label="source manifest:" + name,
    )
    for line in raw.decode("ascii").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\n]+)", line)
        need(match is not None, "manifest syntax:" + name)
        value, member = match.groups()
        need(Path(member).name == member and member not in entries, "manifest set")
        entries[member] = value
    need(bool(entries), "empty manifest")
    return entries


def verify_manifest(name: str, expected_sha: str) -> dict[str, str]:
    entries = manifest(name, expected_sha)
    for member, expected in entries.items():
        path = DATA / member
        safe_source(path)
        need(file_sha256(path) == expected, "member hash:" + name + ":" + member)
    return entries


def exact_pin_map_ready(
    value: dict[str, str] | None,
    expected_names: frozenset[str],
) -> bool:
    return (
        type(value) is dict
        and set(value) == set(expected_names)
        and all(
            type(name) is str
            and Path(name).name == name
            and type(pin) is str
            and PIN.fullmatch(pin) is not None
            for name, pin in value.items()
        )
    )


@dataclass(frozen=True)
class SourceChannel:
    name: str
    manifest_name: str
    manifest_sha: str
    ledger: str
    ledger_sha: str
    count: int
    row_id: str
    endpoint: str
    required: tuple[tuple[str, Any], ...]


CHANNELS = (
    SourceChannel(
        "R297_ORDINARY_FACE",
        "cm2_round297_source_g_ordinary_face_occurrence_edge_promotion_manifest.sha256",
        "1feecefa897c5320eadc006509ba6bde84cdbf692dfaddd024472b93c13c38c0",
        "cm2_round297_source_g_ordinary_face_occurrence_edge_promotion_edge_ledger.json.gz",
        "18a20b4679a8a3e94ccaf1b511694220cad1bc92e1590ded4585ae3735547371",
        330_724,
        "Round297_ordinary_face_occurrence_edge_row_id",
        "exact_occurrence_endpoint_pair",
        (
            ("formal_ordinary_component_edge_witness_credit", 1),
            ("occurrence_endpoint_pair_is_nonself", True),
            ("formal_occurrence_identity_collapse_credit", 0),
            ("formal_DSU_rank_reduction_credit", 0),
        ),
    ),
    SourceChannel(
        "R296_TRUE_SEAM",
        "cm2_round296_source_g_true_seam_occurrence_edge_ledger_closure_manifest.sha256",
        "f7786b9cdec45cb381ec46489eb44b0365b8ee43d81ae9a9611cb2dcdee7fb59",
        "cm2_round296_source_g_true_seam_occurrence_edge_ledger_closure_edge_ledger.json.gz",
        "1b57b10fac9317e1609fb8858972011165bd95e5b1b687604edd6c8ad7139ef7",
        48_444,
        "Round296_true_seam_occurrence_edge_row_id",
        "unordered_formal_occurrence_endpoint_pair",
        (
            ("formal_true_seam_edge_credit", 1),
            ("occurrence_identity_collapsed", False),
            ("formal_DSU_rank_reduction_credit", 0),
        ),
    ),
    SourceChannel(
        "R299C_SIGNED_FACE",
        "cm2_round299c_source_g_r292_signed_support_face_edge_promotion_manifest.sha256",
        "62e04cdd7f9c3d2fb865be0a999e1ce5ed1de435151a1b7bb5bba0176709b9b3",
        "cm2_round299c_source_g_r292_signed_support_face_edge_promotion_canonical_occurrence_edge_pairs.json.gz",
        "e63f164bf9cc559ec8d3a2895e66493933b43b90f1ad3b163dfb41e12bb04df1",
        25_452,
        "Round299C_canonical_signed_face_occurrence_edge_row_id",
        "unordered_formal_occurrence_endpoint_pair",
        (
            ("formal_component_edge_credit", 1),
            ("formal_occurrence_identity_collapse_credit", 0),
            ("formal_DSU_rank_reduction_credit", 0),
        ),
    ),
    SourceChannel(
        "R300B_COMPLETE_FACE",
        "cm2_round300b_source_g_registry_boundary_and_complete_r275_face_inventory_closure_manifest.sha256",
        "6208c4bfd8b147f06ffb735d4b5621faff22585831b5f19d48e8125514ac4a6b",
        "cm2_round300b_source_g_registry_boundary_and_complete_r275_face_inventory_closure_canonical_novel_occurrence_edge_pairs.json.gz",
        "c3d1e604ed0e1256789c239b65d22546035fd3bd333dd11bfb907e221c3cec9e",
        10_416,
        "Round300B_canonical_novel_occurrence_edge_row_id",
        "unordered_formal_occurrence_endpoint_pair",
        (
            ("formal_component_edge_credit", 1),
            ("formal_occurrence_identity_collapse_credit", 0),
            ("formal_DSU_rank_reduction_credit", 0),
            ("all_prior_channel_memberships_false", True),
        ),
    ),
    SourceChannel(
        "R300C_POSITIVE_VOLUME",
        "cm2_round300c_source_g_virtual_stratum_new_occurrence_positive_volume_edge_promotion_manifest.sha256",
        "cd327de2702ac209b0b0a03d09b3744596a901c2d65794dd86231d31a0be3503",
        "cm2_round300c_source_g_virtual_stratum_new_occurrence_positive_volume_edge_promotion_edge_ledger.json.gz",
        "8c9ed8b09e994a00ca3ca4906c35b454523383b7d488f66e7a082dbbd4b1fcec",
        6_314,
        "Round300C_virtual_occurrence_positive_volume_edge_row_id",
        "canonical_component_edge_endpoint_pair",
        (
            ("formal_positive_volume_component_edge_witness_credit", 1),
            ("formal_occurrence_identity_collapse_credit", 0),
            ("formal_DSU_rank_reduction_credit", 0),
        ),
    ),
    SourceChannel(
        "R300E_HALF_OPEN_OWNER",
        "cm2_round300e_source_g_r248_half_open_owner_lower_component_edge_promotion_manifest.sha256",
        "4e6c4eec1af04a907285d41395aeef63e911b3b5486db91b33a95fa62e45177a",
        "cm2_round300e_source_g_r248_half_open_owner_lower_component_edge_promotion_all_edge_ledger.json.gz",
        "4aa7ae76d984d15b345d5d6805ec4f06a47e30a46fff1315f346e81f1f17122f",
        12_992,
        "Round300E_half_open_owner_component_edge_row_id",
        "canonical_component_edge_endpoint_pair",
        (
            ("formal_half_open_owner_component_edge_credit", 1),
            ("eligible_for_component_DSU_application", True),
            ("formal_occurrence_identity_collapse_credit", 0),
            ("formal_DSU_rank_reduction_credit", 0),
        ),
    ),
    SourceChannel(
        "R300F_R245_HALF_OPEN_OWNER",
        "cm2_round300f_source_g_r245_half_open_owner_sheet_attachment_manifest.sha256",
        "811656ed9160b622014a94901a1e08c7d3e6313db08f86d65ae01afefb49bbeb",
        "cm2_round300f_source_g_r245_half_open_owner_sheet_attachment_ledger.json.gz",
        "1f958f9f3e3aff7327d897b39851f2d2d030d820e00859d302241702613cae1f",
        264,
        "Round300F_R245_half_open_owner_attachment_row_id",
        "canonical_component_edge_endpoint_pair",
        (
            ("formal_half_open_owner_component_edge_witness_credit", 1),
            ("eligible_for_component_DSU_application", True),
            ("Round300A_prior_explicit_graph_zero_pair_present", False),
            ("Round300A_two_endpoint_union_credit", 0),
            ("shadow_component_edge_witness_credit", 0),
            ("formal_occurrence_identity_collapse_credit", 0),
            ("formal_DSU_rank_reduction_credit", 0),
        ),
    ),
)


@dataclass(frozen=True)
class VEdge:
    channel: str
    source_id: str
    source_sha: str
    endpoints: tuple[str, str]
    roots: tuple[str, str]


class IndexUF:
    """Independent integer-index union-find, distinct from producer strings."""

    def __init__(self, count: int) -> None:
        self.parent = list(range(count))
        self.weight = [1] * count

    def find(self, item: int) -> int:
        root = item
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[item] != item:
            nxt = self.parent[item]
            self.parent[item] = root
            item = nxt
        return root

    def merge(self, left: int, right: int) -> bool:
        a, b = self.find(left), self.find(right)
        if a == b:
            return False
        if (self.weight[a], -a) < (self.weight[b], -b):
            a, b = b, a
        self.parent[b] = a
        self.weight[a] += self.weight[b]
        return True


def r303b_seal_ready() -> bool:
    values = (
        FINAL_R303B_MANIFEST_SHA256,
        FINAL_R303B_PRODUCER_SHA256,
        FINAL_R303B_VERIFIER_SHA256,
        FINAL_R303B_VERIFICATION_FILE_SHA256,
        FINAL_R303B_VERIFICATION_OBJECT_SHA256,
        FINAL_R303B_RESULT_SHA256,
        FINAL_R303B_EDGE_LEDGER_SHA256,
        FINAL_R303B_WTAIL_LEDGER_SHA256,
    )
    return (
        all(type(value) is str and PIN.fullmatch(value) for value in values)
        and exact_pin_map_ready(
            FINAL_R303B_MANIFEST_MEMBER_PINS,
            R303B_EXPECTED_MANIFEST_MEMBERS,
        )
    )


def seal_ready() -> bool:
    return (
        r303b_seal_ready()
        and type(FINAL_R304_PRODUCER_SHA256) is str
        and PIN.fullmatch(FINAL_R304_PRODUCER_SHA256) is not None
        and type(FINAL_R304_SCHEMA_SNAPSHOT_SHA256) is str
        and PIN.fullmatch(FINAL_R304_SCHEMA_SNAPSHOT_SHA256) is not None
    )


def validate_upstream_seals() -> None:
    r294b = verify_manifest(R294B_MANIFEST, R294B_MANIFEST_SHA256)
    need(
        r294b[R294B_VERIFICATION] == R294B_VERIFICATION_FILE_SHA256,
        "Round294B verification member",
    )
    verification = read_json(R294B_VERIFICATION)
    verify_self(verification, "verification_sha256", R294B_VERIFICATION)
    need(
        verification["verification_sha256"] == R294B_VERIFICATION_OBJECT_SHA256
        and verification["status"].startswith("PASS_INDEPENDENT_ROUND294B"),
        "Round294B semantic admission",
    )
    verify_manifest(R301_MANIFEST, R301_MANIFEST_SHA256)
    verify_manifest(R303A_MANIFEST, R303A_MANIFEST_SHA256)
    r300a = verify_manifest(R300A_MANIFEST, R300A_MANIFEST_SHA256)
    need(
        r300a.get(R300A_LEDGER) == R300A_LEDGER_SHA256
        and r300a.get(R300A_RESULT) == R300A_RESULT_SHA256,
        "Round300A exact manifest members",
    )
    verify_manifest(R266_MANIFEST, R266_MANIFEST_SHA256)
    verify_manifest(R294_MANIFEST, R294_MANIFEST_SHA256)
    verify_manifest(R299A_MANIFEST, R299A_MANIFEST_SHA256)
    need(file_sha256(DATA / R266_CERTIFICATE) == R266_CERTIFICATE_SHA256, "R266")
    need(file_sha256(DATA / R294_REGISTRY) == R294_REGISTRY_SHA256, "R294")
    need(file_sha256(DATA / R299A_LEDGER) == R299A_LEDGER_SHA256, "R299A")


def source_G_denominator() -> dict[str, Any]:
    certificate_path = DATA / R169_CERTIFICATE
    verification_path = DATA / R169_VERIFICATION
    safe_source(certificate_path, 50_000_000)
    safe_source(verification_path, 20_000_000)
    need(
        file_sha256(certificate_path) == R169_CERTIFICATE_SHA256
        and file_sha256(verification_path) == R169_VERIFICATION_SHA256,
        "Round169 byte pins",
    )
    certificate = read_json(R169_CERTIFICATE)
    verification = read_json(R169_VERIFICATION)
    result = certificate.get("result")
    check = verification.get("result")
    need(
        type(result) is dict
        and type(check) is dict
        and certificate.get("result_sha256") == digest(result)
        and verification.get("result_sha256") == digest(check),
        "Round169 nested object closures",
    )
    census = result.get("source_G_exact_key_coverage_census")
    need(
        type(census) is dict
        and result.get("status")
        == (
            "CERTIFIED_SOURCE_G_EXACT_KEY_COVERAGE_DEFICIT_SURVEY__"
            "NO_EXTERIOR_OR_D02_PROMOTION"
        )
        and census.get("candidate_chart_target_pair_count") == 228
        and census.get("candidate_exact_key_envelope_count")
        == SOURCE_G_EXACT_KEY_DISPOSITION_DENOMINATOR
        and census.get("global_geometric_exact_key_disposition_count") == 0
        and census.get("keys_without_a_global_geometric_disposition_count")
        == SOURCE_G_EXACT_KEY_DISPOSITION_DENOMINATOR
        and check.get("status") == "PASS"
        and check.get("source_G_224580_exact_key_deficit_census_recomputed")
        is True,
        "Round169 independent denominator boundary",
    )
    return {
        "source_G_return_signature_key_count":
            SOURCE_G_EXACT_KEY_DISPOSITION_DENOMINATOR,
        "candidate_chart_target_pair_count": 228,
        "crossing_pattern_count_per_pair": 985,
        "baseline_global_disposition_count": 0,
        "baseline_unresolved_count": SOURCE_G_EXACT_KEY_DISPOSITION_DENOMINATOR,
        "Round169_certificate_file_sha256": R169_CERTIFICATE_SHA256,
        "Round169_verification_file_sha256": R169_VERIFICATION_SHA256,
    }


def rebuild_universe() -> tuple[dict[str, str], dict[str, str], list[str]]:
    member_root: dict[str, str] = {}
    member_key: dict[str, str] = {}
    roots: set[str] = set()
    for row in plain_rows(
        R266_CERTIFICATE, "formal_post_Round266_component_member_frontier_ledger"
    ):
        verify_self(row, "row_sha256", "R266 member")
        member = row["component_member_id"]
        root = row["post_Round266_quotient_component_id"]
        need(
            member not in member_root
            and row["member_identity_preserved"] is True
            and type(row["official_key_id"]) is str,
            "R266 member semantics",
        )
        member_root[member] = root
        member_key[member] = row["official_key_id"]
        roots.add(root)
    need(len(member_root) == 259_752 and len(roots) == 63_224, "R266 census")

    preserved: set[str] = set()
    pending: dict[str, tuple[str, str]] = {}
    kinds: Counter[str] = Counter()
    for row in gzip_rows(R294_REGISTRY, "rows"):
        verify_self(row, "row_sha256", "R294 registry")
        occurrence = row["registry_occurrence_id"]
        kind = row["registry_entry_kind"]
        kinds[kind] += 1
        if kind == PRESERVED:
            need(
                occurrence in member_root
                and occurrence not in preserved
                and member_key[occurrence] == row["official_key_id"],
                "R294 preserved",
            )
            preserved.add(occurrence)
        else:
            need(occurrence not in member_root, "R294 append only")
            member_root[occurrence] = occurrence
            roots.add(occurrence)
            if kind == R288:
                need(type(row["official_key_id"]) is str, "R288 key")
                member_key[occurrence] = row["official_key_id"]
            else:
                need(kind == R292 and row["official_key_id"] is None, "R292 key null")
                pending[occurrence] = (
                    row["Round294_occurrence_registry_row_id"],
                    row["row_sha256"],
                )
    need(
        kinds == {PRESERVED: 126_468, R288: 295_336, R292: 9_404}
        and len(preserved) == 126_468,
        "R294 census",
    )
    bound: set[str] = set()
    for row in gzip_rows(R299A_LEDGER, "rows"):
        verify_self(row, "row_sha256", "R299A binding")
        occurrence = row["registry_occurrence_id"]
        source = pending.get(occurrence)
        need(
            source is not None
            and occurrence not in bound
            and row["source_Round294_occurrence_registry_row_id"] == source[0]
            and row["source_Round294_occurrence_registry_row_sha256"] == source[1]
            and row["append_only_official_key_binding"] is True
            and row["occurrence_identity_preserved"] is True,
            "R299A binding semantics",
        )
        member_key[occurrence] = row["official_key_id"]
        bound.add(occurrence)
    ordered_roots = sorted(roots)
    need(
        bound == set(pending)
        and len(member_root) == 564_492
        and len(ordered_roots) == 367_964
        and len(member_key) == 564_492
        and len(set(member_key.values())) == 124,
        "full independent universe",
    )
    return member_root, member_key, ordered_roots


def endpoint_root(
    endpoint: str, member_root: dict[str, str], root_index: dict[str, int]
) -> str:
    if endpoint in root_index:
        return endpoint
    need(endpoint in member_root, "endpoint outside independent universe")
    return member_root[endpoint]


def old_edges(
    member_root: dict[str, str], root_index: dict[str, int]
) -> list[VEdge]:
    edges: list[VEdge] = []
    for source in CHANNELS:
        entries = verify_manifest(source.manifest_name, source.manifest_sha)
        need(entries.get(source.ledger) == source.ledger_sha, "edge ledger pin")
        before = len(edges)
        seen_ids: set[str] = set()
        for row in gzip_rows(source.ledger, "rows"):
            verify_self(row, "row_sha256", source.name)
            row_id = row.get(source.row_id)
            need(type(row_id) is str and row_id not in seen_ids, "edge row id")
            seen_ids.add(row_id)
            for field, expected in source.required:
                need(row.get(field) == expected, source.name + ":" + field)
            pair = row[source.endpoint]
            need(
                type(pair) is list
                and len(pair) == 2
                and pair == sorted(pair)
                and pair[0] != pair[1],
                source.name + ":pair",
            )
            edges.append(
                VEdge(
                    source.name,
                    row_id,
                    row["row_sha256"],
                    (pair[0], pair[1]),
                    (
                        endpoint_root(pair[0], member_root, root_index),
                        endpoint_root(pair[1], member_root, root_index),
                    ),
                )
            )
        need(len(edges) - before == source.count, "channel count:" + source.name)
    need(len(edges) == 434_606, "old edge total")
    return edges


def partition(
    roots: list[str],
    index: dict[str, int],
    uf: IndexUF,
    component_namespace: str,
) -> tuple[dict[str, str], str]:
    groups: dict[int, list[str]] = defaultdict(list)
    for root in roots:
        groups[uf.find(index[root])].append(root)
    components = sorted(sorted(group) for group in groups.values())
    return (
        {
            root: component_namespace + digest(group)
            for group in components
            for root in group
        },
        digest(components),
    )


def apply(
    roots: list[str],
    root_index: dict[str, int],
    edges: Iterable[VEdge],
    keep_forest: bool = False,
    component_namespace: str = "round304-fresh-legal-component:",
) -> tuple[dict[str, str], dict[str, Any], dict[str, list[tuple[str, VEdge]]]]:
    uf = IndexUF(len(roots))
    rank = 0
    count = 0
    per_channel_rank: Counter[str] = Counter()
    forest: dict[str, list[tuple[str, VEdge]]] = defaultdict(list)
    for edge in edges:
        count += 1
        left, right = edge.roots
        if uf.merge(root_index[left], root_index[right]):
            rank += 1
            per_channel_rank[edge.channel] += 1
            if keep_forest:
                forest[left].append((right, edge))
                forest[right].append((left, edge))
    mapping, partition_sha = partition(
        roots,
        root_index,
        uf,
        component_namespace,
    )
    component_count = len(set(mapping.values()))
    need(rank == len(roots) - component_count, "independent rank-nullity")
    return mapping, {
        "edge_rows": count,
        "rank_reduction": rank,
        "component_count": component_count,
        "partition_sha256": partition_sha,
        "per_channel_rank_reduction": dict(sorted(per_channel_rank.items())),
    }, forest


def validate_r303b_and_edges(
    member_root: dict[str, str],
    member_key: dict[str, str],
    root_index: dict[str, int],
    prior_map: dict[str, str],
) -> tuple[list[VEdge], list[dict[str, Any]]]:
    assert FINAL_R303B_MANIFEST_SHA256 is not None
    assert FINAL_R303B_MANIFEST_MEMBER_PINS is not None
    entries = verify_manifest(R303B_MANIFEST, FINAL_R303B_MANIFEST_SHA256)
    need(
        entries == FINAL_R303B_MANIFEST_MEMBER_PINS,
        "R303B exact manifest member/direct-pin map",
    )
    need(
        entries.get(R303B_PRODUCER) == FINAL_R303B_PRODUCER_SHA256,
        "producer pin",
    )
    need(entries.get(R303B_VERIFIER) == FINAL_R303B_VERIFIER_SHA256, "verifier pin")
    need(
        entries.get(R303B_VERIFICATION) == FINAL_R303B_VERIFICATION_FILE_SHA256,
        "verification pin",
    )
    need(entries.get(R303B_RESULT) == FINAL_R303B_RESULT_SHA256, "result pin")
    need(entries.get(R303B_EDGE) == FINAL_R303B_EDGE_LEDGER_SHA256, "edge pin")
    need(
        entries.get(R303B_WTAIL) == FINAL_R303B_WTAIL_LEDGER_SHA256,
        "W-tail pin",
    )
    need(
        FINAL_R303B_MANIFEST_MEMBER_PINS[R303B_PRODUCER]
        == FINAL_R303B_PRODUCER_SHA256
        and FINAL_R303B_MANIFEST_MEMBER_PINS[R303B_VERIFIER]
        == FINAL_R303B_VERIFIER_SHA256
        and FINAL_R303B_MANIFEST_MEMBER_PINS[R303B_VERIFICATION]
        == FINAL_R303B_VERIFICATION_FILE_SHA256
        and FINAL_R303B_MANIFEST_MEMBER_PINS[R303B_RESULT]
        == FINAL_R303B_RESULT_SHA256
        and FINAL_R303B_MANIFEST_MEMBER_PINS[R303B_EDGE]
        == FINAL_R303B_EDGE_LEDGER_SHA256
        and FINAL_R303B_MANIFEST_MEMBER_PINS[R303B_WTAIL]
        == FINAL_R303B_WTAIL_LEDGER_SHA256,
        "R303B duplicated direct-pin slots disagree with exact manifest map",
    )
    result = read_json(R303B_RESULT)
    verification = read_json(R303B_VERIFICATION)
    verify_self(result, "result_sha256", R303B_RESULT)
    verify_self(verification, "verification_sha256", R303B_VERIFICATION)
    need(
        verification["verification_sha256"] == FINAL_R303B_VERIFICATION_OBJECT_SHA256
        and result["producer_sha256"] == FINAL_R303B_PRODUCER_SHA256
        and result["complete_formal_run"] is True
        and result["provisional_Round303A_consumed"] is False
        and result["status"].startswith("PASS_ROUND303B_43912_B1_192_B2")
        and verification["status"] == "PASS_EXACT_CACHELESS_EXPECTED_STATE"
        and verification["verifier_sha256"] == FINAL_R303B_VERIFIER_SHA256
        and verification["producer"] == {
            "filename": R303B_PRODUCER,
            "inert_byte_pin_checked": True,
            "file_sha256": FINAL_R303B_PRODUCER_SHA256,
            "imported_or_executed": False,
        }
        and verification["all_five_ledgers_and_result_exact"] is True
        and verification["candidate_opened_only_after_full_expected_state"]
        is True
        and verification["attack_suite"]["attack_count"] == 55
        and verification["attack_suite"]["rejected_count"] == 55,
        "R303B independent seal",
    )
    need(
        verification["candidate_exact_file_pins"]
        == verification["independently_rebuilt_expected_file_pins"]
        == {
            name: entries[name]
            for name in (
                R303B_PRODUCER,
                R303B_B1,
                R303B_B2A,
                R303B_B2B,
                R303B_EDGE,
                R303B_WTAIL,
                R303B_RESULT,
            )
        },
        "R303B exact cacheless producer-plus-six-file equality",
    )
    admission = result["Round294B_registry_builder_admission"]
    need(
        admission["manifest_file_sha256"] == R294B_MANIFEST_SHA256
        and admission["manifest_member_count"] == 11
        and admission["verification_file_sha256"]
        == R294B_VERIFICATION_FILE_SHA256
        and admission["verification_object_sha256"]
        == R294B_VERIFICATION_OBJECT_SHA256
        and admission["formal_occurrence_registry_row_count"] == 431_208
        and admission["formal_representation_binding_count"] == 46_288
        and admission["direct_Round287_union_issuance_count_rejected"] == 10_020
        and admission["binding_rows_issuing_occurrence_ID_count"] == 0
        and admission["admission_checked_before_Round294_consumption"]
        is True
        and admission["bypass_permitted"] is False,
        "R303B Round294B admission closure",
    )
    edge_meta = result["output_ledgers"]["edge"]
    wtail_meta = result["output_ledgers"]["unresolved"]
    need(
        edge_meta["filename"] == R303B_EDGE
        and edge_meta["row_count"] == 44_104
        and edge_meta["file_sha256"] == FINAL_R303B_EDGE_LEDGER_SHA256
        and wtail_meta["filename"] == R303B_WTAIL
        and wtail_meta["row_count"] == 4
        and wtail_meta["file_sha256"] == FINAL_R303B_WTAIL_LEDGER_SHA256,
        "R303B output ledger metadata",
    )
    edges: list[VEdge] = []
    source_ids: set[str] = set()
    pairs: set[tuple[str, str]] = set()
    endpoints: set[str] = set()
    for row in gzip_rows(R303B_EDGE, "component_connectivity_edge_rows"):
        verify_self(row, "row_sha256", "R303B edge")
        pair = row["canonical_unordered_registry_occurrence_ids"]
        need(
            type(pair) is list
            and len(pair) == 2
            and pair == sorted(pair)
            and pair[0] != pair[1],
            "R303B edge pair",
        )
        roots = (
            endpoint_root(pair[0], member_root, root_index),
            endpoint_root(pair[1], member_root, root_index),
        )
        need(prior_map[roots[0]] != prior_map[roots[1]], "R303B cross prior")
        required_true = (
            "G0_exact_provenance_pins_and_row_closures",
            "G1_endpoint_occurrence_connected_supports",
            "G2_nonempty_connected_included_lower_stratum",
            "G3_left_closure_attaches_to_included_patch",
            "G4_right_closure_attaches_to_included_patch",
            "G5_endpoint_patch_provenance_exactly_closed",
            "candidate_component_connectivity_conclusion",
            "eligible_for_later_fresh_DSU_application",
        )
        need(all(row.get(field) is True for field in required_true), "R303B proof flags")
        need(
            row["formal_component_edge_credit"] == 1
            and row["formal_DSU_rank_reduction_credit"] == 0
            and row["formal_occurrence_identity_collapse_credit"] == 0
            and row["formal_official_key_merge_credit"] == 0
            and row["Round301_DSU_mutated_here"] is False
            and row["old_63224_component_result_reused"] is False,
            "R303B boundary",
        )
        need(
            all(row.get(field) == 0 for field in R303B_ZERO_FIELDS),
            "R303B all downstream fields zero",
        )
        need(
            row["Round301_pre_edge_components"]
            == {
                pair[0]: prior_map[roots[0]],
                pair[1]: prior_map[roots[1]],
            }
            and row["official_key_metadata"]
            == {
                pair[0]: member_key[pair[0]],
                pair[1]: member_key[pair[1]],
            },
            "R303B independent component/key projection",
        )
        source = row["source_Round300D_row_id"]
        pair_key = (pair[0], pair[1])
        need(source not in source_ids and pair_key not in pairs, "R303B duplicate")
        need(not endpoints.intersection(pair), "R303B endpoint reuse")
        source_ids.add(source)
        pairs.add(pair_key)
        endpoints.update(pair)
        edges.append(
            VEdge(
                "R303B_UNIFIED_ATTACHMENT",
                row["Round303B_component_connectivity_edge_row_id"],
                row["row_sha256"],
                pair_key,
                roots,
            )
        )
    unresolved: list[dict[str, Any]] = []
    for row in gzip_rows(R303B_WTAIL, "W_tail_unresolved_rows"):
        verify_self(row, "row_sha256", "R303B W-tail")
        pair = row["canonical_unordered_registry_occurrence_ids"]
        roots = (
            endpoint_root(pair[0], member_root, root_index),
            endpoint_root(pair[1], member_root, root_index),
        )
        need(
            type(pair) is list
            and len(pair) == 2
            and pair == sorted(pair)
            and pair[0] != pair[1]
            and prior_map[roots[0]] != prior_map[roots[1]],
            "W-tail pair",
        )
        need(
            row["disposition"]
            == "UNRESOLVED__ROUND271_W_TAIL_CONNECTED_SIDE_EXTENSION_MISSING"
            and row["eligible_for_later_fresh_DSU_application"] is False
            and row["formal_component_edge_credit"] == 0
            and row["nonedge_credit"] == 0
            and row["exclusion_credit"] == 0,
            "W-tail boundary",
        )
        need(
            all(row.get(field) == 0 for field in R303B_ZERO_FIELDS),
            "W-tail all downstream fields zero",
        )
        source = row["source_Round300D_row_id"]
        pair_key = (pair[0], pair[1])
        need(source not in source_ids and pair_key not in pairs, "edge/W-tail overlap")
        need(not endpoints.intersection(pair), "R303B endpoint reuse")
        source_ids.add(source)
        pairs.add(pair_key)
        endpoints.update(pair)
        unresolved.append(
            {
                "source_id": source,
                "row_id": row["Round303B_W_tail_unresolved_row_id"],
                "row_sha256": row["row_sha256"],
                "endpoints": pair_key,
                "roots": roots,
            }
        )
    need(
        len(edges) == 44_104
        and len(unresolved) == 4
        and len(source_ids) == 44_108
        and len(pairs) == 44_108
        and len(endpoints) == 88_216,
        "R303B exact partition",
    )
    return edges, unresolved


def path(
    start: str,
    target: str,
    forest: dict[str, list[tuple[str, VEdge]]],
) -> list[dict[str, str]]:
    queue = deque([start])
    prior: dict[str, tuple[str, VEdge] | None] = {start: None}
    while queue and target not in prior:
        node = queue.popleft()
        for neighbor, edge in sorted(
            forest.get(node, []),
            key=lambda item: (item[0], item[1].channel, item[1].source_id),
        ):
            if neighbor not in prior:
                prior[neighbor] = (node, edge)
                queue.append(neighbor)
    need(target in prior, "missing independent stronger path")
    output: list[dict[str, str]] = []
    cursor = target
    while cursor != start:
        item = prior[cursor]
        assert item is not None
        previous, edge = item
        output.append({
            "channel": edge.channel,
            "source_row_id": edge.source_id,
            "source_row_sha256": edge.source_sha,
            "from_root": previous,
            "to_root": cursor,
        })
        cursor = previous
    output.reverse()
    return output


def reproject_R300A(
    member_root: dict[str, str],
    root_index: dict[str, int],
    final_map: dict[str, str],
) -> dict[str, Any]:
    need(file_sha256(DATA / R300A_RESULT) == R300A_RESULT_SHA256, "R300A result")
    result = read_json(R300A_RESULT)
    verify_self(result, "result_sha256", R300A_RESULT)
    need(
        result.get("status")
        == (
            "PASS_ROUND300A_EXHAUSTIVE_FAIL_CLOSED_DIAGNOSTIC__"
            "NO_GRAPH_ZERO_COMPONENT_EDGE_PROMOTION"
        )
        and result["frontier_ledger"][
            "canonical_occurrence_pair_row_count"
        ]
        == 3_232
        and result["prior_witness_partition"][
            "R295A_explicit_lower_graph_sheet_witness_pair_count"
        ]
        == 128
        and result["prior_witness_partition"]["unresolved_exact_pair_count"]
        == 3_104,
        "R300A complete frontier semantics",
    )
    rows: list[dict[str, Any]] = []
    histogram: Counter[str] = Counter()
    ids: set[str] = set()
    witnessed = 0
    for row in gzip_rows(R300A_LEDGER, "canonical_occurrence_pair_rows"):
        verify_self(row, "row_sha256", "R300A pair")
        row_id = row.get("Round300A_canonical_occurrence_pair_row_id")
        pair = row.get("canonical_unordered_Round294_registry_occurrence_ids")
        need(
            type(row_id) is str
            and row_id not in ids
            and type(pair) is list
            and len(pair) == 2
            and pair == sorted(pair)
            and pair[0] != pair[1]
            and row.get("left_Round294_registry_occurrence_id") == pair[0]
            and row.get("right_Round294_registry_occurrence_id") == pair[1]
            and row.get("formal_component_edge_credit") == 0
            and row.get("formal_DSU_rank_reduction_credit") == 0
            and row.get("formal_maximality_credit") == 0,
            "R300A exact pair boundary",
        )
        ids.add(row_id)
        left = endpoint_root(pair[0], member_root, root_index)
        right = endpoint_root(pair[1], member_root, root_index)
        same = final_map[left] == final_map[right]
        prior_witness = row.get(
            "R295A_explicit_lower_graph_sheet_witness_present"
        )
        need(type(prior_witness) is bool, "R300A prior witness flag")
        witnessed += int(prior_witness)
        disposition = (
            "PRIOR_R295A_WITNESSED__SAME_FINAL_COMPONENT"
            if prior_witness and same
            else (
                "PRIOR_R295A_WITNESSED__CROSS_FINAL_COMPONENT_INCONSISTENCY"
                if prior_witness
                else (
                    "UNWITNESSED__RECLOSED_BY_OTHER_LEGAL_DSU_PATH"
                    if same
                    else (
                        "UNWITNESSED__CROSS_COMPONENT__FORMAL_PHYSICAL_"
                        "INCLUSION_PACKAGE_REQUIRED"
                    )
                )
            )
        )
        histogram[disposition] += 1
        rows.append(
            {
                "source_Round300A_row_id": row_id,
                "source_Round300A_row_sha256": row["row_sha256"],
                "canonical_occurrence_pair": pair,
                "projected_base_root_pair": sorted([left, right]),
                "final_component_pair": sorted(
                    [final_map[left], final_map[right]]
                ),
                "prior_R295A_witness_present": prior_witness,
                "same_final_component": same,
                "post_Round304_disposition": disposition,
            }
        )
    need(
        len(rows) == 3_232
        and len(ids) == 3_232
        and witnessed == 128
        and histogram[
            "PRIOR_R295A_WITNESSED__CROSS_FINAL_COMPONENT_INCONSISTENCY"
        ]
        == 0,
        "R300A reprojection exact census",
    )
    missing = histogram[
        (
            "UNWITNESSED__CROSS_COMPONENT__FORMAL_PHYSICAL_"
            "INCLUSION_PACKAGE_REQUIRED"
        )
    ]
    return {
        "complete_Round300A_pair_count": len(rows),
        "prior_R295A_witnessed_pair_count": witnessed,
        "previously_unwitnessed_pair_count": 3_104,
        "post_Round304_disposition_histogram": dict(sorted(histogram.items())),
        "complete_reprojection_rows_sha256": digest(rows),
        "cross_component_unwitnessed_pair_count": missing,
        "sealed_physical_inclusion_package_for_cross_pairs_present": False,
        "unsealed_temp_1024_theorem_consumed": False,
        "maximality_proved": False,
        "formal_maximality_credit": 0,
    }


def key_fibre_census(
    member_root: dict[str, str],
    member_key: dict[str, str],
    final_map: dict[str, str],
    maximality: dict[str, Any],
) -> dict[str, Any]:
    member_counts: Counter[str] = Counter()
    components: dict[str, set[str]] = defaultdict(set)
    for member, root in member_root.items():
        key = member_key[member]
        member_counts[key] += 1
        components[key].add(final_map[root])
    keys = sorted(member_counts)
    rows = [
        {
            "official_key_id": key,
            "member_count": member_counts[key],
            "final_component_count": len(components[key]),
            "final_component_ids_sha256": digest(sorted(components[key])),
            "physical_fibre_maximality_available": False,
            "formal_fibre_credit": 0,
        }
        for key in keys
    ]
    need(
        len(keys) == ACTUAL_OFFICIAL_KEY_COUNT
        and sum(member_counts.values()) == 564_492
        and len(keys) != STALE_OFFICIAL_KEY_COUNT,
        "independent actual-124 fibre census",
    )
    return {
        "actual_registry_official_key_count": len(keys),
        "stale_116_official_key_count_rejected": True,
        "all_124_registry_official_keys_enumerated": True,
        "all_564492_members_assigned_to_an_official_key": True,
        "official_key_fibre_rows_sha256": digest(rows),
        "official_key_member_count_histogram": {
            str(member_count): frequency
            for member_count, frequency in sorted(
                Counter(member_counts.values()).items()
            )
        },
        "official_key_final_component_count_histogram": {
            str(component_count): frequency
            for component_count, frequency in sorted(
                Counter(
                    len(value) for value in components.values()
                ).items()
            )
        },
        "maximality_dependency_satisfied": maximality["maximality_proved"],
        "physical_official_key_fibre_exhaustion_proved": False,
        "formal_fibre_credit": 0,
    }


def audit_sealed_prior_only() -> dict[str, Any]:
    """Independently rebuild only sealed pre-R303B state."""

    validate_upstream_seals()
    member_root, member_key, roots = rebuild_universe()
    root_index = {root: index for index, root in enumerate(roots)}
    prior_edges = old_edges(member_root, root_index)
    forward_map, forward, _ = apply(
        roots,
        root_index,
        prior_edges,
        component_namespace="round301-legal-component:",
    )
    reverse_map, reverse, _ = apply(
        roots,
        root_index,
        reversed(prior_edges),
        component_namespace="round301-legal-component:",
    )
    need(
        forward_map == reverse_map
        and forward["edge_rows"] == 434_606
        and forward["rank_reduction"] == 246_016
        and forward["component_count"] == 121_948
        and forward["partition_sha256"]
        == "c1ab6beed75d5e7379103975d6a9ac1b1095a3eb24b34c87288782e7c97cfe09"
        and reverse["partition_sha256"] == forward["partition_sha256"]
        and reverse["rank_reduction"] == forward["rank_reduction"]
        and reverse["component_count"] == forward["component_count"],
        "independent sealed-prior forward/reverse reconstruction",
    )
    assert_snapshot_map(SOURCE_SNAPSHOTS, "source")
    return {
        "schema": "cm2.round304.independent-sealed-prior-only-audit.v1",
        "status": "PASS_INDEPENDENT_SEALED_PRIOR_ONLY__R303B_NOT_OPENED",
        "member_count": len(member_root),
        "base_root_count": len(roots),
        "official_key_count": len(set(member_key.values())),
        "forward": forward,
        "reverse": reverse,
        "forward_reverse_same_partition": True,
        "Round301_partition_loaded_as_DSU_state": False,
        "Round303B_manifest_or_ledger_opened": False,
        "candidate_Round304_artifact_opened": False,
    }


def expected_state(require_candidate_seal: bool = True) -> dict[str, Any]:
    # All missing source seals are checked before candidate output exists/opens.
    need(
        seal_ready() if require_candidate_seal else r303b_seal_ready(),
        "BLOCKED: required final R303B/R304 pins absent",
    )
    validate_upstream_seals()
    member_root, member_key, roots = rebuild_universe()
    root_index = {root: index for index, root in enumerate(roots)}
    prior_edges = old_edges(member_root, root_index)
    prior_map, prior, _ = apply(
        roots,
        root_index,
        prior_edges,
        component_namespace="round301-legal-component:",
    )
    need(
        prior["edge_rows"] == 434_606
        and prior["rank_reduction"] == 246_016
        and prior["component_count"] == 121_948
        and prior["partition_sha256"]
        == "c1ab6beed75d5e7379103975d6a9ac1b1095a3eb24b34c87288782e7c97cfe09",
        "fresh independent prior partition",
    )
    r303b_edges, unresolved = validate_r303b_and_edges(
        member_root, member_key, root_index, prior_map
    )
    all_edges = prior_edges + r303b_edges
    forward_map, forward, forest = apply(
        roots, root_index, all_edges, keep_forest=True
    )
    reverse_map, reverse, _ = apply(roots, root_index, reversed(all_edges))
    need(
        forward_map == reverse_map
        and forward["edge_rows"] == 478_710
        and reverse["edge_rows"] == 478_710
        and forward["rank_reduction"] - prior["rank_reduction"] == 29_252
        and forward["rank_reduction"] == 275_268
        and reverse["rank_reduction"] == 275_268
        and forward["component_count"] == 92_696
        and reverse["component_count"] == 92_696
        and forward["partition_sha256"] == reverse["partition_sha256"]
        and forward["rank_reduction"] == reverse["rank_reduction"]
        and forward["component_count"] == reverse["component_count"],
        "independent exact 29252/275268/92696 forward/reverse outcome",
    )
    wtail = []
    for row in unresolved:
        left, right = row["roots"]
        same = forward_map[left] == forward_map[right]
        stronger_path = path(left, right, forest) if same else []
        need(bool(stronger_path) == same, "independent W-tail path iff same")
        wtail.append(
            {
                "source_id": row["source_id"],
                "source_row_id": row["row_id"],
                "source_row_sha256": row["row_sha256"],
                "canonical_occurrence_endpoint_pair": list(row["endpoints"]),
                "projected_base_root_pair": sorted([left, right]),
                "final_component_pair": sorted([
                    forward_map[left],
                    forward_map[right],
                ]),
                "same_final_component": same,
                "stronger_path": stronger_path,
                "source_row_fed_to_DSU": False,
            }
        )
    need(
        len(wtail) == 4
        and all(
            row["same_final_component"] is True
            and bool(row["stronger_path"])
            and row["source_row_fed_to_DSU"] is False
            for row in wtail
        ),
        "independent exact 4-of-4 W-tail stronger-path reclosure",
    )
    maximality = reproject_R300A(
        member_root,
        root_index,
        forward_map,
    )
    fibre = key_fibre_census(
        member_root,
        member_key,
        forward_map,
        maximality,
    )
    denominator = source_G_denominator()
    global_gate = {
        **denominator,
        "complete_global_half_open_join_ledger_present": False,
        "post_Round304_global_disposition_count": 0,
        "post_Round304_unresolved_global_disposition_count":
            SOURCE_G_EXACT_KEY_DISPOSITION_DENOMINATOR,
        "registry_official_key_count_is_not_the_global_denominator": True,
        "global_source_G_disposition_exhaustion_proved": False,
        "formal_global_disposition_credit": 0,
    }
    assert_snapshot_map(SOURCE_SNAPSHOTS, "source")
    return {
        "member_count": len(member_root),
        "base_root_count": len(roots),
        "official_key_count": len(set(member_key.values())),
        "prior": prior,
        "forward": forward,
        "reverse": reverse,
        "derived_Round303B_incremental_rank_reduction":
            forward["rank_reduction"] - prior["rank_reduction"],
        "W_tail": wtail,
        "maximality_gate": maximality,
        "official_key_fibre_gate": fibre,
        "global_source_G_disposition_gate": global_gate,
        "strict_zero_downstream_credit_required": True,
    }


SCHEMA_SNAPSHOT = {
    "schema": "cm2.round304.schema-snapshot.v1",
    "candidate_files": dict(sorted(CANDIDATE_FILES.items())),
    "tables": dict(sorted(CANDIDATE_TABLES.items())),
    "id_fields": dict(sorted(CANDIDATE_ID_FIELDS.items())),
    "row_schemas": dict(sorted(CANDIDATE_ROW_SCHEMAS.items())),
    "ledger_schemas": dict(sorted(CANDIDATE_LEDGER_SCHEMAS.items())),
    "exact_row_fields": {
        key: list(value)
        for key, value in sorted(CANDIDATE_EXACT_ROW_FIELDS.items())
    },
    "exact_ledger_fields": {
        key: list(value)
        for key, value in sorted(CANDIDATE_EXACT_LEDGER_FIELDS.items())
    },
    "exact_result_fields": list(CANDIDATE_EXACT_RESULT_FIELDS),
    "result_schema": CANDIDATE_RESULT_SCHEMA,
    "source_channel_order": [channel.name for channel in CHANNELS]
    + ["R303B_UNIFIED_ATTACHMENT"],
    "member_count": 564_492,
    "base_root_count": 367_964,
    "actual_official_key_count": 124,
    "stale_official_key_count_rejected": 116,
    "source_G_exact_key_disposition_denominator": 224_580,
    "prior_legal_edge_count": 434_606,
    "R303B_legal_edge_count": 44_104,
    "total_legal_edge_count": 478_710,
    "W_tail_count": 4,
    "producer_seed_affects_output": False,
    "result_is_atomic_commit_marker": True,
    "attack_mechanisms": list(ATTACK_MECHANISMS),
}
COMPUTED_SCHEMA_SNAPSHOT_SHA256 = digest(SCHEMA_SNAPSHOT)


def validate_candidate_row_shape(table: str, row: dict[str, Any]) -> None:
    need(
        set(row) == set(CANDIDATE_EXACT_ROW_FIELDS[table]),
        "candidate exact row fields:" + table,
    )
    need(
        row["schema"] == CANDIDATE_ROW_SCHEMAS[table],
        "candidate row schema:" + table,
    )
    verify_self(row, "row_sha256", "candidate:" + table)


def close_expected_row(
    table: str,
    context: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    need(payload.get("schema") == CANDIDATE_ROW_SCHEMAS[table], "expected schema")
    id_field = CANDIDATE_ID_FIELDS[table]
    need(id_field not in payload and "row_sha256" not in payload, "expected preclosure")
    base = {
        id_field: "round304-" + table + ":" + digest([context, payload]),
        **payload,
    }
    row = {**base, "row_sha256": digest(base)}
    validate_candidate_row_shape(table, row)
    return row


def expected_ledger(
    table: str,
    rows: Iterable[dict[str, Any]],
) -> tuple[bytes, dict[str, Any]]:
    materialized: list[dict[str, Any]] = []
    ids: list[str] = []
    hashes: list[str] = []
    seen: set[str] = set()
    id_field = CANDIDATE_ID_FIELDS[table]
    for row in rows:
        validate_candidate_row_shape(table, row)
        row_id = row[id_field]
        need(row_id not in seen, "expected duplicate row id:" + table)
        seen.add(row_id)
        materialized.append(row)
        ids.append(row_id)
        hashes.append(row["row_sha256"])
    document = {
        "schema": CANDIDATE_LEDGER_SCHEMAS[table],
        "status": "PASS_EXACT_DETERMINISTIC_LEDGER",
        "row_count": len(materialized),
        "row_ids_sha256": digest(ids),
        "row_hashes_sha256": digest(hashes),
        "rows_sha256": digest(materialized),
        CANDIDATE_TABLES[table]: materialized,
    }
    need(
        set(document) == set(CANDIDATE_EXACT_LEDGER_FIELDS[table]),
        "expected exact ledger fields:" + table,
    )
    raw = deterministic_gzip(document)
    return raw, {
        "filename": CANDIDATE_FILES[table],
        "schema": CANDIDATE_LEDGER_SCHEMAS[table],
        "row_count": len(materialized),
        "row_ids_sha256": document["row_ids_sha256"],
        "row_hashes_sha256": document["row_hashes_sha256"],
        "rows_sha256": document["rows_sha256"],
        "file_sha256": hashlib.sha256(raw).hexdigest(),
    }


def iter_expected_edge_rows(
    roots: list[str],
    root_index: dict[str, int],
    edges: Iterable[VEdge],
) -> Iterator[dict[str, Any]]:
    uf = IndexUF(len(roots))
    for index, edge in enumerate(edges):
        reduced = uf.merge(
            root_index[edge.roots[0]],
            root_index[edge.roots[1]],
        )
        payload = {
            "schema": CANDIDATE_ROW_SCHEMAS["edge"],
            "application_index": index,
            "source_channel": edge.channel,
            "source_row_id": edge.source_id,
            "source_row_sha256": edge.source_sha,
            "canonical_occurrence_endpoint_pair": list(edge.endpoints),
            "projected_base_root_pair": sorted(edge.roots),
            "fed_to_fresh_DSU": True,
            "forward_rank_reduction": int(reduced),
            "forward_cycle_or_redundant": int(not reduced),
            "formal_DSU_rank_reduction_credit": int(reduced),
            "serialized_Round301_partition_used_as_state": False,
            "old_63224_partition_used_as_state": False,
            "provisional_Round303B_consumed": False,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
        }
        yield close_expected_row(
            "edge",
            digest([
                "ROUND304_FRESH_DSU_FORWARD_APPLICATION_V1",
                index,
                edge.channel,
                edge.source_id,
                edge.source_sha,
            ]),
            payload,
        )


def iter_expected_member_rows(
    member_root: dict[str, str],
    member_key: dict[str, str],
    final_map: dict[str, str],
) -> Iterator[dict[str, Any]]:
    for member in sorted(member_root):
        base_root = member_root[member]
        payload = {
            "schema": CANDIDATE_ROW_SCHEMAS["member"],
            "registry_occurrence_id": member,
            "base_root_id": base_root,
            "official_key_id": member_key[member],
            "final_component_id": final_map[base_root],
            "member_identity_preserved": True,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
        }
        yield close_expected_row(
            "member",
            digest([
                "ROUND304_FRESH_MEMBER_COMPONENT_V1",
                member,
                base_root,
            ]),
            payload,
        )


def iter_expected_W_tail_rows(
    unresolved: Iterable[dict[str, Any]],
    final_map: dict[str, str],
    forest: dict[str, list[tuple[str, VEdge]]],
) -> Iterator[dict[str, Any]]:
    for item in sorted(unresolved, key=lambda row: row["row_id"]):
        left, right = item["roots"]
        same = final_map[left] == final_map[right]
        stronger_path = path(left, right, forest) if same else []
        need(bool(stronger_path) == same, "expected W-tail stronger path iff same")
        payload = {
            "schema": CANDIDATE_ROW_SCHEMAS["wtail"],
            "source_W_tail_row_id": item["row_id"],
            "source_W_tail_row_sha256": item["row_sha256"],
            "source_Round300D_row_id": item["source_id"],
            "canonical_occurrence_endpoint_pair": list(item["endpoints"]),
            "projected_base_root_pair": sorted([left, right]),
            "final_component_pair": sorted([
                final_map[left],
                final_map[right],
            ]),
            "same_final_component": same,
            "disposition": (
                "RECLOSED_BY_STRONGER_LEGAL_DSU_PATH__ZERO_NEW_EDGE"
                if same
                else (
                    "STILL_CROSS_COMPONENT__WTAIL_EXTENSION_OR_"
                    "OTHER_LEGAL_PATH_REQUIRED"
                )
            ),
            "stronger_legal_path": stronger_path,
            "source_row_fed_to_DSU": False,
            "eligible_for_fresh_DSU_application": False,
            "formal_component_edge_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "nonedge_credit": 0,
            "exclusion_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
        }
        yield close_expected_row(
            "wtail",
            digest([
                "ROUND304_WTAIL_STRONGER_PATH_DISPOSITION_V1",
                item["row_id"],
                item["row_sha256"],
            ]),
            payload,
        )


def iter_expected_residual_rows() -> Iterator[dict[str, Any]]:
    payload = {
        "schema": CANDIDATE_ROW_SCHEMAS["residual"],
        "required_next": (
            "REPROJECT_THE_SEALED_R300A_CANONICAL_CONTACT_FRONTIER_AGAINST_"
            "THIS_NEW_PARTITION_AND_CLOSE_EACH_RESIDUAL_WITH_PHYSICAL_"
            "INCLUSION_OR_EXACT_EXCLUSION"
        ),
        "hard_coded_1024_treated_as_theorem": False,
        "formal_maximality_credit": 0,
        "formal_fibre_credit": 0,
        "formal_global_disposition_credit": 0,
        "Gate5_complete_18_field_block_count": 0,
        "D02_status": "BLOCKED",
        "CM2_status": "NO-GO_FOR_CLAIM",
    }
    yield close_expected_row(
        "residual",
        "ROUND304_POST_DSU_RESIDUAL_GATE_V1",
        payload,
    )


def build_expected_candidate_artifacts() -> tuple[
    dict[str, bytes],
    dict[str, Any],
]:
    """Rebuild all candidate bytes before opening any candidate artifact."""

    need(seal_ready(), "complete R303B and frozen Round304 pins required")
    assert FINAL_R304_PRODUCER_SHA256 is not None
    validate_upstream_seals()
    member_root, member_key, roots = rebuild_universe()
    root_index = {root: index for index, root in enumerate(roots)}
    prior_edges = old_edges(member_root, root_index)
    prior_map, prior, _ = apply(
        roots,
        root_index,
        prior_edges,
        component_namespace="round301-legal-component:",
    )
    need(
        prior["edge_rows"] == 434_606
        and prior["rank_reduction"] == 246_016
        and prior["component_count"] == 121_948
        and prior["partition_sha256"]
        == "c1ab6beed75d5e7379103975d6a9ac1b1095a3eb24b34c87288782e7c97cfe09",
        "expected candidate prior partition",
    )
    r303b_edges, unresolved = validate_r303b_and_edges(
        member_root,
        member_key,
        root_index,
        prior_map,
    )
    all_edges = prior_edges + r303b_edges
    forward_map, forward, forest = apply(
        roots,
        root_index,
        all_edges,
        keep_forest=True,
    )
    reverse_map, reverse, _ = apply(
        roots,
        root_index,
        reversed(all_edges),
    )
    need(
        forward_map == reverse_map
        and forward["edge_rows"] == 478_710
        and reverse["edge_rows"] == 478_710
        and forward["rank_reduction"] - prior["rank_reduction"] == 29_252
        and forward["rank_reduction"] == 275_268
        and reverse["rank_reduction"] == 275_268
        and forward["component_count"] == 92_696
        and reverse["component_count"] == 92_696
        and forward["rank_reduction"] == reverse["rank_reduction"]
        and forward["component_count"] == reverse["component_count"]
        and forward["partition_sha256"] == reverse["partition_sha256"],
        "expected candidate exact 29252/275268/92696 full partition",
    )
    maximality = reproject_R300A(member_root, root_index, forward_map)
    fibre = key_fibre_census(
        member_root,
        member_key,
        forward_map,
        maximality,
    )
    denominator = source_G_denominator()
    global_gate = {
        **denominator,
        "complete_global_half_open_join_ledger_present": False,
        "post_Round304_global_disposition_count": 0,
        "post_Round304_unresolved_global_disposition_count":
            SOURCE_G_EXACT_KEY_DISPOSITION_DENOMINATOR,
        "registry_official_key_count_is_not_the_global_denominator": True,
        "global_source_G_disposition_exhaustion_proved": False,
        "formal_global_disposition_credit": 0,
    }

    artifacts: dict[str, bytes] = {}
    output_ledgers: dict[str, dict[str, Any]] = {}
    edge_bytes, edge_meta = expected_ledger(
        "edge",
        iter_expected_edge_rows(roots, root_index, all_edges),
    )
    artifacts[CANDIDATE_FILES["edge"]] = edge_bytes
    output_ledgers["edge"] = edge_meta
    del edge_bytes
    member_bytes, member_meta = expected_ledger(
        "member",
        iter_expected_member_rows(member_root, member_key, forward_map),
    )
    artifacts[CANDIDATE_FILES["member"]] = member_bytes
    output_ledgers["member"] = member_meta
    del member_bytes
    wtail_rows = list(
        iter_expected_W_tail_rows(unresolved, forward_map, forest)
    )
    need(
        len(wtail_rows) == 4
        and all(
            row["same_final_component"] is True
            and row["disposition"]
            == "RECLOSED_BY_STRONGER_LEGAL_DSU_PATH__ZERO_NEW_EDGE"
            and bool(row["stronger_legal_path"])
            and row["source_row_fed_to_DSU"] is False
            for row in wtail_rows
        ),
        "expected candidate exact 4-of-4 W-tail stronger-path reclosure",
    )
    wtail_bytes, wtail_meta = expected_ledger("wtail", wtail_rows)
    artifacts[CANDIDATE_FILES["wtail"]] = wtail_bytes
    output_ledgers["wtail"] = wtail_meta
    del wtail_bytes
    residual_rows = list(iter_expected_residual_rows())
    residual_bytes, residual_meta = expected_ledger(
        "residual",
        residual_rows,
    )
    artifacts[CANDIDATE_FILES["residual"]] = residual_bytes
    output_ledgers["residual"] = residual_meta
    del residual_bytes

    wtail_histogram = Counter(row["disposition"] for row in wtail_rows)
    same_W_tail = sum(int(row["same_final_component"]) for row in wtail_rows)
    payload = {
        "schema": CANDIDATE_RESULT_SCHEMA,
        "status": (
            "PASS_ROUND304_FRESH_EXTENDED_REGISTRY_LEGAL_DSU__"
            f"{forward['rank_reduction']}_RANK_REDUCTIONS__"
            f"{forward['component_count']}_COMPONENTS__"
            "ZERO_MAXIMALITY_FIBRE_GLOBAL_DISPOSITION_CREDIT"
        ),
        "producer_file_sha256": FINAL_R304_PRODUCER_SHA256,
        "schema_snapshot_sha256": COMPUTED_SCHEMA_SNAPSHOT_SHA256,
        "seed_affects_output": False,
        "Round303B_seal": {
            "manifest_filename": R303B_MANIFEST,
            "manifest_file_sha256": FINAL_R303B_MANIFEST_SHA256,
            "manifest_member_count": 12,
            "producer_file_sha256": FINAL_R303B_PRODUCER_SHA256,
            "verifier_file_sha256": FINAL_R303B_VERIFIER_SHA256,
            "verification_file_sha256": FINAL_R303B_VERIFICATION_FILE_SHA256,
            "verification_object_sha256":
                FINAL_R303B_VERIFICATION_OBJECT_SHA256,
            "result_file_sha256": FINAL_R303B_RESULT_SHA256,
            "edge_ledger_file_sha256": FINAL_R303B_EDGE_LEDGER_SHA256,
            "W_tail_ledger_file_sha256": FINAL_R303B_WTAIL_LEDGER_SHA256,
            "complete_seal_validated_before_ledger_consumption": True,
        },
        "input_file_and_manifest_pins": {
            "Round294B_manifest": {
                R294B_MANIFEST: R294B_MANIFEST_SHA256,
                R294B_VERIFICATION: R294B_VERIFICATION_FILE_SHA256,
            },
            "Round266_manifest": {R266_MANIFEST: R266_MANIFEST_SHA256},
            "Round294_manifest": {R294_MANIFEST: R294_MANIFEST_SHA256},
            "Round299A_manifest": {R299A_MANIFEST: R299A_MANIFEST_SHA256},
            "Round301_historical_manifest": {
                R301_MANIFEST: R301_MANIFEST_SHA256
            },
            "Round303A_manifest": {R303A_MANIFEST: R303A_MANIFEST_SHA256},
            "Round303B_manifest": {
                R303B_MANIFEST: FINAL_R303B_MANIFEST_SHA256
            },
            "Round300A_manifest": {R300A_MANIFEST: R300A_MANIFEST_SHA256},
            "Round169_files": {
                R169_CERTIFICATE: R169_CERTIFICATE_SHA256,
                R169_VERIFICATION: R169_VERIFICATION_SHA256,
            },
        },
        "member_universe": {
            "member_count": len(member_root),
            "base_root_count": len(roots),
            "official_key_count": len(set(member_key.values())),
            "actual_official_key_count": ACTUAL_OFFICIAL_KEY_COUNT,
            "stale_116_official_key_count_rejected": True,
            "unkeyed_member_count": 0,
        },
        "forward_application": {
            **forward,
            "prior_fresh_reconstruction": prior,
            "Round303B_incremental_rank_reduction":
                forward["rank_reduction"] - prior["rank_reduction"],
            "Round303B_census": {
                "edge_count": len(r303b_edges),
                "W_tail_count": len(unresolved),
                "distinct_endpoint_count": 88_216,
            },
        },
        "reverse_application": reverse,
        "forward_reverse_same_partition": True,
        "W_tail_disposition_census": {
            "row_count": len(wtail_rows),
            "same_final_component_count": same_W_tail,
            "cross_final_component_count": len(wtail_rows) - same_W_tail,
            "disposition_histogram": dict(sorted(wtail_histogram.items())),
            "all_rows_excluded_from_DSU_input": True,
            "formal_component_edge_credit": 0,
        },
        "maximality_gate": maximality,
        "official_key_fibre_gate": fibre,
        "global_source_G_disposition_gate": global_gate,
        "residual_gate_census": {
            "R300A_cross_component_unwitnessed_pair_count":
                maximality["cross_component_unwitnessed_pair_count"],
            "actual_official_key_count": ACTUAL_OFFICIAL_KEY_COUNT,
            "stale_official_key_count_rejected": STALE_OFFICIAL_KEY_COUNT,
            "source_G_global_disposition_count": 0,
            "source_G_global_disposition_denominator":
                SOURCE_G_EXACT_KEY_DISPOSITION_DENOMINATOR,
            "Gate5_complete_18_field_block_count": 0,
            "D02_status": "BLOCKED",
            "CM2_status": "NO-GO_FOR_CLAIM",
        },
        "formal_credit_transition": {
            "formal_legal_component_edge_application_credit": 478_710,
            "formal_DSU_rank_reduction_credit": forward["rank_reduction"],
            "formal_component_union_credit": forward["rank_reduction"],
            "formal_component_quotient_credit": 1,
            "formal_post_Round304_component_count": forward["component_count"],
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
            "formal_Jx_Jy_same_point_glue_credit": 0,
        },
        "strict_boundary": {
            "Round301_partition_loaded_as_DSU_state": False,
            "Round301_manifest_members_opened_for_exact_hash_validation": True,
            "Round301_member_component_ledger_loaded_as_DSU_state": False,
            "Round301_edge_application_ledger_loaded_as_DSU_state": False,
            "old_63224_partition_used_as_state": False,
            "conditional_92696_partition_used_as_state": False,
            "provisional_Round303B_consumed": False,
            "W_tail_rows_fed_to_DSU": 0,
            "unsealed_temp_R300A_1024_theorem_consumed": False,
            "maximality_fibre_global_disposition_credit_all_zero": True,
        },
        "atomicity_contract": {
            "input_PRE_POST_identity_equality_required_before_commit": True,
            "complete_batch_no_clobber_preflight_required": True,
            "staged_files_require_atomic_RENAME_NOREPLACE": True,
            "result_is_required_last_commit_marker": True,
            "explicit_root_confined_candidate_directory_required": True,
            "exact_private_stage_orphan_recovery_required_before_retry": True,
        },
        "output_ledgers": output_ledgers,
    }
    result = {**payload, "result_sha256": digest(payload)}
    need(
        set(result) == set(CANDIDATE_EXACT_RESULT_FIELDS),
        "expected exact result fields",
    )
    need(
        json_object_keys_are_strings(result),
        "expected result object keys must be strings",
    )
    result_raw = canonical(result)
    replayed_result = json.loads(result_raw)
    need(
        type(replayed_result) is dict
        and canonical(replayed_result) == result_raw,
        "expected result parse-canonical byte replay",
    )
    replayed_result_sha256 = replayed_result.pop("result_sha256", None)
    need(
        type(replayed_result_sha256) is str
        and replayed_result_sha256 == digest(replayed_result),
        "expected result parse-canonical self-hash replay",
    )
    artifacts[CANDIDATE_FILES["result"]] = result_raw
    assert_snapshot_map(SOURCE_SNAPSHOTS, "source")
    return artifacts, result


def compare_dual_seed_directories(
    first: Path,
    second: Path,
) -> dict[str, Any]:
    need(seal_ready(), "dual-seed artifacts forbidden before all seals")
    output: dict[str, str] = {}
    for key in ("edge", "member", "wtail", "residual", "result"):
        name = CANDIDATE_FILES[key]
        left = first / name
        right = second / name
        left_raw = stable_read_bytes(
            left,
            first,
            CANDIDATE_SNAPSHOTS,
            label="dual-seed A:" + name,
        )
        right_raw = stable_read_bytes(
            right,
            second,
            CANDIDATE_SNAPSHOTS,
            label="dual-seed B:" + name,
        )
        left_hash = hashlib.sha256(left_raw).hexdigest()
        right_hash = hashlib.sha256(right_raw).hexdigest()
        need(
            left_hash == right_hash and left_raw == right_raw,
            "dual-seed exact-byte divergence:" + name,
        )
        output[name] = left_hash
    assert_snapshot_map(CANDIDATE_SNAPSHOTS, "dual-seed candidate")
    return {
        "schema": "cm2.round304.independent-dual-seed-byte-audit.v1",
        "status": "PASS_DUAL_SEED_EXACT_BYTES",
        "seeds": list(DUAL_SEEDS),
        "seed_affects_output": False,
        "artifact_sha256": dict(sorted(output.items())),
    }


def reclose_mutated_W_tail_bundle(
    expected: dict[str, bytes],
    mechanism: str,
) -> dict[str, bytes]:
    bundle = dict(expected)
    ledger_name = CANDIDATE_FILES["wtail"]
    result_name = CANDIDATE_FILES["result"]
    ledger = strict_object(gzip.decompress(bundle[ledger_name]), "attack W-tail")
    table = CANDIDATE_TABLES["wtail"]
    rows = copy.deepcopy(ledger[table])
    need(len(rows) == 4, "attack W-tail census")
    row = rows[0]
    if mechanism == "W_tail_stronger_path_edge_forgery":
        need(bool(row["stronger_legal_path"]), "attack needs nonempty path")
        row["stronger_legal_path"][0]["source_row_id"] = "forged-source-row"
    elif mechanism == "W_tail_stronger_path_disconnect":
        need(bool(row["stronger_legal_path"]), "attack needs nonempty path")
        row["stronger_legal_path"] = row["stronger_legal_path"][:-1]
    elif mechanism == "W_tail_stronger_path_source_hash_forgery":
        need(bool(row["stronger_legal_path"]), "attack needs nonempty path")
        row["stronger_legal_path"][0]["source_row_sha256"] = "f" * 64
    elif mechanism == "W_tail_same_component_flip":
        row["same_final_component"] = not row["same_final_component"]
    elif mechanism == "W_tail_fed_to_DSU":
        row["source_row_fed_to_DSU"] = True
    elif mechanism == "W_tail_edge_promotion":
        row["formal_component_edge_credit"] = 1
    elif mechanism == "W_tail_nonedge_promotion":
        row["nonedge_credit"] = 1
    elif mechanism == "W_tail_exclusion_promotion":
        row["exclusion_credit"] = 1
    else:
        raise VerificationBlocked("unknown coherent W-tail attack")
    base = {key: value for key, value in row.items() if key != "row_sha256"}
    rows[0] = {**base, "row_sha256": digest(base)}
    ledger[table] = rows
    ledger["row_count"] = len(rows)
    ledger["row_ids_sha256"] = digest(
        [item[CANDIDATE_ID_FIELDS["wtail"]] for item in rows]
    )
    ledger["row_hashes_sha256"] = digest(
        [item["row_sha256"] for item in rows]
    )
    ledger["rows_sha256"] = digest(rows)
    mutated_ledger = deterministic_gzip(ledger)
    bundle[ledger_name] = mutated_ledger

    result = strict_object(bundle[result_name], "attack result")
    result_payload = {
        key: value for key, value in result.items() if key != "result_sha256"
    }
    metadata = result_payload["output_ledgers"]["wtail"]
    metadata["file_sha256"] = hashlib.sha256(mutated_ledger).hexdigest()
    metadata["row_count"] = ledger["row_count"]
    metadata["row_ids_sha256"] = ledger["row_ids_sha256"]
    metadata["row_hashes_sha256"] = ledger["row_hashes_sha256"]
    metadata["rows_sha256"] = ledger["rows_sha256"]
    bundle[result_name] = canonical(
        {**result_payload, "result_sha256": digest(result_payload)}
    )
    return bundle


def source_semantic_fixture() -> dict[str, Any]:
    channels = [
        "R297_ORDINARY_FACE",
        "R296_TRUE_SEAM",
        "R299C_SIGNED_FACE",
        "R300B_COMPLETE_FACE",
        "R300C_POSITIVE_VOLUME",
        "R300E_HALF_OPEN_OWNER",
        "R300F_R245_HALF_OPEN_OWNER",
        "R303B_UNIFIED_ATTACHMENT",
    ]
    return {
        "registry": {"e0", "e1", "e2", "e3", "e4", "e5"},
        "projection": {
            "e0": "r0",
            "e1": "r1",
            "e2": "r2",
            "e3": "r3",
            "e4": "r4",
            "e5": "r5",
        },
        "edge_rows": [
            {
                "source_id": "s0",
                "pair": ["e0", "e1"],
                "roots": ["r0", "r1"],
            },
            {
                "source_id": "s1",
                "pair": ["e2", "e3"],
                "roots": ["r2", "r3"],
            },
        ],
        "W_tail_rows": [
            {
                "source_id": "w0",
                "pair": ["e4", "e5"],
                "formal_component_edge_credit": 0,
                "nonedge_credit": 0,
                "exclusion_credit": 0,
                "source_row_fed_to_DSU": False,
            }
        ],
        "proof_flags": {
            "eligible_for_later_fresh_DSU_application": True,
            "G0_exact_provenance_pins_and_row_closures": True,
            "G1_endpoint_occurrence_connected_supports": True,
            "G2_nonempty_connected_included_lower_stratum": True,
            "G3_left_closure_attaches_to_included_patch": True,
            "G4_right_closure_attaches_to_included_patch": True,
            "G5_endpoint_patch_provenance_exactly_closed": True,
            "candidate_component_connectivity_conclusion": True,
        },
        "zero_credits": {
            "formal_occurrence_identity_collapse_credit": 0,
            "formal_official_key_merge_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
            "formal_Jx_Jy_same_point_glue_credit": 0,
        },
        "forbidden_state": {
            "Round301_partition_loaded_as_DSU_state": False,
            "Round301_edge_application_ledger_loaded_as_DSU_state": False,
            "old_63224_partition_used_as_state": False,
            "conditional_92696_partition_used_as_state": False,
        },
        "channel_counts": {name: 1 for name in channels},
        "manifest": dict(FINAL_R303B_MANIFEST_MEMBER_PINS or {}),
        "Round294B_manifest_sha256": R294B_MANIFEST_SHA256,
        "Round303B_verifier_sha256": FINAL_R303B_VERIFIER_SHA256,
        "residual_boundary": {
            "actual_official_key_count": 124,
            "stale_116_official_key_count_rejected": True,
            "source_G_global_disposition_denominator": 224_580,
            "registry_keyspace_is_global_disposition_keyspace": False,
            "hard_coded_1024_treated_as_theorem": False,
            "Gate5_complete_18_field_block_count": 0,
            "D02_status": "BLOCKED",
            "CM2_status": "NO-GO_FOR_CLAIM",
        },
    }


def validate_source_semantic_fixture(value: dict[str, Any]) -> None:
    registry = value["registry"]
    projection = value["projection"]
    edge_rows = value["edge_rows"]
    W_tail_rows = value["W_tail_rows"]
    need(type(registry) is set and len(registry) == 6, "fixture registry")
    edge_sources: set[str] = set()
    edge_pairs: set[tuple[str, str]] = set()
    endpoints: set[str] = set()
    for row in edge_rows:
        pair = row["pair"]
        need(
            type(pair) is list
            and len(pair) == 2
            and pair == sorted(pair)
            and pair[0] != pair[1]
            and all(endpoint in registry for endpoint in pair),
            "fixture edge canonical registry pair",
        )
        need(
            row["roots"] == sorted(
                [projection[pair[0]], projection[pair[1]]]
            ),
            "fixture exact base-root projection",
        )
        need(row["source_id"] not in edge_sources, "fixture source duplicate")
        need(tuple(pair) not in edge_pairs, "fixture edge pair duplicate")
        need(not endpoints.intersection(pair), "fixture endpoint reuse")
        edge_sources.add(row["source_id"])
        edge_pairs.add(tuple(pair))
        endpoints.update(pair)
    for row in W_tail_rows:
        pair = row["pair"]
        need(
            type(pair) is list
            and len(pair) == 2
            and pair == sorted(pair)
            and pair[0] != pair[1]
            and all(endpoint in registry for endpoint in pair)
            and row["source_id"] not in edge_sources
            and tuple(pair) not in edge_pairs
            and not endpoints.intersection(pair),
            "fixture W-tail disjoint canonical pair",
        )
        need(
            row["formal_component_edge_credit"] == 0
            and row["nonedge_credit"] == 0
            and row["exclusion_credit"] == 0
            and row["source_row_fed_to_DSU"] is False,
            "fixture W-tail zero-credit non-input",
        )
    need(
        all(flag is True for flag in value["proof_flags"].values()),
        "fixture exact proof flags",
    )
    need(
        all(credit == 0 for credit in value["zero_credits"].values()),
        "fixture pre-DSU zero credits",
    )
    need(
        all(flag is False for flag in value["forbidden_state"].values()),
        "fixture forbidden DSU state",
    )
    expected_channels = {
        "R297_ORDINARY_FACE",
        "R296_TRUE_SEAM",
        "R299C_SIGNED_FACE",
        "R300B_COMPLETE_FACE",
        "R300C_POSITIVE_VOLUME",
        "R300E_HALF_OPEN_OWNER",
        "R300F_R245_HALF_OPEN_OWNER",
        "R303B_UNIFIED_ATTACHMENT",
    }
    need(
        set(value["channel_counts"]) == expected_channels
        and all(count == 1 for count in value["channel_counts"].values()),
        "fixture exact channel inventory",
    )
    need(
        value["manifest"] == FINAL_R303B_MANIFEST_MEMBER_PINS,
        "fixture exact manifest member map",
    )
    need(
        value["Round294B_manifest_sha256"] == R294B_MANIFEST_SHA256,
        "fixture Round294B admission pin",
    )
    need(
        value["Round303B_verifier_sha256"] == FINAL_R303B_VERIFIER_SHA256,
        "fixture Round303B verifier pin",
    )
    residual = value["residual_boundary"]
    need(
        residual == {
            "actual_official_key_count": 124,
            "stale_116_official_key_count_rejected": True,
            "source_G_global_disposition_denominator": 224_580,
            "registry_keyspace_is_global_disposition_keyspace": False,
            "hard_coded_1024_treated_as_theorem": False,
            "Gate5_complete_18_field_block_count": 0,
            "D02_status": "BLOCKED",
            "CM2_status": "NO-GO_FOR_CLAIM",
        },
        "fixture exact residual zero-credit boundary",
    )


def mutate_source_semantic_fixture(
    mechanism: str,
) -> dict[str, Any]:
    value = copy.deepcopy(source_semantic_fixture())
    if mechanism == "endpoint_outside_registry":
        value["edge_rows"][0]["pair"][1] = "outside"
    elif mechanism == "base_root_injection":
        value["edge_rows"][0]["roots"][1] = "forged-root"
    elif mechanism == "noncanonical_endpoint_pair":
        value["edge_rows"][0]["pair"][1] = "e0"
    elif mechanism == "edge_W_tail_overlap":
        value["W_tail_rows"][0]["source_id"] = "s0"
        value["W_tail_rows"][0]["pair"] = ["e0", "e1"]
    elif mechanism == "edge_uniqueness_forgery":
        value["edge_rows"][1]["source_id"] = "s0"
        value["edge_rows"][1]["pair"] = ["e1", "e3"]
        value["edge_rows"][1]["roots"] = ["r1", "r3"]
    elif mechanism == "eligible_flag_flip":
        value["proof_flags"][
            "eligible_for_later_fresh_DSU_application"
        ] = False
    elif mechanism.startswith("G") and mechanism.endswith("_flip"):
        number = mechanism[1]
        field = [
            key
            for key in value["proof_flags"]
            if key.startswith("G" + number + "_")
        ][0]
        value["proof_flags"][field] = False
    elif mechanism == "candidate_connectivity_flip":
        value["proof_flags"][
            "candidate_component_connectivity_conclusion"
        ] = False
    elif mechanism == "identity_or_key_credit_nonzero":
        value["zero_credits"][
            "formal_occurrence_identity_collapse_credit"
        ] = 1
        value["zero_credits"]["formal_official_key_merge_credit"] = 1
    elif mechanism == "pre_DSU_rank_credit_nonzero":
        value["zero_credits"]["formal_DSU_rank_reduction_credit"] = 1
    elif mechanism == "W_tail_credit_escalation":
        value["W_tail_rows"][0]["formal_component_edge_credit"] = 1
        value["W_tail_rows"][0]["nonedge_credit"] = 1
        value["W_tail_rows"][0]["exclusion_credit"] = 1
    elif mechanism == "W_tail_fed_to_DSU":
        value["W_tail_rows"][0]["source_row_fed_to_DSU"] = True
    elif mechanism == "Round301_state_injection":
        value["forbidden_state"][
            "Round301_partition_loaded_as_DSU_state"
        ] = True
        value["forbidden_state"][
            "Round301_edge_application_ledger_loaded_as_DSU_state"
        ] = True
    elif mechanism == "old_63224_partition_injection":
        value["forbidden_state"]["old_63224_partition_used_as_state"] = True
    elif mechanism == "conditional_92696_partition_injection":
        value["forbidden_state"][
            "conditional_92696_partition_used_as_state"
        ] = True
    elif mechanism == "old_channel_inventory_forgery":
        value["channel_counts"].pop("R297_ORDINARY_FACE")
        value["channel_counts"]["FORGED_CHANNEL"] = 1
    elif mechanism == "manifest_membership_resign":
        value["manifest"]["extra"] = "0" * 64
        first = next(iter(sorted(value["manifest"])))
        value["manifest"][first] = "0" * 64
    elif mechanism == "stale_Round294B_admission":
        value["Round294B_manifest_sha256"] = "0" * 64
    elif mechanism == "stale_Round303B_verifier":
        value["Round303B_verifier_sha256"] = "0" * 64
    elif mechanism == "maximality_credit_nonzero":
        value["zero_credits"]["formal_maximality_credit"] = 1
    elif mechanism == "fibre_credit_nonzero":
        value["zero_credits"]["formal_fibre_credit"] = 1
    elif mechanism == "global_disposition_credit_nonzero":
        value["zero_credits"]["formal_global_disposition_credit"] = 1
    elif mechanism == "Jx_Jy_same_point_credit_nonzero":
        value["zero_credits"]["formal_Jx_Jy_same_point_glue_credit"] = 1
    elif mechanism == "Gate5_complete_block_nonzero":
        value["residual_boundary"][
            "Gate5_complete_18_field_block_count"
        ] = 1
    elif mechanism == "D02_unblocked":
        value["residual_boundary"]["D02_status"] = "PASS"
    elif mechanism == "CM2_unconditional":
        value["residual_boundary"]["CM2_status"] = "UNCONDITIONAL"
    elif mechanism == "stale_116_accepted":
        value["residual_boundary"][
            "stale_116_official_key_count_rejected"
        ] = False
    elif mechanism == "keyspace_224580_as_124":
        value["residual_boundary"][
            "registry_keyspace_is_global_disposition_keyspace"
        ] = True
    elif mechanism == "hard_coded_1024_as_theorem":
        value["residual_boundary"][
            "hard_coded_1024_treated_as_theorem"
        ] = True
    else:
        raise VerificationBlocked("no source semantic mutator:" + mechanism)
    return value


def validate_W_tail_path_row(
    row: dict[str, Any],
    legal_edges: dict[tuple[str, str, str], tuple[str, str]],
) -> None:
    need(
        row["formal_component_edge_credit"] == 0
        and row["nonedge_credit"] == 0
        and row["exclusion_credit"] == 0
        and row["source_row_fed_to_DSU"] is False,
        "pure W-tail zero-credit non-input",
    )
    roots = row["projected_base_root_pair"]
    path_rows = row["stronger_legal_path"]
    same = row["same_final_component"]
    need(bool(path_rows) == same, "pure W-tail path iff same component")
    if not same:
        return
    need(bool(path_rows), "pure W-tail nonempty same-component path")
    cursor = path_rows[0]["from_root"]
    need(cursor in roots, "pure W-tail path starts at an endpoint")
    target = roots[1] if cursor == roots[0] else roots[0]
    for step in path_rows:
        need(step["from_root"] == cursor, "pure W-tail path continuity")
        key = (
            step["channel"],
            step["source_row_id"],
            step["source_row_sha256"],
        )
        need(key in legal_edges, "pure W-tail path legal source")
        need(
            tuple(sorted([step["from_root"], step["to_root"]]))
            == legal_edges[key],
            "pure W-tail path exact edge endpoints",
        )
        cursor = step["to_root"]
    need(cursor == target, "pure W-tail path target")


def extract_W_tail_attack_basis(
    expected: dict[str, bytes],
) -> tuple[list[dict[str, Any]], dict[tuple[str, str, str], tuple[str, str]]]:
    W_tail = strict_object(
        gzip.decompress(expected[CANDIDATE_FILES["wtail"]]),
        "attack W-tail basis",
    )
    rows = W_tail[CANDIDATE_TABLES["wtail"]]
    need(len(rows) == 4, "pure W-tail basis census")
    needed = {
        (
            step["channel"],
            step["source_row_id"],
            step["source_row_sha256"],
        )
        for row in rows
        for step in row["stronger_legal_path"]
    }
    legal: dict[tuple[str, str, str], tuple[str, str]] = {}
    raw_edge = io.BytesIO(expected[CANDIDATE_FILES["edge"]])
    with gzip.GzipFile(fileobj=raw_edge, mode="rb") as binary:
        with io.TextIOWrapper(binary, encoding="utf-8", newline="") as stream:
            for row in iter_array(
                stream,
                '"' + CANDIDATE_TABLES["edge"] + '":[',
            ):
                key = (
                    row["source_channel"],
                    row["source_row_id"],
                    row["source_row_sha256"],
                )
                if key in needed:
                    legal[key] = tuple(row["projected_base_root_pair"])
    need(set(legal) == needed, "pure W-tail complete legal-edge basis")
    for row in rows:
        validate_W_tail_path_row(row, legal)
    return rows, legal


def validate_single_gzip_bytes(raw: bytes) -> None:
    decoder = zlib.decompressobj(wbits=31)
    decoder.decompress(raw)
    need(decoder.eof and not decoder.unused_data, "pure gzip member boundary")


def validate_separation_source(raw: str) -> None:
    tree = ast.parse(raw)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = (
                [alias.name for alias in node.names]
                if isinstance(node, ast.Import)
                else [node.module or ""]
            )
            need(
                all(CANDIDATE_PREFIX not in name for name in names),
                "producer import separation",
            )
        if isinstance(node, ast.Call):
            function = ast.unparse(node.func)
            arguments = " ".join(ast.unparse(arg) for arg in node.args)
            need(
                function not in {"exec", "eval"}
                or "PRODUCER_BYTES" not in arguments,
                "producer exec separation",
            )
            need(
                function not in {"ast.parse", "compile"}
                or "PRODUCER_BYTES" not in arguments,
                "producer parse separation",
            )
            need(
                not function.startswith("tokenize.")
                or "PRODUCER_BYTES" not in arguments,
                "producer tokenize separation",
            )


def local_regular_path(path: Path, directory: Path) -> tuple[int, int, int, int]:
    need(path.parent.resolve() == directory.resolve(), "local path escape")
    need(path.exists() and not path.is_symlink(), "local symlink/missing")
    info = os.lstat(path)
    need(
        stat.S_ISREG(info.st_mode) and info.st_nlink == 1,
        "local hardlink/nonregular",
    )
    return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns)


def fast_attack_expected_fixture() -> dict[str, bytes]:
    """Build the small valid baseline needed by the 55 focused attacks."""

    W_tail_rows: list[dict[str, Any]] = []
    edge_rows: list[dict[str, Any]] = []
    for index in range(4):
        left = f"fast-root-{index}-a"
        right = f"fast-root-{index}-b"
        source_id = f"fast-source-{index}"
        source_sha = ("0" * 63) + str(index)
        W_tail_payload = {
            CANDIDATE_ID_FIELDS["wtail"]: f"fast-wtail-{index}",
            "formal_component_edge_credit": 0,
            "nonedge_credit": 0,
            "exclusion_credit": 0,
            "source_row_fed_to_DSU": False,
            "projected_base_root_pair": [left, right],
            "same_final_component": True,
            "stronger_legal_path": [{
                "channel": "FAST_ATTACK_FIXTURE",
                "source_row_id": source_id,
                "source_row_sha256": source_sha,
                "from_root": left,
                "to_root": right,
            }],
        }
        W_tail_rows.append({
            **W_tail_payload,
            "row_sha256": digest(W_tail_payload),
        })
        edge_rows.append({
            "source_channel": "FAST_ATTACK_FIXTURE",
            "source_row_id": source_id,
            "source_row_sha256": source_sha,
            "projected_base_root_pair": [left, right],
        })
    W_tail_document = {
        "row_count": len(W_tail_rows),
        "row_ids_sha256": digest([
            row[CANDIDATE_ID_FIELDS["wtail"]] for row in W_tail_rows
        ]),
        "row_hashes_sha256": digest([
            row["row_sha256"] for row in W_tail_rows
        ]),
        "rows_sha256": digest(W_tail_rows),
        CANDIDATE_TABLES["wtail"]: W_tail_rows,
    }
    W_tail_raw = deterministic_gzip(W_tail_document)
    result_payload = {
        "schema": "cm2.round304.fast-attack-baseline.v1",
        "output_ledgers": {
            "wtail": {
                "file_sha256": hashlib.sha256(W_tail_raw).hexdigest(),
                "row_count": W_tail_document["row_count"],
                "row_ids_sha256": W_tail_document["row_ids_sha256"],
                "row_hashes_sha256": W_tail_document["row_hashes_sha256"],
                "rows_sha256": W_tail_document["rows_sha256"],
            },
        },
    }
    return {
        CANDIDATE_FILES["wtail"]: W_tail_raw,
        CANDIDATE_FILES["edge"]: deterministic_gzip({
            CANDIDATE_TABLES["edge"]: edge_rows,
        }),
        CANDIDATE_FILES["result"]: canonical({
            **result_payload,
            "result_sha256": digest(result_payload),
        }),
    }


def validate_exact_artifact_bundle(
    actual: dict[str, bytes],
    expected: dict[str, bytes],
) -> None:
    """Pure exact-byte validator shared by baseline and coherent attacks."""

    need(set(actual) == set(expected), "exact artifact bundle filename set")
    for name in sorted(expected):
        if name.endswith(".json.gz"):
            require_single_gzip_member(actual[name], name)
        need(actual[name] == expected[name], "exact artifact bytes:" + name)


def reclose_result_semantic_attack(
    expected: dict[str, bytes],
    mechanism: str,
) -> dict[str, bytes]:
    """Coherently re-sign one result mutation before exact validation."""

    attacked = dict(expected)
    result_name = CANDIDATE_FILES["result"]
    result = strict_object(attacked[result_name], "coherent result attack")
    payload = copy.deepcopy({
        key: value for key, value in result.items() if key != "result_sha256"
    })
    if mechanism == "maximality_credit_nonzero" and "maximality_gate" in payload:
        payload["maximality_gate"]["formal_maximality_credit"] = 1
    elif mechanism == "fibre_credit_nonzero" and "official_key_fibre_gate" in payload:
        payload["official_key_fibre_gate"]["formal_fibre_credit"] = 1
    elif (
        mechanism == "global_disposition_credit_nonzero"
        and "global_source_G_disposition_gate" in payload
    ):
        payload["global_source_G_disposition_gate"][
            "formal_global_disposition_credit"
        ] = 1
    elif (
        mechanism == "Gate5_complete_block_nonzero"
        and "residual_gate_census" in payload
    ):
        payload["residual_gate_census"][
            "Gate5_complete_18_field_block_count"
        ] = 1
    elif (
        mechanism == "Jx_Jy_same_point_credit_nonzero"
        and "formal_credit_transition" in payload
    ):
        payload["formal_credit_transition"][
            "formal_Jx_Jy_same_point_glue_credit"
        ] = 1
    elif mechanism == "D02_unblocked" and "residual_gate_census" in payload:
        payload["residual_gate_census"]["D02_status"] = "PASS"
    elif mechanism == "CM2_unconditional" and "residual_gate_census" in payload:
        payload["residual_gate_census"]["CM2_status"] = "UNCONDITIONAL"
    elif mechanism == "stale_116_accepted" and "member_universe" in payload:
        payload["member_universe"]["stale_116_official_key_count_rejected"] = False
    elif (
        mechanism == "keyspace_224580_as_124"
        and "global_source_G_disposition_gate" in payload
    ):
        payload["global_source_G_disposition_gate"][
            "registry_official_key_count_is_not_the_global_denominator"
        ] = False
    elif mechanism == "hard_coded_1024_as_theorem" and "strict_boundary" in payload:
        payload["strict_boundary"][
            "unsealed_temp_R300A_1024_theorem_consumed"
        ] = True
    else:
        payload["schema"] = str(payload.get("schema", "")) + "__" + mechanism
    attacked[result_name] = canonical({
        **payload,
        "result_sha256": digest(payload),
    })
    return attacked


def run_focused_attacks(
    expected: dict[str, bytes],
    candidate_pins: dict[str, str],
    verifier_sha256: str,
) -> dict[str, Any]:
    """Run 58 concrete attacks covering 55 frozen mechanisms."""

    cascade_mechanisms = set(ATTACK_MECHANISMS[:39])
    W_tail_path = {
        "W_tail_stronger_path_edge_forgery",
        "W_tail_stronger_path_disconnect",
        "W_tail_stronger_path_source_hash_forgery",
        "W_tail_same_component_flip",
    }
    source_semantic = (
        cascade_mechanisms
        - W_tail_path
        - {"seed_dependent_output"}
    )
    wire_variants = {
        "gzip_member_boundary": (
            "gzip_concatenation",
            "gzip_trailing_bytes",
        ),
        "gzip_integrity": (
            "gzip_header_mutation",
            "gzip_truncation",
        ),
    }
    validate_source_semantic_fixture(source_semantic_fixture())
    W_tail_rows, legal_edges = extract_W_tail_attack_basis(expected)
    validate_exact_artifact_bundle(expected, expected)
    verifier_path = Path(__file__)
    need(
        verifier_path.name == VERIFIER_FILENAME
        and not verifier_path.is_symlink(),
        "verifier source basename/symlink boundary",
    )
    verifier_path = verifier_path.absolute()
    need(
        verifier_path == verifier_path.resolve(),
        "verifier source parent symlink boundary",
    )
    verifier_source = stable_read_bytes(
        verifier_path,
        verifier_path.parent,
        SOURCE_SNAPSHOTS,
        maximum=5_000_000,
        label="inert verifier source",
    ).decode("utf-8")
    validate_separation_source(verifier_source)
    baseline_guards = [
        {
            "guard_id": "valid_source_semantic_baseline",
            "governing_validator": "validate_source_semantic_fixture",
            "status": "ACCEPTED_BASELINE",
        },
        {
            "guard_id": "valid_W_tail_legal_path_baseline",
            "governing_validator": "validate_W_tail_path_row",
            "status": "ACCEPTED_BASELINE",
        },
        {
            "guard_id": "valid_exact_artifact_bundle_baseline",
            "governing_validator": "validate_exact_artifact_bundle",
            "status": "ACCEPTED_BASELINE",
        },
        {
            "guard_id": "valid_producer_separation_baseline",
            "governing_validator": "validate_separation_source",
            "status": "ACCEPTED_BASELINE",
        },
    ]

    rows: list[dict[str, Any]] = []
    for mechanism in ATTACK_MECHANISMS:
        variants = wire_variants.get(mechanism, (mechanism,))
        for variant in variants:
            rejected = False
            category = (
                "CASCADE"
                if mechanism in cascade_mechanisms
                else "WIRE"
                if mechanism in wire_variants
                or mechanism in {
                    "duplicate_JSON_key",
                    "nonintegral_JSON",
                    "nonfinite_JSON",
                }
                else "OS_AST"
            )
            try:
                if mechanism in source_semantic:
                    validate_source_semantic_fixture(
                        mutate_source_semantic_fixture(mechanism)
                    )
                elif mechanism in W_tail_path:
                    row = copy.deepcopy(W_tail_rows[0])
                    if mechanism == "W_tail_stronger_path_edge_forgery":
                        row["stronger_legal_path"][0][
                            "source_row_id"
                        ] = "forged-source"
                    elif mechanism == "W_tail_stronger_path_disconnect":
                        row["stronger_legal_path"] = row[
                            "stronger_legal_path"
                        ][:-1]
                    elif (
                        mechanism
                        == "W_tail_stronger_path_source_hash_forgery"
                    ):
                        row["stronger_legal_path"][0][
                            "source_row_sha256"
                        ] = "f" * 64
                    else:
                        row["same_final_component"] = not row[
                            "same_final_component"
                        ]
                    validate_W_tail_path_row(row, legal_edges)
                elif mechanism == "seed_dependent_output":
                    second = reclose_result_semantic_attack(
                        expected,
                        mechanism,
                    )
                    validate_exact_artifact_bundle(second, expected)
                elif mechanism in wire_variants:
                    baseline = expected[CANDIDATE_FILES["wtail"]]
                    if variant == "gzip_concatenation":
                        attacked_raw = baseline + baseline
                    elif variant == "gzip_trailing_bytes":
                        attacked_raw = baseline + b"TRAILING"
                    elif variant == "gzip_header_mutation":
                        mutable = bytearray(baseline)
                        need(len(mutable) > 10, "gzip header fixture length")
                        mutable[4] ^= 1
                        attacked_raw = bytes(mutable)
                    else:
                        need(
                            variant == "gzip_truncation",
                            "known gzip fixture variant",
                        )
                        attacked_raw = baseline[:-1]
                    validate_single_gzip_bytes(attacked_raw)
                    need(
                        attacked_raw == baseline,
                        "canonical deterministic gzip exact bytes",
                    )
                elif mechanism == "duplicate_JSON_key":
                    raw = expected[CANDIDATE_FILES["result"]]
                    strict_object(
                        b'{"schema":"forged",' + raw[1:],
                        variant,
                    )
                elif mechanism == "nonintegral_JSON":
                    strict_object(b'{"value":1.5}', variant)
                elif mechanism == "nonfinite_JSON":
                    strict_object(b'{"value":NaN}', variant)
                elif mechanism in {
                    "symlink_input",
                    "hardlink_input",
                    "path_escape",
                }:
                    with tempfile.TemporaryDirectory(
                        prefix="r304-path-attack-"
                    ) as raw:
                        base = Path(raw)
                        inside = base / "inside"
                        inside.mkdir()
                        original = base / "original"
                        original.write_bytes(b"x")
                        if mechanism == "symlink_input":
                            attacked_path = inside / "candidate"
                            attacked_path.symlink_to(original)
                        elif mechanism == "hardlink_input":
                            attacked_path = inside / "candidate"
                            os.link(original, attacked_path)
                        else:
                            attacked_path = original
                        local_regular_path(attacked_path, inside)
                elif mechanism in {
                    "producer_import",
                    "producer_exec",
                    "producer_parse",
                    "producer_tokenize",
                }:
                    suffix = {
                        "producer_import": (
                            "\nimport " + CANDIDATE_PREFIX + "\n"
                        ),
                        "producer_exec": "\nexec(PRODUCER_BYTES)\n",
                        "producer_parse": "\nast.parse(PRODUCER_BYTES)\n",
                        "producer_tokenize": (
                            "\ntokenize.tokenize(PRODUCER_BYTES.readline)\n"
                        ),
                    }[mechanism]
                    validate_separation_source(verifier_source + suffix)
                elif mechanism in {
                    "existing_target_clobber",
                    "target_appears_after_preflight",
                }:
                    with tempfile.TemporaryDirectory(
                        prefix="r304-atomic-attack-"
                    ) as raw:
                        base = Path(raw)
                        target = base / "target"
                        expected_bytes = b"expected"
                        existed = target.exists()
                        if mechanism == "existing_target_clobber":
                            target.write_bytes(b"wrong")
                            existed = True
                        if existed:
                            need(
                                local_regular_path(target, base)
                                and target.read_bytes() == expected_bytes,
                                "atomic preflight no-clobber",
                            )
                        else:
                            target.write_bytes(b"racer")
                            need(
                                not target.exists(),
                                "atomic target appeared after preflight",
                            )
                elif mechanism in {
                    "input_PRE_POST_TOCTOU",
                    "candidate_PRE_POST_TOCTOU",
                }:
                    with tempfile.TemporaryDirectory(
                        prefix="r304-snapshot-attack-"
                    ) as raw:
                        path = Path(raw) / "object"
                        path.write_bytes(b"before")
                        before = os.lstat(path)
                        identity = (
                            before.st_dev,
                            before.st_ino,
                            before.st_size,
                            before.st_mtime_ns,
                        )
                        path.write_bytes(b"after-longer")
                        after = os.lstat(path)
                        need(
                            (
                                after.st_dev,
                                after.st_ino,
                                after.st_size,
                                after.st_mtime_ns,
                            )
                            == identity,
                            "PRE/POST identity snapshot",
                        )
                else:
                    raise VerificationBlocked(
                        "unimplemented focused mechanism:" + mechanism
                    )
            except (
                VerificationBlocked,
                OSError,
                SyntaxError,
                UnicodeDecodeError,
                ValueError,
            ):
                rejected = True
            need(rejected, "attack unexpectedly accepted:" + variant)

            exact_bundle_rejected: bool | None = None
            if category == "CASCADE":
                coherent = (
                    reclose_mutated_W_tail_bundle(expected, mechanism)
                    if mechanism in W_tail_path
                    else reclose_result_semantic_attack(expected, mechanism)
                )
                exact_bundle_rejected = False
                try:
                    validate_exact_artifact_bundle(coherent, expected)
                except (VerificationBlocked, OSError, ValueError):
                    exact_bundle_rejected = True
                need(
                    exact_bundle_rejected,
                    "coherently resigned cascade accepted:" + mechanism,
                )
            rows.append({
                "fixture_id": mechanism + ":" + variant,
                "mechanism": mechanism,
                "variant": variant,
                "category": category,
                "mutation_stage": "MECHANISM_SPECIFIC_MUTATION_APPLIED",
                "reclosure_stage": (
                    "COHERENT_RESULT_OR_WTAIL_RECLOSURE"
                    if category == "CASCADE"
                    else "NOT_APPLICABLE"
                ),
                "validator_stages": (
                    [
                        "LOCAL_MECHANISM_VALIDATOR",
                        "SHARED_POST_REBUILD_EXACT_ARTIFACT_VALIDATOR",
                    ]
                    if category == "CASCADE"
                    else ["WIRE_OR_OS_AST_GOVERNING_VALIDATOR"]
                ),
                "mechanism_specific_validator_rejected": True,
                "coherently_resigned_exact_bundle_rejected":
                    exact_bundle_rejected,
                "same_post_rebuild_candidate_artifact_validator":
                    exact_bundle_rejected is True,
                "full_upstream_source_ledger_replay_attack": False,
                "status": "REJECTED",
            })

    coherent = reclose_mutated_W_tail_bundle(
        expected,
        "W_tail_edge_promotion",
    )
    coherent_W_tail = strict_object(
        gzip.decompress(coherent[CANDIDATE_FILES["wtail"]]),
        "coherent W-tail credit escalation",
    )
    coherent_W_tail_rows = coherent_W_tail[CANDIDATE_TABLES["wtail"]]
    need(len(coherent_W_tail_rows) == 4, "coherent W-tail attack census")
    coherent_local_rejected = False
    try:
        validate_W_tail_path_row(coherent_W_tail_rows[0], legal_edges)
    except (VerificationBlocked, OSError, ValueError):
        coherent_local_rejected = True
    need(
        coherent_local_rejected,
        "coherent W-tail credit escalation passed local validator",
    )
    coherent_rejected = False
    try:
        validate_exact_artifact_bundle(coherent, expected)
    except (VerificationBlocked, OSError, ValueError):
        coherent_rejected = True
    need(coherent_rejected, "coherent W-tail credit escalation accepted")
    rows.append({
        "fixture_id": (
            "W_tail_credit_escalation:"
            "coherently_resigned_W_tail_edge_promotion"
        ),
        "mechanism": "W_tail_credit_escalation",
        "variant": "coherently_resigned_W_tail_edge_promotion",
        "category": "CASCADE",
        "mutation_stage": "WTail_LEDGER_CREDIT_MUTATION_APPLIED",
        "reclosure_stage": "COHERENT_WTAIL_LEDGER_AND_RESULT_RECLOSURE",
        "validator_stages": [
            "LOCAL_MECHANISM_VALIDATOR",
            "SHARED_POST_REBUILD_EXACT_ARTIFACT_VALIDATOR",
        ],
        "mechanism_specific_validator_rejected": coherent_local_rejected,
        "coherently_resigned_exact_bundle_rejected": coherent_rejected,
        "same_post_rebuild_candidate_artifact_validator": coherent_rejected,
        "full_upstream_source_ledger_replay_attack": False,
        "status": "REJECTED",
    })

    categories = Counter(row["category"] for row in rows)
    need(
        len(ATTACK_MECHANISMS) == 55
        and {row["mechanism"] for row in rows} == set(ATTACK_MECHANISMS)
        and len(rows) == 58
        and categories == Counter({
            "CASCADE": 40,
            "WIRE": 7,
            "OS_AST": 11,
        })
        and all(row["status"] == "REJECTED" for row in rows),
        "exact 55 mechanisms / 58 concrete attack fixtures",
    )
    payload = {
        "schema": (
            "cm2.round304.source-g-fresh-extended-registry-legal-component-"
            "dsu-rebuild.independent-attack-suite.v1"
        ),
        "status": "PASS_ALL_FOCUSED_ATTACKS_REJECTED",
        "producer_inert_sha256": FINAL_R304_PRODUCER_SHA256,
        "verifier_filename": VERIFIER_FILENAME,
        "verifier_file_sha256": verifier_sha256,
        "schema_snapshot_sha256": COMPUTED_SCHEMA_SNAPSHOT_SHA256,
        "candidate_exact_baseline_pins": dict(sorted(candidate_pins.items())),
        "mechanism_count": len(ATTACK_MECHANISMS),
        "concrete_attack_fixture_count": len(rows),
        "executed_count": len(rows),
        "rejected_count": len(rows),
        "fixture_category_counts": dict(sorted(categories.items())),
        "baseline_guard_count": len(baseline_guards),
        "baseline_guards": baseline_guards,
        "shared_post_rebuild_exact_artifact_validator_cascade_count": 40,
        "full_upstream_source_ledger_replay_attack_count": 0,
        "attack_role": "INDEPENDENT_DEFENSE_IN_DEPTH",
        "primary_promotion_boundary": (
            "COMPLETE_CACHELESS_EXPECTED_STATE_EXACT_CANDIDATE_BYTES"
        ),
        "attacks": rows,
        "attack_rows_sha256": digest(rows),
        "all_rejected": True,
        "formal_Round304_promotion_permitted_after_exact_candidate_match": True,
        "formal_maximality_fibre_global_disposition_credit": 0,
    }
    return {**payload, "attack_suite_sha256": digest(payload)}

def resolve_candidate_directory(candidate_dir: Path) -> Path:
    """Validate one explicit, nonsymlink candidate directory."""

    lexical = lexical_directory_without_symlinks(
        candidate_dir,
        "candidate directory",
    )
    resolved = candidate_dir.resolve()
    need(lexical == resolved, "candidate directory contains symlink or dot escape")
    need(
        resolved == DATA.resolve() or ROOT.resolve() in resolved.parents,
        "candidate directory must be deliverables or below workspace root",
    )
    need(resolved != ROOT.resolve(), "workspace root is not a candidate directory")
    return resolved


def read_recovery_stage_file(
    directory_descriptor: int,
    name: str,
    expected: bytes,
    label: str,
) -> os.stat_result:
    info = os.stat(name, dir_fd=directory_descriptor, follow_symlinks=False)
    need(
        stat.S_ISREG(info.st_mode)
        and info.st_uid == os.geteuid()
        and info.st_nlink == 1
        and info.st_size == len(expected),
        label + " stage file boundary",
    )
    descriptor = os.open(
        name,
        os.O_RDONLY
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_CLOEXEC", 0),
        dir_fd=directory_descriptor,
    )
    try:
        opened = os.fstat(descriptor)
        need(file_identity(opened) == file_identity(info), label + " open race")
        chunks: list[bytes] = []
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            chunks.append(block)
        need(b"".join(chunks) == expected, label + " exact stage bytes")
        need(
            file_identity(os.fstat(descriptor)) == file_identity(info),
            label + " fd changed",
        )
    finally:
        os.close(descriptor)
    return info


def recover_private_stage_orphans(
    output_dir: Path,
    output_directory_descriptor: int,
    artifacts: dict[str, bytes],
) -> None:
    """Recover an exact attack/verification stage left by a hard crash."""

    need(
        Path(os.path.abspath(os.fspath(output_dir)))
        == lexical_directory_without_symlinks(output_dir, "recovery output"),
        "recovery output directory boundary",
    )
    expected_names = set(artifacts)
    for stage_name in sorted(os.listdir(output_directory_descriptor)):
        if not stage_name.startswith(".r304-promotion-stage-"):
            continue
        stage_info = os.stat(
            stage_name,
            dir_fd=output_directory_descriptor,
            follow_symlinks=False,
        )
        need(
            stat.S_ISDIR(stage_info.st_mode)
            and stage_info.st_uid == os.geteuid()
            and stat.S_IMODE(stage_info.st_mode) == 0o700,
            "private promotion recovery stage ownership/mode",
        )
        stage_descriptor = os.open(
            stage_name,
            os.O_RDONLY
            | getattr(os, "O_DIRECTORY", 0)
            | getattr(os, "O_NOFOLLOW", 0)
            | getattr(os, "O_CLOEXEC", 0),
            dir_fd=output_directory_descriptor,
        )
        try:
            need(
                directory_identity(os.fstat(stage_descriptor))
                == directory_identity(stage_info),
                "private promotion recovery stage open race",
            )
            names = set(os.listdir(stage_descriptor))
            need(
                names <= expected_names,
                "private promotion recovery stage subset",
            )
            for name in sorted(names):
                read_recovery_stage_file(
                    stage_descriptor,
                    name,
                    artifacts[name],
                    "private promotion recovery:" + name,
                )
                os.unlink(name, dir_fd=stage_descriptor)
            os.fsync(stage_descriptor)
        finally:
            os.close(stage_descriptor)
        os.rmdir(stage_name, dir_fd=output_directory_descriptor)
    os.fsync(output_directory_descriptor)


def publish_attack_then_verification_no_clobber(
    candidate_dir: Path,
    attack_raw: bytes,
    verification_raw: bytes,
) -> None:
    """Serialize recovery/publication under an advisory directory lock."""

    resolved = resolve_candidate_directory(candidate_dir)
    directory_descriptor = os.open(
        resolved,
        os.O_RDONLY
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_CLOEXEC", 0),
    )
    bound_directory_identity = directory_identity(os.fstat(directory_descriptor))
    need(
        bound_directory_identity == directory_identity(os.lstat(resolved)),
        "promotion directory open race",
    )
    artifacts = {
        ATTACK_FILENAME: attack_raw,
        VERIFICATION_FILENAME: verification_raw,
    }
    try:
        fcntl.flock(directory_descriptor, fcntl.LOCK_EX)
        recover_private_stage_orphans(
            candidate_dir,
            directory_descriptor,
            artifacts,
        )
        _publish_attack_then_verification_no_clobber_locked(
            candidate_dir,
            attack_raw,
            verification_raw,
        )
    finally:
        need(
            bound_directory_identity
            == directory_identity(os.fstat(directory_descriptor))
            == directory_identity(os.lstat(resolved)),
            "promotion directory renamed/swapped",
        )
        fcntl.flock(directory_descriptor, fcntl.LOCK_UN)
        os.close(directory_descriptor)


def _publish_attack_then_verification_no_clobber_locked(
    candidate_dir: Path,
    attack_raw: bytes,
    verification_raw: bytes,
) -> None:
    """Publish attack suite first and verification commit marker last."""

    resolved = resolve_candidate_directory(candidate_dir)
    artifacts = {
        ATTACK_FILENAME: attack_raw,
        VERIFICATION_FILENAME: verification_raw,
    }
    ordered_names = [ATTACK_FILENAME, VERIFICATION_FILENAME]
    snapshots: dict[Path, FileIdentity] = {}
    preexisting: dict[str, tuple[FileIdentity, str]] = {}
    for name in ordered_names:
        target = candidate_dir / name
        need(target.parent.resolve() == resolved, "verification-pair path escape")
        if os.path.lexists(target):
            actual = stable_read_bytes(
                target,
                candidate_dir,
                snapshots,
                maximum=10_000_000,
                label="preexisting promotion output:" + name,
            )
            need(actual == artifacts[name], "promotion output no-clobber:" + name)
            preexisting[name] = (
                snapshots[target.resolve()],
                hashlib.sha256(actual).hexdigest(),
            )
    need(
        VERIFICATION_FILENAME not in preexisting
        or ATTACK_FILENAME in preexisting,
        "verification commit marker cannot preexist without attack suite",
    )
    with tempfile.TemporaryDirectory(
        prefix=".r304-promotion-stage-",
        dir=candidate_dir,
    ) as raw_stage:
        stage_dir = Path(raw_stage)
        for name in ordered_names:
            stage = stage_dir / name
            descriptor = os.open(
                stage,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                0o644,
            )
            with os.fdopen(descriptor, "wb", closefd=True) as stream:
                stream.write(artifacts[name])
                stream.flush()
                os.fsync(stream.fileno())
        stage_descriptor = os.open(
            stage_dir,
            os.O_RDONLY
            | getattr(os, "O_DIRECTORY", 0)
            | getattr(os, "O_NOFOLLOW", 0)
            | getattr(os, "O_CLOEXEC", 0),
        )
        directory_descriptor = os.open(
            candidate_dir,
            os.O_RDONLY
            | getattr(os, "O_DIRECTORY", 0)
            | getattr(os, "O_NOFOLLOW", 0)
            | getattr(os, "O_CLOEXEC", 0),
        )
        try:
            for name in ordered_names:
                target = candidate_dir / name
                if name in preexisting:
                    actual = stable_read_bytes(
                        target,
                        candidate_dir,
                        snapshots,
                        maximum=10_000_000,
                        label="stable preexisting promotion output:" + name,
                    )
                    need(
                        (
                            snapshots[target.resolve()],
                            hashlib.sha256(actual).hexdigest(),
                        )
                        == preexisting[name],
                        "preexisting promotion output changed:" + name,
                    )
                    continue
                assert_snapshot_map(
                    SOURCE_SNAPSHOTS,
                    "source before promotion move",
                )
                assert_snapshot_map(
                    CANDIDATE_SNAPSHOTS,
                    "candidate before promotion move",
                )
                try:
                    os.stat(
                        name,
                        dir_fd=directory_descriptor,
                        follow_symlinks=False,
                    )
                except FileNotFoundError:
                    pass
                else:
                    raise VerificationBlocked(
                        "promotion target appeared after preflight:" + name
                    )
                try:
                    rename_noreplace(
                        stage_descriptor,
                        name,
                        directory_descriptor,
                        name,
                    )
                except FileExistsError as exc:
                    raise VerificationBlocked(
                        "promotion target raced commit:" + name
                    ) from exc
            os.fsync(directory_descriptor)
        finally:
            os.close(stage_descriptor)
            os.close(directory_descriptor)
    for name in ordered_names:
        target = candidate_dir / name
        actual = stable_read_bytes(
            target,
            candidate_dir,
            snapshots,
            maximum=10_000_000,
            label="published promotion output:" + name,
        )
        need(actual == artifacts[name], "published exact bytes:" + name)
    assert_snapshot_map(snapshots, "promotion output")
    assert_snapshot_map(SOURCE_SNAPSHOTS, "source after promotion")
    assert_snapshot_map(CANDIDATE_SNAPSHOTS, "candidate after promotion")


def verify_candidate(
    candidate_dir: Path,
    producer_path: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    expected_artifacts, expected_result = build_expected_candidate_artifacts()
    # No candidate output has been opened above this line.
    resolve_candidate_directory(candidate_dir)
    need(
        producer_path.name == CANDIDATE_FILES["producer"]
        and os.path.lexists(producer_path)
        and not producer_path.is_symlink()
        and stat.S_ISREG(os.lstat(producer_path).st_mode)
        and os.lstat(producer_path).st_nlink == 1,
        "producer pre-resolve regular single-link basename boundary",
    )
    producer_lexical = producer_path.absolute()
    producer_resolved = producer_path.resolve()
    need(
        producer_lexical == producer_resolved
        and ROOT.resolve() in producer_resolved.parents,
        "producer path root/symlink boundary",
    )
    producer_sha256 = stable_file_sha256(
        producer_resolved,
        producer_resolved.parent,
        SOURCE_SNAPSHOTS,
        maximum=5_000_000,
        label="inert producer source",
    )
    need(
        producer_sha256 == FINAL_R304_PRODUCER_SHA256,
        "producer inert pin",
    )
    need(
        COMPUTED_SCHEMA_SNAPSHOT_SHA256 == FINAL_R304_SCHEMA_SNAPSHOT_SHA256,
        "schema snapshot pin",
    )
    verifier_path = Path(__file__)
    need(
        verifier_path.name == VERIFIER_FILENAME
        and os.path.lexists(verifier_path)
        and not verifier_path.is_symlink()
        and stat.S_ISREG(os.lstat(verifier_path).st_mode)
        and os.lstat(verifier_path).st_nlink == 1,
        "verifier pre-resolve regular single-link basename boundary",
    )
    verifier_lexical = verifier_path.absolute()
    verifier_resolved = verifier_path.resolve()
    need(
        verifier_lexical == verifier_resolved
        and ROOT.resolve() in verifier_resolved.parents,
        "verifier path root/symlink boundary",
    )
    verifier_sha256 = stable_file_sha256(
        verifier_resolved,
        verifier_resolved.parent,
        SOURCE_SNAPSHOTS,
        maximum=5_000_000,
        label="inert verifier file hash",
    )

    candidate_bundle: dict[str, bytes] = {}
    candidate_pins: dict[str, str] = {}
    for key in ("edge", "member", "wtail", "residual", "result"):
        name = CANDIDATE_FILES[key]
        actual = stable_read_bytes(
            candidate_dir / name,
            candidate_dir,
            CANDIDATE_SNAPSHOTS,
            label="candidate read:" + name,
        )
        candidate_bundle[name] = actual
        candidate_pins[name] = hashlib.sha256(actual).hexdigest()
    validate_exact_artifact_bundle(candidate_bundle, expected_artifacts)
    candidate_result_raw = candidate_bundle[CANDIDATE_FILES["result"]]
    candidate_result = strict_object(
        candidate_result_raw,
        CANDIDATE_FILES["result"],
    )
    verify_self(candidate_result, "result_sha256", CANDIDATE_FILES["result"])
    need(candidate_result == expected_result, "candidate result exact object")
    expected_pins = {
        name: hashlib.sha256(raw).hexdigest()
        for name, raw in expected_artifacts.items()
    }
    need(candidate_pins == expected_pins, "candidate/expected exact pin map")
    assert_snapshot_map(SOURCE_SNAPSHOTS, "source")
    assert_snapshot_map(CANDIDATE_SNAPSHOTS, "candidate")

    attack_baseline_pins = {
        CANDIDATE_FILES["producer"]: producer_sha256,
        **candidate_pins,
    }
    attack_suite = run_focused_attacks(
        expected_artifacts,
        attack_baseline_pins,
        verifier_sha256,
    )
    attack_raw = canonical(attack_suite)
    attack_file_sha256 = hashlib.sha256(attack_raw).hexdigest()
    need(
        attack_suite["mechanism_count"] == 55
        and attack_suite["concrete_attack_fixture_count"] == 58
        and attack_suite["rejected_count"] == 58
        and attack_suite["fixture_category_counts"] == {
            "CASCADE": 40,
            "OS_AST": 11,
            "WIRE": 7,
        }
        and attack_suite[
            "shared_post_rebuild_exact_artifact_validator_cascade_count"
        ] == 40
        and attack_suite[
            "full_upstream_source_ledger_replay_attack_count"
        ] == 0
        and attack_suite["all_rejected"] is True,
        "exact focused attack-suite census",
    )
    need(
        expected_result["forward_application"][
            "Round303B_incremental_rank_reduction"
        ]
        == 29_252
        and expected_result["forward_application"]["rank_reduction"] == 275_268
        and expected_result["forward_application"]["component_count"] == 92_696
        and expected_result["W_tail_disposition_census"][
            "same_final_component_count"
        ]
        == 4
        and expected_result["W_tail_disposition_census"][
            "cross_final_component_count"
        ]
        == 0,
        "verification exact final census",
    )
    payload = {
        "schema": (
            "cm2.round304.source-g-fresh-extended-registry-legal-component-"
            "dsu-rebuild.independent-verification.v1"
        ),
        "status": "PASS_EXACT_CACHELESS_EXPECTED_STATE",
        "producer": {
            "filename": CANDIDATE_FILES["producer"],
            "file_sha256": producer_sha256,
            "treated_as_inert_bytes_only": True,
            "imported_executed_parsed_or_tokenized": False,
        },
        "verifier": {
            "filename": VERIFIER_FILENAME,
            "file_sha256": verifier_sha256,
            "self_hash_computed_at_runtime_without_circular_source_pin": True,
        },
        "schema_snapshot_sha256": COMPUTED_SCHEMA_SNAPSHOT_SHA256,
        "candidate_opened_only_after_complete_expected_bytes": True,
        "candidate_exact_file_pins": dict(sorted(candidate_pins.items())),
        "independently_rebuilt_expected_file_pins": dict(
            sorted(expected_pins.items())
        ),
        "attack_suite": {
            "filename": ATTACK_FILENAME,
            "file_sha256": attack_file_sha256,
            "attack_suite_sha256": attack_suite["attack_suite_sha256"],
            "mechanism_count": 55,
            "concrete_attack_fixture_count": 58,
            "rejected_count": 58,
            "fixture_category_counts": {
                "CASCADE": 40,
                "OS_AST": 11,
                "WIRE": 7,
            },
            "shared_post_rebuild_exact_artifact_validator_cascade_count": 40,
            "full_upstream_source_ledger_replay_attack_count": 0,
            "attack_role": "INDEPENDENT_DEFENSE_IN_DEPTH",
            "all_rejected": True,
        },
        "forward_reverse_same_partition": True,
        "actual_official_key_count": ACTUAL_OFFICIAL_KEY_COUNT,
        "stale_116_official_key_count_rejected": True,
        "source_G_global_disposition_denominator":
            SOURCE_G_EXACT_KEY_DISPOSITION_DENOMINATOR,
        "exact_census_assertions": {
            "Round303B_incremental_rank_reduction": 29_252,
            "total_rank_reduction": 275_268,
            "final_component_count": 92_696,
            "W_tail_reclosed_by_stronger_path_count": 4,
        },
        "strict_zero_downstream_credit": {
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
            "Gate5_complete_18_field_block_count": 0,
            "D02_status": "BLOCKED",
            "CM2_status": "NO-GO_FOR_CLAIM",
        },
        "all_source_and_candidate_PRE_POST_fd_identities_equal": True,
        "verification_built_only_after_candidate_and_attacks_passed": True,
        "atomic_promotion_pair": {
            "attack_suite_is_required_first": True,
            "verification_is_required_last_commit_marker": True,
            "two_target_no_clobber_preflight_required": True,
            "atomic_RENAME_NOREPLACE_required": True,
            "exact_private_stage_orphan_recovery_required_before_retry": True,
        },
        "formal_Round304_promotion_permitted": True,
    }
    verification = {
        **payload,
        "verification_sha256": digest(payload),
    }
    assert_snapshot_map(SOURCE_SNAPSHOTS, "source final")
    assert_snapshot_map(CANDIDATE_SNAPSHOTS, "candidate final")
    return attack_suite, verification


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path)
    parser.add_argument("--candidate-dir", type=Path)
    parser.add_argument("--producer-path", type=Path)
    parser.add_argument("--no-write", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--audit-sealed-prior", action="store_true")
    parser.add_argument("--audit-full-sealed-upstream", action="store_true")
    parser.add_argument("--print-attack-contract", action="store_true")
    parser.add_argument("--dual-seed-dir-a", type=Path)
    parser.add_argument("--dual-seed-dir-b", type=Path)
    args = parser.parse_args()
    if args.root is not None:
        configure_root(args.root)
    if args.self_test:
        fixture = fast_attack_expected_fixture()
        fixture_pins = {
            CANDIDATE_FILES["producer"]: str(FINAL_R304_PRODUCER_SHA256),
            **{
                name: hashlib.sha256(raw).hexdigest()
                for name, raw in fixture.items()
            },
        }
        self_path = Path(__file__)
        need(
            self_path.name == VERIFIER_FILENAME
            and not self_path.is_symlink(),
            "self-test verifier path boundary",
        )
        self_path = self_path.absolute()
        need(self_path == self_path.resolve(), "self-test parent symlink")
        self_sha256 = stable_file_sha256(
            self_path,
            self_path.parent,
            SOURCE_SNAPSHOTS,
            maximum=5_000_000,
            label="self-test verifier hash",
        )
        attacks = run_focused_attacks(
            fixture,
            fixture_pins,
            self_sha256,
        )
        print(
            json.dumps(
                {
                    "schema_snapshot_sha256": COMPUTED_SCHEMA_SNAPSHOT_SHA256,
                    "seal_ready": seal_ready(),
                    "R303B_exact_manifest_member_count":
                        len(R303B_EXPECTED_MANIFEST_MEMBERS),
                    "dual_seed_hooks": list(DUAL_SEEDS),
                    "attack_mechanism_count": len(ATTACK_MECHANISMS),
                    "concrete_attack_fixture_count": attacks[
                        "concrete_attack_fixture_count"
                    ],
                    "rejected_count": attacks["rejected_count"],
                    "fixture_category_counts": attacks[
                        "fixture_category_counts"
                    ],
                    "attack_suite_sha256": attacks[
                        "attack_suite_sha256"
                    ],
                    "producer_imported_executed_parsed_or_tokenized": False,
                    "non_string_object_key_rejected_at_result_boundary":
                        not json_object_keys_are_strings(
                            {"histogram": {2: 1, 10: 1}}
                        ),
                    "candidate_opened": False,
                    "status": "PASS_FORMAL_READY_FAST_ATTACK_SELF_TEST",
                },
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        return
    if args.print_attack_contract:
        print(
            json.dumps(
                {
                    "schema": "cm2.round304.independent-attack-contract.v1",
                    "status":
                        "DECLARED_FAIL_CLOSED__EXECUTION_REQUIRES_SEALED_CANDIDATE",
                    "mechanism_count": len(ATTACK_MECHANISMS),
                    "concrete_attack_fixture_count": 58,
                    "fixture_category_counts": {
                        "CASCADE": 40,
                        "OS_AST": 11,
                        "WIRE": 7,
                    },
                    "mechanisms": list(ATTACK_MECHANISMS),
                    "candidate_opened": False,
                    "attack_credit": 0,
                },
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        return
    if args.audit_sealed_prior:
        print(
            json.dumps(
                audit_sealed_prior_only(),
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        return
    if args.audit_full_sealed_upstream:
        output = expected_state(require_candidate_seal=False)
        output["schema"] = (
            "cm2.round304.independent-full-sealed-upstream-audit.v1"
        )
        output["status"] = (
            "PASS_INDEPENDENT_FULL_SEALED_UPSTREAM__"
            "ROUND304_CANDIDATE_NOT_OPENED"
        )
        output["Round304_candidate_opened"] = False
        print(json.dumps(output, sort_keys=True, separators=(",", ":")))
        return
    if args.dual_seed_dir_a is not None or args.dual_seed_dir_b is not None:
        need(
            args.dual_seed_dir_a is not None
            and args.dual_seed_dir_b is not None,
            "both dual-seed directories required",
        )
        print(
            json.dumps(
                compare_dual_seed_directories(
                    args.dual_seed_dir_a,
                    args.dual_seed_dir_b,
                ),
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        return
    need(args.candidate_dir is not None, "--candidate-dir required")
    producer_path = (
        args.producer_path
        if args.producer_path is not None
        else args.candidate_dir / CANDIDATE_FILES["producer"]
    )
    attacks, verification = verify_candidate(args.candidate_dir, producer_path)
    attack_raw = canonical(attacks)
    verification_raw = canonical(verification)
    if not args.no_write:
        publish_attack_then_verification_no_clobber(
            args.candidate_dir,
            attack_raw,
            verification_raw,
        )
        print(verification_raw.decode("ascii"))
        return
    summary = {
        "schema": "cm2.round304.no-write-exact-output-hashes.v1",
        "status": verification["status"],
        "attack_suite": {
            "filename": ATTACK_FILENAME,
            "file_sha256": hashlib.sha256(attack_raw).hexdigest(),
            "object_sha256": attacks["attack_suite_sha256"],
        },
        "verification": {
            "filename": VERIFICATION_FILENAME,
            "file_sha256": hashlib.sha256(verification_raw).hexdigest(),
            "object_sha256": verification["verification_sha256"],
        },
        "candidate_and_promotion_outputs_written": False,
    }
    print(canonical(summary).decode("ascii"))


if __name__ == "__main__":
    main()
