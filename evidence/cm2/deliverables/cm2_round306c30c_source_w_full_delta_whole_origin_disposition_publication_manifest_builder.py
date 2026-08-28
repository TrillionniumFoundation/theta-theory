#!/usr/bin/env python3
"""Build the two non-self-referential C30c publication manifests.

The payload manifest pins every static input, executable, raw-evidence bundle,
document, P0 supplemental authority, and the exact six-file seal.  After a
manifest-first payload replay, the outer verification pins that replay.  The
root manifest then pins exactly the payload manifest and outer verification.
Neither build phase grants formal credit; only the root manifest-first sealed
verifier may emit the terminal authorization receipt.
"""
from __future__ import annotations

import argparse
import ctypes
import errno
import hashlib
import json
import os
import stat
import sys
import tempfile
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
ROOT_MANIFEST = PREFIX + "_manifest.sha256"
OUTER_VERIFICATION = PREFIX + "_verification.json"
SEALED_DIR = "cm2_round306c30c_sealed"
RECEIPT_VALIDATOR = "cm2_round306c30c_62_attack_run_receipt_validator.py"
RECEIPT_ADAPTER = "cm2_round306c30c_attack_receipt_evidence_adapter.py"
RECEIPT_ADAPTER_VERIFIER = (
    "cm2_round306c30c_attack_receipt_evidence_adapter_independent_verifier.py"
)

CANDIDATE_FILES = (
    "cm2_round306c30b_python_flint_runtime_attestation.json",
    PREFIX + "_combined_boundary_atomic_owner_join_ledger.jsonl.gz",
    PREFIX + "_delta_h_cell_ledger.jsonl.gz",
    PREFIX + "_inherited_h_cell_ledger.jsonl.gz",
    PREFIX + "_result.json",
    PREFIX + "_whole_origin_ledger.jsonl.gz",
)

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
    PREFIX + "_producer.py",
    PREFIX + "_independent_verifier.py",
    PREFIX + "_attack_harness.py",
    PREFIX + "_cold_trace_analyzer.py",
    PREFIX + "_formal_handoff_verification.schema.json",
    PREFIX + "_audit_evidence_bundle_builder.py",
    PREFIX + "_formal_handoff_outer_verifier.py",
    PREFIX + "_publication_manifest_builder.py",
    PREFIX + "_manifest_first_sealed_verifier.py",
    RECEIPT_VALIDATOR,
    RECEIPT_ADAPTER,
    RECEIPT_ADAPTER_VERIFIER,
    PREFIX + "_audit_evidence.tar.gz",
    PREFIX + "_cold_replay.md",
    PREFIX + "_report.md",
    *(SEALED_DIR + "/" + filename for filename in CANDIDATE_FILES),
)))
ROOT_MEMBERS = tuple(sorted((PAYLOAD_MANIFEST, OUTER_VERIFICATION)))


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


def file_bytes(path: Path) -> bytes:
    descriptor = os.open(
        path, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        before = os.fstat(descriptor)
        need(
            stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
            "manifest member regular singleton:" + path.name,
        )
        chunks: list[bytes] = []
        while block := os.read(descriptor, 1 << 20):
            chunks.append(block)
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
        ),
        "manifest member changed during hash:" + path.name,
    )
    raw = b"".join(chunks)
    need(len(raw) == before.st_size, "manifest member byte count:" + path.name)
    return raw


def file_hash(path: Path) -> str:
    return hashlib.sha256(file_bytes(path)).hexdigest()


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


