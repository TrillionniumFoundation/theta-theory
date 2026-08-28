#!/usr/bin/env python3
"""r46 read-only cold-freeze guard entrypoint."""
from __future__ import annotations
import argparse
import ast
from pathlib import Path
import sys
from types import ModuleType

sys.dont_write_bytecode = True
_path = Path(__file__).with_name("c79g_v16r2r46_cold_freeze_adapter.py")
_mod = ModuleType("_r46_guard_adapter")
_mod.__file__ = str(_path)
_mod.__package__ = None
exec(compile(ast.parse(_path.read_text(encoding="utf-8"), str(_path), "exec"),
             str(_path), "exec"), _mod.__dict__, _mod.__dict__)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--preflight", action="store_true")
    args = parser.parse_args(argv)
    return _mod.guard_entrypoint(args.config, ["--preflight"])


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"R46_GUARD_REFUSED: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(2)
