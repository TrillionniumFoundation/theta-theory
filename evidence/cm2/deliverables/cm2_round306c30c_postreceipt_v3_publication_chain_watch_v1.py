#!/usr/bin/env python3
"""Fail-closed watcher for the versioned C30c v3 publication chain.

Until the exact v3 bridge terminal zero-credit boundary exists and its
systemd service is cleanly settled, this process only polls: it does not
create the publication directory or invoke any publication stage.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
import time
from pathlib import Path
from typing import Any

WORKSPACE = Path("/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572")
DELIVERABLES = WORKSPACE / "deliverables"
AUDIT = WORKSPACE / ".cm2-runtime/audit"
BRIDGE_NAME = "c30c-postreceipt-v3-p1-bridge-v1-20260808T0655Z"
BRIDGE = AUDIT / BRIDGE_NAME
BRIDGE_UNIT = "cm2-c30c-postreceipt-v3-p1-bridge-v1-20260808T0655Z.service"
CHAIN_NAME = "c30c-publication-v3-chain-v1-20260808T0715Z"
CHAIN = AUDIT / CHAIN_NAME
PREFIX = "cm2_round306c30c_source_w_full_delta_whole_origin_disposition"
PROGRAMS = {
    "bundle": DELIVERABLES / (PREFIX + "_audit_evidence_bundle_builder_v3.py"),
    "manifests": DELIVERABLES / (PREFIX + "_publication_manifest_builder_v3.py"),
    "outer": DELIVERABLES / (PREFIX + "_formal_handoff_outer_verifier_v3.py"),
    "terminal": DELIVERABLES / (PREFIX + "_terminal_seal_replay_v3.py"),
}
STATIC_GATE = DELIVERABLES / "cm2_round306c30c_publication_static_consistency_gate_v3.py"
C30B_MANIFEST_SHA256 = "6af636a4239f390712d057030f03e09fbbca332c6170f183d3d0095f19f0f248"


class Blocked(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Blocked(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True,
                      separators=(",", ":")).encode("ascii")


def identity(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns)


def capture(path: Path, maximum: int = 64 << 30) -> bytes:
    absolute = Path(os.path.abspath(os.fspath(path)))
    need(absolute.resolve(strict=True) == absolute, "canonical path:" + os.fspath(path))
    descriptor = os.open(absolute, os.O_RDONLY | os.O_CLOEXEC |
                         getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and
             0 <= before.st_size <= maximum, "bounded singleton:" + os.fspath(path))
        chunks: list[bytes] = []
        remaining = before.st_size
        while remaining:
            block = os.read(descriptor, min(4 << 20, remaining))
            need(bool(block), "complete read:" + os.fspath(path))
            chunks.append(block)
            remaining -= len(block)
        need(os.read(descriptor, 1) == b"", "stable EOF:" + os.fspath(path))
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    need(identity(before) == identity(after), "stable capture:" + os.fspath(path))
    return b"".join(chunks)


def sha(path: Path) -> str:
    state = hashlib.sha256()
    descriptor = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                         getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "hash singleton:" + os.fspath(path))
        while block := os.read(descriptor, 4 << 20):
            state.update(block)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    need(identity(before) == identity(after), "stable hash:" + os.fspath(path))
    return state.hexdigest()


def strict_object(raw: bytes, label: str) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            need(type(key) is str and key not in output, "unique key:" + label)
            output[key] = value
        return output
    try:
        value = json.loads(raw.decode("ascii"), object_pairs_hook=unique,
                           parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)))
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise Blocked("strict JSON:" + label) from error
    need(type(value) is dict and raw in {canonical(value), canonical(value) + b"\n"},
         "canonical JSON:" + label)
    return value


def check_pins(pinset: Path) -> dict[str, str]:
    raw = capture(pinset, 4 << 20)
    output: dict[str, str] = {}
    for line in raw.decode("ascii").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  (/.+)", line)
        need(match is not None, "pinset row syntax")
        path = Path(match.group(2))
        need(os.fspath(path) not in output, "unique pin path")
        actual = sha(path)
        need(actual == match.group(1), "pinned bytes:" + path.name)
        output[os.fspath(path)] = actual
    need(len(output) >= 30, "complete publication pinset")
    return output


def bridge_service_success() -> bool:
    completed = subprocess.run(
        ["/usr/bin/systemctl", "--user", "show", BRIDGE_UNIT,
         "-p", "ActiveState", "-p", "SubState", "-p", "Result",
         "-p", "ExecMainCode", "-p", "ExecMainStatus"],
        cwd=WORKSPACE, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    if completed.returncode != 0 or completed.stderr:
        return False
    fields = dict(line.split("=", 1) for line in completed.stdout.decode("ascii").splitlines()
                  if "=" in line)
    return fields == {"ActiveState": "active", "SubState": "exited",
                      "Result": "success", "ExecMainCode": "exited",
                      "ExecMainStatus": "0"}


def exact_bridge_boundary() -> bool:
    terminal = BRIDGE / "terminal_status.json"
    if not terminal.is_file():
        return False
    try:
        value = strict_object(capture(terminal, 4 << 20), "bridge terminal")
    except (Blocked, OSError, ValueError, TypeError):
        return False
    return (
        value.get("schema") == "cm2.round306c30c.postreceipt-v3-p1-bridge-watch.v1"
        and value.get("status") ==
        "PASS_ZERO_CREDIT_THROUGH_DUAL_AND_COLD__BLOCKED_BEFORE_PUBLICATION"
        and value.get("terminal_replay_completed") is False
        and value.get("formal_credit") == 0
        and value.get("source_W_formal_remainder") == 80
        and value.get("source_W_transition_authorized") is False
        and value.get("CM2") == "NO-GO_FOR_CLAIM"
    )


def wait_boundary(maximum_seconds: int) -> None:
    deadline = time.monotonic() + maximum_seconds
    while time.monotonic() < deadline:
        if exact_bridge_boundary():
            for _ in range(120):
                if bridge_service_success():
                    return
                time.sleep(5)
            raise Blocked("bridge terminal exists but service did not settle cleanly")
        failed = subprocess.run(["/usr/bin/systemctl", "--user", "is-failed", BRIDGE_UNIT],
                                cwd=WORKSPACE, stdin=subprocess.DEVNULL,
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                check=False)
        need(failed.returncode != 0, "bridge service failed before terminal boundary")
        time.sleep(30)
    raise Blocked("timeout waiting for exact bridge terminal boundary")


def execute(program: Path, chain_dir: Path) -> bytes:
    completed = subprocess.run(
        ["/usr/bin/python3", "-I", "-B", os.fspath(program),
         "--chain-dir", os.fspath(chain_dir)], cwd=WORKSPACE,
        env={"HOME": "/nonexistent", "LC_ALL": "C.UTF-8", "TZ": "UTC",
             "PATH": "/usr/bin:/bin", "PYTHONDONTWRITEBYTECODE": "1"},
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        check=False,
    )
    need(completed.returncode == 0 and completed.stderr == b"",
         "clean stage execution:" + program.name)
    strict_object(completed.stdout, "stage stdout:" + program.name)
    return completed.stdout


def exclusive(path: Path, raw: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC, 0o400)
    try:
        view = memoryview(raw)
        while view:
            count = os.write(descriptor, view)
            need(count > 0, "complete write:" + path.name)
            view = view[count:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def self_test(pinset: Path) -> dict[str, Any]:
    pins = check_pins(pinset)
    gate = subprocess.run(["/usr/bin/python3", "-I", "-B", os.fspath(STATIC_GATE)],
                          cwd=WORKSPACE,
                          env={"HOME": "/nonexistent", "LC_ALL": "C.UTF-8", "TZ": "UTC"},
                          stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, check=False)
    need(gate.returncode == 0 and gate.stderr == b"", "publication static gate")
    gate_value = strict_object(gate.stdout, "publication static gate")
    need(gate_value.get("status") ==
         "PASS_V3_PUBLICATION_CONTRACTS_COHERENT__ZERO_FORMAL_CREDIT",
         "publication static gate conclusion")
    need(CHAIN.parent == AUDIT and not CHAIN.exists(), "fresh fixed publication directory")
    return {"schema": "cm2.round306c30c.v3-publication-chain-preflight.v1",
            "status": "PASS_FAIL_CLOSED_WATCHER_PREFLIGHT__ZERO_FORMAL_CREDIT",
            "pinned_member_count": len(pins),
            "static_gate_sha256": hashlib.sha256(gate.stdout).hexdigest(),
            "chain_name": CHAIN_NAME,
            "bridge_name": BRIDGE_NAME,
            "formal_credit": 0, "source_W_formal_remainder": 80,
            "source_W_transition_authorized": False,
            "CM2": "NO-GO_FOR_CLAIM"}


def run(pinset: Path, maximum_seconds: int) -> dict[str, Any]:
    pins_before = check_pins(pinset)
    # Hard gate: no publication directory or publication stage exists before this returns.
    wait_boundary(maximum_seconds)
    need(not CHAIN.exists(), "fresh versioned publication directory")
    CHAIN.mkdir(mode=0o700)
    bundle_stdout = execute(PROGRAMS["bundle"], CHAIN)
    need(bundle_stdout == capture(CHAIN / "evidence_bundle_receipt.json", 16 << 20),
         "bundle stdout/receipt identity")
    check_pins(pinset)
    manifest_stdout = execute(PROGRAMS["manifests"], CHAIN)
    need(manifest_stdout == capture(CHAIN / "manifest_receipt.json", 16 << 20),
         "manifest stdout/receipt identity")
    check_pins(pinset)
    outer_stdout = execute(PROGRAMS["outer"], CHAIN)
    outer_path = CHAIN / "outer_verification.json"
    exclusive(outer_path, outer_stdout)
    outer = strict_object(outer_stdout, "outer publication")
    need(outer.get("status") ==
         "PASS_INDEPENDENT_OUTER_MATHEMATICAL_CHECK__CONDITIONAL_80_TO_78"
         and outer.get("formal_credit") == 0
         and outer.get("source_W_formal_remainder") == 80
         and outer.get("source_W_transition_authorized") is False,
         "outer remains conditional")
    check_pins(pinset)
    terminal_stdout = execute(PROGRAMS["terminal"], CHAIN)
    need(terminal_stdout == capture(CHAIN / "terminal_replay.json", 16 << 20),
         "terminal stdout/receipt identity")
    terminal = strict_object(terminal_stdout, "terminal replay")
    need(terminal.get("schema") == "cm2.round306c30c.v3-terminal-replay.v1"
         and terminal.get("status") == "PASS_TERMINAL_REPLAY__FORMAL_SOURCE_W_80_TO_78"
         and terminal.get("round306c30b_manifest_sha256") == C30B_MANIFEST_SHA256
         and terminal.get("source_W_transition") == {"before": 80, "after": 78}
         and terminal.get("formal_credit") ==
             {"resolved_source_W_origin_dispositions": 2,
              "resolved_nonexcluded": 2, "whole_source_W_origin_exclusions": 0}
         and terminal.get("source_W_formal_remainder") == 78
         and terminal.get("source_W_transition_authorized") is True
         and terminal.get("CM2") == "NO-GO_FOR_CLAIM",
         "exact terminal authorization")
    pins_after = check_pins(pinset)
    need(pins_before == pins_after, "publication pins stable across full chain")
    output = {
        "schema": "cm2.round306c30c.v3-publication-chain-watch.v1",
        "status": "PASS_C30C_V3_TERMINAL_REPLAY__FORMAL_SOURCE_W_80_TO_78",
        "chain_name": CHAIN_NAME,
        "terminal_replay_sha256": sha(CHAIN / "terminal_replay.json"),
        "root_manifest_sha256": sha(CHAIN / "root_manifest.sha256"),
        "outer_verification_sha256": sha(CHAIN / "outer_verification.json"),
        "round306c30b_manifest_sha256": C30B_MANIFEST_SHA256,
        "source_W_formal_remainder": 78,
        "source_W_transition_authorized": True,
        "D02": "BLOCKED_COMPOSITE", "D03": "UNAUTHORIZED",
        "D04": "NOT_MINTED", "Gate5": "10/18",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    exclusive(CHAIN / "chain_status.json", canonical(output) + b"\n")
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pinset", required=True, type=Path)
    parser.add_argument("--maximum-wait-seconds", type=int, default=7 * 24 * 3600)
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args()
    try:
        output = (self_test(arguments.pinset.resolve(strict=True)) if arguments.self_test
                  else run(arguments.pinset.resolve(strict=True),
                           arguments.maximum_wait_seconds))
    except (Blocked, OSError, ValueError, TypeError, KeyError,
            subprocess.SubprocessError) as error:
        output = {"schema": "cm2.round306c30c.v3-publication-chain-watch.v1",
                  "status": "BLOCKED_FAIL_CLOSED", "error": str(error),
                  "formal_credit": 0, "source_W_formal_remainder": 80,
                  "source_W_transition_authorized": False,
                  "CM2": "NO-GO_FOR_CLAIM"}
        print(canonical(output).decode("ascii"))
        return 1
    print(canonical(output).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
