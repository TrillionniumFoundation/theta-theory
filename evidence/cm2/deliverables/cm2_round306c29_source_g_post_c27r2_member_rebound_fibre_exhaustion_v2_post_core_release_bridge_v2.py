#!/usr/bin/env python3
"""Gate one exact C29-v2 core into a separate transient release service.

The bridge never creates a release target.  It waits for the pinned formal
core systemd unit and invocation, verifies the completed zero-credit receipt
and source provenance, computes the receipt's current file/object hashes, and
runs a no-output positive preflight over all eleven fresh release targets.
Only then does it launch a new transient systemd service whose direct
``ExecStart`` is the frozen workspace Python plus release watcher.  The gate
records the child's distinct InvocationID/MainPID and exact ExecStart in an
append-only handoff directory outside those eleven targets, then exits zero.
Missing/running predecessors wait; failed, replaced, or inconsistent
predecessors reject without touching a release path.
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
import time
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
AUDIT = ROOT / ".cm2-runtime/audit"
PYTHON = (AUDIT / "c30a-p0-closure-verifier-20260807/"
          "fresh-python-flint-0.9.0/bin/python")
PREFIX = "cm2_round306c29_source_g_post_c27r2_member_rebound_fibre_exhaustion_v2"
RELEASE_WATCHER = ROOT / f"deliverables/{PREFIX}_release_chain_watcher_v4.py"
RELEASE_COLD = ROOT / f"deliverables/{PREFIX}_release_cold_replay_runner_v4.py"
CORE_WATCHER = ROOT / f"deliverables/{PREFIX}_gated_dual_terminal_seed_watcher_v7.py"
CORE_UNIT = "cm2-c29-v2-core-v7-formal-r3-20260808t2242.service"
CORE_INVOCATION = "7faedf0ca66b41d486e1b7bd258cf11e"
CORE_CONTROL = AUDIT / "c29-v2-core-v7-formal-r3-20260808t2242-control"
RELEASE_WATCHER_SHA = "26816b95741fa621b49ef696b8f8616cca564d473fc4bcd3475c443e54848201"
RELEASE_COLD_SHA = "715601a73c4e9957cc3681313e8c11bffd22c3937e93b2a5b9ef8c9f924de27f"
PYTHON_SHA = "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118"
BASE = "cm2.round306c29.source-g-post-c27r2-member-rebound-fibre-exhaustion.v2."
CORE_SCHEMA = BASE + "gated-dual-terminal-seed-core-receipt.v1"
PINSET_SCHEMA = BASE + "gated-transaction-pinset.v1"
CORE_STATUS = (
    "PASS_C29_V2_DUAL_TERMINAL_ADAPTERS_SEED1_PRODUCER_SEED2_NO_IMPORT_"
    "VERIFIER_AND_34_ATTACKS__ZERO_CREDIT_PENDING_RELEASE_TERMINAL"
)
PREFLIGHT_STATUS = (
    "PASS_C29_V2_RELEASE_SOURCES_CORE_AND_ELEVEN_FRESH_PATHS_PREFLIGHT__"
    "NO_OUTPUT_ZERO_CREDIT"
)
CORE_PASS = b"PASS_C29_V2_DUAL_TERMINAL_SEED_CORE__ZERO_CREDIT\n"

CORE_SOURCES = {
    "builder": ROOT / f"deliverables/{PREFIX}_terminal_consumer_adapter_builder_v3.py",
    "adapter_verifier": ROOT / f"deliverables/{PREFIX}_terminal_consumer_adapter_independent_verifier_v1.py",
    "runner": ROOT / f"deliverables/{PREFIX}_transaction_runner_v3.py",
    "producer": ROOT / f"deliverables/{PREFIX}_producer_contract_v4.py",
    "verifier": ROOT / f"deliverables/{PREFIX}_independent_verifier_contract_v4.py",
    "attacks": ROOT / f"deliverables/{PREFIX}_coherent_attack_harness_contract_v5.py",
    "python": PYTHON,
    "watcher": CORE_WATCHER,
}
CORE_SOURCE_PINS = {
    "builder": "8381091ff952c6cc3673efe5789fda3773f55e4c9f990c124e567811d215538e",
    "adapter_verifier": "eccc4422a3ebba0ce505f4802bb508c3da007ae099a2b6f8f21b1347be5b3201",
    "runner": "bdd5e08e4d9a826bf09807a555fe6bb1ad0cd8556f35c828ba5b20d9bff48da5",
    "producer": "711ff12ea95b7a7376c8e02109ab66157431ea287a24c7c0824c948686109886",
    "verifier": "998badc7dad864d5e1c59c24b2c4a397ef08470c6e3bcbbf82c581a815692d1a",
    "attacks": "9a387a712033119c8aa615b5eaf544bf38778119eea18afa598b26cb351620f0",
    "python": PYTHON_SHA,
    "watcher": "6d3141ca0ab3f6e63b7c7a3af581b4537dd872cf860b7d6eb2e491d59ce68182",
}
STAGE_SEEDS = {
    "c27_adapter": "30662901", "c27_adapter_verifier": "30662902",
    "c28_adapter": "30662903", "c28_adapter_verifier": "30662904",
    "producer": "30662905", "independent_verifier": "30662906",
    "coherent_attacks": "30662907",
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


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns,
            value.st_uid, value.st_gid)


def file_sha(path: Path) -> str:
    absolute = path.absolute()
    need(absolute.resolve(strict=True) == absolute, "canonical pinned path")
    descriptor = os.open(absolute, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                         | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular singleton pinned file")
        state = hashlib.sha256()
        while block := os.read(descriptor, 4 << 20):
            state.update(block)
        after = os.fstat(descriptor)
        current = os.stat(absolute, follow_symlinks=False)
        need(fingerprint(before) == fingerprint(after) == fingerprint(current),
             "stable pinned file SHA/stat")
        return state.hexdigest()
    finally:
        os.close(descriptor)


def strict(payload: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(type(key) is str and key not in result, "unique JSON key")
            result[key] = value
        return result
    return json.loads(payload, object_pairs_hook=pairs,
                      parse_constant=lambda token: (_ for _ in ()).throw(
                          ValueError(token)))


def document(path: Path, closure: str) -> dict[str, Any]:
    need(path.is_file() and not path.is_symlink(), "canonical receipt file")
    payload = path.read_bytes()
    need(payload.endswith(b"\n") and not payload.endswith(b"\n\n"),
         "receipt newline")
    value = strict(payload[:-1])
    need(type(value) is dict and canonical(value) == payload[:-1],
         "canonical receipt JSON")
    body = dict(value)
    claim = body.pop(closure, None)
    need(valid_sha(claim) and claim == digest(body), "receipt object closure")
    return value


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace(
        "+00:00", "Z")


def write_once(path: Path, payload: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                         | getattr(os, "O_CLOEXEC", 0)
                         | getattr(os, "O_NOFOLLOW", 0), 0o400)
    try:
        offset = 0
        while offset < len(payload):
            offset += os.write(descriptor, payload[offset:])
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def write_json(path: Path, value: Any) -> None:
    write_once(path, canonical(value) + b"\n")


def release_paths(stem: str) -> dict[str, Path]:
    need(type(stem) is str
         and re.fullmatch(r"c29-v2-release-[a-z0-9][a-z0-9-]{7,100}", stem)
             is not None, "canonical release stem")
    result = {
        "control": AUDIT / (stem + "-control"),
        "cold_control": AUDIT / (stem + "-cold-control"),
        "cold_output": AUDIT / (stem + "-cold-output"),
        "cold_run": AUDIT / (stem + "-cold-run"),
        "evidence": AUDIT / (stem + "-evidence"),
        "release_attack_work": AUDIT / (stem + "-release-attack-work"),
        "release_attacks": AUDIT / (stem + "-release-attacks.json"),
        "manifests": AUDIT / (stem + "-manifests"),
        "outer": AUDIT / (stem + "-outer.json"),
        "seal": AUDIT / (stem + "-seal"),
        "terminal": AUDIT / (stem + "-terminal"),
    }
    need(len(result) == 11 and len(set(result.values())) == 11
         and all(path.parent == AUDIT for path in result.values()),
         "exact eleven release targets")
    return result


def targets_fresh(targets: dict[str, Path]) -> bool:
    return all(not path.exists() and not path.is_symlink()
               for path in targets.values())


def handoff_path(stem: str) -> Path:
    path = AUDIT / (stem + "-post-core-release-handoff-v2")
    need(path.parent == AUDIT, "handoff path topology")
    return path


def source_pins(expect_self: str) -> None:
    need(valid_sha(expect_self) and file_sha(SELF) == expect_self,
         "bridge self pin")
    need(file_sha(RELEASE_WATCHER) == RELEASE_WATCHER_SHA
         and file_sha(RELEASE_COLD) == RELEASE_COLD_SHA
         and set(CORE_SOURCES) == set(CORE_SOURCE_PINS)
         and all(file_sha(CORE_SOURCES[name]) == CORE_SOURCE_PINS[name]
                 for name in CORE_SOURCES), "bridge/release/core source pins")


def systemd_fields(unit: str) -> dict[str, str]:
    completed = subprocess.run([
        "/usr/bin/systemctl", "--user", "show", unit,
        "-p", "LoadState", "-p", "ActiveState", "-p", "SubState",
        "-p", "Result", "-p", "ExecMainCode", "-p", "ExecMainStatus",
        "-p", "InvocationID", "-p", "MainPID", "-p", "Transient",
        "-p", "ExecStart", "-p", "WorkingDirectory", "-p", "Environment"],
        cwd=ROOT,
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False)
    need(completed.returncode == 0 and completed.stderr == b"",
         "systemd unit query")
    return dict(line.split("=", 1) for line in
                completed.stdout.decode("ascii").splitlines() if "=" in line)


def classify_core(fields: dict[str, str]) -> str:
    invocation = fields.get("InvocationID", "")
    if fields.get("LoadState") in {"not-found", "error", "masked"}:
        return "WAIT"
    need(invocation in {"", CORE_INVOCATION}, "replaced core invocation")
    if (fields.get("ActiveState") == "active"
            and fields.get("SubState") == "exited"
            and fields.get("Result") == "success"
            and fields.get("ExecMainCode") in {"1", "exited"}
            and fields.get("ExecMainStatus") == "0"
            and invocation == CORE_INVOCATION):
        return "READY"
    need(fields.get("ActiveState") not in {"failed"}
         and fields.get("Result") not in {"exit-code", "signal", "timeout",
                                          "core-dump", "watchdog"}
         and not (fields.get("ExecMainStatus", "") not in {"", "0"}),
         "formal core failed")
    return "WAIT"


def wait_for_core(timeout_seconds: int, targets: dict[str, Path]) -> None:
    deadline = time.monotonic() + timeout_seconds
    while True:
        need(targets_fresh(targets), "release target appeared while waiting")
        if (CORE_CONTROL / "FAILED.lock").exists():
            raise Blocked("formal core FAILED.lock")
        phase = classify_core(systemd_fields(CORE_UNIT))
        if phase == "READY":
            return
        if time.monotonic() >= deadline:
            raise Blocked("timeout waiting exact formal core")
        time.sleep(min(15, max(0.1, deadline - time.monotonic())))


def validate_core() -> tuple[dict[str, Any], str, str]:
    need(CORE_CONTROL.parent == AUDIT and CORE_CONTROL.is_dir()
         and not CORE_CONTROL.is_symlink(), "exact core control")
    need(classify_core(systemd_fields(CORE_UNIT)) == "READY",
         "exact formal core clean success")
    core_path = CORE_CONTROL / "core_receipt.json"
    core = document(core_path, "core_receipt_sha256")
    pinset_path = CORE_CONTROL / "pinset.json"
    pinset = document(pinset_path, "pinset_sha256")
    stages = set(STAGE_SEEDS)
    need(core.get("schema") == CORE_SCHEMA and core.get("status") == CORE_STATUS
         and core.get("unit_name") == CORE_UNIT
         and core.get("systemd_invocation_id") == CORE_INVOCATION
         and core.get("source_pins") == CORE_SOURCE_PINS
         and pinset.get("schema") == PINSET_SCHEMA
         and pinset.get("source_pins") == CORE_SOURCE_PINS
         and core.get("pinset_file_sha256") == file_sha(pinset_path)
         and core.get("pinset_object_sha256") == pinset["pinset_sha256"]
         and core.get("stage_python_hash_seeds") == STAGE_SEEDS
         and pinset.get("stage_python_hash_seeds") == STAGE_SEEDS
         and core.get("producer_seed1") == STAGE_SEEDS["producer"]
         and core.get("verifier_seed2") == STAGE_SEEDS["independent_verifier"]
         and core.get("dual_real_hash_seeds")
             == [STAGE_SEEDS["producer"], STAGE_SEEDS["independent_verifier"]]
         and type(core.get("stage_command_spec_objects")) is dict
         and set(core["stage_command_spec_objects"]) == stages
         and all(valid_sha(value)
                 for value in core["stage_command_spec_objects"].values())
         and type(core.get("stage_run_attestation_objects")) is dict
         and set(core["stage_run_attestation_objects"]) == stages
         and all(valid_sha(value)
                 for value in core["stage_run_attestation_objects"].values())
         and core.get("formal_credit") == 0
         and core.get("manifest_authorized") is False
         and type(core.get("C29")) is str
         and core["C29"].startswith("UNAUTHORIZED_")
         and core.get("Source_W") == "UNCHANGED_BY_SOURCE_G_C29_V2_CORE"
         and core.get("CM2") == "NO-GO_FOR_CLAIM"
         and (CORE_CONTROL / "PASS.lock").read_bytes() == CORE_PASS
         and not (CORE_CONTROL / "FAILED.lock").exists(),
         "exact core receipt/pinset/provenance boundary")
    need(all(file_sha(CORE_SOURCES[name]) == CORE_SOURCE_PINS[name]
             for name in CORE_SOURCES), "current core source bytes")
    return core, file_sha(core_path), core["core_receipt_sha256"]


def preflight_command(args: argparse.Namespace, core_file: str,
                      core_object: str) -> list[str]:
    return [str(PYTHON), "-I", "-B", str(RELEASE_WATCHER),
            "--preflight-only", "--stem", args.stem,
            "--unit-name", args.unit_name,
            "--core-control-dir", str(CORE_CONTROL),
            "--expect-core-receipt-file-sha256", core_file,
            "--expect-core-receipt-object-sha256", core_object,
            "--expect-watcher-sha256", RELEASE_WATCHER_SHA,
            "--stage-timeout-seconds", str(args.stage_timeout_seconds)]


def clean_environment(seed: str) -> dict[str, str]:
    environment = dict(os.environ)
    environment.update({"PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
                        "PYTHONHASHSEED": seed})
    return environment


def positive_preflight(args: argparse.Namespace, targets: dict[str, Path],
                       core_file: str, core_object: str) -> None:
    need(targets_fresh(targets), "eleven release targets fresh before preflight")
    completed = subprocess.run(preflight_command(args, core_file, core_object),
        cwd=ROOT, env=clean_environment("30662997"), stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=args.preflight_timeout_seconds, check=False)
    expected = {"CM2": "NO-GO_FOR_CLAIM", "formal_credit": 0,
                "status": PREFLIGHT_STATUS}
    need(completed.returncode == 0 and completed.stderr == b""
         and completed.stdout == canonical(expected) + b"\n"
         and targets_fresh(targets),
         "positive release preflight with zero target creation")


def gate_service_identity(unit_name: str) -> str:
    invocation = os.environ.get("INVOCATION_ID")
    need(type(invocation) is str
         and re.fullmatch(r"[0-9a-f]{32}", invocation) is not None,
         "gate systemd invocation environment")
    fields = systemd_fields(unit_name)
    need(fields.get("InvocationID") == invocation
         and fields.get("ActiveState") == "activating"
         and fields.get("SubState") == "start"
         and fields.get("MainPID") == str(os.getpid())
         and fields.get("Transient") == "yes",
         "exact transient gate unit invocation and MainPID")
    return invocation


def release_command(args: argparse.Namespace, core_file: str,
                    core_object: str) -> list[str]:
    command = preflight_command(args, core_file, core_object)
    command.remove("--preflight-only")
    return command


def systemd_run_command(args: argparse.Namespace,
                        release: list[str]) -> list[str]:
    return ["/usr/bin/systemd-run", "--user", "--no-block", "--quiet",
            "--unit=" + args.release_unit_name,
            "--description=CM2 C29 v2 append-only release v4",
            "--property=Type=oneshot", "--property=RemainAfterExit=yes",
            "--property=WorkingDirectory=" + str(ROOT),
            "--property=TimeoutStartSec=infinity",
            "--setenv=PATH=/usr/bin:/bin", "--setenv=LANG=C",
            "--setenv=LC_ALL=C", "--setenv=PYTHONHASHSEED=30662998",
            "--setenv=PYTHONDONTWRITEBYTECODE=1", *release]


def failure_handoff(directory: Path, stage: str, error: BaseException) -> None:
    if not directory.exists():
        return
    body = {"schema": BASE + "post-core-release-handoff-failure.v2",
            "status": "FAILED_CLOSED_C29_V2_POST_CORE_RELEASE_HANDOFF__ZERO_CREDIT",
            "stage": stage, "error": f"{type(error).__name__}:{error}",
            "failed_at_utc": now(), "formal_credit": 0,
            "manifest_authorized": False, "C29": "UNAUTHORIZED",
            "CM2": "NO-GO_FOR_CLAIM"}
    value = dict(body)
    value["failure_receipt_sha256"] = digest(value)
    if not (directory / "failure_receipt.json").exists():
        write_json(directory / "failure_receipt.json", value)
    if not (directory / "FAILED.lock").exists():
        write_once(directory / "FAILED.lock",
                   b"FAILED_CLOSED_C29_V2_POST_CORE_RELEASE_HANDOFF\n")


def launch_release(args: argparse.Namespace, targets: dict[str, Path],
                   core_file: str, core_object: str) -> dict[str, Any]:
    handoff = handoff_path(args.stem)
    need(not handoff.exists() and not handoff.is_symlink(),
         "fresh bridge handoff path")
    gate_invocation = gate_service_identity(args.bridge_unit_name)
    prior = systemd_fields(args.release_unit_name)
    need(prior.get("LoadState") == "not-found"
         and prior.get("InvocationID", "") == "",
         "fresh transient release unit name")
    release = release_command(args, core_file, core_object)
    launcher = systemd_run_command(args, release)
    stage = "handoff_spec"
    handoff.mkdir(mode=0o700)
    try:
        spec_body = {
            "schema": BASE + "post-core-release-launch-spec.v2",
            "status": "PASS_C29_V2_POST_CORE_RELEASE_LAUNCH_SPEC__ZERO_CREDIT",
            "created_at_utc": now(), "bridge_unit_name": args.bridge_unit_name,
            "bridge_invocation_id": gate_invocation,
            "release_unit_name": args.release_unit_name,
            "release_command": release, "systemd_run_command": launcher,
            "working_directory": str(ROOT),
            "environment": {"PATH": "/usr/bin:/bin", "LANG": "C",
                            "LC_ALL": "C", "PYTHONHASHSEED": "30662998",
                            "PYTHONDONTWRITEBYTECODE": "1"},
            "core_unit_name": CORE_UNIT, "core_invocation_id": CORE_INVOCATION,
            "core_receipt_file_sha256": core_file,
            "core_receipt_object_sha256": core_object,
            "source_pins": {"bridge": args.expect_bridge_sha256,
                            "release_watcher": RELEASE_WATCHER_SHA,
                            "release_cold": RELEASE_COLD_SHA,
                            **{"core_" + name: value
                               for name, value in CORE_SOURCE_PINS.items()}},
            "release_targets": {name: str(path.relative_to(ROOT))
                                for name, path in sorted(targets.items())},
            "formal_credit": 0, "manifest_authorized": False,
            "C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM"}
        spec = dict(spec_body)
        spec["launch_spec_sha256"] = digest(spec)
        spec_path = handoff / "launch_spec.json"
        write_json(spec_path, spec)
        stage = "systemd_run"
        completed = subprocess.run(launcher, cwd=ROOT,
            env=clean_environment("30662999"), stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60,
            check=False)
        need(completed.returncode == 0 and completed.stdout == b""
             and completed.stderr == b"", "clean no-block systemd-run")
        stage = "child_identity"
        deadline = time.monotonic() + 30
        child: dict[str, str] | None = None
        while time.monotonic() < deadline:
            observed = systemd_fields(args.release_unit_name)
            invocation = observed.get("InvocationID", "")
            if (re.fullmatch(r"[0-9a-f]{32}", invocation) is not None
                    and observed.get("MainPID", "") not in {"", "0"}):
                child = observed
                break
            time.sleep(0.1)
        need(child is not None, "release child InvocationID/MainPID")
        expected_exec = ("{ path=" + str(PYTHON) + " ; argv[]="
                         + " ".join(release) + " ; ignore_errors=no ;")
        expected_environment = {
            "PATH=/usr/bin:/bin", "LANG=C", "LC_ALL=C",
            "PYTHONHASHSEED=30662998", "PYTHONDONTWRITEBYTECODE=1"}
        need(child.get("LoadState") == "loaded"
             and child.get("Transient") == "yes"
             and child.get("ActiveState") in {"activating", "active"}
             and child.get("SubState") in {"start", "running", "exited"}
             and child.get("WorkingDirectory") == str(ROOT)
             and child.get("ExecStart", "").startswith(expected_exec)
             and set(child.get("Environment", "").split()) == expected_environment,
             "exact direct transient release ExecStart/environment")
        child_invocation = child["InvocationID"]
        child_pid = child["MainPID"]
        time.sleep(0.25)
        confirm = systemd_fields(args.release_unit_name)
        need(confirm.get("InvocationID") == child_invocation
             and confirm.get("ExecStart") == child.get("ExecStart")
             and confirm.get("WorkingDirectory") == str(ROOT),
             "stable child invocation/ExecStart confirmation")
        stage = "handoff_receipt"
        receipt_body = {
            "schema": BASE + "post-core-release-handoff-receipt.v2",
            "status": "PASS_C29_V2_POST_CORE_RELEASE_V4_TRANSIENT_CHILD_STARTED__ZERO_CREDIT",
            "completed_at_utc": now(), "bridge_unit_name": args.bridge_unit_name,
            "bridge_invocation_id": gate_invocation,
            "release_unit_name": args.release_unit_name,
            "release_invocation_id": child_invocation,
            "release_main_pid_at_handoff": child_pid,
            "release_exec_start_sha256": hashlib.sha256(
                child["ExecStart"].encode("ascii")).hexdigest(),
            "release_exec_start": child["ExecStart"],
            "launch_spec_file_sha256": file_sha(spec_path),
            "launch_spec_object_sha256": spec["launch_spec_sha256"],
            "core_unit_name": CORE_UNIT, "core_invocation_id": CORE_INVOCATION,
            "core_receipt_file_sha256": core_file,
            "core_receipt_object_sha256": core_object,
            "eleven_targets_fresh_at_preflight": True,
            "formal_credit": 0, "manifest_authorized": False,
            "C29": "UNAUTHORIZED_PENDING_RELEASE_TERMINAL",
            "Source_W": "UNCHANGED", "CM2": "NO-GO_FOR_CLAIM"}
        receipt = dict(receipt_body)
        receipt["handoff_receipt_sha256"] = digest(receipt)
        write_json(handoff / "handoff_receipt.json", receipt)
        write_once(handoff / "PASS.lock",
                   b"PASS_C29_V2_POST_CORE_RELEASE_V4_TRANSIENT_CHILD_HANDOFF__ZERO_CREDIT\n")
        return receipt
    except BaseException as error:
        failure_handoff(handoff, stage, error)
        raise


def execute(args: argparse.Namespace) -> dict[str, Any]:
    source_pins(args.expect_bridge_sha256)
    targets = release_paths(args.stem)
    handoff = handoff_path(args.stem)
    need(targets_fresh(targets)
         and not handoff.exists() and not handoff.is_symlink(),
         "initial eleven release targets and handoff fresh")
    wait_for_core(args.wait_timeout_seconds, targets)
    _, core_file, core_object = validate_core()
    positive_preflight(args, targets, core_file, core_object)
    source_pins(args.expect_bridge_sha256)
    _, current_file, current_object = validate_core()
    need((current_file, current_object) == (core_file, core_object)
         and targets_fresh(targets), "post-preflight core/target stability")
    if args.preflight_only:
        return {"status":
                "PASS_C29_V2_POST_CORE_RELEASE_BRIDGE_V2_PREFLIGHT__"
                "NO_OUTPUT_ZERO_CREDIT"}
    launch_release(args, targets, core_file, core_object)
    return {"status":
            "PASS_C29_V2_POST_CORE_RELEASE_BRIDGE_V2_HANDOFF__ZERO_CREDIT"}


def self_test() -> dict[str, Any]:
    targets = release_paths("c29-v2-release-bridge-v2-self-test-targets")
    ready = {"LoadState": "loaded", "ActiveState": "active",
             "SubState": "exited", "Result": "success",
             "ExecMainCode": "exited", "ExecMainStatus": "0",
             "InvocationID": CORE_INVOCATION}
    running = {**ready, "ActiveState": "activating", "SubState": "start",
               "ExecMainCode": "0"}
    need(len(targets) == 11 and classify_core(ready) == "READY"
         and classify_core(running) == "WAIT"
         and set(CORE_SOURCES) == set(CORE_SOURCE_PINS)
         and all(file_sha(CORE_SOURCES[name]) == CORE_SOURCE_PINS[name]
                 for name in CORE_SOURCES)
         and file_sha(RELEASE_WATCHER) == RELEASE_WATCHER_SHA
         and file_sha(RELEASE_COLD) == RELEASE_COLD_SHA,
         "bridge positive fixtures")
    failed_rejected = replaced_rejected = False
    try:
        classify_core({**running, "Result": "exit-code", "ExecMainStatus": "2"})
    except Blocked:
        failed_rejected = True
    try:
        classify_core({**running, "InvocationID": "f" * 32})
    except Blocked:
        replaced_rejected = True
    need(failed_rejected and replaced_rejected,
         "bridge failure/replacement fixtures")
    return {"status": "PASS_C29_V2_POST_CORE_RELEASE_BRIDGE_V2_SELF_TEST",
            "formal_credit": 0, "C29": "UNAUTHORIZED",
            "CM2": "NO-GO_FOR_CLAIM"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--stem")
    parser.add_argument("--unit-name")
    parser.add_argument("--expect-bridge-sha256")
    parser.add_argument("--wait-timeout-seconds", type=int, default=604_800)
    parser.add_argument("--preflight-timeout-seconds", type=int, default=3_600)
    parser.add_argument("--stage-timeout-seconds", type=int, default=86_400)
    args = parser.parse_args()
    try:
        if args.self_test:
            need(not args.preflight_only and args.stem is None
                 and args.unit_name is None and args.expect_bridge_sha256 is None,
                 "self-test arguments")
            result = self_test()
        else:
            need(type(args.stem) is str and type(args.unit_name) is str
                 and args.unit_name.endswith(".service")
                 and valid_sha(args.expect_bridge_sha256)
                 and 1 <= args.wait_timeout_seconds <= 1_209_600
                 and 600 <= args.preflight_timeout_seconds <= 14_400
                 and 600 <= args.stage_timeout_seconds <= 172_800,
                 "bridge run arguments")
            result = execute(args)
        sys.stdout.buffer.write(canonical({"CM2": "NO-GO_FOR_CLAIM",
            "formal_credit": 0, "status": result["status"]}) + b"\n")
        return 0
    except (Blocked, OSError, ValueError, KeyError, TypeError,
            subprocess.SubprocessError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
