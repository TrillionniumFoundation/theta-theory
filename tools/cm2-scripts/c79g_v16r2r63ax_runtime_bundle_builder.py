#!/usr/bin/env python3
"""Append-only r63ax successor, preserving the r63aw build rejection."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts/c79g_v16r2r63aw_runtime_bundle_builder.py"
TEMPLATE_SHA256 = "6164c5a3ad7f1605993d77978a128868281fe4ba60072bc231ea68b27b6c9f13"
PREDECESSOR_REJECTIONS = (
    (ROOT / ".cm2-runtime/c79g-v16r2r63av-rejections-"
     "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab/rejection.json",
     "a2c26a1bfadd055393bd2299ebec14e898da492cae9121eab5d64d547fa132d7"),
    (ROOT / ".cm2-runtime/c79g-v16r2r63aw-rejections-"
     "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab/rejection.json",
     "e9f35bcaa5aa4b710b1f34be71e296019685217708ff2a8e5edb0a7560b98af9"),
)


def main(argv: list[str] | None = None) -> int:
    raw = TEMPLATE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != TEMPLATE_SHA256:
        raise RuntimeError("immutable r63aw builder template hash drift")
    for path, expected in PREDECESSOR_REJECTIONS:
        if (not path.is_file() or
                hashlib.sha256(path.read_bytes()).hexdigest() != expected):
            raise RuntimeError("predecessor rejection history is missing or mutated:" + str(path))
    text = raw.decode("utf-8").replace("r63aw", "r63ax").replace("R63AW", "R63AX")
    ns = {
        "__name__": "_c79g_r63ax_builder_template",
        "__file__": str(ROOT / "scripts/c79g_v16r2r63ax_runtime_bundle_builder.py"),
    }
    exec(compile(text, str(TEMPLATE), "exec"), ns, ns)
    return int(ns["main"](sys.argv[1:] if argv is None else argv))


if __name__ == "__main__":
    raise SystemExit(main())
