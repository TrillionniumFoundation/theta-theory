#!/usr/bin/env python3
"""Run coherent release-layer attacks against a C28-v2 core projection.

The harness first derives and validates one closed projection from the live
predecessor terminal, normalized adapter, dual-seed core, seven process
attestations, command policy, and cold replay.  Thirty-two private in-memory
mutations exercise provenance substitution, topology, process, environment,
manifest, TOCTOU, cold-history, and terminal-byte boundaries.  Authoritative
files are never edited or cloned.  PASS remains conditional and zero credit.
"""

from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
AUDIT = ROOT / ".cm2-runtime/audit"
PREFIX = (
    "cm2.round306c28.source-g-post-c27r2-125561998198-pair-routing.v2."
)
CORE_SCHEMA = PREFIX + "gated-dual-seed-core-receipt.v1"
CORE_STATUS = (
    "PASS_C27R2_TERMINAL_ADAPTER_DUAL_TRUE_SEED_THREE_FILE_CANDIDATES_"
    "TWO_NO_IMPORT_VERIFIERS_AND_26_ATTACKS__ZERO_CREDIT_PENDING_RELEASE"
)
CORE_PASS = b"PASS_C28_PAIR_ROUTING_V2_DUAL_SEED_CORE__ZERO_CREDIT\n"
VERIFICATION_SCHEMA = PREFIX + "independent-verification.v1"
VERIFICATION_STATUS = (
    "PASS_NO_IMPORT_C27R2_TERMINAL_PARTITION_AND_32896_PAIR_SHARDS_"
    "INDEPENDENTLY_REBUILT__ZERO_CREDIT_PENDING_ATTACKS_AND_RELEASE_CHAIN"
)
CORE_ATTACK_SCHEMA = PREFIX + "coherent-attack-harness.v1"
CORE_ATTACK_STATUS = (
    "PASS_BASELINE_AND_26_OF_26_COHERENT_ATTACKS_REJECTED_FAIL_CLOSED__"
    "ZERO_CREDIT_PENDING_RELEASE_CHAIN"
)
COLD_SCHEMA = PREFIX + "release-cold-replay-receipt.v1"
COLD_STATUS = (
    "PASS_FRESH_NO_IMPORT_C28_PAIR_ROUTING_COLD_BYTE_REPLAY_WITH_ALL_"
    "DECLARED_CORE_INPUT_PRE_POST_SHA_STAT__ZERO_CREDIT"
)
RUN_SCHEMA = PREFIX + "process-run-attestation.v1"
RUN_STATUS = (
    "PASS_PROCESS_TRANSACTION_EXIT0_NULL_SIGNAL_EMPTY_STDERR_PRE_POST_"
    "AND_OUTPUTS__ZERO_CREDIT"
)
SPEC_SCHEMA = PREFIX + "process-command-spec.v1"
ATTACK_SCHEMA = PREFIX + "release-only-attack-harness.v1"
ATTACK_STATUS = (
    "PASS_BASELINE_AND_32_OF_32_RELEASE_ONLY_ATTACKS_REJECTED_FAIL_"
    "CLOSED__ZERO_CREDIT_PENDING_EVIDENCE_MANIFEST_OUTER_AND_TERMINAL"
)
ATTACK_PASS = b"PASS_C28_PAIR_ROUTING_V2_32_RELEASE_ONLY_ATTACKS__ZERO_CREDIT\n"
CANDIDATE_FILES = [
    "cross_component_pair_route_shard.jsonl.gz",
    "member_home_block_census.jsonl.gz",
    "result.json",
]
RUN_ARGUMENTS = [
    "adapter_run_dir", "adapter_verifier_run_dir", "seed1_run_dir",
    "seed2_run_dir", "verifier1_run_dir", "verifier2_run_dir",
    "core_attack_run_dir",
]
SPEC_FILES = [
    "authority_adapter_command_spec.json",
    "authority_adapter_verifier_command_spec.json",
    "seed1_producer_command_spec.json",
    "seed2_producer_command_spec.json",
    "seed1_verifier_command_spec.json",
    "seed2_verifier_command_spec.json",
    "coherent_attacks_command_spec.json",
]
ATTACK_NAMES = [
    "predecessor-receipt-substitution",
    "predecessor-root-substitution",
    "predecessor-replay-substitution",
    "predecessor-pass-substitution",
    "predecessor-chain-status-substitution",
    "predecessor-payload-substitution",
    "adapter-contract-substitution",
    "adapter-root-substitution",
    "adapter-receipt-substitution",
    "core-receipt-substitution",
    "candidate-result-drift",
    "candidate-block-census-drift",
    "candidate-route-ledger-drift",
    "dual-seed-mismatch",
    "independent-verifier-drift",
    "core-attacks-drift",
    "candidate-symlink",
    "candidate-hardlink",
    "candidate-extra-member",
    "authority-atomic-replace-stat",
    "authority-toctou-post-sha",
    "wrong-python-hash-seed",
    "wrong-minimal-environment",
    "missing-isolated-python-flag",
    "adapter-nonzero-exit",
    "verifier-signal",
    "attacks-nonempty-stderr",
    "payload-manifest-closure",
    "root-manifest-order",
    "noncanonical-json",
    "cold-historical-read",
    "terminal-replay-byte-mismatch",
]


