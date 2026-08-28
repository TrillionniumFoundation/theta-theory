#!/usr/bin/env python3
"""Append-only execution wrapper for the truthful-REJECT preflight."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
from typing import Any


WORKSPACE = Path(__file__).resolve().parent.parent


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


def write_new(path: Path, payload: bytes) -> None:
    path = path.resolve()
    need(path.is_relative_to(WORKSPACE), "output:workspace")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                 | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        os.write(fd, payload)
        os.fsync(fd)
    finally:
        os.close(fd)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--producer", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    try:
        producer = Path(args.producer).resolve()
        out = Path(args.output_dir).resolve()
        need(producer.is_relative_to(WORKSPACE) and producer.is_file(), "producer")
        need(out.is_relative_to(WORKSPACE) and not out.exists(), "output-dir:fresh")
        out.mkdir(parents=True, mode=0o700)
        receipt = out / "preflight.json"
        proc = subprocess.run([
            os.fspath(Path(os.sys.executable)), os.fspath(producer),
            "--output", os.fspath(receipt),
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        write_new(out / "stdout.log", proc.stdout)
        write_new(out / "stderr.log", proc.stderr)
        need(proc.returncode == 2 and proc.stdout == b"" and proc.stderr == b""
             and receipt.is_file(), "truthful-reject-execution")
        body = {
            "schema": "cm2.round306c27r2-c28-c29.post-actual-v5-rebuild-preflight-execution.v2",
            "status": "PASS_OBSERVED_NUMERIC_EXIT_2_SIGNAL_NULL_STDOUT_STDERR_EMPTY__TRUTHFUL_REJECT",
            "command": [os.fspath(Path(os.sys.executable)), os.fspath(producer),
                        "--output", os.fspath(receipt)],
            "numeric_exit_code": proc.returncode, "signal": None,
            "stdout_empty": proc.stdout == b"", "stderr_empty": proc.stderr == b"",
            "stdout_sha256": hashlib.sha256(proc.stdout).hexdigest(),
            "stderr_sha256": hashlib.sha256(proc.stderr).hexdigest(),
            "preflight_file_sha256": hashlib.sha256(receipt.read_bytes()).hexdigest(),
            "producer_source_sha256": hashlib.sha256(producer.read_bytes()).hexdigest(),
            "formal_credit": 0, "manifest_authorized": False,
            "C27R2_C28_C29": "UNAUTHORIZED", "Source_W_formal_remainder": 80,
            "CM2": "NO-GO_FOR_CLAIM",
        }
        body["execution_sha256"] = digest(body)
        write_new(out / "execution.json", canonical(body) + b"\n")
        return 0
    except (Failure, OSError) as exc:
        print("REJECT:" + str(exc))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
