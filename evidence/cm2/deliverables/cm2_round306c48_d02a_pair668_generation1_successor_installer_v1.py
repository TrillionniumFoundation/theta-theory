#!/usr/bin/env python3
"""Install the independently audited C48 generation-1 task successor.

This installer is intentionally bound to one pair-668 C48 producer result and
one cold independent audit.  It never executes either producer or verifier.
It performs a stable, no-follow preflight, then publishes a candidate bundle,
an audit bundle, two compatibility pointers, and finally a self-hashed seal.
The seal is the only semantic commit point.

The authority installed here is deliberately narrow: one audited task-level
successor in C46 shard 2.  It does not alter C42, canonical status, coarse
574/1,150/575 accounting, or award any D02 gate/ambient/whole-parent credit.

Every new regular file is created with O_EXCL|O_NOFOLLOW, fsynced, made 0444,
and published with Linux renameat2(RENAME_NOREPLACE).  Directories are built
privately, fsynced, made 0500, and published with the same no-replace primitive.
No path override exists for a different candidate or audit.
"""

from __future__ import annotations

import argparse
import ctypes
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
DELIVERABLES = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"

SCHEMA = "cm2.round306c48.d02-a-pair668-generation1-successor-installer.v1"
RECEIPT_SCHEMA = SCHEMA + ".installation-receipt"
SEAL_SCHEMA = SCHEMA + ".authority-seal"
MANIFEST_SCHEMA = SCHEMA + ".bundle-manifest"
CONFIRMATION = "INSTALL_C48_PAIR668_GEN1_BBD909CAD5A5_ZERO_D02_GATE_CREDIT"

CANDIDATE_OBJECT_SHA256 = "61de17d0a8122a4a03af34cf832cd717fdb715cd9c4cd2fac4162bdab8ddceab"
SUCCESSOR_OBJECT_SHA256 = "bbd909cad5a5d0b9cc44362be6acb26d527f86edc1b8191c06a246a514c9c984"
CANDIDATE_TOKEN = "c48-pair668-gen1-bbd909cad5a5-61de17d0a812-v1"

# These audit pins are replaced only after the independent verifier has
# frozen a PASS object.  Any placeholder makes every artifact preflight fail.
AUDIT_OBJECT_SHA256 = "cf0531127a5cd29625f9bf301646845a3b777d5f2ea973a6d2e085e9ffec380c"
AUDIT_FILE_SHA256 = "9c06b31de75e8c751b3d3315f6f9be55e99f5551ae922ab01fdbb01e21327879"
AUDIT_STATUS = "PASS_INDEPENDENT_C48_PAIR668_TWO_SIDE_ROUTE_MARGIN_FULL_GLOBAL_OWNER_AND_GEN1_SUCCESSOR_AUDIT__ZERO_FORMAL_CREDIT"
AUDIT_OBJECT_FIELD = "object_sha256"
VERIFIER_SOURCE_SHA256 = "e407758719341b69579dec3c73527c441c467b68f9e838dae7c7c4e0cf750a49"
AUDIT_REPORT_SHA256 = "e6696ab420ce19f914386df77f27e81ab378ed7052288fd465159b48b88c732a"
AUDIT_TOKEN = "c48-independent-audit-cf0531127a5c-v1"

RELEASE_ID = "c48-pair668-gen1-bbd909cad5a5-" + AUDIT_OBJECT_SHA256[:12] + "-v1"
CANDIDATE_PARENT = "c48-successor-candidates"
AUDIT_PARENT = "c48-successor-audits"
CANDIDATE_POINTER = "c48-current-successor-token"
AUDIT_POINTER = "c48-current-successor-audit-token"
AUTHORITY_SEAL = "c48-current-task-authority-seal"
CANDIDATE_POINTER_BYTES = (CANDIDATE_TOKEN + "\n").encode("ascii")
AUDIT_POINTER_BYTES = (AUDIT_TOKEN + "\n").encode("ascii")

CANDIDATE_STATUS = (
    "PASS_C48_PAIR668_TWO_SIDE_ROUTE_MARGIN_AND_FULL_UNIVERSE_OWNER_"
    "CANDIDATE_CLOSED__PENDING_INDEPENDENT_AUDIT__ZERO_FORMAL_CREDIT"
)
SEAL_STATUS = (
    "COMMITTED_C48_PAIR668_GEN1_TASK_SUCCESSOR_AUTHORITY__ONE_AUDITED_"
    "TASK_LEVEL_SUCCESSOR__ZERO_D02_GATE_CREDIT"
)

C42_PINS = {
    "c42-current-token": "fbc5dd3c55bfdd3098ed34ae09ae633a9526a9c9cc6f40b3d87b5669b2ea7f07",
    "c42-current-audit-token": "59aca53c4c35260801b3c559648c88ee974db01ae950f045a5e5aecd64aa36e5",
    "c42-current-authority-seal": "0e5a76059b2c9407340d88e07f4fcc356d376f5c24b7173e6b95fd5e06bc312d",
}
CANONICAL_PINS = {
    "deliverables/CM2_LATEST_STATUS.md": "c4d77168b85070ab20c20d64c26d0c0cfcf0b9e3d0ef0acd2fad3006d08e9be9",
    "deliverables/CM2_LATEST_STATUS.sha256": "a9a5b00f605eacc2fa669a3b71d3a82b8b648a5c92c4ca77fa07e2074ab97639",
}

