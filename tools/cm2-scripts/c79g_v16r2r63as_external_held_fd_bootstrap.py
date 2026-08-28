#!/usr/bin/env python3
"""Externally pinned held-FD bootstrap for the append-only r63as launcher."""
from __future__ import annotations

import ast
import hashlib
import os
from pathlib import Path
import sys
from types import ModuleType

sys.dont_write_bytecode = True
os.environ.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSITE": "1"})

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "scripts/c79g_v16r2r63an_external_held_fd_bootstrap.py"
BASE_SHA256 = "30ce28c461996ab4866f55aca1b3bb8bbe69a1d3a938b074bbc683c0f14f66da"
# Pinned to the freshly installed r63as generated launcher.
LAUNCHER_SHA256 = "a42a0fbf920df6b3f63c718fe63e68c80ab6de15cf7c8cee7f187da1ee1e92d0"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load_impl() -> ModuleType:
    raw = BASE.read_bytes()
    if sha(raw) != BASE_SHA256:
        raise RuntimeError("immutable r63an bootstrap recipe hash drift")
    text = raw.decode("utf-8").replace(
        "905b3f9d94a03122ae336f9f67de6699159c91bf5fd2f0a1ce3ecd07cc5b1b47",
        LAUNCHER_SHA256)
    text = text.replace("r63an", "r63as").replace("R63AN", "R63AS")
    module = ModuleType("_c79g_v16r2r63as_external_bootstrap_impl")
    module.__file__ = str(BASE)
    module.__package__ = None
    sys.modules[module.__name__] = module
    tree = ast.parse(text, str(BASE), mode="exec")
    exec(compile(tree, str(BASE), "exec"), module.__dict__, module.__dict__)
    return module


def main(argv: list[str] | None = None) -> int:
    return int(load_impl().main(argv))


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        os.write(2, ("C79G_R63AS_EXTERNAL_BOOTSTRAP_REJECT: " +
                     str(exc) + "\n").encode("utf-8", "backslashreplace"))
        raise SystemExit(2)
