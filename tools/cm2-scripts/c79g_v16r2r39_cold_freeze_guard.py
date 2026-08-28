#!/usr/bin/env python3
"""r39 read-only exact8 preflight, derived from the immutable r34 guard.

The implementation is loaded in memory and its namespace is rebound to the
fresh r39 candidate.  It emits a report only; it never changes modes and never
creates a manifest, outer receipt, runtime surface, or credit.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from types import ModuleType

os.environ.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"})
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
TAG = "v16r2r39"
PREV = "v16r2r38"

B58 = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
DD9 = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"


def load_template() -> ModuleType:
    path = ROOT / "scripts/c79g_v16r2r34_cold_freeze_guard.py"
    text = path.read_text(encoding="utf-8")
    module = ModuleType("_r39_cold_freeze_guard")
    module.__file__ = str(path)
    module.__package__ = None
    exec(compile(text, str(path), "exec"), module.__dict__, module.__dict__)
    return module


def exact8(module: ModuleType):
    out = module.OUT
    base = module.BASE
    tag = TAG
    prev = PREV
    return (
        (f"deliverables/{base}_{tag}_active_predecessor_supersession_receipt_v1.json",
         "9c599ef16d7be444e07ba2ae93d4c74dd71781eb859d0cb590098ed1fb03378e",
         "2a61766cf941e1798c106a150e335f224fa3d351aff3ee5eda31185b991308bd", 0o444),
        (f"deliverables/{base}_schema_{tag}.json",
         "d547ed583867e817f25d0306057e27b9e781892d6728936da6298b9e40778a61",
         None, 0o444),
        (f"deliverables/{base}_contract_{tag}.json",
         "5886242005f4eaad6ca373f9656f2e82f76ddbbd0e4ff5f1618c12b676daa542",
         "5fd9b909a7df5e77f33f9c202d211e9fd83f38792738c0711c06976249098b93", 0o444),
        (f"deliverables/{base}_{tag}_semantic_source.py",
         "f38b4cefa449102dd1992f1c454f0b55956de405c69253a208d8f55f3dca3961",
         None, 0o664),
        (f"deliverables/{base}_independent_verifier_assembler_authority_consumer_{tag}_semantic_source.py",
         "d899eb16506171d67265b8a3f57359a33e7a8dfdc2aea9498d9ace2ae4fedc9c",
         None, 0o664),
        (f"deliverables/{base}_{prev}_to_{tag}_static_launch_transition_receipt_v1.json",
         "3ee3f9c4c8f595925de135d099a6612366b6bba64404ae4e82e582d2667a96b7",
         "b17553849c4d001457922f50f44af02006ccfab758ffcd1160f97ed735f5df9e", 0o444),
        (f"deliverables/{base}_static_audit_{tag}.json",
         "2a1d24187e3e513347f05c163a38b11f3bea2d9de43afeca077a67aa7cae8b31",
         "8833b9ef25215a1b4b6c9813506fdb7a90ad498a6132a78e1ef186a287a7ed51", 0o444),
        (f"deliverables/{base}_cold_launch_{tag}_semantic_source.py",
         "40196dbcc2a40c956f42ab385b610a302952bcca1fb272b7ce640bb3a5b45543",
         None, 0o664),
    )


def main() -> int:
    module = load_template()
    module.TAG = TAG
    module.PREV = PREV
    module.CHECKPOINT = B58
    module.SUCCESSOR_CHECKPOINT = DD9
    module.EXACT8 = exact8(module)
    # Keep the previously sealed, independently generated no-producer,
    # mutation, and terminal-replay evidence as immutable upstream evidence.
    # The guard's dynamic TAG still checks the new manifest/outer names.
    return int(module.main())


if __name__ == "__main__":
    raise SystemExit(main())