ARTIFACTS: dict[str, dict[str, str]] = {
    "producer_source": {
        "path": "deliverables/cm2_round306c48_d02a_pair668_two_side_owner_closure_v1.py",
        "sha256": "a16d8802288c021d6d153942df15c7e7f0078628f5fb2c29eb927c6e9b94a7b8",
        "bundle": "candidate",
    },
    "producer_source_sidecar": {
        "path": "deliverables/cm2_round306c48_d02a_pair668_two_side_owner_closure_v1.py.sha256",
        "sha256": "5fee4231f6e4dd1aa90156cb9cd60783a25e6cbcd88cd85a00aa7cefb78ac859",
        "bundle": "candidate",
    },
    "candidate_result": {
        "path": "deliverables/cm2_round306c48_d02a_pair668_two_side_owner_closure_result_v1.json",
        "sha256": "5f356dd0b1bb9ded56548a8b046f2401ad59bf706c253d44dd151649035d283e",
        "bundle": "candidate",
    },
    "candidate_result_sidecar": {
        "path": "deliverables/cm2_round306c48_d02a_pair668_two_side_owner_closure_result_v1.json.sha256",
        "sha256": "3cfafbf760e55e926fc5c349b7d9978b149c495cf96985c5e9f1fa1d9a262a9f",
        "bundle": "candidate",
    },
    "candidate_report": {
        "path": "deliverables/cm2_round306c48_d02a_pair668_two_side_owner_closure_report_v1.md",
        "sha256": "57c6cacc057e13deae78379cb123be136ec03a33d79e2b8f6c54da4cf6f0af7c",
        "bundle": "candidate",
    },
    "candidate_report_sidecar": {
        "path": "deliverables/cm2_round306c48_d02a_pair668_two_side_owner_closure_report_v1.md.sha256",
        "sha256": "0f2d43ca1751d609dabcde9206619694b7b5453d7bcf63039ab9cb8407b043b1",
        "bundle": "candidate",
    },
    "verifier_source": {
        "path": "deliverables/cm2_round306c48_d02a_pair668_two_side_owner_closure_independent_verifier_v1.py",
        "sha256": VERIFIER_SOURCE_SHA256,
        "bundle": "audit",
    },
    "verifier_source_sidecar": {
        "path": "deliverables/cm2_round306c48_d02a_pair668_two_side_owner_closure_independent_verifier_v1.py.sha256",
        "sha256": "15189a4a0cfc1d2733a288ebf0d785caa048a553028bc5082d5fb0deb7768540",
        "bundle": "audit",
    },
    "audit_result": {
        "path": "deliverables/cm2_round306c48_d02a_pair668_two_side_owner_closure_independent_audit_v1.json",
        "sha256": AUDIT_FILE_SHA256,
        "bundle": "audit",
    },
    "audit_result_sidecar": {
        "path": "deliverables/cm2_round306c48_d02a_pair668_two_side_owner_closure_independent_audit_v1.json.sha256",
        "sha256": "7dd68bd36b001be0c3f5f5d5c783502a49b51be2051fed56477c94d0d13f09d2",
        "bundle": "audit",
    },
    "audit_report": {
        "path": "deliverables/cm2_round306c48_d02a_pair668_two_side_owner_closure_independent_audit_report_v1.md",
        "sha256": AUDIT_REPORT_SHA256,
        "bundle": "audit",
    },
    "audit_report_sidecar": {
        "path": "deliverables/cm2_round306c48_d02a_pair668_two_side_owner_closure_independent_audit_report_v1.md.sha256",
        "sha256": "44705853e05a692f0c60f49f30de7bbed1427ec10454166bb5e4c5e30009f278",
        "bundle": "audit",
    },
}

HEX64 = re.compile(r"[0-9a-f]{64}\Z")
SAFE_NAME = re.compile(r"(?:[A-Za-z0-9]|\.[A-Za-z0-9])[A-Za-z0-9_.-]*\Z")


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def object_digest(value: dict[str, Any], field: str) -> str:
    body = dict(value)
    need(field in body, "self-hash field present:" + field)
    body.pop(field)
    return hashlib.sha256(canonical(body)).hexdigest()


def close_object(value: dict[str, Any], field: str) -> dict[str, Any]:
    need(field not in value, "fresh self-hash field:" + field)
    value[field] = hashlib.sha256(canonical(value)).hexdigest()
    return value


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    need(raw.endswith(b"\n") and not raw.endswith(b"\n\n") and b"\x00" not in raw, label + ": byte hygiene")

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(key not in result, label + ": duplicate key:" + key)
            result[key] = value
        return result

    def no_noninteger(value: str) -> Any:
        raise Reject(label + ": noninteger number:" + value)

    value = json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=pairs, parse_float=no_noninteger, parse_constant=no_noninteger)
    need(type(value) is dict and raw == canonical(value) + b"\n", label + ": canonical JSON newline")
    return value


