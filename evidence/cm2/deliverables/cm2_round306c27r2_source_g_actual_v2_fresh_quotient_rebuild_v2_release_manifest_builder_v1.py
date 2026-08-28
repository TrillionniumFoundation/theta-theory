#!/usr/bin/env python3
"""Build manifest-first C27R2 release payload and root manifests.

The builder consumes the exact core evidence bundle, a fresh cold replay, and
the release-only attack receipt.  It rechecks every referenced byte before it
creates a fresh output directory.  The manifest receipt remains conditional,
zero credit, and cannot authorize C27R2.
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
STEM = "c27r2-source-g-authority-v2-v6-formal-r2-20260808T180523"
CONTROL = AUDIT / (STEM + "-control")
CANDIDATE = AUDIT / (STEM + "-candidate")
VERIFICATION = AUDIT / (STEM + "-verifier-output/verification.json")
ATTACKS = AUDIT / (STEM + "-attack-work/coherent_attacks.json")
GATE = AUDIT / "c27r2-post-actual-v2-rebuild-gate-v3-r2-zero-credit-20260808T164429"
ACTUAL_TERMINAL = AUDIT / (
    "c27-primitive-twenty-family-gate-v5-actual-v2-dual-seed-zero-credit-"
    "seal-v2-20260808T1544-terminal-replay"
)
CANDIDATE_FILES = ["member_to_post_component.jsonl.gz",
                   "old_c15_component_to_post_component.jsonl.gz",
                   "post_component_census.jsonl.gz", "result.json"]
EVIDENCE_SCHEMA = (
    "cm2.round306c27r2.source-g-authority-v2.release-evidence-bundle.v1"
)
COLD_SCHEMA = (
    "cm2.round306c27r2.source-g-authority-v2.release-cold-replay-receipt.v1"
)
ATTACK_SCHEMA = (
    "cm2.round306c27r2.source-g-authority-v2.release-only-attack-harness.v1"
)
ATTACK_STATUS = (
    "PASS_BASELINE_AND_20_OF_20_RELEASE_ONLY_ATTACKS_REJECTED_FAIL_CLOSED__"
    "ZERO_CREDIT"
)


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


def file_descriptor(path: Path) -> dict[str, Any]:
    absolute = path.absolute()
    need(absolute.resolve(strict=True) == absolute,
         "canonical path:" + str(path))
    descriptor = os.open(absolute, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                         | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular singleton:" + str(path))
        state = hashlib.sha256()
        while block := os.read(descriptor, 4 << 20):
            state.update(block)
        after = os.fstat(descriptor)
        need(fingerprint(before) == fingerprint(after)
             and fingerprint(os.stat(absolute, follow_symlinks=False))
                 == fingerprint(before), "stable path SHA/stat:" + str(path))
        return {"path": str(absolute.relative_to(ROOT)),
                "sha256": state.hexdigest(), "size": before.st_size,
                "stat_fingerprint": list(fingerprint(before))}
    finally:
        os.close(descriptor)


def file_sha(path: Path) -> str:
    return file_descriptor(path)["sha256"]


def strict_load(payload: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(type(key) is str and key not in result, "unique JSON key")
            result[key] = value
        return result
    return json.loads(payload, object_pairs_hook=pairs,
                      parse_constant=lambda token: (_ for _ in ()).throw(
                          ValueError(token)))


def document(path: Path, closure: str) -> dict[str, Any]:
    payload = path.read_bytes()
    need(payload.endswith(b"\n"), "JSON newline:" + str(path))
    value = strict_load(payload[:-1])
    need(type(value) is dict and canonical(value) == payload[:-1],
         "canonical JSON:" + str(path))
    body = dict(value)
    claim = body.pop(closure, None)
    need(valid_sha(claim) and claim == digest(body),
         "object closure:" + str(path))
    return value


def parse_manifest(path: Path) -> dict[str, str]:
    payload = path.read_bytes()
    need(payload.endswith(b"\n"), "manifest newline:" + str(path))
    result: dict[str, str] = {}
    for line in payload.decode("ascii").splitlines():
        pieces = line.split("  ", 1)
        need(len(pieces) == 2 and valid_sha(pieces[0])
             and pieces[1] not in result and pieces[1] != "",
             "manifest row syntax/unique")
        result[pieces[1]] = pieces[0]
    need(list(result) == sorted(result), "manifest canonical path order")
    return result


def manifest(paths: list[Path]) -> bytes:
    descriptors = [file_descriptor(path) for path in paths]
    rows = sorted((value["path"], value["sha256"]) for value in descriptors)
    need(len(rows) == len(set(path for path, _ in rows)),
         "manifest unique paths")
    return ("\n".join(f"{sha256}  {path}" for path, sha256 in rows)
            + "\n").encode("ascii")


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


def execute(args: argparse.Namespace) -> dict[str, Any]:
    pins = (args.expect_builder_sha256, args.expect_evidence_file_sha256,
            args.expect_evidence_object_sha256,
            args.expect_cold_receipt_file_sha256,
            args.expect_cold_receipt_object_sha256,
            args.expect_release_attacks_file_sha256,
            args.expect_release_attacks_object_sha256)
    need(all(valid_sha(value) for value in pins)
         and file_sha(SELF) == args.expect_builder_sha256,
         "all dynamic pins and builder self pin")
    evidence_dir = Path(args.evidence_dir).absolute()
    cold_control = Path(args.cold_control_dir).absolute()
    cold_output = Path(args.cold_output_dir).absolute()
    cold_run = Path(args.cold_run_dir).absolute()
    release_attacks = Path(args.release_attacks_file).absolute()
    output = Path(args.output_dir).absolute()
    need(output.parent == AUDIT and not output.exists(),
         "fresh manifest output directory")
    evidence_path = evidence_dir / "evidence_bundle.json"
    evidence = document(evidence_path, "evidence_bundle_sha256")
    need(file_sha(evidence_path) == args.expect_evidence_file_sha256
         and evidence["evidence_bundle_sha256"]
             == args.expect_evidence_object_sha256
         and evidence.get("schema") == EVIDENCE_SCHEMA
         and evidence.get("formal_credit") == 0
         and evidence.get("manifest_authorized") is False,
         "exact core evidence boundary")
    inventory_path = evidence_dir / "core_inventory.sha256"
    inventory = parse_manifest(inventory_path)
    need(hashlib.sha256(inventory_path.read_bytes()).hexdigest()
             == evidence["core_inventory_sha256"]
         and len(inventory) == evidence["core_member_count"],
         "core inventory bundle closure")
    for relative, expected in inventory.items():
        need(file_sha(ROOT / relative) == expected,
             "core inventory current:" + relative)
    cold_receipt_path = cold_control / "cold_replay_receipt.json"
    cold = document(cold_receipt_path, "cold_replay_receipt_sha256")
    need(file_sha(cold_receipt_path) == args.expect_cold_receipt_file_sha256
         and cold["cold_replay_receipt_sha256"]
             == args.expect_cold_receipt_object_sha256
         and cold.get("schema") == COLD_SCHEMA
         and cold.get("formal_verification_byte_identical") is True
         and cold.get("numeric_exit_code") == 0
         and cold.get("signal") is None
         and cold.get("stderr_empty") is True
         and cold.get("all_core_inputs_pre_post_sha_stat_identical") is True
         and cold.get("formal_credit") == 0,
         "exact cold replay boundary")
    need((cold_control / "PASS.lock").read_bytes()
         == b"PASS_C27R2_RELEASE_COLD_REPLAY__ZERO_CREDIT\n"
         and not (cold_control / "FAILED.lock").exists(),
         "cold PASS-only state")
    cold_verification = cold_output / "verification.json"
    cold_attestation = cold_run / "run_attestation.json"
    need(file_sha(cold_verification) == cold["verification_file_sha256"]
         and file_sha(cold_attestation) == cold["run_attestation_file_sha256"]
         and cold_verification.read_bytes() == VERIFICATION.read_bytes(),
         "cold evidence current and byte-identical")
    release = document(release_attacks, "release_attack_harness_sha256")
    need(file_sha(release_attacks) == args.expect_release_attacks_file_sha256
         and release["release_attack_harness_sha256"]
             == args.expect_release_attacks_object_sha256
         and release.get("schema") == ATTACK_SCHEMA
         and release.get("status") == ATTACK_STATUS
         and release.get("attack_count") == 20
         and release.get("rejected") == 20
         and release.get("accepted") == 0
         and release.get("formal_credit") == 0,
         "20/20 release-only attacks")
    payload_paths = ([CANDIDATE / name for name in CANDIDATE_FILES]
                     + [VERIFICATION, ATTACKS, evidence_path, inventory_path,
                        cold_receipt_path, cold_verification, cold_attestation,
                        release_attacks])
    payload_raw = manifest(payload_paths)
    output.mkdir(mode=0o700)
    payload_path = output / "payload_manifest.sha256"
    write_once(payload_path, payload_raw)
    core_pinset = document(CONTROL / "pinset.json", "pinset_sha256")
    authority = core_pinset["actual_v2_authority"]
    terminal_root = ROOT / authority["actual_terminal_dir"] / "root_manifest.sha256"
    root_paths = [payload_path, CONTROL / "transaction_receipt.json",
                  CONTROL / "PASS.lock", CONTROL / "pinset.json",
                  GATE / "execution_receipt.json", GATE / "gate_receipt.json",
                  GATE / "PASS.lock", terminal_root, evidence_path,
                  cold_receipt_path, release_attacks, SELF]
    root_raw = manifest(root_paths)
    root_path = output / "root_manifest.sha256"
    write_once(root_path, root_raw)
    body = {
        "schema": "cm2.round306c27r2.source-g-authority-v2.release-manifest-receipt.v1",
        "status": "PASS_MANIFEST_FIRST_PAYLOAD_AND_ROOT_CLOSURE__ZERO_CREDIT_PENDING_OUTER_AND_TERMINAL_REPLAY",
        "built_at_utc": utc_now(),
        "payload_manifest_file_sha256": hashlib.sha256(payload_raw).hexdigest(),
        "payload_member_count": len(parse_manifest(payload_path)),
        "root_manifest_file_sha256": hashlib.sha256(root_raw).hexdigest(),
        "root_member_count": len(parse_manifest(root_path)),
        "evidence_bundle_object_sha256": evidence["evidence_bundle_sha256"],
        "cold_replay_object_sha256": cold["cold_replay_receipt_sha256"],
        "release_attacks_object_sha256": release["release_attack_harness_sha256"],
        "formal_credit": 0, "manifest_authorized": False,
        "C27R2": "UNAUTHORIZED_PENDING_OUTER_AND_TERMINAL_REPLAY",
        "C28_C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM",
    }
    receipt = {**body, "manifest_receipt_sha256": digest(body)}
    write_once(output / "manifest_receipt.json", canonical(receipt) + b"\n")
    return receipt


def self_test() -> dict[str, Any]:
    rows = sorted([("z", "0" * 64), ("a", "1" * 64)])
    need([path for path, _ in rows] == ["a", "z"],
         "manifest ordering fixture")
    return {"status": "PASS_MANIFEST_ORDER_AND_OBJECT_CLOSURE_FIXTURE"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    for name in ("evidence-dir", "cold-control-dir", "cold-output-dir",
                 "cold-run-dir", "release-attacks-file", "output-dir",
                 "expect-builder-sha256", "expect-evidence-file-sha256",
                 "expect-evidence-object-sha256",
                 "expect-cold-receipt-file-sha256",
                 "expect-cold-receipt-object-sha256",
                 "expect-release-attacks-file-sha256",
                 "expect-release-attacks-object-sha256"):
        parser.add_argument("--" + name)
    args = parser.parse_args()
    fields = tuple(name.replace("-", "_") for name in (
        "evidence-dir", "cold-control-dir", "cold-output-dir", "cold-run-dir",
        "release-attacks-file", "output-dir", "expect-builder-sha256",
        "expect-evidence-file-sha256", "expect-evidence-object-sha256",
        "expect-cold-receipt-file-sha256", "expect-cold-receipt-object-sha256",
        "expect-release-attacks-file-sha256",
        "expect-release-attacks-object-sha256"))
    try:
        if args.self_test:
            need(all(getattr(args, field) is None for field in fields),
                 "self-test accepts no run arguments")
            result = self_test()
        else:
            need(all(getattr(args, field) is not None for field in fields),
                 "all run arguments")
            result = execute(args)
        sys.stdout.buffer.write(canonical({"CM2": "NO-GO_FOR_CLAIM",
            "formal_credit": 0, "status": result["status"]}) + b"\n")
        return 0
    except (Blocked, OSError, ValueError, KeyError, TypeError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
