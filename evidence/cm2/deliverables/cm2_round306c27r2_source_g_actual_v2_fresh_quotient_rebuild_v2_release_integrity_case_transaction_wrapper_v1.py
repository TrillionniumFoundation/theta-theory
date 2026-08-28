#!/usr/bin/env python3
"""Execute one real C27R2 negative validator transaction.

This wrapper is a separate process.  It independently captures every declared
authority directory/file, the core service, and future-absence sentinels;
executes exactly one validator child; removes the private fixture tree; captures
the authorities again; and only then publishes an exact eleven-file process
transaction.  It is permanently zero-credit and never publishes authority.
"""

from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
PREFIX = "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
REQUEST_SCHEMA = PREFIX + "release-integrity-case-wrapper-request.v1"
REQUEST_STATUS = "FROZEN_REAL_PER_CASE_WRAPPER_REQUEST__ZERO_CREDIT"
RUN_SCHEMA = PREFIX + "release-integrity-case-process-run.v5"
RUN_STATUS = (
    "PASS_REAL_WRAPPER_EXPECTED_VALIDATOR_EXIT2_NULL_SIGNAL_NO_OUTPUT_"
    "AUTHORITY_PRE_POST_FULL_TREE_AND_SERVICE_UNCHANGED__ZERO_CREDIT"
)
PASS_BYTES = (
    b"PASS_C27R2_RELEASE_BOUNDARY_REAL_PER_CASE_WRAPPER_TRANSACTION__"
    b"ZERO_CREDIT\n"
)
RUN_FILES = {
    "PASS.lock", "exit_code.txt", "signal.json", "stderr.log",
    "stdout.log", "timing.json", "input_pre.json", "input_post.json",
    "output_validation.json", "runner_start.json", "run_attestation.json",
}
MAX_CAPTURE_BYTES = 1 << 20
SYSTEMCTL = Path("/usr/bin/systemctl")
SYSTEMCTL_SHA256 = (
    "7ba82b5ba146759c710e1b80fadaa3fdbc0f9b85c8fb2c8c3196b7b1a0037ef8"
)
SERVICE_UID = 1000
SERVICE_RUNTIME = Path("/run/user/1000")
SERVICE_BUS = SERVICE_RUNTIME / "bus"
CONTROL_BUS_ENV = {
    "PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
    "XDG_RUNTIME_DIR": "/run/user/1000",
    "DBUS_SESSION_BUS_ADDRESS": "unix:path=/run/user/1000/bus",
}


class Rejected(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def valid_sha(value: Any) -> bool:
    return type(value) is str and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace(
        "+00:00", "Z")


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns,
            value.st_uid, value.st_gid)


def strict_load(payload: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(key not in result, "duplicate JSON key")
            result[key] = value
        return result
    return json.loads(payload.decode("ascii"), object_pairs_hook=pairs,
                      parse_constant=lambda token: (_ for _ in ()).throw(
                          Rejected("non-finite JSON:" + token)))


def capture_file(path: Path, maximum: int = 16 << 30) \
        -> tuple[bytes, dict[str, Any]]:
    path = path.absolute()
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                         | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1
             and 0 <= before.st_size <= maximum,
             "singleton regular bounded file")
        state = hashlib.sha256()
        chunks: list[bytes] = []
        while block := os.read(descriptor, 4 << 20):
            state.update(block)
            chunks.append(block)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    current = os.stat(path, follow_symlinks=False)
    need(fingerprint(before) == fingerprint(after) == fingerprint(current),
         "file FD/path full9stat identity")
    payload = b"".join(chunks)
    need(len(payload) == before.st_size, "captured exact file size")
    return payload, {"sha256": state.hexdigest(), "size": len(payload),
                     "stat_fingerprint": list(fingerprint(before))}


def closed_document(path: Path, closure: str,
                    maximum: int = 16 << 20) \
        -> tuple[dict[str, Any], dict[str, Any]]:
    payload, record = capture_file(path, maximum)
    need(payload.endswith(b"\n") and not payload.endswith(b"\n\n"),
         "canonical document newline")
    value = strict_load(payload[:-1])
    need(type(value) is dict and canonical(value) == payload[:-1],
         "canonical document object")
    body = dict(value)
    claim = body.pop(closure, None)
    need(valid_sha(claim) and claim == digest(body), "document object closure")
    return value, record


