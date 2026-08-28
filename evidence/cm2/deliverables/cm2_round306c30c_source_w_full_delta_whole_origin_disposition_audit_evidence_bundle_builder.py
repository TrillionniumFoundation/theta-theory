#!/usr/bin/env python3
"""Build the deterministic raw-evidence bundle for C30c.

This is a publication helper, not a mathematical authority.  It refuses to
run until the final P0 supplemental root, outer, terminal, and post-stage100
commit hashes have been copied into the five constants below.  It accepts an exact evidence tree,
retains the raw logs/exit/provenance/trace bytes, and publishes one normalized
tar.gz with an internal byte manifest.  It never grants Source-W credit.
"""
from __future__ import annotations

import argparse
import ctypes
import errno
import gzip
import hashlib
import importlib.machinery
import io
import json
import os
import stat
import sys
import tarfile
import tempfile
import types
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

PREFIX = "cm2_round306c30c_source_w_full_delta_whole_origin_disposition"
WORKSPACE = Path(__file__).resolve().parent.parent
DELIVERABLES = Path(__file__).resolve().parent

# Fill only after the five-layer P0 supplemental closure is formally
# published.  All five values are external pins; leaving any value unset is
# an intentional hard block, not a development default.
P0_SUPPLEMENTAL_ROOT_MANIFEST_SHA256: str | None = (
    "2788fe4dec1ad0c12f82e1b4c21cc78881919634fd6c2a83e99443e88ef84fbe"
)
P0_SUPPLEMENTAL_OUTER_VERIFICATION_SHA256: str | None = (
    "a50c5116592d9713ffb592655bb2dae1378bda39e4979dac318ba39cd7becf8f"
)
P0_SUPPLEMENTAL_TERMINAL_RECEIPT_SHA256: str | None = (
    "1ffceef343ac6ac32c80776b899328ed50e24adbd0f09f60e0be6f7e51afb168"
)
P0_SUPPLEMENTAL_FINAL_COMMIT_SHA256: str | None = (
    "e5cc485bebf76a1aa468dda0e15352c0e427a35e0056bdeae124ce81691509bb"
)
P0_SUPPLEMENTAL_FINAL_COMMIT_V2_SHA256: str | None = (
    "bb71c17db3bd27f070998b6820e92bdf44f4c011d41a255c813ec2955cd8c415"
)

P0_PAYLOAD_MANIFEST_REL = (
    "deliverables/cm2_round306c30a_supplemental_audit_closure_"
    "payload_manifest.sha256"
)
P0_COLD_RECEIPT_REL = (
    "deliverables/cm2_round306c30a_supplemental_audit_closure_"
    "cold_replay_receipt.json"
)
P0_OUTER_VERIFICATION_REL = (
    "deliverables/cm2_round306c30a_supplemental_audit_closure_"
    "outer_verification.json"
)
P0_ROOT_MANIFEST_REL = (
    "deliverables/cm2_round306c30a_supplemental_audit_closure_"
    "root_manifest.sha256"
)
P0_TERMINAL_RECEIPT_REL = (
    "deliverables/cm2_round306c30a_supplemental_audit_closure_"
    "terminal_checker_receipt.json"
)
P0_FINAL_COMMIT_REL = (
    "deliverables/cm2_round306c30a_supplemental_audit_closure_"
    "final_commit_receipt.json"
)
P0_FINAL_COMMIT_V2_REL = (
    "deliverables/cm2_round306c30a_supplemental_audit_closure_"
    "final_commit_v2_receipt.json"
)
P0_POSTCOMMIT_CHECKER_REL = (
    "deliverables/cm2_round306c30a_supplemental_audit_closure_"
    "v5_postcommit_replay_checker.py"
)
P0_POSTCOMMIT_ADDENDUM_REL = (
    "deliverables/cm2_round306c30a_supplemental_audit_closure_"
    "v5_postcommit_addendum.md"
)
P0_POSTCOMMIT_REPLAY_RECEIPT_REL = (
    "deliverables/cm2_round306c30a_supplemental_audit_closure_"
    "postcommit_replay_receipt.json"
)
P0_POSTCOMMIT_REPLAY_MANIFEST_REL = (
    "deliverables/cm2_round306c30a_supplemental_audit_closure_"
    "postcommit_replay_manifest.sha256"
)

PRODUCER_SHA256 = "4644f8aad5fb9b2956a3854d1457d40c93c7f4f134ca808c782d61e0c526e549"
VERIFIER_SHA256 = "0fd82ce16053b69cbb04eddc423cb3f4b8cf8d11923219b50e6ff659f97b7377"
HARNESS_SHA256 = "9f0b72a81098333c3f0b76d7191f48855d608b0aa1e405bdf72cb10532e825c8"
RECEIPT_VALIDATOR = "cm2_round306c30c_62_attack_run_receipt_validator.py"
RECEIPT_VALIDATOR_SHA256 = (
    "8692c8a8e57d535ba8f8162bd4f7f51e8acb04f28755384158b45b4eb2629b61"
)
RECEIPT_ADAPTER = "cm2_round306c30c_attack_receipt_evidence_adapter.py"
RECEIPT_ADAPTER_SHA256 = (
    "f4dac9c42f3de9d02e97060f14bb42ccdfca98015ed4a760bbca044b50c56590"
)
RECEIPT_ADAPTER_VERIFIER = (
    "cm2_round306c30c_attack_receipt_evidence_adapter_independent_verifier.py"
)
RECEIPT_ADAPTER_VERIFIER_SHA256 = (
    "43611f53caa199dce8c529151731db025e197d42232736200fd7b73cd67ba153"
)
TRACE_ANALYZER = PREFIX + "_cold_trace_analyzer.py"
TRACE_ANALYZER_SHA256 = "a9f6c95a0def5f241ecbe25fc815c51a606b11a494b20fb43fbf82713f54732b"
RESULT_OBJECT_SHA256 = "df4531942e743389f5e8f85b2d013132f0808f562c21f430e7904577d67087d4"
INTERPRETER_SHA256 = "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118"

SEEDS = ("30630071", "30630929")
HASH_FINGERPRINTS = {
    "30630071": 5384816073292471411,
    "30630929": -4496445986928603988,
}
PRODUCER_STDOUT = (
    b'{"result_sha256":"df4531942e743389f5e8f85b2d013132f0808f562c21f430e7904577d67087d4",'
    b'"status":"PASS_CANDIDATE_ROUND306C30C_FULL_DELTA_DISPOSITION__'
    b'AWAITING_INDEPENDENT_VERIFIER_AND_MANIFEST"}\n'
)
VERIFIER_STATUS = (
    "PASS_INDEPENDENT_CANDIDATE_C30C__80_DELTA_H_CELLS__"
    "2_RESOLVED_MIXED__ZERO_FORMAL_CREDIT"
)
HARNESS_STATUS = (
    "PASS_62_OF_62_LAYER_SPECIFIC_COHERENT_ATTACKS_REJECTED__"
    "ZERO_FORMAL_CREDIT"
)
RECEIPT_STATUS = (
    "PASS_COMPLETE_C30C_62_ATTACK_RUN_RECEIPT__ZERO_FORMAL_CREDIT"
)
ADAPTER_STATUS = (
    "PASS_RECEIPT_BOUND_TO_EXACT_ATTACK_EVIDENCE__ZERO_FORMAL_CREDIT"
)
ADAPTER_VERIFICATION_STATUS = (
    "PASS_INDEPENDENT_RECEIPT_EVIDENCE_BINDING__ZERO_FORMAL_CREDIT"
)
ATTACK_RUN_FILES = (
    "command.txt", "end_utc.txt", "exit_code.txt", "observed_child_pids.txt",
    "post.sha256", "post.stat", "pre.sha256", "pre.stat", "provenance.json",
    "run.sh", "start_utc.txt", "stderr.log", "stdout.json", "time.txt",
    "time_pid.txt", "wrapper_pid.txt",
)
ATTACK_RUN_NAME = "c30c-v5-toctou-robustness-rerun-20260807T1012-final"


