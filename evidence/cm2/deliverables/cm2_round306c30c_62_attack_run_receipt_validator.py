#!/usr/bin/env python3
"""Fail-closed validator for one completed C30c 62-attack run.

This verifier grants no mathematical or formal credit.  It binds the timed
invocation to the pinned harness/verifier/runtime and candidate bytes, derives
the attack contract from the pinned harness AST, and checks the complete raw
run receipt including signal status and pre/post immutability observations.
"""
from __future__ import annotations

import argparse
import ast
import datetime as dt
import hashlib
import json
import os
import re
import shlex
import stat
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

WORKSPACE = Path(__file__).resolve().parent.parent
AUDIT_ROOT = WORKSPACE / ".cm2-runtime" / "audit"
CANDIDATE_REL = Path(".cm2-runtime/candidates/c30c-v4-seed-30630071")
CANDIDATE = WORKSPACE / CANDIDATE_REL
PYTHON_REL = Path(".cm2-runtime/python-flint-0.9.0/bin/python")
PYTHON = WORKSPACE / PYTHON_REL
PYTHON3 = PYTHON.parent / "python3"
SYSTEM_PYTHON = Path("/usr/bin/python3")
PYTHON_REAL = Path("/usr/bin/python3.12")
PREFIX = "cm2_round306c30c_source_w_full_delta_whole_origin_disposition"
HARNESS_REL = Path("deliverables") / (PREFIX + "_attack_harness.py")
VERIFIER_REL = Path("deliverables") / (PREFIX + "_independent_verifier.py")
HARNESS = WORKSPACE / HARNESS_REL
VERIFIER = WORKSPACE / VERIFIER_REL

EXPECTED_RUN_NAME = "c30c-v5-toctou-robustness-rerun-20260807T1012-final"
EXPECTED_RUN_FILES = {
    "command.txt", "end_utc.txt", "exit_code.txt", "observed_child_pids.txt",
    "post.sha256", "post.stat", "pre.sha256", "pre.stat", "provenance.json",
    "run.sh", "start_utc.txt", "stderr.log", "stdout.json", "time.txt",
    "time_pid.txt", "wrapper_pid.txt",
}
EXPECTED_HARNESS_SHA256 = (
    "9f0b72a81098333c3f0b76d7191f48855d608b0aa1e405bdf72cb10532e825c8"
)
EXPECTED_VERIFIER_SHA256 = (
    "0fd82ce16053b69cbb04eddc423cb3f4b8cf8d11923219b50e6ff659f97b7377"
)
EXPECTED_PYTHON_SHA256 = (
    "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118"
)
EXPECTED_COMMAND_SHA256 = (
    "7875414533ecafbd270a8bad128ebcfc30af28f6008e3ac85270ccf9f38137eb"
)
EXPECTED_PROVENANCE_SHA256 = (
    "731dc491e413d6b8e60e52e4742b888d371fa50902af4b5312cfe9671015823c"
)
EXPECTED_RUNNER_SHA256 = (
    "0d64aded452950a02b7dec67f60bba36e9bc7f07453288d5421f6575a0350492"
)
EXPECTED_BASELINE_RESULT_SHA256 = (
    "df4531942e743389f5e8f85b2d013132f0808f562c21f430e7904577d67087d4"
)
EXPECTED_STATUS = (
    "PASS_62_OF_62_LAYER_SPECIFIC_COHERENT_ATTACKS_REJECTED"
    "__ZERO_FORMAL_CREDIT"
)
OUTPUT_SCHEMA = "cm2.round306c30c.attack-run-receipt-validation.v1"
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
POSITIVE_INTEGER = re.compile(rb"[1-9][0-9]*\n\Z")

CANDIDATE_FILES = {
    "cm2_round306c30b_python_flint_runtime_attestation.json",
    PREFIX + "_combined_boundary_atomic_owner_join_ledger.jsonl.gz",
    PREFIX + "_delta_h_cell_ledger.jsonl.gz",
    PREFIX + "_inherited_h_cell_ledger.jsonl.gz",
    PREFIX + "_result.json",
    PREFIX + "_whole_origin_ledger.jsonl.gz",
}


