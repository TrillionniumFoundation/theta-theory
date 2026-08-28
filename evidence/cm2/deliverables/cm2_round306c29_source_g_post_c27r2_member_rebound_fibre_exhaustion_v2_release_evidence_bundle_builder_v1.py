#!/usr/bin/env python3
"""Freeze the successful C29-v2 core and cold replay as zero-credit evidence."""

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
PREFIX = "cm2_round306c29_source_g_post_c27r2_member_rebound_fibre_exhaustion_v2"
BASE = "cm2.round306c29.source-g-post-c27r2-member-rebound-fibre-exhaustion.v2."
CORE_SCHEMA = BASE + "gated-dual-terminal-seed-core-receipt.v1"
CORE_STATUS = "PASS_C29_V2_DUAL_TERMINAL_ADAPTERS_SEED1_PRODUCER_SEED2_NO_IMPORT_VERIFIER_AND_34_ATTACKS__ZERO_CREDIT_PENDING_RELEASE_TERMINAL"
COLD_SCHEMA = BASE + "release-cold-replay-receipt.v1"
COLD_STATUS = "PASS_C29_V2_FRESH_NO_IMPORT_COLD_BYTE_REPLAY_WITH_ALL_CORE_INPUT_PRE_POST_SHA_STAT__ZERO_CREDIT"
RESULT_SCHEMA = BASE + "producer-result.v1"
VERIFY_SCHEMA = BASE + "independent-verification.v1"
ATTACK_SCHEMA = BASE + "coherent-attacks.v1"
EVIDENCE_SCHEMA = BASE + "release-evidence-bundle.v1"
EVIDENCE_STATUS = "PASS_C29_V2_DUAL_PREDECESSOR_CORE_COLD_PROCESS_AND_BYTE_EVIDENCE_FROZEN__ZERO_CREDIT"
CORE_PASS = b"PASS_C29_V2_DUAL_TERMINAL_SEED_CORE__ZERO_CREDIT\n"
COLD_PASS = b"PASS_C29_V2_RELEASE_COLD_REPLAY__ZERO_CREDIT\n"
C27_PINS = {
    "root": "1f65a624c889773e3104c4311788fc06be04d6ca92e033205074b8cc7f5b27fc",
    "receipt_file": "feccb0b9290bd82ac1d8e78e8e7a21d4f25e0ca3aa3556cc3f0bb6007f61c3dd",
    "receipt_object": "8afbd127c9518f569c2f7b3edcdbe9e0ebf77d88bcca855822e58d21e5cfe782",
    "replay_file": "b480df4b8caaf9876a48720f92a8fb6d86e2b1b5966bcc71b0022c5e49fc12ee",
    "replay_object": "216d2592c49b0302de0042677ce54c96cd5ad1fcb32231da02b39c003cb837e8",
    "pass": "5fe4140b3e8f38196e9ca68cd336ae29be1c8847c7685526f08aa4d7173d7348",
}
EXPECTED_MATH = {
    "members": 502_204, "representations": 549_616,
    "post_C27R2_components": 43_684, "official_keys": 124,
    "component_key_incidences": 60_296,
    "component_key_multiplicity_census": {
        "1": 27_108, "2": 16_556, "3": 8, "4": 8, "5": 4},
    "family_member_census": {"G2A": 5_264, "G2B": 10_128,
        "NON_GRAPH": 55_604, "PRESERVED": 126_468,
        "R2": 295_336, "R292": 9_404},
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
         "JSON newline:" + str(path))
    value = strict(payload[:-1])
    need(type(value) is dict and canonical(value) == payload[:-1],
         "canonical JSON:" + str(path))
    body = dict(value)
    claim = body.pop(closure, None)
    need(valid_sha(claim) and claim == digest(body),
         "object closure:" + str(path))
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


def service_success(unit: str, invocation: str) -> None:
    need(type(unit) is str and unit.endswith(".service")
         and type(invocation) is str and len(invocation) == 32,
         "service identity syntax")
    completed = subprocess.run(["/usr/bin/systemctl", "--user", "show", unit,
        "-p", "ActiveState", "-p", "SubState", "-p", "Result",
        "-p", "ExecMainCode", "-p", "ExecMainStatus", "-p", "InvocationID"],
        cwd=ROOT, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False)
    need(completed.returncode == 0 and completed.stderr == b"",
         "systemd query")
    fields = dict(line.split("=", 1) for line in
                  completed.stdout.decode("ascii").splitlines() if "=" in line)
    need(fields.get("ActiveState") == "active"
         and fields.get("SubState") == "exited"
         and fields.get("Result") == "success"
         and fields.get("ExecMainCode") in {"1", "exited"}
         and fields.get("ExecMainStatus") == "0"
         and fields.get("InvocationID") == invocation,
         "core service clean success")