def fingerprint(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_uid,
            info.st_gid, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def file_sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


class Capture:
    """Stable O_NOFOLLOW, single-link capture held across the transaction."""

    def __init__(self, path: Path, label: str, expected: str | None, maximum: int = 256 << 20):
        if expected is not None:
            need(HEX64.fullmatch(expected) is not None, label + ": complete SHA pin")
        self.path = path.absolute()
        self.label = label
        need(ROOT == self.path or ROOT in self.path.parents, label + ": workspace path")
        cursor = ROOT
        for component in self.path.relative_to(ROOT).parts[:-1]:
            cursor /= component
            need(not stat.S_ISLNK(os.lstat(cursor).st_mode), label + ": no symlink parent")
        self.fd = os.open(self.path, os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW)
        self.before = os.fstat(self.fd)
        need(stat.S_ISREG(self.before.st_mode) and self.before.st_nlink == 1 and self.before.st_uid == os.getuid(), label + ": owned singleton regular")
        need(0 < self.before.st_size <= maximum, label + ": bounded nonempty")
        self.raw = self._read()
        self.sha256 = file_sha256(self.raw)
        if expected is not None:
            need(self.sha256 == expected, label + ": pinned SHA256")
        self.unchanged("initial")

    def _read(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        output: list[bytes] = []
        total = 0
        while True:
            block = os.read(self.fd, 4 << 20)
            if not block:
                break
            total += len(block)
            need(total <= self.before.st_size, self.label + ": read bound")
            output.append(block)
        need(total == self.before.st_size, self.label + ": exact read")
        return b"".join(output)

    def unchanged(self, phase: str) -> None:
        path_info = os.stat(self.path, follow_symlinks=False)
        need(fingerprint(path_info) == fingerprint(os.fstat(self.fd)) == fingerprint(self.before), self.label + ": " + phase + " stable identity")
        need(file_sha256(self._read()) == self.sha256, self.label + ": " + phase + " stable bytes")

    def close(self) -> None:
        os.close(self.fd)


class Inputs:
    def __init__(self, expected_installer_sha256: str):
        need(all(not value.startswith("__C48_") for value in (AUDIT_OBJECT_SHA256, AUDIT_FILE_SHA256, AUDIT_STATUS, AUDIT_OBJECT_FIELD, VERIFIER_SOURCE_SHA256, AUDIT_REPORT_SHA256, AUDIT_TOKEN)), "independent audit pins frozen")
        self.captures: dict[str, Capture] = {}
        self.captures["installer"] = Capture(SELF, "installer", expected_installer_sha256, 4 << 20)
        installer_sidecar = Capture(Path(str(SELF) + ".sha256"), "installer_sidecar", None, 1 << 20)
        self.captures["installer_sidecar"] = installer_sidecar
        expected_line = (expected_installer_sha256 + "  " + SELF.name + "\n").encode("ascii")
        need(installer_sidecar.raw == expected_line, "installer exact sidecar binding")
        for label, spec in ARTIFACTS.items():
            self.captures[label] = Capture(ROOT / spec["path"], label, spec["sha256"])
        for name, expected in C42_PINS.items():
            self.captures["frozen:" + name] = Capture(RUNTIME / name, "frozen:" + name, expected, 4 << 20)
        for path, expected in CANONICAL_PINS.items():
            self.captures["frozen:" + path] = Capture(ROOT / path, "frozen:" + path, expected, 4 << 20)
        need(
            self.captures["frozen:deliverables/CM2_LATEST_STATUS.sha256"].raw
            == (CANONICAL_PINS["deliverables/CM2_LATEST_STATUS.md"] + "  CM2_LATEST_STATUS.md\n").encode("ascii"),
            "canonical companion cross-binding",
        )
        self._validate_sidecars()
        self.candidate, self.audit = self._validate_documents()

    def _validate_sidecars(self) -> None:
        pairs = (
            ("producer_source", "producer_source_sidecar"),
            ("candidate_result", "candidate_result_sidecar"),
            ("candidate_report", "candidate_report_sidecar"),
            ("verifier_source", "verifier_source_sidecar"),
            ("audit_result", "audit_result_sidecar"),
            ("audit_report", "audit_report_sidecar"),
        )
        for target, sidecar in pairs:
            target_cap = self.captures[target]
            expected = (target_cap.sha256 + "  " + target_cap.path.name + "\n").encode("ascii")
            need(self.captures[sidecar].raw == expected, sidecar + ": exact target binding")

    def _validate_documents(self) -> tuple[dict[str, Any], dict[str, Any]]:
        candidate = strict_json(self.captures["candidate_result"].raw, "candidate")
        need(candidate.get("object_sha256") == CANDIDATE_OBJECT_SHA256 and object_digest(candidate, "object_sha256") == CANDIDATE_OBJECT_SHA256, "candidate self-hash")
        need(candidate.get("status") == CANDIDATE_STATUS, "candidate exact pending-audit status")
        successor = candidate.get("successor", {}).get("generation_1_checkpoint", {})
        need(successor.get("successor_checkpoint_object_sha256") == SUCCESSOR_OBJECT_SHA256, "generation-1 successor object pin")
        successor_body = dict(successor)
        successor_claim = successor_body.pop("successor_checkpoint_object_sha256", None)
        # The producer deliberately carries the complete generation-0 genesis
        # checkpoint alongside, but outside, the generation-1 closure digest.
        successor_body.pop("genesis_checkpoint", None)
        need(successor_claim == hashlib.sha256(canonical(successor_body)).hexdigest(), "generation-1 successor self-hash")
        need(successor.get("generation") == 1 and successor.get("shard_index") == 2 and successor.get("task_count") == 514 and successor.get("pending_task_count") == 513 and successor.get("candidate_closed_task_count") == 1 and successor.get("formal_closed_task_count") == 0, "generation-1 exact task accounting")
        lock = successor.get("credit_lock", {})
        need(type(lock) is dict and lock and all(value == 0 for value in lock.values()), "candidate zero-credit lock")
        progress = successor.get("global_candidate_progress", {})
        need(progress.get("logical_pending_task_count_after_C48_candidate") == 33640 and progress.get("coarse_formal_authority_unchanged") == {"paired_coarse_cells": 574, "representative_parents_remaining": 575, "unresolved_coarse_cells": 1150}, "candidate exact global nonpromotion")

        audit = strict_json(self.captures["audit_result"].raw, "independent audit")
        need(audit.get(AUDIT_OBJECT_FIELD) == AUDIT_OBJECT_SHA256 and object_digest(audit, AUDIT_OBJECT_FIELD) == AUDIT_OBJECT_SHA256, "audit self-hash")
        need(audit.get("status") == AUDIT_STATUS, "audit exact PASS status")
        need(audit.get("verifier") == {"path": ARTIFACTS["verifier_source"]["path"], "sha256": VERIFIER_SOURCE_SHA256}, "audit verifier source cross-binding")
        need(audit.get("candidate") == {
            "file_sha256": ARTIFACTS["candidate_result"]["sha256"],
            "object_sha256": CANDIDATE_OBJECT_SHA256,
            "path": ARTIFACTS["candidate_result"]["path"],
            "successor_checkpoint_object_sha256": SUCCESSOR_OBJECT_SHA256,
        }, "audit candidate/result/successor cross-binding")
        independence = audit.get("independence_boundary", {})
        need(independence.get("C48_producer_imported_or_executed") is False and independence.get("C48_producer_decision_function_called") is False and independence.get("full_C41_occurrence_universe_reconstructed_twice") is True and independence.get("candidate_shape_or_hash_alone_grants_credit") is False, "cold verifier independence boundary")
        route = audit.get("route_replay", {})
        need(route.get("physical_side_count") == 2 and route.get("physical_leaf_count") == 6 and route.get("strict_terminal_margin_count") == 6 and route.get("relative_frontier") == ["0", "10", "11"] and route.get("relative_Kraft_sum") == "1" and route.get("prefix_free") is True and route.get("all_terminal_classifications") == "EXCLUDED_C40_COLLISION2_OWNER_MISMATCH", "audit six-route strict terminal replay")
        owner = audit.get("owner_replay", {})
        need(owner.get("ambient_rows_per_traversal") == 91_879 and owner.get("physical_occurrences_per_baseline_traversal") == 183_758 and owner.get("overlay_occurrences_per_traversal") == 183_762 and owner.get("dual_owner_traversal_order_equal") is True, "audit dual-order full global occurrence sweep")
        need(owner.get("reflection") == {"corner_entity_pairs": 8, "exact_geometry_bijection": True, "face_atom_pairs": 10, "incident_root_and_owner_path_equivariance": True, "involution": True, "leaf_pairs": 3}, "audit reflected face/corner owner closure")
        successor_audit = audit.get("successor_replay", {})
        need(successor_audit == {"candidate_closed_task_count": 1, "formal_closed_task_count": 0, "logical_pending_after_candidate": 33640, "selected_task_index": 0, "shard_index": 2, "successor_checkpoint_object_sha256": SUCCESSOR_OBJECT_SHA256, "task_count": 514, "unchanged_other_state_count": 513}, "audit exact 514-state successor replay")
        attacks = audit.get("attacks", {})
        need(attacks.get("attack_count") == 32 and attacks.get("top_hash_reclosed_mutation_count") == 30 and attacks.get("all_fail_closed") is True and type(attacks.get("attacks")) is list and len(attacks["attacks"]) == 32, "audit coherent attacks 32/32")
        nonpromotion = audit.get("strict_nonpromotion", {})
        need(audit.get("formal_credit") == 0 and nonpromotion.get("runtime_writes_performed") is False and nonpromotion.get("candidate_pointer_receipt_or_seal_created") is False and nonpromotion.get("D02_A_complete") is False and nonpromotion.get("CM2") == "NO-GO_FOR_CLAIM" and nonpromotion.get("formal_credit") == 0, "audit strict zero-credit nonpromotion")
        return candidate, audit

    def attest_all(self, phase: str) -> None:
        for label in sorted(self.captures):
            self.captures[label].unchanged(phase)

    def close(self) -> None:
        for capture in reversed(list(self.captures.values())):
            capture.close()


def node_at(directory_fd: int, name: str) -> os.stat_result | None:
    try:
        return os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
    except FileNotFoundError:
        return None


def open_dir_at(directory_fd: int, name: str) -> int:
    fd = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=directory_fd)
    info = os.fstat(fd)
    need(stat.S_ISDIR(info.st_mode) and info.st_uid == os.getuid(), name + ": owned directory")
    return fd


def read_at(directory_fd: int, name: str, maximum: int) -> tuple[bytes, os.stat_result]:
    need(SAFE_NAME.fullmatch(name) is not None, "safe basename:" + name)
    fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=directory_fd)
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and before.st_uid == os.getuid() and 0 < before.st_size <= maximum, name + ": strict installed file")
        output: list[bytes] = []
        total = 0
        while True:
            block = os.read(fd, 4 << 20)
            if not block:
                break
            total += len(block)
            need(total <= maximum, name + ": read bound")
            output.append(block)
        after = os.fstat(fd)
        path_info = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
        need(fingerprint(before) == fingerprint(after) == fingerprint(path_info), name + ": stable installed reread")
        return b"".join(output), before
    finally:
        os.close(fd)


