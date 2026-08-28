#!/usr/bin/env python3
"""Fail-closed process transaction runner for C27R2 authority-v2 stages.

This runner is intentionally mathematical-domain agnostic.  A gated watcher
provides a closed command specification and a closed pinset.  The runner holds
all declared inputs open with O_NOFOLLOW, records pre/post SHA/stat identity,
captures numeric exit and signal separately, requires empty stderr and a
canonical expected stdout status, snapshots declared outputs, and emits either
a zero-credit PASS attestation or an append-only failure receipt.
"""

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
SPEC_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "process-command-spec.v3"
)
PINSET_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "gated-transaction-pinset.v3"
)
ATTESTATION_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "process-run-attestation.v3"
)
FAILURE_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "process-failure-receipt.v3"
)


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def valid_sha(value: Any) -> bool:
    return (
        type(value) is str and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace(
        "+00:00", "Z"
    )


def strict_load(payload: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(key not in result, "duplicate JSON key:" + key)
            result[key] = value
        return result

    def constant(value: str) -> None:
        raise Failure("non-finite JSON:" + value)

    return json.loads(payload, object_pairs_hook=pairs, parse_constant=constant)


def inside(raw: str | Path, *, absent: bool = False) -> Path:
    supplied = Path(raw)
    path = (ROOT / supplied if not supplied.is_absolute()
            else supplied).absolute()
    try:
        relative = path.relative_to(ROOT)
    except ValueError as error:
        raise Failure("path outside workspace:" + str(raw)) from error
    need(all(part not in {"", ".", ".."} for part in relative.parts),
         "canonical workspace path:" + str(raw))
    current = ROOT
    for part in relative.parts:
        current = current / part
        if not current.exists():
            need(absent, "missing path component:" + str(current))
            break
        need(not current.is_symlink(), "symlink path component:" + str(current))
    return path


def fingerprint(info: os.stat_result) -> tuple[int, ...]:
    return (
        info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size,
        info.st_mtime_ns, info.st_ctime_ns, info.st_uid, info.st_gid,
    )


class Capture:
    def __init__(self, path: Path, label: str):
        self.path = inside(path)
        self.label = label
        self.fd = os.open(
            self.path,
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0),
        )
        self.before = os.fstat(self.fd)
        need(stat.S_ISREG(self.before.st_mode) and self.before.st_nlink == 1,
             label + ":regular-single-link")
        self.sha256 = self._hash_fd()

    def _hash_fd(self) -> str:
        os.lseek(self.fd, 0, os.SEEK_SET)
        state = hashlib.sha256()
        while block := os.read(self.fd, 4 << 20):
            state.update(block)
        os.lseek(self.fd, 0, os.SEEK_SET)
        need(fingerprint(os.fstat(self.fd)) == fingerprint(self.before),
             self.label + ":stable-fd-hash")
        return state.hexdigest()

    def bytes(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        chunks: list[bytes] = []
        while block := os.read(self.fd, 4 << 20):
            chunks.append(block)
        os.lseek(self.fd, 0, os.SEEK_SET)
        need(fingerprint(os.fstat(self.fd)) == fingerprint(self.before),
             self.label + ":stable-fd-read")
        return b"".join(chunks)

    def document(self, closure: str) -> dict[str, Any]:
        payload = self.bytes()
        need(payload.endswith(b"\n"), self.label + ":JSON-newline")
        value = strict_load(payload[:-1])
        need(type(value) is dict and canonical(value) == payload[:-1],
             self.label + ":canonical-JSON")
        body = dict(value)
        claim = body.pop(closure, None)
        need(valid_sha(claim) and claim == digest(body),
             self.label + ":object-closure")
        return value

    def attest(self) -> dict[str, Any]:
        current_fd = os.fstat(self.fd)
        need(fingerprint(current_fd) == fingerprint(self.before),
             self.label + ":fd-pre-post-stat")
        current_path = os.stat(self.path, follow_symlinks=False)
        need(fingerprint(current_path) == fingerprint(self.before),
             self.label + ":path-pre-post-identity")
        need(self._hash_fd() == self.sha256,
             self.label + ":fd-pre-post-sha")
        return {
            "path": str(self.path.relative_to(ROOT)),
            "sha256": self.sha256,
            "size": self.before.st_size,
            "stat_fingerprint": list(fingerprint(self.before)),
            "O_NOFOLLOW": True,
            "single_open_file_description_hash_child_fstat_and_path_identity":
                True,
        }

    def close(self) -> None:
        os.close(self.fd)


def external_sha(path: Path) -> str:
    descriptor = os.open(
        path,
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "external regular single-link:" + str(path))
        state = hashlib.sha256()
        while block := os.read(descriptor, 4 << 20):
            state.update(block)
        need(fingerprint(os.fstat(descriptor)) == fingerprint(before),
             "external stable hash:" + str(path))
        return state.hexdigest()
    finally:
        os.close(descriptor)


def write_once(path: Path, payload: bytes) -> None:
    descriptor = os.open(
        path,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
        0o600,
    )
    try:
        offset = 0
        while offset < len(payload):
            offset += os.write(descriptor, payload[offset:])
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def write_json(path: Path, value: Any) -> None:
    write_once(path, canonical(value) + b"\n")


def parse_stdout(payload: bytes, expected_status: str) -> dict[str, Any]:
    need(payload.endswith(b"\n"), "child stdout newline")
    value = strict_load(payload[:-1])
    need(type(value) is dict and canonical(value) == payload[:-1],
         "child stdout canonical JSON")
    need(value == {
        "CM2": "NO-GO_FOR_CLAIM",
        "formal_credit": 0,
        "status": expected_status,
    }, "child exact stdout status")
    return value


def file_snapshot(path: Path) -> dict[str, Any]:
    need(not path.is_symlink() and path.is_file(),
         "output regular no-symlink:" + str(path))
    info = path.stat()
    need(info.st_nlink == 1, "output single-link:" + str(path))
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    after = path.stat()
    need(fingerprint(after) == fingerprint(info),
         "output stable hash:" + str(path))
    return {
        "path": str(path.relative_to(ROOT)),
        "sha256": state.hexdigest(),
        "size": info.st_size,
        "stat_fingerprint": list(fingerprint(info)),
    }


def overlaps(left: Path, right: Path) -> bool:
    """Return true when either path is the other path or its descendant."""
    return left == right or left in right.parents or right in left.parents


def canonical_relative_file(value: Any) -> bool:
    if type(value) is not str or value == "":
        return False
    path = Path(value)
    return (
        not path.is_absolute()
        and all(part not in {"", ".", ".."} for part in path.parts)
        and str(path) == value
    )


def validate_output_roots_prelaunch(
    specifications: list[dict[str, Any]],
    run_dir: Path,
    protected_inputs: set[Path],
) -> list[Path]:
    """Validate declared output topology before any child process is started."""
    roots: list[Path] = []
    for ordinal, item in enumerate(specifications):
        need(type(item) is dict and set(item) == {
            "path", "kind", "precondition", "exact_inventory",
            "required_relative_files",
        }, f"output root specification:{ordinal}")
        raw = item["path"]
        kind = item["kind"]
        precondition = item["precondition"]
        exact = item["exact_inventory"]
        required = item["required_relative_files"]
        need(type(raw) is str and raw != "",
             f"output root path string:{ordinal}")
        need(kind in {"file", "directory"},
             f"output root kind:{ordinal}")
        need(precondition in {"ABSENT", "EXISTING_EMPTY_DIRECTORY"},
             f"output root precondition:{ordinal}")
        need(type(required) is list
             and required == sorted(set(required))
             and all(canonical_relative_file(value) for value in required),
             f"output required inventory:{ordinal}")
        need(exact is None or (
            type(exact) is list
            and exact == sorted(set(exact))
            and all(canonical_relative_file(value) for value in exact)
            and all(value in exact for value in required)
        ), f"output exact inventory:{ordinal}")
        if kind == "file":
            need(precondition == "ABSENT" and exact is None and required == [],
                 f"file output root contract:{ordinal}")
        else:
            need(type(exact) is list or exact is None,
                 f"directory output inventory contract:{ordinal}")
        path = inside(raw, absent=(precondition == "ABSENT"))
        need(path.parent.is_dir() and not path.parent.is_symlink(),
             f"output root existing canonical parent:{ordinal}")
        if precondition == "ABSENT":
            need(not path.exists() and not path.is_symlink(),
                 f"output root absent before child:{ordinal}")
        else:
            need(kind == "directory" and path.is_dir()
                 and not path.is_symlink()
                 and next(path.iterdir(), None) is None,
                 f"output root existing empty directory before child:{ordinal}")
        need(not overlaps(path, run_dir),
             f"output root separated from runner directory:{ordinal}")
        need(all(not overlaps(path, protected) for protected in protected_inputs),
             f"output root separated from declared inputs:{ordinal}")
        need(all(not overlaps(path, previous) for previous in roots),
             f"output roots pairwise nonoverlapping:{ordinal}")
        roots.append(path)
    return roots


def output_snapshot(specifications: list[dict[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for item in specifications:
        need(type(item) is dict and set(item) == {
            "path", "kind", "precondition", "exact_inventory",
            "required_relative_files",
        }, "output root specification")
        path = inside(item["path"])
        kind = item["kind"]
        if kind == "file":
            need(item["exact_inventory"] is None
                 and item["required_relative_files"] == [],
                 "file output root specification")
            result[item["path"]] = {
                "kind": "file", "files": [file_snapshot(path)]}
            continue
        need(kind == "directory" and path.is_dir() and not path.is_symlink(),
             "directory output root")
        files: list[Path] = []
        directories: list[Path] = []
        for current, directory_names, file_names in os.walk(path):
            current_path = Path(current)
            for name in directory_names:
                child = current_path / name
                need(not child.is_symlink(), "no output symlink directory")
                directories.append(child)
            for name in file_names:
                child = current_path / name
                need(not child.is_symlink(), "no output symlink file")
                files.append(child)
        relative_files = sorted(str(value.relative_to(path)) for value in files)
        exact = item["exact_inventory"]
        required = item["required_relative_files"]
        need(exact is None or relative_files == exact,
             "output exact inventory:" + item["path"])
        need(type(required) is list
             and all(value in relative_files for value in required),
             "output required files:" + item["path"])
        result[item["path"]] = {
            "kind": "directory",
            "directory_count": len(directories),
            "files": [file_snapshot(value) for value in sorted(files)],
            "relative_file_inventory": relative_files,
        }
    return result


def child(command: list[str], environment: dict[str, str], timeout: int) \
        -> tuple[bytes, bytes, int, int | None, bool, float]:
    started = time.monotonic()
    process = subprocess.Popen(
        command, cwd=ROOT, env=environment, stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True,
    )
    timed_out = False
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        os.killpg(process.pid, signal.SIGKILL)
        stdout, stderr = process.communicate()
    elapsed = time.monotonic() - started
    returncode = process.returncode
    need(type(returncode) is int, "child return code")
    child_signal = -returncode if returncode < 0 else None
    numeric_exit = returncode if returncode >= 0 else 128 + (-returncode)
    return stdout, stderr, numeric_exit, child_signal, timed_out, elapsed


def failure_receipt(
    run_dir: Path,
    stage: str,
    error: str,
    started_at: str,
    numeric_exit: int | None,
    child_signal: int | None,
    timed_out: bool,
    input_pre: dict[str, Any] | None,
    input_post: dict[str, Any] | None,
    outputs: dict[str, Any] | None,
) -> dict[str, Any]:
    body = {
        "schema": FAILURE_SCHEMA,
        "status": "FAILED_CLOSED_PROCESS_TRANSACTION__ZERO_CREDIT",
        "stage": stage,
        "started_at_utc": started_at,
        "failed_at_utc": utc_now(),
        "error": error,
        "numeric_exit_code": numeric_exit,
        "signal": child_signal,
        "timed_out": timed_out,
        "input_pre": input_pre,
        "input_post": input_post,
        "outputs_observed": outputs,
        "formal_credit": 0,
        "manifest_authorized": False,
        "C27R2": "UNAUTHORIZED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    result = dict(body)
    result["failure_receipt_sha256"] = digest(result)
    if not (run_dir / "failure_receipt.json").exists():
        write_json(run_dir / "failure_receipt.json", result)
    if not (run_dir / "FAILED.lock").exists():
        write_once(run_dir / "FAILED.lock",
                   b"FAILED_CLOSED_C27R2_AUTHORITY_V2_PROCESS_TRANSACTION\n")
    return result


def execute(args: argparse.Namespace) -> dict[str, Any]:
    need(valid_sha(args.expect_runner_sha256)
         and valid_sha(args.expect_python_sha256), "runner/Python pins")
    need(external_sha(SELF) == args.expect_runner_sha256,
         "runner source self pin")
    need(external_sha(PYTHON) == args.expect_python_sha256,
         "Python executable pin")
    spec_capture = Capture(inside(args.command_spec), "command-spec")
    pinset_capture = Capture(inside(args.pinset), "pinset")
    captures: list[Capture] = [spec_capture, pinset_capture]
    run_dir = inside(args.run_dir, absent=True)
    need(not run_dir.exists(), "fresh run directory")
    stage = "unparsed"
    started_at = utc_now()
    numeric_exit: int | None = None
    child_signal: int | None = None
    timed_out = False
    input_pre: dict[str, Any] | None = None
    input_post: dict[str, Any] | None = None
    outputs: dict[str, Any] | None = None
    try:
        spec = spec_capture.document("command_spec_sha256")
        pinset = pinset_capture.document("pinset_sha256")
        need(spec.get("schema") == SPEC_SCHEMA
             and pinset.get("schema") == PINSET_SCHEMA,
             "command spec/pinset schemas")
        stage = spec.get("stage")
        need(stage in {"producer", "independent_verifier", "coherent_attacks"}
             and args.stage == stage, "exact transaction stage")
        need(spec.get("pinset_file_sha256") == pinset_capture.sha256
             and spec.get("pinset_object_sha256") == pinset["pinset_sha256"],
             "command spec pins pinset")
        need(spec.get("runner_source_sha256") == args.expect_runner_sha256
             and spec.get("python_sha256") == args.expect_python_sha256,
             "command spec runner/Python pins")
        source_path = inside(spec["source_path"])
        need(external_sha(source_path) == spec["source_sha256"],
             "stage source pin")
        command = spec.get("argv")
        environment = spec.get("environment")
        timeout = spec.get("timeout_seconds")
        output_specs = spec.get("output_roots")
        need(type(command) is list and all(type(value) is str for value in command)
             and command[:4] == [str(PYTHON), "-I", "-B", str(source_path)],
             "exact isolated Python command")
        need(type(environment) is dict and environment == {
            "PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
            "PYTHONHASHSEED": spec["python_hash_seed"],
        }, "minimal exact environment")
        need(type(spec["python_hash_seed"]) is str
             and spec["python_hash_seed"].isdigit()
             and type(timeout) is int and 60 <= timeout <= 86_400,
             "hash seed/timeout contract")
        need(type(output_specs) is list and len(output_specs) > 0,
             "declared output roots")
        input_paths = spec.get("input_paths")
        need(type(input_paths) is list and input_paths == sorted(set(input_paths)),
             "sorted unique input paths")
        already = {spec_capture.path, pinset_capture.path}
        for ordinal, raw in enumerate(input_paths):
            path = inside(raw)
            need(path not in already, "unique captured input path")
            already.add(path)
            captures.append(Capture(path, f"declared-input-{ordinal:03d}"))
        protected = set(already) | {source_path, SELF}
        need(all(not overlaps(run_dir, path) for path in protected),
             "runner directory separated from declared inputs")
        validate_output_roots_prelaunch(output_specs, run_dir, protected)
        run_dir.mkdir(parents=True, mode=0o700)
        write_json(run_dir / "runner_start.json", {
            "schema": ATTESTATION_SCHEMA + ".start",
            "stage": stage,
            "started_at_utc": started_at,
            "runner_source_sha256": args.expect_runner_sha256,
            "command_spec_file_sha256": spec_capture.sha256,
            "command_spec_object_sha256": spec["command_spec_sha256"],
            "pinset_file_sha256": pinset_capture.sha256,
            "pinset_object_sha256": pinset["pinset_sha256"],
            "formal_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        })
        input_pre = {capture.label: capture.attest() for capture in captures}
        write_json(run_dir / "input_pre.json", input_pre)
        stdout, stderr, numeric_exit, child_signal, timed_out, elapsed = child(
            command, environment, timeout)
        write_once(run_dir / "stdout.log", stdout)
        write_once(run_dir / "stderr.log", stderr)
        write_once(run_dir / "exit_code.txt",
                   (str(numeric_exit) + "\n").encode("ascii"))
        write_json(run_dir / "signal.json", child_signal)
        write_json(run_dir / "timing.json", {
            "elapsed_seconds": round(elapsed, 6), "timed_out": timed_out})
        input_post = {capture.label: capture.attest() for capture in captures}
        write_json(run_dir / "input_post.json", input_post)
        need(input_pre == input_post, "all declared input pre/post SHA/stat")
        outputs = output_snapshot(output_specs)
        write_json(run_dir / "output_validation.json", outputs)
        need(not timed_out and numeric_exit == 0 and child_signal is None,
             "numeric exit0, null signal, no timeout")
        need(stderr == b"", "empty child stderr")
        stdout_value = parse_stdout(stdout, spec["expected_stdout_status"])
        body = {
            "schema": ATTESTATION_SCHEMA,
            "status": "PASS_PROCESS_TRANSACTION_EXIT0_NULL_SIGNAL_EMPTY_STDERR_PRE_POST_AND_OUTPUTS__ZERO_CREDIT",
            "stage": stage,
            "started_at_utc": started_at,
            "ended_at_utc": utc_now(),
            "elapsed_seconds": round(elapsed, 6),
            "numeric_exit_code": numeric_exit,
            "signal": child_signal,
            "timed_out": timed_out,
            "stderr_empty": True,
            "stdout": stdout_value,
            "stdout_sha256": hashlib.sha256(stdout).hexdigest(),
            "stderr_sha256": hashlib.sha256(stderr).hexdigest(),
            "input_pre_post_sha_stat_identical": True,
            "input_attestations": input_post,
            "output_validation": outputs,
            "command_spec_file_sha256": spec_capture.sha256,
            "command_spec_object_sha256": spec["command_spec_sha256"],
            "pinset_file_sha256": pinset_capture.sha256,
            "pinset_object_sha256": pinset["pinset_sha256"],
            "runner_source_sha256": args.expect_runner_sha256,
            "stage_source_sha256": spec["source_sha256"],
            "python_sha256": args.expect_python_sha256,
            "formal_credit": 0,
            "manifest_authorized": False,
            "C27R2": "UNAUTHORIZED_PENDING_RELEASE_CHAIN",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        result = dict(body)
        result["run_attestation_sha256"] = digest(result)
        write_json(run_dir / "run_attestation.json", result)
        write_once(run_dir / "PASS.lock",
                   ("PASS_C27R2_AUTHORITY_V2_" + stage.upper()
                    + "_PROCESS_TRANSACTION__ZERO_CREDIT\n").encode("ascii"))
        return result
    except BaseException as error:
        if run_dir.exists():
            failure_receipt(
                run_dir, stage, f"{type(error).__name__}:{error}", started_at,
                numeric_exit, child_signal, timed_out, input_pre, input_post,
                outputs,
            )
        raise
    finally:
        for capture in captures:
            capture.close()


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--stage", required=True,
                       choices=("producer", "independent_verifier",
                                "coherent_attacks"))
    value.add_argument("--command-spec", required=True)
    value.add_argument("--pinset", required=True)
    value.add_argument("--run-dir", required=True)
    value.add_argument("--expect-runner-sha256", required=True)
    value.add_argument("--expect-python-sha256", required=True)
    return value


def main() -> int:
    args = parser().parse_args()
    try:
        result = execute(args)
        sys.stdout.buffer.write(canonical({
            "CM2": "NO-GO_FOR_CLAIM",
            "formal_credit": 0,
            "stage": result["stage"],
            "status": result["status"],
        }) + b"\n")
        return 0
    except (Failure, OSError, ValueError, KeyError, TypeError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

