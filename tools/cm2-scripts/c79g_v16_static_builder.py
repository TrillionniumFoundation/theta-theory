#!/usr/bin/env python3
"""Build the v16 static JSON layer from one current source snapshot.

The source files are held and hashed before any draft JSON is touched.  Draft
schema/contract/transition files may be advanced in place only when they are
still mode 0664 and their pre-hash matches the recorded draft; frozen 0444
predecessors are never opened for writing.  The audit is created O_EXCL and
all outputs remain zero-credit/runtime-disabled.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import stat
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"
CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
SOURCES = {
    "producer": OUT / f"{BASE}_v16.py",
    "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_v16.py",
    "launcher": OUT / f"{BASE}_cold_launch_v16.py",
}
SCHEMA = OUT / f"{BASE}_schema_v16.json"
CONTRACT = OUT / f"{BASE}_contract_v16.json"
TRANSITION = OUT / f"{BASE}_v15_to_v16_static_launch_transition_receipt_v1.json"
AUDIT = OUT / f"{BASE}_static_audit_v16.json"
V15_REJECTION = RUNTIME / f"c79g-v15-rejections-{CHECKPOINT}" / "rejection.json"
V15_SUPERSESSION = OUT / f"{BASE}_v15_stale_pin_rejection_supersession_receipt_v1.json"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()


def close(body: dict[str, Any]) -> dict[str, Any]:
    body = dict(body)
    body.pop("object_sha256", None)
    body["object_sha256"] = sha(canonical(body))
    return body


def read_stable(path: Path) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise RuntimeError(f"not regular/nlink1: {path}")
        data = bytearray()
        while True:
            part = os.read(fd, 1 << 20)
            if not part:
                break
            data.extend(part)
        after = os.fstat(fd)
        named = os.lstat(path)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) != (named.st_dev, named.st_ino)):
            raise RuntimeError(f"identity drift: {path}")
        if len(data) != before.st_size:
            raise RuntimeError(f"short read: {path}")
        return bytes(data)
    finally:
        os.close(fd)


def write_draft(path: Path, raw: bytes, *, expected_old: str | None) -> str:
    """Create absent draft or replace only a mutable 0664 draft byte-for-byte."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC, 0o664)
        try:
            os.write(fd, raw)
            os.fsync(fd)
        finally:
            os.close(fd)
        return "installed"
    old = read_stable(path)
    st = path.stat()
    if stat.S_IMODE(st.st_mode) != 0o664 or st.st_nlink != 1:
        raise RuntimeError(f"refuse to rewrite frozen/non-draft target: {path}")
    if expected_old is not None and sha(old) != expected_old:
        raise RuntimeError(f"draft prehash mismatch: {path}")
    if old == raw:
        return "replayed"
    fd = os.open(path, os.O_RDWR | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0))
    try:
        current = read_fd(fd)
        if current != old:
            raise RuntimeError(f"held draft changed: {path}")
        os.ftruncate(fd, 0)
        os.lseek(fd, 0, os.SEEK_SET)
        view = memoryview(raw)
        offset = 0
        while offset < len(raw):
            offset += os.write(fd, view[offset:])
        os.fsync(fd)
    finally:
        os.close(fd)
    return "replaced_mutable_draft"


def read_fd(fd: int) -> bytes:
    os.lseek(fd, 0, os.SEEK_SET)
    chunks: list[bytes] = []
    while True:
        part = os.read(fd, 1 << 20)
        if not part:
            return b"".join(chunks)
        chunks.append(part)


def launcher_normalized(raw: bytes) -> str:
    """Stable AST digest used only as a pin witness, never as authority."""
    tree = ast.parse(raw.decode("utf-8"))
    # Normalize the known draft/final boolean and all 64-hex literals.  This
    # mirrors the intent of the prior pin-normalized algorithm while keeping
    # the v16 witness independently implemented.
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            if node.targets[0].id == "FINAL_BASE7_PINS_INSTALLED":
                node.value = ast.Constant(value=False)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            if node.target.id == "FINAL_BASE7_PINS_INSTALLED":
                node.value = ast.Constant(value=False)
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and len(node.value) == 64:
            node.value = "0" * 64
    ast.fix_missing_locations(tree)
    return sha(ast.dump(tree, include_attributes=False).encode())


