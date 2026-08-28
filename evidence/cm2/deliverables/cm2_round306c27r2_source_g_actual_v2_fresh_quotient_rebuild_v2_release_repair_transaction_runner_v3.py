#!/usr/bin/env python3
"""Append-only process transaction runner for the C27R2 release-repair chain.

The Python executable is supplied explicitly and SHA-pinned; no system-Python
path is embedded in this source.  Every declared input is held open with
O_NOFOLLOW, SHA-256 and a nine-field stat identity are compared before/after
the isolated child, and PASS is written last.  All outcomes are zero-credit.
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
BASE = "cm2.round306c27r2.source-g-authority-v2.release-repair."
SPEC_SCHEMA = BASE + "release-repair-process-command-spec.v3"
PINSET_SCHEMA = BASE + "release-repair-process-pinset.v3"
RUN_SCHEMA = BASE + "release-repair-process-run-attestation.v3"
RUN_STATUS = (
    "PASS_C27R2_RELEASE_REPAIR_PROCESS_EXIT0_NULL_SIGNAL_EMPTY_STDERR_"
    "EXACT_ENV_PRE_POST_SHA_NINE_STAT_AND_OUTPUT_INVENTORY__ZERO_CREDIT"
)
FAIL_SCHEMA = BASE + "release-repair-process-failure-receipt.v3"
PASS = b"PASS_C27R2_RELEASE_REPAIR_PROCESS_TRANSACTION__ZERO_CREDIT\n"
EMPTY_SHA = hashlib.sha256(b"").hexdigest()


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
        self.before = os.fstat(self.fd)
        need(stat.S_ISREG(self.before.st_mode) and self.before.st_nlink == 1,
             label + ": regular single-link")
        self.sha256 = self._sha()

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


def write_once(path: Path, raw: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                 | getattr(os, "O_NOFOLLOW", 0), 0o400)
    try:
        offset = 0
        while offset < len(raw):
            offset += os.write(fd, raw[offset:])
        os.fsync(fd)
    finally:
        os.close(fd)


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


def execute(args: argparse.Namespace) -> dict[str, Any]:
    need(valid_sha(args.expect_runner_sha256)
         and valid_sha(args.expect_python_sha256), "dynamic pins")
    runner = Capture(SELF, "runner")
    python = Capture(external_regular(args.python), "python")
    spec_cap = Capture(workspace_path(args.command_spec), "command spec")
    pin_cap = Capture(workspace_path(args.pinset), "pinset")
    captures = [runner, python, spec_cap, pin_cap]
    run_dir = workspace_path(args.run_dir, absent=True)
    need(not run_dir.exists() and not run_dir.is_symlink(), "fresh run dir")
    started = utc()
    stage = "unparsed"
    try:
        need(runner.sha256 == args.expect_runner_sha256
             and python.sha256 == args.expect_python_sha256,
             "runner/Python current pins")
        spec = spec_cap.document("command_spec_sha256")
        pinset = pin_cap.document("pinset_sha256")
        need(spec.get("schema") == SPEC_SCHEMA
             and pinset.get("schema") == PINSET_SCHEMA,
             "spec/pinset schemas")
        stage = spec.get("stage")
        need(type(stage) is str and stage == args.stage and stage != "",
             "exact stage")
        need(spec.get("pinset_file_sha256") == pin_cap.sha256
             and spec.get("pinset_object_sha256") == pinset["pinset_sha256"]
             and spec.get("runner_source_sha256") == runner.sha256
             and spec.get("python_sha256") == python.sha256,
             "spec dynamic source closure")
        source = workspace_path(spec["source_path"])
        source_cap = Capture(source, "stage source")
        captures.append(source_cap)
        need(source_cap.sha256 == spec.get("source_sha256"), "source pin")
        declared = spec.get("input_paths")
        need(type(declared) is list and declared == sorted(set(declared)),
             "sorted unique inputs")
        seen = {c.path for c in captures}
        for ordinal, raw in enumerate(declared):
            path = workspace_path(raw)
            need(path not in seen, "unique input")
            seen.add(path)
            captures.append(Capture(path, f"declared-{ordinal:04d}"))
        outputs = spec.get("output_roots")
        need(type(outputs) is list and outputs, "output roots")
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
        command = spec.get("argv")
        need(type(command) is list and command[:4] == [
            str(python.path), "-I", "-B", str(source)],
            "workspace-pinned Python -I -B command")
        timeout = spec.get("timeout_seconds")
        need(type(timeout) is int and 1 <= timeout <= 86_400,
             "timeout bound")
        run_dir.mkdir(parents=True, mode=0o700)
        write_json(run_dir / "runner_start.json", {
            "schema": RUN_SCHEMA + ".start", "stage": stage,
            "started_at_utc": started, "formal_credit": 0,
            "C27R2": "AUDIT_HOLD_UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM"})
        before = {c.label: c.attest() for c in captures}
        write_json(run_dir / "input_pre.json", before)
        begun = time.monotonic()
        process = subprocess.Popen(command, cwd=ROOT, env=env,
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, start_new_session=True)
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
        write_json(run_dir / "input_post.json", after)
        need(before == after, "input pre/post SHA/nine-stat")
        observed = snapshot(outputs)
        write_json(run_dir / "output_validation.json", observed)
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
            "stage_source_sha256": source_cap.sha256,
            "python_path": str(python.path), "python_sha256": python.sha256,
            "argv_prefix": command[:4], "environment": env,
            "formal_credit": 0, "manifest_authorized": False,
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
        for cap in captures:
            cap.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    for name in ("stage", "command-spec", "pinset", "run-dir", "python",
                 "expect-runner-sha256", "expect-python-sha256"):
        parser.add_argument("--" + name)
    args = parser.parse_args()
    fields = ("stage", "command_spec", "pinset", "run_dir", "python",
              "expect_runner_sha256", "expect_python_sha256")
    try:
        if args.self_test:
            need(all(getattr(args, f) is None for f in fields),
                 "self-test no dynamic arguments")
            fixture = {"schema": RUN_SCHEMA + ".self-test", "formal_credit": 0}
            need(digest(fixture) == hashlib.sha256(canonical(fixture)).hexdigest()
                 and fingerprint(os.stat(SELF, follow_symlinks=False))[3] == 1,
                 "runner fixtures")
            result = {"stage": "self_test",
                "status": "PASS_C27R2_RELEASE_REPAIR_TRANSACTION_RUNNER_V3_SELF_TEST"}
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
