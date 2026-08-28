#!/usr/bin/env python3
"""Fail-closed one-shot launcher for the C30c bridge-v5 worker.

The launcher creates matched fresh audit/control namespaces and then execves
systemd-run.  The separately pinned ExecStartPre gate publishes pinset.json
first and launch-anchor.json last.  The worker may publish only a
non-authoritative READY marker; a separate post-exit finalizer is required.
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
from typing import Any, Sequence


ROOT = Path("/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572")
DELIVERABLES = ROOT / "deliverables"
AUDIT = ROOT / ".cm2-runtime/audit"
CONTROL = ROOT / ".cm2-runtime/control"
SELF = DELIVERABLES / (
    "cm2_round306c30c_postreceipt_v3_p1_bridge_v5_one_shot_launcher_v2.py")
WATCHER = DELIVERABLES / "cm2_round306c30c_postreceipt_v3_p1_bridge_watch_v6.py"
GATE = DELIVERABLES / "cm2_round306c30c_postreceipt_v3_p1_bridge_start_gate_v3.py"
FINALIZER = DELIVERABLES / (
    "cm2_round306c30c_postreceipt_v3_p1_bridge_v5_"
    "post_exit_composite_finalizer_v2.py")
WRAPPER = DELIVERABLES / "cm2_round306c30c_postreceipt_bridge_v3_process_wrapper_v1.py"

PYTHON = Path("/usr/bin/python3.12")
SYSTEMD_RUN = Path("/usr/bin/systemd-run")
SYSTEMCTL = Path("/usr/bin/systemctl")
RUNTIME_DIR = Path("/run/user/1000")
BUS_SOCKET = RUNTIME_DIR / "bus"

# Exact append-only frozen v5 source pins.
WATCHER_SHA256 = "7c56e7f39e50c926fe126f703b28746383f64f9f2be18592ce1a470b805480d9"
GATE_SHA256 = "cd4bbf4005de1c88429eb60cea8f8492c1eab2db81dc883d54117d58631d75f6"
FINALIZER_SHA256 = "b35a215a7510a3e7f87978aa61b4050b2e5d77cb1a3054010287073b4a001949"
WRAPPER_SHA256 = "31fdde13acdbffbcd398c3148a22818fb2b83212a94e2ae8550103acaec9ab81"
PYTHON_SHA256 = "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118"
SYSTEMD_RUN_SHA256 = "49f0bf95eb8a781b93853bf9fc981b4929dd0009f55a3e6db95534c0a2d11716"
SYSTEMCTL_SHA256 = "7ba82b5ba146759c710e1b80fadaa3fdbc0f9b85c8fb2c8c3196b7b1a0037ef8"

SOURCE_SIZES = {
    WATCHER: 158_466,
    GATE: 9_098,
    FINALIZER: 112_885,
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

TOKEN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:-]{7,70}")
HEX64 = re.compile(r"[0-9a-f]{64}")
UNIT = re.compile(
    r"cm2-c30c-postreceipt-v3-p1-bridge-v5-[A-Za-z0-9_.:-]+\.service")
FORBIDDEN_ARG_BYTES = frozenset(b"'\"\\$%")
SELFTEST_STATUS = (
    "PASS_TEMP_ONLY_V5_EXACT_18_WATCHER_20_GATE_ARGV_FINALIZER_PINNED_"
    "NO_SERVICE_ZERO_CREDIT")


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
        state = hashlib.sha256()
        remaining = self.initial[6]
        while remaining:
            block = os.read(self.fd, min(1 << 20, remaining))
            need(bool(block), "held source replay progress:" + self.path.name)
            state.update(block)
            remaining -= len(block)
        need(os.read(self.fd, 1) == b"" and state.hexdigest() == self.sha256,
             "held source byte replay:" + self.path.name)

    def close(self) -> None:
        os.close(self.fd)


class HeldDirectory:
    def __init__(self, path: Path) -> None:
        self.path = path
        before = path.lstat()
        need(stat.S_ISDIR(before.st_mode) and before.st_uid == os.getuid()
             and before.st_gid == os.getgid(), "owned directory:" + str(path))
        self.fd = os.open(
            path, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC
            | getattr(os, "O_NOFOLLOW", 0),
        )
        self.initial = fingerprint(os.fstat(self.fd))
        need(self.initial == fingerprint(before), "directory open race:" + str(path))

    def verify(self) -> None:
        need(fingerprint(self.path.lstat()) == self.initial
             and fingerprint(os.fstat(self.fd)) == self.initial,
             "held parent directory identity:" + str(self.path))

    def absent(self, name: str) -> None:
        try:
            os.stat(name, dir_fd=self.fd, follow_symlinks=False)
        except FileNotFoundError:
            return
        raise Rejected("fresh absent direct sibling:" + name)

    def create_empty_0700(self, name: str) -> "HeldDirectory":
        self.verify()
        self.absent(name)
        prior = self.initial
        os.mkdir(name, 0o700, dir_fd=self.fd)
        os.fsync(self.fd)
        after = os.fstat(self.fd)
        current = self.path.lstat()
        need((after.st_dev, after.st_ino) == (prior[0], prior[1])
             and fingerprint(after) == fingerprint(current),
             "held parent directory after controlled mkdir:" + name)
        self.initial = fingerprint(after)
        state = os.stat(name, dir_fd=self.fd, follow_symlinks=False)
        need(stat.S_ISDIR(state.st_mode) and stat.S_IMODE(state.st_mode) == 0o700
             and state.st_uid == os.getuid() and state.st_gid == os.getgid(),
             "new direct sibling exact 0700 owned directory:" + name)
        child = HeldDirectory(self.path / name)
        need(os.listdir(child.fd) == [], "new direct sibling initially empty:" + name)
        self.verify()
        return child

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
) -> tuple[str, str, Path, Path, Path, Path]:
    token = validate_token(launch_token)
    name = "c30c-postreceipt-v3-p1-bridge-v5-" + token
    unit = "cm2-" + name + ".service"
    need(UNIT.fullmatch(unit) is not None, "exact fresh bridge-v5 unit syntax")
    bridge = audit / name
    control_dir = control / name
    pinset = control_dir / "pinset.json"
    anchor = control_dir / "launch-anchor.json"
    need(bridge.parent == audit and control_dir.parent == control
         and bridge.name == control_dir.name,
         "matched direct audit/control sibling names")
    return name, unit, bridge, control_dir, pinset, anchor


def load_frozen_watcher(held: HeldFile) -> types.ModuleType:
    held.verify()
    module = types.ModuleType("_cm2_bridge_watch_v6_launcher_held")
    module.__file__ = os.fspath(WATCHER)
    module.__package__ = ""
    sys.modules[module.__name__] = module
    exec(compile(held.raw, os.fspath(WATCHER), "exec"), module.__dict__)
    held.verify()
    need(module.WATCHER == WATCHER and module.START_GATE == GATE
         and module.COMPOSITE_FINALIZER == FINALIZER and module.WRAPPER == WRAPPER
         and module.FINAL_PYTHON == PYTHON and module.AUDIT == AUDIT
         and module.CONTROL == CONTROL
         and module.CONTROL_ENV == EXACT_ENVIRONMENT,
         "held watcher exact v5 launch constants")
    return module


def expected_exec_argv(
    module: types.ModuleType, bridge: Path, pinset: Path, anchor: Path,
    unit: str, maximum_wait_seconds: int,
) -> tuple[list[str], list[str]]:
    finalizer_unit = same_token_finalizer_unit(bridge, unit)
    mapping_bridge = bridge if bridge.parent == AUDIT else AUDIT / bridge.name
    need(module.finalizer_unit_for_worker(mapping_bridge, unit) == finalizer_unit,
         "held watcher exact same-token composite finalizer unit")
    watcher = module.expected_watcher_argv(
        bridge, pinset, anchor, unit, maximum_wait_seconds, WATCHER_SHA256,
    )
    gate = module.expected_gate_argv(
        bridge, pinset, anchor, unit, maximum_wait_seconds, GATE_SHA256,
        WATCHER_SHA256,
    )
    need(len(watcher) == 18 and len(gate) == 20,
         "exact watcher18/gate20 argv cardinality")
    need(watcher == safe_argv(watcher, "watcher18")
         and gate == safe_argv(gate, "gate20"),
         "exact shell-neutral watcher/gate argv")
    need(watcher[:4] == [os.fspath(PYTHON), "-I", "-B", "-c"]
         and gate[:4] == [os.fspath(PYTHON), "-I", "-B", "-c"],
         "exact isolated direct-Python prefixes")
    return watcher, gate


def same_token_finalizer_unit(bridge: Path, worker_unit: str) -> str:
    prefix = "c30c-postreceipt-v3-p1-bridge-v5-"
    need(bridge.name.startswith(prefix), "v5 bridge token prefix")
    token = bridge.name[len(prefix):]
    need(TOKEN.fullmatch(token) is not None
         and worker_unit == "cm2-" + prefix + token + ".service",
         "worker exact same-token unit")
    return "cm2-" + prefix + "finalizer-" + token + ".service"


def systemd_run_argv(unit: str, watcher: list[str], gate: list[str]) -> list[str]:
    pre_property = "--property=ExecStartPre=" + " ".join(gate)
    command = [
        os.fspath(SYSTEMD_RUN), "--user", "--expand-environment=no",
        "--unit=" + unit, "--service-type=exec", "--remain-after-exit",
        "--property=StandardOutput=journal", "--property=StandardError=journal",
        pre_property, "--", *watcher,
    ]
    need(len(command) == 28 and command[10:] == watcher,
         "exact systemd-run ten-token prefix plus watcher18")
    need(command[8] == pre_property
         and command[8].removeprefix("--property=ExecStartPre=").split(" ") == gate,
         "ExecStartPre exact plain single-space gate20 join")
    for index, item in enumerate(command):
        need(type(item) is str and item != "" and "\x00" not in item,
             "execve nonempty NUL-free argv")
        if index != 8:
            safe_token(item, "systemd-run")
    return command


def source_holds(expect_self_sha256: str, formal: bool) -> dict[str, HeldFile]:
    need(HEX64.fullmatch(expect_self_sha256) is not None,
         "launcher expected lowercase SHA")
    self_mode = 0o444 if formal else stat.S_IMODE(SELF.lstat().st_mode)
    need(self_mode in {0o444, 0o644, 0o664},
         "launcher selftest development/frozen mode")
    specifications = {
        "launcher": (SELF, expect_self_sha256, None, self_mode, 1000, 1000),
        "watcher_v6": (WATCHER, WATCHER_SHA256, SOURCE_SIZES[WATCHER], 0o444, 1000, 1000),
        "start_gate_v3": (GATE, GATE_SHA256, SOURCE_SIZES[GATE], 0o444, 1000, 1000),
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


def verify_holds(holds: dict[str, HeldFile]) -> None:
    need(set(holds) == {
        "launcher", "watcher_v6", "start_gate_v3", "composite_finalizer",
        "wrapper_v1", "python", "systemd_run", "systemctl",
    }, "exact v5 launcher source/tool pin roles")
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


def unit_absent(unit: str, systemctl: HeldFile) -> None:
    systemctl.verify()
    completed = subprocess.run(
        [os.fspath(SYSTEMCTL), "--user", "show", unit,
         "--property=LoadState", "--value"],
        cwd=ROOT, env=EXACT_ENVIRONMENT, stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    systemctl.verify()
    need(completed.returncode == 0 and completed.stdout == b"not-found\n"
         and completed.stderr == b"", "fresh unit is exactly not-found")


def self_test(
    launch_token: str, maximum_wait_seconds: int, expect_self_sha256: str,
) -> dict[str, Any]:
    holds = source_holds(expect_self_sha256, False)
    audit_parent: HeldDirectory | None = None
    control_parent: HeldDirectory | None = None
    bridge_held: HeldDirectory | None = None
    control_held: HeldDirectory | None = None
    try:
        module = load_frozen_watcher(holds["watcher_v6"])
        with tempfile.TemporaryDirectory(prefix="c30c-bridge-v5-launcher-") as raw:
            root = Path(raw)
            audit = root / "audit"
            control = root / "control"
            os.mkdir(audit, 0o700)
            os.mkdir(control, 0o700)
            name, unit, bridge, control_dir, pinset, anchor = namespace_paths(
                audit, control, launch_token,
            )
            watcher, gate = expected_exec_argv(
                module, bridge, pinset, anchor, unit, maximum_wait_seconds,
            )
            command = systemd_run_argv(unit, watcher, gate)
            audit_parent = HeldDirectory(audit)
            control_parent = HeldDirectory(control)
            audit_parent.absent(name)
            control_parent.absent(name)
            bridge_held = audit_parent.create_empty_0700(name)
            control_held = control_parent.create_empty_0700(name)
            need(bridge_held.path == bridge and control_held.path == control_dir
                 and os.listdir(bridge_held.fd) == []
                 and os.listdir(control_held.fd) == [],
                 "temp-only exact fresh v5 namespace construction")
            need(command[8] == "--property=ExecStartPre=" + " ".join(gate)
                 and command[10:] == watcher,
                 "temp-only exact v5 systemd property and ExecStart")
        verify_holds(holds)
        return {
            "schema": "cm2.round306c30c.postreceipt-bridge-v5-launcher-self-test.v1",
            "status": SELFTEST_STATUS,
            "watcher_argv_count": 18,
            "gate_argv_count": 20,
            "pinned_source_role_count": len(holds),
            "formal_namespace_reads": 0,
            "formal_namespace_writes": 0,
            "service_operations": 0,
            "formal_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        }
    finally:
        for held in (control_held, bridge_held, control_parent, audit_parent):
            if held is not None:
                held.close()
        for held in holds.values():
            held.close()


def execute(
    launch_token: str, maximum_wait_seconds: int, expect_self_sha256: str,
) -> None:
    holds = source_holds(expect_self_sha256, True)
    audit_parent: HeldDirectory | None = None
    control_parent: HeldDirectory | None = None
    bridge_held: HeldDirectory | None = None
    control_held: HeldDirectory | None = None
    try:
        need(AUDIT.is_dir() and CONTROL.is_dir(), "formal audit/control parents")
        name, unit, bridge, control_dir, pinset, anchor = namespace_paths(
            AUDIT, CONTROL, launch_token,
        )
        module = load_frozen_watcher(holds["watcher_v6"])
        watcher, gate = expected_exec_argv(
            module, bridge, pinset, anchor, unit, maximum_wait_seconds,
        )
        finalizer_unit = same_token_finalizer_unit(bridge, unit)
        command = systemd_run_argv(unit, watcher, gate)

        unit_absent(unit, holds["systemctl"])
        unit_absent(finalizer_unit, holds["systemctl"])
        audit_parent = HeldDirectory(AUDIT)
        control_parent = HeldDirectory(CONTROL)
        audit_parent.absent(name)
        control_parent.absent(name)
        bridge_held = audit_parent.create_empty_0700(name)
        control_held = control_parent.create_empty_0700(name)

        verify_holds(holds)
        audit_parent.verify()
        control_parent.verify()
        bridge_held.verify()
        control_held.verify()
        need(os.listdir(bridge_held.fd) == [] and os.listdir(control_held.fd) == [],
             "final empty v5 bridge/control namespaces before systemd-run")
        unit_absent(unit, holds["systemctl"])
        unit_absent(finalizer_unit, holds["systemctl"])
        verify_holds(holds)
        os.execve(os.fspath(SYSTEMD_RUN), command, EXACT_ENVIRONMENT)
        raise Rejected("systemd-run execve unexpectedly returned")
    finally:
        for held in (control_held, bridge_held, control_parent, audit_parent):
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
        execute(
            token, arguments.maximum_wait_seconds,
            arguments.expect_self_sha256,
        )
        raise Rejected("launcher execute unexpectedly returned")
    except (Rejected, OSError, ValueError, TypeError, KeyError,
            subprocess.SubprocessError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
