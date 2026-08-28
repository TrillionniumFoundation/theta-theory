#!/usr/bin/env python3
"""Run only the missing 21-attack stage from the immutable failed v4 r1 core.

This helper is deliberately disposable.  It proves that the canonicalized
attack output contract accepted by the frozen transaction runner really runs
the frozen v4 attack harness.  It binds the one named failed systemd
invocation, the already successful producer and verifier transactions, their
four-file candidate, and the exact pre-child failure.  It never edits or
resumes r1, never starts a service, and never creates a seal or formal credit.
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
PYTHON = Path("/usr/bin/python3.12")
UNIT = "cm2-c27r2-source-g-authority-v2-v4-formal-r1-20260808T182500.service"
INVOCATION_ID = "fa892c0c9b034c0a9dee6d41d0b4baea"
STEM = "c27r2-source-g-authority-v2-v4-formal-r1-20260808T182500"
AUDIT = ROOT / ".cm2-runtime/audit"
CONTROL = AUDIT / (STEM + "-control")
CANDIDATE = AUDIT / (STEM + "-candidate")
PRODUCER_RUN = AUDIT / (STEM + "-producer-run")
VERIFIER_OUTPUT = AUDIT / (STEM + "-verifier-output")
VERIFIER_RUN = AUDIT / (STEM + "-verifier-run")
FAILED_ATTACK_WORK = AUDIT / (STEM + "-attack-work")
FAILED_ATTACK_RUN = AUDIT / (STEM + "-attack-run")
PRODUCER = ROOT / (
    "deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_quotient_"
    "rebuild_v2_producer_v4.py"
)
VERIFIER = ROOT / (
    "deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_quotient_"
    "rebuild_v2_independent_verifier_v4.py"
)
ATTACKS = ROOT / (
    "deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_quotient_"
    "rebuild_v2_coherent_attack_harness_v4.py"
)
RUNNER = ROOT / (
    "deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_quotient_"
    "rebuild_v2_transaction_runner_v4.py"
)
WATCHER_V4 = ROOT / (
    "deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_quotient_"
    "rebuild_v2_gated_dual_seed_watcher_v4.py"
)
WATCHER_V6 = ROOT / (
    "deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_quotient_"
    "rebuild_v2_gated_dual_seed_watcher_v6.py"
)

SOURCE_PINS = {
    "producer": "578d0ce0d39d14dede9d9528be383abb3d4140c26bcac75917fe860a98bb158b",
    "independent_verifier": "acc66bbff3717e16bf56b15f9498070d97a4be1b0cd9253a79b7cae598b4082f",
    "coherent_attack_harness": "1d501ca968853712743524e7aba16d29dadd62b9d46458b53e0421aef2072007",
    "transaction_runner": "7ce75edac7e1aad904718e173cf6ed178f6d2631ba1f5cb4253bcf2c1e121d63",
    "gated_watcher_v4": "80baa6e3a851b60bad387619572c1a1d7dafa460a3c87ea6ad9d7f48c31d6610",
    "python": "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118",
}
UPSTREAM_FILE_PINS = {
    "pinset.json": "cb8934bf7d24f39d5834c3364110c81cc020158a2b396cc6c16672e1e2ab3323",
    "preflight.json": "9053366a44c8de64ea866ad3008412f84639f4ed42a4ecf07848c195df22993c",
    "candidate_validation.json": "5fc41255848070717fe917fb07ca607941012a02fb180fc565c6f1acf5208a31",
    "dual_seed_descriptor_agreement.json": "ae6f57654621459195ca1d66dd7e7a83b3f80f3fbcc961c8f5a145394e62947b",
    "failure_receipt.json": "280cb416238d49fdd160af61e384b2c2e4da4ace7403bb4ec1c0516d6e19bd5a",
    "attack_command_spec.json": "170653ca5076d7615ab07a22d486ae044423783ff094a9977e4da7eae21e291f",
    "result.json": "8d2401172fedd058e3287f29de8e07069dd2a4c5b23ae7f4d7b18bc3a31bd667",
    "verification.json": "3cbe81b70393715eb0f5734a9b9ff6578c2c2da62c8cb6b610ec00fc531261c4",
    "producer_run_attestation.json": "2de15defc484cc79ef359b01d3dcf770d52744e45dff14592a00734b2899f0b4",
    "verifier_run_attestation.json": "5d9df46b67585d7f400cc74944d0fcb4c1d5d87a9e4326d251cbc121a6699a2a",
}
OBJECT_PINS = {
    "prior_pinset": "c5b7fef31f3c35a7bb300135a1829f5fb13bd6db7f287f2accde5e5d980e09a3",
    "failure": "000d8c9bd8db9d8aec7808c842093f18dbeb520a3c9ed9a06972cb039efd5c59",
    "result": "70afe7c796348a657c58feffa227f6cfd9f7b1714e5a3c0c0ae5baa5d2c51fed",
    "verification": "b8dd5a966d790af5e77c967280fba66bf7c7280114f3ff61fd0d73a209313179",
    "producer_run": "3ba07e611bfb8d8a9074e79a7142b00e7fa63ad72dd3674da5dd4309d7cdb31e",
    "verifier_run": "f211e8fa4b2135450c838566e3052040710a769a64fa576a4ecfeb0a3d9ee29d",
}
PINSET_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "gated-transaction-pinset.v4"
)
SPEC_SCHEMA = (
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
ATTACK_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "coherent-attack-harness.v1"
)
ATTACK_STATUS = (
    "PASS_BASELINE_AND_21_OF_21_COHERENT_ATTACKS_REJECTED_FAIL_CLOSED__"
    "ZERO_CREDIT_PENDING_RELEASE_CHAIN"
)
FILES = [
    "member_to_post_component.jsonl.gz",
    "old_c15_component_to_post_component.jsonl.gz",
    "post_component_census.jsonl.gz",
    "result.json",
]
CONTROL_FILES = {
    "FAILED.lock", "attack_command_spec.json", "candidate_validation.json",
    "coherent_attacks_runner.exit_code.txt",
    "coherent_attacks_runner.stderr.log",
    "coherent_attacks_runner.stdout.log",
    "dual_seed_descriptor_agreement.json", "failure_receipt.json",
    "independent_verifier_runner.exit_code.txt",
    "independent_verifier_runner.stderr.log",
    "independent_verifier_runner.stdout.log", "pinset.json", "preflight.json",
    "producer_command_spec.json", "producer_runner.exit_code.txt",
    "producer_runner.stderr.log", "producer_runner.stdout.log",
    "verifier_command_spec.json",
}
RUN_FILES = {
    "PASS.lock", "exit_code.txt", "input_post.json", "input_pre.json",
    "output_validation.json", "run_attestation.json", "runner_start.json",
    "signal.json", "stderr.log", "stdout.log", "timing.json",
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
                      parse_constant=lambda value: (_ for _ in ()).throw(
                          ValueError(value)))


def inside(raw: str | Path, *, absent: bool = False) -> Path:
    value = Path(raw)
    path = (ROOT / value if not value.is_absolute() else value).absolute()
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
             "regular single-link:" + str(path))
        state = hashlib.sha256()
        while block := os.read(descriptor, 4 << 20):
            state.update(block)
        after = os.fstat(descriptor)
        need(fingerprint(before) == fingerprint(after),
             "stable SHA/stat:" + str(path))
        return state.hexdigest()
    finally:
        os.close(descriptor)


def document(path: Path, closure: str | None = None) -> dict[str, Any]:
    payload = path.read_bytes()
    need(payload.endswith(b"\n"), "JSON newline:" + str(path))
    value = strict_load(payload[:-1])
    need(type(value) is dict and canonical(value) == payload[:-1],
         "canonical JSON:" + str(path))
    if closure is not None:
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


def exact_files(directory: Path, expected: set[str], label: str) -> None:
    need(directory.is_dir() and not directory.is_symlink(),
         "real directory:" + label)
    need({entry.name for entry in directory.iterdir()} == expected
         and all(entry.is_file() and not entry.is_symlink()
                 for entry in directory.iterdir()), "exact files:" + label)


def service_failure_boundary() -> None:
    completed = subprocess.run(
        ["/usr/bin/systemctl", "--user", "show", UNIT,
         "-p", "ActiveState", "-p", "SubState", "-p", "Result",
         "-p", "ExecMainCode", "-p", "ExecMainStatus", "-p", "InvocationID"],
        cwd=ROOT, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    need(completed.returncode == 0 and completed.stderr == b"",
         "read exact failed unit")
    fields = dict(line.split("=", 1) for line in
                  completed.stdout.decode("ascii").splitlines() if "=" in line)
    need(fields == {
        "ActiveState": "failed", "SubState": "failed", "Result": "exit-code",
        "ExecMainCode": "1", "ExecMainStatus": "2",
        "InvocationID": INVOCATION_ID,
    }, "exact immutable v4 r1 failed invocation")


def validate_run(directory: Path, stage: str, file_pin: str,
                 object_pin: str) -> dict[str, Any]:
    exact_files(directory, RUN_FILES, stage + " run")
    need((directory / "exit_code.txt").read_bytes() == b"0\n"
         and (directory / "signal.json").read_bytes() == b"null\n"
         and (directory / "stderr.log").read_bytes() == b"",
         stage + " process closure")
    pass_bytes = ("PASS_C27R2_AUTHORITY_V2_" + stage.upper()
                  + "_PROCESS_TRANSACTION__ZERO_CREDIT\n").encode("ascii")
    need((directory / "PASS.lock").read_bytes() == pass_bytes,
         stage + " exact PASS lock")
    path = directory / "run_attestation.json"
    value = document(path, "run_attestation_sha256")
    need(file_sha(path) == file_pin
         and value["run_attestation_sha256"] == object_pin
         and value.get("schema") == RUN_SCHEMA
         and value.get("status") == RUN_STATUS
         and value.get("stage") == stage
         and value.get("numeric_exit_code") == 0
         and value.get("signal") is None
         and value.get("timed_out") is False
         and value.get("stderr_empty") is True
         and value.get("input_pre_post_sha_stat_identical") is True
         and value.get("formal_credit") == 0
         and value.get("manifest_authorized") is False,
         stage + " exact attestation")
    return value


def validate_upstream(expect_v6_sha: str) -> tuple[dict[str, Any], dict[str, Any]]:
    service_failure_boundary()
    exact_files(CONTROL, CONTROL_FILES, "v4 r1 control")
    exact_files(CANDIDATE, set(FILES), "v4 r1 candidate")
    exact_files(VERIFIER_OUTPUT, {"verification.json"}, "v4 r1 verifier output")
    need(not FAILED_ATTACK_WORK.exists() and not FAILED_ATTACK_RUN.exists(),
         "attack child output/run never created")
    need((CONTROL / "FAILED.lock").read_bytes()
         == b"FAILED_CLOSED_C27R2_AUTHORITY_V2_GATED_TRANSACTION\n"
         and not (CONTROL / "PASS.lock").exists(),
         "v4 r1 failed-only control state")
    need((CONTROL / "producer_runner.exit_code.txt").read_bytes() == b"0\n"
         and (CONTROL / "producer_runner.stderr.log").read_bytes() == b""
         and (CONTROL / "independent_verifier_runner.exit_code.txt").read_bytes()
             == b"0\n"
         and (CONTROL / "independent_verifier_runner.stderr.log").read_bytes()
             == b""
         and (CONTROL / "coherent_attacks_runner.exit_code.txt").read_bytes()
             == b"2\n"
         and (CONTROL / "coherent_attacks_runner.stdout.log").read_bytes() == b""
         and (CONTROL / "coherent_attacks_runner.stderr.log").read_bytes()
             == b"REJECT:output required inventory:0\n",
         "exact producer/verifier PASS then pre-child attack-spec rejection")
    paths = {
        **{name: CONTROL / name for name in UPSTREAM_FILE_PINS
           if name not in {"result.json", "verification.json",
                           "producer_run_attestation.json",
                           "verifier_run_attestation.json"}},
        "result.json": CANDIDATE / "result.json",
        "verification.json": VERIFIER_OUTPUT / "verification.json",
        "producer_run_attestation.json": PRODUCER_RUN / "run_attestation.json",
        "verifier_run_attestation.json": VERIFIER_RUN / "run_attestation.json",
    }
    need(all(file_sha(paths[name]) == expected
             for name, expected in UPSTREAM_FILE_PINS.items()),
         "all immutable v4 r1 file pins")
    source_paths = {
        "producer": PRODUCER, "independent_verifier": VERIFIER,
        "coherent_attack_harness": ATTACKS, "transaction_runner": RUNNER,
        "gated_watcher_v4": WATCHER_V4, "python": PYTHON,
    }
    need(all(file_sha(source_paths[name]) == expected
             for name, expected in SOURCE_PINS.items()),
         "all frozen v4 source/Python pins")
    need(valid_sha(expect_v6_sha) and file_sha(WATCHER_V6) == expect_v6_sha,
         "append-only v6 watcher pin")
    prior_pinset = document(CONTROL / "pinset.json", "pinset_sha256")
    need(prior_pinset.get("schema") == PINSET_SCHEMA
         and prior_pinset["pinset_sha256"] == OBJECT_PINS["prior_pinset"]
         and prior_pinset.get("source_pins") == {
             "producer": SOURCE_PINS["producer"],
             "independent_verifier": SOURCE_PINS["independent_verifier"],
             "coherent_attack_harness": SOURCE_PINS["coherent_attack_harness"],
             "transaction_runner": SOURCE_PINS["transaction_runner"],
             "gated_watcher": SOURCE_PINS["gated_watcher_v4"],
             "python": SOURCE_PINS["python"],
         } and prior_pinset.get("run_attacks") is True
         and prior_pinset.get("formal_credit") == 0,
         "prior v4 pinset exact source roles")
    authority = prior_pinset.get("actual_v2_authority")
    need(type(authority) is dict
         and type(authority.get("authority_input_paths")) is list
         and authority["authority_input_paths"]
             == sorted(set(authority["authority_input_paths"])),
         "prior actual-v2 authority inventory")
    bad_spec = document(CONTROL / "attack_command_spec.json",
                        "command_spec_sha256")
    output_roots = bad_spec.get("output_roots")
    need(bad_spec.get("schema") == SPEC_SCHEMA
         and bad_spec.get("stage") == "coherent_attacks"
         and bad_spec.get("source_sha256")
             == SOURCE_PINS["coherent_attack_harness"]
         and type(output_roots) is list and len(output_roots) == 1
         and output_roots[0].get("required_relative_files") == [
             "coherent_attacks.json", "baseline_verification.json"]
         and output_roots[0].get("exact_inventory") is None,
         "original failure isolated to noncanonical required inventory")
    failure = document(CONTROL / "failure_receipt.json",
                       "failure_receipt_sha256")
    need(failure["failure_receipt_sha256"] == OBJECT_PINS["failure"]
         and failure.get("stage") == "coherent_attacks_after_dual_seed_pass"
         and failure.get("error")
             == "Failure:coherent_attacks transaction runner clean exit"
         and failure.get("formal_credit") == 0
         and failure.get("C27R2") == "UNAUTHORIZED",
         "truthful v4 r1 failure receipt")
    result = document(CANDIDATE / "result.json", "result_sha256")
    verification = document(VERIFIER_OUTPUT / "verification.json",
                            "verification_sha256")
    need(result["result_sha256"] == OBJECT_PINS["result"]
         and result.get("formal_credit") == 0
         and result.get("manifest_authorized") is False
         and verification["verification_sha256"] == OBJECT_PINS["verification"]
         and verification.get("candidate_result_object_sha256")
             == result["result_sha256"]
         and verification.get("producer_imported_or_executed") is False
         and verification.get("actual_v2_seed_used") == "seed2"
         and verification.get("formal_credit") == 0,
         "candidate and no-import verification exact PASS")
    validate_run(PRODUCER_RUN, "producer",
                 UPSTREAM_FILE_PINS["producer_run_attestation.json"],
                 OBJECT_PINS["producer_run"])
    validate_run(VERIFIER_RUN, "independent_verifier",
                 UPSTREAM_FILE_PINS["verifier_run_attestation.json"],
                 OBJECT_PINS["verifier_run"])
    return prior_pinset, result


def failure_receipt(control: Path, stage: str, error: BaseException) -> None:
    body = {
        "schema": "cm2.round306c27r2.source-g-authority-v2.disposable-attacks-resume-failure.v1",
        "status": "FAILED_CLOSED_DISPOSABLE_ATTACKS_RESUME__ZERO_CREDIT",
        "stage": stage, "failed_at_utc": utc_now(),
        "error": f"{type(error).__name__}:{error}",
        "formal_credit": 0, "manifest_authorized": False,
        "C27R2": "UNAUTHORIZED", "C28_C29": "UNAUTHORIZED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    value = {**body, "failure_receipt_sha256": digest(body)}
    if not (control / "failure_receipt.json").exists():
        write_json(control / "failure_receipt.json", value)
    if not (control / "FAILED.lock").exists():
        write_once(control / "FAILED.lock",
                   b"FAILED_CLOSED_DISPOSABLE_C27R2_V4_ATTACKS_RESUME\n")


def execute(args: argparse.Namespace) -> dict[str, Any]:
    pins = (args.expect_helper_sha256, args.expect_watcher_v6_sha256)
    need(all(valid_sha(value) for value in pins), "helper/v6 SHA pins")
    need(file_sha(SELF) == args.expect_helper_sha256, "helper self pin")
    prior_pinset, result = validate_upstream(args.expect_watcher_v6_sha256)
    control = inside(args.control_dir, absent=True)
    work = inside(args.attack_work_dir, absent=True)
    run = inside(args.attack_run_dir, absent=True)
    need(len({control, work, run}) == 3
         and all(path.parent == AUDIT for path in (control, work, run))
         and all(not path.exists() for path in (control, work, run)),
         "fresh distinct disposable attack paths")
    if args.preflight_only:
        return {
            "schema": "cm2.round306c27r2.source-g-authority-v2.disposable-attacks-resume-preflight.v1",
            "status": "PASS_EXACT_R1_FAILURE_AND_FRESH_ATTACK_RESUME_PREFLIGHT__NO_PATHS_CREATED_ZERO_CREDIT",
            "unit": UNIT, "invocation_id": INVOCATION_ID,
            "v6_watcher_sha256": args.expect_watcher_v6_sha256,
            "formal_credit": 0, "manifest_authorized": False,
            "C27R2": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM",
        }
    stage = "create_disposable_control"
    try:
        control.mkdir(mode=0o700)
        authority = prior_pinset["actual_v2_authority"]
        pinset_body = {
            "schema": PINSET_SCHEMA,
            "status": "PASS_DISPOSABLE_ATTACKS_RESUME_FROM_EXACT_FAILED_V4_R1__ZERO_CREDIT",
            "prior_failed_unit": UNIT, "prior_invocation_id": INVOCATION_ID,
            "prior_pinset_file_sha256": UPSTREAM_FILE_PINS["pinset.json"],
            "prior_pinset_object_sha256": OBJECT_PINS["prior_pinset"],
            "candidate_result_file_sha256": UPSTREAM_FILE_PINS["result.json"],
            "candidate_result_object_sha256": OBJECT_PINS["result"],
            "verification_file_sha256": UPSTREAM_FILE_PINS["verification.json"],
            "verification_object_sha256": OBJECT_PINS["verification"],
            "actual_v2_authority": authority,
            "source_pins": {
                **SOURCE_PINS,
                "disposable_attacks_resume_helper": args.expect_helper_sha256,
                "gated_watcher_v6": args.expect_watcher_v6_sha256,
            },
            "targets": {"control": str(control.relative_to(ROOT)),
                        "attack_work": str(work.relative_to(ROOT)),
                        "attack_run": str(run.relative_to(ROOT))},
            "disposable_attacks_resume_only": True,
            "service_created_or_started": False,
            "formal_credit": 0, "manifest_authorized": False,
            "C27R2": "UNAUTHORIZED_PENDING_FRESH_FORMAL_CORE_AND_RELEASE_CHAIN",
            "C28_C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM",
        }
        pinset = {**pinset_body, "pinset_sha256": digest(pinset_body)}
        pinset_path = control / "pinset.json"
        write_json(pinset_path, pinset)
        terminal = ROOT / authority["actual_terminal_dir"]
        base = ROOT / authority["actual_base_seal_dir"]
        result_path = work / "coherent_attacks.json"
        argv = [
            str(PYTHON), "-I", "-B", str(ATTACKS),
            "--terminal-dir", str(terminal),
            "--base-seal-dir", str(base),
            "--expect-terminal-root-sha256",
            authority["actual_terminal_root_sha256"],
            "--expect-terminal-receipt-file-sha256",
            authority["actual_terminal_receipt_file_sha256"],
            "--expect-terminal-receipt-object-sha256",
            authority["actual_terminal_receipt_object_sha256"],
            "--candidate-dir", str(CANDIDATE), "--work-dir", str(work),
            "--out-file", str(result_path),
            "--expect-verifier-sha256", SOURCE_PINS["independent_verifier"],
            "--expect-python-sha256", SOURCE_PINS["python"],
            "--expect-harness-sha256", SOURCE_PINS["coherent_attack_harness"],
        ]
        control_inputs = [
            "pinset.json", "preflight.json", "candidate_validation.json",
            "dual_seed_descriptor_agreement.json", "failure_receipt.json",
            "attack_command_spec.json", "FAILED.lock",
            "producer_runner.exit_code.txt", "producer_runner.stderr.log",
            "producer_runner.stdout.log",
            "independent_verifier_runner.exit_code.txt",
            "independent_verifier_runner.stderr.log",
            "independent_verifier_runner.stdout.log",
            "coherent_attacks_runner.exit_code.txt",
            "coherent_attacks_runner.stderr.log",
            "coherent_attacks_runner.stdout.log",
        ]
        run_inputs = [
            str((directory / name).relative_to(ROOT))
            for directory in (PRODUCER_RUN, VERIFIER_RUN)
            for name in sorted(RUN_FILES)
        ]
        input_paths = sorted(set(
            authority["authority_input_paths"]
            + [str((CANDIDATE / name).relative_to(ROOT)) for name in FILES]
            + [str((VERIFIER_OUTPUT / "verification.json").relative_to(ROOT))]
            + [str((CONTROL / name).relative_to(ROOT)) for name in control_inputs]
            + run_inputs
            + [str(path.relative_to(ROOT)) for path in
               (SELF, PRODUCER, VERIFIER, ATTACKS, RUNNER, WATCHER_V4,
                WATCHER_V6)]
        ))
        spec_body = {
            "schema": SPEC_SCHEMA, "stage": "coherent_attacks",
            "source_path": str(ATTACKS),
            "source_sha256": SOURCE_PINS["coherent_attack_harness"],
            "argv": argv,
            "environment": {"PATH": "/usr/bin:/bin", "LANG": "C",
                            "LC_ALL": "C", "PYTHONHASHSEED": "30662725"},
            "python_hash_seed": "30662725",
            "timeout_seconds": args.timeout_seconds,
            "expected_stdout_status": ATTACK_STATUS,
            "input_paths": input_paths,
            "output_roots": [{
                "path": str(work), "kind": "directory",
                "precondition": "ABSENT", "exact_inventory": None,
                "required_relative_files": [
                    "baseline_verification.json", "coherent_attacks.json"],
            }],
            "pinset_file_sha256": file_sha(pinset_path),
            "pinset_object_sha256": pinset["pinset_sha256"],
            "runner_source_sha256": SOURCE_PINS["transaction_runner"],
            "python_sha256": SOURCE_PINS["python"],
            "formal_credit": 0, "CM2": "NO-GO_FOR_CLAIM",
        }
        spec = {**spec_body, "command_spec_sha256": digest(spec_body)}
        spec_path = control / "attack_command_spec.json"
        write_json(spec_path, spec)
        stage = "run_21_attacks"
        completed = subprocess.run(
            [str(PYTHON), "-I", "-B", str(RUNNER),
             "--stage", "coherent_attacks", "--command-spec", str(spec_path),
             "--pinset", str(pinset_path), "--run-dir", str(run),
             "--expect-runner-sha256", SOURCE_PINS["transaction_runner"],
             "--expect-python-sha256", SOURCE_PINS["python"]],
            cwd=ROOT, env={"PATH": "/usr/bin:/bin", "LANG": "C",
                           "LC_ALL": "C", "PYTHONHASHSEED": "30662726"},
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, check=False,
        )
        write_once(control / "runner.stdout.log", completed.stdout)
        write_once(control / "runner.stderr.log", completed.stderr)
        write_once(control / "runner.exit_code.txt",
                   (str(completed.returncode) + "\n").encode("ascii"))
        need(completed.returncode == 0 and completed.stderr == b"",
             "disposable attack runner clean PASS")
        expected_stdout = canonical({
            "CM2": "NO-GO_FOR_CLAIM", "formal_credit": 0,
            "stage": "coherent_attacks", "status": RUN_STATUS,
        }) + b"\n"
        need(completed.stdout == expected_stdout, "runner exact stdout")
        run_attestation_path = run / "run_attestation.json"
        run_attestation = document(run_attestation_path,
                                   "run_attestation_sha256")
        need(run_attestation.get("schema") == RUN_SCHEMA
             and run_attestation.get("status") == RUN_STATUS
             and run_attestation.get("stage") == "coherent_attacks"
             and run_attestation.get("numeric_exit_code") == 0
             and run_attestation.get("signal") is None
             and run_attestation.get("timed_out") is False
             and run_attestation.get("stderr_empty") is True
             and run_attestation.get("input_pre_post_sha_stat_identical") is True,
             "disposable attack process attestation")
        attacks = document(result_path, "attack_harness_sha256")
        need(attacks.get("schema") == ATTACK_SCHEMA
             and attacks.get("status") == ATTACK_STATUS
             and attacks.get("attack_count") == 21
             and attacks.get("rejected") == 21
             and attacks.get("accepted") == 0
             and attacks.get("authoritative_candidate_pre_post_sha256_identical")
                 is True
             and attacks.get("formal_credit") == 0
             and attacks.get("manifest_authorized") is False
             and attacks.get("C27R2") == "UNAUTHORIZED_PENDING_RELEASE_CHAIN",
             "21/21 disposable attacks exact PASS")
        body = {
            "schema": "cm2.round306c27r2.source-g-authority-v2.disposable-attacks-resume-receipt.v1",
            "status": "PASS_EXACT_FAILED_V4_R1_CANDIDATE_AND_VERIFICATION_THROUGH_21_OF_21_DISPOSABLE_ATTACKS__ZERO_CREDIT",
            "completed_at_utc": utc_now(), "prior_unit": UNIT,
            "prior_invocation_id": INVOCATION_ID,
            "prior_failure_receipt_file_sha256":
                UPSTREAM_FILE_PINS["failure_receipt.json"],
            "prior_failure_receipt_object_sha256": OBJECT_PINS["failure"],
            "candidate_result_file_sha256": UPSTREAM_FILE_PINS["result.json"],
            "candidate_result_object_sha256": result["result_sha256"],
            "verification_file_sha256": UPSTREAM_FILE_PINS["verification.json"],
            "verification_object_sha256": OBJECT_PINS["verification"],
            "attack_result_file_sha256": file_sha(result_path),
            "attack_result_object_sha256": attacks["attack_harness_sha256"],
            "run_attestation_file_sha256": file_sha(run_attestation_path),
            "run_attestation_object_sha256":
                run_attestation["run_attestation_sha256"],
            "required_relative_files_canonical_order": [
                "baseline_verification.json", "coherent_attacks.json"],
            "attack_count": 21, "rejected": 21, "accepted": 0,
            "numeric_exit_code": 0, "signal": None, "stderr_empty": True,
            "input_pre_post_sha_stat_identical": True,
            "disposable_only_not_formal_predecessor": True,
            "service_created_or_started": False,
            "seal_or_terminal_created": False,
            "formal_credit": 0, "manifest_authorized": False,
            "C27R2": "UNAUTHORIZED_PENDING_FRESH_FORMAL_CORE_AND_RELEASE_CHAIN",
            "C28_C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM",
        }
        receipt = {**body, "resume_receipt_sha256": digest(body)}
        write_json(control / "resume_receipt.json", receipt)
        write_once(control / "PASS.lock",
                   b"PASS_DISPOSABLE_C27R2_V4_R1_21_ATTACKS_RESUME__ZERO_CREDIT\n")
        return receipt
    except BaseException as error:
        if control.exists():
            failure_receipt(control, stage, error)
        raise


def self_test() -> dict[str, Any]:
    sample = {"b": 2, "a": 1}
    need(canonical(sample) == b'{"a":1,"b":2}'
         and digest(sample) == hashlib.sha256(canonical(sample)).hexdigest(),
         "canonical/closure fixture")
    required = sorted(set([
        "coherent_attacks.json", "baseline_verification.json"]))
    need(required == ["baseline_verification.json", "coherent_attacks.json"],
         "runner inventory ordering fixture")
    return {
        "schema": "cm2.round306c27r2.source-g-authority-v2.disposable-attacks-resume-self-test.v1",
        "status": "PASS_CANONICAL_CLOSURE_AND_OUTPUT_INVENTORY_FIXTURES",
        "formal_credit": 0, "C27R2": "UNAUTHORIZED",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--self-test", action="store_true")
    value.add_argument("--preflight-only", action="store_true")
    value.add_argument("--control-dir")
    value.add_argument("--attack-work-dir")
    value.add_argument("--attack-run-dir")
    value.add_argument("--expect-helper-sha256")
    value.add_argument("--expect-watcher-v6-sha256")
    value.add_argument("--timeout-seconds", type=int, default=43_200)
    return value


def main() -> int:
    args = parser().parse_args()
    run_fields = ("control_dir", "attack_work_dir", "attack_run_dir",
                  "expect_helper_sha256", "expect_watcher_v6_sha256")
    try:
        if args.self_test:
            need(not args.preflight_only
                 and all(getattr(args, name) is None for name in run_fields),
                 "self-test accepts no run arguments")
            result = self_test()
        else:
            need(all(getattr(args, name) is not None for name in run_fields)
                 and 60 <= args.timeout_seconds <= 86_400,
                 "all run arguments and bounded timeout")
            result = execute(args)
        sys.stdout.buffer.write(canonical({
            "CM2": "NO-GO_FOR_CLAIM", "formal_credit": 0,
            "status": result["status"],
        }) + b"\n")
        return 0
    except (Failure, OSError, ValueError, KeyError, TypeError,
            subprocess.SubprocessError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
