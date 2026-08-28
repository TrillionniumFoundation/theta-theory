#!/usr/bin/env python3
"""External held-FD bootstrap for the frozen C79g r34 launcher.

The bootstrap is deliberately independent of the launcher implementation.  It
opens the workspace and launcher beneath held ``openat2`` descriptors, checks
the r34 byte anchor, copies the exact bytes to a sealed memfd, and executes
only that memfd with isolated ``python -I -B -S``.  The child receives exactly
the sealed executable fd, the installed source fd, and the workspace-root fd.

``authorize`` is accepted by the CLI for protocol completeness but is guarded
by ``CM2_R34_AUTHORIZE_APPROVED=1``; this prevents an accidental positive
runtime command while the r34 clean-room handoff is still being audited.
"""
from __future__ import annotations

import argparse
import ctypes
import errno
import fcntl
import hashlib
import os
import re
import stat
import subprocess
import sys
from dataclasses import dataclass

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

PYTHON = "/usr/bin/python3"
LAUNCHER_RELATIVE = (
    "deliverables/"
    "cm2_round306c79g_true_global_no_producer_consumer_"
    "cold_launch_v16r2r34_semantic_source.py"
)
LAUNCHER_SHA256 = "24f9686462f47c009118887d1cdfd0f1b22791eeef335bcb64252d3ade931c0a"

RESOLVE_NO_XDEV = 0x01
RESOLVE_NO_MAGICLINKS = 0x02
RESOLVE_NO_SYMLINKS = 0x04
RESOLVE_BENEATH = 0x08
RESOLVE_FLAGS = RESOLVE_NO_XDEV | RESOLVE_NO_MAGICLINKS | RESOLVE_NO_SYMLINKS | RESOLVE_BENEATH
AT_EMPTY_PATH = 0x1000
AT_SYMLINK_NOFOLLOW = 0x100
STATX_BASIC_STATS = 0x000007FF
STATX_MNT_ID = 0x00001000

F_ADD_SEALS = getattr(fcntl, "F_ADD_SEALS", 1033)
F_GET_SEALS = getattr(fcntl, "F_GET_SEALS", 1034)
F_SEAL_SEAL = getattr(fcntl, "F_SEAL_SEAL", 0x0001)
F_SEAL_SHRINK = getattr(fcntl, "F_SEAL_SHRINK", 0x0002)
F_SEAL_GROW = getattr(fcntl, "F_SEAL_GROW", 0x0004)
F_SEAL_WRITE = getattr(fcntl, "F_SEAL_WRITE", 0x0008)
REQUIRED_SEALS = F_SEAL_SEAL | F_SEAL_SHRINK | F_SEAL_GROW | F_SEAL_WRITE
MFD_CLOEXEC = getattr(os, "MFD_CLOEXEC", 0x0001)
MFD_ALLOW_SEALING = getattr(os, "MFD_ALLOW_SEALING", 0x0002)


class BootstrapRefusal(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if not condition:
        raise BootstrapRefusal(message)


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
        ("stx_dio_offset_align", ctypes.c_uint32), ("spare3", ctypes.c_uint64 * 12),
    ]


def libc() -> ctypes.CDLL:
    need(sys.platform.startswith("linux"), "Linux is required")
    lib = ctypes.CDLL(None, use_errno=True)
    need(hasattr(lib, "syscall") and hasattr(lib, "statx"),
         "Linux syscall/statx are required")
    lib.syscall.restype = ctypes.c_long
    lib.statx.restype = ctypes.c_int
    return lib


def clean_relative(raw: bytes, label: str) -> None:
    need(raw and not raw.startswith(b"/") and b"\x00" not in raw,
         label + ": clean relative bytes")
    need(all(part not in (b"", b".", b"..") for part in raw.split(b"/")),
         label + ": dot/empty/parent component")


def openat2_beneath(dir_fd: int, relative: str | bytes, flags: int) -> int:
    raw = relative if isinstance(relative, bytes) else os.fsencode(relative)
    clean_relative(raw, "openat2")
    how = OpenHow(flags | os.O_CLOEXEC, 0, RESOLVE_FLAGS)
    ctypes.set_errno(0)
    fd = libc().syscall(
        ctypes.c_long(437), ctypes.c_int(dir_fd), ctypes.c_char_p(raw),
        ctypes.byref(how), ctypes.c_size_t(ctypes.sizeof(how)))
    if fd < 0:
        code = ctypes.get_errno()
        if code == errno.ENOENT:
            raise FileNotFoundError(code, os.strerror(code), os.fsdecode(raw))
        raise BootstrapRefusal("openat2 rejected " + os.fsdecode(raw) + ": " + os.strerror(code))
    return int(fd)


