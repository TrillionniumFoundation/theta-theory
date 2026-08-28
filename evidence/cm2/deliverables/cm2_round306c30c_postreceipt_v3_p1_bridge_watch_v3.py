#!/usr/bin/env python3
"""Fail-closed append-only C30c postreceipt bridge v3.

Development candidate only.  Its terminal object is a zero-credit boundary:
Source-W remains 80, transition/publication/terminal replay remain false, and
CM2 remains NO-GO.  The future formal service must execute the final Python
binary directly; there is deliberately no shell launcher or launcher override.
"""
from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import os
import re
import shlex
import stat
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


sys.dont_write_bytecode = True

WORKSPACE = Path("/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572")
DELIVERABLES = WORKSPACE / "deliverables"
AUDIT = WORKSPACE / ".cm2-runtime/audit"
CONTROL = WORKSPACE / ".cm2-runtime/control"
RECEIPTS = WORKSPACE / ".cm2-runtime/receipts"
SCRATCH_PARENT = WORKSPACE / ".cm2-runtime/tmp"

WATCHER = DELIVERABLES / "cm2_round306c30c_postreceipt_v3_p1_bridge_watch_v3.py"
WRAPPER = DELIVERABLES / "cm2_round306c30c_postreceipt_bridge_v3_process_wrapper_v1.py"
VALIDATOR = DELIVERABLES / "cm2_round306c30c_62_attack_run_receipt_validator_v3.py"
PREFIX = "cm2_round306c30c_source_w_full_delta_whole_origin_disposition"
HARNESS = DELIVERABLES / (PREFIX + "_attack_harness.py")
VERIFIER = DELIVERABLES / (PREFIX + "_independent_verifier.py")
ANALYZER = DELIVERABLES / (PREFIX + "_cold_trace_analyzer.py")
PAIRING_GATE = DELIVERABLES / "cm2_round306c30c_cold_trace_unfinished_pairing_attack_gate.py"

VENV_PYTHON = WORKSPACE / ".cm2-runtime/python-flint-0.9.0/bin/python"
VENV_PYTHON3 = WORKSPACE / ".cm2-runtime/python-flint-0.9.0/bin/python3"
SYSTEM_PYTHON_LINK = Path("/usr/bin/python3")
FINAL_PYTHON = Path("/usr/bin/python3.12")
GNU_TIME = Path("/usr/bin/time")
STRACE = Path("/usr/bin/strace")
ENV_BIN = Path("/usr/bin/env")
SYSTEMCTL = Path("/usr/bin/systemctl")

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

PINSET_SCHEMA = "cm2.round306c30c.postreceipt-bridge-v3-pinset.v1"
ANCHOR_SCHEMA = "cm2.round306c30c.postreceipt-bridge-v3-launch-anchor.v1"
REQUEST_SCHEMA = "cm2.round306c30c.bridge-v3-process-request.v1"
WRAPPER_RECEIPT_SCHEMA = "cm2.round306c30c.bridge-v3-process-wrapper-receipt.v1"
BOUNDARY_SCHEMA = "cm2.round306c30c.postreceipt-bridge-v3-boundary.v1"
PASS_BYTES = b"PASS_C30C_POSTRECEIPT_BRIDGE_V3_ZERO_CREDIT_BOUNDARY\n"
FAILED_BYTES = b"FAILED_C30C_POSTRECEIPT_BRIDGE_V3_FAIL_CLOSED\n"
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
    """Hold the user runtime, bus socket and systemctl identity end-to-end."""
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
        need(identity(runtime_current) == identity(self.runtime_state)
             == identity(runtime_held), "runtime full identity drift")
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


def parse_execstart(raw: str, expected_argv: Sequence[str]) -> dict[str, Any]:
    match = re.fullmatch(
        r"\{ path=([^ ;]+) ; argv\[\]=(.+) ; ignore_errors=no ; "
        r"start_time=\[(.*)\] ; stop_time=\[(.*)\] ; pid=([0-9]+) ; "
        r"code=([^ ;]+) ; status=([^ }]+) \}", raw,
    )
    need(match is not None, "strict ExecStart syntax")
    path, argv_text, start, stop, pid, code, status_text = match.groups()
    try:
        argv = shlex.split(argv_text, posix=True)
    except ValueError as error:
        raise Reject("strict ExecStart argv parse") from error
    need(path == os.fspath(FINAL_PYTHON) and argv == list(expected_argv),
         "direct final Python exact ExecStart")
    need(bool(start) and int(pid) > 1, "ExecStart start/pid")
    return {
        "path": path, "argv": argv, "start_time": start, "stop_time": stop,
        "pid": int(pid), "code": code, "status": status_text,
    }


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


