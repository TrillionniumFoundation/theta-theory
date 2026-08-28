#!/usr/bin/env python3
"""One-shot, fail-closed offline rebuild of the C30a python-flint runtime.

The target and every evidence file are exclusive-created.  This program never
removes or overwrites a path.  Each subprocess receives an exact three-variable
environment and each stage records argv, environment, raw stdout/stderr,
return code, and wall/monotonic timing in canonical JSON.
"""

from __future__ import annotations

import datetime
import hashlib
import json
import os
import stat
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

SCRIPT = Path(__file__).resolve(strict=True)
DELIVERABLES = SCRIPT.parent
WORKSPACE = DELIVERABLES.parent
AUDIT = WORKSPACE / ".cm2-runtime/audit/c30a-p0-closure-verifier-20260807"
TARGET = AUDIT / "fresh-python-flint-0.9.0"
ATTESTOR = DELIVERABLES / "cm2_round306c30a_python_flint_fresh_runtime_attestor.py"
LOCK = DELIVERABLES / "cm2_round306c30a_python_flint_runtime_lock.json"
REQUIREMENTS = DELIVERABLES / "cm2_round306c30a_python_flint_requirements.lock"
WHEEL_DIR = DELIVERABLES / "cm2_round306c30a_runtime"
WHEEL = WHEEL_DIR / (
    "python_flint-0.9.0-cp310-abi3-manylinux2014_x86_64."
    "manylinux_2_17_x86_64.whl"
)
MACHINE = Path("/usr/bin/python3.12")

SCRIPT_REL = "deliverables/cm2_round306c30a_python_flint_fresh_runtime_rebuild.py"
ATTESTOR_REL = "deliverables/cm2_round306c30a_python_flint_fresh_runtime_attestor.py"
AUDIT_REL = ".cm2-runtime/audit/c30a-p0-closure-verifier-20260807"
TARGET_REL = AUDIT_REL + "/fresh-python-flint-0.9.0"

MACHINE_SHA256 = "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118"
LOCK_SHA256 = "ffe714b67a0aa05d8094033a0d9cc8e10ccafa03157951adf3d64055c98cdc79"
REQUIREMENTS_SHA256 = "cd171f53dd8a187b2ef4bd7ad0cc2adbe2082395646c0c57407f4e3514c11f5c"
WHEEL_SHA256 = "376b88cacd30612479e839ffdba887599d3f9c8c0e214852bf80bb2b194e4d76"
ENVIRONMENT = {"HOME": "/nonexistent", "LC_ALL": "C.UTF-8", "TZ": "UTC"}


class Reject(RuntimeError):
    """Fail-closed rebuild rejection."""