class Blocked(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Blocked(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=True, allow_nan=False, sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def strict_object(raw: bytes, label: str) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in output, "duplicate JSON key:" + label)
            output[key] = value
        return output

    try:
        value = json.loads(
            raw.decode("ascii"), object_pairs_hook=unique,
            parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
            parse_float=lambda token: (_ for _ in ()).throw(ValueError(token)),
        )
    except (UnicodeDecodeError, ValueError, json.JSONDecodeError) as error:
        raise Blocked("strict JSON:" + label) from error
    need(type(value) is dict, "JSON object:" + label)
    need(raw in {canonical(value), canonical(value) + b"\n"}, "canonical JSON:" + label)
    return value


def evidence_files() -> tuple[str, ...]:
    rows = [
        "preflight/code.sha256.raw",
        "preflight/candidates.sha256.raw",
        "p0/payload_manifest.raw",
        "p0/cold_replay_receipt.raw",
        "p0/outer_verification.raw",
        "p0/root_manifest.raw",
        "p0/terminal_receipt.raw",
        "p0/final_commit_receipt.raw",
        "p0/final_commit_v2_receipt.raw",
        "p0/postcommit_checker.raw",
        "p0/postcommit_addendum.raw",
        "p0/postcommit_replay_receipt.raw",
        "p0/postcommit_replay_manifest.raw",
    ]
    for stage in ("producer", "verifier"):
        for seed in SEEDS:
            rows.extend(
                f"{stage}/{seed}/{name}"
                for name in (
                    "command.json", "provenance.json", "stdout.raw",
                    "stderr.raw", "time.raw", "exit.txt",
                )
            )
    rows.extend(
        "attacks/" + name
        for name in (
            "command.json", "provenance.json", "stdout.raw", "stderr.raw",
            "time.raw", "exit.txt",
        )
    )
    rows.extend(
        "attacks/" + name for name in (
            "validator_receipt.raw", "receipt_adapter.raw",
            "receipt_adapter_verification.raw",
        )
    )
    rows.extend("attacks/run/" + name for name in ATTACK_RUN_FILES)
    rows.extend(
        "cold/" + name
        for name in (
            "command.json", "provenance.json", "stdout.raw", "stderr.raw",
            "time.raw", "exit.txt", "trace.raw", "trace_audit.json",
            "sealed_pre.sha256.raw", "sealed_post.sha256.raw",
        )
    )
    return tuple(sorted(rows))


EXPECTED_FILES = evidence_files()
ALLOW_EMPTY = {
    relative for relative in EXPECTED_FILES if relative.endswith("/stderr.raw")
} | {"attacks/run/stderr.log"}


def exact_tree(root: Path) -> None:
    status = root.lstat()
    need(stat.S_ISDIR(status.st_mode) and not root.is_symlink(), "evidence root directory")
    actual_files: set[str] = set()
    for path in root.rglob("*"):
        relative = path.relative_to(root).as_posix()
        child = path.lstat()
        need(not path.is_symlink(), "evidence symlink:" + relative)
        if stat.S_ISDIR(child.st_mode):
            continue
        need(stat.S_ISREG(child.st_mode), "evidence regular file:" + relative)
        actual_files.add(relative)
    need(actual_files == set(EXPECTED_FILES), "exact evidence file tree")


def open_snapshot(root: Path) -> tuple[dict[str, int], dict[str, tuple[int, ...]]]:
    descriptors: dict[str, int] = {}
    identities: dict[str, tuple[int, ...]] = {}
    try:
        for relative in EXPECTED_FILES:
            path = root / relative
            need(path.resolve(strict=True).is_relative_to(root.resolve(strict=True)),
                 "evidence containment:" + relative)
            descriptor = os.open(
                path, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0)
            )
            status = os.fstat(descriptor)
            identity = (
                status.st_dev, status.st_ino, status.st_mode, status.st_nlink,
                status.st_size, status.st_mtime_ns, status.st_ctime_ns,
            )
            need(
                stat.S_ISREG(status.st_mode) and status.st_nlink == 1
                and (status.st_size > 0 or relative in ALLOW_EMPTY),
                "evidence regular singleton:" + relative,
            )
            path_status = path.lstat()
            need(
                identity == (
                    path_status.st_dev, path_status.st_ino, path_status.st_mode,
                    path_status.st_nlink, path_status.st_size,
                    path_status.st_mtime_ns, path_status.st_ctime_ns,
                ),
                "evidence opened identity:" + relative,
            )
            descriptors[relative] = descriptor
            identities[relative] = identity
    except BaseException:
        for descriptor in descriptors.values():
            os.close(descriptor)
        raise
    return descriptors, identities


def read_descriptor(descriptor: int) -> bytes:
    os.lseek(descriptor, 0, os.SEEK_SET)
    chunks: list[bytes] = []
    while block := os.read(descriptor, 1 << 20):
        chunks.append(block)
    return b"".join(chunks)


def hash_descriptor(descriptor: int) -> tuple[int, str]:
    os.lseek(descriptor, 0, os.SEEK_SET)
    state = hashlib.sha256()
    size = 0
    while block := os.read(descriptor, 1 << 20):
        state.update(block)
        size += len(block)
    return size, state.hexdigest()


def hash_path(path: Path) -> str:
    descriptor = os.open(
        path, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "hashed regular singleton:" + os.fspath(path))
        size, digest = hash_descriptor(descriptor)
        after = os.fstat(descriptor)
        current = path.lstat()
        before_identity = (
            before.st_dev, before.st_ino, before.st_mode, before.st_nlink,
            before.st_size, before.st_mtime_ns, before.st_ctime_ns,
        )
        need(
            size == before.st_size
            and before_identity == (
                after.st_dev, after.st_ino, after.st_mode, after.st_nlink,
                after.st_size, after.st_mtime_ns, after.st_ctime_ns,
            ) == (
                current.st_dev, current.st_ino, current.st_mode,
                current.st_nlink, current.st_size, current.st_mtime_ns,
                current.st_ctime_ns,
            ),
            "hashed file changed:" + os.fspath(path),
        )
        return digest
    finally:
        os.close(descriptor)


