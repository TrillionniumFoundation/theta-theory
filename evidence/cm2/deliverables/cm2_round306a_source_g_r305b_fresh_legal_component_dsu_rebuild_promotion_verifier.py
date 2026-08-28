#!/usr/bin/env python3
"""Independent verifier and promotion gate for Round306A.

The Round306A producer is never imported, executed, parsed, or tokenized here.
It is admitted only as one frozen byte string.  The mathematical reconstruction
uses the independently implemented, sealed Round304 promotion verifier as its
source-replay engine, then independently validates and lifts the eight sealed
Round305B component edges.  Candidate artifacts are opened only after all seven
expected candidate byte strings have been rebuilt in memory.

The final verification file is the sole Round306A credit commit marker.  Formal
publication is ordered attack-suite first, candidate ledgers/result next, and
verification last.  A zero residual on the 3,232-row Round300A frontier is not
promoted to full maximality: transformed-face, cross-chart, retained/event, and
occurrence-fibre exhaustion remain explicit blockers.
"""

from __future__ import annotations

import argparse
import copy
import ctypes
import errno
import fcntl
import gzip
import hashlib
import io
import json
import os
import stat
import sys
import tempfile
import types
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator


def discover_root(source: Path) -> Path:
    for candidate in (source.resolve().parent, *source.resolve().parents):
        if (candidate / "deliverables").is_dir() and (
            candidate / ".venv-cm2"
        ).is_dir():
            return candidate
    raise RuntimeError("workspace root not found")


ROOT = discover_root(Path(__file__))
DATA = ROOT / "deliverables"
PREFIX = "cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild"
SCHEMA = "cm2.round306a.source-g-r305b-fresh-legal-component-dsu-rebuild.v1"
PRODUCER = PREFIX + ".py"
VERIFIER = PREFIX + "_promotion_verifier.py"
ATTACK = PREFIX + "_attack_suite.json"
VERIFICATION = PREFIX + "_verification.json"
PRIVATE_CANDIDATE_ROOT = ROOT / ".cm2-round306a-private-candidates"

EXPECTED_PRODUCER_SHA256 = (
    "ab798332c82f7aa3656c61e3b31698a30b0fa1a83d24900432e076e445d6f5d5"
)
EXPECTED_PRODUCER_SCHEMA_SNAPSHOT_SHA256 = (
    "abfe46bd4ce053ec78af31a1e159dfe9325dac2da9952493058c86b891d1f2ae"
)
R304_VERIFIER = (
    "cm2_round304_source_g_fresh_extended_registry_legal_component_"
    "dsu_rebuild_promotion_verifier.py"
)
R304_VERIFIER_SHA256 = (
    "f605191b318b7d82106d8f7a872ea8101a59ffdf39999ad48fce9d44888d13fb"
)
R304_MANIFEST = (
    "cm2_round304_source_g_fresh_extended_registry_legal_component_"
    "dsu_rebuild_manifest.sha256"
)
R304_MANIFEST_SHA256 = (
    "de49f4233f6a22f43385e727071c5a5ebac68c35788dc2dd13e71d045639838c"
)
R304_PARTITION_SHA256 = (
    "72a745845f322255b95bfabb4b7254709e3f7c40359a0314e96b8e0d91c4bcff"
)
R304_MANIFEST_PINS = {
    "cm2_round304_source_g_fresh_extended_registry_legal_component_dsu_rebuild.py": "fff60d4a108355299ee6b9e3106549eca130ada2f4451d8f4deb50f0056520f5",
    "cm2_round304_source_g_fresh_extended_registry_legal_component_dsu_rebuild_edge_application_ledger.json.gz": "5018e0d9356596f7c679d2fa2ea4d84df9672a3e3d1a977faeae20edf61722fb",
    "cm2_round304_source_g_fresh_extended_registry_legal_component_dsu_rebuild_member_component_ledger.json.gz": "9a7e8c8a0ef810cfd6f29d99c0d2d6701b537ac76d1ab224dcbb60bec966dbd0",
    "cm2_round304_source_g_fresh_extended_registry_legal_component_dsu_rebuild_wtail_disposition_ledger.json.gz": "d7552fe4fd03de2bd45e1586500ac438d95c00288d085ad4e270890f0e93a934",
    "cm2_round304_source_g_fresh_extended_registry_legal_component_dsu_rebuild_residual_gate_ledger.json.gz": "665b61ce0f54d28106159b485cd39171590cd657a3a6d9b823762d1b42123d5f",
    "cm2_round304_source_g_fresh_extended_registry_legal_component_dsu_rebuild_result.json": "2975a8cc61c1b7812fedff6bc9dffd4db8517e822311c54a09317403b3592f7d",
    R304_VERIFIER: R304_VERIFIER_SHA256,
    "cm2_round304_source_g_fresh_extended_registry_legal_component_dsu_rebuild_attack_suite.json": "b14726d34e790a1a944778978260ca23173c3d4ab60c5580175262103bf283c8",
    "cm2_round304_source_g_fresh_extended_registry_legal_component_dsu_rebuild_verification.json": "482c1124cfd9d6daaa8c5d3af4f1a5023efb368946ff01718f73360bd3e558d3",
    "cm2_round304_source_g_fresh_extended_registry_legal_component_dsu_rebuild_report.md": "9a6e0832762e87be37e83d31801f84f68bab17c351603a0abee996318687187e",
    "cm2_round304_source_g_fresh_extended_registry_legal_component_dsu_rebuild_cold_replay.md": "217e0ef96fdc0229be3baab5f5b99c7b60daece3d2a0f71f7ddc89e5bd6ed9df",
}

R305B_PREFIX = (
    "cm2_round305b_source_g_r305a_two_sided_physical_inclusion_"
    "component_edge_promotion"
)
R305B_MANIFEST = R305B_PREFIX + "_manifest.sha256"
R305B_MANIFEST_SHA256 = (
    "1b80e7470e1ad1893f9323f47c64bd0d1aa48b35e0920c0821b25fe316b7dca7"
)
R305B_PHYSICAL = R305B_PREFIX + "_physical_witness_ledger.json.gz"
R305B_EDGE = R305B_PREFIX + "_canonical_component_edge_ledger.json.gz"
R305B_RESULT = R305B_PREFIX + "_result.json"
R305B_ATTACK = R305B_PREFIX + "_attack_suite.json"
R305B_VERIFICATION = R305B_PREFIX + "_verification.json"
R305B_MANIFEST_PINS = {
    R305B_PREFIX + ".py": "bf2c451b782b2e9ecf7fe9b6b2eaef50e06b9e5499b47579d815665fb8cd914b",
    R305B_PREFIX + "_wire_spec.json": "8cd6cbcd936875885b76fe501f76bf949e81233c07d75f715c003beb021ef573",
    R305B_PREFIX + "_wire_contract_fixture.json": "c2695472d522f1a24a2b8b7bbea0dff6e2c932b5dc63f154b27c6887b02e3f02",
    R305B_PHYSICAL: "629b8501e73c1e7bec9a9e21b1a27a4ca6021f9574c79caf83910ec25f3f95fb",
    R305B_PREFIX + "_anchor_ledger.json.gz": "491a696e582bce2c1fe57692e62caf461073812adec953a1bf46d8d7da2423df",
    R305B_PREFIX + "_closure_contact_ledger.json.gz": "19a25d6b462eb13522ed285cf447421410c5a4958642d59106c4cc1dcb58d0bd",
    R305B_PREFIX + "_owner_locus_ledger.json.gz": "9cf42df2be1994a5669c52732434a9823cef7c1532ea86175c8e8996b44ce690",
    R305B_EDGE: "cf56d9b57cd972a2a3272ea465f83f6fadbc3c7ed6962cb70809f19e44addb27",
    R305B_RESULT: "fcc18e0f0c2b05ca06c0c075521e50f00d5fe18bb1f39d853157f5c63cca3932",
    R305B_PREFIX + "_verifier.py": "39e2514d7617bd7e638cf2739dcc40bca3be356802654800499f5065bad29bf9",
    R305B_ATTACK: "b52c9c38ed262497769016602519fbf88f4601405f836c2bae2d7541a1af6735",
    R305B_VERIFICATION: "4b3307d480b56904a03b0820de65e283b57907da990b60dd6dac1de4e59f1dc9",
    R305B_PREFIX + "_report.md": "3e8ac390bd4c12a5609b0c4de9c6589d912517cda5ab6ddd772e0028cb3bedbb",
    R305B_PREFIX + "_cold_replay.md": "9b59bfce5e41f93eb87f90d629d499cd6da27245db5dfd1f13bbd90d7d6eeecf",
}

EXPECTED_PARTITION_SHA256 = (
    "a3f7ce1e28a956a46803ef466709ded0053633f5e104746c6d1e6e51b873e19c"
)
FILES = {
    "edge": PREFIX + "_edge_application_ledger.json.gz",
    "member": PREFIX + "_member_component_ledger.json.gz",
    "promoted": PREFIX + "_r305b_promoted_edge_application_ledger.json.gz",
    "frontier": PREFIX + "_r300a_reprojection_ledger.json.gz",
    "wtail": PREFIX + "_wtail_disposition_ledger.json.gz",
    "residual": PREFIX + "_residual_gate_ledger.json.gz",
    "result": PREFIX + "_result.json",
}
TABLES = {
    "edge": "fresh_edge_application_rows",
    "member": "fresh_member_component_rows",
    "promoted": "Round305B_promoted_edge_application_rows",
    "frontier": "Round300A_complete_reprojection_rows",
    "wtail": "W_tail_disposition_rows",
    "residual": "residual_gate_rows",
}
ID_FIELDS = {
    "edge": "Round306A_fresh_edge_application_row_id",
    "member": "Round306A_fresh_member_component_row_id",
    "promoted": "Round306A_Round305B_promoted_edge_application_row_id",
    "frontier": "Round306A_Round300A_reprojection_row_id",
    "wtail": "Round306A_W_tail_disposition_row_id",
    "residual": "Round306A_residual_gate_row_id",
}
R305B_PHYSICAL_FIELDS = {
    "Round305B_physical_witness_row_id", "schema",
    "source_Round305A_scope_reprojection_row_id",
    "source_Round305A_scope_reprojection_row_sha256",
    "source_Round300A_row_id", "source_Round300A_row_sha256",
    "canonical_registry_occurrence_pair", "Round304_final_component_pair",
    "official_key_pair", "cross_official_key_physical_edge_permitted",
    "occurrence_identity_collapsed", "official_key_identity_merged",
    "proof_core_patch_id", "owner_extension_patch_id",
    "active_function_id", "guard_id", "branch_id",
    "exact_relative_physical_domain", "exact_graph_Gamma",
    "anchor_row_ids", "anchor_row_sha256s", "closure_contact_row_ids",
    "closure_contact_row_sha256s", "owner_locus_row_ids",
    "owner_locus_row_sha256s",
    "owner_extension_sidecar_not_Gamma_core_or_attachment_or_edge_basis",
    "G0_exact_provenance_pins_and_row_closures",
    "G1_endpoint_occurrence_connected_supports",
    "G2_nonempty_connected_included_lower_stratum",
    "G3_left_closure_attaches_to_included_patch",
    "G4_right_closure_attaches_to_included_patch",
    "G5_endpoint_patch_provenance_exactly_closed",
    "relative_physical_closure_limit_lemma_id",
    "corridor_box_used_as_Gamma_intersection", "D4_transfer_used",
    "candidate_physical_connectivity_conclusion",
    "formal_physical_witness_credit", "formal_component_edge_credit",
    "formal_DSU_rank_reduction_credit", "formal_maximality_credit",
    "formal_fibre_credit", "formal_global_disposition_credit", "row_sha256",
}
R305B_EDGE_FIELDS = {
    "Round305B_canonical_component_edge_row_id", "schema",
    "canonical_Round304_final_component_pair", "physical_witness_row_count",
    "physical_witness_row_ids_sha256", "physical_witness_row_sha256s_sha256",
    "canonical_occurrence_pairs_sha256", "canonical_official_key_pair",
    "cross_official_key_physical_edge_permitted",
    "occurrence_identity_collapsed", "official_key_identity_merged",
    "all_128_witnesses_satisfy_G0_G5",
    "deduplicated_from_witness_rows_not_union_rows",
    "formal_component_edge_credit", "eligible_for_later_fresh_DSU_application",
    "formal_DSU_rank_reduction_credit", "row_sha256",
}
ROW_SCHEMAS = {
    key: SCHEMA + "." + suffix for key, suffix in {
        "edge": "fresh-edge-application-row.v1",
        "member": "fresh-member-component-row.v1",
        "promoted": "r305b-promoted-edge-application-row.v1",
        "frontier": "r300a-reprojection-row.v1",
        "wtail": "wtail-disposition-row.v1",
        "residual": "residual-gate-row.v1",
    }.items()
}
ROW_FIELDS = {
    "edge": {
        ID_FIELDS["edge"], "schema", "application_index", "source_channel",
        "source_row_id", "source_row_sha256",
        "canonical_occurrence_endpoint_pair", "projected_base_root_pair",
        "fed_to_new_empty_DSU", "forward_rank_reduction",
        "forward_cycle_or_redundant", "candidate_DSU_rank_reduction",
        "serialized_Round304_partition_used_as_state",
        "formal_credit_without_independent_verification_marker",
        "formal_maximality_credit", "formal_fibre_credit",
        "formal_global_disposition_credit", "row_sha256",
    },
    "member": {
        ID_FIELDS["member"], "schema", "registry_occurrence_id", "base_root_id",
        "official_key_id", "final_component_id", "member_identity_preserved",
        "formal_maximality_credit", "formal_fibre_credit",
        "formal_global_disposition_credit", "row_sha256",
    },
    "promoted": {
        ID_FIELDS["promoted"], "schema", "promoted_edge_index",
        "source_Round305B_component_edge_row_id",
        "source_Round305B_component_edge_row_sha256",
        "source_Round305B_selected_physical_witness_row_id",
        "source_Round305B_selected_physical_witness_row_sha256",
        "selection_rule", "Round304_fresh_checkpoint_component_pair",
        "selected_occurrence_pair", "projected_base_root_pair",
        "official_key_pair", "cross_checkpoint_components_before_application",
        "forward_rank_reduction", "witness_rows_are_not_union_rows",
        "formal_official_key_merge_credit",
        "formal_occurrence_identity_collapse_credit",
        "formal_credit_without_independent_verification_marker", "row_sha256",
    },
    "frontier": {
        ID_FIELDS["frontier"], "schema", "source_Round300A_row_id",
        "source_Round300A_row_sha256", "canonical_occurrence_pair",
        "projected_base_root_pair", "Round306A_final_component_pair",
        "same_Round306A_final_component", "prior_R295A_witness_present",
        "source_Round305B_physical_witness_row_id",
        "source_Round305B_physical_witness_row_sha256", "disposition",
        "Round300A_frontier_residual_credit", "formal_full_maximality_credit",
        "row_sha256",
    },
    "wtail": {
        ID_FIELDS["wtail"], "schema", "source_W_tail_row_id",
        "source_W_tail_row_sha256", "source_Round300D_row_id",
        "canonical_occurrence_endpoint_pair", "projected_base_root_pair",
        "Round306A_final_component_pair", "same_Round306A_final_component",
        "disposition", "stronger_legal_path", "source_row_fed_to_DSU",
        "formal_component_edge_credit", "formal_maximality_credit", "row_sha256",
    },
    "residual": {
        ID_FIELDS["residual"], "schema", "Round300A_complete_pair_count",
        "Round300A_cross_component_residual_count",
        "Round305B_physical_witness_rows_consumed_as_edge_provenance",
        "Round305B_canonical_component_edge_applications",
        "Round305B_rank_reductions", "transformed_face_exhaustion_proved",
        "cross_chart_exhaustion_proved", "retained_event_exhaustion_proved",
        "occurrence_fibre_exhaustion_proved", "full_maximality_proved",
        "formal_maximality_credit", "formal_fibre_credit",
        "formal_global_disposition_credit", "D02_status", "CM2_status",
        "row_sha256",
    },
}
LEDGER_FIELDS = {
    "schema", "schema_snapshot_sha256", "status", "row_count",
    "row_ids_sha256", "row_hashes_sha256", "rows_sha256", "ledger_sha256",
}
RESULT_FIELDS = {
    "schema", "schema_snapshot_sha256", "status", "producer_file_sha256",
    "frozen_Round304_engine", "Round305B_seal", "member_universe",
    "fresh_source_reconstruction_chain", "fresh_Round304_checkpoint",
    "fresh_forward_application", "fresh_reverse_application",
    "forward_reverse_same_partition", "Round305B_edge_application",
    "Round300A_reprojection", "full_maximality_gate",
    "formal_credit_without_independent_verification_marker",
    "candidate_credit_if_independently_verified", "output_ledgers",
    "seed_affects_output", "D02_status", "CM2_status", "result_sha256",
}
SCHEMA_SNAPSHOT = {
    "schema": SCHEMA + ".schema-snapshot.v1",
    "output_files": FILES,
    "tables": TABLES,
    "id_fields": ID_FIELDS,
    "row_schemas": ROW_SCHEMAS,
    "row_fields": {
        key: sorted(fields) for key, fields in sorted(ROW_FIELDS.items())
    },
    "ledger_fields_excluding_table": sorted(LEDGER_FIELDS),
    "result_fields": sorted(RESULT_FIELDS),
    "upstream_Round305B_physical_row_schema": (
        "cm2.round305b.source-g-r305a-two-sided-physical-inclusion-"
        "component-edge-promotion.v1.physical-witness-row.v1"
    ),
    "upstream_Round305B_physical_fields": sorted(R305B_PHYSICAL_FIELDS),
    "upstream_Round305B_edge_row_schema": (
        "cm2.round305b.source-g-r305a-two-sided-physical-inclusion-"
        "component-edge-promotion.v1.canonical-component-edge-row.v1"
    ),
    "upstream_Round305B_edge_fields": sorted(R305B_EDGE_FIELDS),
}
CANDIDATE_ORDER = tuple(FILES[key] for key in (
    "edge", "member", "promoted", "frontier", "wtail", "residual", "result"
))
PROMOTION_ORDER = (ATTACK, *CANDIDATE_ORDER, VERIFICATION)
ENCODER = json.JSONEncoder(
    ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":")
)


