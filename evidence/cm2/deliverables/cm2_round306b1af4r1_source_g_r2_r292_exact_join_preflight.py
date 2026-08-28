#!/usr/bin/env python3
"""Round306B1AF4R1 exact R2/R292 join preflight.

This artifact is a read-only, zero-credit replay.  It byte-pins and streams
the sealed inputs needed to reconstruct the R2 and R292 *join topology*, the
R294/R295A representation-alias dispatch, and deterministic commitments to
those joins.  It deliberately does not construct normalized-support rows and
does not import or execute any upstream Python source.

Candidate and production entry points are unavailable before any filesystem
operation.  ``--print-contract`` is filesystem-inert; ``--self-test`` opens no
pinned input and writes no file (it resolves the local directory only for a
hostile temporary-root test).  ``--full-replay`` is the only mode that opens
the pinned inputs.
"""

from __future__ import annotations

import argparse
from collections import Counter
import copy
from fractions import Fraction
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import re
import sqlite3
import stat
import tempfile
from typing import Any, BinaryIO, Iterator, NoReturn, TextIO


class PreflightBlocked(RuntimeError):
    """Fail-closed pin, replay, semantic, or forbidden-mode violation."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise PreflightBlocked(label)


SCHEMA = "cm2.round306b1af4r1.source-g-r2-r292-exact-join-preflight.v1"
STATUS = "ZERO_CREDIT_READ_ONLY_EXACT_JOIN_PREFLIGHT__NOT_FORMAL_CONSTRUCTOR"
CANDIDATE_BLOCK_REASON = (
    "Round306B1AF4R1 is a read-only zero-credit preflight; candidate and "
    "production construction remain blocked before filesystem access"
)


# (label, basename, exact raw-byte size, SHA-256).  Python dependencies are
# hashed as inert bytes only.  Data inputs are parsed from their held FDs.
INPUT_PINS: tuple[tuple[str, str, int, str], ...] = (
    ("AF2_PARTITION_CONTRACT", "cm2_round306b1af2_source_g_primitive_support_source_partition_freeze_contract.py", 52_538, "a91578a8bef1c4a72f940f7ebc71aea4c0ebc1ddac08ddbb3889a2da6cdd00f5"),
    ("AF3D1_AUTHORITY_DELTA", "cm2_round306b1af3d1_source_g_support_representation_authority_delta_contract.py", 57_389, "d61fbdc7e6d917c9c451cf63a7640285e900fd08dff76800119ca60ae5e55138"),
    ("AF4_SYMBOLIC_KERNEL", "cm2_round306b1af4_source_g_normalized_support_symbolic_kernel.py", 87_237, "c8bb9cf85aace782639859c33625732bf866a7fad34ff31cce58ab84af9f6a6f"),
    ("AF4_TYPED_SCHEMA", "cm2_round306b1af4_source_g_normalized_support_representation_typed_schema_contract.py", 80_436, "ee095fe5db22c6a4dd0804eca0fb553a132546367dcb37fcd75733050aa52cf9"),
    ("R182_GEOMETRY_ROWS", "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json", 158_815_476, "ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c"),
    ("R269_DIRECT_SIGNATURES", "cm2_round269_source_g_closed_collar_direct_signature_materialization_certificate.json", 319_672_585, "472df3ac65c490b79924beaabb382435f5b74ea8ac6c13d71b1d0ab54ffe01d3"),
    ("R270_DIRECT_SIGNATURES", "cm2_round270_source_g_outgoing_g_factor_signature_materialization_certificate.json", 56_705_100, "72a47e53ff601660cb63fe8062403e41a54450fa4a432638faf18a2c76b3efea"),
    ("R271_WALL_AND_TAIL_SIGNATURES", "cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_certificate.json", 112_741_715, "c2a6b66c6fc6ac0b353b36254339a90b91f18c52246c324307ee49569bd7b747"),
    ("R272_DUAL_FACTOR_WALL", "cm2_round272_source_g_boundary_dual_factor_wall_closure_certificate.json", 1_250_159, "16050c7087deb546d39b2c7922274ccae7cec24a799ecafd9a8304ae1186d8f2"),
    ("R275_REVERSE_RECHART", "cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json", 35_517_526, "e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386"),
    ("R286_EXACT_REFINEMENT", "cm2_round286_source_g_partial_overlap_exact_refinement_probe_ledger.json.gz", 1_617_322, "bb7e28cbe029e2bb414313ec4a08f6366acbbad88a519926ec2a3a424e679eda"),
    ("R287_RECHART_DISPOSITION", "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_ledger.json.gz", 7_529_109, "29838e3e6b33f03bf623bbce8b87e6ba5c3306e66beb0b6634496503fb9a4f9a"),
    ("R288_ATOM_DISPOSITION", "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_atom_dispositions.json.gz", 134_114_861, "6b0a8aa1cd38019322a61f5aaefc936006d10769cd21a5c8df374576f9ac570a"),
    ("R292_OVERLAP_EXHAUSTION", "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_ledger.json.gz", 5_544_437, "8863126e88ffd30438938d0a8bdb577f5928ae81f3f17f4b506829d59103a8ab"),
    ("R294_OCCURRENCE_REGISTRY", "cm2_round294_source_g_occurrence_registry_atomic_promotion_registry_ledger.json.gz", 262_951_902, "c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb"),
    ("R294_REPRESENTATION_BINDINGS", "cm2_round294_source_g_occurrence_registry_atomic_promotion_representation_binding_ledger.json.gz", 26_672_326, "f9fcc986771b1c3551420516cd9f2c5dde662f87d044666d9306404f30bb6833"),
    ("R295A_REPRESENTATION_ALIASES", "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_representation_alias_ledger.json.gz", 118_612, "5c826ef03dd6f8662528e565c36089422e590d1ebf9fc8bade99f1665c68ad2f"),
    ("B0_MEMBER_INDEX", "cm2_round306b0_source_g_r306a_universe_support_source_freeze_member_support_source_index.json.gz", 162_499_140, "c9a8649c8473bb6a170187e7f803e95748d2ff2198b1b846d97383dd5f0581af"),
    ("B1R0_PREDICATE_CELLS", "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_predicate_source_cell.json.gz", 105_989_322, "19d13d93fc02296f673ca18cc2edbd96174985f7be8fb0e03694582b188b0f96"),
    ("B1R0_MEMBER_UNIONS", "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_member_union.json.gz", 123_019_951, "4b3633782e4514f598cb9cce19930ba31616f7d42aab002df4f77f9b4601ddf7"),
    ("AF4D1_SEMANTIC_WIRE_DELTA", "cm2_round306b1af4d1_source_g_semantic_wire_delta_contract.py", 84_392, "5082df54ea4c514de906f4a923856adb20c6240c9be33401e784b2513a85f09f"),
    ("R288_EXISTING_OVERLAP_RELATIONS", "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_existing_overlap_relations.json.gz", 7_237_078, "d76d27c436735511dc34056d9237a2772decd30129e3019b74c5a02a118ab24e"),
)

PIN_BY_NAME = {row[1]: row for row in INPUT_PINS}
HEX64 = re.compile(r"^[0-9a-f]{64}$")

R182 = INPUT_PINS[4][1]
R269 = INPUT_PINS[5][1]
R270 = INPUT_PINS[6][1]
R271 = INPUT_PINS[7][1]
R272 = INPUT_PINS[8][1]
R275 = INPUT_PINS[9][1]
R286 = INPUT_PINS[10][1]
R287 = INPUT_PINS[11][1]
R288 = INPUT_PINS[12][1]
R292 = INPUT_PINS[13][1]
R294_REGISTRY = INPUT_PINS[14][1]
R294_BINDINGS = INPUT_PINS[15][1]
R295A = INPUT_PINS[16][1]
B0 = INPUT_PINS[17][1]
B1_CELL = INPUT_PINS[18][1]
B1_MEMBER = INPUT_PINS[19][1]
R288_OVERLAP = INPUT_PINS[21][1]


TABLE_EXPECTATIONS: dict[str, tuple[int, str]] = {
    "R182.collar_occurrence_rows": (54_220, "d77e65b5b9dfb5f7f107b39eaac3553be67ba76231f1888de1f97ecc121361db"),
    "R182.collar_leaf_rows": (202_840, "ced6d2764a7e1f5d404c1d56249e428f0754e53e7dded620e5904f9eb80b694c"),
    "R269.direct": (187_128, "992392cc52465cd5ea427e7776fc16fd889048553950b5338042581c14d98755"),
    "R270.direct": (37_712, "6f23d7d545ff8c3add454fe01da64d095f237222228c1dd382ca9b19420d746e"),
    "R271.side": (70_420, "cec8a0318385127d8ee5d7968c016f8f6b7ee103596fbce5258cc3b25c4930b8"),
    "R271.failclosed": (496, "4820153f78f785914c33b3738885f136b987cf8c2d3b01b509692454d32d6491"),
    "R272.side": (720, "f23f389e39a9715f67fa827026072db638aee34c6f1e539b5ec36bf225e075da"),
    "R275.strict": (5_288, "f1fc71b904d3dd060173c48480c09f2c7960dee2ad51db935d4d80966e0b38b6"),
    "R275.arrangement": (8_500, "6ef756cfb1d5b1f5226643142e77ba897b5dcac326edb301c5d2d01963470ba5"),
    "R286.rows": (7_616, "ef4529302d5a072b04133abb433ee4676acd4e8867a360fd09e05e28053917c6"),
    "R287.region": (13_788, "7d07e90c481b1c511ccce1d56df67f95140aa8d9b5cf5ea30b1d962ace5d8765"),
    "R287.refinement": (7_616, "951e8d912a4bf9494c928fbbdc99663485c019cee79580df98f838e0157555c9"),
    "R288.rows": (332_016, "8007b0c96e44c76bea6038fed8430134f9f424c7a81508f843d72d473f768849"),
    "R288.overlap": (36_680, "8a93bc24e836f2aca8cf59869217851be8dbedb8c930b325549ded7e8098cb7e"),
    "R292.rows": (22_820, "556bd0ed95709fe43ff7837522d8729582ce0e7c9679879a57365f864f6ba055"),
    "R294.registry": (431_208, "33936ecd04cbce9f9a308b0da10381bd854b45028db53db5d3cbb9aa8b264044"),
    "R294.bindings": (46_288, "ece198bf5e8b95448b09f60061677feafca3416525ba80f3b88a51e766414be7"),
    "R295A.aliases": (276, "40047a170d2e89a9e9cf8422ff86e265166e921f86386ecb4df790e8210d09de"),
    "B0.members": (564_492, "c7dfb5534fddeb22fffb81bf539fe44d837aced46577aa5f490a0ae14aba77f5"),
    "B1R0.cells": (295_340, "b89220807eef10bc8412be19c5037ea75fa3c6fdf4321c27938afec0c68c9246"),
    "B1R0.members": (295_336, "6665fc8e72824fba7dbd1d1b7462ae419bb31c25149037da3183d74569b62a3d"),
}


W_TAIL_REGLUES: tuple[dict[str, Any], ...] = (
    {
        "member_id": "source-g-expanded-occurrence:777579326780a1cde1e5b1f37d3bbb9c125adc26409d16599f48f29673f9dc05",
        "interface": "-47967/128000",
        "parent_box": ["-3009/8000", "-4779/12800", "-3/64", "-11/256", "1/800", "1/400"],
        "children": ["round271-W-tail-side:f685c712f6ffcdcb2067dbbb1ce8263f735ade1d3244dae3c24bd81c5df03c8b", "round271-W-tail-side:8bddfee03e177225f624a72fd8ec52953521d9b6d62f49576b69108acb181d15"],
    },
    {
        "member_id": "source-g-expanded-occurrence:3dbc14a6e173aceacb227af67bf77573bf853dc8330d3d7e91dcbd1e0332a9e0",
        "interface": "-47967/128000",
        "parent_box": ["-3009/8000", "-4779/12800", "11/256", "3/64", "-1/400", "-1/800"],
        "children": ["round271-W-tail-side:283deceec14bcb2bf1023665cf8b443eda90cf995e8b4588aa7359e9b50b5943", "round271-W-tail-side:d2ca5b59b2b24166b1b2af242db4fe2081d10c53f6459a56488b9bf105a32a9b"],
    },
    {
        "member_id": "source-g-expanded-occurrence:7679f954c45bd68587aa443c6dcecfa04beabac556043a05c88b96d54d00a231",
        "interface": "47967/128000",
        "parent_box": ["4779/12800", "3009/8000", "11/256", "3/64", "1/800", "1/400"],
        "children": ["round271-W-tail-side:7f514e571220e84dc2a295fbceb2eb3af1dc1c76ac32f7b3b4dee8feeb575380", "round271-W-tail-side:42360900f45f7ec7fb40da6cd66a6651574e40e5e945d70a3a376c6f43705b05"],
    },
    {
        "member_id": "source-g-expanded-occurrence:8d341c7b44298ec53e940bda07a53b38ddd01f34bad63236d0d691cf81a83819",
        "interface": "47967/128000",
        "parent_box": ["4779/12800", "3009/8000", "-3/64", "-11/256", "-1/400", "-1/800"],
        "children": ["round271-W-tail-side:0a7aa9828f1f7d748808d3c987b3cdace8d7803782b02fe75971113ff3d704ae", "round271-W-tail-side:9d741d4b52856aa778df9829354028e84822ab542fca42b401f715357a39c78b"],
    },
)


FORMAL_BLOCKERS = (
    "AF4 kernel does not semantically validate PREDICATE_CELL_EQUIVALENCE or MONOTONE_GRAPH and has no AST differentiation/derivative-sign primitive",
    "DIRECTED_INTERVAL ignores subdivision_path and cannot independently close active curved-factor subdivisions or the closed-hull t=0 tails",
    "ARTIFICIAL_FACE_REGLUE does not verify or restore the common face, common trace, or half-open owner",
    "REPRESENTATION_OWNER_BACKBINDING and incidence/trace/sheet equality are wire-shape checks rather than semantic set-equality checks",
    "SOURCE_LINEAGE_EXHAUSTION checks counts/list lengths rather than exact sets, row hashes, duplicate rejection, and anti-join exhaustion",
    "AF4 kernel accepts an arbitrary positive target radius instead of binding G=9/25 and W=4/25 to authoritative target kind",
    "the G one-sided source factor needs an explicit R182 occurrence reason/equation binding and a semantic one-sided-extension kernel",
    "REFINED_PRIMARY_EXTRA and ALIAS_EXISTING_MEMBER are subcovers, but the AF4 equality-only owner-backbinding rule has no role-specific subset/inclusion semantics",
    "AF4D1 freezes the R292 canonical Kruskal order and representation-role delta, but no executable semantic kernel, authoritative physical-face stream, output-table byte order, or measured runtime-memory limit yet discharges them",
)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in output, "duplicate JSON key:" + key)
        output[key] = value
    return output


def reject_noninteger(token: str) -> Any:
    raise PreflightBlocked("nonintegral JSON token:" + token)


DECODER = json.JSONDecoder(
    object_pairs_hook=unique_object,
    parse_float=reject_noninteger,
    parse_constant=reject_noninteger,
)

# These are two different limits.  The row limit applies both to the exact
# UTF-8 source slice consumed by a successful raw_decode and to the canonical
# serialization of the decoded value.  The parser-buffer limit additionally
# permits one maximum UTF-8 read-block of lookahead/overhang.  Python's text
# reader is asked for characters, so four UTF-8 bytes per character is the
# conservative block conversion.
MAX_DECODED_CANONICAL_ROW_BYTES = 8 << 20
STREAM_READ_CHUNK_CHARACTERS = 1 << 18
MAX_READ_CHUNK_UTF8_BYTES = 4 * STREAM_READ_CHUNK_CHARACTERS
MAX_PARSER_BUFFER_UTF8_BYTES = (
    MAX_DECODED_CANONICAL_ROW_BYTES + MAX_READ_CHUNK_UTF8_BYTES
)


class ListHash:
    """SHA-256 of a canonical JSON list without retaining the list."""

    def __init__(self) -> None:
        self._state = hashlib.sha256(b"[")
        self.count = 0

    def add(self, value: Any) -> None:
        if self.count:
            self._state.update(b",")
        self._state.update(canonical(value))
        self.count += 1

    def finish(self) -> str:
        state = self._state.copy()
        state.update(b"]")
        return state.hexdigest()


class TableAudit:
    def __init__(self, label: str) -> None:
        self.label = label
        self.rows = ListHash()

    def add(self, row: Any, *, closed: bool) -> None:
        if closed:
            check_closed_row(row, self.label)
        self.rows.add(row)

    def finish(self) -> dict[str, Any]:
        expected_count, expected_sha = TABLE_EXPECTATIONS[self.label]
        observed_sha = self.rows.finish()
        need(self.rows.count == expected_count, self.label + ":row count")
        need(observed_sha == expected_sha, self.label + ":ordered rows commitment")
        return {
            "table": self.label,
            "row_count": self.rows.count,
            "rows_sha256": observed_sha,
            "own_row_sha256_checked": self.label not in {
                "R182.collar_occurrence_rows", "R182.collar_leaf_rows"
            },
        }


def check_closed_row(row: Any, label: str) -> None:
    need(type(row) is dict and type(row.get("row_sha256")) is str, label + ":closed row")
    payload = dict(row)
    claimed = payload.pop("row_sha256")
    need(HEX64.fullmatch(claimed) is not None, label + ":row hash syntax")
    need(digest(payload) == claimed, label + ":row hash")


def stat_fingerprint(info: os.stat_result) -> tuple[int, ...]:
    return (
        info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size,
        info.st_mtime_ns, info.st_ctime_ns,
    )


def directory_identity(info: os.stat_result) -> tuple[int, int, int]:
    return (info.st_dev, info.st_ino, info.st_mode)


def path_is_within(path: str, directory: str) -> bool:
    try:
        return os.path.commonpath((path, directory)) == directory
    except ValueError:
        return False


def checked_temporary_root(deliverables_directory: str) -> tuple[str, str, tuple[int, int, int]]:
    """Resolve and seal an OS temporary root outside deliverables."""
    deliverables_real = os.path.realpath(deliverables_directory)
    temporary_root = os.path.realpath(tempfile.gettempdir())
    need(
        not path_is_within(temporary_root, deliverables_real),
        "temporary spill root must be outside real deliverables directory",
    )
    root_info = os.stat(temporary_root, follow_symlinks=False)
    need(stat.S_ISDIR(root_info.st_mode), "temporary spill root must be a real directory")
    return temporary_root, deliverables_real, directory_identity(root_info)


def checked_created_temporary_directory(
    temporary: str,
    temporary_root: str,
    deliverables_real: str,
    root_identity: tuple[int, int, int],
) -> str:
    """Recheck the freshly created spill directory before SQLite opens."""
    root_now = os.stat(temporary_root, follow_symlinks=False)
    need(directory_identity(root_now) == root_identity, "temporary spill root identity changed")
    temporary_named = os.stat(temporary, follow_symlinks=False)
    need(stat.S_ISDIR(temporary_named.st_mode), "created temporary spill path is not a directory")
    temporary_real = os.path.realpath(temporary)
    need(
        os.path.dirname(temporary_real) == temporary_root,
        "created temporary spill directory is not a direct child of checked root",
    )
    need(
        not path_is_within(temporary_real, deliverables_real),
        "created temporary spill directory lies inside real deliverables directory",
    )
    temporary_resolved = os.stat(temporary_real, follow_symlinks=False)
    need(
        directory_identity(temporary_named) == directory_identity(temporary_resolved),
        "created temporary spill path changed during realpath/stat verification",
    )
    root_after = os.stat(temporary_root, follow_symlinks=False)
    need(directory_identity(root_after) == root_identity, "temporary spill root changed before SQLite open")
    return temporary_real


def hash_fd(fd: int, expected_size: int) -> tuple[int, str]:
    os.lseek(fd, 0, os.SEEK_SET)
    total = 0
    state = hashlib.sha256()
    while True:
        block = os.read(fd, 1 << 20)
        if not block:
            break
        total += len(block)
        need(total <= expected_size, "held FD grew while hashing")
        state.update(block)
    os.lseek(fd, 0, os.SEEK_SET)
    return total, state.hexdigest()


class PinnedInputs:
    """Held dirfd and exact single-link input FDs for the complete replay."""

    def __init__(self, directory: str) -> None:
        self.directory = directory
        self.dirfd = -1
        self.dir_before: os.stat_result | None = None
        self.files: dict[str, tuple[int, os.stat_result]] = {}
        self.verification_rows: list[dict[str, Any]] = []

    def __enter__(self) -> "PinnedInputs":
        path_before = os.stat(self.directory, follow_symlinks=False)
        need(stat.S_ISDIR(path_before.st_mode), "deliverables directory")
        flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
        self.dirfd = os.open(self.directory, flags)
        self.dir_before = os.fstat(self.dirfd)
        need(directory_identity(path_before) == directory_identity(self.dir_before), "deliverables dirfd binding")
        try:
            for label, filename, size, sha in INPUT_PINS:
                need(filename == os.path.basename(filename) and filename not in ("", ".", ".."), "pin basename")
                before = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
                need(stat.S_ISREG(before.st_mode), "pin regular:" + filename)
                need(before.st_nlink == 1, "pin nlink one:" + filename)
                need(before.st_size == size, "pin size:" + filename)
                fd = os.open(filename, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0), dir_fd=self.dirfd)
                opened = os.fstat(fd)
                need(stat_fingerprint(before) == stat_fingerprint(opened), "pin path/open race:" + filename)
                n1, h1 = hash_fd(fd, size)
                mid = os.fstat(fd)
                need(stat_fingerprint(opened) == stat_fingerprint(mid), "pin changed pass1:" + filename)
                n2, h2 = hash_fd(fd, size)
                after = os.fstat(fd)
                named_after = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
                need(stat_fingerprint(opened) == stat_fingerprint(after) == stat_fingerprint(named_after), "pin changed/rebound:" + filename)
                need(n1 == n2 == size and h1 == h2 == sha, "pin two-pass hash:" + filename)
                self.files[filename] = (fd, opened)
                self.verification_rows.append({
                    "label": label, "filename": filename, "exact_size": size,
                    "sha256": sha, "pass1_sha256": h1, "pass2_sha256": h2,
                    "regular_file": True, "nlink_one": True,
                    "held_fd_stable": True,
                })
            return self
        except Exception:
            self.close()
            raise

    def stream(self, filename: str, marker: str, *, anchor: str | None = None) -> Iterator[Any]:
        need(filename in self.files, "stream pinned file:" + filename)
        fd, before = self.files[filename]
        os.lseek(fd, 0, os.SEEK_SET)
        raw = os.fdopen(os.dup(fd), "rb")
        binary: BinaryIO = gzip.GzipFile(fileobj=raw, mode="rb") if filename.endswith(".gz") else raw
        text = io.TextIOWrapper(binary, encoding="utf-8", newline="")
        try:
            yield from iter_array(text, marker, anchor=anchor)
        finally:
            try:
                text.close()
            finally:
                if not raw.closed:
                    raw.close()
                os.lseek(fd, 0, os.SEEK_SET)
                need(stat_fingerprint(os.fstat(fd)) == stat_fingerprint(before), "held FD stable after parse:" + filename)

    def close(self) -> None:
        for filename, (fd, before) in list(self.files.items()):
            try:
                need(stat_fingerprint(os.fstat(fd)) == stat_fingerprint(before), "held FD final stability:" + filename)
                if self.dirfd >= 0:
                    named = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
                    need(stat_fingerprint(named) == stat_fingerprint(before), "held pathname final binding:" + filename)
            finally:
                os.close(fd)
        self.files.clear()
        if self.dirfd >= 0:
            try:
                assert self.dir_before is not None
                held = os.fstat(self.dirfd)
                named = os.stat(self.directory, follow_symlinks=False)
                need(directory_identity(self.dir_before) == directory_identity(held) == directory_identity(named), "deliverables directory replaced")
            finally:
                os.close(self.dirfd)
                self.dirfd = -1

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        self.close()


def iter_array(stream: TextIO, marker: str, *, anchor: str | None = None) -> Iterator[Any]:
    """Strictly decode one pinned JSON array incrementally.

    The marker search retains only a marker-sized suffix.  Every append is
    checked against ``MAX_PARSER_BUFFER_UTF8_BYTES``.  A successful decode is
    accepted only when both its consumed source slice and its canonical
    serialization are at most ``MAX_DECODED_CANONICAL_ROW_BYTES``.
    """
    def append_block(buffer: str, label: str) -> str:
        block = stream.read(STREAM_READ_CHUNK_CHARACTERS)
        need(bool(block), label)
        combined = buffer + block
        need(
            len(combined.encode("utf-8")) <= MAX_PARSER_BUFFER_UTF8_BYTES,
            "stream parser buffer exceeds explicit UTF-8 byte cap",
        )
        return combined

    def seek(token: str, initial: str) -> str:
        buffer = initial
        while True:
            position = buffer.find(token)
            if position >= 0:
                return buffer[position + len(token):]
            buffer = append_block(buffer, "missing array marker:" + token)
            position = buffer.find(token)
            if position >= 0:
                return buffer[position + len(token):]
            buffer = buffer[-max(len(token) - 1, 1):]

    buffer = ""
    if anchor is not None:
        buffer = seek(anchor, buffer)
    buffer = seek(marker, buffer)
    # Pretty-printed sources may separate a key from its array with arbitrary
    # JSON whitespace.  Callers can therefore seek the key token alone.
    stripped = buffer.lstrip()
    if stripped.startswith(":"):
        stripped = stripped[1:].lstrip()
        need(stripped.startswith("["), "streamed key is not an array:" + marker)
        buffer = stripped[1:]
    require_comma = False
    while True:
        buffer = buffer.lstrip()
        while not buffer:
            buffer = append_block(buffer, "truncated streamed array")
            buffer = buffer.lstrip()
        if buffer[0] == "]":
            return
        if require_comma:
            need(buffer[0] == ",", "missing streamed comma")
            buffer = buffer[1:].lstrip()
            while not buffer:
                buffer = append_block(buffer, "truncated streamed row after comma")
                buffer = buffer.lstrip()
            need(buffer[0] != "]", "trailing streamed comma")
        else:
            need(buffer[0] != ",", "leading streamed comma")
        while True:
            try:
                value, end = DECODER.raw_decode(buffer)
                break
            except json.JSONDecodeError:
                need(
                    len(buffer.encode("utf-8")) <= MAX_DECODED_CANONICAL_ROW_BYTES,
                    "incomplete streamed row exceeds decoded-row source byte cap",
                )
                buffer = append_block(buffer, "truncated streamed JSON value")
        need(
            len(buffer[:end].encode("utf-8"))
            <= MAX_DECODED_CANONICAL_ROW_BYTES,
            "successful decoded-row source slice exceeds byte cap",
        )
        need(
            len(canonical(value)) <= MAX_DECODED_CANONICAL_ROW_BYTES,
            "successful decoded canonical row exceeds byte cap",
        )
        yield value
        buffer = buffer[end:]
        require_comma = True


def open_database(path: str) -> sqlite3.Connection:
    connection = sqlite3.connect(path)
    connection.execute("PRAGMA journal_mode=OFF")
    connection.execute("PRAGMA synchronous=OFF")
    connection.execute("PRAGMA temp_store=FILE")
    connection.execute("PRAGMA cache_size=-32768")
    connection.execute("PRAGMA foreign_keys=OFF")
    connection.executescript("""
        CREATE TABLE occurrence(occurrence_id TEXT PRIMARY KEY, chart TEXT, target TEXT, reason TEXT, equation TEXT);
        CREATE TABLE leaf(leaf_id TEXT PRIMARY KEY, occurrence_id TEXT, box_json TEXT, graph_class TEXT);
        CREATE TABLE source(source_id TEXT PRIMARY KEY, source_round INTEGER, table_name TEXT, row_sha TEXT, leaf_id TEXT, prefix_kind TEXT, hplus TEXT, hminus TEXT, region_sign TEXT, outgoing_cell TEXT, target TEXT, chart TEXT, reason TEXT, equation TEXT, product_sign TEXT, excluded_face TEXT, extension TEXT);
        CREATE TABLE r271_leaf(leaf_id TEXT PRIMARY KEY, reason TEXT, residual TEXT, row_sha TEXT);
        CREATE TABLE r2_cell(cell_id TEXT PRIMARY KEY, member_id TEXT, source_id TEXT UNIQUE, source_round INTEGER, source_table TEXT, source_sha TEXT, leaf_id TEXT, carrier_json TEXT, family TEXT, inventory_json TEXT, row_sha TEXT);
        CREATE TABLE r2_member(member_id TEXT PRIMARY KEY, member_row_id TEXT UNIQUE, registry_row_id TEXT, b0_row_id TEXT, component_id TEXT, multiplicity INTEGER, cell_ids_json TEXT, source_ids_json TEXT, normalization_json TEXT, row_sha TEXT);
        CREATE TABLE r2_member_edge(cell_id TEXT PRIMARY KEY, member_id TEXT);
        CREATE TABLE r275(region_id TEXT PRIMARY KEY, box_json TEXT, source_table TEXT, row_sha TEXT);
        CREATE TABLE r286(cell_id TEXT PRIMARY KEY, region_id TEXT, box_json TEXT, row_sha TEXT);
        CREATE TABLE r287_source(source_id TEXT PRIMARY KEY, source_row_id TEXT UNIQUE, source_kind TEXT, sigma INTEGER, t2_json TEXT, coordinate_box_json TEXT, region_id TEXT, row_sha TEXT);
        CREATE TABLE r288(atom_row_id TEXT PRIMARY KEY, atom_id TEXT UNIQUE, row_sha TEXT);
        CREATE TABLE r288_overlap(overlap_row_id TEXT PRIMARY KEY, atom_id TEXT, row_sha TEXT);
        CREATE TABLE r292_cell(cell_id TEXT PRIMARY KEY, source_id TEXT, component_id TEXT, union_id TEXT, box_json TEXT, disposition TEXT, occupancy INTEGER, existing_ids_json TEXT, row_sha TEXT);
        CREATE TABLE r292_component(component_id TEXT PRIMARY KEY, union_id TEXT, declared_count INTEGER, cells_json TEXT, row_sha TEXT);
        CREATE TABLE r292_component_edge(component_id TEXT, cell_id TEXT, PRIMARY KEY(component_id,cell_id));
        CREATE TABLE registry(registry_row_id TEXT PRIMARY KEY, member_id TEXT UNIQUE, family TEXT, source_row_id TEXT, kind TEXT, row_sha TEXT);
        CREATE TABLE binding(binding_row_id TEXT PRIMARY KEY, source_rep_id TEXT UNIQUE, source_kind TEXT, source_row_id TEXT, source_row_sha TEXT, source_atom_row_id TEXT, source_atom_row_sha TEXT, target_member_id TEXT, coordinate_system TEXT, row_sha TEXT);
        CREATE TABLE r295(alias_row_id TEXT PRIMARY KEY, target_registry_row_id TEXT, target_member_id TEXT, source_rep_id TEXT UNIQUE, row_sha TEXT);
        CREATE TABLE b0(member_id TEXT PRIMARY KEY, b0_row_id TEXT UNIQUE, component_id TEXT, primary_source_package TEXT, primary_source_row_id TEXT, primary_source_row_sha TEXT, row_sha TEXT);
    """)
    return connection


def jdump(value: Any) -> str:
    return canonical(value).decode("ascii")


def jload(value: str | None) -> Any:
    return None if value is None else json.loads(value)


def insert_batch(connection: sqlite3.Connection, sql: str, batch: list[tuple[Any, ...]]) -> None:
    if batch:
        connection.executemany(sql, batch)
        batch.clear()


def fraction_box_subset(child: list[str], parent: list[str]) -> bool:
    need(len(child) == len(parent) == 6, "six-coordinate box")
    values_c = [Fraction(x) for x in child]
    values_p = [Fraction(x) for x in parent]
    return all(values_p[2 * axis] <= values_c[2 * axis] < values_c[2 * axis + 1] <= values_p[2 * axis + 1] for axis in range(3))


def source_prefix_kind(source_id: str) -> str:
    for prefix, kind in (
        ("round269-signed-region:", "H_GRID"),
        ("round270-signed-region:", "H_GRID"),
        ("round271-W-tail-side:", "W_TAIL"),
        ("round271-G-tail-side:", "G_ONE_SIDED"),
        ("round271-wall-side:", "WALL"),
        ("round272-boundary-wall-side:", "WALL"),
    ):
        if source_id.startswith(prefix):
            return kind
    raise PreflightBlocked("unknown R2 source ID prefix:" + source_id)


def registry_family(row: dict[str, Any]) -> str:
    kind = row["registry_entry_kind"]
    if kind == "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE":
        return "PRESERVED"
    if kind == "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM":
        return "R2"
    if kind == "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT":
        return "R292"
    raise PreflightBlocked("unknown R294 registry kind:" + str(kind))


def stream_commitment(connection: sqlite3.Connection, query: str, columns: tuple[str, ...], json_columns: frozenset[str] = frozenset()) -> dict[str, Any]:
    state = ListHash()
    for values in connection.execute(query):
        row = {}
        for name, value in zip(columns, values):
            row[name] = jload(value) if name in json_columns else value
        state.add(row)
    return {"row_count": state.count, "sha256": state.finish()}


def scalar(connection: sqlite3.Connection, query: str, parameters: tuple[Any, ...] = ()) -> Any:
    row = connection.execute(query, parameters).fetchone()
    need(row is not None and len(row) == 1, "scalar query")
    return row[0]


def create_replay_indexes(connection: sqlite3.Connection) -> None:
    """Create deterministic ephemeral indexes only after bulk streaming load."""
    connection.executescript("""
        CREATE INDEX source_leaf_idx ON source(leaf_id);
        CREATE INDEX r2_cell_member_idx ON r2_cell(member_id);
        CREATE INDEX r2_member_registry_idx ON r2_member(registry_row_id);
        CREATE INDEX r275_source_idx ON r275(source_table);
        CREATE INDEX r286_region_idx ON r286(region_id);
        CREATE INDEX r287_kind_idx ON r287_source(source_kind);
        CREATE INDEX r287_region_idx ON r287_source(region_id);
        CREATE INDEX r292_source_idx ON r292_cell(source_id);
        CREATE INDEX r292_component_idx ON r292_cell(component_id);
        CREATE INDEX registry_source_idx ON registry(source_row_id);
        CREATE INDEX registry_family_idx ON registry(family);
        CREATE INDEX binding_target_idx ON binding(target_member_id);
        CREATE INDEX binding_kind_idx ON binding(source_kind);
        CREATE INDEX r295_target_idx ON r295(target_member_id);
        CREATE INDEX b0_primary_idx ON b0(primary_source_row_id);
    """)


def load_r182(pins: PinnedInputs, db: sqlite3.Connection, audits: list[dict[str, Any]]) -> None:
    audit = TableAudit("R182.collar_occurrence_rows")
    batch: list[tuple[Any, ...]] = []
    for row in pins.stream(R182, '"collar_occurrence_rows":['):
        need(type(row) is list and len(row) == 31, "R182 occurrence row shape")
        audit.add(row, closed=False)
        # collar_leaf_rows[1] binds the Round179 occurrence identifier, which
        # is collar_occurrence_rows[1] (row[0] is the Round182 collar row ID).
        batch.append((row[1], row[4], row[5], row[7], row[8]))
        if len(batch) >= 1024:
            insert_batch(db, "INSERT INTO occurrence VALUES(?,?,?,?,?)", batch)
    insert_batch(db, "INSERT INTO occurrence VALUES(?,?,?,?,?)", batch)
    audits.append(audit.finish())

    audit = TableAudit("R182.collar_leaf_rows")
    for row in pins.stream(R182, '"collar_leaf_rows":['):
        need(type(row) is list and len(row) == 15, "R182 leaf row shape")
        audit.add(row, closed=False)
        batch.append((row[0], row[1], jdump(row[4]), row[9]))
        if len(batch) >= 1024:
            insert_batch(db, "INSERT INTO leaf VALUES(?,?,?,?)", batch)
    insert_batch(db, "INSERT INTO leaf VALUES(?,?,?,?)", batch)
    audits.append(audit.finish())
    need(scalar(db, "SELECT COUNT(*) FROM leaf l LEFT JOIN occurrence o ON o.occurrence_id=l.occurrence_id WHERE o.occurrence_id IS NULL") == 0, "R182 leaf/occurrence anti-join")


def load_source_table(pins: PinnedInputs, db: sqlite3.Connection, audits: list[dict[str, Any]], filename: str, source_round: int, table: str, label: str) -> None:
    anchor = f'"{table}":{{'
    audit = TableAudit(label)
    batch: list[tuple[Any, ...]] = []
    for row in pins.stream(filename, '"rows":[', anchor=anchor):
        need(type(row) is dict, label + ":row object")
        audit.add(row, closed=True)
        source_id = row["signed_region_row_id"]
        local = row.get("local_return_signature") or {}
        batch.append((
            source_id, source_round, table, row["row_sha256"], row["Round182_leaf_row_id"], source_prefix_kind(source_id),
            row.get("HPLUS_sign"), row.get("HMINUS_sign"), row.get("region_factor_sign"), local.get("outgoing_cell"),
            row.get("owner_target"), row.get("chart") or local.get("source_chart"), row.get("reason_label"), row.get("equation"),
            row.get("region_product_sign"), row.get("excluded_transition_face") or row.get("excluded_zero_face"),
            row.get("one_sided_extension") or row.get("connected_side_extension"),
        ))
        if len(batch) >= 1024:
            insert_batch(db, "INSERT INTO source VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", batch)
    insert_batch(db, "INSERT INTO source VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", batch)
    audits.append(audit.finish())


def load_r271_failclosed(pins: PinnedInputs, db: sqlite3.Connection, audits: list[dict[str, Any]]) -> None:
    audit = TableAudit("R271.failclosed")
    batch: list[tuple[Any, ...]] = []
    for row in pins.stream(R271, '"rows":[', anchor='"formal_failclosed_leaf_ledger":{'):
        need(type(row) is dict, "R271 failclosed row")
        audit.add(row, closed=True)
        batch.append((row["Round182_leaf_row_id"], row.get("reason_label"), row.get("residual_reason"), row["row_sha256"]))
        if len(batch) >= 1024:
            insert_batch(db, "INSERT INTO r271_leaf VALUES(?,?,?,?)", batch)
    insert_batch(db, "INSERT INTO r271_leaf VALUES(?,?,?,?)", batch)
    audits.append(audit.finish())


def load_r2_cells(pins: PinnedInputs, db: sqlite3.Connection, audits: list[dict[str, Any]]) -> Counter[str]:
    audit = TableAudit("B1R0.cells")
    batch: list[tuple[Any, ...]] = []
    counts: Counter[str] = Counter()
    for row in pins.stream(B1_CELL, '"predicate_source_cell_rows":['):
        need(type(row) is dict, "B1R0 cell row")
        audit.add(row, closed=True)
        inv = row["predicate_source_inventory"]
        family = inv["predicate_family"]
        counts[family] += 1
        batch.append((
            row["Round306B1R0_predicate_source_cell_row_id"], row["formal_member_id"], row["source_signature_row_id"],
            row["source_round"], row["source_table"], row["source_signature_row_sha256"], row["Round182_leaf_row_id"],
            jdump(row["outer_carrier_box"]), family, jdump(inv), row["row_sha256"],
        ))
        if len(batch) >= 1024:
            insert_batch(db, "INSERT INTO r2_cell VALUES(?,?,?,?,?,?,?,?,?,?,?)", batch)
    insert_batch(db, "INSERT INTO r2_cell VALUES(?,?,?,?,?,?,?,?,?,?,?)", batch)
    audits.append(audit.finish())
    return counts


def load_r2_members(pins: PinnedInputs, db: sqlite3.Connection, audits: list[dict[str, Any]]) -> Counter[int]:
    audit = TableAudit("B1R0.members")
    members: list[tuple[Any, ...]] = []
    edges: list[tuple[Any, ...]] = []
    multiplicities: Counter[int] = Counter()
    for row in pins.stream(B1_MEMBER, '"member_union_rows":['):
        need(type(row) is dict, "B1R0 member row")
        audit.add(row, closed=True)
        n = row["predicate_source_cell_multiplicity"]
        multiplicities[n] += 1
        cell_ids = row["predicate_source_cell_row_ids"]
        source_ids = row["source_signature_row_ids"]
        need(len(cell_ids) == len(source_ids) == n, "B1R0 member multiplicity lists")
        members.append((
            row["member_id"], row["Round306B1R0_member_union_row_id"], row["Round294_registry_row_id"],
            row["Round306B0_member_source_row_id"], row["Round306A_component_id"], n, jdump(cell_ids), jdump(source_ids),
            jdump(row["Round271_W_tail_parent_normalization"]) if row["Round271_W_tail_parent_normalization"] is not None else None,
            row["row_sha256"],
        ))
        edges.extend((cell_id, row["member_id"]) for cell_id in cell_ids)
        if len(members) >= 1024:
            insert_batch(db, "INSERT INTO r2_member VALUES(?,?,?,?,?,?,?,?,?,?)", members)
        if len(edges) >= 2048:
            insert_batch(db, "INSERT INTO r2_member_edge VALUES(?,?)", edges)
    insert_batch(db, "INSERT INTO r2_member VALUES(?,?,?,?,?,?,?,?,?,?)", members)
    insert_batch(db, "INSERT INTO r2_member_edge VALUES(?,?)", edges)
    audits.append(audit.finish())
    return multiplicities


def load_r275(pins: PinnedInputs, db: sqlite3.Connection, audits: list[dict[str, Any]]) -> None:
    for table, label in (("strict_region_ledger", "R275.strict"), ("arrangement_region_ledger", "R275.arrangement")):
        audit = TableAudit(label)
        batch: list[tuple[Any, ...]] = []
        for row in pins.stream(R275, '"rows"', anchor=f'"{table}"'):
            need(type(row) is dict, label + ":row")
            audit.add(row, closed=True)
            batch.append((row["reverse_rechart_region_row_id"], jdump(row["adjacent_rational_region_box"]), table, row["row_sha256"]))
            if len(batch) >= 1024:
                insert_batch(db, "INSERT INTO r275 VALUES(?,?,?,?)", batch)
        insert_batch(db, "INSERT INTO r275 VALUES(?,?,?,?)", batch)
        audits.append(audit.finish())


def load_r286(pins: PinnedInputs, db: sqlite3.Connection, audits: list[dict[str, Any]]) -> None:
    audit = TableAudit("R286.rows")
    batch: list[tuple[Any, ...]] = []
    for row in pins.stream(R286, '"rows":['):
        need(type(row) is dict, "R286 row")
        audit.add(row, closed=True)
        batch.append((row["Round286_refinement_cell_id"], row["Round275_region_id"], jdump(row["cell_exact_box"]), row["row_sha256"]))
        if len(batch) >= 1024:
            insert_batch(db, "INSERT INTO r286 VALUES(?,?,?,?)", batch)
    insert_batch(db, "INSERT INTO r286 VALUES(?,?,?,?)", batch)
    audits.append(audit.finish())


def load_r287(pins: PinnedInputs, db: sqlite3.Connection, audits: list[dict[str, Any]]) -> None:
    specs = (("region_rows", "R287.region"), ("refinement_cell_rows", "R287.refinement"))
    for marker_name, label in specs:
        audit = TableAudit(label)
        batch: list[tuple[Any, ...]] = []
        for row in pins.stream(R287, f'"{marker_name}":['):
            need(type(row) is dict, label + ":row")
            audit.add(row, closed=True)
            if marker_name == "region_rows":
                region_id = row["Round275_region_id"]
                source_id = "WHOLE:" + region_id
                source_row_id = row["Round287_region_disposition_row_id"]
                source_kind = "WHOLE_R275"
                coordinate_box = None
            else:
                region_id = row["Round275_region_id"]
                source_id = row["Round286_refinement_cell_id"]
                source_row_id = row["Round287_refinement_cell_disposition_row_id"]
                source_kind = "R286_CELL"
                coordinate_box = jdump(row["coordinate_box"])
            batch.append((source_id, source_row_id, source_kind, row["physical_t_sign"], jdump(row["physical_t_square_open_interval"]), coordinate_box, region_id, row["row_sha256"]))
            if len(batch) >= 1024:
                insert_batch(db, "INSERT INTO r287_source VALUES(?,?,?,?,?,?,?,?)", batch)
        insert_batch(db, "INSERT INTO r287_source VALUES(?,?,?,?,?,?,?,?)", batch)
        audits.append(audit.finish())


def load_r288(pins: PinnedInputs, db: sqlite3.Connection, audits: list[dict[str, Any]]) -> None:
    audit = TableAudit("R288.rows")
    batch: list[tuple[Any, ...]] = []
    for row in pins.stream(R288, '"rows":['):
        need(type(row) is dict, "R288 row")
        audit.add(row, closed=True)
        batch.append((row["Round288_atom_disposition_row_id"], row["canonical_atom_id"], row["row_sha256"]))
        if len(batch) >= 1024:
            insert_batch(db, "INSERT INTO r288 VALUES(?,?,?)", batch)
    insert_batch(db, "INSERT INTO r288 VALUES(?,?,?)", batch)
    audits.append(audit.finish())


def load_r288_overlap(pins: PinnedInputs, db: sqlite3.Connection, audits: list[dict[str, Any]]) -> None:
    audit = TableAudit("R288.overlap")
    batch: list[tuple[Any, ...]] = []
    for row in pins.stream(R288_OVERLAP, '"rows":['):
        need(type(row) is dict, "R288 overlap row")
        audit.add(row, closed=True)
        batch.append((row["Round288_existing_overlap_relation_row_id"], row["canonical_atom_id"], row["row_sha256"]))
        if len(batch) >= 1024:
            insert_batch(db, "INSERT INTO r288_overlap VALUES(?,?,?)", batch)
    insert_batch(db, "INSERT INTO r288_overlap VALUES(?,?,?)", batch)
    audits.append(audit.finish())


def load_r292(pins: PinnedInputs, db: sqlite3.Connection, audits: list[dict[str, Any]]) -> Counter[str]:
    audit = TableAudit("R292.rows")
    cells: list[tuple[Any, ...]] = []
    components: list[tuple[Any, ...]] = []
    edges: list[tuple[Any, ...]] = []
    counts: Counter[str] = Counter()
    for row in pins.stream(R292, '"rows":['):
        need(type(row) is dict, "R292 row")
        audit.add(row, closed=True)
        if "disposition" in row:
            counts[row["disposition"]] += 1
            cells.append((
                row["Round292_R287_existing_overlap_refinement_cell_id"], row["source_Round287_support_cell_id"],
                row["Round292_refined_new_support_component_id"], row["Round287_potential_new_support_union_id"],
                jdump(row["exact_transformed_open_cell"]), row["disposition"], row["existing_occurrence_occupancy_count"],
                jdump(row["existing_occurrence_ids"]), row["row_sha256"],
            ))
        elif "member_refinement_cell_ids" in row:
            counts["COMPONENT_ROW"] += 1
            component_id = row["Round292_refined_new_support_component_id"]
            member_cells = row["member_refinement_cell_ids"]
            components.append((component_id, row["source_Round287_potential_new_support_union_id"], row["member_refinement_cell_count"], jdump(member_cells), row["row_sha256"]))
            edges.extend((component_id, cell_id) for cell_id in member_cells)
        elif "Round292_registry_overlap_row_id" in row:
            counts["REGISTRY_OVERLAP_ROW"] += 1
        else:
            raise PreflightBlocked("unknown R292 heterogeneous row")
        if len(cells) >= 1024:
            insert_batch(db, "INSERT INTO r292_cell VALUES(?,?,?,?,?,?,?,?,?)", cells)
        if len(components) >= 1024:
            insert_batch(db, "INSERT INTO r292_component VALUES(?,?,?,?,?)", components)
        if len(edges) >= 2048:
            insert_batch(db, "INSERT INTO r292_component_edge VALUES(?,?)", edges)
    insert_batch(db, "INSERT INTO r292_cell VALUES(?,?,?,?,?,?,?,?,?)", cells)
    insert_batch(db, "INSERT INTO r292_component VALUES(?,?,?,?,?)", components)
    insert_batch(db, "INSERT INTO r292_component_edge VALUES(?,?)", edges)
    audits.append(audit.finish())
    return counts


def load_registry(pins: PinnedInputs, db: sqlite3.Connection, audits: list[dict[str, Any]]) -> Counter[str]:
    audit = TableAudit("R294.registry")
    batch: list[tuple[Any, ...]] = []
    counts: Counter[str] = Counter()
    for row in pins.stream(R294_REGISTRY, '"rows":['):
        need(type(row) is dict, "R294 registry row")
        audit.add(row, closed=True)
        family = registry_family(row)
        counts[family] += 1
        batch.append((row["Round294_occurrence_registry_row_id"], row["registry_occurrence_id"], family, row["source_row_id"], row["registry_entry_kind"], row["row_sha256"]))
        if len(batch) >= 1024:
            insert_batch(db, "INSERT INTO registry VALUES(?,?,?,?,?,?)", batch)
    insert_batch(db, "INSERT INTO registry VALUES(?,?,?,?,?,?)", batch)
    audits.append(audit.finish())
    return counts


def load_bindings(pins: PinnedInputs, db: sqlite3.Connection, audits: list[dict[str, Any]]) -> Counter[str]:
    audit = TableAudit("R294.bindings")
    batch: list[tuple[Any, ...]] = []
    counts: Counter[str] = Counter()
    for row in pins.stream(R294_BINDINGS, '"rows":['):
        need(type(row) is dict, "R294 binding row")
        audit.add(row, closed=True)
        kind = row["alias_source_kind"]
        counts[kind] += 1
        coordinate = "T2PS" if kind == "ROUND292_R287_EXACT_REFINED_EXISTING_SUBCOVER_CELL" else "TPS"
        batch.append((
            row["Round294_occurrence_representation_binding_row_id"], row["source_representation_id"], kind,
            row.get("source_row_id"), row.get("source_row_sha256"), row.get("source_Round288_atom_disposition_row_id"),
            row.get("source_Round288_atom_disposition_row_sha256"), row["target_registry_occurrence_id"], coordinate, row["row_sha256"],
        ))
        if len(batch) >= 1024:
            insert_batch(db, "INSERT INTO binding VALUES(?,?,?,?,?,?,?,?,?,?)", batch)
    insert_batch(db, "INSERT INTO binding VALUES(?,?,?,?,?,?,?,?,?,?)", batch)
    audits.append(audit.finish())
    return counts


def load_r295a(pins: PinnedInputs, db: sqlite3.Connection, audits: list[dict[str, Any]]) -> None:
    audit = TableAudit("R295A.aliases")
    batch: list[tuple[Any, ...]] = []
    for row in pins.stream(R295A, '"rows":['):
        need(type(row) is dict, "R295A row")
        audit.add(row, closed=True)
        batch.append((row["Round295A_retained_continuation_alias_row_id"], row["target_Round294_occurrence_registry_row_id"], row["target_Round294_registry_occurrence_id"], row["source_Round179_retained_child_row_id"], row["row_sha256"]))
        if len(batch) >= 1024:
            insert_batch(db, "INSERT INTO r295 VALUES(?,?,?,?,?)", batch)
    insert_batch(db, "INSERT INTO r295 VALUES(?,?,?,?,?)", batch)
    audits.append(audit.finish())


def load_b0(pins: PinnedInputs, db: sqlite3.Connection, audits: list[dict[str, Any]]) -> None:
    audit = TableAudit("B0.members")
    batch: list[tuple[Any, ...]] = []
    for row in pins.stream(B0, '"member_support_source_rows":['):
        need(type(row) is dict, "B0 row")
        audit.add(row, closed=True)
        batch.append((row["member_id"], row["Round306B0_member_support_source_row_id"], row["Round306A_component_id"], row["primary_source_package"], row["primary_source_row_id"], row["primary_source_row_sha256"], row["row_sha256"]))
        if len(batch) >= 1024:
            insert_batch(db, "INSERT INTO b0 VALUES(?,?,?,?,?,?,?)", batch)
    insert_batch(db, "INSERT INTO b0 VALUES(?,?,?,?,?,?,?)", batch)
    audits.append(audit.finish())


EXPECTED_REPLAY_COMMITMENTS: dict[str, dict[str, Any]] = {
    "R2_SELECTED_CELL_JOIN": {"row_count": 295_340, "sha256": "fa4492831c7e0d97c66dac0c14d86ab41e45f28c58afe8a9be5f3461a92460ae"},
    "R2_MEMBER_JOIN": {"row_count": 295_336, "sha256": "248a5b68aa60853243e58ca3dd32a05d96a89db285ae1ef43ce57008e574f6cf"},
    "R2_SOURCE_ANTI_JOIN": {"row_count": 640, "sha256": "f48402e51a7065e392589d6c5efc88eb866a34c8fcf5f1f01e17f2f733253a81"},
    "R292_EXACT_CELL_JOIN": {"row_count": 11_852, "sha256": "0816d40d7a06a23062308da985dd376affd81e1123a8e011029611b7fbd3cfab"},
    "R292_COMPONENT_JOIN": {"row_count": 9_404, "sha256": "7eae6af085b2ab26563567e94fac64a3be087156a5013706b0d3b8f54b4120ab"},
    "ALIAS_DISPATCH": {"row_count": 46_564, "sha256": "893739ab4b10d5ea9e619f9606f6c1fadb9116236774f20171e32adc1b05b60b"},
    "R2_R292_B0_OWNER_BACKBINDING": {"row_count": 304_740, "sha256": "c5ed4ebf7866e1842d3486de76184917099236042145e0117a4d148a11b48632"},
}


def validate_r2(db: sqlite3.Connection, family_counts: Counter[str], multiplicities: Counter[int]) -> dict[str, Any]:
    need(family_counts == Counter({
        "OUTGOING_EXACT_HPLUS_HMINUS_SIGN_CELL": 224_840,
        "OUTGOING_W_TAIL_CHILD_FACTOR_CELL": 12,
        "OUTGOING_G_ONE_SIDED_INTERIOR_CELL": 8,
        "WALL_SOURCE_FACTOR_TIMES_HIT_FACTOR_SIGN_CELL": 70_480,
    }), "R2 predicate-family census")
    need(multiplicities == Counter({1: 295_332, 2: 4}), "R2 member multiplicity")
    need(scalar(db, "SELECT COUNT(*) FROM r2_cell") == 295_340, "R2 cell total")
    need(scalar(db, "SELECT COUNT(*) FROM r2_member") == 295_336, "R2 member total")
    need(scalar(db, "SELECT COUNT(*) FROM source") == 295_980, "R2 source universe")
    need(scalar(db, "SELECT COUNT(*) FROM r2_cell c LEFT JOIN source s ON s.source_id=c.source_id WHERE s.source_id IS NULL") == 0, "R2 cell/source missing")
    need(scalar(db, "SELECT COUNT(*) FROM r2_cell c JOIN source s ON s.source_id=c.source_id WHERE c.source_sha<>s.row_sha OR c.source_round<>s.source_round OR c.source_table<>s.table_name OR c.leaf_id<>s.leaf_id") == 0, "R2 source hash/round/table/leaf binding")
    need(scalar(db, "SELECT COUNT(*) FROM source s LEFT JOIN leaf l ON l.leaf_id=s.leaf_id WHERE l.leaf_id IS NULL") == 0, "R2 source/R182 leaf anti-join")
    need(scalar(db, "SELECT COUNT(*) FROM r2_cell c JOIN leaf l ON l.leaf_id=c.leaf_id WHERE c.family<>'OUTGOING_W_TAIL_CHILD_FACTOR_CELL' AND c.carrier_json<>l.box_json") == 0, "R2 nonsplit carrier/R182 box equality")
    w_tail_mismatches = list(db.execute("SELECT c.carrier_json,l.box_json FROM r2_cell c JOIN leaf l ON l.leaf_id=c.leaf_id WHERE c.family='OUTGOING_W_TAIL_CHILD_FACTOR_CELL' AND c.carrier_json<>l.box_json"))
    need(len(w_tail_mismatches) == 12, "R2 W-tail child/parent mismatch census")
    for child_json, parent_json in w_tail_mismatches:
        child, parent = jload(child_json), jload(parent_json)
        need(fraction_box_subset(child, parent) and child[2:] == parent[2:], "R2 W-tail exact t-subdivision of R182 parent")
    need(scalar(db, "SELECT COUNT(*) FROM source s LEFT JOIN r2_cell c ON c.source_id=s.source_id WHERE c.source_id IS NULL") == 640, "R2 excluded source anti-join")
    need(scalar(db, "SELECT COUNT(*) FROM r2_member_edge e LEFT JOIN r2_cell c ON c.cell_id=e.cell_id WHERE c.cell_id IS NULL") == 0, "R2 member/cell missing")
    need(scalar(db, "SELECT COUNT(*) FROM r2_cell c LEFT JOIN r2_member_edge e ON e.cell_id=c.cell_id WHERE e.cell_id IS NULL OR e.member_id<>c.member_id") == 0, "R2 cell/member exhaustion")

    # Source-prefix/predicate and source-sign consistency.
    expected_prefix = {
        "OUTGOING_EXACT_HPLUS_HMINUS_SIGN_CELL": "H_GRID",
        "OUTGOING_W_TAIL_CHILD_FACTOR_CELL": "W_TAIL",
        "OUTGOING_G_ONE_SIDED_INTERIOR_CELL": "G_ONE_SIDED",
        "WALL_SOURCE_FACTOR_TIMES_HIT_FACTOR_SIGN_CELL": "WALL",
    }
    for family, prefix in expected_prefix.items():
        need(scalar(db, "SELECT COUNT(*) FROM r2_cell c JOIN source s ON s.source_id=c.source_id WHERE c.family=? AND s.prefix_kind<>?", (family, prefix)) == 0, "R2 family/source prefix:" + family)
    for inventory_json, hplus, hminus, region_sign in db.execute("SELECT c.inventory_json,s.hplus,s.hminus,s.region_sign FROM r2_cell c JOIN source s ON s.source_id=c.source_id WHERE c.family='OUTGOING_EXACT_HPLUS_HMINUS_SIGN_CELL'"):
        inventory = jload(inventory_json)
        need((inventory["HPLUS_sign"], inventory["HMINUS_sign"], inventory["region_factor_sign"]) == (hplus, hminus, region_sign), "R2 H-grid sign binding")
    need(scalar(db, "SELECT COUNT(*) FROM r2_cell c JOIN source s ON s.source_id=c.source_id WHERE c.family='OUTGOING_G_ONE_SIDED_INTERIOR_CELL' AND (s.excluded_face<>'t=0' OR s.extension IS NULL)") == 0, "G one-sided source fields")
    need(scalar(db, "SELECT COUNT(*) FROM r2_cell c JOIN source s ON s.source_id=c.source_id WHERE c.family='WALL_SOURCE_FACTOR_TIMES_HIT_FACTOR_SIGN_CELL' AND s.product_sign IS NOT NULL AND json_extract(c.inventory_json,'$.region_product_sign')<>s.product_sign") == 0, "wall product-sign binding")

    # Exact four W-tail parent normalizations and child/interface face geometry.
    observed: list[dict[str, Any]] = []
    for member_id, normalization_json in db.execute("SELECT member_id,normalization_json FROM r2_member WHERE multiplicity=2 ORDER BY member_id"):
        normalization = jload(normalization_json)
        observed.append({
            "member_id": member_id,
            "interface": normalization["artificial_interface"]["value"],
            "parent_box": normalization["normalized_parent_box"],
            "children": normalization["source_children"],
        })
        need(normalization["artificial_interface"]["axis"] == "t", "W-tail interface axis")
        need(normalization["interface_is_not_a_physical_support_boundary"] is True and normalization["full_support_credit"] == 0, "W-tail zero-credit interface")
        child_boxes = [jload(row[0]) for child in normalization["source_children"] for row in db.execute("SELECT carrier_json FROM r2_cell WHERE source_id=?", (child,))]
        need(len(child_boxes) == 2, "W-tail two children")
        child_boxes.sort(key=lambda box: Fraction(box[0]))
        interface = normalization["artificial_interface"]["value"]
        need(child_boxes[0][1] == interface and child_boxes[1][0] == interface, "W-tail common t face")
        need(child_boxes[0][2:] == child_boxes[1][2:] == normalization["normalized_parent_box"][2:], "W-tail common p/s trace")
        need([child_boxes[0][0], child_boxes[1][1], *child_boxes[0][2:]] == normalization["normalized_parent_box"], "W-tail parent box restoration")
    need(sorted(observed, key=lambda row: row["member_id"]) == sorted(W_TAIL_REGLUES, key=lambda row: row["member_id"]), "four exact W-tail re-glues")

    # R294 registry and B0 identity backbindings for every R2 member.
    need(scalar(db, "SELECT COUNT(*) FROM r2_member m LEFT JOIN registry r ON r.member_id=m.member_id LEFT JOIN b0 b ON b.member_id=m.member_id WHERE r.member_id IS NULL OR b.member_id IS NULL OR r.family<>'R2' OR m.registry_row_id<>r.registry_row_id OR m.b0_row_id<>b.b0_row_id OR b.primary_source_package<>'R294' OR b.primary_source_row_id<>r.registry_row_id OR b.primary_source_row_sha<>r.row_sha OR m.component_id<>b.component_id") == 0, "R2 registry/B0 backbinding")

    return {
        "source_rows": 295_980,
        "selected_cells": 295_340,
        "excluded_source_rows": 640,
        "members": 295_336,
        "multiplicity_histogram": {str(k): v for k, v in sorted(multiplicities.items())},
        "predicate_family_counts": dict(sorted(family_counts.items())),
        "four_W_tail_re_glues": [dict(row) for row in W_TAIL_REGLUES],
    }


def validate_r292(db: sqlite3.Connection, row_counts: Counter[str]) -> dict[str, Any]:
    uncovered = "EXACT_UNCOVERED_POSITIVE_OPEN_SLICE__MEMBER_OF_REFINED_PARENT_LOCAL_NEW_SUPPORT"
    occupied = "EXACT_EXISTING_OCCURRENCE_REPRESENTATION_SUBCOVER__NO_NEW_OCCURRENCE_ID"
    need(row_counts == Counter({uncovered: 10_252, occupied: 1_600, "COMPONENT_ROW": 9_404, "REGISTRY_OVERLAP_ROW": 1_564}), "R292 heterogeneous row census")
    need(scalar(db, "SELECT COUNT(*) FROM r292_cell") == 11_852, "R292 exact cells")
    need(scalar(db, "SELECT COUNT(DISTINCT source_id) FROM r292_cell") == 10_668, "R292 source parents")
    need(scalar(db, "SELECT COUNT(*) FROM (SELECT source_id FROM r292_cell GROUP BY source_id HAVING COUNT(*)>1)") == 708, "R292 split parents")
    need(scalar(db, "SELECT COUNT(*) FROM r292_cell c LEFT JOIN r287_source s ON s.source_id=c.source_id WHERE s.source_id IS NULL") == 0, "R292/R287 parent anti-join")
    need(scalar(db, "SELECT COUNT(DISTINCT c.source_id) FROM r292_cell c JOIN r287_source s ON s.source_id=c.source_id WHERE s.source_kind='WHOLE_R275'") == 9_128, "R292 WHOLE parent count")
    need(scalar(db, "SELECT COUNT(DISTINCT c.source_id) FROM r292_cell c JOIN r287_source s ON s.source_id=c.source_id WHERE s.source_kind='R286_CELL'") == 1_540, "R292 R286 parent count")
    need(scalar(db, "SELECT COUNT(*) FROM r292_cell c JOIN r287_source s ON s.source_id=c.source_id WHERE s.source_kind='WHOLE_R275'") == 10_296, "R292 WHOLE derived cells")
    need(scalar(db, "SELECT COUNT(*) FROM r292_cell c JOIN r287_source s ON s.source_id=c.source_id WHERE s.source_kind='R286_CELL'") == 1_556, "R292 R286 derived cells")
    need(scalar(db, "SELECT COUNT(*) FROM r287_source s JOIN r286 x ON x.cell_id=s.source_id WHERE s.source_kind='R286_CELL' AND (s.coordinate_box_json<>x.box_json OR s.region_id<>x.region_id)") == 0, "R287/R286 exact cell binding")
    need(scalar(db, "SELECT COUNT(*) FROM r287_source s LEFT JOIN r275 p ON p.region_id=s.region_id WHERE p.region_id IS NULL") == 0, "R287/R275 anti-join")

    # Exact rational T2PS subset and fixed physical sign recovery.
    for cell_box_json, source_kind, sigma, t2_json, coordinate_json, parent_box_json in db.execute("""
        SELECT c.box_json,s.source_kind,s.sigma,s.t2_json,s.coordinate_box_json,p.box_json
        FROM r292_cell c JOIN r287_source s ON s.source_id=c.source_id
        JOIN r275 p ON p.region_id=s.region_id ORDER BY c.cell_id
    """):
        cell = jload(cell_box_json)
        t2 = jload(t2_json)
        base = jload(coordinate_json) if source_kind == "R286_CELL" else jload(parent_box_json)
        parent = [t2[0], t2[1], base[2], base[3], base[4], base[5]]
        need(sigma in (-1, 1), "R292 physical t sign")
        need(Fraction(cell[0]) > 0 and fraction_box_subset(cell, parent), "R292 exact transformed subset")

    need(scalar(db, "SELECT COUNT(*) FROM r292_cell WHERE disposition=? AND (component_id IS NULL OR occupancy<>0)", (uncovered,)) == 0, "R292 uncovered component assignment")
    need(scalar(db, "SELECT COUNT(*) FROM r292_cell WHERE disposition=? AND (component_id IS NOT NULL OR occupancy=0)", (occupied,)) == 0, "R292 occupied alias assignment")
    need(scalar(db, "SELECT COUNT(*) FROM r292_component") == 9_404, "R292 component rows")
    need(scalar(db, "SELECT COUNT(*) FROM r292_component_edge") == 10_252, "R292 component edge count")
    need(scalar(db, "SELECT COUNT(*) FROM r292_component_edge e LEFT JOIN r292_cell c ON c.cell_id=e.cell_id WHERE c.cell_id IS NULL OR c.component_id<>e.component_id OR c.disposition<>?", (uncovered,)) == 0, "R292 component/cell forward binding")
    need(scalar(db, "SELECT COUNT(*) FROM r292_cell c LEFT JOIN r292_component_edge e ON e.cell_id=c.cell_id AND e.component_id=c.component_id WHERE c.disposition=? AND e.cell_id IS NULL", (uncovered,)) == 0, "R292 cell/component reverse binding")
    need(scalar(db, "SELECT COUNT(*) FROM r292_component c WHERE c.declared_count<>(SELECT COUNT(*) FROM r292_component_edge e WHERE e.component_id=c.component_id)") == 0, "R292 declared component sizes")
    need(scalar(db, "SELECT SUM(declared_count-1) FROM r292_component") == 848, "R292 local connectivity rank")
    histogram = {str(size): count for size, count in db.execute("SELECT declared_count,COUNT(*) FROM r292_component GROUP BY declared_count ORDER BY declared_count")}
    need(histogram == {"1": 9124, "2": 80, "3": 12, "4": 88, "5": 84, "10": 16}, "R292 component histogram")
    need(scalar(db, "SELECT COUNT(*) FROM r292_component c LEFT JOIN registry r ON r.source_row_id=c.component_id LEFT JOIN b0 b ON b.member_id=r.member_id WHERE r.member_id IS NULL OR r.family<>'R292' OR b.member_id IS NULL OR b.primary_source_package<>'R294' OR b.primary_source_row_id<>r.registry_row_id OR b.primary_source_row_sha<>r.row_sha") == 0, "R292 registry/B0 backbinding")

    return {
        "R287_source_cells": 10_668,
        "exact_T2PS_cells": 11_852,
        "split_source_cells": 708,
        "occupied_alias_cells": 1_600,
        "uncovered_cells": 10_252,
        "components": 9_404,
        "refined_primary_extras": 848,
        "component_size_histogram": histogram,
        "primary_rule": "AF4D1_CANONICAL_KRUSKAL_WITH_MIN_UNSIGNED_ASCII_CELL_ID_ROOT",
        "AF4D1_candidate_face_order": ["canonical_physical_face_id_ASCII", "min_endpoint_cell_id_ASCII", "max_endpoint_cell_id_ASCII", "source_face_row_id_ASCII"],
        "pullback": "t=sigma*sqrt(u), sigma=R287.physical_t_sign",
    }


def validate_aliases(db: sqlite3.Connection, binding_counts: Counter[str]) -> dict[str, Any]:
    expected_kinds = Counter({
        "ROUND288_EXACT_EQUAL_EXISTING_SUPPORT_ENVELOPE": 36_680,
        "ROUND287_R275_REGION_INCLUSION_SUBCOVER": 2_476,
        "ROUND287_R286_SIGNED_CELL_INCLUSION_SUBCOVER": 5_532,
        "ROUND292_R287_EXACT_REFINED_EXISTING_SUBCOVER_CELL": 1_600,
    })
    need(binding_counts == expected_kinds, "R294 alias source-kind census")
    need(scalar(db, "SELECT COUNT(*) FROM binding b LEFT JOIN registry r ON r.member_id=b.target_member_id WHERE r.member_id IS NULL") == 0, "R294 alias target registry anti-join")
    need(scalar(db, "SELECT COUNT(*) FROM binding b LEFT JOIN b0 x ON x.member_id=b.target_member_id WHERE x.member_id IS NULL") == 0, "R294 alias target B0 anti-join")
    need(scalar(db, "SELECT COUNT(*) FROM binding b LEFT JOIN r288 a ON a.atom_row_id=b.source_atom_row_id WHERE b.source_kind='ROUND288_EXACT_EQUAL_EXISTING_SUPPORT_ENVELOPE' AND (a.atom_row_id IS NULL OR a.row_sha<>b.source_atom_row_sha OR a.atom_id<>b.source_rep_id)") == 0, "R294/R288 atom-disposition binding")
    need(scalar(db, "SELECT COUNT(*) FROM binding b LEFT JOIN r288_overlap o ON o.overlap_row_id=b.source_row_id WHERE b.source_kind='ROUND288_EXACT_EQUAL_EXISTING_SUPPORT_ENVELOPE' AND (o.overlap_row_id IS NULL OR o.row_sha<>b.source_row_sha OR o.atom_id<>b.source_rep_id)") == 0, "R294/R288 exact-overlap relation binding")
    need(scalar(db, "SELECT COUNT(*) FROM binding b LEFT JOIN r287_source s ON s.source_row_id=b.source_row_id WHERE b.source_kind IN ('ROUND287_R275_REGION_INCLUSION_SUBCOVER','ROUND287_R286_SIGNED_CELL_INCLUSION_SUBCOVER') AND (s.source_row_id IS NULL OR s.row_sha<>b.source_row_sha)") == 0, "R294/R287 source binding")
    need(scalar(db, "SELECT COUNT(*) FROM binding b LEFT JOIN r292_cell c ON c.cell_id=b.source_row_id WHERE b.source_kind='ROUND292_R287_EXACT_REFINED_EXISTING_SUBCOVER_CELL' AND (c.cell_id IS NULL OR c.row_sha<>b.source_row_sha OR c.disposition<>'EXACT_EXISTING_OCCURRENCE_REPRESENTATION_SUBCOVER__NO_NEW_OCCURRENCE_ID')") == 0, "R294/R292 source binding")
    need(scalar(db, "SELECT COUNT(*) FROM r295 a LEFT JOIN registry r ON r.registry_row_id=a.target_registry_row_id LEFT JOIN b0 b ON b.member_id=a.target_member_id WHERE r.member_id IS NULL OR r.member_id<>a.target_member_id OR r.family<>'PRESERVED' OR b.member_id IS NULL") == 0, "R295A target registry/B0 binding")
    need(scalar(db, "SELECT COUNT(*) FROM r295 a JOIN binding b ON b.target_member_id=a.target_member_id") == 0, "R294/R295A target-member disjointness")

    cross = Counter()
    for source_kind, family, coordinate, count in db.execute("SELECT b.source_kind,r.family,b.coordinate_system,COUNT(*) FROM binding b JOIN registry r ON r.member_id=b.target_member_id GROUP BY b.source_kind,r.family,b.coordinate_system"):
        cross[(source_kind, family, coordinate)] = count
    expected_cross = Counter({
        ("ROUND288_EXACT_EQUAL_EXISTING_SUPPORT_ENVELOPE", "PRESERVED", "TPS"): 36_680,
        ("ROUND287_R286_SIGNED_CELL_INCLUSION_SUBCOVER", "PRESERVED", "TPS"): 720,
        ("ROUND292_R287_EXACT_REFINED_EXISTING_SUBCOVER_CELL", "PRESERVED", "T2PS"): 1_600,
        ("ROUND287_R275_REGION_INCLUSION_SUBCOVER", "R2", "TPS"): 2_476,
        ("ROUND287_R286_SIGNED_CELL_INCLUSION_SUBCOVER", "R2", "TPS"): 4_812,
    })
    need(cross == expected_cross, "R294 source-kind/target-family/coordinate cross")
    family_counts = {family: count for family, count in db.execute("SELECT r.family,COUNT(*) FROM binding b JOIN registry r ON r.member_id=b.target_member_id GROUP BY r.family ORDER BY r.family")}
    need(family_counts == {"PRESERVED": 39_000, "R2": 7_288}, "R294 target family partition")
    coordinate_counts = {coord: count for coord, count in db.execute("SELECT coordinate_system,COUNT(*) FROM binding GROUP BY coordinate_system ORDER BY coordinate_system")}
    need(coordinate_counts == {"T2PS": 1_600, "TPS": 44_688}, "R294 coordinate partition")
    multiplicity = {str(n): count for n, count in db.execute("SELECT n,COUNT(*) FROM (SELECT target_member_id,COUNT(*) n FROM binding WHERE source_kind='ROUND292_R287_EXACT_REFINED_EXISTING_SUBCOVER_CELL' GROUP BY target_member_id) GROUP BY n ORDER BY n")}
    need(multiplicity == {"1": 396, "2": 208, "3": 12, "4": 20, "6": 32, "10": 32, "20": 8}, "R292 occupied alias owner multiplicity")
    need(scalar(db, "SELECT COUNT(DISTINCT target_member_id) FROM binding WHERE source_kind='ROUND292_R287_EXACT_REFINED_EXISTING_SUBCOVER_CELL'") == 708, "R292 occupied alias owners")

    return {
        "R294_binding_rows": 46_288,
        "R295A_binding_rows": 276,
        "R294_target_family_counts": family_counts,
        "R294_coordinate_counts": coordinate_counts,
        "R292_occupied_alias_distinct_owners": 708,
        "R292_occupied_alias_owner_multiplicity": multiplicity,
        "no_double_consumption_dispatch": {
            "R292_source_dispatch_T2PS": 1_600,
            "R2_target_dispatch_TPS": 7_288,
            "preserved_R294_TPS": 37_400,
            "preserved_R295A_TPS": 276,
            "total_alias_rows": 46_564,
        },
    }


def replay_commitments(db: sqlite3.Connection) -> dict[str, dict[str, Any]]:
    return {
        "R2_SELECTED_CELL_JOIN": stream_commitment(db, """
            SELECT c.cell_id,c.member_id,c.source_id,c.source_round,c.family,c.leaf_id,c.carrier_json,c.source_sha
            FROM r2_cell c ORDER BY c.cell_id COLLATE BINARY
        """, ("cell_id","member_id","source_id","source_round","family","leaf_id","carrier","source_row_sha256"), frozenset({"carrier"})),
        "R2_MEMBER_JOIN": stream_commitment(db, """
            SELECT member_id,member_row_id,registry_row_id,b0_row_id,component_id,multiplicity,cell_ids_json,source_ids_json,normalization_json
            FROM r2_member ORDER BY member_id COLLATE BINARY
        """, ("member_id","member_row_id","registry_row_id","b0_row_id","component_id","multiplicity","cell_ids","source_ids","normalization"), frozenset({"cell_ids","source_ids","normalization"})),
        "R2_SOURCE_ANTI_JOIN": stream_commitment(db, """
            SELECT s.source_id,s.source_round,s.leaf_id,s.row_sha FROM source s LEFT JOIN r2_cell c ON c.source_id=s.source_id
            WHERE c.source_id IS NULL ORDER BY s.source_id COLLATE BINARY
        """, ("source_id","source_round","leaf_id","source_row_sha256")),
        "R292_EXACT_CELL_JOIN": stream_commitment(db, """
            SELECT c.cell_id,c.source_id,c.component_id,c.disposition,c.box_json,s.sigma,s.source_kind,c.existing_ids_json
            FROM r292_cell c JOIN r287_source s ON s.source_id=c.source_id ORDER BY c.cell_id COLLATE BINARY
        """, ("cell_id","source_id","component_id","disposition","box","physical_t_sign","source_kind","existing_occurrence_ids"), frozenset({"box","existing_occurrence_ids"})),
        "R292_COMPONENT_JOIN": stream_commitment(db, """
            SELECT c.component_id,c.declared_count,c.cells_json,MIN(e.cell_id),r.member_id
            FROM r292_component c JOIN r292_component_edge e ON e.component_id=c.component_id
            JOIN registry r ON r.source_row_id=c.component_id
            GROUP BY c.component_id,c.declared_count,c.cells_json,r.member_id ORDER BY c.component_id COLLATE BINARY
        """, ("component_id","cell_count","cell_ids","primary_cell_id","member_id"), frozenset({"cell_ids"})),
        "ALIAS_DISPATCH": stream_commitment(db, """
            SELECT package,row_id,source_rep_id,source_kind,target_member_id,target_family,coordinate_system FROM (
              SELECT 'R294' package,b.binding_row_id row_id,b.source_rep_id,b.source_kind,b.target_member_id,r.family target_family,b.coordinate_system
              FROM binding b JOIN registry r ON r.member_id=b.target_member_id
              UNION ALL
              SELECT 'R295A',a.alias_row_id,a.source_rep_id,'R295A_POSITIVE_T_CONTINUATION',a.target_member_id,r.family,'TPS'
              FROM r295 a JOIN registry r ON r.registry_row_id=a.target_registry_row_id
            ) ORDER BY package COLLATE BINARY,row_id COLLATE BINARY
        """, ("package","row_id","source_representation_id","source_kind","target_member_id","target_family","coordinate_system")),
        "R2_R292_B0_OWNER_BACKBINDING": stream_commitment(db, """
            SELECT r.member_id,r.family,r.registry_row_id,b.b0_row_id,b.component_id,r.row_sha,b.row_sha
            FROM registry r JOIN b0 b ON b.member_id=r.member_id WHERE r.family IN ('R2','R292')
            ORDER BY r.member_id COLLATE BINARY
        """, ("member_id","family","registry_row_id","B0_row_id","B0_component_id","registry_row_sha256","B0_row_sha256")),
    }


def full_replay() -> dict[str, Any]:
    # The path is resolved only in this explicitly read-only replay mode.
    directory = os.path.dirname(os.path.abspath(__file__))
    temporary_root, deliverables_real, root_identity = checked_temporary_root(directory)
    audits: list[dict[str, Any]] = []
    with PinnedInputs(directory) as pins:
        with tempfile.TemporaryDirectory(
            prefix="cm2-af4r1-readonly-spill-", dir=temporary_root,
        ) as temporary:
            temporary_real = checked_created_temporary_directory(
                temporary, temporary_root, deliverables_real, root_identity,
            )
            database_path = os.path.join(temporary_real, "replay.sqlite3")
            db = open_database(database_path)
            try:
                with db:
                    load_r182(pins, db, audits)
                    load_source_table(pins, db, audits, R269, 269, "formal_direct_side_signature_ledger", "R269.direct")
                    load_source_table(pins, db, audits, R270, 270, "formal_direct_side_signature_ledger", "R270.direct")
                    load_source_table(pins, db, audits, R271, 271, "formal_side_signature_ledger", "R271.side")
                    load_r271_failclosed(pins, db, audits)
                    load_source_table(pins, db, audits, R272, 272, "formal_side_signature_ledger", "R272.side")
                    r2_families = load_r2_cells(pins, db, audits)
                    r2_multiplicity = load_r2_members(pins, db, audits)
                    load_r275(pins, db, audits)
                    load_r286(pins, db, audits)
                    load_r287(pins, db, audits)
                    load_r288(pins, db, audits)
                    load_r288_overlap(pins, db, audits)
                    r292_rows = load_r292(pins, db, audits)
                    registry_counts = load_registry(pins, db, audits)
                    binding_counts = load_bindings(pins, db, audits)
                    load_r295a(pins, db, audits)
                    load_b0(pins, db, audits)
                    create_replay_indexes(db)
                need(registry_counts == Counter({"PRESERVED": 126_468, "R2": 295_336, "R292": 9_404}), "R294 registry family census")
                r2 = validate_r2(db, r2_families, r2_multiplicity)
                r292 = validate_r292(db, r292_rows)
                aliases = validate_aliases(db, binding_counts)
                commitments = replay_commitments(db)
                if EXPECTED_REPLAY_COMMITMENTS:
                    need(commitments == EXPECTED_REPLAY_COMMITMENTS, "frozen replay commitments")
            finally:
                db.close()
        pin_rows = list(pins.verification_rows)

    body = {
        "schema": SCHEMA + ".full-replay.v1",
        "status": "PASS_EXACT_READ_ONLY_R2_R292_JOIN_PREFLIGHT__ZERO_FORMAL_CREDIT",
        "input_pin_count": len(INPUT_PINS),
        "input_bytes": sum(row[2] for row in INPUT_PINS),
        "input_pin_set_sha256": digest(INPUT_PINS),
        "two_pass_held_fd_pins": pin_rows,
        "table_audits": audits,
        "R2": r2,
        "R292": r292,
        "representation_aliases": aliases,
        "canonical_sorted_stream_commitments": commitments,
        "parser": {
            "kind": "PIN_FIRST_INCREMENTAL_JSON_ARRAY_SLICE_DECODER",
            "upstream_python_imported": False,
            "upstream_python_executed": False,
            "external_JSON_tool_executed": False,
            "maximum_decoded_source_slice_bytes": MAX_DECODED_CANONICAL_ROW_BYTES,
            "maximum_decoded_canonical_serialization_bytes": MAX_DECODED_CANONICAL_ROW_BYTES,
            "stream_read_chunk_characters": STREAM_READ_CHUNK_CHARACTERS,
            "maximum_read_chunk_UTF8_bytes": MAX_READ_CHUNK_UTF8_BYTES,
            "maximum_parser_buffer_UTF8_bytes": MAX_PARSER_BUFFER_UTF8_BYTES,
            "every_buffer_append_checked": True,
            "successful_decode_source_slice_and_canonical_serialization_checked": True,
            "NaN_and_Infinity_parse_constants_rejected": True,
            "strict_row_JSON_and_single_comma_array_separators": True,
            "generic_outer_envelope_or_suffix_parser": False,
            "outer_envelope_integrity_supplied_by_prior_exact_two_pass_raw_byte_pin": True,
        },
        "spill": {
            "kind": "EPHEMERAL_SQLITE_OUTSIDE_DELIVERABLES",
            "sqlite_page_cache_configuration_KiB": 32_768,
            "temp_store": "FILE",
            "temporary_root_source": "realpath(tempfile.gettempdir())",
            "temporary_root_checked_outside_real_deliverables_before_creation": True,
            "TemporaryDirectory_explicit_dir_is_checked_root": True,
            "created_directory_realpath_and_stat_rechecked_before_SQLite_open": True,
            "checked_root_directory_identity_rechecked_before_SQLite_open": True,
            "TMPDIR_inside_deliverables_fails_before_database_open": True,
            "persistent_output_files": 0,
            "measured_peak_RSS_claimed": False,
        },
        "formal_credit": 0,
        "candidate_files_written": 0,
        "production_files_written": 0,
        "blockers": list(FORMAL_BLOCKERS),
    }
    return {**body, "full_replay_digest_sha256": digest(body)}


def contract() -> dict[str, Any]:
    pins = [
        {"label": label, "filename": filename, "exact_size": size, "sha256": sha}
        for label, filename, size, sha in INPUT_PINS
    ]
    body = {
        "schema": SCHEMA,
        "status": STATUS,
        "scope": {
            "read_only_full_replay": True,
            "formal_constructor": False,
            "candidate_is_formal": False,
            "formal_member_support_credit": 0,
            "formal_representation_cover_credit": 0,
            "maximality_credit": 0,
            "D02": "BLOCKED",
            "CM2": "NO_GO_FOR_CLAIM",
        },
        "immutable_inputs": {
            "pin_count": len(pins),
            "total_bytes": sum(row["exact_size"] for row in pins),
            "pins": pins,
            "pin_set_sha256": digest(INPUT_PINS),
            "held_dirfd": True,
            "O_NOFOLLOW": True,
            "regular_file_and_nlink_one": True,
            "two_pass_raw_byte_hash": True,
            "parse_from_held_fd": True,
            "upstream_python_imported_or_executed": False,
        },
        "R2_exact_join": {
            "source_rows": 295_980,
            "selected_source_cells": 295_340,
            "member_count": 295_336,
            "source_exclusion_anti_join": 640,
            "multiplicity_histogram": {"1": 295_332, "2": 4},
            "predicate_families": {
                "OUTGOING_EXACT_HPLUS_HMINUS_SIGN_CELL": 224_840,
                "OUTGOING_W_TAIL_CHILD_FACTOR_CELL": 12,
                "OUTGOING_G_ONE_SIDED_INTERIOR_CELL": 8,
                "WALL_SOURCE_FACTOR_TIMES_HIT_FACTOR_SIGN_CELL": 70_480,
            },
            "predicate_AST_blueprint": {
                "base": "OPEN_BOX(t,p,s) AND SIGN(HPLUS,hplus) AND SIGN(HMINUS,hminus)",
                "wall_extension": "AND SIGN((q_axis-k)*(hit_axis-k),region_product_sign)",
                "HPLUS": "v_x+v_y",
                "HMINUS": "v_x-v_y",
                "physical_target_radii": {"G": "9/25", "W": "4/25"},
                "required_domains": ["1-t^2>0", "1-p^2>0", "Delta>0", "r!=0"],
                "outgoing_cell_signs": {"E": ["STRICT_POSITIVE", "STRICT_POSITIVE"], "W": ["STRICT_NEGATIVE", "STRICT_NEGATIVE"], "N": ["STRICT_POSITIVE", "STRICT_NEGATIVE"], "S": ["STRICT_NEGATIVE", "STRICT_POSITIVE"]},
                "materialized_as_formal_AST": False,
            },
            "four_W_tail_re_glues": [dict(row) for row in W_TAIL_REGLUES],
            "common_face_blueprint": "EQ_ZERO(t-interface) AND OPEN_BOX(p,s) AND COMMON_HPLUS_HMINUS_TRACE; half-open owner=min unsigned-ASCII child ID",
        },
        "R292_exact_join": {
            "R287_source_cells": 10_668,
            "exact_transformed_T2PS_cells": 11_852,
            "split_source_cells": 708,
            "occupied_alias_cells": 1_600,
            "uncovered_cells": 10_252,
            "components": 9_404,
            "local_connectivity_rank": 848,
            "primary_representations": 9_404,
            "refined_primary_extras": 848,
            "physical_sign_source": "R287.physical_t_sign",
            "pullback": "t=sigma*sqrt(u), sigma in {-1,+1}",
            "primary_rule": "AF4D1_CANONICAL_KRUSKAL_WITH_MIN_UNSIGNED_ASCII_CELL_ID_ROOT",
            "AF4D1_candidate_face_order": ["canonical_physical_face_id_ASCII", "min_endpoint_cell_id_ASCII", "max_endpoint_cell_id_ASCII", "source_face_row_id_ASCII"],
            "component_size_histogram": {"1": 9124, "2": 80, "3": 12, "4": 88, "5": 84, "10": 16},
        },
        "alias_dispatch": {
            "R294_rows": 46_288,
            "R295A_rows": 276,
            "R294_target_family_partition": {"PRESERVED": 39_000, "R2": 7_288, "R292": 0},
            "R294_coordinate_partition": {"TPS": 44_688, "T2PS": 1_600},
            "no_double_consumption": {"R292_source_dispatch_T2PS": 1_600, "R2_target_dispatch_TPS": 7_288, "preserved_R294_TPS": 37_400, "preserved_R295A_TPS": 276},
        },
        "deterministic_streams": {
            "names": ["R2_SELECTED_CELL_JOIN", "R2_MEMBER_JOIN", "R2_SOURCE_ANTI_JOIN", "R292_EXACT_CELL_JOIN", "R292_COMPONENT_JOIN", "ALIAS_DISPATCH", "R2_R292_B0_OWNER_BACKBINDING"],
            "ordering": "unsigned ASCII/BINARY on the stated primary ID; alias package then row ID",
            "expected_commitments": EXPECTED_REPLAY_COMMITMENTS,
        },
        "memory_and_spill": {
            "decoded_source_slice_cap_bytes": MAX_DECODED_CANONICAL_ROW_BYTES,
            "decoded_canonical_serialization_cap_bytes": MAX_DECODED_CANONICAL_ROW_BYTES,
            "stream_read_chunk_characters": STREAM_READ_CHUNK_CHARACTERS,
            "maximum_read_chunk_UTF8_bytes": MAX_READ_CHUNK_UTF8_BYTES,
            "parser_buffer_cap_bytes": MAX_PARSER_BUFFER_UTF8_BYTES,
            "parser_buffer_cap_semantics": "decoded-row cap plus one maximum UTF-8 read overhang",
            "SQLite_cache_configuration_KiB": 32_768,
            "SQLite_temp_store": "FILE",
            "spill_location": "ephemeral OS temporary directory outside deliverables",
            "temporary_root_source": "realpath(tempfile.gettempdir())",
            "temporary_root_checked_outside_real_deliverables_before_creation": True,
            "TemporaryDirectory_explicit_dir_is_checked_root": True,
            "created_directory_realpath_and_stat_rechecked_before_SQLite_open": True,
            "checked_root_directory_identity_rechecked_before_SQLite_open": True,
            "TMPDIR_inside_deliverables_fails_before_database_open": True,
            "persistent_spill": False,
            "measured_peak_RSS_claimed": False,
        },
        "parser_trust_domain": {
            "pin_must_pass_before_any_array_decode": True,
            "row_JSON_is_strict_duplicate_key_and_nonintegral_number_rejecting": True,
            "array_requires_exactly_one_comma_between_rows_and_forbids_leading_or_trailing_comma": True,
            "decoded_row_cap_applies_to": ["SUCCESSFUL_SOURCE_SLICE_UTF8_BYTES", "DECODED_CANONICAL_SERIALIZATION_BYTES"],
            "every_parser_buffer_append_is_UTF8_byte_cap_checked": True,
            "parser_buffer_cap_includes_one_maximum_UTF8_read_overhang": True,
            "NaN_and_Infinity_parse_constants_rejected": True,
            "generic_outer_JSON_validation": False,
            "outer_prefix_suffix_and_envelope_integrity": "SUPPLIED_ONLY_BY_EXACT_RAW_BYTE_PIN",
        },
        "formal_blockers": list(FORMAL_BLOCKERS),
        "forbidden_modes": {
            "candidate_enabled": False,
            "production_enabled": False,
            "blocked_before_filesystem": True,
            "reason": CANDIDATE_BLOCK_REASON,
        },
    }
    return {**body, "contract_digest_sha256": digest(body)}


def validate_contract(document: dict[str, Any]) -> None:
    # Equality with the independently reconstructed literal document prevents
    # a coherent attacker from mutating a field and merely recomputing the
    # top-level digest.
    need(document == contract(), "exact canonical contract document")
    need(document["schema"] == SCHEMA and document["status"] == STATUS, "contract identity")
    body = dict(document)
    claimed = body.pop("contract_digest_sha256")
    need(claimed == digest(body), "contract digest")
    scope = document["scope"]
    need(scope["read_only_full_replay"] is True and scope["formal_constructor"] is False, "zero-credit scope")
    need(scope["formal_member_support_credit"] == scope["formal_representation_cover_credit"] == scope["maximality_credit"] == 0, "zero theorem credit")
    inputs = document["immutable_inputs"]
    need(inputs["pin_count"] == len(INPUT_PINS) == 22, "exact pin count")
    need(inputs["total_bytes"] == sum(row[2] for row in INPUT_PINS), "pin byte sum")
    need(inputs["pin_set_sha256"] == digest(INPUT_PINS), "pin-set digest")
    need(tuple((row["label"], row["filename"], row["exact_size"], row["sha256"]) for row in inputs["pins"]) == INPUT_PINS, "exact pin rows")
    need(all(inputs[key] is True for key in ("held_dirfd", "O_NOFOLLOW", "regular_file_and_nlink_one", "two_pass_raw_byte_hash", "parse_from_held_fd")), "source security")
    need(document["R2_exact_join"]["selected_source_cells"] == 295_340 and document["R2_exact_join"]["member_count"] == 295_336, "R2 equation")
    need(sum(document["R2_exact_join"]["predicate_families"].values()) == 295_340, "R2 family sum")
    need(len(document["R2_exact_join"]["four_W_tail_re_glues"]) == 4, "four W-tail rows")
    need(document["R292_exact_join"]["exact_transformed_T2PS_cells"] == 11_852 and document["R292_exact_join"]["uncovered_cells"] + document["R292_exact_join"]["occupied_alias_cells"] == 11_852, "R292 exact split")
    need(document["R292_exact_join"]["uncovered_cells"] - document["R292_exact_join"]["components"] == 848, "R292 rank")
    need(document["alias_dispatch"]["R294_target_family_partition"] == {"PRESERVED": 39_000, "R2": 7_288, "R292": 0}, "alias family partition")
    need(document["alias_dispatch"]["R294_coordinate_partition"] == {"TPS": 44_688, "T2PS": 1_600}, "alias coordinate partition")
    spill = document["memory_and_spill"]
    need(
        all(spill[key] is True for key in (
            "temporary_root_checked_outside_real_deliverables_before_creation",
            "TemporaryDirectory_explicit_dir_is_checked_root",
            "created_directory_realpath_and_stat_rechecked_before_SQLite_open",
            "checked_root_directory_identity_rechecked_before_SQLite_open",
            "TMPDIR_inside_deliverables_fails_before_database_open",
        )),
        "exact outside-deliverables temporary spill seal",
    )
    parser_domain = document["parser_trust_domain"]
    need(parser_domain["NaN_and_Infinity_parse_constants_rejected"] is True, "nonfinite JSON constants rejected")
    need(len(document["formal_blockers"]) == len(FORMAL_BLOCKERS) == 9, "exact blockers")
    forbidden = document["forbidden_modes"]
    need(forbidden["candidate_enabled"] is False and forbidden["production_enabled"] is False and forbidden["blocked_before_filesystem"] is True, "forbidden modes")
    need(forbidden["reason"] == CANDIDATE_BLOCK_REASON, "forbidden reason")


def build_candidate(_target: Any = None) -> NoReturn:
    raise PreflightBlocked(CANDIDATE_BLOCK_REASON)


def run_production(_target: Any = None) -> NoReturn:
    raise PreflightBlocked(CANDIDATE_BLOCK_REASON)


def set_path(document: dict[str, Any], path: tuple[Any, ...], value: Any) -> None:
    cursor: Any = document
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = value


def candidate_boundary_probe() -> dict[str, Any]:
    calls = Counter()
    originals = {
        "open": os.open, "stat": os.stat, "lstat": os.lstat, "listdir": os.listdir,
        "scandir": os.scandir, "mkdir": os.mkdir, "replace": os.replace,
    }
    def trap(name: str):
        def blocked(*_args: Any, **_kwargs: Any) -> Any:
            calls[name] += 1
            raise AssertionError("filesystem boundary crossed:" + name)
        return blocked
    try:
        for name in originals:
            setattr(os, name, trap(name))
        for entry in (build_candidate, run_production):
            blocked = False
            try:
                entry("/forbidden")
            except PreflightBlocked as error:
                blocked = str(error) == CANDIDATE_BLOCK_REASON
            need(blocked, "candidate/production exact block")
    finally:
        for name, original in originals.items():
            setattr(os, name, original)
    need(not calls, "candidate/production pre-filesystem")
    for entry in (build_candidate, run_production):
        code = entry.__code__
        need(code.co_names == ("PreflightBlocked", "CANDIDATE_BLOCK_REASON"), "forbidden entry globals")
    return {"filesystem_calls": dict(calls), "candidate_blocked": True, "production_blocked": True}


def hostile_tmpdir_probe() -> dict[str, Any]:
    """Prove TMPDIR=deliverables blocks before pins or SQLite are touched."""
    directory = os.path.dirname(os.path.abspath(__file__))
    original_gettempdir = tempfile.gettempdir
    original_open_database = globals()["open_database"]
    original_pinned_inputs = globals()["PinnedInputs"]
    previous_tmpdir = os.environ.get("TMPDIR")
    database_calls = 0
    pin_context_calls = 0

    def hostile_gettempdir() -> str:
        return os.environ["TMPDIR"]

    def trapped_database(_path: str) -> sqlite3.Connection:
        nonlocal database_calls
        database_calls += 1
        raise AssertionError("database opened under hostile TMPDIR")

    def trapped_pins(_directory: str) -> Any:
        nonlocal pin_context_calls
        pin_context_calls += 1
        raise AssertionError("pinned inputs opened under hostile TMPDIR")

    blocked = False
    try:
        os.environ["TMPDIR"] = directory
        tempfile.gettempdir = hostile_gettempdir
        globals()["open_database"] = trapped_database
        globals()["PinnedInputs"] = trapped_pins
        try:
            full_replay()
        except PreflightBlocked as error:
            blocked = str(error) == "temporary spill root must be outside real deliverables directory"
    finally:
        tempfile.gettempdir = original_gettempdir
        globals()["open_database"] = original_open_database
        globals()["PinnedInputs"] = original_pinned_inputs
        if previous_tmpdir is None:
            os.environ.pop("TMPDIR", None)
        else:
            os.environ["TMPDIR"] = previous_tmpdir
    need(blocked, "hostile TMPDIR=deliverables fail-closed")
    need(database_calls == 0 and pin_context_calls == 0, "hostile TMPDIR blocked before pins and database")
    return {
        "TMPDIR_inside_deliverables_blocked": True,
        "pinned_input_contexts_created": pin_context_calls,
        "database_open_calls": database_calls,
    }


def self_test() -> dict[str, Any]:
    base = contract()
    validate_contract(base)
    mutations: list[tuple[tuple[Any, ...], Any]] = [
        (("status",), "FORMAL"),
        (("scope", "formal_constructor"), True),
        (("scope", "formal_member_support_credit"), 1),
        (("scope", "maximality_credit"), 1),
        (("immutable_inputs", "pin_count"), 19),
        (("immutable_inputs", "total_bytes"), 1),
        (("immutable_inputs", "pin_set_sha256"), "0" * 64),
        (("immutable_inputs", "held_dirfd"), False),
        (("immutable_inputs", "O_NOFOLLOW"), False),
        (("immutable_inputs", "parse_from_held_fd"), False),
        (("R2_exact_join", "selected_source_cells"), 295_339),
        (("R2_exact_join", "member_count"), 295_337),
        (("R2_exact_join", "predicate_families", "OUTGOING_G_ONE_SIDED_INTERIOR_CELL"), 7),
        (("R2_exact_join", "four_W_tail_re_glues"), []),
        (("R292_exact_join", "exact_transformed_T2PS_cells"), 11_851),
        (("R292_exact_join", "uncovered_cells"), 10_251),
        (("R292_exact_join", "components"), 9_403),
        (("alias_dispatch", "R294_target_family_partition", "R292"), 1),
        (("alias_dispatch", "R294_coordinate_partition", "T2PS"), 1_599),
        (("memory_and_spill", "decoded_canonical_serialization_cap_bytes"), MAX_DECODED_CANONICAL_ROW_BYTES + 1),
        (("memory_and_spill", "parser_buffer_cap_bytes"), MAX_PARSER_BUFFER_UTF8_BYTES + 1),
        (("memory_and_spill", "temporary_root_checked_outside_real_deliverables_before_creation"), False),
        (("memory_and_spill", "TemporaryDirectory_explicit_dir_is_checked_root"), False),
        (("memory_and_spill", "created_directory_realpath_and_stat_rechecked_before_SQLite_open"), False),
        (("memory_and_spill", "TMPDIR_inside_deliverables_fails_before_database_open"), False),
        (("parser_trust_domain", "every_parser_buffer_append_is_UTF8_byte_cap_checked"), False),
        (("parser_trust_domain", "parser_buffer_cap_includes_one_maximum_UTF8_read_overhang"), False),
        (("parser_trust_domain", "NaN_and_Infinity_parse_constants_rejected"), False),
        (("formal_blockers",), []),
        (("forbidden_modes", "candidate_enabled"), True),
        (("forbidden_modes", "production_enabled"), True),
        (("forbidden_modes", "blocked_before_filesystem"), False),
        (("forbidden_modes", "reason"), "changed"),
        (("contract_digest_sha256",), "0" * 64),
    ]
    rejected = 0
    for path, value in mutations:
        candidate = copy.deepcopy(base)
        set_path(candidate, path, value)
        if path != ("contract_digest_sha256",):
            body = dict(candidate)
            body.pop("contract_digest_sha256", None)
            candidate["contract_digest_sha256"] = digest(body)
        try:
            validate_contract(candidate)
        except PreflightBlocked:
            rejected += 1
    need(rejected == len(mutations), "all semantic mutations rejected")
    duplicate_rejected = float_rejected = False
    try:
        DECODER.decode('{"x":1,"x":2}')
    except PreflightBlocked:
        duplicate_rejected = True
    try:
        DECODER.decode('{"x":1.5}')
    except PreflightBlocked:
        float_rejected = True
    nonfinite_rejected = 0
    for token in ("NaN", "Infinity", "-Infinity"):
        try:
            DECODER.decode(token)
        except PreflightBlocked:
            nonfinite_rejected += 1
    need(duplicate_rejected and float_rejected and nonfinite_rejected == 3, "strict JSON tests")
    separator_attacks = (
        '{"rows":[{"x":1}{"x":2}]}',
        '{"rows":[,{"x":1}]}',
        '{"rows":[{"x":1},]}',
        '{"rows":[{"x":1},,{"x":2}]}',
    )
    separator_rejected = 0
    for attack in separator_attacks:
        try:
            list(iter_array(io.StringIO(attack), '"rows":['))
        except PreflightBlocked:
            separator_rejected += 1
    need(separator_rejected == len(separator_attacks), "all array separator attacks rejected")
    empty_row_bytes = len(canonical({"x": ""}))
    exact_value = {"x": "a" * (MAX_DECODED_CANONICAL_ROW_BYTES - empty_row_bytes)}
    exact_wire = canonical(exact_value).decode("ascii")
    need(len(exact_wire.encode("utf-8")) == MAX_DECODED_CANONICAL_ROW_BYTES, "exact decoded-row cap fixture")
    parsed = list(iter_array(io.StringIO('{"rows":[' + exact_wire + ']}'), '"rows":['))
    need(parsed == [exact_value], "decoded row exactly at cap accepted")
    del parsed, exact_value, exact_wire
    overflow_value = {"x": "a" * (MAX_DECODED_CANONICAL_ROW_BYTES - empty_row_bytes + 1)}
    overflow_wire = canonical(overflow_value).decode("ascii")
    need(len(overflow_wire.encode("utf-8")) == MAX_DECODED_CANONICAL_ROW_BYTES + 1, "decoded-row cap-plus-one fixture")
    overflow_rejected = False
    try:
        list(iter_array(io.StringIO('{"rows":[' + overflow_wire + ']}'), '"rows":['))
    except PreflightBlocked:
        overflow_rejected = True
    need(overflow_rejected, "decoded row at cap plus one rejected")
    del overflow_value, overflow_wire
    need(fraction_box_subset(["1","2","3","4","5","6"], ["0","3","2","5","4","7"]), "rational subset positive")
    need(not fraction_box_subset(["-1","2","3","4","5","6"], ["0","3","2","5","4","7"]), "rational subset negative")
    hostile_tmpdir = hostile_tmpdir_probe()
    boundary = candidate_boundary_probe()
    return {
        "schema": SCHEMA + ".self-test.v1",
        "status": "PASS_LIGHTWEIGHT_CONTRACT_MUTATION_AND_PREFILESYSTEM_SECURITY_TESTS",
        "semantic_mutations_rejected": rejected,
        "semantic_mutations_total": len(mutations),
        "duplicate_JSON_key_rejected": duplicate_rejected,
        "nonintegral_JSON_number_rejected": float_rejected,
        "NaN_Infinity_constants_rejected": nonfinite_rejected,
        "NaN_Infinity_constants_total": 3,
        "array_separator_attacks_rejected": separator_rejected,
        "array_separator_attacks_total": len(separator_attacks),
        "decoded_row_exact_cap_bytes": MAX_DECODED_CANONICAL_ROW_BYTES,
        "decoded_row_exact_cap_accepted": True,
        "decoded_row_cap_plus_one_rejected": overflow_rejected,
        "maximum_parser_buffer_UTF8_bytes": MAX_PARSER_BUFFER_UTF8_BYTES,
        "generic_outer_JSON_validation_claimed": False,
        "hostile_TMPDIR_boundary": hostile_tmpdir,
        "candidate_boundary": boundary,
        "filesystem_inputs_opened": 0,
        "candidate_or_production_files_written": 0,
        "formal_credit": 0,
    }


def cli(arguments: list[str]) -> int:
    forbidden_tokens = {"--candidate", "--candidate-dir", "--production", "--production-dir"}
    if any(token in forbidden_tokens for token in arguments):
        try:
            build_candidate(None)
        except PreflightBlocked:
            return 1
    parser = argparse.ArgumentParser(add_help=True)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--print-contract", action="store_true")
    modes.add_argument("--self-test", action="store_true")
    modes.add_argument("--full-replay", action="store_true")
    args = parser.parse_args(arguments)
    if args.print_contract:
        print(canonical(contract()).decode("ascii"))
    elif args.self_test:
        print(canonical(self_test()).decode("ascii"))
    elif args.full_replay:
        print(canonical(full_replay()).decode("ascii"))
    return 0


def main() -> int:
    import sys
    return cli(sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())
