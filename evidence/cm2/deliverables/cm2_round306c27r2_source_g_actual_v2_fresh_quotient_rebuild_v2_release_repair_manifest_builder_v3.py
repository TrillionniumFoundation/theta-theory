#!/usr/bin/env python3
"""Build the final manifest-first C27R2 release-repair package v3.

Consumes only the post-attack Stage-B closure.  The actual-v2 terminal is
included as predecessor evidence, never authority.  The earlier C27R2
terminal is current-byte checked for the same core/candidate hashes but is
recorded as HISTORICAL_AUDIT_HOLD and excluded from both new manifests.
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
BASE = "cm2.round306c27r2.source-g-authority-v2.release-repair."
SNAPSHOT_SCHEMA = BASE + "current-snapshot-evidence.v2"
POST_SCHEMA = BASE + "post-attack-evidence-closure.v3"
MANIFEST_SCHEMA = BASE + "manifest-receipt.v3"
MANIFEST_STATUS = ("PASS_C27R2_RELEASE_REPAIR_POST_ATTACK_MANIFEST_FIRST_"
                   "ACTUAL_V2_EVIDENCE_AND_HISTORICAL_COMPATIBILITY_CLOSED__"
                   "ZERO_CREDIT_PENDING_OUTER")
EXPECTED = {"frozen_C15_components": 57_876,
            "post_C27R2_components": 43_684,
            "proof_derived_component_edges": 14_860,
            "successful_DSU_merges": 14_192, "cycle_edges": 668,
            "frozen_C15_members": 502_204,
            "total_unordered_member_pairs": 126_104_177_706,
            "within_post_component_member_pairs": 542_179_508,
            "cross_post_component_member_pairs": 125_561_998_198}
CANDIDATE = {"member_to_post_component.jsonl.gz",
             "old_c15_component_to_post_component.jsonl.gz",
             "post_component_census.jsonl.gz", "result.json"}
OLD_TERMINAL = {"PASS.lock", "chain_status.json", "payload_manifest.sha256",
                "root_manifest.sha256", "terminal_receipt.json",
                "terminal_replay.json"}


class Blocked(RuntimeError): pass


def need(v: bool, label: str) -> None:
    if type(v) is not bool or not v: raise Blocked(label)


def canonical(v: Any) -> bytes:
    return json.dumps(v, sort_keys=True, separators=(",", ":"),
        ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(v: Any) -> str: return hashlib.sha256(canonical(v)).hexdigest()


def sha(v: Any) -> bool:
    return type(v) is str and re.fullmatch(r"[0-9a-f]{64}", v) is not None


def strict(raw: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for k, v in items: need(k not in out, "duplicate key"); out[k] = v
        return out
    return json.loads(raw, object_pairs_hook=pairs,
        parse_constant=lambda x: (_ for _ in ()).throw(Blocked(x)))


def inside(raw: str | Path, absent: bool = False) -> Path:
    supplied = Path(raw); path = (supplied if supplied.is_absolute()
        else ROOT / supplied).absolute()
    try: rel = path.relative_to(ROOT)
    except ValueError as error: raise Blocked("outside workspace") from error
    need(rel.parts and all(x not in {"", ".", ".."} for x in rel.parts),
         "canonical path")
    cursor = ROOT
    for part in rel.parts:
        cursor /= part
        if not cursor.exists(): need(absent, "missing path"); break
        need(not cursor.is_symlink(), "symlink path")
    return path


def fp(s: os.stat_result) -> list[int]:
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size,
            s.st_mtime_ns, s.st_ctime_ns, s.st_uid, s.st_gid]


def rec(path: Path) -> dict[str, Any]:
    need(path.is_file() and not path.is_symlink(), "regular file")
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd); need(stat.S_ISREG(before.st_mode)
            and before.st_nlink == 1, "single-link")
        h = hashlib.sha256()
        while block := os.read(fd, 4 << 20): h.update(block)
        need(fp(os.stat(path, follow_symlinks=False)) == fp(before), "stable file")
        return {"path": str(path.relative_to(ROOT)), "sha256": h.hexdigest(),
                "size": before.st_size, "stat_fingerprint": fp(before)}
    finally: os.close(fd)


def doc(path: Path, closure: str) -> tuple[dict[str, Any], dict[str, Any]]:
    r = rec(path); raw = path.read_bytes(); need(raw.endswith(b"\n"), "newline")
    v = strict(raw[:-1]); need(type(v) is dict and canonical(v) == raw[:-1],
        "canonical JSON")
    body = dict(v); claim = body.pop(closure, None)
    need(sha(claim) and claim == digest(body), "object closure")
    return v, r


def manifest(path: Path) -> dict[str, dict[str, Any]]:
    raw = path.read_bytes(); need(raw.endswith(b"\n"), "manifest newline")
    out: dict[str, dict[str, Any]] = {}
    for line in raw.decode("ascii").splitlines():
        m = re.fullmatch(r"([0-9a-f]{64})  ([^\x00\r\n]+)", line)
        need(m is not None, "manifest row"); claim, shown = m.groups()
        need(shown not in out, "duplicate manifest path")
        item = rec(inside(shown)); need(item["sha256"] == claim, "current SHA")
        out[shown] = item
    need(out and list(out) == sorted(out), "sorted manifest")
    return out


def manifest_bytes(paths: set[Path]) -> bytes:
    rows = []
    for path in sorted(paths):
        item = rec(path); rows.append(f"{item['sha256']}  {item['path']}\n")
    need(rows, "nonempty manifest"); return "".join(rows).encode("ascii")


def write(path: Path, raw: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                 | getattr(os, "O_NOFOLLOW", 0), 0o400)
    try: os.write(fd, raw); os.fsync(fd)
    finally: os.close(fd)


def execute(a: argparse.Namespace) -> dict[str, Any]:
    pins = (a.expect_self_sha256, a.expect_post_file_sha256,
        a.expect_post_object_sha256, a.expect_snapshot_file_sha256,
        a.expect_snapshot_object_sha256, a.expect_decision_file_sha256,
        a.expect_decision_object_sha256, a.expect_old_root_sha256,
        a.expect_old_receipt_file_sha256, a.expect_old_receipt_object_sha256,
        a.expect_old_replay_file_sha256, a.expect_old_replay_object_sha256,
        a.expect_old_pass_sha256, a.expect_core_receipt_file_sha256,
        a.expect_core_receipt_object_sha256)
    need(all(sha(x) for x in pins) and rec(SELF)["sha256"]
         == a.expect_self_sha256, "dynamic SHA/self pins")
    need(all(type(x) is str and x for x in (a.decision_closure_key,
        a.expect_decision_schema, a.expect_decision_status)), "decision strings")

    post_dir = inside(a.post_evidence_dir)
    post, pr = doc(post_dir / "post_attack_evidence.json",
                   "post_attack_evidence_sha256")
    inv_path = post_dir / "authority_inventory.sha256"; inv = manifest(inv_path)
    need(pr["sha256"] == a.expect_post_file_sha256
         and post["post_attack_evidence_sha256"] == a.expect_post_object_sha256
         and post.get("schema") == POST_SCHEMA and post.get("real_case_count") == 44
         and post.get("real_cases_rejected") == 44
         and post.get("authority_pre_post_sha_stat_identical") is True
         and post.get("case_cleanup_complete") is True
         and post.get("authority_inventory_file_sha256") == rec(inv_path)["sha256"]
         and post.get("authority_inventory_member_count") == len(inv)
         and post.get("exact_math") == EXPECTED and post.get("formal_credit") == 0,
         "post evidence closure")

    snapshot_dir = inside(a.snapshot_dir)
    snapshot, sr = doc(snapshot_dir / "snapshot_evidence.json",
                       "snapshot_evidence_sha256")
    need(sr["sha256"] == a.expect_snapshot_file_sha256
         and snapshot["snapshot_evidence_sha256"]
             == a.expect_snapshot_object_sha256
         and snapshot.get("schema") == SNAPSHOT_SCHEMA
         and post.get("snapshot_evidence_file_sha256") == sr["sha256"]
         and post.get("snapshot_evidence_object_sha256")
             == snapshot["snapshot_evidence_sha256"]
         and snapshot.get("core_receipt_file_sha256")
             == a.expect_core_receipt_file_sha256
         and snapshot.get("core_receipt_object_sha256")
             == a.expect_core_receipt_object_sha256, "snapshot/core closure")

    decision_path = inside(a.trust_decision)
    decision, dr = doc(decision_path, a.decision_closure_key)
    need(dr["sha256"] == a.expect_decision_file_sha256
         and decision[a.decision_closure_key] == a.expect_decision_object_sha256
         and decision.get("schema") == a.expect_decision_schema
         and decision.get("status") == a.expect_decision_status
         and decision.get("eligible_as_predecessor_evidence") is True
         and decision.get("authority_eligible") is False
         and decision.get("old_C27R2_authority_eligible") is False,
         "decision closure")
    terminal = decision.get("actual_v2_terminal"); need(type(terminal) is dict
        and type(terminal.get("files")) is dict, "actual terminal map")
    terminal_dir = inside(terminal.get("terminal_dir", ""))
    actual_files = {terminal_dir / name for name in terminal["files"]}
    for path in actual_files:
        need(rec(path)["sha256"] == terminal["files"][path.name],
             "actual terminal current pin")

    candidate = inside(a.candidate_dir); need(candidate.is_dir()
        and {x.name for x in candidate.iterdir()} == CANDIDATE, "candidate inventory")
    result, result_record = doc(candidate / "result.json", "result_sha256")
    need(result.get("exact_census") == EXPECTED and result.get("formal_credit") == 0,
         "candidate result")
    candidate_hashes = {name: rec(candidate / name)["sha256"] for name in CANDIDATE}

    old = inside(a.historical_terminal_dir)
    need(old.is_dir() and {x.name for x in old.iterdir()} == OLD_TERMINAL,
         "historical terminal inventory")
    old_receipt, old_rr = doc(old / "terminal_receipt.json",
                              "terminal_receipt_sha256")
    old_replay, old_rp = doc(old / "terminal_replay.json",
                             "terminal_replay_sha256")
    old_payload = manifest(old / "payload_manifest.sha256")
    old_root = manifest(old / "root_manifest.sha256")
    need(rec(old / "root_manifest.sha256")["sha256"] == a.expect_old_root_sha256
         and old_rr["sha256"] == a.expect_old_receipt_file_sha256
         and old_receipt["terminal_receipt_sha256"]
             == a.expect_old_receipt_object_sha256
         and old_rp["sha256"] == a.expect_old_replay_file_sha256
         and old_replay["terminal_replay_sha256"] == a.expect_old_replay_object_sha256
         and rec(old / "PASS.lock")["sha256"] == a.expect_old_pass_sha256,
         "historical terminal pins")
    for name, value in candidate_hashes.items():
        shown = str((candidate / name).relative_to(ROOT))
        need(shown in old_payload and old_payload[shown]["sha256"] == value,
             "historical same candidate:" + name)
    core_path = inside(a.core_receipt)
    need(rec(core_path)["sha256"] == a.expect_core_receipt_file_sha256
         and str(core_path.relative_to(ROOT)) in old_root
         and old_root[str(core_path.relative_to(ROOT))]["sha256"]
             == a.expect_core_receipt_file_sha256, "historical same core")

    verification = inside(a.verification); attacks = inside(a.core_attacks)
    payload_files = {inside(path) for path in inv}
    payload_files |= {post_dir / "post_attack_evidence.json", inv_path,
        snapshot_dir / "snapshot_evidence.json",
        snapshot_dir / "current_snapshot_inventory.sha256", decision_path,
        verification, attacks, SELF, core_path}
    payload_files |= {candidate / name for name in CANDIDATE}
    for raw in a.source_file: payload_files.add(inside(raw))
    need(not any(str(path).startswith(str(old)) for path in payload_files),
         "historical terminal excluded from payload")
    output = inside(a.output_dir, True); need(not output.exists(), "fresh output")
    output.mkdir(parents=True, mode=0o700)
    payload_path = output / "payload_manifest.sha256"
    write(payload_path, manifest_bytes(payload_files))
    root_files = actual_files | {payload_path, SELF}
    root_path = output / "root_manifest.sha256"
    write(root_path, manifest_bytes(root_files))
    historical = {"root_manifest_file_sha256": a.expect_old_root_sha256,
        "terminal_receipt_file_sha256": a.expect_old_receipt_file_sha256,
        "terminal_receipt_object_sha256": a.expect_old_receipt_object_sha256,
        "terminal_replay_file_sha256": a.expect_old_replay_file_sha256,
        "terminal_replay_object_sha256": a.expect_old_replay_object_sha256,
        "PASS_lock_file_sha256": a.expect_old_pass_sha256,
        "role": "HISTORICAL_AUDIT_HOLD", "authority_eligible": False,
        "included_in_payload": False, "included_in_authority_root": False,
        "same_core_receipt_file_sha256": a.expect_core_receipt_file_sha256,
        "same_core_receipt_object_sha256": a.expect_core_receipt_object_sha256,
        "same_candidate_file_sha256": candidate_hashes}
    body = {"schema": MANIFEST_SCHEMA, "status": MANIFEST_STATUS,
        "completed_at_utc": datetime.now(timezone.utc).isoformat(
            timespec="microseconds").replace("+00:00", "Z"),
        "post_attack_evidence_file_sha256": pr["sha256"],
        "post_attack_evidence_object_sha256": post["post_attack_evidence_sha256"],
        "snapshot_evidence_file_sha256": sr["sha256"],
        "snapshot_evidence_object_sha256": snapshot["snapshot_evidence_sha256"],
        "payload_manifest_file_sha256": rec(payload_path)["sha256"],
        "payload_member_count": len(payload_files),
        "root_manifest_file_sha256": rec(root_path)["sha256"],
        "root_member_count": len(root_files),
        "core_receipt_file_sha256": a.expect_core_receipt_file_sha256,
        "core_receipt_object_sha256": a.expect_core_receipt_object_sha256,
        "candidate_result_file_sha256": result_record["sha256"],
        "candidate_result_object_sha256": result["result_sha256"],
        "candidate_file_sha256": candidate_hashes,
        "actual_v2_terminal_role": "PREDECESSOR_EVIDENCE_ONLY",
        "actual_v2_terminal_authority_eligible": False,
        "historical_C27R2_terminal": historical,
        "real_case_count": 44, "exact_math": EXPECTED, "formal_credit": 0,
        "manifest_authorized": False, "authority_minted": False,
        "C27R2": "AUDIT_HOLD_UNAUTHORIZED", "C28_C29": "UNAUTHORIZED",
        "CM2": "NO-GO_FOR_CLAIM"}
    result_out = {**body, "manifest_receipt_sha256": digest(body)}
    write(output / "manifest_receipt.json", canonical(result_out) + b"\n")
    need({x.name for x in output.iterdir()} == {"manifest_receipt.json",
        "payload_manifest.sha256", "root_manifest.sha256"}, "output inventory")
    return result_out


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__); p.add_argument("--self-test", action="store_true")
    names = ("post-evidence-dir", "snapshot-dir", "trust-decision",
        "decision-closure-key", "expect-decision-schema", "expect-decision-status",
        "candidate-dir", "verification", "core-attacks", "core-receipt",
        "historical-terminal-dir", "output-dir", "expect-self-sha256",
        "expect-post-file-sha256", "expect-post-object-sha256",
        "expect-snapshot-file-sha256", "expect-snapshot-object-sha256",
        "expect-decision-file-sha256", "expect-decision-object-sha256",
        "expect-old-root-sha256", "expect-old-receipt-file-sha256",
        "expect-old-receipt-object-sha256", "expect-old-replay-file-sha256",
        "expect-old-replay-object-sha256", "expect-old-pass-sha256",
        "expect-core-receipt-file-sha256", "expect-core-receipt-object-sha256")
    for name in names: p.add_argument("--" + name)
    p.add_argument("--source-file", action="append"); return p


def main() -> int:
    p = parser(); a = p.parse_args(); names = [x.dest for x in p._actions
        if x.dest not in {"help", "self_test", "source_file"}]
    try:
        if a.self_test:
            need(all(getattr(a, x) is None for x in names)
                 and a.source_file is None, "self-test no args")
            need(EXPECTED["frozen_C15_components"]
                 - EXPECTED["successful_DSU_merges"]
                 == EXPECTED["post_C27R2_components"], "fixture")
            out = {"status": "PASS_C27R2_RELEASE_REPAIR_MANIFEST_V3_SELF_TEST"}
        else:
            need(all(getattr(a, x) is not None for x in names)
                 and type(a.source_file) is list and a.source_file,
                 "all dynamic inputs required")
            out = execute(a)
        sys.stdout.buffer.write(canonical({"CM2": "NO-GO_FOR_CLAIM",
            "formal_credit": 0, "status": out["status"]}) + b"\n"); return 0
    except (Blocked, OSError, ValueError, KeyError, TypeError) as e:
        sys.stderr.write("REJECT:" + str(e) + "\n"); return 2


if __name__ == "__main__": raise SystemExit(main())
