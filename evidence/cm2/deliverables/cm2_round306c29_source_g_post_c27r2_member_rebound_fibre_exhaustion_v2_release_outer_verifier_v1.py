#!/usr/bin/env python3
"""Independently verify the C29-v2 release graph and all candidate ledgers."""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
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
PREFIX = "cm2_round306c29_source_g_post_c27r2_member_rebound_fibre_exhaustion_v2"
BASE = "cm2.round306c29.source-g-post-c27r2-member-rebound-fibre-exhaustion.v2."
CORE_SCHEMA = BASE + "gated-dual-terminal-seed-core-receipt.v1"
COLD_SCHEMA = BASE + "release-cold-replay-receipt.v1"
EVIDENCE_SCHEMA = BASE + "release-evidence-bundle.v1"
ATTACK_SCHEMA = BASE + "release-only-attack-harness.v1"
MANIFEST_SCHEMA = BASE + "release-manifest-receipt.v1"
OUTER_SCHEMA = BASE + "release-outer-verification.v1"
OUTER_STATUS = "PASS_INDEPENDENT_C29_V2_FULL_LEDGER_DUAL_PREDECESSOR_MANIFEST_COLD_AND_40_RELEASE_ATTACK_CHECK__CONDITIONAL_ZERO_CREDIT"
RESULT_SCHEMA = BASE + "producer-result.v1"
VERIFY_SCHEMA = BASE + "independent-verification.v1"
COMPONENT_SCHEMA = BASE + "post-component-row.v1"
FIBRE_SCHEMA = BASE + "official-key-fibre-row.v1"
DISPOSITION_SCHEMA = BASE + "global-member-disposition-row.v1"
EXPECTED_MATH = {
    "members": 502_204, "representations": 549_616,
    "post_C27R2_components": 43_684, "official_keys": 124,
    "component_key_incidences": 60_296,
    "component_key_multiplicity_census": {
        "1": 27_108, "2": 16_556, "3": 8, "4": 8, "5": 4},
    "family_member_census": {"G2A": 5_264, "G2B": 10_128,
        "NON_GRAPH": 55_604, "PRESERVED": 126_468,
        "R2": 295_336, "R292": 9_404},
    "total_unordered_member_pairs": 126_104_177_706,
    "within_post_component_member_pairs": 542_179_508,
    "cross_post_component_member_pairs": 125_561_998_198,
}
LEDGERS = {
    "post_component_official_key_assignment": (
        PREFIX + "_post_component_official_key_assignment_ledger.jsonl.gz",
        COMPONENT_SCHEMA, 43_684, "LEXICOGRAPHIC_POST_C27R2_COMPONENT_ID"),
    "official_key_fibre_exhaustion": (
        PREFIX + "_official_key_fibre_exhaustion_ledger.jsonl.gz",
        FIBRE_SCHEMA, 124, "LEXICOGRAPHIC_OFFICIAL_KEY_ID"),
    "global_member_disposition": (
        PREFIX + "_global_member_disposition_ledger.jsonl.gz",
        DISPOSITION_SCHEMA, 502_204, "C25_MEMBER_ORDINAL"),
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
    return type(value) is str and len(value) == 64 and all(
        char in "0123456789abcdef" for char in value)


def strict(payload: bytes) -> Any:
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
    path = path.absolute()
    need(path.resolve(strict=True) == path, "canonical path:" + str(path))
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                         | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular singleton:" + str(path))
        state = hashlib.sha256()
        while block := os.read(descriptor, 4 << 20):
            state.update(block)
        need(fingerprint(os.fstat(descriptor)) == fingerprint(before),
             "stable SHA/stat:" + str(path))
        return state.hexdigest()
    finally:
        os.close(descriptor)


def document(path: Path, closure: str) -> dict[str, Any]:
    payload = path.read_bytes()
    need(payload.endswith(b"\n") and not payload.endswith(b"\n\n"),
         "JSON newline:" + str(path))
    value = strict(payload[:-1])
    need(type(value) is dict and canonical(value) == payload[:-1],
         "canonical JSON:" + str(path))
    body = dict(value)
    claim = body.pop(closure, None)
    need(valid_sha(claim) and claim == digest(body),
         "object closure:" + str(path))
    return value


def parse_manifest(path: Path) -> dict[str, str]:
    payload = path.read_bytes()
    need(payload.endswith(b"\n"), "manifest newline")
    result: dict[str, str] = {}
    for line in payload.decode("ascii").splitlines():
        fields = line.split("  ", 1)
        need(len(fields) == 2 and valid_sha(fields[0])
             and fields[1] not in result and fields[1] != "", "manifest row")
        relative = Path(fields[1])
        need(not relative.is_absolute() and str(relative) == fields[1]
             and all(part not in {"", ".", ".."} for part in relative.parts),
             "canonical manifest path")
        result[fields[1]] = fields[0]
    need(list(result) == sorted(result), "manifest sorted")
    for raw, expected in result.items():
        need(file_sha(ROOT / raw) == expected, "manifest member drift:" + raw)
    return result


def write_once(path: Path, payload: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                         | getattr(os, "O_NOFOLLOW", 0), 0o400)
    try:
        offset = 0
        while offset < len(payload):
            offset += os.write(descriptor, payload[offset:])
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def ledger(path: Path, schema: str, expected_count: int,
           order: str) -> tuple[dict[str, Any], dict[str, Any]]:
    raw_header = path.read_bytes()[:10]
    need(len(raw_header) == 10 and raw_header[:2] == b"\x1f\x8b"
         and raw_header[4:8] == b"\x00\x00\x00\x00", "deterministic gzip header")
    sequence = hashlib.sha256()
    count = 0
    previous: str | None = None
    aggregates = {"members": 0, "representations": 0, "within": 0,
                  "incidences": 0, "multiplicity": Counter()}
    with gzip.open(path, "rb") as source:
        for raw in source:
            need(raw.endswith(b"\n"), "ledger row newline")
            row = strict(raw[:-1])
            need(type(row) is dict and canonical(row) == raw[:-1]
                 and row.get("schema") == schema and row.get("ordinal") == count,
                 "canonical ledger schema/ordinal")
            body = dict(row)
            claim = body.pop("row_sha256", None)
            need(valid_sha(claim) and claim == digest(body), "ledger row closure")
            sequence.update(bytes.fromhex(claim))
            if schema == COMPONENT_SCHEMA:
                key = row.get("post_C27R2_component_id")
                need(type(key) is str and (previous is None or previous < key),
                     "component lexical order")
                previous = key
                members = row.get("member_count")
                representations = row.get("representation_count")
                keys = row.get("official_key_count")
                need(type(members) is int and members > 0
                     and type(representations) is int and representations >= members
                     and type(keys) is int and 1 <= keys <= 5,
                     "component census row")
                aggregates["members"] += members
                aggregates["representations"] += representations
                aggregates["within"] += members * (members - 1) // 2
                aggregates["incidences"] += keys
                aggregates["multiplicity"][keys] += 1
            elif schema == FIBRE_SCHEMA:
                key = row.get("official_key_id")
                need(type(key) is str and (previous is None or previous < key),
                     "fibre lexical order")
                previous = key
            count += 1
    need(count == expected_count, "ledger row count")
    descriptor = {"filename": path.name, "row_count": count,
                  "size": path.stat().st_size, "sha256": file_sha(path),
                  "row_sequence_sha256": sequence.hexdigest(), "order": order}
    aggregates["multiplicity"] = {
        str(key): value for key, value in sorted(aggregates["multiplicity"].items())}
    return descriptor, aggregates


def execute(args: argparse.Namespace) -> dict[str, Any]:
    pins = (args.expect_outer_sha256, args.expect_manifest_receipt_file_sha256,
            args.expect_manifest_receipt_object_sha256,
            args.expect_payload_manifest_sha256,
            args.expect_root_manifest_sha256,
            args.expect_core_receipt_file_sha256,
            args.expect_core_receipt_object_sha256,
            args.expect_cold_receipt_file_sha256,
            args.expect_cold_receipt_object_sha256,
            args.expect_evidence_file_sha256,
            args.expect_evidence_object_sha256,
            args.expect_release_attacks_file_sha256,
            args.expect_release_attacks_object_sha256)
    need(all(valid_sha(value) for value in pins)
         and file_sha(SELF) == args.expect_outer_sha256, "all outer/dynamic pins")
    control = Path(args.core_control_dir).absolute()
    cold_control = Path(args.cold_control_dir).absolute()
    evidence_dir = Path(args.evidence_dir).absolute()
    attacks_path = Path(args.release_attacks_file).absolute()
    manifest_dir = Path(args.manifest_dir).absolute()
    output = Path(args.output_file).absolute()
    need(output.parent == AUDIT and not output.exists(), "fresh outer output")
    need(manifest_dir.parent == AUDIT and manifest_dir.is_dir()
         and {entry.name for entry in manifest_dir.iterdir()} == {
             "manifest_receipt.json", "payload_manifest.sha256",
             "root_manifest.sha256"}, "manifest exact inventory")
    manifest_receipt_path = manifest_dir / "manifest_receipt.json"
    payload_path = manifest_dir / "payload_manifest.sha256"
    root_path = manifest_dir / "root_manifest.sha256"
    manifest_receipt = document(manifest_receipt_path, "manifest_receipt_sha256")
    payload = parse_manifest(payload_path)
    root = parse_manifest(root_path)
    need(file_sha(manifest_receipt_path) == args.expect_manifest_receipt_file_sha256
         and manifest_receipt["manifest_receipt_sha256"]
             == args.expect_manifest_receipt_object_sha256
         and manifest_receipt.get("schema") == MANIFEST_SCHEMA
         and file_sha(payload_path) == args.expect_payload_manifest_sha256
         and file_sha(root_path) == args.expect_root_manifest_sha256
         and manifest_receipt.get("payload_member_count") == len(payload)
         and manifest_receipt.get("root_member_count") == len(root)
         and manifest_receipt.get("dual_predecessor_root_closure") is True
         and manifest_receipt.get("formal_credit") == 0
         and manifest_receipt.get("manifest_authorized") is False,
         "manifest receipt/closure")
    core_path = control / "core_receipt.json"
    cold_path = cold_control / "cold_replay_receipt.json"
    evidence_path = evidence_dir / "evidence_bundle.json"
    core = document(core_path, "core_receipt_sha256")
    cold = document(cold_path, "cold_replay_receipt_sha256")
    evidence = document(evidence_path, "evidence_bundle_sha256")
    attacks = document(attacks_path, "release_attacks_sha256")
    need(core.get("schema") == CORE_SCHEMA
         and cold.get("schema") == COLD_SCHEMA
         and evidence.get("schema") == EVIDENCE_SCHEMA
         and attacks.get("schema") == ATTACK_SCHEMA
         and file_sha(core_path) == args.expect_core_receipt_file_sha256
         and core["core_receipt_sha256"] == args.expect_core_receipt_object_sha256
         and file_sha(cold_path) == args.expect_cold_receipt_file_sha256
         and cold["cold_replay_receipt_sha256"]
             == args.expect_cold_receipt_object_sha256
         and file_sha(evidence_path) == args.expect_evidence_file_sha256
         and evidence["evidence_bundle_sha256"]
             == args.expect_evidence_object_sha256
         and file_sha(attacks_path) == args.expect_release_attacks_file_sha256
         and attacks["release_attacks_sha256"]
             == args.expect_release_attacks_object_sha256
         and cold.get("formal_verification_byte_identical") is True
         and evidence.get("exact_census") == EXPECTED_MATH
         and attacks.get("attack_census")
             == {"required": 40, "rejected": 40, "accepted": 0},
         "core/cold/evidence/release chain")
    pinset = document(control / "pinset.json", "pinset_sha256")
    targets = {name: ROOT / raw for name, raw in pinset["targets"].items()}
    candidate = targets["candidate"]
    result_path = candidate / (PREFIX + "_result.json")
    result = document(result_path, "result_sha256")
    verification = document(targets["verification"], "verification_sha256")
    core_attacks = document(targets["attacks"], "attacks_sha256")
    need(result.get("schema") == RESULT_SCHEMA
         and result.get("recomputed_census") == EXPECTED_MATH
         and verification.get("schema") == VERIFY_SCHEMA
         and verification.get("independent_recomputed_census") == EXPECTED_MATH
         and verification.get("candidate_result_object_sha256")
             == result["result_sha256"]
         and verification.get("no_import_or_execution_of_producer") is True
         and core_attacks.get("attack_census")
             == {"required": 34, "rejected": 34, "accepted": 0}
         and core_attacks.get("post_rejection_private_case_cleanup", {}).get(
             "all_34_private_cases_removed") is True
         and core_attacks.get("post_rejection_private_case_cleanup", {}).get(
             "remaining_work_files_regular_single_link") is True
         and result.get("theorem", {}).get(
             "C25_fresh_component_id_used_only_as_historical_join_check") is True
         and verification.get("C25_historical_component_binding_only") is True,
         "independent mathematical chain")
    descriptors: dict[str, dict[str, Any]] = {}
    aggregate: dict[str, Any] = {}
    for role, (name, schema, count, order) in LEDGERS.items():
        descriptor, census = ledger(candidate / name, schema, count, order)
        need(descriptor == result["ledgers"][role], "ledger descriptor:" + role)
        descriptors[role] = descriptor
        if schema == COMPONENT_SCHEMA:
            aggregate = census
    need(aggregate == {"members": EXPECTED_MATH["members"],
        "representations": EXPECTED_MATH["representations"],
        "within": EXPECTED_MATH["within_post_component_member_pairs"],
        "incidences": EXPECTED_MATH["component_key_incidences"],
        "multiplicity": EXPECTED_MATH["component_key_multiplicity_census"]},
        "independent component aggregate")
    source = result["source_authority"]
    c27 = manifest_receipt["C27R2_terminal_pins"]
    c28 = manifest_receipt["C28_terminal_pins"]
    need(source["C27R2_terminal_root_manifest_sha256"] == c27["root"]
         and source["C27R2_terminal_receipt_file_sha256"] == c27["receipt_file"]
         and source["C27R2_terminal_receipt_object_sha256"] == c27["receipt_object"]
         and source["C27R2_terminal_replay_file_sha256"] == c27["replay_file"]
         and source["C27R2_terminal_replay_object_sha256"] == c27["replay_object"]
         and source["C28_v2_terminal_root_manifest_sha256"] == c28["root"]
         and source["C28_v2_terminal_receipt_file_sha256"] == c28["receipt_file"]
         and source["C28_v2_terminal_receipt_object_sha256"] == c28["receipt_object"]
         and source["C28_v2_terminal_replay_file_sha256"] == c28["replay_file"]
         and source["C28_v2_terminal_replay_object_sha256"] == c28["replay_object"],
         "dual predecessor source binding")
    required_payload = {str(path.relative_to(ROOT)) for path in (
        core_path, control / "PASS.lock", cold_path, cold_control / "PASS.lock",
        evidence_path, attacks_path, result_path, targets["verification"],
        targets["attacks"])}
    for _, (name, _, _, _) in LEDGERS.items():
        required_payload.add(str((candidate / name).relative_to(ROOT)))
    for terminal in (Path(pinset["C27R2_terminal"]["dir"]).absolute(),
                     Path(pinset["C28_terminal"]["dir"]).absolute()):
        for name in ("root_manifest.sha256", "terminal_receipt.json",
                     "terminal_replay.json", "PASS.lock"):
            required_payload.add(str((terminal / name).relative_to(ROOT)))
    need(required_payload <= set(payload), "required payload coverage")
    if args.preflight_only:
        return {"status": "PASS_C29_V2_INDEPENDENT_OUTER_AND_FRESH_OUTPUT_PREFLIGHT__NO_OUTPUT_ZERO_CREDIT"}
    body = {"schema": OUTER_SCHEMA, "status": OUTER_STATUS,
            "manifest_receipt_file_sha256": args.expect_manifest_receipt_file_sha256,
            "manifest_receipt_object_sha256": args.expect_manifest_receipt_object_sha256,
            "payload_manifest_sha256": args.expect_payload_manifest_sha256,
            "root_manifest_sha256": args.expect_root_manifest_sha256,
            "core_receipt_object_sha256": args.expect_core_receipt_object_sha256,
            "cold_replay_object_sha256": args.expect_cold_receipt_object_sha256,
            "evidence_bundle_object_sha256": args.expect_evidence_object_sha256,
            "release_attacks_object_sha256": args.expect_release_attacks_object_sha256,
            "candidate_result_object_sha256": result["result_sha256"],
            "independent_verification_object_sha256": verification["verification_sha256"],
            "ledger_descriptors": descriptors, "exact_census": EXPECTED_MATH,
            "dual_predecessor_terminal_pins": {"C27R2": c27, "C28": c28},
            "C25_fresh_component_id_historical_only": True,
            "all_three_ledgers_independently_replayed": True,
            "cold_replay_byte_identical": True,
            "core_attacks_rejected": 34, "release_attacks_rejected": 40,
            "outer_is_conditional_until_independent_terminal_byte_replay": True,
            "formal_credit": 0, "manifest_authorized": False,
            "C29": "UNAUTHORIZED_PENDING_TERMINAL_BYTE_REPLAY",
            "Source_W": "UNCHANGED_BY_SOURCE_G_C29_V2_OUTER",
            "D02": "BLOCKED_COMPOSITE", "D03": "UNAUTHORIZED",
            "D04": "NOT_MINTED", "Gate5": "10/18",
            "CM2": "NO-GO_FOR_CLAIM"}
    outer = dict(body)
    outer["outer_verification_sha256"] = digest(outer)
    write_once(output, canonical(outer) + b"\n")
    return outer


def self_test() -> dict[str, Any]:
    need(sum(EXPECTED_MATH["component_key_multiplicity_census"].values())
         == EXPECTED_MATH["post_C27R2_components"]
         and EXPECTED_MATH["total_unordered_member_pairs"]
             - EXPECTED_MATH["within_post_component_member_pairs"]
             == EXPECTED_MATH["cross_post_component_member_pairs"], "math fixture")
    return {"status": "PASS_C29_V2_RELEASE_OUTER_VERIFIER_SELF_TEST",
            "formal_credit": 0, "C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--preflight-only", action="store_true")
    for name in ("core-control-dir", "cold-control-dir", "evidence-dir",
                 "release-attacks-file", "manifest-dir", "output-file",
                 "expect-outer-sha256", "expect-manifest-receipt-file-sha256",
                 "expect-manifest-receipt-object-sha256",
                 "expect-payload-manifest-sha256", "expect-root-manifest-sha256",
                 "expect-core-receipt-file-sha256",
                 "expect-core-receipt-object-sha256",
                 "expect-cold-receipt-file-sha256",
                 "expect-cold-receipt-object-sha256",
                 "expect-evidence-file-sha256", "expect-evidence-object-sha256",
                 "expect-release-attacks-file-sha256",
                 "expect-release-attacks-object-sha256"):
        parser.add_argument("--" + name)
    args = parser.parse_args()
    fields = tuple(name.replace("-", "_") for name in (
        "core-control-dir", "cold-control-dir", "evidence-dir",
        "release-attacks-file", "manifest-dir", "output-file",
        "expect-outer-sha256", "expect-manifest-receipt-file-sha256",
        "expect-manifest-receipt-object-sha256", "expect-payload-manifest-sha256",
        "expect-root-manifest-sha256", "expect-core-receipt-file-sha256",
        "expect-core-receipt-object-sha256", "expect-cold-receipt-file-sha256",
        "expect-cold-receipt-object-sha256", "expect-evidence-file-sha256",
        "expect-evidence-object-sha256", "expect-release-attacks-file-sha256",
        "expect-release-attacks-object-sha256"))
    try:
        if args.self_test:
            need(not args.preflight_only
                 and all(getattr(args, field) is None for field in fields),
                 "self-test arguments")
            result = self_test()
        else:
            need(all(getattr(args, field) is not None for field in fields),
                 "run arguments")
            result = execute(args)
        sys.stdout.buffer.write(canonical({"CM2": "NO-GO_FOR_CLAIM",
            "formal_credit": 0, "status": result["status"]}) + b"\n")
        return 0
    except (Blocked, OSError, ValueError, KeyError, TypeError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
