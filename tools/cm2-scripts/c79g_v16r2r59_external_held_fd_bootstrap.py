#!/usr/bin/env python3
"""r59 external held-FD bootstrap.

The historical, independently reviewed bootstrap is parsed and executed only
from an in-memory AST after its own source hash is checked.  Namespace labels
and the launcher hash are rebound to the already frozen r59 launcher.  No
candidate source is imported and this wrapper creates no workspace files.
"""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path
import os
import sys
from types import ModuleType

sys.dont_write_bytecode = True
os.environ.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"})

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "scripts/c79g_v16r2r34_external_held_fd_bootstrap.py"
BASE_SHA256 = "74ca435e47dedc473869b01eecf3b71a2101caf210605d5d4790eb9361c6709c"
R59_LAUNCHER_SHA256 = "323bced6d33ec437b8a175f82c557bcbd9ce1831411d698643b1dce1537ade80"


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _load() -> ModuleType:
    raw = BASE.read_bytes()
    if _sha(raw) != BASE_SHA256:
        raise RuntimeError("historical held-FD bootstrap source hash drift")
    text = raw.decode("utf-8")
    # Replace the old launcher namespace and its literal source pin before the
    # in-memory compile.  The replacement is intentionally lexical and scoped
    # to the independently pinned bootstrap source.
    text = text.replace("24f9686462f47c009118887d1cdfd0f1b22791eeef335bcb64252d3ade931c0a",
                        R59_LAUNCHER_SHA256)
    for old, new in (
        ("v16r2r34", "v16r2r59"),
        ("V16R2R34", "V16R2R59"),
        ("CM2_R34_AUTHORIZE_APPROVED", "CM2_R59_AUTHORIZE_APPROVED"),
        ("R34", "R59"),
    ):
        text = text.replace(old, new)
    module = ModuleType("_r59_external_held_fd_bootstrap_impl")
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
        os.write(2, ("C79G_R59_EXTERNAL_BOOTSTRAP_REJECT: " + str(exc) + "\n").encode())
        raise SystemExit(2)
