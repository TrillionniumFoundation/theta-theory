#!/usr/bin/env python3
"""Fail-closed watcher skeleton for the C27R2 release-repair v3 chain.

This development source validates a fully pinned future plan and the exact
stage order but intentionally has no execution path.  A later audited watcher
must implement each transaction handoff.  It never creates run/output paths,
services, receipts, seals, terminals, or PASS markers.
"""

from __future__ import annotations

import argparse
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
PLAN_SCHEMA = BASE + "chain-plan.v3"
PLAN_STATUS = ("FROZEN_C27R2_RELEASE_REPAIR_PLAN__EXECUTION_DISABLED_PENDING_"
               "INDEPENDENT_FULL_CHAIN_AUDIT")
STAGES = ["boundary_preflight", "fresh_cold_transaction",
          "current_snapshot_evidence_v2", "baseline_validator_transaction",
          "forty_four_real_case_transactions", "post_attack_validator_replay",
          "post_attack_evidence_v3", "manifest_v3", "outer_full_ledger_v3",
          "conditional_seal_v3", "independent_terminal_byte_replay_v3"]
SOURCE_ROLES = ["python", "transaction_runner", "cold_runner",
    "boundary_validator", "real_case_harness", "trust_decision_auditor",
    "snapshot_builder", "post_attack_builder", "manifest_builder",
    "outer_verifier", "seal_builder", "terminal_replay", "watcher"]
CORE_FILE = "4104edc46bb130bae530a990609d5053bc9d7f675e4e3587e88b8327394c5796"
CORE_OBJECT = "783d05cb9c01a2049a03112f9412bab787b5fad2c81fba1855d9cca4dabcb016"


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


def file_sha(path: Path) -> str:
    need(path.is_file() and not path.is_symlink(), "regular source")
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd); need(stat.S_ISREG(before.st_mode)
            and before.st_nlink == 1, "single-link source")
        h = hashlib.sha256()
        while block := os.read(fd, 1 << 20): h.update(block)
        need(fp(os.stat(path, follow_symlinks=False)) == fp(before), "stable source")
        return h.hexdigest()
    finally: os.close(fd)


def plan(path: Path, closure: str) -> dict[str, Any]:
    raw = path.read_bytes(); need(raw.endswith(b"\n"), "plan newline")
    value = strict(raw[:-1]); need(type(value) is dict
        and canonical(value) == raw[:-1], "canonical plan")
    body = dict(value); claim = body.pop(closure, None)
    need(sha(claim) and claim == digest(body), "plan closure"); return value


def execute(a: argparse.Namespace) -> dict[str, Any]:
    need(sha(a.expect_self_sha256) and file_sha(SELF) == a.expect_self_sha256,
         "watcher self pin")
    need(sha(a.expect_plan_file_sha256) and sha(a.expect_plan_object_sha256)
         and type(a.plan_closure_key) is str and a.plan_closure_key,
         "plan pins")
    plan_path = inside(a.plan)
    value = plan(plan_path, a.plan_closure_key)
    need(file_sha(plan_path) == a.expect_plan_file_sha256
         and value[a.plan_closure_key] == a.expect_plan_object_sha256
         and value.get("schema") == PLAN_SCHEMA and value.get("status") == PLAN_STATUS
         and value.get("stages") == STAGES and value.get("case_count") == 44
         and value.get("core_receipt_file_sha256") == CORE_FILE
         and value.get("core_receipt_object_sha256") == CORE_OBJECT
         and value.get("execution_enabled") is False
         and value.get("formal_credit") == 0
         and value.get("manifest_authorized") is False
         and value.get("CM2") == "NO-GO_FOR_CLAIM", "frozen disabled plan")
    sources = value.get("sources")
    need(type(sources) is dict and set(sources) == set(SOURCE_ROLES),
         "exact source roles")
    for role in SOURCE_ROLES:
        item = sources[role]
        need(type(item) is dict and sha(item.get("sha256")), "source pin:" + role)
        path = SELF if role == "watcher" else inside(item.get("path", ""))
        need(file_sha(path) == item["sha256"], "current source:" + role)
    fresh = value.get("fresh_paths")
    need(type(fresh) is dict and set(fresh) == set(STAGES), "fresh path roles")
    resolved = [inside(fresh[stage], True) for stage in STAGES]
    need(len(set(resolved)) == len(resolved)
         and all(path.parent == AUDIT and not path.exists() and not path.is_symlink()
                 for path in resolved), "fresh distinct audit paths")
    # Deliberately fail closed: v3 is a plan validator, not a launch authority.
    return {"schema": BASE + "watcher-skeleton-preflight.v3",
        "status": "PASS_DISABLED_PLAN_SOURCE_PIN_AND_FRESH_PATH_PREFLIGHT__NO_OUTPUT_CREATED",
        "stage_order": STAGES, "case_count": 44,
        "execution_enabled": False, "formal_credit": 0,
        "manifest_authorized": False, "authority_minted": False,
        "C27R2": "AUDIT_HOLD_UNAUTHORIZED", "C28_C29": "UNAUTHORIZED",
        "CM2": "NO-GO_FOR_CLAIM"}


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__); p.add_argument("--self-test", action="store_true")
    p.add_argument("--preflight-only", action="store_true")
    p.add_argument("--plan"); p.add_argument("--plan-closure-key")
    p.add_argument("--expect-plan-file-sha256")
    p.add_argument("--expect-plan-object-sha256")
    p.add_argument("--expect-self-sha256"); return p


def main() -> int:
    p = parser(); a = p.parse_args()
    fields = ("plan", "plan_closure_key", "expect_plan_file_sha256",
              "expect_plan_object_sha256", "expect_self_sha256")
    try:
        if a.self_test:
            need(not a.preflight_only and all(getattr(a, x) is None for x in fields),
                 "self-test no args")
            need(len(STAGES) == 11 and STAGES[-1]
                 == "independent_terminal_byte_replay_v3"
                 and CORE_FILE != CORE_OBJECT, "plan fixture")
            out = {"status": "PASS_C27R2_REPAIR_WATCHER_SKELETON_V3_SELF_TEST"}
        else:
            need(a.preflight_only and all(getattr(a, x) is not None for x in fields),
                 "only fully pinned preflight-only is implemented")
            out = execute(a)
        sys.stdout.buffer.write(canonical({"CM2": "NO-GO_FOR_CLAIM",
            "formal_credit": 0, "status": out["status"]}) + b"\n"); return 0
    except (Blocked, OSError, ValueError, KeyError, TypeError) as e:
        sys.stderr.write("REJECT:" + str(e) + "\n"); return 2


if __name__ == "__main__": raise SystemExit(main())
