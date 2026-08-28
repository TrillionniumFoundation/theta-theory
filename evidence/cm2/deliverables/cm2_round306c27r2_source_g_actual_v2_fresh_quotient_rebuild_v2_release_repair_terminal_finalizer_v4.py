#!/usr/bin/env python3
"""Official C27R2 v4 terminal finalizer with PASS as the last FS mutation.

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
PLAN_SCHEMA = BASE + "chain-plan.v4"
PLAN_STATUS = (
    "FROZEN_C27R2_RELEASE_REPAIR_V4_EXACT70_PLUS_LOCK8_PLAN__EXECUTION_DISABLED_"
    "PENDING_INDEPENDENT_FULL_CHAIN_AUDIT"
)
ANTICIPATED_SCHEMA = BASE + "anticipated-terminal-receipt.v4"
ANTICIPATED_STATUS = (
    "PASS_C27R2_RELEASE_REPAIR_V4_INDEPENDENT_ANTICIPATED_BYTE_REPLAY__"
    "ZERO_CREDIT_PENDING_OFFICIAL_FINALIZER_AND_SERVICE_CLEAN_SUCCESS"
)
ANTICIPATED_REPLAY_SCHEMA = BASE + "anticipated-terminal-replay.v4"
RUN_SCHEMA = BASE + "release-repair-process-run-attestation.v4"
RUN_STATUS = (
    "PASS_C27R2_RELEASE_REPAIR_PROCESS_EXIT0_NULL_SIGNAL_EMPTY_STDERR_"
    "EXACT_SPEC_PINSET_ARGV_ENV_PRE_POST_FULL9STAT_AND_OUTPUT_INVENTORY__"
    "ZERO_CREDIT"
)
RUN_PASS = b"PASS_C27R2_RELEASE_REPAIR_V4_PROCESS_TRANSACTION__ZERO_CREDIT\n"
TERMINAL_SCHEMA = BASE + "terminal-receipt.v4"
TERMINAL_REPLAY_SCHEMA = BASE + "terminal-replay.v4"
CHAIN_SCHEMA = BASE + "release-chain-status.v4"
TERMINAL_STATUS = (
    "PASS_C27R2_RELEASE_REPAIR_V4_FILESYSTEM_TERMINAL_PASS_LAST__JOINT_"
    "AUTHORITY_REQUIRES_CURRENT_FINALIZER_UNIT_CLEAN_SUCCESS"
)
PASS_BYTES = (
    b"PASS_C27R2_RELEASE_REPAIR_V4_JOINT_SERVICE_GATED_TERMINAL__"
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
BOUNDARY_CONTRACT_FROZEN_GO = False  # boundary v4 NO-GO; append-only v5 pending.
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
        and value["expected_active_state"] == "inactive"
        and value["expected_sub_state"] == "dead"
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


def publish_pass_and_exit(path: Path, raw: bytes) -> None:
    """Publish PASS and terminate after the final successful fsync syscall."""
    parent = os.open(path.parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
                     | getattr(os, "O_NOFOLLOW", 0)
                     | getattr(os, "O_CLOEXEC", 0))
    descriptor = os.open(path.name, os.O_WRONLY | os.O_CREAT | os.O_EXCL
        | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0),
        0o400, dir_fd=parent)
    _write_all(descriptor, raw)
    os.fsync(descriptor)
    os.fsync(parent)
    os._exit(0)


def commit_terminal(output: Path, payload_raw: bytes, root_raw: bytes,
                    model: dict[str, Any],
                    terminate_after_pass: bool = False) -> dict[str, Any]:
    """Write five pre-PASS members, reopen them, then PASS as last mutation."""
    need(not output.exists() and not output.is_symlink(), "fresh terminal")
    output.mkdir(parents=True, mode=0o700)
    fsync_directory(output)
    fsync_directory(output.parent)
    payload_path = output / "payload_manifest.sha256"
    root_path = output / "root_manifest.sha256"
    write_once(payload_path, payload_raw)
    write_once(root_path, root_raw)
    receipt, replay, chain = terminal_models(model,
        record(payload_path)["sha256"], record(root_path)["sha256"])
    receipt_path = output / "terminal_receipt.json"
    replay_path = output / "terminal_replay.json"
    chain_path = output / "chain_status.json"
    write_once(receipt_path, canonical(receipt) + b"\n")
    write_once(replay_path, canonical(replay) + b"\n")
    write_once(chain_path, canonical(chain) + b"\n")
    need(document(receipt_path, "terminal_receipt_sha256")[0] == receipt
         and document(replay_path, "terminal_replay_sha256")[0] == replay
         and document(chain_path, "chain_status_sha256")[0] == chain
         and {path.name for path in output.iterdir()} == TERMINAL_FILES - {"PASS.lock"},
         "all pre-PASS terminal members reopened")
    if terminate_after_pass:
        publish_pass_and_exit(output / "PASS.lock", PASS_BYTES)
    else:
        write_once(output / "PASS.lock", PASS_BYTES)  # Self-test only.
    return replay  # Caller must immediately return normally; no more FS access.


def execute(args: argparse.Namespace) -> dict[str, Any]:
    need(FORMAL_EXECUTION_AUTHORIZED and BOUNDARY_CONTRACT_FROZEN_GO,
         "boundary v4 NO-GO; append-only boundary v5 independent GO required")
    pins = (args.expect_self_sha256, args.expect_plan_file_sha256,
        args.expect_plan_object_sha256, args.expect_anticipated_file_sha256,
        args.expect_anticipated_object_sha256, args.expect_replay_file_sha256,
        args.expect_replay_object_sha256, args.expect_run_file_sha256,
        args.expect_run_object_sha256)
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
    need(re.fullmatch(r"[0-9a-f]{32}", invocation_id) is not None
         and os.environ.get("CM2_FINALIZER_UNIT") == expected_service["unit"],
         "current exact finalizer unit and actual systemd invocation")
    actual_service = {**expected_service, "invocation_id": invocation_id}

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
    run_dir = inside(args.anticipated_run)
    need({path.name for path in run_dir.iterdir()} == RUN_FILES
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
    barrier_paths = [SELF, inside(args.plan),
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
             and not output.exists() and not output.is_symlink(),
             "locked finalizer full-tree post-state and future absence")
        payload_members = {inside(spec["path"]) for spec in input_specs}
        payload_members.update({SELF, inside(args.publication_lock_path)})
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
        return commit_terminal(output, payload_raw, root_raw, model,
                               terminate_after_pass=True)
    finally:
        os.close(lock_fd)


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
        "expected_active_state": "inactive", "expected_sub_state": "dead",
        "fragment_path":
            "/run/user/1000/systemd/transient/cm2-fixture.service"}
    model = {"service": service, "plan_file": "1" * 64,
        "plan_object": "2" * 64, "anticipated_file": "3" * 64,
        "anticipated_object": "4" * 64, "replay_file": "5" * 64,
        "replay_object": "6" * 64, "run_file": "7" * 64,
        "run_object": "8" * 64, "publication_lock_object": "9" * 64}
    with tempfile.TemporaryDirectory(dir=ROOT / ".cm2-runtime",
            prefix="c27r2-finalizer-v4-selftest-") as raw:
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
    return {"status": "PASS_C27R2_RELEASE_REPAIR_FINALIZER_V4_SELF_TEST"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    for name in ("plan", "anticipated-dir", "anticipated-run", "output-dir",
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
