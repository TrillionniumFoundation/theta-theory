#!/usr/bin/env python3
"""Fail-closed seed2 handoff after a complete seed1 actual-v2 transaction."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import signal
import stat
import subprocess
import sys
import time
from typing import Any


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
WATCHER = Path(__file__).resolve()
RUNNER = ROOT / "deliverables/cm2_c27_primitive_twenty_family_gate_v5_actual_v2_runner.py"
PYTHON = Path("/usr/bin/python3.12")
EXPECTED_LEDGER_COUNTS = {
    "candidate_ownership": 7_486_076,
    "materialized_physical_proof_join": 65_064,
    "atom_pair_incidence": 206_632,
    "atom_incidence_disposition": 483_232,
    "full_component_edge_union": 14_860,
}
EXPECTED_OUTPUT_NAMES = {
    *(name + ".jsonl.gz" for name in EXPECTED_LEDGER_COUNTS),
    "assembler_receipt.json", "manifest.sha256",
}


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def identity(info: os.stat_result) -> list[int]:
    return [info.st_dev, info.st_ino, info.st_mode, info.st_nlink,
            info.st_size, info.st_mtime_ns, info.st_ctime_ns,
            info.st_uid, info.st_gid]


def fsha(path: Path) -> str:
    state = hashlib.sha256()
    descriptor = os.open(path, os.O_RDONLY | os.O_CLOEXEC
                         | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular singleton:" + os.fspath(path))
        while True:
            block = os.read(descriptor, 4 << 20)
            if not block:
                break
            state.update(block)
        after = os.fstat(descriptor)
        need(identity(before) == identity(after),
             "stable hash inode:" + os.fspath(path))
    finally:
        os.close(descriptor)
    return state.hexdigest()


def strict_json(path: Path) -> Any:
    raw = path.read_bytes()

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(key not in result, "duplicate JSON key:" + path.name)
            result[key] = value
        return result

    value = json.loads(raw, object_pairs_hook=pairs,
                       parse_constant=lambda item: (_ for _ in ()).throw(
                           Failure("non-finite JSON:" + item)))
    need(raw == canonical(value) + b"\n", "canonical JSON:" + path.name)
    return value


def closed(path: Path, key: str) -> dict[str, Any]:
    value = strict_json(path)
    need(type(value) is dict, "closed JSON object:" + path.name)
    body = dict(value)
    claim = body.pop(key, None)
    need(type(claim) is str and claim == digest(body),
         "JSON object closure:" + path.name)
    return value


def exclusive(path: Path, payload: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                         | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        offset = 0
        while offset < len(payload):
            offset += os.write(descriptor, payload[offset:])
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def write_json(path: Path, value: Any) -> None:
    exclusive(path, canonical(value) + b"\n")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace(
        "+00:00", "Z")


def service_state(unit: str) -> str:
    completed = subprocess.run(
        ["/usr/bin/systemctl", "--user", "show", unit,
         "--property=ActiveState", "--value"],
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=False,
        env=os.environ.copy())
    value = completed.stdout.decode("ascii", "strict").strip()
    return value if completed.returncode == 0 and value else "not-found"


def wait_for_seed1(unit: str, run_dir: Path, timeout_seconds: int) -> str:
    deadline = time.monotonic() + timeout_seconds
    while True:
        state = service_state(unit)
        passed = (run_dir / "PASS.lock").is_file()
        failed = (run_dir / "FAILED.lock").exists()
        if failed:
            raise Failure("seed1 FAILED.lock present")
        if passed and state not in {"active", "activating", "deactivating"}:
            return state
        if not passed and state not in {"active", "activating", "deactivating"}:
            raise Failure("seed1 stopped without PASS.lock:" + state)
        if time.monotonic() >= deadline:
            raise Failure("seed1 handoff timeout")
        time.sleep(15)


def validate_seed1(seed: int, out_dir: Path,
                   run_dir: Path) -> dict[str, Any]:
    need((run_dir / "PASS.lock").read_bytes()
         == b"PASS_TRANSACTION_COMPLETE__ZERO_CREDIT\n"
         and not (run_dir / "FAILED.lock").exists(),
         "seed1 exclusive PASS terminal state")
    attestation_path = run_dir / "run_attestation.json"
    attestation = closed(attestation_path, "run_attestation_sha256")
    need(attestation["execution_seed"] == seed
         and attestation["numeric_exit_code"] == 0
         and attestation["signal"] is None
         and attestation["stderr_empty"] is True
         and attestation["pre_post_sha256_identical"] is True
         and attestation["pre_post_stat_identical"] is True
         and attestation["formal_credit"] == 0
         and attestation["manifest_authorized"] is False
         and attestation["CM2"] == "NO-GO_FOR_CLAIM",
         "seed1 run attestation conclusion")
    need((run_dir / "exit_code.txt").read_bytes() == b"0\n"
         and strict_json(run_dir / "signal.json") is None
         and (run_dir / "stderr.log").read_bytes() == b"",
         "seed1 exit0/no-signal/empty-stderr files")
    input_pre = strict_json(run_dir / "input_pre.json")
    input_post = strict_json(run_dir / "input_post.json")
    need(input_pre == input_post == attestation["input_pre"]
         == attestation["input_post"], "seed1 pre/post snapshot closure")
    validation_path = run_dir / "output_validation.json"
    validation = strict_json(validation_path)
    need(type(validation) is dict
         and digest(validation) == attestation["output_validation_sha256"]
         and validation["status"]
             == "PASS_7_OF_7_GZIP_CANONICAL_COUNT_CLOSURE"
         and validation["output_file_count"] == 7
         and validation["formal_credit"] == 0
         and validation["manifest_authorized"] is False
         and set(validation["ledgers"]) == set(EXPECTED_LEDGER_COUNTS),
         "seed1 seven-output validation closure")
    for name, count in EXPECTED_LEDGER_COUNTS.items():
        item = validation["ledgers"][name]
        need(item["row_count"] == count
             and item["gzip_integrity"] == "PASS"
             and item["canonical_rows"] == "PASS"
             and item["strict_ordering"] == "PASS"
             and item["row_object_closure"] == "PASS"
             and item["formal_credit"] == 0,
             "seed1 ledger validation:" + name)
    entries = sorted(out_dir.iterdir(), key=lambda item: item.name)
    need({entry.name for entry in entries} == EXPECTED_OUTPUT_NAMES,
         "seed1 current exact seven outputs")
    for entry in entries:
        recorded = validation["output_files"][entry.name]
        need(fsha(entry) == recorded["sha256"]
             and identity(entry.stat()) == recorded["stat"],
             "seed1 current output SHA/stat:" + entry.name)
    receipt = closed(out_dir / "assembler_receipt.json",
                     "assembler_receipt_sha256")
    need(receipt["execution_seed"] == seed
         and receipt["formal_credit"] == 0
         and receipt["manifest_authorized"] is False
         and receipt["CM2"] == "NO-GO_FOR_CLAIM",
         "seed1 assembler receipt zero-credit")
    return {
        "run_attestation_file_sha256": fsha(attestation_path),
        "run_attestation_object_sha256":
            attestation["run_attestation_sha256"],
        "output_validation_file_sha256": fsha(validation_path),
        "output_validation_object_sha256": digest(validation),
        "assembler_receipt_file_sha256":
            fsha(out_dir / "assembler_receipt.json"),
        "assembler_receipt_object_sha256":
            receipt["assembler_receipt_sha256"],
        "pass_lock_sha256": fsha(run_dir / "PASS.lock"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed1", required=True, type=int)
    parser.add_argument("--seed1-service", required=True)
    parser.add_argument("--seed1-out-dir", required=True)
    parser.add_argument("--seed1-run-dir", required=True)
    parser.add_argument("--seed2", required=True, type=int)
    parser.add_argument("--seed2-out-dir", required=True)
    parser.add_argument("--seed2-run-dir", required=True)
    parser.add_argument("--handoff-dir", required=True)
    parser.add_argument("--expect-watcher-sha256", required=True)
    parser.add_argument("--expect-runner-sha256", required=True)
    parser.add_argument("--timeout-seconds", type=int, default=172800)
    args = parser.parse_args()
    seed1_out = Path(args.seed1_out_dir).resolve()
    seed1_run = Path(args.seed1_run_dir).resolve()
    seed2_out = Path(args.seed2_out_dir).resolve()
    seed2_run = Path(args.seed2_run_dir).resolve()
    handoff = Path(args.handoff_dir).resolve()
    need(all(ROOT in path.parents
             for path in (seed1_out, seed1_run, seed2_out, seed2_run,
                           handoff)), "all paths inside workspace")
    need(args.seed1 > 0 and args.seed2 > 0 and args.seed1 != args.seed2,
         "two distinct positive real seeds")
    need(not seed2_out.exists() and not seed2_run.exists()
         and not handoff.exists(), "fresh seed2/handoff paths")
    handoff.mkdir(parents=True, mode=0o700)
    stage = "watcher_initialization"
    try:
        need(fsha(WATCHER) == args.expect_watcher_sha256,
             "watcher launch SHA256 pin")
        need(fsha(RUNNER) == args.expect_runner_sha256,
             "runner handoff SHA256 pin")
        write_json(handoff / "watcher_start.json", {
            "schema": "cm2.c27-actual-v2.seed2-gated-handoff-watcher.v1",
            "status": "WAITING_FOR_SEED1_TERMINAL_PASS__ZERO_CREDIT",
            "started_at_utc": utc_now(), "watcher_pid": os.getpid(),
            "seed1_service": args.seed1_service,
            "seed1": args.seed1, "seed2": args.seed2,
            "watcher_source_sha256": args.expect_watcher_sha256,
            "runner_source_sha256": args.expect_runner_sha256,
            "formal_credit": 0, "manifest_authorized": False,
            "CM2": "NO-GO_FOR_CLAIM",
        })

        def interrupted(signum: int, _frame: Any) -> None:
            raise Failure("watcher interrupted by signal:" + str(signum))

        for item in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
            signal.signal(item, interrupted)
        stage = "wait_for_seed1"
        terminal_service_state = wait_for_seed1(
            args.seed1_service, seed1_run, args.timeout_seconds)
        stage = "validate_seed1"
        evidence = validate_seed1(args.seed1, seed1_out, seed1_run)
        need(fsha(RUNNER) == args.expect_runner_sha256,
             "runner unchanged at seed2 handoff")
        need(not seed2_out.exists() and not seed2_run.exists(),
             "fresh seed2 paths at handoff")
        body = {
            "schema": "cm2.c27-actual-v2.seed2-gated-handoff-receipt.v1",
            "status": "PASS_SEED1_FULL_TRANSACTION_AND_CURRENT_HASHES__EXEC_SEED2_ZERO_CREDIT",
            "recorded_at_utc": utc_now(),
            "seed1": args.seed1, "seed1_service_terminal_state":
                terminal_service_state,
            "seed1_evidence": evidence,
            "seed2": args.seed2,
            "seed2_out_dir": str(seed2_out.relative_to(ROOT)),
            "seed2_run_dir": str(seed2_run.relative_to(ROOT)),
            "watcher_source_sha256": args.expect_watcher_sha256,
            "runner_source_sha256": args.expect_runner_sha256,
            "formal_credit": 0, "manifest_authorized": False,
            "C27_C28_C29": "UNAUTHORIZED_PENDING_DUAL_SEED_FINAL_RECEIPT_V2",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        receipt = dict(body)
        receipt["handoff_receipt_sha256"] = digest(receipt)
        write_json(handoff / "handoff_receipt.json", receipt)
        exclusive(handoff / "HANDOFF_GATE_PASS.lock",
                  b"PASS_TO_EXEC_SEED2__ZERO_CREDIT\n")
        command = [str(PYTHON), "-I", "-B", str(RUNNER),
                   "--seed", str(args.seed2),
                   "--out-dir", str(seed2_out),
                   "--run-dir", str(seed2_run),
                   "--expect-runner-sha256", args.expect_runner_sha256]
        environment = {"HOME": "/nonexistent", "LC_ALL": "C.UTF-8",
                       "TZ": "UTC", "PYTHONDONTWRITEBYTECODE": "1"}
        os.execve(PYTHON, command, environment)
    except BaseException as error:
        failure = {
            "schema": "cm2.c27-actual-v2.seed2-handoff-failure.v1",
            "status": "FAIL_CLOSED_SEED2_NOT_STARTED__ZERO_CREDIT",
            "stage": stage, "error_type": type(error).__name__,
            "error": str(error), "recorded_at_utc": utc_now(),
            "formal_credit": 0, "manifest_authorized": False,
            "C27_C28_C29": "UNAUTHORIZED",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        try:
            write_json(handoff / "failure.json", failure)
            exclusive(handoff / "FAILED.lock",
                      b"FAIL_CLOSED_SEED2_NOT_STARTED__ZERO_CREDIT\n")
        except FileExistsError:
            pass
        print("FAIL:" + str(error))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
