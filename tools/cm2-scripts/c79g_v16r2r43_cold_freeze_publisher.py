#!/usr/bin/env python3
"""r43 exact8 -> manifest -> outer-last publisher entrypoint."""
from __future__ import annotations

import argparse
import ast
from pathlib import Path
import sys
from types import ModuleType

sys.dont_write_bytecode = True
_PATH = Path(__file__).with_name("c79g_v16r2r43_cold_freeze_adapter.py")
_MOD = ModuleType("_r43_publisher_adapter")
_MOD.__file__ = str(_PATH)
_MOD.__package__ = None
exec(compile(ast.parse(_PATH.read_text(encoding="utf-8"), str(_PATH), "exec"),
             str(_PATH), "exec"), _MOD.__dict__, _MOD.__dict__)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args(argv)
    if not args.publish:
        parser.error("--publish is required")
    return _MOD.publisher_entrypoint(args.config, True)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"R43_PUBLISHER_REFUSED: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(2)
