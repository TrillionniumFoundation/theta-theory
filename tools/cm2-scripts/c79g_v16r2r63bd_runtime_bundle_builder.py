#!/usr/bin/env python3
"""Append-only r63bd successor of the correctly serialized r63bc recipe.

r63bc's cold build was invoked once with a relative output path and therefore
failed closed before any candidate write.  Its source bytes and rejection are
immutable.  This wrapper only advances the physical successor tag and pins
r63bc as the immediate rejected predecessor; the pre-encode strict-bool fix
and declared/physical seal split are inherited unchanged.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts/c79g_v16r2r63bc_runtime_bundle_builder.py"
TEMPLATE_SHA256 = (
    "89c9fe2d903eb34a62d34956337aa5d6c7ad5c0caee76be428369db463fe43ec"
)
PREDECESSOR_REJECTION = ROOT / (
    ".cm2-runtime/c79g-v16r2r63bc-rejections-"
    "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab/rejection.json"
)
PREDECESSOR_REJECTION_SHA256 = (
    "4a08d0b545b9d0730239a157f7d742364a37dee57c187dc9aa72a86159e6eb85"
)


def main(argv: list[str] | None = None) -> int:
    raw = TEMPLATE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != TEMPLATE_SHA256:
        raise RuntimeError("immutable r63bc builder template hash drift")
    if (not PREDECESSOR_REJECTION.is_file() or
            hashlib.sha256(PREDECESSOR_REJECTION.read_bytes()).hexdigest() !=
            PREDECESSOR_REJECTION_SHA256):
        raise RuntimeError("r63bc official rejection history is missing or mutated")

    text = raw.decode("utf-8").replace("r63bc", "r63bd").replace("R63BC", "R63BD")
    old_path_fragment = "r63bb-rejections-"
    if text.count(old_path_fragment) != 2:
        raise RuntimeError("r63bd predecessor path anchor drift")
    text = text.replace(old_path_fragment, "r63bc-rejections-", 2)
    old_hash = "7d701b98eb5ad7bc30ba3b49242f12b773d4970ed92a7486ac823e78a9644d93"
    if text.count(old_hash) != 1:
        raise RuntimeError("r63bd predecessor hash anchor drift")
    text = text.replace(old_hash, PREDECESSOR_REJECTION_SHA256, 1)
    ns = {
        "__name__": "_c79g_r63bd_builder_template",
        "__file__": str(ROOT / "scripts/c79g_v16r2r63bd_runtime_bundle_builder.py"),
    }
    exec(compile(text, str(TEMPLATE), "exec"), ns, ns)
    return int(ns["main"](sys.argv[1:] if argv is None else argv))


if __name__ == "__main__":
    raise SystemExit(main())
