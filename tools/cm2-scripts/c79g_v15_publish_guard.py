#!/usr/bin/env python3
"""Fail-closed one-shot publisher for the final C79g v15 cold bundle.

``PREFLIGHT`` is strictly read-only.  It acquires the official writer lock,
holds the workspace root, deliverables directory, runtime directory, and the
ordered exact8, and mechanically reconstructs the exact manifest and outer
receipt that the v15 launcher validates.

``PUBLISH`` is authorized only by the complete ordered exact8 pre-hash vector
and all three expected publication hashes on the command line.  The source
one-shot flag remains false and is reported as such; it is not a second hidden
write switch.  Under one uninterrupted official lock plus an O_EXCL transaction
claim it freezes the seven writable v15 members (the v14 supersession receipt is
already frozen), creates the manifest
with O_EXCL, creates the outer receipt last with O_EXCL, fsyncs every file and
directory boundary, and terminally replays the held exact10.

This tool never imports or executes a C79g protocol source.  It performs JSON
and AST inspection only and deliberately has no delete, overwrite, rename, or
runtime command.
"""

from __future__ import annotations

import ast
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
from typing import Any, Iterable


sys.dont_write_bytecode = True


# Audit-visible source state.  It intentionally remains false: the sole write
# authority is the full, exact CLI prehash/publication-hash contract.
ONE_SHOT_PUBLISH_ENABLED = False

CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"

PREDECESSOR_SUPERSESSION = (
    f"deliverables/{BASE}_v14_runtime_registry_shape_drift_rejection_"
    "supersession_receipt_v1.json",
    "aa4323027e2313f8a2eda0d6ffc039a537afe342d496d1f75cd73fcd47446c01",
    "93689e62ae36f405f045a769f4dc6f6e6fd83a16605d08299d5c3397ad657e2e",
)
SCHEMA_V15 = (
    f"deliverables/{BASE}_schema_v15.json",
    "ab120abd2d77667388c94e5af00637f843e7af1b48adba95306e1a7ea79e73bd",
    None,
)
CONTRACT_V15 = (
    f"deliverables/{BASE}_contract_v15.json",
    "292ad598033ff2f89c1d6c502e4e6077df9559688a5885088ad107fa45a7dabf",
    "9a2ba48cbcb200ff95bf1ca593cd8030ba6bac2b1b8fdc84301d3eb72605bd0e",
)
PRODUCER_V15 = (
    f"deliverables/{BASE}_v15.py",
    "7b3621bf6579cd9cc9289ed2bda353cbe5f2e32b108ec718bf80a4fd19af125b",
    None,
)
CONSUMER_V15 = (
    f"deliverables/{BASE}_independent_verifier_assembler_authority_consumer_v15.py",
    "5f988490d014a1427a773b7c5fda03318ec67ad9716a4a75b4008b007e944541",
    None,
)
TRANSITION_V15 = (
    f"deliverables/{BASE}_v14_to_v15_static_launch_transition_receipt_v1.json",
    "74c82c804993a6b00196ba5c0b78a3c5067d3242452d61044229f3f04eaf4a7a",
    "3ead78915247f1a43eaa301d2ebd77d05f790f36530c59deeba677d747bae431",
)
AUDIT_V15 = (
    f"deliverables/{BASE}_static_audit_v15.json",
    "69557bc7971a6c9943a5d4cee36895bc47413d9b45d92c56597d5cde83b3ed06",
    "b00c87033d9ca880901bac9853709bd60644cc39bc24bc3ec4a05216fba82158",
)
LAUNCHER_V15 = (
    f"deliverables/{BASE}_cold_launch_v15.py",
    "c0277dbd809b1414075292fc8bb6d366076663ebfae37270fa156126320a288f",
    None,
)

EXACT8 = (
    PREDECESSOR_SUPERSESSION,
    SCHEMA_V15,
    CONTRACT_V15,
    PRODUCER_V15,
    CONSUMER_V15,
    TRANSITION_V15,
    AUDIT_V15,
    LAUNCHER_V15,
)
MANIFEST_REL = f"deliverables/{BASE}_cold_launch_manifest_v15.sha256"
OUTER_REL = f"deliverables/{BASE}_cold_launch_outer_receipt_v15.json"

EXPECTED_MANIFEST_FILE_SHA256 = (
    "850c8c9e4ce9878049c23bd526cb2c09a15d777e1f0db3462d41098d2645ae34")
EXPECTED_OUTER_FILE_SHA256 = (
    "b928e776404f9156c04ad12a897b90400448115b76b755f4b249b27595a375df")
EXPECTED_OUTER_OBJECT_SHA256 = (
    "61b1f26cda04811a39a8cdb7eb1bd94a14c7f063016ac64063a8855ba68a0be4")

TRANSACTION_CLAIM_NAME = ".c79g-v15-publish-guard.transaction-claim-v1"
TRANSACTION_CLAIM_RAW = b"CM2_C79G_V15_PUBLISH_TRANSACTION_CLAIM_V1\n"

V15_RUNTIME_SURFACES = (
    f".cm2-runtime/c79g-v15-candidate-a-{CHECKPOINT}",
    f".cm2-runtime/c79g-v15-candidate-b-{CHECKPOINT}",
    f".cm2-runtime/c79g-v15-verification-a-{CHECKPOINT}",
    f".cm2-runtime/c79g-v15-verification-b-{CHECKPOINT}",
    f".cm2-runtime/c79g-v15-committed-completion-{CHECKPOINT}",
    f".cm2-runtime/cm2-global-authority-heads/c79g-v15-{CHECKPOINT}.seal",
    f".cm2-runtime/.c79g-v15-candidate-stage-a-{CHECKPOINT}",
    f".cm2-runtime/.c79g-v15-candidate-stage-b-{CHECKPOINT}",
    f".cm2-runtime/.c79g-v15-verification-stage-a-{CHECKPOINT}",
    f".cm2-runtime/.c79g-v15-verification-stage-b-{CHECKPOINT}",
    f".cm2-runtime/.c79g-v15-completion-stage-{CHECKPOINT}",
    f".cm2-runtime/cm2-global-authority-heads/.c79g-v15-authority-stage-"
    f"{CHECKPOINT}.seal",
    f".cm2-runtime/c79g-v15-rejections-{CHECKPOINT}",
)

HEX64 = re.compile(r"[0-9a-f]{64}")
AT_EMPTY_PATH = 0x1000
AT_SYMLINK_NOFOLLOW = 0x100
STATX_BASIC_STATS = 0x000007FF
STATX_MNT_ID = 0x00001000
RESOLVE_NO_XDEV = 0x01
RESOLVE_NO_MAGICLINKS = 0x02
RESOLVE_NO_SYMLINKS = 0x04
RESOLVE_BENEATH = 0x08


