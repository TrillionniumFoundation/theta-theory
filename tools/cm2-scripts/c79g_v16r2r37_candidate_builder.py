#!/usr/bin/env python3
"""Fresh r37 static builder after r36 tooling-chain rejection."""
from __future__ import annotations

import ast
import os
from pathlib import Path
from types import ModuleType

os.environ.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1",
                   "CM2_TEMPLATE_SUFFIX": "v16r2r34",
                   "CM2_TEMPLATE_PREV_SUFFIX": "v16r2r33",
                   "CM2_PREDECESSOR_SUFFIX": "v16r2r36",
                   "CM2_SUCCESSOR_SUFFIX": "v16r2r37"})
import sys
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
TAG = "v16r2r37"; PREV = "v16r2r36"


def load_outer() -> ModuleType:
    path = ROOT / "scripts/c79g_v16r2r35_candidate_builder.py"
    text = path.read_text(encoding="utf-8")
    text = text.replace('TAG = "v16r2r35"', f'TAG = "{TAG}"', 1)
    text = text.replace('PREV = "v16r2r34"', f'PREV = "{PREV}"', 1)
    text = text.replace('CM2_PREDECESSOR_SUFFIX"] = "v16r2r34"', f'CM2_PREDECESSOR_SUFFIX"] = "{PREV}"', 1)
    text = text.replace('CM2_SUCCESSOR_SUFFIX"] = "v16r2r35"', f'CM2_SUCCESSOR_SUFFIX"] = "{TAG}"', 1)
    mod = ModuleType("_r37_schema_builder"); mod.__file__ = str(path); mod.__package__ = None
    exec(compile(text, str(path), "exec"), mod.__dict__, mod.__dict__)
    return mod


def prepare(mod: ModuleType) -> None:
    inner = mod.load_r34_module()
    def fixed_loads(text: str, role: str) -> tuple[str, int]:
        tree = ast.parse(text, mode="exec"); starts: list[int] = []; total = 0
        for line in text.splitlines(keepends=True): starts.append(total); total += len(line.encode())
        symbol = "CHECKPOINT_OBJECT_PIN" if role == "launcher" else "UPSTREAM_CHECKPOINT_OBJECT_PIN"
        replacement = "CHECKPOINT" if role == "launcher" else "UPSTREAM_CHECKPOINT_OBJECT_PIN"
        spans = [(starts[n.lineno - 1] + n.col_offset, starts[n.end_lineno - 1] + n.end_col_offset)
                 for n in ast.walk(tree) if isinstance(n, ast.Name) and n.id == symbol and isinstance(n.ctx, ast.Load)]
        raw = text.encode()
        for a, b in sorted(spans, reverse=True): raw = raw[:a] + replacement.encode() + raw[b:]
        return raw.decode(), len(spans)
    def fixed_paths(text: str, role: str) -> str:
        for old, new in (
            (f"{BASE}_v16r2r34_semantic_source.py", f"{BASE}_{TAG}_semantic_source.py"),
            (f"{BASE}_independent_verifier_assembler_authority_consumer_v16r2r34_semantic_source.py", f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py"),
            (f"{BASE}_cold_launch_v16r2r34_semantic_source.py", f"{BASE}_cold_launch_{TAG}_semantic_source.py")):
            text = text.replace(old, new)
        return text
    inner.replace_checkpoint_loads = fixed_loads
    inner.source_paths = fixed_paths
    mod.install_retag(inner)
    # Ensure the inner main receives this same patched module and generic
    # builder on every call; no fresh unpatched r34 module may be loaded.
    mod.load_r34_module = lambda: inner
    old_load_generic = inner.load_generic
    def load_generic_patched():
        builder = old_load_generic()
        builder.retag = inner.retag
        builder.source_patch = inner.source_patch
        return builder
    inner.load_generic = load_generic_patched


def main() -> int:
    mod = load_outer(); prepare(mod); return int(mod.main())


if __name__ == "__main__": raise SystemExit(main())
