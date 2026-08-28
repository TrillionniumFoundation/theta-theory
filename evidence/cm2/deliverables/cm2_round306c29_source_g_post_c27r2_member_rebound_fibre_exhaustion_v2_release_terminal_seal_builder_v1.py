#!/usr/bin/env python3
"""Build a conditional C29-v2 seal candidate; never mint authority here."""

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
BASE = "cm2.round306c29.source-g-post-c27r2-member-rebound-fibre-exhaustion.v2."
MANIFEST_SCHEMA = BASE + "release-manifest-receipt.v1"
OUTER_SCHEMA = BASE + "release-outer-verification.v1"
OUTER_STATUS = "PASS_INDEPENDENT_C29_V2_FULL_LEDGER_DUAL_PREDECESSOR_MANIFEST_COLD_AND_40_RELEASE_ATTACK_CHECK__CONDITIONAL_ZERO_CREDIT"
SEAL_SCHEMA = BASE + "release-terminal-seal-candidate.v1"
SEAL_STATUS = "PASS_CONDITIONAL_C29_V2_TERMINAL_SEAL_CANDIDATE__ZERO_CREDIT_PENDING_INDEPENDENT_BYTE_REPLAY"
TERMINAL_STATUS = "PASS_C29_V2_TERMINAL_BYTE_REPLAY__FORMAL_SOURCE_G_FIBRE_AUTHORITY_MINTED"
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


def parse_manifest(path: Path) -> dict[str, str]:
    payload = path.read_bytes()
    need(payload.endswith(b"\n"), "manifest newline")
    result: dict[str, str] = {}
    for line in payload.decode("ascii").splitlines():
        fields = line.split("  ", 1)
        need(len(fields) == 2 and valid_sha(fields[0])
             and fields[1] not in result, "manifest row")
        result[fields[1]] = fields[0]
    need(list(result) == sorted(result)
         and all(file_sha(ROOT / path) == sha for path, sha in result.items()),
         "manifest sorted/current")
    return result


