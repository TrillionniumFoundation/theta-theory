#!/usr/bin/env python3
"""Append-only v5 post-exit composite finalizer (zero credit, CM2 NO-GO).

The v5 worker's READY.lock is deliberately non-authoritative.  This program
accepts it only together with the frozen launch anchor/pinset, the exact READY
tree, and the worker unit's clean post-exit tuple.  Its own direct Python
process is bound to systemd MainPID, ExecStart.pid, /proc/self/exe, and the
unit cgroup.  It then publishes a canonical running attestation and composite
receipt before making COMPOSITE_PASS.lock the final filesystem mutation.

Even that filesystem marker is not authority by itself.  A later observer must
again bind the receipt's exact finalizer unit, InvocationID, ExecStart and
fragment and observe active/exited, Result=success, ExecMainStatus=0.  All
objects remain zero-credit and CM2 NO-GO.
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
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence


sys.dont_write_bytecode = True

WORKSPACE = Path("/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572")
DELIVERABLES = WORKSPACE / "deliverables"
AUDIT = WORKSPACE / ".cm2-runtime/audit"
CONTROL = WORKSPACE / ".cm2-runtime/control"
SELF = DELIVERABLES / (
    "cm2_round306c30c_postreceipt_v3_p1_bridge_v5_"
    "post_exit_composite_finalizer_v1.py"
)
FINAL_PYTHON = Path("/usr/bin/python3.12")
SYSTEMCTL = Path("/usr/bin/systemctl")
UID = 1000
RUNTIME_DIR = Path("/run/user/1000")
BUS_SOCKET = RUNTIME_DIR / "bus"

CONTROL_ENV = {
    "HOME": "/nonexistent",
    "PATH": "/usr/bin:/bin",
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "XDG_RUNTIME_DIR": "/run/user/1000",
    "DBUS_SESSION_BUS_ADDRESS": "unix:path=/run/user/1000/bus",
}

# One systemd-show-lossless token.  It opens and retains the exact source FD,
# verifies the fragment-pinned SHA before compile, and transfers custody to
# held_entry.  There is no launcher-file execution or import-path lookup.
FINALIZER_BOOTSTRAP = (
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

PINSET_SCHEMA = "cm2.round306c30c.postreceipt-bridge-v5-pinset.v1"
ANCHOR_SCHEMA = "cm2.round306c30c.postreceipt-bridge-v5-launch-anchor.v1"
BOUNDARY_SCHEMA = "cm2.round306c30c.postreceipt-bridge-v5-boundary.v1"
SNAPSHOT_SCHEMA = "cm2.round306c30c.bridge-v3-recursive-snapshot.v1"
RUNNING_SCHEMA = (
    "cm2.round306c30c.postreceipt-bridge-v5-"
    "composite-finalizer-running-attestation.v1"
)
COMPOSITE_SCHEMA = (
    "cm2.round306c30c.postreceipt-bridge-v5-composite-receipt.v1"
)
READY_BYTES = b"READY_C30C_POSTRECEIPT_BRIDGE_V5_AWAITING_COMPOSITE_FINALIZER\n"
COMPOSITE_PASS_BYTES = (
    b"COMPOSITE_PASS_C30C_POSTRECEIPT_BRIDGE_V5_FILESYSTEM_ONLY__"
    b"FINALIZER_POST_EXIT_GATE_REQUIRED__ZERO_CREDIT\n"
)
PREPARED_READY = ".READY.lock.prepared-v5"
PREPARED_COMPOSITE = ".COMPOSITE_PASS.lock.prepared-v1"
RUNNING_ATTESTATION_NAME = "composite_finalizer_running_service_attestation.json"
COMPOSITE_RECEIPT_NAME = "composite_receipt.json"
COMPOSITE_MARKER_NAME = "COMPOSITE_PASS.lock"
COMPOSITE_RECEIPT_FIELDS = frozenset({
    "schema", "status", "token", "worker_unit", "worker_InvocationID",
    "worker_FragmentPath", "worker_post_exit_attestation_object_sha256",
    "worker_ready_tree_attestation_object_sha256",
    "terminal_boundary_object_sha256", "anchor_file_sha256",
    "anchor_object_sha256", "pinset_file_sha256", "pinset_object_sha256",
    "pinned_role_count", "finalizer_source_sha256", "finalizer_source_stat9",
    "running_attestation_name", "running_attestation_file_sha256",
    "running_attestation_stat9", "running_attestation_object_sha256",
    "composite_marker_name", "composite_marker_sha256",
    "prepared_marker_stat9", "marker_commit_method",
    "filesystem_marker_authoritative", "orphan_READY_authority_eligible",
    "orphan_COMPOSITE_PASS_authority_eligible",
    "joint_authority_requires_post_exit_query", "required_finalizer_post_exit",
    "authority_definition", "formal_credit", "source_W_formal_remainder",
    "source_W_transition_authorized", "publication_authorized",
    "terminal_replay_completed", "CM2", "object_sha256",
})
RUNNING_ATTESTATION_FIELDS = frozenset({
    "schema", "status", "token", "worker_unit", "finalizer_unit",
    "anchor_file_sha256", "anchor_object_sha256", "pinset_file_sha256",
    "finalizer_source_sha256", "worker_post_exit_attestation",
    "finalizer_running_attestation", "worker_ready_tree_attestation",
    "terminal_boundary_object_sha256", "filesystem_marker_authoritative",
    "joint_authority_requires_post_exit_query", "formal_credit",
    "source_W_formal_remainder", "source_W_transition_authorized",
    "publication_authorized", "terminal_replay_completed", "CM2",
    "object_sha256",
})

HEX64 = re.compile(r"[0-9a-f]{64}")
INVOCATION = re.compile(r"[0-9a-f]{32}")
TOKEN = re.compile(r"[A-Za-z0-9_.:-]+")
STAT9_KEYS = frozenset({
    "dev", "ino", "mode", "nlink", "uid", "gid", "size",
    "mtime_ns", "ctime_ns",
})

WORKER_PROPERTIES = (
    "Id", "InvocationID", "ExecStart", "ExecStartPre", "FragmentPath",
    "LoadState", "ActiveState", "SubState", "Result", "ExecMainCode",
    "ExecMainStatus", "MainPID", "ControlPID", "Type", "RemainAfterExit",
    "StandardOutput", "StandardError",
)
FINALIZER_PROPERTIES = (
    "Id", "InvocationID", "ExecStart", "FragmentPath", "LoadState",
    "ActiveState", "SubState", "Result", "ExecMainCode", "ExecMainStatus",
    "MainPID", "ControlPID", "Type", "RemainAfterExit", "StandardOutput",
    "StandardError",
)
BRIDGE_STABLE_FIELDS = frozenset({
    "Id", "InvocationID", "ExecStart", "ExecStartPre", "FragmentPath",
    "FragmentSHA256", "FragmentStat9", "LoadState", "Type",
    "RemainAfterExit", "StandardOutput", "StandardError",
})

STAGES: dict[str, str] = {
    "preflight-byte-replay": "preflight-validator",
    "receipt-validator-replay": "receipt-validator",
    "dual-seed-30630071": "dual-verifier",
    "dual-seed-30630929": "dual-verifier",
    "cold-seed-30630071": "cold-verifier",
    "cold-trace-analyzer": "cold-analyzer",
    "cold-pairing-gate": "pairing-gate",
}
COMMON_STAGE_FILES = frozenset({
    "pre_recursive_snapshot.json", "request.json", "input_pre.snapshot.json",
    "stdout.json", "stderr.log", "time.txt", "inner_attestation.json",
    "process_wrapper_stdout.json", "process_wrapper_stderr.log",
    "process_wrapper_receipt.json", "wrapper_process_attestation.json",
    "stage_conclusion.json", "input_post.snapshot.json",
    "post_recursive_snapshot.json", "final_recursive_snapshot.json",
})
ROOT_READY_FILES = frozenset({
    "root_pre_recursive_snapshot.json",
    "bridge_running_service_attestation.json", "preflight.json",
    "transaction_service_attestation.json", "transaction_receipt.raw.json",
    "transaction_preflight.raw.json", "dual_summary.json",
    "bridge_final_running_service_attestation.json",
    "root_post_recursive_snapshot.json", "terminal_boundary.json",
    "service_stdout.json", "root_final_recursive_snapshot.json", "READY.lock",
})

BASE_PIN_ROLES = frozenset({
    "bridge_watcher", "bridge_start_gate", "bridge_composite_finalizer",
    "process_wrapper", "receipt_validator", "attack_harness",
    "independent_verifier", "cold_analyzer", "pairing_gate", "venv_python",
    "venv_python3", "system_python_link", "final_python", "gnu_time",
    "strace", "env", "systemctl", "transaction_launcher",
    "transaction_pins", "transaction_fragment", "bridge_fragment",
    "transaction_run_dir", "transaction_receipt_dir",
})
EXPECTED_PIN_ROLES = set(BASE_PIN_ROLES)
for _seed in ("30630071", "30630929"):
    EXPECTED_PIN_ROLES.add("candidate_dir_" + _seed)
    EXPECTED_PIN_ROLES.update(
        f"candidate_{_seed}_{index:02d}" for index in range(6)
    )
EXPECTED_PIN_ROLES.update(f"transaction_run_{index:02d}" for index in range(16))
EXPECTED_PIN_ROLES.update(
    f"transaction_receipt_{index:02d}" for index in range(11)
)
EXPECTED_PIN_ROLES = frozenset(EXPECTED_PIN_ROLES)


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
    value = dict(body)
    need("object_sha256" not in value, "fresh object closure")
    value["object_sha256"] = hashlib.sha256(canonical(value)).hexdigest()
    return value


def verify_closure(value: Mapping[str, Any], label: str) -> None:
    need(type(value) is dict and HEX64.fullmatch(value.get("object_sha256", ""))
         is not None, "closure field:" + label)
    body = dict(value)
    observed = body.pop("object_sha256")
    need(hashlib.sha256(canonical(body)).hexdigest() == observed,
         "closure digest:" + label)


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    def pairs(rows: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in rows:
            need(key not in result, "duplicate JSON key:" + label)
            result[key] = value
        return result

    try:
        value = json.loads(
            raw.decode("ascii"), object_pairs_hook=pairs,
            parse_float=lambda _value: (_ for _ in ()).throw(ValueError()),
            parse_constant=lambda _value: (_ for _ in ()).throw(ValueError()),
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise Reject("strict JSON:" + label) from error
    need(type(value) is dict and raw in {canonical(value), canonical(value) + b"\n"},
         "canonical JSON:" + label)
    return value


def zero_contract(value: Mapping[str, Any], label: str) -> None:
    need(type(value.get("formal_credit")) is int
         and value["formal_credit"] == 0, "zero credit:" + label)
    need(type(value.get("source_W_formal_remainder")) is int
         and value["source_W_formal_remainder"] == 80,
         "source-W remainder:" + label)
    for key in (
        "source_W_transition_authorized", "publication_authorized",
        "terminal_replay_completed",
    ):
        need(value.get(key) is False, "explicit false:" + label + ":" + key)
    if "CM2" in value:
        need(value["CM2"] == "NO-GO_FOR_CLAIM", "CM2 NO-GO:" + label)


def exact_file_sha(observed: Any, expected: str, label: str) -> None:
    need(type(observed) is str and HEX64.fullmatch(observed) is not None
         and HEX64.fullmatch(expected) is not None and observed == expected,
         "exact file SHA:" + label)


def stat9(value: os.stat_result) -> dict[str, int]:
    return {
        "dev": value.st_dev, "ino": value.st_ino, "mode": value.st_mode,
        "nlink": value.st_nlink, "uid": value.st_uid, "gid": value.st_gid,
        "size": value.st_size, "mtime_ns": value.st_mtime_ns,
        "ctime_ns": value.st_ctime_ns,
    }


def validate_stat9(value: Any, label: str) -> dict[str, int]:
    need(type(value) is dict and set(value) == STAT9_KEYS
         and all(type(item) is int for item in value.values()),
         "exact stat9:" + label)
    return dict(value)


def identity(value: os.stat_result | Mapping[str, int]) -> tuple[int, ...]:
    row = stat9(value) if isinstance(value, os.stat_result) else value
    return tuple(row[key] for key in (
        "dev", "ino", "mode", "nlink", "uid", "gid", "size",
        "mtime_ns", "ctime_ns",
    ))


def stable_dir_identity(value: os.stat_result | Mapping[str, int]) -> tuple[int, ...]:
    row = stat9(value) if isinstance(value, os.stat_result) else value
    return tuple(row[key] for key in ("dev", "ino", "mode", "uid", "gid"))


def stable_rename_identity(value: Mapping[str, int]) -> tuple[int, ...]:
    return tuple(value[key] for key in (
        "dev", "ino", "mode", "nlink", "uid", "gid", "size", "mtime_ns",
    ))


def runtime_directory_identity_allowed(
    expected: os.stat_result | Mapping[str, int],
    observed: os.stat_result | Mapping[str, int],
) -> bool:
    """Shared /run/user metadata may churn; its inode/owner/mode may not."""
    return stable_dir_identity(expected) == stable_dir_identity(observed)


def read_fd(fd: int, maximum: int) -> bytes:
    before = os.fstat(fd)
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1
         and 0 <= before.st_size <= maximum, "bounded singleton regular FD")
    os.lseek(fd, 0, os.SEEK_SET)
    remaining = before.st_size
    chunks: list[bytes] = []
    while remaining:
        block = os.read(fd, min(4 << 20, remaining))
        need(bool(block), "complete FD read")
        chunks.append(block)
        remaining -= len(block)
    need(os.read(fd, 1) == b"", "stable FD EOF")
    need(identity(os.fstat(fd)) == identity(before), "stable FD stat")
    return b"".join(chunks)


def hash_fd(fd: int, maximum: int = 64 << 30) -> str:
    before = os.fstat(fd)
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1
         and 0 <= before.st_size <= maximum, "bounded hash FD")
    os.lseek(fd, 0, os.SEEK_SET)
    remaining = before.st_size
    digest = hashlib.sha256()
    while remaining:
        block = os.read(fd, min(4 << 20, remaining))
        need(bool(block), "complete hash read")
        digest.update(block)
        remaining -= len(block)
    need(os.read(fd, 1) == b"" and identity(os.fstat(fd)) == identity(before),
         "stable hash EOF/stat")
    return digest.hexdigest()


class HeldFile:
    def __init__(self, path: Path, label: str, maximum: int = 64 << 30):
        self.path = Path(os.path.abspath(os.fspath(path)))
        before = self.path.lstat()
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular singleton:" + label)
        self.fd = os.open(
            self.path, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
        )
        self.initial = os.fstat(self.fd)
        need(identity(before) == identity(self.initial), "held open race:" + label)
        self.raw = read_fd(self.fd, maximum)
        self.sha256 = hashlib.sha256(self.raw).hexdigest()
        self.maximum = maximum
        self.label = label

    def verify(self) -> None:
        need(identity(self.path.lstat()) == identity(self.initial)
             == identity(os.fstat(self.fd)), "held identity drift:" + self.label)
        need(hash_fd(self.fd, self.maximum) == self.sha256,
             "held byte drift:" + self.label)

    def close(self) -> None:
        os.close(self.fd)


class HeldDir:
    def __init__(self, path: Path, label: str):
        self.path = Path(os.path.abspath(os.fspath(path)))
        before = self.path.lstat()
        need(stat.S_ISDIR(before.st_mode) and not stat.S_ISLNK(before.st_mode)
             and before.st_uid == UID and stat.S_IMODE(before.st_mode) == 0o700,
             "private owned directory:" + label)
        self.fd = os.open(
            self.path, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC
            | getattr(os, "O_NOFOLLOW", 0),
        )
        self.initial = os.fstat(self.fd)
        self.label = label
        need(identity(before) == identity(self.initial), "directory open race:" + label)

    def verify(self) -> None:
        need(stable_dir_identity(self.path.lstat())
             == stable_dir_identity(self.initial)
             == stable_dir_identity(os.fstat(self.fd)),
             "held directory renamed:" + self.label)

    def names(self) -> list[str]:
        self.verify()
        return sorted(os.listdir(self.fd))

    def open_regular(self, name: str, maximum: int) -> tuple[bytes, dict[str, int]]:
        need(name and "/" not in name and name not in {".", ".."},
             "direct child token")
        before = os.stat(name, dir_fd=self.fd, follow_symlinks=False)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "direct singleton regular:" + name)
        fd = os.open(
            name, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
            dir_fd=self.fd,
        )
        try:
            opened = os.fstat(fd)
            raw = read_fd(fd, maximum)
            after = os.fstat(fd)
        finally:
            os.close(fd)
        current = os.stat(name, dir_fd=self.fd, follow_symlinks=False)
        need(identity(before) == identity(opened) == identity(after)
             == identity(current), "stable direct child:" + name)
        return raw, stat9(opened)

    def write_once(self, name: str, raw: bytes) -> dict[str, int]:
        need(name and "/" not in name and name not in {".", ".."},
             "direct output token")
        self.verify()
        fd = os.open(
            name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC
            | getattr(os, "O_NOFOLLOW", 0), 0o400, dir_fd=self.fd,
        )
        try:
            offset = 0
            while offset < len(raw):
                count = os.write(fd, raw[offset:])
                need(count > 0, "positive write progress")
                offset += count
            os.fsync(fd)
            written = os.fstat(fd)
        finally:
            os.close(fd)
        observed, reopened = self.open_regular(name, max(1, len(raw)))
        need(observed == raw and reopened == stat9(written),
             "O_EXCL output readback:" + name)
        os.fsync(self.fd)
        self.verify()
        return reopened

    def write_json(self, name: str, value: Mapping[str, Any]) -> dict[str, int]:
        return self.write_once(name, canonical(dict(value)) + b"\n")

    def close(self) -> None:
        os.close(self.fd)


def parse_systemctl(raw: bytes) -> dict[str, str]:
    try:
        rows = raw.decode("ascii").splitlines()
    except UnicodeDecodeError as error:
        raise Reject("systemctl ASCII") from error
    result: dict[str, str] = {}
    for row in rows:
        key, separator, value = row.partition("=")
        need(separator == "=" and key and key not in result,
             "unique systemctl property")
        result[key] = value
    return result


class RuntimeAuthority:
    def __init__(self) -> None:
        need(os.getuid() == UID and os.geteuid() == UID, "exact uid/euid")
        runtime_before = RUNTIME_DIR.lstat()
        need(stat.S_ISDIR(runtime_before.st_mode) and runtime_before.st_uid == UID,
             "owned user runtime")
        self.runtime_fd = os.open(
            RUNTIME_DIR, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC
            | getattr(os, "O_NOFOLLOW", 0),
        )
        self.runtime_state = os.fstat(self.runtime_fd)
        need(identity(runtime_before) == identity(self.runtime_state),
             "runtime open race")
        socket_before = BUS_SOCKET.lstat()
        need(stat.S_ISSOCK(socket_before.st_mode) and socket_before.st_uid == UID,
             "owned real user bus")
        self.socket_fd = os.open(
            BUS_SOCKET, getattr(os, "O_PATH", os.O_RDONLY) | os.O_CLOEXEC
            | getattr(os, "O_NOFOLLOW", 0),
        )
        self.socket_state = os.fstat(self.socket_fd)
        need(identity(socket_before) == identity(self.socket_state),
             "bus socket open race")
        self.systemctl = HeldFile(SYSTEMCTL, "systemctl", 64 << 20)

    def verify(self) -> None:
        need(runtime_directory_identity_allowed(
                 self.runtime_state, RUNTIME_DIR.lstat(),
             ) and runtime_directory_identity_allowed(
                 self.runtime_state, os.fstat(self.runtime_fd),
             ), "runtime stable directory identity drift")
        need(identity(BUS_SOCKET.lstat()) == identity(self.socket_state)
             == identity(os.fstat(self.socket_fd)), "bus identity drift")
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
             "clean systemctl query")
        fields = parse_systemctl(completed.stdout)
        need(set(fields) == set(properties), "exact systemctl property set")
        return fields, completed.stdout

    def close(self) -> None:
        self.systemctl.close()
        os.close(self.socket_fd)
        os.close(self.runtime_fd)


SYSTEMD_SHOW_FORBIDDEN = frozenset(b"'\"\\$%")


def exact_systemd_show_argv(argv: Sequence[str], label: str) -> list[str]:
    result = list(argv)
    need(result and all(type(item) is str and item for item in result),
         "nonempty argv:" + label)
    for item in result:
        try:
            raw = item.encode("ascii")
        except UnicodeEncodeError as error:
            raise Reject("ASCII argv:" + label) from error
        need(all(0x21 <= byte <= 0x7e for byte in raw)
             and not (set(raw) & SYSTEMD_SHOW_FORBIDDEN) and item != ";",
             "systemd-show-lossless token:" + label)
    return result


def expected_execstart_argv(
    bridge: Path, pinset: Path, anchor: Path, worker_unit: str,
    finalizer_unit: str, maximum_wait: int, source_sha256: str,
) -> list[str]:
    need(HEX64.fullmatch(source_sha256) is not None, "finalizer source SHA")
    need(type(maximum_wait) is int and 0 <= maximum_wait <= 7 * 24 * 3600,
         "bounded maximum wait")
    argv = [
        os.fspath(FINAL_PYTHON), "-I", "-B", "-c", FINALIZER_BOOTSTRAP,
        os.fspath(SELF), source_sha256, "--run",
        "--bridge-dir", os.fspath(bridge), "--pinset", os.fspath(pinset),
        "--anchor", os.fspath(anchor), "--worker-unit", worker_unit,
        "--finalizer-unit", finalizer_unit, "--maximum-wait-seconds",
        str(maximum_wait),
    ]
    need(len(argv) == 20, "exact finalizer argv cardinality")
    return exact_systemd_show_argv(argv, "composite finalizer")


def parse_exec_command(
    raw: str, expected_argv: Sequence[str], label: str,
) -> dict[str, Any]:
    match = re.fullmatch(
        r"\{ path=([^ ;]+) ; argv\[\]=(.+) ; ignore_errors=no ; "
        r"start_time=\[(.*)\] ; stop_time=\[(.*)\] ; pid=([0-9]+) ; "
        r"code=([^ ;]+) ; status=([^ }]+) \}", raw,
    )
    need(match is not None, "strict ExecStart syntax:" + label)
    path, argv_text, start, stop, pid, code, status_text = match.groups()
    expected = exact_systemd_show_argv(expected_argv, label)
    need(path == os.fspath(FINAL_PYTHON)
         and argv_text == " ".join(expected), "exact ExecStart argv/path:" + label)
    return {
        "path": path, "argv": expected, "start_time": start,
        "stop_time": stop, "pid": int(pid), "code": code,
        "status": status_text,
    }


def completed_exec_projection(command: Mapping[str, Any], label: str) -> str:
    retained = (
        command.get("pid", 0) > 1
        and command.get("start_time") not in {"", "n/a"}
        and command.get("stop_time") not in {"", "n/a"}
        and command.get("code") == "exited"
        and command.get("status") in {"0", "0/0"}
    )
    decayed = (
        command.get("pid") == 0 and command.get("start_time") == "n/a"
        and command.get("stop_time") == "n/a"
        and command.get("code") == "(null)"
        and command.get("status") in {"0", "0/0"}
    )
    need(retained or decayed, "successful completed/decayed exec projection:" + label)
    return "completed-pid-retained" if retained else "manager-reload-decayed-zero"


def split_units(
    bridge: Path, worker_unit: str, finalizer_unit: str,
) -> str:
    prefix = "c30c-postreceipt-v3-p1-bridge-v5-"
    need(bridge.parent == AUDIT and bridge.name.startswith(prefix),
         "v5 bridge audit namespace")
    token = bridge.name[len(prefix):]
    need(TOKEN.fullmatch(token) is not None,
         "bridge token")
    need(worker_unit == "cm2-" + prefix + token + ".service",
         "worker exact same-token unit")
    need(finalizer_unit == "cm2-" + prefix + "finalizer-" + token + ".service",
         "finalizer exact same-token unit")
    need(worker_unit != finalizer_unit, "distinct worker/finalizer units")
    return token


def material_paths(
    bridge: Path, pinset: Path, anchor: Path,
    worker_unit: str, finalizer_unit: str, maximum_wait: int,
) -> tuple[Path, Path, Path, str]:
    bridge = Path(os.path.abspath(os.fspath(bridge)))
    pinset = Path(os.path.abspath(os.fspath(pinset)))
    anchor = Path(os.path.abspath(os.fspath(anchor)))
    token = split_units(bridge, worker_unit, finalizer_unit)
    need(pinset.parent == anchor.parent and pinset.parent.parent == CONTROL
         and pinset.parent.name == bridge.name, "matched v5 control/audit roots")
    need(pinset.name == "pinset.json" and anchor.name == "launch-anchor.json",
         "exact material basenames")
    need(type(maximum_wait) is int and 0 <= maximum_wait <= 7 * 24 * 3600,
         "bounded finalizer wait")
    return bridge, pinset, anchor, token


def regular_observation(path: Path, maximum: int = 64 << 30) -> dict[str, Any]:
    held = HeldFile(path, "pin regular", maximum)
    try:
        held.verify()
        return {
            "path": os.fspath(held.path), "kind": "regular",
            "sha256": held.sha256, "stat9": stat9(held.initial),
        }
    finally:
        held.close()


def symlink_observation(path: Path) -> dict[str, Any]:
    path = Path(os.path.abspath(os.fspath(path)))
    before = path.lstat()
    need(stat.S_ISLNK(before.st_mode) and before.st_nlink == 1,
         "singleton pin symlink")
    target = os.readlink(path)
    need(identity(path.lstat()) == identity(before), "stable pin symlink")
    return {
        "path": os.fspath(path), "kind": "symlink", "target": target,
        "stat9": stat9(before),
    }


def directory_observation(path: Path) -> dict[str, Any]:
    path = Path(os.path.abspath(os.fspath(path)))
    before = path.lstat()
    need(stat.S_ISDIR(before.st_mode) and not stat.S_ISLNK(before.st_mode),
         "real pin directory")
    fd = os.open(
        path, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC
        | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        opened = os.fstat(fd)
        names = sorted(os.listdir(fd))
        after = os.fstat(fd)
    finally:
        os.close(fd)
    need(identity(before) == identity(opened) == identity(after)
         == identity(path.lstat()), "stable pin directory")
    return {
        "path": os.fspath(path), "kind": "directory", "inventory": names,
        "stat9": stat9(opened),
    }


def observe_pin(row: Mapping[str, Any]) -> dict[str, Any]:
    need(type(row) is dict and set(row) >= {"role", "path", "kind", "stat9"},
         "pin base shape")
    role = row.get("role")
    path_raw = row.get("path")
    need(type(role) is str and re.fullmatch(r"[a-z0-9_]{1,96}", role)
         is not None and type(path_raw) is str, "pin role/path types")
    path = Path(path_raw)
    need(path.is_absolute() and path == Path(os.path.abspath(path_raw)),
         "canonical absolute pin path:" + role)
    validate_stat9(row.get("stat9"), "pin:" + role)
    if row.get("kind") == "regular":
        need(set(row) == {"role", "path", "kind", "sha256", "stat9"}
             and HEX64.fullmatch(row.get("sha256", "")) is not None,
             "regular pin shape:" + role)
        observed = regular_observation(path)
    elif row.get("kind") == "symlink":
        need(set(row) == {"role", "path", "kind", "target", "stat9"}
             and type(row.get("target")) is str, "symlink pin shape:" + role)
        observed = symlink_observation(path)
    elif row.get("kind") == "directory":
        need(set(row) == {"role", "path", "kind", "inventory", "stat9"}
             and type(row.get("inventory")) is list
             and all(type(name) is str for name in row["inventory"]),
             "directory pin shape:" + role)
        observed = directory_observation(path)
    else:
        raise Reject("unknown pin kind:" + role)
    observed["role"] = role
    need(observed == dict(row), "pin live byte/type/stat replay:" + role)
    return observed


def parse_anchor(held: HeldFile, bridge: HeldDir, pinset: HeldFile,
                 worker_unit: str) -> dict[str, Any]:
    value = strict_json(held.raw, "v5 launch anchor")
    verify_closure(value, "v5 launch anchor")
    required = {
        "schema", "status", "watcher_path", "watcher_sha256", "watcher_stat9",
        "gate_path", "gate_sha256", "gate_stat9", "wrapper_path",
        "wrapper_sha256", "wrapper_stat9", "pinset_path", "pinset_sha256",
        "pinset_stat9", "bridge_dir", "bridge_service", "transaction_service",
        "formal_credit", "source_W_formal_remainder",
        "source_W_transition_authorized", "publication_authorized",
        "terminal_replay_completed", "object_sha256",
    }
    need(set(value) == required and value.get("schema") == ANCHOR_SCHEMA
         and value.get("status") == "FROZEN_BRIDGE_V5_PRESTART_GATE_ZERO_CREDIT",
         "exact v5 anchor shape/schema/status")
    zero_contract(value, "anchor")
    for key in ("watcher_sha256", "gate_sha256", "wrapper_sha256", "pinset_sha256"):
        need(HEX64.fullmatch(value.get(key, "")) is not None,
             "anchor SHA:" + key)
    for key in ("watcher_stat9", "gate_stat9", "wrapper_stat9", "pinset_stat9"):
        validate_stat9(value.get(key), "anchor:" + key)
    need(value["pinset_path"] == os.fspath(pinset.path)
         and value["pinset_sha256"] == pinset.sha256
         and value["pinset_stat9"] == stat9(pinset.initial),
         "anchor exact pinset binding")
    need(value["bridge_dir"] == os.fspath(bridge.path), "anchor bridge root")
    service = value.get("bridge_service")
    need(type(service) is dict and set(service) == BRIDGE_STABLE_FIELDS,
         "exact worker stable anchor fields")
    need(service.get("Id") == worker_unit
         and INVOCATION.fullmatch(service.get("InvocationID", "")) is not None,
         "anchor worker unit/invocation")
    need(type(service.get("ExecStart")) is list
         and type(service.get("ExecStartPre")) is list
         and all(type(item) is str for item in service["ExecStart"] + service["ExecStartPre"]),
         "anchor exact exec argv lists")
    need(service.get("LoadState") == "loaded" and service.get("Type") == "exec"
         and service.get("RemainAfterExit") == "yes"
         and service.get("StandardOutput") == "journal"
         and service.get("StandardError") == "journal",
         "anchor worker stable service contract")
    need(type(service.get("FragmentPath")) is str
         and HEX64.fullmatch(service.get("FragmentSHA256", "")) is not None,
         "anchor worker fragment path/SHA")
    validate_stat9(service.get("FragmentStat9"), "anchor worker fragment")
    transaction = value.get("transaction_service")
    need(type(transaction) is dict and set(transaction) == {
        "Id", "InvocationID", "ExecStart", "FragmentPath", "FragmentSHA256",
        "FragmentStat9", "LoadState", "ActiveState", "SubState", "Result",
        "ExecMainCode", "ExecMainStatus", "MainPID", "Type", "RemainAfterExit",
        "StandardOutput", "StandardError",
    }, "anchor exact transaction projection")
    return value


def parse_pinset(
    held: HeldFile, anchor: Mapping[str, Any], executed_source: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    value = strict_json(held.raw, "v5 pinset")
    verify_closure(value, "v5 pinset")
    need(set(value) == {
        "schema", "status", "members", "formal_credit",
        "source_W_formal_remainder", "source_W_transition_authorized",
        "publication_authorized", "terminal_replay_completed", "object_sha256",
    } and value.get("schema") == PINSET_SCHEMA
        and value.get("status") == "FROZEN_EXACT_ROLE_SET_BRIDGE_V5_ZERO_CREDIT",
        "exact pinset shape/schema/status")
    zero_contract(value, "pinset")
    rows = value.get("members")
    need(type(rows) is list and all(type(row) is dict for row in rows),
         "pinset member list")
    roles = [row.get("role") for row in rows]
    need(roles == sorted(roles) and set(roles) == EXPECTED_PIN_ROLES
         and len(roles) == len(EXPECTED_PIN_ROLES), "exact sorted v5 pin role set")
    observations: dict[str, dict[str, Any]] = {}
    for row in rows:
        observed = observe_pin(row)
        observations[observed["role"]] = observed
    finalizer = observations["bridge_composite_finalizer"]
    need(finalizer.get("kind") == "regular"
         and finalizer.get("path") == os.fspath(SELF)
         and finalizer.get("sha256") == executed_source["sha256"]
         and finalizer.get("stat9") == executed_source["stat9"]
         and stat.S_IMODE(finalizer["stat9"]["mode"]) == 0o444,
         "pinset exact held composite finalizer role")
    for role, prefix in (
        ("bridge_watcher", "watcher"), ("bridge_start_gate", "gate"),
        ("process_wrapper", "wrapper"),
    ):
        row = observations[role]
        need(row.get("kind") == "regular"
             and row.get("path") == anchor[prefix + "_path"]
             and row.get("sha256") == anchor[prefix + "_sha256"]
             and row.get("stat9") == anchor[prefix + "_stat9"]
             and stat.S_IMODE(row["stat9"]["mode"]) == 0o444,
             "pinset critical anchor binding:" + role)
    fragment = observations["bridge_fragment"]
    worker = anchor["bridge_service"]
    need(fragment.get("kind") == "regular"
         and fragment.get("path") == worker["FragmentPath"]
         and fragment.get("sha256") == worker["FragmentSHA256"]
         and fragment.get("stat9") == worker["FragmentStat9"],
         "pinset exact worker fragment binding")
    return value, observations


def expected_ready_paths() -> set[str]:
    paths = {"."}
    paths.update(ROOT_READY_FILES)
    for stage in STAGES:
        paths.add(stage)
        files = set(COMMON_STAGE_FILES)
        if stage == "cold-seed-30630071":
            files.add("trace.raw")
        paths.update(stage + "/" + name for name in files)
    return paths


def snapshot_tree(root: HeldDir) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}

    def visit(fd: int, relative: str) -> None:
        directory = os.fstat(fd)
        need(stat.S_ISDIR(directory.st_mode) and directory.st_uid == UID
             and stat.S_IMODE(directory.st_mode) == 0o700,
             "snapshot private directory:" + (relative or "."))
        key = relative or "."
        need(key not in rows, "unique snapshot path")
        rows[key] = {"path": key, "type": "directory", "stat9": stat9(directory)}
        for name in sorted(os.listdir(fd)):
            need(name and name not in {".", ".."} and "/" not in name,
                 "snapshot child token")
            child_path = name if not relative else relative + "/" + name
            state = os.stat(name, dir_fd=fd, follow_symlinks=False)
            if stat.S_ISREG(state.st_mode):
                need(state.st_nlink == 1 and state.st_uid == UID
                     and stat.S_IMODE(state.st_mode) == 0o400,
                     "snapshot frozen singleton file:" + child_path)
                child = os.open(
                    name, os.O_RDONLY | os.O_CLOEXEC
                    | getattr(os, "O_NOFOLLOW", 0), dir_fd=fd,
                )
                try:
                    opened = os.fstat(child)
                    digest = hash_fd(child)
                    after = os.fstat(child)
                finally:
                    os.close(child)
                need(identity(state) == identity(opened) == identity(after),
                     "snapshot stable file:" + child_path)
                rows[child_path] = {
                    "path": child_path, "type": "regular", "sha256": digest,
                    "stat9": stat9(opened),
                }
            elif stat.S_ISDIR(state.st_mode):
                child = os.open(
                    name, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC
                    | getattr(os, "O_NOFOLLOW", 0), dir_fd=fd,
                )
                try:
                    need(identity(state) == identity(os.fstat(child)),
                         "snapshot directory open race:" + child_path)
                    visit(child, child_path)
                finally:
                    os.close(child)
            else:
                raise Reject("snapshot rejects symlink/special:" + child_path)

    root.verify()
    visit(root.fd, "")
    root.verify()
    return rows


def parse_recorded_snapshot(raw: bytes) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    value = strict_json(raw, "root final recursive snapshot")
    verify_closure(value, "root final recursive snapshot")
    need(set(value) == {
        "schema", "rows", "row_count", "formal_credit",
        "source_W_formal_remainder", "source_W_transition_authorized",
        "publication_authorized", "terminal_replay_completed", "object_sha256",
    } and value.get("schema") == SNAPSHOT_SCHEMA, "exact snapshot schema/shape")
    zero_contract(value, "root final snapshot")
    raw_rows = value.get("rows")
    need(type(raw_rows) is list and value.get("row_count") == len(raw_rows),
         "snapshot row count")
    rows: dict[str, dict[str, Any]] = {}
    for row in raw_rows:
        need(type(row) is dict and type(row.get("path")) is str
             and row["path"] not in rows, "snapshot unique row")
        validate_stat9(row.get("stat9"), "snapshot:" + row["path"])
        if row.get("type") == "directory":
            need(set(row) == {"path", "type", "stat9"}, "snapshot directory row")
        else:
            need(row.get("type") == "regular"
                 and set(row) == {"path", "type", "sha256", "stat9"}
                 and HEX64.fullmatch(row.get("sha256", "")) is not None,
                 "snapshot regular row")
        rows[row["path"]] = dict(row)
    return value, rows


def validate_ready_snapshot_release(
    recorded: Mapping[str, Mapping[str, Any]],
    current: Mapping[str, Mapping[str, Any]],
    expected_current: set[str],
) -> None:
    expected_recorded = (expected_current - {
        "root_final_recursive_snapshot.json", "READY.lock",
    }) | {PREPARED_READY}
    need(set(recorded) == expected_recorded, "recorded exact pre-READY tree")
    need(set(current) == expected_current, "current exact READY tree")
    for path, row in recorded.items():
        if path == ".":
            need(stable_dir_identity(row["stat9"])
                 == stable_dir_identity(current[path]["stat9"]),
                 "READY root stable identity")
        elif path == PREPARED_READY:
            released = current["READY.lock"]
            need(row.get("type") == released.get("type") == "regular"
                 and row.get("sha256") == released.get("sha256")
                 == hashlib.sha256(READY_BYTES).hexdigest()
                 and stable_rename_identity(row["stat9"])
                 == stable_rename_identity(released["stat9"]),
                 "READY rename preserves prepared bytes/inode")
        else:
            need(current.get(path) == row,
                 "READY prior member exact hash/full9stat:" + path)


def stable_ready_tree_sha256(rows: Mapping[str, Mapping[str, Any]]) -> str:
    """Normalize only the held root's mutable directory metadata."""
    normalized: list[dict[str, Any]] = []
    for path in sorted(rows):
        row = dict(rows[path])
        if path == ".":
            source = row.get("stat9")
            validate_stat9(source, "stable READY root")
            row["stat9"] = {
                key: source[key] for key in ("dev", "ino", "mode", "uid", "gid")
            }
        normalized.append(row)
    return hashlib.sha256(canonical(normalized)).hexdigest()


