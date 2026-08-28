#!/usr/bin/env python3
"""Append-only r63aq successor of the corrected r63ap recipe.

r63ap's first install occupied its deliverable names before the static-freeze
projection correction was finalized.  This wrapper leaves that historical
bundle untouched and retags the corrected recipe into a fresh r63aq namespace.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts/c79g_v16r2r63ap_runtime_bundle_builder.py"
TEMPLATE_SHA256 = "17e6f8736b079f3833b94c9a924a30d1fd90c0306889633420eb26b819cd5b14"


def main(argv: list[str] | None = None) -> int:
    raw = TEMPLATE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != TEMPLATE_SHA256:
        raise RuntimeError("immutable corrected r63ap builder template hash drift")
    text = raw.decode("utf-8").replace("r63ap", "r63aq").replace("R63AP", "R63AQ")
    ns = {
        "__name__": "_c79g_r63aq_builder_template",
        "__file__": str(ROOT / "scripts/c79g_v16r2r63aq_runtime_bundle_builder.py"),
    }
    exec(compile(text, str(TEMPLATE), "exec"), ns, ns)
    return int(ns["main"](sys.argv[1:] if argv is None else argv))


if __name__ == "__main__":
    raise SystemExit(main())
