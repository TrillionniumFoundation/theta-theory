#!/usr/bin/env python3
"""Fresh-path, exact-service watcher for the C27R2 v4 repair chain.

Default behavior is execution-disabled preflight.  Execution requires a
separately audited enable receipt whose file and object SHA are CLI pinned.
All transaction stages are serial and fail closed.  The finalizer runs as its
own pinned user service; after it exits, this watcher verifies Result=success,
ExecMainStatus=0 and the exact InvocationID.  It never edits terminal files.
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
import subprocess
import sys
import tempfile
import time
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
AUDIT = ROOT / ".cm2-runtime/audit"
BASE = "cm2.round306c27r2.source-g-authority-v2.release-repair."
PLAN_SCHEMA = BASE + "chain-plan.v4"
PLAN_STATUS = (
    "FROZEN_C27R2_RELEASE_REPAIR_V4_EXACT70_PLUS_LOCK8_PLAN__EXECUTION_DISABLED_"
    "PENDING_INDEPENDENT_FULL_CHAIN_AUDIT"
)
ENABLE_SCHEMA = BASE + "execution-enable-receipt.v4"
ENABLE_STATUS = (
    "AUTHORIZED_C27R2_RELEASE_REPAIR_V4_EXACT_PLAN_AND_SOURCES_FOR_ONE_"
    "FRESH_EXECUTION"
)
PREFLIGHT_SCHEMA = BASE + "watcher-preflight.v4"
STAGES = (
    "boundary_preflight", "fresh_cold", "snapshot", "baseline",
    "integrity70_plus_lock8",
    "post", "post_evidence", "manifest", "outer", "conditional_seal",
    "anticipated_terminal",
)
CORE_SERVICE = {"unit":
    "cm2-c27r2-source-g-authority-v2-v6-formal-r2-20260808T180523.service",
    "invocation_id": "aa82e1c6611f4910ae80b94307fb9ca9",
    "load_state": "loaded", "active_state": "active", "sub_state": "exited",
    "result": "success", "exec_main_code": "1", "exec_main_status": "0",
    "fragment_path": ("/run/user/1000/systemd/transient/"
        "cm2-c27r2-source-g-authority-v2-v6-formal-r2-20260808T180523.service"),
    "exec_start_projection_sha256":
        "78978b87ff41a53168897bf103ec692f28b5174b1cc3d063a8eb77cd965c3c29"}
CORE_FILE = "4104edc46bb130bae530a990609d5053bc9d7f675e4e3587e88b8327394c5796"
CORE_OBJECT = "783d05cb9c01a2049a03112f9412bab787b5fad2c81fba1855d9cca4dabcb016"
TERMINAL_SCHEMA = BASE + "terminal-receipt.v4"
TERMINAL_REPLAY_SCHEMA = BASE + "terminal-replay.v4"
CHAIN_SCHEMA = BASE + "release-chain-status.v4"
TERMINAL_STATUS = (
    "PASS_C27R2_RELEASE_REPAIR_V4_FILESYSTEM_TERMINAL_PASS_LAST__JOINT_"
    "AUTHORITY_REQUIRES_CURRENT_FINALIZER_UNIT_CLEAN_SUCCESS"
)
TERMINAL_FILES = {"PASS.lock", "chain_status.json",
    "payload_manifest.sha256", "root_manifest.sha256",
    "terminal_receipt.json", "terminal_replay.json"}
TERMINAL_PASS = (
    b"PASS_C27R2_RELEASE_REPAIR_V4_JOINT_SERVICE_GATED_TERMINAL__"
    b"C28_C29_REBIND_PENDING\n"
)
BOUNDARY_CONTRACT_FROZEN_GO = False  # boundary v4 NO-GO; append-only v5 pending.
FORMAL_EXECUTION_AUTHORIZED = False  # Independent full-chain GO has not been minted.
LOCK_SCHEMA = BASE + "publication-lock.v1"
LOCK_STATUS = "FROZEN_ONE_SHOT_PUBLICATION_LOCK__NO_AUTHORITY"
LOCK_PROTOCOL = "FLOCK_EXCLUSIVE_WHOLE_PUBLICATION_WINDOW_V1"
SPEC_SCHEMA = BASE + "release-repair-process-command-spec.v4"
SPEC_STATUS = "FROZEN_C27R2_RELEASE_REPAIR_V4_EXACT_PROCESS_COMMAND_SPEC"
PINSET_SCHEMA = BASE + "release-repair-process-pinset.v4"
PINSET_STATUS = "FROZEN_C27R2_RELEASE_REPAIR_V4_EXACT_PROCESS_PINSET"
RUN_SCHEMA = BASE + "release-repair-process-run-attestation.v4"
RUN_STATUS = (
    "PASS_C27R2_RELEASE_REPAIR_PROCESS_EXIT0_NULL_SIGNAL_EMPTY_STDERR_"
    "EXACT_SPEC_PINSET_ARGV_ENV_PRE_POST_FULL9STAT_AND_OUTPUT_INVENTORY__"
    "ZERO_CREDIT"
)
LAUNCH_SCHEMA = BASE + "stage-launch-receipt.v4"
PLACEHOLDER = re.compile(r"\$\{([A-Z][A-Z0-9_]*)\}")
ROLE_KEYS = {"path", "kind", "available_after", "file_sha256", "closure",
             "object_sha256", "schema", "status"}
TEMPLATE_KEYS = {"source_role", "input_roles", "output_roots",
    "output_documents", "expected_output_role", "argv_template",
    "argv_template_sha256", "binding_sources", "python_hash_seed",
    "timeout_seconds", "expected_stdout"}
FINALIZER_TEMPLATE_KEYS = {"source_role", "argv_template",
    "argv_template_sha256", "binding_sources", "python_hash_seed"}
SYSTEMD_RUN_POLICY = {"service_type": "exec", "working_directory": str(ROOT),
    "umask": "0077", "no_new_privileges": True, "private_tmp": True,
    "protect_system": "full", "read_write_path": str(AUDIT),
    "transient_collect": False}
SYSTEMCTL_SHA = "7ba82b5ba146759c710e1b80fadaa3fdbc0f9b85c8fb2c8c3196b7b1a0037ef8"


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
    need(type(template) is list and len(template) >= 4
         and all(type(token) is str and token and "\x00" not in token
                 and "\n" not in token and "\r" not in token
                 for token in template), "strict argv template tokens")
    need(type(bindings) is dict and list(bindings) == sorted(bindings)
         and all(re.fullmatch(r"[A-Z][A-Z0-9_]*", role) is not None
                 and type(value) is str and value and "\x00" not in value
                 and "\n" not in value and "\r" not in value
                 for role, value in bindings.items()),
         "sorted strict argv bindings")
    referenced: list[str] = []
    answer: list[str] = []
    for token in template:
        match = PLACEHOLDER.fullmatch(token)
        if match is None:
            need("${" not in token and "}" not in token,
                 "placeholder must occupy whole argv token")
            answer.append(token)
        else:
            role = match.group(1)
            need(role in bindings, "unknown argv placeholder:" + role)
            referenced.append(role); answer.append(bindings[role])
    need(sorted(set(referenced)) == list(bindings),
         "all and only allowlisted bindings referenced")
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
             "single-link file")
        state = hashlib.sha256()
        chunks: list[bytes] = []
        while block := os.read(descriptor, 1 << 20):
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


def write_json(path: Path, value: Any) -> None:
    write_once(path, canonical(value) + b"\n")


def fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
                         | getattr(os, "O_NOFOLLOW", 0))
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def acquire_publication_lock(args: argparse.Namespace, plan: dict[str, Any],
                             plan_record: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    need(valid_sha(args.expect_publication_lock_file_sha256)
         and valid_sha(args.expect_publication_lock_object_sha256),
         "publication lock CLI pins")
    expected_stat = strict(args.expect_publication_lock_stat9_json.encode("ascii"))
    need(type(expected_stat) is list and len(expected_stat) == 9
         and all(type(value) is int for value in expected_stat),
         "publication lock exact stat9 CLI")
    lock_contract = plan.get("publication_lock")
    need(type(lock_contract) is dict and set(lock_contract) == {
         "path", "schema", "status", "protocol"}
         and lock_contract["path"] == args.publication_lock_path
         and lock_contract["schema"] == LOCK_SCHEMA
         and lock_contract["status"] == LOCK_STATUS
         and lock_contract["protocol"] == LOCK_PROTOCOL,
         "plan publication lock role/protocol")
    path = inside(args.publication_lock_path)
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
                         | getattr(os, "O_CLOEXEC", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1
             and fingerprint(before) == expected_stat
             and fingerprint(os.stat(path, follow_symlinks=False)) == expected_stat,
             "publication lock FD/path stat9 identity")
        state = hashlib.sha256(); chunks: list[bytes] = []
        while block := os.read(descriptor, 1 << 20):
            state.update(block); chunks.append(block)
        raw = b"".join(chunks)
        need(state.hexdigest() == args.expect_publication_lock_file_sha256
             and raw.endswith(b"\n"), "publication lock file SHA/newline")
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
             "canonical publication lock object/plan closure")
        fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        need(fingerprint(os.fstat(descriptor)) == expected_stat
             and fingerprint(os.stat(path, follow_symlinks=False)) == expected_stat,
             "publication lock stable after exclusive acquisition")
        return descriptor, value
    except BaseException:
        os.close(descriptor)
        raise


def control_bus_environment() -> dict[str, str]:
    runtime = f"/run/user/{os.getuid()}"
    bus = f"unix:path={runtime}/bus"
    need(Path(runtime).is_dir() and not Path(runtime).is_symlink(),
         "current user runtime directory")
    return {"PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
            "XDG_RUNTIME_DIR": runtime, "DBUS_SESSION_BUS_ADDRESS": bus}


def parse_manifest(path: Path) -> dict[str, str]:
    raw, _ = capture(path)
    need(raw.endswith(b"\n"), "manifest newline")
    result: dict[str, str] = {}
    for line in raw.decode("ascii").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\x00\r\n]+)", line)
        need(match is not None, "manifest row")
        claim, shown = match.groups()
        need(shown not in result and record(inside(shown))["sha256"] == claim,
             "manifest current member")
        result[shown] = claim
    need(result and list(result) == sorted(result), "sorted nonempty manifest")
    return result


def service_show(unit: str) -> dict[str, str]:
    need(external_record(Path("/usr/bin/systemctl"))["sha256"] == SYSTEMCTL_SHA,
         "frozen systemctl binary")
    fields = ("Id", "LoadState", "ActiveState", "SubState", "Result",
              "ExecMainCode", "ExecMainStatus", "InvocationID", "ExecStart",
              "FragmentPath")
    command = ["/usr/bin/systemctl", "--user", "show", unit,
        "--property=" + ",".join(fields),
        "--no-pager"]
    completed = subprocess.run(command, cwd=ROOT,
        env=control_bus_environment(), stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=30)
    need(completed.returncode == 0 and completed.stderr == b"",
         "systemd show success")
    result: dict[str, str] = {}
    for line in completed.stdout.decode("ascii").splitlines():
        key, separator, value = line.partition("=")
        need(separator == "=" and key not in result, "systemd show row")
        result[key] = value
    need(set(result) == set(fields), "systemd show complete identity fields")
    return result


def exec_start_projection(value: str) -> dict[str, str]:
    match = re.fullmatch(
        r"\{ path=([^ ;]+) ; argv\[\]=(.*?) ; ignore_errors=.*", value)
    need(match is not None and bool(match.group(1)) and bool(match.group(2)),
         "canonical nonempty ExecStart projection")
    return {"path": match.group(1), "argv": match.group(2)}


def verify_service(actual: dict[str, str], expected: dict[str, Any],
                   require_inactive: bool,
                   expected_exec_argv: list[str] | None = None) -> None:
    expected_invocation = expected.get("invocation_id")
    projection = exec_start_projection(actual["ExecStart"])
    projection_sha = digest(projection)
    expected_projection_sha = expected.get("exec_start_projection_sha256")
    if expected_exec_argv is not None:
        need(all(type(token) is str and token and not any(character.isspace()
             for character in token) for token in expected_exec_argv),
             "unambiguous expected ExecStart argv")
        expected_projection_sha = digest({"path": expected_exec_argv[0],
            "argv": " ".join(expected_exec_argv)})
    need(actual["Id"] == expected["unit"]
         and actual["LoadState"] == expected["load_state"]
         and actual["ActiveState"] == expected["active_state"]
         and actual["SubState"] == expected["sub_state"]
         and actual["Result"] == expected["result"]
         and actual["ExecMainCode"] == str(expected["exec_main_code"])
         and actual["ExecMainStatus"] == str(expected["exec_main_status"])
         and actual["FragmentPath"] == expected["fragment_path"]
         and valid_sha(expected_projection_sha)
         and projection_sha == expected_projection_sha
         and re.fullmatch(r"[0-9a-f]{32}", actual["InvocationID"]) is not None
         and (expected_invocation is None
              or actual["InvocationID"] == expected_invocation)
         and (not require_inactive or (actual["ActiveState"] == "inactive"
              and actual["SubState"] == "dead")),
         "unit/invocation/ExecStart/FragmentPath/clean service tuple")


def validate_plan(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any]]:
    need(valid_sha(args.expect_self_sha256)
         and record(SELF)["sha256"] == args.expect_self_sha256, "watcher pin")
    plan, plan_record = document(inside(args.plan), "plan_sha256")
    need(plan_record["sha256"] == args.expect_plan_file_sha256
         and plan["plan_sha256"] == args.expect_plan_object_sha256
         and plan.get("schema") == PLAN_SCHEMA and plan.get("status") == PLAN_STATUS
         and plan.get("validator_negative_case_count") == 70
         and plan.get("publication_lock_preflight_case_count") == 8
         and plan.get("total_integrity_check_count") == 78
         and "case_count" not in plan
         and plan.get("stages") == list(STAGES) + ["official_finalizer_service"]
         and plan.get("core_receipt_file_sha256") == CORE_FILE
         and plan.get("core_receipt_object_sha256") == CORE_OBJECT
         and plan.get("execution_enabled") is False
         and plan.get("formal_credit") == 0
         and plan.get("manifest_authorized") is False
         and plan.get("authority_minted") is False,
         "frozen disabled plan")
    fresh = plan.get("fresh_paths")
    need(type(fresh) is dict and set(fresh) == set(STAGES) | {"official_terminal"},
         "exact fresh path roles")
    paths = [inside(fresh[role], absent=True) for role in sorted(fresh)]
    need(len(paths) == len(set(paths))
         and all(path.parent == AUDIT for path in paths),
         "distinct direct audit path roles")
    launch_control = inside(plan.get("launch_control_dir", ""))
    need(launch_control.is_dir() and not launch_control.is_symlink()
         and all(launch_control != path and launch_control not in path.parents
                 and path not in launch_control.parents for path in paths),
         "separate precreated launch-control directory")
    sources = plan.get("sources")
    need(type(sources) is dict and "transaction_runner" in sources,
         "fixed source role map")
    for role, source in sources.items():
        need(type(role) is str and type(source) is dict
             and set(source) == {"path", "sha256"}
             and valid_sha(source["sha256"])
             and record(inside(source["path"]))["sha256"] == source["sha256"],
             "current source role pin:" + str(role))
    python_runtime = plan.get("python_runtime")
    need(type(python_runtime) is dict
         and set(python_runtime) == {"path", "sha256"}
         and Path(python_runtime["path"]).is_absolute()
         and valid_sha(python_runtime["sha256"]), "external Python role")
    roles = plan.get("role_map")
    need(type(roles) is dict and list(roles) == sorted(roles)
         and "plan" in roles and "publication_lock" in roles,
         "sorted fixed role map")
    for role, value in roles.items():
        need(type(role) is str and type(value) is dict and set(value) == ROLE_KEYS
             and value["kind"] in {"plan_cli", "frozen_input",
                 "runtime_output", "fresh_directory"}
             and value["available_after"] in {"preflight", *STAGES}
             and type(value["path"]) is str
             and (value["file_sha256"] is None
                  or valid_sha(value["file_sha256"]))
             and (value["object_sha256"] is None
                  or valid_sha(value["object_sha256"]))
             and (value["closure"] is None or type(value["closure"]) is str)
             and (value["schema"] is None or type(value["schema"]) is str)
             and (value["status"] is None or type(value["status"]) is str),
             "strict role entry:" + str(role))
        inside(value["path"], absent=value["kind"] in {
            "runtime_output", "fresh_directory"})
    need(roles["plan"]["kind"] == "plan_cli"
         and inside(roles["plan"]["path"]) == inside(args.plan)
         and roles["publication_lock"]["path"]
             == plan.get("publication_lock", {}).get("path"),
         "plan CLI/publication-lock roles")
    commands = plan.get("stage_templates")
    need(type(commands) is dict and set(commands) == set(STAGES),
         "exact inner stage templates")
    for stage in STAGES:
        spec = commands[stage]
        need(type(spec) is dict and set(spec) == TEMPLATE_KEYS
             and spec["source_role"] in sources
             and type(spec["input_roles"]) is list
             and spec["input_roles"] == sorted(set(spec["input_roles"]))
             and {"plan", "publication_lock", "transaction_runner",
                  spec["source_role"]} <= set(spec["input_roles"])
             and all(role in roles for role in spec["input_roles"])
             and type(spec["output_roots"]) is list
             and type(spec["output_documents"]) is list
             and spec["expected_output_role"] in roles
             and spec["argv_template_sha256"] == digest(spec["argv_template"])
             and type(spec["binding_sources"]) is dict
             and list(spec["binding_sources"]) == sorted(spec["binding_sources"])
             and all(type(binding) is dict
                     and set(binding) == {"role", "selector"}
                     and binding["role"] in roles
                     and binding["selector"] in {"path", "absolute_path", "file_sha256",
                                                  "object_sha256"}
                     for binding in spec["binding_sources"].values())
             and type(spec["python_hash_seed"]) is str
             and spec["python_hash_seed"].isdigit()
             and type(spec["timeout_seconds"]) is int
             and 1 <= spec["timeout_seconds"] <= 86_400
             and type(spec["expected_stdout"]) is dict
             and spec["expected_stdout"].get("formal_credit") == 0
             and spec["expected_stdout"].get("CM2") == "NO-GO_FOR_CLAIM",
             "stage template contract:" + stage)
        for root in spec["output_roots"]:
            need(type(root) is dict and set(root) == {"role", "exact_files"}
                 and root["role"] in roles
                 and roles[root["role"]]["kind"] == "fresh_directory"
                 and type(root["exact_files"]) is list
                 and root["exact_files"] == sorted(set(root["exact_files"])),
                 "stage output root role:" + stage)
        for output in spec["output_documents"]:
            need(type(output) is dict and set(output) == {
                 "role", "closure", "schema", "status"}
                 and output["role"] in roles
                 and all(type(output[key]) is str
                         for key in ("closure", "schema", "status")),
                 "stage output document role:" + stage)
    finalizer_template = plan.get("finalizer_template")
    need(type(finalizer_template) is dict
         and set(finalizer_template) == FINALIZER_TEMPLATE_KEYS
         and finalizer_template["source_role"] in sources
         and finalizer_template["argv_template_sha256"]
             == digest(finalizer_template["argv_template"])
         and type(finalizer_template["binding_sources"]) is dict
         and list(finalizer_template["binding_sources"])
             == sorted(finalizer_template["binding_sources"])
         and all(type(binding) is dict
                 and set(binding) == {"role", "selector"}
                 and binding["role"] in roles
                 and binding["selector"] in {"path", "absolute_path",
                                              "file_sha256", "object_sha256"}
                 for binding in finalizer_template["binding_sources"].values())
         and type(finalizer_template["python_hash_seed"]) is str
         and finalizer_template["python_hash_seed"].isdigit()
         and plan.get("systemd_run_policy") == SYSTEMD_RUN_POLICY,
         "exact finalizer template/transient unit policy")
    need(plan.get("core_service") == CORE_SERVICE, "core service frozen tuple")
    finalizer = plan.get("finalizer_service")
    need(type(finalizer) is dict and set(finalizer) == {"unit", "launch_mode",
         "invocation_binding", "expected_result", "expected_exec_main_code",
         "expected_exec_main_status", "expected_load_state",
         "expected_active_state", "expected_sub_state", "fragment_path"}
         and type(finalizer["unit"]) is str
         and finalizer["unit"].startswith("cm2-")
         and finalizer["unit"].endswith(".service")
         and finalizer["launch_mode"]
             == "EXPLICIT_USER_BUS_SYSTEMD_RUN_TRANSIENT_V1"
         and finalizer["invocation_binding"]
             == "CAPTURE_FINALIZER_ENV_AND_MATCH_POST_EXIT_SYSTEMD_SHOW"
         and finalizer["expected_result"] == "success"
         and finalizer["expected_exec_main_code"] == 1
         and finalizer["expected_exec_main_status"] == 0
         and finalizer["expected_load_state"] == "loaded"
         and finalizer["expected_active_state"] == "inactive"
         and finalizer["expected_sub_state"] == "dead"
         and finalizer["fragment_path"] ==
             f"/run/user/{os.getuid()}/systemd/transient/{finalizer['unit']}",
         "future finalizer complete service identity without prefilled invocation")
    return plan, plan_record


def validate_fresh_paths_under_lock(plan: dict[str, Any]) -> None:
    paths = [inside(path, absent=True) for path in plan["fresh_paths"].values()]
    role_paths = [inside(spec["path"], absent=True)
                  for spec in plan["role_map"].values()
                  if spec["kind"] in {"runtime_output", "fresh_directory"}]
    need(all(not path.exists() and not path.is_symlink()
             for path in paths + role_paths),
         "all formal fresh paths absent while publication lock held")


def external_record(path: Path) -> dict[str, Any]:
    need(path.is_absolute() and path.is_file() and not path.is_symlink(),
         "external regular runtime")
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
                         | getattr(os, "O_CLOEXEC", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "external runtime single-link")
        state = hashlib.sha256()
        while block := os.read(descriptor, 4 << 20):
            state.update(block)
        need(fingerprint(os.fstat(descriptor)) == fingerprint(before)
             and fingerprint(os.stat(path, follow_symlinks=False))
                 == fingerprint(before), "external runtime stable stat9")
        return {"path": str(path), "sha256": state.hexdigest(),
                "stat_fingerprint": fingerprint(before)}
    finally:
        os.close(descriptor)


def role_value(plan: dict[str, Any], plan_record: dict[str, Any],
               role: str, selector: str, stage: str) -> str:
    spec = plan["role_map"][role]
    path = inside(spec["path"], absent=selector in {"path", "absolute_path"}
        and spec["kind"] in {
        "runtime_output", "fresh_directory"})
    current_index = len(STAGES) if stage == "official_finalizer_service" \
        else STAGES.index(stage)
    available = -1 if spec["available_after"] == "preflight" \
        else STAGES.index(spec["available_after"])
    if selector in {"path", "absolute_path"}:
        return str(path.relative_to(ROOT)) if selector == "path" else str(path)
    need(spec["kind"] != "fresh_directory" and available < current_index,
         "binding role available only from verified predecessor:" + role)
    if spec["kind"] == "plan_cli":
        need(path == inside(plan_record["path"]), "plan role path")
        return plan_record["sha256"] if selector == "file_sha256" \
            else plan["plan_sha256"]
    if selector == "file_sha256":
        item = record(path)
        need(spec["file_sha256"] is None
             or item["sha256"] == spec["file_sha256"],
             "role current file pin:" + role)
        return item["sha256"]
    need(selector == "object_sha256" and type(spec["closure"]) is str,
         "role object selector contract:" + role)
    value, item = document(path, spec["closure"])
    need((spec["file_sha256"] is None or item["sha256"] == spec["file_sha256"])
         and (spec["object_sha256"] is None
              or value[spec["closure"]] == spec["object_sha256"])
         and (spec["schema"] is None or value.get("schema") == spec["schema"])
         and (spec["status"] is None or value.get("status") == spec["status"]),
         "role current object pin/schema/status:" + role)
    return value[spec["closure"]]


def make_environment(seed: str) -> dict[str, str]:
    return {"PATH": "/usr/bin:/bin", "HOME": "/nonexistent", "LANG": "C",
            "LC_ALL": "C", "TZ": "UTC", "PYTHONHASHSEED": seed}


def outer_runner_argv(runner: Path, python: Path, stage: str,
                      spec_path: Path, spec_record: dict[str, Any],
                      spec: dict[str, Any], pinset_path: Path,
                      pinset_record: dict[str, Any], pinset: dict[str, Any],
                      run_dir: Path, lock_fd: int) -> list[str]:
    values = [
        ("stage", stage), ("command-spec", str(spec_path.relative_to(ROOT))),
        ("pinset", str(pinset_path.relative_to(ROOT))),
        ("run-dir", str(run_dir.relative_to(ROOT))), ("python", str(python)),
        ("expect-runner-sha256", record(runner)["sha256"]),
        ("expect-python-sha256", external_record(python)["sha256"]),
        ("expect-command-spec-file-sha256", spec_record["sha256"]),
        ("expect-command-spec-object-sha256", spec["command_spec_sha256"]),
        ("expect-pinset-file-sha256", pinset_record["sha256"]),
        ("expect-pinset-object-sha256", pinset["pinset_sha256"]),
        ("publication-lock-fd", str(lock_fd)),
    ]
    answer = [str(python), "-I", "-B", str(runner)]
    for name, value in values:
        answer.extend(["--" + name, value])
    return answer


def generate_and_run_stage(plan: dict[str, Any], plan_record: dict[str, Any],
                           stage: str, lock_fd: int,
                           lock_value: dict[str, Any],
                           args: argparse.Namespace) -> dict[str, Any]:
    template_spec = plan["stage_templates"][stage]
    roles = plan["role_map"]
    bindings = {name: role_value(plan, plan_record, binding["role"],
                                  binding["selector"], stage)
                for name, binding in template_spec["binding_sources"].items()}
    bindings = dict(sorted(bindings.items()))
    command = expand_argv(template_spec["argv_template"], bindings)
    source_spec = plan["sources"][template_spec["source_role"]]
    source = inside(source_spec["path"])
    runner_spec = plan["sources"]["transaction_runner"]
    runner = inside(runner_spec["path"])
    python = Path(plan["python_runtime"]["path"])
    need(record(source)["sha256"] == source_spec["sha256"]
         and record(runner)["sha256"] == runner_spec["sha256"]
         and external_record(python)["sha256"]
             == plan["python_runtime"]["sha256"]
         and command[:4] == [str(python), "-I", "-B", str(source)],
         "frozen source/runtime and expanded inner command prefix")
    input_paths = sorted({roles[role]["path"]
                          for role in template_spec["input_roles"]})
    input_members = []
    for path in input_paths:
        item = record(inside(path))
        input_members.append({"path": path, "sha256": item["sha256"]})
    output_roots = [{"path": roles[item["role"]]["path"],
                     "exact_files": item["exact_files"]}
                    for item in template_spec["output_roots"]]
    output_documents = [{"path": roles[item["role"]]["path"],
                         "closure": item["closure"], "schema": item["schema"],
                         "status": item["status"]}
                        for item in template_spec["output_documents"]]
    lock_path = inside(plan["publication_lock"]["path"])
    lock_item = record(lock_path)
    lock_contract = {"path": lock_item["path"],
        "file_sha256": lock_item["sha256"],
        "object_sha256": lock_value["publication_lock_sha256"],
        "stat_fingerprint": fingerprint(os.fstat(lock_fd)), "fd": lock_fd,
        "schema": LOCK_SCHEMA, "status": LOCK_STATUS, "protocol": LOCK_PROTOCOL}
    control_root = inside(plan["launch_control_dir"])
    transaction_root = control_root / "transactions"
    if not transaction_root.exists():
        transaction_root.mkdir(mode=0o700)
        fsync_directory(transaction_root); fsync_directory(control_root)
    stage_control = transaction_root / stage
    need(not stage_control.exists() and not stage_control.is_symlink(),
         "fresh stage launch-control directory")
    stage_control.mkdir(mode=0o700)
    fsync_directory(stage_control); fsync_directory(transaction_root)
    pinset_body = {"schema": PINSET_SCHEMA, "status": PINSET_STATUS,
        "stage": stage, "runner_source_sha256": runner_spec["sha256"],
        "python_path": str(python), "python_sha256": plan["python_runtime"]["sha256"],
        "source_path": source_spec["path"], "source_sha256": source_spec["sha256"],
        "input_members": input_members, "formal_credit": 0,
        "manifest_authorized": False, "authority_minted": False}
    pinset = {**pinset_body, "pinset_sha256": digest(pinset_body)}
    pinset_path = stage_control / "pinset.json"
    write_json(pinset_path, pinset); pinset_record = record(pinset_path)
    environment = make_environment(template_spec["python_hash_seed"])
    spec_body = {"schema": SPEC_SCHEMA, "status": SPEC_STATUS, "stage": stage,
        "pinset_file_sha256": pinset_record["sha256"],
        "pinset_object_sha256": pinset["pinset_sha256"],
        "runner_source_sha256": runner_spec["sha256"],
        "python_path": str(python), "python_sha256": plan["python_runtime"]["sha256"],
        "source_path": source_spec["path"], "source_sha256": source_spec["sha256"],
        "input_paths": input_paths, "output_roots": output_roots,
        "output_documents": output_documents,
        "python_hash_seed": template_spec["python_hash_seed"],
        "environment": environment,
        "argv_template": template_spec["argv_template"],
        "argv_template_sha256": template_spec["argv_template_sha256"],
        "argv_bindings": bindings, "argv_bindings_sha256": digest(bindings),
        "expanded_argv": command, "expanded_argv_sha256": digest(command),
        "publication_lock": lock_contract,
        "timeout_seconds": template_spec["timeout_seconds"],
        "expected_stdout": template_spec["expected_stdout"],
        "formal_credit": 0, "manifest_authorized": False,
        "authority_minted": False}
    spec = {**spec_body, "command_spec_sha256": digest(spec_body)}
    spec_path = stage_control / "command_spec.json"
    write_json(spec_path, spec); spec_record = record(spec_path)
    run_dir = inside(plan["fresh_paths"][stage], absent=True)
    outer = outer_runner_argv(runner, python, stage, spec_path, spec_record,
        spec, pinset_path, pinset_record, pinset, run_dir, lock_fd)
    launch_body = {"schema": LAUNCH_SCHEMA,
        "status": "FROZEN_C27R2_V4_STAGE_LAUNCH__ZERO_CREDIT", "stage": stage,
        "plan_file_sha256": plan_record["sha256"],
        "plan_object_sha256": plan["plan_sha256"],
        "argv_template_sha256": template_spec["argv_template_sha256"],
        "argv_bindings_sha256": digest(bindings),
        "expanded_argv_sha256": digest(command),
        "outer_runner_argv": outer, "outer_runner_argv_sha256": digest(outer),
        "command_spec_file_sha256": spec_record["sha256"],
        "command_spec_object_sha256": spec["command_spec_sha256"],
        "pinset_file_sha256": pinset_record["sha256"],
        "pinset_object_sha256": pinset["pinset_sha256"],
        "publication_lock_object_sha256": lock_value["publication_lock_sha256"],
        "formal_credit": 0, "manifest_authorized": False,
        "authority_minted": False}
    launch = {**launch_body, "stage_launch_receipt_sha256": digest(launch_body)}
    write_json(stage_control / "stage_launch_receipt.json", launch)
    completed = subprocess.run(outer, cwd=ROOT, env=environment,
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        check=False, timeout=template_spec["timeout_seconds"] + 60,
        pass_fds=(lock_fd,))
    need(completed.returncode == 0 and completed.stderr == b""
         and run_dir.is_dir() and not run_dir.is_symlink(),
         "stage outer runner clean success:" + stage)
    run, _ = document(run_dir / "run_attestation.json", "run_attestation_sha256")
    expected_path = inside(roles[template_spec["expected_output_role"]]["path"])
    need(expected_path.exists() and run.get("schema") == RUN_SCHEMA
         and run.get("status") == RUN_STATUS and run.get("stage") == stage
         and run.get("argv_template_sha256")
             == template_spec["argv_template_sha256"]
         and run.get("argv_bindings_sha256") == digest(bindings)
         and run.get("expanded_argv_sha256") == digest(command)
         and run.get("outer_runner_argv_sha256") == digest(outer)
         and run.get("publication_lock_exclusive_inherited_and_held") is True,
         "four-digest stage launch/run closure:" + stage)
    return run


def finalizer_systemd_run_argv(plan: dict[str, Any],
                               plan_record: dict[str, Any],
                               finalizer: dict[str, Any],
                               lock_value: dict[str, Any],
                               args: argparse.Namespace) -> list[str]:
    spec = plan["finalizer_template"]
    bindings = {name: role_value(plan, plan_record, binding["role"],
                                  binding["selector"],
                                  "official_finalizer_service")
                for name, binding in spec["binding_sources"].items()}
    bindings = dict(sorted(bindings.items()))
    inner = expand_argv(spec["argv_template"], bindings)
    python = Path(plan["python_runtime"]["path"])
    source_spec = plan["sources"][spec["source_role"]]
    source = inside(source_spec["path"])
    need(inner[:4] == [str(python), "-I", "-B", str(source)]
         and record(source)["sha256"] == source_spec["sha256"],
         "finalizer expanded pinned inner argv")
    policy = plan["systemd_run_policy"]
    need(policy == SYSTEMD_RUN_POLICY, "frozen transient systemd-run policy")
    environment = make_environment(spec["python_hash_seed"])
    environment["CM2_FINALIZER_UNIT"] = finalizer["unit"]
    environment_property = " ".join(
        key + "=" + environment[key] for key in sorted(environment))
    command = ["/usr/bin/systemd-run", "--user", "--unit=" + finalizer["unit"],
        "--service-type=" + policy["service_type"],
        "--property=WorkingDirectory=" + policy["working_directory"],
        "--property=UMask=" + policy["umask"],
        "--property=NoNewPrivileges=yes",
        "--property=PrivateTmp=yes",
        "--property=ProtectSystem=" + policy["protect_system"],
        "--property=ReadWritePaths=" + policy["read_write_path"],
        "--property=Environment=" + environment_property,
        "--", *inner]
    control = inside(plan["launch_control_dir"])
    finalizer_control = control / "official_finalizer_service"
    need(not finalizer_control.exists() and not finalizer_control.is_symlink(),
         "fresh finalizer launch-control directory")
    finalizer_control.mkdir(mode=0o700)
    fsync_directory(finalizer_control); fsync_directory(control)
    body = {"schema": BASE + "finalizer-launch-receipt.v4",
        "status": "FROZEN_EXPLICIT_USER_BUS_SYSTEMD_RUN_FINALIZER__ZERO_CREDIT",
        "plan_file_sha256": plan_record["sha256"],
        "plan_object_sha256": plan["plan_sha256"],
        "argv_template_sha256": spec["argv_template_sha256"],
        "argv_bindings_sha256": digest(bindings),
        "expanded_finalizer_argv_sha256": digest(inner),
        "systemd_run_argv": command, "systemd_run_argv_sha256": digest(command),
        "systemd_run_policy": policy,
        "systemd_run_policy_sha256": digest(policy),
        "publication_lock_object_sha256": lock_value["publication_lock_sha256"],
        "formal_credit": 0, "manifest_authorized": False,
        "authority_minted": False}
    receipt = {**body, "finalizer_launch_receipt_sha256": digest(body)}
    write_json(finalizer_control / "finalizer_launch_receipt.json", receipt)
    return command


def verify_terminal(terminal: Path, plan: dict[str, Any],
                    state: dict[str, str],
                    publication_lock_object_sha256: str) -> dict[str, Any]:
    need(terminal.is_dir() and not terminal.is_symlink()
         and {path.name for path in terminal.iterdir()} == TERMINAL_FILES,
         "official terminal exact six-file inventory")
    need(capture(terminal / "PASS.lock")[0] == TERMINAL_PASS,
         "official terminal exact PASS bytes")
    payload_path = terminal / "payload_manifest.sha256"
    root_path = terminal / "root_manifest.sha256"
    payload = parse_manifest(payload_path)
    root = parse_manifest(root_path)
    payload_record = record(payload_path)
    root_record = record(root_path)
    receipt, receipt_record = document(terminal / "terminal_receipt.json",
                                        "terminal_receipt_sha256")
    replay, replay_record = document(terminal / "terminal_replay.json",
                                      "terminal_replay_sha256")
    chain, _ = document(terminal / "chain_status.json", "chain_status_sha256")
    finalizer = plan["finalizer_service"]
    observed_service = {**finalizer, "invocation_id": state["InvocationID"]}
    common = (receipt, replay, chain)
    need(receipt.get("schema") == TERMINAL_SCHEMA
         and replay.get("schema") == TERMINAL_REPLAY_SCHEMA
         and chain.get("schema") == CHAIN_SCHEMA
         and all(value.get("status") == TERMINAL_STATUS for value in common)
         and all(value.get("validator_negative_case_count") == 70
                 and value.get("publication_lock_preflight_case_count") == 8
                 and value.get("total_integrity_check_count") == 78
                 and "case_count" not in value for value in common)
         and all(value.get("publication_lock_object_sha256")
                 == publication_lock_object_sha256 for value in common)
         and all(value.get("required_finalizer_service_gate")
                 == observed_service for value in common)
         and all(value.get("filesystem_terminal_complete") is True
                 and value.get("authority_mint_is_joint_not_filesystem_only")
                     is True
                 and value.get("joint_service_gate_must_be_observed_after_finalizer_exit")
                     is True
                 and value.get("orphan_PASS_authority_eligible") is False
                 and value.get("formal_credit") == 0
                 and value.get("manifest_authorized") is False
                 and value.get("authority_minted") is False
                 and value.get("manifest_authorized_when_joint_gate_observed")
                     is True
                 and value.get("authority_minted_when_joint_gate_observed") is True
                 and value.get("CM2") == "NO-GO_FOR_CLAIM"
                 for value in common)
         and replay.get("terminal_receipt_object_sha256")
             == receipt["terminal_receipt_sha256"]
         and chain.get("terminal_receipt_object_sha256")
             == receipt["terminal_receipt_sha256"]
         and chain.get("terminal_replay_object_sha256")
             == replay["terminal_replay_sha256"]
         and all(value.get("terminal_payload_manifest_file_sha256")
                 == payload_record["sha256"] for value in common)
         and all(value.get("terminal_root_manifest_file_sha256")
                 == root_record["sha256"] for value in common)
         and payload and root and valid_sha(receipt_record["sha256"])
         and valid_sha(replay_record["sha256"]),
         "official terminal bytes/objects/manifests/dynamic invocation joint gate")
    return {"receipt": receipt, "replay": replay, "chain": chain}


def execute(args: argparse.Namespace) -> dict[str, Any]:
    need(FORMAL_EXECUTION_AUTHORIZED and BOUNDARY_CONTRACT_FROZEN_GO,
         "boundary v4 NO-GO; append-only boundary v5 independent GO required")
    plan, plan_record = validate_plan(args)
    lock_fd = -1
    try:
        lock_fd, lock_value = acquire_publication_lock(
            args, plan, plan_record)
        verify_service(service_show(CORE_SERVICE["unit"]), CORE_SERVICE, True)
        validate_fresh_paths_under_lock(plan)
        if not args.enable_execution:
            return {"schema": PREFLIGHT_SCHEMA,
                "status": "PASS_DISABLED_V4_PLAN_SOURCE_SERVICE_LOCK_AND_FRESH_PATH_PREFLIGHT",
                "plan_file_sha256": plan_record["sha256"],
                "plan_object_sha256": plan["plan_sha256"],
                "publication_lock_object_sha256":
                    lock_value["publication_lock_sha256"],
                "execution_enabled": False, "formal_credit": 0,
                "manifest_authorized": False, "authority_minted": False,
                "C27R2": "AUDIT_HOLD_UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM"}
        enable, enable_record = document(inside(args.enable_receipt),
                                         "enable_receipt_sha256")
        need(enable_record["sha256"] == args.expect_enable_file_sha256
             and enable["enable_receipt_sha256"]
                 == args.expect_enable_object_sha256
             and enable.get("schema") == ENABLE_SCHEMA
             and enable.get("status") == ENABLE_STATUS
             and enable.get("plan_file_sha256") == plan_record["sha256"]
             and enable.get("plan_object_sha256") == plan["plan_sha256"]
             and enable.get("watcher_source_sha256") == record(SELF)["sha256"]
             and enable.get("publication_lock_file_sha256")
                 == args.expect_publication_lock_file_sha256
             and enable.get("publication_lock_object_sha256")
                 == lock_value["publication_lock_sha256"]
             and enable.get("one_shot") is True
             and enable.get("formal_credit") == 0
             and enable.get("manifest_authorized") is False
             and enable.get("authority_minted") is False,
             "separately audited one-shot frozen launch envelope")
        for stage in STAGES:
            generate_and_run_stage(plan, plan_record, stage, lock_fd,
                                   lock_value, args)
        finalizer = plan["finalizer_service"]
        terminal = inside(plan["fresh_paths"]["official_terminal"], absent=True)
        need(not terminal.exists() and not terminal.is_symlink(),
             "official terminal absent immediately before finalizer start")
        before_service = service_show(finalizer["unit"])
        need(before_service["Id"] == finalizer["unit"]
             and before_service["LoadState"] == "not-found"
             and before_service["ActiveState"] == "inactive"
             and before_service["SubState"] == "dead"
             and before_service["InvocationID"] == ""
             and before_service["ExecStart"] == ""
             and before_service["FragmentPath"] == "",
             "finalizer transient unit identity absent before fresh invocation")
        # Handoff safety: release only after all absence/input checks.  The
        # finalizer must acquire the same pinned lock before any terminal write.
        fcntl.flock(lock_fd, fcntl.LOCK_UN)
        start_command = finalizer_systemd_run_argv(
            plan, plan_record, finalizer, lock_value, args)
        start = subprocess.run(start_command, cwd=ROOT,
            env=control_bus_environment(), stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=30)
        need(start.returncode == 0 and start.stderr == b"",
             "explicit transient finalizer systemd-run start")
        deadline = time.monotonic() + plan["finalizer_timeout_seconds"]
        while True:
            state = service_show(finalizer["unit"])
            if state["ActiveState"] == "inactive":
                break
            need(time.monotonic() < deadline, "finalizer service timeout")
            time.sleep(1)
        while True:
            try:
                fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                need(time.monotonic() < deadline,
                     "publication lock reacquire after finalizer")
                time.sleep(0.1)
        expected = {"unit": finalizer["unit"],
            "load_state": finalizer["expected_load_state"],
            "active_state": finalizer["expected_active_state"],
            "sub_state": finalizer["expected_sub_state"],
            "fragment_path": finalizer["fragment_path"],
            "result": finalizer["expected_result"],
            "exec_main_code": finalizer["expected_exec_main_code"],
            "exec_main_status": finalizer["expected_exec_main_status"]}
        inner_marker = start_command.index("--")
        expected_inner = start_command[inner_marker + 1:]
        verify_service(state, expected, True, expected_inner)
        need(not before_service["InvocationID"]
             or state["InvocationID"] != before_service["InvocationID"],
             "fresh finalizer invocation ID")
        terminal = inside(plan["fresh_paths"]["official_terminal"])
        terminal_objects = verify_terminal(terminal, plan, state,
            lock_value["publication_lock_sha256"])
        return {"schema": BASE + "watcher-completion.v4",
        "status": "PASS_C27R2_RELEASE_REPAIR_V4_JOINT_TERMINAL_AND_FINALIZER_SERVICE_GATE",
        "terminal_path": str(terminal.relative_to(ROOT)),
        "terminal_receipt_object_sha256": terminal_objects["receipt"][
            "terminal_receipt_sha256"],
        "terminal_replay_object_sha256": terminal_objects["replay"][
            "terminal_replay_sha256"],
        "chain_status_object_sha256": terminal_objects["chain"][
            "chain_status_sha256"],
        "finalizer_service_observation": state,
        "formal_credit": 0, "manifest_authorized": True,
        "authority_minted": True,
        "C27R2": "FORMAL_AUTHORITY_REPAIRED_BY_JOINT_GATE",
        "C28_C29": "UNAUTHORIZED_PENDING_FRESH_REBIND",
            "CM2": "NO-GO_FOR_CLAIM"}
    finally:
        if lock_fd >= 0:
            os.close(lock_fd)


def self_test() -> dict[str, Any]:
    need(FORMAL_EXECUTION_AUTHORIZED is False
         and BOUNDARY_CONTRACT_FROZEN_GO is False
         and STAGES[-1] == "anticipated_terminal"
         and "official_finalizer_service" not in STAGES,
         "development default disabled/finalizer external")
    try:
        _write_all(-1, b"x", lambda _fd, _raw: 0)
        raise Blocked("zero-progress writer unexpectedly accepted")
    except Blocked as error:
        need(str(error) == "write made positive progress",
             "zero-progress write fixture")
    need(expand_argv(["python", "-I", "-B", "${SOURCE}"],
                     {"SOURCE": "/tmp/source.py"})
         == ["python", "-I", "-B", "/tmp/source.py"],
         "canonical argv template fixture")
    bus_env = control_bus_environment()
    need(set(bus_env) == {"PATH", "LANG", "LC_ALL", "XDG_RUNTIME_DIR",
         "DBUS_SESSION_BUS_ADDRESS"}
         and bus_env["DBUS_SESSION_BUS_ADDRESS"]
             == "unix:path=" + bus_env["XDG_RUNTIME_DIR"] + "/bus",
         "control-plane user-bus environment distinct from child env")
    fixture_argv = ["/usr/bin/python3.12", "-I", "-B", "/tmp/finalizer.py"]
    expected = {"unit": "cm2-fixture.service", "load_state": "loaded",
        "active_state": "inactive", "sub_state": "dead",
        "fragment_path":
            "/run/user/1000/systemd/transient/cm2-fixture.service",
        "result": "success", "exec_main_code": 1,
        "exec_main_status": 0, "invocation_id": "a" * 32}
    verify_service({"Id": "cm2-fixture.service", "LoadState": "loaded",
        "ActiveState": "inactive", "SubState": "dead", "Result": "success",
        "ExecMainCode": "1", "ExecMainStatus": "0",
        "InvocationID": "a" * 32,
        "ExecStart": ("{ path=/usr/bin/python3.12 ; argv[]="
            "/usr/bin/python3.12 -I -B /tmp/finalizer.py ; ignore_errors=no }"),
        "FragmentPath":
            "/run/user/1000/systemd/transient/cm2-fixture.service"},
        expected, True, fixture_argv)
    with tempfile.TemporaryDirectory(dir=AUDIT,
            prefix="c27r2-watcher-v4-selftest-") as raw:
        root = Path(raw); future = root / "future"
        need(not future.exists() and future.parent == root,
             "real fresh-path fixture")
        source = root / "source"; source.write_bytes(b"source\n")
        plan_body = {"schema": PLAN_SCHEMA, "status": PLAN_STATUS}
        plan_value = {**plan_body, "plan_sha256": digest(plan_body)}
        plan_path = root / "plan.json"
        plan_path.write_bytes(canonical(plan_value) + b"\n")
        plan_item = record(plan_path)
        lock_body = {"schema": LOCK_SCHEMA, "status": LOCK_STATUS,
            "protocol": LOCK_PROTOCOL, "one_shot_launch_id": "self-test",
            "plan_file_sha256": plan_item["sha256"],
            "plan_object_sha256": plan_value["plan_sha256"],
            "formal_credit": 0, "manifest_authorized": False,
            "authority_minted": False}
        lock_value = {**lock_body, "publication_lock_sha256": digest(lock_body)}
        lock_path = root / "publication_lock.json"
        lock_path.write_bytes(canonical(lock_value) + b"\n")
        lock_args = argparse.Namespace(
            expect_publication_lock_file_sha256=record(lock_path)["sha256"],
            expect_publication_lock_object_sha256=
                lock_value["publication_lock_sha256"],
            expect_publication_lock_stat9_json=canonical(
                record(lock_path)["stat_fingerprint"]).decode("ascii"),
            publication_lock_path=str(lock_path.relative_to(ROOT)))
        lock_plan = {"plan_sha256": plan_value["plan_sha256"],
            "publication_lock": {"path": str(lock_path.relative_to(ROOT)),
                "schema": LOCK_SCHEMA, "status": LOCK_STATUS,
                "protocol": LOCK_PROTOCOL}}
        lock_fd, checked_lock = acquire_publication_lock(
            lock_args, lock_plan, plan_item)
        contender = os.open(lock_path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        rejected = False
        try:
            try:
                fcntl.flock(contender, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                rejected = True
            need(rejected and checked_lock == lock_value,
                 "real exclusive publication lock/contender rejection fixture")
        finally:
            os.close(contender); os.close(lock_fd)
        terminal = root / "terminal"; terminal.mkdir()
        source_item = record(source)
        payload_path = terminal / "payload_manifest.sha256"
        payload_path.write_bytes(
            f"{source_item['sha256']}  {source_item['path']}\n".encode("ascii"))
        payload_item = record(payload_path)
        root_path = terminal / "root_manifest.sha256"
        root_path.write_bytes(
            f"{payload_item['sha256']}  {payload_item['path']}\n".encode("ascii"))
        service = {"unit": "cm2-fixture.service",
            "launch_mode": "EXPLICIT_USER_BUS_SYSTEMD_RUN_TRANSIENT_V1",
            "invocation_binding":
                "CAPTURE_FINALIZER_ENV_AND_MATCH_POST_EXIT_SYSTEMD_SHOW",
            "expected_result": "success", "expected_exec_main_code": 1,
            "expected_exec_main_status": 0, "expected_load_state": "loaded",
            "expected_active_state": "inactive", "expected_sub_state": "dead",
            "fragment_path":
                "/run/user/1000/systemd/transient/cm2-fixture.service"}
        observed = {"Id": "cm2-fixture.service", "LoadState": "loaded",
            "ActiveState": "inactive", "SubState": "dead", "Result": "success",
            "ExecMainCode": "1", "ExecMainStatus": "0",
            "InvocationID": "b" * 32,
            "ExecStart": ("{ path=/usr/bin/python3.12 ; argv[]="
                "/usr/bin/python3.12 -I -B /tmp/finalizer.py ; ignore_errors=no }"),
            "FragmentPath":
                "/run/user/1000/systemd/transient/cm2-fixture.service"}
        gate = {**service, "invocation_id": observed["InvocationID"]}
        common = {"status": TERMINAL_STATUS,
            "required_finalizer_service_gate": gate,
            "filesystem_terminal_complete": True,
            "authority_mint_is_joint_not_filesystem_only": True,
            "joint_service_gate_must_be_observed_after_finalizer_exit": True,
            "orphan_PASS_authority_eligible": False,
            "validator_negative_case_count": 70,
            "publication_lock_preflight_case_count": 8,
            "total_integrity_check_count": 78,
            "publication_lock_object_sha256": "9" * 64,
            "terminal_payload_manifest_file_sha256": payload_item["sha256"],
            "terminal_root_manifest_file_sha256": record(root_path)["sha256"],
            "formal_credit": 0, "manifest_authorized": False,
            "authority_minted": False,
            "manifest_authorized_when_joint_gate_observed": True,
            "authority_minted_when_joint_gate_observed": True,
            "CM2": "NO-GO_FOR_CLAIM"}
        receipt_body = {"schema": TERMINAL_SCHEMA, **common}
        receipt = {**receipt_body,
            "terminal_receipt_sha256": digest(receipt_body)}
        replay_body = {"schema": TERMINAL_REPLAY_SCHEMA, **common,
            "terminal_receipt_object_sha256": receipt["terminal_receipt_sha256"]}
        replay = {**replay_body, "terminal_replay_sha256": digest(replay_body)}
        chain_body = {"schema": CHAIN_SCHEMA, **common,
            "terminal_receipt_object_sha256": receipt["terminal_receipt_sha256"],
            "terminal_replay_object_sha256": replay["terminal_replay_sha256"]}
        chain = {**chain_body, "chain_status_sha256": digest(chain_body)}
        (terminal / "terminal_receipt.json").write_bytes(canonical(receipt) + b"\n")
        (terminal / "terminal_replay.json").write_bytes(canonical(replay) + b"\n")
        (terminal / "chain_status.json").write_bytes(canonical(chain) + b"\n")
        (terminal / "PASS.lock").write_bytes(TERMINAL_PASS)
        checked = verify_terminal(terminal, {"finalizer_service": service},
                                  observed, "9" * 64)
        need(checked["receipt"]["terminal_receipt_sha256"]
             == receipt["terminal_receipt_sha256"],
             "real dynamic-invocation joint terminal fixture")
    return {"status": "PASS_C27R2_RELEASE_REPAIR_WATCHER_V4_SELF_TEST",
            "CM2": "NO-GO_FOR_CLAIM"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--enable-execution", action="store_true")
    for name in ("plan", "expect-plan-file-sha256",
        "expect-plan-object-sha256", "expect-self-sha256",
        "publication-lock-path", "expect-publication-lock-file-sha256",
        "expect-publication-lock-object-sha256",
        "expect-publication-lock-stat9-json", "enable-receipt",
        "expect-enable-file-sha256", "expect-enable-object-sha256"):
        parser.add_argument("--" + name)
    args = parser.parse_args()
    base_fields = ("plan", "expect_plan_file_sha256",
                   "expect_plan_object_sha256", "expect_self_sha256",
                   "publication_lock_path",
                   "expect_publication_lock_file_sha256",
                   "expect_publication_lock_object_sha256",
                   "expect_publication_lock_stat9_json")
    enable_fields = ("enable_receipt", "expect_enable_file_sha256",
                     "expect_enable_object_sha256")
    try:
        if args.self_test:
            need(not args.enable_execution
                 and all(getattr(args, field) is None
                         for field in base_fields + enable_fields),
                 "self-test no arguments")
            result = self_test()
        else:
            need(all(getattr(args, field) is not None for field in base_fields)
                 and (not args.enable_execution
                      or all(getattr(args, field) is not None
                             for field in enable_fields)),
                 "fully pinned preflight/enable contract")
            result = execute(args)
        sys.stdout.buffer.write(canonical({"CM2": result["CM2"],
            "formal_credit": 0, "status": result["status"]}) + b"\n")
        return 0
    except (Blocked, OSError, ValueError, KeyError, TypeError,
            subprocess.SubprocessError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