def manifest(paths: set[Path]) -> bytes:
    rows = sorted((str(path.absolute().relative_to(ROOT)), file_sha(path))
                  for path in paths)
    need(len(rows) == len({path for path, _ in rows}), "manifest unique")
    return ("\n".join(f"{sha}  {path}" for path, sha in rows) + "\n").encode("ascii")


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
    pins = (args.expect_builder_sha256, args.expect_outer_file_sha256,
            args.expect_outer_object_sha256,
            args.expect_manifest_receipt_file_sha256,
            args.expect_manifest_receipt_object_sha256,
            args.expect_payload_manifest_sha256,
            args.expect_root_manifest_sha256)
    need(all(valid_sha(value) for value in pins)
         and file_sha(SELF) == args.expect_builder_sha256, "all seal/dynamic pins")
    manifest_dir = Path(args.manifest_dir).absolute()
    outer_path = Path(args.outer_file).absolute()
    output = Path(args.output_dir).absolute()
    need(output.parent == AUDIT and not output.exists(), "fresh seal output")
    receipt_path = manifest_dir / "manifest_receipt.json"
    payload_path = manifest_dir / "payload_manifest.sha256"
    root_path = manifest_dir / "root_manifest.sha256"
    manifest_receipt = document(receipt_path, "manifest_receipt_sha256")
    outer = document(outer_path, "outer_verification_sha256")
    need(file_sha(receipt_path) == args.expect_manifest_receipt_file_sha256
         and manifest_receipt["manifest_receipt_sha256"]
             == args.expect_manifest_receipt_object_sha256
         and manifest_receipt.get("schema") == MANIFEST_SCHEMA
         and file_sha(payload_path) == args.expect_payload_manifest_sha256
         and file_sha(root_path) == args.expect_root_manifest_sha256
         and file_sha(outer_path) == args.expect_outer_file_sha256
         and outer["outer_verification_sha256"] == args.expect_outer_object_sha256
         and outer.get("schema") == OUTER_SCHEMA
         and outer.get("status") == OUTER_STATUS
         and outer.get("exact_census") == EXPECTED_MATH
         and outer.get("all_three_ledgers_independently_replayed") is True
         and outer.get("cold_replay_byte_identical") is True
         and outer.get("core_attacks_rejected") == 34
         and outer.get("release_attacks_rejected") == 40
         and outer.get("outer_is_conditional_until_independent_terminal_byte_replay") is True
         and outer.get("formal_credit") == 0
         and outer.get("manifest_authorized") is False
         and outer.get("C29") == "UNAUTHORIZED_PENDING_TERMINAL_BYTE_REPLAY",
         "conditional outer/manifests")
    parse_manifest(payload_path)
    parse_manifest(root_path)
    if args.preflight_only:
        return {"status": "PASS_C29_V2_MANIFEST_OUTER_AND_FRESH_SEAL_PREFLIGHT__NO_OUTPUT_ZERO_CREDIT"}
    output.mkdir(mode=0o700)
    seal_payload_raw = manifest({receipt_path, payload_path, root_path,
                                 outer_path, SELF})
    seal_payload_path = output / "seal_payload_manifest.sha256"
    write_once(seal_payload_path, seal_payload_raw)
    seal_root_raw = manifest({seal_payload_path, root_path, outer_path,
                              receipt_path, SELF})
    seal_root_path = output / "seal_root_manifest.sha256"
    write_once(seal_root_path, seal_root_raw)
    body = {"schema": SEAL_SCHEMA, "status": SEAL_STATUS,
            "built_at_utc": now(),
            "manifest_receipt_file_sha256": args.expect_manifest_receipt_file_sha256,
            "manifest_receipt_object_sha256": args.expect_manifest_receipt_object_sha256,
            "payload_manifest_sha256": args.expect_payload_manifest_sha256,
            "root_manifest_sha256": args.expect_root_manifest_sha256,
            "outer_verification_file_sha256": args.expect_outer_file_sha256,
            "outer_verification_object_sha256": args.expect_outer_object_sha256,
            "seal_payload_manifest_sha256": file_sha(seal_payload_path),
            "seal_root_manifest_sha256": file_sha(seal_root_path),
            "dual_predecessor_terminal_pins": outer["dual_predecessor_terminal_pins"],
            "exact_census": EXPECTED_MATH,
            "expected_terminal_status": TERMINAL_STATUS,
            "terminal_replay_completed": False, "authority_minted": False,
            "formal_credit": 0, "manifest_authorized": False,
            "C29": "UNAUTHORIZED_PENDING_INDEPENDENT_TERMINAL_BYTE_REPLAY",
            "Source_W": "UNCHANGED", "D02": "BLOCKED_COMPOSITE",
            "D03": "UNAUTHORIZED", "D04": "NOT_MINTED", "Gate5": "10/18",
            "CM2": "NO-GO_FOR_CLAIM"}
    seal = dict(body)
    seal["seal_candidate_sha256"] = digest(seal)
    write_once(output / "seal_candidate.json", canonical(seal) + b"\n")
    return seal


def self_test() -> dict[str, Any]:
    body = {"authority_minted": False, "formal_credit": 0}
    need(digest(body) == hashlib.sha256(canonical(body)).hexdigest(), "closure")
    return {"status": "PASS_C29_V2_TERMINAL_SEAL_BUILDER_SELF_TEST",
            "formal_credit": 0, "C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--preflight-only", action="store_true")
    for name in ("manifest-dir", "outer-file", "output-dir",
                 "expect-builder-sha256", "expect-outer-file-sha256",
                 "expect-outer-object-sha256",
                 "expect-manifest-receipt-file-sha256",
                 "expect-manifest-receipt-object-sha256",
                 "expect-payload-manifest-sha256",
                 "expect-root-manifest-sha256"):
        parser.add_argument("--" + name)
    args = parser.parse_args()
    fields = tuple(name.replace("-", "_") for name in (
        "manifest-dir", "outer-file", "output-dir", "expect-builder-sha256",
        "expect-outer-file-sha256", "expect-outer-object-sha256",
        "expect-manifest-receipt-file-sha256",
        "expect-manifest-receipt-object-sha256",
        "expect-payload-manifest-sha256", "expect-root-manifest-sha256"))
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
