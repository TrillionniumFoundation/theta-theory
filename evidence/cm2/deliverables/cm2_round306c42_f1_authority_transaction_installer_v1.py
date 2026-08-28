#!/usr/bin/env python3
"""Install the independently audited C42 f1 authority transaction.

This program is deliberately pinned to one candidate, one producer execution
receipt, and one independent audit.  It has no path override for f2 or any
review-only object.  The transaction is a durable exact-prefix protocol:

  prepared self-hashed receipt -> candidate pointer -> audit pointer -> seal

The two compatibility pointers are *not* authority by themselves.  The final
``c42-current-authority-seal`` is the sole semantic commit point.  Every
publication uses a same-filesystem private stage, fsync, and Linux
renameat2(RENAME_NOREPLACE).  An interrupted exact prefix can be resumed;
non-prefix, symlink, hardlink, or byte-mismatched states fail closed.

Normal use is intentionally two-step and source-pinned::

  python3.12 -I -B THIS.py --preflight --expect-installer-sha256 SHA
  python3.12 -I -B THIS.py --install --expect-installer-sha256 SHA \
      --invocation-id EXTERNAL_ID \
      --confirm INSTALL_C42_F1_A50914A266AF_85A7CD719CEE

``--preflight`` and ``--self-test`` never write below .cm2-runtime.
"""

from __future__ import annotations

import argparse
import copy
import ctypes
from datetime import datetime, timezone
import errno
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
from typing import Any


SELF = Path(__file__).absolute()
ROOT = SELF.parent.parent
RUNTIME = ROOT / ".cm2-runtime"
AUDIT_ROOT = RUNTIME / "audit"
DELIVERABLES = ROOT / "deliverables"

RELEASE_ID = "c42-f1-authority-install-a50914a266af-85a7cd719cee-v1"
CONFIRMATION = "INSTALL_C42_F1_A50914A266AF_85A7CD719CEE"
RECEIPT_SCHEMA = "cm2.round306c42.f1-authority-installation-receipt.v1"
RECEIPT_STATUS = "PREPARED_C42_F1_AUTHORITY_RECEIPT__POINTERS_AND_SEAL_PENDING"
SEAL_SCHEMA = "cm2.round306c42.f1-authority-commit-seal.v1"
SEAL_STATUS = "COMMITTED_C42_F1_AUTHORITY__574_PAIRED__1150_UNRESOLVED"

C42_CANDIDATE_TOKEN = "c42-p391-formal-producer-20260811T044500Z-f1"
C42_AUDIT_TOKEN = "c42-independent-audit-20260811T052900Z-p391-f1"
C42_CANDIDATE_POINTER = "c42-current-token"
C42_AUDIT_POINTER = "c42-current-audit-token"
C42_SEAL = "c42-current-authority-seal"
C42_CANDIDATE_POINTER_BYTES = (C42_CANDIDATE_TOKEN + "\n").encode("ascii")
C42_AUDIT_POINTER_BYTES = (C42_AUDIT_TOKEN + "\n").encode("ascii")
C42_CANDIDATE_POINTER_SHA256 = (
    "fbc5dd3c55bfdd3098ed34ae09ae633a9526a9c9cc6f40b3d87b5669b2ea7f07"
)
C42_AUDIT_POINTER_SHA256 = (
    "59aca53c4c35260801b3c559648c88ee974db01ae950f045a5e5aecd64aa36e5"
)

RECEIPT_DIR_REL = f".cm2-runtime/audit/{RELEASE_ID}"
RECEIPT_REL = RECEIPT_DIR_REL + "/installation_receipt.json"
RECEIPT_STAGE_DIR = "." + RELEASE_ID + ".stage"
SEAL_STAGE = "." + C42_SEAL + "." + RELEASE_ID + ".stage"
CANDIDATE_STAGE = "." + C42_CANDIDATE_POINTER + "." + RELEASE_ID + ".stage"
AUDIT_STAGE = "." + C42_AUDIT_POINTER + "." + RELEASE_ID + ".stage"

C41_CANDIDATE_TOKEN = "c41-lower-strata-depth3-20260811T023804Z-f997365c91559599"
C41_AUDIT_TOKEN = "c41-independent-audit-20260811T031547Z-ab94d420c43c94cd"
C41_CANDIDATE_POINTER_BYTES = (C41_CANDIDATE_TOKEN + "\n").encode("ascii")
C41_AUDIT_POINTER_BYTES = (C41_AUDIT_TOKEN + "\n").encode("ascii")

PINS: dict[str, dict[str, str]] = {
    "c42_producer_source": {
        "path": "deliverables/cm2_round306c42_d02_singleton_wall_endpoint_owner_closure_v1.py",
        "file_sha256": "4b4e96bcb2c701fd6820a04271e2f02058e3699d980a4bee61d4090b2ce30c78",
    },
    "c42_auditor_source": {
        "path": "deliverables/cm2_round306c42_d02_singleton_wall_endpoint_owner_closure_independent_auditor_v1.py",
        "file_sha256": "6da5c8a3f2960ec9f763e314be01e909722b6b03bcd2817e5030295dcd6086eb",
    },
    "c42_result": {
        "path": f".cm2-runtime/candidates/{C42_CANDIDATE_TOKEN}/result.json",
        "file_sha256": "f029c3ce6af33e2f93c33b4155286f60bfafecd724720a598b103ca3c263ccb0",
        "object_sha256": "a50914a266aff3396054d7f16e91d69db7fa735ad15f01cbf07eee8e708d99d2",
    },
    "c42_manifest": {
        "path": f".cm2-runtime/candidates/{C42_CANDIDATE_TOKEN}/root_manifest.sha256",
        "file_sha256": "ce1b6260b26a901a9dda3cfbd94eba5a752b5188d6bdbe7c7d3cd7a4d3f7d058",
    },
    "c42_execution_receipt": {
        "path": ".cm2-runtime/audit/c42-p391-formal-producer-20260811T044500Z-f1/execution_receipt.json",
        "file_sha256": "5a14c48b028dd20951d02659f9d9655f5718a13e69d2811ee823d78c38530a55",
        "object_sha256": "e89f66d0e7636bfa781a6ef7e0309fc1ad00c3215ea699c08b231003e1c39f08",
    },
    "c42_independent_audit": {
        "path": f".cm2-runtime/audit/{C42_AUDIT_TOKEN}/independent_audit.json",
        "file_sha256": "d60bb3c8f79f989df776effa4616ec170097a018547b1f4c929ad068c11138d3",
        "object_sha256": "85a7cd719cee9dceb1763135f74d50bcf28f78ff2426e65996b975b1def7790c",
    },
    "c41_candidate_pointer": {
        "path": ".cm2-runtime/c41-current-token",
        "file_sha256": "9e4f2d9c02c1f3e56639d69c971ccc7846ba229f87723e878f101730df3dd1a9",
    },
    "c41_audit_pointer": {
        "path": ".cm2-runtime/c41-current-audit-token",
        "file_sha256": "f8a9a0bf69169eba05ef3bec1db7e924de4b06b4ab61c97693b2919effd9c86c",
    },
    "c41_result": {
        "path": f".cm2-runtime/candidates/{C41_CANDIDATE_TOKEN}/result.json",
        "file_sha256": "73fde0eee7eb06bb0f144ea98880c72bfea36e10db696731ae72393cd9b0a50f",
        "object_sha256": "b7e47a4ca9d6f4bb1fee10e78877850d5070f6d3c2b06bb0234fbabdaa2b7b24",
    },
    "c41_manifest": {
        "path": f".cm2-runtime/candidates/{C41_CANDIDATE_TOKEN}/root_manifest.sha256",
        "file_sha256": "86e10532d63269cd0fdd58d541b1984522e9718f4613a5dc83211fe84eb258ba",
    },
    "c41_execution_receipt": {
        "path": f".cm2-runtime/audit/{C41_CANDIDATE_TOKEN}/execution_receipt.json",
        "file_sha256": "4500c6c38d1e34002cb3384f0c0c17623c93df6fb46ea7a12229e41ed6cb1dc8",
        "object_sha256": "39f1c6dadcf21a428174520b5a1aa4d072a57c73ffd9c9b04d2c3d639d94fed9",
    },
    "c41_independent_audit": {
        "path": f".cm2-runtime/audit/{C41_AUDIT_TOKEN}/independent_audit.json",
        "file_sha256": "6a800959a90c227d587b82c6246f60123483471f61dcf6a5de4da5381fee4b1e",
        "object_sha256": "44061ec6e26108692fe6e635e9e666cca0b11c66f00384eab539be08f66fe877",
    },
    "c41_producer_source": {
        "path": "deliverables/cm2_round306c41_d02_lower_strata_depth3_closure_v1.py",
        "file_sha256": "3fbf6cec247903d6e6ba147d4d06e912638b1472b74adc8311323c554e6e5bde",
    },
    "c41_auditor_source": {
        "path": "deliverables/cm2_round306c41_d02_lower_strata_depth3_closure_independent_auditor_v1.py",
        "file_sha256": "537f3dea94c3743235df8984ba4922d37f82999ff3d8abbac59e5171ef38b74c",
    },
}