class Reject(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=True, allow_nan=False, sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(type(key) is str and key not in result, "duplicate JSON key")
        result[key] = value
    return result


def parse_json(raw: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(
            raw.decode("utf-8"), object_pairs_hook=unique_object,
            parse_constant=lambda value: (_ for _ in ()).throw(
                Reject(label + ": non-finite JSON:" + value)
            ),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Reject(label + ": invalid JSON") from error
    require(type(value) is dict, label + ": JSON object")
    return value


def captured_file(path: Path, maximum: int = 8 * 1024 * 1024) -> bytes:
    descriptor = os.open(
        os.fspath(path),
        os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        before = os.fstat(descriptor)
        require(stat.S_ISREG(before.st_mode), "regular file:" + os.fspath(path))
        require(before.st_nlink == 1, "singleton file:" + os.fspath(path))
        require(0 <= before.st_size <= maximum, "bounded file:" + os.fspath(path))
        chunks: list[bytes] = []
        remaining = before.st_size
        while remaining:
            chunk = os.read(descriptor, min(1 << 20, remaining))
            require(bool(chunk), "complete read:" + os.fspath(path))
            chunks.append(chunk)
            remaining -= len(chunk)
        require(os.read(descriptor, 1) == b"", "stable EOF:" + os.fspath(path))
        after = os.fstat(descriptor)
        identity = lambda value: (
            value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns,
        )
        require(identity(before) == identity(after), "stable inode:" + os.fspath(path))
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def streamed_hash(path: Path) -> tuple[str, os.stat_result]:
    descriptor = os.open(
        os.fspath(path),
        os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        before = os.fstat(descriptor)
        require(
            stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
            "race-checked regular singleton:" + os.fspath(path),
        )
        state = hashlib.sha256()
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            state.update(block)
        after = os.fstat(descriptor)
        fields = lambda value: (
            value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns,
        )
        require(fields(before) == fields(after), "stable hashed inode:" + os.fspath(path))
        return state.hexdigest(), after
    finally:
        os.close(descriptor)


def stat_identity(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
        value.st_size, value.st_mtime_ns, value.st_ctime_ns,
    )


def python_chain_snapshot() -> tuple[Any, ...]:
    """Pin the exact controlled venv link chain and its regular target.

    The timed command intentionally used the venv entry point.  Its lstat
    identity is therefore part of pre/post.stat, while pre/post.sha256 is the
    hash of the followed executable bytes.  Treating those two observations
    as if they described the same inode makes a valid run impossible.
    """
    first = os.lstat(PYTHON)
    second = os.lstat(PYTHON3)
    system = os.lstat(SYSTEM_PYTHON)
    target = os.lstat(PYTHON_REAL)
    require(
        stat.S_ISLNK(first.st_mode) and os.readlink(PYTHON) == "python3"
        and stat.S_ISLNK(second.st_mode)
        and os.readlink(PYTHON3) == "/usr/bin/python3"
        and stat.S_ISLNK(system.st_mode)
        and os.readlink(SYSTEM_PYTHON) == "python3.12"
        and stat.S_ISREG(target.st_mode) and target.st_nlink == 1
        and PYTHON.resolve(strict=True) == PYTHON_REAL,
        "exact controlled Python symlink chain",
    )
    return (
        stat_identity(first), stat_identity(second), stat_identity(system),
        stat_identity(target),
    )


def python_runtime_hash() -> tuple[str, os.stat_result, os.stat_result]:
    before_chain = python_chain_snapshot()
    descriptor = os.open(
        os.fspath(PYTHON_REAL),
        os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        before = os.fstat(descriptor)
        require(
            stat.S_ISREG(before.st_mode) and before.st_nlink == 1
            and stat_identity(before) == before_chain[-1],
            "controlled Python target identity",
        )
        state = hashlib.sha256()
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            state.update(block)
        after = os.fstat(descriptor)
        require(stat_identity(before) == stat_identity(after),
                "stable controlled Python target")
    finally:
        os.close(descriptor)
    require(before_chain == python_chain_snapshot(),
            "stable controlled Python symlink chain")
    return state.hexdigest(), after, os.lstat(PYTHON)


def safe_run_directory(argument: Path) -> Path:
    require(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", argument.name) is not None,
            "safe run name")
    absolute = Path(os.path.abspath(os.fspath(argument)))
    require(absolute.parent == AUDIT_ROOT, "run is direct audit child")
    require(absolute.name == EXPECTED_RUN_NAME, "exact intended run name")
    require(not absolute.is_symlink() and absolute.is_dir(), "real run directory")
    require(absolute.resolve(strict=True) == absolute, "resolved run directory")
    actual = {entry.name for entry in os.scandir(absolute)}
    require(actual == EXPECTED_RUN_FILES, "exact completed run file set")
    return absolute


def attack_contract(harness_raw: bytes) -> list[dict[str, str]]:
    try:
        tree = ast.parse(harness_raw, filename=os.fspath(HARNESS))
    except SyntaxError as error:
        raise Reject("pinned harness parses") from error
    assignment: ast.AST | None = None
    for node in tree.body:
        if (
            isinstance(node, ast.Assign)
            and any(isinstance(target, ast.Name) and target.id == "ATTACKS"
                    for target in node.targets)
        ):
            require(assignment is None, "single ATTACKS assignment")
            assignment = node.value
    require(isinstance(assignment, ast.Tuple), "literal ATTACKS tuple")
    rows: list[dict[str, str]] = []
    for item in assignment.elts:
        require(
            isinstance(item, ast.Call)
            and isinstance(item.func, ast.Name)
            and item.func.id == "Attack"
            and len(item.args) >= 3,
            "literal Attack call",
        )
        values: list[str] = []
        for argument in item.args[:3]:
            require(
                isinstance(argument, ast.Constant) and type(argument.value) is str,
                "literal attack contract string",
            )
            values.append(argument.value)
        rows.append({
            "attack": values[0], "layer": values[1],
            "expected_reason_prefix": values[2],
        })
    require(
        len(rows) == 62
        and len({row["attack"] for row in rows}) == 62,
        "exact 62 unique AST attacks",
    )
    return rows


def parse_sha256_ledger(raw: bytes, label: str) -> dict[str, str]:
    try:
        lines = raw.decode("utf-8").splitlines()
    except UnicodeDecodeError as error:
        raise Reject(label + ": UTF-8") from error
    result: dict[str, str] = {}
    for line in lines:
        parts = line.split("  ", 1)
        require(
            len(parts) == 2 and HEX64.fullmatch(parts[0]) is not None,
            label + ": sha256sum row",
        )
        path = parts[1]
        require(path not in result, label + ": unique path")
        result[path] = parts[0]
    require(len(result) == 12, label + ": exact 12 members")
    return result


def parse_stat_ledger(raw: bytes, label: str) -> dict[str, dict[str, int]]:
    try:
        lines = raw.decode("utf-8").splitlines()
    except UnicodeDecodeError as error:
        raise Reject(label + ": UTF-8") from error
    result: dict[str, dict[str, int]] = {}
    fields = ("dev", "ino", "mode", "links", "size", "mtime", "ctime")
    for line in lines:
        parts = line.split("|")
        require(len(parts) == 8 and parts[0] not in result,
                label + ": unique stat row")
        values: dict[str, int] = {}
        for expected, item in zip(fields, parts[1:], strict=True):
            key, separator, raw_value = item.partition("=")
            require(separator == "=" and key == expected and bool(raw_value),
                    label + ": stat field order")
            base = 16 if key == "mode" else 10
            try:
                value = int(raw_value, base)
            except ValueError as error:
                raise Reject(label + ": integer stat field") from error
            require(value >= 0, label + ": nonnegative stat field")
            values[key] = value
        result[parts[0]] = values
    require(len(result) == 10, label + ": exact 10 members")
    return result


def parse_utc(raw: bytes, label: str) -> dt.datetime:
    try:
        text = raw.decode("ascii")
        require(text.endswith("\n") and text.count("\n") == 1, label + ": one line")
        value = dt.datetime.strptime(text[:-1], "%Y-%m-%dT%H:%M:%SZ")
    except (UnicodeDecodeError, ValueError) as error:
        raise Reject(label + ": UTC timestamp") from error
    return value.replace(tzinfo=dt.timezone.utc)


def validate_time(raw: bytes, command: str) -> dict[str, Any]:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise Reject("GNU time UTF-8") from error
    timed = re.findall(r'(?m)^\s*Command being timed:\s*"([^"\n]*)"\s*$', text)
    require(len(timed) == 1, "one GNU timed command")
    require("Command terminated by signal" not in text, "no GNU-time signal")
    require(re.search(r"(?m)^\s*Exit status: 0\s*$", text) is not None,
            "GNU-time exit zero")
    try:
        timed_argv = shlex.split(timed[0], posix=True)
        command_argv = shlex.split(command, posix=True)
    except ValueError as error:
        raise Reject("timed/declared command shell syntax") from error
    expected_timed_argv = [
        "/usr/bin/env", "-i", "HOME=/nonexistent", "LC_ALL=C.UTF-8",
        "TZ=UTC", "PYTHONHASHSEED=30630071", os.fspath(PYTHON), "-I", "-B",
        os.fspath(HARNESS), os.fspath(CANDIDATE),
    ]
    expected_declared_argv = [
        "env", "-i", "HOME=/nonexistent", "LC_ALL=C.UTF-8", "TZ=UTC",
        "PYTHONHASHSEED=30630071", PYTHON_REL.as_posix(), "-I", "-B",
        HARNESS_REL.as_posix(), CANDIDATE_REL.as_posix(),
    ]
    require(
        timed_argv == expected_timed_argv
        and command_argv == expected_declared_argv,
        "GNU-time and declared exact argv identity",
    )
    elapsed = re.search(
        r"(?m)^\s*Elapsed \(wall clock\) time \(h:mm:ss or m:ss\):"
        r"\s*([0-9]+(?::[0-9]+){1,2}(?:\.[0-9]+)?)\s*$",
        text,
    )
    require(elapsed is not None, "GNU-time elapsed")
    return {"elapsed": elapsed.group(1).strip(), "signal": None, "exit_code": 0}


def current_bound_hashes(provenance: dict[str, Any]) -> dict[str, str]:
    require(
        not CANDIDATE.is_symlink() and CANDIDATE.is_dir()
        and CANDIDATE.resolve(strict=True) == CANDIDATE,
        "fixed candidate directory",
    )
    require({entry.name for entry in os.scandir(CANDIDATE)} == CANDIDATE_FILES,
            "candidate exact six files")
    paths = [PYTHON, HARNESS, VERIFIER]
    paths.extend(CANDIDATE / name for name in sorted(CANDIDATE_FILES))
    hashes: dict[str, str] = {}
    for path in paths:
        if path == PYTHON:
            value, _state, _link_state = python_runtime_hash()
        else:
            value, _state = streamed_hash(path)
        hashes[os.fspath(path)] = value
    expected_candidate = provenance["candidate_file_sha256"]
    require(type(expected_candidate) is dict, "provenance candidate hash map")
    require(
        expected_candidate
        == {name: hashes[os.fspath(CANDIDATE / name)] for name in sorted(CANDIDATE_FILES)},
        "current exact-six hashes equal provenance",
    )
    return hashes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_directory", type=Path)
    arguments = parser.parse_args()
    run = safe_run_directory(arguments.run_directory)

    captured = {
        name: captured_file(run / name, 16 * 1024 * 1024)
        for name in sorted(EXPECTED_RUN_FILES)
    }
    require(sha256(captured["command.txt"]) == EXPECTED_COMMAND_SHA256,
            "pinned command bytes")
    require(sha256(captured["provenance.json"]) == EXPECTED_PROVENANCE_SHA256,
            "pinned provenance bytes")
    require(sha256(captured["run.sh"]) == EXPECTED_RUNNER_SHA256,
            "pinned runner bytes")

    harness_raw = captured_file(HARNESS, 256 * 1024)
    verifier_raw = captured_file(VERIFIER, 2 * 1024 * 1024)
    require(sha256(harness_raw) == EXPECTED_HARNESS_SHA256, "pinned harness")
    require(sha256(verifier_raw) == EXPECTED_VERIFIER_SHA256, "pinned verifier")
    python_sha, _python_state, _python_link_state = python_runtime_hash()
    require(python_sha == EXPECTED_PYTHON_SHA256, "pinned Python runtime")

    provenance = parse_json(captured["provenance.json"], "provenance")
    require(canonical(provenance) + b"\n" == captured["provenance.json"],
            "canonical provenance bytes")
    require(
        provenance == {
            "candidate_directory": CANDIDATE_REL.as_posix(),
            "candidate_file_sha256": provenance.get("candidate_file_sha256"),
            "command_bytes_without_final_newline_sha256":
                sha256(captured["command.txt"].removesuffix(b"\n")),
            "formal_credit": 0,
            "harness_sha256": EXPECTED_HARNESS_SHA256,
            "intended_start_utc": "2026-08-07T02:12:24Z",
            "purpose": "C30c candidate-only exact 62-case mathematical artifact integrity rerun",
            "python_executable_sha256": EXPECTED_PYTHON_SHA256,
            "schema": "cm2.c30c.robustness-rerun-provenance.v1",
            "verifier_sha256": EXPECTED_VERIFIER_SHA256,
            "zero_credit_until_formal_prerequisites_exist": True,
        },
        "exact provenance contract",
    )
    current_hashes = current_bound_hashes(provenance)

    pre = parse_sha256_ledger(captured["pre.sha256"], "pre.sha256")
    post = parse_sha256_ledger(captured["post.sha256"], "post.sha256")
    require(pre == post, "pre/post sha256 byte identities")
    require(captured["pre.stat"] == captured["post.stat"], "pre/post stat identities")
    expected_paths = {
        os.fspath(PYTHON), os.fspath(HARNESS), os.fspath(VERIFIER),
        os.fspath(run / "command.txt"), os.fspath(run / "provenance.json"),
        os.fspath(run / "run.sh"),
        *(os.fspath(CANDIDATE / name) for name in CANDIDATE_FILES),
    }
    require(set(pre) == expected_paths, "pre/post exact path set")
    bound = dict(current_hashes)
    bound[os.fspath(run / "command.txt")] = EXPECTED_COMMAND_SHA256
    bound[os.fspath(run / "provenance.json")] = EXPECTED_PROVENANCE_SHA256
    bound[os.fspath(run / "run.sh")] = EXPECTED_RUNNER_SHA256
    require(pre == bound, "pre/post hashes equal current pinned bytes")

    observed_stat = parse_stat_ledger(captured["pre.stat"], "pre.stat")
    expected_stat_paths = {
        os.fspath(PYTHON), os.fspath(HARNESS), os.fspath(VERIFIER),
        os.fspath(CANDIDATE),
        *(os.fspath(CANDIDATE / name) for name in CANDIDATE_FILES),
    }
    require(set(observed_stat) == expected_stat_paths, "stat exact path set")
    for path_text, recorded in observed_stat.items():
        state = os.lstat(path_text)
        is_candidate_root = path_text == os.fspath(CANDIDATE)
        is_python_link = path_text == os.fspath(PYTHON)
        if is_python_link:
            require(stat.S_ISLNK(state.st_mode) and state.st_nlink == 1,
                    "current controlled Python link:" + path_text)
            python_value, _target_state, link_state = python_runtime_hash()
            require(
                python_value == EXPECTED_PYTHON_SHA256
                and stat_identity(link_state) == stat_identity(state),
                "current controlled Python chain/hash:" + path_text,
            )
        else:
            require(
                (stat.S_ISDIR(state.st_mode) if is_candidate_root
                 else stat.S_ISREG(state.st_mode) and state.st_nlink == 1)
                and not stat.S_ISLNK(state.st_mode),
                "current stat type/singleton:" + path_text,
            )
        current = {
            "dev": state.st_dev, "ino": state.st_ino, "mode": state.st_mode,
            "links": state.st_nlink, "size": state.st_size,
            "mtime": int(state.st_mtime), "ctime": int(state.st_ctime),
        }
        require(recorded == current, "recorded stat equals current:" + path_text)

    require(captured["exit_code.txt"] == b"0\n", "numeric exit zero")
    require(captured["stderr.log"] == b"", "empty harness stderr")
    require(POSITIVE_INTEGER.fullmatch(captured["wrapper_pid.txt"]) is not None,
            "numeric wrapper PID")
    require(POSITIVE_INTEGER.fullmatch(captured["time_pid.txt"]) is not None,
            "numeric time PID")
    require(
        re.fullmatch(rb"[1-9][0-9]*(?: [1-9][0-9]*)*\n", captured["observed_child_pids.txt"])
        is not None,
        "observed child PID receipt",
    )
    start = parse_utc(captured["start_utc.txt"], "start")
    end = parse_utc(captured["end_utc.txt"], "end")
    require(start < end, "positive run interval")
    command = captured["command.txt"].decode("ascii").removesuffix("\n")
    time_receipt = validate_time(captured["time.txt"], command)

    output = parse_json(captured["stdout.json"], "harness stdout")
    require(canonical(output) + b"\n" == captured["stdout.json"],
            "canonical stdout bytes")
    require(
        set(output) == {
            "C30b_input_kind", "C30c_publisher_I_O_authority", "attack_count",
            "attacks", "baseline_file_sha256", "baseline_result_sha256",
            "formal_credit", "manifest_authorized", "schema", "status",
        },
        "exact harness output keys",
    )
    contract = attack_contract(harness_raw)
    require(
        output["schema"]
        == "cm2.round306c30c.source-w-full-delta.coherent-attack-harness.candidate.v1"
        and output["status"] == EXPECTED_STATUS
        and type(output["attack_count"]) is int
        and output["attack_count"] == 62
        and type(output["formal_credit"]) is int
        and output["formal_credit"] == 0
        and output["manifest_authorized"] is False
        and output["baseline_result_sha256"] == EXPECTED_BASELINE_RESULT_SHA256
        and output["baseline_file_sha256"] == provenance["candidate_file_sha256"]
        and output["C30b_input_kind"] == "FIXED_FORMALLY_SEALED_MANIFEST_AUTHORITY",
        "exact zero-credit harness conclusion",
    )
    require(
        output["C30c_publisher_I_O_authority"] == {
            "producer_filename": PREFIX + "_producer.py",
            "producer_sha256":
                "4644f8aad5fb9b2956a3854d1457d40c93c7f4f134ca808c782d61e0c526e549",
            "loading": "AST_EXTRACTED_SHORT_I_O_HELPERS_FROM_PINNED_BYTES",
            "synthetic_payload_file_count": 6,
            "positive_visibility_transition": "ABSENT_TO_EXACT_SIX",
            "noreplace_cases": [
                "PREEXISTING_COMPLETE", "PREEXISTING_PARTIAL",
                "CONCURRENT_EEXIST",
            ],
        },
        "exact pinned publisher I/O authority",
    )
    require(type(output["attacks"]) is list and len(output["attacks"]) == 62,
            "exact 62 output attacks")
    for expected, observed in zip(contract, output["attacks"], strict=True):
        require(type(observed) is dict, "attack output object")
        require(
            set(observed) == {
                "attack", "expected_reason_prefix", "layer", "rejection",
            }
            and all(observed[key] == expected[key] for key in expected),
            "attack identity/order matches pinned AST",
        )
        rejection = observed["rejection"]
        require(
            type(rejection) is str and ":" in rejection
            and rejection.split(":", 1)[1].startswith(
                expected["expected_reason_prefix"]
            ),
            "attack rejected for expected reason prefix:" + expected["attack"],
        )

    receipt = {
        "schema": OUTPUT_SCHEMA,
        "status": "PASS_COMPLETE_C30C_62_ATTACK_RUN_RECEIPT__ZERO_FORMAL_CREDIT",
        "run_directory": run.name,
        "run_start_utc": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "run_end_utc": end.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "elapsed": time_receipt["elapsed"],
        "harness_stdout_sha256": sha256(captured["stdout.json"]),
        "harness_sha256": EXPECTED_HARNESS_SHA256,
        "verifier_sha256": EXPECTED_VERIFIER_SHA256,
        "python_sha256": EXPECTED_PYTHON_SHA256,
        "baseline_result_sha256": EXPECTED_BASELINE_RESULT_SHA256,
        "attack_count": 62,
        "pre_post_sha256_identical": True,
        "pre_post_stat_identical": True,
        "numeric_exit_code": 0,
        "signal": None,
        "formal_credit": 0,
        "manifest_authorized": False,
        "authority": "AUDIT_ONLY_REQUIRES_P0_FINAL_COMMIT_AND_FORMAL_PUBLICATION_CHAIN",
    }
    print(canonical(receipt).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Reject, OSError, KeyError, TypeError, ValueError) as error:
        print("REJECT_C30C_ATTACK_RUN_RECEIPT:" + str(error), file=sys.stderr)
        raise SystemExit(1)
