#!/usr/bin/env python3
"""Run both actual interpreter modes and record command/output identities."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def utc():
    return datetime.now(timezone.utc).isoformat()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    root = Path(__file__).resolve().parent
    out = root / "optical-verification"
    out.mkdir(parents=True, exist_ok=True)
    script = root / "check_explicit_optical.py"
    commands = []
    for mode, flags in (("normal", []), ("optimized", ["-O"])):
        details = out / (mode + ".details.json")
        command = [sys.executable, *flags, str(script), "--details", str(details)]
        started = utc()
        tic = time.monotonic()
        proc = subprocess.run(command, cwd=root, env=os.environ.copy(), capture_output=True)
        elapsed = time.monotonic() - tic
        ended = utc()
        stdout = out / (mode + ".stdout.json")
        stderr = out / (mode + ".stderr.txt")
        stdout.write_bytes(proc.stdout)
        stderr.write_bytes(proc.stderr)
        commands.append({"mode": mode, "command": command, "cwd": str(root),
                         "started_at": started, "ended_at": ended,
                         "elapsed_seconds": elapsed, "returncode": proc.returncode,
                         "stdout_file": stdout.name, "stdout_bytes": len(proc.stdout),
                         "stdout_sha256": digest(proc.stdout),
                         "stderr_file": stderr.name, "stderr_bytes": len(proc.stderr),
                         "stderr_sha256": digest(proc.stderr),
                         "details_file": details.name,
                         "details_sha256": digest(details.read_bytes()) if details.is_file() else None})
    normal = (out / "normal.stdout.json").read_bytes()
    optimized = (out / "optimized.stdout.json").read_bytes()
    same_stdout = normal == optimized
    normal_details = out / "normal.details.json"
    optimized_details = out / "optimized.details.json"
    same_details = (normal_details.is_file() and optimized_details.is_file()
                    and normal_details.read_bytes() == optimized_details.read_bytes())
    passed = all(c["returncode"] == 0 for c in commands) and same_stdout and same_details
    receipt = {"status": "passed" if passed else "failed", "commands": commands,
               "interpreter": sys.version, "checker_sha256": digest(script.read_bytes()),
               "stdout_byte_identical": same_stdout, "details_byte_identical": same_details,
               "scope": "Executed exact finite algebra checks; not a continuum-proof certificate"}
    (out / "RUN_RECEIPT.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(json.dumps(receipt, indent=2, sort_keys=True))
    if not passed:
        raise RuntimeError("Optical algebra check or optimized-mode equivalence failed")


if __name__ == "__main__":
    main()
