#!/usr/bin/env python3
"""Append-only r63aw successor of the terminal r63av cold probe.

r63av's zero-credit rejection is a historical input, never a writable target.
This wrapper pins that rejection before delegating to the immutable r63av
recipe, retagging only the new physical namespace to r63aw.  The inherited
declared/physical projection and all v4/v6/v7/v10 repairs are retained.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts/c79g_v16r2r63av_runtime_bundle_builder.py"
TEMPLATE_SHA256 = "7a0fcca1907071f8fc7d9d746b3c176b4d88747dbc4e1755b5955ff635f8e4f9"
PREDECESSOR_REJECTION = ROOT / (
    ".cm2-runtime/c79g-v16r2r63av-rejections-"
    "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab/rejection.json")
PREDECESSOR_REJECTION_SHA256 = (
    "a2c26a1bfadd055393bd2299ebec14e898da492cae9121eab5d64d547fa132d7")


def main(argv: list[str] | None = None) -> int:
    raw = TEMPLATE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != TEMPLATE_SHA256:
        raise RuntimeError("immutable r63av builder template hash drift")
    if (not PREDECESSOR_REJECTION.is_file() or
            hashlib.sha256(PREDECESSOR_REJECTION.read_bytes()).hexdigest() !=
            PREDECESSOR_REJECTION_SHA256):
        raise RuntimeError("r63av official rejection history is missing or mutated")
    text = raw.decode("utf-8").replace("r63av", "r63aw").replace("R63AV", "R63AW")
    ns = {
        "__name__": "_c79g_r63aw_builder_template",
        "__file__": str(ROOT / "scripts/c79g_v16r2r63aw_runtime_bundle_builder.py"),
    }
    exec(compile(text, str(TEMPLATE), "exec"), ns, ns)
    return int(ns["main"](sys.argv[1:] if argv is None else argv))


if __name__ == "__main__":
    raise SystemExit(main())
