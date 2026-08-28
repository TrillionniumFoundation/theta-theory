#!/usr/bin/env python3
"""Externally pinned held-FD bootstrap for the append-only r63x launcher."""
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
BASE = ROOT / "scripts/c79g_v16r2r63w_external_held_fd_bootstrap.py"
BASE_SHA256 = "7be9026fcf7a9e954da72da857a865bcda35f6cad20f942045de6fdeecb04a8d"
LAUNCHER_RELATIVE = (
    "deliverables/cm2_round306c79g_true_global_no_producer_consumer_"
    "cold_launch_v16r2r63x_repair_semantic_source.py"
)
LAUNCHER_SHA256 = "faee8e5eac37185f99e99000c4f27164ab5902c9e756974efbfd2040acc2ab58"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load_impl() -> ModuleType:
    raw = BASE.read_bytes()
    if sha(raw) != BASE_SHA256:
        raise RuntimeError("immutable r63w external bootstrap recipe hash drift")
    text = raw.decode("utf-8")
    old_path = (
        "deliverables/cm2_round306c79g_true_global_no_producer_consumer_"
        "cold_launch_v16r2r63w_repair_semantic_source.py")
    text = text.replace(old_path, LAUNCHER_RELATIVE)
    text = text.replace("cold_launch_v16r2r63w_repair_semantic_source.py",
                        "cold_launch_v16r2r63x_repair_semantic_source.py")
    text = text.replace(
        "3ed17cef6a8f6005698b7975ceb202b9da28ad6d2603d74bf3e5f369337ed696",
        LAUNCHER_SHA256)
    for old, new in (
        ("r63w", "r63x"), ("v16r2r63w", "v16r2r63x"),
        ("V16R2R63W", "V16R2R63X"),
        ("CM2_R63W_AUTHORIZE_APPROVED", "CM2_R63X_AUTHORIZE_APPROVED"),
        ("R63W", "R63X"),
    ):
        text = text.replace(old, new)
    module = ModuleType("_c79g_v16r2r63x_external_bootstrap_impl")
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
        os.write(2, ("C79G_R63X_EXTERNAL_BOOTSTRAP_REJECT: " +
                     str(exc) + "\n").encode("utf-8", "backslashreplace"))
        raise SystemExit(2)
