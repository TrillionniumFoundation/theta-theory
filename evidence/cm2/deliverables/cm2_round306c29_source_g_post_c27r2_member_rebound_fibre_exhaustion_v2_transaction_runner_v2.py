#!/usr/bin/env python3
"""Fail-closed process transaction runner for the C29-v2 formal chain."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import signal
import stat
import subprocess
import sys
import time
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
PYTHON = Path("/usr/bin/python3.12")
BASE = "cm2.round306c29.source-g-post-c27r2-member-rebound-fibre-exhaustion.v2."
SPEC_SCHEMA = BASE + "process-command-spec.v1"
PINSET_SCHEMA = BASE + "gated-transaction-pinset.v1"
ATTEST_SCHEMA = BASE + "process-run-attestation.v1"
FAIL_SCHEMA = BASE + "process-failure-receipt.v1"


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


def valid_sha(value: Any) -> bool:
    return (type(value) is str and len(value) == 64
            and all(char in "0123456789abcdef" for char in value))


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace(
        "+00:00", "Z")


def strict(payload: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(key not in result, "duplicate JSON key:" + key)
            result[key] = value
        return result
    return json.loads(payload, object_pairs_hook=pairs,
                      parse_constant=lambda value: (_ for _ in ()).throw(
                          Failure("non-finite JSON:" + value)))


def workspace(raw: str | Path, *, may_absent: bool = False) -> Path:
    supplied = Path(raw)
    path = (ROOT / supplied if not supplied.is_absolute() else supplied).absolute()
    try:
        relative = path.relative_to(ROOT)
    except ValueError as error:
        raise Failure("path outside workspace:" + str(raw)) from error
    need(relative.parts and all(part not in {"", ".", ".."}
                                for part in relative.parts),
         "canonical workspace path:" + str(raw))
    cursor = ROOT
    for part in relative.parts:
        cursor = cursor / part
        if not cursor.exists():
            need(may_absent, "missing path component:" + str(cursor))
            break
        need(not cursor.is_symlink(), "symlink path component:" + str(cursor))
    return path


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns,
            value.st_uid, value.st_gid)


class Capture:
    def __init__(self, raw: str | Path, label: str):
        self.path = workspace(raw)
        self.label = label
        self.fd = os.open(self.path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                          | getattr(os, "O_NOFOLLOW", 0))
        self.before = os.fstat(self.fd)
        need(stat.S_ISREG(self.before.st_mode) and self.before.st_nlink == 1,
             label + ":regular-single-link")
        self.sha256 = self._sha()

    def _sha(self) -> str:
        os.lseek(self.fd, 0, os.SEEK_SET)
        state = hashlib.sha256()
        while block := os.read(self.fd, 4 << 20):
            state.update(block)
        os.lseek(self.fd, 0, os.SEEK_SET)
        need(fingerprint(os.fstat(self.fd)) == fingerprint(self.before),
             self.label + ":stable-fd")
        return state.hexdigest()

    def payload(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        chunks: list[bytes] = []
        while block := os.read(self.fd, 4 << 20):
            chunks.append(block)
        os.lseek(self.fd, 0, os.SEEK_SET)
        need(fingerprint(os.fstat(self.fd)) == fingerprint(self.before),
             self.label + ":stable-read")
        return b"".join(chunks)

    def document(self, closure: str) -> dict[str, Any]:
        payload = self.payload()
        need(payload.endswith(b"\n") and not payload.endswith(b"\n\n"),
             self.label + ":newline")
        value = strict(payload[:-1])
        need(type(value) is dict and canonical(value) == payload[:-1],
             self.label + ":canonical")
        body = dict(value)
        claim = body.pop(closure, None)
        need(valid_sha(claim) and claim == digest(body), self.label + ":closure")
        return value

    def attest(self) -> dict[str, Any]:
        need(fingerprint(os.fstat(self.fd)) == fingerprint(self.before),
             self.label + ":fd-stat")
        need(fingerprint(os.stat(self.path, follow_symlinks=False))
             == fingerprint(self.before), self.label + ":path-stat")
        need(self._sha() == self.sha256, self.label + ":sha")
        return {"path": str(self.path.relative_to(ROOT)),
                "sha256": self.sha256, "size": self.before.st_size,
                "stat_fingerprint": list(fingerprint(self.before)),
                "O_NOFOLLOW": True, "single_open_file_description": True}

    def close(self) -> None:
        os.close(self.fd)


def file_sha(path: Path) -> str:
    capture = Capture(path, "file-sha:" + str(path))
    try:
        return capture.sha256
    finally:
        capture.close()


def write_once(path: Path, payload: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                         | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        offset = 0
        while offset < len(payload):
            offset += os.write(descriptor, payload[offset:])
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def write_json(path: Path, value: Any) -> None:
    write_once(path, canonical(value) + b"\n")


def overlap(left: Path, right: Path) -> bool:
    return left == right or left in right.parents or right in left.parents


def relative_name(value: Any) -> bool:
    if type(value) is not str or not value:
        return False
    path = Path(value)
    return (not path.is_absolute() and str(path) == value
            and all(part not in {"", ".", ".."} for part in path.parts))


def preflight_outputs(specs: Any, run_dir: Path,
                      protected: set[Path]) -> list[Path]:
    need(type(specs) is list and bool(specs), "nonempty output specs")
    roots: list[Path] = []
    for ordinal, item in enumerate(specs):
        need(type(item) is dict and set(item) == {
            "path", "kind", "precondition", "exact_inventory",
            "required_relative_files"}, f"output spec:{ordinal}")
        kind = item["kind"]
        condition = item["precondition"]
        exact = item["exact_inventory"]
        required = item["required_relative_files"]
        need(kind in {"file", "directory"}
             and condition in {"ABSENT", "EXISTING_EMPTY_DIRECTORY"},
             f"output kind/precondition:{ordinal}")
        need(type(required) is list and required == sorted(set(required))
             and all(relative_name(name) for name in required),
             f"output required inventory:{ordinal}")
        need(exact is None or (type(exact) is list
             and exact == sorted(set(exact))
             and all(relative_name(name) for name in exact)
             and all(name in exact for name in required)),
             f"output exact inventory:{ordinal}")
        if kind == "file":
            need(condition == "ABSENT" and exact is None and required == [],
                 f"file output contract:{ordinal}")
        path = workspace(item["path"], may_absent=(condition == "ABSENT"))
        need(path.parent.is_dir() and not path.parent.is_symlink(),
             f"output parent:{ordinal}")
        if condition == "ABSENT":
            need(not path.exists() and not path.is_symlink(),
                 f"output absent:{ordinal}")
        else:
            need(kind == "directory" and path.is_dir()
                 and not path.is_symlink() and next(path.iterdir(), None) is None,
                 f"output empty directory:{ordinal}")
        need(not overlap(path, run_dir)
             and all(not overlap(path, value) for value in protected)
             and all(not overlap(path, value) for value in roots),
             f"output separation:{ordinal}")
        roots.append(path)
    return roots


def snapshot_file(path: Path) -> dict[str, Any]:
    need(path.is_file() and not path.is_symlink(), "output regular:" + str(path))
    before = path.stat()
    need(before.st_nlink == 1, "output single-link:" + str(path))
    sha = file_sha(path)
    need(fingerprint(path.stat()) == fingerprint(before),
         "output stable:" + str(path))
    return {"path": str(path.relative_to(ROOT)), "sha256": sha,
            "size": before.st_size,
            "stat_fingerprint": list(fingerprint(before))}


def snapshot_outputs(specs: list[dict[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for item in specs:
        path = workspace(item["path"])
        if item["kind"] == "file":
            result[item["path"]] = {"kind": "file", "files": [snapshot_file(path)]}
            continue
        need(path.is_dir() and not path.is_symlink(), "output directory")
        files: list[Path] = []
        dirs: list[Path] = []
        for current, dirnames, filenames in os.walk(path):
            base = Path(current)
            for name in dirnames:
                child = base / name
                need(not child.is_symlink(), "output symlink directory")
                dirs.append(child)
            for name in filenames:
                child = base / name
                need(not child.is_symlink(), "output symlink file")
                files.append(child)
        inventory = sorted(str(value.relative_to(path)) for value in files)
        exact = item["exact_inventory"]
        required = item["required_relative_files"]
        need(exact is None or inventory == exact, "exact output inventory")
        need(all(name in inventory for name in required), "required output inventory")
        result[item["path"]] = {
            "kind": "directory", "directory_count": len(dirs),
            "relative_file_inventory": inventory,
            "files": [snapshot_file(value) for value in sorted(files)]}
    return result


def parse_stdout(payload: bytes, expected: str) -> dict[str, Any]:
    need(payload.endswith(b"\n") and not payload.endswith(b"\n\n"),
         "child stdout newline")
    value = strict(payload[:-1])
    need(type(value) is dict and canonical(value) == payload[:-1],
         "child stdout canonical")
    need(value.get("status") == expected and value.get("formal_credit") == 0
         and value.get("CM2") == "NO-GO_FOR_CLAIM",
         "child expected stdout")
    return value


def failure(run_dir: Path, stage: str, error: str, started: str,
            numeric_exit: int | None, child_signal: int | None,
            timed_out: bool, pre: Any, post: Any, outputs: Any) -> None:
    body = {"schema": FAIL_SCHEMA,
            "status": "FAILED_CLOSED_C29_V2_PROCESS_TRANSACTION__ZERO_CREDIT",
            "stage": stage, "started_at_utc": started, "failed_at_utc": now(),
            "error": error, "numeric_exit_code": numeric_exit,
            "signal": child_signal, "timed_out": timed_out,
            "input_pre": pre, "input_post": post,
            "outputs_observed": outputs, "formal_credit": 0,
            "manifest_authorized": False, "C29": "UNAUTHORIZED",
            "CM2": "NO-GO_FOR_CLAIM"}
    result = dict(body)
    result["failure_receipt_sha256"] = digest(result)
    if not (run_dir / "failure_receipt.json").exists():
        write_json(run_dir / "failure_receipt.json", result)
    if not (run_dir / "FAILED.lock").exists():
        write_once(run_dir / "FAILED.lock",
                   b"FAILED_CLOSED_C29_V2_PROCESS_TRANSACTION\n")


def execute(args: argparse.Namespace) -> dict[str, Any]:
    need(valid_sha(args.expect_runner_sha256)
         and valid_sha(args.expect_python_sha256), "runner/Python pins")
    need(file_sha(SELF) == args.expect_runner_sha256, "runner self pin")
    need(file_sha(PYTHON) == args.expect_python_sha256, "Python pin")
    spec_capture = Capture(args.command_spec, "command-spec")
    pinset_capture = Capture(args.pinset, "pinset")
    captures = [spec_capture, pinset_capture]
    run_dir = workspace(args.run_dir, may_absent=True)
    need(not run_dir.exists(), "fresh run directory")
    stage = "unparsed"
    started = now()
    numeric_exit: int | None = None
    child_signal: int | None = None
    timed_out = False
    pre = post = outputs = None
    try:
        spec = spec_capture.document("command_spec_sha256")
        pinset = pinset_capture.document("pinset_sha256")
        need(spec.get("schema") == SPEC_SCHEMA
             and pinset.get("schema") == PINSET_SCHEMA, "spec/pinset schema")
        stage = spec.get("stage")
        need(type(stage) is str and stage == args.stage, "exact stage")
        need(spec.get("pinset_file_sha256") == pinset_capture.sha256
             and spec.get("pinset_object_sha256") == pinset["pinset_sha256"],
             "spec pins pinset")
        source = workspace(spec["source_path"])
        need(file_sha(source) == spec.get("source_sha256"), "stage source pin")
        argv = spec.get("argv")
        seed = spec.get("python_hash_seed")
        timeout = spec.get("timeout_seconds")
        environment = spec.get("environment")
        need(type(argv) is list and all(type(value) is str for value in argv)
             and argv[:4] == [str(PYTHON), "-I", "-B", str(source)],
             "isolated Python argv")
        need(type(seed) is str and seed.isdigit()
             and environment == {"PATH": "/usr/bin:/bin", "LANG": "C",
                                 "LC_ALL": "C", "PYTHONHASHSEED": seed}
             and type(timeout) is int and 60 <= timeout <= 86_400,
             "environment/seed/timeout")
        raw_inputs = spec.get("input_paths")
        need(type(raw_inputs) is list and raw_inputs == sorted(set(raw_inputs)),
             "sorted unique inputs")
        seen = {spec_capture.path, pinset_capture.path}
        for ordinal, raw in enumerate(raw_inputs):
            capture = Capture(raw, f"declared-input-{ordinal:04d}")
            need(capture.path not in seen, "unique declared input")
            seen.add(capture.path)
            captures.append(capture)
        protected = seen | {source, SELF, PYTHON}
        need(all(not overlap(run_dir, value) for value in protected),
             "run directory separation")
        output_specs = spec.get("output_roots")
        preflight_outputs(output_specs, run_dir, protected)
        run_dir.mkdir(parents=True, mode=0o700)
        pre = {capture.label: capture.attest() for capture in captures}
        write_json(run_dir / "input_pre.json", pre)
        started_clock = time.monotonic()
        process = subprocess.Popen(argv, cwd=ROOT, env=environment,
                                   stdin=subprocess.DEVNULL,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   start_new_session=True)
        try:
            stdout, stderr = process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(process.pid, signal.SIGKILL)
            stdout, stderr = process.communicate()
        elapsed = time.monotonic() - started_clock
        code = process.returncode
        need(type(code) is int, "child return code")
        child_signal = -code if code < 0 else None
        numeric_exit = code if code >= 0 else 128 - code
        write_once(run_dir / "stdout.log", stdout)
        write_once(run_dir / "stderr.log", stderr)
        write_once(run_dir / "exit_code.txt", (str(numeric_exit) + "\n").encode())
        write_json(run_dir / "signal.json", child_signal)
        write_json(run_dir / "timing.json", {"elapsed_seconds": round(elapsed, 6),
                                               "timed_out": timed_out})
        post = {capture.label: capture.attest() for capture in captures}
        write_json(run_dir / "input_post.json", post)
        need(pre == post, "input pre/post identical")
        outputs = snapshot_outputs(output_specs)
        write_json(run_dir / "output_validation.json", outputs)
        need(not timed_out and numeric_exit == 0 and child_signal is None,
             "exit0/null-signal/no-timeout")
        need(stderr == b"", "empty stderr")
        stdout_value = parse_stdout(stdout, spec["expected_stdout_status"])
        body = {"schema": ATTEST_SCHEMA,
                "status": "PASS_C29_V2_PROCESS_TRANSACTION_EXIT0_NULL_SIGNAL_EMPTY_STDERR_PRE_POST_AND_OUTPUTS__ZERO_CREDIT",
                "stage": stage, "started_at_utc": started, "ended_at_utc": now(),
                "elapsed_seconds": round(elapsed, 6), "numeric_exit_code": 0,
                "signal": None, "timed_out": False, "stderr_empty": True,
                "stdout": stdout_value,
                "stdout_sha256": hashlib.sha256(stdout).hexdigest(),
                "stderr_sha256": hashlib.sha256(stderr).hexdigest(),
                "input_pre_post_sha_stat_identical": True,
                "input_attestations": post, "output_validation": outputs,
                "command_spec_file_sha256": spec_capture.sha256,
                "command_spec_object_sha256": spec["command_spec_sha256"],
                "pinset_file_sha256": pinset_capture.sha256,
                "pinset_object_sha256": pinset["pinset_sha256"],
                "runner_source_sha256": args.expect_runner_sha256,
                "stage_source_sha256": spec["source_sha256"],
                "python_sha256": args.expect_python_sha256,
                "formal_credit": 0, "manifest_authorized": False,
                "C29": "UNAUTHORIZED_PENDING_RELEASE_CHAIN",
                "CM2": "NO-GO_FOR_CLAIM"}
        result = dict(body)
        result["run_attestation_sha256"] = digest(result)
        write_json(run_dir / "run_attestation.json", result)
        write_once(run_dir / "PASS.lock",
                   ("PASS_C29_V2_" + stage.upper()
                    + "_PROCESS_TRANSACTION__ZERO_CREDIT\n").encode("ascii"))
        return result
    except BaseException as error:
        if run_dir.exists():
            failure(run_dir, stage, f"{type(error).__name__}:{error}", started,
                    numeric_exit, child_signal, timed_out, pre, post, outputs)
        raise
    finally:
        for capture in captures:
            capture.close()


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--self-test", action="store_true")
    value.add_argument("--stage")
    value.add_argument("--command-spec")
    value.add_argument("--pinset")
    value.add_argument("--run-dir")
    value.add_argument("--expect-runner-sha256")
    value.add_argument("--expect-python-sha256")
    return value


def main() -> int:
    try:
        args = parser().parse_args()
        fields = ("stage", "command_spec", "pinset", "run_dir",
                  "expect_runner_sha256", "expect_python_sha256")
        if args.self_test:
            need(all(getattr(args, field) is None for field in fields),
                 "self-test arguments")
            sample = {"schema": SPEC_SCHEMA, "formal_credit": 0}
            need(valid_sha(digest(sample)) and strict(canonical(sample)) == sample,
                 "runner canonical fixture")
            result = {"stage": "self_test",
                      "status": "PASS_C29_V2_TRANSACTION_RUNNER_SELF_TEST"}
        else:
            need(all(getattr(args, field) is not None for field in fields),
                 "all transaction arguments")
            result = execute(args)
        sys.stdout.buffer.write(canonical({"CM2": "NO-GO_FOR_CLAIM",
            "formal_credit": 0, "stage": result["stage"],
            "status": result["status"]}) + b"\n")
        return 0
    except (Failure, OSError, ValueError, KeyError, TypeError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
