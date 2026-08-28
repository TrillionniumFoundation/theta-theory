#!/usr/bin/env python3
"""Fail-closed r23 exact8 -> manifest -> outer-last publisher.

The default ``PREFLIGHT`` command is read-only.  ``FREEZE_PUBLISH`` is an
explicit one-shot operation whose source switch is deliberately disabled in
this clean-room draft.  An independent review may enable that switch in a
separate append-only revision and then run it once.  The guard never imports
or executes a candidate, never opens an authority surface for writing, and
never deletes/overwrites a partial publication.

All eight candidate members are opened from held output-directory descriptors,
hashed, AST parsed/compiled in memory, and replayed after every mode change.
The runtime directory is held under the official coordination lock only to
prove identity and no-writer continuity.  Manifest and outer are O_EXCL,
fsynced, and terminally replayed while the same descriptors and lock remain
held.  Physical chronology is checked from held-FD stat records, not wall
clock claims.
"""
from __future__ import annotations

import ast
import ctypes
from dataclasses import dataclass
import errno
import fcntl
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
from typing import Any, Iterable

sys.dont_write_bytecode = True

# This is intentionally false in the submitted draft.  It prevents an
# accidental publish while the root integrator reviews the preflight report.
ONE_SHOT_FREEZE_PUBLISH_ENABLED = False

BASE = "cm2_round306c79g_true_global_no_producer_consumer"
TAG = "v16r2r23"
PREV = "v16r2r22"
CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
SUCCESSOR_CHECKPOINT = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"

MANIFEST_REL = f"deliverables/{BASE}_cold_launch_manifest_{TAG}.sha256"
OUTER_REL = f"deliverables/{BASE}_cold_launch_outer_receipt_{TAG}.json"


@dataclass(frozen=True)
class Pin:
    relative: str
    file_sha256: str
    object_sha256: str | None
    initial_mode: int


EXACT8: tuple[Pin, ...] = (
    Pin(
        f"deliverables/{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json",
        "65b03dadebe91491fbb2750b0dd51d0829e681f258956669756b067d8be10274",
        "c600d67d618bceb3fe757d439df4fb35b4965cc7adffe2e615ebafc44a26dce0",
        0o444,
    ),
    Pin(
        f"deliverables/{BASE}_schema_{TAG}.json",
        "64e4e00fb6c263b032fc45457924bb08c806b8bcaf23485ff8915d384c82a9a7",
        None,
        0o444,
    ),
    Pin(
        f"deliverables/{BASE}_contract_{TAG}.json",
        "1fcdf3ab8880f541d46425c58e93951171e106da301f709c8423e5800cc34900",
        "8caa1ae7a3bc0b0b819960c1a177845b68ec178209bb1f2df010189a8b7fb92d",
        0o444,
    ),
    Pin(
        f"deliverables/{BASE}_{TAG}_semantic_source.py",
        "e0c8521c8b79244266c600313376f925f24a19c36f84b185186434b2c12ab375",
        None,
        0o664,
    ),
    Pin(
        f"deliverables/{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
        "014ebfc2e98b3c8c17c3dfdec925ca89aa6e802649886973cff7aebb7085456e",
        None,
        0o664,
    ),
    Pin(
        f"deliverables/{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
        "2a97ff19710b1030876b574de0da4a2756e77df6d34e403b6aa8eae8fabbd5d9",
        "0f1a43cefef0b313cca78cb206bc15a29ff35766e577f489ecd12d06122aee36",
        0o444,
    ),
    Pin(
        f"deliverables/{BASE}_static_audit_{TAG}.json",
        "23851f4f1055e679681ba6c1d7bfba0f86c42d121a8606ba283f4aac6a277e1c",
        "c5969ed31d12d70aae4fc994ba9aa29e43d9f4b8f0e9265819bcf9c434cb3d9f",
        0o444,
    ),
    Pin(
        f"deliverables/{BASE}_cold_launch_{TAG}_semantic_source.py",
        "462edc196a572a1fdc8139ad92dce95dcc5a2dcdcb74c117d2a623f4bbca2482",
        None,
        0o664,
    ),
)

SOURCE_PATHS = {p.relative for p in EXACT8 if p.relative.endswith(".py")}
JSON_PATHS = {p.relative for p in EXACT8 if p.relative.endswith(".json")}

# Linux TCB primitives used for held-directory and mount identity.  A missing
# primitive fails closed; there is no pathname or cross-device fallback.
AT_EMPTY_PATH = 0x1000
AT_SYMLINK_NOFOLLOW = 0x100
STATX_BASIC_STATS = 0x000007FF
STATX_MNT_ID = 0x00001000
RESOLVE_NO_XDEV = 0x01
RESOLVE_NO_MAGICLINKS = 0x02
RESOLVE_NO_SYMLINKS = 0x04
RESOLVE_BENEATH = 0x08


