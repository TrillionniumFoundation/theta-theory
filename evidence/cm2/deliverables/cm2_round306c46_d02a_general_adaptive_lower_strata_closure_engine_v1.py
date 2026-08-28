#!/usr/bin/env python3
"""C46 D02-A general adaptive lower-strata closure engine, version 1.

This is a fail-closed C41 row-level inventory, sharding, and generation-zero
checkpoint-template engine.  It does **not** claim to solve the lower-strata
mathematics.  Its read-only plan reconstructs every one of the 33,642 C41
residual primary rows and replays selected endpoint/rechart, incidence,
boundary, face/corner, ambient, reflection-field, prefix, and 862-parent Kraft
relationships recorded by C41.  These are not a global closure proof or a
fresh global terminal snapshot.

Installed C42 is the only authority baseline.  The rejected C43 owner-subset
candidate is parsed only as conditional zero-credit evidence: its pairs 592
and 715 remain in the default execution queue and its 1,146/573 projection is
never used as formal accounting.

V1 is deliberately genesis-only: the only accepted checkpoint is generation
zero with the exact all-pending task vector.  Every successor checkpoint is
rejected unconditionally.  Adaptive split/exit data structures below are
future schema exercises only; they are not accepted execution or persistence.
The exact numerical routing, owner oracle, and independent verifier are absent.

Normal read-only use::

  python3.12 -I -B THIS.py --self-test
  python3.12 -I -B THIS.py --plan --shards 64
  python3.12 -I -B THIS.py --checkpoint-template --shards 64 --shard-index 0

All modes emit canonical JSON on stdout.  No mode writes below ``.cm2-runtime``
or installs a candidate, pointer, receipt, seal, status, or authority.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
from fractions import Fraction as Q
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
from typing import Any, Iterator


SELF = Path(__file__).absolute()
ROOT = SELF.parent.parent
RUNTIME = ROOT / ".cm2-runtime"
AUDIT_ROOT = RUNTIME / "audit"

SCHEMA = "cm2.round306c46.d02-a-general-adaptive-lower-strata.v1"
PLAN_SCHEMA = SCHEMA + ".read-only-plan"
TASK_SCHEMA = SCHEMA + ".task-binding"
SHARD_SCHEMA = SCHEMA + ".pair-preserving-shard"
CHECKPOINT_SCHEMA = SCHEMA + ".resumable-checkpoint"
TASK_STATE_SCHEMA = SCHEMA + ".task-state"

C41_TOKEN = "c41-lower-strata-depth3-20260811T023804Z-f997365c91559599"
C41_DIR = RUNTIME / "candidates" / C41_TOKEN
C41_SCHEMA = "cm2.round306c41.d02-lower-strata-depth3-closure.v1"
C41_STATUS = (
    "PASS_C41_DEPTH3_STRICT_ROUTER_PARTIAL__91879_AMBIENT_LEAVES__"
    "572_WHOLE_CELLS_TERMINAL__1152_FORMAL_UNRESOLVED"
)
C41_OBJECT = "b7e47a4ca9d6f4bb1fee10e78877850d5070f6d3c2b06bb0234fbabdaa2b7b24"
C41_MANIFEST_SHA = "86e10532d63269cd0fdd58d541b1984522e9718f4613a5dc83211fe84eb258ba"

C42_TOKEN = "c42-p391-formal-producer-20260811T044500Z-f1"
C42_AUDIT_TOKEN = "c42-independent-audit-20260811T052900Z-p391-f1"
C42_RELEASE = "c42-f1-authority-install-a50914a266af-85a7cd719cee-v1"
C42_DIR = RUNTIME / "candidates" / C42_TOKEN
C42_OBJECT = "a50914a266aff3396054d7f16e91d69db7fa735ad15f01cbf07eee8e708d99d2"
C42_MANIFEST_SHA = "ce1b6260b26a901a9dda3cfbd94eba5a752b5188d6bdbe7c7d3cd7a4d3f7d058"
C42_AUDIT_OBJECT = "85a7cd719cee9dceb1763135f74d50bcf28f78ff2426e65996b975b1def7790c"
C42_RECEIPT_OBJECT = "c5f2eb78a0d9d717326bc57fb14df823ab3c5181e3e613a0327425c5e33e784e"
C42_SEAL_OBJECT = "b321552768a6aeae6c1d229e52b61ca0b4420314234e02e98366153d4156d460"
C42_POINTER_SHA = "fbc5dd3c55bfdd3098ed34ae09ae633a9526a9c9cc6f40b3d87b5669b2ea7f07"
C42_AUDIT_POINTER_SHA = "59aca53c4c35260801b3c559648c88ee974db01ae950f045a5e5aecd64aa36e5"
C42_RECEIPT_FILE_SHA = "3599494ff330a367a6c27ee57c19c01e86626428871d014c9153f290fdfc407f"
C42_SEAL_FILE_SHA = "0e5a76059b2c9407340d88e07f4fcc356d376f5c24b7173e6b95fd5e06bc312d"
C42_CLOSED_PRIMARY_ID = (
    "c41-c2-outer:6711f208eef9b4a3e63d73649ffed9e296c0de107c5f92185489d287908fbad3"
)
C42_CLOSED_AMBIENT_ID = (
    "c41-ambient:01bcc14671eacb7628822945582e307e70cf9fbeeff7f3f47adc6e9597f3ab38"
)

C43_TOKEN = "c43-sole-deficit-owner-closure-20260811T082400Z-f1"
C43_DIR = RUNTIME / "candidates" / C43_TOKEN
C43_SCHEMA = "cm2.round306c43.d02-sole-deficit-owner-closure.v1"
C43_STATUS = (
    "FORMAL_PRODUCER_PASS_C43_OWNER_ELIGIBLE_SUBSET_592_715__"
    "578_PAIRED__1146_UNRESOLVED__PENDING_INDEPENDENT_C43_AUDIT"
)
C43_OBJECT = "79831178f4450c41540b7ff0f51bde96e61517cbc36a2287efbf0a100cba5bbc"
C43_MANIFEST_SHA = "8bc3b4259f7a600260344436cfc337621c532b44514866ed9fb8425a378390ff"
C43_REJECTED_AUDIT_PATH = (
    AUDIT_ROOT
    / "c43-independent-audit-20260811T114800Z-owner-subset-f1"
    / "independent_audit.json"
)
C43_REJECTED_AUDIT_FILE_SHA = (
    "a9043963a154377555aeae2653197c6fd72f9c500c20c9556dc2f66d404ddeb3"
)
C43_REJECTED_AUDIT_OBJECT = (
    "8acaf57389cf4d4e741a1824217eb2f50213b07aeae2c9b10c3c299ee59067d0"
)
C43_REJECTION_REPORT = (
    ROOT / "deliverables/cm2_round306c43_owner_subset_audit_rejection_report_v1.md"
)
C43_REJECTION_REPORT_SHA = (
    "608dbf90c179051d3c8b5a536a8410f9849fb99e36933e78b6e99d5113a1f430"
)

FORMAL_BASELINE = {
    "paired_coarse_cells": 574,
    "whole_representatives": 287,
    "remaining_representatives": 575,
    "unresolved": 1150,
    "unresolved_zero": False,
    "D02": "BLOCKED_BY_1150_COMPLETE_R1648_CONTINUATIONS",
    "D03": "UNAUTHORIZED",
    "D04": "NOT_MINTED",
    "Gate5": "10/18",
    "CM2": "NO-GO_FOR_CLAIM",
}

EXPECTED_LEDGER_COUNTS = {
    "c1_h1_surface_outers": 16_926,
    "endpoint_recharts": 651,
    "c2_surface_outers": 16_440,
    "incidence_outers": 31_138,
    "boundary_corner_outers": 33_642,
    "routed_ambient_cells": 91_879,
    "split_face_adjacency": 56_870,
    "parent_conservation": 862,
}
EXPECTED_PRIMARY_COUNT = 33_642
EXPECTED_DIRECT_ENDPOINT_COUNT = 276
EXPECTED_ORTHOGONAL_ENDPOINT_COUNT = 375
EXPECTED_RESIDUAL_COUNT = 33_642
EXPECTED_COLLISION3_READY_COUNT = 7_463
EXPECTED_TERMINAL_EXCLUDED_COUNT = 50_774
EXPECTED_RATIONAL_BOUNDARY_COUNT = 33_613
EXPECTED_ALGEBRAIC_BOUNDARY_COUNT = 29

PRIMARY_LEDGER_META = {
    "c1_h1_surface_outers": {
        "id_field": "c1_h1_surface_outer_id",
        "schema": C41_SCHEMA + ".c1-h1-surface-outer",
        "family": "C1_H1",
    },
    "endpoint_recharts": {
        "id_field": "endpoint_rechart_id",
        "schema": C41_SCHEMA + ".endpoint-rechart",
        "family": "ENDPOINT_RECHART",
    },
    "c2_surface_outers": {
        "id_field": "c2_surface_outer_id",
        "schema": C41_SCHEMA + ".c2-surface-outer",
        "family": "C2",
    },
}

B0_CLASSIFICATIONS = {
    "UNRESOLVED_C41_C1_OUTGOING_H1_FACTOR_OUTER",
    "UNRESOLVED_C41_COLLISION2_WALL_ENDPOINT_OUTER",
    "UNRESOLVED_C41_COLLISION2_EVALUATION_EXCEPTION_OUTER",
}
EXPECTED_B0_COUNT = 3_443
OWNER_PREREQUISITE_COUNTS = {668: 43, 496: 39, 783: 38, 695: 7}
OWNER_BLOCKED_REQUIREMENTS = {97: (668,), 211: (496, 783), 664: (695,)}
DIRECT_WHOLE_PAIR_COUNTS = {1: 2, 374: 6, 396: 10, 739: 10, 771: 18, 858: 15}
C43_CONDITIONAL_PAIRS = (592, 715)

PRIORITY_RANK = {
    "OWNER_PREREQUISITE": 0,
    "DIRECT_WHOLE_PAIR": 1,
    "REJECTED_C43_CONDITIONAL_REVALIDATION": 2,
    "OWNER_BLOCKED_LOCAL": 3,
    "GENERAL_ENDPOINT_RECHART": 4,
    "GENERAL_C1_H1": 5,
    "GENERAL_C2": 6,
}

EXIT_CLASSES = {
    "STRICT_EXCLUDED",
    "COLLISION3_READY",
    "CONNECTED_TO_KNOWN",
    "STRICT_CEMETERY_DISCONNECTED",
}
SIDE_ORDER = ("REPRESENTATIVE", "REFLECTED")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
RATIONAL = re.compile(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?\Z")


class Rejected(RuntimeError):
    """A fail-closed schema, inventory, or state transition rejection."""


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


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def strict_pairs(label: str):
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(type(key) is str and key not in result,
                 "duplicate JSON key:" + label + ":" + str(key))
            result[key] = value
        return result
    return pairs


def reject_number(label: str):
    def reject(token: str) -> None:
        raise Rejected("noninteger/nonfinite JSON number:" + label + ":" + token)
    return reject


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    need(not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
         "strict JSON encoding:" + label)
    try:
        value = json.loads(
            raw.decode("ascii", "strict"),
            object_pairs_hook=strict_pairs(label),
            parse_float=reject_number(label),
            parse_constant=reject_number(label),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Rejected("strict JSON parse:" + label) from error
    need(type(value) is dict, "JSON top-level object:" + label)
    return value


def fingerprint(info: os.stat_result) -> tuple[int, ...]:
    return (
        info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size,
        info.st_mtime_ns, info.st_ctime_ns, info.st_uid, info.st_gid,
    )


def lexical_no_symlinks(path: Path, label: str) -> None:
    path = path.absolute()
    need(path == ROOT or ROOT in path.parents, label + ": workspace boundary")
    cursor = ROOT
    need(stat.S_ISDIR(os.lstat(cursor).st_mode), label + ": workspace directory")
    for part in path.relative_to(ROOT).parts:
        cursor /= part
        need(not stat.S_ISLNK(os.lstat(cursor).st_mode),
             label + ": no symlink component")


def stable_read(path: Path, label: str, maximum: int = 1 << 31) -> bytes:
    path = path.absolute()
    lexical_no_symlinks(path.parent, label + " parent")
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        before = os.fstat(descriptor)
        need(
            stat.S_ISREG(before.st_mode) and before.st_nlink == 1
            and before.st_uid == os.getuid()
            and 0 <= before.st_size <= maximum,
            label + ": owned singleton bounded regular",
        )
        blocks: list[bytes] = []
        total = 0
        while block := os.read(descriptor, 4 << 20):
            total += len(block)
            need(total <= before.st_size, label + ": stable size bound")
            blocks.append(block)
        after_fd = os.fstat(descriptor)
        after_path = os.stat(path, follow_symlinks=False)
        need(
            total == before.st_size
            and fingerprint(before) == fingerprint(after_fd)
            == fingerprint(after_path),
            label + ": stable fd/path identity",
        )
        return b"".join(blocks)
    finally:
        os.close(descriptor)


def file_sha256(path: Path, label: str) -> str:
    return hashlib.sha256(stable_read(path, label)).hexdigest()


def strict_json_file(path: Path, label: str) -> dict[str, Any]:
    raw = stable_read(path, label)
    need(raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
         label + ": exactly one terminal LF")
    value = strict_json(raw[:-1], label)
    need(canonical(value) == raw[:-1], label + ": canonical JSON bytes")
    return value


def validate_self_hash(
    value: dict[str, Any], closure: str, expected: str, label: str,
) -> None:
    body = dict(value)
    observed = body.pop(closure, None)
    need(
        type(observed) is str and observed == expected
        and HEX64.fullmatch(expected) is not None
        and digest(body) == expected,
        label + ": exact self hash",
    )


def validate_manifest(
    directory: Path, expected_file_sha: str, expected_count: int, label: str,
) -> tuple[dict[str, str], tuple[str, ...]]:
    lexical_no_symlinks(directory, label + " directory")
    info = os.stat(directory, follow_symlinks=False)
    need(stat.S_ISDIR(info.st_mode) and info.st_uid == os.getuid(),
         label + ": owned directory")
    raw = stable_read(directory / "root_manifest.sha256", label + " manifest")
    need(hashlib.sha256(raw).hexdigest() == expected_file_sha,
         label + ": manifest file pin")
    text = raw.decode("ascii", "strict")
    need(text.endswith("\n") and "\r" not in text,
         label + ": manifest newline")
    members: dict[str, str] = {}
    for ordinal, line in enumerate(text.splitlines()):
        match = re.fullmatch(r"([0-9a-f]{64})  ([A-Za-z0-9][A-Za-z0-9_.-]*)", line)
        need(match is not None, f"{label}: manifest grammar:{ordinal}")
        expected, name = match.groups()
        need(name not in members and name != "root_manifest.sha256",
             f"{label}: unique manifest member:{ordinal}")
        members[name] = expected
    need(len(members) == expected_count and list(members) == sorted(members),
         label + ": exact sorted manifest census")
    inventory = tuple(sorted(entry.name for entry in os.scandir(directory)))
    need(inventory == tuple(sorted([*members, "root_manifest.sha256"])),
         label + ": exact manifest directory inventory")
    for name, expected in members.items():
        need(file_sha256(directory / name, label + " member " + name) == expected,
             label + ": member hash:" + name)
    return members, inventory


def reattest_inventory(directory: Path, expected: tuple[str, ...], label: str) -> None:
    observed = tuple(sorted(entry.name for entry in os.scandir(directory)))
    need(observed == expected, label + ": terminal directory inventory")


def iter_ledger(
    directory: Path, descriptor: dict[str, Any], ledger_name: str,
) -> Iterator[dict[str, Any]]:
    required = {
        "filename", "order", "row_count", "row_hash_line_sequence_sha256",
        "sha256", "size",
    }
    need(type(descriptor) is dict and set(descriptor) == required,
         ledger_name + ": exact descriptor keys")
    path = directory / descriptor["filename"]
    lexical_no_symlinks(path.parent, ledger_name + " parent")
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        before = os.fstat(fd)
        need(
            stat.S_ISREG(before.st_mode) and before.st_nlink == 1
            and before.st_uid == os.getuid()
            and before.st_size == descriptor["size"],
            ledger_name + ": stable compressed input",
        )
        compressed_hash = hashlib.sha256()
        while block := os.read(fd, 4 << 20):
            compressed_hash.update(block)
        need(compressed_hash.hexdigest() == descriptor["sha256"],
             ledger_name + ": compressed SHA")
        os.lseek(fd, 0, os.SEEK_SET)
        sequence = hashlib.sha256()
        count = 0
        with os.fdopen(fd, "rb", closefd=False) as raw_stream:
            with gzip.GzipFile(fileobj=raw_stream, mode="rb") as stream:
                for raw in stream:
                    label = f"{ledger_name}:{count}"
                    need(raw.endswith(b"\n"), label + ": terminal LF")
                    row = strict_json(raw[:-1], label)
                    need(canonical(row) + b"\n" == raw,
                         label + ": canonical row")
                    body = dict(row)
                    observed = body.pop("row_sha256", None)
                    need(
                        type(observed) is str
                        and HEX64.fullmatch(observed) is not None
                        and digest(body) == observed,
                        label + ": row self hash",
                    )
                    sequence.update((observed + "\n").encode("ascii"))
                    count += 1
                    yield row
        after_fd = os.fstat(fd)
        after_path = os.stat(path, follow_symlinks=False)
        need(fingerprint(before) == fingerprint(after_fd) == fingerprint(after_path),
             ledger_name + ": terminal stable identity")
        need(
            count == descriptor["row_count"]
            and sequence.hexdigest() == descriptor["row_hash_line_sequence_sha256"],
            ledger_name + ": row census and sequence closure",
        )
    finally:
        os.close(fd)


def zero_credit(value: Any, label: str) -> None:
    need(type(value) is int and value == 0, label + ": exact integer zero credit")


def prefix_free(paths: list[str], label: str) -> None:
    ordered = sorted(paths)
    need(len(ordered) == len(set(ordered)), label + ": unique paths")
    for left, right in zip(ordered, ordered[1:]):
        need(not right.startswith(left), label + ": prefix-free paths")


def validate_installed_c42() -> dict[str, Any]:
    candidate_raw = stable_read(RUNTIME / "c42-current-token", "C42 pointer", 256)
    audit_raw = stable_read(
        RUNTIME / "c42-current-audit-token", "C42 audit pointer", 256
    )
    need(
        candidate_raw == (C42_TOKEN + "\n").encode("ascii")
        and hashlib.sha256(candidate_raw).hexdigest() == C42_POINTER_SHA
        and audit_raw == (C42_AUDIT_TOKEN + "\n").encode("ascii")
        and hashlib.sha256(audit_raw).hexdigest() == C42_AUDIT_POINTER_SHA,
        "installed C42 exact pointer bytes",
    )
    receipt_path = AUDIT_ROOT / C42_RELEASE / "installation_receipt.json"
    receipt_raw = stable_read(receipt_path, "C42 installation receipt", 4 << 20)
    seal_raw = stable_read(RUNTIME / "c42-current-authority-seal", "C42 seal", 1 << 20)
    need(
        hashlib.sha256(receipt_raw).hexdigest() == C42_RECEIPT_FILE_SHA
        and hashlib.sha256(seal_raw).hexdigest() == C42_SEAL_FILE_SHA,
        "C42 installed transaction file pins",
    )
    for path in (
        RUNTIME / "c42-current-token", RUNTIME / "c42-current-audit-token",
        receipt_path, RUNTIME / "c42-current-authority-seal",
    ):
        info = os.stat(path, follow_symlinks=False)
        need(stat.S_IMODE(info.st_mode) == 0o444 and info.st_nlink == 1,
             "C42 installed node mode/link:" + path.name)
    receipt = strict_json(receipt_raw[:-1], "C42 installation receipt")
    seal = strict_json(seal_raw[:-1], "C42 authority seal")
    need(canonical(receipt) + b"\n" == receipt_raw, "C42 receipt canonical")
    need(canonical(seal) + b"\n" == seal_raw, "C42 seal canonical")
    validate_self_hash(
        receipt, "installation_receipt_object_sha256", C42_RECEIPT_OBJECT,
        "C42 receipt",
    )
    validate_self_hash(
        seal, "authority_seal_object_sha256", C42_SEAL_OBJECT, "C42 seal"
    )
    need(
        seal.get("receipt_file_sha256") == C42_RECEIPT_FILE_SHA
        and seal.get("receipt_object_sha256") == C42_RECEIPT_OBJECT
        and seal.get("candidate_object_sha256") == C42_OBJECT
        and seal.get("independent_audit_object_sha256") == C42_AUDIT_OBJECT
        and seal.get("candidate_pointer_sha256") == C42_POINTER_SHA
        and seal.get("audit_pointer_sha256") == C42_AUDIT_POINTER_SHA
        and seal.get("formal_census_after_commit") == {
            "paired_coarse_cells": 574,
            "remaining_representatives": 575,
            "unresolved": 1150,
            "whole_representatives": 287,
        },
        "C42 seal exact receipt/pointer/object/census bindings",
    )
    _members, inventory = validate_manifest(
        C42_DIR, C42_MANIFEST_SHA, 8, "C42 candidate"
    )
    result = strict_json_file(C42_DIR / "result.json", "C42 result")
    validate_self_hash(result, "object_sha256", C42_OBJECT, "C42 result")
    reattest_inventory(C42_DIR, inventory, "C42 candidate")
    return {
        "authority": "INSTALLED_C42_ONLY",
        "candidate_object_sha256": C42_OBJECT,
        "independent_audit_object_sha256": C42_AUDIT_OBJECT,
        "installation_receipt_object_sha256": C42_RECEIPT_OBJECT,
        "authority_seal_object_sha256": C42_SEAL_OBJECT,
        "formal_baseline": FORMAL_BASELINE,
    }


def parse_q(value: Any, label: str) -> Q:
    need(type(value) is str and RATIONAL.fullmatch(value) is not None,
         label + ": exact rational syntax")
    result = Q(value)
    need(qstr(result) == value, label + ": reduced rational")
    return result


def validate_c41_result() -> tuple[dict[str, Any], tuple[str, ...]]:
    _members, inventory = validate_manifest(
        C41_DIR, C41_MANIFEST_SHA, 13, "C41 candidate"
    )
    result = strict_json_file(C41_DIR / "result.json", "C41 result")
    validate_self_hash(result, "object_sha256", C41_OBJECT, "C41 result")
    need(result.get("schema") == C41_SCHEMA and result.get("status") == C41_STATUS,
         "C41 result schema/status")
    ledgers = result.get("ledgers")
    need(type(ledgers) is dict, "C41 result ledger map")
    for name, count in EXPECTED_LEDGER_COUNTS.items():
        need(name in ledgers and ledgers[name].get("row_count") == count,
             "C41 exact ledger census:" + name)
    lower = result.get("lower_strata_census", {})
    need(
        lower.get("c1_h1_surface_outer_count") == 16_926
        and lower.get("endpoint_rechart_count") == 651
        and lower.get("c2_surface_outer_count") == 16_440
        and lower.get("incidence_outer_count") == 31_138
        and lower.get("boundary_corner_outer_count") == 33_642
        and lower.get("lower_dimensional_ambient_credit") == 0
        and lower.get("D02_gate_credit") == 0,
        "C41 lower-strata exact census and zero credit",
    )
    terminal = result.get("round144_terminal_census", {})
    need(
        terminal == {
            "CONNECTED_TO_KNOWN": 0,
            "EARLIEST_PREFIX_EXCLUDED": 75_384,
            "SOURCE_GRAZING_OR_CEMETERY": 0,
            "TYPED_EVENT_GRAPH": 296,
            "UNRESOLVED_R1648_CONTINUATION": 1_152,
            "terminal_total": 76_832,
            "unresolved_zero": False,
        },
        "C41 formal terminal census",
    )
    return result, inventory


def validate_primary_row(
    row: dict[str, Any], ledger_name: str, global_surfaces: dict[str, str],
) -> tuple[str, dict[str, Any]]:
    meta = PRIMARY_LEDGER_META[ledger_name]
    need(row.get("schema") == meta["schema"], ledger_name + ": row schema")
    zero_credit(row.get("ambient_or_whole_parent_credit"), ledger_name)
    zero_credit(row.get("D02_gate_credit"), ledger_name)
    primary_id = row.get(meta["id_field"])
    need(type(primary_id) is str and primary_id.startswith("c41-"),
         ledger_name + ": primary id")
    surfaces = row.get("normalized_surfaces")
    need(
        type(surfaces) is list
        and type(row.get("normalized_surface_count")) is int
        and row["normalized_surface_count"] == len(surfaces),
        ledger_name + ": nested normalized-surface census",
    )
    surface_ids: list[str] = []
    for ordinal, surface in enumerate(surfaces):
        need(
            type(surface) is dict
            and surface.get("schema")
            == C41_SCHEMA + ".nested-normalized-surface-registry.v1.entry"
            and surface.get("surface_ordinal") == ordinal,
            ledger_name + ": normalized surface schema/ordinal",
        )
        zero_credit(surface.get("ambient_or_whole_parent_credit"),
                    ledger_name + " surface")
        zero_credit(surface.get("D02_gate_credit"), ledger_name + " surface")
        surface_id = surface.get("normalized_surface_id")
        need(
            type(surface_id) is str
            and surface_id.startswith("c41-normalized-surface:")
            and surface_id not in global_surfaces,
            ledger_name + ": globally unique normalized surface",
        )
        global_surfaces[surface_id] = primary_id
        surface_ids.append(surface_id)
    pair = row.get("pair_index")
    path = row.get("descendant_path")
    need(
        type(pair) is int and 0 <= pair < 862
        and type(path) is str and set(path) <= {"0", "1"}
        and type(row.get("c40_source_leaf_id")) is str,
        ledger_name + ": pair/path/source types",
    )
    return primary_id, {
        "primary_id": primary_id,
        "primary_row_sha256": row["row_sha256"],
        "primary_ledger": ledger_name,
        "primary_family": meta["family"],
        "pair_index": pair,
        "c40_source_leaf_id": row["c40_source_leaf_id"],
        "path": path,
        "residual_classification": row.get("residual_classification"),
        "raw_classification": row.get("raw_classification"),
        "normalized_surface_ids": surface_ids,
        "normalized_surface_count": len(surface_ids),
        "endpoint_dependency_ids": [],
        "endpoint_dependency_row_hashes": [],
        "incidence_ids": [],
        "incidence_row_hashes": [],
    }


def load_primary_graph(
    result: dict[str, Any],
) -> tuple[dict[str, dict[str, Any]], dict[str, str], dict[str, Any]]:
    primary: dict[str, dict[str, Any]] = {}
    global_surfaces: dict[str, str] = {}
    classifications: Counter[str] = Counter()
    surface_distribution: Counter[int] = Counter()
    ledger_census: Counter[str] = Counter()

    for ledger_name in ("c1_h1_surface_outers", "c2_surface_outers"):
        for row in iter_ledger(C41_DIR, result["ledgers"][ledger_name], ledger_name):
            primary_id, compact = validate_primary_row(
                row, ledger_name, global_surfaces
            )
            need(primary_id not in primary, "primary outer id uniqueness")
            primary[primary_id] = compact
            classifications[compact["residual_classification"]] += 1
            surface_distribution[compact["normalized_surface_count"]] += 1
            ledger_census[ledger_name] += 1

    direct_endpoint_count = 0
    orthogonal_endpoint_count = 0
    endpoint_kind_census: Counter[str] = Counter()
    endpoint_ids: set[str] = set()
    for row in iter_ledger(
        C41_DIR, result["ledgers"]["endpoint_recharts"], "endpoint_recharts"
    ):
        endpoint_id = row.get("endpoint_rechart_id")
        need(type(endpoint_id) is str and endpoint_id not in endpoint_ids,
             "endpoint id uniqueness")
        endpoint_ids.add(endpoint_id)
        zero_credit(row.get("ambient_or_whole_parent_credit"), "endpoint")
        zero_credit(row.get("D02_gate_credit"), "endpoint")
        geometry = row.get("endpoint_rechart_geometry")
        need(
            row.get("schema") == PRIMARY_LEDGER_META["endpoint_recharts"]["schema"]
            and row.get("carrier_existence_status")
            == "CERTIFIED_EXACT_ENDPOINT_CARRIER"
            and row.get("certified_carrier_dimension") == 1
            and type(geometry) is dict
            and geometry.get("rechart_route_status")
            == "EXACT_ENDPOINT_CARRIER_RETAINED__RECHART_ROUTE_PENDING",
            "endpoint exact carrier and pending rechart",
        )
        endpoint_kind = geometry.get("endpoint_kind")
        need(endpoint_kind in {
            "ALGEBRAIC_H0_SOURCE_CHART_SEAM",
            "RATIONAL_P_ENDPOINT_STEREOGRAPHIC_RECHART",
        }, "endpoint kind enum")
        endpoint_kind_census[endpoint_kind] += 1
        if row.get("orthogonal_to_primary_residual") is True:
            orthogonal_endpoint_count += 1
            owner = row.get("owning_primary_outer_id")
            need(owner in primary, "orthogonal endpoint owning primary FK")
            compact = primary[owner]
            need(
                row.get("pair_index") == compact["pair_index"]
                and row.get("c40_source_leaf_id") == compact["c40_source_leaf_id"]
                and row.get("descendant_path") == compact["path"]
                and row.get("normalized_surface_count") == 0
                and row.get("normalized_surfaces") == [],
                "orthogonal endpoint exact owner binding",
            )
            compact["endpoint_dependency_ids"].append(endpoint_id)
            compact["endpoint_dependency_row_hashes"].append(row["row_sha256"])
        else:
            direct_endpoint_count += 1
            primary_id, compact = validate_primary_row(
                row, "endpoint_recharts", global_surfaces
            )
            need(primary_id not in primary, "direct endpoint primary uniqueness")
            primary[primary_id] = compact
            classifications[compact["residual_classification"]] += 1
            surface_distribution[compact["normalized_surface_count"]] += 1
            ledger_census["endpoint_recharts:direct"] += 1

    need(
        len(primary) == EXPECTED_PRIMARY_COUNT
        and ledger_census["c1_h1_surface_outers"] == 16_926
        and ledger_census["c2_surface_outers"] == 16_440
        and direct_endpoint_count == EXPECTED_DIRECT_ENDPOINT_COUNT
        and orthogonal_endpoint_count == EXPECTED_ORTHOGONAL_ENDPOINT_COUNT
        and len(endpoint_ids) == EXPECTED_LEDGER_COUNTS["endpoint_recharts"],
        "exact C41 primary and endpoint census",
    )
    return primary, global_surfaces, {
        "primary_family_census": {
            "C1_H1": 16_926,
            "C2": 16_440,
            "ENDPOINT_RECHART": 276,
        },
        "residual_classification_census": dict(sorted(classifications.items())),
        "normalized_surface_count_distribution": {
            str(key): value for key, value in sorted(surface_distribution.items())
        },
        "normalized_surface_total": len(global_surfaces),
        "endpoint_total": len(endpoint_ids),
        "direct_endpoint_primary_count": direct_endpoint_count,
        "orthogonal_endpoint_dependency_count": orthogonal_endpoint_count,
        "endpoint_kind_census": dict(sorted(endpoint_kind_census.items())),
    }


def attach_incidences(
    result: dict[str, Any], primary: dict[str, dict[str, Any]],
    global_surfaces: dict[str, str],
) -> dict[str, Any]:
    seen: set[str] = set()
    pair_keys_by_owner: dict[str, set[tuple[str, str]]] = defaultdict(set)
    count = 0
    for row in iter_ledger(
        C41_DIR, result["ledgers"]["incidence_outers"], "incidence_outers"
    ):
        incidence_id = row.get("incidence_outer_id")
        owner = row.get("owning_outer_id")
        left = row.get("left_normalized_surface_id")
        right = row.get("right_normalized_surface_id")
        need(
            row.get("schema") == C41_SCHEMA + ".incidence-outer"
            and type(incidence_id) is str and incidence_id not in seen
            and owner in primary and left != right
            and global_surfaces.get(left) == owner
            and global_surfaces.get(right) == owner,
            "incidence exact owner/surface foreign keys",
        )
        compact = primary[owner]
        need(
            row.get("pair_index") == compact["pair_index"]
            and row.get("c40_source_leaf_id") == compact["c40_source_leaf_id"]
            and row.get("descendant_path") == compact["path"]
            and row.get("classification")
            == "UNRESOLVED_C41_PAIR_INCIDENCE_KRAWCZYK_PENDING"
            and row.get("certified_intersection_dimension") is None
            and row.get("intersection_existence") is None
            and row.get("rank_status") is None,
            "incidence pending exact schema",
        )
        zero_credit(row.get("ambient_or_whole_parent_credit"), "incidence")
        zero_credit(row.get("D02_gate_credit"), "incidence")
        key = tuple(sorted((left, right)))
        need(key not in pair_keys_by_owner[owner], "incidence pair uniqueness")
        pair_keys_by_owner[owner].add(key)
        compact["incidence_ids"].append(incidence_id)
        compact["incidence_row_hashes"].append(row["row_sha256"])
        seen.add(incidence_id)
        count += 1
    need(count == EXPECTED_LEDGER_COUNTS["incidence_outers"],
         "exact incidence row count")
    owner_count = 0
    for owner, compact in primary.items():
        n = compact["normalized_surface_count"]
        expected = n * (n - 1) // 2
        need(len(compact["incidence_ids"]) == expected,
             "complete all-pairs incidence inventory:" + owner)
        if expected:
            owner_count += 1
    return {
        "incidence_count": count,
        "incidence_owner_count": owner_count,
        "all_normalized_surface_pairs_materialized": True,
        "incidence_ambient_credit": 0,
        "incidence_D02_credit": 0,
    }


def load_split_ids(result: dict[str, Any]) -> set[str]:
    split_ids: set[str] = set()
    count = 0
    for row in iter_ledger(
        C41_DIR, result["ledgers"]["split_face_adjacency"],
        "split_face_adjacency",
    ):
        split_id = row.get("split_face_adjacency_id")
        need(
            row.get("schema") == C41_SCHEMA + ".split-face-adjacency"
            and type(split_id) is str and split_id not in split_ids
            and row.get("exact_split_conservation") == "1"
            and row.get("lower_child_path") == row.get("parent_path", "") + "0"
            and row.get("upper_child_path") == row.get("parent_path", "") + "1"
            and row.get("half_open_shared_face_owner") == "LOWER_BIT_CHILD",
            "split exact binary adjacency",
        )
        zero_credit(row.get("ambient_or_whole_parent_credit"), "split")
        zero_credit(row.get("D02_gate_credit"), "split")
        split_ids.add(split_id)
        count += 1
    need(count == EXPECTED_LEDGER_COUNTS["split_face_adjacency"],
         "exact split row count")
    return split_ids


def attach_boundaries(
    result: dict[str, Any], primary: dict[str, dict[str, Any]],
    split_ids: set[str],
) -> dict[str, Any]:
    seen_boundaries: set[str] = set()
    seen_faces: set[str] = set()
    seen_corners: set[str] = set()
    seen_surface_face_links: set[str] = set()
    shape_census: Counter[str] = Counter()
    for row in iter_ledger(
        C41_DIR, result["ledgers"]["boundary_corner_outers"],
        "boundary_corner_outers",
    ):
        owner = row.get("owning_outer_id")
        boundary_id = row.get("boundary_corner_outer_id")
        need(
            row.get("schema") == C41_SCHEMA + ".boundary-corner-outer"
            and owner in primary and type(boundary_id) is str
            and boundary_id not in seen_boundaries,
            "boundary exact unique owning primary",
        )
        compact = primary[owner]
        need(
            row.get("pair_index") == compact["pair_index"]
            and row.get("c40_source_leaf_id") == compact["c40_source_leaf_id"]
            and row.get("descendant_path") == compact["path"]
            and row.get("face_family")
            == ["t_lower", "t_upper", "p_lower", "p_upper"]
            and row.get("corner_family") == ["t0p0", "t0p1", "t1p0", "t1p1"]
            and row.get("boundary_and_corner_inventory_complete") is False
            and row.get("global_sibling_adjacency_and_half_open_owner_complete")
            is False,
            "boundary pending full owner semantics",
        )
        zero_credit(row.get("ambient_or_whole_parent_credit"), "boundary")
        zero_credit(row.get("D02_gate_credit"), "boundary")
        face_rows = row.get("face_rows")
        corner_rows = row.get("corner_rows")
        need(type(face_rows) is list and type(corner_rows) is list,
             "boundary nested row lists")
        face_count = row.get("exact_face_row_count")
        corner_count = row.get("exact_corner_row_count")
        need(face_count == len(face_rows) and corner_count == len(corner_rows),
             "boundary nested row census")
        if row.get("exact_rational_face_and_corner_geometry_complete") is True:
            need(face_count == 4 and corner_count == 4,
                 "rational four-face/four-corner inventory")
            shape_census["RATIONAL_4_FACE_4_CORNER"] += 1
        else:
            need(face_count == 0 and corner_count == 0,
                 "algebraic endpoint zero rational boundary rows")
            shape_census["ALGEBRAIC_RECHART_0_FACE_0_CORNER"] += 1
        face_ids: list[str] = []
        corner_ids: list[str] = []
        normalized = set(compact["normalized_surface_ids"])
        for face in face_rows:
            face_id = face.get("boundary_face_id")
            need(
                type(face_id) is str and face_id not in seen_faces
                and face.get("global_face_owner_resolved") is False
                and face.get("global_face_owner_rule")
                == "LEXICOGRAPHIC_MINIMUM_AMBIENT_PATH_AMONG_INCIDENT_CELLS",
                "boundary face unresolved global owner",
            )
            zero_credit(face.get("face_ambient_credit"), "boundary face")
            zero_credit(face.get("D02_gate_credit"), "boundary face")
            if face.get("last_split_face") is True:
                need(face.get("split_face_adjacency_id") in split_ids,
                     "boundary face split adjacency FK")
            links = face.get("surface_face_incidence_links")
            need(type(links) is list, "surface-face link list")
            linked: set[str] = set()
            for link in links:
                link_id = link.get("surface_face_incidence_id")
                body = dict(link)
                body.pop("surface_face_incidence_id", None)
                need(
                    type(link_id) is str and link_id not in seen_surface_face_links
                    and link_id == "c41-surface-face-incidence:" + digest(body)
                    and link.get("boundary_face_id") == face_id
                    and link.get("normalized_surface_id") in normalized
                    and link.get("certified_intersection_dimension") is None
                    and link.get("intersection_existence") is None
                    and link.get("rank_status") is None,
                    "surface-face incidence exact pending FK",
                )
                zero_credit(link.get("ambient_or_whole_parent_credit"),
                            "surface-face incidence")
                zero_credit(link.get("D02_gate_credit"),
                            "surface-face incidence")
                linked.add(link["normalized_surface_id"])
                seen_surface_face_links.add(link_id)
            need(linked == normalized, "each face covers every normalized surface")
            seen_faces.add(face_id)
            face_ids.append(face_id)
        for corner in corner_rows:
            corner_id = corner.get("boundary_corner_id")
            need(
                type(corner_id) is str and corner_id not in seen_corners
                and corner.get("global_corner_owner_resolved") is False
                and corner.get("global_corner_owner_rule")
                == "LEXICOGRAPHIC_MINIMUM_AMBIENT_PATH_AMONG_INCIDENT_CELLS"
                and corner.get("surface_corner_incidence_status")
                == "SURFACE_CORNER_CENSUS_PENDING",
                "boundary corner unresolved global owner",
            )
            zero_credit(corner.get("corner_ambient_credit"), "boundary corner")
            zero_credit(corner.get("D02_gate_credit"), "boundary corner")
            seen_corners.add(corner_id)
            corner_ids.append(corner_id)
        compact.update({
            "boundary_id": boundary_id,
            "boundary_row_sha256": row["row_sha256"],
            "face_ids": face_ids,
            "corner_ids": corner_ids,
        })
        seen_boundaries.add(boundary_id)
    need(
        len(seen_boundaries) == EXPECTED_PRIMARY_COUNT
        and all("boundary_id" in row for row in primary.values())
        and shape_census["RATIONAL_4_FACE_4_CORNER"]
        == EXPECTED_RATIONAL_BOUNDARY_COUNT
        and shape_census["ALGEBRAIC_RECHART_0_FACE_0_CORNER"]
        == EXPECTED_ALGEBRAIC_BOUNDARY_COUNT,
        "full boundary/corner ownership inventory census",
    )
    return {
        "boundary_outer_count": len(seen_boundaries),
        "face_row_count": len(seen_faces),
        "corner_row_count": len(seen_corners),
        "surface_face_incidence_link_count": len(seen_surface_face_links),
        "boundary_shape_census": dict(sorted(shape_census.items())),
        "all_global_face_owners_pending_zero_credit": True,
        "all_global_corner_owners_pending_zero_credit": True,
    }


def attach_ambient_and_validate_parents(
    result: dict[str, Any], primary: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    dispositions: Counter[str] = Counter()
    pair_rows: dict[int, list[dict[str, Any]]] = defaultdict(list)
    attached: set[str] = set()
    null_reflection_box_count = 0
    for row in iter_ledger(
        C41_DIR, result["ledgers"]["routed_ambient_cells"],
        "routed_ambient_cells",
    ):
        need(row.get("schema") == C41_SCHEMA + ".routed-ambient-cell",
             "ambient row schema")
        pair = row.get("pair_index")
        path = row.get("path")
        need(type(pair) is int and 0 <= pair < 862
             and type(path) is str and set(path) <= {"0", "1"},
             "ambient pair/path")
        fraction = parse_q(row.get("parent_volume_fraction"), "ambient fraction")
        need(fraction > 0, "ambient positive parent fraction")
        zero_credit(row.get("lower_dimensional_ambient_credit"), "ambient lower")
        zero_credit(row.get("collision3_ready_credit"), "ambient collision3")
        zero_credit(row.get("D02_gate_credit"), "ambient D02")
        family = row.get("disposition_family")
        need(family in {"TERMINAL_EXCLUDED", "RESIDUAL_OUTER", "COLLISION3_READY"},
             "ambient disposition enum")
        dispositions[family] += 1
        if family == "TERMINAL_EXCLUDED":
            need(row.get("local_round144_terminal_credit") == 1
                 and row.get("obligation_ids") == [],
                 "terminal ambient exact local credit")
        else:
            zero_credit(row.get("local_round144_terminal_credit"),
                        "nonterminal ambient local")
        pair_rows[pair].append({
            "path": path,
            "fraction": fraction,
            "family": family,
            "row_sha256": row["row_sha256"],
        })
        if family != "RESIDUAL_OUTER":
            need(row.get("obligation_ids") == [],
                 "nonresidual ambient has no lower obligation")
            continue
        obligations = row.get("obligation_ids")
        need(type(obligations) is list and len(obligations) > 0,
             "residual ambient obligation list")
        owner = obligations[0]
        need(owner in primary and owner not in attached,
             "residual ambient unique primary FK")
        compact = primary[owner]
        expected_obligations = [
            owner,
            *compact["endpoint_dependency_ids"],
            *compact["incidence_ids"],
            compact["boundary_id"],
        ]
        need(
            obligations == expected_obligations
            and row.get("pair_index") == compact["pair_index"]
            and row.get("c40_source_leaf_id") == compact["c40_source_leaf_id"]
            and path == compact["path"]
            and row.get("residual_classification")
            == compact["residual_classification"],
            "ambient exact ordered lower-strata foreign-key closure",
        )
        representative_cell = row.get("representative_cell_id")
        reflected_cell = row.get("reflected_cell_id")
        need(
            type(representative_cell) is str and type(reflected_cell) is str
            and representative_cell.startswith("c32-compact-cell:")
            and reflected_cell.startswith("c32-compact-cell:")
            and representative_cell != reflected_cell,
            "ambient representative/reflected cell binding",
        )
        representative_box = row.get("closed_representative_box")
        reflected_box = row.get("closed_reflected_box")
        need((representative_box is None) == (reflected_box is None),
             "ambient paired reflection box nullity")
        if representative_box is None:
            null_reflection_box_count += 1
        else:
            need(type(representative_box) is dict and type(reflected_box) is dict,
                 "ambient exact paired closed boxes")
        compact.update({
            "ambient_id": row["c41_ambient_cell_id"],
            "ambient_row_sha256": row["row_sha256"],
            "parent_volume_fraction": row["parent_volume_fraction"],
            "representative_cell_id": representative_cell,
            "reflected_cell_id": reflected_cell,
            "representative_box_sha256": digest(representative_box),
            "reflected_box_sha256": digest(reflected_box),
            "obligation_sequence_sha256": digest(obligations),
        })
        attached.add(owner)

    need(
        dispositions == Counter({
            "TERMINAL_EXCLUDED": EXPECTED_TERMINAL_EXCLUDED_COUNT,
            "RESIDUAL_OUTER": EXPECTED_RESIDUAL_COUNT,
            "COLLISION3_READY": EXPECTED_COLLISION3_READY_COUNT,
        })
        and attached == set(primary)
        and null_reflection_box_count == EXPECTED_ALGEBRAIC_BOUNDARY_COUNT,
        "complete ambient disposition/primary/reflection census",
    )

    parents: dict[int, dict[str, Any]] = {}
    for row in iter_ledger(
        C41_DIR, result["ledgers"]["parent_conservation"],
        "parent_conservation",
    ):
        pair = row.get("pair_index")
        need(type(pair) is int and 0 <= pair < 862 and pair not in parents,
             "parent pair unique range")
        rows = pair_rows.get(pair, [])
        paths = [value["path"] for value in rows]
        prefix_free(paths, "parent paths:" + str(pair))
        kraft = sum((value["fraction"] for value in rows), Q(0))
        terminal = sum(
            (value["fraction"] for value in rows
             if value["family"] == "TERMINAL_EXCLUDED"), Q(0)
        )
        unresolved = kraft - terminal
        need(
            kraft == 1
            and row.get("schema") == C41_SCHEMA + ".parent-conservation"
            and row.get("parent_Kraft_conservation") == "1"
            and row.get("path_prefix_free") is True
            and row.get("leaf_count") == len(rows)
            and row.get("terminal_leaf_count")
            == sum(value["family"] == "TERMINAL_EXCLUDED" for value in rows)
            and row.get("nonterminal_leaf_count")
            == sum(value["family"] != "TERMINAL_EXCLUDED" for value in rows)
            and parse_q(row.get("terminal_excluded_parent_volume"),
                        "parent terminal fraction") == terminal
            and parse_q(row.get("unresolved_parent_volume"),
                        "parent unresolved fraction") == unresolved,
            "862-parent prefix/Kraft/fraction conservation:" + str(pair),
        )
        zero_credit(row.get("lower_dimensional_credit"), "parent lower")
        zero_credit(row.get("D02_gate_credit"), "parent D02")
        parents[pair] = row
    need(set(parents) == set(range(862)) and len(pair_rows) == 862,
         "exact 862-parent and ambient pair coverage")
    nonterminal_pairs = {
        pair for pair, rows in pair_rows.items()
        if any(row["family"] != "TERMINAL_EXCLUDED" for row in rows)
    }
    residual_pairs = {
        row["pair_index"] for row in primary.values()
    }
    need(len(nonterminal_pairs) == 576 and residual_pairs == nonterminal_pairs,
         "C41 exact 576 residual representative parents")
    return {
        "ambient_disposition_census": dict(sorted(dispositions.items())),
        "residual_primary_foreign_key_count": len(attached),
        "C41_row_level_representative_reflected_field_count": len(attached),
        "algebraic_null_paired_box_count": null_reflection_box_count,
        "parent_conservation_row_count": len(parents),
        "parent_path_prefix_free_count": len(parents),
        "parent_Kraft_one_count": len(parents),
        "C41_nonterminal_representative_pair_count": len(nonterminal_pairs),
    }


def path_absent(path: Path) -> bool:
    try:
        os.lstat(path)
    except FileNotFoundError:
        return True
    return False


def validate_c43_conditional_overlay(
    primary: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    # The candidate bytes are useful inputs, but the later hostile review is
    # the controlling fact: no C43 pointer/seal exists and no formal count moves.
    _members, inventory = validate_manifest(
        C43_DIR, C43_MANIFEST_SHA, 12, "C43 conditional candidate"
    )
    result = strict_json_file(C43_DIR / "result.json", "C43 conditional result")
    validate_self_hash(result, "object_sha256", C43_OBJECT, "C43 result")
    need(
        result.get("schema") == C43_SCHEMA and result.get("status") == C43_STATUS
        and result.get("formal_producer_run") is True
        and result.get("producer_output_is_authority") is False
        and result.get("formal_authority") is False
        and result.get("authority_pointer_installed") is False
        and result.get("independent_C43_audit_outstanding") is True,
        "C43 producer remains nonauthority",
    )
    installed_c42 = result.get("installed_C42_authority", {})
    need(installed_c42 == {
        "authority_seal_object_sha256": C42_SEAL_OBJECT,
        "candidate_object_sha256": C42_OBJECT,
        "independent_audit_object_sha256": C42_AUDIT_OBJECT,
        "installation_receipt_object_sha256": C42_RECEIPT_OBJECT,
        "root_manifest_sha256": C42_MANIFEST_SHA,
    }, "C43 conditional evidence exact C42 lineage")
    need(
        result.get("closure_census", {}).get("whole_paired_coarse_cell_count") == 578
        and result.get("closure_census", {}).get(
            "remaining_representative_parent_count") == 573
        and result.get("round144_census", {}).get(
            "UNRESOLVED_R1648_CONTINUATION") == 1146,
        "C43 conditional projected census bytes",
    )

    exact_sources: dict[int, str] = {}
    for row in iter_ledger(
        C43_DIR, result["ledgers"]["exact_sources"], "C43 exact_sources"
    ):
        pair = row.get("pair_index")
        owner = row.get("C41_primary_outer_id")
        need(
            row.get("schema") == C43_SCHEMA + ".exact-source"
            and pair in C43_CONDITIONAL_PAIRS and pair not in exact_sources
            and owner in primary and primary[owner]["pair_index"] == pair
            and row.get("C41_candidate_object_sha256") == C41_OBJECT
            and row.get("C41_root_manifest_sha256") == C41_MANIFEST_SHA
            and row.get("C41_primary_outer_row_sha256")
            == primary[owner]["primary_row_sha256"]
            and row.get("C41_ambient_cell_id") == primary[owner]["ambient_id"]
            and row.get("C41_ambient_row_sha256")
            == primary[owner]["ambient_row_sha256"]
            and row.get("C41_boundary_outer_id") == primary[owner]["boundary_id"]
            and row.get("C41_boundary_outer_row_sha256")
            == primary[owner]["boundary_row_sha256"]
            and row.get("producer_output_is_authority") is False
            and row.get("D02_gate_credit") == 0,
            "C43 conditional exact-source to C41 binding",
        )
        exact_sources[pair] = owner
    need(set(exact_sources) == set(C43_CONDITIONAL_PAIRS),
         "C43 conditional exact two-source census")

    blockers: dict[int, tuple[int, ...]] = {}
    eligibility: dict[int, bool] = {}
    for row in iter_ledger(
        C43_DIR, result["ledgers"]["source_preflight"], "C43 source_preflight"
    ):
        pair = row.get("pair_index")
        need(pair in {97, 211, 592, 664, 715} and pair not in blockers,
             "C43 preflight five unique pairs")
        owner_pairs = sorted({
            value["canonical_owner"]["pair_index"]
            for value in row.get("canonical_residual_owner_blockers", [])
            if value["canonical_owner"]["pair_index"] != pair
        })
        blockers[pair] = tuple(owner_pairs)
        eligibility[pair] = row.get("eligible_for_C43_credit") is True
        need(
            row.get("relative_Kraft_sum") == "1"
            and row.get("lower_dimensional_ambient_credit") == 0
            and row.get("D02_gate_credit") == 0,
            "C43 preflight zero-credit Kraft",
        )
    need(
        {pair: blockers[pair] for pair in OWNER_BLOCKED_REQUIREMENTS}
        == OWNER_BLOCKED_REQUIREMENTS
        and eligibility == {97: False, 211: False, 592: True,
                            664: False, 715: True},
        "C43 owner dependency topology",
    )

    rejected_raw = stable_read(
        C43_REJECTED_AUDIT_PATH, "rejected C43 audit object", 8 << 20
    )
    need(hashlib.sha256(rejected_raw).hexdigest() == C43_REJECTED_AUDIT_FILE_SHA,
         "rejected C43 audit file pin")
    rejected = strict_json(rejected_raw[:-1], "rejected C43 audit")
    need(canonical(rejected) + b"\n" == rejected_raw,
         "rejected C43 audit canonical bytes")
    validate_self_hash(
        rejected, "object_sha256", C43_REJECTED_AUDIT_OBJECT,
        "rejected C43 audit",
    )
    report_raw = stable_read(C43_REJECTION_REPORT, "C43 rejection report", 1 << 20)
    need(
        hashlib.sha256(report_raw).hexdigest() == C43_REJECTION_REPORT_SHA
        and b"REJECTED_FOR_AUTHORITY__ZERO_FORMAL_CREDIT" in report_raw,
        "C43 hostile rejection report controls PASS-looking audit object",
    )
    need(all(path_absent(RUNTIME / name) for name in (
        "c43-current-token", "c43-current-audit-token",
        "c43-current-authority-seal",
    )), "no C43 authority pointer or seal")
    reattest_inventory(C43_DIR, inventory, "C43 conditional candidate")
    return {
        "candidate_object_sha256": C43_OBJECT,
        "candidate_manifest_file_sha256": C43_MANIFEST_SHA,
        "rejected_audit_object_sha256": C43_REJECTED_AUDIT_OBJECT,
        "rejection_report_sha256": C43_REJECTION_REPORT_SHA,
        "authority_status": "REJECTED_FOR_AUTHORITY__ZERO_FORMAL_CREDIT",
        "conditional_source_outer_ids": {
            str(pair): exact_sources[pair] for pair in sorted(exact_sources)
        },
        "blocked_pair_owner_prerequisites": {
            str(pair): list(blockers[pair]) for pair in sorted(OWNER_BLOCKED_REQUIREMENTS)
        },
        "conditional_projection_not_formal": {
            "paired": 578, "unresolved": 1146, "remaining": 573,
        },
        "formal_baseline_unchanged": FORMAL_BASELINE,
    }


def sequence_digest(values: list[str]) -> str:
    state = hashlib.sha256()
    for value in values:
        state.update(value.encode("ascii") + b"\n")
    return state.hexdigest()


def task_priority(compact: dict[str, Any], conditional_ids: set[str]) \
        -> tuple[str, int, list[int], list[int]]:
    pair = compact["pair_index"]
    is_b0 = (
        compact["residual_classification"] in B0_CLASSIFICATIONS
        and compact["normalized_surface_count"] == 0
    )
    if compact["primary_id"] in conditional_ids:
        value = "REJECTED_C43_CONDITIONAL_REVALIDATION"
    elif is_b0 and pair in OWNER_PREREQUISITE_COUNTS:
        value = "OWNER_PREREQUISITE"
    elif is_b0 and pair in DIRECT_WHOLE_PAIR_COUNTS:
        value = "DIRECT_WHOLE_PAIR"
    elif is_b0 and pair in OWNER_BLOCKED_REQUIREMENTS:
        value = "OWNER_BLOCKED_LOCAL"
    elif compact["primary_family"] == "ENDPOINT_RECHART":
        value = "GENERAL_ENDPOINT_RECHART"
    elif compact["primary_family"] == "C1_H1":
        value = "GENERAL_C1_H1"
    else:
        value = "GENERAL_C2"
    requires = list(OWNER_BLOCKED_REQUIREMENTS.get(pair, ())) \
        if value == "OWNER_BLOCKED_LOCAL" else []
    unblocks = sorted(
        blocked for blocked, owners in OWNER_BLOCKED_REQUIREMENTS.items()
        if value == "OWNER_PREREQUISITE" and pair in owners
    )
    return value, PRIORITY_RANK[value], requires, unblocks


def build_tasks(
    primary: dict[str, dict[str, Any]], c43: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    conditional_ids = set(c43["conditional_source_outer_ids"].values())
    need(C42_CLOSED_PRIMARY_ID in primary
         and primary[C42_CLOSED_PRIMARY_ID]["pair_index"] == 391
         and primary[C42_CLOSED_PRIMARY_ID]["ambient_id"] == C42_CLOSED_AMBIENT_ID,
         "exact installed C42 closed C41 source")
    tasks: list[dict[str, Any]] = []
    priority_census: Counter[str] = Counter()
    queue_state_census: Counter[str] = Counter()
    b0_count = 0
    for primary_id, compact in primary.items():
        is_b0 = (
            compact["residual_classification"] in B0_CLASSIFICATIONS
            and compact["normalized_surface_count"] == 0
        )
        b0_count += int(is_b0)
        if primary_id == C42_CLOSED_PRIMARY_ID:
            queue_state = "CLOSED_BY_INSTALLED_C42_AUTHORITY"
            priority_class = "INSTALLED_PREDECESSOR_CLOSED"
            priority_rank = -1
            requires: list[int] = []
            unblocks: list[int] = []
        else:
            queue_state = "RESUMABLE_PENDING_ZERO_CREDIT"
            priority_class, priority_rank, requires, unblocks = task_priority(
                compact, conditional_ids
            )
            priority_census[priority_class] += 1
        queue_state_census[queue_state] += 1
        dependencies = {
            "normalized_surface_count": compact["normalized_surface_count"],
            "normalized_surface_ids_sha256": digest(
                compact["normalized_surface_ids"]
            ),
            "endpoint_rechart_count": len(compact["endpoint_dependency_ids"]),
            "endpoint_rechart_ids_sha256": digest(
                compact["endpoint_dependency_ids"]
            ),
            "endpoint_rechart_row_hash_sequence_sha256": sequence_digest(
                compact["endpoint_dependency_row_hashes"]
            ),
            "pair_incidence_count": len(compact["incidence_ids"]),
            "pair_incidence_ids_sha256": digest(compact["incidence_ids"]),
            "pair_incidence_row_hash_sequence_sha256": sequence_digest(
                compact["incidence_row_hashes"]
            ),
            "boundary_outer_id": compact["boundary_id"],
            "boundary_outer_row_sha256": compact["boundary_row_sha256"],
            "face_count": len(compact["face_ids"]),
            "face_ids_sha256": digest(compact["face_ids"]),
            "corner_count": len(compact["corner_ids"]),
            "corner_ids_sha256": digest(compact["corner_ids"]),
            "ordered_C41_obligation_sequence_sha256": compact[
                "obligation_sequence_sha256"
            ],
        }
        dependency_closure = digest(dependencies)
        semantic: dict[str, Any] = {
            "schema": TASK_SCHEMA,
            "C41_candidate_object_sha256": C41_OBJECT,
            "primary_ledger": compact["primary_ledger"],
            "primary_family": compact["primary_family"],
            "primary_outer_id": primary_id,
            "primary_outer_row_sha256": compact["primary_row_sha256"],
            "ambient_cell_id": compact["ambient_id"],
            "ambient_row_sha256": compact["ambient_row_sha256"],
            "pair_index": compact["pair_index"],
            "descendant_path": compact["path"],
            "parent_volume_fraction": compact["parent_volume_fraction"],
            "residual_classification": compact["residual_classification"],
            "raw_classification": compact["raw_classification"],
            "representative_reflected_binding": {
                "representative_cell_id": compact["representative_cell_id"],
                "reflected_cell_id": compact["reflected_cell_id"],
                "representative_box_sha256": compact[
                    "representative_box_sha256"
                ],
                "reflected_box_sha256": compact["reflected_box_sha256"],
                "required_physical_sides": list(SIDE_ORDER),
            },
            "lower_strata_dependencies": dependencies,
            "dependency_closure_sha256": dependency_closure,
            "queue": {
                "state": queue_state,
                "priority_class": priority_class,
                "priority_rank": priority_rank,
                "canonical_owner_prerequisite_pairs": requires,
                "unblocks_sole_deficit_pairs": unblocks,
                "is_B0_zero_surface_task": is_b0,
                "C43_conditional_evidence_present": primary_id in conditional_ids,
                "C43_conditional_evidence_has_formal_credit": False,
            },
            "oracle_gate": {
                "status": "BLOCKED__NO_PINNED_NUMERICAL_ORACLE",
                "adapter_source_sha256": None,
                "split_transitions_enabled": False,
                "exit_transitions_enabled": False,
                "required_independent_implementations": 2,
            },
            "credit_lock": {
                "lower_dimensional_ambient_credit": 0,
                "terminal_credit": 0,
                "whole_parent_credit": 0,
                "D02_gate_credit": 0,
                "formal_credit": 0,
            },
        }
        binding = digest(semantic)
        semantic["task_binding_sha256"] = binding
        semantic["task_id"] = "c46-d02a-task:" + binding
        semantic["estimated_work_units"] = (
            4 + 4 * dependencies["normalized_surface_count"]
            + 8 * dependencies["endpoint_rechart_count"]
            + 8 * dependencies["pair_incidence_count"]
            + 2 * dependencies["face_count"]
            + 2 * dependencies["corner_count"]
        )
        tasks.append(semantic)
    need(b0_count == EXPECTED_B0_COUNT, "exact 3,443 B0 task projection")
    need(
        priority_census["OWNER_PREREQUISITE"]
        == sum(OWNER_PREREQUISITE_COUNTS.values()) == 127
        and priority_census["DIRECT_WHOLE_PAIR"]
        == sum(DIRECT_WHOLE_PAIR_COUNTS.values()) == 61
        and priority_census["OWNER_BLOCKED_LOCAL"] == 3
        and priority_census["REJECTED_C43_CONDITIONAL_REVALIDATION"] == 2
        and queue_state_census == Counter({
            "RESUMABLE_PENDING_ZERO_CREDIT": 33_641,
            "CLOSED_BY_INSTALLED_C42_AUTHORITY": 1,
        }),
        "priority overlay and installed-C42-only queue census",
    )
    tasks.sort(key=lambda row: (
        row["pair_index"], row["descendant_path"], row["primary_outer_id"]
    ))
    need(len(tasks) == EXPECTED_PRIMARY_COUNT
         and len({row["task_id"] for row in tasks}) == EXPECTED_PRIMARY_COUNT,
         "full task count and identity uniqueness")
    return tasks, {
        "full_inventory_task_count": len(tasks),
        "default_execution_queue_count": 33_641,
        "installed_C42_closed_task_count": 1,
        "C43_conditional_rows_still_in_default_queue": 2,
        "priority_census": dict(sorted(priority_census.items())),
        "queue_state_census": dict(sorted(queue_state_census.items())),
        "owner_prerequisite_pair_counts": {
            str(pair): count for pair, count in sorted(OWNER_PREREQUISITE_COUNTS.items())
        },
        "direct_whole_pair_counts": {
            str(pair): count for pair, count in sorted(DIRECT_WHOLE_PAIR_COUNTS.items())
        },
        "owner_blocked_requirements": {
            str(pair): list(owners)
            for pair, owners in sorted(OWNER_BLOCKED_REQUIREMENTS.items())
        },
    }


def assign_pair_preserving_shards(
    tasks: list[dict[str, Any]], shard_count: int,
) -> list[dict[str, Any]]:
    need(type(shard_count) is int and 1 <= shard_count <= 128,
         "shard count in [1,128]")
    selected = [
        row for row in tasks
        if row["queue"]["state"] == "RESUMABLE_PENDING_ZERO_CREDIT"
    ]
    grouped: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in selected:
        grouped[row["pair_index"]].append(row)
    need(len(grouped) == FORMAL_BASELINE["remaining_representatives"],
         "installed-C42 baseline leaves exactly 575 pair groups")
    groups: list[tuple[int, int, int, list[dict[str, Any]]]] = []
    for pair, rows in grouped.items():
        rows.sort(key=lambda row: (
            row["queue"]["priority_rank"], row["descendant_path"],
            row["primary_outer_id"],
        ))
        priority = min(row["queue"]["priority_rank"] for row in rows)
        work = sum(row["estimated_work_units"] for row in rows)
        groups.append((priority, -work, pair, rows))
    groups.sort(key=lambda value: (value[0], value[1], value[2]))

    buckets: list[list[dict[str, Any]]] = [[] for _ in range(shard_count)]
    loads = [0] * shard_count
    pairs_by_shard: list[set[int]] = [set() for _ in range(shard_count)]
    for _priority, negative_work, pair, rows in groups:
        work = -negative_work
        target = min(
            range(shard_count),
            key=lambda index: (loads[index], len(pairs_by_shard[index]), index),
        )
        buckets[target].extend(rows)
        loads[target] += work
        pairs_by_shard[target].add(pair)

    seen_tasks: set[str] = set()
    seen_pairs: dict[int, int] = {}
    shards: list[dict[str, Any]] = []
    for index, rows in enumerate(buckets):
        rows.sort(key=lambda row: (
            row["queue"]["priority_rank"], row["pair_index"],
            row["descendant_path"], row["primary_outer_id"],
        ))
        for row in rows:
            need(row["task_id"] not in seen_tasks, "shard task uniqueness")
            seen_tasks.add(row["task_id"])
            prior = seen_pairs.setdefault(row["pair_index"], index)
            need(prior == index, "pair may not cross shard boundary")
        priority = Counter(row["queue"]["priority_class"] for row in rows)
        family = Counter(row["primary_family"] for row in rows)
        binding_sequence = [row["task_binding_sha256"] for row in rows]
        semantic: dict[str, Any] = {
            "schema": SHARD_SCHEMA,
            "shard_index": index,
            "pair_count": len(pairs_by_shard[index]),
            "pair_indices": sorted(pairs_by_shard[index]),
            "task_count": len(rows),
            "estimated_work_units": loads[index],
            "priority_census": dict(sorted(priority.items())),
            "primary_family_census": dict(sorted(family.items())),
            "ordered_task_binding_sequence_sha256": sequence_digest(
                binding_sequence
            ),
            "first_task_id": rows[0]["task_id"] if rows else None,
            "last_task_id": rows[-1]["task_id"] if rows else None,
            "pair_preserving": True,
            "credit": 0,
        }
        semantic["shard_id"] = "c46-d02a-shard:" + digest(semantic)
        semantic["_tasks"] = rows
        shards.append(semantic)
    need(
        len(seen_tasks) == len(selected) == 33_641
        and len(seen_pairs) == 575
        and set(seen_tasks) == {row["task_id"] for row in selected},
        "shard disjoint complete full-queue coverage",
    )
    return shards


def public_shard(shard: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in shard.items() if key != "_tasks"}


def build_read_only_plan(shard_count: int) \
        -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    authority = validate_installed_c42()
    result, c41_inventory = validate_c41_result()
    primary, surfaces, primary_census = load_primary_graph(result)
    incidence_census = attach_incidences(result, primary, surfaces)
    split_ids = load_split_ids(result)
    boundary_census = attach_boundaries(result, primary, split_ids)
    ambient_parent_census = attach_ambient_and_validate_parents(result, primary)
    c43 = validate_c43_conditional_overlay(primary)
    tasks, queue_census = build_tasks(primary, c43)
    shards = assign_pair_preserving_shards(tasks, shard_count)
    pending = [
        row for row in tasks
        if row["queue"]["state"] == "RESUMABLE_PENDING_ZERO_CREDIT"
    ]
    ordered_binding_root = sequence_digest([
        row["task_binding_sha256"] for row in pending
    ])
    all_binding_root = sequence_digest([
        row["task_binding_sha256"] for row in tasks
    ])
    reattest_inventory(C41_DIR, c41_inventory, "C41 candidate")
    semantic: dict[str, Any] = {
        "schema": PLAN_SCHEMA,
        "status": (
            "PASS_READ_ONLY_C46_C41_ROW_LEVEL_INVENTORY_SHARDING__"
            "GENESIS_TEMPLATE_ONLY__INSTALLED_C42_BASELINE__ZERO_CREDIT"
        ),
        "engine_source": {
            "path": str(SELF.relative_to(ROOT)),
            "sha256": file_sha256(SELF, "C46 engine source"),
        },
        "authority_baseline": authority,
        "C41_frozen_inventory": {
            "candidate_path": str(C41_DIR.relative_to(ROOT)),
            "candidate_object_sha256": C41_OBJECT,
            "root_manifest_file_sha256": C41_MANIFEST_SHA,
            "candidate_schema": C41_SCHEMA,
        },
        "C43_conditional_rejected_overlay": c43,
        "full_lower_strata_inventory": {
            **primary_census,
            **incidence_census,
            **boundary_census,
            **ambient_parent_census,
            "split_face_adjacency_count": len(split_ids),
            "primary_residual_outer_count": EXPECTED_PRIMARY_COUNT,
            "C1_H1_plus_direct_endpoint_plus_C2_identity": (
                "16926+276+16440=33642"
            ),
            "replay_scope": "FROZEN_C41_ROWS_AND_SELECTED_INTERNAL_RELATIONSHIPS",
            "C41_row_level_primary_ambient_boundary_endpoint_incidence_FKs_replayed": True,
            "C41_row_level_reflection_fields_replayed": True,
            "C41_row_level_face_corner_and_split_structure_partially_replayed": True,
            "global_reflection_occurrence_closure_claimed": False,
            "global_face_corner_owner_closure_claimed": False,
            "global_split_adjacency_closure_claimed": False,
            "fresh_global_terminal_snapshot_rebuilt": False,
            "ambient_census_scope": "C41_ROUTED_AMBIENT_LEDGER_SNAPSHOT_ONLY",
            "all_lower_dimensional_credit": 0,
        },
        "queue": {
            **queue_census,
            "all_inventory_task_binding_sequence_sha256": all_binding_root,
            "ordered_default_queue_binding_sequence_sha256": ordered_binding_root,
            "default_queue_uses_installed_C42_only": True,
            "installed_C42_closed_source_provenance": (
                "PINNED_CONSTANT_ASSERTION_CROSSCHECKED_TO_C42_ARTIFACT__"
                "NOT_INDEPENDENTLY_DERIVED_FROM_C41_LEDGER"
            ),
            "installed_C42_closed_source_independently_derived_from_C41": False,
            "default_formal_census": FORMAL_BASELINE,
            "C43_1146_573_projection_used_as_formal_baseline": False,
        },
        "sharding": {
            "shard_count": shard_count,
            "nonempty_shard_count": sum(
                shard["task_count"] > 0 for shard in shards
            ),
            "pair_count": 575,
            "task_count": 33_641,
            "pair_preserving": True,
            "shards_disjoint_and_complete": True,
            "shards": [public_shard(shard) for shard in shards],
        },
        "genesis_checkpoint_contract": {
            "accepted_generation": 0,
            "accepted_task_state": "EXACT_ALL_PENDING_VECTOR",
            "successor_checkpoint_supported": False,
            "validate_checkpoint_accepts_non_genesis": False,
            "make_successor_checkpoint": "UNCONDITIONAL_REJECTED",
            "checkpoint_template_is_execution_progress": False,
            "checkpoint_template_credit": 0,
        },
        "future_unexecutable_adaptive_schema": {
            "mathematical_fixed_depth_cap": None,
            "fixed_depth_may_be_used_as_terminal_proof": False,
            "schema_exit_classes": sorted(EXIT_CLASSES),
            "schema_shape_self_tests_only": True,
            "schema_is_verified_execution": False,
            "schema_is_persistable_in_v1_checkpoint": False,
        },
        "implementation_boundary": {
            "implemented": [
                "frozen C41 artifact inventory and row self-hash replay",
                "selected C41 row-level foreign-key and structural checks",
                "C41 row-level reflection fields and 862-parent prefix/Kraft replay",
                "priority overlays and pair-preserving shards",
                "generation-zero exact all-pending checkpoint template",
                "unconditional rejection of every successor checkpoint",
                "future adaptive and exit schema shape self-tests",
                "fail-closed production oracle gate",
            ],
            "not_yet_implemented": [
                "any accepted non-genesis execution checkpoint",
                "exact C1/H1 graph isolation oracle",
                "endpoint/rechart continuation oracle",
                "C2 and 31138-incidence Krawczyk/rank oracle",
                "global face/corner owner reconstruction after adaptive splits",
                "production numerical split-box adapter and cold independent verifier",
            ],
            "full_mathematical_closure_claimed": False,
            "full_run_started": False,
            "production_split_or_exit_transition_enabled": False,
            "global_terminal_snapshot_rebuilt": False,
        },
        "strict_nonpromotion": {
            "runtime_writes_performed": False,
            "candidate_created": False,
            "pointer_or_seal_created": False,
            "ambient_credit": 0,
            "terminal_credit": 0,
            "whole_parent_credit": 0,
            "D02_gate_credit": 0,
            "formal_credit": 0,
            "D02": FORMAL_BASELINE["D02"],
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    semantic["plan_object_sha256"] = digest(semantic)
    return semantic, tasks, shards


def initial_task_state(task: dict[str, Any]) -> dict[str, Any]:
    need(task["queue"]["state"] == "RESUMABLE_PENDING_ZERO_CREDIT",
         "checkpoint only for pending task")
    return {
        "schema": TASK_STATE_SCHEMA,
        "task_id": task["task_id"],
        "task_binding_sha256": task["task_binding_sha256"],
        "pair_index": task["pair_index"],
        "source_descendant_path": task["descendant_path"],
        "dependency_closure_sha256": task["dependency_closure_sha256"],
        "state": "RESUMABLE_PENDING_ZERO_CREDIT",
        "frontier": [{
            "relative_path": "",
            "absolute_path": task["descendant_path"],
            "relative_fraction": "1",
            "state": "RESUMABLE_PENDING_ZERO_CREDIT",
            "reason": "INITIAL_UNROUTED_LOWER_STRATUM",
        }],
        "exits": [],
        "split_events": [],
        "event_count": 0,
        "deepest_additional_depth": 0,
        "relative_Kraft_sum": "1",
        "prefix_free": True,
        "credit_lock": {
            "ambient_credit": 0,
            "terminal_credit": 0,
            "whole_parent_credit": 0,
            "D02_gate_credit": 0,
            "formal_credit": 0,
        },
    }


def validate_task_state(state: dict[str, Any], task: dict[str, Any]) -> None:
    need(
        state.get("schema") == TASK_STATE_SCHEMA
        and state.get("task_id") == task["task_id"]
        and state.get("task_binding_sha256") == task["task_binding_sha256"]
        and state.get("pair_index") == task["pair_index"]
        and state.get("source_descendant_path") == task["descendant_path"]
        and state.get("dependency_closure_sha256")
        == task["dependency_closure_sha256"],
        "task state exact frozen binding",
    )
    frontier = state.get("frontier")
    exits = state.get("exits")
    split_events = state.get("split_events")
    need(type(frontier) is list and type(exits) is list
         and type(split_events) is list,
         "task state frontier/exits/split-event lists")
    all_rows = [*frontier, *exits]
    relative_paths: list[str] = []
    kraft = Q(0)
    for row in all_rows:
        relative = row.get("relative_path")
        need(type(relative) is str and set(relative) <= {"0", "1"},
             "adaptive relative binary path")
        need(row.get("absolute_path") == task["descendant_path"] + relative,
             "adaptive absolute/relative path binding")
        expected = Q(1, 2 ** len(relative))
        need(parse_q(row.get("relative_fraction"), "adaptive leaf fraction")
             == expected, "adaptive exact dyadic leaf fraction")
        relative_paths.append(relative)
        kraft += expected
    prefix_free(relative_paths, "adaptive task leaves")
    need(kraft == 1 and state.get("relative_Kraft_sum") == "1"
         and state.get("prefix_free") is True,
         "adaptive task prefix/Kraft conservation")
    need(all(row.get("state") == "RESUMABLE_PENDING_ZERO_CREDIT"
             for row in frontier), "frontier only resumable pending")
    need(all(
        row.get("state") == "D02_A_EXIT_ZERO_CREDIT"
        and row.get("exit_class") in EXIT_CLASSES
        and type(row.get("certificate")) is dict
        and row.get("certificate_object_sha256")
        == row["certificate"].get("certificate_object_sha256")
        for row in exits
    ), "exit state enum and embedded certificate")
    for row in exits:
        validate_exit_certificate(
            row["certificate"], task, row, row["exit_class"]
        )
    internal_paths = {
        relative[:index]
        for relative in relative_paths
        for index in range(len(relative))
    }
    observed_split_paths: list[str] = []
    for event in split_events:
        event_body = dict(event)
        event_hash = event_body.pop("split_event_object_sha256", None)
        relative = event.get("relative_path")
        need(
            type(event_hash) is str and event_hash == digest(event_body)
            and type(relative) is str and set(relative) <= {"0", "1"}
            and event.get("absolute_path")
            == task["descendant_path"] + relative
            and event.get("split_axis") in {"t", "p"}
            and type(event.get("split_coordinate")) is str
            and RATIONAL.fullmatch(event["split_coordinate"]) is not None
            and type(event.get("split_certificate_sha256")) is str
            and HEX64.fullmatch(event["split_certificate_sha256"])
            is not None
            and event.get("oracle_adapter_source_sha256")
            == task["oracle_gate"]["adapter_source_sha256"],
            "retained exact adaptive split event",
        )
        observed_split_paths.append(relative)
    need(
        len(observed_split_paths) == len(set(observed_split_paths))
        and set(observed_split_paths) == internal_paths,
        "split-event set exactly equals adaptive internal nodes",
    )
    expected_state = (
        "D02_A_SOURCE_CLOSED_ZERO_CREDIT" if not frontier
        else "RESUMABLE_PENDING_ZERO_CREDIT"
    )
    need(state.get("state") == expected_state,
         "task aggregate state follows frontier")
    deepest = max((len(path) for path in relative_paths), default=0)
    need(type(state.get("event_count")) is int
         and state["event_count"] >= len(split_events) + len(exits)
         and state.get("deepest_additional_depth") == deepest,
         "task event/depth counters are exact lower bounds")
    need(state.get("credit_lock") == {
        "ambient_credit": 0, "terminal_credit": 0,
        "whole_parent_credit": 0, "D02_gate_credit": 0,
        "formal_credit": 0,
    }, "task state strict zero-credit lock")


def expected_lower_strata_closure(task: dict[str, Any]) -> dict[str, Any]:
    dependencies = task["lower_strata_dependencies"]
    return {
        "normalized_graph": {
            "expected_count": dependencies["normalized_surface_count"],
            "source_ids_sha256": dependencies[
                "normalized_surface_ids_sha256"
            ],
        },
        "endpoint_recharts": {
            "expected_count": dependencies["endpoint_rechart_count"],
            "source_ids_sha256": dependencies["endpoint_rechart_ids_sha256"],
            "source_row_hash_sequence_sha256": dependencies[
                "endpoint_rechart_row_hash_sequence_sha256"
            ],
        },
        "pair_incidences": {
            "expected_count": dependencies["pair_incidence_count"],
            "source_ids_sha256": dependencies["pair_incidence_ids_sha256"],
            "source_row_hash_sequence_sha256": dependencies[
                "pair_incidence_row_hash_sequence_sha256"
            ],
        },
        "boundary_owner": {
            "expected_count": 1,
            "source_id": dependencies["boundary_outer_id"],
            "source_row_sha256": dependencies["boundary_outer_row_sha256"],
        },
        "face_owners": {
            "expected_count": dependencies["face_count"],
            "source_ids_sha256": dependencies["face_ids_sha256"],
        },
        "corner_owners": {
            "expected_count": dependencies["corner_count"],
            "source_ids_sha256": dependencies["corner_ids_sha256"],
        },
    }


def validate_exit_certificate(
    certificate: dict[str, Any], task: dict[str, Any], leaf: dict[str, Any],
    exit_class: str,
) -> None:
    need(exit_class in EXIT_CLASSES, "D02-A exit class")
    body = dict(certificate)
    observed = body.pop("certificate_object_sha256", None)
    need(type(observed) is str and observed == digest(body),
         "exit certificate self hash")
    need(
        certificate.get("schema") == SCHEMA + ".exit-certificate"
        and certificate.get("exit_class") == exit_class
        and certificate.get("task_id") == task["task_id"]
        and certificate.get("task_binding_sha256")
        == task["task_binding_sha256"]
        and certificate.get("primary_outer_id") == task["primary_outer_id"]
        and certificate.get("ambient_cell_id") == task["ambient_cell_id"]
        and certificate.get("relative_path") == leaf["relative_path"]
        and certificate.get("absolute_path") == leaf["absolute_path"]
        and certificate.get("dependency_closure_sha256")
        == task["dependency_closure_sha256"]
        and certificate.get("oracle_adapter_source_sha256")
        == task["oracle_gate"]["adapter_source_sha256"]
        and certificate.get("all_endpoint_recharts_closed") is True
        and certificate.get("all_pair_incidences_closed") is True
        and certificate.get("all_face_owners_closed") is True
        and certificate.get("all_corner_owners_closed") is True
        and certificate.get("original_reflection_binding_complete") is True
        and certificate.get("formal_credit") == 0,
        "exit complete lower-strata ownership closure",
    )
    closure = certificate.get("lower_strata_closure")
    expected_closure = expected_lower_strata_closure(task)
    need(type(closure) is dict and set(closure) == set(expected_closure),
         "exit exact lower-strata closure classes")
    for category, expected in expected_closure.items():
        observed = closure[category]
        need(
            type(observed) is dict
            and {key: observed.get(key) for key in expected} == expected
            and set(observed) == {*expected, "closure_evidence_sha256"}
            and type(observed.get("closure_evidence_sha256")) is str
            and HEX64.fullmatch(observed["closure_evidence_sha256"])
            is not None,
            "exit exact dependency-bound closure: " + category,
        )
    sides = certificate.get("physical_sides")
    reflection = task["representative_reflected_binding"]
    expected_sides = [{
        "side": "REPRESENTATIVE",
        "source_cell_id": reflection["representative_cell_id"],
        "source_box_sha256": reflection["representative_box_sha256"],
    }, {
        "side": "REFLECTED",
        "source_cell_id": reflection["reflected_cell_id"],
        "source_box_sha256": reflection["reflected_box_sha256"],
    }]
    need(
        type(sides) is list and len(sides) == 2
        and all({key: row.get(key) for key in expected} == expected
                for row, expected in zip(sides, expected_sides, strict=True))
        and all(set(row) == {
                    "side", "source_cell_id", "source_box_sha256", "complete",
                    "occurrence_binding_sha256",
                }
                and row.get("complete") is True
                and type(row.get("occurrence_binding_sha256")) is str
                and HEX64.fullmatch(row["occurrence_binding_sha256"])
                is not None for row in sides),
        "exit exact representative/reflected two-side certificate",
    )
    handoff = certificate.get("collision3_handoff")
    if exit_class == "COLLISION3_READY":
        need(type(handoff) is dict, "collision3 handoff object")
        handoff_body = dict(handoff)
        handoff_hash = handoff_body.pop("handoff_object_sha256", None)
        fields = {
            "exact_owner", "discriminant", "root_order", "official_word",
            "chart", "wall", "homogeneity", "incidence", "core",
            "terminal_margin",
        }
        need(
            type(handoff_hash) is str and handoff_hash == digest(handoff_body)
            and set(handoff_body) == fields
            and all(type(handoff_body[field]) is str and handoff_body[field]
                    for field in fields),
            "collision3 exact handoff fields and self hash",
        )
    else:
        need(handoff is None, "noncollision exit has no collision3 handoff")


def advance_task_state(
    state: dict[str, Any], task: dict[str, Any],
    decisions: list[dict[str, Any]], event_budget: int,
    oracle_adapter_source_sha256: str | None = None,
) -> dict[str, Any]:
    need(type(event_budget) is int and event_budget >= 0,
         "nonnegative event budget")
    value = copy.deepcopy(state)
    validate_task_state(value, task)
    processed = 0
    for decision in decisions:
        if processed >= event_budget:
            break
        relative = decision.get("relative_path")
        matches = [
            index for index, row in enumerate(value["frontier"])
            if row["relative_path"] == relative
        ]
        need(len(matches) == 1, "decision binds one pending frontier leaf")
        index = matches[0]
        leaf = value["frontier"].pop(index)
        action = decision.get("action")
        if action == "RESUMABLE_PENDING":
            reason = decision.get("reason")
            need(reason in {"EVENT_BUDGET", "NUMERIC_PRECISION_BUDGET",
                            "OWNER_DEPENDENCY_PENDING", "ORACLE_NOT_AVAILABLE"},
                 "pending reason enum")
            leaf["reason"] = reason
            value["frontier"].insert(index, leaf)
        elif action == "SPLIT":
            oracle_gate = task.get("oracle_gate")
            need(
                type(oracle_gate) is dict
                and oracle_gate.get("status") == "VERIFIED_ORACLE_AVAILABLE"
                and oracle_gate.get("split_transitions_enabled") is True
                and type(oracle_gate.get("adapter_source_sha256")) is str
                and HEX64.fullmatch(oracle_gate["adapter_source_sha256"])
                is not None
                and oracle_adapter_source_sha256
                == oracle_gate["adapter_source_sha256"],
                "split blocked without task-bound verified numerical oracle",
            )
            need(
                decision.get("split_axis") in {"t", "p"}
                and type(decision.get("split_coordinate")) is str
                and RATIONAL.fullmatch(decision["split_coordinate"]) is not None
                and type(decision.get("split_certificate_sha256")) is str
                and HEX64.fullmatch(decision["split_certificate_sha256"])
                is not None,
                "adaptive exact split evidence shape",
            )
            split_body = {
                "relative_path": relative,
                "absolute_path": leaf["absolute_path"],
                "split_axis": decision["split_axis"],
                "split_coordinate": decision["split_coordinate"],
                "split_certificate_sha256": decision[
                    "split_certificate_sha256"
                ],
                "oracle_adapter_source_sha256": oracle_adapter_source_sha256,
            }
            value["split_events"].append({
                **split_body,
                "split_event_object_sha256": digest(split_body),
            })
            fraction = parse_q(leaf["relative_fraction"], "split parent fraction") / 2
            children = []
            for bit in ("0", "1"):
                child_relative = relative + bit
                children.append({
                    "relative_path": child_relative,
                    "absolute_path": task["descendant_path"] + child_relative,
                    "relative_fraction": qstr(fraction),
                    "state": "RESUMABLE_PENDING_ZERO_CREDIT",
                    "reason": "ADAPTIVE_CHILD_UNROUTED",
                })
            value["frontier"][index:index] = children
        elif action == "EXIT":
            oracle_gate = task.get("oracle_gate")
            need(
                type(oracle_gate) is dict
                and oracle_gate.get("status") == "VERIFIED_ORACLE_AVAILABLE"
                and oracle_gate.get("exit_transitions_enabled") is True
                and type(oracle_gate.get("adapter_source_sha256")) is str
                and HEX64.fullmatch(oracle_gate["adapter_source_sha256"])
                is not None
                and oracle_adapter_source_sha256
                == oracle_gate["adapter_source_sha256"],
                "exit blocked without task-bound verified numerical oracle",
            )
            exit_class = decision.get("exit_class")
            certificate = decision.get("certificate")
            need(type(certificate) is dict, "exit certificate object")
            validate_exit_certificate(certificate, task, leaf, exit_class)
            value["exits"].append({
                "relative_path": leaf["relative_path"],
                "absolute_path": leaf["absolute_path"],
                "relative_fraction": leaf["relative_fraction"],
                "state": "D02_A_EXIT_ZERO_CREDIT",
                "exit_class": exit_class,
                "certificate_object_sha256": certificate[
                    "certificate_object_sha256"
                ],
                "certificate": certificate,
            })
        else:
            raise Rejected("adaptive decision action enum")
        processed += 1
    if processed >= event_budget and value["frontier"]:
        for leaf in value["frontier"]:
            leaf["reason"] = "EVENT_BUDGET"
    value["frontier"].sort(key=lambda row: row["relative_path"])
    value["exits"].sort(key=lambda row: row["relative_path"])
    value["event_count"] += processed
    value["deepest_additional_depth"] = max(
        [len(row["relative_path"])
         for row in [*value["frontier"], *value["exits"]]],
        default=0,
    )
    value["state"] = (
        "D02_A_SOURCE_CLOSED_ZERO_CREDIT"
        if not value["frontier"] else "RESUMABLE_PENDING_ZERO_CREDIT"
    )
    validate_task_state(value, task)
    return value


def make_checkpoint(
    plan: dict[str, Any], shard: dict[str, Any],
    task_states: list[dict[str, Any]] | None = None,
    generation: int = 0, previous: str | None = None,
) -> dict[str, Any]:
    tasks = shard["_tasks"]
    plan_body = dict(plan)
    plan_hash = plan_body.pop("plan_object_sha256", None)
    need(type(plan_hash) is str and plan_hash == digest(plan_body),
         "checkpoint plan self hash")
    need(public_shard(shard) in plan["sharding"]["shards"],
         "checkpoint shard belongs to plan")
    need(generation == 0 and previous is None,
         "genesis constructor cannot skip predecessor generations")
    initial_states = [initial_task_state(task) for task in tasks]
    if task_states is None:
        task_states = initial_states
    need(task_states == initial_states,
         "genesis checkpoint is exact all-pending initial task vector")
    lookup = {task["task_id"]: task for task in tasks}
    need(len(task_states) == len(tasks)
         and [row["task_id"] for row in task_states]
         == [row["task_id"] for row in tasks],
         "checkpoint exact ordered shard task inventory")
    for state in task_states:
        validate_task_state(state, lookup[state["task_id"]])
    completed = sum(
        row["state"] == "D02_A_SOURCE_CLOSED_ZERO_CREDIT"
        for row in task_states
    )
    body: dict[str, Any] = {
        "schema": CHECKPOINT_SCHEMA,
        "status": (
            "D02_A_SHARD_CLOSED_ZERO_CREDIT" if completed == len(tasks)
            else "RESUMABLE_PENDING_ZERO_CREDIT"
        ),
        "plan_object_sha256": plan["plan_object_sha256"],
        "shard_id": shard["shard_id"],
        "shard_index": shard["shard_index"],
        "generation": generation,
        "previous_checkpoint_object_sha256": previous,
        "task_count": len(tasks),
        "completed_task_count": completed,
        "pending_task_count": len(tasks) - completed,
        "ordered_task_binding_sequence_sha256": shard[
            "ordered_task_binding_sequence_sha256"
        ],
        "ordered_task_state_sequence_sha256": sequence_digest([
            digest(state) for state in task_states
        ]),
        "work_cursor": checkpoint_work_cursor(task_states),
        "task_states": task_states,
        "credit_lock": {
            "ambient_credit": 0, "terminal_credit": 0,
            "whole_parent_credit": 0, "D02_gate_credit": 0,
            "formal_credit": 0,
        },
        "authority_baseline": "INSTALLED_C42_ONLY__574_1150_575",
        "C43_conditional_credit": 0,
    }
    return {**body, "checkpoint_object_sha256": digest(body)}


def checkpoint_work_cursor(task_states: list[dict[str, Any]]) -> dict[str, Any]:
    pending = [
        index for index, state in enumerate(task_states)
        if state["state"] == "RESUMABLE_PENDING_ZERO_CREDIT"
    ]
    completed = [
        index for index, state in enumerate(task_states)
        if state["state"] == "D02_A_SOURCE_CLOSED_ZERO_CREDIT"
    ]
    return {
        "mode": "EXACT_ORDERED_TASK_STATE_VECTOR__NO_SCALAR_CURSOR",
        "first_pending_task_index": pending[0] if pending else None,
        "pending_task_indices_sha256": digest(pending),
        "completed_task_indices_sha256": digest(completed),
        "scalar_cursor_may_imply_prior_completion": False,
    }


def validate_task_state_successor(
    predecessor: dict[str, Any], successor: dict[str, Any],
    task: dict[str, Any],
) -> None:
    validate_task_state(predecessor, task)
    validate_task_state(successor, task)
    need(
        successor["event_count"] >= predecessor["event_count"]
        and successor["deepest_additional_depth"]
        >= predecessor["deepest_additional_depth"]
        and successor["split_events"][:len(predecessor["split_events"])]
        == predecessor["split_events"],
        "checkpoint successor monotone event/split history",
    )
    old_exits = {
        row["relative_path"]: row for row in predecessor["exits"]
    }
    new_exits = {row["relative_path"]: row for row in successor["exits"]}
    need(all(new_exits.get(path) == row for path, row in old_exits.items()),
         "checkpoint successor preserves every certified exit byte-for-byte")
    new_leaves = [*successor["frontier"], *successor["exits"]]
    old_leaves = [*predecessor["frontier"], *predecessor["exits"]]
    for new_leaf in new_leaves:
        owners = [
            old_leaf for old_leaf in old_leaves
            if new_leaf["relative_path"].startswith(old_leaf["relative_path"])
        ]
        need(len(owners) == 1,
             "successor leaf has exactly one predecessor-leaf owner")
    for old_frontier in predecessor["frontier"]:
        path = old_frontier["relative_path"]
        descendants = [
            row for row in new_leaves if row["relative_path"].startswith(path)
        ]
        need(len(descendants) > 0, "predecessor frontier cannot disappear")
        descendant_paths = [row["relative_path"] for row in descendants]
        prefix_free(descendant_paths, "successor refinement:" + path)
        total = sum((
            parse_q(row["relative_fraction"], "successor refinement fraction")
            for row in descendants
        ), Q(0))
        need(total == parse_q(
            old_frontier["relative_fraction"], "predecessor frontier fraction"
        ), "successor refinement preserves exact predecessor Kraft mass")


def _validate_checkpoint_object(
    checkpoint: dict[str, Any], plan: dict[str, Any], shard: dict[str, Any],
) -> None:
    body = dict(checkpoint)
    observed = body.pop("checkpoint_object_sha256", None)
    need(type(observed) is str and observed == digest(body),
         "checkpoint self hash")
    tasks = shard["_tasks"]
    states = checkpoint.get("task_states")
    need(
        checkpoint.get("schema") == CHECKPOINT_SCHEMA
        and checkpoint.get("plan_object_sha256") == plan["plan_object_sha256"]
        and checkpoint.get("shard_id") == shard["shard_id"]
        and checkpoint.get("shard_index") == shard["shard_index"]
        and checkpoint.get("ordered_task_binding_sequence_sha256")
        == shard["ordered_task_binding_sequence_sha256"]
        and type(states) is list
        and [row.get("task_id") for row in states]
        == [row["task_id"] for row in tasks]
        and checkpoint.get("authority_baseline")
        == "INSTALLED_C42_ONLY__574_1150_575"
        and checkpoint.get("C43_conditional_credit") == 0
        and checkpoint.get("credit_lock") == {
            "ambient_credit": 0, "terminal_credit": 0,
            "whole_parent_credit": 0, "D02_gate_credit": 0,
            "formal_credit": 0,
        },
        "checkpoint frozen plan/shard/authority bindings",
    )
    lookup = {task["task_id"]: task for task in tasks}
    for state in states:
        validate_task_state(state, lookup[state["task_id"]])
    completed = sum(
        row["state"] == "D02_A_SOURCE_CLOSED_ZERO_CREDIT" for row in states
    )
    pending = len(states) - completed
    expected_status = (
        "D02_A_SHARD_CLOSED_ZERO_CREDIT" if pending == 0
        else "RESUMABLE_PENDING_ZERO_CREDIT"
    )
    need(
        checkpoint.get("task_count") == len(tasks)
        and checkpoint.get("completed_task_count") == completed
        and checkpoint.get("pending_task_count") == pending
        and checkpoint.get("status") == expected_status,
        "checkpoint exact completion census",
    )
    need(
        checkpoint.get("ordered_task_state_sequence_sha256")
        == sequence_digest([digest(state) for state in states])
        and checkpoint.get("work_cursor") == checkpoint_work_cursor(states),
        "checkpoint exact task-state vector prevents scalar cursor skips",
    )
    generation = checkpoint.get("generation")
    previous = checkpoint.get("previous_checkpoint_object_sha256")
    need(
        type(generation) is int and generation >= 0
        and ((generation == 0 and previous is None)
             or (generation > 0 and type(previous) is str
                 and HEX64.fullmatch(previous) is not None)),
        "checkpoint immutable generation link shape",
    )


def validate_checkpoint(
    checkpoint: dict[str, Any], plan: dict[str, Any], shard: dict[str, Any],
    predecessor: dict[str, Any] | None = None,
) -> None:
    _validate_checkpoint_object(checkpoint, plan, shard)
    need(
        checkpoint["generation"] == 0
        and checkpoint["previous_checkpoint_object_sha256"] is None
        and predecessor is None,
        "C46 v1 checkpoint validator is genesis-only",
    )
    expected_states = [initial_task_state(task) for task in shard["_tasks"]]
    need(checkpoint["task_states"] == expected_states,
         "generation zero is exact all-pending initial vector")


def validate_checkpoint_chain(
    chain: list[dict[str, Any]], plan: dict[str, Any],
    shard: dict[str, Any],
) -> None:
    need(type(chain) is list and len(chain) == 1,
         "C46 v1 accepts only a one-object genesis chain")
    validate_checkpoint(chain[0], plan, shard)


def make_successor_checkpoint(
    predecessor_chain: list[dict[str, Any]], plan: dict[str, Any],
    shard: dict[str, Any], task_states: list[dict[str, Any]],
) -> dict[str, Any]:
    raise Rejected(
        "C46 v1 is genesis-only; every successor checkpoint is rejected"
    )


def _synthetic_task() -> dict[str, Any]:
    empty = digest([])
    zeros = "0" * 64
    task: dict[str, Any] = {
        "task_id": "c46-selftest-task",
        "task_binding_sha256": digest({"selftest": "task-binding"}),
        "primary_outer_id": "synthetic-primary",
        "ambient_cell_id": "synthetic-ambient",
        "pair_index": 17,
        "descendant_path": "101",
        "dependency_closure_sha256": digest({"selftest": "dependencies"}),
        "representative_reflected_binding": {
            "representative_cell_id": "synthetic-representative",
            "reflected_cell_id": "synthetic-reflected",
            "representative_box_sha256": digest({"box": "representative"}),
            "reflected_box_sha256": digest({"box": "reflected"}),
            "required_physical_sides": list(SIDE_ORDER),
        },
        "lower_strata_dependencies": {
            "normalized_surface_count": 0,
            "normalized_surface_ids_sha256": empty,
            "endpoint_rechart_count": 0,
            "endpoint_rechart_ids_sha256": empty,
            "endpoint_rechart_row_hash_sequence_sha256": zeros,
            "pair_incidence_count": 0,
            "pair_incidence_ids_sha256": empty,
            "pair_incidence_row_hash_sequence_sha256": zeros,
            "boundary_outer_id": "synthetic-boundary",
            "boundary_outer_row_sha256": digest({"row": "boundary"}),
            "face_count": 0,
            "face_ids_sha256": empty,
            "corner_count": 0,
            "corner_ids_sha256": empty,
            "ordered_C41_obligation_sequence_sha256": zeros,
        },
        "oracle_gate": {
            "status": "VERIFIED_ORACLE_AVAILABLE",
            "adapter_source_sha256": digest({
                "selftest": "synthetic-oracle-adapter"
            }),
            "split_transitions_enabled": True,
            "exit_transitions_enabled": True,
            "required_independent_implementations": 0,
        },
        "queue": {"state": "RESUMABLE_PENDING_ZERO_CREDIT"},
    }
    return task


def _synthetic_exit_certificate(
    task: dict[str, Any], leaf: dict[str, Any], exit_class: str,
) -> dict[str, Any]:
    closure: dict[str, Any] = {}
    for category, expected in expected_lower_strata_closure(task).items():
        closure[category] = {
            **expected,
            "closure_evidence_sha256": digest({
                "category": category,
                "relative_path": leaf["relative_path"],
            }),
        }
    reflection = task["representative_reflected_binding"]
    sides = [{
        "side": "REPRESENTATIVE",
        "source_cell_id": reflection["representative_cell_id"],
        "source_box_sha256": reflection["representative_box_sha256"],
        "complete": True,
        "occurrence_binding_sha256": digest({
            "side": "REPRESENTATIVE", "path": leaf["relative_path"],
        }),
    }, {
        "side": "REFLECTED",
        "source_cell_id": reflection["reflected_cell_id"],
        "source_box_sha256": reflection["reflected_box_sha256"],
        "complete": True,
        "occurrence_binding_sha256": digest({
            "side": "REFLECTED", "path": leaf["relative_path"],
        }),
    }]
    handoff = None
    if exit_class == "COLLISION3_READY":
        handoff_body = {
            "exact_owner": "synthetic-owner",
            "discriminant": "synthetic-discriminant",
            "root_order": "synthetic-root-order",
            "official_word": "synthetic-official-word",
            "chart": "synthetic-chart",
            "wall": "synthetic-wall",
            "homogeneity": "synthetic-homogeneity",
            "incidence": "synthetic-incidence",
            "core": "synthetic-core",
            "terminal_margin": "synthetic-terminal-margin",
        }
        handoff = {
            **handoff_body,
            "handoff_object_sha256": digest(handoff_body),
        }
    body: dict[str, Any] = {
        "schema": SCHEMA + ".exit-certificate",
        "exit_class": exit_class,
        "task_id": task["task_id"],
        "task_binding_sha256": task["task_binding_sha256"],
        "primary_outer_id": task["primary_outer_id"],
        "ambient_cell_id": task["ambient_cell_id"],
        "relative_path": leaf["relative_path"],
        "absolute_path": leaf["absolute_path"],
        "dependency_closure_sha256": task["dependency_closure_sha256"],
        "oracle_adapter_source_sha256": task[
            "oracle_gate"
        ]["adapter_source_sha256"],
        "lower_strata_closure": closure,
        "all_endpoint_recharts_closed": True,
        "all_pair_incidences_closed": True,
        "all_face_owners_closed": True,
        "all_corner_owners_closed": True,
        "original_reflection_binding_complete": True,
        "physical_sides": sides,
        "collision3_handoff": handoff,
        "formal_credit": 0,
    }
    return {**body, "certificate_object_sha256": digest(body)}


def _expect_rejected(function: Any, label: str) -> None:
    try:
        function()
    except Rejected:
        return
    raise AssertionError("expected fail-closed rejection: " + label)


def self_test() -> dict[str, Any]:
    tests: list[str] = []

    _expect_rejected(
        lambda: strict_json(b'{"x":1,"x":2}', "duplicate JSON"),
        "duplicate JSON member",
    )
    tests.append("duplicate JSON members rejected")
    _expect_rejected(
        lambda: strict_json(b'{"x":NaN}', "nonfinite JSON"),
        "nonfinite JSON number",
    )
    tests.append("nonfinite JSON numbers rejected")
    _expect_rejected(
        lambda: strict_json(b'{"x":1.25}', "noninteger JSON"),
        "noninteger JSON number",
    )
    tests.append("noninteger JSON numbers rejected")

    task = _synthetic_task()
    oracle = task["oracle_gate"]["adapter_source_sha256"]
    initial = initial_task_state(task)
    validate_task_state(initial, task)
    tests.append("initial checkpoint state is prefix-free Kraft one")

    blocked_task = copy.deepcopy(task)
    blocked_task["oracle_gate"] = {
        "status": "BLOCKED__NO_PINNED_NUMERICAL_ORACLE",
        "adapter_source_sha256": None,
        "split_transitions_enabled": False,
        "exit_transitions_enabled": False,
        "required_independent_implementations": 2,
    }
    _expect_rejected(lambda: advance_task_state(
        initial_task_state(blocked_task), blocked_task, [{
            "relative_path": "",
            "action": "SPLIT",
            "split_axis": "t",
            "split_coordinate": "0",
            "split_certificate_sha256": digest({"split": "untrusted"}),
        }], 1, oracle
    ), "production split without pinned oracle")
    tests.append("production split/exit disabled without pinned numerical oracle")

    budgeted = advance_task_state(initial, task, [{
        "relative_path": "",
        "action": "SPLIT",
        "split_axis": "t",
        "split_coordinate": "0",
        "split_certificate_sha256": digest({"split": "must-not-run"}),
    }], 0, oracle)
    need(budgeted["state"] == "RESUMABLE_PENDING_ZERO_CREDIT"
         and budgeted["event_count"] == 0
         and budgeted["frontier"][0]["reason"] == "EVENT_BUDGET",
         "zero budget cannot manufacture closure")
    tests.append("budget exhaustion remains resumable pending zero credit")

    split = advance_task_state(initial, task, [{
        "relative_path": "",
        "action": "SPLIT",
        "split_axis": "p",
        "split_coordinate": "1/2",
        "split_certificate_sha256": digest({"split": "root"}),
    }], 1, oracle)
    need([row["relative_path"] for row in split["frontier"]] == ["0", "1"]
         and split["relative_Kraft_sum"] == "1",
         "adaptive split exact children")
    tests.append("future split schema retains exact evidence and Kraft one")

    leaf0 = next(row for row in split["frontier"]
                 if row["relative_path"] == "0")
    collision = _synthetic_exit_certificate(
        task, leaf0, "COLLISION3_READY"
    )
    half = advance_task_state(split, task, [{
        "relative_path": "0",
        "action": "EXIT",
        "exit_class": "COLLISION3_READY",
        "certificate": collision,
    }], 1, oracle)
    need(half["state"] == "RESUMABLE_PENDING_ZERO_CREDIT"
         and len(half["frontier"]) == 1 and len(half["exits"]) == 1,
         "partial exit stays pending")
    tests.append("future collision3 schema requires all ten fields")

    incomplete = _synthetic_exit_certificate(
        task, half["frontier"][0], "CONNECTED_TO_KNOWN"
    )
    del incomplete["lower_strata_closure"]["face_owners"][
        "closure_evidence_sha256"
    ]
    incomplete_body = dict(incomplete)
    incomplete_body.pop("certificate_object_sha256")
    incomplete["certificate_object_sha256"] = digest(incomplete_body)
    _expect_rejected(lambda: advance_task_state(half, task, [{
        "relative_path": "1",
        "action": "EXIT",
        "exit_class": "CONNECTED_TO_KNOWN",
        "certificate": incomplete,
    }], 1, oracle), "incomplete face-owner certificate")
    tests.append(
        "future schema rejects incomplete face/corner/endpoint/incidence shape"
    )

    leaf1 = half["frontier"][0]
    connected = _synthetic_exit_certificate(
        task, leaf1, "CONNECTED_TO_KNOWN"
    )
    closed = advance_task_state(half, task, [{
        "relative_path": "1",
        "action": "EXIT",
        "exit_class": "CONNECTED_TO_KNOWN",
        "certificate": connected,
    }], 1, oracle)
    need(closed["state"] == "D02_A_SOURCE_CLOSED_ZERO_CREDIT"
         and not closed["frontier"], "all adaptive leaves closed")
    tests.append(
        "future in-memory schema shape closes only after every adaptive leaf exits"
    )

    deep = initial_task_state(task)
    for depth in range(17):
        relative = "0" * depth
        deep = advance_task_state(deep, task, [{
            "relative_path": relative,
            "action": "SPLIT",
            "split_axis": "t" if depth % 2 == 0 else "p",
            "split_coordinate": str(depth),
            "split_certificate_sha256": digest({"depth": depth}),
        }], 1, oracle)
    need(deep["deepest_additional_depth"] == 17
         and deep["state"] == "RESUMABLE_PENDING_ZERO_CREDIT",
         "no depth-three terminal cap")
    tests.append("future schema models depth beyond three without credit")

    shard_body: dict[str, Any] = {
        "schema": SHARD_SCHEMA,
        "shard_index": 0,
        "pair_count": 1,
        "pair_indices": [17],
        "task_count": 1,
        "estimated_work_units": 1,
        "priority_census": {"SELFTEST": 1},
        "primary_family_census": {"SELFTEST": 1},
        "ordered_task_binding_sequence_sha256": sequence_digest([
            task["task_binding_sha256"]
        ]),
        "first_task_id": task["task_id"],
        "last_task_id": task["task_id"],
        "pair_preserving": True,
        "credit": 0,
    }
    shard_body["shard_id"] = "c46-d02a-shard:" + digest(shard_body)
    shard = {**shard_body, "_tasks": [task]}
    plan_body = {
        "schema": PLAN_SCHEMA,
        "sharding": {"shards": [public_shard(shard)]},
    }
    plan = {**plan_body, "plan_object_sha256": digest(plan_body)}
    genesis = make_checkpoint(plan, shard)
    validate_checkpoint(genesis, plan, shard)
    validate_checkpoint_chain([genesis], plan, shard)
    need(
        genesis["generation"] == 0
        and genesis["completed_task_count"] == 0
        and genesis["pending_task_count"] == 1
        and genesis["task_states"] == [initial_task_state(task)],
        "genesis exact all-pending vector",
    )
    tests.append("only exact all-pending generation-zero template validates")

    _expect_rejected(lambda: make_successor_checkpoint(
        [genesis], plan, shard, [closed]
    ), "successor constructor")
    tests.append(
        "successor checkpoint constructor is unconditionally rejected"
    )

    forged = copy.deepcopy(genesis)
    forged.update({
        "status": "D02_A_SHARD_CLOSED_ZERO_CREDIT",
        "generation": 1,
        "previous_checkpoint_object_sha256": genesis[
            "checkpoint_object_sha256"
        ],
        "completed_task_count": 1,
        "pending_task_count": 0,
        "ordered_task_state_sequence_sha256": sequence_digest([
            digest(closed)
        ]),
        "work_cursor": checkpoint_work_cursor([closed]),
        "task_states": [closed],
    })
    forged_body = dict(forged)
    forged_body.pop("checkpoint_object_sha256")
    forged["checkpoint_object_sha256"] = digest(forged_body)
    _expect_rejected(
        lambda: validate_checkpoint(forged, plan, shard, genesis),
        "forged structurally complete non-genesis checkpoint",
    )
    tests.append("non-genesis closed checkpoint is rejected despite valid shape")
    _expect_rejected(
        lambda: validate_checkpoint_chain([genesis, forged], plan, shard),
        "multi-object checkpoint chain",
    )
    tests.append("checkpoint chain validator accepts genesis object only")

    tampered = copy.deepcopy(genesis)
    tampered["C43_conditional_credit"] = 1
    tampered_body = dict(tampered)
    tampered_body.pop("checkpoint_object_sha256")
    tampered["checkpoint_object_sha256"] = digest(tampered_body)
    _expect_rejected(
        lambda: validate_checkpoint(tampered, plan, shard),
        "conditional C43 credit",
    )
    tests.append("rejected C43 overlay cannot acquire checkpoint credit")

    body: dict[str, Any] = {
        "schema": SCHEMA + ".self-test",
        "status": "PASS",
        "test_count": len(tests),
        "tests": tests,
        "checkpoint_scope": "GENESIS_ONLY",
        "successor_checkpoint_supported": False,
        "future_schema_execution_verified": False,
        "future_schema_mathematical_fixed_depth_cap": None,
        "full_inventory_read": False,
        "global_terminal_snapshot_read": False,
        "runtime_writes_performed": False,
        "formal_credit": 0,
        "source_sha256": file_sha256(SELF, "C46 self-test source"),
    }
    return {**body, "self_test_object_sha256": digest(body)}


def emit(value: dict[str, Any], stream: Any = sys.stdout.buffer) -> None:
    stream.write(canonical(value) + b"\n")
    stream.flush()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--self-test", action="store_true")
    modes.add_argument("--plan", action="store_true")
    modes.add_argument("--checkpoint-template", action="store_true")
    parser.add_argument("--shards", type=int, default=64)
    parser.add_argument("--shard-index", type=int)
    arguments = parser.parse_args(argv)
    try:
        if arguments.self_test:
            need(arguments.shard_index is None,
                 "self-test does not select a shard")
            value = self_test()
        else:
            plan, _tasks, shards = build_read_only_plan(arguments.shards)
            if arguments.plan:
                need(arguments.shard_index is None,
                     "plan mode does not select one shard")
                value = plan
            else:
                need(type(arguments.shard_index) is int
                     and 0 <= arguments.shard_index < len(shards),
                     "checkpoint shard index in range")
                value = make_checkpoint(
                    plan, shards[arguments.shard_index]
                )
                validate_checkpoint(
                    value, plan, shards[arguments.shard_index]
                )
        emit(value)
        return 0
    except (Rejected, OSError, ValueError, KeyError, TypeError) as error:
        failure_body = {
            "schema": SCHEMA + ".fail-closed-error",
            "status": "REJECTED",
            "error_class": type(error).__name__,
            "reason": str(error),
            "runtime_writes_performed": False,
            "formal_credit": 0,
        }
        emit({**failure_body, "error_object_sha256": digest(failure_body)})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
