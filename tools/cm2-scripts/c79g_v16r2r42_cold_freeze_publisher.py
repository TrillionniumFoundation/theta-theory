#!/usr/bin/env python3
"""r42 exact8 -> manifest -> outer-last publisher entrypoint."""
from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import sys

_PATH = Path(__file__).with_name("c79g_v16r2r42_cold_freeze_adapter.py")
_SPEC = importlib.util.spec_from_file_location("_r42_publisher_adapter", _PATH)
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError("r42 adapter unavailable")
_MOD = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _MOD
_SPEC.loader.exec_module(_MOD)


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
        print(f"R42_PUBLISHER_REFUSED: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(2)
