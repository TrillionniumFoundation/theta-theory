#!/usr/bin/env python3
"""Run actual-v2 with a closed, immutable pre/post input transaction."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import gzip
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import signal
import stat
import subprocess
import sys
import time
from typing import Any, Iterable


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
RUNNER = Path(__file__).resolve()
ASSEMBLER = ROOT / "deliverables/cm2_c27_primitive_twenty_family_gate_v5_actual_v2.py"
ASSEMBLER_SHA256 = "038c6a661438f9253fb00a29b9f41941bea33a3a8769a258d8dfa5763880b561"
PYTHON = Path("/usr/bin/python3.12")
PYTHON_SHA256 = "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118"
EXPECTED_LEDGER_COUNTS = {
    "candidate_ownership": 7_486_076,
    "materialized_physical_proof_join": 65_064,
    "atom_pair_incidence": 206_632,
    "atom_incidence_disposition": 483_232,
    "full_component_edge_union": 14_860,
}
EXPECTED_OUTPUT_NAMES = {
    *(name + ".jsonl.gz" for name in EXPECTED_LEDGER_COUNTS),
    "assembler_receipt.json", "manifest.sha256",
}


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def fsha(path: Path) -> str:
    state = hashlib.sha256()
    descriptor = os.open(os.fspath(path), os.O_RDONLY | os.O_CLOEXEC
                         | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular singleton:" + os.fspath(path))
        while True:
            block = os.read(descriptor, 4 << 20)
            if not block:
                break
            state.update(block)
        after = os.fstat(descriptor)
        need(identity(before) == identity(after),
             "stable hash inode:" + os.fspath(path))
    finally:
        os.close(descriptor)
    return state.hexdigest()


def identity(info: os.stat_result) -> list[int]:
    return [info.st_dev, info.st_ino, info.st_mode, info.st_nlink,
            info.st_size, info.st_mtime_ns, info.st_ctime_ns,
            info.st_uid, info.st_gid]


def fixed(relative: str) -> Path:
    need(type(relative) is str and relative and not Path(relative).is_absolute(),
         "relative input path")
    pieces = Path(relative).parts
    need(all(piece not in {"", ".", ".."} for piece in pieces),
         "canonical input path")
    current = ROOT
    for piece in pieces:
        current /= piece
        need(not current.is_symlink(), "no symlink input:" + relative)
    resolved = current.resolve(strict=True)
    need(ROOT in resolved.parents and resolved == current,
         "input inside workspace:" + relative)
    return resolved


def strict_json(path: Path) -> dict[str, Any]:
    value = strict_json_bytes(path.read_bytes(), path.name)
    need(type(value) is dict, "JSON object:" + path.name)
    return value


def strict_json_bytes(raw: bytes, label: str) -> Any:

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(key not in result, "duplicate JSON key:" + label)
            result[key] = value
        return result

    value = json.loads(raw, object_pairs_hook=pairs,
                       parse_constant=lambda item: (_ for _ in ()).throw(
                           Failure("non-finite JSON:" + item)))
    return value


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace(
        "+00:00", "Z")


def manifest_members(path: Path) -> Iterable[Path]:
    seen: set[str] = set()
    for line in path.read_text("ascii").splitlines():
        pieces = line.split("  ", 1)
        need(len(pieces) == 2 and len(pieces[0]) == 64
             and pieces[1] not in seen, "manifest row:" + path.name)
        seen.add(pieces[1])
        member = fixed(pieces[1])
        need(fsha(member) == pieces[0], "manifest member:" + pieces[1])
        yield member


def descriptor_paths(value: Any) -> Iterable[Path]:
    if type(value) is dict:
        path = value.get("path")
        has_hash = type(value.get("sha256")) is str or type(
            value.get("file_sha256")) is str
        if type(path) is str and has_hash and not Path(path).is_absolute():
            try:
                yield fixed(path)
            except (Failure, FileNotFoundError):
                pass
        for child in value.values():
            yield from descriptor_paths(child)
    elif type(value) is list:
        for child in value:
            yield from descriptor_paths(child)


def load_contract() -> Any:
    need(fsha(ASSEMBLER) == ASSEMBLER_SHA256, "pinned assembler source")
    specification = importlib.util.spec_from_file_location(
        "cm2_actual_v2_pinned_contract", ASSEMBLER)
    need(specification is not None and specification.loader is not None,
         "assembler import specification")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def input_paths(module: Any) -> list[Path]:
    paths: set[Path] = {RUNNER, ASSEMBLER, PYTHON, fixed(module.C15[0]),
                       fixed(module.INTERFACE[0])}
    documents: list[Path] = []
    for record in module.SEALS.values():
        receipt = fixed(record[0])
        payload = receipt.parent / "payload_manifest.sha256"
        root = receipt.parent / "root_manifest.sha256"
        cold = fixed(record[5])
        paths.update((receipt, payload, root, cold))
        documents.extend((receipt, cold))
        paths.update(manifest_members(payload))
        paths.update(manifest_members(root))
    for record in module.SOURCE_DOCUMENTS.values():
        document = fixed(record[0])
        paths.add(document)
        documents.append(document)
    documents.append(fixed(module.INTERFACE[0]))
    for document in documents:
        value = strict_json(document)
        paths.update(descriptor_paths(value))
    return sorted(paths, key=os.fspath)


def snapshot(paths: list[Path]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for path in paths:
        before = path.stat()
        observed = fsha(path)
        after = path.stat()
        need(identity(before) == identity(after),
             "stable snapshot:" + os.fspath(path))
        label = (str(path.relative_to(ROOT)) if ROOT in path.parents
                 else str(path))
        result[label] = {"sha256": observed, "stat": identity(after)}
    need(result[str(ASSEMBLER.relative_to(ROOT))]["sha256"]
         == ASSEMBLER_SHA256, "assembler snapshot pin")
    need(result[str(PYTHON)]["sha256"] == PYTHON_SHA256,
         "Python snapshot pin")
    return result


def exclusive(path: Path, payload: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                         | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        offset = 0
        while offset < len(payload):
            offset += os.write(descriptor, payload[offset:])
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def write_json(path: Path, value: Any) -> None:
    exclusive(path, canonical(value) + b"\n")


def fresh_paths(out_dir: Path, run_dir: Path) -> None:
    need(ROOT in out_dir.parents and ROOT in run_dir.parents,
         "outputs inside workspace")
    need(out_dir != run_dir and out_dir not in run_dir.parents
         and run_dir not in out_dir.parents, "disjoint output/run paths")
    need(not out_dir.exists() and not run_dir.exists(), "fresh output paths")
    for path in (out_dir, run_dir):
        current = path.parent
        while current != ROOT:
            need(not current.is_symlink(), "no symlink output parent")
            current = current.parent


def ledger_validation(path: Path, descriptor: dict[str, Any],
                      expected_count: int) -> dict[str, Any]:
    need(path.stat().st_size == descriptor["size"]
         and fsha(path) == descriptor["sha256"],
         "output ledger descriptor:" + path.name)
    need(descriptor["path"] == str(path.relative_to(ROOT))
         and descriptor["row_count"] == expected_count,
         "output ledger path/count:" + path.name)
    ordering = descriptor["ordering"]
    need(type(ordering) is list and ordering
         and all(type(item) is str and item for item in ordering),
         "output ledger ordering:" + path.name)
    sequence = hashlib.sha256()
    count = 0
    previous: tuple[bytes, ...] | None = None
    try:
        with gzip.open(path, "rb") as stream:
            for raw in stream:
                need(raw.endswith(b"\n"), "gzip row newline:" + path.name)
                payload = raw[:-1]
                row = strict_json_bytes(payload, path.name)
                need(type(row) is dict and canonical(row) == payload,
                     "canonical gzip row:" + path.name)
                body = dict(row)
                claim = body.pop("row_sha256", None)
                need(type(claim) is str and len(claim) == 64
                     and claim == digest(body),
                     "gzip row object closure:" + path.name)
                need(row.get("schema") == descriptor["row_schema"]
                     and type(row.get("ordinal")) is int
                     and row["ordinal"] == count
                     and row.get("formal_credit") == 0,
                     "gzip schema/ordinal/zero-credit:" + path.name)
                key = tuple(canonical(row[item]) for item in ordering)
                need(previous is None or previous < key,
                     "strict gzip ordering:" + path.name)
                previous = key
                sequence.update(claim.encode("ascii") + b"\n")
                count += 1
    except (EOFError, gzip.BadGzipFile) as error:
        raise Failure("gzip integrity:" + path.name + ":" + str(error))
    need(count == descriptor["row_count"] == expected_count
         and sequence.hexdigest() == descriptor["row_sequence_sha256"],
         "gzip count/sequence closure:" + path.name)
    return {
        "path": str(path.relative_to(ROOT)),
        "file_sha256": descriptor["sha256"],
        "file_size": descriptor["size"],
        "row_count": count,
        "row_sequence_sha256": sequence.hexdigest(),
        "gzip_integrity": "PASS",
        "canonical_rows": "PASS",
        "strict_ordering": "PASS",
        "row_object_closure": "PASS",
        "formal_credit": 0,
    }


def manifest_validation(path: Path, required: set[Path]) -> dict[str, Any]:
    raw = path.read_bytes()
    need(raw.endswith(b"\n") and raw.decode("ascii").encode("ascii") == raw,
         "canonical manifest encoding/newline")
    rows = raw.decode("ascii").splitlines()
    need(rows == sorted(rows) and len(rows) == len(set(rows)),
         "sorted unique manifest rows")
    seen: set[Path] = set()
    for ordinal, row in enumerate(rows):
        pieces = row.split("  ", 1)
        need(len(pieces) == 2 and len(pieces[0]) == 64,
             "manifest row:" + str(ordinal))
        member = fixed(pieces[1])
        need(member not in seen and fsha(member) == pieces[0],
             "manifest member closure:" + pieces[1])
        seen.add(member)
    need(required.issubset(seen) and path not in seen,
         "manifest contains all payload outputs and excludes itself")
    return {"file_sha256": fsha(path), "member_count": len(rows),
            "all_member_sha256": "PASS", "sorted_unique": True}


def output_validation(out_dir: Path,
                      receipt: dict[str, Any]) -> dict[str, Any]:
    entries = sorted(out_dir.iterdir(), key=lambda item: item.name)
    need(all(item.is_file() and not item.is_symlink() for item in entries)
         and {item.name for item in entries} == EXPECTED_OUTPUT_NAMES,
         "exact seven regular nonsymlink assembler outputs")
    descriptors = receipt["materialized_ledger_descriptors"]
    need(type(descriptors) is dict
         and set(descriptors) == set(EXPECTED_LEDGER_COUNTS),
         "exact five output ledger descriptors")
    ledgers: dict[str, Any] = {}
    for name, expected_count in EXPECTED_LEDGER_COUNTS.items():
        ledgers[name] = ledger_validation(
            out_dir / (name + ".jsonl.gz"), descriptors[name],
            expected_count)
    exact = receipt["exact_census"]
    need(exact["candidate_total"] == EXPECTED_LEDGER_COUNTS[
             "candidate_ownership"]
         and exact["materialized_physical_proof_total"]
             == EXPECTED_LEDGER_COUNTS["materialized_physical_proof_join"]
         and exact["atom_pair_incidence_total"]
             == EXPECTED_LEDGER_COUNTS["atom_pair_incidence"]
         and exact["primitive_atom_denominator"]
             == EXPECTED_LEDGER_COUNTS["atom_incidence_disposition"]
         and exact["full_component_edge_union_total"]
             == EXPECTED_LEDGER_COUNTS["full_component_edge_union"],
         "receipt/ledger exact count closure")
    required = {out_dir / (name + ".jsonl.gz")
                for name in EXPECTED_LEDGER_COUNTS}
    required.add(out_dir / "assembler_receipt.json")
    manifest = manifest_validation(out_dir / "manifest.sha256", required)
    files = {entry.name: {"sha256": fsha(entry),
                         "stat": identity(entry.stat())}
             for entry in entries}
    return {"status": "PASS_7_OF_7_GZIP_CANONICAL_COUNT_CLOSURE",
            "output_file_count": len(files), "output_files": files,
            "ledgers": ledgers, "manifest": manifest,
            "formal_credit": 0, "manifest_authorized": False}


def record_failure(run_dir: Path, stage: str, error: BaseException) -> None:
    if not run_dir.is_dir():
        return
    payload = {"schema": "cm2.actual-v2-run-failure-lock.v1",
               "status": "FAIL_CLOSED_ZERO_CREDIT",
               "stage": stage, "error_type": type(error).__name__,
               "error": str(error), "recorded_at_utc": utc_now(),
               "formal_credit": 0, "manifest_authorized": False,
               "C27_C28_C29": "UNAUTHORIZED",
               "CM2": "NO-GO_FOR_CLAIM"}
    try:
        write_json(run_dir / "failure.json", payload)
        exclusive(run_dir / "FAILED.lock", b"FAIL_CLOSED_ZERO_CREDIT\n")
    except FileExistsError:
        pass


def run(seed: int, out_dir: Path, run_dir: Path,
        expected_runner_sha256: str) -> dict[str, Any]:
    need(type(seed) is int and seed > 0, "positive seed")
    need(type(expected_runner_sha256) is str
         and len(expected_runner_sha256) == 64,
         "runner SHA256 launch pin")
    fresh_paths(out_dir, run_dir)
    run_dir.mkdir(parents=True, mode=0o700)
    stage = "transaction_initialization"
    try:
        exclusive(run_dir / "TRANSACTION.lock",
                  b"IMMUTABLE_FRESH_RUN_DIRECTORY__ZERO_CREDIT\n")
        runner_sha256 = fsha(RUNNER)
        need(runner_sha256 == expected_runner_sha256,
             "runner launch SHA256 pin")
        command = [str(PYTHON), "-I", "-B", str(ASSEMBLER),
                   "--out-dir", str(out_dir), "--seed", str(seed)]
        write_json(run_dir / "command.json", command)
        write_json(run_dir / "runner_command.json", sys.argv)
        write_json(run_dir / "pins.json", {
            "runner": {"path": str(RUNNER.relative_to(ROOT)),
                       "sha256": runner_sha256},
            "assembler": {"path": str(ASSEMBLER.relative_to(ROOT)),
                          "sha256": ASSEMBLER_SHA256},
            "python": {"path": str(PYTHON), "sha256": PYTHON_SHA256},
        })
        write_json(run_dir / "transaction.json", {
            "schema": "cm2.actual-v2-fresh-run-transaction.v2",
            "created_at_utc": utc_now(), "execution_seed": seed,
            "out_dir": str(out_dir.relative_to(ROOT)),
            "run_dir": str(run_dir.relative_to(ROOT)),
            "old_truncated_output_reused": False,
            "formal_credit": 0, "manifest_authorized": False,
            "C27_C28_C29": "UNAUTHORIZED_PENDING_FINAL_RECEIPT_V2",
            "CM2": "NO-GO_FOR_CLAIM",
        })

        stage = "input_pre_snapshot"
        module = load_contract()
        inputs = input_paths(module)
        pre = snapshot(inputs)
        write_json(run_dir / "input_pre.json", pre)

        environment = {"HOME": "/nonexistent", "LC_ALL": "C.UTF-8",
                       "TZ": "UTC", "PYTHONHASHSEED": str(seed)}
        stdout_fd = os.open(run_dir / "stdout.log",
                            os.O_WRONLY | os.O_CREAT | os.O_EXCL
                            | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
                            0o600)
        stderr_fd = os.open(run_dir / "stderr.log",
                            os.O_WRONLY | os.O_CREAT | os.O_EXCL
                            | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
                            0o600)
        process: subprocess.Popen[bytes] | None = None
        received_parent_signals: list[int] = []

        def forward(signum: int, _frame: Any) -> None:
            received_parent_signals.append(signum)
            if process is not None and process.poll() is None:
                process.send_signal(signum)

        previous_handlers = {item: signal.getsignal(item)
                             for item in (signal.SIGTERM, signal.SIGINT,
                                          signal.SIGHUP)}
        for item in previous_handlers:
            signal.signal(item, forward)
        start_wall_ns = time.time_ns()
        start_monotonic_ns = time.monotonic_ns()
        try:
            stage = "assembler_process"
            process = subprocess.Popen(command, cwd=ROOT, env=environment,
                                       stdout=stdout_fd, stderr=stderr_fd,
                                       close_fds=True)
            write_json(run_dir / "start.json", {
                "started_at_utc": utc_now(), "wall_clock_ns": start_wall_ns,
                "monotonic_ns": start_monotonic_ns,
                "runner_pid": os.getpid(), "assembler_pid": process.pid,
            })
            exclusive(run_dir / "child_pid.txt",
                      (str(process.pid) + "\n").encode("ascii"))
            return_code = process.wait()
        finally:
            for item, handler in previous_handlers.items():
                signal.signal(item, handler)
            os.fsync(stdout_fd)
            os.fsync(stderr_fd)
            os.close(stdout_fd)
            os.close(stderr_fd)
        end_monotonic_ns = time.monotonic_ns()
        end_wall_ns = time.time_ns()
        child_signal = -return_code if return_code < 0 else None
        numeric_exit_code = return_code if return_code >= 0 else None
        exclusive(run_dir / "exit_code.txt",
                  (str(return_code) + "\n").encode("ascii"))
        write_json(run_dir / "signal.json", child_signal)
        write_json(run_dir / "time.json", {
            "start_wall_clock_ns": start_wall_ns,
            "end_wall_clock_ns": end_wall_ns,
            "start_monotonic_ns": start_monotonic_ns,
            "end_monotonic_ns": end_monotonic_ns,
            "duration_ns": end_monotonic_ns - start_monotonic_ns,
        })
        write_json(run_dir / "end.json", {
            "ended_at_utc": utc_now(), "numeric_exit_code": numeric_exit_code,
            "signal": child_signal,
            "parent_signals_received": received_parent_signals,
            "duration_ns": end_monotonic_ns - start_monotonic_ns,
        })

        stage = "input_post_snapshot"
        post = snapshot(inputs)
        write_json(run_dir / "input_post.json", post)
        need(pre == post, "pre/post input SHA/stat identity")
        stderr_bytes = (run_dir / "stderr.log").read_bytes()
        stdout_bytes = (run_dir / "stdout.log").read_bytes()
        need(numeric_exit_code == 0 and child_signal is None
             and not received_parent_signals and stderr_bytes == b"",
             "assembler exit0/no signal/stderr empty")
        lines = stdout_bytes.splitlines()
        need(len(lines) == 1, "single assembler stdout JSON")
        summary = strict_json_bytes(lines[0], "assembler stdout")
        need(type(summary) is dict and canonical(summary) == lines[0],
             "canonical assembler stdout JSON")

        stage = "receipt_closure"
        receipt_path = out_dir / "assembler_receipt.json"
        receipt = strict_json(receipt_path)
        body = dict(receipt)
        claim = body.pop("assembler_receipt_sha256", None)
        need(claim == digest(body) == summary["assembler_receipt_sha256"],
             "assembler receipt closure")
        need(receipt["execution_seed"] == seed
             and receipt["assembler_source_sha256"] == ASSEMBLER_SHA256
             and receipt["exact_census"]["candidate_total"] == 7_486_076
             and receipt["exact_census"]
                 ["materialized_physical_proof_total"] == 65_064
             and receipt["exact_census"]
                 ["fresh_DSU_final_component_total"] == 43_684
             and receipt["formal_credit"] == 0
             and receipt["manifest_authorized"] is False,
             "exact assembler zero-credit conclusion")

        stage = "seven_output_validation"
        validation = output_validation(out_dir, receipt)
        write_json(run_dir / "output_validation.json", validation)
        body = {
            "schema": "cm2.c27-independent.primitive-twenty-family-gate-v5-actual-v2-run-attestation.v2",
            "status": "PASS_EXIT0_NO_SIGNAL_STDERR_EMPTY_PRE_POST_IDENTICAL_7_OF_7_GZIP_CANONICAL_COUNT_CLOSURE__ZERO_CREDIT",
            "execution_seed": seed, "argv": command,
            "numeric_exit_code": 0, "signal": None,
            "stdout_line_count": 1, "stderr_empty": True,
            "input_file_count": len(inputs), "input_pre": pre,
            "input_post": post, "pre_post_sha256_identical": True,
            "pre_post_stat_identical": True,
            "assembler_receipt_file_sha256": fsha(receipt_path),
            "assembler_receipt_object_sha256":
                receipt["assembler_receipt_sha256"],
            "output_validation_sha256": digest(validation),
            "output_files": validation["output_files"],
            "formal_credit": 0, "manifest_authorized": False,
            "source_W_transition_authorized": False,
            "C27_C28_C29": "UNAUTHORIZED_PENDING_FINAL_RECEIPT_V2",
            "CM2": "NO-GO_FOR_CLAIM",
            "runner_source_sha256": runner_sha256,
        }
        result = dict(body)
        result["run_attestation_sha256"] = digest(result)
        write_json(run_dir / "run_attestation.json", result)
        exclusive(run_dir / "PASS.lock",
                  b"PASS_TRANSACTION_COMPLETE__ZERO_CREDIT\n")
        return result
    except BaseException as error:
        record_failure(run_dir, stage, error)
        raise


def preflight(seed: int, out_dir: Path, run_dir: Path,
              expected_runner_sha256: str) -> dict[str, Any]:
    need(type(seed) is int and seed > 0, "positive seed")
    fresh_paths(out_dir, run_dir)
    runner_sha256 = fsha(RUNNER)
    need(runner_sha256 == expected_runner_sha256,
         "runner preflight SHA256 pin")
    module = load_contract()
    inputs = input_paths(module)
    pre = snapshot(inputs)
    return {
        "status": "PASS_FRESH_PATHS_AND_FULL_INPUT_SNAPSHOT__ZERO_CREDIT",
        "execution_seed": seed, "input_file_count": len(inputs),
        "input_snapshot_sha256": digest(pre),
        "runner_source_sha256": runner_sha256,
        "assembler_source_sha256": fsha(ASSEMBLER),
        "python_sha256": fsha(PYTHON),
        "out_dir": str(out_dir.relative_to(ROOT)),
        "run_dir": str(run_dir.relative_to(ROOT)),
        "formal_credit": 0, "manifest_authorized": False,
        "CM2": "NO-GO_FOR_CLAIM",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", required=True, type=int)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--expect-runner-sha256", required=True)
    parser.add_argument("--preflight-only", action="store_true")
    arguments = parser.parse_args()
    try:
        out_dir = Path(arguments.out_dir).resolve()
        run_dir = Path(arguments.run_dir).resolve()
        if arguments.preflight_only:
            result = preflight(arguments.seed, out_dir, run_dir,
                               arguments.expect_runner_sha256)
        else:
            result = run(arguments.seed, out_dir, run_dir,
                         arguments.expect_runner_sha256)
    except (Failure, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError, EOFError, gzip.BadGzipFile) as error:
        print("FAIL:" + str(error))
        return 2
    print(canonical(result if arguments.preflight_only else {
        "status": result["status"],
        "input_file_count": result["input_file_count"],
        "run_attestation_sha256": result["run_attestation_sha256"],
    }).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
