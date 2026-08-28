#!/usr/bin/env python3
"""r41 independent checker/terminal replay evidence.

This wrapper runs the two independent static checkers plus the semantic/path
audits twice (hash seeds 1 and 99991), and verifies the r41 exact8 bytes are
unchanged.  It is read-only by default; only an explicit ``--seal`` or
``--install`` can create the one 0444 receipt.  No r34/r39 receipt is accepted
as a side witness, and no manifest/outer/runtime/authority/credit is touched.
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
B58 = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
C53 = ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"
C53_SHA = "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3"
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
SIDE = {
    "no_producer": OUT / f"{BASE}_{TAG}_no_producer_dual_seed_evidence_receipt_v1.json",
    "mutation_attacks": OUT / f"{BASE}_{TAG}_mutation_attack_evidence_receipt_v1.json",
}
CHECKERS = {
    "A": (ROOT / "scripts/c79g_v16r2r20_independent_reviewer.py",
           "ea7302f2e43e8977194677780deaab4a66b74070f2663ba0bb71c22655348f9d"),
    "B": (ROOT / "scripts/c79g_v16r2r23_structure_checker_b.py",
           "3e24458c32afb17f8a516a28aa20afbb503c93314d1e0382df27242d524f628d"),
    "semantic": (ROOT / "scripts/c79g_v16r2r34_runtime_semantic_audit.py",
                 "16b19de63a8aa97a82d8c0a4a5bf461395496a76bc8c8a298eb261f9b903607e"),
    "path": (ROOT / "scripts/c79g_v16r2r34_path_successor_checker.py",
             "90d824515039415e65b6249b7cd89caa481bb20ee6157e91f64c325dfddb8060"),
}


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


def closed(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = stable(path)
    value = json.loads(raw.decode())
    if not isinstance(value, dict):
        raise RuntimeError(f"receipt object:{path}")
    claim = value.get("object_sha256")
    body = dict(value); body.pop("object_sha256", None)
    if not isinstance(claim, str) or sha(canon(body)) != claim:
        raise RuntimeError(f"receipt closure:{path}")
    return value, raw


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


def assert_members() -> dict[str, str]:
    if any("v16r2r34" in str(p) or "v16r2r39" in str(p) for p in EXACT8):
        raise RuntimeError("historical exact8 path rebound")
    hashes: dict[str, str] = {}
    for path in EXACT8:
        raw = stable(path)
        if path.stat().st_nlink != 1 or stat.S_IMODE(path.stat().st_mode) not in (0o444, 0o664):
            raise RuntimeError(f"exact8 identity/mode:{path}")
        hashes[str(path.relative_to(ROOT))] = sha(raw)
    if MANIFEST.exists() or OUTER.exists():
        raise RuntimeError("manifest/outer present")
    c53 = stable(C53)
    if sha(c53) != C53_SHA:
        raise RuntimeError("C53 drift")
    return hashes


def run_checker(name: str, seed: str) -> tuple[dict[str, Any], bytes]:
    path, expected = CHECKERS[name]
    if sha(stable(path)) != expected:
        raise RuntimeError(f"checker source hash drift:{name}")
    env = dict(os.environ)
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1",
                "PYTHONHASHSEED": seed,
                "CM2_SUCCESSOR_SUFFIX": TAG,
                "CM2_PREDECESSOR_SUFFIX": PREV})
    proc = subprocess.run(["/usr/bin/python3", "-I", "-B", str(path)],
                          cwd=str(ROOT), env=env, text=True,
                          capture_output=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"{name} rc={proc.returncode}:{proc.stderr[-500:]}")
    value = json.loads(proc.stdout)
    if not isinstance(value, dict) or value.get("failed_check_count") != 0 or \
            value.get("read_only") is not True:
        raise RuntimeError(f"{name} failed/read-write report")
    expected_prefix = {"A": "PASS_DUAL_STATIC_CANDIDATE_34_OF_34",
                       "B": "PASS_INDEPENDENT_CHECKER_B",
                       "semantic": "PASS_R34_CURRENT_PATH_CHECKPOINT_AND_TRUST_AUDIT",
                       "path": "PASS_R34_PATCH_SPEC_CHECK"}[name]
    if not str(value.get("status", "")).startswith(expected_prefix):
        raise RuntimeError(f"{name} status:{value.get('status')}")
    if value.get("successor_suffix") != TAG or value.get("predecessor_suffix") != PREV:
        raise RuntimeError(f"{name} namespace report")
    return value, proc.stdout.encode()


def preflight() -> tuple[dict[str, Any], bytes]:
    before = assert_members()
    checker_reports: dict[str, Any] = {}
    checker_hashes: dict[str, str] = {}
    for name in CHECKERS:
        values: list[dict[str, Any]] = []
        raws: list[bytes] = []
        for seed in ("1", "99991"):
            value, raw = run_checker(name, seed)
            values.append(value); raws.append(raw)
        if raws[0] != raws[1] or canon(values[0]) != canon(values[1]):
            raise RuntimeError(f"{name} seed replay drift")
        checker_reports[name] = {"status": values[0]["status"],
                                 "failed_check_count": 0,
                                 "report_sha256": sha(raws[0])}
        checker_hashes[name] = sha(raws[0])
    side_meta: dict[str, Any] = {}
    for name, path in SIDE.items():
        if "v16r2r34" in str(path) or "v16r2r39" in str(path):
            raise RuntimeError("old side receipt rebound")
        value, raw = closed(path)
        expected = ("PASS_READ_ONLY_NO_PRODUCER_DUAL_SEED_RECONSTRUCTION__ZERO_CREDIT"
                    if name == "no_producer" else
                    "PASS_READ_ONLY_MUTATION_ATTACKS__13_OF_13_FAIL_CLOSED__ZERO_CREDIT")
        if value.get("status") != expected or value.get("successor_suffix") != TAG or \
                value.get("predecessor_suffix") != PREV or \
                value.get("formal_global_closure_credit") != 0 or \
                value.get("D02_unlock") is not False or \
                value.get("runtime_authorized") is not False:
            raise RuntimeError(f"side receipt gate:{name}")
        side_meta[name] = {"path": str(path.relative_to(ROOT)),
                           "file_sha256": sha(raw),
                           "object_sha256": value["object_sha256"],
                           "status": value["status"]}
    after = assert_members()
    if before != after:
        raise RuntimeError("exact8 changed during replay")
    report: dict[str, Any] = {
        "schema": f"cm2.c79g.{TAG}.dual-checker-terminal-replay.v1",
        "status": "PASS_DUAL_INDEPENDENT_CHECKERS_AND_TERMINAL_BYTE_REPLAY__ZERO_CREDIT",
        "successor_suffix": TAG, "predecessor_suffix": PREV,
        "exact8_ordered_paths": [str(p.relative_to(ROOT)) for p in EXACT8],
        "exact8_file_sha256": before, "exact8_second_read_identical": True,
        "checker_reports": checker_reports, "checker_report_sha256": checker_hashes,
        "evidence_receipts": side_meta,
        "C53_authority_head_sha256_before_after": C53_SHA,
        "manifest_created": False, "outer_created": False,
        "formal_global_closure_credit": 0, "D02_unlock": False,
        "runtime_authorized": False,
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
            print(json.dumps({"status": "PREFLIGHT_PASS_R41_TERMINAL_REPLAY__ZERO_CREDIT",
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
        print(json.dumps({"status": "FAIL_CLOSED_R41_TERMINAL_REPLAY_INTERRUPTED",
                          "installation_performed": False,
                          "formal_global_closure_credit": 0,
                          "D02_unlock": False, "runtime_authorized": False},
                         sort_keys=True))
        return 130
    except Exception as exc:
        print(json.dumps({"status": "FAIL_CLOSED_R41_TERMINAL_REPLAY",
                          "error": f"{type(exc).__name__}: {exc}",
                          "installation_performed": False,
                          "formal_global_closure_credit": 0,
                          "D02_unlock": False, "runtime_authorized": False},
                         sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
