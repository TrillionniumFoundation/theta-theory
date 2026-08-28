#!/usr/bin/env python3
"""r41 mutation-attack evidence (read-only unless ``--seal``/``--install``).

The attack harness only reconstructs frozen upstream data in memory.  This
wrapper binds its receipt to the r41 exact8 namespace, runs two hash-seed
replays in ``-I -B`` subprocesses, and refuses every r34/r39 target.  Its only
possible write is the explicitly requested 0444 append-only side receipt.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
from typing import Any

sys.dont_write_bytecode = True
os.environ.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"})

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
TAG = "v16r2r41"
PREV = "v16r2r40"
CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
HARNESS = ROOT / "scripts/c79g_v16r2_global_consumer_attack_harness.py"
RECEIPT = OUT / f"{BASE}_{TAG}_mutation_attack_evidence_receipt_v1.json"
MANIFEST = OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256"
OUTER = OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json"
EXACT8 = (
    OUT / f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json",
    OUT / f"{BASE}_schema_{TAG}.json",
    OUT / f"{BASE}_contract_{TAG}.json",
    OUT / f"{BASE}_{TAG}_semantic_source.py",
    OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
    OUT / f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
    OUT / f"{BASE}_static_audit_{TAG}.json",
    OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py",
)


def canon(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
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
            raise RuntimeError(f"unstable:{path}")
        chunks: list[bytes] = []
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            chunks.append(block)
        after = os.fstat(fd); named_after = os.lstat(path)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) !=
                (named_after.st_dev, named_after.st_ino)):
            raise RuntimeError(f"identity drift:{path}")
        return b"".join(chunks)
    finally:
        os.close(fd)


def install(path: Path, raw: bytes) -> str:
    if path != RECEIPT:
        raise RuntimeError("receipt target mismatch")
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                     os.O_CLOEXEC, 0o444)
    except FileExistsError:
        if (stable(path) != raw or path.stat().st_nlink != 1 or
                stat.S_IMODE(path.stat().st_mode) != 0o444):
            raise RuntimeError("append-only mismatch")
        return "replayed"
    try:
        view = memoryview(raw); offset = 0
        while offset < len(view):
            written = os.write(fd, view[offset:])
            if written <= 0:
                raise RuntimeError("short receipt write")
            offset += written
        os.fsync(fd); os.fchmod(fd, 0o444)
    finally:
        os.close(fd)
    dfd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try:
        os.fsync(dfd)
    finally:
        os.close(dfd)
    return "installed"


def assert_inputs() -> dict[str, str]:
    if any("v16r2r34" in str(p) or "v16r2r39" in str(p) for p in EXACT8):
        raise RuntimeError("historical path rebound")
    hashes: dict[str, str] = {}
    for path in EXACT8:
        raw = stable(path)
        if path.stat().st_nlink != 1 or stat.S_IMODE(path.stat().st_mode) not in (0o444, 0o664):
            raise RuntimeError(f"bad exact8 identity/mode:{path}")
        hashes[str(path.relative_to(ROOT))] = sha(raw)
    if not HARNESS.is_file() or MANIFEST.exists() or OUTER.exists():
        raise RuntimeError("harness/cold-surface predicate")
    return hashes


def run_attack(seed: str) -> tuple[dict[str, Any], bytes]:
    env = dict(os.environ)
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1",
                "PYTHONHASHSEED": seed})
    proc = subprocess.run(["/usr/bin/python3", "-I", "-B", str(HARNESS)],
                          cwd=str(ROOT), env=env, text=True,
                          capture_output=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"attack harness rc={proc.returncode}:{proc.stderr[-600:]}")
    value = json.loads(proc.stdout)
    if not isinstance(value, dict):
        raise RuntimeError("attack report object required")
    if (value.get("status") !=
            "PASS_READ_ONLY_ATTACK_HARNESS__ALL_MUTATIONS_FAIL_CLOSED__ZERO_CREDIT" or
            value.get("attack_count") != 13 or
            value.get("failed_closed_count") != 13 or
            not isinstance(value.get("attacks"), list) or
            len(value["attacks"]) != 13 or
            any(row.get("status") != "FAIL_CLOSED" for row in value["attacks"])):
        raise RuntimeError("13/13 fail-closed predicate")
    baseline = value.get("baseline", {})
    if tuple(baseline.get(k) for k in ("overlay_rows", "successor_rows",
                                       "parent_rows",
                                       "public_unresolved_after_reconstruction")) != \
            (1148, 76832, 862, 0):
        raise RuntimeError("attack baseline census")
    credit = value.get("credit", {})
    if credit.get("formal_global_closure_credit") != 0 or \
            credit.get("D02_unlock") is not False or \
            credit.get("runtime_authorized") is not False:
        raise RuntimeError("attack credit predicate")
    writes = value.get("writes", {})
    if any(writes.get(k) is not False for k in
           ("deliverables", "runtime", "manifest", "outer", "credit", "pyc")):
        raise RuntimeError("attack write predicate")
    return value, proc.stdout.encode()


def preflight() -> tuple[dict[str, Any], bytes]:
    hashes_before = assert_inputs()
    reports: dict[str, dict[str, Any]] = {}
    raw_reports: dict[str, bytes] = {}
    for seed in ("1", "99991"):
        reports[seed], raw_reports[seed] = run_attack(seed)
    if (reports["1"].get("attack_name_order_sha256") !=
            reports["99991"].get("attack_name_order_sha256") or
            reports["1"].get("baseline") != reports["99991"].get("baseline") or
            canon(reports["1"]) != canon(reports["99991"])):
        raise RuntimeError("attack dual-seed drift")
    hashes_after = assert_inputs()
    if hashes_before != hashes_after or MANIFEST.exists() or OUTER.exists():
        raise RuntimeError("attack mutated candidate/cold surfaces")
    report: dict[str, Any] = {
        "schema": f"cm2.c79g.{TAG}.mutation-attack-evidence.v1",
        "status": "PASS_READ_ONLY_MUTATION_ATTACKS__13_OF_13_FAIL_CLOSED__ZERO_CREDIT",
        "successor_suffix": TAG, "predecessor_suffix": PREV,
        "attack_count": 13, "failed_closed_count": 13,
        "attack_name_order_sha256": reports["1"].get("attack_name_order_sha256"),
        "attack_report_sha256": {"1": sha(raw_reports["1"]),
                                  "99991": sha(raw_reports["99991"])},
        "baseline_reconstruction": reports["1"].get("baseline", {}).get("census"),
        "effective_checkpoint_object_sha256": CHECKPOINT,
        "source_hashes": hashes_after,
        "formal_global_closure_credit": 0, "D02_unlock": False,
        "runtime_authorized": False,
        "writes": {"deliverables": False, "runtime": False,
                    "manifest": False, "outer": False, "credit": False,
                    "pyc": False},
    }
    report["object_sha256"] = sha(canon(report))
    return report, canon(report) + b"\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--seal", action="store_true")
    mode.add_argument("--install", action="store_true")
    args = parser.parse_args(argv)
    try:
        report, raw = preflight()
        if not (args.seal or args.install):
            print(json.dumps({"status": "PREFLIGHT_PASS_R41_ATTACKS__ZERO_CREDIT",
                              "receipt_target": str(RECEIPT.relative_to(ROOT)),
                              "object_sha256": report["object_sha256"],
                              "installation_performed": False,
                              "formal_global_closure_credit": 0,
                              "D02_unlock": False, "runtime_authorized": False},
                             sort_keys=True))
            return 0
        action = install(RECEIPT, raw)
        print(json.dumps({"status": report["status"],
                          "receipt": str(RECEIPT.relative_to(ROOT)),
                          "receipt_sha256": sha(raw),
                          "object_sha256": report["object_sha256"],
                          "action": action}, sort_keys=True))
        return 0
    except KeyboardInterrupt:
        print(json.dumps({"status": "FAIL_CLOSED_R41_ATTACK_EVIDENCE_INTERRUPTED",
                          "installation_performed": False,
                          "formal_global_closure_credit": 0,
                          "D02_unlock": False, "runtime_authorized": False},
                         sort_keys=True))
        return 130
    except Exception as exc:
        print(json.dumps({"status": "FAIL_CLOSED_R41_ATTACK_EVIDENCE",
                          "error": f"{type(exc).__name__}: {exc}",
                          "installation_performed": False,
                          "formal_global_closure_credit": 0,
                          "D02_unlock": False, "runtime_authorized": False},
                         sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
