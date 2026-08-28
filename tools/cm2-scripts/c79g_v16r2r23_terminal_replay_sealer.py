#!/usr/bin/env python3
"""Seal r23 dual-checker terminal replay and byte-stability evidence."""
from __future__ import annotations
import hashlib, json, os, stat, subprocess, sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]; OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
TAG = "v16r2r23"; PREV = "v16r2r22"
A = ROOT / "scripts/c79g_v16r2r20_independent_reviewer.py"
B = ROOT / "scripts/c79g_v16r2r23_structure_checker_b.py"
RECEIPT = OUT / f"{BASE}_{TAG}_dual_checker_terminal_replay_receipt_v1.json"
C53 = ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"
NO_PRODUCER = OUT / f"{BASE}_{TAG}_no_producer_dual_seed_evidence_receipt_v1.json"
ATTACK = OUT / f"{BASE}_{TAG}_mutation_attack_evidence_receipt_v1.json"


def canon(v: Any) -> bytes:
    return json.dumps(v, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()


def sha(raw: bytes) -> str: return hashlib.sha256(raw).hexdigest()


def read(path: Path) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd); named = os.lstat(path)
        if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or
                (before.st_dev, before.st_ino, before.st_size) !=
                (named.st_dev, named.st_ino, named.st_size)):
            raise RuntimeError(f"identity:{path}")
        parts = []
        while True:
            b = os.read(fd, 1 << 20)
            if not b: break
            parts.append(b)
        after = os.fstat(fd); named2 = os.lstat(path)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) != (named2.st_dev, named2.st_ino)):
            raise RuntimeError(f"drift:{path}")
        return b"".join(parts)
    finally: os.close(fd)


def run(path: Path, env: dict[str, str]) -> tuple[dict[str, Any], bytes]:
    p = subprocess.run(["/usr/bin/python3", "-I", "-B", str(path)],
                       cwd=str(ROOT), env=env, capture_output=True, check=False)
    if p.returncode != 0:
        raise RuntimeError(f"{path.name}:rc={p.returncode}:{p.stderr[-300:]!r}")
    value = json.loads(p.stdout)
    if not isinstance(value, dict): raise RuntimeError("report object")
    return value, p.stdout


def install(path: Path, raw: bytes) -> str:
    try: fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC, 0o444)
    except FileExistsError:
        if read(path) != raw or stat.S_IMODE(path.stat().st_mode) != 0o444 or path.stat().st_nlink != 1:
            raise RuntimeError("append-only mismatch")
        return "replayed"
    try:
        view=memoryview(raw); off=0
        while off<len(view): off += os.write(fd, view[off:])
        os.fsync(fd); os.fchmod(fd,0o444)
    finally: os.close(fd)
    dfd=os.open(path.parent,os.O_RDONLY|os.O_DIRECTORY|os.O_CLOEXEC)
    try: os.fsync(dfd)
    finally: os.close(dfd)
    return "installed"


def main() -> int:
    try:
        exact8 = [
            OUT / f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json",
            OUT / f"{BASE}_schema_{TAG}.json",
            OUT / f"{BASE}_contract_{TAG}.json",
            OUT / f"{BASE}_{TAG}_semantic_source.py",
            OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
            OUT / f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
            OUT / f"{BASE}_static_audit_{TAG}.json",
            OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py",
        ]
        first = {str(p.relative_to(ROOT)): read(p) for p in exact8}
        second = {str(p.relative_to(ROOT)): read(p) for p in exact8}
        if first != second: raise RuntimeError("exact8 replay drift")
        if any(p.stat().st_nlink != 1 for p in exact8): raise RuntimeError("nlink")
        env = dict(os.environ); env.update({"PYTHONDONTWRITEBYTECODE":"1", "CM2_SUCCESSOR_SUFFIX":TAG, "CM2_PREDECESSOR_SUFFIX":PREV})
        a1, a1raw = run(A, env); a2, a2raw = run(A, env)
        b1, b1raw = run(B, env); b2, b2raw = run(B, env)
        if a1raw != a2raw or b1raw != b2raw: raise RuntimeError("review report replay drift")
        if (a1.get("status") != "PASS_DUAL_STATIC_CANDIDATE_34_OF_34__RUNTIME_NOT_AUTHORIZED" or
                a1.get("failed_check_count") != 0 or b1.get("status") != "PASS_INDEPENDENT_CHECKER_B__ZERO_CREDIT" or
                b1.get("failed_check_count") != 0): raise RuntimeError("checker pass")
        evidence = {}
        for name, path in (("no_producer", NO_PRODUCER), ("mutation_attacks", ATTACK)):
            raw = read(path); value = json.loads(raw)
            body = dict(value); claim = body.pop("object_sha256", None)
            if claim != sha(canon(body)): raise RuntimeError(name + " closure")
            evidence[name] = {"path": str(path.relative_to(ROOT)), "file_sha256": sha(raw), "object_sha256": claim, "status": value.get("status")}
        c53a = read(C53); c53b = read(C53)
        if c53a != c53b: raise RuntimeError("C53 drift")
        manifest = OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256"
        outer = OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json"
        if manifest.exists() or outer.exists(): raise RuntimeError("cold surface appeared")
        receipt = {
            "schema": f"cm2.c79g.{TAG}.dual-checker-terminal-replay.v1",
            "status": "PASS_DUAL_INDEPENDENT_CHECKERS_AND_TERMINAL_BYTE_REPLAY__ZERO_CREDIT",
            "successor_suffix": TAG, "predecessor_suffix": PREV,
            "exact8_ordered_paths": list(first),
            "exact8_file_sha256": {k: sha(v) for k,v in first.items()},
            "exact8_second_read_identical": True,
            "checker_A": {"check_count": a1.get("check_count"), "object_sha256": a1.get("object_sha256"), "report_sha256": sha(a1raw), "two_runs_byte_identical": True},
            "checker_B": {"check_count": b1.get("check_count"), "object_sha256": b1.get("object_sha256"), "report_sha256": sha(b1raw), "two_runs_byte_identical": True},
            "evidence_receipts": evidence,
            "C53_authority_head_sha256_before_after": sha(c53a),
            "manifest_created": False, "outer_created": False,
            "formal_global_closure_credit": 0, "D02_unlock": False,
            "runtime_authorized": False,
        }
        receipt["object_sha256"] = sha(canon(receipt)); raw = canon(receipt)+b"\n"
        action=install(RECEIPT,raw)
        print(json.dumps({"status":receipt["status"],"action":action,"receipt":str(RECEIPT.relative_to(ROOT)),"receipt_sha256":sha(raw),"object_sha256":receipt["object_sha256"]},sort_keys=True)); return 0
    except Exception as exc:
        print(json.dumps({"status":"FAIL_CLOSED_TERMINAL_REPLAY","error":f"{type(exc).__name__}: {exc}","formal_global_closure_credit":0,"D02_unlock":False,"runtime_authorized":False},sort_keys=True)); return 1


if __name__ == "__main__": raise SystemExit(main())
