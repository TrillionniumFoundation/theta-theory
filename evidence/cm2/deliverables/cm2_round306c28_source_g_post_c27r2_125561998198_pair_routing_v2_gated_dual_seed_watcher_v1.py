#!/usr/bin/env python3
"""Fail-closed C28-v2 adapter, dual-seed math-core, verifier and attack gate.

All predecessor hashes and every output location are supplied explicitly.
Preflight creates no path.  A real run first derives and independently checks
the non-legacy C27R2 terminal adapter, then runs two genuine hash seeds into
fresh candidate directories, independently verifies both, executes all 26
coherent attacks, and emits a zero-credit core receipt.  It never runs the
release chain, never mints C28, and never starts C29.
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
PYTHON = Path("/usr/bin/python3.12")
SOURCES = {
    "adapter_builder": ROOT / (
        "deliverables/cm2_round306c28_source_g_post_c27r2_125561998198_"
        "pair_routing_v2_authority_adapter_builder_v1.py"),
    "adapter_verifier": ROOT / (
        "deliverables/cm2_round306c28_source_g_post_c27r2_125561998198_"
        "pair_routing_v2_authority_adapter_independent_verifier_v1.py"),
    "producer": ROOT / (
        "deliverables/cm2_round306c28_source_g_post_c27r2_125561998198_"
        "pair_routing_v2_producer.py"),
    "independent_verifier": ROOT / (
        "deliverables/cm2_round306c28_source_g_post_c27r2_125561998198_"
        "pair_routing_v2_independent_verifier.py"),
    "coherent_attacks": ROOT / (
        "deliverables/cm2_round306c28_source_g_post_c27r2_125561998198_"
        "pair_routing_v2_coherent_attack_harness.py"),
    "transaction_runner": ROOT / (
        "deliverables/cm2_round306c28_source_g_post_c27r2_125561998198_"
        "pair_routing_v2_transaction_runner_v1.py"),
}
SOURCE_PINS = {
    "adapter_builder":
        "15dc2695345ad5ece0038797b3ccb0031b0c22b8aa06ed0730bf7c93aaf7fca0",
    "adapter_verifier":
        "23aea6fddc9dc64c3c5d598557f6d1f64d7689c11ee2d932da9938730427b90b",
    "producer":
        "364610cfa465601ac99fcd5ee3528ee5da791fcb5fb1c9ab27ff38966d211205",
    "independent_verifier":
        "7ca21d0e02f95afc1a8fc9635c3aa31bb290b8499f28860f8f8ae095b451cb04",
    "coherent_attacks":
        "5ec0a477cfa9a78f4c104135ae58c6d6115c8cafef70e3e52653095054bf59be",
    "transaction_runner":
        "d37ebb999f226d6af65338b9ccc5c40ace70de80bf1db32cd4e129740d740ae3",
    "python":
        "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118",
}
SPEC_SCHEMA = (
    "cm2.round306c28.source-g-post-c27r2-125561998198-pair-routing.v2."
    "process-command-spec.v1"
)
PINSET_SCHEMA = (
    "cm2.round306c28.source-g-post-c27r2-125561998198-pair-routing.v2."
    "gated-transaction-pinset.v1"
)
RUN_SCHEMA = (
    "cm2.round306c28.source-g-post-c27r2-125561998198-pair-routing.v2."
    "process-run-attestation.v1"
)
RUN_STATUS = (
    "PASS_PROCESS_TRANSACTION_EXIT0_NULL_SIGNAL_EMPTY_STDERR_PRE_POST_"
    "AND_OUTPUTS__ZERO_CREDIT"
)
ADAPTER_STATUS = (
    "PASS_ORIGINAL_C27R2_TERMINAL_RECEIPT_ROOT_PASS_AND_BYTE_REPLAY__"
    "NORMALIZED_C28_ADAPTER_ZERO_CREDIT"
)
ADAPTER_VERIFICATION_STATUS = (
    "PASS_NO_IMPORT_OR_EXEC_BUILDER__ORIGINAL_C27R2_TERMINAL_AND_"
    "NORMALIZED_C28_ADAPTER_INDEPENDENTLY_VERIFIED_ZERO_CREDIT"
)
RESULT_SCHEMA = (
    "cm2.round306c28.source-g-post-c27r2-125561998198-pair-routing.v2."
    "producer-result.v1"
)
RESULT_STATUS = (
    "PASS_POST_C27R2_PARTITION_502204_MEMBERS_43684_COMPONENTS_AND_"
    "32896_PAIR_SHARDS_REBUILT__125561998198_EXACT_NONEDGE_CANDIDATE_"
    "ZERO_CREDIT__C28_UNAUTHORIZED_PENDING_RELEASE_TERMINAL"
)
VERIFICATION_SCHEMA = (
    "cm2.round306c28.source-g-post-c27r2-125561998198-pair-routing.v2."
    "independent-verification.v1"
)
VERIFICATION_STATUS = (
    "PASS_NO_IMPORT_C27R2_TERMINAL_PARTITION_AND_32896_PAIR_SHARDS_"
    "INDEPENDENTLY_REBUILT__ZERO_CREDIT_PENDING_ATTACKS_AND_RELEASE_CHAIN"
)
ATTACK_SCHEMA = (
    "cm2.round306c28.source-g-post-c27r2-125561998198-pair-routing.v2."
    "coherent-attack-harness.v1"
)
ATTACK_STATUS = (
    "PASS_BASELINE_AND_26_OF_26_COHERENT_ATTACKS_REJECTED_FAIL_CLOSED__"
    "ZERO_CREDIT_PENDING_RELEASE_CHAIN"
)
CORE_SCHEMA = (
    "cm2.round306c28.source-g-post-c27r2-125561998198-pair-routing.v2."
    "gated-dual-seed-core-receipt.v1"
)
CORE_STATUS = (
    "PASS_C27R2_TERMINAL_ADAPTER_DUAL_TRUE_SEED_THREE_FILE_CANDIDATES_"
    "TWO_NO_IMPORT_VERIFIERS_AND_26_ATTACKS__ZERO_CREDIT_PENDING_RELEASE"
)
CORE_PASS = b"PASS_C28_PAIR_ROUTING_V2_DUAL_SEED_CORE__ZERO_CREDIT\n"
CANDIDATE_FILES = {
    "member_home_block_census.jsonl.gz",
    "cross_component_pair_route_shard.jsonl.gz", "result.json",
}
ADAPTER_FILES = {
    "authority_contract.json", "payload_manifest.sha256",
    "root_manifest.sha256", "terminal_receipt.json", "PASS.lock",
}
RUN_FILES = {
    "PASS.lock", "exit_code.txt", "input_post.json", "input_pre.json",
    "output_validation.json", "run_attestation.json", "runner_start.json",
    "signal.json", "stderr.log", "stdout.log", "timing.json",
}
EXPECTED = {
    "members": 502_204, "post_components": 43_684,
    "total_pairs": 126_104_177_706, "within_pairs": 542_179_508,
    "cross_pairs": 125_561_998_198, "blocks": 256, "shards": 32_896,
}


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
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                 | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular singleton:" + str(path))
        state = hashlib.sha256()
        while block := os.read(fd, 4 << 20):
            state.update(block)
        need(fingerprint(before) == fingerprint(os.fstat(fd)),
             "stable file:" + str(path))
        return state.hexdigest()
    finally:
        os.close(fd)


def document(path: Path, closure: str) -> dict[str, Any]:
    payload = path.read_bytes()
    need(payload.endswith(b"\n") and not payload.endswith(b"\n\n"),
         "JSON newline:" + str(path))
    value = strict_load(payload[:-1])
    need(type(value) is dict and canonical(value) == payload[:-1],
         "canonical JSON:" + str(path))
    body = dict(value)
    claim = body.pop(closure, None)
    need(valid_sha(claim) and claim == digest(body),
         "object closure:" + str(path))
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


def target_paths(args: argparse.Namespace) -> dict[str, Path]:
    names = (
        "control", "adapter", "adapter-verification", "adapter-run",
        "adapter-verifier-run", "seed1-candidate", "seed1-run",
        "seed2-candidate", "seed2-run", "verifier1-output",
        "verifier1-run", "verifier2-output", "verifier2-run",
        "attack-work", "attack-run",
    )
    result = {name.replace("-", "_"): Path(
        getattr(args, name.replace("-", "_") + "_dir")).absolute()
        for name in names}
    need(len(set(result.values())) == len(result)
         and all(path.parent == AUDIT and not path.exists()
                 and not path.is_symlink() for path in result.values()),
         "fifteen fresh distinct audit paths")
    return result


def clean_run(command: list[str], label: str,
              control: Path | None = None) -> bytes:
    completed = subprocess.run(
        command, cwd=ROOT,
        env={"PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
             "PYTHONHASHSEED": "30662800"},
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False)
    if control is not None:
        write_once(control / (label + ".stdout.log"), completed.stdout)
        write_once(control / (label + ".stderr.log"), completed.stderr)
        write_once(control / (label + ".exit_code.txt"),
                   (str(completed.returncode) + "\n").encode("ascii"))
    need(completed.returncode == 0 and completed.stderr == b""
         and completed.stdout.endswith(b"\n"), "clean process:" + label)
    value = strict_load(completed.stdout[:-1])
    need(type(value) is dict and canonical(value) == completed.stdout[:-1],
         "canonical stdout:" + label)
    return completed.stdout


def source_preflight(expect_self: str) -> dict[str, str]:
    need(valid_sha(expect_self) and file_sha(SELF) == expect_self,
         "watcher self pin")
    observed = {name: file_sha(path) for name, path in SOURCES.items()}
    observed["python"] = file_sha(PYTHON)
    need(observed == SOURCE_PINS, "all frozen source/Python pins")
    tests: dict[str, str] = {}
    for name, path in SOURCES.items():
        stdout = clean_run([str(PYTHON), "-I", "-B", str(path),
                            "--self-test"], name + "_selftest")
        tests[name] = hashlib.sha256(stdout).hexdigest()
    return tests


def predecessor_args(args: argparse.Namespace) -> list[str]:
    return [
        "--c27r2-terminal-dir", args.c27r2_terminal_dir,
        "--expect-terminal-root-sha256", args.expect_terminal_root_sha256,
        "--expect-terminal-receipt-file-sha256",
        args.expect_terminal_receipt_file_sha256,
        "--expect-terminal-receipt-object-sha256",
        args.expect_terminal_receipt_object_sha256,
        "--expect-terminal-replay-file-sha256",
        args.expect_terminal_replay_file_sha256,
        "--expect-terminal-replay-object-sha256",
        args.expect_terminal_replay_object_sha256,
        "--expect-terminal-pass-lock-sha256",
        args.expect_terminal_pass_lock_sha256,
    ]


def predecessor_files(args: argparse.Namespace) -> list[str]:
    terminal = Path(args.c27r2_terminal_dir).absolute()
    return sorted(str(terminal / name) for name in (
        "PASS.lock", "chain_status.json", "payload_manifest.sha256",
        "root_manifest.sha256", "terminal_receipt.json",
        "terminal_replay.json",
    ))


def command_spec(
    stage: str, source: Path, source_sha: str, argv: list[str], seed: str,
    timeout: int, input_paths: list[str], output_roots: list[dict[str, Any]],
    expected_status: str, pinset_path: Path, pinset: dict[str, Any],
) -> dict[str, Any]:
    body = {
        "schema": SPEC_SCHEMA, "stage": stage,
        "source_path": str(source), "source_sha256": source_sha,
        "argv": [str(PYTHON), "-I", "-B", str(source), *argv],
        "environment": {"PATH": "/usr/bin:/bin", "LANG": "C",
                        "LC_ALL": "C", "PYTHONHASHSEED": seed},
        "python_hash_seed": seed, "timeout_seconds": timeout,
        "input_paths": sorted(set(input_paths)),
        "output_roots": output_roots,
        "expected_stdout_status": expected_status,
        "pinset_file_sha256": file_sha(pinset_path),
        "pinset_object_sha256": pinset["pinset_sha256"],
        "runner_source_sha256": SOURCE_PINS["transaction_runner"],
        "python_sha256": SOURCE_PINS["python"],
        "formal_credit": 0, "manifest_authorized": False,
        "C28": "UNAUTHORIZED", "C29": "UNAUTHORIZED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    return {**body, "command_spec_sha256": digest(body)}


def output_dir(path: Path, files: list[str], *, existing: bool = False) \
        -> dict[str, Any]:
    return {"path": str(path), "kind": "directory",
            "precondition": ("EXISTING_EMPTY_DIRECTORY" if existing
                             else "ABSENT"),
            "exact_inventory": sorted(files),
            "required_relative_files": sorted(files)}


def output_dynamic_dir(path: Path, required: list[str]) -> dict[str, Any]:
    return {"path": str(path), "kind": "directory",
            "precondition": "ABSENT", "exact_inventory": None,
            "required_relative_files": sorted(required)}


def output_file(path: Path) -> dict[str, Any]:
    return {"path": str(path), "kind": "file", "precondition": "ABSENT",
            "exact_inventory": None, "required_relative_files": []}


def run_transaction(stage: str, spec_path: Path, pinset_path: Path,
                    run_dir: Path, control: Path) -> dict[str, Any]:
    stdout = clean_run([
        str(PYTHON), "-I", "-B", str(SOURCES["transaction_runner"]),
        "--stage", stage, "--command-spec", str(spec_path),
        "--pinset", str(pinset_path), "--run-dir", str(run_dir),
        "--expect-runner-sha256", SOURCE_PINS["transaction_runner"],
        "--expect-python-sha256", SOURCE_PINS["python"],
    ], stage + "_runner", control)
    need({entry.name for entry in run_dir.iterdir()} == RUN_FILES,
         "exact runner inventory:" + stage)
    need((run_dir / "exit_code.txt").read_bytes() == b"0\n"
         and (run_dir / "signal.json").read_bytes() == b"null\n"
         and (run_dir / "stderr.log").read_bytes() == b""
         and (run_dir / "input_pre.json").read_bytes()
             == (run_dir / "input_post.json").read_bytes(),
         "exact process closure:" + stage)
    receipt = document(run_dir / "run_attestation.json",
                       "run_attestation_sha256")
    need(receipt.get("schema") == RUN_SCHEMA
         and receipt.get("status") == RUN_STATUS
         and receipt.get("stage") == stage
         and receipt.get("numeric_exit_code") == 0
         and receipt.get("signal") is None
         and receipt.get("timed_out") is False
         and receipt.get("stderr_empty") is True
         and receipt.get("input_pre_post_sha_stat_identical") is True,
         "run attestation semantics:" + stage)
    need(hashlib.sha256(stdout).hexdigest()
         == file_sha(control / (stage + "_runner.stdout.log")),
         "runner stdout capture:" + stage)
    return receipt


def adapter_contract(adapter: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    contract = document(adapter / "authority_contract.json", "contract_sha256")
    receipt = document(adapter / "terminal_receipt.json",
                       "terminal_receipt_sha256")
    need({entry.name for entry in adapter.iterdir()} == ADAPTER_FILES
         and contract["terminal"]["root_manifest_sha256"]
             == file_sha(adapter / "root_manifest.sha256")
         and contract["terminal"]["receipt_file_sha256"]
             == file_sha(adapter / "terminal_receipt.json")
         and contract["terminal"]["receipt_object_sha256"]
             == receipt["terminal_receipt_sha256"],
         "adapter post-run closure")
    return contract, receipt


def exact_candidate(path: Path) -> dict[str, Any]:
    need(path.is_dir() and {entry.name for entry in path.iterdir()}
         == CANDIDATE_FILES, "exact three-file candidate")
    result = document(path / "result.json", "result_sha256")
    need(result.get("schema") == RESULT_SCHEMA
         and result.get("status") == RESULT_STATUS
         and result.get("post_C27R2_partition_census") == {
             "members": EXPECTED["members"],
             "components": EXPECTED["post_components"],
             "total_unordered_member_pairs": EXPECTED["total_pairs"],
             "within_post_component_member_pairs": EXPECTED["within_pairs"],
             "cross_post_component_member_pairs": EXPECTED["cross_pairs"],
         }
         and result.get("formal_credit") == 0
         and result.get("manifest_authorized") is False,
         "candidate exact math and zero-credit semantics")
    return result


def failure(control: Path, stage: str, error: BaseException) -> None:
    body = {"schema": CORE_SCHEMA + ".failure", "status":
            "FAILED_CLOSED_C28_CORE__ZERO_CREDIT", "stage": stage,
            "failed_at_utc": utc_now(),
            "error": f"{type(error).__name__}:{error}",
            "formal_credit": 0, "manifest_authorized": False,
            "C28": "UNAUTHORIZED", "C29": "UNAUTHORIZED",
            "CM2": "NO-GO_FOR_CLAIM"}
    value = {**body, "failure_receipt_sha256": digest(body)}
    if not (control / "failure_receipt.json").exists():
        write_json(control / "failure_receipt.json", value)
    if not (control / "FAILED.lock").exists():
        write_once(control / "FAILED.lock",
                   b"FAILED_CLOSED_C28_PAIR_ROUTING_V2_CORE\n")


def execute(args: argparse.Namespace) -> dict[str, Any]:
    pins = (
        args.expect_terminal_root_sha256,
        args.expect_terminal_receipt_file_sha256,
        args.expect_terminal_receipt_object_sha256,
        args.expect_terminal_replay_file_sha256,
        args.expect_terminal_replay_object_sha256,
        args.expect_terminal_pass_lock_sha256, args.expect_watcher_sha256,
    )
    need(all(valid_sha(value) for value in pins), "all dynamic pins")
    targets = target_paths(args)
    tests = source_preflight(args.expect_watcher_sha256)
    preflight_stdout = clean_run([
        str(PYTHON), "-I", "-B", str(SOURCES["adapter_builder"]),
        "--preflight-only", *predecessor_args(args),
        "--expect-builder-sha256", SOURCE_PINS["adapter_builder"],
        "--output-dir", str(targets["adapter"]),
    ], "adapter_preflight")
    need(all(not path.exists() for path in targets.values()),
         "preflight creates no transaction path")
    if args.preflight_only:
        return {"status":
                "PASS_C28_ALL_SOURCES_ORIGINAL_TERMINAL_AND_FIFTEEN_FRESH_"
                "PATHS_PREFLIGHT__NO_OUTPUT_CREATED_ZERO_CREDIT",
                "self_test_stdout_sha256": tests,
                "adapter_preflight_stdout_sha256":
                    hashlib.sha256(preflight_stdout).hexdigest()}
    control = targets["control"]
    stage = "create_control"
    try:
        control.mkdir(mode=0o700)
        pinset_body = {
            "schema": PINSET_SCHEMA,
            "status": "PASS_FROZEN_SOURCES_ORIGINAL_C27R2_TERMINAL_AND_FRESH_PATHS__ZERO_CREDIT",
            "predecessor": {
                "terminal_dir": args.c27r2_terminal_dir,
                "terminal_root_sha256": args.expect_terminal_root_sha256,
                "terminal_receipt_file_sha256":
                    args.expect_terminal_receipt_file_sha256,
                "terminal_receipt_object_sha256":
                    args.expect_terminal_receipt_object_sha256,
                "terminal_replay_file_sha256":
                    args.expect_terminal_replay_file_sha256,
                "terminal_replay_object_sha256":
                    args.expect_terminal_replay_object_sha256,
                "terminal_pass_lock_sha256":
                    args.expect_terminal_pass_lock_sha256,
            },
            "source_pins": {**SOURCE_PINS,
                            "watcher": args.expect_watcher_sha256},
            "self_test_stdout_sha256": tests,
            "targets": {name: str(path.relative_to(ROOT))
                        for name, path in targets.items()},
            "true_seeds": ["30662801", "30662802"],
            "formal_credit": 0, "manifest_authorized": False,
            "C27R2": "AUTHORIZED_PREDECESSOR_ONLY",
            "C28": "UNAUTHORIZED", "C29": "UNAUTHORIZED",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        pinset = {**pinset_body, "pinset_sha256": digest(pinset_body)}
        pinset_path = control / "pinset.json"
        write_json(pinset_path, pinset)
        terminal_files = predecessor_files(args)

        stage = "authority_adapter"
        spec = command_spec(
            stage, SOURCES["adapter_builder"], SOURCE_PINS["adapter_builder"],
            [*predecessor_args(args), "--expect-builder-sha256",
             SOURCE_PINS["adapter_builder"], "--output-dir",
             str(targets["adapter"])], "30662801", 3_600,
            terminal_files, output_dir(targets["adapter"],
                                       sorted(ADAPTER_FILES)),
            ADAPTER_STATUS, pinset_path, pinset)
        spec_path = control / "authority_adapter_command_spec.json"
        write_json(spec_path, spec)
        adapter_run = run_transaction(
            stage, spec_path, pinset_path, targets["adapter_run"], control)
        contract, adapter_receipt = adapter_contract(targets["adapter"])
        contract_file_sha = file_sha(
            targets["adapter"] / "authority_contract.json")
        contract_object_sha = contract["contract_sha256"]
        adapter_root_sha = file_sha(targets["adapter"] / "root_manifest.sha256")
        adapter_receipt_file_sha = file_sha(
            targets["adapter"] / "terminal_receipt.json")
        adapter_receipt_object_sha = adapter_receipt["terminal_receipt_sha256"]
        adapter_files = sorted(str(targets["adapter"] / name)
                               for name in ADAPTER_FILES)

        stage = "authority_adapter_verifier"
        spec = command_spec(
            stage, SOURCES["adapter_verifier"],
            SOURCE_PINS["adapter_verifier"],
            [*predecessor_args(args), "--expect-builder-sha256",
             SOURCE_PINS["adapter_builder"], "--expect-verifier-sha256",
             SOURCE_PINS["adapter_verifier"], "--adapter-dir",
             str(targets["adapter"]),
             "--expect-adapter-contract-file-sha256", contract_file_sha,
             "--expect-adapter-contract-object-sha256", contract_object_sha,
             "--output-dir", str(targets["adapter_verification"])],
            "30662802", 3_600,
            terminal_files + adapter_files + [str(SOURCES["adapter_builder"])],
            [output_dir(targets["adapter_verification"],
                        ["verification.json"])],
            ADAPTER_VERIFICATION_STATUS, pinset_path, pinset)
        spec_path = control / "authority_adapter_verifier_command_spec.json"
        write_json(spec_path, spec)
        adapter_verifier_run = run_transaction(
            stage, spec_path, pinset_path,
            targets["adapter_verifier_run"], control)
        adapter_verification = document(
            targets["adapter_verification"] / "verification.json",
            "verification_sha256")
        need(adapter_verification.get("status")
                 == ADAPTER_VERIFICATION_STATUS
             and adapter_verification.get("builder_imported_or_executed")
                 is False, "adapter independent verification")

        selected_paths = sorted(
            descriptor["path"] for descriptor in contract["payload"].values())
        math_inputs = adapter_files + [str(ROOT / path)
                                       for path in selected_paths]
        candidate_runs: list[dict[str, Any]] = []
        for label, seed, candidate_key, run_key in (
            ("seed1", "30662801", "seed1_candidate", "seed1_run"),
            ("seed2", "30662802", "seed2_candidate", "seed2_run"),
        ):
            stage = "producer"
            candidate = targets[candidate_key]
            spec = command_spec(
                stage, SOURCES["producer"], SOURCE_PINS["producer"], [
                    "--c27r2-terminal-dir", str(targets["adapter"]),
                    "--authority-contract",
                    str(targets["adapter"] / "authority_contract.json"),
                    "--expect-authority-contract-sha256", contract_file_sha,
                    "--expect-terminal-root-sha256", adapter_root_sha,
                    "--expect-terminal-receipt-file-sha256",
                    adapter_receipt_file_sha,
                    "--expect-terminal-receipt-object-sha256",
                    adapter_receipt_object_sha, "--out-dir", str(candidate),
                ], seed, 21_600, math_inputs,
                [output_dir(candidate, sorted(CANDIDATE_FILES))],
                RESULT_STATUS, pinset_path, pinset)
            spec_path = control / (label + "_producer_command_spec.json")
            write_json(spec_path, spec)
            candidate_runs.append(run_transaction(
                stage, spec_path, pinset_path, targets[run_key], control))
        seed1_result = exact_candidate(targets["seed1_candidate"])
        seed2_result = exact_candidate(targets["seed2_candidate"])
        agreement = {
            name: {
                "seed1_sha256": file_sha(targets["seed1_candidate"] / name),
                "seed2_sha256": file_sha(targets["seed2_candidate"] / name),
            } for name in sorted(CANDIDATE_FILES)
        }
        need(all(value["seed1_sha256"] == value["seed2_sha256"]
                 for value in agreement.values())
             and seed1_result == seed2_result,
             "dual true-seed candidate byte identity")
        write_json(control / "dual_seed_byte_agreement.json", agreement)

        verification_runs: list[dict[str, Any]] = []
        verification_values: list[dict[str, Any]] = []
        for label, seed, candidate_key, output_key, run_key in (
            ("seed1", "30662801", "seed1_candidate", "verifier1_output",
             "verifier1_run"),
            ("seed2", "30662802", "seed2_candidate", "verifier2_output",
             "verifier2_run"),
        ):
            stage = "independent_verifier"
            verification_dir = targets[output_key]
            verification_dir.mkdir(mode=0o700)
            out_file = verification_dir / "verification.json"
            candidate = targets[candidate_key]
            verifier_inputs = math_inputs + [str(SOURCES["producer"])] + [
                str(candidate / name) for name in sorted(CANDIDATE_FILES)]
            spec = command_spec(
                stage, SOURCES["independent_verifier"],
                SOURCE_PINS["independent_verifier"], [
                    "--c27r2-terminal-dir", str(targets["adapter"]),
                    "--authority-contract",
                    str(targets["adapter"] / "authority_contract.json"),
                    "--expect-authority-contract-sha256", contract_file_sha,
                    "--expect-terminal-root-sha256", adapter_root_sha,
                    "--expect-terminal-receipt-file-sha256",
                    adapter_receipt_file_sha,
                    "--expect-terminal-receipt-object-sha256",
                    adapter_receipt_object_sha, "--producer",
                    str(SOURCES["producer"]), "--expect-producer-sha256",
                    SOURCE_PINS["producer"], "--expect-verifier-sha256",
                    SOURCE_PINS["independent_verifier"], "--candidate-dir",
                    str(candidate), "--out-file", str(out_file),
                ], seed, 21_600, verifier_inputs,
                [output_dir(verification_dir, ["verification.json"],
                            existing=True)],
                VERIFICATION_STATUS, pinset_path, pinset)
            spec_path = control / (label + "_verifier_command_spec.json")
            write_json(spec_path, spec)
            verification_runs.append(run_transaction(
                stage, spec_path, pinset_path, targets[run_key], control))
            value = document(out_file, "verification_sha256")
            need(value.get("schema") == VERIFICATION_SCHEMA
                 and value.get("status") == VERIFICATION_STATUS
                 and value.get("independence", {}).get("producer_imported")
                     is False
                 and value.get("independence", {}).get("producer_executed")
                     is False
                 and value.get("verified_census") == {
                     "members": EXPECTED["members"],
                     "post_components": EXPECTED["post_components"],
                     "blocks": EXPECTED["blocks"],
                     "shards": EXPECTED["shards"],
                     "total_pairs": EXPECTED["total_pairs"],
                     "within_pairs": EXPECTED["within_pairs"],
                     "cross_pairs": EXPECTED["cross_pairs"],
                 }, "independent verifier exact result:" + label)
            verification_values.append(value)
        need(verification_values[0]["verified_census"]
                 == verification_values[1]["verified_census"]
             and verification_values[0]["candidate_result_sha256"]
                 == verification_values[1]["candidate_result_sha256"],
             "dual verifier semantic agreement")

        stage = "coherent_attacks"
        attack_result = control / "coherent_attacks.json"
        attack_inputs = math_inputs + [
            str(SOURCES["producer"]), str(SOURCES["independent_verifier"]),
            *[str(targets["seed1_candidate"] / name)
              for name in sorted(CANDIDATE_FILES)],
        ]
        spec = command_spec(
            stage, SOURCES["coherent_attacks"],
            SOURCE_PINS["coherent_attacks"], [
                "--c27r2-terminal-dir", str(targets["adapter"]),
                "--authority-contract",
                str(targets["adapter"] / "authority_contract.json"),
                "--expect-authority-contract-sha256", contract_file_sha,
                "--expect-terminal-root-sha256", adapter_root_sha,
                "--expect-terminal-receipt-file-sha256",
                adapter_receipt_file_sha,
                "--expect-terminal-receipt-object-sha256",
                adapter_receipt_object_sha, "--producer",
                str(SOURCES["producer"]), "--verifier",
                str(SOURCES["independent_verifier"]), "--python", str(PYTHON),
                "--expect-producer-sha256", SOURCE_PINS["producer"],
                "--expect-verifier-sha256",
                SOURCE_PINS["independent_verifier"],
                "--expect-harness-sha256", SOURCE_PINS["coherent_attacks"],
                "--expect-python-sha256", SOURCE_PINS["python"],
                "--candidate-dir", str(targets["seed1_candidate"]),
                "--work-dir", str(targets["attack_work"]),
                "--result-file", str(attack_result),
            ], "30662803", 21_600, attack_inputs,
            [output_dynamic_dir(targets["attack_work"],
                                ["baseline_verification.json"]),
             output_file(attack_result)], ATTACK_STATUS, pinset_path, pinset)
        spec_path = control / "coherent_attacks_command_spec.json"
        write_json(spec_path, spec)
        attack_run = run_transaction(
            stage, spec_path, pinset_path, targets["attack_run"], control)
        attacks = document(attack_result, "attack_receipt_sha256")
        need(attacks.get("schema") == ATTACK_SCHEMA
             and attacks.get("status") == ATTACK_STATUS
             and attacks.get("attack_census") == {
                 "planned": 26, "executed": 26,
                 "rejected_fail_closed": 26, "accepted": 0,
             } and attacks.get("formal_credit") == 0,
             "26/26 coherent attacks")
        body = {
            "schema": CORE_SCHEMA, "status": CORE_STATUS,
            "completed_at_utc": utc_now(),
            "predecessor_terminal_pins": pinset["predecessor"],
            "adapter_contract_file_sha256": contract_file_sha,
            "adapter_contract_object_sha256": contract_object_sha,
            "adapter_receipt_object_sha256": adapter_receipt_object_sha,
            "adapter_verification_object_sha256":
                adapter_verification["verification_sha256"],
            "dual_seed_candidate_file_agreement": agreement,
            "candidate_result_object_sha256": seed1_result["result_sha256"],
            "verifier_object_sha256": [
                value["verification_sha256"] for value in verification_values],
            "attack_receipt_object_sha256": attacks["attack_receipt_sha256"],
            "run_attestation_object_sha256": {
                "adapter": adapter_run["run_attestation_sha256"],
                "adapter_verifier":
                    adapter_verifier_run["run_attestation_sha256"],
                "producer_seed1": candidate_runs[0]["run_attestation_sha256"],
                "producer_seed2": candidate_runs[1]["run_attestation_sha256"],
                "verifier_seed1":
                    verification_runs[0]["run_attestation_sha256"],
                "verifier_seed2":
                    verification_runs[1]["run_attestation_sha256"],
                "coherent_attacks": attack_run["run_attestation_sha256"],
            },
            "exact_math": EXPECTED,
            "process_closures": {
                "all_seven_transactions_exit0_null_signal_empty_stderr": True,
                "all_declared_inputs_pre_post_SHA_stat_identical": True,
                "two_real_PYTHONHASHSEED_candidates_byte_identical": True,
                "two_no_import_verifiers_rebuilt_full_candidate": True,
                "all_26_coherent_attacks_rejected": True,
                "release_chain_created_or_started": False,
                "C29_created_or_started": False,
            },
            "formal_credit": 0, "manifest_authorized": False,
            "C27R2": "AUTHORIZED_PREDECESSOR_ONLY",
            "C28": "UNAUTHORIZED_PENDING_RELEASE_TERMINAL",
            "C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM",
        }
        receipt = {**body, "core_receipt_sha256": digest(body)}
        write_json(control / "core_receipt.json", receipt)
        write_once(control / "PASS.lock", CORE_PASS)
        return receipt
    except BaseException as error:
        if control.exists():
            failure(control, stage, error)
        raise


def self_test() -> dict[str, Any]:
    body = {"schema": CORE_SCHEMA, "status": CORE_STATUS,
            "exact_math": EXPECTED, "formal_credit": 0}
    need(digest(body) == hashlib.sha256(canonical(body)).hexdigest(),
         "watcher closure fixture")
    need(len(CANDIDATE_FILES) == 3 and len(ADAPTER_FILES) == 5,
         "inventory fixture")
    return {"status": "PASS_WATCHER_CLOSURE_AND_INVENTORY_FIXTURE",
            "formal_credit": 0, "CM2": "NO-GO_FOR_CLAIM"}


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--self-test", action="store_true")
    value.add_argument("--preflight-only", action="store_true")
    for name in (
        "c27r2-terminal-dir", "expect-terminal-root-sha256",
        "expect-terminal-receipt-file-sha256",
        "expect-terminal-receipt-object-sha256",
        "expect-terminal-replay-file-sha256",
        "expect-terminal-replay-object-sha256",
        "expect-terminal-pass-lock-sha256", "expect-watcher-sha256",
        "control-dir", "adapter-dir", "adapter-verification-dir",
        "adapter-run-dir", "adapter-verifier-run-dir",
        "seed1-candidate-dir", "seed1-run-dir", "seed2-candidate-dir",
        "seed2-run-dir", "verifier1-output-dir", "verifier1-run-dir",
        "verifier2-output-dir", "verifier2-run-dir", "attack-work-dir",
        "attack-run-dir",
    ):
        value.add_argument("--" + name)
    return value


def main() -> int:
    args = parser().parse_args()
    fields = tuple(name for name in vars(args) if name not in {
        "self_test", "preflight_only"})
    try:
        if args.self_test:
            need(not args.preflight_only
                 and all(getattr(args, field) is None for field in fields),
                 "self-test accepts no run arguments")
            result = self_test()
        else:
            need(all(getattr(args, field) is not None for field in fields),
                 "all predecessor pins, self pin, and fresh paths required")
            result = execute(args)
        sys.stdout.buffer.write(canonical({
            "CM2": "NO-GO_FOR_CLAIM", "formal_credit": 0,
            "status": result["status"],
        }) + b"\n")
        return 0
    except (Blocked, OSError, ValueError, KeyError, TypeError,
            subprocess.SubprocessError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