def mount_id(fd: int) -> int:
    info = Statx()
    ctypes.set_errno(0)
    rc = libc().statx(
        ctypes.c_int(fd), ctypes.c_char_p(b""),
        ctypes.c_int(AT_EMPTY_PATH | AT_SYMLINK_NOFOLLOW),
        ctypes.c_uint(STATX_BASIC_STATS | STATX_MNT_ID), ctypes.byref(info))
    if rc != 0:
        raise BootstrapRefusal("statx rejected held fd: " + os.strerror(ctypes.get_errno()))
    need(bool(info.stx_mask & STATX_MNT_ID), "statx mount id unavailable")
    return int(info.stx_mnt_id)


def fingerprint(st: os.stat_result) -> tuple[int, ...]:
    return (st.st_dev, st.st_ino, st.st_mode, st.st_nlink, st.st_uid,
            st.st_gid, st.st_size, st.st_mtime_ns, st.st_ctime_ns)


def directory_identity(st: os.stat_result) -> tuple[int, ...]:
    return (st.st_dev, st.st_ino, st.st_mode, st.st_uid, st.st_gid)


def pread_all(fd: int) -> bytes:
    chunks: list[bytes] = []
    offset = 0
    while True:
        block = os.pread(fd, 1 << 20, offset)
        if not block:
            return b"".join(chunks)
        chunks.append(block)
        offset += len(block)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def valid_sha(value: str) -> bool:
    return bool(re.fullmatch(r"[0-9a-f]{64}", value)) and value != "0" * 64


@dataclass(frozen=True)
class HeldIdentity:
    state: os.stat_result
    mnt_id: int