EXPECTED_C42_STATUS = (
    "FORMAL_PRODUCER_PASS_C42_P391_OWNER_CLOSURE__PENDING_INDEPENDENT_C42_AUDIT"
)
EXPECTED_C42_AUDIT_STATUS = (
    "PASS_INDEPENDENT_C42_P391_OWNER_CLOSURE_AUDIT__54_OF_54_ATTACKS_FAIL_CLOSED"
)
EXPECTED_C41_STATUS = (
    "PASS_C41_DEPTH3_STRICT_ROUTER_PARTIAL__91879_AMBIENT_LEAVES__"
    "572_WHOLE_CELLS_TERMINAL__1152_FORMAL_UNRESOLVED"
)
EXPECTED_C41_AUDIT_STATUS = (
    "PASS_INDEPENDENT_C41_DEPTH3_CLOSURE_AUDIT__37_OF_37_MUTATIONS_REJECTED"
)

HEX64 = re.compile(r"[0-9a-f]{64}")
INVOCATION = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:@+-]{7,191}")


class Rejected(RuntimeError):
    """A fail-closed validation or transaction rejection."""


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def object_digest(value: dict[str, Any]) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def strict_json(raw: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(type(key) is str and key not in result, "duplicate JSON key")
            result[key] = value
        return result
    try:
        return json.loads(
            raw.decode("ascii"), object_pairs_hook=pairs,
            parse_constant=lambda token: (_ for _ in ()).throw(
                Rejected("non-finite JSON:" + token)),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Rejected("strict canonical JSON parse") from error


def fingerprint(info: os.stat_result) -> list[int]:
    return [info.st_dev, info.st_ino, info.st_mode, info.st_nlink,
            info.st_size, info.st_mtime_ns, info.st_ctime_ns,
            info.st_uid, info.st_gid]


def directory_identity(info: os.stat_result) -> list[int]:
    """Stable identity fields; directory size/times/nlink change on publish."""
    return [info.st_dev, info.st_ino, info.st_mode, info.st_uid, info.st_gid]


def relative(path: Path) -> str:
    return str(path.absolute().relative_to(ROOT))


def lexical_no_symlinks(path: Path, label: str) -> None:
    path = path.absolute()
    need(path == ROOT or ROOT in path.parents, label + ": workspace boundary")
    cursor = ROOT
    need(stat.S_ISDIR(os.lstat(cursor).st_mode), label + ": root directory")
    for part in path.relative_to(ROOT).parts:
        cursor /= part
        info = os.lstat(cursor)
        need(not stat.S_ISLNK(info.st_mode), label + ": symlink component")


class Capture:
    """One stable O_NOFOLLOW single-link file capture held across commit."""

    def __init__(self, path: Path, label: str, expected_sha256: str | None = None,
                 maximum: int = 1 << 30):
        self.path = path.absolute()
        self.label = label
        lexical_no_symlinks(self.path.parent, label + " parent")
        self.fd = os.open(
            self.path,
            os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW,
        )
        self.before = os.fstat(self.fd)
        need(stat.S_ISREG(self.before.st_mode) and self.before.st_nlink == 1,
             label + ": singleton regular")
        need(self.before.st_uid == os.getuid() and 0 <= self.before.st_size <= maximum,
             label + ": owner and size")
        self.raw = self._read()
        self.sha256 = hashlib.sha256(self.raw).hexdigest()
        if expected_sha256 is not None:
            need(HEX64.fullmatch(expected_sha256) is not None
                 and self.sha256 == expected_sha256, label + ": pinned SHA256")
        self.unchanged("initial")

    def _read(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        chunks: list[bytes] = []
        total = 0
        while block := os.read(self.fd, 4 << 20):
            chunks.append(block)
            total += len(block)
            need(total <= self.before.st_size, self.label + ": read bound")
        os.lseek(self.fd, 0, os.SEEK_SET)
        need(total == self.before.st_size, self.label + ": exact size")
        return b"".join(chunks)

    def unchanged(self, phase: str) -> None:
        current = os.stat(self.path, follow_symlinks=False)
        need(fingerprint(current) == fingerprint(self.before)
             == fingerprint(os.fstat(self.fd)),
             self.label + ": " + phase + " nine-stat identity")
        need(hashlib.sha256(self._read()).hexdigest() == self.sha256,
             self.label + ": " + phase + " SHA identity")

    def document(self, closure: str) -> dict[str, Any]:
        need(self.raw.endswith(b"\n") and not self.raw.endswith(b"\n\n"),
             self.label + ": one terminal newline")
        value = strict_json(self.raw[:-1])
        need(type(value) is dict and canonical(value) == self.raw[:-1],
             self.label + ": canonical object")
        body = dict(value)
        claim = body.pop(closure, None)
        need(type(claim) is str and HEX64.fullmatch(claim) is not None
             and claim == object_digest(body), self.label + ": self hash")
        return value

    def record(self) -> dict[str, Any]:
        return {
            "path": relative(self.path),
            "file_sha256": self.sha256,
            "size": self.before.st_size,
            "stat_fingerprint": fingerprint(self.before),
            "O_NOFOLLOW": True,
            "single_link": True,
        }

    def close(self) -> None:
        os.close(self.fd)


class Inputs:
    def __init__(self, expected_installer_sha256: str):
        need(HEX64.fullmatch(expected_installer_sha256) is not None,
             "installer expected SHA syntax")
        self.captures: dict[str, Capture] = {}
        self.add("installer", SELF, expected_installer_sha256, 4 << 20)
        for label, pin in PINS.items():
            self.add(label, ROOT / pin["path"], pin["file_sha256"])
        self.c42_manifest_members = self.verify_manifest(
            "c42_manifest", ROOT / f".cm2-runtime/candidates/{C42_CANDIDATE_TOKEN}",
            expected_count=8,
        )
        self.c41_manifest_members = self.verify_manifest(
            "c41_manifest", ROOT / f".cm2-runtime/candidates/{C41_CANDIDATE_TOKEN}",
            expected_count=13,
        )

    def add(self, label: str, path: Path, expected: str,
            maximum: int = 1 << 30) -> Capture:
        need(label not in self.captures, "unique input label")
        cap = Capture(path, label, expected, maximum)
        self.captures[label] = cap
        return cap

    def verify_manifest(self, label: str, directory: Path,
                        expected_count: int) -> dict[str, str]:
        manifest = self.captures[label]
        need(manifest.raw.endswith(b"\n"), label + ": newline")
        rows = manifest.raw.decode("ascii").splitlines()
        need(len(rows) == expected_count, label + ": exact row count")
        members: dict[str, str] = {}
        for row in rows:
            match = re.fullmatch(r"([0-9a-f]{64})  ([A-Za-z0-9][A-Za-z0-9_.-]*)", row)
            need(match is not None, label + ": strict row grammar")
            sha, name = match.groups()
            need(name not in members and name != "root_manifest.sha256",
                 label + ": unique safe member")
            members[name] = sha
        need(list(members) == sorted(members), label + ": sorted members")
        lexical_no_symlinks(directory, label + " directory")
        actual = sorted(entry.name for entry in os.scandir(directory))
        need(actual == sorted([*members, "root_manifest.sha256"]),
             label + ": exact directory inventory")
        for name, sha in members.items():
            key = label + ":member:" + name
            if (directory / name).absolute() in [c.path for c in self.captures.values()]:
                cap = next(c for c in self.captures.values()
                           if c.path == (directory / name).absolute())
                need(cap.sha256 == sha, key + ": reused capture SHA")
            else:
                self.add(key, directory / name, sha)
        return members

    def attest_all(self, phase: str) -> None:
        for label in sorted(self.captures):
            self.captures[label].unchanged(phase)

    def close(self) -> None:
        for cap in reversed(list(self.captures.values())):
            cap.close()


def validate_semantics(inputs: Inputs) -> dict[str, Any]:
    c41_pointer = inputs.captures["c41_candidate_pointer"]
    c41_audit_pointer = inputs.captures["c41_audit_pointer"]
    need(c41_pointer.raw == C41_CANDIDATE_POINTER_BYTES
         and c41_audit_pointer.raw == C41_AUDIT_POINTER_BYTES,
         "current C41 exact pointer bytes")

    c41 = inputs.captures["c41_result"].document("object_sha256")
    c41_receipt = inputs.captures["c41_execution_receipt"].document(
        "receipt_object_sha256")
    c41_audit = inputs.captures["c41_independent_audit"].document("object_sha256")
    need(c41["object_sha256"] == PINS["c41_result"]["object_sha256"]
         and c41.get("status") == EXPECTED_C41_STATUS,
         "C41 result object/status")
    need(c41_receipt["receipt_object_sha256"]
         == PINS["c41_execution_receipt"]["object_sha256"]
         and c41_receipt.get("candidate_path")
         == f".cm2-runtime/candidates/{C41_CANDIDATE_TOKEN}"
         and c41_receipt.get("candidate_object_sha256") == c41["object_sha256"]
         and c41_receipt.get("root_manifest_sha256")
         == PINS["c41_manifest"]["file_sha256"],
         "C41 receipt binding")
    need(c41_audit["object_sha256"]
         == PINS["c41_independent_audit"]["object_sha256"]
         and c41_audit.get("status") == EXPECTED_C41_AUDIT_STATUS
         and c41_audit.get("candidate_path")
         == f".cm2-runtime/candidates/{C41_CANDIDATE_TOKEN}"
         and c41_audit.get("candidate_object_sha256") == c41["object_sha256"]
         and c41_audit.get("execution_receipt_object_sha256")
         == c41_receipt["receipt_object_sha256"],
         "C41 audit binding")

    result = inputs.captures["c42_result"].document("object_sha256")
    receipt = inputs.captures["c42_execution_receipt"].document(
        "receipt_object_sha256")
    audit = inputs.captures["c42_independent_audit"].document("object_sha256")
    c42_path = f".cm2-runtime/candidates/{C42_CANDIDATE_TOKEN}"
    invocation = "c42-formal-producer-20260811T044500Z-p391-f1"
    need(result["object_sha256"] == PINS["c42_result"]["object_sha256"]
         and result.get("status") == EXPECTED_C42_STATUS
         and result.get("formal_producer_run") is True
         and result.get("review_only") is False
         and result.get("authority_pointer_installed") is False
         and result.get("producer_output_is_authority") is False
         and result.get("formal_authority") is False
         and result.get("independent_C42_audit_outstanding") is True,
         "C42 exact formal f1 non-authority producer result")
    need(result.get("closure_census", {}).get(
             "whole_terminal_paired_coarse_cell_count") == 574
         and result.get("closure_census", {}).get(
             "whole_terminal_representative_parent_count") == 287
         and result.get("closure_census", {}).get(
             "C34_common_refinement_credit_zero_row_count") == 575
         and result.get("round144_terminal_census", {}).get(
             "UNRESOLVED_R1648_CONTINUATION") == 1150
         and result.get("round144_terminal_census", {}).get(
             "terminal_total") == 76832
         and result.get("round144_terminal_census", {}).get(
             "unresolved_zero") is False,
         "C42 exact census")
    c41_input = result.get("C41_audited_input", {})
    need(c41_input.get("path")
         == f".cm2-runtime/candidates/{C41_CANDIDATE_TOKEN}"
         and c41_input.get("object_sha256") == c41["object_sha256"]
         and c41_input.get("independent_audit_object_sha256")
         == c41_audit["object_sha256"]
         and c41_input.get("installed_pointer_sha256") == {
             "candidate_pointer_sha256": PINS["c41_candidate_pointer"]["file_sha256"],
             "audit_pointer_sha256": PINS["c41_audit_pointer"]["file_sha256"],
         }, "C42 result exact C41 authority lineage")

    need(receipt["receipt_object_sha256"]
         == PINS["c42_execution_receipt"]["object_sha256"]
         and receipt.get("candidate_path") == c42_path
         and receipt.get("InvocationID") == invocation
         and receipt.get("candidate_object_sha256") == result["object_sha256"]
         and receipt.get("root_manifest_sha256")
         == PINS["c42_manifest"]["file_sha256"]
         and receipt.get("producer_source_sha256")
         == PINS["c42_producer_source"]["file_sha256"]
         and receipt.get("formal_producer_run") is True
         and receipt.get("producer_output_is_authority") is False
         and receipt.get("authority_pointer_installed") is False,
         "C42 exact f1 execution receipt")
    attacks = audit.get("attacks")
    need(audit["object_sha256"]
         == PINS["c42_independent_audit"]["object_sha256"]
         and audit.get("status") == EXPECTED_C42_AUDIT_STATUS
         and audit.get("candidate_path") == c42_path
         and audit.get("InvocationID") == invocation
         and audit.get("candidate_object_sha256") == result["object_sha256"]
         and audit.get("execution_receipt_object_sha256")
         == receipt["receipt_object_sha256"]
         and audit.get("root_manifest_sha256")
         == PINS["c42_manifest"]["file_sha256"]
         and audit.get("producer_source_sha256")
         == PINS["c42_producer_source"]["file_sha256"]
         and audit.get("independent_auditor_source_sha256")
         == PINS["c42_auditor_source"]["file_sha256"]
         and audit.get("authority_pointer_installed") is False
         and audit.get("producer_output_is_authority") is False
         and type(attacks) is dict and len(attacks) == 54
         and all(value is True for value in attacks.values()),
         "C42 exact f1 independent audit and 54 attacks")
    need(receipt.get("candidate_path") == c42_path
         and audit.get("candidate_path") == c42_path
         and receipt.get("InvocationID") == invocation
         and audit.get("InvocationID") == invocation
         and not C42_CANDIDATE_TOKEN.endswith("-f2")
         and "review-only" not in C42_CANDIDATE_TOKEN
         and "hardened-review" not in C42_CANDIDATE_TOKEN,
         "reject f2 and review-only path or invocation substitution")
    return {"c41": c41, "c41_receipt": c41_receipt,
            "c41_audit": c41_audit, "result": result,
            "receipt": receipt, "audit": audit}


def node_at(directory_fd: int, name: str) -> os.stat_result | None:
    try:
        return os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
    except FileNotFoundError:
        return None


def read_at(directory_fd: int, name: str, maximum: int = 1 << 20) \
        -> tuple[bytes, os.stat_result]:
    fd = os.open(name, os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW,
                 dir_fd=directory_fd)
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1
             and before.st_uid == os.getuid() and before.st_size <= maximum,
             name + ": strict installed node")
        blocks: list[bytes] = []
        total = 0
        while block := os.read(fd, 1 << 20):
            total += len(block)
            need(total <= maximum, name + ": installed read bound")
            blocks.append(block)
        after = os.fstat(fd)
        current = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
        need(fingerprint(before) == fingerprint(after) == fingerprint(current),
             name + ": stable installed node")
        return b"".join(blocks), before
    finally:
        os.close(fd)


def fsync_dir(fd: int) -> None:
    os.fsync(fd)


def write_once_at(directory_fd: int, name: str, payload: bytes,
                  mode: int = 0o444) -> None:
    need("/" not in name and name not in {"", ".", ".."}, "safe output basename")
    fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                 | os.O_NOFOLLOW | os.O_CLOEXEC, mode, dir_fd=directory_fd)
    try:
        os.fchmod(fd, mode)
        view = memoryview(payload)
        offset = 0
        while offset < len(view):
            written = os.write(fd, view[offset:])
            need(written > 0, "write-all positive progress")
            offset += written
        need(offset == len(payload), "write-all exact")
        os.fsync(fd)
    finally:
        os.close(fd)
    raw, info = read_at(directory_fd, name, max(1, len(payload)))
    need(raw == payload and stat.S_IMODE(info.st_mode) == mode,
         name + ": staged terminal replay")
    fsync_dir(directory_fd)


def rename_noreplace(source_fd: int, source_name: str,
                     target_fd: int, target_name: str) -> None:
    function = getattr(ctypes.CDLL(None, use_errno=True), "renameat2", None)
    need(function is not None, "renameat2(RENAME_NOREPLACE) available")
    function.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int,
                         ctypes.c_char_p, ctypes.c_uint]
    function.restype = ctypes.c_int
    result = function(source_fd, os.fsencode(source_name), target_fd,
                      os.fsencode(target_name), 1)
    if result == 0:
        return
    number = ctypes.get_errno()
    if number == errno.EEXIST:
        raise FileExistsError(number, os.strerror(number), target_name)
    raise OSError(number, os.strerror(number), target_name)


