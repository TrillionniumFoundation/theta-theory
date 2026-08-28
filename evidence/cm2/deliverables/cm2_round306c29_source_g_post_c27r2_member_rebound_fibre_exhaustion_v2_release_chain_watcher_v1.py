#!/usr/bin/env python3
"""Run the append-only C29-v2 release chain after a formally clean core.

This watcher is inert unless an exact core receipt, a clean systemd service,
all frozen source pins, and eleven fresh targets pass.  The final replay is
the only child allowed to mint C29; every earlier child remains zero-credit.
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
PREFIX = "cm2_round306c29_source_g_post_c27r2_member_rebound_fibre_exhaustion_v2"
PROGRAMS = {
    "cold": ROOT / f"deliverables/{PREFIX}_release_cold_replay_runner_v1.py",
    "evidence": ROOT / f"deliverables/{PREFIX}_release_evidence_bundle_builder_v1.py",
    "release_attacks": ROOT / f"deliverables/{PREFIX}_release_only_attack_harness_v1.py",
    "manifests": ROOT / f"deliverables/{PREFIX}_release_manifest_builder_v1.py",
    "outer": ROOT / f"deliverables/{PREFIX}_release_outer_verifier_v1.py",
    "seal": ROOT / f"deliverables/{PREFIX}_release_terminal_seal_builder_v1.py",
    "terminal": ROOT / f"deliverables/{PREFIX}_terminal_byte_replay_v1.py",
}
PINS = {
    "cold": "46da52b4fdf1e89ead9f77c184303d1b2cd97dd38493b4a4aa5aef4e9057c2e7",
    "evidence": "766c217ac0aee04d81493a6ff4ab019702a856bc24dc1d585225535a60d4f28c",
    "release_attacks": "5409cf898395aa3c81da588fe309e9d4aaa534889ea23944b29846e7c2e20e15",
    "manifests": "143b0962dd1dd1b6c00653c18f855e5431307736cc27da5ba5f42896255fa0d7",
    "outer": "41f7dcd8a352bd82e200472d8263c62fc7738b7ce72b727e31394ba7eb223829",
    "seal": "9d47ab01af382c11c8e157546772119f1f5b479807e6e6def472fc56c939f61e",
    "terminal": "d77c2b2e2b80cf879c791e8f3dcfa95964096c9ba1f7c752dd4d3a46596e184f",
    "python": "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118",
}
BASE = "cm2.round306c29.source-g-post-c27r2-member-rebound-fibre-exhaustion.v2."
CORE_SCHEMA = BASE + "gated-dual-terminal-seed-core-receipt.v1"
CORE_STATUS = "PASS_C29_V2_DUAL_TERMINAL_ADAPTERS_SEED1_PRODUCER_SEED2_NO_IMPORT_VERIFIER_AND_34_ATTACKS__ZERO_CREDIT_PENDING_RELEASE_TERMINAL"
TERMINAL_STATUS = "PASS_C29_V2_TERMINAL_BYTE_REPLAY__FORMAL_SOURCE_G_FIBRE_AUTHORITY_MINTED"
PASS_BYTES = b"PASS_C29_V2_SOURCE_G_FIBRE_AUTHORITY_TERMINAL_BYTE_REPLAY__SOURCE_W_UNCHANGED_CM2_NO_GO\n"
WATCH_PASS = b"PASS_C29_V2_RELEASE_CHAIN_TERMINAL_MINTED__SOURCE_W_UNCHANGED_CM2_NO_GO\n"
EXPECTED_STATUS = {
    "cold": "PASS_C29_V2_FRESH_NO_IMPORT_COLD_BYTE_REPLAY_WITH_ALL_CORE_INPUT_PRE_POST_SHA_STAT__ZERO_CREDIT",
    "evidence": "PASS_C29_V2_DUAL_PREDECESSOR_CORE_COLD_PROCESS_AND_BYTE_EVIDENCE_FROZEN__ZERO_CREDIT",
    "release_attacks": "PASS_C29_V2_40_OF_40_DUAL_PREDECESSOR_RELEASE_ONLY_ATTACKS_REJECTED__ZERO_CREDIT",
    "manifests": "PASS_C29_V2_MANIFEST_FIRST_PAYLOAD_AND_DUAL_PREDECESSOR_ROOT_CLOSURE__ZERO_CREDIT_PENDING_OUTER_TERMINAL",
    "outer": "PASS_INDEPENDENT_C29_V2_FULL_LEDGER_DUAL_PREDECESSOR_MANIFEST_COLD_AND_40_RELEASE_ATTACK_CHECK__CONDITIONAL_ZERO_CREDIT",
    "seal": "PASS_CONDITIONAL_C29_V2_TERMINAL_SEAL_CANDIDATE__ZERO_CREDIT_PENDING_INDEPENDENT_BYTE_REPLAY",
    "terminal": TERMINAL_STATUS,
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
    return type(value) is str and len(value) == 64 and all(
        char in "0123456789abcdef" for char in value)


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace(
        "+00:00", "Z")


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


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns,
            value.st_uid, value.st_gid)


def file_sha(path: Path) -> str:
    path = path.absolute()
    need(path.resolve(strict=True) == path, "canonical path:" + str(path))
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                         | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular singleton:" + str(path))
        state = hashlib.sha256()
        while block := os.read(descriptor, 4 << 20):
            state.update(block)
        need(fingerprint(os.fstat(descriptor)) == fingerprint(before),
             "stable SHA/stat:" + str(path))
        return state.hexdigest()
    finally:
        os.close(descriptor)


def document(path: Path, closure: str) -> dict[str, Any]:
    payload = path.read_bytes()
    need(payload.endswith(b"\n") and not payload.endswith(b"\n\n"),
         "JSON newline")
    value = strict(payload[:-1])
    need(type(value) is dict and canonical(value) == payload[:-1],
         "canonical JSON")
    body = dict(value)
    claim = body.pop(closure, None)
    need(valid_sha(claim) and claim == digest(body), "object closure")
    return value


def write_once(path: Path, payload: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
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


def paths(stem: str) -> dict[str, Path]:
    need(re.fullmatch(r"c29-v2-release-[a-z0-9][a-z0-9-]{7,100}", stem)
         is not None, "canonical release stem")
    values = {
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
    need(len(values) == 11 and len(set(values.values())) == 11
         and all(path.parent == AUDIT for path in values.values()),
         "release target topology")
    return values


def source_pins(expect_self: str) -> dict[str, str]:
    need(valid_sha(expect_self) and file_sha(SELF) == expect_self,
         "watcher self pin")
    need(file_sha(PYTHON) == PINS["python"]
         and all(file_sha(PROGRAMS[name]) == PINS[name] for name in PROGRAMS),
         "frozen release source pins")
    return {**PINS, "watcher": expect_self}


def run(program: str, argv: list[str], stage: str, control: Path,
        timeout: int) -> dict[str, Any]:
    completed = subprocess.run([str(PYTHON), "-I", "-B", str(PROGRAMS[program]),
                                *argv], cwd=ROOT,
        env={"PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
             "PYTHONHASHSEED": str(30662990 + len(list(control.iterdir())))},
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, timeout=timeout, check=False)
    write_once(control / (stage + ".stdout.log"), completed.stdout)
    write_once(control / (stage + ".stderr.log"), completed.stderr)
    write_once(control / (stage + ".exit_code.txt"),
               (str(completed.returncode) + "\n").encode("ascii"))
    need(completed.returncode == 0 and completed.stderr == b"",
         stage + ":clean child process")
    output = strict(completed.stdout.rstrip(b"\n"))
    need(type(output) is dict and canonical(output) + b"\n" == completed.stdout
         and output == {"CM2": "NO-GO_FOR_CLAIM", "formal_credit": 0,
                        "status": EXPECTED_STATUS[program]},
         stage + ":canonical stdout status")
    return output


def self_tests() -> None:
    for name, program in PROGRAMS.items():
        completed = subprocess.run([str(PYTHON), "-I", "-B", str(program),
                                    "--self-test"], cwd=ROOT,
            env={"PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
                 "PYTHONHASHSEED": str(30662970 + len(name))},
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, timeout=300, check=False)
        need(completed.returncode == 0 and completed.stderr == b"",
             name + ":source self-test")


def initial(args: argparse.Namespace, targets: dict[str, Path]) -> dict[str, Any]:
    source_pins(args.expect_watcher_sha256)
    self_tests()
    need(all(not path.exists() and not path.is_symlink()
             for path in targets.values()), "all eleven release targets fresh")
    core_control = Path(args.core_control_dir).absolute()
    need(core_control.parent == AUDIT and core_control.is_dir(), "core control")
    core_path = core_control / "core_receipt.json"
    core = document(core_path, "core_receipt_sha256")
    need(file_sha(core_path) == args.expect_core_receipt_file_sha256
         and core["core_receipt_sha256"] == args.expect_core_receipt_object_sha256
         and core.get("schema") == CORE_SCHEMA and core.get("status") == CORE_STATUS
         and core.get("formal_credit") == 0
         and core.get("manifest_authorized") is False
         and core.get("CM2") == "NO-GO_FOR_CLAIM", "exact core boundary")
    # This is the only child preflight whose predecessors already exist.
    completed = subprocess.run([str(PYTHON), "-I", "-B", str(PROGRAMS["cold"]),
        "--preflight-only", "--core-control-dir", str(core_control),
        "--control-dir", str(targets["cold_control"]),
        "--output-dir", str(targets["cold_output"]),
        "--run-dir", str(targets["cold_run"]),
        "--expect-core-receipt-file-sha256", args.expect_core_receipt_file_sha256,
        "--expect-core-receipt-object-sha256", args.expect_core_receipt_object_sha256,
        "--expect-helper-sha256", PINS["cold"],
        "--timeout-seconds", str(args.stage_timeout_seconds)], cwd=ROOT,
        env={"PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
             "PYTHONHASHSEED": "30662989"}, stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=600, check=False)
    need(completed.returncode == 0 and completed.stderr == b""
         and all(not path.exists() for path in targets.values()),
         "cold/core/fresh preflight creates nothing")
    return core


def failure(control: Path, stage: str, error: BaseException) -> None:
    if not control.exists():
        return
    body = {"schema": BASE + "release-chain-failure.v1",
            "status": "FAILED_CLOSED_C29_V2_RELEASE_CHAIN__ZERO_CREDIT",
            "stage": stage, "error": f"{type(error).__name__}:{error}",
            "failed_at_utc": now(), "authority_minted": False,
            "formal_credit": 0, "manifest_authorized": False,
            "C29": "UNAUTHORIZED", "Source_W": "UNCHANGED",
            "CM2": "NO-GO_FOR_CLAIM"}
    receipt = dict(body)
    receipt["failure_receipt_sha256"] = digest(receipt)
    if not (control / "failure_receipt.json").exists():
        write_json(control / "failure_receipt.json", receipt)
    if not (control / "FAILED.lock").exists():
        write_once(control / "FAILED.lock", b"FAILED_CLOSED_C29_V2_RELEASE_CHAIN\n")


def execute(args: argparse.Namespace) -> dict[str, Any]:
    targets = paths(args.stem)
    core = initial(args, targets)
    if args.preflight_only:
        return {"status": "PASS_C29_V2_RELEASE_SOURCES_CORE_AND_ELEVEN_FRESH_PATHS_PREFLIGHT__NO_OUTPUT_ZERO_CREDIT"}
    invocation = os.environ.get("INVOCATION_ID")
    need(type(invocation) is str and re.fullmatch(r"[0-9a-f]{32}", invocation)
         is not None and args.unit_name.endswith(".service"),
         "release systemd identity")
    control = targets["control"]
    control.mkdir(mode=0o700)
    stage = "pinset"
    try:
        pinset_body = {"schema": BASE + "release-chain-pinset.v1",
            "status": "PASS_C29_V2_RELEASE_SOURCE_CORE_AND_FRESH_TARGET_PINSET__ZERO_CREDIT",
            "release_unit_name": args.unit_name,
            "release_invocation_id": invocation,
            "core_control_dir": str(Path(args.core_control_dir).absolute().relative_to(ROOT)),
            "core_receipt_file_sha256": args.expect_core_receipt_file_sha256,
            "core_receipt_object_sha256": args.expect_core_receipt_object_sha256,
            "source_pins": source_pins(args.expect_watcher_sha256),
            "targets": {name: str(path.relative_to(ROOT))
                        for name, path in sorted(targets.items())},
            "formal_credit": 0, "manifest_authorized": False,
            "C29": "UNAUTHORIZED", "Source_W": "UNCHANGED",
            "CM2": "NO-GO_FOR_CLAIM"}
        pinset = dict(pinset_body)
        pinset["pinset_sha256"] = digest(pinset)
        write_json(control / "pinset.json", pinset)
        core_control = Path(args.core_control_dir).absolute()
        stage = "cold"
        run("cold", ["--core-control-dir", str(core_control),
            "--control-dir", str(targets["cold_control"]),
            "--output-dir", str(targets["cold_output"]),
            "--run-dir", str(targets["cold_run"]),
            "--expect-core-receipt-file-sha256", args.expect_core_receipt_file_sha256,
            "--expect-core-receipt-object-sha256", args.expect_core_receipt_object_sha256,
            "--expect-helper-sha256", PINS["cold"],
            "--timeout-seconds", str(args.stage_timeout_seconds)], stage, control,
            args.stage_timeout_seconds + 600)
        cold_path = targets["cold_control"] / "cold_replay_receipt.json"
        cold = document(cold_path, "cold_replay_receipt_sha256")
        cold_file = file_sha(cold_path)
        cold_object = cold["cold_replay_receipt_sha256"]
        stage = "evidence"
        run("evidence", ["--core-control-dir", str(core_control),
            "--cold-control-dir", str(targets["cold_control"]),
            "--cold-output-dir", str(targets["cold_output"]),
            "--cold-run-dir", str(targets["cold_run"]),
            "--output-dir", str(targets["evidence"]),
            "--expect-core-receipt-file-sha256", args.expect_core_receipt_file_sha256,
            "--expect-core-receipt-object-sha256", args.expect_core_receipt_object_sha256,
            "--expect-cold-receipt-file-sha256", cold_file,
            "--expect-cold-receipt-object-sha256", cold_object,
            "--expect-builder-sha256", PINS["evidence"]], stage, control,
            args.stage_timeout_seconds)
        evidence_path = targets["evidence"] / "evidence_bundle.json"
        evidence = document(evidence_path, "evidence_bundle_sha256")
        evidence_file = file_sha(evidence_path)
        evidence_object = evidence["evidence_bundle_sha256"]
        stage = "release_attacks"
        run("release_attacks", ["--core-control-dir", str(core_control),
            "--cold-control-dir", str(targets["cold_control"]),
            "--evidence-dir", str(targets["evidence"]),
            "--work-dir", str(targets["release_attack_work"]),
            "--result-file", str(targets["release_attacks"]),
            "--expect-core-receipt-file-sha256", args.expect_core_receipt_file_sha256,
            "--expect-core-receipt-object-sha256", args.expect_core_receipt_object_sha256,
            "--expect-cold-receipt-file-sha256", cold_file,
            "--expect-cold-receipt-object-sha256", cold_object,
            "--expect-evidence-file-sha256", evidence_file,
            "--expect-evidence-object-sha256", evidence_object,
            "--expect-harness-sha256", PINS["release_attacks"]], stage, control,
            args.stage_timeout_seconds)
        release = document(targets["release_attacks"], "release_attacks_sha256")
        release_file = file_sha(targets["release_attacks"])
        release_object = release["release_attacks_sha256"]
        common = ["--core-control-dir", str(core_control),
            "--cold-control-dir", str(targets["cold_control"]),
            "--cold-output-dir", str(targets["cold_output"]),
            "--cold-run-dir", str(targets["cold_run"]),
            "--evidence-dir", str(targets["evidence"]),
            "--release-attack-work-dir", str(targets["release_attack_work"]),
            "--release-attacks-file", str(targets["release_attacks"]),
            "--expect-core-receipt-file-sha256", args.expect_core_receipt_file_sha256,
            "--expect-core-receipt-object-sha256", args.expect_core_receipt_object_sha256,
            "--expect-cold-receipt-file-sha256", cold_file,
            "--expect-cold-receipt-object-sha256", cold_object,
            "--expect-evidence-file-sha256", evidence_file,
            "--expect-evidence-object-sha256", evidence_object,
            "--expect-release-attacks-file-sha256", release_file,
            "--expect-release-attacks-object-sha256", release_object]
        stage = "manifests"
        run("manifests", [*common, "--output-dir", str(targets["manifests"]),
            "--expect-builder-sha256", PINS["manifests"]], stage, control,
            args.stage_timeout_seconds)
        manifest_receipt_path = targets["manifests"] / "manifest_receipt.json"
        manifest_receipt = document(manifest_receipt_path, "manifest_receipt_sha256")
        manifest_file = file_sha(manifest_receipt_path)
        manifest_object = manifest_receipt["manifest_receipt_sha256"]
        payload_sha = file_sha(targets["manifests"] / "payload_manifest.sha256")
        root_sha = file_sha(targets["manifests"] / "root_manifest.sha256")
        outer_common = ["--core-control-dir", str(core_control),
            "--cold-control-dir", str(targets["cold_control"]),
            "--evidence-dir", str(targets["evidence"]),
            "--release-attacks-file", str(targets["release_attacks"]),
            "--manifest-dir", str(targets["manifests"]),
            "--expect-manifest-receipt-file-sha256", manifest_file,
            "--expect-manifest-receipt-object-sha256", manifest_object,
            "--expect-payload-manifest-sha256", payload_sha,
            "--expect-root-manifest-sha256", root_sha,
            "--expect-core-receipt-file-sha256", args.expect_core_receipt_file_sha256,
            "--expect-core-receipt-object-sha256", args.expect_core_receipt_object_sha256,
            "--expect-cold-receipt-file-sha256", cold_file,
            "--expect-cold-receipt-object-sha256", cold_object,
            "--expect-evidence-file-sha256", evidence_file,
            "--expect-evidence-object-sha256", evidence_object,
            "--expect-release-attacks-file-sha256", release_file,
            "--expect-release-attacks-object-sha256", release_object]
        stage = "outer"
        run("outer", [*outer_common, "--output-file", str(targets["outer"]),
            "--expect-outer-sha256", PINS["outer"]], stage, control,
            args.stage_timeout_seconds)
        outer = document(targets["outer"], "outer_verification_sha256")
        outer_file = file_sha(targets["outer"])
        outer_object = outer["outer_verification_sha256"]
        stage = "seal"
        run("seal", ["--manifest-dir", str(targets["manifests"]),
            "--outer-file", str(targets["outer"]),
            "--output-dir", str(targets["seal"]),
            "--expect-builder-sha256", PINS["seal"],
            "--expect-outer-file-sha256", outer_file,
            "--expect-outer-object-sha256", outer_object,
            "--expect-manifest-receipt-file-sha256", manifest_file,
            "--expect-manifest-receipt-object-sha256", manifest_object,
            "--expect-payload-manifest-sha256", payload_sha,
            "--expect-root-manifest-sha256", root_sha], stage, control,
            args.stage_timeout_seconds)
        seal = document(targets["seal"] / "seal_candidate.json",
                        "seal_candidate_sha256")
        stage = "terminal"
        run("terminal", ["--core-control-dir", str(core_control),
            "--cold-control-dir", str(targets["cold_control"]),
            "--evidence-dir", str(targets["evidence"]),
            "--release-attacks-file", str(targets["release_attacks"]),
            "--manifest-dir", str(targets["manifests"]),
            "--outer-file", str(targets["outer"]),
            "--seal-dir", str(targets["seal"]),
            "--output-dir", str(targets["terminal"]),
            "--expect-replay-sha256", PINS["terminal"],
            "--expect-seal-candidate-file-sha256",
                file_sha(targets["seal"] / "seal_candidate.json"),
            "--expect-seal-candidate-object-sha256", seal["seal_candidate_sha256"],
            "--expect-seal-payload-manifest-sha256",
                file_sha(targets["seal"] / "seal_payload_manifest.sha256"),
            "--expect-seal-root-manifest-sha256",
                file_sha(targets["seal"] / "seal_root_manifest.sha256"),
            "--expect-outer-file-sha256", outer_file,
            "--expect-outer-object-sha256", outer_object,
            "--expect-manifest-receipt-file-sha256", manifest_file,
            "--expect-manifest-receipt-object-sha256", manifest_object], stage,
            control, args.stage_timeout_seconds)
        terminal_receipt_path = targets["terminal"] / "terminal_receipt.json"
        terminal_replay_path = targets["terminal"] / "terminal_replay.json"
        terminal_receipt = document(terminal_receipt_path, "terminal_receipt_sha256")
        terminal_replay = document(terminal_replay_path, "terminal_replay_sha256")
        need({entry.name for entry in targets["terminal"].iterdir()} == {
                 "PASS.lock", "chain_status.json", "payload_manifest.sha256",
                 "root_manifest.sha256", "terminal_receipt.json",
                 "terminal_replay.json"}
             and (targets["terminal"] / "PASS.lock").read_bytes() == PASS_BYTES
             and terminal_receipt.get("status") == TERMINAL_STATUS
             and terminal_replay.get("status") == TERMINAL_STATUS
             and terminal_receipt.get("authority_minted") is True
             and terminal_receipt.get("manifest_authorized") is True
             and terminal_receipt.get("Source_W")
                 == "UNCHANGED_BY_SOURCE_G_C29_V2_TERMINAL"
             and terminal_receipt.get("CM2") == "NO-GO_FOR_CLAIM",
             "exact final terminal")
        body = {"schema": BASE + "release-chain-watch-receipt.v1",
            "status": TERMINAL_STATUS, "completed_at_utc": now(),
            "release_unit_name": args.unit_name,
            "release_invocation_id": invocation,
            "release_pinset_file_sha256": file_sha(control / "pinset.json"),
            "release_pinset_object_sha256": pinset["pinset_sha256"],
            "core_unit_name": core["unit_name"],
            "core_invocation_id": core["systemd_invocation_id"],
            "terminal_receipt_file_sha256": file_sha(terminal_receipt_path),
            "terminal_receipt_object_sha256": terminal_receipt["terminal_receipt_sha256"],
            "terminal_replay_file_sha256": file_sha(terminal_replay_path),
            "terminal_replay_object_sha256": terminal_replay["terminal_replay_sha256"],
            "terminal_root_manifest_sha256":
                file_sha(targets["terminal"] / "root_manifest.sha256"),
            "authority_minted": True, "formal_credit": 0,
            "manifest_authorized": True,
            "C29": "AUTHORIZED_TERMINAL_SOURCE_G_POST_C27R2_FIBRE_AUTHORITY",
            "Source_W": "UNCHANGED", "D02": "BLOCKED_COMPOSITE",
            "D03": "UNAUTHORIZED", "D04": "NOT_MINTED", "Gate5": "10/18",
            "CM2": "NO-GO_FOR_CLAIM"}
        watch = dict(body)
        watch["watch_receipt_sha256"] = digest(watch)
        write_json(control / "watch_receipt.json", watch)
        write_once(control / "PASS.lock", WATCH_PASS)
        return watch
    except BaseException as error:
        failure(control, stage, error)
        raise


def self_test() -> dict[str, Any]:
    test = paths("c29-v2-release-self-test-targets")
    need(len(test) == 11 and all(valid_sha(value) for value in PINS.values()),
         "watcher fixtures")
    return {"status": "PASS_C29_V2_RELEASE_CHAIN_WATCHER_SELF_TEST",
            "formal_credit": 0, "C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--preflight-only", action="store_true")
    for name in ("stem", "unit-name", "core-control-dir",
                 "expect-core-receipt-file-sha256",
                 "expect-core-receipt-object-sha256", "expect-watcher-sha256"):
        parser.add_argument("--" + name)
    parser.add_argument("--stage-timeout-seconds", type=int, default=86_400)
    args = parser.parse_args()
    fields = ("stem", "unit_name", "core_control_dir",
              "expect_core_receipt_file_sha256",
              "expect_core_receipt_object_sha256", "expect_watcher_sha256")
    try:
        if args.self_test:
            need(not args.preflight_only
                 and all(getattr(args, field) is None for field in fields),
                 "self-test arguments")
            result = self_test()
        else:
            need(all(getattr(args, field) is not None for field in fields)
                 and 600 <= args.stage_timeout_seconds <= 172_800,
                 "run arguments")
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
