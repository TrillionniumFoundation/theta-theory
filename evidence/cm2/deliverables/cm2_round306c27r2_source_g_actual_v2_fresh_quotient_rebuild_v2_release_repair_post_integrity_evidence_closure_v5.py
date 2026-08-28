#!/usr/bin/env python3
"""Close C27R2 v5 evidence after 70 validator and eight lock checks.

The program reopens the Stage-A full9stat ledger, the baseline transaction,
the combined integrity transaction, its 70 distinct eleven-file validator
processes, the separate eight-case lock-preflight receipt, and the post
transaction.  Counts and closure booleans are
derived from current files; receipt claims are never accepted as substitutes.
It emits zero-credit evidence only and never writes a manifest or PASS marker.
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
SNAPSHOT_SCHEMA = BASE + "current-snapshot-evidence.v5"
SNAPSHOT_STATUS = (
    "PASS_C27R2_RELEASE_REPAIR_V5_CORE_FRESH_COLD_BOUNDARY_TRUST_EXACT_"
    "TERMINAL_INVENTORIES_AND_FULL9STAT_SNAPSHOT_FROZEN__ZERO_CREDIT_"
    "NOT_MANIFEST_AUTHORIZED"
)
POST_SCHEMA = BASE + "post-integrity-evidence-closure.v5"
POST_STATUS = (
    "PASS_C27R2_RELEASE_REPAIR_V5_SNAPSHOT_BASELINE_VALIDATOR70_LOCK8_REAL_"
    "TRANSACTIONS_POST_REPLAY_FULL9STAT_AND_PRIVATE_CLEANUP_CLOSED__ZERO_"
    "CREDIT_PENDING_MANIFEST"
)
PLAN_SCHEMA = BASE + "chain-plan.v5"
PLAN_STATUS = (
    "FROZEN_C27R2_RELEASE_REPAIR_V5_EXACT70_PLUS_LOCK8_PLAN__EXECUTION_DISABLED_"
    "PENDING_INDEPENDENT_FULL_CHAIN_AUDIT"
)
RUN_SCHEMA = BASE + "release-repair-process-run-attestation.v5"
RUN_STATUS = (
    "PASS_C27R2_RELEASE_REPAIR_PROCESS_EXIT0_NULL_SIGNAL_EMPTY_STDERR_"
    "EXACT_SPEC_PINSET_ARGV_ENV_PRE_POST_FULL9STAT_AND_OUTPUT_INVENTORY__"
    "ZERO_CREDIT"
)
RUN_PASS = b"PASS_C27R2_RELEASE_REPAIR_V5_PROCESS_TRANSACTION__ZERO_CREDIT\n"
RUN_FILES = {
    "PASS.lock", "exit_code.txt", "signal.json", "stderr.log", "stdout.log",
    "timing.json", "input_pre.json", "input_post.json",
    "output_validation.json", "runner_start.json", "run_attestation.json",
}
PRIOR_TRANSACTION_STAGES = (
    "boundary_preflight", "fresh_cold", "snapshot", "baseline",
    "integrity70_plus_lock8", "post",
)
LAUNCH_CONTROL_FILES = {
    "command_spec.json", "fd_bound_request.json", "pinset.json",
    "stage_launch_receipt.json",
}
FIXTURE_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "release-integrity-fixture.v5"
)
FIXTURE_STATUS = (
    "PASS_C27R2_RELEASE_BOUNDARY_V5_CONTROL_70_OF_70_REAL_VALIDATOR_WRAPPERS_"
    "AND_8_OF_8_PUBLICATION_LOCK_PREFLIGHTS_REJECTED__ZERO_CREDIT"
)
CASE_RUN_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "release-integrity-case-process-run.v5"
)
CASE_RUN_STATUS = (
    "PASS_REAL_WRAPPER_EXPECTED_VALIDATOR_EXIT2_NULL_SIGNAL_NO_OUTPUT_"
    "AUTHORITY_PRE_POST_FULL_TREE_AND_SERVICE_UNCHANGED__ZERO_CREDIT"
)
CASE_RUN_PASS = (
    b"PASS_C27R2_RELEASE_BOUNDARY_REAL_PER_CASE_WRAPPER_TRANSACTION__"
    b"ZERO_CREDIT\n"
)
FIXTURE_PASS = (
    b"PASS_C27R2_RELEASE_BOUNDARY_V5_70_VALIDATOR_PLUS_8_LOCK_CHECKS__"
    b"ZERO_CREDIT\n")
FIXTURE_CONTROL_FILES = {"baseline-validation.json", "baseline.stderr.log",
    "baseline.stdout.log", "empty-override-map.json",
    "publication-lock-preflight.json"}
LOCK_PREFLIGHT_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "release-publication-lock-preflight.v1")
LOCK_PREFLIGHT_STATUS = (
    "PASS_8_OF_8_REAL_PUBLICATION_LOCK_PROTOCOL_NEGATIVES_REJECTED__ZERO_CREDIT")
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
BOUNDARY_CONTRACT_FROZEN_GO = False  # boundary v5 NO-GO; append-only v6 pending.
FORMAL_EXECUTION_AUTHORIZED = False  # Independent full-chain GO has not been minted.
CASE_NAMES = (
    "wrong-core-unit", "wrong-core-invocation",
    "actual-terminal-directory-swap", "actual-base-directory-swap",
    "actual-terminal-receipt-file-pin", "actual-terminal-receipt-object-pin",
    "actual-terminal-root-pin", "actual-terminal-PASS-drift",
    "actual-payload-manifest-drift",
    "post-actual-gate-execution-receipt-drift",
    "post-actual-gate-PASS-drift", "seed1-identical-bytes-new-inode",
    "seed2-edge-drift", "frozen-C15-drift",
    "core-transaction-receipt-coherent-reclosure",
    "core-pinset-actual-pin-lie", "producer-command-spec-lie",
    "verifier-command-spec-seed-and-pin-lie", "attack-command-spec-lie",
    "candidate-result-census-coherent-reclosure", "candidate-truncated-gzip",
    "candidate-missing-member", "candidate-extra-member", "candidate-symlink",
    "candidate-hardlink", "independent-verification-coherent-reclosure",
    "core-attacks-coherent-reclosure", "producer-nonzero-exit",
    "verifier-signal", "attack-nonempty-stderr", "process-input-post-drift",
    "process-output-validation-drift", "cold-historical-verification-drift",
    "cold-receipt-coherent-reclosure", "evidence-inventory-member-drift",
    "wrong-PYTHONHASHSEED", "missing-isolated-python-flag",
    "atomic-replace-same-bytes-new-inode", "post-hash-content-TOCTOU",
    "payload-manifest-reorder", "manifest-duplicate", "manifest-traversal",
    "root-member-substitution", "outer-fake-release-count-coherent-reclosure",
    "future-seal-fake-authority", "terminal-byte-mismatch", "core-PASS-drift",
    "core-control-extra-member", "core-control-runner-stdout-drift",
    "gate-extra-member", "gate-stage-stdout-drift", "producer-run-extra-member",
    "producer-run-PASS-drift", "producer-run-stdout-drift",
    "producer-run-timing-drift", "producer-run-runner-start-drift",
    "cold-control-PASS-drift", "cold-control-runner-stdout-drift",
    "cold-run-extra-member", "cold-run-PASS-drift", "cold-run-stdout-drift",
    "cold-run-timing-drift", "cold-run-runner-start-drift",
    "producer-command-spec-extra-argv",
    "core-spec-extra-input", "cold-spec-extra-input",
    "attestation-extra-path", "attestation-omitted-path",
    "service-query-missing-bus-route", "service-query-wrong-bus-route",
)
LOCK_CASE_NAMES = ("missing-lock-arguments", "bad-inherited-fd",
    "wrong-inode-path-substitution", "unlocked-inherited-fd",
    "shared-only-inherited-lock", "symlink-or-nonsingleton-lock-path",
    "lock-pin-or-stat-drift", "early-close-or-unlock")
EXPECTED = {
    "frozen_C15_components": 57_876, "post_C27R2_components": 43_684,
    "proof_derived_component_edges": 14_860,
    "successful_DSU_merges": 14_192, "cycle_edges": 668,
    "frozen_C15_members": 502_204,
    "total_unordered_member_pairs": 126_104_177_706,
    "within_post_component_member_pairs": 542_179_508,
    "cross_post_component_member_pairs": 125_561_998_198,
}
ABSENCE_ROLES = ("outer", "conditional_seal", "anticipated_terminal",
                 "official_terminal")


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


def expand_argv(template: Any, bindings: Any) -> list[str]:
    need(type(template) is list and type(bindings) is dict
         and list(bindings) == sorted(bindings), "argv template/bindings")
    used: list[str] = []; answer: list[str] = []
    for token in template:
        need(type(token) is str and token and "\x00" not in token,
             "argv token")
        match = re.fullmatch(r"\$\{([A-Z][A-Z0-9_]*)\}", token)
        if match is None:
            need("${" not in token and "}" not in token,
                 "whole-token placeholder")
            answer.append(token)
        else:
            role = match.group(1); need(role in bindings, "known binding")
            used.append(role); answer.append(bindings[role])
    need(sorted(set(used)) == list(bindings), "all bindings used once or more")
    return answer


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
        current = os.stat(path, follow_symlinks=False)
        need(fingerprint(current) == fingerprint(before)
             and fingerprint(os.fstat(descriptor)) == fingerprint(before),
             "stable full9stat")
        return b"".join(chunks), {"path": str(path.relative_to(ROOT)), "sha256": state.hexdigest(),
                "size": before.st_size, "stat_fingerprint": fingerprint(before),
                "O_NOFOLLOW": True, "single_link": True}
    finally:
        os.close(descriptor)


def record(path: Path) -> dict[str, Any]:
    return capture(path, False)[1]


def read_current(path: Path) -> bytes:
    return capture(path)[0]


def plain_document(path: Path) -> dict[str, Any]:
    raw = read_current(path)
    need(raw.endswith(b"\n"), "plain JSON newline")
    value = strict(raw[:-1])
    need(type(value) is dict and canonical(value) == raw[:-1],
         "canonical plain JSON")
    return value


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


def read_snapshot(directory: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    need(directory.is_dir() and sorted(x.name for x in directory.iterdir()) == [
        "snapshot_evidence.json", "snapshot_records.jsonl"],
        "snapshot exact inventory")
    receipt = document(directory / "snapshot_evidence.json",
                       "snapshot_evidence_sha256")[0]
    need(receipt.get("schema") == SNAPSHOT_SCHEMA
         and receipt.get("status") == SNAPSHOT_STATUS
         and receipt.get("exact_math") == EXPECTED
         and receipt.get("fixture_credit_claimed") is False
         and receipt.get("formal_credit") == 0
         and receipt.get("manifest_authorized") is False,
         "snapshot receipt contract")
    raw, ledger_item = capture(directory / "snapshot_records.jsonl")
    need(raw.endswith(b"\n"), "snapshot ledger newline")
    rows: list[dict[str, Any]] = []
    for ordinal, line in enumerate(raw.splitlines()):
        row = strict(line)
        body = dict(row)
        claim = body.pop("row_sha256", None)
        need(type(row) is dict and canonical(row) == line
             and row.get("schema") == BASE + "snapshot-member-row.v5"
             and row.get("ordinal") == ordinal
             and valid_sha(claim) and claim == digest(body)
             and type(row.get("stat_fingerprint")) is list
             and len(row["stat_fingerprint"]) == 9
             and row.get("size") == row["stat_fingerprint"][4]
             and row.get("O_NOFOLLOW") is True
             and row.get("single_link") is True,
             "snapshot row contract")
        rows.append(row)
    need(len(rows) == receipt.get("snapshot_record_count")
         and ledger_item["sha256"] == receipt.get("snapshot_records_file_sha256"),
         "snapshot descriptor")
    return receipt, rows


def plan_contract(path: Path, file_pin: str, object_pin: str) -> dict[str, Any]:
    plan, item = document(path, "plan_sha256")
    need(item["sha256"] == file_pin and plan["plan_sha256"] == object_pin
         and plan.get("schema") == PLAN_SCHEMA and plan.get("status") == PLAN_STATUS
         and plan.get("validator_negative_case_count") == 70
         and plan.get("publication_lock_preflight_case_count") == 8
         and plan.get("total_integrity_check_count") == 78
         and "case_count" not in plan
         and tuple(plan.get("ordered_case_names", [])) == CASE_NAMES
         and plan.get("ordered_validator70_object_sha256")
             == ORDERED_VALIDATOR70_OBJECT_SHA
         and plan.get("ordered_lock8_object_sha256") == ORDERED_LOCK8_OBJECT_SHA
         and plan.get("exact_math") == EXPECTED
         and plan.get("execution_enabled") is False
         and plan.get("formal_credit") == 0, "frozen plan")
    sources = plan.get("sources")
    need(type(sources) is dict
         and sources.get("boundary_validator") == {
             "path": BOUNDARY_VALIDATOR_PATH, "sha256": BOUNDARY_VALIDATOR_SHA}
         and sources.get("integrity70_plus_lock8_runner") == {
             "path": INTEGRITY_RUNNER_PATH, "sha256": INTEGRITY_RUNNER_SHA}
         and record(inside(BOUNDARY_VALIDATOR_PATH))["sha256"]
             == BOUNDARY_VALIDATOR_SHA
         and record(inside(INTEGRITY_RUNNER_PATH))["sha256"]
             == INTEGRITY_RUNNER_SHA,
         "frozen boundary sources")
    return plan


def exact_regular_members(directory: Path, names: set[str], label: str
                         ) -> dict[str, tuple[bytes, dict[str, Any]]]:
    need(directory.is_dir() and not directory.is_symlink(),
         label + ": directory")
    entries = list(os.scandir(directory))
    need({entry.name for entry in entries} == names and len(entries) == len(names),
         label + ": exact inventory")
    for entry in entries:
        info = entry.stat(follow_symlinks=False)
        need(not entry.is_symlink() and stat.S_ISREG(info.st_mode)
             and info.st_nlink == 1,
             label + ": every member regular single-link")
    return {name: capture(directory / name) for name in sorted(names)}


def transaction(directory: Path, plan: dict[str, Any], role: str) -> dict[str, Any]:
    members = exact_regular_members(directory, RUN_FILES,
                                    "transaction:" + role)
    need(members["PASS.lock"][0] == RUN_PASS
         and members["exit_code.txt"][0] == b"0\n"
         and members["signal.json"][0] == b"null\n"
         and members["stderr.log"][0] == b""
         and members["input_pre.json"][0] == members["input_post.json"][0],
         "transaction scalar bytes:" + role)
    run, _ = document(directory / "run_attestation.json",
                      "run_attestation_sha256")
    spec = plan.get("stage_templates", {}).get(role)
    need(type(spec) is dict and type(spec.get("source_role")) is str
         and spec["source_role"] in plan.get("sources", {})
         and type(spec.get("input_roles")) is list
         and type(spec.get("output_roots")) is list,
         "two-layer transaction plan role")
    source = plan["sources"][spec["source_role"]]
    input_paths = sorted({plan["role_map"][name]["path"]
                          for name in spec["input_roles"]})
    output_roots = [{"path": plan["role_map"][row["role"]]["path"],
                     "exact_files": row["exact_files"]}
                    for row in spec["output_roots"]]
    control = inside(plan["launch_control_dir"]) / "transactions" / role
    command_spec_path = control / "command_spec.json"
    pinset_path = control / "pinset.json"
    launch, _ = document(control / "stage_launch_receipt.json",
                         "stage_launch_receipt_sha256")
    command_spec, command_spec_record = document(
        command_spec_path, "command_spec_sha256")
    pinset, pinset_record = document(pinset_path, "pinset_sha256")
    request, request_record = document(control / "fd_bound_request.json",
                                       "request_sha256")
    expected_attested = [str(command_spec_path.relative_to(ROOT)),
        str(pinset_path.relative_to(ROOT)), *input_paths,
        str((control / "fd_bound_request.json").relative_to(ROOT))]
    bindings = run.get("argv_bindings")
    template = run.get("argv_template")
    expanded = expand_argv(template, bindings)
    expected_environment = {"PATH": "/usr/bin:/bin", "HOME": "/nonexistent",
        "LANG": "C", "LC_ALL": "C", "TZ": "UTC",
        "PYTHONHASHSEED": spec["python_hash_seed"]}
    stdout_raw = members["stdout.log"][0]
    need(stdout_raw.endswith(b"\n"), "transaction stdout newline:" + role)
    stdout_value = strict(stdout_raw[:-1])
    need(type(stdout_value) is dict and canonical(stdout_value) == stdout_raw[:-1],
         "transaction canonical stdout:" + role)
    timing = plain_document(directory / "timing.json")
    output_validation = plain_document(directory / "output_validation.json")
    runner_start = plain_document(directory / "runner_start.json")
    input_pre = plain_document(directory / "input_pre.json")
    input_post = plain_document(directory / "input_post.json")
    claimed_members = run.get("member_file_sha256")
    expected_member_names = RUN_FILES - {"PASS.lock", "run_attestation.json"}
    expected_member_hashes = {name: members[name][1]["sha256"]
                              for name in sorted(expected_member_names)}
    need(run.get("schema") == RUN_SCHEMA and run.get("status") == RUN_STATUS
         and run.get("stage") == role
         and run.get("stage_source_path") == source["path"]
         and run.get("stage_source_sha256") == source["sha256"]
         and run.get("command_spec_file_sha256")
             == command_spec_record["sha256"]
         and run.get("command_spec_object_sha256")
             == command_spec["command_spec_sha256"]
         and run.get("pinset_file_sha256") == pinset_record["sha256"]
         and run.get("pinset_object_sha256") == pinset["pinset_sha256"]
         and run.get("fd_bound_request_file_sha256") == request_record["sha256"]
         and run.get("fd_bound_request_object_sha256") == request["request_sha256"]
         and run.get("fd_bound_input_map_sha256")
             == digest(request["input_files"])
         and run.get("fd_bound_output_dirfd_map_sha256")
             == digest(request["output_roots"])
         and run.get("fd_bound_wrapper_path")
             == command_spec.get("fd_bound_wrapper_path")
             == pinset.get("fd_bound_wrapper_path")
         and run.get("fd_bound_wrapper_sha256")
             == command_spec.get("fd_bound_wrapper_sha256")
             == pinset.get("fd_bound_wrapper_sha256")
         and request.get("stage") == role
         and request.get("stage_source_path") == source["path"]
         and request.get("stage_source_sha256") == source["sha256"]
         and request.get("original_argv") == expanded
         and request.get("exact_environment") == expected_environment
         and request.get("formal_credit") == 0
         and request.get("manifest_authorized") is False
         and request.get("authority_minted") is False
         and template == spec["argv_template"]
         and run.get("argv_template_sha256") == spec["argv_template_sha256"]
             == digest(template)
         and run.get("argv_bindings_sha256") == digest(bindings)
         and run.get("exact_argv") == expanded
         and run.get("expanded_argv_sha256") == digest(expanded)
         and run.get("outer_runner_argv_sha256")
             == digest(run.get("outer_runner_argv"))
         and launch.get("argv_template_sha256") == digest(template)
         and launch.get("argv_bindings_sha256") == digest(bindings)
         and launch.get("expanded_argv_sha256") == digest(expanded)
         and launch.get("outer_runner_argv_sha256")
             == run.get("outer_runner_argv_sha256")
         and launch.get("fd_bound_wrapper_path")
             == run.get("fd_bound_wrapper_path")
         and launch.get("fd_bound_wrapper_sha256")
             == run.get("fd_bound_wrapper_sha256")
         and run.get("exact_environment") == expected_environment
         and run.get("exact_input_paths") == input_paths
         and run.get("exact_attested_contract_paths") == expected_attested
         and run.get("exact_output_roots") == output_roots
         and run.get("publication_lock_exclusive_inherited_and_held") is True
         and run.get("numeric_exit_code") == 0 and run.get("signal") is None
         and run.get("timed_out") is False and run.get("stderr_empty") is True
         and run.get("input_pre_post_sha_full9stat_identical") is True
         and run.get("input_attestations") == input_pre == input_post
         and stdout_value == spec.get("expected_stdout")
         and run.get("stdout_sha256") == hashlib.sha256(stdout_raw).hexdigest()
         and set(timing) == {"elapsed_seconds", "timed_out"}
         and timing.get("elapsed_seconds") == run.get("elapsed_seconds")
         and timing.get("timed_out") is False
         and output_validation == run.get("output_validation")
         and set(runner_start) == {"schema", "stage", "started_at_utc",
             "formal_credit", "fd_bound_formal_stage",
             "fd_bound_request_object_sha256", "C27R2", "CM2"}
         and runner_start.get("schema") == RUN_SCHEMA + ".start"
         and runner_start.get("stage") == role
         and runner_start.get("started_at_utc") == run.get("started_at_utc")
         and runner_start.get("fd_bound_formal_stage") is True
         and runner_start.get("fd_bound_request_object_sha256")
             == request["request_sha256"]
         and run.get("exact_inventory") == sorted(RUN_FILES)
         and claimed_members == expected_member_hashes
         and run.get("fd_bound_parent_directory_swap_defense") is True
         and type(run.get("fd_bound_execution_result")) is dict
         and run["fd_bound_execution_result"].get("request_object_sha256")
             == request["request_sha256"]
         and run.get("formal_credit") == 0
         and run.get("manifest_authorized") is False,
         "transaction facts:" + role)
    return run


def case_transaction(directory: Path, case: str, ordinal: int,
                     expected_sources: dict[str, Any]) -> dict[str, Any]:
    members = exact_regular_members(directory, RUN_FILES,
                                    "case:" + case)
    need(members["PASS.lock"][0] == CASE_RUN_PASS
         and members["exit_code.txt"][0] == b"0\n"
         and members["signal.json"][0] == b"null\n"
         and members["stderr.log"][0] == b"",
         "case scalar closure")
    run, _ = document(directory / "run_attestation.json",
                      "run_attestation_sha256")
    start = plain_document(directory / "runner_start.json")
    output = document(directory / "output_validation.json",
                      "output_validation_sha256")[0]
    input_value = plain_document(directory / "input_pre.json")
    input_post = plain_document(directory / "input_post.json")
    stdout = plain_document(directory / "stdout.log")
    request = input_value.get("wrapper_request")
    need(run.get("schema") == CASE_RUN_SCHEMA
         and run.get("status") == CASE_RUN_STATUS
         and run.get("mode") == "formal" and run.get("case") == case
         and run.get("ordinal") == ordinal
         and run.get("real_wrapper_process") is True
         and run.get("wrapper_expected_numeric_exit_code") == 0
         and run.get("wrapper_expected_signal") is None
         and run.get("wrapper_expected_stderr_empty") is True
         and run.get("actual_child_numeric_exit_code") == 2
         and run.get("actual_child_signal") is None
         and run.get("actual_child_timed_out") is False
         and run.get("actual_child_validator_output_created") is False
         and run.get("actual_authority_pre_post_identical") is True
         and type(request) is dict
         and request.get("source_pins") == expected_sources
         and input_value.get("validator_command") == start.get("exact_argv")
         and input_value.get("validator_environment")
             == start.get("exact_environment")
         and input_post.get("validator_command")
             == input_value.get("validator_command")
         and input_post.get("validator_environment")
             == input_value.get("validator_environment")
         and input_value.get("schema") == CASE_RUN_SCHEMA + ".input.v1"
         and input_post.get("schema") == CASE_RUN_SCHEMA + ".input.v1"
         and input_value.get("phase") == "pre"
         and input_post.get("phase") == "post"
         and input_value.get("snapshot") == input_post.get("snapshot")
         and run.get("actual_authority_pre_snapshot_sha256")
             == input_value.get("snapshot", {}).get("snapshot_sha256")
         and run.get("actual_authority_post_snapshot_sha256")
             == input_post.get("snapshot", {}).get("snapshot_sha256")
         and run.get("request_file_sha256")
             == input_value.get("request_file_sha256")
             == input_post.get("request_file_sha256")
         and run.get("request_object_sha256")
             == input_value.get("request_object_sha256")
             == input_post.get("request_object_sha256")
         and output.get("expected_validator_rejection") is True
         and output.get("child_numeric_exit_code") == 2
         and output.get("child_signal") is None
         and output.get("child_validator_output_created") is False
         and stdout.get("schema") == CASE_RUN_SCHEMA + ".stdout.v1"
         and stdout.get("status") == CASE_RUN_STATUS
         and stdout.get("case") == case
         and run.get("exact_inventory") == sorted(RUN_FILES)
         and run.get("formal_credit") == 0
         and run.get("manifest_authorized") is False,
         "case factual contract:" + case)
    claimed_members = run.get("member_file_sha256")
    need(type(claimed_members) is dict
         and set(claimed_members) == RUN_FILES - {"PASS.lock", "run_attestation.json"}
         and all(record(directory / name)["sha256"] == claim
                 for name, claim in claimed_members.items()),
         "case member hashes:" + case)
    return run


def execute(args: argparse.Namespace) -> dict[str, Any]:
    need(FORMAL_EXECUTION_AUTHORIZED and BOUNDARY_CONTRACT_FROZEN_GO,
         "boundary v5 NO-GO; append-only boundary v6 independent GO required")
    need(all(valid_sha(x) for x in (args.expect_self_sha256,
        args.expect_plan_file_sha256, args.expect_plan_object_sha256,
        args.expect_snapshot_file_sha256, args.expect_snapshot_object_sha256,
        args.expect_fixture_file_sha256, args.expect_fixture_object_sha256)),
        "SHA pins")
    need(record(SELF)["sha256"] == args.expect_self_sha256, "self pin")
    plan_path = inside(args.plan)
    plan = plan_contract(plan_path, args.expect_plan_file_sha256,
                         args.expect_plan_object_sha256)
    snapshot_dir = inside(args.snapshot_dir)
    snapshot, rows = read_snapshot(snapshot_dir)
    snapshot_file = record(snapshot_dir / "snapshot_evidence.json")
    need(snapshot_file["sha256"] == args.expect_snapshot_file_sha256
         and snapshot["snapshot_evidence_sha256"]
             == args.expect_snapshot_object_sha256
         and snapshot.get("plan_file_sha256") == args.expect_plan_file_sha256
         and snapshot.get("plan_object_sha256") == args.expect_plan_object_sha256,
         "snapshot pins")

    need(inside(args.baseline_run) == inside(plan["fresh_paths"]["baseline"])
         and inside(args.cases_run)
             == inside(plan["fresh_paths"]["integrity70_plus_lock8"])
         and inside(args.post_run) == inside(plan["fresh_paths"]["post"]),
         "CLI transaction roots equal frozen plan paths")
    prior_runs = {stage: transaction(inside(plan["fresh_paths"][stage]),
                                     plan, stage)
                  for stage in PRIOR_TRANSACTION_STAGES}
    baseline = prior_runs["baseline"]
    cases_outer = prior_runs["integrity70_plus_lock8"]
    post = prior_runs["post"]
    fixture_path = inside(args.fixture_receipt)
    fixture, fixture_record = document(fixture_path, "fixture_receipt_sha256")
    need(fixture_record["sha256"] == args.expect_fixture_file_sha256
         and fixture["fixture_receipt_sha256"] == args.expect_fixture_object_sha256
         and fixture.get("schema") == FIXTURE_SCHEMA
         and fixture.get("status") == FIXTURE_STATUS
         and fixture.get("mode") == "formal"
         and fixture.get("validator_negative_case_count") == 70
         and fixture.get("validator_rejected_count") == 70
         and fixture.get("publication_lock_preflight_case_count") == 8
         and fixture.get("publication_lock_preflight_rejected_count") == 8
         and fixture.get("total_integrity_check_count") == 78
         and "case_count" not in fixture
         and fixture.get("accepted_count") == 0
         and fixture.get("validator_wrapper_process_execution_count") == 70
         and fixture.get("publication_lock_preflight_process_execution_count") == 8
         and tuple(fixture.get("ordered_validator_negative_case_names", []))
             == CASE_NAMES
         and tuple(fixture.get("ordered_publication_lock_preflight_case_names", []))
             == LOCK_CASE_NAMES
         and fixture.get("ordered_validator_negative_inventory_sha256")
             == ORDERED_VALIDATOR70_OBJECT_SHA
         and fixture.get("ordered_publication_lock_preflight_inventory_sha256")
             == ORDERED_LOCK8_OBJECT_SHA
         and fixture.get("formal_credit") == 0
         and fixture.get("manifest_authorized") is False,
         "validator70 plus lock8 fixture receipt")
    expected_sources = fixture.get("source_pins")
    need(type(expected_sources) is dict
         and expected_sources == plan.get("boundary_source_pins"),
         "frozen boundary source pins")
    case_dirs = fixture.get("validator_case_process_directories")
    case_rows = fixture.get("validator_cases")
    need(type(case_dirs) is list and len(case_dirs) == 70
         and len(set(case_dirs)) == 70
         and type(case_rows) is list and len(case_rows) == 70,
         "70 distinct validator process directories")
    work_root = fixture_path.parent
    case_paths = [inside(path) for path in case_dirs]
    need(all(path.parent == work_root and path.name.startswith("case-process-")
             for path in case_paths), "case directories direct under work root")
    control = work_root / "control"
    expected_top = {"control", "fixture_receipt.json", "PASS.lock",
                    *(path.name for path in case_paths)}
    need({path.name for path in work_root.iterdir()} == expected_top
         and len(expected_top) == 73
         and control.is_dir() and not control.is_symlink()
         and {path.name for path in control.iterdir()} == FIXTURE_CONTROL_FILES
         and read_current(work_root / "PASS.lock") == FIXTURE_PASS
         and read_current(control / "baseline.stderr.log") == b"",
         "fixture top exact73/control exact5/PASS/current baseline stderr")
    lock_receipt, lock_receipt_record = document(
        control / "publication-lock-preflight.json",
        "lock_preflight_receipt_sha256")
    need(lock_receipt.get("schema") == LOCK_PREFLIGHT_SCHEMA
         and lock_receipt.get("status") == LOCK_PREFLIGHT_STATUS
         and lock_receipt.get("publication_lock_preflight_case_count") == 8
         and lock_receipt.get("publication_lock_preflight_rejected_count") == 8
         and tuple(lock_receipt.get(
             "ordered_publication_lock_preflight_case_names", []))
             == LOCK_CASE_NAMES
         and lock_receipt.get(
             "ordered_publication_lock_preflight_inventory_sha256")
             == ORDERED_LOCK8_OBJECT_SHA
         and lock_receipt.get("formal_credit") == 0
         and lock_receipt.get("manifest_authorized") is False
         and valid_sha(lock_receipt_record["sha256"]),
         "separate eight-case publication-lock preflight receipt")
    reopened: list[dict[str, Any]] = []
    for ordinal, (name, shown, receipt_row) in enumerate(
            zip(CASE_NAMES, case_dirs, case_rows, strict=True)):
        need(type(receipt_row) is dict and receipt_row.get("ordinal") == ordinal
             and receipt_row.get("case") == name
             and receipt_row.get("case_process_directory") == shown
             and receipt_row.get("numeric_exit_code") == 2
             and receipt_row.get("signal") is None
             and receipt_row.get("timed_out") is False
             and receipt_row.get("validator_output_created") is False,
             "fixture case row:" + name)
        reopened.append(case_transaction(case_paths[ordinal], name, ordinal,
                                         expected_sources))
    need(list(work_root.glob("private-c27r2-release-fixture-*")) == [],
         "zero private fixture roots")
    sentinels = plan.get("future_absence_sentinels")
    need(type(sentinels) is dict and tuple(sorted(sentinels))
         == tuple(sorted(ABSENCE_ROLES)), "exact future absence sentinel roles")
    absence_records: list[dict[str, Any]] = []
    for role in ABSENCE_ROLES:
        path = inside(sentinels[role], absent=True)
        need(not path.exists() and not path.is_symlink()
             and path.parent.is_dir() and not path.parent.is_symlink(),
             "final future absence:" + role)
        absence_records.append({"role": role,
            "path": str(path.relative_to(ROOT)), "absent": True,
            "parent_stat_fingerprint": fingerprint(os.stat(
                path.parent, follow_symlinks=False))})

    # Decisive Stage-A comparison: current records must be byte-for-byte equal.
    for row in rows:
        current = record(inside(row["path"]))
        expected = {key: row[key] for key in (
            "path", "sha256", "size", "stat_fingerprint", "O_NOFOLLOW",
            "single_link")}
        need(current == expected, "Stage-A current full9stat:" + row["role"])

    publication_lock_path = inside(plan["publication_lock"]["path"])
    evidence_paths = {SELF, plan_path, publication_lock_path,
        snapshot_dir / "snapshot_evidence.json",
        snapshot_dir / "snapshot_records.jsonl", fixture_path,
        work_root / "PASS.lock"}
    evidence_paths.update(path for path in control.iterdir() if path.is_file())
    launch_root = inside(plan["launch_control_dir"]) / "transactions"
    for stage in PRIOR_TRANSACTION_STAGES:
        launch = launch_root / stage
        need(launch.is_dir() and not launch.is_symlink()
             and {path.name for path in launch.iterdir()} == LAUNCH_CONTROL_FILES,
             "exact stage launch-control inventory:" + stage)
        evidence_paths.update(path for path in launch.iterdir() if path.is_file())
    for root in (*(inside(plan["fresh_paths"][stage])
                   for stage in PRIOR_TRANSACTION_STAGES),
                 *(inside(path) for path in case_dirs)):
        evidence_paths.update(path for path in root.iterdir() if path.is_file())
    records = [record(path) for path in sorted(evidence_paths)]
    output = inside(args.output_dir, absent=True)
    need(not output.exists() and not output.is_symlink(), "fresh output")
    output.mkdir(parents=True, mode=0o700)
    fsync_directory(output)
    fsync_directory(output.parent)
    inventory = output / "authority_records.jsonl"
    inventory_rows: list[dict[str, Any]] = []
    for ordinal, item in enumerate(records):
        body = {"schema": BASE + "post-authority-member-row.v5",
                "ordinal": ordinal, **item, "formal_credit": 0}
        inventory_rows.append({**body, "row_sha256": digest(body)})
    write_once(inventory, b"".join(canonical(row) + b"\n"
                                   for row in inventory_rows))
    body = {
        "schema": POST_SCHEMA, "status": POST_STATUS,
        "completed_at_utc": datetime.now(timezone.utc).isoformat(
            timespec="microseconds").replace("+00:00", "Z"),
        "plan_file_sha256": args.expect_plan_file_sha256,
        "plan_object_sha256": args.expect_plan_object_sha256,
        "snapshot_evidence_file_sha256": snapshot_file["sha256"],
        "snapshot_evidence_object_sha256": snapshot["snapshot_evidence_sha256"],
        "baseline_run_object_sha256": baseline["run_attestation_sha256"],
        "integrity70_plus_lock8_run_object_sha256":
            cases_outer["run_attestation_sha256"],
        "post_run_object_sha256": post["run_attestation_sha256"],
        "prior_transaction_stage_count": len(PRIOR_TRANSACTION_STAGES),
        "prior_transaction_stages": list(PRIOR_TRANSACTION_STAGES),
        "prior_transaction_run_object_sha256": {
            stage: prior_runs[stage]["run_attestation_sha256"]
            for stage in PRIOR_TRANSACTION_STAGES},
        "stage_launch_control_exact_member_count": len(LAUNCH_CONTROL_FILES),
        "all_prior_stage_launch_controls_reopened": True,
        "publication_lock_file_sha256": record(publication_lock_path)["sha256"],
        "fixture_receipt_file_sha256": fixture_record["sha256"],
        "fixture_receipt_object_sha256": fixture["fixture_receipt_sha256"],
        "ordered_validator_negative_case_names": list(CASE_NAMES),
        "ordered_publication_lock_preflight_case_names": list(LOCK_CASE_NAMES),
        "ordered_validator70_object_sha256": ORDERED_VALIDATOR70_OBJECT_SHA,
        "ordered_lock8_object_sha256": ORDERED_LOCK8_OBJECT_SHA,
        "validator_negative_case_count": 70,
        "validator_rejected_count": 70,
        "publication_lock_preflight_case_count": 8,
        "publication_lock_preflight_rejected_count": 8,
        "total_integrity_check_count": 78, "accepted_count": 0,
        "real_validator_wrapper_process_count": 70,
        "real_lock_preflight_process_count": 8,
        "publication_lock_preflight_file_sha256": lock_receipt_record["sha256"],
        "publication_lock_preflight_object_sha256":
            lock_receipt["lock_preflight_receipt_sha256"],
        "case_process_transcripts_reopened": len(reopened),
        "fixture_top_entry_count": len(expected_top),
        "fixture_control_member_count": len(FIXTURE_CONTROL_FILES),
        "fixture_top_and_control_exact_inventories_reopened": True,
        "snapshot_records_reopened": len(rows),
        "authority_pre_post_sha_full9stat_identical": True,
        "private_fixture_root_count": 0, "case_cleanup_complete": True,
        "final_future_absence_records": absence_records,
        "final_future_absence_roles": list(ABSENCE_ROLES),
        "authority_records_file_sha256": record(inventory)["sha256"],
        "authority_record_count": len(inventory_rows),
        "exact_math": EXPECTED, "formal_credit": 0,
        "manifest_authorized": False, "authority_minted": False,
        "C27R2": "AUDIT_HOLD_UNAUTHORIZED", "C28_C29": "UNAUTHORIZED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    receipt = {**body, "post_integrity_evidence_sha256": digest(body)}
    write_once(output / "post_integrity_evidence.json", canonical(receipt) + b"\n")
    need(sorted(path.name for path in output.iterdir()) == [
        "authority_records.jsonl", "post_integrity_evidence.json"],
        "post evidence output inventory")
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
    need(len(CASE_NAMES) == 70 and len(set(CASE_NAMES)) == 70
         and len(LOCK_CASE_NAMES) == 8 and len(set(LOCK_CASE_NAMES)) == 8
         and not set(CASE_NAMES) & set(LOCK_CASE_NAMES),
         "separate exact unique validator70 and lock8 names")
    with tempfile.TemporaryDirectory(dir=ROOT / ".cm2-runtime",
            prefix="c27r2-post-v5-selftest-") as raw:
        root = Path(raw)
        member = root / "member"
        member.write_bytes(b"x\n")
        before = record(member)
        after = record(member)
        need(before == after and len(before["stat_fingerprint"]) == 9,
             "real Stage-A/Stage-B record equality")
        case = root / "case"
        case.mkdir()
        for name in RUN_FILES:
            (case / name).write_bytes(b"")
        need(set(exact_regular_members(case, RUN_FILES, "selftest")) == RUN_FILES,
             "real eleven-member inventory fixture")
        extra = case / "extra-directory"; extra.mkdir()
        rejected = False
        try:
            exact_regular_members(case, RUN_FILES, "extra-negative")
        except Blocked:
            rejected = True
        need(rejected, "extra directory rejected")
        extra.rmdir()
        victim = case / "timing.json"; victim.unlink()
        victim.symlink_to(case / "stdout.log")
        rejected = False
        try:
            exact_regular_members(case, RUN_FILES, "symlink-negative")
        except Blocked:
            rejected = True
        need(rejected, "symlink member rejected")
    return {"status": "PASS_C27R2_RELEASE_REPAIR_POST_V5_SELF_TEST"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    for name in ("plan", "snapshot-dir", "baseline-run", "cases-run",
                 "post-run", "fixture-receipt", "output-dir",
                 "expect-self-sha256", "expect-plan-file-sha256",
                 "expect-plan-object-sha256", "expect-snapshot-file-sha256",
                 "expect-snapshot-object-sha256", "expect-fixture-file-sha256",
                 "expect-fixture-object-sha256"):
        parser.add_argument("--" + name)
    args = parser.parse_args()
    fields = tuple(action.dest for action in parser._actions
                   if action.dest not in {"help", "self_test"})
    try:
        if args.self_test:
            need(all(getattr(args, name) is None for name in fields),
                 "self-test no arguments")
            result = self_test()
        else:
            need(all(getattr(args, name) is not None for name in fields),
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
