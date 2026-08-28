#!/usr/bin/env python3
"""Append-only r63ao successor built from the frozen r63an repair recipe.

The r63an install was closed with an official zero-credit rejection after a
post-preflight source-anchor correction.  This wrapper keeps that recipe
immutable, retags only the new publication namespace, and lets the builder's
own NOREPLACE installer mint a fresh successor surface.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts/c79g_v16r2r63an_runtime_bundle_builder.py"
TEMPLATE_SHA256 = "c60a91849ef31a119eab5923e96ba0d7e8501c56096a49509d9728eeae7a1de0"


def main(argv: list[str] | None = None) -> int:
    raw = TEMPLATE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != TEMPLATE_SHA256:
        raise RuntimeError("immutable r63an builder template hash drift")
    # Retag the successor only.  The nested r63am template pin and all
    # historical bytes remain checked by the r63an recipe itself.
    text = raw.decode("utf-8").replace("r63an", "r63ao").replace("R63AN", "R63AO")
    ns = {
        "__name__": "_c79g_r63ao_builder_template",
        "__file__": str(ROOT / "scripts/c79g_v16r2r63ao_runtime_bundle_builder.py"),
    }
    exec(compile(text, str(TEMPLATE), "exec"), ns, ns)
    return int(ns["main"](sys.argv[1:] if argv is None else argv))


if __name__ == "__main__":
    raise SystemExit(main())
