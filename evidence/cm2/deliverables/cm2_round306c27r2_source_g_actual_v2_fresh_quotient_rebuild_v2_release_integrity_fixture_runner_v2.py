#!/usr/bin/env python3
"""Run the exact 44 real C27R2 release-boundary integrity fixtures.

The runner is append-only and permanently zero-credit.  It first invokes the
independent boundary validator once with a file/object-pinned empty override.
It then executes 44 isolated validator subprocesses.  Each negative case has
exactly one allowlisted logical override mapped to ``CASE_ROOT/override``;
ordinary copies are used sequentially and removed after the case, so ext4
without reflink remains bounded well below 3 GiB.  Authoritative files are
snapshotted before and after the suite and are never edited.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
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
VALIDATOR_DEFAULT = ROOT / "deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_quotient_rebuild_v2_release_repair_boundary_independent_validator_v2.py"
PREFIX = "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
OVERRIDE_SCHEMA = PREFIX + "release-repair-boundary-override-map.v2"
RESULT_SCHEMA = PREFIX + "release-integrity-fixture.v2"
RESULT_STATUS = (
    "PASS_C27R2_RELEASE_BOUNDARY_CONTROL_AND_44_OF_44_REAL_SUBPROCESS_"
    "INTEGRITY_FIXTURES_REJECTED__ZERO_CREDIT"
)
PASS_BYTES = b"PASS_C27R2_RELEASE_BOUNDARY_44_REAL_FIXTURES__ZERO_CREDIT\n"
EMPTY_SHA = hashlib.sha256(b"").hexdigest()
MAX_CAPTURE_BYTES = 1 << 20

CASE_RUN_FILES = {
    "PASS.lock", "exit_code.txt", "signal.json", "stderr.log",
    "stdout.log", "timing.json", "input_pre.json", "input_post.json",
    "output_validation.json", "runner_start.json", "run_attestation.json",
}
CASE_RUN_PASS = (
    b"PASS_C27R2_RELEASE_BOUNDARY_EXPECTED_REJECTION_PROCESS_"
    b"TRANSACTION__ZERO_CREDIT\n"
)
CASE_RUN_SCHEMA = PREFIX + "release-integrity-case-process-run.v2"
CASE_RUN_STATUS = (
    "PASS_EXPECTED_VALIDATOR_EXIT2_NULL_SIGNAL_NO_OUTPUT_AND_AUTHORITY_"
    "UNCHANGED__ZERO_CREDIT"
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
    "manifest-duplicate-and-traversal",
    "root-member-substitution",
    "outer-fake-release-count-coherent-reclosure",
    "terminal-byte-mismatch",
]


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


def file_record(path: Path) -> dict[str, Any]:
    path = path.absolute()
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                         | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "authoritative singleton regular file")
        state = hashlib.sha256()
        while block := os.read(descriptor, 4 << 20):
            state.update(block)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    current = os.stat(path, follow_symlinks=False)
    need(fingerprint(before) == fingerprint(after) == fingerprint(current),
         "authoritative current full9stat")
    return {"sha256": state.hexdigest(), "size": before.st_size,
            "stat_fingerprint": list(fingerprint(before))}


def strict_document(path: Path, closure: str) -> dict[str, Any]:
    payload = path.read_bytes()
    need(payload.endswith(b"\n") and not payload.endswith(b"\n\n"),
         "canonical document newline")
    value = json.loads(payload[:-1])
    need(type(value) is dict and canonical(value) == payload[:-1],
         "canonical JSON")
    body = dict(value)
    claim = body.pop(closure, None)
    need(valid_sha(claim) and claim == digest(body), "object closure")
    return value


def write_once(path: Path, payload: bytes, mode: int = 0o400) -> None:
    path = path.absolute()
    need(path.parent.is_dir() and not path.parent.is_symlink()
         and not path.exists() and not path.is_symlink(), "fresh write path")
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                         | getattr(os, "O_CLOEXEC", 0)
                         | getattr(os, "O_NOFOLLOW", 0), mode)
    try:
        os.write(descriptor, payload)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


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
    result.extend([Path(args.validator).absolute(), SELF])
    return result


def authority_snapshot(args: argparse.Namespace) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for root in authoritative_roots(args):
        need(root.exists() and not root.is_symlink(), "authority root exists")
        paths = [root] if root.is_file() else sorted(
            path for path in root.rglob("*") if path.is_file())
        for path in paths:
            need(not path.is_symlink(), "no authoritative symlink")
            logical = str(path.relative_to(ROOT))
            need(logical not in result, "disjoint authority roots")
            result[logical] = file_record(path)
    return result


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
    try:
        completed = subprocess.run(command, cwd=ROOT, env=environment,
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, check=False, timeout=timeout)
        timed_out = False
        code = completed.returncode
        stdout = completed.stdout
        stderr = completed.stderr
    except subprocess.TimeoutExpired as error:
        timed_out = True
        code = None
        stdout = error.stdout or b""
        stderr = error.stderr or b""
    return {"numeric_exit_code": code if code is not None and code >= 0 else None,
            "signal": -code if code is not None and code < 0 else None,
            "timed_out": timed_out,
            "elapsed_seconds": round(time.monotonic() - started, 6),
            "stdout": stdout, "stderr": stderr}


def authority_projection(snapshot: dict[str, Any]) -> str:
    return hashlib.sha256(b"".join(
        canonical({"path": path, **record}) + b"\n"
        for path, record in sorted(snapshot.items()))).hexdigest()


def relative_workspace(path: Path) -> str:
    try:
        relative = path.absolute().relative_to(ROOT)
    except ValueError as error:
        raise Rejected("path outside workspace:" + str(path)) from error
    need(relative.parts and all(part not in {"", ".", ".."}
                                for part in relative.parts),
         "canonical workspace-relative path")
    return str(relative)


def write_case_process_transaction(process_dir: Path, record: dict[str, Any],
                                   projection: str) -> None:
    """Persist one successful wrapper transaction around an expected reject.

    The child validator's exit 2 is the asserted negative-test outcome.  The
    surrounding fixture transaction therefore exits 0 and has an empty
    stderr, matching the common eleven-file process contract consumed by the
    release-repair back half.
    """
    need(not process_dir.exists() and not process_dir.is_symlink(),
         "fresh case process directory")
    process_dir.mkdir(mode=0o700)
    input_state = {
        "schema": CASE_RUN_SCHEMA + ".input.v1",
        "mode": "formal",
        "case": record["case"],
        "ordinal": record["ordinal"],
        "authority_projection_sha256": projection,
        "override_map_file_sha256": record["override_map_file_sha256"],
        "override_map_object_sha256": record["override_map_object_sha256"],
        "validator_sha256": record["validator_sha256"],
        "runner_sha256": record["runner_sha256"],
        "python_sha256": record["python_sha256"],
        "formal_credit": 0,
    }
    input_bytes = canonical(input_state) + b"\n"
    start = {
        "schema": CASE_RUN_SCHEMA + ".start.v1",
        "mode": "formal", "case": record["case"],
        "ordinal": record["ordinal"],
        "started_at_utc": record["started_at_utc"],
        "command_argv_sha256": record["command_argv_sha256"],
        "exact_environment": record["exact_environment"],
        "formal_credit": 0,
    }
    timing = {
        "schema": CASE_RUN_SCHEMA + ".timing.v1",
        "started_at_utc": record["started_at_utc"],
        "finished_at_utc": record["finished_at_utc"],
        "elapsed_seconds": record["elapsed_seconds"],
        "timed_out": False,
        "formal_credit": 0,
    }
    output_validation = {
        "schema": CASE_RUN_SCHEMA + ".output-validation.v1",
        "case": record["case"],
        "expected_validator_rejection": True,
        "child_numeric_exit_code": 2,
        "child_signal": None,
        "child_stdout_sha256": record["stdout_sha256"],
        "child_stderr_sha256": record["stderr_sha256"],
        "child_stdout_size": record["stdout_size"],
        "child_stderr_size": record["stderr_size"],
        "child_validator_output_created": False,
        "bounded_capture": True,
        "formal_credit": 0,
    }
    wrapper_stdout = canonical({
        "schema": CASE_RUN_SCHEMA + ".stdout.v1",
        "status": CASE_RUN_STATUS,
        "case": record["case"], "formal_credit": 0,
        "CM2": "NO-GO_FOR_CLAIM",
    }) + b"\n"
    write_once(process_dir / "exit_code.txt", b"0\n")
    write_once(process_dir / "signal.json", b"null\n")
    write_once(process_dir / "stderr.log", b"")
    write_once(process_dir / "stdout.log", wrapper_stdout)
    write_once(process_dir / "timing.json", canonical(timing) + b"\n")
    write_once(process_dir / "input_pre.json", input_bytes)
    write_once(process_dir / "input_post.json", input_bytes)
    write_once(process_dir / "output_validation.json",
               canonical(output_validation) + b"\n")
    write_once(process_dir / "runner_start.json", canonical(start) + b"\n")
    members = {
        name: file_record(process_dir / name)["sha256"]
        for name in sorted(CASE_RUN_FILES - {"PASS.lock", "run_attestation.json"})
    }
    body = {
        "schema": CASE_RUN_SCHEMA, "status": CASE_RUN_STATUS,
        "mode": "formal", "case": record["case"],
        "ordinal": record["ordinal"],
        "numeric_exit_code": 0, "signal": None, "timed_out": False,
        "stderr_empty": True,
        "input_pre_post_sha_stat_identical": True,
        "expected_child_rejection": True,
        "child_numeric_exit_code": 2, "child_signal": None,
        "child_timed_out": False,
        "child_validator_output_created": False,
        "child_command_argv_sha256": record["command_argv_sha256"],
        "child_stdout_sha256": record["stdout_sha256"],
        "child_stderr_sha256": record["stderr_sha256"],
        "exact_inventory": sorted(CASE_RUN_FILES),
        "member_file_sha256": members,
        "PASS_lock_file_sha256": hashlib.sha256(CASE_RUN_PASS).hexdigest(),
        "authority_projection_sha256": projection,
        "formal_credit": 0, "manifest_authorized": False,
        "C27R2": "UNAUTHORIZED_PENDING_REPAIRED_RELEASE_CHAIN",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    attestation = dict(body)
    attestation["run_attestation_sha256"] = digest(body)
    write_once(process_dir / "run_attestation.json",
               canonical(attestation) + b"\n")
    write_once(process_dir / "PASS.lock", CASE_RUN_PASS)
    need({path.name for path in process_dir.iterdir()} == CASE_RUN_FILES
         and (process_dir / "input_pre.json").read_bytes()
             == (process_dir / "input_post.json").read_bytes(),
         "exact eleven-file successful case process transaction")


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
        "outer": args.future_outer_relative,
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
        ("manifest-duplicate-and-traversal", "terminal_payload",
            "manifest-duplicate-traversal", {}),
        ("root-member-substitution", "terminal_root", "manifest-substitute", {}),
        ("outer-fake-release-count-coherent-reclosure", "outer", "fake-outer", {}),
        ("terminal-byte-mismatch", "terminal", "fake-terminal", {}),
    ]
    need([row[0] for row in specs] == CASE_NAMES, "exact ordered 44 cases")
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
    elif mutation in {"fake-outer", "fake-terminal"}:
        target.mkdir()
        if mutation == "fake-outer":
            body = {"schema": PREFIX + "fake-outer.v1", "released": 44,
                    "formal_credit": 0, "manifest_authorized": True,
                    "C27R2": "MINTED", "CM2": "NO-GO_FOR_CLAIM"}
            body["fake_outer_sha256"] = digest(body)
            (target / "outer_verification.json").write_bytes(canonical(body) + b"\n")
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
        elif mutation == "manifest-reorder":
            lines = target.read_bytes().splitlines()
            need(len(lines) > 1, "reorder manifest rows")
            target.write_bytes(b"\n".join(reversed(lines)) + b"\n")
        elif mutation == "manifest-duplicate-traversal":
            lines = target.read_bytes().splitlines()
            need(bool(lines), "manifest rows")
            target.write_bytes(b"\n".join(lines + [lines[0],
                b"0" * 64 + b"  ../outside"]) + b"\n")
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
    process = subprocess.Popen(command, cwd=ROOT, env=environment,
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
        stdout, stderr = process.communicate(timeout=timeout)
        code = process.returncode
        timed_out = False
    except (subprocess.TimeoutExpired, Rejected):
        process.kill()
        stdout, stderr = process.communicate()
        code = process.returncode
        timed_out = True
    return {"numeric_exit_code": code if code >= 0 else None,
            "signal": -code if code < 0 else None, "timed_out": timed_out,
            "elapsed_seconds": round(time.monotonic() - started, 6),
            "stdout": stdout, "stderr": stderr}


def execute_case(args: argparse.Namespace, spec: dict[str, Any], index: int,
                 work: Path, environment: dict[str, str]) -> dict[str, Any]:
    case_root = work / f"private-c27r2-release-fixture-{index:02d}-{spec['name']}"
    case_root.mkdir(mode=0o700)
    prepared = prepare_override(spec, case_root)
    mapping = closed_map("private", [{"logical_path": prepared["logical_path"],
        "physical_path": prepared["physical_path"]}])
    map_path = case_root / "override-map.json"
    write_once(map_path, canonical(mapping) + b"\n")
    out_file = case_root / "validator-output.json"
    missing_i = spec["name"] == "missing-isolated-python-flag"
    case_env = dict(environment)
    if spec["name"] == "wrong-PYTHONHASHSEED":
        case_env["PYTHONHASHSEED"] = "1"
    barrier = spec["mutation"] in {"atomic", "toctou"}
    command = validator_command(args, "private", map_path, case_root,
        out_file, spec["changes"], missing_i, barrier)
    if barrier:
        result = invoke_barrier(command, case_env, case_root,
            spec["mutation"] == "toctou", args.case_timeout_seconds)
    else:
        result = invoke(command, case_env, args.case_timeout_seconds)
    need(result["numeric_exit_code"] == 2 and result["signal"] is None
         and result["timed_out"] is False and not out_file.exists(),
         "real validator subprocess rejected without output:" + spec["name"])
    transcript = {
        "ordinal": index, "case": spec["name"],
        "logical_override": prepared["logical_path"],
        "mutation": prepared["mutation"],
        "private_copy_bytes": prepared["private_copy_bytes"],
        "override_map_file_sha256": file_record(map_path)["sha256"],
        "override_map_object_sha256": mapping["override_map_sha256"],
        "numeric_exit_code": result["numeric_exit_code"],
        "signal": result["signal"], "timed_out": result["timed_out"],
        "elapsed_seconds": result["elapsed_seconds"],
        "stdout_sha256": hashlib.sha256(result["stdout"]).hexdigest(),
        "stderr_sha256": hashlib.sha256(result["stderr"]).hexdigest(),
        "stderr_prefix": result["stderr"][:512].decode("utf-8", "replace"),
        "validator_output_created": False,
        "private_exact_one_override": True,
        "formal_credit": 0,
    }
    write_once(case_root / "stdout.log", result["stdout"])
    write_once(case_root / "stderr.log", result["stderr"])
    write_once(case_root / "case_receipt.json", canonical(transcript) + b"\n")
    remove_private(case_root / "override")
    remove_private(case_root / "private-hardlink-source")
    return transcript


def environment(args: argparse.Namespace) -> dict[str, str]:
    return {"PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
            "PYTHONHASHSEED": args.expected_python_hash_seed}


def execute(args: argparse.Namespace) -> dict[str, Any]:
    need(Path(sys.executable).absolute() == Path(args.python).absolute()
         and sys.flags.isolated == 1 and sys.dont_write_bytecode,
         "runner workspace Python -I -B")
    expected_env = environment(args)
    need({key: os.environ.get(key) for key in expected_env} == expected_env,
         "runner exact environment")
    need(file_record(Path(args.python))["sha256"]
             == args.expect_python_sha256
         and file_record(Path(args.validator))["sha256"]
             == args.expect_validator_sha256
         and file_record(SELF)["sha256"] == args.expect_runner_sha256,
         "runner/validator/Python current pins")
    work = Path(args.work_dir).absolute()
    out_file = Path(args.out_file).absolute()
    need(work.parent == AUDIT and work.name.startswith(
         "c27r2-release-repair-integrity-v2-")
         and not work.exists() and not work.is_symlink(),
         "fresh direct audit work directory")
    need(out_file.parent == work and out_file.name == "fixture_receipt.json",
         "exact output under work")
    work.mkdir(mode=0o700)
    before = authority_snapshot(args)
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
         and baseline_output.is_file(), "formal empty-override control PASS")
    baseline_value = strict_document(baseline_output, "validation_sha256")
    need(baseline_value.get("status")
             == "PASS_C27R2_RELEASE_REPAIR_BOUNDARY_FORMAL_EMPTY_OVERRIDE_CURRENT_PROCESS_INVENTORY_AND_AUTHORITY_CLOSURE__ZERO_CREDIT"
         and baseline_value.get("mode") == "formal"
         and baseline_value.get("override_count") == 0
         and baseline_value.get("formal_credit") == 0
         and baseline_value.get("manifest_authorized") is False
         and baseline_value.get("C27R2")
             == "UNAUTHORIZED_PENDING_REPAIRED_RELEASE_CHAIN",
         "control validation exact conditional state")
    write_once(control / "baseline.stdout.log", baseline["stdout"])
    write_once(control / "baseline.stderr.log", baseline["stderr"])
    records: list[dict[str, Any]] = []
    max_private = 0
    for index, spec in enumerate(case_specs(args)):
        record = execute_case(args, spec, index, work, expected_env)
        records.append(record)
        max_private = max(max_private, record["private_copy_bytes"])
    after = authority_snapshot(args)
    need(before == after, "all authoritative SHA/full9stat unchanged")
    need(len(records) == 44
         and [row["case"] for row in records] == CASE_NAMES
         and all(row["numeric_exit_code"] == 2
                 and row["signal"] is None
                 and row["timed_out"] is False
                 and row["validator_output_created"] is False
                 for row in records),
         "exact 44 real subprocess rejections")
    need(max_private < 3 * (1 << 30), "peak private ordinary copy below 3 GiB")
    authority_projection = hashlib.sha256(b"".join(
        canonical({"path": path, **record}) + b"\n"
        for path, record in sorted(before.items()))).hexdigest()
    body = {
        "schema": RESULT_SCHEMA,
        "status": RESULT_STATUS,
        "completed_at_utc": utc_now(),
        "validator_sha256": args.expect_validator_sha256,
        "runner_sha256": args.expect_runner_sha256,
        "python_sha256": args.expect_python_sha256,
        "control": {"numeric_exit_code": 0, "signal": None,
            "timed_out": False,
            "empty_override_map_file_sha256": file_record(empty_path)["sha256"],
            "empty_override_map_object_sha256": empty["override_map_sha256"],
            "validation_file_sha256": file_record(baseline_output)["sha256"],
            "validation_object_sha256": baseline_value["validation_sha256"]},
        "case_count": len(records), "rejected": len(records), "accepted": 0,
        "ordered_case_names": CASE_NAMES, "cases": records,
        "real_subprocess_per_case": True,
        "private_exact_one_override_per_case": True,
        "ordinary_copy_only": True,
        "sequential_private_copy_cleanup": True,
        "maximum_private_copy_bytes": max_private,
        "peak_private_copy_below_3GiB": True,
        "authoritative_file_count": len(before),
        "authoritative_pre_post_sha_full9stat_identical": True,
        "authoritative_projection_sha256": authority_projection,
        "fresh_cold_and_evidence_consumed": True,
        "future_outer_seal_terminal_absent_at_control": True,
        "formal_credit": 0, "manifest_authorized": False,
        "C27R2": "UNAUTHORIZED_PENDING_REPAIRED_RELEASE_CHAIN",
        "C28_C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM",
    }
    result = dict(body)
    result["fixture_receipt_sha256"] = digest(body)
    write_once(out_file, canonical(result) + b"\n")
    write_once(work / "PASS.lock", PASS_BYTES)
    return result


def self_test() -> dict[str, Any]:
    need(len(CASE_NAMES) == 44 and len(set(CASE_NAMES)) == 44,
         "exact unique 44-case inventory")
    formal = closed_map("formal", [])
    private = closed_map("private", [{"logical_path": "x/y",
                                       "physical_path": "/tmp/case/override"}])
    need(formal["override_map_sha256"] == digest({key: value for key, value
        in formal.items() if key != "override_map_sha256"})
         and private["override_map_sha256"] == digest({key: value for key, value
        in private.items() if key != "override_map_sha256"}),
        "override closure fixtures")
    with tempfile.TemporaryDirectory(prefix="c27r2-fixture-runner-v2-") as raw:
        root = Path(raw)
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
    return {"schema": RESULT_SCHEMA + ".self-test",
            "status": "PASS_EXACT_44_CASE_INVENTORY_OVERRIDE_CLOSURE_ORDINARY_"
                      "COPY_RECLOSURE_AND_PRIVATE_LINK_TINY_FIXTURES",
            "formal_reads": 0, "formal_outputs": 0,
            "formal_credit": 0, "manifest_authorized": False,
            "C27R2": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM"}


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--self-test", action="store_true")
    value.add_argument("--validator", default=str(VALIDATOR_DEFAULT))
    value.add_argument("--expect-runner-sha256")
    value.add_argument("--work-dir")
    value.add_argument("--out-file")
    value.add_argument("--control-timeout-seconds", type=int, default=21_600)
    value.add_argument("--case-timeout-seconds", type=int, default=21_600)
    for name in VALIDATOR_COMMON:
        value.add_argument("--" + name.replace("_", "-"))
    return value


def main() -> int:
    args = parser().parse_args()
    try:
        if args.self_test:
            result = self_test()
        else:
            need(args.work_dir is not None and args.out_file is not None
                 and args.expect_runner_sha256 is not None
                 and all(getattr(args, name) is not None
                         for name in VALIDATOR_COMMON),
                 "all formal runner arguments required")
            need(all(valid_sha(getattr(args, name)) for name in
                [item for item in VALIDATOR_COMMON if item.startswith("expect_")]
                + ["expect_runner_sha256"]), "all SHA pins lowercase exact")
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
