#!/usr/bin/env python3
"""Freeze pre-attack current-byte evidence for the C27R2 repair.

Stage A runs only after a fresh cold transaction and an approved boundary
preflight/trust decision.  It grants no attack credit and cannot authorize a
manifest.  Stage B must later reopen this inventory after the baseline,
44 real cases and post-attack validator replay.
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
SNAPSHOT_SCHEMA = BASE + "current-snapshot-evidence.v2"
SNAPSHOT_STATUS = ("PASS_C27R2_RELEASE_REPAIR_CORE_FRESH_COLD_BOUNDARY_"
                   "PREFLIGHT_TRUST_AND_CURRENT_INVENTORY_FROZEN__ZERO_"
                   "CREDIT_NOT_MANIFEST_AUTHORIZED")
CORE_SCHEMA = ("cm2.round306c27r2.source-g-actual-v2-fresh-quotient-"
               "rebuild.v2.gated-dual-seed-transaction-receipt.v4")
CORE_STATUS = ("PASS_GATE_SEED1_FOUR_FILE_CANDIDATE_SEED2_NO_IMPORT_REPLAY_"
               "AND_21_ATTACKS__ZERO_CREDIT_PENDING_OUTER_SEAL_AND_"
               "TERMINAL_REPLAY")
CORE_PASS = b"PASS_C27R2_AUTHORITY_V2_GATED_DUAL_SEED_CORE__ZERO_CREDIT\n"
RUN_FILES = {"PASS.lock", "exit_code.txt", "input_post.json",
             "input_pre.json", "output_validation.json",
             "run_attestation.json", "runner_start.json", "signal.json",
             "stderr.log", "stdout.log", "timing.json"}
CORE_TARGETS = ("producer_run", "verifier_run", "attack_run")
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


def valid_sha(v: Any) -> bool:
    return type(v) is str and re.fullmatch(r"[0-9a-f]{64}", v) is not None


def strict(raw: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for k, v in items: need(k not in out, "duplicate JSON key"); out[k] = v
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
    need(valid_sha(claim) and claim == digest(body), "object closure")
    return v, r


def process(path: Path) -> dict[str, Any]:
    need(path.is_dir() and not path.is_symlink()
         and {x.name for x in path.iterdir()} == RUN_FILES, "run inventory")
    need((path / "exit_code.txt").read_bytes() == b"0\n"
         and (path / "stderr.log").read_bytes() == b""
         and strict((path / "signal.json").read_bytes()[:-1]) is None,
         "run scalars")
    run, rr = doc(path / "run_attestation.json", "run_attestation_sha256")
    need(run.get("numeric_exit_code") == 0 and run.get("signal") is None
         and run.get("timed_out") is False and run.get("stderr_empty") is True
         and run.get("input_pre_post_sha_stat_identical",
                     run.get("input_pre_post_identical")) is True
         and run.get("formal_credit") == 0
         and (path / "input_pre.json").read_bytes()
             == (path / "input_post.json").read_bytes(), "run semantics")
    return rr


def inventory(path: Path) -> list[Path]:
    raw = path.read_bytes(); need(raw.endswith(b"\n"), "inventory newline")
    answer: list[Path] = []; shown: list[str] = []
    for line in raw.decode("ascii").splitlines():
        m = re.fullmatch(r"([0-9a-f]{64})  ([^\x00\r\n]+)", line)
        need(m is not None, "inventory line"); claim, name = m.groups()
        need(name not in shown, "inventory duplicate")
        p = inside(name); need(rec(p)["sha256"] == claim, "inventory current SHA")
        shown.append(name); answer.append(p)
    need(answer and shown == sorted(shown), "sorted inventory")
    return answer


def add_tree(paths: set[Path], root: Path) -> None:
    need(root.is_dir() and not root.is_symlink(), "tree root")
    for current, dirs, files in os.walk(root):
        base = Path(current)
        for name in dirs: need(not (base / name).is_symlink(), "tree symlink")
        for name in files: paths.add(base / name)


def execute(a: argparse.Namespace) -> dict[str, Any]:
    shas = (a.expect_self_sha256, a.expect_core_receipt_file_sha256,
        a.expect_core_receipt_object_sha256, a.expect_cold_receipt_file_sha256,
        a.expect_cold_receipt_object_sha256, a.expect_boundary_file_sha256,
        a.expect_boundary_object_sha256, a.expect_decision_file_sha256,
        a.expect_decision_object_sha256)
    need(all(valid_sha(x) for x in shas) and rec(SELF)["sha256"]
         == a.expect_self_sha256, "all SHA/self pins")
    strings = (a.cold_closure_key, a.expect_cold_schema, a.expect_cold_status,
        a.boundary_closure_key, a.expect_boundary_schema, a.expect_boundary_status,
        a.decision_closure_key, a.expect_decision_schema, a.expect_decision_status)
    need(all(type(x) is str and x for x in strings), "dynamic string pins")

    control = inside(a.core_control)
    core, cr = doc(control / "transaction_receipt.json",
                   "transaction_receipt_sha256")
    pinset, _ = doc(control / "pinset.json", "pinset_sha256")
    need(cr["sha256"] == a.expect_core_receipt_file_sha256
         and core["transaction_receipt_sha256"]
             == a.expect_core_receipt_object_sha256
         and core.get("schema") == CORE_SCHEMA and core.get("status") == CORE_STATUS
         and core.get("formal_credit") == 0
         and (control / "PASS.lock").read_bytes() == CORE_PASS, "core boundary")
    targets = pinset.get("targets"); need(type(targets) is dict
        and set(CORE_TARGETS) <= set(targets), "core targets")
    for name in CORE_TARGETS: process(inside(targets[name]))

    cold_path = inside(a.cold_receipt)
    cold, cold_r = doc(cold_path, a.cold_closure_key)
    need(cold_r["sha256"] == a.expect_cold_receipt_file_sha256
         and cold[a.cold_closure_key] == a.expect_cold_receipt_object_sha256
         and cold.get("schema") == a.expect_cold_schema
         and cold.get("status") == a.expect_cold_status
         and cold.get("formal_credit") == 0
         and cold.get("formal_verification_byte_identical") is True
         and cold.get("all_core_inputs_pre_post_sha_stat_identical") is True,
         "fresh cold receipt")
    process(inside(a.cold_run))

    boundary_path = inside(a.boundary_preflight_receipt)
    boundary, br = doc(boundary_path, a.boundary_closure_key)
    need(br["sha256"] == a.expect_boundary_file_sha256
         and boundary[a.boundary_closure_key] == a.expect_boundary_object_sha256
         and boundary.get("schema") == a.expect_boundary_schema
         and boundary.get("status") == a.expect_boundary_status
         and boundary.get("mode") in {"formal-preflight", "formal"}
         and boundary.get("formal_credit") == 0
         and boundary.get("manifest_authorized") is False,
         "boundary preflight")
    process(inside(a.boundary_run)); boundary_inventory = inventory(
        inside(a.boundary_inventory))

    decision_path = inside(a.trust_decision)
    decision, dr = doc(decision_path, a.decision_closure_key)
    need(dr["sha256"] == a.expect_decision_file_sha256
         and decision[a.decision_closure_key] == a.expect_decision_object_sha256
         and decision.get("schema") == a.expect_decision_schema
         and decision.get("status") == a.expect_decision_status
         and decision.get("semantic_projection_attacks_only") is True
         and decision.get("process_and_cold_current_byte_closure_verified") is True
         and decision.get("eligible_as_predecessor_evidence") is True
         and decision.get("authority_eligible") is False
         and decision.get("old_C27R2_authority_eligible") is False
         and decision.get("formal_credit") == 0
         and decision.get("CM2") == "NO-GO_FOR_CLAIM", "trust decision")
    process(inside(a.decision_run)); decision_inventory = inventory(
        inside(a.decision_inventory))

    paths: set[Path] = {SELF, cold_path, boundary_path, decision_path}
    for root in (control, *(inside(targets[x]) for x in CORE_TARGETS),
                 cold_path.parent, inside(a.cold_run), boundary_path.parent,
                 inside(a.boundary_run), decision_path.parent, inside(a.decision_run)):
        add_tree(paths, root)
    paths.update(boundary_inventory + decision_inventory)
    auth = pinset.get("actual_v2_authority"); need(type(auth) is dict
        and type(auth.get("authority_input_paths")) is list, "core authority inputs")
    paths.update(inside(x) for x in auth["authority_input_paths"])
    terminal = decision.get("actual_v2_terminal"); need(type(terminal) is dict
        and type(terminal.get("files")) is dict, "decision terminal map")
    terminal_dir = inside(terminal.get("terminal_dir", ""))
    paths.update(terminal_dir / name for name in terminal["files"])
    current = [rec(p) for p in sorted(paths)]
    raw = "".join(f"{x['sha256']}  {x['path']}\n" for x in current).encode("ascii")
    output = inside(a.output_dir, True); need(not output.exists(), "fresh output")
    output.mkdir(parents=True, mode=0o700)
    inv = output / "current_snapshot_inventory.sha256"
    fd = os.open(inv, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o400)
    try: os.write(fd, raw); os.fsync(fd)
    finally: os.close(fd)
    body = {"schema": SNAPSHOT_SCHEMA, "status": SNAPSHOT_STATUS,
        "completed_at_utc": datetime.now(timezone.utc).isoformat(
            timespec="microseconds").replace("+00:00", "Z"),
        "core_receipt_file_sha256": cr["sha256"],
        "core_receipt_object_sha256": core["transaction_receipt_sha256"],
        "cold_receipt_file_sha256": cold_r["sha256"],
        "cold_receipt_object_sha256": cold[a.cold_closure_key],
        "boundary_preflight_file_sha256": br["sha256"],
        "boundary_preflight_object_sha256": boundary[a.boundary_closure_key],
        "decision_file_sha256": dr["sha256"],
        "decision_object_sha256": decision[a.decision_closure_key],
        "current_snapshot_inventory_file_sha256": rec(inv)["sha256"],
        "current_snapshot_inventory_member_count": len(current),
        "fresh_cold": True, "attack_credit_claimed": False,
        "actual_v2_terminal_role": "PREDECESSOR_EVIDENCE_ONLY",
        "historical_C27R2_terminal_authority_eligible": False,
        "exact_math": EXPECTED, "formal_credit": 0,
        "manifest_authorized": False, "authority_minted": False,
        "C27R2": "AUDIT_HOLD_UNAUTHORIZED", "C28_C29": "UNAUTHORIZED",
        "CM2": "NO-GO_FOR_CLAIM"}
    result = {**body, "snapshot_evidence_sha256": digest(body)}
    out = output / "snapshot_evidence.json"
    fd = os.open(out, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o400)
    try: os.write(fd, canonical(result) + b"\n"); os.fsync(fd)
    finally: os.close(fd)
    need({x.name for x in output.iterdir()} == {inv.name, out.name},
         "snapshot inventory")
    return result


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__); p.add_argument("--self-test", action="store_true")
    names = ("core-control", "cold-receipt", "cold-run",
        "boundary-preflight-receipt", "boundary-run", "boundary-inventory",
        "trust-decision", "decision-run", "decision-inventory", "output-dir",
        "cold-closure-key", "boundary-closure-key", "decision-closure-key",
        "expect-cold-schema", "expect-cold-status", "expect-boundary-schema",
        "expect-boundary-status", "expect-decision-schema", "expect-decision-status",
        "expect-self-sha256", "expect-core-receipt-file-sha256",
        "expect-core-receipt-object-sha256", "expect-cold-receipt-file-sha256",
        "expect-cold-receipt-object-sha256", "expect-boundary-file-sha256",
        "expect-boundary-object-sha256", "expect-decision-file-sha256",
        "expect-decision-object-sha256")
    for name in names: p.add_argument("--" + name)
    return p


def main() -> int:
    p = parser(); a = p.parse_args(); names = [x.dest for x in p._actions
        if x.dest not in {"help", "self_test"}]
    try:
        if a.self_test:
            need(all(getattr(a, x) is None for x in names), "self-test no args")
            need(EXPECTED["frozen_C15_components"]
                 - EXPECTED["successful_DSU_merges"]
                 == EXPECTED["post_C27R2_components"], "math fixture")
            result = {"status": "PASS_C27R2_CURRENT_SNAPSHOT_EVIDENCE_V2_SELF_TEST"}
        else:
            need(all(getattr(a, x) is not None for x in names), "all pins required")
            result = execute(a)
        sys.stdout.buffer.write(canonical({"CM2": "NO-GO_FOR_CLAIM",
            "formal_credit": 0, "status": result["status"]}) + b"\n"); return 0
    except (Blocked, OSError, ValueError, KeyError, TypeError) as e:
        sys.stderr.write("REJECT:" + str(e) + "\n"); return 2


if __name__ == "__main__": raise SystemExit(main())
