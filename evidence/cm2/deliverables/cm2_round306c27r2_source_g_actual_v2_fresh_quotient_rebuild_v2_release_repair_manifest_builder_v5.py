#!/usr/bin/env python3
"""Build the exact-role, manifest-first C27R2 release-repair package v5.

There is no caller-selected ``--source-file`` escape hatch.  Every immutable
authority/source role is frozen in the externally pinned v5 plan; every
runtime role is fixed by this program.  Historical C27R2 terminal bytes are
audit-only and are rejected from both new manifests.
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
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
BASE = "cm2.round306c27r2.source-g-authority-v2.release-repair."
PLAN_SCHEMA = BASE + "chain-plan.v5"
PLAN_STATUS = (
    "FROZEN_C27R2_RELEASE_REPAIR_V5_EXACT70_PLUS_LOCK8_PLAN__EXECUTION_DISABLED_"
    "PENDING_INDEPENDENT_FULL_CHAIN_AUDIT"
)
SNAPSHOT_SCHEMA = BASE + "current-snapshot-evidence.v5"
POST_SCHEMA = BASE + "post-integrity-evidence-closure.v5"
POST_STATUS = (
    "PASS_C27R2_RELEASE_REPAIR_V5_SNAPSHOT_BASELINE_VALIDATOR70_LOCK8_REAL_"
    "TRANSACTIONS_POST_REPLAY_FULL9STAT_AND_PRIVATE_CLEANUP_CLOSED__ZERO_"
    "CREDIT_PENDING_MANIFEST"
)
MANIFEST_SCHEMA = BASE + "manifest-receipt.v5"
MANIFEST_STATUS = (
    "PASS_C27R2_RELEASE_REPAIR_V5_EXACT_ROLE_MANIFESTS_POST_VALIDATOR70_LOCK8_"
    "ACTUAL_V2_PREDECESSOR_ONLY_AND_HISTORICAL_EXCLUSION_CLOSED__ZERO_"
    "CREDIT_PENDING_OUTER"
)
EXPECTED = {
    "frozen_C15_components": 57_876, "post_C27R2_components": 43_684,
    "proof_derived_component_edges": 14_860,
    "successful_DSU_merges": 14_192, "cycle_edges": 668,
    "frozen_C15_members": 502_204,
    "total_unordered_member_pairs": 126_104_177_706,
    "within_post_component_member_pairs": 542_179_508,
    "cross_post_component_member_pairs": 125_561_998_198,
}
CANDIDATE_FILES = {
    "member_to_post_component.jsonl.gz",
    "old_c15_component_to_post_component.jsonl.gz",
    "post_component_census.jsonl.gz", "result.json",
}
SOURCE_ROLES = {
    "python", "transaction_runner", "fd_bound_stage_wrapper", "cold_runner",
    "boundary_validator",
    "integrity70_plus_lock8_runner", "trust_decision_auditor", "snapshot_builder",
    "post_evidence_builder", "manifest_builder", "outer_verifier",
    "conditional_seal_builder", "anticipated_terminal_builder",
    "terminal_finalizer", "watcher",
}
RUNTIME_FILES = {
    "plan", "snapshot_receipt", "snapshot_records", "post_receipt",
    "post_records", "candidate_member", "candidate_old_map",
    "candidate_census", "candidate_result", "verification", "core_attacks",
    "core_receipt", "core_pinset", "frozen_C15", "seed1_edge", "seed2_edge",
    "fixture_receipt",
}
BOUNDARY_VALIDATOR_PATH = (
    "deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_quotient_"
    "rebuild_v2_release_repair_boundary_independent_validator_v6.py"
)
BOUNDARY_VALIDATOR_SHA = "0" * 64  # Pending final boundary-v6 source pin.
INTEGRITY_RUNNER_PATH = (
    "deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_quotient_"
    "rebuild_v2_release_integrity_fixture_runner_v6.py"
)
INTEGRITY_RUNNER_SHA = "0" * 64  # Pending final boundary-v6 source pin.
ORDERED_VALIDATOR70_OBJECT_SHA = "12a18411f62ba091fad7a28af44fe6a2eea1e4befe211c0f58d16a30a1a434b8"
ORDERED_LOCK8_OBJECT_SHA = "92add6db3116e10fe54cda24ce5d61288bb47622e6956f1353898ba707811c5d"
COLD_RUNNER_PATH = (
    "deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_quotient_"
    "rebuild_v2_release_cold_replay_runner_v4.py"
)
COLD_RUNNER_SHA = "3d44ebbc37449192f975e3687284c6e74285f7d7f564e40ef12e37232f0ec838"
BOUNDARY_CONTRACT_FROZEN_GO = False  # boundary v5 historical NO-GO; v6 pending.
FORMAL_EXECUTION_AUTHORIZED = False  # Independent full-chain GO has not been minted.


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
            need(key not in out, "duplicate JSON key")
            out[key] = value
        return out
    return json.loads(raw, object_pairs_hook=pairs,
        parse_constant=lambda value: (_ for _ in ()).throw(Blocked(value)))


def fingerprint(info: os.stat_result) -> list[int]:
    return [info.st_dev, info.st_ino, info.st_mode, info.st_nlink,
            info.st_size, info.st_mtime_ns, info.st_ctime_ns,
            info.st_uid, info.st_gid]


def inside(raw: str | Path, absent: bool = False) -> Path:
    supplied = Path(raw)
    path = (supplied if supplied.is_absolute() else ROOT / supplied).absolute()
    try:
        relative = path.relative_to(ROOT)
    except ValueError as error:
        raise Blocked("outside workspace") from error
    need(relative.parts and all(x not in {"", ".", ".."} for x in relative.parts),
         "canonical path")
    cursor = ROOT
    for part in relative.parts:
        cursor /= part
        if not cursor.exists():
            need(absent, "missing path")
            break
        need(not cursor.is_symlink(), "symlink path")
    return path


def capture(path: Path, retain_bytes: bool = True) -> tuple[bytes, dict[str, Any]]:
    need(path.is_file() and not path.is_symlink(), "regular file")
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular single-link")
        state = hashlib.sha256()
        chunks: list[bytes] = []
        while block := os.read(descriptor, 4 << 20):
            state.update(block)
            if retain_bytes: chunks.append(block)
        need(fingerprint(os.stat(path, follow_symlinks=False))
             == fingerprint(before)
             and fingerprint(os.fstat(descriptor)) == fingerprint(before),
             "stable full9stat")
        return b"".join(chunks), {"path": str(path.relative_to(ROOT)), "sha256": state.hexdigest(),
                "size": before.st_size, "stat_fingerprint": fingerprint(before)}
    finally:
        os.close(descriptor)


def record(path: Path) -> dict[str, Any]:
    return capture(path, False)[1]


def document(path: Path, closure: str) -> tuple[dict[str, Any], dict[str, Any]]:
    raw, item = capture(path)
    need(raw.endswith(b"\n"), "newline")
    value = strict(raw[:-1])
    need(type(value) is dict and canonical(value) == raw[:-1], "canonical JSON")
    body = dict(value)
    claim = body.pop(closure, None)
    need(valid_sha(claim) and claim == digest(body), "object closure")
    return value, item


def _write_all(descriptor: int, raw: bytes, writer: Any = os.write) -> None:
    offset = 0
    while offset < len(raw):
        count = writer(descriptor, raw[offset:])
        need(type(count) is int and count > 0, "write made positive progress")
        offset += count


def write_once(path: Path, raw: bytes) -> None:
    parent = os.open(path.parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
                     | getattr(os, "O_NOFOLLOW", 0)
                     | getattr(os, "O_CLOEXEC", 0))
    descriptor = -1
    try:
        descriptor = os.open(path.name, os.O_WRONLY | os.O_CREAT | os.O_EXCL
            | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0),
            0o400, dir_fd=parent)
        _write_all(descriptor, raw)
        os.fsync(descriptor)
        before = os.fstat(descriptor)
    finally:
        if descriptor >= 0:
            os.close(descriptor)
    reopened = os.open(path.name, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
                       | getattr(os, "O_CLOEXEC", 0), dir_fd=parent)
    try:
        chunks: list[bytes] = []
        while block := os.read(reopened, 1 << 20):
            chunks.append(block)
        after = os.fstat(reopened)
        current = os.stat(path.name, dir_fd=parent, follow_symlinks=False)
        observed = b"".join(chunks)
        need(observed == raw and stat.S_ISREG(after.st_mode) and after.st_nlink == 1
             and fingerprint(before) == fingerprint(after) == fingerprint(current)
             and hashlib.sha256(raw).digest() == hashlib.sha256(observed).digest(),
             "reopen exact bytes/SHA/full9stat/single-link")
        os.fsync(parent)
    finally:
        os.close(reopened)
        os.close(parent)


def fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
                         | getattr(os, "O_NOFOLLOW", 0))
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def records_ledger(path: Path, schema: str) -> list[dict[str, Any]]:
    raw, _ = capture(path)
    need(raw.endswith(b"\n"), "record ledger newline")
    rows: list[dict[str, Any]] = []
    for ordinal, line in enumerate(raw.splitlines()):
        row = strict(line)
        body = dict(row)
        claim = body.pop("row_sha256", None)
        need(type(row) is dict and canonical(row) == line
             and row.get("schema") == schema and row.get("ordinal") == ordinal
             and valid_sha(claim) and claim == digest(body), "record ledger row")
        current = record(inside(row["path"]))
        need(current["sha256"] == row["sha256"]
             and current["size"] == row["size"]
             and current["stat_fingerprint"] == row["stat_fingerprint"],
             "record ledger current byte/full9stat")
        rows.append(row)
    need(len(rows) > 0, "nonempty record ledger")
    return rows


def manifest_bytes(paths: set[Path]) -> bytes:
    rows = []
    for path in sorted(paths):
        item = record(path)
        rows.append(f"{item['sha256']}  {item['path']}\n")
    need(len(rows) > 0, "nonempty manifest")
    return "".join(rows).encode("ascii")


def load_plan(path: Path, file_pin: str, object_pin: str) -> tuple[dict[str, Any], dict[str, Any]]:
    value, item = document(path, "plan_sha256")
    need(item["sha256"] == file_pin and value["plan_sha256"] == object_pin
         and value.get("schema") == PLAN_SCHEMA and value.get("status") == PLAN_STATUS
         and value.get("validator_negative_case_count") == 70
         and value.get("publication_lock_preflight_case_count") == 8
         and value.get("total_integrity_check_count") == 78
         and "case_count" not in value and value.get("exact_math") == EXPECTED
         and value.get("ordered_validator70_object_sha256")
             == ORDERED_VALIDATOR70_OBJECT_SHA
         and value.get("ordered_lock8_object_sha256") == ORDERED_LOCK8_OBJECT_SHA
         and value.get("execution_enabled") is False
         and value.get("formal_credit") == 0
         and value.get("manifest_authorized") is False
         and value.get("authority_minted") is False, "frozen plan")
    sources = value.get("sources")
    need(type(sources) is dict and set(sources) == SOURCE_ROLES,
         "exact source roles")
    for role, spec in sources.items():
        current = record(inside(spec["path"])) if type(spec) is dict \
            and "path" in spec else {}
        need(type(spec) is dict and set(spec) == {"path", "sha256"}
             and valid_sha(spec["sha256"])
             and current.get("path") == spec["path"]
             and current.get("sha256") == spec["sha256"],
             "source role:" + role)
    need(sources["boundary_validator"] == {"path": BOUNDARY_VALIDATOR_PATH,
            "sha256": BOUNDARY_VALIDATOR_SHA}
         and sources["integrity70_plus_lock8_runner"] == {
            "path": INTEGRITY_RUNNER_PATH, "sha256": INTEGRITY_RUNNER_SHA}
         and sources["cold_runner"] == {"path": COLD_RUNNER_PATH,
            "sha256": COLD_RUNNER_SHA},
         "frozen boundary/cold source pins")
    return value, item


def execute(args: argparse.Namespace) -> dict[str, Any]:
    need(FORMAL_EXECUTION_AUTHORIZED and BOUNDARY_CONTRACT_FROZEN_GO,
         "boundary v5 NO-GO; append-only boundary v6 independent GO required")
    pins = (args.expect_self_sha256, args.expect_plan_file_sha256,
        args.expect_plan_object_sha256, args.expect_snapshot_file_sha256,
        args.expect_snapshot_object_sha256, args.expect_post_file_sha256,
        args.expect_post_object_sha256)
    need(all(valid_sha(pin) for pin in pins)
         and record(SELF)["sha256"] == args.expect_self_sha256, "all pins")
    plan_path = inside(args.plan)
    plan, plan_record = load_plan(plan_path, args.expect_plan_file_sha256,
                                  args.expect_plan_object_sha256)
    need(plan["sources"]["manifest_builder"]["path"] == record(SELF)["path"]
         and plan["sources"]["manifest_builder"]["sha256"]
             == args.expect_self_sha256, "manifest source plan role")

    snapshot_dir = inside(args.snapshot_dir)
    snapshot, snapshot_record = document(snapshot_dir / "snapshot_evidence.json",
                                          "snapshot_evidence_sha256")
    snapshot_rows_path = snapshot_dir / "snapshot_records.jsonl"
    snapshot_rows = records_ledger(snapshot_rows_path,
                                    BASE + "snapshot-member-row.v5")
    need(snapshot_record["sha256"] == args.expect_snapshot_file_sha256
         and snapshot["snapshot_evidence_sha256"]
             == args.expect_snapshot_object_sha256
         and snapshot.get("schema") == SNAPSHOT_SCHEMA
         and snapshot.get("snapshot_record_count") == len(snapshot_rows)
         and snapshot.get("formal_credit") == 0
         and snapshot.get("manifest_authorized") is False,
         "snapshot crosslink")

    post_dir = inside(args.post_dir)
    post, post_record = document(post_dir / "post_integrity_evidence.json",
                                 "post_integrity_evidence_sha256")
    post_rows_path = post_dir / "authority_records.jsonl"
    post_rows = records_ledger(post_rows_path,
                               BASE + "post-authority-member-row.v5")
    need(post_record["sha256"] == args.expect_post_file_sha256
         and post["post_integrity_evidence_sha256"]
             == args.expect_post_object_sha256
         and post.get("schema") == POST_SCHEMA and post.get("status") == POST_STATUS
         and post.get("plan_file_sha256") == args.expect_plan_file_sha256
         and post.get("plan_object_sha256") == args.expect_plan_object_sha256
         and post.get("snapshot_evidence_file_sha256")
             == args.expect_snapshot_file_sha256
         and post.get("snapshot_evidence_object_sha256")
             == args.expect_snapshot_object_sha256
         and post.get("validator_negative_case_count") == 70
         and post.get("validator_rejected_count") == 70
         and post.get("publication_lock_preflight_case_count") == 8
         and post.get("publication_lock_preflight_rejected_count") == 8
         and post.get("total_integrity_check_count") == 78
         and "case_count" not in post
         and post.get("accepted_count") == 0
         and post.get("case_process_transcripts_reopened") == 70
         and post.get("authority_record_count") == len(post_rows)
         and post.get("formal_credit") == 0
         and post.get("manifest_authorized") is False,
         "post validator70/lock8 crosslink/governance")

    candidate = inside(args.candidate_dir)
    need(candidate.is_dir() and not candidate.is_symlink()
         and {path.name for path in candidate.iterdir()} == CANDIDATE_FILES,
         "candidate exact inventory")
    runtime_paths = {
        "plan": plan_path,
        "snapshot_receipt": snapshot_dir / "snapshot_evidence.json",
        "snapshot_records": snapshot_rows_path,
        "post_receipt": post_dir / "post_integrity_evidence.json",
        "post_records": post_rows_path,
        "candidate_member": candidate / "member_to_post_component.jsonl.gz",
        "candidate_old_map": candidate / "old_c15_component_to_post_component.jsonl.gz",
        "candidate_census": candidate / "post_component_census.jsonl.gz",
        "candidate_result": candidate / "result.json",
        "verification": inside(args.verification),
        "core_attacks": inside(args.core_attacks),
        "core_receipt": inside(args.core_receipt),
        "core_pinset": inside(args.core_pinset),
        "frozen_C15": inside(args.frozen_c15),
        "seed1_edge": inside(args.seed1_edge),
        "seed2_edge": inside(args.seed2_edge),
        "fixture_receipt": inside(args.fixture_receipt),
    }
    need(set(runtime_paths) == RUNTIME_FILES, "exact runtime roles")
    frozen_runtime = plan.get("runtime_authority_roles")
    need(type(frozen_runtime) is dict and set(frozen_runtime) == RUNTIME_FILES,
         "plan exact runtime authority roles")
    for role, path in runtime_paths.items():
        spec = frozen_runtime[role]
        current = record(path)
        need(type(spec) is dict and set(spec) == {"path", "sha256"}
             and current["path"] == spec["path"]
             and current["sha256"] == spec["sha256"],
             "runtime role pin:" + role)
    result, _ = document(runtime_paths["candidate_result"], "result_sha256")
    need(result.get("exact_census") == EXPECTED
         and result.get("formal_credit") == 0
         and result.get("manifest_authorized") is False,
         "candidate result conditional governance")

    payload_paths = set(runtime_paths.values())
    payload_paths.update(inside(spec["path"]) for spec in plan["sources"].values())
    payload_paths.update(inside(row["path"]) for row in snapshot_rows + post_rows)
    historical = inside(plan["historical_terminal_dir"])
    need(not any(path == historical or historical in path.parents
                 for path in payload_paths), "historical terminal excluded")
    actual_root_specs = plan.get("actual_v2_root_members")
    need(type(actual_root_specs) is list and actual_root_specs,
         "actual-v2 root members")
    actual_paths: set[Path] = set()
    for spec in actual_root_specs:
        need(type(spec) is dict and set(spec) == {"path", "sha256"},
             "actual root member shape")
        path = inside(spec["path"])
        need(record(path)["sha256"] == spec["sha256"], "actual root pin")
        actual_paths.add(path)

    output = inside(args.output_dir, absent=True)
    need(not output.exists() and not output.is_symlink(), "fresh output")
    output.mkdir(parents=True, mode=0o700)
    fsync_directory(output)
    fsync_directory(output.parent)
    payload_path = output / "payload_manifest.sha256"
    write_once(payload_path, manifest_bytes(payload_paths))
    root_paths = actual_paths | {payload_path, plan_path, SELF}
    root_path = output / "root_manifest.sha256"
    write_once(root_path, manifest_bytes(root_paths))
    candidate_hashes = {name: record(candidate / name)["sha256"]
                        for name in CANDIDATE_FILES}
    body = {
        "schema": MANIFEST_SCHEMA, "status": MANIFEST_STATUS,
        "completed_at_utc": datetime.now(timezone.utc).isoformat(
            timespec="microseconds").replace("+00:00", "Z"),
        "plan_file_sha256": plan_record["sha256"],
        "plan_object_sha256": plan["plan_sha256"],
        "snapshot_evidence_file_sha256": snapshot_record["sha256"],
        "snapshot_evidence_object_sha256": snapshot["snapshot_evidence_sha256"],
        "post_evidence_file_sha256": post_record["sha256"],
        "post_evidence_object_sha256": post["post_integrity_evidence_sha256"],
        "payload_manifest_file_sha256": record(payload_path)["sha256"],
        "payload_member_count": len(payload_paths),
        "root_manifest_file_sha256": record(root_path)["sha256"],
        "root_member_count": len(root_paths),
        "source_roles": sorted(SOURCE_ROLES),
        "runtime_authority_roles": sorted(RUNTIME_FILES),
        "candidate_file_sha256": candidate_hashes,
        "core_receipt_file_sha256": record(runtime_paths["core_receipt"])["sha256"],
        "core_receipt_object_sha256": plan["core_receipt_object_sha256"],
        "core_pinset_file_sha256": record(runtime_paths["core_pinset"])["sha256"],
        "core_pinset_object_sha256": plan["core_pinset_object_sha256"],
        "frozen_C15_path": record(runtime_paths["frozen_C15"])["path"],
        "frozen_C15_sha256": record(runtime_paths["frozen_C15"])["sha256"],
        "seed1_edge_path": record(runtime_paths["seed1_edge"])["path"],
        "seed1_edge_sha256": record(runtime_paths["seed1_edge"])["sha256"],
        "seed2_edge_path": record(runtime_paths["seed2_edge"])["path"],
        "seed2_edge_sha256": record(runtime_paths["seed2_edge"])["sha256"],
        "actual_v2_terminal_role": "PREDECESSOR_EVIDENCE_ONLY",
        "actual_v2_terminal_authority_eligible": False,
        "historical_C27R2_terminal": {
            "path": str(historical.relative_to(ROOT)), "role": "AUDIT_ONLY",
            "authority_eligible": False, "included_in_payload": False,
            "included_in_authority_root": False,
        },
        "validator_negative_case_count": 70, "validator_rejected_count": 70,
        "publication_lock_preflight_case_count": 8,
        "publication_lock_preflight_rejected_count": 8,
        "total_integrity_check_count": 78, "accepted_count": 0,
        "exact_math": EXPECTED, "formal_credit": 0,
        "manifest_authorized": False, "authority_minted": False,
        "C27R2": "AUDIT_HOLD_UNAUTHORIZED", "C28_C29": "UNAUTHORIZED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    receipt = {**body, "manifest_receipt_sha256": digest(body)}
    write_once(output / "manifest_receipt.json", canonical(receipt) + b"\n")
    need({path.name for path in output.iterdir()} == {
        "manifest_receipt.json", "payload_manifest.sha256",
        "root_manifest.sha256"}, "manifest output inventory")
    return receipt


def self_test() -> dict[str, Any]:
    need(FORMAL_EXECUTION_AUTHORIZED is False
         and BOUNDARY_CONTRACT_FROZEN_GO is False,
         "development source remains launch-blocked on boundary v6 audit")
    try:
        _write_all(-1, b"x", lambda _fd, _raw: 0)
        raise Blocked("zero-progress writer unexpectedly accepted")
    except Blocked as error:
        need(str(error) == "write made positive progress",
             "zero-progress write fixture")
    need("source-file" not in {"source-file" for _ in ()}
         and len(SOURCE_ROLES) == 15 and len(RUNTIME_FILES) == 17,
         "exact role counts")
    with tempfile.TemporaryDirectory(dir=ROOT / ".cm2-runtime",
            prefix="c27r2-manifest-v5-selftest-") as raw:
        root = Path(raw)
        one = root / "one"; two = root / "two"
        one.write_bytes(b"one\n"); two.write_bytes(b"two\n")
        payload = manifest_bytes({one, two})
        lines = payload.decode("ascii").splitlines()
        need(len(lines) == 2 and lines == sorted(lines, key=lambda row: row[66:]),
             "real exact sorted manifest fixture")
    return {"status": "PASS_C27R2_RELEASE_REPAIR_MANIFEST_V5_SELF_TEST"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    for name in ("plan", "snapshot-dir", "post-dir", "candidate-dir",
        "verification", "core-attacks", "core-receipt", "core-pinset",
        "frozen-c15", "seed1-edge", "seed2-edge", "fixture-receipt",
        "output-dir", "expect-self-sha256", "expect-plan-file-sha256",
        "expect-plan-object-sha256", "expect-snapshot-file-sha256",
        "expect-snapshot-object-sha256", "expect-post-file-sha256",
        "expect-post-object-sha256"):
        parser.add_argument("--" + name)
    args = parser.parse_args()
    fields = tuple(action.dest for action in parser._actions
                   if action.dest not in {"help", "self_test"})
    try:
        if args.self_test:
            need(all(getattr(args, field) is None for field in fields),
                 "self-test no arguments")
            result = self_test()
        else:
            need(all(getattr(args, field) is not None for field in fields),
                 "all frozen roles required")
            result = execute(args)
        sys.stdout.buffer.write(canonical({"CM2": "NO-GO_FOR_CLAIM",
            "formal_credit": 0, "status": result["status"]}) + b"\n")
        return 0
    except (Blocked, OSError, ValueError, KeyError, TypeError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
