#!/usr/bin/env python3
"""Read-only preflight for the successor v16r2 semantic clean-room.

It proves that the full-shape v15 inputs and the frozen v16 rejection chain
are available and unchanged.  It does not generate protocol bytes, execute a
consumer, or create a manifest/outer/runtime surface.
"""

from __future__ import annotations

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
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
V15 = {
    "schema": OUT / f"{BASE}_schema_v15.json",
    "contract": OUT / f"{BASE}_contract_v15.json",
    "transition": OUT / f"{BASE}_v14_to_v15_static_launch_transition_receipt_v1.json",
    "audit": OUT / f"{BASE}_static_audit_v15.json",
    "producer": OUT / f"{BASE}_v15.py",
    "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_v15.py",
    "launcher": OUT / f"{BASE}_cold_launch_v15.py",
}
V15_EXPECTED_SHA = {
    "schema": "ab120abd2d77667388c94e5af00637f843e7af1b48adba95306e1a7ea79e73bd",
    "contract": "292ad598033ff2f89c1d6c502e4e6077df9559688a5885088ad107fa45a7dabf",
    "transition": "74c82c804993a6b00196ba5c0b78a3c5067d3242452d61044229f3f04eaf4a7a",
    "audit": "69557bc7971a6c9943a5d4cee36895bc47413d9b45d92c56597d5cde83b3ed06",
    "producer": "7b3621bf6579cd9cc9289ed2bda353cbe5f2e32b108ec718bf80a4fd19af125b",
    "consumer": "5f988490d014a1427a773b7c5fda03318ec67ad9716a4a75b4008b007e944541",
    "launcher": "1ded892a514f21cb534d25a4ecf6cc0b82b97775371f7666d5d24f359d21e015",
}
V16_REJECTION = RUNTIME / (
    "c79g-v16-rejections-dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"
) / "rejection.json"
V16_SUPERSESSION = OUT / (
    f"{BASE}_v16_semantic_rejection_supersession_receipt_v1.json")
V16R2_PREFIX = f"{BASE}_v16r2"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read(path: Path) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise RuntimeError(f"not regular/nlink1: {path}")
        data = bytearray()
        while True:
            chunk = os.read(fd, 1 << 20)
            if not chunk:
                break
            data.extend(chunk)
        after = os.fstat(fd)
        named = os.lstat(path)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) != (named.st_dev, named.st_ino)):
            raise RuntimeError(f"identity drift: {path}")
        return bytes(data)
    finally:
        os.close(fd)


def main() -> int:
    try:
        checks: list[dict[str, Any]] = []

        def add(name: str, passed: bool, detail: Any = None) -> None:
            row: dict[str, Any] = {"name": name, "passed": bool(passed)}
            if detail is not None:
                row["detail"] = detail
            checks.append(row)

        raws = {role: read(path) for role, path in V15.items()}
        actual = {role: sha(raw) for role, raw in raws.items()}
        add("v15_held_input_hashes_exact", actual == V15_EXPECTED_SHA,
            {"actual": actual, "expected": V15_EXPECTED_SHA})
        add("v15_inputs_regular_nlink1", all(
            stat.S_ISREG(path.stat().st_mode) and path.stat().st_nlink == 1
            for path in V15.values()))

        values: dict[str, dict[str, Any]] = {}
        for role in ("schema", "contract", "transition", "audit"):
            values[role] = json.loads(raws[role].decode("utf-8"))
        schema = values["schema"]
        add("full_schema_root_ref", schema.get("$ref") ==
            "#/$defs/coldLaunchedCommittedAuthority")
        add("full_schema_defs_46", len(schema.get("$defs", {})) == 46,
            len(schema.get("$defs", {})))
        add("contract_key_shape_30", len(values["contract"]) == 30,
            len(values["contract"]))
        add("transition_key_shape_31", len(values["transition"]) == 31,
            len(values["transition"]))
        add("audit_key_shape_30", len(values["audit"]) == 30,
            len(values["audit"]))
        add("v16_rejection_frozen", V16_REJECTION.is_file() and
            stat.S_IMODE(V16_REJECTION.stat().st_mode) == 0o444 and
            V16_REJECTION.stat().st_nlink == 1)
        add("v16_supersession_frozen", V16_SUPERSESSION.is_file() and
            stat.S_IMODE(V16_SUPERSESSION.stat().st_mode) == 0o444 and
            V16_SUPERSESSION.stat().st_nlink == 1)
        add("v16_rejection_zero_credit", json.loads(read(V16_REJECTION)).get(
            "formal_global_closure_credit") == 0 and
            json.loads(read(V16_REJECTION)).get("D02_unlock") is False)
        add("v16r2_namespace_absent", not any(
            path.name.startswith(V16R2_PREFIX) for path in OUT.iterdir()))
        add("v16r2_manifest_outer_absent", not any(
            token in path.name for path in OUT.iterdir()
            for token in ("cold_launch_manifest_v16r2", "cold_launch_outer_receipt_v16r2")))
        add("no_v16r2_pyc", not any("v16r2" in str(path) and
            path.suffix == ".pyc" for path in ROOT.rglob("*.pyc")))

        failed = [row["name"] for row in checks if not row["passed"]]
        report = {
            "schema": "cm2.c79g.v16r2.regeneration-preflight.v1",
            "status": "READY_FOR_SEMANTIC_REGENERATION" if not failed else
            "FAIL_CLOSED_V16R2_PREFLIGHT",
            "check_count": len(checks),
            "failed_check_count": len(failed),
            "failed_checks": failed,
            "checks": checks,
            "input_source": "v15_full_shape_bytes_plus_frozen_v16_semantic_rejection",
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "runtime_authorized": False,
        }
        print(json.dumps(report, ensure_ascii=False, sort_keys=True))
        return 0 if not failed else 1
    except Exception as exc:
        print(json.dumps({"schema": "cm2.c79g.v16r2.regeneration-preflight.failure.v1",
                          "status": "FAIL_CLOSED_V16R2_PREFLIGHT",
                          "error_type": type(exc).__name__, "error": str(exc),
                          "formal_global_closure_credit": 0,
                          "D02_unlock": False}, ensure_ascii=False, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
