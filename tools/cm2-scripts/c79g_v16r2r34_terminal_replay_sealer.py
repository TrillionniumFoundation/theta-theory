#!/usr/bin/env python3
"""Seal r34 terminal replay/byte-stability evidence (no publication)."""
from __future__ import annotations

import ast
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
from typing import Any

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
TAG = "v16r2r34"; PREV = "v16r2r33"
B58 = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
C53 = ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"
RECEIPT = OUT / f"{BASE}_{TAG}_dual_checker_terminal_replay_receipt_v1.json"
SIDE = {
    "no_producer": OUT / f"{BASE}_{TAG}_no_producer_dual_seed_evidence_receipt_v1.json",
    "mutation_attacks": OUT / f"{BASE}_{TAG}_mutation_attack_evidence_receipt_v1.json",
}
EXACT8 = [
    OUT / f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json",
    OUT / f"{BASE}_schema_{TAG}.json", OUT / f"{BASE}_contract_{TAG}.json",
    OUT / f"{BASE}_{TAG}_semantic_source.py",
    OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
    OUT / f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
    OUT / f"{BASE}_static_audit_{TAG}.json",
    OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py",
]


def canon(v: Any) -> bytes:
    return json.dumps(v, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()


def sha(raw: bytes) -> str: return hashlib.sha256(raw).hexdigest()


def stable(path: Path) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd); named = os.lstat(path)
        if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or
                (before.st_dev, before.st_ino, before.st_size) !=
                (named.st_dev, named.st_ino, named.st_size)):
            raise RuntimeError("unstable")
        chunks = []
        while True:
            b = os.read(fd, 1 << 20)
            if not b: break
            chunks.append(b)
        after = os.fstat(fd); named2 = os.lstat(path)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) != (named2.st_dev, named2.st_ino)):
            raise RuntimeError("drift")
        return b"".join(chunks)
    finally: os.close(fd)


def closed(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = stable(path); v = json.loads(raw.decode())
    if not isinstance(v, dict): raise RuntimeError("receipt object")
    claim = v.get("object_sha256"); body = dict(v); body.pop("object_sha256", None)
    if not isinstance(claim, str) or sha(canon(body)) != claim: raise RuntimeError("receipt closure")
    return v, raw


def install(path: Path, raw: bytes) -> str:
    try: fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC, 0o444)
    except FileExistsError:
        if stable(path) != raw or stat.S_IMODE(path.stat().st_mode) != 0o444 or path.stat().st_nlink != 1:
            raise RuntimeError("append-only mismatch")
        return "replayed"
    try:
        view = memoryview(raw); off = 0
        while off < len(view): off += os.write(fd, view[off:])
        os.fsync(fd); os.fchmod(fd, 0o444)
    finally: os.close(fd)
    dfd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try: os.fsync(dfd)
    finally: os.close(dfd)
    return "installed"


def run(script: Path, seed: str) -> tuple[dict[str, Any], bytes]:
    env = dict(os.environ); env.update({"PYTHONDONTWRITEBYTECODE":"1", "PYTHONHASHSEED":seed,
                                        "CM2_SUCCESSOR_SUFFIX":TAG, "CM2_PREDECESSOR_SUFFIX":PREV})
    p = subprocess.run(["/usr/bin/python3", "-I", "-B", str(script)], cwd=str(ROOT), env=env,
                       capture_output=True, check=False)
    if p.returncode != 0: raise RuntimeError(f"{script.name}:rc={p.returncode}:{p.stderr[-300:]!r}")
    v = json.loads(p.stdout)
    if not isinstance(v, dict): raise RuntimeError("report object")
    return v, p.stdout


