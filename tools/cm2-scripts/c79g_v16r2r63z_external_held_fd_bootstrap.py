#!/usr/bin/env python3
"""Externally pinned held-FD bootstrap for the append-only r63z launcher."""
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
BASE = ROOT / "scripts/c79g_v16r2r63y_external_held_fd_bootstrap.py"
BASE_SHA256 = "60b8d83ef4c3401938bb5e77df324ae5520d801bef0c3fde445e25f42fc5772d"
LAUNCHER_RELATIVE = (
    "deliverables/cm2_round306c79g_true_global_no_producer_consumer_"
    "cold_launch_v16r2r63z_repair_semantic_source.py"
)
LAUNCHER_SHA256 = "16c72f0a78c4cd0346000f83c551de00420896368cce591d213f27d6f01e9933"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load_impl() -> ModuleType:
    raw = BASE.read_bytes()
    if sha(raw) != BASE_SHA256:
        raise RuntimeError("immutable r63y external bootstrap recipe hash drift")
    text = raw.decode("utf-8")
    old_path = (
        "deliverables/cm2_round306c79g_true_global_no_producer_consumer_"
        "cold_launch_v16r2r63y_repair_semantic_source.py")
    text = text.replace(old_path, LAUNCHER_RELATIVE)
    text = text.replace("cold_launch_v16r2r63y_repair_semantic_source.py",
                        "cold_launch_v16r2r63z_repair_semantic_source.py")
    text = text.replace(
        "f56219ad84b72bb0b00b0a619d1d01361d09d2cb1c0666cf407a1aac115951eb",
        LAUNCHER_SHA256)
    for old, new in (
        ("r63y", "r63z"), ("v16r2r63y", "v16r2r63z"),
        ("V16R2R63Y", "V16R2R63Z"),
        ("CM2_R63Y_AUTHORIZE_APPROVED", "CM2_R63Z_AUTHORIZE_APPROVED"),
        ("R63Y", "R63Z"),
    ):
        text = text.replace(old, new)
    module = ModuleType("_c79g_v16r2r63z_external_bootstrap_impl")
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
        os.write(2, ("C79G_R63Z_EXTERNAL_BOOTSTRAP_REJECT: " +
                     str(exc) + "\n").encode("utf-8", "backslashreplace"))
        raise SystemExit(2)