def require(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=True, allow_nan=False, sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read_regular(path: Path, maximum: int = 512 * 1024 * 1024) -> bytes:
    absolute = Path(os.path.abspath(os.fspath(path)))
    before = absolute.lstat()
    require(
        stat.S_ISREG(before.st_mode) and not absolute.is_symlink()
        and before.st_nlink == 1 and 0 < before.st_size <= maximum,
        "regular singleton:" + os.fspath(path),
    )
    descriptor = os.open(
        absolute,
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        opened = os.fstat(descriptor)
        require(
            (opened.st_dev, opened.st_ino, opened.st_size,
             opened.st_mtime_ns, opened.st_ctime_ns)
            == (before.st_dev, before.st_ino, before.st_size,
                before.st_mtime_ns, before.st_ctime_ns),
            "input identity:" + os.fspath(path),
        )
        chunks: list[bytes] = []
        remaining = opened.st_size
        while remaining:
            block = os.read(descriptor, min(1024 * 1024, remaining))
            require(bool(block), "short input read")
            chunks.append(block)
            remaining -= len(block)
        require(not os.read(descriptor, 1), "growing input")
        after = os.fstat(descriptor)
        require(
            (after.st_dev, after.st_ino, after.st_size,
             after.st_mtime_ns, after.st_ctime_ns)
            == (opened.st_dev, opened.st_ino, opened.st_size,
                opened.st_mtime_ns, opened.st_ctime_ns),
            "changed input:" + os.fspath(path),
        )
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def write_exclusive(path: Path, raw: bytes) -> None:
    descriptor = os.open(
        path,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL
        | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
        0o600,
    )
    complete = False
    try:
        offset = 0
        while offset < len(raw):
            written = os.write(descriptor, raw[offset:])
            require(written > 0, "short output write")
            offset += written
        os.fsync(descriptor)
        complete = True
    finally:
        os.close(descriptor)
        if not complete:
            try:
                path.unlink()
            except OSError:
                pass


def artifact(path: Path) -> dict[str, Any]:
    raw = read_regular_allow_empty(path)
    return {
        "path": path.relative_to(WORKSPACE).as_posix(),
        "sha256": sha256(raw),
        "size": len(raw),
    }


def read_regular_allow_empty(path: Path) -> bytes:
    absolute = Path(os.path.abspath(os.fspath(path)))
    before = absolute.lstat()
    require(
        stat.S_ISREG(before.st_mode) and not absolute.is_symlink()
        and before.st_nlink == 1 and 0 <= before.st_size <= 512 * 1024 * 1024,
        "artifact singleton:" + os.fspath(path),
    )
    descriptor = os.open(
        absolute,
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        opened = os.fstat(descriptor)
        require(
            (opened.st_dev, opened.st_ino, opened.st_size,
             opened.st_mtime_ns, opened.st_ctime_ns)
            == (before.st_dev, before.st_ino, before.st_size,
                before.st_mtime_ns, before.st_ctime_ns),
            "artifact identity",
        )
        chunks: list[bytes] = []
        remaining = opened.st_size
        while remaining:
            block = os.read(descriptor, min(1024 * 1024, remaining))
            require(bool(block), "short artifact read")
            chunks.append(block)
            remaining -= len(block)
        require(not os.read(descriptor, 1), "growing artifact")
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def utc_now() -> str:
    return datetime.datetime.now(datetime.UTC).isoformat(timespec="microseconds")


def run_stage(name: str, argv: list[str], stdout_name: str, stderr_name: str) -> dict[str, Any]:
    stdout_path = AUDIT / stdout_name
    stderr_path = AUDIT / stderr_name
    record_path = AUDIT / f"fresh_runtime_{name}_stage.json"
    require(
        not stdout_path.exists() and not stderr_path.exists() and not record_path.exists(),
        "stage output pre-existence:" + name,
    )
    stdout_fd = os.open(
        stdout_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_CLOEXEC", 0),
        0o600,
    )
    stderr_fd = os.open(
        stderr_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_CLOEXEC", 0),
        0o600,
    )
    started_wall = utc_now()
    started_ns = time.monotonic_ns()
    try:
        process = subprocess.run(
            argv, stdin=subprocess.DEVNULL, stdout=stdout_fd, stderr=stderr_fd,
            cwd=WORKSPACE, env=ENVIRONMENT, check=False,
        )
    finally:
        os.close(stdout_fd)
        os.close(stderr_fd)
    ended_ns = time.monotonic_ns()
    ended_wall = utc_now()
    record = {
        "schema": "cm2.round306c30a.python-flint-fresh-runtime-stage.v1",
        "stage": name,
        "argv": argv,
        "cwd": os.fspath(WORKSPACE),
        "environment": ENVIRONMENT,
        "stdin": "/dev/null",
        "started_utc": started_wall,
        "ended_utc": ended_wall,
        "elapsed_monotonic_ns": ended_ns - started_ns,
        "returncode": process.returncode,
        "stdout": artifact(stdout_path),
        "stderr": artifact(stderr_path),
    }
    write_exclusive(record_path, canonical(record) + b"\n")
    require(process.returncode == 0, "stage exit:" + name)
    return record


def strict_attestation(raw: bytes) -> dict[str, Any]:
    require(raw.endswith(b"\n") and raw.count(b"\n") == 1, "attestation one line")
    require(raw == raw.strip(b"\n") + b"\n", "attestation newline form")
    try:
        value = json.loads(raw.decode("ascii"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Reject("attestation JSON") from error
    require(type(value) is dict and value.get("verdict") == "PASS", "attestation verdict")
    require(canonical(value) + b"\n" == raw, "attestation canonical bytes")
    return value


def preflight() -> dict[str, Any]:
    require(SCRIPT == WORKSPACE / SCRIPT_REL, "rebuild canonical location")
    require(AUDIT.is_dir() and not AUDIT.is_symlink(), "audit directory")
    require(not TARGET.exists() and not TARGET.is_symlink(), "fresh target absent")
    require(
        os.environ == ENVIRONMENT
        and sys.flags.isolated == 1
        and sys.flags.ignore_environment == 1
        and sys.flags.dont_write_bytecode == 1
        and sys.flags.no_user_site == 1
        and sys.flags.safe_path is True,
        "rebuild invocation contract",
    )
    source_raw = read_regular(SCRIPT, maximum=4 * 1024 * 1024)
    attestor_raw = read_regular(ATTESTOR, maximum=4 * 1024 * 1024)
    machine_raw = read_regular(MACHINE, maximum=128 * 1024 * 1024)
    lock_raw = read_regular(LOCK, maximum=64 * 1024)
    requirements_raw = read_regular(REQUIREMENTS, maximum=64 * 1024)
    wheel_raw = read_regular(WHEEL, maximum=256 * 1024 * 1024)
    require(sha256(machine_raw) == MACHINE_SHA256, "machine interpreter pin")
    require(sha256(lock_raw) == LOCK_SHA256, "runtime lock pin")
    require(sha256(requirements_raw) == REQUIREMENTS_SHA256, "requirements pin")
    require(sha256(wheel_raw) == WHEEL_SHA256, "wheel pin")
    return {
        "rebuild": {"path": SCRIPT_REL, "sha256": sha256(source_raw)},
        "attestor": {"path": ATTESTOR_REL, "sha256": sha256(attestor_raw)},
        "machine_python": {"path": "/usr/bin/python3.12", "sha256": sha256(machine_raw)},
        "runtime_lock": {
            "path": "deliverables/cm2_round306c30a_python_flint_runtime_lock.json",
            "sha256": sha256(lock_raw),
        },
        "requirements_lock": {
            "path": "deliverables/cm2_round306c30a_python_flint_requirements.lock",
            "sha256": sha256(requirements_raw),
        },
        "sealed_wheel": {
            "path": WHEEL.relative_to(WORKSPACE).as_posix(),
            "sha256": sha256(wheel_raw), "size": len(wheel_raw),
        },
    }


def main() -> int:
    try:
        require(len(sys.argv) == 1, "no arguments accepted")
        descriptor_path = AUDIT / "fresh_runtime_rebuild_descriptor.json"
        require(not descriptor_path.exists(), "descriptor absent")
        trust = preflight()

        create_argv = [
            "/usr/bin/python3.12", "-I", "-B", "-m", "venv", "--copies",
            os.fspath(TARGET),
        ]
        create = run_stage(
            "venv_create", create_argv,
            "fresh_runtime_venv_create_stdout.log",
            "fresh_runtime_venv_create_stderr.log",
        )
        fresh_python = TARGET / "bin/python"
        require(fresh_python.is_file() and not fresh_python.is_symlink(),
                "fresh copied python")

        install_argv = [
            os.fspath(fresh_python), "-I", "-B", "-m", "pip",
            "--disable-pip-version-check", "--no-cache-dir", "install",
            "--no-index", "--no-deps", "--only-binary=:all:",
            "--require-hashes", "--find-links", os.fspath(WHEEL_DIR),
            "-r", os.fspath(REQUIREMENTS),
        ]
        install = run_stage(
            "offline_install", install_argv,
            "fresh_runtime_offline_install_stdout.log",
            "fresh_runtime_offline_install_stderr.log",
        )

        freeze_argv = [
            os.fspath(fresh_python), "-I", "-B", "-m", "pip",
            "--disable-pip-version-check", "freeze", "--all",
        ]
        freeze = run_stage(
            "freeze", freeze_argv,
            "fresh_runtime_freeze.txt", "fresh_runtime_freeze_stderr.log",
        )
        freeze_raw = read_regular(AUDIT / "fresh_runtime_freeze.txt", maximum=64 * 1024)
        require(b"python-flint==0.9.0\n" in freeze_raw, "freeze python-flint pin")

        attest_argv = [
            os.fspath(fresh_python), "-I", "-B", os.fspath(ATTESTOR),
        ]
        attest = run_stage(
            "attestation", attest_argv,
            "fresh_runtime_attestation.json", "fresh_runtime_attestation_stderr.log",
        )
        attestation_raw = read_regular(
            AUDIT / "fresh_runtime_attestation.json", maximum=64 * 1024 * 1024
        )
        attestation = strict_attestation(attestation_raw)

        descriptor: dict[str, Any] = {
            "schema": "cm2.round306c30a.python-flint-fresh-runtime-rebuild.v1",
            "verdict": "PASS",
            "offline": True,
            "target_relpath": TARGET_REL,
            "target_precondition": "ABSENT",
            "target_policy": "EXCLUSIVE_CREATE_NO_DELETE_NO_OVERWRITE",
            "orchestrator_environment": ENVIRONMENT,
            "orchestrator_flags": {
                "isolated": sys.flags.isolated,
                "ignore_environment": sys.flags.ignore_environment,
                "dont_write_bytecode": sys.flags.dont_write_bytecode,
                "no_user_site": sys.flags.no_user_site,
                "safe_path": sys.flags.safe_path,
            },
            "trust_roots": trust,
            "stages": [create, install, freeze, attest],
            "attestation": artifact(AUDIT / "fresh_runtime_attestation.json"),
            "attestation_payload_sha256": attestation["attestation_payload_sha256"],
            "freeze": artifact(AUDIT / "fresh_runtime_freeze.txt"),
        }
        descriptor["descriptor_payload_sha256"] = sha256(canonical(descriptor))
        write_exclusive(descriptor_path, canonical(descriptor) + b"\n")
        completion = {
            "schema": "cm2.round306c30a.python-flint-fresh-runtime-completion.v1",
            "status": "PASS_FRESH_OFFLINE_RUNTIME_REBUILT_AND_INDEPENDENTLY_ATTESTED",
            "target_relpath": TARGET_REL,
            "descriptor": artifact(descriptor_path),
            "attestation": artifact(AUDIT / "fresh_runtime_attestation.json"),
            "freeze": artifact(AUDIT / "fresh_runtime_freeze.txt"),
        }
        sys.stdout.buffer.write(canonical(completion) + b"\n")
        sys.stdout.buffer.flush()
    except Exception as error:
        print(
            "C30A_FRESH_RUNTIME_REBUILD_REJECT:"
            + error.__class__.__name__ + ":" + str(error),
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
