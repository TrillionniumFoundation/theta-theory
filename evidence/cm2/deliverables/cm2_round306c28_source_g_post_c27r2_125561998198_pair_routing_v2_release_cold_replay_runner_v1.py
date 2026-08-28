#!/usr/bin/env python3
"""Run a fresh no-import cold replay of a terminal-pending C28-v2 core.

The core location and its receipt hashes are supplied at launch time.  Every
declared core member is held by the C28 transaction runner across the replay,
so SHA256 and the complete nine-field stat fingerprint must be unchanged.
The fresh verification is required to be byte-identical to the selected
formal verification.  This helper is conditional and cannot create a
manifest, seal, terminal receipt, or C28 authority.
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
PRODUCER = ROOT / (
    "deliverables/cm2_round306c28_source_g_post_c27r2_125561998198_"
    "pair_routing_v2_producer.py"
)
VERIFIER = ROOT / (
    "deliverables/cm2_round306c28_source_g_post_c27r2_125561998198_"
    "pair_routing_v2_independent_verifier.py"
)
RUNNER = ROOT / (
    "deliverables/cm2_round306c28_source_g_post_c27r2_125561998198_"
    "pair_routing_v2_transaction_runner_v1.py"
)
PREFIX = (
    "cm2.round306c28.source-g-post-c27r2-125561998198-pair-routing.v2."
)
CORE_SCHEMA = PREFIX + "gated-dual-seed-core-receipt.v1"
CORE_STATUS = (
    "PASS_C27R2_TERMINAL_ADAPTER_DUAL_TRUE_SEED_THREE_FILE_CANDIDATES_"
    "TWO_NO_IMPORT_VERIFIERS_AND_26_ATTACKS__ZERO_CREDIT_PENDING_RELEASE"
)
CORE_PASS = b"PASS_C28_PAIR_ROUTING_V2_DUAL_SEED_CORE__ZERO_CREDIT\n"
PINSET_SCHEMA = PREFIX + "gated-transaction-pinset.v1"
SPEC_SCHEMA = PREFIX + "process-command-spec.v1"
RUN_SCHEMA = PREFIX + "process-run-attestation.v1"
RUN_STATUS = (
    "PASS_PROCESS_TRANSACTION_EXIT0_NULL_SIGNAL_EMPTY_STDERR_PRE_POST_"
    "AND_OUTPUTS__ZERO_CREDIT"
)
VERIFICATION_SCHEMA = PREFIX + "independent-verification.v1"
VERIFICATION_STATUS = (
    "PASS_NO_IMPORT_C27R2_TERMINAL_PARTITION_AND_32896_PAIR_SHARDS_"
    "INDEPENDENTLY_REBUILT__ZERO_CREDIT_PENDING_ATTACKS_AND_RELEASE_CHAIN"
)
COLD_SCHEMA = PREFIX + "release-cold-replay-receipt.v1"
COLD_STATUS = (
    "PASS_FRESH_NO_IMPORT_C28_PAIR_ROUTING_COLD_BYTE_REPLAY_WITH_ALL_"
    "DECLARED_CORE_INPUT_PRE_POST_SHA_STAT__ZERO_CREDIT"
)
COLD_PASS = b"PASS_C28_PAIR_ROUTING_V2_RELEASE_COLD_REPLAY__ZERO_CREDIT\n"
CANDIDATE_FILES = {
    "member_home_block_census.jsonl.gz",
    "cross_component_pair_route_shard.jsonl.gz",
    "result.json",
}
EXPECTED = {
    "members": 502_204,
    "post_components": 43_684,
    "blocks": 256,
    "shards": 32_896,
    "total_pairs": 126_104_177_706,
    "within_pairs": 542_179_508,
    "cross_pairs": 125_561_998_198,
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


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns,
            value.st_uid, value.st_gid)


def file_sha(path: Path) -> str:
    absolute = path.absolute()
    need(absolute.resolve(strict=True) == absolute,
         "canonical file path:" + str(path))
    fd = os.open(absolute, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                 | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular singleton:" + str(path))
        state = hashlib.sha256()
        while block := os.read(fd, 4 << 20):
            state.update(block)
        need(fingerprint(before) == fingerprint(os.fstat(fd)),
             "stable SHA/stat:" + str(path))
        return state.hexdigest()
    finally:
        os.close(fd)


def strict_load(payload: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(type(key) is str and key not in result,
                 "unique JSON key:" + str(key))
            result[key] = value
        return result
    return json.loads(payload, object_pairs_hook=pairs,
                      parse_constant=lambda token: (_ for _ in ()).throw(
                          ValueError(token)))


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


def audit_path(raw: str, *, absent: bool = False) -> Path:
    path = Path(raw).absolute()
    need(path.parent == AUDIT, "direct audit child:" + str(path))
    if absent:
        need(not path.exists() and not path.is_symlink(),
             "fresh path:" + str(path))
    else:
        need(path.is_dir() and not path.is_symlink(),
             "existing audit directory:" + str(path))
    return path


def inventory(directories: list[Path]) -> list[str]:
    result: list[str] = []
    for directory in directories:
        need(directory.is_dir() and not directory.is_symlink(),
             "core directory:" + str(directory))
        for current, directory_names, file_names in os.walk(directory):
            base = Path(current)
            for name in directory_names:
                need(not (base / name).is_symlink(), "no core symlink dir")
            for name in file_names:
                path = base / name
                need(path.is_file() and not path.is_symlink(),
                     "regular core member:" + str(path))
                result.append(str(path.relative_to(ROOT)))
    need(result and len(result) == len(set(result)),
         "nonempty disjoint core inventory")
    return sorted(result)


def validate_core(args: argparse.Namespace) -> tuple[
        Path, Path, Path, dict[str, Any], dict[str, Any], list[str]]:
    control = audit_path(args.core_control_dir)
    adapter = audit_path(args.adapter_dir)
    candidate = audit_path(args.candidate_dir)
    formal = Path(args.formal_verification_file).absolute()
    need(formal.parent.parent == AUDIT and formal.is_file()
         and not formal.is_symlink(), "formal verification path")
    receipt_path = control / "core_receipt.json"
    receipt = document(receipt_path, "core_receipt_sha256")
    need(file_sha(receipt_path) == args.expect_core_receipt_file_sha256
         and receipt["core_receipt_sha256"]
             == args.expect_core_receipt_object_sha256
         and receipt.get("schema") == CORE_SCHEMA
         and receipt.get("status") == CORE_STATUS
         and receipt.get("exact_math") == EXPECTED
         and receipt.get("formal_credit") == 0
         and receipt.get("manifest_authorized") is False
         and receipt.get("C28") == "UNAUTHORIZED_PENDING_RELEASE_TERMINAL"
         and receipt.get("C29") == "UNAUTHORIZED"
         and receipt.get("CM2") == "NO-GO_FOR_CLAIM"
         and (control / "PASS.lock").read_bytes() == CORE_PASS
         and file_sha(control / "PASS.lock") == args.expect_core_pass_sha256
         and not (control / "FAILED.lock").exists(),
         "exact terminal-pending core boundary")
    need({entry.name for entry in candidate.iterdir()} == CANDIDATE_FILES,
         "exact candidate inventory")
    result = document(candidate / "result.json", "result_sha256")
    census = result.get("post_C27R2_partition_census")
    need(census == {
        "members": EXPECTED["members"],
        "components": EXPECTED["post_components"],
        "total_unordered_member_pairs": EXPECTED["total_pairs"],
        "within_post_component_member_pairs": EXPECTED["within_pairs"],
        "cross_post_component_member_pairs": EXPECTED["cross_pairs"],
    } and result.get("formal_credit") == 0
      and result.get("manifest_authorized") is False,
      "candidate math/zero credit")
    verification = document(formal, "verification_sha256")
    need(verification.get("schema") == VERIFICATION_SCHEMA
         and verification.get("status") == VERIFICATION_STATUS
         and verification.get("verified_census") == EXPECTED
         and verification.get("candidate_result_sha256")
             == result["result_sha256"]
         and verification.get("independence", {}).get("producer_imported")
             is False
         and verification.get("independence", {}).get("producer_executed")
             is False,
         "formal no-import verification")
    contract = document(adapter / "authority_contract.json", "contract_sha256")
    adapter_receipt = document(adapter / "terminal_receipt.json",
                               "terminal_receipt_sha256")
    need(contract.get("terminal", {}).get("root_manifest_sha256")
             == file_sha(adapter / "root_manifest.sha256")
         and contract.get("terminal", {}).get("receipt_file_sha256")
             == file_sha(adapter / "terminal_receipt.json")
         and contract.get("terminal", {}).get("receipt_object_sha256")
             == adapter_receipt["terminal_receipt_sha256"],
         "adapter contract closure")
    core_dirs = [audit_path(raw) for raw in args.core_dir]
    need(len(core_dirs) >= 4 and control in core_dirs and adapter in core_dirs
         and candidate in core_dirs and formal.parent in core_dirs,
         "declared core directories cover required authority")
    members = inventory(core_dirs)
    return control, adapter, candidate, contract, verification, members


def failure(control: Path, stage: str, error: BaseException) -> None:
    body = {
        "schema": PREFIX + "release-cold-replay-failure.v1",
        "status": "FAILED_CLOSED_C28_RELEASE_COLD_REPLAY__ZERO_CREDIT",
        "failed_at_utc": utc_now(), "stage": stage,
        "error": f"{type(error).__name__}:{error}",
        "formal_credit": 0, "manifest_authorized": False,
        "C28": "UNAUTHORIZED", "C29": "UNAUTHORIZED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    value = {**body, "failure_receipt_sha256": digest(body)}
    if not (control / "failure_receipt.json").exists():
        write_json(control / "failure_receipt.json", value)
    if not (control / "FAILED.lock").exists():
        write_once(control / "FAILED.lock",
                   b"FAILED_CLOSED_C28_RELEASE_COLD_REPLAY\n")


def execute(args: argparse.Namespace) -> dict[str, Any]:
    pins = (args.expect_core_receipt_file_sha256,
            args.expect_core_receipt_object_sha256,
            args.expect_core_pass_sha256, args.expect_helper_sha256,
            args.expect_producer_sha256, args.expect_verifier_sha256,
            args.expect_transaction_runner_sha256, args.expect_python_sha256)
    need(all(valid_sha(value) for value in pins), "all dynamic pins")
    need(file_sha(SELF) == args.expect_helper_sha256
         and file_sha(PRODUCER) == args.expect_producer_sha256
         and file_sha(VERIFIER) == args.expect_verifier_sha256
         and file_sha(RUNNER) == args.expect_transaction_runner_sha256
         and file_sha(PYTHON) == args.expect_python_sha256,
         "frozen helper/core source/Python pins")
    _, adapter, candidate, contract, formal_verification, members = \
        validate_core(args)
    control = audit_path(args.control_dir, absent=True)
    output = audit_path(args.output_dir, absent=True)
    run = audit_path(args.run_dir, absent=True)
    need(len({control, output, run}) == 3, "fresh distinct release paths")
    if args.preflight_only:
        return {"status":
                "PASS_C28_CORE_COLD_REPLAY_PREFLIGHT__NO_PATHS_CREATED_ZERO_CREDIT"}
    stage = "create_control"
    try:
        control.mkdir(mode=0o700)
        output.mkdir(mode=0o700)
        pinset_body = {
            "schema": PINSET_SCHEMA,
            "status": "PASS_C28_RELEASE_COLD_REPLAY_DYNAMIC_CORE_PINSET__ZERO_CREDIT",
            "core_receipt_file_sha256":
                args.expect_core_receipt_file_sha256,
            "core_receipt_object_sha256":
                args.expect_core_receipt_object_sha256,
            "core_pass_lock_sha256": args.expect_core_pass_sha256,
            "adapter_contract_file_sha256":
                file_sha(adapter / "authority_contract.json"),
            "source_pins": {
                "cold_replay_helper": args.expect_helper_sha256,
                "producer": args.expect_producer_sha256,
                "independent_verifier": args.expect_verifier_sha256,
                "transaction_runner": args.expect_transaction_runner_sha256,
                "python": args.expect_python_sha256,
            },
            "targets": {
                "control": str(control.relative_to(ROOT)),
                "output": str(output.relative_to(ROOT)),
                "run": str(run.relative_to(ROOT)),
            },
            "formal_credit": 0, "manifest_authorized": False,
            "C27R2": "AUTHORIZED_PREDECESSOR_ONLY",
            "C28": "UNAUTHORIZED", "C29": "UNAUTHORIZED",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        pinset = {**pinset_body, "pinset_sha256": digest(pinset_body)}
        pinset_path = control / "pinset.json"
        write_json(pinset_path, pinset)
        contract_file_sha = file_sha(adapter / "authority_contract.json")
        adapter_receipt = document(adapter / "terminal_receipt.json",
                                   "terminal_receipt_sha256")
        verification_path = output / "verification.json"
        argv = [
            str(PYTHON), "-I", "-B", str(VERIFIER),
            "--c27r2-terminal-dir", str(adapter),
            "--authority-contract", str(adapter / "authority_contract.json"),
            "--expect-authority-contract-sha256", contract_file_sha,
            "--expect-terminal-root-sha256",
            file_sha(adapter / "root_manifest.sha256"),
            "--expect-terminal-receipt-file-sha256",
            file_sha(adapter / "terminal_receipt.json"),
            "--expect-terminal-receipt-object-sha256",
            adapter_receipt["terminal_receipt_sha256"],
            "--producer", str(PRODUCER),
            "--expect-producer-sha256", args.expect_producer_sha256,
            "--expect-verifier-sha256", args.expect_verifier_sha256,
            "--candidate-dir", str(candidate),
            "--out-file", str(verification_path),
        ]
        inputs = sorted(set(members + [
            str(SELF.relative_to(ROOT)), str(PRODUCER.relative_to(ROOT)),
            str(VERIFIER.relative_to(ROOT)), str(RUNNER.relative_to(ROOT)),
        ]))
        spec_body = {
            "schema": SPEC_SCHEMA, "stage": "independent_verifier",
            "source_path": str(VERIFIER),
            "source_sha256": args.expect_verifier_sha256,
            "argv": argv,
            "environment": {"PATH": "/usr/bin:/bin", "LANG": "C",
                            "LC_ALL": "C", "PYTHONHASHSEED": "30662828"},
            "python_hash_seed": "30662828",
            "timeout_seconds": args.timeout_seconds,
            "input_paths": inputs,
            "output_roots": [{
                "path": str(output), "kind": "directory",
                "precondition": "EXISTING_EMPTY_DIRECTORY",
                "exact_inventory": ["verification.json"],
                "required_relative_files": ["verification.json"],
            }],
            "expected_stdout_status": VERIFICATION_STATUS,
            "pinset_file_sha256": file_sha(pinset_path),
            "pinset_object_sha256": pinset["pinset_sha256"],
            "runner_source_sha256": args.expect_transaction_runner_sha256,
            "python_sha256": args.expect_python_sha256,
            "formal_credit": 0, "manifest_authorized": False,
            "C28": "UNAUTHORIZED", "C29": "UNAUTHORIZED",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        spec = {**spec_body, "command_spec_sha256": digest(spec_body)}
        spec_path = control / "cold_command_spec.json"
        write_json(spec_path, spec)
        stage = "cold_no_import_verifier"
        completed = subprocess.run([
            str(PYTHON), "-I", "-B", str(RUNNER),
            "--stage", "independent_verifier",
            "--command-spec", str(spec_path), "--pinset", str(pinset_path),
            "--run-dir", str(run), "--expect-runner-sha256",
            args.expect_transaction_runner_sha256,
            "--expect-python-sha256", args.expect_python_sha256,
        ], cwd=ROOT, env={"PATH": "/usr/bin:/bin", "LANG": "C",
                          "LC_ALL": "C", "PYTHONHASHSEED": "30662829"},
           stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
           stderr=subprocess.PIPE, check=False)
        write_once(control / "runner.stdout.log", completed.stdout)
        write_once(control / "runner.stderr.log", completed.stderr)
        write_once(control / "runner.exit_code.txt",
                   (str(completed.returncode) + "\n").encode("ascii"))
        need(completed.returncode == 0 and completed.stderr == b"",
             "cold transaction clean exit")
        cold = document(verification_path, "verification_sha256")
        formal_path = Path(args.formal_verification_file).absolute()
        need(verification_path.read_bytes() == formal_path.read_bytes()
             and cold["verification_sha256"]
                 == formal_verification["verification_sha256"],
             "cold verification byte-identical to selected formal verifier")
        attestation = document(run / "run_attestation.json",
                               "run_attestation_sha256")
        need(attestation.get("schema") == RUN_SCHEMA
             and attestation.get("status") == RUN_STATUS
             and attestation.get("stage") == "independent_verifier"
             and attestation.get("numeric_exit_code") == 0
             and attestation.get("signal") is None
             and attestation.get("timed_out") is False
             and attestation.get("stderr_empty") is True
             and attestation.get("input_pre_post_sha_stat_identical") is True
             and (run / "input_pre.json").read_bytes()
                 == (run / "input_post.json").read_bytes(),
             "cold transaction attestation")
        body = {
            "schema": COLD_SCHEMA, "status": COLD_STATUS,
            "completed_at_utc": utc_now(),
            "core_receipt_file_sha256":
                args.expect_core_receipt_file_sha256,
            "core_receipt_object_sha256":
                args.expect_core_receipt_object_sha256,
            "core_pass_lock_sha256": args.expect_core_pass_sha256,
            "formal_verification_file_sha256": file_sha(formal_path),
            "formal_verification_object_sha256":
                formal_verification["verification_sha256"],
            "cold_verification_file_sha256": file_sha(verification_path),
            "cold_verification_object_sha256": cold["verification_sha256"],
            "cold_replay_byte_identical": True,
            "run_attestation_file_sha256":
                file_sha(run / "run_attestation.json"),
            "run_attestation_object_sha256":
                attestation["run_attestation_sha256"],
            "numeric_exit_code": 0, "signal": None,
            "stderr_empty": True,
            "all_declared_core_inputs_pre_post_sha_stat_identical": True,
            "declared_core_input_count": len(inputs),
            "formal_credit": 0, "manifest_authorized": False,
            "C27R2": "AUTHORIZED_PREDECESSOR_ONLY",
            "C28": "UNAUTHORIZED_PENDING_RELEASE_ATTACKS_MANIFEST_OUTER_AND_TERMINAL_REPLAY",
            "C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM",
        }
        receipt = {**body, "cold_replay_receipt_sha256": digest(body)}
        write_json(control / "cold_replay_receipt.json", receipt)
        write_once(control / "PASS.lock", COLD_PASS)
        return receipt
    except BaseException as error:
        if control.exists():
            failure(control, stage, error)
        raise


def self_test() -> dict[str, Any]:
    body = {"schema": COLD_SCHEMA, "status": COLD_STATUS,
            "exact_math": EXPECTED, "formal_credit": 0}
    need(digest(body) == hashlib.sha256(canonical(body)).hexdigest()
         and len(CANDIDATE_FILES) == 3,
         "cold replay closure/inventory fixture")
    return {"status": "PASS_C28_RELEASE_COLD_REPLAY_FIXTURE"}


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--self-test", action="store_true")
    value.add_argument("--preflight-only", action="store_true")
    for name in (
        "core-control-dir", "adapter-dir", "candidate-dir",
        "formal-verification-file", "control-dir", "output-dir", "run-dir",
        "expect-core-receipt-file-sha256",
        "expect-core-receipt-object-sha256", "expect-core-pass-sha256",
        "expect-helper-sha256", "expect-producer-sha256",
        "expect-verifier-sha256", "expect-transaction-runner-sha256",
        "expect-python-sha256",
    ):
        value.add_argument("--" + name)
    value.add_argument("--core-dir", action="append")
    value.add_argument("--timeout-seconds", type=int, default=21_600)
    return value


def main() -> int:
    args = parser().parse_args()
    fields = (
        "core_control_dir", "adapter_dir", "candidate_dir",
        "formal_verification_file", "control_dir", "output_dir", "run_dir",
        "expect_core_receipt_file_sha256",
        "expect_core_receipt_object_sha256", "expect_core_pass_sha256",
        "expect_helper_sha256", "expect_producer_sha256",
        "expect_verifier_sha256", "expect_transaction_runner_sha256",
        "expect_python_sha256",
    )
    try:
        if args.self_test:
            need(not args.preflight_only and args.core_dir is None
                 and all(getattr(args, field) is None for field in fields),
                 "self-test accepts no run arguments")
            result = self_test()
        else:
            need(args.core_dir is not None
                 and all(getattr(args, field) is not None for field in fields)
                 and 60 <= args.timeout_seconds <= 86_400,
                 "all run arguments and bounded timeout")
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
