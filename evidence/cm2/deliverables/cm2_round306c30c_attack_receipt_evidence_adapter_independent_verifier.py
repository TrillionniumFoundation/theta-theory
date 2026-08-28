#!/usr/bin/env python3
"""Independently verify the C30c receipt-to-evidence adapter.

The verifier does not import the adapter or the receipt validator.  It checks
their pinned bytes, replays the validator, recaptures the exact completed run
and watcher receipt, and recomputes every adapter binding.  It writes nothing
and never authorizes a Source-W transition.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import subprocess
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parent.parent
AUDIT_ROOT = WORKSPACE / ".cm2-runtime" / "audit"
RUN_NAME = "c30c-v5-toctou-robustness-rerun-20260807T1012-final"
RUN_REL = ".cm2-runtime/audit/" + RUN_NAME
RECEIPT_NAME = RUN_NAME + "-receipt-validation.json"
RECEIPT_REL = ".cm2-runtime/audit/" + RECEIPT_NAME
ADAPTER_NAME = RUN_NAME + "-receipt-evidence-adapter.json"
ADAPTER_SCRIPT = (
    WORKSPACE / "deliverables"
    / "cm2_round306c30c_attack_receipt_evidence_adapter.py"
)
ADAPTER_SCRIPT_SHA256 = (
    "f4dac9c42f3de9d02e97060f14bb42ccdfca98015ed4a760bbca044b50c56590"
)
VALIDATOR = (
    WORKSPACE / "deliverables"
    / "cm2_round306c30c_62_attack_run_receipt_validator.py"
)
VALIDATOR_REL = "deliverables/cm2_round306c30c_62_attack_run_receipt_validator.py"
VALIDATOR_SHA256 = (
    "8692c8a8e57d535ba8f8162bd4f7f51e8acb04f28755384158b45b4eb2629b61"
)
PYTHON = WORKSPACE / ".cm2-runtime/python-flint-0.9.0/bin/python"
PYTHON3 = PYTHON.parent / "python3"
SYSTEM_PYTHON = Path("/usr/bin/python3")
PYTHON_REAL = Path("/usr/bin/python3.12")
PYTHON_SHA256 = (
    "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118"
)
RUN_FILES = frozenset({
    "command.txt", "end_utc.txt", "exit_code.txt", "observed_child_pids.txt",
    "post.sha256", "post.stat", "pre.sha256", "pre.stat", "provenance.json",
    "run.sh", "start_utc.txt", "stderr.log", "stdout.json", "time.txt",
    "time_pid.txt", "wrapper_pid.txt",
})
RECEIPT_STATUS = "PASS_COMPLETE_C30C_62_ATTACK_RUN_RECEIPT__ZERO_FORMAL_CREDIT"
ADAPTER_STATUS = "PASS_RECEIPT_BOUND_TO_EXACT_ATTACK_EVIDENCE__ZERO_FORMAL_CREDIT"


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=True, allow_nan=False, sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for key, value in pairs:
        need(type(key) is str and key not in output, "unique JSON keys")
        output[key] = value
    return output


def strict_object(raw: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(
            raw.decode("ascii"), object_pairs_hook=unique_object,
            parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
            parse_float=lambda token: (_ for _ in ()).throw(ValueError(token)),
        )
    except (UnicodeDecodeError, ValueError, json.JSONDecodeError) as error:
        raise Reject("strict JSON:" + label) from error
    need(type(value) is dict, "JSON object:" + label)
    need(raw in {canonical(value), canonical(value) + b"\n"},
         "canonical JSON:" + label)
    return value


def capture(path: Path, maximum: int = 64 << 20) -> tuple[bytes, tuple[int, ...]]:
    absolute = Path(os.path.abspath(os.fspath(path)))
    need(absolute.resolve(strict=True) == absolute, "canonical path:" + os.fspath(path))
    descriptor = os.open(
        absolute, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        before = os.fstat(descriptor)
        need(
            stat.S_ISREG(before.st_mode) and before.st_nlink == 1
            and 0 <= before.st_size <= maximum,
            "bounded regular singleton:" + os.fspath(path),
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
    finally:
        os.close(descriptor)
    identity = lambda value: (
        value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
        value.st_size, value.st_mtime_ns, value.st_ctime_ns,
    )
    need(identity(before) == identity(after), "stable capture:" + os.fspath(path))
    return b"".join(chunks), identity(after)


def node_identity(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
        value.st_size, value.st_mtime_ns, value.st_ctime_ns,
    )


def runtime_chain_state() -> tuple[tuple[int, ...], ...]:
    """Independently attest each link text and the terminal regular inode."""
    link_specs = (
        (PYTHON, "python3"),
        (PYTHON3, "/usr/bin/python3"),
        (SYSTEM_PYTHON, "python3.12"),
    )
    states: list[tuple[int, ...]] = []
    for path, expected_target in link_specs:
        observed = os.lstat(path)
        need(
            stat.S_ISLNK(observed.st_mode) and observed.st_nlink == 1
            and os.readlink(path) == expected_target,
            "controlled runtime link:" + os.fspath(path),
        )
        states.append(node_identity(observed))
    terminal = os.lstat(PYTHON_REAL)
    need(
        stat.S_ISREG(terminal.st_mode) and terminal.st_nlink == 1
        and Path(os.path.realpath(PYTHON)) == PYTHON_REAL,
        "controlled runtime terminal",
    )
    states.append(node_identity(terminal))
    return tuple(states)


def capture_runtime() -> tuple[bytes, tuple[tuple[int, ...], ...]]:
    before_chain = runtime_chain_state()
    descriptor = os.open(
        PYTHON_REAL,
        os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        before = os.fstat(descriptor)
        need(
            node_identity(before) == before_chain[-1]
            and stat.S_ISREG(before.st_mode) and before.st_nlink == 1
            and 0 < before.st_size <= 64 << 20,
            "controlled runtime target capture",
        )
        digest_input: list[bytes] = []
        remaining = before.st_size
        while remaining:
            block = os.read(descriptor, min(1 << 20, remaining))
            need(bool(block), "complete controlled runtime read")
            digest_input.append(block)
            remaining -= len(block)
        need(os.read(descriptor, 1) == b"", "controlled runtime EOF")
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    need(node_identity(before) == node_identity(after),
         "controlled runtime target stable")
    need(before_chain == runtime_chain_state(), "controlled runtime chain stable")
    return b"".join(digest_input), before_chain


def unchanged_runtime(expected: tuple[tuple[int, ...], ...]) -> None:
    need(runtime_chain_state() == expected, "unchanged controlled runtime chain")


def unchanged(path: Path, expected: tuple[int, ...]) -> None:
    current = path.lstat()
    observed = (
        current.st_dev, current.st_ino, current.st_mode, current.st_nlink,
        current.st_size, current.st_mtime_ns, current.st_ctime_ns,
    )
    need(observed == expected, "unchanged capture:" + os.fspath(path))


def exact_adapter(path: Path) -> Path:
    absolute = Path(os.path.abspath(os.fspath(path)))
    need(
        absolute.parent == AUDIT_ROOT and absolute.name == ADAPTER_NAME
        and absolute.resolve(strict=True) == absolute,
        "exact adapter path",
    )
    return absolute


def exact_run() -> Path:
    run = AUDIT_ROOT / RUN_NAME
    need(
        run.resolve(strict=True) == run and run.is_dir() and not run.is_symlink()
        and {entry.name for entry in os.scandir(run)} == RUN_FILES,
        "exact completed run tree",
    )
    return run


def validate_receipt_result(value: dict[str, Any], stdout_raw: bytes) -> None:
    need(
        value.get("schema") == "cm2.round306c30c.attack-run-receipt-validation.v1"
        and value.get("status") == RECEIPT_STATUS
        and value.get("run_directory") == RUN_NAME
        and value.get("attack_count") == 62
        and value.get("pre_post_sha256_identical") is True
        and value.get("pre_post_stat_identical") is True
        and value.get("numeric_exit_code") == 0
        and value.get("signal") is None
        and value.get("formal_credit") == 0
        and value.get("manifest_authorized") is False
        and value.get("harness_stdout_sha256") == sha256(stdout_raw),
        "exact successful validator result",
    )


def verify(adapter_argument: Path) -> dict[str, Any]:
    adapter_path = exact_adapter(adapter_argument)
    run = exact_run()
    receipt = AUDIT_ROOT / RECEIPT_NAME
    need(receipt.resolve(strict=True) == receipt, "exact watcher receipt")

    adapter_script_raw, adapter_script_identity = capture(ADAPTER_SCRIPT, 4 << 20)
    validator_raw, validator_identity = capture(VALIDATOR, 4 << 20)
    python_raw, python_identity = capture_runtime()
    need(sha256(adapter_script_raw) == ADAPTER_SCRIPT_SHA256,
         "pinned adapter implementation")
    need(sha256(validator_raw) == VALIDATOR_SHA256, "pinned validator implementation")
    need(sha256(python_raw) == PYTHON_SHA256, "pinned Python runtime")

    adapter_raw, adapter_identity = capture(adapter_path, 16 << 20)
    adapter = strict_object(adapter_raw, "adapter")
    body = dict(adapter)
    payload_sha256 = body.pop("payload_sha256", None)
    need(payload_sha256 == sha256(canonical(body)), "closed adapter object")
    need(
        set(body) == {
            "formal_credit", "python_sha256", "receipt_file",
            "receipt_file_sha256", "receipt_result_sha256",
            "receipt_validator", "required_bindings", "run_directory",
            "run_files", "schema", "source_W_transition_authorized", "status",
        }
        and body["schema"] == "cm2.round306c30c.attack-receipt-evidence-adapter.v1"
        and body["status"] == ADAPTER_STATUS
        and body["run_directory"] == RUN_REL
        and body["receipt_file"] == RECEIPT_REL
        and body["python_sha256"] == PYTHON_SHA256
        and body["formal_credit"] == 0
        and body["source_W_transition_authorized"] is False,
        "exact zero-credit adapter envelope",
    )

    receipt_raw, receipt_identity = capture(receipt, 8 << 20)
    watcher = strict_object(receipt_raw, "watcher receipt")
    need(
        set(watcher) == {
            "validator_exit_code", "validator_result", "validator_stderr",
            "watch_status",
        }
        and watcher["watch_status"] == "VALIDATOR_COMPLETED"
        and watcher["validator_exit_code"] == 0
        and watcher["validator_stderr"] == ""
        and type(watcher["validator_result"]) is dict
        and body["receipt_file_sha256"] == sha256(receipt_raw),
        "adapter binds successful watcher receipt",
    )

    run_raw: dict[str, bytes] = {}
    run_identities: dict[str, tuple[int, ...]] = {}
    for name in sorted(RUN_FILES):
        run_raw[name], run_identities[name] = capture(run / name)
    expected_file_map = {
        name: {"sha256": sha256(raw), "size": len(raw)}
        for name, raw in sorted(run_raw.items())
    }
    need(body["run_files"] == expected_file_map, "all exact run bytes bound")
    need(run_raw["exit_code.txt"] == b"0\n", "numeric exit zero")
    need(run_raw["stderr.log"] == b"", "empty attack stderr")
    need(run_raw["pre.sha256"] == run_raw["post.sha256"],
         "pre/post SHA identity")
    need(run_raw["pre.stat"] == run_raw["post.stat"], "pre/post stat identity")

    bindings = body["required_bindings"]
    need(
        bindings == {
            "harness_stdout_sha256": sha256(run_raw["stdout.json"]),
            "numeric_exit_sha256": sha256(run_raw["exit_code.txt"]),
            "pre_sha256_ledger_sha256": sha256(run_raw["pre.sha256"]),
            "post_sha256_ledger_sha256": sha256(run_raw["post.sha256"]),
            "pre_stat_ledger_sha256": sha256(run_raw["pre.stat"]),
            "post_stat_ledger_sha256": sha256(run_raw["post.stat"]),
            "pre_post_sha256_identical": True,
            "pre_post_stat_identical": True,
            "numeric_exit_code": 0,
            "signal": None,
        },
        "explicit stdout/pre/post/exit adapter bindings",
    )

    completed = subprocess.run(
        [os.fspath(PYTHON), "-I", "-B", os.fspath(VALIDATOR), os.fspath(run)],
        cwd=WORKSPACE,
        env={"HOME": "/nonexistent", "LC_ALL": "C.UTF-8", "TZ": "UTC"},
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        check=False,
    )
    need(completed.returncode == 0 and completed.stderr == b"",
         "independent fresh validator replay")
    replay = strict_object(completed.stdout, "validator replay")
    need(replay == watcher["validator_result"], "receipt/fresh replay identity")
    validate_receipt_result(replay, run_raw["stdout.json"])
    need(body["receipt_result_sha256"] == sha256(canonical(replay)),
         "adapter binds receipt result object")
    need(
        body["receipt_validator"] == {
            "path": VALIDATOR_REL,
            "sha256": VALIDATOR_SHA256,
            "replay_stdout_sha256": sha256(completed.stdout),
        },
        "adapter binds validator bytes and replay",
    )

    unchanged(ADAPTER_SCRIPT, adapter_script_identity)
    unchanged(VALIDATOR, validator_identity)
    unchanged_runtime(python_identity)
    unchanged(adapter_path, adapter_identity)
    unchanged(receipt, receipt_identity)
    for name, identity in run_identities.items():
        unchanged(run / name, identity)
    exact_run()

    return {
        "schema": "cm2.round306c30c.attack-receipt-evidence-adapter-verification.v1",
        "status": "PASS_INDEPENDENT_RECEIPT_EVIDENCE_BINDING__ZERO_FORMAL_CREDIT",
        "adapter_sha256": sha256(adapter_raw),
        "receipt_file_sha256": sha256(receipt_raw),
        "receipt_validator_sha256": VALIDATOR_SHA256,
        "harness_stdout_sha256": sha256(run_raw["stdout.json"]),
        "pre_post_sha256_identical": True,
        "pre_post_stat_identical": True,
        "numeric_exit_code": 0,
        "signal": None,
        "formal_credit": 0,
        "source_W_transition_authorized": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--adapter", required=True, type=Path)
    arguments = parser.parse_args()
    try:
        output = verify(arguments.adapter)
    except (Reject, OSError, ValueError, KeyError, TypeError) as error:
        print(canonical({
            "schema": "cm2.round306c30c.attack-receipt-evidence-adapter-verification.v1",
            "status": "BLOCKED_FAIL_CLOSED",
            "error": str(error),
            "formal_credit": 0,
            "source_W_transition_authorized": False,
        }).decode("ascii"))
        return 1
    print(canonical(output).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
