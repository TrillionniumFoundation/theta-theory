#!/usr/bin/env python3
"""Externally pinned held-FD bootstrap for the append-only r63aa launcher."""
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
BASE = ROOT / "scripts/c79g_v16r2r63z_external_held_fd_bootstrap.py"
BASE_SHA256 = "21c38ef33895eff1e12758edd60e76a106a4718f6322a87864f23180671e58bd"
LAUNCHER_RELATIVE = (
    "deliverables/cm2_round306c79g_true_global_no_producer_consumer_"
    "cold_launch_v16r2r63aa_repair_semantic_source.py"
)
LAUNCHER_SHA256 = "3966cc1492bbc0f700a66c5bc9ba377bac39faf34c898f6571bc030623070de7"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load_impl() -> ModuleType:
    raw = BASE.read_bytes()
    if sha(raw) != BASE_SHA256:
        raise RuntimeError("immutable r63z external bootstrap recipe hash drift")
    text = raw.decode("utf-8")
    old_path = (
        "deliverables/cm2_round306c79g_true_global_no_producer_consumer_"
        "cold_launch_v16r2r63z_repair_semantic_source.py")
    text = text.replace(old_path, LAUNCHER_RELATIVE)
    text = text.replace("cold_launch_v16r2r63z_repair_semantic_source.py",
                        "cold_launch_v16r2r63aa_repair_semantic_source.py")
    text = text.replace(
        "16c72f0a78c4cd0346000f83c551de00420896368cce591d213f27d6f01e9933",
        LAUNCHER_SHA256)
    for old, new in (
        ("r63z", "r63aa"), ("v16r2r63z", "v16r2r63aa"),
        ("V16R2R63Z", "V16R2R63AA"),
        ("CM2_R63Z_AUTHORIZE_APPROVED", "CM2_R63AA_AUTHORIZE_APPROVED"),
        ("R63Z", "R63AA"),
    ):
        text = text.replace(old, new)
    module = ModuleType("_c79g_v16r2r63aa_external_bootstrap_impl")
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
        os.write(2, ("C79G_R63AA_EXTERNAL_BOOTSTRAP_REJECT: " +
                     str(exc) + "\n").encode("utf-8", "backslashreplace"))
        raise SystemExit(2)