def validate_core(control: Path, expected_file: str, expected_object: str) \
        -> tuple[dict[str, Any], dict[str, Any], dict[str, Path]]:
    need(control.parent == AUDIT and control.is_dir() and not control.is_symlink(),
         "core control path")
    receipt_path = control / "core_receipt.json"
    receipt = document(receipt_path, "core_receipt_sha256")
    need(file_sha(receipt_path) == expected_file
         and receipt["core_receipt_sha256"] == expected_object
         and receipt.get("schema") == CORE_SCHEMA
         and receipt.get("status") == CORE_STATUS
         and receipt.get("formal_credit") == 0
         and receipt.get("manifest_authorized") is False
         and receipt.get("Source_W") == "UNCHANGED_BY_SOURCE_G_C29_V2_CORE"
         and receipt.get("CM2") == "NO-GO_FOR_CLAIM"
         and (control / "PASS.lock").read_bytes() == CORE_PASS
         and not (control / "FAILED.lock").exists(), "core terminal receipt")
    service_success(receipt["unit_name"], receipt["systemd_invocation_id"])
    pinset = document(control / "pinset.json", "pinset_sha256")
    need(receipt.get("pinset_file_sha256") == file_sha(control / "pinset.json")
         and receipt.get("pinset_object_sha256") == pinset["pinset_sha256"]
         and pinset.get("C27R2_terminal", {}).get("root") == C27_PINS["root"]
         and all(pinset.get("C27R2_terminal", {}).get(key) == value
                 for key, value in C27_PINS.items())
         and all(valid_sha(pinset.get("C28_terminal", {}).get(key))
                 for key in ("root", "receipt_file", "receipt_object",
                             "replay_file", "replay_object", "pass")),
         "dual predecessor pinset")
    targets = {name: ROOT / raw for name, raw in pinset.get("targets", {}).items()}
    need(set(targets) >= {"candidate", "verification", "attacks",
                          "c27_adapter", "c28_adapter"}
         and all(path.is_relative_to(AUDIT) and path.exists()
                 and not path.is_symlink() for path in targets.values()),
         "complete core target map")
    result = document(targets["candidate"] / (PREFIX + "_result.json"),
                      "result_sha256")
    verification = document(targets["verification"], "verification_sha256")
    attacks = document(targets["attacks"], "attacks_sha256")
    need(result.get("schema") == RESULT_SCHEMA
         and result.get("recomputed_census") == EXPECTED_MATH
         and verification.get("schema") == VERIFY_SCHEMA
         and verification.get("independent_recomputed_census") == EXPECTED_MATH
         and verification.get("candidate_result_object_sha256")
             == result["result_sha256"]
         and verification.get("no_import_or_execution_of_producer") is True
         and attacks.get("schema") == ATTACK_SCHEMA
         and attacks.get("attack_census")
             == {"required": 34, "rejected": 34, "accepted": 0}
         and attacks.get("post_rejection_private_case_cleanup", {}).get(
             "all_34_private_cases_removed") is True
         and attacks.get("post_rejection_private_case_cleanup", {}).get(
             "remaining_work_files_regular_single_link") is True
         and all(value.get("formal_credit") == 0 for value in
                 (result, verification, attacks)), "core math/verifier/attacks")
    return receipt, pinset, targets


def validate_cold(control: Path, output: Path, run: Path,
                  core_file: str, core_object: str,
                  expected_file: str, expected_object: str) -> dict[str, Any]:
    need(all(path.is_relative_to(AUDIT) and path.exists()
             and not path.is_symlink() for path in (control, output, run)),
         "cold paths")
    receipt_path = control / "cold_replay_receipt.json"
    receipt = document(receipt_path, "cold_replay_receipt_sha256")
    need(file_sha(receipt_path) == expected_file
         and receipt["cold_replay_receipt_sha256"] == expected_object
         and receipt.get("schema") == COLD_SCHEMA
         and receipt.get("status") == COLD_STATUS
         and receipt.get("core_receipt_file_sha256") == core_file
         and receipt.get("core_receipt_object_sha256") == core_object
         and receipt.get("formal_verification_byte_identical") is True
         and receipt.get("all_core_inputs_pre_post_sha_stat_identical") is True
         and receipt.get("numeric_exit_code") == 0
         and receipt.get("signal") is None
         and receipt.get("stderr_empty") is True
         and receipt.get("formal_credit") == 0
         and receipt.get("manifest_authorized") is False
         and (control / "PASS.lock").read_bytes() == COLD_PASS
         and not (control / "FAILED.lock").exists(), "cold replay boundary")
    need((output / "verification.json").is_file()
         and (run / "run_attestation.json").is_file(), "cold artifacts")
    return receipt


def inventory(paths: list[Path]) -> dict[str, dict[str, Any]]:
    files: set[Path] = set()
    for path in paths:
        if path.is_file():
            files.add(path.absolute())
            continue
        need(path.is_dir() and not path.is_symlink(), "inventory directory")
        for current, directories, names in os.walk(path):
            base = Path(current)
            need(all(not (base / name).is_symlink() for name in directories),
                 "inventory directory symlink")
            for name in names:
                item = (base / name).absolute()
                need(item.is_file() and not item.is_symlink(),
                     "inventory regular member")
                files.add(item)
    result: dict[str, dict[str, Any]] = {}
    for path in sorted(files):
        before = path.stat(follow_symlinks=False)
        relative = str(path.relative_to(ROOT))
        result[relative] = {"sha256": file_sha(path), "size": before.st_size,
                            "stat_fingerprint": list(fingerprint(before)),
                            "O_NOFOLLOW": True, "single_link": True}
    return result


