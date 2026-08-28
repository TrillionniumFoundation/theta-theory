#!/usr/bin/env python3
"""Fail-closed r40 guard entrypoint for the parameterised adapter.

The candidate-specific guard is compiled in memory from the pinned r39/r34
templates.  It accepts only ``--config PATH --preflight`` and emits no file.
"""
from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import sys

_ADAPTER_PATH = Path(__file__).with_name("c79g_v16r2r40_cold_freeze_adapter.py")
_SPEC = importlib.util.spec_from_file_location("_r40_adapter_guard_entry", _ADAPTER_PATH)
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError("cannot load r40 adapter")
_ADAPTER = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _ADAPTER
_SPEC.loader.exec_module(_ADAPTER)
guard_entrypoint = _ADAPTER.guard_entrypoint


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--preflight", action="store_true")
    args = parser.parse_args(argv)
    if not args.preflight:
        parser.error("--preflight is required")
    return guard_entrypoint(args.config, ["--preflight"])


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"R40_GUARD_REFUSED: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(2)