def load_pinned_trace_analyzer() -> Any:
    path = DELIVERABLES / TRACE_ANALYZER
    descriptor = os.open(
        path, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        before = os.fstat(descriptor)
        need(
            stat.S_ISREG(before.st_mode) and before.st_nlink == 1
            and 0 < before.st_size <= 4 << 20,
            "trace analyzer regular singleton",
        )
        raw = read_descriptor(descriptor)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    current = path.lstat()
    identity = (
        before.st_dev, before.st_ino, before.st_mode, before.st_nlink,
        before.st_size, before.st_mtime_ns, before.st_ctime_ns,
    )
    need(
        identity == (
            after.st_dev, after.st_ino, after.st_mode, after.st_nlink,
            after.st_size, after.st_mtime_ns, after.st_ctime_ns,
        ) == (
            current.st_dev, current.st_ino, current.st_mode, current.st_nlink,
            current.st_size, current.st_mtime_ns, current.st_ctime_ns,
        )
        and sha256(raw) == TRACE_ANALYZER_SHA256,
        "pinned trace analyzer bytes",
    )
    name = PREFIX + "_pinned_cold_trace_analyzer"
    module = types.ModuleType(name)
    module.__file__ = os.fspath(path)
    module.__package__ = ""
    module.__loader__ = None
    module.__spec__ = importlib.machinery.ModuleSpec(
        name=name, loader=None, origin=os.fspath(path)
    )
    exec(compile(raw, os.fspath(path), "exec", dont_inherit=True), module.__dict__)
    need(
        callable(getattr(module, "analyze_trace", None))
        and path.lstat() == current,
        "loaded pinned trace analyzer",
    )
    return module


def validate_provenance(
    raw: bytes, stage: str, seed: str | None, source_sha256: str,
) -> None:
    value = strict_object(raw, stage + ":provenance")
    need(
        value.get("schema") == "cm2.round306c30c.execution-provenance.v1"
        and value.get("stage") == stage
        and value.get("cwd") == os.fspath(WORKSPACE)
        and value.get("interpreter_sha256") == INTERPRETER_SHA256
        and value.get("source_sha256") == source_sha256
        and type(value.get("argv")) is list
        and all(type(item) is str for item in value["argv"]),
        "execution provenance identity:" + stage,
    )
    environment = value.get("environment")
    need(type(environment) is dict, "execution provenance environment:" + stage)
    if stage == "producer":
        need(
            value.get("seed") == int(seed or "-1")
            and value.get("hash_sentinel")
            == "CM2_C30C_HASH_SEED_SENTINEL_v1"
            and environment == {
                "HOME": "/nonexistent", "LC_ALL": "C.UTF-8",
                "PYTHONHASHSEED": seed, "TZ": "UTC",
            }
            and value.get("interpreter_flags") == {
                "dont_write_bytecode": 1, "hash_randomization": 1,
                "ignore_environment": 0, "isolated": 0,
                "no_user_site": 1, "safe_path": True,
            }
            and value.get("hash_fingerprint") == HASH_FINGERPRINTS[seed or ""],
            "controlled producer provenance:" + str(seed),
        )
    else:
        need(
            value.get("seed") is None
            and value.get("interpreter_flags", {}).get("isolated") == 1
            and value.get("interpreter_flags", {}).get("dont_write_bytecode") == 1,
            "isolated read-only provenance:" + stage,
        )


def parse_manifest(raw: bytes, label: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    try:
        lines = raw.decode("ascii").splitlines()
    except UnicodeDecodeError as error:
        raise Blocked("manifest ASCII:" + label) from error
    for line in lines:
        parts = line.split("  ", 1)
        need(
            len(parts) == 2 and len(parts[0]) == 64
            and all(character in "0123456789abcdef" for character in parts[0])
            and parts[1] and not Path(parts[1]).is_absolute()
            and ".." not in Path(parts[1]).parts and parts[1] not in rows,
            "manifest syntax:" + label,
        )
        rows[parts[1]] = parts[0]
    return rows


def closed_object(raw: bytes, label: str) -> dict[str, Any]:
    value = strict_object(raw, label)
    body = dict(value)
    object_hash = body.pop("payload_sha256", None)
    need(object_hash == sha256(canonical(body)), "closed object:" + label)
    return value


def sha_manifest_by_basename(raw: bytes, label: str) -> dict[str, str]:
    rows = parse_manifest(raw, label)
    output: dict[str, str] = {}
    for path, digest in rows.items():
        name = Path(path).name
        need(name not in output, "duplicate manifest basename:" + label)
        output[name] = digest
    return output


def validate_attack_receipt_bridge(raw: dict[str, bytes]) -> dict[str, Any]:
    watcher_raw = raw["attacks/validator_receipt.raw"]
    adapter_raw = raw["attacks/receipt_adapter.raw"]
    verification_raw = raw["attacks/receipt_adapter_verification.raw"]
    watcher = strict_object(watcher_raw, "attack watcher receipt")
    need(
        set(watcher) == {
            "validator_exit_code", "validator_result", "validator_stderr",
            "watch_status",
        }
        and watcher.get("watch_status") == "VALIDATOR_COMPLETED"
        and watcher.get("validator_exit_code") == 0
        and watcher.get("validator_stderr") == ""
        and type(watcher.get("validator_result")) is dict,
        "successful exact watcher receipt",
    )
    receipt = watcher["validator_result"]
    need(
        set(receipt) == {
            "attack_count", "authority", "baseline_result_sha256", "elapsed",
            "formal_credit", "harness_sha256", "harness_stdout_sha256",
            "manifest_authorized", "numeric_exit_code", "pre_post_sha256_identical",
            "pre_post_stat_identical", "python_sha256", "run_directory",
            "run_end_utc", "run_start_utc", "schema", "signal", "status",
            "verifier_sha256",
        }
        and receipt.get("schema")
        == "cm2.round306c30c.attack-run-receipt-validation.v1"
        and receipt.get("status") == RECEIPT_STATUS
        and receipt.get("run_directory") == ATTACK_RUN_NAME
        and receipt.get("attack_count") == 62
        and receipt.get("pre_post_sha256_identical") is True
        and receipt.get("pre_post_stat_identical") is True
        and receipt.get("numeric_exit_code") == 0
        and receipt.get("signal") is None
        and receipt.get("formal_credit") == 0
        and receipt.get("manifest_authorized") is False,
        "successful zero-credit attack receipt",
    )

    adapter = closed_object(adapter_raw, "attack receipt adapter")
    need(
        set(adapter) == {
            "formal_credit", "payload_sha256", "python_sha256",
            "receipt_file", "receipt_file_sha256", "receipt_result_sha256",
            "receipt_validator", "required_bindings", "run_directory",
            "run_files", "schema", "source_W_transition_authorized", "status",
        }
        and adapter.get("schema")
        == "cm2.round306c30c.attack-receipt-evidence-adapter.v1"
        and adapter.get("status") == ADAPTER_STATUS
        and adapter.get("run_directory")
        == ".cm2-runtime/audit/" + ATTACK_RUN_NAME
        and adapter.get("receipt_file")
        == ".cm2-runtime/audit/" + ATTACK_RUN_NAME + "-receipt-validation.json"
        and adapter.get("receipt_file_sha256") == sha256(watcher_raw)
        and adapter.get("receipt_result_sha256") == sha256(canonical(receipt))
        and adapter.get("python_sha256") == INTERPRETER_SHA256
        and adapter.get("formal_credit") == 0
        and adapter.get("source_W_transition_authorized") is False,
        "closed zero-credit attack adapter",
    )
    need(
        adapter.get("receipt_validator") == {
            "path": "deliverables/" + RECEIPT_VALIDATOR,
            "sha256": RECEIPT_VALIDATOR_SHA256,
            "replay_stdout_sha256": sha256(canonical(receipt) + b"\n"),
        },
        "adapter pins receipt validator and replay",
    )

    run_map = {
        name: {
            "sha256": sha256(raw["attacks/run/" + name]),
            "size": len(raw["attacks/run/" + name]),
        }
        for name in ATTACK_RUN_FILES
    }
    need(adapter.get("run_files") == run_map, "adapter binds all 16 raw run files")
    need(
        raw["attacks/run/stdout.json"] == raw["attacks/stdout.raw"]
        and raw["attacks/run/stderr.log"] == raw["attacks/stderr.raw"]
        and raw["attacks/run/time.txt"] == raw["attacks/time.raw"]
        and raw["attacks/run/exit_code.txt"] == raw["attacks/exit.txt"],
        "bundle attack projection equals exact run bytes",
    )
    need(
        raw["attacks/run/exit_code.txt"] == b"0\n"
        and raw["attacks/run/stderr.log"] == b""
        and raw["attacks/run/pre.sha256"] == raw["attacks/run/post.sha256"]
        and raw["attacks/run/pre.stat"] == raw["attacks/run/post.stat"],
        "raw run exit and pre/post immutability",
    )
    bindings = adapter.get("required_bindings")
    need(
        type(bindings) is dict
        and set(bindings) == {
            "harness_stdout_sha256", "numeric_exit_code", "numeric_exit_sha256",
            "post_sha256_ledger_sha256", "post_stat_ledger_sha256",
            "pre_post_sha256_identical", "pre_post_stat_identical",
            "pre_sha256_ledger_sha256", "pre_stat_ledger_sha256", "signal",
        }
        and bindings == {
            "harness_stdout_sha256": sha256(raw["attacks/run/stdout.json"]),
            "numeric_exit_sha256": sha256(raw["attacks/run/exit_code.txt"]),
            "pre_sha256_ledger_sha256": sha256(raw["attacks/run/pre.sha256"]),
            "post_sha256_ledger_sha256": sha256(raw["attacks/run/post.sha256"]),
            "pre_stat_ledger_sha256": sha256(raw["attacks/run/pre.stat"]),
            "post_stat_ledger_sha256": sha256(raw["attacks/run/post.stat"]),
            "pre_post_sha256_identical": True,
            "pre_post_stat_identical": True,
            "numeric_exit_code": 0,
            "signal": None,
        }
        and receipt.get("harness_stdout_sha256")
        == bindings["harness_stdout_sha256"],
        "adapter explicit stdout/pre/post/exit bindings",
    )

    verification = strict_object(
        verification_raw, "attack receipt adapter independent verification"
    )
    need(
        set(verification) == {
            "adapter_sha256", "formal_credit", "harness_stdout_sha256",
            "numeric_exit_code", "pre_post_sha256_identical",
            "pre_post_stat_identical", "receipt_file_sha256",
            "receipt_validator_sha256", "schema", "signal",
            "source_W_transition_authorized", "status",
        }
        and verification.get("schema")
        == "cm2.round306c30c.attack-receipt-evidence-adapter-verification.v1"
        and verification.get("status") == ADAPTER_VERIFICATION_STATUS
        and verification.get("adapter_sha256") == sha256(adapter_raw)
        and verification.get("receipt_file_sha256") == sha256(watcher_raw)
        and verification.get("receipt_validator_sha256")
        == RECEIPT_VALIDATOR_SHA256
        and verification.get("harness_stdout_sha256")
        == bindings["harness_stdout_sha256"]
        and verification.get("pre_post_sha256_identical") is True
        and verification.get("pre_post_stat_identical") is True
        and verification.get("numeric_exit_code") == 0
        and verification.get("signal") is None
        and verification.get("formal_credit") == 0
        and verification.get("source_W_transition_authorized") is False,
        "independent adapter verification retained",
    )
    return {
        "receipt_validator_sha256": RECEIPT_VALIDATOR_SHA256,
        "receipt_adapter_script_sha256": RECEIPT_ADAPTER_SHA256,
        "receipt_adapter_verifier_script_sha256": RECEIPT_ADAPTER_VERIFIER_SHA256,
        "validator_receipt_sha256": sha256(watcher_raw),
        "receipt_adapter_sha256": sha256(adapter_raw),
        "receipt_adapter_verification_sha256": sha256(verification_raw),
        "receipt_result_sha256": sha256(canonical(receipt)),
        "harness_stdout_sha256": bindings["harness_stdout_sha256"],
        "run_file_count": len(ATTACK_RUN_FILES),
        "run_files_map_sha256": sha256(canonical(run_map)),
        "pre_post_sha256_identical": True,
        "pre_post_stat_identical": True,
        "numeric_exit_code": 0,
        "signal": None,
        "formal_credit": 0,
        "source_W_transition_authorized": False,
    }


def validate_gnu_time(raw: bytes, label: str) -> None:
    """Reject signal-terminated or nonzero timed invocations fail-closed."""
    try:
        lines = raw.decode("ascii").splitlines()
    except UnicodeDecodeError as error:
        raise Blocked("GNU time ASCII:" + label) from error
    stripped = [line.strip() for line in lines]
    need(
        len([line for line in stripped if line.startswith("Command being timed:")])
        == 1,
        "GNU time command binding:" + label,
    )
    need(
        not any(line.startswith("Command terminated by signal") for line in stripped),
        "signal-terminated timed invocation:" + label,
    )
    need(
        [line for line in stripped if line.startswith("Exit status:")]
        == ["Exit status: 0"],
        "GNU time exit status:" + label,
    )


def p0_conclusion() -> dict[str, Any]:
    return {
        "original_c30a_whole_origin_exclusion_credit": 160,
        "supplemental_additional_whole_origin_exclusion_credit": 0,
        "source_W_transition": {"before": 252, "after": 92},
        "source_W_252_to_90": "FORBIDDEN",
        "D02": "BLOCKED_COMPOSITE",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def validate_p0_commit_v2(
    value: dict[str, Any], commit_raw: bytes,
    official_targets: dict[str, Any], conclusion: dict[str, Any],
    checker_raw: bytes, addendum_raw: bytes, replay_raw: bytes,
    replay_manifest_raw: bytes, replay_receipt: dict[str, Any],
) -> None:
    expected_targets = {
        P0_COLD_RECEIPT_REL: {
            "kind": "file", "sha256":
            "2b725b4c69cf188ed5ade87170c0d60705eff50abbcddeb884d6b8ceae4462b2",
            "size": 711,
        },
        P0_OUTER_VERIFICATION_REL: {
            "kind": "file", "sha256":
            "a50c5116592d9713ffb592655bb2dae1378bda39e4979dac318ba39cd7becf8f",
            "size": 665,
        },
        P0_PAYLOAD_MANIFEST_REL: {
            "kind": "file", "sha256":
            "e4dc5432124e350d436b00fa82b552a3617e120d5d9c16c41e554d149e9a4502",
            "size": 60884,
        },
        P0_ROOT_MANIFEST_REL: {
            "kind": "file", "sha256":
            "2788fe4dec1ad0c12f82e1b4c21cc78881919634fd6c2a83e99443e88ef84fbe",
            "size": 294,
        },
        "deliverables/cm2_round306c30a_supplemental_audit_closure_sealed": {
            "file_count": 286, "kind": "directory-tree", "sha256":
            "87673daab711a68206effcfd8da3c6f71fc5f9c55e652c129b13f686d6a48114",
            "total_size": 27665805,
        },
        P0_TERMINAL_RECEIPT_REL: {
            "kind": "file", "sha256":
            "1ffceef343ac6ac32c80776b899328ed50e24adbd0f09f60e0be6f7e51afb168",
            "size": 943,
        },
    }
    expected_keys = {
        "addendum_sha256", "checker_sha256", "conclusion",
        "double_replay_stages", "manifest_stage_exit_sha256",
        "official_targets", "original_commit_authority",
        "original_final_commit_sha256", "payload_sha256",
        "postcommit_manifest_member_count", "postcommit_manifest_sha256",
        "postcommit_replay_receipt_sha256", "run_root", "schema", "status",
    }
    need(
        set(value) == expected_keys
        and value.get("payload_sha256")
        == "10db49e806fb030e25318678e9576cd04d3fe1a7afeac2dc3bc68a0d428286d1"
        and value.get("schema")
        == "cm2.round306c30a.supplemental-final-commit-v2.v1"
        and value.get("status")
        == ("PASS_ADDITIVE_FINAL_COMMIT_V2_AFTER_DOUBLE_POSTPUBLICATION_"
            "REPLAY__ZERO_ADDITIONAL_CREDIT")
        and value.get("checker_sha256") == sha256(checker_raw)
        == "82d126f5f83528729fff9c56827575963819b4be92286e1d9558cf74a82e2828"
        and value.get("addendum_sha256") == sha256(addendum_raw)
        == "66c3b4f3113b4038d77c8b93e7e1c783937089e3e09f8f54434d409c780c2464"
        and value.get("postcommit_replay_receipt_sha256") == sha256(replay_raw)
        == "8c15d45770b29057f3d204055b3383e647cc91859bef0d763a2c85ca5fa4f2a8"
        and value.get("postcommit_manifest_sha256")
        == sha256(replay_manifest_raw)
        == "63c2260d47e89d7710d4c18a1c4a94255484e4769c069eec6362e4a81a535085"
        and value.get("postcommit_manifest_member_count") == 32
        and value.get("original_final_commit_sha256") == sha256(commit_raw)
        and value.get("original_commit_authority")
        == "SUPERSEDED_BY_THIS_ADDITIVE_V2_COMMIT"
        and value.get("run_root")
        == ".cm2-runtime/audit/c30a-supplemental-p0b-v5-20260807-1028b"
        and value.get("manifest_stage_exit_sha256")
        == "94ebf9e708aff94b41040be56683352c5c0c712a2906366308caabe3518b438f"
        and value.get("conclusion") == conclusion
        and value.get("official_targets") == expected_targets
        and official_targets == expected_targets,
        "P0 additive final commit v2 exact authority",
    )
    stages = value.get("double_replay_stages")
    need(
        type(stages) is dict
        and set(stages) == {"110_postcommit_replay_a", "111_postcommit_replay_b"}
        and sha256(canonical(stages))
        == "ef2f1183cd7f0e922458773f004dece41185d3631e464b59ff2e3e94bfc27fac",
        "P0 additive v2 exact double replay stages",
    )
    artifact_names = {
        "docker_create_stderr", "docker_create_stdout", "docker_inspect_post",
        "docker_inspect_post_raw", "docker_inspect_pre",
        "docker_inspect_pre_raw", "exit", "start", "stderr", "stdout", "time",
    }
    empty = {
        "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "size": 0,
    }
    for stage in stages.values():
        artifacts = stage.get("artifacts") if type(stage) is dict else None
        need(
            type(stage) is dict and set(stage) == {"artifacts", "exit_sha256"}
            and type(artifacts) is dict and set(artifacts) == artifact_names
            and all(
                type(item) is dict and set(item) == {"sha256", "size"}
                and type(item["sha256"]) is str and len(item["sha256"]) == 64
                and type(item["size"]) is int and item["size"] >= 0
                for item in artifacts.values()
            )
            and stage["exit_sha256"] == artifacts["exit"]["sha256"]
            and artifacts["stdout"] == {
                "sha256":
                "8c15d45770b29057f3d204055b3383e647cc91859bef0d763a2c85ca5fa4f2a8",
                "size": 11355,
            }
            and artifacts["stderr"] == empty
            and artifacts["docker_create_stderr"] == empty,
            "P0 additive v2 replay artifact closure",
        )
    replay_keys = {
        "addendum_sha256", "base_stages", "checker_sha256",
        "cold_replay_receipt_sha256", "conclusion",
        "core_trace_audit_payload_sha256", "historical_preflight_payload_sha256",
        "historical_stage10_fact", "official_targets",
        "original_final_commit_sha256", "outer_verification_sha256",
        "payload_manifest_sha256", "payload_sha256",
        "pipeline_precommit_receipt_sha256", "present_day_fact",
        "root_manifest_sha256", "run_root", "schema", "stage100_exit_sha256",
        "stage101_exit_sha256", "stage99_exit_sha256", "status",
        "terminal_receipt_sha256",
    }
    need(
        set(replay_receipt) == replay_keys
        and replay_receipt.get("payload_sha256")
        == "be0ca6435d2714ecd45c6bcf2dd30ac29a2fc436eb9c7ee8f7b1cf32f39e9200"
        and replay_receipt.get("schema")
        == "cm2.round306c30a.supplemental-postpublication-semantic-replay.v1"
        and replay_receipt.get("status")
        == ("PASS_POSTPUBLICATION_FULL_CORE_AND_STAGE95_TO_101_REPLAY__"
            "ZERO_ADDITIONAL_CREDIT")
        and replay_receipt.get("run_root") == value.get("run_root")
        and replay_receipt.get("conclusion") == conclusion
        and replay_receipt.get("original_final_commit_sha256") == sha256(commit_raw)
        and replay_receipt.get("official_targets") == expected_targets
        and replay_receipt.get("checker_sha256") == sha256(checker_raw)
        and replay_receipt.get("addendum_sha256") == sha256(addendum_raw)
        and replay_receipt.get("payload_manifest_sha256")
        == expected_targets[P0_PAYLOAD_MANIFEST_REL]["sha256"]
        and replay_receipt.get("cold_replay_receipt_sha256")
        == expected_targets[P0_COLD_RECEIPT_REL]["sha256"]
        and replay_receipt.get("outer_verification_sha256")
        == expected_targets[P0_OUTER_VERIFICATION_REL]["sha256"]
        and replay_receipt.get("root_manifest_sha256")
        == expected_targets[P0_ROOT_MANIFEST_REL]["sha256"]
        and replay_receipt.get("terminal_receipt_sha256")
        == expected_targets[P0_TERMINAL_RECEIPT_REL]["sha256"],
        "P0 postcommit replay receipt semantic closure",
    )
    suffixes = {
        "docker_create_stderr": "docker_create.stderr.raw",
        "docker_create_stdout": "docker_create.stdout.raw",
        "docker_inspect_post": "docker_inspect_post.json",
        "docker_inspect_post_raw": "docker_inspect_post.raw.json",
        "docker_inspect_pre": "docker_inspect_pre.json",
        "docker_inspect_pre_raw": "docker_inspect_pre.raw.json",
        "exit": "exit.json", "start": "start.json", "stderr": "stderr.raw",
        "stdout": "stdout.raw", "time": "time.txt",
    }
    run_root = value["run_root"]
    expected_manifest = {
        run_root + "/cm2_round306c30a_supplemental_audit_closure_"
        "pipeline_precommit_receipt.json":
            replay_receipt["pipeline_precommit_receipt_sha256"],
        P0_COLD_RECEIPT_REL: expected_targets[P0_COLD_RECEIPT_REL]["sha256"],
        P0_FINAL_COMMIT_REL: sha256(commit_raw),
        P0_OUTER_VERIFICATION_REL: expected_targets[P0_OUTER_VERIFICATION_REL]["sha256"],
        P0_PAYLOAD_MANIFEST_REL: expected_targets[P0_PAYLOAD_MANIFEST_REL]["sha256"],
        P0_POSTCOMMIT_REPLAY_RECEIPT_REL: sha256(replay_raw),
        P0_ROOT_MANIFEST_REL: expected_targets[P0_ROOT_MANIFEST_REL]["sha256"],
        P0_TERMINAL_RECEIPT_REL: expected_targets[P0_TERMINAL_RECEIPT_REL]["sha256"],
        P0_POSTCOMMIT_ADDENDUM_REL: sha256(addendum_raw),
        P0_POSTCOMMIT_CHECKER_REL: sha256(checker_raw),
    }
    for stage_name, stage in stages.items():
        for artifact_name, artifact in stage["artifacts"].items():
            expected_manifest[
                run_root + "/stages/" + stage_name + "/" + suffixes[artifact_name]
            ] = artifact["sha256"]
    manifest_rows = parse_manifest(replay_manifest_raw, "P0 postcommit replay manifest")
    need(
        len(expected_manifest) == 32 and manifest_rows == expected_manifest,
        "P0 exact 32-member postcommit manifest bindings",
    )


def validate_p0_chain(raw: dict[str, bytes]) -> dict[str, str]:
    need(
        P0_SUPPLEMENTAL_ROOT_MANIFEST_SHA256 is not None
        and P0_SUPPLEMENTAL_OUTER_VERIFICATION_SHA256 is not None
        and P0_SUPPLEMENTAL_TERMINAL_RECEIPT_SHA256 is not None
        and P0_SUPPLEMENTAL_FINAL_COMMIT_SHA256 is not None
        and P0_SUPPLEMENTAL_FINAL_COMMIT_V2_SHA256 is not None,
        "P0_SUPPLEMENTAL_FINAL_PINS_UNSET",
    )
    payload_raw = raw["p0/payload_manifest.raw"]
    cold_raw = raw["p0/cold_replay_receipt.raw"]
    outer_raw = raw["p0/outer_verification.raw"]
    root_raw = raw["p0/root_manifest.raw"]
    terminal_raw = raw["p0/terminal_receipt.raw"]
    commit_raw = raw["p0/final_commit_receipt.raw"]
    commit_v2_raw = raw["p0/final_commit_v2_receipt.raw"]
    checker_raw = raw["p0/postcommit_checker.raw"]
    addendum_raw = raw["p0/postcommit_addendum.raw"]
    replay_raw = raw["p0/postcommit_replay_receipt.raw"]
    replay_manifest_raw = raw["p0/postcommit_replay_manifest.raw"]
    replay_receipt = closed_object(replay_raw, "P0 postcommit replay receipt")
    need(
        sha256(root_raw) == P0_SUPPLEMENTAL_ROOT_MANIFEST_SHA256
        and sha256(outer_raw) == P0_SUPPLEMENTAL_OUTER_VERIFICATION_SHA256
        and sha256(terminal_raw) == P0_SUPPLEMENTAL_TERMINAL_RECEIPT_SHA256
        and sha256(commit_raw) == P0_SUPPLEMENTAL_FINAL_COMMIT_SHA256
        and sha256(commit_v2_raw) == P0_SUPPLEMENTAL_FINAL_COMMIT_V2_SHA256,
        "externally pinned P0 supplemental authority",
    )
    root_rows = parse_manifest(root_raw, "P0 root")
    need(
        root_rows == {
            P0_PAYLOAD_MANIFEST_REL: sha256(payload_raw),
            P0_OUTER_VERIFICATION_REL: sha256(outer_raw),
        },
        "P0 exact two-member root closure",
    )
    cold = closed_object(cold_raw, "P0 cold receipt")
    outer = closed_object(outer_raw, "P0 outer verification")
    terminal = closed_object(terminal_raw, "P0 terminal receipt")
    commit = closed_object(commit_raw, "P0 final commit")
    commit_v2 = closed_object(commit_v2_raw, "P0 final commit v2")
    precommit = commit.get("pipeline_precommit_receipt", {})
    terminal_replay = precommit.get("terminal_replay", {}) if type(precommit) is dict else {}
    official_targets = commit.get("official_targets", {})
    expected_target_names = {
        "deliverables/cm2_round306c30a_supplemental_audit_closure_sealed",
        P0_PAYLOAD_MANIFEST_REL,
        P0_COLD_RECEIPT_REL,
        P0_OUTER_VERIFICATION_REL,
        P0_ROOT_MANIFEST_REL,
        P0_TERMINAL_RECEIPT_REL,
    }
    conclusion = p0_conclusion()
    need(
        cold.get("schema")
        == "cm2.round306c30a.supplemental-audit-cold-receipt.v1"
        and cold.get("status")
        == "PASS_PAYLOAD_AND_AUTHORITATIVE_FULL_TRACE_COLD_REPLAY"
        and cold.get("payload_manifest_sha256") == sha256(payload_raw)
        and cold.get("conclusion") == conclusion
        and outer.get("schema")
        == "cm2.round306c30a.supplemental-audit-outer-verification.v1"
        and outer.get("status")
        == "PASS_SUPPLEMENTAL_AUDIT_CLOSURE__ZERO_ADDITIONAL_CREDIT"
        and outer.get("payload_manifest_sha256") == sha256(payload_raw)
        and outer.get("cold_replay_receipt_sha256") == sha256(cold_raw)
        and outer.get("conclusion") == conclusion
        and terminal.get("schema")
        == "cm2.round306c30a.supplemental-audit-terminal-receipt.v1"
        and terminal.get("status")
        == "PASS_TERMINAL_C30A_SUPPLEMENTAL_AUDIT_AUTHORIZATION__252_TO_92_ONLY"
        and terminal.get("root_manifest_sha256") == sha256(root_raw)
        and terminal.get("payload_manifest_sha256") == sha256(payload_raw)
        and terminal.get("outer_verification_sha256") == sha256(outer_raw)
        and terminal.get("cold_replay_receipt_sha256") == sha256(cold_raw)
        and terminal.get("authority_condition")
        == "REQUIRES_POST_PUBLICATION_STAGE100_REPLAY_AND_FINAL_COMMIT"
        and terminal.get("conclusion") == conclusion,
        "P0 five-layer terminal closure and 252-to-90 prohibition",
    )
    need(
        commit.get("schema")
        == "cm2.round306c30a.supplemental-final-commit.v5"
        and commit.get("status")
        == "PASS_FINAL_COMMIT_AFTER_POST_PUBLICATION_REPLAY__ZERO_ADDITIONAL_CREDIT"
        and commit.get("conclusion") == conclusion
        and type(precommit) is dict
        and precommit.get("schema")
        == "cm2.round306c30a.supplemental-pipeline-precommit.v5"
        and precommit.get("status")
        == "PASS_STAGE100_AND_SIX_OFFICIAL_TARGETS__READY_TO_COMMIT"
        and precommit.get("conclusion") == conclusion
        and terminal_replay.get("schema")
        == "cm2.round306c30a.supplemental-terminal-replay.v5"
        and terminal_replay.get("status")
        == "PASS_FULL_FIVE_LAYER_TERMINAL_REPLAY__252_TO_92_ONLY"
        and terminal_replay.get("payload_manifest_sha256") == sha256(payload_raw)
        and terminal_replay.get("cold_replay_receipt_sha256") == sha256(cold_raw)
        and terminal_replay.get("outer_verification_sha256") == sha256(outer_raw)
        and terminal_replay.get("root_manifest_sha256") == sha256(root_raw)
        and terminal_replay.get("terminal_receipt_sha256") == sha256(terminal_raw)
        and terminal_replay.get("conclusion") == conclusion
        and commit.get("pipeline_precommit_receipt_sha256")
        == sha256(canonical(precommit) + b"\n")
        and official_targets == precommit.get("official_targets")
        and type(official_targets) is dict
        and set(official_targets) == expected_target_names
        and official_targets[P0_PAYLOAD_MANIFEST_REL].get("sha256")
        == sha256(payload_raw)
        and official_targets[P0_COLD_RECEIPT_REL].get("sha256")
        == sha256(cold_raw)
        and official_targets[P0_OUTER_VERIFICATION_REL].get("sha256")
        == sha256(outer_raw)
        and official_targets[P0_ROOT_MANIFEST_REL].get("sha256")
        == sha256(root_raw)
        and official_targets[P0_TERMINAL_RECEIPT_REL].get("sha256")
        == sha256(terminal_raw)
        and commit.get("stage100_exit_sha256")
        == precommit.get("stage100_artifacts", {}).get("exit", {}).get("sha256"),
        "P0 post-stage100 final commit closure",
    )
    validate_p0_commit_v2(
        commit_v2, commit_raw, official_targets, conclusion,
        checker_raw, addendum_raw, replay_raw, replay_manifest_raw, replay_receipt,
    )
    return {
        "root_manifest_sha256": sha256(root_raw),
        "outer_verification_sha256": sha256(outer_raw),
        "terminal_receipt_file_sha256": sha256(terminal_raw),
        "terminal_receipt_object_sha256": terminal["payload_sha256"],
        "final_commit_receipt_sha256": sha256(commit_raw),
        "final_commit_v2_receipt_sha256": sha256(commit_v2_raw),
    }


def validate_evidence(
    raw: dict[str, bytes], trace_raw: bytes, trace_analyzer: Any,
) -> dict[str, Any]:
    validate_p0_chain(raw)
    code = sha_manifest_by_basename(
        raw["preflight/code.sha256.raw"], "code preflight"
    )
    need(
        code == {
            "python": INTERPRETER_SHA256,
            PREFIX + "_producer.py": PRODUCER_SHA256,
            PREFIX + "_independent_verifier.py": VERIFIER_SHA256,
            PREFIX + "_attack_harness.py": HARNESS_SHA256,
            TRACE_ANALYZER: TRACE_ANALYZER_SHA256,
            RECEIPT_VALIDATOR: RECEIPT_VALIDATOR_SHA256,
            RECEIPT_ADAPTER: RECEIPT_ADAPTER_SHA256,
            RECEIPT_ADAPTER_VERIFIER: RECEIPT_ADAPTER_VERIFIER_SHA256,
        },
        "preflight executable pins including receipt bridge",
    )
    for seed in SEEDS:
        producer = f"producer/{seed}/"
        verifier = f"verifier/{seed}/"
        validate_gnu_time(raw[producer + "time.raw"], "producer:" + seed)
        need(raw[producer + "exit.txt"] == b"0\n", "producer exit:" + seed)
        need(raw[producer + "stdout.raw"] == PRODUCER_STDOUT, "producer stdout:" + seed)
        need(raw[producer + "stderr.raw"] == b"", "producer stderr:" + seed)
        validate_provenance(
            raw[producer + "provenance.json"], "producer", seed, PRODUCER_SHA256
        )
        validate_gnu_time(raw[verifier + "time.raw"], "verifier:" + seed)
        need(raw[verifier + "exit.txt"] == b"0\n", "verifier exit:" + seed)
        need(raw[verifier + "stderr.raw"] == b"", "verifier stderr:" + seed)
        output = strict_object(raw[verifier + "stdout.raw"], "verifier stdout:" + seed)
        need(
            output.get("status") == VERIFIER_STATUS
            and output.get("candidate_result_sha256") == RESULT_OBJECT_SHA256
            and output.get("formal_credit") == 0
            and output.get("manifest_authorized") is False,
            "verifier candidate-only result:" + seed,
        )
        validate_provenance(
            raw[verifier + "provenance.json"], "verifier", None, VERIFIER_SHA256
        )
    need(
        raw["verifier/30630071/stdout.raw"]
        == raw["verifier/30630929/stdout.raw"],
        "dual candidate verifier stdout byte identity",
    )
    validate_gnu_time(raw["attacks/time.raw"], "attacks")
    need(raw["attacks/exit.txt"] == b"0\n", "attack harness exit")
    need(raw["attacks/stderr.raw"] == b"", "attack harness stderr")
    attacks = strict_object(raw["attacks/stdout.raw"], "attack harness stdout")
    need(
        attacks.get("status") == HARNESS_STATUS
        and attacks.get("attack_count") == 62
        and type(attacks.get("attacks")) is list
        and len(attacks["attacks"]) == 62
        and attacks.get("formal_credit") == 0
        and attacks.get("manifest_authorized") is False,
        "62 coherent attacks",
    )
    validate_provenance(
        raw["attacks/provenance.json"], "attacks", None, HARNESS_SHA256
    )
    receipt_authority = validate_attack_receipt_bridge(raw)
    validate_gnu_time(raw["cold/time.raw"], "cold")
    need(raw["cold/exit.txt"] == b"0\n", "cold replay exit")
    need(raw["cold/stderr.raw"] == b"", "cold replay stderr")
    need(
        raw["cold/stdout.raw"] == raw["verifier/30630071/stdout.raw"],
        "cold replay stdout identity",
    )
    cold_provenance = strict_object(
        raw["cold/provenance.json"], "cold:provenance"
    )
    validate_provenance(
        raw["cold/provenance.json"], "cold", None, VERIFIER_SHA256
    )
    need(bool(cold_provenance["argv"]), "cold provenance argv")
    candidate = Path(cold_provenance["argv"][-1])
    if not candidate.is_absolute():
        candidate = WORKSPACE / candidate
    try:
        recomputed_trace = trace_analyzer.analyze_trace(
            trace_raw, raw["cold/stdout.raw"], raw["cold/stderr.raw"],
            raw["cold/time.raw"], candidate,
        )
    except (OSError, RuntimeError, TypeError, ValueError) as error:
        raise Blocked("independent cold trace recomputation") from error
    trace = strict_object(raw["cold/trace_audit.json"], "cold trace audit")
    need(
        trace == recomputed_trace
        and trace.get("status")
        == "PASS_C30C_COLD_TRACE_ZERO_PROTECTED_MUTATION"
        and trace.get("exit_status") == 0
        and trace.get("top_level_stdout_writes") == 1
        and trace.get("stderr_bytes") == 0
        and trace.get("protected_write_capable_opens") == 0
        and trace.get("protected_path_mutations") == 0
        and trace.get("protected_fd_writes") == 0
        and trace.get("historical_candidate_reads") == 0
        and trace.get("trace_sha256") == sha256(trace_raw)
        and trace.get("network_syscalls") == 0
        and trace.get("candidate_member_count") == 6,
        "cold replay trace fail-close",
    )
    need(
        raw["cold/sealed_pre.sha256.raw"]
        == raw["cold/sealed_post.sha256.raw"],
        "cold sealed pre/post identity",
    )
    return receipt_authority


def normalized_tar_info(name: str, size: int) -> tarfile.TarInfo:
    info = tarfile.TarInfo(name)
    info.size = size
    info.mode = 0o600
    info.uid = 0
    info.gid = 0
    info.uname = ""
    info.gname = ""
    info.mtime = 0
    return info


def fsync_directory(path: Path) -> None:
    descriptor = os.open(
        path, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC
        | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def rename_noreplace(staging: Path, target: Path) -> None:
    libc = ctypes.CDLL(None, use_errno=True)
    function = getattr(libc, "renameat2", None)
    need(function is not None, "renameat2 RENAME_NOREPLACE available")
    function.argtypes = [
        ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p,
        ctypes.c_uint,
    ]
    function.restype = ctypes.c_int
    if function(-100, os.fsencode(staging), -100, os.fsencode(target), 1) != 0:
        error = ctypes.get_errno()
        if error == errno.EEXIST:
            raise Blocked("bundle target already exists")
        raise OSError(error, os.strerror(error), os.fspath(target))


def build_bundle(evidence_root: Path, output: Path) -> dict[str, Any]:
    need(
        P0_SUPPLEMENTAL_ROOT_MANIFEST_SHA256 is not None
        and P0_SUPPLEMENTAL_OUTER_VERIFICATION_SHA256 is not None
        and P0_SUPPLEMENTAL_TERMINAL_RECEIPT_SHA256 is not None
        and P0_SUPPLEMENTAL_FINAL_COMMIT_SHA256 is not None
        and P0_SUPPLEMENTAL_FINAL_COMMIT_V2_SHA256 is not None,
        "P0_SUPPLEMENTAL_FINAL_PINS_UNSET",
    )
    evidence_root = Path(os.path.abspath(os.fspath(evidence_root)))
    output = Path(os.path.abspath(os.fspath(output)))
    need(output.parent.is_dir() and not output.parent.is_symlink(), "bundle output parent")
    try:
        output.lstat()
    except FileNotFoundError:
        pass
    else:
        raise Blocked("bundle target already exists")
    exact_tree(evidence_root)
    descriptors, identities = open_snapshot(evidence_root)
    staging: Path | None = None
    try:
        raw = {
            relative: read_descriptor(descriptor)
            for relative, descriptor in descriptors.items()
            if relative != "cold/trace.raw"
        }
        trace_raw = read_descriptor(descriptors["cold/trace.raw"])
        trace_size = len(trace_raw)
        trace_sha256 = sha256(trace_raw)
        need(trace_size == identities["cold/trace.raw"][4], "trace byte count")
        trace_analyzer = load_pinned_trace_analyzer()
        receipt_authority = validate_evidence(raw, trace_raw, trace_analyzer)
        rows = [
            {
                "path": relative,
                "size": (
                    trace_size if relative == "cold/trace.raw"
                    else len(raw[relative])
                ),
                "sha256": (
                    trace_sha256 if relative == "cold/trace.raw"
                    else sha256(raw[relative])
                ),
            }
            for relative in EXPECTED_FILES
        ]
        p0_authority = validate_p0_chain(raw)
        internal = {
            "schema": "cm2.round306c30c.audit-evidence-bundle-manifest.v1",
            "formal_credit": 0,
            "P0_supplemental_authority": p0_authority,
            "producer_sha256": PRODUCER_SHA256,
            "independent_verifier_sha256": VERIFIER_SHA256,
            "attack_harness_sha256": HARNESS_SHA256,
            "cold_trace_analyzer_sha256": TRACE_ANALYZER_SHA256,
            "receipt_validator_sha256": RECEIPT_VALIDATOR_SHA256,
            "receipt_adapter_sha256": RECEIPT_ADAPTER_SHA256,
            "receipt_adapter_independent_verifier_sha256": (
                RECEIPT_ADAPTER_VERIFIER_SHA256
            ),
            "attack_receipt_authority": receipt_authority,
            "member_count": len(rows),
            "members": rows,
        }
        internal_raw = canonical(internal) + b"\n"
        descriptor, staging_name = tempfile.mkstemp(
            prefix="." + output.name + ".staging-", dir=output.parent
        )
        staging = Path(staging_name)
        try:
            with os.fdopen(descriptor, "wb") as raw_output:
                with gzip.GzipFile(
                    filename="", mode="wb", fileobj=raw_output,
                    compresslevel=9, mtime=0,
                ) as compressed:
                    with tarfile.open(
                        fileobj=compressed, mode="w|", format=tarfile.USTAR_FORMAT
                    ) as archive:
                        archive.addfile(
                            normalized_tar_info("bundle_manifest.json", len(internal_raw)),
                            io.BytesIO(internal_raw),
                        )
                        for relative in EXPECTED_FILES:
                            os.lseek(descriptors[relative], 0, os.SEEK_SET)
                            with os.fdopen(os.dup(descriptors[relative]), "rb") as source:
                                archive.addfile(
                                    normalized_tar_info(
                                        relative,
                                        trace_size if relative == "cold/trace.raw"
                                        else len(raw[relative]),
                                    ),
                                    source,
                                )
                raw_output.flush()
                os.fsync(raw_output.fileno())
            os.chmod(staging, 0o600)
            exact_tree(evidence_root)
            for relative, identity in identities.items():
                current = (evidence_root / relative).lstat()
                need(
                    identity == (
                        current.st_dev, current.st_ino, current.st_mode,
                        current.st_nlink, current.st_size,
                        current.st_mtime_ns, current.st_ctime_ns,
                    ),
                    "evidence changed during bundle:" + relative,
                )
            with staging.open("rb") as stream:
                need(stream.read(2) == b"\x1f\x8b", "bundle gzip header")
            bundle_sha256 = hash_path(staging)
            rename_noreplace(staging, output)
            staging = None
            fsync_directory(output.parent)
            need(hash_path(output) == bundle_sha256, "published bundle hash")
        finally:
            if staging is not None and staging.exists() and not staging.is_symlink():
                staging.unlink()
        return {
            "schema": "cm2.round306c30c.audit-evidence-bundle-build.v1",
            "status": "PASS_DETERMINISTIC_RAW_EVIDENCE_BUNDLE__ZERO_FORMAL_CREDIT",
            "bundle": os.fspath(output),
            "bundle_sha256": bundle_sha256,
            "raw_member_count": len(EXPECTED_FILES),
            "formal_credit": 0,
            "source_W_transition_authorized": False,
        }
    finally:
        for descriptor in descriptors.values():
            os.close(descriptor)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-dir", required=True, type=Path)
    parser.add_argument("--output-bundle", required=True, type=Path)
    arguments = parser.parse_args()
    try:
        output = build_bundle(arguments.evidence_dir, arguments.output_bundle)
    except (Blocked, OSError, ValueError, KeyError, TypeError) as error:
        print(canonical({
            "schema": "cm2.round306c30c.audit-evidence-bundle-build.v1",
            "status": "BLOCKED_FAIL_CLOSED",
            "error": str(error),
            "formal_credit": 0,
            "source_W_transition_authorized": False,
        }).decode("ascii"))
        return 1
    print(canonical(output).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
