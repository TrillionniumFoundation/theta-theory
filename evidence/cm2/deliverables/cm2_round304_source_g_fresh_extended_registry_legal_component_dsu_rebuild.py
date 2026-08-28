#!/usr/bin/env python3
"""Round304 fresh extended-registry legal-component DSU producer.

The producer opens Round303B only through its frozen twelve-member seal and
rebuilds the DSU from source ledgers.  It never reads a serialized Round301
partition as DSU state.  Formal publication is an explicit ``--candidate-dir``
operation with no-clobber staging and the result committed last.
"""

from __future__ import annotations

import argparse
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
from collections import Counter, defaultdict, deque
from collections.abc import Callable, Iterable, Iterator
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
INPUT_SNAPSHOTS: dict[Path, FileIdentity] = {}
PARENT_DIRECTORY_SNAPSHOTS: dict[Path, DirectoryIdentity] = {}

# Frozen pins from one completed exact Round303B manifest.
R303B_MANIFEST_SHA256: str | None = (
    "7d7293c488a05c8873a63b7d63d0bf125260c6b9d3c60595201896cfde0c9786"
)
R303B_PRODUCER_SHA256: str | None = (
    "02ce70a560b7fa029e2c7a70a1e4627cb423ac67ba187dba059b57194a646735"
)
R303B_VERIFIER_SHA256: str | None = (
    "420883fbc6b2ad5a8413e51635b814bac7c1f059e1ff937765e38c8ac98ff88f"
)
R303B_VERIFICATION_FILE_SHA256: str | None = (
    "6dde1fc938c5059290b811d297306ae16347fd93624a29d7b0ba59974cc06d5a"
)
R303B_VERIFICATION_OBJECT_SHA256: str | None = (
    "a803d41e9be3513fb2b2e1ac87e22b35c83c2e678647105708a0857339cbfe57"
)
R303B_RESULT_SHA256: str | None = (
    "4bd7127f9d935cf7b334fd7660fa6332f8aa23a9c819ac7e018c8add8473eaa1"
)
R303B_EDGE_LEDGER_SHA256: str | None = (
    "650df67dfcc3033c42b36638a0da4b3d63ce575469cab84a5e8971ed7b23243a"
)
R303B_WTAIL_LEDGER_SHA256: str | None = (
    "eaa18cdec4217e57238d8e5b4209c33295dc325dbb352f1d52347e0d18acdf8e"
)
R303B_MANIFEST_MEMBER_PINS: dict[str, str] | None = {
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
R303B = {
    "producer": "cm2_round303b_source_g_unified_attachment_edge_producer.py",
    "manifest": R303B_PREFIX + "_manifest.sha256",
    "result": R303B_PREFIX + "_result.json",
    "verifier": R303B_PREFIX + "_verifier.py",
    "verification": R303B_PREFIX + "_verification.json",
    "edge": R303B_PREFIX + "_component_edge_ledger.json.gz",
    "unresolved": R303B_PREFIX + "_wtail_unresolved_ledger.json.gz",
    "b1": R303B_PREFIX + "_b1_graph_attachment_lemma_ledger.json.gz",
    "b2a": R303B_PREFIX + "_b2a_analytic_sheet_lemma_ledger.json.gz",
    "b2b": R303B_PREFIX + "_b2b_physical_inclusion_lemma_ledger.json.gz",
    "attack": R303B_PREFIX + "_attack_suite.json",
    "report": R303B_PREFIX + "_report.md",
    "cold": R303B_PREFIX + "_cold_replay.md",
}
R303B_EXPECTED_MANIFEST_MEMBERS = frozenset(
    value for key, value in R303B.items() if key != "manifest"
)

R304_PREFIX = (
    "cm2_round304_source_g_fresh_extended_registry_legal_component_dsu_rebuild"
)
R304_FILES = {
    "producer": R304_PREFIX + ".py",
    "edge": R304_PREFIX + "_edge_application_ledger.json.gz",
    "member": R304_PREFIX + "_member_component_ledger.json.gz",
    "wtail": R304_PREFIX + "_wtail_disposition_ledger.json.gz",
    "residual": R304_PREFIX + "_residual_gate_ledger.json.gz",
    "result": R304_PREFIX + "_result.json",
}
R304_TABLES = {
    "edge": "fresh_DSU_edge_application_rows",
    "member": "fresh_member_component_rows",
    "wtail": "W_tail_stronger_path_disposition_rows",
    "residual": "post_DSU_residual_gate_rows",
}
R304_ID_FIELDS = {
    "edge": "Round304_fresh_DSU_edge_application_row_id",
    "member": "Round304_fresh_member_component_row_id",
    "wtail": "Round304_W_tail_disposition_row_id",
    "residual": "Round304_residual_gate_row_id",
}
R304_ROW_SCHEMAS = {
    "edge": "cm2.round304.fresh-dsu-edge-application-row.v1",
    "member": "cm2.round304.fresh-member-component-row.v1",
    "wtail": "cm2.round304.wtail-stronger-path-disposition-row.v1",
    "residual": "cm2.round304.post-dsu-residual-gate-row.v1",
}
R304_LEDGER_SCHEMAS = {
    key: value.removesuffix("-row.v1") + "-ledger.v1"
    for key, value in R304_ROW_SCHEMAS.items()
}
R304_RESULT_SCHEMA = (
    "cm2.round304.source-g-fresh-extended-registry-legal-component-"
    "dsu-rebuild.v1"
)
R304_EXACT_ROW_FIELDS = {
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
R304_EXACT_LEDGER_BASE_FIELDS = (
    "row_count",
    "row_hashes_sha256",
    "row_ids_sha256",
    "rows_sha256",
    "schema",
    "status",
)
R304_EXACT_LEDGER_FIELDS = {
    key: tuple(sorted((*R304_EXACT_LEDGER_BASE_FIELDS, table)))
    for key, table in R304_TABLES.items()
}
R304_EXACT_RESULT_FIELDS = (
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
R304_SEED_A = 304_001
R304_SEED_B = 304_997
R304_ATTACK_MECHANISMS = (
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
R304_SCHEMA_SNAPSHOT = {
    "schema": "cm2.round304.schema-snapshot.v1",
    "candidate_files": dict(sorted(R304_FILES.items())),
    "tables": dict(sorted(R304_TABLES.items())),
    "id_fields": dict(sorted(R304_ID_FIELDS.items())),
    "row_schemas": dict(sorted(R304_ROW_SCHEMAS.items())),
    "ledger_schemas": dict(sorted(R304_LEDGER_SCHEMAS.items())),
    "exact_row_fields": {
        key: list(value)
        for key, value in sorted(R304_EXACT_ROW_FIELDS.items())
    },
    "exact_ledger_fields": {
        key: list(value)
        for key, value in sorted(R304_EXACT_LEDGER_FIELDS.items())
    },
    "exact_result_fields": list(R304_EXACT_RESULT_FIELDS),
    "result_schema": R304_RESULT_SCHEMA,
    "source_channel_order": [
        "R297_ORDINARY_FACE",
        "R296_TRUE_SEAM",
        "R299C_SIGNED_FACE",
        "R300B_COMPLETE_FACE",
        "R300C_POSITIVE_VOLUME",
        "R300E_HALF_OPEN_OWNER",
        "R300F_R245_HALF_OPEN_OWNER",
        "R303B_UNIFIED_ATTACHMENT",
    ],
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
    "attack_mechanisms": list(R304_ATTACK_MECHANISMS),
}
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
R301_RESULT = "cm2_round301_source_g_legal_component_dsu_application_result.json"
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
R300A_PAIR_COMMITMENT = {
    "row_count": 3_232,
    "row_ids_sha256": (
        "876617c3beda3cc50bcff712e6273786ba87a513d5422e875960353c6eb64332"
    ),
    "row_hashes_sha256": (
        "2f34355d24534220e6cf42e636925d0f5adf9d7430b61563f20f2d4d928faac4"
    ),
    "rows_sha256": (
        "7991da0c6f268cfb87628f1bee88f560ed319bec1028bee43e427c65ac8f6f16"
    ),
}

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
R266_MANIFEST = "cm2_round266_source_g_expanded_curved_face_closure_manifest.sha256"
R266_MANIFEST_SHA256 = (
    "63fb5b25d52ca5de579256499629d04d15f6a313e0a73f7e80fcb463385cbe09"
)
R294_REGISTRY = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_registry_ledger.json.gz"
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
R299A_MANIFEST = (
    "cm2_round299a_source_g_refined_occurrence_official_key_binding_closure_manifest.sha256"
)
R299A_MANIFEST_SHA256 = (
    "b1dfe718dd2b7477d9cc4067f1bade59d1589b3822eaf4b94b9dd721e61b468e"
)

R266_MEMBER_COMMITMENT = {
    "row_count": 259_752,
    "row_ids_sha256": "f064d177c25985b38c899c651923b83ba47ee36b465902cca85a4c21e0c33ca6",
    "row_hashes_sha256": "1f28c84d14cf3fabb38d0f2d1fdf862ce8f6a4559552d68fd9c0a5bd0a3ed3ee",
    "rows_sha256": "28398acde446047ff4a210b2fa0831d2c44e3758f7e9239b5ec63cecc386b257",
}
R266_ROOT_COMMITMENT = {
    "row_count": 63_224,
    "row_ids_sha256": "46889c11f7b1870bfe39faab0625054233c1c48b2cba2bd87cc9232b0405520a",
    "row_hashes_sha256": "a32bce700a94c39886a0d837e371e48562ae8380b71959e7326b0c4afef5e3b2",
    "rows_sha256": "bfdf5cde6fc68d39676e1543a6138672e7b8a68424280c6f895a8408f3eb579d",
}
R294_COMMITMENT = {
    "row_count": 431_208,
    "row_ids_sha256": "bbaca3ecbb804a87fd509aac2b8bd9f505d0c008e7bddbeb1a2ecb2a966f5509",
    "row_hashes_sha256": "ea98de3dab7e6f308f5a07d04bc29ca0d9dcd265a5323d8ecdb728cc501eed56",
    "rows_sha256": "33936ecd04cbce9f9a308b0da10381bd854b45028db53db5d3cbb9aa8b264044",
    "occurrence_ids_sha256": "169869b5755eda22f1527e7393a5bef0a77a842eefbdf45ab34d315b0dad1936",
}
R299A_COMMITMENT = {
    "row_count": 9_404,
    "row_ids_sha256": "a3786265b52feafd316cc81c71ab05ee32976b5ff7f1de091853d34a7b33e6e3",
    "row_hashes_sha256": "65e6f22b9085685b20a50dedfcb62cd08dd01e1ea70a61ee850d74450402b333",
    "rows_sha256": "6955fe1c36555c7aa492e4c5cfd1ab945fe16b824ea49bd3d72cea3bd3136c0f",
}

PRESERVED = "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE"
R288 = "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM"
R292 = "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT"


class PromotionBlocked(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise PromotionBlocked(label)


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
    INPUT_SNAPSHOTS.clear()
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


R304_SCHEMA_SNAPSHOT_SHA256 = digest(R304_SCHEMA_SNAPSHOT)


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
        label + " nonregular/hardlink/unbounded",
    )
    identity = file_identity(info)
    path = directory / name
    prior = snapshots.setdefault(path, identity)
    need(prior == identity, label + " PRE/POST snapshot mismatch")
    return identity


def inert_source_sha256(path: Path) -> str:
    need(
        os.path.lexists(path)
        and not path.is_symlink()
        and stat.S_ISREG(os.lstat(path).st_mode),
        "producer source pre-resolve boundary",
    )
    directory = path.parent
    snapshots: dict[Path, FileIdentity] = {}
    with fd_bound_binary(
        path,
        directory,
        snapshots,
        maximum=5_000_000,
        label="producer source",
    ) as stream:
        state = hashlib.sha256()
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    assert_snapshot_map(snapshots, "producer source")
    return state.hexdigest()


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


def safe_file(path: Path, maximum: int = 3_000_000_000) -> None:
    safe_regular(
        path,
        DATA,
        INPUT_SNAPSHOTS,
        maximum,
        "input:" + path.name,
    )


def assert_snapshot_map(
    snapshots: dict[Path, FileIdentity],
    label: str,
) -> None:
    for path, expected in sorted(snapshots.items(), key=lambda item: str(item[0])):
        need(os.path.lexists(path) and not path.is_symlink(), label + " disappeared")
        info = os.lstat(path)
        need(
            file_identity(info) == expected,
            label + " POST snapshot mismatch:" + path.name,
        )
    assert_parent_directory_snapshots(label)


def assert_input_snapshots_unchanged() -> None:
    assert_snapshot_map(INPUT_SNAPSHOTS, "input")


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


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with fd_bound_binary(
        path,
        DATA,
        INPUT_SNAPSHOTS,
        label="input hash:" + path.name,
    ) as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def stable_read_bytes(path: Path, maximum: int = 3_000_000_000) -> bytes:
    with fd_bound_binary(
        path,
        DATA,
        INPUT_SNAPSHOTS,
        maximum=maximum,
        label="input read:" + path.name,
    ) as stream:
        chunks: list[bytes] = []
        total = 0
        while True:
            block = stream.read(1 << 20)
            if not block:
                break
            total += len(block)
            need(total <= maximum, "bounded stable read:" + path.name)
            chunks.append(block)
        return b"".join(chunks)


def stable_local_bytes(
    path: Path,
    directory: Path,
    snapshots: dict[Path, FileIdentity],
    *,
    maximum: int,
    label: str,
) -> bytes:
    chunks: list[bytes] = []
    with fd_bound_binary(
        path,
        directory,
        snapshots,
        maximum=maximum,
        label=label,
    ) as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            chunks.append(block)
    return b"".join(chunks)


def strict_object(raw: bytes, label: str) -> dict[str, Any]:
    need(raw and not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw, label)

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in out, "duplicate JSON key:" + label + ":" + key)
            out[key] = value
        return out

    def reject(token: str) -> Any:
        raise PromotionBlocked(
            "nonintegral/nonfinite JSON:" + label + ":" + token
        )

    value = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=unique,
        parse_float=reject,
        parse_constant=reject,
    )
    need(type(value) is dict, "top-level object:" + label)
    return value


def read_json(name: str) -> dict[str, Any]:
    path = DATA / name
    return strict_object(stable_read_bytes(path), name)


def check_self(document: dict[str, Any], field: str, label: str) -> None:
    payload = dict(document)
    claimed = payload.pop(field, None)
    need(type(claimed) is str and claimed == digest(payload), "self hash:" + label)


def check_row(row: dict[str, Any], label: str) -> None:
    check_self(row, "row_sha256", label)


class ListHash:
    def __init__(self) -> None:
        self.state = hashlib.sha256(b"[")
        self.count = 0

    def add(self, value: Any) -> None:
        if self.count:
            self.state.update(b",")
        self.state.update(canonical(value))
        self.count += 1

    def finish(self) -> str:
        state = self.state.copy()
        state.update(b"]")
        return state.hexdigest()


def iter_array(stream: TextIO, marker: str, initial: str = "") -> Iterator[dict[str, Any]]:
    buffer = initial
    while marker not in buffer:
        block = stream.read(1 << 20)
        need(bool(block), "missing array:" + marker)
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
            PromotionBlocked("float:" + token)
        ),
        parse_constant=lambda token: (_ for _ in ()).throw(
            PromotionBlocked("constant:" + token)
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


def validated_gzip_rows(
    name: str,
    table: str,
    id_field: str,
    expected: dict[str, Any],
) -> Iterator[dict[str, Any]]:
    path = DATA / name
    rows, ids, hashes = ListHash(), ListHash(), ListHash()
    occurrences = ListHash() if "occurrence_ids_sha256" in expected else None
    seen: set[str] = set()
    with fd_bound_binary(
        path,
        DATA,
        INPUT_SNAPSHOTS,
        label="gzip source:" + name,
    ) as raw:
        with gzip.GzipFile(fileobj=raw, mode="rb") as binary:
            with io.TextIOWrapper(binary, encoding="utf-8", newline="") as stream:
                for row in iter_array(stream, '"' + table + '":['):
                    check_row(row, name)
                    row_id = row.get(id_field)
                    need(
                        type(row_id) is str and row_id not in seen,
                        "row id:" + name,
                    )
                    seen.add(row_id)
                    rows.add(row)
                    ids.add(row_id)
                    hashes.add(row["row_sha256"])
                    if occurrences is not None:
                        occurrences.add(row["registry_occurrence_id"])
                    yield row
    actual = {
        "row_count": rows.count,
        "row_ids_sha256": ids.finish(),
        "row_hashes_sha256": hashes.finish(),
        "rows_sha256": rows.finish(),
    }
    if occurrences is not None:
        actual["occurrence_ids_sha256"] = occurrences.finish()
    need(actual == expected, "ledger commitment:" + name)


def stream_plain_table(
    name: str,
    table: str,
    id_field: str,
    expected: dict[str, Any],
    visit: Callable[[dict[str, Any]], None],
) -> None:
    path = DATA / name
    marker = '"' + table + '":'
    carry = ""
    with fd_bound_binary(
        path,
        DATA,
        INPUT_SNAPSHOTS,
        label="plain source:" + name,
    ) as raw:
        stream = io.TextIOWrapper(raw, encoding="utf-8", newline="")
        try:
            while True:
                block = stream.read(1 << 20)
                need(bool(block), "missing table:" + table)
                combined = carry + block
                if marker in combined:
                    initial = combined.split(marker, 1)[1]
                    break
                carry = combined[-len(marker):]
            rows, ids, hashes = ListHash(), ListHash(), ListHash()
            seen: set[str] = set()
            for row in iter_array(stream, '"rows":[', initial):
                check_row(row, table)
                row_id = row.get(id_field)
                need(type(row_id) is str and row_id not in seen, "plain row id")
                seen.add(row_id)
                rows.add(row)
                ids.add(row_id)
                hashes.add(row["row_sha256"])
                visit(row)
        finally:
            stream.detach()
    need(
        {
            "row_count": rows.count,
            "row_ids_sha256": ids.finish(),
            "row_hashes_sha256": hashes.finish(),
            "rows_sha256": rows.finish(),
        }
        == expected,
        "plain commitment:" + table,
    )


def parse_manifest(name: str, expected_sha: str) -> dict[str, str]:
    path = DATA / name
    safe_file(path, 500_000)
    need(file_sha256(path) == expected_sha, "manifest pin:" + name)
    entries: dict[str, str] = {}
    raw = stable_read_bytes(path, 500_000)
    for line in raw.decode("ascii").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\n]+)", line)
        need(match is not None, "manifest syntax:" + name)
        value, member = match.groups()
        need(Path(member).name == member and member not in entries, "manifest set")
        entries[member] = value
    need(bool(entries), "empty manifest:" + name)
    return entries


