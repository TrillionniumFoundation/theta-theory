#!/usr/bin/env python3
"""No-import anticipated terminal builder for C27R2 repair v4.

It independently reopens the conditional chain and writes an anticipated
four-file package.  The package contains no PASS and every governance field
remains unauthorized.  The separately audited finalizer is the only program
allowed to construct the official terminal and write PASS last.
"""

from __future__ import annotations

import argparse
import ast
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
PLAN_SCHEMA = BASE + "chain-plan.v4"
PLAN_STATUS = (
    "FROZEN_C27R2_RELEASE_REPAIR_V4_EXACT70_PLUS_LOCK8_PLAN__EXECUTION_DISABLED_"
    "PENDING_INDEPENDENT_FULL_CHAIN_AUDIT"
)
MANIFEST_SCHEMA = BASE + "manifest-receipt.v4"
OUTER_SCHEMA = BASE + "outer-verification.v4"
SEAL_SCHEMA = BASE + "conditional-seal.v4"
SEAL_STATUS = (
    "PASS_CONDITIONAL_C27R2_RELEASE_REPAIR_V4_SEAL_EXACT_MANIFEST_OUTER_"
    "AND_FINALIZER_SERVICE_EXPECTATION__ZERO_CREDIT_NOT_AUTHORITY"
)
EXPECT_SCHEMA = BASE + "terminal-expectation.v4"
EXPECT_STATUS = (
    "PASS_C27R2_RELEASE_REPAIR_V4_TERMINAL_EXPECTATION_BYTES_FROZEN__"
    "PENDING_ANTICIPATED_REPLAY_AND_FINALIZER_SERVICE_CLEAN_SUCCESS"
)
ANTICIPATED_SCHEMA = BASE + "anticipated-terminal-receipt.v4"
ANTICIPATED_STATUS = (
    "PASS_C27R2_RELEASE_REPAIR_V4_INDEPENDENT_ANTICIPATED_BYTE_REPLAY__"
    "ZERO_CREDIT_PENDING_OFFICIAL_FINALIZER_AND_SERVICE_CLEAN_SUCCESS"
)
REPLAY_SCHEMA = BASE + "anticipated-terminal-replay.v4"
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
BOUNDARY_CONTRACT_FROZEN_GO = False  # boundary v4 NO-GO; append-only v5 pending.
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


def independence() -> str:
    raw, _ = capture(SELF); tree = ast.parse(raw, filename=str(SELF))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            need(all(alias.name.split(".")[0]
                     not in {"subprocess", "importlib", "runpy"}
                     for alias in node.names), "forbidden import")
        if isinstance(node, ast.ImportFrom):
            need((node.module or "").split(".")[0]
                 not in {"subprocess", "importlib", "runpy"},
                 "forbidden from-import")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            need(node.func.id not in {"exec", "eval", "compile", "__import__"},
                 "forbidden dynamic execution")
    return hashlib.sha256(raw).hexdigest()


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
             "single-link file")
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
    body = dict(value); claim = body.pop(closure, None)
    need(valid_sha(claim) and claim == digest(body), "object closure")
    return value, item


def parse_manifest(path: Path) -> dict[str, str]:
    raw, _ = capture(path); need(raw.endswith(b"\n"), "manifest newline")
    result: dict[str, str] = {}
    for line in raw.decode("ascii").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\x00\r\n]+)", line)
        need(match is not None, "manifest row")
        claim, shown = match.groups()
        need(shown not in result and record(inside(shown))["sha256"] == claim,
             "manifest current member")
        result[shown] = claim
    need(len(result) > 0 and list(result) == sorted(result), "sorted manifest")
    return result


def manifest_bytes(paths: set[Path]) -> bytes:
    rows = []
    for path in sorted(paths):
        item = record(path)
        rows.append(f"{item['sha256']}  {item['path']}\n")
    need(len(rows) > 0, "nonempty manifest")
    return "".join(rows).encode("ascii")


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