class VerificationBlocked(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if not value:
        raise VerificationBlocked(label)


def canonical(value: Any) -> bytes:
    return ENCODER.encode(value).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


SCHEMA_SNAPSHOT_SHA256 = digest(SCHEMA_SNAPSHOT)
need(
    SCHEMA_SNAPSHOT_SHA256 == EXPECTED_PRODUCER_SCHEMA_SNAPSHOT_SHA256,
    "exact frozen producer schema snapshot",
)


@dataclass(frozen=True)
class SealedSnapshot:
    device: int
    inode: int
    mode: int
    links: int
    size: int
    mtime_ns: int
    ctime_ns: int
    sha256: str


SEALED_SNAPSHOTS: dict[str, SealedSnapshot] = {}


def stable_data_file(
    name: str,
    *,
    maximum: int,
    expected_sha256: str | None = None,
    capture: bool = False,
) -> tuple[bytes | None, str]:
    need(
        Path(name).name == name and maximum >= 0,
        "stable data flat basename:" + name,
    )
    data_fd = os.open(
        DATA,
        os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        bound = os.fstat(data_fd)
        path_info = os.stat(DATA, follow_symlinks=False)
        need(
            stat.S_ISDIR(bound.st_mode)
            and not stat.S_ISLNK(path_info.st_mode)
            and (bound.st_dev, bound.st_ino) == (path_info.st_dev, path_info.st_ino),
            "stable deliverables directory:" + name,
        )
        descriptor = os.open(
            name,
            os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0),
            dir_fd=data_fd,
        )
        try:
            before = os.fstat(descriptor)
            directory_entry = os.stat(name, dir_fd=data_fd, follow_symlinks=False)
            need(
                stat.S_ISREG(before.st_mode)
                and not stat.S_ISLNK(directory_entry.st_mode)
                and before.st_nlink == 1
                and before.st_size <= maximum
                and (before.st_dev, before.st_ino)
                == (directory_entry.st_dev, directory_entry.st_ino),
                "stable regular bounded source:" + name,
            )
            hasher = hashlib.sha256()
            chunks: list[bytes] | None = [] if capture else None
            while block := os.read(descriptor, 1 << 20):
                hasher.update(block)
                if chunks is not None:
                    chunks.append(block)
            after = os.fstat(descriptor)
            identity_before = (
                before.st_dev, before.st_ino, before.st_mode, before.st_nlink,
                before.st_size, before.st_mtime_ns, before.st_ctime_ns,
            )
            identity_after = (
                after.st_dev, after.st_ino, after.st_mode, after.st_nlink,
                after.st_size, after.st_mtime_ns, after.st_ctime_ns,
            )
            need(identity_before == identity_after, "source changed during read:" + name)
            sha256 = hasher.hexdigest()
            snapshot = SealedSnapshot(*identity_after, sha256)
            previous = SEALED_SNAPSHOTS.get(name)
            need(previous is None or previous == snapshot, "source snapshot changed:" + name)
            SEALED_SNAPSHOTS[name] = snapshot
            need(
                expected_sha256 is None or sha256 == expected_sha256,
                "source exact byte pin:" + name,
            )
            return (b"".join(chunks) if chunks is not None else None), sha256
        finally:
            os.close(descriptor)
    finally:
        os.close(data_fd)


def stable_sha256(name: str, expected: str | None = None) -> str:
    _raw, actual = stable_data_file(
        name, maximum=5_000_000_000, expected_sha256=expected, capture=False
    )
    return actual


def stable_bytes(name: str, maximum: int, expected: str | None = None) -> bytes:
    raw, _actual = stable_data_file(
        name, maximum=maximum, expected_sha256=expected, capture=True
    )
    assert raw is not None
    return raw


def assert_sealed_snapshots(label: str) -> None:
    data_fd = os.open(
        DATA,
        os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        bound = os.fstat(data_fd)
        path_info = os.stat(DATA, follow_symlinks=False)
        need(
            (bound.st_dev, bound.st_ino) == (path_info.st_dev, path_info.st_ino),
            "deliverables snapshot directory:" + label,
        )
        for name, expected in SEALED_SNAPSHOTS.items():
            current = os.stat(name, dir_fd=data_fd, follow_symlinks=False)
            need(
                stat.S_ISREG(current.st_mode)
                and (
                    current.st_dev, current.st_ino, current.st_mode,
                    current.st_nlink, current.st_size, current.st_mtime_ns,
                    current.st_ctime_ns,
                )
                == (
                    expected.device, expected.inode, expected.mode,
                    expected.links, expected.size, expected.mtime_ns,
                    expected.ctime_ns,
                ),
                "sealed snapshot changed:" + label + ":" + name,
            )
    finally:
        os.close(data_fd)


def strict_object(raw: bytes, label: str) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in output, label + ":duplicate-key:" + key)
            output[key] = value
        return output

    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=unique,
            parse_float=lambda token: (_ for _ in ()).throw(
                VerificationBlocked(label + ":float:" + token)
            ),
            parse_constant=lambda token: (_ for _ in ()).throw(
                VerificationBlocked(label + ":constant:" + token)
            ),
        )
    except UnicodeDecodeError as exc:
        raise VerificationBlocked(label + ":utf8") from exc
    need(type(value) is dict, label + ":object")
    return value


def read_json(name: str) -> dict[str, Any]:
    return strict_object(stable_bytes(name, 1_000_000_000), name)


def verify_self(value: dict[str, Any], field: str, label: str) -> None:
    expected = value.get(field)
    need(type(expected) is str and len(expected) == 64, label + ":self-field")
    payload = dict(value)
    payload.pop(field)
    need(digest(payload) == expected, label + ":self-hash")


def parse_manifest(name: str, expected_sha: str) -> dict[str, str]:
    raw = stable_bytes(name, 2_000_000, expected_sha)
    entries: dict[str, str] = {}
    try:
        lines = raw.decode("ascii").splitlines()
    except UnicodeDecodeError as exc:
        raise VerificationBlocked(name + ":manifest-ascii") from exc
    for line in lines:
        pieces = line.split("  ", 1)
        need(len(pieces) == 2, name + ":line")
        pin, member = pieces
        need(
            len(pin) == 64
            and all(ch in "0123456789abcdef" for ch in pin)
            and Path(member).name == member
            and member not in entries,
            name + ":member",
        )
        entries[member] = pin
    return entries


def require_regular_pin(name: str, expected: str) -> None:
    stable_sha256(name, expected)


def validate_round304_engine_seal() -> None:
    entries = parse_manifest(R304_MANIFEST, R304_MANIFEST_SHA256)
    need(entries == R304_MANIFEST_PINS, "Round304 exact 11-member seal")
    for name, expected in entries.items():
        require_regular_pin(name, expected)
    need(
        entries[R304_VERIFIER] == R304_VERIFIER_SHA256,
        "Round304 promotion verifier is exact independent engine",
    )


def validate_round305b_seal() -> None:
    entries = parse_manifest(R305B_MANIFEST, R305B_MANIFEST_SHA256)
    need(entries == R305B_MANIFEST_PINS, "Round305B exact 14-member seal")
    for name, expected in entries.items():
        require_regular_pin(name, expected)
    verification = read_json(R305B_VERIFICATION)
    verify_self(verification, "verification_sha256", R305B_VERIFICATION)
    attack = read_json(R305B_ATTACK)
    verify_self(attack, "attack_suite_sha256", R305B_ATTACK)
    result = read_json(R305B_RESULT)
    verify_self(result, "result_sha256", R305B_RESULT)
    candidate_names = (
        R305B_PHYSICAL,
        R305B_PREFIX + "_anchor_ledger.json.gz",
        R305B_PREFIX + "_closure_contact_ledger.json.gz",
        R305B_PREFIX + "_owner_locus_ledger.json.gz",
        R305B_EDGE,
        R305B_RESULT,
    )
    exact_candidate_pins = {name: entries[name] for name in candidate_names}
    need(
        verification.get("status")
        == "PASS_EXACT_CACHELESS_ROUND305B_TWO_SIDED_PHYSICAL_INCLUSION_COMPONENT_EDGE_PROMOTION"
        and verification.get("formal_Round305B_promotion_permitted") is True
        and verification["candidate"]["exact_six_file_set"]
        == list(candidate_names)
        and verification["candidate"]["exact_file_sha256s"]
        == exact_candidate_pins
        and verification["candidate"][
            "all_six_files_equal_independently_rebuilt_bytes"
        ] is True
        and verification["attack_suite"]["attack_count"] == 99
        and verification["attack_suite"]["rejected_count"] == 99
        and verification["attack_suite"]["all_rejected"] is True
        and attack["attack_count"] == attack["rejected_count"] == 99
        and attack["all_rejected"] is True
        and attack["binding_mode"] == "EXACT_FORMAL_CANDIDATE"
        and attack["baseline_candidate_file_sha256s"]
        == exact_candidate_pins
        and verification["attack_suite"]["filename"] == R305B_ATTACK
        and verification["attack_suite"]["file_sha256"]
        == entries[R305B_ATTACK]
        == hashlib.sha256(canonical(attack)).hexdigest()
        and verification["attack_suite"]["object_self_sha256"]
        == attack["attack_suite_sha256"]
        and verification["atomic_publication_contract"][
            "attack_suite_is_first"
        ] is True
        and verification["atomic_publication_contract"][
            "verification_is_last_and_sole_formal_credit_commit_marker"
        ] is True,
        "Round305B content-bound independent admission marker",
    )
    need(
        verification["formal_credit_without_verification_commit_marker"]
        == {
            "formal_DSU_rank_reduction_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
            "formal_maximality_credit": 0,
            "officially_admitted_anchor_binding_credit": 0,
            "officially_admitted_component_edge_credit": 0,
            "officially_admitted_physical_witness_credit": 0,
        }
        and verification[
            "formal_credit_transition_at_this_verification_commit_marker"
        ]
        == {
            "formal_DSU_rank_reduction_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
            "formal_maximality_credit": 0,
            "officially_admitted_anchor_binding_credit": 2048,
            "officially_admitted_component_edge_credit": 8,
            "officially_admitted_physical_witness_credit": 1024,
        },
        "Round305B verification sole credit transition",
    )
    need(
        result["status"]
        == "PASS_ROUND305B_DIRECT_G0_G5_ZERO_CREDIT_CANDIDATE__PENDING_INDEPENDENT_VERIFICATION__ZERO_OFFICIALLY_ADMITTED_CREDIT",
        "Round305B candidate itself remained zero credit",
    )


def load_independent_engine() -> Any:
    validate_round304_engine_seal()
    path = DATA / R304_VERIFIER
    source = stable_bytes(R304_VERIFIER, 10_000_000, R304_VERIFIER_SHA256)
    module_name = "_round304_independent_verifier_engine"
    module = types.ModuleType(module_name)
    module.__file__ = str(path)
    module.__package__ = ""
    sys.modules[module_name] = module
    code = compile(source, str(path), "exec", dont_inherit=True, optimize=0)
    exec(code, module.__dict__)
    module.configure_root(ROOT)
    stable_sha256(R304_VERIFIER, R304_VERIFIER_SHA256)
    return module


def deterministic_gzip(document: dict[str, Any]) -> bytes:
    output = io.BytesIO()
    with gzip.GzipFile(
        filename="", mode="wb", fileobj=output, mtime=0, compresslevel=9
    ) as stream:
        stream.write(canonical(document))
    return output.getvalue()


def validate_closed_ledger(
    name: str, table: str, id_field: str, expected_count: int
) -> list[dict[str, Any]]:
    raw = stable_bytes(name, 100_000_000, R305B_MANIFEST_PINS[name])
    try:
        expanded = gzip.decompress(raw)
    except gzip.BadGzipFile as exc:
        raise VerificationBlocked(name + ":gzip") from exc
    document = strict_object(expanded, name)
    need(deterministic_gzip(document) == raw, name + ":deterministic-single-gzip")
    expected_schema = (
        "cm2.round305b.source-g-r305a-two-sided-physical-inclusion-"
        "component-edge-promotion.v1."
        + (
            "physical-witness-ledger.v1"
            if name == R305B_PHYSICAL
            else "canonical-component-edge-ledger.v1"
        )
    )
    need(
        set(document)
        == {
            "schema", "status", "every_row_closed_by_own_sha256",
            "formal_credit", "row_count", "row_ids_sha256",
            "row_hashes_sha256", "rows_sha256", "rows", "ledger_sha256",
        }
        and document.get("schema") == expected_schema
        and document.get("status")
        == (
            "PASS_ZERO_CREDIT_CANDIDATE_LEDGER__PUBLISHED_OR_STAGED__"
            "PENDING_INDEPENDENT_VERIFICATION"
        )
        and document.get("every_row_closed_by_own_sha256") is True
        and document.get("formal_credit") == 0,
        name + ":exact sealed ledger schema",
    )
    rows = document.get(table)
    need(type(rows) is list and len(rows) == expected_count, name + ":count")
    ids: list[str] = []
    hashes: list[str] = []
    seen: set[str] = set()
    for row in rows:
        need(type(row) is dict and type(row.get(id_field)) is str, name + ":row")
        verify_self(row, "row_sha256", name + ":row")
        need(row[id_field] not in seen, name + ":duplicate-row")
        seen.add(row[id_field])
        ids.append(row[id_field])
        hashes.append(row["row_sha256"])
    need(
        document.get("row_count") == expected_count
        and document.get("row_ids_sha256") == digest(ids)
        and document.get("row_hashes_sha256") == digest(hashes)
        and document.get("rows_sha256") == digest(rows),
        name + ":commitments",
    )
    if "ledger_sha256" in document:
        verify_self(document, "ledger_sha256", name + ":ledger")
    return rows


@dataclass(frozen=True)
class Lift:
    edge_row_id: str
    edge_row_sha256: str
    component_pair: tuple[str, str]
    witness_row_id: str
    witness_row_sha256: str
    occurrence_pair: tuple[str, str]
    root_pair: tuple[str, str]
    official_key_pair: tuple[str, str]


