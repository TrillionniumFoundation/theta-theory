#!/usr/bin/env python3
"""Build the manifest-first C27R2 release-repair package v2.

The approved actual-v2 terminal is bound only as predecessor evidence.  The
earlier C27R2 terminal is represented by non-authoritative historical pins and
is deliberately excluded from both payload and authority roots.  This source
cannot create a seal, terminal receipt, or PASS lock.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
AUDIT = ROOT / ".cm2-runtime/audit"
BASE = "cm2.round306c27r2.source-g-authority-v2.release-repair."
EVIDENCE_SCHEMA = BASE + "evidence-bundle.v2"
EVIDENCE_STATUS = ("PASS_C27R2_RELEASE_REPAIR_CURRENT_CORE_BOUNDARY_REAL_"
                   "CASES_AND_TRUST_DECISION_REOPENED__ZERO_CREDIT_PENDING_"
                   "MANIFEST")
MANIFEST_SCHEMA = BASE + "manifest-receipt.v2"
MANIFEST_STATUS = ("PASS_C27R2_RELEASE_REPAIR_MANIFEST_FIRST_CURRENT_CORE_"
                   "BOUNDARY_REAL_CASE_TRUST_AND_ACTUAL_V2_PREDECESSOR_"
                   "EVIDENCE_CLOSURE__ZERO_CREDIT_PENDING_OUTER")
EXPECTED = {"frozen_C15_components": 57_876,
            "post_C27R2_components": 43_684,
            "proof_derived_component_edges": 14_860,
            "successful_DSU_merges": 14_192, "cycle_edges": 668,
            "frozen_C15_members": 502_204,
            "total_unordered_member_pairs": 126_104_177_706,
            "within_post_component_member_pairs": 542_179_508,
            "cross_post_component_member_pairs": 125_561_998_198}
CANDIDATE_FILES = {"member_to_post_component.jsonl.gz",
                   "old_c15_component_to_post_component.jsonl.gz",
                   "post_component_census.jsonl.gz", "result.json"}


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
    return type(value) is str and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def strict(raw: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in items:
            need(type(key) is str and key not in out, "duplicate JSON key")
            out[key] = value
        return out
    return json.loads(raw, object_pairs_hook=pairs,
        parse_constant=lambda x: (_ for _ in ()).throw(Blocked(x)))


def inside(raw: str | Path, *, absent: bool = False) -> Path:
    supplied = Path(raw)
    path = (supplied if supplied.is_absolute() else ROOT / supplied).absolute()
    try:
        relative = path.relative_to(ROOT)
    except ValueError as error:
        raise Blocked("path outside workspace") from error
    need(relative.parts and all(x not in {"", ".", ".."}
                                for x in relative.parts), "canonical path")
    cursor = ROOT
    for part in relative.parts:
        cursor /= part
        if not cursor.exists():
            need(absent, "missing path")
            break
        need(not cursor.is_symlink(), "symlink path component")
    return path


def fingerprint(info: os.stat_result) -> list[int]:
    return [info.st_dev, info.st_ino, info.st_mode, info.st_nlink,
            info.st_size, info.st_mtime_ns, info.st_ctime_ns,
            info.st_uid, info.st_gid]


def record(path: Path) -> dict[str, Any]:
    need(path.is_file() and not path.is_symlink(), "regular current file")
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "single-link current file")
        state = hashlib.sha256()
        while block := os.read(fd, 4 << 20):
            state.update(block)
        need(fingerprint(os.stat(path, follow_symlinks=False))
             == fingerprint(before), "stable current file")
        return {"path": str(path.relative_to(ROOT)), "sha256": state.hexdigest(),
                "size": before.st_size, "stat_fingerprint": fingerprint(before)}
    finally:
        os.close(fd)


def document(path: Path, closure: str) -> tuple[dict[str, Any], dict[str, Any]]:
    item = record(path)
    raw = path.read_bytes()
    need(raw.endswith(b"\n"), "JSON newline")
    value = strict(raw[:-1])
    need(type(value) is dict and canonical(value) == raw[:-1], "canonical JSON")
    body = dict(value)
    claim = body.pop(closure, None)
    need(valid_sha(claim) and claim == digest(body), "object closure:" + closure)
    return value, item


def parse_manifest(path: Path) -> dict[str, dict[str, Any]]:
    raw = path.read_bytes()
    need(raw.endswith(b"\n"), "manifest newline")
    result: dict[str, dict[str, Any]] = {}
    for line in raw.decode("ascii").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\x00\r\n]+)", line)
        need(match is not None, "manifest line")
        claim, shown = match.groups()
        need(shown not in result, "manifest duplicate")
        item = record(inside(shown))
        need(item["sha256"] == claim, "manifest current SHA")
        result[shown] = item
    need(result and list(result) == sorted(result), "sorted nonempty manifest")
    return result


def manifest(paths: set[Path]) -> bytes:
    rows = []
    for path in sorted(paths):
        item = record(path)
        rows.append(f"{item['sha256']}  {item['path']}\n")
    need(rows, "nonempty manifest")
    return "".join(rows).encode("ascii")


def write(path: Path, raw: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                 | getattr(os, "O_NOFOLLOW", 0), 0o400)
    try:
        os.write(fd, raw); os.fsync(fd)
    finally:
        os.close(fd)


def actual_terminal(decision: dict[str, Any], args: argparse.Namespace) -> set[Path]:
    need(decision.get("schema") == args.expect_decision_schema
         and decision.get("status") == args.expect_decision_status
         and decision.get("eligible_as_predecessor_evidence") is True
         and decision.get("authority_eligible") is False
         and decision.get("old_C27R2_authority_eligible") is False
         and decision.get("formal_credit") == 0, "decision semantics")
    terminal = decision.get("actual_v2_terminal")
    need(type(terminal) is dict, "actual-v2 terminal map")
    path = inside(terminal.get("terminal_dir", ""))
    names = {"PASS.lock", "payload_manifest.sha256", "root_manifest.sha256",
             "terminal_receipt.json", "terminal_replay.json"}
    file_map = terminal.get("files")
    need(path.is_dir() and not path.is_symlink()
         and {x.name for x in path.iterdir()} == names
         and type(file_map) is dict and set(file_map) == names,
         "actual-v2 terminal exact inventory/map")
    answer = {path / name for name in names}
    for item in answer:
        need(record(item)["sha256"] == file_map[item.name],
             "actual-v2 decision current pin")
    return answer


def execute(args: argparse.Namespace) -> dict[str, Any]:
    dynamic = (args.expect_self_sha256, args.expect_evidence_file_sha256,
        args.expect_evidence_object_sha256, args.expect_decision_file_sha256,
        args.expect_decision_object_sha256,
        args.historical_terminal_root_sha256,
        args.historical_terminal_receipt_file_sha256,
        args.historical_terminal_receipt_object_sha256,
        args.historical_terminal_replay_file_sha256,
        args.historical_terminal_replay_object_sha256,
        args.historical_terminal_pass_sha256)
    need(all(valid_sha(x) for x in dynamic), "all dynamic SHA pins")
    need(record(SELF)["sha256"] == args.expect_self_sha256, "self pin")
    need(type(args.expect_decision_schema) is str and args.expect_decision_schema
         and type(args.expect_decision_status) is str and args.expect_decision_status
         and type(args.decision_closure_key) is str and args.decision_closure_key,
         "decision dynamic strings")

    evidence_dir = inside(args.evidence_dir)
    evidence, evidence_record = document(evidence_dir / "evidence_bundle.json",
                                         "evidence_bundle_sha256")
    inventory_path = evidence_dir / "authority_inventory.sha256"
    inventory = parse_manifest(inventory_path)
    need(evidence_record["sha256"] == args.expect_evidence_file_sha256
         and evidence["evidence_bundle_sha256"]
             == args.expect_evidence_object_sha256
         and evidence.get("schema") == EVIDENCE_SCHEMA
         and evidence.get("status") == EVIDENCE_STATUS
         and evidence.get("authority_inventory_file_sha256")
             == record(inventory_path)["sha256"]
         and evidence.get("authority_inventory_member_count") == len(inventory)
         and evidence.get("exact_math") == EXPECTED
         and evidence.get("actual_v2_terminal_role")
             == "PREDECESSOR_EVIDENCE_ONLY"
         and evidence.get("actual_v2_terminal_authority_eligible") is False
         and evidence.get("formal_credit") == 0,
         "evidence exact closure")

    decision_path = inside(args.trust_decision)
    decision, decision_record = document(decision_path, args.decision_closure_key)
    need(decision_record["sha256"] == args.expect_decision_file_sha256
         and decision[args.decision_closure_key]
             == args.expect_decision_object_sha256
         and evidence.get("decision_file_sha256") == decision_record["sha256"]
         and evidence.get("decision_object_sha256")
             == decision[args.decision_closure_key], "decision/evidence closure")
    actual_files = actual_terminal(decision, args)

    candidate = inside(args.candidate_dir)
    need(candidate.is_dir() and not candidate.is_symlink()
         and {x.name for x in candidate.iterdir()} == CANDIDATE_FILES
         and all(x.is_file() and not x.is_symlink() for x in candidate.iterdir()),
         "candidate exact four files")
    result, _ = document(candidate / "result.json", "result_sha256")
    need(result.get("exact_census") == EXPECTED and result.get("formal_credit") == 0,
         "candidate exact math")

    verification = inside(args.verification)
    core_attacks = inside(args.core_attacks)
    payload_files = {inside(path) for path in inventory}
    payload_files |= {evidence_dir / "evidence_bundle.json", inventory_path,
                      decision_path, verification, core_attacks, SELF}
    payload_files |= {candidate / name for name in CANDIDATE_FILES}
    for raw in args.source_file:
        payload_files.add(inside(raw))
    need(not any("c27r2-release-chain-v1-formal-r1-20260808T183910-terminal"
                 in str(path) for path in payload_files),
         "historical C27R2 terminal excluded from payload")

    output = inside(args.output_dir, absent=True)
    need(not output.exists() and not output.is_symlink(), "fresh manifest output")
    output.mkdir(parents=True, mode=0o700)
    payload_raw = manifest(payload_files)
    payload_path = output / "payload_manifest.sha256"
    write(payload_path, payload_raw)
    root_files = set(actual_files) | {payload_path, SELF}
    root_raw = manifest(root_files)
    root_path = output / "root_manifest.sha256"
    write(root_path, root_raw)
    historical = {
        "root_manifest_file_sha256": args.historical_terminal_root_sha256,
        "terminal_receipt_file_sha256":
            args.historical_terminal_receipt_file_sha256,
        "terminal_receipt_object_sha256":
            args.historical_terminal_receipt_object_sha256,
        "terminal_replay_file_sha256":
            args.historical_terminal_replay_file_sha256,
        "terminal_replay_object_sha256":
            args.historical_terminal_replay_object_sha256,
        "PASS_lock_file_sha256": args.historical_terminal_pass_sha256,
        "role": "HISTORICAL_AUDIT_ONLY", "authority_eligible": False,
        "included_in_payload": False, "included_in_authority_root": False}
    body = {"schema": MANIFEST_SCHEMA, "status": MANIFEST_STATUS,
        "completed_at_utc": datetime.now(timezone.utc).isoformat(
            timespec="microseconds").replace("+00:00", "Z"),
        "evidence_bundle_file_sha256": evidence_record["sha256"],
        "evidence_bundle_object_sha256": evidence["evidence_bundle_sha256"],
        "decision_file_sha256": decision_record["sha256"],
        "decision_object_sha256": decision[args.decision_closure_key],
        "boundary_receipt_object_sha256":
            evidence["boundary_receipt_object_sha256"],
        "case_receipt_object_sha256": evidence["case_receipt_object_sha256"],
        "payload_manifest_file_sha256": record(payload_path)["sha256"],
        "payload_member_count": len(payload_files),
        "root_manifest_file_sha256": record(root_path)["sha256"],
        "root_member_count": len(root_files),
        "actual_v2_terminal_role": "PREDECESSOR_EVIDENCE_ONLY",
        "actual_v2_terminal_authority_eligible": False,
        "historical_C27R2_terminal": historical,
        "exact_math": EXPECTED, "formal_credit": 0,
        "manifest_authorized": False, "authority_minted": False,
        "C27R2": "AUDIT_HOLD_UNAUTHORIZED", "C28_C29": "UNAUTHORIZED",
        "CM2": "NO-GO_FOR_CLAIM"}
    receipt = {**body, "manifest_receipt_sha256": digest(body)}
    write(output / "manifest_receipt.json", canonical(receipt) + b"\n")
    need({x.name for x in output.iterdir()} == {"manifest_receipt.json",
         "payload_manifest.sha256", "root_manifest.sha256"},
         "manifest output inventory")
    return receipt


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--self-test", action="store_true")
    names = ("evidence-dir", "candidate-dir", "verification", "core-attacks",
        "trust-decision", "decision-closure-key", "expect-decision-schema",
        "expect-decision-status", "output-dir", "expect-self-sha256",
        "expect-evidence-file-sha256", "expect-evidence-object-sha256",
        "expect-decision-file-sha256", "expect-decision-object-sha256",
        "historical-terminal-root-sha256",
        "historical-terminal-receipt-file-sha256",
        "historical-terminal-receipt-object-sha256",
        "historical-terminal-replay-file-sha256",
        "historical-terminal-replay-object-sha256",
        "historical-terminal-pass-sha256")
    for name in names:
        value.add_argument("--" + name)
    value.add_argument("--source-file", action="append")
    return value


def main() -> int:
    p = parser(); args = p.parse_args()
    names = [x.dest for x in p._actions if x.dest not in {"help", "self_test",
                                                          "source_file"}]
    try:
        if args.self_test:
            need(all(getattr(args, x) is None for x in names)
                 and args.source_file is None, "self-test no arguments")
            need(EXPECTED["frozen_C15_components"]
                 - EXPECTED["successful_DSU_merges"]
                 == EXPECTED["post_C27R2_components"], "manifest fixture")
            result = {"status": "PASS_C27R2_RELEASE_REPAIR_MANIFEST_V2_SELF_TEST"}
        else:
            need(all(getattr(args, x) is not None for x in names)
                 and type(args.source_file) is list and args.source_file,
                 "all manifest arguments/source pins required")
            result = execute(args)
        sys.stdout.buffer.write(canonical({"CM2": "NO-GO_FOR_CLAIM",
            "formal_credit": 0, "status": result["status"]}) + b"\n")
        return 0
    except (Blocked, OSError, ValueError, KeyError, TypeError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