def validate_ready_tree(
    root: HeldDir, exact_composite_extras: frozenset[str] = frozenset(),
) -> dict[str, Any]:
    raw, snapshot_stat = root.open_regular("root_final_recursive_snapshot.json", 64 << 30)
    recorded_object, recorded = parse_recorded_snapshot(raw)
    need(exact_composite_extras in {
        frozenset(), frozenset({
            RUNNING_ATTESTATION_NAME, COMPOSITE_RECEIPT_NAME,
            COMPOSITE_MARKER_NAME,
        }),
    }, "bounded READY-tree composite extension mode")
    current_all = snapshot_tree(root)
    worker_paths = expected_ready_paths()
    need(set(current_all) == worker_paths | set(exact_composite_extras),
         "exact worker READY plus bounded composite inventory")
    current = {path: current_all[path] for path in worker_paths}
    validate_ready_snapshot_release(recorded, current, worker_paths)
    ready_raw, ready_stat = root.open_regular("READY.lock", 128)
    need(ready_raw == READY_BYTES
         and current["root_final_recursive_snapshot.json"]["sha256"]
             == hashlib.sha256(raw).hexdigest()
         and current["root_final_recursive_snapshot.json"]["stat9"]
             == snapshot_stat
         and current["READY.lock"]["sha256"]
             == hashlib.sha256(ready_raw).hexdigest()
         and current["READY.lock"]["stat9"] == ready_stat,
         "exact non-authoritative READY/snapshot current bindings")
    return closed({
        "schema": "cm2.round306c30c.postreceipt-bridge-v5-ready-tree-attestation.v1",
        "status": "PASS_EXACT_WORKER_READY_TREE__READY_NON_AUTHORITATIVE",
        "recorded_snapshot_object_sha256": recorded_object["object_sha256"],
        "recorded_snapshot_file_sha256": hashlib.sha256(raw).hexdigest(),
        "recorded_snapshot_stat9": snapshot_stat,
        "ready_sha256": hashlib.sha256(ready_raw).hexdigest(),
        "ready_stat9": ready_stat,
        "observed_row_count": len(current),
        "observed_tree_sha256": stable_ready_tree_sha256(current),
        "ready_marker_authoritative": False,
        "formal_credit": 0, "source_W_formal_remainder": 80,
        "source_W_transition_authorized": False,
        "publication_authorized": False, "terminal_replay_completed": False,
        "CM2": "NO-GO_FOR_CLAIM",
    })


