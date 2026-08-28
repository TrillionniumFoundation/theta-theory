#!/usr/bin/env python3
"""Construct r63ah with an explicit contract/schema stage-path repair.

The r63ag consumer was correctly restored to the generic authority-stage
spelling, but its derived contract still advertised the retagged r63ag stage.
This successor keeps r63ag immutable and patches the base builder's contract
object before its hash closure, so the contract, consumer, and frozen schema
agree byte-for-byte on the stage path.
"""
from __future__ import annotations

import builtins
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts/c79g_v16r2r63ag_runtime_bundle_builder.py"
TEMPLATE_SHA256 = "25b4811a7705a811ad5685724a2efa2f6204d0a50a66860b482eb0fee5db579c"


def main(argv: list[str] | None = None) -> int:
    raw = TEMPLATE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != TEMPLATE_SHA256:
        raise RuntimeError("immutable r63ag builder template hash drift")
    text = raw.decode("utf-8").replace("r63ag", "r63ah")

    real_compile = builtins.compile
    anchor = "    contract_value = retag_json_runtime_targets(contract_value)\n"
    old_stage = ".c79g-v16r2r63ah-authority-stage-"
    new_stage = ".c79g-v16r2-authority-stage-"
    helper = (
        "    def _r63ah_stage_json(value):\n"
        "        if isinstance(value, dict):\n"
        "            return {key: _r63ah_stage_json(item) for key, item in value.items()}\n"
        "        if isinstance(value, list):\n"
        "            return [_r63ah_stage_json(item) for item in value]\n"
        "        if isinstance(value, str):\n"
        f"            return value.replace({old_stage!r}, {new_stage!r})\n"
        "        return value\n"
        "    contract_value = _r63ah_stage_json(contract_value)\n"
    )

    def patched_compile(source, filename, mode, *args, **kwargs):
        if isinstance(source, str) and source.count(anchor) == 1 and \
                "RUNTIME_TARGET_PREFIX_NEW = \"c79g-v16r2r63ah-\"" in source:
            source = source.replace(anchor, helper + anchor, 1)
        return real_compile(source, filename, mode, *args, **kwargs)

    ns = {
        "__name__": "_c79g_r63ah_builder_template",
        "__file__": str(ROOT / "scripts/c79g_v16r2r63ah_runtime_bundle_builder.py"),
        "compile": patched_compile,
    }
    exec(patched_compile(text, str(TEMPLATE), "exec"), ns, ns)
    return int(ns["main"](sys.argv[1:] if argv is None else argv))


if __name__ == "__main__":
    raise SystemExit(main())