def execute(args: argparse.Namespace) -> dict[str, Any]:
    need(FORMAL_EXECUTION_AUTHORIZED and BOUNDARY_CONTRACT_FROZEN_GO,
         "boundary v4 NO-GO; append-only boundary v5 independent GO required")
    pins = (args.expect_self_sha256, args.expect_plan_file_sha256,
        args.expect_plan_object_sha256, args.expect_seal_file_sha256,
        args.expect_seal_object_sha256, args.expect_expectation_file_sha256,
        args.expect_expectation_object_sha256, args.expect_manifest_file_sha256,
        args.expect_manifest_object_sha256, args.expect_outer_file_sha256,
        args.expect_outer_object_sha256)
    need(all(valid_sha(value) for value in pins)
         and independence() == args.expect_self_sha256,
         "all pins/no-import independence")
    plan, plan_record = document(inside(args.plan), "plan_sha256")
    need(plan_record["sha256"] == args.expect_plan_file_sha256
         and plan["plan_sha256"] == args.expect_plan_object_sha256
         and plan.get("schema") == PLAN_SCHEMA
         and plan.get("status") == PLAN_STATUS
         and plan.get("validator_negative_case_count") == 70
         and plan.get("publication_lock_preflight_case_count") == 8
         and plan.get("total_integrity_check_count") == 78
         and "case_count" not in plan
         and plan.get("exact_math") == EXPECTED
         and plan.get("formal_credit") == 0
         and plan.get("manifest_authorized") is False
         and plan.get("authority_minted") is False,
         "frozen plan")
    service = plan.get("finalizer_service")
    need(type(service) is dict and set(service) == {"unit", "launch_mode",
         "invocation_binding", "expected_result", "expected_exec_main_code",
         "expected_exec_main_status", "expected_load_state",
         "expected_active_state", "expected_sub_state", "fragment_path"}
         and service.get("invocation_binding")
             == "CAPTURE_FINALIZER_ENV_AND_MATCH_POST_EXIT_SYSTEMD_SHOW"
         and service.get("expected_result") == "success"
         and service.get("expected_exec_main_code") == 1
         and service.get("expected_exec_main_status") == 0
         and service.get("expected_load_state") == "loaded"
         and service.get("expected_active_state") == "inactive"
         and service.get("expected_sub_state") == "dead"
         and service.get("launch_mode")
             == "EXPLICIT_USER_BUS_SYSTEMD_RUN_TRANSIENT_V1"
         and type(service.get("unit")) is str
         and service["unit"].startswith("cm2-")
         and service["unit"].endswith(".service")
         and service.get("fragment_path")
             == f"/run/user/{os.getuid()}/systemd/transient/{service['unit']}",
         "future unit/ExecStart-template/FragmentPath/clean finalizer contract")

    seal_dir = inside(args.seal_dir)
    need({path.name for path in seal_dir.iterdir()} == {
        "conditional_seal.json", "seal_payload_manifest.sha256",
        "seal_root_manifest.sha256", "terminal_expectation.json"},
        "conditional seal inventory")
    seal, seal_record = document(seal_dir / "conditional_seal.json",
                                  "conditional_seal_sha256")
    expectation, expectation_record = document(
        seal_dir / "terminal_expectation.json", "terminal_expectation_sha256")
    seal_payload = seal_dir / "seal_payload_manifest.sha256"
    seal_root = seal_dir / "seal_root_manifest.sha256"
    parse_manifest(seal_payload); parse_manifest(seal_root)
    need(seal_record["sha256"] == args.expect_seal_file_sha256
         and seal["conditional_seal_sha256"] == args.expect_seal_object_sha256
         and expectation_record["sha256"] == args.expect_expectation_file_sha256
         and expectation["terminal_expectation_sha256"]
             == args.expect_expectation_object_sha256
         and seal.get("schema") == SEAL_SCHEMA and seal.get("status") == SEAL_STATUS
         and expectation.get("schema") == EXPECT_SCHEMA
         and expectation.get("status") == EXPECT_STATUS
         and seal.get("required_finalizer_service_gate") == service
         and expectation.get("required_finalizer_service_gate") == service
         and seal.get("formal_credit") == expectation.get("formal_credit") == 0
         and seal.get("manifest_authorized") is False
         and expectation.get("manifest_authorized") is False
         and seal.get("authority_minted") is False
         and expectation.get("authority_minted") is False,
         "conditional seal/expectation governance")

    manifest_dir = inside(args.manifest_dir)
    manifest, manifest_record = document(manifest_dir / "manifest_receipt.json",
                                         "manifest_receipt_sha256")
    payload_path = manifest_dir / "payload_manifest.sha256"
    root_path = manifest_dir / "root_manifest.sha256"
    parse_manifest(payload_path); parse_manifest(root_path)
    need(manifest_record["sha256"] == args.expect_manifest_file_sha256
         and manifest["manifest_receipt_sha256"]
             == args.expect_manifest_object_sha256
         and manifest.get("schema") == MANIFEST_SCHEMA
         and manifest.get("formal_credit") == 0
         and manifest.get("manifest_authorized") is False
         and manifest.get("authority_minted") is False,
         "manifest boundary")
    outer, outer_record = document(inside(args.outer_file),
                                    "outer_verification_sha256")
    need(outer_record["sha256"] == args.expect_outer_file_sha256
         and outer["outer_verification_sha256"] == args.expect_outer_object_sha256
         and outer.get("schema") == OUTER_SCHEMA
         and outer.get("outer_is_conditional_until_finalizer_service_clean_success")
             is True and outer.get("formal_credit") == 0
         and outer.get("manifest_authorized") is False
         and outer.get("authority_minted") is False,
         "outer boundary")
    candidate = inside(args.candidate_dir)
    need({path.name for path in candidate.iterdir()} == CANDIDATE_FILES,
         "candidate inventory")
    post_dir = inside(args.post_dir)
    output = inside(args.output_dir, absent=True)
    need(not output.exists()
         and str(output.relative_to(ROOT)) == seal.get("anticipated_dir"),
         "fresh exact anticipated path")
    output.mkdir(parents=True, mode=0o700)
    fsync_directory(output)
    fsync_directory(output.parent)
    payload_paths = {seal_dir / "conditional_seal.json", seal_payload, seal_root,
        seal_dir / "terminal_expectation.json",
        manifest_dir / "manifest_receipt.json", payload_path, root_path,
        inside(args.outer_file), post_dir / "post_integrity_evidence.json",
        post_dir / "authority_records.jsonl", SELF}
    payload_paths.update(candidate / name for name in CANDIDATE_FILES)
    anticipated_payload = output / "payload_manifest.sha256"
    write_once(anticipated_payload, manifest_bytes(payload_paths))
    anticipated_root = output / "root_manifest.sha256"
    write_once(anticipated_root, manifest_bytes({seal_root, root_path,
        inside(args.outer_file), anticipated_payload, SELF}))
    body = {"schema": ANTICIPATED_SCHEMA, "status": ANTICIPATED_STATUS,
        "plan_file_sha256": plan_record["sha256"],
        "plan_object_sha256": plan["plan_sha256"],
        "conditional_seal_file_sha256": seal_record["sha256"],
        "conditional_seal_object_sha256": seal["conditional_seal_sha256"],
        "terminal_expectation_file_sha256": expectation_record["sha256"],
        "terminal_expectation_object_sha256":
            expectation["terminal_expectation_sha256"],
        "manifest_receipt_file_sha256": manifest_record["sha256"],
        "manifest_receipt_object_sha256": manifest["manifest_receipt_sha256"],
        "outer_verification_file_sha256": outer_record["sha256"],
        "outer_verification_object_sha256": outer["outer_verification_sha256"],
        "anticipated_payload_manifest_file_sha256":
            record(anticipated_payload)["sha256"],
        "anticipated_root_manifest_file_sha256": record(anticipated_root)["sha256"],
        "required_finalizer_service_gate": service,
        "validator_negative_case_count": 70,
        "publication_lock_preflight_case_count": 8,
        "total_integrity_check_count": 78,
        "independent_no_import_replay_source_sha256": args.expect_self_sha256,
        "official_authority_definition": expectation["official_authority_definition"],
        "orphan_PASS_authority_eligible": False,
        "exact_math": EXPECTED, "formal_credit": 0,
        "manifest_authorized": False, "authority_minted": False,
        "C27R2": "AUDIT_HOLD_UNAUTHORIZED", "C28_C29": "UNAUTHORIZED",
        "CM2": "NO-GO_FOR_CLAIM"}
    receipt = {**body, "anticipated_terminal_receipt_sha256": digest(body)}
    receipt_path = output / "anticipated_terminal_receipt.json"
    write_once(receipt_path, canonical(receipt) + b"\n")
    replay_body = {"schema": REPLAY_SCHEMA, "status": ANTICIPATED_STATUS,
        "anticipated_terminal_receipt_file_sha256": record(receipt_path)["sha256"],
        "anticipated_terminal_receipt_object_sha256":
            receipt["anticipated_terminal_receipt_sha256"],
        "anticipated_payload_manifest_file_sha256":
            record(anticipated_payload)["sha256"],
        "anticipated_root_manifest_file_sha256": record(anticipated_root)["sha256"],
        "independent_no_import_replay_source_sha256": args.expect_self_sha256,
        "required_finalizer_service_gate": service,
        "validator_negative_case_count": 70,
        "publication_lock_preflight_case_count": 8,
        "total_integrity_check_count": 78,
        "formal_credit": 0, "manifest_authorized": False,
        "authority_minted": False, "C27R2": "AUDIT_HOLD_UNAUTHORIZED",
        "CM2": "NO-GO_FOR_CLAIM"}
    replay = {**replay_body, "anticipated_replay_sha256": digest(replay_body)}
    write_once(output / "anticipated_replay.json", canonical(replay) + b"\n")
    need({path.name for path in output.iterdir()} == {
        "anticipated_replay.json", "anticipated_terminal_receipt.json",
        "payload_manifest.sha256", "root_manifest.sha256"}
        and not (output / "PASS.lock").exists(),
        "anticipated exact inventory/no PASS")
    return replay


