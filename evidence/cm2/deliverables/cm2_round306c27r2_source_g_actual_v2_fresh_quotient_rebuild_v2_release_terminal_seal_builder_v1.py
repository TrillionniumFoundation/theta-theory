#!/usr/bin/env python3
"""Build a conditional C27R2 terminal seal candidate.

This builder binds the manifest-first package and independent outer verifier.
It emits no PASS lock and no authority.  Only the separate terminal byte
replay source may turn this candidate into the terminal receipt.
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
OUTER_SCHEMA = (
    "cm2.round306c27r2.source-g-authority-v2.release-outer-verification.v1"
)
OUTER_STATUS = (
    "PASS_INDEPENDENT_RELEASE_OUTER_FULL_LEDGER_MANIFEST_COLD_AND_ATTACK_"
    "CHECK__CONDITIONAL_C27R2_ZERO_CREDIT"
)
MANIFEST_SCHEMA = (
    "cm2.round306c27r2.source-g-authority-v2.release-manifest-receipt.v1"
)
EXPECTED_MATH = {
    "frozen_C15_members": 502_204, "frozen_C15_components": 57_876,
    "proof_derived_component_edges": 14_860,
    "successful_DSU_merges": 14_192, "cycle_edges": 668,
    "post_C27R2_components": 43_684,
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
    return (type(value) is str and len(value) == 64
            and all(character in "0123456789abcdef" for character in value))


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace(
        "+00:00", "Z")


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns,
            value.st_uid, value.st_gid)


def file_sha(path: Path) -> str:
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
        need(fingerprint(before) == fingerprint(os.fstat(fd)),
             "stable SHA/stat:" + str(path))
        return state.hexdigest()
    finally:
        os.close(fd)


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
    need(payload.endswith(b"\n"), "JSON newline")
    value = strict_load(payload[:-1])
    need(type(value) is dict and canonical(value) == payload[:-1],
         "canonical JSON")
    body = dict(value)
    claim = body.pop(closure, None)
    need(valid_sha(claim) and claim == digest(body), "object closure")
    return value


def manifest(paths: list[Path]) -> bytes:
    rows = sorted((str(path.absolute().relative_to(ROOT)), file_sha(path))
                  for path in paths)
    need(len(rows) == len(set(path for path, _ in rows)),
         "manifest unique paths")
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


def execute(args: argparse.Namespace) -> dict[str, Any]:
    pins = (args.expect_builder_sha256, args.expect_outer_file_sha256,
            args.expect_outer_object_sha256,
            args.expect_manifest_receipt_file_sha256,
            args.expect_manifest_receipt_object_sha256,
            args.expect_payload_manifest_sha256,
            args.expect_root_manifest_sha256)
    need(all(valid_sha(value) for value in pins)
         and file_sha(SELF) == args.expect_builder_sha256,
         "all seal dynamic/self pins")
    manifest_dir = Path(args.manifest_dir).absolute()
    outer_path = Path(args.outer_file).absolute()
    output = Path(args.output_dir).absolute()
    need(output.parent == AUDIT and not output.exists(),
         "fresh seal candidate directory")
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
         and outer["outer_verification_sha256"]
             == args.expect_outer_object_sha256
         and outer.get("schema") == OUTER_SCHEMA
         and outer.get("status") == OUTER_STATUS
         and outer.get("exact_census") == EXPECTED_MATH
         and outer.get("cold_replay_byte_identical") is True
         and outer.get("core_attacks_rejected") == 21
         and outer.get("release_attacks_rejected") == 20
         and outer.get("outer_is_conditional_until_independent_terminal_byte_replay")
             is True and outer.get("formal_credit") == 0
         and outer.get("manifest_authorized") is False
         and outer.get("C27R2") == "UNAUTHORIZED_PENDING_TERMINAL_BYTE_REPLAY",
         "exact conditional outer and manifests")
    if args.preflight_only:
        return {"status": "PASS_MANIFEST_OUTER_AND_FRESH_SEAL_PREFLIGHT__NO_OUTPUT_CREATED_ZERO_CREDIT"}
    payload_raw = manifest([receipt_path, payload_path, root_path, outer_path,
                            SELF])
    body = {
        "schema": "cm2.round306c27r2.source-g-authority-v2.release-terminal-seal-candidate.v1",
        "status": "PASS_CONDITIONAL_TERMINAL_SEAL_CANDIDATE__ZERO_CREDIT_PENDING_INDEPENDENT_BYTE_REPLAY",
        "built_at_utc": utc_now(),
        "manifest_receipt_file_sha256": args.expect_manifest_receipt_file_sha256,
        "manifest_receipt_object_sha256":
            args.expect_manifest_receipt_object_sha256,
        "payload_manifest_sha256": args.expect_payload_manifest_sha256,
        "root_manifest_sha256": args.expect_root_manifest_sha256,
        "outer_verification_file_sha256": args.expect_outer_file_sha256,
        "outer_verification_object_sha256": args.expect_outer_object_sha256,
        "exact_census": EXPECTED_MATH,
        "expected_terminal_status":
            "PASS_C27R2_TERMINAL_BYTE_REPLAY__FORMAL_C27R2_AUTHORITY_MINTED",
        "terminal_replay_completed": False,
        "authority_minted": False, "formal_credit": 0,
        "manifest_authorized": False,
        "C27R2": "UNAUTHORIZED_PENDING_INDEPENDENT_TERMINAL_BYTE_REPLAY",
        "C28_C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM",
    }
    seal = {**body, "seal_candidate_sha256": digest(body)}
    output.mkdir(mode=0o700)
    write_once(output / "seal_payload_manifest.sha256", payload_raw)
    root_raw = manifest([output / "seal_payload_manifest.sha256", root_path,
                         outer_path, receipt_path, SELF])
    write_once(output / "seal_root_manifest.sha256", root_raw)
    write_once(output / "seal_candidate.json", canonical(seal) + b"\n")
    return seal


def self_test() -> dict[str, Any]:
    body = {"authority_minted": False, "formal_credit": 0}
    need(digest(body) == hashlib.sha256(canonical(body)).hexdigest(),
         "seal closure fixture")
    return {"status": "PASS_SEAL_CANDIDATE_CLOSURE_FIXTURE"}


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
