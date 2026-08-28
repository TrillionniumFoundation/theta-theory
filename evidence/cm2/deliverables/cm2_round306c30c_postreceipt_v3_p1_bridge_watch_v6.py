#!/usr/bin/env python3
"""Fail-closed append-only C30c postreceipt bridge watcher v6.

This implementation retains the audited bridge-v5 authority protocol and
post-exit composite finalizer, while pinning the append-only cold analyzer v2
that correctly parses ``strace -yy`` deleted-memfd FD annotations.

Development candidate only.  Its worker output is a zero-credit boundary:
Source-W remains 80, transition/publication/terminal replay remain false, and
CM2 remains NO-GO.  A separately pinned direct-Python ExecStartPre gate
publishes the exact pinset first and the launch anchor last.  The anchor freezes
only prestart-stable service authority.  This watcher validates running state
at startup and after every stage.  Startup binds systemd MainPID and
ExecStart.pid to its own process.  Later checks continue to bind MainPID,
/proc/self/exe and the service cgroup to the same process while accepting only
systemd's exact post-daemon-reload ExecStart pid=0/n-a projection.  The worker
publishes only a non-authoritative READY marker.  Authority requires a separate
post-exit composite finalizer receipt, marker, and successful finalizer unit.
"""
from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence


sys.dont_write_bytecode = True

WORKSPACE = Path("/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572")
DELIVERABLES = WORKSPACE / "deliverables"
AUDIT = WORKSPACE / ".cm2-runtime/audit"
CONTROL = WORKSPACE / ".cm2-runtime/control"
RECEIPTS = WORKSPACE / ".cm2-runtime/receipts"
SCRATCH_PARENT = WORKSPACE / ".cm2-runtime/tmp"

WATCHER = DELIVERABLES / "cm2_round306c30c_postreceipt_v3_p1_bridge_watch_v6.py"
START_GATE = DELIVERABLES / "cm2_round306c30c_postreceipt_v3_p1_bridge_start_gate_v3.py"
COMPOSITE_FINALIZER = DELIVERABLES / (
    "cm2_round306c30c_postreceipt_v3_p1_bridge_v5_"
    "post_exit_composite_finalizer_v2.py"
)
WORKER_LAUNCHER = DELIVERABLES / (
    "cm2_round306c30c_postreceipt_v3_p1_bridge_v5_one_shot_launcher_v2.py"
)
FINALIZER_LAUNCHER = DELIVERABLES / (
    "cm2_round306c30c_postreceipt_v3_p1_bridge_v5_"
    "composite_finalizer_launcher_v2.py"
)
WRAPPER = DELIVERABLES / "cm2_round306c30c_postreceipt_bridge_v3_process_wrapper_v1.py"
VALIDATOR = DELIVERABLES / "cm2_round306c30c_62_attack_run_receipt_validator_v3.py"
PREFIX = "cm2_round306c30c_source_w_full_delta_whole_origin_disposition"
HARNESS = DELIVERABLES / (PREFIX + "_attack_harness.py")
VERIFIER = DELIVERABLES / (PREFIX + "_independent_verifier.py")
ANALYZER = DELIVERABLES / (PREFIX + "_cold_trace_analyzer_v2.py")
ANALYZER_SHA256 = "f523b413d5ac7d98a441a0bc39e00dc75f70833634709d98c15b76679ce92a94"
ANALYZER_SIZE = 29_807
PAIRING_GATE = DELIVERABLES / "cm2_round306c30c_cold_trace_unfinished_pairing_attack_gate.py"

VENV_PYTHON = WORKSPACE / ".cm2-runtime/python-flint-0.9.0/bin/python"
VENV_PYTHON3 = WORKSPACE / ".cm2-runtime/python-flint-0.9.0/bin/python3"
SYSTEM_PYTHON_LINK = Path("/usr/bin/python3")
FINAL_PYTHON = Path("/usr/bin/python3.12")
GNU_TIME = Path("/usr/bin/time")
STRACE = Path("/usr/bin/strace")
ENV_BIN = Path("/usr/bin/env")
SYSTEMCTL = Path("/usr/bin/systemctl")

# These exact shell-neutral single tokens live in the systemd fragment argv,
# not in a mutable launcher file.  systemctl's ExecStart/ExecStartPre show
# projection joins argv lossily with ASCII spaces, so the code tokens contain
# no ASCII whitespace, quote, or backslash.  Each token opens its source with
# O_NOFOLLOW, checks the fragment-approved SHA before compile, retains the FD,
# and hands executed-byte custody into the corresponding held entry.
GATE_BOOTSTRAP = (
    "s=__import__(chr(115)+chr(121)+chr(115));"
    "o=__import__(chr(111)+chr(115));"
    "h=__import__(chr(104)+chr(97)+chr(115)+chr(104)+chr(108)+chr(105)+chr(98));"
    "t=__import__(chr(116)+chr(121)+chr(112)+chr(101)+chr(115));"
    "p=s.argv[1];x=s.argv[2];"
    "f=o.open(p,o.O_RDONLY|o.O_CLOEXEC|o.O_NOFOLLOW);q=o.fstat(f);"
    "1/(((q.st_mode&61440)==32768)*((q.st_mode&4095)==292)*(q.st_nlink==1)*(q.st_uid==1000)*(q.st_gid==1000)*(0<=q.st_size<=8388608));"
    "r=o.fdopen(f,chr(114)+chr(98),closefd=False).read(8388609);"
    "1/(len(r)==q.st_size);d=h.sha256(r).hexdigest();1/(d==x);"
    "m=t.ModuleType(p);m.__file__=p;s.modules[p]=m;"
    "exec(compile(r,p,chr(101)+chr(120)+chr(101)+chr(99)),m.__dict__);"
    "s.exit(m.held_entry(f,q,r,x,s.argv[3:]))"
)
WATCHER_BOOTSTRAP = (
    "s=__import__(chr(115)+chr(121)+chr(115));"
    "o=__import__(chr(111)+chr(115));"
    "h=__import__(chr(104)+chr(97)+chr(115)+chr(104)+chr(108)+chr(105)+chr(98));"
    "t=__import__(chr(116)+chr(121)+chr(112)+chr(101)+chr(115));"
    "p=s.argv[1];x=s.argv[2];"
    "f=o.open(p,o.O_RDONLY|o.O_CLOEXEC|o.O_NOFOLLOW);q=o.fstat(f);"
    "1/(((q.st_mode&61440)==32768)*((q.st_mode&4095)==292)*(q.st_nlink==1)*(q.st_uid==1000)*(q.st_gid==1000)*(0<=q.st_size<=8388608));"
    "r=o.fdopen(f,chr(114)+chr(98),closefd=False).read(8388609);"
    "1/(len(r)==q.st_size);d=h.sha256(r).hexdigest();1/(d==x);"
    "m=t.ModuleType(p);m.__file__=p;s.modules[p]=m;"
    "exec(compile(r,p,chr(101)+chr(120)+chr(101)+chr(99)),m.__dict__);"
    "s.exit(m.held_watcher_entry(f,q,r,x,s.argv[3:]))"
)

TRANSACTION_NAME = "c30c-v5-toctou-robustness-rerun-20260808T0635Z-receipt-v3"
TRANSACTION_UNIT = "cm2-c30c-v3-20260808T0635Z.service"
TRANSACTION_INVOCATION = "93e5141a642a4016bcbedf622282ca28"
TRANSACTION_FRAGMENT = Path("/run/user/1000/systemd/transient/" + TRANSACTION_UNIT)
TRANSACTION_CONTROL = CONTROL / TRANSACTION_NAME
TRANSACTION_LAUNCHER = TRANSACTION_CONTROL / "launch.sh"
TRANSACTION_PINS = TRANSACTION_CONTROL / "pins.sha256"
RUN = AUDIT / TRANSACTION_NAME
RECEIPT = RECEIPTS / TRANSACTION_NAME

UID = 1000
RUNTIME_DIR = Path("/run/user/1000")
BUS_SOCKET = RUNTIME_DIR / "bus"
CONTROL_ENV = {
    "HOME": "/nonexistent", "PATH": "/usr/bin:/bin",
    "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
    "XDG_RUNTIME_DIR": "/run/user/1000",
    "DBUS_SESSION_BUS_ADDRESS": "unix:path=/run/user/1000/bus",
}
BASE_ENV = {
    "HOME": "/nonexistent", "PATH": "/usr/bin:/bin",
    "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC",
    "PYTHONDONTWRITEBYTECODE": "1",
}

RUN_FILES = frozenset({
    "command.txt", "end_utc.txt", "exit_code.txt", "observed_child_pids.txt",
    "post.sha256", "post.stat", "pre.sha256", "pre.stat", "provenance.json",
    "run.sh", "start_utc.txt", "stderr.log", "stdout.json", "time.txt",
    "time_pid.txt", "wrapper_pid.txt",
})
RECEIPT_FILES = frozenset({
    "build.json", "postrun-pin-check.log", "preflight-pin-check.log",
    "preflight.exit", "preflight.json", "preflight.stderr", "receipt.exit",
    "receipt.json", "receipt.stderr", "transaction-end-utc.txt",
    "transaction-run.exit",
})
CANDIDATE_FILES = frozenset({
    "cm2_round306c30b_python_flint_runtime_attestation.json",
    PREFIX + "_combined_boundary_atomic_owner_join_ledger.jsonl.gz",
    PREFIX + "_delta_h_cell_ledger.jsonl.gz",
    PREFIX + "_inherited_h_cell_ledger.jsonl.gz",
    PREFIX + "_result.json", PREFIX + "_whole_origin_ledger.jsonl.gz",
})
CANDIDATES = {
    "30630071": WORKSPACE / ".cm2-runtime/candidates/c30c-v4-seed-30630071",
    "30630929": WORKSPACE / ".cm2-runtime/candidates/c30c-v4-seed-30630929",
}

PINSET_SCHEMA = "cm2.round306c30c.postreceipt-bridge-v5-pinset.v1"
ANCHOR_SCHEMA = "cm2.round306c30c.postreceipt-bridge-v5-launch-anchor.v1"
REQUEST_SCHEMA = "cm2.round306c30c.bridge-v3-process-request.v1"
WRAPPER_RECEIPT_SCHEMA = "cm2.round306c30c.bridge-v3-process-wrapper-receipt.v1"
BOUNDARY_SCHEMA = "cm2.round306c30c.postreceipt-bridge-v5-boundary.v1"
READY_BYTES = b"READY_C30C_POSTRECEIPT_BRIDGE_V5_AWAITING_COMPOSITE_FINALIZER\n"
FAILED_BYTES = b"FAILED_C30C_POSTRECEIPT_BRIDGE_V5_FAIL_CLOSED\n"
HEX64 = re.compile(r"[0-9a-f]{64}")
UTC_LINE = re.compile(rb"20[0-9]{2}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z\n")

EXPECTED_RECEIPT_STATUS = "PASS_COMPLETE_C30C_62_ATTACK_RUN_RECEIPT_V3__ZERO_FORMAL_CREDIT"
EXPECTED_VERIFIER_STATUS = (
    "PASS_INDEPENDENT_CANDIDATE_C30C__80_DELTA_H_CELLS__"
    "2_RESOLVED_MIXED__ZERO_FORMAL_CREDIT"
)
EXPECTED_ANALYZER_STATUS = "PASS_C30C_COLD_TRACE_ZERO_PROTECTED_MUTATION"
EXPECTED_PAIRING_STATUS = "PASS_STRICT_PID_SYSCALL_PAIRING_AND_7_ATTACKS__ZERO_FORMAL_CREDIT"


class Reject(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=True, allow_nan=False, sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def closed(body: Mapping[str, Any]) -> dict[str, Any]:
    output = dict(body)
    need("object_sha256" not in output, "fresh closure")
    output["object_sha256"] = hashlib.sha256(canonical(output)).hexdigest()
    return output


def verify_closure(value: Mapping[str, Any], label: str) -> None:
    need(type(value) is dict and type(value.get("object_sha256")) is str
         and HEX64.fullmatch(value["object_sha256"]) is not None,
         "closure field:" + label)
    body = dict(value); observed = body.pop("object_sha256")
    need(hashlib.sha256(canonical(body)).hexdigest() == observed,
         "closure digest:" + label)


def exact_bool(value: Any, label: str) -> bool:
    need(type(value) is bool, "bool field:" + label)
    return value


def exact_int(value: Any, label: str) -> int:
    need(type(value) is int, "int field:" + label)
    return value


def exact_string(value: Any, label: str) -> str:
    need(type(value) is str, "string field:" + label)
    return value


def stat9(value: os.stat_result) -> dict[str, int]:
    return {
        "dev": value.st_dev, "ino": value.st_ino, "mode": value.st_mode,
        "nlink": value.st_nlink, "uid": value.st_uid, "gid": value.st_gid,
        "size": value.st_size, "mtime_ns": value.st_mtime_ns,
        "ctime_ns": value.st_ctime_ns,
    }


def identity(value: os.stat_result) -> tuple[int, ...]:
    row = stat9(value)
    return tuple(row[key] for key in (
        "dev", "ino", "mode", "nlink", "uid", "gid", "size",
        "mtime_ns", "ctime_ns",
    ))


def stable_dir_identity(value: os.stat_result) -> tuple[int, ...]:
    row = stat9(value)
    return tuple(row[key] for key in ("dev", "ino", "mode", "uid", "gid"))


def write_all(fd: int, raw: bytes) -> None:
    offset = 0
    while offset < len(raw):
        count = os.write(fd, raw[offset:])
        need(count > 0, "write-all progress")
        offset += count


def read_all(fd: int, maximum: int, singleton: bool = True) -> bytes:
    before = os.fstat(fd)
    need(stat.S_ISREG(before.st_mode)
         and (before.st_nlink == 1 if singleton else before.st_nlink in {0, 1})
         and 0 <= before.st_size <= maximum, "bounded regular FD")
    os.lseek(fd, 0, os.SEEK_SET)
    chunks: list[bytes] = []; remaining = before.st_size
    while remaining:
        block = os.read(fd, min(4 << 20, remaining))
        need(bool(block), "complete FD read")
        chunks.append(block); remaining -= len(block)
    need(os.read(fd, 1) == b"", "stable EOF")
    after = os.fstat(fd)
    need(identity(before) == identity(after), "stable regular FD")
    return b"".join(chunks)


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(
            raw.decode("ascii"),
            parse_float=lambda _: (_ for _ in ()).throw(ValueError()),
            parse_constant=lambda _: (_ for _ in ()).throw(ValueError()),
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise Reject("strict JSON:" + label) from error
    need(type(value) is dict and raw in {canonical(value), canonical(value) + b"\n"},
         "canonical JSON:" + label)
    return value


class HeldFile:
    """A raw-lstat, no-follow regular file held for the whole bridge."""
    def __init__(self, path: Path, label: str, maximum: int = 64 << 30):
        self.path = Path(os.path.abspath(os.fspath(path)))
        before = self.path.lstat()
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "raw regular singleton:" + label)
        self.fd = os.open(
            self.path, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
        )
        self.initial = os.fstat(self.fd)
        need(identity(before) == identity(self.initial), "open race:" + label)
        self.raw = read_all(self.fd, maximum)
        self.sha256 = hashlib.sha256(self.raw).hexdigest()
        self.label = label; self.maximum = maximum

    def verify(self) -> None:
        current = self.path.lstat(); held = os.fstat(self.fd)
        need(identity(current) == identity(self.initial) == identity(held),
             "held inode/full9stat drift:" + self.label)
        need(hashlib.sha256(read_all(self.fd, self.maximum)).hexdigest() == self.sha256,
             "held byte drift:" + self.label)

    def close(self) -> None:
        os.close(self.fd)


class HeldDir:
    """Directory custody; every named child operation is relative to held fd."""
    def __init__(self, path: Path, label: str, fresh: bool = False):
        self.path = Path(os.path.abspath(os.fspath(path)))
        before = self.path.lstat()
        need(stat.S_ISDIR(before.st_mode) and not stat.S_ISLNK(before.st_mode)
             and before.st_uid == UID and stat.S_IMODE(before.st_mode) == 0o700,
             "raw private owned directory:" + label)
        self.fd = os.open(
            self.path, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC
            | getattr(os, "O_NOFOLLOW", 0),
        )
        self.initial = os.fstat(self.fd); self.label = label
        need(identity(before) == identity(self.initial), "directory open race:" + label)
        if fresh:
            need(os.listdir(self.fd) == [], "fresh directory:" + label)

    def verify(self) -> None:
        current = self.path.lstat(); held = os.fstat(self.fd)
        need(stable_dir_identity(current) == stable_dir_identity(self.initial)
             == stable_dir_identity(held), "held directory/root renamed:" + self.label)

    def names(self) -> list[str]:
        self.verify(); return sorted(os.listdir(self.fd))

    def lstat(self, name: str) -> os.stat_result:
        return os.stat(name, dir_fd=self.fd, follow_symlinks=False)

    def open_regular(self, name: str, maximum: int = 64 << 30) -> tuple[bytes, dict[str, int]]:
        need(name and "/" not in name and name not in {".", ".."}, "direct regular child")
        before = self.lstat(name)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular singleton child:" + name)
        fd = os.open(name, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
                     dir_fd=self.fd)
        try:
            opened = os.fstat(fd); raw = read_all(fd, maximum); after = os.fstat(fd)
        finally:
            os.close(fd)
        path_after = self.lstat(name)
        need(identity(before) == identity(opened) == identity(after) == identity(path_after),
             "stable same-dirfd child:" + name)
        return raw, stat9(opened)

    def write_once(self, name: str, raw: bytes, mode: int = 0o400) -> dict[str, int]:
        need(name and "/" not in name and name not in {".", ".."}, "direct output child")
        self.verify()
        fd = os.open(
            name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC
            | getattr(os, "O_NOFOLLOW", 0), mode, dir_fd=self.fd,
        )
        try:
            write_all(fd, raw); os.fsync(fd); written = os.fstat(fd)
            need(stat.S_ISREG(written.st_mode) and written.st_nlink == 1,
                 "published regular singleton:" + name)
        finally:
            os.close(fd)
        observed, state = self.open_regular(name, max(len(raw), 1))
        need(observed == raw and state == stat9(written), "reopen published bytes:" + name)
        os.fsync(self.fd); self.verify()
        return state

    def write_json(self, name: str, value: Mapping[str, Any]) -> dict[str, int]:
        return self.write_once(name, canonical(dict(value)) + b"\n")

    def write_or_verify(self, name: str, raw: bytes) -> None:
        try:
            self.write_once(name, raw)
        except FileExistsError:
            observed, _ = self.open_regular(name, max(len(raw), 1))
            need(observed == raw, "existing durable child exact bytes:" + name)

    def mkdir_once(self, name: str) -> "HeldDir":
        need(name and "/" not in name and name not in {".", ".."}, "direct stage child")
        self.verify(); before = os.fstat(self.fd)
        os.mkdir(name, 0o700, dir_fd=self.fd); os.fsync(self.fd)
        after = os.fstat(self.fd)
        need(stable_dir_identity(before) == stable_dir_identity(after),
             "root identity across stage mkdir")
        child = HeldDir(self.path / name, "stage:" + name, fresh=True)
        self.verify(); return child

    def close(self) -> None:
        os.close(self.fd)


def rename_noreplace(root: HeldDir, source: str, target: str) -> None:
    need(all(name and "/" not in name and name not in {".", ".."}
             for name in (source, target)), "direct rename children")
    libc = ctypes.CDLL(None, use_errno=True)
    renameat2 = libc.renameat2
    renameat2.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int,
                          ctypes.c_char_p, ctypes.c_uint]
    renameat2.restype = ctypes.c_int
    result = renameat2(
        root.fd, source.encode("ascii"), root.fd, target.encode("ascii"), 1,
    )  # RENAME_NOREPLACE
    if result != 0:
        number = ctypes.get_errno()
        raise OSError(number, os.strerror(number))
    os.fsync(root.fd)
    root.verify()


