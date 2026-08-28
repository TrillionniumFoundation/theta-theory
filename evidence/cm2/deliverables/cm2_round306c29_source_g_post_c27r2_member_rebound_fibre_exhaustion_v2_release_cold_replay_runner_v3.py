#!/usr/bin/env python3
"""Run a fresh no-import cold replay of a successful C29-v2 core."""

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
PYTHON = (ROOT / ".cm2-runtime/audit/c30a-p0-closure-verifier-20260807/"
          "fresh-python-flint-0.9.0/bin/python")
PREFIX = "cm2_round306c29_source_g_post_c27r2_member_rebound_fibre_exhaustion_v2"
VERIFIER = ROOT / f"deliverables/{PREFIX}_independent_verifier_contract_v4.py"
RUNNER = ROOT / f"deliverables/{PREFIX}_transaction_runner_v3.py"
VERIFIER_SHA = "998badc7dad864d5e1c59c24b2c4a397ef08470c6e3bcbbf82c581a815692d1a"
RUNNER_SHA = "bdd5e08e4d9a826bf09807a555fe6bb1ad0cd8556f35c828ba5b20d9bff48da5"
PYTHON_SHA = "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118"
CORE_SOURCES = {
    "builder": ROOT / f"deliverables/{PREFIX}_terminal_consumer_adapter_builder_v3.py",
    "adapter_verifier": ROOT / f"deliverables/{PREFIX}_terminal_consumer_adapter_independent_verifier_v1.py",
    "runner": RUNNER,
    "producer": ROOT / f"deliverables/{PREFIX}_producer_contract_v4.py",
    "verifier": VERIFIER,
    "attacks": ROOT / f"deliverables/{PREFIX}_coherent_attack_harness_contract_v5.py",
    "python": PYTHON,
    "watcher": ROOT / f"deliverables/{PREFIX}_gated_dual_terminal_seed_watcher_v7.py",
}
CORE_SOURCE_PINS = {
    "builder": "8381091ff952c6cc3673efe5789fda3773f55e4c9f990c124e567811d215538e",
    "adapter_verifier": "eccc4422a3ebba0ce505f4802bb508c3da007ae099a2b6f8f21b1347be5b3201",
    "runner": RUNNER_SHA,
    "producer": "711ff12ea95b7a7376c8e02109ab66157431ea287a24c7c0824c948686109886",
    "verifier": VERIFIER_SHA,
    "attacks": "9a387a712033119c8aa615b5eaf544bf38778119eea18afa598b26cb351620f0",
    "python": PYTHON_SHA,
    "watcher": "6d3141ca0ab3f6e63b7c7a3af581b4537dd872cf860b7d6eb2e491d59ce68182",
}
CORE_STAGE_SEEDS = {
    "c27_adapter": "30662901", "c27_adapter_verifier": "30662902",
    "c28_adapter": "30662903", "c28_adapter_verifier": "30662904",
    "producer": "30662905", "independent_verifier": "30662906",
    "coherent_attacks": "30662907",
}
CORE_STAGE_SOURCE_PINS = {
    "c27_adapter": "builder", "c27_adapter_verifier": "adapter_verifier",
    "c28_adapter": "builder", "c28_adapter_verifier": "adapter_verifier",
    "producer": "producer", "independent_verifier": "verifier",
    "coherent_attacks": "attacks",
}
CORE_TARGET_KEYS = {
    "control", "c27_adapter", "c27_adapter_verification",
    "c28_adapter", "c28_adapter_verification", "candidate", "verification",
    "attack_work", "attacks", "run_c27_adapter", "run_c27_adapter_verifier",
    "run_c28_adapter", "run_c28_adapter_verifier", "run_producer",
    "run_independent_verifier", "run_coherent_attacks",
}
BASE = "cm2.round306c29.source-g-post-c27r2-member-rebound-fibre-exhaustion.v2."
CORE_SCHEMA = BASE + "gated-dual-terminal-seed-core-receipt.v1"
CORE_STATUS = "PASS_C29_V2_DUAL_TERMINAL_ADAPTERS_SEED1_PRODUCER_SEED2_NO_IMPORT_VERIFIER_AND_34_ATTACKS__ZERO_CREDIT_PENDING_RELEASE_TERMINAL"
PINSET_SCHEMA = BASE + "gated-transaction-pinset.v1"
SPEC_SCHEMA = BASE + "process-command-spec.v1"
RUN_SCHEMA = BASE + "process-run-attestation.v1"
RUN_STATUS = "PASS_C29_V2_PROCESS_TRANSACTION_EXIT0_NULL_SIGNAL_EMPTY_STDERR_PRE_POST_AND_OUTPUTS__ZERO_CREDIT"
VERIFY_STATUS = "PASS_NO_IMPORT_INDEPENDENT_C29_V2_FULL_RECONSTRUCTION__CONDITIONAL_ZERO_CREDIT_PENDING_ATTACKS_AND_RELEASE_TERMINAL"
COLD_SCHEMA = BASE + "release-cold-replay-receipt.v1"
COLD_STATUS = "PASS_C29_V2_FRESH_NO_IMPORT_COLD_BYTE_REPLAY_WITH_ALL_CORE_INPUT_PRE_POST_SHA_STAT__ZERO_CREDIT"


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
    return type(value) is str and len(value) == 64 and all(
        char in "0123456789abcdef" for char in value)


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace(
        "+00:00", "Z")