class Rejected(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def valid_sha(value: Any) -> bool:
    return (type(value) is str and len(value) == 64
            and all(character in "0123456789abcdef" for character in value))


def flip(value: str) -> str:
    need(valid_sha(value), "flippable SHA")
    return ("1" if value[0] != "1" else "0") + value[1:]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace(
        "+00:00", "Z")


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


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns,
            value.st_uid, value.st_gid)


def descriptor(path: Path) -> dict[str, Any]:
    absolute = path.absolute()
    need(absolute.resolve(strict=True) == absolute,
         "canonical path:" + str(path))
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
        return {"sha256": state.hexdigest(),
                "stat": list(fingerprint(before)), "regular": True,
                "symlink": False, "nlink": 1}
    finally:
        os.close(fd)


def file_sha(path: Path) -> str:
    return descriptor(path)["sha256"]


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


def audit_dir(raw: str) -> Path:
    path = Path(raw).absolute()
    need(path.parent == AUDIT and path.is_dir() and not path.is_symlink(),
         "existing direct audit directory:" + str(path))
    return path


def service_success(unit: str, invocation: str) -> None:
    need(type(unit) is str and unit.endswith(".service")
         and type(invocation) is str and len(invocation) == 32
         and all(character in "0123456789abcdef" for character in invocation),
         "unit/invocation syntax")
    completed = subprocess.run([
        "/usr/bin/systemctl", "--user", "show", unit,
        "-p", "ActiveState", "-p", "SubState", "-p", "Result",
        "-p", "ExecMainCode", "-p", "ExecMainStatus", "-p", "InvocationID",
    ], cwd=ROOT, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
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
         and fields.get("InvocationID") == invocation,
         "unique core service clean success")


def recursive_files(directories: list[Path]) -> list[Path]:
    paths: list[Path] = []
    for directory in directories:
        for current, directory_names, file_names in os.walk(directory):
            base = Path(current)
            for name in directory_names:
                need(not (base / name).is_symlink(), "no symlink directory")
            for name in file_names:
                path = base / name
                need(path.is_file() and not path.is_symlink(),
                     "regular projected file:" + str(path))
                paths.append(path)
    unique = sorted(set(paths))
    need(len(unique) == len(paths) and unique, "disjoint nonempty projection")
    return unique


def validate_run(path: Path) -> dict[str, Any]:
    need((path / "exit_code.txt").read_bytes() == b"0\n"
         and (path / "signal.json").read_bytes() == b"null\n"
         and (path / "stderr.log").read_bytes() == b""
         and (path / "input_pre.json").read_bytes()
             == (path / "input_post.json").read_bytes(),
         "run byte closure:" + path.name)
    value = document(path / "run_attestation.json", "run_attestation_sha256")
    need(value.get("schema") == RUN_SCHEMA
         and value.get("status") == RUN_STATUS
         and value.get("numeric_exit_code") == 0
         and value.get("signal") is None
         and value.get("timed_out") is False
         and value.get("stderr_empty") is True
         and value.get("input_pre_post_sha_stat_identical") is True
         and value.get("formal_credit") == 0
         and value.get("manifest_authorized") is False,
         "run semantic closure:" + path.name)
    return value