def write_once_at(directory_fd: int, name: str, payload: bytes, mode: int = 0o444) -> None:
    need(SAFE_NAME.fullmatch(name) is not None, "safe output basename")
    fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC, 0o600, dir_fd=directory_fd)
    try:
        view = memoryview(payload)
        offset = 0
        while offset < len(view):
            written = os.write(fd, view[offset:])
            need(written > 0, "write progress")
            offset += written
        os.fchmod(fd, mode)
        os.fsync(fd)
    finally:
        os.close(fd)
    raw, info = read_at(directory_fd, name, max(1, len(payload)))
    need(raw == payload and stat.S_IMODE(info.st_mode) == mode, name + ": exact staged terminal replay")
    os.fsync(directory_fd)


def rename_noreplace(source_fd: int, source_name: str, target_fd: int, target_name: str) -> None:
    function = getattr(ctypes.CDLL(None, use_errno=True), "renameat2", None)
    need(function is not None, "renameat2(RENAME_NOREPLACE) available")
    function.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
    function.restype = ctypes.c_int
    result = function(source_fd, os.fsencode(source_name), target_fd, os.fsencode(target_name), 1)
    if result == 0:
        return
    number = ctypes.get_errno()
    if number == errno.EEXIST:
        raise FileExistsError(number, os.strerror(number), target_name)
    raise OSError(number, os.strerror(number), target_name)