def validate_entire_manifest(name: str, expected_sha: str) -> dict[str, str]:
    entries = parse_manifest(name, expected_sha)
    for member, expected in entries.items():
        path = DATA / member
        safe_file(path)
        need(file_sha256(path) == expected, "manifest member:" + name + ":" + member)
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


def validate_exact_manifest_pin_map(
    manifest_name: str,
    manifest_sha256: str,
    expected_pins: dict[str, str],
) -> dict[str, str]:
    entries = validate_entire_manifest(manifest_name, manifest_sha256)
    need(
        entries == dict(expected_pins),
        "exact manifest member/pin map:" + manifest_name,
    )
    return entries


def deterministic_gzip(document: dict[str, Any]) -> bytes:
    """Return one deterministic gzip member containing canonical JSON."""

    raw = canonical(document)
    output = io.BytesIO()
    with gzip.GzipFile(
        filename="",
        mode="wb",
        fileobj=output,
        mtime=0,
        compresslevel=9,
    ) as stream:
        stream.write(raw)
    return output.getvalue()


def build_generated_ledger(
    table: str,
    rows: Iterable[dict[str, Any]],
) -> tuple[bytes, dict[str, Any]]:
    materialized: list[dict[str, Any]] = []
    ids: list[str] = []
    hashes: list[str] = []
    seen: set[str] = set()
    id_field = R304_ID_FIELDS[table]
    for row in rows:
        validate_generated_row(table, row)
        row_id = row[id_field]
        need(row_id not in seen, "duplicate generated row id:" + table)
        seen.add(row_id)
        materialized.append(row)
        ids.append(row_id)
        hashes.append(row["row_sha256"])
    document = {
        "schema": R304_LEDGER_SCHEMAS[table],
        "status": "PASS_EXACT_DETERMINISTIC_LEDGER",
        "row_count": len(materialized),
        "row_ids_sha256": digest(ids),
        "row_hashes_sha256": digest(hashes),
        "rows_sha256": digest(materialized),
        R304_TABLES[table]: materialized,
    }
    need(
        set(document) == set(R304_EXACT_LEDGER_FIELDS[table]),
        "exact generated ledger fields:" + table,
    )
    raw = deterministic_gzip(document)
    return raw, {
        "filename": R304_FILES[table],
        "schema": R304_LEDGER_SCHEMAS[table],
        "row_count": len(materialized),
        "row_ids_sha256": document["row_ids_sha256"],
        "row_hashes_sha256": document["row_hashes_sha256"],
        "rows_sha256": document["rows_sha256"],
        "file_sha256": hashlib.sha256(raw).hexdigest(),
    }


def close_object(payload: dict[str, Any], field: str) -> dict[str, Any]:
    need(field not in payload, "preexisting closure field:" + field)
    output = dict(payload)
    output[field] = digest(payload)
    return output