def strict_closed_object(raw: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(raw)
    except (UnicodeDecodeError, ValueError, json.JSONDecodeError) as error:
        raise Blocked("strict JSON:" + label) from error
    need(type(value) is dict and raw in {canonical(value), canonical(value) + b"\n"},
         "canonical JSON:" + label)
    body = dict(value)
    object_hash = body.pop("payload_sha256", None)
    need(object_hash == hashlib.sha256(canonical(body)).hexdigest(),
         "closed JSON:" + label)
    return value


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
        and value.get("checker_sha256")
        == hashlib.sha256(checker_raw).hexdigest()
        == "82d126f5f83528729fff9c56827575963819b4be92286e1d9558cf74a82e2828"
        and value.get("addendum_sha256")
        == hashlib.sha256(addendum_raw).hexdigest()
        == "66c3b4f3113b4038d77c8b93e7e1c783937089e3e09f8f54434d409c780c2464"
        and value.get("postcommit_replay_receipt_sha256")
        == hashlib.sha256(replay_raw).hexdigest()
        == "8c15d45770b29057f3d204055b3383e647cc91859bef0d763a2c85ca5fa4f2a8"
        and value.get("postcommit_manifest_sha256")
        == hashlib.sha256(replay_manifest_raw).hexdigest()
        == "63c2260d47e89d7710d4c18a1c4a94255484e4769c069eec6362e4a81a535085"
        and value.get("postcommit_manifest_member_count") == 32
        and value.get("original_final_commit_sha256")
        == hashlib.sha256(commit_raw).hexdigest()
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
        and hashlib.sha256(canonical(stages)).hexdigest()
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
        and replay_receipt.get("original_final_commit_sha256")
        == hashlib.sha256(commit_raw).hexdigest()
        and replay_receipt.get("official_targets") == expected_targets
        and replay_receipt.get("checker_sha256")
        == hashlib.sha256(checker_raw).hexdigest()
        and replay_receipt.get("addendum_sha256")
        == hashlib.sha256(addendum_raw).hexdigest()
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
        "deliverables/" + P0_FINAL_COMMIT:
            hashlib.sha256(commit_raw).hexdigest(),
        "deliverables/" + P0_OUTER_VERIFICATION:
            expected_targets[prefix + "_outer_verification.json"]["sha256"],
        "deliverables/" + P0_PAYLOAD_MANIFEST:
            expected_targets[prefix + "_payload_manifest.sha256"]["sha256"],
        "deliverables/" + P0_POSTCOMMIT_REPLAY_RECEIPT:
            hashlib.sha256(replay_raw).hexdigest(),
        "deliverables/" + P0_ROOT_MANIFEST:
            expected_targets[prefix + "_root_manifest.sha256"]["sha256"],
        "deliverables/" + P0_TERMINAL_RECEIPT:
            expected_targets[prefix + "_terminal_checker_receipt.json"]["sha256"],
        "deliverables/" + P0_POSTCOMMIT_ADDENDUM:
            hashlib.sha256(addendum_raw).hexdigest(),
        "deliverables/" + P0_POSTCOMMIT_CHECKER:
            hashlib.sha256(checker_raw).hexdigest(),
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


def validate_p0_pins() -> None:
    need(
        P0_SUPPLEMENTAL_ROOT_MANIFEST_SHA256 is not None
        and P0_SUPPLEMENTAL_OUTER_VERIFICATION_SHA256 is not None
        and P0_SUPPLEMENTAL_TERMINAL_RECEIPT_SHA256 is not None
        and P0_SUPPLEMENTAL_FINAL_COMMIT_SHA256 is not None
        and P0_SUPPLEMENTAL_FINAL_COMMIT_V2_SHA256 is not None,
        "P0_SUPPLEMENTAL_FINAL_PINS_UNSET",
    )
    payload_raw = file_bytes(ROOT / P0_PAYLOAD_MANIFEST)
    cold_raw = file_bytes(ROOT / P0_COLD_RECEIPT)
    outer_raw = file_bytes(ROOT / P0_OUTER_VERIFICATION)
    root_raw = file_bytes(ROOT / P0_ROOT_MANIFEST)
    terminal_raw = file_bytes(ROOT / P0_TERMINAL_RECEIPT)
    commit_raw = file_bytes(ROOT / P0_FINAL_COMMIT)
    commit_v2_raw = file_bytes(ROOT / P0_FINAL_COMMIT_V2)
    checker_raw = file_bytes(ROOT / P0_POSTCOMMIT_CHECKER)
    addendum_raw = file_bytes(ROOT / P0_POSTCOMMIT_ADDENDUM)
    replay_raw = file_bytes(ROOT / P0_POSTCOMMIT_REPLAY_RECEIPT)
    replay_manifest_raw = file_bytes(ROOT / P0_POSTCOMMIT_REPLAY_MANIFEST)
    replay_receipt = strict_closed_object(
        replay_raw, "P0 postcommit replay receipt"
    )
    need(
        hashlib.sha256(root_raw).hexdigest()
        == P0_SUPPLEMENTAL_ROOT_MANIFEST_SHA256
        and hashlib.sha256(outer_raw).hexdigest()
        == P0_SUPPLEMENTAL_OUTER_VERIFICATION_SHA256
        and hashlib.sha256(terminal_raw).hexdigest()
        == P0_SUPPLEMENTAL_TERMINAL_RECEIPT_SHA256
        and hashlib.sha256(commit_raw).hexdigest()
        == P0_SUPPLEMENTAL_FINAL_COMMIT_SHA256
        and hashlib.sha256(commit_v2_raw).hexdigest()
        == P0_SUPPLEMENTAL_FINAL_COMMIT_V2_SHA256,
        "externally pinned P0 supplemental authority",
    )
    root_rows = parse_manifest(root_raw, "P0 root")
    need(
        root_rows == {
            "deliverables/" + P0_PAYLOAD_MANIFEST:
                hashlib.sha256(payload_raw).hexdigest(),
            "deliverables/" + P0_OUTER_VERIFICATION:
                hashlib.sha256(outer_raw).hexdigest(),
        },
        "P0 exact two-member root",
    )
    cold = strict_closed_object(cold_raw, "P0 cold receipt")
    outer = strict_closed_object(outer_raw, "P0 outer verification")
    terminal = strict_closed_object(terminal_raw, "P0 terminal receipt")
    commit = strict_closed_object(commit_raw, "P0 final commit")
    commit_v2 = strict_closed_object(commit_v2_raw, "P0 final commit v2")
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
        cold.get("status") == "PASS_PAYLOAD_AND_AUTHORITATIVE_FULL_TRACE_COLD_REPLAY"
        and cold.get("payload_manifest_sha256")
        == hashlib.sha256(payload_raw).hexdigest()
        and cold.get("conclusion") == conclusion
        and outer.get("status")
        == "PASS_SUPPLEMENTAL_AUDIT_CLOSURE__ZERO_ADDITIONAL_CREDIT"
        and outer.get("payload_manifest_sha256")
        == hashlib.sha256(payload_raw).hexdigest()
        and outer.get("cold_replay_receipt_sha256")
        == hashlib.sha256(cold_raw).hexdigest()
        and outer.get("conclusion") == conclusion
        and terminal.get("status")
        == "PASS_TERMINAL_C30A_SUPPLEMENTAL_AUDIT_AUTHORIZATION__252_TO_92_ONLY"
        and terminal.get("root_manifest_sha256")
        == hashlib.sha256(root_raw).hexdigest()
        and terminal.get("payload_manifest_sha256")
        == hashlib.sha256(payload_raw).hexdigest()
        and terminal.get("outer_verification_sha256")
        == hashlib.sha256(outer_raw).hexdigest()
        and terminal.get("cold_replay_receipt_sha256")
        == hashlib.sha256(cold_raw).hexdigest()
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
        and terminal_replay.get("payload_manifest_sha256")
        == hashlib.sha256(payload_raw).hexdigest()
        and terminal_replay.get("cold_replay_receipt_sha256")
        == hashlib.sha256(cold_raw).hexdigest()
        and terminal_replay.get("outer_verification_sha256")
        == hashlib.sha256(outer_raw).hexdigest()
        and terminal_replay.get("root_manifest_sha256")
        == hashlib.sha256(root_raw).hexdigest()
        and terminal_replay.get("terminal_receipt_sha256")
        == hashlib.sha256(terminal_raw).hexdigest()
        and terminal_replay.get("conclusion") == conclusion
        and commit.get("pipeline_precommit_receipt_sha256")
        == hashlib.sha256(canonical(precommit) + b"\n").hexdigest()
        and official_targets == precommit.get("official_targets")
        and type(official_targets) is dict
        and set(official_targets) == expected_target_names
        and official_targets["deliverables/" + P0_PAYLOAD_MANIFEST].get("sha256")
        == hashlib.sha256(payload_raw).hexdigest()
        and official_targets["deliverables/" + P0_COLD_RECEIPT].get("sha256")
        == hashlib.sha256(cold_raw).hexdigest()
        and official_targets["deliverables/" + P0_OUTER_VERIFICATION].get("sha256")
        == hashlib.sha256(outer_raw).hexdigest()
        and official_targets["deliverables/" + P0_ROOT_MANIFEST].get("sha256")
        == hashlib.sha256(root_raw).hexdigest()
        and official_targets["deliverables/" + P0_TERMINAL_RECEIPT].get("sha256")
        == hashlib.sha256(terminal_raw).hexdigest()
        and commit.get("stage100_exit_sha256")
        == precommit.get("stage100_artifacts", {}).get("exit", {}).get("sha256"),
        "P0 post-stage100 final commit closure",
    )
    validate_p0_commit_v2(
        commit_v2, commit_raw, official_targets, conclusion,
        checker_raw, addendum_raw, replay_raw, replay_manifest_raw, replay_receipt,
    )