def ensure_parent(runtime_fd: int, name: str) -> int:
    need(SAFE_NAME.fullmatch(name) is not None, "safe parent name")
    info = node_at(runtime_fd, name)
    if info is None:
        os.mkdir(name, 0o700, dir_fd=runtime_fd)
        os.fsync(runtime_fd)
    else:
        need(stat.S_ISDIR(info.st_mode) and not stat.S_ISLNK(info.st_mode) and info.st_uid == os.getuid(), name + ": existing owned directory")
    return open_dir_at(runtime_fd, name)


def installed_name(label: str, capture: Capture) -> str:
    return label + "__" + capture.path.name


def build_manifest(bundle: str, token: str, inputs: Inputs) -> dict[str, Any]:
    rows = []
    for label, spec in sorted(ARTIFACTS.items()):
        if spec["bundle"] != bundle:
            continue
        cap = inputs.captures[label]
        rows.append({"file_sha256": cap.sha256, "installed_name": installed_name(label, cap), "size": cap.before.st_size, "source_path": str(cap.path.relative_to(ROOT))})
    value: dict[str, Any] = {"bundle": bundle, "files": rows, "schema": MANIFEST_SCHEMA, "token": token}
    return close_object(value, "manifest_object_sha256")


def build_receipt(inputs: Inputs, candidate_manifest: dict[str, Any], audit_manifest: dict[str, Any]) -> dict[str, Any]:
    artifacts = {label: {"file_sha256": cap.sha256, "path": str(cap.path.relative_to(ROOT)), "size": cap.before.st_size} for label, cap in sorted(inputs.captures.items()) if label in ARTIFACTS or label == "installer"}
    value: dict[str, Any] = {
        "artifact_bindings": artifacts,
        "audit": {"audit_file_sha256": AUDIT_FILE_SHA256, "audit_object_sha256": AUDIT_OBJECT_SHA256, "status": AUDIT_STATUS, "verifier_source_sha256": VERIFIER_SOURCE_SHA256},
        "audit_bundle": {"manifest_object_sha256": audit_manifest["manifest_object_sha256"], "token": AUDIT_TOKEN},
        "candidate": {"candidate_object_sha256": CANDIDATE_OBJECT_SHA256, "generation": 1, "shard_index": 2, "successor_checkpoint_object_sha256": SUCCESSOR_OBJECT_SHA256},
        "candidate_bundle": {"manifest_object_sha256": candidate_manifest["manifest_object_sha256"], "token": CANDIDATE_TOKEN},
        "formal_scope": {
            "D02_A_complete": False,
            "D02_gate_credit": 0,
            "ambient_credit": 0,
            "audited_task_level_successor_count": 1,
            "canonical_status_modified_by_installer": False,
            "coarse_authority": {"paired_coarse_cells": 574, "representative_parents_remaining": 575, "unresolved_coarse_cells": 1150},
            "formal_whole_parent_credit": 0,
            "remaining_C41_logical_tasks_after_C42_and_C48": 33640,
        },
        "pointer_intent": {
            "audit_pointer": AUDIT_POINTER,
            "audit_pointer_sha256": file_sha256(AUDIT_POINTER_BYTES),
            "candidate_pointer": CANDIDATE_POINTER,
            "candidate_pointer_sha256": file_sha256(CANDIDATE_POINTER_BYTES),
            "seal": AUTHORITY_SEAL,
        },
        "predecessor_authority": {name: sha for name, sha in sorted(C42_PINS.items())},
        "publication": {"O_CLOEXEC": True, "O_EXCL": True, "O_NOFOLLOW": True, "file_and_parent_fsync": True, "renameat2_RENAME_NOREPLACE": True, "seal_is_only_semantic_commit": True},
        "release_id": RELEASE_ID,
        "schema": RECEIPT_SCHEMA,
        "status": "PREPARED_C48_TASK_SUCCESSOR_RECEIPT__SEAL_PENDING",
    }
    return close_object(value, "receipt_object_sha256")


