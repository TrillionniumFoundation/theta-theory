#!/usr/bin/env python3
"""Build the append-only C28-v2 release-repair manifests.

This builder accepts only the formal current-byte boundary validation and the
v3 real private filesystem/process attack package.  The earlier 32-case
projection and the earlier C28 terminal are historical audit-hold evidence;
neither can authorize this package.  This source never writes a seal, a
terminal receipt, or a PASS lock.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
AUDIT = ROOT / ".cm2-runtime/audit"
PREFIX = "cm2.round306c28.source-g-post-c27r2-125561998198-pair-routing.v2."

CORE_SCHEMA = PREFIX + "gated-dual-seed-core-receipt.v1"
CORE_STATUS = (
    "PASS_C27R2_TERMINAL_ADAPTER_DUAL_TRUE_SEED_THREE_FILE_CANDIDATES_"
    "TWO_NO_IMPORT_VERIFIERS_AND_26_ATTACKS__ZERO_CREDIT_PENDING_RELEASE"
)
COLD_SCHEMA = PREFIX + "release-cold-replay-receipt.v1"
COLD_STATUS = (
    "PASS_FRESH_NO_IMPORT_C28_PAIR_ROUTING_COLD_BYTE_REPLAY_WITH_ALL_"
    "DECLARED_CORE_INPUT_PRE_POST_SHA_STAT__ZERO_CREDIT"
)
EVIDENCE_SCHEMA = PREFIX + "release-evidence-bundle.v1"
EVIDENCE_STATUS = (
    "PASS_C28_CORE_COLD_32_RELEASE_ATTACKS_AND_ALL_AUTHORITY_INPUT_"
    "SHA_STAT_EVIDENCE__ZERO_CREDIT"
)
BOUNDARY_SCHEMA = PREFIX + "release-boundary-independent-validation.v1"
BOUNDARY_STATUS = (
    "PASS_C28_V2_FORMAL_REAL_RELEASE_BOUNDARY_CURRENT_BYTES_C27R2_CORE_"
    "PROCESS_COLD_AND_CANONICAL_CLOSURE__ZERO_CREDIT"
)
REAL_ATTACK_SCHEMA = PREFIX + "real-release-only-attack-harness.v3"
REAL_ATTACK_STATUS = (
    "PASS_C28_V2_FORMAL_BASELINE_AND_40_OF_40_REAL_PRIVATE_FILESYSTEM_"
    "PROCESS_TOCTOU_ENV_COLD_MANIFEST_AND_TERMINAL_ATTACKS_REJECTED__"
    "ZERO_CREDIT_PENDING_REPAIR_MANIFEST_OUTER_SEAL_TERMINAL"
)
RESULT_SCHEMA = PREFIX + "producer-result.v1"
RESULT_STATUS = (
    "PASS_POST_C27R2_PARTITION_502204_MEMBERS_43684_COMPONENTS_AND_"
    "32896_PAIR_SHARDS_REBUILT__125561998198_EXACT_NONEDGE_CANDIDATE_"
    "ZERO_CREDIT__C28_UNAUTHORIZED_PENDING_RELEASE_TERMINAL"
)
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
MANIFEST_SCHEMA = PREFIX + "release-repair-manifest-receipt.v2"
MANIFEST_STATUS = (
    "PASS_C28_RELEASE_REPAIR_MANIFEST_FIRST_REAL_BOUNDARY_40_FIXTURE_"
    "TRANSCRIPTS_CORE_COLD_EVIDENCE_AND_C27R2_ROOT_CLOSURE__ZERO_CREDIT_"
    "PENDING_OUTER_TEMPLATE_TERMINAL"
)

EXPECTED = {
    "members": 502_204, "post_components": 43_684, "blocks": 256,
    "shards": 32_896, "total_pairs": 126_104_177_706,
    "within_pairs": 542_179_508, "cross_pairs": 125_561_998_198,
}
CANDIDATE_FILES = {
    "member_home_block_census.jsonl.gz",
    "cross_component_pair_route_shard.jsonl.gz", "result.json",
}
BOUNDARY_INVENTORY = {
    "PASS.lock", "authority_inventory.sha256", "validation.json",
}
REAL_ATTACK_INVENTORY = {"PASS.lock", "release_attacks.json"}
REAL_WORK_INVENTORY = {
    "case_receipts.jsonl", "case_receipts_manifest.sha256",
    "cleanup_receipt.json",
}
BOUNDARY_PASS = (
    b"PASS_C28_V2_REAL_RELEASE_BOUNDARY_FORMAL_CURRENT_BYTES__ZERO_CREDIT\n"
)
REAL_ATTACK_PASS = b"PASS_C28_V2_40_REAL_RELEASE_ONLY_ATTACKS__ZERO_CREDIT\n"

C27 = {
    "root": "1f65a624c889773e3104c4311788fc06be04d6ca92e033205074b8cc7f5b27fc",
    "receipt_file": "feccb0b9290bd82ac1d8e78e8e7a21d4f25e0ca3aa3556cc3f0bb6007f61c3dd",
    "receipt_object": "8afbd127c9518f569c2f7b3edcdbe9e0ebf77d88bcca855822e58d21e5cfe782",
    "replay_file": "b480df4b8caaf9876a48720f92a8fb6d86e2b1b5966bcc71b0022c5e49fc12ee",
    "replay_object": "216d2592c49b0302de0042677ce54c96cd5ad1fcb32231da02b39c003cb837e8",
    "pass": "5fe4140b3e8f38196e9ca68cd336ae29be1c8847c7685526f08aa4d7173d7348",
}
C27_STATUS = "PASS_C27R2_TERMINAL_BYTE_REPLAY__FORMAL_C27R2_AUTHORITY_MINTED"
C27_PASS = b"PASS_C27R2_AUTHORITY_V2_TERMINAL_BYTE_REPLAY__C28_C29_UNAUTHORIZED\n"

HISTORICAL_C28 = {
    "root": "252964856f55584dc2fab6f7a1f0ac4cadd66fd6935b4063bdbe0eb455ba0982",
    "receipt_file": "bde9d40da7f5a548f75d0885b377d3f1a654786be5f748b14a2e1b0ea720ec73",
    "receipt_object": "53eca26fcfa87a6f8c4f557740dd4170b0f38ff54afec07f82af82a035ad7f13",
    "replay_file": "ad93a50c9871dd2cf771256ffb3ad4485c648de695453118956831f0e2c16750",
    "replay_object": "5bcaa87e88ebf2214bde5462bd3148f6600732c3d79394a234a7c447aba99079",
    "chain_file": "39d9727162be21ee4f3a0b790ea8d75532a6b189e89da477f2bda2adbdbf6089",
    "chain_object": "ec664037bdbb38e90e6029600efdeaccf8a5b6cb2867418b006901d9484fab9e",
    "pass": "a8d3b06c5794a5b0edbbec633ee45b29ce81b97ea707eba3a43d6e6d98ef5509",
}


class Blocked(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Blocked(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def object_sha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def valid_sha(value: Any) -> bool:
    return (type(value) is str and len(value) == 64
            and all(character in "0123456789abcdef" for character in value))


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace(
        "+00:00", "Z")


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns,
            value.st_uid, value.st_gid)


def capture(path: Path) -> tuple[bytes, str, tuple[int, ...]]:
    absolute = path.absolute()
    need(absolute.resolve(strict=True) == absolute,
         "canonical existing path:" + str(path))
    fd = os.open(absolute, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                 | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular single-link file:" + str(path))
        chunks: list[bytes] = []
        state = hashlib.sha256()
        while block := os.read(fd, 4 << 20):
            chunks.append(block)
            state.update(block)
        current = os.stat(absolute, follow_symlinks=False)
        need(fingerprint(before) == fingerprint(os.fstat(fd))
             == fingerprint(current), "stable SHA/stat:" + str(path))
        return b"".join(chunks), state.hexdigest(), fingerprint(before)
    finally:
        os.close(fd)


def file_sha(path: Path) -> str:
    return capture(path)[1]


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
    payload, _, _ = capture(path)
    need(payload.endswith(b"\n") and not payload.endswith(b"\n\n"),
         "single JSON newline:" + str(path))
    value = strict_load(payload[:-1])
    need(type(value) is dict and canonical(value) == payload[:-1],
         "canonical JSON:" + str(path))
    body = dict(value)
    claim = body.pop(closure, None)
    need(valid_sha(claim) and claim == object_sha(body),
         "object closure:" + str(path))
    return value


def manifest(path: Path) -> dict[str, str]:
    payload, _, _ = capture(path)
    need(payload.endswith(b"\n") and payload != b"\n",
         "nonempty manifest:" + str(path))
    result: dict[str, str] = {}
    for line in payload.decode("ascii").splitlines():
        fields = line.split("  ", 1)
        need(len(fields) == 2 and valid_sha(fields[0])
             and fields[1] not in result and fields[1],
             "manifest syntax/unique path")
        relative = Path(fields[1])
        need(not relative.is_absolute()
             and all(part not in {"", ".", ".."} for part in relative.parts)
             and str(relative) == fields[1], "canonical manifest path")
        result[fields[1]] = fields[0]
    need(list(result) == sorted(result), "manifest ordering")
    for relative, expected in result.items():
        need(file_sha(ROOT / relative) == expected,
             "current manifest member:" + relative)
    return result


def build_manifest(paths: set[Path]) -> bytes:
    rows = sorted((str(path.absolute().relative_to(ROOT)), file_sha(path))
                  for path in paths)
    need(rows and len(rows) == len({path for path, _ in rows}),
         "nonempty unique manifest members")
    return ("\n".join(f"{sha256}  {path}" for path, sha256 in rows)
            + "\n").encode("ascii")


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


def audit_dir(raw: str, inventory: set[str] | None = None) -> Path:
    path = Path(raw).absolute()
    need(path.parent == AUDIT and path.is_dir() and not path.is_symlink(),
         "direct audit directory:" + str(path))
    if inventory is not None:
        need({entry.name for entry in path.iterdir()} == inventory,
             "exact inventory:" + path.name)
    return path


def direct_file(raw: str) -> Path:
    path = Path(raw).absolute()
    need(path.parent == AUDIT and path.is_file() and not path.is_symlink(),
         "direct audit file:" + str(path))
    return path


def validate_c27(path: Path) -> None:
    need({entry.name for entry in path.iterdir()} == {
        "PASS.lock", "chain_status.json", "payload_manifest.sha256",
        "root_manifest.sha256", "terminal_receipt.json",
        "terminal_replay.json"}, "exact C27R2 terminal inventory")
    receipt = document(path / "terminal_receipt.json", "terminal_receipt_sha256")
    replay = document(path / "terminal_replay.json", "terminal_replay_sha256")
    need(file_sha(path / "root_manifest.sha256") == C27["root"]
         and file_sha(path / "terminal_receipt.json") == C27["receipt_file"]
         and receipt["terminal_receipt_sha256"] == C27["receipt_object"]
         and file_sha(path / "terminal_replay.json") == C27["replay_file"]
         and replay["terminal_replay_sha256"] == C27["replay_object"]
         and file_sha(path / "PASS.lock") == C27["pass"]
         and (path / "PASS.lock").read_bytes() == C27_PASS
         and receipt.get("status") == C27_STATUS
         and receipt.get("authority_minted") is True
         and receipt.get("manifest_authorized") is True,
         "immutable C27R2 authority")
    manifest(path / "payload_manifest.sha256")
    manifest(path / "root_manifest.sha256")


def validate_historical(path: Path) -> None:
    need({entry.name for entry in path.iterdir()} == {
        "PASS.lock", "chain_status.json", "payload_manifest.sha256",
        "root_manifest.sha256", "terminal_receipt.json",
        "terminal_replay.json"}, "exact historical C28 inventory")
    receipt = document(path / "terminal_receipt.json", "terminal_receipt_sha256")
    replay = document(path / "terminal_replay.json", "terminal_replay_sha256")
    chain = document(path / "chain_status.json", "chain_status_sha256")
    need(file_sha(path / "root_manifest.sha256") == HISTORICAL_C28["root"]
         and file_sha(path / "terminal_receipt.json")
             == HISTORICAL_C28["receipt_file"]
         and receipt["terminal_receipt_sha256"]
             == HISTORICAL_C28["receipt_object"]
         and file_sha(path / "terminal_replay.json")
             == HISTORICAL_C28["replay_file"]
         and replay["terminal_replay_sha256"]
             == HISTORICAL_C28["replay_object"]
         and file_sha(path / "chain_status.json")
             == HISTORICAL_C28["chain_file"]
         and chain["chain_status_sha256"] == HISTORICAL_C28["chain_object"]
         and file_sha(path / "PASS.lock") == HISTORICAL_C28["pass"],
         "historical C28 byte pins")
    manifest(path / "payload_manifest.sha256")
    manifest(path / "root_manifest.sha256")


def execute(args: argparse.Namespace) -> dict[str, Any]:
    dynamic = (
        args.expect_builder_sha256, args.expect_core_receipt_file_sha256,
        args.expect_core_receipt_object_sha256, args.expect_core_pass_sha256,
        args.expect_cold_receipt_file_sha256,
        args.expect_cold_receipt_object_sha256,
        args.expect_evidence_file_sha256, args.expect_evidence_object_sha256,
        args.expect_boundary_file_sha256, args.expect_boundary_object_sha256,
        args.expect_boundary_inventory_sha256,
        args.expect_real_attack_file_sha256,
        args.expect_real_attack_object_sha256,
        args.expect_case_receipts_file_sha256,
        args.expect_case_manifest_sha256, args.expect_cleanup_file_sha256,
        args.expect_cleanup_object_sha256, args.expect_attack_name_digest,
    )
    need(all(valid_sha(item) and item != "0" * 64 for item in dynamic)
         and file_sha(SELF) == args.expect_builder_sha256,
         "non-placeholder dynamic pins and builder self pin")

    control = audit_dir(args.core_control_dir)
    predecessor = audit_dir(args.predecessor_terminal_dir)
    historical = audit_dir(args.historical_c28_terminal_dir)
    adapter = audit_dir(args.adapter_dir)
    candidate = audit_dir(args.candidate_dir, CANDIDATE_FILES)
    cold_control = audit_dir(args.cold_control_dir)
    cold_output = audit_dir(args.cold_output_dir)
    cold_run = audit_dir(args.cold_run_dir)
    evidence_dir = audit_dir(args.evidence_dir)
    boundary_dir = audit_dir(args.boundary_formal_dir, BOUNDARY_INVENTORY)
    real_attack_dir = audit_dir(args.real_attack_dir, REAL_ATTACK_INVENTORY)
    real_work_dir = audit_dir(args.real_work_dir, REAL_WORK_INVENTORY)
    formal = direct_file(args.formal_verification_file)
    core_attacks_path = direct_file(args.core_attacks_file)
    output = Path(args.output_dir).absolute()
    need(output.parent == AUDIT and not output.exists()
         and not output.is_symlink(), "fresh manifest output")

    validate_c27(predecessor)
    validate_historical(historical)

    core_path = control / "core_receipt.json"
    core = document(core_path, "core_receipt_sha256")
    need(file_sha(core_path) == args.expect_core_receipt_file_sha256
         and core["core_receipt_sha256"]
             == args.expect_core_receipt_object_sha256
         and core.get("schema") == CORE_SCHEMA and core.get("status") == CORE_STATUS
         and core.get("exact_math") == EXPECTED
         and core.get("formal_credit") == 0
         and core.get("manifest_authorized") is False
         and core.get("C28") == "UNAUTHORIZED_PENDING_RELEASE_TERMINAL"
         and file_sha(control / "PASS.lock") == args.expect_core_pass_sha256,
         "core-v5 exact zero-credit boundary")
    pins = core.get("predecessor_terminal_pins", {})
    need(pins.get("terminal_root_sha256") == C27["root"]
         and pins.get("terminal_receipt_file_sha256") == C27["receipt_file"]
         and pins.get("terminal_receipt_object_sha256") == C27["receipt_object"]
         and pins.get("terminal_replay_file_sha256") == C27["replay_file"]
         and pins.get("terminal_replay_object_sha256") == C27["replay_object"]
         and pins.get("terminal_pass_lock_sha256") == C27["pass"],
         "core-v5 binds C27R2 authority")

    result = document(candidate / "result.json", "result_sha256")
    verification = document(formal, "verification_sha256")
    core_attacks = document(core_attacks_path, "attack_receipt_sha256")
    need(result.get("schema") == RESULT_SCHEMA and result.get("status") == RESULT_STATUS
         and result.get("formal_credit") == 0
         and result.get("manifest_authorized") is False
         and verification.get("schema") == VERIFICATION_SCHEMA
         and verification.get("status") == VERIFICATION_STATUS
         and verification.get("candidate_result_sha256") == result["result_sha256"]
         and verification.get("verified_census") == EXPECTED
         and verification.get("independence") == {
             "producer_executed": False, "producer_imported": False}
         and core_attacks.get("schema") == CORE_ATTACK_SCHEMA
         and core_attacks.get("status") == CORE_ATTACK_STATUS
         and core_attacks.get("attack_census") == {
             "accepted": 0, "executed": 26, "planned": 26,
             "rejected_fail_closed": 26},
         "selected core candidate/verifier/26 attacks")

    cold_path = cold_control / "cold_replay_receipt.json"
    cold = document(cold_path, "cold_replay_receipt_sha256")
    evidence_path = evidence_dir / "evidence_bundle.json"
    evidence = document(evidence_path, "evidence_bundle_sha256")
    evidence_inventory_path = evidence_dir / "authority_inventory.sha256"
    evidence_inventory = manifest(evidence_inventory_path)
    need(file_sha(cold_path) == args.expect_cold_receipt_file_sha256
         and cold["cold_replay_receipt_sha256"]
             == args.expect_cold_receipt_object_sha256
         and cold.get("schema") == COLD_SCHEMA and cold.get("status") == COLD_STATUS
         and cold.get("cold_replay_byte_identical") is True
         and cold.get("all_declared_core_inputs_pre_post_sha_stat_identical") is True
         and file_sha(evidence_path) == args.expect_evidence_file_sha256
         and evidence["evidence_bundle_sha256"]
             == args.expect_evidence_object_sha256
         and evidence.get("schema") == EVIDENCE_SCHEMA
         and evidence.get("status") == EVIDENCE_STATUS
         and file_sha(evidence_inventory_path)
             == evidence.get("authority_inventory_sha256")
         and len(evidence_inventory) == evidence.get("authority_member_count")
         and all(item.get("formal_credit") == 0
                 and item.get("manifest_authorized") is False
                 for item in (cold, evidence)),
         "cold and historical evidence current closure")

    boundary_path = boundary_dir / "validation.json"
    boundary = document(boundary_path, "validation_sha256")
    boundary_inventory_path = boundary_dir / "authority_inventory.sha256"
    boundary_inventory = manifest(boundary_inventory_path)
    need(file_sha(boundary_path) == args.expect_boundary_file_sha256
         and boundary["validation_sha256"]
             == args.expect_boundary_object_sha256
         and boundary.get("schema") == BOUNDARY_SCHEMA
         and boundary.get("status") == BOUNDARY_STATUS
         and (boundary_dir / "PASS.lock").read_bytes() == BOUNDARY_PASS
         and file_sha(boundary_inventory_path)
             == args.expect_boundary_inventory_sha256
         and boundary.get("validation_mode") == "FORMAL_CURRENT_BYTES"
         and boundary.get("path_resolution", {}).get("entry_count") == 0
         and boundary.get("path_resolution", {}).get("canonical_workspace_paths_only") is True
         and boundary.get("path_resolution", {}).get("race_barrier_used") is False
         and boundary.get("path_resolution", {}).get("isolated_python") is True
         and boundary.get("current_authority_inventory", {}).get("manifest_sha256")
             == args.expect_boundary_inventory_sha256
         and boundary.get("current_authority_inventory", {}).get("member_count")
             == len(boundary_inventory)
         and boundary.get("current_authority_inventory", {}).get("all_regular_single_link") is True
         and boundary.get("current_authority_inventory", {}).get(
             "all_current_sha_and_complete_9_stat_match_recorded") is True
         and boundary.get("exact_math") == EXPECTED
         and boundary.get("formal_credit") == 0
         and boundary.get("manifest_authorized") is False,
         "formal real boundary current-byte receipt")

    real_attack_path = real_attack_dir / "release_attacks.json"
    real_attack = document(real_attack_path, "release_attack_receipt_sha256")
    cases_path = real_work_dir / "case_receipts.jsonl"
    case_manifest_path = real_work_dir / "case_receipts_manifest.sha256"
    cleanup_path = real_work_dir / "cleanup_receipt.json"
    cleanup = document(cleanup_path, "cleanup_receipt_sha256")
    case_manifest = manifest(case_manifest_path)
    need(file_sha(real_attack_path) == args.expect_real_attack_file_sha256
         and real_attack["release_attack_receipt_sha256"]
             == args.expect_real_attack_object_sha256
         and real_attack.get("schema") == REAL_ATTACK_SCHEMA
         and real_attack.get("status") == REAL_ATTACK_STATUS
         and (real_attack_dir / "PASS.lock").read_bytes() == REAL_ATTACK_PASS
         and real_attack.get("attack_census") == {
             "accepted": 0, "executed": 40, "planned": 40,
             "rejected_fail_closed": 40}
         and real_attack.get("ordered_attack_name_sha256")
             == args.expect_attack_name_digest
         and real_attack.get("formal_validation_file_sha256")
             == args.expect_boundary_file_sha256
         and real_attack.get("formal_validation_object_sha256")
             == args.expect_boundary_object_sha256
         and real_attack.get("authority_pre_post_sha_stat_identical") is True
         and real_attack.get("formal_credit") == 0
         and real_attack.get("manifest_authorized") is False
         and file_sha(cases_path) == args.expect_case_receipts_file_sha256
         and file_sha(case_manifest_path) == args.expect_case_manifest_sha256
         and str(cases_path.relative_to(ROOT)) in case_manifest
         and case_manifest[str(cases_path.relative_to(ROOT))]
             == args.expect_case_receipts_file_sha256
         and file_sha(cleanup_path) == args.expect_cleanup_file_sha256
         and cleanup["cleanup_receipt_sha256"]
             == args.expect_cleanup_object_sha256
         and cleanup.get("all_private_cases_removed") is True,
         "40 real attack receipt/transcript/cleanup closure")

    transcript_members = {ROOT / relative for relative in case_manifest}
    payload_paths = {
        *(candidate / name for name in CANDIDATE_FILES), formal,
        core_attacks_path, core_path, control / "PASS.lock",
        control / "pinset.json", cold_path, cold_control / "PASS.lock",
        cold_output / "verification.json", cold_run / "run_attestation.json",
        evidence_path, evidence_inventory_path,
        boundary_path, boundary_inventory_path, boundary_dir / "PASS.lock",
        real_attack_path, real_attack_dir / "PASS.lock", cases_path,
        case_manifest_path, cleanup_path,
        adapter / "authority_contract.json", adapter / "root_manifest.sha256",
        adapter / "terminal_receipt.json", adapter / "PASS.lock",
        predecessor / "root_manifest.sha256",
        predecessor / "terminal_receipt.json",
        predecessor / "terminal_replay.json", predecessor / "chain_status.json",
        predecessor / "PASS.lock", historical / "root_manifest.sha256",
        historical / "terminal_receipt.json",
        historical / "terminal_replay.json", historical / "chain_status.json",
        historical / "PASS.lock", SELF, *transcript_members,
    }
    payload_raw = build_manifest(payload_paths)
    if args.preflight_only:
        return {"status":
                "PASS_C28_RELEASE_REPAIR_MANIFEST_PREFLIGHT__NO_OUTPUT_"
                "CREATED_ZERO_CREDIT"}

    output.mkdir(mode=0o700)
    payload_path = output / "payload_manifest.sha256"
    write_once(payload_path, payload_raw)
    root_paths = {
        payload_path, core_path, control / "PASS.lock", cold_path,
        evidence_path, boundary_path, boundary_inventory_path,
        real_attack_path, case_manifest_path, cleanup_path,
        predecessor / "root_manifest.sha256",
        predecessor / "terminal_receipt.json",
        predecessor / "terminal_replay.json", predecessor / "PASS.lock",
        historical / "root_manifest.sha256",
        historical / "terminal_receipt.json",
        historical / "terminal_replay.json", historical / "PASS.lock", SELF,
    }
    root_path = output / "root_manifest.sha256"
    write_once(root_path, build_manifest(root_paths))
    payload = manifest(payload_path)
    root = manifest(root_path)
    body = {
        "schema": MANIFEST_SCHEMA, "status": MANIFEST_STATUS,
        "built_at_utc": now(),
        "payload_manifest_file_sha256": file_sha(payload_path),
        "payload_member_count": len(payload),
        "root_manifest_file_sha256": file_sha(root_path),
        "root_member_count": len(root),
        "core_receipt_file_sha256": args.expect_core_receipt_file_sha256,
        "core_receipt_object_sha256": args.expect_core_receipt_object_sha256,
        "cold_replay_receipt_file_sha256": args.expect_cold_receipt_file_sha256,
        "cold_replay_receipt_object_sha256": args.expect_cold_receipt_object_sha256,
        "evidence_bundle_file_sha256": args.expect_evidence_file_sha256,
        "evidence_bundle_object_sha256": args.expect_evidence_object_sha256,
        "formal_boundary_file_sha256": args.expect_boundary_file_sha256,
        "formal_boundary_object_sha256": args.expect_boundary_object_sha256,
        "formal_boundary_inventory_sha256":
            args.expect_boundary_inventory_sha256,
        "real_attack_file_sha256": args.expect_real_attack_file_sha256,
        "real_attack_object_sha256": args.expect_real_attack_object_sha256,
        "case_receipts_file_sha256": args.expect_case_receipts_file_sha256,
        "case_receipts_manifest_sha256": args.expect_case_manifest_sha256,
        "cleanup_receipt_file_sha256": args.expect_cleanup_file_sha256,
        "cleanup_receipt_object_sha256": args.expect_cleanup_object_sha256,
        "ordered_attack_name_sha256": args.expect_attack_name_digest,
        "real_release_attack_count": 40,
        "selected_candidate_result_object_sha256": result["result_sha256"],
        "C27R2_terminal_pins": dict(C27),
        "C27R2_terminal_root_manifest_sha256": C27["root"],
        "historical_C28_v1_terminal_pins": dict(HISTORICAL_C28),
        "historical_C28_v1_terminal_role": "AUDIT_HOLD_EVIDENCE_ONLY",
        "historical_C28_v1_terminal_authoritative": False,
        "legacy_32_projection_attack_harness_authoritative": False,
        "only_real_boundary_v1_and_real_attack_v3_authoritative": True,
        "exact_math": EXPECTED, "predecessor_root_closure": True,
        "formal_credit": 0, "manifest_authorized": False,
        "C27R2": "AUTHORIZED_PREDECESSOR_ONLY",
        "C28": "UNAUTHORIZED_PENDING_INDEPENDENT_OUTER_TEMPLATE_AND_TERMINAL",
        "C29": "UNAUTHORIZED", "Source_W": "UNCHANGED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    receipt = {**body, "manifest_receipt_sha256": object_sha(body)}
    write_once(output / "manifest_receipt.json", canonical(receipt) + b"\n")
    need({entry.name for entry in output.iterdir()} == {
        "manifest_receipt.json", "payload_manifest.sha256",
        "root_manifest.sha256"}, "exact manifest output inventory")
    return receipt


def self_test() -> dict[str, Any]:
    need(EXPECTED["total_pairs"]
             == EXPECTED["within_pairs"] + EXPECTED["cross_pairs"]
         and len(C27) == 6 and len(HISTORICAL_C28) == 8
         and BOUNDARY_INVENTORY == {
             "PASS.lock", "authority_inventory.sha256", "validation.json"}
         and REAL_WORK_INVENTORY == {
             "case_receipts.jsonl", "case_receipts_manifest.sha256",
             "cleanup_receipt.json"}, "fixed repair-chain fixtures")
    return {"status": "PASS_C28_RELEASE_REPAIR_MANIFEST_BUILDER_V2_SELF_TEST",
            "formal_credit": 0, "C28": "UNAUTHORIZED",
            "CM2": "NO-GO_FOR_CLAIM"}


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--self-test", action="store_true")
    value.add_argument("--preflight-only", action="store_true")
    for name in (
        "core-control-dir", "predecessor-terminal-dir",
        "historical-c28-terminal-dir", "adapter-dir", "candidate-dir",
        "formal-verification-file", "core-attacks-file", "cold-control-dir",
        "cold-output-dir", "cold-run-dir", "evidence-dir",
        "boundary-formal-dir", "real-attack-dir", "real-work-dir",
        "output-dir", "expect-builder-sha256",
        "expect-core-receipt-file-sha256",
        "expect-core-receipt-object-sha256", "expect-core-pass-sha256",
        "expect-cold-receipt-file-sha256",
        "expect-cold-receipt-object-sha256",
        "expect-evidence-file-sha256", "expect-evidence-object-sha256",
        "expect-boundary-file-sha256", "expect-boundary-object-sha256",
        "expect-boundary-inventory-sha256",
        "expect-real-attack-file-sha256",
        "expect-real-attack-object-sha256",
        "expect-case-receipts-file-sha256", "expect-case-manifest-sha256",
        "expect-cleanup-file-sha256", "expect-cleanup-object-sha256",
        "expect-attack-name-digest",
    ):
        value.add_argument("--" + name)
    return value


def main() -> int:
    args = parser().parse_args()
    fields = tuple(name for name in vars(args)
                   if name not in {"self_test", "preflight_only"})
    try:
        if args.self_test:
            need(not args.preflight_only
                 and all(getattr(args, field) is None for field in fields),
                 "self-test accepts no run arguments")
            result = self_test()
        else:
            need(all(getattr(args, field) is not None for field in fields),
                 "all run arguments required")
            result = execute(args)
        sys.stdout.buffer.write(canonical({
            "CM2": "NO-GO_FOR_CLAIM", "formal_credit": 0,
            "status": result["status"],
        }) + b"\n")
        return 0
    except (Blocked, OSError, ValueError, KeyError, TypeError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
