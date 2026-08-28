#!/usr/bin/env python3
"""Externally pinned cold launcher for the C79g v3 exact10 static bundle.

This is the sole constructor of a positive-credit C79g value.  The producer
and independent consumer are executed from source descriptors already held by
this launcher and can emit only zero-credit persisted surfaces or a zero-credit
inner live composite.  Non-authorize and zero-output authorize branches replay
the exact10 static bundle after clean child exit.  The positive authorize branch
replays exact10 before its child-live ACK, then commits the non-persisted wrapper
only by a raw blocking fd1 final-newline write; RELEASE and reap are thereafter
non-authority cleanup.
"""

from __future__ import annotations

import argparse
import copy
import ctypes
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
from typing import Any, Mapping


SELF = Path(os.path.abspath(__file__))
ROOT = SELF.parents[1]
OUT = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"
CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
REJECTION = OUT / (BASE + "_v2_rejection_supersession_receipt_v1.json")
SCHEMA = OUT / (BASE + "_schema_v3.json")
CONTRACT = OUT / (BASE + "_contract_v3.json")
PRODUCER = OUT / (BASE + "_v3.py")
CONSUMER = OUT / (BASE + "_independent_verifier_assembler_authority_consumer_v3.py")
TRANSITION = OUT / (BASE + "_v2_to_v3_static_launch_transition_receipt_v1.json")
AUDIT = OUT / (BASE + "_static_audit_v3.json")
MANIFEST = OUT / (BASE + "_cold_launch_manifest_v3.sha256")
OUTER = OUT / (BASE + "_cold_launch_outer_receipt_v3.json")
REJECTION_NAMESPACE = RUNTIME / ("c79g-v3-rejections-" + CHECKPOINT)

# Filled only after the base seven bytes are final.  The launcher is eighth
# and is pinned by the later manifest plus the external cold-start SHA-256.
BASE7_PINS: dict[Path, tuple[str, str | None]] = {
    REJECTION: ("fdd1921afda98a34c87ae20094e60fca1b75c8f233cf37890e7817fe35d82408",
                "518cbc5b30fc62d55291feef407c5677b880a05cb9a5b9f51404c79381c648fa"),
    SCHEMA: ("275a86286480f915af69e18d81d7032140e3db6982d32679206a6a5b88fee036", None),
    CONTRACT: ("ee2a969b5d3ae28dfc116fc24ab6bee6c3983d64db183641981108481c05ae7d",
               "fe82dcf80e8dd856390b694e8a286abc3087f33d0a2b4bebda1a01836b796a6b"),
    PRODUCER: ("587933a52505488fd87b1c4f99d5659df6f3c3e9557c0a77edd642e6e4dde0ab", None),
    CONSUMER: ("d66143d32f4c4257041f03e24e4a4da8f15542853b2a8f47fa39f5b72871bfdd", None),
    TRANSITION: ("d2c0a78db1ae19ccb21f068c4c4f9337220cabbf16721fdc15ed41825a6f3374",
                 "fabe51379dc16bd4177d2116a43f2d1d5c103cc5a53f845fd5397eae0ea1c25b"),
    AUDIT: ("b7c3732296df713b6588527284983fab758e225c17c51fbc4a38b1f43da8aece",
            "2ef7588e66a83944fee0e2044177445f15b71fe030871ca96f354ce65dc8499a"),
}
EXACT8 = (REJECTION, SCHEMA, CONTRACT, PRODUCER, CONSUMER, TRANSITION, AUDIT, SELF)
INNER_SCHEMA = "cm2.round306c79g.true-global-no-producer-consumer.v3.inner-composite"
COLD_ROOT_SCHEMA = (
    "cm2.round306c79g.true-global-no-producer-consumer.v3."
    "cold-launched-committed-authority"
)
COLD_ROOT_DOMAIN = b"CM2_C79G_V3_COLD_LAUNCHED_AUTHORITY_ROOT_V1\0"
LIVE_PROTOCOL = "CM2_C79G_V3_COLD_TWO_PHASE_LIVE_ACK_V1"
LIVE_REQUEST_SCHEMA = (
    "cm2.round306c79g.true-global-no-producer-consumer.v3."
    "cold-live-commit-request"
)
LIVE_ACK_SCHEMA = (
    "cm2.round306c79g.true-global-no-producer-consumer.v3.cold-live-ack"
)
LIVE_RELEASE_SCHEMA = (
    "cm2.round306c79g.true-global-no-producer-consumer.v3.cold-live-release"
)
PREWRAPPER_BODY_DOMAIN = "CM2_C79G_V3_COLD_PREWRAPPER_BODY_V1"
TRANSACTION_BINDING_DOMAIN = "CM2_C79G_V3_COLD_TRANSACTION_BINDING_V1"
LIVE_ACK_BINDING_DOMAIN = "CM2_C79G_V3_COLD_LIVE_ACK_BINDING_V1"
SOURCE_FD_ENV = "CM2_C79G_V3_COLD_SOURCE_FD"
COORDINATION_PARENT_FD_ENV = "CM2_C79G_V3_COORDINATION_PARENT_FD"
WORKSPACE_ROOT_ENV = "CM2_C79G_V3_COLD_WORKSPACE_ROOT"
LAUNCHER_SHA_ENV = "CM2_C79G_V3_COLD_LAUNCHER_FILE_SHA256"


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def sha_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def close_object(value: dict[str, Any]) -> dict[str, Any]:
    need("object_sha256" not in value, "object closes exactly once")
    out = copy.deepcopy(value)
    out["object_sha256"] = sha_bytes(canonical(value))
    return out


def strict_json(raw: bytes, label: str) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(key not in result, label + ":duplicate key:" + key)
            result[key] = value
        return result
    try:
        return json.loads(
            raw, object_pairs_hook=pairs,
            parse_constant=lambda token: (_ for _ in ()).throw(
                Reject(label + ":non-finite:" + token)))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Reject(label + ":strict JSON") from exc


def verify_object(value: Mapping[str, Any], label: str,
                  expected: str | None = None) -> None:
    body = copy.deepcopy(dict(value))
    claim = body.pop("object_sha256", None)
    need(isinstance(claim, str) and claim == sha_bytes(canonical(body)),
         label + ":object closure")
    if expected is not None:
        need(claim == expected, label + ":object pin")


AT_EMPTY_PATH = 0x1000
AT_SYMLINK_NOFOLLOW = 0x100
STATX_BASIC_STATS = 0x000007ff
STATX_MNT_ID = 0x00001000
RESOLVE_NO_XDEV = 0x01
RESOLVE_NO_MAGICLINKS = 0x02
RESOLVE_NO_SYMLINKS = 0x04
RESOLVE_BENEATH = 0x08


class OpenHow(ctypes.Structure):
    _fields_ = [("flags", ctypes.c_uint64), ("mode", ctypes.c_uint64),
                ("resolve", ctypes.c_uint64)]


