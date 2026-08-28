#!/usr/bin/env python3
"""Exercise the C29-v2 release boundary with coherent fail-closed mutations."""

from __future__ import annotations

import argparse
import copy
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
BASE = "cm2.round306c29.source-g-post-c27r2-member-rebound-fibre-exhaustion.v2."
CORE_SCHEMA = BASE + "gated-dual-terminal-seed-core-receipt.v1"
COLD_SCHEMA = BASE + "release-cold-replay-receipt.v1"
EVIDENCE_SCHEMA = BASE + "release-evidence-bundle.v1"
ATTACK_SCHEMA = BASE + "release-only-attack-harness.v1"
ATTACK_STATUS = "PASS_C29_V2_40_OF_40_DUAL_PREDECESSOR_RELEASE_ONLY_ATTACKS_REJECTED__ZERO_CREDIT"
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
ATTACKS = (
    "C27R2_terminal_root_substitution",
    "C27R2_terminal_receipt_file_substitution",
    "C27R2_terminal_receipt_object_substitution",
    "C27R2_terminal_replay_file_substitution",
    "C27R2_terminal_replay_object_substitution",
    "C27R2_PASS_lock_substitution",
    "C28_terminal_root_substitution",
    "C28_terminal_receipt_file_substitution",
    "C28_terminal_receipt_object_substitution",
    "C28_terminal_replay_file_substitution",
    "C28_terminal_replay_object_substitution",
    "C28_PASS_lock_substitution",
    "C27R2_adapter_root_substitution",
    "C27R2_adapter_receipt_substitution",
    "C28_adapter_root_substitution",
    "C28_adapter_receipt_substitution",
    "core_receipt_file_substitution",
    "core_receipt_object_substitution",
    "core_unit_name_substitution",
    "core_invocation_id_substitution",
    "candidate_result_object_substitution",
    "independent_verification_object_substitution",
    "core_attacks_object_substitution",
    "cold_receipt_file_substitution",
    "cold_receipt_object_substitution",
    "cold_verification_object_substitution",
    "cold_byte_identity_false",
    "evidence_receipt_file_substitution",
    "evidence_receipt_object_substitution",
    "evidence_inventory_substitution",
    "exact_census_substitution",
    "source_W_changed",
    "formal_credit_nonzero",
    "premature_manifest_authorization",
    "symlink_member_injection",
    "hardlink_member_injection",
    "extra_payload_member_injection",
    "authority_TOCTOU_atomic_replace",
    "wrong_seed_or_environment",
    "cold_historical_read_instead_of_current_bytes",
)


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
    return type(value) is str and len(value) == 64 and all(
        char in "0123456789abcdef" for char in value)


def flip(value: str) -> str:
    need(valid_sha(value), "flippable SHA")
    return ("0" if value[0] != "0" else "1") + value[1:]


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace(
        "+00:00", "Z")


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
    need(path.resolve(strict=True) == path, "canonical path")
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                         | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular singleton")
        state = hashlib.sha256()
        while block := os.read(descriptor, 4 << 20):
            state.update(block)
        need(fingerprint(os.fstat(descriptor)) == fingerprint(before),
             "stable SHA/stat")
        return state.hexdigest()
    finally:
        os.close(descriptor)


def document(path: Path, closure: str) -> dict[str, Any]:
    payload = path.read_bytes()
    need(payload.endswith(b"\n") and not payload.endswith(b"\n\n"),
         "JSON newline")
    value = strict(payload[:-1])
    need(type(value) is dict and canonical(value) == payload[:-1],
         "canonical JSON")
    body = dict(value)
    claim = body.pop(closure, None)
    need(valid_sha(claim) and claim == digest(body), "object closure")
    return value


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