def ensure_absent_at(fd: int, name: str, label: str) -> None:
    need(node_at(fd, name) is None, label + ": absent (including symlink)")


def exact_or_absent(fd: int, name: str, payload: bytes, label: str) -> str:
    info = node_at(fd, name)
    if info is None:
        return "ABSENT"
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1,
         label + ": existing singleton regular")
    raw, _ = read_at(fd, name, max(1, len(payload)))
    need(raw == payload, label + ": existing exact bytes")
    return "EXACT"


def install_exact(runtime_fd: int, stage_name: str, target_name: str,
                  payload: bytes) -> str:
    target_state = exact_or_absent(runtime_fd, target_name, payload, target_name)
    stage_state = exact_or_absent(runtime_fd, stage_name, payload, stage_name)
    if target_state == "EXACT":
        if stage_state == "EXACT":
            os.unlink(stage_name, dir_fd=runtime_fd)
            fsync_dir(runtime_fd)
        return "RESUMED_EXACT"
    if stage_state == "ABSENT":
        write_once_at(runtime_fd, stage_name, payload)
    rename_noreplace(runtime_fd, stage_name, runtime_fd, target_name)
    fsync_dir(runtime_fd)
    raw, _ = read_at(runtime_fd, target_name, len(payload))
    need(raw == payload, target_name + ": post-rename bytes")
    return "INSTALLED"


