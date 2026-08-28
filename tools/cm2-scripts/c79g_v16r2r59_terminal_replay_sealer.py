#!/usr/bin/env python3
"""r59 pre-freeze exact8 terminal replay receipt.

This is a read-only replay of the two current independent static reviewers and
the eight candidate bytes.  It does not chmod, publish, execute, or authorize
anything; ``--seal`` can create only this 0444 side receipt.
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
TAG = "v16r2r59"
PREV = "v16r2r58"
CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
SUCCESSOR = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"
C53 = ROOT / (".cm2-runtime/cm2-global-authority-heads/"
              "predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal")
C53_SHA = "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3"
REVIEWER_A = ROOT / "scripts/c79g_v16r2r59_role_aware_reviewer.py"
REVIEWER_B = ROOT / "scripts/c79g_v16r2r59_helper_reviewer_b.py"
NO_PRODUCER = OUT / f"{BASE}_{TAG}_no_producer_dual_seed_evidence_receipt_v1.json"
ATTACKS = OUT / f"{BASE}_{TAG}_mutation_attack_evidence_receipt_v1.json"
HELPER = OUT / f"{BASE}_{TAG}_launcher_registry_helper_version_neutral_review_receipt_v1.json"
RECEIPT = OUT / f"{BASE}_{TAG}_dual_checker_terminal_replay_receipt_v1.json"
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


def canonical(value: Any) -> bytes:
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
        data = bytearray()
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            data.extend(block)
        after = os.fstat(fd); named_after = os.lstat(path)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) !=
                (named_after.st_dev, named_after.st_ino) or
                len(data) != before.st_size):
            raise RuntimeError(f"identity drift:{path}")
        return bytes(data)
    finally:
        os.close(fd)


def closed(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = stable(path); value = json.loads(raw.decode())
    if not isinstance(value, dict):
        raise RuntimeError(f"object required:{path}")
    claim = value.get("object_sha256"); body = dict(value); body.pop("object_sha256", None)
    if not isinstance(claim, str) or sha(canonical(body)) != claim:
        raise RuntimeError(f"closure:{path}")
    return value, raw


def run_checker(path: Path, seed: str, which: str) -> tuple[dict[str, Any], bytes]:
    env = dict(os.environ)
    env.update({"PYTHONHASHSEED": seed, "PYTHONDONTWRITEBYTECODE": "1",
                "PYTHONNOUSERSITE": "1", "CM2_SUCCESSOR_SUFFIX": TAG,
                "CM2_PREDECESSOR_SUFFIX": PREV})
    proc = subprocess.run(["/usr/bin/python3", "-I", "-B", "-S", str(path)],
                          cwd=str(ROOT), env=env, text=True,
                          capture_output=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"checker {which} rc={proc.returncode}:{proc.stderr[-600:]}")
    value = json.loads(proc.stdout)
    if which == "A":
        ok = (str(value.get("status", "")).startswith("PASS_DUAL_STATIC_CANDIDATE_34_OF_34") and
              value.get("check_count") == 34 and value.get("failed_check_count") == 0 and
              value.get("formal_global_closure_credit") == 0 and
              value.get("D02_unlock") is False and value.get("runtime_authorized") is False)
    else:
        ok = (value.get("status") == "PASS_VERSION_NEUTRAL_HELPER_REVIEW_B__ZERO_CREDIT" and
              not value.get("failed_checks") and
              value.get("formal_global_closure_credit") == 0 and
              value.get("D02_unlock") is False and value.get("runtime_authorized") is False)
    if not ok:
        raise RuntimeError(f"checker {which} gate")
    return value, proc.stdout.encode()


def assert_inputs() -> dict[str, str]:
    if MANIFEST.exists() or OUTER.exists():
        raise RuntimeError("manifest/outer present")
    hashes: dict[str, str] = {}
    for path in EXACT8:
        raw = stable(path); second = stable(path); mode = stat.S_IMODE(path.stat().st_mode)
        expected = 0o664 if path.suffix == ".py" else 0o444
        if raw != second or mode != expected or path.stat().st_nlink != 1 or not raw:
            raise RuntimeError(f"exact8 mode/identity:{path}")
        hashes[str(path.relative_to(ROOT))] = sha(raw)
    for dep, statuses in ((NO_PRODUCER,
                           {"PASS_READ_ONLY_NO_PRODUCER_DUAL_SEED_RECONSTRUCTION__ZERO_CREDIT"}),
                          (ATTACKS,
                           {"PASS_R59_STATIC_ATTACK_ENUMERATION_137_OF_137__LEGACY_13_FAIL_CLOSED__"
                            "RUNTIME_EXECUTION_DEFERRED__ZERO_CREDIT"}),
                          (HELPER,
                           {"PASS_R59_DUAL_INDEPENDENT_VERSION_NEUTRAL_HELPER_REVIEW__ZERO_CREDIT"})):
        value, _ = closed(dep)
        if value.get("status") not in statuses or value.get("formal_global_closure_credit") != 0 or \
                value.get("D02_unlock") is not False or value.get("runtime_authorized") is not False:
            raise RuntimeError(f"side receipt gate:{dep.name}")
    c53 = stable(C53)
    if sha(c53) != C53_SHA:
        raise RuntimeError("C53 drift")
    if any(TAG in str(p) for p in ROOT.rglob("*.pyc")):
        raise RuntimeError("r59 pyc present")
    return hashes


def install(raw: bytes) -> str:
    try:
        fd = os.open(RECEIPT, os.O_RDWR | os.O_CREAT | os.O_EXCL |
                     os.O_CLOEXEC, 0o444)
    except FileExistsError:
        if stable(RECEIPT) != raw or RECEIPT.stat().st_nlink != 1 or \
                stat.S_IMODE(RECEIPT.stat().st_mode) != 0o444:
            raise RuntimeError("append-only mismatch")
        return "replayed"
    try:
        view = memoryview(raw); offset = 0
        while offset < len(view):
            n = os.write(fd, view[offset:])
            if n <= 0:
                raise RuntimeError("short receipt write")
            offset += n
        os.fsync(fd); os.fchmod(fd, 0o444); os.fsync(fd)
        os.lseek(fd, 0, os.SEEK_SET)
        if os.read(fd, len(raw) + 1) != raw:
            raise RuntimeError("same-fd replay")
    finally:
        os.close(fd)
    dfd = os.open(OUT, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try:
        os.fsync(dfd)
    finally:
        os.close(dfd)
    return "installed"


def preflight() -> tuple[dict[str, Any], bytes]:
    before = assert_inputs()
    checker_meta: dict[str, Any] = {}
    for which, path in (("A", REVIEWER_A), ("B", REVIEWER_B)):
        first, raw_first = run_checker(path, "1", which)
        second, raw_second = run_checker(path, "99991", which)
        if raw_first != raw_second:
            raise RuntimeError(f"checker {which} seed drift")
        checker_meta[which] = {"status": first["status"],
                               "report_sha256": sha(raw_first),
                               "failed_check_count": first.get("failed_check_count", 0)}
    after = assert_inputs()
    if before != after:
        raise RuntimeError("exact8 changed during replay")
    report: dict[str, Any] = {
        "schema": f"cm2.c79g.{TAG}.dual-checker-terminal-replay.v1",
        "status": "PASS_R59_DUAL_INDEPENDENT_CHECKERS_AND_TERMINAL_BYTE_REPLAY__ZERO_CREDIT__COLD_FREEZE_PENDING",
        "successor_suffix": TAG, "predecessor_suffix": PREV,
        "effective_checkpoint_object_sha256": CHECKPOINT,
        "successor_checkpoint_object_sha256": SUCCESSOR,
        "exact8_ordered_paths": [str(p.relative_to(ROOT)) for p in EXACT8],
        "exact8_file_sha256": before,
        "exact8_second_read_identical": True,
        "checker_reports": checker_meta,
        "evidence_receipts": {
            "no_producer": str(NO_PRODUCER.relative_to(ROOT)),
            "mutation_attacks": str(ATTACKS.relative_to(ROOT)),
            "helper_review": str(HELPER.relative_to(ROOT)),
        },
        "C53_authority_head_sha256_before_after": C53_SHA,
        "manifest_created": False, "outer_created": False,
        "formal_global_closure_credit": 0, "D02_unlock": False,
        "runtime_authorized": False,
    }
    report["object_sha256"] = sha(canonical(report))
    return report, canonical(report) + b"\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--seal", action="store_true")
    parser.add_argument("--install", action="store_true"); args = parser.parse_args(argv)
    try:
        report, raw = preflight()
        if not (args.seal or args.install):
            print(json.dumps({"status": "PREFLIGHT_PASS_R59_TERMINAL_REPLAY__ZERO_CREDIT",
                              "receipt_target": str(RECEIPT.relative_to(ROOT)),
                              "object_sha256": report["object_sha256"],
                              "installation_performed": False,
                              "formal_global_closure_credit": 0,
                              "D02_unlock": False, "runtime_authorized": False}, sort_keys=True)); return 0
        action = install(raw)
        print(json.dumps({"status": report["status"],
                          "receipt": str(RECEIPT.relative_to(ROOT)),
                          "receipt_sha256": sha(raw), "object_sha256": report["object_sha256"],
                          "action": action}, sort_keys=True)); return 0
    except Exception as exc:
        print(json.dumps({"status": "FAIL_CLOSED_R59_TERMINAL_REPLAY",
                          "error": f"{type(exc).__name__}: {exc}",
                          "formal_global_closure_credit": 0, "D02_unlock": False,
                          "runtime_authorized": False}, sort_keys=True)); return 1


if __name__ == "__main__":
    raise SystemExit(main())
