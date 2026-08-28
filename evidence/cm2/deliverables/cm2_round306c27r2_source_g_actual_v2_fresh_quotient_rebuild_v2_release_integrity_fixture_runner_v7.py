#!/usr/bin/env python3
"""Run the exact 70 real C27R2 release-boundary integrity fixtures.

The runner is append-only and permanently zero-credit.  It first invokes the
independent boundary validator once with a file/object-pinned empty override,
then executes eight independent publication-lock protocol preflights and 70
isolated real per-case wrapper subprocesses.  Each validator negative case has
exactly one allowlisted logical override mapped to ``CASE_ROOT/override``;
ordinary copies are used sequentially and removed after the case, so ext4
without reflink remains bounded well below 3 GiB.  Authoritative files are
snapshotted before and after the suite and are never edited.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import time
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent.parent
AUDIT = ROOT / ".cm2-runtime/audit"
SELF = Path(__file__).resolve()
VALIDATOR_DEFAULT = ROOT / "deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_quotient_rebuild_v2_release_repair_boundary_independent_validator_v7.py"
CASE_WRAPPER_DEFAULT = ROOT / "deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_quotient_rebuild_v2_release_integrity_case_transaction_wrapper_v2.py"
PREFIX = "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
OVERRIDE_SCHEMA = PREFIX + "release-repair-boundary-override-map.v7"
RESULT_SCHEMA = PREFIX + "release-integrity-fixture.v7"
RESULT_STATUS = (
    "PASS_C27R2_RELEASE_BOUNDARY_V7_CONTROL_70_OF_70_REAL_SINGLE_OPEN_"
    "VALIDATOR_WRAPPERS_AND_8_OF_8_PUBLICATION_LOCK_PREFLIGHTS_REJECTED_"
    "WITH_TEN_PROPERTY_SERVICE_IDENTITY_AND_COLD_EXACT14__ZERO_CREDIT"
)
PASS_BYTES = (
    b"PASS_C27R2_RELEASE_BOUNDARY_V7_70_VALIDATOR_PLUS_8_LOCK_CHECKS__"
    b"ZERO_CREDIT\n"
)
EMPTY_SHA = hashlib.sha256(b"").hexdigest()
MAX_CAPTURE_BYTES = 1 << 20

SYSTEMCTL = Path("/usr/bin/systemctl")
SYSTEMCTL_SHA256 = (
    "7ba82b5ba146759c710e1b80fadaa3fdbc0f9b85c8fb2c8c3196b7b1a0037ef8"
)
SERVICE_UID = 1000
SERVICE_RUNTIME = Path("/run/user/1000")
SERVICE_BUS = SERVICE_RUNTIME / "bus"
SERVICE_TRANSIENT = SERVICE_RUNTIME / "systemd/transient"
SERVICE_FIELDS = (
    "Id", "LoadState", "ActiveState", "SubState", "Result",
    "ExecMainCode", "ExecMainStatus", "InvocationID", "ExecStart",
    "FragmentPath",
)
CONTROL_BUS_ENV = {
    "PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
    "XDG_RUNTIME_DIR": "/run/user/1000",
    "DBUS_SESSION_BUS_ADDRESS": "unix:path=/run/user/1000/bus",
}
PUBLICATION_LOCK_SCHEMA = (
    "cm2.round306c27r2.source-g-authority-v2.release-repair."
    "publication-lock.v1"
)
PUBLICATION_LOCK_STATUS = "FROZEN_ONE_SHOT_PUBLICATION_LOCK__NO_AUTHORITY"
PUBLICATION_LOCK_PROTOCOL = "FLOCK_EXCLUSIVE_WHOLE_PUBLICATION_WINDOW_V1"

CASE_RUN_FILES = {
    "PASS.lock", "exit_code.txt", "signal.json", "stderr.log",
    "stdout.log", "timing.json", "input_pre.json", "input_post.json",
    "output_validation.json", "runner_start.json", "run_attestation.json",
}
CASE_RUN_PASS = (
    b"PASS_C27R2_RELEASE_BOUNDARY_REAL_PER_CASE_WRAPPER_TRANSACTION__"
    b"ZERO_CREDIT\n"
)
CONTROL_OUTPUT_FILES = {
    "baseline-validation.json", "baseline.stderr.log", "baseline.stdout.log",
    "empty-override-map.json", "publication-lock-preflight.json",
}
CASE_RUN_SCHEMA = PREFIX + "release-integrity-case-process-run.v6"
CASE_RUN_STATUS = (
    "PASS_REAL_SINGLE_OPEN_WRAPPER_EXPECTED_VALIDATOR_EXIT2_NULL_SIGNAL_NO_"
    "OUTPUT_AUTHORITY_PRE_POST_FULL_TREE_AND_TEN_PROPERTY_SERVICE_"
    "UNCHANGED__ZERO_CREDIT"
)
CASE_WRAPPER_REQUEST_SCHEMA = PREFIX + "release-integrity-case-wrapper-request.v2"
CASE_WRAPPER_REQUEST_STATUS = (
    "FROZEN_REAL_PER_CASE_WRAPPER_REQUEST_V2__ZERO_CREDIT")
LOCK_PREFLIGHT_SCHEMA = PREFIX + "release-publication-lock-preflight.v1"
LOCK_PREFLIGHT_STATUS = (
    "PASS_8_OF_8_REAL_PUBLICATION_LOCK_PROTOCOL_NEGATIVES_REJECTED__"
    "ZERO_CREDIT"
)
LOCK_PREFLIGHT_CASE_NAMES = [
    "missing-lock-arguments",
    "bad-inherited-fd",
    "wrong-inode-path-substitution",
    "unlocked-inherited-fd",
    "shared-only-inherited-lock",
    "symlink-or-nonsingleton-lock-path",
    "lock-pin-or-stat-drift",
    "early-close-or-unlock",
]

CORE_SOURCE_RELATIVES = (
    "deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_quotient_rebuild_v2_producer_v4.py",
    "deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_quotient_rebuild_v2_independent_verifier_v4.py",
    "deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_quotient_rebuild_v2_coherent_attack_harness_v4.py",
    "deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_quotient_rebuild_v2_transaction_runner_v4.py",
    "deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_quotient_rebuild_v2_gated_dual_seed_watcher_v6.py",
)
GATE_SOURCE_RELATIVES = (
    "deliverables/cm2_round306c27r2_post_actual_v2_rebuild_gate_v3.py",
    "deliverables/cm2_round306c27r2_post_actual_v2_rebuild_gate_v3_independent_verifier_r2.py",
    "deliverables/cm2_round306c27r2_post_actual_v2_rebuild_gate_v3_coherent_attack_harness_r2.py",
)

CASE_NAMES = [
    "wrong-core-unit",
    "wrong-core-invocation",
    "actual-terminal-directory-swap",
    "actual-base-directory-swap",
    "actual-terminal-receipt-file-pin",
    "actual-terminal-receipt-object-pin",
    "actual-terminal-root-pin",
    "actual-terminal-PASS-drift",
    "actual-payload-manifest-drift",
    "post-actual-gate-execution-receipt-drift",
    "post-actual-gate-PASS-drift",
    "seed1-identical-bytes-new-inode",
    "seed2-edge-drift",
    "frozen-C15-drift",
    "core-transaction-receipt-coherent-reclosure",
    "core-pinset-actual-pin-lie",
    "producer-command-spec-lie",
    "verifier-command-spec-seed-and-pin-lie",
    "attack-command-spec-lie",
    "candidate-result-census-coherent-reclosure",
    "candidate-truncated-gzip",
    "candidate-missing-member",
    "candidate-extra-member",
    "candidate-symlink",
    "candidate-hardlink",
    "independent-verification-coherent-reclosure",
    "core-attacks-coherent-reclosure",
    "producer-nonzero-exit",
    "verifier-signal",
    "attack-nonempty-stderr",
    "process-input-post-drift",
    "process-output-validation-drift",
    "cold-historical-verification-drift",
    "cold-receipt-coherent-reclosure",
    "evidence-inventory-member-drift",
    "wrong-PYTHONHASHSEED",
    "missing-isolated-python-flag",
    "atomic-replace-same-bytes-new-inode",
    "post-hash-content-TOCTOU",
    "payload-manifest-reorder",
    "manifest-duplicate",
    "manifest-traversal",
    "root-member-substitution",
    "outer-fake-release-count-coherent-reclosure",
    "future-seal-fake-authority",
    "terminal-byte-mismatch",
    "core-PASS-drift",
    "core-control-extra-member",
    "core-control-runner-stdout-drift",
    "gate-extra-member",
    "gate-stage-stdout-drift",
    "producer-run-extra-member",
    "producer-run-PASS-drift",
    "producer-run-stdout-drift",
    "producer-run-timing-drift",
    "producer-run-runner-start-drift",
    "cold-control-PASS-drift",
    "cold-control-runner-stdout-drift",
    "cold-run-extra-member",
    "cold-run-PASS-drift",
    "cold-run-stdout-drift",
    "cold-run-timing-drift",
    "cold-run-runner-start-drift",
    "producer-command-spec-extra-argv",
    "core-spec-extra-input",
    "cold-spec-extra-input",
    "attestation-extra-path",
    "attestation-omitted-path",
    "service-query-missing-bus-route",
    "service-query-wrong-bus-route",
]
VALIDATOR_NEGATIVE_INVENTORY_SHA256 = (
    "12a18411f62ba091fad7a28af44fe6a2eea1e4befe211c0f58d16a30a1a434b8"
)
PUBLICATION_LOCK_PREFLIGHT_INVENTORY_SHA256 = (
    "92add6db3116e10fe54cda24ce5d61288bb47622e6956f1353898ba707811c5d"
)


class Rejected(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def valid_sha(value: Any) -> bool:
    return type(value) is str and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def flip(value: str) -> str:
    need(valid_sha(value), "flippable SHA")
    return ("1" if value[0] != "1" else "0") + value[1:]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace(
        "+00:00", "Z")


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns,
            value.st_uid, value.st_gid)


def capture_file(path: Path, maximum: int = 16 << 30) \
        -> tuple[bytes, dict[str, Any]]:
    path = path.absolute()
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                         | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1
             and 0 <= before.st_size <= maximum,
             "authoritative singleton regular file")
        state = hashlib.sha256()
        chunks: list[bytes] = []
        while block := os.read(descriptor, 4 << 20):
            state.update(block)
            chunks.append(block)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    current = os.stat(path, follow_symlinks=False)
    need(fingerprint(before) == fingerprint(after) == fingerprint(current),
         "authoritative current full9stat")
    payload = b"".join(chunks)
    need(len(payload) == before.st_size, "captured exact file length")
    return payload, {"sha256": state.hexdigest(), "size": before.st_size,
                     "stat_fingerprint": list(fingerprint(before))}


def file_record(path: Path) -> dict[str, Any]:
    return capture_file(path)[1]


def strict_document(path: Path, closure: str) -> dict[str, Any]:
    payload = capture_file(path, 1 << 30)[0]
    need(payload.endswith(b"\n") and not payload.endswith(b"\n\n"),
         "canonical document newline")
    value = json.loads(payload[:-1])
    need(type(value) is dict and canonical(value) == payload[:-1],
         "canonical JSON")
    body = dict(value)
    claim = body.pop(closure, None)
    need(valid_sha(claim) and claim == digest(body), "object closure")
    return value


def strict_canonical_document(path: Path) -> dict[str, Any]:
    payload = capture_file(path, 1 << 30)[0]
    need(payload.endswith(b"\n") and not payload.endswith(b"\n\n"),
         "canonical document newline")
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(type(key) is str and key not in result,
                 "canonical document duplicate key")
            result[key] = value
        return result
    value = json.loads(payload[:-1], object_pairs_hook=pairs,
        parse_constant=lambda token: (_ for _ in ()).throw(
            Rejected("non-finite JSON:" + token)))
    need(type(value) is dict and canonical(value) == payload[:-1],
         "canonical exact document")
    return value


def validate_case_input_documents(process_dir: Path,
                                  request: dict[str, Any],
                                  request_record: dict[str, Any],
                                  command: list[str],
                                  environment_value: dict[str, str],
                                  case: str, ordinal: int) \
        -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    input_pre = strict_canonical_document(process_dir / "input_pre.json")
    input_post = strict_canonical_document(process_dir / "input_post.json")
    runner_start = strict_canonical_document(process_dir / "runner_start.json")
    input_keys = {"schema", "phase", "case", "ordinal",
        "request_file_sha256", "request_object_sha256", "wrapper_request",
        "snapshot", "validator_command", "validator_environment",
        "formal_credit"}
    need(set(input_pre) == set(input_post) == input_keys
         and input_pre["phase"] == "pre" and input_post["phase"] == "post"
         and input_pre["schema"] == input_post["schema"]
             == CASE_RUN_SCHEMA + ".input.v1"
         and input_pre["case"] == input_post["case"] == case
         and input_pre["ordinal"] == input_post["ordinal"] == ordinal
         and input_pre["request_file_sha256"]
             == input_post["request_file_sha256"] == request_record["sha256"]
         and input_pre["request_object_sha256"]
             == input_post["request_object_sha256"]
             == request["request_sha256"]
         and input_pre["wrapper_request"]
             == input_post["wrapper_request"] == request
         and input_pre["validator_command"]
             == input_post["validator_command"] == command
         and input_pre["validator_environment"]
             == input_post["validator_environment"] == environment_value
         and input_pre["formal_credit"] == input_post["formal_credit"] == 0
         and input_pre["snapshot"] == input_post["snapshot"]
         and type(input_pre["snapshot"]) is dict
         and valid_sha(input_pre["snapshot"].get("snapshot_sha256"))
         and runner_start == {"schema": CASE_RUN_SCHEMA + ".start.v1",
             "mode": "formal", "case": case, "ordinal": ordinal,
             "started_at_utc": runner_start["started_at_utc"],
             "exact_argv": command, "exact_environment": environment_value,
             "wrapper_pid": runner_start["wrapper_pid"], "formal_credit": 0},
         "outer runner exact request/argv/env/input pre-post rebinding")
    return input_pre, input_post, runner_start


def write_once(path: Path, payload: bytes, mode: int = 0o400) -> None:
    path = path.absolute()
    need(path.parent.is_dir() and not path.parent.is_symlink()
         and not path.exists() and not path.is_symlink(), "fresh write path")
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                         | getattr(os, "O_CLOEXEC", 0)
                         | getattr(os, "O_NOFOLLOW", 0), mode)
    try:
        view = memoryview(payload)
        offset = 0
        while offset < len(view):
            written = os.write(descriptor, view[offset:])
            need(type(written) is int and written > 0,
                 "write-all made positive progress")
            offset += written
        need(offset == len(payload), "write-all exact payload length")
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    reopened_payload, reopened = capture_file(path, max(1, len(payload)))
    need(reopened_payload == payload
         and reopened["sha256"] == hashlib.sha256(payload).hexdigest()
         and reopened["size"] == len(payload),
         "reopened output exact bytes/current SHA/full9stat")
    parent_descriptor = os.open(path.parent, os.O_RDONLY
                                | getattr(os, "O_DIRECTORY", 0)
                                | getattr(os, "O_CLOEXEC", 0)
                                | getattr(os, "O_NOFOLLOW", 0))
    try:
        os.fsync(parent_descriptor)
    finally:
        os.close(parent_descriptor)


def closed_map(mode: str, entries: list[dict[str, str]]) -> dict[str, Any]:
    body = {"schema": OVERRIDE_SCHEMA, "mode": mode, "entries": entries,
            "formal_credit": 0, "manifest_authorized": False,
            "C27R2": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM"}
    result = dict(body)
    result["override_map_sha256"] = digest(body)
    return result


def copy_ordinary(source: Path, target: Path) -> None:
    if source.is_dir():
        shutil.copytree(source, target, copy_function=shutil.copyfile,
                        symlinks=False)
        for path in target.rglob("*"):
            if path.is_file():
                path.chmod(0o600)
    else:
        shutil.copyfile(source, target)
        target.chmod(0o600)


def remove_private(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink(missing_ok=True)
    elif path.exists():
        shutil.rmtree(path)


def reclose_json(path: Path, closure: str,
                 mutate: Callable[[dict[str, Any]], None]) -> None:
    value = json.loads(path.read_bytes())
    need(type(value) is dict and closure in value, "reclosable JSON")
    value.pop(closure)
    mutate(value)
    value[closure] = digest(value)
    path.write_bytes(canonical(value) + b"\n")


def plain_json_mutate(path: Path,
                      mutate: Callable[[dict[str, Any]], None]) -> None:
    value = json.loads(path.read_bytes())
    need(type(value) is dict, "plain JSON object")
    mutate(value)
    path.write_bytes(canonical(value) + b"\n")


def authoritative_roots(args: argparse.Namespace) -> list[Path]:
    names = [
        "actual_terminal_relative", "actual_base_relative", "gate_relative",
        "seed1_edge_relative", "seed2_edge_relative", "frozen_c15_relative",
        "core_control_relative", "candidate_relative", "verifier_output_relative",
        "attack_work_relative", "producer_run_relative", "verifier_run_relative",
        "attack_run_relative", "cold_control_relative", "cold_output_relative",
        "cold_run_relative", "evidence_relative",
        "cold_helper_relative", "evidence_builder_relative",
    ]
    result = [(ROOT / getattr(args, name)).absolute() for name in names]
    result.extend((ROOT / name).absolute() for name in
                  CORE_SOURCE_RELATIVES + GATE_SOURCE_RELATIVES)
    result.extend([Path(args.validator).absolute(), SELF,
                   Path(args.python).absolute(),
                   Path(args.case_wrapper).absolute(),
                   Path(args.publication_lock_path).absolute()])
    return result


def absence_sentinels(targets: list[Path], parent: Path) \
        -> dict[str, dict[str, Any]]:
    """Capture exact nonexistence plus a stable full9stat parent sentinel."""
    parent = parent.absolute()
    need(parent.is_dir() and not parent.is_symlink(),
         "absence sentinel real parent")
    result: dict[str, dict[str, Any]] = {}
    for raw in targets:
        target = raw.absolute()
        need(target.parent == parent and target.name not in {"", ".", ".."},
             "absence sentinel direct parent/canonical target")
        before = os.stat(parent, follow_symlinks=False)
        try:
            os.stat(target, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            raise Rejected("future authority absence sentinel exists:" + str(target))
        after = os.stat(parent, follow_symlinks=False)
        need(fingerprint(before) == fingerprint(after),
             "absence sentinel stable parent full9stat")
        key = str(target)
        need(key not in result, "unique absence sentinel target")
        result[key] = {
            "path": key, "exists": False, "symlink": False,
            "parent_path": str(parent),
            "parent_stat_fingerprint": list(fingerprint(before)),
        }
    need(len(result) == len(targets), "exact absence sentinel count")
    return result


def future_absence_snapshot(args: argparse.Namespace) \
        -> dict[str, dict[str, Any]]:
    targets = [
        (ROOT / args.future_outer_relative).absolute(),
        (ROOT / args.future_seal_relative).absolute(),
        (ROOT / args.future_terminal_relative).absolute(),
    ]
    need(all(target.parent == AUDIT for target in targets),
         "future authorities are direct audit siblings")
    return absence_sentinels(targets, AUDIT)


def service_query_environment(fixture: str) -> dict[str, str]:
    need(fixture in {"fixed", "missing", "wrong"},
         "service query fixture mode")
    result = dict(CONTROL_BUS_ENV)
    if fixture == "missing":
        result.pop("XDG_RUNTIME_DIR")
        result.pop("DBUS_SESSION_BUS_ADDRESS")
    elif fixture == "wrong":
        result["XDG_RUNTIME_DIR"] = "/run/user/1000/c27r2-missing-runtime"
        result["DBUS_SESSION_BUS_ADDRESS"] = (
            "unix:path=/run/user/1000/c27r2-missing-bus")
    return result


def service_bus_stat() -> list[int]:
    need(os.getuid() == os.geteuid() == SERVICE_UID
         and SERVICE_RUNTIME.is_dir() and not SERVICE_RUNTIME.is_symlink(),
         "exact user-bus UID/runtime path")
    runtime = os.stat(SERVICE_RUNTIME, follow_symlinks=False)
    socket = os.stat(SERVICE_BUS, follow_symlinks=False)
    need(stat.S_ISDIR(runtime.st_mode) and runtime.st_uid == SERVICE_UID
         and stat.S_ISSOCK(socket.st_mode) and socket.st_uid == SERVICE_UID
         and socket.st_nlink == 1,
         "exact owned runtime directory and singleton Unix bus socket")
    return list(fingerprint(socket))


def parse_service_properties(payload: bytes) -> dict[str, str]:
    lines = payload.decode("ascii").splitlines()
    pairs = [line.split("=", 1) for line in lines if "=" in line]
    need(len(lines) == len(pairs) == len(SERVICE_FIELDS)
         and len({pair[0] for pair in pairs}) == len(SERVICE_FIELDS)
         and {pair[0] for pair in pairs} == set(SERVICE_FIELDS),
         "service snapshot exact ten-key first-equals parse")
    return dict(pairs)


def service_snapshot(args: argparse.Namespace) -> dict[str, Any]:
    need(type(args.core_unit) is str and args.core_unit.endswith(".service")
         and re.fullmatch(r"[0-9a-f]{32}", args.core_invocation_id) is not None,
         "service unit/invocation syntax")
    need(file_record(SYSTEMCTL)["sha256"] == SYSTEMCTL_SHA256,
         "exact current systemctl binary pin")
    socket_before = service_bus_stat()
    command = [str(SYSTEMCTL), "--user", "show", args.core_unit]
    for field in SERVICE_FIELDS:
        command.extend(["-p", field])
    completed = subprocess.run(command, cwd=ROOT, env=CONTROL_BUS_ENV,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=30)
    socket_after = service_bus_stat()
    need(socket_before == socket_after,
         "user bus socket full9stat unchanged across query")
    need(completed.returncode == 0 and completed.stderr == b"",
         "service snapshot clean query")
    fields = parse_service_properties(completed.stdout)
    need(fields["Id"] == args.core_unit
         and fields["Result"] == "success"
         and fields["ExecMainCode"] == "1"
         and fields["ExecMainStatus"] == "0"
         and fields["LoadState"] == "loaded"
         and fields["ActiveState"] == "active"
         and fields["SubState"] == "exited"
         and fields["InvocationID"] == args.core_invocation_id
         and fields["ExecStart"] != "",
         "service snapshot exact current clean tuple")
    exec_line = ("ExecStart=" + fields["ExecStart"] + "\n").encode("ascii")
    need(valid_sha(args.core_exec_start_property_sha256)
         and hashlib.sha256(exec_line).hexdigest()
             == args.core_exec_start_property_sha256,
         "service ExecStart raw property SHA current")
    fragment_path = Path(args.core_fragment_path).absolute()
    need(str(fragment_path) == args.core_fragment_path
         and fragment_path.parent == SERVICE_TRANSIENT
         and fragment_path.name == args.core_unit
         and SERVICE_TRANSIENT.is_dir()
         and not SERVICE_TRANSIENT.is_symlink()
         and fields["FragmentPath"] == args.core_fragment_path,
         "service exact real transient FragmentPath")
    _, fragment_record = capture_file(fragment_path, 16 << 20)
    expected_stat = json.loads(args.core_fragment_stat9_json)
    need(type(expected_stat) is list and len(expected_stat) == 9
         and all(type(item) is int for item in expected_stat)
         and canonical(expected_stat).decode("ascii")
             == args.core_fragment_stat9_json
         and valid_sha(args.core_fragment_file_sha256)
         and fragment_record["sha256"] == args.core_fragment_file_sha256
         and fragment_record["stat_fingerprint"] == expected_stat,
         "service FragmentPath singleton SHA/full9stat current")
    return {"properties": fields,
        "exec_start_property_sha256": args.core_exec_start_property_sha256,
        "fragment_file": {"path": args.core_fragment_path,
                          **fragment_record}}


def publication_lock_stat_argument(raw: str) -> list[int]:
    value = json.loads(raw)
    need(type(value) is list and len(value) == 9
         and all(type(item) is int for item in value)
         and canonical(value).decode("ascii") == raw,
         "canonical exact publication lock stat9 argument")
    return value


def validate_publication_lock(args: argparse.Namespace,
                              fixture: bool = False) -> dict[str, Any]:
    """Verify an inherited already-exclusive lock without acquiring a gap."""
    path = Path(args.publication_lock_path).absolute()
    if not fixture:
        need(path.parent.parent == AUDIT and path.name == "publication_lock.json"
             and path.parent.name.endswith("-control"),
             "publication lock in distinct one-shot launch-control directory")
    expected_stat = publication_lock_stat_argument(
        args.publication_lock_stat9_json)
    need(valid_sha(args.publication_lock_file_sha256)
         and valid_sha(args.publication_lock_object_sha256)
         and type(args.publication_lock_fd) is int
         and args.publication_lock_fd >= 3,
         "publication lock pins and inherited fd syntax")
    fd_stat = os.fstat(args.publication_lock_fd)
    need(stat.S_ISREG(fd_stat.st_mode) and fd_stat.st_nlink == 1
         and list(fingerprint(fd_stat)) == expected_stat,
         "publication inherited fd exact regular singleton stat9")
    payload, path_record = capture_file(path, 1 << 20)
    need(path_record["sha256"] == args.publication_lock_file_sha256
         and path_record["stat_fingerprint"] == expected_stat
         and (fd_stat.st_dev, fd_stat.st_ino) == tuple(expected_stat[:2]),
         "publication lock fd/path same inode and exact file/stat pins")
    need(payload.endswith(b"\n") and not payload.endswith(b"\n\n"),
         "publication lock canonical newline")
    value = json.loads(payload[:-1])
    need(type(value) is dict and canonical(value) == payload[:-1],
         "publication lock canonical JSON object")
    body = dict(value)
    object_sha = body.pop("publication_lock_sha256", None)
    need(valid_sha(object_sha) and object_sha == digest(body)
         and object_sha == args.publication_lock_object_sha256
         and set(value) == {"schema", "status", "protocol",
                            "one_shot_launch_id", "plan_file_sha256",
                            "plan_object_sha256", "formal_credit",
                            "manifest_authorized", "authority_minted",
                            "publication_lock_sha256"}
         and value.get("schema") == PUBLICATION_LOCK_SCHEMA
         and value.get("status") == PUBLICATION_LOCK_STATUS
         and value.get("protocol") == PUBLICATION_LOCK_PROTOCOL
         and type(value.get("one_shot_launch_id")) is str
         and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{7,127}",
                          value["one_shot_launch_id"]) is not None
         and valid_sha(value.get("plan_file_sha256"))
         and valid_sha(value.get("plan_object_sha256"))
         and value.get("formal_credit") == 0
         and value.get("manifest_authorized") is False
         and value.get("authority_minted") is False,
         "publication lock exact canonical object closure/policy")
    def probe_blocked(operation: int) -> bool:
        probe = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                        | getattr(os, "O_NOFOLLOW", 0))
        try:
            try:
                fcntl.flock(probe, operation | fcntl.LOCK_NB)
            except BlockingIOError:
                return True
            fcntl.flock(probe, fcntl.LOCK_UN)
            return False
        finally:
            os.close(probe)
    need(probe_blocked(fcntl.LOCK_EX) and probe_blocked(fcntl.LOCK_SH),
         "separate opens prove inherited publication fd already exclusive")
    fcntl.flock(args.publication_lock_fd,
                fcntl.LOCK_EX | fcntl.LOCK_NB)
    final_fd = os.fstat(args.publication_lock_fd)
    need(list(fingerprint(final_fd)) == expected_stat,
         "publication lock remains exclusive and current")
    return {
        "path": str(path), "file_sha256": path_record["sha256"],
        "object_sha256": object_sha, "stat_fingerprint": expected_stat,
        "fd": args.publication_lock_fd,
        "fd_stat_fingerprint": list(fingerprint(final_fd)),
        "inherited_fd": True, "path_fd_same_inode": True,
        "protocol": PUBLICATION_LOCK_PROTOCOL, "exclusive_held": True,
        "one_shot_launch_id": value["one_shot_launch_id"],
        "plan_file_sha256": value["plan_file_sha256"],
        "plan_object_sha256": value["plan_object_sha256"],
    }


def fixture_lock(path: Path, label: str) -> argparse.Namespace:
    body = {"schema": PUBLICATION_LOCK_SCHEMA,
        "status": PUBLICATION_LOCK_STATUS,
        "protocol": PUBLICATION_LOCK_PROTOCOL,
        "one_shot_launch_id": "fixture-" + label + "-control",
        "plan_file_sha256": hashlib.sha256(("file:" + label).encode()).hexdigest(),
        "plan_object_sha256": hashlib.sha256(("object:" + label).encode()).hexdigest(),
        "formal_credit": 0, "manifest_authorized": False,
        "authority_minted": False}
    value = dict(body)
    value["publication_lock_sha256"] = digest(body)
    write_once(path, canonical(value) + b"\n", 0o400)
    record = file_record(path)
    return argparse.Namespace(
        publication_lock_path=str(path),
        publication_lock_file_sha256=record["sha256"],
        publication_lock_object_sha256=value["publication_lock_sha256"],
        publication_lock_stat9_json=canonical(
            record["stat_fingerprint"]).decode("ascii"),
        publication_lock_fd=-1)


def expect_lock_rejection(action: Callable[[], Any], label: str) -> None:
    try:
        action()
    except (Rejected, OSError, ValueError, KeyError, TypeError,
            AttributeError):
        return
    raise Rejected("lock preflight unexpectedly accepted:" + label)


def execute_lock_preflight_case(args: argparse.Namespace) -> None:
    name = args.lock_preflight_case
    need(name in LOCK_PREFLIGHT_CASE_NAMES,
         "exact publication lock preflight case name")
    expected_env = {"PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
                    "PYTHONHASHSEED": args.expected_python_hash_seed}
    need(dict(os.environ) == expected_env
         and file_record(SELF)["sha256"] == args.expect_runner_sha256,
         "lock preflight runner current pin/minimal environment")
    root = Path(args.lock_preflight_work_dir).absolute()
    need(not root.exists() and not root.is_symlink(),
         "fresh lock preflight private root")
    root.mkdir(mode=0o700)
    descriptors: list[int] = []
    checks = 0
    try:
        if name == "missing-lock-arguments":
            expect_lock_rejection(
                lambda: validate_publication_lock(argparse.Namespace(), True),
                name)
            checks = 1
        elif name == "bad-inherited-fd":
            contract = fixture_lock(root / "lock.json", name)
            contract.publication_lock_fd = 999_999
            expect_lock_rejection(
                lambda: validate_publication_lock(contract, True), name)
            checks = 1
        elif name == "wrong-inode-path-substitution":
            first = fixture_lock(root / "first.json", name + "-first")
            second = fixture_lock(root / "second.json", name + "-second")
            descriptor = os.open(first.publication_lock_path, os.O_RDONLY
                | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
            descriptors.append(descriptor)
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
            first.publication_lock_path = second.publication_lock_path
            first.publication_lock_fd = descriptor
            expect_lock_rejection(
                lambda: validate_publication_lock(first, True), name)
            checks = 1
        elif name == "unlocked-inherited-fd":
            contract = fixture_lock(root / "lock.json", name)
            descriptor = os.open(contract.publication_lock_path, os.O_RDONLY
                | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
            descriptors.append(descriptor)
            contract.publication_lock_fd = descriptor
            expect_lock_rejection(
                lambda: validate_publication_lock(contract, True), name)
            checks = 1
        elif name == "shared-only-inherited-lock":
            contract = fixture_lock(root / "lock.json", name)
            descriptor = os.open(contract.publication_lock_path, os.O_RDONLY
                | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
            descriptors.append(descriptor)
            fcntl.flock(descriptor, fcntl.LOCK_SH | fcntl.LOCK_NB)
            contract.publication_lock_fd = descriptor
            expect_lock_rejection(
                lambda: validate_publication_lock(contract, True), name)
            checks = 1
        elif name == "symlink-or-nonsingleton-lock-path":
            contract = fixture_lock(root / "source.json", name)
            descriptor = os.open(contract.publication_lock_path, os.O_RDONLY
                | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
            descriptors.append(descriptor)
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
            contract.publication_lock_fd = descriptor
            symlink = root / "symlink.json"
            symlink.symlink_to(Path(contract.publication_lock_path))
            original = contract.publication_lock_path
            contract.publication_lock_path = str(symlink)
            expect_lock_rejection(
                lambda: validate_publication_lock(contract, True), name + ":symlink")
            contract.publication_lock_path = original
            os.link(original, root / "hardlink.json")
            expect_lock_rejection(
                lambda: validate_publication_lock(contract, True), name + ":nlink")
            checks = 2
        elif name == "lock-pin-or-stat-drift":
            contract = fixture_lock(root / "lock.json", name)
            descriptor = os.open(contract.publication_lock_path, os.O_RDONLY
                | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
            descriptors.append(descriptor)
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
            contract.publication_lock_fd = descriptor
            bad_pin = argparse.Namespace(**vars(contract))
            bad_pin.publication_lock_file_sha256 = flip(
                contract.publication_lock_file_sha256)
            expect_lock_rejection(
                lambda: validate_publication_lock(bad_pin, True), name + ":pin")
            stat9 = publication_lock_stat_argument(
                contract.publication_lock_stat9_json)
            stat9[1] += 1
            bad_stat = argparse.Namespace(**vars(contract))
            bad_stat.publication_lock_stat9_json = canonical(stat9).decode("ascii")
            expect_lock_rejection(
                lambda: validate_publication_lock(bad_stat, True), name + ":stat")
            checks = 2
        else:
            contract = fixture_lock(root / "lock.json", name)
            descriptor = os.open(contract.publication_lock_path, os.O_RDONLY
                | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
            contract.publication_lock_fd = descriptor
            fcntl.flock(descriptor, fcntl.LOCK_UN)
            expect_lock_rejection(
                lambda: validate_publication_lock(contract, True), name + ":unlock")
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
            os.close(descriptor)
            contract.publication_lock_fd = descriptor
            expect_lock_rejection(
                lambda: validate_publication_lock(contract, True), name + ":close")
            checks = 2
        need(checks in {1, 2}, "lock preflight executed injected check(s)")
    finally:
        for descriptor in descriptors:
            try:
                fcntl.flock(descriptor, fcntl.LOCK_UN)
                os.close(descriptor)
            except OSError:
                pass
        remove_private(root)
    need(not root.exists() and not root.is_symlink(),
         "lock preflight private root cleaned")
    raise Rejected("EXPECTED_PUBLICATION_LOCK_PREFLIGHT_REJECTION:" + name)


def authority_key(path: Path) -> str:
    try:
        return str(path.absolute().relative_to(ROOT))
    except ValueError:
        return "external:" + str(path.absolute())


def snapshot_authority_node(path: Path,
                            result: dict[str, Any]) -> None:
    """Recursively close every directory and file, including empty dirs."""
    path = path.absolute()
    initial = os.stat(path, follow_symlinks=False)
    need(not stat.S_ISLNK(initial.st_mode), "no authority symlink")
    key = authority_key(path)
    need(key not in result, "disjoint authority path inventory")
    if stat.S_ISREG(initial.st_mode):
        record = file_record(path)
        need(record["stat_fingerprint"] == list(fingerprint(initial)),
             "authority file initial/current full9stat")
        result[key] = {"node_type": "regular", **record}
        return
    need(stat.S_ISDIR(initial.st_mode),
         "authority node is regular file or directory")
    with os.scandir(path) as stream:
        entries = sorted(list(stream), key=lambda item: item.name)
    inventory: list[dict[str, str]] = []
    for entry in entries:
        child_stat = entry.stat(follow_symlinks=False)
        need(not stat.S_ISLNK(child_stat.st_mode),
             "no symlink in authority directory tree")
        if stat.S_ISDIR(child_stat.st_mode):
            kind = "directory"
        elif stat.S_ISREG(child_stat.st_mode):
            kind = "regular"
        else:
            raise Rejected("unexpected authority node type:" + entry.path)
        inventory.append({"name": entry.name, "node_type": kind})
        snapshot_authority_node(Path(entry.path), result)
    final = os.stat(path, follow_symlinks=False)
    need(fingerprint(initial) == fingerprint(final),
         "authority directory full9stat stable across exact inventory scan")
    result[key] = {
        "node_type": "directory",
        "stat_fingerprint": list(fingerprint(initial)),
        "entry_count": len(inventory),
        "entries": inventory,
        "entry_inventory_sha256": digest(inventory),
    }


def authority_snapshot(args: argparse.Namespace) -> dict[str, Any]:
    nodes: dict[str, Any] = {}
    for root in authoritative_roots(args):
        need(root.exists() and not root.is_symlink(), "authority root exists")
        snapshot_authority_node(root, nodes)
    absence = future_absence_snapshot(args)
    result = {"authority_nodes": nodes,
              "core_service": service_snapshot(args),
              "future_absence": absence,
              "authority_node_count": len(nodes),
              "future_absence_count": len(absence)}
    result["snapshot_sha256"] = digest(result)
    return result


def current_source_pins(args: argparse.Namespace) -> dict[str, dict[str, Any]]:
    paths = {
        **{f"core_source_{index:02d}": (ROOT / relative).absolute()
           for index, relative in enumerate(CORE_SOURCE_RELATIVES)},
        **{f"gate_source_{index:02d}": (ROOT / relative).absolute()
           for index, relative in enumerate(GATE_SOURCE_RELATIVES)},
        "cold_helper": (ROOT / args.cold_helper_relative).absolute(),
        "evidence_builder": (ROOT / args.evidence_builder_relative).absolute(),
        "validator": Path(args.validator).absolute(),
        "runner": SELF,
        "case_wrapper": Path(args.case_wrapper).absolute(),
        "python": Path(args.python).absolute(),
    }
    return {name: {"path": str(path), "sha256": file_record(path)["sha256"]}
            for name, path in sorted(paths.items())}


VALIDATOR_COMMON = [
    "python", "expect_python_sha256", "expect_validator_sha256",
    "expected_python_hash_seed", "actual_terminal_relative",
    "actual_base_relative", "expect_actual_terminal_root_sha256",
    "expect_actual_terminal_receipt_file_sha256",
    "expect_actual_terminal_receipt_object_sha256", "seed1_edge_relative",
    "expect_seed1_edge_sha256", "seed2_edge_relative",
    "expect_seed2_edge_sha256", "frozen_c15_relative",
    "expect_frozen_c15_sha256", "gate_relative",
    "expect_gate_receipt_file_sha256", "expect_gate_receipt_object_sha256",
    "expect_gate_root_file_sha256", "expect_gate_root_object_sha256",
    "core_control_relative", "candidate_relative", "verifier_output_relative",
    "attack_work_relative", "producer_run_relative", "verifier_run_relative",
    "attack_run_relative", "expect_core_receipt_file_sha256",
    "expect_core_receipt_object_sha256", "core_unit", "core_invocation_id",
    "core_exec_start_property_sha256", "core_fragment_path",
    "core_fragment_file_sha256", "core_fragment_stat9_json",
    "service_query_fixture",
    "cold_control_relative", "cold_output_relative", "cold_run_relative",
    "expect_cold_receipt_file_sha256", "expect_cold_receipt_object_sha256",
    "cold_helper_relative", "expect_cold_helper_sha256",
    "cold_python_hash_seed", "evidence_relative", "evidence_builder_relative",
    "expect_evidence_builder_sha256", "expect_evidence_file_sha256",
    "expect_evidence_object_sha256",
    "future_outer_relative", "future_seal_relative", "future_terminal_relative",
]


def validator_command(args: argparse.Namespace, mode: str, override_map: Path,
                      case_root: Path | None, out_file: Path,
                      changes: dict[str, str] | None = None,
                      missing_isolated: bool = False,
                      barrier: bool = False) -> list[str]:
    changes = changes or {}
    command = [args.python]
    if not missing_isolated:
        command.append("-I")
    command.extend(["-B", args.validator, "--mode", mode,
                    "--override-map", str(override_map),
                    "--expect-override-map-file-sha256",
                    file_record(override_map)["sha256"],
                    "--expect-override-map-object-sha256",
                    strict_document(override_map, "override_map_sha256")
                        ["override_map_sha256"]])
    if case_root is not None:
        command.extend(["--case-root", str(case_root)])
    if barrier:
        command.append("--fixture-barrier")
    for name in VALIDATOR_COMMON:
        value = changes.get(name, str(getattr(args, name)))
        command.extend(["--" + name.replace("_", "-"), value])
    command.extend(["--out-file", str(out_file)])
    return command


def invoke(command: list[str], environment: dict[str, str], timeout: int) \
        -> dict[str, Any]:
    started = time.monotonic()
    with tempfile.TemporaryFile() as stdout_stream, \
            tempfile.TemporaryFile() as stderr_stream:
        try:
            completed = subprocess.run(command, cwd=ROOT, env=environment,
                stdin=subprocess.DEVNULL, stdout=stdout_stream,
                stderr=stderr_stream, check=False, timeout=timeout)
            timed_out = False
            code = completed.returncode
        except subprocess.TimeoutExpired:
            timed_out = True
            code = None
        stdout_stream.seek(0, os.SEEK_END)
        stdout_size = stdout_stream.tell()
        stderr_stream.seek(0, os.SEEK_END)
        stderr_size = stderr_stream.tell()
        stdout_stream.seek(0)
        stderr_stream.seek(0)
        stdout = stdout_stream.read(MAX_CAPTURE_BYTES + 1)
        stderr = stderr_stream.read(MAX_CAPTURE_BYTES + 1)
    return {"numeric_exit_code": code if code is not None and code >= 0 else None,
            "signal": -code if code is not None and code < 0 else None,
            "timed_out": timed_out,
            "elapsed_seconds": round(time.monotonic() - started, 6),
            "stdout": stdout, "stderr": stderr,
            "stdout_size": stdout_size, "stderr_size": stderr_size,
            "capture_bounded": (stdout_size <= MAX_CAPTURE_BYTES
                                and stderr_size <= MAX_CAPTURE_BYTES)}


def authority_projection(snapshot: dict[str, Any]) -> str:
    body = dict(snapshot)
    claim = body.pop("snapshot_sha256", None)
    need(valid_sha(claim) and claim == digest(body),
         "authority snapshot object closure")
    return claim


def relative_workspace(path: Path) -> str:
    try:
        relative = path.absolute().relative_to(ROOT)
    except ValueError as error:
        raise Rejected("path outside workspace:" + str(path)) from error
    need(relative.parts and all(part not in {"", ".", ".."}
                                for part in relative.parts),
         "canonical workspace-relative path")
    return str(relative)


def targets(args: argparse.Namespace) -> dict[str, str]:
    def child(base: str, name: str) -> str:
        return str(Path(getattr(args, base)) / name)
    benign = child("core_control_relative", "transaction_receipt.json")
    return {
        "benign": benign,
        "terminal_pass": child("actual_terminal_relative", "PASS.lock"),
        "terminal_payload": child("actual_terminal_relative", "payload_manifest.sha256"),
        "terminal_root": child("actual_terminal_relative", "root_manifest.sha256"),
        "gate_execution": child("gate_relative", "execution_receipt.json"),
        "gate_pass": child("gate_relative", "PASS.lock"),
        "seed1": args.seed1_edge_relative,
        "seed2": args.seed2_edge_relative,
        "c15": args.frozen_c15_relative,
        "core_receipt": benign,
        "pinset": child("core_control_relative", "pinset.json"),
        "producer_spec": child("core_control_relative", "producer_command_spec.json"),
        "verifier_spec": child("core_control_relative", "verifier_command_spec.json"),
        "attack_spec": child("core_control_relative", "attack_command_spec.json"),
        "result": child("candidate_relative", "result.json"),
        "member_gzip": child("candidate_relative", "member_to_post_component.jsonl.gz"),
        "candidate": args.candidate_relative,
        "verification": child("verifier_output_relative", "verification.json"),
        "attacks": child("attack_work_relative", "coherent_attacks.json"),
        "producer_exit": child("producer_run_relative", "exit_code.txt"),
        "verifier_signal": child("verifier_run_relative", "signal.json"),
        "attack_stderr": child("attack_run_relative", "stderr.log"),
        "input_post": child("producer_run_relative", "input_post.json"),
        "output_validation": child("producer_run_relative", "output_validation.json"),
        "cold_verification": child("cold_output_relative", "verification.json"),
        "cold_receipt": child("cold_control_relative", "cold_replay_receipt.json"),
        "evidence_inventory": child("evidence_relative", "core_inventory.sha256"),
        "base_payload": child("actual_base_relative", "payload_manifest.sha256"),
        "core_pass": child("core_control_relative", "PASS.lock"),
        "core_control": args.core_control_relative,
        "core_runner_stdout": child("core_control_relative",
                                    "producer_runner.stdout.log"),
        "gate": args.gate_relative,
        "gate_stdout": child("gate_relative", "producer.stdout.log"),
        "producer_run": args.producer_run_relative,
        "producer_run_pass": child("producer_run_relative", "PASS.lock"),
        "producer_run_stdout": child("producer_run_relative", "stdout.log"),
        "producer_run_timing": child("producer_run_relative", "timing.json"),
        "producer_run_start": child("producer_run_relative", "runner_start.json"),
        "cold_pass": child("cold_control_relative", "PASS.lock"),
        "cold_runner_stdout": child("cold_control_relative", "runner.stdout.log"),
        "cold_run": args.cold_run_relative,
        "cold_run_pass": child("cold_run_relative", "PASS.lock"),
        "cold_run_stdout": child("cold_run_relative", "stdout.log"),
        "cold_run_timing": child("cold_run_relative", "timing.json"),
        "cold_run_start": child("cold_run_relative", "runner_start.json"),
        "cold_spec": child("cold_control_relative", "cold_command_spec.json"),
        "producer_attestation": child("producer_run_relative",
                                      "run_attestation.json"),
        "outer": args.future_outer_relative,
        "seal": args.future_seal_relative,
        "terminal": args.future_terminal_relative,
    }


def case_specs(args: argparse.Namespace) -> list[dict[str, Any]]:
    target = targets(args)
    specs = [
        ("wrong-core-unit", "benign", "copy", {"core_unit": "cm2-c27r2-wrong.service"}),
        ("wrong-core-invocation", "benign", "copy", {"core_invocation_id": "0" * 32}),
        ("actual-terminal-directory-swap", "benign", "copy",
            {"actual_terminal_relative": args.actual_base_relative}),
        ("actual-base-directory-swap", "benign", "copy",
            {"actual_base_relative": args.actual_terminal_relative}),
        ("actual-terminal-receipt-file-pin", "benign", "copy",
            {"expect_actual_terminal_receipt_file_sha256":
                flip(args.expect_actual_terminal_receipt_file_sha256)}),
        ("actual-terminal-receipt-object-pin", "benign", "copy",
            {"expect_actual_terminal_receipt_object_sha256":
                flip(args.expect_actual_terminal_receipt_object_sha256)}),
        ("actual-terminal-root-pin", "benign", "copy",
            {"expect_actual_terminal_root_sha256":
                flip(args.expect_actual_terminal_root_sha256)}),
        ("actual-terminal-PASS-drift", "terminal_pass", "append", {}),
        ("actual-payload-manifest-drift", "terminal_payload", "append", {}),
        ("post-actual-gate-execution-receipt-drift", "gate_execution",
            "reclose-gate-root", {}),
        ("post-actual-gate-PASS-drift", "gate_pass", "append", {}),
        ("seed1-identical-bytes-new-inode", "seed1", "copy", {}),
        ("seed2-edge-drift", "seed2", "truncate", {}),
        ("frozen-C15-drift", "c15", "truncate", {}),
        ("core-transaction-receipt-coherent-reclosure", "core_receipt",
            "reclose-core", {}),
        ("core-pinset-actual-pin-lie", "pinset", "reclose-pinset", {}),
        ("producer-command-spec-lie", "producer_spec", "reclose-producer-spec", {}),
        ("verifier-command-spec-seed-and-pin-lie", "verifier_spec",
            "reclose-verifier-spec", {}),
        ("attack-command-spec-lie", "attack_spec", "reclose-attack-spec", {}),
        ("candidate-result-census-coherent-reclosure", "result",
            "reclose-result", {}),
        ("candidate-truncated-gzip", "member_gzip", "truncate", {}),
        ("candidate-missing-member", "candidate", "missing-candidate", {}),
        ("candidate-extra-member", "candidate", "extra-candidate", {}),
        ("candidate-symlink", "candidate", "symlink", {}),
        ("candidate-hardlink", "result", "hardlink", {}),
        ("independent-verification-coherent-reclosure", "verification",
            "reclose-verification", {}),
        ("core-attacks-coherent-reclosure", "attacks", "reclose-attacks", {}),
        ("producer-nonzero-exit", "producer_exit", "exit2", {}),
        ("verifier-signal", "verifier_signal", "signal9", {}),
        ("attack-nonempty-stderr", "attack_stderr", "append", {}),
        ("process-input-post-drift", "input_post", "plain-json-drift", {}),
        ("process-output-validation-drift", "output_validation",
            "plain-json-drift", {}),
        ("cold-historical-verification-drift", "cold_verification",
            "reclose-verification", {}),
        ("cold-receipt-coherent-reclosure", "cold_receipt",
            "reclose-cold", {}),
        ("evidence-inventory-member-drift", "evidence_inventory", "append", {}),
        ("wrong-PYTHONHASHSEED", "benign", "copy", {}),
        ("missing-isolated-python-flag", "benign", "copy", {}),
        ("atomic-replace-same-bytes-new-inode", "core_receipt", "atomic", {}),
        ("post-hash-content-TOCTOU", "core_receipt", "toctou", {}),
        ("payload-manifest-reorder", "base_payload", "manifest-reorder", {}),
        ("manifest-duplicate", "terminal_payload", "manifest-duplicate", {}),
        ("manifest-traversal", "terminal_payload", "manifest-traversal", {}),
        ("root-member-substitution", "terminal_root", "manifest-substitute", {}),
        ("outer-fake-release-count-coherent-reclosure", "outer", "fake-outer", {}),
        ("future-seal-fake-authority", "seal", "fake-seal", {}),
        ("terminal-byte-mismatch", "terminal", "fake-terminal", {}),
        ("core-PASS-drift", "core_pass", "append", {}),
        ("core-control-extra-member", "core_control", "extra-directory-member", {}),
        ("core-control-runner-stdout-drift", "core_runner_stdout", "append", {}),
        ("gate-extra-member", "gate", "extra-directory-member", {}),
        ("gate-stage-stdout-drift", "gate_stdout", "append", {}),
        ("producer-run-extra-member", "producer_run", "extra-directory-member", {}),
        ("producer-run-PASS-drift", "producer_run_pass", "append", {}),
        ("producer-run-stdout-drift", "producer_run_stdout", "append", {}),
        ("producer-run-timing-drift", "producer_run_timing", "plain-json-drift", {}),
        ("producer-run-runner-start-drift", "producer_run_start", "plain-json-drift", {}),
        ("cold-control-PASS-drift", "cold_pass", "append", {}),
        ("cold-control-runner-stdout-drift", "cold_runner_stdout", "append", {}),
        ("cold-run-extra-member", "cold_run", "extra-directory-member", {}),
        ("cold-run-PASS-drift", "cold_run_pass", "append", {}),
        ("cold-run-stdout-drift", "cold_run_stdout", "append", {}),
        ("cold-run-timing-drift", "cold_run_timing", "plain-json-drift", {}),
        ("cold-run-runner-start-drift", "cold_run_start", "plain-json-drift", {}),
        ("producer-command-spec-extra-argv", "producer_spec",
            "reclose-producer-extra-argv", {}),
        ("core-spec-extra-input", "producer_spec",
            "reclose-spec-extra-input", {}),
        ("cold-spec-extra-input", "cold_spec",
            "reclose-spec-extra-input", {}),
        ("attestation-extra-path", "producer_attestation",
            "reclose-attestation-extra-path", {}),
        ("attestation-omitted-path", "producer_attestation",
            "reclose-attestation-omitted-path", {}),
        ("service-query-missing-bus-route", "benign", "copy",
            {"service_query_fixture": "missing"}),
        ("service-query-wrong-bus-route", "benign", "copy",
            {"service_query_fixture": "wrong"}),
    ]
    need([row[0] for row in specs] == CASE_NAMES, "exact ordered 70 cases")
    need(digest({"validator_negative_case_count": len(CASE_NAMES),
                 "ordered_validator_negative_case_names": CASE_NAMES})
             == VALIDATOR_NEGATIVE_INVENTORY_SHA256,
         "frozen ordered 70 validator inventory digest")
    return [{"name": name, "logical": target[key], "mutation": mutation,
             "changes": changes} for name, key, mutation, changes in specs]


def prepare_override(spec: dict[str, Any], case_root: Path) -> dict[str, Any]:
    logical = spec["logical"]
    source = (ROOT / logical).absolute()
    target = case_root / "override"
    mutation = spec["mutation"]
    if mutation == "symlink":
        target.symlink_to(source)
    elif mutation == "hardlink":
        private_source = case_root / "private-hardlink-source"
        shutil.copyfile(source, private_source)
        os.link(private_source, target)
    elif mutation in {"fake-outer", "fake-seal", "fake-terminal"}:
        target.mkdir()
        if mutation == "fake-outer":
            body = {"schema": PREFIX + "fake-outer.v1", "released": 64,
                    "formal_credit": 0, "manifest_authorized": True,
                    "C27R2": "MINTED", "CM2": "NO-GO_FOR_CLAIM"}
            body["fake_outer_sha256"] = digest(body)
            (target / "outer_verification.json").write_bytes(canonical(body) + b"\n")
        elif mutation == "fake-seal":
            body = {"schema": PREFIX + "fake-seal.v1", "authority_minted": True,
                    "formal_credit": 0, "manifest_authorized": True,
                    "C27R2": "MINTED", "CM2": "NO-GO_FOR_CLAIM"}
            body["fake_seal_sha256"] = digest(body)
            (target / "seal_receipt.json").write_bytes(canonical(body) + b"\n")
        else:
            (target / "PASS.lock").write_bytes(
                b"PASS_C27R2_AUTHORITY_V2_TERMINAL_BYTE_REPLAY__MISMATCH\n")
    else:
        need(source.exists() and not source.is_symlink(), "fixture source exists")
        copy_ordinary(source, target)
        if mutation == "append":
            target.write_bytes(target.read_bytes() + b"FIXTURE\n")
        elif mutation == "truncate":
            size = target.stat().st_size
            with target.open("r+b") as stream:
                stream.truncate(max(1, size // 2))
        elif mutation == "reclose-gate-root":
            reclose_json(target, "execution_receipt_sha256",
                         lambda value: value.__setitem__("formal_credit", 1))
        elif mutation == "reclose-core":
            reclose_json(target, "transaction_receipt_sha256",
                         lambda value: value.__setitem__("C27R2", "MINTED"))
        elif mutation == "reclose-pinset":
            def change_pinset(value: dict[str, Any]) -> None:
                value["actual_v2_authority"]["actual_terminal_root_sha256"] = "0" * 64
            reclose_json(target, "pinset_sha256", change_pinset)
        elif mutation == "reclose-producer-spec":
            def change_producer(value: dict[str, Any]) -> None:
                value["environment"]["PYTHONHASHSEED"] = "1"
                value["python_hash_seed"] = "1"
            reclose_json(target, "command_spec_sha256", change_producer)
        elif mutation == "reclose-producer-extra-argv":
            reclose_json(target, "command_spec_sha256",
                lambda value: value["argv"].extend(["--unexpected", "fixture"]))
        elif mutation == "reclose-spec-extra-input":
            def add_spec_input(value: dict[str, Any]) -> None:
                paths = value.get("input_paths")
                need(type(paths) is list, "spec input paths list")
                extra = relative_workspace(SELF)
                need(extra not in paths, "spec fixture input is new")
                value["input_paths"] = sorted([*paths, extra])
            reclose_json(target, "command_spec_sha256", add_spec_input)
        elif mutation == "reclose-verifier-spec":
            def change_verifier(value: dict[str, Any]) -> None:
                value["source_sha256"] = "0" * 64
                value["environment"]["PYTHONHASHSEED"] = "1"
            reclose_json(target, "command_spec_sha256", change_verifier)
        elif mutation == "reclose-attack-spec":
            reclose_json(target, "command_spec_sha256",
                lambda value: value["argv"].__setitem__(1, "-E"))
        elif mutation == "reclose-result":
            def change_result(value: dict[str, Any]) -> None:
                value["exact_census"]["post_C27R2_components"] += 1
            reclose_json(target, "result_sha256", change_result)
        elif mutation == "missing-candidate":
            (target / "result.json").unlink()
        elif mutation == "extra-candidate":
            (target / "unexpected.extra").write_bytes(b"extra\n")
        elif mutation == "reclose-verification":
            reclose_json(target, "verification_sha256",
                lambda value: value.__setitem__("manifest_authorized", True))
        elif mutation == "reclose-attacks":
            reclose_json(target, "attack_harness_sha256",
                lambda value: value.__setitem__("accepted", 1))
        elif mutation == "exit2":
            target.write_bytes(b"2\n")
        elif mutation == "signal9":
            target.write_bytes(b"9\n")
        elif mutation == "plain-json-drift":
            plain_json_mutate(target,
                lambda value: value.__setitem__("__fixture_drift__", True))
        elif mutation == "reclose-cold":
            reclose_json(target, "cold_replay_receipt_sha256",
                lambda value: value.__setitem__("formal_verification_byte_identical", False))
        elif mutation in {"reclose-attestation-extra-path",
                          "reclose-attestation-omitted-path"}:
            def change_attestation(value: dict[str, Any]) -> None:
                inputs = value.get("input_attestations")
                need(type(inputs) is dict, "attestation input map")
                if mutation == "reclose-attestation-extra-path":
                    label = "declared-input-999"
                    need(label not in inputs, "attestation fixture label new")
                    inputs[label] = {
                        "path": relative_workspace(SELF), **file_record(SELF),
                        "O_NOFOLLOW": True,
                        "single_open_file_description_hash_child_fstat_and_path_identity":
                            True}
                else:
                    labels = sorted(name for name in inputs
                                    if name.startswith("declared-input-"))
                    need(bool(labels), "attestation declared input present")
                    inputs.pop(labels[-1])
            reclose_json(target, "run_attestation_sha256",
                         change_attestation)
        elif mutation == "manifest-reorder":
            lines = target.read_bytes().splitlines()
            need(len(lines) > 1, "reorder manifest rows")
            target.write_bytes(b"\n".join(reversed(lines)) + b"\n")
        elif mutation == "manifest-duplicate":
            lines = target.read_bytes().splitlines()
            need(bool(lines), "manifest rows")
            target.write_bytes(b"\n".join(lines + [lines[0]]) + b"\n")
        elif mutation == "manifest-traversal":
            lines = target.read_bytes().splitlines()
            need(bool(lines), "manifest rows")
            target.write_bytes(b"\n".join(lines + [
                b"0" * 64 + b"  ../outside"]) + b"\n")
        elif mutation == "extra-directory-member":
            need(target.is_dir(), "directory override")
            (target / "unexpected.extra").write_bytes(b"extra\n")
        elif mutation == "manifest-substitute":
            lines = target.read_bytes().splitlines()
            need(bool(lines), "root manifest rows")
            lines[0] = b"0" * 64 + lines[0][64:]
            target.write_bytes(b"\n".join(lines) + b"\n")
        elif mutation not in {"copy", "atomic", "toctou"}:
            raise Rejected("unknown mutation:" + mutation)
    size = 0
    if target.is_file() and not target.is_symlink():
        size = target.stat().st_size
    elif target.is_dir() and not target.is_symlink():
        size = sum(path.stat().st_size for path in target.rglob("*")
                   if path.is_file() and not path.is_symlink())
    return {"logical_path": logical, "physical_path": str(target),
            "private_copy_bytes": size, "mutation": mutation}


def invoke_barrier(command: list[str], environment: dict[str, str],
                   case_root: Path, content_drift: bool,
                   timeout: int) -> dict[str, Any]:
    started = time.monotonic()
    with tempfile.TemporaryFile() as stdout_stream, \
            tempfile.TemporaryFile() as stderr_stream:
        process = subprocess.Popen(command, cwd=ROOT, env=environment,
            stdin=subprocess.DEVNULL, stdout=stdout_stream, stderr=stderr_stream)
        deadline = time.monotonic() + min(timeout, 60)
        try:
            while not (case_root / "fd-opened.lock").exists():
                if process.poll() is not None:
                    break
                need(time.monotonic() < deadline, "barrier opened in time")
                time.sleep(0.01)
            need(process.poll() is None and (case_root / "fd-opened.lock").exists(),
                 "validator reached barrier")
            override = case_root / "override"
            replacement = case_root / "replacement"
            payload = override.read_bytes()
            if content_drift:
                payload += b"TOCTOU\n"
            replacement.write_bytes(payload)
            os.replace(replacement, override)
            (case_root / "continue.lock").write_bytes(b"CONTINUE\n")
            process.wait(timeout=timeout)
            code = process.returncode
            timed_out = False
        except (subprocess.TimeoutExpired, Rejected):
            process.kill()
            process.wait()
            code = process.returncode
            timed_out = True
        stdout_stream.seek(0, os.SEEK_END)
        stdout_size = stdout_stream.tell()
        stderr_stream.seek(0, os.SEEK_END)
        stderr_size = stderr_stream.tell()
        stdout_stream.seek(0)
        stderr_stream.seek(0)
        stdout = stdout_stream.read(MAX_CAPTURE_BYTES + 1)
        stderr = stderr_stream.read(MAX_CAPTURE_BYTES + 1)
    return {"numeric_exit_code": code if code >= 0 else None,
            "signal": -code if code < 0 else None, "timed_out": timed_out,
            "elapsed_seconds": round(time.monotonic() - started, 6),
            "stdout": stdout, "stderr": stderr,
            "stdout_size": stdout_size, "stderr_size": stderr_size,
            "capture_bounded": (stdout_size <= MAX_CAPTURE_BYTES
                                and stderr_size <= MAX_CAPTURE_BYTES)}


def execute_case(args: argparse.Namespace, spec: dict[str, Any], index: int,
                 work: Path, environment: dict[str, str], projection: str,
                 source_pins: dict[str, dict[str, Any]]) -> dict[str, Any]:
    case_root = work / f"private-c27r2-release-fixture-{index:02d}-{spec['name']}"
    process_dir = work / f"case-process-{index:02d}-{spec['name']}"
    started_at = utc_now()
    transcript: dict[str, Any] | None = None
    try:
        case_root.mkdir(mode=0o700)
        prepared = prepare_override(spec, case_root)
        mapping = closed_map("private", [{
            "logical_path": prepared["logical_path"],
            "physical_path": prepared["physical_path"]}])
        map_path = case_root / "override-map.json"
        write_once(map_path, canonical(mapping) + b"\n")
        map_file_sha = file_record(map_path)["sha256"]
        out_file = case_root / "validator-output.json"
        missing_i = spec["name"] == "missing-isolated-python-flag"
        case_env = dict(environment)
        if spec["name"] == "wrong-PYTHONHASHSEED":
            case_env["PYTHONHASHSEED"] = "1"
        barrier = spec["mutation"] in {"atomic", "toctou"}
        command = validator_command(args, "private", map_path, case_root,
            out_file, spec["changes"], missing_i, barrier)
        command_sha = digest(command)
        request_body = {
            "schema": CASE_WRAPPER_REQUEST_SCHEMA,
            "status": CASE_WRAPPER_REQUEST_STATUS,
            "case": spec["name"], "ordinal": index,
            "case_root": str(case_root), "process_dir": str(process_dir),
            "validator_out_file": str(out_file),
            "validator_command": command,
            "validator_environment": case_env,
            "validator_environment_fixture": (
                "wrong-hash" if spec["name"] == "wrong-PYTHONHASHSEED"
                else "fixed"),
            "validator_command_fixture": (
                "missing-isolated" if missing_i else "fixed"),
            "authority_roots": sorted({str(path.absolute())
                                        for path in authoritative_roots(args)}),
            "future_targets": sorted(str((ROOT / relative).absolute())
                for relative in (args.future_outer_relative,
                                 args.future_seal_relative,
                                 args.future_terminal_relative)),
            "future_parent": str(AUDIT),
            "core_unit": args.core_unit,
            "core_invocation_id": args.core_invocation_id,
            "core_exec_start_property_sha256":
                args.core_exec_start_property_sha256,
            "core_fragment_path": args.core_fragment_path,
            "core_fragment_file_sha256": args.core_fragment_file_sha256,
            "core_fragment_stat9_json": args.core_fragment_stat9_json,
            "core_fragment_stat_fingerprint":
                json.loads(args.core_fragment_stat9_json),
            "control_timeout_seconds": args.case_timeout_seconds,
            "expected_authority_projection_sha256": projection,
            "python_path": str(Path(args.python).absolute()),
            "python_sha256": args.expect_python_sha256,
            "validator_path": str(Path(args.validator).absolute()),
            "validator_sha256": args.expect_validator_sha256,
            "runner_path": str(SELF),
            "runner_sha256": args.expect_runner_sha256,
            "wrapper_path": str(Path(args.case_wrapper).absolute()),
            "wrapper_sha256": args.expect_case_wrapper_sha256,
            "source_pins": source_pins,
            "override_map_file_sha256": map_file_sha,
            "override_map_object_sha256": mapping["override_map_sha256"],
            "logical_override": prepared["logical_path"],
            "mutation": prepared["mutation"],
            "barrier_mode": (spec["mutation"] if barrier else "none"),
            "private_copy_bytes": prepared["private_copy_bytes"],
            "formal_credit": 0, "manifest_authorized": False,
            "C27R2": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM",
        }
        request = dict(request_body)
        request["request_sha256"] = digest(request_body)
        request_path = case_root / "wrapper-request.json"
        write_once(request_path, canonical(request) + b"\n")
        request_record = file_record(request_path)
        wrapper_command = [args.python, "-I", "-B", args.case_wrapper,
            "--request", str(request_path),
            "--expect-request-file-sha256", request_record["sha256"],
            "--expect-request-object-sha256", request["request_sha256"],
            "--python", args.python,
            "--expected-python-hash-seed", args.expected_python_hash_seed,
            "--expect-wrapper-sha256", args.expect_case_wrapper_sha256]
        result = invoke(wrapper_command, environment,
                        args.case_timeout_seconds + 120)
        finished_at = utc_now()
        expected_stdout = canonical({"schema": CASE_RUN_SCHEMA + ".stdout.v1",
            "status": CASE_RUN_STATUS, "case": spec["name"],
            "formal_credit": 0, "CM2": "NO-GO_FOR_CLAIM"}) + b"\n"
        need(result["capture_bounded"] is True
             and result["numeric_exit_code"] == 0
             and result["signal"] is None and result["timed_out"] is False
             and result["stderr"] == b"" and result["stdout"] == expected_stdout
             and process_dir.is_dir()
             and {path.name for path in process_dir.iterdir()}
                 == CASE_RUN_FILES,
             "real outer wrapper process clean exact11 transaction:"
             + spec["name"])
        attestation = strict_document(process_dir / "run_attestation.json",
                                      "run_attestation_sha256")
        output = strict_document(process_dir / "output_validation.json",
                                 "output_validation_sha256")
        input_pre, input_post, runner_start = validate_case_input_documents(
            process_dir, request, request_record, command, case_env,
            spec["name"], index)
        need(attestation.get("schema") == CASE_RUN_SCHEMA
             and attestation.get("status") == CASE_RUN_STATUS
             and attestation.get("case") == spec["name"]
             and attestation.get("real_wrapper_process") is True
             and attestation.get("actual_child_numeric_exit_code") == 2
             and attestation.get("actual_child_signal") is None
             and attestation.get("actual_child_timed_out") is False
             and attestation.get("actual_child_validator_output_created")
                 is False
             and attestation.get("actual_authority_pre_post_identical") is True
             and attestation.get("request_file_sha256")
                 == request_record["sha256"]
             and attestation.get("request_object_sha256")
                 == request["request_sha256"]
             and attestation.get("actual_authority_pre_snapshot_sha256")
                 == input_pre["snapshot"]["snapshot_sha256"]
             and attestation.get("actual_authority_post_snapshot_sha256")
                 == input_post["snapshot"]["snapshot_sha256"]
             and output.get("child_numeric_exit_code") == 2
             and output.get("child_signal") is None
             and output.get("child_validator_output_created") is False
             and file_record(process_dir / "stdout.log")["sha256"]
                 == hashlib.sha256(result["stdout"]).hexdigest()
             and (process_dir / "stderr.log").stat().st_size == 0
             and capture_file(process_dir / "exit_code.txt", 1 << 20)[0]
                 == b"0\n"
             and capture_file(process_dir / "signal.json", 1 << 20)[0]
                 == b"null\n"
             and capture_file(process_dir / "PASS.lock", 1 << 20)[0]
                 == CASE_RUN_PASS,
             "outer observation binds real wrapper and validator child")
        input_projection = {
            "argv": command, "environment": case_env,
            "override_map_file_sha256": map_file_sha,
            "override_map_object_sha256": mapping["override_map_sha256"],
            "source_pins": source_pins,
            "wrapper_request_file_sha256": request_record["sha256"],
            "wrapper_request_object_sha256": request["request_sha256"],
        }
        output_projection = {
            "numeric_exit_code": output["child_numeric_exit_code"],
            "signal": output["child_signal"], "timed_out": False,
            "stdout_size": output["child_stdout_size"],
            "stderr_size": output["child_stderr_size"],
            "stdout_sha256": output["child_stdout_sha256"],
            "stderr_sha256": output["child_stderr_sha256"],
            "validator_output_created": False,
            "wrapper_numeric_exit_code": result["numeric_exit_code"],
            "wrapper_signal": result["signal"],
            "wrapper_stdout_sha256": hashlib.sha256(result["stdout"]).hexdigest(),
            "wrapper_stderr_sha256": hashlib.sha256(result["stderr"]).hexdigest(),
        }
        body = {
            "ordinal": index, "case": spec["name"],
            "started_at_utc": started_at, "finished_at_utc": finished_at,
            "logical_override": prepared["logical_path"],
            "mutation": prepared["mutation"],
            "private_copy_bytes": prepared["private_copy_bytes"],
            "override_map_file_sha256": map_file_sha,
            "override_map_object_sha256": mapping["override_map_sha256"],
            "argv": command, "environment": case_env,
            "command_argv_sha256": command_sha,
            "python_sha256": args.expect_python_sha256,
            "validator_sha256": args.expect_validator_sha256,
            "runner_sha256": args.expect_runner_sha256,
            "case_wrapper_sha256": args.expect_case_wrapper_sha256,
            "wrapper_argv": wrapper_command,
            "source_pins": source_pins,
            "input_projection_sha256": digest(input_projection),
            "output_projection_sha256": digest(output_projection),
            **output_projection,
            "elapsed_seconds": result["elapsed_seconds"],
            "stderr_prefix": output["child_stderr_prefix"],
            "capture_limit_bytes": MAX_CAPTURE_BYTES,
            "capture_bounded": True,
            "private_exact_one_override": True,
            "private_case_root_cleaned": True,
            "case_process_directory": relative_workspace(process_dir),
            "formal_credit": 0,
        }
        transcript = dict(body)
        transcript["transcript_sha256"] = digest(body)
    finally:
        remove_private(case_root)
        need(not case_root.exists() and not case_root.is_symlink(),
             "private case root removed as filesystem fact:" + spec["name"])
    need(transcript is not None, "case transcript constructed")
    need(process_dir.is_dir()
         and {path.name for path in process_dir.iterdir()} == CASE_RUN_FILES,
         "case process transaction persisted after private cleanup")
    return transcript


def environment(args: argparse.Namespace) -> dict[str, str]:
    return {"PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
            "PYTHONHASHSEED": args.expected_python_hash_seed}


def execute_lock_preflights(args: argparse.Namespace, work: Path,
                            control: Path, environment_value: dict[str, str],
                            publication_lock: dict[str, Any],
                            publication_lock_fixture: bool = False) \
        -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for index, name in enumerate(LOCK_PREFLIGHT_CASE_NAMES):
        private = work / f"private-publication-lock-preflight-{index:02d}-{name}"
        command = [args.python, "-I", "-B", str(SELF),
            "--lock-preflight-case", name,
            "--lock-preflight-work-dir", str(private),
            "--expected-python-hash-seed", args.expected_python_hash_seed,
            "--expect-runner-sha256", args.expect_runner_sha256]
        started_at = utc_now()
        result = invoke(command, environment_value, 120)
        finished_at = utc_now()
        expected_stderr = (
            "REJECT:EXPECTED_PUBLICATION_LOCK_PREFLIGHT_REJECTION:"
            + name + "\n").encode("ascii")
        need(result["numeric_exit_code"] == 2 and result["signal"] is None
             and result["timed_out"] is False and result["stdout"] == b""
             and result["stderr"] == expected_stderr
             and result["capture_bounded"] is True
             and not private.exists() and not private.is_symlink(),
             "real publication lock preflight rejected/cleaned:" + name)
        need(validate_publication_lock(args, publication_lock_fixture)
                 == publication_lock,
             "real chain publication lock unchanged across preflight")
        body = {"ordinal": index, "case": name,
            "started_at_utc": started_at, "finished_at_utc": finished_at,
            "argv": command, "environment": environment_value,
            "numeric_exit_code": 2, "signal": None, "timed_out": False,
            "stdout_sha256": hashlib.sha256(result["stdout"]).hexdigest(),
            "stderr_sha256": hashlib.sha256(result["stderr"]).hexdigest(),
            "stdout_size": result["stdout_size"],
            "stderr_size": result["stderr_size"],
            "private_root_cleaned": True,
            "runner_sha256": args.expect_runner_sha256,
            "formal_credit": 0}
        record = dict(body)
        record["case_receipt_sha256"] = digest(body)
        records.append(record)
    inventory = {"publication_lock_preflight_case_count":
                     len(LOCK_PREFLIGHT_CASE_NAMES),
                 "ordered_publication_lock_preflight_case_names":
                     LOCK_PREFLIGHT_CASE_NAMES}
    body = {"schema": LOCK_PREFLIGHT_SCHEMA, "status": LOCK_PREFLIGHT_STATUS,
        "mode": "formal", "completed_at_utc": utc_now(),
        "publication_lock_protocol": PUBLICATION_LOCK_PROTOCOL,
        "publication_lock": publication_lock,
        "publication_lock_preflight_case_count": 8,
        "publication_lock_preflight_rejected_count": 8,
        "ordered_publication_lock_preflight_case_names":
            LOCK_PREFLIGHT_CASE_NAMES,
        "ordered_publication_lock_preflight_inventory_sha256":
            PUBLICATION_LOCK_PREFLIGHT_INVENTORY_SHA256,
        "real_subprocess_per_case": True,
        "all_private_roots_cleaned": True, "cases": records,
        "formal_credit": 0, "manifest_authorized": False,
        "C27R2": "UNAUTHORIZED_PENDING_REPAIRED_RELEASE_CHAIN",
        "CM2": "NO-GO_FOR_CLAIM"}
    receipt = dict(body)
    need(digest(inventory) == PUBLICATION_LOCK_PREFLIGHT_INVENTORY_SHA256,
         "frozen ordered 8 lock-preflight inventory digest")
    receipt["lock_preflight_receipt_sha256"] = digest(body)
    path = control / "publication-lock-preflight.json"
    write_once(path, canonical(receipt) + b"\n")
    reread = strict_document(path, "lock_preflight_receipt_sha256")
    need(reread == receipt, "publication lock preflight receipt reopened")
    return receipt


def execute(args: argparse.Namespace) -> dict[str, Any]:
    need(Path(sys.executable).absolute() == Path(args.python).absolute()
         and sys.flags.isolated == 1 and sys.dont_write_bytecode,
         "runner workspace Python -I -B")
    expected_env = environment(args)
    need(dict(os.environ) == expected_env,
         "runner exact environment")
    need(args.service_query_fixture == "fixed",
         "formal runner fixes internal user-bus service query route")
    need(file_record(Path(args.python))["sha256"]
             == args.expect_python_sha256
         and file_record(Path(args.validator))["sha256"]
             == args.expect_validator_sha256
         and file_record(SELF)["sha256"] == args.expect_runner_sha256
         and file_record(Path(args.case_wrapper))["sha256"]
             == args.expect_case_wrapper_sha256,
         "runner/wrapper/validator/Python current pins")
    publication_lock = validate_publication_lock(args)
    work = Path(args.work_dir).absolute()
    out_file = Path(args.out_file).absolute()
    need(work.parent == AUDIT and work.name.startswith(
         "c27r2-release-repair-integrity-v7-")
         and not work.exists() and not work.is_symlink(),
         "fresh direct audit work directory")
    need(out_file.parent == work and out_file.name == "fixture_receipt.json",
         "exact output under work")
    work.mkdir(mode=0o700)
    before = authority_snapshot(args)
    before_projection = authority_projection(before)
    absence_before = future_absence_snapshot(args)
    need(len(absence_before) == 3
         and all(record["exists"] is False and record["symlink"] is False
                 and len(record["parent_stat_fingerprint"]) == 9
                 for record in absence_before.values()),
         "three future authority absence sentinels captured pre-suite")
    source_pins = current_source_pins(args)
    need(source_pins["python"]["sha256"] == args.expect_python_sha256
         and source_pins["validator"]["sha256"]
             == args.expect_validator_sha256
         and source_pins["runner"]["sha256"] == args.expect_runner_sha256
         and source_pins["case_wrapper"]["sha256"]
             == args.expect_case_wrapper_sha256
         and source_pins["cold_helper"]["sha256"]
             == args.expect_cold_helper_sha256
         and source_pins["evidence_builder"]["sha256"]
             == args.expect_evidence_builder_sha256,
         "all transcript source pins current and CLI-bound")
    control = work / "control"
    control.mkdir(mode=0o700)
    empty = closed_map("formal", [])
    empty_path = control / "empty-override-map.json"
    write_once(empty_path, canonical(empty) + b"\n")
    baseline_output = control / "baseline-validation.json"
    baseline_command = validator_command(args, "formal", empty_path, None,
                                         baseline_output)
    baseline = invoke(baseline_command, expected_env, args.control_timeout_seconds)
    need(baseline["numeric_exit_code"] == 0 and baseline["signal"] is None
         and baseline["timed_out"] is False and baseline["stderr"] == b""
         and baseline["capture_bounded"] is True
         and baseline_output.is_file(), "formal empty-override control PASS")
    baseline_value = strict_document(baseline_output, "validation_sha256")
    need(baseline_value.get("status")
             == "PASS_C27R2_RELEASE_REPAIR_BOUNDARY_V7_FORMAL_EMPTY_OVERRIDE_EXACT_SPEC_ATTESTATION_INPUT_SET_FIXED_USER_BUS_SERVICE_QUERY_TEN_PROPERTY_EXECSTART_FRAGMENT_COLD_EXACT14_CURRENT_PROCESS_INVENTORY_AND_AUTHORITY_CLOSURE__ZERO_CREDIT"
         and baseline_value.get("mode") == "formal"
         and baseline_value.get("override_count") == 0
         and baseline_value.get("formal_credit") == 0
         and baseline_value.get("manifest_authorized") is False
         and baseline_value.get("core_service", {}).get("state")
             == before["core_service"]
         and baseline_value.get("cold", {}).get("current_core_service")
             == before["core_service"]
         and baseline_value.get("C27R2")
             == "UNAUTHORIZED_PENDING_REPAIRED_RELEASE_CHAIN",
         "control validation exact conditional state")
    need(validate_publication_lock(args) == publication_lock,
         "publication lock exclusive/current after formal control")
    write_once(control / "baseline.stdout.log", baseline["stdout"])
    write_once(control / "baseline.stderr.log", baseline["stderr"])
    lock_preflight = execute_lock_preflights(
        args, work, control, expected_env, publication_lock)
    records: list[dict[str, Any]] = []
    max_private = 0
    for index, spec in enumerate(case_specs(args)):
        record = execute_case(args, spec, index, work, expected_env,
                              before_projection, source_pins)
        records.append(record)
        max_private = max(max_private, record["private_copy_bytes"])
        need(validate_publication_lock(args) == publication_lock,
             "publication lock exclusive/current after case")
    after = authority_snapshot(args)
    need(before == after, "all authoritative SHA/full9stat unchanged")
    need(len(records) == 70
         and [row["case"] for row in records] == CASE_NAMES
         and all(row["numeric_exit_code"] == 2
                 and row["signal"] is None
                 and row["timed_out"] is False
                 and row["validator_output_created"] is False
                 for row in records),
         "exact 70 real subprocess rejections")
    private_roots = list(work.glob("private-c27r2-release-fixture-*"))
    need(private_roots == [], "all 70 private case roots absent after cleanup")
    case_process_directories = [row["case_process_directory"] for row in records]
    need(len(case_process_directories) == 70
         and len(set(case_process_directories)) == 70
         and all({path.name for path in (ROOT / relative).iterdir()}
                 == CASE_RUN_FILES for relative in case_process_directories),
         "70 distinct exact eleven-file case process directories")
    case_process_names = [Path(relative).name
                          for relative in case_process_directories]
    expected_final_top_inventory = sorted({
        "PASS.lock", "fixture_receipt.json", "control", *case_process_names})
    need({path.name for path in control.iterdir()} == CONTROL_OUTPUT_FILES,
         "exact five-file baseline plus lock-preflight control inventory")
    need(max_private < 3 * (1 << 30), "peak private ordinary copy below 3 GiB")
    authority_projection_sha = authority_projection(before)
    need(authority_projection_sha == before_projection,
         "authority projection stable")
    absence_after = future_absence_snapshot(args)
    need(absence_after == absence_before,
         "future absence sentinel pre/post projection identical")
    absence_projection_sha = digest(absence_before)
    final_absence_before_receipt = future_absence_snapshot(args)
    need(final_absence_before_receipt == absence_before,
         "final-window future absence reread before receipt")
    body = {
        "schema": RESULT_SCHEMA,
        "status": RESULT_STATUS,
        "mode": "formal",
        "completed_at_utc": utc_now(),
        "validator_sha256": args.expect_validator_sha256,
        "runner_sha256": args.expect_runner_sha256,
        "case_wrapper_sha256": args.expect_case_wrapper_sha256,
        "python_sha256": args.expect_python_sha256,
        "source_pins": source_pins,
        "control": {"numeric_exit_code": 0, "signal": None,
            "timed_out": False,
            "empty_override_map_file_sha256": file_record(empty_path)["sha256"],
            "empty_override_map_object_sha256": empty["override_map_sha256"],
            "validation_file_sha256": file_record(baseline_output)["sha256"],
            "validation_object_sha256": baseline_value["validation_sha256"]},
        "baseline_accepted": True,
        "authority_pre_sha_stat_captured": True,
        "validator_negative_case_count": 70,
        "validator_rejected_count": 70,
        "publication_lock_preflight_case_count": 8,
        "publication_lock_preflight_rejected_count": 8,
        "total_integrity_check_count": 78,
        "validator_wrapper_process_execution_count": 70,
        "publication_lock_preflight_process_execution_count": 8,
        "validator_case_process_directories": case_process_directories,
        "validator_case_process_file_inventory": sorted(CASE_RUN_FILES),
        "control_file_inventory": sorted(CONTROL_OUTPUT_FILES),
        "expected_final_top_level_inventory": expected_final_top_inventory,
        "ordered_validator_negative_case_names": CASE_NAMES,
        "ordered_validator_negative_inventory_sha256":
            VALIDATOR_NEGATIVE_INVENTORY_SHA256,
        "validator_cases": records,
        "real_wrapper_subprocess_per_validator_case": True,
        "publication_lock_preflight_receipt_file_sha256":
            file_record(control / "publication-lock-preflight.json")["sha256"],
        "publication_lock_preflight_receipt_object_sha256":
            lock_preflight["lock_preflight_receipt_sha256"],
        "ordered_publication_lock_preflight_case_names":
            LOCK_PREFLIGHT_CASE_NAMES,
        "ordered_publication_lock_preflight_inventory_sha256":
            lock_preflight[
                "ordered_publication_lock_preflight_inventory_sha256"],
        "private_exact_one_override_per_case": True,
        "ordinary_copy_only": True,
        "sequential_private_copy_cleanup": True,
        "case_workdirs_cleaned": True,
        "remaining_private_case_workdirs": 0,
        "retained_case_artifacts_exactly_process_transactions": True,
        "maximum_private_copy_bytes": max_private,
        "peak_private_copy_below_3GiB": True,
        "authoritative_node_count": before["authority_node_count"],
        "authoritative_pre_post_sha_full9stat_identical": True,
        "authoritative_inputs_pre_post_sha_stat_identical": True,
        "authority_pre_post_sha_stat_identical": True,
        "authoritative_projection_sha256": authority_projection_sha,
        "current_core_service_snapshot": before["core_service"],
        "cold_current_core_service_bound": True,
        "service_snapshot_pre_post_identical": True,
        "service_query_policy": {
            "systemctl_path": str(SYSTEMCTL),
            "systemctl_sha256": SYSTEMCTL_SHA256,
            "service_uid": SERVICE_UID,
            "runtime_path": str(SERVICE_RUNTIME),
            "bus_socket_path": str(SERVICE_BUS),
            "environment": CONTROL_BUS_ENV,
            "fixture": args.service_query_fixture,
            "returned_field_count": 10,
            "expected_exec_start_property_sha256":
                args.core_exec_start_property_sha256,
            "expected_fragment_path": args.core_fragment_path,
            "expected_fragment_file_sha256": args.core_fragment_file_sha256,
            "expected_fragment_stat_fingerprint":
                json.loads(args.core_fragment_stat9_json),
        },
        "process_policy": {
            "runner_and_case_wrapper_environment": expected_env,
            "validator_child_environment_default": expected_env,
            "control_service_query_environment": CONTROL_BUS_ENV,
            "control_environment_not_inherited_by_math_or_validator": True,
            "python_isolated": True,
            "python_dont_write_bytecode": True,
        },
        "publication_lock": {
            **publication_lock,
            "exclusive_held_entire_control_and_case_window": True,
            "exclusive_held_entire_publication_window": True,
            "future_writers_require_same_protocol": True,
        },
        "fresh_cold_and_evidence_consumed": True,
        "future_outer_seal_terminal_absent_at_control": True,
        "future_authority_absence_sentinel_count": 3,
        "future_authority_absence_sentinels": absence_before,
        "future_authority_absence_projection_sha256": absence_projection_sha,
        "future_authority_absence_pre_post_identical": True,
        "future_authority_absence_final_before_receipt_verified": True,
        "future_authority_absence_final_before_PASS_verified": True,
        "formal_credit": 0, "manifest_authorized": False,
        "C27R2": "UNAUTHORIZED_PENDING_REPAIRED_RELEASE_CHAIN",
        "C28_C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM",
    }
    result = dict(body)
    result["fixture_receipt_sha256"] = digest(body)
    need(validate_publication_lock(args) == publication_lock,
         "publication lock exclusive/current before receipt publication")
    need(future_absence_snapshot(args) == absence_before,
         "immediate future absence reread before receipt write")
    write_once(out_file, canonical(result) + b"\n")
    need(strict_document(out_file, "fixture_receipt_sha256") == result,
         "reopened canonical fixture receipt object closure")
    expected_before_pass = sorted(set(expected_final_top_inventory)
                                  - {"PASS.lock"})
    need(sorted(path.name for path in work.iterdir()) == expected_before_pass
         and {path.name for path in control.iterdir()} == CONTROL_OUTPUT_FILES
         and strict_document(control / "publication-lock-preflight.json",
                             "lock_preflight_receipt_sha256")
             == lock_preflight
         and all(strict_document(ROOT / relative / "run_attestation.json",
                                 "run_attestation_sha256").get(
                                     "actual_authority_pre_post_identical")
                 is True for relative in case_process_directories),
         "exact current pre-PASS receipt/control/70 wrapper inventories")
    final_absence_before_pass = future_absence_snapshot(args)
    need(final_absence_before_pass == absence_before,
         "final-window future absence reread before PASS")
    write_once(work / "PASS.lock", PASS_BYTES)
    need(validate_publication_lock(args) == publication_lock,
         "publication lock exclusive/current after receipt and PASS fsync")
    need(sorted(path.name for path in work.iterdir())
             == expected_final_top_inventory
         and {path.name for path in control.iterdir()} == CONTROL_OUTPUT_FILES,
         "exact final runner top/control inventory")
    need(strict_document(out_file, "fixture_receipt_sha256") == result
         and capture_file(work / "PASS.lock", 1 << 20)[0] == PASS_BYTES,
         "post-PASS current receipt closure and exact terminal bytes")
    return result


def self_test() -> dict[str, Any]:
    need(len(CASE_NAMES) == 70 and len(set(CASE_NAMES)) == 70,
         "exact unique 70-case inventory")
    need(len(LOCK_PREFLIGHT_CASE_NAMES) == 8
         and len(set(LOCK_PREFLIGHT_CASE_NAMES)) == 8,
         "exact unique 8-case publication lock preflight inventory")
    need(len(CONTROL_OUTPUT_FILES) == 5 and len(CASE_RUN_FILES) == 11,
         "exact control/case process output inventories")
    need(digest({"validator_negative_case_count": len(CASE_NAMES),
            "ordered_validator_negative_case_names": CASE_NAMES})
             == VALIDATOR_NEGATIVE_INVENTORY_SHA256
         and digest({"publication_lock_preflight_case_count":
                len(LOCK_PREFLIGHT_CASE_NAMES),
            "ordered_publication_lock_preflight_case_names":
                LOCK_PREFLIGHT_CASE_NAMES})
             == PUBLICATION_LOCK_PREFLIGHT_INVENTORY_SHA256,
         "separate ordered validator/lock inventory object digest fixtures")
    fixed_bus = service_query_environment("fixed")
    missing_bus = service_query_environment("missing")
    wrong_bus = service_query_environment("wrong")
    need(fixed_bus == CONTROL_BUS_ENV
         and set(fixed_bus) == {"PATH", "LANG", "LC_ALL",
                               "XDG_RUNTIME_DIR",
                               "DBUS_SESSION_BUS_ADDRESS"}
         and missing_bus == {"PATH": "/usr/bin:/bin", "LANG": "C",
                             "LC_ALL": "C"}
         and wrong_bus["XDG_RUNTIME_DIR"]
             == "/run/user/1000/c27r2-missing-runtime"
         and wrong_bus["DBUS_SESSION_BUS_ADDRESS"]
             == "unix:path=/run/user/1000/c27r2-missing-bus"
         and wrong_bus != fixed_bus,
         "fixed/missing/wrong user-bus query environment fixtures")
    service_fixture = (
        b"Result=success\nExecMainCode=1\nExecMainStatus=0\n"
        b"ExecStart={ path=/x ; argv[]=x --a=b ; status=0 }\nId=u.service\n"
        b"LoadState=loaded\nActiveState=active\nSubState=exited\n"
        b"FragmentPath=/run/user/1000/systemd/transient/u.service\n"
        b"InvocationID=0123456789abcdef0123456789abcdef\n")
    parsed_service = parse_service_properties(service_fixture)
    need(parsed_service["Id"] == "u.service"
         and "--a=b" in parsed_service["ExecStart"]
         and set(parsed_service) == set(SERVICE_FIELDS),
         "ten-key first-equals service property fixture")
    dummy = argparse.Namespace(
        actual_terminal_relative="audit/actual-terminal",
        actual_base_relative="audit/actual-base", gate_relative="audit/gate",
        seed1_edge_relative="audit/seed1", seed2_edge_relative="audit/seed2",
        frozen_c15_relative="audit/c15", core_control_relative="audit/core",
        candidate_relative="audit/candidate",
        verifier_output_relative="audit/verifier",
        attack_work_relative="audit/attacks",
        producer_run_relative="audit/producer-run",
        verifier_run_relative="audit/verifier-run",
        attack_run_relative="audit/attack-run",
        cold_control_relative="audit/cold-control",
        cold_output_relative="audit/cold-output",
        cold_run_relative="audit/cold-run",
        evidence_relative="audit/evidence",
        future_outer_relative="audit/future-outer",
        future_seal_relative="audit/future-seal",
        future_terminal_relative="audit/future-terminal",
        expect_actual_terminal_receipt_file_sha256="1" * 64,
        expect_actual_terminal_receipt_object_sha256="2" * 64,
        expect_actual_terminal_root_sha256="3" * 64,
    )
    specs = case_specs(dummy)
    need(len(specs) == 70 and [row["name"] for row in specs] == CASE_NAMES
         and all(set(row) == {"name", "logical", "mutation", "changes"}
                 for row in specs),
         "actual exact70 case-spec construction fixture")
    formal = closed_map("formal", [])
    private = closed_map("private", [{"logical_path": "x/y",
                                       "physical_path": "/tmp/case/override"}])
    need(formal["override_map_sha256"] == digest({key: value for key, value
        in formal.items() if key != "override_map_sha256"})
         and private["override_map_sha256"] == digest({key: value for key, value
        in private.items() if key != "override_map_sha256"}),
        "override closure fixtures")
    with tempfile.TemporaryDirectory(prefix="c27r2-fixture-runner-v7-") as raw:
        root = Path(raw)
        lock_body = {
            "schema": PUBLICATION_LOCK_SCHEMA,
            "status": PUBLICATION_LOCK_STATUS,
            "protocol": PUBLICATION_LOCK_PROTOCOL,
            "one_shot_launch_id": "tiny-launch-control-v1",
            "plan_file_sha256": "1" * 64,
            "plan_object_sha256": "2" * 64,
            "formal_credit": 0, "manifest_authorized": False,
            "authority_minted": False,
        }
        lock_value = dict(lock_body)
        lock_value["publication_lock_sha256"] = digest(lock_body)
        lock_path = root / "publication_lock.json"
        write_once(lock_path, canonical(lock_value) + b"\n")
        lock_record = file_record(lock_path)
        lock_fd = os.open(lock_path, os.O_RDONLY
                          | getattr(os, "O_CLOEXEC", 0)
                          | getattr(os, "O_NOFOLLOW", 0))
        lock_args = argparse.Namespace(
            publication_lock_path=str(lock_path),
            publication_lock_file_sha256=lock_record["sha256"],
            publication_lock_object_sha256=
                lock_value["publication_lock_sha256"],
            publication_lock_stat9_json=canonical(
                lock_record["stat_fingerprint"]).decode("ascii"),
            publication_lock_fd=lock_fd)
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            verified_lock = validate_publication_lock(lock_args, fixture=True)
            need(verified_lock["exclusive_held"] is True
                 and verified_lock["path_fd_same_inode"] is True,
                 "real inherited exclusive publication lock fixture")
            for changed in (
                {"publication_lock_file_sha256":
                    flip(lock_record["sha256"])},
                {"publication_lock_stat9_json": canonical(
                    [*lock_record["stat_fingerprint"][:1],
                     lock_record["stat_fingerprint"][1] + 1,
                     *lock_record["stat_fingerprint"][2:]]).decode("ascii")},
            ):
                broken = argparse.Namespace(**vars(lock_args))
                for key, value in changed.items():
                    setattr(broken, key, value)
                try:
                    validate_publication_lock(broken, fixture=True)
                except (Rejected, OSError):
                    pass
                else:
                    raise Rejected("publication lock pin/stat drift rejected")
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
            try:
                validate_publication_lock(lock_args, fixture=True)
            except (Rejected, OSError):
                pass
            else:
                raise Rejected("unlocked publication fd rejected")
            fcntl.flock(lock_fd, fcntl.LOCK_SH | fcntl.LOCK_NB)
            try:
                validate_publication_lock(lock_args, fixture=True)
            except (Rejected, OSError):
                pass
            else:
                raise Rejected("shared-only publication fd rejected")
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            preflight_work = root / "lock-preflight-work"
            preflight_control = preflight_work / "control"
            preflight_control.mkdir(parents=True)
            preflight_args = argparse.Namespace(**vars(lock_args))
            preflight_args.python = "/usr/bin/python3.12"
            preflight_args.expected_python_hash_seed = "30662790"
            preflight_args.expect_runner_sha256 = file_record(SELF)["sha256"]
            preflight_environment = {
                "PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
                "PYTHONHASHSEED": "30662790"}
            preflight_receipt = execute_lock_preflights(
                preflight_args, preflight_work, preflight_control,
                preflight_environment, verified_lock, True)
            need(preflight_receipt[
                     "publication_lock_preflight_case_count"] == 8
                 and preflight_receipt[
                     "publication_lock_preflight_rejected_count"] == 8
                 and preflight_receipt["ordered_publication_lock_preflight_case_names"]
                     == LOCK_PREFLIGHT_CASE_NAMES,
                 "8/8 real publication lock preflight subprocess fixtures")
        finally:
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
            os.close(lock_fd)
        sentinel_parent = root / "sentinel-parent"
        sentinel_parent.mkdir()
        sentinel_targets = [sentinel_parent / name for name in
                            ("future-outer", "future-seal", "future-terminal")]
        sentinel_before = absence_sentinels(sentinel_targets, sentinel_parent)
        sentinel_targets[1].mkdir()
        try:
            absence_sentinels(sentinel_targets, sentinel_parent)
        except Rejected:
            pass
        else:
            raise Rejected("final-window future creation fixture rejected")
        remove_private(sentinel_targets[1])
        sentinel_after_cleanup = absence_sentinels(
            sentinel_targets, sentinel_parent)
        need(len(sentinel_before) == len(sentinel_after_cleanup) == 3
             and all(record["exists"] is False
                     for record in sentinel_after_cleanup.values()),
             "final-window creation rejected and cleanup restores absence")
        source = root / "source.json"
        body = {"schema": "fixture", "formal_credit": 0}
        value = dict(body)
        value["receipt_sha256"] = digest(body)
        source.write_bytes(canonical(value) + b"\n")
        copy = root / "copy.json"
        copy_ordinary(source, copy)
        reclose_json(copy, "receipt_sha256",
                     lambda item: item.__setitem__("formal_credit", 1))
        need(strict_document(copy, "receipt_sha256")["formal_credit"] == 1,
             "coherent reclosure fixture")
        hard_source = root / "hard-source"
        hard_target = root / "hard-target"
        hard_source.write_bytes(b"x")
        os.link(hard_source, hard_target)
        need(os.stat(hard_source).st_nlink == os.stat(hard_target).st_nlink == 2,
             "private hardlink fixture")
        private_root = root / "private-c27r2-release-fixture-00-tiny"
        private_root.mkdir()
        (private_root / "override").write_bytes(b"tiny\n")
        remove_private(private_root)
        need(not private_root.exists() and not private_root.is_symlink(),
             "real private-root cleanup fixture")
        exact_env = {"PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
                     "PYTHONHASHSEED": "30662790"}
        input_dir = root / "input-rebind"
        input_dir.mkdir()
        request_body = {"schema": "runner-input-rebind-fixture.v1"}
        request = dict(request_body)
        request["request_sha256"] = digest(request_body)
        request_record = {"sha256": hashlib.sha256(b"request-file").hexdigest()}
        command = ["/usr/bin/python3.12", "-I", "-B", "validator.py"]
        snapshot = {"snapshot_sha256": hashlib.sha256(b"snapshot").hexdigest()}
        common_input = {"schema": CASE_RUN_SCHEMA + ".input.v1",
            "case": "tiny", "ordinal": 0,
            "request_file_sha256": request_record["sha256"],
            "request_object_sha256": request["request_sha256"],
            "wrapper_request": request, "snapshot": snapshot,
            "validator_command": command, "validator_environment": exact_env,
            "formal_credit": 0}
        write_once(input_dir / "input_pre.json", canonical(
            {**common_input, "phase": "pre"}) + b"\n")
        write_once(input_dir / "input_post.json", canonical(
            {**common_input, "phase": "post"}) + b"\n")
        write_once(input_dir / "runner_start.json", canonical({
            "schema": CASE_RUN_SCHEMA + ".start.v1", "mode": "formal",
            "case": "tiny", "ordinal": 0, "started_at_utc": "fixture",
            "exact_argv": command, "exact_environment": exact_env,
            "wrapper_pid": 1, "formal_credit": 0}) + b"\n")
        rebound = validate_case_input_documents(input_dir, request,
            request_record, command, exact_env, "tiny", 0)
        need(rebound[0]["wrapper_request"] == rebound[1]["wrapper_request"]
                 == request,
             "runner exact input pre/post request/argv/env rebind fixture")
        wrapper_selftest = invoke([
            "/usr/bin/python3.12", "-I", "-B", str(CASE_WRAPPER_DEFAULT),
            "--self-test"], exact_env, 30)
        need(wrapper_selftest["numeric_exit_code"] == 0
             and wrapper_selftest["signal"] is None
             and wrapper_selftest["timed_out"] is False
             and wrapper_selftest["stderr"] == b""
             and b"REAL_TREE_EMPTY_DIR_WRITE_ALL_REOPEN" in
                 wrapper_selftest["stdout"],
             "real immutable case-wrapper subprocess selftest fixture")
        bounded = invoke(["/usr/bin/python3.12", "-I", "-B", "-c",
                          "import sys;sys.stdout.write('ok')"], exact_env, 30)
        overflow = invoke(["/usr/bin/python3.12", "-I", "-B", "-c",
                           "import sys;sys.stdout.write('x'*1048577)"],
                          exact_env, 30)
        need(bounded["capture_bounded"] is True and bounded["stdout"] == b"ok"
             and overflow["capture_bounded"] is False
             and overflow["stdout_size"] == MAX_CAPTURE_BYTES + 1,
             "real bounded communicate and overflow fixture")
    return {"schema": RESULT_SCHEMA + ".self-test",
            "status": "PASS_EXACT_70_VALIDATOR_REAL_WRAPPERS_AND_8_LOCK_"
                      "PREFLIGHTS_EXACT11_CLEANUP_BOUNDED_PROCESS_PRIVATE_"
                      "LINK_FIXED_MISSING_WRONG_USER_BUS_AND_FINAL_WINDOW_"
                      "ABSENCE_TINY_FIXTURES",
            "formal_reads": 0, "formal_outputs": 0,
            "formal_credit": 0, "manifest_authorized": False,
            "C27R2": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM"}


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--self-test", action="store_true")
    value.add_argument("--lock-preflight-case",
                       choices=tuple(LOCK_PREFLIGHT_CASE_NAMES))
    value.add_argument("--lock-preflight-work-dir")
    value.add_argument("--validator", default=str(VALIDATOR_DEFAULT))
    value.add_argument("--case-wrapper", default=str(CASE_WRAPPER_DEFAULT))
    value.add_argument("--expect-case-wrapper-sha256")
    value.add_argument("--expect-runner-sha256")
    value.add_argument("--work-dir")
    value.add_argument("--out-file")
    value.add_argument("--control-timeout-seconds", type=int, default=21_600)
    value.add_argument("--case-timeout-seconds", type=int, default=21_600)
    value.add_argument("--publication-lock-path")
    value.add_argument("--publication-lock-file-sha256")
    value.add_argument("--publication-lock-object-sha256")
    value.add_argument("--publication-lock-stat9-json")
    value.add_argument("--publication-lock-fd", type=int)
    for name in VALIDATOR_COMMON:
        value.add_argument("--" + name.replace("_", "-"))
    return value


def main() -> int:
    args = parser().parse_args()
    try:
        if args.self_test:
            result = self_test()
        elif args.lock_preflight_case is not None:
            need(args.lock_preflight_work_dir is not None
                 and args.expected_python_hash_seed is not None
                 and args.expect_runner_sha256 is not None,
                 "all lock preflight worker arguments required")
            execute_lock_preflight_case(args)
            raise Rejected("lock preflight worker did not reject")
        else:
            need(args.work_dir is not None and args.out_file is not None
                 and args.expect_runner_sha256 is not None
                 and args.expect_case_wrapper_sha256 is not None
                 and args.publication_lock_path is not None
                 and args.publication_lock_file_sha256 is not None
                 and args.publication_lock_object_sha256 is not None
                 and args.publication_lock_stat9_json is not None
                 and args.publication_lock_fd is not None
                 and all(getattr(args, name) is not None
                         for name in VALIDATOR_COMMON),
                 "all formal runner arguments required")
            need(all(valid_sha(getattr(args, name)) for name in
                [item for item in VALIDATOR_COMMON if item.startswith("expect_")]
                + ["expect_runner_sha256", "publication_lock_file_sha256",
                   "publication_lock_object_sha256",
                   "expect_case_wrapper_sha256"]),
                 "all SHA pins lowercase exact")
            result = execute(args)
        sys.stdout.buffer.write(canonical({"schema": result["schema"],
            "status": result["status"], "formal_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM"}) + b"\n")
        return 0
    except (Rejected, OSError, ValueError, KeyError, TypeError,
            subprocess.SubprocessError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
