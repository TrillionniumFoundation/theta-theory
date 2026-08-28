#!/usr/bin/env python3
"""Externally pinned held-FD bootstrap for the append-only r63af launcher."""
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
BASE = ROOT / "scripts/c79g_v16r2r63ab_external_held_fd_bootstrap.py"
BASE_SHA256 = "784d5acb7913f0678e9fadd6bc0a20d0ff5996dff3e4e57b4d23fbfad20261ab"
LAUNCHER_RELATIVE = (
    "deliverables/cm2_round306c79g_true_global_no_producer_consumer_"
    "cold_launch_v16r2r63af_repair_semantic_source.py"
)
LAUNCHER_SHA256 = "821b3cb49e3af372de9c4c32b45ed0d0cee819cdc213e768de805d458da3c223"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load_impl() -> ModuleType:
    raw = BASE.read_bytes()
    if sha(raw) != BASE_SHA256:
        raise RuntimeError("immutable r63ab external bootstrap recipe hash drift")
    text = raw.decode("utf-8")
    old_path = (
        "deliverables/cm2_round306c79g_true_global_no_producer_consumer_"
        "cold_launch_v16r2r63ab_repair_semantic_source.py")
    text = text.replace(old_path, LAUNCHER_RELATIVE)
    text = text.replace(
        "8a6d57cd49706c8b370cd2292c067c419ae161442eb9f6488677ce4457f36612",
        LAUNCHER_SHA256)
    for old, new in (
        ("r63ab", "r63af"), ("v16r2r63ab", "v16r2r63af"),
        ("V16R2R63AB", "V16R2R63AF"),
        ("CM2_R63AB_AUTHORIZE_APPROVED", "CM2_R63AF_AUTHORIZE_APPROVED"),
        ("R63AB", "R63AF"),
    ):
        text = text.replace(old, new)
    module = ModuleType("_c79g_v16r2r63af_external_bootstrap_impl")
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
        os.write(2, ("C79G_R63AF_EXTERNAL_BOOTSTRAP_REJECT: " +
                     str(exc) + "\n").encode("utf-8", "backslashreplace"))
        raise SystemExit(2)