def execute(args: argparse.Namespace) -> dict[str, Any]:
    pins = (args.expect_builder_sha256, args.expect_core_receipt_file_sha256,
            args.expect_core_receipt_object_sha256,
            args.expect_cold_receipt_file_sha256,
            args.expect_cold_receipt_object_sha256)
    need(all(valid_sha(value) for value in pins)
         and file_sha(SELF) == args.expect_builder_sha256, "builder/dynamic pins")
    core_control = Path(args.core_control_dir).absolute()
    cold_control = Path(args.cold_control_dir).absolute()
    cold_output = Path(args.cold_output_dir).absolute()
    cold_run = Path(args.cold_run_dir).absolute()
    output = Path(args.output_dir).absolute()
    need(output.parent == AUDIT and not output.exists(), "fresh evidence output")
    core, _, targets = validate_core(core_control,
        args.expect_core_receipt_file_sha256,
        args.expect_core_receipt_object_sha256)
    cold = validate_cold(cold_control, cold_output, cold_run,
        args.expect_core_receipt_file_sha256,
        args.expect_core_receipt_object_sha256,
        args.expect_cold_receipt_file_sha256,
        args.expect_cold_receipt_object_sha256)
    if args.preflight_only:
        return {"status": "PASS_C29_V2_CORE_COLD_AND_FRESH_EVIDENCE_PREFLIGHT__NO_OUTPUT_ZERO_CREDIT"}
    entries = inventory([core_control, *targets.values(), cold_control,
                         cold_output, cold_run, SELF])
    raw = ("\n".join(f"{value['sha256']}  {path}"
                     for path, value in sorted(entries.items())) + "\n").encode("ascii")
    body = {"schema": EVIDENCE_SCHEMA, "status": EVIDENCE_STATUS,
            "built_at_utc": now(),
            "core_receipt_file_sha256": args.expect_core_receipt_file_sha256,
            "core_receipt_object_sha256": args.expect_core_receipt_object_sha256,
            "core_unit_name": core["unit_name"],
            "core_invocation_id": core["systemd_invocation_id"],
            "cold_replay_receipt_file_sha256": args.expect_cold_receipt_file_sha256,
            "cold_replay_receipt_object_sha256": args.expect_cold_receipt_object_sha256,
            "cold_verification_object_sha256": cold["verification_object_sha256"],
            "evidence_member_count": len(entries),
            "evidence_inventory_sha256": hashlib.sha256(raw).hexdigest(),
            "attestations": entries, "exact_census": EXPECTED_MATH,
            "dual_predecessor_pins": {
                "C27R2": core["C27R2_source_terminal"],
                "C28": core["C28_source_terminal"]},
            "core_attacks_rejected": 34,
            "cold_replay_byte_identical": True,
            "formal_credit": 0, "manifest_authorized": False,
            "C29": "UNAUTHORIZED_PENDING_RELEASE_ATTACKS_MANIFEST_OUTER_SEAL_TERMINAL_REPLAY",
            "Source_W": "UNCHANGED_BY_SOURCE_G_C29_V2_EVIDENCE",
            "CM2": "NO-GO_FOR_CLAIM"}
    receipt = dict(body)
    receipt["evidence_bundle_sha256"] = digest(receipt)
    output.mkdir(mode=0o700)
    write_once(output / "evidence_inventory.sha256", raw)
    write_once(output / "evidence_bundle.json", canonical(receipt) + b"\n")
    return receipt


def self_test() -> dict[str, Any]:
    need(sum(EXPECTED_MATH["component_key_multiplicity_census"].values())
         == EXPECTED_MATH["post_C27R2_components"]
         and all(valid_sha(value) for value in C27_PINS.values()), "fixtures")
    return {"status": "PASS_C29_V2_RELEASE_EVIDENCE_BUILDER_SELF_TEST",
            "formal_credit": 0, "C29": "UNAUTHORIZED",
            "CM2": "NO-GO_FOR_CLAIM"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--preflight-only", action="store_true")
    for name in ("core-control-dir", "cold-control-dir", "cold-output-dir",
                 "cold-run-dir", "output-dir",
                 "expect-core-receipt-file-sha256",
                 "expect-core-receipt-object-sha256",
                 "expect-cold-receipt-file-sha256",
                 "expect-cold-receipt-object-sha256",
                 "expect-builder-sha256"):
        parser.add_argument("--" + name)
    args = parser.parse_args()
    fields = ("core_control_dir", "cold_control_dir", "cold_output_dir",
              "cold_run_dir", "output_dir", "expect_core_receipt_file_sha256",
              "expect_core_receipt_object_sha256",
              "expect_cold_receipt_file_sha256",
              "expect_cold_receipt_object_sha256", "expect_builder_sha256")
    try:
        if args.self_test:
            need(not args.preflight_only
                 and all(getattr(args, field) is None for field in fields),
                 "self-test arguments")
            result = self_test()
        else:
            need(all(getattr(args, field) is not None for field in fields),
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
