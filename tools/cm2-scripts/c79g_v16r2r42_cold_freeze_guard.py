#!/usr/bin/env python3
"""r42 read-only cold-freeze guard entrypoint."""
from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import sys

_PATH = Path(__file__).with_name("c79g_v16r2r42_cold_freeze_adapter.py")
_SPEC = importlib.util.spec_from_file_location("_r42_guard_adapter", _PATH)
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError("r42 adapter unavailable")
_MOD = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _MOD
_SPEC.loader.exec_module(_MOD)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--preflight", action="store_true")
    args = parser.parse_args(argv)
    # The inherited publisher's in-memory ``run_guard`` invokes the guard
    # with only ``--config``.  Treat the omitted flag as the same read-only
    # preflight, while still accepting the explicit operator spelling.
    return _MOD.guard_entrypoint(args.config, ["--preflight"])


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"R42_GUARD_REFUSED: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(2)
