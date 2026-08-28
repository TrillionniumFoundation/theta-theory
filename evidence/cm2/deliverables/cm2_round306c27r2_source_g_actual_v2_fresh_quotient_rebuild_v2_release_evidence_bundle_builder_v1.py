#!/usr/bin/env python3
"""Build a zero-credit C27R2 release evidence bundle after the formal core.

The unique v6 formal-r2 service and its exact terminal core receipt are hard
gates.  Missing, running, failed, noncanonical, linked, drifting, or incomplete
core state is rejected before the requested output files are created.  This
stage packages evidence only; it cannot authorize C27R2 or downstream work.
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
UNIT = "cm2-c27r2-source-g-authority-v2-v6-formal-r2-20260808T180523.service"
INVOCATION_ID = "aa82e1c6611f4910ae80b94307fb9ca9"
STEM = "c27r2-source-g-authority-v2-v6-formal-r2-20260808T180523"
CORE = {
    "control": AUDIT / (STEM + "-control"),
    "candidate": AUDIT / (STEM + "-candidate"),
    "producer_run": AUDIT / (STEM + "-producer-run"),
    "verifier_output": AUDIT / (STEM + "-verifier-output"),
    "verifier_run": AUDIT / (STEM + "-verifier-run"),
    "attack_work": AUDIT / (STEM + "-attack-work"),
    "attack_run": AUDIT / (STEM + "-attack-run"),
}
PYTHON = Path("/usr/bin/python3.12")
SOURCES = {
    "producer": ROOT / ("deliverables/cm2_round306c27r2_source_g_actual_v2_"
                        "fresh_quotient_rebuild_v2_producer_v4.py"),
    "independent_verifier": ROOT / ("deliverables/cm2_round306c27r2_source_g_"
                                     "actual_v2_fresh_quotient_rebuild_v2_"
                                     "independent_verifier_v4.py"),
    "coherent_attack_harness": ROOT / ("deliverables/cm2_round306c27r2_source_g_"
                                        "actual_v2_fresh_quotient_rebuild_v2_"
                                        "coherent_attack_harness_v4.py"),
    "transaction_runner": ROOT / ("deliverables/cm2_round306c27r2_source_g_"
                                   "actual_v2_fresh_quotient_rebuild_v2_"
                                   "transaction_runner_v4.py"),
    "gated_watcher": ROOT / ("deliverables/cm2_round306c27r2_source_g_actual_v2_"
                              "fresh_quotient_rebuild_v2_gated_dual_seed_"
                              "watcher_v6.py"),
    "python": PYTHON,
}
SOURCE_PINS = {
    "producer": "578d0ce0d39d14dede9d9528be383abb3d4140c26bcac75917fe860a98bb158b",
    "independent_verifier": "acc66bbff3717e16bf56b15f9498070d97a4be1b0cd9253a79b7cae598b4082f",
    "coherent_attack_harness": "1d501ca968853712743524e7aba16d29dadd62b9d46458b53e0421aef2072007",
    "transaction_runner": "7ce75edac7e1aad904718e173cf6ed178f6d2631ba1f5cb4253bcf2c1e121d63",
    "gated_watcher": "68c1d70ca55e4d17f1b727a6b1eda8343c1a6eaecd61df43ed5449198a88331d",
    "python": "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118",
}
TRANSACTION_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "gated-dual-seed-transaction-receipt.v4"
)
TRANSACTION_STATUS = (
    "PASS_GATE_SEED1_FOUR_FILE_CANDIDATE_SEED2_NO_IMPORT_REPLAY_AND_21_"
    "ATTACKS__ZERO_CREDIT_PENDING_OUTER_SEAL_AND_TERMINAL_REPLAY"
)
RESULT_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "producer-result.v1"
)
VERIFICATION_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "independent-verification.v1"
)
ATTACK_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "coherent-attack-harness.v1"
)
RUN_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "process-run-attestation.v4"
)
RUN_STATUS = (
    "PASS_PROCESS_TRANSACTION_EXIT0_NULL_SIGNAL_EMPTY_STDERR_PRE_POST_"
    "AND_OUTPUTS__ZERO_CREDIT"
)
CORE_PASS = b"PASS_C27R2_AUTHORITY_V2_GATED_DUAL_SEED_CORE__ZERO_CREDIT\n"
CANDIDATE_FILES = {
    "member_to_post_component.jsonl.gz",
    "old_c15_component_to_post_component.jsonl.gz",
    "post_component_census.jsonl.gz", "result.json",
}
RUN_FILES = {
    "PASS.lock", "exit_code.txt", "input_post.json", "input_pre.json",
    "output_validation.json", "run_attestation.json", "runner_start.json",
    "signal.json", "stderr.log", "stdout.log", "timing.json",
}
CONTROL_FILES = {
    "PASS.lock", "attack_command_spec.json", "candidate_validation.json",
    "coherent_attacks_runner.exit_code.txt",
    "coherent_attacks_runner.stderr.log",
    "coherent_attacks_runner.stdout.log",
    "dual_seed_descriptor_agreement.json",
    "independent_verifier_runner.exit_code.txt",
    "independent_verifier_runner.stderr.log",
    "independent_verifier_runner.stdout.log", "pinset.json", "preflight.json",
    "producer_command_spec.json", "producer_runner.exit_code.txt",
    "producer_runner.stderr.log", "producer_runner.stdout.log",
    "transaction_receipt.json", "verifier_command_spec.json",
}
EXPECTED_MATH = {
    "frozen_C15_members": 502_204,
    "frozen_C15_components": 57_876,
    "proof_derived_component_edges": 14_860,
    "successful_DSU_merges": 14_192,
    "cycle_edges": 668,
    "post_C27R2_components": 43_684,
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
    return (type(value) is str and len(value) == 64
            and all(character in "0123456789abcdef" for character in value))


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace(
        "+00:00", "Z")


def strict_load(payload: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(type(key) is str and key not in result, "unique JSON key")
            result[key] = value
        return result
    return json.loads(payload, object_pairs_hook=pairs,
                      parse_constant=lambda value: (_ for _ in ()).throw(
                          ValueError(value)))


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns,
            value.st_uid, value.st_gid)


class Capture:
    def __init__(self, path: Path, label: str):
        self.path = path.absolute()
        try:
            self.path.relative_to(ROOT)
        except ValueError:
            need(self.path == PYTHON, "outside workspace:" + str(path))
        need(self.path.resolve(strict=True) == self.path,
             "canonical path:" + label)
        self.label = label
        self.fd = os.open(self.path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                          | getattr(os, "O_NOFOLLOW", 0))
        self.before = os.fstat(self.fd)
        need(stat.S_ISREG(self.before.st_mode) and self.before.st_nlink == 1,
             "regular singleton:" + label)
        self.sha256 = self._hash()

    def _hash(self) -> str:
        os.lseek(self.fd, 0, os.SEEK_SET)
        state = hashlib.sha256()
        while block := os.read(self.fd, 4 << 20):
            state.update(block)
        os.lseek(self.fd, 0, os.SEEK_SET)
        need(fingerprint(os.fstat(self.fd)) == fingerprint(self.before),
             "stable fd:" + self.label)
        return state.hexdigest()

    def bytes(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        chunks: list[bytes] = []
        while block := os.read(self.fd, 4 << 20):
            chunks.append(block)
        os.lseek(self.fd, 0, os.SEEK_SET)
        need(fingerprint(os.fstat(self.fd)) == fingerprint(self.before),
             "stable read:" + self.label)
        return b"".join(chunks)

    def document(self, closure: str | None = None) -> dict[str, Any]:
        payload = self.bytes()
        need(payload.endswith(b"\n"), "JSON newline:" + self.label)
        value = strict_load(payload[:-1])
        need(type(value) is dict and canonical(value) == payload[:-1],
             "canonical JSON:" + self.label)
        if closure is not None:
            body = dict(value)
            claim = body.pop(closure, None)
            need(valid_sha(claim) and claim == digest(body),
                 "object closure:" + self.label)
        return value

    def attest(self) -> dict[str, Any]:
        need(fingerprint(os.fstat(self.fd)) == fingerprint(self.before)
             and fingerprint(os.stat(self.path, follow_symlinks=False))
                 == fingerprint(self.before)
             and self._hash() == self.sha256,
             "pre/post SHA/stat/path identity:" + self.label)
        return {"path": str(self.path.relative_to(ROOT)),
                "sha256": self.sha256, "size": self.before.st_size,
                "stat_fingerprint": list(fingerprint(self.before)),
                "O_NOFOLLOW": True, "single_link": True}

    def close(self) -> None:
        os.close(self.fd)


def file_sha(path: Path) -> str:
    capture = Capture(path, str(path))
    try:
        return capture.sha256
    finally:
        capture.close()


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


def exact_files(directory: Path, expected: set[str], label: str) -> None:
    need(directory.is_dir() and not directory.is_symlink(),
         "real directory:" + label)
    entries = list(directory.iterdir())
    need({entry.name for entry in entries} == expected
         and all(entry.is_file() and not entry.is_symlink() for entry in entries),
         "exact file inventory:" + label)


def service_success() -> dict[str, str]:
    completed = subprocess.run(
        ["/usr/bin/systemctl", "--user", "show", UNIT,
         "-p", "ActiveState", "-p", "SubState", "-p", "Result",
         "-p", "ExecMainCode", "-p", "ExecMainStatus", "-p", "InvocationID"],
        cwd=ROOT, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    need(completed.returncode == 0 and completed.stderr == b"",
         "query predecessor service")
    fields = dict(line.split("=", 1) for line in
                  completed.stdout.decode("ascii").splitlines() if "=" in line)
    need(fields.get("ActiveState") == "active"
         and fields.get("SubState") == "exited"
         and fields.get("Result") == "success"
         and fields.get("ExecMainCode") in {"1", "exited"}
         and fields.get("ExecMainStatus") == "0"
         and fields.get("InvocationID") == INVOCATION_ID,
         "unique predecessor service clean success")
    return fields


def validate_run(directory: Path, stage: str) -> dict[str, Any]:
    exact_files(directory, RUN_FILES, stage + " run")
    need((directory / "exit_code.txt").read_bytes() == b"0\n"
         and (directory / "signal.json").read_bytes() == b"null\n"
         and (directory / "stderr.log").read_bytes() == b""
         and (directory / "input_pre.json").read_bytes()
             == (directory / "input_post.json").read_bytes(),
         stage + " exact process and input closure")
    capture = Capture(directory / "run_attestation.json", stage + " attestation")
    try:
        value = capture.document("run_attestation_sha256")
        need(value.get("schema") == RUN_SCHEMA
             and value.get("status") == RUN_STATUS
             and value.get("stage") == stage
             and value.get("numeric_exit_code") == 0
             and value.get("signal") is None
             and value.get("timed_out") is False
             and value.get("stderr_empty") is True
             and value.get("input_pre_post_sha_stat_identical") is True
             and value.get("formal_credit") == 0
             and value.get("manifest_authorized") is False,
             stage + " run attestation semantics")
        return value
    finally:
        capture.close()


def recursive_captures() -> list[Capture]:
    captures: list[Capture] = []
    for role, directory in sorted(CORE.items()):
        need(directory.is_dir() and not directory.is_symlink(),
             "complete core directory:" + role)
        for current, directory_names, file_names in os.walk(directory):
            current_path = Path(current)
            need(directory_names == sorted(directory_names)
                 or type(directory_names) is list, "walk directory list")
            for name in directory_names:
                need(not (current_path / name).is_symlink(),
                     "no core symlink directory:" + role)
            for name in sorted(file_names):
                captures.append(Capture(current_path / name,
                                        role + "/" + str(
                                            (current_path / name).relative_to(directory))))
    return captures


def validate_core(expected_file_sha: str, expected_object_sha: str) \
        -> tuple[dict[str, Any], list[Capture], dict[str, Any]]:
    need(valid_sha(expected_file_sha) and valid_sha(expected_object_sha),
         "core receipt SHA pins")
    service = service_success()
    exact_files(CORE["control"], CONTROL_FILES, "core control")
    exact_files(CORE["candidate"], CANDIDATE_FILES, "candidate")
    exact_files(CORE["verifier_output"], {"verification.json"},
                "verifier output")
    exact_files(CORE["producer_run"], RUN_FILES, "producer run")
    exact_files(CORE["verifier_run"], RUN_FILES, "verifier run")
    exact_files(CORE["attack_run"], RUN_FILES, "attack run")
    need((CORE["control"] / "PASS.lock").read_bytes() == CORE_PASS
         and not (CORE["control"] / "FAILED.lock").exists()
         and all((CORE[name] / "stderr.log").read_bytes() == b""
                 for name in ("producer_run", "verifier_run", "attack_run")),
         "core PASS-only and empty stderr")
    need(all(file_sha(SOURCES[name]) == value
             for name, value in SOURCE_PINS.items()),
         "frozen source/Python pins")
    receipt_capture = Capture(CORE["control"] / "transaction_receipt.json",
                              "core transaction receipt")
    captures: list[Capture] = [receipt_capture]
    try:
        receipt = receipt_capture.document("transaction_receipt_sha256")
        need(receipt_capture.sha256 == expected_file_sha
             and receipt["transaction_receipt_sha256"] == expected_object_sha
             and receipt.get("schema") == TRANSACTION_SCHEMA
             and receipt.get("status") == TRANSACTION_STATUS
             and receipt.get("formal_credit") == 0
             and receipt.get("manifest_authorized") is False
             and receipt.get("C27R2")
                 == "UNAUTHORIZED_PENDING_OUTER_SEAL_AND_TERMINAL_REPLAY"
             and receipt.get("C28_C29") == "UNAUTHORIZED"
             and receipt.get("CM2") == "NO-GO_FOR_CLAIM",
             "exact terminal core receipt")
        closures = receipt.get("exact_process_closures")
        need(type(closures) is dict
             and closures == {
                 "attacks_started_only_after_seed1_and_seed2_pass": True,
                 "canonical_quotient_and_three_descriptors_agree": True,
                 "gate_passed_before_any_transaction_directory": True,
                 "outer_verifier_or_seal_or_terminal_replay_created": False,
                 "seed1_exact_four_gzip_canonical_count_closure": True,
                 "seed1_numeric_exit0_signal_null_stderr_empty_pre_post": True,
                 "seed2_no_import_independent_full_candidate_replay": True,
                 "seed2_numeric_exit0_signal_null_stderr_empty_pre_post": True,
             }, "exact core process closure inventory")
        result_capture = Capture(CORE["candidate"] / "result.json",
                                 "candidate result")
        verification_capture = Capture(
            CORE["verifier_output"] / "verification.json", "verification")
        attacks_capture = Capture(
            CORE["attack_work"] / "coherent_attacks.json", "attacks")
        captures.extend((result_capture, verification_capture, attacks_capture))
        result = result_capture.document("result_sha256")
        verification = verification_capture.document("verification_sha256")
        attacks = attacks_capture.document("attack_harness_sha256")
        need(result.get("schema") == RESULT_SCHEMA
             and result.get("exact_census") == EXPECTED_MATH
             and result.get("formal_credit") == 0
             and result.get("manifest_authorized") is False,
             "candidate result math/credit")
        need(verification.get("schema") == VERIFICATION_SCHEMA
             and verification.get("candidate_result_object_sha256")
                 == result["result_sha256"]
             and verification.get("producer_imported_or_executed") is False
             and verification.get("actual_v2_seed_used") == "seed2"
             and verification.get("formal_credit") == 0,
             "no-import seed2 verification")
        need(attacks.get("schema") == ATTACK_SCHEMA
             and attacks.get("attack_count") == 21
             and attacks.get("rejected") == 21
             and attacks.get("accepted") == 0
             and attacks.get("authoritative_candidate_pre_post_sha256_identical")
                 is True and attacks.get("formal_credit") == 0,
             "21/21 core attacks")
        runs = {stage: validate_run(CORE[role], stage) for stage, role in (
            ("producer", "producer_run"),
            ("independent_verifier", "verifier_run"),
            ("coherent_attacks", "attack_run"),
        )}
        captures.extend(recursive_captures())
        return receipt, captures, {"service": service, "runs": runs,
                                   "result": result,
                                   "verification": verification,
                                   "attacks": attacks}
    except BaseException:
        for capture in captures:
            capture.close()
        raise


def execute(args: argparse.Namespace) -> dict[str, Any]:
    need(valid_sha(args.expect_builder_sha256)
         and file_sha(SELF) == args.expect_builder_sha256,
         "evidence builder self pin")
    output_dir = Path(args.output_dir).absolute()
    need(output_dir.parent == AUDIT and not output_dir.exists(),
         "fresh release evidence directory")
    receipt, captures, validated = validate_core(
        args.expect_core_receipt_file_sha256,
        args.expect_core_receipt_object_sha256)
    try:
        if args.preflight_only:
            return {
                "status": "PASS_EXACT_FORMAL_CORE_AND_FRESH_EVIDENCE_PREFLIGHT__NO_OUTPUT_CREATED_ZERO_CREDIT"
            }
        attestations: dict[str, dict[str, Any]] = {}
        for capture in captures:
            path = str(capture.path.relative_to(ROOT))
            if path not in attestations:
                attestations[path] = capture.attest()
        attestations = dict(sorted(attestations.items()))
        manifest_lines = [f"{value['sha256']}  {path}"
                          for path, value in attestations.items()]
        manifest = ("\n".join(manifest_lines) + "\n").encode("ascii")
        body = {
            "schema": "cm2.round306c27r2.source-g-authority-v2.release-evidence-bundle.v1",
            "status": "PASS_EXACT_V6_FORMAL_R2_CORE_SERVICE_RECEIPT_CANDIDATE_DUAL_VERIFIER_21_ATTACKS_AND_PROCESS_CLOSURE__ZERO_CREDIT",
            "built_at_utc": utc_now(), "predecessor_unit": UNIT,
            "predecessor_invocation_id": INVOCATION_ID,
            "core_transaction_receipt_file_sha256":
                args.expect_core_receipt_file_sha256,
            "core_transaction_receipt_object_sha256":
                args.expect_core_receipt_object_sha256,
            "core_transaction_status": receipt["status"],
            "core_member_count": len(attestations),
            "core_inventory_sha256": hashlib.sha256(manifest).hexdigest(),
            "attestations": attestations,
            "validated_projection": {
                "exact_census": EXPECTED_MATH,
                "producer_run_object_sha256":
                    validated["runs"]["producer"]["run_attestation_sha256"],
                "verifier_run_object_sha256":
                    validated["runs"]["independent_verifier"][
                        "run_attestation_sha256"],
                "attack_run_object_sha256":
                    validated["runs"]["coherent_attacks"][
                        "run_attestation_sha256"],
                "candidate_result_object_sha256":
                    validated["result"]["result_sha256"],
                "verification_object_sha256":
                    validated["verification"]["verification_sha256"],
                "attacks_object_sha256":
                    validated["attacks"]["attack_harness_sha256"],
            },
            "cold_replay_completed": False,
            "release_attacks_completed": False,
            "formal_credit": 0, "manifest_authorized": False,
            "C27R2": "UNAUTHORIZED_PENDING_COLD_RELEASE_ATTACKS_MANIFEST_OUTER_AND_TERMINAL_REPLAY",
            "C28_C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM",
        }
        result = {**body, "evidence_bundle_sha256": digest(body)}
        output_dir.mkdir(mode=0o700)
        write_once(output_dir / "core_inventory.sha256", manifest)
        write_once(output_dir / "evidence_bundle.json", canonical(result) + b"\n")
        return result
    finally:
        for capture in captures:
            capture.close()


def self_test() -> dict[str, Any]:
    body = {"schema": "fixture", "formal_credit": 0}
    closed = {**body, "sha256": digest(body)}
    need(closed["sha256"] == digest(body)
         and SOURCE_PINS["gated_watcher"].startswith("68c1d70c"),
         "canonical closure/source fixture")
    return {"schema": "cm2.round306c27r2.release-evidence-builder-self-test.v1",
            "status": "PASS_CANONICAL_CLOSURE_AND_FROZEN_SOURCE_PIN_FIXTURE",
            "formal_credit": 0, "C27R2": "UNAUTHORIZED",
            "CM2": "NO-GO_FOR_CLAIM"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--output-dir")
    parser.add_argument("--expect-core-receipt-file-sha256")
    parser.add_argument("--expect-core-receipt-object-sha256")
    parser.add_argument("--expect-builder-sha256")
    args = parser.parse_args()
    fields = ("output_dir", "expect_core_receipt_file_sha256",
              "expect_core_receipt_object_sha256", "expect_builder_sha256")
    try:
        if args.self_test:
            need(not args.preflight_only
                 and all(getattr(args, field) is None for field in fields),
                 "self-test accepts no run arguments")
            result = self_test()
        else:
            need(all(getattr(args, field) is not None for field in fields),
                 "all run arguments")
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
