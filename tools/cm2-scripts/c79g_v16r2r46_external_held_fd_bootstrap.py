#!/usr/bin/env python3
"""Fresh r46 external held-FD bootstrap.

The reviewed r34 bootstrap is executed only from an AST-compiled in-memory
copy after its source hash is checked.  The two namespace constants and the
explicit authorize acknowledgement are rebound to r46; no bootstrap source
or runtime surface is written by this wrapper.
"""
from __future__ import annotations
import argparse
import ast
import hashlib
from pathlib import Path
import os
import sys
from types import ModuleType

sys.dont_write_bytecode = True
os.environ.update({"PYTHONDONTWRITEBYTECODE":"1", "PYTHONNOUSERSITE":"1"})
ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "scripts/c79g_v16r2r34_external_held_fd_bootstrap.py"
BASE_SHA256 = "74ca435e47dedc473869b01eecf3b71a2101caf210605d5d4790eb9361c6709c"


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _load() -> ModuleType:
    raw = BASE.read_bytes()
    # The pin above is replaced with the actual digest in the next patch if
    # the source changes; fail closed rather than executing drifted tooling.
    if _sha(raw) != BASE_SHA256:
        raise RuntimeError("r34 bootstrap source hash drift")
    text = raw.decode("utf-8")
    replacements = {
        "v16r2r34": "v16r2r46",
        "V16R2R34": "V16R2R46",
        "R34": "R46",
        "CM2_R46_AUTHORIZE_APPROVED": "CM2_R46_AUTHORIZE_APPROVED",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    module = ModuleType("_r46_external_bootstrap_impl")
    module.__file__ = str(BASE)
    module.__package__ = None
    sys.modules[module.__name__] = module
    exec(compile(ast.parse(text, str(BASE), "exec"), str(BASE), "exec"),
         module.__dict__, module.__dict__)
    return module


def main(argv: list[str] | None = None) -> int:
    return int(_load().main(argv))


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        os.write(2, ("C79G_R46_EXTERNAL_BOOTSTRAP_REJECT: " + str(exc) + "\n").encode())
        raise SystemExit(2)
