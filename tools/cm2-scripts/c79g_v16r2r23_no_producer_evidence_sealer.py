#!/usr/bin/env python3
"""Seal the r23 read-only no-producer/dual-seed evidence receipt.

The helper and reviewer are run as isolated, no-bytecode subprocesses.  The
only persistent output is one append-only 0444 receipt; no candidate/runtime
surface, manifest, outer receipt, authority head, or credit is touched.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import stat
import sys
from typing import Any

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
TAG = "v16r2r23"
PREV = "v16r2r22"
RECEIPT = OUT / f"{BASE}_{TAG}_no_producer_dual_seed_evidence_receipt_v1.json"
HELPER = ROOT / "scripts/c79g_v16r2_global_consumer_precompute.py"
REVIEWER = ROOT / "scripts/c79g_v16r2r20_independent_reviewer.py"
CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def stable(path: Path) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        named = os.lstat(path)
        if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or
                (before.st_dev, before.st_ino, before.st_size) !=
                (named.st_dev, named.st_ino, named.st_size)):
            raise RuntimeError(f"unstable input:{path}")
        chunks = []
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            chunks.append(block)
        after, named_after = os.fstat(fd), os.lstat(path)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) !=
                (named_after.st_dev, named_after.st_ino)):
            raise RuntimeError(f"identity drift:{path}")
        return b"".join(chunks)
    finally:
        os.close(fd)


def closed(value: dict[str, Any]) -> bool:
    claim = value.get("object_sha256")
    if not isinstance(claim, str):
        return False
    body = dict(value)
    body.pop("object_sha256", None)
    return sha(canonical(body)) == claim


def install(path: Path, raw: bytes) -> str:
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                     os.O_CLOEXEC, 0o444)
    except FileExistsError:
        if stable(path) != raw or stat.S_IMODE(path.stat().st_mode) != 0o444 or path.stat().st_nlink != 1:
            raise RuntimeError(f"append-only mismatch:{path}")
        return "replayed"
    try:
        view = memoryview(raw); offset = 0
        while offset < len(view):
            offset += os.write(fd, view[offset:])
        os.fsync(fd); os.fchmod(fd, 0o444)
    finally:
        os.close(fd)
    dfd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try:
        os.fsync(dfd)
    finally:
        os.close(dfd)
    return "installed"


def run_json(command: list[str], env: dict[str, str]) -> dict[str, Any]:
    proc = subprocess.run(command, cwd=str(ROOT), env=env, text=True,
                          capture_output=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"subprocess rc={proc.returncode}: {proc.stderr[-500:]}")
    try:
        value = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("subprocess did not emit one JSON object") from exc
    if not isinstance(value, dict):
        raise RuntimeError("subprocess report object required")
    return value


def main() -> int:
    try:
        env = dict(os.environ)
        env.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "1"})
        precompute = run_json([
            "/usr/bin/python3", "-I", "-B", str(HELPER)], env)
        if precompute.get("status") != "PASS_READ_ONLY_IN_MEMORY_RECONSTRUCTION__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED":
            raise RuntimeError("precompute status")
        recon = precompute.get("reconstruction", {})
        if (recon.get("overlay_rows"), recon.get("successor_rows"),
                recon.get("parent_rows"),
                recon.get("public_unresolved_after_reconstruction")) != (1148, 76832, 862, 0):
            raise RuntimeError("reconstruction counts")
        seed = precompute.get("seed_invariance", {})
        if seed.get("pass") is not True or seed.get("seeds") != [1, 99991]:
            raise RuntimeError("seed invariance")
        writes = precompute.get("writes", {})
        if any(writes.get(k) is not False for k in ("deliverables", "runtime", "manifest", "outer", "credit")):
            raise RuntimeError("precompute write claim")
        review_env = dict(env)
        review_env.update({"CM2_SUCCESSOR_SUFFIX": TAG, "CM2_PREDECESSOR_SUFFIX": PREV})
        review = run_json(["/usr/bin/python3", "-I", "-B", str(REVIEWER)], review_env)
        if (review.get("status") != "PASS_DUAL_STATIC_CANDIDATE_34_OF_34__RUNTIME_NOT_AUTHORIZED" or
                review.get("check_count") != 34 or review.get("failed_check_count") != 0 or
                review.get("read_only") is not True):
            raise RuntimeError("reviewer gate")
        hashes = {}
        for role, path in {
            "producer": OUT / f"{BASE}_{TAG}_semantic_source.py",
            "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
            "launcher": OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py",
        }.items():
            hashes[role] = sha(stable(path))
        report = {
            "schema": f"cm2.c79g.{TAG}.no-producer-dual-seed-evidence.v1",
            "status": "PASS_READ_ONLY_NO_PRODUCER_DUAL_SEED_RECONSTRUCTION__ZERO_CREDIT",
            "successor_suffix": TAG,
            "predecessor_suffix": PREV,
            "effective_checkpoint_object_sha256": CHECKPOINT,
            "reconstruction": {k: recon[k] for k in ("overlay_rows", "successor_rows", "parent_rows", "public_unresolved_after_reconstruction", "all_parent_unresolved_count_zero")},
            "canonical_line_sequence_sha256": precompute.get("canonical_line_sequence_sha256"),
            "seed_invariance": seed,
            "independent_reviewer": {"status": review["status"], "check_count": 34, "failed_check_count": 0, "object_sha256": review.get("object_sha256")},
            "source_hashes": hashes,
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "runtime_authorized": False,
            "writes": {"deliverables": False, "runtime": False, "manifest": False, "outer": False, "credit": False, "pyc": False},
        }
        report["object_sha256"] = sha(canonical(report))
        raw = canonical(report) + b"\n"
        action = install(RECEIPT, raw)
        print(json.dumps({"status": report["status"], "receipt": str(RECEIPT.relative_to(ROOT)), "receipt_sha256": sha(raw), "object_sha256": report["object_sha256"], "action": action}, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({"status": "FAIL_CLOSED_NO_PRODUCER_EVIDENCE_SEAL", "error": f"{type(exc).__name__}: {exc}", "formal_global_closure_credit": 0, "D02_unlock": False, "runtime_authorized": False}, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
