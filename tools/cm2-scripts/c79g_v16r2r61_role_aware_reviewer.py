#!/usr/bin/env python3
"""Read-only r61 role-aware reviewer, retagged from the frozen r60 reviewer.

The reviewed implementation is loaded as an AST-only recipe.  Only its
namespace pins are rebound to the installed r61 exact8/chain; no candidate,
manifest, outer, or runtime file is written.
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
PARENT = ROOT / "scripts/c79g_v16r2r60_role_aware_reviewer.py"
PARENT_SHA = "c9443e25a75ad03258680c9e898a24c8abb9966b592f3f293fc8787090a680d9"


def stable(path: Path, expected: str | None = None) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        named = os.lstat(path)
        if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or
                (before.st_dev, before.st_ino) != (named.st_dev, named.st_ino)):
            raise RuntimeError(f"unstable reviewer witness:{path}")
        chunks: list[bytes] = []
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            chunks.append(block)
        raw = b"".join(chunks)
        after = os.fstat(fd)
        if (before.st_dev, before.st_ino, before.st_size) != \
                (after.st_dev, after.st_ino, len(raw)):
            raise RuntimeError(f"reviewer witness changed:{path}")
        if expected is not None and hashlib.sha256(raw).hexdigest() != expected:
            raise RuntimeError(f"reviewer witness hash:{path}")
        return raw
    finally:
        os.close(fd)


def load_parent() -> dict[str, Any]:
    raw = stable(PARENT, PARENT_SHA)
    tree = ast.parse(raw.decode("utf-8"), str(PARENT), mode="exec")
    compile(tree, str(PARENT), "exec")
    ns: dict[str, Any] = {"__name__": "_r60_role_reviewer_for_r61",
                          "__file__": str(PARENT), "__package__": None}
    exec(compile(tree, str(PARENT), "exec"), ns, ns)
    return ns


N = load_parent()
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
TAG = "v16r2r61"
PREV = "v16r2r60"
ANCHOR_FILE = "a6e7ebe51eed1a877f0440d2bf90827e17ca955912d449a4eaca6fc17f383838"
ANCHOR_OBJECT = "fc63955e5c40352413245ca0e8a2a4a098a4b3f596f534838a9442190dd98be2"
OUT = ROOT / "deliverables"
N.update({
    "BASE": BASE, "TAG": TAG, "PREV": PREV,
    "ANCHOR_FILE": ANCHOR_FILE, "ANCHOR_OBJECT": ANCHOR_OBJECT,
    "ANCHOR": OUT / f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json",
    "SUP": OUT / f"{BASE}_{PREV}_to_{TAG}_builder_self_report_rejection_supersession_receipt_v1.json",
    "REJ": OUT / f"{BASE}_{PREV}_builder_self_report_rejection_receipt_v1.json",
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
    raise SystemExit(N["main"]())
