#!/usr/bin/env python3
"""Minimal append-only runner for the post-actual-v2 C27R2 rebuild gate v3.

This runner creates only a gate-control directory.  It has no C27R2 rebuild
implementation and no service-launch path.  A positive result authorizes a
future fresh rebuild to begin; it is not C27R2 authority or formal credit.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import time
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
PYTHON = Path("/usr/bin/python3.12")
SOURCES = {
    "producer": ROOT / "deliverables/cm2_round306c27r2_post_actual_v2_rebuild_gate_v3.py",
    "independent_verifier": ROOT / "deliverables/cm2_round306c27r2_post_actual_v2_rebuild_gate_v3_independent_verifier.py",
    "coherent_attack_harness": ROOT / "deliverables/cm2_round306c27r2_post_actual_v2_rebuild_gate_v3_coherent_attack_harness.py",
    "python": PYTHON,
}
SOURCE_PINS = {
    "producer": "aab253ba102dc5f168ff96089145ea8a23a3f4ff8255dad92d668430c93c82f8",
    "independent_verifier": "f3a5e2c00d46aaef4635cb7b7688d090b540d46dfcd7d06fe22212abe6e2c373",
    "coherent_attack_harness": "d94ae7226b372659c98650b6ee2fd0a839f375983148a6cb6d7448f476c17919",
    "python": "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118",
}
OUTPUT_PREFIX = "c27r2-post-actual-v2-rebuild-gate-v3-zero-credit-"


class Reject(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def wire(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def object_sha(value: Any) -> str:
    return hashlib.sha256(wire(value)).hexdigest()


def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in result, "duplicate-key:" + key)
        result[key] = value
    return result


def parse_closed(path: Path, closure: str, label: str) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    value = json.loads(
        raw, object_pairs_hook=unique,
        parse_constant=lambda item: (_ for _ in ()).throw(
            Reject(label + ":nonfinite:" + item)))
    need(type(value) is dict and raw == wire(value) + b"\n", label + ":canonical")
    body = dict(value)
    claim = body.pop(closure, None)
    need(type(claim) is str and claim == object_sha(body), label + ":closure")
    return value, raw


def file_sha(path: Path) -> str:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                         | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular-single-link:" + str(path))
        identity = (before.st_dev, before.st_ino, before.st_mode,
                    before.st_nlink, before.st_size, before.st_mtime_ns,
                    before.st_ctime_ns, before.st_uid, before.st_gid)
        state = hashlib.sha256()
        while block := os.read(descriptor, 4 << 20):
            state.update(block)
        after = os.fstat(descriptor)
        need(identity == (after.st_dev, after.st_ino, after.st_mode,
                          after.st_nlink, after.st_size, after.st_mtime_ns,
                          after.st_ctime_ns, after.st_uid, after.st_gid),
             "stable-fstat:" + str(path))
        return state.hexdigest()
    finally:
        os.close(descriptor)


def write_new(path: Path, raw: bytes) -> None:
    need(path.parent.is_dir(), "output-parent")
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                         | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        os.write(descriptor, raw)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def stage(output: Path, name: str, command: list[str], expected_exit: int) -> dict[str, Any]:
    started = time.time_ns()
    process = subprocess.run(command, cwd=ROOT, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, check=False)
    ended = time.time_ns()
    write_new(output / (name + ".stdout.log"), process.stdout)
    write_new(output / (name + ".stderr.log"), process.stderr)
    write_new(output / (name + ".exit_code.txt"),
              (str(process.returncode) + "\n").encode("ascii"))
    need(process.returncode == expected_exit, name + ":expected-exit")
    need(process.stderr == b"", name + ":empty-stderr")
    return {
        "name": name, "expected_exit_code": expected_exit,
        "observed_exit_code": process.returncode,
        "stdout_sha256": hashlib.sha256(process.stdout).hexdigest(),
        "stderr_sha256": hashlib.sha256(process.stderr).hexdigest(),
        "stderr_empty": True, "started_time_ns": started,
        "ended_time_ns": ended, "duration_ns": ended - started,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--negative-missing-self-test", type=Path)
    args = parser.parse_args()
    try:
        output = Path(args.output_dir).resolve()
        need(output.name.startswith(OUTPUT_PREFIX), "gate-only-output-name")
        need(output.parent.is_dir() and not output.exists(), "fresh-output-directory")
        for label, path in SOURCES.items():
            need(file_sha(path) == SOURCE_PINS[label], "source-pin:" + label)
        os.mkdir(output, 0o700)

        receipt_path = output / "gate_receipt.json"
        producer_command = [
            str(PYTHON), str(SOURCES["producer"]),
            "--output", str(receipt_path),
        ]
        negative = args.negative_missing_self_test is not None
        if negative:
            missing = args.negative_missing_self_test.resolve()
            need(missing.is_absolute() and not missing.exists()
                 and not (missing == ROOT or ROOT in missing.parents),
                 "negative-path-absent-outside-workspace")
            producer_command.extend(["--negative-missing-self-test", str(missing)])
        stages = [stage(output, "producer", producer_command, 2 if negative else 0)]

        receipt, receipt_raw = parse_closed(
            receipt_path, "gate_receipt_sha256", "gate-receipt")
        need(receipt["decision"] == ("REJECT" if negative else "PASS")
             and receipt["fresh_C27R2_rebuild_may_start"] is (not negative)
             and receipt["formal_credit"] == 0
             and receipt["manifest_authorized"] is False
             and receipt["CM2"] == "NO-GO_FOR_CLAIM",
             "producer-receipt-mode")

        verification_path = output / "independent_verification.json"
        stages.append(stage(output, "independent_verifier", [
            str(PYTHON), str(SOURCES["independent_verifier"]),
            "--receipt", str(receipt_path),
            "--producer-source", str(SOURCES["producer"]),
            "--expect-producer-sha256", SOURCE_PINS["producer"],
            "--output", str(verification_path),
        ], 0))
        verification, verification_raw = parse_closed(
            verification_path, "verification_sha256", "independent-verification")
        need(verification["gate_receipt_file_sha256"]
             == hashlib.sha256(receipt_raw).hexdigest()
             and verification["gate_receipt_object_sha256"]
                 == receipt["gate_receipt_sha256"]
             and verification["gate_decision"] == receipt["decision"]
             and verification["fresh_C27R2_rebuild_may_start"]
                 is receipt["fresh_C27R2_rebuild_may_start"]
             and verification["formal_credit"] == 0
             and verification["manifest_authorized"] is False,
             "independent-verification-binding")

        attacks_path = output / "coherent_attacks.json"
        stages.append(stage(output, "coherent_attacks", [
            str(PYTHON), str(SOURCES["coherent_attack_harness"]),
            "--receipt", str(receipt_path),
            "--control-verification", str(verification_path),
            "--verifier-source", str(SOURCES["independent_verifier"]),
            "--producer-source", str(SOURCES["producer"]),
            "--expect-verifier-sha256", SOURCE_PINS["independent_verifier"],
            "--expect-producer-sha256", SOURCE_PINS["producer"],
            "--output", str(attacks_path),
        ], 0))
        attacks, attacks_raw = parse_closed(
            attacks_path, "attack_result_sha256", "coherent-attacks")
        need(attacks["attack_total"] == attacks["attack_passed"] == 16
             and attacks["all_forged_receipts_rejected_without_artifact"] is True
             and attacks["gate_receipt_file_sha256"]
                 == hashlib.sha256(receipt_raw).hexdigest()
             and attacks["control_verification_file_sha256"]
                 == hashlib.sha256(verification_raw).hexdigest()
             and attacks["fresh_C27R2_rebuild_may_start"] is (not negative)
             and attacks["formal_credit"] == 0
             and attacks["manifest_authorized"] is False,
             "coherent-attack-binding")

        body = {
            "schema": "cm2.round306c27r2.post-actual-v2-rebuild-gate-execution.v3",
            "status": (
                "PASS_GATE_PRODUCER_INDEPENDENT_VERIFIER_AND_16_COHERENT_ATTACKS__"
                "FRESH_C27R2_REBUILD_MAY_BEGIN__ZERO_CREDIT"
                if not negative else
                "PASS_NEGATIVE_MISSING_TERMINAL_SELF_TEST_REJECTED_AND_INDEPENDENTLY_"
                "VERIFIED_WITH_16_COHERENT_ATTACKS__ZERO_CREDIT"
            ),
            "mode": "NEGATIVE_MISSING_TERMINAL_SELF_TEST" if negative else "POSITIVE",
            "source_pins": SOURCE_PINS,
            "stage_total": 3, "stages": stages,
            "gate_receipt_file_sha256": hashlib.sha256(receipt_raw).hexdigest(),
            "gate_receipt_object_sha256": receipt["gate_receipt_sha256"],
            "independent_verification_file_sha256": hashlib.sha256(verification_raw).hexdigest(),
            "independent_verification_object_sha256": verification["verification_sha256"],
            "coherent_attacks_file_sha256": hashlib.sha256(attacks_raw).hexdigest(),
            "coherent_attacks_object_sha256": attacks["attack_result_sha256"],
            "gate_decision": receipt["decision"],
            "actual_v2_terminal_gate_validated": receipt["actual_v2_terminal_gate_validated"],
            "fresh_C27R2_rebuild_may_start": receipt["fresh_C27R2_rebuild_may_start"],
            "runner_action_surface": [
                "gate_receipt", "independent_verification", "coherent_attacks",
                "stage_attestations", "execution_receipt", "gate_lock",
            ],
            "C27R2_rebuild_candidate_created": False,
            "C27R2_rebuild_output_created": False,
            "C27R2_rebuild_seal_created": False,
            "C27R2_rebuild_service_created_or_started": False,
            "formal_credit": 0, "manifest_authorized": False,
            "C27R2": "PREFLIGHT_GATE_PASS_ONLY__NOT_REBUILT_NOT_CREDITED"
                if not negative else "UNAUTHORIZED",
            "C28": "UNAUTHORIZED", "C29": "UNAUTHORIZED",
            "CM2": "NO-GO_FOR_CLAIM",
            "intended_process_exit_code": 2 if negative else 0,
        }
        body["execution_receipt_sha256"] = object_sha(body)
        write_new(output / "execution_receipt.json", wire(body) + b"\n")
        lock_name = "NEGATIVE_SELF_TEST_PASS.lock" if negative else "PASS.lock"
        lock = (
            b"PASS_NEGATIVE_MISSING_TERMINAL_GATE_V3_SELF_TEST__ZERO_CREDIT\n"
            if negative else
            b"PASS_POST_ACTUAL_V2_C27R2_REBUILD_GATE_V3__FRESH_REBUILD_MAY_BEGIN__ZERO_CREDIT\n"
        )
        write_new(output / lock_name, lock)
        print(wire({"status": body["status"],
                    "execution_receipt_sha256": body["execution_receipt_sha256"],
                    "fresh_C27R2_rebuild_may_start":
                        body["fresh_C27R2_rebuild_may_start"]}).decode("ascii"))
        return 2 if negative else 0
    except (Reject, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError, subprocess.SubprocessError) as error:
        print("REJECT:" + str(error))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
