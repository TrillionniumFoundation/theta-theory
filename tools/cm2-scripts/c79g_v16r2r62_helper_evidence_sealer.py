#!/usr/bin/env python3
"""r62 version-neutral helper evidence sealer (read-only by default).

The immutable r61 sealer is parsed and executed only as a recipe.  Namespace
pins are retargeted to the already-installed r62 static7/anchor and the r62
reviewer pair.  ``--seal`` is the sole mode that may append the helper receipt;
normal invocation performs only dual-seed static preflight.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import stat
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True
os.environ.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"})

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "scripts/c79g_v16r2r61_helper_evidence_sealer.py"
PARENT_SHA = "41610f547787f96fc47be53df2e3f4a2238a5faf811f046c38393009e20417af"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
TAG = "v16r2r62"
PREV = "v16r2r61"
OUT = ROOT / "deliverables"
R60_PYC = ROOT / "scripts/__pycache__/c79g_v16r2r60_candidate_builder.cpython-312.pyc"
R60_PYC_SHA = "21349b99e545c96b6521578ecbd66e0e06afb16d2fb2f3cafa1d5f149be0e4d7"
R60_PYC_SIZE = 20453
R61_PYC = ROOT / "scripts/__pycache__/c79g_v16r2r61_no_producer_evidence_sealer.cpython-312.pyc"
R61_PYC_SHA = "a25be0dadafa36751eff506d169f670776fb91f42ab4118596e5511a88a135a7"
R61_PYC_SIZE = 21748
PYC_ALLOWLIST = {
    str(R60_PYC.relative_to(ROOT)): (R60_PYC_SHA, R60_PYC_SIZE),
    str(R61_PYC.relative_to(ROOT)): (R61_PYC_SHA, R61_PYC_SIZE),
}


def stable(path: Path, expected: str | None = None,
           expected_size: int | None = None) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd); named = os.lstat(path)
        if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or
                (before.st_dev, before.st_ino, before.st_size) !=
                (named.st_dev, named.st_ino, named.st_size)):
            raise RuntimeError(f"unstable sealer witness:{path}")
        chunks: list[bytes] = []
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            chunks.append(block)
        raw = b"".join(chunks); after = os.fstat(fd)
        if (before.st_dev, before.st_ino, before.st_size) != \
                (after.st_dev, after.st_ino, len(raw)):
            raise RuntimeError(f"sealer witness changed:{path}")
        if expected is not None and hashlib.sha256(raw).hexdigest() != expected:
            raise RuntimeError(f"sealer witness hash:{path}")
        if expected_size is not None and len(raw) != expected_size:
            raise RuntimeError(f"sealer witness size:{path}")
        return raw
    finally:
        os.close(fd)


def canon(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def assert_pyc_allowlist() -> dict[str, Any]:
    witnesses: dict[str, Any] = {}
    for rel, (digest, size) in PYC_ALLOWLIST.items():
        path = ROOT / rel; raw = stable(path, digest, size); st = path.stat()
        if stat.S_IMODE(st.st_mode) != 0o664 or st.st_nlink != 1:
            raise RuntimeError(f"tooling pyc identity:{path}")
        witnesses[rel] = {"file_sha256": sha(raw), "size": len(raw),
                          "mode": stat.S_IMODE(st.st_mode), "nlink": st.st_nlink}
    unexpected: list[str] = []
    for path in ROOT.rglob("*.pyc"):
        if not path.is_file() or path.is_symlink():
            continue
        rel = str(path.relative_to(ROOT))
        if (("v16r2r60" in rel or "v16r2r61" in rel or "v16r2r62" in rel)
                and rel not in PYC_ALLOWLIST):
            unexpected.append(rel)
    if unexpected:
        raise RuntimeError("unexpected tooling pyc:" + ",".join(sorted(unexpected)))
    return {"allowlist": witnesses, "unexpected_tagged_pyc": []}


def load_parent() -> dict[str, Any]:
    raw = stable(PARENT, PARENT_SHA)
    tree = ast.parse(raw.decode("utf-8"), str(PARENT), mode="exec")
    compile(tree, str(PARENT), "exec")
    ns: dict[str, Any] = {"__name__": "_r61_helper_sealer_for_r62",
                          "__file__": str(PARENT), "__package__": None}
    exec(compile(tree, str(PARENT), "exec"), ns, ns)
    return ns


N = load_parent()
N.update({
    "BASE": BASE, "TAG": TAG, "PREV": PREV,
    "UPSTREAM": "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab",
    "SUCCESSOR": "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b",
    "ANCHOR": OUT / f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json",
    "ANCHOR_FILE_SHA": "bf90b37c218c18d974793498816f6165807685e3f8e806bbf034468a7af66194",
    "ANCHOR_OBJECT": "0262a45dfb6812eaae673955934f6eb0ca5d6ace92f75b428f1cde33e777c9c6",
    "LAUNCHER": OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py",
    "RECEIPT": OUT / f"{BASE}_{TAG}_launcher_registry_helper_version_neutral_review_receipt_v1.json",
    "REVIEW_A": ROOT / "scripts/c79g_v16r2r62_role_aware_reviewer.py",
    "REVIEW_B": ROOT / "scripts/c79g_v16r2r62_helper_reviewer_b.py",
    "MANIFEST": OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256",
    "OUTER": OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json",
    "C53": ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal",
    "C53_SHA": "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3",
})


def preflight() -> tuple[dict[str, Any], bytes]:
    body, _ = N["preflight"]()
    body = dict(body)
    body["schema"] = f"cm2.c79g.{TAG}.launcher-registry-helper-version-neutral-review.v1"
    body["status"] = "PASS_R62_DUAL_INDEPENDENT_VERSION_NEUTRAL_HELPER_REVIEW__ZERO_CREDIT"
    body["candidate_namespace"] = TAG
    body["pyc_policy"] = assert_pyc_allowlist()
    body.pop("object_sha256", None)
    body["object_sha256"] = sha(canon(body))
    return body, canon(body) + b"\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--seal", action="store_true")
    args = parser.parse_args(argv)
    try:
        body, raw = preflight()
        if args.seal:
            body["install_result"] = N["install"](raw)
        print(json.dumps(body, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":")))
        return 0
    except Exception as exc:
        print(json.dumps({"schema": f"cm2.c79g.{TAG}.helper-evidence-sealer.failure.v1",
                          "status": "FAIL_CLOSED_R62_HELPER_EVIDENCE",
                          "error": f"{type(exc).__name__}:{exc}",
                          "formal_global_closure_credit": 0,
                          "D02_unlock": False, "runtime_authorized": False},
                         separators=(",", ":")))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
