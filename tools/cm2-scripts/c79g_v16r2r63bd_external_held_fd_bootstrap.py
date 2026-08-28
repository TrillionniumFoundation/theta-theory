#!/usr/bin/env python3
"""Externally pinned held-FD bootstrap for the append-only r63bd launcher."""
from __future__ import annotations

import ast
import builtins
import hashlib
import os
from pathlib import Path
import sys
from types import ModuleType

sys.dont_write_bytecode = True
os.environ.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSITE": "1"})

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "scripts/c79g_v16r2r63ba_external_held_fd_bootstrap.py"
BASE_SHA256 = "f637e8f7e8055faf8f4e94ad1c5d8f42f4a331346a17ecd25fc8ba852bbec629"
LAUNCHER_SHA256 = "44cfaab515b07c98e24196d9fc849086e9f095e968795175eb0e5f10dfb1b848"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load_impl() -> ModuleType:
    raw = BASE.read_bytes()
    if sha(raw) != BASE_SHA256:
        raise RuntimeError("immutable r63ba bootstrap recipe hash drift")
    text = raw.decode("utf-8")
    old_hash = "d55ef3672d2c6b52d2e41961eed7e791447505c8860c8d3afa5e6cca6761978c"
    if text.count(old_hash) < 1:
        raise RuntimeError("r63ba launcher pin replacement anchor drift")
    text = text.replace(old_hash, LAUNCHER_SHA256)
    text = text.replace("r63ba", "r63bd").replace("R63BA", "R63BD")
    module = ModuleType("_c79g_v16r2r63bd_external_bootstrap_impl")
    module.__file__ = str(BASE)
    module.__package__ = None
    sys.modules[module.__name__] = module
    tree = ast.parse(text, str(BASE), mode="exec")
    exec(compile(tree, str(BASE), "exec"), module.__dict__, module.__dict__)
    return module


def main(argv: list[str] | None = None) -> int:
    impl = load_impl()
    real_compile = builtins.compile
    builtins.compile = impl._compile_with_stable_root(real_compile)
    try:
        return int(impl.main(argv))
    finally:
        builtins.compile = real_compile


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        os.write(2, ("C79G_R63BD_EXTERNAL_BOOTSTRAP_REJECT: " +
                     str(exc) + "\n").encode("utf-8", "backslashreplace"))
        raise SystemExit(2)
