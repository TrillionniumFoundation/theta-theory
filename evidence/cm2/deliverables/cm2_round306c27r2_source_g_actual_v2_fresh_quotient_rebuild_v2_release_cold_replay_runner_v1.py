#!/usr/bin/env python3
"""Run a fresh no-import seed2 cold replay of the formal C27R2 core.

The core service must be the unique clean v6 formal-r2 invocation.  All core
files are declared transaction-runner inputs, so their pre/post SHA and
9-field stat identities are held across the replay.  The fresh verification
must be byte-identical to the core verification.  Success is conditional and
zero credit; this program cannot create a manifest, seal, or terminal receipt.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
AUDIT = ROOT / ".cm2-runtime/audit"
UNIT = "cm2-c27r2-source-g-authority-v2-v6-formal-r2-20260808T180523.service"
INVOCATION_ID = "aa82e1c6611f4910ae80b94307fb9ca9"
STEM = "c27r2-source-g-authority-v2-v6-formal-r2-20260808T180523"
CONTROL = AUDIT / (STEM + "-control")
CANDIDATE = AUDIT / (STEM + "-candidate")
CORE_VERIFICATION = AUDIT / (STEM + "-verifier-output/verification.json")
CORE_DIRS = [AUDIT / (STEM + suffix) for suffix in (
    "-control", "-candidate", "-producer-run", "-verifier-output",
    "-verifier-run", "-attack-work", "-attack-run",
)]
PYTHON = Path("/usr/bin/python3.12")
VERIFIER = ROOT / ("deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_"
                   "quotient_rebuild_v2_independent_verifier_v4.py")
RUNNER = ROOT / ("deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_"
                 "quotient_rebuild_v2_transaction_runner_v4.py")
VERIFIER_SHA = "acc66bbff3717e16bf56b15f9498070d97a4be1b0cd9253a79b7cae598b4082f"
RUNNER_SHA = "7ce75edac7e1aad904718e173cf6ed178f6d2631ba1f5cb4253bcf2c1e121d63"
PYTHON_SHA = "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118"
PINSET_SCHEMA = ("cm2.round306c27r2.source-g-actual-v2-fresh-quotient-"
                 "rebuild.v2.gated-transaction-pinset.v4")
SPEC_SCHEMA = ("cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild."
               "v2.process-command-spec.v4")
RUN_SCHEMA = ("cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild."
              "v2.process-run-attestation.v4")
RUN_STATUS = ("PASS_PROCESS_TRANSACTION_EXIT0_NULL_SIGNAL_EMPTY_STDERR_PRE_"
              "POST_AND_OUTPUTS__ZERO_CREDIT")
TRANSACTION_SCHEMA = ("cm2.round306c27r2.source-g-actual-v2-fresh-quotient-"
                      "rebuild.v2.gated-dual-seed-transaction-receipt.v4")
TRANSACTION_STATUS = ("PASS_GATE_SEED1_FOUR_FILE_CANDIDATE_SEED2_NO_IMPORT_"
                      "REPLAY_AND_21_ATTACKS__ZERO_CREDIT_PENDING_OUTER_SEAL_"
                      "AND_TERMINAL_REPLAY")
VERIFICATION_STATUS = ("PASS_NO_IMPORT_ACTUAL_V2_SEED2_INDEPENDENT_QUOTIENT_"
                       "AND_BYTE_EXACT_CANDIDATE_REPLAY__ZERO_CREDIT_PENDING_"
                       "ATTACKS_COLD_REPLAY_AND_TERMINAL_SEAL")
FILES = ["member_to_post_component.jsonl.gz",
         "old_c15_component_to_post_component.jsonl.gz",
         "post_component_census.jsonl.gz", "result.json"]


class Blocked(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Blocked(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def valid_sha(value: Any) -> bool:
    return (type(value) is str and len(value) == 64
            and all(character in "0123456789abcdef" for character in value))


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace(
        "+00:00", "Z")


def strict_load(payload: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(type(key) is str and key not in result, "unique JSON key")
            result[key] = value
        return result
    return json.loads(payload, object_pairs_hook=pairs,
                      parse_constant=lambda token: (_ for _ in ()).throw(
                          ValueError(token)))


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns,
            value.st_uid, value.st_gid)


def file_sha(path: Path) -> str:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                         | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular singleton:" + str(path))
        state = hashlib.sha256()
        while block := os.read(descriptor, 4 << 20):
            state.update(block)
        after = os.fstat(descriptor)
        need(fingerprint(before) == fingerprint(after),
             "stable SHA/stat:" + str(path))
        return state.hexdigest()
    finally:
        os.close(descriptor)


def document(path: Path, closure: str) -> dict[str, Any]:
    payload = path.read_bytes()
    need(payload.endswith(b"\n"), "JSON newline:" + str(path))
    value = strict_load(payload[:-1])
    need(type(value) is dict and canonical(value) == payload[:-1],
         "canonical JSON:" + str(path))
    body = dict(value)
    claim = body.pop(closure, None)
    need(valid_sha(claim) and claim == digest(body),
         "object closure:" + str(path))
    return value


def write_once(path: Path, payload: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                         | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        offset = 0
        while offset < len(payload):
            offset += os.write(descriptor, payload[offset:])
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def write_json(path: Path, value: Any) -> None:
    write_once(path, canonical(value) + b"\n")


def service_success() -> None:
    completed = subprocess.run(
        ["/usr/bin/systemctl", "--user", "show", UNIT,
         "-p", "ActiveState", "-p", "SubState", "-p", "Result",
         "-p", "ExecMainCode", "-p", "ExecMainStatus", "-p", "InvocationID"],
        cwd=ROOT, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False)
    need(completed.returncode == 0 and completed.stderr == b"",
         "query core service")
    fields = dict(line.split("=", 1) for line in
                  completed.stdout.decode("ascii").splitlines() if "=" in line)
    need(fields.get("ActiveState") == "active"
         and fields.get("SubState") == "exited"
         and fields.get("Result") == "success"
         and fields.get("ExecMainCode") in {"1", "exited"}
         and fields.get("ExecMainStatus") == "0"
         and fields.get("InvocationID") == INVOCATION_ID,
         "unique core service clean success")


def core_inputs() -> list[str]:
    result: list[str] = []
    for directory in CORE_DIRS:
        need(directory.is_dir() and not directory.is_symlink(),
             "complete core directory:" + directory.name)
        for current, directory_names, file_names in os.walk(directory):
            current_path = Path(current)
            for name in directory_names:
                need(not (current_path / name).is_symlink(),
                     "no core symlink directory")
            for name in file_names:
                path = current_path / name
                need(path.is_file() and not path.is_symlink(),
                     "regular core file")
                result.append(str(path.relative_to(ROOT)))
    return sorted(set(result))


def validate_core(expected_file: str, expected_object: str) -> dict[str, Any]:
    service_success()
    need(valid_sha(expected_file) and valid_sha(expected_object),
         "core receipt pins")
    receipt_path = CONTROL / "transaction_receipt.json"
    receipt = document(receipt_path, "transaction_receipt_sha256")
    need(file_sha(receipt_path) == expected_file
         and receipt["transaction_receipt_sha256"] == expected_object
         and receipt.get("schema") == TRANSACTION_SCHEMA
         and receipt.get("status") == TRANSACTION_STATUS
         and receipt.get("formal_credit") == 0
         and receipt.get("manifest_authorized") is False
         and receipt.get("C27R2")
             == "UNAUTHORIZED_PENDING_OUTER_SEAL_AND_TERMINAL_REPLAY"
         and (CONTROL / "PASS.lock").read_bytes()
             == b"PASS_C27R2_AUTHORITY_V2_GATED_DUAL_SEED_CORE__ZERO_CREDIT\n"
         and not (CONTROL / "FAILED.lock").exists(),
         "exact terminal core boundary")
    pinset = document(CONTROL / "pinset.json", "pinset_sha256")
    authority = pinset.get("actual_v2_authority")
    need(type(authority) is dict
         and type(authority.get("authority_input_paths")) is list,
         "actual-v2 authority in core pinset")
    need({entry.name for entry in CANDIDATE.iterdir()} == set(FILES),
         "exact four-file candidate")
    need(file_sha(VERIFIER) == VERIFIER_SHA
         and file_sha(RUNNER) == RUNNER_SHA
         and file_sha(PYTHON) == PYTHON_SHA,
         "frozen verifier/runner/Python pins")
    return authority


def failure(control: Path, stage: str, error: BaseException) -> None:
    body = {"schema": "cm2.round306c27r2.release-cold-replay-failure.v1",
            "status": "FAILED_CLOSED_RELEASE_COLD_REPLAY__ZERO_CREDIT",
            "failed_at_utc": utc_now(), "stage": stage,
            "error": f"{type(error).__name__}:{error}",
            "formal_credit": 0, "manifest_authorized": False,
            "C27R2": "UNAUTHORIZED", "C28_C29": "UNAUTHORIZED",
            "CM2": "NO-GO_FOR_CLAIM"}
    value = {**body, "failure_receipt_sha256": digest(body)}
    if not (control / "failure_receipt.json").exists():
        write_json(control / "failure_receipt.json", value)
    if not (control / "FAILED.lock").exists():
        write_once(control / "FAILED.lock",
                   b"FAILED_CLOSED_C27R2_RELEASE_COLD_REPLAY\n")


def execute(args: argparse.Namespace) -> dict[str, Any]:
    need(valid_sha(args.expect_helper_sha256)
         and file_sha(SELF) == args.expect_helper_sha256,
         "cold helper self pin")
    authority = validate_core(args.expect_core_receipt_file_sha256,
                              args.expect_core_receipt_object_sha256)
    control = Path(args.control_dir).absolute()
    output = Path(args.output_dir).absolute()
    run = Path(args.run_dir).absolute()
    need(len({control, output, run}) == 3
         and all(path.parent == AUDIT for path in (control, output, run))
         and all(not path.exists() for path in (control, output, run)),
         "fresh distinct cold replay paths")
    if args.preflight_only:
        return {"status": "PASS_CORE_AND_FRESH_COLD_REPLAY_PREFLIGHT__NO_PATHS_CREATED_ZERO_CREDIT"}
    stage = "create_control"
    try:
        control.mkdir(mode=0o700)
        output.mkdir(mode=0o700)
        pinset_body = {
            "schema": PINSET_SCHEMA,
            "status": "PASS_C27R2_RELEASE_COLD_REPLAY_PINSET__ZERO_CREDIT",
            "predecessor_unit": UNIT, "predecessor_invocation_id": INVOCATION_ID,
            "core_receipt_file_sha256": args.expect_core_receipt_file_sha256,
            "core_receipt_object_sha256": args.expect_core_receipt_object_sha256,
            "actual_v2_authority": authority,
            "source_pins": {"independent_verifier": VERIFIER_SHA,
                            "transaction_runner": RUNNER_SHA,
                            "cold_replay_helper": args.expect_helper_sha256,
                            "python": PYTHON_SHA},
            "targets": {"control": str(control.relative_to(ROOT)),
                        "output": str(output.relative_to(ROOT)),
                        "run": str(run.relative_to(ROOT))},
            "cold_replay_only": True, "formal_credit": 0,
            "manifest_authorized": False, "C27R2": "UNAUTHORIZED",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        pinset = {**pinset_body, "pinset_sha256": digest(pinset_body)}
        pinset_path = control / "pinset.json"
        write_json(pinset_path, pinset)
        verification_path = output / "verification.json"
        argv = [str(PYTHON), "-I", "-B", str(VERIFIER),
                "--terminal-dir", str(ROOT / authority["actual_terminal_dir"]),
                "--base-seal-dir", str(ROOT / authority["actual_base_seal_dir"]),
                "--expect-terminal-root-sha256",
                authority["actual_terminal_root_sha256"],
                "--expect-terminal-receipt-file-sha256",
                authority["actual_terminal_receipt_file_sha256"],
                "--expect-terminal-receipt-object-sha256",
                authority["actual_terminal_receipt_object_sha256"],
                "--candidate-dir", str(CANDIDATE),
                "--out-file", str(verification_path)]
        inputs = sorted(set(core_inputs() + [
            str(SELF.relative_to(ROOT)), str(VERIFIER.relative_to(ROOT)),
            str(RUNNER.relative_to(ROOT))]))
        spec_body = {
            "schema": SPEC_SCHEMA, "stage": "independent_verifier",
            "source_path": str(VERIFIER), "source_sha256": VERIFIER_SHA,
            "argv": argv,
            "environment": {"PATH": "/usr/bin:/bin", "LANG": "C",
                            "LC_ALL": "C", "PYTHONHASHSEED": "30662727"},
            "python_hash_seed": "30662727", "timeout_seconds": args.timeout_seconds,
            "expected_stdout_status": VERIFICATION_STATUS,
            "input_paths": inputs,
            "output_roots": [{"path": str(output), "kind": "directory",
                              "precondition": "EXISTING_EMPTY_DIRECTORY",
                              "exact_inventory": ["verification.json"],
                              "required_relative_files": ["verification.json"]}],
            "pinset_file_sha256": file_sha(pinset_path),
            "pinset_object_sha256": pinset["pinset_sha256"],
            "runner_source_sha256": RUNNER_SHA, "python_sha256": PYTHON_SHA,
            "formal_credit": 0, "CM2": "NO-GO_FOR_CLAIM",
        }
        spec = {**spec_body, "command_spec_sha256": digest(spec_body)}
        spec_path = control / "cold_command_spec.json"
        write_json(spec_path, spec)
        stage = "cold_no_import_verifier"
        completed = subprocess.run(
            [str(PYTHON), "-I", "-B", str(RUNNER),
             "--stage", "independent_verifier", "--command-spec", str(spec_path),
             "--pinset", str(pinset_path), "--run-dir", str(run),
             "--expect-runner-sha256", RUNNER_SHA,
             "--expect-python-sha256", PYTHON_SHA],
            cwd=ROOT, env={"PATH": "/usr/bin:/bin", "LANG": "C",
                           "LC_ALL": "C", "PYTHONHASHSEED": "30662728"},
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, check=False)
        write_once(control / "runner.stdout.log", completed.stdout)
        write_once(control / "runner.stderr.log", completed.stderr)
        write_once(control / "runner.exit_code.txt",
                   (str(completed.returncode) + "\n").encode("ascii"))
        need(completed.returncode == 0 and completed.stderr == b"",
             "cold runner clean exit")
        cold = document(verification_path, "verification_sha256")
        prior = document(CORE_VERIFICATION, "verification_sha256")
        need(verification_path.read_bytes() == CORE_VERIFICATION.read_bytes()
             and cold["verification_sha256"] == prior["verification_sha256"],
             "cold replay byte-identical to formal seed2 verification")
        run_attestation = document(run / "run_attestation.json",
                                   "run_attestation_sha256")
        need(run_attestation.get("schema") == RUN_SCHEMA
             and run_attestation.get("status") == RUN_STATUS
             and run_attestation.get("numeric_exit_code") == 0
             and run_attestation.get("signal") is None
             and run_attestation.get("stderr_empty") is True
             and run_attestation.get("input_pre_post_sha_stat_identical") is True,
             "cold transaction attestation")
        body = {
            "schema": "cm2.round306c27r2.source-g-authority-v2.release-cold-replay-receipt.v1",
            "status": "PASS_FRESH_NO_IMPORT_SEED2_COLD_BYTE_REPLAY_WITH_ALL_CORE_INPUT_PRE_POST_SHA_STAT__ZERO_CREDIT",
            "completed_at_utc": utc_now(), "predecessor_unit": UNIT,
            "predecessor_invocation_id": INVOCATION_ID,
            "core_receipt_file_sha256": args.expect_core_receipt_file_sha256,
            "core_receipt_object_sha256": args.expect_core_receipt_object_sha256,
            "verification_file_sha256": file_sha(verification_path),
            "verification_object_sha256": cold["verification_sha256"],
            "formal_verification_byte_identical": True,
            "run_attestation_file_sha256": file_sha(run / "run_attestation.json"),
            "run_attestation_object_sha256":
                run_attestation["run_attestation_sha256"],
            "numeric_exit_code": 0, "signal": None, "stderr_empty": True,
            "all_core_inputs_pre_post_sha_stat_identical": True,
            "formal_credit": 0, "manifest_authorized": False,
            "C27R2": "UNAUTHORIZED_PENDING_RELEASE_ATTACKS_MANIFEST_OUTER_AND_TERMINAL_REPLAY",
            "C28_C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM",
        }
        receipt = {**body, "cold_replay_receipt_sha256": digest(body)}
        write_json(control / "cold_replay_receipt.json", receipt)
        write_once(control / "PASS.lock",
                   b"PASS_C27R2_RELEASE_COLD_REPLAY__ZERO_CREDIT\n")
        return receipt
    except BaseException as error:
        if control.exists():
            failure(control, stage, error)
        raise


def self_test() -> dict[str, Any]:
    required = ["verification.json"]
    need(required == sorted(set(required)) and valid_sha(VERIFIER_SHA),
         "canonical inventory/source pin fixture")
    return {"status": "PASS_COLD_REPLAY_INVENTORY_AND_SOURCE_PIN_FIXTURE"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--control-dir")
    parser.add_argument("--output-dir")
    parser.add_argument("--run-dir")
    parser.add_argument("--expect-core-receipt-file-sha256")
    parser.add_argument("--expect-core-receipt-object-sha256")
    parser.add_argument("--expect-helper-sha256")
    parser.add_argument("--timeout-seconds", type=int, default=10_800)
    args = parser.parse_args()
    fields = ("control_dir", "output_dir", "run_dir",
              "expect_core_receipt_file_sha256",
              "expect_core_receipt_object_sha256", "expect_helper_sha256")
    try:
        if args.self_test:
            need(not args.preflight_only
                 and all(getattr(args, field) is None for field in fields),
                 "self-test accepts no run arguments")
            result = self_test()
        else:
            need(all(getattr(args, field) is not None for field in fields)
                 and 60 <= args.timeout_seconds <= 86_400,
                 "all run arguments and bounded timeout")
            result = execute(args)
        sys.stdout.buffer.write(canonical({"CM2": "NO-GO_FOR_CLAIM",
            "formal_credit": 0, "status": result["status"]}) + b"\n")
        return 0
    except (Blocked, OSError, ValueError, KeyError, TypeError,
            subprocess.SubprocessError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
