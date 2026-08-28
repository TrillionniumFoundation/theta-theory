#!/usr/bin/env python3
"""Independently validate the current C28-v2 core/release boundary.

Formal mode accepts an exactly empty override map.  Private-fixture mode
accepts exactly one allowlisted logical-path override and is permanently
zero-credit.  Both modes execute the same byte, JSON, gzip, manifest, process,
inventory, current-path and nine-field-stat validation path.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import time
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
AUDIT = ROOT / ".cm2-runtime/audit"
BASE = "cm2.round306c28.source-g-post-c27r2-125561998198-pair-routing.v2."
CORE_SCHEMA = BASE + "gated-dual-seed-core-receipt.v1"
CORE_STATUS = (
    "PASS_C27R2_TERMINAL_ADAPTER_DUAL_TRUE_SEED_THREE_FILE_CANDIDATES_"
    "TWO_NO_IMPORT_VERIFIERS_AND_26_ATTACKS__ZERO_CREDIT_PENDING_RELEASE"
)
PINSET_SCHEMA = BASE + "gated-transaction-pinset.v1"
SPEC_SCHEMA = BASE + "process-command-spec.v1"
RUN_SCHEMA = BASE + "process-run-attestation.v1"
RUN_STATUS = (
    "PASS_PROCESS_TRANSACTION_EXIT0_NULL_SIGNAL_EMPTY_STDERR_PRE_POST_"
    "AND_OUTPUTS__ZERO_CREDIT"
)
RESULT_SCHEMA = BASE + "producer-result.v1"
VERIFY_SCHEMA = BASE + "independent-verification.v1"
ATTACK_SCHEMA = BASE + "coherent-attack-harness.v1"
OVERRIDE_SCHEMA = BASE + "release-repair-boundary-override-map.v1"
OUTPUT_SCHEMA = BASE + "release-repair-boundary-independent-validation.v1"
OUTPUT_STATUS = (
    "PASS_C28_RELEASE_REPAIR_BOUNDARY_CURRENT_BYTES_PROCESS_AND_INVENTORY_"
    "VALIDATED__ZERO_CREDIT"
)
CORE_PASS = b"PASS_C28_PAIR_ROUTING_V2_DUAL_SEED_CORE__ZERO_CREDIT\n"
EXPECTED = {"members": 502_204, "post_components": 43_684,
    "total_pairs": 126_104_177_706, "within_pairs": 542_179_508,
    "cross_pairs": 125_561_998_198, "blocks": 256, "shards": 32_896}
CANDIDATE_FILES = {
    "member_home_block_census.jsonl.gz",
    "cross_component_pair_route_shard.jsonl.gz", "result.json"}
ADAPTER_FILES = {"authority_contract.json", "payload_manifest.sha256",
    "root_manifest.sha256", "terminal_receipt.json", "PASS.lock"}
RUN_FILES = {"PASS.lock", "exit_code.txt", "input_post.json",
    "input_pre.json", "output_validation.json", "run_attestation.json",
    "runner_start.json", "signal.json", "stderr.log", "stdout.log",
    "timing.json"}
TARGET_KEYS = {"control", "adapter", "adapter_verification",
    "adapter_run", "adapter_verifier_run", "seed1_candidate", "seed1_run",
    "seed2_candidate", "seed2_run", "verifier1_output", "verifier1_run",
    "verifier2_output", "verifier2_run", "attack_work", "attack_run"}
SOURCE_PINS = {
    "adapter_builder": "15dc2695345ad5ece0038797b3ccb0031b0c22b8aa06ed0730bf7c93aaf7fca0",
    "adapter_verifier": "23aea6fddc9dc64c3c5d598557f6d1f64d7689c11ee2d932da9938730427b90b",
    "producer": "364610cfa465601ac99fcd5ee3528ee5da791fcb5fb1c9ab27ff38966d211205",
    "independent_verifier": "7ca21d0e02f95afc1a8fc9635c3aa31bb290b8499f28860f8f8ae095b451cb04",
    "coherent_attacks": "ea09933a45c7b00a268edd961336069b43c15561a1e6c345fdadb160c02e50c1",
    "transaction_runner": "d37ebb999f226d6af65338b9ccc5c40ace70de80bf1db32cd4e129740d740ae3",
    "python": "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118",
    "attack_python": "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118",
    "watcher": "4c9d353c7b1214c43a437f7dfc9bbd0ac82f24a669c1ae7f11b378ac2a7ca1ea",
}
STAGES = {
    "adapter": ("authority_adapter_command_spec.json", "adapter_run",
                "adapter_builder", "30662801", "authority_adapter"),
    "adapter_verifier": ("authority_adapter_verifier_command_spec.json",
                "adapter_verifier_run", "adapter_verifier", "30662802",
                "authority_adapter_verifier"),
    "producer_seed1": ("seed1_producer_command_spec.json", "seed1_run",
                "producer", "30662801", "producer"),
    "producer_seed2": ("seed2_producer_command_spec.json", "seed2_run",
                "producer", "30662802", "producer"),
    "verifier_seed1": ("seed1_verifier_command_spec.json", "verifier1_run",
                "independent_verifier", "30662801", "independent_verifier"),
    "verifier_seed2": ("seed2_verifier_command_spec.json", "verifier2_run",
                "independent_verifier", "30662802", "independent_verifier"),
    "coherent_attacks": ("coherent_attacks_command_spec.json", "attack_run",
                "coherent_attacks", "30662803", "coherent_attacks"),
}
EMPTY_SHA = hashlib.sha256(b"").hexdigest()


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
    return type(value) is str and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def strict(payload: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(type(key) is str and key not in result, "duplicate JSON key")
            result[key] = value
        return result
    return json.loads(payload, object_pairs_hook=pairs,
                      parse_constant=lambda token: (_ for _ in ()).throw(
                          Rejected("non-finite JSON:" + token)))


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns,
            value.st_uid, value.st_gid)


def logical_name(raw: str | Path, root: Path) -> str:
    value = Path(raw)
    if value.is_absolute():
        try:
            value = value.relative_to(ROOT)
        except ValueError:
            try:
                value = value.relative_to(root)
            except ValueError as error:
                raise Rejected("path outside authority root") from error
    name = str(value)
    need(name != "" and not value.is_absolute() and str(Path(name)) == name
         and all(part not in {"", ".", ".."} for part in value.parts),
         "canonical logical path")
    return name


def safe_direct_document(path: Path, closure: str) -> dict[str, Any]:
    need(path.is_file() and not path.is_symlink(), "override document regular")
    raw = path.read_bytes()
    need(raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
         "override document newline")
    value = strict(raw[:-1])
    need(type(value) is dict and canonical(value) == raw[:-1],
         "override document canonical")
    body = dict(value)
    claim = body.pop(closure, None)
    need(valid_sha(claim) and claim == digest(body), "override object closure")
    return value


def validate_override(value: dict[str, Any], mode: str, authority_root: Path,
                      case_root: Path | None) -> dict[str, Path]:
    overrides = value.get("overrides")
    need(value.get("schema") == OVERRIDE_SCHEMA
         and value.get("mode") == mode
         and value.get("authority_root") == str(authority_root)
         and value.get("formal_credit") == 0
         and value.get("C28") == "AUDIT_HOLD_UNAUTHORIZED"
         and value.get("CM2") == "NO-GO_FOR_CLAIM"
         and type(overrides) is list, "override map boundary")
    if mode == "formal":
        need(overrides == [] and case_root is None, "formal empty override")
        return {}
    need(case_root is not None and case_root.is_absolute()
         and case_root.is_relative_to(AUDIT) and case_root.is_dir()
         and not case_root.is_symlink() and len(overrides) == 1,
         "private fixture root/single override")
    item = overrides[0]
    need(type(item) is dict and set(item) == {
        "case_name", "logical_path", "physical_path", "barrier_after_open"},
        "single override shape")
    logical = logical_name(item["logical_path"], authority_root)
    physical = Path(item["physical_path"])
    need(physical.is_absolute() and physical.is_relative_to(case_root)
         and physical != case_root and type(item["case_name"]) is str
         and re.fullmatch(r"[a-z0-9][a-z0-9-]{2,80}", item["case_name"])
             is not None
         and type(item["barrier_after_open"]) is bool,
         "private override confinement")
    return {logical: physical}


class Resolver:
    def __init__(self, root: Path, overrides: dict[str, Path],
                 barrier_logical: str | None = None,
                 barrier_dir: Path | None = None):
        self.root = root
        self.overrides = overrides
        self.barrier_logical = barrier_logical
        self.barrier_dir = barrier_dir
        self.barrier_used = False
        self.allowed: set[str] = set()
        self.used: set[str] = set()
        self.pre: dict[str, dict[str, Any]] = {}

    def logical(self, raw: str | Path) -> str:
        return logical_name(raw, self.root)

    def path(self, raw: str | Path) -> tuple[str, Path]:
        logical = self.logical(raw)
        path = self.overrides.get(logical, self.root / logical)
        if logical in self.overrides:
            self.used.add(logical)
        return logical, path

    def capture(self, raw: str | Path, maximum: int = 16 << 30) \
            -> tuple[bytes, dict[str, Any]]:
        logical, path = self.path(raw)
        current = path.parent
        need(current.exists() and not current.is_symlink(),
             "capture parent exists/no symlink")
        need(path.is_file() and not path.is_symlink(), "capture regular file")
        descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                             | getattr(os, "O_NOFOLLOW", 0))
        try:
            before = os.fstat(descriptor)
            need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1
                 and 0 <= before.st_size <= maximum,
                 "capture regular singleton/bounded")
            state = hashlib.sha256()
            chunks: list[bytes] = []
            while block := os.read(descriptor, 4 << 20):
                state.update(block)
                chunks.append(block)
            if (logical == self.barrier_logical and not self.barrier_used
                    and self.barrier_dir is not None):
                self.barrier_used = True
                (self.barrier_dir / "fd-opened.lock").write_bytes(b"OPENED\n")
                deadline = time.monotonic() + 30
                while not (self.barrier_dir / "continue.lock").exists():
                    need(time.monotonic() < deadline, "fixture barrier timeout")
                    time.sleep(0.01)
            after = os.fstat(descriptor)
        finally:
            os.close(descriptor)
        current_stat = os.stat(path, follow_symlinks=False)
        need(fingerprint(before) == fingerprint(after)
             == fingerprint(current_stat), "capture FD/path nine-stat identity")
        raw_bytes = b"".join(chunks)
        record = {"path": logical, "sha256": state.hexdigest(),
                  "size": len(raw_bytes),
                  "stat_fingerprint": list(fingerprint(before))}
        prior = self.pre.setdefault(logical, record)
        need(prior == record, "repeat capture identity")
        return raw_bytes, record

    def document(self, raw: str | Path, closure: str) -> dict[str, Any]:
        payload, _ = self.capture(raw, 64 << 20)
        need(payload.endswith(b"\n") and not payload.endswith(b"\n\n"),
             "document newline")
        value = strict(payload[:-1])
        need(type(value) is dict and canonical(value) == payload[:-1],
             "canonical document")
        body = dict(value)
        claim = body.pop(closure, None)
        need(valid_sha(claim) and claim == digest(body), "document closure")
        return value

    def plain(self, raw: str | Path) -> Any:
        payload, _ = self.capture(raw, 512 << 20)
        need(payload.endswith(b"\n") and not payload.endswith(b"\n\n"),
             "plain JSON newline")
        value = strict(payload[:-1])
        need(canonical(value) == payload[:-1], "plain canonical JSON")
        return value

    def verify_current(self) -> str:
        rows: list[dict[str, Any]] = []
        for logical, expected in sorted(self.pre.items()):
            path = self.overrides.get(logical, self.root / logical)
            need(path.is_file() and not path.is_symlink(),
                 "post current regular")
            info = path.stat(follow_symlinks=False)
            need(info.st_nlink == 1 and list(fingerprint(info))
                 == expected["stat_fingerprint"], "post current nine-stat")
            descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                                 | getattr(os, "O_NOFOLLOW", 0))
            try:
                state = hashlib.sha256()
                while block := os.read(descriptor, 4 << 20):
                    state.update(block)
            finally:
                os.close(descriptor)
            need(state.hexdigest() == expected["sha256"], "post current SHA")
            rows.append(expected)
        return hashlib.sha256(b"".join(canonical(row) + b"\n"
                                       for row in rows)).hexdigest()


def sha_record_matches(value: Any, record: dict[str, Any]) -> bool:
    return (type(value) is dict and value.get("sha256") == record["sha256"]
            and value.get("size") == record["size"]
            and value.get("stat_fingerprint") == record["stat_fingerprint"])


def parse_manifest(resolver: Resolver, raw: str | Path) -> dict[str, str]:
    payload, _ = resolver.capture(raw, 64 << 20)
    need(payload.endswith(b"\n"), "manifest newline")
    result: dict[str, str] = {}
    for line in payload.decode("ascii").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\x00\r\n]+)", line)
        need(match is not None and match.group(2) not in result,
             "manifest row/unique")
        logical = resolver.logical(match.group(2))
        need(logical == match.group(2), "manifest canonical logical path")
        result[logical] = match.group(1)
    need(list(result) == sorted(result), "manifest sorted")
    for logical, expected in result.items():
        _, observed = resolver.capture(logical)
        need(observed["sha256"] == expected, "manifest current member")
    return result


def gzip_rows(payload: bytes) -> tuple[list[dict[str, Any]], str]:
    need(payload[:3] == b"\x1f\x8b\x08" and len(payload) >= 10
         and int.from_bytes(payload[4:8], "little") == 0,
         "gzip header/mtime0")
    rows: list[dict[str, Any]] = []
    sequence = hashlib.sha256()
    try:
        with gzip.GzipFile(fileobj=io.BytesIO(payload), mode="rb") as stream:
            for raw in stream:
                need(raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
                     "JSONL newline")
                value = strict(raw[:-1])
                need(type(value) is dict and canonical(value) == raw[:-1],
                     "canonical JSONL")
                body = dict(value)
                claim = body.pop("row_sha256", None)
                need(valid_sha(claim) and claim == digest(body), "row closure")
                sequence.update(claim.encode("ascii") + b"\n")
                rows.append(value)
    except (gzip.BadGzipFile, EOFError) as error:
        raise Rejected("truncated/invalid gzip") from error
    return rows, sequence.hexdigest()


def directory_snapshot(resolver: Resolver, raw: str | Path) -> dict[str, Any]:
    logical, path = resolver.path(raw)
    need(path.is_dir() and not path.is_symlink(), "snapshot directory")
    files: list[tuple[str, Path]] = []
    directory_count = 0
    for current, dirnames, filenames in os.walk(path):
        base = Path(current)
        for name in dirnames:
            member = base / name
            need(not member.is_symlink(), "snapshot symlink directory")
            directory_count += 1
        for name in filenames:
            member = base / name
            need(member.is_file() and not member.is_symlink(),
                 "snapshot regular file")
            relative = str(member.relative_to(path))
            child_logical = str(Path(logical) / relative)
            files.append((relative, member))
            resolver.allowed.add(child_logical)
    records: list[dict[str, Any]] = []
    for relative, _ in sorted(files):
        _, record = resolver.capture(str(Path(logical) / relative))
        records.append(record)
    return {"kind": "directory", "directory_count": directory_count,
            "relative_file_inventory": [name for name, _ in sorted(files)],
            "files": records}


def validate_service(unit: str, invocation: str) -> None:
    need(type(unit) is str and unit.endswith(".service")
         and re.fullmatch(r"[0-9a-f]{32}", invocation) is not None,
         "service identity syntax")
    completed = subprocess.run(["/usr/bin/systemctl", "--user", "show", unit,
        "-p", "ActiveState", "-p", "SubState", "-p", "Result",
        "-p", "ExecMainCode", "-p", "ExecMainStatus", "-p", "InvocationID"],
        cwd=ROOT, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False)
    need(completed.returncode == 0 and completed.stderr == b"",
         "service query")
    fields = dict(line.split("=", 1) for line in
                  completed.stdout.decode("ascii").splitlines() if "=" in line)
    need(fields.get("ActiveState") == "active"
         and fields.get("SubState") == "exited"
         and fields.get("Result") == "success"
         and fields.get("ExecMainCode") in {"1", "exited"}
         and fields.get("ExecMainStatus") == "0"
         and fields.get("InvocationID") == invocation,
         "exact clean core service")


def validate_environment(args: argparse.Namespace) -> None:
    python = Path(args.python).absolute()
    need(sys.flags.isolated == 1 and Path(sys.executable).absolute() == python,
         "isolated exact Python executable")
    resolver = Resolver(ROOT, {})
    _, record = resolver.capture(python.relative_to(ROOT))
    need(record["sha256"] == args.expect_python_sha256
         and os.environ.get("PATH") == "/usr/bin:/bin"
         and os.environ.get("LANG") == "C"
         and os.environ.get("LC_ALL") == "C"
         and os.environ.get("PYTHONHASHSEED") == args.expected_hash_seed,
         "exact Python/environment/hash seed")


def validate_historical_current(resolver: Resolver, value: Any,
                                label: str) -> None:
    need(type(value) is dict and {"command-spec", "pinset"} <= set(value),
         label + ":input attestation map")
    for name, record in value.items():
        need(type(record) is dict and valid_sha(record.get("sha256"))
             and type(record.get("size")) is int
             and type(record.get("stat_fingerprint")) is list
             and len(record["stat_fingerprint"]) == 9,
             label + ":historical record shape")
        logical = resolver.logical(record["path"])
        resolver.allowed.add(logical)
        _, current = resolver.capture(logical)
        need(sha_record_matches(record, current),
             label + ":historical equals current SHA/nine-stat")


def validate_candidate(resolver: Resolver, directory: str) -> dict[str, Any]:
    logical, path = resolver.path(directory)
    need(path.is_dir() and not path.is_symlink()
         and {entry.name for entry in path.iterdir()} == CANDIDATE_FILES,
         "candidate exact inventory")
    result = resolver.document(str(Path(logical) / "result.json"),
                               "result_sha256")
    need(result.get("schema") == RESULT_SCHEMA
         and result.get("formal_credit") == 0
         and result.get("manifest_authorized") is False
         and result.get("post_C27R2_partition_census") == {
             "components": EXPECTED["post_components"],
             "cross_post_component_member_pairs": EXPECTED["cross_pairs"],
             "members": EXPECTED["members"],
             "total_unordered_member_pairs": EXPECTED["total_pairs"],
             "within_post_component_member_pairs": EXPECTED["within_pairs"]},
         "candidate exact result boundary")
    for role, name in (("member_home_block_census",
                        "member_home_block_census.jsonl.gz"),
                       ("cross_component_pair_route_shard",
                        "cross_component_pair_route_shard.jsonl.gz")):
        payload, record = resolver.capture(str(Path(logical) / name), 1 << 30)
        rows, sequence = gzip_rows(payload)
        descriptor = result["ledgers"][role]
        need(record["sha256"] == descriptor["sha256"]
             and record["size"] == descriptor["size"]
             and len(rows) == descriptor["row_count"]
             and sequence == descriptor["row_sequence_sha256"]
             and descriptor.get("canonical_jsonl") is True
             and descriptor.get("gzip_mtime") == 0,
             "candidate ledger descriptor/closure")
    return result


def validate_run(resolver: Resolver, control: str, pinset: dict[str, Any],
                 core: dict[str, Any], name: str, values: tuple[str, ...],
                 targets: dict[str, str]) -> dict[str, Any]:
    spec_name, run_key, source_key, seed, exact_stage = values
    spec_logical = str(Path(control) / spec_name)
    spec = resolver.document(spec_logical, "command_spec_sha256")
    run_logical = targets[run_key]
    _, run_path = resolver.path(run_logical)
    need(run_path.is_dir() and not run_path.is_symlink()
         and {entry.name for entry in run_path.iterdir()} == RUN_FILES,
         name + ":run exact inventory")
    attestation = resolver.document(
        str(Path(run_logical) / "run_attestation.json"),
        "run_attestation_sha256")
    need(spec.get("schema") == SPEC_SCHEMA and spec.get("stage") == exact_stage
         and spec.get("source_sha256") == SOURCE_PINS[source_key]
         and spec.get("python_hash_seed") == seed
         and spec.get("environment") == {"PATH": "/usr/bin:/bin", "LANG": "C",
             "LC_ALL": "C", "PYTHONHASHSEED": seed}
         and spec.get("runner_source_sha256") == SOURCE_PINS["transaction_runner"]
         and spec.get("python_sha256") == SOURCE_PINS["python"]
         and spec.get("pinset_object_sha256") == pinset["pinset_sha256"]
         and attestation.get("schema") == RUN_SCHEMA
         and attestation.get("status") == RUN_STATUS
         and attestation.get("stage") == exact_stage
         and attestation.get("numeric_exit_code") == 0
         and attestation.get("signal") is None
         and attestation.get("timed_out") is False
         and attestation.get("stderr_empty") is True
         and attestation.get("stderr_sha256") == EMPTY_SHA
         and attestation.get("input_pre_post_sha_stat_identical") is True
         and attestation.get("command_spec_object_sha256")
             == spec["command_spec_sha256"]
         and attestation.get("pinset_object_sha256") == pinset["pinset_sha256"]
         and attestation.get("runner_source_sha256")
             == SOURCE_PINS["transaction_runner"]
         and attestation.get("stage_source_sha256") == SOURCE_PINS[source_key]
         and attestation.get("python_sha256") == SOURCE_PINS["python"]
         and attestation.get("formal_credit") == 0
         and core["run_attestation_object_sha256"][name]
             == attestation["run_attestation_sha256"],
         name + ":spec/run/process closure")
    need(resolver.capture(str(Path(run_logical) / "exit_code.txt"))[0] == b"0\n"
         and resolver.capture(str(Path(run_logical) / "signal.json"))[0]
             == b"null\n"
         and resolver.capture(str(Path(run_logical) / "stderr.log"))[0] == b""
         and resolver.capture(str(Path(run_logical) / "input_pre.json"))[0]
             == resolver.capture(str(Path(run_logical) / "input_post.json"))[0]
         and resolver.plain(str(Path(run_logical) / "input_post.json"))
             == attestation["input_attestations"]
         and resolver.plain(str(Path(run_logical) / "output_validation.json"))
             == attestation["output_validation"],
         name + ":run sidecars")
    validate_historical_current(resolver, attestation["input_attestations"], name)
    current_outputs: dict[str, Any] = {}
    for output in spec["output_roots"]:
        logical = resolver.logical(output["path"])
        if output["kind"] == "file":
            _, record = resolver.capture(logical)
            current_outputs[output["path"]] = {"kind": "file", "files": [record]}
        else:
            snapshot = directory_snapshot(resolver, logical)
            exact = output["exact_inventory"]
            need(exact is None or snapshot["relative_file_inventory"] == exact,
                 name + ":exact current output inventory")
            current_outputs[output["path"]] = snapshot
    need(current_outputs == attestation["output_validation"],
         name + ":historical output equals current")
    return attestation


def execute(args: argparse.Namespace) -> dict[str, Any]:
    validate_environment(args)
    need(valid_sha(args.expect_validator_sha256)
         and valid_sha(args.expect_core_receipt_file_sha256)
         and valid_sha(args.expect_core_receipt_object_sha256),
         "dynamic SHA pins")
    direct = Resolver(ROOT, {})
    _, self_record = direct.capture(SELF.relative_to(ROOT))
    need(self_record["sha256"] == args.expect_validator_sha256,
         "validator self pin")
    authority_root = Path(args.authority_root).absolute()
    need(authority_root.is_dir() and not authority_root.is_symlink(),
         "authority root")
    case_root = (None if args.private_case_root is None
                 else Path(args.private_case_root).absolute())
    override_value = safe_direct_document(Path(args.override_map_file).absolute(),
                                          "override_map_sha256")
    overrides = validate_override(override_value, args.mode, authority_root,
                                  case_root)
    barrier_logical = None
    barrier_dir = None
    if overrides:
        item = override_value["overrides"][0]
        if item["barrier_after_open"]:
            barrier_logical = logical_name(item["logical_path"], authority_root)
            barrier_dir = case_root
    resolver = Resolver(authority_root, overrides, barrier_logical, barrier_dir)
    control = resolver.logical(args.core_control_relative)
    core_path = str(Path(control) / "core_receipt.json")
    pinset_path = str(Path(control) / "pinset.json")
    core = resolver.document(core_path, "core_receipt_sha256")
    pinset = resolver.document(pinset_path, "pinset_sha256")
    _, core_record = resolver.capture(core_path)
    need(core_record["sha256"] == args.expect_core_receipt_file_sha256
         and core["core_receipt_sha256"]
             == args.expect_core_receipt_object_sha256
         and core.get("schema") == CORE_SCHEMA and core.get("status") == CORE_STATUS
         and core.get("exact_math") == EXPECTED
         and core.get("formal_credit") == 0
         and core.get("manifest_authorized") is False
         and core.get("C28") == "UNAUTHORIZED_PENDING_RELEASE_TERMINAL"
         and core.get("C29") == "UNAUTHORIZED"
         and core.get("CM2") == "NO-GO_FOR_CLAIM"
         and pinset.get("schema") == PINSET_SCHEMA
         and pinset.get("source_pins") == SOURCE_PINS
         and pinset.get("true_seeds") == ["30662801", "30662802"]
         and pinset.get("formal_credit") == 0
         and pinset.get("manifest_authorized") is False
         and resolver.capture(str(Path(control) / "PASS.lock"))[0] == CORE_PASS,
         "core receipt/pinset boundary")
    if args.mode == "formal":
        need(authority_root == ROOT, "formal authority root exact workspace")
        validate_service(args.expected_core_unit,
                         args.expected_core_invocation_id)
    targets_raw = pinset.get("targets")
    need(type(targets_raw) is dict and set(targets_raw) == TARGET_KEYS,
         "exact fifteen core targets")
    targets = {name: resolver.logical(raw) for name, raw in targets_raw.items()}
    need(targets["control"] == control, "core control target identity")
    for value in targets.values():
        resolver.allowed.add(value)
    adapter_logical = targets["adapter"]
    _, adapter_path = resolver.path(adapter_logical)
    need(adapter_path.is_dir() and not adapter_path.is_symlink()
         and {entry.name for entry in adapter_path.iterdir()} == ADAPTER_FILES,
         "adapter exact inventory")
    contract_path = str(Path(adapter_logical) / "authority_contract.json")
    receipt_path = str(Path(adapter_logical) / "terminal_receipt.json")
    contract = resolver.document(contract_path, "authority_contract_sha256")
    adapter_receipt = resolver.document(receipt_path, "terminal_receipt_sha256")
    _, contract_record = resolver.capture(contract_path)
    need(contract_record["sha256"] == core["adapter_contract_file_sha256"]
         and contract["authority_contract_sha256"]
             == core["adapter_contract_object_sha256"]
         and adapter_receipt["terminal_receipt_sha256"]
             == core["adapter_receipt_object_sha256"], "adapter core pins")
    parse_manifest(resolver, str(Path(adapter_logical) / "payload_manifest.sha256"))
    parse_manifest(resolver, str(Path(adapter_logical) / "root_manifest.sha256"))
    adapter_verification = resolver.document(
        str(Path(targets["adapter_verification"]) / "verification.json"),
        "verification_sha256")
    need(adapter_verification["verification_sha256"]
         == core["adapter_verification_object_sha256"],
         "adapter verification core pin")
    seed1 = validate_candidate(resolver, targets["seed1_candidate"])
    seed2 = validate_candidate(resolver, targets["seed2_candidate"])
    for name in CANDIDATE_FILES:
        first, first_record = resolver.capture(
            str(Path(targets["seed1_candidate"]) / name))
        second, second_record = resolver.capture(
            str(Path(targets["seed2_candidate"]) / name))
        agreement = core["dual_seed_candidate_file_agreement"][name]
        need(first == second
             and first_record["sha256"] == agreement["seed1_sha256"]
             and second_record["sha256"] == agreement["seed2_sha256"],
             "dual seed candidate byte agreement")
    need(seed1["result_sha256"] == seed2["result_sha256"]
         == core["candidate_result_object_sha256"],
         "candidate result object pin")
    verifier_values = [resolver.document(
        str(Path(targets[name]) / "verification.json"), "verification_sha256")
        for name in ("verifier1_output", "verifier2_output")]
    need([value["verification_sha256"] for value in verifier_values]
         == core["verifier_object_sha256"]
         and all(value.get("schema") == VERIFY_SCHEMA for value in verifier_values),
         "dual verifier object pins")
    attacks = resolver.document(str(Path(control) / "coherent_attacks.json"),
                                "attack_receipt_sha256")
    need(attacks.get("schema") == ATTACK_SCHEMA
         and attacks["attack_receipt_sha256"]
             == core["attack_receipt_object_sha256"],
         "coherent attack receipt core pin")
    run_objects: dict[str, str] = {}
    for name, values in STAGES.items():
        attestation = validate_run(resolver, control, pinset, core, name,
                                   values, targets)
        run_objects[name] = attestation["run_attestation_sha256"]
    need(run_objects == core["run_attestation_object_sha256"],
         "all seven run object pins")
    resolver.allowed.update({core_path, pinset_path,
        str(Path(control) / "PASS.lock"), contract_path, receipt_path})
    need(set(overrides) <= resolver.allowed and set(overrides) == resolver.used,
         "private override exact allowlist/consumption")
    current_digest = resolver.verify_current()
    output = Path(args.out_file).absolute()
    need(output.parent == AUDIT and not output.exists() and not output.is_symlink(),
         "fresh audit output")
    body = {"schema": OUTPUT_SCHEMA, "status": OUTPUT_STATUS,
        "completed_at_utc": datetime.now(timezone.utc).isoformat(
            timespec="microseconds").replace("+00:00", "Z"),
        "mode": args.mode,
        "core_unit_name": args.expected_core_unit,
        "core_invocation_id": args.expected_core_invocation_id,
        "core_receipt_file_sha256": core_record["sha256"],
        "core_receipt_object_sha256": core["core_receipt_sha256"],
        "override_map_file_sha256": hashlib.sha256(
            Path(args.override_map_file).read_bytes()).hexdigest(),
        "override_map_object_sha256": override_value["override_map_sha256"],
        "captured_current_file_count": len(resolver.pre),
        "captured_current_identity_sha256": current_digest,
        "exact_target_count": 15, "exact_stage_count": 7,
        "dual_seed_candidate_byte_identical": True,
        "historical_inputs_equal_current_SHA_size_nine_stat": True,
        "historical_outputs_equal_current_inventory_SHA_size_nine_stat": True,
        "formal_credit": 0, "manifest_authorized": False,
        "C28": "AUDIT_HOLD_UNAUTHORIZED", "C29": "UNAUTHORIZED",
        "CM2": "NO-GO_FOR_CLAIM"}
    result = {**body, "boundary_validation_sha256": digest(body)}
    descriptor = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                         | getattr(os, "O_NOFOLLOW", 0), 0o400)
    try:
        os.write(descriptor, canonical(result) + b"\n")
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    return result


def self_test() -> dict[str, Any]:
    duplicate_rejected = escape_rejected = bad_override_rejected = False
    try:
        strict(b'{"a":1,"a":2}')
    except Rejected:
        duplicate_rejected = True
    try:
        logical_name("../escape", ROOT)
    except Rejected:
        escape_rejected = True
    formal = {"schema": OVERRIDE_SCHEMA, "mode": "formal",
        "authority_root": str(ROOT), "overrides": [], "formal_credit": 0,
        "C28": "AUDIT_HOLD_UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM"}
    need(validate_override(formal, "formal", ROOT, None) == {},
         "formal override fixture")
    bad = dict(formal)
    bad["overrides"] = [{"logical_path": "x"}]
    try:
        validate_override(bad, "formal", ROOT, None)
    except Rejected:
        bad_override_rejected = True
    row_body = {"schema": "fixture", "ordinal": 0}
    row = {**row_body, "row_sha256": digest(row_body)}
    raw = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as stream:
        stream.write(canonical(row) + b"\n")
    rows, sequence = gzip_rows(raw.getvalue())
    resolver = Resolver(ROOT, {})
    resolver.capture(SELF.relative_to(ROOT))
    current = resolver.verify_current()
    need(duplicate_rejected and escape_rejected and bad_override_rejected
         and rows == [row] and sequence
             == hashlib.sha256((row["row_sha256"] + "\n").encode()).hexdigest()
         and valid_sha(current), "validator integrity fixtures")
    return {"status":
            "PASS_C28_RELEASE_REPAIR_BOUNDARY_VALIDATOR_V1_SELF_TEST",
            "formal_credit": 0, "C28": "AUDIT_HOLD_UNAUTHORIZED",
            "CM2": "NO-GO_FOR_CLAIM"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--mode", choices=("formal", "private-fixture"))
    for name in ("authority-root", "core-control-relative", "override-map-file",
                 "expected-core-unit", "expected-core-invocation-id",
                 "expect-core-receipt-file-sha256",
                 "expect-core-receipt-object-sha256", "python",
                 "expect-python-sha256", "expect-validator-sha256",
                 "expected-hash-seed", "out-file"):
        parser.add_argument("--" + name)
    parser.add_argument("--private-case-root")
    args = parser.parse_args()
    fields = ("mode", "authority_root", "core_control_relative",
              "override_map_file", "expected_core_unit",
              "expected_core_invocation_id", "expect_core_receipt_file_sha256",
              "expect_core_receipt_object_sha256", "python",
              "expect_python_sha256", "expect_validator_sha256",
              "expected_hash_seed", "out_file")
    try:
        if args.self_test:
            need(all(getattr(args, field) is None for field in fields)
                 and args.private_case_root is None, "self-test arguments")
            result = self_test()
        else:
            need(all(getattr(args, field) is not None for field in fields)
                 and ((args.mode == "formal" and args.private_case_root is None)
                      or (args.mode == "private-fixture"
                          and args.private_case_root is not None)),
                 "all validator arguments")
            result = execute(args)
        sys.stdout.buffer.write(canonical({"CM2": "NO-GO_FOR_CLAIM",
            "formal_credit": 0, "status": result["status"]}) + b"\n")
        return 0
    except (Rejected, OSError, ValueError, KeyError, TypeError,
            subprocess.SubprocessError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