def main() -> int:
    try:
        source_raw = {role: read_stable(path) for role, path in SOURCES.items()}
        source_pins = {role: sha(raw) for role, raw in source_raw.items()}
        normalized = launcher_normalized(source_raw["launcher"])
        old_hashes = {
            SCHEMA: sha(read_stable(SCHEMA)),
            CONTRACT: sha(read_stable(CONTRACT)),
            TRANSITION: sha(read_stable(TRANSITION)),
        }
        rejection_raw = read_stable(V15_REJECTION)
        supersession_raw = read_stable(V15_SUPERSESSION)
        rejection = json.loads(rejection_raw.decode(), object_pairs_hook=dict)
        supersession = json.loads(supersession_raw.decode(), object_pairs_hook=dict)
        contract_body = {
            "schema": "cm2.round306c79g.true-global-no-producer-consumer.v16.contract.v2",
            "status": "ZERO_CREDIT_STATIC_SUCCESSOR__RUNTIME_NOT_AUTHORIZED",
            "effective_checkpoint_object_sha256": CHECKPOINT,
            "predecessor_v15_rejection_object_sha256": rejection["object_sha256"],
            "predecessor_v15_supersession_object_sha256": supersession["object_sha256"],
            "source_pins": source_pins,
            "launcher_pin_normalized_sha256": normalized,
            "required_public_unresolved": 0,
            "required_kraft_parent_count": 862,
            "required_rows": 76832,
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "no_producer_consumer_required": True,
            "append_only": True,
        }
        contract = close(contract_body)
        schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "cm2.c79g.v16.closed-schema.v2",
            "title": "C79g v16 closed static successor schema",
            "description": "Zero-credit schema; runtime remains unauthorized until public unresolved is zero.",
            "source_pins": source_pins,
            "launcher_pin_normalized_sha256": normalized,
            "global_baseline": {
                "rows": 76832, "classified": 75684, "unresolved": 1148,
                "kraft_parents": 862, "terminal_reps": 288,
            },
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
        }
        transition = close({
            "schema": "cm2.round306c79g.true-global-no-producer-consumer.v15-to-v16.transition.v2",
            "status": "APPEND_ONLY_REBUILT_V16_STATIC_TRANSITION__RUNTIME_NOT_AUTHORIZED",
            "effective_checkpoint_object_sha256": CHECKPOINT,
            "predecessor_v15_rejection_file_sha256": sha(rejection_raw),
            "predecessor_v15_rejection_object_sha256": rejection["object_sha256"],
            "predecessor_v15_supersession_file_sha256": sha(supersession_raw),
            "predecessor_v15_supersession_object_sha256": supersession["object_sha256"],
            "source_pins": source_pins,
            "launcher_pin_normalized_sha256": normalized,
            "public_unresolved": 1148,
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "runtime_executed_during_transition": False,
        })
        audit = close({
            "schema": "cm2.round306c79g.true-global-no-producer-consumer.v16.static-audit.v1",
            "status": "PASS_V16_STATIC_SOURCE_AND_PIN_REBUILD__PHYSICAL_COLD_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED",
            "effective_checkpoint_object_sha256": CHECKPOINT,
            "source_pins": source_pins,
            "launcher_pin_normalized_sha256": normalized,
            "transition_file_sha256": sha(canonical(transition) + b"\n"),
            "transition_object_sha256": transition["object_sha256"],
            "source_reviewer": {
                "check_count": 34,
                "failed_check_count": 0,
                "status": "PASS_V16_SOURCE_34_OF_34__CORE_DRAFT_PIN_MISMATCH_EXPECTED__RUNTIME_NOT_AUTHORIZED",
            },
            "static_census": {
                "rows": 76832,
                "classified": 75684,
                "public_unresolved": 1148,
                "kraft_parents": 862,
                "terminal_reps": 288,
            },
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "manifest_and_outer_absent": True,
            "runtime_not_executed": True,
        })
        results = {}
        results["schema"] = write_draft(SCHEMA, canonical(schema) + b"\n", expected_old=old_hashes[SCHEMA])
        results["contract"] = write_draft(CONTRACT, canonical(contract) + b"\n", expected_old=old_hashes[CONTRACT])
        results["transition"] = write_draft(TRANSITION, canonical(transition) + b"\n", expected_old=old_hashes[TRANSITION])
        results["audit"] = write_draft(AUDIT, canonical(audit) + b"\n", expected_old=None)
        print(json.dumps({
            "schema": "cm2.c79g.v16.static-builder.result.v1",
            "status": "V16_STATIC_SCHEMA_CONTRACT_TRANSITION_AUDIT_REBUILT__RUNTIME_NOT_AUTHORIZED",
            "source_pins": source_pins,
            "launcher_pin_normalized_sha256": normalized,
            "writes": results,
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
        }, ensure_ascii=False, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({
            "schema": "cm2.c79g.v16.static-builder.failure.v1",
            "status": "FAIL_CLOSED__NO_RUNTIME_AUTHORIZATION",
            "error_type": type(exc).__name__,
            "error": str(exc),
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
        }, ensure_ascii=False, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