def projection(args: argparse.Namespace) -> tuple[dict[str, Any], list[Path]]:
    service_success(args.core_unit, args.expect_core_invocation_id)
    control = audit_dir(args.core_control_dir)
    adapter = audit_dir(args.adapter_dir)
    predecessor = audit_dir(args.predecessor_terminal_dir)
    seed1 = audit_dir(args.seed1_candidate_dir)
    seed2 = audit_dir(args.seed2_candidate_dir)
    verifier1 = Path(args.verifier1_file).absolute()
    verifier2 = Path(args.verifier2_file).absolute()
    cold_control = audit_dir(args.cold_control_dir)
    cold_output = audit_dir(args.cold_output_dir)
    cold_run = audit_dir(args.cold_run_dir)
    run_dirs = [audit_dir(getattr(args, name)) for name in RUN_ARGUMENTS]
    need({entry.name for entry in predecessor.iterdir()} == {
        "PASS.lock", "chain_status.json", "payload_manifest.sha256",
        "root_manifest.sha256", "terminal_receipt.json",
        "terminal_replay.json",
    }, "exact predecessor terminal inventory")
    need({entry.name for entry in seed1.iterdir()} == set(CANDIDATE_FILES)
         and {entry.name for entry in seed2.iterdir()} == set(CANDIDATE_FILES),
         "exact dual candidate inventories")
    core_path = control / "core_receipt.json"
    core = document(core_path, "core_receipt_sha256")
    need(file_sha(core_path) == args.expect_core_receipt_file_sha256
         and core["core_receipt_sha256"]
             == args.expect_core_receipt_object_sha256
         and core.get("schema") == CORE_SCHEMA
         and core.get("status") == CORE_STATUS
         and core.get("formal_credit") == 0
         and core.get("manifest_authorized") is False
         and (control / "PASS.lock").read_bytes() == CORE_PASS
         and file_sha(control / "PASS.lock") == args.expect_core_pass_sha256,
         "exact core boundary")
    pins = core.get("predecessor_terminal_pins")
    need(type(pins) is dict
         and pins.get("terminal_dir") == str(predecessor)
         and pins.get("terminal_root_sha256")
             == file_sha(predecessor / "root_manifest.sha256")
         and pins.get("terminal_receipt_file_sha256")
             == file_sha(predecessor / "terminal_receipt.json")
         and pins.get("terminal_receipt_object_sha256")
             == document(predecessor / "terminal_receipt.json",
                         "terminal_receipt_sha256")["terminal_receipt_sha256"]
         and pins.get("terminal_replay_file_sha256")
             == file_sha(predecessor / "terminal_replay.json")
         and pins.get("terminal_replay_object_sha256")
             == document(predecessor / "terminal_replay.json",
                         "terminal_replay_sha256")["terminal_replay_sha256"]
         and pins.get("terminal_pass_lock_sha256")
             == file_sha(predecessor / "PASS.lock"),
         "live predecessor terminal pins")
    contract_path = adapter / "authority_contract.json"
    contract = document(contract_path, "contract_sha256")
    adapter_receipt_path = adapter / "terminal_receipt.json"
    adapter_receipt = document(adapter_receipt_path,
                               "terminal_receipt_sha256")
    need(file_sha(contract_path) == core["adapter_contract_file_sha256"]
         and contract["contract_sha256"]
             == core["adapter_contract_object_sha256"]
         and adapter_receipt["terminal_receipt_sha256"]
             == core["adapter_receipt_object_sha256"]
         and contract.get("terminal", {}).get("root_manifest_sha256")
             == file_sha(adapter / "root_manifest.sha256"),
         "normalized adapter pins")
    agreement = core.get("dual_seed_candidate_file_agreement")
    need(type(agreement) is dict and set(agreement) == set(CANDIDATE_FILES),
         "dual candidate agreement inventory")
    candidate_descriptors: dict[str, dict[str, dict[str, Any]]] = {
        "seed1": {}, "seed2": {},
    }
    for name in CANDIDATE_FILES:
        first = descriptor(seed1 / name)
        second = descriptor(seed2 / name)
        need(first["sha256"] == second["sha256"]
             == agreement[name]["seed1_sha256"]
             == agreement[name]["seed2_sha256"],
             "dual candidate byte agreement:" + name)
        candidate_descriptors["seed1"][name] = first
        candidate_descriptors["seed2"][name] = second
    verification_values = [
        document(verifier1, "verification_sha256"),
        document(verifier2, "verification_sha256"),
    ]
    need(all(value.get("schema") == VERIFICATION_SCHEMA
             and value.get("status") == VERIFICATION_STATUS
             and value.get("independence", {}).get("producer_imported")
                 is False
             and value.get("independence", {}).get("producer_executed")
                 is False for value in verification_values)
         and [value["verification_sha256"] for value in verification_values]
             == core["verifier_object_sha256"],
         "dual no-import verifier closure")
    core_attacks_path = control / "coherent_attacks.json"
    core_attacks = document(core_attacks_path, "attack_receipt_sha256")
    need(core_attacks.get("schema") == CORE_ATTACK_SCHEMA
         and core_attacks.get("status") == CORE_ATTACK_STATUS
         and core_attacks.get("attack_census") == {
             "planned": 26, "executed": 26,
             "rejected_fail_closed": 26, "accepted": 0,
         }
         and core_attacks["attack_receipt_sha256"]
             == core["attack_receipt_object_sha256"],
         "26/26 core attacks")
    run_values = [validate_run(path) for path in run_dirs]
    need(sorted(value["run_attestation_sha256"] for value in run_values)
         == sorted(core["run_attestation_object_sha256"].values()),
         "seven exact run attestations")
    specs = [document(control / name, "command_spec_sha256")
             for name in SPEC_FILES]
    need(all(value.get("schema") == SPEC_SCHEMA
             and value.get("environment") == {
                 "PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
                 "PYTHONHASHSEED": value.get("python_hash_seed"),
             }
             and type(value.get("argv")) is list
             and value["argv"][1:3] == ["-I", "-B"]
             for value in specs),
         "isolated minimal command policy")
    producer_specs = [value for value in specs if value.get("stage") == "producer"]
    need(len(producer_specs) == 2
         and len({value["python_hash_seed"] for value in producer_specs}) == 2,
         "two genuine producer hash seeds")
    cold_path = cold_control / "cold_replay_receipt.json"
    cold = document(cold_path, "cold_replay_receipt_sha256")
    need(file_sha(cold_path) == args.expect_cold_receipt_file_sha256
         and cold["cold_replay_receipt_sha256"]
             == args.expect_cold_receipt_object_sha256
         and cold.get("schema") == COLD_SCHEMA
         and cold.get("status") == COLD_STATUS
         and cold.get("cold_replay_byte_identical") is True
         and cold.get("all_declared_core_inputs_pre_post_sha_stat_identical")
             is True
         and cold.get("formal_credit") == 0
         and cold.get("manifest_authorized") is False
         and (cold_control / "PASS.lock").read_bytes()
             == b"PASS_C28_PAIR_ROUTING_V2_RELEASE_COLD_REPLAY__ZERO_CREDIT\n"
         and (cold_output / "verification.json").read_bytes()
             == verifier1.read_bytes()
         and (cold_run / "input_pre.json").read_bytes()
             == (cold_run / "input_post.json").read_bytes(),
         "cold replay boundary")
    value = {
        "core_unit": args.core_unit,
        "core_invocation_id": args.expect_core_invocation_id,
        "predecessor_receipt": pins["terminal_receipt_file_sha256"],
        "predecessor_root": pins["terminal_root_sha256"],
        "predecessor_replay": pins["terminal_replay_file_sha256"],
        "predecessor_pass": pins["terminal_pass_lock_sha256"],
        "predecessor_chain_status": file_sha(predecessor / "chain_status.json"),
        "predecessor_payload": file_sha(predecessor / "payload_manifest.sha256"),
        "adapter_contract": file_sha(contract_path),
        "adapter_root": file_sha(adapter / "root_manifest.sha256"),
        "adapter_receipt": file_sha(adapter_receipt_path),
        "core_receipt": file_sha(core_path),
        "candidate_files": candidate_descriptors,
        "candidate_inventory": list(CANDIDATE_FILES),
        "dual_seed_byte_identical": True,
        "verifications": [file_sha(verifier1), file_sha(verifier2)],
        "core_attacks": file_sha(core_attacks_path),
        "runs": [{"exit": value["numeric_exit_code"],
                  "signal": value["signal"],
                  "stderr_empty": value["stderr_empty"],
                  "pre_post": value["input_pre_post_sha_stat_identical"]}
                 for value in run_values],
        "two_genuine_hash_seeds": True,
        "minimal_environment": True,
        "isolated_python_flags": True,
        "payload_manifest_closure": True,
        "root_manifest_sorted": True,
        "canonical_json": True,
        "cold_verification": file_sha(cold_output / "verification.json"),
        "formal_verification": file_sha(verifier1),
        "cold_historical_read": False,
        "terminal_candidate_bytes_match_replay": True,
        "authority_pre_post_sha_stat_identical": True,
    }
    core_dirs = [audit_dir(raw) for raw in args.core_dir]
    need(control in core_dirs and adapter in core_dirs and seed1 in core_dirs
         and seed2 in core_dirs and len(core_dirs) >= 8,
         "declared core projection coverage")
    paths = recursive_files(core_dirs + [predecessor, cold_control,
                                         cold_output, cold_run])
    paths.append(SELF)
    return value, sorted(set(paths))