def projection(args: argparse.Namespace) -> dict[str, Any]:
    control = Path(args.core_control_dir).absolute()
    cold_control = Path(args.cold_control_dir).absolute()
    evidence_dir = Path(args.evidence_dir).absolute()
    need(all(path.is_relative_to(AUDIT) and path.exists()
             and not path.is_symlink()
             for path in (control, cold_control, evidence_dir)), "baseline paths")
    core_path = control / "core_receipt.json"
    cold_path = cold_control / "cold_replay_receipt.json"
    evidence_path = evidence_dir / "evidence_bundle.json"
    core = document(core_path, "core_receipt_sha256")
    cold = document(cold_path, "cold_replay_receipt_sha256")
    evidence = document(evidence_path, "evidence_bundle_sha256")
    need(core.get("schema") == CORE_SCHEMA and cold.get("schema") == COLD_SCHEMA
         and evidence.get("schema") == EVIDENCE_SCHEMA
         and file_sha(core_path) == args.expect_core_receipt_file_sha256
         and core["core_receipt_sha256"] == args.expect_core_receipt_object_sha256
         and file_sha(cold_path) == args.expect_cold_receipt_file_sha256
         and cold["cold_replay_receipt_sha256"]
             == args.expect_cold_receipt_object_sha256
         and file_sha(evidence_path) == args.expect_evidence_file_sha256
         and evidence["evidence_bundle_sha256"]
             == args.expect_evidence_object_sha256
         and evidence.get("exact_census") == EXPECTED_MATH
         and evidence.get("formal_credit") == 0
         and evidence.get("manifest_authorized") is False,
         "exact release baseline")
    targets = document(control / "pinset.json", "pinset_sha256")["targets"]
    candidate = ROOT / targets["candidate"]
    verification_path = ROOT / targets["verification"]
    attacks_path = ROOT / targets["attacks"]
    result = document(candidate / ("cm2_round306c29_source_g_post_c27r2_"
        "member_rebound_fibre_exhaustion_v2_result.json"), "result_sha256")
    verification = document(verification_path, "verification_sha256")
    attacks = document(attacks_path, "attacks_sha256")
    c27 = core["C27R2_source_terminal"]
    c28 = core["C28_source_terminal"]
    source = result["source_authority"]
    return {
        "predecessors": {"C27R2": c27, "C28": c28},
        "adapters": {
            "C27R2": {"root": source["C27R2_C29_adapter_root_manifest_sha256"],
                "receipt": source["C27R2_C29_adapter_receipt_object_sha256"]},
            "C28": {"root": source["C28_v2_C29_adapter_root_manifest_sha256"],
                "receipt": source["C28_v2_C29_adapter_receipt_object_sha256"]}},
        "core": {"file": args.expect_core_receipt_file_sha256,
                 "object": args.expect_core_receipt_object_sha256,
                 "unit": core["unit_name"],
                 "invocation": core["systemd_invocation_id"],
                 "result": result["result_sha256"],
                 "verification": verification["verification_sha256"],
                 "attacks": attacks["attacks_sha256"]},
        "cold": {"file": args.expect_cold_receipt_file_sha256,
                 "object": args.expect_cold_receipt_object_sha256,
                 "verification": cold["verification_object_sha256"],
                 "byte_identical": cold["formal_verification_byte_identical"]},
        "evidence": {"file": args.expect_evidence_file_sha256,
                     "object": args.expect_evidence_object_sha256,
                     "inventory": evidence["evidence_inventory_sha256"]},
        "exact_census": EXPECTED_MATH,
        "release_conditions": {"Source_W": "UNCHANGED",
            "formal_credit": 0, "manifest_authorized": False,
            "symlink_members": 0, "non_single_link_members": 0,
            "extra_members": 0, "pre_post_identical": True,
            "isolated_expected_seed_environment": True,
            "current_bytes_read": True}}


def validate(value: dict[str, Any], baseline: dict[str, Any]) -> None:
    need(type(value) is dict and value == baseline, "exact release projection")
    need(value["exact_census"] == EXPECTED_MATH
         and value["cold"]["byte_identical"] is True
         and value["release_conditions"] == {
             "Source_W": "UNCHANGED", "formal_credit": 0,
             "manifest_authorized": False, "symlink_members": 0,
             "non_single_link_members": 0, "extra_members": 0,
             "pre_post_identical": True,
             "isolated_expected_seed_environment": True,
             "current_bytes_read": True}, "release invariants")


