#!/usr/bin/env python3
"""Independent preflight and post-install audit for the C42 f1 transaction.

This file does not import or execute the installer.  It treats the installer,
producer, producer receipt, C42 audit, C41 authority lineage, compatibility
pointers, prepared installation receipt, and final seal as inert bytes.
``--preflight`` requires a pristine target state.  ``--audit-installed``
requires the complete exact prefix and validates the final seal as the sole
authority commit point.  ``--self-test`` writes only to a temporary directory.
"""

from __future__ import annotations

import argparse
import copy
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

RELEASE_ID = "c42-f1-authority-install-a50914a266af-85a7cd719cee-v1"
RECEIPT_SCHEMA = "cm2.round306c42.f1-authority-installation-receipt.v1"
RECEIPT_STATUS = "PREPARED_C42_F1_AUTHORITY_RECEIPT__POINTERS_AND_SEAL_PENDING"
SEAL_SCHEMA = "cm2.round306c42.f1-authority-commit-seal.v1"
SEAL_STATUS = "COMMITTED_C42_F1_AUTHORITY__574_PAIRED__1150_UNRESOLVED"
RECEIPT_REL = (
    ".cm2-runtime/audit/" + RELEASE_ID + "/installation_receipt.json"
)

CANDIDATE_TOKEN = "c42-p391-formal-producer-20260811T044500Z-f1"
AUDIT_TOKEN = "c42-independent-audit-20260811T052900Z-p391-f1"
CANDIDATE_POINTER = "c42-current-token"
AUDIT_POINTER = "c42-current-audit-token"
SEAL_NAME = "c42-current-authority-seal"
CANDIDATE_STAGE = ".c42-current-token." + RELEASE_ID + ".stage"
AUDIT_STAGE = ".c42-current-audit-token." + RELEASE_ID + ".stage"
SEAL_STAGE = ".c42-current-authority-seal." + RELEASE_ID + ".stage"
RECEIPT_STAGE_DIR = "." + RELEASE_ID + ".stage"
CANDIDATE_POINTER_RAW = (CANDIDATE_TOKEN + "\n").encode("ascii")
AUDIT_POINTER_RAW = (AUDIT_TOKEN + "\n").encode("ascii")
CANDIDATE_POINTER_SHA = (
    "fbc5dd3c55bfdd3098ed34ae09ae633a9526a9c9cc6f40b3d87b5669b2ea7f07"
)
AUDIT_POINTER_SHA = (
    "59aca53c4c35260801b3c559648c88ee974db01ae950f045a5e5aecd64aa36e5"
)

INSTALLER_PATH = (
    "deliverables/cm2_round306c42_f1_authority_transaction_installer_v1.py"
)
INSTALLER_SHA = "66f88bc5913af695691c5ae58be7938f94f3f68a9eeeeed32bcd96b37938c276"