def validate_sealed_exact_six() -> None:
    sealed = ROOT / SEALED_DIR
    status = sealed.lstat()
    need(stat.S_ISDIR(status.st_mode) and not sealed.is_symlink(), "C30c sealed directory")
    need(
        {member.name for member in sealed.iterdir()} == set(CANDIDATE_FILES),
        "C30c sealed exact six",
    )


def strict_outer_verification() -> None:
    raw = file_bytes(ROOT / OUTER_VERIFICATION)
    try:
        value = json.loads(raw)
    except (UnicodeDecodeError, ValueError, json.JSONDecodeError) as error:
        raise Blocked("outer verification JSON") from error
    body = dict(value) if type(value) is dict else {}
    verification_object_sha256 = body.pop("verification_object_sha256", None)
    p0 = value.get("authorization", {}).get(
        "C30a_P0_supplemental_closure", {}
    ) if type(value) is dict else {}
    p0_terminal = strict_closed_object(
        file_bytes(ROOT / P0_TERMINAL_RECEIPT), "P0 terminal receipt"
    )
    need(
        type(value) is dict and raw == canonical(value)
        and verification_object_sha256 == hashlib.sha256(canonical(body)).hexdigest()
        and value.get("schema")
        == "cm2.round306c30c.source-w-full-delta.formal-handoff-verification.v1"
        and value.get("status")
        == ("PASS_FORMAL_C30C__80_DELTA_H_CELLS__2_RESOLVED_MIXED__"
            "SOURCE_W_80_TO_78__D02_STILL_BLOCKED")
        and value.get("formal_handoff", {}).get(
            "candidate_result_formal_credit_remains_zero"
        ) is True
        and value.get("formal_handoff", {}).get(
            "authorized_by_outer_verification_and_manifest"
        ) is True,
        "outer formal verification contract",
    )
    need(
        p0.get("root_manifest_sha256")
        == P0_SUPPLEMENTAL_ROOT_MANIFEST_SHA256
        and p0.get("outer_verification_sha256")
        == P0_SUPPLEMENTAL_OUTER_VERIFICATION_SHA256
        and p0.get("terminal_receipt_file_sha256")
        == P0_SUPPLEMENTAL_TERMINAL_RECEIPT_SHA256
        and p0.get("final_commit_receipt_sha256")
        == P0_SUPPLEMENTAL_FINAL_COMMIT_SHA256
        and p0.get("final_commit_v2_receipt_sha256")
        == P0_SUPPLEMENTAL_FINAL_COMMIT_V2_SHA256
        and p0.get("terminal_receipt_object_sha256")
        == p0_terminal.get("payload_sha256")
        and p0.get("formal_source_W_transition") == "252->92"
        and value.get("sealed_publication", {}).get("manifest_sha256")
        == file_hash(ROOT / PAYLOAD_MANIFEST)
        and value.get("formal_handoff", {}).get("after", {}).get("remaining") == 78
        and value.get("strict_nonpromotion", {}).get("D02")
        == "BLOCKED_BY_78_REMAINING_SOURCE_W_ORIGINS_AND_COMPOSITE_GATE",
        "outer formal verification contract",
    )


