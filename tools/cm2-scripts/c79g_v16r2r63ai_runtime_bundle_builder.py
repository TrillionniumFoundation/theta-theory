#!/usr/bin/env python3
"""Construct the append-only r63ai successor with contract stage alignment.

The r63ah successor restored the consumer's generic authority-stage prefix,
but its contract construction still retained the retagged r63ah path.  This
wrapper keeps r63ah immutable and injects the same generic-stage rewrite into
the base builder immediately after runtime-target retagging and before object
closure.
"""
from __future__ import annotations

import builtins
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts/c79g_v16r2r63ah_runtime_bundle_builder.py"
TEMPLATE_SHA256 = "5b6ebcd039faa0464fd8e33524abf745bb86eef64bb163e22f68e057cc0df5b7"


def main(argv: list[str] | None = None) -> int:
    raw = TEMPLATE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != TEMPLATE_SHA256:
        raise RuntimeError("immutable r63ah builder template hash drift")

    # Every nested successor loader eventually calls compile() on the base
    # builder source.  Intercept that process-wide call briefly so the
    # contract rewrite is applied at the actual construction point (before
    # contract_raw/object_sha256 are sealed), regardless of loader depth.
    real_compile = builtins.compile
    anchor = "    contract_value = retag_json_runtime_targets(contract_value)\n"
    old_stage = ".c79g-v16r2r63ai-authority-stage-"
    new_stage = ".c79g-v16r2-authority-stage-"
    marker = "_R63AI_STAGE_PATCH_APPLIED_"
    helper = (
        f"    # {marker}\n"
        "    def _r63ai_stage_json(value):\n"
        "        if isinstance(value, dict):\n"
        "            return {key: _r63ai_stage_json(item) for key, item in value.items()}\n"
        "        if isinstance(value, list):\n"
        "            return [_r63ai_stage_json(item) for item in value]\n"
        "        if isinstance(value, str):\n"
        f"            return value.replace({old_stage!r}, {new_stage!r})\n"
        "        return value\n"
        "    contract_value = _r63ai_stage_json(contract_value)\n"
    )

    def patched_compile(source, filename, mode, *args, **kwargs):
        source_is_bytes = isinstance(source, (bytes, bytearray))
        if source_is_bytes:
            source_text = bytes(source).decode("utf-8")
        elif isinstance(source, str):
            source_text = source
        else:
            return real_compile(source, filename, mode, *args, **kwargs)
        # The base builder is the only compiled source with both this exact
        # construction anchor and its construct function.  Wrapper literals
        # containing the anchor are therefore excluded safely.
        if ("def construct() -> tuple[dict[str, bytes], dict[str, Any]]:" in source_text
                and source_text.count(anchor) == 1
                and marker not in source_text):
            source_text = source_text.replace(anchor, helper + anchor, 1)
            source = source_text.encode("utf-8") if source_is_bytes else source_text
        return real_compile(source, filename, mode, *args, **kwargs)

    builtins.compile = patched_compile
    try:
        text = raw.decode("utf-8").replace("r63ah", "r63ai")
        ns = {
            "__name__": "_c79g_r63ai_builder_template",
            "__file__": str(ROOT / "scripts/c79g_v16r2r63ai_runtime_bundle_builder.py"),
        }
        exec(real_compile(text, str(TEMPLATE), "exec"), ns, ns)
        return int(ns["main"](sys.argv[1:] if argv is None else argv))
    finally:
        builtins.compile = real_compile


if __name__ == "__main__":
    raise SystemExit(main())