class _StatxTimestamp(ctypes.Structure):
    _fields_ = [("tv_sec", ctypes.c_int64), ("tv_nsec", ctypes.c_uint32),
                ("reserved", ctypes.c_int32)]


class _Statx(ctypes.Structure):
    _fields_ = [
        ("stx_mask", ctypes.c_uint32), ("stx_blksize", ctypes.c_uint32),
        ("stx_attributes", ctypes.c_uint64), ("stx_nlink", ctypes.c_uint32),
        ("stx_uid", ctypes.c_uint32), ("stx_gid", ctypes.c_uint32),
        ("stx_mode", ctypes.c_uint16), ("spare0", ctypes.c_uint16),
        ("stx_ino", ctypes.c_uint64), ("stx_size", ctypes.c_uint64),
        ("stx_blocks", ctypes.c_uint64),
        ("stx_attributes_mask", ctypes.c_uint64),
        ("stx_atime", _StatxTimestamp), ("stx_btime", _StatxTimestamp),
        ("stx_ctime", _StatxTimestamp), ("stx_mtime", _StatxTimestamp),
        ("stx_rdev_major", ctypes.c_uint32),
        ("stx_rdev_minor", ctypes.c_uint32),
        ("stx_dev_major", ctypes.c_uint32),
        ("stx_dev_minor", ctypes.c_uint32), ("stx_mnt_id", ctypes.c_uint64),
        ("stx_dio_mem_align", ctypes.c_uint32),
        ("stx_dio_offset_align", ctypes.c_uint32),
        ("spare3", ctypes.c_uint64 * 12),
    ]


class _OpenHow(ctypes.Structure):
    _fields_ = [("flags", ctypes.c_uint64), ("mode", ctypes.c_uint64),
                ("resolve", ctypes.c_uint64)]


def _libc() -> ctypes.CDLL:
    lib = ctypes.CDLL(None, use_errno=True)
    need(hasattr(lib, "statx") and hasattr(lib, "syscall"),
         "Linux statx/syscall unavailable")
    return lib


def fd_mount_id(fd: int) -> int:
    info = _Statx()
    lib = _libc()
    ctypes.set_errno(0)
    result = lib.statx(
        ctypes.c_int(fd), ctypes.c_char_p(b""),
        ctypes.c_int(AT_EMPTY_PATH | AT_SYMLINK_NOFOLLOW),
        ctypes.c_uint(STATX_BASIC_STATS | STATX_MNT_ID), ctypes.byref(info))
    need(result == 0 and bool(info.stx_mask & STATX_MNT_ID),
         "statx mount id")
    mount = int(info.stx_mnt_id)
    need(mount > 0, "positive mount id")
    return mount


def secure_open_dir(parent_fd: int, relative: str) -> int:
    need(relative not in {"", ".", ".."} and "/" not in relative,
         "clean direct directory component")
    lib = _libc()
    how = _OpenHow(
        os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC, 0,
        RESOLVE_NO_XDEV | RESOLVE_NO_MAGICLINKS |
        RESOLVE_NO_SYMLINKS | RESOLVE_BENEATH,
    )
    ctypes.set_errno(0)
    fd = lib.syscall(
        ctypes.c_long(437), ctypes.c_int(parent_fd),
        ctypes.c_char_p(os.fsencode(relative)), ctypes.byref(how),
        ctypes.c_size_t(ctypes.sizeof(how)),
    )
    if fd < 0:
        code = ctypes.get_errno()
        raise Reject("openat2 " + relative + ":" + os.strerror(code))
    return int(fd)


