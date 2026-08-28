#!/usr/bin/env python3
"""Read-only r62 role-aware reviewer, controlled retag of r61.

The frozen r61 reviewer is parsed and executed in an inert namespace.  The
only candidate-specific changes are r62 chain/path/hash pins.  A separate
precheck enforces the r60-builder + r61-sealer tooling-pyc allowlist; no
candidate, manifest, outer, or runtime file is written.
"""
from __future__ import annotations

import ast
import hashlib
import os
import stat
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True
os.environ.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"})

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "scripts/c79g_v16r2r61_role_aware_reviewer.py"
PARENT_SHA = "287ca04c066028bb1071cd8d989e286db7616f9ea43fbf36fb4dc85685cc0ab7"

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
            raise RuntimeError(f"unstable reviewer witness:{path}")
        chunks: list[bytes] = []
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            chunks.append(block)
        raw = b"".join(chunks); after = os.fstat(fd)
        if (before.st_dev, before.st_ino, before.st_size) != \
                (after.st_dev, after.st_ino, len(raw)):
            raise RuntimeError(f"reviewer witness changed:{path}")
        if expected is not None and hashlib.sha256(raw).hexdigest() != expected:
            raise RuntimeError(f"reviewer witness hash:{path}")
        if expected_size is not None and len(raw) != expected_size:
            raise RuntimeError(f"reviewer witness size:{path}")
        return raw
    finally:
        os.close(fd)


def assert_pyc_allowlist() -> None:
    for rel, (digest, size) in PYC_ALLOWLIST.items():
        path = ROOT / rel
        raw = stable(path, digest, size)
        if stat.S_IMODE(path.stat().st_mode) != 0o664 or path.stat().st_nlink != 1:
            raise RuntimeError(f"tooling pyc identity:{path}")
        if hashlib.sha256(raw).hexdigest() != digest:
            raise RuntimeError(f"tooling pyc digest:{path}")
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


def load_parent() -> dict[str, Any]:
    raw = stable(PARENT, PARENT_SHA)
    tree = ast.parse(raw.decode("utf-8"), str(PARENT), mode="exec")
    compile(tree, str(PARENT), "exec")
    ns: dict[str, Any] = {"__name__": "_r61_role_reviewer_for_r62",
                          "__file__": str(PARENT), "__package__": None}
    exec(compile(tree, str(PARENT), "exec"), ns, ns)
    return ns


N = load_parent()
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
TAG = "v16r2r62"
PREV = "v16r2r61"
OUT = ROOT / "deliverables"
ANCHOR_FILE = "bf90b37c218c18d974793498816f6165807685e3f8e806bbf034468a7af66194"
ANCHOR_OBJECT = "0262a45dfb6812eaae673955934f6eb0ca5d6ace92f75b428f1cde33e777c9c6"
N.update({
    "BASE": BASE, "TAG": TAG, "PREV": PREV,
    "ANCHOR_FILE": ANCHOR_FILE, "ANCHOR_OBJECT": ANCHOR_OBJECT,
    "ANCHOR": OUT / f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json",
    "SUP": OUT / f"{BASE}_{PREV}_to_{TAG}_no_producer_tooling_pyc_rejection_supersession_receipt_v1.json",
    "REJ": OUT / f"{BASE}_{PREV}_no_producer_tooling_pyc_rejection_receipt_v1.json",
    "V14": OUT / f"{BASE}_v14_runtime_registry_shape_drift_rejection_supersession_receipt_v1.json",
    "MANIFEST": OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256",
    "OUTER": OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json",
    "SOURCES": {
        "producer": OUT / f"{BASE}_{TAG}_semantic_source.py",
        "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
        "launcher": OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py",
    },
    "JSONS": {
        "schema": OUT / f"{BASE}_schema_{TAG}.json",
        "contract": OUT / f"{BASE}_contract_{TAG}.json",
        "transition": OUT / f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
        "audit": OUT / f"{BASE}_static_audit_{TAG}.json",
    },
})


if __name__ == "__main__":
    assert_pyc_allowlist()
    # The r61 wrapper itself contains the frozen r60 namespace under ``N``;
    # use that inner reviewer namespace rather than assuming the wrapper
    # re-exports every function at top level.
    reviewer = N.get("N", N)
    reviewer.update({
        "BASE": BASE, "TAG": TAG, "PREV": PREV,
        "ANCHOR_FILE": ANCHOR_FILE, "ANCHOR_OBJECT": ANCHOR_OBJECT,
        "ANCHOR": N["ANCHOR"], "SUP": N["SUP"], "REJ": N["REJ"],
        "V14": N["V14"], "MANIFEST": N["MANIFEST"], "OUTER": N["OUTER"],
        "SOURCES": N["SOURCES"], "JSONS": N["JSONS"],
    })
    raise SystemExit(reviewer["main"]())
