#!/usr/bin/env python3
"""Externally pinned held-FD bootstrap for the append-only r63am launcher."""
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
BASE = ROOT / "scripts/c79g_v16r2r63al_external_held_fd_bootstrap.py"
BASE_SHA256 = "5fcc6ff6bcfc569facc268375f42bd1c9fa357d56081b977ee001cc12f3a5bb4"
LAUNCHER_RELATIVE = (
    "deliverables/cm2_round306c79g_true_global_no_producer_consumer_"
    "cold_launch_v16r2r63am_repair_semantic_source.py"
)
LAUNCHER_SHA256 = "8d611ebb000b60a6d4010824754966d00df7bbc9e1b6e735c658e10c2b14c6b0"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load_impl() -> ModuleType:
    raw = BASE.read_bytes()
    if sha(raw) != BASE_SHA256:
        raise RuntimeError("immutable r63al external bootstrap recipe hash drift")
    text = raw.decode("utf-8")
    old_path = (
        "deliverables/cm2_round306c79g_true_global_no_producer_consumer_"
        "cold_launch_v16r2r63al_repair_semantic_source.py")
    text = text.replace(old_path, LAUNCHER_RELATIVE)
    text = text.replace(
        "14b8b536c42484849c1a3148b08a99389055be03b24ac7129fbd780e42b6c1b2",
        LAUNCHER_SHA256)
    for old, new in (
        ("v16r2r63al", "v16r2r63am"),
        ("r63al", "r63am"),
        ("V16R2R63AL", "V16R2R63AM"),
        ("CM2_R63AL_AUTHORIZE_APPROVED", "CM2_R63AM_AUTHORIZE_APPROVED"),
        ("R63AL", "R63AM"),
    ):
        text = text.replace(old, new)
    module = ModuleType("_c79g_v16r2r63am_external_bootstrap_impl")
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
        os.write(2, ("C79G_R63AM_EXTERNAL_BOOTSTRAP_REJECT: " +
                     str(exc) + "\n").encode("utf-8", "backslashreplace"))
        raise SystemExit(2)
