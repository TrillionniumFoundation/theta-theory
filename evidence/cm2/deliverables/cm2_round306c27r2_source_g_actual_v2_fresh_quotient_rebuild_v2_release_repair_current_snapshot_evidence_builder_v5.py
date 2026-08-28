#!/usr/bin/env python3
"""Freeze the complete pre-fixture C27R2 release-repair authority snapshot.

This is Stage A of the append-only v5 repair.  It consumes one externally
frozen plan (file and object SHA pinned on the command line), reopens every
authority member with O_NOFOLLOW, and persists path, SHA-256, size and the
full nine-field stat fingerprint.  It grants no credit and cannot authorize a
manifest.  Stage B must compare every persisted record after the exact 70
validator wrappers and separately classified eight publication-lock checks.
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
import subprocess
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
SNAPSHOT_STATUS = (
    "PASS_C27R2_RELEASE_REPAIR_V5_CORE_FRESH_COLD_BOUNDARY_TRUST_"
    "EXACT_TERMINAL_INVENTORIES_AND_FULL9STAT_SNAPSHOT_FROZEN__ZERO_"
    "CREDIT_NOT_MANIFEST_AUTHORIZED"
)
CORE_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "gated-dual-seed-transaction-receipt.v4"
)
CORE_STATUS = (
    "PASS_GATE_SEED1_FOUR_FILE_CANDIDATE_SEED2_NO_IMPORT_REPLAY_AND_21_"
    "ATTACKS__ZERO_CREDIT_PENDING_OUTER_SEAL_AND_TERMINAL_REPLAY"
)
COLD_SCHEMA = "cm2.round306c27r2.source-g-authority-v2.release-cold-replay-receipt.v4"
COLD_STATUS = (
    "PASS_FRESH_NO_IMPORT_SEED2_COLD_BYTE_REPLAY_WITH_FIXED_CONTROL_BUS_AND_"
    "ALL_CORE_INPUT_PRE_POST_SHA_STAT__ZERO_CREDIT"
)
COLD_RUN_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "process-run-attestation.v4"
)
COLD_RUN_STATUS = (
    "PASS_PROCESS_TRANSACTION_EXIT0_NULL_SIGNAL_EMPTY_STDERR_PRE_POST_"
    "AND_OUTPUTS__ZERO_CREDIT"
)
BOUNDARY_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "release-boundary-validator.v5"
)
BOUNDARY_STATUS = (
    "PASS_C27R2_RELEASE_REPAIR_BOUNDARY_V5_FORMAL_EMPTY_OVERRIDE_EXACT_"
    "SPEC_ATTESTATION_INPUT_SET_FIXED_USER_BUS_SERVICE_QUERY_CURRENT_PROCESS_"
    "INVENTORY_AND_AUTHORITY_CLOSURE__ZERO_CREDIT"
)
DECISION_SCHEMA = BASE + "trust-decision.v4"
DECISION_STATUS = (
    "PASS_ACTUAL_V2_PREDECESSOR_ONLY_OLD_C27R2_AUDIT_HOLD_AND_REAL_"
    "RELEASE_REPAIR_REQUIRED__ZERO_CREDIT"
)
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
COLD_HELPER_PATH = (
    "deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_quotient_"
    "rebuild_v2_release_cold_replay_runner_v4.py"
)
COLD_HELPER_SHA = "3d44ebbc37449192f975e3687284c6e74285f7d7f564e40ef12e37232f0ec838"
COLD_INPUT_COUNT = 165
COLD_INPUT_PATHS_SHA = "fe01c7fd4eabdfd992f6528938e8d624578dc5618c6440c4aae082c828cbee2c"
COLD_ROLE_MAP_SHA = "f4673ac89907f9fae4b90df5ffe77036235329b9a8d6317751fd37ca8d9d76ed"
COLD_CAPTURE_COUNT = 167
COLD_ATTESTED_SEQUENCE_SHA = "623cfb0a624152b2523948d86542d267b6e25ebdb185d1080b13de3468372bbf"
COLD_ROOT = ".cm2-runtime/audit/c27r2-release-cold-v4-r1-20260808T191556Z"
COLD_CONTROL_DIR = COLD_ROOT + "-control"
COLD_RUN_DIR = COLD_ROOT + "-run"
COLD_OUTPUT_DIR = COLD_ROOT + "-output"
COLD_CONTROL_FILES = ["PASS.lock", "cold_command_spec.json",
    "cold_replay_receipt.json", "pinset.json", "runner.exit_code.txt",
    "runner.stderr.log", "runner.stdout.log"]
COLD_RUN_FILES = ["PASS.lock", "exit_code.txt", "input_post.json",
    "input_pre.json", "output_validation.json", "run_attestation.json",
    "runner_start.json", "signal.json", "stderr.log", "stdout.log",
    "timing.json"]
COLD_OUTPUT_FILES = ["verification.json"]
COLD_PINS = {
    "receipt_file_sha256": "2b43a4be6285f04ad4f6a94dd005079477d1c4819135b9b44af6d791ffe94502",
    "receipt_object_sha256": "66df67907f836947b9633644a697682aebdf1b313b7691ff241f4687b69c6ac6",
    "command_spec_file_sha256": "672b545199ec326fdb14d34f741a8de99fc961facff591023499701a5b6d6ab1",
    "command_spec_object_sha256": "e8e5e2ad5de71720f5ca705d1eb56728285b61f80e4b4fdbb153a63a4b8d89fd",
    "pinset_file_sha256": "a6c23811f8f9fb3dd8048cb3b409750e0dbd1c78b44ca8c9e8481203a70819e2",
    "pinset_object_sha256": "80a106dbb721243b6878047e9d2214b52b0f5a3211d2833c5390a69acad1c644",
    "run_attestation_file_sha256": "775b89405ce88db5db710863b9e12c3b4ff0514bc4a27c6d1c171128bfef6703",
    "run_attestation_object_sha256": "a89ed2f2f8ee46224af1e8dc95577a77aa7d0c12e69f695f464774d55c759746",
    "verification_file_sha256": "de1ff5b4fda6f4acb999c6784b2e8a567e5d34ae8db439b6e8979f89e9266b4e",
    "verification_object_sha256": "86ed61381a9c614cf3662926041a89445a968534ccc20897a3f56842836e0d25",
}
SYSTEMCTL = Path("/usr/bin/systemctl")
SYSTEMCTL_SHA = "7ba82b5ba146759c710e1b80fadaa3fdbc0f9b85c8fb2c8c3196b7b1a0037ef8"
CONTROL_BUS_ENV = {"PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
    "XDG_RUNTIME_DIR": "/run/user/1000",
    "DBUS_SESSION_BUS_ADDRESS": "unix:path=/run/user/1000/bus"}
COLD_SERVICE = {
    "unit": "cm2-c27r2-release-cold-v4-r1-20260808T191556Z.service",
    "load_state": "loaded", "active_state": "active", "sub_state": "exited",
    "result": "success", "exec_main_code": "1", "exec_main_status": "0",
    "invocation_id": "69c171922ce64dea90e79fa462750c26",
    "fragment_path": ("/run/user/1000/systemd/transient/"
        "cm2-c27r2-release-cold-v4-r1-20260808T191556Z.service"),
    "exec_start_projection_sha256":
        "d2d69ab7f245da6b1546dce9f4508c44394800c2b26a1af089c99ea873dab80f",
}
BOUNDARY_CONTRACT_FROZEN_GO = False  # boundary v5 NO-GO; append-only v6 pending.
FORMAL_EXECUTION_AUTHORIZED = False  # Independent full-chain GO has not been minted.
DOC_CONTRACTS = {
    "core_receipt": ("transaction_receipt_sha256", CORE_SCHEMA, CORE_STATUS),
    "fresh_cold_receipt": ("cold_replay_receipt_sha256", COLD_SCHEMA, COLD_STATUS),
    "boundary_preflight": ("validation_sha256", BOUNDARY_SCHEMA, BOUNDARY_STATUS),
    "trust_decision": ("trust_decision_sha256", DECISION_SCHEMA, DECISION_STATUS),
}
EXPECTED = {
    "frozen_C15_components": 57_876,
    "post_C27R2_components": 43_684,
    "proof_derived_component_edges": 14_860,
    "successful_DSU_merges": 14_192,
    "cycle_edges": 668,
    "frozen_C15_members": 502_204,
    "total_unordered_member_pairs": 126_104_177_706,
    "within_post_component_member_pairs": 542_179_508,
    "cross_post_component_member_pairs": 125_561_998_198,
}


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
            need(type(key) is str and key not in out, "duplicate JSON key")
            out[key] = value
        return out
    return json.loads(raw, object_pairs_hook=pairs,
                      parse_constant=lambda value: (_ for _ in ()).throw(
                          Blocked("non-finite JSON:" + value)))


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
        raise Blocked("path outside workspace") from error
    need(relative.parts and all(part not in {"", ".", ".."}
                                for part in relative.parts), "canonical path")
    cursor = ROOT
    for part in relative.parts:
        cursor /= part
        if not cursor.exists():
            need(absent, "missing path:" + str(cursor))
            break
        need(not cursor.is_symlink(), "symlink path:" + str(cursor))
    return path


def capture(path: Path, retain_bytes: bool = True) -> tuple[bytes, dict[str, Any]]:
    need(path.is_file() and not path.is_symlink(), "regular file")
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular single-link file")
        state = hashlib.sha256()
        chunks: list[bytes] = []
        while block := os.read(descriptor, 4 << 20):
            state.update(block)
            if retain_bytes: chunks.append(block)
        after = os.stat(path, follow_symlinks=False)
        need(fingerprint(after) == fingerprint(before)
             and fingerprint(os.fstat(descriptor)) == fingerprint(before),
             "stable full9stat")
        return b"".join(chunks), {"path": str(path.relative_to(ROOT)),
                "sha256": state.hexdigest(), "size": before.st_size,
                "stat_fingerprint": fingerprint(before),
                "O_NOFOLLOW": True, "single_link": True}
    finally:
        os.close(descriptor)


def record(path: Path) -> dict[str, Any]:
    return capture(path, False)[1]


def document(path: Path, closure: str) -> tuple[dict[str, Any], dict[str, Any]]:
    raw, item = capture(path)
    need(raw.endswith(b"\n"), "JSON newline")
    value = strict(raw[:-1])
    need(type(value) is dict and canonical(value) == raw[:-1], "canonical JSON")
    body = dict(value)
    claim = body.pop(closure, None)
    need(valid_sha(claim) and claim == digest(body), "object closure:" + closure)
    return value, item


def stable_external_sha(path: Path) -> str:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
                         | getattr(os, "O_CLOEXEC", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "external executable regular single-link")
        state = hashlib.sha256()
        while block := os.read(descriptor, 1 << 20):
            state.update(block)
        need(fingerprint(os.fstat(descriptor)) == fingerprint(before)
             and fingerprint(os.stat(path, follow_symlinks=False))
                 == fingerprint(before),
             "external executable stable full9stat")
        return state.hexdigest()
    finally:
        os.close(descriptor)


def cold_service_snapshot() -> dict[str, str]:
    need(stable_external_sha(SYSTEMCTL) == SYSTEMCTL_SHA,
         "frozen systemctl binary")
    keys = ("Id", "LoadState", "ActiveState", "SubState", "Result",
            "ExecMainCode", "ExecMainStatus", "InvocationID", "ExecStart",
            "FragmentPath")
    result = subprocess.run([str(SYSTEMCTL), "--user", "show",
        COLD_SERVICE["unit"], "--property=" + ",".join(keys), "--no-pager"],
        cwd=ROOT, env=CONTROL_BUS_ENV, stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30,
        check=False)
    need(result.returncode == 0 and result.stderr == b""
         and len(result.stdout) <= 16_384, "fixed-user-bus cold service query")
    rows: dict[str, str] = {}
    for raw in result.stdout.splitlines():
        need(b"=" in raw, "service property row")
        key_raw, value_raw = raw.split(b"=", 1)
        key = key_raw.decode("ascii")
        value = value_raw.decode("ascii")
        need(key in keys and key not in rows and "\x00" not in value,
             "exact unique service property")
        rows[key] = value
    need(set(rows) == set(keys), "exact service property set")
    match = re.fullmatch(
        r"\{ path=([^ ;]+) ; argv\[\]=(.*?) ; ignore_errors=.*",
        rows["ExecStart"])
    need(match is not None, "canonical cold ExecStart projection")
    normalized = {"unit": rows["Id"], "load_state": rows["LoadState"],
        "active_state": rows["ActiveState"], "sub_state": rows["SubState"],
        "result": rows["Result"], "exec_main_code": rows["ExecMainCode"],
        "exec_main_status": rows["ExecMainStatus"],
        "invocation_id": rows["InvocationID"],
        "fragment_path": rows["FragmentPath"],
        "exec_start_projection_sha256": digest({"path": match.group(1),
                                                  "argv": match.group(2)})}
    return normalized


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


def load_plan(path: Path, file_pin: str, object_pin: str) -> tuple[dict[str, Any], dict[str, Any]]:
    value, item = document(path, "plan_sha256")
    need(item["sha256"] == file_pin and value["plan_sha256"] == object_pin,
         "plan file/object pins")
    need(value.get("schema") == PLAN_SCHEMA and value.get("status") == PLAN_STATUS
         and value.get("mode") == "formal"
         and value.get("validator_negative_case_count") == 70
         and value.get("publication_lock_preflight_case_count") == 8
         and value.get("total_integrity_check_count") == 78
         and "case_count" not in value
         and value.get("exact_math") == EXPECTED
         and value.get("execution_enabled") is False
         and value.get("formal_credit") == 0
         and value.get("manifest_authorized") is False
         and value.get("authority_minted") is False
         and value.get("C27R2") == "AUDIT_HOLD_UNAUTHORIZED"
         and value.get("CM2") == "NO-GO_FOR_CLAIM", "frozen plan governance")
    return value, item


def verify_plan_contract(plan: dict[str, Any], plan_path: Path) -> list[dict[str, Any]]:
    sources = plan.get("sources")
    need(type(sources) is dict
         and sources.get("boundary_validator") == {
             "path": BOUNDARY_VALIDATOR_PATH, "sha256": BOUNDARY_VALIDATOR_SHA}
         and sources.get("integrity70_plus_lock8_runner") == {
             "path": INTEGRITY_RUNNER_PATH, "sha256": INTEGRITY_RUNNER_SHA}
         and sources.get("cold_runner") == {
             "path": COLD_HELPER_PATH, "sha256": COLD_HELPER_SHA}
         and plan.get("ordered_validator70_object_sha256")
             == ORDERED_VALIDATOR70_OBJECT_SHA
         and plan.get("ordered_lock8_object_sha256") == ORDERED_LOCK8_OBJECT_SHA
         and record(inside(BOUNDARY_VALIDATOR_PATH))["sha256"]
             == BOUNDARY_VALIDATOR_SHA
         and record(inside(INTEGRITY_RUNNER_PATH))["sha256"]
             == INTEGRITY_RUNNER_SHA
         and record(inside(COLD_HELPER_PATH))["sha256"] == COLD_HELPER_SHA,
         "frozen boundary validator/integrity70+lock8 runner/cold-v4 objects")
    for role, spec in sources.items():
        current_source = record(inside(spec["path"])) if type(spec) is dict \
            and "path" in spec else {}
        need(type(role) is str and type(spec) is dict
             and set(spec) == {"path", "sha256"}
             and valid_sha(spec["sha256"])
             and current_source.get("path") == spec["path"]
             and current_source.get("sha256") == spec["sha256"],
             "every source role current pin:" + str(role))
    documents = plan.get("documents")
    need(type(documents) is dict and set(documents) == set(DOC_CONTRACTS),
         "exact document roles")
    for role, (closure, schema, status) in DOC_CONTRACTS.items():
        spec = documents[role]
        need(type(spec) is dict and set(spec) == {
            "path", "file_sha256", "object_sha256"}, "document spec:" + role)
        value, item = document(inside(spec["path"]), closure)
        need(item["path"] == spec["path"]
             and item["sha256"] == spec["file_sha256"]
             and value[closure] == spec["object_sha256"]
             and value.get("schema") == schema and value.get("status") == status
             and value.get("formal_credit") == 0
             and value.get("manifest_authorized") is False,
             "document contract:" + role)
    decision = document(inside(documents["trust_decision"]["path"]),
                        "trust_decision_sha256")[0]
    need(decision.get("actual_v2_terminal_role") == "PREDECESSOR_EVIDENCE_ONLY"
         and decision.get("actual_v2_authority_eligible") is False
         and decision.get("old_C27R2_authority_eligible") is False,
         "trust decision governance")
    cold = document(inside(documents["fresh_cold_receipt"]["path"]),
                    "cold_replay_receipt_sha256")[0]
    cold_contract = plan.get("fresh_cold_contract")
    need(type(cold_contract) is dict and set(cold_contract) == {
        "helper_source_path", "helper_source_sha256", "command_spec_path",
        "pinset_path", "run_attestation_path", "declared_input_count",
        "declared_input_paths_sha256", "declared_input_role_map_sha256",
        "process_capture_count", "attested_sequence_sha256",
        "control_directory", "run_directory", "output_directory",
        "receipt_path", "verification_path", "pinned_objects", "service"}
        and cold_contract["helper_source_path"] == COLD_HELPER_PATH
        and cold_contract["helper_source_sha256"] == COLD_HELPER_SHA
        and cold_contract["command_spec_path"]
            == COLD_CONTROL_DIR + "/cold_command_spec.json"
        and cold_contract["pinset_path"] == COLD_CONTROL_DIR + "/pinset.json"
        and cold_contract["run_attestation_path"]
            == COLD_RUN_DIR + "/run_attestation.json"
        and cold_contract["receipt_path"]
            == COLD_CONTROL_DIR + "/cold_replay_receipt.json"
        and cold_contract["verification_path"]
            == COLD_OUTPUT_DIR + "/verification.json"
        and cold_contract["control_directory"] == COLD_CONTROL_DIR
        and cold_contract["run_directory"] == COLD_RUN_DIR
        and cold_contract["output_directory"] == COLD_OUTPUT_DIR
        and cold_contract["declared_input_count"] == COLD_INPUT_COUNT
        and cold_contract["declared_input_paths_sha256"] == COLD_INPUT_PATHS_SHA
        and cold_contract["declared_input_role_map_sha256"] == COLD_ROLE_MAP_SHA
        and cold_contract["process_capture_count"] == COLD_CAPTURE_COUNT
        and cold_contract["attested_sequence_sha256"]
            == COLD_ATTESTED_SEQUENCE_SHA
        and cold_contract["pinned_objects"] == COLD_PINS
        and cold_contract["service"] == COLD_SERVICE
        and cold_service_snapshot() == COLD_SERVICE
        and documents["fresh_cold_receipt"]["path"]
            == cold_contract["receipt_path"]
        and documents["fresh_cold_receipt"]["file_sha256"]
            == COLD_PINS["receipt_file_sha256"]
        and documents["fresh_cold_receipt"]["object_sha256"]
            == COLD_PINS["receipt_object_sha256"],
        "fresh cold v4 fixed source/count/path/role/object/service contract")
    spec = document(inside(cold_contract["command_spec_path"]),
                    "command_spec_sha256")[0]
    pinset = document(inside(cold_contract["pinset_path"]),
                      "pinset_sha256")[0]
    run = document(inside(cold_contract["run_attestation_path"]),
                   "run_attestation_sha256")[0]
    verification = document(inside(cold_contract["verification_path"]),
                            "verification_sha256")[0]
    need(record(inside(cold_contract["command_spec_path"]))["sha256"]
             == COLD_PINS["command_spec_file_sha256"]
         and spec["command_spec_sha256"]
             == COLD_PINS["command_spec_object_sha256"]
         and record(inside(cold_contract["pinset_path"]))["sha256"]
             == COLD_PINS["pinset_file_sha256"]
         and pinset["pinset_sha256"] == COLD_PINS["pinset_object_sha256"]
         and record(inside(cold_contract["run_attestation_path"]))["sha256"]
             == COLD_PINS["run_attestation_file_sha256"]
         and run["run_attestation_sha256"]
             == COLD_PINS["run_attestation_object_sha256"]
         and record(inside(cold_contract["verification_path"]))["sha256"]
             == COLD_PINS["verification_file_sha256"]
         and verification["verification_sha256"]
             == COLD_PINS["verification_object_sha256"],
         "fresh cold v4 exact file/object pins")
    inputs = spec.get("input_paths")
    need(type(inputs) is list and len(inputs) == COLD_INPUT_COUNT
         and inputs == sorted(set(inputs))
         and hashlib.sha256(b"".join(
             path.encode("ascii") + b"\n" for path in inputs)).hexdigest()
             == COLD_INPUT_PATHS_SHA
         and spec.get("exact_declared_input_count") == COLD_INPUT_COUNT
         and spec.get("exact_declared_input_paths_sha256") == COLD_INPUT_PATHS_SHA
         and spec.get("declared_input_role_map_sha256") == COLD_ROLE_MAP_SHA
         and pinset.get("exact_declared_input_count") == COLD_INPUT_COUNT
         and pinset.get("exact_declared_input_paths_sha256") == COLD_INPUT_PATHS_SHA
         and pinset.get("declared_input_role_map_sha256") == COLD_ROLE_MAP_SHA
         and pinset.get("source_pins", {}).get("cold_replay_helper")
             == COLD_HELPER_SHA,
         "fresh cold v4 dynamic spec/pinset exact semantic closure")
    attestations = run.get("input_attestations")
    labels = ["command-spec", "pinset"] + [
        f"declared-input-{ordinal:03d}" for ordinal in range(COLD_INPUT_COUNT)]
    need(type(attestations) is dict and set(attestations) == set(labels),
         "fresh cold exact 167 attestation labels")
    observed_attested = [attestations[label].get("path") for label in labels]
    expected_attested = [cold_contract["command_spec_path"],
        cold_contract["pinset_path"], *inputs]
    need(all(record(inside(path))["path"] == path for path in expected_attested),
         "fresh cold contract paths canonical/current")
    for label, path in zip(labels, expected_attested, strict=True):
        row = attestations[label]
        current = record(inside(path))
        need(type(row) is dict and row.get("path") == path
             and row.get("sha256") == current["sha256"]
             and row.get("size") == current["size"]
             and row.get("stat_fingerprint") == current["stat_fingerprint"]
             and row.get("O_NOFOLLOW") is True
             and row.get("single_open_file_description_hash_child_fstat_and_path_identity")
                 is True,
             "fresh cold attested current byte/full9stat:" + label)
    need(observed_attested == expected_attested
         and len(observed_attested) == COLD_CAPTURE_COUNT
         and len(set(observed_attested)) == COLD_CAPTURE_COUNT
         and run.get("schema") == COLD_RUN_SCHEMA
         and run.get("status") == COLD_RUN_STATUS
         and run.get("input_pre_post_sha_stat_identical") is True
         and cold.get("exact_declared_input_count") == COLD_INPUT_COUNT
         and cold.get("exact_process_capture_count") == COLD_CAPTURE_COUNT
         and cold.get("exact_declared_input_paths_sha256") == COLD_INPUT_PATHS_SHA
         and cold.get("exact_attested_path_sequence_sha256")
             == COLD_ATTESTED_SEQUENCE_SHA
             == hashlib.sha256(b"".join(
                 path.encode("ascii") + b"\n"
                 for path in expected_attested)).hexdigest()
         and cold.get("all_core_inputs_pre_post_sha_stat_identical") is True,
         "fresh cold exact spec/pinset/165 inputs/167 capture closure")

    directories = plan.get("exact_directories")
    need(type(directories) is list and len(directories) > 0,
         "exact terminal directories")
    roles: list[str] = []
    for spec in directories:
        need(type(spec) is dict and set(spec) == {"role", "path", "members"},
             "directory spec shape")
        members = spec["members"]
        need(type(spec["role"]) is str and spec["role"] not in roles
             and type(members) is list and members == sorted(set(members)),
             "directory role/inventory")
        roles.append(spec["role"])
        directory = inside(spec["path"])
        need(str(directory.relative_to(ROOT)) == spec["path"]
             and directory.is_dir() and not directory.is_symlink()
             and sorted(entry.name for entry in directory.iterdir()) == members,
             "exact terminal inventory:" + spec["role"])
    directory_map = {spec["role"]: {"path": spec["path"],
        "members": spec["members"]} for spec in directories}
    need(directory_map.get("fresh_cold_control") == {
             "path": COLD_CONTROL_DIR, "members": COLD_CONTROL_FILES}
         and directory_map.get("fresh_cold_run") == {
             "path": COLD_RUN_DIR, "members": COLD_RUN_FILES}
         and directory_map.get("fresh_cold_output") == {
             "path": COLD_OUTPUT_DIR, "members": COLD_OUTPUT_FILES},
         "fresh cold v4 exact control7/run11/output1 inventories")

    authority = plan.get("authority_members")
    need(type(authority) is list and len(authority) > 0, "authority member list")
    need([row.get("role") for row in authority]
         == sorted(set(row.get("role") for row in authority)),
         "sorted unique authority roles")
    authority_paths = {row.get("path") for row in authority}
    required_paths = {str(SELF.relative_to(ROOT)), str(plan_path.relative_to(ROOT))}
    publication_lock = plan.get("publication_lock")
    need(type(publication_lock) is dict
         and set(publication_lock) == {"path", "schema", "status", "protocol"}
         and publication_lock["schema"] == BASE + "publication-lock.v1"
         and publication_lock["status"]
             == "FROZEN_ONE_SHOT_PUBLICATION_LOCK__NO_AUTHORITY"
         and publication_lock["protocol"]
             == "FLOCK_EXCLUSIVE_WHOLE_PUBLICATION_WINDOW_V1",
         "frozen publication-lock plan contract")
    required_paths.add(publication_lock["path"])
    required_paths.update(spec["path"] for spec in sources.values())
    required_paths.update(spec["path"] for spec in documents.values())
    required_paths.update({cold_contract["command_spec_path"],
                           cold_contract["pinset_path"],
                           cold_contract["run_attestation_path"],
                           *inputs})
    for spec in directories:
        base = Path(spec["path"])
        required_paths.update(str(base / member) for member in spec["members"])
    need(required_paths <= authority_paths,
         "authority snapshot covers plan/source/document/cold/exact-directory union")
    records: list[dict[str, Any]] = []
    for ordinal, spec in enumerate(authority):
        need(type(spec) is dict and set(spec) == {"role", "path", "sha256"}
             and valid_sha(spec["sha256"]), "authority member spec")
        current = record(inside(spec["path"]))
        need(current["path"] == spec["path"]
             and current["sha256"] == spec["sha256"],
             "authority member canonical path/SHA")
        body = {"schema": BASE + "snapshot-member-row.v5", "ordinal": ordinal,
                "role": spec["role"], **current, "formal_credit": 0}
        records.append({**body, "row_sha256": digest(body)})
    return records


def execute(args: argparse.Namespace) -> dict[str, Any]:
    need(FORMAL_EXECUTION_AUTHORIZED and BOUNDARY_CONTRACT_FROZEN_GO,
         "boundary v5 NO-GO; append-only boundary v6 independent GO required")
    need(valid_sha(args.expect_self_sha256)
         and record(SELF)["sha256"] == args.expect_self_sha256,
         "snapshot source pin")
    need(valid_sha(args.expect_plan_file_sha256)
         and valid_sha(args.expect_plan_object_sha256), "plan SHA pins")
    plan, plan_record = load_plan(inside(args.plan),
        args.expect_plan_file_sha256, args.expect_plan_object_sha256)
    rows = verify_plan_contract(plan, inside(args.plan))
    output = inside(args.output_dir, absent=True)
    need(not output.exists() and not output.is_symlink(), "fresh output")
    output.mkdir(parents=True, mode=0o700)
    fsync_directory(output)
    fsync_directory(output.parent)
    ledger = output / "snapshot_records.jsonl"
    write_once(ledger, b"".join(canonical(row) + b"\n" for row in rows))
    sequence = hashlib.sha256(b"".join(
        row["row_sha256"].encode("ascii") + b"\n" for row in rows)).hexdigest()
    body = {
        "schema": SNAPSHOT_SCHEMA, "status": SNAPSHOT_STATUS,
        "completed_at_utc": datetime.now(timezone.utc).isoformat(
            timespec="microseconds").replace("+00:00", "Z"),
        "plan_file_sha256": plan_record["sha256"],
        "plan_object_sha256": plan["plan_sha256"],
        "snapshot_records_file_sha256": record(ledger)["sha256"],
        "snapshot_record_count": len(rows),
        "snapshot_row_sequence_sha256": sequence,
        "record_contract": ["path", "sha256", "size", "stat_fingerprint",
                            "O_NOFOLLOW", "single_link"],
        "all_exact_terminal_inventories_reopened": True,
        "all_decision_and_authority_file_object_hashes_reopened": True,
        "fresh_cold": True, "fixture_credit_claimed": False,
        "exact_math": EXPECTED,
        "formal_credit": 0, "manifest_authorized": False,
        "authority_minted": False, "C27R2": "AUDIT_HOLD_UNAUTHORIZED",
        "C28_C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM",
    }
    receipt = {**body, "snapshot_evidence_sha256": digest(body)}
    write_once(output / "snapshot_evidence.json", canonical(receipt) + b"\n")
    need(sorted(path.name for path in output.iterdir()) == [
        "snapshot_evidence.json", "snapshot_records.jsonl"],
        "snapshot output inventory")
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
    need(EXPECTED["frozen_C15_components"]
         - EXPECTED["successful_DSU_merges"]
         == EXPECTED["post_C27R2_components"], "math identity")
    with tempfile.TemporaryDirectory(dir=ROOT / ".cm2-runtime",
            prefix="c27r2-snapshot-v5-selftest-") as raw:
        path = Path(raw) / "member"
        path.write_bytes(b"authority\n")
        first = record(path)
        second = record(path)
        need(first == second and len(first["stat_fingerprint"]) == 9
             and first["size"] == 10 and first["O_NOFOLLOW"] is True,
             "real O_NOFOLLOW full9stat fixture")
        row_body = {"schema": BASE + "snapshot-member-row.v5", "ordinal": 0,
                    "role": "fixture", **first, "formal_credit": 0}
        row = {**row_body, "row_sha256": digest(row_body)}
        need(row["row_sha256"] == digest(row_body), "real row closure fixture")
    return {"status": "PASS_C27R2_RELEASE_REPAIR_SNAPSHOT_V5_SELF_TEST"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    for name in ("plan", "output-dir", "expect-self-sha256",
                 "expect-plan-file-sha256", "expect-plan-object-sha256"):
        parser.add_argument("--" + name)
    args = parser.parse_args()
    fields = ("plan", "output_dir", "expect_self_sha256",
              "expect_plan_file_sha256", "expect_plan_object_sha256")
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
