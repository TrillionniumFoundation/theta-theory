#!/usr/bin/env python3
"""Append-only numeric-exit runner for the actual-v5 C27R2 preflight."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any


HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent
PRODUCER = HERE / "cm2_round306c27r2_source_g_fresh_actual_v5_rebuild_preflight.py"


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def fsha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_new(path: Path, payload: bytes) -> None:
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
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    run_dir = Path(args.run_dir)
    run_dir.mkdir(parents=True, exist_ok=False)
    output = run_dir / "payload/preflight.json"
    producer_before = fsha(PRODUCER)
    command = [sys.executable, str(PRODUCER), "--output", str(output)]
    completed = subprocess.run(command, cwd=WORKSPACE, capture_output=True,
                               check=False)
    producer_after = fsha(PRODUCER)
    write_new(run_dir / "stdout.log", completed.stdout)
    write_new(run_dir / "stderr.log", completed.stderr)
    result = json.loads(output.read_bytes()) if output.exists() else None
    body = {
        "schema": "cm2.round306c27r2.source-g-fresh-actual-v5-rebuild-preflight.execution.v1",
        "command": command,
        "cwd": str(WORKSPACE),
        "numeric_exit": completed.returncode,
        "signal": None if completed.returncode >= 0 else -completed.returncode,
        "stderr_empty": completed.stderr == b"",
        "stdout_sha256": hashlib.sha256(completed.stdout).hexdigest(),
        "stderr_sha256": hashlib.sha256(completed.stderr).hexdigest(),
        "producer_pre_sha256": producer_before,
        "producer_post_sha256": producer_after,
        "producer_unchanged": producer_before == producer_after,
        "preflight_present": output.exists(),
        "preflight_file_sha256": fsha(output) if output.exists() else None,
        "preflight_object_sha256": result.get("preflight_sha256") if isinstance(result, dict) else None,
        "preflight_decision": result.get("decision") if isinstance(result, dict) else None,
        "preflight_intended_process_exit_code": (
            result.get("intended_process_exit_code") if isinstance(result, dict) else None
        ),
        "truthful_reject": (
            completed.returncode == 2 and completed.stderr == b""
            and isinstance(result, dict) and result.get("decision") == "REJECT"
            and result.get("intended_process_exit_code") == 2
        ),
        "formal_credit": 0,
        "manifest_authorized": False,
    }
    body["execution_sha256"] = digest(body)
    write_new(run_dir / "execution.json", canonical(body) + b"\n")
    print(canonical({"numeric_exit": completed.returncode,
                     "truthful_reject": body["truthful_reject"],
                     "execution_sha256": body["execution_sha256"]}).decode("ascii"))
    return 0 if body["truthful_reject"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
