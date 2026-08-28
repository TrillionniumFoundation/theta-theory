#!/usr/bin/env python3
"""Build the append-only C27R2 release-repair evidence bundle v2.

This is the first back-half stage.  It accepts only exact, dynamically pinned
front-half boundary, real-case and trust-anchor decisions.  The actual-v2
terminal may enter as predecessor *evidence* only; neither it nor the earlier
C27R2 terminal is treated as an authority.  This source cannot create a
manifest, seal, terminal receipt, or PASS lock.
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
CORE_SCHEMA = ("cm2.round306c27r2.source-g-actual-v2-fresh-quotient-"
               "rebuild.v2.gated-dual-seed-transaction-receipt.v4")
CORE_STATUS = ("PASS_GATE_SEED1_FOUR_FILE_CANDIDATE_SEED2_NO_IMPORT_REPLAY_"
               "AND_21_ATTACKS__ZERO_CREDIT_PENDING_OUTER_SEAL_AND_"
               "TERMINAL_REPLAY")
CORE_PASS = b"PASS_C27R2_AUTHORITY_V2_GATED_DUAL_SEED_CORE__ZERO_CREDIT\n"
EVIDENCE_SCHEMA = BASE + "evidence-bundle.v2"
EVIDENCE_STATUS = ("PASS_C27R2_RELEASE_REPAIR_CURRENT_CORE_BOUNDARY_REAL_"
                   "CASES_AND_TRUST_DECISION_REOPENED__ZERO_CREDIT_PENDING_"
                   "MANIFEST")
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
        answer: dict[str, Any] = {}
        for key, value in items:
            need(type(key) is str and key not in answer, "duplicate JSON key")
            answer[key] = value
        return answer
    return json.loads(raw, object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(Blocked(x)))


def inside(raw: str | Path, *, absent: bool = False,
           audit_only: bool = False) -> Path:
    supplied = Path(raw)
    path = (supplied if supplied.is_absolute() else ROOT / supplied).absolute()
    anchor = AUDIT if audit_only else ROOT
    try:
        relative = path.relative_to(anchor)
    except ValueError as error:
        raise Blocked("path outside allowed root") from error
    need(relative.parts and all(x not in {"", ".", ".."}
                                for x in relative.parts), "canonical path")
    cursor = anchor
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
        after = os.stat(path, follow_symlinks=False)
        need(fingerprint(after) == fingerprint(before), "stable current file")
        return {"path": str(path.relative_to(ROOT)),
                "sha256": state.hexdigest(), "size": before.st_size,
                "stat_fingerprint": fingerprint(before)}
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


def exact_dir(path: Path, names: set[str]) -> None:
    need(path.is_dir() and not path.is_symlink(), "directory")
    actual = {x.name for x in path.iterdir()}
    need(actual == names and all(x.is_file() and not x.is_symlink()
                                 for x in path.iterdir()), "exact inventory")


def process_transcript(path: Path) -> dict[str, Any]:
    exact_dir(path, RUN_FILES)
    need((path / "exit_code.txt").read_bytes() == b"0\n"
         and (path / "stderr.log").read_bytes() == b""
         and strict((path / "signal.json").read_bytes()[:-1]) is None,
         "clean process scalars")
    run, run_record = document(path / "run_attestation.json",
                               "run_attestation_sha256")
    need(run.get("numeric_exit_code") == 0 and run.get("signal") is None
         and run.get("timed_out") is False and run.get("stderr_empty") is True
         and run.get("formal_credit") == 0
         and run.get("input_pre_post_sha_stat_identical",
                     run.get("input_pre_post_identical")) is True,
         "process attestation semantics")
    pre_raw = (path / "input_pre.json").read_bytes()
    post_raw = (path / "input_post.json").read_bytes()
    need(pre_raw.endswith(b"\n") and post_raw.endswith(b"\n")
         and strict(pre_raw[:-1]) == strict(post_raw[:-1]), "process pre/post")
    return {"run_attestation": run_record,
            "inventory": [record(path / name) for name in sorted(RUN_FILES)]}


def parse_inventory(path: Path) -> list[dict[str, Any]]:
    raw = path.read_bytes()
    need(raw.endswith(b"\n"), "inventory newline")
    rows: list[dict[str, Any]] = []
    shown_paths: list[str] = []
    for line in raw.decode("ascii").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\x00\r\n]+)", line)
        need(match is not None, "inventory line")
        claim, shown = match.groups()
        need(shown not in shown_paths, "inventory duplicate")
        item = record(inside(shown))
        need(item["sha256"] == claim, "inventory current SHA")
        shown_paths.append(shown)
        rows.append(item)
    need(rows and shown_paths == sorted(shown_paths), "sorted nonempty inventory")
    return rows


def add_tree(paths: set[Path], root: Path) -> None:
    need(root.is_dir() and not root.is_symlink(), "tree root")
    for current, directories, files in os.walk(root):
        base = Path(current)
        need(not base.is_symlink(), "tree symlink root")
        for name in directories:
            need(not (base / name).is_symlink(), "tree symlink directory")
        for name in files:
            paths.add(base / name)


def decision_semantics(value: dict[str, Any], args: argparse.Namespace) -> list[Path]:
    need(value.get("schema") == args.expect_decision_schema
         and value.get("status") == args.expect_decision_status
         and value.get("decision_schema") == args.expect_decision_schema
         and value.get("decision_status") == args.expect_decision_status,
         "decision exact schema/status")
    scope = value.get("scope_claims_exact")
    need(type(scope) is dict
         and scope.get("actual_v2_terminal") == "PREDECESSOR_EVIDENCE_ONLY"
         and scope.get("historical_C27R2_terminal") == "HISTORICAL_AUDIT_ONLY"
         and scope.get("C27R2_release_repair") == "BACK_HALF_ONLY",
         "decision exact scope")
    need(value.get("semantic_projection_attacks_only") is True
         and value.get("process_and_cold_current_byte_closure_verified") is True
         and value.get("eligible_as_predecessor_evidence") is True
         and value.get("authority_eligible") is False
         and value.get("old_C27R2_authority_eligible") is False
         and value.get("formal_credit") == 0
         and value.get("CM2") == "NO-GO_FOR_CLAIM", "decision semantics")
    terminal = value.get("actual_v2_terminal")
    need(type(terminal) is dict, "actual-v2 terminal map")
    terminal_dir = inside(terminal.get("terminal_dir", ""), audit_only=True)
    expected_names = {"PASS.lock", "payload_manifest.sha256",
                      "root_manifest.sha256", "terminal_receipt.json",
                      "terminal_replay.json"}
    exact_dir(terminal_dir, expected_names)
    file_map = terminal.get("files")
    need(type(file_map) is dict and set(file_map) == expected_names
         and all(valid_sha(x) for x in file_map.values()), "terminal exact file map")
    actual = []
    for name in sorted(expected_names):
        item = record(terminal_dir / name)
        need(item["sha256"] == file_map[name], "terminal decision file pin:" + name)
        actual.append(terminal_dir / name)
    receipt, rr = document(terminal_dir / "terminal_receipt.json",
                           "terminal_receipt_sha256")
    replay_record = record(terminal_dir / "terminal_replay.json")
    need(rr["sha256"] == terminal.get("terminal_receipt_file_sha256")
         and receipt["terminal_receipt_sha256"]
             == terminal.get("terminal_receipt_object_sha256")
         and replay_record["sha256"] == terminal.get("terminal_replay_file_sha256")
         and record(terminal_dir / "root_manifest.sha256")["sha256"]
             == terminal.get("root_manifest_file_sha256")
         and record(terminal_dir / "PASS.lock")["sha256"]
             == terminal.get("PASS_lock_file_sha256")
         and receipt.get("formal_credit") == 0
         and receipt.get("manifest_authorized") is False,
         "terminal decision map closure")
    return actual


def execute(args: argparse.Namespace) -> dict[str, Any]:
    sha_args = (args.expect_self_sha256,
        args.expect_core_receipt_file_sha256, args.expect_core_receipt_object_sha256,
        args.expect_boundary_file_sha256, args.expect_boundary_object_sha256,
        args.expect_case_file_sha256, args.expect_case_object_sha256,
        args.expect_decision_file_sha256, args.expect_decision_object_sha256)
    need(all(valid_sha(x) for x in sha_args), "all dynamic SHA pins")
    need(record(SELF)["sha256"] == args.expect_self_sha256, "self pin")
    strings = (args.expect_boundary_schema, args.expect_boundary_status,
        args.boundary_closure_key, args.expect_case_schema, args.expect_case_status,
        args.case_closure_key, args.expect_decision_schema,
        args.expect_decision_status, args.decision_closure_key)
    need(all(type(x) is str and x for x in strings), "dynamic schema/status/closure pins")

    control = inside(args.core_control, audit_only=True)
    core, core_record = document(control / "transaction_receipt.json",
                                 "transaction_receipt_sha256")
    pinset, _ = document(control / "pinset.json", "pinset_sha256")
    need(core_record["sha256"] == args.expect_core_receipt_file_sha256
         and core["transaction_receipt_sha256"]
             == args.expect_core_receipt_object_sha256
         and core.get("schema") == CORE_SCHEMA and core.get("status") == CORE_STATUS
         and core.get("formal_credit") == 0
         and core.get("manifest_authorized") is False
         and (control / "PASS.lock").read_bytes() == CORE_PASS,
         "formal core boundary")
    targets = pinset.get("targets")
    need(type(targets) is dict and set(CORE_TARGETS) <= set(targets),
         "core process targets")
    core_runs = {name: process_transcript(inside(targets[name], audit_only=True))
                 for name in CORE_TARGETS}

    boundary_path = inside(args.boundary_receipt, audit_only=True)
    boundary, boundary_record = document(boundary_path, args.boundary_closure_key)
    need(boundary_record["sha256"] == args.expect_boundary_file_sha256
         and boundary[args.boundary_closure_key] == args.expect_boundary_object_sha256
         and boundary.get("schema") == args.expect_boundary_schema
         and boundary.get("status") == args.expect_boundary_status
         and boundary.get("mode") == "formal"
         and boundary.get("formal_credit") == 0
         and boundary.get("manifest_authorized") is False,
         "formal boundary receipt")
    boundary_inventory = parse_inventory(inside(args.boundary_inventory, audit_only=True))
    boundary_run = process_transcript(inside(args.boundary_run, audit_only=True))

    case_path = inside(args.case_receipt, audit_only=True)
    cases, case_record = document(case_path, args.case_closure_key)
    need(case_record["sha256"] == args.expect_case_file_sha256
         and cases[args.case_closure_key] == args.expect_case_object_sha256
         and cases.get("schema") == args.expect_case_schema
         and cases.get("status") == args.expect_case_status
         and cases.get("mode") == "formal"
         and type(cases.get("case_count", cases.get("total"))) is int
         and cases.get("case_count", cases.get("total")) > 0
         and cases.get("rejected_count", cases.get("rejected"))
             == cases.get("case_count", cases.get("total"))
         and cases.get("formal_credit") == 0
         and cases.get("manifest_authorized") is False,
         "real-case receipt")
    case_inventory = parse_inventory(inside(args.case_inventory, audit_only=True))
    case_run = process_transcript(inside(args.case_run, audit_only=True))

    decision_path = inside(args.trust_decision, audit_only=True)
    decision, decision_record = document(decision_path, args.decision_closure_key)
    need(decision_record["sha256"] == args.expect_decision_file_sha256
         and decision[args.decision_closure_key]
             == args.expect_decision_object_sha256, "trust decision pins")
    terminal_files = decision_semantics(decision, args)
    decision_inventory = parse_inventory(inside(args.decision_inventory,
                                                audit_only=True))
    decision_run = process_transcript(inside(args.decision_run, audit_only=True))

    paths: set[Path] = {SELF, boundary_path, case_path, decision_path}
    for tree in (control, *(inside(targets[name], audit_only=True)
                            for name in CORE_TARGETS),
                 boundary_path.parent, inside(args.boundary_run, audit_only=True),
                 case_path.parent, inside(args.case_run, audit_only=True),
                 decision_path.parent, inside(args.decision_run, audit_only=True)):
        add_tree(paths, tree)
    for manifest_rows in (boundary_inventory, case_inventory, decision_inventory):
        paths.update(inside(x["path"]) for x in manifest_rows)
    authority = pinset.get("actual_v2_authority")
    need(type(authority) is dict
         and type(authority.get("authority_input_paths")) is list,
         "core authority input paths")
    paths.update(inside(x) for x in authority["authority_input_paths"])
    paths.update(terminal_files)
    current = [record(path) for path in sorted(paths)]
    manifest_raw = "".join(f"{x['sha256']}  {x['path']}\n"
                           for x in current).encode("ascii")
    output = inside(args.output_dir, absent=True, audit_only=True)
    need(not output.exists() and not output.is_symlink(), "fresh evidence output")
    output.mkdir(parents=True, mode=0o700)

    inventory_path = output / "authority_inventory.sha256"
    fd = os.open(inventory_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o400)
    try:
        os.write(fd, manifest_raw); os.fsync(fd)
    finally:
        os.close(fd)
    body = {"schema": EVIDENCE_SCHEMA, "status": EVIDENCE_STATUS,
        "completed_at_utc": datetime.now(timezone.utc).isoformat(
            timespec="microseconds").replace("+00:00", "Z"),
        "core_receipt_file_sha256": core_record["sha256"],
        "core_receipt_object_sha256": core["transaction_receipt_sha256"],
        "boundary_schema": args.expect_boundary_schema,
        "boundary_status": args.expect_boundary_status,
        "boundary_receipt_file_sha256": boundary_record["sha256"],
        "boundary_receipt_object_sha256": boundary[args.boundary_closure_key],
        "case_schema": args.expect_case_schema, "case_status": args.expect_case_status,
        "case_receipt_file_sha256": case_record["sha256"],
        "case_receipt_object_sha256": cases[args.case_closure_key],
        "real_case_count": cases.get("case_count", cases.get("total")),
        "real_cases_rejected": cases.get("rejected_count", cases.get("rejected")),
        "decision_schema": args.expect_decision_schema,
        "decision_status": args.expect_decision_status,
        "decision_file_sha256": decision_record["sha256"],
        "decision_object_sha256": decision[args.decision_closure_key],
        "core_process_transcript_count": len(core_runs),
        "boundary_case_decision_process_transcripts_reopened": True,
        "all_process_exit0_null_signal_empty_stderr_pre_post_identical": True,
        "boundary_inventory_current_file_count": len(boundary_inventory),
        "case_inventory_current_file_count": len(case_inventory),
        "decision_inventory_current_file_count": len(decision_inventory),
        "authority_inventory_file_sha256": hashlib.sha256(manifest_raw).hexdigest(),
        "authority_inventory_member_count": len(current),
        "actual_v2_terminal_role": "PREDECESSOR_EVIDENCE_ONLY",
        "actual_v2_terminal_authority_eligible": False,
        "historical_C27R2_terminal": {"role": "HISTORICAL_AUDIT_ONLY",
            "authority_eligible": False, "included_in_authority_root": False},
        "exact_math": EXPECTED, "formal_credit": 0,
        "manifest_authorized": False, "authority_minted": False,
        "C27R2": "AUDIT_HOLD_UNAUTHORIZED", "C28_C29": "UNAUTHORIZED",
        "CM2": "NO-GO_FOR_CLAIM"}
    receipt = {**body, "evidence_bundle_sha256": digest(body)}
    evidence_path = output / "evidence_bundle.json"
    fd = os.open(evidence_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o400)
    try:
        os.write(fd, canonical(receipt) + b"\n"); os.fsync(fd)
    finally:
        os.close(fd)
    exact_dir(output, {"authority_inventory.sha256", "evidence_bundle.json"})
    return receipt


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--self-test", action="store_true")
    names = ("core-control", "boundary-receipt", "boundary-inventory",
        "boundary-run", "case-receipt", "case-inventory", "case-run",
        "trust-decision", "decision-inventory", "decision-run", "output-dir",
        "boundary-closure-key", "case-closure-key", "decision-closure-key",
        "expect-boundary-schema", "expect-boundary-status",
        "expect-case-schema", "expect-case-status", "expect-decision-schema",
        "expect-decision-status", "expect-self-sha256",
        "expect-core-receipt-file-sha256", "expect-core-receipt-object-sha256",
        "expect-boundary-file-sha256", "expect-boundary-object-sha256",
        "expect-case-file-sha256", "expect-case-object-sha256",
        "expect-decision-file-sha256", "expect-decision-object-sha256")
    for name in names:
        value.add_argument("--" + name)
    return value


def main() -> int:
    args = parser().parse_args()
    names = [x.dest for x in parser()._actions
             if x.dest not in {"help", "self_test"}]
    try:
        if args.self_test:
            need(all(getattr(args, name) is None for name in names),
                 "self-test no arguments")
            need(EXPECTED["frozen_C15_components"]
                 - EXPECTED["successful_DSU_merges"]
                 == EXPECTED["post_C27R2_components"]
                 and EXPECTED["proof_derived_component_edges"]
                 - EXPECTED["successful_DSU_merges"] == EXPECTED["cycle_edges"]
                 and EXPECTED["total_unordered_member_pairs"]
                 - EXPECTED["within_post_component_member_pairs"]
                 == EXPECTED["cross_post_component_member_pairs"],
                 "math fixtures")
            result = {"status": "PASS_C27R2_RELEASE_REPAIR_EVIDENCE_V2_SELF_TEST"}
        else:
            need(all(getattr(args, name) is not None for name in names),
                 "all dynamic arguments required")
            result = execute(args)
        sys.stdout.buffer.write(canonical({"CM2": "NO-GO_FOR_CLAIM",
            "formal_credit": 0, "status": result["status"]}) + b"\n")
        return 0
    except (Blocked, OSError, ValueError, KeyError, TypeError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
