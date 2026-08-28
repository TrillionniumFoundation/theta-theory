#!/usr/bin/env python3
"""Independent terminal byte replay and receipt mint for C27R2 authority v2.

This is the only release source allowed to authorize C27R2.  It independently
revalidates the conditional seal, outer verifier, manifests and current bytes,
constructs the expected terminal receipt twice, and requires exact canonical
byte identity.  It never starts C28 or C29 and leaves CM2 NO-GO.
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
GATE = AUDIT / "c27r2-post-actual-v2-rebuild-gate-v3-r2-zero-credit-20260808T164429"
ACTUAL_TERMINAL = AUDIT / (
    "c27-primitive-twenty-family-gate-v5-actual-v2-dual-seed-zero-credit-"
    "seal-v2-20260808T1544-terminal-replay"
)
SEAL_SCHEMA = (
    "cm2.round306c27r2.source-g-authority-v2.release-terminal-seal-candidate.v1"
)
SEAL_STATUS = (
    "PASS_CONDITIONAL_TERMINAL_SEAL_CANDIDATE__ZERO_CREDIT_PENDING_"
    "INDEPENDENT_BYTE_REPLAY"
)
OUTER_SCHEMA = (
    "cm2.round306c27r2.source-g-authority-v2.release-outer-verification.v1"
)
OUTER_STATUS = (
    "PASS_INDEPENDENT_RELEASE_OUTER_FULL_LEDGER_MANIFEST_COLD_AND_ATTACK_"
    "CHECK__CONDITIONAL_C27R2_ZERO_CREDIT"
)
TERMINAL_STATUS = (
    "PASS_C27R2_TERMINAL_BYTE_REPLAY__FORMAL_C27R2_AUTHORITY_MINTED"
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
CANDIDATE_FILES = ["member_to_post_component.jsonl.gz",
                   "old_c15_component_to_post_component.jsonl.gz",
                   "post_component_census.jsonl.gz", "result.json"]
PASS_BYTES = b"PASS_C27R2_AUTHORITY_V2_TERMINAL_BYTE_REPLAY__C28_C29_UNAUTHORIZED\n"


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
    need(payload.endswith(b"\n"), "manifest newline")
    rows: dict[str, str] = {}
    for line in payload.decode("ascii").splitlines():
        pieces = line.split("  ", 1)
        need(len(pieces) == 2 and valid_sha(pieces[0])
             and pieces[1] not in rows and pieces[1] != "",
             "manifest row syntax/unique")
        relative = Path(pieces[1])
        need(not relative.is_absolute()
             and all(part not in {"", ".", ".."} for part in relative.parts)
             and str(relative) == pieces[1], "canonical manifest path")
        rows[pieces[1]] = pieces[0]
    need(list(rows) == sorted(rows), "manifest sorted paths")
    for relative, expected in rows.items():
        need(file_sha(ROOT / relative) == expected,
             "manifest current member:" + relative)
    return rows


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


def terminal_body(seal: dict[str, Any], outer: dict[str, Any],
                  terminal_payload_sha: str, terminal_root_sha: str) \
        -> dict[str, Any]:
    return {
        "schema": "cm2.round306c27r2.source-g-authority-v2.terminal-receipt.v1",
        "status": TERMINAL_STATUS,
        "seal_candidate_object_sha256": seal["seal_candidate_sha256"],
        "manifest_receipt_object_sha256":
            seal["manifest_receipt_object_sha256"],
        "payload_manifest_sha256": seal["payload_manifest_sha256"],
        "root_manifest_sha256": seal["root_manifest_sha256"],
        "outer_verification_object_sha256":
            outer["outer_verification_sha256"],
        "terminal_payload_manifest_sha256": terminal_payload_sha,
        "terminal_root_manifest_sha256": terminal_root_sha,
        "exact_census": EXPECTED_MATH,
        "terminal_replay_completed": True,
        "terminal_receipt_byte_replay_identical": True,
        "authority_minted": True,
        "formal_credit": 0,
        "manifest_authorized": True,
        "C27R2": "AUTHORIZED_TERMINAL_SOURCE_G_QUOTIENT_AUTHORITY",
        "C28": "UNAUTHORIZED_NOT_STARTED",
        "C29": "UNAUTHORIZED_NOT_STARTED",
        "Source_W": "UNCHANGED",
        "D02": "BLOCKED_COMPOSITE", "D03": "UNAUTHORIZED",
        "D04": "NOT_MINTED", "Gate5": "10/18",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def execute(args: argparse.Namespace) -> dict[str, Any]:
    pins = (args.expect_replay_sha256, args.expect_seal_candidate_file_sha256,
            args.expect_seal_candidate_object_sha256,
            args.expect_seal_payload_manifest_sha256,
            args.expect_seal_root_manifest_sha256,
            args.expect_outer_file_sha256, args.expect_outer_object_sha256,
            args.expect_manifest_receipt_file_sha256,
            args.expect_manifest_receipt_object_sha256)
    need(all(valid_sha(value) for value in pins)
         and file_sha(SELF) == args.expect_replay_sha256,
         "all replay dynamic/self pins")
    seal_dir = Path(args.seal_dir).absolute()
    manifest_dir = Path(args.manifest_dir).absolute()
    outer_path = Path(args.outer_file).absolute()
    output = Path(args.output_dir).absolute()
    need(output.parent == AUDIT and not output.exists(),
         "fresh terminal replay directory")
    need({entry.name for entry in seal_dir.iterdir()} == {
        "seal_candidate.json", "seal_payload_manifest.sha256",
        "seal_root_manifest.sha256"}, "exact seal candidate inventory")
    seal_path = seal_dir / "seal_candidate.json"
    seal_payload = seal_dir / "seal_payload_manifest.sha256"
    seal_root = seal_dir / "seal_root_manifest.sha256"
    receipt_path = manifest_dir / "manifest_receipt.json"
    seal = document(seal_path, "seal_candidate_sha256")
    outer = document(outer_path, "outer_verification_sha256")
    manifest_receipt = document(receipt_path, "manifest_receipt_sha256")
    need(file_sha(seal_path) == args.expect_seal_candidate_file_sha256
         and seal["seal_candidate_sha256"]
             == args.expect_seal_candidate_object_sha256
         and file_sha(seal_payload) == args.expect_seal_payload_manifest_sha256
         and file_sha(seal_root) == args.expect_seal_root_manifest_sha256
         and file_sha(outer_path) == args.expect_outer_file_sha256
         and outer["outer_verification_sha256"] == args.expect_outer_object_sha256
         and file_sha(receipt_path) == args.expect_manifest_receipt_file_sha256
         and manifest_receipt["manifest_receipt_sha256"]
             == args.expect_manifest_receipt_object_sha256
         and seal.get("schema") == SEAL_SCHEMA and seal.get("status") == SEAL_STATUS
         and seal.get("exact_census") == EXPECTED_MATH
         and seal.get("terminal_replay_completed") is False
         and seal.get("authority_minted") is False
         and seal.get("manifest_authorized") is False
         and outer.get("schema") == OUTER_SCHEMA
         and outer.get("status") == OUTER_STATUS
         and outer.get("exact_census") == EXPECTED_MATH
         and outer.get("formal_credit") == 0,
         "exact conditional seal/outer/manifest")
    parse_manifest(seal_payload)
    parse_manifest(seal_root)
    parse_manifest(manifest_dir / "payload_manifest.sha256")
    parse_manifest(manifest_dir / "root_manifest.sha256")
    if args.preflight_only:
        return {"status": "PASS_SEAL_OUTER_MANIFEST_AND_FRESH_TERMINAL_PREFLIGHT__NO_OUTPUT_CREATED_ZERO_CREDIT"}
    terminal_payload_raw = manifest([
        seal_path, seal_payload, seal_root, receipt_path,
        manifest_dir / "payload_manifest.sha256",
        manifest_dir / "root_manifest.sha256", outer_path,
        CONTROL / "transaction_receipt.json", CONTROL / "PASS.lock", SELF,
    ] + [CANDIDATE / name for name in CANDIDATE_FILES])
    terminal_payload_sha = hashlib.sha256(terminal_payload_raw).hexdigest()
    output.mkdir(mode=0o700)
    payload_path = output / "payload_manifest.sha256"
    write_once(payload_path, terminal_payload_raw)
    terminal_root_raw = manifest([
        payload_path, seal_root, manifest_dir / "root_manifest.sha256",
        CONTROL / "transaction_receipt.json", CONTROL / "PASS.lock",
        GATE / "execution_receipt.json", GATE / "PASS.lock",
        ACTUAL_TERMINAL / "root_manifest.sha256", SELF,
    ])
    terminal_root_sha = hashlib.sha256(terminal_root_raw).hexdigest()
    root_path = output / "root_manifest.sha256"
    write_once(root_path, terminal_root_raw)
    first = terminal_body(seal, outer, terminal_payload_sha, terminal_root_sha)
    second = terminal_body(dict(seal), dict(outer),
                           file_sha(payload_path), file_sha(root_path))
    need(first == second and canonical(first) == canonical(second),
         "independent terminal body byte replay")
    receipt = {**first, "terminal_receipt_sha256": digest(first)}
    receipt_raw = canonical(receipt) + b"\n"
    receipt_output = output / "terminal_receipt.json"
    write_once(receipt_output, receipt_raw)
    need(receipt_output.read_bytes() == receipt_raw,
         "terminal receipt exact byte replay")
    replay_body = {
        "schema": "cm2.round306c27r2.source-g-authority-v2.terminal-byte-replay.v1",
        "status": TERMINAL_STATUS,
        "terminal_receipt_file_sha256": file_sha(receipt_output),
        "terminal_receipt_object_sha256": receipt["terminal_receipt_sha256"],
        "terminal_receipt_byte_replay_identical": True,
        "terminal_payload_manifest_sha256": terminal_payload_sha,
        "terminal_root_manifest_sha256": terminal_root_sha,
        "authority_minted": True, "formal_credit": 0,
        "manifest_authorized": True,
        "C27R2": "AUTHORIZED_TERMINAL_SOURCE_G_QUOTIENT_AUTHORITY",
        "C28_C29": "UNAUTHORIZED_NOT_STARTED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    replay = {**replay_body, "terminal_replay_sha256": digest(replay_body)}
    replay_path = output / "terminal_replay.json"
    write_once(replay_path, canonical(replay) + b"\n")
    chain_body = {
        "schema": "cm2.round306c27r2.source-g-authority-v2.release-chain-status.v1",
        "status": TERMINAL_STATUS,
        "terminal_receipt_file_sha256": file_sha(receipt_output),
        "terminal_receipt_object_sha256": receipt["terminal_receipt_sha256"],
        "terminal_replay_file_sha256": file_sha(replay_path),
        "terminal_replay_object_sha256": replay["terminal_replay_sha256"],
        "authority_minted": True, "formal_credit": 0,
        "manifest_authorized": True,
        "C27R2": "AUTHORIZED_TERMINAL_SOURCE_G_QUOTIENT_AUTHORITY",
        "C28_C29": "UNAUTHORIZED_NOT_STARTED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    chain = {**chain_body, "chain_status_sha256": digest(chain_body)}
    write_once(output / "chain_status.json", canonical(chain) + b"\n")
    write_once(output / "PASS.lock", PASS_BYTES)
    return replay


def self_test() -> dict[str, Any]:
    seal = {"seal_candidate_sha256": "0" * 64,
            "manifest_receipt_object_sha256": "1" * 64,
            "payload_manifest_sha256": "2" * 64,
            "root_manifest_sha256": "3" * 64}
    outer = {"outer_verification_sha256": "4" * 64}
    first = terminal_body(seal, outer, "5" * 64, "6" * 64)
    second = terminal_body(dict(seal), dict(outer), "5" * 64, "6" * 64)
    need(canonical(first) == canonical(second), "terminal byte fixture")
    return {"status": "PASS_INDEPENDENT_TERMINAL_BODY_BYTE_FIXTURE"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--preflight-only", action="store_true")
    for name in ("seal-dir", "manifest-dir", "outer-file", "output-dir",
                 "expect-replay-sha256", "expect-seal-candidate-file-sha256",
                 "expect-seal-candidate-object-sha256",
                 "expect-seal-payload-manifest-sha256",
                 "expect-seal-root-manifest-sha256",
                 "expect-outer-file-sha256", "expect-outer-object-sha256",
                 "expect-manifest-receipt-file-sha256",
                 "expect-manifest-receipt-object-sha256"):
        parser.add_argument("--" + name)
    args = parser.parse_args()
    fields = tuple(name.replace("-", "_") for name in (
        "seal-dir", "manifest-dir", "outer-file", "output-dir",
        "expect-replay-sha256", "expect-seal-candidate-file-sha256",
        "expect-seal-candidate-object-sha256",
        "expect-seal-payload-manifest-sha256",
        "expect-seal-root-manifest-sha256", "expect-outer-file-sha256",
        "expect-outer-object-sha256", "expect-manifest-receipt-file-sha256",
        "expect-manifest-receipt-object-sha256"))
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