def close_generated_row(
    *,
    table: str,
    context: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    id_field = R304_ID_FIELDS[table]
    need(payload.get("schema") == R304_ROW_SCHEMAS[table], "row schema:" + table)
    need(id_field not in payload and "row_sha256" not in payload, "preclosed row")
    row_id = "round304-" + table + ":" + digest([context, payload])
    return close_object({id_field: row_id, **payload}, "row_sha256")


def resolve_candidate_directory(candidate_dir: Path) -> Path:
    """Validate one explicit, nonsymlink candidate publication directory."""

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
    """Recover exact private stages left around an atomic no-replace move."""

    need(
        Path(os.path.abspath(os.fspath(output_dir)))
        == lexical_directory_without_symlinks(output_dir, "recovery output"),
        "recovery output directory boundary",
    )
    expected_names = set(artifacts)
    for stage_name in sorted(os.listdir(output_directory_descriptor)):
        if not stage_name.startswith(".r304-stage-"):
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
            "private recovery stage ownership/mode",
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
                "private recovery stage open race",
            )
            names = set(os.listdir(stage_descriptor))
            need(names <= expected_names, "private recovery stage subset")
            for name in sorted(names):
                read_recovery_stage_file(
                    stage_descriptor,
                    name,
                    artifacts[name],
                    "private recovery:" + name,
                )
                os.unlink(name, dir_fd=stage_descriptor)
            os.fsync(stage_descriptor)
        finally:
            os.close(stage_descriptor)
        os.rmdir(stage_name, dir_fd=output_directory_descriptor)
    os.fsync(output_directory_descriptor)


def publish_atomic_batch_no_clobber(
    output_dir: Path,
    artifacts: dict[str, bytes],
) -> None:
    """Serialize recovery/publication under an advisory directory lock."""

    resolved = resolve_candidate_directory(output_dir)
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
        "publication directory open race",
    )
    try:
        fcntl.flock(directory_descriptor, fcntl.LOCK_EX)
        recover_private_stage_orphans(
            output_dir,
            directory_descriptor,
            artifacts,
        )
        _publish_atomic_batch_no_clobber_locked(output_dir, artifacts)
    finally:
        need(
            bound_directory_identity
            == directory_identity(os.fstat(directory_descriptor))
            == directory_identity(os.lstat(resolved)),
            "publication directory renamed/swapped",
        )
        fcntl.flock(directory_descriptor, fcntl.LOCK_UN)
        os.close(directory_descriptor)


def _publish_atomic_batch_no_clobber_locked(
    output_dir: Path,
    artifacts: dict[str, bytes],
) -> None:
    """Atomically publish ledgers followed by the result commit marker.

    Every existing target must already contain the exact bytes.  An interrupted
    publication may be resumed from exact single-link ledgers, but the result is
    always atomically moved last.
    """

    resolved = resolve_candidate_directory(output_dir)
    expected_names = {
        value for key, value in R304_FILES.items() if key != "producer"
    }
    need(set(artifacts) == expected_names, "exact candidate artifact set")
    result_name = R304_FILES["result"]
    ordered_names = sorted(set(artifacts) - {result_name}) + [result_name]

    # Preflight the entire batch before publishing a single new name.
    output_snapshots: dict[Path, FileIdentity] = {}
    preexisting: dict[str, tuple[FileIdentity, str]] = {}
    for name in ordered_names:
        target = output_dir / name
        need(target.parent.resolve() == resolved, "candidate path escape")
        if os.path.lexists(target):
            actual = stable_local_bytes(
                target,
                output_dir,
                output_snapshots,
                maximum=max(1, len(artifacts[name])),
                label="preexisting candidate:" + name,
            )
            need(actual == artifacts[name], "no-clobber:" + name)
            preexisting[name] = (
                output_snapshots[target.resolve()],
                hashlib.sha256(actual).hexdigest(),
            )
    need(
        result_name not in preexisting
        or set(preexisting) == set(ordered_names),
        "result commit marker cannot preexist with a partial ledger batch",
    )

    with tempfile.TemporaryDirectory(
        prefix=".r304-stage-",
        dir=output_dir,
    ) as raw_stage:
        stage = Path(raw_stage)
        for name in ordered_names:
            path = stage / name
            flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
            descriptor = os.open(path, flags, 0o644)
            try:
                with os.fdopen(descriptor, "wb", closefd=True) as stream:
                    stream.write(artifacts[name])
                    stream.flush()
                    os.fsync(stream.fileno())
            except BaseException:
                try:
                    os.close(descriptor)
                except OSError:
                    pass
                raise
        stage_descriptor = os.open(
            stage,
            os.O_RDONLY
            | getattr(os, "O_DIRECTORY", 0)
            | getattr(os, "O_NOFOLLOW", 0)
            | getattr(os, "O_CLOEXEC", 0),
        )
        directory_descriptor = os.open(
            output_dir,
            os.O_RDONLY
            | getattr(os, "O_DIRECTORY", 0)
            | getattr(os, "O_NOFOLLOW", 0)
            | getattr(os, "O_CLOEXEC", 0),
        )
        try:
            for name in ordered_names:
                target = output_dir / name
                if name in preexisting:
                    actual = stable_local_bytes(
                        target,
                        output_dir,
                        output_snapshots,
                        maximum=max(1, len(artifacts[name])),
                        label="stable preexisting candidate:" + name,
                    )
                    need(
                        (
                            output_snapshots[target.resolve()],
                            hashlib.sha256(actual).hexdigest(),
                        )
                        == preexisting[name],
                        "preexisting target changed after preflight:" + name,
                    )
                    continue
                if name == result_name:
                    assert_input_snapshots_unchanged()
                try:
                    os.stat(
                        name,
                        dir_fd=directory_descriptor,
                        follow_symlinks=False,
                    )
                except FileNotFoundError:
                    pass
                else:
                    raise PromotionBlocked(
                        "target appeared after preflight:" + name
                    )
                try:
                    rename_noreplace(
                        stage_descriptor,
                        name,
                        directory_descriptor,
                        name,
                    )
                except FileExistsError as exc:
                    raise PromotionBlocked(
                        "target raced commit after preflight:" + name
                    ) from exc
            os.fsync(directory_descriptor)
        finally:
            os.close(stage_descriptor)
            os.close(directory_descriptor)
    # The staging directory has now been removed, so every newly published
    # target must again be a single-link regular file with exact bytes.
    for name in ordered_names:
        target = output_dir / name
        actual = stable_local_bytes(
            target,
            output_dir,
            output_snapshots,
            maximum=max(1, len(artifacts[name])),
            label="published candidate:" + name,
        )
        need(
            actual == artifacts[name],
            "post-publication exact target proof:" + name,
        )
    assert_snapshot_map(output_snapshots, "candidate output")
    assert_input_snapshots_unchanged()


@dataclass
class Member:
    member_id: str
    base_root: str
    official_key: str | None


@dataclass(frozen=True)
class Edge:
    channel: str
    source_id: str
    source_sha: str
    endpoints: tuple[str, str]
    roots: tuple[str, str]


@dataclass(frozen=True)
class Channel:
    name: str
    manifest: str
    manifest_sha: str
    ledger: str
    ledger_sha: str
    result: str
    verification: str
    count: int
    row_id: str
    endpoint: str
    commitment: dict[str, Any]
    required: tuple[tuple[str, Any], ...]


def channel(
    name: str,
    prefix: str,
    manifest_sha: str,
    ledger_suffix: str,
    ledger_sha: str,
    count: int,
    row_id: str,
    endpoint: str,
    commitment: tuple[str, str, str],
    required: tuple[tuple[str, Any], ...],
) -> Channel:
    return Channel(
        name=name,
        manifest=prefix + "_manifest.sha256",
        manifest_sha=manifest_sha,
        ledger=prefix + ledger_suffix,
        ledger_sha=ledger_sha,
        result=prefix + "_result.json",
        verification=prefix + "_verification.json",
        count=count,
        row_id=row_id,
        endpoint=endpoint,
        commitment={
            "row_count": count,
            "row_ids_sha256": commitment[0],
            "row_hashes_sha256": commitment[1],
            "rows_sha256": commitment[2],
        },
        required=required,
    )