def strict(payload: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(key not in result, "duplicate JSON key")
            result[key] = value
        return result
    return json.loads(payload, object_pairs_hook=pairs,
                      parse_constant=lambda token: (_ for _ in ()).throw(
                          Failure("non-finite JSON:" + token)))


def fingerprint(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink,
            info.st_size, info.st_mtime_ns, info.st_ctime_ns,
            info.st_uid, info.st_gid)


def file_sha(path: Path) -> str:
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                 | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular singleton")
        state = hashlib.sha256()
        while block := os.read(fd, 4 << 20):
            state.update(block)
        need(fingerprint(os.fstat(fd)) == fingerprint(before), "stable hash")
        return state.hexdigest()
    finally:
        os.close(fd)


def document(path: Path, closure: str) -> dict[str, Any]:
    payload = path.read_bytes()
    need(payload.endswith(b"\n") and not payload.endswith(b"\n\n"),
         "JSON newline")
    value = strict(payload[:-1])
    need(type(value) is dict and canonical(value) == payload[:-1], "canonical JSON")
    body = dict(value)
    claim = body.pop(closure, None)
    need(valid_sha(claim) and claim == digest(body), "object closure")
    return value


def write_once(path: Path, payload: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                 | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        offset = 0
        while offset < len(payload):
            offset += os.write(fd, payload[offset:])
        os.fsync(fd)
    finally:
        os.close(fd)


def write_json(path: Path, value: Any) -> None:
    write_once(path, canonical(value) + b"\n")


def service_success(unit: str, invocation: str) -> None:
    need(type(unit) is str and unit.endswith(".service")
         and len(invocation) == 32, "unit/invocation syntax")
    completed = subprocess.run(["/usr/bin/systemctl", "--user", "show", unit,
        "-p", "ActiveState", "-p", "SubState", "-p", "Result",
        "-p", "ExecMainCode", "-p", "ExecMainStatus", "-p", "InvocationID"],
        cwd=ROOT, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False)
    need(completed.returncode == 0 and completed.stderr == b"", "systemd query")
    fields = dict(line.split("=", 1) for line in completed.stdout.decode().splitlines()
                  if "=" in line)
    need(fields.get("ActiveState") == "active" and fields.get("SubState") == "exited"
         and fields.get("Result") == "success"
         and fields.get("ExecMainCode") in {"1", "exited"}
         and fields.get("ExecMainStatus") == "0"
         and fields.get("InvocationID") == invocation, "core service clean success")


def recursive_files(path: Path) -> list[str]:
    if path.is_file():
        need(not path.is_symlink(), "core file symlink")
        return [str(path.relative_to(ROOT))]
    need(path.is_dir() and not path.is_symlink(), "core directory")
    result: list[str] = []
    for current, dirs, files in os.walk(path):
        base = Path(current)
        need(all(not (base / name).is_symlink() for name in dirs), "core dir symlink")
        for name in files:
            item = base / name
            need(item.is_file() and not item.is_symlink(), "core regular file")
            result.append(str(item.relative_to(ROOT)))
    return result


def adapter_args(adapter: Path) -> list[str]:
    receipt = document(adapter / "terminal_receipt.json", "terminal_receipt_sha256")
    authority_kind = receipt.get("authority_kind")
    need(authority_kind in {"C27R2", "C28"}, "adapter authority kind")
    label = "c27r2" if authority_kind == "C27R2" else "c28"
    return ["--" + label + "-terminal-dir", str(adapter),
            "--expect-" + label + "-root-sha256", file_sha(adapter / "root_manifest.sha256"),
            "--expect-" + label + "-receipt-file-sha256", file_sha(adapter / "terminal_receipt.json"),
            "--expect-" + label + "-receipt-object-sha256", receipt["terminal_receipt_sha256"]]


def validate_core_provenance(core: dict[str, Any],
                             pinset: dict[str, Any]) -> None:
    stages = set(CORE_STAGE_SEEDS)
    spec_objects = core.get("stage_command_spec_objects")
    run_objects = core.get("stage_run_attestation_objects")
    need(pinset.get("source_pins") == CORE_SOURCE_PINS
         and core.get("source_pins") == CORE_SOURCE_PINS
         and core.get("source_pins") == pinset.get("source_pins"),
         "core source pin closure")
    need(pinset.get("stage_python_hash_seeds") == CORE_STAGE_SEEDS
         and core.get("stage_python_hash_seeds") == CORE_STAGE_SEEDS
         and pinset.get("producer_seed1") == CORE_STAGE_SEEDS["producer"]
         and core.get("producer_seed1") == CORE_STAGE_SEEDS["producer"]
         and pinset.get("verifier_seed2")
             == CORE_STAGE_SEEDS["independent_verifier"]
         and core.get("verifier_seed2")
             == CORE_STAGE_SEEDS["independent_verifier"]
         and pinset.get("dual_real_hash_seeds")
             == [CORE_STAGE_SEEDS["producer"],
                 CORE_STAGE_SEEDS["independent_verifier"]]
         and core.get("dual_real_hash_seeds")
             == [CORE_STAGE_SEEDS["producer"],
                 CORE_STAGE_SEEDS["independent_verifier"]],
         "core seed provenance closure")
    need(type(spec_objects) is dict and set(spec_objects) == stages
         and type(run_objects) is dict and set(run_objects) == stages
         and all(valid_sha(value) for value in spec_objects.values())
         and all(valid_sha(value) for value in run_objects.values()),
         "core command/run object provenance closure")


def validate_core_command_specs(control: Path, core: dict[str, Any],
                                pinset: dict[str, Any]) -> None:
    expected_objects = core["stage_command_spec_objects"]
    pinset_path = control / "pinset.json"
    for stage, seed in CORE_STAGE_SEEDS.items():
        value = document(control / (stage + "_command_spec.json"),
                         "command_spec_sha256")
        source_name = CORE_STAGE_SOURCE_PINS[stage]
        need(value.get("schema") == SPEC_SCHEMA
             and value.get("stage") == stage
             and value.get("command_spec_sha256") == expected_objects[stage]
             and value.get("source_path") == str(CORE_SOURCES[source_name])
             and value.get("source_sha256") == CORE_SOURCE_PINS[source_name]
             and value.get("python_hash_seed") == seed
             and value.get("environment") == {
                 "PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
                 "PYTHONHASHSEED": seed}
             and value.get("pinset_file_sha256") == file_sha(pinset_path)
             and value.get("pinset_object_sha256") == pinset["pinset_sha256"]
             and value.get("runner_source_sha256") == CORE_SOURCE_PINS["runner"]
             and value.get("python_sha256") == CORE_SOURCE_PINS["python"],
             stage + ":core command spec provenance")


def validate_core(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any], dict[str, Path]]:
    control = Path(args.core_control_dir).absolute()
    need(control.parent == AUDIT and control.is_dir(), "core control")
    core_path = control / "core_receipt.json"
    core = document(core_path, "core_receipt_sha256")
    need(valid_sha(args.expect_core_receipt_file_sha256)
         and valid_sha(args.expect_core_receipt_object_sha256)
         and file_sha(core_path) == args.expect_core_receipt_file_sha256
         and core["core_receipt_sha256"] == args.expect_core_receipt_object_sha256
         and core.get("schema") == CORE_SCHEMA and core.get("status") == CORE_STATUS
         and core.get("formal_credit") == 0
         and core.get("manifest_authorized") is False
         and core.get("C29", "").startswith("UNAUTHORIZED_")
         and (control / "PASS.lock").read_bytes()
             == b"PASS_C29_V2_DUAL_TERMINAL_SEED_CORE__ZERO_CREDIT\n"
         and not (control / "FAILED.lock").exists(), "core boundary")
    service_success(core["unit_name"], core["systemd_invocation_id"])
    pinset = document(control / "pinset.json", "pinset_sha256")
    need(pinset.get("schema") == PINSET_SCHEMA
         and core.get("pinset_file_sha256") == file_sha(control / "pinset.json")
         and core.get("pinset_object_sha256") == pinset["pinset_sha256"],
         "core pinset")
    validate_core_provenance(core, pinset)
    validate_core_command_specs(control, core, pinset)
    need(type(pinset.get("targets")) is dict
         and set(pinset["targets"]) == CORE_TARGET_KEYS,
         "exact core target keys")
    targets = {name: ROOT / raw for name, raw in pinset["targets"].items()}
    need(all(path.is_relative_to(AUDIT) and path.absolute() == path
             and not path.is_symlink() for path in targets.values()), "core targets")
    return core, pinset, targets


def execute(args: argparse.Namespace) -> dict[str, Any]:
    need(valid_sha(args.expect_helper_sha256)
         and file_sha(SELF) == args.expect_helper_sha256
         and all(file_sha(CORE_SOURCES[name]) == CORE_SOURCE_PINS[name]
                 for name in CORE_SOURCES), "cold/core source pins")
    core, core_pinset, targets = validate_core(args)
    control = Path(args.control_dir).absolute()
    output = Path(args.output_dir).absolute()
    run = Path(args.run_dir).absolute()
    need(len({control, output, run}) == 3
         and all(path.parent == AUDIT and not path.exists()
                 and not path.is_symlink()
                 for path in (control, output, run)), "fresh cold paths")
    if args.preflight_only:
        return {"status": "PASS_C29_V2_CORE_AND_FRESH_COLD_REPLAY_PREFLIGHT__NO_OUTPUT_ZERO_CREDIT"}
    stage = "control"
    try:
        control.mkdir(mode=0o700)
        output.mkdir(mode=0o700)
        body = {"schema": PINSET_SCHEMA,
                "status": "PASS_C29_V2_RELEASE_COLD_REPLAY_PINSET__ZERO_CREDIT",
                "core_receipt_file_sha256": args.expect_core_receipt_file_sha256,
                "core_receipt_object_sha256": args.expect_core_receipt_object_sha256,
                "source_pins": {**CORE_SOURCE_PINS,
                                "helper": args.expect_helper_sha256},
                "formal_credit": 0, "manifest_authorized": False,
                "C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM"}
        cold_pinset = dict(body)
        cold_pinset["pinset_sha256"] = digest(cold_pinset)
        pinset_path = control / "pinset.json"
        write_json(pinset_path, cold_pinset)
        c27 = targets["c27_adapter"]
        c28 = targets["c28_adapter"]
        authority = adapter_args(c27) + adapter_args(c28)
        verification_path = output / "verification.json"
        argv = [str(PYTHON), "-I", "-B", str(VERIFIER), *authority,
                "--candidate-dir", str(targets["candidate"]),
                "--out-file", str(verification_path)]
        inputs: list[str] = []
        for path in targets.values():
            inputs.extend(recursive_files(path))
        # Re-capture every external input named by the original isolated core
        # command specs (not merely the spec files themselves).  This includes
        # the C25 member/representation authority and all frozen sources.
        core_control = targets["control"]
        for spec_path in sorted(core_control.glob("*_command_spec.json")):
            spec_value = document(spec_path, "command_spec_sha256")
            need(spec_value.get("schema") == SPEC_SCHEMA
                 and type(spec_value.get("input_paths")) is list,
                 "core command-spec input inventory")
            source_member = Path(spec_value["source_path"])
            need(source_member in CORE_SOURCES.values(),
                 "core command-spec frozen source")
            inputs.append(str(source_member.relative_to(ROOT)))
            for raw in spec_value["input_paths"]:
                member = ROOT / raw
                need(member.is_file() and not member.is_symlink(),
                     "core external input")
                inputs.append(str(member.relative_to(ROOT)))
        for adapter in (c27, c28):
            for member in (adapter / "payload_manifest.sha256").read_text().splitlines():
                inputs.append(member.split("  ", 1)[1])
        inputs.extend([str(SELF.relative_to(ROOT))])
        inputs.extend(str(path.relative_to(ROOT))
                      for path in CORE_SOURCES.values())
        spec_body = {"schema": SPEC_SCHEMA, "stage": "independent_verifier",
            "source_path": str(VERIFIER), "source_sha256": VERIFIER_SHA,
            "argv": argv, "environment": {"PATH": "/usr/bin:/bin", "LANG": "C",
                "LC_ALL": "C", "PYTHONHASHSEED": "30662982"},
            "python_hash_seed": "30662982", "timeout_seconds": args.timeout_seconds,
            "expected_stdout_status": VERIFY_STATUS,
            "input_paths": sorted(set(inputs)),
            "output_roots": [{"path": str(output), "kind": "directory",
                "precondition": "EXISTING_EMPTY_DIRECTORY",
                "exact_inventory": ["verification.json"],
                "required_relative_files": ["verification.json"]}],
            "pinset_file_sha256": file_sha(pinset_path),
            "pinset_object_sha256": cold_pinset["pinset_sha256"],
            "runner_source_sha256": RUNNER_SHA, "python_sha256": PYTHON_SHA,
            "formal_credit": 0, "CM2": "NO-GO_FOR_CLAIM"}
        spec = dict(spec_body)
        spec["command_spec_sha256"] = digest(spec)
        spec_path = control / "cold_command_spec.json"
        write_json(spec_path, spec)
        stage = "cold_verifier"
        completed = subprocess.run([str(PYTHON), "-I", "-B", str(RUNNER),
            "--stage", "independent_verifier", "--command-spec", str(spec_path),
            "--pinset", str(pinset_path), "--run-dir", str(run),
            "--expect-runner-sha256", RUNNER_SHA,
            "--expect-python-sha256", PYTHON_SHA], cwd=ROOT,
            env={"PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
                 "PYTHONHASHSEED": "30662983"}, stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        write_once(control / "runner.stdout.log", completed.stdout)
        write_once(control / "runner.stderr.log", completed.stderr)
        write_once(control / "runner.exit_code.txt",
                   (str(completed.returncode) + "\n").encode())
        need(completed.returncode == 0 and completed.stderr == b"", "cold runner")
        prior_path = targets["verification"]
        cold = document(verification_path, "verification_sha256")
        prior = document(prior_path, "verification_sha256")
        need(verification_path.read_bytes() == prior_path.read_bytes()
             and cold["verification_sha256"] == prior["verification_sha256"],
             "cold byte replay")
        attestation = document(run / "run_attestation.json", "run_attestation_sha256")
        need(attestation.get("schema") == RUN_SCHEMA
             and attestation.get("status") == RUN_STATUS
             and attestation.get("numeric_exit_code") == 0
             and attestation.get("signal") is None
             and attestation.get("stderr_empty") is True
             and attestation.get("input_pre_post_sha_stat_identical") is True,
             "cold attestation")
        body = {"schema": COLD_SCHEMA, "status": COLD_STATUS,
                "completed_at_utc": now(),
                "core_receipt_file_sha256": args.expect_core_receipt_file_sha256,
                "core_receipt_object_sha256": args.expect_core_receipt_object_sha256,
                "core_unit_name": core["unit_name"],
                "core_invocation_id": core["systemd_invocation_id"],
                "verification_file_sha256": file_sha(verification_path),
                "verification_object_sha256": cold["verification_sha256"],
                "formal_verification_byte_identical": True,
                "run_attestation_file_sha256": file_sha(run / "run_attestation.json"),
                "run_attestation_object_sha256": attestation["run_attestation_sha256"],
                "all_core_inputs_pre_post_sha_stat_identical": True,
                "numeric_exit_code": 0, "signal": None, "stderr_empty": True,
                "formal_credit": 0, "manifest_authorized": False,
                "C29": "UNAUTHORIZED_PENDING_RELEASE_ATTACKS_MANIFEST_OUTER_SEAL_TERMINAL_REPLAY",
                "CM2": "NO-GO_FOR_CLAIM"}
        receipt = dict(body)
        receipt["cold_replay_receipt_sha256"] = digest(receipt)
        write_json(control / "cold_replay_receipt.json", receipt)
        write_once(control / "PASS.lock", b"PASS_C29_V2_RELEASE_COLD_REPLAY__ZERO_CREDIT\n")
        return receipt
    except BaseException as error:
        if control.exists():
            body = {"schema": BASE + "release-cold-failure.v1",
                    "status": "FAILED_CLOSED_C29_V2_RELEASE_COLD_REPLAY__ZERO_CREDIT",
                    "stage": stage, "error": f"{type(error).__name__}:{error}",
                    "formal_credit": 0, "C29": "UNAUTHORIZED",
                    "CM2": "NO-GO_FOR_CLAIM"}
            failure = dict(body)
            failure["failure_receipt_sha256"] = digest(failure)
            if not (control / "failure_receipt.json").exists():
                write_json(control / "failure_receipt.json", failure)
            if not (control / "FAILED.lock").exists():
                write_once(control / "FAILED.lock", b"FAILED_CLOSED_C29_V2_RELEASE_COLD_REPLAY\n")
        raise


def self_test() -> dict[str, Any]:
    spec_objects = {stage: "0" * 64 for stage in CORE_STAGE_SEEDS}
    run_objects = {stage: "1" * 64 for stage in CORE_STAGE_SEEDS}
    fixture = {
        "source_pins": CORE_SOURCE_PINS,
        "stage_python_hash_seeds": CORE_STAGE_SEEDS,
        "producer_seed1": CORE_STAGE_SEEDS["producer"],
        "verifier_seed2": CORE_STAGE_SEEDS["independent_verifier"],
        "dual_real_hash_seeds": [CORE_STAGE_SEEDS["producer"],
                                 CORE_STAGE_SEEDS["independent_verifier"]],
        "stage_command_spec_objects": spec_objects,
        "stage_run_attestation_objects": run_objects,
    }
    validate_core_provenance(fixture, fixture)
    wrong = dict(fixture)
    wrong["source_pins"] = {**CORE_SOURCE_PINS, "watcher": "f" * 64}
    rejected = False
    try:
        validate_core_provenance(wrong, fixture)
    except Failure:
        rejected = True
    missing = dict(fixture)
    missing["source_pins"] = {name: value for name, value in CORE_SOURCE_PINS.items()
                              if name != "watcher"}
    missing_rejected = False
    try:
        validate_core_provenance(fixture, missing)
    except Failure:
        missing_rejected = True
    need(rejected and missing_rejected
         and set(CORE_SOURCES) == set(CORE_SOURCE_PINS)
         and set(CORE_STAGE_SOURCE_PINS) == set(CORE_STAGE_SEEDS)
         and len(CORE_TARGET_KEYS) == 16
         and all(file_sha(CORE_SOURCES[name]) == CORE_SOURCE_PINS[name]
                 for name in CORE_SOURCES), "source/provenance fixtures")
    return {"status": "PASS_C29_V2_COLD_REPLAY_V3_COMPLETE_CORE_PROVENANCE_SELF_TEST",
            "formal_credit": 0, "C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--preflight-only", action="store_true")
    for name in ("core-control-dir", "control-dir", "output-dir", "run-dir",
                 "expect-core-receipt-file-sha256",
                 "expect-core-receipt-object-sha256", "expect-helper-sha256"):
        parser.add_argument("--" + name)
    parser.add_argument("--timeout-seconds", type=int, default=21_600)
    args = parser.parse_args()
    fields = ("core_control_dir", "control_dir", "output_dir", "run_dir",
              "expect_core_receipt_file_sha256", "expect_core_receipt_object_sha256",
              "expect_helper_sha256")
    try:
        if args.self_test:
            need(not args.preflight_only
                 and all(getattr(args, field) is None for field in fields),
                 "self-test arguments")
            result = self_test()
        else:
            need(all(getattr(args, field) is not None for field in fields)
                 and 60 <= args.timeout_seconds <= 86_400, "run arguments")
            result = execute(args)
        sys.stdout.buffer.write(canonical({"CM2": "NO-GO_FOR_CLAIM",
            "formal_credit": 0, "status": result["status"]}) + b"\n")
        return 0
    except (Failure, OSError, ValueError, KeyError, TypeError,
            subprocess.SubprocessError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
