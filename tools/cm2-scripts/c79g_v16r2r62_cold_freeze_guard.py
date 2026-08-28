#!/usr/bin/env python3
"""Controlled r62 retag of the immutable r59 cold-freeze guard.

The historical guard is parsed and compiled as an inert recipe.  Its exact8
pins, side-receipt paths, and version labels are rebound in memory; this
wrapper is read-only and never changes modes or creates publication surfaces.
"""
from __future__ import annotations

import ast
import hashlib
import os
import stat
import sys
import types
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True
os.environ.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"})

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "scripts/c79g_v16r2r59_cold_freeze_guard.py"
SOURCE_SHA = "f16b81177a13c5d7cdcf804c342b1029c523b4b240611c4ca8e35590e3e0fa1d"
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

ANCHOR = ("deliverables/" + BASE +
          "_v16r2r62_active_predecessor_supersession_receipt_v1.json")
EXACT8_DATA = (
    (ANCHOR, "bf90b37c218c18d974793498816f6165807685e3f8e806bbf034468a7af66194",
     "0262a45dfb6812eaae673955934f6eb0ca5d6ace92f75b428f1cde33e777c9c6", 0o444),
    (f"deliverables/{BASE}_schema_v16r2r62.json",
     "1a9c03d332a1c12a34f330b30acb77b13a8f315732fc0bc75be29d3b8c3e1577", None, 0o444),
    (f"deliverables/{BASE}_contract_v16r2r62.json",
     "e5093fc90f063542f23c69dde6e0a674b885a5115893b668d755da81156fd4b7",
     "83e8fa14f00b1d545d09c6aeecbc85cd77c6b66d79b6c00753f1c99ac9e823bd", 0o444),
    (f"deliverables/{BASE}_v16r2r62_semantic_source.py",
     "1c494a66668b7ee7f12a1d5eac25225a68f72d256303aa7114b939e57772659a", None, 0o664),
    (f"deliverables/{BASE}_independent_verifier_assembler_authority_consumer_v16r2r62_semantic_source.py",
     "0e68a498f60d659f72247fc6a2a45ee7ee2503765c6b645d1e6ab46d6abc8f20", None, 0o664),
    (f"deliverables/{BASE}_v16r2r61_to_v16r2r62_static_launch_transition_receipt_v1.json",
     "23d328057145051a0e42d5b6c4d06350a5e2aab38c06a6a02049225b520b7357",
     "62a5a5e4f2a788c440f74425b0e13865e031cf14352b7ba99ed7ef248dfc9cdc", 0o444),
    (f"deliverables/{BASE}_static_audit_v16r2r62.json",
     "e1cf25ad75c9f7b99e375e03eee92581ac5108b35e51cabe993a77040dbe9601",
     "a4b97b73352e4129c5b1954bce83886ecdd716b63a6c5b528cafa15979756207", 0o444),
    (f"deliverables/{BASE}_cold_launch_v16r2r62_semantic_source.py",
     "d82461275e83ce720b1c18751b54de5611781db9992eae63e57091a4bf9230f0", None, 0o664),
)


def stable(path: Path, expected: str | None = None,
           expected_size: int | None = None) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd); named = os.lstat(path)
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
        raw = b"".join(chunks); after = os.fstat(fd)
        if (before.st_dev, before.st_ino, before.st_size) != \
                (after.st_dev, after.st_ino, len(raw)):
            raise RuntimeError(f"identity drift:{path}")
        if expected is not None and hashlib.sha256(raw).hexdigest() != expected:
            raise RuntimeError(f"hash drift:{path}")
        if expected_size is not None and len(raw) != expected_size:
            raise RuntimeError(f"size drift:{path}")
        return raw
    finally:
        os.close(fd)


def assert_pyc_allowlist() -> None:
    for rel, (digest, size) in PYC_ALLOWLIST.items():
        path = ROOT / rel; stable(path, digest, size); st = path.stat()
        if stat.S_IMODE(st.st_mode) != 0o664 or st.st_nlink != 1:
            raise RuntimeError(f"tooling pyc identity:{path}")
    unexpected = []
    for path in ROOT.rglob("*.pyc"):
        if not path.is_file() or path.is_symlink():
            continue
        rel = str(path.relative_to(ROOT))
        if ("v16r2r60" in rel or "v16r2r61" in rel or "v16r2r62" in rel) and rel not in PYC_ALLOWLIST:
            unexpected.append(rel)
    if unexpected:
        raise RuntimeError("unexpected tooling pyc:" + ",".join(sorted(unexpected)))


class Retag(ast.NodeTransformer):
    def visit_Constant(self, node: ast.Constant) -> ast.AST:
        if isinstance(node.value, str):
            value = node.value.replace("v16r2r59", "v16r2r62")
            value = value.replace("v16r2r58", "v16r2r61")
            value = value.replace("R59", "R62").replace("r59", "r62")
            value = value.replace("R58", "R61").replace("r58", "r61")
            return ast.copy_location(ast.Constant(value), node)
        return node


def load() -> dict[str, Any]:
    raw = stable(SOURCE, SOURCE_SHA)
    tree = ast.parse(raw.decode("utf-8"), str(SOURCE), mode="exec")
    tree = Retag().visit(tree); ast.fix_missing_locations(tree)
    compile(tree, str(SOURCE), "exec")
    # dataclass decoration in the historical guard consults sys.modules for
    # its synthetic module; register that inert namespace before exec.
    module = types.ModuleType("_r59_guard_recipe_for_r62")
    module.__file__ = str(SOURCE)
    sys.modules[module.__name__] = module
    ns: dict[str, Any] = module.__dict__
    ns.update({"__package__": None})
    exec(compile(tree, str(SOURCE), "exec"), ns, ns)
    Pin = ns["Pin"]
    ns["TAG"] = TAG; ns["PREV"] = PREV; ns["BASE"] = BASE; ns["OUT"] = OUT
    ns["EXACT8"] = tuple(Pin(path, file_sha, obj, mode)
                         for path, file_sha, obj, mode in EXACT8_DATA)
    ns["MANIFEST"] = OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256"
    ns["OUTER"] = OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json"
    ns["RECEIPTS"] = {
        "helper": OUT / f"{BASE}_{TAG}_launcher_registry_helper_version_neutral_review_receipt_v1.json",
        "no_producer": OUT / f"{BASE}_{TAG}_no_producer_dual_seed_evidence_receipt_v1.json",
        "attacks": OUT / f"{BASE}_{TAG}_mutation_attack_evidence_receipt_v1.json",
        "terminal": OUT / f"{BASE}_{TAG}_dual_checker_terminal_replay_receipt_v1.json",
    }
    return ns


def main() -> int:
    assert_pyc_allowlist()
    ns = load()
    old_tagged = ns.get("tagged_pyc")
    def tagged_pyc_r62() -> list[str]:
        assert_pyc_allowlist()
        return old_tagged() if old_tagged is not None else []
    ns["tagged_pyc"] = tagged_pyc_r62
    return int(ns["main"]())


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print({"status": "PREFLIGHT_FAIL_CLOSED_R62_COLD_FREEZE_GUARD_WRAPPER",
               "error": f"{type(exc).__name__}:{exc}",
               "manifest_created": False, "outer_created": False,
               "formal_global_closure_credit": 0, "D02_unlock": False,
               "runtime_authorized": False})
        raise