def atomic_publish_bytes(path: Path, raw: bytes, label: str) -> dict[str, int]:
    absolute = Path(os.path.abspath(os.fspath(path)))
    need(absolute.name in {"pinset.json", "launch-anchor.json"},
         "exact v5 material basename:" + label)
    parent = HeldDir(absolute.parent, "material parent:" + label)
    prepared = "." + absolute.name + ".prepared-v5"
    try:
        names = set(parent.names())
        need(absolute.name not in names and prepared not in names,
             "fresh no-replace material:" + label)
        parent.write_once(prepared, raw)
        prepared_raw, prepared_state = parent.open_regular(
            prepared, max(len(raw), 1),
        )
        need(prepared_raw == raw, "prepared material byte replay:" + label)
        rename_noreplace(parent, prepared, absolute.name)
        published_raw, published_state = parent.open_regular(
            absolute.name, max(len(raw), 1),
        )
        stable_keys = {"dev", "ino", "mode", "nlink", "uid", "gid", "size", "mtime_ns"}
        need(published_raw == raw
             and all(published_state[key] == prepared_state[key]
                     for key in stable_keys),
             "published material byte/inode replay:" + label)
        return published_state
    finally:
        parent.close()


def recursive_snapshot(root: HeldDir) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []

    def visit(fd: int, relative: str) -> None:
        directory = os.fstat(fd)
        need(stat.S_ISDIR(directory.st_mode), "snapshot directory type")
        rows.append({"path": relative or ".", "type": "directory", "stat9": stat9(directory)})
        names = sorted(os.listdir(fd))
        for name in names:
            need(name not in {".", ".."} and "/" not in name, "snapshot child token")
            child_relative = name if not relative else relative + "/" + name
            state = os.stat(name, dir_fd=fd, follow_symlinks=False)
            if stat.S_ISREG(state.st_mode):
                need(state.st_nlink == 1, "snapshot regular singleton:" + child_relative)
                child = os.open(name, os.O_RDONLY | os.O_CLOEXEC
                                | getattr(os, "O_NOFOLLOW", 0), dir_fd=fd)
                try:
                    opened = os.fstat(child); raw = read_all(child, 64 << 30)
                    after = os.fstat(child)
                finally:
                    os.close(child)
                need(identity(state) == identity(opened) == identity(after),
                     "snapshot stable file:" + child_relative)
                rows.append({
                    "path": child_relative, "type": "regular",
                    "sha256": hashlib.sha256(raw).hexdigest(), "stat9": stat9(opened),
                })
            elif stat.S_ISDIR(state.st_mode):
                child = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC
                                | getattr(os, "O_NOFOLLOW", 0), dir_fd=fd)
                try:
                    need(identity(state) == identity(os.fstat(child)),
                         "snapshot directory race:" + child_relative)
                    visit(child, child_relative)
                finally:
                    os.close(child)
            else:
                raise Reject("snapshot rejects symlink/special:" + child_relative)

    root.verify(); visit(root.fd, "") ; root.verify()
    return closed({
        "schema": "cm2.round306c30c.bridge-v3-recursive-snapshot.v1",
        "rows": rows, "row_count": len(rows),
        "formal_credit": 0, "source_W_formal_remainder": 80,
        "source_W_transition_authorized": False,
        "publication_authorized": False, "terminal_replay_completed": False,
    })


def verify_snapshot_extension(
    before: Mapping[str, Any], after: Mapping[str, Any], added_name: str,
) -> None:
    verify_closure(before, "snapshot before extension")
    verify_closure(after, "snapshot after extension")
    old = {row["path"]: row for row in before["rows"]}
    new = {row["path"]: row for row in after["rows"]}
    need(set(new) == set(old) | {added_name}, "recursive exact one-file extension")
    need(new[added_name]["type"] == "regular", "snapshot extension regular")
    for path, row in old.items():
        if path == ".":
            old_stat = row["stat9"]; new_stat = new[path]["stat9"]
            need(tuple(old_stat[key] for key in ("dev", "ino", "mode", "uid", "gid"))
                 == tuple(new_stat[key] for key in ("dev", "ino", "mode", "uid", "gid")),
                 "snapshot root identity across extension")
        else:
            need(new[path] == row, "recursive prior member full9stat/hash stable:" + path)


def zero_contract(value: Mapping[str, Any], label: str) -> None:
    need("formal_credit" in value and exact_int(value["formal_credit"], label + ":credit") == 0,
         "zero credit:" + label)
    need("source_W_formal_remainder" in value
         and exact_int(value["source_W_formal_remainder"], label + ":remainder") == 80,
         "remainder 80:" + label)
    for key in ("source_W_transition_authorized", "publication_authorized",
                "terminal_replay_completed"):
        need(key in value and exact_bool(value[key], label + ":" + key) is False,
             "explicit false:" + label + ":" + key)


