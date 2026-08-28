#!/usr/bin/env python3
"""Fail-closed one-shot launcher for the bridge-v5 composite finalizer.

This launcher is a narrow post-exit gate.  It accepts only the exact fresh
same-token finalizer unit, an exact clean active/exited worker unit, and the
non-authoritative READY tree with no failure or composite artifacts.  It then
execves systemd-run with the held-source 20-token finalizer command.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import tempfile
import types
from typing import Any, Mapping, Sequence


ROOT = Path("/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572")
DELIVERABLES = ROOT / "deliverables"
AUDIT = ROOT / ".cm2-runtime/audit"
CONTROL = ROOT / ".cm2-runtime/control"
SELF = DELIVERABLES / (
    "cm2_round306c30c_postreceipt_v3_p1_bridge_v5_"
    "composite_finalizer_launcher_v1.py")
WATCHER = DELIVERABLES / "cm2_round306c30c_postreceipt_v3_p1_bridge_watch_v5.py"
GATE = DELIVERABLES / "cm2_round306c30c_postreceipt_v3_p1_bridge_start_gate_v2.py"
FINALIZER = DELIVERABLES / (
    "cm2_round306c30c_postreceipt_v3_p1_bridge_v5_"
    "post_exit_composite_finalizer_v1.py")
WRAPPER = DELIVERABLES / "cm2_round306c30c_postreceipt_bridge_v3_process_wrapper_v1.py"

PYTHON = Path("/usr/bin/python3.12")
SYSTEMD_RUN = Path("/usr/bin/systemd-run")
SYSTEMCTL = Path("/usr/bin/systemctl")
RUNTIME_DIR = Path("/run/user/1000")
BUS_SOCKET = RUNTIME_DIR / "bus"

# Exact append-only frozen v5 source pins.
WATCHER_SHA256 = "3c62736ac55a825096116d6ca2762555bae1387a56a5caab2f0d7fbe9dd82c60"
GATE_SHA256 = "430f9c3e987746d0423a7a1bfbe7457bb94ae2d65c32ede8d3e18a887e95e10a"
FINALIZER_SHA256 = "cf21e006da01904d85ec8c38c984889553c458cebcb8d324624225ebb180d1bd"
WRAPPER_SHA256 = "31fdde13acdbffbcd398c3148a22818fb2b83212a94e2ae8550103acaec9ab81"
PYTHON_SHA256 = "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118"
SYSTEMD_RUN_SHA256 = "49f0bf95eb8a781b93853bf9fc981b4929dd0009f55a3e6db95534c0a2d11716"
SYSTEMCTL_SHA256 = "7ba82b5ba146759c710e1b80fadaa3fdbc0f9b85c8fb2c8c3196b7b1a0037ef8"

SOURCE_SIZES = {
    WATCHER: 155_299,
    GATE: 9_086,
    FINALIZER: 106_248,
    WRAPPER: 35_559,
    PYTHON: 8_020_928,
    SYSTEMD_RUN: 68_392,
    SYSTEMCTL: 1_501_304,
}

EXACT_ENVIRONMENT = {
    "HOME": "/nonexistent",
    "PATH": "/usr/bin:/bin",
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "XDG_RUNTIME_DIR": "/run/user/1000",
    "DBUS_SESSION_BUS_ADDRESS": "unix:path=/run/user/1000/bus",
}

READY_BYTES = b"READY_C30C_POSTRECEIPT_BRIDGE_V5_AWAITING_COMPOSITE_FINALIZER\n"
PREPARED_COMPOSITE = ".COMPOSITE_PASS.lock.prepared-v1"
RUNNING_ATTESTATION = "composite_finalizer_running_service_attestation.json"
COMPOSITE_RECEIPT = "composite_receipt.json"
COMPOSITE_MARKER = "COMPOSITE_PASS.lock"
FORBIDDEN_READY_NAMES = frozenset({
    PREPARED_COMPOSITE, RUNNING_ATTESTATION, COMPOSITE_RECEIPT,
    COMPOSITE_MARKER, "FAILED.lock", "failure_receipt.json", "PASS.lock",
})

TOKEN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:-]{7,70}")
HEX64 = re.compile(r"[0-9a-f]{64}")
INVOCATION = re.compile(r"[0-9a-f]{32}")
WORKER_UNIT = re.compile(
    r"cm2-c30c-postreceipt-v3-p1-bridge-v5-[A-Za-z0-9_.:-]+\.service")
FINALIZER_UNIT = re.compile(
    r"cm2-c30c-postreceipt-v3-p1-bridge-v5-finalizer-"
    r"[A-Za-z0-9_.:-]+\.service")
FORBIDDEN_ARG_BYTES = frozenset(b"'\"\\$%")
SELFTEST_STATUS = (
    "PASS_TEMP_ONLY_V5_POST_EXIT_GATE_EXACT_20_FINALIZER_ARGV_"
    "NO_SERVICE_ZERO_CREDIT")

WORKER_PROPERTIES = (
    "Id", "InvocationID", "ExecStart", "ExecStartPre", "FragmentPath",
    "LoadState", "ActiveState", "SubState", "Result", "ExecMainCode",
    "ExecMainStatus", "MainPID", "ControlPID", "Type", "RemainAfterExit",
    "StandardOutput", "StandardError",
)


class Rejected(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Rejected(label)


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
        value.st_uid, value.st_gid, value.st_size,
        value.st_mtime_ns, value.st_ctime_ns,
    )


class HeldFile:
    def __init__(
        self, path: Path, expected_sha256: str, expected_size: int | None,
        expected_mode: int, expected_uid: int, expected_gid: int,
    ) -> None:
        need(HEX64.fullmatch(expected_sha256) is not None,
             "lowercase source SHA pin:" + path.name)
        self.path = path
        before = path.lstat()
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1
             and stat.S_IMODE(before.st_mode) == expected_mode
             and before.st_uid == expected_uid and before.st_gid == expected_gid
             and (expected_size is None or before.st_size == expected_size),
             "frozen exact source stat:" + path.name)
        self.fd = os.open(
            path, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
        )
        try:
            opened = os.fstat(self.fd)
            need(fingerprint(opened) == fingerprint(before),
                 "source open race:" + path.name)
            chunks: list[bytes] = []
            remaining = opened.st_size
            while remaining:
                block = os.read(self.fd, min(1 << 20, remaining))
                need(bool(block), "complete source read:" + path.name)
                chunks.append(block)
                remaining -= len(block)
            need(os.read(self.fd, 1) == b"", "exact source EOF:" + path.name)
            self.raw = b"".join(chunks)
            self.sha256 = hashlib.sha256(self.raw).hexdigest()
            self.initial = fingerprint(opened)
            need(self.sha256 == expected_sha256,
                 "frozen exact source SHA:" + path.name)
            self.verify()
        except BaseException:
            os.close(self.fd)
            raise

    def verify(self) -> None:
        need(fingerprint(self.path.lstat()) == self.initial
             and fingerprint(os.fstat(self.fd)) == self.initial,
             "held source identity replay:" + self.path.name)
        os.lseek(self.fd, 0, os.SEEK_SET)
        digest = hashlib.sha256()
        remaining = self.initial[6]
        while remaining:
            block = os.read(self.fd, min(1 << 20, remaining))
            need(bool(block), "held source replay progress:" + self.path.name)
            digest.update(block)
            remaining -= len(block)
        need(os.read(self.fd, 1) == b"" and digest.hexdigest() == self.sha256,
             "held source byte replay:" + self.path.name)

    def close(self) -> None:
        os.close(self.fd)


class HeldDirectory:
    def __init__(self, path: Path) -> None:
        self.path = path
        before = path.lstat()
        need(stat.S_ISDIR(before.st_mode) and before.st_uid == os.getuid()
             and before.st_gid == os.getgid() and stat.S_IMODE(before.st_mode) == 0o700,
             "exact private owned directory:" + str(path))
        self.fd = os.open(
            path, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC
            | getattr(os, "O_NOFOLLOW", 0),
        )
        self.initial = fingerprint(os.fstat(self.fd))
        need(self.initial == fingerprint(before), "directory open race:" + str(path))

    def verify(self) -> None:
        need(fingerprint(self.path.lstat()) == self.initial
             and fingerprint(os.fstat(self.fd)) == self.initial,
             "held directory identity:" + str(self.path))

    def names(self) -> set[str]:
        self.verify()
        return set(os.listdir(self.fd))

    def read_regular(self, name: str, maximum: int) -> tuple[bytes, tuple[int, ...]]:
        need(name and "/" not in name and name not in {".", ".."},
             "direct child token")
        before = os.stat(name, dir_fd=self.fd, follow_symlinks=False)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1
             and stat.S_IMODE(before.st_mode) == 0o400
             and before.st_uid == os.getuid() and before.st_gid == os.getgid()
             and 0 <= before.st_size <= maximum,
             "exact frozen direct regular:" + name)
        fd = os.open(
            name, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
            dir_fd=self.fd,
        )
        try:
            opened = os.fstat(fd)
            chunks: list[bytes] = []
            remaining = opened.st_size
            while remaining:
                block = os.read(fd, min(1 << 20, remaining))
                need(bool(block), "direct child read progress:" + name)
                chunks.append(block)
                remaining -= len(block)
            need(os.read(fd, 1) == b"", "direct child exact EOF:" + name)
            after = os.fstat(fd)
        finally:
            os.close(fd)
        current = os.stat(name, dir_fd=self.fd, follow_symlinks=False)
        need(fingerprint(before) == fingerprint(opened)
             == fingerprint(after) == fingerprint(current),
             "stable direct child:" + name)
        return b"".join(chunks), fingerprint(opened)

    def close(self) -> None:
        os.close(self.fd)


def safe_token(value: Any, label: str) -> str:
    need(type(value) is str and value != "", "nonempty argv token:" + label)
    try:
        raw = value.encode("ascii")
    except UnicodeEncodeError as error:
        raise Rejected("ASCII argv token:" + label) from error
    need(all(0x21 <= byte <= 0x7e for byte in raw)
         and not (set(raw) & FORBIDDEN_ARG_BYTES) and value != ";",
         "systemd-show-lossless argv token:" + label)
    return value


def safe_argv(value: Sequence[str], label: str) -> list[str]:
    result = list(value)
    need(bool(result), "nonempty argv:" + label)
    for item in result:
        safe_token(item, label)
    return result


def validate_token(value: Any) -> str:
    need(type(value) is str and TOKEN.fullmatch(value) is not None,
         "launch-token exact safe syntax")
    return value


def namespace_paths(
    audit: Path, control: Path, launch_token: str,
) -> tuple[str, str, str, Path, Path, Path]:
    token = validate_token(launch_token)
    name = "c30c-postreceipt-v3-p1-bridge-v5-" + token
    worker = "cm2-" + name + ".service"
    finalizer = (
        "cm2-c30c-postreceipt-v3-p1-bridge-v5-finalizer-" + token + ".service")
    need(WORKER_UNIT.fullmatch(worker) is not None
         and FINALIZER_UNIT.fullmatch(finalizer) is not None
         and worker != finalizer, "exact distinct same-token units")
    bridge = audit / name
    control_dir = control / name
    need(bridge.parent == audit and control_dir.parent == control
         and bridge.name == control_dir.name,
         "matched direct audit/control sibling names")
    return name, worker, finalizer, bridge, control_dir, control_dir / "pinset.json"


def load_frozen_modules(
    watcher_held: HeldFile, finalizer_held: HeldFile,
) -> tuple[types.ModuleType, types.ModuleType]:
    watcher_held.verify()
    watcher = types.ModuleType("_cm2_bridge_watch_v5_finalizer_launcher_held")
    watcher.__file__ = os.fspath(WATCHER)
    watcher.__package__ = ""
    sys.modules[watcher.__name__] = watcher
    exec(compile(watcher_held.raw, os.fspath(WATCHER), "exec"), watcher.__dict__)
    watcher_held.verify()
    need(watcher.WATCHER == WATCHER and watcher.START_GATE == GATE
         and watcher.COMPOSITE_FINALIZER == FINALIZER and watcher.WRAPPER == WRAPPER
         and watcher.FINAL_PYTHON == PYTHON and watcher.AUDIT == AUDIT
         and watcher.CONTROL == CONTROL
         and watcher.CONTROL_ENV == EXACT_ENVIRONMENT,
         "held watcher exact v5 launch constants")

    finalizer_held.verify()
    finalizer = types.ModuleType("_cm2_bridge_v5_composite_finalizer_launcher_held")
    finalizer.__file__ = os.fspath(FINALIZER)
    finalizer.__package__ = ""
    sys.modules[finalizer.__name__] = finalizer
    exec(compile(finalizer_held.raw, os.fspath(FINALIZER), "exec"), finalizer.__dict__)
    finalizer_held.verify()
    need(finalizer.SELF == FINALIZER and finalizer.FINAL_PYTHON == PYTHON
         and finalizer.SYSTEMCTL == SYSTEMCTL and finalizer.AUDIT == AUDIT
         and finalizer.CONTROL == CONTROL
         and finalizer.CONTROL_ENV == EXACT_ENVIRONMENT
         and finalizer.READY_BYTES == READY_BYTES
         and finalizer.PREPARED_COMPOSITE == PREPARED_COMPOSITE
         and finalizer.RUNNING_ATTESTATION_NAME == RUNNING_ATTESTATION
         and finalizer.COMPOSITE_RECEIPT_NAME == COMPOSITE_RECEIPT
         and finalizer.COMPOSITE_MARKER_NAME == COMPOSITE_MARKER,
         "held finalizer exact interface/constants")
    return watcher, finalizer


def expected_argvs(
    watcher_module: types.ModuleType, finalizer_module: types.ModuleType,
    bridge: Path, control_dir: Path, worker_unit: str, finalizer_unit: str,
    maximum_wait_seconds: int,
) -> tuple[list[str], list[str], list[str]]:
    pinset = control_dir / "pinset.json"
    anchor = control_dir / "launch-anchor.json"
    mapping_bridge = bridge if bridge.parent == AUDIT else AUDIT / bridge.name
    need(watcher_module.finalizer_unit_for_worker(mapping_bridge, worker_unit)
         == finalizer_unit,
         "held watcher exact same-token composite finalizer unit")
    watcher = watcher_module.expected_watcher_argv(
        bridge, pinset, anchor, worker_unit, maximum_wait_seconds, WATCHER_SHA256,
    )
    gate = watcher_module.expected_gate_argv(
        bridge, pinset, anchor, worker_unit, maximum_wait_seconds, GATE_SHA256,
        WATCHER_SHA256,
    )
    finalizer = finalizer_module.expected_execstart_argv(
        bridge, pinset, anchor, worker_unit, finalizer_unit,
        maximum_wait_seconds, FINALIZER_SHA256,
    )
    need(len(watcher) == 18 and len(gate) == 20 and len(finalizer) == 20,
         "exact watcher18/gate20/finalizer20 argv cardinality")
    need(watcher == safe_argv(watcher, "watcher18")
         and gate == safe_argv(gate, "gate20")
         and finalizer == safe_argv(finalizer, "finalizer20"),
         "exact shell-neutral worker/gate/finalizer argv")
    return watcher, gate, finalizer


def finalizer_systemd_run_argv(unit: str, finalizer: list[str]) -> list[str]:
    command = [
        os.fspath(SYSTEMD_RUN), "--user", "--expand-environment=no",
        "--unit=" + unit, "--service-type=exec", "--remain-after-exit",
        "--property=StandardOutput=journal", "--property=StandardError=journal",
        "--", *finalizer,
    ]
    need(len(command) == 29 and command[9:] == finalizer,
         "exact systemd-run nine-token prefix plus finalizer20")
    for item in command:
        safe_token(item, "finalizer systemd-run")
    return command


def source_holds(expect_self_sha256: str, formal: bool) -> dict[str, HeldFile]:
    need(HEX64.fullmatch(expect_self_sha256) is not None,
         "launcher expected lowercase SHA")
    self_mode = 0o444 if formal else stat.S_IMODE(SELF.lstat().st_mode)
    need(self_mode in {0o444, 0o644, 0o664},
         "launcher selftest development/frozen mode")
    specifications = {
        "launcher": (SELF, expect_self_sha256, None, self_mode, 1000, 1000),
        "watcher_v5": (WATCHER, WATCHER_SHA256, SOURCE_SIZES[WATCHER], 0o444, 1000, 1000),
        "start_gate_v2": (GATE, GATE_SHA256, SOURCE_SIZES[GATE], 0o444, 1000, 1000),
        "composite_finalizer": (FINALIZER, FINALIZER_SHA256, SOURCE_SIZES[FINALIZER], 0o444, 1000, 1000),
        "wrapper_v1": (WRAPPER, WRAPPER_SHA256, SOURCE_SIZES[WRAPPER], 0o444, 1000, 1000),
        "python": (PYTHON, PYTHON_SHA256, SOURCE_SIZES[PYTHON], 0o755, 0, 0),
        "systemd_run": (SYSTEMD_RUN, SYSTEMD_RUN_SHA256, SOURCE_SIZES[SYSTEMD_RUN], 0o755, 0, 0),
        "systemctl": (SYSTEMCTL, SYSTEMCTL_SHA256, SOURCE_SIZES[SYSTEMCTL], 0o755, 0, 0),
    }
    result: dict[str, HeldFile] = {}
    try:
        for role, specification in specifications.items():
            result[role] = HeldFile(*specification)
        return result
    except BaseException:
        for held in result.values():
            held.close()
        raise


def verify_holds(holds: Mapping[str, HeldFile]) -> None:
    need(set(holds) == {
        "launcher", "watcher_v5", "start_gate_v2", "composite_finalizer",
        "wrapper_v1", "python", "systemd_run", "systemctl",
    }, "exact v5 finalizer-launcher source/tool pin roles")
    for held in holds.values():
        held.verify()


def verify_exact_runtime() -> None:
    need(Path(sys.executable) == PYTHON and sys.flags.isolated == 1
         and sys.dont_write_bytecode,
         "exact /usr/bin/python3.12 -I -B launcher runtime")
    need(dict(os.environ) == EXACT_ENVIRONMENT,
         "exact minimal six-variable user-bus environment")
    runtime = RUNTIME_DIR.lstat()
    bus = BUS_SOCKET.lstat()
    need(stat.S_ISDIR(runtime.st_mode) and stat.S_IMODE(runtime.st_mode) == 0o700
         and runtime.st_uid == 1000 and runtime.st_gid == 1000,
         "exact owned user runtime directory")
    need(stat.S_ISSOCK(bus.st_mode) and bus.st_uid == 1000,
         "exact owned user bus socket")


def parse_systemctl(raw: bytes) -> dict[str, str]:
    try:
        rows = raw.decode("ascii").splitlines()
    except UnicodeDecodeError as error:
        raise Rejected("systemctl ASCII") from error
    result: dict[str, str] = {}
    for row in rows:
        key, separator, value = row.partition("=")
        need(separator == "=" and key and key not in result,
             "unique systemctl property")
        result[key] = value
    return result


def query_unit(
    unit: str, properties: Sequence[str], systemctl: HeldFile,
) -> dict[str, str]:
    systemctl.verify()
    command = [os.fspath(SYSTEMCTL), "--user", "show", unit]
    for key in properties:
        command.extend(["-p", key])
    completed = subprocess.run(
        command, cwd=ROOT, env=EXACT_ENVIRONMENT, stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    systemctl.verify()
    need(completed.returncode == 0 and completed.stderr == b"",
         "clean exact systemctl query")
    fields = parse_systemctl(completed.stdout)
    need(set(fields) == set(properties), "exact systemctl property set")
    return fields


def unit_absent(unit: str, systemctl: HeldFile) -> None:
    fields = query_unit(unit, ("LoadState",), systemctl)
    need(fields == {"LoadState": "not-found"},
         "fresh finalizer unit is exactly not-found")


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
    expected = safe_argv(expected_argv, label)
    need(path == os.fspath(PYTHON) and argv_text == " ".join(expected),
         "exact ExecStart argv/path:" + label)
    result = {
        "start": start, "stop": stop, "pid": int(pid),
        "code": code, "status": status_text,
    }
    retained = (
        result["pid"] > 1 and result["start"] not in {"", "n/a"}
        and result["stop"] not in {"", "n/a"}
        and result["code"] == "exited" and result["status"] in {"0", "0/0"}
    )
    decayed = (
        result["pid"] == 0 and result["start"] == "n/a"
        and result["stop"] == "n/a" and result["code"] == "(null)"
        and result["status"] in {"0", "0/0"}
    )
    need(retained or decayed, "successful completed/decayed projection:" + label)
    return result


def validate_worker_post_exit(
    fields: Mapping[str, str], worker_unit: str, watcher_argv: Sequence[str],
    gate_argv: Sequence[str],
) -> None:
    need(fields.get("Id") == worker_unit
         and INVOCATION.fullmatch(fields.get("InvocationID", "")) is not None
         and fields.get("FragmentPath")
             == "/run/user/1000/systemd/transient/" + worker_unit
         and fields.get("LoadState") == "loaded"
         and fields.get("ActiveState") == "active"
         and fields.get("SubState") == "exited"
         and fields.get("Result") == "success"
         and fields.get("ExecMainCode") == "1"
         and fields.get("ExecMainStatus") == "0"
         and fields.get("MainPID") == "0" and fields.get("ControlPID") == "0"
         and fields.get("Type") == "exec"
         and fields.get("RemainAfterExit") == "yes"
         and fields.get("StandardOutput") == "journal"
         and fields.get("StandardError") == "journal",
         "worker exact clean active/exited terminal tuple")
    parse_exec_command(fields["ExecStart"], watcher_argv, "worker ExecStart")
    parse_exec_command(fields["ExecStartPre"], gate_argv, "worker ExecStartPre")


def validate_ready_namespace(bridge: HeldDirectory) -> None:
    names = bridge.names()
    need("READY.lock" in names and names.isdisjoint(FORBIDDEN_READY_NAMES),
         "READY present with no failure/PASS/composite artifacts")
    raw, _state = bridge.read_regular("READY.lock", 128)
    need(raw == READY_BYTES, "exact non-authoritative READY bytes")
    bridge.verify()


def self_test(
    launch_token: str, maximum_wait_seconds: int, expect_self_sha256: str,
) -> dict[str, Any]:
    holds = source_holds(expect_self_sha256, False)
    try:
        watcher_module, finalizer_module = load_frozen_modules(
            holds["watcher_v5"], holds["composite_finalizer"],
        )
        with tempfile.TemporaryDirectory(prefix="c30c-v5-finalizer-launcher-") as raw:
            root = Path(raw)
            audit = root / "audit"
            control = root / "control"
            os.mkdir(audit, 0o700)
            os.mkdir(control, 0o700)
            name, worker, finalizer_unit, bridge, control_dir, _pinset = namespace_paths(
                audit, control, launch_token,
            )
            watcher, gate, finalizer = expected_argvs(
                watcher_module, finalizer_module, bridge, control_dir, worker,
                finalizer_unit, maximum_wait_seconds,
            )
            command = finalizer_systemd_run_argv(finalizer_unit, finalizer)
            need(name == bridge.name == control_dir.name
                 and len(command) == 29 and command[9:] == finalizer,
                 "temp-only exact same-token finalizer command")

            fake_fields = {
                "Id": worker, "InvocationID": "1" * 32,
                "ExecStart": _exec_fixture(watcher, 5001),
                "ExecStartPre": _exec_fixture(gate, 5000),
                "FragmentPath": "/run/user/1000/systemd/transient/" + worker,
                "LoadState": "loaded", "ActiveState": "active",
                "SubState": "exited", "Result": "success",
                "ExecMainCode": "1", "ExecMainStatus": "0",
                "MainPID": "0", "ControlPID": "0", "Type": "exec",
                "RemainAfterExit": "yes", "StandardOutput": "journal",
                "StandardError": "journal",
            }
            validate_worker_post_exit(fake_fields, worker, watcher, gate)
            decayed_fields = dict(fake_fields)
            decayed_fields["ExecStart"] = _exec_decayed_fixture(watcher)
            decayed_fields["ExecStartPre"] = _exec_decayed_fixture(gate)
            validate_worker_post_exit(
                decayed_fields, worker, watcher, gate,
            )
            failed = dict(fake_fields)
            failed["Result"] = "exit-code"
            need(_rejected(lambda: validate_worker_post_exit(
                failed, worker, watcher, gate,
            )), "temp-only failed worker rejected")
            stale = dict(fake_fields)
            stale["ExecStart"] = _exec_stale_zero_pid_fixture(watcher)
            need(_rejected(lambda: validate_worker_post_exit(
                stale, worker, watcher, gate,
            )), "temp-only stale pid-zero/non-n-a worker metadata rejected")
        verify_holds(holds)
        return {
            "schema": (
                "cm2.round306c30c.postreceipt-bridge-v5-"
                "composite-finalizer-launcher-self-test.v1"),
            "status": SELFTEST_STATUS,
            "watcher_argv_count": 18,
            "gate_argv_count": 20,
            "finalizer_argv_count": 20,
            "systemd_run_argv_count": 29,
            "retained_worker_projection_accepted": True,
            "decayed_worker_projection_accepted": True,
            "failed_worker_rejected": True,
            "stale_worker_metadata_rejected": True,
            "pinned_source_role_count": len(holds),
            "formal_namespace_reads": 0,
            "formal_namespace_writes": 0,
            "service_operations": 0,
            "formal_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        }
    finally:
        for held in holds.values():
            held.close()


def _exec_fixture(argv: Sequence[str], pid: int) -> str:
    return (
        "{ path=/usr/bin/python3.12 ; argv[]=" + " ".join(argv)
        + " ; ignore_errors=no ; start_time=[Sun 2026-08-09 00:00:00 UTC]"
        + " ; stop_time=[Sun 2026-08-09 00:00:01 UTC] ; pid=" + str(pid)
        + " ; code=exited ; status=0 }")


def _exec_decayed_fixture(argv: Sequence[str]) -> str:
    return (
        "{ path=/usr/bin/python3.12 ; argv[]=" + " ".join(argv)
        + " ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0"
        + " ; code=(null) ; status=0 }")


def _exec_stale_zero_pid_fixture(argv: Sequence[str]) -> str:
    return (
        "{ path=/usr/bin/python3.12 ; argv[]=" + " ".join(argv)
        + " ; ignore_errors=no ; start_time=[Sun 2026-08-09 00:00:00 UTC]"
        + " ; stop_time=[Sun 2026-08-09 00:00:01 UTC] ; pid=0"
        + " ; code=exited ; status=0 }")


def _rejected(call: Any) -> bool:
    try:
        call()
    except (Rejected, OSError, ValueError, TypeError, KeyError):
        return True
    return False


def execute(
    launch_token: str, maximum_wait_seconds: int, expect_self_sha256: str,
) -> None:
    holds = source_holds(expect_self_sha256, True)
    bridge: HeldDirectory | None = None
    control_dir: HeldDirectory | None = None
    try:
        need(AUDIT.is_dir() and CONTROL.is_dir(), "formal audit/control parents")
        name, worker_unit, finalizer_unit, bridge_path, control_path, _pinset = (
            namespace_paths(AUDIT, CONTROL, launch_token)
        )
        need(name == bridge_path.name == control_path.name,
             "formal exact same-token namespace")
        watcher_module, finalizer_module = load_frozen_modules(
            holds["watcher_v5"], holds["composite_finalizer"],
        )
        watcher, gate, finalizer = expected_argvs(
            watcher_module, finalizer_module, bridge_path, control_path,
            worker_unit, finalizer_unit, maximum_wait_seconds,
        )
        command = finalizer_systemd_run_argv(finalizer_unit, finalizer)

        bridge = HeldDirectory(bridge_path)
        control_dir = HeldDirectory(control_path)
        control_names = control_dir.names()
        need({"pinset.json", "launch-anchor.json"}.issubset(control_names),
             "existing exact v5 gate materials")
        control_dir.read_regular("pinset.json", 16 << 20)
        control_dir.read_regular("launch-anchor.json", 8 << 20)
        validate_ready_namespace(bridge)
        unit_absent(finalizer_unit, holds["systemctl"])
        fields = query_unit(worker_unit, WORKER_PROPERTIES, holds["systemctl"])
        validate_worker_post_exit(fields, worker_unit, watcher, gate)

        verify_holds(holds)
        bridge.verify()
        control_dir.verify()
        validate_ready_namespace(bridge)
        unit_absent(finalizer_unit, holds["systemctl"])
        fields = query_unit(worker_unit, WORKER_PROPERTIES, holds["systemctl"])
        validate_worker_post_exit(fields, worker_unit, watcher, gate)
        verify_holds(holds)
        bridge.verify()
        control_dir.verify()
        os.execve(os.fspath(SYSTEMD_RUN), command, EXACT_ENVIRONMENT)
        raise Rejected("systemd-run execve unexpectedly returned")
    finally:
        for held in (control_dir, bridge):
            if held is not None:
                held.close()
        for held in holds.values():
            held.close()


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--self-test", action="store_true")
    value.add_argument("--launch-token", required=True)
    value.add_argument("--expect-self-sha256", required=True)
    value.add_argument("--maximum-wait-seconds", required=True, type=int)
    return value


def main() -> int:
    arguments = parser().parse_args()
    try:
        verify_exact_runtime()
        token = validate_token(arguments.launch_token)
        need(type(arguments.maximum_wait_seconds) is int
             and 0 <= arguments.maximum_wait_seconds <= 7 * 24 * 3600,
             "bounded explicit maximum-wait-seconds")
        if arguments.self_test:
            result = self_test(
                token, arguments.maximum_wait_seconds,
                arguments.expect_self_sha256,
            )
            sys.stdout.write(json.dumps(
                result, sort_keys=True, separators=(",", ":"),
                ensure_ascii=True, allow_nan=False,
            ) + "\n")
            return 0
        execute(token, arguments.maximum_wait_seconds, arguments.expect_self_sha256)
        raise Rejected("launcher execute unexpectedly returned")
    except (Rejected, OSError, ValueError, TypeError, KeyError,
            subprocess.SubprocessError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
