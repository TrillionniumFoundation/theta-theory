#!/usr/bin/env python3
"""Gate and run the zero-credit C29-v2 dual-terminal mathematical core."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
AUDIT = ROOT / ".cm2-runtime/audit"
PYTHON = Path("/usr/bin/python3.12")
PREFIX = "cm2_round306c29_source_g_post_c27r2_member_rebound_fibre_exhaustion_v2"
BUILDER = ROOT / f"deliverables/{PREFIX}_terminal_consumer_adapter_builder_v2.py"
ADAPTER_VERIFIER = ROOT / f"deliverables/{PREFIX}_terminal_consumer_adapter_independent_verifier_v1.py"
RUNNER = ROOT / f"deliverables/{PREFIX}_transaction_runner_v1.py"
PRODUCER = ROOT / f"deliverables/{PREFIX}_producer_contract_v3.py"
VERIFIER = ROOT / f"deliverables/{PREFIX}_independent_verifier_contract_v3.py"
ATTACKS = ROOT / f"deliverables/{PREFIX}_coherent_attack_harness_contract_v5.py"
PINS = {
    "builder": "1a50765bb1fadd3fbd0ff69594c5c355969786350e7e988aab2acfe519e8ecc9",
    "adapter_verifier": "eccc4422a3ebba0ce505f4802bb508c3da007ae099a2b6f8f21b1347be5b3201",
    "runner": "ce04aa7d977ef50fac956be2717dd9c0eb70ce6f09932468357698965d58beb3",
    "producer": "4ede5bf738431b769ecbb87d4160c9d35e5243314799583d418380b9e72a23c7",
    "verifier": "3229f56ca8d00c479a3f671dd6f4d8d415da893bfd57897963f0eb0ea82eb192",
    "attacks": "9a387a712033119c8aa615b5eaf544bf38778119eea18afa598b26cb351620f0",
    "python": "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118",
}
C27_PINS = {
    "root": "1f65a624c889773e3104c4311788fc06be04d6ca92e033205074b8cc7f5b27fc",
    "receipt_file": "feccb0b9290bd82ac1d8e78e8e7a21d4f25e0ca3aa3556cc3f0bb6007f61c3dd",
    "receipt_object": "8afbd127c9518f569c2f7b3edcdbe9e0ebf77d88bcca855822e58d21e5cfe782",
    "replay_file": "b480df4b8caaf9876a48720f92a8fb6d86e2b1b5966bcc71b0022c5e49fc12ee",
    "replay_object": "216d2592c49b0302de0042677ce54c96cd5ad1fcb32231da02b39c003cb837e8",
    "pass": "5fe4140b3e8f38196e9ca68cd336ae29be1c8847c7685526f08aa4d7173d7348",
}
BASE = "cm2.round306c29.source-g-post-c27r2-member-rebound-fibre-exhaustion.v2."
PINSET_SCHEMA = BASE + "gated-transaction-pinset.v1"
SPEC_SCHEMA = BASE + "process-command-spec.v1"
RUN_SCHEMA = BASE + "process-run-attestation.v1"
RUN_STATUS = "PASS_C29_V2_PROCESS_TRANSACTION_EXIT0_NULL_SIGNAL_EMPTY_STDERR_PRE_POST_AND_OUTPUTS__ZERO_CREDIT"
CORE_SCHEMA = BASE + "gated-dual-terminal-seed-core-receipt.v1"
CORE_STATUS = "PASS_C29_V2_DUAL_TERMINAL_ADAPTERS_SEED1_PRODUCER_SEED2_NO_IMPORT_VERIFIER_AND_34_ATTACKS__ZERO_CREDIT_PENDING_RELEASE_TERMINAL"
ADAPTER_BUILD_STATUS = "PASS_C29_V2_SOURCE_TERMINAL_CONSUMER_ADAPTER_PREFLIGHT__NO_OUTPUT_ZERO_CREDIT"
ADAPTER_VERIFY_STATUS = "PASS_NO_IMPORT_C29_V2_TERMINAL_CONSUMER_ADAPTER_INDEPENDENT_VERIFICATION__ZERO_CREDIT"
PRODUCER_STATUS = "PASS_C29_V2_MATHEMATICAL_CANDIDATE__POST_C27R2_MEMBER_REBIND_AND_FIBRE_EXHAUSTION_RECOMPUTED__ZERO_CREDIT_PENDING_FULL_RELEASE_TERMINAL"
VERIFIER_STATUS = "PASS_NO_IMPORT_INDEPENDENT_C29_V2_FULL_RECONSTRUCTION__CONDITIONAL_ZERO_CREDIT_PENDING_ATTACKS_AND_RELEASE_TERMINAL"
ATTACK_STATUS = "PASS_34_OF_34_C29_V2_COHERENT_CANDIDATE_AND_AUTHORITY_ATTACKS_REJECTED__ZERO_CREDIT"
CANDIDATE_FILES = sorted([
    PREFIX + "_global_member_disposition_ledger.jsonl.gz",
    PREFIX + "_official_key_fibre_exhaustion_ledger.jsonl.gz",
    PREFIX + "_post_component_official_key_assignment_ledger.jsonl.gz",
    PREFIX + "_result.json",
])
ADAPTER_FILES = sorted(["PASS.lock", "c29_consumer_projection.json",
                        "payload_manifest.sha256", "root_manifest.sha256",
                        "terminal_receipt.json"])
STAGES = ("c27_adapter", "c27_adapter_verifier", "c28_adapter",
          "c28_adapter_verifier", "producer", "independent_verifier",
          "coherent_attacks")


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
            and all(char in "0123456789abcdef" for char in value))


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
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                         | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular single-link:" + str(path))
        state = hashlib.sha256()
        while block := os.read(descriptor, 4 << 20):
            state.update(block)
        need(fingerprint(os.fstat(descriptor)) == fingerprint(before),
             "stable hash:" + str(path))
        return state.hexdigest()
    finally:
        os.close(descriptor)


def document(path: Path, closure: str) -> dict[str, Any]:
    payload = path.read_bytes()
    need(payload.endswith(b"\n") and not payload.endswith(b"\n\n"),
         "document newline:" + str(path))
    value = strict(payload[:-1])
    need(type(value) is dict and canonical(value) == payload[:-1],
         "canonical document:" + str(path))
    body = dict(value)
    claim = body.pop(closure, None)
    need(valid_sha(claim) and claim == digest(body), "document closure")
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


def parse_manifest(path: Path) -> dict[str, str]:
    payload = path.read_bytes()
    need(payload.endswith(b"\n"), "manifest newline")
    result: dict[str, str] = {}
    for line in payload.decode("ascii").splitlines():
        fields = line.split("  ", 1)
        need(len(fields) == 2 and valid_sha(fields[0])
             and fields[1] not in result, "manifest row")
        result[fields[1]] = fields[0]
    return result


def paths(stem: str) -> dict[str, Path]:
    need(re.fullmatch(r"c29-v2-[a-z0-9][a-z0-9-]{7,100}", stem) is not None,
         "canonical unique stem")
    result = {
        "control": AUDIT / (stem + "-control"),
        "c27_adapter": AUDIT / (stem + "-c27-adapter"),
        "c27_adapter_verification": AUDIT / (stem + "-c27-adapter-verification.json"),
        "c28_adapter": AUDIT / (stem + "-c28-adapter"),
        "c28_adapter_verification": AUDIT / (stem + "-c28-adapter-verification.json"),
        "candidate": AUDIT / (stem + "-candidate"),
        "verification": AUDIT / (stem + "-verification.json"),
        "attack_work": AUDIT / (stem + "-attack-work"),
        "attacks": AUDIT / (stem + "-attacks.json"),
    }
    result.update({"run_" + stage: AUDIT / (stem + "-run-" + stage.replace("_", "-"))
                   for stage in STAGES})
    need(len(set(result.values())) == len(result)
         and all(path.parent == AUDIT for path in result.values()),
         "fresh topology")
    return result


def source_files() -> dict[str, Path]:
    values = {"builder": BUILDER, "adapter_verifier": ADAPTER_VERIFIER,
              "runner": RUNNER, "producer": PRODUCER,
              "verifier": VERIFIER, "attacks": ATTACKS, "python": PYTHON}
    need(all(path.is_file() and not path.is_symlink()
             and file_sha(path) == PINS[name] for name, path in values.items()),
         "frozen source/Python pins")
    return values


def terminal_inputs(directory: Path) -> list[str]:
    need(directory.parent == AUDIT and directory.is_dir()
         and {entry.name for entry in directory.iterdir()} == {
             "PASS.lock", "chain_status.json", "payload_manifest.sha256",
             "root_manifest.sha256", "terminal_receipt.json",
             "terminal_replay.json"}, "source terminal inventory")
    result = [str((directory / name).relative_to(ROOT)) for name in sorted(
        entry.name for entry in directory.iterdir())]
    for name in ("root_manifest.sha256", "payload_manifest.sha256"):
        for member in parse_manifest(directory / name):
            path = ROOT / member
            need(path.is_file() and not path.is_symlink()
                 and file_sha(path) == parse_manifest(directory / name)[member],
                 "terminal manifest member")
            result.append(member)
    return sorted(set(result))


def adapter_inputs(directory: Path) -> list[str]:
    need(directory.is_dir() and {entry.name for entry in directory.iterdir()}
         == set(ADAPTER_FILES), "adapter inventory")
    result = [str((directory / name).relative_to(ROOT)) for name in ADAPTER_FILES]
    for member in parse_manifest(directory / "payload_manifest.sha256"):
        result.append(member)
    return sorted(set(result))


def c25_inputs() -> list[str]:
    names = [
        "cm2_round306c25_source_g_502204_member_549616_representation_typed_global_support_ledger_manifest.sha256",
        "cm2_round306c25_source_g_502204_member_549616_representation_typed_global_support_ledger_member_ledger.jsonl.gz",
        "cm2_round306c25_source_g_502204_member_549616_representation_typed_global_support_ledger_representation_ledger.jsonl.gz",
        "cm2_round306c25_source_g_502204_member_549616_representation_typed_global_support_ledger_result.json",
        "cm2_round306c25_source_g_502204_member_549616_representation_typed_global_support_ledger_verification.json",
    ]
    result = ["deliverables/" + name for name in names]
    need(all((ROOT / path).is_file() and not (ROOT / path).is_symlink()
             for path in result), "C25 inputs")
    return result


def pinset(args: argparse.Namespace, targets: dict[str, Path]) -> dict[str, Any]:
    body = {"schema": PINSET_SCHEMA,
            "status": "PASS_C29_V2_DUAL_TERMINAL_CORE_PINSET__ZERO_CREDIT",
            "source_pins": PINS,
            "C27R2_terminal": {"dir": args.c27r2_terminal_dir, **C27_PINS},
            "C28_terminal": {
                "dir": args.c28_terminal_dir,
                "root": args.expect_c28_root_sha256,
                "receipt_file": args.expect_c28_receipt_file_sha256,
                "receipt_object": args.expect_c28_receipt_object_sha256,
                "replay_file": args.expect_c28_replay_file_sha256,
                "replay_object": args.expect_c28_replay_object_sha256,
                "pass": args.expect_c28_pass_lock_sha256},
            "targets": {name: str(path.relative_to(ROOT))
                        for name, path in sorted(targets.items())},
            "seed1": "30662901", "seed2": "30662902",
            "formal_credit": 0, "manifest_authorized": False,
            "C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM"}
    value = dict(body)
    value["pinset_sha256"] = digest(value)
    return value


def spec(stage: str, source: Path, source_sha: str, argv: list[str], seed: str,
         expected_status: str, inputs: list[str], outputs: list[dict[str, Any]],
         pinset_path: Path, pinset_value: dict[str, Any], timeout: int) -> dict[str, Any]:
    body = {"schema": SPEC_SCHEMA, "stage": stage,
            "source_path": str(source), "source_sha256": source_sha,
            "argv": argv,
            "environment": {"PATH": "/usr/bin:/bin", "LANG": "C",
                            "LC_ALL": "C", "PYTHONHASHSEED": seed},
            "python_hash_seed": seed, "timeout_seconds": timeout,
            "expected_stdout_status": expected_status,
            "input_paths": sorted(set(inputs)), "output_roots": outputs,
            "pinset_file_sha256": file_sha(pinset_path),
            "pinset_object_sha256": pinset_value["pinset_sha256"],
            "runner_source_sha256": PINS["runner"],
            "python_sha256": PINS["python"], "formal_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM"}
    value = dict(body)
    value["command_spec_sha256"] = digest(value)
    return value


def run_stage(control: Path, targets: dict[str, Path], pinset_path: Path,
              pinset_value: dict[str, Any], stage: str, source: Path,
              source_sha: str, argv: list[str], seed: str, expected: str,
              inputs: list[str], outputs: list[dict[str, Any]], timeout: int) -> dict[str, Any]:
    spec_value = spec(stage, source, source_sha, argv, seed, expected, inputs,
                      outputs, pinset_path, pinset_value, timeout)
    spec_path = control / (stage + "_command_spec.json")
    write_json(spec_path, spec_value)
    run_dir = targets["run_" + stage]
    completed = subprocess.run([
        str(PYTHON), "-I", "-B", str(RUNNER), "--stage", stage,
        "--command-spec", str(spec_path), "--pinset", str(pinset_path),
        "--run-dir", str(run_dir), "--expect-runner-sha256", PINS["runner"],
        "--expect-python-sha256", PINS["python"]], cwd=ROOT,
        env={"PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
             "PYTHONHASHSEED": str(int(seed) + 100)}, stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    write_once(control / (stage + ".runner.stdout.log"), completed.stdout)
    write_once(control / (stage + ".runner.stderr.log"), completed.stderr)
    write_once(control / (stage + ".runner.exit_code.txt"),
               (str(completed.returncode) + "\n").encode("ascii"))
    need(completed.returncode == 0 and completed.stderr == b"",
         stage + ":transaction runner clean exit")
    attestation = document(run_dir / "run_attestation.json",
                           "run_attestation_sha256")
    need(attestation.get("schema") == RUN_SCHEMA
         and attestation.get("status") == RUN_STATUS
         and attestation.get("stage") == stage
         and attestation.get("numeric_exit_code") == 0
         and attestation.get("signal") is None
         and attestation.get("stderr_empty") is True
         and attestation.get("input_pre_post_sha_stat_identical") is True,
         stage + ":run attestation")
    return attestation


def adapter_args(kind: str, terminal: Path, pins: dict[str, str],
                 output: Path) -> list[str]:
    return [str(PYTHON), "-I", "-B", str(BUILDER), "--kind", kind,
            "--source-terminal-dir", str(terminal),
            "--expect-source-root-sha256", pins["root"],
            "--expect-source-receipt-file-sha256", pins["receipt_file"],
            "--expect-source-receipt-object-sha256", pins["receipt_object"],
            "--expect-source-replay-file-sha256", pins["replay_file"],
            "--expect-source-replay-object-sha256", pins["replay_object"],
            "--expect-source-pass-lock-sha256", pins["pass"],
            "--expect-builder-sha256", PINS["builder"],
            "--output-dir", str(output)]


def adapter_verifier_args(kind: str, terminal: Path, pins: dict[str, str],
                          adapter: Path, output: Path) -> list[str]:
    receipt = document(adapter / "terminal_receipt.json", "terminal_receipt_sha256")
    return [str(PYTHON), "-I", "-B", str(ADAPTER_VERIFIER), "--kind", kind,
            "--source-terminal-dir", str(terminal),
            "--expect-source-root-sha256", pins["root"],
            "--expect-source-receipt-file-sha256", pins["receipt_file"],
            "--expect-source-receipt-object-sha256", pins["receipt_object"],
            "--expect-source-replay-file-sha256", pins["replay_file"],
            "--expect-source-replay-object-sha256", pins["replay_object"],
            "--expect-source-pass-lock-sha256", pins["pass"],
            "--adapter-dir", str(adapter),
            "--expect-adapter-root-sha256", file_sha(adapter / "root_manifest.sha256"),
            "--expect-adapter-receipt-file-sha256", file_sha(adapter / "terminal_receipt.json"),
            "--expect-adapter-receipt-object-sha256", receipt["terminal_receipt_sha256"],
            "--expect-verifier-sha256", PINS["adapter_verifier"],
            "--out-file", str(output)]


def core_authority_args(c27: Path, c28: Path) -> list[str]:
    result: list[str] = []
    for label, adapter in (("c27r2", c27), ("c28", c28)):
        receipt = document(adapter / "terminal_receipt.json", "terminal_receipt_sha256")
        result.extend(["--" + label + "-terminal-dir", str(adapter),
            "--expect-" + label + "-root-sha256", file_sha(adapter / "root_manifest.sha256"),
            "--expect-" + label + "-receipt-file-sha256", file_sha(adapter / "terminal_receipt.json"),
            "--expect-" + label + "-receipt-object-sha256", receipt["terminal_receipt_sha256"]])
    return result


def preflight_builder(kind: str, terminal: Path, pins: dict[str, str],
                      target: Path) -> None:
    completed = subprocess.run(adapter_args(kind, terminal, pins, target)
                               + ["--preflight-only"], cwd=ROOT,
        env={"PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
             "PYTHONHASHSEED": "30662900"}, stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    need(completed.returncode == 0 and completed.stderr == b""
         and not target.exists(), kind + ":adapter preflight")


def execute(args: argparse.Namespace) -> dict[str, Any]:
    need(valid_sha(args.expect_watcher_sha256)
         and file_sha(SELF) == args.expect_watcher_sha256, "watcher self pin")
    source_files()
    c27 = Path(args.c27r2_terminal_dir).absolute()
    c28 = Path(args.c28_terminal_dir).absolute()
    need(c27.parent == AUDIT and c28.parent == AUDIT, "terminal paths")
    c28pins = {"root": args.expect_c28_root_sha256,
               "receipt_file": args.expect_c28_receipt_file_sha256,
               "receipt_object": args.expect_c28_receipt_object_sha256,
               "replay_file": args.expect_c28_replay_file_sha256,
               "replay_object": args.expect_c28_replay_object_sha256,
               "pass": args.expect_c28_pass_lock_sha256}
    need(all(valid_sha(value) for value in c28pins.values()), "C28 terminal pins")
    targets = paths(args.stem)
    need(all(not path.exists() and not path.is_symlink()
             for path in targets.values()), "all fresh targets")
    terminal_inputs(c27)
    terminal_inputs(c28)
    preflight_builder("C27R2", c27, C27_PINS, targets["c27_adapter"])
    preflight_builder("C28", c28, c28pins, targets["c28_adapter"])
    if args.preflight_only:
        need(all(not path.exists() for path in targets.values()),
             "preflight creates nothing")
        return {"status": "PASS_C29_V2_DUAL_TERMINAL_CORE_AND_ALL_FRESH_TARGETS_PREFLIGHT__NO_OUTPUT_ZERO_CREDIT"}
    invocation = os.environ.get("INVOCATION_ID")
    need(type(invocation) is str and re.fullmatch(r"[0-9a-f]{32}", invocation) is not None,
         "systemd invocation ID")
    control = targets["control"]
    control.mkdir(mode=0o700)
    stage = "control"
    try:
        pinset_value = pinset(args, targets)
        pinset_path = control / "pinset.json"
        write_json(pinset_path, pinset_value)
        terminal_sets = {"C27R2": terminal_inputs(c27), "C28": terminal_inputs(c28)}
        attestations: dict[str, Any] = {}
        stage = "c27_adapter"
        attestations[stage] = run_stage(control, targets, pinset_path, pinset_value,
            stage, BUILDER, PINS["builder"],
            adapter_args("C27R2", c27, C27_PINS, targets[stage]), "30662901",
            "PASS_C29_V2_C27R2_TERMINAL_CONSUMER_ADAPTER__ZERO_CREDIT",
            terminal_sets["C27R2"] + [str(BUILDER.relative_to(ROOT))],
            [{"path": str(targets[stage]), "kind": "directory", "precondition": "ABSENT",
              "exact_inventory": ADAPTER_FILES, "required_relative_files": ADAPTER_FILES}],
            args.timeout_seconds)
        stage = "c27_adapter_verifier"
        attestations[stage] = run_stage(control, targets, pinset_path, pinset_value,
            stage, ADAPTER_VERIFIER, PINS["adapter_verifier"],
            adapter_verifier_args("C27R2", c27, C27_PINS, targets["c27_adapter"],
                                  targets["c27_adapter_verification"]), "30662902",
            ADAPTER_VERIFY_STATUS,
            terminal_sets["C27R2"] + adapter_inputs(targets["c27_adapter"]),
            [{"path": str(targets["c27_adapter_verification"]), "kind": "file",
              "precondition": "ABSENT", "exact_inventory": None,
              "required_relative_files": []}], args.timeout_seconds)
        stage = "c28_adapter"
        attestations[stage] = run_stage(control, targets, pinset_path, pinset_value,
            stage, BUILDER, PINS["builder"],
            adapter_args("C28", c28, c28pins, targets[stage]), "30662903",
            "PASS_C29_V2_C28_TERMINAL_CONSUMER_ADAPTER__ZERO_CREDIT",
            terminal_sets["C28"] + [str(BUILDER.relative_to(ROOT))],
            [{"path": str(targets[stage]), "kind": "directory", "precondition": "ABSENT",
              "exact_inventory": ADAPTER_FILES, "required_relative_files": ADAPTER_FILES}],
            args.timeout_seconds)
        stage = "c28_adapter_verifier"
        attestations[stage] = run_stage(control, targets, pinset_path, pinset_value,
            stage, ADAPTER_VERIFIER, PINS["adapter_verifier"],
            adapter_verifier_args("C28", c28, c28pins, targets["c28_adapter"],
                                  targets["c28_adapter_verification"]), "30662904",
            ADAPTER_VERIFY_STATUS,
            terminal_sets["C28"] + adapter_inputs(targets["c28_adapter"]),
            [{"path": str(targets["c28_adapter_verification"]), "kind": "file",
              "precondition": "ABSENT", "exact_inventory": None,
              "required_relative_files": []}], args.timeout_seconds)
        authorities = core_authority_args(targets["c27_adapter"], targets["c28_adapter"])
        core_inputs = sorted(set(adapter_inputs(targets["c27_adapter"])
                                 + adapter_inputs(targets["c28_adapter"])
                                 + c25_inputs()
                                 + [str(targets["c27_adapter_verification"].relative_to(ROOT)),
                                    str(targets["c28_adapter_verification"].relative_to(ROOT))]))
        stage = "producer"
        attestations[stage] = run_stage(control, targets, pinset_path, pinset_value,
            stage, PRODUCER, PINS["producer"],
            [str(PYTHON), "-I", "-B", str(PRODUCER), *authorities,
             "--out-dir", str(targets["candidate"])], "30662905", PRODUCER_STATUS,
            core_inputs, [{"path": str(targets["candidate"]), "kind": "directory",
                "precondition": "ABSENT", "exact_inventory": CANDIDATE_FILES,
                "required_relative_files": CANDIDATE_FILES}], args.timeout_seconds)
        candidate_inputs = core_inputs + [str((targets["candidate"] / name).relative_to(ROOT))
                                           for name in CANDIDATE_FILES]
        stage = "independent_verifier"
        attestations[stage] = run_stage(control, targets, pinset_path, pinset_value,
            stage, VERIFIER, PINS["verifier"],
            [str(PYTHON), "-I", "-B", str(VERIFIER), *authorities,
             "--candidate-dir", str(targets["candidate"]),
             "--out-file", str(targets["verification"])], "30662906", VERIFIER_STATUS,
            candidate_inputs, [{"path": str(targets["verification"]), "kind": "file",
                "precondition": "ABSENT", "exact_inventory": None,
                "required_relative_files": []}], args.timeout_seconds)
        stage = "coherent_attacks"
        attestations[stage] = run_stage(control, targets, pinset_path, pinset_value,
            stage, ATTACKS, PINS["attacks"],
            [str(PYTHON), "-I", "-B", str(ATTACKS), "--python", str(PYTHON),
             "--expect-python-sha256", PINS["python"], "--verifier", str(VERIFIER),
             "--expect-verifier-sha256", PINS["verifier"],
             "--expect-harness-sha256", PINS["attacks"], *authorities,
             "--candidate-dir", str(targets["candidate"]),
             "--work-dir", str(targets["attack_work"]),
             "--result-file", str(targets["attacks"]),
             "--timeout-seconds", str(args.timeout_seconds)], "30662907", ATTACK_STATUS,
            candidate_inputs + [str(targets["verification"].relative_to(ROOT))],
            [{"path": str(targets["attack_work"]), "kind": "directory",
              "precondition": "ABSENT", "exact_inventory": None,
              "required_relative_files": []},
             {"path": str(targets["attacks"]), "kind": "file",
              "precondition": "ABSENT", "exact_inventory": None,
              "required_relative_files": []}], args.attack_timeout_seconds)
        result = document(targets["candidate"] / (PREFIX + "_result.json"), "result_sha256")
        verification = document(targets["verification"], "verification_sha256")
        attacks = document(targets["attacks"], "attacks_sha256")
        need(result.get("status") == PRODUCER_STATUS
             and verification.get("status") == VERIFIER_STATUS
             and attacks.get("status") == ATTACK_STATUS
             and attacks.get("attack_census") == {"required": 34, "rejected": 34, "accepted": 0}
             and result.get("formal_credit") == 0
             and verification.get("formal_credit") == 0
             and attacks.get("formal_credit") == 0, "core mathematical receipts")
        body = {"schema": CORE_SCHEMA, "status": CORE_STATUS,
                "completed_at_utc": now(), "unit_name": args.unit_name,
                "systemd_invocation_id": invocation,
                "pinset_file_sha256": file_sha(pinset_path),
                "pinset_object_sha256": pinset_value["pinset_sha256"],
                "source_pins": PINS,
                "C27R2_source_terminal": {"dir": args.c27r2_terminal_dir, **C27_PINS},
                "C28_source_terminal": {"dir": args.c28_terminal_dir, **c28pins},
                "adapter_verification_files": {
                    "C27R2": file_sha(targets["c27_adapter_verification"]),
                    "C28": file_sha(targets["c28_adapter_verification"])},
                "candidate_files": {name: file_sha(targets["candidate"] / name)
                                    for name in CANDIDATE_FILES},
                "result_object_sha256": result["result_sha256"],
                "verification_file_sha256": file_sha(targets["verification"]),
                "verification_object_sha256": verification["verification_sha256"],
                "attacks_file_sha256": file_sha(targets["attacks"]),
                "attacks_object_sha256": attacks["attacks_sha256"],
                "stage_run_attestation_objects": {
                    name: value["run_attestation_sha256"]
                    for name, value in sorted(attestations.items())},
                "dual_real_hash_seeds": ["30662905", "30662906"],
                "no_import_verifier": True, "coherent_attacks_rejected": 34,
                "formal_credit": 0, "manifest_authorized": False,
                "C29": "UNAUTHORIZED_PENDING_COLD_TOCTOU_RELEASE_ATTACKS_MANIFEST_OUTER_SEAL_TERMINAL_REPLAY",
                "Source_W": "UNCHANGED_BY_SOURCE_G_C29_V2_CORE",
                "D02": "BLOCKED_COMPOSITE", "D03": "UNAUTHORIZED",
                "D04": "NOT_MINTED", "Gate5": "10/18",
                "CM2": "NO-GO_FOR_CLAIM"}
        receipt = dict(body)
        receipt["core_receipt_sha256"] = digest(receipt)
        write_json(control / "core_receipt.json", receipt)
        write_once(control / "PASS.lock", b"PASS_C29_V2_DUAL_TERMINAL_SEED_CORE__ZERO_CREDIT\n")
        return receipt
    except BaseException as error:
        failure_body = {"schema": BASE + "gated-core-failure.v1",
                        "status": "FAILED_CLOSED_C29_V2_GATED_CORE__ZERO_CREDIT",
                        "stage": stage, "error": f"{type(error).__name__}:{error}",
                        "failed_at_utc": now(), "formal_credit": 0,
                        "manifest_authorized": False, "C29": "UNAUTHORIZED",
                        "CM2": "NO-GO_FOR_CLAIM"}
        failure = dict(failure_body)
        failure["failure_receipt_sha256"] = digest(failure)
        if not (control / "failure_receipt.json").exists():
            write_json(control / "failure_receipt.json", failure)
        if not (control / "FAILED.lock").exists():
            write_once(control / "FAILED.lock", b"FAILED_CLOSED_C29_V2_GATED_CORE\n")
        raise


def self_test() -> dict[str, Any]:
    test = paths("c29-v2-self-test-targets")
    need(len(test) == 16 and CANDIDATE_FILES == sorted(set(CANDIDATE_FILES))
         and all(valid_sha(value) for value in PINS.values()), "watcher fixture")
    return {"status": "PASS_C29_V2_GATED_CORE_WATCHER_TOPOLOGY_SELF_TEST",
            "formal_credit": 0, "C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM"}


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--self-test", action="store_true")
    value.add_argument("--preflight-only", action="store_true")
    for name in ("stem", "unit-name", "c27r2-terminal-dir", "c28-terminal-dir",
                 "expect-c28-root-sha256", "expect-c28-receipt-file-sha256",
                 "expect-c28-receipt-object-sha256",
                 "expect-c28-replay-file-sha256",
                 "expect-c28-replay-object-sha256",
                 "expect-c28-pass-lock-sha256", "expect-watcher-sha256"):
        value.add_argument("--" + name)
    value.add_argument("--timeout-seconds", type=int, default=21_600)
    value.add_argument("--attack-timeout-seconds", type=int, default=86_400)
    return value


def main() -> int:
    args = parser().parse_args()
    fields = ("stem", "unit_name", "c27r2_terminal_dir", "c28_terminal_dir",
              "expect_c28_root_sha256", "expect_c28_receipt_file_sha256",
              "expect_c28_receipt_object_sha256", "expect_c28_replay_file_sha256",
              "expect_c28_replay_object_sha256", "expect_c28_pass_lock_sha256",
              "expect_watcher_sha256")
    try:
        if args.self_test:
            need(not args.preflight_only
                 and all(getattr(args, field) is None for field in fields),
                 "self-test arguments")
            result = self_test()
        else:
            need(all(getattr(args, field) is not None for field in fields)
                 and 60 <= args.timeout_seconds <= 86_400
                 and 60 <= args.attack_timeout_seconds <= 86_400,
                 "all watcher arguments")
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
