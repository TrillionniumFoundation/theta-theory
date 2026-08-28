#!/usr/bin/env python3
"""Close C27R2 repair evidence after baseline, 44 real cases and replay.

Stage B reopens the immutable Stage-A snapshot, a clean baseline validator
transaction, every one of 44 real isolated process transcripts, and a clean
post-attack validator replay.  It proves current SHA/9-stat identity and
cleanup before authorizing the manifest stage.  It emits no manifest or PASS.
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
POST_STATUS = ("PASS_C27R2_RELEASE_REPAIR_SNAPSHOT_BASELINE_44_REAL_CASES_"
               "POST_REPLAY_CURRENT_SHA_STAT_AND_CLEANUP_CLOSED__ZERO_"
               "CREDIT_PENDING_MANIFEST")
RUN_FILES = {"PASS.lock", "exit_code.txt", "input_post.json",
             "input_pre.json", "output_validation.json",
             "run_attestation.json", "runner_start.json", "signal.json",
             "stderr.log", "stdout.log", "timing.json"}
EXPECTED = {"frozen_C15_components": 57_876,
            "post_C27R2_components": 43_684,
            "proof_derived_component_edges": 14_860,
            "successful_DSU_merges": 14_192, "cycle_edges": 668,
            "frozen_C15_members": 502_204,
            "total_unordered_member_pairs": 126_104_177_706,
            "within_post_component_member_pairs": 542_179_508,
            "cross_post_component_member_pairs": 125_561_998_198}


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


def process(path: Path) -> dict[str, Any]:
    need(path.is_dir() and not path.is_symlink()
         and {x.name for x in path.iterdir()} == RUN_FILES, "process inventory")
    need((path / "exit_code.txt").read_bytes() == b"0\n"
         and (path / "stderr.log").read_bytes() == b""
         and strict((path / "signal.json").read_bytes()[:-1]) is None,
         "process scalars")
    run, rr = doc(path / "run_attestation.json", "run_attestation_sha256")
    need(run.get("numeric_exit_code") == 0 and run.get("signal") is None
         and run.get("timed_out") is False and run.get("stderr_empty") is True
         and run.get("input_pre_post_sha_stat_identical",
                     run.get("input_pre_post_identical")) is True
         and run.get("formal_credit") == 0
         and (path / "input_pre.json").read_bytes()
             == (path / "input_post.json").read_bytes(), "process semantics")
    return rr


def inventory(path: Path) -> list[Path]:
    raw = path.read_bytes(); need(raw.endswith(b"\n"), "inventory newline")
    out: list[Path] = []; names: list[str] = []
    for line in raw.decode("ascii").splitlines():
        m = re.fullmatch(r"([0-9a-f]{64})  ([^\x00\r\n]+)", line)
        need(m is not None, "inventory line"); claim, shown = m.groups()
        need(shown not in names, "duplicate inventory path")
        p = inside(shown); need(rec(p)["sha256"] == claim, "current SHA")
        names.append(shown); out.append(p)
    need(out and names == sorted(names), "sorted inventory")
    return out


def add_tree(paths: set[Path], root: Path) -> None:
    need(root.is_dir() and not root.is_symlink(), "tree root")
    for current, dirs, files in os.walk(root):
        base = Path(current)
        for name in dirs: need(not (base / name).is_symlink(), "tree symlink")
        for name in files: paths.add(base / name)


def pinned_doc(path: str, closure: str, schema: str, status: str,
               file_pin: str, object_pin: str) -> tuple[dict[str, Any], Path]:
    p = inside(path); value, r = doc(p, closure)
    need(r["sha256"] == file_pin and value[closure] == object_pin
         and value.get("schema") == schema and value.get("status") == status
         and value.get("mode") == "formal" and value.get("formal_credit") == 0
         and value.get("manifest_authorized") is False, "pinned formal doc")
    return value, p


def execute(a: argparse.Namespace) -> dict[str, Any]:
    sha_fields = (a.expect_self_sha256, a.expect_snapshot_file_sha256,
        a.expect_snapshot_object_sha256, a.expect_baseline_file_sha256,
        a.expect_baseline_object_sha256, a.expect_cases_file_sha256,
        a.expect_cases_object_sha256, a.expect_post_file_sha256,
        a.expect_post_object_sha256)
    need(all(sha(x) for x in sha_fields) and rec(SELF)["sha256"]
         == a.expect_self_sha256, "SHA/self pins")
    strings = (a.baseline_closure_key, a.expect_baseline_schema,
        a.expect_baseline_status, a.cases_closure_key, a.expect_cases_schema,
        a.expect_cases_status, a.post_closure_key, a.expect_post_schema,
        a.expect_post_status)
    need(all(type(x) is str and x for x in strings), "dynamic strings")

    snapshot_dir = inside(a.snapshot_dir)
    snapshot, sr = doc(snapshot_dir / "snapshot_evidence.json",
                       "snapshot_evidence_sha256")
    snapshot_inventory_path = snapshot_dir / "current_snapshot_inventory.sha256"
    snapshot_paths = inventory(snapshot_inventory_path)
    need(sr["sha256"] == a.expect_snapshot_file_sha256
         and snapshot["snapshot_evidence_sha256"]
             == a.expect_snapshot_object_sha256
         and snapshot.get("schema") == SNAPSHOT_SCHEMA
         and snapshot.get("attack_credit_claimed") is False
         and snapshot.get("fresh_cold") is True
         and snapshot.get("current_snapshot_inventory_file_sha256")
             == rec(snapshot_inventory_path)["sha256"]
         and snapshot.get("current_snapshot_inventory_member_count")
             == len(snapshot_paths) and snapshot.get("exact_math") == EXPECTED
         and snapshot.get("formal_credit") == 0, "snapshot closure")

    baseline, baseline_path = pinned_doc(a.baseline_receipt,
        a.baseline_closure_key, a.expect_baseline_schema, a.expect_baseline_status,
        a.expect_baseline_file_sha256, a.expect_baseline_object_sha256)
    need(baseline.get("baseline_accepted") is True
         and baseline.get("authority_pre_sha_stat_captured") is True,
         "baseline semantics")
    process(inside(a.baseline_run)); baseline_inventory = inventory(
        inside(a.baseline_inventory))

    cases, cases_path = pinned_doc(a.cases_receipt, a.cases_closure_key,
        a.expect_cases_schema, a.expect_cases_status,
        a.expect_cases_file_sha256, a.expect_cases_object_sha256)
    case_dirs = cases.get("case_process_directories")
    need(cases.get("case_count") == 44 and cases.get("rejected_count") == 44
         and cases.get("accepted_count", 0) == 0
         and cases.get("real_process_execution_count") == 44
         and cases.get("authoritative_inputs_pre_post_sha_stat_identical") is True
         and cases.get("case_workdirs_cleaned") is True
         and type(case_dirs) is list and len(case_dirs) == 44
         and len(set(case_dirs)) == 44, "44 real-case semantics")
    case_runs = [inside(x) for x in case_dirs]
    for run in case_runs: process(run)
    process(inside(a.cases_run)); cases_inventory = inventory(
        inside(a.cases_inventory))

    post, post_path = pinned_doc(a.post_receipt, a.post_closure_key,
        a.expect_post_schema, a.expect_post_status,
        a.expect_post_file_sha256, a.expect_post_object_sha256)
    need(post.get("baseline_equivalent") is True
         and post.get("authority_pre_post_sha_stat_identical") is True
         and post.get("cleanup_complete") is True
         and post.get("remaining_case_workdirs") == 0,
         "post-attack semantics")
    process(inside(a.post_run)); post_inventory = inventory(inside(a.post_inventory))

    # This is the decisive pre/post reopen: every Stage-A byte is current now.
    for path in snapshot_paths: rec(path)
    paths: set[Path] = {SELF, snapshot_dir / "snapshot_evidence.json",
        snapshot_inventory_path, baseline_path, cases_path, post_path}
    paths.update(snapshot_paths + baseline_inventory + cases_inventory + post_inventory)
    for root in (inside(a.baseline_run), inside(a.cases_run), inside(a.post_run),
                 *case_runs, baseline_path.parent, cases_path.parent, post_path.parent):
        add_tree(paths, root)
    current = [rec(path) for path in sorted(paths)]
    raw = "".join(f"{x['sha256']}  {x['path']}\n" for x in current).encode("ascii")
    output = inside(a.output_dir, True); need(not output.exists(), "fresh output")
    output.mkdir(parents=True, mode=0o700)
    inv = output / "authority_inventory.sha256"
    fd = os.open(inv, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o400)
    try: os.write(fd, raw); os.fsync(fd)
    finally: os.close(fd)
    body = {"schema": POST_SCHEMA, "status": POST_STATUS,
        "completed_at_utc": datetime.now(timezone.utc).isoformat(
            timespec="microseconds").replace("+00:00", "Z"),
        "snapshot_evidence_file_sha256": sr["sha256"],
        "snapshot_evidence_object_sha256": snapshot["snapshot_evidence_sha256"],
        "baseline_receipt_file_sha256": rec(baseline_path)["sha256"],
        "baseline_receipt_object_sha256": baseline[a.baseline_closure_key],
        "cases_receipt_file_sha256": rec(cases_path)["sha256"],
        "cases_receipt_object_sha256": cases[a.cases_closure_key],
        "post_receipt_file_sha256": rec(post_path)["sha256"],
        "post_receipt_object_sha256": post[a.post_closure_key],
        "real_case_count": 44, "real_cases_rejected": 44,
        "case_process_transcripts_reopened": 44,
        "snapshot_current_after_cases": True,
        "authority_pre_post_sha_stat_identical": True,
        "case_cleanup_complete": True,
        "authority_inventory_file_sha256": rec(inv)["sha256"],
        "authority_inventory_member_count": len(current),
        "actual_v2_terminal_role": "PREDECESSOR_EVIDENCE_ONLY",
        "historical_C27R2_terminal_authority_eligible": False,
        "exact_math": EXPECTED, "formal_credit": 0,
        "manifest_authorized": False, "authority_minted": False,
        "C27R2": "AUDIT_HOLD_UNAUTHORIZED", "C28_C29": "UNAUTHORIZED",
        "CM2": "NO-GO_FOR_CLAIM"}
    result = {**body, "post_attack_evidence_sha256": digest(body)}
    out = output / "post_attack_evidence.json"
    fd = os.open(out, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o400)
    try: os.write(fd, canonical(result) + b"\n"); os.fsync(fd)
    finally: os.close(fd)
    need({x.name for x in output.iterdir()} == {inv.name, out.name},
         "output inventory")
    return result


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__); p.add_argument("--self-test", action="store_true")
    names = ("snapshot-dir", "baseline-receipt", "baseline-run",
        "baseline-inventory", "cases-receipt", "cases-run", "cases-inventory",
        "post-receipt", "post-run", "post-inventory", "output-dir",
        "baseline-closure-key", "cases-closure-key", "post-closure-key",
        "expect-baseline-schema", "expect-baseline-status", "expect-cases-schema",
        "expect-cases-status", "expect-post-schema", "expect-post-status",
        "expect-self-sha256", "expect-snapshot-file-sha256",
        "expect-snapshot-object-sha256", "expect-baseline-file-sha256",
        "expect-baseline-object-sha256", "expect-cases-file-sha256",
        "expect-cases-object-sha256", "expect-post-file-sha256",
        "expect-post-object-sha256")
    for name in names: p.add_argument("--" + name)
    return p


def main() -> int:
    p = parser(); a = p.parse_args(); names = [x.dest for x in p._actions
        if x.dest not in {"help", "self_test"}]
    try:
        if a.self_test:
            need(all(getattr(a, x) is None for x in names), "self-test no args")
            need(44 > 0 and EXPECTED["proof_derived_component_edges"]
                 - EXPECTED["successful_DSU_merges"] == EXPECTED["cycle_edges"],
                 "fixture")
            result = {"status": "PASS_C27R2_POST_ATTACK_EVIDENCE_V3_SELF_TEST"}
        else:
            need(all(getattr(a, x) is not None for x in names), "all pins required")
            result = execute(a)
        sys.stdout.buffer.write(canonical({"CM2": "NO-GO_FOR_CLAIM",
            "formal_credit": 0, "status": result["status"]}) + b"\n"); return 0
    except (Blocked, OSError, ValueError, KeyError, TypeError) as e:
        sys.stderr.write("REJECT:" + str(e) + "\n"); return 2


if __name__ == "__main__": raise SystemExit(main())