class RuntimeAuthority:
    """Hold the runtime route without freezing shared-directory timestamps.

    /run/user/UID is shared by every user service, so its size, nlink, mtime and
    ctime are not authority and legitimately change during a long verifier.
    Its path/held-FD dev+ino+type+mode+owner remain frozen.  The bus socket and
    systemctl executable retain full identity/byte custody.
    """
    def __init__(self) -> None:
        need(os.getuid() == UID and os.geteuid() == UID, "exact bridge uid/euid")
        runtime_before = RUNTIME_DIR.lstat()
        need(stat.S_ISDIR(runtime_before.st_mode) and runtime_before.st_uid == UID,
             "owned runtime directory")
        self.runtime_fd = os.open(
            RUNTIME_DIR, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC
            | getattr(os, "O_NOFOLLOW", 0),
        )
        self.runtime_state = os.fstat(self.runtime_fd)
        need(identity(runtime_before) == identity(self.runtime_state), "runtime open race")
        self.runtime_stable_identity = stable_dir_identity(self.runtime_state)
        socket_before = BUS_SOCKET.lstat()
        need(stat.S_ISSOCK(socket_before.st_mode) and socket_before.st_uid == UID,
             "owned real bus socket")
        self.socket_fd = os.open(
            BUS_SOCKET, getattr(os, "O_PATH", os.O_RDONLY) | os.O_CLOEXEC
            | getattr(os, "O_NOFOLLOW", 0),
        )
        self.socket_state = os.fstat(self.socket_fd)
        need(identity(socket_before) == identity(self.socket_state), "bus socket open race")
        self.systemctl = HeldFile(SYSTEMCTL, "systemctl final path", 64 << 20)
        self.baseline = closed({
            "schema": "cm2.round306c30c.bridge-v3-runtime-authority.v1",
            "uid": UID, "runtime_path": os.fspath(RUNTIME_DIR),
            "runtime_stat9": stat9(self.runtime_state),
            "runtime_stable_identity_fields": [
                "dev", "ino", "mode", "uid", "gid",
            ],
            "socket_path": os.fspath(BUS_SOCKET),
            "socket_stat9": stat9(self.socket_state),
            "systemctl_path": os.fspath(SYSTEMCTL),
            "systemctl_sha256": self.systemctl.sha256,
            "systemctl_stat9": stat9(self.systemctl.initial),
            "control_env": dict(CONTROL_ENV),
            "formal_credit": 0, "source_W_formal_remainder": 80,
            "source_W_transition_authorized": False,
            "publication_authorized": False, "terminal_replay_completed": False,
        })

    def verify(self) -> None:
        runtime_current = RUNTIME_DIR.lstat(); runtime_held = os.fstat(self.runtime_fd)
        socket_current = BUS_SOCKET.lstat(); socket_held = os.fstat(self.socket_fd)
        need(stable_dir_identity(runtime_current)
             == self.runtime_stable_identity
             == stable_dir_identity(runtime_held),
             "runtime stable path/held-FD identity drift")
        need(identity(socket_current) == identity(self.socket_state)
             == identity(socket_held), "bus socket full identity drift")
        self.systemctl.verify()

    def query(self, unit: str, properties: Sequence[str]) -> tuple[dict[str, str], bytes]:
        self.verify()
        command = [os.fspath(SYSTEMCTL), "--user", "show", unit]
        for key in properties:
            command.extend(["-p", key])
        completed = subprocess.run(
            command, cwd=WORKSPACE, env=CONTROL_ENV, stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        self.verify()
        need(completed.returncode == 0 and completed.stderr == b"",
             "clean held-bus systemctl query")
        fields = parse_systemctl(completed.stdout)
        need(set(fields) == set(properties), "exact systemctl property set")
        return fields, completed.stdout

    def close(self) -> None:
        self.systemctl.close(); os.close(self.socket_fd); os.close(self.runtime_fd)


def parse_systemctl(raw: bytes) -> dict[str, str]:
    try:
        rows = raw.decode("ascii").splitlines()
    except UnicodeDecodeError as error:
        raise Reject("systemctl ASCII") from error
    output: dict[str, str] = {}
    for row in rows:
        key, separator, value = row.partition("=")
        need(separator == "=" and key and key not in output,
             "unique systemctl property")
        output[key] = value
    return output


SYSTEMD_SHOW_FORBIDDEN_ARG_BYTES = frozenset(b"'\"\\$%")


def exact_systemd_show_argv(
    expected_argv: Sequence[str], label: str,
) -> list[str]:
    expected = list(expected_argv)
    need(expected and all(type(item) is str and item for item in expected),
         "nonempty exact argv tokens:" + label)
    for item in expected:
        try:
            encoded = item.encode("ascii")
        except UnicodeEncodeError as error:
            raise Reject("ASCII exact argv token:" + label) from error
        need(all(0x21 <= byte <= 0x7e for byte in encoded)
             and not (set(encoded) & SYSTEMD_SHOW_FORBIDDEN_ARG_BYTES)
             and item != ";",
             "systemd-show-lossless argv token:" + label)
    return expected


def parse_exec_command(
    raw: str, expected_argv: Sequence[str], expected_path: Path,
    require_started: bool, label: str,
    allow_started_projection_decay: bool = False,
) -> dict[str, Any]:
    match = re.fullmatch(
        r"\{ path=([^ ;]+) ; argv\[\]=(.+) ; ignore_errors=no ; "
        r"start_time=\[(.*)\] ; stop_time=\[(.*)\] ; pid=([0-9]+) ; "
        r"code=([^ ;]+) ; status=([^ }]+) \}", raw,
    )
    need(match is not None, "strict exec command syntax:" + label)
    path, argv_text, start, stop, pid, code, status_text = match.groups()
    argv = exact_systemd_show_argv(expected_argv, label)
    need(argv_text == " ".join(argv),
         "systemd-show exact raw argv join:" + label)
    need(path == os.fspath(expected_path),
         "direct exact exec command:" + label)
    parsed_pid = int(pid)
    if require_started:
        live_projection = start not in {"", "n/a"} and parsed_pid > 1
        decayed_projection = (
            allow_started_projection_decay and parsed_pid == 0
            and start == "n/a" and stop == "n/a" and code == "(null)"
            and status_text in {"0", "0/0"}
        )
        need(live_projection or decayed_projection,
             "started or exact manager-reload-decayed exec projection:" + label)
    else:
        need(parsed_pid >= 0, "nonnegative exec command pid:" + label)
    return {
        "path": path, "argv": argv, "start_time": start, "stop_time": stop,
        "pid": parsed_pid, "code": code, "status": status_text,
    }


def parse_execstart(raw: str, expected_argv: Sequence[str]) -> dict[str, Any]:
    return parse_exec_command(
        raw, expected_argv, FINAL_PYTHON, True, "ExecStart",
    )


def validate_future_exec_projection(
    command: Mapping[str, Any], label: str,
) -> None:
    need(command.get("pid") == 0
         and command.get("start_time") == "n/a"
         and command.get("stop_time") == "n/a"
         and command.get("code") == "(null)"
         and command.get("status") in {"0", "0/0"},
         "exact future-not-started exec projection:" + label)


def validate_live_exec_projection(
    command: Mapping[str, Any], process_pid: int, label: str,
) -> None:
    need(command.get("pid") == process_pid
         and command.get("start_time") not in {None, "", "n/a"}
         and command.get("stop_time") == "n/a"
         and command.get("code") == "(null)"
         and command.get("status") in {"0", "0/0"},
         "exact live exec projection:" + label)


def validate_completed_exec_projection(
    command: Mapping[str, Any], label: str,
) -> None:
    need(type(command.get("pid")) is int and command["pid"] > 1
         and command.get("start_time") not in {None, "", "n/a"}
         and command.get("stop_time") not in {None, "", "n/a"}
         and command.get("code") == "exited"
         and command.get("status") in {"0", "0/0"},
         "exact clean completed exec projection:" + label)


def expected_watcher_argv(
    bridge: Path, pinset: Path, anchor: Path, unit: str, maximum_wait: int,
    source_sha256: str,
) -> list[str]:
    need(HEX64.fullmatch(source_sha256) is not None, "watcher bootstrap source SHA")
    argv = [
        os.fspath(FINAL_PYTHON), "-I", "-B", "-c", WATCHER_BOOTSTRAP,
        os.fspath(WATCHER), source_sha256, "--run",
        "--bridge-dir", os.fspath(bridge), "--pinset", os.fspath(pinset),
        "--anchor", os.fspath(anchor), "--unit", unit,
        "--maximum-wait-seconds", str(maximum_wait),
    ]
    return exact_systemd_show_argv(argv, "expected watcher")


def expected_gate_argv(
    bridge: Path, pinset: Path, anchor: Path, unit: str, maximum_wait: int,
    source_sha256: str, watcher_source_sha256: str,
) -> list[str]:
    need(HEX64.fullmatch(source_sha256) is not None, "gate bootstrap source SHA")
    need(HEX64.fullmatch(watcher_source_sha256) is not None,
         "gate approved watcher source SHA")
    argv = [
        os.fspath(FINAL_PYTHON), "-I", "-B", "-c", GATE_BOOTSTRAP,
        os.fspath(START_GATE), source_sha256, "--publish",
        "--bridge-dir", os.fspath(bridge), "--pinset", os.fspath(pinset),
        "--anchor", os.fspath(anchor), "--unit", unit,
        "--maximum-wait-seconds", str(maximum_wait),
        "--watcher-source-sha256", watcher_source_sha256,
    ]
    return exact_systemd_show_argv(argv, "expected gate")


def bootstrap_source_state_allowed(
    mode: int, nlink: int, uid: int, gid: int, size: int,
) -> bool:
    return bool(
        (mode & 61440) == 32768 and (mode & 4095) == 292
        and nlink == 1 and uid == UID and gid == UID
        and 0 <= size <= 8388608
    )


def validate_invocation_binding(authority: str, environment: str | None,
                                label: str) -> None:
    need(re.fullmatch(r"[0-9a-f]{32}", authority) is not None,
         "authoritative InvocationID:" + label)
    need(type(environment) is str and environment == authority,
         "INVOCATION_ID environment/authority closure:" + label)


def regular_observation(path: Path, label: str, maximum: int = 64 << 30) -> dict[str, Any]:
    held = HeldFile(path, label, maximum)
    try:
        held.verify()
        return {
            "path": os.fspath(held.path), "kind": "regular",
            "sha256": held.sha256, "stat9": stat9(held.initial),
        }
    finally:
        held.close()


def symlink_observation(path: Path, label: str) -> dict[str, Any]:
    absolute = Path(os.path.abspath(os.fspath(path)))
    before = absolute.lstat()
    need(stat.S_ISLNK(before.st_mode) and before.st_nlink == 1,
         "singleton symlink:" + label)
    target = os.readlink(absolute); after = absolute.lstat()
    need(identity(before) == identity(after), "stable symlink:" + label)
    return {"path": os.fspath(absolute), "kind": "symlink",
            "target": target, "stat9": stat9(before)}


def directory_observation(path: Path, label: str) -> dict[str, Any]:
    absolute = Path(os.path.abspath(os.fspath(path)))
    before = absolute.lstat()
    need(stat.S_ISDIR(before.st_mode) and not stat.S_ISLNK(before.st_mode),
         "real directory:" + label)
    fd = os.open(absolute, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC
                 | getattr(os, "O_NOFOLLOW", 0))
    try:
        opened = os.fstat(fd); names = sorted(os.listdir(fd)); after = os.fstat(fd)
    finally:
        os.close(fd)
    path_after = absolute.lstat()
    need(identity(before) == identity(opened) == identity(after) == identity(path_after),
         "stable directory inventory:" + label)
    return {"path": os.fspath(absolute), "kind": "directory",
            "inventory": names, "stat9": stat9(opened)}


def observe_pin(row: Mapping[str, Any]) -> dict[str, Any]:
    need(type(row) is dict and set(row) >= {"role", "path", "kind", "stat9"},
         "pin row base shape")
    role = exact_string(row.get("role"), "pin role")
    path = Path(exact_string(row.get("path"), "pin path"))
    need(path.is_absolute(), "absolute pin path:" + role)
    kind = row.get("kind")
    if kind == "regular":
        need(set(row) == {"role", "path", "kind", "sha256", "stat9"}
             and type(row.get("sha256")) is str
             and HEX64.fullmatch(row["sha256"]) is not None,
             "regular pin exact shape:" + role)
        observed = regular_observation(path, "pin:" + role)
    elif kind == "symlink":
        need(set(row) == {"role", "path", "kind", "target", "stat9"},
             "symlink pin exact shape:" + role)
        observed = symlink_observation(path, "pin:" + role)
    elif kind == "directory":
        need(set(row) == {"role", "path", "kind", "inventory", "stat9"}
             and type(row.get("inventory")) is list,
             "directory pin exact shape:" + role)
        observed = directory_observation(path, "pin:" + role)
    else:
        raise Reject("unknown pin kind:" + role)
    observed["role"] = role
    need(observed == dict(row), "current pin byte/type/full9stat:" + role)
    return observed


def make_pin_observation(role: str, path: Path) -> dict[str, Any]:
    need(re.fullmatch(r"[a-z0-9_]{1,96}", role) is not None,
         "pin role token")
    absolute = Path(os.path.abspath(os.fspath(path)))
    state = absolute.lstat()
    if stat.S_ISREG(state.st_mode):
        observed = regular_observation(absolute, "gate pin:" + role)
    elif stat.S_ISLNK(state.st_mode):
        observed = symlink_observation(absolute, "gate pin:" + role)
    elif stat.S_ISDIR(state.st_mode):
        observed = directory_observation(absolute, "gate pin:" + role)
    else:
        raise Reject("unsupported gate pin kind:" + role)
    observed["role"] = role
    return observed


def required_pin_roles(bridge_fragment: Path) -> dict[str, Path]:
    roles: dict[str, Path] = {
        "bridge_watcher": WATCHER, "bridge_start_gate": START_GATE,
        "bridge_composite_finalizer": COMPOSITE_FINALIZER,
        "bridge_worker_launcher": WORKER_LAUNCHER,
        "bridge_finalizer_launcher": FINALIZER_LAUNCHER,
        "process_wrapper": WRAPPER,
        "receipt_validator": VALIDATOR, "attack_harness": HARNESS,
        "independent_verifier": VERIFIER, "cold_analyzer": ANALYZER,
        "pairing_gate": PAIRING_GATE, "venv_python": VENV_PYTHON,
        "venv_python3": VENV_PYTHON3, "system_python_link": SYSTEM_PYTHON_LINK,
        "final_python": FINAL_PYTHON, "gnu_time": GNU_TIME,
        "strace": STRACE, "env": ENV_BIN, "systemctl": SYSTEMCTL,
        "transaction_launcher": TRANSACTION_LAUNCHER,
        "transaction_pins": TRANSACTION_PINS,
        "transaction_fragment": TRANSACTION_FRAGMENT,
        "bridge_fragment": bridge_fragment,
        "transaction_run_dir": RUN, "transaction_receipt_dir": RECEIPT,
    }
    for seed, candidate in CANDIDATES.items():
        roles["candidate_dir_" + seed] = candidate
        for index, name in enumerate(sorted(CANDIDATE_FILES)):
            roles[f"candidate_{seed}_{index:02d}"] = candidate / name
    for index, name in enumerate(sorted(RUN_FILES)):
        roles[f"transaction_run_{index:02d}"] = RUN / name
    for index, name in enumerate(sorted(RECEIPT_FILES)):
        roles[f"transaction_receipt_{index:02d}"] = RECEIPT / name
    return roles


BRIDGE_STABLE_ANCHOR_FIELDS = frozenset({
    "Id", "InvocationID", "ExecStart", "ExecStartPre", "FragmentPath",
    "FragmentSHA256", "FragmentStat9", "LoadState", "Type",
    "RemainAfterExit", "StandardOutput", "StandardError",
})


def validate_bridge_anchor_projection(service: Mapping[str, Any]) -> None:
    need(type(service) is dict and set(service) == BRIDGE_STABLE_ANCHOR_FIELDS,
         "exact prestart-stable bridge anchor projection")
    for command in ("ExecStart", "ExecStartPre"):
        need(type(service.get(command)) is list
             and all(type(item) is str for item in service[command]),
             "exact bridge command argv:" + command)
    for forbidden in (
        "ActiveState", "SubState", "Result", "ExecMainCode",
        "ExecMainStatus", "MainPID", "ControlPID",
    ):
        need(forbidden not in service, "live field forbidden in anchor:" + forbidden)


def parse_anchor(held: HeldFile) -> dict[str, Any]:
    need(all(token not in os.fspath(held.path)
             for token in ("bridge-v1", "bridge-v2", "bridge-v3")),
         "reject old anchor path")
    value = strict_json(held.raw, "launch anchor"); verify_closure(value, "launch anchor")
    required = {
        "schema", "status", "watcher_path", "watcher_sha256", "watcher_stat9",
        "gate_path", "gate_sha256", "gate_stat9",
        "wrapper_path", "wrapper_sha256", "wrapper_stat9", "pinset_path",
        "pinset_sha256", "pinset_stat9", "bridge_dir", "bridge_service",
        "transaction_service", "formal_credit", "source_W_formal_remainder",
        "source_W_transition_authorized", "publication_authorized",
        "terminal_replay_completed", "object_sha256",
    }
    need(set(value) == required and value.get("schema") == ANCHOR_SCHEMA
         and value.get("status")
         == "FROZEN_BRIDGE_V5_PRESTART_GATE_ZERO_CREDIT",
         "exact v5 anchor schema/fields")
    zero_contract(value, "anchor")
    for name in ("watcher_sha256", "gate_sha256", "wrapper_sha256", "pinset_sha256"):
        need(type(value.get(name)) is str and HEX64.fullmatch(value[name]) is not None,
             "anchor SHA:" + name)
    for name in ("watcher_stat9", "gate_stat9", "wrapper_stat9", "pinset_stat9"):
        need(type(value.get(name)) is dict and set(value[name]) == set(stat9(os.stat_result((0,) * 10))),
             "anchor stat9:" + name)
    for service_name in ("bridge_service", "transaction_service"):
        service = value.get(service_name)
        need(type(service) is dict, "anchor service object:" + service_name)
    bridge_service = value["bridge_service"]
    validate_bridge_anchor_projection(bridge_service)
    transaction = value["transaction_service"]
    required_transaction = {
        "Id", "InvocationID", "ExecStart", "FragmentPath", "FragmentSHA256",
        "FragmentStat9", "LoadState", "ActiveState", "SubState", "Result",
        "ExecMainCode", "ExecMainStatus", "MainPID", "Type", "RemainAfterExit",
        "StandardOutput", "StandardError",
    }
    need(set(transaction) == required_transaction,
         "exact transaction service anchor fields")
    return value


def load_pinset(held: HeldFile, expected_sha: str, anchor: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    need(all(token not in os.fspath(held.path)
             for token in ("bridge-v1", "bridge-v2", "bridge-v3")),
         "reject old pinset path")
    need(type(expected_sha) is str and HEX64.fullmatch(expected_sha) is not None
         and held.sha256 == expected_sha, "pinset CLI SHA")
    value = strict_json(held.raw, "pinset"); verify_closure(value, "pinset")
    need(set(value) == {
        "schema", "status", "members", "formal_credit", "source_W_formal_remainder",
        "source_W_transition_authorized", "publication_authorized",
        "terminal_replay_completed", "object_sha256",
    } and value.get("schema") == PINSET_SCHEMA
        and value.get("status") == "FROZEN_EXACT_ROLE_SET_BRIDGE_V5_ZERO_CREDIT",
        "exact v5 pinset schema")
    zero_contract(value, "pinset")
    rows = value.get("members")
    need(type(rows) is list and all(type(row) is dict for row in rows), "pinset member list")
    observations: dict[str, dict[str, Any]] = {}
    for row in rows:
        observed = observe_pin(row); role = observed["role"]
        need(role not in observations, "unique pin role:" + role)
        observations[role] = observed
    fragment = Path(anchor["bridge_service"]["FragmentPath"])
    expected_roles = required_pin_roles(fragment)
    need(set(observations) == set(expected_roles), "pinset exact role set")
    for role, path in expected_roles.items():
        need(observations[role]["path"] == os.fspath(Path(os.path.abspath(os.fspath(path)))),
             "pin exact role path:" + role)
    need(observations["venv_python"]["kind"] == "symlink"
         and observations["venv_python"]["target"] == "python3"
         and observations["venv_python3"]["kind"] == "symlink"
         and observations["venv_python3"]["target"] == "/usr/bin/python3"
         and observations["system_python_link"]["kind"] == "symlink"
         and observations["system_python_link"]["target"] == "python3.12"
         and VENV_PYTHON.resolve(strict=True) == FINAL_PYTHON,
         "exact final Python symlink chain")
    return value, observations


TRANSACTION_SERVICE_PROPERTIES = (
    "Id", "InvocationID", "ExecStart", "FragmentPath", "LoadState",
    "ActiveState", "SubState", "Result", "ExecMainCode", "ExecMainStatus",
    "MainPID", "Type", "RemainAfterExit", "StandardOutput", "StandardError",
)
BRIDGE_SERVICE_PROPERTIES = (
    "Id", "InvocationID", "ExecStart", "ExecStartPre", "FragmentPath",
    "LoadState", "ActiveState", "SubState", "Result", "ExecMainCode",
    "ExecMainStatus", "MainPID", "ControlPID", "Type", "RemainAfterExit",
    "StandardOutput", "StandardError",
)
BRIDGE_STABLE_PROPERTIES = (
    "Id", "InvocationID", "FragmentPath", "LoadState", "Type",
    "RemainAfterExit", "StandardOutput", "StandardError",
)


def validate_anchor_bindings(
    anchor: Mapping[str, Any], anchor_file: HeldFile, pinset_file: HeldFile,
    self_file: HeldFile, gate_file: HeldFile, wrapper_file: HeldFile,
    bridge: HeldDir,
) -> None:
    need(anchor.get("watcher_path") == os.fspath(WATCHER)
         and anchor.get("watcher_sha256") == self_file.sha256
         and anchor.get("watcher_stat9") == stat9(self_file.initial),
         "anchor watcher byte/full9stat binding")
    need(anchor.get("gate_path") == os.fspath(START_GATE)
         and anchor.get("gate_sha256") == gate_file.sha256
         and anchor.get("gate_stat9") == stat9(gate_file.initial),
         "anchor start-gate byte/full9stat binding")
    need(anchor.get("wrapper_path") == os.fspath(WRAPPER)
         and anchor.get("wrapper_sha256") == wrapper_file.sha256
         and anchor.get("wrapper_stat9") == stat9(wrapper_file.initial),
         "anchor wrapper byte/full9stat binding")
    need(anchor.get("pinset_path") == os.fspath(pinset_file.path)
         and anchor.get("pinset_sha256") == pinset_file.sha256
         and anchor.get("pinset_stat9") == stat9(pinset_file.initial),
         "anchor pinset byte/full9stat binding")
    need(anchor.get("bridge_dir") == os.fspath(bridge.path), "anchor bridge root")
    expected_argv = anchor["bridge_service"]["ExecStart"]
    need(len(expected_argv) == 18
        and re.fullmatch(r"[0-9]+", expected_argv[-1]) is not None
        and 0 <= int(expected_argv[-1]) <= 7 * 24 * 3600,
         "bounded watcher argv wait")
    maximum_wait = int(expected_argv[-1])
    need(expected_argv == expected_watcher_argv(
            bridge.path, pinset_file.path, anchor_file.path,
            anchor["bridge_service"]["Id"], maximum_wait, self_file.sha256,
         )
        and "/bin/sh" not in expected_argv and os.fspath(WRAPPER) not in expected_argv,
         "direct final Python exact watcher ExecStart argv")
    expected_pre = anchor["bridge_service"]["ExecStartPre"]
    need(expected_pre == expected_gate_argv(
            bridge.path, pinset_file.path, anchor_file.path,
            anchor["bridge_service"]["Id"], maximum_wait, gate_file.sha256,
            self_file.sha256,
         )
         and "/bin/sh" not in expected_pre and os.fspath(WRAPPER) not in expected_pre,
         "direct final Python exact gate ExecStartPre argv")
    validate_invocation_binding(
        anchor["bridge_service"]["InvocationID"],
        os.environ.get("INVOCATION_ID"), "watcher",
    )


def validate_service(
    runtime: RuntimeAuthority, expected: Mapping[str, Any],
    expected_argv: Sequence[str] | None, fragment_held: HeldFile,
    label: str,
) -> dict[str, Any]:
    unit = exact_string(expected.get("Id"), label + ":Id")
    fields, raw = runtime.query(unit, TRANSACTION_SERVICE_PROPERTIES)
    for key in TRANSACTION_SERVICE_PROPERTIES:
        if key == "ExecStart":
            continue
        need(type(expected.get(key)) is str and fields[key] == expected[key],
             "service exact field:" + label + ":" + key)
    if expected_argv is not None:
        execstart = parse_execstart(fields["ExecStart"], expected_argv)
    else:
        need(type(expected.get("ExecStart")) is str
             and fields["ExecStart"] == expected["ExecStart"],
             "transaction exact ExecStart raw")
        execstart = {"raw": fields["ExecStart"]}
    need(fields["FragmentPath"] == os.fspath(fragment_held.path),
         "service fragment exact path:" + label)
    fragment_held.verify()
    need(expected.get("FragmentSHA256") == fragment_held.sha256
         and expected.get("FragmentStat9") == stat9(fragment_held.initial),
         "service fragment SHA/full9stat:" + label)
    return closed({
        "schema": "cm2.round306c30c.bridge-v5-transaction-service-attestation.v1",
        "status": "PASS_EXACT_SYSTEMD_SERVICE_AND_FRAGMENT",
        "label": label, "properties": fields, "execstart": execstart,
        "systemctl_stdout_sha256": hashlib.sha256(raw).hexdigest(),
        "fragment_sha256": fragment_held.sha256,
        "fragment_stat9": stat9(fragment_held.initial),
        "runtime_authority_object_sha256": runtime.baseline["object_sha256"],
        "formal_credit": 0, "source_W_formal_remainder": 80,
        "source_W_transition_authorized": False,
        "publication_authorized": False, "terminal_replay_completed": False,
    })


def validate_running_live_fields(
    fields: Mapping[str, str], execstart: Mapping[str, Any],
    process_pid: int, allow_execstart_projection_decay: bool = False,
) -> dict[str, Any]:
    need(type(process_pid) is int and process_pid > 1, "real watcher process pid")
    need(fields.get("ActiveState") == "active", "bridge live ActiveState=active")
    need(fields.get("SubState") == "running", "bridge live SubState=running")
    need(fields.get("Result") == "success", "bridge live Result=success")
    need(fields.get("ExecMainCode") == "0", "bridge live ExecMainCode=0")
    need(fields.get("ExecMainStatus") == "0", "bridge live ExecMainStatus=0")
    need(fields.get("ControlPID") == "0", "bridge live ControlPID=0")
    main_pid = exact_int(int(exact_string(fields.get("MainPID"), "MainPID")),
                         "MainPID integer")
    exec_pid = exact_int(execstart.get("pid"), "ExecStart pid")
    need(main_pid == process_pid,
         "MainPID == os.getpid outer-process binding")
    if allow_execstart_projection_decay and exec_pid == 0:
        need(execstart.get("start_time") == "n/a"
             and execstart.get("stop_time") == "n/a"
             and execstart.get("code") == "(null)"
             and execstart.get("status") in {"0", "0/0"},
             "exact systemd manager-reload ExecStart zero projection")
        projection = "manager-reload-decayed-zero"
    else:
        validate_live_exec_projection(execstart, process_pid, "ExecStart")
        projection = "live-pid-bound"
    return {
        "phase": "running", "ActiveState": fields["ActiveState"],
        "SubState": fields["SubState"], "Result": fields["Result"],
        "ExecMainCode": fields["ExecMainCode"],
        "ExecMainStatus": fields["ExecMainStatus"],
        "MainPID": main_pid, "ControlPID": 0,
        "ExecStartPID": exec_pid,
        "ExecStartProjection": projection,
        "outer_process_binding": True,
    }


def validate_outer_proc_binding(process_pid: int, unit: str) -> dict[str, Any]:
    need(type(process_pid) is int and process_pid == os.getpid() and process_pid > 1,
         "outer /proc binding uses current watcher PID")
    need(type(unit) is str and re.fullmatch(
        r"cm2-c30c-postreceipt-v3-p1-bridge-v5-[A-Za-z0-9_.:-]+\.service",
        unit,
    ) is not None, "outer /proc binding exact v5 unit")
    proc = Path("/proc") / str(process_pid)
    exe_link = os.readlink(proc / "exe")
    exe_state = (proc / "exe").stat()
    final_state = FINAL_PYTHON.stat()
    need(exe_link == os.fspath(FINAL_PYTHON)
         and (exe_state.st_dev, exe_state.st_ino)
             == (final_state.st_dev, final_state.st_ino),
         "outer /proc exe == final Python inode")
    cgroup_fd = os.open(
        proc / "cgroup", os.O_RDONLY | os.O_CLOEXEC
        | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        chunks: list[bytes] = []
        total = 0
        while True:
            block = os.read(cgroup_fd, 4096)
            if not block:
                break
            total += len(block)
            need(total <= 65536, "bounded outer cgroup projection")
            chunks.append(block)
    finally:
        os.close(cgroup_fd)
    cgroup_raw = b"".join(chunks)
    try:
        cgroup_text = cgroup_raw.decode("ascii")
    except UnicodeDecodeError as error:
        raise Reject("outer cgroup ASCII") from error
    rows = cgroup_text.splitlines()
    expected_suffix = "/" + unit
    need(len(rows) == 1 and rows[0].startswith("0::/")
         and rows[0].endswith(expected_suffix),
         "outer watcher exact unified service cgroup")
    return {
        "pid": process_pid,
        "proc_exe_link": exe_link,
        "proc_exe_stat9": stat9(exe_state),
        "proc_cgroup_sha256": hashlib.sha256(cgroup_raw).hexdigest(),
        "proc_cgroup_line": rows[0],
        "service_cgroup_bound": True,
    }


def validate_gate_phase_fields(
    fields: Mapping[str, str], execstart: Mapping[str, Any],
    execstartpre: Mapping[str, Any], process_pid: int,
) -> dict[str, Any]:
    need(type(process_pid) is int and process_pid > 1, "real gate process pid")
    need(fields.get("ActiveState") == "activating",
         "gate ActiveState=activating")
    need(fields.get("SubState") == "start-pre", "gate SubState=start-pre")
    need(fields.get("Result") == "success", "gate Result=success")
    need(fields.get("ExecMainCode") == "0", "gate prestart ExecMainCode=0")
    need(fields.get("ExecMainStatus") == "0", "gate prestart ExecMainStatus=0")
    need(fields.get("MainPID") == "0", "gate has no premature MainPID")
    control_pid = int(exact_string(fields.get("ControlPID"), "ControlPID"))
    need(control_pid == process_pid,
         "ControlPID == ExecStartPre.pid == os.getpid gate binding")
    validate_future_exec_projection(execstart, "future ExecStart")
    validate_live_exec_projection(execstartpre, process_pid, "live ExecStartPre")
    return {
        "phase": "start-pre", "ActiveState": fields["ActiveState"],
        "SubState": fields["SubState"], "MainPID": 0,
        "ControlPID": control_pid, "future_ExecStart_pid": 0,
        "gate_process_binding": True,
    }


def validate_bridge_service(
    runtime: RuntimeAuthority, expected: Mapping[str, Any],
    fragment_held: HeldFile, process_pid: int,
    allow_execstart_projection_decay: bool = False,
) -> dict[str, Any]:
    unit = exact_string(expected.get("Id"), "bridge-running:Id")
    fields, raw = runtime.query(unit, BRIDGE_SERVICE_PROPERTIES)
    for key in BRIDGE_STABLE_PROPERTIES:
        need(type(expected.get(key)) is str and fields[key] == expected[key],
             "bridge stable service field:" + key)
    expected_start = expected.get("ExecStart")
    expected_pre = expected.get("ExecStartPre")
    need(type(expected_start) is list and type(expected_pre) is list,
         "bridge stable exec argv lists")
    execstart = parse_exec_command(
        fields["ExecStart"], expected_start, FINAL_PYTHON, True, "ExecStart",
        allow_started_projection_decay=allow_execstart_projection_decay,
    )
    execstartpre = parse_exec_command(
        fields["ExecStartPre"], expected_pre, FINAL_PYTHON, True, "ExecStartPre",
        allow_started_projection_decay=allow_execstart_projection_decay,
    )
    if allow_execstart_projection_decay and execstartpre["pid"] == 0:
        need(execstartpre["start_time"] == "n/a"
             and execstartpre["stop_time"] == "n/a"
             and execstartpre["code"] == "(null)"
             and execstartpre["status"] in {"0", "0/0"},
             "exact manager-reload-decayed ExecStartPre projection")
        pre_projection = "manager-reload-decayed-zero"
    else:
        validate_completed_exec_projection(execstartpre, "completed ExecStartPre")
        pre_projection = "completed-gate-pid-retained"
    live = validate_running_live_fields(
        fields, execstart, process_pid, allow_execstart_projection_decay,
    )
    proc_binding = validate_outer_proc_binding(process_pid, unit)
    need(fields["FragmentPath"] == os.fspath(fragment_held.path),
         "bridge service fragment exact path")
    fragment_held.verify()
    need(expected.get("FragmentSHA256") == fragment_held.sha256
         and expected.get("FragmentStat9") == stat9(fragment_held.initial),
         "bridge service fragment SHA/full9stat")
    return closed({
        "schema": "cm2.round306c30c.bridge-v5-running-service-attestation.v1",
        "status": "PASS_PRESTART_STABLE_AND_RUNNING_LIVE_PID_BOUND",
        "label": "bridge-running", "properties": fields,
        "execstart": execstart, "execstartpre": execstartpre,
        "execstartpre_projection": pre_projection,
        "running_live_invariants": live,
        "outer_proc_binding": proc_binding,
        "continuous_revalidation": allow_execstart_projection_decay,
        "systemctl_stdout_sha256": hashlib.sha256(raw).hexdigest(),
        "fragment_sha256": fragment_held.sha256,
        "fragment_stat9": stat9(fragment_held.initial),
        "runtime_authority_object_sha256": runtime.baseline["object_sha256"],
        "formal_credit": 0, "source_W_formal_remainder": 80,
        "source_W_transition_authorized": False,
        "publication_authorized": False, "terminal_replay_completed": False,
    })


def wait_bridge_running_service(
    runtime: RuntimeAuthority, expected: Mapping[str, Any],
    fragment_held: HeldFile, process_pid: int,
) -> dict[str, Any]:
    deadline = time.monotonic() + 15.0
    last_error: Reject | None = None
    while True:
        try:
            return validate_bridge_service(
                runtime, expected, fragment_held, process_pid,
            )
        except Reject as error:
            last_error = error
        if time.monotonic() >= deadline:
            raise Reject("bridge running-state settlement timeout:" + str(last_error))
        time.sleep(0.05)


def capture_gate_prestart_service(
    runtime: RuntimeAuthority, bridge: Path, pinset: Path, anchor: Path,
    unit: str, maximum_wait: int, watcher_sha256: str, gate_sha256: str,
    fragment_held: HeldFile | None = None,
) -> tuple[dict[str, Any], dict[str, Any], HeldFile]:
    expected_start = expected_watcher_argv(
        bridge, pinset, anchor, unit, maximum_wait, watcher_sha256,
    )
    expected_pre = expected_gate_argv(
        bridge, pinset, anchor, unit, maximum_wait, gate_sha256,
        watcher_sha256,
    )
    fields, raw = runtime.query(unit, BRIDGE_SERVICE_PROPERTIES)
    need(fields["Id"] == unit, "gate exact service Id")
    need(fields["LoadState"] == "loaded", "gate service loaded")
    need(fields["Type"] == "exec", "gate requires Type=exec")
    need(fields["RemainAfterExit"] == "yes", "gate requires RemainAfterExit=yes")
    invocation = fields["InvocationID"]
    validate_invocation_binding(invocation, os.environ.get("INVOCATION_ID"), "gate")
    expected_fragment = RUNTIME_DIR / "systemd/transient" / unit
    need(fields["FragmentPath"] == os.fspath(expected_fragment),
         "gate exact transient FragmentPath")
    created = fragment_held is None
    fragment = (HeldFile(expected_fragment, "gate bridge fragment", 1 << 20)
                if fragment_held is None else fragment_held)
    try:
        need(fragment.path == expected_fragment, "held gate fragment path")
        fragment.verify()
        execstart = parse_exec_command(
            fields["ExecStart"], expected_start, FINAL_PYTHON, False,
            "future ExecStart",
        )
        execstartpre = parse_exec_command(
            fields["ExecStartPre"], expected_pre, FINAL_PYTHON, True,
            "live ExecStartPre",
        )
        phase = validate_gate_phase_fields(
            fields, execstart, execstartpre, os.getpid(),
        )
        stable = {
            "Id": fields["Id"], "InvocationID": invocation,
            "ExecStart": expected_start, "ExecStartPre": expected_pre,
            "FragmentPath": fields["FragmentPath"],
            "FragmentSHA256": fragment.sha256,
            "FragmentStat9": stat9(fragment.initial),
            "LoadState": fields["LoadState"], "Type": fields["Type"],
            "RemainAfterExit": fields["RemainAfterExit"],
            "StandardOutput": fields["StandardOutput"],
            "StandardError": fields["StandardError"],
        }
        attestation = {
            "stable": stable, "phase": phase,
            "systemctl_stdout_sha256": hashlib.sha256(raw).hexdigest(),
        }
        return stable, attestation, fragment
    except BaseException:
        if created:
            fragment.close()
        raise


def capture_transaction_service(
    runtime: RuntimeAuthority, fragment_held: HeldFile | None = None,
) -> tuple[dict[str, Any], HeldFile]:
    fields, _raw = runtime.query(
        TRANSACTION_UNIT, TRANSACTION_SERVICE_PROPERTIES,
    )
    expected_exact = {
        "Id": TRANSACTION_UNIT, "InvocationID": TRANSACTION_INVOCATION,
        "FragmentPath": os.fspath(TRANSACTION_FRAGMENT),
        "LoadState": "loaded", "ActiveState": "active", "SubState": "exited",
        "Result": "success", "ExecMainCode": "1", "ExecMainStatus": "0",
        "MainPID": "0", "Type": "oneshot", "RemainAfterExit": "yes",
        "StandardOutput": "journal", "StandardError": "journal",
    }
    for key, value in expected_exact.items():
        need(fields[key] == value, "gate transaction exact authority:" + key)
    parsed = parse_exec_command(
        fields["ExecStart"], [os.fspath(TRANSACTION_LAUNCHER)],
        TRANSACTION_LAUNCHER, True, "transaction ExecStart",
        allow_started_projection_decay=True,
    )
    if parsed["pid"] == 0:
        validate_future_exec_projection(
            parsed, "manager-reload-decayed completed transaction ExecStart",
        )
    else:
        validate_completed_exec_projection(parsed, "transaction ExecStart")
    created = fragment_held is None
    fragment = (HeldFile(TRANSACTION_FRAGMENT, "gate transaction fragment", 1 << 20)
                if fragment_held is None else fragment_held)
    try:
        fragment.verify()
        result: dict[str, Any] = dict(fields)
        result["FragmentSHA256"] = fragment.sha256
        result["FragmentStat9"] = stat9(fragment.initial)
        return result, fragment
    except BaseException:
        if created:
            fragment.close()
        raise


def gate_material_paths(
    bridge_path: Path, pinset_path: Path, anchor_path: Path, unit: str,
    maximum_wait: int,
) -> tuple[Path, Path, Path]:
    bridge = Path(os.path.abspath(os.fspath(bridge_path)))
    pinset = Path(os.path.abspath(os.fspath(pinset_path)))
    anchor = Path(os.path.abspath(os.fspath(anchor_path)))
    need(pinset.parent == anchor.parent
         and pinset.parent.parent == CONTROL
         and pinset.parent.name.startswith("c30c-postreceipt-v3-p1-bridge-v5-")
         and bridge.parent == AUDIT and bridge.name == pinset.parent.name,
         "matched fresh v5 control/audit namespaces")
    need(pinset.name == "pinset.json" and anchor.name == "launch-anchor.json",
         "exact v5 material names")
    finalizer_unit_for_worker(bridge, unit)
    need(type(maximum_wait) is int and 0 <= maximum_wait <= 7 * 24 * 3600,
         "bounded gate maximum wait")
    return bridge, pinset, anchor


def finalizer_unit_for_worker(bridge: Path, worker_unit: str) -> str:
    prefix = "c30c-postreceipt-v3-p1-bridge-v5-"
    need(bridge.parent == AUDIT and bridge.name.startswith(prefix),
         "v5 worker/finalizer audit namespace")
    token = bridge.name[len(prefix):]
    need(re.fullmatch(r"[A-Za-z0-9_.:-]+", token) is not None,
         "v5 worker/finalizer token")
    need(worker_unit == "cm2-" + prefix + token + ".service",
         "worker exact same-token unit")
    return "cm2-" + prefix + "finalizer-" + token + ".service"


def publish_gate_materials(
    bridge_path: Path, pinset_path: Path, anchor_path: Path,
    unit: str, maximum_wait: int, executed_gate: Mapping[str, Any],
    executed_watcher: Mapping[str, Any],
) -> dict[str, Any]:
    need(type(executed_gate) is dict
         and set(executed_gate) == {"path", "sha256", "stat9"}
         and executed_gate.get("path") == os.fspath(START_GATE)
         and type(executed_gate.get("sha256")) is str
         and HEX64.fullmatch(executed_gate["sha256"]) is not None
         and type(executed_gate.get("stat9")) is dict,
         "exact held-bootstrap executed gate binding")
    need(type(executed_watcher) is dict
         and set(executed_watcher) == {"path", "sha256", "stat9"}
         and executed_watcher.get("path") == os.fspath(WATCHER)
         and type(executed_watcher.get("sha256")) is str
         and HEX64.fullmatch(executed_watcher["sha256"]) is not None
         and type(executed_watcher.get("stat9")) is dict,
         "exact precompile-approved held watcher binding")
    bridge_path, pinset_path, anchor_path = gate_material_paths(
        bridge_path, pinset_path, anchor_path, unit, maximum_wait,
    )
    bridge = HeldDir(bridge_path, "gate fresh bridge root", fresh=True)
    control = HeldDir(pinset_path.parent, "gate fresh control root", fresh=True)
    runtime = RuntimeAuthority()
    bridge_fragment: HeldFile | None = None
    transaction_fragment: HeldFile | None = None
    pinset_file: HeldFile | None = None
    anchor_file: HeldFile | None = None
    self_file: HeldFile | None = None
    gate_file: HeldFile | None = None
    wrapper_file: HeldFile | None = None
    try:
        self_file = HeldFile(WATCHER, "gate held watcher bootstrap source", 8 << 20)
        gate_file = HeldFile(START_GATE, "gate held executed source", 8 << 20)
        wrapper_file = HeldFile(WRAPPER, "gate held process wrapper", 8 << 20)
        need(self_file.path == Path(executed_watcher["path"])
             and self_file.sha256 == executed_watcher["sha256"]
             and stat9(self_file.initial) == executed_watcher["stat9"],
             "precompile-approved watcher == held gate implementation")
        need(gate_file.path == Path(executed_gate["path"])
             and gate_file.sha256 == executed_gate["sha256"]
             and stat9(gate_file.initial) == executed_gate["stat9"],
             "held-bootstrap execution binding before authority capture")
        stable, gate_attestation, bridge_fragment = capture_gate_prestart_service(
            runtime, bridge_path, pinset_path, anchor_path, unit, maximum_wait,
            self_file.sha256, gate_file.sha256,
        )
        transaction, transaction_fragment = capture_transaction_service(runtime)
        roles = required_pin_roles(bridge_fragment.path)
        observations = {
            role: make_pin_observation(role, path)
            for role, path in sorted(roles.items())
        }
        need(set(observations) == set(roles), "gate exact pin role construction")
        executed_row = observations["bridge_start_gate"]
        need(executed_row["path"] == executed_gate["path"]
             and executed_row["sha256"] == executed_gate["sha256"]
             and executed_row["stat9"] == executed_gate["stat9"],
             "executed gate bytes/full9stat == pinset gate role")
        watcher_row = observations["bridge_watcher"]
        need(watcher_row["path"] == executed_watcher["path"]
             and watcher_row["sha256"] == executed_watcher["sha256"]
             and watcher_row["stat9"] == executed_watcher["stat9"],
             "precompile-approved watcher bytes/full9stat == pinset watcher role")
        analyzer_row = observations["cold_analyzer"]
        need(analyzer_row["kind"] == "regular"
             and analyzer_row["path"] == os.fspath(ANALYZER)
             and analyzer_row["sha256"] == ANALYZER_SHA256
             and analyzer_row["stat9"]["size"] == ANALYZER_SIZE,
             "watcher-source-pinned exact cold analyzer bytes/size")
        for critical in (
            "bridge_watcher", "bridge_start_gate",
            "bridge_composite_finalizer", "bridge_worker_launcher",
            "bridge_finalizer_launcher", "process_wrapper", "cold_analyzer",
        ):
            need(observations[critical]["kind"] == "regular"
                 and stat.S_IMODE(observations[critical]["stat9"]["mode"]) == 0o444,
                 "frozen read-only launch code:" + critical)
        pinset = closed({
            "schema": PINSET_SCHEMA,
            "status": "FROZEN_EXACT_ROLE_SET_BRIDGE_V5_ZERO_CREDIT",
            "members": [observations[role] for role in sorted(observations)],
            "formal_credit": 0, "source_W_formal_remainder": 80,
            "source_W_transition_authorized": False,
            "publication_authorized": False, "terminal_replay_completed": False,
        })
        pinset_raw = canonical(pinset) + b"\n"
        atomic_publish_bytes(pinset_path, pinset_raw, "pinset-first")
        need("launch-anchor.json" not in control.names(),
             "anchor absent after durable pinset publication")
        pinset_file = HeldFile(pinset_path, "gate published pinset", 16 << 20)
        for row in pinset["members"]:
            need(observe_pin(row) == row, "gate post-pinset role replay")
        stable_replay, _gate_replay, replay_fragment = capture_gate_prestart_service(
            runtime, bridge_path, pinset_path, anchor_path, unit, maximum_wait,
            self_file.sha256, gate_file.sha256,
            bridge_fragment,
        )
        need(replay_fragment is bridge_fragment and stable_replay == stable,
             "gate stable authority across pinset publication")
        transaction_replay, replay_transaction_fragment = capture_transaction_service(
            runtime, transaction_fragment,
        )
        need(replay_transaction_fragment is transaction_fragment
             and transaction_replay == transaction,
             "gate transaction authority across pinset publication")
        need(bridge.names() == [], "bridge root remains fresh before anchor release")

        for role, held in (
            ("bridge_watcher", self_file), ("bridge_start_gate", gate_file),
            ("process_wrapper", wrapper_file),
        ):
            row = observations[role]
            need(row["path"] == os.fspath(held.path)
                 and row["sha256"] == held.sha256
                 and row["stat9"] == stat9(held.initial),
                 "pinset/held critical launch code closure:" + role)
        need(gate_file.path == Path(executed_gate["path"])
             and gate_file.sha256 == executed_gate["sha256"]
             and stat9(gate_file.initial) == executed_gate["stat9"],
             "executed gate bytes/full9stat == anchor held gate")
        need(self_file.path == Path(executed_watcher["path"])
             and self_file.sha256 == executed_watcher["sha256"]
             and stat9(self_file.initial) == executed_watcher["stat9"],
             "precompile-approved watcher bytes/full9stat == anchor held watcher")
        anchor = closed({
            "schema": ANCHOR_SCHEMA,
            "status": "FROZEN_BRIDGE_V5_PRESTART_GATE_ZERO_CREDIT",
            "watcher_path": os.fspath(WATCHER),
            "watcher_sha256": self_file.sha256,
            "watcher_stat9": stat9(self_file.initial),
            "gate_path": os.fspath(START_GATE),
            "gate_sha256": gate_file.sha256,
            "gate_stat9": stat9(gate_file.initial),
            "wrapper_path": os.fspath(WRAPPER),
            "wrapper_sha256": wrapper_file.sha256,
            "wrapper_stat9": stat9(wrapper_file.initial),
            "pinset_path": os.fspath(pinset_path),
            "pinset_sha256": pinset_file.sha256,
            "pinset_stat9": stat9(pinset_file.initial),
            "bridge_dir": os.fspath(bridge_path),
            "bridge_service": stable,
            "transaction_service": transaction,
            "formal_credit": 0, "source_W_formal_remainder": 80,
            "source_W_transition_authorized": False,
            "publication_authorized": False, "terminal_replay_completed": False,
        })
        anchor_raw = canonical(anchor) + b"\n"
        for row in pinset["members"]:
            need(observe_pin(row) == row, "gate final pre-anchor role replay")
        gate_file.verify()
        self_file.verify()
        need(gate_file.sha256 == executed_gate["sha256"]
             and stat9(gate_file.initial) == executed_gate["stat9"],
             "held-bootstrap gate stable immediately before anchor")
        need(self_file.sha256 == executed_watcher["sha256"]
             and stat9(self_file.initial) == executed_watcher["stat9"],
             "precompile-approved watcher stable immediately before anchor")
        stable_before_anchor, _gate_before_anchor, before_anchor_fragment = (
            capture_gate_prestart_service(
                runtime, bridge_path, pinset_path, anchor_path, unit,
                maximum_wait, self_file.sha256, gate_file.sha256,
                bridge_fragment,
            )
        )
        transaction_before_anchor, before_anchor_transaction_fragment = (
            capture_transaction_service(runtime, transaction_fragment)
        )
        need(before_anchor_fragment is bridge_fragment
             and stable_before_anchor == stable
             and before_anchor_transaction_fragment is transaction_fragment
             and transaction_before_anchor == transaction,
             "all service authority stable immediately before anchor")
        need(control.names() == ["pinset.json"] and bridge.names() == [],
             "exact pre-anchor release inventories")
        atomic_publish_bytes(anchor_path, anchor_raw, "anchor-last")

        # The anchor is the sole material release marker.  Everything after its
        # durable no-replace rename is read-only replay; systemd additionally
        # requires this ExecStartPre process to exit zero before ExecStart.
        anchor_file = HeldFile(anchor_path, "gate published anchor", 8 << 20)
        need(parse_anchor(anchor_file) == anchor, "gate anchor exact byte replay")
        parsed_pinset, replayed = load_pinset(
            pinset_file, pinset_file.sha256, anchor,
        )
        need(parsed_pinset == pinset and replayed == observations,
             "gate pinset exact byte/role replay")
        validate_anchor_bindings(
            anchor, anchor_file, pinset_file, self_file, gate_file,
            wrapper_file, bridge,
        )
        stable_final, _gate_final, final_fragment = capture_gate_prestart_service(
            runtime, bridge_path, pinset_path, anchor_path, unit, maximum_wait,
            self_file.sha256, gate_file.sha256,
            bridge_fragment,
        )
        need(final_fragment is bridge_fragment and stable_final == stable,
             "gate authority stable after anchor release")
        gate_file.verify()
        self_file.verify()
        need(gate_file.sha256 == executed_gate["sha256"]
             and stat9(gate_file.initial) == executed_gate["stat9"],
             "held-bootstrap gate stable after anchor replay")
        need(self_file.sha256 == executed_watcher["sha256"]
             and stat9(self_file.initial) == executed_watcher["stat9"],
             "precompile-approved watcher stable after anchor replay")
        return closed({
            "schema": "cm2.round306c30c.postreceipt-bridge-v5-start-gate-receipt.v1",
            "status": "PASS_PINSET_THEN_ANCHOR_LAST_BYTE_REPLAYED_ZERO_CREDIT",
            "unit": unit, "InvocationID": stable["InvocationID"],
            "FragmentPath": stable["FragmentPath"],
            "pinset_sha256": pinset_file.sha256,
            "anchor_sha256": anchor_file.sha256,
            "pinned_role_count": len(observations),
            "prestart_phase_attestation": gate_attestation,
            "formal_credit": 0, "source_W_formal_remainder": 80,
            "source_W_transition_authorized": False,
            "publication_authorized": False, "terminal_replay_completed": False,
            "CM2": "NO-GO_FOR_CLAIM",
        })
    finally:
        for held in (anchor_file, pinset_file, wrapper_file, gate_file, self_file,
                     transaction_fragment, bridge_fragment):
            if held is not None:
                try: held.close()
                except OSError: pass
        runtime.close(); control.close(); bridge.close()


def verify_launch_materials(
    anchor_file: HeldFile, pinset_file: HeldFile, self_file: HeldFile,
    gate_file: HeldFile, wrapper_file: HeldFile, bridge_fragment: HeldFile,
    transaction_fragment: HeldFile, runtime: RuntimeAuthority,
    anchor: Mapping[str, Any], bridge: HeldDir,
) -> dict[str, dict[str, Any]]:
    for held in (anchor_file, pinset_file, self_file, gate_file, wrapper_file,
                 bridge_fragment, transaction_fragment):
        held.verify()
    runtime.verify(); bridge.verify()
    parsed = parse_anchor(anchor_file)
    need(parsed == dict(anchor), "anchor stable parsed object")
    _pinset, observations = load_pinset(pinset_file, anchor["pinset_sha256"], anchor)
    validate_anchor_bindings(
        anchor, anchor_file, pinset_file, self_file, gate_file, wrapper_file, bridge,
    )
    return observations


def exact_directory_files(path: Path, expected: set[str], label: str) -> HeldDir:
    directory = HeldDir(path, label)
    try:
        need(set(directory.names()) == expected, "exact inventory:" + label)
        for name in sorted(expected):
            state = directory.lstat(name)
            need(stat.S_ISREG(state.st_mode) and state.st_nlink == 1,
                 "all members regular singleton:" + label + ":" + name)
        return directory
    except BaseException:
        directory.close(); raise


def strict_pin_file(raw: bytes) -> list[tuple[str, str]]:
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as error:
        raise Reject("transaction pins ASCII") from error
    need(text.endswith("\n"), "transaction pins final newline")
    rows: list[tuple[str, str]] = []
    for line in text.splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  (/[^\n]+)", line)
        need(match is not None, "strict transaction pin row")
        digest, path = match.groups()
        need(path not in {item[1] for item in rows}, "unique transaction pin path")
        rows.append((digest, path))
    need(len(rows) == 13, "exact 13 transaction pins")
    return rows


def parse_utc_line(raw: bytes, label: str) -> datetime:
    need(UTC_LINE.fullmatch(raw) is not None, "strict UTC bytes:" + label)
    try:
        value = datetime.strptime(raw.decode("ascii").strip(), "%Y-%m-%dT%H:%M:%SZ")
    except (UnicodeDecodeError, ValueError) as error:
        raise Reject("strict UTC value:" + label) from error
    return value.replace(tzinfo=timezone.utc)


def followed_file_sha256(path: Path, maximum: int = 8 << 30) -> str:
    absolute = Path(os.path.abspath(os.fspath(path)))
    link_before = absolute.lstat()
    need((stat.S_ISREG(link_before.st_mode) and link_before.st_nlink == 1)
         or (stat.S_ISLNK(link_before.st_mode) and link_before.st_nlink == 1),
         "transaction pin regular/symlink singleton")
    fd = os.open(absolute, os.O_RDONLY | os.O_CLOEXEC)
    try:
        opened = os.fstat(fd); raw = read_all(fd, maximum); after = os.fstat(fd)
    finally:
        os.close(fd)
    link_after = absolute.lstat()
    need(identity(link_before) == identity(link_after)
         and identity(opened) == identity(after), "transaction pin stable follow")
    return hashlib.sha256(raw).hexdigest()


def validate_pin_log(raw: bytes, pins: Sequence[tuple[str, str]], label: str) -> None:
    expected = b"".join(
        path.encode("ascii") + ": 成功\n".encode("utf-8") for _digest, path in pins
    )
    need(raw == expected, "strict sha256sum pin log byte replay:" + label)


def strict_build(value: Mapping[str, Any]) -> None:
    required = {
        "command_sha256", "control_directory", "downstream_publication_authorized",
        "formal_credit", "launcher_sha256", "pin_member_count", "pinset_sha256",
        "provenance_sha256", "receipt_directory", "run_directory", "run_name",
        "runner_sha256", "schema", "source_W_formal_remainder", "status",
        "validator_sha256",
    }
    need(set(value) == required
         and value.get("schema") == "cm2.c30c.receipted-transaction-v3-build.v1"
         and value.get("status") == "PASS_FRESH_FAIL_CLOSED_TRANSACTION_BUILT_NOT_YET_RUN",
         "strict transaction build schema/status")
    need(exact_int(value.get("formal_credit"), "build credit") == 0
         and exact_int(value.get("source_W_formal_remainder"), "build remainder") == 80
         and exact_int(value.get("pin_member_count"), "build pins") == 13
         and exact_bool(value.get("downstream_publication_authorized"), "build publication") is False,
         "strict transaction build zero-credit fields")
    for name in ("command_sha256", "launcher_sha256", "pinset_sha256",
                 "provenance_sha256", "runner_sha256", "validator_sha256"):
        need(type(value.get(name)) is str and HEX64.fullmatch(value[name]) is not None,
             "build SHA field:" + name)


def strict_preflight(value: Mapping[str, Any]) -> None:
    required = {
        "attack_contract_count", "candidate_exact_six", "candidate_gzip_row_counts",
        "downstream_publication_authorized", "formal_credit", "pinned_input_count",
        "run_name", "schema", "source_W_formal_remainder", "status",
        "validator_sha256",
    }
    need(set(value) == required and value.get("schema") == "cm2.c30c.receipt-v3-preflight.v1"
         and value.get("status") == "PASS_FAIL_CLOSED_STATIC_AND_FIXTURE_PREFLIGHT",
         "strict transaction preflight schema/status")
    need(exact_int(value.get("attack_contract_count"), "preflight attacks") == 62
         and exact_int(value.get("pinned_input_count"), "preflight pins") == 10
         and exact_bool(value.get("candidate_exact_six"), "preflight candidate") is True
         and exact_int(value.get("formal_credit"), "preflight credit") == 0
         and exact_int(value.get("source_W_formal_remainder"), "preflight remainder") == 80
         and exact_bool(value.get("downstream_publication_authorized"), "preflight publication") is False,
         "strict preflight typed conclusion")
    counts = value.get("candidate_gzip_row_counts")
    need(type(counts) is dict and set(counts) == {
        PREFIX + "_combined_boundary_atomic_owner_join_ledger.jsonl.gz",
        PREFIX + "_delta_h_cell_ledger.jsonl.gz",
        PREFIX + "_inherited_h_cell_ledger.jsonl.gz",
        PREFIX + "_whole_origin_ledger.jsonl.gz",
    } and all(type(item) is int for item in counts.values()),
         "strict preflight gzip row counts")


def strict_transaction_receipt(value: Mapping[str, Any]) -> None:
    required = {
        "schema", "status", "run_directory", "run_start_utc", "run_end_utc",
        "elapsed", "harness_stdout_sha256", "harness_sha256", "verifier_sha256",
        "validator_sha256", "python_sha256", "baseline_result_sha256",
        "attack_count", "pre_post_sha256_identical", "pre_post_stat_identical",
        "numeric_exit_code", "signal", "formal_credit", "manifest_authorized",
        "source_W_formal_remainder", "source_W_transition_authorized",
        "downstream_publication_authorized", "authority",
    }
    need(set(value) == required
         and value.get("schema") == "cm2.round306c30c.attack-run-receipt-validation.v3"
         and value.get("status") == EXPECTED_RECEIPT_STATUS
         and value.get("run_directory") == TRANSACTION_NAME,
         "strict transaction receipt schema/status")
    need(exact_int(value.get("attack_count"), "receipt attacks") == 62
         and exact_int(value.get("numeric_exit_code"), "receipt exit") == 0
         and value.get("signal") is None
         and exact_bool(value.get("pre_post_sha256_identical"), "receipt SHA closure") is True
         and exact_bool(value.get("pre_post_stat_identical"), "receipt stat closure") is True
         and exact_int(value.get("formal_credit"), "receipt credit") == 0
         and exact_bool(value.get("manifest_authorized"), "receipt manifest") is False
         and exact_int(value.get("source_W_formal_remainder"), "receipt remainder") == 80
         and exact_bool(value.get("source_W_transition_authorized"), "receipt transition") is False
         and exact_bool(value.get("downstream_publication_authorized"), "receipt publication") is False,
         "strict transaction receipt typed conclusion")
    for name in ("harness_stdout_sha256", "harness_sha256", "verifier_sha256",
                 "validator_sha256", "python_sha256", "baseline_result_sha256"):
        need(type(value.get(name)) is str and HEX64.fullmatch(value[name]) is not None,
             "receipt SHA field:" + name)


def validate_transaction_boundary() -> tuple[dict[str, Any], bytes, bytes]:
    run = exact_directory_files(RUN, set(RUN_FILES), "transaction run")
    receipt = exact_directory_files(RECEIPT, set(RECEIPT_FILES), "transaction receipt")
    pins_held = HeldFile(TRANSACTION_PINS, "transaction pins", 4 << 20)
    try:
        pins = strict_pin_file(pins_held.raw)
        for name in ("preflight.exit", "receipt.exit", "transaction-run.exit"):
            need(receipt.open_regular(name, 32)[0] == b"0\n", "zero exit byte:" + name)
        for name in ("preflight.stderr", "receipt.stderr"):
            need(receipt.open_regular(name, 64 << 20)[0] == b"", "empty stderr:" + name)
        need(run.open_regular("stderr.log", 64 << 20)[0] == b"", "harness stderr empty")
        need(run.open_regular("exit_code.txt", 32)[0] == b"0\n", "harness exit zero")
        need(run.open_regular("pre.sha256", 4 << 20)[0]
             == run.open_regular("post.sha256", 4 << 20)[0], "pre/post SHA bytes")
        need(run.open_regular("pre.stat", 4 << 20)[0]
             == run.open_regular("post.stat", 4 << 20)[0], "pre/post stat bytes")
        for name in ("start_utc.txt", "end_utc.txt"):
            need(UTC_LINE.fullmatch(run.open_regular(name, 64)[0]) is not None,
                 "strict run UTC:" + name)
        run_end_raw = run.open_regular("end_utc.txt", 64)[0]
        end_raw = receipt.open_regular("transaction-end-utc.txt", 64)[0]
        run_end = parse_utc_line(run_end_raw, "run end")
        transaction_end = parse_utc_line(end_raw, "transaction end")
        need(0 <= (transaction_end - run_end).total_seconds() <= 300,
             "transaction receipt end strictly follows run end within 300s")
        validate_pin_log(receipt.open_regular("preflight-pin-check.log", 4 << 20)[0],
                         pins, "preflight")
        validate_pin_log(receipt.open_regular("postrun-pin-check.log", 4 << 20)[0],
                         pins, "postrun")
        build_raw = receipt.open_regular("build.json", 4 << 20)[0]
        preflight_raw = receipt.open_regular("preflight.json", 4 << 20)[0]
        final_raw = receipt.open_regular("receipt.json", 16 << 20)[0]
        build = strict_json(build_raw, "transaction build")
        preflight = strict_json(preflight_raw, "transaction preflight")
        strict_build(build); strict_preflight(preflight)
        final = strict_json(final_raw, "transaction receipt")
        strict_transaction_receipt(final)
        for digest, path_text in pins:
            need(followed_file_sha256(Path(path_text)) == digest,
                 "transaction pin current SHA:" + path_text)
        need(build["command_sha256"] == hashlib.sha256(
                 run.open_regular("command.txt", 4 << 20)[0]).hexdigest()
             and build["provenance_sha256"] == hashlib.sha256(
                 run.open_regular("provenance.json", 4 << 20)[0]).hexdigest()
             and build["runner_sha256"] == hashlib.sha256(
                 run.open_regular("run.sh", 4 << 20)[0]).hexdigest()
             and build["launcher_sha256"] == followed_file_sha256(TRANSACTION_LAUNCHER)
             and build["pinset_sha256"] == pins_held.sha256
             and build["validator_sha256"] == followed_file_sha256(VALIDATOR),
             "transaction build hash/path closure")
        need(preflight["validator_sha256"] == followed_file_sha256(VALIDATOR)
             and final["validator_sha256"] == followed_file_sha256(VALIDATOR)
             and final["harness_sha256"] == followed_file_sha256(HARNESS)
             and final["verifier_sha256"] == followed_file_sha256(VERIFIER)
             and final["python_sha256"] == followed_file_sha256(VENV_PYTHON)
             and final["harness_stdout_sha256"] == hashlib.sha256(
                 run.open_regular("stdout.json", 64 << 20)[0]).hexdigest(),
             "preflight/final receipt hash closure")
        need((final["run_start_utc"] + "\n").encode("ascii")
             == run.open_regular("start_utc.txt", 64)[0]
             and (final["run_end_utc"] + "\n").encode("ascii")
             == run.open_regular("end_utc.txt", 64)[0],
             "receipt start/end byte closure")
        pins_held.verify()
        need(set(run.names()) == set(RUN_FILES)
             and set(receipt.names()) == set(RECEIPT_FILES), "transaction final inventories")
        return final, final_raw, preflight_raw
    finally:
        pins_held.close(); run.close(); receipt.close()


def stage_request(
    stage: str, argv: Sequence[str], environment: Mapping[str, str],
    expected_exe_real: Path, trace: bool,
) -> dict[str, Any]:
    need(all(type(item) is str and item for item in argv), "stage argv strings")
    return closed({
        "schema": REQUEST_SCHEMA, "stage": stage, "inner_argv": list(argv),
        "inner_env": dict(environment),
        "expected_exe_real": os.fspath(expected_exe_real.resolve(strict=True)),
        "trace_requested": trace, "formal_credit": 0,
        "source_W_formal_remainder": 80,
        "source_W_transition_authorized": False,
        "publication_authorized": False, "terminal_replay_completed": False,
    })


def validate_wrapper_receipt(value: Mapping[str, Any], request_sha: str) -> dict[str, Any]:
    verify_closure(value, "process wrapper receipt")
    required = {
        "schema", "status", "execution_mode", "wrapper_pid", "gnu_time_pid", "trampoline_pid",
        "true_inner_pid", "three_level_pid_distinct", "time_argv",
        "expected_time_command", "time_returncode", "gnu_time", "attestation",
        "captures", "request_path", "request_sha256", "request_stat9",
        "wrapper_sha256", "wrapper_stat9", "gnu_time_sha256", "gnu_time_stat9",
        "python_sha256", "python_stat9", "started_ns", "ended_ns",
        "formal_credit", "source_W_formal_remainder",
        "source_W_transition_authorized", "publication_authorized",
        "terminal_replay_completed", "object_sha256",
    }
    need(set(value) == required and value.get("schema") == WRAPPER_RECEIPT_SCHEMA
         and value.get("status") == "PASS_WRAPPER_CAPTURED_TRUE_INNER_PID_ZERO_CREDIT",
         "wrapper exact schema/status/fields")
    zero_contract(value, "wrapper receipt")
    mode = value.get("execution_mode")
    need(mode in {"TRAMPOLINE_TRUE_INNER", "GNU_TIME_DIRECT_TRACE_CHILD"},
         "wrapper exact execution mode")
    base_pids = [value.get(name) for name in (
        "wrapper_pid", "gnu_time_pid", "true_inner_pid",
    )]
    need(all(type(pid) is int and pid > 1 for pid in base_pids)
         and len(set(base_pids)) == 3
         and exact_bool(value.get("three_level_pid_distinct"), "pid distinct") is True,
         "three distinct wrapper/time/inner PIDs")
    if mode == "TRAMPOLINE_TRUE_INNER":
        need(type(value.get("trampoline_pid")) is int
             and value["trampoline_pid"] > 1
             and value["trampoline_pid"] not in set(base_pids),
             "distinct trampoline PID")
    else:
        need(value.get("trampoline_pid") is None, "direct trace has no trampoline")
    need(value.get("request_sha256") == request_sha, "wrapper request SHA")
    need(type(value.get("time_returncode")) is int, "wrapper time return type")
    attestation = value.get("attestation")
    need(type(attestation) is dict, "nested inner attestation")
    verify_closure(attestation, "inner attestation")
    required_attest = {
        "schema", "status", "trampoline_pid", "time_parent_pid", "true_inner_pid",
        "resolved_inner_argv", "inner_env", "proc_cmdline_sha256",
        "proc_environ_sha256", "proc_exe_link", "proc_exe_stat9",
        "wait_returncode", "numeric_exit_code", "signal", "ended_ns",
        "formal_credit", "source_W_formal_remainder",
        "source_W_transition_authorized", "publication_authorized",
        "terminal_replay_completed", "object_sha256",
    }
    need(set(attestation) == required_attest
         and attestation.get("schema") == "cm2.round306c30c.bridge-v3-inner-process-attestation.v1"
         and attestation.get("status") in {
             "PASS_TRUE_INNER_PID_CAPTURED_AND_WAITED",
             "PASS_TRUE_GNU_TIME_CHILD_PID_CAPTURED_AND_WAITED",
         },
         "inner attestation exact schema/status/fields")
    zero_contract(attestation, "inner attestation")
    need(type(attestation.get("wait_returncode")) is int
         and type(attestation.get("numeric_exit_code")) is int
         and attestation["numeric_exit_code"] == 0
         and attestation["wait_returncode"] == 0
         and attestation.get("signal") is None,
         "true inner exact clean wait exit/signal")
    need(attestation.get("true_inner_pid") == value.get("true_inner_pid")
         and attestation.get("trampoline_pid") == value.get("trampoline_pid")
         and attestation.get("time_parent_pid") == value.get("gnu_time_pid"),
         "nested PID closure")
    timing = value.get("gnu_time")
    need(type(timing) is dict and set(timing) == {
        "command", "exit_status", "signal", "elapsed_text", "maxrss_kb",
    } and exact_int(timing.get("exit_status"), "GNU time exit") == 0
        and timing.get("signal") is None
        and timing.get("command") == value.get("expected_time_command"),
        "exact GNU time command/exit")
    captures = value.get("captures")
    need(type(captures) is list and bool(captures), "wrapper captures list")
    names: set[str] = set()
    for row in captures:
        need(type(row) is dict and set(row) == {"name", "sha256", "size", "stat9"}
             and type(row.get("name")) is str and type(row.get("sha256")) is str
             and HEX64.fullmatch(row["sha256"]) is not None
             and type(row.get("size")) is int and row["size"] >= 0
             and type(row.get("stat9")) is dict,
             "wrapper capture exact descriptor")
        need(row["name"] not in names, "unique capture name"); names.add(row["name"])
    need(names in ({"stdout.capture", "stderr.capture", "time.capture", "attestation.capture"},
                   {"stdout.capture", "stderr.capture", "time.capture",
                    "attestation.capture", "trace.capture"}),
         "exact wrapper capture inventory")
    return dict(value)


def validate_inner_output(kind: str, value: Mapping[str, Any]) -> None:
    need(type(value) is dict and type(value.get("schema")) is str
         and type(value.get("status")) is str, "inner output schema/status types")
    if kind == "preflight-validator":
        strict_preflight(value)
    elif kind == "receipt-validator":
        strict_transaction_receipt(value)
    elif kind in {"dual-verifier", "cold-verifier"}:
        need(value.get("schema")
             == "cm2.round306c30c.source-w-full-delta.independent-verification.candidate.v1"
             and value.get("status") == EXPECTED_VERIFIER_STATUS,
             "verifier exact schema/status")
        need(exact_int(value.get("formal_credit"), "verifier credit") == 0
             and exact_bool(value.get("manifest_authorized"), "verifier manifest") is False
             and value.get("proposed_source_W_remaining_transition") == "80->78",
             "verifier zero-credit diagnostic conclusion")
    elif kind == "cold-analyzer":
        need(value.get("schema") == "cm2.round306c30c.cold-strace-audit.v2"
             and value.get("status") == EXPECTED_ANALYZER_STATUS
             and exact_int(value.get("exit_status"), "analyzer exit") == 0
             and exact_int(value.get("top_level_stdout_writes"),
                           "analyzer stdout writes") == 1
             and exact_int(value.get("top_level_stdout_write_bytes"),
                           "analyzer stdout bytes") == 1839
             and exact_int(value.get("stderr_write_syscalls"),
                           "analyzer stderr writes") == 0
             and exact_int(value.get("stderr_bytes"),
                           "analyzer stderr bytes") == 0
             and exact_int(value.get("protected_path_mutations"), "analyzer mutation") == 0
             and exact_int(value.get("protected_fd_writes"), "analyzer FD writes") == 0
             and exact_int(value.get("protected_write_capable_opens"),
                           "analyzer write-capable opens") == 0
             and exact_int(value.get("historical_candidate_reads"),
                           "analyzer historical candidate reads") == 0
             and exact_int(value.get("network_syscalls"), "analyzer network") == 0,
             "analyzer exact no-mutation conclusion")
    elif kind == "pairing-gate":
        need(value.get("schema")
             == "cm2.round306c30c.cold-trace-unfinished-pairing-attack-gate.v1"
             and value.get("status") == EXPECTED_PAIRING_STATUS
             and exact_int(value.get("attack_count"), "pairing attacks") == 7
             and exact_int(value.get("formal_credit"), "pairing credit") == 0
             and exact_bool(value.get("source_W_transition_authorized"),
                            "pairing transition") is False,
             "pairing exact zero-credit conclusion")
    else:
        raise Reject("unknown inner output kind")


def input_snapshot(observations: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    return closed({
        "schema": "cm2.round306c30c.bridge-v3-input-snapshot.v1",
        "roles": [dict(observations[key]) for key in sorted(observations)],
        "role_count": len(observations), "formal_credit": 0,
        "source_W_formal_remainder": 80,
        "source_W_transition_authorized": False,
        "publication_authorized": False, "terminal_replay_completed": False,
    })


def read_scratch_capture(
    scratch: HeldDir, descriptor: Mapping[str, Any], maximum: int,
) -> bytes:
    name = descriptor["name"]
    raw, state = scratch.open_regular(name, maximum)
    need(hashlib.sha256(raw).hexdigest() == descriptor["sha256"]
         and len(raw) == descriptor["size"] and state == descriptor["stat9"],
         "scratch capture descriptor/full9stat:" + name)
    return raw


def run_stage(
    root: HeldDir, stage_name: str, kind: str, request: Mapping[str, Any],
    observations_before: Mapping[str, Mapping[str, Any]],
    material_reverify: Any, seen_inner_pids: set[int],
) -> tuple[dict[str, Any], bytes, HeldDir]:
    stage = root.mkdir_once(stage_name)
    pre_tree = recursive_snapshot(stage)
    stage.write_json("pre_recursive_snapshot.json", pre_tree)
    verify_snapshot_extension(
        pre_tree, recursive_snapshot(stage), "pre_recursive_snapshot.json",
    )
    request_raw = canonical(dict(request)) + b"\n"
    request_sha = hashlib.sha256(request_raw).hexdigest()
    stage.write_once("request.json", request_raw)
    before = input_snapshot(observations_before)
    stage.write_json("input_pre.snapshot.json", before)

    scratch_path = Path(tempfile.mkdtemp(prefix="cm2-c30c-bridge-v3-wrapper-"))
    os.chmod(scratch_path, 0o700)
    scratch = HeldDir(scratch_path, "nonformal process scratch", fresh=True)
    wrapper_argv = [
        os.fspath(FINAL_PYTHON), "-I", "-B", os.fspath(WRAPPER), "--run",
        "--request", os.fspath(stage.path / "request.json"),
        "--request-sha256", request_sha, "--scratch", os.fspath(scratch_path),
    ]
    wrapper_env = dict(BASE_ENV)
    started_ns = time.time_ns()
    wrapper_process = subprocess.Popen(
        wrapper_argv, cwd=WORKSPACE, env=wrapper_env, stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True,
    )
    wrapper_pid = wrapper_process.pid
    wrapper_stdout, wrapper_stderr = wrapper_process.communicate()
    wrapper_returncode = wrapper_process.returncode
    ended_ns = time.time_ns()
    need(wrapper_returncode == 0 and wrapper_stderr == b"",
         "process wrapper clean exit/stderr")
    wrapper_value = validate_wrapper_receipt(
        strict_json(wrapper_stdout, "process wrapper stdout"), request_sha,
    )
    need(wrapper_value["wrapper_pid"] == wrapper_pid,
         "actual Popen wrapper PID/receipt closure")
    need(wrapper_value["true_inner_pid"] not in seen_inner_pids,
         "independent true inner PID across stages")
    seen_inner_pids.add(wrapper_value["true_inner_pid"])
    descriptors = {row["name"]: row for row in wrapper_value["captures"]}
    need(set(scratch.names()) == set(descriptors), "scratch exact output inventory")
    published_names = {
        "stdout.capture": "stdout.json", "stderr.capture": "stderr.log",
        "time.capture": "time.txt", "attestation.capture": "inner_attestation.json",
        "trace.capture": "trace.raw",
    }
    published: dict[str, bytes] = {}
    for scratch_name in sorted(descriptors):
        maximum = 8 << 30 if scratch_name == "trace.capture" else 256 << 20
        raw = read_scratch_capture(scratch, descriptors[scratch_name], maximum)
        formal_name = published_names[scratch_name]
        stage.write_once(formal_name, raw)
        published[formal_name] = raw
    scratch.verify()
    stage.write_once("process_wrapper_stdout.json", wrapper_stdout)
    stage.write_once("process_wrapper_stderr.log", wrapper_stderr)
    stage.write_json("process_wrapper_receipt.json", wrapper_value)
    process_receipt = closed({
        "schema": "cm2.round306c30c.bridge-v3-wrapper-process.v1",
        "status": "PASS_DIRECT_WRAPPER_PROCESS_ZERO_CREDIT",
        "argv": wrapper_argv, "env": wrapper_env,
        "wrapper_pid": wrapper_pid, "numeric_exit_code": wrapper_returncode,
        "signal": None, "stderr_empty": True,
        "stdout_sha256": hashlib.sha256(wrapper_stdout).hexdigest(),
        "started_ns": started_ns, "ended_ns": ended_ns,
        "wrapper_object_sha256": wrapper_value["object_sha256"],
        "true_inner_pid": wrapper_value["true_inner_pid"],
        "formal_credit": 0, "source_W_formal_remainder": 80,
        "source_W_transition_authorized": False,
        "publication_authorized": False, "terminal_replay_completed": False,
    })
    stage.write_json("wrapper_process_attestation.json", process_receipt)
    need(published.get("stderr.log") == b"", "true inner stderr empty")
    inner = strict_json(published["stdout.json"], "true inner stdout")
    validate_inner_output(kind, inner)
    conclusion = closed({
        "schema": "cm2.round306c30c.bridge-v3-stage-conclusion.v1",
        "status": "PASS_STAGE_ZERO_CREDIT__" + kind.upper().replace("-", "_"),
        "stage": stage_name, "kind": kind,
        "inner_stdout_sha256": hashlib.sha256(published["stdout.json"]).hexdigest(),
        "inner_attestation_sha256": hashlib.sha256(
            published["inner_attestation.json"]).hexdigest(),
        "wrapper_receipt_object_sha256": wrapper_value["object_sha256"],
        "formal_credit": 0, "source_W_formal_remainder": 80,
        "source_W_transition_authorized": False,
        "publication_authorized": False, "terminal_replay_completed": False,
    })
    stage.write_json("stage_conclusion.json", conclusion)
    observations_after = material_reverify()
    after = input_snapshot(observations_after)
    need(before == after, "stage full pin input pre/post identity")
    stage.write_json("input_post.snapshot.json", after)
    post_tree = recursive_snapshot(stage)
    stage.write_json("post_recursive_snapshot.json", post_tree)
    verify_snapshot_extension(
        post_tree, recursive_snapshot(stage), "post_recursive_snapshot.json",
    )
    final_stage_tree = recursive_snapshot(stage)
    stage.write_json("final_recursive_snapshot.json", final_stage_tree)
    verify_snapshot_extension(
        final_stage_tree, recursive_snapshot(stage), "final_recursive_snapshot.json",
    )
    stage.verify(); root.verify(); scratch.close()
    return conclusion, published["stdout.json"], stage


def publish_failure(root: HeldDir, error: BaseException) -> None:
    # READY is deliberately non-authoritative, so a durability failure after
    # its rename may append FAILED.  No worker-side PASS marker exists in v5.
    need("PASS.lock" not in root.names() and "COMPOSITE_PASS.lock" not in root.names(),
         "worker cannot append failure after an authoritative marker")
    failure = closed({
        "schema": BOUNDARY_SCHEMA, "status": "BLOCKED_FAIL_CLOSED",
        "error_type": type(error).__name__, "error": str(error),
        "formal_credit": 0, "source_W_formal_remainder": 80,
        "source_W_transition_authorized": False,
        "publication_authorized": False, "terminal_replay_completed": False,
        "CM2": "NO-GO_FOR_CLAIM",
    })
    raw = canonical(failure) + b"\n"
    if "failure_receipt.json" in root.names():
        existing = strict_json(
            root.open_regular("failure_receipt.json", 4 << 20)[0], "existing failure",
        )
        verify_closure(existing, "existing failure")
        zero_contract(existing, "existing failure")
        need(existing.get("status") == "BLOCKED_FAIL_CLOSED", "existing failure status")
    else:
        root.write_once("failure_receipt.json", raw)
    # FAILED is always attempted/verified even when a failure receipt preexists.
    root.write_or_verify("FAILED.lock", FAILED_BYTES)
    root.verify()


PREPARED_READY = ".READY.lock.prepared-v5"


def prepare_ready(root: HeldDir) -> None:
    names = set(root.names())
    need("failure_receipt.json" not in names and "FAILED.lock" not in names
         and "READY.lock" not in names and PREPARED_READY not in names
         and "PASS.lock" not in names and "COMPOSITE_PASS.lock" not in names,
         "READY-after-failure/preexisting terminal marker forbidden")
    # The bytes and inode are fully written, reopened and verified while still
    # under a hidden name.  READY remains non-authoritative after publication.
    root.write_once(PREPARED_READY, READY_BYTES)


def commit_ready_last(root: HeldDir) -> None:
    names = set(root.names())
    need(PREPARED_READY in names and "READY.lock" not in names
         and "failure_receipt.json" not in names and "FAILED.lock" not in names,
         "exact prepared READY commit state")
    raw, state = root.open_regular(PREPARED_READY, 128)
    need(raw == READY_BYTES and state["nlink"] == 1,
         "prepared READY exact bytes/inode")
    libc = ctypes.CDLL(None, use_errno=True)
    renameat2 = libc.renameat2
    renameat2.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int,
                          ctypes.c_char_p, ctypes.c_uint]
    renameat2.restype = ctypes.c_int
    result = renameat2(
        root.fd, PREPARED_READY.encode("ascii"), root.fd, b"READY.lock", 1,
    )  # RENAME_NOREPLACE
    if result != 0:
        number = ctypes.get_errno()
        raise OSError(number, os.strerror(number))
    # A failing post-rename fsync makes the worker fail.  READY alone is never
    # authoritative; the composite finalizer also requires worker unit exit 0.
    os.fsync(root.fd)


def close_required_before_ready(resource: Any, label: str) -> None:
    try:
        resource.close()
    except OSError as error:
        raise Reject("required pre-READY close failed:" + label) from error


def close_silently(resource: Any | None) -> None:
    if resource is not None:
        try:
            resource.close()
        except OSError:
            pass


def wait_transaction_service(
    runtime: RuntimeAuthority, anchor: Mapping[str, Any], fragment: HeldFile,
    maximum_wait: int,
) -> dict[str, Any]:
    need(type(maximum_wait) is int and 0 <= maximum_wait <= 7 * 24 * 3600,
         "bounded wait seconds")
    deadline = time.monotonic() + maximum_wait
    while True:
        try:
            attestation = validate_service(
                runtime, anchor["transaction_service"], None, fragment, "transaction",
            )
            if RECEIPT.is_dir() and (RECEIPT / "receipt.json").is_file():
                return attestation
        except Reject:
            pass
        need(time.monotonic() < deadline, "transaction service/receipt wait timeout")
        time.sleep(2)


def math_env(seed: str | None = None) -> dict[str, str]:
    output = dict(BASE_ENV)
    if seed is not None:
        need(re.fullmatch(r"[0-9]{8}", seed) is not None, "seed token")
        output["PYTHONHASHSEED"] = seed
    return output


def run_bridge(
    bridge_path: Path, pinset_path: Path, anchor_path: Path,
    unit: str, maximum_wait: int, executed_watcher: Mapping[str, Any],
    terminal_watcher_release: Callable[[], None],
) -> None:
    need(type(executed_watcher) is dict
         and set(executed_watcher) == {"path", "sha256", "stat9"}
         and executed_watcher.get("path") == os.fspath(WATCHER)
         and type(executed_watcher.get("sha256")) is str
         and HEX64.fullmatch(executed_watcher["sha256"]) is not None
         and type(executed_watcher.get("stat9")) is dict,
         "exact held-bootstrap executed watcher binding")
    raw_bridge = Path(os.path.abspath(os.fspath(bridge_path)))
    need(raw_bridge.parent == AUDIT
         and raw_bridge.name.startswith("c30c-postreceipt-v3-p1-bridge-v5-")
         and all(token not in raw_bridge.name
                 for token in ("bridge-v1", "bridge-v2", "bridge-v3")),
         "fresh bridge-v5 audit namespace")
    bridge = HeldDir(raw_bridge, "formal bridge root", fresh=True)
    anchor_file = HeldFile(anchor_path, "launch anchor", 8 << 20)
    pinset_file = HeldFile(pinset_path, "launch pinset", 16 << 20)
    self_file = HeldFile(WATCHER, "current __file__ watcher", 8 << 20)
    gate_file = HeldFile(START_GATE, "ExecStartPre gate", 8 << 20)
    wrapper_file = HeldFile(WRAPPER, "process wrapper", 8 << 20)
    runtime = RuntimeAuthority()
    bridge_fragment: HeldFile | None = None
    transaction_fragment: HeldFile | None = None
    stages: list[HeldDir] = []
    ready_published = False
    try:
        need(Path(__file__).is_absolute()
             and Path(__file__).lstat().st_ino == self_file.initial.st_ino,
             "current __file__ exact held identity")
        need(self_file.sha256 == executed_watcher["sha256"]
             and stat9(self_file.initial) == executed_watcher["stat9"],
             "executed watcher bytes/full9stat == held watcher")
        anchor = parse_anchor(anchor_file)
        need(pinset_file.sha256 == anchor["pinset_sha256"],
             "anchor-bound pinset SHA without ExecStart self-cycle")
        need(anchor["bridge_service"]["Id"] == unit, "literal bridge unit")
        finalizer_unit = finalizer_unit_for_worker(raw_bridge, unit)
        bridge_fragment = HeldFile(
            Path(anchor["bridge_service"]["FragmentPath"]), "bridge fragment", 1 << 20,
        )
        transaction_fragment = HeldFile(
            TRANSACTION_FRAGMENT, "transaction fragment", 1 << 20,
        )
        observations = verify_launch_materials(
            anchor_file, pinset_file, self_file, gate_file, wrapper_file, bridge_fragment,
            transaction_fragment, runtime, anchor, bridge,
        )

        def reverify() -> dict[str, dict[str, Any]]:
            # systemd may discard ExecStart's transient pid/start-time status
            # after a manager reload while retaining MainPID and the service
            # cgroup.  Revalidate the exact allowed projection after every
            # external stage; no other pid or service-state drift is accepted.
            validate_bridge_service(
                runtime, anchor["bridge_service"], bridge_fragment,
                os.getpid(), allow_execstart_projection_decay=True,
            )
            return verify_launch_materials(
                anchor_file, pinset_file, self_file, gate_file, wrapper_file, bridge_fragment,
                transaction_fragment, runtime, anchor, bridge,
            )

        bridge_pre = recursive_snapshot(bridge)
        bridge.write_json("root_pre_recursive_snapshot.json", bridge_pre)
        verify_snapshot_extension(
            bridge_pre, recursive_snapshot(bridge), "root_pre_recursive_snapshot.json",
        )
        bridge_service = wait_bridge_running_service(
            runtime, anchor["bridge_service"], bridge_fragment, os.getpid(),
        )
        bridge.write_json("bridge_running_service_attestation.json", bridge_service)
        preflight = closed({
            "schema": "cm2.round306c30c.postreceipt-bridge-v5-preflight.v1",
            "status": "PASS_GATE_RELEASE_RUNNING_PID_BOUND_AND_EXACT_PINS_ZERO_CREDIT",
            "anchor_sha256": anchor_file.sha256, "anchor_stat9": stat9(anchor_file.initial),
            "pinset_sha256": pinset_file.sha256, "pinset_stat9": stat9(pinset_file.initial),
            "watcher_sha256": self_file.sha256, "watcher_stat9": stat9(self_file.initial),
            "gate_sha256": gate_file.sha256, "gate_stat9": stat9(gate_file.initial),
            "wrapper_sha256": wrapper_file.sha256,
            "wrapper_stat9": stat9(wrapper_file.initial),
            "runtime_authority": runtime.baseline,
            "pinned_role_count": len(observations),
            "formal_credit": 0, "source_W_formal_remainder": 80,
            "source_W_transition_authorized": False,
            "publication_authorized": False, "terminal_replay_completed": False,
            "CM2": "NO-GO_FOR_CLAIM",
        })
        bridge.write_json("preflight.json", preflight)

        transaction_service = wait_transaction_service(
            runtime, anchor, transaction_fragment, maximum_wait,
        )
        bridge.write_json("transaction_service_attestation.json", transaction_service)
        transaction, transaction_raw, preflight_raw = validate_transaction_boundary()
        bridge.write_once("transaction_receipt.raw.json", transaction_raw)
        bridge.write_once("transaction_preflight.raw.json", preflight_raw)

        seen_inner_pids: set[int] = set()
        preflight_request = stage_request(
            "preflight-byte-replay",
            [os.fspath(FINAL_PYTHON), "-I", "-B", os.fspath(VALIDATOR), "--self-test"],
            math_env(), FINAL_PYTHON, False,
        )
        conclusion, replayed_preflight, stage = run_stage(
            bridge, "preflight-byte-replay", "preflight-validator",
            preflight_request, observations, reverify, seen_inner_pids,
        )
        stages.append(stage)
        strict_preflight(strict_json(replayed_preflight, "preflight byte replay"))
        need(replayed_preflight == preflight_raw, "preflight validator exact byte replay")

        receipt_request = stage_request(
            "receipt-validator-replay",
            [os.fspath(FINAL_PYTHON), "-I", "-B", os.fspath(VALIDATOR), os.fspath(RUN)],
            math_env(), FINAL_PYTHON, False,
        )
        _conclusion, replayed_receipt, stage = run_stage(
            bridge, "receipt-validator-replay", "receipt-validator",
            receipt_request, observations, reverify, seen_inner_pids,
        )
        stages.append(stage)
        need(replayed_receipt == transaction_raw, "receipt validator exact byte replay")

        dual_outputs: dict[str, bytes] = {}
        for seed, candidate in CANDIDATES.items():
            request = stage_request(
                "dual-seed-" + seed,
                [os.fspath(VENV_PYTHON), "-I", "-B", os.fspath(VERIFIER),
                 os.fspath(candidate)],
                math_env(seed), FINAL_PYTHON, False,
            )
            _conclusion, raw, stage = run_stage(
                bridge, "dual-seed-" + seed, "dual-verifier", request,
                observations, reverify, seen_inner_pids,
            )
            stages.append(stage); dual_outputs[seed] = raw
        need(dual_outputs["30630071"] == dual_outputs["30630929"],
             "dual real seed byte identity")
        bridge.write_json("dual_summary.json", closed({
            "schema": "cm2.round306c30c.bridge-v5-dual-summary.v1",
            "status": "PASS_DUAL_TRUE_INNER_PID_BYTE_IDENTICAL_ZERO_CREDIT",
            "seeds": ["30630071", "30630929"],
            "stdout_sha256": hashlib.sha256(dual_outputs["30630071"]).hexdigest(),
            "formal_credit": 0, "source_W_formal_remainder": 80,
            "source_W_transition_authorized": False,
            "publication_authorized": False, "terminal_replay_completed": False,
        }))

        cold_request = stage_request(
            "cold-seed-30630071",
            [os.fspath(STRACE), "-f", "-yy", "-s", "4096", "-e", "trace=all",
             "-o", "@CM2_TRACE_FD@", os.fspath(VENV_PYTHON), "-I", "-B",
             os.fspath(VERIFIER), os.fspath(CANDIDATES["30630071"])],
            math_env("30630071"), STRACE.resolve(strict=True), True,
        )
        _conclusion, cold_raw, cold_stage = run_stage(
            bridge, "cold-seed-30630071", "cold-verifier", cold_request,
            observations, reverify, seen_inner_pids,
        )
        stages.append(cold_stage)
        need(cold_raw == dual_outputs["30630071"], "cold/dual byte identity")

        analyzer_request = stage_request(
            "cold-trace-analyzer",
            [os.fspath(FINAL_PYTHON), "-I", "-B", os.fspath(ANALYZER),
             "--trace", os.fspath(cold_stage.path / "trace.raw"),
             "--stdout", os.fspath(cold_stage.path / "stdout.json"),
             "--stderr", os.fspath(cold_stage.path / "stderr.log"),
             "--time", os.fspath(cold_stage.path / "time.txt"),
             "--candidate-dir", os.fspath(CANDIDATES["30630071"])],
            math_env("30630071"), FINAL_PYTHON, False,
        )
        _conclusion, _raw, stage = run_stage(
            bridge, "cold-trace-analyzer", "cold-analyzer", analyzer_request,
            observations, reverify, seen_inner_pids,
        )
        stages.append(stage)
        pairing_request = stage_request(
            "cold-pairing-gate",
            [os.fspath(FINAL_PYTHON), "-I", "-B", os.fspath(PAIRING_GATE)],
            math_env("30630071"), FINAL_PYTHON, False,
        )
        _conclusion, _raw, stage = run_stage(
            bridge, "cold-pairing-gate", "pairing-gate", pairing_request,
            observations, reverify, seen_inner_pids,
        )
        stages.append(stage)
        need(len(seen_inner_pids) == 7, "seven independent true inner PIDs")

        final_service = validate_bridge_service(
            runtime, anchor["bridge_service"], bridge_fragment,
            os.getpid(), allow_execstart_projection_decay=True,
        )
        bridge.write_json(
            "bridge_final_running_service_attestation.json", final_service,
        )
        final_observations = reverify()
        need(input_snapshot(observations) == input_snapshot(final_observations),
             "full bridge pin/input stability")
        runtime.verify()
        root_post = recursive_snapshot(bridge)
        bridge.write_json("root_post_recursive_snapshot.json", root_post)
        verify_snapshot_extension(
            root_post, recursive_snapshot(bridge), "root_post_recursive_snapshot.json",
        )
        boundary = closed({
            "schema": BOUNDARY_SCHEMA,
            "status": "PASS_ZERO_CREDIT_POSTRECEIPT_BOUNDARY__PUBLICATION_NOT_AUTHORIZED",
            "anchor_sha256": anchor_file.sha256, "pinset_sha256": pinset_file.sha256,
            "transaction_receipt_sha256": hashlib.sha256(transaction_raw).hexdigest(),
            "preflight_replay_sha256": hashlib.sha256(preflight_raw).hexdigest(),
            "dual_stdout_sha256": hashlib.sha256(dual_outputs["30630071"]).hexdigest(),
            "independent_true_inner_pid_count": len(seen_inner_pids),
            "bridge_service_post_exit_verification_required": True,
            "bridge_service_revalidated_after_every_stage": True,
            "manager_reload_execstart_zero_projection_bounded": True,
            "prepared_ready_name": PREPARED_READY,
            "ready_commit_method": "renameat2_RENAME_NOREPLACE_then_parent_fsync",
            "ready_marker_authoritative": False,
            "required_authoritative_composite": [
                "composite_receipt.json", "COMPOSITE_PASS.lock",
                "post_exit_finalizer_unit_success",
            ],
            "required_finalizer_unit": finalizer_unit,
            "required_finalizer_path": os.fspath(COMPOSITE_FINALIZER),
            "required_finalizer_sha256":
                observations["bridge_composite_finalizer"]["sha256"],
            "required_finalizer_stat9":
                observations["bridge_composite_finalizer"]["stat9"],
            "formal_credit": 0, "source_W_formal_remainder": 80,
            "source_W_transition_authorized": False,
            "publication_authorized": False, "terminal_replay_completed": False,
            "CM2": "NO-GO_FOR_CLAIM",
        })
        bridge.write_json("terminal_boundary.json", boundary)
        success_stdout = closed({
            "schema": "cm2.round306c30c.bridge-v5-service-stdout.v1",
            "status": "READY_WORKER_STDOUT_AWAITING_POST_EXIT_COMPOSITE_FINALIZER",
            "boundary_object_sha256": boundary["object_sha256"],
            "formal_credit": 0, "source_W_formal_remainder": 80,
            "source_W_transition_authorized": False,
            "publication_authorized": False, "terminal_replay_completed": False,
            "CM2": "NO-GO_FOR_CLAIM",
        })
        bridge.write_json("service_stdout.json", success_stdout)
        prepare_ready(bridge)
        final_tree = recursive_snapshot(bridge)
        bridge.write_json("root_final_recursive_snapshot.json", final_tree)
        verify_snapshot_extension(
            final_tree, recursive_snapshot(bridge), "root_final_recursive_snapshot.json",
        )
        # Replays and every userspace close except the bridge dirfd happen
        # before READY.  The bridge dirfd is left to kernel process teardown.
        # READY is non-authoritative until the separate finalizer unit exits 0.
        reverify(); runtime.verify(); bridge.verify()
        need("FAILED.lock" not in bridge.names() and "failure_receipt.json" not in bridge.names(),
             "no failure before READY")
        while stages:
            close_required_before_ready(stages.pop(), "stage")
        close_required_before_ready(transaction_fragment, "transaction fragment")
        transaction_fragment = None
        close_required_before_ready(bridge_fragment, "bridge fragment")
        bridge_fragment = None
        close_required_before_ready(runtime, "runtime authority")
        runtime = None
        close_required_before_ready(wrapper_file, "wrapper source")
        wrapper_file = None
        close_required_before_ready(gate_file, "gate source")
        gate_file = None
        close_required_before_ready(self_file, "watcher source")
        self_file = None
        close_required_before_ready(pinset_file, "pinset")
        pinset_file = None
        close_required_before_ready(anchor_file, "anchor")
        anchor_file = None
        terminal_watcher_release()
        commit_ready_last(bridge)
        ready_published = True
        return
    finally:
        for stage in stages:
            close_silently(stage)
        close_silently(transaction_fragment)
        close_silently(bridge_fragment)
        close_silently(runtime)
        close_silently(wrapper_file)
        close_silently(gate_file)
        close_silently(self_file)
        close_silently(pinset_file)
        close_silently(anchor_file)
        if not ready_published:
            close_silently(bridge)


def rejected(callable_object: Any, label: str) -> str:
    try:
        callable_object()
    except (Reject, OSError, ValueError, TypeError, KeyError,
            subprocess.SubprocessError) as error:
        need(bool(str(error)), "nonempty fixture rejection:" + label)
        return str(error)
    raise Reject("negative fixture accepted:" + label)


def write_fixture(path: Path, raw: bytes, mode: int = 0o400) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, mode)
    try:
        write_all(fd, raw); os.fsync(fd)
    finally:
        os.close(fd)


def tiny_wrapper_receipt(root: Path) -> dict[str, Any]:
    request = closed({
        "schema": REQUEST_SCHEMA, "stage": "watcher-tiny",
        "inner_argv": [
            os.fspath(FINAL_PYTHON), "-I", "-B", "-c",
            "import time;print('{\"formal_credit\":0,\"publication_authorized\":false,\"source_W_formal_remainder\":80,\"source_W_transition_authorized\":false,\"status\":\"PASS_TINY\",\"terminal_replay_completed\":false}');time.sleep(.25)",
        ],
        "inner_env": math_env(), "expected_exe_real": os.fspath(FINAL_PYTHON),
        "trace_requested": False, "formal_credit": 0,
        "source_W_formal_remainder": 80,
        "source_W_transition_authorized": False,
        "publication_authorized": False, "terminal_replay_completed": False,
    })
    request_raw = canonical(request) + b"\n"; request_path = root / "request.json"
    write_fixture(request_path, request_raw)
    scratch = root / "scratch"; scratch.mkdir(mode=0o700)
    completed = subprocess.run(
        [os.fspath(FINAL_PYTHON), "-I", "-B", os.fspath(WRAPPER), "--run",
         "--request", os.fspath(request_path), "--request-sha256",
         hashlib.sha256(request_raw).hexdigest(), "--scratch", os.fspath(scratch)],
        cwd=WORKSPACE, env=BASE_ENV, stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    need(completed.returncode == 0 and completed.stderr == b"",
         "tiny production wrapper run")
    value = strict_json(completed.stdout, "tiny wrapper receipt")
    validate_wrapper_receipt(value, hashlib.sha256(request_raw).hexdigest())
    return value


def gate_self_test(executed_gate: Mapping[str, Any] | None = None) -> dict[str, Any]:
    attacks: dict[str, str] = {}
    bootstrap_verified = False
    if executed_gate is not None:
        row = make_pin_observation("bridge_start_gate", START_GATE)
        need(type(executed_gate) is dict
             and executed_gate.get("path") == row["path"]
             and executed_gate.get("sha256") == row["sha256"]
             and executed_gate.get("stat9") == row["stat9"],
             "selftest held-bootstrap executed gate binding")
        bootstrap_verified = True
    process_pid = os.getpid()
    for label, bootstrap in (
        ("gate", GATE_BOOTSTRAP), ("watcher", WATCHER_BOOTSTRAP),
    ):
        need(exact_systemd_show_argv([bootstrap], label) == [bootstrap],
             "shell-neutral single-token bootstrap:" + label)
    need(bootstrap_source_state_allowed(
        stat.S_IFREG | 0o444, 1, UID, UID, 0,
    ), "positive bootstrap precompile source predicate")
    bootstrap_state_negatives = {
        "nonregular": bootstrap_source_state_allowed(
            stat.S_IFDIR | 0o444, 1, UID, UID, 1,
        ),
        "writable_mode": bootstrap_source_state_allowed(
            stat.S_IFREG | 0o644, 1, UID, UID, 1,
        ),
        "non_singleton": bootstrap_source_state_allowed(
            stat.S_IFREG | 0o444, 2, UID, UID, 1,
        ),
        "wrong_owner": bootstrap_source_state_allowed(
            stat.S_IFREG | 0o444, 1, UID + 1, UID, 1,
        ),
        "oversize": bootstrap_source_state_allowed(
            stat.S_IFREG | 0o444, 1, UID, UID, 8388609,
        ),
    }
    need(not any(bootstrap_state_negatives.values()),
         "bootstrap precompile source predicate negatives")
    fixture_name = "c30c-postreceipt-v3-p1-bridge-v5-selftest"
    fixture_bridge = AUDIT / fixture_name
    fixture_control = CONTROL / fixture_name
    fixture_unit = "cm2-c30c-postreceipt-v3-p1-bridge-v5-selftest.service"
    fixture_finalizer_unit = (
        "cm2-c30c-postreceipt-v3-p1-bridge-v5-finalizer-selftest.service"
    )
    need(finalizer_unit_for_worker(fixture_bridge, fixture_unit)
         == fixture_finalizer_unit,
         "exact same-token composite finalizer unit derivation")
    need(required_pin_roles(TRANSACTION_FRAGMENT)["bridge_composite_finalizer"]
         == COMPOSITE_FINALIZER,
         "exact composite finalizer required pin role")
    fixture_watcher_sha = "a" * 64
    fixture_gate_sha = "b" * 64
    fixture_watcher_argv = expected_watcher_argv(
        fixture_bridge, fixture_control / "pinset.json",
        fixture_control / "launch-anchor.json", fixture_unit, 17,
        fixture_watcher_sha,
    )
    fixture_gate_argv = expected_gate_argv(
        fixture_bridge, fixture_control / "pinset.json",
        fixture_control / "launch-anchor.json", fixture_unit, 17,
        fixture_gate_sha, fixture_watcher_sha,
    )
    need(len(fixture_watcher_argv) == 18 and len(fixture_gate_argv) == 20,
         "exact watcher/gate argv cardinalities")

    def fixture_exec_raw(
        argv: Sequence[str], pid: int = process_pid, start: str = "fixture",
        stop: str = "n/a", code: str = "(null)", status: str = "0/0",
    ) -> str:
        return (
            "{ path=" + os.fspath(FINAL_PYTHON)
            + " ; argv[]=" + " ".join(exact_systemd_show_argv(
                argv, "selftest fixture raw",
            ))
            + " ; ignore_errors=no ; start_time=[" + start + "] ; stop_time=["
            + stop + "] ; pid=" + str(pid) + " ; code=" + code
            + " ; status=" + status + " }"
        )

    need(parse_exec_command(
        fixture_exec_raw(fixture_watcher_argv), fixture_watcher_argv,
        FINAL_PYTHON, True, "selftest watcher roundtrip",
    )["argv"] == fixture_watcher_argv,
         "watcher exact argv parse roundtrip")
    need(parse_exec_command(
        fixture_exec_raw(fixture_gate_argv), fixture_gate_argv,
        FINAL_PYTHON, True, "selftest gate roundtrip",
    )["argv"] == fixture_gate_argv,
         "gate exact argv parse roundtrip")
    running_fields = {
        "ActiveState": "active", "SubState": "running", "Result": "success",
        "ExecMainCode": "0", "ExecMainStatus": "0",
        "MainPID": str(process_pid), "ControlPID": "0",
    }
    start_pre_fields = {
        "ActiveState": "activating", "SubState": "start-pre",
        "Result": "success", "ExecMainCode": "0", "ExecMainStatus": "0",
        "MainPID": "0", "ControlPID": str(process_pid),
    }
    live_exec = {
        "pid": process_pid, "start_time": "fixture", "stop_time": "n/a",
        "code": "(null)", "status": "0/0",
    }
    completed_gate_exec = {
        "pid": process_pid, "start_time": "fixture",
        "stop_time": "fixture-complete", "code": "exited", "status": "0",
    }
    need(validate_running_live_fields(
        running_fields, live_exec, process_pid,
    )["outer_process_binding"] is True, "positive running PID binding")
    decayed_exec = {
        "pid": 0, "start_time": "n/a", "stop_time": "n/a",
        "code": "(null)", "status": "0/0",
    }
    parsed_decay = parse_exec_command(
        fixture_exec_raw(
            fixture_watcher_argv, pid=0, start="n/a", stop="n/a",
        ),
        fixture_watcher_argv, FINAL_PYTHON, True,
        "selftest manager reload decay",
        allow_started_projection_decay=True,
    )
    need(parsed_decay["pid"] == 0 and validate_running_live_fields(
        running_fields, decayed_exec, process_pid,
        allow_execstart_projection_decay=True,
    )["ExecStartProjection"] == "manager-reload-decayed-zero",
         "positive bounded manager reload decay")
    parsed_pre_decay = parse_exec_command(
        fixture_exec_raw(
            fixture_gate_argv, pid=0, start="n/a", stop="n/a",
        ),
        fixture_gate_argv, FINAL_PYTHON, True,
        "selftest manager reload gate decay",
        allow_started_projection_decay=True,
    )
    need(parsed_pre_decay["pid"] == 0,
         "positive bounded ExecStartPre manager reload decay")
    need(validate_gate_phase_fields(
        start_pre_fields, decayed_exec, live_exec,
        process_pid,
    )["gate_process_binding"] is True, "positive start-pre PID binding")

    attacks["start_pre_state_as_running"] = rejected(
        lambda: validate_running_live_fields(
            start_pre_fields, live_exec, process_pid,
        ), "start-pre state accepted as running",
    )
    attacks["running_state_as_start_pre"] = rejected(
        lambda: validate_gate_phase_fields(
            running_fields, decayed_exec, live_exec, process_pid,
        ), "running state accepted as start-pre",
    )
    attacks["stale_future_execstart_pid"] = rejected(
        lambda: validate_gate_phase_fields(
            start_pre_fields, {**decayed_exec, "pid": process_pid - 1},
            live_exec, process_pid,
        ), "stale future ExecStart pid",
    )
    attacks["outer_pid_substitution"] = rejected(
        lambda: validate_running_live_fields(
            running_fields, {**live_exec, "pid": process_pid + 1}, process_pid,
        ), "outer PID substitution",
    )
    attacks["future_execstart_stale_metadata"] = rejected(
        lambda: validate_gate_phase_fields(
            start_pre_fields,
            {**decayed_exec, "start_time": "stale", "code": "exited",
             "status": "77"},
            live_exec, process_pid,
        ), "future ExecStart stale metadata",
    )
    attacks["live_execstart_stale_metadata"] = rejected(
        lambda: validate_running_live_fields(
            running_fields,
            {**live_exec, "stop_time": "already-stopped", "code": "exited",
             "status": "77"},
            process_pid,
        ), "live ExecStart stale metadata",
    )
    attacks["completed_execstartpre_stale_metadata"] = rejected(
        lambda: validate_completed_exec_projection(
            {**completed_gate_exec, "stop_time": "n/a", "status": "77"},
            "completed ExecStartPre stale fixture",
        ), "completed ExecStartPre stale metadata",
    )
    decayed_wrong_main = dict(running_fields)
    decayed_wrong_main["MainPID"] = str(process_pid + 1)
    attacks["decayed_projection_main_pid_substitution"] = rejected(
        lambda: validate_running_live_fields(
            decayed_wrong_main, decayed_exec, process_pid,
            allow_execstart_projection_decay=True,
        ), "decayed projection MainPID substitution",
    )
    attacks["malformed_execstart_zero_projection"] = rejected(
        lambda: parse_exec_command(
            fixture_exec_raw(
                fixture_watcher_argv, pid=0, start="fixture", stop="n/a",
            ),
            fixture_watcher_argv, FINAL_PYTHON, True,
            "malformed reload decay",
            allow_started_projection_decay=True,
        ), "malformed ExecStart zero projection",
    )
    attacks["malformed_execstartpre_zero_projection"] = rejected(
        lambda: parse_exec_command(
            fixture_exec_raw(
                fixture_gate_argv, pid=0, start="n/a", stop="fixture",
            ),
            fixture_gate_argv, FINAL_PYTHON, True,
            "malformed gate reload decay",
            allow_started_projection_decay=True,
        ), "malformed ExecStartPre zero projection",
    )
    attacks["stale_invocation_id"] = rejected(
        lambda: validate_invocation_binding(
            "0" * 32, "1" * 32, "stale authority fixture",
        ), "stale InvocationID",
    )
    stable_projection: dict[str, Any] = {
        key: "fixture" for key in BRIDGE_STABLE_ANCHOR_FIELDS
    }
    stable_projection["ExecStart"] = ["watcher"]
    stable_projection["ExecStartPre"] = ["gate"]
    stable_projection["FragmentStat9"] = {}
    validate_bridge_anchor_projection(stable_projection)
    injected_start_pre = dict(stable_projection)
    injected_start_pre["SubState"] = "start-pre"
    attacks["start_pre_live_field_frozen_in_anchor"] = rejected(
        lambda: validate_bridge_anchor_projection(injected_start_pre),
        "start-pre live field injected into stable anchor",
    )

    with tempfile.TemporaryDirectory(prefix="cm2-c30c-bridge-v5-gate-selftest-") as temporary:
        root = Path(temporary); os.chmod(root, 0o700)
        pinset_path = root / "pinset.json"
        anchor_path = root / "launch-anchor.json"
        pinset_raw = b"{\"fixture\":\"pinset-first\"}\n"
        anchor_raw = b"{\"fixture\":\"anchor-last\"}\n"
        atomic_publish_bytes(pinset_path, pinset_raw, "selftest pinset")
        need(not anchor_path.exists(), "anchor absent after pinset-first release")
        attacks["anchor_visible_before_pinset"] = "anchor absent after durable pinset"
        attacks["pinset_overwrite"] = rejected(
            lambda: atomic_publish_bytes(pinset_path, pinset_raw, "overwrite"),
            "pinset no-replace",
        )
        atomic_publish_bytes(anchor_path, anchor_raw, "selftest anchor")
        pinset_held = HeldFile(pinset_path, "selftest published pinset")
        anchor_held = HeldFile(anchor_path, "selftest published anchor")
        try:
            need(sorted(path.name for path in root.iterdir())
                 == ["launch-anchor.json", "pinset.json"]
                 and pinset_held.raw == pinset_raw and anchor_held.raw == anchor_raw,
                 "pinset then anchor-last exact durable inventory")
        finally:
            anchor_held.close(); pinset_held.close()

        fragment = root / "fragment"; write_fixture(fragment, b"fragment\n")
        held_fragment = HeldFile(fragment, "stale fragment authority fixture")
        replacement = root / "fragment.replacement"
        write_fixture(replacement, b"fragment\n")
        os.replace(replacement, fragment)
        attacks["stale_fragment_authority"] = rejected(
            held_fragment.verify, "stale FragmentPath inode",
        )
        held_fragment.close()

    need(set(attacks) == {
        "start_pre_state_as_running", "running_state_as_start_pre",
        "stale_future_execstart_pid", "outer_pid_substitution",
        "future_execstart_stale_metadata", "live_execstart_stale_metadata",
        "completed_execstartpre_stale_metadata",
        "decayed_projection_main_pid_substitution",
        "malformed_execstart_zero_projection",
        "malformed_execstartpre_zero_projection",
        "stale_invocation_id", "start_pre_live_field_frozen_in_anchor",
        "anchor_visible_before_pinset",
        "pinset_overwrite", "stale_fragment_authority",
    }, "exact fifteen gate negative/release fixture inventory")
    return closed({
        "schema": "cm2.round306c30c.postreceipt-bridge-v5-start-gate-selftest.v1",
        "status": "PASS_15_START_GATE_RELOAD_DECAY_AND_LIVE_PID_NEGATIVE_RELEASE_FIXTURES",
        "negative_release_fixture_count": len(attacks),
        "negative_release_fixtures": attacks,
        "exact_exec_argv_cardinality": {"watcher": 18, "gate": 20},
        "exact_exec_argv_roundtrip": True,
        "bounded_manager_reload_projection_roundtrip": True,
        "bootstrap_shell_neutral_single_tokens": True,
        "bootstrap_precompile_source_predicate_negative_count":
            len(bootstrap_state_negatives),
        "held_gate_bootstrap_verified": bootstrap_verified,
        "formal_execution_authorized": False,
        "formal_credit": 0, "source_W_formal_remainder": 80,
        "source_W_transition_authorized": False,
        "publication_authorized": False, "terminal_replay_completed": False,
        "CM2": "NO-GO_FOR_CLAIM",
    })


def post_ready_fault_injection_self_test(parent: Path) -> dict[str, str]:
    """Prove commit-fsync/close/replay faults cannot create authority."""
    results: dict[str, str] = {}
    for label in ("commit_fsync", "close", "replay"):
        path = parent / ("post-ready-" + label)
        path.mkdir(mode=0o700)
        pid = os.fork()
        if pid == 0:
            try:
                root = HeldDir(path, "post-READY " + label, fresh=True)
                prepare_ready(root)
                if label == "commit_fsync":
                    original_fsync = os.fsync

                    def injected_fsync(_fd: int) -> None:
                        raise OSError(5, "injected READY commit fsync fault")

                    os.fsync = injected_fsync
                    try:
                        # commit_ready_last performs the no-replace rename and
                        # then this injected parent fsync fails.  READY may be
                        # visible but the worker must exit nonzero, so the
                        # joint post-exit finalizer gate rejects it.
                        commit_ready_last(root)
                    finally:
                        os.fsync = original_fsync
                else:
                    commit_ready_last(root)
                if label == "close":
                    original_close = os.close

                    def injected_close(_fd: int) -> None:
                        raise OSError(5, "injected post-READY close fault")

                    os.close = injected_close
                    try:
                        root.close()
                    finally:
                        os.close = original_close
                else:
                    raise Reject("injected post-READY held-source replay fault")
            except BaseException:
                os._exit(73)
            os._exit(0)
        waited, status = os.waitpid(pid, 0)
        need(waited == pid and os.WIFEXITED(status) and os.WEXITSTATUS(status) == 73,
             "post-READY fault forces nonzero worker exit:" + label)
        held = HeldDir(path, "post-READY parent audit:" + label)
        try:
            need(held.names() == ["READY.lock"]
                 and held.open_regular("READY.lock", 128)[0] == READY_BYTES,
                 "fault leaves only exact non-authoritative READY:" + label)
        finally:
            held.close()
        result_name = "fsync_during_ready_commit" if label == "commit_fsync" \
            else label + "_after_ready"
        results[result_name] = (
            "worker exit 73; READY non-authoritative; no PASS/composite marker"
        )
    need(set(results) == {
        "fsync_during_ready_commit", "close_after_ready", "replay_after_ready",
    }, "exact post-READY fault injection inventory")
    return results


def self_test(executed_watcher: Mapping[str, Any] | None = None) -> dict[str, Any]:
    attacks: dict[str, str] = {}
    bootstrap_verified = False
    runtime_fixture = os.stat_result((
        stat.S_IFDIR | 0o700, 41, 68, 2, UID, UID, 80, 1, 2, 3,
    ))
    runtime_mutable_metadata = os.stat_result((
        stat.S_IFDIR | 0o700, 41, 68, 99, UID, UID, 9999, 4, 5, 6,
    ))
    runtime_inode_substitution = os.stat_result((
        stat.S_IFDIR | 0o700, 42, 68, 2, UID, UID, 80, 1, 2, 3,
    ))
    need(stable_dir_identity(runtime_fixture)
         == stable_dir_identity(runtime_mutable_metadata)
         and stable_dir_identity(runtime_fixture)
             != stable_dir_identity(runtime_inode_substitution),
         "runtime directory mutable metadata projection only")
    if executed_watcher is not None:
        row = make_pin_observation("bridge_watcher", WATCHER)
        need(type(executed_watcher) is dict
             and executed_watcher.get("path") == row["path"]
             and executed_watcher.get("sha256") == row["sha256"]
             and executed_watcher.get("stat9") == row["stat9"],
             "selftest held-bootstrap executed watcher binding")
        bootstrap_verified = True
    bad_environment = dict(CONTROL_ENV)
    bad_environment["DBUS_SESSION_BUS_ADDRESS"] = "unix:path=/run/user/1000/cm2-missing-bus"
    bad_bus = subprocess.run(
        [os.fspath(SYSTEMCTL), "--user", "show", TRANSACTION_UNIT, "-p", "Id"],
        cwd=WORKSPACE, env=bad_environment, stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    need(bad_bus.returncode != 0 and bad_bus.stderr != b"", "real bad-bus route rejects")
    attacks["bad_bus_real_route"] = "systemctl rejected real missing bus route"

    validator = subprocess.run(
        [os.fspath(FINAL_PYTHON), "-I", "-B", os.fspath(VALIDATOR), "--self-test"],
        cwd=WORKSPACE, env=BASE_ENV, stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    preflight_held = HeldFile(RECEIPT / "preflight.json", "actual preflight", 4 << 20)
    try:
        need(validator.returncode == 0 and validator.stderr == b""
             and validator.stdout == preflight_held.raw,
             "production preflight validator byte replay")
        strict_preflight(strict_json(validator.stdout, "production preflight replay"))
    finally:
        preflight_held.close()

    with tempfile.TemporaryDirectory(prefix="cm2-c30c-bridge-v3-selftest-") as temporary:
        root_path = Path(temporary); os.chmod(root_path, 0o700)
        raw = b"same immutable bytes\n"
        for fixture_name in ("anchor", "pinset"):
            original = root_path / (fixture_name + ".json")
            write_fixture(original, raw)
            held = HeldFile(original, fixture_name + " substitution")
            replacement = root_path / (fixture_name + ".replacement")
            write_fixture(replacement, raw)
            os.replace(replacement, original)
            attacks[fixture_name + "_same_byte_inode_substitution"] = rejected(
                held.verify, fixture_name + " inode substitution",
            )
            held.close()

        hardlink_source = root_path / "hardlink-source"; write_fixture(hardlink_source, raw)
        os.link(hardlink_source, root_path / "hardlink-second")
        attacks["hardlink_input"] = rejected(
            lambda: HeldFile(hardlink_source, "hardlink"), "hardlink input",
        )

        rename_parent = root_path / "rename-parent"; rename_parent.mkdir(mode=0o700)
        rename_root = rename_parent / "root"; rename_root.mkdir(mode=0o700)
        held_root = HeldDir(rename_root, "rename fixture root", fresh=True)
        renamed = rename_parent / "renamed"; os.rename(rename_root, renamed)
        attacks["root_rename"] = rejected(held_root.verify, "root rename")
        held_root.close()

        fragment = root_path / "fragment"; write_fixture(fragment, b"fragment\n")
        held_fragment = HeldFile(fragment, "fragment fixture")
        replacement = root_path / "fragment-new"; write_fixture(replacement, b"fragment\n")
        os.replace(replacement, fragment)
        attacks["fragment_same_byte_inode_substitution"] = rejected(
            held_fragment.verify, "fragment replacement",
        )
        held_fragment.close()

        altered_preflight = dict(strict_json(validator.stdout, "fixture preflight"))
        altered_preflight["attack_contract_count"] = True
        attacks["preflight_bool_int_tamper"] = rejected(
            lambda: strict_preflight(altered_preflight), "preflight bool/int",
        )

        wrapper_root = root_path / "wrapper"; wrapper_root.mkdir(mode=0o700)
        wrapper_value = tiny_wrapper_receipt(wrapper_root)
        bad_pid = dict(wrapper_value)
        bad_attestation = dict(bad_pid["attestation"])
        bad_attestation.pop("object_sha256")
        bad_attestation["true_inner_pid"] = bad_attestation["trampoline_pid"]
        bad_pid["attestation"] = closed(bad_attestation)
        bad_pid["true_inner_pid"] = bad_pid["trampoline_pid"]
        bad_pid.pop("object_sha256")
        bad_pid = closed(bad_pid)
        attacks["inner_pid_substitution"] = rejected(
            lambda: validate_wrapper_receipt(bad_pid, wrapper_value["request_sha256"]),
            "inner PID substitution",
        )
        bad_time = dict(wrapper_value); timing = dict(bad_time["gnu_time"])
        timing["command"] += " --substituted"; bad_time["gnu_time"] = timing
        bad_time.pop("object_sha256"); bad_time = closed(bad_time)
        attacks["gnu_time_command_substitution"] = rejected(
            lambda: validate_wrapper_receipt(bad_time, wrapper_value["request_sha256"]),
            "GNU time substitution",
        )

        analyzer_fixture = {
            "schema": "cm2.round306c30c.cold-strace-audit.v2",
            "status": EXPECTED_ANALYZER_STATUS,
            "exit_status": 0, "top_level_stdout_writes": 1,
            "top_level_stdout_write_bytes": 1839,
            "stderr_write_syscalls": 0, "stderr_bytes": 0,
            "protected_path_mutations": 0, "protected_fd_writes": 0,
            "protected_write_capable_opens": 0,
            "historical_candidate_reads": 0, "network_syscalls": 0,
        }
        validate_inner_output("cold-analyzer", analyzer_fixture)
        for field in (
            "stderr_bytes", "protected_write_capable_opens",
            "historical_candidate_reads",
        ):
            substituted_analyzer = dict(analyzer_fixture)
            substituted_analyzer[field] = 1
            attacks["analyzer_" + field + "_substitution"] = rejected(
                lambda substituted_analyzer=substituted_analyzer, field=field:
                    validate_inner_output("cold-analyzer", substituted_analyzer),
                "analyzer " + field + " substitution",
            )

        output_dir_path = root_path / "output"; output_dir_path.mkdir(mode=0o700)
        output_dir = HeldDir(output_dir_path, "output symlink fixture", fresh=True)
        os.symlink("missing", output_dir_path / "stdout.json")
        attacks["output_symlink"] = rejected(
            lambda: output_dir.open_regular("stdout.json"), "output symlink",
        )
        output_dir.close()

        failure_path = root_path / "failure-root"; failure_path.mkdir(mode=0o700)
        failure_root = HeldDir(failure_path, "failure fixture", fresh=True)
        publish_failure(failure_root, Reject("fixture failure"))
        attacks["ready_after_failure"] = rejected(
            lambda: prepare_ready(failure_root), "READY after failure",
        )
        need(failure_root.open_regular("FAILED.lock", 128)[0] == FAILED_BYTES,
             "FAILED always durable after preexisting failure")
        failure_root.close()

        old_anchor = root_path / "bridge-v1-anchor.json"
        write_fixture(old_anchor, canonical(closed({"schema": "old-v1"})) + b"\n")
        old_held = HeldFile(old_anchor, "old v1 anchor")
        attacks["old_v1_anchor"] = rejected(lambda: parse_anchor(old_held), "old v1")
        old_held.close()

        ready_path = root_path / "ready-positive"; ready_path.mkdir(mode=0o700)
        ready_root = HeldDir(ready_path, "positive READY commit", fresh=True)
        prepare_ready(ready_root); commit_ready_last(ready_root)
        need(ready_root.names() == ["READY.lock"]
             and ready_root.open_regular("READY.lock", 128)[0] == READY_BYTES,
             "renameat2 no-replace non-authoritative READY selftest")
        ready_root.close()

    need(set(attacks) == {
        "bad_bus_real_route", "anchor_same_byte_inode_substitution",
        "pinset_same_byte_inode_substitution", "hardlink_input", "root_rename",
        "fragment_same_byte_inode_substitution", "preflight_bool_int_tamper",
        "inner_pid_substitution", "gnu_time_command_substitution",
        "output_symlink", "ready_after_failure", "old_v1_anchor",
        "analyzer_stderr_bytes_substitution",
        "analyzer_protected_write_capable_opens_substitution",
        "analyzer_historical_candidate_reads_substitution",
    }, "exact 15 negative fixture inventory")
    gate_tests = gate_self_test()
    with tempfile.TemporaryDirectory(
        prefix="cm2-c30c-bridge-v5-terminal-fault-selftest-",
    ) as terminal_temporary:
        terminal_parent = Path(terminal_temporary); os.chmod(terminal_parent, 0o700)
        terminal_faults = post_ready_fault_injection_self_test(terminal_parent)
    return closed({
        "schema": "cm2.round306c30c.postreceipt-bridge-v5-selftest.v1",
        "status": "PASS_15_PRODUCTION_3_POST_READY_FAULT_AND_15_GATE_NEGATIVES_ZERO_CREDIT",
        "production_preflight_byte_replay": True,
        "held_watcher_bootstrap_verified": bootstrap_verified,
        "renameat2_noreplace_ready_commit": True,
        "worker_ready_marker_authoritative": False,
        "post_ready_fault_injection_count": len(terminal_faults),
        "post_ready_fault_injections": terminal_faults,
        "post_ready_faults_require_nonzero_worker_exit": True,
        "authoritative_composite_requires_finalizer_unit_exit_success": True,
        "bridge_service_revalidated_after_every_stage": True,
        "manager_reload_execstart_zero_projection_bounded": True,
        "mainpid_proc_exe_and_service_cgroup_remain_bound": True,
        "runtime_directory_mutable_metadata_projection_bounded": True,
        "runtime_directory_inode_mode_owner_substitution_rejected": True,
        "negative_fixture_count": len(attacks), "negative_fixtures": attacks,
        "gate_negative_release_fixture_count":
            gate_tests["negative_release_fixture_count"],
        "gate_selftest_object_sha256": gate_tests["object_sha256"],
        "gate_exact_exec_argv_cardinality":
            gate_tests["exact_exec_argv_cardinality"],
        "gate_exact_exec_argv_roundtrip":
            gate_tests["exact_exec_argv_roundtrip"],
        "total_negative_release_fixture_count":
            len(attacks) + len(terminal_faults)
            + gate_tests["negative_release_fixture_count"],
        "formal_execution_authorized": False,
        "formal_credit": 0, "source_W_formal_remainder": 80,
        "source_W_transition_authorized": False,
        "publication_authorized": False, "terminal_replay_completed": False,
        "CM2": "NO-GO_FOR_CLAIM",
    })


def verify_executed_watcher_source(
    watcher_fd: int, watcher_state: os.stat_result, watcher_raw: bytes,
    expected_sha256: str,
) -> dict[str, Any]:
    need(Path(os.path.abspath(os.fspath(__file__))) == WATCHER,
         "exact executed watcher __file__ path")
    need(HEX64.fullmatch(expected_sha256) is not None
         and hashlib.sha256(watcher_raw).hexdigest() == expected_sha256,
         "executed watcher raw expected SHA")
    state_identity = identity(watcher_state)
    need(identity(WATCHER.lstat()) == state_identity
         and identity(os.fstat(watcher_fd)) == state_identity,
         "executed watcher path/held inode closure")
    need(read_all(watcher_fd, 8 << 20) == watcher_raw,
         "executed watcher exact held byte replay")
    return {
        "path": os.fspath(WATCHER), "sha256": expected_sha256,
        "stat9": stat9(watcher_state),
    }


def main_arguments(
    argv: Sequence[str], executed_watcher: Mapping[str, Any] | None = None,
    terminal_watcher_release: Callable[[], None] | None = None,
) -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--self-test", action="store_true")
    modes.add_argument("--run", action="store_true")
    parser.add_argument("--bridge-dir", type=Path)
    parser.add_argument("--pinset", type=Path)
    parser.add_argument("--anchor", type=Path)
    parser.add_argument("--unit")
    parser.add_argument("--maximum-wait-seconds", type=int, default=7 * 24 * 3600)
    arguments = parser.parse_args(list(argv))
    try:
        if arguments.self_test:
            need(all(value is None for value in (
                arguments.bridge_dir, arguments.pinset,
                arguments.anchor, arguments.unit,
            )), "selftest has no formal launch material")
            print(canonical(self_test(executed_watcher)).decode("ascii"))
            return 0
        need(executed_watcher is not None,
             "production run requires held -c watcher bootstrap")
        need(terminal_watcher_release is not None,
             "production run requires pre-READY held-watcher release")
        need(arguments.bridge_dir is not None and arguments.pinset is not None
             and arguments.anchor is not None and type(arguments.unit) is str,
             "complete direct-Python run material")
        run_bridge(
            arguments.bridge_dir, arguments.pinset, arguments.anchor,
            arguments.unit, arguments.maximum_wait_seconds, executed_watcher,
            terminal_watcher_release,
        )
        # Worker success is intentionally silent.  READY is not authoritative;
        # the post-exit finalizer must verify this unit exited successfully.
        return 0
    except (Reject, OSError, ValueError, TypeError, KeyError,
            subprocess.SubprocessError) as error:
        if arguments.run and arguments.bridge_dir is not None:
            try:
                root = HeldDir(arguments.bridge_dir, "failed bridge root")
                try:
                    publish_failure(root, error)
                finally:
                    root.close()
            except (Reject, OSError, ValueError, TypeError, KeyError):
                pass
        failure = closed({
            "schema": BOUNDARY_SCHEMA, "status": "BLOCKED_FAIL_CLOSED",
            "error": str(error), "formal_credit": 0,
            "source_W_formal_remainder": 80,
            "source_W_transition_authorized": False,
            "publication_authorized": False, "terminal_replay_completed": False,
            "CM2": "NO-GO_FOR_CLAIM",
        })
        print(canonical(failure).decode("ascii"), file=sys.stderr)
        return 2


def held_watcher_entry(
    watcher_fd: int, watcher_state: os.stat_result, watcher_raw: bytes,
    expected_sha256: str, argv: list[str],
) -> int:
    released = False

    def release_before_ready() -> None:
        nonlocal released
        verify_executed_watcher_source(
            watcher_fd, watcher_state, watcher_raw, expected_sha256,
        )
        os.close(watcher_fd)
        released = True

    try:
        binding = verify_executed_watcher_source(
            watcher_fd, watcher_state, watcher_raw, expected_sha256,
        )
        return main_arguments(argv, binding, release_before_ready)
    finally:
        if not released:
            try:
                os.close(watcher_fd)
            except OSError:
                pass


def main() -> int:
    return main_arguments(sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())