class StatxTimestamp(ctypes.Structure):
    _fields_ = [("tv_sec", ctypes.c_int64), ("tv_nsec", ctypes.c_uint32),
                ("reserved", ctypes.c_int32)]


class Statx(ctypes.Structure):
    _fields_ = [
        ("stx_mask", ctypes.c_uint32), ("stx_blksize", ctypes.c_uint32),
        ("stx_attributes", ctypes.c_uint64), ("stx_nlink", ctypes.c_uint32),
        ("stx_uid", ctypes.c_uint32), ("stx_gid", ctypes.c_uint32),
        ("stx_mode", ctypes.c_uint16), ("spare0", ctypes.c_uint16),
        ("stx_ino", ctypes.c_uint64), ("stx_size", ctypes.c_uint64),
        ("stx_blocks", ctypes.c_uint64), ("stx_attributes_mask", ctypes.c_uint64),
        ("stx_atime", StatxTimestamp), ("stx_btime", StatxTimestamp),
        ("stx_ctime", StatxTimestamp), ("stx_mtime", StatxTimestamp),
        ("stx_rdev_major", ctypes.c_uint32), ("stx_rdev_minor", ctypes.c_uint32),
        ("stx_dev_major", ctypes.c_uint32), ("stx_dev_minor", ctypes.c_uint32),
        ("stx_mnt_id", ctypes.c_uint64), ("stx_dio_mem_align", ctypes.c_uint32),
        ("stx_dio_offset_align", ctypes.c_uint32),
        ("spare3", ctypes.c_uint64 * 12),
    ]


def _libc() -> ctypes.CDLL:
    need(sys.platform.startswith("linux"), "cold launcher is Linux fail-closed")
    library = ctypes.CDLL(None, use_errno=True)
    need(hasattr(library, "syscall") and hasattr(library, "statx"),
         "openat2 and statx required")
    return library


def _relative(path: Path) -> bytes:
    absolute = Path(os.path.abspath(path))
    need(absolute != ROOT and ROOT in absolute.parents and not path.is_symlink(),
         "exact nonsymlink workspace path:" + str(path))
    relative = absolute.relative_to(ROOT)
    need(relative.parts and all(part not in {"", ".", ".."} for part in relative.parts),
         "clean relative path:" + str(path))
    return os.fsencode(str(relative))


def openat2_beneath(path: Path, flags: int = os.O_RDONLY) -> int:
    root_fd = os.open(ROOT, getattr(os, "O_PATH", os.O_RDONLY) |
                      os.O_DIRECTORY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0))
    try:
        how = OpenHow(flags | os.O_CLOEXEC, 0,
                      RESOLVE_NO_XDEV | RESOLVE_NO_MAGICLINKS |
                      RESOLVE_NO_SYMLINKS | RESOLVE_BENEATH)
        ctypes.set_errno(0)
        descriptor = _libc().syscall(
            ctypes.c_long(437), ctypes.c_int(root_fd),
            ctypes.c_char_p(_relative(path)), ctypes.byref(how),
            ctypes.c_size_t(ctypes.sizeof(how)))
        if descriptor < 0:
            code = ctypes.get_errno()
            raise Reject("openat2 fail closed:" + str(path) + ":" + os.strerror(code))
        return int(descriptor)
    finally:
        os.close(root_fd)


def mount_id(fd: int) -> int:
    info = Statx()
    ctypes.set_errno(0)
    outcome = _libc().statx(
        ctypes.c_int(fd), ctypes.c_char_p(b""),
        ctypes.c_int(AT_EMPTY_PATH | AT_SYMLINK_NOFOLLOW),
        ctypes.c_uint(STATX_BASIC_STATS | STATX_MNT_ID), ctypes.byref(info))
    if outcome != 0:
        code = ctypes.get_errno()
        raise Reject("statx fail closed:" + os.strerror(code))
    need(bool(info.stx_mask & STATX_MNT_ID), "statx mount id unavailable")
    return int(info.stx_mnt_id)


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns)


def cold_publication_chronology(
        exact8: list[os.stat_result], manifest: os.stat_result,
        outer: os.stat_result) -> dict[str, bool]:
    """Prove final chmod/freeze order, not merely content-write mtime order."""
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


def directory_identity(value: os.stat_result) -> tuple[int, int, int]:
    return (value.st_dev, value.st_ino, value.st_mode)


