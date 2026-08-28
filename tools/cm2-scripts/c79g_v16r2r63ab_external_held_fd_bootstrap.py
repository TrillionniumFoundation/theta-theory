#!/usr/bin/env python3
"""Externally pinned held-FD bootstrap for the append-only r63ab launcher."""
from __future__ import annotations

import ast
import hashlib
import os
from pathlib import Path
import sys
from types import ModuleType

sys.dont_write_bytecode = True
os.environ.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"})

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "scripts/c79g_v16r2r63aa_external_held_fd_bootstrap.py"
BASE_SHA256 = "04924b7bca5271771fbe84b6aa0c62f70fd7b06f5dfbfd523541e89b35a56565"
LAUNCHER_RELATIVE = (
    "deliverables/cm2_round306c79g_true_global_no_producer_consumer_"
    "cold_launch_v16r2r63ab_repair_semantic_source.py"
)
LAUNCHER_SHA256 = "8a6d57cd49706c8b370cd2292c067c419ae161442eb9f6488677ce4457f36612"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load_impl() -> ModuleType:
    raw = BASE.read_bytes()
    if sha(raw) != BASE_SHA256:
        raise RuntimeError("immutable r63aa external bootstrap recipe hash drift")
    text = raw.decode("utf-8")
    old_path = (
        "deliverables/cm2_round306c79g_true_global_no_producer_consumer_"
        "cold_launch_v16r2r63aa_repair_semantic_source.py")
    text = text.replace(old_path, LAUNCHER_RELATIVE)
    text = text.replace(
        "16r2r63aa_repair_semantic_source.py",
        "16r2r63ab_repair_semantic_source.py")
    text = text.replace(
        "3966cc1492bbc0f700a66c5bc9ba377bac39faf34c898f6571bc030623070de7",
        LAUNCHER_SHA256)
    for old, new in (
        ("r63aa", "r63ab"), ("v16r2r63aa", "v16r2r63ab"),
        ("V16R2R63AA", "V16R2R63AB"),
        ("CM2_R63AA_AUTHORIZE_APPROVED", "CM2_R63AB_AUTHORIZE_APPROVED"),
        ("R63AA", "R63AB"),
    ):
        text = text.replace(old, new)
    module = ModuleType("_c79g_v16r2r63ab_external_bootstrap_impl")
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
        os.write(2, ("C79G_R63AB_EXTERNAL_BOOTSTRAP_REJECT: " +
                     str(exc) + "\n").encode("utf-8", "backslashreplace"))
        raise SystemExit(2)