def build_round305b_lifts(
    engine: Any,
    member_root: dict[str, str],
    member_key: dict[str, str],
    root_index: dict[str, int],
    checkpoint_map: dict[str, str],
) -> tuple[list[Any], list[Lift], dict[str, dict[str, Any]]]:
    checkpoint_histogram: Counter[str] = Counter()
    checkpoint_cross: dict[str, dict[str, Any]] = {}
    all_r300a_ids: set[str] = set()
    for source in engine.gzip_rows(
        engine.R300A_LEDGER, "canonical_occurrence_pair_rows"
    ):
        engine.verify_self(source, "row_sha256", "Round306A checkpoint R300A")
        source_id = source.get("Round300A_canonical_occurrence_pair_row_id")
        pair = source.get("canonical_unordered_Round294_registry_occurrence_ids")
        prior = source.get("R295A_explicit_lower_graph_sheet_witness_present")
        need(
            type(source_id) is str
            and source_id not in all_r300a_ids
            and type(pair) is list
            and len(pair) == 2
            and pair == sorted(pair)
            and pair[0] != pair[1]
            and type(prior) is bool,
            "Round300A checkpoint source boundary",
        )
        all_r300a_ids.add(source_id)
        roots = tuple(
            engine.endpoint_root(item, member_root, root_index) for item in pair
        )
        component_pair = tuple(sorted(checkpoint_map[item] for item in roots))
        same = component_pair[0] == component_pair[1]
        classification = (
            "PRIOR_SAME" if prior and same else
            "PRIOR_CROSS" if prior else
            "UNPRIOR_SAME" if same else
            "UNPRIOR_CROSS"
        )
        checkpoint_histogram[classification] += 1
        if classification == "UNPRIOR_CROSS":
            checkpoint_cross[source_id] = {
                "row_sha256": source["row_sha256"],
                "occurrence_pair": pair,
                "root_pair": roots,
                "component_pair": component_pair,
                "official_key_pair": tuple(
                    sorted(member_key[item] for item in pair)
                ),
            }
    need(
        len(all_r300a_ids) == 3232
        and {
            key: checkpoint_histogram[key]
            for key in ("PRIOR_CROSS", "PRIOR_SAME", "UNPRIOR_CROSS", "UNPRIOR_SAME")
        }
        == {
            "PRIOR_CROSS": 0,
            "PRIOR_SAME": 128,
            "UNPRIOR_CROSS": 1024,
            "UNPRIOR_SAME": 2080,
        }
        and len(checkpoint_cross) == 1024,
        "fresh Round304 checkpoint exact R300A 128/2080/1024/0 classification",
    )
    physical = validate_closed_ledger(
        R305B_PHYSICAL, "rows", "Round305B_physical_witness_row_id", 1024
    )
    edge_rows = validate_closed_ledger(
        R305B_EDGE, "rows", "Round305B_canonical_component_edge_row_id", 8
    )
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    by_source: dict[str, dict[str, Any]] = {}
    for row in physical:
        need(
            set(row) == R305B_PHYSICAL_FIELDS
            and row.get("schema")
            == "cm2.round305b.source-g-r305a-two-sided-physical-inclusion-component-edge-promotion.v1.physical-witness-row.v1",
            "Round305B exact physical witness wire",
        )
        component_pair = tuple(row.get("Round304_final_component_pair", []))
        occurrence_pair = tuple(row.get("canonical_registry_occurrence_pair", []))
        G_fields = (
            "G0_exact_provenance_pins_and_row_closures",
            "G1_endpoint_occurrence_connected_supports",
            "G2_nonempty_connected_included_lower_stratum",
            "G3_left_closure_attaches_to_included_patch",
            "G4_right_closure_attaches_to_included_patch",
            "G5_endpoint_patch_provenance_exactly_closed",
        )
        need(
            len(component_pair) == 2
            and list(component_pair) == sorted(component_pair)
            and component_pair[0] != component_pair[1]
            and len(occurrence_pair) == 2
            and list(occurrence_pair) == sorted(occurrence_pair)
            and occurrence_pair[0] != occurrence_pair[1]
            and row.get("cross_official_key_physical_edge_permitted") is True
            and row.get("occurrence_identity_collapsed") is False
            and row.get("official_key_identity_merged") is False
            and row.get(
                "owner_extension_sidecar_not_Gamma_core_or_attachment_or_edge_basis"
            ) is True
            and row.get("corridor_box_used_as_Gamma_intersection") is False
            and row.get("D4_transfer_used") is False
            and row.get("candidate_physical_connectivity_conclusion") is True
            and all(
                type(row.get(field)) is dict
                and row[field].get("satisfied") is True
                for field in G_fields
            )
            and row.get("formal_physical_witness_credit") == 1
            and row.get("formal_component_edge_credit") == 0
            and row.get("formal_DSU_rank_reduction_credit") == 0
            and row.get("formal_maximality_credit") == 0
            and row.get("formal_fibre_credit") == 0
            and row.get("formal_global_disposition_credit") == 0,
            "Round305B physical witness lift boundary",
        )
        source = row.get("source_Round300A_row_id")
        need(type(source) is str and source not in by_source, "Round305B source uniqueness")
        checkpoint = checkpoint_cross.get(source)
        need(
            checkpoint is not None
            and row["source_Round300A_row_sha256"] == checkpoint["row_sha256"]
            and list(occurrence_pair) == checkpoint["occurrence_pair"]
            and component_pair == checkpoint["component_pair"]
            and tuple(row["official_key_pair"]) == checkpoint["official_key_pair"]
            and checkpoint["official_key_pair"][0]
            != checkpoint["official_key_pair"][1],
            "physical witness exact checkpoint source/root/component/key projection",
        )
        by_source[source] = row
        grouped[component_pair].append(row)
    need(
        set(by_source) == set(checkpoint_cross)
        and
        len(grouped) == 8
        and {len(rows) for rows in grouped.values()} == {128}
        and len({item for pair in grouped for item in pair}) == 16,
        "Round305B exact eight-pair matching",
    )
    edges: list[Any] = []
    lifts: list[Lift] = []
    seen_pairs: set[tuple[str, str]] = set()
    for edge_row in sorted(
        edge_rows, key=lambda row: row["Round305B_canonical_component_edge_row_id"]
    ):
        need(
            set(edge_row) == R305B_EDGE_FIELDS
            and edge_row.get("schema")
            == "cm2.round305b.source-g-r305a-two-sided-physical-inclusion-component-edge-promotion.v1.canonical-component-edge-row.v1",
            "Round305B exact component-edge wire",
        )
        component_pair = tuple(edge_row.get("canonical_Round304_final_component_pair", []))
        witnesses = grouped.get(component_pair, [])
        by_id = {row["Round305B_physical_witness_row_id"]: row for row in witnesses}
        witness_ids = sorted(by_id)
        witness_hashes = [by_id[item]["row_sha256"] for item in witness_ids]
        occurrence_pairs = sorted(
            row["canonical_registry_occurrence_pair"] for row in witnesses
        )
        official_profiles = {tuple(row["official_key_pair"]) for row in witnesses}
        need(
            len(component_pair) == 2
            and component_pair not in seen_pairs
            and len(witnesses) == 128
            and edge_row.get("physical_witness_row_count") == 128
            and edge_row.get("physical_witness_row_ids_sha256") == digest(witness_ids)
            and edge_row.get("physical_witness_row_sha256s_sha256") == digest(witness_hashes)
            and edge_row.get("canonical_occurrence_pairs_sha256") == digest(occurrence_pairs)
            and len(official_profiles) == 1
            and tuple(edge_row.get("canonical_official_key_pair", []))
            == next(iter(official_profiles))
            and edge_row.get("cross_official_key_physical_edge_permitted") is True
            and edge_row.get("occurrence_identity_collapsed") is False
            and edge_row.get("official_key_identity_merged") is False
            and edge_row.get("all_128_witnesses_satisfy_G0_G5") is True
            and edge_row.get("deduplicated_from_witness_rows_not_union_rows") is True
            and edge_row.get("formal_component_edge_credit") == 1
            and edge_row.get("eligible_for_later_fresh_DSU_application") is True
            and edge_row.get("formal_DSU_rank_reduction_credit") == 0,
            "Round305B component edge closure",
        )
        seen_pairs.add(component_pair)
        chosen = min(
            witnesses,
            key=lambda row: (
                tuple(row["canonical_registry_occurrence_pair"]),
                row["Round305B_physical_witness_row_id"],
            ),
        )
        occurrence_pair = tuple(chosen["canonical_registry_occurrence_pair"])
        need(all(item in member_root for item in occurrence_pair), "lift endpoint universe")
        root_pair = tuple(
            engine.endpoint_root(item, member_root, root_index)
            for item in occurrence_pair
        )
        selected_checkpoint = checkpoint_cross[
            chosen["source_Round300A_row_id"]
        ]
        reprojected = tuple(sorted(checkpoint_map[item] for item in root_pair))
        official_key_pair = tuple(chosen["official_key_pair"])
        need(
            reprojected == component_pair
            and root_pair == selected_checkpoint["root_pair"]
            and component_pair == selected_checkpoint["component_pair"]
            and checkpoint_map[root_pair[0]] != checkpoint_map[root_pair[1]]
            and list(official_key_pair) == sorted(official_key_pair)
            and official_key_pair
            == tuple(sorted(member_key[item] for item in occurrence_pair)),
            "independent exact lift projection",
        )
        lift = Lift(
            edge_row["Round305B_canonical_component_edge_row_id"],
            edge_row["row_sha256"],
            component_pair,
            chosen["Round305B_physical_witness_row_id"],
            chosen["row_sha256"],
            occurrence_pair,
            root_pair,
            official_key_pair,
        )
        lifts.append(lift)
        edges.append(
            engine.VEdge(
                "R305B_PHYSICAL_COMPONENT_EDGE",
                lift.edge_row_id,
                lift.edge_row_sha256,
                lift.occurrence_pair,
                lift.root_pair,
            )
        )
    need(len(edges) == len(lifts) == 8, "exact eight independent lifts")
    return edges, lifts, by_source


def make_row(id_field: str, namespace: str, payload: dict[str, Any]) -> dict[str, Any]:
    need(id_field not in payload and "row_sha256" not in payload, "row closure")
    row = {id_field: namespace + digest([namespace, payload]), **payload}
    row["row_sha256"] = digest(row)
    return row


def build_ledger(
    key: str, rows: Iterable[dict[str, Any]]
) -> tuple[bytes, dict[str, Any]]:
    materialized = list(rows)
    id_field = ID_FIELDS[key]
    ids = [row[id_field] for row in materialized]
    hashes = [row["row_sha256"] for row in materialized]
    need(len(ids) == len(set(ids)), "generated duplicate IDs:" + key)
    for row in materialized:
        need(
            set(row) == ROW_FIELDS[key]
            and row["schema"] == ROW_SCHEMAS[key],
            "generated exact row schema:" + key,
        )
        verify_self(row, "row_sha256", "generated:" + key)
    payload = {
        "schema": SCHEMA + "." + key + "-ledger.v1",
        "schema_snapshot_sha256": SCHEMA_SNAPSHOT_SHA256,
        "status": "PASS_DETERMINISTIC_ZERO_CREDIT_CANDIDATE_LEDGER",
        "row_count": len(materialized),
        "row_ids_sha256": digest(ids),
        "row_hashes_sha256": digest(hashes),
        "rows_sha256": digest(materialized),
        TABLES[key]: materialized,
    }
    document = {**payload, "ledger_sha256": digest(payload)}
    need(
        set(document) == LEDGER_FIELDS | {TABLES[key]},
        "generated exact ledger schema:" + key,
    )
    raw = deterministic_gzip(document)
    return raw, {
        "filename": FILES[key],
        "schema": document["schema"],
        "row_count": len(materialized),
        "row_ids_sha256": document["row_ids_sha256"],
        "row_hashes_sha256": document["row_hashes_sha256"],
        "rows_sha256": document["rows_sha256"],
        "ledger_sha256": document["ledger_sha256"],
        "file_sha256": hashlib.sha256(raw).hexdigest(),
    }


def iter_edge_rows(
    engine: Any,
    roots: list[str],
    root_index: dict[str, int],
    edges: list[Any],
) -> Iterator[dict[str, Any]]:
    dsu = engine.IndexUF(len(roots))
    for index, edge in enumerate(edges):
        reduced = dsu.merge(root_index[edge.roots[0]], root_index[edge.roots[1]])
        yield make_row(
            ID_FIELDS["edge"],
            "round306a-edge-application:",
            {
                "schema": SCHEMA + ".fresh-edge-application-row.v1",
                "application_index": index,
                "source_channel": edge.channel,
                "source_row_id": edge.source_id,
                "source_row_sha256": edge.source_sha,
                "canonical_occurrence_endpoint_pair": list(edge.endpoints),
                "projected_base_root_pair": sorted(edge.roots),
                "fed_to_new_empty_DSU": True,
                "forward_rank_reduction": int(reduced),
                "forward_cycle_or_redundant": int(not reduced),
                "candidate_DSU_rank_reduction": int(reduced),
                "serialized_Round304_partition_used_as_state": False,
                "formal_credit_without_independent_verification_marker": 0,
                "formal_maximality_credit": 0,
                "formal_fibre_credit": 0,
                "formal_global_disposition_credit": 0,
            },
        )


def iter_member_rows(
    member_root: dict[str, str],
    member_key: dict[str, str],
    final_map: dict[str, str],
) -> Iterator[dict[str, Any]]:
    for member in sorted(member_root):
        base_root = member_root[member]
        yield make_row(
            ID_FIELDS["member"],
            "round306a-member-component:",
            {
                "schema": SCHEMA + ".fresh-member-component-row.v1",
                "registry_occurrence_id": member,
                "base_root_id": base_root,
                "official_key_id": member_key[member],
                "final_component_id": final_map[base_root],
                "member_identity_preserved": True,
                "formal_maximality_credit": 0,
                "formal_fibre_credit": 0,
                "formal_global_disposition_credit": 0,
            },
        )


def iter_promoted_rows(lifts: list[Lift]) -> Iterator[dict[str, Any]]:
    for index, lift in enumerate(lifts):
        yield make_row(
            ID_FIELDS["promoted"],
            "round306a-r305b-promoted-edge-application:",
            {
                "schema": SCHEMA + ".r305b-promoted-edge-application-row.v1",
                "promoted_edge_index": index,
                "source_Round305B_component_edge_row_id": lift.edge_row_id,
                "source_Round305B_component_edge_row_sha256": lift.edge_row_sha256,
                "source_Round305B_selected_physical_witness_row_id": lift.witness_row_id,
                "source_Round305B_selected_physical_witness_row_sha256": lift.witness_row_sha256,
                "selection_rule": "LEXICOGRAPHIC_MIN_OCCURRENCE_PAIR_THEN_WITNESS_ID",
                "Round304_fresh_checkpoint_component_pair": list(lift.component_pair),
                "selected_occurrence_pair": list(lift.occurrence_pair),
                "projected_base_root_pair": list(lift.root_pair),
                "official_key_pair": list(lift.official_key_pair),
                "cross_checkpoint_components_before_application": True,
                "forward_rank_reduction": 1,
                "witness_rows_are_not_union_rows": True,
                "formal_official_key_merge_credit": 0,
                "formal_occurrence_identity_collapse_credit": 0,
                "formal_credit_without_independent_verification_marker": 0,
            },
        )


