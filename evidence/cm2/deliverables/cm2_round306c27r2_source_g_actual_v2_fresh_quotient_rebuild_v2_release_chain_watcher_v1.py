#!/usr/bin/env python3
"""Fail-closed gated watcher for the complete C27R2 release chain.

No release path is created until the unique formal-r2 service, exact terminal
core receipt, frozen source pins, all stage self-tests, and every fresh target
pass.  Stages are cold replay, evidence, 20 release attacks, manifests,
independent outer verification, conditional seal, then independent terminal
byte replay.  C28 and C29 remain unauthorized and are never started here.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
AUDIT = ROOT / ".cm2-runtime/audit"
PYTHON = Path("/usr/bin/python3.12")
PROGRAMS = {
    "cold": ROOT / ("deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_"
                    "quotient_rebuild_v2_release_cold_replay_runner_v1.py"),
    "evidence": ROOT / ("deliverables/cm2_round306c27r2_source_g_actual_v2_"
                        "fresh_quotient_rebuild_v2_release_evidence_bundle_"
                        "builder_v1.py"),
    "attacks": ROOT / ("deliverables/cm2_round306c27r2_source_g_actual_v2_"
                       "fresh_quotient_rebuild_v2_release_only_attack_harness_v1.py"),
    "manifests": ROOT / ("deliverables/cm2_round306c27r2_source_g_actual_v2_"
                         "fresh_quotient_rebuild_v2_release_manifest_builder_v1.py"),
    "outer": ROOT / ("deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_"
                     "quotient_rebuild_v2_release_outer_verifier_v1.py"),
    "seal": ROOT / ("deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_"
                    "quotient_rebuild_v2_release_terminal_seal_builder_v1.py"),
    "terminal": ROOT / ("deliverables/cm2_round306c27r2_source_g_actual_v2_"
                        "fresh_quotient_rebuild_v2_terminal_byte_replay_v1.py"),
}
PROGRAM_PINS = {
    "cold": "cbba1bbb2229ffed8c20b687985b8bff80a9da27c54004e2c9309803c71095b6",
    "evidence": "beb339c6fd8ab0b5b3b4effde8563c8b8a30eec2733e5a3bdf4b85038cec8fe3",
    "attacks": "52708604cf76f5912c8eea8ff9de55febdc60deb871c57ca5c259262a114681f",
    "manifests": "9a41ae25f5082dadf075441c840d58a96bf9bfdcc584c7946ea7011915c00744",
    "outer": "303dbb8383e7e8103b6b9d39e622b07300ffd00be289bcd82298120fdfd6d2e2",
    "seal": "981054ba4ddd044f0b568e418583aef2d3a6ee18679f6d13da9035ef5ef8d72d",
    "terminal": "f088bf08794e278569593b4a7f52c7c5b35636d0ac2a376483e786a862664a0f",
    "python": "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118",
}
TERMINAL_STATUS = (
    "PASS_C27R2_TERMINAL_BYTE_REPLAY__FORMAL_C27R2_AUTHORITY_MINTED"
)
PASS_BYTES = b"PASS_C27R2_AUTHORITY_V2_TERMINAL_BYTE_REPLAY__C28_C29_UNAUTHORIZED\n"


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


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace(
        "+00:00", "Z")


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns,
            value.st_uid, value.st_gid)


def file_sha(path: Path) -> str:
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                 | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular singleton:" + str(path))
        state = hashlib.sha256()
        while block := os.read(fd, 4 << 20):
            state.update(block)
        need(fingerprint(before) == fingerprint(os.fstat(fd)),
             "stable SHA/stat:" + str(path))
        return state.hexdigest()
    finally:
        os.close(fd)


def strict_load(payload: bytes) -> Any:
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
    payload = path.read_bytes()
    need(payload.endswith(b"\n"), "JSON newline:" + str(path))
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
                 | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        offset = 0
        while offset < len(payload):
            offset += os.write(fd, payload[offset:])
        os.fsync(fd)
    finally:
        os.close(fd)


def write_json(path: Path, value: Any) -> None:
    write_once(path, canonical(value) + b"\n")


def source_pins(expect_self: str) -> dict[str, str]:
    need(valid_sha(expect_self) and file_sha(SELF) == expect_self,
         "watcher self pin")
    observed = {name: file_sha(path) for name, path in PROGRAMS.items()}
    observed["python"] = file_sha(PYTHON)
    need(observed == PROGRAM_PINS, "all release source/Python pins")
    return {**observed, "watcher": expect_self}


def target_paths(args: argparse.Namespace) -> dict[str, Path]:
    result = {name: Path(getattr(args, name + "_dir")).absolute()
              for name in ("control", "cold_control", "cold_output", "cold_run",
                           "evidence", "release_attacks", "manifests", "outer",
                           "seal", "terminal")}
    need(len(set(result.values())) == len(result)
         and all(path.parent == AUDIT for path in result.values())
         and all(not path.exists() for path in result.values()),
         "ten fresh distinct release paths")
    return result


def run(program: Path, argv: list[str], label: str,
        control: Path | None = None) -> bytes:
    runtime = f"/run/user/{os.getuid()}"
    completed = subprocess.run(
        [str(PYTHON), "-I", "-B", str(program), *argv], cwd=ROOT,
        env={"PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
             "PYTHONHASHSEED": "30662729", "PYTHONDONTWRITEBYTECODE": "1",
             "XDG_RUNTIME_DIR": runtime,
             "DBUS_SESSION_BUS_ADDRESS": "unix:path=" + runtime + "/bus"},
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False)
    if control is not None:
        write_once(control / (label + ".stdout.log"), completed.stdout)
        write_once(control / (label + ".stderr.log"), completed.stderr)
        write_once(control / (label + ".exit_code.txt"),
                   (str(completed.returncode) + "\n").encode("ascii"))
    need(completed.returncode == 0 and completed.stderr == b""
         and completed.stdout.endswith(b"\n"),
         "clean release stage:" + label)
    value = strict_load(completed.stdout[:-1])
    need(type(value) is dict and canonical(value) == completed.stdout[:-1],
         "canonical stage stdout:" + label)
    return completed.stdout


def self_tests() -> dict[str, str]:
    result: dict[str, str] = {}
    for name, program in PROGRAMS.items():
        stdout = run(program, ["--self-test"], name + "_selftest")
        result[name] = hashlib.sha256(stdout).hexdigest()
    return result


def initial_preflight(args: argparse.Namespace, paths: dict[str, Path]) \
        -> dict[str, Any]:
    common = ["--expect-core-receipt-file-sha256",
              args.expect_core_receipt_file_sha256,
              "--expect-core-receipt-object-sha256",
              args.expect_core_receipt_object_sha256]
    evidence_stdout = run(PROGRAMS["evidence"], [
        "--preflight-only", "--output-dir", str(paths["evidence"]),
        *common, "--expect-builder-sha256", PROGRAM_PINS["evidence"]],
        "evidence_preflight")
    cold_stdout = run(PROGRAMS["cold"], [
        "--preflight-only", "--control-dir", str(paths["cold_control"]),
        "--output-dir", str(paths["cold_output"]),
        "--run-dir", str(paths["cold_run"]), *common,
        "--expect-helper-sha256", PROGRAM_PINS["cold"]], "cold_preflight")
    need(all(not path.exists() for path in paths.values()),
         "preflight creates zero release paths")
    return {"evidence_preflight_sha256": hashlib.sha256(evidence_stdout).hexdigest(),
            "cold_preflight_sha256": hashlib.sha256(cold_stdout).hexdigest()}


def failure(control: Path, stage: str, error: BaseException) -> None:
    body = {"schema": "cm2.round306c27r2.release-chain-failure.v1",
            "status": "FAILED_CLOSED_RELEASE_CHAIN__ZERO_CREDIT",
            "failed_at_utc": utc_now(), "stage": stage,
            "error": f"{type(error).__name__}:{error}",
            "formal_credit": 0, "manifest_authorized": False,
            "C27R2": "UNAUTHORIZED", "C28_C29": "UNAUTHORIZED",
            "CM2": "NO-GO_FOR_CLAIM"}
    value = {**body, "failure_receipt_sha256": digest(body)}
    if not (control / "failure_receipt.json").exists():
        write_json(control / "failure_receipt.json", value)
    if not (control / "FAILED.lock").exists():
        write_once(control / "FAILED.lock",
                   b"FAILED_CLOSED_C27R2_RELEASE_CHAIN\n")


def execute(args: argparse.Namespace) -> dict[str, Any]:
    pins = (args.expect_core_receipt_file_sha256,
            args.expect_core_receipt_object_sha256,
            args.expect_watcher_sha256)
    need(all(valid_sha(value) for value in pins), "core/watcher pins")
    sources = source_pins(args.expect_watcher_sha256)
    paths = target_paths(args)
    tests = self_tests()
    preflight = initial_preflight(args, paths)
    if args.preflight_only:
        return {"status": "PASS_ALL_RELEASE_SOURCES_CORE_AND_TEN_FRESH_PATH_PREFLIGHT__NO_PATHS_CREATED_ZERO_CREDIT",
                "source_pins": sources, "self_test_stdout_sha256": tests,
                **preflight}
    control = paths["control"]
    stage = "create_control"
    try:
        control.mkdir(mode=0o700)
        pinset_body = {
            "schema": "cm2.round306c27r2.release-chain-pinset.v1",
            "status": "PASS_CORE_SOURCE_AND_FRESH_RELEASE_PATH_PINSET__ZERO_CREDIT",
            "core_receipt_file_sha256": args.expect_core_receipt_file_sha256,
            "core_receipt_object_sha256": args.expect_core_receipt_object_sha256,
            "source_pins": sources,
            "targets": {name: str(path.relative_to(ROOT))
                        for name, path in paths.items()},
            "self_test_stdout_sha256": tests, "preflight": preflight,
            "formal_credit": 0, "manifest_authorized": False,
            "C27R2": "UNAUTHORIZED", "C28_C29": "UNAUTHORIZED",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        pinset = {**pinset_body, "pinset_sha256": digest(pinset_body)}
        write_json(control / "pinset.json", pinset)
        common = ["--expect-core-receipt-file-sha256",
                  args.expect_core_receipt_file_sha256,
                  "--expect-core-receipt-object-sha256",
                  args.expect_core_receipt_object_sha256]
        stage = "cold_replay"
        run(PROGRAMS["cold"], ["--control-dir", str(paths["cold_control"]),
            "--output-dir", str(paths["cold_output"]), "--run-dir",
            str(paths["cold_run"]), *common, "--expect-helper-sha256",
            PROGRAM_PINS["cold"]], stage, control)
        cold_receipt_path = paths["cold_control"] / "cold_replay_receipt.json"
        cold = document(cold_receipt_path, "cold_replay_receipt_sha256")
        stage = "evidence"
        run(PROGRAMS["evidence"], ["--output-dir", str(paths["evidence"]),
            *common, "--expect-builder-sha256", PROGRAM_PINS["evidence"]],
            stage, control)
        evidence_path = paths["evidence"] / "evidence_bundle.json"
        evidence = document(evidence_path, "evidence_bundle_sha256")
        stage = "release_attacks"
        run(PROGRAMS["attacks"], [
            "--evidence-dir", str(paths["evidence"]),
            "--cold-control-dir", str(paths["cold_control"]),
            "--cold-output-dir", str(paths["cold_output"]),
            "--cold-run-dir", str(paths["cold_run"]),
            "--output-dir", str(paths["release_attacks"]),
            "--expect-harness-sha256", PROGRAM_PINS["attacks"], *common,
            "--expect-evidence-file-sha256", file_sha(evidence_path),
            "--expect-evidence-object-sha256", evidence["evidence_bundle_sha256"],
            "--expect-cold-receipt-file-sha256", file_sha(cold_receipt_path),
            "--expect-cold-receipt-object-sha256",
            cold["cold_replay_receipt_sha256"]], stage, control)
        release_path = paths["release_attacks"] / "release_attacks.json"
        release = document(release_path, "release_attack_harness_sha256")
        stage = "manifests"
        run(PROGRAMS["manifests"], [
            "--evidence-dir", str(paths["evidence"]),
            "--cold-control-dir", str(paths["cold_control"]),
            "--cold-output-dir", str(paths["cold_output"]),
            "--cold-run-dir", str(paths["cold_run"]),
            "--release-attacks-file", str(release_path),
            "--output-dir", str(paths["manifests"]),
            "--expect-builder-sha256", PROGRAM_PINS["manifests"],
            "--expect-evidence-file-sha256", file_sha(evidence_path),
            "--expect-evidence-object-sha256", evidence["evidence_bundle_sha256"],
            "--expect-cold-receipt-file-sha256", file_sha(cold_receipt_path),
            "--expect-cold-receipt-object-sha256",
            cold["cold_replay_receipt_sha256"],
            "--expect-release-attacks-file-sha256", file_sha(release_path),
            "--expect-release-attacks-object-sha256",
            release["release_attack_harness_sha256"]], stage, control)
        manifest_receipt_path = paths["manifests"] / "manifest_receipt.json"
        manifest_receipt = document(manifest_receipt_path,
                                    "manifest_receipt_sha256")
        payload_sha = file_sha(paths["manifests"] / "payload_manifest.sha256")
        root_sha = file_sha(paths["manifests"] / "root_manifest.sha256")
        stage = "outer"
        outer_stdout = run(PROGRAMS["outer"], [
            "--manifest-dir", str(paths["manifests"]),
            "--expect-outer-sha256", PROGRAM_PINS["outer"],
            "--expect-manifest-receipt-file-sha256",
            file_sha(manifest_receipt_path),
            "--expect-manifest-receipt-object-sha256",
            manifest_receipt["manifest_receipt_sha256"],
            "--expect-payload-manifest-sha256", payload_sha,
            "--expect-root-manifest-sha256", root_sha], stage, control)
        paths["outer"].mkdir(mode=0o700)
        outer_path = paths["outer"] / "outer_verification.json"
        write_once(outer_path, outer_stdout)
        outer = document(outer_path, "outer_verification_sha256")
        stage = "seal"
        run(PROGRAMS["seal"], ["--manifest-dir", str(paths["manifests"]),
            "--outer-file", str(outer_path), "--output-dir", str(paths["seal"]),
            "--expect-builder-sha256", PROGRAM_PINS["seal"],
            "--expect-outer-file-sha256", file_sha(outer_path),
            "--expect-outer-object-sha256", outer["outer_verification_sha256"],
            "--expect-manifest-receipt-file-sha256",
            file_sha(manifest_receipt_path),
            "--expect-manifest-receipt-object-sha256",
            manifest_receipt["manifest_receipt_sha256"],
            "--expect-payload-manifest-sha256", payload_sha,
            "--expect-root-manifest-sha256", root_sha], stage, control)
        seal_path = paths["seal"] / "seal_candidate.json"
        seal = document(seal_path, "seal_candidate_sha256")
        stage = "terminal_byte_replay"
        run(PROGRAMS["terminal"], ["--seal-dir", str(paths["seal"]),
            "--manifest-dir", str(paths["manifests"]),
            "--outer-file", str(outer_path), "--output-dir",
            str(paths["terminal"]), "--expect-replay-sha256",
            PROGRAM_PINS["terminal"], "--expect-seal-candidate-file-sha256",
            file_sha(seal_path), "--expect-seal-candidate-object-sha256",
            seal["seal_candidate_sha256"],
            "--expect-seal-payload-manifest-sha256",
            file_sha(paths["seal"] / "seal_payload_manifest.sha256"),
            "--expect-seal-root-manifest-sha256",
            file_sha(paths["seal"] / "seal_root_manifest.sha256"),
            "--expect-outer-file-sha256", file_sha(outer_path),
            "--expect-outer-object-sha256", outer["outer_verification_sha256"],
            "--expect-manifest-receipt-file-sha256",
            file_sha(manifest_receipt_path),
            "--expect-manifest-receipt-object-sha256",
            manifest_receipt["manifest_receipt_sha256"]], stage, control)
        terminal_receipt = document(paths["terminal"] / "terminal_receipt.json",
                                    "terminal_receipt_sha256")
        terminal_replay = document(paths["terminal"] / "terminal_replay.json",
                                   "terminal_replay_sha256")
        need(terminal_receipt.get("status") == TERMINAL_STATUS
             and terminal_replay.get("status") == TERMINAL_STATUS
             and terminal_receipt.get("authority_minted") is True
             and terminal_receipt.get("manifest_authorized") is True
             and terminal_receipt.get("C27R2")
                 == "AUTHORIZED_TERMINAL_SOURCE_G_QUOTIENT_AUTHORITY"
             and terminal_receipt.get("C28") == "UNAUTHORIZED_NOT_STARTED"
             and terminal_receipt.get("C29") == "UNAUTHORIZED_NOT_STARTED"
             and (paths["terminal"] / "PASS.lock").read_bytes() == PASS_BYTES,
             "exact terminal authorization without downstream start")
        body = {
            "schema": "cm2.round306c27r2.release-chain-watch-receipt.v1",
            "status": TERMINAL_STATUS, "completed_at_utc": utc_now(),
            "pinset_object_sha256": pinset["pinset_sha256"],
            "terminal_receipt_file_sha256":
                file_sha(paths["terminal"] / "terminal_receipt.json"),
            "terminal_receipt_object_sha256":
                terminal_receipt["terminal_receipt_sha256"],
            "terminal_replay_file_sha256":
                file_sha(paths["terminal"] / "terminal_replay.json"),
            "terminal_replay_object_sha256":
                terminal_replay["terminal_replay_sha256"],
            "authority_minted": True, "formal_credit": 0,
            "manifest_authorized": True,
            "C27R2": "AUTHORIZED_TERMINAL_SOURCE_G_QUOTIENT_AUTHORITY",
            "C28_C29": "UNAUTHORIZED_NOT_STARTED",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        receipt = {**body, "watch_receipt_sha256": digest(body)}
        write_json(control / "watch_receipt.json", receipt)
        write_once(control / "PASS.lock",
                   b"PASS_C27R2_RELEASE_CHAIN_TERMINAL__C28_C29_UNAUTHORIZED\n")
        return receipt
    except BaseException as error:
        if control.exists():
            failure(control, stage, error)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--expect-core-receipt-file-sha256", required=True)
    parser.add_argument("--expect-core-receipt-object-sha256", required=True)
    parser.add_argument("--expect-watcher-sha256", required=True)
    for name in ("control", "cold-control", "cold-output", "cold-run",
                 "evidence", "release-attacks", "manifests", "outer", "seal",
                 "terminal"):
        parser.add_argument("--" + name + "-dir", required=True)
    args = parser.parse_args()
    try:
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
