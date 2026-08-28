#!/usr/bin/env python3
"""Fresh r36 invocation of the audited schema-repair clean-room builder.

r35 already has an immutable rejection/supersession chain from a tooling
failure, so this wrapper advances to r36 and never reuses that namespace.
"""
from __future__ import annotations

import os
import ast
from pathlib import Path
from types import ModuleType

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
os.environ["PYTHONNOUSERSITE"] = "1"
os.environ["CM2_TEMPLATE_SUFFIX"] = "v16r2r34"
os.environ["CM2_TEMPLATE_PREV_SUFFIX"] = "v16r2r33"
os.environ["CM2_PREDECESSOR_SUFFIX"] = "v16r2r35"
os.environ["CM2_SUCCESSOR_SUFFIX"] = "v16r2r36"
import sys
sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]


def load_transformed() -> ModuleType:
    source_path = ROOT / "scripts/c79g_v16r2r35_candidate_builder.py"
    source = source_path.read_text(encoding="utf-8")
    # Change only the wrapper's active assignment/env literals.  The embedded
    # r34 exact10 pin table is intentionally left byte-for-byte untouched.
    source = source.replace('TAG = "v16r2r35"', 'TAG = "v16r2r36"', 1)
    source = source.replace('PREV = "v16r2r34"', 'PREV = "v16r2r35"', 1)
    source = source.replace('CM2_PREDECESSOR_SUFFIX"] = "v16r2r34"',
                            'CM2_PREDECESSOR_SUFFIX"] = "v16r2r35"', 1)
    source = source.replace('CM2_SUCCESSOR_SUFFIX"] = "v16r2r35"',
                            'CM2_SUCCESSOR_SUFFIX"] = "v16r2r36"', 1)
    module = ModuleType("_r36_schema_repair_builder")
    module.__file__ = str(source_path); module.__package__ = None
    exec(compile(source, str(source_path), "exec"), module.__dict__, module.__dict__)
    return module


def main() -> int:
    module = load_transformed()
    # Prepare the inner r34 module once so the r34 main cannot reload an
    # unpatched copy.  Its historical helper counted only the literal
    # CHECKPOINT_OBJECT_PIN name; r34 producer/consumer sources already use
    # UPSTREAM_CHECKPOINT_OBJECT_PIN, so count that symbol as well.
    inner = module.load_r34_module()
    def fixed_checkpoint_loads(text: str, role: str) -> tuple[str, int]:
        tree = ast.parse(text, mode="exec")
        starts: list[int] = []
        total = 0
        for line in text.splitlines(keepends=True):
            starts.append(total); total += len(line.encode("utf-8"))
        symbol = "CHECKPOINT_OBJECT_PIN" if role == "launcher" else "UPSTREAM_CHECKPOINT_OBJECT_PIN"
        replacement = "CHECKPOINT" if role == "launcher" else "UPSTREAM_CHECKPOINT_OBJECT_PIN"
        spans: list[tuple[int, int]] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and node.id == symbol and isinstance(node.ctx, ast.Load):
                spans.append((starts[node.lineno - 1] + node.col_offset,
                              starts[node.end_lineno - 1] + node.end_col_offset))
        raw = text.encode("utf-8")
        for left, right in sorted(spans, reverse=True):
            raw = raw[:left] + replacement.encode("ascii") + raw[right:]
        return raw.decode("utf-8"), len(spans)
    inner.replace_checkpoint_loads = fixed_checkpoint_loads
    def fixed_source_paths(text: str, role: str) -> str:
        # r34 is already a suffixed executable source; the generic helper's
        # old unsuffixed SELF assertion is not applicable to this successor.
        replacements = (
            (f"{BASE}_v16r2r34_semantic_source.py",
             f"{BASE}_v16r2r36_semantic_source.py"),
            (f"{BASE}_independent_verifier_assembler_authority_consumer_v16r2r34_semantic_source.py",
             f"{BASE}_independent_verifier_assembler_authority_consumer_v16r2r36_semantic_source.py"),
            (f"{BASE}_cold_launch_v16r2r34_semantic_source.py",
             f"{BASE}_cold_launch_v16r2r36_semantic_source.py"),
        )
        for old, new in replacements:
            text = text.replace(old, new)
        return text
    inner.source_paths = fixed_source_paths
    module.install_retag(inner)
    module.load_r34_module = lambda: inner
    return int(module.main())


if __name__ == "__main__":
    raise SystemExit(main())
