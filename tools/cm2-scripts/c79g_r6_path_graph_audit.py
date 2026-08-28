#!/usr/bin/env python3
"""Read-only audit of the r6 JSON/source active path graph.

This audit is deliberately separate from the JSON builder.  It catches the
failure mode where a fresh zero-credit JSON quartet is internally closed but
the executable source bytes still point at a predecessor quartet.  It never
imports protocol sources, writes a report, creates bytecode, or changes any
runtime state.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
R6 = {
    "schema": OUT / f"{BASE}_schema_v16r6.json",
    "contract": OUT / f"{BASE}_contract_v16r6.json",
    "transition": OUT / f"{BASE}_v16r2_to_v16r6_static_launch_transition_receipt_v1.json",
    "audit": OUT / f"{BASE}_static_audit_v16r6.json",
}
SOURCES = {
    "producer": OUT / f"{BASE}_cold_launch_v16r2r7_semantic_source.py",
    "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_v16r2r7_semantic_source.py",
    "launcher": OUT / f"{BASE}_v16r2r7_semantic_source.py",
}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()


def read_stable(path: Path) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise RuntimeError(f"not regular/nlink1: {path}")
        chunks: list[bytes] = []
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            chunks.append(block)
        after = os.fstat(fd)
        named = os.lstat(path)
        ident = lambda st: (st.st_dev, st.st_ino, st.st_size,
                            st.st_mtime_ns, st.st_ctime_ns, st.st_nlink)
        if ident(before) != ident(after) or ident(before) != ident(named):
            raise RuntimeError(f"identity drift: {path}")
        raw = b"".join(chunks)
        if len(raw) != before.st_size:
            raise RuntimeError(f"short read: {path}")
        return raw
    finally:
        os.close(fd)


def read_json(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = read_stable(path)
    value = json.loads(raw.decode("utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"JSON root is not object: {path}")
    return value, raw


def object_closed(value: dict[str, Any]) -> bool:
    claim = value.get("object_sha256")
    body = dict(value)
    body.pop("object_sha256", None)
    return isinstance(claim, str) and claim == sha(canonical(body))


def main() -> int:
    checks: list[dict[str, Any]] = []
    values: dict[str, dict[str, Any]] = {}
    raws: dict[str, bytes] = {}
    source_raw: dict[str, bytes] = {}
    errors: list[str] = []

    for role, path in SOURCES.items():
        try:
            raw = read_stable(path)
            source_raw[role] = raw
            tree = ast.parse(raw.decode("utf-8"), filename=str(path))
            compile(tree, str(path), "exec")
            st = path.stat()
            checks.append({"name": role + "_parse_compile", "passed": True,
                           "sha256": sha(raw), "mode": oct(stat.S_IMODE(st.st_mode)),
                           "nlink": st.st_nlink})
        except Exception as exc:
            errors.append(f"{role}: {type(exc).__name__}: {exc}")
            checks.append({"name": role + "_parse_compile", "passed": False})

    for role, path in R6.items():
        try:
            value, raw = read_json(path)
            values[role], raws[role] = value, raw
            closed = True if role == "schema" else object_closed(value)
            checks.append({"name": role + "_object_closure", "passed": closed,
                           "sha256": sha(raw), "object_sha256": value.get("object_sha256")})
        except Exception as exc:
            errors.append(f"{role}: {type(exc).__name__}: {exc}")
            checks.append({"name": role + "_object_closure", "passed": False})

    contract = values.get("contract", {})
    bundle = contract.get("v16r6_bundle", {})
    exact8 = bundle.get("exact8_ordered_paths", [])
    paths = {
        "predecessor": f"deliverables/{BASE}_v16r2r7_active_predecessor_supersession_receipt_v1.json",
        "schema": f"deliverables/{BASE}_schema_v16r6.json",
        "contract": f"deliverables/{BASE}_contract_v16r6.json",
        "transition": f"deliverables/{BASE}_v16r2_to_v16r6_static_launch_transition_receipt_v1.json",
        "audit": f"deliverables/{BASE}_static_audit_v16r6.json",
        "producer": f"deliverables/{BASE}_cold_launch_v16r2r7_semantic_source.py",
        "consumer": f"deliverables/{BASE}_independent_verifier_assembler_authority_consumer_v16r2r7_semantic_source.py",
        "launcher": f"deliverables/{BASE}_v16r2r7_semantic_source.py",
        "manifest": f"deliverables/{BASE}_cold_launch_manifest_v16r6.sha256",
        "outer": f"deliverables/{BASE}_cold_launch_outer_receipt_v16r6.json",
    }
    checks.append({"name": "exact8_order", "passed": exact8 == [
        paths["predecessor"], paths["schema"], paths["contract"],
        paths["producer"], paths["consumer"], paths["transition"], paths["audit"],
        paths["launcher"]] if exact8 else False, "observed": exact8})

    missing_by_role: dict[str, list[str]] = {}
    required = (paths["schema"], paths["contract"], paths["transition"],
                paths["audit"], paths["manifest"], paths["outer"],
                paths["producer"], paths["consumer"], paths["launcher"])
    for role, raw in source_raw.items():
        text = raw.decode("utf-8", "replace")
        missing = [item for item in required if item not in text]
        if missing:
            missing_by_role[role] = missing
    checks.append({"name": "source_active_path_graph", "passed": not missing_by_role,
                   "missing": missing_by_role})

    source_pins = bundle.get("source_hashes", {})
    actual_pins = {role: sha(raw) for role, raw in source_raw.items()}
    checks.append({"name": "source_hash_pins", "passed": source_pins == actual_pins,
                   "expected": source_pins, "observed": actual_pins})
    checks.append({"name": "baseline_zero_credit", "passed":
                   bundle.get("formal_global_closure_credit") == 0 and
                   bundle.get("D02_unlock") is False and
                   bundle.get("effective_checkpoint_object_sha256") is not None,
                   "formal_global_closure_credit": bundle.get("formal_global_closure_credit"),
                   "D02_unlock": bundle.get("D02_unlock"),
                   "effective_checkpoint_object_sha256": bundle.get(
                       "effective_checkpoint_object_sha256")})

    failed = [item["name"] for item in checks if not item.get("passed")]
    report = {
        "schema": "cm2.c79g.r6.path-graph-audit.v1",
        "status": "PASS_R6_ACTIVE_PATH_GRAPH" if not failed else
                  "FAIL_CLOSED_R6_ACTIVE_PATH_GRAPH_MISMATCH",
        "read_only": True,
        "checks": checks,
        "failed_checks": failed,
        "errors": errors,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "runtime_authorized": False,
        "writes": False,
    }
    report["object_sha256"] = sha(canonical(report))
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 0 if not failed and not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