class Reject(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if not condition:
        raise Reject(message)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def strict_pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in items:
        need(key not in result, "duplicate JSON key:" + key)
        result[key] = value
    return result


def reject_constant(value: str) -> Any:
    raise ValueError("non-finite JSON constant:" + value)


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    need(raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
         label + ":one terminal newline")
    try:
        value = json.loads(
            raw.decode("utf-8"), object_pairs_hook=strict_pairs,
            parse_constant=reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise Reject(label + ":strict JSON parse") from exc
    need(isinstance(value, dict), label + ":top-level object")
    return value


def verify_object(raw: bytes, claimed: str, label: str) -> dict[str, Any]:
    need(isinstance(claimed, str) and len(claimed) == 64,
         label + ":object pin shape")
    value = strict_json(raw, label)
    body = dict(value)
    actual = body.pop("object_sha256", None)
    need(actual == claimed and sha(canonical(body)) == claimed,
         label + ":object closure")
    return value


def file_identity(value: os.stat_result) -> tuple[int, int, int, int, int]:
    return (value.st_dev, value.st_ino, value.st_size, value.st_mode,
            value.st_nlink)


def dir_identity(value: os.stat_result) -> tuple[int, int, int, int]:
    # Directory size legitimately changes as manifest/outer entries are
    # published; it is not an identity component.
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink)


def fd_read(fd: int) -> bytes:
    os.lseek(fd, 0, os.SEEK_SET)
    chunks: list[bytes] = []
    while True:
        block = os.read(fd, 1 << 20)
        if not block:
            return b"".join(chunks)
        chunks.append(block)


def recursive_scan(fd: int, predicate: Any, label: str) -> None:
    """Scan without following symlinked directories."""
    for name in os.listdir(fd):
        need(name not in {"", ".", ".."}, label + ":bad entry")
        state = os.stat(name, dir_fd=fd, follow_symlinks=False)
        if predicate(name, state):
            raise Reject(label + ":forbidden " + name)
        if stat.S_ISDIR(state.st_mode) and not stat.S_ISLNK(state.st_mode):
            child = os.open(
                name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW |
                os.O_CLOEXEC, dir_fd=fd)
            try:
                recursive_scan(child, predicate, label)
            finally:
                os.close(child)


class HeldDirectories:
    def __init__(self, root_text: str) -> None:
        self.root = Path(root_text)
        need(self.root.is_absolute() and os.path.normpath(root_text) == root_text,
             "root must be absolute normalized path")
        root_path = os.lstat(self.root)
        need(stat.S_ISDIR(root_path.st_mode) and not stat.S_ISLNK(root_path.st_mode),
             "root directory")
        self.root_fd = os.open(
            self.root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW |
            os.O_CLOEXEC)
        self.out_fd = -1
        self.runtime_fd = -1
        self.locked = False
        try:
            self.root_before = os.fstat(self.root_fd)
            need(dir_identity(root_path) == dir_identity(self.root_before),
                 "root path/fd identity")
            self.out_fd = secure_open_dir(self.root_fd, "deliverables")
            self.runtime_fd = secure_open_dir(self.root_fd, ".cm2-runtime")
            self.out_before = os.fstat(self.out_fd)
            self.runtime_before = os.fstat(self.runtime_fd)
            need(stat.S_ISDIR(self.out_before.st_mode) and
                 stat.S_ISDIR(self.runtime_before.st_mode), "held directories")
            need(self.root_before.st_dev == self.out_before.st_dev ==
                 self.runtime_before.st_dev, "one filesystem device")
            self.mount_id = fd_mount_id(self.root_fd)
            need(fd_mount_id(self.out_fd) == self.mount_id ==
                 fd_mount_id(self.runtime_fd), "one statx mount id")
            fcntl.flock(self.runtime_fd, fcntl.LOCK_EX)
            self.locked = True
            probe = secure_open_dir(self.root_fd, ".cm2-runtime")
            try:
                blocked = False
                try:
                    fcntl.flock(probe, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except BlockingIOError:
                    blocked = True
                need(blocked, "official lock independent probe")
            finally:
                os.close(probe)
            self.replay()
        except BaseException:
            self.close()
            raise

    def replay(self) -> None:
        root_path = os.lstat(self.root)
        out_path = os.stat("deliverables", dir_fd=self.root_fd,
                           follow_symlinks=False)
        runtime_path = os.stat(".cm2-runtime", dir_fd=self.root_fd,
                               follow_symlinks=False)
        root_now, out_now, runtime_now = (
            os.fstat(self.root_fd), os.fstat(self.out_fd),
            os.fstat(self.runtime_fd))
        need(dir_identity(root_path) == dir_identity(root_now) ==
             dir_identity(self.root_before),
             "root identity drift")
        need(dir_identity(out_path) == dir_identity(out_now) ==
             dir_identity(self.out_before),
             "deliverables identity drift")
        need(dir_identity(runtime_path) == dir_identity(runtime_now) ==
             dir_identity(self.runtime_before),
             "runtime identity drift")
        need(root_now.st_dev == out_now.st_dev == runtime_now.st_dev,
             "mount/device drift")
        need(fd_mount_id(self.root_fd) == fd_mount_id(self.out_fd) ==
             fd_mount_id(self.runtime_fd) == self.mount_id,
             "statx mount drift")

    def sync(self) -> None:
        os.fsync(self.out_fd)
        os.fsync(self.runtime_fd)
        os.fsync(self.root_fd)
        self.replay()

    def close(self) -> None:
        if self.locked and self.runtime_fd >= 0:
            try:
                fcntl.flock(self.runtime_fd, fcntl.LOCK_UN)
            except OSError:
                pass
            self.locked = False
        for fd in (self.runtime_fd, self.out_fd, self.root_fd):
            if fd >= 0:
                try:
                    os.close(fd)
                except OSError:
                    pass
        self.runtime_fd = self.out_fd = self.root_fd = -1


class HeldFile:
    def __init__(self, dirs: HeldDirectories, pin: Pin) -> None:
        self.dirs = dirs
        self.pin = pin
        rel = Path(pin.relative)
        need(rel.parts[:1] == ("deliverables",) and len(rel.parts) == 2,
             "direct deliverable path:" + pin.relative)
        self.name = rel.name
        path_state = os.stat(self.name, dir_fd=dirs.out_fd,
                             follow_symlinks=False)
        need(stat.S_ISREG(path_state.st_mode) and
             not stat.S_ISLNK(path_state.st_mode) and path_state.st_nlink == 1,
             pin.relative + ":regular nlink1")
        need(stat.S_IMODE(path_state.st_mode) == pin.initial_mode,
             pin.relative + f":initial mode {pin.initial_mode:04o}")
        self.fd = os.open(
            self.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC,
            dir_fd=dirs.out_fd)
        try:
            before = os.fstat(self.fd)
            need(file_identity(path_state) == file_identity(before),
                 pin.relative + ":path/fd identity")
            need(fd_mount_id(self.fd) == dirs.mount_id and
                 before.st_dev == dirs.out_before.st_dev,
                 pin.relative + ":held statx mount")
            raw = fd_read(self.fd)
            need(sha(raw) == pin.file_sha256, pin.relative + ":file hash")
            if pin.object_sha256 is not None:
                verify_object(raw, pin.object_sha256, pin.relative)
            self.before = before
        except BaseException:
            os.close(self.fd)
            self.fd = -1
            raise

    def replay(self, expected_mode: int = 0o444) -> os.stat_result:
        path_before = os.stat(self.name, dir_fd=self.dirs.out_fd,
                              follow_symlinks=False)
        fd_before = os.fstat(self.fd)
        need(stat.S_ISREG(path_before.st_mode) and path_before.st_nlink == 1 and
             file_identity(path_before) == file_identity(fd_before),
             self.pin.relative + ":terminal pre-read identity")
        need(stat.S_IMODE(fd_before.st_mode) == expected_mode,
             self.pin.relative + f":terminal mode {expected_mode:04o}")
        raw = fd_read(self.fd)
        fd_after = os.fstat(self.fd)
        path_after = os.stat(self.name, dir_fd=self.dirs.out_fd,
                             follow_symlinks=False)
        need(file_identity(path_before) == file_identity(fd_after) ==
             file_identity(path_after) and fd_after.st_nlink == 1,
             self.pin.relative + ":terminal read bracket identity")
        need(fd_mount_id(self.fd) == self.dirs.mount_id,
             self.pin.relative + ":terminal statx mount")
        need(sha(raw) == self.pin.file_sha256,
             self.pin.relative + ":terminal hash")
        if self.pin.object_sha256 is not None:
            verify_object(raw, self.pin.object_sha256, self.pin.relative)
        return fd_state

    def freeze(self) -> os.stat_result:
        need(stat.S_IMODE(os.fstat(self.fd).st_mode) in {0o664, 0o644},
             self.pin.relative + ":freeze source mode")
        os.fsync(self.fd)
        os.fchmod(self.fd, 0o444)
        os.fsync(self.fd)
        self.dirs.sync()
        return self.replay(0o444)

    def close(self) -> None:
        if self.fd >= 0:
            try:
                os.close(self.fd)
            except OSError:
                pass
            self.fd = -1


def exact_paths() -> list[str]:
    return [p.relative for p in EXACT8]


def assert_absent(dirs: HeldDirectories, relative: str) -> None:
    rel = Path(relative)
    need(rel.parts[:1] == ("deliverables",) and len(rel.parts) == 2,
         "direct absence path")
    try:
        os.stat(rel.name, dir_fd=dirs.out_fd, follow_symlinks=False)
    except FileNotFoundError:
        return
    raise Reject(relative + ":must be absent")


def assert_no_pyc(dirs: HeldDirectories) -> None:
    # Historical CM2 rounds intentionally retain their own pyc evidence.  The
    # r23 clean-room gate rejects only bytecode that could belong to this
    # successor (or a freshly generated guard/source copy), while still
    # walking every directory without following symlinks.
    def forbidden(name: str, state: os.stat_result) -> bool:
        if not name.lower().endswith(".pyc"):
            return False
        lowered = name.lower()
        # A tagged symlink, directory, FIFO, or socket is just as unsafe as a
        # regular bytecode file; reject by lexical entry before type filtering.
        return TAG.lower() in lowered
    recursive_scan(dirs.root_fd, forbidden, "r23 pyc scan")


def assert_runtime_absent(dirs: HeldDirectories) -> None:
    """No successor-named runtime namespace may preexist or appear."""
    def forbidden(name: str, state: os.stat_result) -> bool:
        return TAG.lower() in name.lower()
    recursive_scan(dirs.runtime_fd, forbidden, "r23 runtime scan")


def source_ast_checks(raw_by_path: dict[str, bytes]) -> None:
    for path in SOURCE_PATHS:
        try:
            tree = ast.parse(raw_by_path[path].decode("utf-8"), filename=path)
            compile(tree, path, "exec")
        except (UnicodeDecodeError, SyntaxError, ValueError) as exc:
            raise Reject(path + ":AST/compile") from exc
    launcher = ast.parse(
        raw_by_path[next(p for p in SOURCE_PATHS if "cold_launch_" in p)].decode(),
        filename="r23 launcher",
    )
    flags = [
        node for node in launcher.body
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and
        isinstance(node.targets[0], ast.Name) and
        node.targets[0].id == "FINAL_BASE7_PINS_INSTALLED"
    ]
    need(len(flags) == 1 and isinstance(flags[0].value, ast.Constant) and
         flags[0].value.value is True, "launcher final pins flag")
    need(sum(isinstance(n, ast.FunctionDef) and
             n.name == "configure_workspace_paths" for n in launcher.body) == 1,
         "launcher configurator")


def stable_path_bytes(path: Path) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             str(path) + ":checker regular/nlink1")
        raw = fd_read(fd)
        after = os.fstat(fd)
        need(file_identity(before) == file_identity(after),
             str(path) + ":checker source drift")
        return raw
    finally:
        os.close(fd)


def run_checker(path: Path, root: Path, seed: str) -> dict[str, Any]:
    before = stable_path_bytes(path)
    env = dict(os.environ)
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "CM2_SUCCESSOR_SUFFIX": TAG,
                "CM2_PREDECESSOR_SUFFIX": PREV, "PYTHONHASHSEED": seed})
    proc = subprocess.run(
        ["/usr/bin/python3", "-I", "-B", str(path)], cwd=str(root), env=env,
        text=True, capture_output=True, check=False,
    )
    need(proc.returncode == 0, path.name + ":nonzero")
    try:
        value = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise Reject(path.name + ":one JSON report") from exc
    need(isinstance(value, dict), path.name + ":report object")
    need(stable_path_bytes(path) == before, path.name + ":post-run source drift")
    need(value.get("read_only") is True and
         value.get("formal_global_closure_credit", 0) in (0, False, None) and
         value.get("D02_unlock") is not True and
         value.get("runtime_authorized") is not True,
         path.name + ":report zero/read-only boundary")
    need(value.get("object_sha256") == sha(canonical({
        k: v for k, v in value.items() if k != "object_sha256"})),
         path.name + ":report object closure")
    return value