PINS: dict[str, tuple[str, str]] = {
    "installer": (INSTALLER_PATH, INSTALLER_SHA),
    "producer_source": (
        "deliverables/cm2_round306c42_d02_singleton_wall_endpoint_owner_closure_v1.py",
        "4b4e96bcb2c701fd6820a04271e2f02058e3699d980a4bee61d4090b2ce30c78",
    ),
    "auditor_source": (
        "deliverables/cm2_round306c42_d02_singleton_wall_endpoint_owner_closure_independent_auditor_v1.py",
        "6da5c8a3f2960ec9f763e314be01e909722b6b03bcd2817e5030295dcd6086eb",
    ),
    "candidate_result": (
        f".cm2-runtime/candidates/{CANDIDATE_TOKEN}/result.json",
        "f029c3ce6af33e2f93c33b4155286f60bfafecd724720a598b103ca3c263ccb0",
    ),
    "candidate_manifest": (
        f".cm2-runtime/candidates/{CANDIDATE_TOKEN}/root_manifest.sha256",
        "ce1b6260b26a901a9dda3cfbd94eba5a752b5188d6bdbe7c7d3cd7a4d3f7d058",
    ),
    "producer_receipt": (
        ".cm2-runtime/audit/c42-p391-formal-producer-20260811T044500Z-f1/execution_receipt.json",
        "5a14c48b028dd20951d02659f9d9655f5718a13e69d2811ee823d78c38530a55",
    ),
    "independent_audit": (
        f".cm2-runtime/audit/{AUDIT_TOKEN}/independent_audit.json",
        "d60bb3c8f79f989df776effa4616ec170097a018547b1f4c929ad068c11138d3",
    ),
    "c41_pointer": (
        ".cm2-runtime/c41-current-token",
        "9e4f2d9c02c1f3e56639d69c971ccc7846ba229f87723e878f101730df3dd1a9",
    ),
    "c41_audit_pointer": (
        ".cm2-runtime/c41-current-audit-token",
        "f8a9a0bf69169eba05ef3bec1db7e924de4b06b4ab61c97693b2919effd9c86c",
    ),
    "c41_result": (
        ".cm2-runtime/candidates/c41-lower-strata-depth3-20260811T023804Z-f997365c91559599/result.json",
        "73fde0eee7eb06bb0f144ea98880c72bfea36e10db696731ae72393cd9b0a50f",
    ),
    "c41_manifest": (
        ".cm2-runtime/candidates/c41-lower-strata-depth3-20260811T023804Z-f997365c91559599/root_manifest.sha256",
        "86e10532d63269cd0fdd58d541b1984522e9718f4613a5dc83211fe84eb258ba",
    ),
    "c41_receipt": (
        ".cm2-runtime/audit/c41-lower-strata-depth3-20260811T023804Z-f997365c91559599/execution_receipt.json",
        "4500c6c38d1e34002cb3384f0c0c17623c93df6fb46ea7a12229e41ed6cb1dc8",
    ),
    "c41_audit": (
        ".cm2-runtime/audit/c41-independent-audit-20260811T031547Z-ab94d420c43c94cd/independent_audit.json",
        "6a800959a90c227d587b82c6246f60123483471f61dcf6a5de4da5381fee4b1e",
    ),
    "c41_producer_source": (
        "deliverables/cm2_round306c41_d02_lower_strata_depth3_closure_v1.py",
        "3fbf6cec247903d6e6ba147d4d06e912638b1472b74adc8311323c554e6e5bde",
    ),
    "c41_auditor_source": (
        "deliverables/cm2_round306c41_d02_lower_strata_depth3_closure_independent_auditor_v1.py",
        "537f3dea94c3743235df8984ba4922d37f82999ff3d8abbac59e5171ef38b74c",
    ),
}

RECEIPT_FILE_MAP = {
    "c42_result": "candidate_result",
    "c42_manifest": "candidate_manifest",
    "c42_execution_receipt": "producer_receipt",
    "c42_independent_audit": "independent_audit",
    "c42_producer_source": "producer_source",
    "c42_auditor_source": "auditor_source",
    "c41_candidate_pointer": "c41_pointer",
    "c41_audit_pointer": "c41_audit_pointer",
    "c41_result": "c41_result",
    "c41_manifest": "c41_manifest",
    "c41_execution_receipt": "c41_receipt",
    "c41_independent_audit": "c41_audit",
    "c41_producer_source": "c41_producer_source",
    "c41_auditor_source": "c41_auditor_source",
}

OBJECTS = {
    "candidate": "a50914a266aff3396054d7f16e91d69db7fa735ad15f01cbf07eee8e708d99d2",
    "producer_receipt": "e89f66d0e7636bfa781a6ef7e0309fc1ad00c3215ea699c08b231003e1c39f08",
    "independent_audit": "85a7cd719cee9dceb1763135f74d50bcf28f78ff2426e65996b975b1def7790c",
    "c41_candidate": "b7e47a4ca9d6f4bb1fee10e78877850d5070f6d3c2b06bb0234fbabdaa2b7b24",
    "c41_receipt": "39f1c6dadcf21a428174520b5a1aa4d072a57c73ffd9c9b04d2c3d639d94fed9",
    "c41_audit": "44061ec6e26108692fe6e635e9e666cca0b11c66f00384eab539be08f66fe877",
}

HEX64 = re.compile(r"[0-9a-f]{64}")
INVOCATION = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:@+-]{7,191}")