class Reject(RuntimeError):
    """A fail-closed publication refusal."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise Reject(label)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False).encode("ascii")


def strict_pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in items:
        need(key not in result, "duplicate JSON key:" + key)
        result[key] = value
    return result


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    need(raw.endswith(b"\n"), label + ":terminal newline")
    need(not raw.endswith(b"\n\n"), label + ":single terminal newline")
    try:
        value = json.loads(raw, object_pairs_hook=strict_pairs)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Reject(label + ":strict JSON parse") from exc
    need(isinstance(value, dict), label + ":top-level object")
    return value


def verify_object(raw: bytes, expected: str, label: str,
                  require_canonical_file: bool = False) -> dict[str, Any]:
    need(HEX64.fullmatch(expected) is not None, label + ":expected object pin")
    value = strict_json(raw, label)
    claim = value.get("object_sha256")
    need(claim == expected, label + ":object claim pin")
    body = dict(value)
    del body["object_sha256"]
    need(sha256(canonical(body)) == expected, label + ":object closure")
    if require_canonical_file:
        need(raw == canonical(value) + b"\n", label + ":canonical file bytes")
    return value


def close_object(body: dict[str, Any]) -> dict[str, Any]:
    need("object_sha256" not in body, "outer body excludes object pin")
    result = dict(body)
    result["object_sha256"] = sha256(canonical(body))
    return result


def expected_publication() -> tuple[bytes, bytes, list[dict[str, str]]]:
    entries = [
        {"path": relative, "file_sha256": file_sha}
        for relative, file_sha, _ in EXACT8
    ]
    manifest_raw = b"".join(
        f"{item['file_sha256']}  {item['path']}\n".encode("ascii")
        for item in entries)
    manifest_sha = sha256(manifest_raw)
    outer = close_object({
        "schema": (
            "cm2.round306c79g.true-global-no-producer-consumer."
            "cold-launch-outer-receipt.v15"),
        "status": (
            "FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__"
            "RUNTIME_DEFERRED"),
        "effective_checkpoint_object_sha256": CHECKPOINT,
        "exact8_ordered_entries": entries,
        "cold_launch_manifest": {
            "path": MANIFEST_REL,
            "file_sha256": manifest_sha,
            "ordered_entry_count": 8,
        },
        "cold_launcher": {
            "path": LAUNCHER_V15[0],
            "file_sha256": LAUNCHER_V15[1],
        },
        "all_exact8_regular_0444_nlink1_and_held_for_runtime": True,
        "outer_published_after_exact8_manifest": True,
        "runtime_entry_must_be_cold_launcher": True,
        "sole_external_static_file_anchor_is_launcher_sha256": True,
        "declared_external_tcb": [
            "EXTERNAL_HELD_FD_SEALED_MEMFD_BOOTSTRAP",
            "PYTHON3_ISOLATED_INTERPRETER",
            "LINUX_KERNEL_OPENAT2_STATX_MEMFD_PROCFS",
        ],
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "runtime_executed_during_static_freeze": False,
    })
    outer_raw = canonical(outer) + b"\n"
    need(manifest_sha == EXPECTED_MANIFEST_FILE_SHA256,
         "mechanical manifest hash constant")
    need(sha256(outer_raw) == EXPECTED_OUTER_FILE_SHA256,
         "mechanical outer file hash constant")
    need(outer["object_sha256"] == EXPECTED_OUTER_OBJECT_SHA256,
         "mechanical outer object hash constant")
    return manifest_raw, outer_raw, entries


class StatxTimestamp(ctypes.Structure):
    _fields_ = [
        ("tv_sec", ctypes.c_int64),
        ("tv_nsec", ctypes.c_uint32),
        ("reserved", ctypes.c_int32),
    ]


class Statx(ctypes.Structure):
    _fields_ = [
        ("stx_mask", ctypes.c_uint32), ("stx_blksize", ctypes.c_uint32),
        ("stx_attributes", ctypes.c_uint64), ("stx_nlink", ctypes.c_uint32),
        ("stx_uid", ctypes.c_uint32), ("stx_gid", ctypes.c_uint32),
        ("stx_mode", ctypes.c_uint16), ("spare0", ctypes.c_uint16),
        ("stx_ino", ctypes.c_uint64), ("stx_size", ctypes.c_uint64),
        ("stx_blocks", ctypes.c_uint64),
        ("stx_attributes_mask", ctypes.c_uint64),
        ("stx_atime", StatxTimestamp), ("stx_btime", StatxTimestamp),
        ("stx_ctime", StatxTimestamp), ("stx_mtime", StatxTimestamp),
        ("stx_rdev_major", ctypes.c_uint32),
        ("stx_rdev_minor", ctypes.c_uint32),
        ("stx_dev_major", ctypes.c_uint32),
        ("stx_dev_minor", ctypes.c_uint32),
        ("stx_mnt_id", ctypes.c_uint64),
        ("stx_dio_mem_align", ctypes.c_uint32),
        ("stx_dio_offset_align", ctypes.c_uint32),
        ("spare3", ctypes.c_uint64 * 12),
    ]


class OpenHow(ctypes.Structure):
    _fields_ = [
        ("flags", ctypes.c_uint64),
        ("mode", ctypes.c_uint64),
        ("resolve", ctypes.c_uint64),
    ]


def library() -> ctypes.CDLL:
    result = ctypes.CDLL(None, use_errno=True)
    need(hasattr(result, "statx") and hasattr(result, "syscall"),
         "Linux statx/syscall TCB available")
    return result


def fd_mount_id(fd: int) -> int:
    info = Statx()
    ctypes.set_errno(0)
    outcome = library().statx(
        ctypes.c_int(fd), ctypes.c_char_p(b""),
        ctypes.c_int(AT_EMPTY_PATH | AT_SYMLINK_NOFOLLOW),
        ctypes.c_uint(STATX_BASIC_STATS | STATX_MNT_ID), ctypes.byref(info))
    need(outcome == 0 and bool(info.stx_mask & STATX_MNT_ID),
         "statx mount identity")
    statx_id = int(info.stx_mnt_id)
    need(statx_id > 0, "positive statx mount identity")
    with open(f"/proc/self/fdinfo/{fd}", "r", encoding="ascii") as stream:
        rows = [line for line in stream if line.startswith("mnt_id:\t")]
    need(len(rows) == 1 and int(rows[0].split("\t", 1)[1]) == statx_id,
         "statx/proc mount identity consensus")
    return statx_id


def openat2(dir_fd: int, relative: str, flags: int) -> int:
    path = Path(relative)
    need(relative not in {"", ".", ".."} and not path.is_absolute() and
         all(part not in {"", ".", ".."} for part in path.parts),
         "clean openat2 relative path:" + relative)
    how = OpenHow(
        flags | os.O_CLOEXEC,
        0,
        RESOLVE_NO_XDEV | RESOLVE_NO_MAGICLINKS |
        RESOLVE_NO_SYMLINKS | RESOLVE_BENEATH,
    )
    ctypes.set_errno(0)
    descriptor = library().syscall(
        ctypes.c_long(437), ctypes.c_int(dir_fd),
        ctypes.c_char_p(os.fsencode(relative)), ctypes.byref(how),
        ctypes.c_size_t(ctypes.sizeof(how)))
    if descriptor < 0:
        code = ctypes.get_errno()
        if code == errno.ENOENT:
            raise FileNotFoundError(code, os.strerror(code), relative)
        raise Reject("openat2 fail closed:" + relative + ":" + os.strerror(code))
    return int(descriptor)


def dir_identity(value: os.stat_result) -> tuple[int, int, int]:
    return value.st_dev, value.st_ino, value.st_mode


def file_identity(value: os.stat_result) -> tuple[int, int]:
    return value.st_dev, value.st_ino


def read_fd(fd: int) -> bytes:
    os.lseek(fd, 0, os.SEEK_SET)
    chunks: list[bytes] = []
    while True:
        block = os.read(fd, 1 << 20)
        if not block:
            return b"".join(chunks)
        chunks.append(block)


def process_fd_snapshot() -> frozenset[int]:
    """Return the live descriptor set without retaining the /proc scan fd."""
    result: set[int] = set()
    for name in os.listdir("/proc/self/fd"):
        if not name.isdecimal():
            continue
        descriptor = int(name)
        try:
            fcntl.fcntl(descriptor, fcntl.F_GETFD)
        except OSError:
            # The descriptor used internally by listdir may already be gone.
            continue
        result.add(descriptor)
    return frozenset(result)


class HeldDirectories:
    """Held ROOT/OUT/runtime identities and the official runtime lock."""

    def __init__(self, root_text: str) -> None:
        self.root_path = Path(root_text)
        need(self.root_path.is_absolute() and
             os.path.normpath(root_text) == root_text,
             "workspace root is absolute normalized lexical path")
        root_lstat = os.lstat(self.root_path)
        need(stat.S_ISDIR(root_lstat.st_mode) and
             not stat.S_ISLNK(root_lstat.st_mode),
             "workspace root real directory not symlink")
        self.root_fd = os.open(
            self.root_path,
            os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC |
            getattr(os, "O_NOATIME", 0))
        self.out_fd = -1
        self.runtime_fd = -1
        self.claim_fd = -1
        self.claim_identity: tuple[int, int] | None = None
        self.claim_owned = False
        self.claim_acquisition_pending = False
        self.claim_fd_baseline: frozenset[int] | None = None
        self.locked = False
        try:
            self.root_before = os.fstat(self.root_fd)
            need(dir_identity(root_lstat) == dir_identity(self.root_before),
                 "workspace root path/fd identity")
            self.out_fd = openat2(
                self.root_fd, "deliverables", os.O_RDONLY | os.O_DIRECTORY)
            self.runtime_fd = openat2(
                self.root_fd, ".cm2-runtime", os.O_RDONLY | os.O_DIRECTORY)
            self.out_before = os.fstat(self.out_fd)
            self.runtime_before = os.fstat(self.runtime_fd)
            need(stat.S_ISDIR(self.out_before.st_mode) and
                 stat.S_ISDIR(self.runtime_before.st_mode),
                 "held output and runtime directories")
            self.mount_id = fd_mount_id(self.root_fd)
            need(fd_mount_id(self.out_fd) == self.mount_id ==
                 fd_mount_id(self.runtime_fd) and
                 self.root_before.st_dev == self.out_before.st_dev ==
                 self.runtime_before.st_dev,
                 "ROOT/OUT/runtime one held mount")
            fcntl.flock(self.runtime_fd, fcntl.LOCK_EX)
            self.locked = True
            self._probe_lock()
            self.replay()
        except BaseException:
            self.close()
            raise

    def _probe_lock(self) -> None:
        probe = openat2(
            self.root_fd, ".cm2-runtime", os.O_RDONLY | os.O_DIRECTORY)
        try:
            blocked = False
            try:
                fcntl.flock(probe, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                blocked = True
            need(blocked, "independent nonblocking probe sees official LOCK_EX")
        finally:
            os.close(probe)

    def replay(self) -> None:
        root_path = os.lstat(self.root_path)
        root_now = os.fstat(self.root_fd)
        out_path = os.stat(
            "deliverables", dir_fd=self.root_fd, follow_symlinks=False)
        runtime_path = os.stat(
            ".cm2-runtime", dir_fd=self.root_fd, follow_symlinks=False)
        out_now = os.fstat(self.out_fd)
        runtime_now = os.fstat(self.runtime_fd)
        need(stat.S_ISDIR(root_path.st_mode) and
             stat.S_ISDIR(out_path.st_mode) and
             stat.S_ISDIR(runtime_path.st_mode),
             "ROOT/OUT/runtime remain directories")
        need(dir_identity(root_path) == dir_identity(root_now) ==
             dir_identity(self.root_before), "ROOT no parent swap")
        need(dir_identity(out_path) == dir_identity(out_now) ==
             dir_identity(self.out_before), "OUT no parent swap")
        need(dir_identity(runtime_path) == dir_identity(runtime_now) ==
             dir_identity(self.runtime_before), "runtime no parent swap")
        need(fd_mount_id(self.root_fd) == fd_mount_id(self.out_fd) ==
             fd_mount_id(self.runtime_fd) == self.mount_id,
             "held directory mount replay")

    def fsync_boundaries(self) -> None:
        os.fsync(self.out_fd)
        os.fsync(self.runtime_fd)
        os.fsync(self.root_fd)
        self.replay()

    def revalidate_claim(self) -> None:
        need(self.claim_owned and self.claim_fd >= 0 and
             self.claim_identity is not None,
             "publisher transaction claim is held")
        path_state = os.stat(
            TRANSACTION_CLAIM_NAME, dir_fd=self.runtime_fd,
            follow_symlinks=False)
        fd_state = os.fstat(self.claim_fd)
        need(stat.S_ISREG(path_state.st_mode) and
             file_identity(path_state) == file_identity(fd_state) ==
             self.claim_identity,
             "publisher transaction claim path/fd identity")
        need(stat.S_IMODE(fd_state.st_mode) == 0o600 and
             fd_state.st_nlink == 1 and
             fd_mount_id(self.claim_fd) == self.mount_id and
             read_fd(self.claim_fd) == TRANSACTION_CLAIM_RAW,
             "publisher transaction claim mode/link/mount/bytes")

    def acquire_claim(self) -> None:
        need(self.locked and not self.claim_owned and self.claim_fd < 0 and
             not self.claim_acquisition_pending and
             self.claim_fd_baseline is None,
             "publisher transaction claim clean acquisition state")
        # Snapshot before O_EXCL.  If CPython dispatches a signal after the
        # kernel returned the new fd but before STORE_ATTR claim_fd, the open
        # descriptor can still be recovered by its new-fd and named/held inode
        # identity.  This closes the otherwise unobservable CALL/STORE window
        # without ever unlinking a foreign pathname inode.
        self.claim_fd_baseline = process_fd_snapshot()
        self.claim_acquisition_pending = True
        try:
            self.claim_fd = os.open(
                TRANSACTION_CLAIM_NAME,
                os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW |
                os.O_CLOEXEC,
                0o600, dir_fd=self.runtime_fd)
            self.claim_owned = True
            held_state = os.fstat(self.claim_fd)
            self.claim_identity = file_identity(held_state)
            os.fchmod(self.claim_fd, 0o600)
            offset = 0
            while offset < len(TRANSACTION_CLAIM_RAW):
                count = os.write(self.claim_fd, TRANSACTION_CLAIM_RAW[offset:])
                need(count > 0, "publisher transaction claim complete write")
                offset += count
            os.fsync(self.claim_fd)
            os.fsync(self.runtime_fd)
            os.fsync(self.root_fd)
            self.revalidate_claim()
            self.claim_acquisition_pending = False
            self.claim_fd_baseline = None
        except BaseException:
            if (self.claim_owned or self.claim_fd >= 0 or
                    self.claim_acquisition_pending):
                try:
                    self.cleanup_claim_acquisition()
                except BaseException:
                    pass
            raise

    def recover_unstored_claim_fd(self) -> bool:
        """Recover only this process's post-snapshot fd for the named claim."""
        need(self.claim_acquisition_pending and self.claim_fd < 0 and
             self.claim_fd_baseline is not None,
             "publisher pending claim recovery state")
        try:
            path_state = os.stat(
                TRANSACTION_CLAIM_NAME, dir_fd=self.runtime_fd,
                follow_symlinks=False)
        except FileNotFoundError:
            self.claim_acquisition_pending = False
            self.claim_fd_baseline = None
            return False
        need(stat.S_ISREG(path_state.st_mode),
             "publisher pending claim recovery named regular file")
        candidates: list[int] = []
        for descriptor in sorted(
                process_fd_snapshot() - self.claim_fd_baseline):
            try:
                fd_state = os.fstat(descriptor)
            except OSError:
                continue
            if (stat.S_ISREG(fd_state.st_mode) and
                    file_identity(fd_state) == file_identity(path_state)):
                candidates.append(descriptor)
        need(len(candidates) == 1,
             "publisher pending claim recovery requires one fresh held/name "
             "identity and refuses foreign inode")
        self.claim_fd = candidates[0]
        self.claim_identity = file_identity(path_state)
        self.claim_owned = True
        self.claim_acquisition_pending = False
        self.claim_fd_baseline = None
        return True

    def cleanup_claim_acquisition(self) -> None:
        if self.claim_acquisition_pending and self.claim_fd < 0:
            self.recover_unstored_claim_fd()
        if self.claim_owned or self.claim_fd >= 0:
            self.remove_owned_claim()
        else:
            need(not self.claim_acquisition_pending and
                 self.claim_fd_baseline is None,
                 "publisher claim cleanup terminal state")

    def remove_owned_claim(self) -> None:
        # O_EXCL ownership can exist after claim_fd was stored but before the
        # later owned flag/identity snapshot.  A held descriptor is sufficient
        # for fresh named-vs-held identity-only cleanup.
        if not self.claim_owned and self.claim_fd < 0:
            need(self.claim_identity is None, "unowned claim identity absent")
            return
        need(self.claim_fd >= 0, "publisher claim cleanup held fd")
        path_state = os.stat(
            TRANSACTION_CLAIM_NAME, dir_fd=self.runtime_fd,
            follow_symlinks=False)
        fd_state = os.fstat(self.claim_fd)
        need(stat.S_ISREG(path_state.st_mode) and
             file_identity(path_state) == file_identity(fd_state),
             "publisher claim cleanup refuses foreign pathname inode")
        if self.claim_identity is not None:
            need(file_identity(fd_state) == self.claim_identity,
                 "publisher claim cleanup held identity snapshot")
        content_error: str | None = None
        if self.claim_owned and self.claim_identity is not None:
            try:
                self.revalidate_claim()
            except BaseException as exc:
                # Content/mode drift is reported after identity-safe unlink;
                # it must not strand the installer-owned coordination inode.
                content_error = type(exc).__name__ + ":" + str(exc)
        os.unlink(TRANSACTION_CLAIM_NAME, dir_fd=self.runtime_fd)
        self.claim_owned = False
        os.fsync(self.runtime_fd)
        os.fsync(self.root_fd)
        try:
            os.stat(TRANSACTION_CLAIM_NAME, dir_fd=self.runtime_fd,
                    follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            raise Reject("publisher transaction claim unlink replay")
        os.close(self.claim_fd)
        self.claim_fd = -1
        self.claim_identity = None
        self.claim_acquisition_pending = False
        self.claim_fd_baseline = None
        self.replay()
        if content_error is not None:
            raise Reject("publisher transaction claim drift removed:" +
                         content_error)

    def close(self) -> None:
        if (self.claim_owned or self.claim_fd >= 0 or
                self.claim_acquisition_pending):
            try:
                self.cleanup_claim_acquisition()
            except BaseException:
                # The main transaction path explicitly surfaces cleanup
                # failures.  This is constructor/unwind last-resort cleanup.
                if self.claim_fd >= 0:
                    try:
                        os.close(self.claim_fd)
                    except OSError:
                        pass
                    self.claim_fd = -1
                self.claim_identity = None
                self.claim_owned = False
                self.claim_acquisition_pending = False
                self.claim_fd_baseline = None
        if self.locked and self.runtime_fd >= 0:
            try:
                fcntl.flock(self.runtime_fd, fcntl.LOCK_UN)
            except OSError:
                pass
            self.locked = False
        for descriptor in (self.runtime_fd, self.out_fd, self.root_fd):
            if descriptor >= 0:
                try:
                    os.close(descriptor)
                except OSError:
                    pass
        self.runtime_fd = self.out_fd = self.root_fd = -1


class HeldFile:
    """One exact output-directory file held across the whole command."""

    def __init__(self, directories: HeldDirectories,
                 pin: tuple[str, str, str | None], expected_mode: int) -> None:
        self.directories = directories
        self.relative, self.file_sha256, self.object_sha256 = pin
        parts = Path(self.relative).parts
        need(len(parts) == 2 and parts[0] == "deliverables",
             "exact8 direct output member:" + self.relative)
        self.name = parts[1]
        path_state = os.stat(
            self.name, dir_fd=directories.out_fd, follow_symlinks=False)
        need(stat.S_ISREG(path_state.st_mode) and
             not stat.S_ISLNK(path_state.st_mode),
             self.relative + ":regular no symlink")
        need(path_state.st_nlink == 1 and
             stat.S_IMODE(path_state.st_mode) == expected_mode,
             self.relative + f":exact initial {expected_mode:04o}/nlink1")
        self.fd = os.open(
            self.name,
            os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC |
            getattr(os, "O_NOATIME", 0),
            dir_fd=directories.out_fd)
        try:
            self.before = os.fstat(self.fd)
            need(file_identity(path_state) == file_identity(self.before),
                 self.relative + ":path/fd identity")
            need(fd_mount_id(self.fd) == directories.mount_id and
                 self.before.st_dev == directories.out_before.st_dev,
                 self.relative + ":held output mount")
            raw = read_fd(self.fd)
            need(sha256(raw) == self.file_sha256,
                 self.relative + ":file hash pin")
            if self.object_sha256 is not None:
                verify_object(
                    raw, self.object_sha256, self.relative,
                    require_canonical_file=(self.relative == PREDECESSOR_SUPERSESSION[0]))
        except BaseException:
            os.close(self.fd)
            self.fd = -1
            raise

    @classmethod
    def create_exclusive(cls, directories: HeldDirectories, relative: str,
                         raw: bytes, object_sha256: str | None) -> "HeldFile":
        self = cls.__new__(cls)
        self.directories = directories
        self.relative = relative
        self.file_sha256 = sha256(raw)
        self.object_sha256 = object_sha256
        parts = Path(relative).parts
        need(len(parts) == 2 and parts[0] == "deliverables",
             "publication direct output member:" + relative)
        self.name = parts[1]
        try:
            os.stat(self.name, dir_fd=directories.out_fd, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            raise Reject(relative + ":must not preexist")
        self.fd = os.open(
            self.name,
            os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC,
            0o444, dir_fd=directories.out_fd)
        try:
            offset = 0
            while offset < len(raw):
                count = os.write(self.fd, raw[offset:])
                need(count > 0, relative + ":complete write")
                offset += count
            os.fsync(self.fd)
            os.fchmod(self.fd, 0o444)
            os.fsync(self.fd)
            directories.fsync_boundaries()
            path_state = os.stat(
                self.name, dir_fd=directories.out_fd, follow_symlinks=False)
            self.before = os.fstat(self.fd)
            need(file_identity(path_state) == file_identity(self.before) and
                 stat.S_ISREG(self.before.st_mode) and
                 stat.S_IMODE(self.before.st_mode) == 0o444 and
                 self.before.st_nlink == 1 and self.before.st_size == len(raw),
                 relative + ":exclusive frozen publication")
            need(read_fd(self.fd) == raw and sha256(raw) == self.file_sha256,
                 relative + ":published bytes replay")
            if object_sha256 is not None:
                verify_object(raw, object_sha256, relative, True)
            return self
        except BaseException:
            # Append-only fail-closed behavior: a partial O_EXCL surface is
            # never deleted or overwritten by this guard.
            os.close(self.fd)
            self.fd = -1
            raise

    def replay(self, expected_mode: int = 0o444) -> os.stat_result:
        path_state = os.stat(
            self.name, dir_fd=self.directories.out_fd, follow_symlinks=False)
        fd_state = os.fstat(self.fd)
        need(stat.S_ISREG(path_state.st_mode) and
             file_identity(path_state) == file_identity(fd_state),
             self.relative + ":terminal path/fd identity")
        need(stat.S_IMODE(fd_state.st_mode) == expected_mode and
             fd_state.st_nlink == 1,
             self.relative + f":terminal {expected_mode:04o}/nlink1")
        need(fd_mount_id(self.fd) == self.directories.mount_id,
             self.relative + ":terminal mount")
        raw = read_fd(self.fd)
        need(sha256(raw) == self.file_sha256,
             self.relative + ":terminal file hash")
        if self.object_sha256 is not None:
            verify_object(
                raw, self.object_sha256, self.relative,
                require_canonical_file=(
                    self.relative in {PREDECESSOR_SUPERSESSION[0], OUTER_REL}))
        return fd_state

    def freeze(self) -> os.stat_result:
        need(stat.S_IMODE(os.fstat(self.fd).st_mode) == 0o664,
             self.relative + ":freeze begins at 0664")
        os.fsync(self.fd)
        os.fchmod(self.fd, 0o444)
        os.fsync(self.fd)
        self.directories.fsync_boundaries()
        self.before = self.replay(0o444)
        return self.before

    def restore_prepublication_mode(self) -> os.stat_result:
        """Rollback a pre-manifest chmod without changing pinned bytes."""
        self.replay(0o444)
        os.fchmod(self.fd, 0o664)
        os.fsync(self.fd)
        self.directories.fsync_boundaries()
        self.before = self.replay(0o664)
        return self.before

    def close(self) -> None:
        if self.fd >= 0:
            try:
                os.close(self.fd)
            except OSError:
                pass
            self.fd = -1


def assert_output_absent(directories: HeldDirectories, relative: str) -> None:
    parts = Path(relative).parts
    need(len(parts) == 2 and parts[0] == "deliverables",
         "absence direct output path")
    try:
        os.stat(parts[1], dir_fd=directories.out_fd, follow_symlinks=False)
    except FileNotFoundError:
        return
    raise Reject(relative + ":must remain absent including broken symlink")


def assert_secure_absent(root_fd: int, relative: str) -> None:
    try:
        descriptor = openat2(
            root_fd, relative,
            getattr(os, "O_PATH", os.O_RDONLY) | getattr(os, "O_NOFOLLOW", 0))
    except FileNotFoundError:
        return
    else:
        os.close(descriptor)
    raise Reject(relative + ":runtime surface must remain absent")


def scan_names(fd: int, predicate: Any, label: str,
               prefix: str = "") -> None:
    """Secure recursive lexical scan without following directory symlinks."""
    for name in os.listdir(fd):
        need(name not in {"", ".", ".."}, label + ":clean directory entry")
        relative = name if not prefix else prefix + "/" + name
        if predicate(relative, name):
            raise Reject(label + ":forbidden entry:" + relative)
        state = os.stat(name, dir_fd=fd, follow_symlinks=False)
        if stat.S_ISDIR(state.st_mode) and not stat.S_ISLNK(state.st_mode):
            child = os.open(
                name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW |
                os.O_CLOEXEC | getattr(os, "O_NOATIME", 0), dir_fd=fd)
            try:
                scan_names(child, predicate, label, relative)
            finally:
                os.close(child)


def assert_no_v15_pyc(directories: HeldDirectories) -> None:
    """Reject every lexical v15 .pyc anywhere beneath the held root.

    Restricting this check to conventional ``__pycache__`` directories would
    permit a direct or relocated bytecode contaminant.  The recursive scan is
    rooted in the already-held workspace descriptor and never follows a
    symlinked directory.
    """
    predicate = lambda _relative, name: (
        name.lower().endswith(".pyc") and "v15" in name.lower())
    scan_names(directories.root_fd, predicate, "v15 pyc")


def assert_v15_runtime_absent(
        directories: HeldDirectories, *, allowed_claim: bool = False,
) -> None:
    if allowed_claim:
        directories.revalidate_claim()
    for relative in V15_RUNTIME_SURFACES:
        assert_secure_absent(directories.root_fd, relative)
    scan_names(
        directories.runtime_fd,
        lambda relative, name: (
            "c79g-v15" in name.lower() and not
            (allowed_claim and relative == TRANSACTION_CLAIM_NAME)),
        "v15 runtime namespace")
    if allowed_claim:
        directories.revalidate_claim()


def verify_launcher_ast(raw: bytes) -> None:
    """Prove final pins and exact8 order without importing the launcher."""
    try:
        tree = ast.parse(raw.decode("utf-8"), filename=LAUNCHER_V15[0])
    except (UnicodeDecodeError, SyntaxError) as exc:
        raise Reject("launcher AST parse") from exc
    flags = [
        node for node in tree.body
        if isinstance(node, (ast.Assign, ast.AnnAssign)) and
        ((isinstance(node, ast.Assign) and len(node.targets) == 1 and
          isinstance(node.targets[0], ast.Name) and
          node.targets[0].id == "FINAL_BASE7_PINS_INSTALLED") or
         (isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and
          node.target.id == "FINAL_BASE7_PINS_INSTALLED"))
    ]
    need(len(flags) == 1 and isinstance(flags[0].value, ast.Constant) and
         flags[0].value.value is True,
         "launcher final base7 flag installed")
    configurators = [
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and
        node.name == "configure_workspace_paths"]
    need(len(configurators) == 1, "launcher unique path configurator")
    assignments = {
        target.id: node.value
        for node in configurators[0].body
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and
        isinstance((target := node.targets[0]), ast.Name) and
        target.id in {"BASE7_PINS", "EXACT8"}
    }
    need(set(assignments) == {"BASE7_PINS", "EXACT8"},
         "launcher base7/exact8 assignments")
    table = assignments["BASE7_PINS"]
    need(isinstance(table, ast.Dict), "launcher base7 dict")
    names = [node.id if isinstance(node, ast.Name) else None
             for node in table.keys]
    need(names == [
        "V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT",
        "SCHEMA", "CONTRACT", "PRODUCER",
        "CONSUMER", "TRANSITION", "AUDIT"],
        "launcher base7 exact order")
    expected = [(item[1], item[2]) for item in EXACT8[:7]]
    # The first tuple deliberately references the two audited v14 constants.
    first = table.values[0]
    need(isinstance(first, ast.Tuple) and [
        item.id if isinstance(item, ast.Name) else None for item in first.elts
    ] == ["V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_FILE_PIN",
          "V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_OBJECT_PIN"],
         "launcher v14 receipt named pins")
    for node, pair in zip(table.values[1:], expected[1:]):
        need(isinstance(node, ast.Tuple) and ast.literal_eval(node) == pair,
             "launcher literal base7 pin")
    exact = assignments["EXACT8"]
    need(isinstance(exact, ast.Tuple) and [
        item.id if isinstance(item, ast.Name) else None for item in exact.elts
    ] == [
        "V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT",
        "SCHEMA", "CONTRACT", "PRODUCER",
        "CONSUMER", "TRANSITION", "AUDIT", "SELF"],
        "launcher exact8 exact order")
    constants: dict[str, Any] = {}
    for node in tree.body:
        if (isinstance(node, ast.Assign) and len(node.targets) == 1 and
                isinstance(node.targets[0], ast.Name) and
                node.targets[0].id in {
                    "V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_FILE_PIN",
                    "V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_OBJECT_PIN"}):
            constants[node.targets[0].id] = ast.literal_eval(node.value)
    need(constants == {
        "V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_FILE_PIN":
            PREDECESSOR_SUPERSESSION[1],
        "V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_OBJECT_PIN":
            PREDECESSOR_SUPERSESSION[2],
    }, "launcher v14 receipt constant pins")


def verify_static_surfaces(held: dict[str, HeldFile]) -> None:
    schema = strict_json(read_fd(held[SCHEMA_V15[0]].fd), "v15 schema")
    need(schema.get("$ref") == "#/$defs/coldLaunchedCommittedAuthority",
         "v15 schema cold-launched sole root")

    receipt = verify_object(
        read_fd(held[PREDECESSOR_SUPERSESSION[0]].fd), PREDECESSOR_SUPERSESSION[2],
        "v14 supersession", True)
    need(receipt.get("status") ==
         "FROZEN_APPEND_ONLY_V14_RUNTIME_REGISTRY_SHAPE_DRIFT_REJECTION__"
         "ZERO_CREDIT__V15_SUCCESSOR_ONLY" and
         receipt.get("v15_successor_contract", {}).get(
             "v15_current_exact8_first_member_must_be_this_receipt") is True,
         "v14 receipt v15 one-way anchor")

    contract = verify_object(
        read_fd(held[CONTRACT_V15[0]].fd), CONTRACT_V15[2], "v15 contract")
    paths = [item[0] for item in EXACT8]
    bundle = contract.get("v15_bundle", {})
    need(contract.get("status") ==
         "STATIC_CONTRACT_BYTES_FINAL__COLD_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED" and
         contract.get("effective_checkpoint_object_sha256") == CHECKPOINT and
         bundle.get("base7_ordered_paths") == paths[:7] and
         bundle.get("exact8_ordered_paths") == paths and
         bundle.get("exact10_ordered_paths") == paths + [MANIFEST_REL, OUTER_REL] and
         bundle.get("cold_launch_outer_closure", {}).get(
             "current_v15_exact10_plus_all_append_only_predecessors_unique_file_identity_count") == 126,
         "v15 contract exact ordered publication paths")
    publication = contract.get("exact_publication_paths", {})
    need(publication.get("cold_launch_exact8_manifest") == MANIFEST_REL and
         publication.get("cold_launch_outer_last") == OUTER_REL and
         publication.get("cold_launcher") == LAUNCHER_V15[0],
         "v15 contract manifest/outer/launcher paths")
    runtime_from_contract = {
        publication.get("candidate_A"), publication.get("candidate_B"),
        publication.get("verification_A"), publication.get("verification_B"),
        publication.get("committed_completion"), publication.get("authority_seal"),
        publication.get("completion_staging_path"),
        publication.get("authority_staging_path"),
        publication.get("v15_rejection_namespace"),
        str(publication.get("candidate_staging_path_template", "")).replace(
            "{a|b}", "a"),
        str(publication.get("candidate_staging_path_template", "")).replace(
            "{a|b}", "b"),
        str(publication.get("verification_staging_path_template", "")).replace(
            "{a|b}", "a"),
        str(publication.get("verification_staging_path_template", "")).replace(
            "{a|b}", "b"),
    }
    need(runtime_from_contract == set(V15_RUNTIME_SURFACES),
         "v15 contract exact runtime surface set")
    freeze = contract.get("static_freeze_protocol_requirements", {})
    need(freeze.get(
        "requires_cold_launch_exact8_each_final_0444_and_fsynced_before_manifest_write") is True and
        freeze.get(
        "requires_cold_launch_manifest_written_then_0444_and_fsynced_before_outer_write") is True and
        freeze.get(
        "requires_cold_launch_outer_written_last_then_0444_and_fsynced_before_parent_fsync") is True and
        freeze.get("pyc_or___pycache___written") is False and
        freeze.get("runtime_execution_performed_while_drafting") is False,
        "v15 contract physical freeze requirements")

    transition = verify_object(
        read_fd(held[TRANSITION_V15[0]].fd), TRANSITION_V15[2], "v15 transition")
    need(transition.get("status") ==
         "STATIC_BYTES_CLOSED_V14_TO_V15__PHYSICAL_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED" and
         transition.get("formal_global_closure_credit") == 0 and
         transition.get("D02_unlock") is False and
         transition.get("runtime_executed_during_transition") is False,
         "v15 transition zero-credit no-run boundary")

    audit = verify_object(
        read_fd(held[AUDIT_V15[0]].fd), AUDIT_V15[2], "v15 static audit")
    need(audit.get("status") ==
         "PASS_DUAL_STATIC_PIN_NORMALIZED_AST_GO_V15__"
         "PHYSICAL_COLD_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED",
         "v15 audit final dual GO")
    expected_audited = {
        "closed_schema": SCHEMA_V15,
        "contract": CONTRACT_V15,
        "build_only_producer": PRODUCER_V15,
        "independent_verifier_assembler_authority_consumer": CONSUMER_V15,
        "v14_to_v15_transition_receipt": TRANSITION_V15,
    }
    audited = audit.get("audited_v15_bundle", {})
    for key, (relative, file_sha, object_sha) in expected_audited.items():
        record = audited.get(key, {})
        need(record.get("path") == relative and
             record.get("file_sha256") == file_sha and
             (object_sha is None or record.get("object_sha256") == object_sha),
             "v15 audit pin:" + key)
    need(audit.get("static_credit_census", {}).get(
             "all_persisted_v15_objects_formal_global_closure_credit") == 0 and
         audit.get("static_credit_census", {}).get(
             "all_persisted_v15_objects_D02_unlock") is False and
         audit.get("static_no_run", {}).get("C79_v15_runtime_artifact_count") == 0 and
         audit.get("static_no_run", {}).get("pyc_or___pycache___created") is False and
         audit.get("final_audit_acceptance", {}).get(
             "requires_cold_exact8_freeze_manifest_then_outer_last_and_terminal_replay") is True and
         audit.get("final_audit_acceptance", {}).get(
             "this_audit_authorizes_C79_runtime") is False,
         "v15 audit static zero-credit freeze gate")

    verify_launcher_ast(read_fd(held[LAUNCHER_V15[0]].fd))


def assert_unpublished_clean(
        directories: HeldDirectories, *, allowed_claim: bool = False,
) -> None:
    directories.replay()
    assert_output_absent(directories, MANIFEST_REL)
    assert_output_absent(directories, OUTER_REL)
    assert_no_v15_pyc(directories)
    assert_v15_runtime_absent(directories, allowed_claim=allowed_claim)
    directories.replay()


def publication_cli_tail() -> list[str]:
    return [
        "PUBLISH",
        *(item[1] for item in EXACT8),
        EXPECTED_MANIFEST_FILE_SHA256,
        EXPECTED_OUTER_FILE_SHA256,
        EXPECTED_OUTER_OBJECT_SHA256,
    ]


def verify_publish_cli(actual: Iterable[str]) -> None:
    expected = publication_cli_tail()
    need(list(actual) == expected,
         "PUBLISH requires exact ordered prehash/publication-hash CLI")
    need(ONE_SHOT_PUBLISH_ENABLED is False,
         "audited source flag must remain false; exact CLI is sole authority")


def chronology(exact8: list[os.stat_result], manifest: os.stat_result,
               outer: os.stat_result) -> dict[str, bool]:
    exact8_mtime_not_after_ctime = all(
        item.st_mtime_ns <= item.st_ctime_ns for item in exact8)
    max_exact8_before_manifest = (
        max(max(item.st_mtime_ns, item.st_ctime_ns) for item in exact8) <
        manifest.st_mtime_ns)
    manifest_mtime_not_after_ctime = manifest.st_mtime_ns <= manifest.st_ctime_ns
    manifest_ctime_before_outer = manifest.st_ctime_ns < outer.st_mtime_ns
    outer_mtime_not_after_ctime = outer.st_mtime_ns <= outer.st_ctime_ns
    return {
        "all_exact8_mtime_not_after_final_ctime": exact8_mtime_not_after_ctime,
        "max_exact8_final_mtime_ctime_before_manifest_mtime":
            max_exact8_before_manifest,
        "manifest_mtime_not_after_final_ctime": manifest_mtime_not_after_ctime,
        "manifest_final_ctime_before_outer_mtime": manifest_ctime_before_outer,
        "outer_mtime_not_after_final_ctime": outer_mtime_not_after_ctime,
        "physical_exact8_freeze_then_manifest_freeze_then_outer_freeze_chronology":
            exact8_mtime_not_after_ctime and max_exact8_before_manifest and
            manifest_mtime_not_after_ctime and manifest_ctime_before_outer and
            outer_mtime_not_after_ctime,
    }


def output_exists(directories: HeldDirectories, relative: str) -> bool:
    parts = Path(relative).parts
    need(len(parts) == 2 and parts[0] == "deliverables",
         "existence direct output path")
    try:
        os.stat(parts[1], dir_fd=directories.out_fd, follow_symlinks=False)
    except FileNotFoundError:
        return False
    return True


def run(root_text: str, command_and_hashes: list[str]) -> dict[str, Any]:
    need(command_and_hashes, "command required")
    command = command_and_hashes[0]
    read_only = command in {"PREFLIGHT", "PRECHECK"}
    need(read_only or command == "PUBLISH", "exact command")
    if read_only:
        need(command_and_hashes == [command],
             command + " takes no hash arguments")
    else:
        # This full exact vector is validated before the lock, claim, target
        # opens, chmods, or O_EXCL publication surfaces.
        verify_publish_cli(command_and_hashes)

    manifest_raw, outer_raw, entries = expected_publication()
    directories = HeldDirectories(root_text)
    opened: list[HeldFile] = []
    held: dict[str, HeldFile] = {}
    result: dict[str, Any] | None = None
    primary: BaseException | None = None
    rollback: dict[str, Any] = {
        "attempted": False,
        "restored_prepublication_modes": False,
        "append_only_publication_boundary_crossed": False,
        "manifest_present": False,
        "outer_present": False,
        "error": None,
    }
    cleanup_error: str | None = None
    try:
        assert_unpublished_clean(directories)
        if not read_only:
            directories.acquire_claim()
            assert_unpublished_clean(directories, allowed_claim=True)
        for index, pin in enumerate(EXACT8):
            expected_mode = 0o444 if index == 0 else 0o664
            item = HeldFile(directories, pin, expected_mode)
            opened.append(item)
            held[item.relative] = item
        need(len({file_identity(item.before) for item in opened}) == 8 and
             len({item.before.st_dev for item in opened}) == 1 and
             all(fd_mount_id(item.fd) == directories.mount_id for item in opened),
             "prepublication exact8 pairwise unique on held mount")
        verify_static_surfaces(held)
        assert_unpublished_clean(
            directories, allowed_claim=not read_only)
        for index, item in enumerate(opened):
            item.replay(0o444 if index == 0 else 0o664)
        directories.replay()

        if read_only:
            result = {
                "status": (
                    command + "_READ_ONLY_PASS_UNDER_OFFICIAL_LOCK_V15__"
                    "EXACT8_PREHASHED__PUBLICATION_BYTES_MECHANICALLY_CLOSED"),
                "source_one_shot_flag": ONE_SHOT_PUBLISH_ENABLED,
                "publish_authority":
                    "COMPLETE_EXACT_CLI_PREHASH_AND_PUBLICATION_HASH_CONTRACT",
                "ordered_exact8_prepublication": [
                    {"ordinal": index, "path": pin[0],
                     "file_sha256": pin[1], "object_sha256": pin[2],
                     "required_initial_mode": "0444" if index == 1 else "0664"}
                    for index, pin in enumerate(EXACT8, start=1)
                ],
                "required_publish_argv_tail": publication_cli_tail(),
                "mechanical_manifest_file_sha256":
                    EXPECTED_MANIFEST_FILE_SHA256,
                "mechanical_outer_file_sha256": EXPECTED_OUTER_FILE_SHA256,
                "mechanical_outer_object_sha256": EXPECTED_OUTER_OBJECT_SHA256,
                "manifest_absent": True,
                "outer_absent": True,
                "v15_pyc_absent": True,
                "v15_runtime_absent": True,
                "transaction_claim_created": False,
                "ROOT_OUT_runtime_held_same_mount": True,
                "official_runtime_LOCK_EX_held_and_independently_probed": True,
                "target_protocol_import_or_execution_count": 0,
                "named_file_write_chmod_fsync_or_publication_count": 0,
            }
        else:
            # Receipt ordinal one is already permanently frozen.  Fsync and
            # replay it first, then freeze the seven 0664 v15 members in order.
            directories.revalidate_claim()
            os.fsync(opened[0].fd)
            directories.fsync_boundaries()
            opened[0].replay(0o444)
            for index in range(1, 8):
                directories.revalidate_claim()
                opened[index].freeze()
                for prefix_index in range(index + 1):
                    opened[prefix_index].replay(0o444)
                for suffix_index in range(index + 1, 8):
                    opened[suffix_index].replay(0o664)
                assert_unpublished_clean(directories, allowed_claim=True)

            exact8_states = [item.replay(0o444) for item in opened]
            directories.fsync_boundaries()
            assert_unpublished_clean(directories, allowed_claim=True)

            manifest = HeldFile.create_exclusive(
                directories, MANIFEST_REL, manifest_raw, None)
            opened.append(manifest)
            manifest_state = manifest.replay(0o444)
            need(manifest_state.st_mtime_ns <= manifest_state.st_ctime_ns and
                 max(max(item.st_mtime_ns, item.st_ctime_ns)
                     for item in exact8_states) < manifest_state.st_mtime_ns,
                 "exact8 physical freeze strictly before manifest")
            assert_output_absent(directories, OUTER_REL)
            assert_no_v15_pyc(directories)
            assert_v15_runtime_absent(directories, allowed_claim=True)
            directories.replay()

            outer = HeldFile.create_exclusive(
                directories, OUTER_REL, outer_raw,
                EXPECTED_OUTER_OBJECT_SHA256)
            opened.append(outer)
            outer_state = outer.replay(0o444)
            final_chronology = chronology(
                exact8_states, manifest_state, outer_state)
            need(all(final_chronology.values()),
                 "launcher-identical physical exact8/manifest/outer chronology")
            assert_no_v15_pyc(directories)
            assert_v15_runtime_absent(directories, allowed_claim=True)

            terminal_states = [item.replay(0o444) for item in opened]
            need(len(terminal_states) == 10 and
                 len({file_identity(item) for item in terminal_states}) == 10 and
                 len({item.st_dev for item in terminal_states}) == 1 and
                 all(fd_mount_id(item.fd) == directories.mount_id
                     for item in opened),
                 "terminal exact10 pairwise unique on held mount")
            need(read_fd(opened[8].fd) == manifest_raw and
                 read_fd(opened[9].fd) == outer_raw,
                 "terminal exact manifest and outer bytes")
            verify_static_surfaces(held)
            directories.fsync_boundaries()
            directories.replay()
            need(chronology(
                terminal_states[:8], terminal_states[8], terminal_states[9]) ==
                 final_chronology,
                 "terminal exact10 chronology unchanged")

            # Remove only the held, identity-matching transaction claim, then
            # replay exact10 once more under the still-held official lock.
            directories.remove_owned_claim()
            assert_v15_runtime_absent(directories)
            post_claim_states = [item.replay(0o444) for item in opened]
            need([file_identity(item) for item in post_claim_states] ==
                 [file_identity(item) for item in terminal_states],
                 "post-claim-removal exact10 identity replay")
            result = {
                "status": (
                    "TERMINAL_EXACT10_HELD_REPLAY_PASS_UNDER_SAME_OFFICIAL_"
                    "LOCK_V15__FROZEN_MANIFEST_OUTER_LAST__RUNTIME_NOT_EXECUTED"),
                "authorization":
                    "EXPLICIT_COMPLETE_EXACT_PREHASH_PUBLICATION_HASH_CONTRACT",
                "source_one_shot_flag": ONE_SHOT_PUBLISH_ENABLED,
                "ordered_exact10": [
                    {"ordinal": index, "path": relative,
                     "file_sha256": file_sha}
                    for index, (relative, file_sha) in enumerate([
                        *((item[0], item[1]) for item in EXACT8),
                        (MANIFEST_REL, EXPECTED_MANIFEST_FILE_SHA256),
                        (OUTER_REL, EXPECTED_OUTER_FILE_SHA256),
                    ], start=1)
                ],
                "outer_object_sha256": EXPECTED_OUTER_OBJECT_SHA256,
                "chronology": final_chronology,
                "unique_file_identity_count": 10,
                "same_st_dev_and_statx_mount_id": True,
                "all_exact10_regular_0444_nlink1": True,
                "manifest_O_EXCL_outer_last_O_EXCL": True,
                "transaction_claim_O_EXCL_identity_removed_before_unlock": True,
                "post_claim_removal_terminal_replay": True,
                "v15_pyc_absent": True,
                "v15_runtime_absent": True,
                "target_protocol_import_or_execution_count": 0,
            }
    except BaseException as exc:
        primary = exc
        if not read_only:
            rollback["attempted"] = True
            rollback["manifest_present"] = output_exists(
                directories, MANIFEST_REL)
            rollback["outer_present"] = output_exists(directories, OUTER_REL)
            rollback["append_only_publication_boundary_crossed"] = bool(
                rollback["manifest_present"] or rollback["outer_present"])
            if not rollback["append_only_publication_boundary_crossed"]:
                try:
                    for item in reversed(opened[:8]):
                        if item.relative != PREDECESSOR_SUPERSESSION[0] and \
                                stat.S_IMODE(os.fstat(item.fd).st_mode) == 0o444:
                            item.restore_prepublication_mode()
                    for index, item in enumerate(opened[:8]):
                        item.replay(0o444 if index == 0 else 0o664)
                    assert_unpublished_clean(
                        directories, allowed_claim=directories.claim_owned)
                    rollback["restored_prepublication_modes"] = True
                except BaseException as rollback_exc:
                    rollback["error"] = (
                        type(rollback_exc).__name__ + ":" + str(rollback_exc))
            else:
                rollback["error"] = (
                    "APPEND_ONLY_BOUNDARY_PRESERVED__NO_MANIFEST_OR_OUTER_"
                    "DELETE_OVERWRITE_RENAME__SUPERSESSION_REQUIRED_IF_INCOMPLETE")
    finally:
        if (directories.claim_owned or directories.claim_fd >= 0 or
                directories.claim_acquisition_pending):
            try:
                directories.cleanup_claim_acquisition()
            except BaseException as exc:
                cleanup_error = type(exc).__name__ + ":" + str(exc)
        seen: set[int] = set()
        for item in reversed(opened):
            if id(item) not in seen:
                seen.add(id(item))
                item.close()
        directories.close()

    if primary is not None or cleanup_error is not None:
        failure = {
            "primary_error": (None if primary is None else
                              type(primary).__name__ + ":" + str(primary)),
            "rollback": rollback,
            "transaction_claim_cleanup_error": cleanup_error,
            "failure_boundary": (
                "BEFORE_MANIFEST_MODE_ROLLBACK_ATTEMPTED__AT_OR_AFTER_MANIFEST_"
                "APPEND_ONLY_SURFACES_PRESERVED_AND_SUCCESSOR_REQUIRED"),
        }
        raise Reject("PUBLISH transaction failed:" +
                     canonical(failure).decode("ascii")) from primary
    need(result is not None, "command produced a result")
    return result


def main() -> int:
    if not __debug__:
        raise Reject("python -O is forbidden")
    need(len(sys.argv) >= 3, "usage: guard ROOT PREFLIGHT|PUBLISH ...")
    result = run(sys.argv[1], sys.argv[2:])
    os.write(1, canonical(result) + b"\n")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Reject as exc:
        os.write(2, ("FAIL_CLOSED_V15_PUBLISH_GUARD:" + str(exc) + "\n").encode("utf-8"))
        raise SystemExit(1)
