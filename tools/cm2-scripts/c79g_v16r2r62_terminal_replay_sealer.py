#!/usr/bin/env python3
"""Controlled r62 retag of the frozen terminal-replay sealer.

The historical r60-named (r59-tagged) sealer is loaded as an AST recipe and
retagged in memory only.  It retains the append-only/read-only behavior of the
source; this preparation step neither runs its checkers nor seals a receipt.
"""
from __future__ import annotations

import ast
import hashlib
import os
from pathlib import Path
import stat
import sys
from typing import Any

sys.dont_write_bytecode = True
os.environ.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"})

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "scripts/c79g_v16r2r60_terminal_replay_sealer.py"
SOURCE_SHA = "94b7c02582d44b6df035e2a93e84537262d06cfc95f82d25c2c04645a09e1c20"

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


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def stable(path: Path, expected: str | None = None,
           expected_size: int | None = None) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        named = os.lstat(path)
        if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or
                (before.st_dev, before.st_ino, before.st_size) !=
                (named.st_dev, named.st_ino, named.st_size)):
            raise RuntimeError(f"unstable witness:{path}")
        chunks: list[bytes] = []
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            chunks.append(block)
        raw = b"".join(chunks)
        after = os.fstat(fd)
        named_after = os.lstat(path)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) !=
                (named_after.st_dev, named_after.st_ino) or
                len(raw) != before.st_size):
            raise RuntimeError(f"identity drift:{path}")
        if expected is not None and sha(raw) != expected:
            raise RuntimeError(f"witness hash:{path}")
        if expected_size is not None and len(raw) != expected_size:
            raise RuntimeError(f"witness size:{path}")
        return raw
    finally:
        os.close(fd)


def assert_pyc_allowlist() -> None:
    for rel, (expected, size) in PYC_ALLOWLIST.items():
        path = ROOT / rel
        raw = stable(path, expected, size)
        st = path.stat()
        if stat.S_IMODE(st.st_mode) != 0o664 or st.st_nlink != 1:
            raise RuntimeError(f"tooling pyc identity:{path}")
        if sha(raw) != expected:
            raise RuntimeError(f"tooling pyc digest:{path}")
    unexpected: list[str] = []
    for path in ROOT.rglob("*.pyc"):
        if not path.is_file() or path.is_symlink():
            continue
        rel = str(path.relative_to(ROOT))
        if (("v16r2r60" in rel or "v16r2r61" in rel or
             "v16r2r62" in rel) and rel not in PYC_ALLOWLIST):
            unexpected.append(rel)
    if unexpected:
        raise RuntimeError("unexpected tooling pyc:" + ",".join(sorted(unexpected)))


class _RetagStrings(ast.NodeTransformer):
    def visit_Constant(self, node: ast.Constant) -> ast.AST:
        if isinstance(node.value, str):
            value = node.value
            value = value.replace("v16r2r59", "v16r2r62")
            value = value.replace("v16r2r58", "v16r2r61")
            value = value.replace("R59", "R62")
            value = value.replace("r59", "r62")
            value = value.replace("r58", "r61")
            return ast.copy_location(ast.Constant(value), node)
        return node


def load_recipe() -> dict[str, Any]:
    raw = stable(SOURCE, SOURCE_SHA)
    tree = ast.parse(raw.decode("utf-8"), str(SOURCE), mode="exec")
    tree = _RetagStrings().visit(tree)
    ast.fix_missing_locations(tree)
    compile(tree, str(SOURCE), "exec")
    ns: dict[str, Any] = {"__name__": "_r60_terminal_recipe_for_r62",
                          "__file__": str(SOURCE), "__package__": None}
    exec(compile(tree, str(SOURCE), "exec"), ns, ns)
    ns["TAG"] = "v16r2r62"
    ns["PREV"] = "v16r2r61"
    return ns


def main(argv: list[str] | None = None) -> int:
    try:
        assert_pyc_allowlist()
        ns = load_recipe()
        old_assert = ns["assert_inputs"]
        old_no_tagged = ns.get("no_tagged_pyc")

        def assert_inputs_r62() -> dict[str, str]:
            result = old_assert()
            assert_pyc_allowlist()
            return result

        def no_tagged_pyc_r62() -> None:
            if old_no_tagged is not None:
                old_no_tagged()
            assert_pyc_allowlist()

        ns["assert_inputs"] = assert_inputs_r62
        if old_no_tagged is not None:
            ns["no_tagged_pyc"] = no_tagged_pyc_r62
        return int(ns["main"](argv))
    except Exception as exc:
        print({"status": "FAIL_CLOSED_R62_TERMINAL_REPLAY_WRAPPER",
               "error": f"{type(exc).__name__}: {exc}",
               "formal_global_closure_credit": 0,
               "D02_unlock": False, "runtime_authorized": False})
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