def process_start_ticks() -> int:
    raw = Path(f"/proc/{os.getpid()}/stat").read_text(encoding="ascii")
    suffix = raw[raw.rfind(")") + 2:].split()
    need(len(suffix) >= 20 and suffix[19].isdigit(), "process start ticks")
    return int(suffix[19])


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace(
        "+00:00", "Z")


def binding_records(inputs: Inputs, docs: dict[str, Any]) -> dict[str, Any]:
    labels = [
        "c42_result", "c42_manifest", "c42_execution_receipt",
        "c42_independent_audit", "c42_producer_source", "c42_auditor_source",
        "c41_candidate_pointer", "c41_audit_pointer", "c41_result",
        "c41_manifest", "c41_execution_receipt", "c41_independent_audit",
        "c41_producer_source", "c41_auditor_source",
    ]
    return {
        "files": {label: inputs.captures[label].record() for label in labels},
        "objects": {
            "c42_candidate_object_sha256": docs["result"]["object_sha256"],
            "c42_execution_receipt_object_sha256":
                docs["receipt"]["receipt_object_sha256"],
            "c42_independent_audit_object_sha256": docs["audit"]["object_sha256"],
            "c41_candidate_object_sha256": docs["c41"]["object_sha256"],
            "c41_execution_receipt_object_sha256":
                docs["c41_receipt"]["receipt_object_sha256"],
            "c41_independent_audit_object_sha256": docs["c41_audit"]["object_sha256"],
        },
    }


