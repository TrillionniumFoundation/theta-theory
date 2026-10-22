#!/usr/bin/env python3
"""Capture a real independent artifact-audit execution without altering its inputs."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

directory = Path(__file__).resolve().parent
if len(sys.argv) != 3 or sys.argv[1] not in {"normal", "optimized"} or not sys.argv[2].isdigit():
    raise SystemExit("usage: run_independent_check.py {normal|optimized} NUMBER")
mode, number = sys.argv[1:]
tag = "independent-check-" + number + "-" + mode
log = directory / (tag + ".stdout.log")
receipt_file = directory / (tag + ".command.json")
result = directory / (tag + ".result.json")
if any(p.exists() for p in (log, receipt_file, result)):
    raise RuntimeError("Refusing to overwrite an actual prior execution")
command = [sys.executable] + (["-O"] if mode == "optimized" else []) + [
    "-B", str(directory / "verify_ci_artifact.py"),
    "--article-root", str(directory.parent / "theta-theory-round3/papers/A2-DYN-localized-clearance-records-author-revision"),
    "--artifact-root", str(directory / "extracted"),
    "--archive", str(directory.parent / "A2_DYN_CI_39712256295.zip"),
    "--output", str(result),
]
start = datetime.now(timezone.utc).isoformat()
monotonic = time.monotonic()
with log.open("wb") as output:
    process = subprocess.run(command, cwd=directory, stdout=output, stderr=subprocess.STDOUT)
data = {
    "command": command, "cwd": str(directory), "mode": mode,
    "started_utc": start, "finished_utc": datetime.now(timezone.utc).isoformat(),
    "elapsed_seconds": time.monotonic() - monotonic, "exit_code": process.returncode,
    "log": log.name, "log_bytes": log.stat().st_size,
    "log_sha256": hashlib.sha256(log.read_bytes()).hexdigest(),
    "result": result.name,
    "result_sha256": hashlib.sha256(result.read_bytes()).hexdigest() if result.exists() else None,
    "checker_sha256": hashlib.sha256((directory / "verify_ci_artifact.py").read_bytes()).hexdigest(),
}
receipt_file.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
print(log.read_text(), end="")
print(json.dumps(data, sort_keys=True))
raise SystemExit(process.returncode)