def main() -> int:
    try:
        first = {str(p.relative_to(ROOT)): stable(p) for p in EXACT8}
        second = {str(p.relative_to(ROOT)): stable(p) for p in EXACT8}
        if first != second: raise RuntimeError("exact8 replay drift")
        if any(p.stat().st_nlink != 1 for p in EXACT8): raise RuntimeError("nlink")
        scripts = {
            "A": ROOT / "scripts/c79g_v16r2r20_independent_reviewer.py",
            "B": ROOT / "scripts/c79g_v16r2r23_structure_checker_b.py",
            "semantic": ROOT / "scripts/c79g_v16r2r34_runtime_semantic_audit.py",
            "path": ROOT / "scripts/c79g_v16r2r34_path_successor_checker.py",
        }
        reports: dict[str, Any] = {}; report_hashes: dict[str, Any] = {}
        for name, script in scripts.items():
            vals = []; raws = []
            for seed in ("1", "99991"):
                v, raw = run(script, seed); vals.append(v); raws.append(raw)
            if raws[0] != raws[1]: raise RuntimeError(name + " seed report drift")
            if name == "A": ok = vals[0].get("status") == "PASS_DUAL_STATIC_CANDIDATE_34_OF_34__RUNTIME_NOT_AUTHORIZED" and vals[0].get("failed_check_count") == 0
            elif name == "B": ok = vals[0].get("status") == "PASS_INDEPENDENT_CHECKER_B__ZERO_CREDIT" and vals[0].get("failed_check_count") == 0
            elif name == "semantic": ok = vals[0].get("status") == "PASS_R34_CURRENT_PATH_CHECKPOINT_AND_TRUST_AUDIT__ZERO_CREDIT" and vals[0].get("failed_check_count") == 0
            else: ok = vals[0].get("status") == "PASS_R34_PATCH_SPEC_CHECK__ZERO_CREDIT" and vals[0].get("failed_check_count") == 0
            if not ok: raise RuntimeError(name + " gate")
            reports[name] = {"status": vals[0].get("status"), "failed_check_count": vals[0].get("failed_check_count")}
            report_hashes[name] = sha(raws[0])
        side_meta = {}
        for name, path in SIDE.items():
            v, raw = closed(path)
            expected = ("PASS_READ_ONLY_NO_PRODUCER_DUAL_SEED_RECONSTRUCTION__ZERO_CREDIT" if name == "no_producer" else
                        "PASS_READ_ONLY_MUTATION_ATTACKS__13_OF_13_FAIL_CLOSED__ZERO_CREDIT")
            if v.get("status") != expected or v.get("formal_global_closure_credit") != 0 or v.get("D02_unlock") is not False or v.get("runtime_authorized") is not False:
                raise RuntimeError(name + " side gate")
            side_meta[name] = {"path": str(path.relative_to(ROOT)), "file_sha256": sha(raw), "object_sha256": v["object_sha256"], "status": v["status"]}
        c53a, c53b = stable(C53), stable(C53)
        if c53a != c53b or sha(c53a) != "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3": raise RuntimeError("C53 drift")
        manifest = OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256"; outer = OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json"
        if manifest.exists() or outer.exists(): raise RuntimeError("manifest/outer appeared")
        receipt = {"schema": f"cm2.c79g.{TAG}.dual-checker-terminal-replay.v1",
                   "status": "PASS_DUAL_INDEPENDENT_CHECKERS_AND_TERMINAL_BYTE_REPLAY__ZERO_CREDIT",
                   "successor_suffix": TAG, "predecessor_suffix": PREV,
                   "exact8_ordered_paths": list(first),
                   "exact8_file_sha256": {k: sha(v) for k, v in first.items()},
                   "exact8_second_read_identical": True, "checker_reports": reports,
                   "checker_report_sha256": report_hashes, "evidence_receipts": side_meta,
                   "C53_authority_head_sha256_before_after": sha(c53a),
                   "manifest_created": False, "outer_created": False,
                   "formal_global_closure_credit": 0, "D02_unlock": False,
                   "runtime_authorized": False}
        receipt["object_sha256"] = sha(canon(receipt)); raw = canon(receipt) + b"\n"
        action = install(RECEIPT, raw)
        print(json.dumps({"status": receipt["status"], "action": action,
                          "receipt": str(RECEIPT.relative_to(ROOT)),
                          "receipt_sha256": sha(raw), "object_sha256": receipt["object_sha256"]}, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({"status":"FAIL_CLOSED_TERMINAL_REPLAY", "error":f"{type(exc).__name__}: {exc}",
                          "formal_global_closure_credit":0,"D02_unlock":False,"runtime_authorized":False}, sort_keys=True)); return 1


if __name__ == "__main__": raise SystemExit(main())