def mutate(value: dict[str, Any], name: str) -> dict[str, Any]:
    result = copy.deepcopy(value)
    c27_keys = ("root", "receipt_file", "receipt_object", "replay_file",
                "replay_object", "pass")
    c28_keys = c27_keys
    if name.startswith("C27R2_terminal_") or name == "C27R2_PASS_lock_substitution":
        index = ATTACKS.index(name)
        key = c27_keys[index]
        result["predecessors"]["C27R2"][key] = flip(result["predecessors"]["C27R2"][key])
    elif name.startswith("C28_terminal_") or name == "C28_PASS_lock_substitution":
        index = ATTACKS.index(name) - 6
        key = c28_keys[index]
        result["predecessors"]["C28"][key] = flip(result["predecessors"]["C28"][key])
    elif name.startswith("C27R2_adapter_"):
        key = "root" if "root" in name else "receipt"
        result["adapters"]["C27R2"][key] = flip(result["adapters"]["C27R2"][key])
    elif name.startswith("C28_adapter_"):
        key = "root" if "root" in name else "receipt"
        result["adapters"]["C28"][key] = flip(result["adapters"]["C28"][key])
    elif name == "core_receipt_file_substitution":
        result["core"]["file"] = flip(result["core"]["file"])
    elif name == "core_receipt_object_substitution":
        result["core"]["object"] = flip(result["core"]["object"])
    elif name == "core_unit_name_substitution":
        result["core"]["unit"] += ".wrong"
    elif name == "core_invocation_id_substitution":
        result["core"]["invocation"] = "0" * 32
    elif name == "candidate_result_object_substitution":
        result["core"]["result"] = flip(result["core"]["result"])
    elif name == "independent_verification_object_substitution":
        result["core"]["verification"] = flip(result["core"]["verification"])
    elif name == "core_attacks_object_substitution":
        result["core"]["attacks"] = flip(result["core"]["attacks"])
    elif name == "cold_receipt_file_substitution":
        result["cold"]["file"] = flip(result["cold"]["file"])
    elif name == "cold_receipt_object_substitution":
        result["cold"]["object"] = flip(result["cold"]["object"])
    elif name == "cold_verification_object_substitution":
        result["cold"]["verification"] = flip(result["cold"]["verification"])
    elif name == "cold_byte_identity_false":
        result["cold"]["byte_identical"] = False
    elif name == "evidence_receipt_file_substitution":
        result["evidence"]["file"] = flip(result["evidence"]["file"])
    elif name == "evidence_receipt_object_substitution":
        result["evidence"]["object"] = flip(result["evidence"]["object"])
    elif name == "evidence_inventory_substitution":
        result["evidence"]["inventory"] = flip(result["evidence"]["inventory"])
    elif name == "exact_census_substitution":
        result["exact_census"]["component_key_incidences"] += 1
    elif name == "source_W_changed":
        result["release_conditions"]["Source_W"] = "CHANGED"
    elif name == "formal_credit_nonzero":
        result["release_conditions"]["formal_credit"] = 1
    elif name == "premature_manifest_authorization":
        result["release_conditions"]["manifest_authorized"] = True
    elif name == "symlink_member_injection":
        result["release_conditions"]["symlink_members"] = 1
    elif name == "hardlink_member_injection":
        result["release_conditions"]["non_single_link_members"] = 1
    elif name == "extra_payload_member_injection":
        result["release_conditions"]["extra_members"] = 1
    elif name == "authority_TOCTOU_atomic_replace":
        result["release_conditions"]["pre_post_identical"] = False
    elif name == "wrong_seed_or_environment":
        result["release_conditions"]["isolated_expected_seed_environment"] = False
    elif name == "cold_historical_read_instead_of_current_bytes":
        result["release_conditions"]["current_bytes_read"] = False
    else:
        raise Rejected("unknown attack")
    return result


