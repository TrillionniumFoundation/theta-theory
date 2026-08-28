#!/usr/bin/env python3
"""Official C27R2 v5 terminal finalizer with PASS as the last FS mutation.

Authority is a joint gate: this exact six-file terminal (PASS written last)
plus the current finalizer unit's post-exit Result=success, ExecMainStatus=0
and exact InvocationID.  A filesystem PASS without that current unit tuple is
explicitly ineligible and must be rejected by downstream watchers.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
import time
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
BASE = "cm2.round306c27r2.source-g-authority-v2.release-repair."
PLAN_SCHEMA = BASE + "chain-plan.v5"
PLAN_STATUS = (
    "FROZEN_C27R2_RELEASE_REPAIR_V5_EXACT70_PLUS_LOCK8_PLAN__EXECUTION_DISABLED_"
    "PENDING_INDEPENDENT_FULL_CHAIN_AUDIT"
)
ANTICIPATED_SCHEMA = BASE + "anticipated-terminal-receipt.v5"
ANTICIPATED_STATUS = (
    "PASS_C27R2_RELEASE_REPAIR_V5_INDEPENDENT_ANTICIPATED_BYTE_REPLAY__"
    "ZERO_CREDIT_PENDING_OFFICIAL_FINALIZER_AND_SERVICE_CLEAN_SUCCESS"
)
ANTICIPATED_REPLAY_SCHEMA = BASE + "anticipated-terminal-replay.v5"
MANIFEST_SCHEMA = BASE + "manifest-receipt.v5"
OUTER_SCHEMA = BASE + "outer-verification.v5"
SEAL_SCHEMA = BASE + "conditional-seal.v5"
EXPECT_SCHEMA = BASE + "terminal-expectation.v5"
MANIFEST_STATUS = (
    "PASS_C27R2_RELEASE_REPAIR_V5_EXACT_ROLE_MANIFESTS_POST_VALIDATOR70_LOCK8_"
    "ACTUAL_V2_PREDECESSOR_ONLY_AND_HISTORICAL_EXCLUSION_CLOSED__ZERO_"
    "CREDIT_PENDING_OUTER"
)
OUTER_STATUS = (
    "PASS_INDEPENDENT_C27R2_RELEASE_REPAIR_FULL_LEDGER_EDGE_DSU_FROZEN_"
    "C15_MEMBER_UNIVERSE_MANIFEST_VALIDATOR70_LOCK8_AND_CORE_OBJECT_REPLAY__"
    "CONDITIONAL_ZERO_CREDIT_PENDING_TERMINAL"
)
SEAL_STATUS = (
    "PASS_CONDITIONAL_C27R2_RELEASE_REPAIR_V5_SEAL_EXACT_MANIFEST_OUTER_"
    "AND_FINALIZER_SERVICE_EXPECTATION__ZERO_CREDIT_NOT_AUTHORITY"
)
EXPECT_STATUS = (
    "PASS_C27R2_RELEASE_REPAIR_V5_TERMINAL_EXPECTATION_BYTES_FROZEN__"
    "PENDING_ANTICIPATED_REPLAY_AND_FINALIZER_SERVICE_CLEAN_SUCCESS"
)
RUN_SCHEMA = BASE + "release-repair-process-run-attestation.v5"
RUN_STATUS = (
    "PASS_C27R2_RELEASE_REPAIR_PROCESS_EXIT0_NULL_SIGNAL_EMPTY_STDERR_"
    "EXACT_SPEC_PINSET_ARGV_ENV_PRE_POST_FULL9STAT_AND_OUTPUT_INVENTORY__"
    "ZERO_CREDIT"
)
RUN_PASS = b"PASS_C27R2_RELEASE_REPAIR_V5_PROCESS_TRANSACTION__ZERO_CREDIT\n"
TERMINAL_SCHEMA = BASE + "terminal-receipt.v5"
TERMINAL_REPLAY_SCHEMA = BASE + "terminal-replay.v5"
CHAIN_SCHEMA = BASE + "release-chain-status.v5"
TERMINAL_STATUS = (
    "PASS_C27R2_RELEASE_REPAIR_V5_FILESYSTEM_TERMINAL_PASS_LAST__JOINT_"
    "AUTHORITY_REQUIRES_CURRENT_FINALIZER_UNIT_CLEAN_SUCCESS"
)
PASS_BYTES = (
    b"PASS_C27R2_RELEASE_REPAIR_V5_JOINT_SERVICE_GATED_TERMINAL__"
    b"C28_C29_REBIND_PENDING\n"
)
TERMINAL_FILES = {
    "PASS.lock", "chain_status.json", "payload_manifest.sha256",
    "root_manifest.sha256", "terminal_receipt.json", "terminal_replay.json",
}
ANTICIPATED_FILES = {"anticipated_replay.json",
    "anticipated_terminal_receipt.json", "payload_manifest.sha256",
    "root_manifest.sha256"}
RUN_FILES = {"PASS.lock", "exit_code.txt", "signal.json", "stderr.log",
    "stdout.log", "timing.json", "input_pre.json", "input_post.json",
    "output_validation.json", "runner_start.json", "run_attestation.json"}
EXPECTED = {
    "frozen_C15_components": 57_876, "post_C27R2_components": 43_684,
    "proof_derived_component_edges": 14_860,
    "successful_DSU_merges": 14_192, "cycle_edges": 668,
    "frozen_C15_members": 502_204,
    "total_unordered_member_pairs": 126_104_177_706,
    "within_post_component_member_pairs": 542_179_508,
    "cross_post_component_member_pairs": 125_561_998_198,
}
BOUNDARY_CONTRACT_FROZEN_GO = False  # boundary v5 NO-GO; append-only v6 pending.
FORMAL_EXECUTION_AUTHORIZED = False  # Independent full-chain GO has not been minted.
LOCK_SCHEMA = BASE + "publication-lock.v1"
LOCK_STATUS = "FROZEN_ONE_SHOT_PUBLICATION_LOCK__NO_AUTHORITY"
LOCK_PROTOCOL = "FLOCK_EXCLUSIVE_WHOLE_PUBLICATION_WINDOW_V1"


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


def directory_identity(info: os.stat_result) -> list[int]:
    return [info.st_dev, info.st_ino, info.st_mode, info.st_uid, info.st_gid]


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


def read_current(path: Path) -> bytes:
    return capture(path)[0]


def document(path: Path, closure: str) -> tuple[dict[str, Any], dict[str, Any]]:
    raw, item = capture(path)
    need(raw.endswith(b"\n"), "newline")
    value = strict(raw[:-1])
    need(type(value) is dict and canonical(value) == raw[:-1], "canonical JSON")
    body = dict(value); claim = body.pop(closure, None)
    need(valid_sha(claim) and claim == digest(body), "object closure")
    return value, item


def plain_document(path: Path) -> dict[str, Any]:
    raw, _ = capture(path)
    need(raw.endswith(b"\n"), "plain JSON newline")
    value = strict(raw[:-1])
    need(type(value) is dict and canonical(value) == raw[:-1],
         "canonical plain JSON")
    return value


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


def manifest_bytes(paths: set[Path], virtual: dict[Path, str] | None = None) -> bytes:
    virtual = virtual or {}; rows = []
    for path in sorted(paths | set(virtual)):
        claim = virtual[path] if path in virtual else record(path)["sha256"]
        need(valid_sha(claim), "manifest SHA")
        rows.append(f"{claim}  {path.relative_to(ROOT)}\n")
    need(len(rows) > 0, "nonempty manifest")
    return "".join(rows).encode("ascii")


def parse_manifest_current(path: Path) -> tuple[dict[str, str], bytes]:
    raw, _ = capture(path)
    need(raw.endswith(b"\n"), "manifest newline")
    result: dict[str, str] = {}
    for line in raw.decode("ascii").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\x00\r\n]+)", line)
        need(match is not None, "manifest canonical row")
        claim, shown = match.groups()
        need(shown not in result and record(inside(shown))["sha256"] == claim,
             "manifest unique current member")
        result[shown] = claim
    paths = {inside(shown) for shown in result}
    need(result and list(result) == sorted(result)
         and manifest_bytes(paths) == raw, "manifest exact canonical rebuild")
    return result, raw


def parse_manifest_bytes(raw: bytes) -> dict[str, str]:
    need(raw.endswith(b"\n"), "manifest bytes newline")
    result: dict[str, str] = {}
    for line in raw.decode("ascii").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\x00\r\n]+)", line)
        need(match is not None, "manifest bytes row")
        claim, shown = match.groups()
        need(shown not in result, "manifest bytes unique member")
        result[shown] = claim
    need(result and list(result) == sorted(result),
         "manifest bytes sorted nonempty")
    return result


def unique_manifest_member(manifest: dict[str, str], file_sha: str,
                           basename: str) -> Path:
    matches = [inside(path) for path, claim in manifest.items()
               if claim == file_sha and Path(path).name == basename]
    need(len(matches) == 1, "unique predecessor in anticipated payload:" + basename)
    return matches[0]


def reconstruct_anticipated(anticipated: Path, plan: dict[str, Any],
                            plan_record: dict[str, Any],
                            service: dict[str, Any], receipt: dict[str, Any],
                            replay: dict[str, Any]) -> dict[str, Any]:
    """Independently rebuild the canonical four-file anticipated package."""
    payload_path = anticipated / "payload_manifest.sha256"
    root_path = anticipated / "root_manifest.sha256"
    payload, payload_raw = parse_manifest_current(payload_path)
    root, root_raw = parse_manifest_current(root_path)
    payload_file_sha = hashlib.sha256(payload_raw).hexdigest()
    root_file_sha = hashlib.sha256(root_raw).hexdigest()
    seal_path = unique_manifest_member(payload,
        receipt.get("conditional_seal_file_sha256"), "conditional_seal.json")
    expectation_path = unique_manifest_member(payload,
        receipt.get("terminal_expectation_file_sha256"), "terminal_expectation.json")
    manifest_path = unique_manifest_member(payload,
        receipt.get("manifest_receipt_file_sha256"), "manifest_receipt.json")
    outer_path = unique_manifest_member(payload,
        receipt.get("outer_verification_file_sha256"), "outer_verification.json")
    seal, seal_record = document(seal_path, "conditional_seal_sha256")
    expectation, expectation_record = document(
        expectation_path, "terminal_expectation_sha256")
    manifest, manifest_record = document(manifest_path, "manifest_receipt_sha256")
    outer, outer_record = document(outer_path, "outer_verification_sha256")
    anticipated_source = plan.get("sources", {}).get("anticipated_terminal_builder")
    need(type(anticipated_source) is dict
         and set(anticipated_source) == {"path", "sha256"}
         and record(inside(anticipated_source["path"]))["sha256"]
             == anticipated_source["sha256"],
         "current anticipated builder source pin")
    planned_inputs = {row.get("path"): row.get("sha256")
        for row in plan.get("finalizer_input_members", [])
        if type(row) is dict}
    need(all(planned_inputs.get(path) == claim
             for path, claim in {**payload, **root}.items())
         and all(planned_inputs.get(item["path"]) == item["sha256"]
                 for item in (seal_record, expectation_record,
                              manifest_record, outer_record)),
         "anticipated predecessor manifests/documents bound by finalizer plan pins")
    expected_payload_names = {
        "conditional_seal.json", "seal_payload_manifest.sha256",
        "seal_root_manifest.sha256", "terminal_expectation.json",
        "manifest_receipt.json", "payload_manifest.sha256",
        "root_manifest.sha256", "outer_verification.json",
        "post_integrity_evidence.json", "authority_records.jsonl",
        "member_to_post_component.jsonl.gz",
        "old_c15_component_to_post_component.jsonl.gz",
        "post_component_census.jsonl.gz", "result.json",
        Path(anticipated_source["path"]).name,
    }
    need(len(payload) == 15
         and {Path(path).name for path in payload} == expected_payload_names,
         "anticipated payload exact fifteen-member semantic inventory")
    expected_root_names = {"seal_root_manifest.sha256", "root_manifest.sha256",
        "outer_verification.json", "payload_manifest.sha256",
        Path(anticipated_source["path"]).name}
    need(len(root) == 5 and {Path(path).name for path in root} == expected_root_names
         and root.get(str(payload_path.relative_to(ROOT))) == payload_file_sha,
         "anticipated root exact five-member current payload binding")
    need(seal.get("schema") == SEAL_SCHEMA
         and seal.get("status") == SEAL_STATUS
         and expectation.get("schema") == EXPECT_SCHEMA
         and expectation.get("status") == EXPECT_STATUS
         and manifest.get("schema") == MANIFEST_SCHEMA
         and manifest.get("status") == MANIFEST_STATUS
         and outer.get("schema") == OUTER_SCHEMA
         and outer.get("status") == OUTER_STATUS
         and seal.get("plan_file_sha256") == plan_record["sha256"]
         and seal.get("plan_object_sha256") == plan["plan_sha256"]
         and seal.get("manifest_receipt_file_sha256") == manifest_record["sha256"]
         and seal.get("manifest_receipt_object_sha256")
             == manifest["manifest_receipt_sha256"]
         and seal.get("outer_verification_file_sha256") == outer_record["sha256"]
         and seal.get("outer_verification_object_sha256")
             == outer["outer_verification_sha256"]
         and expectation.get("conditional_seal_file_sha256")
             == seal_record["sha256"]
         and expectation.get("conditional_seal_object_sha256")
             == seal["conditional_seal_sha256"]
         and outer.get("manifest_receipt_file_sha256") == manifest_record["sha256"]
         and outer.get("manifest_receipt_object_sha256")
             == manifest["manifest_receipt_sha256"]
         and all(value.get("exact_math") == EXPECTED
                 for value in (seal, expectation, manifest, outer))
         and all(value.get("validator_negative_case_count") == 70
                 and value.get("publication_lock_preflight_case_count") == 8
                 and value.get("total_integrity_check_count") == 78
                 for value in (seal, expectation, manifest, outer))
         and seal.get("required_finalizer_service_gate") == service
         and expectation.get("required_finalizer_service_gate") == service
         and all(value.get("formal_credit") == 0
                 and value.get("manifest_authorized") is False
                 and value.get("authority_minted") is False
                 for value in (seal, expectation, manifest, outer)),
         "anticipated predecessors current schemas/governance/service")
    receipt_body = {"schema": ANTICIPATED_SCHEMA, "status": ANTICIPATED_STATUS,
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
        "anticipated_payload_manifest_file_sha256": payload_file_sha,
        "anticipated_root_manifest_file_sha256": root_file_sha,
        "required_finalizer_service_gate": service,
        "validator_negative_case_count": 70,
        "publication_lock_preflight_case_count": 8,
        "total_integrity_check_count": 78,
        "independent_no_import_replay_source_sha256": anticipated_source["sha256"],
        "official_authority_definition": expectation["official_authority_definition"],
        "orphan_PASS_authority_eligible": False, "exact_math": EXPECTED,
        "formal_credit": 0, "manifest_authorized": False,
        "authority_minted": False, "C27R2": "AUDIT_HOLD_UNAUTHORIZED",
        "C28_C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM"}
    expected_receipt = {**receipt_body,
        "anticipated_terminal_receipt_sha256": digest(receipt_body)}
    receipt_file_sha = hashlib.sha256(canonical(expected_receipt) + b"\n").hexdigest()
    replay_body = {"schema": ANTICIPATED_REPLAY_SCHEMA,
        "status": ANTICIPATED_STATUS,
        "anticipated_terminal_receipt_file_sha256": receipt_file_sha,
        "anticipated_terminal_receipt_object_sha256":
            expected_receipt["anticipated_terminal_receipt_sha256"],
        "anticipated_payload_manifest_file_sha256": payload_file_sha,
        "anticipated_root_manifest_file_sha256": root_file_sha,
        "independent_no_import_replay_source_sha256": anticipated_source["sha256"],
        "required_finalizer_service_gate": service,
        "validator_negative_case_count": 70,
        "publication_lock_preflight_case_count": 8,
        "total_integrity_check_count": 78, "formal_credit": 0,
        "manifest_authorized": False, "authority_minted": False,
        "C27R2": "AUDIT_HOLD_UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM"}
    expected_replay = {**replay_body,
        "anticipated_replay_sha256": digest(replay_body)}
    need(receipt == expected_receipt and replay == expected_replay,
         "anticipated receipt/replay independently canonical reconstructed")
    return {"payload": payload, "root": root,
        "payload_file_sha256": payload_file_sha,
        "root_file_sha256": root_file_sha,
        "receipt_file_sha256": receipt_file_sha,
        "receipt_object_sha256": expected_receipt[
            "anticipated_terminal_receipt_sha256"],
        "replay_object_sha256": expected_replay["anticipated_replay_sha256"]}


def service_contract(plan: dict[str, Any]) -> dict[str, Any]:
    value = plan.get("finalizer_service")
    need(type(value) is dict and set(value) == {
        "unit", "launch_mode", "invocation_binding", "expected_result",
        "expected_exec_main_code", "expected_exec_main_status",
        "expected_load_state", "expected_active_state", "expected_sub_state",
        "fragment_path"}
        and value["expected_result"] == "success"
        and value["expected_exec_main_code"] == 1
        and value["expected_exec_main_status"] == 0
        and value["expected_load_state"] == "loaded"
        and value["expected_active_state"] == "active"
        and value["expected_sub_state"] == "exited"
        and value["launch_mode"] == "EXPLICIT_USER_BUS_SYSTEMD_RUN_TRANSIENT_V1"
        and type(value["unit"]) is str and value["unit"].startswith("cm2-")
        and value["unit"].endswith(".service")
        and value["fragment_path"]
            == f"/run/user/{os.getuid()}/systemd/transient/{value['unit']}"
        and value["invocation_binding"]
            == "CAPTURE_FINALIZER_ENV_AND_MATCH_POST_EXIT_SYSTEMD_SHOW",
        "future finalizer service contract")
    return value


def acquire_publication_lock(args: argparse.Namespace, plan: dict[str, Any],
                             plan_record: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    need(valid_sha(args.expect_publication_lock_file_sha256)
         and valid_sha(args.expect_publication_lock_object_sha256)
         and type(args.publication_lock_timeout_seconds) is str
         and args.publication_lock_timeout_seconds.isdigit(),
         "publication lock dynamic pins/timeout")
    timeout = int(args.publication_lock_timeout_seconds)
    need(1 <= timeout <= 300, "publication lock timeout bound")
    expected_stat = strict(args.expect_publication_lock_stat9_json.encode("ascii"))
    need(type(expected_stat) is list and len(expected_stat) == 9
         and all(type(value) is int for value in expected_stat),
         "publication lock stat9")
    contract = plan.get("publication_lock")
    need(type(contract) is dict and set(contract) == {
         "path", "schema", "status", "protocol"}
         and contract["path"] == args.publication_lock_path
         and contract["schema"] == LOCK_SCHEMA
         and contract["status"] == LOCK_STATUS
         and contract["protocol"] == LOCK_PROTOCOL,
         "plan publication lock contract")
    path = inside(args.publication_lock_path)
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
                         | getattr(os, "O_CLOEXEC", 0))
    try:
        info = os.fstat(descriptor)
        need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1
             and fingerprint(info) == expected_stat
             and fingerprint(os.stat(path, follow_symlinks=False)) == expected_stat,
             "publication lock FD/path identity")
        chunks: list[bytes] = []
        while block := os.read(descriptor, 1 << 20): chunks.append(block)
        raw = b"".join(chunks)
        need(hashlib.sha256(raw).hexdigest()
             == args.expect_publication_lock_file_sha256 and raw.endswith(b"\n"),
             "publication lock bytes")
        value = strict(raw[:-1]); body = dict(value)
        claim = body.pop("publication_lock_sha256", None)
        need(type(value) is dict and canonical(value) == raw[:-1]
             and claim == digest(body)
             and claim == args.expect_publication_lock_object_sha256
             and value.get("schema") == LOCK_SCHEMA
             and value.get("status") == LOCK_STATUS
             and value.get("protocol") == LOCK_PROTOCOL
             and value.get("plan_file_sha256") == plan_record["sha256"]
             and value.get("plan_object_sha256") == plan["plan_sha256"]
             and value.get("formal_credit") == 0
             and value.get("manifest_authorized") is False
             and value.get("authority_minted") is False,
             "publication lock canonical object/plan closure")
        deadline = time.monotonic() + timeout
        while True:
            try:
                fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                need(time.monotonic() < deadline, "publication lock timeout")
                time.sleep(0.05)
        need(fingerprint(os.fstat(descriptor)) == expected_stat
             and fingerprint(os.stat(path, follow_symlinks=False)) == expected_stat,
             "publication lock stable exclusive acquisition")
        return descriptor, value
    except BaseException:
        os.close(descriptor)
        raise


def terminal_models(model: dict[str, Any], payload_sha: str,
                    root_sha: str) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    service = model["service"]
    common = {"status": TERMINAL_STATUS,
        "plan_file_sha256": model["plan_file"],
        "plan_object_sha256": model["plan_object"],
        "anticipated_terminal_receipt_file_sha256": model["anticipated_file"],
        "anticipated_terminal_receipt_object_sha256": model["anticipated_object"],
        "anticipated_replay_file_sha256": model["replay_file"],
        "anticipated_replay_object_sha256": model["replay_object"],
        "anticipated_transaction_file_sha256": model["run_file"],
        "anticipated_transaction_object_sha256": model["run_object"],
        "publication_lock_object_sha256": model["publication_lock_object"],
        "terminal_payload_manifest_file_sha256": payload_sha,
        "terminal_root_manifest_file_sha256": root_sha,
        "required_finalizer_service_gate": service,
        "official_authority_definition":
            "EXACT_TERMINAL_INVENTORY_AND_PASS_LAST_PLUS_CURRENT_FINALIZER_"
            "UNIT_INVOCATION_EXECSTART_FRAGMENTPATH_AND_CLEAN_EXIT_TUPLE",
        "filesystem_terminal_complete": True,
        "authority_mint_is_joint_not_filesystem_only": True,
        "joint_service_gate_must_be_observed_after_finalizer_exit": True,
        "orphan_PASS_authority_eligible": False,
        "validator_negative_case_count": 70,
        "publication_lock_preflight_case_count": 8,
        "total_integrity_check_count": 78,
        "exact_math": EXPECTED, "formal_credit": 0,
        "manifest_authorized": False, "authority_minted": False,
        "manifest_authorized_when_joint_gate_observed": True,
        "authority_minted_when_joint_gate_observed": True,
        "C27R2": "FILESYSTEM_TERMINAL_COMPLETE_PENDING_POST_EXIT_SERVICE_GATE",
        "C28": "UNAUTHORIZED_PENDING_FRESH_REBIND",
        "C29": "UNAUTHORIZED_PENDING_FRESH_REBIND",
        "CM2": "NO-GO_FOR_CLAIM"}
    receipt_body = {"schema": TERMINAL_SCHEMA, **common}
    receipt = {**receipt_body, "terminal_receipt_sha256": digest(receipt_body)}
    replay_body = {"schema": TERMINAL_REPLAY_SCHEMA, **common,
        "terminal_receipt_object_sha256": receipt["terminal_receipt_sha256"],
        "independent_anticipated_byte_replay_verified": True}
    replay = {**replay_body, "terminal_replay_sha256": digest(replay_body)}
    chain_body = {"schema": CHAIN_SCHEMA, **common,
        "terminal_receipt_object_sha256": receipt["terminal_receipt_sha256"],
        "terminal_replay_object_sha256": replay["terminal_replay_sha256"]}
    chain = {**chain_body, "chain_status_sha256": digest(chain_body)}
    return receipt, replay, chain


def read_at(directory_fd: int, name: str) -> tuple[bytes, list[int]]:
    need("/" not in name and name not in {"", ".", ".."}, "flat terminal name")
    descriptor = os.open(name, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_CLOEXEC", 0), dir_fd=directory_fd)
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "terminal member regular single-link")
        chunks: list[bytes] = []
        while block := os.read(descriptor, 1 << 20):
            chunks.append(block)
        after = os.fstat(descriptor)
        current = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
        need(fingerprint(before) == fingerprint(after) == fingerprint(current),
             "terminal member stable full9stat through held dirfd")
        return b"".join(chunks), fingerprint(after)
    finally:
        os.close(descriptor)


def write_once_at(directory_fd: int, name: str, raw: bytes) -> dict[str, Any]:
    descriptor = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL
        | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0),
        0o400, dir_fd=directory_fd)
    try:
        _write_all(descriptor, raw)
        os.fsync(descriptor)
        written = fingerprint(os.fstat(descriptor))
    finally:
        os.close(descriptor)
    observed, reopened = read_at(directory_fd, name)
    need(observed == raw and hashlib.sha256(observed).hexdigest()
         == hashlib.sha256(raw).hexdigest() and written == reopened,
         "terminal O_EXCL member readback/hash/full9stat")
    return {"sha256": hashlib.sha256(raw).hexdigest(),
            "stat_fingerprint": reopened}


def exact_flat_inventory(directory_fd: int, expected: set[str]) -> None:
    names = os.listdir(directory_fd)
    need(set(names) == expected and len(names) == len(expected),
         "terminal exact flat inventory")
    for name in names:
        info = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
        need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1,
             "terminal rejects extra directory/link/device/multilink")


def commit_terminal_at(parent_fd: int, leaf: str, payload_raw: bytes,
                       root_raw: bytes, model: dict[str, Any],
                       terminate_after_pass: bool = False) -> dict[str, Any]:
    """One held parent dirfd, one terminal dirfd, O_EXCL members, PASS last."""
    need("/" not in leaf and leaf not in {"", ".", ".."},
         "single terminal leaf")
    parent_before = directory_identity(os.fstat(parent_fd))
    need(stat.S_ISDIR(os.fstat(parent_fd).st_mode), "held terminal parent dirfd")
    try:
        os.stat(leaf, dir_fd=parent_fd, follow_symlinks=False)
    except FileNotFoundError:
        pass
    else:
        raise Blocked("fresh terminal leaf already exists under held parent")
    os.mkdir(leaf, 0o700, dir_fd=parent_fd)
    terminal_fd = os.open(leaf, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0),
        dir_fd=parent_fd)
    try:
        need(directory_identity(os.fstat(parent_fd)) == parent_before,
             "held terminal parent stable through mkdirat")
        os.fsync(parent_fd)
        os.fsync(terminal_fd)
        payload_rows = parse_manifest_bytes(payload_raw)
        root_rows = parse_manifest_bytes(root_raw)
        payload_sha = hashlib.sha256(payload_raw).hexdigest()
        need(sum(claim == payload_sha
                 and Path(shown).name == "payload_manifest.sha256"
                 for shown, claim in root_rows.items()) == 1,
             "terminal root uniquely binds current payload manifest SHA")
        payload_item = write_once_at(
            terminal_fd, "payload_manifest.sha256", payload_raw)
        root_item = write_once_at(terminal_fd, "root_manifest.sha256", root_raw)
        receipt, replay, chain = terminal_models(model,
            payload_item["sha256"], root_item["sha256"])
        prepass = {
            "terminal_receipt.json": canonical(receipt) + b"\n",
            "terminal_replay.json": canonical(replay) + b"\n",
            "chain_status.json": canonical(chain) + b"\n",
        }
        for name, raw in prepass.items():
            write_once_at(terminal_fd, name, raw)
        for name, closure, expected in (
            ("terminal_receipt.json", "terminal_receipt_sha256", receipt),
            ("terminal_replay.json", "terminal_replay_sha256", replay),
            ("chain_status.json", "chain_status_sha256", chain),
        ):
            raw, _ = read_at(terminal_fd, name)
            need(raw.endswith(b"\n"), "terminal canonical JSON newline")
            value = strict(raw[:-1]); body = dict(value)
            claim = body.pop(closure, None)
            need(type(value) is dict and canonical(value) == raw[:-1]
                 and claim == digest(body) and value == expected,
                 "terminal pre-PASS canonical object reconstruction")
        exact_flat_inventory(terminal_fd, TERMINAL_FILES - {"PASS.lock"})
        os.fsync(terminal_fd)

        # The PASS create is the strict final filesystem mutation.  Only
        # readback/stat and durability syscalls follow it; the formal branch
        # terminates with os._exit so no Python cleanup can mutate the tree.
        write_once_at(terminal_fd, "PASS.lock", PASS_BYTES)
        exact_flat_inventory(terminal_fd, TERMINAL_FILES)
        pass_observed, _ = read_at(terminal_fd, "PASS.lock")
        need(pass_observed == PASS_BYTES, "terminal exact PASS readback")
        os.fsync(terminal_fd)
        if terminate_after_pass:
            os._exit(0)
        return replay
    finally:
        os.close(terminal_fd)


def commit_terminal(output: Path, payload_raw: bytes, root_raw: bytes,
                    model: dict[str, Any],
                    terminate_after_pass: bool = False) -> dict[str, Any]:
    need(not output.exists() and not output.is_symlink()
         and output.parent.is_dir() and not output.parent.is_symlink(),
         "fresh terminal and existing parent")
    parent_fd = os.open(output.parent, os.O_RDONLY
        | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_CLOEXEC", 0))
    try:
        return commit_terminal_at(parent_fd, output.name, payload_raw, root_raw,
                                  model, terminate_after_pass)
    finally:
        os.close(parent_fd)


def execute(args: argparse.Namespace) -> dict[str, Any]:
    need(FORMAL_EXECUTION_AUTHORIZED and BOUNDARY_CONTRACT_FROZEN_GO,
         "boundary v5 NO-GO; append-only boundary v6 independent GO required")
    pins = (args.expect_self_sha256, args.expect_plan_file_sha256,
        args.expect_plan_object_sha256, args.expect_anticipated_file_sha256,
        args.expect_anticipated_object_sha256, args.expect_replay_file_sha256,
        args.expect_replay_object_sha256, args.expect_run_file_sha256,
        args.expect_run_object_sha256)
    pins = (*pins, args.expect_pre_release_pinset_file_sha256,
            args.expect_pre_release_pinset_object_sha256)
    need(all(valid_sha(value) for value in pins)
         and record(SELF)["sha256"] == args.expect_self_sha256, "all pins")
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
         and plan.get("formal_credit") == 0, "frozen plan")
    expected_service = service_contract(plan)
    invocation_id = os.environ.get("INVOCATION_ID", "")
    exec_start_projection_sha = os.environ.get(
        "CM2_FINALIZER_EXECSTART_PROJECTION_SHA256", "")
    need(re.fullmatch(r"[0-9a-f]{32}", invocation_id) is not None
         and valid_sha(exec_start_projection_sha)
         and os.environ.get("CM2_FINALIZER_UNIT") == expected_service["unit"],
         "current exact finalizer unit/invocation/ExecStart projection")
    actual_service = {**expected_service, "invocation_id": invocation_id,
        "exec_start_projection_sha256": exec_start_projection_sha}

    pre_release_path = inside(args.pre_release_pinset)
    pre_release, pre_release_record = document(
        pre_release_path, "pre_release_pinset_sha256")
    frozen_dynamic = pre_release.get("dynamic_predecessor_members")
    need(pre_release_record["sha256"]
             == args.expect_pre_release_pinset_file_sha256
         and pre_release["pre_release_pinset_sha256"]
             == args.expect_pre_release_pinset_object_sha256
         and pre_release.get("schema")
             == BASE + "finalizer-pre-release-pinset.v1"
         and pre_release.get("status")
             == "FROZEN_FINALIZER_DYNAMIC_PREDECESSOR_PINS_UNDER_EX_LOCK"
         and pre_release.get("plan_file_sha256") == plan_record["sha256"]
         and pre_release.get("plan_object_sha256") == plan["plan_sha256"]
         and type(frozen_dynamic) is list and len(frozen_dynamic) > 0
         and pre_release.get("dynamic_predecessor_members_sha256")
             == digest(frozen_dynamic)
         and [{"path": row.get("path"), "sha256": row.get("sha256")}
              for row in frozen_dynamic] == plan.get("finalizer_input_members")
         and pre_release.get("formal_credit") == 0
         and pre_release.get("manifest_authorized") is False
         and pre_release.get("authority_minted") is False,
         "frozen pre-release dynamic predecessor pinset")

    anticipated = inside(args.anticipated_dir)
    need({path.name for path in anticipated.iterdir()} == ANTICIPATED_FILES,
         "anticipated inventory")
    receipt, receipt_record = document(
        anticipated / "anticipated_terminal_receipt.json",
        "anticipated_terminal_receipt_sha256")
    replay, replay_record = document(anticipated / "anticipated_replay.json",
                                      "anticipated_replay_sha256")
    need(receipt_record["sha256"] == args.expect_anticipated_file_sha256
         and receipt["anticipated_terminal_receipt_sha256"]
             == args.expect_anticipated_object_sha256
         and replay_record["sha256"] == args.expect_replay_file_sha256
         and replay["anticipated_replay_sha256"] == args.expect_replay_object_sha256
         and receipt.get("schema") == ANTICIPATED_SCHEMA
         and receipt.get("status") == ANTICIPATED_STATUS
         and replay.get("schema") == ANTICIPATED_REPLAY_SCHEMA
         and replay.get("status") == ANTICIPATED_STATUS
         and receipt.get("required_finalizer_service_gate") == expected_service
         and replay.get("required_finalizer_service_gate") == expected_service
         and receipt.get("formal_credit") == replay.get("formal_credit") == 0
         and receipt.get("manifest_authorized") is False
         and replay.get("manifest_authorized") is False
         and receipt.get("authority_minted") is False
         and replay.get("authority_minted") is False,
         "anticipated package exact conditional state")
    rebuilt_anticipated = reconstruct_anticipated(
        anticipated, plan, plan_record, expected_service, receipt, replay)
    planned_input_map = {row["path"]: row["sha256"]
        for row in plan["finalizer_input_members"]}
    need(rebuilt_anticipated["receipt_file_sha256"] == receipt_record["sha256"]
         and rebuilt_anticipated["receipt_object_sha256"]
             == receipt["anticipated_terminal_receipt_sha256"]
         and rebuilt_anticipated["replay_object_sha256"]
             == replay["anticipated_replay_sha256"],
         "anticipated four-file reconstruction pins current bytes/objects")
    need(all(planned_input_map.get(str((anticipated / name).relative_to(ROOT)))
                 == record(anticipated / name)["sha256"]
             for name in ANTICIPATED_FILES),
         "anticipated exact four files are finalizer plan-pinned inputs")
    run_dir = inside(args.anticipated_run)
    run_entries = list(os.scandir(run_dir))
    need({entry.name for entry in run_entries} == RUN_FILES
         and len(run_entries) == len(RUN_FILES)
         and all(not entry.is_symlink()
             and stat.S_ISREG(entry.stat(follow_symlinks=False).st_mode)
             and entry.stat(follow_symlinks=False).st_nlink == 1
             for entry in run_entries)
         and read_current(run_dir / "PASS.lock") == RUN_PASS
         and read_current(run_dir / "exit_code.txt") == b"0\n"
         and read_current(run_dir / "signal.json") == b"null\n"
         and read_current(run_dir / "stderr.log") == b""
         and read_current(run_dir / "input_pre.json")
             == read_current(run_dir / "input_post.json"),
         "anticipated transaction current clean success")
    run, run_record = document(run_dir / "run_attestation.json",
                               "run_attestation_sha256")
    need(run_record["sha256"] == args.expect_run_file_sha256
         and run["run_attestation_sha256"] == args.expect_run_object_sha256
         and run.get("schema") == RUN_SCHEMA and run.get("status") == RUN_STATUS
         and run.get("stage") == "anticipated_terminal"
         and run.get("numeric_exit_code") == 0 and run.get("signal") is None
         and run.get("timed_out") is False and run.get("stderr_empty") is True
         and run.get("input_pre_post_sha_full9stat_identical") is True
         and run.get("formal_credit") == 0
         and run.get("manifest_authorized") is False
         and run.get("authority_minted") is False,
         "anticipated transaction attestation")
    member_hashes = {name: record(run_dir / name)["sha256"]
        for name in sorted(RUN_FILES - {"PASS.lock", "run_attestation.json"})}
    output_validation = plain_document(run_dir / "output_validation.json")
    input_pre = plain_document(run_dir / "input_pre.json")
    input_post = plain_document(run_dir / "input_post.json")
    runner_start = plain_document(run_dir / "runner_start.json")
    timing = plain_document(run_dir / "timing.json")
    stdout_raw = read_current(run_dir / "stdout.log")
    need(stdout_raw.endswith(b"\n"), "anticipated canonical stdout newline")
    stdout_value = strict(stdout_raw[:-1])
    anticipated_rel = str(anticipated.relative_to(ROOT))
    output_rows = output_validation.get(anticipated_rel)
    current_anticipated = {str((anticipated / name).relative_to(ROOT)):
        record(anticipated / name)["sha256"] for name in ANTICIPATED_FILES}
    need(type(output_rows) is list and len(output_rows) == 4
         and {row.get("path"): row.get("sha256") for row in output_rows}
             == current_anticipated
         and run.get("output_validation") == output_validation
         and run.get("input_attestations") == input_pre == input_post
         and run.get("exact_inventory") == sorted(RUN_FILES)
         and run.get("member_file_sha256") == member_hashes
         and run.get("stdout_sha256") == hashlib.sha256(stdout_raw).hexdigest()
         and canonical(stdout_value) == stdout_raw[:-1]
         and stdout_value == plan["stage_templates"][
             "anticipated_terminal"]["expected_stdout"]
         and runner_start.get("stage") == "anticipated_terminal"
         and runner_start.get("started_at_utc") == run.get("started_at_utc")
         and runner_start.get("fd_bound_formal_stage") is True
         and timing == {"elapsed_seconds": run.get("elapsed_seconds"),
                        "timed_out": False}
         and run.get("argv_template")
             == plan["stage_templates"]["anticipated_terminal"]["argv_template"]
         and run.get("argv_template_sha256")
             == digest(run.get("argv_template"))
         and run.get("argv_bindings_sha256")
             == digest(run.get("argv_bindings"))
         and run.get("expanded_argv_sha256") == digest(run.get("exact_argv"))
         and run.get("exact_environment", {}).get("PYTHONHASHSEED")
             == plan["stage_templates"]["anticipated_terminal"][
                 "python_hash_seed"],
         "anticipated run current exact11/output/stdout/timing/input closure")
    input_specs = plan.get("finalizer_input_members")
    need(type(input_specs) is list and len(input_specs) > 0,
         "finalizer exact input inventory")
    captures: list[dict[str, Any]] = []
    for spec in input_specs:
        need(type(spec) is dict and set(spec) == {"path", "sha256"},
             "finalizer input spec")
        current = record(inside(spec["path"]))
        need(current["sha256"] == spec["sha256"], "finalizer input SHA")
        captures.append(current)
    output = inside(args.output_dir, absent=True)
    need(output.parent.is_dir() and not output.parent.is_symlink(),
         "official terminal parent exists")
    output_parent_fd = os.open(output.parent, os.O_RDONLY
        | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_CLOEXEC", 0))
    output_parent_stat = fingerprint(os.fstat(output_parent_fd))
    need(output_parent_stat == fingerprint(os.stat(
        output.parent, follow_symlinks=False)),
        "official terminal parent held before final barrier")
    barrier_paths = [SELF, inside(args.plan),
        pre_release_path,
        *(anticipated / name for name in sorted(ANTICIPATED_FILES)),
        *(run_dir / name for name in sorted(RUN_FILES)),
        *(inside(spec["path"]) for spec in input_specs)]
    unique_barrier = sorted(set(barrier_paths))
    barrier_before = [record(path) for path in unique_barrier]
    lock_fd, lock_value = acquire_publication_lock(args, plan, plan_record)
    try:
        # The lock is acquired before the final full-tree revalidation and is
        # held until PASS-last has been fsynced and reopened.
        need(barrier_before == [record(path) for path in unique_barrier]
             and captures == [record(inside(spec["path"]))
                              for spec in input_specs]
             and captures == frozen_dynamic
             and fingerprint(os.fstat(output_parent_fd)) == output_parent_stat
             and fingerprint(os.stat(output.parent, follow_symlinks=False))
                 == output_parent_stat
             and not output.exists() and not output.is_symlink(),
             "locked finalizer full-tree post-state and future absence")
        need(document(pre_release_path, "pre_release_pinset_sha256")[0]
                 == pre_release
             and record(pre_release_path) == pre_release_record
             and pre_release.get("publication_lock_object_sha256")
                 == lock_value["publication_lock_sha256"],
             "pre-release dynamic pins revalidated after finalizer lock acquire")
        payload_members = {inside(spec["path"]) for spec in input_specs}
        payload_members.update({SELF, inside(args.publication_lock_path),
                                pre_release_path})
        payload_raw = manifest_bytes(payload_members)
        future_payload = output / "payload_manifest.sha256"
        root_raw = manifest_bytes({inside(args.plan),
            anticipated / "root_manifest.sha256", SELF,
            inside(args.publication_lock_path)},
            {future_payload: hashlib.sha256(payload_raw).hexdigest()})
        model = {"service": actual_service,
            "plan_file": plan_record["sha256"],
            "plan_object": plan["plan_sha256"],
            "anticipated_file": receipt_record["sha256"],
            "anticipated_object": receipt["anticipated_terminal_receipt_sha256"],
            "replay_file": replay_record["sha256"],
            "replay_object": replay["anticipated_replay_sha256"],
            "run_file": run_record["sha256"],
            "run_object": run["run_attestation_sha256"],
            "publication_lock_object": lock_value["publication_lock_sha256"]}
        return commit_terminal_at(output_parent_fd, output.name, payload_raw,
                                  root_raw, model, terminate_after_pass=True)
    finally:
        os.close(lock_fd)
        os.close(output_parent_fd)


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
    service = {"unit": "cm2-fixture.service",
        "launch_mode": "EXPLICIT_USER_BUS_SYSTEMD_RUN_TRANSIENT_V1",
        "invocation_binding":
            "CAPTURE_FINALIZER_ENV_AND_MATCH_POST_EXIT_SYSTEMD_SHOW",
        "invocation_id": "1" * 32,
        "expected_result": "success", "expected_exec_main_code": 1,
        "expected_exec_main_status": 0, "expected_load_state": "loaded",
        "expected_active_state": "active", "expected_sub_state": "exited",
        "fragment_path":
            "/run/user/1000/systemd/transient/cm2-fixture.service"}
    model = {"service": service, "plan_file": "1" * 64,
        "plan_object": "2" * 64, "anticipated_file": "3" * 64,
        "anticipated_object": "4" * 64, "replay_file": "5" * 64,
        "replay_object": "6" * 64, "run_file": "7" * 64,
        "run_object": "8" * 64, "publication_lock_object": "9" * 64}
    with tempfile.TemporaryDirectory(dir=ROOT / ".cm2-runtime",
            prefix="c27r2-finalizer-v5-selftest-") as raw:
        parent = Path(raw); source = parent / "source"; source.write_bytes(b"x\n")
        output = parent / "terminal"
        payload = manifest_bytes({source})
        future = output / "payload_manifest.sha256"
        root = manifest_bytes({source},
            {future: hashlib.sha256(payload).hexdigest()})
        replay = commit_terminal(output, payload, root, model)
        need({path.name for path in output.iterdir()} == TERMINAL_FILES
             and (output / "PASS.lock").read_bytes() == PASS_BYTES
             and replay.get("authority_mint_is_joint_not_filesystem_only") is True
             and replay.get("authority_minted") is False
             and replay.get("authority_minted_when_joint_gate_observed") is True
             and replay.get("orphan_PASS_authority_eligible") is False,
             "real six-file PASS-last joint-gate fixture")
        swap_parent = parent / "published"
        swap_parent.mkdir()
        held_parent = os.open(swap_parent, os.O_RDONLY
            | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0))
        try:
            held_name = parent / "published-held"
            swap_parent.rename(held_name)
            swap_parent.mkdir()
            commit_terminal_at(held_parent, "terminal", payload, root, model)
            need((held_name / "terminal/PASS.lock").read_bytes() == PASS_BYTES
                 and not (swap_parent / "terminal").exists(),
                 "held terminal parent dirfd defeats parent directory swap")
        finally:
            os.close(held_parent)
        invalid = parent / "invalid-inventory"; invalid.mkdir()
        (invalid / "member").write_bytes(b"x\n")
        (invalid / "extra-directory").mkdir()
        invalid_fd = os.open(invalid, os.O_RDONLY
            | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0))
        rejected = False
        try:
            exact_flat_inventory(invalid_fd, {"member", "extra-directory"})
        except Blocked:
            rejected = True
        finally:
            os.close(invalid_fd)
        need(rejected, "terminal extra directory/type negative rejected")
    return {"status": "PASS_C27R2_RELEASE_REPAIR_FINALIZER_V5_SELF_TEST"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    for name in ("plan", "anticipated-dir", "anticipated-run", "output-dir",
        "pre-release-pinset", "expect-pre-release-pinset-file-sha256",
        "expect-pre-release-pinset-object-sha256",
        "expect-self-sha256", "expect-plan-file-sha256",
        "expect-plan-object-sha256", "expect-anticipated-file-sha256",
        "expect-anticipated-object-sha256", "expect-replay-file-sha256",
        "expect-replay-object-sha256", "expect-run-file-sha256",
        "expect-run-object-sha256", "publication-lock-path",
        "expect-publication-lock-file-sha256",
        "expect-publication-lock-object-sha256",
        "expect-publication-lock-stat9-json",
        "publication-lock-timeout-seconds"):
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
        return 0  # Must be the immediate post-PASS normal service return.
    except (Blocked, OSError, ValueError, KeyError, TypeError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
