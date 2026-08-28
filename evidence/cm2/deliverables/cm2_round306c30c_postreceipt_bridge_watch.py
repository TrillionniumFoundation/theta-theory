#!/usr/bin/env python3
"""Persistent fail-close watcher for the C30c receipt evidence bridge.

It waits for the already-running exact receipt validator.  Only a successful
62/62 receipt is allowed to trigger the immutable adapter and its independent
verifier.  It never writes inside the attack run or either candidate tree and
does not build, publish, seal, or authorize C30c.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import time
from typing import Any


WORKSPACE = Path(__file__).resolve().parent.parent
AUDIT = WORKSPACE / ".cm2-runtime" / "audit"
DELIVERABLES = WORKSPACE / "deliverables"
RUN_NAME = "c30c-v5-toctou-robustness-rerun-20260807T1012-final"
RUN = AUDIT / RUN_NAME
RECEIPT = AUDIT / (RUN_NAME + "-receipt-validation.json")
ADAPTER = AUDIT / (RUN_NAME + "-receipt-evidence-adapter.json")
VERIFICATION = AUDIT / (RUN_NAME + "-receipt-evidence-adapter-verification.json")
BRIDGE_RECEIPT = AUDIT / (RUN_NAME + "-receipt-evidence-bridge-watch.json")
FAILURE_RECEIPT = AUDIT / (RUN_NAME + "-receipt-evidence-bridge-watch-failure.json")
PYTHON = WORKSPACE / ".cm2-runtime/python-flint-0.9.0/bin/python"
PYTHON3 = PYTHON.parent / "python3"
SYSTEM_PYTHON = Path("/usr/bin/python3")
PYTHON_REAL = Path("/usr/bin/python3.12")
PYTHON_SHA256 = "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118"
VALIDATOR_SCRIPT = DELIVERABLES / "cm2_round306c30c_62_attack_run_receipt_validator.py"
ADAPTER_SCRIPT = DELIVERABLES / "cm2_round306c30c_attack_receipt_evidence_adapter.py"
VERIFIER_SCRIPT = DELIVERABLES / "cm2_round306c30c_attack_receipt_evidence_adapter_independent_verifier.py"

EXPECTED = {
    VALIDATOR_SCRIPT: "8692c8a8e57d535ba8f8162bd4f7f51e8acb04f28755384158b45b4eb2629b61",
    ADAPTER_SCRIPT: "f4dac9c42f3de9d02e97060f14bb42ccdfca98015ed4a760bbca044b50c56590",
    VERIFIER_SCRIPT: "43611f53caa199dce8c529151731db025e197d42232736200fd7b73cd67ba153",
}


class Blocked(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Blocked(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def identity(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
        value.st_size, value.st_mtime_ns, value.st_ctime_ns,
    )


def python_chain() -> tuple[tuple[int, ...], ...]:
    entry = os.lstat(PYTHON)
    venv_target = os.lstat(PYTHON3)
    system_entry = os.lstat(SYSTEM_PYTHON)
    resolved_target = os.lstat(PYTHON_REAL)
    need(
        stat.S_ISLNK(entry.st_mode) and entry.st_nlink == 1
        and os.readlink(PYTHON) == "python3"
        and stat.S_ISLNK(venv_target.st_mode) and venv_target.st_nlink == 1
        and os.readlink(PYTHON3) == "/usr/bin/python3"
        and stat.S_ISLNK(system_entry.st_mode) and system_entry.st_nlink == 1
        and os.readlink(SYSTEM_PYTHON) == "python3.12"
        and stat.S_ISREG(resolved_target.st_mode) and resolved_target.st_nlink == 1
        and PYTHON.resolve(strict=True) == PYTHON_REAL,
        "exact controlled Python runtime chain",
    )
    return tuple(map(identity, (entry, venv_target, system_entry, resolved_target)))


def python_hash() -> str:
    chain_before = python_chain()
    descriptor = os.open(
        PYTHON_REAL,
        os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        before = os.fstat(descriptor)
        need(identity(before) == chain_before[-1], "controlled Python target identity")
        digest = hashlib.sha256()
        while block := os.read(descriptor, 1 << 20):
            digest.update(block)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    need(
        identity(before) == identity(after) and chain_before == python_chain(),
        "stable controlled Python runtime chain",
    )
    return digest.hexdigest()


def strict_object(raw: bytes, label: str) -> dict[str, Any]:
    value = json.loads(raw)
    need(type(value) is dict and raw in {canonical(value), canonical(value) + b"\n"},
         "canonical object:" + label)
    return value


def exclusive_write(path: Path, raw: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC, 0o400)
    try:
        os.write(descriptor, raw)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def receipt_ready() -> dict[str, Any] | None:
    try:
        raw = RECEIPT.read_bytes()
    except FileNotFoundError:
        return None
    value = strict_object(raw, "validator watcher receipt")
    result = value.get("validator_result")
    need(value.get("watch_status") == "VALIDATOR_COMPLETED" and
         value.get("validator_exit_code") == 0 and value.get("validator_stderr") == "" and
         type(result) is dict, "successful watcher receipt")
    need(result.get("status") ==
         "PASS_COMPLETE_C30C_62_ATTACK_RUN_RECEIPT__ZERO_FORMAL_CREDIT" and
         result.get("attack_count") == 62 and result.get("numeric_exit_code") == 0 and
         result.get("signal") is None and result.get("pre_post_sha256_identical") is True and
         result.get("pre_post_stat_identical") is True and result.get("formal_credit") == 0 and
         result.get("manifest_authorized") is False,
         "complete zero-credit receipt")
    return value


def run() -> dict[str, Any]:
    need(python_hash() == PYTHON_SHA256, "pinned controlled Python runtime")
    for path, expected in EXPECTED.items():
        need(path.is_file() and not path.is_symlink() and file_hash(path) == expected,
             "pinned executable:" + path.name)
    while receipt_ready() is None:
        time.sleep(30)
    watcher = receipt_ready()
    need(watcher is not None, "receipt remained present")

    if not ADAPTER.exists():
        completed = subprocess.run(
            [os.fspath(PYTHON), "-I", "-B", os.fspath(ADAPTER_SCRIPT),
             "--run-dir", os.fspath(RUN), "--validator-receipt", os.fspath(RECEIPT),
             "--output-adapter", os.fspath(ADAPTER)],
            cwd=WORKSPACE, env={"HOME": "/nonexistent", "LC_ALL": "C.UTF-8", "TZ": "UTC"},
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        need(completed.returncode == 0 and completed.stderr == b"", "adapter execution")
        summary = strict_object(completed.stdout, "adapter summary")
        need(summary.get("status") ==
             "PASS_RECEIPT_BOUND_TO_EXACT_ATTACK_EVIDENCE__ZERO_FORMAL_CREDIT",
             "adapter summary status")
    adapter_raw = ADAPTER.read_bytes()
    adapter = strict_object(adapter_raw, "adapter")
    need(adapter.get("status") ==
         "PASS_RECEIPT_BOUND_TO_EXACT_ATTACK_EVIDENCE__ZERO_FORMAL_CREDIT" and
         adapter.get("formal_credit") == 0 and
         adapter.get("source_W_transition_authorized") is False,
         "adapter zero-credit status")

    completed = subprocess.run(
        [os.fspath(PYTHON), "-I", "-B", os.fspath(VERIFIER_SCRIPT),
         "--adapter", os.fspath(ADAPTER)],
        cwd=WORKSPACE, env={"HOME": "/nonexistent", "LC_ALL": "C.UTF-8", "TZ": "UTC"},
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    need(completed.returncode == 0 and completed.stderr == b"", "adapter verifier execution")
    verification = strict_object(completed.stdout, "adapter verification")
    need(verification.get("status") ==
         "PASS_INDEPENDENT_RECEIPT_EVIDENCE_BINDING__ZERO_FORMAL_CREDIT" and
         verification.get("formal_credit") == 0 and
         verification.get("source_W_transition_authorized") is False,
         "adapter verification status")
    if not VERIFICATION.exists():
        exclusive_write(VERIFICATION, canonical(verification) + b"\n")
    else:
        need(VERIFICATION.read_bytes() == canonical(verification) + b"\n",
             "existing verification exact identity")
    return {
        "schema": "cm2.round306c30c.postreceipt-bridge-watch.v1",
        "status": "PASS_RECEIPT_BRIDGE_READY__AWAITING_DUAL_COLD_BUNDLE_AND_SEAL",
        "validator_receipt_sha256": file_hash(RECEIPT),
        "adapter_sha256": file_hash(ADAPTER),
        "adapter_verification_sha256": file_hash(VERIFICATION),
        "formal_credit": 0,
        "source_W_transition_authorized": False,
        "CM2": "NO-GO_FOR_CLAIM",
    }


def main() -> int:
    try:
        result = run()
        if not BRIDGE_RECEIPT.exists():
            exclusive_write(BRIDGE_RECEIPT, canonical(result) + b"\n")
        return 0
    except (Blocked, OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        failure = {
            "schema": "cm2.round306c30c.postreceipt-bridge-watch.v1",
            "status": "BLOCKED_FAIL_CLOSED",
            "error": str(error),
            "formal_credit": 0,
            "source_W_transition_authorized": False,
            "CM2": "NO-GO_FOR_CLAIM",
        }
        if not FAILURE_RECEIPT.exists():
            exclusive_write(FAILURE_RECEIPT, canonical(failure) + b"\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
