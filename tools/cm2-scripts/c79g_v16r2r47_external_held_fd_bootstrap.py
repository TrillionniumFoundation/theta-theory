#!/usr/bin/env python3
"""Append-only r47 external held-FD bootstrap for the frozen r46 launcher.

The r34 bootstrap remains an immutable, pinned implementation template.  This
wrapper compiles a transformed copy in memory, rebinding its namespace to the
already frozen r46 launcher and replacing the template's launcher hash with
the actual r46 hash.  It never writes a bootstrap source, bytecode, or runtime
surface itself.  The r47 acknowledgement is deliberately distinct from the
failed r46 tooling attempt.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import os
from pathlib import Path
import sys
from types import ModuleType

sys.dont_write_bytecode = True
os.environ.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"})

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "scripts/c79g_v16r2r34_external_held_fd_bootstrap.py"
BASE_SHA256 = "74ca435e47dedc473869b01eecf3b71a2101caf210605d5d4790eb9361c6709c"
R46_LAUNCHER_SHA256 = "16f20bb7d33f955161140de87abb79e80d9ef6f1ff0d1cecc8d1872937b4b370"
R34_LAUNCHER_SHA256 = "24f9686462f47c009118887d1cdfd0f1b22791eeef335bcb64252d3ade931c0a"


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _load() -> ModuleType:
    raw = BASE.read_bytes()
    if _sha(raw) != BASE_SHA256:
        raise RuntimeError("r34 bootstrap source hash drift")
    text = raw.decode("utf-8")
    namespace_replacements = (
        ("v16r2r34", "v16r2r46"),
        ("V16R2R34", "V16R2R46"),
    )
    for old, new in namespace_replacements:
        count = text.count(old)
        if old == "v16r2r34" and count < 1:
            raise RuntimeError(f"r47 transformation literal missing:{old}")
        if count:
            text = text.replace(old, new)
    token_old = "CM2_R34_AUTHORIZE_APPROVED"
    token_count = text.count(token_old)
    if token_count < 1:
        raise RuntimeError("r47 authorization token literal missing")
    text = text.replace(token_old, "CM2_R47_AUTHORIZE_APPROVED")
    hash_count = text.count(R34_LAUNCHER_SHA256)
    if hash_count != 1:
        raise RuntimeError(f"r47 transformation literal count:{R34_LAUNCHER_SHA256}:{hash_count}")
    text = text.replace(R34_LAUNCHER_SHA256, R46_LAUNCHER_SHA256, 1)
    tree = ast.parse(text, str(BASE), "exec")
    # Verify the transformed constants before executing the in-memory module.
    literals = {
        node.targets[0].id: node.value.value
        for node in tree.body
        if isinstance(node, ast.Assign)
        and len(node.targets) == 1
        and isinstance(node.targets[0], ast.Name)
        and isinstance(node.value, ast.Constant)
        and isinstance(node.value.value, str)
        and node.targets[0].id in {"LAUNCHER_RELATIVE", "LAUNCHER_SHA256"}
    }
    if literals.get("LAUNCHER_SHA256") != R46_LAUNCHER_SHA256:
        raise RuntimeError("r47 transformed launcher hash not installed")
    module = ModuleType("_r47_external_bootstrap_impl")
    module.__file__ = str(BASE)
    module.__package__ = None
    sys.modules[module.__name__] = module
    exec(compile(tree, str(BASE), "exec"), module.__dict__, module.__dict__)
    return module


def main(argv: list[str] | None = None) -> int:
    return int(_load().main(argv))


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        os.write(2, ("C79G_R47_EXTERNAL_BOOTSTRAP_REJECT: " + str(exc) + "\n").encode())
        raise SystemExit(2)
