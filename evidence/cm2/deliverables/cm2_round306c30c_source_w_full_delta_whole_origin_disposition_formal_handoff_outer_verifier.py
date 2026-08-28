#!/usr/bin/env python3
"""Mint the C30c outer handoff verification from retained raw evidence.

This program never runs the producer, mathematical verifier, or attack
harness.  It independently checks their retained bytes, the deterministic
audit bundle, the payload-manifest-first replay, the exact six-file seal, and
the P0 five-layer chain plus its post-stage100 final commit.  The emitted verification remains
conditional until it is pinned by the two-member C30c root manifest and the
root manifest-first sealed verifier succeeds.

The five P0 hashes below bind the externally published supplemental authority.
of that authority.  With any unset pin this program fails closed before it can
create an output file.
"""
from __future__ import annotations

import argparse
import ctypes
import errno
import gzip
import hashlib
import importlib.machinery
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

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent
PREFIX = "cm2_round306c30c_source_w_full_delta_whole_origin_disposition"
P0_PREFIX = "cm2_round306c30a_supplemental_audit_closure"

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
TRACE_ANALYZER_SHA256 = "a9f6c95a0def5f241ecbe25fc815c51a606b11a494b20fb43fbf82713f54732b"
INTERPRETER_SHA256 = "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118"
RESULT_OBJECT_SHA256 = "df4531942e743389f5e8f85b2d013132f0808f562c21f430e7904577d67087d4"
PRODUCER_STDOUT_SHA256 = "24c3c857f97a290db2e21a8713dfc645428311d94a37909aa845b85467f76eb6"

SEEDS = ("30630071", "30630929")
HASH_FINGERPRINTS = {
    "30630071": 5384816073292471411,
    "30630929": -4496445986928603988,
}
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
ATTACK_RUN_NAME = "c30c-v5-toctou-robustness-rerun-20260807T1012-final"
ATTACK_RUN_FILES = (
    "command.txt", "end_utc.txt", "exit_code.txt", "observed_child_pids.txt",
    "post.sha256", "post.stat", "pre.sha256", "pre.stat", "provenance.json",
    "run.sh", "start_utc.txt", "stderr.log", "stdout.json", "time.txt",
    "time_pid.txt", "wrapper_pid.txt",
)
PAYLOAD_REPLAY_STATUS = (
    "PASS_PAYLOAD_MANIFEST_FIRST_C30C__READY_FOR_OUTER_HANDOFF__"
    "ZERO_FORMAL_CREDIT"
)
FORMAL_STATUS = (
    "PASS_FORMAL_C30C__80_DELTA_H_CELLS__2_RESOLVED_MIXED__"
    "SOURCE_W_80_TO_78__D02_STILL_BLOCKED"
)

P0_PAYLOAD_MANIFEST = P0_PREFIX + "_payload_manifest.sha256"
P0_COLD_RECEIPT = P0_PREFIX + "_cold_replay_receipt.json"
P0_OUTER_VERIFICATION = P0_PREFIX + "_outer_verification.json"
P0_ROOT_MANIFEST = P0_PREFIX + "_root_manifest.sha256"
P0_TERMINAL_RECEIPT = P0_PREFIX + "_terminal_checker_receipt.json"
P0_FINAL_COMMIT = P0_PREFIX + "_final_commit_receipt.json"
P0_FINAL_COMMIT_V2 = P0_PREFIX + "_final_commit_v2_receipt.json"
P0_POSTCOMMIT_CHECKER = P0_PREFIX + "_v5_postcommit_replay_checker.py"
P0_POSTCOMMIT_ADDENDUM = P0_PREFIX + "_v5_postcommit_addendum.md"
P0_POSTCOMMIT_REPLAY_RECEIPT = P0_PREFIX + "_postcommit_replay_receipt.json"
P0_POSTCOMMIT_REPLAY_MANIFEST = P0_PREFIX + "_postcommit_replay_manifest.sha256"

PAYLOAD_MANIFEST = PREFIX + "_payload_manifest.sha256"
EVIDENCE_BUNDLE = PREFIX + "_audit_evidence.tar.gz"
OUTER_VERIFICATION = PREFIX + "_verification.json"
SEALED_DIR = "cm2_round306c30c_sealed"
PRODUCER = PREFIX + "_producer.py"
VERIFIER = PREFIX + "_independent_verifier.py"
HARNESS = PREFIX + "_attack_harness.py"
TRACE_ANALYZER = PREFIX + "_cold_trace_analyzer.py"
SEALED_VERIFIER = PREFIX + "_manifest_first_sealed_verifier.py"

CANDIDATE_SPECS = {
    "cm2_round306c30b_python_flint_runtime_attestation.json": {
        "size": 30352,
        "sha256": "6b48cd0ca3fd53f9fdd457cc3c1106055e12db4d4ad999fcfd1fc89ad36b95df",
    },
    PREFIX + "_combined_boundary_atomic_owner_join_ledger.jsonl.gz": {
        "size": 14320015,
        "sha256": "63f004bdb065d8674ecfde9eb957f3477ee6c3f806064ef8f151850cd391d251",
    },
    PREFIX + "_delta_h_cell_ledger.jsonl.gz": {
        "size": 727361,
        "sha256": "acbd71e9155d81d17ae4b42eecd31f0fc9d4bb91ac36aa93a7ab7df08e3dee50",
    },
    PREFIX + "_inherited_h_cell_ledger.jsonl.gz": {
        "size": 719350,
        "sha256": "d4142d7748e0546184542bea7b3b337c9f33e7312efa2e7c5271d2a9dba30abd",
    },
    PREFIX + "_result.json": {
        "size": 11697,
        "sha256": "96c1e9f627bd6113fc56f7b6d35856581b57b4afde049e997b10eef3f8c706f1",
    },
    PREFIX + "_whole_origin_ledger.jsonl.gz": {
        "size": 4473069,
        "sha256": "48a3e612de84004ba746d93d492e8f3e9f587ebf6b3574615fa946dddf21a573",
    },
}
CANDIDATE_FILES = tuple(sorted(CANDIDATE_SPECS))