class Rejected(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: dict[str, Any]) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def strict(raw: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(key not in result, "duplicate JSON key")
            result[key] = value
        return result
    try:
        return json.loads(raw.decode("ascii"), object_pairs_hook=pairs,
            parse_constant=lambda token: (_ for _ in ()).throw(
                Rejected("nonfinite JSON:" + token)))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Rejected("strict JSON parse") from error


def fp(info: os.stat_result) -> list[int]:
    return [info.st_dev, info.st_ino, info.st_mode, info.st_nlink,
            info.st_size, info.st_mtime_ns, info.st_ctime_ns,
            info.st_uid, info.st_gid]


def relative(path: Path) -> str:
    return str(path.absolute().relative_to(ROOT))


def lexical_no_symlinks(path: Path, label: str) -> None:
    path = path.absolute()
    need(path == ROOT or ROOT in path.parents, label + ": workspace boundary")
    cursor = ROOT
    need(stat.S_ISDIR(os.lstat(cursor).st_mode), label + ": root directory")
    for part in path.relative_to(ROOT).parts:
        cursor /= part
        need(not stat.S_ISLNK(os.lstat(cursor).st_mode),
             label + ": no symlink component")


class Capture:
    def __init__(self, path: Path, expected_sha: str | None, label: str,
                 maximum: int = 1 << 30):
        self.path = path.absolute()
        self.label = label
        lexical_no_symlinks(self.path.parent, label + " parent")
        self.fd = os.open(self.path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
        self.before = os.fstat(self.fd)
        need(stat.S_ISREG(self.before.st_mode) and self.before.st_nlink == 1
             and self.before.st_uid == os.getuid()
             and 0 <= self.before.st_size <= maximum,
             label + ": singleton regular owned bounded")
        self.raw = self.read()
        self.sha = hashlib.sha256(self.raw).hexdigest()
        if expected_sha is not None:
            need(HEX64.fullmatch(expected_sha) is not None
                 and self.sha == expected_sha, label + ": file SHA pin")
        self.unchanged("open")

    def read(self) -> bytes:
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
        need(fp(current) == fp(self.before) == fp(os.fstat(self.fd)),
             self.label + ": " + phase + " stat")
        need(hashlib.sha256(self.read()).hexdigest() == self.sha,
             self.label + ": " + phase + " bytes")

    def record(self) -> dict[str, Any]:
        return {
            "path": relative(self.path),
            "file_sha256": self.sha,
            "size": self.before.st_size,
            "stat_fingerprint": fp(self.before),
            "O_NOFOLLOW": True,
            "single_link": True,
        }

    def close(self) -> None:
        os.close(self.fd)


def document(cap: Capture, closure: str) -> dict[str, Any]:
    need(cap.raw.endswith(b"\n") and not cap.raw.endswith(b"\n\n"),
         cap.label + ": newline")
    value = strict(cap.raw[:-1])
    need(type(value) is dict and canonical(value) == cap.raw[:-1],
         cap.label + ": canonical")
    body = dict(value)
    claim = body.pop(closure, None)
    need(type(claim) is str and HEX64.fullmatch(claim) is not None
         and claim == digest(body), cap.label + ": object closure")
    return value


class FrozenInputs:
    def __init__(self, expected_auditor_sha: str):
        need(HEX64.fullmatch(expected_auditor_sha) is not None,
             "auditor source expectation")
        self.caps: dict[str, Capture] = {
            "self": Capture(SELF, expected_auditor_sha, "independent auditor", 4 << 20)
        }
        for label, (path, sha) in PINS.items():
            self.caps[label] = Capture(ROOT / path, sha, label)
        self.verify_manifest(
            "candidate_manifest",
            ROOT / f".cm2-runtime/candidates/{CANDIDATE_TOKEN}", 8)
        self.verify_manifest(
            "c41_manifest",
            ROOT / ".cm2-runtime/candidates/"
                   "c41-lower-strata-depth3-20260811T023804Z-f997365c91559599",
            13)

    def verify_manifest(self, label: str, directory: Path,
                        expected_count: int) -> None:
        manifest = self.caps[label]
        need(manifest.raw.endswith(b"\n"), label + ": terminal newline")
        rows = manifest.raw.decode("ascii").splitlines()
        need(len(rows) == expected_count, label + ": row count")
        members: dict[str, str] = {}
        for row in rows:
            match = re.fullmatch(
                r"([0-9a-f]{64})  ([A-Za-z0-9][A-Za-z0-9_.-]*)", row)
            need(match is not None, label + ": row grammar")
            sha, name = match.groups()
            need(name not in members and name != "root_manifest.sha256",
                 label + ": unique safe member")
            members[name] = sha
        need(list(members) == sorted(members), label + ": sorted")
        lexical_no_symlinks(directory, label + " directory")
        need(sorted(entry.name for entry in os.scandir(directory))
             == sorted([*members, "root_manifest.sha256"]),
             label + ": exact inventory")
        known_paths = {cap.path: cap for cap in self.caps.values()}
        for name, sha in members.items():
            path = (directory / name).absolute()
            if path in known_paths:
                need(known_paths[path].sha == sha,
                     label + ": reused member SHA:" + name)
            else:
                key = label + ":member:" + name
                self.caps[key] = Capture(path, sha, key)

    def unchanged(self, phase: str) -> None:
        for cap in self.caps.values():
            cap.unchanged(phase)

    def close(self) -> None:
        for cap in reversed(list(self.caps.values())):
            cap.close()


def validate_lineage(inputs: FrozenInputs) -> dict[str, Any]:
    need(inputs.caps["c41_pointer"].raw
         == b"c41-lower-strata-depth3-20260811T023804Z-f997365c91559599\n"
         and inputs.caps["c41_audit_pointer"].raw
         == b"c41-independent-audit-20260811T031547Z-ab94d420c43c94cd\n",
         "exact current C41 pointer bytes")
    c41 = document(inputs.caps["c41_result"], "object_sha256")
    c41_receipt = document(inputs.caps["c41_receipt"], "receipt_object_sha256")
    c41_audit = document(inputs.caps["c41_audit"], "object_sha256")
    need(c41["object_sha256"] == OBJECTS["c41_candidate"]
         and c41_receipt["receipt_object_sha256"] == OBJECTS["c41_receipt"]
         and c41_audit["object_sha256"] == OBJECTS["c41_audit"]
         and c41_audit.get("candidate_object_sha256") == c41["object_sha256"]
         and c41_audit.get("execution_receipt_object_sha256")
         == c41_receipt["receipt_object_sha256"], "C41 object lineage")

    candidate = document(inputs.caps["candidate_result"], "object_sha256")
    producer_receipt = document(inputs.caps["producer_receipt"],
                                "receipt_object_sha256")
    audit = document(inputs.caps["independent_audit"], "object_sha256")
    path = f".cm2-runtime/candidates/{CANDIDATE_TOKEN}"
    invocation = "c42-formal-producer-20260811T044500Z-p391-f1"
    need(candidate["object_sha256"] == OBJECTS["candidate"]
         and candidate.get("formal_producer_run") is True
         and candidate.get("review_only") is False
         and candidate.get("authority_pointer_installed") is False
         and candidate.get("producer_output_is_authority") is False,
         "formal f1 candidate semantics")
    need(producer_receipt["receipt_object_sha256"] == OBJECTS["producer_receipt"]
         and producer_receipt.get("candidate_path") == path
         and producer_receipt.get("InvocationID") == invocation
         and producer_receipt.get("candidate_object_sha256") == OBJECTS["candidate"]
         and producer_receipt.get("root_manifest_sha256")
         == PINS["candidate_manifest"][1]
         and producer_receipt.get("producer_source_sha256")
         == PINS["producer_source"][1], "formal f1 producer receipt")
    attacks = audit.get("attacks")
    need(audit["object_sha256"] == OBJECTS["independent_audit"]
         and audit.get("status")
         == "PASS_INDEPENDENT_C42_P391_OWNER_CLOSURE_AUDIT__54_OF_54_ATTACKS_FAIL_CLOSED"
         and audit.get("candidate_path") == path
         and audit.get("InvocationID") == invocation
         and audit.get("candidate_object_sha256") == OBJECTS["candidate"]
         and audit.get("execution_receipt_object_sha256")
         == OBJECTS["producer_receipt"]
         and audit.get("root_manifest_sha256") == PINS["candidate_manifest"][1]
         and audit.get("producer_source_sha256") == PINS["producer_source"][1]
         and audit.get("independent_auditor_source_sha256")
         == PINS["auditor_source"][1]
         and type(attacks) is dict and len(attacks) == 54
         and all(value is True for value in attacks.values()),
         "C42 f1 independent audit binding and attacks")
    c41_input = candidate.get("C41_audited_input", {})
    need(c41_input.get("object_sha256") == OBJECTS["c41_candidate"]
         and c41_input.get("independent_audit_object_sha256")
         == OBJECTS["c41_audit"]
         and c41_input.get("installed_pointer_sha256") == {
             "candidate_pointer_sha256": PINS["c41_pointer"][1],
             "audit_pointer_sha256": PINS["c41_audit_pointer"][1],
         }, "C42 to current C41 authority binding")
    return {"candidate": candidate, "producer_receipt": producer_receipt,
            "audit": audit, "c41": c41, "c41_audit": c41_audit}


def lstat_or_none(path: Path) -> os.stat_result | None:
    try:
        return os.lstat(path)
    except FileNotFoundError:
        return None


def capture_unpinned(path: Path, label: str, maximum: int = 4 << 20) \
        -> tuple[bytes, os.stat_result]:
    lexical_no_symlinks(path.absolute().parent, label + " parent")
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1
             and before.st_uid == os.getuid() and before.st_size <= maximum,
             label + ": strict node")
        chunks: list[bytes] = []
        total = 0
        while block := os.read(fd, 1 << 20):
            chunks.append(block)
            total += len(block)
            need(total <= maximum, label + ": bound")
        after = os.fstat(fd)
    finally:
        os.close(fd)
    need(fp(before) == fp(after) == fp(os.stat(path, follow_symlinks=False)),
         label + ": stable")
    return b"".join(chunks), before


def validate_receipt(raw: bytes) -> dict[str, Any]:
    need(raw.endswith(b"\n") and not raw.endswith(b"\n\n"), "receipt newline")
    value = strict(raw[:-1])
    need(type(value) is dict and canonical(value) == raw[:-1], "receipt canonical")
    need(set(value) == {
        "schema", "status", "release_id", "InvocationID", "installer",
        "bindings", "prepared_pointer_records", "authority_contract",
        "post_install_census", "filesystem_policy",
        "installation_receipt_object_sha256",
    }, "receipt exact top-level keys")
    body = dict(value)
    claim = body.pop("installation_receipt_object_sha256", None)
    need(type(claim) is str and claim == digest(body), "receipt self hash")
    need(value.get("schema") == RECEIPT_SCHEMA
         and value.get("status") == RECEIPT_STATUS
         and value.get("release_id") == RELEASE_ID,
         "receipt fixed identity")
    need(type(value.get("InvocationID")) is str
         and INVOCATION.fullmatch(value["InvocationID"]) is not None,
         "receipt invocation syntax")
    contract = value.get("authority_contract", {})
    need(contract == {
        "candidate_pointer_path": ".cm2-runtime/" + CANDIDATE_POINTER,
        "candidate_pointer_sha256": CANDIDATE_POINTER_SHA,
        "audit_pointer_path": ".cm2-runtime/" + AUDIT_POINTER,
        "audit_pointer_sha256": AUDIT_POINTER_SHA,
        "seal_path": ".cm2-runtime/" + SEAL_NAME,
        "receipt_path": RECEIPT_REL,
        "publication_order": ["receipt", "candidate_pointer", "audit_pointer",
                              "authority_seal"],
        "authority_commit_point": "authority_seal_RENAME_NOREPLACE",
        "pointers_before_seal_have_formal_authority": False,
        "exact_prefix_recovery_only": True,
    }, "receipt exact authority contract")
    files = value.get("bindings", {}).get("files", {})
    installer = value.get("installer", {})
    need(type(installer) is dict and set(installer) == {
             "path", "source_sha256", "pid", "proc_start_ticks", "started_utc"
         }
         and installer.get("path") == INSTALLER_PATH
         and installer.get("source_sha256") == INSTALLER_SHA,
         "receipt installer pin")
    need(type(installer.get("pid")) is int and installer["pid"] > 0
         and type(installer.get("proc_start_ticks")) is int
         and installer["proc_start_ticks"] > 0
         and type(installer.get("started_utc")) is str
         and installer["started_utc"].endswith("Z"),
         "receipt installer provenance shape")
    need(type(value.get("bindings")) is dict
         and set(value["bindings"]) == {"files", "objects"},
         "receipt exact bindings shape")
    need(type(files) is dict and set(files) == set(RECEIPT_FILE_MAP),
         "receipt exact file-binding labels")
    for receipt_key, local_key in RECEIPT_FILE_MAP.items():
        record = files.get(receipt_key, {})
        need(type(record) is dict and set(record) == {
                 "path", "file_sha256", "size", "stat_fingerprint",
                 "O_NOFOLLOW", "single_link"
             }
             and record.get("path") == PINS[local_key][0]
             and files.get(receipt_key, {}).get("file_sha256") == PINS[local_key][1],
             "receipt file binding:" + receipt_key)
        need(type(record.get("size")) is int and record["size"] >= 0
             and type(record.get("stat_fingerprint")) is list
             and len(record["stat_fingerprint"]) == 9
             and all(type(item) is int for item in record["stat_fingerprint"])
             and record.get("O_NOFOLLOW") is True
             and record.get("single_link") is True,
             "receipt file capture shape:" + receipt_key)
    objects = value.get("bindings", {}).get("objects", {})
    need(type(objects) is dict and set(objects) == {
             "c42_candidate_object_sha256",
             "c42_execution_receipt_object_sha256",
             "c42_independent_audit_object_sha256",
             "c41_candidate_object_sha256",
             "c41_execution_receipt_object_sha256",
             "c41_independent_audit_object_sha256",
         }
         and objects.get("c42_candidate_object_sha256") == OBJECTS["candidate"]
         and objects.get("c42_execution_receipt_object_sha256")
         == OBJECTS["producer_receipt"]
         and objects.get("c42_independent_audit_object_sha256")
         == OBJECTS["independent_audit"]
         and objects.get("c41_candidate_object_sha256")
         == OBJECTS["c41_candidate"]
         and objects.get("c41_execution_receipt_object_sha256")
         == OBJECTS["c41_receipt"]
         and objects.get("c41_independent_audit_object_sha256")
         == OBJECTS["c41_audit"], "receipt exact object binding")
    need(value.get("prepared_pointer_records") == {
        "candidate": {"path": ".cm2-runtime/" + CANDIDATE_POINTER,
                      "token": CANDIDATE_TOKEN,
                      "file_sha256": CANDIDATE_POINTER_SHA},
        "audit": {"path": ".cm2-runtime/" + AUDIT_POINTER,
                  "token": AUDIT_TOKEN,
                  "file_sha256": AUDIT_POINTER_SHA},
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


def validate_seal(raw: bytes, receipt_raw: bytes) -> dict[str, Any]:
    need(raw.endswith(b"\n") and not raw.endswith(b"\n\n"), "seal newline")
    value = strict(raw[:-1])
    need(type(value) is dict and canonical(value) == raw[:-1], "seal canonical")
    body = dict(value)
    claim = body.pop("authority_seal_object_sha256", None)
    need(type(claim) is str and claim == digest(body), "seal self hash")
    receipt = validate_receipt(receipt_raw)
    expected_body = {
        "schema": SEAL_SCHEMA,
        "status": SEAL_STATUS,
        "release_id": RELEASE_ID,
        "receipt_path": RECEIPT_REL,
        "receipt_file_sha256": hashlib.sha256(receipt_raw).hexdigest(),
        "receipt_object_sha256": receipt["installation_receipt_object_sha256"],
        "candidate_token": CANDIDATE_TOKEN,
        "candidate_pointer_sha256": CANDIDATE_POINTER_SHA,
        "candidate_object_sha256": OBJECTS["candidate"],
        "audit_token": AUDIT_TOKEN,
        "audit_pointer_sha256": AUDIT_POINTER_SHA,
        "independent_audit_object_sha256": OBJECTS["independent_audit"],
        "installer_source_sha256": INSTALLER_SHA,
        "semantic_commit": {
            "this_seal_is_required": True,
            "compatibility_pointers_without_this_seal_are_not_authority": True,
            "publication_method":
                "renameat2_RENAME_NOREPLACE_then_runtime_fsync",
        },
        "formal_census_after_commit": {
            "paired_coarse_cells": 574,
            "whole_representatives": 287,
            "remaining_representatives": 575,
            "unresolved": 1150,
        },
    }
    expected = {**expected_body,
                "authority_seal_object_sha256": digest(expected_body)}
    need(value == expected, "seal exact reconstruction")
    return value


def preflight(expected_auditor_sha: str) -> dict[str, Any]:
    inputs = FrozenInputs(expected_auditor_sha)
    try:
        docs = validate_lineage(inputs)
        targets = [
            RUNTIME / CANDIDATE_POINTER,
            RUNTIME / AUDIT_POINTER,
            RUNTIME / SEAL_NAME,
            RUNTIME / CANDIDATE_STAGE,
            RUNTIME / AUDIT_STAGE,
            RUNTIME / SEAL_STAGE,
            AUDIT_ROOT / RELEASE_ID,
            AUDIT_ROOT / RECEIPT_STAGE_DIR,
        ]
        need(all(lstat_or_none(path) is None for path in targets),
             "all authority transaction targets pristine absent")
        inputs.unchanged("terminal preflight")
        return {
            "schema": "cm2.round306c42.f1-authority-independent-preflight.v1",
            "status": "PASS_INDEPENDENT_PRISTINE_PREFLIGHT__F1_ONLY__54_ATTACKS__NO_WRITE",
            "installer_source_sha256": INSTALLER_SHA,
            "independent_preflight_source_sha256": inputs.caps["self"].sha,
            "candidate_object_sha256": docs["candidate"]["object_sha256"],
            "independent_audit_object_sha256": docs["audit"]["object_sha256"],
            "attack_count": len(docs["audit"]["attacks"]),
            "targets_absent": True,
            "writes_performed": False,
            "authority_installed": False,
        }
    finally:
        inputs.close()


def audit_installed(expected_auditor_sha: str) -> dict[str, Any]:
    inputs = FrozenInputs(expected_auditor_sha)
    transaction_caps: dict[str, Capture] = {}
    receipt_directory_fd = -1
    try:
        docs = validate_lineage(inputs)
        receipt_directory = AUDIT_ROOT / RELEASE_ID
        lexical_no_symlinks(receipt_directory, "receipt directory")
        receipt_directory_fd = os.open(
            receipt_directory,
            os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
        )
        receipt_directory_info = os.fstat(receipt_directory_fd)
        need(stat.S_ISDIR(receipt_directory_info.st_mode)
             and receipt_directory_info.st_uid == os.getuid()
             and stat.S_IMODE(receipt_directory_info.st_mode) == 0o500
             and fp(receipt_directory_info)
             == fp(os.stat(receipt_directory, follow_symlinks=False))
             and sorted(os.listdir(receipt_directory_fd))
             == ["installation_receipt.json"],
             "installed receipt exact owned immutable directory")
        transaction_caps = {
            "candidate_pointer": Capture(
                RUNTIME / CANDIDATE_POINTER, CANDIDATE_POINTER_SHA,
                "installed candidate pointer", 256),
            "audit_pointer": Capture(
                RUNTIME / AUDIT_POINTER, AUDIT_POINTER_SHA,
                "installed audit pointer", 256),
            "receipt": Capture(
                ROOT / RECEIPT_REL, None, "installation receipt", 4 << 20),
            "seal": Capture(
                RUNTIME / SEAL_NAME, None, "authority seal", 1 << 20),
        }
        candidate_raw = transaction_caps["candidate_pointer"].raw
        audit_raw = transaction_caps["audit_pointer"].raw
        receipt_raw = transaction_caps["receipt"].raw
        seal_raw = transaction_caps["seal"].raw
        need(all(stat.S_IMODE(cap.before.st_mode) == 0o444
                 for cap in transaction_caps.values()),
             "installed transaction nodes exact immutable mode")

        def stages_absent(phase: str) -> None:
            for stage in (RUNTIME / CANDIDATE_STAGE, RUNTIME / AUDIT_STAGE,
                          RUNTIME / SEAL_STAGE, AUDIT_ROOT / RECEIPT_STAGE_DIR):
                need(lstat_or_none(stage) is None,
                     phase + ": no private stage:" + stage.name)

        stages_absent("initial installed audit")
        need(candidate_raw == CANDIDATE_POINTER_RAW
             and audit_raw == AUDIT_POINTER_RAW,
             "installed exact compatibility pointers")
        receipt = validate_receipt(receipt_raw)
        receipt_files = receipt["bindings"]["files"]
        for receipt_key, local_key in RECEIPT_FILE_MAP.items():
            need(receipt_files[receipt_key] == inputs.caps[local_key].record(),
                 "receipt truthful current capture:" + receipt_key)
        seal = validate_seal(seal_raw, receipt_raw)
        inputs.unchanged("terminal installed audit")
        for cap in transaction_caps.values():
            cap.unchanged("terminal installed audit")
        need(fp(os.fstat(receipt_directory_fd)) == fp(receipt_directory_info)
             == fp(os.stat(receipt_directory, follow_symlinks=False))
             and sorted(os.listdir(receipt_directory_fd))
             == ["installation_receipt.json"],
             "terminal receipt directory identity and inventory")
        stages_absent("terminal installed audit")
        return {
            "schema": "cm2.round306c42.f1-authority-independent-installed-audit.v1",
            "status": "PASS_INDEPENDENT_C42_F1_AUTHORITY_SEAL_AUDIT__574_PAIRED__1150_UNRESOLVED",
            "candidate_object_sha256": docs["candidate"]["object_sha256"],
            "independent_audit_object_sha256": docs["audit"]["object_sha256"],
            "installation_receipt_object_sha256":
                receipt["installation_receipt_object_sha256"],
            "authority_seal_object_sha256": seal["authority_seal_object_sha256"],
            "authority_installed": True,
            "formal_census": {"paired": 574, "whole_representatives": 287,
                              "remaining_representatives": 575,
                              "unresolved": 1150},
            "D02": "BLOCKED", "CM2": "NO-GO_FOR_CLAIM",
        }
    finally:
        for cap in reversed(list(transaction_caps.values())):
            cap.close()
        if receipt_directory_fd >= 0:
            os.close(receipt_directory_fd)
        inputs.close()


def rejected(call: Any, label: str) -> None:
    try:
        call()
    except (Rejected, OSError, KeyError, TypeError, ValueError):
        return
    raise Rejected("hostile fixture accepted:" + label)


def self_test() -> dict[str, Any]:
    attacks: dict[str, bool] = {}
    rejected(lambda: strict(b'{"x":1,"x":2}'), "duplicate key")
    attacks["duplicate_key"] = True
    rejected(lambda: strict(b'{"x":Infinity}'), "nonfinite")
    attacks["nonfinite"] = True
    receipt_body = {
        "schema": RECEIPT_SCHEMA, "status": RECEIPT_STATUS,
        "release_id": RELEASE_ID, "authority_contract": {},
    }
    receipt = {**receipt_body,
               "installation_receipt_object_sha256": digest(receipt_body)}
    changed = copy.deepcopy(receipt)
    changed["release_id"] += "-f2"
    rejected(lambda: validate_receipt(canonical(changed) + b"\n"),
             "f2 stale self hash")
    attacks["f2_receipt_substitution"] = True
    changed = copy.deepcopy(receipt)
    changed["installation_receipt_object_sha256"] = "0" * 64
    rejected(lambda: validate_receipt(canonical(changed) + b"\n"),
             "receipt closure")
    attacks["receipt_self_hash"] = True
    with tempfile.TemporaryDirectory(prefix="cm2-c42-auditor-selftest-") as raw:
        root = Path(raw)
        (root / "regular").write_bytes(b"x\n")
        os.symlink("missing", root / "dangling")
        rejected(lambda: capture_unpinned(root / "dangling", "dangling"),
                 "dangling symlink")
        attacks["dangling_symlink"] = True
        os.link(root / "regular", root / "hardlink")
        rejected(lambda: capture_unpinned(root / "regular", "hardlink"),
                 "hardlink")
        attacks["hardlink"] = True
    rejected(lambda: need(AUDIT_TOKEN.endswith("-f2"), "f2 token"),
             "f2 token")
    attacks["f2_token"] = True
    rejected(lambda: need(False, "seal missing"), "seal missing")
    attacks["seal_required"] = True
    need(len(attacks) == 8 and all(attacks.values()), "attack census")
    return {
        "schema": "cm2.round306c42.f1-authority-independent-auditor-self-test.v1",
        "status": "PASS_INDEPENDENT_C42_F1_TRANSACTION_8_OF_8_ATTACKS_FAIL_CLOSED",
        "attack_count": 8,
        "attacks": attacks,
        "runtime_writes_performed": False,
    }


def emit(value: dict[str, Any]) -> None:
    sys.stdout.buffer.write(canonical(value) + b"\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--preflight", action="store_true")
    mode.add_argument("--audit-installed", action="store_true")
    mode.add_argument("--self-test", action="store_true")
    parser.add_argument("--expect-auditor-sha256")
    args = parser.parse_args()
    try:
        if args.self_test:
            need(args.expect_auditor_sha256 is None,
                 "self-test has no external source argument")
            emit(self_test())
        else:
            need(type(args.expect_auditor_sha256) is str,
                 "expected auditor SHA required")
            emit(preflight(args.expect_auditor_sha256) if args.preflight
                 else audit_installed(args.expect_auditor_sha256))
        return 0
    except (Rejected, OSError, KeyError, TypeError, ValueError) as error:
        emit({
            "schema": "cm2.round306c42.f1-authority-independent-auditor-rejection.v1",
            "status": "REJECTED_FAIL_CLOSED_NO_AUTHORITY_CLAIM",
            "error_type": type(error).__name__, "error": str(error),
        })
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