def read_closed_child(root: HeldDir, name: str, maximum: int) -> tuple[dict[str, Any], bytes]:
    raw, _state = root.open_regular(name, maximum)
    value = strict_json(raw, name)
    verify_closure(value, name)
    zero_contract(value, name)
    return value, raw


def validate_ready_documents(
    root: HeldDir, anchor: Mapping[str, Any], anchor_file_sha256: str,
    pinset: HeldFile,
    finalizer_unit: str, executed_source: Mapping[str, Any],
) -> dict[str, Any]:
    boundary, boundary_raw = read_closed_child(root, "terminal_boundary.json", 4 << 20)
    required = {
        "schema", "status", "anchor_sha256", "pinset_sha256",
        "transaction_receipt_sha256", "preflight_replay_sha256",
        "dual_stdout_sha256", "independent_true_inner_pid_count",
        "bridge_service_post_exit_verification_required",
        "bridge_service_revalidated_after_every_stage",
        "manager_reload_execstart_zero_projection_bounded", "prepared_ready_name",
        "ready_commit_method", "ready_marker_authoritative",
        "required_authoritative_composite", "required_finalizer_unit",
        "required_finalizer_path", "required_finalizer_sha256",
        "required_finalizer_stat9", "formal_credit", "source_W_formal_remainder",
        "source_W_transition_authorized", "publication_authorized",
        "terminal_replay_completed", "CM2", "object_sha256",
    }
    need(set(boundary) == required and boundary.get("schema") == BOUNDARY_SCHEMA
         and boundary.get("status")
         == "PASS_ZERO_CREDIT_POSTRECEIPT_BOUNDARY__PUBLICATION_NOT_AUTHORIZED",
         "exact boundary shape/schema/status")
    exact_file_sha(boundary.get("anchor_sha256"), anchor_file_sha256,
                   "boundary anchor")
    need(boundary.get("pinset_sha256") == pinset.sha256,
         "boundary pinset file SHA")
    need(boundary.get("independent_true_inner_pid_count") == 7
         and boundary.get("bridge_service_post_exit_verification_required") is True
         and boundary.get("bridge_service_revalidated_after_every_stage") is True
         and boundary.get("manager_reload_execstart_zero_projection_bounded") is True
         and boundary.get("prepared_ready_name") == PREPARED_READY
         and boundary.get("ready_commit_method")
             == "renameat2_RENAME_NOREPLACE_then_parent_fsync"
         and boundary.get("ready_marker_authoritative") is False
         and boundary.get("required_authoritative_composite") == [
             COMPOSITE_RECEIPT_NAME, COMPOSITE_MARKER_NAME,
             "post_exit_finalizer_unit_success",
         ], "boundary exact composite requirement")
    need(boundary.get("required_finalizer_unit") == finalizer_unit
         and boundary.get("required_finalizer_path") == os.fspath(SELF)
         and boundary.get("required_finalizer_sha256") == executed_source["sha256"]
         and boundary.get("required_finalizer_stat9") == executed_source["stat9"],
         "boundary exact finalizer unit/source pin")
    service, service_raw = read_closed_child(root, "service_stdout.json", 4 << 20)
    need(set(service) == {
        "schema", "status", "boundary_object_sha256", "formal_credit",
        "source_W_formal_remainder", "source_W_transition_authorized",
        "publication_authorized", "terminal_replay_completed", "CM2",
        "object_sha256",
    } and service.get("schema")
        == "cm2.round306c30c.bridge-v5-service-stdout.v1"
        and service.get("status")
        == "READY_WORKER_STDOUT_AWAITING_POST_EXIT_COMPOSITE_FINALIZER"
        and service.get("boundary_object_sha256") == boundary["object_sha256"],
        "service stdout exact boundary closure")
    preflight, _ = read_closed_child(root, "preflight.json", 8 << 20)
    need(preflight.get("schema")
         == "cm2.round306c30c.postreceipt-bridge-v5-preflight.v1"
         and preflight.get("status")
         == "PASS_GATE_RELEASE_RUNNING_PID_BOUND_AND_EXACT_PINS_ZERO_CREDIT"
         and preflight.get("pinset_sha256") == pinset.sha256
         and preflight.get("pinned_role_count") == len(EXPECTED_PIN_ROLES),
         "preflight exact expanded pin role count")
    return {
        "boundary": boundary,
        "boundary_file_sha256": hashlib.sha256(boundary_raw).hexdigest(),
        "service_stdout_object_sha256": service["object_sha256"],
        "service_stdout_file_sha256": hashlib.sha256(service_raw).hexdigest(),
        "preflight_object_sha256": preflight["object_sha256"],
    }


