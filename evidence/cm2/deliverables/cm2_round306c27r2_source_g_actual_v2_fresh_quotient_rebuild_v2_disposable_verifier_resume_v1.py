#!/usr/bin/env python3
"""Resume one disposable C27R2 v4 producer fixture at the verifier stage.

This is test-only plumbing.  It binds a completed zero-credit producer fixture,
creates a fresh verifier output and runner transaction, executes the v4
no-import verifier against the same four-file candidate, and emits a separate
zero-credit receipt.  It never runs attacks or starts a service.
"""

from __future__ import annotations

import argparse
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
PYTHON = Path("/usr/bin/python3.12")
VERIFIER = ROOT / (
    "deliverables/"
    "cm2_round306c27r2_source_g_actual_v2_fresh_quotient_rebuild_v2_"
    "independent_verifier_v4.py"
)
RUNNER = ROOT / (
    "deliverables/"
    "cm2_round306c27r2_source_g_actual_v2_fresh_quotient_rebuild_v2_"
    "transaction_runner_v4.py"
)
PINSET_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "gated-transaction-pinset.v4"
)
COMMAND_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "process-command-spec.v4"
)
RUN_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "process-run-attestation.v4"
)
RUN_STATUS = (
    "PASS_PROCESS_TRANSACTION_EXIT0_NULL_SIGNAL_EMPTY_STDERR_PRE_POST_"
    "AND_OUTPUTS__ZERO_CREDIT"
)
VERIFICATION_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "independent-verification.v1"
)
VERIFICATION_STATUS = (
    "PASS_NO_IMPORT_ACTUAL_V2_SEED2_INDEPENDENT_QUOTIENT_AND_BYTE_EXACT_"
    "CANDIDATE_REPLAY__ZERO_CREDIT_PENDING_ATTACKS_COLD_REPLAY_AND_"
    "TERMINAL_SEAL"
)
FIXTURE_STATUS = (
    "PASS_DISPOSABLE_REAL_INPUT_SEED1_PRODUCER_EXACT_FOUR_FILE_"
    "CANDIDATE_AND_RUNNER_ATTESTATION__ZERO_CREDIT"
)
FILES = [
    "member_to_post_component.jsonl.gz",
    "old_c15_component_to_post_component.jsonl.gz",
    "post_component_census.jsonl.gz",
    "result.json",
]
EXPECTED_PROJECTION = {
    "old_components": 57_876,
    "edges": 14_860,
    "merges": 14_192,
    "cycles": 668,
    "post_components": 43_684,
    "members": 502_204,
    "within_pairs": 542_179_508,
    "cross_pairs": 125_561_998_198,
}


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def valid_sha(value: Any) -> bool:
    return (
        type(value) is str and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def strict_load(payload: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(key not in result, "duplicate JSON key:" + key)
            result[key] = value
        return result

    def constant(value: str) -> None:
        raise Failure("non-finite JSON:" + value)

    return json.loads(payload, object_pairs_hook=pairs, parse_constant=constant)


def inside(raw: str | Path, *, absent: bool = False) -> Path:
    supplied = Path(raw)
    path = (ROOT / supplied if not supplied.is_absolute()
            else supplied).absolute()
    try:
        relative = path.relative_to(ROOT)
    except ValueError as error:
        raise Failure("path outside workspace:" + str(raw)) from error
    need(all(part not in {"", ".", ".."} for part in relative.parts),
         "canonical workspace path:" + str(raw))
    current = ROOT
    for part in relative.parts:
        current = current / part
        if not current.exists():
            need(absent, "missing path component:" + str(current))
            break
        need(not current.is_symlink(), "symlink path component:" + str(current))
    return path


def file_sha(path: Path) -> str:
    descriptor = os.open(
        path,
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular single-link:" + str(path))
        state = hashlib.sha256()
        while block := os.read(descriptor, 4 << 20):
            state.update(block)
        after = os.fstat(descriptor)
        need((before.st_dev, before.st_ino, before.st_mode, before.st_nlink,
              before.st_size, before.st_mtime_ns, before.st_ctime_ns)
             == (after.st_dev, after.st_ino, after.st_mode, after.st_nlink,
                 after.st_size, after.st_mtime_ns, after.st_ctime_ns),
             "stable file hash:" + str(path))
        return state.hexdigest()
    finally:
        os.close(descriptor)


def document(path: Path, closure: str) -> dict[str, Any]:
    payload = path.read_bytes()
    need(payload.endswith(b"\n"), "document newline:" + str(path))
    value = strict_load(payload[:-1])
    need(type(value) is dict and canonical(value) == payload[:-1],
         "canonical document:" + str(path))
    body = dict(value)
    claim = body.pop(closure, None)
    need(valid_sha(claim) and claim == digest(body),
         "document closure:" + str(path))
    return value


def write_once(path: Path, payload: bytes) -> None:
    descriptor = os.open(
        path,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
        0o600,
    )
    try:
        offset = 0
        while offset < len(payload):
            offset += os.write(descriptor, payload[offset:])
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def write_json(path: Path, value: Any) -> None:
    write_once(path, canonical(value) + b"\n")


def execute(args: argparse.Namespace) -> dict[str, Any]:
    pins = (
        args.expect_fixture_receipt_file_sha256,
        args.expect_fixture_receipt_object_sha256,
        args.expect_result_file_sha256,
        args.expect_verifier_sha256,
        args.expect_runner_sha256,
        args.expect_helper_sha256,
        args.expect_python_sha256,
    )
    need(all(valid_sha(value) for value in pins), "all external SHA pins")
    need(file_sha(SELF) == args.expect_helper_sha256, "helper self pin")
    need(file_sha(VERIFIER) == args.expect_verifier_sha256, "verifier pin")
    need(file_sha(RUNNER) == args.expect_runner_sha256, "runner pin")
    need(file_sha(PYTHON) == args.expect_python_sha256, "Python pin")

    prior = inside(args.prior_control_dir)
    candidate = inside(args.candidate_dir)
    control = inside(args.control_dir, absent=True)
    output = inside(args.verifier_output_dir, absent=True)
    run = inside(args.verifier_run_dir, absent=True)
    need(prior.is_dir() and candidate.is_dir(), "prior control/candidate dirs")
    need(len({control, output, run}) == 3
         and all(not path.exists() for path in (control, output, run)),
         "fresh distinct resume targets")
    inventory = sorted(path.name for path in candidate.iterdir())
    need(inventory == FILES and all((candidate / name).is_file()
                                    for name in FILES),
         "same exact four-file candidate")

    fixture_path = prior / "producer_stage_fixture_receipt.json"
    fixture = document(fixture_path, "producer_stage_fixture_receipt_sha256")
    need(file_sha(fixture_path) == args.expect_fixture_receipt_file_sha256
         and fixture["producer_stage_fixture_receipt_sha256"]
             == args.expect_fixture_receipt_object_sha256
         and fixture.get("status") == FIXTURE_STATUS
         and fixture.get("candidate_dir")
             == str(candidate.relative_to(ROOT))
         and fixture.get("candidate_exact_inventory") == FILES
         and fixture.get("producer_numeric_exit_code") == 0
         and fixture.get("producer_signal") is None
         and fixture.get("producer_stderr_empty") is True
         and fixture.get("producer_inputs_pre_post_sha_stat_identical") is True
         and fixture.get("formal_credit") == 0
         and fixture.get("manifest_authorized") is False
         and fixture.get("CM2") == "NO-GO_FOR_CLAIM",
         "producer fixture exact zero-credit PASS")
    result_path = candidate / "result.json"
    result = document(result_path, "result_sha256")
    need(file_sha(result_path) == args.expect_result_file_sha256
         == fixture["candidate_result_file_sha256"]
         and result["result_sha256"]
             == fixture["candidate_result_object_sha256"],
         "producer result fixture binding")
    producer_path = inside(result["producer_source_attestation"]["path"])
    need(file_sha(producer_path) == result["producer_source_sha256"]
         == result["producer_source_attestation"]["sha256"],
         "producer source current result pin")

    prior_pinset_path = prior / "pinset.json"
    prior_pinset = document(prior_pinset_path, "pinset_sha256")
    need(prior_pinset.get("schema") == PINSET_SCHEMA
         and prior_pinset.get("source_pins", {}).get("independent_verifier")
             == args.expect_verifier_sha256
         and prior_pinset.get("source_pins", {}).get("transaction_runner")
             == args.expect_runner_sha256,
         "prior pinset v4 verifier/runner")
    authority = prior_pinset.get("actual_v2_authority")
    need(type(authority) is dict
         and type(authority.get("authority_input_paths")) is list,
         "prior actual-v2 authority capture")

    control.mkdir(parents=True, mode=0o700)
    output.mkdir(parents=True, mode=0o700)
    pinset_body = {
        "schema": PINSET_SCHEMA,
        "status": "PASS_DISPOSABLE_VERIFIER_RESUME_PINSET__ZERO_CREDIT",
        "prior_producer_fixture": {
            "control_dir": str(prior.relative_to(ROOT)),
            "receipt_file_sha256": args.expect_fixture_receipt_file_sha256,
            "receipt_object_sha256": args.expect_fixture_receipt_object_sha256,
            "candidate_dir": str(candidate.relative_to(ROOT)),
            "result_file_sha256": args.expect_result_file_sha256,
            "result_object_sha256": result["result_sha256"],
        },
        "actual_v2_authority": authority,
        "source_pins": {
            "independent_verifier": args.expect_verifier_sha256,
            "transaction_runner": args.expect_runner_sha256,
            "disposable_resume_helper": args.expect_helper_sha256,
            "python": args.expect_python_sha256,
        },
        "targets": {
            "control": str(control.relative_to(ROOT)),
            "verifier_output": str(output.relative_to(ROOT)),
            "verifier_run": str(run.relative_to(ROOT)),
        },
        "disposable_verifier_only": True,
        "run_attacks": False,
        "formal_credit": 0,
        "manifest_authorized": False,
        "C27R2": "UNAUTHORIZED_PENDING_RELEASE_CHAIN",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    pinset = dict(pinset_body)
    pinset["pinset_sha256"] = digest(pinset)
    pinset_path = control / "pinset.json"
    write_json(pinset_path, pinset)

    terminal = ROOT / authority["actual_terminal_dir"]
    base = ROOT / authority["actual_base_seal_dir"]
    verification_path = output / "verification.json"
    argv = [
        str(PYTHON), "-I", "-B", str(VERIFIER),
        "--terminal-dir", str(terminal),
        "--base-seal-dir", str(base),
        "--expect-terminal-root-sha256",
        authority["actual_terminal_root_sha256"],
        "--expect-terminal-receipt-file-sha256",
        authority["actual_terminal_receipt_file_sha256"],
        "--expect-terminal-receipt-object-sha256",
        authority["actual_terminal_receipt_object_sha256"],
        "--candidate-dir", str(candidate),
        "--out-file", str(verification_path),
    ]
    producer_run = ROOT / fixture["producer_run_dir"]
    input_paths = sorted(set(
        authority["authority_input_paths"]
        + [str((candidate / name).relative_to(ROOT)) for name in FILES]
        + [
            str(SELF.relative_to(ROOT)), str(VERIFIER.relative_to(ROOT)),
            str(RUNNER.relative_to(ROOT)), str(producer_path.relative_to(ROOT)),
            str(fixture_path.relative_to(ROOT)),
            str(prior_pinset_path.relative_to(ROOT)),
            str((prior / "preflight.json").relative_to(ROOT)),
            str((prior / "candidate_validation.json").relative_to(ROOT)),
            str((producer_run / "run_attestation.json").relative_to(ROOT)),
        ]
    ))
    spec_body = {
        "schema": COMMAND_SCHEMA,
        "stage": "independent_verifier",
        "source_path": str(VERIFIER),
        "source_sha256": args.expect_verifier_sha256,
        "argv": argv,
        "environment": {
            "PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
            "PYTHONHASHSEED": "30662722",
        },
        "python_hash_seed": "30662722",
        "timeout_seconds": args.timeout_seconds,
        "expected_stdout_status": VERIFICATION_STATUS,
        "input_paths": input_paths,
        "output_roots": [{
            "path": str(output),
            "kind": "directory",
            "precondition": "EXISTING_EMPTY_DIRECTORY",
            "exact_inventory": ["verification.json"],
            "required_relative_files": ["verification.json"],
        }],
        "pinset_file_sha256": file_sha(pinset_path),
        "pinset_object_sha256": pinset["pinset_sha256"],
        "runner_source_sha256": args.expect_runner_sha256,
        "python_sha256": args.expect_python_sha256,
        "formal_credit": 0,
        "CM2": "NO-GO_FOR_CLAIM",
    }
    spec = dict(spec_body)
    spec["command_spec_sha256"] = digest(spec)
    spec_path = control / "verifier_command_spec.json"
    write_json(spec_path, spec)

    completed = subprocess.run(
        [
            str(PYTHON), "-I", "-B", str(RUNNER),
            "--stage", "independent_verifier",
            "--command-spec", str(spec_path),
            "--pinset", str(pinset_path),
            "--run-dir", str(run),
            "--expect-runner-sha256", args.expect_runner_sha256,
            "--expect-python-sha256", args.expect_python_sha256,
        ],
        cwd=ROOT,
        env={"PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
             "PYTHONHASHSEED": "30662724"},
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    write_once(control / "runner.stdout.log", completed.stdout)
    write_once(control / "runner.stderr.log", completed.stderr)
    write_once(control / "runner.exit_code.txt",
               (str(completed.returncode) + "\n").encode("ascii"))
    need(completed.returncode == 0 and completed.stderr == b"",
         "verifier runner clean PASS")
    runner_stdout = strict_load(completed.stdout[:-1])
    need(completed.stdout.endswith(b"\n")
         and canonical(runner_stdout) == completed.stdout[:-1]
         and runner_stdout == {
             "CM2": "NO-GO_FOR_CLAIM", "formal_credit": 0,
             "stage": "independent_verifier", "status": RUN_STATUS,
         }, "runner exact stdout")

    run_attestation_path = run / "run_attestation.json"
    run_attestation = document(
        run_attestation_path, "run_attestation_sha256")
    need(run_attestation.get("schema") == RUN_SCHEMA
         and run_attestation.get("status") == RUN_STATUS
         and run_attestation.get("numeric_exit_code") == 0
         and run_attestation.get("signal") is None
         and run_attestation.get("timed_out") is False
         and run_attestation.get("stderr_empty") is True
         and run_attestation.get("input_pre_post_sha_stat_identical") is True,
         "runner verifier attestation")
    verification = document(verification_path, "verification_sha256")
    projection = verification.get("mathematical_projection")
    need(verification.get("schema") == VERIFICATION_SCHEMA
         and verification.get("status") == VERIFICATION_STATUS
         and verification.get("producer_imported_or_executed") is False
         and verification.get("actual_v2_seed_used") == "seed2"
         and verification.get("candidate_result_file_sha256")
             == args.expect_result_file_sha256
         and verification.get("candidate_result_object_sha256")
             == result["result_sha256"]
         and type(projection) is dict
         and all(projection.get(key) == value
                 for key, value in EXPECTED_PROJECTION.items())
         and verification.get("formal_credit") == 0
         and verification.get("manifest_authorized") is False
         and verification.get("CM2") == "NO-GO_FOR_CLAIM",
         "no-import seed2 exact full-ledger verification PASS")

    body = {
        "schema": (
            "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild."
            "v2.disposable-verifier-resume-receipt.v1"
        ),
        "status": (
            "PASS_SAME_DISPOSABLE_SEED1_FOUR_FILE_CANDIDATE_SEED2_NO_IMPORT_"
            "FULL_LEDGER_VERIFIER_PROCESS_TRANSACTION__ZERO_CREDIT"
        ),
        "prior_fixture_receipt_file_sha256":
            args.expect_fixture_receipt_file_sha256,
        "prior_fixture_receipt_object_sha256":
            args.expect_fixture_receipt_object_sha256,
        "candidate_result_file_sha256": args.expect_result_file_sha256,
        "candidate_result_object_sha256": result["result_sha256"],
        "verification_file_sha256": file_sha(verification_path),
        "verification_object_sha256": verification["verification_sha256"],
        "run_attestation_file_sha256": file_sha(run_attestation_path),
        "run_attestation_object_sha256":
            run_attestation["run_attestation_sha256"],
        "mathematical_projection": projection,
        "numeric_exit_code": 0,
        "signal": None,
        "stderr_empty": True,
        "input_pre_post_sha_stat_identical": True,
        "attacks_run": False,
        "service_created_or_started": False,
        "formal_credit": 0,
        "manifest_authorized": False,
        "C27R2": "UNAUTHORIZED_PENDING_ATTACKS_AND_RELEASE_CHAIN",
        "C28_C29": "UNAUTHORIZED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    receipt = dict(body)
    receipt["resume_receipt_sha256"] = digest(receipt)
    write_json(control / "resume_receipt.json", receipt)
    write_once(
        control / "PASS.lock",
        b"PASS_DISPOSABLE_C27R2_AUTHORITY_V2_V4_SEED2_VERIFIER__ZERO_CREDIT\n",
    )
    return receipt


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--prior-control-dir", required=True)
    value.add_argument("--candidate-dir", required=True)
    value.add_argument("--control-dir", required=True)
    value.add_argument("--verifier-output-dir", required=True)
    value.add_argument("--verifier-run-dir", required=True)
    value.add_argument("--expect-fixture-receipt-file-sha256", required=True)
    value.add_argument("--expect-fixture-receipt-object-sha256", required=True)
    value.add_argument("--expect-result-file-sha256", required=True)
    value.add_argument("--expect-verifier-sha256", required=True)
    value.add_argument("--expect-runner-sha256", required=True)
    value.add_argument("--expect-helper-sha256", required=True)
    value.add_argument("--expect-python-sha256", required=True)
    value.add_argument("--timeout-seconds", type=int, default=10_800)
    return value


def main() -> int:
    args = parser().parse_args()
    try:
        need(60 <= args.timeout_seconds <= 86_400, "bounded timeout")
        receipt = execute(args)
        sys.stdout.buffer.write(canonical({
            "CM2": "NO-GO_FOR_CLAIM", "formal_credit": 0,
            "status": receipt["status"],
        }) + b"\n")
        return 0
    except (Failure, OSError, ValueError, KeyError, TypeError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
