#!/usr/bin/env python3
"""Build zero-credit C28 release-repair evidence from current bytes.

The boundary and 52-case schemas/statuses are dynamic exact pins so this
back-half can be frozen only after the independently developed front-half is
frozen.  The builder reopens the core's seven process transcripts, the cold,
boundary and attack process transcripts, and both current-byte inventory
manifests.  It cannot write a manifest, seal, terminal receipt, or PASS lock.
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
BASE = "cm2.round306c28.source-g-post-c27r2-125561998198-pair-routing.v2."
CORE_SCHEMA = BASE + "gated-dual-seed-core-receipt.v1"
CORE_STATUS = ("PASS_C27R2_TERMINAL_ADAPTER_DUAL_TRUE_SEED_THREE_FILE_"
    "CANDIDATES_TWO_NO_IMPORT_VERIFIERS_AND_26_ATTACKS__ZERO_CREDIT_"
    "PENDING_RELEASE")
COLD_SCHEMA = BASE + "release-cold-replay-receipt.v1"
EVIDENCE_SCHEMA = BASE + "release-repair-evidence-bundle.v2"
EVIDENCE_STATUS = ("PASS_C28_RELEASE_REPAIR_CORE_COLD_CURRENT_BOUNDARY_AND_"
    "52_REAL_CASE_PROCESS_TRANSCRIPTS_REOPENED__ZERO_CREDIT_PENDING_MANIFEST")
CORE_PASS = b"PASS_C28_PAIR_ROUTING_V2_DUAL_SEED_CORE__ZERO_CREDIT\n"
RUN_INVENTORY_V1 = {"PASS.lock", "exit_code.txt", "input_post.json",
    "input_pre.json", "output_validation.json", "run_attestation.json",
    "runner_start.json", "signal.json", "stderr.log", "stdout.log",
    "timing.json"}
RUN_INVENTORY_V2 = RUN_INVENTORY_V1
EXPECTED = {"members": 502_204, "post_components": 43_684,
    "blocks": 256, "shards": 32_896, "total_pairs": 126_104_177_706,
    "within_pairs": 542_179_508, "cross_pairs": 125_561_998_198}
RUN_TARGETS = ("adapter_run", "adapter_verifier_run", "seed1_run",
    "seed2_run", "verifier1_run", "verifier2_run", "attack_run")


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


def audit_path(raw: str, *, absent: bool = False) -> Path:
    supplied = Path(raw)
    path = (supplied if supplied.is_absolute() else ROOT / supplied).absolute()
    try:
        relative = path.relative_to(AUDIT)
    except ValueError as error:
        raise Blocked("path outside audit root") from error
    need(relative.parts and all(p not in {"", ".", ".."}
                                for p in relative.parts), "canonical path")
    cursor = AUDIT
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
        current = os.stat(path, follow_symlinks=False)
        need(fingerprint(current) == fingerprint(before), "stable current file")
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


def exact_dir(path: Path, names: set[str]) -> None:
    need(path.is_dir() and not path.is_symlink(), "directory")
    actual = {p.name for p in path.iterdir()}
    need(actual == names and all(p.is_file() and not p.is_symlink()
                                 for p in path.iterdir()), "exact inventory")


def process_transcript(path: Path, *, v2: bool = False) -> dict[str, Any]:
    exact_dir(path, RUN_INVENTORY_V2 if v2 else RUN_INVENTORY_V1)
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
    pre = strict((path / "input_pre.json").read_bytes()[:-1])
    post = strict((path / "input_post.json").read_bytes()[:-1])
    need(pre == post, "process pre/post bytes")
    return {"run_attestation": run_record,
            "inventory": [record(path / name) for name in sorted(RUN_INVENTORY_V1)]}


def parse_manifest(path: Path) -> list[dict[str, Any]]:
    raw = path.read_bytes()
    need(raw.endswith(b"\n"), "inventory manifest newline")
    records: list[dict[str, Any]] = []
    seen: set[str] = set()
    for line in raw.decode("ascii").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\x00\r\n]+)", line)
        need(match is not None, "manifest line")
        claim, shown = match.groups()
        need(shown not in seen, "manifest duplicate")
        seen.add(shown)
        path_item = audit_path(shown)
        item = record(path_item)
        need(item["sha256"] == claim, "manifest current SHA")
        records.append(item)
    need(records and [x["path"] for x in records] == sorted(seen),
         "manifest sorted/nonempty")
    return records


def tree_records(roots: list[Path]) -> list[dict[str, Any]]:
    paths: set[Path] = {SELF}
    for root in roots:
        need(root.is_dir() and not root.is_symlink(), "tree root")
        for current, directories, files in os.walk(root):
            current_path = Path(current)
            need(not current_path.is_symlink(), "tree symlink directory")
            for name in directories:
                need(not (current_path / name).is_symlink(), "tree symlink")
            for name in files:
                paths.add(current_path / name)
    return [record(p) for p in sorted(paths)]


def execute(args: argparse.Namespace) -> dict[str, Any]:
    dynamic = (args.expect_self_sha256, args.expect_core_receipt_file_sha256,
        args.expect_core_receipt_object_sha256, args.expect_cold_receipt_file_sha256,
        args.expect_cold_receipt_object_sha256, args.expect_boundary_file_sha256,
        args.expect_boundary_object_sha256, args.expect_attack_file_sha256,
        args.expect_attack_object_sha256)
    need(all(valid_sha(x) for x in dynamic), "all dynamic SHA pins")
    need(record(SELF)["sha256"] == args.expect_self_sha256, "self pin")
    need(type(args.expect_boundary_schema) is str and args.expect_boundary_schema
         and type(args.expect_boundary_status) is str and args.expect_boundary_status
         and type(args.expect_attack_schema) is str and args.expect_attack_schema
         and type(args.expect_attack_status) is str and args.expect_attack_status,
         "dynamic schema/status pins")
    control = audit_path(args.core_control)
    cold_control = audit_path(args.cold_control)
    boundary_receipt_path = audit_path(args.boundary_receipt)
    attack_receipt_path = audit_path(args.attack_receipt)
    core, core_rec = document(control / "core_receipt.json", "core_receipt_sha256")
    pinset, _ = document(control / "pinset.json", "pinset_sha256")
    need(core_rec["sha256"] == args.expect_core_receipt_file_sha256
         and core["core_receipt_sha256"] == args.expect_core_receipt_object_sha256
         and core.get("schema") == CORE_SCHEMA and core.get("status") == CORE_STATUS
         and core.get("exact_math") == EXPECTED and core.get("formal_credit") == 0
         and (control / "PASS.lock").read_bytes() == CORE_PASS,
         "core exact boundary")
    need(type(pinset.get("targets")) is dict
         and set(RUN_TARGETS) <= set(pinset["targets"]), "core target map")
    core_runs = {name: process_transcript(audit_path(pinset["targets"][name]))
                 for name in RUN_TARGETS}
    cold, cold_rec = document(cold_control / "cold_replay_receipt.json",
                              "cold_replay_receipt_sha256")
    need(cold_rec["sha256"] == args.expect_cold_receipt_file_sha256
         and cold["cold_replay_receipt_sha256"]
             == args.expect_cold_receipt_object_sha256
         and cold.get("schema") == COLD_SCHEMA and cold.get("formal_credit") == 0
         and cold.get("exact_math") == EXPECTED,
         "cold receipt")
    cold_run = process_transcript(audit_path(args.cold_run))
    boundary, boundary_rec = document(boundary_receipt_path,
                                      args.boundary_closure_key)
    need(boundary_rec["sha256"] == args.expect_boundary_file_sha256
         and boundary[args.boundary_closure_key]
             == args.expect_boundary_object_sha256
         and boundary.get("schema") == args.expect_boundary_schema
         and boundary.get("status") == args.expect_boundary_status
         and boundary.get("mode") == "formal"
         and boundary.get("formal_credit") == 0
         and boundary.get("manifest_authorized") is False
         and boundary.get("C28") == "AUDIT_HOLD_UNAUTHORIZED",
         "formal boundary receipt")
    boundary_inventory = parse_manifest(audit_path(args.boundary_inventory))
    boundary_run = process_transcript(audit_path(args.boundary_run), v2=True)
    attacks, attack_rec = document(attack_receipt_path, args.attack_closure_key)
    need(attack_rec["sha256"] == args.expect_attack_file_sha256
         and attacks[args.attack_closure_key] == args.expect_attack_object_sha256
         and attacks.get("schema") == args.expect_attack_schema
         and attacks.get("status") == args.expect_attack_status
         and attacks.get("case_count", attacks.get("total")) == 52
         and attacks.get("rejected_count", attacks.get("rejected")) == 52
         and attacks.get("formal_credit") == 0
         and attacks.get("manifest_authorized") is False,
         "52-case real attack receipt")
    case_inventory = parse_manifest(audit_path(args.attack_case_manifest))
    attack_run = process_transcript(audit_path(args.attack_run), v2=True)
    roots = [control, cold_control, audit_path(args.cold_run),
        boundary_receipt_path.parent, audit_path(args.boundary_run),
        attack_receipt_path.parent, audit_path(args.attack_run)]
    current = tree_records(roots)
    manifest_lines = "".join(f"{item['sha256']}  {item['path']}\n"
                             for item in current).encode("ascii")
    output = audit_path(args.output_dir, absent=True)
    need(not output.exists() and not output.is_symlink(), "fresh evidence output")
    output.mkdir(parents=True, mode=0o700)
    manifest_path = output / "authority_inventory.sha256"
    fd = os.open(manifest_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o400)
    try:
        os.write(fd, manifest_lines); os.fsync(fd)
    finally:
        os.close(fd)
    body = {"schema": EVIDENCE_SCHEMA, "status": EVIDENCE_STATUS,
        "completed_at_utc": datetime.now(timezone.utc).isoformat(
            timespec="microseconds").replace("+00:00", "Z"),
        "core_receipt_file_sha256": core_rec["sha256"],
        "core_receipt_object_sha256": core["core_receipt_sha256"],
        "cold_receipt_file_sha256": cold_rec["sha256"],
        "cold_receipt_object_sha256": cold["cold_replay_receipt_sha256"],
        "boundary_schema": args.expect_boundary_schema,
        "boundary_status": args.expect_boundary_status,
        "boundary_receipt_file_sha256": boundary_rec["sha256"],
        "boundary_receipt_object_sha256": boundary[args.boundary_closure_key],
        "boundary_inventory_current_file_count": len(boundary_inventory),
        "attack_schema": args.expect_attack_schema,
        "attack_status": args.expect_attack_status,
        "attack_receipt_file_sha256": attack_rec["sha256"],
        "attack_receipt_object_sha256": attacks[args.attack_closure_key],
        "real_attack_cases_total": 52, "real_attack_cases_rejected": 52,
        "case_inventory_current_file_count": len(case_inventory),
        "core_process_transcript_count": len(core_runs),
        "cold_boundary_attack_process_transcripts_reopened": True,
        "all_process_exit0_null_signal_empty_stderr_pre_post_identical": True,
        "authority_inventory_file_sha256": hashlib.sha256(manifest_lines).hexdigest(),
        "authority_inventory_member_count": len(current),
        "exact_math": EXPECTED,
        "C27R2": "ONLY_AUTHORIZED_PREDECESSOR",
        "historical_C28_terminal": {"role": "AUDIT_EVIDENCE_ONLY",
                                     "authority_eligible": False},
        "formal_credit": 0, "manifest_authorized": False,
        "C28": "AUDIT_HOLD_UNAUTHORIZED", "C29": "UNAUTHORIZED",
        "CM2": "NO-GO_FOR_CLAIM"}
    result = {**body, "evidence_bundle_sha256": digest(body)}
    out_path = output / "evidence_bundle.json"
    fd = os.open(out_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o400)
    try:
        os.write(fd, canonical(result) + b"\n"); os.fsync(fd)
    finally:
        os.close(fd)
    exact_dir(output, {"authority_inventory.sha256", "evidence_bundle.json"})
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    names = ("core-control", "cold-control", "cold-run", "boundary-receipt",
        "boundary-inventory", "boundary-run", "attack-receipt",
        "attack-case-manifest", "attack-run", "boundary-closure-key",
        "attack-closure-key", "expect-boundary-schema", "expect-boundary-status",
        "expect-attack-schema", "expect-attack-status", "expect-self-sha256",
        "expect-core-receipt-file-sha256", "expect-core-receipt-object-sha256",
        "expect-cold-receipt-file-sha256", "expect-cold-receipt-object-sha256",
        "expect-boundary-file-sha256", "expect-boundary-object-sha256",
        "expect-attack-file-sha256", "expect-attack-object-sha256", "output-dir")
    for name in names:
        parser.add_argument("--" + name)
    args = parser.parse_args()
    try:
        if args.self_test:
            need(all(getattr(args, name.replace("-", "_")) is None
                     for name in names), "self-test no arguments")
            sample = b"0" * 64 + b"  .cm2-runtime/audit/x\n"
            need(re.fullmatch(rb"[0-9a-f]{64}  [^\x00\r\n]+\n", sample)
                 is not None and EXPECTED["total_pairs"]
                 == EXPECTED["within_pairs"] + EXPECTED["cross_pairs"],
                 "evidence fixtures")
            result = {"status": "PASS_C28_RELEASE_REPAIR_EVIDENCE_V2_SELF_TEST"}
        else:
            need(all(getattr(args, name.replace("-", "_")) is not None
                     for name in names), "all evidence arguments")
            result = execute(args)
        sys.stdout.buffer.write(canonical({"CM2": "NO-GO_FOR_CLAIM",
            "formal_credit": 0, "status": result["status"]}) + b"\n")
        return 0
    except (Blocked, OSError, ValueError, KeyError, TypeError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
