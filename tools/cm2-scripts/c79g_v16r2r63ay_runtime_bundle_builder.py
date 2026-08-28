#!/usr/bin/env python3
"""Append-only r63ay successor fixing the cold-proof v10 rejection projection.

The r63ax surface and its official rejection remain immutable.  This wrapper
changes only the schema-facing launcher proof member: historical v10 evidence
is retained, while the serialized ``official_v10_later_rejection`` member is
projected to the frozen exact rejection object required by the current schema.
"""
from __future__ import annotations

import builtins
import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts/c79g_v16r2r63ax_runtime_bundle_builder.py"
TEMPLATE_SHA256 = "67728c720b28793e74d629ec983ce07805b7906327e5215c0df4553694e451bd"
PREDECESSOR_REJECTION = ROOT / (
    ".cm2-runtime/c79g-v16r2r63ax-rejections-"
    "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab/rejection.json")
PREDECESSOR_REJECTION_SHA256 = (
    "ae56a8dcfc49523268af01b221ce5eb220019b97e44c1e47a4d80036f8269959")
MARKER = "_R63AY_COLD_V10_REJECTION_SCHEMA_PROJECTION_APPLIED_"


def _patch_base_source(source_text: str) -> str:
    if MARKER in source_text:
        return source_text
    if "def construct() -> tuple[dict[str, bytes], dict[str, Any]]:" not in source_text:
        return source_text
    launcher_anchor = '    launcher_raw = launcher_text.encode("utf-8")\n'
    if source_text.count(launcher_anchor) != 2:
        return source_text
    helper = '''    # _R63AY_COLD_V10_REJECTION_SCHEMA_PROJECTION_APPLIED_
    _r63ay_v10_old = ("'official_v10_later_rejection': "
                      "{'path': str(V10_OFFICIAL_REJECTION.relative_to(ROOT)), "
                      "'namespace_path': str(V10_OFFICIAL_REJECTION.parent.relative_to(ROOT)), "
                      "'file_sha256': V10_REJECTION_FILE_PIN, "
                      "'object_sha256': V10_REJECTION_OBJECT_PIN},")
    _r63ay_v10_new = ("'official_v10_later_rejection': "
                      "expected_v10_published_rejected_segment()['official_later_rejection'],")
    if launcher_text.count(_r63ay_v10_old) != 1:
        raise RuntimeError("r63ay official-v10 schema projection anchor drift")
    launcher_text = launcher_text.replace(_r63ay_v10_old, _r63ay_v10_new, 1)
'''
    return source_text.replace(launcher_anchor, helper + launcher_anchor)


def main(argv: list[str] | None = None) -> int:
    raw = TEMPLATE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != TEMPLATE_SHA256:
        raise RuntimeError("immutable r63ax builder template hash drift")
    if (not PREDECESSOR_REJECTION.is_file() or
            hashlib.sha256(PREDECESSOR_REJECTION.read_bytes()).hexdigest() !=
            PREDECESSOR_REJECTION_SHA256):
        raise RuntimeError("r63ax official rejection history is missing or mutated")
    text = raw.decode("utf-8").replace("r63ax", "r63ay").replace("R63AX", "R63AY")
    real_compile = builtins.compile

    def patched_compile(source, filename, mode, *args, **kwargs):
        source_is_bytes = isinstance(source, (bytes, bytearray))
        if source_is_bytes:
            source_text = bytes(source).decode("utf-8")
        elif isinstance(source, str):
            source_text = source
        else:
            return real_compile(source, filename, mode, *args, **kwargs)
        if MARKER not in source_text:
            patched = _patch_base_source(source_text)
            if patched != source_text:
                source = patched.encode("utf-8") if source_is_bytes else patched
        return real_compile(source, filename, mode, *args, **kwargs)

    builtins.compile = patched_compile
    try:
        ns = {
            "__name__": "_c79g_r63ay_builder_template",
            "__file__": str(ROOT / "scripts/c79g_v16r2r63ay_runtime_bundle_builder.py"),
        }
        exec(real_compile(text, str(TEMPLATE), "exec"), ns, ns)
        return int(ns["main"](sys.argv[1:] if argv is None else argv))
    finally:
        builtins.compile = real_compile


if __name__ == "__main__":
    raise SystemExit(main())
