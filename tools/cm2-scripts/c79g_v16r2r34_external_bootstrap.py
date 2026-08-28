#!/usr/bin/env python3
"""Minimal external held-FD bootstrap for the frozen r34 cold launcher.

It does not import the launcher.  It opens the installed 0444 launcher under
an openat2-bound workspace fd, seals an identical memfd, and invokes that fd
with the three descriptors required by the launcher's self-proof.
"""
from __future__ import annotations

import argparse
import ctypes
import fcntl
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

PYTHON = "/usr/bin/python3"
ROOT_DEFAULT = "/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572"
LAUNCHER_REL = "deliverables/cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v16r2r34_semantic_source.py"
LAUNCHER_SHA = "24f9686462f47c009118887d1cdfd0f1b22791eeef335bcb64252d3ade931c0a"
RESOLVE = 0x01 | 0x02 | 0x04 | 0x08
F_ADD_SEALS = getattr(fcntl, "F_ADD_SEALS", 1033)
F_GET_SEALS = getattr(fcntl, "F_GET_SEALS", 1034)
SEALS = (getattr(fcntl, "F_SEAL_SEAL", 1) | getattr(fcntl, "F_SEAL_SHRINK", 2) |
         getattr(fcntl, "F_SEAL_GROW", 4) | getattr(fcntl, "F_SEAL_WRITE", 8))
MFD_CLOEXEC = getattr(os, "MFD_CLOEXEC", 1)
MFD_ALLOW_SEALING = getattr(os, "MFD_ALLOW_SEALING", 2)


class Refusal(RuntimeError):
    pass


def need(ok: bool, msg: str) -> None:
    if not ok:
        raise Refusal(msg)


class OpenHow(ctypes.Structure):
    _fields_ = [("flags", ctypes.c_uint64), ("mode", ctypes.c_uint64),
                ("resolve", ctypes.c_uint64)]


def openat2(dirfd: int, rel: bytes, flags: int) -> int:
    need(rel and not rel.startswith(b"/") and b".." not in rel.split(b"/"), "clean relative path")
    how = OpenHow(flags | os.O_CLOEXEC, 0, RESOLVE)
    libc = ctypes.CDLL(None, use_errno=True); libc.syscall.restype = ctypes.c_long
    fd = libc.syscall(ctypes.c_long(437), ctypes.c_int(dirfd), ctypes.c_char_p(rel), ctypes.byref(how), ctypes.c_size_t(ctypes.sizeof(how)))
    if fd < 0:
        err = ctypes.get_errno(); raise Refusal(f"openat2:{os.strerror(err)}")
    return int(fd)


def read_fd(fd: int) -> bytes:
    chunks: list[bytes] = []; offset = 0
    while True:
        block = os.pread(fd, 1 << 20, offset)
        if not block: return b"".join(chunks)
        chunks.append(block); offset += len(block)


def sealed(raw: bytes) -> int:
    need(hasattr(os, "memfd_create"), "memfd_create unavailable")
    fd = os.memfd_create("c79g-r34-external-launcher", MFD_CLOEXEC | MFD_ALLOW_SEALING)
    try:
        offset = 0
        while offset < len(raw):
            n = os.write(fd, raw[offset:]); need(n > 0, "memfd short write"); offset += n
        os.fsync(fd); os.fchmod(fd, 0o444); fcntl.fcntl(fd, F_ADD_SEALS, SEALS)
        st = os.fstat(fd)
        need(stat.S_ISREG(st.st_mode) and stat.S_IMODE(st.st_mode) == 0o444 and st.st_nlink == 0 and fcntl.fcntl(fd, F_GET_SEALS) == SEALS and read_fd(fd) == raw, "sealed launcher identity")
        return fd
    except BaseException:
        os.close(fd); raise


def parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser()
    cli.add_argument("--workspace-root", default=ROOT_DEFAULT)
    cli.add_argument("--expected-launcher-sha256", default=LAUNCHER_SHA)
    sub = cli.add_subparsers(dest="command", required=True)
    build = sub.add_parser("build"); build.add_argument("--outdir", required=True)
    verify = sub.add_parser("verify"); verify.add_argument("--orientation", choices=("a", "b"), required=True)
    for name in ("assemble", "authorize", "reject"):
        sub.add_parser(name)
    return cli


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    root = os.path.abspath(args.workspace_root)
    need(root == os.path.normpath(root) and root != "/", "normalized workspace root")
    need(args.expected_launcher_sha256 == LAUNCHER_SHA and len(LAUNCHER_SHA) == 64, "launcher pin")
    slash = rootfd = source = execfd = -1
    try:
        slash = os.open("/", os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NOFOLLOW)
        rootfd = openat2(slash, os.fsencode(root.lstrip("/")), os.O_RDONLY | os.O_DIRECTORY)
        source = openat2(rootfd, os.fsencode(LAUNCHER_REL), os.O_RDONLY | os.O_NOFOLLOW)
        st = os.fstat(source); raw = read_fd(source)
        need(stat.S_ISREG(st.st_mode) and stat.S_IMODE(st.st_mode) == 0o444 and st.st_nlink == 1 and hashlib.sha256(raw).hexdigest() == LAUNCHER_SHA, "installed launcher pin/mode")
        execfd = sealed(raw)
        if args.command == "build": forwarded = ["build", "--outdir", args.outdir]
        elif args.command == "verify": forwarded = ["verify", "--orientation", args.orientation]
        else: forwarded = [args.command]
        argv2 = [PYTHON, "-I", "-B", "-S", f"/proc/self/fd/{execfd}",
                 "--bootstrap-exec-fd", str(execfd), "--bootstrap-source-fd", str(source),
                 "--bootstrap-root-fd", str(rootfd), "--cold-workspace-root", root,
                 "--expected-launcher-sha256", LAUNCHER_SHA, *forwarded]
        env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC"}
        if "PYTHONHASHSEED" in os.environ: env["PYTHONHASHSEED"] = os.environ["PYTHONHASHSEED"]
        return subprocess.run(argv2, env=env, close_fds=True, pass_fds=(execfd, source, rootfd), check=False).returncode
    except (Refusal, OSError, ValueError) as exc:
        os.write(2, ("R34_EXTERNAL_BOOTSTRAP_REJECT: " + str(exc) + "\n").encode())
        return 2
    finally:
        for fd in (execfd, source, rootfd, slash):
            if fd >= 0:
                try: os.close(fd)
                except OSError: pass


if __name__ == "__main__":
    raise SystemExit(main())
