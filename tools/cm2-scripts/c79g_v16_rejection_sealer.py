#!/usr/bin/env python3
"""Seal a fail-closed v16 semantic rejection and its supersession receipt.

This tool is deliberately an O_EXCL-only evidence writer.  It never imports
or executes a protocol source, never creates a manifest/outer/runtime surface,
and never writes a credit-bearing value.  It is used only after the independent
34-check reviewer has returned a non-zero result.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
REVIEWER = ROOT / "scripts/c79g_v16_independent_reviewer.py"
SOURCES = {
    "producer": OUT / f"{BASE}_v16.py",
    "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_v16.py",
    "launcher": OUT / f"{BASE}_cold_launch_v16.py",
}
PREDECESSOR = OUT / f"{BASE}_v15_stale_pin_rejection_supersession_receipt_v1.json"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def close(body: dict[str, Any]) -> dict[str, Any]:
    value = dict(body)
    value.pop("object_sha256", None)
    value["object_sha256"] = sha(canonical(value))
    return value


def read_stable(path: Path) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise RuntimeError(f"not regular/nlink1: {path}")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(fd, 1 << 20)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(fd)
        named = os.lstat(path)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) != (named.st_dev, named.st_ino)):
            raise RuntimeError(f"identity drift: {path}")
        raw = b"".join(chunks)
        if len(raw) != before.st_size:
            raise RuntimeError(f"short read: {path}")
        return raw
    finally:
        os.close(fd)


def install_new(path: Path, raw: bytes, mode: int = 0o444) -> None:
    path.parent.mkdir(mode=0o755, parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                 os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0), mode)
    try:
        view = memoryview(raw)
        offset = 0
        while offset < len(view):
            offset += os.write(fd, view[offset:])
        os.fsync(fd)
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise RuntimeError(f"bad installed identity: {path}")
    finally:
        os.close(fd)
    os.chmod(path, mode, follow_symlinks=False)
    directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY |
                        os.O_CLOEXEC)
    try:
        os.fsync(directory)
    finally:
        os.close(directory)


def main() -> int:
    if len(sys.argv) != 1:
        print("arguments are forbidden", file=sys.stderr)
        return 2
    try:
        proc = subprocess.run(
            ["/usr/bin/python3", "-I", "-B", str(REVIEWER)],
            cwd=str(ROOT), check=False, capture_output=True, text=True,
            env={"PATH": "/usr/bin:/bin", "PYTHONDONTWRITEBYTECODE": "1"},
        )
        if proc.returncode == 0:
            raise RuntimeError("refuse to seal rejection when reviewer passed")
        report = json.loads(proc.stdout)
        if not isinstance(report, dict) or report.get("formal_global_closure_credit") != 0 or report.get("D02_unlock") is not False:
            raise RuntimeError("review report is not zero-credit fail-closed")
        source_raw = {role: read_stable(path) for role, path in SOURCES.items()}
        source_hashes = {role: sha(raw) for role, raw in source_raw.items()}
        report_raw = canonical(report)
        # Derive a fresh namespace from the held source/reviewer evidence.  A
        # later run cannot accidentally reuse this rejection directory.
        seed = canonical({"source_hashes": source_hashes,
                          "review_object_sha256": report.get("object_sha256"),
                          "ci_exit": proc.returncode,
                          "kind": "v16-semantic-rejection"})
        checkpoint = sha(seed)
        namespace = RUNTIME / f"c79g-v16-rejections-{checkpoint}"
        rejection_path = namespace / "rejection.json"
        predecessor_raw = read_stable(PREDECESSOR)
        predecessor = json.loads(predecessor_raw.decode("utf-8"))
        rejection = close({
            "schema": "cm2.round306c79g.true-global-no-producer-consumer.v16-semantic-rejection.v1",
            "status": "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT",
            "effective_checkpoint_object_sha256": checkpoint,
            "rejection_reason": "V16_SEMANTIC_SOURCE_AND_CLOSED_SHAPE_MISMATCH",
            "source_hashes": source_hashes,
            "independent_reviewer_status": report.get("status"),
            "independent_reviewer_check_count": report.get("check_count"),
            "independent_reviewer_failed_check_count": report.get("failed_check_count"),
            "independent_reviewer_failed_checks": report.get("failed_checks"),
            "independent_reviewer_object_sha256": report.get("object_sha256"),
            "semantic_defects": report.get("semantic_audit", {}).get("defects", []),
            "reviewer_ci_exit_code": proc.returncode,
            "public_unresolved": 1148,
            "required_rows": 76832,
            "required_kraft_parent_count": 862,
            "D02_formal_pending_task_count": 33638,
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "D02_started": False,
            "runtime_authority": False,
            "overwrite_delete_or_reuse_allowed": False,
            "successor_only": "v16r2-semantic-regeneration",
        })
        rejection_raw = canonical(rejection) + b"\n"
        install_new(rejection_path, rejection_raw)
        supersession_path = OUT / (
            f"{BASE}_v16_semantic_rejection_supersession_receipt_v1.json")
        supersession = close({
            "schema": "cm2.round306c79g.true-global-no-producer-consumer.v16-semantic-rejection-supersession.v1",
            "status": "FROZEN_APPEND_ONLY_V16_SEMANTIC_REJECTION__V16R2_SUCCESSOR_ONLY",
            "append_only": True,
            "predecessor_v15_supersession_file_sha256": sha(predecessor_raw),
            "predecessor_v15_supersession_object_sha256": predecessor.get("object_sha256"),
            "rejection_path": str(rejection_path.relative_to(ROOT)),
            "rejection_file_sha256": sha(rejection_raw),
            "rejection_object_sha256": rejection["object_sha256"],
            "successor_namespace": "v16r2-semantic-regeneration",
            "successor_runtime_authorized": False,
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
        })
        supersession_raw = canonical(supersession) + b"\n"
        install_new(supersession_path, supersession_raw)
        print(json.dumps({
            "schema": "cm2.c79g.v16.rejection-sealer.result.v1",
            "status": "FROZEN_FAIL_CLOSED_V16_REJECTION__NO_RUNTIME_AUTHORITY",
            "checkpoint": checkpoint,
            "rejection_path": str(rejection_path.relative_to(ROOT)),
            "rejection_file_sha256": sha(rejection_raw),
            "rejection_object_sha256": rejection["object_sha256"],
            "supersession_path": str(supersession_path.relative_to(ROOT)),
            "supersession_file_sha256": sha(supersession_raw),
            "supersession_object_sha256": supersession["object_sha256"],
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
        }, ensure_ascii=False, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({"status": "FAIL_CLOSED_REJECTION_SEALER_FAILURE",
                          "error_type": type(exc).__name__,
                          "error": str(exc),
                          "formal_global_closure_credit": 0,
                          "D02_unlock": False}, ensure_ascii=False,
                         sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