def validate_worker_post_exit_fields(
    fields: Mapping[str, str], anchor_service: Mapping[str, Any],
) -> dict[str, Any]:
    need(type(fields) is dict and set(fields) == set(WORKER_PROPERTIES),
         "worker exact post-exit systemd property set")
    for key in (
        "Id", "InvocationID", "FragmentPath", "LoadState", "Type",
        "RemainAfterExit", "StandardOutput", "StandardError",
    ):
        need(fields.get(key) == anchor_service.get(key),
             "worker post-exit stable field:" + key)
    start = parse_exec_command(fields["ExecStart"], anchor_service["ExecStart"],
                               "worker ExecStart")
    pre = parse_exec_command(fields["ExecStartPre"], anchor_service["ExecStartPre"],
                             "worker ExecStartPre")
    start_projection = completed_exec_projection(start, "worker ExecStart")
    pre_projection = completed_exec_projection(pre, "worker ExecStartPre")
    need(fields.get("ActiveState") == "active"
         and fields.get("SubState") == "exited"
         and fields.get("Result") == "success"
         and fields.get("ExecMainCode") == "1"
         and fields.get("ExecMainStatus") == "0"
         and fields.get("MainPID") == "0" and fields.get("ControlPID") == "0",
         "worker exact clean active/exited terminal tuple")
    return {
        "fields": dict(fields), "execstart": start, "execstartpre": pre,
        "execstart_projection": start_projection,
        "execstartpre_projection": pre_projection,
        "worker_post_exit_success": True,
    }


def validate_worker_post_exit(
    runtime: RuntimeAuthority, anchor_service: Mapping[str, Any],
    fragment: HeldFile,
) -> dict[str, Any]:
    fields, raw = runtime.query(anchor_service["Id"], WORKER_PROPERTIES)
    result = validate_worker_post_exit_fields(fields, anchor_service)
    fragment.verify()
    need(fields["FragmentPath"] == os.fspath(fragment.path)
         and fragment.sha256 == anchor_service["FragmentSHA256"]
         and stat9(fragment.initial) == anchor_service["FragmentStat9"],
         "worker exact held fragment")
    return closed({
        "schema": "cm2.round306c30c.postreceipt-bridge-v5-worker-post-exit-attestation.v1",
        "status": "PASS_WORKER_ACTIVE_EXITED_RESULT_SUCCESS_EXACT_AUTHORITY",
        **result,
        "systemctl_stdout_sha256": hashlib.sha256(raw).hexdigest(),
        "fragment_sha256": fragment.sha256,
        "fragment_stat9": stat9(fragment.initial),
        "formal_credit": 0, "source_W_formal_remainder": 80,
        "source_W_transition_authorized": False,
        "publication_authorized": False, "terminal_replay_completed": False,
        "CM2": "NO-GO_FOR_CLAIM",
    })