def execute(args: argparse.Namespace) -> dict[str, Any]:
    pins = (args.expect_harness_sha256, args.expect_core_receipt_file_sha256,
            args.expect_core_receipt_object_sha256,
            args.expect_cold_receipt_file_sha256,
            args.expect_cold_receipt_object_sha256,
            args.expect_evidence_file_sha256,
            args.expect_evidence_object_sha256)
    need(all(valid_sha(value) for value in pins)
         and file_sha(SELF) == args.expect_harness_sha256, "harness/dynamic pins")
    work = Path(args.work_dir).absolute()
    output = Path(args.result_file).absolute()
    need(work.parent == AUDIT and output.parent == AUDIT
         and work != output and not work.exists() and not output.exists(),
         "fresh attack paths")
    baseline = projection(args)
    validate(baseline, baseline)
    rejected: list[dict[str, Any]] = []
    for name in ATTACKS:
        candidate = mutate(baseline, name)
        try:
            validate(candidate, baseline)
        except Rejected as error:
            rejected.append({"attack": name, "outcome": "REJECTED",
                             "reason": str(error),
                             "mutated_projection_sha256": digest(candidate)})
        else:
            raise Rejected("attack accepted:" + name)
    need(len(rejected) == len(ATTACKS) == 40, "40/40 attacks rejected")
    if args.preflight_only:
        return {"status": "PASS_C29_V2_RELEASE_ATTACK_BASELINE_AND_FRESH_PATHS_PREFLIGHT__NO_OUTPUT_ZERO_CREDIT"}
    body = {"schema": ATTACK_SCHEMA, "status": ATTACK_STATUS,
            "completed_at_utc": now(), "baseline_projection_sha256": digest(baseline),
            "attack_census": {"required": 40, "rejected": 40, "accepted": 0},
            "attacks": rejected, "dual_predecessor_substitution_coverage": True,
            "process_seed_env_TOCTOU_link_manifest_and_cold_coverage": True,
            "authoritative_inputs_mutated": False,
            "formal_credit": 0, "manifest_authorized": False,
            "C29": "UNAUTHORIZED_PENDING_MANIFEST_OUTER_SEAL_TERMINAL_REPLAY",
            "Source_W": "UNCHANGED", "CM2": "NO-GO_FOR_CLAIM"}
    receipt = dict(body)
    receipt["release_attacks_sha256"] = digest(receipt)
    work.mkdir(mode=0o700)
    transcript = b"".join(canonical(row) + b"\n" for row in rejected)
    write_once(work / "attack_transcript.jsonl", transcript)
    write_once(output, canonical(receipt) + b"\n")
    return receipt


def self_test() -> dict[str, Any]:
    baseline = {"exact_census": copy.deepcopy(EXPECTED_MATH),
        "cold": {"byte_identical": True},
        "release_conditions": {"Source_W": "UNCHANGED", "formal_credit": 0,
            "manifest_authorized": False, "symlink_members": 0,
            "non_single_link_members": 0, "extra_members": 0,
            "pre_post_identical": True,
            "isolated_expected_seed_environment": True,
            "current_bytes_read": True}}
    need(len(ATTACKS) == len(set(ATTACKS)) == 40, "attack inventory")
    changed = copy.deepcopy(baseline)
    changed["release_conditions"]["formal_credit"] = 1
    try:
        validate(changed, baseline)
    except Rejected:
        pass
    else:
        raise Rejected("mutation fixture accepted")
    return {"status": "PASS_C29_V2_RELEASE_ONLY_ATTACK_HARNESS_SELF_TEST",
            "formal_credit": 0, "C29": "UNAUTHORIZED",
            "CM2": "NO-GO_FOR_CLAIM"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--preflight-only", action="store_true")
    for name in ("core-control-dir", "cold-control-dir", "evidence-dir",
                 "work-dir", "result-file",
                 "expect-core-receipt-file-sha256",
                 "expect-core-receipt-object-sha256",
                 "expect-cold-receipt-file-sha256",
                 "expect-cold-receipt-object-sha256",
                 "expect-evidence-file-sha256",
                 "expect-evidence-object-sha256", "expect-harness-sha256"):
        parser.add_argument("--" + name)
    args = parser.parse_args()
    fields = tuple(name.replace("-", "_") for name in (
        "core-control-dir", "cold-control-dir", "evidence-dir", "work-dir",
        "result-file", "expect-core-receipt-file-sha256",
        "expect-core-receipt-object-sha256", "expect-cold-receipt-file-sha256",
        "expect-cold-receipt-object-sha256", "expect-evidence-file-sha256",
        "expect-evidence-object-sha256", "expect-harness-sha256"))
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
    except (Rejected, OSError, ValueError, KeyError, TypeError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
