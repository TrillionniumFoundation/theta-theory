#!/usr/bin/env python3
"""Minimal external held-FD bootstrap for the C79g v14 cold launcher.

This file is an explicitly declared external TCB.  It never imports the
launcher.  A launch occurs only after a caller supplies an absolute workspace
root, a full lowercase SHA-256 anchor, and one exact protocol subcommand.  The
installed launcher is opened beneath held directory descriptors with Linux
``openat2``, copied byte-for-byte into a sealed memfd, and invoked as
``/usr/bin/python3 -I -B -S /proc/self/fd/EXEC``.

The child inherits exactly three non-stdio descriptors: the sealed executable
memfd, the installed source, and the workspace root.  Standard input, output,
and error are inherited unchanged, and the child's return code is returned.
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


PYTHON = "/usr/bin/python3"
LAUNCHER_RELATIVE = (
    "deliverables/"
    "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v14.py"
)

# Deliberately false: importing this module or running it without an exact
# command never executes protocol code.  Automation may make the one-site
# False -> True change after pinning this bootstrap, but the normal explicit
# CLI authorization (full launcher hash plus exact subcommand) is sufficient.
EXECUTION_ENABLED = False

RESOLVE_NO_XDEV = 0x01
RESOLVE_NO_MAGICLINKS = 0x02
RESOLVE_NO_SYMLINKS = 0x04
RESOLVE_BENEATH = 0x08
RESOLVE_FLAGS = (
    RESOLVE_NO_XDEV | RESOLVE_NO_MAGICLINKS |
    RESOLVE_NO_SYMLINKS | RESOLVE_BENEATH
)

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
REQUIRED_EXEC_SEALS = (
    F_SEAL_SEAL | F_SEAL_SHRINK | F_SEAL_GROW | F_SEAL_WRITE
)
MFD_CLOEXEC = getattr(os, "MFD_CLOEXEC", 0x0001)
MFD_ALLOW_SEALING = getattr(os, "MFD_ALLOW_SEALING", 0x0002)


class BootstrapRefusal(RuntimeError):
    """A fail-closed bootstrap refusal."""


def need(condition: bool, message: str) -> None:
    if not condition:
        raise BootstrapRefusal(message)


class OpenHow(ctypes.Structure):
    _fields_ = [
        ("flags", ctypes.c_uint64),
        ("mode", ctypes.c_uint64),
        ("resolve", ctypes.c_uint64),
    ]


class StatxTimestamp(ctypes.Structure):
    _fields_ = [
        ("tv_sec", ctypes.c_int64),
        ("tv_nsec", ctypes.c_uint32),
        ("reserved", ctypes.c_int32),
    ]


class Statx(ctypes.Structure):
    _fields_ = [
        ("stx_mask", ctypes.c_uint32),
        ("stx_blksize", ctypes.c_uint32),
        ("stx_attributes", ctypes.c_uint64),
        ("stx_nlink", ctypes.c_uint32),
        ("stx_uid", ctypes.c_uint32),
        ("stx_gid", ctypes.c_uint32),
        ("stx_mode", ctypes.c_uint16),
        ("spare0", ctypes.c_uint16),
        ("stx_ino", ctypes.c_uint64),
        ("stx_size", ctypes.c_uint64),
        ("stx_blocks", ctypes.c_uint64),
        ("stx_attributes_mask", ctypes.c_uint64),
        ("stx_atime", StatxTimestamp),
        ("stx_btime", StatxTimestamp),
        ("stx_ctime", StatxTimestamp),
        ("stx_mtime", StatxTimestamp),
        ("stx_rdev_major", ctypes.c_uint32),
        ("stx_rdev_minor", ctypes.c_uint32),
        ("stx_dev_major", ctypes.c_uint32),
        ("stx_dev_minor", ctypes.c_uint32),
        ("stx_mnt_id", ctypes.c_uint64),
        ("stx_dio_mem_align", ctypes.c_uint32),
        ("stx_dio_offset_align", ctypes.c_uint32),
        ("spare3", ctypes.c_uint64 * 12),
    ]


def libc() -> ctypes.CDLL:
    need(sys.platform.startswith("linux"), "Linux is required")
    library = ctypes.CDLL(None, use_errno=True)
    need(hasattr(library, "syscall") and hasattr(library, "statx"),
         "Linux openat2 and statx are required")
    library.syscall.restype = ctypes.c_long
    library.statx.restype = ctypes.c_int
    return library


def clean_relative(raw: bytes, label: str) -> None:
    need(raw and not raw.startswith(b"/") and b"\x00" not in raw,
         label + ": clean nonempty relative bytes")
    parts = raw.split(b"/")
    need(all(part not in (b"", b".", b"..") for part in parts),
         label + ": dot, empty, and parent components are forbidden")


def openat2_beneath(dir_fd: int, relative: str | bytes, flags: int) -> int:
    raw = relative if isinstance(relative, bytes) else os.fsencode(relative)
    clean_relative(raw, "openat2 path")
    how = OpenHow(flags | os.O_CLOEXEC, 0, RESOLVE_FLAGS)
    ctypes.set_errno(0)
    descriptor = libc().syscall(
        ctypes.c_long(437), ctypes.c_int(dir_fd), ctypes.c_char_p(raw),
        ctypes.byref(how), ctypes.c_size_t(ctypes.sizeof(how)))
    if descriptor < 0:
        code = ctypes.get_errno()
        if code == errno.ENOENT:
            raise FileNotFoundError(code, os.strerror(code), os.fsdecode(raw))
        raise BootstrapRefusal(
            "openat2 rejected " + os.fsdecode(raw) + ": " + os.strerror(code))
    return int(descriptor)


def mount_id(fd: int) -> int:
    info = Statx()
    ctypes.set_errno(0)
    outcome = libc().statx(
        ctypes.c_int(fd), ctypes.c_char_p(b""),
        ctypes.c_int(AT_EMPTY_PATH | AT_SYMLINK_NOFOLLOW),
        ctypes.c_uint(STATX_BASIC_STATS | STATX_MNT_ID), ctypes.byref(info))
    if outcome != 0:
        code = ctypes.get_errno()
        raise BootstrapRefusal("statx rejected held fd: " + os.strerror(code))
    need(bool(info.stx_mask & STATX_MNT_ID), "statx mount id is unavailable")
    return int(info.stx_mnt_id)


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
        value.st_uid, value.st_gid, value.st_size,
        value.st_mtime_ns, value.st_ctime_ns,
    )


def directory_identity(value: os.stat_result) -> tuple[int, int, int, int, int]:
    return (
        value.st_dev, value.st_ino, value.st_mode,
        value.st_uid, value.st_gid,
    )


def pread_all(fd: int) -> bytes:
    blocks: list[bytes] = []
    offset = 0
    while True:
        block = os.pread(fd, 1 << 20, offset)
        if not block:
            return b"".join(blocks)
        blocks.append(block)
        offset += len(block)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def is_sha256(value: str) -> bool:
    return (
        re.fullmatch(r"[0-9a-f]{64}", value) is not None and
        value != "0" * 64
    )


@dataclass(frozen=True)
class HeldIdentity:
    state: os.stat_result
    mnt_id: int


class HeldLauncher:
    """Hold and replay root, parent, and installed launcher identities."""

    def __init__(self, workspace_root: str, expected_sha256: str) -> None:
        need(workspace_root == os.path.abspath(workspace_root),
             "workspace root must be absolute")
        need(workspace_root == os.path.normpath(workspace_root) and
             workspace_root != "/",
             "workspace root must be normalized and non-root")
        need(is_sha256(expected_sha256),
             "expected launcher SHA-256 must be full lowercase nonzero hex")
        root_relative = os.fsencode(workspace_root[1:])
        clean_relative(root_relative, "workspace root")
        launcher_raw = os.fsencode(LAUNCHER_RELATIVE)
        clean_relative(launcher_raw, "launcher relative path")
        parent_relative, basename = launcher_raw.rsplit(b"/", 1)

        self.workspace_root = workspace_root
        self.expected_sha256 = expected_sha256
        self.slash_fd = -1
        self.root_fd = -1
        self.parent_fd = -1
        self.source_fd = -1
        try:
            self.slash_fd = os.open(
                "/", os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC |
                getattr(os, "O_NOFOLLOW", 0))
            self.root_fd = openat2_beneath(
                self.slash_fd, root_relative, os.O_RDONLY | os.O_DIRECTORY)
            self.parent_fd = openat2_beneath(
                self.root_fd, parent_relative, os.O_RDONLY | os.O_DIRECTORY)
            self.source_fd = openat2_beneath(
                self.parent_fd, basename,
                os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))

            root_state = os.fstat(self.root_fd)
            parent_state = os.fstat(self.parent_fd)
            source_before = os.fstat(self.source_fd)
            root_label_state = os.lstat(workspace_root)
            parent_path_state = os.stat(
                os.fsdecode(parent_relative), dir_fd=self.root_fd,
                follow_symlinks=False)
            source_path_state = os.stat(
                os.fsdecode(basename), dir_fd=self.parent_fd,
                follow_symlinks=False)
            need(stat.S_ISDIR(root_state.st_mode) and
                 directory_identity(root_state) ==
                     directory_identity(root_label_state),
                 "workspace root label/held-fd identity")
            need(stat.S_ISDIR(parent_state.st_mode) and
                 fingerprint(parent_state) == fingerprint(parent_path_state),
                 "launcher parent label/held-fd identity")
            need(stat.S_ISREG(source_before.st_mode) and
                 stat.S_IMODE(source_before.st_mode) == 0o444 and
                 source_before.st_nlink == 1 and
                 fingerprint(source_before) == fingerprint(source_path_state),
                 "installed launcher must be regular 0444 nlink1")

            root_mount = mount_id(self.root_fd)
            parent_mount = mount_id(self.parent_fd)
            source_mount = mount_id(self.source_fd)
            need(root_mount == parent_mount == source_mount,
                 "root, launcher parent, and source must share one mount")
            raw = pread_all(self.source_fd)
            source_after = os.fstat(self.source_fd)
            need(fingerprint(source_before) == fingerprint(source_after),
                 "installed launcher identity-bracketed read")
            need(sha256(raw) == expected_sha256,
                 "installed launcher SHA-256 mismatch")

            self.root_identity = HeldIdentity(root_state, root_mount)
            self.parent_identity = HeldIdentity(parent_state, parent_mount)
            self.source_identity = HeldIdentity(source_before, source_mount)
            self.raw = raw
            self.root_relative = root_relative
            self.parent_relative = parent_relative
            self.basename = basename
            self.replay()
        except BaseException:
            self.close()
            raise

    def replay(self) -> None:
        need(self.root_fd >= 0 and self.parent_fd >= 0 and self.source_fd >= 0,
             "held launcher is live")
        root_now = os.fstat(self.root_fd)
        parent_now = os.fstat(self.parent_fd)
        source_before = os.fstat(self.source_fd)
        source_raw = pread_all(self.source_fd)
        source_after = os.fstat(self.source_fd)
        root_label_now = os.lstat(self.workspace_root)

        root_path_fd = openat2_beneath(
            self.slash_fd, self.root_relative,
            os.O_RDONLY | os.O_DIRECTORY)
        parent_path_fd = -1
        source_from_parent_fd = -1
        source_from_root_fd = -1
        try:
            root_path_now = os.fstat(root_path_fd)
            parent_path_fd = openat2_beneath(
                root_path_fd, self.parent_relative,
                os.O_RDONLY | os.O_DIRECTORY)
            parent_path_now = os.fstat(parent_path_fd)
            source_from_parent_fd = openat2_beneath(
                parent_path_fd, self.basename,
                os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
            source_from_root_fd = openat2_beneath(
                root_path_fd, os.fsencode(LAUNCHER_RELATIVE),
                os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
            parent_source_now = os.fstat(source_from_parent_fd)
            root_source_now = os.fstat(source_from_root_fd)
            need(
                fingerprint(root_now) ==
                    fingerprint(self.root_identity.state) ==
                    fingerprint(root_path_now) and
                directory_identity(root_label_now) ==
                    directory_identity(self.root_identity.state) and
                mount_id(self.root_fd) ==
                    mount_id(root_path_fd) == self.root_identity.mnt_id,
                "workspace root path/fd/mount drift")
            need(
                fingerprint(parent_now) ==
                    fingerprint(self.parent_identity.state) ==
                    fingerprint(parent_path_now) and
                mount_id(self.parent_fd) ==
                    mount_id(parent_path_fd) == self.parent_identity.mnt_id,
                "launcher parent path/fd/mount drift")
            need(
                fingerprint(source_before) ==
                    fingerprint(self.source_identity.state) ==
                    fingerprint(source_after) ==
                    fingerprint(parent_source_now) ==
                    fingerprint(root_source_now) and
                mount_id(self.source_fd) ==
                    mount_id(source_from_parent_fd) ==
                    mount_id(source_from_root_fd) == self.source_identity.mnt_id,
                "launcher source path/fd/mount drift")
            need(source_raw == self.raw and
                 sha256(source_raw) == self.expected_sha256,
                 "launcher held bytes/hash drift")
        finally:
            for descriptor in (
                    source_from_root_fd, source_from_parent_fd,
                    parent_path_fd, root_path_fd):
                if descriptor >= 0:
                    os.close(descriptor)

    def close_noninherited(self) -> None:
        for name in ("parent_fd", "slash_fd"):
            descriptor = getattr(self, name)
            if descriptor >= 0:
                os.close(descriptor)
                setattr(self, name, -1)

    def close(self) -> None:
        for name in ("source_fd", "parent_fd", "root_fd", "slash_fd"):
            descriptor = getattr(self, name, -1)
            if descriptor >= 0:
                try:
                    os.close(descriptor)
                finally:
                    setattr(self, name, -1)


class SealedExecutable:
    def __init__(self, raw: bytes, expected_sha256: str) -> None:
        need(hasattr(os, "memfd_create"), "Linux memfd_create is required")
        self.fd = os.memfd_create(
            "c79g-v14-external-held-fd-bootstrap",
            MFD_CLOEXEC | MFD_ALLOW_SEALING)
        try:
            offset = 0
            while offset < len(raw):
                written = os.write(self.fd, raw[offset:])
                need(written > 0, "complete launcher memfd write")
                offset += written
            os.fsync(self.fd)
            os.fchmod(self.fd, 0o444)
            fcntl.fcntl(self.fd, F_ADD_SEALS, REQUIRED_EXEC_SEALS)
            state = os.fstat(self.fd)
            mnt_id = mount_id(self.fd)
            replay = pread_all(self.fd)
            replay_state = os.fstat(self.fd)
            need(stat.S_ISREG(state.st_mode) and
                 stat.S_IMODE(state.st_mode) == 0o444 and
                 state.st_nlink == 0 and
                 fingerprint(state) == fingerprint(replay_state),
                 "sealed executable exact anonymous 0444 identity")
            need(fcntl.fcntl(self.fd, F_GET_SEALS) == REQUIRED_EXEC_SEALS,
                 "sealed executable exact permanent seal set")
            need(replay == raw and sha256(replay) == expected_sha256,
                 "sealed executable exact launcher bytes/hash")
            self.identity = HeldIdentity(state, mnt_id)
            self.raw = raw
            self.expected_sha256 = expected_sha256
        except BaseException:
            self.close()
            raise

    def replay(self) -> None:
        state_before = os.fstat(self.fd)
        raw = pread_all(self.fd)
        state_after = os.fstat(self.fd)
        need(fingerprint(state_before) ==
             fingerprint(self.identity.state) == fingerprint(state_after),
             "sealed executable identity drift")
        need(mount_id(self.fd) == self.identity.mnt_id,
             "sealed executable mount drift")
        need(fcntl.fcntl(self.fd, F_GET_SEALS) == REQUIRED_EXEC_SEALS,
             "sealed executable seal drift")
        need(raw == self.raw and sha256(raw) == self.expected_sha256,
             "sealed executable byte/hash drift")

    def close(self) -> None:
        if getattr(self, "fd", -1) >= 0:
            try:
                os.close(self.fd)
            finally:
                self.fd = -1


def forwarded_command(args: argparse.Namespace) -> list[str]:
    if args.command == "build":
        need(args.outdir is not None and args.outdir != "",
             "build requires a nonempty --outdir")
        return ["build", "--outdir", args.outdir]
    if args.command == "verify":
        need(args.orientation in ("a", "b"),
             "verify requires exact orientation a or b")
        return ["verify", "--orientation", args.orientation]
    need(args.command in ("assemble", "authorize", "reject"),
         "explicit protocol subcommand required")
    return [args.command]


def clean_environment() -> dict[str, str]:
    environment = {
        "PATH": "/usr/bin:/bin",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
    }
    seed = os.environ.get("PYTHONHASHSEED")
    if seed is not None:
        need(seed == "random" or
             (seed.isascii() and seed.isdecimal() and
              0 <= int(seed) <= 4294967295),
             "PYTHONHASHSEED must be random or an integer in [0, 4294967295]")
        environment["PYTHONHASHSEED"] = seed
    return environment


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
    forwarded = forwarded_command(args)
    explicit_cli_authorization = (
        is_sha256(args.expected_launcher_sha256) and
        forwarded[0] in {"build", "verify", "assemble", "authorize", "reject"}
    )
    need(EXECUTION_ENABLED is True or explicit_cli_authorization,
         "execution requires the enable flag or an exact pinned CLI command")
    need(os.path.isfile(PYTHON) and os.access(PYTHON, os.X_OK),
         "/usr/bin/python3 executable is required")

    held = HeldLauncher(args.workspace_root, args.expected_launcher_sha256)
    sealed: SealedExecutable | None = None
    try:
        sealed = SealedExecutable(held.raw, args.expected_launcher_sha256)
        held.replay()
        sealed.replay()
        inherited = (sealed.fd, held.source_fd, held.root_fd)
        need(len(set(inherited)) == 3 and all(fd >= 3 for fd in inherited),
             "exactly three distinct non-stdio bootstrap fds")
        executable = "/proc/self/fd/" + str(sealed.fd)
        child_argv = [
            PYTHON, "-I", "-B", "-S", executable,
            "--bootstrap-exec-fd", str(sealed.fd),
            "--bootstrap-source-fd", str(held.source_fd),
            "--bootstrap-root-fd", str(held.root_fd),
            "--cold-workspace-root", args.workspace_root,
            "--expected-launcher-sha256", args.expected_launcher_sha256,
            *forwarded,
        ]
        result = subprocess.run(
            child_argv, close_fds=True, pass_fds=inherited,
            env=clean_environment(), check=False)
        sealed.replay()
        held.replay()
        return int(result.returncode)
    finally:
        if sealed is not None:
            sealed.close()
        held.close()


def main(argv: list[str] | None = None) -> int:
    try:
        args = parser().parse_args(argv)
        return launch(args)
    except (BootstrapRefusal, FileNotFoundError, OSError, ValueError) as exc:
        os.write(
            2,
            ("C79G_V14_EXTERNAL_BOOTSTRAP_REJECT: " + str(exc) + "\n").encode(
                "utf-8", "backslashreplace"))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
