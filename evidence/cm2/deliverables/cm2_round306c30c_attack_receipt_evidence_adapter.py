#!/usr/bin/env python3
"""Bind a completed C30c attack receipt to immutable downstream evidence.

This adapter grants no mathematical or formal credit.  It replays the pinned
receipt validator against the exact completed run, requires byte identity with
the watcher-published receipt, and publishes one closed JSON bridge.  The
bridge pins every run receipt byte, including stdout, numeric exit, and both
pre/post SHA/stat observations.  It never writes inside the run or candidate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import subprocess
import tempfile
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parent.parent
AUDIT_ROOT = WORKSPACE / ".cm2-runtime" / "audit"
RUN_NAME = "c30c-v5-toctou-robustness-rerun-20260807T1012-final"
RECEIPT_NAME = RUN_NAME + "-receipt-validation.json"
ADAPTER_NAME = RUN_NAME + "-receipt-evidence-adapter.json"
VALIDATOR = (
    WORKSPACE / "deliverables"
    / "cm2_round306c30c_62_attack_run_receipt_validator.py"
)
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
VALIDATOR_STATUS = (
    "PASS_COMPLETE_C30C_62_ATTACK_RUN_RECEIPT__ZERO_FORMAL_CREDIT"
)


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


def file_capture(path: Path, maximum: int = 64 << 20) -> tuple[bytes, tuple[int, ...]]:
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


def stat_identity(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
        value.st_size, value.st_mtime_ns, value.st_ctime_ns,
    )


def python_link_chain() -> tuple[tuple[int, ...], ...]:
    """Capture the exact three-link venv-to-system interpreter chain."""
    entry = os.lstat(PYTHON)
    venv_python3 = os.lstat(PYTHON3)
    system_python3 = os.lstat(SYSTEM_PYTHON)
    real = os.lstat(PYTHON_REAL)
    need(
        stat.S_ISLNK(entry.st_mode) and entry.st_nlink == 1
        and os.readlink(PYTHON) == "python3"
        and stat.S_ISLNK(venv_python3.st_mode) and venv_python3.st_nlink == 1
        and os.readlink(PYTHON3) == "/usr/bin/python3"
        and stat.S_ISLNK(system_python3.st_mode) and system_python3.st_nlink == 1
        and os.readlink(SYSTEM_PYTHON) == "python3.12"
        and stat.S_ISREG(real.st_mode) and real.st_nlink == 1
        and PYTHON.resolve(strict=True) == PYTHON_REAL,
        "exact controlled Python link chain",
    )
    return tuple(map(stat_identity, (entry, venv_python3, system_python3, real)))


def python_runtime_capture(
    maximum: int = 64 << 20,
) -> tuple[bytes, tuple[tuple[int, ...], ...]]:
    """Read only the pinned real target while proving the link chain stable."""
    chain_before = python_link_chain()
    descriptor = os.open(
        PYTHON_REAL,
        os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        before = os.fstat(descriptor)
        need(
            stat.S_ISREG(before.st_mode) and before.st_nlink == 1
            and stat_identity(before) == chain_before[-1]
            and 0 < before.st_size <= maximum,
            "controlled Python target identity",
        )
        chunks: list[bytes] = []
        remaining = before.st_size
        while remaining:
            block = os.read(descriptor, min(1 << 20, remaining))
            need(bool(block), "complete controlled Python read")
            chunks.append(block)
            remaining -= len(block)
        need(os.read(descriptor, 1) == b"", "stable controlled Python EOF")
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    need(stat_identity(before) == stat_identity(after),
         "stable controlled Python target")
    need(chain_before == python_link_chain(), "stable controlled Python link chain")
    return b"".join(chunks), chain_before


def require_python_runtime(expected: tuple[tuple[int, ...], ...]) -> None:
    need(python_link_chain() == expected, "controlled Python chain unchanged")


def require_identity(path: Path, expected: tuple[int, ...]) -> None:
    current = path.lstat()
    observed = (
        current.st_dev, current.st_ino, current.st_mode, current.st_nlink,
        current.st_size, current.st_mtime_ns, current.st_ctime_ns,
    )
    need(observed == expected, "captured file unchanged:" + os.fspath(path))


def exact_run(path: Path) -> Path:
    absolute = Path(os.path.abspath(os.fspath(path)))
    need(
        absolute.parent == AUDIT_ROOT and absolute.name == RUN_NAME
        and absolute.resolve(strict=True) == absolute and absolute.is_dir()
        and not absolute.is_symlink(),
        "exact completed run directory",
    )
    need({entry.name for entry in os.scandir(absolute)} == RUN_FILES,
         "exact completed run member set")
    return absolute


def exact_receipt(path: Path) -> Path:
    absolute = Path(os.path.abspath(os.fspath(path)))
    need(
        absolute.parent == AUDIT_ROOT and absolute.name == RECEIPT_NAME
        and absolute.resolve(strict=True) == absolute,
        "exact watcher receipt path",
    )
    return absolute


def exact_output(path: Path) -> Path:
    absolute = Path(os.path.abspath(os.fspath(path)))
    need(absolute.parent == AUDIT_ROOT and absolute.name == ADAPTER_NAME,
         "exact adapter output path")
    try:
        absolute.lstat()
    except FileNotFoundError:
        pass
    else:
        raise Reject("adapter output already exists")
    return absolute


def validate_validator_result(value: dict[str, Any], stdout_raw: bytes) -> None:
    need(
        value.get("schema") == "cm2.round306c30c.attack-run-receipt-validation.v1"
        and value.get("status") == VALIDATOR_STATUS
        and value.get("run_directory") == RUN_NAME
        and value.get("attack_count") == 62
        and value.get("pre_post_sha256_identical") is True
        and value.get("pre_post_stat_identical") is True
        and value.get("numeric_exit_code") == 0
        and value.get("signal") is None
        and value.get("formal_credit") == 0
        and value.get("manifest_authorized") is False
        and value.get("harness_stdout_sha256") == sha256(stdout_raw),
        "complete zero-credit validator result",
    )


def publish_noreplace(output: Path, raw: bytes) -> None:
    descriptor, staging_name = tempfile.mkstemp(
        prefix="." + output.name + ".staging-", dir=output.parent
    )
    staging = Path(staging_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(staging, 0o400)
        need(staging.read_bytes() == raw, "adapter staging bytes")
        os.link(staging, output)
        directory = os.open(output.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if staging.exists() and not staging.is_symlink():
            staging.unlink()


def build(run_argument: Path, receipt_argument: Path, output_argument: Path) -> dict[str, Any]:
    run = exact_run(run_argument)
    receipt = exact_receipt(receipt_argument)
    output = exact_output(output_argument)
    validator_raw, validator_identity = file_capture(VALIDATOR, 4 << 20)
    python_raw, python_identity = python_runtime_capture()
    need(sha256(validator_raw) == VALIDATOR_SHA256, "pinned receipt validator")
    need(sha256(python_raw) == PYTHON_SHA256, "pinned Python runtime")

    run_raw: dict[str, bytes] = {}
    run_identities: dict[str, tuple[int, ...]] = {}
    for name in sorted(RUN_FILES):
        run_raw[name], run_identities[name] = file_capture(run / name)
    receipt_raw, receipt_identity = file_capture(receipt, 8 << 20)
    watcher = strict_object(receipt_raw, "watcher receipt")
    need(
        set(watcher) == {
            "validator_exit_code", "validator_result", "validator_stderr",
            "watch_status",
        }
        and watcher["watch_status"] == "VALIDATOR_COMPLETED"
        and watcher["validator_exit_code"] == 0
        and watcher["validator_stderr"] == ""
        and type(watcher["validator_result"]) is dict,
        "successful exact watcher receipt",
    )

    completed = subprocess.run(
        [os.fspath(PYTHON), "-I", "-B", os.fspath(VALIDATOR), os.fspath(run)],
        cwd=WORKSPACE,
        env={"HOME": "/nonexistent", "LC_ALL": "C.UTF-8", "TZ": "UTC"},
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        check=False,
    )
    need(completed.returncode == 0 and completed.stderr == b"",
         "fresh receipt-validator replay")
    replay = strict_object(completed.stdout, "validator replay stdout")
    need(replay == watcher["validator_result"], "watcher/fresh validator identity")
    validate_validator_result(replay, run_raw["stdout.json"])
    need(run_raw["exit_code.txt"] == b"0\n", "numeric exit zero")
    need(run_raw["stderr.log"] == b"", "empty attack stderr")
    need(run_raw["pre.sha256"] == run_raw["post.sha256"],
         "pre/post SHA ledger identity")
    need(run_raw["pre.stat"] == run_raw["post.stat"],
         "pre/post stat ledger identity")

    require_identity(VALIDATOR, validator_identity)
    require_python_runtime(python_identity)
    require_identity(receipt, receipt_identity)
    for name, identity in run_identities.items():
        require_identity(run / name, identity)
    exact_run(run)

    run_files = {
        name: {"sha256": sha256(raw), "size": len(raw)}
        for name, raw in sorted(run_raw.items())
    }
    body = {
        "schema": "cm2.round306c30c.attack-receipt-evidence-adapter.v1",
        "status": "PASS_RECEIPT_BOUND_TO_EXACT_ATTACK_EVIDENCE__ZERO_FORMAL_CREDIT",
        "run_directory": run.relative_to(WORKSPACE).as_posix(),
        "receipt_file": receipt.relative_to(WORKSPACE).as_posix(),
        "receipt_file_sha256": sha256(receipt_raw),
        "receipt_result_sha256": sha256(canonical(replay)),
        "receipt_validator": {
            "path": VALIDATOR.relative_to(WORKSPACE).as_posix(),
            "sha256": VALIDATOR_SHA256,
            "replay_stdout_sha256": sha256(completed.stdout),
        },
        "python_sha256": PYTHON_SHA256,
        "run_files": run_files,
        "required_bindings": {
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
        "formal_credit": 0,
        "source_W_transition_authorized": False,
    }
    output_value = {**body, "payload_sha256": sha256(canonical(body))}
    publish_noreplace(output, canonical(output_value) + b"\n")
    return {
        "schema": "cm2.round306c30c.attack-receipt-evidence-adapter-build.v1",
        "status": "PASS_ADAPTER_PUBLISHED__ZERO_FORMAL_CREDIT",
        "adapter": output.relative_to(WORKSPACE).as_posix(),
        "adapter_sha256": sha256(canonical(output_value) + b"\n"),
        "formal_credit": 0,
        "source_W_transition_authorized": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--validator-receipt", required=True, type=Path)
    parser.add_argument("--output-adapter", required=True, type=Path)
    arguments = parser.parse_args()
    try:
        output = build(
            arguments.run_dir, arguments.validator_receipt, arguments.output_adapter
        )
    except (Reject, OSError, ValueError, KeyError, TypeError) as error:
        print(canonical({
            "schema": "cm2.round306c30c.attack-receipt-evidence-adapter-build.v1",
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
