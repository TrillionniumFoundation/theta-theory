#!/usr/bin/env python3
"""Seal the already completed r23 read-only mutation-attack report."""
from __future__ import annotations
import hashlib, json, os, stat, sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
TAG = "v16r2r23"
INPUT = Path("/tmp/r23_attacks.json")
RECEIPT = OUT / f"{BASE}_{TAG}_mutation_attack_evidence_receipt_v1.json"


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def install(path: Path, raw: bytes) -> str:
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                     os.O_CLOEXEC, 0o444)
    except FileExistsError:
        old = path.read_bytes()
        if old != raw or stat.S_IMODE(path.stat().st_mode) != 0o444 or path.stat().st_nlink != 1:
            raise RuntimeError("append-only mismatch")
        return "replayed"
    try:
        os.write(fd, raw); os.fsync(fd); os.fchmod(fd, 0o444)
    finally:
        os.close(fd)
    dfd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try: os.fsync(dfd)
    finally: os.close(dfd)
    return "installed"


def main() -> int:
    try:
        raw = INPUT.read_bytes()
        report = json.loads(raw)
        attacks = report.get("attacks")
        if (report.get("status") != "PASS_READ_ONLY_ATTACK_HARNESS__ALL_MUTATIONS_FAIL_CLOSED__ZERO_CREDIT" or
                report.get("attack_count") != 13 or report.get("failed_closed_count") != 13 or
                not isinstance(attacks, list) or len(attacks) != 13 or
                any(item.get("status") != "FAIL_CLOSED" for item in attacks) or
                report.get("credit", {}).get("formal_global_closure_credit") != 0 or
                report.get("credit", {}).get("D02_unlock") is not False or
                any(report.get("writes", {}).get(k) is not False for k in ("deliverables", "runtime", "manifest", "outer", "credit", "pyc"))):
            raise RuntimeError("attack report did not pass strict predicates")
        baseline = report.get("baseline", {})
        if (baseline.get("overlay_rows"), baseline.get("successor_rows"), baseline.get("parent_rows")) != (1148, 76832, 862):
            raise RuntimeError("attack baseline census")
        receipt = {
            "schema": f"cm2.c79g.{TAG}.mutation-attack-evidence.v1",
            "status": "PASS_READ_ONLY_MUTATION_ATTACKS__13_OF_13_FAIL_CLOSED__ZERO_CREDIT",
            "successor_suffix": TAG,
            "attack_count": 13,
            "failed_closed_count": 13,
            "attack_name_order_sha256": report.get("attack_name_order_sha256"),
            "attack_report_sha256": sha(raw),
            "seed_invariance": report.get("seed_invariance"),
            "baseline_reconstruction": {k: baseline[k] for k in ("overlay_rows", "successor_rows", "parent_rows")},
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "runtime_authorized": False,
            "writes": {"deliverables": False, "runtime": False, "manifest": False, "outer": False, "credit": False, "pyc": False},
        }
        receipt["object_sha256"] = sha(canonical(receipt))
        blob = canonical(receipt) + b"\n"
        action = install(RECEIPT, blob)
        print(json.dumps({"status": receipt["status"], "receipt": str(RECEIPT.relative_to(ROOT)), "receipt_sha256": sha(blob), "object_sha256": receipt["object_sha256"], "action": action}, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({"status": "FAIL_CLOSED_ATTACK_EVIDENCE_SEAL", "error": f"{type(exc).__name__}: {exc}", "formal_global_closure_credit": 0, "D02_unlock": False, "runtime_authorized": False}, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
