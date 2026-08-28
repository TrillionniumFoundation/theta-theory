#!/usr/bin/env python3
"""Wait for the current C30c run, then execute only its receipt validator."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import time

WORKSPACE = Path(__file__).resolve().parent.parent
RUN = WORKSPACE / ".cm2-runtime/audit/c30c-v5-toctou-robustness-rerun-20260807T1012-final"
PYTHON = WORKSPACE / ".cm2-runtime/python-flint-0.9.0/bin/python"
VALIDATOR = WORKSPACE / "deliverables/cm2_round306c30c_62_attack_run_receipt_validator.py"
RECEIPT = WORKSPACE / ".cm2-runtime/audit/c30c-v5-toctou-robustness-rerun-20260807T1012-final-receipt-validation.json"

def exclusive(path: Path, payload: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC, 0o400)
    try:
        os.write(fd, payload)
        os.fsync(fd)
    finally:
        os.close(fd)

def main() -> int:
    if RECEIPT.exists():
        return 0
    while not (RUN / "exit_code.txt").is_file():
        time.sleep(60)
    # The wrapper writes exit/end/post files after the timed child.  Wait for
    # the validator's exact completed file set rather than racing the wrapper.
    required = {"end_utc.txt", "post.sha256", "post.stat", "time.txt"}
    while not all((RUN / name).is_file() for name in required):
        time.sleep(5)
    completed = subprocess.run(
        [str(PYTHON), "-I", "-B", str(VALIDATOR), str(RUN)],
        cwd=WORKSPACE, env={"HOME": "/nonexistent", "LC_ALL": "C.UTF-8", "TZ": "UTC"},
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if completed.returncode == 0:
        try:
            parsed = json.loads(completed.stdout)
        except json.JSONDecodeError:
            parsed = {"status": "REJECT_VALIDATOR_NON_JSON_STDOUT"}
        receipt = {
            "watch_status": "VALIDATOR_COMPLETED",
            "validator_exit_code": completed.returncode,
            "validator_result": parsed,
            "validator_stderr": completed.stderr.decode("utf-8", "replace"),
        }
    else:
        receipt = {
            "watch_status": "VALIDATOR_REJECTED",
            "validator_exit_code": completed.returncode,
            "validator_stdout": completed.stdout.decode("utf-8", "replace"),
            "validator_stderr": completed.stderr.decode("utf-8", "replace"),
        }
    exclusive(RECEIPT, json.dumps(receipt, sort_keys=True, separators=(",", ":")).encode("ascii"))
    return 0 if completed.returncode == 0 else 2

if __name__ == "__main__":
    raise SystemExit(main())