def static_surfaces(dirs: HeldDirectories, held: dict[str, HeldFile],
                    root: Path) -> dict[str, Any]:
    """Independent preflight of the immutable bytes; no candidate execution."""
    raw = {rel: fd_read(item.fd) for rel, item in held.items()}
    values = {
        rel: strict_json(raw[rel], rel) for rel in JSON_PATHS
    }
    for pin in EXACT8:
        if pin.object_sha256 is not None:
            verify_object(raw[pin.relative], pin.object_sha256, pin.relative)
    source_ast_checks(raw)
    contract = values[EXACT8[2].relative]
    transition = values[EXACT8[5].relative]
    audit = values[EXACT8[6].relative]
    schema = values[EXACT8[1].relative]
    bundle = contract.get("v16r2_bundle", {})
    need(contract.get("status") ==
         "STATIC_CONTRACT_BYTES_FINAL__COLD_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED",
         "contract status")
    need(contract.get("effective_checkpoint_object_sha256") == CHECKPOINT,
         "contract checkpoint")
    need(bundle.get("base7_ordered_paths") == exact_paths()[:-1] and
         bundle.get("exact8_ordered_paths") == exact_paths() and
         bundle.get("exact10_ordered_paths") ==
         exact_paths() + [MANIFEST_REL, OUTER_REL], "contract exact order")
    need(bundle.get("D02_unlock") is False and
         bundle.get("formal_global_closure_credit") == 0,
         "contract zero credit")
    need(transition.get("status") ==
         "STATIC_BYTES_CLOSED_V16_TO_V16R2__PHYSICAL_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED",
         "transition status")
    need(transition.get("formal_global_closure_credit") == 0 and
         transition.get("D02_unlock") is False and
         transition.get("runtime_executed_during_transition") is False,
         "transition zero/no-run")
    need(transition.get("cold_launch_boundary", {}).get("base7_order") ==
         exact_paths()[:-1], "transition base7")
    need(audit.get("status") ==
         "PASS_DUAL_STATIC_PIN_NORMALIZED_AST_GO_V16R2__PHYSICAL_COLD_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED",
         "audit status")
    census = audit.get("static_credit_census", {})
    need(audit.get("object_sha256") and
         census.get("all_persisted_r9_objects_formal_global_closure_credit") == 0 and
         census.get("all_persisted_r9_objects_D02_unlock") is False and
         census.get("all_persisted_r9_objects_D02_started") is False and
         census.get("cold_live_inner_formal_global_closure_credit") == 0,
         "audit zero credit")
    need(len(schema.get("$defs", {})) == 46 and
         sum(isinstance(n, dict) and "$ref" in n for n in _walk(schema)) == 242 and
         sum(isinstance(n, dict) and n.get("additionalProperties") is False
             for n in _walk(schema)) == 52, "schema census")
    # The schema's positive consts describe a future wrapper and are not live
    # credit.  Every active instance/receipt root remains zero-credit.
    for value in (contract, transition, audit):
        for node in _walk(value):
            if isinstance(node, dict):
                need(node.get("formal_global_closure_credit", 0) in (0, False, None) and
                     node.get("D02_unlock") is not True and
                     node.get("runtime_authorized") is not True,
                     "active zero-credit census")
    reviewer_path = root / "scripts/c79g_v16r2r20_independent_reviewer.py"
    checker_b_path = root / "scripts/c79g_v16r2r23_structure_checker_b.py"
    reviewer = run_checker(reviewer_path, root, "1")
    reviewer_seed2 = run_checker(reviewer_path, root, "99991")
    checker_b = run_checker(checker_b_path, root, "1")
    checker_b_seed2 = run_checker(checker_b_path, root, "99991")
    need(canonical(reviewer) == canonical(reviewer_seed2),
         "reviewer dual-PYTHONHASHSEED replay")
    need(canonical(checker_b) == canonical(checker_b_seed2),
         "checker B dual-PYTHONHASHSEED replay")
    need(reviewer.get("status") ==
         "PASS_DUAL_STATIC_CANDIDATE_34_OF_34__RUNTIME_NOT_AUTHORIZED" and
         reviewer.get("check_count") == 34 and
         reviewer.get("failed_check_count") == 0,
         "reviewer A 34/34")
    need(checker_b.get("status") == "PASS_INDEPENDENT_CHECKER_B__ZERO_CREDIT" and
         checker_b.get("check_count") == 16 and
         checker_b.get("failed_check_count") == 0,
         "checker B 16/16")
    anchor = values[EXACT8[0].relative]
    need(anchor.get("upstream_checkpoint_object_sha256") == CHECKPOINT and
         anchor.get("successor_checkpoint_object_sha256") == SUCCESSOR_CHECKPOINT and
         transition.get("effective_checkpoint_object_sha256") == SUCCESSOR_CHECKPOINT and
         audit.get("effective_checkpoint_object_sha256") == SUCCESSOR_CHECKPOINT,
         "checkpoint chain upstream/successor semantics")
    # Independent no-producer, mutation-attack, and terminal-replay receipts
    # are side evidence, never exact8 members or authority writes.  When
    # present they must be closed, zero-credit, and explicitly read-only.
    side_names = (
        f"{BASE}_{TAG}_no_producer_dual_seed_evidence_receipt_v1.json",
        f"{BASE}_{TAG}_mutation_attack_evidence_receipt_v1.json",
        f"{BASE}_{TAG}_dual_checker_terminal_replay_receipt_v1.json",
    )
    for name in side_names:
        side = root / "deliverables" / name
        need(side.is_file(), "missing side evidence:" + name)
        side_value = strict_json(stable_path_bytes(side), name)
        claim = side_value.get("object_sha256")
        need(isinstance(claim, str) and
             claim == sha(canonical({k: v for k, v in side_value.items()
                                     if k != "object_sha256"})),
             name + ":object closure")
        need(side_value.get("formal_global_closure_credit") == 0 and
             side_value.get("D02_unlock") is False and
             side_value.get("runtime_authorized") is False,
             name + ":zero credit")
        if isinstance(side_value.get("writes"), dict):
            need(all(v is False for v in side_value["writes"].values()),
                 name + ":write boundary")
    assert_absent(dirs, MANIFEST_REL)
    assert_absent(dirs, OUTER_REL)
    assert_no_pyc(dirs)
    assert_runtime_absent(dirs)
    dirs.replay()
    return {"reviewer_A": reviewer, "checker_B": checker_b}


