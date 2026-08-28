#!/usr/bin/env python3
"""Append-only r34 mutation-attack evidence sealer.

Runs the independent read-only attack harness in a no-bytecode subprocess and
installs only a closed 0444 evidence receipt.  It never runs a candidate or
touches a protocol/runtime/credit surface.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
from typing import Any

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
TAG = "v16r2r34"
HARNESS = ROOT / "scripts/c79g_v16r2_global_consumer_attack_harness.py"
RECEIPT = OUT / f"{BASE}_{TAG}_mutation_attack_evidence_receipt_v1.json"
B58 = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"


def canon(v: Any) -> bytes:
    return json.dumps(v, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def stable(path: Path) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd); named = os.lstat(path)
        if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or
                (before.st_dev, before.st_ino, before.st_size) !=
                (named.st_dev, named.st_ino, named.st_size)):
            raise RuntimeError("unstable input")
        parts = []
        while True:
            b = os.read(fd, 1 << 20)
            if not b: break
            parts.append(b)
        after = os.fstat(fd); named2 = os.lstat(path)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) != (named2.st_dev, named2.st_ino)):
            raise RuntimeError("identity drift")
        return b"".join(parts)
    finally:
        os.close(fd)


def install(path: Path, raw: bytes) -> str:
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                     os.O_CLOEXEC, 0o444)
    except FileExistsError:
        if stable(path) != raw or stat.S_IMODE(path.stat().st_mode) != 0o444 or path.stat().st_nlink != 1:
            raise RuntimeError("append-only mismatch")
        return "replayed"
    try:
        view = memoryview(raw); off = 0
        while off < len(view): off += os.write(fd, view[off:])
        os.fsync(fd); os.fchmod(fd, 0o444)
    finally:
        os.close(fd)
    dfd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try: os.fsync(dfd)
    finally: os.close(dfd)
    return "installed"


def main() -> int:
    try:
        env = dict(os.environ)
        env.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "1"})
        p = subprocess.run(["/usr/bin/python3", "-I", "-B", str(HARNESS)],
                           cwd=str(ROOT), env=env, capture_output=True,
                           check=False)
        if p.returncode != 0:
            raise RuntimeError(f"attack harness rc={p.returncode}:{p.stderr[-400:]!r}")
        value = json.loads(p.stdout)
        attacks = value.get("attacks")
        if (value.get("status") !=
                "PASS_READ_ONLY_ATTACK_HARNESS__ALL_MUTATIONS_FAIL_CLOSED__ZERO_CREDIT" or
                value.get("attack_count") != 13 or
                value.get("failed_closed_count") != 13 or
                not isinstance(attacks, list) or len(attacks) != 13 or
                any(row.get("status") != "FAIL_CLOSED" for row in attacks)):
            raise RuntimeError("attack predicates")
        baseline = value.get("baseline", {})
        if (baseline.get("overlay_rows"), baseline.get("successor_rows"),
                baseline.get("parent_rows"),
                baseline.get("public_unresolved_after_reconstruction")) != (1148, 76832, 862, 0):
            raise RuntimeError("baseline census")
        credit = value.get("credit", {})
        if credit.get("formal_global_closure_credit") != 0 or credit.get("D02_unlock") is not False or credit.get("runtime_authorized") is not False:
            raise RuntimeError("credit predicate")
        writes = value.get("writes", {})
        if any(writes.get(k) is not False for k in ("deliverables", "runtime", "manifest", "outer", "credit", "pyc")):
            raise RuntimeError("write predicate")
        receipt = {
            "schema": f"cm2.c79g.{TAG}.mutation-attack-evidence.v1",
            "status": "PASS_READ_ONLY_MUTATION_ATTACKS__13_OF_13_FAIL_CLOSED__ZERO_CREDIT",
            "successor_suffix": TAG, "attack_count": 13, "failed_closed_count": 13,
            "attack_name_order_sha256": value.get("attack_name_order_sha256"),
            "attack_report_sha256": sha(p.stdout),
            "seed_invariance": value.get("seed_invariance"),
            "baseline_reconstruction": {k: baseline.get(k) for k in ("overlay_rows", "successor_rows", "parent_rows")},
            "effective_checkpoint_object_sha256": B58,
            "formal_global_closure_credit": 0, "D02_unlock": False,
            "runtime_authorized": False,
            "writes": {"deliverables": False, "runtime": False, "manifest": False,
                        "outer": False, "credit": False, "pyc": False},
        }
        receipt["object_sha256"] = sha(canon(receipt))
        raw = canon(receipt) + b"\n"
        action = install(RECEIPT, raw)
        print(json.dumps({"status": receipt["status"], "receipt": str(RECEIPT.relative_to(ROOT)),
                          "receipt_sha256": sha(raw), "object_sha256": receipt["object_sha256"],
                          "action": action}, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({"status": "FAIL_CLOSED_ATTACK_EVIDENCE_SEAL",
                          "error": f"{type(exc).__name__}: {exc}",
                          "formal_global_closure_credit": 0, "D02_unlock": False,
                          "runtime_authorized": False}, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