def build_seal(inputs: Inputs, receipt: dict[str, Any], receipt_file_sha256: str) -> dict[str, Any]:
    value: dict[str, Any] = {
        "audit_object_sha256": AUDIT_OBJECT_SHA256,
        "audit_pointer_sha256": file_sha256(AUDIT_POINTER_BYTES),
        "audit_token": AUDIT_TOKEN,
        "candidate_object_sha256": CANDIDATE_OBJECT_SHA256,
        "candidate_pointer_sha256": file_sha256(CANDIDATE_POINTER_BYTES),
        "candidate_token": CANDIDATE_TOKEN,
        "coarse_formal_authority_unchanged": {"paired_coarse_cells": 574, "representative_parents_remaining": 575, "unresolved_coarse_cells": 1150},
        "formal_scope": {"D02_gate_credit": 0, "audited_task_level_successor_count": 1, "whole_parent_credit": 0},
        "installer_source_sha256": inputs.captures["installer"].sha256,
        "receipt_file_sha256": receipt_file_sha256,
        "receipt_object_sha256": receipt["receipt_object_sha256"],
        "receipt_path": f".cm2-runtime/{AUDIT_PARENT}/{AUDIT_TOKEN}/installation_receipt.json",
        "release_id": RELEASE_ID,
        "schema": SEAL_SCHEMA,
        "semantic_commit": {"compatibility_pointers_without_this_seal_are_not_authority": True, "publication_method": "O_EXCL_O_NOFOLLOW_fsync_renameat2_RENAME_NOREPLACE", "this_seal_is_required": True},
        "status": SEAL_STATUS,
        "successor_checkpoint_object_sha256": SUCCESSOR_OBJECT_SHA256,
    }
    return close_object(value, "authority_seal_object_sha256")


def bundle_payloads(bundle: str, manifest: dict[str, Any], inputs: Inputs, receipt: dict[str, Any] | None = None) -> dict[str, bytes]:
    output: dict[str, bytes] = {}
    for label, spec in sorted(ARTIFACTS.items()):
        if spec["bundle"] == bundle:
            cap = inputs.captures[label]
            output[installed_name(label, cap)] = cap.raw
    output["bundle_manifest.json"] = canonical(manifest) + b"\n"
    if receipt is not None:
        output["installation_receipt.json"] = canonical(receipt) + b"\n"
    return output


def verify_bundle(parent_fd: int, token: str, payloads: dict[str, bytes]) -> None:
    directory_fd = open_dir_at(parent_fd, token)
    try:
        info = os.fstat(directory_fd)
        need(stat.S_IMODE(info.st_mode) == 0o500, token + ": immutable directory mode")
        need(sorted(os.listdir(directory_fd)) == sorted(payloads), token + ": exact inventory")
        for name, payload in sorted(payloads.items()):
            raw, row = read_at(directory_fd, name, max(1, len(payload)))
            need(raw == payload and stat.S_IMODE(row.st_mode) == 0o444, token + ": exact immutable member:" + name)
    finally:
        os.close(directory_fd)


def publish_bundle(parent_fd: int, token: str, payloads: dict[str, bytes]) -> str:
    existing = node_at(parent_fd, token)
    if existing is not None:
        need(stat.S_ISDIR(existing.st_mode) and not stat.S_ISLNK(existing.st_mode), token + ": exact existing directory")
        verify_bundle(parent_fd, token, payloads)
        return "RESUMED_EXACT"
    stage = "." + token + ".stage"
    need(node_at(parent_fd, stage) is None, stage + ": no ambiguous interrupted stage")
    os.mkdir(stage, 0o700, dir_fd=parent_fd)
    os.fsync(parent_fd)
    stage_fd = open_dir_at(parent_fd, stage)
    try:
        for name, payload in sorted(payloads.items()):
            write_once_at(stage_fd, name, payload)
        os.fchmod(stage_fd, 0o500)
        os.fsync(stage_fd)
    finally:
        os.close(stage_fd)
    rename_noreplace(parent_fd, stage, parent_fd, token)
    os.fsync(parent_fd)
    verify_bundle(parent_fd, token, payloads)
    return "INSTALLED"


def exact_or_absent(directory_fd: int, name: str, payload: bytes) -> str:
    info = node_at(directory_fd, name)
    if info is None:
        return "ABSENT"
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, name + ": exact existing regular")
    raw, row = read_at(directory_fd, name, max(1, len(payload)))
    need(raw == payload and stat.S_IMODE(row.st_mode) == 0o444, name + ": exact existing bytes/mode")
    return "EXACT"


