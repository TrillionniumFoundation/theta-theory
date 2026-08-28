#!/usr/bin/env python3
"""Append-only exact-contract process runner for C27R2 release repair v4.

The Python executable is supplied explicitly and SHA-pinned; no system-Python
path is embedded in this source.  Every declared input is held open with
O_NOFOLLOW, SHA-256 and a nine-field stat identity are compared before/after
the isolated child, and PASS is written last.  All outcomes are zero-credit.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import stat
import subprocess
import sys
import tempfile
import time
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
BASE = "cm2.round306c27r2.source-g-authority-v2.release-repair."
SPEC_SCHEMA = BASE + "release-repair-process-command-spec.v4"
SPEC_STATUS = "FROZEN_C27R2_RELEASE_REPAIR_V4_EXACT_PROCESS_COMMAND_SPEC"
PINSET_SCHEMA = BASE + "release-repair-process-pinset.v4"
PINSET_STATUS = "FROZEN_C27R2_RELEASE_REPAIR_V4_EXACT_PROCESS_PINSET"
RUN_SCHEMA = BASE + "release-repair-process-run-attestation.v4"
RUN_STATUS = (
    "PASS_C27R2_RELEASE_REPAIR_PROCESS_EXIT0_NULL_SIGNAL_EMPTY_STDERR_"
    "EXACT_SPEC_PINSET_ARGV_ENV_PRE_POST_FULL9STAT_AND_OUTPUT_INVENTORY__"
    "ZERO_CREDIT"
)
FAIL_SCHEMA = BASE + "release-repair-process-failure-receipt.v4"
PASS = b"PASS_C27R2_RELEASE_REPAIR_V4_PROCESS_TRANSACTION__ZERO_CREDIT\n"
EMPTY_SHA = hashlib.sha256(b"").hexdigest()
STAGES = {
    "boundary_preflight", "fresh_cold", "snapshot", "baseline",
    "integrity70_plus_lock8",
    "post", "post_evidence", "manifest", "outer", "conditional_seal",
    "anticipated_terminal",
}
FORMAL_EXECUTION_AUTHORIZED = False  # boundary v5/full-chain audit still pending.
SPEC_KEYS = {
    "schema", "status", "stage", "pinset_file_sha256",
    "pinset_object_sha256", "runner_source_sha256", "python_path",
    "python_sha256", "source_path", "source_sha256", "input_paths",
    "output_roots", "output_documents", "python_hash_seed", "environment",
    "argv_template", "argv_template_sha256", "argv_bindings",
    "argv_bindings_sha256", "expanded_argv", "expanded_argv_sha256",
    "publication_lock",
    "timeout_seconds", "expected_stdout", "formal_credit",
    "manifest_authorized", "authority_minted", "command_spec_sha256",
}
PLACEHOLDER = re.compile(r"\$\{([A-Z][A-Z0-9_]*)\}")
LOCK_SCHEMA = BASE + "publication-lock.v1"
LOCK_STATUS = "FROZEN_ONE_SHOT_PUBLICATION_LOCK__NO_AUTHORITY"
LOCK_PROTOCOL = "FLOCK_EXCLUSIVE_WHOLE_PUBLICATION_WINDOW_V1"
PINSET_KEYS = {
    "schema", "status", "stage", "runner_source_sha256", "python_path",
    "python_sha256", "source_path", "source_sha256", "input_members",
    "formal_credit", "manifest_authorized", "authority_minted",
    "pinset_sha256",
}


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


def expand_argv(template: Any, bindings: Any) -> list[str]:
    need(type(template) is list and len(template) >= 4
         and all(type(token) is str and token and "\x00" not in token
                 and "\n" not in token and "\r" not in token
                 for token in template), "strict argv template tokens")
    need(type(bindings) is dict and list(bindings) == sorted(bindings)
         and all(re.fullmatch(r"[A-Z][A-Z0-9_]*", role) is not None
                 and type(value) is str and value and "\x00" not in value
                 and "\n" not in value and "\r" not in value
                 for role, value in bindings.items()),
         "sorted strict argv bindings")
    referenced: list[str] = []
    expanded: list[str] = []
    for token in template:
        match = PLACEHOLDER.fullmatch(token)
        if match is None:
            need("${" not in token and "}" not in token,
                 "placeholder must occupy whole argv token")
            expanded.append(token)
            continue
        role = match.group(1)
        need(role in bindings, "unknown argv placeholder:" + role)
        referenced.append(role)
        expanded.append(bindings[role])
    need(sorted(set(referenced)) == list(bindings),
         "every binding referenced and no residual/unknown placeholders")
    return expanded


def canonical_outer_argv(args: argparse.Namespace, python_path: Path) -> list[str]:
    values = [
        ("stage", args.stage), ("command-spec", args.command_spec),
        ("pinset", args.pinset), ("run-dir", args.run_dir),
        ("python", args.python),
        ("expect-runner-sha256", args.expect_runner_sha256),
        ("expect-python-sha256", args.expect_python_sha256),
        ("expect-command-spec-file-sha256",
         args.expect_command_spec_file_sha256),
        ("expect-command-spec-object-sha256",
         args.expect_command_spec_object_sha256),
        ("expect-pinset-file-sha256", args.expect_pinset_file_sha256),
        ("expect-pinset-object-sha256", args.expect_pinset_object_sha256),
        ("publication-lock-fd", args.publication_lock_fd),
    ]
    need(all(type(value) is str for _, value in values),
         "outer runner constructor inputs")
    answer = [str(python_path), "-I", "-B", str(SELF)]
    for name, value in values:
        answer.extend(["--" + name, value])
    return answer


def valid_sha(value: Any) -> bool:
    return (type(value) is str and len(value) == 64
            and all(c in "0123456789abcdef" for c in value))


def strict(raw: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in items:
            need(type(key) is str and key not in out, "duplicate JSON key")
            out[key] = value
        return out
    return json.loads(raw, object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(
                          Rejected("non-finite JSON:" + x)))


def fingerprint(info: os.stat_result) -> list[int]:
    return [info.st_dev, info.st_ino, info.st_mode, info.st_nlink,
            info.st_size, info.st_mtime_ns, info.st_ctime_ns,
            info.st_uid, info.st_gid]


def workspace_path(raw: str, absent: bool = False) -> Path:
    supplied = Path(raw)
    path = (supplied if supplied.is_absolute() else ROOT / supplied).absolute()
    try:
        relative = path.relative_to(ROOT)
    except ValueError as error:
        raise Rejected("path outside workspace:" + raw) from error
    need(relative.parts and all(p not in {"", ".", ".."}
                                for p in relative.parts), "canonical path")
    cursor = ROOT
    for part in relative.parts:
        cursor /= part
        if not cursor.exists():
            need(absent, "missing path:" + str(cursor))
            break
        need(not cursor.is_symlink(), "symlink path:" + str(cursor))
    return path


def external_regular(raw: str) -> Path:
    path = Path(raw).absolute()
    need(path.is_absolute() and path.is_file() and not path.is_symlink(),
         "external regular executable")
    return path


class Capture:
    def __init__(self, path: Path, label: str):
        self.path, self.label = path, label
        self.fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
                          | getattr(os, "O_CLOEXEC", 0))
        try:
            self.before = os.fstat(self.fd)
            need(stat.S_ISREG(self.before.st_mode) and self.before.st_nlink == 1,
                 label + ": regular single-link")
            self.sha256 = self._sha()
        except BaseException:
            os.close(self.fd)
            raise

    def _sha(self) -> str:
        os.lseek(self.fd, 0, os.SEEK_SET)
        state = hashlib.sha256()
        while block := os.read(self.fd, 4 << 20):
            state.update(block)
        os.lseek(self.fd, 0, os.SEEK_SET)
        need(fingerprint(os.fstat(self.fd)) == fingerprint(self.before),
             self.label + ": stable FD")
        return state.hexdigest()

    def bytes(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        chunks: list[bytes] = []
        while block := os.read(self.fd, 4 << 20):
            chunks.append(block)
        os.lseek(self.fd, 0, os.SEEK_SET)
        need(fingerprint(os.fstat(self.fd)) == fingerprint(self.before),
             self.label + ": stable read")
        return b"".join(chunks)

    def document(self, closure: str) -> dict[str, Any]:
        raw = self.bytes()
        need(raw.endswith(b"\n"), self.label + ": newline")
        value = strict(raw[:-1])
        need(type(value) is dict and canonical(value) == raw[:-1],
             self.label + ": canonical JSON")
        body = dict(value)
        claim = body.pop(closure, None)
        need(valid_sha(claim) and claim == digest(body),
             self.label + ": object closure")
        return value

    def attest(self) -> dict[str, Any]:
        current = os.stat(self.path, follow_symlinks=False)
        need(fingerprint(current) == fingerprint(self.before)
             and fingerprint(os.fstat(self.fd)) == fingerprint(self.before)
             and self._sha() == self.sha256,
             self.label + ": current SHA/nine-stat")
        try:
            shown = str(self.path.relative_to(ROOT))
        except ValueError:
            shown = str(self.path)
        return {"path": shown, "sha256": self.sha256,
                "stat_fingerprint": fingerprint(self.before),
                "O_NOFOLLOW": True, "single_link": True}

    def close(self) -> None:
        os.close(self.fd)


def _write_all(fd: int, raw: bytes, writer: Any = os.write) -> None:
    offset = 0
    while offset < len(raw):
        count = writer(fd, raw[offset:])
        need(type(count) is int and count > 0, "write made positive progress")
        offset += count


def write_once(path: Path, raw: bytes) -> None:
    parent = os.open(path.parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
                     | getattr(os, "O_NOFOLLOW", 0)
                     | getattr(os, "O_CLOEXEC", 0))
    fd = -1
    try:
        fd = os.open(path.name, os.O_WRONLY | os.O_CREAT | os.O_EXCL
            | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0),
            0o400, dir_fd=parent)
        _write_all(fd, raw)
        os.fsync(fd)
        before = os.fstat(fd)
    finally:
        if fd >= 0:
            os.close(fd)
    reopened = os.open(path.name, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
                       | getattr(os, "O_CLOEXEC", 0), dir_fd=parent)
    try:
        chunks: list[bytes] = []
        while block := os.read(reopened, 1 << 20):
            chunks.append(block)
        after = os.fstat(reopened)
        current = os.stat(path.name, dir_fd=parent, follow_symlinks=False)
        observed = b"".join(chunks)
        need(observed == raw and stat.S_ISREG(after.st_mode) and after.st_nlink == 1
             and fingerprint(before) == fingerprint(after) == fingerprint(current)
             and hashlib.sha256(raw).digest() == hashlib.sha256(observed).digest(),
             "reopen exact bytes/SHA/full9stat/single-link")
        os.fsync(parent)
    finally:
        os.close(reopened)
        os.close(parent)


def fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
                         | getattr(os, "O_NOFOLLOW", 0))
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def write_json(path: Path, value: Any) -> None:
    write_once(path, canonical(value) + b"\n")


def file_record(path: Path) -> dict[str, Any]:
    cap = Capture(path, "output:" + str(path))
    try:
        return cap.attest()
    finally:
        cap.close()


def snapshot(outputs: list[dict[str, Any]]) -> dict[str, Any]:
    answer: dict[str, Any] = {}
    for item in outputs:
        need(type(item) is dict and set(item) == {"path", "exact_files"},
             "output contract shape")
        directory = workspace_path(item["path"])
        exact = item["exact_files"]
        need(directory.is_dir() and not directory.is_symlink()
             and type(exact) is list and exact == sorted(set(exact)),
             "output directory/exact inventory")
        actual = sorted(str(p.relative_to(directory))
                        for p in directory.rglob("*") if p.is_file())
        need(actual == exact, "output exact file inventory")
        need(not any(p.is_symlink() for p in directory.rglob("*")),
             "output no symlinks")
        answer[item["path"]] = [file_record(directory / name)
                                 for name in exact]
    return answer


def utc() -> str:
    return datetime.now(timezone.utc).isoformat(
        timespec="microseconds").replace("+00:00", "Z")


def execute(args: argparse.Namespace, self_test_only: bool = False) -> dict[str, Any]:
    need(self_test_only or FORMAL_EXECUTION_AUTHORIZED,
         "formal transaction execution remains explicitly disabled")
    need(valid_sha(args.expect_runner_sha256)
         and valid_sha(args.expect_python_sha256)
         and valid_sha(args.expect_command_spec_file_sha256)
         and valid_sha(args.expect_command_spec_object_sha256)
         and valid_sha(args.expect_pinset_file_sha256)
         and valid_sha(args.expect_pinset_object_sha256), "dynamic pins")
    run_dir = workspace_path(args.run_dir, absent=True)
    need(not run_dir.exists() and not run_dir.is_symlink(), "fresh run dir")
    run_dir.mkdir(parents=True, mode=0o700)
    fsync_directory(run_dir)
    fsync_directory(run_dir.parent)
    started = utc()
    stage = "unparsed"
    captures: list[Capture] = []
    pinned_only: list[Capture] = []
    try:
        runner = Capture(SELF, "runner"); pinned_only.append(runner)
        python = Capture(external_regular(args.python), "python")
        pinned_only.append(python)
        spec_cap = Capture(workspace_path(args.command_spec), "command spec")
        captures.append(spec_cap)
        pin_cap = Capture(workspace_path(args.pinset), "pinset")
        captures.append(pin_cap)
        need(runner.sha256 == args.expect_runner_sha256
             and python.sha256 == args.expect_python_sha256,
             "runner/Python current pins")
        outer_argv = canonical_outer_argv(args, python.path)
        if not self_test_only:
            need(sys.flags.isolated == 1 and sys.dont_write_bytecode
                 and [str(python.path), "-I", "-B", *sys.argv] == outer_argv,
                 "exact outer runner argv and isolated Python flags")
        spec = spec_cap.document("command_spec_sha256")
        pinset = pin_cap.document("pinset_sha256")
        need(set(spec) == SPEC_KEYS and set(pinset) == PINSET_KEYS
             and spec_cap.sha256 == args.expect_command_spec_file_sha256
             and spec["command_spec_sha256"]
                 == args.expect_command_spec_object_sha256
             and pin_cap.sha256 == args.expect_pinset_file_sha256
             and pinset["pinset_sha256"] == args.expect_pinset_object_sha256
             and spec.get("schema") == SPEC_SCHEMA
             and spec.get("status") == SPEC_STATUS
             and pinset.get("schema") == PINSET_SCHEMA
             and pinset.get("status") == PINSET_STATUS
             and spec.get("formal_credit") == pinset.get("formal_credit") == 0
             and spec.get("manifest_authorized") is False
             and pinset.get("manifest_authorized") is False
             and spec.get("authority_minted") is False
             and pinset.get("authority_minted") is False,
             "exact spec/pinset schemas, inventories and governance")
        lock = spec.get("publication_lock")
        need(type(lock) is dict and set(lock) == {"path", "file_sha256",
             "object_sha256", "stat_fingerprint", "fd", "schema", "status",
             "protocol"} and valid_sha(lock["file_sha256"])
             and valid_sha(lock["object_sha256"])
             and type(lock["stat_fingerprint"]) is list
             and len(lock["stat_fingerprint"]) == 9
             and lock["schema"] == LOCK_SCHEMA and lock["status"] == LOCK_STATUS
             and lock["protocol"] == LOCK_PROTOCOL
             and type(args.publication_lock_fd) is str
             and args.publication_lock_fd.isdigit()
             and lock["fd"] == int(args.publication_lock_fd) >= 3,
             "exact inherited publication lock contract")
        lock_fd = lock["fd"]
        lock_path = workspace_path(lock["path"])
        lock_info = os.fstat(lock_fd)
        need(stat.S_ISREG(lock_info.st_mode) and lock_info.st_nlink == 1
             and fingerprint(lock_info) == lock["stat_fingerprint"]
             and fingerprint(os.stat(lock_path, follow_symlinks=False))
                 == lock["stat_fingerprint"],
             "publication lock inherited FD/path identity")
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        lock_cap = Capture(lock_path, "publication-lock")
        pinned_only.append(lock_cap)
        lock_document = lock_cap.document("publication_lock_sha256")
        need(lock_cap.sha256 == lock["file_sha256"]
             and lock_document["publication_lock_sha256"]
                 == lock["object_sha256"]
             and lock_document.get("schema") == LOCK_SCHEMA
             and lock_document.get("status") == LOCK_STATUS
             and lock_document.get("protocol") == LOCK_PROTOCOL
             and lock_document.get("formal_credit") == 0
             and lock_document.get("manifest_authorized") is False
             and lock_document.get("authority_minted") is False,
             "publication lock object/current byte pins")
        stage = spec.get("stage")
        need(type(stage) is str and stage == args.stage and stage in STAGES
             and pinset.get("stage") == stage,
             "exact stage")
        need(spec.get("pinset_file_sha256") == pin_cap.sha256
             and spec.get("pinset_object_sha256") == pinset["pinset_sha256"]
             and spec.get("runner_source_sha256") == runner.sha256
             and spec.get("python_path") == str(python.path)
             and spec.get("python_sha256") == python.sha256
             and pinset.get("runner_source_sha256") == runner.sha256
             and pinset.get("python_path") == str(python.path)
             and pinset.get("python_sha256") == python.sha256,
             "spec dynamic source closure")
        source = workspace_path(spec["source_path"])
        source_cap = Capture(source, "stage source")
        pinned_only.append(source_cap)
        need(source_cap.sha256 == spec.get("source_sha256")
             and pinset.get("source_path") == spec.get("source_path")
             and pinset.get("source_sha256") == source_cap.sha256,
             "source pin")
        declared = spec.get("input_paths")
        need(type(declared) is list and declared == sorted(set(declared)),
             "sorted unique inputs")
        input_members = pinset.get("input_members")
        need(type(input_members) is list
             and [row.get("path") for row in input_members] == declared
             and all(type(row) is dict and set(row) == {"path", "sha256"}
                     and valid_sha(row["sha256"]) for row in input_members),
             "pinset exact input member inventory")
        seen = {c.path for c in captures}
        for ordinal, (raw, member) in enumerate(zip(declared, input_members,
                                                     strict=True)):
            path = workspace_path(raw)
            need(path not in seen, "unique input")
            seen.add(path)
            capture = Capture(path, f"declared-{ordinal:04d}")
            need(capture.sha256 == member["sha256"], "declared input SHA")
            captures.append(capture)
        need(file_record(SELF)["path"] in declared
             and spec["source_path"] in declared,
             "runner and stage source included in exact declared inputs")
        outputs = spec.get("output_roots")
        need(type(outputs) is list and len(outputs) > 0, "output roots")
        for item in outputs:
            need(type(item) is dict and set(item) == {"path", "exact_files"},
                 "output contract")
            path = workspace_path(item["path"], absent=True)
            need(not path.exists() and not path.is_symlink(), "fresh output")
            need(path not in seen and run_dir not in path.parents
                 and path not in run_dir.parents, "separated outputs")
        seed = spec.get("python_hash_seed")
        env = {"PATH": "/usr/bin:/bin", "HOME": "/nonexistent",
               "LANG": "C", "LC_ALL": "C", "TZ": "UTC",
               "PYTHONHASHSEED": seed}
        need(type(seed) is str and seed.isdigit()
             and spec.get("environment") == env, "exact environment")
        template = spec.get("argv_template")
        bindings = spec.get("argv_bindings")
        command = expand_argv(template, bindings)
        need(spec.get("argv_template_sha256") == digest(template)
             and spec.get("argv_bindings_sha256") == digest(bindings)
             and spec.get("expanded_argv") == command
             and spec.get("expanded_argv_sha256") == digest(command)
             and len(command) >= 4 and command[:4] == [
            str(python.path), "-I", "-B", str(source)]
             and all(type(value) is str for value in command),
            "single canonical inner argv expansion and pinned Python command")
        timeout = spec.get("timeout_seconds")
        need(type(timeout) is int and 1 <= timeout <= 86_400,
             "timeout bound")
        write_json(run_dir / "runner_start.json", {
            "schema": RUN_SCHEMA + ".start", "stage": stage,
            "started_at_utc": started, "formal_credit": 0,
            "C27R2": "AUDIT_HOLD_UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM"})
        before = {c.label: c.attest() for c in captures}
        pinned_before = {c.label: c.attest() for c in pinned_only}
        write_json(run_dir / "input_pre.json", before)
        begun = time.monotonic()
        process = subprocess.Popen(command, cwd=ROOT, env=env,
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, start_new_session=True,
            pass_fds=(lock_fd,))
        timed_out = False
        try:
            stdout, stderr = process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(process.pid, signal.SIGKILL)
            stdout, stderr = process.communicate()
        elapsed = round(time.monotonic() - begun, 6)
        returncode = process.returncode
        need(type(returncode) is int, "return code")
        child_signal = -returncode if returncode < 0 else None
        numeric_exit = returncode if returncode >= 0 else 128 - returncode
        write_once(run_dir / "stdout.log", stdout)
        write_once(run_dir / "stderr.log", stderr)
        write_once(run_dir / "exit_code.txt", f"{numeric_exit}\n".encode())
        write_json(run_dir / "signal.json", child_signal)
        write_json(run_dir / "timing.json", {
            "elapsed_seconds": elapsed, "timed_out": timed_out})
        after = {c.label: c.attest() for c in captures}
        pinned_after = {c.label: c.attest() for c in pinned_only}
        write_json(run_dir / "input_post.json", after)
        need(before == after and pinned_before == pinned_after,
             "input and pinned-source pre/post SHA/nine-stat")
        expected_attested_paths = [spec_cap.attest()["path"],
                                   pin_cap.attest()["path"], *declared]
        observed_attested_paths = [item["path"] for item in after.values()]
        need(observed_attested_paths == expected_attested_paths,
             "ordered attested paths exactly spec/pinset plus declared inputs")
        observed = snapshot(outputs)
        write_json(run_dir / "output_validation.json", observed)
        output_documents = spec.get("output_documents")
        need(type(output_documents) is list
             and output_documents == sorted(output_documents,
                                              key=lambda row: row["path"]),
             "sorted exact output document contracts")
        for contract in output_documents:
            need(type(contract) is dict and set(contract) == {
                "path", "closure", "schema", "status"},
                "output document contract shape")
            output_capture = Capture(workspace_path(contract["path"]),
                                     "output-document")
            try:
                value = output_capture.document(contract["closure"])
                need(value.get("schema") == contract["schema"]
                     and value.get("status") == contract["status"]
                     and value.get("formal_credit") == 0,
                     "output document schema/status")
            finally:
                output_capture.close()
        need(not timed_out and numeric_exit == 0 and child_signal is None
             and stderr == b"" and hashlib.sha256(stderr).hexdigest() == EMPTY_SHA,
             "exit0/null signal/empty stderr")
        expected = spec.get("expected_stdout")
        need(stdout.endswith(b"\n"), "stdout newline")
        parsed = strict(stdout[:-1])
        need(type(expected) is dict and parsed == expected
             and canonical(parsed) == stdout[:-1]
             and parsed.get("formal_credit") == 0
             and parsed.get("CM2") == "NO-GO_FOR_CLAIM",
             "canonical exact stdout")
        body = {"schema": RUN_SCHEMA, "status": RUN_STATUS,
            "stage": stage, "started_at_utc": started,
            "completed_at_utc": utc(), "elapsed_seconds": elapsed,
            "numeric_exit_code": 0, "signal": None, "timed_out": False,
            "stderr_empty": True, "stdout_sha256": hashlib.sha256(stdout).hexdigest(),
            "stderr_sha256": EMPTY_SHA, "input_pre_post_identical": True,
            "input_attestations": after, "output_validation": observed,
            "command_spec_file_sha256": spec_cap.sha256,
            "command_spec_object_sha256": spec["command_spec_sha256"],
            "pinset_file_sha256": pin_cap.sha256,
            "pinset_object_sha256": pinset["pinset_sha256"],
            "runner_source_sha256": runner.sha256,
            "stage_source_path": spec["source_path"],
            "stage_source_sha256": source_cap.sha256,
            "python_path": str(python.path), "python_sha256": python.sha256,
            "argv_template": template,
            "argv_template_sha256": spec["argv_template_sha256"],
            "argv_bindings": bindings,
            "argv_bindings_sha256": spec["argv_bindings_sha256"],
            "exact_argv": command,
            "expanded_argv_sha256": spec["expanded_argv_sha256"],
            "outer_runner_argv": outer_argv,
            "outer_runner_argv_sha256": digest(outer_argv),
            "outer_runner_argv_constructed_by_frozen_source": True,
            "publication_lock": lock,
            "publication_lock_exclusive_inherited_and_held": True,
            "exact_environment": env,
            "exact_input_paths": declared, "exact_output_roots": outputs,
            "exact_attested_contract_paths": expected_attested_paths,
            "output_document_contracts": output_documents,
            "input_pre_post_sha_full9stat_identical": True,
            "pinned_runner_python_source_pre_post_full9stat_identical": True,
            "formal_credit": 0, "manifest_authorized": False,
            "authority_minted": False,
            "C27R2": "AUDIT_HOLD_UNAUTHORIZED", "C29": "UNAUTHORIZED",
            "CM2": "NO-GO_FOR_CLAIM"}
        result = {**body, "run_attestation_sha256": digest(body)}
        write_json(run_dir / "run_attestation.json", result)
        write_once(run_dir / "PASS.lock", PASS)
        return result
    except BaseException as error:
        if run_dir.exists() and not (run_dir / "PASS.lock").exists():
            body = {"schema": FAIL_SCHEMA,
                "status": "FAILED_CLOSED_C27R2_RELEASE_REPAIR_PROCESS",
                "stage": stage, "failed_at_utc": utc(),
                "error": type(error).__name__ + ":" + str(error),
                "formal_credit": 0, "manifest_authorized": False,
                "C27R2": "AUDIT_HOLD_UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM"}
            receipt = {**body, "failure_receipt_sha256": digest(body)}
            if not (run_dir / "failure_receipt.json").exists():
                write_json(run_dir / "failure_receipt.json", receipt)
            if not (run_dir / "FAILED.lock").exists():
                write_once(run_dir / "FAILED.lock",
                           b"FAILED_C27R2_RELEASE_REPAIR_PROCESS__ZERO_CREDIT\n")
        raise
    finally:
        for cap in captures + pinned_only:
            cap.close()


def self_test_transaction() -> dict[str, Any]:
    """Run the actual v4 runner around a tiny isolated child transaction."""
    need(FORMAL_EXECUTION_AUTHORIZED is False
         and "terminal_finalize" not in STAGES,
         "formal disabled/authority finalizer excluded")
    try:
        _write_all(-1, b"x", lambda _fd, _raw: 0)
        raise Rejected("zero-progress writer unexpectedly accepted")
    except Rejected as error:
        need(str(error) == "write made positive progress",
             "zero-progress write fixture")
    need(expand_argv(["python", "-I", "-B", "${SOURCE}"],
                     {"SOURCE": "/tmp/source.py"})
         == ["python", "-I", "-B", "/tmp/source.py"],
         "single canonical argv expansion fixture")
    for bad_template, bad_bindings in ((["x", "-I", "-B", "${UNKNOWN}"], {}),
                                        (["x", "-I", "-B", "pre${A}"],
                                         {"A": "value"}),
                                        (["x", "-I", "-B", "literal"],
                                         {"UNUSED": "value"})):
        rejected = False
        try:
            expand_argv(bad_template, bad_bindings)
        except Rejected:
            rejected = True
        need(rejected, "bad argv template rejected")
    with tempfile.TemporaryDirectory(dir=ROOT / ".cm2-runtime",
            prefix="c27r2-transaction-v4-selftest-") as raw:
        root = Path(raw)
        lock_body = {"schema": LOCK_SCHEMA, "status": LOCK_STATUS,
            "protocol": LOCK_PROTOCOL, "one_shot_launch_id": "self-test",
            "plan_file_sha256": "1" * 64, "plan_object_sha256": "2" * 64,
            "formal_credit": 0, "manifest_authorized": False,
            "authority_minted": False}
        lock_value = {**lock_body, "publication_lock_sha256": digest(lock_body)}
        lock_path = root / "publication_lock.json"
        lock_path.write_bytes(canonical(lock_value) + b"\n")
        lock_fd = os.open(lock_path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        input_path = root / "input.txt"
        input_path.write_bytes(b"immutable\n")
        output = root / "output"
        receipt_path = output / "receipt.json"
        output_body = {"schema": BASE + "runner-selftest-output.v4",
                       "status": "PASS_REAL_ISOLATED_CHILD_TRANSACTION",
                       "formal_credit": 0}
        output_value = {**output_body, "receipt_sha256": digest(output_body)}
        expected_stdout = {"CM2": "NO-GO_FOR_CLAIM", "formal_credit": 0,
                           "status": "PASS_REAL_ISOLATED_CHILD_TRANSACTION"}
        source = root / "child.py"
        script = (
            "import hashlib,json,pathlib\n"
            f"p=pathlib.Path({str(output)!r});p.mkdir()\n"
            f"v={output_value!r}\n"
            "raw=json.dumps(v,sort_keys=True,separators=(',',':'),"
            "ensure_ascii=True,allow_nan=False).encode('ascii')+b'\\n'\n"
            "(p/'receipt.json').write_bytes(raw)\n"
            f"print(json.dumps({expected_stdout!r},sort_keys=True,"
            "separators=(',',':'),ensure_ascii=True,allow_nan=False))\n"
        ).encode("utf-8")
        source.write_bytes(script)
        python_path = Path(sys.executable).resolve()
        runner_sha = file_record(SELF)["sha256"]
        python_sha = file_record(python_path)["sha256"]
        source_sha = file_record(source)["sha256"]
        input_rel = str(input_path.relative_to(ROOT))
        source_rel = str(source.relative_to(ROOT))
        runner_rel = str(SELF.relative_to(ROOT))
        lock_rel = str(lock_path.relative_to(ROOT))
        declared_inputs = sorted([input_rel, lock_rel, runner_rel, source_rel])
        output_rel = str(output.relative_to(ROOT))
        receipt_rel = str(receipt_path.relative_to(ROOT))
        environment = {"PATH": "/usr/bin:/bin", "HOME": "/nonexistent",
            "LANG": "C", "LC_ALL": "C", "TZ": "UTC",
            "PYTHONHASHSEED": "424242"}
        pinset_body = {"schema": PINSET_SCHEMA, "status": PINSET_STATUS,
            "stage": "snapshot", "runner_source_sha256": runner_sha,
            "python_path": str(python_path), "python_sha256": python_sha,
            "source_path": source_rel, "source_sha256": source_sha,
            "input_members": [{"path": path,
                "sha256": file_record(workspace_path(path))["sha256"]}
                for path in declared_inputs],
            "formal_credit": 0, "manifest_authorized": False,
            "authority_minted": False}
        pinset = {**pinset_body, "pinset_sha256": digest(pinset_body)}
        pinset_path = root / "pinset.json"
        pinset_path.write_bytes(canonical(pinset) + b"\n")
        spec_body = {"schema": SPEC_SCHEMA, "status": SPEC_STATUS,
            "stage": "snapshot",
            "pinset_file_sha256": file_record(pinset_path)["sha256"],
            "pinset_object_sha256": pinset["pinset_sha256"],
            "runner_source_sha256": runner_sha,
            "python_path": str(python_path), "python_sha256": python_sha,
            "source_path": source_rel, "source_sha256": source_sha,
            "input_paths": declared_inputs,
            "output_roots": [{"path": output_rel,
                              "exact_files": ["receipt.json"]}],
            "output_documents": [{"path": receipt_rel,
                "closure": "receipt_sha256",
                "schema": output_body["schema"],
                "status": output_body["status"]}],
            "python_hash_seed": "424242", "environment": environment,
            "argv_template": [str(python_path), "-I", "-B", "${SOURCE_PATH}"],
            "argv_template_sha256": digest(
                [str(python_path), "-I", "-B", "${SOURCE_PATH}"]),
            "argv_bindings": {"SOURCE_PATH": str(source.absolute())},
            "argv_bindings_sha256": digest(
                {"SOURCE_PATH": str(source.absolute())}),
            "expanded_argv": [str(python_path), "-I", "-B",
                              str(source.absolute())],
            "expanded_argv_sha256": digest([str(python_path), "-I", "-B",
                                             str(source.absolute())]),
            "publication_lock": {"path": lock_rel,
                "file_sha256": file_record(lock_path)["sha256"],
                "object_sha256": lock_value["publication_lock_sha256"],
                "stat_fingerprint": fingerprint(os.fstat(lock_fd)),
                "fd": lock_fd, "schema": LOCK_SCHEMA,
                "status": LOCK_STATUS, "protocol": LOCK_PROTOCOL},
            "timeout_seconds": 30, "expected_stdout": expected_stdout,
            "formal_credit": 0, "manifest_authorized": False,
            "authority_minted": False}
        spec = {**spec_body, "command_spec_sha256": digest(spec_body)}
        spec_path = root / "spec.json"
        spec_path.write_bytes(canonical(spec) + b"\n")
        run_dir = root / "run"
        args = argparse.Namespace(stage="snapshot", command_spec=str(spec_path),
            pinset=str(pinset_path), run_dir=str(run_dir), python=str(python_path),
            expect_runner_sha256=runner_sha, expect_python_sha256=python_sha,
            expect_command_spec_file_sha256=file_record(spec_path)["sha256"],
            expect_command_spec_object_sha256=spec["command_spec_sha256"],
            expect_pinset_file_sha256=file_record(pinset_path)["sha256"],
            expect_pinset_object_sha256=pinset["pinset_sha256"],
            publication_lock_fd=str(lock_fd))
        result = execute(args, True)
        need(result["status"] == RUN_STATUS
             and {path.name for path in run_dir.iterdir()} == {
                 "PASS.lock", "exit_code.txt", "input_post.json",
                 "input_pre.json", "output_validation.json",
                 "run_attestation.json", "runner_start.json", "signal.json",
                 "stderr.log", "stdout.log", "timing.json"}
             and (run_dir / "PASS.lock").read_bytes() == PASS,
             "real runner output contract")
        failed_dir = root / "failed-run"
        failed_args = argparse.Namespace(**vars(args))
        failed_args.run_dir = str(failed_dir)
        failed_args.expect_runner_sha256 = "0" * 64
        try:
            execute(failed_args, True)
            raise Rejected("failure fixture unexpectedly accepted")
        except Rejected as error:
            need(str(error) == "runner/Python current pins",
                 "expected real failure reason")
        need({path.name for path in failed_dir.iterdir()} == {
             "FAILED.lock", "failure_receipt.json"}
             and (failed_dir / "FAILED.lock").read_bytes()
                 == b"FAILED_C27R2_RELEASE_REPAIR_PROCESS__ZERO_CREDIT\n",
             "real preflight failure receipt/FAILED lock")
        failure_raw = (failed_dir / "failure_receipt.json").read_bytes()
        failure = strict(failure_raw[:-1]); failure_body = dict(failure)
        failure_claim = failure_body.pop("failure_receipt_sha256", None)
        need(failure_raw.endswith(b"\n")
             and canonical(failure) == failure_raw[:-1]
             and failure.get("schema") == FAIL_SCHEMA
             and failure_claim == digest(failure_body),
             "real canonical failure receipt closure")
        os.close(lock_fd)
        return {"stage": "self_test",
            "status": "PASS_C27R2_RELEASE_REPAIR_TRANSACTION_RUNNER_V4_REAL_SELF_TEST"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    for name in ("stage", "command-spec", "pinset", "run-dir", "python",
                 "expect-runner-sha256", "expect-python-sha256",
                 "expect-command-spec-file-sha256",
                 "expect-command-spec-object-sha256",
                 "expect-pinset-file-sha256", "expect-pinset-object-sha256",
                 "publication-lock-fd"):
        parser.add_argument("--" + name)
    args = parser.parse_args()
    fields = ("stage", "command_spec", "pinset", "run_dir", "python",
              "expect_runner_sha256", "expect_python_sha256",
              "expect_command_spec_file_sha256",
              "expect_command_spec_object_sha256",
              "expect_pinset_file_sha256", "expect_pinset_object_sha256")
    try:
        if args.self_test:
            need(all(getattr(args, f) is None for f in fields),
                 "self-test no dynamic arguments")
            result = self_test_transaction()
        else:
            need(all(getattr(args, f) is not None for f in fields),
                 "all transaction arguments")
            result = execute(args)
        sys.stdout.buffer.write(canonical({"CM2": "NO-GO_FOR_CLAIM",
            "formal_credit": 0, "stage": result["stage"],
            "status": result["status"]}) + b"\n")
        return 0
    except (Rejected, OSError, ValueError, KeyError, TypeError,
            subprocess.SubprocessError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
