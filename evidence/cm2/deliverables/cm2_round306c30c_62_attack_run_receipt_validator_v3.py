#!/usr/bin/env python3
"""Self-contained, fail-closed validator for the fresh C30c v3 transaction.

This file deliberately does not import any earlier receipt validator.  It is
the single versioned source of truth for the command, provenance, runner, raw
receipt, and 62-attack output contract.  A pass is audit-only: it grants zero
formal credit and does not authorize a Source-W transition or publication.
"""
from __future__ import annotations

import argparse
import ast
import datetime as dt
import gzip
import hashlib
import json
import os
import re
import shlex
import stat
import sys
import tempfile
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

WORKSPACE = Path("/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572")
AUDIT_ROOT = WORKSPACE / ".cm2-runtime/audit"
RUN_NAME = "c30c-v5-toctou-robustness-rerun-20260808T0635Z-receipt-v3"
RUN = AUDIT_ROOT / RUN_NAME
PREFIX = "cm2_round306c30c_source_w_full_delta_whole_origin_disposition"

CANDIDATE_REL = Path(".cm2-runtime/candidates/c30c-v4-seed-30630071")
CANDIDATE = WORKSPACE / CANDIDATE_REL
PYTHON_REL = Path(".cm2-runtime/python-flint-0.9.0/bin/python")
PYTHON = WORKSPACE / PYTHON_REL
PYTHON3 = PYTHON.parent / "python3"
SYSTEM_PYTHON = Path("/usr/bin/python3")
PYTHON_REAL = Path("/usr/bin/python3.12")
HARNESS_REL = Path("deliverables") / (PREFIX + "_attack_harness.py")
VERIFIER_REL = Path("deliverables") / (PREFIX + "_independent_verifier.py")
VALIDATOR_REL = Path("deliverables/cm2_round306c30c_62_attack_run_receipt_validator_v3.py")
HARNESS = WORKSPACE / HARNESS_REL
VERIFIER = WORKSPACE / VERIFIER_REL
VALIDATOR = WORKSPACE / VALIDATOR_REL

EXPECTED_PYTHON_SHA256 = "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118"
EXPECTED_HARNESS_SHA256 = "9f0b72a81098333c3f0b76d7191f48855d608b0aa1e405bdf72cb10532e825c8"
EXPECTED_VERIFIER_SHA256 = "0fd82ce16053b69cbb04eddc423cb3f4b8cf8d11923219b50e6ff659f97b7377"
EXPECTED_BASELINE_RESULT_SHA256 = "df4531942e743389f5e8f85b2d013132f0808f562c21f430e7904577d67087d4"
EXPECTED_STATUS = (
    "PASS_62_OF_62_LAYER_SPECIFIC_COHERENT_ATTACKS_REJECTED"
    "__ZERO_FORMAL_CREDIT"
)
OUTPUT_SCHEMA = "cm2.round306c30c.attack-run-receipt-validation.v3"

CANDIDATE_HASHES = {
    "cm2_round306c30b_python_flint_runtime_attestation.json":
        "6b48cd0ca3fd53f9fdd457cc3c1106055e12db4d4ad999fcfd1fc89ad36b95df",
    PREFIX + "_combined_boundary_atomic_owner_join_ledger.jsonl.gz":
        "63f004bdb065d8674ecfde9eb957f3477ee6c3f806064ef8f151850cd391d251",
    PREFIX + "_delta_h_cell_ledger.jsonl.gz":
        "acbd71e9155d81d17ae4b42eecd31f0fc9d4bb91ac36aa93a7ab7df08e3dee50",
    PREFIX + "_inherited_h_cell_ledger.jsonl.gz":
        "d4142d7748e0546184542bea7b3b337c9f33e7312efa2e7c5271d2a9dba30abd",
    PREFIX + "_result.json":
        "96c1e9f627bd6113fc56f7b6d35856581b57b4afde049e997b10eef3f8c706f1",
    PREFIX + "_whole_origin_ledger.jsonl.gz":
        "48a3e612de84004ba746d93d492e8f3e9f587ebf6b3574615fa946dddf21a573",
}
EXPECTED_GZIP_ROWS = {
    PREFIX + "_combined_boundary_atomic_owner_join_ledger.jsonl.gz": 2080,
    PREFIX + "_delta_h_cell_ledger.jsonl.gz": 80,
    PREFIX + "_inherited_h_cell_ledger.jsonl.gz": 88,
    PREFIX + "_whole_origin_ledger.jsonl.gz": 2,
}

