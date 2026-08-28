#!/usr/bin/env python3
"""Fail-closed r40 exact8 -> manifest -> outer-last publisher entrypoint.

No action occurs without both ``--config PATH --publish`` and the exact
``CM2_R40_PUBLISH_ACK=EXACT8_MANIFEST_OUTER_LAST`` environment token.  The
implementation itself is loaded in memory by the adapter; its publication
descriptor is O_RDWR so same-FD terminal replay cannot raise EBADF.
"""
from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import sys

_ADAPTER_PATH = Path(__file__).with_name("c79g_v16r2r40_cold_freeze_adapter.py")
_SPEC = importlib.util.spec_from_file_location("_r40_adapter_publisher_entry", _ADAPTER_PATH)
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError("cannot load r40 adapter")
_ADAPTER = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _ADAPTER
_SPEC.loader.exec_module(_ADAPTER)
publisher_entrypoint = _ADAPTER.publisher_entrypoint


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args(argv)
    if not args.publish:
        parser.error("--publish is required")
    return publisher_entrypoint(args.config, True)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"R40_PUBLISHER_REFUSED: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(2)