def manifest_bytes(members: tuple[str, ...]) -> bytes:
    rows: list[bytes] = []
    for relative in members:
        need(
            relative and not Path(relative).is_absolute()
            and ".." not in Path(relative).parts,
            "manifest relative path",
        )
        path = ROOT / relative
        need(path.resolve(strict=True).is_relative_to(ROOT.resolve(strict=True)),
             "manifest containment:" + relative)
        rows.append((file_hash(path) + "  " + relative + "\n").encode("ascii"))
    return b"".join(rows)


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
            raise Blocked("manifest target already exists")
        raise OSError(error, os.strerror(error), os.fspath(target))


def publish_manifest(phase: str) -> dict[str, Any]:
    validate_p0_pins()
    need(phase in {"payload", "root"}, "manifest phase")
    if phase == "payload":
        validate_sealed_exact_six()
        members = PAYLOAD_MEMBERS
        target = ROOT / PAYLOAD_MANIFEST
    else:
        strict_outer_verification()
        members = ROOT_MEMBERS
        target = ROOT / ROOT_MANIFEST
    try:
        target.lstat()
    except FileNotFoundError:
        pass
    else:
        raise Blocked("manifest target already exists")
    payload = manifest_bytes(members)
    validate_p0_pins()
    if phase == "root":
        strict_outer_verification()
    need(manifest_bytes(members) == payload, "manifest member map stable across capture")
    descriptor, staging_name = tempfile.mkstemp(
        prefix="." + target.name + ".staging-", dir=ROOT
    )
    staging = Path(staging_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(staging, 0o600)
        need(staging.read_bytes() == payload, "manifest staging bytes")
        rename_noreplace(staging, target)
        fsync_directory(ROOT)
    finally:
        if staging.exists() and not staging.is_symlink():
            staging.unlink()
    return {
        "schema": "cm2.round306c30c.publication-manifest-build.v1",
        "status": "PASS_" + phase.upper() + "_MANIFEST_BUILT__ZERO_FORMAL_CREDIT",
        "phase": phase,
        "manifest": target.name,
        "manifest_sha256": file_hash(target),
        "member_count": len(members),
        "formal_credit": 0,
        "source_W_transition_authorized": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("payload", "root"), required=True)
    arguments = parser.parse_args()
    try:
        output = publish_manifest(arguments.phase)
    except (Blocked, OSError, ValueError, KeyError, TypeError) as error:
        print(canonical({
            "schema": "cm2.round306c30c.publication-manifest-build.v1",
            "status": "BLOCKED_FAIL_CLOSED",
            "phase": arguments.phase,
            "error": str(error),
            "formal_credit": 0,
            "source_W_transition_authorized": False,
        }).decode("ascii"))
        return 1
    print(canonical(output).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