def _walk(value: Any):
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def publication_bytes() -> tuple[bytes, bytes, str, str]:
    entries = [{"path": pin.relative, "file_sha256": pin.file_sha256}
               for pin in EXACT8]
    manifest = b"".join(
        f"{entry['file_sha256']}  {entry['path']}\n".encode("ascii")
        for entry in entries)
    manifest_sha = sha(manifest)
    outer_body = {
        # The launcher consumes this as the v16r2 outer protocol object.  The
        # r23 suffix belongs to the source namespace/path, not to the outer
        # schema version (the launcher explicitly requires ``.v16r2``).
        "schema": "cm2.round306c79g.true-global-no-producer-consumer.cold-launch-outer-receipt.v16r2",
        "status": "FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED",
        # The outer is bound to the successor transition checkpoint.  The
        # contract/audit's effective upstream C53 pin remains CHECKPOINT;
        # launcher runtime and historical rejection namespaces use this
        # successor object pin.
        "effective_checkpoint_object_sha256": SUCCESSOR_CHECKPOINT,
        "exact8_ordered_entries": entries,
        "cold_launch_manifest": {"path": MANIFEST_REL,
                                 "file_sha256": manifest_sha,
                                 "ordered_entry_count": 8},
        "cold_launcher": {"path": EXACT8[-1].relative,
                          "file_sha256": EXACT8[-1].file_sha256},
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
    }
    outer_body["object_sha256"] = sha(canonical(outer_body))
    outer = canonical(outer_body) + b"\n"
    return manifest, outer, manifest_sha, outer_body["object_sha256"]


