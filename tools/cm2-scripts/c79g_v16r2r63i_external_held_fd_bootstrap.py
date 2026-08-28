#!/usr/bin/env python3
"""Externally pinned held-FD bootstrap for the r63i successor launcher."""
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
BASE = ROOT / "scripts/c79g_v16r2r34_external_held_fd_bootstrap.py"
BASE_SHA256 = "74ca435e47dedc473869b01eecf3b71a2101caf210605d5d4790eb9361c6709c"
LAUNCHER_RELATIVE = (
    "deliverables/"
    "cm2_round306c79g_true_global_no_producer_consumer_"
    "cold_launch_v16r2r63i_repair_semantic_source.py"
)
LAUNCHER_SHA256 = "e4dfcb0f2bd391968f51c7b84a240ece99a3e6e5efeb2129bcbb9f6c60fa8a02"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load_impl() -> ModuleType:
    raw = BASE.read_bytes()
    if sha(raw) != BASE_SHA256:
        raise RuntimeError("immutable external bootstrap recipe hash drift")
    text = raw.decode("utf-8")
    text = text.replace(
        "deliverables/cm2_round306c79g_true_global_no_producer_consumer_"
        "cold_launch_v16r2r34_semantic_source.py", LAUNCHER_RELATIVE)
    text = text.replace(
        "cold_launch_v16r2r34_semantic_source.py",
        "cold_launch_v16r2r63i_repair_semantic_source.py")
    text = text.replace(
        "24f9686462f47c009118887d1cdfd0f1b22791eeef335bcb64252d3ade931c0a",
        LAUNCHER_SHA256)
    for old, new in (
        ("r34", "r63i"), ("v16r2r34", "v16r2r63i"),
        ("V16R2R34", "V16R2R63I"),
        ("CM2_R34_AUTHORIZE_APPROVED", "CM2_R63I_AUTHORIZE_APPROVED"),
        ("R34", "R63I"),
    ):
        text = text.replace(old, new)
    module = ModuleType("_c79g_v16r2r63i_external_bootstrap_impl")
    module.__file__ = str(BASE)
    module.__package__ = None
    sys.modules[module.__name__] = module
    tree = ast.parse(text, str(BASE), mode="exec")
    code = compile(tree, str(BASE), "exec")
    exec(code, module.__dict__, module.__dict__)
    return module


def main(argv: list[str] | None = None) -> int:
    return int(load_impl().main(argv))


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        os.write(2, ("C79G_R63I_EXTERNAL_BOOTSTRAP_REJECT: " +
                     str(exc) + "\n").encode("utf-8", "backslashreplace"))
        raise SystemExit(2)
