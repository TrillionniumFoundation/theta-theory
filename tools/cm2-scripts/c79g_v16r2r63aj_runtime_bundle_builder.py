#!/usr/bin/env python3
"""Construct r63aj with the final authority-stage contract binding repair.

The r63ai runtime consumer uses the schema's generic authority staging path,
but the inherited JSON contract still carried the retagged path in one field
that is reconstructed after the first rewrite.  This append-only successor
adds an explicit field assignment at the base builder's pre-closure point.
"""
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
    text = raw.decode("utf-8").replace("r63ai", "r63aj")
    old = '        "    contract_value = _r63aj_stage_json(contract_value)\\n"\n'
    new = (
        old
        + '        "    _r63aj_paths = contract_value.get(\\"exact_publication_paths\\")\\n"\n'
        + '        "    if isinstance(_r63aj_paths, dict):\\n"\n'
        + '        "        _r63aj_paths[\\"authority_staging_path\\"] = (\\n"\n'
        + '        "            \\".cm2-runtime/cm2-global-authority-heads/.c79g-v16r2-authority-stage-\\" + CHECKPOINT + \\".seal\\")\\n"\n'
        + '        "        _r63aj_paths[\\"authority_staging_prefix\\"] = \\".cm2-runtime/cm2-global-authority-heads/.c79g-v16r2-authority-stage-\\"\\n"\n'
    )
    if text.count(old) != 1:
        raise RuntimeError("r63aj stage-helper anchor drift")
    text = text.replace(old, new, 1)
    ns = {
        "__name__": "_c79g_r63aj_builder_template",
        "__file__": str(ROOT / "scripts/c79g_v16r2r63aj_runtime_bundle_builder.py"),
    }
    exec(compile(text, str(TEMPLATE), "exec"), ns, ns)
    return int(ns["main"](sys.argv[1:] if argv is None else argv))


if __name__ == "__main__":
    raise SystemExit(main())
