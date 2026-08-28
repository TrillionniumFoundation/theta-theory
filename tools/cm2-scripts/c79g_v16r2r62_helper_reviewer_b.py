#!/usr/bin/env python3
"""Read-only r62 helper reviewer B, controlled retag of r61.

The historical checker is parsed as an inert AST recipe.  The helper source
is never imported, and the only filesystem effects are stable reads and the
JSON report on stdout.  Tooling pycs are restricted to the pinned r60/r61
witness pair.
"""
from __future__ import annotations

import ast
import hashlib
import os
import stat
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"})

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "scripts/c79g_v16r2r61_helper_reviewer_b.py"
PARENT_SHA = "a3c3a33105cb07c7d723d8943fc7952ac1b29c96d1c87a816e809154e3d55a2d"

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
        path = ROOT / rel; raw = stable(path, digest, size)
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


def main() -> int:
    # Parse the frozen r61 wrapper, then follow its pinned r60 parent into a
    # second inert namespace.  The outer wrapper keeps its checker namespace
    # local to its own main function, so it does not expose OUT directly.
    raw = stable(PARENT, PARENT_SHA)
    tree = ast.parse(raw.decode("utf-8"), str(PARENT), mode="exec")
    compile(tree, str(PARENT), "exec")
    recipe = {"__name__": "_r61_helper_recipe_for_r62",
              "__file__": str(PARENT), "__package__": None}
    exec(compile(tree, str(PARENT), "exec"), recipe, recipe)
    parent = recipe.get("PARENT")
    parent_sha = recipe.get("PARENT_SHA")
    if not isinstance(parent, Path) or not isinstance(parent_sha, str):
        raise RuntimeError("r61 helper recipe parent pin missing")
    parent_raw = stable(parent, parent_sha)
    parent_tree = ast.parse(parent_raw.decode("utf-8"), str(parent), mode="exec")
    compile(parent_tree, str(parent), "exec")
    reviewer = {"__name__": "_r60_helper_reviewer_for_r62",
                "__file__": str(parent), "__package__": None}
    exec(compile(parent_tree, str(parent), "exec"), reviewer, reviewer)
    reviewer["TAG"] = "v16r2r62"
    reviewer["CURRENT"] = reviewer["OUT"] / (
        f"{reviewer['BASE']}_cold_launch_v16r2r62_semantic_source.py")
    reviewer["PRODUCER"] = reviewer["OUT"] / (
        f"{reviewer['BASE']}_v16r2r62_semantic_source.py")
    # The helper function is intentionally version-neutral; expected AST
    # digests remain the frozen values shared by r60/r61/r62.
    return int(reviewer["main"]())


if __name__ == "__main__":
    assert_pyc_allowlist()
    raise SystemExit(main())
