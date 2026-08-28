#!/usr/bin/env python3
"""Append-only C30c v3 postreceipt bridge v2.

This program is a zero-credit bridge only.  It validates the completed C30c
v3 transaction and its exact systemd authority, performs fresh dual-seed
independent checks and a retained full-trace cold replay, and emits a terminal
*boundary* which explicitly does not authorize publication or Source-W 80->78.

The formal path is intentionally launch-material driven: a canonical launch
anchor pins the launcher, this watcher, and a canonical full-stat pinset.  The
service ExecStart must pass the anchor hash as a literal argument.  This avoids
self-hash cycles while leaving a post-exit bridge service tuple for the later
publication finalizer to verify independently.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


sys.dont_write_bytecode = True

WORKSPACE = Path("/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572")
DELIVERABLES = WORKSPACE / "deliverables"
AUDIT = WORKSPACE / ".cm2-runtime/audit"
CONTROL = WORKSPACE / ".cm2-runtime/control"
RECEIPTS = WORKSPACE / ".cm2-runtime/receipts"

PREFIX = "cm2_round306c30c_source_w_full_delta_whole_origin_disposition"
TRANSACTION_NAME = "c30c-v5-toctou-robustness-rerun-20260808T0635Z-receipt-v3"
TRANSACTION_UNIT = "cm2-c30c-v3-20260808T0635Z.service"
TRANSACTION_INVOCATION_ID = "93e5141a642a4016bcbedf622282ca28"
TRANSACTION_FRAGMENT = Path(
    "/run/user/1000/systemd/transient/cm2-c30c-v3-20260808T0635Z.service"
)
TRANSACTION_LAUNCHER = (
    CONTROL / TRANSACTION_NAME / "launch.sh"
)
RUN = AUDIT / TRANSACTION_NAME
RECEIPT = RECEIPTS / TRANSACTION_NAME

WATCHER = DELIVERABLES / Path(__file__).name
LAUNCHER = DELIVERABLES / "cm2_round306c30c_postreceipt_v3_p1_bridge_launcher_v2.sh"
VALIDATOR = DELIVERABLES / "cm2_round306c30c_62_attack_run_receipt_validator_v3.py"
HARNESS = DELIVERABLES / (PREFIX + "_attack_harness.py")
VERIFIER = DELIVERABLES / (PREFIX + "_independent_verifier.py")
ANALYZER = DELIVERABLES / (PREFIX + "_cold_trace_analyzer.py")
PAIRING_GATE = DELIVERABLES / "cm2_round306c30c_cold_trace_unfinished_pairing_attack_gate.py"

PYTHON = WORKSPACE / ".cm2-runtime/python-flint-0.9.0/bin/python"
PYTHON_LINK_2 = WORKSPACE / ".cm2-runtime/python-flint-0.9.0/bin/python3"
SYSTEM_PYTHON_LINK = Path("/usr/bin/python3")
SYSTEM_PYTHON_REAL = Path("/usr/bin/python3.12")
TIME = Path("/usr/bin/time")
STRACE = Path("/usr/bin/strace")
ENV = Path("/usr/bin/env")
SYSTEMCTL = Path("/usr/bin/systemctl")

EXPECTED_RECEIPT_STATUS = (
    "PASS_COMPLETE_C30C_62_ATTACK_RUN_RECEIPT_V3__ZERO_FORMAL_CREDIT"
)
EXPECTED_VERIFIER_STATUS = (
    "PASS_INDEPENDENT_CANDIDATE_C30C__80_DELTA_H_CELLS__"
    "2_RESOLVED_MIXED__ZERO_FORMAL_CREDIT"
)
EXPECTED_ANALYZER_STATUS = "PASS_C30C_COLD_TRACE_ZERO_PROTECTED_MUTATION"
EXPECTED_PAIRING_STATUS = (
    "PASS_STRICT_PID_SYSCALL_PAIRING_AND_7_ATTACKS__ZERO_FORMAL_CREDIT"
)

UID = 1000
RUNTIME_DIR = Path("/run/user/1000")
BUS_SOCKET = RUNTIME_DIR / "bus"
CONTROL_BUS_ENV = {
    "HOME": "/nonexistent",
    "PATH": "/usr/bin:/bin",
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "XDG_RUNTIME_DIR": "/run/user/1000",
    "DBUS_SESSION_BUS_ADDRESS": "unix:path=/run/user/1000/bus",
}
MATH_ENV_BASE = {
    "HOME": "/nonexistent",
    "PATH": "/usr/bin:/bin",
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "TZ": "UTC",
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
    PREFIX + "_result.json",
    PREFIX + "_whole_origin_ledger.jsonl.gz",
})
CANDIDATES = {
    "30630071": WORKSPACE / ".cm2-runtime/candidates/c30c-v4-seed-30630071",
    "30630929": WORKSPACE / ".cm2-runtime/candidates/c30c-v4-seed-30630929",
}

PINSET_SCHEMA = "cm2.round306c30c.postreceipt-bridge-v2-pinset.v1"
ANCHOR_SCHEMA = "cm2.round306c30c.postreceipt-bridge-v2-launch-anchor.v1"
PROCESS_SCHEMA = "cm2.round306c30c.postreceipt-bridge-v2-process.v1"
BOUNDARY_SCHEMA = "cm2.round306c30c.postreceipt-bridge-v2-terminal-boundary.v1"
PASS_LOCK = b"PASS_C30C_POSTRECEIPT_BRIDGE_V2_ZERO_CREDIT_BOUNDARY\n"
FAILED_LOCK = b"FAILED_C30C_POSTRECEIPT_BRIDGE_V2_FAIL_CLOSED\n"
HEX64 = re.compile(r"[0-9a-f]{64}")


class Blocked(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Blocked(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=True, allow_nan=False, sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def object_with_closure(body: Mapping[str, Any]) -> dict[str, Any]:
    output = dict(body)
    need("object_sha256" not in output, "fresh object closure")
    output["object_sha256"] = hashlib.sha256(canonical(output)).hexdigest()
    return output


def verify_object_closure(value: Mapping[str, Any], label: str) -> str:
    need(type(value) is dict and HEX64.fullmatch(str(value.get("object_sha256", "")))
         is not None, "object closure field:" + label)
    body = dict(value)
    observed = body.pop("object_sha256")
    expected = hashlib.sha256(canonical(body)).hexdigest()
    need(observed == expected, "object closure:" + label)
    return expected


def stat9(value: os.stat_result) -> dict[str, int]:
    return {
        "dev": value.st_dev,
        "ino": value.st_ino,
        "mode": value.st_mode,
        "nlink": value.st_nlink,
        "uid": value.st_uid,
        "gid": value.st_gid,
        "size": value.st_size,
        "mtime_ns": value.st_mtime_ns,
        "ctime_ns": value.st_ctime_ns,
    }


def identity(value: os.stat_result) -> tuple[int, ...]:
    item = stat9(value)
    return tuple(item[key] for key in (
        "dev", "ino", "mode", "nlink", "uid", "gid", "size",
        "mtime_ns", "ctime_ns",
    ))


def directory_identity(value: os.stat_result) -> tuple[int, ...]:
    """Identity fields that must survive an intentional child publication.

    A successful O_EXCL create is expected to change the parent directory's
    size and timestamps.  Its inode, ownership, mode, and link identity must
    nevertheless remain the same across the publication.
    """
    item = stat9(value)
    return tuple(item[key] for key in (
        "dev", "ino", "mode", "nlink", "uid", "gid",
    ))


def absolute_no_parent_symlink(path: Path, label: str) -> Path:
    absolute = Path(os.path.abspath(os.fspath(path)))
    need(absolute.is_absolute(), "absolute path:" + label)
    need(absolute.parent.resolve(strict=True) == absolute.parent,
         "no parent symlink:" + label)
    return absolute


def capture_regular(
    path: Path, label: str, maximum: int = 64 << 30,
) -> tuple[bytes, dict[str, int]]:
    absolute = absolute_no_parent_symlink(path, label)
    path_before = absolute.lstat()
    need(stat.S_ISREG(path_before.st_mode) and path_before.st_nlink == 1
         and 0 <= path_before.st_size <= maximum,
         "bounded regular singleton:" + label)
    descriptor = os.open(
        absolute, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        before = os.fstat(descriptor)
        chunks: list[bytes] = []
        remaining = before.st_size
        while remaining:
            block = os.read(descriptor, min(4 << 20, remaining))
            need(bool(block), "complete read:" + label)
            chunks.append(block)
            remaining -= len(block)
        need(os.read(descriptor, 1) == b"", "stable EOF:" + label)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    path_after = absolute.lstat()
    raw = b"".join(chunks)
    need(identity(path_before) == identity(before) == identity(after)
         == identity(path_after) and len(raw) == before.st_size,
         "single-FD stable capture:" + label)
    return raw, stat9(before)


def capture_symlink(path: Path, label: str) -> tuple[str, dict[str, int]]:
    absolute = absolute_no_parent_symlink(path, label)
    before = absolute.lstat()
    need(stat.S_ISLNK(before.st_mode) and before.st_nlink == 1,
         "singleton symlink:" + label)
    target = os.readlink(absolute)
    after = absolute.lstat()
    need(identity(before) == identity(after), "stable symlink:" + label)
    return target, stat9(before)


def capture_directory(
    path: Path, label: str,
) -> tuple[list[str], dict[str, int]]:
    absolute = absolute_no_parent_symlink(path, label)
    before_path = absolute.lstat()
    need(stat.S_ISDIR(before_path.st_mode) and not stat.S_ISLNK(before_path.st_mode),
         "real directory:" + label)
    descriptor = os.open(
        absolute, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC
        | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        before = os.fstat(descriptor)
        names = sorted(os.listdir(descriptor))
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    after_path = absolute.lstat()
    need(identity(before_path) == identity(before) == identity(after)
         == identity(after_path), "stable directory inventory:" + label)
    return names, stat9(before)


def sha256_file(path: Path, maximum: int = 64 << 30) -> str:
    return hashlib.sha256(capture_regular(path, os.fspath(path), maximum)[0]).hexdigest()


def strict_object_raw(raw: bytes, label: str) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            need(type(key) is str and key not in output, "unique key:" + label)
            output[key] = value
        return output
    try:
        value = json.loads(
            raw.decode("ascii"), object_pairs_hook=unique,
            parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
            parse_float=lambda token: (_ for _ in ()).throw(ValueError(token)),
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise Blocked("strict JSON:" + label) from error
    need(type(value) is dict and raw in {canonical(value), canonical(value) + b"\n"},
         "canonical JSON:" + label)
    return value


def strict_object_file(path: Path, label: str, maximum: int = 16 << 20) -> dict[str, Any]:
    return strict_object_raw(capture_regular(path, label, maximum)[0], label)


def fsync_directory(path: Path) -> None:
    descriptor = os.open(
        path, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC
        | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def durable_write_once(path: Path, raw: bytes, mode: int = 0o400) -> dict[str, int]:
    parent = absolute_no_parent_symlink(path.parent, "write parent:" + path.name)
    need(parent.is_dir() and not parent.is_symlink(), "write parent directory:" + path.name)
    need(path.parent == parent and path.name not in {"", ".", ".."},
         "direct child durable output")
    parent_fd = os.open(
        parent, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC
        | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        parent_before = os.fstat(parent_fd)
        descriptor = os.open(
            path.name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC
            | getattr(os, "O_NOFOLLOW", 0), mode, dir_fd=parent_fd,
        )
        try:
            offset = 0
            while offset < len(raw):
                written = os.write(descriptor, raw[offset:])
                need(written > 0, "write-all:" + path.name)
                offset += written
            os.fsync(descriptor)
            written_state = os.fstat(descriptor)
        finally:
            os.close(descriptor)
        reopen = os.open(
            path.name, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
            dir_fd=parent_fd,
        )
        try:
            reopen_before = os.fstat(reopen)
            chunks: list[bytes] = []
            while block := os.read(reopen, 1 << 20):
                chunks.append(block)
            reopen_after = os.fstat(reopen)
        finally:
            os.close(reopen)
        need(b"".join(chunks) == raw
             and identity(written_state) == identity(reopen_before)
             == identity(reopen_after),
             "same-dirfd reopen byte/stat verification:" + path.name)
        os.fsync(parent_fd)
        parent_after = os.fstat(parent_fd)
    finally:
        os.close(parent_fd)
    need(directory_identity(parent_before) == directory_identity(parent_after),
         "parent directory identity stable across durable publication:"
         + path.name)
    return stat9(written_state)


def durable_json_once(path: Path, value: Mapping[str, Any]) -> dict[str, int]:
    return durable_write_once(path, canonical(dict(value)) + b"\n")


def exact_members(directory: Path, expected: Iterable[str], label: str) -> None:
    names, _ = capture_directory(directory, label)
    need(names == sorted(set(expected)), "exact inventory:" + label)


def verify_control_bus_environment(environment: Mapping[str, str]) -> dict[str, Any]:
    need(os.getuid() == UID and os.geteuid() == UID, "exact control uid")
    need(dict(environment) == CONTROL_BUS_ENV, "exact CONTROL_BUS_ENV")
    runtime_before = RUNTIME_DIR.lstat()
    need(stat.S_ISDIR(runtime_before.st_mode) and not stat.S_ISLNK(runtime_before.st_mode)
         and runtime_before.st_uid == UID, "owned runtime directory")
    socket_before = BUS_SOCKET.lstat()
    need(stat.S_ISSOCK(socket_before.st_mode) and not stat.S_ISLNK(socket_before.st_mode)
         and socket_before.st_uid == UID, "owned user-bus socket")
    runtime_after = RUNTIME_DIR.lstat()
    socket_after = BUS_SOCKET.lstat()
    need(identity(runtime_before) == identity(runtime_after)
         and identity(socket_before) == identity(socket_after),
         "stable control bus authority")
    return {
        "uid": UID,
        "runtime_dir": os.fspath(RUNTIME_DIR),
        "runtime_stat9": stat9(runtime_before),
        "bus_socket": os.fspath(BUS_SOCKET),
        "bus_socket_stat9": stat9(socket_before),
        "control_env": dict(environment),
    }


def pin_member_observation(member: Mapping[str, Any]) -> dict[str, Any]:
    need(type(member) is dict and set(member) >= {"path", "kind", "stat9"},
         "pin member shape")
    path = Path(str(member["path"]))
    need(path.is_absolute(), "absolute pin member")
    kind = member["kind"]
    if kind == "regular":
        need(set(member) == {"path", "kind", "sha256", "stat9"}
             and HEX64.fullmatch(str(member["sha256"])) is not None,
             "regular pin shape")
        raw, observed_stat = capture_regular(path, "pin:" + os.fspath(path))
        observed = {
            "path": os.fspath(path), "kind": "regular",
            "sha256": hashlib.sha256(raw).hexdigest(), "stat9": observed_stat,
        }
    elif kind == "symlink":
        need(set(member) == {"path", "kind", "link_target", "stat9"},
             "symlink pin shape")
        target, observed_stat = capture_symlink(path, "pin:" + os.fspath(path))
        observed = {
            "path": os.fspath(path), "kind": "symlink",
            "link_target": target, "stat9": observed_stat,
        }
    elif kind == "directory":
        need(set(member) == {"path", "kind", "inventory", "stat9"}
             and type(member["inventory"]) is list,
             "directory pin shape")
        inventory, observed_stat = capture_directory(path, "pin:" + os.fspath(path))
        observed = {
            "path": os.fspath(path), "kind": "directory",
            "inventory": inventory, "stat9": observed_stat,
        }
    else:
        raise Blocked("unknown pin kind")
    need(observed == dict(member), "pinned member current byte/stat identity:" + os.fspath(path))
    return observed


def required_pin_paths() -> set[str]:
    paths = {
        WATCHER, LAUNCHER, VALIDATOR, HARNESS, VERIFIER, ANALYZER, PAIRING_GATE,
        PYTHON, PYTHON_LINK_2, SYSTEM_PYTHON_LINK, SYSTEM_PYTHON_REAL,
        TIME, STRACE, ENV, SYSTEMCTL,
        TRANSACTION_LAUNCHER, CONTROL / TRANSACTION_NAME / "pins.sha256",
        RUN / "command.txt", RUN / "provenance.json", RUN / "run.sh",
    }
    for candidate in CANDIDATES.values():
        paths.add(candidate)
        paths.update(candidate / name for name in CANDIDATE_FILES)
    return {os.fspath(path) for path in paths}


def verify_python_chain(members: Mapping[str, Mapping[str, Any]]) -> None:
    expected = {
        os.fspath(PYTHON): "python3",
        os.fspath(PYTHON_LINK_2): "/usr/bin/python3",
        os.fspath(SYSTEM_PYTHON_LINK): "python3.12",
    }
    for path, target in expected.items():
        item = members.get(path)
        need(type(item) is dict and item.get("kind") == "symlink"
             and item.get("link_target") == target,
             "exact Python symlink chain:" + path)
    final = members.get(os.fspath(SYSTEM_PYTHON_REAL))
    need(type(final) is dict and final.get("kind") == "regular",
         "regular final Python target")
    need(PYTHON.resolve(strict=True) == SYSTEM_PYTHON_REAL,
         "Python symlink chain final target")


def load_pinset(path: Path, expected_sha256: str) -> tuple[dict[str, Any], dict[str, Any]]:
    need(HEX64.fullmatch(expected_sha256) is not None, "pinset CLI SHA")
    raw, _ = capture_regular(path, "pinset", 8 << 20)
    need(hashlib.sha256(raw).hexdigest() == expected_sha256, "exact pinset file SHA")
    value = strict_object_raw(raw, "pinset")
    verify_object_closure(value, "pinset")
    need(value.get("schema") == PINSET_SCHEMA
         and value.get("status") == "FROZEN_ZERO_CREDIT_PINSET"
         and value.get("formal_credit") == 0
         and value.get("source_W_formal_remainder") == 80
         and value.get("publication_authorized") is False,
         "pinset zero-credit contract")
    rows = value.get("members")
    need(type(rows) is list and len(rows) == len({str(row.get("path")) for row in rows
                                                 if type(row) is dict}),
         "unique pin members")
    observations: dict[str, Any] = {}
    for row in rows:
        observed = pin_member_observation(row)
        observations[observed["path"]] = observed
    need(set(observations) >= required_pin_paths(), "complete required pin role set")
    verify_python_chain(observations)
    return value, observations


def load_anchor(
    path: Path, expected_sha256: str, pinset_path: Path,
    launcher_path: Path, bridge_dir: Path,
) -> dict[str, Any]:
    need(HEX64.fullmatch(expected_sha256) is not None, "anchor CLI SHA")
    raw, _ = capture_regular(path, "launch anchor", 4 << 20)
    need(hashlib.sha256(raw).hexdigest() == expected_sha256, "exact launch anchor SHA")
    value = strict_object_raw(raw, "launch anchor")
    verify_object_closure(value, "launch anchor")
    need(value.get("schema") == ANCHOR_SCHEMA
         and value.get("status") == "FROZEN_ZERO_CREDIT_LAUNCH_ANCHOR"
         and value.get("watcher_path") == os.fspath(WATCHER)
         and value.get("watcher_sha256") == sha256_file(WATCHER, 8 << 20)
         and value.get("launcher_path") == os.fspath(launcher_path)
         and value.get("launcher_sha256") == sha256_file(launcher_path, 1 << 20)
         and value.get("pinset_path") == os.fspath(pinset_path)
         and value.get("pinset_sha256") == sha256_file(pinset_path, 8 << 20)
         and value.get("bridge_dir") == os.fspath(bridge_dir)
         and value.get("transaction_unit") == TRANSACTION_UNIT
         and value.get("transaction_invocation_id") == TRANSACTION_INVOCATION_ID
         and value.get("transaction_fragment") == os.fspath(TRANSACTION_FRAGMENT)
         and value.get("transaction_execstart") == os.fspath(TRANSACTION_LAUNCHER)
         and value.get("formal_credit") == 0
         and value.get("source_W_formal_remainder") == 80
         and value.get("publication_authorized") is False,
         "launch anchor exact contract")
    return value


def parse_systemctl_fields(raw: bytes) -> dict[str, str]:
    try:
        lines = raw.decode("ascii").splitlines()
    except UnicodeDecodeError as error:
        raise Blocked("systemctl ASCII") from error
    fields: dict[str, str] = {}
    for line in lines:
        key, separator, value = line.partition("=")
        need(separator == "=" and key and key not in fields, "unique systemctl field")
        fields[key] = value
    return fields


def validate_execstart(value: str, expected: Path) -> dict[str, Any]:
    match = re.fullmatch(
        r"\{ path=([^ ;]+) ; argv\[\]=([^ ;]+) ; ignore_errors=no ; "
        r"start_time=\[(.*)\] ; stop_time=\[(.*)\] ; pid=([0-9]+) ; "
        r"code=([^ ;]+) ; status=([^ }]+) \}", value,
    )
    need(match is not None, "strict ExecStart record")
    path, argv, start, stop, pid, code, status_text = match.groups()
    need(path == argv == os.fspath(expected), "exact ExecStart path/argv")
    need(bool(start) and bool(stop) and int(pid) > 0,
         "complete ExecStart runtime fields")
    need(code == "exited" and status_text == "0/0", "clean ExecStart result")
    return {
        "path": path, "argv": [argv], "ignore_errors": False,
        "start_time": start, "stop_time": stop, "pid": int(pid),
        "code": code, "status": status_text,
    }


def query_transaction_service() -> dict[str, Any]:
    bus = verify_control_bus_environment(CONTROL_BUS_ENV)
    properties = (
        "Id", "LoadState", "ActiveState", "SubState", "Result",
        "ExecMainCode", "ExecMainStatus", "InvocationID", "MainPID",
        "FragmentPath", "ExecStart", "Type", "RemainAfterExit", "StandardError",
    )
    command = [os.fspath(SYSTEMCTL), "--user", "show", TRANSACTION_UNIT]
    for item in properties:
        command.extend(["-p", item])
    completed = subprocess.run(
        command, cwd=WORKSPACE, env=CONTROL_BUS_ENV,
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        check=False,
    )
    need(completed.returncode == 0 and completed.stderr == b"",
         "clean systemctl transaction query")
    bus_after = verify_control_bus_environment(CONTROL_BUS_ENV)
    need(bus == bus_after, "control bus SHA/full9stat stable across systemctl query")
    fields = parse_systemctl_fields(completed.stdout)
    need(set(fields) == set(properties), "exact transaction service property set")
    expected = {
        "Id": TRANSACTION_UNIT,
        "LoadState": "loaded",
        "ActiveState": "active",
        "SubState": "exited",
        "Result": "success",
        "ExecMainCode": "exited",
        "ExecMainStatus": "0",
        "InvocationID": TRANSACTION_INVOCATION_ID,
        "MainPID": "0",
        "FragmentPath": os.fspath(TRANSACTION_FRAGMENT),
        "Type": "oneshot",
        "RemainAfterExit": "yes",
        "StandardError": "journal",
    }
    for key, value in expected.items():
        need(fields.get(key) == value, "transaction service authority:" + key)
    execstart = validate_execstart(fields["ExecStart"], TRANSACTION_LAUNCHER)
    fragment_raw, fragment_stat = capture_regular(
        TRANSACTION_FRAGMENT, "transaction transient fragment", 1 << 20,
    )
    return object_with_closure({
        "schema": "cm2.round306c30c.postreceipt-bridge-v2-transaction-service.v1",
        "status": "PASS_EXACT_TRANSACTION_SERVICE_CLEAN_EXIT",
        "properties": fields,
        "execstart": execstart,
        "fragment_sha256": hashlib.sha256(fragment_raw).hexdigest(),
        "fragment_stat9": fragment_stat,
        "systemctl_stdout_sha256": hashlib.sha256(completed.stdout).hexdigest(),
        "control_bus": bus,
        "formal_credit": 0,
        "source_W_formal_remainder": 80,
        "publication_authorized": False,
    })


def service_failed() -> bool:
    bus_before = verify_control_bus_environment(CONTROL_BUS_ENV)
    completed = subprocess.run(
        [os.fspath(SYSTEMCTL), "--user", "is-failed", TRANSACTION_UNIT],
        cwd=WORKSPACE, env=CONTROL_BUS_ENV, stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    need(completed.stderr == b"", "is-failed stderr empty")
    need(bus_before == verify_control_bus_environment(CONTROL_BUS_ENV),
         "control bus stable across is-failed query")
    return completed.returncode == 0


def wait_for_transaction(maximum_seconds: int) -> dict[str, Any]:
    deadline = time.monotonic() + maximum_seconds
    while time.monotonic() < deadline:
        if (RECEIPT / "transaction-end-utc.txt").is_file():
            for _ in range(120):
                try:
                    return query_transaction_service()
                except Blocked:
                    if service_failed():
                        raise Blocked("transaction receipt exists but service failed")
                    time.sleep(5)
            raise Blocked("transaction receipt exists but service did not settle cleanly")
        need(not service_failed(), "transaction service failed before receipt")
        time.sleep(30)
    raise Blocked("timeout waiting for exact v3 transaction")


def snapshot_path(path: Path) -> dict[str, Any]:
    state = path.lstat()
    if stat.S_ISREG(state.st_mode):
        raw, observed = capture_regular(path, "snapshot:" + os.fspath(path))
        return {"path": os.fspath(path), "kind": "regular",
                "sha256": hashlib.sha256(raw).hexdigest(), "stat9": observed}
    if stat.S_ISLNK(state.st_mode):
        target, observed = capture_symlink(path, "snapshot:" + os.fspath(path))
        return {"path": os.fspath(path), "kind": "symlink",
                "link_target": target, "stat9": observed}
    if stat.S_ISDIR(state.st_mode):
        inventory, observed = capture_directory(path, "snapshot:" + os.fspath(path))
        return {"path": os.fspath(path), "kind": "directory",
                "inventory": inventory, "stat9": observed}
    raise Blocked("unsupported snapshot type:" + os.fspath(path))


def snapshot(paths: Sequence[Path]) -> dict[str, Any]:
    unique = sorted({Path(os.path.abspath(os.fspath(path))) for path in paths},
                    key=os.fspath)
    return object_with_closure({
        "schema": "cm2.round306c30c.postreceipt-bridge-v2-snapshot.v1",
        "members": [snapshot_path(path) for path in unique],
    })


def parse_gnu_time(raw: bytes) -> dict[str, Any]:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise Blocked("GNU time UTF-8") from error
    exits = re.findall(r"(?m)^\s*Exit status:\s*([0-9]+)\s*$", text)
    signals = re.findall(
        r"(?m)^\s*Command terminated by signal\s+([0-9]+)\s*$", text,
    )
    commands = re.findall(r'(?m)^\s*Command being timed:\s*"([^"\n]*)"\s*$', text)
    need(len(exits) == 1 and len(commands) == 1 and len(signals) <= 1,
         "complete GNU time receipt")
    return {
        "exit_status": int(exits[0]),
        "signal": None if not signals else int(signals[0]),
        "command_display": commands[0],
    }


def create_directory_once(path: Path) -> None:
    parent = absolute_no_parent_symlink(path.parent, "mkdir parent")
    need(path.parent == parent and path.name not in {"", ".", ".."},
         "direct child durable directory")
    parent_fd = os.open(
        parent, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC
        | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        parent_before = os.fstat(parent_fd)
        os.mkdir(path.name, 0o700, dir_fd=parent_fd)
        os.fsync(parent_fd)
        parent_after = os.fstat(parent_fd)
    finally:
        os.close(parent_fd)
    need(directory_identity(parent_before) == directory_identity(parent_after),
         "parent directory identity stable across mkdir:" + path.name)
    names, state = capture_directory(path, "fresh directory")
    need(names == [] and stat.S_ISDIR(state["mode"]), "fresh empty directory")
    fsync_directory(parent)


def fsync_existing_file(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "fsync regular output:" + path.name)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def run_process_stage(
    stage_dir: Path,
    inner_argv: Sequence[str],
    input_paths: Sequence[Path],
    expected_status: str,
    extra_outputs: Sequence[str] = (),
) -> tuple[dict[str, Any], bytes]:
    create_directory_once(stage_dir)
    stdout_path = stage_dir / "stdout.json"
    stderr_path = stage_dir / "stderr.log"
    time_path = stage_dir / "time.txt"
    process_path = stage_dir / "process_receipt.json"
    pre_path = stage_dir / "pre.snapshot.json"
    post_path = stage_dir / "post.snapshot.json"
    spec_path = stage_dir / "spec.json"
    for name in ("stdout.json", "stderr.log", "time.txt", "process_receipt.json",
                 "pre.snapshot.json", "post.snapshot.json", "spec.json", *extra_outputs):
        need(not (stage_dir / name).exists(), "fresh stage output:" + name)

    pre = snapshot(input_paths)
    spec = object_with_closure({
        "schema": "cm2.round306c30c.postreceipt-bridge-v2-process-spec.v1",
        "inner_argv": list(inner_argv),
        "wrapper_argv": [os.fspath(TIME), "--verbose",
                         "--output=" + os.fspath(time_path), "--", *inner_argv],
        "wrapper_env": dict(MATH_ENV_BASE),
        "expected_status": expected_status,
        "extra_outputs": list(extra_outputs),
        "formal_credit": 0,
        "source_W_formal_remainder": 80,
        "publication_authorized": False,
    })
    durable_json_once(spec_path, spec)
    durable_json_once(pre_path, pre)
    stdout_fd = os.open(stdout_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC,
                        0o400)
    stderr_fd = os.open(stderr_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC,
                        0o400)
    command = spec["wrapper_argv"]
    started_ns = time.time_ns()
    try:
        process = subprocess.Popen(
            command, cwd=WORKSPACE, env=MATH_ENV_BASE, stdin=subprocess.DEVNULL,
            stdout=stdout_fd, stderr=stderr_fd, close_fds=True,
        )
        wrapper_pid = process.pid
        returncode = process.wait()
        os.fsync(stdout_fd)
        os.fsync(stderr_fd)
    finally:
        os.close(stdout_fd)
        os.close(stderr_fd)
    ended_ns = time.time_ns()
    fsync_existing_file(time_path)
    for name in extra_outputs:
        fsync_existing_file(stage_dir / name)
    fsync_directory(stage_dir)

    post = snapshot(input_paths)
    durable_json_once(post_path, post)
    stdout_raw, stdout_stat = capture_regular(stdout_path, "stage stdout", 64 << 20)
    stderr_raw, stderr_stat = capture_regular(stderr_path, "stage stderr", 64 << 20)
    time_raw, time_stat = capture_regular(time_path, "stage time", 8 << 20)
    timed = parse_gnu_time(time_raw)
    signal_number = -returncode if returncode < 0 else timed["signal"]
    value = strict_object_raw(stdout_raw, "stage stdout")
    need(returncode == 0 and timed["exit_status"] == 0 and signal_number is None,
         "numeric exit zero/no signal")
    need(stderr_raw == b"", "stage stderr empty")
    need(value.get("status") == expected_status, "exact stage status")
    need(value.get("formal_credit", 0) == 0,
         "stage cannot report nonzero formal credit")
    need(value.get("source_W_transition_authorized", False) is False,
         "stage cannot authorize Source-W transition")
    need(value.get("publication_authorized", False) is False,
         "stage cannot authorize publication")
    need(pre == post, "stage input pre/post SHA+full9stat identity")
    extras: dict[str, Any] = {}
    for name in extra_outputs:
        raw, state = capture_regular(stage_dir / name, "extra output:" + name, 512 << 20)
        extras[name] = {"sha256": hashlib.sha256(raw).hexdigest(),
                        "size": len(raw), "stat9": state}
    receipt = object_with_closure({
        "schema": PROCESS_SCHEMA,
        "status": "PASS_CLEAN_PROCESS_TRANSACTION__ZERO_FORMAL_CREDIT",
        "wrapper_pid": wrapper_pid,
        "inner_argv": list(inner_argv),
        "wrapper_argv": list(command),
        "wrapper_env": dict(MATH_ENV_BASE),
        "started_ns": started_ns,
        "ended_ns": ended_ns,
        "numeric_exit_code": 0,
        "signal": None,
        "stderr_empty": True,
        "stdout_sha256": hashlib.sha256(stdout_raw).hexdigest(),
        "stdout_stat9": stdout_stat,
        "stderr_sha256": hashlib.sha256(stderr_raw).hexdigest(),
        "stderr_stat9": stderr_stat,
        "time_sha256": hashlib.sha256(time_raw).hexdigest(),
        "time_stat9": time_stat,
        "gnu_time": timed,
        "spec_sha256": sha256_file(spec_path, 4 << 20),
        "pre_snapshot_sha256": sha256_file(pre_path, 16 << 20),
        "post_snapshot_sha256": sha256_file(post_path, 16 << 20),
        "pre_post_identical": True,
        "extra_outputs": extras,
        "formal_credit": 0,
        "source_W_formal_remainder": 80,
        "publication_authorized": False,
    })
    durable_json_once(process_path, receipt)
    exact_members(stage_dir, {
        "stdout.json", "stderr.log", "time.txt", "process_receipt.json",
        "pre.snapshot.json", "post.snapshot.json", "spec.json", *extra_outputs,
    }, "completed process stage")
    return receipt, stdout_raw


def transaction_inputs() -> list[Path]:
    return [RUN, RECEIPT, *(RUN / name for name in RUN_FILES),
            *(RECEIPT / name for name in RECEIPT_FILES), VALIDATOR]


def validate_transaction_boundary() -> tuple[dict[str, Any], bytes]:
    exact_members(RUN, RUN_FILES, "completed transaction run")
    exact_members(RECEIPT, RECEIPT_FILES, "completed transaction receipt")
    for name in ("preflight.exit", "transaction-run.exit", "receipt.exit"):
        need(capture_regular(RECEIPT / name, name, 32)[0] == b"0\n",
             "transaction numeric exit:" + name)
    for name in ("preflight.stderr", "receipt.stderr"):
        need(capture_regular(RECEIPT / name, name, 64 << 20)[0] == b"",
             "transaction empty stderr:" + name)
    need(capture_regular(RUN / "stderr.log", "run stderr", 64 << 20)[0] == b"",
         "harness stderr empty")
    need(capture_regular(RUN / "exit_code.txt", "run exit", 32)[0] == b"0\n",
         "harness numeric exit zero")
    need(capture_regular(RUN / "pre.sha256", "run pre sha", 4 << 20)[0]
         == capture_regular(RUN / "post.sha256", "run post sha", 4 << 20)[0],
         "transaction pre/post SHA identity")
    need(capture_regular(RUN / "pre.stat", "run pre stat", 4 << 20)[0]
         == capture_regular(RUN / "post.stat", "run post stat", 4 << 20)[0],
         "transaction pre/post stat identity")
    raw, _ = capture_regular(RECEIPT / "receipt.json", "transaction receipt", 8 << 20)
    value = strict_object_raw(raw, "transaction receipt")
    need(value.get("schema") == "cm2.round306c30c.attack-run-receipt-validation.v3"
         and value.get("status") == EXPECTED_RECEIPT_STATUS
         and value.get("run_directory") == TRANSACTION_NAME
         and value.get("attack_count") == 62
         and value.get("numeric_exit_code") == 0
         and value.get("signal") is None
         and value.get("pre_post_sha256_identical") is True
         and value.get("pre_post_stat_identical") is True
         and value.get("formal_credit") == 0
         and value.get("manifest_authorized") is False
         and value.get("source_W_formal_remainder") == 80
         and value.get("source_W_transition_authorized") is False
         and value.get("downstream_publication_authorized") is False,
         "exact transaction receipt conclusion")
    return value, raw


def env_inner(seed: str, program: Path, arguments: Sequence[str]) -> list[str]:
    environment = {**MATH_ENV_BASE, "PYTHONHASHSEED": seed}
    assignments = [key + "=" + environment[key] for key in sorted(environment)]
    return [os.fspath(ENV), "-i", *assignments, os.fspath(PYTHON), "-I", "-B",
            os.fspath(program), *arguments]


def verifier_inputs(candidate: Path, pinset_path: Path, anchor_path: Path) -> list[Path]:
    return [
        pinset_path, anchor_path, WATCHER, LAUNCHER, PYTHON, PYTHON_LINK_2,
        SYSTEM_PYTHON_LINK, SYSTEM_PYTHON_REAL, TIME, ENV, VERIFIER,
        candidate, *(candidate / name for name in CANDIDATE_FILES),
    ]


def run_bridge(
    bridge: Path, pinset_path: Path, anchor_path: Path,
    pinset_sha256: str, anchor_sha256: str, launcher: Path,
    maximum_wait_seconds: int,
) -> dict[str, Any]:
    need(bridge.parent == AUDIT and bridge.name.startswith("c30c-postreceipt-v3-p1-bridge-v2-"),
         "fixed append-only bridge namespace")
    exact_members(bridge, set(), "fresh bridge root")
    anchor = load_anchor(anchor_path, anchor_sha256, pinset_path, launcher, bridge)
    pinset, pins_before = load_pinset(pinset_path, pinset_sha256)
    need(anchor["pinset_sha256"] == pinset_sha256, "anchor/pinset file binding")
    need(anchor["pinset_object_sha256"] == pinset["object_sha256"],
         "anchor/pinset object binding")
    preflight = object_with_closure({
        "schema": "cm2.round306c30c.postreceipt-bridge-v2-preflight.v1",
        "status": "PASS_FROZEN_LAUNCH_AND_PINSET_PREFLIGHT__ZERO_FORMAL_CREDIT",
        "anchor_sha256": anchor_sha256,
        "pinset_sha256": pinset_sha256,
        "pinset_object_sha256": pinset["object_sha256"],
        "pinned_member_count": len(pins_before),
        "control_bus": verify_control_bus_environment(CONTROL_BUS_ENV),
        "formal_credit": 0,
        "source_W_formal_remainder": 80,
        "publication_authorized": False,
    })
    durable_json_once(bridge / "preflight.json", preflight)

    service_receipt = wait_for_transaction(maximum_wait_seconds)
    durable_json_once(bridge / "transaction_service_receipt.json", service_receipt)
    transaction, transaction_raw = validate_transaction_boundary()

    receipt_stage, replay_raw = run_process_stage(
        bridge / "receipt-validator-replay",
        [os.fspath(ENV), "-i", *(
            key + "=" + MATH_ENV_BASE[key] for key in sorted(MATH_ENV_BASE)
        ), os.fspath(SYSTEM_PYTHON_REAL), "-I", "-B", os.fspath(VALIDATOR),
         os.fspath(RUN)],
        transaction_inputs() + [SYSTEM_PYTHON_REAL, ENV, TIME],
        EXPECTED_RECEIPT_STATUS,
    )
    need(replay_raw == transaction_raw, "receipt validator byte replay identity")
    receipt_gate = object_with_closure({
        "schema": "cm2.round306c30c.postreceipt-bridge-v2-receipt-gate.v1",
        "status": "PASS_EXACT_TRANSACTION_RECEIPT_AND_SERVICE__ZERO_FORMAL_CREDIT",
        "transaction_receipt_sha256": hashlib.sha256(transaction_raw).hexdigest(),
        "transaction_service_receipt_sha256": sha256_file(
            bridge / "transaction_service_receipt.json", 8 << 20),
        "validator_process_receipt_sha256": sha256_file(
            bridge / "receipt-validator-replay/process_receipt.json", 8 << 20),
        "numeric_exit_code": transaction["numeric_exit_code"],
        "signal": transaction["signal"],
        "stderr_empty": True,
        "formal_credit": 0,
        "source_W_formal_remainder": 80,
        "publication_authorized": False,
    })
    durable_json_once(bridge / "receipt_gate.json", receipt_gate)

    dual_outputs: dict[str, bytes] = {}
    dual_receipts: dict[str, str] = {}
    for seed, candidate in CANDIDATES.items():
        receipt, raw = run_process_stage(
            bridge / ("dual-seed-" + seed),
            env_inner(seed, VERIFIER, [os.fspath(candidate)]),
            verifier_inputs(candidate, pinset_path, anchor_path),
            EXPECTED_VERIFIER_STATUS,
        )
        value = strict_object_raw(raw, "dual verifier:" + seed)
        need(value.get("formal_credit") == 0
             and value.get("manifest_authorized") is False
             and value.get("proposed_source_W_remaining_transition") == "80->78",
             "dual zero-credit conclusion:" + seed)
        dual_outputs[seed] = raw
        dual_receipts[seed] = receipt["object_sha256"]
    need(dual_outputs["30630071"] == dual_outputs["30630929"],
         "dual seed byte identity")
    dual_summary = object_with_closure({
        "schema": "cm2.round306c30c.postreceipt-bridge-v2-dual.v1",
        "status": "PASS_FRESH_DUAL_SEED_PROCESS_TRANSACTIONS__ZERO_FORMAL_CREDIT",
        "seeds": ["30630071", "30630929"],
        "process_object_sha256": dual_receipts,
        "stdout_sha256": hashlib.sha256(dual_outputs["30630071"]).hexdigest(),
        "formal_credit": 0,
        "source_W_formal_remainder": 80,
        "publication_authorized": False,
    })
    durable_json_once(bridge / "dual_summary.json", dual_summary)

    cold_dir = bridge / "cold-seed-30630071"
    cold_inner = [
        os.fspath(STRACE), "-f", "-yy", "-s", "4096", "-e", "trace=all",
        "-o", os.fspath(cold_dir / "trace.raw"),
        *env_inner("30630071", VERIFIER,
                   [os.fspath(CANDIDATES["30630071"])]),
    ]
    cold_receipt, cold_raw = run_process_stage(
        cold_dir, cold_inner,
        verifier_inputs(CANDIDATES["30630071"], pinset_path, anchor_path)
        + [STRACE],
        EXPECTED_VERIFIER_STATUS, extra_outputs=["trace.raw"],
    )
    need(cold_raw == dual_outputs["30630071"], "cold/dual verifier byte identity")
    trace = cold_dir / "trace.raw"
    analyzer_inputs = [
        trace, cold_dir / "stdout.json", cold_dir / "stderr.log",
        cold_dir / "time.txt", ANALYZER, PYTHON, PYTHON_LINK_2,
        SYSTEM_PYTHON_LINK, SYSTEM_PYTHON_REAL, ENV, TIME,
        CANDIDATES["30630071"],
        *(CANDIDATES["30630071"] / name for name in CANDIDATE_FILES),
    ]
    analyzer_receipt, analyzer_raw = run_process_stage(
        bridge / "cold-trace-analyzer",
        env_inner("30630071", ANALYZER, [
            "--trace", os.fspath(trace),
            "--stdout", os.fspath(cold_dir / "stdout.json"),
            "--stderr", os.fspath(cold_dir / "stderr.log"),
            "--time", os.fspath(cold_dir / "time.txt"),
            "--candidate-dir", os.fspath(CANDIDATES["30630071"]),
        ]),
        analyzer_inputs, EXPECTED_ANALYZER_STATUS,
    )
    pairing_receipt, pairing_raw = run_process_stage(
        bridge / "cold-pairing-gate",
        env_inner("30630071", PAIRING_GATE, []),
        [PAIRING_GATE, ANALYZER, PYTHON, PYTHON_LINK_2,
         SYSTEM_PYTHON_LINK, SYSTEM_PYTHON_REAL, ENV, TIME],
        EXPECTED_PAIRING_STATUS,
    )
    cold_summary = object_with_closure({
        "schema": "cm2.round306c30c.postreceipt-bridge-v2-cold.v1",
        "status": "PASS_FRESH_COLD_TRACE_PROCESS_TRANSACTIONS__ZERO_FORMAL_CREDIT",
        "cold_process_object_sha256": cold_receipt["object_sha256"],
        "analyzer_process_object_sha256": analyzer_receipt["object_sha256"],
        "pairing_process_object_sha256": pairing_receipt["object_sha256"],
        "trace_sha256": sha256_file(trace, 512 << 20),
        "analyzer_stdout_sha256": hashlib.sha256(analyzer_raw).hexdigest(),
        "pairing_stdout_sha256": hashlib.sha256(pairing_raw).hexdigest(),
        "formal_credit": 0,
        "source_W_formal_remainder": 80,
        "publication_authorized": False,
    })
    durable_json_once(bridge / "cold_summary.json", cold_summary)

    _pinset_after, pins_after = load_pinset(pinset_path, pinset_sha256)
    need(pins_before == pins_after, "full bridge pin SHA+full9stat stability")
    preterminal_members = {
        "preflight.json", "transaction_service_receipt.json",
        "receipt-validator-replay", "receipt_gate.json",
        "dual-seed-30630071", "dual-seed-30630929", "dual_summary.json",
        "cold-seed-30630071", "cold-trace-analyzer", "cold-pairing-gate",
        "cold_summary.json",
    }
    exact_members(bridge, preterminal_members, "preterminal bridge root")
    boundary = object_with_closure({
        "schema": BOUNDARY_SCHEMA,
        "status": "PASS_ZERO_CREDIT_POSTRECEIPT_BOUNDARY__PUBLICATION_NOT_AUTHORIZED",
        "anchor_sha256": anchor_sha256,
        "pinset_sha256": pinset_sha256,
        "transaction_unit": TRANSACTION_UNIT,
        "transaction_invocation_id": TRANSACTION_INVOCATION_ID,
        "transaction_service_receipt_sha256": sha256_file(
            bridge / "transaction_service_receipt.json", 8 << 20),
        "receipt_gate_sha256": sha256_file(bridge / "receipt_gate.json", 8 << 20),
        "dual_summary_sha256": sha256_file(bridge / "dual_summary.json", 8 << 20),
        "cold_summary_sha256": sha256_file(bridge / "cold_summary.json", 8 << 20),
        "bridge_service_post_exit_verification_required": True,
        "terminal_replay_completed": False,
        "formal_credit": 0,
        "source_W_formal_remainder": 80,
        "source_W_transition_authorized": False,
        "publication_authorized": False,
        "CM2": "NO-GO_FOR_CLAIM",
    })
    durable_json_once(bridge / "terminal_boundary.json", boundary)
    durable_write_once(bridge / "PASS.lock", PASS_LOCK)
    exact_members(bridge, preterminal_members | {"terminal_boundary.json", "PASS.lock"},
                  "completed zero-credit bridge root")
    return boundary


def fixture_member(path: Path) -> dict[str, Any]:
    state = path.lstat()
    if stat.S_ISREG(state.st_mode):
        raw, observed = capture_regular(path, "fixture")
        return {"path": os.fspath(path), "kind": "regular",
                "sha256": hashlib.sha256(raw).hexdigest(), "stat9": observed}
    if stat.S_ISLNK(state.st_mode):
        target, observed = capture_symlink(path, "fixture")
        return {"path": os.fspath(path), "kind": "symlink",
                "link_target": target, "stat9": observed}
    if stat.S_ISDIR(state.st_mode):
        inventory, observed = capture_directory(path, "fixture")
        return {"path": os.fspath(path), "kind": "directory",
                "inventory": inventory, "stat9": observed}
    raise Blocked("fixture type")


def rejected(callable_object: Any, expected_prefix: str) -> str:
    try:
        callable_object()
    except (Blocked, OSError, ValueError, TypeError, KeyError) as error:
        reason = str(error)
        need(reason.startswith(expected_prefix), "exact fixture rejection:" + reason)
        return reason
    raise Blocked("negative fixture accepted:" + expected_prefix)


def self_test() -> dict[str, Any]:
    bus = verify_control_bus_environment(CONTROL_BUS_ENV)
    control_probe = subprocess.run(
        [os.fspath(SYSTEMCTL), "--user", "show", TRANSACTION_UNIT, "-p", "Id"],
        cwd=WORKSPACE, env=CONTROL_BUS_ENV, stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    need(control_probe.returncode == 0 and control_probe.stderr == b""
         and control_probe.stdout == ("Id=" + TRANSACTION_UNIT + "\n").encode("ascii"),
         "positive user-bus control fixture")
    attacks: dict[str, str] = {}
    wrong_bus = dict(CONTROL_BUS_ENV)
    wrong_bus["DBUS_SESSION_BUS_ADDRESS"] = "unix:path=/run/user/1000/missing"
    attacks["wrong_bus_env"] = rejected(
        lambda: verify_control_bus_environment(wrong_bus), "exact CONTROL_BUS_ENV",
    )
    missing_bus = dict(CONTROL_BUS_ENV)
    missing_bus.pop("XDG_RUNTIME_DIR")
    attacks["missing_bus_env"] = rejected(
        lambda: verify_control_bus_environment(missing_bus), "exact CONTROL_BUS_ENV",
    )

    clean_fields = {
        "Id": TRANSACTION_UNIT, "LoadState": "loaded", "ActiveState": "active",
        "SubState": "exited", "Result": "success", "ExecMainCode": "exited",
        "ExecMainStatus": "0", "InvocationID": TRANSACTION_INVOCATION_ID,
        "MainPID": "0", "FragmentPath": os.fspath(TRANSACTION_FRAGMENT),
        "Type": "oneshot", "RemainAfterExit": "yes", "StandardError": "journal",
    }
    def pure_service_fixture(fields: Mapping[str, str], execstart: str) -> None:
        expected = dict(clean_fields)
        for key, value in expected.items():
            need(fields.get(key) == value, "transaction service authority:" + key)
        validate_execstart(execstart, TRANSACTION_LAUNCHER)
    clean_exec = (
        "{ path=" + os.fspath(TRANSACTION_LAUNCHER)
        + " ; argv[]=" + os.fspath(TRANSACTION_LAUNCHER)
        + " ; ignore_errors=no ; start_time=[start] ; stop_time=[stop] ; "
        "pid=1 ; code=exited ; status=0/0 }"
    )
    pure_service_fixture(clean_fields, clean_exec)
    changed = dict(clean_fields); changed["InvocationID"] = "0" * 32
    attacks["invocation_substitution"] = rejected(
        lambda: pure_service_fixture(changed, clean_exec),
        "transaction service authority:InvocationID",
    )
    changed = dict(clean_fields); changed["Id"] = "lookalike.service"
    attacks["unit_substitution"] = rejected(
        lambda: pure_service_fixture(changed, clean_exec),
        "transaction service authority:Id",
    )
    bad_exec = clean_exec.replace(os.fspath(TRANSACTION_LAUNCHER), "/tmp/lookalike")
    attacks["execstart_substitution"] = rejected(
        lambda: pure_service_fixture(clean_fields, bad_exec), "exact ExecStart path/argv",
    )

    with tempfile.TemporaryDirectory(prefix="cm2-c30c-bridge-v2-fixture-") as temporary:
        root = Path(temporary)
        target = root / "target"
        durable_write_once(target, b"fixture")
        link1 = root / "python"
        link2 = root / "python3"
        link1.symlink_to("python3")
        link2.symlink_to(target)
        members = [fixture_member(target), fixture_member(link1), fixture_member(link2)]
        for member in members:
            pin_member_observation(member)
        link1.unlink(); link1.symlink_to("target")
        attacks["symlink_chain_drift"] = rejected(
            lambda: pin_member_observation(members[1]),
            "pinned member current byte/stat identity:",
        )

        pinned = fixture_member(target)
        tampered = root / "tampered"
        durable_write_once(tampered, b"tamper")
        os.replace(tampered, target)
        attacks["pin_tamper"] = rejected(
            lambda: pin_member_observation(pinned),
            "pinned member current byte/stat identity:",
        )

        inventory = root / "inventory"
        inventory.mkdir()
        durable_write_once(inventory / "a", b"a")
        expected_inventory = fixture_member(inventory)
        durable_write_once(inventory / "extra", b"x")
        attacks["extra_member"] = rejected(
            lambda: pin_member_observation(expected_inventory),
            "pinned member current byte/stat identity:",
        )

        stable = root / "stable"
        durable_write_once(stable, b"before")
        before = snapshot([stable])
        replacement = root / "replacement"
        durable_write_once(replacement, b"after")
        os.replace(replacement, stable)
        after = snapshot([stable])
        attacks["toctou_replace"] = rejected(
            lambda: need(before == after, "stage input pre/post SHA+full9stat identity"),
            "stage input pre/post SHA+full9stat identity",
        )

        object_value = object_with_closure({"schema": "fixture", "value": 1})
        verify_object_closure(object_value, "fixture")
        object_value["value"] = 2
        attacks["object_tamper"] = rejected(
            lambda: verify_object_closure(object_value, "fixture"),
            "object closure:fixture",
        )

    need(set(attacks) == {
        "wrong_bus_env", "missing_bus_env", "invocation_substitution",
        "unit_substitution", "execstart_substitution", "symlink_chain_drift",
        "pin_tamper", "extra_member", "toctou_replace", "object_tamper",
    }, "exact negative fixture inventory")
    return object_with_closure({
        "schema": "cm2.round306c30c.postreceipt-bridge-v2-preflight.v1",
        "status": "PASS_STATIC_AND_10_TINY_NEGATIVE_FIXTURES__ZERO_FORMAL_CREDIT",
        "control_bus": bus,
        "control_probe_sha256": hashlib.sha256(control_probe.stdout).hexdigest(),
        "negative_fixtures": attacks,
        "negative_fixture_count": len(attacks),
        "formal_execution_authorized": False,
        "formal_credit": 0,
        "source_W_formal_remainder": 80,
        "source_W_transition_authorized": False,
        "publication_authorized": False,
        "CM2": "NO-GO_FOR_CLAIM",
    })


def failure_output(error: BaseException) -> dict[str, Any]:
    return object_with_closure({
        "schema": BOUNDARY_SCHEMA,
        "status": "BLOCKED_FAIL_CLOSED",
        "error": str(error),
        "formal_credit": 0,
        "source_W_formal_remainder": 80,
        "source_W_transition_authorized": False,
        "publication_authorized": False,
        "CM2": "NO-GO_FOR_CLAIM",
    })


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--bridge-dir", type=Path)
    parser.add_argument("--pinset", type=Path)
    parser.add_argument("--pinset-sha256")
    parser.add_argument("--anchor", type=Path)
    parser.add_argument("--anchor-sha256")
    parser.add_argument("--launcher", type=Path, default=LAUNCHER)
    parser.add_argument("--maximum-wait-seconds", type=int, default=7 * 24 * 3600)
    arguments = parser.parse_args()
    try:
        need(arguments.self_test != arguments.run, "choose exactly one mode")
        if arguments.self_test:
            need(all(value is None for value in (
                arguments.bridge_dir, arguments.pinset, arguments.pinset_sha256,
                arguments.anchor, arguments.anchor_sha256,
            )), "self-test has no formal paths")
            output = self_test()
        else:
            need(all(value is not None for value in (
                arguments.bridge_dir, arguments.pinset, arguments.pinset_sha256,
                arguments.anchor, arguments.anchor_sha256,
            )), "complete formal launch material")
            bridge = Path(os.path.abspath(os.fspath(arguments.bridge_dir)))
            need(bridge.is_dir() and not bridge.is_symlink(), "precreated real bridge dir")
            output = run_bridge(
                bridge,
                arguments.pinset.resolve(strict=True),
                arguments.anchor.resolve(strict=True),
                str(arguments.pinset_sha256),
                str(arguments.anchor_sha256),
                arguments.launcher.resolve(strict=True),
                arguments.maximum_wait_seconds,
            )
    except (Blocked, OSError, ValueError, TypeError, KeyError,
            subprocess.SubprocessError) as error:
        output = failure_output(error)
        if arguments.run and arguments.bridge_dir is not None:
            bridge = Path(os.path.abspath(os.fspath(arguments.bridge_dir)))
            if bridge.is_dir() and not bridge.is_symlink():
                try:
                    if not (bridge / "PASS.lock").exists():
                        durable_json_once(bridge / "failure_receipt.json", output)
                        durable_write_once(bridge / "FAILED.lock", FAILED_LOCK)
                except (Blocked, OSError):
                    pass
        print(canonical(output).decode("ascii"), file=sys.stderr)
        return 1
    print(canonical(output).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
