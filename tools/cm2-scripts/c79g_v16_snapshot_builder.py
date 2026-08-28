#!/usr/bin/env python3
"""Append-only C79g v16 snapshot builder.

This utility is deliberately small and boring: it takes one held, read-only
snapshot of the current v15 *source bytes*, rewrites only the protocol
namespace/version labels, and installs a new v16 file set with O_EXCL.  It
never opens an existing v15 target for writing, never imports protocol code,
and runs with ``-I -B`` so the builder itself cannot create bytecode.

The builder is a staging tool, not an authority issuer.  Its output remains
zero-credit until the independent v16 reviewer and the later cold publisher
close all pins.  Existing targets are replayed byte-for-byte; a mismatch is a
hard failure rather than an overwrite.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
from pathlib import Path
from typing import Any

import sys

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"
CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"

V15 = {
    "producer": OUT / f"{BASE}_v15.py",
    "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_v15.py",
    "launcher": OUT / f"{BASE}_cold_launch_v15.py",
}
V16 = {
    "producer": OUT / f"{BASE}_v16.py",
    "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_v16.py",
    "launcher": OUT / f"{BASE}_cold_launch_v16.py",
}

V16_SCHEMA = OUT / f"{BASE}_schema_v16.json"
V16_CONTRACT = OUT / f"{BASE}_contract_v16.json"
V16_TRANSITION = OUT / f"{BASE}_v15_to_v16_static_launch_transition_receipt_v1.json"
V16_AUDIT = OUT / f"{BASE}_static_audit_v16.json"
V15_REJECTION_NS = RUNTIME / f"c79g-v15-rejections-{CHECKPOINT}"
V15_REJECTION = V15_REJECTION_NS / "rejection.json"
V15_SUPERSESSION = OUT / f"{BASE}_v15_stale_pin_rejection_supersession_receipt_v1.json"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def closed(body: dict[str, Any]) -> dict[str, Any]:
    if "object_sha256" in body:
        raise ValueError("object field must be absent before closure")
    result = dict(body)
    result["object_sha256"] = sha(canonical(body))
    return result


def read_stable(path: Path) -> bytes:
    flags = os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise RuntimeError(f"not a regular nlink1 file: {path}")
        chunks: list[bytes] = []
        while True:
            part = os.read(fd, 1 << 20)
            if not part:
                break
            chunks.append(part)
        after = os.fstat(fd)
        named = os.lstat(path)
        if (before.st_dev, before.st_ino, before.st_size) != (
            after.st_dev, after.st_ino, after.st_size):
            raise RuntimeError(f"held file changed while reading: {path}")
        if (before.st_dev, before.st_ino) != (named.st_dev, named.st_ino):
            raise RuntimeError(f"path identity changed while reading: {path}")
        raw = b"".join(chunks)
        if len(raw) != before.st_size:
            raise RuntimeError(f"short read: {path}")
        return raw
    finally:
        os.close(fd)


def install_exact(path: Path, raw: bytes, *, mode: int = 0o664) -> str:
    """Install one absent file, or replay an identical existing file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(
            path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC,
            mode,
        )
    except FileExistsError:
        existing = read_stable(path)
        if existing != raw:
            raise RuntimeError(f"append-only target mismatch: {path}")
        return "replayed"
    try:
        view = memoryview(raw)
        offset = 0
        while offset < len(raw):
            offset += os.write(fd, view[offset:])
        os.fsync(fd)
        os.fchmod(fd, mode)
    finally:
        os.close(fd)
    dir_fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try:
        os.fsync(dir_fd)
    finally:
        os.close(dir_fd)
    return "installed"


def rewrite_namespace(raw: bytes) -> bytes:
    """Deterministic label-only rewrite; no executable semantics are added."""
    text = raw.decode("utf-8")
    # Longest/specific tokens first to avoid partial substitutions.
    for old, new in (
        ("C79G_V15", "C79G_V16"),
        ("C79g v15", "C79g v16"),
        ("c79g-v15", "c79g-v16"),
        ("V15", "V16"),
        ("v15", "v16"),
    ):
        text = text.replace(old, new)
    return text.encode("utf-8")


def source_snapshot() -> dict[str, Any]:
    snapshot: dict[str, Any] = {}
    for role, path in V15.items():
        raw = read_stable(path)
        rewritten = rewrite_namespace(raw)
        target = V16[role]
        action = install_exact(target, rewritten)
        snapshot[role] = {
            "source_path": str(path.relative_to(ROOT)),
            "target_path": str(target.relative_to(ROOT)),
            "source_sha256": sha(raw),
            "target_sha256": sha(rewritten),
            "target_bytes": len(rewritten),
            "action": action,
        }
    return snapshot