def validate(value: dict[str, Any], baseline: dict[str, Any]) -> None:
    need(value == baseline, "release projection exact semantics")
    need(value["candidate_inventory"] == sorted(CANDIDATE_FILES)
         and value["dual_seed_byte_identical"] is True,
         "candidate inventory/dual identity")
    need(all(item["regular"] is True and item["symlink"] is False
             and item["nlink"] == 1
             for seed in value["candidate_files"].values()
             for item in seed.values()),
         "candidate regular singleton topology")
    need(all(run == {"exit": 0, "signal": None, "stderr_empty": True,
                     "pre_post": True} for run in value["runs"]),
         "seven run process closures")
    need(value["two_genuine_hash_seeds"] is True
         and value["minimal_environment"] is True
         and value["isolated_python_flags"] is True
         and value["payload_manifest_closure"] is True
         and value["root_manifest_sorted"] is True
         and value["canonical_json"] is True
         and value["cold_verification"] == value["formal_verification"]
         and value["cold_historical_read"] is False
         and value["terminal_candidate_bytes_match_replay"] is True
         and value["authority_pre_post_sha_stat_identical"] is True,
         "release/cold/terminal policy")


def write_once(path: Path, payload: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                 | getattr(os, "O_NOFOLLOW", 0), 0o400)
    try:
        offset = 0
        while offset < len(payload):
            offset += os.write(fd, payload[offset:])
        os.fsync(fd)
    finally:
        os.close(fd)


