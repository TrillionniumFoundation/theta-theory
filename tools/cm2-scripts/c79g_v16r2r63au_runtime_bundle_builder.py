#!/usr/bin/env python3
"""Append-only r63au successor correcting the live v10 pin projection.

r63at passed the static surface, both cold verification routes, the 137
fail-closed attack set, and terminal assemble replay.  Its second authorize
was nevertheless rejected by the closed schema because the cold-root
``live_v10_exact10_ordered_pins`` witness was serialized from the raw pin
tuples (path/file/object only) instead of the frozen schema-facing exact10
objects (which also carry the stable role ``name``).  This successor leaves
all r63at bytes and its rejection immutable, and changes only that
schema-facing launcher projection before the launcher is hashed.
"""
from __future__ import annotations

import builtins
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts/c79g_v16r2r63at_runtime_bundle_builder.py"
TEMPLATE_SHA256 = (
    "e12d59af176ebb098cd55b832f380069d19b02ec900ed6adcb441fb18a44765b"
)
MARKER = "_R63AU_LIVE_V10_SCHEMA_PROJECTION_APPLIED_"

# These are the three launcher expressions whose closed-schema definitions are
# exact constants.  v3/v5 are deliberately left as raw prefix witnesses.  The
# expected_* helpers already construct the frozen named objects in the exact
# historical order, so no raw pin/path/descriptor bytes are changed.
LIVE_PROJECTIONS = (
    (
        "'live_v6_exact10_ordered_pins': "
        "[{'path': str(path.relative_to(ROOT)), 'file_sha256': file_pin, "
        "**({'object_sha256': object_pin} if object_pin is not None else {})} "
        "for path, file_pin, object_pin in V6_EXACT10_PINS],",
        "'live_v6_exact10_ordered_pins': "
        "expected_v6_published_rejected_segment()['ordered_published_exact10'],",
    ),
    (
        "'live_v7_exact10_ordered_pins': "
        "[{'path': str(path.relative_to(ROOT)), 'file_sha256': file_pin, "
        "**({'object_sha256': object_pin} if object_pin is not None else {})} "
        "for path, file_pin, object_pin in V7_EXACT10_PINS],",
        "'live_v7_exact10_ordered_pins': "
        "expected_v7_published_rejected_segment()['ordered_published_exact10'],",
    ),
    (
        "'live_v10_exact10_ordered_pins': "
        "[{'path': str(path.relative_to(ROOT)), 'file_sha256': file_pin, "
        "**({'object_sha256': object_pin} if object_pin is not None else {})} "
        "for path, file_pin, object_pin in V10_EXACT10_PINS],",
        "'live_v10_exact10_ordered_pins': "
        "expected_v10_published_rejected_segment()['ordered_published_exact10'],",
    ),
)


def _patch_base_source(source_text: str) -> str:
    """Inject the projection into the actual launcher constructor source."""
    if MARKER in source_text:
        return source_text
    # Only the base constructor source owns launcher_text and seals its bytes;
    # wrapper source literals must never be rewritten.
    if "def construct() -> tuple[dict[str, bytes], dict[str, Any]]:" not in source_text:
        return source_text
    launcher_anchor = '    launcher_raw = launcher_text.encode("utf-8")\n'
    # Some nested constructor wrappers carry the ``construct`` signature but
    # do not own launcher_text; only the actual source with the close anchor
    # is authoritative for this projection.
    if source_text.count(launcher_anchor) < 1:
        return source_text

    # The base constructor performs two launcher passes (before and after the
    # final audit rebind).  Apply the same deterministic projection before
    # each pass is hashed, and fail closed if either pass ever loses the
    # historical serializer anchor.
    helper_lines = [f"    # {MARKER}"]
    for index, (old, new) in enumerate(LIVE_PROJECTIONS, 1):
        helper_lines.extend([
            f"    _r63au_live_old_{index} = {old!r}",
            f"    _r63au_live_new_{index} = {new!r}",
            f"    if launcher_text.count(_r63au_live_old_{index}) != 1:",
            f"        raise RuntimeError(\"r63au live exact10 serializer anchor {index} drift\")",
            "    launcher_text = launcher_text.replace(",
            f"        _r63au_live_old_{index}, _r63au_live_new_{index}, 1)",
        ])
    helper = "\n".join(helper_lines) + "\n"
    source_text = source_text.replace(
        launcher_anchor, helper + launcher_anchor)
    return source_text


def main(argv: list[str] | None = None) -> int:
    raw = TEMPLATE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != TEMPLATE_SHA256:
        raise RuntimeError("immutable r63at builder template hash drift")

    # Every nested successor eventually compiles the base constructor source.
    # Intercept only that source, underneath the inherited compile hooks, so
    # the new projection is applied after all r63at retagging/path repairs and
    # before the launcher, manifest, outer, and successor receipt hashes close.
    real_compile = builtins.compile

    def patched_compile(source, filename, mode, *args, **kwargs):
        source_is_bytes = isinstance(source, (bytes, bytearray))
        if source_is_bytes:
            source_text = bytes(source).decode("utf-8")
        elif isinstance(source, str):
            source_text = source
        else:
            return real_compile(source, filename, mode, *args, **kwargs)
        patched = _patch_base_source(source_text)
        if patched != source_text:
            source = patched.encode("utf-8") if source_is_bytes else patched
        return real_compile(source, filename, mode, *args, **kwargs)

    builtins.compile = patched_compile
    try:
        text = raw.decode("utf-8").replace("r63at", "r63au").replace("R63AT", "R63AU")
        ns = {
            "__name__": "_c79g_r63au_builder_template",
            "__file__": str(ROOT / "scripts/c79g_v16r2r63au_runtime_bundle_builder.py"),
        }
        exec(real_compile(text, str(TEMPLATE), "exec"), ns, ns)
        return int(ns["main"](sys.argv[1:] if argv is None else argv))
    finally:
        builtins.compile = real_compile


if __name__ == "__main__":
    raise SystemExit(main())
