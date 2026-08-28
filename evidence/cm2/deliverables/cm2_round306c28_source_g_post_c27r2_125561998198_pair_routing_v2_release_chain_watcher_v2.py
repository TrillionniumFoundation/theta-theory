#!/usr/bin/env python3
"""Fail-closed gated watcher for the complete C28-v2 release DAG.

All formal-core receipt hashes are launch-time parameters.  Before any release
path exists, the watcher verifies the completed core service, immutable C27R2
predecessor, frozen core/release sources, seven self-tests, one positive cold
preflight, and ten fresh targets.  A real systemd-scoped run then executes
cold replay, 32 release attacks, evidence, manifests, independent outer,
conditional seal, and finally independent terminal byte replay.  Only that
last stage may mint C28; C29 is never started and CM2 remains NO-GO.
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
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
AUDIT = ROOT / ".cm2-runtime/audit"
PYTHON = Path("/usr/bin/python3.12")
BASE_NAME = (
    "cm2_round306c28_source_g_post_c27r2_125561998198_pair_routing_v2"
)
PROGRAMS = {
    "cold": ROOT / ("deliverables/" + BASE_NAME
                    + "_release_cold_replay_runner_v1.py"),
    "attacks": ROOT / ("deliverables/" + BASE_NAME
                       + "_release_only_attack_harness_v2.py"),
    "evidence": ROOT / ("deliverables/" + BASE_NAME
                        + "_release_evidence_bundle_builder_v1.py"),
    "manifests": ROOT / ("deliverables/" + BASE_NAME
                         + "_release_manifest_builder_v1.py"),
    "outer": ROOT / ("deliverables/" + BASE_NAME
                     + "_release_outer_verifier_v1.py"),
    "seal": ROOT / ("deliverables/" + BASE_NAME
                    + "_release_terminal_seal_builder_v1.py"),
    "terminal": ROOT / ("deliverables/" + BASE_NAME
                        + "_terminal_byte_replay_v1.py"),
}
PROGRAM_PINS = {
    "cold": "6f5dddc45b101560995e5f24b7719672e3aab5e3c340605c2cae88b9b03cb0d9",
    "attacks": "2ac993f90b27f5553fe889e82ba95274643479040a901ce11323d8d1511a059e",
    "evidence": "e0088877c875450873fd23d4355eb198e966e744297a4b42276503231115b116",
    "manifests": "4e2234e1cdbe338d711415906d731acab2951fbf135f5fc5be1220f3d123b431",
    "outer": "faa70adc417b3203a680bb607f6a542ff67e94f88431d5b2967616ae172935f3",
    "seal": "320b941b4bb50920c4c73f4cff9aaf0b72d44db1c8e05f9e4009369ac401f99e",
    "terminal": "46381fd883a9a1069e678bdb5cf9a46b6ccb57a96c3749b6a7109c14fbc3b770",
    "python": "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118",
}
CORE_SOURCE_PINS = {
    "producer": "364610cfa465601ac99fcd5ee3528ee5da791fcb5fb1c9ab27ff38966d211205",
    "independent_verifier":
        "7ca21d0e02f95afc1a8fc9635c3aa31bb290b8499f28860f8f8ae095b451cb04",
    "coherent_attacks":
        "ea09933a45c7b00a268edd961336069b43c15561a1e6c345fdadb160c02e50c1",
    "transaction_runner":
        "d37ebb999f226d6af65338b9ccc5c40ace70de80bf1db32cd4e129740d740ae3",
    "watcher":
        "4c9d353c7b1214c43a437f7dfc9bbd0ac82f24a669c1ae7f11b378ac2a7ca1ea",
}
PREFIX = (
    "cm2.round306c28.source-g-post-c27r2-125561998198-pair-routing.v2."
)
PINSET_SCHEMA = PREFIX + "release-chain-pinset.v1"
CORE_PINSET_SCHEMA = PREFIX + "gated-transaction-pinset.v1"
CORE_SCHEMA = PREFIX + "gated-dual-seed-core-receipt.v1"
CORE_STATUS = (
    "PASS_C27R2_TERMINAL_ADAPTER_DUAL_TRUE_SEED_THREE_FILE_CANDIDATES_"
    "TWO_NO_IMPORT_VERIFIERS_AND_26_ATTACKS__ZERO_CREDIT_PENDING_RELEASE"
)
EXPECTED = {
    "members": 502_204, "post_components": 43_684, "blocks": 256,
    "shards": 32_896, "total_pairs": 126_104_177_706,
    "within_pairs": 542_179_508, "cross_pairs": 125_561_998_198,
}
C27 = {
    "root": "1f65a624c889773e3104c4311788fc06be04d6ca92e033205074b8cc7f5b27fc",
    "receipt_file": "feccb0b9290bd82ac1d8e78e8e7a21d4f25e0ca3aa3556cc3f0bb6007f61c3dd",
    "receipt_object": "8afbd127c9518f569c2f7b3edcdbe9e0ebf77d88bcca855822e58d21e5cfe782",
    "replay_file": "b480df4b8caaf9876a48720f92a8fb6d86e2b1b5966bcc71b0022c5e49fc12ee",
    "replay_object": "216d2592c49b0302de0042677ce54c96cd5ad1fcb32231da02b39c003cb837e8",
    "pass": "5fe4140b3e8f38196e9ca68cd336ae29be1c8847c7685526f08aa4d7173d7348",
}
EXPECTED_STATUS = {
    "cold": (
        "PASS_FRESH_NO_IMPORT_C28_PAIR_ROUTING_COLD_BYTE_REPLAY_WITH_ALL_"
        "DECLARED_CORE_INPUT_PRE_POST_SHA_STAT__ZERO_CREDIT"),
    "attacks": (
        "PASS_BASELINE_AND_32_OF_32_RELEASE_ONLY_ATTACKS_REJECTED_FAIL_"
        "CLOSED__ZERO_CREDIT_PENDING_EVIDENCE_MANIFEST_OUTER_AND_TERMINAL"),
    "evidence": (
        "PASS_C28_CORE_COLD_32_RELEASE_ATTACKS_AND_ALL_AUTHORITY_INPUT_"
        "SHA_STAT_EVIDENCE__ZERO_CREDIT"),
    "manifests": (
        "PASS_C28_MANIFEST_FIRST_PAYLOAD_AND_C27R2_ROOT_CLOSURE__ZERO_"
        "CREDIT_PENDING_OUTER_SEAL_AND_TERMINAL_REPLAY"),
    "outer": (
        "PASS_INDEPENDENT_C28_FULL_PAIR_LEDGER_MANIFEST_COLD_AND_32_RELEASE_"
        "ATTACK_CHECK__CONDITIONAL_ZERO_CREDIT"),
    "seal": (
        "PASS_CONDITIONAL_C28_TERMINAL_SEAL_CANDIDATE__ZERO_CREDIT_PENDING_"
        "INDEPENDENT_BYTE_REPLAY"),
    "terminal": (
        "PASS_C28_TERMINAL_BYTE_REPLAY__FORMAL_C28_PAIR_ROUTING_AUTHORITY_"
        "MINTED"),
}
TERMINAL_STATUS = EXPECTED_STATUS["terminal"]
TERMINAL_PASS = b"PASS_C28_PAIR_ROUTING_V2_TERMINAL_BYTE_REPLAY__C29_UNAUTHORIZED\n"
WATCH_PASS = b"PASS_C28_RELEASE_CHAIN_TERMINAL__C29_UNAUTHORIZED\n"


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
    return (type(value) is str and len(value) == 64
            and all(character in "0123456789abcdef" for character in value))


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace(
        "+00:00", "Z")


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns,
            value.st_uid, value.st_gid)


def file_sha(path: Path) -> str:
    absolute = path.absolute()
    need(absolute.resolve(strict=True) == absolute,
         "canonical path:" + str(path))
    fd = os.open(absolute, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                 | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular singleton:" + str(path))
        state = hashlib.sha256()
        while block := os.read(fd, 4 << 20):
            state.update(block)
        need(fingerprint(before) == fingerprint(os.fstat(fd))
             == fingerprint(os.stat(absolute, follow_symlinks=False)),
             "stable fd/path SHA/stat:" + str(path))
        return state.hexdigest()
    finally:
        os.close(fd)


def strict_load(payload: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(type(key) is str and key not in result,
                 "unique JSON key:" + str(key))
            result[key] = value
        return result
    return json.loads(payload, object_pairs_hook=pairs,
                      parse_constant=lambda token: (_ for _ in ()).throw(
                          ValueError(token)))


def document(path: Path, closure: str) -> dict[str, Any]:
    payload = path.read_bytes()
    need(payload.endswith(b"\n") and not payload.endswith(b"\n\n"),
         "JSON newline:" + str(path))
    value = strict_load(payload[:-1])
    need(type(value) is dict and canonical(value) == payload[:-1],
         "canonical JSON:" + str(path))
    body = dict(value)
    claim = body.pop(closure, None)
    need(valid_sha(claim) and claim == digest(body),
         "object closure:" + str(path))
    return value


def write_once(path: Path, payload: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                 | getattr(os, "O_NOFOLLOW", 0), 0o400)
    try:
        offset = 0
        while offset < len(payload):
            offset += os.write(fd, payload[offset:])
        os.fsync(fd)
    finally:
        os.close(fd)


def write_json(path: Path, value: Any) -> None:
    write_once(path, canonical(value) + b"\n")


def service_success(unit: str, invocation: str) -> None:
    need(type(unit) is str and unit.endswith(".service")
         and type(invocation) is str
         and re.fullmatch(r"[0-9a-f]{32}", invocation) is not None,
         "core unit/invocation syntax")
    completed = subprocess.run([
        "/usr/bin/systemctl", "--user", "show", unit,
        "-p", "ActiveState", "-p", "SubState", "-p", "Result",
        "-p", "ExecMainCode", "-p", "ExecMainStatus", "-p", "InvocationID",
    ], cwd=ROOT, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
       stderr=subprocess.PIPE, check=False)
    need(completed.returncode == 0 and completed.stderr == b"",
         "query formal core service")
    fields = dict(line.split("=", 1) for line in
                  completed.stdout.decode("ascii").splitlines() if "=" in line)
    need(fields.get("ActiveState") == "active"
         and fields.get("SubState") == "exited"
         and fields.get("Result") == "success"
         and fields.get("ExecMainCode") in {"1", "exited"}
         and fields.get("ExecMainStatus") == "0"
         and fields.get("InvocationID") == invocation,
         "unique formal core clean success")


def release_paths(stem: str) -> dict[str, Path]:
    need(type(stem) is str
         and re.fullmatch(r"c28-v2-release-[a-z0-9][a-z0-9-]{7,100}", stem)
             is not None, "canonical C28 release stem")
    values = {
        "control": AUDIT / (stem + "-control"),
        "cold_control": AUDIT / (stem + "-cold-control"),
        "cold_output": AUDIT / (stem + "-cold-output"),
        "cold_run": AUDIT / (stem + "-cold-run"),
        "release_attacks": AUDIT / (stem + "-release-attacks"),
        "evidence": AUDIT / (stem + "-evidence"),
        "manifests": AUDIT / (stem + "-manifests"),
        "outer": AUDIT / (stem + "-outer.json"),
        "seal": AUDIT / (stem + "-seal"),
        "terminal": AUDIT / (stem + "-terminal"),
    }
    need(len(values) == 10 and len(set(values.values())) == 10
         and all(path.parent == AUDIT for path in values.values()),
         "ten-path release topology")
    return values


def source_pins(expect_self: str) -> dict[str, str]:
    need(valid_sha(expect_self) and file_sha(SELF) == expect_self,
         "watcher self pin")
    observed = {name: file_sha(path) for name, path in PROGRAMS.items()}
    observed["python"] = file_sha(PYTHON)
    need(observed == PROGRAM_PINS, "frozen release source/Python pins")
    return {**observed, "watcher": expect_self}


def self_tests() -> dict[str, str]:
    result: dict[str, str] = {}
    for index, (name, program) in enumerate(PROGRAMS.items()):
        completed = subprocess.run([
            str(PYTHON), "-I", "-B", str(program), "--self-test",
        ], cwd=ROOT, env={"PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
                         "PYTHONHASHSEED": str(30662870 + index)},
           stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
           stderr=subprocess.PIPE, timeout=300, check=False)
        need(completed.returncode == 0 and completed.stderr == b""
             and completed.stdout.endswith(b"\n"),
             "release source self-test:" + name)
        value = strict_load(completed.stdout[:-1])
        need(value.get("CM2") == "NO-GO_FOR_CLAIM"
             and value.get("formal_credit") == 0
             and type(value.get("status")) is str
             and canonical(value) + b"\n" == completed.stdout,
             "canonical self-test stdout:" + name)
        result[name] = hashlib.sha256(completed.stdout).hexdigest()
    return result


def validate_predecessor(path: Path) -> None:
    need(path.parent == AUDIT and path.is_dir() and not path.is_symlink()
         and {entry.name for entry in path.iterdir()} == {
             "PASS.lock", "chain_status.json", "payload_manifest.sha256",
             "root_manifest.sha256", "terminal_receipt.json",
             "terminal_replay.json"}, "exact C27R2 terminal inventory")
    receipt = document(path / "terminal_receipt.json", "terminal_receipt_sha256")
    replay = document(path / "terminal_replay.json", "terminal_replay_sha256")
    need(file_sha(path / "root_manifest.sha256") == C27["root"]
         and file_sha(path / "terminal_receipt.json") == C27["receipt_file"]
         and receipt["terminal_receipt_sha256"] == C27["receipt_object"]
         and file_sha(path / "terminal_replay.json") == C27["replay_file"]
         and replay["terminal_replay_sha256"] == C27["replay_object"]
         and file_sha(path / "PASS.lock") == C27["pass"]
         and receipt.get("authority_minted") is True
         and receipt.get("manifest_authorized") is True,
         "immutable C27R2 terminal pins")


def core_context(args: argparse.Namespace) -> dict[str, Any]:
    service_success(args.core_unit, args.expect_core_invocation_id)
    control = Path(args.core_control_dir).absolute()
    need(control.parent == AUDIT and control.is_dir() and not control.is_symlink(),
         "formal core control directory")
    core_path = control / "core_receipt.json"
    core = document(core_path, "core_receipt_sha256")
    need(file_sha(core_path) == args.expect_core_receipt_file_sha256
         and core["core_receipt_sha256"]
             == args.expect_core_receipt_object_sha256
         and core.get("schema") == CORE_SCHEMA and core.get("status") == CORE_STATUS
         and core.get("exact_math") == EXPECTED
         and core.get("formal_credit") == 0
         and core.get("manifest_authorized") is False
         and core.get("C28") == "UNAUTHORIZED_PENDING_RELEASE_TERMINAL"
         and core.get("C29") == "UNAUTHORIZED"
         and core.get("CM2") == "NO-GO_FOR_CLAIM"
         and file_sha(control / "PASS.lock") == args.expect_core_pass_sha256,
         "exact terminal-pending core boundary")
    pinset = document(control / "pinset.json", "pinset_sha256")
    need(pinset.get("schema") == CORE_PINSET_SCHEMA
         and pinset.get("formal_credit") == 0
         and pinset.get("manifest_authorized") is False,
         "core pinset boundary")
    for name, expected in CORE_SOURCE_PINS.items():
        need(pinset.get("source_pins", {}).get(name) == expected,
             "frozen core source pin:" + name)
    expected_targets = {
        "control", "adapter", "adapter_verification", "adapter_run",
        "adapter_verifier_run", "seed1_candidate", "seed1_run",
        "seed2_candidate", "seed2_run", "verifier1_output",
        "verifier1_run", "verifier2_output", "verifier2_run",
        "attack_work", "attack_run",
    }
    raw_targets = pinset.get("targets", {})
    need(type(raw_targets) is dict and set(raw_targets) == expected_targets,
         "exact core target inventory")
    targets = {name: (ROOT / raw).absolute() for name, raw in raw_targets.items()}
    need(targets["control"] == control
         and len(set(targets.values())) == len(targets)
         and all(path.parent == AUDIT and path.is_dir() and not path.is_symlink()
                 for path in targets.values()), "live core target topology")
    predecessor = Path(pinset.get("predecessor", {}).get("terminal_dir", "")).absolute()
    validate_predecessor(predecessor)
    predecessor_pins = pinset["predecessor"]
    need(predecessor_pins.get("terminal_root_sha256") == C27["root"]
         and predecessor_pins.get("terminal_receipt_file_sha256")
             == C27["receipt_file"]
         and predecessor_pins.get("terminal_receipt_object_sha256")
             == C27["receipt_object"]
         and predecessor_pins.get("terminal_replay_file_sha256")
             == C27["replay_file"]
         and predecessor_pins.get("terminal_replay_object_sha256")
             == C27["replay_object"]
         and predecessor_pins.get("terminal_pass_lock_sha256") == C27["pass"],
         "core pinset exact predecessor")
    return {"control": control, "core": core, "core_path": core_path,
            "pinset": pinset, "targets": targets,
            "core_dirs": sorted(targets.values()), "predecessor": predecessor}


def repeated(flag: str, paths: list[Path]) -> list[str]:
    result: list[str] = []
    for path in paths:
        result.extend([flag, str(path)])
    return result


def cold_args(args: argparse.Namespace, core: dict[str, Any],
              targets: dict[str, Path], *, preflight: bool = False) -> list[str]:
    values = (["--preflight-only"] if preflight else []) + [
        "--core-control-dir", str(core["control"]),
        "--adapter-dir", str(core["targets"]["adapter"]),
        "--candidate-dir", str(core["targets"]["seed1_candidate"]),
        "--formal-verification-file",
        str(core["targets"]["verifier1_output"] / "verification.json"),
        "--control-dir", str(targets["cold_control"]),
        "--output-dir", str(targets["cold_output"]),
        "--run-dir", str(targets["cold_run"]),
        "--expect-core-receipt-file-sha256",
        args.expect_core_receipt_file_sha256,
        "--expect-core-receipt-object-sha256",
        args.expect_core_receipt_object_sha256,
        "--expect-core-pass-sha256", args.expect_core_pass_sha256,
        "--expect-helper-sha256", PROGRAM_PINS["cold"],
        "--expect-producer-sha256", CORE_SOURCE_PINS["producer"],
        "--expect-verifier-sha256", CORE_SOURCE_PINS["independent_verifier"],
        "--expect-transaction-runner-sha256",
        CORE_SOURCE_PINS["transaction_runner"],
        "--expect-python-sha256", PROGRAM_PINS["python"],
        "--timeout-seconds", str(args.stage_timeout_seconds),
    ]
    values.extend(repeated("--core-dir", core["core_dirs"]))
    return values


def invoke(name: str, argv: list[str], stage: str,
           timeout: int, control: Path | None = None,
           expected: str | None = None) -> dict[str, Any]:
    runtime = f"/run/user/{os.getuid()}"
    completed = subprocess.run([
        str(PYTHON), "-I", "-B", str(PROGRAMS[name]), *argv,
    ], cwd=ROOT, env={
        "PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
        "PYTHONHASHSEED": str(30662890 + len(stage)),
        "PYTHONDONTWRITEBYTECODE": "1", "XDG_RUNTIME_DIR": runtime,
        "DBUS_SESSION_BUS_ADDRESS": "unix:path=" + runtime + "/bus",
    }, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
       stderr=subprocess.PIPE, timeout=timeout, check=False)
    if control is not None:
        write_once(control / (stage + ".stdout.log"), completed.stdout)
        write_once(control / (stage + ".stderr.log"), completed.stderr)
        write_once(control / (stage + ".exit_code.txt"),
                   (str(completed.returncode) + "\n").encode("ascii"))
    need(completed.returncode == 0 and completed.stderr == b""
         and completed.stdout.endswith(b"\n"), "clean stage:" + stage)
    value = strict_load(completed.stdout[:-1])
    need(type(value) is dict and canonical(value) + b"\n" == completed.stdout
         and value.get("CM2") == "NO-GO_FOR_CLAIM"
         and value.get("formal_credit") == 0
         and value.get("status") == (expected or EXPECTED_STATUS[name]),
         "canonical stage stdout/status:" + stage)
    return value


def initial(args: argparse.Namespace, targets: dict[str, Path]) \
        -> tuple[dict[str, Any], dict[str, Any]]:
    sources = source_pins(args.expect_watcher_sha256)
    tests = self_tests()
    need(all(not path.exists() and not path.is_symlink()
             for path in targets.values()), "all ten release targets fresh")
    core = core_context(args)
    invoke("cold", cold_args(args, core, targets, preflight=True),
           "cold_positive_preflight", 900, expected=(
               "PASS_C28_CORE_COLD_REPLAY_PREFLIGHT__NO_PATHS_CREATED_ZERO_CREDIT"))
    need(all(not path.exists() and not path.is_symlink()
             for path in targets.values()),
         "positive preflight creates zero release paths")
    return core, {"source_pins": sources,
                  "self_test_stdout_sha256": tests,
                  "positive_cold_preflight": True}


def failure(control: Path, stage: str, error: BaseException) -> None:
    if not control.exists():
        return
    body = {
        "schema": PREFIX + "release-chain-failure.v1",
        "status": "FAILED_CLOSED_C28_RELEASE_CHAIN__ZERO_CREDIT",
        "failed_at_utc": now(), "stage": stage,
        "error": f"{type(error).__name__}:{error}",
        "authority_minted_by_watcher": False,
        "formal_credit": 0, "manifest_authorized": False,
        "C27R2": "AUTHORIZED_PREDECESSOR_ONLY",
        "C28": "UNAUTHORIZED_UNLESS_A_COMPLETE_VALID_TERMINAL_ALREADY_EXISTS",
        "C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM",
    }
    receipt = {**body, "failure_receipt_sha256": digest(body)}
    if not (control / "failure_receipt.json").exists():
        write_json(control / "failure_receipt.json", receipt)
    if not (control / "FAILED.lock").exists():
        write_once(control / "FAILED.lock", b"FAILED_CLOSED_C28_RELEASE_CHAIN\n")


def execute(args: argparse.Namespace) -> dict[str, Any]:
    pins = (args.expect_core_receipt_file_sha256,
            args.expect_core_receipt_object_sha256,
            args.expect_core_pass_sha256, args.expect_watcher_sha256)
    need(all(valid_sha(value) for value in pins), "dynamic core/watcher pins")
    targets = release_paths(args.stem)
    core, preflight = initial(args, targets)
    if args.preflight_only:
        return {"status":
                "PASS_C28_RELEASE_SOURCES_CORE_AND_TEN_FRESH_PATHS_PREFLIGHT__"
                "NO_OUTPUT_CREATED_ZERO_CREDIT"}
    release_invocation = os.environ.get("INVOCATION_ID")
    need(type(args.release_unit) is str and args.release_unit.endswith(".service")
         and type(release_invocation) is str
         and re.fullmatch(r"[0-9a-f]{32}", release_invocation) is not None,
         "real release requires unique systemd invocation")
    control = targets["control"]
    stage = "create_control"
    try:
        control.mkdir(mode=0o700)
        pinset_body = {
            "schema": PINSET_SCHEMA,
            "status": "PASS_C28_CORE_RELEASE_SOURCES_AND_FRESH_TARGET_PINSET__ZERO_CREDIT",
            "release_unit": args.release_unit,
            "release_invocation_id": release_invocation,
            "core_unit": args.core_unit,
            "core_invocation_id": args.expect_core_invocation_id,
            "core_control_dir": str(core["control"].relative_to(ROOT)),
            "core_receipt_file_sha256": args.expect_core_receipt_file_sha256,
            "core_receipt_object_sha256": args.expect_core_receipt_object_sha256,
            "core_pass_lock_sha256": args.expect_core_pass_sha256,
            **preflight,
            "targets": {name: str(path.relative_to(ROOT))
                        for name, path in sorted(targets.items())},
            "formal_credit": 0, "manifest_authorized": False,
            "C27R2": "AUTHORIZED_PREDECESSOR_ONLY",
            "C28": "UNAUTHORIZED", "C29": "UNAUTHORIZED",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        pinset = {**pinset_body, "pinset_sha256": digest(pinset_body)}
        write_json(control / "pinset.json", pinset)
        stage = "cold_replay"
        invoke("cold", cold_args(args, core, targets), stage,
               args.stage_timeout_seconds, control)
        cold_path = targets["cold_control"] / "cold_replay_receipt.json"
        cold = document(cold_path, "cold_replay_receipt_sha256")
        stage = "release_attacks"
        attack_args = [
            "--core-unit", args.core_unit,
            "--expect-core-invocation-id", args.expect_core_invocation_id,
            "--core-control-dir", str(core["control"]),
            "--predecessor-terminal-dir", str(core["predecessor"]),
            "--adapter-dir", str(core["targets"]["adapter"]),
            "--seed1-candidate-dir", str(core["targets"]["seed1_candidate"]),
            "--seed2-candidate-dir", str(core["targets"]["seed2_candidate"]),
            "--verifier1-file",
            str(core["targets"]["verifier1_output"] / "verification.json"),
            "--verifier2-file",
            str(core["targets"]["verifier2_output"] / "verification.json"),
            "--cold-control-dir", str(targets["cold_control"]),
            "--cold-output-dir", str(targets["cold_output"]),
            "--cold-run-dir", str(targets["cold_run"]),
            "--output-dir", str(targets["release_attacks"]),
            "--expect-harness-sha256", PROGRAM_PINS["attacks"],
            "--expect-core-receipt-file-sha256",
            args.expect_core_receipt_file_sha256,
            "--expect-core-receipt-object-sha256",
            args.expect_core_receipt_object_sha256,
            "--expect-core-pass-sha256", args.expect_core_pass_sha256,
            "--expect-cold-receipt-file-sha256", file_sha(cold_path),
            "--expect-cold-receipt-object-sha256",
            cold["cold_replay_receipt_sha256"],
            "--adapter-run-dir", str(core["targets"]["adapter_run"]),
            "--adapter-verifier-run-dir",
            str(core["targets"]["adapter_verifier_run"]),
            "--seed1-run-dir", str(core["targets"]["seed1_run"]),
            "--seed2-run-dir", str(core["targets"]["seed2_run"]),
            "--verifier1-run-dir", str(core["targets"]["verifier1_run"]),
            "--verifier2-run-dir", str(core["targets"]["verifier2_run"]),
            "--core-attack-run-dir", str(core["targets"]["attack_run"]),
        ]
        attack_args.extend(repeated("--core-dir", core["core_dirs"]))
        invoke("attacks", attack_args, stage, args.stage_timeout_seconds, control)
        attack_path = targets["release_attacks"] / "release_attacks.json"
        attacks = document(attack_path, "release_attack_receipt_sha256")
        stage = "evidence"
        evidence_roots = list(core["core_dirs"]) + [
            core["predecessor"], targets["cold_control"],
            targets["cold_output"], targets["cold_run"],
            targets["release_attacks"],
        ]
        evidence_args = [
            "--core-unit", args.core_unit,
            "--expect-core-invocation-id", args.expect_core_invocation_id,
            "--core-control-dir", str(core["control"]),
            "--cold-control-dir", str(targets["cold_control"]),
            "--release-attack-dir", str(targets["release_attacks"]),
            "--output-dir", str(targets["evidence"]),
            "--expect-builder-sha256", PROGRAM_PINS["evidence"],
            "--expect-core-receipt-file-sha256",
            args.expect_core_receipt_file_sha256,
            "--expect-core-receipt-object-sha256",
            args.expect_core_receipt_object_sha256,
            "--expect-core-pass-sha256", args.expect_core_pass_sha256,
            "--expect-cold-receipt-file-sha256", file_sha(cold_path),
            "--expect-cold-receipt-object-sha256",
            cold["cold_replay_receipt_sha256"],
            "--expect-release-attack-file-sha256", file_sha(attack_path),
            "--expect-release-attack-object-sha256",
            attacks["release_attack_receipt_sha256"],
        ]
        evidence_args.extend(repeated("--evidence-root", evidence_roots))
        invoke("evidence", evidence_args, stage,
               args.stage_timeout_seconds, control)
        evidence_path = targets["evidence"] / "evidence_bundle.json"
        evidence = document(evidence_path, "evidence_bundle_sha256")
        stage = "manifests"
        common_release_args = [
            "--core-control-dir", str(core["control"]),
            "--predecessor-terminal-dir", str(core["predecessor"]),
            "--adapter-dir", str(core["targets"]["adapter"]),
            "--candidate-dir", str(core["targets"]["seed1_candidate"]),
            "--formal-verification-file",
            str(core["targets"]["verifier1_output"] / "verification.json"),
            "--core-attacks-file", str(core["control"] / "coherent_attacks.json"),
            "--cold-control-dir", str(targets["cold_control"]),
            "--cold-output-dir", str(targets["cold_output"]),
            "--cold-run-dir", str(targets["cold_run"]),
            "--release-attack-dir", str(targets["release_attacks"]),
            "--evidence-dir", str(targets["evidence"]),
            "--expect-core-receipt-file-sha256",
            args.expect_core_receipt_file_sha256,
            "--expect-core-receipt-object-sha256",
            args.expect_core_receipt_object_sha256,
            "--expect-core-pass-sha256", args.expect_core_pass_sha256,
            "--expect-cold-receipt-file-sha256", file_sha(cold_path),
            "--expect-cold-receipt-object-sha256",
            cold["cold_replay_receipt_sha256"],
            "--expect-release-attack-file-sha256", file_sha(attack_path),
            "--expect-release-attack-object-sha256",
            attacks["release_attack_receipt_sha256"],
            "--expect-evidence-file-sha256", file_sha(evidence_path),
            "--expect-evidence-object-sha256",
            evidence["evidence_bundle_sha256"],
        ]
        invoke("manifests", [*common_release_args,
            "--output-dir", str(targets["manifests"]),
            "--expect-builder-sha256", PROGRAM_PINS["manifests"]],
            stage, args.stage_timeout_seconds, control)
        manifest_receipt_path = targets["manifests"] / "manifest_receipt.json"
        manifest_receipt = document(manifest_receipt_path,
                                    "manifest_receipt_sha256")
        payload_sha = file_sha(targets["manifests"] / "payload_manifest.sha256")
        root_sha = file_sha(targets["manifests"] / "root_manifest.sha256")
        stage = "independent_outer"
        outer_args = [
            "--core-unit", args.core_unit,
            "--expect-core-invocation-id", args.expect_core_invocation_id,
            "--core-control-dir", str(core["control"]),
            "--candidate-dir", str(core["targets"]["seed1_candidate"]),
            "--formal-verification-file",
            str(core["targets"]["verifier1_output"] / "verification.json"),
            "--core-attacks-file", str(core["control"] / "coherent_attacks.json"),
            "--cold-control-dir", str(targets["cold_control"]),
            "--release-attack-dir", str(targets["release_attacks"]),
            "--evidence-dir", str(targets["evidence"]),
            "--manifest-dir", str(targets["manifests"]),
            "--output-file", str(targets["outer"]),
            "--expect-outer-sha256", PROGRAM_PINS["outer"],
            "--expect-manifest-receipt-file-sha256",
            file_sha(manifest_receipt_path),
            "--expect-manifest-receipt-object-sha256",
            manifest_receipt["manifest_receipt_sha256"],
            "--expect-payload-manifest-sha256", payload_sha,
            "--expect-root-manifest-sha256", root_sha,
            "--expect-core-receipt-file-sha256",
            args.expect_core_receipt_file_sha256,
            "--expect-core-receipt-object-sha256",
            args.expect_core_receipt_object_sha256,
            "--expect-core-pass-sha256", args.expect_core_pass_sha256,
            "--expect-cold-receipt-file-sha256", file_sha(cold_path),
            "--expect-cold-receipt-object-sha256",
            cold["cold_replay_receipt_sha256"],
            "--expect-release-attack-file-sha256", file_sha(attack_path),
            "--expect-release-attack-object-sha256",
            attacks["release_attack_receipt_sha256"],
            "--expect-evidence-file-sha256", file_sha(evidence_path),
            "--expect-evidence-object-sha256",
            evidence["evidence_bundle_sha256"],
        ]
        invoke("outer", outer_args, stage, args.stage_timeout_seconds, control)
        outer = document(targets["outer"], "outer_verification_sha256")
        stage = "conditional_seal"
        seal_args = [
            "--manifest-dir", str(targets["manifests"]),
            "--outer-file", str(targets["outer"]),
            "--output-dir", str(targets["seal"]),
            "--expect-builder-sha256", PROGRAM_PINS["seal"],
            "--expect-outer-file-sha256", file_sha(targets["outer"]),
            "--expect-outer-object-sha256",
            outer["outer_verification_sha256"],
            "--expect-manifest-receipt-file-sha256",
            file_sha(manifest_receipt_path),
            "--expect-manifest-receipt-object-sha256",
            manifest_receipt["manifest_receipt_sha256"],
            "--expect-payload-manifest-sha256", payload_sha,
            "--expect-root-manifest-sha256", root_sha,
        ]
        invoke("seal", seal_args, stage, args.stage_timeout_seconds, control)
        seal_path = targets["seal"] / "seal_candidate.json"
        seal = document(seal_path, "seal_candidate_sha256")
        stage = "independent_terminal_byte_replay"
        terminal_args = [
            "--seal-dir", str(targets["seal"]),
            "--manifest-dir", str(targets["manifests"]),
            "--outer-file", str(targets["outer"]),
            "--core-control-dir", str(core["control"]),
            "--predecessor-terminal-dir", str(core["predecessor"]),
            "--output-dir", str(targets["terminal"]),
            "--expect-replay-sha256", PROGRAM_PINS["terminal"],
            "--expect-seal-candidate-file-sha256", file_sha(seal_path),
            "--expect-seal-candidate-object-sha256",
            seal["seal_candidate_sha256"],
            "--expect-seal-payload-manifest-sha256",
            file_sha(targets["seal"] / "seal_payload_manifest.sha256"),
            "--expect-seal-root-manifest-sha256",
            file_sha(targets["seal"] / "seal_root_manifest.sha256"),
            "--expect-outer-file-sha256", file_sha(targets["outer"]),
            "--expect-outer-object-sha256",
            outer["outer_verification_sha256"],
            "--expect-manifest-receipt-file-sha256",
            file_sha(manifest_receipt_path),
            "--expect-manifest-receipt-object-sha256",
            manifest_receipt["manifest_receipt_sha256"],
            "--expect-core-receipt-file-sha256",
            args.expect_core_receipt_file_sha256,
            "--expect-core-receipt-object-sha256",
            args.expect_core_receipt_object_sha256,
            "--expect-core-pass-sha256", args.expect_core_pass_sha256,
        ]
        invoke("terminal", terminal_args, stage,
               args.stage_timeout_seconds, control)
        terminal_receipt_path = targets["terminal"] / "terminal_receipt.json"
        terminal_replay_path = targets["terminal"] / "terminal_replay.json"
        terminal_receipt = document(terminal_receipt_path,
                                    "terminal_receipt_sha256")
        terminal_replay = document(terminal_replay_path,
                                   "terminal_replay_sha256")
        need(terminal_receipt.get("status") == TERMINAL_STATUS
             and terminal_replay.get("status") == TERMINAL_STATUS
             and terminal_receipt.get("authority_minted") is True
             and terminal_receipt.get("manifest_authorized") is True
             and terminal_receipt.get("C27R2_terminal_root_manifest_sha256")
                 == C27["root"]
             and terminal_receipt.get("C28")
                 == "AUTHORIZED_TERMINAL_SOURCE_G_PAIR_ROUTING_AUTHORITY"
             and terminal_receipt.get("C29") == "UNAUTHORIZED_NOT_STARTED"
             and terminal_receipt.get("CM2") == "NO-GO_FOR_CLAIM"
             and (targets["terminal"] / "PASS.lock").read_bytes()
                 == TERMINAL_PASS,
             "terminal mints only C28 after independent byte replay")
        body = {
            "schema": PREFIX + "release-chain-watch-receipt.v1",
            "status": TERMINAL_STATUS, "completed_at_utc": now(),
            "pinset_object_sha256": pinset["pinset_sha256"],
            "terminal_root_manifest_sha256":
                file_sha(targets["terminal"] / "root_manifest.sha256"),
            "terminal_receipt_file_sha256": file_sha(terminal_receipt_path),
            "terminal_receipt_object_sha256":
                terminal_receipt["terminal_receipt_sha256"],
            "terminal_replay_file_sha256": file_sha(terminal_replay_path),
            "terminal_replay_object_sha256":
                terminal_replay["terminal_replay_sha256"],
            "authority_minted": True, "formal_credit": 0,
            "manifest_authorized": True,
            "C27R2": "AUTHORIZED_TERMINAL_PREDECESSOR_UNCHANGED",
            "C28": "AUTHORIZED_TERMINAL_SOURCE_G_PAIR_ROUTING_AUTHORITY",
            "C29": "UNAUTHORIZED_NOT_STARTED", "Source_W": "UNCHANGED",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        receipt = {**body, "watch_receipt_sha256": digest(body)}
        write_json(control / "watch_receipt.json", receipt)
        write_once(control / "PASS.lock", WATCH_PASS)
        return receipt
    except BaseException as error:
        failure(control, stage, error)
        raise


def self_test() -> dict[str, Any]:
    paths = release_paths("c28-v2-release-self-test-targets")
    need(len(paths) == 10 and all(valid_sha(value)
                                  for value in PROGRAM_PINS.values())
         and all(valid_sha(value) for value in CORE_SOURCE_PINS.values())
         and EXPECTED["total_pairs"]
             == EXPECTED["within_pairs"] + EXPECTED["cross_pairs"],
         "watcher topology/source/math fixtures")
    return {"status": "PASS_C28_RELEASE_CHAIN_WATCHER_V2_SELF_TEST",
            "formal_credit": 0, "C28": "UNAUTHORIZED",
            "C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM"}


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--self-test", action="store_true")
    value.add_argument("--preflight-only", action="store_true")
    for name in (
        "stem", "release-unit", "core-unit", "expect-core-invocation-id",
        "core-control-dir", "expect-core-receipt-file-sha256",
        "expect-core-receipt-object-sha256", "expect-core-pass-sha256",
        "expect-watcher-sha256",
    ):
        value.add_argument("--" + name)
    value.add_argument("--stage-timeout-seconds", type=int, default=86_400)
    return value


def main() -> int:
    args = parser().parse_args()
    fields = (
        "stem", "release_unit", "core_unit", "expect_core_invocation_id",
        "core_control_dir", "expect_core_receipt_file_sha256",
        "expect_core_receipt_object_sha256", "expect_core_pass_sha256",
        "expect_watcher_sha256",
    )
    try:
        if args.self_test:
            need(not args.preflight_only
                 and all(getattr(args, field) is None for field in fields),
                 "self-test accepts no run arguments")
            result = self_test()
        else:
            need(all(getattr(args, field) is not None for field in fields)
                 and 600 <= args.stage_timeout_seconds <= 172_800,
                 "all run arguments and bounded timeout")
            result = execute(args)
        sys.stdout.buffer.write(canonical({
            "CM2": "NO-GO_FOR_CLAIM", "formal_credit": 0,
            "status": result["status"],
        }) + b"\n")
        return 0
    except (Blocked, OSError, ValueError, KeyError, TypeError,
            subprocess.SubprocessError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