def create_exclusive(dirs: HeldDirectories, relative: str, raw: bytes) -> int:
    rel = Path(relative)
    need(rel.parts[:1] == ("deliverables",) and len(rel.parts) == 2,
         "publication direct path")
    try:
        fd = os.open(rel.name, os.O_RDWR | os.O_CREAT | os.O_EXCL |
                     os.O_NOFOLLOW | os.O_CLOEXEC, 0o444, dir_fd=dirs.out_fd)
    except FileExistsError as exc:
        raise Reject(relative + ":preexisting append-only target") from exc
    try:
        view = memoryview(raw); offset = 0
        while offset < len(view):
            count = os.write(fd, view[offset:])
            need(count > 0, relative + ":short write")
            offset += count
        os.fsync(fd)
        os.fchmod(fd, 0o444)
        os.fsync(fd)
        dirs.sync()
        state = os.fstat(fd)
        path_state = os.stat(rel.name, dir_fd=dirs.out_fd,
                             follow_symlinks=False)
        need(stat.S_ISREG(state.st_mode) and state.st_nlink == 1 and
             stat.S_IMODE(state.st_mode) == 0o444 and
             file_identity(state) == file_identity(path_state) and
             fd_mount_id(fd) == dirs.mount_id and
             fd_read(fd) == raw,
             relative + ":published identity")
        return fd
    except BaseException:
        os.close(fd)
        raise


