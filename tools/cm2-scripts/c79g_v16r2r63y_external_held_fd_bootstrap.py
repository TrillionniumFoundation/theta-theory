#!/usr/bin/env python3
"""Externally pinned held-FD bootstrap for the append-only r63y launcher."""
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
BASE = ROOT / "scripts/c79g_v16r2r63x_external_held_fd_bootstrap.py"
BASE_SHA256 = "7b4f56a915565b2e8deed56561ec3c126a5a95724bc046328e080614e171d61f"
LAUNCHER_RELATIVE = (
    "deliverables/cm2_round306c79g_true_global_no_producer_consumer_"
    "cold_launch_v16r2r63y_repair_semantic_source.py"
)
LAUNCHER_SHA256 = "f56219ad84b72bb0b00b0a619d1d01361d09d2cb1c0666cf407a1aac115951eb"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load_impl() -> ModuleType:
    raw = BASE.read_bytes()
    if sha(raw) != BASE_SHA256:
        raise RuntimeError("immutable r63x external bootstrap recipe hash drift")
    text = raw.decode("utf-8")
    old_path = (
        "deliverables/cm2_round306c79g_true_global_no_producer_consumer_"
        "cold_launch_v16r2r63x_repair_semantic_source.py")
    text = text.replace(old_path, LAUNCHER_RELATIVE)
    text = text.replace("cold_launch_v16r2r63x_repair_semantic_source.py",
                        "cold_launch_v16r2r63y_repair_semantic_source.py")
    text = text.replace(
        "faee8e5eac37185f99e99000c4f27164ab5902c9e756974efbfd2040acc2ab58",
        LAUNCHER_SHA256)
    for old, new in (
        ("r63x", "r63y"), ("v16r2r63x", "v16r2r63y"),
        ("V16R2R63X", "V16R2R63Y"),
        ("CM2_R63X_AUTHORIZE_APPROVED", "CM2_R63Y_AUTHORIZE_APPROVED"),
        ("R63X", "R63Y"),
    ):
        text = text.replace(old, new)
    module = ModuleType("_c79g_v16r2r63y_external_bootstrap_impl")
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
        os.write(2, ("C79G_R63Y_EXTERNAL_BOOTSTRAP_REJECT: " +
                     str(exc) + "\n").encode("utf-8", "backslashreplace"))
        raise SystemExit(2)