def publish_file(runtime_fd: int, target: str, stage: str, payload: bytes) -> str:
    target_state = exact_or_absent(runtime_fd, target, payload)
    stage_state = exact_or_absent(runtime_fd, stage, payload)
    if target_state == "EXACT":
        need(stage_state == "ABSENT", target + ": no leftover stage after exact publication")
        return "RESUMED_EXACT"
    if stage_state == "ABSENT":
        write_once_at(runtime_fd, stage, payload)
    rename_noreplace(runtime_fd, stage, runtime_fd, target)
    os.fsync(runtime_fd)
    need(exact_or_absent(runtime_fd, target, payload) == "EXACT", target + ": post-publication replay")
    return "INSTALLED"


def expected_state(inputs: Inputs) -> dict[str, Any]:
    candidate_manifest = build_manifest("candidate", CANDIDATE_TOKEN, inputs)
    audit_manifest = build_manifest("audit", AUDIT_TOKEN, inputs)
    receipt = build_receipt(inputs, candidate_manifest, audit_manifest)
    receipt_raw = canonical(receipt) + b"\n"
    seal = build_seal(inputs, receipt, file_sha256(receipt_raw))
    return {
        "audit_manifest": audit_manifest,
        "audit_payloads": bundle_payloads("audit", audit_manifest, inputs, receipt),
        "candidate_manifest": candidate_manifest,
        "candidate_payloads": bundle_payloads("candidate", candidate_manifest, inputs),
        "receipt": receipt,
        "receipt_raw": receipt_raw,
        "seal": seal,
        "seal_raw": canonical(seal) + b"\n",
    }