def write_once(path: Path, payload: bytes, mode: int = 0o400) \
        -> dict[str, Any]:
    path = path.absolute()
    need(path.parent.is_dir() and not path.parent.is_symlink()
         and not path.exists() and not path.is_symlink(), "fresh write path")
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                         | getattr(os, "O_CLOEXEC", 0)
                         | getattr(os, "O_NOFOLLOW", 0), mode)
    try:
        view = memoryview(payload)
        offset = 0
        while offset < len(view):
            written = os.write(descriptor, view[offset:])
            need(type(written) is int and written > 0,
                 "write-all positive progress")
            offset += written
        need(offset == len(payload), "write-all exact length")
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    reopened, record = capture_file(path, max(1, len(payload)))
    need(reopened == payload, "reopened exact output bytes")
    parent = os.open(path.parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
                     | getattr(os, "O_CLOEXEC", 0)
                     | getattr(os, "O_NOFOLLOW", 0))
    try:
        os.fsync(parent)
    finally:
        os.close(parent)
    return record


def authority_key(path: Path) -> str:
    try:
        return str(path.absolute().relative_to(ROOT))
    except ValueError:
        return "external:" + str(path.absolute())


def snapshot_node(path: Path, result: dict[str, Any]) -> None:
    path = path.absolute()
    initial = os.stat(path, follow_symlinks=False)
    need(not stat.S_ISLNK(initial.st_mode), "no authority symlink")
    key = authority_key(path)
    need(key not in result, "unique authority node")
    if stat.S_ISREG(initial.st_mode):
        _, record = capture_file(path)
        need(record["stat_fingerprint"] == list(fingerprint(initial)),
             "authority file initial/current full9stat")
        result[key] = {"node_type": "regular", **record}
        return
    need(stat.S_ISDIR(initial.st_mode),
         "authority node regular file or directory")
    with os.scandir(path) as stream:
        entries = sorted(list(stream), key=lambda item: item.name)
    inventory: list[dict[str, str]] = []
    for entry in entries:
        child = entry.stat(follow_symlinks=False)
        need(not stat.S_ISLNK(child.st_mode), "no authority tree symlink")
        if stat.S_ISDIR(child.st_mode):
            kind = "directory"
        elif stat.S_ISREG(child.st_mode):
            kind = "regular"
        else:
            raise Rejected("unexpected authority node type:" + entry.path)
        inventory.append({"name": entry.name, "node_type": kind})
        snapshot_node(Path(entry.path), result)
    final = os.stat(path, follow_symlinks=False)
    need(fingerprint(initial) == fingerprint(final),
         "authority directory stable full9stat during scan")
    result[key] = {"node_type": "directory",
        "stat_fingerprint": list(fingerprint(initial)),
        "entry_count": len(inventory), "entries": inventory,
        "entry_inventory_sha256": digest(inventory)}


def service_bus_stat() -> list[int]:
    need(os.getuid() == os.geteuid() == SERVICE_UID
         and SERVICE_RUNTIME.is_dir() and not SERVICE_RUNTIME.is_symlink(),
         "exact service uid/runtime")
    runtime = os.stat(SERVICE_RUNTIME, follow_symlinks=False)
    bus = os.stat(SERVICE_BUS, follow_symlinks=False)
    need(stat.S_ISDIR(runtime.st_mode) and runtime.st_uid == SERVICE_UID
         and stat.S_ISSOCK(bus.st_mode) and bus.st_uid == SERVICE_UID
         and bus.st_nlink == 1,
         "owned real runtime and singleton bus socket")
    return list(fingerprint(bus))


def service_snapshot(unit: str, invocation: str) -> dict[str, str]:
    need(type(unit) is str and unit.endswith(".service")
         and re.fullmatch(r"[0-9a-f]{32}", invocation) is not None,
         "service unit/invocation syntax")
    _, systemctl = capture_file(SYSTEMCTL, 16 << 20)
    need(systemctl["sha256"] == SYSTEMCTL_SHA256,
         "exact systemctl current pin")
    before = service_bus_stat()
    completed = subprocess.run([
        str(SYSTEMCTL), "--user", "show", unit,
        "-p", "LoadState", "-p", "ActiveState", "-p", "SubState",
        "-p", "Result", "-p", "ExecMainCode", "-p", "ExecMainStatus",
        "-p", "InvocationID"], cwd=ROOT, env=CONTROL_BUS_ENV,
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False, timeout=30)
    after = service_bus_stat()
    need(before == after and completed.returncode == 0
         and completed.stderr == b"", "clean fixed-route service query")
    lines = completed.stdout.decode("ascii").splitlines()
    need(len(lines) == 7 and all(line.count("=") == 1 for line in lines)
         and len({line.split("=", 1)[0] for line in lines}) == 7,
         "wrapper service query exactly seven unique key/value lines")
    fields = dict(line.split("=", 1) for line in lines)
    need(fields == {"Result": "success", "ExecMainCode": "1",
                    "ExecMainStatus": "0", "LoadState": "loaded",
                    "ActiveState": "active", "SubState": "exited",
                    "InvocationID": invocation}, "exact service state")
    return fields


