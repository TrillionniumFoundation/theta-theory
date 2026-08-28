#!/usr/bin/env python3
"""Build a strictly conditional C27R2 v4 seal; never mint authority.

The output contains manifests, a conditional seal, and a terminal expectation
whose governance remains unauthorized.  It contains no PASS and no official
terminal receipt.  Only the separately audited finalizer may write the six
official terminal members and PASS last.
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
MANIFEST_STATUS = (
    "PASS_C27R2_RELEASE_REPAIR_V4_EXACT_ROLE_MANIFESTS_POST_VALIDATOR70_LOCK8_"
    "ACTUAL_V2_PREDECESSOR_ONLY_AND_HISTORICAL_EXCLUSION_CLOSED__ZERO_"
    "CREDIT_PENDING_OUTER"
)
OUTER_SCHEMA = BASE + "outer-verification.v4"
OUTER_STATUS = (
    "PASS_INDEPENDENT_C27R2_RELEASE_REPAIR_FULL_LEDGER_EDGE_DSU_FROZEN_"
    "C15_MEMBER_UNIVERSE_MANIFEST_VALIDATOR70_LOCK8_AND_CORE_OBJECT_REPLAY__"
    "CONDITIONAL_ZERO_CREDIT_PENDING_TERMINAL"
)
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
EXPECTED = {
    "frozen_C15_components": 57_876, "post_C27R2_components": 43_684,
    "proof_derived_component_edges": 14_860,
    "successful_DSU_merges": 14_192, "cycle_edges": 668,
    "frozen_C15_members": 502_204,
    "total_unordered_member_pairs": 126_104_177_706,
    "within_post_component_member_pairs": 542_179_508,
    "cross_post_component_member_pairs": 125_561_998_198,
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
    need(relative.parts and all(part not in {"", ".", ".."}
                                for part in relative.parts), "canonical path")
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


def service_contract(plan: dict[str, Any]) -> dict[str, Any]:
    value = plan.get("finalizer_service")
    need(type(value) is dict and set(value) == {
        "unit", "launch_mode", "invocation_binding", "expected_result",
        "expected_exec_main_code", "expected_exec_main_status",
        "expected_load_state", "expected_active_state", "expected_sub_state",
        "fragment_path"}
        and type(value["unit"]) is str and value["unit"].startswith("cm2-")
        and value["unit"].endswith(".service")
        and value["launch_mode"] == "EXPLICIT_USER_BUS_SYSTEMD_RUN_TRANSIENT_V1"
        and value["invocation_binding"]
            == "CAPTURE_FINALIZER_ENV_AND_MATCH_POST_EXIT_SYSTEMD_SHOW"
        and value["expected_result"] == "success"
        and value["expected_exec_main_code"] == 1
        and value["expected_exec_main_status"] == 0
        and value["expected_load_state"] == "loaded"
        and value["expected_active_state"] == "inactive"
        and value["expected_sub_state"] == "dead"
        and value["fragment_path"]
            == f"/run/user/{os.getuid()}/systemd/transient/{value['unit']}",
        "unit/ExecStart-via-template/FragmentPath/clean finalizer contract")
    return value


def execute(args: argparse.Namespace) -> dict[str, Any]:
    need(FORMAL_EXECUTION_AUTHORIZED and BOUNDARY_CONTRACT_FROZEN_GO,
         "boundary v4 NO-GO; append-only boundary v5 independent GO required")
    pins = (args.expect_self_sha256, args.expect_plan_file_sha256,
        args.expect_plan_object_sha256, args.expect_manifest_file_sha256,
        args.expect_manifest_object_sha256, args.expect_payload_sha256,
        args.expect_root_sha256, args.expect_outer_file_sha256,
        args.expect_outer_object_sha256,
        args.expect_anticipated_builder_sha256)
    need(all(valid_sha(value) for value in pins)
         and record(SELF)["sha256"] == args.expect_self_sha256, "all pins")
    plan, plan_record = document(inside(args.plan), "plan_sha256")
    need(plan_record["sha256"] == args.expect_plan_file_sha256
         and plan["plan_sha256"] == args.expect_plan_object_sha256
         and plan.get("schema") == PLAN_SCHEMA and plan.get("status") == PLAN_STATUS
         and plan.get("validator_negative_case_count") == 70
         and plan.get("publication_lock_preflight_case_count") == 8
         and plan.get("total_integrity_check_count") == 78
         and "case_count" not in plan and plan.get("exact_math") == EXPECTED
         and plan.get("formal_credit") == 0
         and plan.get("manifest_authorized") is False
         and plan.get("authority_minted") is False,
         "frozen plan")
    service = service_contract(plan)
    anticipated_source = inside(args.anticipated_builder_source)
    need(record(anticipated_source)["sha256"]
             == args.expect_anticipated_builder_sha256
         and plan.get("sources", {}).get("anticipated_terminal_builder") == {
             "path": record(anticipated_source)["path"],
             "sha256": args.expect_anticipated_builder_sha256},
         "anticipated builder source pin")

    manifest_dir = inside(args.manifest_dir)
    need({path.name for path in manifest_dir.iterdir()} == {
        "manifest_receipt.json", "payload_manifest.sha256",
        "root_manifest.sha256"}, "manifest inventory")
    manifest, manifest_record = document(manifest_dir / "manifest_receipt.json",
                                         "manifest_receipt_sha256")
    payload_path = manifest_dir / "payload_manifest.sha256"
    root_path = manifest_dir / "root_manifest.sha256"
    payload = parse_manifest(payload_path); root = parse_manifest(root_path)
    need(manifest_record["sha256"] == args.expect_manifest_file_sha256
         and manifest["manifest_receipt_sha256"]
             == args.expect_manifest_object_sha256
         and manifest.get("schema") == MANIFEST_SCHEMA
         and manifest.get("status") == MANIFEST_STATUS
         and record(payload_path)["sha256"] == args.expect_payload_sha256
         and record(root_path)["sha256"] == args.expect_root_sha256
         and manifest.get("payload_member_count") == len(payload)
         and manifest.get("root_member_count") == len(root)
         and manifest.get("exact_math") == EXPECTED
         and manifest.get("formal_credit") == 0
         and manifest.get("manifest_authorized") is False
         and manifest.get("authority_minted") is False,
         "manifest conditional boundary")
    outer, outer_record = document(inside(args.outer_file),
                                    "outer_verification_sha256")
    need(outer_record["sha256"] == args.expect_outer_file_sha256
         and outer["outer_verification_sha256"] == args.expect_outer_object_sha256
         and outer.get("schema") == OUTER_SCHEMA and outer.get("status") == OUTER_STATUS
         and outer.get("manifest_receipt_file_sha256")
             == args.expect_manifest_file_sha256
         and outer.get("manifest_receipt_object_sha256")
             == args.expect_manifest_object_sha256
         and outer.get("exact_math") == EXPECTED
         and outer.get("outer_is_conditional_until_finalizer_service_clean_success")
             is True and outer.get("formal_credit") == 0
         and outer.get("manifest_authorized") is False
         and outer.get("authority_minted") is False,
         "outer conditional boundary")
    output = inside(args.output_dir, absent=True)
    anticipated_dir = inside(args.anticipated_dir, absent=True)
    need(not output.exists() and not anticipated_dir.exists()
         and output != anticipated_dir and output.parent == anticipated_dir.parent,
         "fresh separated seal/anticipated paths")
    output.mkdir(parents=True, mode=0o700)
    fsync_directory(output)
    fsync_directory(output.parent)
    seal_payload = output / "seal_payload_manifest.sha256"
    write_once(seal_payload, manifest_bytes({inside(args.plan),
        manifest_dir / "manifest_receipt.json", payload_path, root_path,
        inside(args.outer_file), SELF, anticipated_source}))
    seal_root = output / "seal_root_manifest.sha256"
    write_once(seal_root, manifest_bytes({seal_payload, root_path,
        inside(args.outer_file), anticipated_source}))
    seal_body = {"schema": SEAL_SCHEMA, "status": SEAL_STATUS,
        "plan_file_sha256": plan_record["sha256"],
        "plan_object_sha256": plan["plan_sha256"],
        "manifest_receipt_file_sha256": manifest_record["sha256"],
        "manifest_receipt_object_sha256": manifest["manifest_receipt_sha256"],
        "outer_verification_file_sha256": outer_record["sha256"],
        "outer_verification_object_sha256": outer["outer_verification_sha256"],
        "seal_payload_manifest_file_sha256": record(seal_payload)["sha256"],
        "seal_root_manifest_file_sha256": record(seal_root)["sha256"],
        "anticipated_dir": str(anticipated_dir.relative_to(ROOT)),
        "anticipated_builder_source_sha256": args.expect_anticipated_builder_sha256,
        "required_finalizer_service_gate": service,
        "validator_negative_case_count": 70,
        "publication_lock_preflight_case_count": 8,
        "total_integrity_check_count": 78,
        "exact_math": EXPECTED, "terminal_replay_completed": False,
        "finalizer_service_clean_success_observed": False,
        "formal_credit": 0, "manifest_authorized": False,
        "authority_minted": False, "C27R2": "AUDIT_HOLD_UNAUTHORIZED",
        "C28_C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM"}
    seal = {**seal_body, "conditional_seal_sha256": digest(seal_body)}
    seal_path = output / "conditional_seal.json"
    write_once(seal_path, canonical(seal) + b"\n")
    expectation_body = {"schema": EXPECT_SCHEMA, "status": EXPECT_STATUS,
        "conditional_seal_file_sha256": record(seal_path)["sha256"],
        "conditional_seal_object_sha256": seal["conditional_seal_sha256"],
        "seal_payload_manifest_file_sha256": record(seal_payload)["sha256"],
        "seal_root_manifest_file_sha256": record(seal_root)["sha256"],
        "anticipated_dir": seal["anticipated_dir"],
        "required_finalizer_service_gate": service,
        "validator_negative_case_count": 70,
        "publication_lock_preflight_case_count": 8,
        "total_integrity_check_count": 78,
        "official_authority_definition":
            "EXACT_TERMINAL_INVENTORY_AND_PASS_LAST_PLUS_CURRENT_FINALIZER_"
            "UNIT_RESULT_SUCCESS_EXEC_MAIN_STATUS_0_EXACT_INVOCATION",
        "orphan_PASS_authority_eligible": False,
        "exact_math": EXPECTED, "formal_credit": 0,
        "manifest_authorized": False, "authority_minted": False,
        "C27R2": "AUDIT_HOLD_UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM"}
    expectation = {**expectation_body,
        "terminal_expectation_sha256": digest(expectation_body)}
    write_once(output / "terminal_expectation.json",
               canonical(expectation) + b"\n")
    need({path.name for path in output.iterdir()} == {
        "conditional_seal.json", "seal_payload_manifest.sha256",
        "seal_root_manifest.sha256", "terminal_expectation.json"}
        and not (output / "PASS.lock").exists(),
        "exact conditional output/no PASS")
    return seal


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
    with tempfile.TemporaryDirectory(dir=ROOT / ".cm2-runtime",
            prefix="c27r2-seal-v4-selftest-") as raw:
        root = Path(raw); one = root / "one"; two = root / "two"
        one.write_bytes(b"1\n"); two.write_bytes(b"2\n")
        first = manifest_bytes({one, two}); second = manifest_bytes({two, one})
        need(first == second and b"PASS" not in first,
             "real deterministic conditional manifest fixture")
    body = {"schema": SEAL_SCHEMA, "status": SEAL_STATUS,
            "authority_minted": False, "manifest_authorized": False}
    need(digest(body) == hashlib.sha256(canonical(body)).hexdigest(),
         "conditional object closure")
    return {"status": "PASS_C27R2_RELEASE_REPAIR_CONDITIONAL_SEAL_V4_SELF_TEST"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    for name in ("plan", "manifest-dir", "outer-file",
        "anticipated-builder-source", "output-dir", "anticipated-dir",
        "expect-self-sha256", "expect-plan-file-sha256",
        "expect-plan-object-sha256", "expect-manifest-file-sha256",
        "expect-manifest-object-sha256", "expect-payload-sha256",
        "expect-root-sha256", "expect-outer-file-sha256",
        "expect-outer-object-sha256", "expect-anticipated-builder-sha256"):
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