def required_pin_roles(bridge_fragment: Path) -> dict[str, Path]:
    roles: dict[str, Path] = {
        "bridge_watcher": WATCHER, "process_wrapper": WRAPPER,
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


def parse_anchor(held: HeldFile) -> dict[str, Any]:
    need("bridge-v1" not in os.fspath(held.path)
         and "bridge-v2" not in os.fspath(held.path), "reject old anchor path")
    value = strict_json(held.raw, "launch anchor"); verify_closure(value, "launch anchor")
    required = {
        "schema", "status", "watcher_path", "watcher_sha256", "watcher_stat9",
        "wrapper_path", "wrapper_sha256", "wrapper_stat9", "pinset_path",
        "pinset_sha256", "pinset_stat9", "bridge_dir", "bridge_service",
        "transaction_service", "formal_credit", "source_W_formal_remainder",
        "source_W_transition_authorized", "publication_authorized",
        "terminal_replay_completed", "object_sha256",
    }
    need(set(value) == required and value.get("schema") == ANCHOR_SCHEMA
         and value.get("status") == "FROZEN_BRIDGE_V3_DIRECT_PYTHON_ZERO_CREDIT",
         "exact v3 anchor schema/fields")
    zero_contract(value, "anchor")
    for name in ("watcher_sha256", "wrapper_sha256", "pinset_sha256"):
        need(type(value.get(name)) is str and HEX64.fullmatch(value[name]) is not None,
             "anchor SHA:" + name)
    for name in ("watcher_stat9", "wrapper_stat9", "pinset_stat9"):
        need(type(value.get(name)) is dict and set(value[name]) == set(stat9(os.stat_result((0,) * 10))),
             "anchor stat9:" + name)
    for service_name in ("bridge_service", "transaction_service"):
        service = value.get(service_name)
        need(type(service) is dict, "anchor service object:" + service_name)
    bridge_service = value["bridge_service"]
    required_bridge = {
        "Id", "InvocationID", "ExecStart", "FragmentPath", "FragmentSHA256",
        "FragmentStat9", "LoadState", "ActiveState", "SubState", "Result",
        "ExecMainCode", "ExecMainStatus", "MainPID", "Type", "RemainAfterExit",
        "StandardOutput", "StandardError",
    }
    need(set(bridge_service) == required_bridge
         and type(bridge_service.get("ExecStart")) is list
         and all(type(item) is str for item in bridge_service["ExecStart"]),
         "exact bridge service anchor fields")
    transaction = value["transaction_service"]
    need(set(transaction) == required_bridge, "exact transaction service anchor fields")
    return value


def load_pinset(held: HeldFile, expected_sha: str, anchor: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    need("bridge-v1" not in os.fspath(held.path)
         and "bridge-v2" not in os.fspath(held.path), "reject old pinset path")
    need(type(expected_sha) is str and HEX64.fullmatch(expected_sha) is not None
         and held.sha256 == expected_sha, "pinset CLI SHA")
    value = strict_json(held.raw, "pinset"); verify_closure(value, "pinset")
    need(set(value) == {
        "schema", "status", "members", "formal_credit", "source_W_formal_remainder",
        "source_W_transition_authorized", "publication_authorized",
        "terminal_replay_completed", "object_sha256",
    } and value.get("schema") == PINSET_SCHEMA
        and value.get("status") == "FROZEN_EXACT_ROLE_SET_BRIDGE_V3_ZERO_CREDIT",
        "exact v3 pinset schema")
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


SERVICE_PROPERTIES = (
    "Id", "InvocationID", "ExecStart", "FragmentPath", "LoadState",
    "ActiveState", "SubState", "Result", "ExecMainCode", "ExecMainStatus",
    "MainPID", "Type", "RemainAfterExit", "StandardOutput", "StandardError",
)


def validate_anchor_bindings(
    anchor: Mapping[str, Any], anchor_file: HeldFile, pinset_file: HeldFile,
    self_file: HeldFile, wrapper_file: HeldFile, bridge: HeldDir,
) -> None:
    need(anchor.get("watcher_path") == os.fspath(WATCHER)
         and anchor.get("watcher_sha256") == self_file.sha256
         and anchor.get("watcher_stat9") == stat9(self_file.initial),
         "anchor watcher byte/full9stat binding")
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
    need(len(expected_argv) == 15 and expected_argv[:14] == [
        os.fspath(FINAL_PYTHON), "-I", "-B", os.fspath(WATCHER), "--run",
        "--bridge-dir", os.fspath(bridge.path), "--pinset",
        os.fspath(pinset_file.path), "--anchor", os.fspath(anchor_file.path), "--unit",
        anchor["bridge_service"]["Id"], "--maximum-wait-seconds",
    ] and re.fullmatch(r"[0-9]+", expected_argv[14]) is not None
        and 0 <= int(expected_argv[14]) <= 7 * 24 * 3600
        and "/bin/sh" not in expected_argv and os.fspath(WRAPPER) not in expected_argv,
         "direct final Python exact watcher ExecStart argv")
    invocation_environment = os.environ.get("INVOCATION_ID")
    need(type(invocation_environment) is str
         and invocation_environment == anchor["bridge_service"]["InvocationID"],
         "service INVOCATION_ID environment/anchor closure")


def validate_service(
    runtime: RuntimeAuthority, expected: Mapping[str, Any],
    expected_argv: Sequence[str] | None, fragment_held: HeldFile,
    label: str,
) -> dict[str, Any]:
    unit = exact_string(expected.get("Id"), label + ":Id")
    fields, raw = runtime.query(unit, SERVICE_PROPERTIES)
    for key in SERVICE_PROPERTIES:
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
        "schema": "cm2.round306c30c.bridge-v3-service-attestation.v1",
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


def verify_launch_materials(
    anchor_file: HeldFile, pinset_file: HeldFile, self_file: HeldFile,
    wrapper_file: HeldFile, bridge_fragment: HeldFile,
    transaction_fragment: HeldFile, runtime: RuntimeAuthority,
    anchor: Mapping[str, Any], bridge: HeldDir,
) -> dict[str, dict[str, Any]]:
    for held in (anchor_file, pinset_file, self_file, wrapper_file,
                 bridge_fragment, transaction_fragment):
        held.verify()
    runtime.verify(); bridge.verify()
    parsed = parse_anchor(anchor_file)
    need(parsed == dict(anchor), "anchor stable parsed object")
    _pinset, observations = load_pinset(pinset_file, anchor["pinset_sha256"], anchor)
    validate_anchor_bindings(
        anchor, anchor_file, pinset_file, self_file, wrapper_file, bridge,
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
        need(value.get("schema") == "cm2.round306c30c.cold-strace-audit.v1"
             and value.get("status") == EXPECTED_ANALYZER_STATUS
             and exact_int(value.get("exit_status"), "analyzer exit") == 0
             and exact_int(value.get("protected_path_mutations"), "analyzer mutation") == 0
             and exact_int(value.get("protected_fd_writes"), "analyzer FD writes") == 0
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
    need("PASS.lock" not in root.names(), "cannot append failure after PASS")
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


PREPARED_PASS = ".PASS.lock.prepared-v3"


def prepare_pass(root: HeldDir) -> None:
    names = set(root.names())
    need("failure_receipt.json" not in names and "FAILED.lock" not in names
         and "PASS.lock" not in names and PREPARED_PASS not in names,
         "PASS-after-failure/preexisting PASS forbidden")
    # The bytes and inode are fully written, reopened and verified while still
    # under a non-authoritative name.  The final no-replace rename is deferred.
    root.write_once(PREPARED_PASS, PASS_BYTES)


def commit_pass_last(root: HeldDir) -> None:
    names = set(root.names())
    need(PREPARED_PASS in names and "PASS.lock" not in names
         and "failure_receipt.json" not in names and "FAILED.lock" not in names,
         "exact prepared PASS commit state")
    raw, state = root.open_regular(PREPARED_PASS, 128)
    need(raw == PASS_BYTES and state["nlink"] == 1, "prepared PASS exact bytes/inode")
    libc = ctypes.CDLL(None, use_errno=True)
    renameat2 = libc.renameat2
    renameat2.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int,
                          ctypes.c_char_p, ctypes.c_uint]
    renameat2.restype = ctypes.c_int
    result = renameat2(
        root.fd, PREPARED_PASS.encode("ascii"), root.fd, b"PASS.lock", 1,
    )  # RENAME_NOREPLACE
    if result != 0:
        number = ctypes.get_errno()
        raise OSError(number, os.strerror(number))
    # Parent durability is part of the final publication; no check or write is
    # permitted after this fsync in successful run mode.
    os.fsync(root.fd)


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
    unit: str, maximum_wait: int,
) -> None:
    raw_bridge = Path(os.path.abspath(os.fspath(bridge_path)))
    need(raw_bridge.parent == AUDIT
         and raw_bridge.name.startswith("c30c-postreceipt-v3-p1-bridge-v3-")
         and "bridge-v1" not in raw_bridge.name and "bridge-v2" not in raw_bridge.name,
         "fresh bridge-v3 audit namespace")
    bridge = HeldDir(raw_bridge, "formal bridge root", fresh=True)
    anchor_file = HeldFile(anchor_path, "launch anchor", 8 << 20)
    pinset_file = HeldFile(pinset_path, "launch pinset", 16 << 20)
    self_file = HeldFile(WATCHER, "current __file__ watcher", 8 << 20)
    wrapper_file = HeldFile(WRAPPER, "process wrapper", 8 << 20)
    runtime = RuntimeAuthority()
    bridge_fragment: HeldFile | None = None
    transaction_fragment: HeldFile | None = None
    stages: list[HeldDir] = []
    try:
        need(Path(__file__).is_absolute()
             and Path(__file__).lstat().st_ino == self_file.initial.st_ino,
             "current __file__ exact held identity")
        anchor = parse_anchor(anchor_file)
        need(pinset_file.sha256 == anchor["pinset_sha256"],
             "anchor-bound pinset SHA without ExecStart self-cycle")
        need(anchor["bridge_service"]["Id"] == unit, "literal bridge unit")
        bridge_fragment = HeldFile(
            Path(anchor["bridge_service"]["FragmentPath"]), "bridge fragment", 1 << 20,
        )
        transaction_fragment = HeldFile(
            TRANSACTION_FRAGMENT, "transaction fragment", 1 << 20,
        )
        observations = verify_launch_materials(
            anchor_file, pinset_file, self_file, wrapper_file, bridge_fragment,
            transaction_fragment, runtime, anchor, bridge,
        )

        def reverify() -> dict[str, dict[str, Any]]:
            return verify_launch_materials(
                anchor_file, pinset_file, self_file, wrapper_file, bridge_fragment,
                transaction_fragment, runtime, anchor, bridge,
            )

        bridge_pre = recursive_snapshot(bridge)
        bridge.write_json("root_pre_recursive_snapshot.json", bridge_pre)
        verify_snapshot_extension(
            bridge_pre, recursive_snapshot(bridge), "root_pre_recursive_snapshot.json",
        )
        bridge_service = validate_service(
            runtime, anchor["bridge_service"], anchor["bridge_service"]["ExecStart"],
            bridge_fragment, "bridge-running",
        )
        bridge.write_json("bridge_running_service_attestation.json", bridge_service)
        preflight = closed({
            "schema": "cm2.round306c30c.postreceipt-bridge-v3-preflight.v1",
            "status": "PASS_DIRECT_PYTHON_HELD_DIRFD_AND_EXACT_PINS_ZERO_CREDIT",
            "anchor_sha256": anchor_file.sha256, "anchor_stat9": stat9(anchor_file.initial),
            "pinset_sha256": pinset_file.sha256, "pinset_stat9": stat9(pinset_file.initial),
            "watcher_sha256": self_file.sha256, "watcher_stat9": stat9(self_file.initial),
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
            "schema": "cm2.round306c30c.bridge-v3-dual-summary.v1",
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
            "prepared_pass_name": PREPARED_PASS,
            "pass_commit_method": "renameat2_RENAME_NOREPLACE_then_parent_fsync",
            "formal_credit": 0, "source_W_formal_remainder": 80,
            "source_W_transition_authorized": False,
            "publication_authorized": False, "terminal_replay_completed": False,
            "CM2": "NO-GO_FOR_CLAIM",
        })
        bridge.write_json("terminal_boundary.json", boundary)
        success_stdout = closed({
            "schema": "cm2.round306c30c.bridge-v3-service-stdout.v1",
            "status": "PASS_SERVICE_STDOUT_PREPARED_BEFORE_PASS_ZERO_CREDIT",
            "boundary_object_sha256": boundary["object_sha256"],
            "formal_credit": 0, "source_W_formal_remainder": 80,
            "source_W_transition_authorized": False,
            "publication_authorized": False, "terminal_replay_completed": False,
            "CM2": "NO-GO_FOR_CLAIM",
        })
        bridge.write_json("service_stdout.json", success_stdout)
        prepare_pass(bridge)
        final_tree = recursive_snapshot(bridge)
        bridge.write_json("root_final_recursive_snapshot.json", final_tree)
        verify_snapshot_extension(
            final_tree, recursive_snapshot(bridge), "root_final_recursive_snapshot.json",
        )
        # Every fallible closure occurs before the no-replace PASS publication.
        reverify(); runtime.verify(); bridge.verify()
        need("FAILED.lock" not in bridge.names() and "failure_receipt.json" not in bridge.names(),
             "no failure before PASS")
        commit_pass_last(bridge)
        return
    finally:
        for stage in stages:
            try: stage.close()
            except OSError: pass
        if transaction_fragment is not None: transaction_fragment.close()
        if bridge_fragment is not None: bridge_fragment.close()
        runtime.close(); wrapper_file.close(); self_file.close()
        pinset_file.close(); anchor_file.close(); bridge.close()


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


def self_test() -> dict[str, Any]:
    attacks: dict[str, str] = {}
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
        attacks["pass_after_failure"] = rejected(
            lambda: prepare_pass(failure_root), "PASS after failure",
        )
        need(failure_root.open_regular("FAILED.lock", 128)[0] == FAILED_BYTES,
             "FAILED always durable after preexisting failure")
        failure_root.close()

        old_anchor = root_path / "bridge-v1-anchor.json"
        write_fixture(old_anchor, canonical(closed({"schema": "old-v1"})) + b"\n")
        old_held = HeldFile(old_anchor, "old v1 anchor")
        attacks["old_v1_anchor"] = rejected(lambda: parse_anchor(old_held), "old v1")
        old_held.close()

        pass_path = root_path / "pass-positive"; pass_path.mkdir(mode=0o700)
        pass_root = HeldDir(pass_path, "positive PASS commit", fresh=True)
        prepare_pass(pass_root); commit_pass_last(pass_root)
        need(pass_root.names() == ["PASS.lock"]
             and pass_root.open_regular("PASS.lock", 128)[0] == PASS_BYTES,
             "renameat2 no-replace PASS commit selftest")
        pass_root.close()

    need(set(attacks) == {
        "bad_bus_real_route", "anchor_same_byte_inode_substitution",
        "pinset_same_byte_inode_substitution", "hardlink_input", "root_rename",
        "fragment_same_byte_inode_substitution", "preflight_bool_int_tamper",
        "inner_pid_substitution", "gnu_time_command_substitution",
        "output_symlink", "pass_after_failure", "old_v1_anchor",
    }, "exact 12 negative fixture inventory")
    return closed({
        "schema": "cm2.round306c30c.postreceipt-bridge-v3-selftest.v1",
        "status": "PASS_WRAPPER_AND_12_PRODUCTION_NEGATIVE_FIXTURES_ZERO_CREDIT",
        "production_preflight_byte_replay": True,
        "renameat2_noreplace_pass_commit": True,
        "negative_fixture_count": len(attacks), "negative_fixtures": attacks,
        "formal_execution_authorized": False,
        "formal_credit": 0, "source_W_formal_remainder": 80,
        "source_W_transition_authorized": False,
        "publication_authorized": False, "terminal_replay_completed": False,
        "CM2": "NO-GO_FOR_CLAIM",
    })


def main() -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--self-test", action="store_true")
    modes.add_argument("--run", action="store_true")
    parser.add_argument("--bridge-dir", type=Path)
    parser.add_argument("--pinset", type=Path)
    parser.add_argument("--anchor", type=Path)
    parser.add_argument("--unit")
    parser.add_argument("--maximum-wait-seconds", type=int, default=7 * 24 * 3600)
    arguments = parser.parse_args()
    try:
        if arguments.self_test:
            need(all(value is None for value in (
                arguments.bridge_dir, arguments.pinset,
                arguments.anchor, arguments.unit,
            )), "selftest has no formal launch material")
            print(canonical(self_test()).decode("ascii"))
            return 0
        need(arguments.bridge_dir is not None and arguments.pinset is not None
             and arguments.anchor is not None and type(arguments.unit) is str,
             "complete direct-Python run material")
        run_bridge(
            arguments.bridge_dir, arguments.pinset, arguments.anchor,
            arguments.unit, arguments.maximum_wait_seconds,
        )
        # Formal success is intentionally silent: service_stdout.json was
        # durably published before PASS, and PASS was the final write.
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


if __name__ == "__main__":
    raise SystemExit(main())
