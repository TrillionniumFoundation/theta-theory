#!/usr/bin/env python3
"""Construct r63ak with post-retag authority staging-path closure."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts/c79g_v16r2r63ai_runtime_bundle_builder.py"
TEMPLATE_SHA256 = "a6ee544e746154701f36a5c49e8d7b7c995a627989dbdd1f21153425a3cab91e"


def main(argv: list[str] | None = None) -> int:
    raw = TEMPLATE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != TEMPLATE_SHA256:
        raise RuntimeError("immutable r63ai builder template hash drift")
    text = raw.decode("utf-8").replace("r63ai", "r63ak")

    # Make the injected helper run after the base builder's retag operation.
    # The explicit assignment is therefore the final value before contract
    # object closure, independent of which intermediate prefix was present.
    old_helper_line = '        "    contract_value = _r63ak_stage_json(contract_value)\\n"\n'
    new_helper_line = (
        old_helper_line
        + '        "    _r63ak_paths = contract_value.get(\\"exact_publication_paths\\")\\n"\n'
        + '        "    if isinstance(_r63ak_paths, dict):\\n"\n'
        + '        "        _r63ak_paths[\\"authority_staging_path\\"] = (\\n"\n'
        + '        "            \\".cm2-runtime/cm2-global-authority-heads/.c79g-v16r2-authority-stage-\\" + CHECKPOINT + \\".seal\\")\\n"\n'
        + '        "        _r63ak_paths[\\"authority_staging_prefix\\"] = \\".cm2-runtime/cm2-global-authority-heads/.c79g-v16r2-authority-stage-\\"\\n"\n'
    )
    if text.count(old_helper_line) != 1:
        raise RuntimeError("r63ak helper anchor drift")
    text = text.replace(old_helper_line, new_helper_line, 1)
    old_insert = "            source_text = source_text.replace(anchor, helper + anchor, 1)\n"
    new_insert = "            source_text = source_text.replace(anchor, anchor + helper, 1)\n"
    if text.count(old_insert) != 1:
        raise RuntimeError("r63ak post-retag insertion anchor drift")
    text = text.replace(old_insert, new_insert, 1)

    ns = {
        "__name__": "_c79g_r63ak_builder_template",
        "__file__": str(ROOT / "scripts/c79g_v16r2r63ak_runtime_bundle_builder.py"),
    }
    exec(compile(text, str(TEMPLATE), "exec"), ns, ns)
    return int(ns["main"](sys.argv[1:] if argv is None else argv))


if __name__ == "__main__":
    raise SystemExit(main())
