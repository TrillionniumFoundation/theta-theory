#!/usr/bin/env python3
"""Controlled, read-only r61 retag of the frozen r60 helper reviewer B.

The reviewed r60 implementation is loaded as an inert AST recipe.  Only its
TAG/current/producer paths are rebound in memory; no r60 source or receipt is
modified and no candidate/runtime entry is executed.
"""
from __future__ import annotations

import ast
import hashlib
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"})

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "scripts/c79g_v16r2r60_helper_reviewer_b.py"
PARENT_SHA = "d4964e9815b678bd73574d6403fdd236e433b7c09c1234e492f7cab90c042fab"


def stable(path: Path, expected: str | None = None) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        named = os.lstat(path)
        if (before.st_dev, before.st_ino, before.st_size) != \
                (named.st_dev, named.st_ino, named.st_size) or \
                before.st_nlink != 1:
            raise RuntimeError(f"unstable reviewer parent:{path}")
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
            raise RuntimeError(f"reviewer parent changed:{path}")
        if expected is not None and hashlib.sha256(raw).hexdigest() != expected:
            raise RuntimeError(f"reviewer parent hash:{path}")
        return raw
    finally:
        os.close(fd)


def main() -> int:
    raw = stable(PARENT, PARENT_SHA)
    tree = ast.parse(raw.decode("utf-8"), str(PARENT), mode="exec")
    compile(tree, str(PARENT), "exec")
    ns = {"__name__": "_r60_helper_reviewer_for_r61",
          "__file__": str(PARENT), "__package__": None}
    exec(compile(tree, str(PARENT), "exec"), ns, ns)
    ns["TAG"] = "v16r2r61"
    ns["CURRENT"] = ns["OUT"] / (
        f"{ns['BASE']}_cold_launch_v16r2r61_semantic_source.py")
    ns["PRODUCER"] = ns["OUT"] / (
        f"{ns['BASE']}_v16r2r61_semantic_source.py")
    # The helper AST is version-neutral; EXPECTED_CURRENT remains the frozen
    # digest shared by r60/r61.  Invoke only the reviewer's read-only main.
    return int(ns["main"]())


if __name__ == "__main__":
    raise SystemExit(main())
