#!/usr/bin/env python3
"""Read-only terminal audit for the already-published r34 exact10 freeze."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
from typing import Any

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
TAG = "v16r2r34"
PREV = "v16r2r33"
CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
MANIFEST = OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256"
OUTER = OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json"
EXACT8: tuple[tuple[str, str, str | None], ...] = (
    (f"deliverables/{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json", "b0a47e3ea586aa9bca2fb647ace2086651c318b0676369e09b59d8b705ef7a89", "9047ba11c82743b18731818044755b7dedf591cf4bc1e3982921871521c78b0e"),
    (f"deliverables/{BASE}_schema_{TAG}.json", "faa68634c03eda0818f970c1963436bcc446a83695c5f20da36f6c632de9192d", None),
    (f"deliverables/{BASE}_contract_{TAG}.json", "3c1e109fbb6a80b83e623131b549bf5007d8c9e3f3676087133714aa5f554b71", "98477ae1718cd6ad1a87cbe86a2099725e80bf1c2a4c16eed1d9271a2813f780"),
    (f"deliverables/{BASE}_{TAG}_semantic_source.py", "e83a718c0a480e4deaa44fc091b18d3438f87519efe7db27f4204cf99a3596ed", None),
    (f"deliverables/{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py", "877f4a6ba6475ee27ffca8e030302d9af7c5309fcefb689b37be4049682a1e9b", None),
    (f"deliverables/{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json", "86ccf4e8543a095105958981804b1531a48b4da89f0dc9f1f363bf0c396c7933", "29d32e73855644d56d28d58345eeaf25ebc4ddc6a5c6a2ea2800f5a19faa13a3"),
    (f"deliverables/{BASE}_static_audit_{TAG}.json", "b924ecbc71ef8e280d1fa15bba22ba0af682711217713b2c7217b475c629e187", "c9c8ef2cbdfc0098e9c307ab360d5275bd4efe97f1038d24298b5684fbb5bf9a"),
    (f"deliverables/{BASE}_cold_launch_{TAG}_semantic_source.py", "24f9686462f47c009118887d1cdfd0f1b22791eeef335bcb64252d3ade931c0a", None),
)
C53 = ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"
C53_SHA = "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3"
C53_OBJECT = "cb90ab914c3b6518384669f42d05df33c21a717596190131c6a0f5683934cbfb"


def canon(v: Any) -> bytes:
    return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def stable(path: Path) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0))
    try:
        a = os.fstat(fd); n = os.lstat(path)
        if not stat.S_ISREG(a.st_mode) or a.st_nlink != 1 or (a.st_dev, a.st_ino, a.st_size) != (n.st_dev, n.st_ino, n.st_size):
            raise RuntimeError("unstable:" + str(path))
        out: list[bytes] = []
        while True:
            b = os.read(fd, 1 << 20)
            if not b: break
            out.append(b)
        z = os.fstat(fd); n2 = os.lstat(path)
        if (a.st_dev, a.st_ino, a.st_size) != (z.st_dev, z.st_ino, z.st_size) or (a.st_dev, a.st_ino) != (n2.st_dev, n2.st_ino):
            raise RuntimeError("drift:" + str(path))
        return b"".join(out)
    finally:
        os.close(fd)


def report_run(script: Path, seed: str) -> tuple[int, dict[str, Any] | None, str]:
    env = dict(os.environ); env.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1", "PYTHONHASHSEED": seed, "CM2_SUCCESSOR_SUFFIX": TAG, "CM2_PREDECESSOR_SUFFIX": PREV})
    p = subprocess.run(["/usr/bin/python3", "-I", "-B", str(script)], cwd=ROOT, env=env, capture_output=True, check=False)
    try: value = json.loads(p.stdout.decode())
    except Exception: value = None
    return p.returncode, value if isinstance(value, dict) else None, p.stderr.decode("utf-8", "replace")[-240:]


def main() -> int:
    checks: dict[str, bool] = {}
    details: dict[str, Any] = {}
    try:
        raws: list[bytes] = []
        for relative, pin, obj in EXACT8:
            p = ROOT / relative; raw = stable(p); s = os.stat(p, follow_symlinks=False)
            value = json.loads(raw.decode()) if p.suffix == ".json" else None
            actual_obj = value.get("object_sha256") if isinstance(value, dict) else None
            ok = sha(raw) == pin and stat.S_IMODE(s.st_mode) == 0o444 and s.st_nlink == 1 and (obj is None or actual_obj == obj)
            checks["exact8:" + relative] = ok; raws.append(raw)
        manifest_raw = stable(MANIFEST); outer_raw = stable(OUTER)
        expected_manifest = b"".join(f"{pin}  {relative}\n".encode("ascii") for relative, pin, _ in EXACT8)
        checks["manifest_exact_order_and_hash"] = manifest_raw == expected_manifest and sha(manifest_raw) == "10dc65def99655225de2483dcda227cc68a510dc1f2a11e1ac504641c52950cc" and stat.S_IMODE(os.stat(MANIFEST).st_mode) == 0o444 and os.stat(MANIFEST).st_nlink == 1
        outer = json.loads(outer_raw.decode()); claim = outer.get("object_sha256"); body = dict(outer); body.pop("object_sha256", None)
        checks["outer_canonical_16_key_zero_credit"] = set(outer) == {"schema", "status", "effective_checkpoint_object_sha256", "exact8_ordered_entries", "cold_launch_manifest", "cold_launcher", "all_exact8_regular_0444_nlink1_and_held_for_runtime", "outer_published_after_exact8_manifest", "runtime_entry_must_be_cold_launcher", "sole_external_static_file_anchor_is_launcher_sha256", "declared_external_tcb", "formal_global_closure_credit", "D02_unlock", "runtime_executed_during_static_freeze", "object_sha256"} and claim == sha(canon(body)) and outer_raw == canon(outer) + b"\n" and outer["effective_checkpoint_object_sha256"] == CHECKPOINT and outer["formal_global_closure_credit"] == 0 and outer["D02_unlock"] is False and outer["exact8_ordered_entries"] == [{"path": r, "file_sha256": p} for r, p, _ in EXACT8] and outer["cold_launch_manifest"]["file_sha256"] == sha(manifest_raw) and outer["cold_launcher"]["file_sha256"] == EXACT8[-1][1]
        checks["outer_hash"] = sha(outer_raw) == "9e1b41dd1083f11edcdfd6e26771eff707a14b09dd3dd3c9ba311adcd0c48d07" and claim == "ba09affd7a70d320a3ad00eeff85b32b31b3eb64e2248b129837a6a36c04927c"
        c53raw = stable(C53); c53v = json.loads(c53raw.decode()); checks["c53_unchanged"] = sha(c53raw) == C53_SHA and c53v.get("authority_seal_object_sha256") == C53_OBJECT
        checks["no_r34_pyc"] = not any(TAG in str(p) for p in ROOT.rglob("*.pyc"))
        checks["no_r34_runtime_surface"] = not any(TAG in str(p) for p in (ROOT / ".cm2-runtime").rglob("*") if p.is_file())
        # Independent static reports remain required after chmod/publication.
        scripts = {"A": ROOT / "scripts/c79g_v16r2r20_independent_reviewer.py", "B": ROOT / "scripts/c79g_v16r2r23_structure_checker_b.py", "semantic": ROOT / "scripts/c79g_v16r2r34_runtime_semantic_audit.py", "path": ROOT / "scripts/c79g_v16r2r34_path_successor_checker.py"}
        for name, script in scripts.items():
            rows = []
            for seed in ("1", "99991"):
                rc, value, err = report_run(script, seed); rows.append({"seed": seed, "rc": rc, "status": value.get("status") if value else None, "failed": value.get("failed_check_count") if value else None, "stderr": err})
            checks["report_" + name] = rows[0]["rc"] == 0 and rows[1]["rc"] == 0 and rows[0]["status"] == rows[1]["status"] and rows[0]["failed"] == 0 and rows[1]["failed"] == 0
            details["report_" + name] = rows
        details["outer_file_sha256"] = sha(outer_raw); details["outer_object_sha256"] = claim; details["manifest_file_sha256"] = sha(manifest_raw)
        passed = all(checks.values())
        out = {"schema": "cm2.c79g.v16r2r34.post-freeze-audit.v1", "status": "PASS_R34_POST_FREEZE_EXACT10_AND_DUAL_STATIC_REPLAY__ZERO_CREDIT" if passed else "FAIL_CLOSED_R34_POST_FREEZE_AUDIT", "checks": checks, "details": details, "check_count": len(checks), "failed_check_count": sum(not x for x in checks.values()), "formal_global_closure_credit": 0, "D02_unlock": False, "runtime_authorized": False}
        out["object_sha256"] = sha(canon(out)); print(json.dumps(out, ensure_ascii=False, sort_keys=True)); return 0 if passed else 1
    except Exception as exc:
        out = {"schema": "cm2.c79g.v16r2r34.post-freeze-audit.v1", "status": "FAIL_CLOSED_R34_POST_FREEZE_AUDIT_EXCEPTION", "error": f"{type(exc).__name__}: {exc}", "formal_global_closure_credit": 0, "D02_unlock": False, "runtime_authorized": False}; out["object_sha256"] = sha(canon(out)); print(json.dumps(out, sort_keys=True)); return 1


if __name__ == "__main__":
    raise SystemExit(main())
