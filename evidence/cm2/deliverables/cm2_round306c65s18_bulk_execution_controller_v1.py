#!/usr/bin/env python3
"""Fail-closed two-worker launcher for C65s18 v3 shards 2..63.

The controller never removes or replaces artifacts.  It launches at most two
exact frozen executor commands and admits a replacement worker only after the
completed shard passes the independent read-only first-layer checker.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from typing import Any


OUT = Path(__file__).resolve().parent
ROOT = OUT.parent
PYTHON = ROOT / ".venv-neurips/bin/python"
EXECUTOR = OUT / "cm2_round306c65s18_depth18_64shard_executor_v3.py"
CHECKER = OUT / "cm2_round306c65s18_bulk_shard_readonly_checker_v1.py"
EXECUTOR_SHA = "170df261ed9451fc3ecc1fca5e686c6f6d8eeb3d643126da09f30c634cda22ef"
BASE = "cm2_round306c65s18_depth18_64shard"


def file_sha(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def paths(shard: int) -> tuple[Path, Path]:
    return (OUT / f"{BASE}_shard_{shard:02d}_leaf_ledger_v3.jsonl.gz",
            OUT / f"{BASE}_shard_{shard:02d}_receipt_v3.json")


def emit(value: dict[str, Any]) -> None:
    print(json.dumps(value, sort_keys=True, separators=(",", ":")), flush=True)


def stop_all(active: dict[int, subprocess.Popen[str]]) -> None:
    for process in active.values():
        if process.poll() is None:
            process.terminate()
    deadline = time.monotonic() + 10
    while any(process.poll() is None for process in active.values()) and time.monotonic() < deadline:
        time.sleep(0.1)
    for process in active.values():
        if process.poll() is None:
            process.kill()
    for process in active.values():
        try:
            process.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--first", type=int, default=2)
    parser.add_argument("--last", type=int, default=63)
    parser.add_argument("--workers", type=int, default=2)
    args = parser.parse_args()
    if not (0 <= args.first <= args.last < 64 and args.workers in (1, 2)):
        emit({"status": "FAIL_CLOSED", "reason": "range/workers"})
        return 1
    if file_sha(EXECUTOR) != EXECUTOR_SHA:
        emit({"status": "FAIL_CLOSED", "reason": "executor SHA"})
        return 1
    for shard in range(args.first, args.last + 1):
        ledger, receipt = paths(shard)
        if ledger.exists() or receipt.exists():
            emit({"status": "FAIL_CLOSED", "reason": "preexisting output",
                  "shard_id": shard, "ledger_exists": ledger.exists(),
                  "receipt_exists": receipt.exists()})
            return 1

    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    pending = list(range(args.first, args.last + 1))
    active: dict[int, subprocess.Popen[str]] = {}
    started_at: dict[int, float] = {}
    completed = 0
    try:
        while pending or active:
            while pending and len(active) < args.workers:
                if file_sha(EXECUTOR) != EXECUTOR_SHA:
                    raise RuntimeError("executor SHA changed")
                shard = pending.pop(0)
                command = [str(PYTHON), "-B", str(EXECUTOR), "--shard", str(shard)]
                active[shard] = subprocess.Popen(
                    command, cwd=ROOT, env=env, text=True,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                started_at[shard] = time.monotonic()
                emit({"status": "STARTED", "shard_id": shard,
                      "active_shards": sorted(active),
                      "command": ".venv-neurips/bin/python -B " +
                      "deliverables/cm2_round306c65s18_depth18_64shard_executor_v3.py --shard " +
                      str(shard)})
            finished = [shard for shard, process in active.items()
                        if process.poll() is not None]
            if not finished:
                time.sleep(1)
                continue
            for shard in sorted(finished):
                process = active.pop(shard)
                stdout, stderr = process.communicate()
                elapsed = time.monotonic() - started_at.pop(shard)
                if process.returncode != 0:
                    raise RuntimeError(
                        f"shard {shard} executor rc={process.returncode} stdout={stdout!r} stderr={stderr!r}")
                try:
                    producer_result = json.loads(stdout)
                except json.JSONDecodeError as error:
                    raise RuntimeError(f"shard {shard} non-JSON stdout:{error}") from error
                if (producer_result.get("status") !=
                        "PASS_COMPLETE_NO_REPLACE_DEPTH18_SHARD__ZERO_CREDIT"):
                    raise RuntimeError(f"shard {shard} producer status:{producer_result}")
                checked = subprocess.run(
                    [str(PYTHON), "-B", str(CHECKER), "--shard", str(shard)],
                    cwd=ROOT, env=env, text=True, capture_output=True)
                if checked.returncode != 0:
                    raise RuntimeError(
                        f"shard {shard} checker rc={checked.returncode} "
                        f"stdout={checked.stdout!r} stderr={checked.stderr!r}")
                try:
                    verification = json.loads(checked.stdout)
                except json.JSONDecodeError as error:
                    raise RuntimeError(f"shard {shard} checker non-JSON:{error}") from error
                if verification.get("status") != "PASS_READ_ONLY_FIRST_LAYER_ZERO_CREDIT":
                    raise RuntimeError(f"shard {shard} checker status:{verification}")
                completed += 1
                emit({"status": "SHARD_AND_FIRST_LAYER_CHECK_PASS",
                      "shard_id": shard, "elapsed_seconds": round(elapsed, 3),
                      "completed_in_this_run": completed,
                      "remaining_not_started": len(pending),
                      "producer_object_sha256": producer_result.get("object_sha256"),
                      "verification": verification})
    except (OSError, RuntimeError) as error:
        stop_all(active)
        emit({"status": "FAIL_CLOSED_STOPPED_ALL", "reason": str(error),
              "completed_in_this_run": completed,
              "active_at_failure": sorted(active),
              "remaining_not_started": pending})
        return 1
    emit({"status": "PASS_ALL_REQUESTED_SHARDS_AND_FIRST_LAYER_CHECKS_ZERO_CREDIT",
          "first": args.first, "last": args.last, "completed": completed})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