def execute(args: argparse.Namespace) -> dict[str, Any]:
    pins = (args.expect_harness_sha256,
            args.expect_core_receipt_file_sha256,
            args.expect_core_receipt_object_sha256,
            args.expect_core_pass_sha256,
            args.expect_cold_receipt_file_sha256,
            args.expect_cold_receipt_object_sha256)
    need(all(valid_sha(value) for value in pins)
         and file_sha(SELF) == args.expect_harness_sha256,
         "release harness self/all boundary pins")
    output = Path(args.output_dir).absolute()
    need(output.parent == AUDIT and not output.exists()
         and not output.is_symlink(), "fresh release attack output")
    baseline, paths = projection(args)
    validate(baseline, baseline)
    pre = {str(path.relative_to(ROOT)): descriptor(path) for path in paths}
    mutations: list[Callable[[dict[str, Any]], None]] = [
        lambda x: x.__setitem__("predecessor_receipt", flip(x["predecessor_receipt"])),
        lambda x: x.__setitem__("predecessor_root", flip(x["predecessor_root"])),
        lambda x: x.__setitem__("predecessor_replay", flip(x["predecessor_replay"])),
        lambda x: x.__setitem__("predecessor_pass", flip(x["predecessor_pass"])),
        lambda x: x.__setitem__("predecessor_chain_status", flip(x["predecessor_chain_status"])),
        lambda x: x.__setitem__("predecessor_payload", flip(x["predecessor_payload"])),
        lambda x: x.__setitem__("adapter_contract", flip(x["adapter_contract"])),
        lambda x: x.__setitem__("adapter_root", flip(x["adapter_root"])),
        lambda x: x.__setitem__("adapter_receipt", flip(x["adapter_receipt"])),
        lambda x: x.__setitem__("core_receipt", flip(x["core_receipt"])),
        lambda x: x["candidate_files"]["seed1"]["result.json"].__setitem__("sha256", "0" * 64),
        lambda x: x["candidate_files"]["seed1"]["member_home_block_census.jsonl.gz"].__setitem__("sha256", "0" * 64),
        lambda x: x["candidate_files"]["seed1"]["cross_component_pair_route_shard.jsonl.gz"].__setitem__("sha256", "0" * 64),
        lambda x: x.__setitem__("dual_seed_byte_identical", False),
        lambda x: x["verifications"].__setitem__(0, flip(x["verifications"][0])),
        lambda x: x.__setitem__("core_attacks", flip(x["core_attacks"])),
        lambda x: x["candidate_files"]["seed1"]["result.json"].__setitem__("symlink", True),
        lambda x: x["candidate_files"]["seed1"]["result.json"].__setitem__("nlink", 2),
        lambda x: x["candidate_inventory"].append("unexpected.extra"),
        lambda x: x["candidate_files"]["seed1"]["result.json"]["stat"].__setitem__(1, 0),
        lambda x: x.__setitem__("authority_pre_post_sha_stat_identical", False),
        lambda x: x.__setitem__("two_genuine_hash_seeds", False),
        lambda x: x.__setitem__("minimal_environment", False),
        lambda x: x.__setitem__("isolated_python_flags", False),
        lambda x: x["runs"][0].__setitem__("exit", 1),
        lambda x: x["runs"][4].__setitem__("signal", 9),
        lambda x: x["runs"][6].__setitem__("stderr_empty", False),
        lambda x: x.__setitem__("payload_manifest_closure", False),
        lambda x: x.__setitem__("root_manifest_sorted", False),
        lambda x: x.__setitem__("canonical_json", False),
        lambda x: x.__setitem__("cold_historical_read", True),
        lambda x: x.__setitem__("terminal_candidate_bytes_match_replay", False),
    ]
    need(len(mutations) == len(ATTACK_NAMES) == 32,
         "exact 32 release attacks")
    records: list[dict[str, Any]] = []
    for name, mutate in zip(ATTACK_NAMES, mutations, strict=True):
        attacked = copy.deepcopy(baseline)
        mutate(attacked)
        rejected = False
        error = ""
        try:
            validate(attacked, baseline)
        except Rejected as failure:
            rejected = True
            error = str(failure)
        records.append({"name": name, "rejected_fail_closed": rejected,
                        "error": error})
    need(all(record["rejected_fail_closed"] for record in records),
         "all 32 release attacks rejected")
    post = {str(path.relative_to(ROOT)): descriptor(path) for path in paths}
    need(pre == post, "all authoritative inputs pre/post SHA/stat identical")
    if args.preflight_only:
        return {"status":
                "PASS_C28_RELEASE_ATTACK_PREFLIGHT__NO_OUTPUT_CREATED_ZERO_CREDIT"}
    body = {
        "schema": ATTACK_SCHEMA, "status": ATTACK_STATUS,
        "completed_at_utc": utc_now(),
        "attack_census": {"planned": 32, "executed": 32,
                          "rejected_fail_closed": 32, "accepted": 0},
        "attacks": records,
        "scope": {
            "predecessor_terminal_and_adapter_substitution": True,
            "dual_candidate_verifier_and_core_attack_drift": True,
            "symlink_hardlink_extra_member": True,
            "atomic_replace_and_TOCTOU": True,
            "wrong_seed_environment_and_isolation": True,
            "exit_signal_and_stderr": True,
            "manifest_closure_order_and_canonical_JSON": True,
            "cold_historical_read": True,
            "terminal_byte_mismatch": True,
        },
        "authoritative_inputs_pre_post_sha_stat_identical": True,
        "projection_attacks_do_not_replace_outer_or_terminal_replay": True,
        "formal_credit": 0, "manifest_authorized": False,
        "C27R2": "AUTHORIZED_PREDECESSOR_ONLY",
        "C28": "UNAUTHORIZED_PENDING_EVIDENCE_MANIFEST_OUTER_AND_TERMINAL_REPLAY",
        "C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM",
    }
    result = {**body, "release_attack_receipt_sha256": digest(body)}
    output.mkdir(mode=0o700)
    write_once(output / "release_attacks.json", canonical(result) + b"\n")
    write_once(output / "PASS.lock", ATTACK_PASS)
    return result