PAYLOAD_MEMBERS = tuple(sorted((
    "cm2_round306c30a_python_flint_requirements.lock",
    "cm2_round306c30a_python_flint_runtime_lock.json",
    ("cm2_round306c30a_runtime/python_flint-0.9.0-cp310-abi3-"
     "manylinux2014_x86_64.manylinux_2_17_x86_64.whl"),
    "cm2_round306c30b_python_flint_runtime_attestation_auditor.py",
    P0_PAYLOAD_MANIFEST,
    P0_COLD_RECEIPT,
    P0_OUTER_VERIFICATION,
    P0_ROOT_MANIFEST,
    P0_TERMINAL_RECEIPT,
    P0_FINAL_COMMIT,
    P0_FINAL_COMMIT_V2,
    P0_POSTCOMMIT_CHECKER,
    P0_POSTCOMMIT_ADDENDUM,
    P0_POSTCOMMIT_REPLAY_RECEIPT,
    P0_POSTCOMMIT_REPLAY_MANIFEST,
    PRODUCER,
    VERIFIER,
    HARNESS,
    TRACE_ANALYZER,
    PREFIX + "_formal_handoff_verification.schema.json",
    PREFIX + "_audit_evidence_bundle_builder.py",
    PREFIX + "_formal_handoff_outer_verifier.py",
    PREFIX + "_publication_manifest_builder.py",
    SEALED_VERIFIER,
    RECEIPT_VALIDATOR,
    RECEIPT_ADAPTER,
    RECEIPT_ADAPTER_VERIFIER,
    EVIDENCE_BUNDLE,
    PREFIX + "_cold_replay.md",
    PREFIX + "_report.md",
    *(SEALED_DIR + "/" + filename for filename in CANDIDATE_FILES),
)))


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
        "attacks/" + name for name in (
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
        "cold/" + name for name in (
            "command.json", "provenance.json", "stdout.raw", "stderr.raw",
            "time.raw", "exit.txt", "trace.raw", "trace_audit.json",
            "sealed_pre.sha256.raw", "sealed_post.sha256.raw",
        )
    )
    return tuple(sorted(rows))


BUNDLE_MEMBERS = evidence_files()
PAYLOAD_REPLAY_FILES = tuple(sorted((
    "manifest_pre.raw", "manifest_post.raw", "stdout.raw", "stderr.raw",
    "exit.txt", "time.raw", "trace.raw", "trace_audit.json",
    "sealed_pre.sha256.raw", "sealed_post.sha256.raw", "provenance.json",
)))


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


def closed_object(raw: bytes, label: str) -> dict[str, Any]:
    value = strict_object(raw, label)
    body = dict(value)
    object_hash = body.pop("payload_sha256", None)
    need(object_hash == sha256(canonical(body)), "closed object:" + label)
    return value


def validate_attack_receipt_bridge(raw: dict[str, bytes]) -> dict[str, Any]:
    """Independently bind the completed-run receipt to all retained bytes."""
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
    need(
        set(run_map) == set(ATTACK_RUN_FILES)
        and adapter.get("run_files") == run_map,
        "adapter binds all 16 raw run files",
    )
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


def identity(status: os.stat_result) -> tuple[int, ...]:
    return (
        status.st_dev, status.st_ino, status.st_mode, status.st_nlink,
        status.st_size, status.st_mtime_ns, status.st_ctime_ns,
    )


