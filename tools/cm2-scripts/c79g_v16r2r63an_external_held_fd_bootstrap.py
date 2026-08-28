#!/usr/bin/env python3
"""Externally pinned held-FD bootstrap for the append-only r63an launcher."""
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
BASE = ROOT / "scripts/c79g_v16r2r63am_external_held_fd_bootstrap.py"
BASE_SHA256 = "65dd6fc57e5194af34811f06d40da039b6157655d3814d77847cff5c993e682a"
LAUNCHER_RELATIVE = (
    "deliverables/cm2_round306c79g_true_global_no_producer_consumer_"
    "cold_launch_v16r2r63an_repair_semantic_source.py"
)
LAUNCHER_SHA256 = "905b3f9d94a03122ae336f9f67de6699159c91bf5fd2f0a1ce3ecd07cc5b1b47"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load_impl() -> ModuleType:
    raw = BASE.read_bytes()
    if sha(raw) != BASE_SHA256:
        raise RuntimeError("immutable r63am external bootstrap recipe hash drift")
    text = raw.decode("utf-8")
    old_path = (
        "deliverables/cm2_round306c79g_true_global_no_producer_consumer_"
        "cold_launch_v16r2r63am_repair_semantic_source.py")
    text = text.replace(old_path, LAUNCHER_RELATIVE)
    text = text.replace(
        "8d611ebb000b60a6d4010824754966d00df7bbc9e1b6e735c658e10c2b14c6b0",
        LAUNCHER_SHA256)
    for old, new in (
        ("v16r2r63am", "v16r2r63an"),
        ("r63am", "r63an"),
        ("V16R2R63AM", "V16R2R63AN"),
        ("CM2_R63AM_AUTHORIZE_APPROVED", "CM2_R63AN_AUTHORIZE_APPROVED"),
        ("R63AM", "R63AN"),
    ):
        text = text.replace(old, new)
    module = ModuleType("_c79g_v16r2r63an_external_bootstrap_impl")
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
        os.write(2, ("C79G_R63AN_EXTERNAL_BOOTSTRAP_REJECT: " +
                     str(exc) + "\n").encode("utf-8", "backslashreplace"))
        raise SystemExit(2)