class HeldFile:
    def __init__(self, path: Path, label: str, expected: str | None = None) -> None:
        self.path = path
        self.label = label
        before_path = path.lstat()
        need(stat.S_ISREG(before_path.st_mode) and not path.is_symlink() and
             stat.S_IMODE(before_path.st_mode) == 0o444 and before_path.st_nlink == 1,
             label + ":regular 0444 nlink1")
        self.fd = openat2_beneath(path)
        self.before = os.fstat(self.fd)
        self.mount_id = mount_id(self.fd)
        need(directory_identity(before_path) == directory_identity(self.before),
             label + ":initial path/fd identity")
        self.raw = self._read()
        after_fd = os.fstat(self.fd)
        after_path = path.lstat()
        need(fingerprint(before_path) == fingerprint(self.before) ==
             fingerprint(after_fd) == fingerprint(after_path) and
             mount_id(self.fd) == self.mount_id,
             label + ":initial bracketed same-fd read")
        self.file_sha256 = sha_bytes(self.raw)
        if expected is not None:
            need(self.file_sha256 == expected, label + ":file pin")

    @property
    def identity(self) -> tuple[int, int]:
        return (self.before.st_dev, self.before.st_ino)

    def _read(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        chunks: list[bytes] = []
        while True:
            chunk = os.read(self.fd, 1 << 20)
            if not chunk:
                return b"".join(chunks)
            chunks.append(chunk)

    def terminal_replay(self) -> None:
        before_fd = os.fstat(self.fd)
        before_path = self.path.lstat()
        replay = self._read()
        after_fd = os.fstat(self.fd)
        after_path = self.path.lstat()
        need(replay == self.raw and
             fingerprint(before_fd) == fingerprint(before_path) ==
             fingerprint(self.before) == fingerprint(after_fd) ==
             fingerprint(after_path) and
             stat.S_ISREG(after_fd.st_mode) and
             stat.S_IMODE(after_fd.st_mode) == 0o444 and after_fd.st_nlink == 1 and
             mount_id(self.fd) == self.mount_id,
             self.label + ":terminal bracketed same-fd replay")

    def identity_object(self) -> dict[str, Any]:
        return {
            "path": str(self.path.relative_to(ROOT)),
            "file_sha256": self.file_sha256,
            "st_dev": self.before.st_dev,
            "st_ino": self.before.st_ino,
            "stx_mnt_id": self.mount_id,
            "st_size": self.before.st_size,
            "mode": "0444",
            "nlink": 1,
            "opened_by_exact_lexical_path_with_O_NOFOLLOW": True,
            "opened_with_openat2_RESOLVE_BENEATH_NO_SYMLINKS_NO_MAGICLINKS_NO_XDEV": True,
            "statx_mount_id_stable": True,
            "initial_fd_identity_equals_terminal_fd_identity": True,
            "initial_bytes_equal_terminal_same_fd_bytes": True,
            "terminal_fd_identity_equals_terminal_path_lstat_identity": True,
            "parent_components_securely_walked": True,
            "regular_file": True,
        }

    def close(self) -> None:
        os.close(self.fd)


class HeldCoordinationParent:
    """Launcher-owned official-writer lock on the exact RUNTIME dir inode.

    The same open-file-description is inherited by every child.  Keeping this
    launcher descriptor open prevents a child crash after the final dynamic
    ACK from releasing the lock before the positive wrapper's final newline is
    committed through the raw blocking stdout pipe.
    This is a mandatory cooperative protocol lock; it is deliberately not
    described as isolation from a same-UID process that ignores the protocol.
    """

    def __init__(self) -> None:
        self.path = RUNTIME
        before_path = self.path.lstat()
        need(stat.S_ISDIR(before_path.st_mode) and not self.path.is_symlink(),
             "coordination parent exact nonsymlink directory")
        self.fd = openat2_beneath(
            self.path, os.O_RDONLY | os.O_DIRECTORY)
        self.before = os.fstat(self.fd)
        self.mount_id = mount_id(self.fd)
        need(fingerprint(before_path) == fingerprint(self.before),
             "coordination parent initial path/fd identity")
        fcntl.flock(self.fd, fcntl.LOCK_EX)
        self.lock_owned = True
        self.verify()

    @property
    def identity(self) -> tuple[int, int]:
        return (self.before.st_dev, self.before.st_ino)

    def verify(self) -> None:
        before_fd = os.fstat(self.fd)
        before_path = self.path.lstat()
        fcntl.flock(self.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        after_fd = os.fstat(self.fd)
        after_path = self.path.lstat()
        need(self.lock_owned and
             stat.S_ISDIR(before_fd.st_mode) and stat.S_ISDIR(after_fd.st_mode) and
             directory_identity(before_fd) == directory_identity(before_path) ==
             directory_identity(self.before) == directory_identity(after_fd) ==
             directory_identity(after_path) and mount_id(self.fd) == self.mount_id,
             "launcher-owned coordination lock and parent identity stable")

    def identity_object(self) -> dict[str, Any]:
        return {
            "path": str(self.path.relative_to(ROOT)),
            "st_dev": self.before.st_dev,
            "st_ino": self.before.st_ino,
            "stx_mnt_id": self.mount_id,
            "directory": True,
            "opened_with_openat2_RESOLVE_BENEATH_NO_SYMLINKS_NO_MAGICLINKS_NO_XDEV": True,
            "launcher_owned_flock_LOCK_EX": self.lock_owned,
            "same_open_file_description_inherited_by_child": True,
            "lock_scope_is_mandatory_official_writer_protocol_only": True,
            "same_uid_bypass_is_not_claimed_prevented": True,
        }

    def close(self) -> None:
        if self.lock_owned:
            fcntl.flock(self.fd, fcntl.LOCK_UN)
            self.lock_owned = False
        os.close(self.fd)


class HeldEmptyRejectionNamespace:
    """Launcher-level permanent-rejection guard for every non-reject command."""
    def __init__(self, coordination: HeldCoordinationParent) -> None:
        coordination.verify()
        name = REJECTION_NAMESPACE.name
        created_descriptor = -1
        try:
            state = os.stat(name, dir_fd=coordination.fd, follow_symlinks=False)
        except FileNotFoundError:
            os.mkdir(name, 0o555, dir_fd=coordination.fd)
            created_descriptor = os.open(
                name, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC |
                getattr(os, "O_NOFOLLOW", 0), dir_fd=coordination.fd)
            os.fchmod(created_descriptor, 0o555)
            os.fsync(created_descriptor)
            os.fsync(coordination.fd)
            state = os.stat(name, dir_fd=coordination.fd, follow_symlinks=False)
        self.path = REJECTION_NAMESPACE
        self.fd = created_descriptor if created_descriptor >= 0 else openat2_beneath(
            self.path, os.O_RDONLY | os.O_DIRECTORY)
        self.before = os.fstat(self.fd)
        self.mount_id = mount_id(self.fd)
        path_before = self.path.lstat()
        first = set(os.listdir(self.fd))
        after = os.fstat(self.fd)
        path_after = self.path.lstat()
        second = set(os.listdir(self.fd))
        need(stat.S_ISDIR(state.st_mode) and
             stat.S_IMODE(state.st_mode) == 0o555 and state.st_nlink == 2 and
             fingerprint(state) == fingerprint(self.before) ==
                 fingerprint(path_before) == fingerprint(after) ==
                 fingerprint(path_after) and
             first == second == set() and
             self.mount_id == coordination.mount_id,
             "launcher permanent-rejection namespace exact empty sealed state")

    def terminal_replay(self) -> None:
        before = os.fstat(self.fd)
        path_before = self.path.lstat()
        first = set(os.listdir(self.fd))
        after = os.fstat(self.fd)
        path_after = self.path.lstat()
        second = set(os.listdir(self.fd))
        need(fingerprint(before) == fingerprint(path_before) ==
             fingerprint(self.before) == fingerprint(after) ==
             fingerprint(path_after) and first == second == set() and
             stat.S_IMODE(after.st_mode) == 0o555 and after.st_nlink == 2 and
             mount_id(self.fd) == self.mount_id,
             "launcher rejection namespace terminal exact-empty replay")

    def close(self) -> None:
        os.close(self.fd)


def parse_manifest(raw: bytes) -> list[dict[str, str]]:
    need(raw.endswith(b"\n"), "cold manifest terminal newline")
    result: list[dict[str, str]] = []
    seen: set[str] = set()
    for line in raw.decode("ascii").splitlines():
        parts = line.split("  ", 1)
        need(len(parts) == 2 and re.fullmatch(r"[0-9a-f]{64}", parts[0]) is not None and
             parts[1] not in seen, "cold manifest exact line")
        seen.add(parts[1])
        result.append({"path": parts[1], "file_sha256": parts[0]})
    return result


class HeldBundle:
    def __init__(self, expected_launcher_sha256: str) -> None:
        need(SELF == OUT / (BASE + "_cold_launch_v3.py"),
             "exact cold launcher path")
        for path, (file_pin, object_pin) in BASE7_PINS.items():
            need(re.fullmatch(r"[0-9a-f]{64}", file_pin) is not None and
                 file_pin != "0" * 64 and
                 (object_pin is None or
                  (re.fullmatch(r"[0-9a-f]{64}", object_pin) is not None and
                   object_pin != "0" * 64)),
                 "all embedded base7 pins final")
        need(re.fullmatch(r"[0-9a-f]{64}", expected_launcher_sha256) is not None and
             expected_launcher_sha256 != "0" * 64,
             "caller-supplied sole external launcher SHA-256 anchor")
        # Trust flows only from the externally pinned launcher and its embedded
        # base-seven pins.  The later manifest and outer are reconstructed from
        # those already-held bytes; neither is an independent caller input.
        self.files = [
            HeldFile(
                path, "cold exact8:" + path.name,
                expected_launcher_sha256 if path == SELF else BASE7_PINS[path][0])
            for path in EXACT8
        ]
        self.by_path = {guard.path: guard for guard in self.files}
        need(expected_launcher_sha256 == self.by_path[SELF].file_sha256,
             "sole external launcher SHA-256 equals held SELF")
        for path, (file_pin, _) in BASE7_PINS.items():
            need(self.by_path[path].file_sha256 == file_pin,
                 "embedded base7 file pin:" + path.name)
        expected_entries = [
            {"path": str(path.relative_to(ROOT)),
             "file_sha256": self.by_path[path].file_sha256}
            for path in EXACT8
        ]
        expected_manifest_raw = b"".join(
            (entry["file_sha256"] + "  " + entry["path"] + "\n").encode("ascii")
            for entry in expected_entries
        )
        self.manifest = HeldFile(MANIFEST, "cold exact8 manifest")
        need(self.manifest.raw == expected_manifest_raw,
             "cold manifest byte-identical to reconstructed ordered exact8")
        entries = parse_manifest(self.manifest.raw)
        need(entries == expected_entries, "cold manifest exact ordered eight")
        self.outer = HeldFile(OUTER, "cold outer-last")
        exact10 = [*self.files, self.manifest, self.outer]
        need(len(exact10) == 10 and len({item.identity for item in exact10}) == 10 and
             len({item.mount_id for item in exact10}) == 1,
             "cold exact10 identities globally unique on one mount")
        self.chronology = cold_publication_chronology(
            [item.before for item in self.files],
            self.manifest.before, self.outer.before)
        need(all(self.chronology.values()),
             "physical exact8 freeze then manifest freeze then outer freeze chronology")
        self.entries = entries
        self.schema = strict_json(self.by_path[SCHEMA].raw, "closed schema")
        need(isinstance(self.schema, dict) and
             self.schema.get("$ref") == "#/$defs/coldLaunchedCommittedAuthority",
             "closed schema has cold-launched root only")
        for path in (REJECTION, CONTRACT, TRANSITION, AUDIT):
            value = strict_json(self.by_path[path].raw, "cold object:" + path.name)
            need(isinstance(value, dict), "cold base JSON object:" + path.name)
            verify_object(value, path.name, BASE7_PINS[path][1])
        self.outer_object = strict_json(self.outer.raw, "cold outer-last")
        need(isinstance(self.outer_object, dict), "cold outer JSON object")
        verify_object(self.outer_object, "cold outer-last")
        need(set(self.outer_object) == {
                 "schema", "status", "effective_checkpoint_object_sha256",
                 "exact8_ordered_entries", "cold_launch_manifest", "cold_launcher",
                 "all_exact8_regular_0444_nlink1_and_held_for_runtime",
                 "outer_published_after_exact8_manifest",
                 "runtime_entry_must_be_cold_launcher",
                 "sole_external_trust_anchor_is_launcher_sha256",
                 "formal_global_closure_credit", "D02_unlock",
                 "runtime_executed_during_static_freeze", "object_sha256"} and
             self.outer.raw == canonical(self.outer_object) + b"\n" and
             self.outer_object.get("schema") ==
                 "cm2.round306c79g.true-global-no-producer-consumer."
                 "cold-launch-outer-receipt.v3" and
             self.outer_object.get("status") ==
                 "FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED" and
             self.outer_object.get("effective_checkpoint_object_sha256") == CHECKPOINT and
             self.outer_object.get("exact8_ordered_entries") == entries and
             self.outer_object.get("cold_launch_manifest") == {
                 "path": str(MANIFEST.relative_to(ROOT)),
                 "file_sha256": self.manifest.file_sha256,
                 "ordered_entry_count": 8,
             } and
             self.outer_object.get("cold_launcher") == {
                 "path": str(SELF.relative_to(ROOT)),
                 "file_sha256": self.by_path[SELF].file_sha256,
             } and
             self.outer_object.get("all_exact8_regular_0444_nlink1_and_held_for_runtime") is True and
             self.outer_object.get("outer_published_after_exact8_manifest") is True and
             self.outer_object.get("runtime_entry_must_be_cold_launcher") is True and
             self.outer_object.get("sole_external_trust_anchor_is_launcher_sha256") is True and
             self.outer_object.get("formal_global_closure_credit") == 0 and
             self.outer_object.get("D02_unlock") is False and
             self.outer_object.get("runtime_executed_during_static_freeze") is False,
             "cold outer-last exact closure")

    def terminal_replay(self) -> None:
        for guard in [*self.files, self.manifest, self.outer]:
            guard.terminal_replay()
        terminal_chronology = cold_publication_chronology(
            [item.before for item in self.files],
            self.manifest.before, self.outer.before)
        need(terminal_chronology == self.chronology and
             all(terminal_chronology.values()),
             "terminal cold freeze chronology unchanged")

    def close(self) -> None:
        for guard in [*self.files, self.manifest, self.outer]:
            guard.close()


def _type_matches(value: Any, type_name: str) -> bool:
    return {
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
        "integer": type(value) is int,
        "number": type(value) in {int, float},
        "boolean": type(value) is bool,
        "null": value is None,
    }.get(type_name, False)


def validate_schema(value: Any, node: Mapping[str, Any], root: Mapping[str, Any],
                    label: str) -> None:
    if "$ref" in node:
        reference = node["$ref"]
        need(isinstance(reference, str) and reference.startswith("#/$defs/"),
             label + ":local ref only")
        name = reference.removeprefix("#/$defs/")
        target = root.get("$defs", {}).get(name)
        need(isinstance(target, dict), label + ":resolved ref:" + name)
        validate_schema(value, target, root, label + "->" + name)
        return
    if "const" in node:
        expected = node["const"]
        need(type(value) is type(expected) and value == expected, label + ":const")
    type_name = node.get("type")
    if type_name is not None:
        need(isinstance(type_name, str) and _type_matches(value, type_name),
             label + ":type:" + str(type_name))
    if isinstance(value, dict):
        required = node.get("required", [])
        need(isinstance(required, list) and all(key in value for key in required),
             label + ":required")
        properties = node.get("properties", {})
        need(isinstance(properties, dict), label + ":properties")
        if node.get("additionalProperties") is False:
            need(set(value) <= set(properties), label + ":additionalProperties")
        for key, child in properties.items():
            if key in value:
                need(isinstance(child, dict), label + ":child schema")
                validate_schema(value[key], child, root, label + "." + key)
    if isinstance(value, list):
        if "minItems" in node:
            need(len(value) >= node["minItems"], label + ":minItems")
        if "maxItems" in node:
            need(len(value) <= node["maxItems"], label + ":maxItems")
        if node.get("uniqueItems") is True:
            need(len({canonical(item) for item in value}) == len(value),
                 label + ":uniqueItems")
        prefix = node.get("prefixItems", [])
        need(isinstance(prefix, list), label + ":prefixItems")
        for index, child_schema in enumerate(prefix[:len(value)]):
            need(isinstance(child_schema, dict), label + ":prefix schema")
            validate_schema(value[index], child_schema, root, f"{label}[{index}]")
        if len(value) > len(prefix):
            item_schema = node.get("items")
            need(item_schema is not False, label + ":items false")
            if item_schema is not None:
                need(isinstance(item_schema, dict), label + ":items schema")
                for index in range(len(prefix), len(value)):
                    validate_schema(value[index], item_schema, root,
                                    f"{label}[{index}]")
    if isinstance(value, str):
        if "minLength" in node:
            need(len(value) >= node["minLength"], label + ":minLength")
        if "pattern" in node:
            need(re.search(node["pattern"], value) is not None, label + ":pattern")
    if type(value) in {int, float} and "minimum" in node:
        need(value >= node["minimum"], label + ":minimum")


def child_environment(bundle: HeldBundle, source: HeldFile,
                      coordination: HeldCoordinationParent) -> dict[str, str]:
    return {
        "LC_ALL": "C",
        "TZ": "UTC",
        SOURCE_FD_ENV: str(source.fd),
        COORDINATION_PARENT_FD_ENV: str(coordination.fd),
        WORKSPACE_ROOT_ENV: str(ROOT),
        LAUNCHER_SHA_ENV: bundle.by_path[SELF].file_sha256,
    }


def child_argv(source: HeldFile, command: str,
               forwarded: list[str]) -> list[str]:
    return [sys.executable, "-I", "-B", "-S",
            "/proc/self/fd/" + str(source.fd), command, *forwarded]


def run_non_authorize_child(
        bundle: HeldBundle, coordination: HeldCoordinationParent,
        rejection_guard: HeldEmptyRejectionNamespace | None,
        command: str, forwarded: list[str]) -> bytes:
    need((command == "reject") == (rejection_guard is None),
         "reject is the sole command exempt from the exact-empty namespace guard")
    source = bundle.by_path[PRODUCER if command == "build" else CONSUMER]
    completed = subprocess.run(
        child_argv(source, command, forwarded),
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=child_environment(bundle, source, coordination),
        pass_fds=(source.fd, coordination.fd), check=False)
    if completed.stderr:
        sys.stderr.buffer.write(completed.stderr)
    need(completed.returncode == 0, "cold child rejected or failed")
    bundle.terminal_replay()
    if rejection_guard is not None:
        rejection_guard.terminal_replay()
    coordination.verify()
    return completed.stdout


def cold_root(bundle: HeldBundle, coordination: HeldCoordinationParent,
              inner_raw: bytes) -> tuple[dict[str, Any], dict[str, Any]]:
    need(inner_raw.endswith(b"\n") and inner_raw.count(b"\n") == 1,
         "authorize child first stdout is exactly one JSON line")
    inner = strict_json(inner_raw, "zero-credit inner live composite")
    need(isinstance(inner, dict), "inner live composite object")
    verify_object(inner, "inner live composite")
    validate_schema(inner, {"$ref": "#/$defs/innerComposite"}, bundle.schema, "inner")
    need(inner.get("schema") == INNER_SCHEMA and
         inner.get("formal_global_closure_credit") == 0 and
         inner.get("D02_unlock") is False and
         inner.get("cold_launcher_required") is True and
         inner_raw == canonical(inner) + b"\n",
         "direct consumer result is canonical launcher-required zero-only inner")
    proof = {
        "launcher_identity": bundle.by_path[SELF].identity_object(),
        "manifest_identity": bundle.manifest.identity_object(),
        "outer_identity": bundle.outer.identity_object(),
        "ordered_exact8_identities": [bundle.by_path[path].identity_object()
                                       for path in EXACT8],
        "exact10_identity_count": 10,
        "all_exact10_identities_globally_unique_on_one_statx_mount": True,
        **bundle.chronology,
        "external_launcher_file_sha256_pin_required": True,
        "external_launcher_file_sha256_equals_held_launcher": True,
        "sole_external_launcher_sha256_is_only_external_static_anchor": True,
        "manifest_and_outer_reconstructed_without_independent_external_hash": True,
        "child_source_path": str(CONSUMER.relative_to(ROOT)),
        "child_source_file_sha256": bundle.by_path[CONSUMER].file_sha256,
        "child_source_executed_from_held_exact8_fd": True,
        "child_python_isolated_no_site_and_no_pyc": True,
        "child_first_stdout_exact_one_canonical_inner_object": True,
        "inner_validated_against_closed_innerComposite_schema": True,
        "cold_outer_object_sha256": bundle.outer_object["object_sha256"],
        "official_writer_coordination_parent": coordination.identity_object(),
        "launcher_owned_coordination_lock_acquired_before_child_spawn": True,
        "coordination_lock_passed_as_same_open_file_description": True,
        "coordination_lock_is_mandatory_for_official_writers_only": True,
        "launcher_empty_rejection_namespace_guard_held_from_before_child_spawn_and_terminally_replayed_before_final_dynamic_request": True,
        "same_uid_or_filesystem_administrator_bypass_not_claimed_prevented": True,
        "cold_two_phase_live_protocol": LIVE_PROTOCOL,
        "wrapper_closed_and_schema_validated_before_request": True,
        "wrapper_body_excludes_transaction_binding_request_ACK_and_RELEASE_to_avoid_hash_cycle": True,
        "transaction_binding_is_replay_identical_not_fresh_or_random": True,
        "terminal_exact10_replay_completed_before_final_dynamic_request": True,
        "final_dynamic_ack_bound_to_inner_and_final_wrapper_object": True,
        "final_dynamic_ack_requires_full_replay_and_fresh_rejection_scan": True,
        "launcher_lock_survives_child_exit_or_crash_until_wrapper_raw_final_newline_commit": True,
        "no_fallible_schema_or_filesystem_gate_after_validated_ack": True,
        "positive_wrapper_stdout_fd1_blocking_pipe_preflushed_and_duplicated_before_dynamic_request": True,
        "positive_wrapper_raw_fd1_final_newline_write_is_semantic_commit": True,
        "post_ACK_release_and_child_exit_are_non_authority_cleanup": True,
    }
    authority_root_sha256 = sha_bytes(COLD_ROOT_DOMAIN + canonical({
        "inner_object_sha256": inner["object_sha256"],
        "manifest_file_sha256": bundle.manifest.file_sha256,
        "outer_file_sha256": bundle.outer.file_sha256,
        "outer_object_sha256": bundle.outer_object["object_sha256"],
        "launcher_file_sha256": bundle.by_path[SELF].file_sha256,
        "coordination_parent_st_dev": coordination.before.st_dev,
        "coordination_parent_st_ino": coordination.before.st_ino,
        "coordination_parent_statx_mnt_id": coordination.mount_id,
    }))
    root = close_object({
        "schema": COLD_ROOT_SCHEMA,
        "status": "GO_COLD_LAUNCHED_LIVE_COMPOSITE_ONLY",
        "authority_decision": "GO_COLD_LAUNCHED_COMPOSITE_ONLY",
        "effective_checkpoint_object_sha256": CHECKPOINT,
        "inner_composite": inner,
        "cold_launch_proof": proof,
        "preseal_root_sha256": inner["preseal_root_sha256"],
        "inner_authority_root_sha256": inner["authority_root_sha256"],
        "authority_root_domain": COLD_ROOT_DOMAIN[:-1].decode("ascii"),
        "authority_root_sha256": authority_root_sha256,
        "formal_global_closure_credit": 1,
        "D02_unlock": True,
        "D02_gate_credit": 0,
        "D02_task_credit": 0,
        "D02_formal_pending_task_count": 33_638,
        "D02_started": False,
        "root_is_virtual_and_must_not_be_persisted": True,
    })
    validate_schema(root, bundle.schema, bundle.schema, "cold-root")
    return root, inner


def _read_child_line(pipe: Any, label: str) -> bytes:
    maximum = 32 * 1024 * 1024
    raw = pipe.readline(maximum + 1)
    need(raw.endswith(b"\n") and len(raw) <= maximum and raw.count(b"\n") == 1,
         label + ":one bounded newline-terminated object")
    return raw


def _wrapper_body_domain_sha256(root: Mapping[str, Any]) -> str:
    body = {key: value for key, value in root.items() if key != "object_sha256"}
    return sha_bytes(PREWRAPPER_BODY_DOMAIN.encode("ascii") + b"\x00" +
                     canonical(body))


def _deterministic_transaction_binding(
        bundle: HeldBundle, inner_object_sha256: str,
        wrapper_body_domain_sha256: str,
        wrapper_object_sha256: str) -> str:
    # This value prevents private-pipe transaction mixups.  It is intentionally
    # deterministic and is not represented as a freshness or randomness claim.
    return sha_bytes(
        TRANSACTION_BINDING_DOMAIN.encode("ascii") + b"\x00" +
        inner_object_sha256.encode("ascii") +
        wrapper_body_domain_sha256.encode("ascii") +
        wrapper_object_sha256.encode("ascii") +
        bundle.by_path[SELF].file_sha256.encode("ascii"))


def _expected_ack_binding(request: Mapping[str, Any]) -> str:
    return sha_bytes(
        LIVE_ACK_BINDING_DOMAIN.encode("ascii") + b"\x00" +
        request["transaction_binding_sha256"].encode("ascii") +
        request["inner_object_sha256"].encode("ascii") +
        request["wrapper_body_domain_sha256"].encode("ascii") +
        request["wrapper_object_sha256"].encode("ascii") +
        request["object_sha256"].encode("ascii"))


def _validate_lock_ack(value: Any,
                       coordination: HeldCoordinationParent) -> None:
    need(isinstance(value, dict) and set(value) == {
             "path", "held_parent_st_dev", "held_parent_st_ino",
             "held_parent_statx_mnt_id", "lock_api",
             "received_from_frozen_launcher_as_inherited_open_file_description_fd",
             "child_duplicated_and_identity_mount_checked_inherited_fd",
             "child_calls_LOCK_UN",
             "launcher_lock_owner_scope_requirement_includes_child_live_protocol",
             "mandatory_for_all_official_runtime_writers",
             "acquired_before_any_runtime_evidence_or_commit_surface_open_for_this_command",
             "required_final_hold_scope",
             "protocol_requires_launcher_RELEASE_before_normal_child_guard_close",
             "coordination_lock_is_not_claimed_as_a_security_boundary_against_noncooperating_same_uid_or_filesystem_administrator",
             "launcher_exclusive_lock_confirmed_by_independent_nonblocking_probe",
         } and
         value.get("path") == str(RUNTIME.relative_to(ROOT)) and
         value.get("held_parent_st_dev") == coordination.before.st_dev and
         value.get("held_parent_st_ino") == coordination.before.st_ino and
         value.get("held_parent_statx_mnt_id") == coordination.mount_id and
         value.get("lock_api") == "launcher_owned_fcntl.flock(LOCK_EX)" and
         value.get("received_from_frozen_launcher_as_inherited_open_file_description_fd") is True and
         value.get("child_duplicated_and_identity_mount_checked_inherited_fd") is True and
         value.get("child_calls_LOCK_UN") is False and
         value.get("launcher_lock_owner_scope_requirement_includes_child_live_protocol") is True and
         value.get("mandatory_for_all_official_runtime_writers") is True and
         value.get("acquired_before_any_runtime_evidence_or_commit_surface_open_for_this_command") is True and
         value.get("required_final_hold_scope") == [
             "inner_canonical_stdout_flush", "launcher_commit_request",
             "absolute_last_dynamic_terminal_replay",
             "live_ACK_canonical_stdout_flush",
             "launcher_positive_wrapper_raw_fd1_final_newline_write", "launcher_RELEASE"] and
         value.get("protocol_requires_launcher_RELEASE_before_normal_child_guard_close") is True and
         value.get("coordination_lock_is_not_claimed_as_a_security_boundary_against_noncooperating_same_uid_or_filesystem_administrator") is True and
         value.get("launcher_exclusive_lock_confirmed_by_independent_nonblocking_probe") is True,
         "live ACK exact launcher-owned official-writer lock proof")


def _validate_live_ack(
        raw: bytes, request: Mapping[str, Any],
        coordination: HeldCoordinationParent) -> dict[str, Any]:
    ack = strict_json(raw, "cold final-dynamic live ACK")
    need(isinstance(ack, dict), "cold live ACK object")
    verify_object(ack, "cold final-dynamic live ACK")
    expected_keys = {
        "schema", "status", "protocol", "transaction_binding_domain",
        "transaction_binding_sha256",
        "request_object_sha256", "inner_object_sha256",
        "wrapper_body_domain", "wrapper_body_domain_sha256",
        "wrapper_object_sha256", "ack_binding_domain", "ack_binding_sha256",
        "official_writer_coordination_lock", "final_dynamic_replay_census",
        "all_dynamic_conjuncts_live",
        "wrapper_closed_and_schema_validated_before_request",
        "wrapper_body_excludes_transaction_binding_request_ACK_and_RELEASE_to_avoid_hash_cycle",
        "transaction_binding_is_replay_identical_not_fresh_or_random",
        "static_cold_exact10_terminal_replay_completed_by_launcher_before_request",
        "launcher_empty_rejection_namespace_guard_terminally_replayed_before_request",
        "positive_wrapper_emitted_by_combined_child",
        "release_required_before_dynamic_guards_close",
        "positive_wrapper_raw_fd1_final_newline_write_is_launcher_semantic_commit",
        "post_ACK_RELEASE_and_child_exit_are_non_authority_cleanup",
        "formal_global_closure_credit", "D02_unlock", "object_sha256",
    }
    expected_census = {
        "C78l_C78s_held_file_count": 51,
        "C78l_C78s_held_directory_count": 5,
        "C55_C72_fixed_held_file_count_excluding_shared_head": 16,
        "shared_C72G_C53_head_held_via_C42_full10_count": 1,
        "frozen_v2_readable_held_file_count": 4,
        "frozen_v2_source_metadata_only_held_count": 2,
        "current_producer_metadata_only_held_count": 1,
        "consumer_SELF_held_count": 1,
        "public_candidate_verification_completion_held_file_count": 24,
        "public_candidate_verification_completion_held_directory_count": 5,
        "C42_full10_union_candidate9_held_file_count": 16,
        "C42_candidate_held_directory_count": 1,
        "authority_seal_held_file_count": 1,
        "static_policy_held_file_count": 8,
        "terminal_deterministic_stage_absence_count": 5,
        "fresh_rejection_namespace_scan_count": 1,
    }
    need(set(ack) == expected_keys and ack.get("schema") == LIVE_ACK_SCHEMA and
         ack.get("status") ==
             "ACK_FINAL_DYNAMIC_CONJUNCTS_LIVE__ZERO_CREDIT__AWAIT_POSITIVE_WRAPPER_AND_RELEASE" and
         ack.get("protocol") == LIVE_PROTOCOL and
         ack.get("transaction_binding_domain") == TRANSACTION_BINDING_DOMAIN and
         ack.get("transaction_binding_sha256") ==
             request["transaction_binding_sha256"] and
         ack.get("request_object_sha256") == request["object_sha256"] and
         ack.get("inner_object_sha256") == request["inner_object_sha256"] and
         ack.get("wrapper_body_domain") == PREWRAPPER_BODY_DOMAIN and
         ack.get("wrapper_body_domain_sha256") ==
             request["wrapper_body_domain_sha256"] and
         ack.get("wrapper_object_sha256") == request["wrapper_object_sha256"] and
         ack.get("ack_binding_domain") == LIVE_ACK_BINDING_DOMAIN and
         ack.get("ack_binding_sha256") == _expected_ack_binding(request) and
         ack.get("final_dynamic_replay_census") == expected_census and
         ack.get("all_dynamic_conjuncts_live") is True and
         ack.get("wrapper_closed_and_schema_validated_before_request") is True and
         ack.get("wrapper_body_excludes_transaction_binding_request_ACK_and_RELEASE_to_avoid_hash_cycle") is True and
         ack.get("transaction_binding_is_replay_identical_not_fresh_or_random") is True and
         ack.get("static_cold_exact10_terminal_replay_completed_by_launcher_before_request") is True and
         ack.get("launcher_empty_rejection_namespace_guard_terminally_replayed_before_request") is True and
         ack.get("positive_wrapper_emitted_by_combined_child") is False and
         ack.get("release_required_before_dynamic_guards_close") is True and
         ack.get("positive_wrapper_raw_fd1_final_newline_write_is_launcher_semantic_commit") is True and
         ack.get("post_ACK_RELEASE_and_child_exit_are_non_authority_cleanup") is True and
         ack.get("formal_global_closure_credit") == 0 and
         ack.get("D02_unlock") is False and raw == canonical(ack) + b"\n",
         "cold live ACK exact binding, census, zero-credit, and chronology")
    _validate_lock_ack(ack["official_writer_coordination_lock"], coordination)
    return ack


def run_authorize_child(
        bundle: HeldBundle, coordination: HeldCoordinationParent,
        rejection_guard: HeldEmptyRejectionNamespace) -> bool:
    source = bundle.by_path[CONSUMER]
    process = subprocess.Popen(
        child_argv(source, "authorize", []),
        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        # Inherit stderr so a verbose rejecting child cannot deadlock on a
        # bounded stderr pipe while the two-phase stdout protocol is active.
        stderr=None,
        env=child_environment(bundle, source, coordination),
        pass_fds=(source.fd, coordination.fd))
    need(process.stdin is not None and process.stdout is not None,
         "cold authorize dedicated bidirectional pipes")
    wrapper_committed = False
    positive_output_fd = -1
    try:
        inner_raw = process.stdout.readline(32 * 1024 * 1024 + 1)
        if inner_raw == b"":
            # The first authorize call may install the immutable zero-credit
            # authority seal and intentionally emit nothing.  A clean child
            # exit is a successful non-authoritative operation.
            process.wait()
            need(process.returncode == 0,
                 "cold authorize zero-output seal installation")
            bundle.terminal_replay()
            rejection_guard.terminal_replay()
            coordination.verify()
            return False
        need(inner_raw.endswith(b"\n") and
             len(inner_raw) <= 32 * 1024 * 1024 and
             inner_raw.count(b"\n") == 1,
             "cold inner stdout:one bounded newline-terminated object")
        need(sys.stdout.buffer.fileno() == 1,
             "positive wrapper stdout is exact fd1")
        sys.stdout.buffer.flush()
        stdout_flags = fcntl.fcntl(1, fcntl.F_GETFL)
        stdout_info = os.fstat(1)
        need(stat.S_ISFIFO(stdout_info.st_mode) and
             not (stdout_flags & os.O_NONBLOCK) and os.get_blocking(1),
             "positive wrapper fd1 is a blocking pipe preflushed before final ACK")
        positive_output_fd = os.dup(1)
        held_stdout_info = os.fstat(positive_output_fd)
        held_stdout_flags = fcntl.fcntl(positive_output_fd, fcntl.F_GETFL)
        need((held_stdout_info.st_dev, held_stdout_info.st_ino, held_stdout_info.st_mode) ==
             (stdout_info.st_dev, stdout_info.st_ino, stdout_info.st_mode) and
             not (held_stdout_flags & os.O_NONBLOCK) and
             os.get_blocking(positive_output_fd),
             "held duplicate of prevalidated blocking positive-output pipe")
        root, inner = cold_root(bundle, coordination, inner_raw)
        root_raw = canonical(root) + b"\n"
        need(root_raw.endswith(b"\n") and root_raw.count(b"\n") == 1,
             "preclosed wrapper exact canonical line")
        wrapper_body_sha256 = _wrapper_body_domain_sha256(root)
        transaction_binding = _deterministic_transaction_binding(
            bundle, inner["object_sha256"], wrapper_body_sha256,
            root["object_sha256"])
        # Absolute last launcher-side static gate.  The child performs the
        # complete dynamic replay only after receiving the bound request.
        bundle.terminal_replay()
        rejection_guard.terminal_replay()
        coordination.verify()
        request = close_object({
            "schema": LIVE_REQUEST_SCHEMA,
            "status": "REQUEST_FINAL_DYNAMIC_LIVE_ACK_BEFORE_POSITIVE_WRAPPER_OUTPUT",
            "protocol": LIVE_PROTOCOL,
            "transaction_binding_domain": TRANSACTION_BINDING_DOMAIN,
            "transaction_binding_sha256": transaction_binding,
            "inner_object_sha256": inner["object_sha256"],
            "wrapper_body_domain": PREWRAPPER_BODY_DOMAIN,
            "wrapper_body_domain_sha256": wrapper_body_sha256,
            "wrapper_object_sha256": root["object_sha256"],
            "wrapper_closed_and_schema_validated_before_request": True,
            "wrapper_body_excludes_transaction_binding_request_ACK_and_RELEASE_to_avoid_hash_cycle": True,
            "transaction_binding_is_replay_identical_not_fresh_or_random": True,
            "static_cold_exact10_terminal_replay_completed_by_launcher_before_request": True,
            "launcher_empty_rejection_namespace_guard_terminally_replayed_before_request": True,
        })
        request_raw = canonical(request) + b"\n"
        written = process.stdin.write(request_raw)
        need(written == len(request_raw), "complete cold live request write")
        process.stdin.flush()
        ack_raw = _read_child_line(process.stdout, "cold final-dynamic ACK")
        ack = _validate_live_ack(ack_raw, request, coordination)

        # Fully prepare the non-authoritative cleanup message before the
        # positive stdout commit.  Failure here still exposes no wrapper.
        release = close_object({
            "schema": LIVE_RELEASE_SCHEMA,
            "status": "RELEASE_AFTER_POSITIVE_WRAPPER_RAW_FD1_FINAL_NEWLINE_COMMIT",
            "protocol": LIVE_PROTOCOL,
            "transaction_binding_sha256":
                request["transaction_binding_sha256"],
            "inner_object_sha256": request["inner_object_sha256"],
            "wrapper_body_domain_sha256": request["wrapper_body_domain_sha256"],
            "wrapper_object_sha256": request["wrapper_object_sha256"],
            "ack_object_sha256": ack["object_sha256"],
        })
        release_raw = canonical(release) + b"\n"

        # No schema, filesystem, subprocess-status, or semantic gate follows
        # the validated ACK before exposure.  The launcher-owned lock remains
        # held even if the child crashes in this tiny output window.
        view = memoryview(root_raw)
        offset = 0
        while offset < len(view):
            try:
                written = os.write(positive_output_fd, view[offset:])
            except InterruptedError:
                continue
            need(written > 0, "positive wrapper raw fd1 made forward progress")
            offset += written
        # The semantic commit is the successful raw write of the final newline.
        # From this assignment onward there is no authority-determining gate.
        wrapper_committed = True

        # From the raw final-newline commit onward cleanup cannot revoke or downgrade the
        # already valid wrapper.  Keep the launcher lock while making a
        # best-effort bound RELEASE and reaping the child; do not apply another
        # authority gate after the semantic commit.
        try:
            process.stdin.write(release_raw)
            process.stdin.flush()
        except (BrokenPipeError, OSError):
            pass
        try:
            process.stdin.close()
        except OSError:
            pass
        try:
            process.wait()
        except (OSError, subprocess.SubprocessError):
            pass
    finally:
        if wrapper_committed:
            # The wrapper's final raw newline is the semantic commit.  Every
            # operation below is strictly best-effort resource cleanup and
            # cannot turn that already exposed line back into a rejection.
            try:
                if process.stdin is not None and not process.stdin.closed:
                    process.stdin.close()
            except OSError:
                pass
            try:
                if process.poll() is None:
                    process.terminate()
                    process.wait()
            except (OSError, subprocess.SubprocessError):
                pass
            try:
                process.stdout.close()
            except OSError:
                pass
            if positive_output_fd >= 0:
                try:
                    os.close(positive_output_fd)
                except OSError:
                    pass
        else:
            if process.stdin is not None and not process.stdin.closed:
                process.stdin.close()
            if process.poll() is None:
                process.terminate()
                process.wait()
            process.stdout.close()
            if positive_output_fd >= 0:
                os.close(positive_output_fd)
        # If wrapper exposure failed, the lock still remained held throughout
        # cleanup.  If it succeeded, RELEASE and child cleanup occurred before
        # the caller finally unlocks the coordination parent.
        if not wrapper_committed:
            coordination.verify()
    return wrapper_committed


def parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--expected-launcher-sha256", required=True)
    sub = cli.add_subparsers(dest="command", required=True)
    build = sub.add_parser("build")
    build.add_argument("--outdir", required=True)
    verify = sub.add_parser("verify")
    verify.add_argument("--orientation", required=True, choices=("a", "b"))
    sub.add_parser("assemble")
    sub.add_parser("authorize")
    sub.add_parser("reject")
    return cli


def main(argv: list[str] | None = None) -> int:
    need(sys.flags.isolated == 1 and sys.flags.dont_write_bytecode == 1 and
         sys.flags.no_site == 1,
         "invoke cold launcher only as: python3 -I -B -S <launcher> ...")
    args = parser().parse_args(argv)
    bundle = HeldBundle(args.expected_launcher_sha256)
    wrapper_committed = False
    try:
        coordination = HeldCoordinationParent()
        rejection_guard: HeldEmptyRejectionNamespace | None = None
        try:
            if args.command != "reject":
                rejection_guard = HeldEmptyRejectionNamespace(coordination)
            if args.command == "build":
                stdout = run_non_authorize_child(
                    bundle, coordination, rejection_guard,
                    "build", ["--outdir", args.outdir])
            elif args.command == "verify":
                stdout = run_non_authorize_child(
                    bundle, coordination, rejection_guard,
                    "verify", ["--orientation", args.orientation])
            elif args.command == "assemble":
                stdout = run_non_authorize_child(
                    bundle, coordination, rejection_guard, "assemble", [])
            elif args.command == "reject":
                stdout = run_non_authorize_child(
                    bundle, coordination, None, "reject", [])
            else:
                need(rejection_guard is not None,
                     "authorize requires held exact-empty rejection namespace")
                wrapper_committed = run_authorize_child(
                    bundle, coordination, rejection_guard)
                stdout = b""
            if args.command != "authorize":
                need(not stdout, "non-root cold child unexpectedly wrote stdout")
        finally:
            if rejection_guard is not None:
                rejection_guard.close()
            if wrapper_committed:
                try:
                    coordination.close()
                except OSError:
                    pass
            else:
                coordination.close()
    finally:
        if wrapper_committed:
            try:
                bundle.close()
            except OSError:
                pass
        else:
            bundle.close()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Reject as exc:
        print("REJECT:", exc, file=sys.stderr)
        raise SystemExit(2)