def chronology(states: list[os.stat_result], manifest: os.stat_result,
               outer: os.stat_result) -> dict[str, bool]:
    exact_ok = all(s.st_mtime_ns <= s.st_ctime_ns for s in states)
    manifest_ok = manifest.st_mtime_ns <= manifest.st_ctime_ns
    outer_ok = outer.st_mtime_ns <= outer.st_ctime_ns
    order_ok = max(max(s.st_mtime_ns, s.st_ctime_ns) for s in states) < manifest.st_mtime_ns < outer.st_mtime_ns
    return {
        "all_exact8_mtime_not_after_final_ctime": exact_ok,
        "manifest_mtime_not_after_final_ctime": manifest_ok,
        "outer_mtime_not_after_final_ctime": outer_ok,
        "max_exact8_final_mtime_ctime_before_manifest_mtime": order_ok,
        "manifest_final_ctime_before_outer_mtime": manifest.st_ctime_ns < outer.st_mtime_ns,
        "physical_exact8_freeze_then_manifest_freeze_then_outer_freeze_chronology":
            exact_ok and manifest_ok and outer_ok and order_ok and
            manifest.st_ctime_ns < outer.st_mtime_ns,
    }


def run(root_text: str, command: str) -> dict[str, Any]:
    need(command in {"PREFLIGHT", "FREEZE_PUBLISH"}, "command")
    if command == "FREEZE_PUBLISH":
        need(ONE_SHOT_FREEZE_PUBLISH_ENABLED,
             "one-shot freeze switch disabled in clean-room draft")
    root = Path(root_text)
    dirs = HeldDirectories(root_text)
    opened: list[HeldFile] = []
    extra_fds: list[int] = []
    try:
        assert_absent(dirs, MANIFEST_REL)
        assert_absent(dirs, OUTER_REL)
        assert_no_pyc(dirs)
        assert_runtime_absent(dirs)
        held: dict[str, HeldFile] = {}
        for pin in EXACT8:
            item = HeldFile(dirs, pin)
            held[pin.relative] = item
            opened.append(item)
        need(len({(os.fstat(i.fd).st_dev, os.fstat(i.fd).st_ino)
                  for i in opened}) == 8, "exact8 distinct identities")
        dirs.replay()
        checks = static_surfaces(dirs, held, root)
        manifest_raw, outer_raw, manifest_sha, outer_object_sha = publication_bytes()
        if command == "PREFLIGHT":
            return {
                "schema": f"cm2.c79g.{TAG}.cold-freeze-guard-preflight.v1",
                "status": "PREFLIGHT_READ_ONLY_PASS__EXACT8_PREHASHED__MANIFEST_OUTER_ABSENT",
                "successor_suffix": TAG,
                "predecessor_suffix": PREV,
                "ordered_exact8": [{"path": p.relative,
                                    "file_sha256": p.file_sha256,
                                    "object_sha256": p.object_sha256,
                                    "initial_mode": oct(p.initial_mode)} for p in EXACT8],
                "manifest_path": MANIFEST_REL,
                "manifest_file_sha256": manifest_sha,
                "outer_path": OUTER_REL,
                "outer_object_sha256": outer_object_sha,
                "outer_file_sha256": sha(outer_raw),
                "manifest_absent": True,
                "outer_absent": True,
                "runtime_authority_writes": False,
                "candidate_execution_count": 0,
                "pyc_absent": True,
                "official_lock_held": True,
                "static_checks": {"reviewer_A": checks["reviewer_A"].get("object_sha256"),
                                   "checker_B": checks["checker_B"].get("object_sha256")},
                "one_shot_publish_enabled": ONE_SHOT_FREEZE_PUBLISH_ENABLED,
            }
        # The source switch above is the only route to this block.
        states: list[os.stat_result] = []
        for index, item in enumerate(opened):
            # Every member, including the already-0444 JSON anchor/receipts,
            # is explicitly fsynced before its terminal replay.  Directory
            # fsync alone does not establish file-data durability.
            os.fsync(item.fd)
            if index == 0 or item.pin.initial_mode == 0o444:
                states.append(item.replay(0o444))
            else:
                states.append(item.freeze())
            for prior in opened[: index + 1]:
                prior.replay(0o444)
            for later in opened[index + 1:]:
                later.replay(later.pin.initial_mode)
            assert_absent(dirs, MANIFEST_REL); assert_absent(dirs, OUTER_REL)
            assert_no_pyc(dirs)
            assert_runtime_absent(dirs)
        states = [item.replay(0o444) for item in opened]
        for item in opened:
            os.fsync(item.fd)
        dirs.sync()
        manifest_fd = create_exclusive(dirs, MANIFEST_REL, manifest_raw)
        extra_fds.append(manifest_fd)
        manifest_state = os.fstat(manifest_fd)
        need(max(max(s.st_mtime_ns, s.st_ctime_ns) for s in states) <
             manifest_state.st_mtime_ns, "exact8 before manifest")
        outer_fd = create_exclusive(dirs, OUTER_REL, outer_raw)
        extra_fds.append(outer_fd)
        outer_state = os.fstat(outer_fd)
        chrono = chronology(states, manifest_state, outer_state)
        need(all(chrono.values()), "physical chronology")
        need(fd_read(manifest_fd) == manifest_raw and
             fd_read(outer_fd) == outer_raw, "terminal publication replay")
        dirs.sync(); dirs.replay(); assert_no_pyc(dirs); assert_runtime_absent(dirs)
        return {
            "schema": f"cm2.c79g.{TAG}.cold-freeze-guard-terminal.v1",
            "status": "TERMINAL_EXACT10_HELD_REPLAY_PASS__FROZEN_MANIFEST_OUTER_LAST__RUNTIME_NOT_EXECUTED",
            "successor_suffix": TAG, "predecessor_suffix": PREV,
            "ordered_exact10": [p.relative for p in EXACT8] + [MANIFEST_REL, OUTER_REL],
            "manifest_file_sha256": manifest_sha,
            "outer_file_sha256": sha(outer_raw),
            "outer_object_sha256": outer_object_sha,
            "chronology": chrono,
            "unique_file_identity_count": 10,
            "all_exact10_regular_0444_nlink1": True,
            "manifest_O_EXCL_outer_last_O_EXCL": True,
            "runtime_authority_writes": False,
            "candidate_execution_count": 0,
            "pyc_absent": True,
        }
    finally:
        for fd in reversed(extra_fds):
            try: os.close(fd)
            except OSError: pass
        for item in reversed(opened): item.close()
        dirs.close()


def main() -> int:
    need(len(sys.argv) == 3, "usage: guard ABSOLUTE_ROOT PREFLIGHT|FREEZE_PUBLISH")
    try:
        result = run(sys.argv[1], sys.argv[2])
        os.write(1, canonical(result) + b"\n")
        return 0
    except Reject as exc:
        os.write(2, ("FAIL_CLOSED_R23_FREEZE_GUARD:" + str(exc) + "\n").encode())
        return 1
    except Exception as exc:
        os.write(2, ("FAIL_CLOSED_R23_FREEZE_GUARD_EXCEPTION:" +
                     type(exc).__name__ + ":" + str(exc) + "\n").encode())
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