def build_frontier_rows(
    engine: Any,
    member_root: dict[str, str],
    root_index: dict[str, int],
    final_map: dict[str, str],
    witness_by_source: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    rows: list[dict[str, Any]] = []
    histogram: Counter[str] = Counter()
    source_ids: set[str] = set()
    for source in engine.gzip_rows(
        engine.R300A_LEDGER, "canonical_occurrence_pair_rows"
    ):
        engine.verify_self(source, "row_sha256", "Round306A independent R300A")
        source_id = source.get("Round300A_canonical_occurrence_pair_row_id")
        pair = source.get("canonical_unordered_Round294_registry_occurrence_ids")
        need(
            type(source_id) is str
            and source_id not in source_ids
            and type(pair) is list
            and len(pair) == 2
            and pair == sorted(pair)
            and pair[0] != pair[1]
            and source.get("left_Round294_registry_occurrence_id") == pair[0]
            and source.get("right_Round294_registry_occurrence_id") == pair[1]
            and source.get("formal_component_edge_credit") == 0
            and source.get("formal_DSU_rank_reduction_credit") == 0
            and source.get("formal_maximality_credit") == 0,
            "Round300A exact independent source row",
        )
        source_ids.add(source_id)
        root_pair = [
            engine.endpoint_root(item, member_root, root_index) for item in pair
        ]
        component_pair = sorted(final_map[item] for item in root_pair)
        same = component_pair[0] == component_pair[1]
        prior = source["R295A_explicit_lower_graph_sheet_witness_present"]
        need(type(prior) is bool, "Round300A prior witness boolean")
        r305b = witness_by_source.get(source_id)
        disposition = (
            "PRIOR_R295A_WITNESSED__SAME_ROUND306A_COMPONENT"
            if prior and same
            else (
                "PREVIOUSLY_UNWITNESSED__RECLOSED_BY_ROUND305B_PHYSICAL_EDGE"
                if (not prior and r305b is not None and same)
                else (
                    "PREVIOUSLY_UNWITNESSED__RECLOSED_BY_OTHER_LEGAL_DSU_PATH"
                    if (not prior and same)
                    else "CROSS_COMPONENT__FULL_MAXIMALITY_BLOCKER"
                )
            )
        )
        histogram[disposition] += 1
        rows.append(
            make_row(
                ID_FIELDS["frontier"],
                "round306a-r300a-reprojection:",
                {
                    "schema": SCHEMA + ".r300a-reprojection-row.v1",
                    "source_Round300A_row_id": source_id,
                    "source_Round300A_row_sha256": source["row_sha256"],
                    "canonical_occurrence_pair": pair,
                    "projected_base_root_pair": sorted(root_pair),
                    "Round306A_final_component_pair": component_pair,
                    "same_Round306A_final_component": same,
                    "prior_R295A_witness_present": prior,
                    "source_Round305B_physical_witness_row_id": (
                        r305b["Round305B_physical_witness_row_id"] if r305b else None
                    ),
                    "source_Round305B_physical_witness_row_sha256": (
                        r305b["row_sha256"] if r305b else None
                    ),
                    "disposition": disposition,
                    "Round300A_frontier_residual_credit": int(not same),
                    "formal_full_maximality_credit": 0,
                },
            )
        )
    expected = {
        "PREVIOUSLY_UNWITNESSED__RECLOSED_BY_OTHER_LEGAL_DSU_PATH": 2080,
        "PREVIOUSLY_UNWITNESSED__RECLOSED_BY_ROUND305B_PHYSICAL_EDGE": 1024,
        "PRIOR_R295A_WITNESSED__SAME_ROUND306A_COMPONENT": 128,
    }
    need(
        len(rows) == len(source_ids) == 3232
        and dict(sorted(histogram.items())) == expected,
        "Round300A exact zero residual frontier",
    )
    return rows, expected


def build_wtail_rows(
    engine: Any,
    unresolved: list[dict[str, Any]],
    final_map: dict[str, str],
    forest: dict[str, list[tuple[str, Any]]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in sorted(unresolved, key=lambda row: row["row_id"]):
        left, right = item["roots"]
        same = final_map[left] == final_map[right]
        stronger_path = engine.path(left, right, forest) if same else []
        need(same and bool(stronger_path), "Round306A W-tail reclosure")
        rows.append(
            make_row(
                ID_FIELDS["wtail"],
                "round306a-wtail-disposition:",
                {
                    "schema": SCHEMA + ".wtail-disposition-row.v1",
                    "source_W_tail_row_id": item["row_id"],
                    "source_W_tail_row_sha256": item["row_sha256"],
                    "source_Round300D_row_id": item["source_id"],
                    "canonical_occurrence_endpoint_pair": list(item["endpoints"]),
                    "projected_base_root_pair": sorted(item["roots"]),
                    "Round306A_final_component_pair": sorted(
                        [final_map[left], final_map[right]]
                    ),
                    "same_Round306A_final_component": True,
                    "disposition": "RECLOSED_BY_STRONGER_LEGAL_DSU_PATH__ZERO_NEW_EDGE",
                    "stronger_legal_path": stronger_path,
                    "source_row_fed_to_DSU": False,
                    "formal_component_edge_credit": 0,
                    "formal_maximality_credit": 0,
                },
            )
        )
    need(len(rows) == 4, "exact four W-tail rows")
    return rows


def reconstruct_state() -> dict[str, Any]:
    need(
        stable_sha256(PRODUCER, EXPECTED_PRODUCER_SHA256)
        == EXPECTED_PRODUCER_SHA256,
        "inert Round306A producer byte pin",
    )
    validate_round305b_seal()
    engine = load_independent_engine()
    engine.validate_upstream_seals()
    member_root, member_key, roots = engine.rebuild_universe()
    root_index = {root: index for index, root in enumerate(roots)}
    prior_edges = engine.old_edges(member_root, root_index)
    prior_map, prior, _ = engine.apply(
        roots,
        root_index,
        prior_edges,
        component_namespace="round301-legal-component:",
    )
    need(
        prior == {
            "edge_rows": 434606,
            "rank_reduction": 246016,
            "component_count": 121948,
            "partition_sha256": "c1ab6beed75d5e7379103975d6a9ac1b1095a3eb24b34c87288782e7c97cfe09",
            "per_channel_rank_reduction": prior["per_channel_rank_reduction"],
        },
        "fresh pre-R303B independent checkpoint",
    )
    r303b_edges, unresolved = engine.validate_r303b_and_edges(
        member_root, member_key, root_index, prior_map
    )
    r303b_census = {
        "edge_count": len(r303b_edges),
        "W_tail_count": len(unresolved),
        "distinct_endpoint_count": len({
            endpoint
            for item in (*r303b_edges, *unresolved)
            for endpoint in (
                item.endpoints if hasattr(item, "endpoints") else item["endpoints"]
            )
        }),
    }
    need(
        r303b_census
        == {"edge_count": 44104, "W_tail_count": 4,
            "distinct_endpoint_count": 88216},
        "independent Round303B exact census",
    )
    base_edges = prior_edges + r303b_edges
    checkpoint_map, checkpoint, _ = engine.apply(roots, root_index, base_edges)
    need(
        checkpoint["edge_rows"] == 478710
        and checkpoint["rank_reduction"] == 275268
        and checkpoint["component_count"] == 92696
        and checkpoint["partition_sha256"] == R304_PARTITION_SHA256,
        "fresh exact Round304 checkpoint through independent engine",
    )
    new_edges, lifts, witness_by_source = build_round305b_lifts(
        engine, member_root, member_key, root_index, checkpoint_map
    )
    all_edges = base_edges + new_edges
    final_map, forward, forest = engine.apply(
        roots,
        root_index,
        all_edges,
        keep_forest=True,
        component_namespace="round306-fresh-legal-component:",
    )
    reverse_map, reverse, _ = engine.apply(
        roots,
        root_index,
        reversed(all_edges),
        component_namespace="round306-fresh-legal-component:",
    )
    need(
        final_map == reverse_map
        and forward["edge_rows"] == reverse["edge_rows"] == 478718
        and forward["rank_reduction"] == reverse["rank_reduction"] == 275276
        and forward["component_count"] == reverse["component_count"] == 92688
        and forward["partition_sha256"]
        == reverse["partition_sha256"]
        == EXPECTED_PARTITION_SHA256
        and forward["per_channel_rank_reduction"].get(
            "R305B_PHYSICAL_COMPONENT_EDGE"
        )
        == 8
        and reverse["per_channel_rank_reduction"].get(
            "R305B_PHYSICAL_COMPONENT_EDGE"
        )
        == 8,
        "Round306A exact independent forward/reverse outcome",
    )
    frontier, frontier_histogram = build_frontier_rows(
        engine, member_root, root_index, final_map, witness_by_source
    )
    wtail = build_wtail_rows(engine, unresolved, final_map, forest)
    engine.assert_snapshot_map(engine.SOURCE_SNAPSHOTS, "Round304 engine source")
    need(
        stable_sha256(PRODUCER, EXPECTED_PRODUCER_SHA256)
        == EXPECTED_PRODUCER_SHA256
        and stable_sha256(R304_VERIFIER, R304_VERIFIER_SHA256)
        == R304_VERIFIER_SHA256
        and stable_sha256(R304_MANIFEST, R304_MANIFEST_SHA256)
        == R304_MANIFEST_SHA256
        and stable_sha256(R305B_MANIFEST, R305B_MANIFEST_SHA256)
        == R305B_MANIFEST_SHA256
        and stable_sha256(R305B_PHYSICAL, R305B_MANIFEST_PINS[R305B_PHYSICAL])
        == R305B_MANIFEST_PINS[R305B_PHYSICAL]
        and stable_sha256(R305B_EDGE, R305B_MANIFEST_PINS[R305B_EDGE])
        == R305B_MANIFEST_PINS[R305B_EDGE]
        and stable_sha256(
            R305B_VERIFICATION, R305B_MANIFEST_PINS[R305B_VERIFICATION]
        ) == R305B_MANIFEST_PINS[R305B_VERIFICATION],
        "critical source pins unchanged after independent reconstruction",
    )
    assert_sealed_snapshots("post-independent-reconstruction")
    return {
        "engine": engine,
        "member_root": member_root,
        "member_key": member_key,
        "roots": roots,
        "root_index": root_index,
        "prior": prior,
        "r303b_census": r303b_census,
        "checkpoint": checkpoint,
        "all_edges": all_edges,
        "lifts": lifts,
        "final_map": final_map,
        "forward": forward,
        "reverse": reverse,
        "frontier": frontier,
        "frontier_histogram": frontier_histogram,
        "wtail": wtail,
    }


def build_expected_candidate() -> tuple[dict[str, bytes], dict[str, Any]]:
    state = reconstruct_state()
    artifacts: dict[str, bytes] = {}
    metadata: dict[str, Any] = {}
    row_sources: tuple[tuple[str, Iterable[dict[str, Any]]], ...] = (
        (
            "edge",
            iter_edge_rows(
                state["engine"],
                state["roots"],
                state["root_index"],
                state["all_edges"],
            ),
        ),
        (
            "member",
            iter_member_rows(
                state["member_root"], state["member_key"], state["final_map"]
            ),
        ),
        ("promoted", iter_promoted_rows(state["lifts"])),
        ("frontier", state["frontier"]),
        ("wtail", state["wtail"]),
    )
    for key, rows in row_sources:
        raw, meta = build_ledger(key, rows)
        artifacts[FILES[key]] = raw
        metadata[key] = meta
    residual = make_row(
        ID_FIELDS["residual"],
        "round306a-residual-gate:",
        {
            "schema": SCHEMA + ".residual-gate-row.v1",
            "Round300A_complete_pair_count": 3232,
            "Round300A_cross_component_residual_count": 0,
            "Round305B_physical_witness_rows_consumed_as_edge_provenance": 1024,
            "Round305B_canonical_component_edge_applications": 8,
            "Round305B_rank_reductions": 8,
            "transformed_face_exhaustion_proved": False,
            "cross_chart_exhaustion_proved": False,
            "retained_event_exhaustion_proved": False,
            "occurrence_fibre_exhaustion_proved": False,
            "full_maximality_proved": False,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
            "D02_status": "BLOCKED",
            "CM2_status": "NO-GO_FOR_CLAIM",
        },
    )
    raw, meta = build_ledger("residual", [residual])
    artifacts[FILES["residual"]] = raw
    metadata["residual"] = meta
    result_payload = {
        "schema": SCHEMA + ".zero-credit-candidate-result.v1",
        "schema_snapshot_sha256": SCHEMA_SNAPSHOT_SHA256,
        "status": (
            "PASS_ROUND306A_FRESH_478718_EDGE_DSU_CANDIDATE__"
            "275276_RANK_REDUCTIONS__92688_COMPONENTS__"
            "PENDING_INDEPENDENT_VERIFICATION__"
            "ZERO_NEW_FORMAL_DSU_AND_MAXIMALITY_CREDIT"
        ),
        "producer_file_sha256": EXPECTED_PRODUCER_SHA256,
        "frozen_Round304_engine": {
            "filename": (
                "cm2_round304_source_g_fresh_extended_registry_legal_"
                "component_dsu_rebuild.py"
            ),
            "file_sha256": R304_MANIFEST_PINS[
                "cm2_round304_source_g_fresh_extended_registry_legal_component_dsu_rebuild.py"
            ],
            "complete_source_member_and_edge_universe_rebuilt": True,
            "serialized_Round304_partition_loaded_as_state": False,
        },
        "Round305B_seal": {
            "manifest_filename": R305B_MANIFEST,
            "manifest_file_sha256": R305B_MANIFEST_SHA256,
            "manifest_member_count": 14,
            "physical_witness_rows": 1024,
            "canonical_component_edges": 8,
            "independent_verification_is_formal_credit_marker": True,
        },
        "member_universe": {
            "member_count": len(state["member_root"]),
            "base_root_count": len(state["roots"]),
            "official_key_count": len(set(state["member_key"].values())),
        },
        "fresh_source_reconstruction_chain": {
            "pre_R303B_checkpoint": state["prior"],
            "Round303B_census": state["r303b_census"],
            "fresh_Round304_checkpoint": state["checkpoint"],
            "serialized_Round304_partition_loaded_as_state": False,
        },
        "fresh_Round304_checkpoint": state["checkpoint"],
        "fresh_forward_application": state["forward"],
        "fresh_reverse_application": state["reverse"],
        "forward_reverse_same_partition": True,
        "Round305B_edge_application": {
            "physical_witness_rows_are_not_union_rows": True,
            "edge_application_count": 8,
            "rank_reduction_count": 8,
            "sixteen_distinct_pre_edge_components": True,
            "selection_rule": "LEXICOGRAPHIC_MIN_OCCURRENCE_PAIR_THEN_WITNESS_ID",
            "inherited_officially_admitted_Round305B_component_edge_credit": 8,
            "new_component_edge_credit_issued_by_Round306A": 0,
            "candidate_incremental_DSU_rank_reduction_count": 8,
        },
        "Round300A_reprojection": {
            "row_count": 3232,
            "cross_component_residual_count": 0,
            "disposition_histogram": state["frontier_histogram"],
            "full_maximality_credit": 0,
        },
        "full_maximality_gate": {
            "Round300A_frontier_reprojected_to_zero": True,
            "transformed_face_exhaustion_proved": False,
            "cross_chart_exhaustion_proved": False,
            "retained_event_exhaustion_proved": False,
            "occurrence_fibre_exhaustion_proved": False,
            "full_maximality_proved": False,
            "formal_maximality_credit": 0,
        },
        "formal_credit_without_independent_verification_marker": {
            "formal_legal_component_edge_application_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_component_union_credit": 0,
            "formal_component_quotient_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
        },
        "candidate_credit_if_independently_verified": {
            "credit_semantics": (
                "REPLACEMENT_CERTIFICATE__NOT_ADDITIVE_TO_ROUND304_TOTALS"
            ),
            "superseded_Round304_totals": {
                "legal_edge_application_count": 478710,
                "DSU_rank_reduction_count": 275268,
                "post_Round304_component_count": 92696,
            },
            "incremental_over_sealed_Round304": {
                "new_Round305B_component_edge_applications": 8,
                "additional_DSU_rank_reductions": 8,
                "component_count_decrease": 8,
                "physical_witness_rows": 1024,
                "physical_witness_rows_are_not_union_rows": True,
            },
            "formal_legal_component_edge_application_credit": 478718,
            "formal_DSU_rank_reduction_credit": 275276,
            "formal_component_union_credit": 275276,
            "formal_component_quotient_credit": 1,
            "formal_post_Round306A_component_count": 92688,
            "formal_maximality_credit": 0,
        },
        "output_ledgers": metadata,
        "seed_affects_output": False,
        "D02_status": "BLOCKED",
        "CM2_status": "NO-GO_FOR_CLAIM",
    }
    result = {**result_payload, "result_sha256": digest(result_payload)}
    need(set(result) == RESULT_FIELDS, "generated exact result schema")
    result_raw = canonical(result)
    verify_self(strict_object(result_raw, "expected Round306A result"),
                "result_sha256", "expected Round306A result")
    artifacts[FILES["result"]] = result_raw
    need(
        tuple(artifacts) == CANDIDATE_ORDER,
        "exact expected candidate generation order",
    )
    need(
        stable_sha256(PRODUCER, EXPECTED_PRODUCER_SHA256)
        == EXPECTED_PRODUCER_SHA256,
        "producer inert pin after expected-byte reconstruction",
    )
    return artifacts, result


def validate_exact_bundle(
    bundle: dict[str, bytes], expected: dict[str, bytes]
) -> None:
    need(set(bundle) == set(CANDIDATE_ORDER), "exact seven candidate names")
    need(set(expected) == set(CANDIDATE_ORDER), "exact seven expected names")
    for name in CANDIDATE_ORDER:
        need(bundle[name] == expected[name], "exact candidate bytes:" + name)


@dataclass(frozen=True)
class FileSnapshot:
    device: int
    inode: int
    mode: int
    links: int
    size: int
    mtime_ns: int
    ctime_ns: int
    sha256: str


@dataclass(frozen=True)
class DirectorySnapshot:
    path: str
    device: int
    inode: int
    mode: int
    links: int
    size: int
    mtime_ns: int
    ctime_ns: int
    names: tuple[str, ...]
    names_sha256: str


@dataclass(frozen=True)
class CandidateSnapshot:
    directory: DirectorySnapshot
    files: tuple[tuple[str, FileSnapshot], ...]


def exact_directory(path: Path, label: str) -> Path:
    lexical = Path(os.path.abspath(os.fspath(path)))
    current = Path(lexical.anchor)
    for part in lexical.parts[1:]:
        current /= part
        need(os.path.lexists(current), label + ":missing-component:" + part)
        info = os.lstat(current)
        need(
            not stat.S_ISLNK(info.st_mode) and stat.S_ISDIR(info.st_mode),
            label + ":symlink-or-nondirectory:" + part,
        )
    need(lexical == lexical.resolve(), label + ":resolved-path")
    return lexical


def enforce_candidate_location_policy(
    candidate: Path,
    workspace: Path,
    formal_data: Path,
    private_root: Path,
) -> tuple[Path, Path]:
    candidate_absolute = Path(os.path.abspath(os.fspath(candidate)))
    workspace_absolute = Path(os.path.abspath(os.fspath(workspace)))
    data_absolute = Path(os.path.abspath(os.fspath(formal_data)))
    private_absolute = Path(os.path.abspath(os.fspath(private_root)))
    need(
        candidate_absolute != data_absolute
        and data_absolute not in candidate_absolute.parents,
        "candidate may not be deliverables or any deliverables descendant",
    )
    need(
        private_absolute != data_absolute
        and data_absolute not in private_absolute.parents
        and workspace_absolute in private_absolute.parents
        and candidate_absolute.parent == private_absolute,
        "candidate must be one direct child of the dedicated private root",
    )
    return candidate_absolute, private_absolute


def resolve_candidate_directory(candidate_dir: Path) -> Path:
    candidate_absolute, private_absolute = enforce_candidate_location_policy(
        candidate_dir, ROOT, DATA, PRIVATE_CANDIDATE_ROOT
    )
    private = exact_directory(private_absolute, "dedicated candidate root")
    need(
        stat.S_IMODE(os.lstat(private).st_mode) == 0o700,
        "dedicated candidate root mode 0700",
    )
    directory = exact_directory(candidate_absolute, "candidate directory")
    need(directory.parent == private, "candidate direct-child path stability")
    return directory


def read_candidate_file(
    directory_fd: int,
    name: str,
    expected_size: int,
) -> tuple[bytes, FileSnapshot]:
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(name, flags, dir_fd=directory_fd)
    try:
        before = os.fstat(descriptor)
        need(
            stat.S_ISREG(before.st_mode)
            and before.st_nlink == 1
            and before.st_size == expected_size
            and stat.S_IMODE(before.st_mode) == 0o600,
            "private candidate file boundary:" + name,
        )
        chunks: list[bytes] = []
        remaining = expected_size
        while remaining:
            block = os.read(descriptor, min(1 << 20, remaining))
            need(bool(block), "candidate short read:" + name)
            chunks.append(block)
            remaining -= len(block)
        need(os.read(descriptor, 1) == b"", "candidate trailing byte:" + name)
        raw = b"".join(chunks)
        after = os.fstat(descriptor)
        identity_before = (
            before.st_dev, before.st_ino, before.st_mode, before.st_nlink,
            before.st_size, before.st_mtime_ns, before.st_ctime_ns,
        )
        identity_after = (
            after.st_dev, after.st_ino, after.st_mode, after.st_nlink,
            after.st_size, after.st_mtime_ns, after.st_ctime_ns,
        )
        need(identity_before == identity_after, "candidate changed during read:" + name)
        return raw, FileSnapshot(
            *identity_after, hashlib.sha256(raw).hexdigest()
        )
    finally:
        os.close(descriptor)


def read_candidate_bundle(
    candidate_dir: Path,
    expected: dict[str, bytes],
) -> tuple[dict[str, bytes], CandidateSnapshot, Path]:
    directory = resolve_candidate_directory(candidate_dir)
    directory_info = os.lstat(directory)
    need(
        stat.S_IMODE(directory_info.st_mode) == 0o700,
        "candidate directory mode 0700",
    )
    descriptor = os.open(
        directory, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        before = os.fstat(descriptor)
        before_identity = (
            before.st_dev, before.st_ino, before.st_mode, before.st_nlink,
            before.st_size, before.st_mtime_ns, before.st_ctime_ns,
        )
        path_identity = (
            directory_info.st_dev, directory_info.st_ino,
            directory_info.st_mode, directory_info.st_nlink,
            directory_info.st_size, directory_info.st_mtime_ns,
            directory_info.st_ctime_ns,
        )
        need(before_identity == path_identity,
             "candidate directory path/fd identity before census")
        names = tuple(sorted(os.listdir(descriptor)))
        need(names == tuple(sorted(CANDIDATE_ORDER)),
             "candidate exact seven-file census")
        bundle: dict[str, bytes] = {}
        snapshots: dict[str, FileSnapshot] = {}
        for name in CANDIDATE_ORDER:
            raw, snapshot = read_candidate_file(descriptor, name, len(expected[name]))
            bundle[name] = raw
            snapshots[name] = snapshot
        names_after = tuple(sorted(os.listdir(descriptor)))
        after = os.fstat(descriptor)
        path_after = os.lstat(directory)
        after_identity = (
            after.st_dev, after.st_ino, after.st_mode, after.st_nlink,
            after.st_size, after.st_mtime_ns, after.st_ctime_ns,
        )
        path_after_identity = (
            path_after.st_dev, path_after.st_ino, path_after.st_mode,
            path_after.st_nlink, path_after.st_size,
            path_after.st_mtime_ns, path_after.st_ctime_ns,
        )
        need(
            names_after == names
            and after_identity == before_identity == path_after_identity,
            "candidate directory path/fd/census/mtime/ctime stability",
        )
        return (
            bundle,
            CandidateSnapshot(
                DirectorySnapshot(
                    str(directory), after.st_dev, after.st_ino, after.st_mode,
                    after.st_nlink, after.st_size, after.st_mtime_ns,
                    after.st_ctime_ns, names, digest(list(names)),
                ),
                tuple(sorted(snapshots.items())),
            ),
            directory,
        )
    finally:
        os.close(descriptor)


def assert_candidate_snapshot(
    candidate_dir: Path,
    snapshots: CandidateSnapshot,
    expected: dict[str, bytes],
    label: str,
) -> None:
    bundle, current, _ = read_candidate_bundle(candidate_dir, expected)
    need(
        current == snapshots
        and current.directory.path
        == str(resolve_candidate_directory(candidate_dir))
        and current.directory.names_sha256 == digest(list(current.directory.names)),
        "candidate secondary path/inode/census snapshot changed:" + label,
    )
    validate_exact_bundle(bundle, expected)


def contract_model() -> dict[str, Any]:
    return {
        "member_count": 564492,
        "base_root_count": 367964,
        "old_legal_edge_count": 478710,
        "Round305B_physical_witness_count": 1024,
        "Round305B_component_edge_count": 8,
        "Round305B_distinct_pre_edge_component_count": 16,
        "fresh_Round304_R300A_checkpoint_classification": {
            "prior_same": 128,
            "unprior_same": 2080,
            "unprior_cross": 1024,
            "prior_cross": 0,
        },
        "Round305B_physical_source_set_equals_checkpoint_cross_set": True,
        "Round305B_physical_all_G0_G5_satisfied": True,
        "Round305B_physical_exact_credit_boundary": True,
        "Round305B_edges_one_key_profile_and_16_vertex_matching": True,
        "sealed_inputs_fd_bound_and_snapshot_checked": True,
        "Round304_verifier_engine_compiled_from_verified_source_bytes": True,
        "producer_schema_snapshot_sha256": SCHEMA_SNAPSHOT_SHA256,
        "fresh_edge_application_count": 478718,
        "fresh_rank_reduction_count": 275276,
        "incremental_Round305B_rank_reduction_count": 8,
        "fresh_component_count": 92688,
        "fresh_partition_sha256": EXPECTED_PARTITION_SHA256,
        "forward_reverse_same_partition": True,
        "serialized_Round304_partition_used_as_state": False,
        "Round305B_witness_rows_used_as_union_rows": False,
        "Round300A_reprojection_count": 3232,
        "Round300A_cross_component_residual_count": 0,
        "transformed_face_exhaustion_proved": False,
        "cross_chart_exhaustion_proved": False,
        "retained_event_exhaustion_proved": False,
        "occurrence_fibre_exhaustion_proved": False,
        "full_maximality_proved": False,
        "formal_maximality_credit": 0,
        "formal_fibre_credit": 0,
        "formal_global_disposition_credit": 0,
        "candidate_producer_imported_or_executed": False,
        "independent_engine_is_Round304_promotion_verifier": True,
        "candidate_opened_only_after_expected_bytes_complete": True,
        "attack_suite_committed_first": True,
        "verification_committed_last": True,
        "fresh_quotient_supersedes_Round304_quotient": True,
        "fresh_rank_credit_additive_to_Round304_credit": False,
        "D02_status": "BLOCKED",
        "CM2_status": "NO-GO_FOR_CLAIM",
    }


def validate_contract_model(value: dict[str, Any]) -> None:
    need(value == contract_model(), "Round306A exact proof/credit contract")


def rejected(callback: Any) -> bool:
    try:
        callback()
    except (VerificationBlocked, KeyError, TypeError, ValueError, OSError):
        return True
    return False


def write_transaction_file_safe(
    directory: Path, name: str, raw: bytes, mode: int = 0o600
) -> None:
    directory_fd = os.open(
        directory,
        os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        descriptor = os.open(
            name,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL
            | getattr(os, "O_NOFOLLOW", 0),
            mode,
            dir_fd=directory_fd,
        )
        try:
            offset = 0
            while offset < len(raw):
                written = os.write(descriptor, raw[offset:])
                need(written > 0, "transaction fixture write progress")
                offset += written
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)


def make_transaction_case(
    base: Path, label: str
) -> tuple[Path, Path, Path, Path]:
    workspace = base / label
    data = workspace / "deliverables"
    private = workspace / "private-candidates"
    candidate = private / "candidate"
    for directory in (workspace, data, private, candidate):
        os.mkdir(directory, 0o700)
    return workspace, data, private, candidate


def populate_transaction_candidate(
    candidate: Path, expected: dict[str, bytes]
) -> None:
    for name in CANDIDATE_ORDER:
        write_transaction_file_safe(candidate, name, expected[name])


def validate_transaction_candidate(
    candidate: Path,
    workspace: Path,
    data: Path,
    private: Path,
    expected: dict[str, bytes],
) -> None:
    candidate_absolute, private_absolute = enforce_candidate_location_policy(
        candidate, workspace, data, private
    )
    need(
        exact_directory(private_absolute, "transaction private root")
        == private_absolute
        and stat.S_IMODE(os.lstat(private_absolute).st_mode) == 0o700,
        "transaction private root boundary",
    )
    directory = exact_directory(candidate_absolute, "transaction candidate")
    need(
        directory.parent == private_absolute
        and stat.S_IMODE(os.lstat(directory).st_mode) == 0o700,
        "transaction candidate directory boundary",
    )
    descriptor = os.open(
        directory,
        os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        before = os.fstat(descriptor)
        names = tuple(sorted(os.listdir(descriptor)))
        need(names == tuple(sorted(CANDIDATE_ORDER)),
             "transaction candidate exact census")
        for name in CANDIDATE_ORDER:
            raw, _snapshot = read_candidate_file(
                descriptor, name, len(expected[name])
            )
            need(raw == expected[name], "transaction candidate exact bytes")
        after = os.fstat(descriptor)
        need(
            names == tuple(sorted(os.listdir(descriptor)))
            and (
                before.st_dev, before.st_ino, before.st_mode,
                before.st_nlink, before.st_size, before.st_mtime_ns,
                before.st_ctime_ns,
            )
            == (
                after.st_dev, after.st_ino, after.st_mode,
                after.st_nlink, after.st_size, after.st_mtime_ns,
                after.st_ctime_ns,
            ),
            "transaction candidate stable second census",
        )
    finally:
        os.close(descriptor)


def run_filesystem_transaction_attacks() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    expected_candidate = {
        name: ("transaction-candidate:" + name).encode("ascii")
        for name in CANDIDATE_ORDER
    }
    promotion_artifacts = {
        name: ("transaction-promotion:" + name).encode("ascii")
        for name in PROMOTION_ORDER
    }
    rows: list[dict[str, Any]] = []

    def record(name: str, boundary: str, callback: Any) -> None:
        need(rejected(callback), "transaction attack accepted:" + name)
        row = {
            "attack_name": name,
            "attack_category": "FILESYSTEM_TRANSACTION",
            "rejected": True,
            "rejection_boundary": boundary,
        }
        rows.append(row)

    with tempfile.TemporaryDirectory(
        prefix=".round306a-hostile-", dir=ROOT
    ) as temporary:
        base = Path(temporary)
        os.chmod(base, 0o700)

        workspace, data, private, _candidate = make_transaction_case(
            base, "candidate-under-data"
        )
        under_data = data / "candidate"
        os.mkdir(under_data, 0o700)
        populate_transaction_candidate(under_data, expected_candidate)
        record(
            "CANDIDATE_UNDER_DELIVERABLES",
            "candidate path may not equal or descend from formal deliverables",
            lambda: validate_transaction_candidate(
                under_data, workspace, data, private, expected_candidate
            ),
        )

        workspace, data, private, candidate = make_transaction_case(
            base, "candidate-extra"
        )
        populate_transaction_candidate(candidate, expected_candidate)
        write_transaction_file_safe(candidate, "foreign.bin", b"foreign")
        record(
            "CANDIDATE_EXTRA_FILE",
            "second directory census requires exact seven-file set",
            lambda: validate_transaction_candidate(
                candidate, workspace, data, private, expected_candidate
            ),
        )

        workspace, data, private, candidate = make_transaction_case(
            base, "candidate-symlink"
        )
        populate_transaction_candidate(candidate, expected_candidate)
        victim = CANDIDATE_ORDER[0]
        os.unlink(candidate / victim)
        os.symlink(CANDIDATE_ORDER[1], candidate / victim)
        record(
            "CANDIDATE_SYMLINK_FILE",
            "O_NOFOLLOW exact regular candidate file",
            lambda: validate_transaction_candidate(
                candidate, workspace, data, private, expected_candidate
            ),
        )

        workspace, data, private, candidate = make_transaction_case(
            base, "candidate-hardlink"
        )
        populate_transaction_candidate(candidate, expected_candidate)
        victim = CANDIDATE_ORDER[1]
        os.unlink(candidate / victim)
        os.link(candidate / CANDIDATE_ORDER[0], candidate / victim)
        record(
            "CANDIDATE_HARDLINK_FILE",
            "candidate files require link count one",
            lambda: validate_transaction_candidate(
                candidate, workspace, data, private, expected_candidate
            ),
        )

        workspace, data, private, candidate = make_transaction_case(
            base, "candidate-file-permission"
        )
        populate_transaction_candidate(candidate, expected_candidate)
        os.chmod(candidate / CANDIDATE_ORDER[0], 0o644)
        record(
            "CANDIDATE_FILE_PERMISSION",
            "candidate files require exact mode 0600",
            lambda: validate_transaction_candidate(
                candidate, workspace, data, private, expected_candidate
            ),
        )

        workspace, data, private, candidate = make_transaction_case(
            base, "candidate-directory-permission"
        )
        populate_transaction_candidate(candidate, expected_candidate)
        os.chmod(candidate, 0o755)
        record(
            "CANDIDATE_DIRECTORY_PERMISSION",
            "candidate directory requires exact mode 0700",
            lambda: validate_transaction_candidate(
                candidate, workspace, data, private, expected_candidate
            ),
        )

        output = base / "foreign-stage-output"
        os.mkdir(output, 0o700)
        output_fd = os.open(output, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            stage_name = ".transaction-stage"
            os.mkdir(stage_name, 0o700, dir_fd=output_fd)
            write_transaction_file_safe(output / stage_name, "foreign", b"x")
            record(
                "FOREIGN_STAGE_MEMBER",
                "promotion stage contains only exact targets or owned partial names",
                lambda: ensure_stage(
                    output_fd, stage_name, promotion_artifacts,
                    [False] * len(PROMOTION_ORDER),
                ),
            )
        finally:
            os.close(output_fd)

        output = base / "formal-nonprefix-output"
        os.mkdir(output, 0o700)
        write_transaction_file_safe(
            output, PROMOTION_ORDER[1], promotion_artifacts[PROMOTION_ORDER[1]]
        )
        output_fd = os.open(output, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            record(
                "FORMAL_NONPREFIX",
                "preexisting formal files must form one exact commit prefix",
                lambda: formal_target_state(output_fd, promotion_artifacts),
            )
        finally:
            os.close(output_fd)

        output = base / "no-clobber-output"
        stage = base / "no-clobber-stage"
        os.mkdir(output, 0o700)
        os.mkdir(stage, 0o700)
        source_name = PROMOTION_ORDER[0]
        write_transaction_file_safe(stage, source_name, b"new")
        write_transaction_file_safe(output, source_name, b"old")
        output_fd = os.open(output, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        stage_fd = os.open(stage, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            def no_clobber_attack() -> None:
                try:
                    rename_noreplace(stage_fd, source_name, output_fd, source_name)
                except FileExistsError as exc:
                    read_exact_at(output_fd, source_name, b"old", "no-clobber target")
                    raise VerificationBlocked("no-clobber rejected") from exc
                return None

            record(
                "FORMAL_NO_CLOBBER",
                "renameat2 RENAME_NOREPLACE preserves an existing target",
                no_clobber_attack,
            )
        finally:
            os.close(stage_fd)
            os.close(output_fd)

        output = base / "partial-recovery-output"
        os.mkdir(output, 0o700)
        output_fd = os.open(output, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        recovery_stage_name = ".transaction-recovery-stage"
        os.mkdir(recovery_stage_name, 0o700, dir_fd=output_fd)
        recovery_stage = output / recovery_stage_name
        partial = stage_partial_name(
            0, PROMOTION_ORDER[0], promotion_artifacts[PROMOTION_ORDER[0]]
        )
        write_transaction_file_safe(recovery_stage, partial, b"partial-corrupt")
        write_transaction_file_safe(
            recovery_stage, PROMOTION_ORDER[1], b"invalid-exact-target"
        )
        recovery_fd = ensure_stage(
            output_fd, recovery_stage_name, promotion_artifacts,
            [False] * len(PROMOTION_ORDER),
        )
        try:
            need(
                tuple(sorted(os.listdir(recovery_fd)))
                == tuple(sorted(PROMOTION_ORDER)),
                "recovery exact target census",
            )
            for name in PROMOTION_ORDER:
                read_exact_at(
                    recovery_fd, name, promotion_artifacts[name],
                    "recovered stage target",
                )
        finally:
            os.close(recovery_fd)
            os.close(output_fd)
        recovery = {
            "scenario_id": "R01_PARTIAL_AND_INVALID_STAGE_RECOVERY",
            "scenario_category": "OWNED_STAGE_RECOVERY",
            "recovered_and_revalidated": True,
            "partial_temp_removed": True,
            "invalid_exact_target_removed": True,
            "all_exact_targets_rebuilt_via_temp_fsync_readback_rename": True,
        }
        recovery["row_sha256"] = digest(recovery)

    need(len(rows) == 9, "exact nine real filesystem transaction attacks")
    return rows, recovery


def build_attack_suite(
    producer_sha256: str | None = None,
    verifier_sha256: str | None = None,
    candidate_sha256s: dict[str, str] | None = None,
) -> dict[str, Any]:
    formal = (
        producer_sha256 is not None
        and verifier_sha256 is not None
        and candidate_sha256s is not None
    )
    if not formal:
        producer_sha256 = "0" * 64
        verifier_sha256 = runtime_verifier_sha256()
        candidate_sha256s = {
            name: hashlib.sha256(("selftest:" + name).encode("ascii")).hexdigest()
            for name in CANDIDATE_ORDER
        }
    assert producer_sha256 is not None
    assert verifier_sha256 is not None
    assert candidate_sha256s is not None
    need(
        len(producer_sha256) == len(verifier_sha256) == 64
        and set(candidate_sha256s) == set(CANDIDATE_ORDER)
        and all(len(value) == 64 for value in candidate_sha256s.values()),
        "attack exact baseline bindings",
    )
    base = contract_model()
    validate_contract_model(base)
    semantic_mutations: list[tuple[str, str, Any]] = [
        ("DROP_MEMBER", "exact member universe", lambda x: x.__setitem__("member_count", 564491)),
        ("DROP_BASE_ROOT", "exact base-root universe", lambda x: x.__setitem__("base_root_count", 367963)),
        ("DROP_OLD_EDGE", "complete pre-R305B edge universe", lambda x: x.__setitem__("old_legal_edge_count", 478709)),
        ("WITNESSES_AS_UNIONS", "1024 witnesses are provenance, not union rows", lambda x: x.__setitem__("Round305B_witness_rows_used_as_union_rows", True)),
        ("NINTH_EDGE", "exact eight canonical component edges", lambda x: x.__setitem__("Round305B_component_edge_count", 9)),
        ("NONMATCHING_PRECOMPONENTS", "eight edges join sixteen old components", lambda x: x.__setitem__("Round305B_distinct_pre_edge_component_count", 15)),
        ("CHECKPOINT_CLASSIFICATION_DRIFT", "exact prior/same/cross R300A partition", lambda x: x["fresh_Round304_R300A_checkpoint_classification"].__setitem__("unprior_cross", 1023)),
        ("PHYSICAL_SOURCE_SUBSTITUTION", "physical source set equals exact checkpoint cross set", lambda x: x.__setitem__("Round305B_physical_source_set_equals_checkpoint_cross_set", False)),
        ("PHYSICAL_G5_FALSE", "every physical row independently satisfies G0-G5", lambda x: x.__setitem__("Round305B_physical_all_G0_G5_satisfied", False)),
        ("PHYSICAL_FALSE_CREDIT", "physical rows carry only their sealed witness credit", lambda x: x.__setitem__("Round305B_physical_exact_credit_boundary", False)),
        ("EDGE_KEY_PROFILE_DRIFT", "each edge has one key profile and matching topology", lambda x: x.__setitem__("Round305B_edges_one_key_profile_and_16_vertex_matching", False)),
        ("PATH_BASED_SEALED_INPUT", "sealed inputs are fd-bound with PRE/POST snapshots", lambda x: x.__setitem__("sealed_inputs_fd_bound_and_snapshot_checked", False)),
        ("STALE_ENGINE_PYC", "Round304 verifier engine executes verified source bytes", lambda x: x.__setitem__("Round304_verifier_engine_compiled_from_verified_source_bytes", False)),
        ("PRODUCER_SCHEMA_DRIFT", "exact frozen producer wire snapshot", lambda x: x.__setitem__("producer_schema_snapshot_sha256", "0" * 64)),
        ("SEVEN_INCREMENTAL_RANKS", "all eight lifted edges reduce rank", lambda x: x.__setitem__("incremental_Round305B_rank_reduction_count", 7)),
        ("WRONG_TOTAL_RANK", "exact fresh rank", lambda x: x.__setitem__("fresh_rank_reduction_count", 275268)),
        ("WRONG_COMPONENT_COUNT", "exact fresh quotient cardinality", lambda x: x.__setitem__("fresh_component_count", 92696)),
        ("PARTITION_DRIFT", "forward/reverse exact partition commitment", lambda x: x.__setitem__("fresh_partition_sha256", "0" * 64)),
        ("REUSE_SERIALIZED_R304_STATE", "fresh DSU starts empty", lambda x: x.__setitem__("serialized_Round304_partition_used_as_state", True)),
        ("REVERSE_DIVERGENCE", "forward/reverse equality", lambda x: x.__setitem__("forward_reverse_same_partition", False)),
        ("R300A_RESIDUAL", "complete R300A frontier recloses", lambda x: x.__setitem__("Round300A_cross_component_residual_count", 1)),
        ("PREMATURE_MAXIMALITY", "other maximality channels remain open", lambda x: x.__setitem__("full_maximality_proved", True)),
        ("PREMATURE_FIBRE", "fibre credit remains zero", lambda x: x.__setitem__("formal_fibre_credit", 1)),
        ("PREMATURE_GLOBAL", "global disposition credit remains zero", lambda x: x.__setitem__("formal_global_disposition_credit", 1)),
        ("IMPORT_PRODUCER", "producer is inert pinned bytes", lambda x: x.__setitem__("candidate_producer_imported_or_executed", True)),
        ("USE_PRODUCER_ENGINE", "independent Round304 verifier engine only", lambda x: x.__setitem__("independent_engine_is_Round304_promotion_verifier", False)),
        ("ADDITIVE_DOUBLE_CREDIT", "fresh quotient supersedes rather than adds", lambda x: x.__setitem__("fresh_rank_credit_additive_to_Round304_credit", True)),
        ("VERIFICATION_NOT_LAST", "verification is sole final marker", lambda x: x.__setitem__("verification_committed_last", False)),
    ]
    semantic_rows: list[dict[str, Any]] = []
    for name, boundary, mutate in semantic_mutations:
        candidate = copy.deepcopy(base)
        mutate(candidate)
        need(
            rejected(lambda candidate=candidate: validate_contract_model(candidate)),
            "semantic attack accepted:" + name,
        )
        semantic_rows.append({
            "attack_name": name,
            "attack_category": "SEMANTIC_CONTRACT_UNIT",
            "rejected": True,
            "rejection_boundary": boundary,
        })

    wire_expected = {
        name: (candidate_sha256s[name] + ":" + name).encode("ascii")
        for name in CANDIDATE_ORDER
    }
    wire_rows: list[dict[str, Any]] = []
    wire_cases: list[tuple[str, str, dict[str, bytes]]] = []
    for index, name in enumerate(CANDIDATE_ORDER, 1):
        missing = dict(wire_expected)
        missing.pop(name)
        wire_cases.append((f"MISSING_{index}", "exact candidate name set", missing))
        altered = dict(wire_expected)
        altered[name] = altered[name] + b"!"
        wire_cases.append((f"ALTERED_{index}", "exact candidate bytes", altered))
        renamed = dict(wire_expected)
        renamed[name + ".bak"] = renamed.pop(name)
        wire_cases.append((f"RENAMED_{index}", "flat exact candidate basenames", renamed))
        extra = dict(wire_expected)
        extra[f"unexpected-{index}"] = b"foreign"
        wire_cases.append((f"EXTRA_{index}", "no foreign candidate members", extra))
    for name, boundary, candidate in wire_cases:
        need(
            rejected(lambda candidate=candidate: validate_exact_bundle(
                candidate, wire_expected
            )),
            "wire attack accepted:" + name,
        )
        wire_rows.append({
            "attack_name": name,
            "attack_category": "EXACT_WIRE_UNIT",
            "rejected": True,
            "rejection_boundary": boundary,
        })
    need(len(semantic_rows) == 28, "exact 28 semantic contract unit attacks")
    need(len(wire_rows) == 28, "exact 28 exact-wire unit attacks")
    transaction_rows, recovery = run_filesystem_transaction_attacks()
    need(
        len(transaction_rows) == 9
        and recovery["recovered_and_revalidated"] is True,
        "exact real filesystem transaction defense scenarios",
    )
    rows = semantic_rows + wire_rows + transaction_rows
    need(len(rows) == 65, "exact 65 rejected Round306A attacks")
    for index, row in enumerate(rows, 1):
        row["attack_id"] = f"A{index:02d}_" + row.pop("attack_name")
        row["row_sha256"] = digest(row)
    semantic_rows = rows[:28]
    wire_rows = rows[28:56]
    transaction_rows = rows[56:]
    payload = {
        "schema": SCHEMA + ".independent-attack-suite.v1",
        "status": (
            "PASS_28_SEMANTIC_UNITS_28_WIRE_UNITS_"
            "9_REAL_FILESYSTEM_ATTACKS_AND_1_RECOVERY_SELFTEST"
        ),
        "binding_mode": "EXACT_FORMAL_CANDIDATE" if formal else "SELFTEST_SYNTHETIC",
        "producer": {
            "filename": PRODUCER,
            "file_sha256": producer_sha256,
            "treated_as_inert_pinned_bytes_only": True,
            "imported_executed_parsed_or_tokenized": False,
        },
        "runtime_verifier": {
            "filename": VERIFIER,
            "file_sha256": verifier_sha256,
            "self_pin_embedded_in_source": False,
        },
        "independent_reconstruction_engine": {
            "filename": R304_VERIFIER,
            "file_sha256": R304_VERIFIER_SHA256,
            "Round304_producer_engine_used": False,
        },
        "producer_schema_snapshot_sha256": SCHEMA_SNAPSHOT_SHA256,
        "baseline_candidate_file_sha256s": dict(sorted(candidate_sha256s.items())),
        "semantic_contract_unit_count": len(semantic_rows),
        "semantic_contract_unit_rejected_count": len(semantic_rows),
        "exact_wire_unit_count": len(wire_rows),
        "exact_wire_unit_rejected_count": len(wire_rows),
        "filesystem_transaction_attack_count": len(transaction_rows),
        "filesystem_transaction_rejected_count": len(transaction_rows),
        "recovery_transaction_selftest_count": 1,
        "recovery_transaction_selftest_passed_count": 1,
        "attack_count": len(rows),
        "rejected_count": len(rows),
        "all_rejected": True,
        "scenario_count": len(rows) + 1,
        "all_defenses_passed": True,
        "attacks": rows,
        "owned_stage_recovery_selftest": recovery,
        "semantic_contract_unit_rows_sha256": digest(semantic_rows),
        "exact_wire_unit_rows_sha256": digest(wire_rows),
        "filesystem_transaction_rows_sha256": digest(transaction_rows),
        "attack_rows_sha256": digest(rows),
        "formal_Round306A_credit": 0,
    }
    return {**payload, "attack_suite_sha256": digest(payload)}


def runtime_verifier_sha256() -> str:
    path = Path(os.path.abspath(os.fspath(Path(__file__))))
    expected = DATA / VERIFIER
    need(
        path == expected
        and path.resolve() == expected.resolve()
        and os.path.lexists(path)
        and not path.is_symlink()
        and stat.S_ISREG(os.lstat(path).st_mode)
        and os.lstat(path).st_nlink == 1
        and path == path.resolve(),
        "runtime verifier is exact deliverables/VERIFIER path",
    )
    actual = stable_sha256(VERIFIER)
    snapshot = SEALED_SNAPSHOTS[VERIFIER]
    current = os.lstat(path)
    need(
        (
            current.st_dev, current.st_ino, current.st_mode,
            current.st_nlink, current.st_size, current.st_mtime_ns,
            current.st_ctime_ns,
        )
        == (
            snapshot.device, snapshot.inode, snapshot.mode,
            snapshot.links, snapshot.size, snapshot.mtime_ns,
            snapshot.ctime_ns,
        )
        and actual == snapshot.sha256,
        "runtime verifier fd/path inode and bytes stable",
    )
    return actual


def build_verification(
    result: dict[str, Any],
    candidate_sha256s: dict[str, str],
    attacks: dict[str, Any],
    verifier_sha256: str,
) -> dict[str, Any]:
    verify_self(attacks, "attack_suite_sha256", "Round306A attack suite")
    attack_raw = canonical(attacks)
    need(
        attacks["binding_mode"] == "EXACT_FORMAL_CANDIDATE"
        and attacks["producer"]["file_sha256"] == EXPECTED_PRODUCER_SHA256
        and attacks["runtime_verifier"]["file_sha256"] == verifier_sha256
        and attacks["baseline_candidate_file_sha256s"]
        == dict(sorted(candidate_sha256s.items()))
        and attacks["producer_schema_snapshot_sha256"]
        == SCHEMA_SNAPSHOT_SHA256
        and attacks["semantic_contract_unit_count"]
        == attacks["semantic_contract_unit_rejected_count"] == 28
        and attacks["exact_wire_unit_count"]
        == attacks["exact_wire_unit_rejected_count"] == 28
        and attacks["filesystem_transaction_attack_count"]
        == attacks["filesystem_transaction_rejected_count"] == 9
        and attacks["recovery_transaction_selftest_count"]
        == attacks["recovery_transaction_selftest_passed_count"] == 1
        and attacks["attack_count"] == attacks["rejected_count"] == 65
        and attacks["scenario_count"] == 66
        and attacks["all_rejected"] is True
        and attacks["all_defenses_passed"] is True,
        "formal attack exact binding",
    )
    before = {
        "officially_admitted_fresh_legal_component_edge_application_count": 0,
        "officially_admitted_fresh_DSU_rank_reduction_count": 0,
        "officially_admitted_fresh_component_union_count": 0,
        "officially_admitted_fresh_component_quotient_count": 0,
        "incremental_Round305B_rank_reduction_count": 0,
        "formal_maximality_credit": 0,
        "formal_fibre_credit": 0,
        "formal_global_disposition_credit": 0,
    }
    transition = {
        "officially_admitted_fresh_legal_component_edge_application_count": 478718,
        "officially_admitted_fresh_DSU_rank_reduction_count": 275276,
        "officially_admitted_fresh_component_union_count": 275276,
        "officially_admitted_fresh_component_quotient_count": 1,
        "incremental_Round305B_rank_reduction_count": 8,
        "post_Round306A_component_count": 92688,
        "formal_maximality_credit": 0,
        "formal_fibre_credit": 0,
        "formal_global_disposition_credit": 0,
    }
    payload = {
        "schema": SCHEMA + ".independent-verification.v1",
        "status": "PASS_EXACT_CACHELESS_ROUND306A_FRESH_LEGAL_COMPONENT_DSU_REBUILD",
        "producer": {
            "filename": PRODUCER,
            "file_sha256": EXPECTED_PRODUCER_SHA256,
            "treated_as_inert_pinned_bytes_only": True,
            "imported_executed_parsed_or_tokenized": False,
        },
        "runtime_verifier": {
            "filename": VERIFIER,
            "file_sha256": verifier_sha256,
            "runtime_self_hash_without_circular_source_pin": True,
        },
        "independent_reconstruction_engine": {
            "filename": R304_VERIFIER,
            "file_sha256": R304_VERIFIER_SHA256,
            "sealed_in_exact_Round304_11_member_manifest": True,
            "Round304_producer_engine_imported_or_executed": False,
            "independent_integer_index_DSU_used": True,
        },
        "candidate": {
            "opened_only_after_full_expected_bytes_rebuilt": True,
            "private_directory_separate_from_deliverables": True,
            "dedicated_private_candidate_root": PRIVATE_CANDIDATE_ROOT.name,
            "candidate_is_one_direct_child_of_dedicated_private_root": True,
            "candidate_and_private_root_mode": "0700",
            "candidate_file_mode": "0600",
            "candidate_file_link_count": 1,
            "fd_path_inode_and_second_census_snapshot_bound": True,
            "exact_seven_file_set": list(CANDIDATE_ORDER),
            "exact_file_sha256s": dict(sorted(candidate_sha256s.items())),
            "independent_expected_result_sha256": result["result_sha256"],
            "producer_schema_snapshot_sha256": SCHEMA_SNAPSHOT_SHA256,
            "all_seven_files_equal_independently_rebuilt_bytes": True,
            "candidate_outputs_written_or_replaced_during_admission": False,
        },
        "exact_fresh_DSU_census": {
            "member_count": 564492,
            "base_root_count": 367964,
            "legal_edge_application_count": 478718,
            "fresh_rank_reduction_count": 275276,
            "fresh_component_count": 92688,
            "fresh_partition_sha256": EXPECTED_PARTITION_SHA256,
            "forward_reverse_same_partition": True,
            "serialized_Round304_partition_used_as_state": False,
        },
        "Round305B_lift": {
            "physical_witness_rows_consumed_as_provenance": 1024,
            "canonical_component_edges_lifted": 8,
            "distinct_Round304_pre_edge_components": 16,
            "incremental_rank_reductions": 8,
            "witness_rows_are_not_union_rows": True,
        },
        "Round300A_reprojection": {
            "row_count": 3232,
            "cross_component_residual_count": 0,
            "sufficient_for_full_maximality": False,
        },
        "attack_suite": {
            "filename": ATTACK,
            "file_sha256": hashlib.sha256(attack_raw).hexdigest(),
            "object_self_sha256": attacks["attack_suite_sha256"],
            "attack_rows_sha256": attacks["attack_rows_sha256"],
            "semantic_contract_unit_rows_sha256": (
                attacks["semantic_contract_unit_rows_sha256"]
            ),
            "exact_wire_unit_rows_sha256": attacks["exact_wire_unit_rows_sha256"],
            "filesystem_transaction_rows_sha256": (
                attacks["filesystem_transaction_rows_sha256"]
            ),
            "semantic_contract_unit_count": 28,
            "semantic_contract_unit_rejected_count": 28,
            "exact_wire_unit_count": 28,
            "exact_wire_unit_rejected_count": 28,
            "filesystem_transaction_attack_count": 9,
            "filesystem_transaction_rejected_count": 9,
            "recovery_transaction_selftest_count": 1,
            "recovery_transaction_selftest_passed_count": 1,
            "attack_count": 65,
            "rejected_count": 65,
            "scenario_count": 66,
            "all_rejected": True,
            "all_defenses_passed": True,
        },
        "formal_credit_without_verification_commit_marker": before,
        "formal_credit_transition_at_this_verification_commit_marker": transition,
        "formal_credit_marker_definition": {
            "verification_last_and_sole_credit_marker": True,
            "marker_valid_only_after_exact_attack_seven_candidate_marker_full_bundle_postcheck": True,
            "fresh_marker_unlinked_on_owned_postcheck_failure": True,
            "marker_inode_and_exact_bytes_must_match_before_rollback": True,
            "preexisting_marker_is_never_claimed_as_owned_for_rollback": True,
            "credit_is_content_semantic_not_mtime_authenticated": True,
        },
        "credit_accounting": {
            "credit_semantics": (
                "REPLACEMENT_CERTIFICATE__NOT_ADDITIVE_TO_ROUND304_TOTALS"
            ),
            "fresh_Round306A_quotient_supersedes_Round304_quotient": True,
            "Round306A_275276_is_not_added_to_Round304_275268": True,
            "additive_to_prior_DSU_rank_credit": False,
            "increment_over_Round304_fresh_rank": 8,
            "superseded_Round304_legal_edge_application_count": 478710,
            "superseded_Round304_rank_reduction_count": 275268,
            "superseded_Round304_component_count": 92696,
        },
        "strict_downstream_boundary": {
            "Round300A_frontier_reprojected_to_zero": True,
            "transformed_face_exhaustion_proved": False,
            "cross_chart_exhaustion_proved": False,
            "retained_event_exhaustion_proved": False,
            "occurrence_fibre_exhaustion_proved": False,
            "full_maximality_proved": False,
            "official_fibres_exhausted": 0,
            "Source_G_global_dispositions_completed": 0,
            "D02_status": "BLOCKED",
            "CM2_status": "NO-GO_FOR_CLAIM",
        },
        "atomic_publication_contract": {
            "exact_output_directory": "deliverables",
            "commit_order": list(PROMOTION_ORDER),
            "attack_suite_is_first": True,
            "verification_is_last_and_sole_formal_credit_commit_marker": True,
            "flock_bound_directory_fd": True,
            "stage_fd_path_inode_bound_before_and_after_each_formal_rename": True,
            "owned_temp_name_then_fsync_exact_readback_atomic_stage_rename": True,
            "owned_partial_and_invalid_exact_stage_recovery": True,
            "foreign_stage_members_fail_closed": True,
            "fsync_stage_and_output_after_each_formal_rename": True,
            "renameat2_RENAME_NOREPLACE": True,
            "exact_prefix_recovery_only": True,
            "no_clobber": True,
            "post_marker_full_bundle_candidate_seal_and_source_postcheck": True,
            "safe_owned_marker_rollback_on_postcheck_failure": True,
        },
        "formal_Round306A_promotion_permitted": True,
    }
    return {**payload, "verification_sha256": digest(payload)}


def admit_candidate(
    candidate_dir: Path,
) -> tuple[
    dict[str, bytes], CandidateSnapshot, dict[str, Any],
    dict[str, Any], bytes, dict[str, Any], bytes,
]:
    expected, result = build_expected_candidate()
    need(
        stable_sha256(PRODUCER, EXPECTED_PRODUCER_SHA256)
        == EXPECTED_PRODUCER_SHA256,
        "producer inert pin before candidate open",
    )
    verifier_sha256 = runtime_verifier_sha256()
    bundle, snapshots, resolved = read_candidate_bundle(candidate_dir, expected)
    validate_exact_bundle(bundle, expected)
    candidate_sha256s = {
        name: hashlib.sha256(bundle[name]).hexdigest() for name in CANDIDATE_ORDER
    }
    attacks = build_attack_suite(
        EXPECTED_PRODUCER_SHA256, verifier_sha256, candidate_sha256s
    )
    attack_raw = canonical(attacks)
    need(
        canonical(strict_object(attack_raw, "generated Round306A attacks"))
        == attack_raw,
        "generated attack canonical bytes",
    )
    verification = build_verification(
        result, candidate_sha256s, attacks, verifier_sha256
    )
    verification_raw = canonical(verification)
    verify_self(verification, "verification_sha256", "generated verification")
    need(
        canonical(strict_object(verification_raw, "generated Round306A verification"))
        == verification_raw,
        "generated verification canonical bytes",
    )
    assert_candidate_snapshot(resolved, snapshots, expected, "post-attacks")
    need(
        stable_sha256(PRODUCER, EXPECTED_PRODUCER_SHA256)
        == EXPECTED_PRODUCER_SHA256
        and runtime_verifier_sha256() == verifier_sha256,
        "producer/verifier unchanged during admission",
    )
    assert_sealed_snapshots("post-candidate-admission")
    return (
        bundle, snapshots, result, attacks, attack_raw, verification,
        verification_raw,
    )


def read_exact_at(directory_fd: int, name: str, expected: bytes, label: str) -> bytes:
    descriptor = os.open(
        name, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=directory_fd
    )
    try:
        before = os.fstat(descriptor)
        named_before = os.stat(
            name, dir_fd=directory_fd, follow_symlinks=False
        )
        before_identity = (
            before.st_dev, before.st_ino, before.st_mode, before.st_nlink,
            before.st_size, before.st_mtime_ns, before.st_ctime_ns,
        )
        named_before_identity = (
            named_before.st_dev, named_before.st_ino, named_before.st_mode,
            named_before.st_nlink, named_before.st_size,
            named_before.st_mtime_ns, named_before.st_ctime_ns,
        )
        need(
            stat.S_ISREG(before.st_mode)
            and before.st_nlink == 1
            and before.st_size == len(expected)
            and stat.S_IMODE(before.st_mode) == 0o600,
            label + ":regular-size:" + name,
        )
        need(
            before_identity == named_before_identity,
            label + ":fd-path-inode-before:" + name,
        )
        chunks: list[bytes] = []
        remaining = len(expected)
        while remaining:
            block = os.read(descriptor, min(1 << 20, remaining))
            need(bool(block), label + ":short-read:" + name)
            chunks.append(block)
            remaining -= len(block)
        need(os.read(descriptor, 1) == b"", label + ":trailing:" + name)
        raw = b"".join(chunks)
        after = os.fstat(descriptor)
        named_after = os.stat(
            name, dir_fd=directory_fd, follow_symlinks=False
        )
        after_identity = (
            after.st_dev, after.st_ino, after.st_mode, after.st_nlink,
            after.st_size, after.st_mtime_ns, after.st_ctime_ns,
        )
        named_after_identity = (
            named_after.st_dev, named_after.st_ino, named_after.st_mode,
            named_after.st_nlink, named_after.st_size,
            named_after.st_mtime_ns, named_after.st_ctime_ns,
        )
        need(
            before_identity == after_identity == named_after_identity
            and raw == expected,
            label + ":stable-exact:" + name,
        )
        return raw
    finally:
        os.close(descriptor)


def rename_noreplace(
    old_directory_fd: int,
    old_name: str,
    new_directory_fd: int,
    new_name: str,
) -> None:
    libc = ctypes.CDLL(None, use_errno=True)
    function = getattr(libc, "renameat2", None)
    need(function is not None, "renameat2 required")
    function.argtypes = [
        ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p,
        ctypes.c_uint,
    ]
    function.restype = ctypes.c_int
    result = function(
        old_directory_fd,
        os.fsencode(old_name),
        new_directory_fd,
        os.fsencode(new_name),
        1,  # RENAME_NOREPLACE
    )
    if result != 0:
        code = ctypes.get_errno()
        if code == errno.EEXIST:
            raise FileExistsError(code, os.strerror(code), new_name)
        raise OSError(code, os.strerror(code), new_name)


def formal_target_state(
    directory_fd: int,
    artifacts: dict[str, bytes],
) -> list[bool]:
    states: list[bool] = []
    for name in PROMOTION_ORDER:
        try:
            os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
        except FileNotFoundError:
            states.append(False)
            continue
        read_exact_at(directory_fd, name, artifacts[name], "formal target")
        states.append(True)
    first_missing = next((i for i, exists in enumerate(states) if not exists), len(states))
    need(
        states == [True] * first_missing + [False] * (len(states) - first_missing),
        "formal targets must be one exact publication prefix",
    )
    return states


def exact_entry_or_false(
    directory_fd: int, name: str, expected: bytes, label: str
) -> bool:
    try:
        read_exact_at(directory_fd, name, expected, label)
    except (VerificationBlocked, OSError):
        return False
    return True


def stage_partial_name(index: int, name: str, raw: bytes) -> str:
    return (
        f".round306a-txn-{index:02d}-"
        + hashlib.sha256((name + ":").encode("ascii") + raw).hexdigest()[:20]
        + ".partial"
    )


def assert_bound_stage(
    output_fd: int,
    stage_name: str,
    stage_fd: int,
    expected_identity: tuple[int, int, int],
    label: str,
) -> None:
    opened = os.fstat(stage_fd)
    named = os.stat(stage_name, dir_fd=output_fd, follow_symlinks=False)
    opened_identity = (opened.st_dev, opened.st_ino, opened.st_mode)
    named_identity = (named.st_dev, named.st_ino, named.st_mode)
    need(
        opened_identity == named_identity == expected_identity,
        "stage fd/path inode stability:" + label,
    )


def ensure_stage(
    output_fd: int,
    stage_name: str,
    artifacts: dict[str, bytes],
    existing: list[bool],
) -> int:
    try:
        os.mkdir(stage_name, mode=0o700, dir_fd=output_fd)
    except FileExistsError:
        pass
    stage_fd = os.open(
        stage_name,
        os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0),
        dir_fd=output_fd,
    )
    stage_info = os.fstat(stage_fd)
    need(
        stat.S_ISDIR(stage_info.st_mode)
        and stat.S_IMODE(stage_info.st_mode) == 0o700,
        "private exact promotion stage",
    )
    stage_named = os.stat(stage_name, dir_fd=output_fd, follow_symlinks=False)
    need(
        (stage_info.st_dev, stage_info.st_ino)
        == (stage_named.st_dev, stage_named.st_ino),
        "promotion stage fd/path inode binding",
    )
    names = set(os.listdir(stage_fd))
    partial_names = {
        stage_partial_name(index, name, artifacts[name])
        for index, name in enumerate(PROMOTION_ORDER)
    }
    need(
        names <= set(PROMOTION_ORDER) | partial_names,
        "foreign promotion stage member",
    )
    for index, name in enumerate(PROMOTION_ORDER):
        partial = stage_partial_name(index, name, artifacts[name])
        if partial in names:
            os.unlink(partial, dir_fd=stage_fd)
            os.fsync(stage_fd)
            names.remove(partial)
        if name in names:
            if not exact_entry_or_false(
                stage_fd, name, artifacts[name], "recoverable stage target"
            ):
                os.unlink(name, dir_fd=stage_fd)
                os.fsync(stage_fd)
                names.remove(name)
            elif existing[index]:
                os.unlink(name, dir_fd=stage_fd)
                os.fsync(stage_fd)
                names.remove(name)
        if existing[index]:
            continue
        if name not in names:
            descriptor = os.open(
                partial,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL
                | getattr(os, "O_NOFOLLOW", 0),
                0o600,
                dir_fd=stage_fd,
            )
            try:
                raw = artifacts[name]
                offset = 0
                while offset < len(raw):
                    written = os.write(
                        descriptor, raw[offset:offset + (1 << 20)]
                    )
                    need(written > 0, "stage partial write progress:" + name)
                    offset += written
                os.fsync(descriptor)
            finally:
                os.close(descriptor)
            read_exact_at(stage_fd, partial, artifacts[name], "stage partial readback")
            rename_noreplace(stage_fd, partial, stage_fd, name)
            os.fsync(stage_fd)
            read_exact_at(stage_fd, name, artifacts[name], "new stage")
    os.fsync(stage_fd)
    return stage_fd


def entry_identity_at(directory_fd: int, name: str) -> tuple[int, ...]:
    info = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
    return (
        info.st_dev, info.st_ino, info.st_mode, info.st_nlink,
        info.st_size, info.st_mtime_ns, info.st_ctime_ns,
    )


def entry_inode_at(directory_fd: int, name: str) -> tuple[int, int]:
    info = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
    return info.st_dev, info.st_ino


def rollback_owned_marker(
    output_fd: int,
    marker_inode: tuple[int, int],
    marker_raw: bytes,
) -> bool:
    try:
        need(
            entry_inode_at(output_fd, VERIFICATION) == marker_inode,
            "rollback marker inode identity",
        )
        read_exact_at(
            output_fd, VERIFICATION, marker_raw, "rollback owned marker bytes"
        )
        os.unlink(VERIFICATION, dir_fd=output_fd)
        os.fsync(output_fd)
        return True
    except (VerificationBlocked, OSError):
        return False


def publish_formal_promotion(
    candidate_dir: Path,
    candidate_bundle: dict[str, bytes],
    candidate_snapshots: CandidateSnapshot,
    attack_raw: bytes,
    verification_raw: bytes,
) -> None:
    artifacts = {
        ATTACK: attack_raw,
        **{name: candidate_bundle[name] for name in CANDIDATE_ORDER},
        VERIFICATION: verification_raw,
    }
    need(tuple(artifacts) == PROMOTION_ORDER, "exact formal commit order")
    marker = strict_object(verification_raw, "formal verification marker")
    verify_self(marker, "verification_sha256", "formal verification marker")
    need(
        marker["candidate"]["exact_file_sha256s"]
        == {
            name: hashlib.sha256(candidate_bundle[name]).hexdigest()
            for name in sorted(CANDIDATE_ORDER)
        }
        and marker["attack_suite"]["file_sha256"]
        == hashlib.sha256(attack_raw).hexdigest()
        and marker["formal_Round306A_promotion_permitted"] is True,
        "verification marker content binds the complete candidate and attack",
    )
    expected_candidate = dict(candidate_bundle)
    candidate_resolved = resolve_candidate_directory(candidate_dir)
    assert_candidate_snapshot(
        candidate_resolved, candidate_snapshots, expected_candidate, "pre-promotion"
    )
    output = exact_directory(DATA, "formal deliverables")
    need(output == DATA.resolve(), "one exact formal output directory")
    output_fd = os.open(
        output,
        os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        fcntl.flock(output_fd, fcntl.LOCK_EX)
        bound = os.fstat(output_fd)
        path_info = os.stat(output, follow_symlinks=False)
        need(
            (bound.st_dev, bound.st_ino) == (path_info.st_dev, path_info.st_ino),
            "bound formal output directory inode",
        )
        existing = formal_target_state(output_fd, artifacts)
        stage_token = digest({
            "order": list(PROMOTION_ORDER),
            "sha256s": {
                name: hashlib.sha256(artifacts[name]).hexdigest()
                for name in PROMOTION_ORDER
            },
        })[:24]
        stage_name = "." + PREFIX + "-promotion-stage-" + stage_token
        stage_prefix = "." + PREFIX + "-promotion-stage-"
        orphans = {
            name for name in os.listdir(output_fd) if name.startswith(stage_prefix)
        }
        need(
            orphans <= {stage_name},
            "foreign or stale Round306A promotion stage requires manual audit",
        )
        if all(existing):
            if orphans:
                recovery_fd = ensure_stage(
                    output_fd, stage_name, artifacts, existing
                )
                try:
                    need(
                        not os.listdir(recovery_fd),
                        "post-marker exact orphan recovery stage is empty",
                    )
                finally:
                    os.close(recovery_fd)
                os.rmdir(stage_name, dir_fd=output_fd)
                os.fsync(output_fd)
            assert_candidate_snapshot(
                candidate_resolved,
                candidate_snapshots,
                expected_candidate,
                "idempotent complete promotion",
            )
            assert_sealed_snapshots("idempotent-complete-promotion")
            need(
                stable_sha256(PRODUCER, EXPECTED_PRODUCER_SHA256)
                == EXPECTED_PRODUCER_SHA256
                and runtime_verifier_sha256()
                == marker["runtime_verifier"]["file_sha256"],
                "idempotent complete source pins",
            )
            need(all(formal_target_state(output_fd, artifacts)),
                 "idempotent full formal bundle")
            return
        stage_fd = ensure_stage(output_fd, stage_name, artifacts, existing)
        stage_identity = (
            os.fstat(stage_fd).st_dev,
            os.fstat(stage_fd).st_ino,
            os.fstat(stage_fd).st_mode,
        )
        marker_committed_inode: tuple[int, int] | None = None
        try:
            try:
                for index, name in enumerate(PROMOTION_ORDER):
                    assert_bound_stage(
                        output_fd, stage_name, stage_fd, stage_identity,
                        "before-formal-rename:" + name,
                    )
                    if existing[index]:
                        continue
                    read_exact_at(
                        stage_fd, name, artifacts[name],
                        "bound stage source before formal rename",
                    )
                    source_inode = entry_inode_at(stage_fd, name)
                    if name == VERIFICATION:
                        for prior in PROMOTION_ORDER[:-1]:
                            read_exact_at(
                                output_fd, prior, artifacts[prior],
                                "complete prefix before sole marker",
                            )
                        need(
                            stable_sha256(PRODUCER, EXPECTED_PRODUCER_SHA256)
                            == EXPECTED_PRODUCER_SHA256
                            and runtime_verifier_sha256()
                            == marker["runtime_verifier"]["file_sha256"],
                            "source pins immediately before verification marker",
                        )
                        assert_sealed_snapshots("immediately-before-sole-marker")
                        assert_candidate_snapshot(
                            candidate_resolved,
                            candidate_snapshots,
                            expected_candidate,
                            "immediately before sole marker",
                        )
                    try:
                        rename_noreplace(stage_fd, name, output_fd, name)
                    except FileExistsError as exc:
                        raise VerificationBlocked(
                            "formal target raced no-clobber commit:" + name
                        ) from exc
                    if name == VERIFICATION:
                        marker_committed_inode = source_inode
                    os.fsync(stage_fd)
                    os.fsync(output_fd)
                    need(
                        entry_inode_at(output_fd, name) == source_inode,
                        "formal target preserves bound stage source inode:" + name,
                    )
                    read_exact_at(output_fd, name, artifacts[name], "post-commit")
                    assert_bound_stage(
                        output_fd, stage_name, stage_fd, stage_identity,
                        "after-formal-rename:" + name,
                    )
                need(not os.listdir(stage_fd), "promotion stage empty after commit")
                os.fsync(stage_fd)
                os.close(stage_fd)
                stage_fd = -1
                os.rmdir(stage_name, dir_fd=output_fd)
                os.fsync(output_fd)
                need(
                    all(formal_target_state(output_fd, artifacts)),
                    "complete formal bundle including marker",
                )
                current_path = os.stat(output, follow_symlinks=False)
                need(
                    (bound.st_dev, bound.st_ino)
                    == (current_path.st_dev, current_path.st_ino),
                    "formal directory stable after promotion",
                )
                assert_candidate_snapshot(
                    candidate_resolved,
                    candidate_snapshots,
                    expected_candidate,
                    "post-marker full-bundle validation",
                )
                assert_sealed_snapshots("post-marker-full-bundle-validation")
                need(
                    stable_sha256(PRODUCER, EXPECTED_PRODUCER_SHA256)
                    == EXPECTED_PRODUCER_SHA256
                    and runtime_verifier_sha256()
                    == marker["runtime_verifier"]["file_sha256"],
                    "post-marker source pins",
                )
            except BaseException as error:
                if stage_fd >= 0:
                    os.close(stage_fd)
                    stage_fd = -1
                if marker_committed_inode is not None:
                    rolled_back = rollback_owned_marker(
                        output_fd, marker_committed_inode, verification_raw
                    )
                    if not rolled_back:
                        raise VerificationBlocked(
                            "post-marker failure and safe marker rollback refused"
                        ) from error
                    raise VerificationBlocked(
                        "post-marker validation failed; owned marker rolled back"
                    ) from error
                raise
        finally:
            if stage_fd >= 0:
                os.close(stage_fd)
    finally:
        try:
            fcntl.flock(output_fd, fcntl.LOCK_UN)
        finally:
            os.close(output_fd)


def print_contract() -> None:
    print(canonical({
        "schema": SCHEMA + ".independent-verifier-contract.v1",
        "status": "IMPLEMENTED_INDEPENDENT_ZERO_CREDIT_VERIFIER",
        "expected_producer_sha256": EXPECTED_PRODUCER_SHA256,
        "producer_schema_snapshot_sha256": SCHEMA_SNAPSHOT_SHA256,
        "independent_engine": R304_VERIFIER,
        "independent_engine_sha256": R304_VERIFIER_SHA256,
        "candidate_artifact_count": len(CANDIDATE_ORDER),
        "dedicated_private_candidate_root": PRIVATE_CANDIDATE_ROOT.name,
        "semantic_contract_unit_count": 28,
        "exact_wire_unit_count": 28,
        "filesystem_transaction_attack_count": 9,
        "recovery_transaction_selftest_count": 1,
        "attack_count": 65,
        "defense_scenario_count": 66,
        "expected_member_count": 564492,
        "expected_base_root_count": 367964,
        "expected_edge_application_count": 478718,
        "expected_rank_reduction_count": 275276,
        "incremental_Round305B_rank_reduction_count": 8,
        "expected_component_count": 92688,
        "expected_partition_sha256": EXPECTED_PARTITION_SHA256,
        "formal_full_maximality_credit": 0,
        "promotion_order": list(PROMOTION_ORDER),
    }).decode("ascii"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--print-contract", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--no-write-reconstruction", action="store_true")
    parser.add_argument("--candidate-dir", type=Path)
    parser.add_argument("--promote", action="store_true")
    arguments = parser.parse_args()
    modes = sum((
        arguments.print_contract,
        arguments.self_test,
        arguments.no_write_reconstruction,
        arguments.candidate_dir is not None,
    ))
    need(modes == 1, "choose exactly one explicit verifier mode")
    need(not arguments.promote or arguments.candidate_dir is not None,
         "--promote requires --candidate-dir")
    if arguments.print_contract:
        print_contract()
        return
    if arguments.self_test:
        attacks = build_attack_suite()
        verify_self(attacks, "attack_suite_sha256", "self-test attacks")
        need(
            stable_sha256(R304_VERIFIER, R304_VERIFIER_SHA256)
            == R304_VERIFIER_SHA256
            and stable_sha256(R304_MANIFEST, R304_MANIFEST_SHA256)
            == R304_MANIFEST_SHA256
            and stable_sha256(R305B_MANIFEST, R305B_MANIFEST_SHA256)
            == R305B_MANIFEST_SHA256,
            "self-test frozen dependency pins",
        )
        print(canonical({
            "status": "PASS_ROUND306A_LIGHTWEIGHT_VERIFIER_SELF_TEST",
            "producer_pin_currently_matches": (
                stable_sha256(PRODUCER, EXPECTED_PRODUCER_SHA256)
                == EXPECTED_PRODUCER_SHA256
            ),
            "runtime_verifier_sha256": runtime_verifier_sha256(),
            "Round304_promotion_verifier_engine_pin_matches": True,
            "Round305B_manifest_pin_matches": True,
            "attack_count": attacks["attack_count"],
            "rejected_count": attacks["rejected_count"],
            "semantic_contract_unit_count": (
                attacks["semantic_contract_unit_count"]
            ),
            "exact_wire_unit_count": attacks["exact_wire_unit_count"],
            "filesystem_transaction_attack_count": (
                attacks["filesystem_transaction_attack_count"]
            ),
            "recovery_transaction_selftest_count": (
                attacks["recovery_transaction_selftest_count"]
            ),
            "defense_scenario_count": attacks["scenario_count"],
            "attack_suite_sha256": attacks["attack_suite_sha256"],
            "candidate_opened": False,
            "producer_imported_executed_parsed_or_tokenized": False,
            "formal_artifact_written": False,
        }).decode("ascii"))
        return
    if arguments.no_write_reconstruction:
        expected, result = build_expected_candidate()
        print(canonical({
            "status": "PASS_INDEPENDENT_CACHELESS_NO_WRITE_ROUND306A_RECONSTRUCTION",
            "result_sha256": result["result_sha256"],
            "expected_candidate_file_sha256s": {
                name: hashlib.sha256(expected[name]).hexdigest()
                for name in CANDIDATE_ORDER
            },
            "fresh_rank_reduction_count": 275276,
            "fresh_component_count": 92688,
            "incremental_Round305B_rank_reduction_count": 8,
            "Round300A_cross_component_residual_count": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
            "candidate_opened": False,
            "candidate_or_formal_output_written": False,
            "producer_imported_executed_parsed_or_tokenized": False,
        }).decode("ascii"))
        return
    assert arguments.candidate_dir is not None
    (
        bundle, snapshots, result, attacks, attack_raw, verification,
        verification_raw,
    ) = admit_candidate(arguments.candidate_dir)
    if arguments.promote:
        publish_formal_promotion(
            arguments.candidate_dir,
            bundle,
            snapshots,
            attack_raw,
            verification_raw,
        )
        print(verification_raw.decode("ascii"))
        return
    before = verification["formal_credit_without_verification_commit_marker"]
    need(all(value == 0 for value in before.values()),
         "admission without marker remains zero credit")
    print(canonical({
        "status": "PASS_EXACT_ROUND306A_PRIVATE_CANDIDATE_ADMISSION__ZERO_FORMAL_CREDIT",
        "candidate_file_sha256s": verification["candidate"]["exact_file_sha256s"],
        "candidate_result_sha256": result["result_sha256"],
        "attack_suite": {
            "filename": ATTACK,
            "file_sha256": hashlib.sha256(attack_raw).hexdigest(),
            "object_self_sha256": attacks["attack_suite_sha256"],
        },
        "verification": {
            "filename": VERIFICATION,
            "file_sha256": hashlib.sha256(verification_raw).hexdigest(),
            "object_self_sha256": verification["verification_sha256"],
        },
        "formal_credit": before,
        "formal_deliverables_written": False,
    }).decode("ascii"))


if __name__ == "__main__":
    try:
        main()
    except VerificationBlocked as error:
        print("BLOCKED_ROUND306A_VERIFIER:" + str(error))
        raise SystemExit(2)
