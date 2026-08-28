#!/usr/bin/env python3
"""Build the manifest-first, still-unauthorized C28-v2 release package.

The builder consumes one selected dual-seed candidate, the independent core
verification, cold replay, 32/32 release-only attacks, and the O_NOFOLLOW
evidence bundle.  It also binds the one minted C27R2 predecessor terminal.
Preflight validates every available byte but creates no path.  This source
cannot build a seal, replay terminal bytes, authorize C28, or start C29.
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
PREFIX = (
    "cm2.round306c28.source-g-post-c27r2-125561998198-pair-routing.v2."
)
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
ATTACK_SCHEMA = PREFIX + "release-only-attack-harness.v1"
ATTACK_STATUS = (
    "PASS_BASELINE_AND_32_OF_32_RELEASE_ONLY_ATTACKS_REJECTED_FAIL_"
    "CLOSED__ZERO_CREDIT_PENDING_EVIDENCE_MANIFEST_OUTER_AND_TERMINAL"
)
EVIDENCE_SCHEMA = PREFIX + "release-evidence-bundle.v1"
EVIDENCE_STATUS = (
    "PASS_C28_CORE_COLD_32_RELEASE_ATTACKS_AND_ALL_AUTHORITY_INPUT_"
    "SHA_STAT_EVIDENCE__ZERO_CREDIT"
)
VERIFICATION_SCHEMA = PREFIX + "independent-verification.v1"
RESULT_SCHEMA = PREFIX + "producer-result.v1"
RESULT_STATUS = (
    "PASS_POST_C27R2_PARTITION_502204_MEMBERS_43684_COMPONENTS_AND_"
    "32896_PAIR_SHARDS_REBUILT__125561998198_EXACT_NONEDGE_CANDIDATE_"
    "ZERO_CREDIT__C28_UNAUTHORIZED_PENDING_RELEASE_TERMINAL"
)
MANIFEST_SCHEMA = PREFIX + "release-manifest-receipt.v1"
MANIFEST_STATUS = (
    "PASS_C28_MANIFEST_FIRST_PAYLOAD_AND_C27R2_ROOT_CLOSURE__ZERO_"
    "CREDIT_PENDING_OUTER_SEAL_AND_TERMINAL_REPLAY"
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


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace(
        "+00:00", "Z")


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns,
            value.st_uid, value.st_gid)


def file_descriptor(path: Path) -> dict[str, Any]:
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
        need(fingerprint(before) == fingerprint(os.fstat(fd))
             == fingerprint(os.stat(absolute, follow_symlinks=False)),
             "stable fd/path SHA/stat:" + str(path))
        return {"path": str(absolute.relative_to(ROOT)),
                "sha256": state.hexdigest(), "size": before.st_size,
                "stat_fingerprint": list(fingerprint(before))}
    finally:
        os.close(fd)


def file_sha(path: Path) -> str:
    return file_descriptor(path)["sha256"]


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


def parse_manifest(path: Path, *, verify: bool = True) -> dict[str, str]:
    payload = path.read_bytes()
    need(payload.endswith(b"\n") and payload != b"\n",
         "manifest newline/nonempty:" + str(path))
    result: dict[str, str] = {}
    for line in payload.decode("ascii").splitlines():
        fields = line.split("  ", 1)
        need(len(fields) == 2 and valid_sha(fields[0])
             and fields[1] not in result and fields[1] != "",
             "manifest row syntax/unique")
        relative = Path(fields[1])
        need(not relative.is_absolute()
             and all(part not in {"", ".", ".."} for part in relative.parts)
             and str(relative) == fields[1], "canonical manifest path")
        result[fields[1]] = fields[0]
    need(list(result) == sorted(result), "manifest path order")
    if verify:
        for relative, expected in result.items():
            need(file_sha(ROOT / relative) == expected,
                 "manifest current member:" + relative)
    return result


def manifest(paths: set[Path]) -> bytes:
    rows = sorted((file_descriptor(path)["path"], file_sha(path))
                  for path in paths)
    need(rows and len(rows) == len({path for path, _ in rows}),
         "nonempty unique manifest paths")
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


def audit_dir(raw: str) -> Path:
    path = Path(raw).absolute()
    need(path.parent == AUDIT and path.is_dir() and not path.is_symlink(),
         "existing direct audit directory:" + str(path))
    return path


def validate_predecessor(path: Path) -> None:
    need(path.parent == AUDIT and path.is_dir() and not path.is_symlink()
         and {entry.name for entry in path.iterdir()} == {
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
         "immutable C27R2 terminal pins/semantics")
    parse_manifest(path / "payload_manifest.sha256")
    parse_manifest(path / "root_manifest.sha256")


def execute(args: argparse.Namespace) -> dict[str, Any]:
    pins = (
        args.expect_builder_sha256, args.expect_core_receipt_file_sha256,
        args.expect_core_receipt_object_sha256, args.expect_core_pass_sha256,
        args.expect_cold_receipt_file_sha256,
        args.expect_cold_receipt_object_sha256,
        args.expect_release_attack_file_sha256,
        args.expect_release_attack_object_sha256,
        args.expect_evidence_file_sha256, args.expect_evidence_object_sha256,
    )
    need(all(valid_sha(value) for value in pins)
         and file_sha(SELF) == args.expect_builder_sha256,
         "manifest builder self/all dynamic pins")
    control = audit_dir(args.core_control_dir)
    predecessor = audit_dir(args.predecessor_terminal_dir)
    adapter = audit_dir(args.adapter_dir)
    candidate = audit_dir(args.candidate_dir)
    cold_control = audit_dir(args.cold_control_dir)
    cold_output = audit_dir(args.cold_output_dir)
    cold_run = audit_dir(args.cold_run_dir)
    release_dir = audit_dir(args.release_attack_dir)
    evidence_dir = audit_dir(args.evidence_dir)
    formal = Path(args.formal_verification_file).absolute()
    core_attacks = Path(args.core_attacks_file).absolute()
    output = Path(args.output_dir).absolute()
    need(output.parent == AUDIT and not output.exists()
         and not output.is_symlink(), "fresh manifest output")
    need({entry.name for entry in candidate.iterdir()} == CANDIDATE_FILES,
         "exact selected candidate inventory")
    validate_predecessor(predecessor)
    core_path = control / "core_receipt.json"
    core = document(core_path, "core_receipt_sha256")
    need(file_sha(core_path) == args.expect_core_receipt_file_sha256
         and core["core_receipt_sha256"]
             == args.expect_core_receipt_object_sha256
         and core.get("schema") == CORE_SCHEMA
         and core.get("status") == CORE_STATUS
         and core.get("exact_math") == EXPECTED
         and core.get("formal_credit") == 0
         and core.get("manifest_authorized") is False
         and core.get("C28") == "UNAUTHORIZED_PENDING_RELEASE_TERMINAL"
         and core.get("C29") == "UNAUTHORIZED"
         and core.get("CM2") == "NO-GO_FOR_CLAIM"
         and file_sha(control / "PASS.lock") == args.expect_core_pass_sha256,
         "exact terminal-pending core boundary")
    predecessor_pins = core.get("predecessor_terminal_pins", {})
    need(predecessor_pins.get("terminal_root_sha256") == C27["root"]
         and predecessor_pins.get("terminal_receipt_file_sha256")
             == C27["receipt_file"]
         and predecessor_pins.get("terminal_receipt_object_sha256")
             == C27["receipt_object"]
         and predecessor_pins.get("terminal_replay_file_sha256")
             == C27["replay_file"]
         and predecessor_pins.get("terminal_replay_object_sha256")
             == C27["replay_object"]
         and predecessor_pins.get("terminal_pass_lock_sha256") == C27["pass"],
         "core binds the one minted C27R2 terminal")
    result_path = candidate / "result.json"
    result = document(result_path, "result_sha256")
    verification = document(formal, "verification_sha256")
    need(result.get("schema") == RESULT_SCHEMA
         and result.get("status") == RESULT_STATUS
         and verification.get("schema") == VERIFICATION_SCHEMA
         and verification.get("candidate_result_sha256")
             == result["result_sha256"]
         and verification.get("verified_census") == EXPECTED
         and verification.get("independence", {}).get("producer_imported")
             is False
         and verification.get("independence", {}).get("producer_executed")
             is False, "selected candidate/no-import verification")
    cold_path = cold_control / "cold_replay_receipt.json"
    cold = document(cold_path, "cold_replay_receipt_sha256")
    release_path = release_dir / "release_attacks.json"
    release = document(release_path, "release_attack_receipt_sha256")
    evidence_path = evidence_dir / "evidence_bundle.json"
    evidence = document(evidence_path, "evidence_bundle_sha256")
    need(file_sha(cold_path) == args.expect_cold_receipt_file_sha256
         and cold["cold_replay_receipt_sha256"]
             == args.expect_cold_receipt_object_sha256
         and cold.get("schema") == COLD_SCHEMA and cold.get("status") == COLD_STATUS
         and cold.get("cold_replay_byte_identical") is True
         and file_sha(release_path) == args.expect_release_attack_file_sha256
         and release["release_attack_receipt_sha256"]
             == args.expect_release_attack_object_sha256
         and release.get("schema") == ATTACK_SCHEMA
         and release.get("status") == ATTACK_STATUS
         and release.get("attack_census") == {
             "planned": 32, "executed": 32,
             "rejected_fail_closed": 32, "accepted": 0}
         and file_sha(evidence_path) == args.expect_evidence_file_sha256
         and evidence["evidence_bundle_sha256"]
             == args.expect_evidence_object_sha256
         and evidence.get("schema") == EVIDENCE_SCHEMA
         and evidence.get("status") == EVIDENCE_STATUS
         and all(item.get("formal_credit") == 0
                 and item.get("manifest_authorized") is False
                 for item in (cold, release, evidence)),
         "cold/release/evidence zero-credit chain")
    inventory_path = evidence_dir / "authority_inventory.sha256"
    inventory = parse_manifest(inventory_path)
    need(hashlib.sha256(inventory_path.read_bytes()).hexdigest()
             == evidence.get("authority_inventory_sha256")
         and len(inventory) == evidence.get("authority_member_count"),
         "evidence inventory closure/current bytes")
    payload_paths = {
        *(candidate / name for name in CANDIDATE_FILES), formal, core_attacks,
        core_path, control / "PASS.lock", control / "pinset.json",
        cold_path, cold_control / "PASS.lock",
        cold_output / "verification.json", cold_run / "run_attestation.json",
        release_path, release_dir / "PASS.lock", evidence_path, inventory_path,
        adapter / "authority_contract.json", adapter / "root_manifest.sha256",
        adapter / "terminal_receipt.json", adapter / "PASS.lock",
        predecessor / "root_manifest.sha256",
        predecessor / "terminal_receipt.json",
        predecessor / "terminal_replay.json", predecessor / "chain_status.json",
        predecessor / "PASS.lock", SELF,
    }
    payload_raw = manifest(payload_paths)
    if args.preflight_only:
        return {"status":
                "PASS_C28_RELEASE_CHAIN_AND_FRESH_MANIFEST_PREFLIGHT__NO_"
                "OUTPUT_CREATED_ZERO_CREDIT"}
    output.mkdir(mode=0o700)
    payload_path = output / "payload_manifest.sha256"
    write_once(payload_path, payload_raw)
    root_paths = {
        payload_path, core_path, control / "PASS.lock", control / "pinset.json",
        evidence_path, cold_path, release_path,
        predecessor / "root_manifest.sha256",
        predecessor / "terminal_receipt.json",
        predecessor / "terminal_replay.json", predecessor / "PASS.lock", SELF,
    }
    root_raw = manifest(root_paths)
    root_path = output / "root_manifest.sha256"
    write_once(root_path, root_raw)
    body = {
        "schema": MANIFEST_SCHEMA, "status": MANIFEST_STATUS,
        "built_at_utc": now(),
        "payload_manifest_file_sha256": file_sha(payload_path),
        "payload_member_count": len(parse_manifest(payload_path)),
        "root_manifest_file_sha256": file_sha(root_path),
        "root_member_count": len(parse_manifest(root_path)),
        "core_receipt_file_sha256": args.expect_core_receipt_file_sha256,
        "core_receipt_object_sha256": args.expect_core_receipt_object_sha256,
        "cold_replay_receipt_file_sha256": args.expect_cold_receipt_file_sha256,
        "cold_replay_receipt_object_sha256": args.expect_cold_receipt_object_sha256,
        "release_attack_file_sha256": args.expect_release_attack_file_sha256,
        "release_attack_object_sha256": args.expect_release_attack_object_sha256,
        "evidence_bundle_file_sha256": args.expect_evidence_file_sha256,
        "evidence_bundle_object_sha256": args.expect_evidence_object_sha256,
        "selected_candidate_result_object_sha256": result["result_sha256"],
        "C27R2_terminal_pins": dict(C27),
        "C27R2_terminal_root_manifest_sha256": C27["root"],
        "exact_math": EXPECTED, "predecessor_root_closure": True,
        "formal_credit": 0, "manifest_authorized": False,
        "C27R2": "AUTHORIZED_PREDECESSOR_ONLY",
        "C28": "UNAUTHORIZED_PENDING_INDEPENDENT_OUTER_SEAL_AND_TERMINAL_REPLAY",
        "C29": "UNAUTHORIZED", "Source_W": "UNCHANGED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    receipt = {**body, "manifest_receipt_sha256": digest(body)}
    write_once(output / "manifest_receipt.json", canonical(receipt) + b"\n")
    return receipt


def self_test() -> dict[str, Any]:
    need(all(valid_sha(value) for value in C27.values())
         and EXPECTED["total_pairs"]
             == EXPECTED["within_pairs"] + EXPECTED["cross_pairs"],
         "fixed predecessor/math fixtures")
    return {"status": "PASS_C28_RELEASE_MANIFEST_BUILDER_SELF_TEST",
            "formal_credit": 0, "C28": "UNAUTHORIZED",
            "CM2": "NO-GO_FOR_CLAIM"}


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--self-test", action="store_true")
    value.add_argument("--preflight-only", action="store_true")
    for name in (
        "core-control-dir", "predecessor-terminal-dir", "adapter-dir",
        "candidate-dir", "formal-verification-file", "core-attacks-file",
        "cold-control-dir", "cold-output-dir", "cold-run-dir",
        "release-attack-dir", "evidence-dir", "output-dir",
        "expect-builder-sha256", "expect-core-receipt-file-sha256",
        "expect-core-receipt-object-sha256", "expect-core-pass-sha256",
        "expect-cold-receipt-file-sha256",
        "expect-cold-receipt-object-sha256",
        "expect-release-attack-file-sha256",
        "expect-release-attack-object-sha256",
        "expect-evidence-file-sha256", "expect-evidence-object-sha256",
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
                 "all run arguments")
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