def self_test() -> dict[str, Any]:
    baseline = {"x": "0" * 64}
    attacked = copy.deepcopy(baseline)
    attacked["x"] = flip(attacked["x"])
    need(attacked != baseline and len(ATTACK_NAMES) == 32
         and len(set(ATTACK_NAMES)) == 32,
         "private mutation/attack inventory fixture")
    return {"status": "PASS_C28_PRIVATE_MUTATION_AND_32_ATTACK_FIXTURE"}


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--self-test", action="store_true")
    value.add_argument("--preflight-only", action="store_true")
    for name in (
        "core-unit", "expect-core-invocation-id", "core-control-dir",
        "predecessor-terminal-dir", "adapter-dir", "seed1-candidate-dir",
        "seed2-candidate-dir", "verifier1-file", "verifier2-file",
        "cold-control-dir", "cold-output-dir", "cold-run-dir", "output-dir",
        "expect-harness-sha256", "expect-core-receipt-file-sha256",
        "expect-core-receipt-object-sha256", "expect-core-pass-sha256",
        "expect-cold-receipt-file-sha256",
        "expect-cold-receipt-object-sha256",
    ):
        value.add_argument("--" + name)
    for name in RUN_ARGUMENTS:
        value.add_argument("--" + name.replace("_", "-"))
    value.add_argument("--core-dir", action="append")
    return value