OLD_CHANNELS = (
    channel(
        "R297_ORDINARY_FACE",
        "cm2_round297_source_g_ordinary_face_occurrence_edge_promotion",
        "1feecefa897c5320eadc006509ba6bde84cdbf692dfaddd024472b93c13c38c0",
        "_edge_ledger.json.gz",
        "18a20b4679a8a3e94ccaf1b511694220cad1bc92e1590ded4585ae3735547371",
        330_724,
        "Round297_ordinary_face_occurrence_edge_row_id",
        "exact_occurrence_endpoint_pair",
        (
            "6ee71aba6c26953b7b368dc89d985468fb7410e6d5a47b0300c2962ceca045a6",
            "02586985662d453791f1461d71c15cca7e5e109b25025a8eec5f5c7c441c937d",
            "52a6ee955af86ac186824c23d27c0372d3c14792839f372620d311c9f144dbe0",
        ),
        (
            ("formal_ordinary_component_edge_witness_credit", 1),
            ("occurrence_endpoint_pair_is_nonself", True),
            ("formal_occurrence_identity_collapse_credit", 0),
            ("formal_DSU_rank_reduction_credit", 0),
        ),
    ),
    channel(
        "R296_TRUE_SEAM",
        "cm2_round296_source_g_true_seam_occurrence_edge_ledger_closure",
        "f7786b9cdec45cb381ec46489eb44b0365b8ee43d81ae9a9611cb2dcdee7fb59",
        "_edge_ledger.json.gz",
        "1b57b10fac9317e1609fb8858972011165bd95e5b1b687604edd6c8ad7139ef7",
        48_444,
        "Round296_true_seam_occurrence_edge_row_id",
        "unordered_formal_occurrence_endpoint_pair",
        (
            "d6ad370122651272a384f4fc8f48ca8b3e6a6b3f2cd9c9f03a073c1d207f853a",
            "608bf8140bcb77b950f00628804c649e82ebdb1055816df2ae32f68b3e321a06",
            "e989828d774a08694404fe678c4ae74dc199f8f5cdf4d398dc755f5ff4b0561f",
        ),
        (
            ("formal_true_seam_edge_credit", 1),
            ("occurrence_identity_collapsed", False),
            ("formal_DSU_rank_reduction_credit", 0),
        ),
    ),
    channel(
        "R299C_SIGNED_FACE",
        "cm2_round299c_source_g_r292_signed_support_face_edge_promotion",
        "62e04cdd7f9c3d2fb865be0a999e1ce5ed1de435151a1b7bb5bba0176709b9b3",
        "_canonical_occurrence_edge_pairs.json.gz",
        "e63f164bf9cc559ec8d3a2895e66493933b43b90f1ad3b163dfb41e12bb04df1",
        25_452,
        "Round299C_canonical_signed_face_occurrence_edge_row_id",
        "unordered_formal_occurrence_endpoint_pair",
        (
            "56c09af202b36a867f1cc9893c968ab231a952fdea85cafdde999be4ebcba70d",
            "138395a9a63f16623f2df4ff3656d82c744a522de23f20fc728c925baa833dc6",
            "14c6f44ab989a075a46de4c842b14cad9dff211373b52d0be41c8083620c3c87",
        ),
        (
            ("formal_component_edge_credit", 1),
            ("formal_occurrence_identity_collapse_credit", 0),
            ("formal_DSU_rank_reduction_credit", 0),
        ),
    ),
    channel(
        "R300B_COMPLETE_FACE",
        "cm2_round300b_source_g_registry_boundary_and_complete_r275_face_inventory_closure",
        "6208c4bfd8b147f06ffb735d4b5621faff22585831b5f19d48e8125514ac4a6b",
        "_canonical_novel_occurrence_edge_pairs.json.gz",
        "c3d1e604ed0e1256789c239b65d22546035fd3bd333dd11bfb907e221c3cec9e",
        10_416,
        "Round300B_canonical_novel_occurrence_edge_row_id",
        "unordered_formal_occurrence_endpoint_pair",
        (
            "5b3c7f446db963d7b763ffebf5d596c1fda92e3d31e573fd3fd95b1c855b5119",
            "cbd960748bfed1d31e31cbad053c3a0c11d8264fe043e35fe85350c54bf8f648",
            "cbc1cf8de07559c50db2cd84920379c9e0bd839c22bf9be3267784adc801c808",
        ),
        (
            ("formal_component_edge_credit", 1),
            ("formal_occurrence_identity_collapse_credit", 0),
            ("formal_DSU_rank_reduction_credit", 0),
            ("all_prior_channel_memberships_false", True),
        ),
    ),
    channel(
        "R300C_POSITIVE_VOLUME",
        "cm2_round300c_source_g_virtual_stratum_new_occurrence_positive_volume_edge_promotion",
        "cd327de2702ac209b0b0a03d09b3744596a901c2d65794dd86231d31a0be3503",
        "_edge_ledger.json.gz",
        "8c9ed8b09e994a00ca3ca4906c35b454523383b7d488f66e7a082dbbd4b1fcec",
        6_314,
        "Round300C_virtual_occurrence_positive_volume_edge_row_id",
        "canonical_component_edge_endpoint_pair",
        (
            "f35b03655c3fb6986d4798b1b9a2858cba915d1279d393396315358ef0632c65",
            "2f4c62e37a58c457bdc22c3271bce1229acfda942f46ec38341a7fd693897efb",
            "41716c0e35152d8e735310a2efdb55cbe7cf5813c8f94dc0ee4f88525bcd0a5b",
        ),
        (
            ("formal_positive_volume_component_edge_witness_credit", 1),
            ("formal_occurrence_identity_collapse_credit", 0),
            ("formal_DSU_rank_reduction_credit", 0),
        ),
    ),
    channel(
        "R300E_HALF_OPEN_OWNER",
        "cm2_round300e_source_g_r248_half_open_owner_lower_component_edge_promotion",
        "4e6c4eec1af04a907285d41395aeef63e911b3b5486db91b33a95fa62e45177a",
        "_all_edge_ledger.json.gz",
        "4aa7ae76d984d15b345d5d6805ec4f06a47e30a46fff1315f346e81f1f17122f",
        12_992,
        "Round300E_half_open_owner_component_edge_row_id",
        "canonical_component_edge_endpoint_pair",
        (
            "d2a8a525bd593f1e9cedcd3306b84b87ba6ccc88a4878d18572c32dca43f2272",
            "de692835ee6333a65e554a4f1567186995b5d3c80adfd374227fc82e096fc4c7",
            "76bfbac5c9706416be4ed1e4df3104006dc26cb68cf5e8f23c5b482aa44ac20a",
        ),
        (
            ("formal_half_open_owner_component_edge_credit", 1),
            ("eligible_for_component_DSU_application", True),
            ("formal_occurrence_identity_collapse_credit", 0),
            ("formal_DSU_rank_reduction_credit", 0),
        ),
    ),
    channel(
        "R300F_R245_HALF_OPEN_OWNER",
        "cm2_round300f_source_g_r245_half_open_owner_sheet_attachment",
        "811656ed9160b622014a94901a1e08c7d3e6313db08f86d65ae01afefb49bbeb",
        "_ledger.json.gz",
        "1f958f9f3e3aff7327d897b39851f2d2d030d820e00859d302241702613cae1f",
        264,
        "Round300F_R245_half_open_owner_attachment_row_id",
        "canonical_component_edge_endpoint_pair",
        (
            "e836f0e338cd43b19cebc718fe5ba60d8e5a313bcf8aac9eea72b8bfc8246c22",
            "58fc944871aaba4d49708359d59a6c996953068cef3d59e7a1d3719179944180",
            "6be4a94b83fb5b1b61a93bf84ca2b61fb1f9dfd9cbf4425b5dbb6a0dcdc9f6c2",
        ),
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


class DSU:
    def __init__(self, roots: Iterable[str]) -> None:
        self.parent = {root: root for root in roots}
        self.size = {root: 1 for root in self.parent}

    def find(self, item: str) -> str:
        while self.parent[item] != item:
            self.parent[item] = self.parent[self.parent[item]]
            item = self.parent[item]
        return item

    def union(self, left: str, right: str) -> bool:
        a, b = self.find(left), self.find(right)
        if a == b:
            return False
        if (self.size[a], a) < (self.size[b], b):
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        return True


def reconstruct_members() -> tuple[dict[str, Member], set[str], dict[str, Any]]:
    validate_entire_manifest(R266_MANIFEST, R266_MANIFEST_SHA256)
    validate_entire_manifest(R294_MANIFEST, R294_MANIFEST_SHA256)
    validate_entire_manifest(R299A_MANIFEST, R299A_MANIFEST_SHA256)
    members: dict[str, Member] = {}
    retained: set[str] = set()

    def member_row(row: dict[str, Any]) -> None:
        member_id = row["component_member_id"]
        root = row["post_Round266_quotient_component_id"]
        need(member_id not in members, "duplicate Round266 member")
        need(row["member_identity_preserved"] is True, "Round266 identity")
        members[member_id] = Member(member_id, root, row["official_key_id"])
        retained.add(root)

    stream_plain_table(
        R266_CERTIFICATE,
        "formal_post_Round266_component_member_frontier_ledger",
        "post_Round266_component_member_frontier_row_id",
        R266_MEMBER_COMMITMENT,
        member_row,
    )
    root_keys: dict[str, str] = {}

    def root_row(row: dict[str, Any]) -> None:
        root = row["post_Round266_quotient_component_id"]
        need(root in retained and root not in root_keys, "Round266 root coverage")
        root_keys[root] = row["official_key_id"]

    stream_plain_table(
        R266_CERTIFICATE,
        "formal_post_Round266_component_frontier_ledger",
        "post_Round266_component_frontier_row_id",
        R266_ROOT_COMMITMENT,
        root_row,
    )
    need(len(members) == 259_752 and len(retained) == 63_224, "Round266 census")
    need(set(root_keys) == retained, "Round266 root exact set")
    need(
        all(member.official_key == root_keys[member.base_root] for member in members.values()),
        "Round266 key purity",
    )

    kinds: Counter[str] = Counter()
    preserved: set[str] = set()
    refined: dict[str, tuple[str, str]] = {}
    new_roots: set[str] = set()
    keys = set(root_keys.values())
    for row in validated_gzip_rows(
        R294_REGISTRY,
        "rows",
        "Round294_occurrence_registry_row_id",
        R294_COMMITMENT,
    ):
        occurrence = row["registry_occurrence_id"]
        kind = row["registry_entry_kind"]
        kinds[kind] += 1
        if kind == PRESERVED:
            need(occurrence in members and occurrence not in preserved, "preservation")
            need(members[occurrence].official_key == row["official_key_id"], "key")
            preserved.add(occurrence)
            continue
        need(occurrence not in members, "append-only identity")
        if kind == R288:
            key = row["official_key_id"]
            need(type(key) is str, "R288 key")
            keys.add(key)
        else:
            need(kind == R292 and row["official_key_id"] is None, "R292 unbound")
            key = None
            refined[occurrence] = (
                row["Round294_occurrence_registry_row_id"],
                row["row_sha256"],
            )
        members[occurrence] = Member(occurrence, occurrence, key)
        new_roots.add(occurrence)
    need(
        kinds == {PRESERVED: 126_468, R288: 295_336, R292: 9_404}
        and len(preserved) == 126_468
        and len(new_roots) == 304_740,
        "Round294 census",
    )

    bound: set[str] = set()
    for row in validated_gzip_rows(
        R299A_LEDGER,
        "rows",
        "Round299A_refined_occurrence_official_key_binding_row_id",
        R299A_COMMITMENT,
    ):
        occurrence = row["registry_occurrence_id"]
        source = refined.get(occurrence)
        member = members.get(occurrence)
        need(
            source is not None
            and member is not None
            and member.official_key is None
            and occurrence not in bound
            and row["source_Round294_occurrence_registry_row_id"] == source[0]
            and row["source_Round294_occurrence_registry_row_sha256"] == source[1]
            and row["append_only_official_key_binding"] is True
            and row["occurrence_identity_preserved"] is True,
            "Round299A binding",
        )
        member.official_key = row["official_key_id"]
        keys.add(row["official_key_id"])
        bound.add(occurrence)
    roots = retained | new_roots
    need(
        bound == set(refined)
        and len(members) == 564_492
        and len(roots) == 367_964
        and len(keys) == 124
        and all(member.official_key is not None for member in members.values()),
        "expanded universe",
    )
    return members, roots, {
        "member_count": len(members),
        "base_root_count": len(roots),
        "official_key_count": len(keys),
    }


def project(endpoint: str, members: dict[str, Member], roots: set[str]) -> str:
    if endpoint in roots:
        return endpoint
    member = members.get(endpoint)
    need(member is not None, "endpoint outside fresh member universe")
    return member.base_root


def collect_old_edges(
    members: dict[str, Member], roots: set[str]
) -> list[Edge]:
    output: list[Edge] = []
    for item in OLD_CHANNELS:
        entries = validate_entire_manifest(item.manifest, item.manifest_sha)
        need(entries.get(item.ledger) == item.ledger_sha, "ledger manifest pin")
        result = read_json(item.result)
        verification = read_json(item.verification)
        check_self(result, "result_sha256", item.result)
        check_self(verification, "verification_sha256", item.verification)
        need(
            result["status"].startswith("PASS")
            and verification["status"].startswith("PASS"),
            "sealed channel status:" + item.name,
        )
        before = len(output)
        for row in validated_gzip_rows(
            item.ledger, "rows", item.row_id, item.commitment
        ):
            for field, expected in item.required:
                need(row.get(field) == expected, item.name + ":" + field)
            pair = row[item.endpoint]
            need(
                type(pair) is list
                and len(pair) == 2
                and pair == sorted(pair)
                and pair[0] != pair[1],
                item.name + ":canonical pair",
            )
            output.append(
                Edge(
                    item.name,
                    row[item.row_id],
                    row["row_sha256"],
                    (pair[0], pair[1]),
                    (
                        project(pair[0], members, roots),
                        project(pair[1], members, roots),
                    ),
                )
            )
        need(len(output) - before == item.count, "channel count:" + item.name)
    need(len(output) == 434_606, "prior legal edge total")
    return output


def round303b_seal_ready() -> bool:
    values = (
        R303B_MANIFEST_SHA256,
        R303B_PRODUCER_SHA256,
        R303B_VERIFIER_SHA256,
        R303B_VERIFICATION_FILE_SHA256,
        R303B_VERIFICATION_OBJECT_SHA256,
        R303B_RESULT_SHA256,
        R303B_EDGE_LEDGER_SHA256,
        R303B_WTAIL_LEDGER_SHA256,
    )
    return (
        all(type(value) is str and PIN.fullmatch(value) for value in values)
        and exact_pin_map_ready(
            R303B_MANIFEST_MEMBER_PINS,
            R303B_EXPECTED_MANIFEST_MEMBERS,
        )
    )


def collect_round303b(
    members: dict[str, Member],
    roots: set[str],
    prior_map: dict[str, str],
) -> tuple[list[Edge], list[dict[str, Any]], dict[str, Any]]:
    need(round303b_seal_ready(), "R303B final manifest/verifier/verification pins absent")
    assert R303B_MANIFEST_SHA256 is not None
    assert R303B_MANIFEST_MEMBER_PINS is not None
    entries = validate_exact_manifest_pin_map(
        R303B["manifest"],
        R303B_MANIFEST_SHA256,
        R303B_MANIFEST_MEMBER_PINS,
    )
    for key in ("producer", "result", "verifier", "verification", "edge", "unresolved"):
        need(R303B[key] in entries, "R303B missing manifest member:" + key)
    need(entries[R303B["producer"]] == R303B_PRODUCER_SHA256, "R303B producer pin")
    need(entries[R303B["verifier"]] == R303B_VERIFIER_SHA256, "R303B verifier pin")
    need(
        entries[R303B["verification"]] == R303B_VERIFICATION_FILE_SHA256,
        "R303B verification file pin",
    )
    need(entries[R303B["result"]] == R303B_RESULT_SHA256, "R303B result pin")
    need(entries[R303B["edge"]] == R303B_EDGE_LEDGER_SHA256, "R303B edge pin")
    need(
        entries[R303B["unresolved"]] == R303B_WTAIL_LEDGER_SHA256,
        "R303B W-tail pin",
    )
    need(
        R303B_MANIFEST_MEMBER_PINS[R303B["producer"]]
        == R303B_PRODUCER_SHA256
        and R303B_MANIFEST_MEMBER_PINS[R303B["verifier"]]
        == R303B_VERIFIER_SHA256
        and R303B_MANIFEST_MEMBER_PINS[R303B["verification"]]
        == R303B_VERIFICATION_FILE_SHA256
        and R303B_MANIFEST_MEMBER_PINS[R303B["result"]]
        == R303B_RESULT_SHA256
        and R303B_MANIFEST_MEMBER_PINS[R303B["edge"]]
        == R303B_EDGE_LEDGER_SHA256
        and R303B_MANIFEST_MEMBER_PINS[R303B["unresolved"]]
        == R303B_WTAIL_LEDGER_SHA256,
        "R303B duplicated direct-pin slots disagree with exact manifest map",
    )
    result = read_json(R303B["result"])
    verification = read_json(R303B["verification"])
    check_self(result, "result_sha256", R303B["result"])
    check_self(verification, "verification_sha256", R303B["verification"])
    need(
        verification["verification_sha256"] == R303B_VERIFICATION_OBJECT_SHA256,
        "R303B verification object pin",
    )
    need(
        result["status"].startswith("PASS_ROUND303B_43912_B1_192_B2")
        and result["producer_sha256"] == R303B_PRODUCER_SHA256
        and result["complete_formal_run"] is True
        and result["provisional_Round303A_consumed"] is False
        and verification["status"] == "PASS_EXACT_CACHELESS_EXPECTED_STATE"
        and verification["verifier_sha256"] == R303B_VERIFIER_SHA256
        and verification["producer"] == {
            "filename": R303B["producer"],
            "inert_byte_pin_checked": True,
            "file_sha256": R303B_PRODUCER_SHA256,
            "imported_or_executed": False,
        }
        and verification["all_five_ledgers_and_result_exact"] is True
        and verification["candidate_opened_only_after_full_expected_state"]
        is True
        and verification["attack_suite"]["attack_count"] == 55
        and verification["attack_suite"]["rejected_count"] == 55,
        "R303B formal independent seal",
    )
    need(
        verification["candidate_exact_file_pins"]
        == verification["independently_rebuilt_expected_file_pins"]
        == {
            R303B[key]: entries[R303B[key]]
            for key in (
                "producer",
                "b1",
                "b2a",
                "b2b",
                "edge",
                "unresolved",
                "result",
            )
        },
        "R303B exact cacheless six-file equality",
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
        and admission["direct_Round287_union_issuance_count_rejected"]
        == 10_020
        and admission["binding_rows_issuing_occurrence_ID_count"] == 0
        and admission["admission_checked_before_Round294_consumption"]
        is True
        and admission["bypass_permitted"] is False,
        "R303B Round294B admission",
    )

    edge_meta = result["output_ledgers"]["edge"]
    unresolved_meta = result["output_ledgers"]["unresolved"]
    need(
        edge_meta["filename"] == R303B["edge"]
        and edge_meta["row_count"] == 44_104
        and edge_meta["file_sha256"] == R303B_EDGE_LEDGER_SHA256
        and unresolved_meta["filename"] == R303B["unresolved"]
        and unresolved_meta["row_count"] == 4
        and unresolved_meta["file_sha256"] == R303B_WTAIL_LEDGER_SHA256,
        "R303B result output census",
    )
    edges: list[Edge] = []
    edge_sources: set[str] = set()
    all_pairs: set[tuple[str, str]] = set()
    all_endpoints: set[str] = set()
    for row in validated_gzip_rows(
        R303B["edge"],
        "component_connectivity_edge_rows",
        "Round303B_component_connectivity_edge_row_id",
        {
            "row_count": edge_meta["row_count"],
            "row_ids_sha256": edge_meta["row_ids_sha256"],
            "row_hashes_sha256": edge_meta["row_hashes_sha256"],
            "rows_sha256": edge_meta["rows_sha256"],
        },
    ):
        pair = row["canonical_unordered_registry_occurrence_ids"]
        need(
            type(pair) is list
            and len(pair) == 2
            and pair == sorted(pair)
            and pair[0] != pair[1],
            "R303B edge pair",
        )
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
        need(all(row.get(field) is True for field in required_true), "R303B theorem/eligibility")
        need(
            row["formal_component_edge_credit"] == 1
            and row["formal_DSU_rank_reduction_credit"] == 0
            and row["formal_occurrence_identity_collapse_credit"] == 0
            and row["formal_official_key_merge_credit"] == 0
            and row["Round301_DSU_mutated_here"] is False
            and row["old_63224_component_result_reused"] is False,
            "R303B credit boundary",
        )
        roots_pair = (
            project(pair[0], members, roots),
            project(pair[1], members, roots),
        )
        need(
            prior_map[roots_pair[0]] != prior_map[roots_pair[1]],
            "R303B edge must be cross independently rebuilt prior partition",
        )
        need(
            row["Round301_pre_edge_components"]
            == {
                pair[0]: prior_map[roots_pair[0]],
                pair[1]: prior_map[roots_pair[1]],
            },
            "R303B exact independently rebuilt pre-edge components",
        )
        need(
            row["official_key_metadata"]
            == {
                pair[0]: members[pair[0]].official_key,
                pair[1]: members[pair[1]].official_key,
            },
            "R303B exact endpoint official keys",
        )
        need(
            all(row.get(field) == 0 for field in R303B_ZERO_FIELDS),
            "R303B every downstream field zero before fresh DSU",
        )
        source = row["source_Round300D_row_id"]
        need(source not in edge_sources, "duplicate R303B source")
        edge_sources.add(source)
        pair_key = (pair[0], pair[1])
        need(pair_key not in all_pairs, "duplicate R303B pair")
        all_pairs.add(pair_key)
        need(not all_endpoints.intersection(pair), "R303B endpoint reuse")
        all_endpoints.update(pair)
        edges.append(
            Edge(
                "R303B_UNIFIED_ATTACHMENT",
                row["Round303B_component_connectivity_edge_row_id"],
                row["row_sha256"],
                pair_key,
                roots_pair,
            )
        )

    unresolved: list[dict[str, Any]] = []
    unresolved_sources: set[str] = set()
    for row in validated_gzip_rows(
        R303B["unresolved"],
        "W_tail_unresolved_rows",
        "Round303B_W_tail_unresolved_row_id",
        {
            "row_count": unresolved_meta["row_count"],
            "row_ids_sha256": unresolved_meta["row_ids_sha256"],
            "row_hashes_sha256": unresolved_meta["row_hashes_sha256"],
            "rows_sha256": unresolved_meta["rows_sha256"],
        },
    ):
        pair = row["canonical_unordered_registry_occurrence_ids"]
        need(
            type(pair) is list
            and len(pair) == 2
            and pair == sorted(pair)
            and pair[0] != pair[1],
            "W-tail pair",
        )
        need(
            row["disposition"]
            == "UNRESOLVED__ROUND271_W_TAIL_CONNECTED_SIDE_EXTENSION_MISSING"
            and row["eligible_for_later_fresh_DSU_application"] is False
            and row["formal_component_edge_credit"] == 0
            and row["nonedge_credit"] == 0
            and row["exclusion_credit"] == 0
            and row["formal_DSU_rank_reduction_credit"] == 0,
            "W-tail zero-credit boundary",
        )
        need(
            all(row.get(field) == 0 for field in R303B_ZERO_FIELDS),
            "W-tail every downstream field zero",
        )
        roots_pair = (
            project(pair[0], members, roots),
            project(pair[1], members, roots),
        )
        need(
            prior_map[roots_pair[0]] != prior_map[roots_pair[1]],
            "W-tail must be cross prior partition",
        )
        source = row["source_Round300D_row_id"]
        need(
            source not in edge_sources and source not in unresolved_sources,
            "edge/W-tail source disjointness",
        )
        unresolved_sources.add(source)
        pair_key = (pair[0], pair[1])
        need(pair_key not in all_pairs, "edge/W-tail pair disjointness")
        all_pairs.add(pair_key)
        need(not all_endpoints.intersection(pair), "R303B endpoint reuse")
        all_endpoints.update(pair)
        unresolved.append(
            {
                "row_id": row["Round303B_W_tail_unresolved_row_id"],
                "row_sha256": row["row_sha256"],
                "source_Round300D_row_id": source,
                "endpoints": pair_key,
                "roots": roots_pair,
            }
        )
    need(
        len(edges) == 44_104
        and len(unresolved) == 4
        and len(edge_sources | unresolved_sources) == 44_108
        and len(all_pairs) == 44_108
        and len(all_endpoints) == 88_216,
        "complete R303B partition",
    )
    return edges, unresolved, {
        "edge_count": len(edges),
        "W_tail_count": len(unresolved),
        "distinct_endpoint_count": len(all_endpoints),
    }


def canonical_partition(
    dsu: DSU,
    roots: set[str],
    component_namespace: str,
) -> tuple[dict[str, str], str]:
    groups: dict[str, list[str]] = defaultdict(list)
    for root in sorted(roots):
        groups[dsu.find(root)].append(root)
    sets = sorted(sorted(group) for group in groups.values())
    mapping = {
        root: component_namespace + digest(group)
        for group in sets
        for root in group
    }
    return mapping, digest(sets)


def apply_edges(
    roots: set[str],
    edges: Iterable[Edge],
    witness_forest: bool = False,
    component_namespace: str = "round304-fresh-legal-component:",
) -> tuple[dict[str, str], dict[str, Any], dict[str, list[tuple[str, Edge]]]]:
    dsu = DSU(roots)
    rank = 0
    count = 0
    adjacency: dict[str, list[tuple[str, Edge]]] = defaultdict(list)
    channel_rank: Counter[str] = Counter()
    for edge in edges:
        count += 1
        if dsu.union(*edge.roots):
            rank += 1
            channel_rank[edge.channel] += 1
            if witness_forest:
                left, right = edge.roots
                adjacency[left].append((right, edge))
                adjacency[right].append((left, edge))
    mapping, partition_sha = canonical_partition(
        dsu,
        roots,
        component_namespace,
    )
    components = len(set(mapping.values()))
    need(rank == len(roots) - components, "rank-nullity")
    return mapping, {
        "edge_rows": count,
        "rank_reduction": rank,
        "component_count": components,
        "partition_sha256": partition_sha,
        "per_channel_rank_reduction": dict(sorted(channel_rank.items())),
    }, adjacency


def witness_path(
    start: str,
    target: str,
    adjacency: dict[str, list[tuple[str, Edge]]],
) -> list[dict[str, str]]:
    queue = deque([start])
    prior: dict[str, tuple[str, Edge] | None] = {start: None}
    while queue and target not in prior:
        node = queue.popleft()
        for neighbor, edge in sorted(
            adjacency.get(node, []),
            key=lambda entry: (entry[0], entry[1].channel, entry[1].source_id),
        ):
            if neighbor not in prior:
                prior[neighbor] = (node, edge)
                queue.append(neighbor)
    need(target in prior, "missing stronger legal path")
    path: list[dict[str, str]] = []
    cursor = target
    while cursor != start:
        previous = prior[cursor]
        assert previous is not None
        node, edge = previous
        path.append(
            {
                "channel": edge.channel,
                "source_row_id": edge.source_id,
                "source_row_sha256": edge.source_sha,
                "from_root": node,
                "to_root": cursor,
            }
        )
        cursor = node
    path.reverse()
    return path


def validate_generated_row(table: str, row: dict[str, Any]) -> None:
    need(
        set(row) == set(R304_EXACT_ROW_FIELDS[table]),
        "exact generated row fields:" + table,
    )
    need(row["schema"] == R304_ROW_SCHEMAS[table], "generated row schema:" + table)
    check_row(row, "generated:" + table)


def iter_edge_application_rows(
    roots: set[str],
    edges: Iterable[Edge],
) -> Iterator[dict[str, Any]]:
    """Replay forward application from a newly initialized empty DSU."""

    dsu = DSU(roots)
    for index, edge in enumerate(edges):
        reduced = dsu.union(*edge.roots)
        payload = {
            "schema": R304_ROW_SCHEMAS["edge"],
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
        row = close_generated_row(
            table="edge",
            context=digest([
                "ROUND304_FRESH_DSU_FORWARD_APPLICATION_V1",
                index,
                edge.channel,
                edge.source_id,
                edge.source_sha,
            ]),
            payload=payload,
        )
        validate_generated_row("edge", row)
        yield row


def iter_member_component_rows(
    members: dict[str, Member],
    final_map: dict[str, str],
) -> Iterator[dict[str, Any]]:
    for member_id in sorted(members):
        member = members[member_id]
        need(type(member.official_key) is str, "unkeyed generated member")
        payload = {
            "schema": R304_ROW_SCHEMAS["member"],
            "registry_occurrence_id": member.member_id,
            "base_root_id": member.base_root,
            "official_key_id": member.official_key,
            "final_component_id": final_map[member.base_root],
            "member_identity_preserved": True,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
        }
        row = close_generated_row(
            table="member",
            context=digest([
                "ROUND304_FRESH_MEMBER_COMPONENT_V1",
                member.member_id,
                member.base_root,
            ]),
            payload=payload,
        )
        validate_generated_row("member", row)
        yield row


def iter_W_tail_disposition_rows(
    unresolved: Iterable[dict[str, Any]],
    final_map: dict[str, str],
    forest: dict[str, list[tuple[str, Edge]]],
) -> Iterator[dict[str, Any]]:
    for item in sorted(unresolved, key=lambda row: row["row_id"]):
        left, right = item["roots"]
        same = final_map[left] == final_map[right]
        stronger_path = witness_path(left, right, forest) if same else []
        need(bool(stronger_path) == same, "W-tail stronger-path iff same component")
        payload = {
            "schema": R304_ROW_SCHEMAS["wtail"],
            "source_W_tail_row_id": item["row_id"],
            "source_W_tail_row_sha256": item["row_sha256"],
            "source_Round300D_row_id": item["source_Round300D_row_id"],
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
        row = close_generated_row(
            table="wtail",
            context=digest([
                "ROUND304_WTAIL_STRONGER_PATH_DISPOSITION_V1",
                item["row_id"],
                item["row_sha256"],
            ]),
            payload=payload,
        )
        validate_generated_row("wtail", row)
        yield row


def iter_residual_gate_rows() -> Iterator[dict[str, Any]]:
    payload = {
        "schema": R304_ROW_SCHEMAS["residual"],
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
    row = close_generated_row(
        table="residual",
        context="ROUND304_POST_DSU_RESIDUAL_GATE_V1",
        payload=payload,
    )
    validate_generated_row("residual", row)
    yield row


def validate_admission_and_historical_seals() -> None:
    validate_entire_manifest(R294B_MANIFEST, R294B_MANIFEST_SHA256)
    verification_path = DATA / R294B_VERIFICATION
    need(
        file_sha256(verification_path) == R294B_VERIFICATION_FILE_SHA256,
        "Round294B verification file",
    )
    verification = read_json(R294B_VERIFICATION)
    check_self(verification, "verification_sha256", R294B_VERIFICATION)
    need(
        verification["verification_sha256"] == R294B_VERIFICATION_OBJECT_SHA256
        and verification["status"].startswith("PASS_INDEPENDENT_ROUND294B")
        and verification["independent_registry_census"][
            "formal_occurrence_registry_row_count"
        ]
        == 431_208
        and verification["independent_registry_census"][
            "formal_representation_binding_count"
        ]
        == 46_288
        and verification["independent_registry_census"][
            "direct_Round287_union_issuance_count_rejected"
        ]
        == 10_020,
        "Round294B admission semantics",
    )
    validate_entire_manifest(R301_MANIFEST, R301_MANIFEST_SHA256)
    validate_entire_manifest(R303A_MANIFEST, R303A_MANIFEST_SHA256)
    r300a_entries = validate_entire_manifest(
        R300A_MANIFEST,
        R300A_MANIFEST_SHA256,
    )
    need(
        r300a_entries.get(R300A_LEDGER) == R300A_LEDGER_SHA256
        and r300a_entries.get(R300A_RESULT) == R300A_RESULT_SHA256,
        "Round300A exact ledger/result manifest pins",
    )


def validate_source_G_disposition_denominator() -> dict[str, Any]:
    """Pin the 224,580-key envelope without upgrading its zero disposition.

    The Round169 object is a deficit survey.  It is useful here only to make
    the global denominator exact and to prevent the 124 registry keys from
    being conflated with the 224,580 source-G return-signature keys.
    """

    certificate_path = DATA / R169_CERTIFICATE
    verification_path = DATA / R169_VERIFICATION
    safe_file(certificate_path, 50_000_000)
    safe_file(verification_path, 20_000_000)
    need(
        file_sha256(certificate_path) == R169_CERTIFICATE_SHA256
        and file_sha256(verification_path) == R169_VERIFICATION_SHA256,
        "Round169 exact file pins",
    )
    certificate = read_json(R169_CERTIFICATE)
    verification = read_json(R169_VERIFICATION)
    result = certificate.get("result")
    verification_result = verification.get("result")
    need(
        type(result) is dict
        and type(verification_result) is dict
        and certificate.get("result_sha256") == digest(result)
        and verification.get("result_sha256") == digest(verification_result),
        "Round169 wrapper closures",
    )
    census = result.get("source_G_exact_key_coverage_census")
    need(
        result.get("status")
        == (
            "CERTIFIED_SOURCE_G_EXACT_KEY_COVERAGE_DEFICIT_SURVEY__"
            "NO_EXTERIOR_OR_D02_PROMOTION"
        )
        and type(census) is dict
        and census.get("candidate_chart_target_pair_count") == 228
        and census.get("candidate_exact_key_envelope_count")
        == SOURCE_G_EXACT_KEY_DISPOSITION_DENOMINATOR
        and census.get("global_geometric_exact_key_disposition_count") == 0
        and census.get("keys_without_a_global_geometric_disposition_count")
        == SOURCE_G_EXACT_KEY_DISPOSITION_DENOMINATOR
        and verification_result.get("status") == "PASS"
        and verification_result.get(
            "source_G_224580_exact_key_deficit_census_recomputed"
        )
        is True,
        "Round169 exact zero-disposition denominator",
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


def reproject_R300A_frontier(
    members: dict[str, Member],
    roots: set[str],
    final_map: dict[str, str],
) -> dict[str, Any]:
    """Reproject every sealed R300A pair against the newly built quotient.

    This is a blocker census, not a physical-inclusion theorem.  A
    cross-component row remains unresolved regardless of any unsealed temp
    theorem about the currently observed 1,024-pair subset.
    """

    result_path = DATA / R300A_RESULT
    need(file_sha256(result_path) == R300A_RESULT_SHA256, "Round300A result pin")
    result = read_json(R300A_RESULT)
    check_self(result, "result_sha256", R300A_RESULT)
    need(
        result["status"]
        == (
            "PASS_ROUND300A_EXHAUSTIVE_FAIL_CLOSED_DIAGNOSTIC__"
            "NO_GRAPH_ZERO_COMPONENT_EDGE_PROMOTION"
        )
        and result["frontier_ledger"]["canonical_occurrence_pair_row_count"]
        == 3_232
        and result["prior_witness_partition"][
            "R295A_explicit_lower_graph_sheet_witness_pair_count"
        ]
        == 128
        and result["prior_witness_partition"]["unresolved_exact_pair_count"]
        == 3_104,
        "Round300A complete fail-closed frontier",
    )

    classifications: list[dict[str, Any]] = []
    histogram: Counter[str] = Counter()
    witnessed = 0
    unresolved = 0
    for row in validated_gzip_rows(
        R300A_LEDGER,
        "canonical_occurrence_pair_rows",
        "Round300A_canonical_occurrence_pair_row_id",
        R300A_PAIR_COMMITMENT,
    ):
        pair = row["canonical_unordered_Round294_registry_occurrence_ids"]
        need(
            type(pair) is list
            and len(pair) == 2
            and pair == sorted(pair)
            and pair[0] != pair[1]
            and row["left_Round294_registry_occurrence_id"] == pair[0]
            and row["right_Round294_registry_occurrence_id"] == pair[1]
            and row["formal_component_edge_credit"] == 0
            and row["formal_DSU_rank_reduction_credit"] == 0
            and row["formal_maximality_credit"] == 0,
            "Round300A pair boundary",
        )
        left_root = project(pair[0], members, roots)
        right_root = project(pair[1], members, roots)
        same = final_map[left_root] == final_map[right_root]
        prior_witness = row[
            "R295A_explicit_lower_graph_sheet_witness_present"
        ]
        need(type(prior_witness) is bool, "Round300A witness flag")
        witnessed += int(prior_witness)
        unresolved += int(not prior_witness)
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
        classifications.append(
            {
                "source_Round300A_row_id":
                    row["Round300A_canonical_occurrence_pair_row_id"],
                "source_Round300A_row_sha256": row["row_sha256"],
                "canonical_occurrence_pair": pair,
                "projected_base_root_pair": sorted([left_root, right_root]),
                "final_component_pair": sorted(
                    [final_map[left_root], final_map[right_root]]
                ),
                "prior_R295A_witness_present": prior_witness,
                "same_final_component": same,
                "post_Round304_disposition": disposition,
            }
        )
    need(
        len(classifications) == 3_232
        and witnessed == 128
        and unresolved == 3_104,
        "Round300A reprojection census",
    )
    inconsistent = histogram[
        "PRIOR_R295A_WITNESSED__CROSS_FINAL_COMPONENT_INCONSISTENCY"
    ]
    need(inconsistent == 0, "Round300A prior witnessed pair split")
    missing = histogram[
        (
            "UNWITNESSED__CROSS_COMPONENT__FORMAL_PHYSICAL_"
            "INCLUSION_PACKAGE_REQUIRED"
        )
    ]
    return {
        "complete_Round300A_pair_count": len(classifications),
        "prior_R295A_witnessed_pair_count": witnessed,
        "previously_unwitnessed_pair_count": unresolved,
        "post_Round304_disposition_histogram": dict(sorted(histogram.items())),
        "complete_reprojection_rows_sha256": digest(classifications),
        "cross_component_unwitnessed_pair_count": missing,
        "sealed_physical_inclusion_package_for_cross_pairs_present": False,
        "unsealed_temp_1024_theorem_consumed": False,
        "maximality_proved": False,
        "formal_maximality_credit": 0,
    }


def official_key_fibre_census(
    members: dict[str, Member],
    final_map: dict[str, str],
    maximality_gate: dict[str, Any],
) -> dict[str, Any]:
    """Enumerate the actual 124 registry fibres, without physical promotion."""

    by_key_members: Counter[str] = Counter()
    by_key_components: dict[str, set[str]] = defaultdict(set)
    for member in members.values():
        need(type(member.official_key) is str, "official key missing")
        by_key_members[member.official_key] += 1
        by_key_components[member.official_key].add(final_map[member.base_root])
    keys = sorted(by_key_members)
    rows = [
        {
            "official_key_id": key,
            "member_count": by_key_members[key],
            "final_component_count": len(by_key_components[key]),
            "final_component_ids_sha256": digest(
                sorted(by_key_components[key])
            ),
            "physical_fibre_maximality_available": False,
            "formal_fibre_credit": 0,
        }
        for key in keys
    ]
    need(
        len(keys) == ACTUAL_OFFICIAL_KEY_COUNT
        and sum(by_key_members.values()) == 564_492
        and STALE_OFFICIAL_KEY_COUNT != len(keys),
        "actual 124-key fibre census and stale-116 rejection",
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
                Counter(by_key_members.values()).items()
            )
        },
        "official_key_final_component_count_histogram": {
            str(component_count): frequency
            for component_count, frequency in sorted(
                Counter(
                    len(components)
                    for components in by_key_components.values()
                ).items()
            )
        },
        "maximality_dependency_satisfied":
            maximality_gate["maximality_proved"],
        "physical_official_key_fibre_exhaustion_proved": False,
        "formal_fibre_credit": 0,
    }


def audit_sealed_prior_only() -> dict[str, Any]:
    """Rebuild the pre-R303B universe and quotient without touching R303B.

    This is the only executable audit permitted while the Round303B package
    is unsealed.  It deliberately stops after the seven sealed old channels.
    """

    validate_admission_and_historical_seals()
    members, roots, universe = reconstruct_members()
    old_edges = collect_old_edges(members, roots)
    forward_map, forward, _ = apply_edges(
        roots,
        old_edges,
        component_namespace="round301-legal-component:",
    )
    reverse_map, reverse, _ = apply_edges(
        roots,
        reversed(old_edges),
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
        "sealed-prior fresh forward/reverse reconstruction",
    )
    assert_input_snapshots_unchanged()
    return {
        "schema": "cm2.round304.sealed-prior-only-audit.v1",
        "status": "PASS_SEALED_PRIOR_ONLY__R303B_NOT_OPENED",
        "universe": universe,
        "forward": forward,
        "reverse": reverse,
        "forward_reverse_same_partition": True,
        "Round301_partition_loaded_as_DSU_state": False,
        "Round303B_manifest_or_ledger_opened": False,
        "formal_Round304_artifact_written": False,
    }


def reconstruct(seed: int = R304_SEED_A) -> dict[str, Any]:
    need(type(seed) is int and 0 <= seed < 2**63, "seed contract")
    # The missing seal check deliberately precedes every candidate ledger open.
    need(round303b_seal_ready(), "BLOCKED: final sealed Round303B pins are absent")
    validate_admission_and_historical_seals()
    members, roots, universe = reconstruct_members()
    old_edges = collect_old_edges(members, roots)
    prior_map, prior, _ = apply_edges(
        roots,
        old_edges,
        component_namespace="round301-legal-component:",
    )
    need(
        prior["edge_rows"] == 434_606
        and prior["rank_reduction"] == 246_016
        and prior["component_count"] == 121_948
        and prior["partition_sha256"]
        == "c1ab6beed75d5e7379103975d6a9ac1b1095a3eb24b34c87288782e7c97cfe09",
        "fresh prior reconstruction differs from sealed Round301 census",
    )
    new_edges, unresolved, r303b_census = collect_round303b(
        members, roots, prior_map
    )
    all_edges = old_edges + new_edges
    forward_map, forward, forest = apply_edges(roots, all_edges, witness_forest=True)
    reverse_map, reverse, _ = apply_edges(roots, reversed(all_edges))
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
        "exact 29252/275268/92696 fresh forward/reverse outcome",
    )
    dispositions: list[dict[str, Any]] = []
    for row in unresolved:
        left, right = row["roots"]
        same = forward_map[left] == forward_map[right]
        dispositions.append(
            {
                "source_W_tail_row_id": row["row_id"],
                "source_W_tail_row_sha256": row["row_sha256"],
                "source_Round300D_row_id": row["source_Round300D_row_id"],
                "endpoint_pair": list(row["endpoints"]),
                "projected_root_pair": sorted([left, right]),
                "disposition": (
                    "RECLOSED_BY_STRONGER_LEGAL_DSU_PATH__ZERO_NEW_EDGE"
                    if same
                    else "STILL_CROSS_COMPONENT__WTAIL_EXTENSION_OR_OTHER_LEGAL_PATH_REQUIRED"
                ),
                "stronger_legal_path": witness_path(left, right, forest) if same else [],
                "formal_component_edge_credit": 0,
                "nonedge_credit": 0,
                "exclusion_credit": 0,
                "source_row_fed_to_DSU": False,
            }
        )
    need(
        len(dispositions) == 4
        and all(
            row["disposition"]
            == "RECLOSED_BY_STRONGER_LEGAL_DSU_PATH__ZERO_NEW_EDGE"
            and bool(row["stronger_legal_path"])
            for row in dispositions
        ),
        "exact 4-of-4 W-tail stronger-path reclosure",
    )
    maximality_gate = reproject_R300A_frontier(
        members,
        roots,
        forward_map,
    )
    fibre_gate = official_key_fibre_census(
        members,
        forward_map,
        maximality_gate,
    )
    source_G_denominator = validate_source_G_disposition_denominator()
    global_gate = {
        **source_G_denominator,
        "complete_global_half_open_join_ledger_present": False,
        "post_Round304_global_disposition_count": 0,
        "post_Round304_unresolved_global_disposition_count":
            SOURCE_G_EXACT_KEY_DISPOSITION_DENOMINATOR,
        "registry_official_key_count_is_not_the_global_denominator": True,
        "global_source_G_disposition_exhaustion_proved": False,
        "formal_global_disposition_credit": 0,
    }
    assert_input_snapshots_unchanged()
    return {
        "schema": (
            "cm2.round304.source-g-fresh-extended-registry-legal-component-"
            "dsu-rebuild.design-diagnostic.v1"
        ),
        "status": "DIAGNOSTIC_ONLY__NO_FORMAL_ARTIFACT_WRITTEN",
        "seed_affects_output": False,
        "schema_snapshot_sha256": R304_SCHEMA_SNAPSHOT_SHA256,
        "universe": universe,
        "prior_fresh_reconstruction": prior,
        "Round303B": r303b_census,
        "fresh_forward": forward,
        "fresh_reverse": reverse,
        "forward_reverse_same_partition": True,
        "derived_Round303B_incremental_rank_reduction":
            forward["rank_reduction"] - prior["rank_reduction"],
        "W_tail_dispositions": dispositions,
        "maximality_gate": maximality_gate,
        "official_key_fibre_gate": fibre_gate,
        "global_source_G_disposition_gate": global_gate,
        "hypothesis_checks": {
            "total_edge_rows_is_478710": forward["edge_rows"] == 478_710,
            "rank_reduction_is_275268": forward["rank_reduction"] == 275_268,
            "component_count_is_92696": forward["component_count"] == 92_696,
            "all_four_W_tail_reclosed_by_stronger_paths": all(
                row["disposition"].startswith("RECLOSED") for row in dispositions
            ),
        },
        "strict_zero_downstream_credit": {
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
            "Gate5_complete_18_field_block_count": 0,
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "forbidden_inputs_opened_as_DSU_state": {
            "old_63224_partition": False,
            "Round301_member_component_ledger": False,
            "Round301_edge_application_ledger": False,
            "conditional_92696_partition": False,
        },
    }


def build_candidate_artifacts(seed: int) -> tuple[dict[str, bytes], dict[str, Any]]:
    """Build the complete deterministic candidate artifact batch."""

    need(type(seed) is int and 0 <= seed < 2**63, "candidate seed contract")
    need(round303b_seal_ready(), "sealed Round303B required")
    validate_admission_and_historical_seals()
    members, roots, universe = reconstruct_members()
    old_edges = collect_old_edges(members, roots)
    prior_map, prior, _ = apply_edges(
        roots,
        old_edges,
        component_namespace="round301-legal-component:",
    )
    need(
        prior["edge_rows"] == 434_606
        and prior["rank_reduction"] == 246_016
        and prior["component_count"] == 121_948
        and prior["partition_sha256"]
        == "c1ab6beed75d5e7379103975d6a9ac1b1095a3eb24b34c87288782e7c97cfe09",
        "candidate fresh prior reconstruction",
    )
    r303b_edges, unresolved, r303b_census = collect_round303b(
        members,
        roots,
        prior_map,
    )
    all_edges = old_edges + r303b_edges
    forward_map, forward, forest = apply_edges(
        roots,
        all_edges,
        witness_forest=True,
    )
    reverse_map, reverse, _ = apply_edges(roots, reversed(all_edges))
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
        "candidate exact 29252/275268/92696 forward/reverse reconstruction",
    )

    maximality_gate = reproject_R300A_frontier(members, roots, forward_map)
    fibre_gate = official_key_fibre_census(
        members,
        forward_map,
        maximality_gate,
    )
    denominator = validate_source_G_disposition_denominator()
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
    edge_bytes, edge_meta = build_generated_ledger(
        "edge",
        iter_edge_application_rows(roots, all_edges),
    )
    artifacts[R304_FILES["edge"]] = edge_bytes
    output_ledgers["edge"] = edge_meta
    del edge_bytes
    member_bytes, member_meta = build_generated_ledger(
        "member",
        iter_member_component_rows(members, forward_map),
    )
    artifacts[R304_FILES["member"]] = member_bytes
    output_ledgers["member"] = member_meta
    del member_bytes
    wtail_rows = list(
        iter_W_tail_disposition_rows(unresolved, forward_map, forest)
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
        "candidate exact 4-of-4 W-tail stronger-path reclosure",
    )
    wtail_bytes, wtail_meta = build_generated_ledger("wtail", wtail_rows)
    artifacts[R304_FILES["wtail"]] = wtail_bytes
    output_ledgers["wtail"] = wtail_meta
    del wtail_bytes
    residual_rows = list(iter_residual_gate_rows())
    residual_bytes, residual_meta = build_generated_ledger(
        "residual",
        residual_rows,
    )
    artifacts[R304_FILES["residual"]] = residual_bytes
    output_ledgers["residual"] = residual_meta
    del residual_bytes
    assert_input_snapshots_unchanged()

    wtail_histogram = Counter(row["disposition"] for row in wtail_rows)
    wtail_same = sum(int(row["same_final_component"]) for row in wtail_rows)
    result_payload = {
        "schema": R304_RESULT_SCHEMA,
        "status": (
            "PASS_ROUND304_FRESH_EXTENDED_REGISTRY_LEGAL_DSU__"
            f"{forward['rank_reduction']}_RANK_REDUCTIONS__"
            f"{forward['component_count']}_COMPONENTS__"
            "ZERO_MAXIMALITY_FIBRE_GLOBAL_DISPOSITION_CREDIT"
        ),
        "producer_file_sha256": inert_source_sha256(Path(__file__)),
        "schema_snapshot_sha256": R304_SCHEMA_SNAPSHOT_SHA256,
        "seed_affects_output": False,
        "Round303B_seal": {
            "manifest_filename": R303B["manifest"],
            "manifest_file_sha256": R303B_MANIFEST_SHA256,
            "manifest_member_count": 12,
            "producer_file_sha256": R303B_PRODUCER_SHA256,
            "verifier_file_sha256": R303B_VERIFIER_SHA256,
            "verification_file_sha256": R303B_VERIFICATION_FILE_SHA256,
            "verification_object_sha256": R303B_VERIFICATION_OBJECT_SHA256,
            "result_file_sha256": R303B_RESULT_SHA256,
            "edge_ledger_file_sha256": R303B_EDGE_LEDGER_SHA256,
            "W_tail_ledger_file_sha256": R303B_WTAIL_LEDGER_SHA256,
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
            "Round303B_manifest": {R303B["manifest"]: R303B_MANIFEST_SHA256},
            "Round300A_manifest": {R300A_MANIFEST: R300A_MANIFEST_SHA256},
            "Round169_files": {
                R169_CERTIFICATE: R169_CERTIFICATE_SHA256,
                R169_VERIFICATION: R169_VERIFICATION_SHA256,
            },
        },
        "member_universe": {
            **universe,
            "actual_official_key_count": ACTUAL_OFFICIAL_KEY_COUNT,
            "stale_116_official_key_count_rejected": True,
            "unkeyed_member_count": 0,
        },
        "forward_application": {
            **forward,
            "prior_fresh_reconstruction": prior,
            "Round303B_incremental_rank_reduction":
                forward["rank_reduction"] - prior["rank_reduction"],
            "Round303B_census": r303b_census,
        },
        "reverse_application": reverse,
        "forward_reverse_same_partition": True,
        "W_tail_disposition_census": {
            "row_count": len(wtail_rows),
            "same_final_component_count": wtail_same,
            "cross_final_component_count": len(wtail_rows) - wtail_same,
            "disposition_histogram": dict(sorted(wtail_histogram.items())),
            "all_rows_excluded_from_DSU_input": True,
            "formal_component_edge_credit": 0,
        },
        "maximality_gate": maximality_gate,
        "official_key_fibre_gate": fibre_gate,
        "global_source_G_disposition_gate": global_gate,
        "residual_gate_census": {
            "R300A_cross_component_unwitnessed_pair_count":
                maximality_gate["cross_component_unwitnessed_pair_count"],
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
            "formal_post_Round304_component_count":
                forward["component_count"],
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
    need(
        json_object_keys_are_strings(result_payload),
        "result payload object keys must be strings",
    )
    result_payload_raw = canonical(result_payload)
    need(
        canonical(json.loads(result_payload_raw)) == result_payload_raw,
        "result payload parse-canonical byte replay",
    )
    result = close_object(result_payload, "result_sha256")
    need(
        set(result) == set(R304_EXACT_RESULT_FIELDS),
        "exact generated result fields",
    )
    result_bytes = canonical(result)
    replayed_result = json.loads(result_bytes)
    need(
        type(replayed_result) is dict
        and canonical(replayed_result) == result_bytes,
        "result parse-canonical byte replay",
    )
    replayed_result_sha256 = replayed_result.pop("result_sha256", None)
    need(
        type(replayed_result_sha256) is str
        and replayed_result_sha256 == digest(replayed_result),
        "result parse-canonical self-hash replay",
    )
    artifacts[R304_FILES["result"]] = result_bytes
    return artifacts, result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path)
    parser.add_argument("--print-contract", action="store_true")
    parser.add_argument("--print-attack-contract", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--audit-sealed-prior", action="store_true")
    parser.add_argument("--dual-seed", action="store_true")
    parser.add_argument("--candidate-dir", type=Path)
    parser.add_argument("--no-write", action="store_true")
    parser.add_argument("--seed", type=int, default=R304_SEED_A)
    args = parser.parse_args()
    if args.root is not None:
        configure_root(args.root)
    candidate_dir = args.candidate_dir
    if args.print_contract:
        print(
            json.dumps(
                {
                    "status": "FORMAL_READY__FULL_REBUILD_REQUIRED_FOR_OUTPUT",
                    "Round303B_seal_ready": round303b_seal_ready(),
                    "expected_member_count": 564_492,
                    "expected_base_root_count": 367_964,
                    "prior_edge_count": 434_606,
                    "future_Round303B_edge_count": 44_104,
                    "W_tail_row_count": 4,
                    "R303B_exact_manifest_member_count":
                        len(R303B_EXPECTED_MANIFEST_MEMBERS),
                    "schema_snapshot_sha256":
                        R304_SCHEMA_SNAPSHOT_SHA256,
                    "dual_seed_hooks": [R304_SEED_A, R304_SEED_B],
                    "publication_requires_explicit_candidate_dir": True,
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
                    "schema": "cm2.round304.attack-contract.v1",
                    "status": "DECLARED_FAIL_CLOSED_ATTACK_CONTRACT",
                    "mechanism_count": len(R304_ATTACK_MECHANISMS),
                    "mechanisms": list(R304_ATTACK_MECHANISMS),
                    "attack_credit": 0,
                },
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        return
    if args.self_test:
        good_pin_map = {
            name: "0" * 64 for name in R303B_EXPECTED_MANIFEST_MEMBERS
        }
        sample = {"schema": "self-test", "value": 1}
        print(
            json.dumps(
                {
                    "schema_snapshot_sha256":
                        R304_SCHEMA_SNAPSHOT_SHA256,
                    "exact_twelve_member_pin_map_contract":
                        exact_pin_map_ready(
                            good_pin_map,
                            R303B_EXPECTED_MANIFEST_MEMBERS,
                        ),
                    "missing_member_pin_map_rejected":
                        not exact_pin_map_ready(
                            {
                                name: value
                                for index, (name, value) in enumerate(
                                    sorted(good_pin_map.items())
                                )
                                if index
                            },
                            R303B_EXPECTED_MANIFEST_MEMBERS,
                        ),
                    "deterministic_single_member_gzip":
                        deterministic_gzip(sample)
                        == deterministic_gzip(sample),
                    "non_string_object_key_rejected_at_result_boundary":
                        not json_object_keys_are_strings(
                            {"histogram": {2: 1, 10: 1}}
                        ),
                    "Round303B_seal_ready": round303b_seal_ready(),
                    "Round303B_artifact_opened": False,
                    "formal_artifact_written": False,
                    "status": "PASS_FORMAL_READY_LOCAL_SELF_TEST",
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
    if args.dual_seed:
        need(
            (args.seed, R304_SEED_B) == (R304_SEED_A, R304_SEED_B),
            "dual-seed hook uses frozen seeds",
        )
        first = reconstruct(R304_SEED_A)
        second = reconstruct(R304_SEED_B)
        need(canonical(first) == canonical(second), "dual-seed byte divergence")
        print(canonical(first).decode("ascii"))
        return
    if args.no_write:
        need(candidate_dir is None, "--no-write conflicts with --candidate-dir")
        _, result = build_candidate_artifacts(args.seed)
        print(canonical(result).decode("ascii"))
        return
    if candidate_dir is not None:
        artifacts, result = build_candidate_artifacts(args.seed)
        publish_atomic_batch_no_clobber(candidate_dir, artifacts)
        print(canonical(result).decode("ascii"))
        return
    # A no-publication reconstruction summary remains available without a
    # candidate directory; it cannot create candidate artifacts.
    print(
        json.dumps(
            reconstruct(args.seed),
            sort_keys=True,
            separators=(",", ":"),
        )
    )


if __name__ == "__main__":
    main()
