#!/usr/bin/env python3
"""Held-FD bootstrap for the append-only r63 publication repair.

The executable/source/root handoff remains the independently pinned r62
bootstrap and r62 launcher.  Only the manifest and outer path names are
retagged in memory to the separately sealed repair publication; the installed
r62 launcher bytes are still checked against their original SHA-256 anchor.
"""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path
import os
import sys
from types import ModuleType

sys.dont_write_bytecode = True
os.environ.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"})

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "scripts/c79g_v16r2r34_external_held_fd_bootstrap.py"
BASE_SHA256 = "74ca435e47dedc473869b01eecf3b71a2101caf210605d5d4790eb9361c6709c"
R62_LAUNCHER_SHA256 = "d82461275e83ce720b1c18751b54de5611781db9992eae63e57091a4bf9230f0"
R62_MANIFEST = "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_manifest_v16r2r62.sha256"
R62_OUTER = "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_outer_receipt_v16r2r62.json"
R63_MANIFEST = "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_manifest_v16r2r63_repair.sha256"
R63_OUTER = "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_outer_receipt_v16r2r63_repair.json"


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _load() -> ModuleType:
    raw = BASE.read_bytes()
    if _sha(raw) != BASE_SHA256:
        raise RuntimeError("historical held-FD bootstrap source hash drift")
    text = raw.decode("utf-8")
    text = text.replace("24f9686462f47c009118887d1cdfd0f1b22791eeef335bcb64252d3ade931c0a",
                        R62_LAUNCHER_SHA256)
    for old, new in (("v16r2r34", "v16r2r62"),
                     ("V16R2R34", "V16R2R62"),
                     ("CM2_R34_AUTHORIZE_APPROVED", "CM2_R62_AUTHORIZE_APPROVED"),
                     ("R34", "R62"),):
        text = text.replace(old, new)
    # The launcher itself is still the pinned r62 source; only its publication
    # path constants are rebound in the sealed in-memory module.
    text = text.replace(R62_MANIFEST, R63_MANIFEST)
    text = text.replace(R62_OUTER, R63_OUTER)
    module = ModuleType("_r63_publication_repair_external_bootstrap_impl")
    module.__file__ = str(BASE)
    module.__package__ = None
    sys.modules[module.__name__] = module
    exec(compile(ast.parse(text, str(BASE), "exec"), str(BASE), "exec"),
         module.__dict__, module.__dict__)
    return module


def main(argv: list[str] | None = None) -> int:
    return int(_load().main(argv))


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        os.write(2, ("C79G_R63_REPAIR_EXTERNAL_BOOTSTRAP_REJECT: " + str(exc) + "\n").encode())
        raise SystemExit(2)