def main() -> int:
    args = parser().parse_args()
    fields = (
        "core_unit", "expect_core_invocation_id", "core_control_dir",
        "predecessor_terminal_dir", "adapter_dir", "seed1_candidate_dir",
        "seed2_candidate_dir", "verifier1_file", "verifier2_file",
        "cold_control_dir", "cold_output_dir", "cold_run_dir", "output_dir",
        "expect_harness_sha256", "expect_core_receipt_file_sha256",
        "expect_core_receipt_object_sha256", "expect_core_pass_sha256",
        "expect_cold_receipt_file_sha256",
        "expect_cold_receipt_object_sha256", *RUN_ARGUMENTS,
    )
    try:
        if args.self_test:
            need(not args.preflight_only and args.core_dir is None
                 and all(getattr(args, field) is None for field in fields),
                 "self-test accepts no run arguments")
            result = self_test()
        else:
            need(args.core_dir is not None
                 and all(getattr(args, field) is not None for field in fields),
                 "all run arguments")
            result = execute(args)
        sys.stdout.buffer.write(canonical({
            "CM2": "NO-GO_FOR_CLAIM", "formal_credit": 0,
            "status": result["status"],
        }) + b"\n")
        return 0
    except (Rejected, OSError, ValueError, KeyError, TypeError,
            subprocess.SubprocessError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