def self_test() -> dict[str, Any]:
    need(FORMAL_EXECUTION_AUTHORIZED is False
         and BOUNDARY_CONTRACT_FROZEN_GO is False,
         "development chain remains execution-disabled")
    try:
        _write_all(-1, b"x", lambda _fd, _raw: 0)
        raise Blocked("zero-progress writer unexpectedly accepted")
    except Blocked as error:
        need(str(error) == "write made positive progress",
             "zero-progress write fixture")
    need(independence() == record(SELF)["sha256"],
         "no-import independence")
    with tempfile.TemporaryDirectory(dir=ROOT / ".cm2-runtime",
            prefix="c27r2-anticipated-v4-selftest-") as raw:
        root = Path(raw); one = root / "one"; two = root / "two"
        one.write_bytes(b"one\n"); two.write_bytes(b"two\n")
        need(manifest_bytes({one, two}) == manifest_bytes({two, one})
             and not (root / "PASS.lock").exists(),
             "real deterministic no-PASS fixture")
    return {"status": "PASS_C27R2_RELEASE_REPAIR_ANTICIPATED_V4_SELF_TEST"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    for name in ("plan", "seal-dir", "manifest-dir", "outer-file",
        "candidate-dir", "post-dir", "output-dir", "expect-self-sha256",
        "expect-plan-file-sha256", "expect-plan-object-sha256",
        "expect-seal-file-sha256", "expect-seal-object-sha256",
        "expect-expectation-file-sha256", "expect-expectation-object-sha256",
        "expect-manifest-file-sha256", "expect-manifest-object-sha256",
        "expect-outer-file-sha256", "expect-outer-object-sha256"):
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
                 "all frozen inputs required")
            result = execute(args)
        sys.stdout.buffer.write(canonical({"CM2": "NO-GO_FOR_CLAIM",
            "formal_credit": 0, "status": result["status"]}) + b"\n")
        return 0
    except (Blocked, OSError, ValueError, KeyError, TypeError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
