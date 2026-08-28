#!/usr/bin/env python3
"""Process custody helper for the append-only C30c bridge v3.

This helper never mints CM2 authority.  It gives GNU time a private anonymous
FD, runs a small trampoline, and has that trampoline bind the *real* inner PID
and its /proc identity before waiting for its exact exit/signal.  Captures are
first anonymous FDs and are then published only into a non-formal scratch
directory through an already-held directory FD.  The bridge watcher later
copies verified bytes into its own held formal stage FD.
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
from typing import Any, Mapping, Sequence


sys.dont_write_bytecode = True

WORKSPACE = Path("/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572")
SELF = WORKSPACE / "deliverables/cm2_round306c30c_postreceipt_bridge_v3_process_wrapper_v1.py"
PYTHON = Path("/usr/bin/python3.12")
GNU_TIME = Path("/usr/bin/time")
STRACE = Path("/usr/bin/strace")
REQUEST_SCHEMA = "cm2.round306c30c.bridge-v3-process-request.v1"
ATTEST_SCHEMA = "cm2.round306c30c.bridge-v3-inner-process-attestation.v1"
RECEIPT_SCHEMA = "cm2.round306c30c.bridge-v3-process-wrapper-receipt.v1"
TRACE_TOKEN = "@CM2_TRACE_FD@"
HEX64 = re.compile(r"[0-9a-f]{64}")


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
    result = dict(body)
    need("object_sha256" not in result, "fresh object closure")
    result["object_sha256"] = hashlib.sha256(canonical(result)).hexdigest()
    return result


def verify_closure(value: Mapping[str, Any], label: str) -> None:
    need(type(value) is dict and type(value.get("object_sha256")) is str
         and HEX64.fullmatch(value["object_sha256"]) is not None,
         "closure field:" + label)
    body = dict(value)
    observed = body.pop("object_sha256")
    need(hashlib.sha256(canonical(body)).hexdigest() == observed,
         "closure digest:" + label)


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


def dir_identity(value: os.stat_result) -> tuple[int, ...]:
    row = stat9(value)
    return tuple(row[key] for key in ("dev", "ino", "mode", "nlink", "uid", "gid"))


def read_all_fd(fd: int, maximum: int, require_link: bool = True) -> bytes:
    before = os.fstat(fd)
    need(stat.S_ISREG(before.st_mode)
         and (before.st_nlink == 1 if require_link else before.st_nlink in {0, 1})
         and 0 <= before.st_size <= maximum, "bounded singleton FD")
    os.lseek(fd, 0, os.SEEK_SET)
    chunks: list[bytes] = []
    remaining = before.st_size
    while remaining:
        block = os.read(fd, min(4 << 20, remaining))
        need(bool(block), "complete FD read")
        chunks.append(block)
        remaining -= len(block)
    need(os.read(fd, 1) == b"", "stable FD EOF")
    after = os.fstat(fd)
    need(identity(before) == identity(after), "stable FD identity")
    return b"".join(chunks)


def write_all_fd(fd: int, raw: bytes) -> None:
    offset = 0
    while offset < len(raw):
        count = os.write(fd, raw[offset:])
        need(count > 0, "write-all progress")
        offset += count


class HeldRegular:
    def __init__(self, path: Path, label: str, maximum: int = 16 << 20):
        self.path = Path(os.path.abspath(os.fspath(path)))
        before = self.path.lstat()
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "raw CLI regular singleton:" + label)
        self.fd = os.open(
            self.path, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
        )
        self.state = os.fstat(self.fd)
        need(identity(before) == identity(self.state), "CLI regular race:" + label)
        self.raw = read_all_fd(self.fd, maximum)
        self.sha256 = hashlib.sha256(self.raw).hexdigest()
        self.label = label

    def verify(self) -> None:
        current = self.path.lstat()
        held = os.fstat(self.fd)
        need(identity(current) == identity(self.state) == identity(held),
             "held regular inode drift:" + self.label)
        need(hashlib.sha256(read_all_fd(self.fd, max(len(self.raw), 1))) .hexdigest()
             == self.sha256, "held regular byte drift:" + self.label)

    def close(self) -> None:
        os.close(self.fd)


class HeldDirectory:
    def __init__(self, path: Path, label: str, require_empty: bool):
        self.path = Path(os.path.abspath(os.fspath(path)))
        before = self.path.lstat()
        need(stat.S_ISDIR(before.st_mode) and not stat.S_ISLNK(before.st_mode)
             and stat.S_IMODE(before.st_mode) == 0o700,
             "raw CLI private directory:" + label)
        self.fd = os.open(
            self.path, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC
            | getattr(os, "O_NOFOLLOW", 0),
        )
        self.initial = os.fstat(self.fd)
        need(identity(before) == identity(self.initial), "CLI directory race:" + label)
        self.label = label
        if require_empty:
            need(os.listdir(self.fd) == [], "fresh scratch directory")

    def verify_identity(self) -> None:
        current = self.path.lstat()
        held = os.fstat(self.fd)
        need(dir_identity(current) == dir_identity(self.initial) == dir_identity(held),
             "held directory identity drift:" + self.label)

    def names(self) -> list[str]:
        self.verify_identity()
        return sorted(os.listdir(self.fd))

    def write_once(self, name: str, raw: bytes) -> dict[str, Any]:
        need(name and "/" not in name and name not in {".", ".."},
             "direct scratch child")
        self.verify_identity()
        fd = os.open(
            name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC
            | getattr(os, "O_NOFOLLOW", 0), 0o400, dir_fd=self.fd,
        )
        try:
            write_all_fd(fd, raw)
            os.fsync(fd)
            written = os.fstat(fd)
            need(stat.S_ISREG(written.st_mode) and written.st_nlink == 1,
                 "scratch published regular singleton")
        finally:
            os.close(fd)
        check = os.open(
            name, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
            dir_fd=self.fd,
        )
        try:
            observed = read_all_fd(check, max(len(raw), 1))
            reopened = os.fstat(check)
        finally:
            os.close(check)
        need(raw == observed and identity(written) == identity(reopened),
             "scratch same-dirfd reopen")
        os.fsync(self.fd)
        self.verify_identity()
        return {
            "name": name, "sha256": hashlib.sha256(raw).hexdigest(),
            "size": len(raw), "stat9": stat9(written),
        }

    def close(self) -> None:
        os.close(self.fd)


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(
            raw.decode("ascii"), parse_float=lambda _: (_ for _ in ()).throw(ValueError()),
            parse_constant=lambda _: (_ for _ in ()).throw(ValueError()),
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise Reject("strict JSON:" + label) from error
    need(type(value) is dict and raw in {canonical(value), canonical(value) + b"\n"},
         "canonical JSON:" + label)
    return value


def exact_bool(value: Any, label: str) -> bool:
    need(type(value) is bool, "bool field:" + label)
    return value


def exact_int(value: Any, label: str) -> int:
    need(type(value) is int, "int field:" + label)
    return value


def validate_request(value: Mapping[str, Any]) -> dict[str, Any]:
    verify_closure(value, "process request")
    required = {
        "schema", "stage", "inner_argv", "inner_env", "expected_exe_real",
        "trace_requested", "formal_credit", "source_W_formal_remainder",
        "source_W_transition_authorized", "publication_authorized",
        "terminal_replay_completed", "object_sha256",
    }
    need(set(value) == required and value.get("schema") == REQUEST_SCHEMA,
         "exact process request schema/fields")
    stage = value.get("stage")
    argv = value.get("inner_argv")
    environment = value.get("inner_env")
    need(type(stage) is str and re.fullmatch(r"[a-z0-9-]{1,64}", stage) is not None,
         "stage token")
    need(type(argv) is list and bool(argv)
         and all(type(item) is str and item and "\x00" not in item for item in argv),
         "exact inner argv types")
    need(type(environment) is dict and bool(environment)
         and all(type(key) is str and type(item) is str and key and "\x00" not in key + item
                 for key, item in environment.items()), "exact inner env types")
    expected = value.get("expected_exe_real")
    need(type(expected) is str and Path(expected).is_absolute(), "expected exe path")
    trace = exact_bool(value.get("trace_requested"), "trace_requested")
    need((sum(item.count(TRACE_TOKEN) for item in argv) == 1) == trace,
         "exact trace placeholder cardinality")
    need(exact_int(value.get("formal_credit"), "formal_credit") == 0,
         "zero formal credit")
    need(exact_int(value.get("source_W_formal_remainder"), "remainder") == 80,
         "Source-W remains 80")
    for name in ("source_W_transition_authorized", "publication_authorized",
                 "terminal_replay_completed"):
        need(exact_bool(value.get(name), name) is False, "false field:" + name)
    return dict(value)


def read_proc_file(path: Path, maximum: int) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0))
    try:
        chunks: list[bytes] = []
        total = 0
        while True:
            block = os.read(fd, 65536)
            if not block:
                break
            total += len(block)
            need(total <= maximum, "bounded proc capture")
            chunks.append(block)
        return b"".join(chunks)
    finally:
        os.close(fd)


def proc_string_vector(raw: bytes, label: str) -> list[str]:
    need(raw.endswith(b"\x00"), "NUL terminated proc vector:" + label)
    try:
        return [part.decode("utf-8") for part in raw[:-1].split(b"\x00")]
    except UnicodeDecodeError as error:
        raise Reject("UTF-8 proc vector:" + label) from error


def trampoline(request_fd: int, request_sha256: str, attestation_fd: int,
               stdout_fd: int, stderr_fd: int, trace_fd: int | None) -> int:
    raw = read_all_fd(request_fd, 16 << 20)
    need(hashlib.sha256(raw).hexdigest() == request_sha256, "trampoline request SHA")
    request = validate_request(strict_json(raw, "trampoline request"))
    argv = list(request["inner_argv"])
    if request["trace_requested"]:
        need(trace_fd is not None, "trace FD supplied")
        argv = [item.replace(TRACE_TOKEN, "/proc/self/fd/" + str(trace_fd)) for item in argv]
    else:
        need(trace_fd is None, "no unexpected trace FD")
    process = subprocess.Popen(
        argv, cwd=WORKSPACE, env=request["inner_env"], stdin=subprocess.DEVNULL,
        stdout=stdout_fd, stderr=stderr_fd, close_fds=True,
        pass_fds=() if trace_fd is None else (trace_fd,),
    )
    inner_pid = process.pid
    need(inner_pid not in {os.getpid(), os.getppid()} and inner_pid > 1,
         "distinct true inner PID")
    proc = Path("/proc") / str(inner_pid)
    pidfd = os.pidfd_open(inner_pid, 0) if hasattr(os, "pidfd_open") else -1
    exe_fd = os.open(proc / "exe", os.O_RDONLY | os.O_CLOEXEC)
    try:
        exe_state = os.fstat(exe_fd)
        need(stat.S_ISREG(exe_state.st_mode), "inner /proc exe regular")
        exe_link = os.readlink(proc / "exe")
        cmdline_raw = read_proc_file(proc / "cmdline", 4 << 20)
        environ_raw = read_proc_file(proc / "environ", 4 << 20)
        cmdline = proc_string_vector(cmdline_raw, "cmdline")
        environment_rows = proc_string_vector(environ_raw, "environ")
        observed_environment: dict[str, str] = {}
        for row in environment_rows:
            key, separator, item = row.partition("=")
            need(separator == "=" and key and key not in observed_environment,
                 "unique proc environment")
            observed_environment[key] = item
        need(cmdline == argv, "exact /proc inner argv")
        need(observed_environment == request["inner_env"], "exact /proc inner env")
        need(Path(exe_link).resolve(strict=True)
             == Path(request["expected_exe_real"]).resolve(strict=True),
             "exact /proc inner executable")
        returncode = process.wait()
        ended_ns = time.time_ns()
        held_after = os.fstat(exe_fd)
        need(identity(exe_state) == identity(held_after), "held inner exe identity")
    finally:
        os.close(exe_fd)
        if pidfd >= 0:
            os.close(pidfd)
    exit_code = returncode if returncode >= 0 else None
    signal_number = -returncode if returncode < 0 else None
    attestation = closed({
        "schema": ATTEST_SCHEMA,
        "status": "PASS_TRUE_INNER_PID_CAPTURED_AND_WAITED",
        "trampoline_pid": os.getpid(), "time_parent_pid": os.getppid(),
        "true_inner_pid": inner_pid, "resolved_inner_argv": argv,
        "inner_env": request["inner_env"],
        "proc_cmdline_sha256": hashlib.sha256(cmdline_raw).hexdigest(),
        "proc_environ_sha256": hashlib.sha256(environ_raw).hexdigest(),
        "proc_exe_link": exe_link, "proc_exe_stat9": stat9(exe_state),
        "wait_returncode": returncode, "numeric_exit_code": exit_code,
        "signal": signal_number, "ended_ns": ended_ns,
        "formal_credit": 0, "source_W_formal_remainder": 80,
        "source_W_transition_authorized": False,
        "publication_authorized": False, "terminal_replay_completed": False,
    })
    payload = canonical(attestation) + b"\n"
    os.lseek(attestation_fd, 0, os.SEEK_SET)
    os.ftruncate(attestation_fd, 0)
    write_all_fd(attestation_fd, payload)
    os.fsync(attestation_fd)
    if signal_number is not None:
        return 128 + signal_number
    return int(exit_code)


def anonymous_file(name: str) -> int:
    need(hasattr(os, "memfd_create"), "memfd required")
    return os.memfd_create(name, getattr(os, "MFD_CLOEXEC", 0x0001))


def discover_single_time_child(time_pid: int, timeout_seconds: float = 10.0) -> int:
    deadline = time.monotonic() + timeout_seconds
    child_file = Path("/proc") / str(time_pid) / "task" / str(time_pid) / "children"
    while True:
        try:
            raw = child_file.read_bytes()
            rows = raw.split()
            if rows:
                need(len(rows) == 1 and rows[0].isdigit(), "single GNU-time child PID")
                pid = int(rows[0])
                need(pid > 1 and pid != time_pid, "true GNU-time child PID")
                return pid
        except FileNotFoundError:
            pass
        need(time.monotonic() < deadline, "discover GNU-time child timeout")
        time.sleep(0.001)


def capture_direct_child(
    pid: int, expected_argv: Sequence[str], expected_env: Mapping[str, str],
    expected_exe: str,
) -> tuple[dict[str, Any], int]:
    proc = Path("/proc") / str(pid)
    deadline = time.monotonic() + 10.0
    last_cmdline: list[str] = []
    while True:
        exe_fd = -1
        try:
            exe_fd = os.open(proc / "exe", os.O_RDONLY | os.O_CLOEXEC)
            exe_state = os.fstat(exe_fd)
            need(stat.S_ISREG(exe_state.st_mode), "direct child /proc exe regular")
            exe_link = os.readlink(proc / "exe")
            cmdline_raw = read_proc_file(proc / "cmdline", 4 << 20)
            environ_raw = read_proc_file(proc / "environ", 4 << 20)
            cmdline = (proc_string_vector(cmdline_raw, "direct child cmdline")
                       if cmdline_raw.endswith(b"\x00") else [])
            last_cmdline = cmdline
            if (cmdline == list(expected_argv)
                    and Path(exe_link).resolve(strict=True)
                    == Path(expected_exe).resolve(strict=True)):
                environment_rows = proc_string_vector(
                    environ_raw, "direct child environ",
                )
                environment: dict[str, str] = {}
                for row in environment_rows:
                    key, separator, item = row.partition("=")
                    need(separator == "=" and key and key not in environment,
                         "unique direct child environment")
                    environment[key] = item
                need(environment == dict(expected_env), "exact direct child /proc env")
                return ({
                    "cmdline_raw": cmdline_raw, "environ_raw": environ_raw,
                    "exe_link": exe_link, "exe_state": exe_state,
                }, exe_fd)
        except FileNotFoundError:
            pass
        if exe_fd >= 0:
            os.close(exe_fd)
        need(time.monotonic() < deadline,
             "direct child exec transition timeout observed=" + repr(last_cmdline))
        time.sleep(0.001)


def parse_time(raw: bytes, expected_command: str) -> dict[str, Any]:
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as error:
        raise Reject("GNU time ASCII") from error
    commands = re.findall(
        r'(?m)^\s*Command being timed:\s*"(.*)"\s*$', text,
    )
    exits = re.findall(r"(?m)^\s*Exit status:\s*([0-9]+)\s*$", text)
    signals = re.findall(
        r"(?m)^\s*Command terminated by signal\s+([0-9]+)\s*$", text,
    )
    elapsed = re.findall(
        r"(?m)^\s*Elapsed \(wall clock\) time .*:\s*([^\n]+)\s*$", text,
    )
    rss = re.findall(
        r"(?m)^\s*Maximum resident set size \(kbytes\):\s*([0-9]+)\s*$", text,
    )
    need(len(commands) == len(exits) == len(elapsed) == len(rss) == 1
         and len(signals) <= 1, "exact GNU time report:" + repr(text))
    need(commands[0] == expected_command, "exact GNU time command")
    return {
        "command": commands[0], "exit_status": int(exits[0]),
        "signal": None if not signals else int(signals[0]),
        "elapsed_text": elapsed[0].strip(), "maxrss_kb": int(rss[0]),
    }


def run_request(request_path: Path, request_sha256: str, scratch_path: Path) -> dict[str, Any]:
    request_file = HeldRegular(request_path, "process request")
    scratch = HeldDirectory(scratch_path, "process scratch", require_empty=True)
    descriptors: list[int] = []
    try:
        need(request_file.sha256 == request_sha256, "process request CLI SHA")
        request = validate_request(strict_json(request_file.raw, "process request"))
        self_file = HeldRegular(SELF, "process wrapper self", 8 << 20)
        time_file = HeldRegular(GNU_TIME, "GNU time", 8 << 20)
        python_file = HeldRegular(PYTHON, "final Python", 64 << 20)
        try:
            stdout_fd = anonymous_file("cm2-v3-stdout")
            stderr_fd = anonymous_file("cm2-v3-stderr")
            time_fd = anonymous_file("cm2-v3-time")
            attest_fd = anonymous_file("cm2-v3-attestation")
            descriptors.extend([stdout_fd, stderr_fd, time_fd, attest_fd])
            trace_fd: int | None = None
            if request["trace_requested"]:
                trace_fd = anonymous_file("cm2-v3-trace")
                descriptors.append(trace_fd)
            trampoline_argv = [
                os.fspath(PYTHON), "-I", "-B", os.fspath(SELF),
                "--trampoline", "--request-fd", str(request_file.fd),
                "--request-sha256", request_sha256,
                "--attestation-fd", str(attest_fd),
                "--stdout-fd", str(stdout_fd), "--stderr-fd", str(stderr_fd),
            ]
            execution_mode = "TRAMPOLINE_TRUE_INNER"
            timed_target = list(trampoline_argv)
            timed_environment = {
                "HOME": "/nonexistent", "PATH": "/usr/bin:/bin",
                "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC",
                "PYTHONDONTWRITEBYTECODE": "1",
            }
            if trace_fd is not None:
                # GNU time directly owns the strace process.  This preserves the
                # legacy cold analyzer's genuine `Command being timed: strace ...`
                # evidence while this wrapper independently holds that real
                # non-time child PID and its /proc identity.
                execution_mode = "GNU_TIME_DIRECT_TRACE_CHILD"
                timed_target = [
                    item.replace(TRACE_TOKEN, "/proc/self/fd/" + str(trace_fd))
                    for item in request["inner_argv"]
                ]
                timed_environment = dict(request["inner_env"])
            expected_time_command = " ".join(timed_target)
            time_argv = [
                os.fspath(GNU_TIME), "--verbose",
                "--output=/proc/self/fd/" + str(time_fd), "--", *timed_target,
            ]
            inherited = tuple([request_file.fd, stdout_fd, stderr_fd, time_fd,
                               attest_fd] + ([] if trace_fd is None else [trace_fd]))
            started_ns = time.time_ns()
            timed = subprocess.Popen(
                time_argv, cwd=WORKSPACE, env=timed_environment,
                stdin=subprocess.DEVNULL,
                stdout=stdout_fd if trace_fd is not None else subprocess.DEVNULL,
                stderr=stderr_fd if trace_fd is not None else subprocess.DEVNULL,
                close_fds=True, pass_fds=inherited,
            )
            time_pid = timed.pid
            direct_capture: dict[str, Any] | None = None
            direct_exe_fd = -1
            direct_pid: int | None = None
            if trace_fd is not None:
                direct_pid = discover_single_time_child(time_pid)
                direct_capture, direct_exe_fd = capture_direct_child(
                    direct_pid, timed_target, timed_environment,
                    request["expected_exe_real"],
                )
            time_returncode = timed.wait()
            ended_ns = time.time_ns()
            if direct_capture is not None:
                direct_time_raw = read_all_fd(time_fd, 8 << 20, False)
                direct_timing = parse_time(direct_time_raw, expected_time_command)
                try:
                    need(identity(direct_capture["exe_state"])
                         == identity(os.fstat(direct_exe_fd)),
                         "held direct child exe identity through wait")
                finally:
                    os.close(direct_exe_fd)
                attestation_value = closed({
                    "schema": ATTEST_SCHEMA,
                    "status": "PASS_TRUE_GNU_TIME_CHILD_PID_CAPTURED_AND_WAITED",
                    "trampoline_pid": None, "time_parent_pid": time_pid,
                    "true_inner_pid": direct_pid,
                    "resolved_inner_argv": timed_target,
                    "inner_env": timed_environment,
                    "proc_cmdline_sha256": hashlib.sha256(
                        direct_capture["cmdline_raw"]).hexdigest(),
                    "proc_environ_sha256": hashlib.sha256(
                        direct_capture["environ_raw"]).hexdigest(),
                    "proc_exe_link": direct_capture["exe_link"],
                    "proc_exe_stat9": stat9(direct_capture["exe_state"]),
                    "wait_returncode": time_returncode,
                    "numeric_exit_code": time_returncode,
                    "signal": direct_timing["signal"], "ended_ns": ended_ns,
                    "formal_credit": 0, "source_W_formal_remainder": 80,
                    "source_W_transition_authorized": False,
                    "publication_authorized": False,
                    "terminal_replay_completed": False,
                })
                os.lseek(attest_fd, 0, os.SEEK_SET); os.ftruncate(attest_fd, 0)
                write_all_fd(attest_fd, canonical(attestation_value) + b"\n")
                os.fsync(attest_fd)
            outputs = {
                "stdout.capture": read_all_fd(stdout_fd, 256 << 20, False),
                "stderr.capture": read_all_fd(stderr_fd, 256 << 20, False),
                "time.capture": read_all_fd(time_fd, 8 << 20, False),
                "attestation.capture": read_all_fd(attest_fd, 16 << 20, False),
            }
            if trace_fd is not None:
                outputs["trace.capture"] = read_all_fd(trace_fd, 8 << 30, False)
            attestation = strict_json(outputs["attestation.capture"], "attestation")
            verify_closure(attestation, "attestation")
            need(attestation.get("schema") == ATTEST_SCHEMA,
                 "attestation exact schema")
            timing = parse_time(outputs["time.capture"], expected_time_command)
            need(type(attestation.get("wait_returncode")) is int,
                 "attestation wait return type")
            expected_time_exit = (attestation["wait_returncode"] if
                                  attestation["wait_returncode"] >= 0 else
                                  128 + -attestation["wait_returncode"])
            need(time_returncode == timing["exit_status"] == expected_time_exit,
                 "time/trampoline/inner exit closure")
            published = [scratch.write_once(name, raw)
                         for name, raw in sorted(outputs.items())]
            request_file.verify(); self_file.verify(); time_file.verify(); python_file.verify()
            expected_names = sorted(outputs)
            need(scratch.names() == expected_names, "exact scratch capture inventory")
            receipt = closed({
                "schema": RECEIPT_SCHEMA,
                "status": "PASS_WRAPPER_CAPTURED_TRUE_INNER_PID_ZERO_CREDIT",
                "execution_mode": execution_mode,
                "wrapper_pid": os.getpid(), "gnu_time_pid": time_pid,
                "trampoline_pid": attestation["trampoline_pid"],
                "true_inner_pid": attestation["true_inner_pid"],
                "three_level_pid_distinct": (
                    len({os.getpid(), time_pid, attestation["true_inner_pid"]}) == 3
                    if attestation["trampoline_pid"] is None else
                    len({os.getpid(), time_pid, attestation["trampoline_pid"],
                         attestation["true_inner_pid"]}) == 4
                ),
                "time_argv": time_argv, "expected_time_command": expected_time_command,
                "time_returncode": time_returncode, "gnu_time": timing,
                "attestation": attestation, "captures": published,
                "request_path": os.fspath(request_file.path),
                "request_sha256": request_sha256,
                "request_stat9": stat9(request_file.state),
                "wrapper_sha256": self_file.sha256,
                "wrapper_stat9": stat9(self_file.state),
                "gnu_time_sha256": time_file.sha256,
                "gnu_time_stat9": stat9(time_file.state),
                "python_sha256": python_file.sha256,
                "python_stat9": stat9(python_file.state),
                "started_ns": started_ns, "ended_ns": ended_ns,
                "formal_credit": 0, "source_W_formal_remainder": 80,
                "source_W_transition_authorized": False,
                "publication_authorized": False,
                "terminal_replay_completed": False,
            })
            need(receipt["three_level_pid_distinct"] is True,
                 "wrapper/time/(trampoline)/inner PIDs distinct")
            return receipt
        finally:
            self_file.close(); time_file.close(); python_file.close()
    finally:
        for descriptor in descriptors:
            try:
                os.close(descriptor)
            except OSError:
                pass
        request_file.close(); scratch.close()


def self_test() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="cm2-c30c-v3-wrapper-") as temporary:
        root = Path(temporary)
        os.chmod(root, 0o700)
        scratch = root / "scratch"
        scratch.mkdir(mode=0o700)
        request = closed({
            "schema": REQUEST_SCHEMA, "stage": "tiny-positive",
            "inner_argv": [
                os.fspath(PYTHON), "-I", "-B", "-c",
                "import time;print('{\"formal_credit\":0,\"publication_authorized\":false,\"source_W_formal_remainder\":80,\"source_W_transition_authorized\":false,\"status\":\"PASS_TINY\",\"terminal_replay_completed\":false}');time.sleep(.25)",
            ],
            "inner_env": {
                "HOME": "/nonexistent", "PATH": "/usr/bin:/bin",
                "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC",
                "PYTHONDONTWRITEBYTECODE": "1",
            },
            "expected_exe_real": os.fspath(PYTHON), "trace_requested": False,
            "formal_credit": 0, "source_W_formal_remainder": 80,
            "source_W_transition_authorized": False,
            "publication_authorized": False, "terminal_replay_completed": False,
        })
        request_raw = canonical(request) + b"\n"
        request_path = root / "request.json"
        fd = os.open(request_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o400)
        try:
            write_all_fd(fd, request_raw); os.fsync(fd)
        finally:
            os.close(fd)
        receipt = run_request(
            request_path, hashlib.sha256(request_raw).hexdigest(), scratch,
        )
        need(receipt["status"] == "PASS_WRAPPER_CAPTURED_TRUE_INNER_PID_ZERO_CREDIT",
             "positive wrapper selftest")
        need(receipt["attestation"]["numeric_exit_code"] == 0
             and receipt["attestation"]["signal"] is None,
             "tiny inner clean exit")
        trace_scratch = root / "trace-scratch"; trace_scratch.mkdir(mode=0o700)
        trace_request = closed({
            "schema": REQUEST_SCHEMA, "stage": "tiny-trace-positive",
            "inner_argv": [
                os.fspath(STRACE), "-f", "-yy", "-s", "4096", "-e", "trace=all",
                "-o", TRACE_TOKEN, os.fspath(PYTHON), "-I", "-B", "-c",
                "import time;print('{\"formal_credit\":0,\"publication_authorized\":false,\"source_W_formal_remainder\":80,\"source_W_transition_authorized\":false,\"status\":\"PASS_TINY_TRACE\",\"terminal_replay_completed\":false}');time.sleep(.25)",
            ],
            "inner_env": dict(request["inner_env"]),
            "expected_exe_real": os.fspath(STRACE), "trace_requested": True,
            "formal_credit": 0, "source_W_formal_remainder": 80,
            "source_W_transition_authorized": False,
            "publication_authorized": False, "terminal_replay_completed": False,
        })
        trace_raw = canonical(trace_request) + b"\n"
        trace_path = root / "trace-request.json"; write_fd = os.open(
            trace_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o400,
        )
        try:
            write_all_fd(write_fd, trace_raw); os.fsync(write_fd)
        finally:
            os.close(write_fd)
        trace_receipt = run_request(
            trace_path, hashlib.sha256(trace_raw).hexdigest(), trace_scratch,
        )
        need(trace_receipt["execution_mode"] == "GNU_TIME_DIRECT_TRACE_CHILD"
             and trace_receipt["trampoline_pid"] is None
             and os.fspath(STRACE) in trace_receipt["gnu_time"]["command"]
             and "trace.capture" in {row["name"] for row in trace_receipt["captures"]},
             "direct GNU-time strace child selftest")
        return closed({
            "schema": "cm2.round306c30c.bridge-v3-wrapper-selftest.v1",
            "status": "PASS_TRUE_INNER_PID_AND_DIRECT_STRACE_GNU_TIME_SELFTEST_ZERO_CREDIT",
            "capture_count": len(receipt["captures"]) + len(trace_receipt["captures"]),
            "pid_distinct": receipt["three_level_pid_distinct"]
                            and trace_receipt["three_level_pid_distinct"],
            "direct_trace_mode": True,
            "formal_credit": 0, "source_W_formal_remainder": 80,
            "source_W_transition_authorized": False,
            "publication_authorized": False, "terminal_replay_completed": False,
        })


def main() -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--self-test", action="store_true")
    modes.add_argument("--run", action="store_true")
    modes.add_argument("--trampoline", action="store_true")
    parser.add_argument("--request", type=Path)
    parser.add_argument("--request-sha256")
    parser.add_argument("--scratch", type=Path)
    parser.add_argument("--request-fd", type=int)
    parser.add_argument("--attestation-fd", type=int)
    parser.add_argument("--stdout-fd", type=int)
    parser.add_argument("--stderr-fd", type=int)
    parser.add_argument("--trace-fd", type=int)
    args = parser.parse_args()
    try:
        if args.self_test:
            need(all(value is None for value in (
                args.request, args.request_sha256, args.scratch, args.request_fd,
                args.attestation_fd, args.stdout_fd, args.stderr_fd, args.trace_fd,
            )), "selftest has no formal arguments")
            print(canonical(self_test()).decode("ascii"))
            return 0
        if args.trampoline:
            need(args.request is None and args.scratch is None
                 and type(args.request_fd) is int and type(args.attestation_fd) is int
                 and type(args.stdout_fd) is int and type(args.stderr_fd) is int
                 and type(args.request_sha256) is str,
                 "complete trampoline FD arguments")
            return trampoline(
                args.request_fd, args.request_sha256, args.attestation_fd,
                args.stdout_fd, args.stderr_fd, args.trace_fd,
            )
        need(args.request is not None and type(args.request_sha256) is str
             and args.scratch is not None and all(value is None for value in (
                 args.request_fd, args.attestation_fd, args.stdout_fd,
                 args.stderr_fd, args.trace_fd,
             )), "complete wrapper run arguments")
        receipt = run_request(args.request, args.request_sha256, args.scratch)
        print(canonical(receipt).decode("ascii"))
        return 0
    except (Reject, OSError, ValueError, TypeError, KeyError,
            subprocess.SubprocessError) as error:
        failure = closed({
            "schema": RECEIPT_SCHEMA, "status": "BLOCKED_FAIL_CLOSED",
            "error": str(error), "formal_credit": 0,
            "source_W_formal_remainder": 80,
            "source_W_transition_authorized": False,
            "publication_authorized": False, "terminal_replay_completed": False,
        })
        print(canonical(failure).decode("ascii"), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