def absence_snapshot(targets: list[Path], parent: Path) \
        -> dict[str, dict[str, Any]]:
    parent = parent.absolute()
    need(parent.is_dir() and not parent.is_symlink(), "real absence parent")
    result: dict[str, dict[str, Any]] = {}
    for target in targets:
        target = target.absolute()
        need(target.parent == parent and target.name not in {"", ".", ".."},
             "direct canonical absence target")
        before = os.stat(parent, follow_symlinks=False)
        try:
            os.stat(target, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            raise Rejected("future target exists:" + str(target))
        after = os.stat(parent, follow_symlinks=False)
        need(fingerprint(before) == fingerprint(after),
             "absence parent stable full9stat")
        result[str(target)] = {"path": str(target), "exists": False,
            "symlink": False, "parent_path": str(parent),
            "parent_stat_fingerprint": list(fingerprint(before))}
    return result


def full_snapshot(request: dict[str, Any]) -> dict[str, Any]:
    nodes: dict[str, Any] = {}
    roots = request["authority_roots"]
    need(type(roots) is list and roots == sorted(set(roots))
         and all(type(item) is str for item in roots),
         "sorted unique authority roots")
    for raw in roots:
        snapshot_node(Path(raw), nodes)
    service = service_snapshot(request["core_unit"],
                               request["core_invocation_id"])
    targets = [Path(item) for item in request["future_targets"]]
    absence = absence_snapshot(targets, Path(request["future_parent"]))
    result = {"authority_nodes": nodes, "core_service": service,
              "future_absence": absence,
              "authority_node_count": len(nodes),
              "future_absence_count": len(absence)}
    result["snapshot_sha256"] = digest(result)
    return result


def invoke(command: list[str], environment: dict[str, str], timeout: int) \
        -> dict[str, Any]:
    started = time.monotonic()
    with tempfile.TemporaryFile() as stdout_stream, \
            tempfile.TemporaryFile() as stderr_stream:
        try:
            completed = subprocess.run(command, cwd=ROOT, env=environment,
                stdin=subprocess.DEVNULL, stdout=stdout_stream,
                stderr=stderr_stream, check=False, timeout=timeout)
            timed_out = False
            code = completed.returncode
        except subprocess.TimeoutExpired:
            timed_out = True
            code = None
        elapsed = time.monotonic() - started
        stdout_stream.seek(0, os.SEEK_END)
        stdout_size = stdout_stream.tell()
        stderr_stream.seek(0, os.SEEK_END)
        stderr_size = stderr_stream.tell()
        stdout_stream.seek(0)
        stderr_stream.seek(0)
        stdout = stdout_stream.read(MAX_CAPTURE_BYTES + 1)
        stderr = stderr_stream.read(MAX_CAPTURE_BYTES + 1)
    if code is None:
        numeric, child_signal = None, None
    elif code < 0:
        numeric, child_signal = None, -code
    else:
        numeric, child_signal = code, None
    return {"numeric_exit_code": numeric, "signal": child_signal,
            "timed_out": timed_out, "elapsed_seconds": elapsed,
            "stdout": stdout, "stderr": stderr,
            "stdout_size": stdout_size, "stderr_size": stderr_size,
            "capture_bounded": stdout_size <= MAX_CAPTURE_BYTES
                               and stderr_size <= MAX_CAPTURE_BYTES}


def invoke_barrier(command: list[str], environment: dict[str, str],
                   case_root: Path, content_drift: bool,
                   timeout: int) -> dict[str, Any]:
    started = time.monotonic()
    with tempfile.TemporaryFile() as stdout_stream, \
            tempfile.TemporaryFile() as stderr_stream:
        process = subprocess.Popen(command, cwd=ROOT, env=environment,
            stdin=subprocess.DEVNULL, stdout=stdout_stream,
            stderr=stderr_stream)
        deadline = time.monotonic() + min(timeout, 60)
        try:
            while not (case_root / "fd-opened.lock").exists():
                if process.poll() is not None:
                    break
                need(time.monotonic() < deadline, "barrier opened in time")
                time.sleep(0.01)
            need(process.poll() is None
                 and (case_root / "fd-opened.lock").exists(),
                 "validator reached barrier")
            override = case_root / "override"
            replacement = case_root / "replacement"
            payload = capture_file(override)[0]
            if content_drift:
                payload += b"TOCTOU\n"
            write_once(replacement, payload, 0o600)
            os.replace(replacement, override)
            write_once(case_root / "continue.lock", b"CONTINUE\n", 0o600)
            process.wait(timeout=timeout)
            code = process.returncode
            timed_out = False
        except (subprocess.TimeoutExpired, Rejected):
            process.kill()
            process.wait()
            code = process.returncode
            timed_out = True
        stdout_stream.seek(0, os.SEEK_END)
        stdout_size = stdout_stream.tell()
        stderr_stream.seek(0, os.SEEK_END)
        stderr_size = stderr_stream.tell()
        stdout_stream.seek(0)
        stderr_stream.seek(0)
        stdout = stdout_stream.read(MAX_CAPTURE_BYTES + 1)
        stderr = stderr_stream.read(MAX_CAPTURE_BYTES + 1)
    return {"numeric_exit_code": code if code >= 0 else None,
            "signal": -code if code < 0 else None, "timed_out": timed_out,
            "elapsed_seconds": round(time.monotonic() - started, 6),
            "stdout": stdout, "stderr": stderr,
            "stdout_size": stdout_size, "stderr_size": stderr_size,
            "capture_bounded": (stdout_size <= MAX_CAPTURE_BYTES
                                and stderr_size <= MAX_CAPTURE_BYTES)}


def remove_private(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink(missing_ok=True)
    elif path.exists():
        shutil.rmtree(path)


def write_transaction(process_dir: Path, request: dict[str, Any],
                      request_record: dict[str, Any], pre: dict[str, Any],
                      post: dict[str, Any], child: dict[str, Any],
                      started_at: str, finished_at: str) -> bytes:
    need(not process_dir.exists() and not process_dir.is_symlink(),
         "fresh process transaction directory")
    process_dir.mkdir(mode=0o700)
    wrapper_stdout = canonical({"schema": RUN_SCHEMA + ".stdout.v1",
        "status": RUN_STATUS, "case": request["case"],
        "formal_credit": 0, "CM2": "NO-GO_FOR_CLAIM"}) + b"\n"
    input_pre = {"schema": RUN_SCHEMA + ".input.v1", "phase": "pre",
        "case": request["case"], "ordinal": request["ordinal"],
        "request_file_sha256": request_record["sha256"],
        "request_object_sha256": request["request_sha256"],
        "wrapper_request": request,
        "snapshot": pre, "validator_command": request["validator_command"],
        "validator_environment": request["validator_environment"],
        "formal_credit": 0}
    input_post = {"schema": RUN_SCHEMA + ".input.v1", "phase": "post",
        "case": request["case"], "ordinal": request["ordinal"],
        "request_file_sha256": request_record["sha256"],
        "request_object_sha256": request["request_sha256"],
        "wrapper_request": request,
        "snapshot": post, "validator_command": request["validator_command"],
        "validator_environment": request["validator_environment"],
        "formal_credit": 0}
    start = {"schema": RUN_SCHEMA + ".start.v1", "mode": "formal",
        "case": request["case"], "ordinal": request["ordinal"],
        "started_at_utc": started_at,
        "exact_argv": request["validator_command"],
        "exact_environment": request["validator_environment"],
        "wrapper_pid": os.getpid(), "formal_credit": 0}
    timing = {"schema": RUN_SCHEMA + ".timing.v1",
        "started_at_utc": started_at, "finished_at_utc": finished_at,
        "elapsed_seconds": child["elapsed_seconds"], "timed_out": False,
        "formal_credit": 0}
    output_body = {"schema": RUN_SCHEMA + ".output-validation.v1",
        "case": request["case"], "expected_validator_rejection": True,
        "child_numeric_exit_code": 2, "child_signal": None,
        "child_stdout_sha256": hashlib.sha256(child["stdout"]).hexdigest(),
        "child_stderr_sha256": hashlib.sha256(child["stderr"]).hexdigest(),
        "child_stdout_size": child["stdout_size"],
        "child_stderr_size": child["stderr_size"],
        "child_stderr_prefix": child["stderr"][:512].decode(
            "utf-8", "replace"),
        "child_validator_output_created": False, "bounded_capture": True,
        "private_case_root_cleaned": True, "formal_credit": 0}
    output = dict(output_body)
    output["output_validation_sha256"] = digest(output_body)
    write_once(process_dir / "exit_code.txt", b"0\n")
    write_once(process_dir / "signal.json", b"null\n")
    write_once(process_dir / "stderr.log", b"")
    write_once(process_dir / "stdout.log", wrapper_stdout)
    write_once(process_dir / "timing.json", canonical(timing) + b"\n")
    write_once(process_dir / "input_pre.json", canonical(input_pre) + b"\n")
    write_once(process_dir / "input_post.json", canonical(input_post) + b"\n")
    write_once(process_dir / "output_validation.json", canonical(output) + b"\n")
    write_once(process_dir / "runner_start.json", canonical(start) + b"\n")
    members = {name: capture_file(process_dir / name)[1]["sha256"]
               for name in sorted(RUN_FILES - {"PASS.lock",
                                                "run_attestation.json"})}
    body = {"schema": RUN_SCHEMA, "status": RUN_STATUS, "mode": "formal",
        "case": request["case"], "ordinal": request["ordinal"],
        "real_wrapper_process": True, "wrapper_pid": os.getpid(),
        "wrapper_expected_numeric_exit_code": 0,
        "wrapper_expected_signal": None, "wrapper_expected_stderr_empty": True,
        "wrapper_stdout_sha256": hashlib.sha256(wrapper_stdout).hexdigest(),
        "actual_child_numeric_exit_code": 2, "actual_child_signal": None,
        "actual_child_timed_out": False,
        "actual_child_validator_output_created": False,
        "actual_authority_pre_snapshot_sha256": pre["snapshot_sha256"],
        "actual_authority_post_snapshot_sha256": post["snapshot_sha256"],
        "actual_authority_pre_post_identical": pre == post,
        "private_case_root_cleaned": True,
        "request_file_sha256": request_record["sha256"],
        "request_object_sha256": request["request_sha256"],
        "exact_inventory": sorted(RUN_FILES), "member_file_sha256": members,
        "PASS_lock_file_sha256": hashlib.sha256(PASS_BYTES).hexdigest(),
        "formal_credit": 0, "manifest_authorized": False,
        "C27R2": "UNAUTHORIZED_PENDING_REPAIRED_RELEASE_CHAIN",
        "CM2": "NO-GO_FOR_CLAIM"}
    attestation = dict(body)
    attestation["run_attestation_sha256"] = digest(body)
    write_once(process_dir / "run_attestation.json",
               canonical(attestation) + b"\n")
    need({path.name for path in process_dir.iterdir()}
             == RUN_FILES - {"PASS.lock"},
         "exact ten files before PASS publication")
    for name, expected in members.items():
        need(capture_file(process_dir / name)[1]["sha256"] == expected,
             "current exact10 member before PASS")
    document, _ = closed_document(process_dir / "run_attestation.json",
                                  "run_attestation_sha256")
    need(document == attestation, "current canonical attestation before PASS")
    write_once(process_dir / "PASS.lock", PASS_BYTES)
    need({path.name for path in process_dir.iterdir()} == RUN_FILES,
         "exact eleven files after PASS publication")
    parent = os.open(process_dir, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
                     | getattr(os, "O_CLOEXEC", 0))
    try:
        os.fsync(parent)
    finally:
        os.close(parent)
    return wrapper_stdout


def execute(args: argparse.Namespace) -> bytes:
    python = Path(args.python).absolute()
    need(Path(sys.executable).absolute() == python
         and sys.flags.isolated == 1 and sys.dont_write_bytecode,
         "wrapper Python -I -B")
    expected_env = {"PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
                    "PYTHONHASHSEED": args.expected_python_hash_seed}
    need(dict(os.environ) == expected_env,
         "wrapper exact four-key minimal environment")
    self_payload, self_record = capture_file(SELF, 16 << 20)
    need(self_record["sha256"] == args.expect_wrapper_sha256,
         "wrapper current self pin")
    request, request_record = closed_document(Path(args.request),
                                              "request_sha256", 16 << 20)
    required = {"schema", "status", "case", "ordinal", "case_root",
        "process_dir", "validator_out_file", "validator_command",
        "validator_environment", "validator_environment_fixture",
        "validator_command_fixture", "authority_roots", "future_targets",
        "future_parent", "core_unit", "core_invocation_id",
        "control_timeout_seconds", "expected_authority_projection_sha256",
        "python_path", "python_sha256", "validator_path",
        "validator_sha256", "runner_path", "runner_sha256",
        "wrapper_path", "wrapper_sha256", "source_pins",
        "override_map_file_sha256", "override_map_object_sha256",
        "logical_override", "mutation", "barrier_mode",
        "private_copy_bytes",
        "formal_credit", "manifest_authorized", "C27R2", "CM2",
        "request_sha256"}
    need(set(request) == required and request["schema"] == REQUEST_SCHEMA
         and request["status"] == REQUEST_STATUS
         and type(request["case"]) is str and type(request["ordinal"]) is int
         and request["formal_credit"] == 0
         and request["manifest_authorized"] is False
         and request["C27R2"] == "UNAUTHORIZED"
         and request["CM2"] == "NO-GO_FOR_CLAIM",
         "exact zero-credit wrapper request schema")
    need(request["barrier_mode"] in {"none", "atomic", "toctou"},
         "exact wrapper barrier mode")
    need(request["python_path"] == str(python)
         and request["wrapper_path"] == str(SELF)
         and request["wrapper_sha256"] == args.expect_wrapper_sha256
         and request["python_sha256"]
             == capture_file(python, 64 << 20)[1]["sha256"],
         "wrapper/Python request current pins")
    validator = Path(request["validator_path"]).absolute()
    runner = Path(request["runner_path"]).absolute()
    need(capture_file(validator, 16 << 20)[1]["sha256"]
             == request["validator_sha256"]
         and capture_file(runner, 16 << 20)[1]["sha256"]
             == request["runner_sha256"],
         "validator/runner request current pins")
    command = request["validator_command"]
    need(request["validator_command_fixture"]
             in {"fixed", "missing-isolated"}
         and type(command) is list and len(command) > 8
         and all(type(item) is str for item in command),
         "validator child command fixture syntax")
    expected_prefix = ([str(python), "-I", "-B", str(validator)]
        if request["validator_command_fixture"] == "fixed"
        else [str(python), "-B", str(validator)])
    need(command[:len(expected_prefix)] == expected_prefix,
         "exact validator child command fixture prefix")
    child_environment = dict(expected_env)
    need(request["validator_environment_fixture"] in {"fixed", "wrong-hash"},
         "validator child environment fixture syntax")
    if request["validator_environment_fixture"] == "wrong-hash":
        child_environment["PYTHONHASHSEED"] = "1"
    need(request["validator_environment"] == child_environment,
         "validator child exact four-key fixture environment")
    case_root = Path(request["case_root"]).absolute()
    process_dir = Path(request["process_dir"]).absolute()
    out_file = Path(request["validator_out_file"]).absolute()
    need(case_root.is_dir() and not case_root.is_symlink()
         and out_file.parent == case_root and not out_file.exists()
         and not out_file.is_symlink() and not process_dir.exists()
         and not process_dir.is_symlink(), "fresh case output/process paths")
    pre = full_snapshot(request)
    need(pre["snapshot_sha256"]
             == request["expected_authority_projection_sha256"],
         "wrapper actual pre snapshot matches suite authority")
    started_at = utc_now()
    child: dict[str, Any] | None = None
    try:
        if request["barrier_mode"] == "none":
            child = invoke(command, child_environment,
                           request["control_timeout_seconds"])
        else:
            child = invoke_barrier(command, child_environment, case_root,
                request["barrier_mode"] == "toctou",
                request["control_timeout_seconds"])
        need(child["numeric_exit_code"] == 2 and child["signal"] is None
             and child["timed_out"] is False
             and child["capture_bounded"] is True
             and not out_file.exists() and not out_file.is_symlink(),
             "real validator child expected rejection/no output")
    finally:
        remove_private(case_root)
    need(not case_root.exists() and not case_root.is_symlink(),
         "wrapper cleaned private case root")
    post = full_snapshot(request)
    need(pre == post, "wrapper actual authority pre/post snapshots identical")
    need(child is not None, "validator child result captured")
    finished_at = utc_now()
    return write_transaction(process_dir, request, request_record, pre, post,
                             child, started_at, finished_at)


def self_test() -> dict[str, Any]:
    need(digest({"b": 2, "a": 1})
         == hashlib.sha256(b'{"a":1,"b":2}').hexdigest(),
         "canonical digest fixture")
    with tempfile.TemporaryDirectory(prefix="c27r2-real-case-wrapper-v1-") as raw:
        root = Path(raw)
        tree = root / "tree"
        tree.mkdir()
        empty = tree / "empty"
        empty.mkdir()
        payload = tree / "payload"
        payload.write_bytes(b"fixture\n")
        snapshot: dict[str, Any] = {}
        snapshot_node(tree, snapshot)
        need(any(record.get("node_type") == "directory"
                 and record.get("entry_count") == 0
                 for record in snapshot.values())
             and any(record.get("node_type") == "regular"
                     for record in snapshot.values()),
             "real empty-directory and regular-file snapshot fixture")
        target = root / "write-once"
        record = write_once(target, b"write-all-fixture\n")
        need(record["sha256"]
                 == hashlib.sha256(b"write-all-fixture\n").hexdigest()
             and len(record["stat_fingerprint"]) == 9,
             "write-all/fsync/reopen/full9stat fixture")
        symlink = tree / "bad-link"
        symlink.symlink_to(payload)
        try:
            snapshot_node(tree, {})
        except Rejected:
            pass
        else:
            raise Rejected("authority symlink fixture rejected")
    self_payload, _ = capture_file(SELF, 16 << 20)
    tree = ast.parse(self_payload, filename=str(SELF))
    need(all(not (isinstance(node, (ast.Import, ast.ImportFrom))
                      and any(alias.name.startswith("cm2_")
                              for alias in node.names))
             and not (isinstance(node, ast.Call)
                      and isinstance(node.func, ast.Name)
                      and node.func.id in {"exec", "eval", "compile"})
             for node in ast.walk(tree)),
         "wrapper has no formal source import/exec/eval/compile")
    return {"schema": RUN_SCHEMA + ".wrapper-self-test.v1",
        "status": "PASS_REAL_TREE_EMPTY_DIR_WRITE_ALL_REOPEN_AND_SYMLINK_"
                  "REJECTION_TINY_FIXTURES",
        "formal_reads": 0, "formal_outputs": 0, "formal_credit": 0,
        "manifest_authorized": False, "C27R2": "UNAUTHORIZED",
        "CM2": "NO-GO_FOR_CLAIM"}


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--self-test", action="store_true")
    value.add_argument("--request")
    value.add_argument("--expect-request-file-sha256")
    value.add_argument("--expect-request-object-sha256")
    value.add_argument("--python")
    value.add_argument("--expected-python-hash-seed")
    value.add_argument("--expect-wrapper-sha256")
    return value


def main() -> int:
    args = parser().parse_args()
    try:
        if args.self_test:
            result = self_test()
            stdout = canonical({"schema": result["schema"],
                "status": result["status"], "formal_credit": 0,
                "CM2": "NO-GO_FOR_CLAIM"}) + b"\n"
        else:
            need(all(getattr(args, name) is not None for name in
                ("request", "expect_request_file_sha256",
                 "expect_request_object_sha256", "python",
                 "expected_python_hash_seed", "expect_wrapper_sha256")),
                 "all wrapper arguments required")
            need(valid_sha(args.expect_request_file_sha256)
                 and valid_sha(args.expect_request_object_sha256)
                 and valid_sha(args.expect_wrapper_sha256),
                 "wrapper SHA arguments exact")
            request, record = closed_document(Path(args.request),
                                              "request_sha256", 16 << 20)
            need(record["sha256"] == args.expect_request_file_sha256
                 and request["request_sha256"]
                     == args.expect_request_object_sha256,
                 "wrapper request file/object CLI pins")
            stdout = execute(args)
        sys.stdout.buffer.write(stdout)
        return 0
    except (Rejected, OSError, ValueError, KeyError, TypeError,
            subprocess.SubprocessError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
