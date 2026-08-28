#!/usr/bin/env python3
"""Append-only r63ba successor fixing v6/v7 cold-proof projections.

The r63az surface and its official rejection remain immutable.  This wrapper
rebuilds the same two schema-facing projections from the immutable r63ay
builder while pinning r63az as the immediate rejected predecessor.
"""
from __future__ import annotations

import builtins
import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts/c79g_v16r2r63ay_runtime_bundle_builder.py"
TEMPLATE_SHA256 = "f22ee2f001714e6048f2c01d11dcad89f7795fd00c5c22988796be939d660bed"
PREDECESSOR_REJECTION = ROOT / (
    ".cm2-runtime/c79g-v16r2r63az-rejections-"
    "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab/rejection.json")
PREDECESSOR_REJECTION_SHA256 = (
    "8ae9547c070bd9d16a552e30f920fdb24a85c2c158d80f50d56e9d71c6d5adb4")
MARKER = "_R63BA_COLD_V6_V7_REJECTION_SCHEMA_PROJECTIONS_APPLIED_"


def _patch_base_source(source_text: str) -> str:
    if MARKER in source_text:
        return source_text
    if "def construct() -> tuple[dict[str, bytes], dict[str, Any]]:" not in source_text:
        return source_text
    launcher_anchor = '    launcher_raw = launcher_text.encode("utf-8")\n'
    if source_text.count(launcher_anchor) != 2:
        return source_text
    helper = '''    # _R63BA_COLD_V6_V7_REJECTION_SCHEMA_PROJECTIONS_APPLIED_
    _r63ba_v7_old = ("'official_v7_later_rejection': "
                     "{'path': str(V7_OFFICIAL_REJECTION.relative_to(ROOT)), "
                     "'namespace_path': str(V7_OFFICIAL_REJECTION.parent.relative_to(ROOT)), "
                     "'file_sha256': V7_REJECTION_FILE_PIN, "
                     "'object_sha256': V7_REJECTION_OBJECT_PIN},")
    _r63ba_v7_new = ("'official_v7_later_rejection': "
                     "expected_v7_published_rejected_segment()['official_later_rejection'],")
    _r63ba_v6_old = ("'official_v6_later_rejection': "
                     "{'path': str(V6_OFFICIAL_REJECTION.relative_to(ROOT)), "
                     "'namespace_path': str(V6_OFFICIAL_REJECTION.parent.relative_to(ROOT)), "
                     "'file_sha256': V6_REJECTION_FILE_PIN, "
                     "'object_sha256': V6_REJECTION_OBJECT_PIN},")
    _r63ba_v6_new = ("'official_v6_later_rejection': "
                     "expected_v6_published_rejected_segment()['official_later_rejection'],")
    for _old, _new, _label in ((_r63ba_v7_old, _r63ba_v7_new, "v7"),
                               (_r63ba_v6_old, _r63ba_v6_new, "v6")):
        if launcher_text.count(_old) != 1:
            raise RuntimeError("r63ba official-" + _label + " schema projection anchor drift")
        launcher_text = launcher_text.replace(_old, _new, 1)
'''
    return source_text.replace(launcher_anchor, helper + launcher_anchor)


def main(argv: list[str] | None = None) -> int:
    raw = TEMPLATE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != TEMPLATE_SHA256:
        raise RuntimeError("immutable r63ay builder template hash drift")
    if (not PREDECESSOR_REJECTION.is_file() or
            hashlib.sha256(PREDECESSOR_REJECTION.read_bytes()).hexdigest() !=
            PREDECESSOR_REJECTION_SHA256):
        raise RuntimeError("r63az official rejection history is missing or mutated")
    text = raw.decode("utf-8").replace("r63ay", "r63ba").replace("R63AY", "R63BA")
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
            "__name__": "_c79g_r63ba_builder_template",
            "__file__": str(ROOT / "scripts/c79g_v16r2r63ba_runtime_bundle_builder.py"),
        }
        exec(real_compile(text, str(TEMPLATE), "exec"), ns, ns)
        return int(ns["main"](sys.argv[1:] if argv is None else argv))
    finally:
        builtins.compile = real_compile


if __name__ == "__main__":
    raise SystemExit(main())
