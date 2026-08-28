#!/usr/bin/env python3
"""Construct the append-only r63y successor of the failed r63x build."""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts/c79g_v16r2r63x_runtime_bundle_builder.py"
TEMPLATE_SHA256 = "1c7fda53ef0370b9c34638ae570fc1738331790563e690d14e681368e34b16e2"


def main(argv: list[str] | None = None) -> int:
    raw = TEMPLATE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != TEMPLATE_SHA256:
        raise RuntimeError("immutable r63x builder template hash drift")
    # Retag the already-corrected in-memory recipe to a fresh namespace.  It
    # still pins and reads the original immutable r62 witnesses; x artifacts
    # remain untouched evidence and y is written with O_EXCL only.
    text = raw.decode("utf-8").replace("r63x", "r63y")
    ns = {
        "__name__": "_c79g_r63y_builder_template",
        "__file__": str(ROOT / "scripts/c79g_v16r2r63y_runtime_bundle_builder.py"),
    }
    exec(compile(text, str(TEMPLATE), "exec"), ns, ns)
    return int(ns["main"](sys.argv[1:] if argv is None else argv))


if __name__ == "__main__":
    raise SystemExit(main())
