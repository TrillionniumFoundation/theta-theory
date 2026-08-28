#!/usr/bin/env python3
"""Append-only r63ar successor of the r63aq recipe.

The r63aq runtime reached the second authorize phase but its projected
current-later-rejection carried the historical v8 commit-operation spelling.
This successor preserves every r63aq byte and publication path, retags into a
new namespace, and changes only that schema-facing constant.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts/c79g_v16r2r63aq_runtime_bundle_builder.py"
TEMPLATE_SHA256 = "b27e3f7ff57ffb949099cb2a50b17b584da0ed3e834b4ce95e3ac1abac7ce774"


def main(argv: list[str] | None = None) -> int:
    raw = TEMPLATE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != TEMPLATE_SHA256:
        raise RuntimeError("immutable r63aq builder template hash drift")
    # First retag the already-corrected wrapper.  Its nested r63ap recipe is
    # still hash-pinned; only the generated successor namespace is new.
    text = raw.decode("utf-8").replace("r63aq", "r63ar").replace("R63AQ", "R63AR")
    needle = 'text = raw.decode("utf-8").replace("r63ap", "r63ar").replace("R63AP", "R63AR")'
    replacement = (
        'text = raw.decode("utf-8").replace("r63ap", "r63ar").replace("R63AP", "R63AR")\n'
        '    text = text.replace("O_CREAT_EXCL_FIXED_TARGET_NO_FALLBACK",\n'
        '                        "O_CREAT_O_EXCL_FIXED_TARGET_NO_FALLBACK")'
    )
    if text.count(needle) != 1:
        raise RuntimeError("r63ar retag insertion anchor drift")
    text = text.replace(needle, replacement, 1)
    ns = {
        "__name__": "_c79g_r63ar_builder_template",
        "__file__": str(ROOT / "scripts/c79g_v16r2r63ar_runtime_bundle_builder.py"),
    }
    exec(compile(text, str(TEMPLATE), "exec"), ns, ns)
    return int(ns["main"](sys.argv[1:] if argv is None else argv))


if __name__ == "__main__":
    raise SystemExit(main())
