#!/usr/bin/env python3
"""Persistent zero-credit C30c v3 post-receipt mathematical bridge.

The watcher waits for the exact v3 transaction to finish, replays its pinned
receipt validator, and only then runs fresh independent checker receipts under
two controlled hash seeds followed by a retained full-trace cold replay.  It
writes only to its own versioned audit directory.

The existing evidence-bundle/manifests/outer/terminal programs are inventoried
but deliberately not invoked: their published contracts pin the older
20260807 receipt transaction and validator.  Therefore a successful watcher
run remains zero credit, leaves Source-W at 80, and ends at a documented
publication-toolchain boundary.
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
import time
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

WORKSPACE = Path("/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572")
DELIVERABLES = WORKSPACE / "deliverables"
AUDIT = WORKSPACE / ".cm2-runtime/audit"
CONTROL = WORKSPACE / ".cm2-runtime/control"
RECEIPTS = WORKSPACE / ".cm2-runtime/receipts"
PYTHON = WORKSPACE / ".cm2-runtime/python-flint-0.9.0/bin/python"
SYSTEM_PYTHON = Path("/usr/bin/python3")
PYTHON_REAL = Path("/usr/bin/python3.12")

TRANSACTION_NAME = "c30c-v5-toctou-robustness-rerun-20260808T0635Z-receipt-v3"
TRANSACTION_UNIT = "cm2-c30c-v3-20260808T0635Z.service"
RUN = AUDIT / TRANSACTION_NAME
TRANSACTION_CONTROL = CONTROL / TRANSACTION_NAME
TRANSACTION_RECEIPT = RECEIPTS / TRANSACTION_NAME
BRIDGE_NAME = "c30c-postreceipt-v3-p1-bridge-v1-20260808T0655Z"
DEFAULT_BRIDGE = AUDIT / BRIDGE_NAME

PREFIX = "cm2_round306c30c_source_w_full_delta_whole_origin_disposition"
VALIDATOR = DELIVERABLES / "cm2_round306c30c_62_attack_run_receipt_validator_v3.py"
HARNESS = DELIVERABLES / (PREFIX + "_attack_harness.py")
VERIFIER = DELIVERABLES / (PREFIX + "_independent_verifier.py")
ANALYZER = DELIVERABLES / (PREFIX + "_cold_trace_analyzer.py")
PAIRING_GATE = DELIVERABLES / "cm2_round306c30c_cold_trace_unfinished_pairing_attack_gate.py"
CANDIDATES = {
    "30630071": WORKSPACE / ".cm2-runtime/candidates/c30c-v4-seed-30630071",
    "30630929": WORKSPACE / ".cm2-runtime/candidates/c30c-v4-seed-30630929",
}

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
EXPECTED_PINSET_SHA256 = (
    "ef311977aa629637042970fa4ebb8b3bfbe55849af2f89a0d964e782579e32b0"
)
EXPECTED_ACTIVE_PINSET_SHA256 = (
    "f9ed697cf779d7649ac75b571b83ddb6b605ab14ee3aa28095f751e7836bc2a4"
)

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

LEGACY_PUBLICATION_TOOLS = {
    "bundle_builder": DELIVERABLES / (PREFIX + "_audit_evidence_bundle_builder.py"),
    "manifest_builder": DELIVERABLES / (PREFIX + "_publication_manifest_builder.py"),
    "outer_checker": DELIVERABLES / (PREFIX + "_formal_handoff_outer_verifier.py"),
    "terminal_replay": DELIVERABLES / (PREFIX + "_manifest_first_sealed_verifier.py"),
    "receipt_consistency_gate": (
        DELIVERABLES / "cm2_round306c30c_receipt_authority_static_consistency_gate.py"
    ),
}
LEGACY_RUN_NAME = "c30c-v5-toctou-robustness-rerun-20260807T1012-final"
LEGACY_VALIDATOR = "cm2_round306c30c_62_attack_run_receipt_validator.py"
LEGACY_VALIDATOR_SHA256 = (
    "8692c8a8e57d535ba8f8162bd4f7f51e8acb04f28755384158b45b4eb2629b61"
)


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


def strict_object(raw: bytes, label: str) -> dict[str, Any]:
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
    need(type(value) is dict, "JSON object:" + label)
    need(raw in {canonical(value), canonical(value) + b"\n"},
         "canonical JSON bytes:" + label)
    return value


def identity(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
        value.st_size, value.st_mtime_ns, value.st_ctime_ns,
    )


def stable_hash(path: Path, maximum: int = 512 << 20) -> tuple[str, int]:
    absolute = Path(os.path.abspath(os.fspath(path)))
    need(absolute.resolve(strict=True) == absolute, "canonical path:" + os.fspath(path))
    descriptor = os.open(
        absolute, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        before = os.fstat(descriptor)
        need(
            stat.S_ISREG(before.st_mode) and before.st_nlink == 1
            and 0 <= before.st_size <= maximum,
            "bounded regular singleton:" + os.fspath(path),
        )
        digest = hashlib.sha256()
        total = 0
        while block := os.read(descriptor, 4 << 20):
            digest.update(block)
            total += len(block)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    need(identity(before) == identity(after) and total == before.st_size,
         "stable hash capture:" + os.fspath(path))
    return digest.hexdigest(), total


def stable_bytes(path: Path, maximum: int = 64 << 20) -> bytes:
    descriptor = os.open(
        path, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        before = os.fstat(descriptor)
        need(
            stat.S_ISREG(before.st_mode) and before.st_nlink == 1
            and 0 <= before.st_size <= maximum,
            "bounded byte capture:" + os.fspath(path),
        )
        chunks: list[bytes] = []
        remaining = before.st_size
        while remaining:
            block = os.read(descriptor, min(1 << 20, remaining))
            need(bool(block), "complete read:" + os.fspath(path))
            chunks.append(block)
            remaining -= len(block)
        need(os.read(descriptor, 1) == b"", "stable EOF:" + os.fspath(path))
        after = os.fstat(descriptor)
        raw = b"".join(chunks)
    finally:
        os.close(descriptor)
    need(identity(before) == identity(after) and len(raw) == before.st_size,
         "stable byte capture:" + os.fspath(path))
    return raw


def exclusive_write(path: Path, raw: bytes) -> None:
    descriptor = os.open(
        path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC, 0o400,
    )
    try:
        written = 0
        while written < len(raw):
            count = os.write(descriptor, raw[written:])
            need(count > 0, "complete exclusive write:" + path.name)
            written += count
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def write_json(path: Path, value: dict[str, Any]) -> None:
    exclusive_write(path, canonical(value) + b"\n")


def parse_pinset(path: Path) -> dict[Path, str]:
    raw = stable_bytes(path, 1 << 20)
    need(hashlib.sha256(raw).hexdigest() == EXPECTED_PINSET_SHA256,
         "bridge pinset exact hash")
    pins: dict[Path, str] = {}
    for line in raw.decode("ascii").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  (/[^\x00\r\n]+)", line)
        need(match is not None, "strict bridge pinset row")
        absolute = Path(match.group(2))
        need(absolute not in pins, "unique bridge pin path")
        pins[absolute] = match.group(1)
    need(len(pins) >= 30, "complete bridge pinset")
    return pins


def check_pins(pinset: Path) -> dict[str, str]:
    pins = parse_pinset(pinset)
    observed: dict[str, str] = {}
    for path, expected in pins.items():
        actual, _ = stable_hash(path)
        need(actual == expected, "pinned bytes:" + path.name)
        observed[os.fspath(path)] = actual
    return observed


def exact_members(directory: Path, expected: frozenset[str], label: str) -> None:
    need(directory.is_dir() and not directory.is_symlink(), "directory:" + label)
    need({entry.name for entry in os.scandir(directory)} == set(expected),
         "exact members:" + label)


def service_completed() -> bool:
    completed = subprocess.run(
        ["/usr/bin/systemctl", "--user", "show", TRANSACTION_UNIT,
         "-p", "ActiveState", "-p", "SubState", "-p", "Result",
         "-p", "ExecMainCode", "-p", "ExecMainStatus"],
        cwd=WORKSPACE, env={"HOME": os.environ.get("HOME", "/nonexistent")},
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    if completed.returncode != 0 or completed.stderr:
        return False
    fields = dict(
        line.split("=", 1) for line in completed.stdout.decode("ascii").splitlines()
        if "=" in line
    )
    return fields == {
        "ActiveState": "active", "SubState": "exited", "Result": "success",
        "ExecMainCode": "exited", "ExecMainStatus": "0",
    }


def wait_for_transaction(maximum_seconds: int) -> None:
    deadline = time.monotonic() + maximum_seconds
    while time.monotonic() < deadline:
        if (TRANSACTION_RECEIPT / "transaction-end-utc.txt").is_file():
            for _ in range(120):
                if service_completed():
                    return
                time.sleep(5)
            raise Blocked("transaction receipt exists but service did not settle cleanly")
        failed = subprocess.run(
            ["/usr/bin/systemctl", "--user", "is-failed", TRANSACTION_UNIT],
            cwd=WORKSPACE, stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False,
        )
        need(failed.returncode != 0, "v3 transaction service failed before receipt")
        time.sleep(30)
    raise Blocked("timeout waiting for v3 transaction")


def validate_transaction(pinset: Path) -> dict[str, Any]:
    pin_before = check_pins(pinset)
    active_pinset = TRANSACTION_CONTROL / "pins.sha256"
    active_pinset_raw = stable_bytes(active_pinset, 1 << 20)
    need(hashlib.sha256(active_pinset_raw).hexdigest() == EXPECTED_ACTIVE_PINSET_SHA256,
         "active transaction pinset hash")
    exact_members(RUN, RUN_FILES, "completed v3 run")
    exact_members(TRANSACTION_RECEIPT, RECEIPT_FILES, "completed v3 receipt")
    for name in ("preflight.exit", "transaction-run.exit", "receipt.exit"):
        need(stable_bytes(TRANSACTION_RECEIPT / name, 32) == b"0\n",
             "numeric zero:" + name)
    for name in ("preflight.stderr", "receipt.stderr"):
        need(stable_bytes(TRANSACTION_RECEIPT / name, 1 << 20) == b"",
             "empty receipt stderr:" + name)
    need(stable_bytes(RUN / "stderr.log", 64 << 20) == b"", "empty run stderr")
    need(stable_bytes(RUN / "exit_code.txt", 32) == b"0\n", "run numeric exit zero")
    need(stable_bytes(RUN / "pre.sha256", 1 << 20)
         == stable_bytes(RUN / "post.sha256", 1 << 20), "run pre/post sha equality")
    need(stable_bytes(RUN / "pre.stat", 1 << 20)
         == stable_bytes(RUN / "post.stat", 1 << 20), "run pre/post stat equality")
    receipt_raw = stable_bytes(TRANSACTION_RECEIPT / "receipt.json", 4 << 20)
    receipt = strict_object(receipt_raw, "v3 receipt")
    need(
        receipt.get("schema") == "cm2.round306c30c.attack-run-receipt-validation.v3"
        and receipt.get("status") == EXPECTED_RECEIPT_STATUS
        and receipt.get("run_directory") == TRANSACTION_NAME
        and receipt.get("attack_count") == 62
        and receipt.get("numeric_exit_code") == 0
        and receipt.get("signal") is None
        and receipt.get("pre_post_sha256_identical") is True
        and receipt.get("pre_post_stat_identical") is True
        and receipt.get("formal_credit") == 0
        and receipt.get("manifest_authorized") is False
        and receipt.get("source_W_formal_remainder") == 80
        and receipt.get("source_W_transition_authorized") is False
        and receipt.get("downstream_publication_authorized") is False,
        "exact zero-credit v3 receipt conclusion",
    )
    replay = subprocess.run(
        [os.fspath(SYSTEM_PYTHON), "-I", "-B", os.fspath(VALIDATOR), os.fspath(RUN)],
        cwd=WORKSPACE,
        env={"HOME": "/nonexistent", "LC_ALL": "C.UTF-8", "TZ": "UTC"},
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    need(replay.returncode == 0 and replay.stderr == b"", "v3 validator replay")
    need(replay.stdout == receipt_raw, "v3 validator replay byte identity")
    pin_after = check_pins(pinset)
    need(pin_before == pin_after, "bridge pins stable across receipt validation")
    return {
        "schema": "cm2.round306c30c.postreceipt-v3-receipt-gate.v1",
        "status": "PASS_EXACT_V3_RECEIPT_REPLAY__ZERO_FORMAL_CREDIT",
        "transaction_unit": TRANSACTION_UNIT,
        "transaction_receipt_sha256": hashlib.sha256(receipt_raw).hexdigest(),
        "transaction_validator_sha256": receipt["validator_sha256"],
        "attack_count": 62,
        "numeric_exit_code": 0,
        "signal": None,
        "pre_post_sha256_identical": True,
        "pre_post_stat_identical": True,
        "formal_credit": 0,
        "source_W_formal_remainder": 80,
        "source_W_transition_authorized": False,
    }


def target_paths(candidate: Path) -> list[Path]:
    return [PYTHON_REAL, VERIFIER, *sorted(candidate.iterdir())]


def snapshot(paths: list[Path]) -> tuple[bytes, bytes]:
    hashes: list[str] = []
    stats: list[dict[str, Any]] = []
    for path in paths:
        digest, size = stable_hash(path)
        status = path.lstat()
        hashes.append(digest + "  " + os.fspath(path))
        stats.append({
            "path": os.fspath(path), "dev": status.st_dev, "ino": status.st_ino,
            "mode": status.st_mode, "links": status.st_nlink, "size": size,
            "mtime_ns": status.st_mtime_ns, "ctime_ns": status.st_ctime_ns,
        })
    return ("\n".join(hashes) + "\n").encode("ascii"), canonical(stats) + b"\n"


def run_timed_checker(seed: str, candidate: Path, output: Path) -> dict[str, Any]:
    output.mkdir(mode=0o700)
    paths = target_paths(candidate)
    pre_hash, pre_stat = snapshot(paths)
    exclusive_write(output / "pre.sha256", pre_hash)
    exclusive_write(output / "pre.stat.json", pre_stat)
    stdout_path = output / "stdout.json"
    stderr_path = output / "stderr.log"
    time_path = output / "time.txt"
    command = [
        "/usr/bin/time", "--verbose", "--output=" + os.fspath(time_path), "--",
        os.fspath(PYTHON), "-I", "-B", os.fspath(VERIFIER), os.fspath(candidate),
    ]
    with stdout_path.open("xb") as stdout, stderr_path.open("xb") as stderr:
        completed = subprocess.run(
            command, cwd=WORKSPACE,
            env={
                "HOME": "/nonexistent", "LC_ALL": "C.UTF-8", "TZ": "UTC",
                "PATH": "/usr/bin:/bin", "PYTHONHASHSEED": seed,
                "PYTHONDONTWRITEBYTECODE": "1",
            },
            stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr, check=False,
        )
    exclusive_write(output / "exit.txt", (str(completed.returncode) + "\n").encode("ascii"))
    post_hash, post_stat = snapshot(paths)
    exclusive_write(output / "post.sha256", post_hash)
    exclusive_write(output / "post.stat.json", post_stat)
    need(completed.returncode == 0, "dual checker exit:" + seed)
    need(stable_bytes(stderr_path, 64 << 20) == b"", "dual checker stderr:" + seed)
    need(pre_hash == post_hash and pre_stat == post_stat,
         "dual checker pre/post identity:" + seed)
    raw = stable_bytes(stdout_path, 64 << 20)
    value = strict_object(raw, "dual checker stdout:" + seed)
    need(
        value.get("status") == EXPECTED_VERIFIER_STATUS
        and value.get("formal_credit") == 0
        and value.get("manifest_authorized") is False
        and value.get("proposed_source_W_remaining_transition") == "80->78",
        "dual checker zero-credit result:" + seed,
    )
    return value


def run_dual_checker(bridge: Path, pinset: Path) -> dict[str, Any]:
    before = check_pins(pinset)
    outputs: dict[str, dict[str, Any]] = {}
    stdout_hashes: dict[str, str] = {}
    for seed, candidate in CANDIDATES.items():
        result = run_timed_checker(seed, candidate, bridge / ("dual-seed-" + seed))
        outputs[seed] = result
        stdout_hashes[seed] = stable_hash(
            bridge / ("dual-seed-" + seed) / "stdout.json", 64 << 20
        )[0]
    need(canonical(outputs["30630071"]) == canonical(outputs["30630929"]),
         "dual checker output identity")
    after = check_pins(pinset)
    need(before == after, "bridge pins stable across dual checker")
    return {
        "schema": "cm2.round306c30c.postreceipt-v3-dual-checker.v1",
        "status": "PASS_FRESH_DUAL_CONTROLLED_SEED_CHECKER__ZERO_FORMAL_CREDIT",
        "seeds": list(CANDIDATES),
        "stdout_sha256": stdout_hashes,
        "candidate_result_sha256": outputs["30630071"]["candidate_result_sha256"],
        "formal_credit": 0,
        "source_W_formal_remainder": 80,
        "source_W_transition_authorized": False,
    }


def run_cold_replay(bridge: Path, pinset: Path) -> dict[str, Any]:
    before = check_pins(pinset)
    cold = bridge / "cold-seed-30630071"
    cold.mkdir(mode=0o700)
    candidate = CANDIDATES["30630071"]
    paths = target_paths(candidate) + [ANALYZER, PAIRING_GATE]
    pre_hash, pre_stat = snapshot(paths)
    exclusive_write(cold / "pre.sha256", pre_hash)
    exclusive_write(cold / "pre.stat.json", pre_stat)
    trace = cold / "trace.raw"
    stdout_path = cold / "stdout.json"
    stderr_path = cold / "stderr.log"
    time_path = cold / "time.txt"
    command = [
        "/usr/bin/time", "--verbose", "--output=" + os.fspath(time_path), "--",
        "/usr/bin/strace", "-f", "-yy", "-s", "4096", "-e", "trace=all",
        "-o", os.fspath(trace), "/usr/bin/env", "-i", "HOME=/nonexistent",
        "LC_ALL=C.UTF-8", "TZ=UTC", "PATH=/usr/bin:/bin",
        "PYTHONHASHSEED=30630071", "PYTHONDONTWRITEBYTECODE=1",
        os.fspath(PYTHON), "-I", "-B", os.fspath(VERIFIER), os.fspath(candidate),
    ]
    with stdout_path.open("xb") as stdout, stderr_path.open("xb") as stderr:
        completed = subprocess.run(
            command, cwd=WORKSPACE, stdin=subprocess.DEVNULL,
            stdout=stdout, stderr=stderr, check=False,
        )
    exclusive_write(cold / "exit.txt", (str(completed.returncode) + "\n").encode("ascii"))
    post_hash, post_stat = snapshot(paths)
    exclusive_write(cold / "post.sha256", post_hash)
    exclusive_write(cold / "post.stat.json", post_stat)
    need(completed.returncode == 0, "cold checker exit")
    need(stable_bytes(stderr_path, 64 << 20) == b"", "cold checker stderr")
    need(pre_hash == post_hash and pre_stat == post_stat, "cold checker pre/post identity")
    cold_output = strict_object(stable_bytes(stdout_path, 64 << 20), "cold stdout")
    need(cold_output.get("status") == EXPECTED_VERIFIER_STATUS,
         "cold checker mathematical result")

    analyzer_stdout = cold / "trace_audit.json"
    analyzer_stderr = cold / "trace_audit.stderr"
    with analyzer_stdout.open("xb") as stdout, analyzer_stderr.open("xb") as stderr:
        analyzed = subprocess.run(
            [os.fspath(PYTHON), "-I", "-B", os.fspath(ANALYZER),
             "--trace", os.fspath(trace), "--stdout", os.fspath(stdout_path),
             "--stderr", os.fspath(stderr_path), "--time", os.fspath(time_path),
             "--candidate-dir", os.fspath(candidate)],
            cwd=WORKSPACE,
            env={"HOME": "/nonexistent", "LC_ALL": "C.UTF-8", "TZ": "UTC"},
            stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr, check=False,
        )
    need(analyzed.returncode == 0 and stable_bytes(analyzer_stderr, 1 << 20) == b"",
         "cold trace analyzer execution")
    trace_audit = strict_object(stable_bytes(analyzer_stdout, 4 << 20), "trace audit")
    need(trace_audit.get("status") == EXPECTED_ANALYZER_STATUS,
         "cold trace analyzer result")

    gate_stdout = cold / "pairing_gate.json"
    gate_stderr = cold / "pairing_gate.stderr"
    with gate_stdout.open("xb") as stdout, gate_stderr.open("xb") as stderr:
        gated = subprocess.run(
            [os.fspath(PYTHON), "-I", "-B", os.fspath(PAIRING_GATE)],
            cwd=WORKSPACE,
            env={"HOME": "/nonexistent", "LC_ALL": "C.UTF-8", "TZ": "UTC"},
            stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr, check=False,
        )
    need(gated.returncode == 0 and stable_bytes(gate_stderr, 1 << 20) == b"",
         "cold pairing gate execution")
    pairing = strict_object(stable_bytes(gate_stdout, 4 << 20), "pairing gate")
    need(pairing.get("status") == EXPECTED_PAIRING_STATUS,
         "cold pairing gate result")
    after = check_pins(pinset)
    need(before == after, "bridge pins stable across cold replay")
    return {
        "schema": "cm2.round306c30c.postreceipt-v3-cold-replay.v1",
        "status": "PASS_FRESH_FULL_TRACE_COLD_REPLAY__ZERO_FORMAL_CREDIT",
        "trace_sha256": stable_hash(trace)[0],
        "checker_stdout_sha256": stable_hash(stdout_path, 64 << 20)[0],
        "trace_audit_sha256": stable_hash(analyzer_stdout, 4 << 20)[0],
        "pairing_gate_sha256": stable_hash(gate_stdout, 4 << 20)[0],
        "formal_credit": 0,
        "source_W_formal_remainder": 80,
        "source_W_transition_authorized": False,
    }


def downstream_inventory() -> dict[str, Any]:
    hashes: dict[str, str] = {}
    incompatible: list[str] = []
    for label, path in LEGACY_PUBLICATION_TOOLS.items():
        raw = stable_bytes(path, 8 << 20)
        hashes[label] = hashlib.sha256(raw).hexdigest()
        if (
            LEGACY_RUN_NAME.encode("ascii") in raw
            or LEGACY_VALIDATOR.encode("ascii") in raw
            or LEGACY_VALIDATOR_SHA256.encode("ascii") in raw
        ):
            incompatible.append(label)
    need(set(incompatible) == set(LEGACY_PUBLICATION_TOOLS),
         "legacy publication boundary remains explicitly detected")
    return {
        "schema": "cm2.round306c30c.postreceipt-v3-downstream-inventory.v1",
        "status": "BLOCKED_FAIL_CLOSED_V3_PUBLICATION_TOOLCHAIN_REQUIRED",
        "tool_sha256": hashes,
        "incompatible_legacy_contracts": sorted(incompatible),
        "gaps": [
            "V3_RECEIPT_EVIDENCE_ADAPTER_AND_INDEPENDENT_ADAPTER_CHECKER_NOT_MINTED",
            "V3_EVIDENCE_BUNDLE_CONTRACT_NOT_MINTED",
            "V3_PAYLOAD_AND_ROOT_MANIFEST_CONTRACTS_NOT_MINTED",
            "V3_OUTER_CHECKER_NOT_MINTED",
            "V3_TERMINAL_SEAL_AND_TERMINAL_REPLAY_NOT_MINTED",
        ],
        "legacy_run_name": LEGACY_RUN_NAME,
        "required_run_name": TRANSACTION_NAME,
        "legacy_validator_sha256": LEGACY_VALIDATOR_SHA256,
        "required_validator_sha256": stable_hash(VALIDATOR, 4 << 20)[0],
        "formal_credit": 0,
        "source_W_formal_remainder": 80,
        "source_W_transition_authorized": False,
    }


def self_test(pinset: Path) -> dict[str, Any]:
    pins = check_pins(pinset)
    inventory = downstream_inventory()
    need(DEFAULT_BRIDGE.parent == AUDIT and not DEFAULT_BRIDGE.is_symlink(),
         "fixed bridge audit path")
    return {
        "schema": "cm2.round306c30c.postreceipt-v3-p1-bridge-preflight.v1",
        "status": "PASS_ZERO_CREDIT_WATCHER_PREFLIGHT",
        "transaction_name": TRANSACTION_NAME,
        "transaction_unit": TRANSACTION_UNIT,
        "pinned_member_count": len(pins),
        "publication_boundary_status": inventory["status"],
        "formal_credit": 0,
        "source_W_formal_remainder": 80,
        "source_W_transition_authorized": False,
    }


def run(bridge: Path, pinset: Path, maximum_wait_seconds: int) -> dict[str, Any]:
    need(bridge == DEFAULT_BRIDGE, "fixed versioned bridge directory")
    need(bridge.is_dir() and not bridge.is_symlink(), "real bridge directory")
    write_json(bridge / "preflight.json", self_test(pinset))
    wait_for_transaction(maximum_wait_seconds)
    receipt_gate = validate_transaction(pinset)
    write_json(bridge / "receipt_gate.json", receipt_gate)
    dual = run_dual_checker(bridge, pinset)
    write_json(bridge / "dual_checker_receipt.json", dual)
    cold = run_cold_replay(bridge, pinset)
    write_json(bridge / "cold_replay_receipt.json", cold)
    inventory = downstream_inventory()
    write_json(bridge / "downstream_inventory.json", inventory)
    return {
        "schema": "cm2.round306c30c.postreceipt-v3-p1-bridge-watch.v1",
        "status": "PASS_ZERO_CREDIT_THROUGH_DUAL_AND_COLD__BLOCKED_BEFORE_PUBLICATION",
        "receipt_gate_sha256": stable_hash(bridge / "receipt_gate.json", 4 << 20)[0],
        "dual_checker_receipt_sha256": stable_hash(
            bridge / "dual_checker_receipt.json", 4 << 20
        )[0],
        "cold_replay_receipt_sha256": stable_hash(
            bridge / "cold_replay_receipt.json", 4 << 20
        )[0],
        "downstream_inventory_sha256": stable_hash(
            bridge / "downstream_inventory.json", 4 << 20
        )[0],
        "publication_boundary_status": inventory["status"],
        "terminal_replay_completed": False,
        "formal_credit": 0,
        "source_W_formal_remainder": 80,
        "source_W_transition_authorized": False,
        "CM2": "NO-GO_FOR_CLAIM",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pinset", required=True, type=Path)
    parser.add_argument("--bridge-dir", type=Path, default=DEFAULT_BRIDGE)
    parser.add_argument("--maximum-wait-seconds", type=int, default=7 * 24 * 3600)
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args()
    try:
        result = (
            self_test(arguments.pinset)
            if arguments.self_test
            else run(arguments.bridge_dir, arguments.pinset,
                     arguments.maximum_wait_seconds)
        )
        if not arguments.self_test:
            write_json(arguments.bridge_dir / "terminal_status.json", result)
        print(canonical(result).decode("ascii"))
        return 0
    except (Blocked, OSError, ValueError, KeyError, TypeError) as error:
        failure = {
            "schema": "cm2.round306c30c.postreceipt-v3-p1-bridge-watch.v1",
            "status": "BLOCKED_FAIL_CLOSED",
            "error": str(error),
            "formal_credit": 0,
            "source_W_formal_remainder": 80,
            "source_W_transition_authorized": False,
            "CM2": "NO-GO_FOR_CLAIM",
        }
        if not arguments.self_test and arguments.bridge_dir.is_dir():
            try:
                write_json(arguments.bridge_dir / "failure_receipt.json", failure)
            except (Blocked, OSError):
                pass
        print(canonical(failure).decode("ascii"), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
