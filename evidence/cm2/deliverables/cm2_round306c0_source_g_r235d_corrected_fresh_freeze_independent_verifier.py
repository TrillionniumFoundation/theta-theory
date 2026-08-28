#!/usr/bin/env python3
"""Independent verifier for the Round306C0 R235D-corrected fresh freeze.

This program consumes the sealed Round306A and R235D packages only as pinned
data.  It never imports or executes either package's producer or verifier.  It
independently removes the exact thirty-two invalid members, reconstructs every
old-root disposition, remaps all 478,718 edge applications, performs fresh
forward and reverse DSU replays, and rebuilds the corrected root/member/
component ledgers and exact cross-component pair denominator.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from copy import deepcopy
from dataclasses import dataclass
import gzip
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
from typing import Any, Final, Iterable, Iterator, Mapping
import zlib


class Rejected(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Rejected(label)


ROOT: Final = Path(__file__).parent
PREFIX: Final = "cm2_round306c0_source_g_r235d_corrected_fresh_freeze"
SCHEMA: Final = "cm2.round306c0.source-g-r235d-corrected-fresh-freeze.v1"
PRODUCER_NAME: Final = PREFIX + "_producer.py"
VERIFIER_NAME: Final = PREFIX + "_independent_verifier.py"
ATTACK_NAME: Final = PREFIX + "_attack_suite.json"
VERIFICATION_NAME: Final = PREFIX + "_verification.json"
REPORT_NAME: Final = PREFIX + "_report.md"
COLD_NAME: Final = PREFIX + "_cold_replay.md"
MANIFEST_NAME: Final = PREFIX + "_manifest.sha256"
COMPONENT_NAMESPACE: Final = "round306c0-fresh-legal-component:"
CORRECTED_ROOT_NAMESPACE: Final = "round306c0-corrected-base-root:"
ROW_CAP: Final = 8_388_608
FIXED_SPILL_PARENT: Final = "/tmp/cm2-round306c0-spill"

OUTPUTS: Final = {
    "authority_frontier": PREFIX + "_authority_frontier.json",
    "member_invalidation": PREFIX + "_member_invalidation_ledger.jsonl.gz",
    "root_disposition": PREFIX + "_base_root_disposition_ledger.jsonl.gz",
    "edge_remap": PREFIX + "_edge_remap_application_ledger.jsonl.gz",
    "member_component": PREFIX + "_fresh_member_component_ledger.jsonl.gz",
    "base_root_component": PREFIX + "_fresh_base_root_component_ledger.jsonl.gz",
    "component_census": PREFIX + "_fresh_component_census.jsonl.gz",
    "pair_denominator": PREFIX + "_cross_component_pair_denominator.json",
    "result": PREFIX + "_result.json",
}
OUTPUT_ORDER: Final = tuple(OUTPUTS)
MANIFEST_MEMBERS: Final = (
    PRODUCER_NAME,
    *(OUTPUTS[role] for role in OUTPUT_ORDER),
    VERIFIER_NAME,
    ATTACK_NAME,
    VERIFICATION_NAME,
    REPORT_NAME,
    COLD_NAME,
)

ROW_SCHEMAS: Final = {
    "member_invalidation": SCHEMA + ".member-invalidation-row.v1",
    "root_disposition": SCHEMA + ".base-root-disposition-row.v1",
    "edge_remap": SCHEMA + ".edge-remap-application-row.v1",
    "member_component": SCHEMA + ".fresh-member-component-row.v1",
    "base_root_component": SCHEMA + ".fresh-base-root-component-row.v1",
    "component_census": SCHEMA + ".fresh-component-census-row.v1",
}

ROW_FIELDS: Final = {
    "member_invalidation": (
        "schema", "row_id", "invalidation_role", "registry_member_id",
        "source_R235D_authority_ordinal",
        "source_R235D_invalidation_row_id", "source_R235D_invalidation_row_sha256",
        "source_Round306A_member_row_ordinal",
        "source_Round306A_member_row_id",
        "source_Round306A_member_row_wire_sha256",
        "source_Round306A_member_row_sha256", "old_base_root_id",
        "old_component_id",
        "formal_R248_correction_overlay_credit_without_independent_verification_marker",
        "row_sha256",
    ),
    "root_disposition": (
        "schema", "row_id", "old_base_root_id", "disposition",
        "old_member_count", "deleted_member_count", "deleted_member_ids",
        "deleted_member_ids_sha256",
        "retained_member_count", "retained_member_ids_sha256",
        "retained_source_row_sha256_sequence_sha256", "official_key_id",
        "canonical_input_commitment_sha256",
        "corrected_base_root_id_or_null", "old_component_id",
        "candidate_complete_selected_row_R248_correction_overlay",
        "formal_corrected_root_credit_without_independent_verification_marker",
        "row_sha256",
    ),
    "edge_remap": (
        "schema", "row_id", "application_index", "source_Round306A_row_id",
        "source_Round306A_row_wire_sha256", "source_Round306A_row_sha256",
        "source_channel", "source_row_id",
        "old_canonical_occurrence_endpoint_pair",
        "corrected_canonical_occurrence_endpoint_pair",
        "old_projected_base_root_pair",
        "corrected_projected_base_root_pair", "delete_root_hit_count",
        "invalid_member_endpoint_hit_count",
        "distinct_root_remap_collision", "forward_rank_reduction",
        "old_forward_rank_flag_match", "reverse_application_index",
        "reverse_rank_reduction",
        "formal_corrected_DSU_credit_without_independent_verification_marker",
        "row_sha256",
    ),
    "member_component": (
        "schema", "row_id", "registry_member_id",
        "source_Round306A_row_ordinal", "source_Round306A_row_id",
        "source_Round306A_row_wire_sha256", "source_Round306A_row_sha256",
        "old_base_root_id",
        "corrected_base_root_id", "root_disposition", "official_key_id",
        "corrected_component_id", "member_identity_preserved",
        "formal_corrected_member_universe_credit_without_independent_verification_marker",
        "formal_corrected_DSU_credit_without_independent_verification_marker",
        "row_sha256",
    ),
    "base_root_component": (
        "schema", "row_id", "corrected_base_root_id", "old_base_root_id",
        "root_disposition", "member_count", "member_ids_sha256",
        "official_key_id", "corrected_component_id", "edge_row_hit_count",
        "projected_root_slot_hit_count", "exact_occurrence_root_slot_hit_count",
        "formal_corrected_DSU_credit_without_independent_verification_marker",
        "row_sha256",
    ),
    "component_census": (
        "schema", "row_id", "corrected_component_id", "base_root_count",
        "base_root_ids_sha256", "member_count", "member_ids_sha256",
        "formal_corrected_DSU_credit_without_independent_verification_marker",
        "row_sha256",
    ),
}
ROW_ID_NAMESPACES: Final = {
    "member_invalidation": "round306c0-member-invalidation:",
    "root_disposition": "round306c0-base-root-disposition:",
    "edge_remap": "round306c0-edge-remap-application:",
    "member_component": "round306c0-member-component:",
    "base_root_component": "round306c0-base-root-component:",
    "component_census": "round306c0-component-census:",
}
LEDGER_ROW_COUNTS: Final = {
    "member_invalidation": 32,
    "root_disposition": 367_964,
    "edge_remap": 478_718,
    "member_component": 564_460,
    "base_root_component": 367_948,
    "component_census": 92_672,
}

OLD_MEMBER_SCHEMA: Final = "cm2.round306a.source-g-r305b-fresh-legal-component-dsu-rebuild.v1.fresh-member-component-row.v1"
OLD_MEMBER_FIELDS: Final = {
    "Round306A_fresh_member_component_row_id", "schema", "registry_occurrence_id",
    "base_root_id", "official_key_id", "final_component_id",
    "member_identity_preserved", "formal_maximality_credit", "formal_fibre_credit",
    "formal_global_disposition_credit", "row_sha256",
}
OLD_EDGE_SCHEMA: Final = "cm2.round306a.source-g-r305b-fresh-legal-component-dsu-rebuild.v1.fresh-edge-application-row.v1"
OLD_EDGE_FIELDS: Final = {
    "Round306A_fresh_edge_application_row_id", "schema", "application_index",
    "source_channel", "source_row_id", "source_row_sha256",
    "canonical_occurrence_endpoint_pair", "projected_base_root_pair",
    "fed_to_new_empty_DSU", "forward_rank_reduction",
    "forward_cycle_or_redundant", "candidate_DSU_rank_reduction",
    "serialized_Round304_partition_used_as_state",
    "formal_credit_without_independent_verification_marker",
    "formal_maximality_credit", "formal_fibre_credit",
    "formal_global_disposition_credit", "row_sha256",
}
R235D_ROW_SCHEMA: Final = "cm2.round306b1af4k2r235d.source-g-double-endpoint-source-only-local-theorem.row.v1"
R235D_RESULT_SCHEMA: Final = "cm2.round306b1af4k2r235d.source-g-double-endpoint-source-only-local-theorem.result.v1"
R235D_VERIFICATION_SCHEMA: Final = "cm2.round306b1af4k2r235d.source-g-double-endpoint-source-only-local-theorem.verification.v1"


@dataclass(frozen=True)
class Pin:
    role: str
    filename: str
    size: int
    sha256: str


ROUND306A_MANIFEST: Final = Pin(
    "ROUND306A_MANIFEST",
    "cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_manifest.sha256",
    1_982,
    "35da99af5bb4c424284af2d7b396fc94b82dd6c6aa468c6a43a139107f9d9efc",
)
ROUND306A_MEMBERS: Final = (
    Pin("ROUND306A_PRODUCER", "cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild.py", 74_003, "ab798332c82f7aa3656c61e3b31698a30b0fa1a83d24900432e076e445d6f5d5"),
    Pin("ROUND306A_EDGE_LEDGER", "cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_edge_application_ledger.json.gz", 118_345_367, "6da4620a100c980f921350f162fda064580e603f8ff7221eeed768b8bd091d1f"),
    Pin("ROUND306A_MEMBER_LEDGER", "cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_member_component_ledger.json.gz", 107_900_487, "710ebb660a7e7fad6a691c03bf845cf0081037ed09cc49a885c94c4bc472c276"),
    Pin("ROUND306A_R305B_LEDGER", "cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_r305b_promoted_edge_application_ledger.json.gz", 5_012, "08f9ff2f5df0210cedd8cb3f8d998846e3722bd6bb0a2216d8d6c24a95a64a41"),
    Pin("ROUND306A_R300A_LEDGER", "cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_r300a_reprojection_ledger.json.gz", 961_815, "c3e62f9833c333fb89758edd5c3f1648364a70b91bd1ed85650241a4cd10b673"),
    Pin("ROUND306A_WTAIL_LEDGER", "cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_wtail_disposition_ledger.json.gz", 3_667, "6bdcc231b3cfd67f18ff3c62c27af08fdc9eb562a2c4e24a601798c0ad6d2556"),
    Pin("ROUND306A_RESIDUAL_LEDGER", "cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_residual_gate_ledger.json.gz", 797, "1e79d529f3ca1fcefa170263a5d8b88929361ea27c0eeb3c6de108b870f9d8b8"),
    Pin("ROUND306A_RESULT", "cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_result.json", 9_827, "febe77da4285791b54e098c80a4b868c1e5dc6e43e98a7553bfff5e065075010"),
    Pin("ROUND306A_VERIFIER", "cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_promotion_verifier.py", 134_516, "60cc0f9cec6c8f4121f7ed7fde45b11e1b72bd9adc897364d9c0937c92a54c72"),
    Pin("ROUND306A_ATTACK", "cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_attack_suite.json", 18_537, "9e3f2bcf3f39af739bc05ca2f3acef2828f96e6f19402fe6a85bb3353f5fc25e"),
    Pin("ROUND306A_VERIFICATION", "cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_verification.json", 9_311, "38fd7f9d41dcf39a2ec887d72b31da3d003cf03eda154da34d3a5d87ff12ba7e"),
    Pin("ROUND306A_REPORT", "cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_report.md", 9_175, "d2bd7d808736c333a4bb9b9af55d55d72e61e38023b1723c976d10eaae54671b"),
    Pin("ROUND306A_COLD_REPLAY", "cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_cold_replay.md", 8_118, "ce3cb89ccf84ee6e6349afd5c3a9d92d6e981c3138b05fe3da791558d56c974e"),
)

R235D_MANIFEST: Final = Pin(
    "R235D_MANIFEST",
    "cm2_round306b1af4k2r235d_source_g_double_endpoint_source_only_local_theorem_manifest.sha256",
    1_276,
    "0aa2128655e7f90eaeeda47a66901ea45e0908a6f569dc7760ead49ac539e7c0",
)
R235D_MEMBERS: Final = (
    Pin("R235D_PRODUCER", "cm2_round306b1af4k2r235d_source_g_double_endpoint_source_only_local_theorem_producer.py", 84_128, "d6d78b8ffb60c52a70294a83ff575c9d45efac4a1e618743e96ff503a15e7423"),
    Pin("R235D_LEDGER", "cm2_round306b1af4k2r235d_source_g_double_endpoint_source_only_local_theorem_row_commitment_ledger.jsonl.gz", 144_211, "6eaeee6a158ad7c0c3d62380214e1ae24ac2a63cb7678b312401cca91cb4cfe0"),
    Pin("R235D_RESULT", "cm2_round306b1af4k2r235d_source_g_double_endpoint_source_only_local_theorem_result.json", 45_075, "3856a04a5b88574f1ffd6aac7f4fda42c014eac401c2a73efbc6c0ea10c9e5ff"),
    Pin("R235D_VERIFIER", "cm2_round306b1af4k2r235d_source_g_double_endpoint_source_only_local_theorem_independent_verifier.py", 88_342, "cc80855562d8ea8022881314647e6fe974ea8060b41e2c49c8ab48a28ac18559"),
    Pin("R235D_ATTACK", "cm2_round306b1af4k2r235d_source_g_double_endpoint_source_only_local_theorem_attack_suite.json", 1_340, "238309c6fea17edbcbe383e966383e57f8dd9bf888baff152bd09a0a28cd5236"),
    Pin("R235D_VERIFICATION", "cm2_round306b1af4k2r235d_source_g_double_endpoint_source_only_local_theorem_verification.json", 1_740, "865f2aab8fab721aa24c0772d516806968555a28eb5529056e3cb6438d9d1468"),
    Pin("R235D_REPORT", "cm2_round306b1af4k2r235d_source_g_double_endpoint_source_only_local_theorem_report.md", 3_893, "bd5604653adab6edb5c584b43d80e76001a6e324cf615fed269263e22d0fb192"),
    Pin("R235D_COLD", "cm2_round306b1af4k2r235d_source_g_double_endpoint_source_only_local_theorem_cold_replay.md", 1_134, "c36dbdf77460ebadec55d476d6d6401bed05466f569f627c583b55afd124aedd"),
)

AUTHORITY_PINS: Final = (ROUND306A_MANIFEST, *ROUND306A_MEMBERS, R235D_MANIFEST, *R235D_MEMBERS)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def object_sha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def is_sha256(value: Any) -> bool:
    return type(value) is str and len(value) == 64 and all(ch in "0123456789abcdef" for ch in value)


def same_typed(left: Any, right: Any) -> bool:
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return set(left) == set(right) and all(same_typed(left[key], right[key]) for key in left)
    if type(left) in (list, tuple):
        return len(left) == len(right) and all(same_typed(a, b) for a, b in zip(left, right, strict=True))
    return bool(left == right)


def exact(left: Any, right: Any, label: str) -> None:
    require(same_typed(left, right), label)


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in out, "duplicate JSON key")
        out[key] = value
    return out


def reject_number(token: str) -> Any:
    raise Rejected("nonintegral/nonfinite number:" + token)


STRICT_DECODER: Final = json.JSONDecoder(
    object_pairs_hook=strict_pairs,
    parse_float=reject_number,
    parse_constant=reject_number,
)


def validate_tree(value: Any) -> None:
    if type(value) is dict:
        for key, item in value.items():
            require(type(key) is str, "JSON key type")
            validate_tree(key); validate_tree(item)
    elif type(value) is list:
        for item in value: validate_tree(item)
    elif type(value) is str:
        require("\x00" not in value and not any(0xD800 <= ord(ch) <= 0xDFFF for ch in value), "JSON string")
    else:
        require(value is None or type(value) in {bool, int}, "JSON scalar type")


def strict_json(raw: bytes, label: str, cap: int, newline: bool = False) -> Any:
    require(0 < len(raw) <= cap and not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw, "JSON raw boundary:" + label)
    body = raw
    if newline:
        require(raw.endswith(b"\n") and not raw.endswith(b"\n\n"), "JSON newline:" + label)
        body = raw[:-1]
    try:
        text = body.decode("ascii")
        value, end = STRICT_DECODER.raw_decode(text)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Rejected("JSON decode:" + label) from exc
    require(end == len(text), "JSON trailing bytes:" + label)
    validate_tree(value)
    require(canonical(value) == body, "JSON canonical bytes:" + label)
    return value


def row_bytes(row: Any, label: str) -> bytes:
    raw = canonical(row)
    require(len(raw) <= ROW_CAP, "post-decode canonical row cap:" + label)
    return raw


def verify_closed_row(row: dict[str, Any], fields: Iterable[str], label: str) -> None:
    exact(tuple(sorted(row)), tuple(sorted(fields)), "row fields:" + label)
    require(is_sha256(row.get("row_sha256")), "row digest shape:" + label)
    body = dict(row); claimed = body.pop("row_sha256")
    exact(claimed, object_sha(body), "row digest closure:" + label)
    row_bytes(row, label)


def identity(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def directory_identity(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_mode)


def hash_fd(fd: int) -> str:
    os.lseek(fd, 0, os.SEEK_SET); hasher = hashlib.sha256()
    while True:
        chunk = os.read(fd, 1_048_576)
        if not chunk: return hasher.hexdigest()
        hasher.update(chunk)


def stable_source_sha(filename: str, label: str) -> str:
    path = ROOT / filename
    before = os.stat(path, follow_symlinks=False)
    require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, label + " regular one-link")
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0))
    try:
        opened = os.fstat(fd)
        exact(identity(opened), identity(before), label + " open race")
        first = hash_fd(fd); second = hash_fd(fd)
        exact(first, second, label + " two-pass digest")
        exact(identity(os.fstat(fd)), identity(opened), label + " held identity")
        exact(identity(os.stat(path, follow_symlinks=False)), identity(opened), label + " path identity")
        return first
    finally:
        os.close(fd)


def parse_manifest(raw: bytes, expected: tuple[Pin, ...], label: str) -> None:
    try: text = raw.decode("ascii")
    except UnicodeDecodeError as exc: raise Rejected("manifest encoding:" + label) from exc
    require(text.endswith("\n"), "manifest newline:" + label)
    lines = text.splitlines()
    exact(lines, [pin.sha256 + "  " + pin.filename for pin in expected], "manifest exact ordered members:" + label)


class AuthoritySnapshot:
    def __init__(self) -> None:
        self.dirfd = -1
        self.initial: os.stat_result | None = None
        self.fds: dict[str, int] = {}
        self.ids: dict[str, tuple[int, ...]] = {}

    def __enter__(self) -> "AuthoritySnapshot":
        before = os.stat(ROOT, follow_symlinks=False)
        require(stat.S_ISDIR(before.st_mode) and not ROOT.is_symlink(), "authority directory")
        self.dirfd = os.open(ROOT, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0))
        self.initial = os.fstat(self.dirfd)
        exact(directory_identity(before), directory_identity(self.initial), "authority directory race")
        require(len(AUTHORITY_PINS) == 23 and len({pin.role for pin in AUTHORITY_PINS}) == 23, "authority pin roles")
        for pin in AUTHORITY_PINS:
            require(pin.filename == os.path.basename(pin.filename) and type(pin.size) is int and pin.size > 0 and is_sha256(pin.sha256), "pin shape:" + pin.role)
            before_file = os.stat(pin.filename, dir_fd=self.dirfd, follow_symlinks=False)
            require(stat.S_ISREG(before_file.st_mode) and before_file.st_nlink == 1 and before_file.st_size == pin.size, "pin stat:" + pin.role)
            fd = os.open(pin.filename, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0), dir_fd=self.dirfd)
            opened = os.fstat(fd); exact(identity(opened), identity(before_file), "pin open race:" + pin.role)
            one = hash_fd(fd); two = hash_fd(fd); exact(one, two, "pin two pass:" + pin.role); exact(one, pin.sha256, "pin digest:" + pin.role)
            self.fds[pin.role] = fd; self.ids[pin.role] = identity(opened)
        parse_manifest(self.read("ROUND306A_MANIFEST"), ROUND306A_MEMBERS, "Round306A")
        parse_manifest(self.read("R235D_MANIFEST"), R235D_MEMBERS, "R235D")
        return self

    def read(self, role: str) -> bytes:
        fd = self.fds[role]; os.lseek(fd, 0, os.SEEK_SET); chunks: list[bytes] = []
        while True:
            chunk = os.read(fd, 1_048_576)
            if not chunk: return b"".join(chunks)
            chunks.append(chunk)

    def final_revalidate(self) -> None:
        require(self.initial is not None, "snapshot open")
        current_dir = os.stat(ROOT, follow_symlinks=False)
        exact(directory_identity(self.initial), directory_identity(os.fstat(self.dirfd)), "held authority dir")
        exact(directory_identity(self.initial), directory_identity(current_dir), "authority dir path")
        for pin in reversed(AUTHORITY_PINS):
            held = os.fstat(self.fds[pin.role]); path = os.stat(pin.filename, dir_fd=self.dirfd, follow_symlinks=False)
            exact(identity(held), self.ids[pin.role], "held pin identity:" + pin.role)
            exact(identity(path), self.ids[pin.role], "final pin path identity:" + pin.role)
            exact(hash_fd(self.fds[pin.role]), pin.sha256, "final pin digest:" + pin.role)

    def __exit__(self, *_: Any) -> None:
        for fd in self.fds.values():
            try: os.close(fd)
            except OSError: pass
        self.fds.clear()
        if self.dirfd >= 0:
            try: os.close(self.dirfd)
            except OSError: pass
            self.dirfd = -1


class DSU:
    def __init__(self, size: int) -> None:
        require(type(size) is int and size >= 0, "DSU size")
        self.parent = list(range(size)); self.rank = [0] * size

    def find(self, item: int) -> int:
        parent = self.parent
        while parent[item] != item:
            parent[item] = parent[parent[item]]; item = parent[item]
        return item

    def union(self, left: int, right: int) -> bool:
        a, b = self.find(left), self.find(right)
        if a == b: return False
        if self.rank[a] < self.rank[b]: a, b = b, a
        self.parent[b] = a
        if self.rank[a] == self.rank[b]: self.rank[a] += 1
        return True


class SequenceCommitment:
    """Streaming SHA-256 of a canonical JSON array."""

    def __init__(self) -> None:
        self.hasher = hashlib.sha256(); self.hasher.update(b"["); self.count = 0

    def add_raw(self, raw: bytes) -> None:
        if self.count: self.hasher.update(b",")
        self.hasher.update(raw); self.count += 1

    def add(self, value: Any) -> None:
        self.add_raw(canonical(value))

    def finish(self) -> str:
        copy = self.hasher.copy(); copy.update(b"]"); return copy.hexdigest()


class GzipByteStream:
    """Single-member gzip decoder over a held descriptor."""

    def __init__(self, fd: int, label: str, require_mtime_zero: bool = False) -> None:
        self.fd = fd; self.label = label; self.buffer = bytearray(); self.done = False
        os.lseek(fd, 0, os.SEEK_SET)
        header = os.read(fd, 10); require(len(header) == 10 and header[:3] == b"\x1f\x8b\x08", "gzip header:" + label)
        require(header[3] == 0, "gzip flags:" + label)
        if require_mtime_zero: require(header[4:8] == b"\x00\x00\x00\x00", "gzip mtime:" + label)
        os.lseek(fd, 0, os.SEEK_SET)
        self.decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
        self.compressed_pending = b""

    def _pull(self) -> None:
        if self.done: return
        chunk = self.compressed_pending
        if chunk:
            self.compressed_pending = b""
        else:
            chunk = os.read(self.fd, 1_048_576)
        if chunk:
            try: plain = self.decoder.decompress(chunk, 65_536)
            except zlib.error as exc: raise Rejected("gzip decode:" + self.label) from exc
            require(not self.decoder.unused_data, "gzip extra member/trailing:" + self.label)
            self.compressed_pending = self.decoder.unconsumed_tail
            require(len(plain) <= 65_536, "bounded gzip pull:" + self.label)
            self.buffer.extend(plain)
            return
        try: final_plain = self.decoder.flush(65_536)
        except zlib.error as exc: raise Rejected("gzip flush:" + self.label) from exc
        require(len(final_plain) <= 65_536, "bounded gzip flush:" + self.label)
        self.buffer.extend(final_plain)
        require(self.decoder.eof and not self.decoder.unused_data and not self.decoder.unconsumed_tail and not self.compressed_pending, "gzip completeness:" + self.label)
        self.done = True

    def ensure(self, count: int) -> None:
        while len(self.buffer) < count and not self.done: self._pull()

    def consume(self, count: int) -> bytes:
        self.ensure(count); require(len(self.buffer) >= count, "truncated gzip plain:" + self.label)
        out = bytes(self.buffer[:count]); del self.buffer[:count]; return out

    def consume_literal(self, expected: bytes) -> None:
        exact(self.consume(len(expected)), expected, "gzip JSON literal:" + self.label)

    def json_value(self, cap: int) -> tuple[Any, bytes]:
        self.ensure(1)
        require(self.buffer[:1] in (b"{", b"["), "gzip JSON container start:" + self.label)
        position = 0
        depth = 0
        in_string = False
        escaped = False
        while True:
            while position < len(self.buffer):
                byte = self.buffer[position]
                if byte >= 0x80:
                    raise Rejected("non-ASCII gzip JSON:" + self.label)
                if in_string:
                    if escaped:
                        escaped = False
                    elif byte == 0x5C:
                        escaped = True
                    elif byte == 0x22:
                        in_string = False
                elif byte == 0x22:
                    in_string = True
                elif byte in (0x7B, 0x5B):
                    depth += 1
                elif byte in (0x7D, 0x5D):
                    depth -= 1
                    require(depth >= 0, "gzip JSON negative depth:" + self.label)
                    if depth == 0:
                        end = position + 1
                        raw = bytes(self.buffer[:end])
                        del self.buffer[:end]
                        value = strict_json(raw, "gzip JSON value:" + self.label, cap)
                        return value, raw
                position += 1
            require(len(self.buffer) <= cap, "decoded JSON value cap:" + self.label)
            if self.done:
                raise Rejected("truncated/invalid gzip JSON:" + self.label)
            self._pull()

    def remainder(self, cap: int) -> bytes:
        while not self.done:
            require(len(self.buffer) <= cap, "gzip remainder cap:" + self.label); self._pull()
        require(len(self.buffer) <= cap, "gzip remainder cap:" + self.label)
        out = bytes(self.buffer); self.buffer.clear(); return out


def gzip_plain(fd: int, label: str, cap: int, require_mtime_zero: bool = False) -> bytes:
    stream = GzipByteStream(fd, label, require_mtime_zero=require_mtime_zero)
    return stream.remainder(cap)


@dataclass(frozen=True)
class ScanReceipt:
    row_count: int
    row_ids_sha256: str
    row_hashes_sha256: str
    rows_sha256: str
    ledger_sha256: str
    schema: str
    status: str


def scan_wrapped_ledger(
    snapshot: AuthoritySnapshot,
    role: str,
    table: str,
    id_field: str,
    expected_row_schema: str,
    expected_fields: set[str],
    consume_row: Any,
) -> ScanReceipt:
    stream = GzipByteStream(snapshot.fds[role], role)
    prefix = b'{"' + table.encode("ascii") + b'":['
    stream.consume_literal(prefix)
    ids, hashes, rows = SequenceCommitment(), SequenceCommitment(), SequenceCommitment()
    payload_hash = hashlib.sha256(); payload_hash.update(prefix)
    count = 0; seen_ids: set[str] = set()
    stream.ensure(1)
    if stream.buffer[:1] != b"]":
        while True:
            if count: stream.consume_literal(b","); payload_hash.update(b",")
            row, raw = stream.json_value(ROW_CAP)
            require(type(row) is dict, "source ledger row type:" + role)
            verify_closed_row(row, expected_fields, role + ":" + str(count))
            exact(row["schema"], expected_row_schema, "source row schema:" + role)
            row_id = row[id_field]; require(type(row_id) is str and row_id not in seen_ids, "source row id:" + role)
            seen_ids.add(row_id); ids.add(row_id); hashes.add(row["row_sha256"]); rows.add_raw(raw); payload_hash.update(raw)
            consume_row(count, row); count += 1
            stream.ensure(1)
            if stream.buffer[:1] == b"]": break
            require(
                bytes(stream.buffer[:1]) == b",",
                "source row separator:" + role + ":" + str(count) + ":" + repr(bytes(stream.buffer[:8])),
            )
    stream.consume_literal(b"]"); payload_hash.update(b"]")
    suffix = stream.remainder(2_000_000)
    require(suffix.startswith(b",") and suffix.endswith(b"}"), "source ledger suffix framing:" + role)
    tail = strict_json(b"{" + suffix[1:], role + " tail", 2_000_000)
    require(type(tail) is dict and set(tail) == {"ledger_sha256","row_count","row_hashes_sha256","row_ids_sha256","rows_sha256","schema","schema_snapshot_sha256","status"}, "source ledger tail fields:" + role)
    exact(tail["row_count"], count, "source ledger row count:" + role)
    exact(tail["row_ids_sha256"], ids.finish(), "source ledger ids:" + role)
    exact(tail["row_hashes_sha256"], hashes.finish(), "source ledger hashes:" + role)
    exact(tail["rows_sha256"], rows.finish(), "source ledger rows:" + role)
    tail_payload = dict(tail); claimed_ledger = tail_payload.pop("ledger_sha256")
    canonical_tail = canonical(tail_payload)
    payload_hash.update(b","); payload_hash.update(canonical_tail[1:])
    exact(claimed_ledger, payload_hash.hexdigest(), "source ledger payload digest:" + role)
    return ScanReceipt(count, ids.finish(), hashes.finish(), rows.finish(), claimed_ledger, tail["schema"], tail["status"])


def scan_jsonl_gzip(fd: int, label: str, fields: Iterable[str], schema: str, consume_row: Any) -> dict[str, Any]:
    stream = GzipByteStream(fd, label, require_mtime_zero=True)
    ids, hashes, rows = SequenceCommitment(), SequenceCommitment(), SequenceCommitment()
    count = 0; seen: set[str] = set(); plain_hash = hashlib.sha256(); plain_size = 0
    pending = bytearray()
    while not stream.done:
        stream._pull()
        if stream.buffer:
            pending.extend(stream.buffer); stream.buffer.clear()
        while True:
            newline = pending.find(b"\n")
            if newline < 0: break
            raw = bytes(pending[:newline]); del pending[:newline + 1]
            require(0 < len(raw) <= ROW_CAP, "JSONL row cap/framing:" + label)
            row = strict_json(raw, label + ":" + str(count), ROW_CAP)
            require(type(row) is dict, "JSONL row type:" + label)
            verify_closed_row(row, fields, label + ":" + str(count)); exact(row["schema"], schema, "JSONL schema:" + label)
            row_id = row["row_id"]; require(type(row_id) is str and row_id not in seen, "JSONL row id:" + label); seen.add(row_id)
            ids.add(row_id); hashes.add(row["row_sha256"]); rows.add_raw(raw)
            line = raw + b"\n"; plain_hash.update(line); plain_size += len(line)
            consume_row(count, row); count += 1
        require(len(pending) <= ROW_CAP, "JSONL pending row cap:" + label)
    require(not pending, "JSONL final newline:" + label)
    return {"row_count":count,"row_ids_sha256":ids.finish(),"row_hashes_sha256":hashes.finish(),"rows_sha256":rows.finish(),"uncompressed_jsonl_sha256":plain_hash.hexdigest(),"uncompressed_jsonl_size":plain_size}


@dataclass(frozen=True, slots=True)
class InvalidFact:
    role: str
    member_id: str
    r235d_ordinal: int
    r235d_row_id: str
    r235d_row_sha256: str
    old_ordinal: int
    old_row_id: str
    old_wire_sha256: str
    old_row_sha256: str
    claimed_root_disposition: Mapping[str, Any]


def validate_envelope(raw: bytes, schema: str, label: str, cap: int) -> dict[str, Any]:
    doc = strict_json(raw, label, cap, newline=True)
    require(type(doc) is dict and set(doc) == {"schema","result","result_sha256"}, "envelope fields:" + label)
    exact(doc["schema"], schema, "envelope schema:" + label)
    exact(doc["result_sha256"], object_sha(doc["result"]), "envelope digest:" + label)
    return doc


def validate_r235d(snapshot: AuthoritySnapshot) -> tuple[dict[str, InvalidFact], dict[str, Any]]:
    result_doc = validate_envelope(snapshot.read("R235D_RESULT"), R235D_RESULT_SCHEMA, "R235D result", 1_000_000)
    verification_doc = validate_envelope(snapshot.read("R235D_VERIFICATION"), R235D_VERIFICATION_SCHEMA, "R235D verification", 1_000_000)
    result, verification = result_doc["result"], verification_doc["result"]
    exact(result["status"], "PASS_16_ROW_SOURCE_ONLY_LOCAL_THEOREM__OLD_R248_R306A_B0_B1G0_AF2_K2I0_K2I1_K2I2_K2I3_K2I4_BINDINGS_SUPERSEDED__FRESH_REFREEZE_REQUIRED__ZERO_GLOBAL_CREDIT", "R235D status")
    exact(verification["status"], "PASS_INDEPENDENT_16_ROW_THEOREM_AND_32_MEMBER_20_ROOT_OLD_FREEZE_INVALIDATION_REPLAY__ZERO_GLOBAL_CREDIT", "R235D verification status")
    exact(verification["producer_imported_or_executed"], False, "R235D verifier independence")
    exact(verification["independent_invalid_members"], 32, "R235D invalid member census")
    exact(verification["independent_old_root_dispositions"], 20, "R235D root census")
    exact(verification["independent_R306A_target_feature_closed_rows"], 48, "R235D closed target feature census")
    exact(verification["independent_package_wide_invalidation_claimed"], False, "R235D package scope")
    exact(verification["candidate_result_file_sha256"], R235D_MEMBERS[2].sha256, "R235D result pin in verification")
    exact(verification["candidate_ledger_sha256"], R235D_MEMBERS[1].sha256, "R235D ledger pin in verification")
    scope = result["downstream_invalidation"]["selected_pinned_artifact_invalidation_scope"]
    exact(scope["package_wide_invalidation_claimed"], False, "R235D no package-wide R248 claim")
    exact(scope["unhashed_package_members_are_not_asserted_invalid"], True, "R235D unhashed scope")
    exact(result["downstream_invalidation"]["old_freeze_invalidated"], True, "R235D old freeze invalidated")
    exact(result["downstream_invalidation"]["formal_credit"], {"corrected_member_universe":0,"corrected_DSU":0,"normalized_support":0,"physical_incidence":0,"representation_cover":0,"B1A":0,"B2":0,"maximality":0,"fibre":0,"CM2":0}, "R235D zero global credit")
    plain = gzip_plain(snapshot.fds["R235D_LEDGER"], "R235D ledger", 40_000_000, require_mtime_zero=True)
    require(plain.endswith(b"\n") and not plain.endswith(b"\n\n"), "R235D JSONL framing")
    lines = plain.splitlines(); exact(len(lines), 16, "R235D row count")
    row_sequence, conclusion_sequence = SequenceCommitment(), SequenceCommitment()
    facts: dict[str, InvalidFact] = {}; sheet_ids: list[str] = []; side_ids: list[str] = []
    sheet_owner_bindings: list[Any] = []
    bulk_owner_bindings: list[Any] = []
    for ordinal, raw in enumerate(lines):
        row = strict_json(raw, "R235D row:" + str(ordinal), ROW_CAP)
        require(type(row) is dict and row["schema"] == R235D_ROW_SCHEMA, "R235D row schema")
        exact(row["authority_ordinal"], ordinal, "R235D authority ordinal")
        nonpromotion = [row[key] for key in ("normalized_full_support_credit","physical_incidence_equivalence_credit","representation_pullback_credit","G2_authority_credit","B1A_credit","B2_credit","maximality_credit","fibre_credit","CM2_credit")]
        exact(nonpromotion, [0] * 9, "R235D row nonpromotion")
        exact(row["local_source_only_endpoint_graph_key_authority_credit"], 1, "R235D local credit")
        expected_conclusion = object_sha({"input":row["canonical_input_commitment"],"theorem":row["local_theorem"],"conclusion":row["local_conclusion"],"downstream_invalidation":row["downstream_invalidation"],"nonpromotion":[0]*9})
        exact(row["conclusion_sha256"], expected_conclusion, "R235D conclusion closure")
        row_wire_sha = hashlib.sha256(raw).hexdigest(); row_sequence.add(row_wire_sha); conclusion_sequence.add(row["conclusion_sha256"])
        binding = row["downstream_invalidation"]
        sheet_owner_bindings.append(binding["R248_target_sheet_owner_row"])
        bulk_owner_bindings.append(binding["R248_target_only_bulk_row"])
        for role, member_key, ref_key, disposition_key in (
            ("TARGET_SHEET", "invalid_TARGET_SHEET_member_id", "Round306A_invalid_TARGET_SHEET_member_row", "old_TARGET_SHEET_base_root_disposition"),
            ("TARGET_ONLY_SIDE", "invalid_TARGET_ONLY_SIDE_member_id", "Round306A_invalid_TARGET_ONLY_SIDE_member_row", "old_TARGET_ONLY_SIDE_base_root_disposition"),
        ):
            member_id, ref = binding[member_key], binding[ref_key]
            require(type(member_id) is str and member_id not in facts, "R235D invalid member uniqueness")
            require(type(ref) is list and len(ref) == 4 and type(ref[0]) is int and all(type(item) is str for item in ref[1:]), "R235D closed R306A ref")
            facts[member_id] = InvalidFact(role, member_id, ordinal, row["authority_row_id"], row_wire_sha, ref[0], ref[1], ref[2], ref[3], binding[disposition_key])
            (sheet_ids if role == "TARGET_SHEET" else side_ids).append(member_id)
    exact((len(facts),len(set(sheet_ids)),len(set(side_ids))),(32,16,16),"R235D invalid partition")
    invalid_union = sorted(facts)
    invalid_sets = result["downstream_invalidation"]["invalid_member_sets"]
    exact(invalid_sets["TARGET_SHEET"]["sorted_member_ids"], sorted(sheet_ids), "R235D sheet IDs")
    exact(invalid_sets["TARGET_ONLY_SIDE"]["sorted_member_ids"], sorted(side_ids), "R235D side IDs")
    exact(invalid_sets["UNION"]["sorted_member_ids"], invalid_union, "R235D invalid union IDs")
    exact((object_sha(sorted(sheet_ids)),object_sha(sorted(side_ids)),object_sha(invalid_union)),("0163d9c564b74b8cff5a9d5f309a25037d461b3874ca4805161cf639aeec73f4","f6f5acf3a89bb0a09f83b7f0ac783019fddc5b36ca7d8df833d6c052cc20e957","9c95eae730d5a033d65dadf2d27828b9876325e943049dd788ac1ed740687e52"),"R235D invalid commitments")
    ledger = result["authority_ledger"]
    exact((ledger["row_count"],ledger["sha256"],ledger["ordered_row_sha256_sequence_sha256"],ledger["ordered_conclusion_sha256_sequence_sha256"]),(16,R235D_MEMBERS[1].sha256,row_sequence.finish(),conclusion_sequence.finish()),"R235D ledger commitments")
    root_claim = result["downstream_invalidation"]["old_Round306A_base_root_dispositions"]
    exact((root_claim["affected_root_count"],root_claim["DELETE_ROOT_count"],root_claim["REKEY_ROOT_count"]),(20,16,4),"R235D old root dispositions")
    result["_independent_R248_target_sheet_owner_binding_sequence_sha256"] = object_sha(sheet_owner_bindings)
    result["_independent_R248_target_only_bulk_binding_sequence_sha256"] = object_sha(bulk_owner_bindings)
    return facts, result


@dataclass(frozen=True, slots=True)
class OldMember:
    member_id: str
    ordinal: int
    row_id: str
    wire_sha256: str
    row_sha256: str
    base_root_id: str
    official_key_id: str
    old_component_id: str


@dataclass(slots=True)
class RootInfo:
    old_root_id: str
    official_key_id: str
    old_component_id: str
    members: list[OldMember]


@dataclass(frozen=True, slots=True)
class RootDisposition:
    old_root_id: str
    disposition: str
    corrected_root_id: str | None
    old_member_count: int
    deleted_member_ids: tuple[str, ...]
    retained_members: tuple[OldMember, ...]
    retained_member_ids_sha256: str
    retained_source_row_sha256_sequence_sha256: str
    official_key_id: str
    old_component_id: str
    canonical_input_commitment_sha256: str


@dataclass(frozen=True, slots=True)
class EdgeInput:
    application_index: int
    old_row_id: str
    old_wire_sha256: str
    old_row_sha256: str
    source_channel: str
    source_row_id: str
    old_endpoints: tuple[str, str]
    corrected_endpoints: tuple[str, str]
    old_roots: tuple[str, str]
    corrected_roots: tuple[str, str]
    forward_rank: int


@dataclass(slots=True)
class RebuildState:
    invalid_facts: dict[str, InvalidFact]
    r235d_result: dict[str, Any]
    round306a_result: dict[str, Any]
    members: dict[str, OldMember]
    roots: dict[str, RootInfo]
    dispositions: dict[str, RootDisposition]
    corrected_roots: list[str]
    edges: list[EdgeInput]
    reverse_rank_flags: list[int]
    component_map: dict[str, str]
    component_root_sets: list[list[str]]
    component_members: dict[str, list[str]]
    edge_row_hits: Counter[str]
    projected_root_slots: Counter[str]
    occurrence_root_slots: Counter[str]
    partition_sha256: str
    forward_rank: int
    reverse_rank: int
    member_source_receipt: ScanReceipt
    edge_source_receipt: ScanReceipt


def validate_round306a_documents(snapshot: AuthoritySnapshot) -> dict[str, Any]:
    result = strict_json(snapshot.read("ROUND306A_RESULT"), "Round306A result", 100_000, newline=False)
    verification = strict_json(snapshot.read("ROUND306A_VERIFICATION"), "Round306A verification", 100_000, newline=False)
    require(type(result) is dict and type(verification) is dict, "Round306A document types")
    result_body = dict(result); result_digest = result_body.pop("result_sha256")
    exact(result_digest, object_sha(result_body), "Round306A result closure")
    verification_body = dict(verification); verification_digest = verification_body.pop("verification_sha256")
    exact(verification_digest, object_sha(verification_body), "Round306A verification closure")
    exact(verification["status"], "PASS_EXACT_CACHELESS_ROUND306A_FRESH_LEGAL_COMPONENT_DSU_REBUILD", "Round306A verification status")
    exact(verification["formal_Round306A_promotion_permitted"], True, "Round306A promotion marker")
    exact(verification["formal_credit_marker_definition"]["verification_last_and_sole_credit_marker"], True, "Round306A last credit marker")
    exact((result["member_universe"]["member_count"],result["member_universe"]["base_root_count"]),(564_492,367_964),"Round306A old universe")
    expected_replay = {"component_count":92_688,"rank_reduction":275_276,"partition_sha256":"a3f7ce1e28a956a46803ef466709ded0053633f5e104746c6d1e6e51b873e19c"}
    exact({key:result["fresh_forward_application"][key] for key in expected_replay}, expected_replay, "Round306A forward seal")
    exact({key:result["fresh_reverse_application"][key] for key in expected_replay}, expected_replay, "Round306A reverse seal")
    exact(result["fresh_forward_application"]["edge_rows"], 478_718, "Round306A edge census")
    exact(result["forward_reverse_same_partition"], True, "Round306A forward reverse marker")
    exact(result["candidate_credit_if_independently_verified"]["formal_component_quotient_credit"], 1, "Round306A credited component quotient")
    exact(
        verification["exact_fresh_DSU_census"],
        {
            "base_root_count": 367_964,
            "forward_reverse_same_partition": True,
            "fresh_component_count": 92_688,
            "fresh_partition_sha256": "a3f7ce1e28a956a46803ef466709ded0053633f5e104746c6d1e6e51b873e19c",
            "fresh_rank_reduction_count": 275_276,
            "legal_edge_application_count": 478_718,
            "member_count": 564_492,
            "serialized_Round304_partition_used_as_state": False,
        },
        "Round306A verification exact census",
    )
    zero_credit = result["formal_credit_without_independent_verification_marker"]
    require(type(zero_credit) is dict and len(zero_credit) > 0, "Round306A zero-credit object")
    for key, value in zero_credit.items():
        require(type(key) is str and type(value) is int and value == 0, "Round306A candidate zero credit")
    return result


def rekey_input(
    old_root: str,
    old_count: int,
    deleted: tuple[str, ...],
    retained: tuple[OldMember, ...],
    retained_ids_sha: str,
    retained_row_sha_sequence_sha: str,
    official_key: str,
) -> dict[str, Any]:
    return {
        "schema":"cm2.round306c0.corrected-base-root-rekey-input.v1",
        "old_base_root_id":old_root,
        "old_member_count":old_count,
        "deleted_member_ids":list(deleted),
        "deleted_member_count":len(deleted),
        "retained_member_count":len(retained),
        "retained_member_ids_sha256":retained_ids_sha,
        "retained_source_row_sha256_sequence_sha256":retained_row_sha_sequence_sha,
        "official_key_id":official_key,
    }


def rebuild_state(snapshot: AuthoritySnapshot) -> RebuildState:
    invalid_facts, r235d_result = validate_r235d(snapshot)
    round306a_result = validate_round306a_documents(snapshot)
    members: dict[str, OldMember] = {}; roots: dict[str, RootInfo] = {}
    last_member = ""

    def consume_member(ordinal: int, row: dict[str, Any]) -> None:
        nonlocal last_member
        exact((row["member_identity_preserved"],row["formal_maximality_credit"],row["formal_fibre_credit"],row["formal_global_disposition_credit"]),(True,0,0,0),"old member credit boundary")
        member_id = sys.intern(row["registry_occurrence_id"]); require(member_id > last_member and member_id not in members, "old member strict order")
        last_member = member_id
        old = OldMember(
            member_id,
            ordinal,
            row["Round306A_fresh_member_component_row_id"],
            hashlib.sha256(canonical(row)).hexdigest(),
            row["row_sha256"],
            sys.intern(row["base_root_id"]),
            sys.intern(row["official_key_id"]),
            sys.intern(row["final_component_id"]),
        )
        members[member_id] = old
        root = roots.get(old.base_root_id)
        if root is None:
            roots[old.base_root_id] = RootInfo(old.base_root_id,old.official_key_id,old.old_component_id,[old])
        else:
            exact((root.official_key_id,root.old_component_id),(old.official_key_id,old.old_component_id),"old root key/component consistency")
            root.members.append(old)
        fact = invalid_facts.get(member_id)
        if fact is not None:
            exact((fact.old_ordinal,fact.old_row_id,fact.old_wire_sha256,fact.old_row_sha256),(ordinal,old.row_id,hashlib.sha256(row_bytes(row,"old member ref")).hexdigest(),old.row_sha256),"R235D/Round306A invalid member closed join")

    member_receipt = scan_wrapped_ledger(snapshot,"ROUND306A_MEMBER_LEDGER","fresh_member_component_rows","Round306A_fresh_member_component_row_id",OLD_MEMBER_SCHEMA,OLD_MEMBER_FIELDS,consume_member)
    exact(member_receipt.row_count,564_492,"old member ledger count"); exact(len(members),564_492,"old distinct members"); exact(len(roots),367_964,"old roots")
    source_member_meta = round306a_result["output_ledgers"]["member"]
    exact((member_receipt.row_count,member_receipt.row_ids_sha256,member_receipt.row_hashes_sha256,member_receipt.rows_sha256,member_receipt.ledger_sha256),(source_member_meta["row_count"],source_member_meta["row_ids_sha256"],source_member_meta["row_hashes_sha256"],source_member_meta["rows_sha256"],source_member_meta["ledger_sha256"]),"old member result commitments")
    exact(set(invalid_facts).issubset(members),True,"all invalid members joined")

    invalid_by_root: dict[str, list[str]] = defaultdict(list)
    for member_id in invalid_facts: invalid_by_root[members[member_id].base_root_id].append(member_id)
    dispositions: dict[str, RootDisposition] = {}
    histogram: Counter[str] = Counter()
    for old_root in sorted(roots):
        info = roots[old_root]; info.members.sort(key=lambda item:item.member_id)
        deleted = tuple(sorted(invalid_by_root.get(old_root,[])))
        retained = tuple(item for item in info.members if item.member_id not in invalid_facts)
        retained_ids_sha = object_sha([item.member_id for item in retained])
        retained_rows_sha = object_sha([item.row_sha256 for item in retained])
        if not retained:
            disposition, corrected = "DELETE_ROOT", None
        elif deleted:
            disposition = "REKEY_ROOT"
            commitment = rekey_input(old_root,len(info.members),deleted,retained,retained_ids_sha,retained_rows_sha,info.official_key_id)
            corrected = CORRECTED_ROOT_NAMESPACE + object_sha(commitment)
        else:
            disposition, corrected = "KEEP_ROOT", old_root
        canonical_input = {
            "schema":SCHEMA + ".base-root-disposition-input.v1",
            "old_base_root_id":old_root,
            "disposition": disposition,
            "old_component_id": info.old_component_id,
            "old_member_count":len(info.members),
            "deleted_member_ids":list(deleted),
            "deleted_member_count": len(deleted),
            "deleted_member_ids_sha256": object_sha(list(deleted)),
            "retained_member_count": len(retained),
            "retained_member_ids_sha256":retained_ids_sha,
            "retained_source_row_sha256_sequence_sha256":retained_rows_sha,
            "official_key_id":info.official_key_id,
        }
        dispositions[old_root] = RootDisposition(old_root,disposition,corrected,len(info.members),deleted,retained,retained_ids_sha,retained_rows_sha,info.official_key_id,info.old_component_id,object_sha(canonical_input))
        histogram[disposition] += 1
    exact(dict(histogram),{"KEEP_ROOT":367_944,"DELETE_ROOT":16,"REKEY_ROOT":4},"root disposition histogram")
    corrected_roots = sorted(item.corrected_root_id for item in dispositions.values() if item.corrected_root_id is not None)
    exact((len(corrected_roots),len(set(corrected_roots))),(367_948,367_948),"corrected roots exact cover")
    keep_targets = {old for old,item in dispositions.items() if item.disposition=="KEEP_ROOT"}
    rekey_targets = {item.corrected_root_id for item in dispositions.values() if item.disposition=="REKEY_ROOT"}
    require(not keep_targets & rekey_targets and len(rekey_targets)==4,"fresh injective rekey targets")
    for member_id,fact in invalid_facts.items():
        root = members[member_id].base_root_id; actual = dispositions[root]; claim = fact.claimed_root_disposition
        exact((claim["old_base_root_id"],claim["old_member_count"],claim["invalid_member_ids"],claim["invalid_member_count"],claim["required_disposition"]),(root,actual.old_member_count,list(actual.deleted_member_ids),len(actual.deleted_member_ids),actual.disposition),"R235D root claim against complete member cover")

    root_index = {root:index for index,root in enumerate(corrected_roots)}
    forward_dsu = DSU(len(corrected_roots)); edges: list[EdgeInput] = []
    edge_hits: Counter[str] = Counter(); projected_slots: Counter[str] = Counter(); occurrence_slots: Counter[str] = Counter()
    forward_rank = 0; self_cycle_indices: list[int] = []

    def consume_edge(ordinal: int, row: dict[str, Any]) -> None:
        nonlocal forward_rank
        exact(row["application_index"],ordinal,"old edge exact order")
        exact((row["fed_to_new_empty_DSU"],row["serialized_Round304_partition_used_as_state"],row["formal_credit_without_independent_verification_marker"],row["formal_maximality_credit"],row["formal_fibre_credit"],row["formal_global_disposition_credit"]),(True,False,0,0,0,0),"old edge boundary")
        require(type(row["forward_rank_reduction"]) is int and row["forward_rank_reduction"] in {0,1},"old forward rank type")
        exact(row["candidate_DSU_rank_reduction"],row["forward_rank_reduction"],"old candidate rank flag")
        exact(row["forward_cycle_or_redundant"],1-row["forward_rank_reduction"],"old cycle flag")
        endpoints = row["canonical_occurrence_endpoint_pair"]
        require(type(endpoints) is list and len(endpoints)==2 and endpoints==sorted(endpoints) and endpoints[0]!=endpoints[1],"old occurrence pair")
        require(all(endpoint in members or endpoint in dispositions for endpoint in endpoints),"old occurrence endpoint cover")
        require(endpoints[0] not in invalid_facts and endpoints[1] not in invalid_facts,"invalid member occurrence endpoint hit")
        old_roots = sorted([endpoint if endpoint in dispositions else members[endpoint].base_root_id for endpoint in endpoints])
        exact(row["projected_base_root_pair"],old_roots,"old edge root projection")
        mapped = [dispositions[root].corrected_root_id for root in old_roots]
        require(all(type(root) is str for root in mapped),"delete root edge hit")
        corrected_pair = sorted(mapped)  # type: ignore[arg-type]
        require(not distinct_remap_collision(old_roots,corrected_pair),"distinct root remap collision")
        corrected_endpoints = sorted([
            dispositions[endpoint].corrected_root_id if endpoint in dispositions else endpoint
            for endpoint in endpoints
        ])
        require(all(type(endpoint) is str for endpoint in corrected_endpoints) and corrected_endpoints[0] != corrected_endpoints[1],"corrected occurrence endpoint pair")
        reduced = forward_dsu.union(root_index[corrected_pair[0]],root_index[corrected_pair[1]])
        exact(int(reduced),row["forward_rank_reduction"],"old/new forward rank transcript")
        forward_rank += int(reduced)
        if old_roots[0] == old_roots[1]: self_cycle_indices.append(ordinal)
        row_root_hits = set(old_roots)
        for root in old_roots: projected_slots[root] += 1
        for endpoint in endpoints:
            if endpoint in dispositions:
                require(type(dispositions[endpoint].corrected_root_id) is str,"exact occurrence corrected root")
                occurrence_slots[endpoint] += 1
                row_root_hits.add(endpoint)
        for root in row_root_hits: edge_hits[root] += 1
        edges.append(EdgeInput(
            ordinal,
            row["Round306A_fresh_edge_application_row_id"],
            hashlib.sha256(canonical(row)).hexdigest(),
            row["row_sha256"],
            row["source_channel"],
            row["source_row_id"],
            (endpoints[0], endpoints[1]),
            (corrected_endpoints[0], corrected_endpoints[1]),
            (old_roots[0], old_roots[1]),
            (corrected_pair[0], corrected_pair[1]),
            int(reduced),
        ))

    edge_receipt = scan_wrapped_ledger(snapshot,"ROUND306A_EDGE_LEDGER","fresh_edge_application_rows","Round306A_fresh_edge_application_row_id",OLD_EDGE_SCHEMA,OLD_EDGE_FIELDS,consume_edge)
    exact(edge_receipt.row_count,478_718,"old edge ledger count")
    source_edge_meta = round306a_result["output_ledgers"]["edge"]
    exact((edge_receipt.row_count,edge_receipt.row_ids_sha256,edge_receipt.row_hashes_sha256,edge_receipt.rows_sha256,edge_receipt.ledger_sha256),(source_edge_meta["row_count"],source_edge_meta["row_ids_sha256"],source_edge_meta["row_hashes_sha256"],source_edge_meta["rows_sha256"],source_edge_meta["ledger_sha256"]),"old edge result commitments")
    exact((forward_rank,len(self_cycle_indices),object_sha(self_cycle_indices)),(275_276,15_932,"a391791492f3c871f67dd652c7183f7c14e2f006a70a82d380e178479ace943c"),"corrected forward/self-cycle census")
    for item in dispositions.values():
        if item.disposition == "DELETE_ROOT":
            exact((edge_hits[item.old_root_id],projected_slots[item.old_root_id],occurrence_slots[item.old_root_id]),(0,0,0),"delete root zero edge/occurrence hits")
        elif item.disposition == "REKEY_ROOT":
            exact((edge_hits[item.old_root_id],projected_slots[item.old_root_id],occurrence_slots[item.old_root_id]),(336,518,96),"rekey edge/projected/exact-occurrence hits")
    reverse_dsu = DSU(len(corrected_roots)); reverse_flags = [0] * len(edges); reverse_rank = 0
    for reverse_index, edge in enumerate(reversed(edges)):
        reduced = reverse_dsu.union(root_index[edge.corrected_roots[0]],root_index[edge.corrected_roots[1]])
        reverse_flags[edge.application_index] = int(reduced); reverse_rank += int(reduced)
        exact(len(edges)-1-edge.application_index,reverse_index,"reverse application index")
    forward_map, forward_sets, partition_sha = component_mapping(forward_dsu,corrected_roots)
    reverse_map, reverse_sets, reverse_sha = component_mapping(reverse_dsu,corrected_roots)
    exact((forward_rank,reverse_rank,len(forward_sets),partition_sha),(275_276,275_276,92_672,"1ae914d4e2cff22d1fa6ddad4ffe4679c594bde3cdad27acf1480202b7a89434"),"fresh C0 DSU census")
    exact((reverse_sets,reverse_sha),(forward_sets,partition_sha),"fresh forward/reverse partition")
    del reverse_map
    component_members: dict[str,list[str]] = defaultdict(list)
    for member_id,member in members.items():
        if member_id in invalid_facts: continue
        corrected_root = dispositions[member.base_root_id].corrected_root_id
        require(type(corrected_root) is str,"surviving corrected root")
        component_members[forward_map[corrected_root]].append(member_id)
    for values in component_members.values(): values.sort()
    exact((sum(map(len,component_members.values())),len(component_members)),(564_460,92_672),"corrected component member cover")
    sizes = [len(values) for values in component_members.values()]
    square_sum = sum(size*size for size in sizes); all_pairs = 564_460*564_459//2; within = sum(size*(size-1)//2 for size in sizes); cross = all_pairs-within
    exact((square_sum,all_pairs,within,cross),(974_874_492,159_307_263_570,487_155_016,158_820_108_554),"corrected pair arithmetic")
    old_component_sizes: Counter[str] = Counter(member.old_component_id for member in members.values())
    old_square_sum = sum(size * size for size in old_component_sizes.values())
    old_all_pairs = 564_492 * 564_491 // 2
    old_within = sum(size * (size - 1) // 2 for size in old_component_sizes.values())
    old_cross = old_all_pairs - old_within
    exact(
        (len(old_component_sizes), old_square_sum, old_all_pairs, old_within, old_cross),
        (92_688, 975_049_356, 159_325_326_786, 487_242_432, 158_838_084_354),
        "old component pair arithmetic",
    )
    exact(
        (old_all_pairs - all_pairs, old_within - within, old_cross - cross),
        (18_063_216, 87_416, 17_975_800),
        "data-derived pair arithmetic deltas",
    )
    affected_components = {members[member].old_component_id for member in invalid_facts}
    corrected_old_component_sizes = Counter(
        member.old_component_id
        for member_id, member in members.items()
        if member_id not in invalid_facts
    )
    vanished_components = sorted(
        component for component in affected_components
        if corrected_old_component_sizes[component] == 0
    )
    retained_components = sorted(
        component for component in affected_components
        if corrected_old_component_sizes[component] > 0
    )
    exact(len(affected_components), 20, "affected old component count")
    exact(len(vanished_components), 16, "vanished singleton component count")
    exact(
        sorted(old_component_sizes[component] for component in vanished_components),
        [1] * 16,
        "vanished singleton old sizes",
    )
    exact(
        sorted(corrected_old_component_sizes[component] for component in vanished_components),
        [0] * 16,
        "vanished singleton corrected sizes",
    )
    exact(len(retained_components), 4, "retained affected component count")
    exact(
        sorted(old_component_sizes[component] for component in retained_components),
        [5_442, 5_442, 5_490, 5_490],
        "retained affected old sizes",
    )
    affected_old_roots = {
        members[member_id].base_root_id for member_id in invalid_facts
    }
    rekey_corrected_roots = sorted(
        disposition.corrected_root_id
        for old_root, disposition in dispositions.items()
        if old_root in affected_old_roots and disposition.disposition == "REKEY_ROOT"
    )
    require(all(type(root) is str for root in rekey_corrected_roots), "rekey corrected roots")
    rekey_fresh_components = {
        forward_map[root] for root in rekey_corrected_roots
    }
    exact(len(rekey_fresh_components), 4, "distinct rekey fresh component count")
    exact(
        sorted(len(component_members[component]) for component in rekey_fresh_components),
        [5_438, 5_438, 5_486, 5_486],
        "retained affected fresh component sizes",
    )
    return RebuildState(invalid_facts,r235d_result,round306a_result,members,roots,dispositions,corrected_roots,edges,reverse_flags,forward_map,forward_sets,dict(component_members),edge_hits,projected_slots,occurrence_slots,partition_sha,forward_rank,reverse_rank,member_receipt,edge_receipt)


def component_mapping(dsu: DSU, roots: list[str]) -> tuple[dict[str, str], list[list[str]], str]:
    groups: dict[int, list[str]] = defaultdict(list)
    for index, root in enumerate(roots): groups[dsu.find(index)].append(root)
    sets = sorted(sorted(group) for group in groups.values())
    mapping: dict[str, str] = {}
    for group in sets:
        component_id = COMPONENT_NAMESPACE + object_sha(group)
        for root in group:
            mapping[root] = component_id
    return mapping, sets, object_sha(sets)


def distinct_remap_collision(old_pair: list[str], corrected_pair: list[str]) -> bool:
    require(type(old_pair) is list and type(corrected_pair) is list and len(old_pair) == len(corrected_pair) == 2, "root pair shape")
    require(all(type(item) is str for item in old_pair + corrected_pair), "root pair types")
    return old_pair[0] != old_pair[1] and corrected_pair[0] == corrected_pair[1]


def make_row(kind: str, payload: dict[str, Any]) -> dict[str, Any]:
    require(kind in ROW_FIELDS and "row_id" not in payload and "row_sha256" not in payload, "row construction:" + kind)
    core = {"schema": ROW_SCHEMAS[kind], **payload}
    row = {"schema": ROW_SCHEMAS[kind], "row_id": ROW_ID_NAMESPACES[kind] + object_sha(core), **payload}
    row["row_sha256"] = object_sha(row)
    verify_closed_row(row, ROW_FIELDS[kind], "generated:" + kind)
    return row


def schema_snapshot() -> dict[str, Any]:
    return {
        "schema": SCHEMA + ".schema-snapshot.v1",
        "output_files": OUTPUTS,
        "output_order": list(OUTPUT_ORDER),
        "row_schemas": ROW_SCHEMAS,
        "row_fields": {key: list(value) for key, value in ROW_FIELDS.items()},
        "row_id_namespaces": ROW_ID_NAMESPACES,
        "row_id_derivation": "namespace+sha256(canonical_json({schema,...core_without_row_id_or_row_sha256}))",
        "row_sha256_derivation": "sha256(canonical_json(row_without_row_sha256))",
        "jsonl_ledger_serialization": "one canonical ASCII JSON row plus LF; gzip level 9; mtime 0; empty filename; single member",
        "corrected_root_derivation": {
            "KEEP_ROOT": "corrected_base_root_id=old_base_root_id",
            "DELETE_ROOT": "corrected_base_root_id_or_null=null",
            "REKEY_ROOT": "round306c0-corrected-base-root:+sha256(canonical_json(rekey_input))",
            "rekey_input_schema": "cm2.round306c0.corrected-base-root-rekey-input.v1",
            "rekey_input_fields": [
                "schema", "old_base_root_id", "old_member_count",
                "deleted_member_ids", "deleted_member_count",
                "retained_member_count", "retained_member_ids_sha256",
                "retained_source_row_sha256_sequence_sha256", "official_key_id",
            ],
        },
        "base_root_disposition_input_commitment": {
            "uniform_for_KEEP_DELETE_REKEY": True,
            "schema": SCHEMA + ".base-root-disposition-input.v1",
            "fields": [
                "schema", "old_base_root_id", "disposition",
                "old_component_id", "old_member_count", "deleted_member_ids",
                "deleted_member_count", "deleted_member_ids_sha256",
                "retained_member_count", "retained_member_ids_sha256",
                "retained_source_row_sha256_sequence_sha256", "official_key_id",
            ],
            "REKEY_corrected_root_id_uses_separate_strict_rekey_input": True,
        },
        "component_id_derivation": "round306c0-fresh-legal-component:+sha256(canonical_json(sorted_corrected_root_ids))",
        "formal_credit_rule": "all producer artifacts are zero credit; independent verification is last and sole marker",
    }


def expected_rows(state: RebuildState, kind: str) -> Iterator[dict[str, Any]]:
    if kind == "member_invalidation":
        for fact in sorted(state.invalid_facts.values(), key=lambda item: (item.member_id, item.role)):
            member = state.members[fact.member_id]
            yield make_row(kind, {
                "invalidation_role": fact.role,
                "registry_member_id": fact.member_id,
                "source_R235D_authority_ordinal": fact.r235d_ordinal,
                "source_R235D_invalidation_row_id": fact.r235d_row_id,
                "source_R235D_invalidation_row_sha256": fact.r235d_row_sha256,
                "source_Round306A_member_row_ordinal": member.ordinal,
                "source_Round306A_member_row_id": member.row_id,
                "source_Round306A_member_row_wire_sha256": member.wire_sha256,
                "source_Round306A_member_row_sha256": member.row_sha256,
                "old_base_root_id": member.base_root_id,
                "old_component_id": member.old_component_id,
                "formal_R248_correction_overlay_credit_without_independent_verification_marker": 0,
            })
        return
    if kind == "root_disposition":
        for old_root in sorted(state.dispositions):
            item = state.dispositions[old_root]
            yield make_row(kind, {
                "old_base_root_id": old_root,
                "disposition": item.disposition,
                "old_member_count": item.old_member_count,
                "deleted_member_count": len(item.deleted_member_ids),
                "deleted_member_ids": list(item.deleted_member_ids),
                "deleted_member_ids_sha256": object_sha(list(item.deleted_member_ids)),
                "retained_member_count": len(item.retained_members),
                "retained_member_ids_sha256": item.retained_member_ids_sha256,
                "retained_source_row_sha256_sequence_sha256": item.retained_source_row_sha256_sequence_sha256,
                "official_key_id": item.official_key_id,
                "canonical_input_commitment_sha256": item.canonical_input_commitment_sha256,
                "corrected_base_root_id_or_null": item.corrected_root_id,
                "old_component_id": item.old_component_id,
                "candidate_complete_selected_row_R248_correction_overlay": True,
                "formal_corrected_root_credit_without_independent_verification_marker": 0,
            })
        return
    if kind == "edge_remap":
        for edge in state.edges:
            delete_hits = sum(
                state.dispositions[item].disposition == "DELETE_ROOT"
                for item in (*edge.old_endpoints, *edge.old_roots)
                if item in state.dispositions
            )
            invalid_hits = sum(item in state.invalid_facts for item in edge.old_endpoints)
            yield make_row(kind, {
                "application_index": edge.application_index,
                "source_Round306A_row_id": edge.old_row_id,
                "source_Round306A_row_wire_sha256": edge.old_wire_sha256,
                "source_Round306A_row_sha256": edge.old_row_sha256,
                "source_channel": edge.source_channel,
                "source_row_id": edge.source_row_id,
                "old_canonical_occurrence_endpoint_pair": list(edge.old_endpoints),
                "corrected_canonical_occurrence_endpoint_pair": list(edge.corrected_endpoints),
                "old_projected_base_root_pair": list(edge.old_roots),
                "corrected_projected_base_root_pair": list(edge.corrected_roots),
                "delete_root_hit_count": delete_hits,
                "invalid_member_endpoint_hit_count": invalid_hits,
                "distinct_root_remap_collision": distinct_remap_collision(list(edge.old_roots), list(edge.corrected_roots)),
                "forward_rank_reduction": edge.forward_rank,
                "old_forward_rank_flag_match": True,
                "reverse_application_index": len(state.edges) - 1 - edge.application_index,
                "reverse_rank_reduction": state.reverse_rank_flags[edge.application_index],
                "formal_corrected_DSU_credit_without_independent_verification_marker": 0,
            })
        return
    if kind == "member_component":
        for member_id in sorted(state.members):
            if member_id in state.invalid_facts:
                continue
            member = state.members[member_id]
            disposition = state.dispositions[member.base_root_id]
            corrected_root = disposition.corrected_root_id
            require(type(corrected_root) is str, "expected member corrected root")
            yield make_row(kind, {
                "registry_member_id": member_id,
                "source_Round306A_row_ordinal": member.ordinal,
                "source_Round306A_row_id": member.row_id,
                "source_Round306A_row_wire_sha256": member.wire_sha256,
                "source_Round306A_row_sha256": member.row_sha256,
                "old_base_root_id": member.base_root_id,
                "corrected_base_root_id": corrected_root,
                "root_disposition": disposition.disposition,
                "official_key_id": member.official_key_id,
                "corrected_component_id": state.component_map[corrected_root],
                "member_identity_preserved": True,
                "formal_corrected_member_universe_credit_without_independent_verification_marker": 0,
                "formal_corrected_DSU_credit_without_independent_verification_marker": 0,
            })
        return
    if kind == "base_root_component":
        old_by_corrected = {
            item.corrected_root_id: old_root
            for old_root, item in state.dispositions.items()
            if item.corrected_root_id is not None
        }
        for corrected_root in state.corrected_roots:
            old_root = old_by_corrected[corrected_root]
            item = state.dispositions[old_root]
            retained_ids = [member.member_id for member in item.retained_members]
            yield make_row(kind, {
                "corrected_base_root_id": corrected_root,
                "old_base_root_id": old_root,
                "root_disposition": item.disposition,
                "member_count": len(retained_ids),
                "member_ids_sha256": object_sha(retained_ids),
                "official_key_id": item.official_key_id,
                "corrected_component_id": state.component_map[corrected_root],
                "edge_row_hit_count": state.edge_row_hits[old_root],
                "projected_root_slot_hit_count": state.projected_root_slots[old_root],
                "exact_occurrence_root_slot_hit_count": state.occurrence_root_slots[old_root],
                "formal_corrected_DSU_credit_without_independent_verification_marker": 0,
            })
        return
    if kind == "component_census":
        roots_by_component = {
            COMPONENT_NAMESPACE + object_sha(roots): roots
            for roots in state.component_root_sets
        }
        exact(set(roots_by_component), set(state.component_members), "expected component cover")
        for component_id in sorted(roots_by_component):
            roots = roots_by_component[component_id]
            members = state.component_members[component_id]
            yield make_row(kind, {
                "corrected_component_id": component_id,
                "base_root_count": len(roots),
                "base_root_ids_sha256": object_sha(roots),
                "member_count": len(members),
                "member_ids_sha256": object_sha(members),
                "formal_corrected_DSU_credit_without_independent_verification_marker": 0,
            })
        return
    raise Rejected("unknown expected ledger kind:" + kind)


class CandidateSnapshot:
    def __init__(self, path: Path) -> None:
        self.path = Path(os.path.abspath(os.fspath(path)))
        self.dirfd = -1
        self.initial: tuple[int, ...] | None = None
        self.fds: dict[str, int] = {}
        self.ids: dict[str, tuple[int, ...]] = {}
        self.hashes: dict[str, str] = {}

    def __enter__(self) -> "CandidateSnapshot":
        deliverables = ROOT.resolve(strict=True)
        require(
            os.path.commonpath((os.fspath(self.path), os.fspath(deliverables)))
            != os.fspath(deliverables),
            "candidate outside deliverables",
        )
        before = os.stat(self.path, follow_symlinks=False)
        require(stat.S_ISDIR(before.st_mode), "candidate directory")
        self.dirfd = os.open(
            self.path,
            os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
            | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0),
        )
        opened = os.fstat(self.dirfd)
        exact(directory_identity(before), directory_identity(opened), "candidate directory race")
        self.initial = directory_identity(opened)
        exact(set(os.listdir(self.dirfd)), set(OUTPUTS.values()), "candidate exact file set")
        for role in OUTPUT_ORDER:
            filename = OUTPUTS[role]
            before_file = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
            require(stat.S_ISREG(before_file.st_mode) and before_file.st_nlink == 1, "candidate regular one-link:" + role)
            fd = os.open(
                filename,
                os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0),
                dir_fd=self.dirfd,
            )
            opened_file = os.fstat(fd)
            exact(identity(opened_file), identity(before_file), "candidate open race:" + role)
            first = hash_fd(fd); second = hash_fd(fd)
            exact(first, second, "candidate two-pass digest:" + role)
            self.fds[role] = fd
            self.ids[role] = identity(opened_file)
            self.hashes[role] = first
        return self

    def read(self, role: str) -> bytes:
        fd = self.fds[role]; os.lseek(fd, 0, os.SEEK_SET)
        chunks: list[bytes] = []
        while True:
            chunk = os.read(fd, 1_048_576)
            if not chunk: return b"".join(chunks)
            chunks.append(chunk)

    def final_revalidate(self) -> None:
        require(self.initial is not None, "candidate snapshot open")
        exact(directory_identity(os.fstat(self.dirfd)), self.initial, "held candidate directory")
        exact(directory_identity(os.stat(self.path, follow_symlinks=False)), self.initial, "candidate directory path")
        for role in reversed(OUTPUT_ORDER):
            current = os.stat(OUTPUTS[role], dir_fd=self.dirfd, follow_symlinks=False)
            exact(identity(current), self.ids[role], "candidate final path identity:" + role)
            exact(identity(os.fstat(self.fds[role])), self.ids[role], "candidate held identity:" + role)
            exact(hash_fd(self.fds[role]), self.hashes[role], "candidate final digest:" + role)

    def __exit__(self, *_: Any) -> None:
        for fd in self.fds.values():
            try: os.close(fd)
            except OSError: pass
        if self.dirfd >= 0:
            try: os.close(self.dirfd)
            except OSError: pass


def verify_candidate(state: RebuildState, candidate_path: Path) -> dict[str, Any]:
    with CandidateSnapshot(candidate_path) as candidate:
        authority = strict_json(candidate.read("authority_frontier"), "candidate authority frontier", ROW_CAP)
        pair = strict_json(candidate.read("pair_denominator"), "candidate pair denominator", ROW_CAP)
        result = strict_json(candidate.read("result"), "candidate result", ROW_CAP)
        for document, field, label in (
            (authority, "authority_frontier_sha256", "authority frontier"),
            (pair, "pair_denominator_sha256", "pair denominator"),
            (result, "result_sha256", "result"),
        ):
            require(type(document) is dict and is_sha256(document.get(field)), "candidate self hash:" + label)
            body = dict(document); claimed = body.pop(field)
            exact(claimed, object_sha(body), "candidate document closure:" + label)

        producer_path = ROOT / PRODUCER_NAME
        producer_info = os.stat(producer_path, follow_symlinks=False)
        require(stat.S_ISREG(producer_info.st_mode) and producer_info.st_nlink == 1, "candidate producer source identity")
        producer_fd = os.open(producer_path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0))
        try: producer_sha = hash_fd(producer_fd)
        finally: os.close(producer_fd)
        exact(authority["producer_file_sha256"], producer_sha, "authority producer pin")
        exact(result["producer_file_sha256"], producer_sha, "result producer pin")
        frontier = authority["r235d_frontier"]
        exact(
            frontier["R248_target_sheet_owner_binding_sequence_sha256"],
            state.r235d_result["_independent_R248_target_sheet_owner_binding_sequence_sha256"],
            "independent R248 sheet owner binding commitment",
        )
        exact(
            frontier["R248_target_only_bulk_binding_sequence_sha256"],
            state.r235d_result["_independent_R248_target_only_bulk_binding_sequence_sha256"],
            "independent R248 bulk owner binding commitment",
        )
        exact(
            (pair["corrected_member_count"], pair["corrected_component_count"], pair["all_unordered_member_pairs"], pair["within_component_unordered_member_pairs"], pair["cross_component_pair_denominator"]),
            (564_460, 92_672, 159_307_263_570, 487_155_016, 158_820_108_554),
            "candidate pair arithmetic",
        )
        exact(result["fresh_forward_application"]["partition_sha256"], state.partition_sha256, "candidate forward partition")
        exact(result["fresh_reverse_application"]["partition_sha256"], state.partition_sha256, "candidate reverse partition")
        exact(result["affected_component_census"]["deleted_singleton_old_to_corrected_sizes"], [[1, 0]] * 16, "candidate delete transitions")
        exact(result["affected_component_census"]["surviving_rekey_corrected_member_sizes"], [5_438, 5_438, 5_486, 5_486], "candidate rekey fresh sizes")
        require(all(type(value) is int and value == 0 for value in result["formal_credit_without_independent_verification_marker"].values()), "candidate zero-credit boundary")
        descriptors = result["output_artifacts_in_publication_order_before_result"]
        exact([item["role"] for item in descriptors], list(OUTPUT_ORDER[:-1]), "candidate descriptor order")
        for item in descriptors:
            role = item["role"]
            exact(item["filename"], OUTPUTS[role], "candidate descriptor filename:" + role)
            exact(item["size"], candidate.ids[role][4], "candidate descriptor size:" + role)
            exact(item["sha256"], candidate.hashes[role], "candidate descriptor digest:" + role)

        ledger_receipts: dict[str, dict[str, Any]] = {}
        for kind in ROW_FIELDS:
            expected = iter(expected_rows(state, kind))
            def consume(ordinal: int, row: dict[str, Any], *, _expected: Iterator[dict[str, Any]] = expected, _kind: str = kind) -> None:
                try:
                    wanted = next(_expected)
                except StopIteration as exc:
                    raise Rejected("candidate extra row:" + _kind) from exc
                exact(row, wanted, "candidate row:" + _kind + ":" + str(ordinal))
            receipt = scan_jsonl_gzip(
                candidate.fds[kind], "candidate:" + kind,
                ROW_FIELDS[kind], ROW_SCHEMAS[kind], consume,
            )
            exact(receipt["row_count"], LEDGER_ROW_COUNTS[kind], "candidate row count:" + kind)
            try:
                next(expected)
            except StopIteration:
                pass
            else:
                raise Rejected("candidate missing row:" + kind)
            ledger_receipts[kind] = receipt
        candidate.final_revalidate()
        return {
            "status": "PASS_INDEPENDENT_C0_CANDIDATE_FULL_ROW_COMPARATOR__ZERO_GLOBAL_CREDIT",
            "artifact_count": 9,
            "candidate_artifact_sha256": {role: candidate.hashes[role] for role in OUTPUT_ORDER},
            "ledger_receipts": ledger_receipts,
            "corrected_partition_sha256": state.partition_sha256,
            "corrected_member_count": 564_460,
            "corrected_component_count": 92_672,
            "cross_component_pair_denominator": 158_820_108_554,
            "producer_or_upstream_producer_or_verifier_imported_or_executed": False,
            "formal_credit": {"corrected_DSU": 0, "B1A": 0, "B2": 0, "CM2": 0},
        }


def clone_candidate(source: Path, parent: Path) -> Path:
    path = Path(tempfile.mkdtemp(prefix="attack.", dir=parent))
    for role in OUTPUT_ORDER:
        source_fd = os.open(source / OUTPUTS[role], os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        target_fd = os.open(path / OUTPUTS[role], os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        try:
            while True:
                copied = os.copy_file_range(source_fd, target_fd, 8_388_608)
                if copied == 0:
                    break
        finally:
            os.close(target_fd)
            os.close(source_fd)
    return path


def remove_tree(path: Path) -> None:
    if path.is_symlink():
        path.unlink()
        return
    for entry in path.iterdir():
        entry.unlink()
    path.rmdir()


def rewrite_closed_document(path: Path, field: str, mutate: Any) -> None:
    value = strict_json(path.read_bytes(), "attack source", ROW_CAP)
    require(type(value) is dict, "attack document type")
    mutate(value)
    body = dict(value)
    body.pop(field, None)
    value[field] = object_sha(body)
    path.write_bytes(canonical(value))


def attack_suite(state: RebuildState, candidate_path: Path) -> dict[str, Any]:
    baseline = verify_candidate(state, candidate_path)
    parent = fixed_spill_parent()
    parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    attacks: list[dict[str, Any]] = []
    attack_path = clone_candidate(candidate_path, parent)

    def restore_role(role: str) -> None:
        target = attack_path / OUTPUTS[role]
        if target.exists() or target.is_symlink():
            target.unlink()
        source_fd = os.open(candidate_path / OUTPUTS[role], os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        target_fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        try:
            while True:
                copied = os.copy_file_range(source_fd, target_fd, 8_388_608)
                if copied == 0:
                    break
        finally:
            os.close(target_fd)
            os.close(source_fd)

    def execute(attack_id: str, mutate: Any, restore: Any, path_transform: Any = None) -> None:
        verify_path = attack_path
        alias: Path | None = None
        try:
            mutate(attack_path)
            if path_transform is not None:
                alias = path_transform(attack_path)
                verify_path = alias
            try:
                verify_candidate(state, verify_path)
            except Rejected as exc:
                boundary = str(exc)
            else:
                raise Rejected("coherent attack accepted:" + attack_id)
            body = {
                "attack_id": attack_id,
                "rejected": True,
                "rejection_boundary": boundary,
            }
            attacks.append({**body, "row_sha256": object_sha(body)})
        finally:
            if alias is not None and alias.is_symlink():
                alias.unlink()
            restore()

    execute("A01_EXTRA_FILE", lambda path: (path / "foreign").write_bytes(b"x"), lambda: (attack_path / "foreign").unlink())
    execute("A02_MISSING_RESULT", lambda path: (path / OUTPUTS["result"]).unlink(), lambda: restore_role("result"))
    execute(
        "A03_RESULT_SYMLINK",
        lambda path: ((path / OUTPUTS["result"]).unlink(), (path / OUTPUTS["result"]).symlink_to(candidate_path / OUTPUTS["result"])),
        lambda: restore_role("result"),
    )
    execute(
        "A04_HARDLINKED_RESULT",
        lambda path: ((path / OUTPUTS["result"]).unlink(), os.link(path / OUTPUTS["authority_frontier"], path / OUTPUTS["result"])),
        lambda: restore_role("result"),
    )
    def directory_symlink(path: Path) -> Path:
        alias = Path(os.fspath(path) + ".alias")
        alias.symlink_to(path, target_is_directory=True)
        return alias

    execute("A05_CANDIDATE_DIRECTORY_SYMLINK", lambda path: None, lambda: None, directory_symlink)

    def authority_mutation(key: str, value: Any) -> Any:
        return lambda path: rewrite_closed_document(
            path / OUTPUTS["authority_frontier"],
            "authority_frontier_sha256",
            lambda document: document["r235d_frontier"].__setitem__(key, value),
        )

    execute("A06_SHEET_OWNER_COMMITMENT", authority_mutation("R248_target_sheet_owner_binding_sequence_sha256", "0" * 64), lambda: restore_role("authority_frontier"))
    execute("A07_BULK_OWNER_COMMITMENT", authority_mutation("R248_target_only_bulk_binding_sequence_sha256", "0" * 64), lambda: restore_role("authority_frontier"))
    execute(
        "A08_AUTHORITY_PRODUCER_PIN",
        lambda path: rewrite_closed_document(path / OUTPUTS["authority_frontier"], "authority_frontier_sha256", lambda document: document.__setitem__("producer_file_sha256", "0" * 64)),
        lambda: restore_role("authority_frontier"),
    )
    pair_fields = (
        "corrected_member_count", "corrected_component_count", "all_unordered_member_pairs",
        "within_component_unordered_member_pairs", "cross_component_pair_denominator",
    )
    for ordinal, field in enumerate(pair_fields, 9):
        execute(
            "A" + str(ordinal).zfill(2) + "_PAIR_" + field.upper(),
            lambda path, _field=field: rewrite_closed_document(path / OUTPUTS["pair_denominator"], "pair_denominator_sha256", lambda document: document.__setitem__(_field, document[_field] + 1)),
            lambda: restore_role("pair_denominator"),
        )
    execute(
        "A14_FORWARD_PARTITION",
        lambda path: rewrite_closed_document(path / OUTPUTS["result"], "result_sha256", lambda document: document["fresh_forward_application"].__setitem__("partition_sha256", "0" * 64)),
        lambda: restore_role("result"),
    )
    execute(
        "A15_DELETE_CENSUS",
        lambda path: rewrite_closed_document(path / OUTPUTS["result"], "result_sha256", lambda document: document["affected_component_census"]["deleted_singleton_old_to_corrected_sizes"].__setitem__(0, [1, 1])),
        lambda: restore_role("result"),
    )
    execute(
        "A16_REKEY_CENSUS",
        lambda path: rewrite_closed_document(path / OUTPUTS["result"], "result_sha256", lambda document: document["affected_component_census"]["surviving_rekey_corrected_member_sizes"].__setitem__(0, 5_439)),
        lambda: restore_role("result"),
    )
    execute(
        "A17_PRE_VERIFICATION_CREDIT",
        lambda path: rewrite_closed_document(path / OUTPUTS["result"], "result_sha256", lambda document: document["formal_credit_without_independent_verification_marker"].__setitem__("corrected_DSU", 1)),
        lambda: restore_role("result"),
    )
    execute(
        "A18_DESCRIPTOR_DIGEST",
        lambda path: rewrite_closed_document(path / OUTPUTS["result"], "result_sha256", lambda document: document["output_artifacts_in_publication_order_before_result"][0].__setitem__("sha256", "0" * 64)),
        lambda: restore_role("result"),
    )
    for ordinal, role in enumerate(("member_invalidation", "root_disposition", "edge_remap", "member_component", "base_root_component", "component_census"), 19):
        def corrupt(path: Path, _role: str = role) -> None:
            target = path / OUTPUTS[_role]
            fd = os.open(target, os.O_WRONLY)
            try:
                os.pwrite(fd, b"X", 0)
            finally:
                os.close(fd)
            mutated_sha = hashlib.sha256(target.read_bytes()).hexdigest()
            rewrite_closed_document(
                path / OUTPUTS["result"],
                "result_sha256",
                lambda document: next(
                    descriptor for descriptor in document["output_artifacts_in_publication_order_before_result"]
                    if descriptor["role"] == _role
                ).__setitem__("sha256", mutated_sha),
            )
        execute(
            "A" + str(ordinal).zfill(2) + "_CORRUPT_" + role.upper(),
            corrupt,
            lambda _role=role: (restore_role(_role), restore_role("result")),
        )

    require(len(attacks) == 24 and all(row["rejected"] is True for row in attacks), "attack census")
    body = {
        "schema": SCHEMA + ".coherent-attack-suite.v1",
        "status": "PASS_24_OF_24_COHERENT_ATTACKS_REJECTED",
        "verifier_filename": VERIFIER_NAME,
        "verifier_file_sha256": stable_source_sha(VERIFIER_NAME, "attack verifier source"),
        "attack_count": 24,
        "rejected_count": 24,
        "all_rejected": True,
        "baseline_candidate_artifact_sha256": baseline["candidate_artifact_sha256"],
        "attacks": attacks,
    }
    remove_tree(attack_path)
    return {**body, "attack_suite_sha256": object_sha(body)}


def read_attack_suite() -> tuple[dict[str, Any], str]:
    path = ROOT / ATTACK_NAME
    before = os.stat(path, follow_symlinks=False)
    require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "attack suite regular one-link")
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0))
    try:
        opened = os.fstat(fd)
        exact(identity(opened), identity(before), "attack suite open race")
        first = hash_fd(fd); second = hash_fd(fd)
        exact(first, second, "attack suite two-pass digest")
        os.lseek(fd, 0, os.SEEK_SET)
        raw = b""
        while True:
            chunk = os.read(fd, 1_048_576)
            if not chunk:
                break
            raw += chunk
        exact(identity(os.fstat(fd)), identity(opened), "attack suite held identity")
        exact(identity(os.stat(path, follow_symlinks=False)), identity(opened), "attack suite path identity")
    finally:
        os.close(fd)
    value = strict_json(raw, "attack suite", 1_000_000)
    require(type(value) is dict, "attack suite document")
    body = dict(value); claimed = body.pop("attack_suite_sha256")
    exact(claimed, object_sha(body), "attack suite closure")
    exact((value["attack_count"], value["rejected_count"], value["all_rejected"]), (24, 24, True), "attack suite census")
    exact(value["verifier_filename"], VERIFIER_NAME, "attack verifier filename")
    exact(value["verifier_file_sha256"], stable_source_sha(VERIFIER_NAME, "current verifier source"), "attack verifier source pin")
    exact(first, hashlib.sha256(raw).hexdigest(), "attack suite read digest")
    return value, first


def verification_document(receipt: dict[str, Any]) -> dict[str, Any]:
    attack, attack_file_sha = read_attack_suite()
    body = {
        "schema": SCHEMA + ".verification.v1",
        **receipt,
        "attack_suite": {
            "filename": ATTACK_NAME,
            "file_sha256": attack_file_sha,
            "object_self_sha256": attack["attack_suite_sha256"],
            "attack_count": attack["attack_count"],
            "rejected_count": attack["rejected_count"],
            "all_rejected": attack["all_rejected"],
        },
        "formal_credit_marker": {
            "verification_last_and_sole_corrected_DSU_credit_marker": True,
            "corrected_DSU": 1,
            "B1A": 0,
            "B2": 0,
            "CM2": 0,
        },
    }
    return {**body, "verification_sha256": object_sha(body)}


class ManifestFirstSnapshot:
    def __init__(self) -> None:
        self.dirfd = -1
        self.fds: dict[str, int] = {}
        self.ids: dict[str, tuple[int, ...]] = {}
        self.hashes: dict[str, str] = {}

    def __enter__(self) -> "ManifestFirstSnapshot":
        before_dir = os.stat(ROOT, follow_symlinks=False)
        require(stat.S_ISDIR(before_dir.st_mode) and not ROOT.is_symlink(), "manifest authority directory")
        self.dirfd = os.open(ROOT, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0))
        exact(directory_identity(os.fstat(self.dirfd)), directory_identity(before_dir), "manifest authority directory race")
        manifest_fd = os.open(MANIFEST_NAME, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0), dir_fd=self.dirfd)
        manifest_info = os.fstat(manifest_fd)
        require(stat.S_ISREG(manifest_info.st_mode) and manifest_info.st_nlink == 1, "manifest regular one-link")
        self.fds[MANIFEST_NAME] = manifest_fd
        self.ids[MANIFEST_NAME] = identity(manifest_info)
        manifest_sha = hash_fd(manifest_fd)
        self.hashes[MANIFEST_NAME] = manifest_sha
        os.lseek(manifest_fd, 0, os.SEEK_SET)
        raw = b""
        while True:
            chunk = os.read(manifest_fd, 1_048_576)
            if not chunk:
                break
            raw += chunk
        try:
            text = raw.decode("ascii")
        except UnicodeDecodeError as exc:
            raise Rejected("manifest ascii") from exc
        require(text.endswith("\n") and not text.endswith("\n\n"), "manifest newline")
        lines = text.splitlines()
        exact(len(lines), len(MANIFEST_MEMBERS), "manifest member count")
        entries: dict[str, str] = {}
        for line, expected_name in zip(lines, MANIFEST_MEMBERS, strict=True):
            require(len(line) == 66 + len(expected_name) and line[64:66] == "  ", "manifest wire:" + expected_name)
            digest_value, filename = line[:64], line[66:]
            require(is_sha256(digest_value), "manifest digest:" + expected_name)
            exact(filename, expected_name, "manifest order")
            entries[filename] = digest_value
        exact(len(entries), len(MANIFEST_MEMBERS), "manifest unique names")
        for filename in MANIFEST_MEMBERS:
            before = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
            require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "manifest member regular one-link:" + filename)
            fd = os.open(filename, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0), dir_fd=self.dirfd)
            opened = os.fstat(fd)
            exact(identity(opened), identity(before), "manifest member open race:" + filename)
            first = hash_fd(fd); second = hash_fd(fd)
            exact(first, second, "manifest member two-pass digest:" + filename)
            exact(first, entries[filename], "manifest member pin:" + filename)
            self.fds[filename] = fd
            self.ids[filename] = identity(opened)
            self.hashes[filename] = first
        return self

    def read(self, filename: str) -> bytes:
        fd = self.fds[filename]
        os.lseek(fd, 0, os.SEEK_SET)
        chunks: list[bytes] = []
        while True:
            chunk = os.read(fd, 1_048_576)
            if not chunk:
                return b"".join(chunks)
            chunks.append(chunk)

    def final_revalidate(self) -> None:
        for filename in reversed((MANIFEST_NAME, *MANIFEST_MEMBERS)):
            exact(identity(os.fstat(self.fds[filename])), self.ids[filename], "manifest final held identity:" + filename)
            exact(identity(os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)), self.ids[filename], "manifest final path identity:" + filename)
            exact(hash_fd(self.fds[filename]), self.hashes[filename], "manifest final digest:" + filename)

    def __exit__(self, *_: Any) -> None:
        for fd in self.fds.values():
            try:
                os.close(fd)
            except OSError:
                pass
        if self.dirfd >= 0:
            try:
                os.close(self.dirfd)
            except OSError:
                pass


def manifest_first_no_write(candidate_path: Path) -> dict[str, Any]:
    with ManifestFirstSnapshot() as package:
        with AuthoritySnapshot() as authority:
            state = rebuild_state(authority)
            receipt = verify_candidate(state, candidate_path)
            authority.final_revalidate()
        for role in OUTPUT_ORDER:
            exact(receipt["candidate_artifact_sha256"][role], package.hashes[OUTPUTS[role]], "manifest candidate equality:" + role)
        expected_verification = canonical(verification_document(receipt))
        exact(package.read(VERIFICATION_NAME), expected_verification, "manifest verification-last byte identity")
        package.final_revalidate()
        return {
            "status": "PASS_MANIFEST_FIRST_HELD_FD_FINAL_NO_WRITE_FULL_REPLAY",
            "manifest_sha256": package.hashes[MANIFEST_NAME],
            "manifest_member_count": len(MANIFEST_MEMBERS),
            "corrected_partition_sha256": receipt["corrected_partition_sha256"],
            "corrected_member_count": receipt["corrected_member_count"],
            "corrected_component_count": receipt["corrected_component_count"],
            "cross_component_pair_denominator": receipt["cross_component_pair_denominator"],
            "deliverables_write_syscalls": 0,
        }


def publish_document(filename: str, document: dict[str, Any]) -> None:
    output = ROOT / filename
    require(not output.exists(), "output no-clobber:" + filename)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0)
    fd = os.open(output, flags, 0o600)
    try:
        os.write(fd, canonical(document)); os.fsync(fd)
    finally:
        os.close(fd)


def fixed_spill_parent(tmpdir_value: Any = None) -> Path:
    require(tmpdir_value is None or type(tmpdir_value) is str, "TMPDIR attack type")
    deliverables = ROOT.resolve(strict=True)
    fixed = Path(FIXED_SPILL_PARENT)
    require(os.path.commonpath((str(fixed), str(deliverables))) != str(deliverables), "spill outside deliverables")
    return fixed


def strict_runtime() -> None:
    require(type(sys.flags.isolated) is int and sys.flags.isolated == 1, "python -I required")
    require(sys.dont_write_bytecode is True, "python -B required")


def main() -> int:
    strict_runtime()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-publish", action="store_true")
    parser.add_argument("--verify-no-write", action="store_true")
    parser.add_argument("--attack-publish", action="store_true")
    parser.add_argument("--manifest-first-no-write", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--candidate-dir")
    args = parser.parse_args()
    require(sum(bool(x) for x in (args.verify_publish, args.verify_no_write, args.attack_publish, args.manifest_first_no_write, args.self_test)) == 1, "exact mode")
    if args.self_test:
        with AuthoritySnapshot() as authority:
            state = rebuild_state(authority)
            authority.final_revalidate()
        print("PASS_C0_INDEPENDENT_AUTHORITY_AND_FRESH_DSU_REBUILD_SELF_TEST")
        print("corrected_partition_sha256=" + state.partition_sha256)
        print("corrected_member_count=" + str(sum(len(values) for values in state.component_members.values())))
        print("corrected_component_count=" + str(len(state.component_members)))
        return 0
    require(type(args.candidate_dir) is str and args.candidate_dir != "", "candidate directory required")
    if args.manifest_first_no_write:
        print(json.dumps(manifest_first_no_write(Path(args.candidate_dir)), sort_keys=True, separators=(",", ":")))
        return 0
    with AuthoritySnapshot() as authority:
        state = rebuild_state(authority)
        if args.attack_publish:
            suite = attack_suite(state, Path(args.candidate_dir))
            publish_document(ATTACK_NAME, suite)
            receipt = {
                "status": suite["status"],
                "attack_count": suite["attack_count"],
                "attack_suite_sha256": suite["attack_suite_sha256"],
            }
        else:
            receipt = verify_candidate(state, Path(args.candidate_dir))
        authority.final_revalidate()
    if args.verify_publish:
        publish_document(VERIFICATION_NAME, verification_document(receipt))
    print(json.dumps(receipt, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