def open_capture(path: Path) -> dict[str, Any]:
    absolute = Path(os.path.abspath(os.fspath(path)))
    need(absolute.resolve(strict=True).is_relative_to(WORKSPACE.resolve(strict=True)),
         "capture containment:" + os.fspath(path))
    descriptor = os.open(
        absolute, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular singleton:" + os.fspath(path))
        current = absolute.lstat()
        need(identity(before) == identity(current), "opened identity:" + os.fspath(path))
    except BaseException:
        os.close(descriptor)
        raise
    return {"path": absolute, "fd": descriptor, "identity": identity(before)}


def read_capture(capture: dict[str, Any], maximum: int = 64 << 20) -> bytes:
    need(capture["identity"][4] <= maximum, "capture size:" + os.fspath(capture["path"]))
    os.lseek(capture["fd"], 0, os.SEEK_SET)
    chunks: list[bytes] = []
    while block := os.read(capture["fd"], 1 << 20):
        chunks.append(block)
    raw = b"".join(chunks)
    need(len(raw) == capture["identity"][4], "capture byte count")
    return raw


def hash_capture(capture: dict[str, Any]) -> str:
    os.lseek(capture["fd"], 0, os.SEEK_SET)
    state = hashlib.sha256()
    count = 0
    while block := os.read(capture["fd"], 1 << 20):
        state.update(block)
        count += len(block)
    need(count == capture["identity"][4], "hash byte count")
    return state.hexdigest()


def require_current(capture: dict[str, Any]) -> None:
    after = os.fstat(capture["fd"])
    current = capture["path"].lstat()
    need(
        capture["identity"] == identity(after) == identity(current),
        "capture changed:" + os.fspath(capture["path"]),
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
    prefix = "deliverables/" + P0_PREFIX
    expected_targets = {
        prefix + "_cold_replay_receipt.json": {
            "kind": "file", "sha256":
            "2b725b4c69cf188ed5ade87170c0d60705eff50abbcddeb884d6b8ceae4462b2",
            "size": 711,
        },
        prefix + "_outer_verification.json": {
            "kind": "file", "sha256":
            "a50c5116592d9713ffb592655bb2dae1378bda39e4979dac318ba39cd7becf8f",
            "size": 665,
        },
        prefix + "_payload_manifest.sha256": {
            "kind": "file", "sha256":
            "e4dc5432124e350d436b00fa82b552a3617e120d5d9c16c41e554d149e9a4502",
            "size": 60884,
        },
        prefix + "_root_manifest.sha256": {
            "kind": "file", "sha256":
            "2788fe4dec1ad0c12f82e1b4c21cc78881919634fd6c2a83e99443e88ef84fbe",
            "size": 294,
        },
        prefix + "_sealed": {
            "file_count": 286, "kind": "directory-tree", "sha256":
            "87673daab711a68206effcfd8da3c6f71fc5f9c55e652c129b13f686d6a48114",
            "total_size": 27665805,
        },
        prefix + "_terminal_checker_receipt.json": {
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
        == expected_targets[prefix + "_payload_manifest.sha256"]["sha256"]
        and replay_receipt.get("cold_replay_receipt_sha256")
        == expected_targets[prefix + "_cold_replay_receipt.json"]["sha256"]
        and replay_receipt.get("outer_verification_sha256")
        == expected_targets[prefix + "_outer_verification.json"]["sha256"]
        and replay_receipt.get("root_manifest_sha256")
        == expected_targets[prefix + "_root_manifest.sha256"]["sha256"]
        and replay_receipt.get("terminal_receipt_sha256")
        == expected_targets[prefix + "_terminal_checker_receipt.json"]["sha256"],
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
        "deliverables/" + P0_COLD_RECEIPT:
            expected_targets[prefix + "_cold_replay_receipt.json"]["sha256"],
        "deliverables/" + P0_FINAL_COMMIT: sha256(commit_raw),
        "deliverables/" + P0_OUTER_VERIFICATION:
            expected_targets[prefix + "_outer_verification.json"]["sha256"],
        "deliverables/" + P0_PAYLOAD_MANIFEST:
            expected_targets[prefix + "_payload_manifest.sha256"]["sha256"],
        "deliverables/" + P0_POSTCOMMIT_REPLAY_RECEIPT: sha256(replay_raw),
        "deliverables/" + P0_ROOT_MANIFEST:
            expected_targets[prefix + "_root_manifest.sha256"]["sha256"],
        "deliverables/" + P0_TERMINAL_RECEIPT:
            expected_targets[prefix + "_terminal_checker_receipt.json"]["sha256"],
        "deliverables/" + P0_POSTCOMMIT_ADDENDUM: sha256(addendum_raw),
        "deliverables/" + P0_POSTCOMMIT_CHECKER: sha256(checker_raw),
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


def validate_p0_bytes(values: dict[str, bytes]) -> dict[str, str]:
    need(
        P0_SUPPLEMENTAL_ROOT_MANIFEST_SHA256 is not None
        and P0_SUPPLEMENTAL_OUTER_VERIFICATION_SHA256 is not None
        and P0_SUPPLEMENTAL_TERMINAL_RECEIPT_SHA256 is not None
        and P0_SUPPLEMENTAL_FINAL_COMMIT_SHA256 is not None
        and P0_SUPPLEMENTAL_FINAL_COMMIT_V2_SHA256 is not None,
        "P0_SUPPLEMENTAL_FINAL_PINS_UNSET",
    )
    payload = values["payload"]
    cold_raw = values["cold"]
    outer_raw = values["outer"]
    root_raw = values["root"]
    terminal_raw = values["terminal"]
    commit_raw = values["commit"]
    commit_v2_raw = values["commit_v2"]
    checker_raw = values["checker"]
    addendum_raw = values["addendum"]
    replay_raw = values["replay"]
    replay_manifest_raw = values["replay_manifest"]
    replay_receipt = closed_object(replay_raw, "P0 postcommit replay receipt")
    need(
        sha256(root_raw) == P0_SUPPLEMENTAL_ROOT_MANIFEST_SHA256
        and sha256(outer_raw) == P0_SUPPLEMENTAL_OUTER_VERIFICATION_SHA256
        and sha256(terminal_raw) == P0_SUPPLEMENTAL_TERMINAL_RECEIPT_SHA256
        and sha256(commit_raw) == P0_SUPPLEMENTAL_FINAL_COMMIT_SHA256
        and sha256(commit_v2_raw) == P0_SUPPLEMENTAL_FINAL_COMMIT_V2_SHA256,
        "external P0 authority pins",
    )
    root_rows = parse_manifest(root_raw, "P0 root")
    need(
        root_rows == {
            "deliverables/" + P0_PAYLOAD_MANIFEST: sha256(payload),
            "deliverables/" + P0_OUTER_VERIFICATION: sha256(outer_raw),
        },
        "P0 exact two-member root",
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
        "deliverables/" + P0_PREFIX + "_sealed",
        "deliverables/" + P0_PAYLOAD_MANIFEST,
        "deliverables/" + P0_COLD_RECEIPT,
        "deliverables/" + P0_OUTER_VERIFICATION,
        "deliverables/" + P0_ROOT_MANIFEST,
        "deliverables/" + P0_TERMINAL_RECEIPT,
    }
    conclusion = p0_conclusion()
    need(
        cold.get("schema")
        == "cm2.round306c30a.supplemental-audit-cold-receipt.v1"
        and cold.get("status")
        == "PASS_PAYLOAD_AND_AUTHORITATIVE_FULL_TRACE_COLD_REPLAY"
        and cold.get("payload_manifest_sha256") == sha256(payload)
        and cold.get("conclusion") == conclusion
        and outer.get("schema")
        == "cm2.round306c30a.supplemental-audit-outer-verification.v1"
        and outer.get("status")
        == "PASS_SUPPLEMENTAL_AUDIT_CLOSURE__ZERO_ADDITIONAL_CREDIT"
        and outer.get("payload_manifest_sha256") == sha256(payload)
        and outer.get("cold_replay_receipt_sha256") == sha256(cold_raw)
        and outer.get("conclusion") == conclusion
        and terminal.get("schema")
        == "cm2.round306c30a.supplemental-audit-terminal-receipt.v1"
        and terminal.get("status")
        == "PASS_TERMINAL_C30A_SUPPLEMENTAL_AUDIT_AUTHORIZATION__252_TO_92_ONLY"
        and terminal.get("root_manifest_sha256") == sha256(root_raw)
        and terminal.get("payload_manifest_sha256") == sha256(payload)
        and terminal.get("outer_verification_sha256") == sha256(outer_raw)
        and terminal.get("cold_replay_receipt_sha256") == sha256(cold_raw)
        and terminal.get("authority_condition")
        == "REQUIRES_POST_PUBLICATION_STAGE100_REPLAY_AND_FINAL_COMMIT"
        and terminal.get("conclusion") == conclusion,
        "P0 terminal 252-to-92-only closure",
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
        and terminal_replay.get("payload_manifest_sha256") == sha256(payload)
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
        and official_targets["deliverables/" + P0_PAYLOAD_MANIFEST].get("sha256")
        == sha256(payload)
        and official_targets["deliverables/" + P0_COLD_RECEIPT].get("sha256")
        == sha256(cold_raw)
        and official_targets["deliverables/" + P0_OUTER_VERIFICATION].get("sha256")
        == sha256(outer_raw)
        and official_targets["deliverables/" + P0_ROOT_MANIFEST].get("sha256")
        == sha256(root_raw)
        and official_targets["deliverables/" + P0_TERMINAL_RECEIPT].get("sha256")
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


def sha_manifest_by_basename(raw: bytes, label: str) -> dict[str, str]:
    rows = parse_manifest(raw, label)
    output: dict[str, str] = {}
    for path, digest in rows.items():
        name = Path(path).name
        need(name not in output, "duplicate manifest basename:" + label)
        output[name] = digest
    return output


def validate_command(raw: bytes, provenance: dict[str, Any], stage: str) -> None:
    command = strict_object(raw, stage + " command")
    need(
        command.get("schema") == "cm2.round306c30c.execution-command.v1"
        and command.get("stage") == stage
        and command.get("cwd") == os.fspath(WORKSPACE)
        and command.get("argv") == provenance.get("argv")
        and command.get("environment") == provenance.get("environment"),
        "retained command/provenance equality:" + stage,
    )


def validate_gnu_time(raw: bytes, label: str) -> None:
    """Bind evidence acceptance to an unsignalled zero-exit GNU time record."""
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


def load_pinned_trace_analyzer(raw: bytes) -> Any:
    need(sha256(raw) == TRACE_ANALYZER_SHA256, "pinned trace analyzer bytes")
    path = ROOT / TRACE_ANALYZER
    name = PREFIX + "_outer_pinned_cold_trace_analyzer"
    module = types.ModuleType(name)
    module.__file__ = os.fspath(path)
    module.__package__ = ""
    module.__loader__ = None
    module.__spec__ = importlib.machinery.ModuleSpec(
        name=name, loader=None, origin=os.fspath(path)
    )
    exec(compile(raw, os.fspath(path), "exec", dont_inherit=True), module.__dict__)
    need(callable(getattr(module, "analyze_trace", None)), "loaded trace analyzer")
    return module


def validate_provenance(
    raw: bytes, stage: str, source_sha256: str, seed: str | None,
) -> dict[str, Any]:
    value = strict_object(raw, stage + " provenance")
    need(
        value.get("schema") == "cm2.round306c30c.execution-provenance.v1"
        and value.get("stage") == stage
        and value.get("cwd") == os.fspath(WORKSPACE)
        and value.get("interpreter_sha256") == INTERPRETER_SHA256
        and value.get("source_sha256") == source_sha256
        and type(value.get("argv")) is list
        and all(type(item) is str for item in value["argv"]),
        "execution provenance:" + stage,
    )
    if stage == "producer":
        need(
            value.get("seed") == int(seed or "-1")
            and value.get("hash_sentinel") == "CM2_C30C_HASH_SEED_SENTINEL_v1"
            and value.get("hash_fingerprint") == HASH_FINGERPRINTS[seed or ""]
            and value.get("environment") == {
                "HOME": "/nonexistent", "LC_ALL": "C.UTF-8",
                "PYTHONHASHSEED": seed, "TZ": "UTC",
            }
            and value.get("interpreter_flags") == {
                "dont_write_bytecode": 1, "hash_randomization": 1,
                "ignore_environment": 0, "isolated": 0,
                "no_user_site": 1, "safe_path": True,
            }
            and "-P" in value["argv"] and "-s" in value["argv"]
            and "-B" in value["argv"] and "-I" not in value["argv"],
            "controlled seed provenance:" + str(seed),
        )
    else:
        need(
            value.get("seed") is None
            and value.get("interpreter_flags", {}).get("isolated") == 1
            and value.get("interpreter_flags", {}).get("dont_write_bytecode") == 1
            and "-I" in value["argv"] and "-B" in value["argv"],
            "isolated provenance:" + stage,
        )
    return value


def validate_bundle(
    capture: dict[str, Any], trace_analyzer: Any,
) -> dict[str, Any]:
    need(os.pread(capture["fd"], 10, 0) == bytes.fromhex("1f8b08000000000002ff"),
         "deterministic gzip header")
    bundle_sha256 = hash_capture(capture)
    os.lseek(capture["fd"], 0, os.SEEK_SET)
    retained: dict[str, bytes] = {}
    digests: dict[str, tuple[int, str]] = {}
    with os.fdopen(os.dup(capture["fd"]), "rb") as compressed:
        with gzip.GzipFile(fileobj=compressed, mode="rb") as uncompressed:
            with tarfile.open(fileobj=uncompressed, mode="r|", format=tarfile.USTAR_FORMAT) as archive:
                expected_names = ("bundle_manifest.json",) + BUNDLE_MEMBERS
                internal: dict[str, Any] | None = None
                for index, member in enumerate(archive):
                    need(index < len(expected_names) and member.name == expected_names[index],
                         "bundle exact member order")
                    need(
                        member.isfile() and not member.issym() and not member.islnk()
                        and member.mode == 0o600 and member.uid == 0 and member.gid == 0
                        and member.uname == "" and member.gname == "" and member.mtime == 0,
                        "normalized tar metadata:" + member.name,
                    )
                    source = archive.extractfile(member)
                    need(source is not None, "tar member stream:" + member.name)
                    state = hashlib.sha256()
                    size = 0
                    chunks: list[bytes] = []
                    for block in iter(lambda: source.read(1 << 20), b""):
                        state.update(block)
                        size += len(block)
                        limit = 256 << 20 if member.name == "cold/trace.raw" else 64 << 20
                        need(size <= limit, "retained bundle member size:" + member.name)
                        chunks.append(block)
                    need(size == member.size, "tar member byte count:" + member.name)
                    raw = b"".join(chunks)
                    if member.name == "bundle_manifest.json":
                        internal = strict_object(raw, "bundle internal manifest")
                    else:
                        digests[member.name] = (size, state.hexdigest())
                        retained[member.name] = raw
                need(len(digests) == len(BUNDLE_MEMBERS), "bundle exact member count")
    need(internal is not None, "bundle internal manifest retained")
    rows = internal.get("members")
    need(
        set(internal) == {
            "P0_supplemental_authority", "attack_harness_sha256",
            "attack_receipt_authority", "cold_trace_analyzer_sha256",
            "formal_credit", "independent_verifier_sha256", "member_count",
            "members", "producer_sha256", "receipt_adapter_independent_verifier_sha256",
            "receipt_adapter_sha256", "receipt_validator_sha256", "schema",
        }
        and internal.get("schema")
        == "cm2.round306c30c.audit-evidence-bundle-manifest.v1"
        and internal.get("formal_credit") == 0
        and internal.get("producer_sha256") == PRODUCER_SHA256
        and internal.get("independent_verifier_sha256") == VERIFIER_SHA256
        and internal.get("attack_harness_sha256") == HARNESS_SHA256
        and internal.get("cold_trace_analyzer_sha256") == TRACE_ANALYZER_SHA256
        and internal.get("receipt_validator_sha256") == RECEIPT_VALIDATOR_SHA256
        and internal.get("receipt_adapter_sha256") == RECEIPT_ADAPTER_SHA256
        and internal.get("receipt_adapter_independent_verifier_sha256")
        == RECEIPT_ADAPTER_VERIFIER_SHA256
        and internal.get("member_count") == len(BUNDLE_MEMBERS)
        and type(rows) is list and len(rows) == len(BUNDLE_MEMBERS),
        "bundle internal authority",
    )
    internal_map: dict[str, tuple[int, str]] = {}
    for row in rows:
        need(
            type(row) is dict and set(row) == {"path", "size", "sha256"}
            and type(row["path"]) is str and row["path"] not in internal_map
            and type(row["size"]) is int and type(row["sha256"]) is str,
            "bundle internal manifest row",
        )
        internal_map[row["path"]] = (row["size"], row["sha256"])
    need(tuple(sorted(internal_map)) == BUNDLE_MEMBERS and internal_map == digests,
         "bundle internal byte closure")

    receipt_authority = validate_attack_receipt_bridge(retained)
    need(
        internal.get("attack_receipt_authority") == receipt_authority,
        "bundle internal/external attack receipt authority identity",
    )

    p0 = validate_p0_bytes({
        "payload": retained["p0/payload_manifest.raw"],
        "cold": retained["p0/cold_replay_receipt.raw"],
        "outer": retained["p0/outer_verification.raw"],
        "root": retained["p0/root_manifest.raw"],
        "terminal": retained["p0/terminal_receipt.raw"],
        "commit": retained["p0/final_commit_receipt.raw"],
        "commit_v2": retained["p0/final_commit_v2_receipt.raw"],
        "checker": retained["p0/postcommit_checker.raw"],
        "addendum": retained["p0/postcommit_addendum.raw"],
        "replay": retained["p0/postcommit_replay_receipt.raw"],
        "replay_manifest": retained["p0/postcommit_replay_manifest.raw"],
    })
    need(internal.get("P0_supplemental_authority") == p0,
         "bundle P0 internal authority")

    code = sha_manifest_by_basename(retained["preflight/code.sha256.raw"], "code preflight")
    need(
        code == {
            PRODUCER: PRODUCER_SHA256,
            VERIFIER: VERIFIER_SHA256,
            HARNESS: HARNESS_SHA256,
            TRACE_ANALYZER: TRACE_ANALYZER_SHA256,
            RECEIPT_VALIDATOR: RECEIPT_VALIDATOR_SHA256,
            RECEIPT_ADAPTER: RECEIPT_ADAPTER_SHA256,
            RECEIPT_ADAPTER_VERIFIER: RECEIPT_ADAPTER_VERIFIER_SHA256,
            "python": INTERPRETER_SHA256,
        },
        "preflight executable pins",
    )
    candidate_rows = parse_manifest(
        retained["preflight/candidates.sha256.raw"], "candidate preflight"
    )
    need(len(candidate_rows) == len(SEEDS) * len(CANDIDATE_FILES),
         "dual candidate preflight row count")
    for seed in SEEDS:
        for name, spec in CANDIDATE_SPECS.items():
            matches = [digest for path, digest in candidate_rows.items()
                       if f"c30c-v4-seed-{seed}" in Path(path).parts
                       and Path(path).name == name]
            need(matches == [spec["sha256"]], "candidate preflight:" + seed + ":" + name)

    verifier_outputs: list[bytes] = []
    fingerprints: dict[str, int] = {}
    for seed in SEEDS:
        producer = f"producer/{seed}/"
        verifier = f"verifier/{seed}/"
        producer_provenance = validate_provenance(
            retained[producer + "provenance.json"], "producer", PRODUCER_SHA256, seed
        )
        validate_command(retained[producer + "command.json"], producer_provenance, "producer")
        validate_gnu_time(retained[producer + "time.raw"], "producer:" + seed)
        need(
            retained[producer + "exit.txt"] == b"0\n"
            and retained[producer + "stderr.raw"] == b""
            and sha256(retained[producer + "stdout.raw"]) == PRODUCER_STDOUT_SHA256,
            "controlled producer raw logs:" + seed,
        )
        fingerprints[seed] = producer_provenance["hash_fingerprint"]
        verifier_provenance = validate_provenance(
            retained[verifier + "provenance.json"], "verifier", VERIFIER_SHA256, None
        )
        validate_command(retained[verifier + "command.json"], verifier_provenance, "verifier")
        validate_gnu_time(retained[verifier + "time.raw"], "verifier:" + seed)
        output = strict_object(retained[verifier + "stdout.raw"], "verifier stdout:" + seed)
        need(
            retained[verifier + "exit.txt"] == b"0\n"
            and retained[verifier + "stderr.raw"] == b""
            and output.get("status") == VERIFIER_STATUS
            and output.get("candidate_result_sha256") == RESULT_OBJECT_SHA256
            and output.get("combined_Delta_H_cell_census") == 80
            and output.get("whole_origin_disposition_census") == {"RESOLVED_MIXED": 2}
            and output.get("formal_credit") == 0
            and output.get("manifest_authorized") is False,
            "independent verifier raw logs:" + seed,
        )
        verifier_outputs.append(retained[verifier + "stdout.raw"])
    need(verifier_outputs[0] == verifier_outputs[1], "dual verifier stdout identity")

    attack_provenance = validate_provenance(
        retained["attacks/provenance.json"], "attacks", HARNESS_SHA256, None
    )
    validate_command(retained["attacks/command.json"], attack_provenance, "attacks")
    validate_gnu_time(retained["attacks/time.raw"], "attacks")
    attacks = strict_object(retained["attacks/stdout.raw"], "attacks stdout")
    outcomes = attacks.get("attacks")
    need(
        retained["attacks/exit.txt"] == b"0\n"
        and retained["attacks/stderr.raw"] == b""
        and attacks.get("status") == HARNESS_STATUS
        and attacks.get("attack_count") == 62
        and type(outcomes) is list and len(outcomes) == 62
        and len({row.get("attack") for row in outcomes if type(row) is dict}) == 62
        and all(
            type(row) is dict
            and set(row) == {"attack", "layer", "expected_reason_prefix", "rejection"}
            and all(type(row[key]) is str and row[key] for key in row)
            for row in outcomes
        )
        and attacks.get("formal_credit") == 0
        and attacks.get("manifest_authorized") is False,
        "62 layer-specific coherent attacks",
    )

    cold_provenance = validate_provenance(
        retained["cold/provenance.json"], "cold", VERIFIER_SHA256, None
    )
    validate_command(retained["cold/command.json"], cold_provenance, "cold")
    validate_gnu_time(retained["cold/time.raw"], "cold")
    need(bool(cold_provenance["argv"]), "cold provenance argv")
    cold_candidate = Path(cold_provenance["argv"][-1])
    if not cold_candidate.is_absolute():
        cold_candidate = WORKSPACE / cold_candidate
    try:
        recomputed_trace = trace_analyzer.analyze_trace(
            retained["cold/trace.raw"], retained["cold/stdout.raw"],
            retained["cold/stderr.raw"], retained["cold/time.raw"], cold_candidate,
        )
    except (OSError, RuntimeError, TypeError, ValueError) as error:
        raise Blocked("independent cold trace recomputation") from error
    trace = strict_object(retained["cold/trace_audit.json"], "cold trace audit")
    trace_digest = digests["cold/trace.raw"][1]
    need(
        retained["cold/exit.txt"] == b"0\n"
        and retained["cold/stderr.raw"] == b""
        and retained["cold/stdout.raw"] == verifier_outputs[0]
        and trace == recomputed_trace
        and trace.get("status")
        == "PASS_C30C_COLD_TRACE_ZERO_PROTECTED_MUTATION"
        and trace.get("exit_status") == 0
        and trace.get("top_level_stdout_writes") == 1
        and trace.get("stderr_bytes") == 0
        and trace.get("protected_write_capable_opens") == 0
        and trace.get("protected_path_mutations") == 0
        and trace.get("protected_fd_writes") == 0
        and trace.get("historical_candidate_reads") == 0
        and trace.get("network_syscalls") == 0
        and trace.get("candidate_member_count") == 6
        and trace.get("trace_sha256") == trace_digest
        and retained["cold/sealed_pre.sha256.raw"]
        == retained["cold/sealed_post.sha256.raw"],
        "scrubbed cold verifier replay",
    )
    sealed_rows = sha_manifest_by_basename(
        retained["cold/sealed_pre.sha256.raw"], "cold sealed pre"
    )
    need(sealed_rows == {name: spec["sha256"] for name, spec in CANDIDATE_SPECS.items()},
         "cold sealed exact six")
    return {
        "bundle_sha256": bundle_sha256,
        "p0": p0,
        "fingerprints": fingerprints,
        "verifier_stdout_sha256": sha256(verifier_outputs[0]),
        "attacks_outcomes_sha256": sha256(canonical(outcomes)),
        "cold_trace": trace,
        "cold_trace_sha256": trace_digest,
        "receipt_authority": receipt_authority,
        "raw": retained,
    }


def exact_replay_tree(root: Path) -> None:
    status = root.lstat()
    need(stat.S_ISDIR(status.st_mode) and not root.is_symlink(), "payload replay directory")
    actual: set[str] = set()
    for path in root.rglob("*"):
        relative = path.relative_to(root).as_posix()
        child = path.lstat()
        need(not path.is_symlink(), "payload replay symlink:" + relative)
        if stat.S_ISDIR(child.st_mode):
            continue
        need(stat.S_ISREG(child.st_mode), "payload replay regular:" + relative)
        actual.add(relative)
    need(actual == set(PAYLOAD_REPLAY_FILES), "payload replay exact raw tree")


def validate_payload_replay(
    root: Path, payload_raw: bytes, payload_rows: dict[str, str],
    trace_analyzer: Any,
) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    exact_replay_tree(root)
    captures = {relative: open_capture(root / relative) for relative in PAYLOAD_REPLAY_FILES}
    try:
        small = {
            relative: read_capture(capture)
            for relative, capture in captures.items() if relative != "trace.raw"
        }
        trace_raw = read_capture(captures["trace.raw"], maximum=256 << 20)
        trace_sha256 = sha256(trace_raw)
        need(
            small["manifest_pre.raw"] == payload_raw
            and small["manifest_post.raw"] == payload_raw,
            "payload manifest raw pre/post identity",
        )
        output = strict_object(small["stdout.raw"], "payload replay stdout")
        need(
            small["exit.txt"] == b"0\n" and small["stderr.raw"] == b""
            and small["stdout.raw"] == canonical(output) + b"\n"
            and output.get("schema")
            == "cm2.round306c30c.manifest-first-sealed-replay.v1"
            and output.get("phase") == "payload"
            and output.get("status") == PAYLOAD_REPLAY_STATUS
            and output.get("payload_manifest_sha256") == sha256(payload_raw)
            and output.get("root_manifest_sha256") is None
            and output.get("candidate_result_sha256") == RESULT_OBJECT_SHA256
            and output.get("candidate_result_formal_credit") == 0
            and output.get("formal_credit") == 0
            and output.get("source_W_transition_authorized") is False,
            "payload manifest-first zero-credit receipt",
        )
        provenance = strict_object(small["provenance.json"], "payload replay provenance")
        need(
            provenance.get("schema")
            == "cm2.round306c30c.payload-manifest-first-provenance.v1"
            and provenance.get("stage") == "payload_manifest_first"
            and provenance.get("cwd") == os.fspath(WORKSPACE)
            and provenance.get("interpreter_sha256") == INTERPRETER_SHA256
            and provenance.get("source_sha256") == payload_rows[SEALED_VERIFIER]
            and provenance.get("environment") == {
                "HOME": "/nonexistent", "LC_ALL": "C.UTF-8",
                "PATH": "/usr/bin:/bin", "PYTHONDONTWRITEBYTECODE": "1",
                "TZ": "UTC",
            }
            and provenance.get("interpreter_flags") == {
                "dont_write_bytecode": 1, "isolated": 1,
                "no_user_site": 1, "safe_path": True,
            }
            and type(provenance.get("argv")) is list
            and "-I" in provenance["argv"] and "-B" in provenance["argv"]
            and provenance["argv"][-2:] == ["--phase", "payload"],
            "payload manifest-first provenance",
        )
        validate_gnu_time(small["time.raw"], "payload manifest-first")
        try:
            recomputed_trace = trace_analyzer.analyze_trace(
                trace_raw, small["stdout.raw"], small["stderr.raw"],
                small["time.raw"], ROOT / SEALED_DIR,
            )
        except (OSError, RuntimeError, TypeError, ValueError) as error:
            raise Blocked("independent payload trace recomputation") from error
        trace = strict_object(small["trace_audit.json"], "payload replay trace audit")
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
            and trace.get("network_syscalls") == 0
            and trace.get("candidate_member_count") == 6
            and trace.get("trace_sha256") == trace_sha256,
            "payload manifest-first trace audit",
        )
        need(small["sealed_pre.sha256.raw"] == small["sealed_post.sha256.raw"],
             "payload sealed raw pre/post identity")
        sealed = sha_manifest_by_basename(small["sealed_pre.sha256.raw"], "payload sealed")
        need(sealed == {name: spec["sha256"] for name, spec in CANDIDATE_SPECS.items()},
             "payload replay exact six seal")
        for capture in captures.values():
            require_current(capture)
        exact_replay_tree(root)
        return {
            "output": output,
            "trace": trace,
            "trace_sha256": trace_sha256,
            "stdout_sha256": sha256(small["stdout.raw"]),
        }, captures
    except BaseException:
        for capture in captures.values():
            os.close(capture["fd"])
        raise


def validate_payload_manifest(
    manifest_path: Path,
) -> tuple[dict[str, Any], dict[str, dict[str, Any]], bytes, dict[str, str]]:
    manifest_capture = open_capture(manifest_path)
    members: dict[str, dict[str, Any]] = {}
    try:
        raw = read_capture(manifest_capture)
        rows = parse_manifest(raw, "C30c payload")
        need(tuple(sorted(rows)) == PAYLOAD_MEMBERS, "C30c payload exact member map")
        for relative, expected in sorted(rows.items()):
            path = ROOT / relative
            need(path.resolve(strict=True).is_relative_to(ROOT.resolve(strict=True)),
                 "payload member containment:" + relative)
            capture = open_capture(path)
            members[relative] = capture
            need(hash_capture(capture) == expected, "payload member hash:" + relative)
        sealed = ROOT / SEALED_DIR
        status = sealed.lstat()
        need(stat.S_ISDIR(status.st_mode) and not sealed.is_symlink(), "sealed directory")
        need({item.name for item in sealed.iterdir()} == set(CANDIDATE_FILES),
             "sealed exact six")
        for name, spec in CANDIDATE_SPECS.items():
            relative = SEALED_DIR + "/" + name
            need(
                members[relative]["identity"][4] == spec["size"]
                and rows[relative] == spec["sha256"],
                "sealed fixed candidate:" + name,
            )
        return manifest_capture, members, raw, rows
    except BaseException:
        os.close(manifest_capture["fd"])
        for capture in members.values():
            os.close(capture["fd"])
        raise


def build_verification(
    evidence_bundle: Path, payload_manifest: Path, replay_dir: Path,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    need(
        P0_SUPPLEMENTAL_ROOT_MANIFEST_SHA256 is not None
        and P0_SUPPLEMENTAL_OUTER_VERIFICATION_SHA256 is not None
        and P0_SUPPLEMENTAL_TERMINAL_RECEIPT_SHA256 is not None
        and P0_SUPPLEMENTAL_FINAL_COMMIT_SHA256 is not None
        and P0_SUPPLEMENTAL_FINAL_COMMIT_V2_SHA256 is not None,
        "P0_SUPPLEMENTAL_FINAL_PINS_UNSET",
    )
    need(payload_manifest.resolve(strict=True) == (ROOT / PAYLOAD_MANIFEST).resolve(strict=True),
         "fixed payload manifest path")
    need(evidence_bundle.resolve(strict=True) == (ROOT / EVIDENCE_BUNDLE).resolve(strict=True),
         "fixed evidence bundle path")
    manifest_capture, members, payload_raw, payload_rows = validate_payload_manifest(
        payload_manifest
    )
    replay_captures: dict[str, dict[str, Any]] = {}
    all_captures = [manifest_capture, *members.values()]
    try:
        trace_analyzer = load_pinned_trace_analyzer(
            read_capture(members[TRACE_ANALYZER], maximum=4 << 20)
        )
        bundle = validate_bundle(members[EVIDENCE_BUNDLE], trace_analyzer)
        actual_p0 = validate_p0_bytes({
            "payload": read_capture(members[P0_PAYLOAD_MANIFEST]),
            "cold": read_capture(members[P0_COLD_RECEIPT]),
            "outer": read_capture(members[P0_OUTER_VERIFICATION]),
            "root": read_capture(members[P0_ROOT_MANIFEST]),
            "terminal": read_capture(members[P0_TERMINAL_RECEIPT]),
            "commit": read_capture(members[P0_FINAL_COMMIT]),
            "commit_v2": read_capture(members[P0_FINAL_COMMIT_V2]),
            "checker": read_capture(members[P0_POSTCOMMIT_CHECKER]),
            "addendum": read_capture(members[P0_POSTCOMMIT_ADDENDUM]),
            "replay": read_capture(members[P0_POSTCOMMIT_REPLAY_RECEIPT]),
            "replay_manifest": read_capture(members[P0_POSTCOMMIT_REPLAY_MANIFEST]),
        })
        need(bundle["p0"] == actual_p0, "bundle/manifest P0 byte authority equality")
        replay, replay_captures = validate_payload_replay(
            replay_dir, payload_raw, payload_rows, trace_analyzer
        )
        all_captures.extend(replay_captures.values())
        need(
            replay["output"].get("sealed_verifier_stdout_sha256")
            == bundle["verifier_stdout_sha256"],
            "payload replay/phase-one verifier stdout identity",
        )
        candidate_files = {
            name: {"size": spec["size"], "sha256": spec["sha256"]}
            for name, spec in CANDIDATE_SPECS.items()
        }
        cold_trace = bundle["cold_trace"]
        body: dict[str, Any] = {
            "schema": "cm2.round306c30c.source-w-full-delta.formal-handoff-verification.v1",
            "status": FORMAL_STATUS,
            "authorization": {
                "layer": "OUTER_MANIFEST_PINNED_VERIFICATION",
                "candidate_result_is_evidence_only": True,
                "candidate_result_object_sha256": RESULT_OBJECT_SHA256,
                "candidate_result_formal_credit": {
                    "combined_Delta_H_cell_dispositions": 0,
                    "resolved_source_W_origin_dispositions": 0,
                    "resolved_nonexcluded": 0,
                    "whole_source_W_origin_exclusions": 0,
                },
                "C30b_formal_baseline": {
                    "manifest_sha256": "6af636a4239f390712d057030f03e09fbbca332c6170f183d3d0095f19f0f248",
                    "verification_sha256": "e9e72536be9ba707fe2fdf6034b47978be4d09235e5133414ec7b0a31acf4e71",
                    "result_file_sha256": "b015e5bd6a4ee01d71ac95765d07dcbc63c3888f0c8ff9205e2d8c688958c11b",
                    "result_object_sha256": "7abf8da628eb35b20ed27b032dc55ea29e9944530d2d5a6a64993a995f1ad85e",
                    "formal_source_W_remaining": 80,
                },
                "C30a_P0_supplemental_closure": {
                    "required_before_C30c_authorization": True,
                    **actual_p0,
                    "formal_source_W_transition": "252->92",
                },
            },
            "executables": {
                "producer_sha256": PRODUCER_SHA256,
                "independent_verifier_sha256": VERIFIER_SHA256,
                "attack_harness_sha256": HARNESS_SHA256,
                "cold_trace_analyzer_sha256": TRACE_ANALYZER_SHA256,
            },
            "runtime": {
                "python_version": "3.12.3", "python_flint": "0.9.0",
                "flint_version": "3.6.0",
                "requirements_lock_sha256": "cd171f53dd8a187b2ef4bd7ad0cc2adbe2082395646c0c57407f4e3514c11f5c",
                "runtime_lock_sha256": "ffe714b67a0aa05d8094033a0d9cc8e10ccafa03157951adf3d64055c98cdc79",
                "wheel_sha256": "376b88cacd30612479e839ffdba887599d3f9c8c0e214852bf80bb2b194e4d76",
                "runtime_attestation_sha256": CANDIDATE_SPECS[
                    "cm2_round306c30b_python_flint_runtime_attestation.json"
                ]["sha256"],
            },
            "controlled_seed_replay": {
                "producer_runtime_contract": (
                    "ENV_I_EXACT_4_VARIABLES__PYTHONHASHSEED_IN_"
                    "{30630071,30630929}__PYTHON_-P_-s_-B"
                ),
                "seeds": [30630071, 30630929],
                "hash_fingerprints": bundle["fingerprints"],
                "candidate_file_count": 6,
                "candidate_files": candidate_files,
                "byte_identical_files": 6,
                "canonical_stdout_sha256": PRODUCER_STDOUT_SHA256,
                "both_exit_zero": True,
                "program_stderr_empty": True,
            },
            "independent_reconstruction": {
                "verified_candidate_count": 2, "both_exit_zero": True,
                "stdout_byte_identical": True, "program_stderr_empty": True,
                "status": VERIFIER_STATUS,
                "combined_Delta_H_cell_census": 80,
                "inherited_H_cell_census": 88,
                "boundary_atomic_join_row_census": 2080,
                "whole_origin_census": 2,
                "whole_origin_disposition_census": {"RESOLVED_MIXED": 2},
                "candidate_result_object_sha256": RESULT_OBJECT_SHA256,
                "formal_credit": 0,
            },
            "coherent_attacks": {
                "attack_count": 62, "rejected_count": 62,
                "all_layer_specific_reasons_matched": True,
                "candidate_baseline_immutable": True,
                "outcomes_sha256": bundle["attacks_outcomes_sha256"],
            },
            "attack_receipt_authority": bundle["receipt_authority"],
            "scrubbed_cold_replay": {
                "runtime_contract": "SCRUBBED_ENV__PINNED_PYTHON_-I_-B",
                "exit_status": 0, "stdout_canonical_single_json": True,
                "stdout_matches_phase_one": True,
                "top_level_stdout_writes": cold_trace["top_level_stdout_writes"],
                "stderr_bytes": cold_trace["stderr_bytes"],
                "protected_write_capable_opens": cold_trace["protected_write_capable_opens"],
                "protected_path_mutations": cold_trace["protected_path_mutations"],
                "protected_fd_writes": cold_trace["protected_fd_writes"],
                "historical_candidate_reads": cold_trace["historical_candidate_reads"],
                "network_syscalls": cold_trace["network_syscalls"],
                "trace_sha256": bundle["cold_trace_sha256"],
                "trace_retained": True,
            },
            "sealed_publication": {
                "sealed_directory": "deliverables/" + SEALED_DIR,
                "sealed_member_count": 6, "sealed_files": candidate_files,
                "byte_identical_to_both_controlled_candidates": True,
                "manifest_sha256": sha256(payload_raw),
                "manifest_exact_member_count": len(PAYLOAD_MEMBERS),
                "manifest_exact_member_map_sha256": sha256(canonical(payload_rows)),
                "manifest_precheck_passed_before_verifier": True,
                "manifest_postcheck_passed": True,
                "sealed_directory_unchanged_during_final_replay": True,
            },
            "formal_handoff": {
                "candidate_result_formal_credit_remains_zero": True,
                "authorized_by_outer_verification_and_manifest": True,
                "before": {
                    "excluded": 74746, "conservative_live": 2086,
                    "remaining": 80, "resolved_nonexcluded": 2006,
                    "total": 76832,
                    "remaining_partition": {
                        "full_Delta": 2, "multi_Delta": 20, "reduced_live": 2,
                        "retained_source_seams": 2, "compact_q": 54,
                    },
                },
                "credits": {
                    "combined_Delta_H_cell_dispositions": 80,
                    "resolved_origin_dispositions": 2,
                    "resolved_nonexcluded": 2, "whole_origin_exclusions": 0,
                },
                "after": {
                    "excluded": 74746, "conservative_live": 2086,
                    "remaining": 78, "resolved_nonexcluded": 2008,
                    "total": 76832,
                    "remaining_partition": {
                        "multi_Delta": 20, "reduced_live": 2,
                        "retained_source_seams": 2, "compact_q": 54,
                    },
                },
                "conservation_identity": "74746+2086=76832",
            },
            "strict_nonpromotion": {
                "D02": "BLOCKED_BY_78_REMAINING_SOURCE_W_ORIGINS_AND_COMPOSITE_GATE",
                "D03": "UNAUTHORIZED", "D04": "NOT_MINTED",
                "Gate5_filled_field_slots": "10/18",
                "Gate5_complete_global_blocks": 0,
                "CM2": "NO-GO_FOR_CLAIM",
            },
            "verification_hash_convention": (
                "SHA256_CANONICAL_JSON_EXCLUDING_verification_object_sha256"
            ),
        }
        verification = {
            **body, "verification_object_sha256": sha256(canonical(body))
        }
        for capture in all_captures:
            require_current(capture)
        return verification, all_captures
    except BaseException:
        for capture in all_captures:
            try:
                os.close(capture["fd"])
            except OSError:
                pass
        raise


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
            raise Blocked("outer verification target already exists")
        raise OSError(error, os.strerror(error), os.fspath(target))


def publish(
    evidence_bundle: Path, payload_manifest: Path, replay_dir: Path, output: Path,
) -> dict[str, Any]:
    need(
        P0_SUPPLEMENTAL_ROOT_MANIFEST_SHA256 is not None
        and P0_SUPPLEMENTAL_OUTER_VERIFICATION_SHA256 is not None
        and P0_SUPPLEMENTAL_TERMINAL_RECEIPT_SHA256 is not None
        and P0_SUPPLEMENTAL_FINAL_COMMIT_SHA256 is not None
        and P0_SUPPLEMENTAL_FINAL_COMMIT_V2_SHA256 is not None,
        "P0_SUPPLEMENTAL_FINAL_PINS_UNSET",
    )
    output = Path(os.path.abspath(os.fspath(output)))
    need(output == ROOT / OUTER_VERIFICATION, "fixed outer verification output")
    try:
        output.lstat()
    except FileNotFoundError:
        pass
    else:
        raise Blocked("outer verification target already exists")
    verification, captures = build_verification(
        evidence_bundle, payload_manifest, replay_dir
    )
    staging: Path | None = None
    try:
        raw = canonical(verification)
        descriptor, staging_name = tempfile.mkstemp(
            prefix="." + output.name + ".staging-", dir=output.parent
        )
        staging = Path(staging_name)
        try:
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(raw)
                stream.flush()
                os.fsync(stream.fileno())
            os.chmod(staging, 0o600)
            need(staging.read_bytes() == raw, "outer verification staging bytes")
            for capture in captures:
                require_current(capture)
            rename_noreplace(staging, output)
            staging = None
            fsync_directory(output.parent)
        finally:
            if staging is not None and staging.exists() and not staging.is_symlink():
                staging.unlink()
        return {
            "schema": "cm2.round306c30c.formal-handoff-outer-build.v1",
            "status": "OUTER_VERIFICATION_MINTED__AWAITING_ROOT_MANIFEST__ZERO_FORMAL_CREDIT",
            "verification_file_sha256": sha256(raw),
            "verification_object_sha256": verification["verification_object_sha256"],
            "formal_credit": 0,
            "source_W_transition_authorized": False,
        }
    finally:
        for capture in captures:
            try:
                os.close(capture["fd"])
            except OSError:
                pass


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-bundle", required=True, type=Path)
    parser.add_argument("--payload-manifest", required=True, type=Path)
    parser.add_argument("--payload-replay-dir", required=True, type=Path)
    parser.add_argument("--output-verification", required=True, type=Path)
    arguments = parser.parse_args()
    try:
        output = publish(
            arguments.evidence_bundle, arguments.payload_manifest,
            arguments.payload_replay_dir, arguments.output_verification,
        )
    except (Blocked, OSError, ValueError, KeyError, TypeError, tarfile.TarError) as error:
        print(canonical({
            "schema": "cm2.round306c30c.formal-handoff-outer-build.v1",
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