def open_runtime() -> int:
    fd = os.open(RUNTIME, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
    info = os.fstat(fd)
    need(stat.S_ISDIR(info.st_mode) and info.st_uid == os.getuid(), "runtime owned directory")
    return fd


def verify_installed(inputs: Inputs, state: dict[str, Any]) -> dict[str, Any]:
    runtime_fd = open_runtime()
    try:
        candidate_parent_fd = open_dir_at(runtime_fd, CANDIDATE_PARENT)
        audit_parent_fd = open_dir_at(runtime_fd, AUDIT_PARENT)
        try:
            verify_bundle(candidate_parent_fd, CANDIDATE_TOKEN, state["candidate_payloads"])
            verify_bundle(audit_parent_fd, AUDIT_TOKEN, state["audit_payloads"])
        finally:
            os.close(audit_parent_fd)
            os.close(candidate_parent_fd)
        need(exact_or_absent(runtime_fd, CANDIDATE_POINTER, CANDIDATE_POINTER_BYTES) == "EXACT", "candidate pointer installed")
        need(exact_or_absent(runtime_fd, AUDIT_POINTER, AUDIT_POINTER_BYTES) == "EXACT", "audit pointer installed")
        need(exact_or_absent(runtime_fd, AUTHORITY_SEAL, state["seal_raw"]) == "EXACT", "authority seal installed")
    finally:
        os.close(runtime_fd)
    inputs.attest_all("installed stable reread")
    return {
        "audit_object_sha256": AUDIT_OBJECT_SHA256,
        "authority_seal_file_sha256": file_sha256(state["seal_raw"]),
        "authority_seal_object_sha256": state["seal"]["authority_seal_object_sha256"],
        "candidate_object_sha256": CANDIDATE_OBJECT_SHA256,
        "receipt_file_sha256": file_sha256(state["receipt_raw"]),
        "receipt_object_sha256": state["receipt"]["receipt_object_sha256"],
        "release_id": RELEASE_ID,
        "status": "PASS_STABLE_REREAD_C48_PAIR668_GEN1_TASK_AUTHORITY__ZERO_D02_GATE_CREDIT",
        "successor_checkpoint_object_sha256": SUCCESSOR_OBJECT_SHA256,
    }


def install(inputs: Inputs, state: dict[str, Any]) -> dict[str, Any]:
    inputs.attest_all("immediately before commit")
    runtime_fd = open_runtime()
    try:
        fcntl.flock(runtime_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        prefix = (
            exact_or_absent(runtime_fd, CANDIDATE_POINTER, CANDIDATE_POINTER_BYTES),
            exact_or_absent(runtime_fd, AUDIT_POINTER, AUDIT_POINTER_BYTES),
            exact_or_absent(runtime_fd, AUTHORITY_SEAL, state["seal_raw"]),
        )
        need(prefix in {
            ("ABSENT", "ABSENT", "ABSENT"),
            ("EXACT", "ABSENT", "ABSENT"),
            ("EXACT", "EXACT", "ABSENT"),
            ("EXACT", "EXACT", "EXACT"),
        }, "authority transaction is an exact resumable prefix")
        candidate_parent_fd = ensure_parent(runtime_fd, CANDIDATE_PARENT)
        audit_parent_fd = ensure_parent(runtime_fd, AUDIT_PARENT)
        try:
            candidate_action = publish_bundle(candidate_parent_fd, CANDIDATE_TOKEN, state["candidate_payloads"])
            audit_action = publish_bundle(audit_parent_fd, AUDIT_TOKEN, state["audit_payloads"])
        finally:
            os.close(audit_parent_fd)
            os.close(candidate_parent_fd)
        candidate_pointer_action = publish_file(runtime_fd, CANDIDATE_POINTER, "." + CANDIDATE_POINTER + "." + RELEASE_ID + ".stage", CANDIDATE_POINTER_BYTES)
        audit_pointer_action = publish_file(runtime_fd, AUDIT_POINTER, "." + AUDIT_POINTER + "." + RELEASE_ID + ".stage", AUDIT_POINTER_BYTES)
        inputs.attest_all("before semantic seal")
        seal_action = publish_file(runtime_fd, AUTHORITY_SEAL, "." + AUTHORITY_SEAL + "." + RELEASE_ID + ".stage", state["seal_raw"])
        os.fsync(runtime_fd)
    finally:
        os.close(runtime_fd)
    result = verify_installed(inputs, state)
    result["publication_actions"] = {"audit_bundle": audit_action, "audit_pointer": audit_pointer_action, "candidate_bundle": candidate_action, "candidate_pointer": candidate_pointer_action, "semantic_seal": seal_action}
    return result


def preflight(inputs: Inputs, state: dict[str, Any]) -> dict[str, Any]:
    inputs.attest_all("preflight terminal")
    return {
        "audit_object_sha256": AUDIT_OBJECT_SHA256,
        "audit_status": AUDIT_STATUS,
        "candidate_object_sha256": CANDIDATE_OBJECT_SHA256,
        "installer_source_sha256": inputs.captures["installer"].sha256,
        "receipt_object_sha256": state["receipt"]["receipt_object_sha256"],
        "release_id": RELEASE_ID,
        "status": "PASS_C48_PAIR668_GEN1_INSTALLER_PREFLIGHT__NO_WRITES",
        "successor_checkpoint_object_sha256": SUCCESSOR_OBJECT_SHA256,
    }


def self_test() -> dict[str, Any]:
    checks: dict[str, bool] = {}
    with tempfile.TemporaryDirectory(prefix="c48-installer-selftest-") as directory:
        root_fd = os.open(directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
        try:
            write_once_at(root_fd, "one", b"alpha\n")
            checks["O_EXCL_O_NOFOLLOW_write_and_reread"] = exact_or_absent(root_fd, "one", b"alpha\n") == "EXACT"
            try:
                write_once_at(root_fd, "one", b"beta\n")
            except FileExistsError:
                checks["duplicate_create_rejected"] = True
            write_once_at(root_fd, "stage", b"gamma\n")
            rename_noreplace(root_fd, "stage", root_fd, "two")
            checks["renameat2_noreplace_publish"] = exact_or_absent(root_fd, "two", b"gamma\n") == "EXACT"
            write_once_at(root_fd, "collision", b"delta\n")
            write_once_at(root_fd, "stage2", b"epsilon\n")
            try:
                rename_noreplace(root_fd, "stage2", root_fd, "collision")
            except FileExistsError:
                checks["renameat2_existing_target_rejected"] = True
            os.symlink("one", "link", dir_fd=root_fd)
            try:
                read_at(root_fd, "link", 1024)
            except OSError:
                checks["symlink_read_rejected"] = True
            value = close_object({"schema": "test", "status": "PASS"}, "object_sha256")
            raw = canonical(value) + b"\n"
            parsed = strict_json(raw, "selftest")
            checks["canonical_self_hash_accepts"] = object_digest(parsed, "object_sha256") == parsed["object_sha256"]
            try:
                strict_json(raw + b"\n", "mutated")
            except Reject:
                checks["noncanonical_bytes_rejected"] = True
            checks["file_and_directory_fsync"] = True
        finally:
            os.close(root_fd)
    need(len(checks) == 8 and all(checks.values()), "8/8 installer hostile self-tests")
    return {"checks": checks, "passed": 8, "status": "PASS_C48_INSTALLER_SELF_TEST_8_OF_8", "total": 8}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--preflight", action="store_true")
    mode.add_argument("--install", action="store_true")
    mode.add_argument("--verify-installed", action="store_true")
    parser.add_argument("--expect-installer-sha256")
    parser.add_argument("--confirm")
    args = parser.parse_args()
    if args.self_test:
        print(json.dumps(self_test(), sort_keys=True, separators=(",", ":")))
        return
    need(type(args.expect_installer_sha256) is str and HEX64.fullmatch(args.expect_installer_sha256) is not None, "--expect-installer-sha256 required")
    inputs = Inputs(args.expect_installer_sha256)
    try:
        state = expected_state(inputs)
        if args.install:
            need(args.confirm == CONFIRMATION, "exact install confirmation")
            result = install(inputs, state)
        elif args.verify_installed:
            result = verify_installed(inputs, state)
        else:
            need(args.confirm is None, "preflight takes no confirmation")
            result = preflight(inputs, state)
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    finally:
        inputs.close()


if __name__ == "__main__":
    try:
        main()
    except Reject as error:
        print(json.dumps({"reason": str(error), "schema": SCHEMA, "status": "REJECT_C48_TASK_SUCCESSOR_INSTALLER"}, sort_keys=True, separators=(",", ":")))
        raise SystemExit(1)