def make_rejection(snapshot: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    observed_launcher = snapshot["launcher"]["source_sha256"]
    body = {
        "schema": "cm2.round306c79g.true-global-no-producer-consumer.v15-stale-pin-rejection.v1",
        "status": "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT",
        "rejection_reason": "STALE_LAUNCHER_PIN_AFTER_STATIC_REPORT",
        "effective_checkpoint_object_sha256": CHECKPOINT,
        "observed_v15_launcher_sha256": observed_launcher,
        "superseded_v15_static_audit_launcher_sha256": "c0277dbd809b1414075292fc8bb6d366076663ebfae37270fa156126320a288f",
        "observed_common_callsite_row_count": 3761,
        "superseded_common_callsite_row_count": 3758,
        "observed_common_callsite_census_sha256": "d36efa7b5777a19693f79e3b69dc7cd8f018dbc1f44c3d5337d722072e66a0ae",
        "superseded_common_callsite_census_sha256": "85900d9bb620f13aa5d929a27d8325515d84bf0cc97ec25b2545c108ace2b08f",
        "append_only": True,
        "overwrite_delete_or_reuse_allowed": False,
        "runtime_authority": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "D02_started": False,
        "D02_formal_pending_task_count": 33638,
        "public_unresolved": 1148,
        "successor_only": "v16",
    }
    rejection = closed(body)
    supersession_body = {
        "schema": "cm2.round306c79g.true-global-no-producer-consumer.v15-to-v16-rejection-supersession.v1",
        "status": "FROZEN_APPEND_ONLY_V15_STALE_PIN_REJECTION__V16_SUCCESSOR_ONLY",
        "predecessor_rejection_path": str(V15_REJECTION.relative_to(ROOT)),
        "predecessor_rejection_file_sha256": sha(canonical(rejection) + b"\n"),
        "predecessor_rejection_object_sha256": rejection["object_sha256"],
        "successor_namespace": "v16",
        "successor_runtime_authorized": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "append_only": True,
    }
    return rejection, closed(supersession_body)


def core_surfaces(snapshot: dict[str, Any], supersession: dict[str, Any]) -> dict[Path, bytes]:
    src = {
        role: values["target_sha256"] for role, values in snapshot.items()
    }
    schema = {
        "schema": "cm2.round306c79g.true-global-no-producer-consumer.v16.schema.v1",
        "status": "DRAFT_STATIC_SUCCESSOR__RUNTIME_NOT_AUTHORIZED",
        "effective_checkpoint_object_sha256": CHECKPOINT,
        "predecessor_v15_supersession_object_sha256": supersession["object_sha256"],
        "source_pins": src,
        "global_baseline": {
            "rows": 76832,
            "classified": 75684,
            "unresolved": 1148,
            "kraft_parents": 862,
            "terminal_reps": 288,
        },
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
    }
    contract = closed({
        "schema": "cm2.round306c79g.true-global-no-producer-consumer.v16.contract.v1",
        "status": "ZERO_CREDIT_STATIC_SUCCESSOR__RUNTIME_NOT_AUTHORIZED",
        "effective_checkpoint_object_sha256": CHECKPOINT,
        "source_pins": src,
        "required_public_unresolved": 0,
        "required_kraft_parent_count": 862,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "no_producer_consumer_required": True,
        "append_only": True,
    })
    transition = closed({
        "schema": "cm2.round306c79g.true-global-no-producer-consumer.v15-to-v16.transition.v1",
        "status": "APPEND_ONLY_REJECTED_V15_TO_V16_STATIC_SUCCESSOR",
        "predecessor_supersession_file_sha256": sha(canonical(supersession) + b"\n"),
        "predecessor_supersession_object_sha256": supersession["object_sha256"],
        "source_pins": src,
        "reason": "REBUILD_FROM_CURRENT_BYTES_AFTER_STALE_PIN_DRIFT",
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
    })
    return {
        V16_SCHEMA: canonical(schema) + b"\n",
        V16_CONTRACT: canonical(contract) + b"\n",
        V16_TRANSITION: canonical(transition) + b"\n",
    }


def command_snapshot() -> dict[str, Any]:
    snapshot = source_snapshot()
    rejection, supersession = make_rejection(snapshot)
    V15_REJECTION_NS.mkdir(parents=True, exist_ok=True)
    install_exact(V15_REJECTION, canonical(rejection) + b"\n", mode=0o444)
    install_exact(V15_SUPERSESSION, canonical(supersession) + b"\n", mode=0o444)
    installed: dict[str, Any] = {
        "sources": snapshot,
        "v15_rejection": {
            "path": str(V15_REJECTION.relative_to(ROOT)),
            "file_sha256": sha(canonical(rejection) + b"\n"),
            "object_sha256": rejection["object_sha256"],
        },
        "v15_supersession": {
            "path": str(V15_SUPERSESSION.relative_to(ROOT)),
            "file_sha256": sha(canonical(supersession) + b"\n"),
            "object_sha256": supersession["object_sha256"],
        },
    }
    for path, raw in core_surfaces(snapshot, supersession)[0].items() if False else []:
        del path, raw
    for path, raw in core_surfaces(snapshot, supersession).items():
        action = install_exact(path, raw)
        installed[path.name] = {"action": action, "file_sha256": sha(raw)}
    return {
        "schema": "cm2.c79g.v16.snapshot-builder.result.v1",
        "status": "V16_SOURCE_SNAPSHOT_AND_CORE_DRAFTS_INSTALLED__RUNTIME_NOT_AUTHORIZED",
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "installed": installed,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("SNAPSHOT",))
    args = parser.parse_args()
    try:
        result = command_snapshot()
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({
            "schema": "cm2.c79g.v16.snapshot-builder.failure.v1",
            "status": "FAIL_CLOSED__NO_RUNTIME_AUTHORIZATION",
            "error_type": type(exc).__name__,
            "error": str(exc),
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
        }, ensure_ascii=False, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