INITIAL_RUN_FILES = {"command.txt", "provenance.json", "run.sh"}
COMPLETED_RUN_FILES = INITIAL_RUN_FILES | {
    "end_utc.txt", "exit_code.txt", "observed_child_pids.txt",
    "post.sha256", "post.stat", "pre.sha256", "pre.stat", "start_utc.txt",
    "stderr.log", "stdout.json", "time.txt", "time_pid.txt", "wrapper_pid.txt",
}
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
POSITIVE_INTEGER = re.compile(rb"[1-9][0-9]*\n\Z")


class Reject(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=True, allow_nan=False, sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        require(type(key) is str and key not in value, "duplicate JSON key")
        value[key] = item
    return value


def parse_json(raw: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(
            raw.decode("utf-8"), object_pairs_hook=unique_object,
            parse_constant=lambda token: (_ for _ in ()).throw(
                Reject(label + ": non-finite JSON:" + token)
            ),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Reject(label + ": invalid JSON") from error
    require(type(value) is dict, label + ": JSON object")
    return value


def stat_identity(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
        value.st_size, value.st_mtime_ns, value.st_ctime_ns,
    )


def captured_file(path: Path, maximum: int = 16 * 1024 * 1024) -> bytes:
    descriptor = os.open(
        os.fspath(path), os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        before = os.fstat(descriptor)
        require(stat.S_ISREG(before.st_mode), "regular file:" + os.fspath(path))
        require(before.st_nlink == 1, "singleton file:" + os.fspath(path))
        require(0 <= before.st_size <= maximum, "bounded file:" + os.fspath(path))
        blocks: list[bytes] = []
        remaining = before.st_size
        while remaining:
            block = os.read(descriptor, min(1 << 20, remaining))
            require(bool(block), "complete read:" + os.fspath(path))
            blocks.append(block)
            remaining -= len(block)
        require(os.read(descriptor, 1) == b"", "stable EOF:" + os.fspath(path))
        after = os.fstat(descriptor)
        require(stat_identity(before) == stat_identity(after),
                "stable inode:" + os.fspath(path))
        return b"".join(blocks)
    finally:
        os.close(descriptor)


def streamed_hash(path: Path) -> tuple[str, os.stat_result]:
    descriptor = os.open(
        os.fspath(path), os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        before = os.fstat(descriptor)
        require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
                "hash regular singleton:" + os.fspath(path))
        state = hashlib.sha256()
        while block := os.read(descriptor, 4 << 20):
            state.update(block)
        after = os.fstat(descriptor)
        require(stat_identity(before) == stat_identity(after),
                "stable hashed inode:" + os.fspath(path))
        return state.hexdigest(), after
    finally:
        os.close(descriptor)


def python_snapshot() -> tuple[Any, ...]:
    first = os.lstat(PYTHON)
    second = os.lstat(PYTHON3)
    system = os.lstat(SYSTEM_PYTHON)
    target = os.lstat(PYTHON_REAL)
    require(
        stat.S_ISLNK(first.st_mode) and os.readlink(PYTHON) == "python3"
        and stat.S_ISLNK(second.st_mode) and os.readlink(PYTHON3) == "/usr/bin/python3"
        and stat.S_ISLNK(system.st_mode) and os.readlink(SYSTEM_PYTHON) == "python3.12"
        and stat.S_ISREG(target.st_mode) and target.st_nlink == 1
        and PYTHON.resolve(strict=True) == PYTHON_REAL,
        "exact controlled Python symlink chain",
    )
    return (
        stat_identity(first), stat_identity(second), stat_identity(system),
        stat_identity(target),
    )


def python_hash() -> tuple[str, os.stat_result, os.stat_result]:
    before_chain = python_snapshot()
    value, target = streamed_hash(PYTHON_REAL)
    require(before_chain == python_snapshot(), "stable controlled Python chain")
    return value, target, os.lstat(PYTHON)


def command_bytes() -> bytes:
    return (
        b"env -i HOME=/nonexistent LC_ALL=C.UTF-8 TZ=UTC "
        b"PYTHONHASHSEED=30630071 "
        + PYTHON_REL.as_posix().encode("ascii") + b" -I -B "
        + HARNESS_REL.as_posix().encode("ascii") + b" "
        + CANDIDATE_REL.as_posix().encode("ascii") + b"\n"
    )


def provenance_object() -> dict[str, Any]:
    return {
        "candidate_directory": CANDIDATE_REL.as_posix(),
        "candidate_file_sha256": CANDIDATE_HASHES,
        "command_bytes_without_final_newline_sha256":
            sha256(command_bytes().removesuffix(b"\n")),
        "downstream_publication_authorized": False,
        "formal_credit": 0,
        "harness_sha256": EXPECTED_HARNESS_SHA256,
        "intended_start_utc": "2026-08-08T06:35:00Z",
        "prior_completed_62_case_run_use": "DIAGNOSTIC_ONLY",
        "purpose": "fresh C30c exact 62-case receipt transaction v3",
        "python_executable_sha256": EXPECTED_PYTHON_SHA256,
        "receipt_validator": VALIDATOR_REL.as_posix(),
        "run_name": RUN_NAME,
        "schema": "cm2.c30c.robustness-rerun-provenance.v3",
        "source_W_formal_remainder_before_terminal_replay": 80,
        "verifier_sha256": EXPECTED_VERIFIER_SHA256,
        "zero_credit_until_terminal_replay": True,
    }


def provenance_bytes() -> bytes:
    return canonical(provenance_object()) + b"\n"


def runner_bytes() -> bytes:
    return f'''#!/bin/bash
set -uo pipefail
set -C

WORKSPACE={WORKSPACE}
RUN_DIR="$WORKSPACE/.cm2-runtime/audit/{RUN_NAME}"
PYTHON="$WORKSPACE/{PYTHON_REL.as_posix()}"
HARNESS="$WORKSPACE/{HARNESS_REL.as_posix()}"
VERIFIER="$WORKSPACE/{VERIFIER_REL.as_posix()}"
VALIDATOR="$WORKSPACE/{VALIDATOR_REL.as_posix()}"
CANDIDATE="$WORKSPACE/{CANDIDATE_REL.as_posix()}"

cd "$WORKSPACE" || exit 125
umask 077

for name in start_utc.txt wrapper_pid.txt pre.sha256 pre.stat stdout.json \\
    stderr.log time.txt time_pid.txt observed_child_pids.txt exit_code.txt \\
    end_utc.txt post.sha256 post.stat; do
    if [[ -e "$RUN_DIR/$name" ]]; then
        exit 124
    fi
done

/usr/bin/date -u +'%Y-%m-%dT%H:%M:%SZ' > "$RUN_DIR/start_utc.txt" || exit 123
/usr/bin/printf '%s\n' "$$" > "$RUN_DIR/wrapper_pid.txt" || exit 123
/usr/bin/sha256sum \\
    "$PYTHON" "$HARNESS" "$VERIFIER" "$VALIDATOR" \\
    "$RUN_DIR/command.txt" "$RUN_DIR/provenance.json" "$RUN_DIR/run.sh" \\
    "$CANDIDATE"/* > "$RUN_DIR/pre.sha256" || exit 123
/usr/bin/stat -c '%n|dev=%d|ino=%i|mode=%f|links=%h|size=%s|mtime=%Y|ctime=%Z' \\
    "$PYTHON" "$HARNESS" "$VERIFIER" "$VALIDATOR" \\
    "$CANDIDATE" "$CANDIDATE"/* > "$RUN_DIR/pre.stat" || exit 123

/usr/bin/time --verbose --output="$RUN_DIR/time.txt" -- \\
    /usr/bin/env -i HOME=/nonexistent LC_ALL=C.UTF-8 TZ=UTC \\
    PYTHONHASHSEED=30630071 \\
    "$PYTHON" -I -B "$HARNESS" "$CANDIDATE" \\
    > "$RUN_DIR/stdout.json" 2> "$RUN_DIR/stderr.log" &
TIME_PID=$!
/usr/bin/printf '%s\n' "$TIME_PID" > "$RUN_DIR/time_pid.txt" || exit 123

for _attempt in $(/usr/bin/seq 1 200); do
    if [[ -r "/proc/$TIME_PID/task/$TIME_PID/children" ]]; then
        read -r CHILDREN < "/proc/$TIME_PID/task/$TIME_PID/children" || true
        if [[ -n "${{CHILDREN:-}}" ]]; then
            /usr/bin/printf '%s\n' "$CHILDREN" \
                > "$RUN_DIR/observed_child_pids.txt" || exit 123
            break
        fi
    fi
    /usr/bin/sleep 0.05
done

wait "$TIME_PID"
RUN_EXIT=$?
/usr/bin/printf '%s\n' "$RUN_EXIT" > "$RUN_DIR/exit_code.txt" || exit 123
/usr/bin/date -u +'%Y-%m-%dT%H:%M:%SZ' > "$RUN_DIR/end_utc.txt" || exit 123
/usr/bin/sha256sum \\
    "$PYTHON" "$HARNESS" "$VERIFIER" "$VALIDATOR" \\
    "$RUN_DIR/command.txt" "$RUN_DIR/provenance.json" "$RUN_DIR/run.sh" \\
    "$CANDIDATE"/* > "$RUN_DIR/post.sha256" || exit 123
/usr/bin/stat -c '%n|dev=%d|ino=%i|mode=%f|links=%h|size=%s|mtime=%Y|ctime=%Z' \\
    "$PYTHON" "$HARNESS" "$VERIFIER" "$VALIDATOR" \\
    "$CANDIDATE" "$CANDIDATE"/* > "$RUN_DIR/post.stat" || exit 123
/usr/bin/sync -f "$RUN_DIR"
exit "$RUN_EXIT"
'''.encode("ascii")


def safe_run_directory(argument: Path, completed: bool) -> Path:
    absolute = Path(os.path.abspath(os.fspath(argument)))
    require(absolute == RUN and absolute.parent == AUDIT_ROOT,
            "exact direct audit run path")
    require(not absolute.is_symlink() and absolute.is_dir(), "real run directory")
    require(absolute.resolve(strict=True) == absolute, "resolved run directory")
    actual = {entry.name for entry in os.scandir(absolute)}
    require(actual == (COMPLETED_RUN_FILES if completed else INITIAL_RUN_FILES),
            "exact run file set")
    return absolute


def attack_contract(harness_raw: bytes) -> list[dict[str, str]]:
    try:
        tree = ast.parse(harness_raw, filename=os.fspath(HARNESS))
    except SyntaxError as error:
        raise Reject("pinned harness parses") from error
    assignment: ast.AST | None = None
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "ATTACKS"
            for target in node.targets
        ):
            require(assignment is None, "single ATTACKS assignment")
            assignment = node.value
    require(isinstance(assignment, ast.Tuple), "literal ATTACKS tuple")
    rows: list[dict[str, str]] = []
    for item in assignment.elts:
        require(
            isinstance(item, ast.Call) and isinstance(item.func, ast.Name)
            and item.func.id == "Attack" and len(item.args) >= 3,
            "literal Attack call",
        )
        values: list[str] = []
        for argument in item.args[:3]:
            require(isinstance(argument, ast.Constant)
                    and type(argument.value) is str,
                    "literal attack contract string")
            values.append(argument.value)
        rows.append({
            "attack": values[0], "layer": values[1],
            "expected_reason_prefix": values[2],
        })
    require(len(rows) == 62 and len({row["attack"] for row in rows}) == 62,
            "exact 62 unique AST attacks")
    return rows


def parse_sha_ledger(raw: bytes, label: str) -> dict[str, str]:
    try:
        lines = raw.decode("utf-8").splitlines()
    except UnicodeDecodeError as error:
        raise Reject(label + ": UTF-8") from error
    result: dict[str, str] = {}
    for line in lines:
        parts = line.split("  ", 1)
        require(len(parts) == 2 and HEX64.fullmatch(parts[0]) is not None,
                label + ": sha256sum row")
        require(parts[1] not in result, label + ": unique path")
        result[parts[1]] = parts[0]
    require(len(result) == 13, label + ": exact 13 members")
    return result


def parse_stat_ledger(raw: bytes, label: str) -> dict[str, dict[str, int]]:
    result: dict[str, dict[str, int]] = {}
    fields = ("dev", "ino", "mode", "links", "size", "mtime", "ctime")
    try:
        lines = raw.decode("utf-8").splitlines()
    except UnicodeDecodeError as error:
        raise Reject(label + ": UTF-8") from error
    for line in lines:
        parts = line.split("|")
        require(len(parts) == 8 and parts[0] not in result,
                label + ": unique stat row")
        values: dict[str, int] = {}
        for expected, item in zip(fields, parts[1:], strict=True):
            key, separator, text = item.partition("=")
            require(separator == "=" and key == expected and bool(text),
                    label + ": stat field order")
            try:
                value = int(text, 16 if key == "mode" else 10)
            except ValueError as error:
                raise Reject(label + ": integer stat field") from error
            require(value >= 0, label + ": nonnegative stat field")
            values[key] = value
        result[parts[0]] = values
    require(len(result) == 11, label + ": exact 11 members")
    return result


def parse_utc(raw: bytes, label: str) -> dt.datetime:
    try:
        text = raw.decode("ascii")
        require(text.endswith("\n") and text.count("\n") == 1,
                label + ": one line")
        value = dt.datetime.strptime(text[:-1], "%Y-%m-%dT%H:%M:%SZ")
    except (UnicodeDecodeError, ValueError) as error:
        raise Reject(label + ": UTC timestamp") from error
    return value.replace(tzinfo=dt.timezone.utc)


def validate_time(raw: bytes) -> str:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise Reject("GNU time UTF-8") from error
    timed = re.findall(r'(?m)^\s*Command being timed:\s*"([^"\n]*)"\s*$', text)
    require(len(timed) == 1 and "Command terminated by signal" not in text,
            "one unsignaled GNU timed command")
    require(re.search(r"(?m)^\s*Exit status: 0\s*$", text) is not None,
            "GNU-time exit zero")
    expected = [
        "/usr/bin/env", "-i", "HOME=/nonexistent", "LC_ALL=C.UTF-8", "TZ=UTC",
        "PYTHONHASHSEED=30630071", os.fspath(PYTHON), "-I", "-B",
        os.fspath(HARNESS), os.fspath(CANDIDATE),
    ]
    try:
        observed = shlex.split(timed[0], posix=True)
    except ValueError as error:
        raise Reject("GNU timed argv syntax") from error
    require(observed == expected, "GNU-time exact argv identity")
    elapsed = re.search(
        r"(?m)^\s*Elapsed \(wall clock\) time \(h:mm:ss or m:ss\):"
        r"\s*([0-9]+(?::[0-9]+){1,2}(?:\.[0-9]+)?)\s*$", text,
    )
    require(elapsed is not None, "GNU-time elapsed")
    return elapsed.group(1).strip()


def current_hashes() -> dict[str, str]:
    require(not CANDIDATE.is_symlink() and CANDIDATE.is_dir()
            and CANDIDATE.resolve(strict=True) == CANDIDATE,
            "fixed candidate directory")
    require({entry.name for entry in os.scandir(CANDIDATE)} == set(CANDIDATE_HASHES),
            "candidate exact six files")
    python_value, _target, _link = python_hash()
    require(python_value == EXPECTED_PYTHON_SHA256, "pinned Python runtime")
    hashes = {os.fspath(PYTHON): python_value}
    for path, expected in ((HARNESS, EXPECTED_HARNESS_SHA256),
                           (VERIFIER, EXPECTED_VERIFIER_SHA256)):
        value, _state = streamed_hash(path)
        require(value == expected, "pinned executable:" + path.name)
        hashes[os.fspath(path)] = value
    validator_value, _validator_state = streamed_hash(VALIDATOR)
    hashes[os.fspath(VALIDATOR)] = validator_value
    observed_candidate: dict[str, str] = {}
    for name in sorted(CANDIDATE_HASHES):
        value, _state = streamed_hash(CANDIDATE / name)
        observed_candidate[name] = value
        hashes[os.fspath(CANDIDATE / name)] = value
    require(observed_candidate == CANDIDATE_HASHES, "pinned candidate exact-six hashes")
    return hashes


def self_test() -> dict[str, Any]:
    hashes = current_hashes()
    harness_raw = captured_file(HARNESS, 256 * 1024)
    attacks = attack_contract(harness_raw)
    ast.parse(captured_file(VALIDATOR, 2 * 1024 * 1024), filename=os.fspath(VALIDATOR))
    require(parse_json(b'{"a":1}', "positive fixture") == {"a": 1},
            "positive JSON fixture")
    try:
        parse_json(b'{"a":1,"a":2}', "duplicate fixture")
    except Reject:
        pass
    else:
        raise Reject("duplicate-key fixture rejected")
    try:
        parse_sha_ledger(b"", "truncation fixture")
    except Reject:
        pass
    else:
        raise Reject("truncated sha fixture rejected")
    with tempfile.TemporaryDirectory(prefix="cm2-c30c-v3-selftest-") as temporary:
        target = Path(temporary) / "target"
        target.write_bytes(b"fixture")
        link = Path(temporary) / "link"
        link.symlink_to(target)
        try:
            captured_file(link)
        except (OSError, Reject):
            pass
        else:
            raise Reject("symlink fixture rejected")
    gzip_rows: dict[str, int] = {}
    for name, expected_count in sorted(EXPECTED_GZIP_ROWS.items()):
        count = 0
        with gzip.open(CANDIDATE / name, "rb") as stream:
            for raw in stream:
                row = parse_json(raw, "canonical gzip row:" + name)
                require(canonical(row) + b"\n" == raw,
                        "canonical gzip row bytes:" + name)
                count += 1
        require(count == expected_count, "gzip row-count closure:" + name)
        gzip_rows[name] = count
    result_raw = captured_file(CANDIDATE / (PREFIX + "_result.json"))
    require(canonical(parse_json(result_raw, "candidate result")) == result_raw,
            "canonical candidate result bytes")
    return {
        "schema": "cm2.c30c.receipt-v3-preflight.v1",
        "status": "PASS_FAIL_CLOSED_STATIC_AND_FIXTURE_PREFLIGHT",
        "run_name": RUN_NAME,
        "attack_contract_count": len(attacks),
        "candidate_gzip_row_counts": gzip_rows,
        "candidate_exact_six": True,
        "pinned_input_count": len(hashes),
        "validator_sha256": hashes[os.fspath(VALIDATOR)],
        "formal_credit": 0,
        "source_W_formal_remainder": 80,
        "downstream_publication_authorized": False,
    }


def validate(run_argument: Path) -> dict[str, Any]:
    run = safe_run_directory(run_argument, completed=True)
    captured = {
        name: captured_file(run / name, 16 * 1024 * 1024)
        for name in sorted(COMPLETED_RUN_FILES)
    }
    require(captured["command.txt"] == command_bytes(), "exact command bytes")
    require(captured["provenance.json"] == provenance_bytes(),
            "exact canonical provenance bytes")
    require(captured["run.sh"] == runner_bytes(), "exact versioned runner bytes")
    provenance = parse_json(captured["provenance.json"], "provenance")
    require(provenance == provenance_object(), "exact provenance contract")

    current = current_hashes()
    pre = parse_sha_ledger(captured["pre.sha256"], "pre.sha256")
    post = parse_sha_ledger(captured["post.sha256"], "post.sha256")
    require(pre == post, "pre/post sha256 byte identities")
    require(captured["pre.stat"] == captured["post.stat"],
            "pre/post stat identities")
    bound = dict(current)
    bound[os.fspath(run / "command.txt")] = sha256(command_bytes())
    bound[os.fspath(run / "provenance.json")] = sha256(provenance_bytes())
    bound[os.fspath(run / "run.sh")] = sha256(runner_bytes())
    require(pre == bound, "pre/post hashes equal current pinned bytes")

    observed_stat = parse_stat_ledger(captured["pre.stat"], "pre.stat")
    expected_stat_paths = {
        os.fspath(PYTHON), os.fspath(HARNESS), os.fspath(VERIFIER),
        os.fspath(VALIDATOR), os.fspath(CANDIDATE),
        *(os.fspath(CANDIDATE / name) for name in CANDIDATE_HASHES),
    }
    require(set(observed_stat) == expected_stat_paths, "stat exact path set")
    for path_text, recorded in observed_stat.items():
        state = os.lstat(path_text)
        is_root = path_text == os.fspath(CANDIDATE)
        is_python = path_text == os.fspath(PYTHON)
        if is_python:
            require(stat.S_ISLNK(state.st_mode) and state.st_nlink == 1,
                    "current Python link")
            value, _target, link = python_hash()
            require(value == EXPECTED_PYTHON_SHA256
                    and stat_identity(link) == stat_identity(state),
                    "current Python chain/hash")
        else:
            require((stat.S_ISDIR(state.st_mode) if is_root else
                     stat.S_ISREG(state.st_mode) and state.st_nlink == 1)
                    and not stat.S_ISLNK(state.st_mode),
                    "current stat type/singleton:" + path_text)
        current_stat = {
            "dev": state.st_dev, "ino": state.st_ino, "mode": state.st_mode,
            "links": state.st_nlink, "size": state.st_size,
            "mtime": int(state.st_mtime), "ctime": int(state.st_ctime),
        }
        require(recorded == current_stat, "recorded stat equals current:" + path_text)

    require(captured["exit_code.txt"] == b"0\n", "numeric exit zero")
    require(captured["stderr.log"] == b"", "empty harness stderr")
    require(POSITIVE_INTEGER.fullmatch(captured["wrapper_pid.txt"]) is not None,
            "numeric wrapper PID")
    require(POSITIVE_INTEGER.fullmatch(captured["time_pid.txt"]) is not None,
            "numeric time PID")
    require(re.fullmatch(rb"[1-9][0-9]*(?: [1-9][0-9]*)*\n",
                         captured["observed_child_pids.txt"]) is not None,
            "observed child PID receipt")
    start = parse_utc(captured["start_utc.txt"], "start")
    end = parse_utc(captured["end_utc.txt"], "end")
    require(start < end, "positive run interval")
    elapsed = validate_time(captured["time.txt"])

    harness_raw = captured_file(HARNESS, 256 * 1024)
    output = parse_json(captured["stdout.json"], "harness stdout")
    require(canonical(output) + b"\n" == captured["stdout.json"],
            "canonical harness stdout bytes")
    require(set(output) == {
        "C30b_input_kind", "C30c_publisher_I_O_authority", "attack_count",
        "attacks", "baseline_file_sha256", "baseline_result_sha256",
        "formal_credit", "manifest_authorized", "schema", "status",
    }, "exact harness output keys")
    require(
        output["schema"]
        == "cm2.round306c30c.source-w-full-delta.coherent-attack-harness.candidate.v1"
        and output["status"] == EXPECTED_STATUS
        and type(output["attack_count"]) is int and output["attack_count"] == 62
        and type(output["formal_credit"]) is int and output["formal_credit"] == 0
        and output["manifest_authorized"] is False
        and output["baseline_result_sha256"] == EXPECTED_BASELINE_RESULT_SHA256
        and output["baseline_file_sha256"] == CANDIDATE_HASHES
        and output["C30b_input_kind"] == "FIXED_FORMALLY_SEALED_MANIFEST_AUTHORITY",
        "exact zero-credit harness conclusion",
    )
    require(output["C30c_publisher_I_O_authority"] == {
        "producer_filename": PREFIX + "_producer.py",
        "producer_sha256":
            "4644f8aad5fb9b2956a3854d1457d40c93c7f4f134ca808c782d61e0c526e549",
        "loading": "AST_EXTRACTED_SHORT_I_O_HELPERS_FROM_PINNED_BYTES",
        "synthetic_payload_file_count": 6,
        "positive_visibility_transition": "ABSENT_TO_EXACT_SIX",
        "noreplace_cases": [
            "PREEXISTING_COMPLETE", "PREEXISTING_PARTIAL", "CONCURRENT_EEXIST",
        ],
    }, "exact publisher I/O authority")
    contract = attack_contract(harness_raw)
    require(type(output["attacks"]) is list and len(output["attacks"]) == 62,
            "exact 62 output attacks")
    for expected, observed in zip(contract, output["attacks"], strict=True):
        require(type(observed) is dict and set(observed) == {
            "attack", "expected_reason_prefix", "layer", "rejection",
        }, "attack output object")
        require(all(observed[key] == expected[key] for key in expected),
                "attack identity/order matches pinned AST")
        rejection = observed["rejection"]
        require(type(rejection) is str and ":" in rejection
                and rejection.split(":", 1)[1].startswith(
                    expected["expected_reason_prefix"]),
                "attack expected rejection:" + expected["attack"])

    return {
        "schema": OUTPUT_SCHEMA,
        "status": "PASS_COMPLETE_C30C_62_ATTACK_RUN_RECEIPT_V3__ZERO_FORMAL_CREDIT",
        "run_directory": run.name,
        "run_start_utc": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "run_end_utc": end.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "elapsed": elapsed,
        "harness_stdout_sha256": sha256(captured["stdout.json"]),
        "harness_sha256": EXPECTED_HARNESS_SHA256,
        "verifier_sha256": EXPECTED_VERIFIER_SHA256,
        "validator_sha256": current[os.fspath(VALIDATOR)],
        "python_sha256": EXPECTED_PYTHON_SHA256,
        "baseline_result_sha256": EXPECTED_BASELINE_RESULT_SHA256,
        "attack_count": 62,
        "pre_post_sha256_identical": True,
        "pre_post_stat_identical": True,
        "numeric_exit_code": 0,
        "signal": None,
        "formal_credit": 0,
        "manifest_authorized": False,
        "source_W_formal_remainder": 80,
        "source_W_transition_authorized": False,
        "downstream_publication_authorized": False,
        "authority": "AUDIT_ONLY_REQUIRES_DUAL_VERIFIER_COLD_TOCTOU_AND_TERMINAL_REPLAY",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_directory", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args()
    require(arguments.self_test != (arguments.run_directory is not None),
            "choose exactly one of --self-test or run_directory")
    result = self_test() if arguments.self_test else validate(arguments.run_directory)
    print(canonical(result).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Reject, OSError, KeyError, TypeError, ValueError) as error:
        print("REJECT_C30C_ATTACK_RUN_RECEIPT_V3:" + str(error), file=sys.stderr)
        raise SystemExit(1)
