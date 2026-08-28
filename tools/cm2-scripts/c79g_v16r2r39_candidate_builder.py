#!/usr/bin/env python3
"""Fresh append-only r39 candidate builder.

r38's in-memory DAG was otherwise closed, but its launcher source patch saw
the active namespace block twice: the r34 template already contained the
block and ``launcher_globals`` injected it a second time.  r39 removes that
single template-local block in memory, then lets the audited r34 patcher add
one canonical block.  No r34--r38 bytes are modified or reused as outputs.
"""
from __future__ import annotations

import ast
import os
import re
import sys
from pathlib import Path
from types import ModuleType

os.environ.update({
    "PYTHONDONTWRITEBYTECODE": "1",
    "PYTHONNOUSERSITE": "1",
    "CM2_TEMPLATE_SUFFIX": "v16r2r34",
    "CM2_TEMPLATE_PREV_SUFFIX": "v16r2r33",
    "CM2_PREDECESSOR_SUFFIX": "v16r2r38",
    "CM2_SUCCESSOR_SUFFIX": "v16r2r39",
})
sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
TAG = "v16r2r39"
PREV = "v16r2r38"


def load_outer() -> ModuleType:
    """Load the complete r35 builder as source, retagged in memory only."""
    path = ROOT / "scripts/c79g_v16r2r35_candidate_builder.py"
    text = path.read_text(encoding="utf-8")
    replacements = (
        ('TAG = "v16r2r35"', f'TAG = "{TAG}"'),
        ('PREV = "v16r2r34"', f'PREV = "{PREV}"'),
        ('CM2_PREDECESSOR_SUFFIX"] = "v16r2r34"',
         f'CM2_PREDECESSOR_SUFFIX"] = "{PREV}"'),
        ('CM2_SUCCESSOR_SUFFIX"] = "v16r2r35"',
         f'CM2_SUCCESSOR_SUFFIX"] = "{TAG}"'),
    )
    for old, new in replacements:
        if text.count(old) != 1:
            raise RuntimeError(f"r39 template literal census:{old}:{text.count(old)}")
        text = text.replace(old, new, 1)
    module = ModuleType("_r39_builder")
    module.__file__ = str(path)
    module.__package__ = None
    exec(compile(text, str(path), "exec"), module.__dict__, module.__dict__)
    return module


def _offsets(text: str) -> list[int]:
    result: list[int] = []
    total = 0
    for line in text.splitlines(keepends=True):
        result.append(total)
        total += len(line.encode("utf-8"))
    return result


def _fixed_loads(text: str, role: str):
    """Normalize only executable checkpoint loads; preserve successor literals."""
    tree = ast.parse(text, mode="exec")
    symbol = "CHECKPOINT" if role == "launcher" else "UPSTREAM_CHECKPOINT_OBJECT_PIN"
    # The r34 launcher already loads CHECKPOINT.  Counting those loads is the
    # source-patch gate; replacing a name with itself is deliberately a no-op.
    starts = _offsets(text)
    spans = [
        (starts[node.lineno - 1] + node.col_offset,
         starts[node.end_lineno - 1] + node.end_col_offset)
        for node in ast.walk(tree)
        if isinstance(node, ast.Name) and node.id == symbol
        and isinstance(node.ctx, ast.Load)
    ]
    raw = text.encode("utf-8")
    for start, end in sorted(spans, reverse=True):
        raw = raw[:start] + symbol.encode("ascii") + raw[end:]
    return raw.decode("utf-8"), len(spans)


def _fixed_paths(text: str, role: str) -> str:
    replacements = (
        (f"{BASE}_v16r2r34_semantic_source.py",
         f"{BASE}_{TAG}_semantic_source.py"),
        (f"{BASE}_independent_verifier_assembler_authority_consumer_v16r2r34_semantic_source.py",
         f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py"),
        (f"{BASE}_cold_launch_v16r2r34_semantic_source.py",
         f"{BASE}_cold_launch_{TAG}_semantic_source.py"),
    )
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def _strip_config_active_block(text: str) -> str:
    """Remove exactly one pre-existing active block inside the configurator."""
    # Restrict the match to indented lines, so module-scope declarations and
    # historical evidence are untouched.  The r34 source has this exact
    # seven-assignment block immediately after ``OUT = ...``.
    block = re.compile(
        r"(?ms)^    ACTIVE_PREDECESSOR_SUPERSESSION\s*=.*?\n"
        r"^    ACTIVE_REJECTED_RETRY_SUPERSESSION\s*=.*?\n"
        r"^    ACTIVE_EXACT8_FIRST_MEMBER\s*=.*?\n"
        r"^    ACTIVE_SUCCESSOR_NAMESPACE\s*=.*?\n"
        r"^    ACTIVE_SUCCESSOR_NAMESPACE_TAG\s*=.*?\n"
        r"^    ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN\s*=.*?\n"
        r"^    ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN\s*=.*?\n")
    text, count = block.subn("", text, count=1)
    if count != 1:
        raise RuntimeError(f"r39 launcher active block count:{count}")
    return text


def _fixed_launcher_globals(text: str, anchor_file: str,
                            anchor_object: str) -> str:
    # The source already has the global declaration and one block.  Remove the
    # function-local assignments only; the audited r34 injector then adds one
    # target block and performs its historical-BASE/path checks.
    return original_launcher_globals(
        _strip_config_active_block(text), anchor_file, anchor_object)


original_launcher_globals = None


def prepare(module: ModuleType) -> None:
    global original_launcher_globals
    inner = module.load_r34_module()
    original_launcher_globals = inner.launcher_globals
    inner.replace_checkpoint_loads = _fixed_loads
    inner.source_paths = _fixed_paths
    inner.launcher_globals = _fixed_launcher_globals

    # The outer r35 wrapper must keep using this patched inner module.  Its
    # generic loader otherwise returns an unpatched r19 builder and silently
    # loses the source/JSON gates.
    original_generic = inner.load_generic

    def load_generic_patched():
        builder = original_generic()
        builder.retag = inner.retag
        builder.source_patch = inner.source_patch
        return builder

    inner.load_generic = load_generic_patched
    module.install_retag(inner)
    module.load_r34_module = lambda: inner


def main() -> int:
    module = load_outer()
    prepare(module)
    return int(module.main())


if __name__ == "__main__":
    raise SystemExit(main())