def validate_proc_binding(process_pid: int, unit: str) -> dict[str, Any]:
    need(type(process_pid) is int and process_pid == os.getpid() and process_pid > 1,
         "outer proc binding current PID")
    proc = Path("/proc") / str(process_pid)
    exe_link = os.readlink(proc / "exe")
    exe_state = (proc / "exe").stat()
    python_state = FINAL_PYTHON.stat()
    need(exe_link == os.fspath(FINAL_PYTHON)
         and (exe_state.st_dev, exe_state.st_ino)
             == (python_state.st_dev, python_state.st_ino),
         "finalizer /proc exe exact Python inode")
    fd = os.open(
        proc / "cgroup", os.O_RDONLY | os.O_CLOEXEC
        | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        chunks: list[bytes] = []
        total = 0
        while True:
            block = os.read(fd, 4096)
            if not block:
                break
            total += len(block)
            need(total <= 65536, "bounded cgroup projection")
            chunks.append(block)
    finally:
        os.close(fd)
    raw = b"".join(chunks)
    try:
        rows = raw.decode("ascii").splitlines()
    except UnicodeDecodeError as error:
        raise Reject("cgroup ASCII") from error
    need(len(rows) == 1 and rows[0].startswith("0::/")
         and rows[0].endswith("/" + unit), "exact finalizer service cgroup")
    return {
        "pid": process_pid, "proc_exe_link": exe_link,
        "proc_exe_stat9": stat9(exe_state),
        "proc_cgroup_sha256": hashlib.sha256(raw).hexdigest(),
        "proc_cgroup_line": rows[0], "service_cgroup_bound": True,
    }


def validate_finalizer_running_fields(
    fields: Mapping[str, str], expected_argv: Sequence[str], finalizer_unit: str,
    invocation_id: str, fragment_path: Path, process_pid: int,
) -> dict[str, Any]:
    need(type(fields) is dict and set(fields) == set(FINALIZER_PROPERTIES),
         "finalizer exact running systemd property set")
    need(fields.get("Id") == finalizer_unit
         and fields.get("InvocationID") == invocation_id
         and INVOCATION.fullmatch(invocation_id) is not None,
         "finalizer unit/invocation authority")
    command = parse_exec_command(fields["ExecStart"], expected_argv,
                                 "finalizer ExecStart")
    need(fields.get("FragmentPath") == os.fspath(fragment_path)
         and fields.get("LoadState") == "loaded"
         and fields.get("ActiveState") == "active"
         and fields.get("SubState") == "running"
         and fields.get("Result") == "success"
         and fields.get("ExecMainCode") == "0"
         and fields.get("ExecMainStatus") == "0"
         and fields.get("ControlPID") == "0"
         and fields.get("Type") == "exec"
         and fields.get("RemainAfterExit") == "yes"
         and fields.get("StandardOutput") == "journal"
         and fields.get("StandardError") == "journal",
         "finalizer exact running service tuple")
    main_pid = int(fields.get("MainPID", "-1"))
    need(main_pid == command["pid"] == process_pid,
         "MainPID == ExecStart.pid == os.getpid")
    need(command["start_time"] not in {"", "n/a"}
         and command["stop_time"] == "n/a"
         and command["code"] == "(null)"
         and command["status"] in {"0", "0/0"},
         "finalizer live ExecStart projection")
    return {
        "fields": dict(fields), "execstart": command,
        "MainPID": main_pid, "ExecStartPID": command["pid"],
        "outer_process_binding": True,
    }


def validate_finalizer_running(
    runtime: RuntimeAuthority, expected_argv: Sequence[str], finalizer_unit: str,
    invocation_id: str, fragment: HeldFile, process_pid: int,
) -> dict[str, Any]:
    fields, raw = runtime.query(finalizer_unit, FINALIZER_PROPERTIES)
    result = validate_finalizer_running_fields(
        fields, expected_argv, finalizer_unit, invocation_id, fragment.path,
        process_pid,
    )
    fragment.verify()
    proc = validate_proc_binding(process_pid, finalizer_unit)
    return closed({
        "schema": RUNNING_SCHEMA,
        "status": "PASS_FINALIZER_RUNNING_MAINPID_EXECSTARTPID_PROC_CGROUP_BOUND",
        **result, "outer_proc_binding": proc,
        "systemctl_stdout_sha256": hashlib.sha256(raw).hexdigest(),
        "fragment_sha256": fragment.sha256,
        "fragment_stat9": stat9(fragment.initial),
        "formal_credit": 0, "source_W_formal_remainder": 80,
        "source_W_transition_authorized": False,
        "publication_authorized": False, "terminal_replay_completed": False,
        "CM2": "NO-GO_FOR_CLAIM",
    })


def validate_finalizer_post_exit_fields(
    fields: Mapping[str, str], expected: Mapping[str, Any],
) -> dict[str, Any]:
    need(type(fields) is dict and set(fields) == set(FINALIZER_PROPERTIES),
         "finalizer exact post-exit systemd property set")
    need(set(expected) == {
        "Id", "InvocationID", "ExecStart", "FragmentPath", "FragmentSHA256",
        "FragmentStat9", "LoadState", "ActiveState", "SubState", "Result",
        "ExecMainCode", "ExecMainStatus", "MainPID", "ControlPID", "Type",
        "RemainAfterExit", "StandardOutput", "StandardError",
    } and HEX64.fullmatch(expected.get("FragmentSHA256", "")) is not None,
         "exact finalizer post-exit contract shape")
    validate_stat9(expected.get("FragmentStat9"), "post-exit finalizer fragment")
    for key in (
        "Id", "InvocationID", "FragmentPath", "LoadState", "Type",
        "RemainAfterExit", "StandardOutput", "StandardError",
    ):
        need(fields.get(key) == expected.get(key),
             "finalizer post-exit stable field:" + key)
    command = parse_exec_command(fields["ExecStart"], expected["ExecStart"],
                                 "post-exit finalizer ExecStart")
    projection = completed_exec_projection(command, "post-exit finalizer ExecStart")
    need(fields.get("ActiveState") == "active"
         and fields.get("SubState") == "exited"
         and fields.get("Result") == "success"
         and fields.get("ExecMainCode") == "1"
         and fields.get("ExecMainStatus") == "0"
         and fields.get("MainPID") == "0" and fields.get("ControlPID") == "0",
         "finalizer required post-marker unit success")
    return {
        "fields": dict(fields), "execstart": command,
        "execstart_projection": projection,
        "finalizer_post_exit_success": True,
    }


def validate_composite_receipt(value: Mapping[str, Any]) -> None:
    need(type(value) is dict and set(value) == COMPOSITE_RECEIPT_FIELDS,
         "exact composite receipt field set")
    verify_closure(value, "exact composite receipt")
    zero_contract(value, "exact composite receipt")
    need(value.get("schema") == COMPOSITE_SCHEMA
         and value.get("status") == (
             "FILESYSTEM_COMPOSITE_PREPARED__JOINT_AUTHORITY_PENDING_"
             "FINALIZER_POST_EXIT_SUCCESS"
         ), "exact composite receipt schema/status")
    need(type(value.get("token")) is str
         and TOKEN.fullmatch(value["token"]) is not None
         and type(value.get("worker_unit")) is str
         and INVOCATION.fullmatch(value.get("worker_InvocationID", "")) is not None
         and type(value.get("worker_FragmentPath")) is str,
         "composite receipt worker identity types")
    token = value["token"]
    bridge = AUDIT / ("c30c-postreceipt-v3-p1-bridge-v5-" + token)
    control = CONTROL / bridge.name
    worker_unit = "cm2-c30c-postreceipt-v3-p1-bridge-v5-" + token + ".service"
    finalizer_unit = (
        "cm2-c30c-postreceipt-v3-p1-bridge-v5-finalizer-" + token + ".service"
    )
    need(value["worker_unit"] == worker_unit,
         "composite receipt same-token worker unit")
    for key in (
        "worker_post_exit_attestation_object_sha256",
        "worker_ready_tree_attestation_object_sha256",
        "terminal_boundary_object_sha256", "anchor_file_sha256",
        "anchor_object_sha256", "pinset_file_sha256", "pinset_object_sha256",
        "finalizer_source_sha256", "running_attestation_file_sha256",
        "running_attestation_object_sha256", "composite_marker_sha256",
    ):
        need(HEX64.fullmatch(value.get(key, "")) is not None,
             "composite receipt SHA:" + key)
    for key in (
        "finalizer_source_stat9", "running_attestation_stat9",
        "prepared_marker_stat9",
    ):
        validate_stat9(value.get(key), "composite receipt:" + key)
    need(value.get("pinned_role_count") == len(EXPECTED_PIN_ROLES)
         and value.get("running_attestation_name") == RUNNING_ATTESTATION_NAME
         and value.get("composite_marker_name") == COMPOSITE_MARKER_NAME
         and value.get("composite_marker_sha256")
             == hashlib.sha256(COMPOSITE_PASS_BYTES).hexdigest()
         and value.get("marker_commit_method") == (
             "PREPARED_FSYNCED_SINGLETON_THEN_RENAMEAT2_NOREPLACE_"
             "AS_LAST_FS_MUTATION_THEN_PARENT_FSYNC_THEN_OS__EXIT_0"
         )
         and value.get("filesystem_marker_authoritative") is False
         and value.get("orphan_READY_authority_eligible") is False
         and value.get("orphan_COMPOSITE_PASS_authority_eligible") is False
         and value.get("joint_authority_requires_post_exit_query") is True,
         "composite receipt exact authority flags")
    expected = value.get("required_finalizer_post_exit")
    need(type(expected) is dict, "composite receipt post-exit contract")
    expected_argv = expected.get("ExecStart")
    need(type(expected_argv) is list and len(expected_argv) == 20
         and type(expected_argv[-1]) is str and expected_argv[-1].isdigit(),
         "composite receipt exact finalizer20 shape")
    maximum_wait = int(expected_argv[-1])
    need(expected.get("Id") == finalizer_unit
         and expected.get("FragmentPath")
             == f"/run/user/{UID}/systemd/transient/{finalizer_unit}"
         and expected_argv == expected_execstart_argv(
             bridge, control / "pinset.json", control / "launch-anchor.json",
             worker_unit, finalizer_unit, maximum_wait,
             value["finalizer_source_sha256"],
         ), "composite receipt same-token exact held finalizer20")
    need(stat.S_IMODE(value["finalizer_source_stat9"]["mode"]) == 0o444
         and value.get("authority_definition") == (
             "EXACT_READY_TREE_AND_WORKER_POST_EXIT_SUCCESS_PLUS_"
             "COMPOSITE_RECEIPT_AND_MARKER_PLUS_FRESH_FINALIZER_"
             "POST_EXIT_UNIT_INVOCATION_EXECSTART_FRAGMENT_SUCCESS"
         ), "composite receipt source freeze/authority definition")
    # Shape/SHA/stat validation is independent of a future observed service.
    validate_finalizer_post_exit_fields({
        "Id": expected.get("Id", ""),
        "InvocationID": expected.get("InvocationID", ""),
        "ExecStart": exec_raw(expected.get("ExecStart", []), pid=2, running=False)
            if type(expected.get("ExecStart")) is list else "",
        "FragmentPath": expected.get("FragmentPath", ""),
        "LoadState": expected.get("LoadState", ""),
        "ActiveState": expected.get("ActiveState", ""),
        "SubState": expected.get("SubState", ""),
        "Result": expected.get("Result", ""),
        "ExecMainCode": expected.get("ExecMainCode", ""),
        "ExecMainStatus": expected.get("ExecMainStatus", ""),
        "MainPID": expected.get("MainPID", ""),
        "ControlPID": expected.get("ControlPID", ""),
        "Type": expected.get("Type", ""),
        "RemainAfterExit": expected.get("RemainAfterExit", ""),
        "StandardOutput": expected.get("StandardOutput", ""),
        "StandardError": expected.get("StandardError", ""),
    }, expected)


def validate_running_attestation(value: Mapping[str, Any]) -> None:
    need(type(value) is dict and set(value) == RUNNING_ATTESTATION_FIELDS,
         "exact running attestation field set")
    verify_closure(value, "exact running attestation")
    zero_contract(value, "exact running attestation")
    need(value.get("schema") == RUNNING_SCHEMA
         and value.get("status")
             == "PASS_COMPOSITE_FINALIZER_RUNNING_EXACT_OUTER_PROCESS"
         and type(value.get("token")) is str
         and TOKEN.fullmatch(value["token"]) is not None,
         "running attestation schema/status/token")
    token = value["token"]
    need(value.get("worker_unit")
         == f"cm2-c30c-postreceipt-v3-p1-bridge-v5-{token}.service"
         and value.get("finalizer_unit")
         == f"cm2-c30c-postreceipt-v3-p1-bridge-v5-finalizer-{token}.service",
         "running attestation same-token units")
    for key in (
        "anchor_file_sha256", "anchor_object_sha256", "pinset_file_sha256",
        "finalizer_source_sha256", "terminal_boundary_object_sha256",
    ):
        need(HEX64.fullmatch(value.get(key, "")) is not None,
             "running attestation SHA:" + key)
    need(value.get("filesystem_marker_authoritative") is False
         and value.get("joint_authority_requires_post_exit_query") is True,
         "running attestation joint flags")
    for key in (
        "worker_post_exit_attestation", "finalizer_running_attestation",
        "worker_ready_tree_attestation",
    ):
        nested = value.get(key)
        need(type(nested) is dict, "running nested object:" + key)
        verify_closure(nested, "running nested object:" + key)
        zero_contract(nested, "running nested object:" + key)
    worker = value["worker_post_exit_attestation"]
    finalizer = value["finalizer_running_attestation"]
    ready = value["worker_ready_tree_attestation"]
    need(worker.get("schema")
         == "cm2.round306c30c.postreceipt-bridge-v5-worker-post-exit-attestation.v1"
         and worker.get("status")
         == "PASS_WORKER_ACTIVE_EXITED_RESULT_SUCCESS_EXACT_AUTHORITY"
         and worker.get("worker_post_exit_success") is True,
         "running nested worker post-exit attestation")
    need(finalizer.get("schema") == RUNNING_SCHEMA
         and finalizer.get("status")
         == "PASS_FINALIZER_RUNNING_MAINPID_EXECSTARTPID_PROC_CGROUP_BOUND"
         and finalizer.get("outer_process_binding") is True,
         "running nested finalizer live attestation")
    need(ready.get("schema")
         == "cm2.round306c30c.postreceipt-bridge-v5-ready-tree-attestation.v1"
         and ready.get("status")
         == "PASS_EXACT_WORKER_READY_TREE__READY_NON_AUTHORITATIVE"
         and ready.get("ready_marker_authoritative") is False,
         "running nested worker READY attestation")


def post_exit_tuple_eligible(
    marker_bytes: bytes | None, receipt: Mapping[str, Any] | None,
    finalizer_fields: Mapping[str, str] | None,
    fragment_observation: Mapping[str, Any] | None,
) -> bool:
    """Non-authoritative tuple subgate used only inside the full tree replay."""
    try:
        need(marker_bytes == COMPOSITE_PASS_BYTES, "exact composite marker")
        validate_composite_receipt(receipt)
        expected = receipt.get("required_finalizer_post_exit")
        need(type(expected) is dict and type(finalizer_fields) is dict,
             "post-exit expected/observed objects")
        validate_finalizer_post_exit_fields(finalizer_fields, expected)
        need(type(fragment_observation) is dict
             and fragment_observation.get("path") == expected["FragmentPath"]
             and fragment_observation.get("sha256") == expected["FragmentSHA256"]
             and fragment_observation.get("stat9") == expected["FragmentStat9"],
             "fresh post-exit finalizer fragment replay")
        return True
    except (Reject, KeyError, TypeError, ValueError):
        return False


def validate_post_exit_joint_authority(
    root: HeldDir, runtime: RuntimeAuthority,
) -> dict[str, Any]:
    """Read-only downstream verifier; call only after the finalizer has exited."""
    marker_raw, marker_stat = root.open_regular(COMPOSITE_MARKER_NAME, 256)
    receipt_raw, _receipt_stat = root.open_regular(COMPOSITE_RECEIPT_NAME, 16 << 20)
    receipt = strict_json(receipt_raw, "post-exit composite receipt")
    validate_composite_receipt(receipt)
    running_raw, running_stat = root.open_regular(
        RUNNING_ATTESTATION_NAME, 64 << 20,
    )
    running = strict_json(running_raw, "post-exit running attestation")
    validate_running_attestation(running)
    need(receipt.get("running_attestation_file_sha256")
         == hashlib.sha256(running_raw).hexdigest()
         and receipt.get("running_attestation_stat9") == running_stat
         and receipt.get("running_attestation_object_sha256")
             == running["object_sha256"]
         and receipt.get("composite_marker_sha256")
             == hashlib.sha256(marker_raw).hexdigest()
         and marker_raw == COMPOSITE_PASS_BYTES
         and stable_rename_identity(receipt["prepared_marker_stat9"])
             == stable_rename_identity(marker_stat),
         "post-exit marker/receipt/running-attestation closure")
    ready_tree = validate_ready_tree(root, frozenset({
        RUNNING_ATTESTATION_NAME, COMPOSITE_RECEIPT_NAME,
        COMPOSITE_MARKER_NAME,
    }))
    expected = receipt.get("required_finalizer_post_exit")
    need(type(expected) is dict, "post-exit finalizer contract")
    token = receipt["token"]
    bridge_path = AUDIT / ("c30c-postreceipt-v3-p1-bridge-v5-" + token)
    control = CONTROL / bridge_path.name
    worker_unit = receipt["worker_unit"]
    finalizer_unit = expected["Id"]
    need(root.path == bridge_path, "joint gate exact same-token bridge root")
    source = HeldFile(SELF, "joint finalizer source", 8 << 20)
    anchor_file = HeldFile(control / "launch-anchor.json", "joint anchor", 8 << 20)
    pinset = HeldFile(control / "pinset.json", "joint pinset", 16 << 20)
    worker_fragment: HeldFile | None = None
    finalizer_fragment: HeldFile | None = None
    try:
        executed_source = {
            "path": os.fspath(source.path), "sha256": source.sha256,
            "stat9": stat9(source.initial),
        }
        need(source.sha256 == receipt["finalizer_source_sha256"]
             and stat9(source.initial) == receipt["finalizer_source_stat9"]
             and anchor_file.sha256 == receipt["anchor_file_sha256"]
             and pinset.sha256 == receipt["pinset_file_sha256"],
             "joint source/anchor/pinset file pins")
        anchor = parse_anchor(anchor_file, root, pinset, worker_unit)
        pinset_object, observations = parse_pinset(
            pinset, anchor, executed_source,
        )
        need(anchor["object_sha256"] == receipt["anchor_object_sha256"]
             and pinset_object["object_sha256"] == receipt["pinset_object_sha256"]
             and len(observations) == receipt["pinned_role_count"]
             and receipt["worker_InvocationID"]
                 == anchor["bridge_service"]["InvocationID"]
             and receipt["worker_FragmentPath"]
                 == anchor["bridge_service"]["FragmentPath"],
             "joint anchor/pinset object closures")
        documents = validate_ready_documents(
            root, anchor, anchor_file.sha256, pinset, finalizer_unit,
            executed_source,
        )
        maximum_wait = int(expected["ExecStart"][-1])
        need(type(anchor["bridge_service"]["ExecStart"][-1]) is str
             and anchor["bridge_service"]["ExecStart"][-1].isdigit()
             and int(anchor["bridge_service"]["ExecStart"][-1]) == maximum_wait,
             "joint worker/finalizer maximum-wait closure")
        worker_fragment = HeldFile(
            Path(anchor["bridge_service"]["FragmentPath"]),
            "joint worker fragment", 1 << 20,
        )
        finalizer_fragment = HeldFile(
            Path(expected["FragmentPath"]), "joint finalizer fragment", 1 << 20,
        )
        worker_exit = validate_worker_post_exit(
            runtime, anchor["bridge_service"], worker_fragment,
        )
        fields, systemctl_raw = runtime.query(finalizer_unit, FINALIZER_PROPERTIES)
        observed = {
            "path": os.fspath(finalizer_fragment.path),
            "sha256": finalizer_fragment.sha256,
            "stat9": stat9(finalizer_fragment.initial),
        }
        need(post_exit_tuple_eligible(
            marker_raw, receipt, fields, observed,
        ), "joint post-exit authority gate")
        need(receipt["worker_post_exit_attestation_object_sha256"]
             == running["worker_post_exit_attestation"]["object_sha256"]
             and receipt["worker_ready_tree_attestation_object_sha256"]
             == ready_tree["object_sha256"]
             == running["worker_ready_tree_attestation"]["object_sha256"]
             and receipt["terminal_boundary_object_sha256"]
             == documents["boundary"]["object_sha256"]
             == running["terminal_boundary_object_sha256"]
             and running["anchor_file_sha256"] == anchor_file.sha256
             and running["anchor_object_sha256"] == anchor["object_sha256"]
             and running["pinset_file_sha256"] == pinset.sha256
             and running["finalizer_source_sha256"] == source.sha256
             and running["token"] == token
             and running["worker_unit"] == worker_unit
             and running["finalizer_unit"] == finalizer_unit,
             "joint receipt/running/material exact digest closure")
        historical_finalizer = running["finalizer_running_attestation"]
        historical_worker = running["worker_post_exit_attestation"]
        need(historical_finalizer.get("fragment_sha256")
             == expected["FragmentSHA256"]
             and historical_finalizer.get("fragment_stat9")
             == expected["FragmentStat9"]
             and historical_finalizer.get("fields", {}).get("Id")
             == finalizer_unit
             and historical_finalizer.get("fields", {}).get("InvocationID")
             == expected["InvocationID"]
             and historical_finalizer.get("fields", {}).get("FragmentPath")
             == expected["FragmentPath"]
             and historical_finalizer.get("execstart", {}).get("argv")
             == expected["ExecStart"]
             and historical_worker.get("fields", {}).get("Id") == worker_unit
             and historical_worker.get("fields", {}).get("InvocationID")
             == anchor["bridge_service"]["InvocationID"]
             and historical_worker.get("fields", {}).get("FragmentPath")
             == anchor["bridge_service"]["FragmentPath"]
             and historical_worker.get("fragment_sha256")
             == anchor["bridge_service"]["FragmentSHA256"]
             and historical_worker.get("fragment_stat9")
             == anchor["bridge_service"]["FragmentStat9"]
             and worker_exit.get("worker_post_exit_success") is True,
             "joint historical-running/current-worker/finalizer contract")
        for held in (
            source, anchor_file, pinset, worker_fragment, finalizer_fragment,
        ):
            held.verify()
        runtime.verify()
        root.verify()
        return closed({
            "schema": (
                "cm2.round306c30c.postreceipt-bridge-v5-"
                "composite-joint-authority-attestation.v1"
            ),
            "status": "PASS_JOINT_FILESYSTEM_AND_FINALIZER_POST_EXIT_GATE_ZERO_CREDIT",
            "composite_receipt_object_sha256": receipt["object_sha256"],
            "running_attestation_object_sha256": running["object_sha256"],
            "finalizer_unit": expected["Id"],
            "finalizer_InvocationID": expected["InvocationID"],
            "worker_post_exit_attestation_object_sha256":
                worker_exit["object_sha256"],
            "finalizer_fragment_sha256": finalizer_fragment.sha256,
            "systemctl_stdout_sha256": hashlib.sha256(systemctl_raw).hexdigest(),
            "worker_ready_tree_attestation_object_sha256":
                ready_tree["object_sha256"],
            "filesystem_marker_authoritative_alone": False,
            "joint_gate_observed": True,
            "formal_credit": 0, "source_W_formal_remainder": 80,
            "source_W_transition_authorized": False,
            "publication_authorized": False, "terminal_replay_completed": False,
            "CM2": "NO-GO_FOR_CLAIM",
        })
    finally:
        for held in (
            finalizer_fragment, worker_fragment, pinset, anchor_file, source,
        ):
            if held is not None:
                held.close()


def assert_tree_extension(
    root: HeldDir, baseline: Mapping[str, Mapping[str, Any]],
    extras: set[str],
) -> dict[str, dict[str, Any]]:
    current = snapshot_tree(root)
    need(set(current) == set(baseline) | extras, "exact finalizer tree extension")
    for path, row in baseline.items():
        if path == ".":
            need(stable_dir_identity(row["stat9"])
                 == stable_dir_identity(current[path]["stat9"]),
                 "finalizer root stable identity")
        else:
            need(current[path] == row,
                 "worker READY member stable through finalizer:" + path)
    return current


def rename_noreplace(root: HeldDir, source: str, target: str) -> None:
    need(all(name and "/" not in name and name not in {".", ".."}
             for name in (source, target)), "direct rename tokens")
    libc = ctypes.CDLL(None, use_errno=True)
    renameat2 = libc.renameat2
    renameat2.argtypes = [
        ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p,
        ctypes.c_uint,
    ]
    renameat2.restype = ctypes.c_int
    result = renameat2(
        root.fd, source.encode("ascii"), root.fd, target.encode("ascii"), 1,
    )
    if result != 0:
        number = ctypes.get_errno()
        raise OSError(number, os.strerror(number))


def publish_composite_marker_last(
    root: HeldDir, terminate: bool,
    fsyncer: Callable[[int], None] = os.fsync,
) -> None:
    """Rename is the last mutation; parent fsync is the final durability gate."""
    rename_noreplace(root, PREPARED_COMPOSITE, COMPOSITE_MARKER_NAME)
    fsyncer(root.fd)
    if terminate:
        os._exit(0)


def required_post_exit_contract(
    running: Mapping[str, Any], expected_argv: Sequence[str],
) -> dict[str, Any]:
    fields = running["fields"]
    return {
        "Id": fields["Id"], "InvocationID": fields["InvocationID"],
        "ExecStart": list(expected_argv), "FragmentPath": fields["FragmentPath"],
        "FragmentSHA256": running["fragment_sha256"],
        "FragmentStat9": running["fragment_stat9"],
        "LoadState": "loaded", "ActiveState": "active", "SubState": "exited",
        "Result": "success", "ExecMainCode": "1", "ExecMainStatus": "0",
        "MainPID": "0", "ControlPID": "0", "Type": "exec",
        "RemainAfterExit": "yes", "StandardOutput": "journal",
        "StandardError": "journal",
    }


def run_finalizer(
    bridge_path: Path, pinset_path: Path, anchor_path: Path,
    worker_unit: str, finalizer_unit: str, maximum_wait: int,
    executed_source: Mapping[str, Any], reverify_source: Callable[[], None],
) -> None:
    bridge_path, pinset_path, anchor_path, token = material_paths(
        bridge_path, pinset_path, anchor_path, worker_unit, finalizer_unit,
        maximum_wait,
    )
    invocation_id = os.environ.get("INVOCATION_ID", "")
    need(INVOCATION.fullmatch(invocation_id) is not None,
         "finalizer authoritative INVOCATION_ID environment")
    expected_argv = expected_execstart_argv(
        bridge_path, pinset_path, anchor_path, worker_unit, finalizer_unit,
        maximum_wait, executed_source["sha256"],
    )
    bridge = HeldDir(bridge_path, "worker READY bridge")
    pinset = HeldFile(pinset_path, "v5 pinset", 16 << 20)
    anchor_file = HeldFile(anchor_path, "v5 anchor", 8 << 20)
    runtime = RuntimeAuthority()
    worker_fragment: HeldFile | None = None
    finalizer_fragment: HeldFile | None = None
    marker_prepared = False
    try:
        need(set(bridge.names()).isdisjoint({
            PREPARED_COMPOSITE, RUNNING_ATTESTATION_NAME,
            COMPOSITE_RECEIPT_NAME, COMPOSITE_MARKER_NAME,
            "FAILED.lock", "failure_receipt.json", "PASS.lock",
        }), "fresh fail-closed composite namespace")
        anchor = parse_anchor(anchor_file, bridge, pinset, worker_unit)
        _pinset_object, observations = parse_pinset(
            pinset, anchor, executed_source,
        )
        ready_tree = validate_ready_tree(bridge)
        documents = validate_ready_documents(
            bridge, anchor, anchor_file.sha256, pinset, finalizer_unit,
            executed_source,
        )
        baseline = snapshot_tree(bridge)
        worker_fragment = HeldFile(
            Path(anchor["bridge_service"]["FragmentPath"]),
            "worker fragment", 1 << 20,
        )
        finalizer_fragment_path = Path(
            f"/run/user/{UID}/systemd/transient/{finalizer_unit}"
        )
        finalizer_fragment = HeldFile(
            finalizer_fragment_path, "finalizer fragment", 1 << 20,
        )
        worker_exit = validate_worker_post_exit(
            runtime, anchor["bridge_service"], worker_fragment,
        )
        finalizer_running = validate_finalizer_running(
            runtime, expected_argv, finalizer_unit, invocation_id,
            finalizer_fragment, os.getpid(),
        )
        need(observations["bridge_composite_finalizer"]["sha256"]
             == executed_source["sha256"], "finalizer source role replay")

        # Prepare and durably close the marker inode before any composite
        # object.  Only its no-replace rename is left for the last mutation.
        prepared_stat = bridge.write_once(PREPARED_COMPOSITE, COMPOSITE_PASS_BYTES)
        marker_prepared = True
        assert_tree_extension(bridge, baseline, {PREPARED_COMPOSITE})
        pinset.verify()
        anchor_file.verify()
        worker_fragment.verify()
        finalizer_fragment.verify()
        parse_pinset(pinset, anchor, executed_source)
        worker_exit = validate_worker_post_exit(
            runtime, anchor["bridge_service"], worker_fragment,
        )
        finalizer_running = validate_finalizer_running(
            runtime, expected_argv, finalizer_unit, invocation_id,
            finalizer_fragment, os.getpid(),
        )

        running_attestation = closed({
            "schema": RUNNING_SCHEMA,
            "status": "PASS_COMPOSITE_FINALIZER_RUNNING_EXACT_OUTER_PROCESS",
            "token": token, "worker_unit": worker_unit,
            "finalizer_unit": finalizer_unit,
            "anchor_file_sha256": anchor_file.sha256,
            "anchor_object_sha256": anchor["object_sha256"],
            "pinset_file_sha256": pinset.sha256,
            "finalizer_source_sha256": executed_source["sha256"],
            "worker_post_exit_attestation": worker_exit,
            "finalizer_running_attestation": finalizer_running,
            "worker_ready_tree_attestation": ready_tree,
            "terminal_boundary_object_sha256": documents["boundary"]["object_sha256"],
            "filesystem_marker_authoritative": False,
            "joint_authority_requires_post_exit_query": True,
            "formal_credit": 0, "source_W_formal_remainder": 80,
            "source_W_transition_authorized": False,
            "publication_authorized": False, "terminal_replay_completed": False,
            "CM2": "NO-GO_FOR_CLAIM",
        })
        validate_running_attestation(running_attestation)
        running_stat = bridge.write_json(
            RUNNING_ATTESTATION_NAME, running_attestation,
        )
        running_raw, _ = bridge.open_regular(RUNNING_ATTESTATION_NAME, 16 << 20)
        assert_tree_extension(
            bridge, baseline, {PREPARED_COMPOSITE, RUNNING_ATTESTATION_NAME},
        )

        post_exit_contract = required_post_exit_contract(
            finalizer_running, expected_argv,
        )
        receipt = closed({
            "schema": COMPOSITE_SCHEMA,
            "status": (
                "FILESYSTEM_COMPOSITE_PREPARED__JOINT_AUTHORITY_PENDING_"
                "FINALIZER_POST_EXIT_SUCCESS"
            ),
            "token": token, "worker_unit": worker_unit,
            "worker_InvocationID": anchor["bridge_service"]["InvocationID"],
            "worker_FragmentPath": anchor["bridge_service"]["FragmentPath"],
            "worker_post_exit_attestation_object_sha256": worker_exit["object_sha256"],
            "worker_ready_tree_attestation_object_sha256": ready_tree["object_sha256"],
            "terminal_boundary_object_sha256": documents["boundary"]["object_sha256"],
            "anchor_file_sha256": anchor_file.sha256,
            "anchor_object_sha256": anchor["object_sha256"],
            "pinset_file_sha256": pinset.sha256,
            "pinset_object_sha256": _pinset_object["object_sha256"],
            "pinned_role_count": len(observations),
            "finalizer_source_sha256": executed_source["sha256"],
            "finalizer_source_stat9": executed_source["stat9"],
            "running_attestation_name": RUNNING_ATTESTATION_NAME,
            "running_attestation_file_sha256": hashlib.sha256(running_raw).hexdigest(),
            "running_attestation_stat9": running_stat,
            "running_attestation_object_sha256": running_attestation["object_sha256"],
            "composite_marker_name": COMPOSITE_MARKER_NAME,
            "composite_marker_sha256": hashlib.sha256(COMPOSITE_PASS_BYTES).hexdigest(),
            "prepared_marker_stat9": prepared_stat,
            "marker_commit_method": (
                "PREPARED_FSYNCED_SINGLETON_THEN_RENAMEAT2_NOREPLACE_"
                "AS_LAST_FS_MUTATION_THEN_PARENT_FSYNC_THEN_OS__EXIT_0"
            ),
            "filesystem_marker_authoritative": False,
            "orphan_READY_authority_eligible": False,
            "orphan_COMPOSITE_PASS_authority_eligible": False,
            "joint_authority_requires_post_exit_query": True,
            "required_finalizer_post_exit": post_exit_contract,
            "authority_definition": (
                "EXACT_READY_TREE_AND_WORKER_POST_EXIT_SUCCESS_PLUS_"
                "COMPOSITE_RECEIPT_AND_MARKER_PLUS_FRESH_FINALIZER_"
                "POST_EXIT_UNIT_INVOCATION_EXECSTART_FRAGMENT_SUCCESS"
            ),
            "formal_credit": 0, "source_W_formal_remainder": 80,
            "source_W_transition_authorized": False,
            "publication_authorized": False, "terminal_replay_completed": False,
            "CM2": "NO-GO_FOR_CLAIM",
        })
        validate_composite_receipt(receipt)
        bridge.write_json(COMPOSITE_RECEIPT_NAME, receipt)
        final_extras = {
            PREPARED_COMPOSITE, RUNNING_ATTESTATION_NAME, COMPOSITE_RECEIPT_NAME,
        }
        assert_tree_extension(bridge, baseline, final_extras)

        # Final fail-closed replay.  Source/pin/service/tree FDs remain held
        # through the marker and are closed only by kernel teardown after
        # os._exit(0), eliminating a post-custody verification window.
        pinset.verify()
        anchor_file.verify()
        worker_fragment.verify()
        finalizer_fragment.verify()
        parse_pinset(pinset, anchor, executed_source)
        validate_worker_post_exit(runtime, anchor["bridge_service"], worker_fragment)
        validate_finalizer_running(
            runtime, expected_argv, finalizer_unit, invocation_id,
            finalizer_fragment, os.getpid(),
        )
        assert_tree_extension(bridge, baseline, final_extras)
        reverify_source()
        bridge.verify()

        # No Python statement capable of a filesystem mutation follows a
        # successful production rename.  Kernel FD teardown follows _exit(0).
        publish_composite_marker_last(bridge, terminate=True)
        raise Reject("unreachable after composite marker")
    finally:
        # The production success path never reaches finally because os._exit
        # terminates immediately.  Every error path lacks COMPOSITE_PASS.lock.
        for resource in (runtime, worker_fragment, finalizer_fragment,
                         pinset, anchor_file, bridge):
            if resource is not None:
                try:
                    resource.close()
                except OSError:
                    pass
        if marker_prepared:
            # Intentionally append-only: a failed attempt may leave only the
            # hidden prepared marker and pre-marker evidence, never PASS.
            pass


def rejected(call: Callable[[], Any], label: str) -> str:
    try:
        call()
    except (Reject, OSError, ValueError, KeyError, TypeError):
        return "rejected:" + label
    raise Reject("negative fixture accepted:" + label)


def exec_raw(argv: Sequence[str], *, pid: int, running: bool) -> str:
    start = "Sun 2026-08-09 00:00:00 UTC"
    stop = "n/a" if running else "Sun 2026-08-09 00:00:01 UTC"
    code = "(null)" if running else "exited"
    return (
        "{ path=/usr/bin/python3.12 ; argv[]=" + " ".join(argv)
        + " ; ignore_errors=no ; start_time=[" + start + "] ; stop_time=["
        + stop + "] ; pid=" + str(pid) + " ; code=" + code
        + " ; status=0 }"
    )


def self_test() -> dict[str, Any]:
    fake_bridge = AUDIT / "c30c-postreceipt-v3-p1-bridge-v5-selftest"
    fake_control = CONTROL / fake_bridge.name
    worker_unit = "cm2-c30c-postreceipt-v3-p1-bridge-v5-selftest.service"
    finalizer_unit = "cm2-c30c-postreceipt-v3-p1-bridge-v5-finalizer-selftest.service"
    source_sha = "1" * 64
    argv = expected_execstart_argv(
        fake_bridge, fake_control / "pinset.json",
        fake_control / "launch-anchor.json", worker_unit, finalizer_unit, 17,
        source_sha,
    )
    need(len(argv) == 20
         and exact_systemd_show_argv(argv, "selftest") == argv,
         "20-token held bootstrap argv roundtrip")
    need((stat.S_IFREG | 0o444) & 61440 == stat.S_IFREG
         and not (set(FINALIZER_BOOTSTRAP.encode("ascii")) & SYSTEMD_SHOW_FORBIDDEN)
         and all(0x21 <= byte <= 0x7e
                 for byte in FINALIZER_BOOTSTRAP.encode("ascii")),
         "held bootstrap shell-neutral source predicate")

    worker_anchor = {
        "Id": worker_unit, "InvocationID": "2" * 32,
        "ExecStart": argv, "ExecStartPre": argv,
        "FragmentPath": f"/run/user/1000/systemd/transient/{worker_unit}",
        "LoadState": "loaded", "Type": "exec", "RemainAfterExit": "yes",
        "StandardOutput": "journal", "StandardError": "journal",
    }
    worker_fields = {
        **worker_anchor,
        "ExecStart": exec_raw(argv, pid=1111, running=False),
        "ExecStartPre": exec_raw(argv, pid=1110, running=False),
        "ActiveState": "active", "SubState": "exited", "Result": "success",
        "ExecMainCode": "1", "ExecMainStatus": "0", "MainPID": "0",
        "ControlPID": "0",
    }
    validate_worker_post_exit_fields(worker_fields, worker_anchor)
    failed_worker = dict(worker_fields)
    failed_worker["Result"] = "exit-code"
    failed_worker["ExecMainStatus"] = "7"
    attacks = {
        "worker_failure": rejected(
            lambda: validate_worker_post_exit_fields(failed_worker, worker_anchor),
            "worker failure",
        ),
    }
    attacks["boundary_anchor_sha_substitution"] = rejected(
        lambda: exact_file_sha("5" * 64, "6" * 64, "boundary fixture"),
        "boundary anchor SHA substitution",
    )
    runtime_base = {
        "dev": 1, "ino": 2, "mode": stat.S_IFDIR | 0o700, "nlink": 3,
        "uid": UID, "gid": UID, "size": 4096, "mtime_ns": 10,
        "ctime_ns": 11,
    }
    runtime_metadata_churn = {
        **runtime_base, "nlink": 99, "size": 8192, "mtime_ns": 20,
        "ctime_ns": 21,
    }
    need(runtime_directory_identity_allowed(runtime_base, runtime_metadata_churn),
         "shared runtime mutable metadata accepted")
    runtime_substitution = {**runtime_metadata_churn, "ino": 999}
    attacks["runtime_directory_inode_substitution"] = rejected(
        lambda: need(runtime_directory_identity_allowed(
            runtime_base, runtime_substitution,
        ), "runtime directory inode substitution"),
        "runtime directory inode substitution",
    )
    ready_rows_before = {
        ".": {"path": ".", "type": "directory", "stat9": runtime_base},
        "READY.lock": {
            "path": "READY.lock", "type": "regular", "sha256": "7" * 64,
            "stat9": {**runtime_base, "mode": stat.S_IFREG | 0o400},
        },
    }
    ready_rows_after = {
        **ready_rows_before,
        ".": {
            "path": ".", "type": "directory",
            "stat9": runtime_metadata_churn,
        },
    }
    need(stable_ready_tree_sha256(ready_rows_before)
         == stable_ready_tree_sha256(ready_rows_after),
         "READY attestation stable across composite root metadata extension")
    ready_inode_swap = {
        **ready_rows_after,
        ".": {
            "path": ".", "type": "directory",
            "stat9": runtime_substitution,
        },
    }
    attacks["ready_root_inode_substitution"] = rejected(
        lambda: need(stable_ready_tree_sha256(ready_rows_before)
                     == stable_ready_tree_sha256(ready_inode_swap),
                     "READY root inode substitution"),
        "READY root inode substitution",
    )

    process_pid = os.getpid()
    fragment_path = Path(
        f"/run/user/1000/systemd/transient/{finalizer_unit}"
    )
    running_fields = {
        "Id": finalizer_unit, "InvocationID": "3" * 32,
        "ExecStart": exec_raw(argv, pid=process_pid, running=True),
        "FragmentPath": os.fspath(fragment_path), "LoadState": "loaded",
        "ActiveState": "active", "SubState": "running", "Result": "success",
        "ExecMainCode": "0", "ExecMainStatus": "0",
        "MainPID": str(process_pid), "ControlPID": "0", "Type": "exec",
        "RemainAfterExit": "yes", "StandardOutput": "journal",
        "StandardError": "journal",
    }
    validate_finalizer_running_fields(
        running_fields, argv, finalizer_unit, "3" * 32, fragment_path,
        process_pid,
    )
    wrong_pid = dict(running_fields)
    wrong_pid["MainPID"] = str(process_pid + 1)
    attacks["outer_pid_substitution"] = rejected(
        lambda: validate_finalizer_running_fields(
            wrong_pid, argv, finalizer_unit, "3" * 32, fragment_path,
            process_pid,
        ), "outer PID substitution",
    )

    expected_post = {
        "Id": finalizer_unit, "InvocationID": "3" * 32,
        "ExecStart": argv, "FragmentPath": os.fspath(fragment_path),
        "FragmentSHA256": "4" * 64,
        "FragmentStat9": {key: 1 for key in STAT9_KEYS},
        "LoadState": "loaded", "ActiveState": "active", "SubState": "exited",
        "Result": "success", "ExecMainCode": "1", "ExecMainStatus": "0",
        "MainPID": "0", "ControlPID": "0", "Type": "exec",
        "RemainAfterExit": "yes", "StandardOutput": "journal",
        "StandardError": "journal",
    }
    post_fields = {
        key: value for key, value in expected_post.items()
        if key not in {"FragmentSHA256", "FragmentStat9"}
    }
    post_fields["ExecStart"] = exec_raw(argv, pid=process_pid, running=False)
    validate_finalizer_post_exit_fields(post_fields, expected_post)
    attacks["post_marker_running_not_success"] = rejected(
        lambda: validate_finalizer_post_exit_fields(running_fields, expected_post),
        "post-marker unit still running",
    )

    with tempfile.TemporaryDirectory(
        dir=WORKSPACE / ".cm2-runtime", prefix="c30c-v5-finalizer-selftest-",
    ) as raw_parent:
        parent = Path(raw_parent)
        orphan = parent / "orphan"
        orphan.mkdir(0o700)
        orphan_root = HeldDir(orphan, "orphan READY")
        try:
            orphan_root.write_once("READY.lock", READY_BYTES)
            attacks["orphan_READY"] = rejected(
                lambda: validate_ready_tree(orphan_root), "orphan READY tree",
            )
        finally:
            orphan_root.close()

        no_replace = parent / "no-replace"
        no_replace.mkdir(0o700)
        no_replace_root = HeldDir(no_replace, "marker no-replace")
        try:
            no_replace_root.write_once(PREPARED_COMPOSITE, COMPOSITE_PASS_BYTES)
            no_replace_root.write_once(COMPOSITE_MARKER_NAME, b"ORPHAN\n")
            attacks["marker_no_replace"] = rejected(
                lambda: publish_composite_marker_last(no_replace_root, False),
                "marker no-replace",
            )
            need(no_replace_root.open_regular(COMPOSITE_MARKER_NAME, 128)[0]
                 == b"ORPHAN\n", "no-replace preserves old marker")
        finally:
            no_replace_root.close()

        fsync_fault = parent / "fsync-fault"
        fsync_fault.mkdir(0o700)
        fsync_fault_root = HeldDir(fsync_fault, "marker parent-fsync fault")
        try:
            fsync_fault_root.write_once(PREPARED_COMPOSITE, COMPOSITE_PASS_BYTES)

            def fail_fsync(_fd: int) -> None:
                raise OSError(5, "injected parent fsync fault")

            attacks["commit_parent_fsync_fault"] = rejected(
                lambda: publish_composite_marker_last(
                    fsync_fault_root, False, fail_fsync,
                ), "commit parent fsync fault",
            )
            need(fsync_fault_root.open_regular(COMPOSITE_MARKER_NAME, 256)[0]
                 == COMPOSITE_PASS_BYTES
                 and PREPARED_COMPOSITE not in fsync_fault_root.names(),
                 "fsync fault leaves only non-authoritative orphan marker")
        finally:
            fsync_fault_root.close()

        last = parent / "last"
        last.mkdir(0o700)
        last_root = HeldDir(last, "marker last")
        try:
            last_root.write_once(PREPARED_COMPOSITE, COMPOSITE_PASS_BYTES)
            last_root.write_once(RUNNING_ATTESTATION_NAME, b"{}\n")
            last_root.write_once(COMPOSITE_RECEIPT_NAME, b"{}\n")
            before = last_root.names()
            need(before == sorted({
                PREPARED_COMPOSITE, RUNNING_ATTESTATION_NAME,
                COMPOSITE_RECEIPT_NAME,
            }), "exact pre-marker inventory")
            publish_composite_marker_last(last_root, False)
            need(last_root.names() == sorted({
                COMPOSITE_MARKER_NAME, RUNNING_ATTESTATION_NAME,
                COMPOSITE_RECEIPT_NAME,
            }) and last_root.open_regular(COMPOSITE_MARKER_NAME, 256)[0]
                == COMPOSITE_PASS_BYTES, "marker exact last no-replace rename")
        finally:
            last_root.close()

    minimal_receipt = closed({
        "schema": COMPOSITE_SCHEMA, "filesystem_marker_authoritative": False,
        "joint_authority_requires_post_exit_query": True,
        "required_finalizer_post_exit": expected_post,
        "formal_credit": 0, "source_W_formal_remainder": 80,
        "source_W_transition_authorized": False,
        "publication_authorized": False, "terminal_replay_completed": False,
        "CM2": "NO-GO_FOR_CLAIM",
    })
    attacks["minimal_receipt"] = rejected(
        lambda: need(post_exit_tuple_eligible(
            COMPOSITE_PASS_BYTES, minimal_receipt, post_fields, {
                "path": os.fspath(fragment_path), "sha256": "4" * 64,
                "stat9": expected_post["FragmentStat9"],
            },
        ), "minimal receipt"),
        "minimal receipt",
    )
    fragment_fixture = {
        "path": os.fspath(fragment_path),
        "sha256": expected_post["FragmentSHA256"],
        "stat9": expected_post["FragmentStat9"],
    }
    file_stat_fixture = {key: 1 for key in STAT9_KEYS}
    file_stat_fixture["mode"] = stat.S_IFREG | 0o444
    receipt_fixture = closed({
        "schema": COMPOSITE_SCHEMA,
        "status": (
            "FILESYSTEM_COMPOSITE_PREPARED__JOINT_AUTHORITY_PENDING_"
            "FINALIZER_POST_EXIT_SUCCESS"
        ),
        "token": "selftest", "worker_unit": worker_unit,
        "worker_InvocationID": "2" * 32,
        "worker_FragmentPath": worker_anchor["FragmentPath"],
        "worker_post_exit_attestation_object_sha256": "5" * 64,
        "worker_ready_tree_attestation_object_sha256": "6" * 64,
        "terminal_boundary_object_sha256": "7" * 64,
        "anchor_file_sha256": "8" * 64,
        "anchor_object_sha256": "9" * 64,
        "pinset_file_sha256": "a" * 64,
        "pinset_object_sha256": "b" * 64,
        "pinned_role_count": len(EXPECTED_PIN_ROLES),
        "finalizer_source_sha256": source_sha,
        "finalizer_source_stat9": file_stat_fixture,
        "running_attestation_name": RUNNING_ATTESTATION_NAME,
        "running_attestation_file_sha256": "c" * 64,
        "running_attestation_stat9": file_stat_fixture,
        "running_attestation_object_sha256": "d" * 64,
        "composite_marker_name": COMPOSITE_MARKER_NAME,
        "composite_marker_sha256": hashlib.sha256(COMPOSITE_PASS_BYTES).hexdigest(),
        "prepared_marker_stat9": file_stat_fixture,
        "marker_commit_method": (
            "PREPARED_FSYNCED_SINGLETON_THEN_RENAMEAT2_NOREPLACE_"
            "AS_LAST_FS_MUTATION_THEN_PARENT_FSYNC_THEN_OS__EXIT_0"
        ),
        "filesystem_marker_authoritative": False,
        "orphan_READY_authority_eligible": False,
        "orphan_COMPOSITE_PASS_authority_eligible": False,
        "joint_authority_requires_post_exit_query": True,
        "required_finalizer_post_exit": expected_post,
        "authority_definition": (
            "EXACT_READY_TREE_AND_WORKER_POST_EXIT_SUCCESS_PLUS_"
            "COMPOSITE_RECEIPT_AND_MARKER_PLUS_FRESH_FINALIZER_"
            "POST_EXIT_UNIT_INVOCATION_EXECSTART_FRAGMENT_SUCCESS"
        ),
        "formal_credit": 0, "source_W_formal_remainder": 80,
        "source_W_transition_authorized": False,
        "publication_authorized": False, "terminal_replay_completed": False,
        "CM2": "NO-GO_FOR_CLAIM",
    })
    need(not post_exit_tuple_eligible(
             COMPOSITE_PASS_BYTES, receipt_fixture, None, fragment_fixture,
         )
         and not post_exit_tuple_eligible(
             None, receipt_fixture, post_fields, fragment_fixture,
         )
         and post_exit_tuple_eligible(
             COMPOSITE_PASS_BYTES, receipt_fixture, post_fields,
             fragment_fixture,
         ), "post-marker success is mandatory joint authority gate")
    attacks["post_marker_unit_success_required"] = (
        "marker and receipt rejected until fresh active/exited success query"
    )
    need(set(attacks) == {
        "worker_failure", "orphan_READY", "outer_pid_substitution",
        "marker_no_replace", "post_marker_running_not_success",
        "post_marker_unit_success_required", "boundary_anchor_sha_substitution",
        "runtime_directory_inode_substitution",
        "commit_parent_fsync_fault",
        "minimal_receipt",
        "ready_root_inode_substitution",
    }, "exact selftest negative inventory")
    return closed({
        "schema": (
            "cm2.round306c30c.postreceipt-bridge-v5-"
            "composite-finalizer-selftest.v1"
        ),
        "status": "PASS_11_COMPOSITE_FINALIZER_NEGATIVES_ZERO_CREDIT",
        "exact_exec_argv_cardinality": len(argv),
        "held_source_bootstrap_shell_neutral": True,
        "runtime_mutable_metadata_accepted": True,
        "ready_attestation_composite_extension_stable": True,
        "worker_failure_rejected": True, "orphan_READY_rejected": True,
        "outer_PID_substitution_rejected": True,
        "marker_no_replace_and_last": True,
        "commit_parent_fsync_fault_is_non_authoritative": True,
        "post_marker_unit_success_required": True,
        "filesystem_marker_authoritative": False,
        "negative_fixtures": attacks,
        "formal_execution_authorized": False,
        "formal_credit": 0, "source_W_formal_remainder": 80,
        "source_W_transition_authorized": False,
        "publication_authorized": False, "terminal_replay_completed": False,
        "CM2": "NO-GO_FOR_CLAIM",
    })


def verify_executed_source(
    fd: int, state: os.stat_result, raw: bytes, expected_sha256: str,
) -> dict[str, Any]:
    need(Path(os.path.abspath(os.fspath(__file__))) == SELF,
         "executed finalizer exact __file__")
    need(stat.S_ISREG(state.st_mode) and stat.S_IMODE(state.st_mode) == 0o444
         and state.st_nlink == 1 and state.st_uid == UID and state.st_gid == UID
         and 0 <= state.st_size <= 8 << 20, "held source frozen state")
    need(HEX64.fullmatch(expected_sha256) is not None
         and hashlib.sha256(raw).hexdigest() == expected_sha256,
         "held source expected SHA")
    need(identity(SELF.lstat()) == identity(state) == identity(os.fstat(fd)),
         "held source path/FD identity")
    need(read_fd(fd, 8 << 20) == raw, "held source exact byte replay")
    return {
        "path": os.fspath(SELF), "sha256": expected_sha256,
        "stat9": stat9(state),
    }


def main_arguments(
    argv: Sequence[str], executed_source: Mapping[str, Any] | None = None,
    release_source: Callable[[], None] | None = None,
) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--self-test", action="store_true")
    modes.add_argument("--run", action="store_true")
    parser.add_argument("--bridge-dir", type=Path)
    parser.add_argument("--pinset", type=Path)
    parser.add_argument("--anchor", type=Path)
    parser.add_argument("--worker-unit")
    parser.add_argument("--finalizer-unit")
    parser.add_argument("--maximum-wait-seconds", type=int, default=7 * 24 * 3600)
    arguments = parser.parse_args(list(argv))
    try:
        if arguments.self_test:
            need(all(value is None for value in (
                arguments.bridge_dir, arguments.pinset, arguments.anchor,
                arguments.worker_unit, arguments.finalizer_unit,
            )), "selftest has no formal launch material")
            print(canonical(self_test()).decode("ascii"))
            return 0
        need(executed_source is not None and release_source is not None,
             "production requires held -c source bootstrap")
        need(arguments.bridge_dir is not None and arguments.pinset is not None
             and arguments.anchor is not None
             and type(arguments.worker_unit) is str
             and type(arguments.finalizer_unit) is str,
             "complete production finalizer material")
        run_finalizer(
            arguments.bridge_dir, arguments.pinset, arguments.anchor,
            arguments.worker_unit, arguments.finalizer_unit,
            arguments.maximum_wait_seconds, executed_source, release_source,
        )
        raise Reject("unreachable production return")
    except (Reject, OSError, ValueError, TypeError, KeyError,
            subprocess.SubprocessError) as error:
        failure = closed({
            "schema": COMPOSITE_SCHEMA, "status": "BLOCKED_FAIL_CLOSED",
            "error_type": type(error).__name__, "error": str(error),
            "authoritative_composite_pass_published": False,
            "filesystem_marker_may_be_orphaned_after_commit_fsync_fault": True,
            "formal_credit": 0, "source_W_formal_remainder": 80,
            "source_W_transition_authorized": False,
            "publication_authorized": False, "terminal_replay_completed": False,
            "CM2": "NO-GO_FOR_CLAIM",
        })
        print(canonical(failure).decode("ascii"), file=sys.stderr)
        return 2


def held_entry(
    source_fd: int, source_state: os.stat_result, source_raw: bytes,
    expected_sha256: str, argv: list[str],
) -> int:
    def reverify() -> None:
        verify_executed_source(
            source_fd, source_state, source_raw, expected_sha256,
        )

    try:
        binding = verify_executed_source(
            source_fd, source_state, source_raw, expected_sha256,
        )
        return main_arguments(argv, binding, reverify)
    finally:
        # Production success uses os._exit(0), so the held source FD remains
        # live through marker publication and is closed only by the kernel.
        try:
            os.close(source_fd)
        except OSError:
            pass


if __name__ == "__main__":
    raise SystemExit(main_arguments(sys.argv[1:]))