class HeldLauncher:
    def __init__(self, workspace_root: str, expected_sha256: str) -> None:
        need(workspace_root == os.path.abspath(workspace_root), "workspace root must be absolute")
        need(workspace_root == os.path.normpath(workspace_root) and workspace_root != "/",
             "workspace root must be normalized and non-root")
        need(expected_sha256 == LAUNCHER_SHA256 and valid_sha(expected_sha256),
             "r34 launcher hash pin")
        root_relative = os.fsencode(workspace_root[1:])
        clean_relative(root_relative, "workspace root")
        launcher_raw = os.fsencode(LAUNCHER_RELATIVE)
        parent_relative, basename = launcher_raw.rsplit(b"/", 1)
        self.workspace_root = workspace_root
        self.expected_sha256 = expected_sha256
        self.slash_fd = self.root_fd = self.parent_fd = self.source_fd = -1
        try:
            self.slash_fd = os.open("/", os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC |
                                    getattr(os, "O_NOFOLLOW", 0))
            self.root_fd = openat2_beneath(self.slash_fd, root_relative,
                                           os.O_RDONLY | os.O_DIRECTORY)
            self.parent_fd = openat2_beneath(self.root_fd, parent_relative,
                                             os.O_RDONLY | os.O_DIRECTORY)
            self.source_fd = openat2_beneath(self.parent_fd, basename,
                                             os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
            root_state = os.fstat(self.root_fd)
            parent_state = os.fstat(self.parent_fd)
            source_state = os.fstat(self.source_fd)
            root_label = os.lstat(workspace_root)
            parent_label = os.stat(os.fsdecode(parent_relative), dir_fd=self.root_fd,
                                   follow_symlinks=False)
            source_label = os.stat(os.fsdecode(basename), dir_fd=self.parent_fd,
                                   follow_symlinks=False)
            need(stat.S_ISDIR(root_state.st_mode) and
                 directory_identity(root_state) == directory_identity(root_label),
                 "root identity")
            need(stat.S_ISDIR(parent_state.st_mode) and
                 fingerprint(parent_state) == fingerprint(parent_label),
                 "launcher parent identity")
            need(stat.S_ISREG(source_state.st_mode) and
                 stat.S_IMODE(source_state.st_mode) == 0o444 and
                 source_state.st_nlink == 1 and
                 fingerprint(source_state) == fingerprint(source_label),
                 "r34 launcher must be regular 0444 nlink1")
            mounts = (mount_id(self.root_fd), mount_id(self.parent_fd),
                      mount_id(self.source_fd))
            need(mounts[0] == mounts[1] == mounts[2], "mount identity")
            raw = pread_all(self.source_fd)
            after = os.fstat(self.source_fd)
            need(fingerprint(source_state) == fingerprint(after), "source read drift")
            need(sha256(raw) == expected_sha256, "launcher bytes/hash")
            self.root_identity = HeldIdentity(root_state, mounts[0])
            self.parent_identity = HeldIdentity(parent_state, mounts[1])
            self.source_identity = HeldIdentity(source_state, mounts[2])
            self.raw = raw
            self.root_relative = root_relative
            self.parent_relative = parent_relative
            self.basename = basename
            self.replay()
        except BaseException:
            self.close()
            raise

    def replay(self) -> None:
        need(min(self.slash_fd, self.root_fd, self.parent_fd, self.source_fd) >= 0,
             "held descriptors live")
        root_now = os.fstat(self.root_fd)
        parent_now = os.fstat(self.parent_fd)
        source_before = os.fstat(self.source_fd)
        source_raw = pread_all(self.source_fd)
        source_after = os.fstat(self.source_fd)
        root_label = os.lstat(self.workspace_root)
        root_path_fd = openat2_beneath(self.slash_fd, self.root_relative,
                                       os.O_RDONLY | os.O_DIRECTORY)
        parent_path_fd = source_from_parent_fd = source_from_root_fd = -1
        try:
            root_path_state = os.fstat(root_path_fd)
            parent_path_fd = openat2_beneath(root_path_fd, self.parent_relative,
                                             os.O_RDONLY | os.O_DIRECTORY)
            parent_path_state = os.fstat(parent_path_fd)
            source_from_parent_fd = openat2_beneath(
                parent_path_fd, self.basename,
                os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
            source_from_root_fd = openat2_beneath(
                root_path_fd, os.fsencode(LAUNCHER_RELATIVE),
                os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
            parent_source = os.fstat(source_from_parent_fd)
            root_source = os.fstat(source_from_root_fd)
            need(fingerprint(root_now) == fingerprint(self.root_identity.state) ==
                 fingerprint(root_path_state) and
                 directory_identity(root_label) == directory_identity(self.root_identity.state) and
                 mount_id(self.root_fd) == mount_id(root_path_fd) == self.root_identity.mnt_id,
                 "root path/fd drift")
            need(fingerprint(parent_now) == fingerprint(self.parent_identity.state) ==
                 fingerprint(parent_path_state) and
                 mount_id(self.parent_fd) == mount_id(parent_path_fd) == self.parent_identity.mnt_id,
                 "parent path/fd drift")
            need(fingerprint(source_before) == fingerprint(self.source_identity.state) ==
                 fingerprint(source_after) == fingerprint(parent_source) ==
                 fingerprint(root_source) and
                 mount_id(self.source_fd) == mount_id(source_from_parent_fd) ==
                 mount_id(source_from_root_fd) == self.source_identity.mnt_id and
                 source_raw == self.raw and sha256(source_raw) == self.expected_sha256,
                 "source path/fd/hash drift")
        finally:
            for fd in (source_from_root_fd, source_from_parent_fd,
                       parent_path_fd, root_path_fd):
                if fd >= 0:
                    os.close(fd)

    def close(self) -> None:
        for name in ("source_fd", "parent_fd", "root_fd", "slash_fd"):
            fd = getattr(self, name, -1)
            if fd >= 0:
                try:
                    os.close(fd)
                finally:
                    setattr(self, name, -1)


class SealedExecutable:
    def __init__(self, raw: bytes, expected_sha256: str) -> None:
        need(hasattr(os, "memfd_create"), "memfd_create unavailable")
        self.fd = os.memfd_create("c79g-v16r2r34-external-bootstrap",
                                  MFD_CLOEXEC | MFD_ALLOW_SEALING)
        try:
            offset = 0
            while offset < len(raw):
                count = os.write(self.fd, raw[offset:])
                need(count > 0, "memfd complete write")
                offset += count
            os.fsync(self.fd)
            os.fchmod(self.fd, 0o444)
            fcntl.fcntl(self.fd, F_ADD_SEALS, REQUIRED_SEALS)
            state = os.fstat(self.fd)
            replay_state = os.fstat(self.fd)
            need(stat.S_ISREG(state.st_mode) and stat.S_IMODE(state.st_mode) == 0o444 and
                 state.st_nlink == 0 and fingerprint(state) == fingerprint(replay_state),
                 "sealed memfd identity")
            need(fcntl.fcntl(self.fd, F_GET_SEALS) == REQUIRED_SEALS,
                 "sealed memfd seals")
            need(pread_all(self.fd) == raw and sha256(raw) == expected_sha256,
                 "sealed memfd bytes/hash")
            self.identity = HeldIdentity(state, mount_id(self.fd))
            self.raw = raw
            self.expected_sha256 = expected_sha256
        except BaseException:
            self.close()
            raise

    def replay(self) -> None:
        before = os.fstat(self.fd)
        raw = pread_all(self.fd)
        after = os.fstat(self.fd)
        need(fingerprint(before) == fingerprint(self.identity.state) == fingerprint(after),
             "sealed memfd identity drift")
        need(mount_id(self.fd) == self.identity.mnt_id and
             fcntl.fcntl(self.fd, F_GET_SEALS) == REQUIRED_SEALS,
             "sealed memfd seal/mount drift")
        need(raw == self.raw and sha256(raw) == self.expected_sha256,
             "sealed memfd bytes drift")

    def close(self) -> None:
        if getattr(self, "fd", -1) >= 0:
            try:
                os.close(self.fd)
            finally:
                self.fd = -1


def forwarded(args: argparse.Namespace) -> list[str]:
    if args.command == "build":
        need(args.outdir not in (None, ""), "build --outdir required")
        return ["build", "--outdir", args.outdir]
    if args.command == "verify":
        return ["verify", "--orientation", args.orientation]
    need(args.command in {"assemble", "authorize", "reject"}, "unknown command")
    if args.command == "authorize":
        need(os.environ.get("CM2_R34_AUTHORIZE_APPROVED") == "1",
             "authorize withheld: CM2_R34_AUTHORIZE_APPROVED=1 required")
    return [args.command]


def clean_environment() -> dict[str, str]:
    env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC"}
    seed = os.environ.get("PYTHONHASHSEED")
    if seed is not None:
        need(seed == "random" or (seed.isascii() and seed.isdecimal() and
                                   0 <= int(seed) <= 4294967295),
             "invalid PYTHONHASHSEED")
        env["PYTHONHASHSEED"] = seed
    return env


def parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--workspace-root", required=True)
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


def launch(args: argparse.Namespace) -> int:
    command = forwarded(args)
    need(valid_sha(args.expected_launcher_sha256) and
         args.expected_launcher_sha256 == LAUNCHER_SHA256,
         "exact r34 launcher pin required")
    need(os.path.isfile(PYTHON) and os.access(PYTHON, os.X_OK),
         "/usr/bin/python3 unavailable")
    held = HeldLauncher(args.workspace_root, args.expected_launcher_sha256)
    sealed: SealedExecutable | None = None
    try:
        sealed = SealedExecutable(held.raw, args.expected_launcher_sha256)
        held.replay(); sealed.replay()
        inherited = (sealed.fd, held.source_fd, held.root_fd)
        need(len(set(inherited)) == 3 and all(fd >= 3 for fd in inherited),
             "three distinct non-stdio fds")
        child_argv = [
            PYTHON, "-I", "-B", "-S", "/proc/self/fd/" + str(sealed.fd),
            "--bootstrap-exec-fd", str(sealed.fd),
            "--bootstrap-source-fd", str(held.source_fd),
            "--bootstrap-root-fd", str(held.root_fd),
            "--cold-workspace-root", args.workspace_root,
            "--expected-launcher-sha256", args.expected_launcher_sha256,
            *command,
        ]
        result = subprocess.run(child_argv, close_fds=True,
                                pass_fds=inherited, env=clean_environment(),
                                check=False)
        sealed.replay(); held.replay()
        return int(result.returncode)
    finally:
        if sealed is not None:
            sealed.close()
        held.close()


def main(argv: list[str] | None = None) -> int:
    try:
        args = parser().parse_args(argv)
        return launch(args)
    except Exception as exc:
        os.write(2, ("C79G_R34_EXTERNAL_BOOTSTRAP_REJECT: " +
                     str(exc) + "\n").encode("utf-8", "backslashreplace"))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