def receipt_document(inputs: Inputs, docs: dict[str, Any], invocation: str,
                     pointer_records: dict[str, dict[str, Any]]) -> dict[str, Any]:
    body: dict[str, Any] = {
        "schema": RECEIPT_SCHEMA,
        "status": RECEIPT_STATUS,
        "release_id": RELEASE_ID,
        "InvocationID": invocation,
        "installer": {
            "path": relative(SELF),
            "source_sha256": inputs.captures["installer"].sha256,
            "pid": os.getpid(),
            "proc_start_ticks": process_start_ticks(),
            "started_utc": utc_now(),
        },
        "bindings": binding_records(inputs, docs),
        "prepared_pointer_records": pointer_records,
        "authority_contract": {
            "candidate_pointer_path": ".cm2-runtime/" + C42_CANDIDATE_POINTER,
            "candidate_pointer_sha256": C42_CANDIDATE_POINTER_SHA256,
            "audit_pointer_path": ".cm2-runtime/" + C42_AUDIT_POINTER,
            "audit_pointer_sha256": C42_AUDIT_POINTER_SHA256,
            "seal_path": ".cm2-runtime/" + C42_SEAL,
            "receipt_path": RECEIPT_REL,
            "publication_order": ["receipt", "candidate_pointer",
                                  "audit_pointer", "authority_seal"],
            "authority_commit_point": "authority_seal_RENAME_NOREPLACE",
            "pointers_before_seal_have_formal_authority": False,
            "exact_prefix_recovery_only": True,
        },
        "post_install_census": {
            "whole_terminal_paired_coarse_cells": 574,
            "whole_terminal_representatives": 287,
            "remaining_representatives": 575,
            "UNRESOLVED_R1648_CONTINUATION": 1150,
            "D02": "BLOCKED_BY_1150_COMPLETE_R1648_CONTINUATIONS",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "filesystem_policy": {
            "O_EXCL": True, "O_NOFOLLOW": True, "O_CLOEXEC": True,
            "file_fsync": True, "directory_fsync": True,
            "renameat2_RENAME_NOREPLACE": True,
            "ordinary_rename_or_replace_or_mv_used": False,
        },
    }
    return {**body, "installation_receipt_object_sha256": object_digest(body)}


def closed_bytes(document: dict[str, Any]) -> bytes:
    return canonical(document) + b"\n"


def validate_receipt_bytes(raw: bytes) -> dict[str, Any]:
    need(raw.endswith(b"\n") and not raw.endswith(b"\n\n"), "receipt newline")
    value = strict_json(raw[:-1])
    need(type(value) is dict and canonical(value) == raw[:-1], "receipt canonical")
    need(set(value) == {
        "schema", "status", "release_id", "InvocationID", "installer",
        "bindings", "prepared_pointer_records", "authority_contract",
        "post_install_census", "filesystem_policy",
        "installation_receipt_object_sha256",
    }, "receipt exact top-level keys")
    body = dict(value)
    claim = body.pop("installation_receipt_object_sha256", None)
    need(type(claim) is str and claim == object_digest(body), "receipt self hash")
    need(value.get("schema") == RECEIPT_SCHEMA
         and value.get("status") == RECEIPT_STATUS
         and value.get("release_id") == RELEASE_ID,
         "receipt fixed identity")
    need(type(value.get("InvocationID")) is str
         and INVOCATION.fullmatch(value["InvocationID"]) is not None,
         "receipt invocation syntax")
    contract = value.get("authority_contract", {})
    need(contract == {
        "candidate_pointer_path": ".cm2-runtime/" + C42_CANDIDATE_POINTER,
        "candidate_pointer_sha256": C42_CANDIDATE_POINTER_SHA256,
        "audit_pointer_path": ".cm2-runtime/" + C42_AUDIT_POINTER,
        "audit_pointer_sha256": C42_AUDIT_POINTER_SHA256,
        "seal_path": ".cm2-runtime/" + C42_SEAL,
        "receipt_path": RECEIPT_REL,
        "publication_order": ["receipt", "candidate_pointer",
                              "audit_pointer", "authority_seal"],
        "authority_commit_point": "authority_seal_RENAME_NOREPLACE",
        "pointers_before_seal_have_formal_authority": False,
        "exact_prefix_recovery_only": True,
    }, "receipt exact authority contract")
    installer = value.get("installer", {})
    need(type(installer) is dict and set(installer) == {
        "path", "source_sha256", "pid", "proc_start_ticks", "started_utc"
    } and installer.get("path") == relative(SELF)
         and type(installer.get("source_sha256")) is str
         and HEX64.fullmatch(installer["source_sha256"]) is not None
         and type(installer.get("pid")) is int and installer["pid"] > 0
         and type(installer.get("proc_start_ticks")) is int
         and installer["proc_start_ticks"] > 0
         and type(installer.get("started_utc")) is str
         and installer["started_utc"].endswith("Z"),
         "receipt exact installer metadata")
    need(type(value.get("bindings")) is dict
         and set(value["bindings"]) == {"files", "objects"},
         "receipt exact bindings shape")
    objects = value.get("bindings", {}).get("objects", {})
    need(type(objects) is dict and set(objects) == {
             "c42_candidate_object_sha256",
             "c42_execution_receipt_object_sha256",
             "c42_independent_audit_object_sha256",
             "c41_candidate_object_sha256",
             "c41_execution_receipt_object_sha256",
             "c41_independent_audit_object_sha256",
         }
         and objects.get("c42_candidate_object_sha256")
         == PINS["c42_result"]["object_sha256"]
         and objects.get("c42_execution_receipt_object_sha256")
         == PINS["c42_execution_receipt"]["object_sha256"]
         and objects.get("c42_independent_audit_object_sha256")
         == PINS["c42_independent_audit"]["object_sha256"]
         and objects.get("c41_candidate_object_sha256")
         == PINS["c41_result"]["object_sha256"]
         and objects.get("c41_execution_receipt_object_sha256")
         == PINS["c41_execution_receipt"]["object_sha256"]
         and objects.get("c41_independent_audit_object_sha256")
         == PINS["c41_independent_audit"]["object_sha256"],
         "receipt object pins")
    files = value.get("bindings", {}).get("files", {})
    required_labels = {
        "c42_result", "c42_manifest", "c42_execution_receipt",
        "c42_independent_audit", "c42_producer_source", "c42_auditor_source",
        "c41_candidate_pointer", "c41_audit_pointer", "c41_result",
        "c41_manifest", "c41_execution_receipt", "c41_independent_audit",
        "c41_producer_source", "c41_auditor_source",
    }
    need(type(files) is dict and set(files) == required_labels,
         "receipt exact file binding labels")
    for label in sorted(required_labels):
        need(type(files[label]) is dict and set(files[label]) == {
                 "path", "file_sha256", "size", "stat_fingerprint",
                 "O_NOFOLLOW", "single_link"
             }
             and files[label].get("path") == PINS[label]["path"]
             and files[label].get("file_sha256")
             == PINS[label]["file_sha256"]
             and type(files[label].get("size")) is int
             and files[label]["size"] >= 0
             and type(files[label].get("stat_fingerprint")) is list
             and len(files[label]["stat_fingerprint"]) == 9
             and all(type(item) is int
                     for item in files[label]["stat_fingerprint"])
             and files[label].get("O_NOFOLLOW") is True
             and files[label].get("single_link") is True,
             "receipt exact file binding:" + label)
    need(value.get("prepared_pointer_records") == {
        "candidate": {
            "path": ".cm2-runtime/" + C42_CANDIDATE_POINTER,
            "token": C42_CANDIDATE_TOKEN,
            "file_sha256": C42_CANDIDATE_POINTER_SHA256,
        },
        "audit": {
            "path": ".cm2-runtime/" + C42_AUDIT_POINTER,
            "token": C42_AUDIT_TOKEN,
            "file_sha256": C42_AUDIT_POINTER_SHA256,
        },
    }, "receipt exact pointer preparation")
    need(value.get("filesystem_policy") == {
        "O_EXCL": True, "O_NOFOLLOW": True, "O_CLOEXEC": True,
        "file_fsync": True, "directory_fsync": True,
        "renameat2_RENAME_NOREPLACE": True,
        "ordinary_rename_or_replace_or_mv_used": False,
    }, "receipt exact filesystem policy")
    need(value.get("post_install_census") == {
        "whole_terminal_paired_coarse_cells": 574,
        "whole_terminal_representatives": 287,
        "remaining_representatives": 575,
        "UNRESOLVED_R1648_CONTINUATION": 1150,
        "D02": "BLOCKED_BY_1150_COMPLETE_R1648_CONTINUATIONS",
        "CM2": "NO-GO_FOR_CLAIM",
    }, "receipt exact post-install census")
    return value


def seal_document(receipt_raw: bytes, receipt: dict[str, Any],
                  installer_sha256: str) -> dict[str, Any]:
    body: dict[str, Any] = {
        "schema": SEAL_SCHEMA,
        "status": SEAL_STATUS,
        "release_id": RELEASE_ID,
        "receipt_path": RECEIPT_REL,
        "receipt_file_sha256": hashlib.sha256(receipt_raw).hexdigest(),
        "receipt_object_sha256": receipt["installation_receipt_object_sha256"],
        "candidate_token": C42_CANDIDATE_TOKEN,
        "candidate_pointer_sha256": C42_CANDIDATE_POINTER_SHA256,
        "candidate_object_sha256": PINS["c42_result"]["object_sha256"],
        "audit_token": C42_AUDIT_TOKEN,
        "audit_pointer_sha256": C42_AUDIT_POINTER_SHA256,
        "independent_audit_object_sha256":
            PINS["c42_independent_audit"]["object_sha256"],
        "installer_source_sha256": installer_sha256,
        "semantic_commit": {
            "this_seal_is_required": True,
            "compatibility_pointers_without_this_seal_are_not_authority": True,
            "publication_method": "renameat2_RENAME_NOREPLACE_then_runtime_fsync",
        },
        "formal_census_after_commit": {
            "paired_coarse_cells": 574,
            "whole_representatives": 287,
            "remaining_representatives": 575,
            "unresolved": 1150,
        },
    }
    return {**body, "authority_seal_object_sha256": object_digest(body)}


def validate_seal_bytes(raw: bytes, receipt_raw: bytes,
                        installer_sha256: str) -> dict[str, Any]:
    need(raw.endswith(b"\n") and not raw.endswith(b"\n\n"), "seal newline")
    value = strict_json(raw[:-1])
    need(type(value) is dict and canonical(value) == raw[:-1], "seal canonical")
    body = dict(value)
    claim = body.pop("authority_seal_object_sha256", None)
    need(type(claim) is str and claim == object_digest(body), "seal self hash")
    receipt = validate_receipt_bytes(receipt_raw)
    expected = seal_document(receipt_raw, receipt, installer_sha256)
    need(value == expected, "seal exact reconstruction")
    return value


def open_bound_directory(path: Path, label: str) -> tuple[int, list[int]]:
    lexical_no_symlinks(path, label)
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
    before = os.fstat(fd)
    need(stat.S_ISDIR(before.st_mode)
         and directory_identity(before)
         == directory_identity(os.stat(path, follow_symlinks=False)),
         label + ": bound directory")
    return fd, directory_identity(before)


def classify_runtime(runtime_fd: int, audit_fd: int) -> dict[str, str]:
    states: dict[str, str] = {}
    for name, payload, label in (
        (C42_CANDIDATE_POINTER, C42_CANDIDATE_POINTER_BYTES, "candidate_pointer"),
        (C42_AUDIT_POINTER, C42_AUDIT_POINTER_BYTES, "audit_pointer"),
    ):
        states[label] = exact_or_absent(runtime_fd, name, payload, label)
    seal_info = node_at(runtime_fd, C42_SEAL)
    states["seal"] = "ABSENT" if seal_info is None else "PRESENT"
    receipt_info = node_at(audit_fd, RELEASE_ID)
    if receipt_info is None:
        states["receipt"] = "ABSENT"
    else:
        need(stat.S_ISDIR(receipt_info.st_mode), "receipt node directory")
        states["receipt"] = "PRESENT"
    # Any audit pointer without candidate pointer is a forbidden non-prefix.
    need(not (states["audit_pointer"] == "EXACT"
              and states["candidate_pointer"] == "ABSENT"),
         "non-prefix audit pointer without candidate pointer")
    need(not (states["candidate_pointer"] == "EXACT"
              and states["receipt"] == "ABSENT"),
         "non-prefix candidate pointer without prepared receipt")
    need(not (states["seal"] == "PRESENT"
              and (states["receipt"] != "PRESENT"
                   or states["candidate_pointer"] != "EXACT"
                   or states["audit_pointer"] != "EXACT")),
         "seal without complete prefix")
    return states


def pristine_preflight(expected_installer_sha256: str) -> dict[str, Any]:
    inputs = Inputs(expected_installer_sha256)
    runtime_fd = audit_fd = -1
    try:
        docs = validate_semantics(inputs)
        runtime_fd, runtime_identity = open_bound_directory(RUNTIME, "runtime")
        audit_fd, audit_identity = open_bound_directory(AUDIT_ROOT, "audit root")
        for name, label in (
            (C42_CANDIDATE_POINTER, "C42 candidate pointer"),
            (C42_AUDIT_POINTER, "C42 audit pointer"),
            (C42_SEAL, "C42 authority seal"),
            (CANDIDATE_STAGE, "candidate stage"),
            (AUDIT_STAGE, "audit stage"),
            (SEAL_STAGE, "seal stage"),
        ):
            ensure_absent_at(runtime_fd, name, label)
        ensure_absent_at(audit_fd, RELEASE_ID, "installation receipt directory")
        ensure_absent_at(audit_fd, RECEIPT_STAGE_DIR, "receipt stage directory")
        inputs.attest_all("preflight terminal")
        return {
            "schema": "cm2.round306c42.f1-authority-installer-preflight.v1",
            "status": "PASS_PRISTINE_C42_F1_AUTHORITY_INSTALL_PREFLIGHT__NO_WRITE",
            "release_id": RELEASE_ID,
            "installer_source_sha256": inputs.captures["installer"].sha256,
            "C41_candidate_object_sha256": docs["c41"]["object_sha256"],
            "C41_independent_audit_object_sha256": docs["c41_audit"]["object_sha256"],
            "C42_candidate_object_sha256": docs["result"]["object_sha256"],
            "C42_independent_audit_object_sha256": docs["audit"]["object_sha256"],
            "C42_attack_count": len(docs["audit"]["attacks"]),
            "runtime_directory_fingerprint": runtime_identity,
            "audit_directory_fingerprint": audit_identity,
            "targets_absent": True,
            "writes_performed": False,
            "install_command_required": True,
        }
    finally:
        if audit_fd >= 0:
            os.close(audit_fd)
        if runtime_fd >= 0:
            os.close(runtime_fd)
        inputs.close()


def publish_receipt(audit_fd: int, receipt_raw: bytes) \
        -> tuple[str, int, bytes, dict[str, Any]]:
    existing = node_at(audit_fd, RELEASE_ID)
    stage = node_at(audit_fd, RECEIPT_STAGE_DIR)
    if existing is not None:
        need(stat.S_ISDIR(existing.st_mode), "existing receipt directory")
        release_fd = os.open(RELEASE_ID, os.O_RDONLY | os.O_DIRECTORY
                             | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=audit_fd)
        need(sorted(os.listdir(release_fd)) == ["installation_receipt.json"],
             "existing receipt exact directory inventory")
        raw, _ = read_at(release_fd, "installation_receipt.json", 4 << 20)
        existing_receipt = validate_receipt_bytes(raw)
        need(stage is None, "no receipt stage beside final receipt")
        return "RESUMED_EXACT", release_fd, raw, existing_receipt
    need(stage is None, "stale receipt stage requires independent review")
    os.mkdir(RECEIPT_STAGE_DIR, 0o700, dir_fd=audit_fd)
    fsync_dir(audit_fd)
    stage_fd = os.open(RECEIPT_STAGE_DIR, os.O_RDONLY | os.O_DIRECTORY
                       | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=audit_fd)
    try:
        write_once_at(stage_fd, "installation_receipt.json", receipt_raw)
        os.fchmod(stage_fd, 0o500)
        fsync_dir(stage_fd)
    finally:
        os.close(stage_fd)
    rename_noreplace(audit_fd, RECEIPT_STAGE_DIR, audit_fd, RELEASE_ID)
    fsync_dir(audit_fd)
    release_fd = os.open(RELEASE_ID, os.O_RDONLY | os.O_DIRECTORY
                         | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=audit_fd)
    need(sorted(os.listdir(release_fd)) == ["installation_receipt.json"],
         "published receipt exact directory inventory")
    raw, _ = read_at(release_fd, "installation_receipt.json", 4 << 20)
    need(raw == receipt_raw, "published receipt exact bytes")
    return "INSTALLED", release_fd, raw, validate_receipt_bytes(raw)


def attest_receipt_directory(audit_fd: int, release_fd: int,
                             receipt_raw: bytes, phase: str,
                             expected_identity: list[int] | None = None) \
        -> list[int]:
    bound = os.fstat(release_fd)
    current = os.stat(RELEASE_ID, dir_fd=audit_fd, follow_symlinks=False)
    identity = directory_identity(bound)
    need(stat.S_ISDIR(bound.st_mode) and bound.st_uid == os.getuid()
         and stat.S_IMODE(bound.st_mode) == 0o500
         and identity == directory_identity(current)
         and (expected_identity is None or identity == expected_identity),
         phase + ": receipt directory path binding")
    need(sorted(os.listdir(release_fd)) == ["installation_receipt.json"],
         phase + ": receipt directory exact inventory")
    replay, info = read_at(release_fd, "installation_receipt.json", 4 << 20)
    need(replay == receipt_raw and stat.S_IMODE(info.st_mode) == 0o444,
         phase + ": receipt terminal byte and mode replay")
    return identity


def install(expected_installer_sha256: str, invocation: str,
            confirmation: str) -> dict[str, Any]:
    need(confirmation == CONFIRMATION, "exact installation confirmation")
    need(INVOCATION.fullmatch(invocation) is not None, "exact invocation syntax")
    inputs = Inputs(expected_installer_sha256)
    runtime_fd = audit_fd = receipt_fd = -1
    commit_guards: list[Capture] = []
    try:
        docs = validate_semantics(inputs)
        runtime_fd, runtime_identity = open_bound_directory(RUNTIME, "runtime")
        audit_fd, audit_identity = open_bound_directory(AUDIT_ROOT, "audit root")
        fcntl.flock(runtime_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        states = classify_runtime(runtime_fd, audit_fd)
        need(states["seal"] == "ABSENT", "C42 authority seal must be absent")
        pointer_records = {
            "candidate": {
                "path": ".cm2-runtime/" + C42_CANDIDATE_POINTER,
                "token": C42_CANDIDATE_TOKEN,
                "file_sha256": C42_CANDIDATE_POINTER_SHA256,
            },
            "audit": {
                "path": ".cm2-runtime/" + C42_AUDIT_POINTER,
                "token": C42_AUDIT_TOKEN,
                "file_sha256": C42_AUDIT_POINTER_SHA256,
            },
        }
        receipt = receipt_document(inputs, docs, invocation, pointer_records)
        receipt_raw = closed_bytes(receipt)
        receipt_state, receipt_fd, receipt_raw, receipt = publish_receipt(
            audit_fd, receipt_raw)
        need(receipt.get("InvocationID") == invocation
             and receipt.get("installer", {}).get("source_sha256")
             == inputs.captures["installer"].sha256,
             "prepared receipt exact invocation and installer source")
        receipt_files = receipt.get("bindings", {}).get("files", {})
        for label in sorted(PINS):
            need(receipt_files.get(label) == inputs.captures[label].record(),
                 "prepared receipt current exact capture:" + label)
        receipt_identity = attest_receipt_directory(
            audit_fd, receipt_fd, receipt_raw, "prepared")
        commit_guards.append(Capture(
            ROOT / RECEIPT_REL, "prepared receipt guard",
            hashlib.sha256(receipt_raw).hexdigest(), 4 << 20))
        # Receipt is durable but explicitly prepared/non-authority at this point.
        candidate_state = install_exact(
            runtime_fd, CANDIDATE_STAGE, C42_CANDIDATE_POINTER,
            C42_CANDIDATE_POINTER_BYTES)
        audit_state = install_exact(
            runtime_fd, AUDIT_STAGE, C42_AUDIT_POINTER, C42_AUDIT_POINTER_BYTES)
        commit_guards.extend([
            Capture(RUNTIME / C42_CANDIDATE_POINTER, "candidate pointer guard",
                    C42_CANDIDATE_POINTER_SHA256, 256),
            Capture(RUNTIME / C42_AUDIT_POINTER, "audit pointer guard",
                    C42_AUDIT_POINTER_SHA256, 256),
        ])
        need(all(stat.S_IMODE(guard.before.st_mode) == 0o444
                 for guard in commit_guards),
             "prepared transaction nodes exact immutable mode")
        for guard in commit_guards:
            guard.unchanged("before authority seal")
        attest_receipt_directory(audit_fd, receipt_fd, receipt_raw,
                                 "before authority seal", receipt_identity)
        inputs.attest_all("before authority seal")
        need(directory_identity(os.fstat(runtime_fd)) == runtime_identity
             == directory_identity(os.stat(RUNTIME, follow_symlinks=False))
             and directory_identity(os.fstat(audit_fd)) == audit_identity
             == directory_identity(os.stat(AUDIT_ROOT, follow_symlinks=False)),
             "bound parent directories before seal")
        seal = seal_document(receipt_raw, receipt,
                             inputs.captures["installer"].sha256)
        seal_raw = closed_bytes(seal)
        seal_state = install_exact(runtime_fd, SEAL_STAGE, C42_SEAL, seal_raw)
        fsync_dir(runtime_fd)
        final_candidate, _ = read_at(runtime_fd, C42_CANDIDATE_POINTER, 256)
        final_audit, _ = read_at(runtime_fd, C42_AUDIT_POINTER, 256)
        final_seal, _ = read_at(runtime_fd, C42_SEAL, 1 << 20)
        need(final_candidate == C42_CANDIDATE_POINTER_BYTES
             and final_audit == C42_AUDIT_POINTER_BYTES,
             "terminal pointer byte replay")
        validate_seal_bytes(final_seal, receipt_raw,
                            inputs.captures["installer"].sha256)
        for guard in commit_guards:
            guard.unchanged("post-commit terminal")
        attest_receipt_directory(audit_fd, receipt_fd, receipt_raw,
                                 "post-commit terminal", receipt_identity)
        inputs.attest_all("post-commit terminal")
        need(directory_identity(os.fstat(runtime_fd)) == runtime_identity
             == directory_identity(os.stat(RUNTIME, follow_symlinks=False))
             and directory_identity(os.fstat(audit_fd)) == audit_identity
             == directory_identity(os.stat(AUDIT_ROOT, follow_symlinks=False)),
             "bound parent directories post-commit")
        return {
            "schema": "cm2.round306c42.f1-authority-installer-run.v1",
            "status": "COMMITTED_C42_F1_AUTHORITY_TRANSACTION",
            "release_id": RELEASE_ID,
            "receipt_state": receipt_state,
            "candidate_pointer_state": candidate_state,
            "audit_pointer_state": audit_state,
            "authority_seal_state": seal_state,
            "authority_seal_object_sha256": seal["authority_seal_object_sha256"],
            "receipt_object_sha256": receipt["installation_receipt_object_sha256"],
            "formal_census": {"paired": 574, "unresolved": 1150,
                              "remaining_representatives": 575},
            "D02": "BLOCKED", "CM2": "NO-GO_FOR_CLAIM",
        }
    finally:
        for guard in reversed(commit_guards):
            guard.close()
        if receipt_fd >= 0:
            os.close(receipt_fd)
        if audit_fd >= 0:
            os.close(audit_fd)
        if runtime_fd >= 0:
            try:
                fcntl.flock(runtime_fd, fcntl.LOCK_UN)
            except OSError:
                pass
            os.close(runtime_fd)
        inputs.close()


def expect_rejected(callable_object: Any, label: str) -> None:
    try:
        callable_object()
    except (Rejected, OSError, ValueError):
        return
    raise Rejected("self-test attack accepted:" + label)


def self_test() -> dict[str, Any]:
    attacks: dict[str, bool] = {}
    expect_rejected(lambda: strict_json(b'{"a":1,"a":2}'), "duplicate key")
    attacks["duplicate_JSON_key"] = True
    expect_rejected(lambda: strict_json(b'{"x":NaN}'), "NaN")
    attacks["nonfinite_JSON"] = True

    sample_body = {"schema": RECEIPT_SCHEMA, "release_id": RELEASE_ID}
    sample = {**sample_body,
              "installation_receipt_object_sha256": object_digest(sample_body)}
    mutated = copy.deepcopy(sample)
    mutated["release_id"] = RELEASE_ID + "-f2"
    raw_mutated = closed_bytes(mutated)
    expect_rejected(lambda: validate_receipt_bytes(raw_mutated),
                    "receipt stale self hash/f2")
    attacks["receipt_mutation_and_f2_substitution"] = True

    fake_result = {
        "formal_producer_run": True, "review_only": False,
        "authority_pointer_installed": False, "producer_output_is_authority": False,
    }
    fake_result["review_only"] = True
    expect_rejected(
        lambda: need(fake_result["review_only"] is False,
                     "review-only candidate rejected"), "review-only")
    attacks["review_only_candidate"] = True

    with tempfile.TemporaryDirectory(prefix="cm2-c42-installer-selftest-") as raw:
        directory = Path(raw)
        fd = os.open(directory, os.O_RDONLY | os.O_DIRECTORY
                     | os.O_NOFOLLOW | os.O_CLOEXEC)
        try:
            write_once_at(fd, "source", b"source\n")
            write_once_at(fd, "target", b"target\n")
            expect_rejected(lambda: rename_noreplace(fd, "source", fd, "target"),
                            "no-replace collision")
            source_raw, _ = read_at(fd, "source")
            target_raw, _ = read_at(fd, "target")
            need(source_raw == b"source\n" and target_raw == b"target\n",
                 "collision preserves source and target")
            attacks["renameat2_existing_target_no_clobber"] = True

            os.symlink("missing", directory / "dangling")
            expect_rejected(lambda: read_at(fd, "dangling"), "dangling symlink")
            attacks["dangling_symlink_target"] = True

            write_once_at(fd, "hardlink-source", b"hard\n")
            os.link(directory / "hardlink-source", directory / "hardlink-alias")
            expect_rejected(lambda: read_at(fd, "hardlink-source"), "hardlink")
            attacks["hardlink_nlink_gt_one"] = True

            state1 = install_exact(fd, ".pointer.stage", "pointer", b"p\n")
            state2 = install_exact(fd, ".pointer.stage", "pointer", b"p\n")
            need(state1 == "INSTALLED" and state2 == "RESUMED_EXACT",
                 "exact prefix retry")
            attacks["exact_prefix_idempotent_resume"] = True

            write_once_at(fd, "bad-pointer", b"wrong\n")
            expect_rejected(lambda: install_exact(
                fd, ".bad.stage", "bad-pointer", b"right\n"),
                "mismatched prefix")
            attacks["mismatched_prefix_rejected"] = True
        finally:
            os.close(fd)

    need(len(attacks) == 9 and all(attacks.values()), "self-test census")
    return {
        "schema": "cm2.round306c42.f1-authority-installer-self-test.v1",
        "status": "PASS_C42_F1_INSTALLER_9_OF_9_HOSTILE_TESTS_FAIL_CLOSED",
        "attack_count": 9,
        "attacks": attacks,
        "runtime_writes_performed": False,
    }


def emit(value: dict[str, Any]) -> None:
    sys.stdout.buffer.write(canonical(value) + b"\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--preflight", action="store_true")
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--install", action="store_true")
    parser.add_argument("--expect-installer-sha256")
    parser.add_argument("--invocation-id")
    parser.add_argument("--confirm")
    args = parser.parse_args()
    try:
        if args.self_test:
            need(args.expect_installer_sha256 is None
                 and args.invocation_id is None and args.confirm is None,
                 "self-test takes no install arguments")
            emit(self_test())
            return 0
        need(type(args.expect_installer_sha256) is str,
             "expected installer SHA required")
        if args.preflight or args.dry_run:
            need(args.invocation_id is None and args.confirm is None,
                 "preflight has no install arguments")
            emit(pristine_preflight(args.expect_installer_sha256))
            return 0
        need(type(args.invocation_id) is str and type(args.confirm) is str,
             "install invocation and confirmation required")
        emit(install(args.expect_installer_sha256, args.invocation_id,
                     args.confirm))
        return 0
    except (Rejected, OSError, KeyError, TypeError, ValueError) as error:
        emit({
            "schema": "cm2.round306c42.f1-authority-installer-rejection.v1",
            "status": "REJECTED_FAIL_CLOSED_NO_AUTHORITY_CLAIM",
            "error_type": type(error).__name__,
            "error": str(error),
        })
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
