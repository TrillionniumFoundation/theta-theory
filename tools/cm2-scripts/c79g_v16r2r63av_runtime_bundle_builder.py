#!/usr/bin/env python3
"""Build the append-only r63av declared/physical-path successor.

This successor starts from the complete r63au chain (which already contains
the v4/v6/v7/v10 successor repairs) and applies the immutable r63an
declared/physical projection as an outer guard.  The r63an source and every
predecessor remain immutable; only the new retagged constructor is hashed.
"""
from __future__ import annotations

import builtins
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts/c79g_v16r2r63au_runtime_bundle_builder.py"
TEMPLATE_SHA256 = "9190c143e634218fe3204babf1ac4f19de690afb745ad462a0c13bd02268c763"
R63AN_PATCH_SOURCE = ROOT / "scripts/c79g_v16r2r63an_runtime_bundle_builder.py"
R63AN_PATCH_SOURCE_SHA256 = "c60a91849ef31a119eab5923e96ba0d7e8501c56096a49509d9728eeae7a1de0"
MARKER = "_R63AV_LIVE_SCHEMA_PROJECTION_APPLIED_"

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


def _patch_named_launcher_projection(source_text: str) -> str:
    if (MARKER in source_text or
            "_R63AV_LIVE_V10_SCHEMA_PROJECTION_APPLIED_" in source_text):
        return source_text
    if "def construct() -> tuple[dict[str, bytes], dict[str, Any]]:" not in source_text:
        return source_text
    # Nested successor wrappers carry the constructor signature in source
    # literals but do not own the raw-byte anchors.  Leave those layers to
    # their inherited hooks; only the actual constructor is eligible here.
    if (source_text.count('    producer_raw = producer_text.encode("utf-8")\n') != 1 or
            source_text.count('    consumer_raw = consumer_text.encode("utf-8")\n') != 1):
        return source_text
    launcher_anchor = '    launcher_raw = launcher_text.encode("utf-8")\n'
    if source_text.count(launcher_anchor) != 2:
        return source_text
    helper_lines = [f"    # {MARKER}"]
    for index, (old, new) in enumerate(LIVE_PROJECTIONS, 1):
        helper_lines.extend([
            f"    _r63av_live_old_{index} = {old!r}",
            f"    _r63av_live_new_{index} = {new!r}",
            f"    if launcher_text.count(_r63av_live_old_{index}) != 1:",
            f"        raise RuntimeError(\"r63av live exact10 serializer anchor {index} drift\")",
            "    launcher_text = launcher_text.replace(",
            f"        _r63av_live_old_{index}, _r63av_live_new_{index}, 1)",
        ])
    helper = "\n".join(helper_lines) + "\n"
    return source_text.replace(launcher_anchor, helper + launcher_anchor)


def _patch_base_source(source_text: str, declared_physical_patch) -> str:
    """Apply inherited r63an and new r63av patches to constructor source."""
    if "def construct() -> tuple[dict[str, bytes], dict[str, Any]]:" not in source_text:
        return source_text
    # The complete r63au chain already contains the immutable r63an
    # declared/physical projection. Re-entering that patch here would apply
    # producer/launcher anchors a second time and correctly reject as drift.
    # Keep the outer hook idempotent and only install the named exact10
    # projection if an inherited layer omitted it.
    return _patch_named_launcher_projection(source_text)


def main(argv: list[str] | None = None) -> int:
    raw = TEMPLATE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != TEMPLATE_SHA256:
        raise RuntimeError("immutable r63au builder template hash drift")

    # Load only the immutable r63an patch function.  Executing the module with
    # a private name defines helpers but does not invoke its CLI.
    r63an_raw = R63AN_PATCH_SOURCE.read_bytes()
    if hashlib.sha256(r63an_raw).hexdigest() != R63AN_PATCH_SOURCE_SHA256:
        raise RuntimeError("immutable r63an patch source hash drift")
    patch_ns: dict[str, object] = {
        "__name__": "_c79g_r63an_patch_helpers",
        "__file__": str(R63AN_PATCH_SOURCE),
    }
    real_compile = builtins.compile
    exec(real_compile(r63an_raw.decode("utf-8"), str(R63AN_PATCH_SOURCE), "exec"),
         patch_ns, patch_ns)
    declared_physical_patch = patch_ns.get("_patch_base_source")
    if not callable(declared_physical_patch):
        raise RuntimeError("immutable r63an declared/physical patch helper missing")

    # Retag the complete r63au chain.  Its nested hooks still run in their
    # historical order; the outer dispatcher adds the immutable r63an guard
    # only when the chain has not already installed it.
    text = raw.decode("utf-8").replace("r63au", "r63av").replace("R63AU", "R63AV")

    def patched_compile(source, filename, mode, *args, **kwargs):
        source_is_bytes = isinstance(source, (bytes, bytearray))
        if source_is_bytes:
            source_text = bytes(source).decode("utf-8")
        elif isinstance(source, str):
            source_text = source
        else:
            return real_compile(source, filename, mode, *args, **kwargs)
        patched = _patch_base_source(source_text, declared_physical_patch)
        if patched != source_text:
            source = patched.encode("utf-8") if source_is_bytes else patched
        return real_compile(source, filename, mode, *args, **kwargs)

    builtins.compile = patched_compile
    try:
        ns = {
            "__name__": "_c79g_r63av_builder_template",
            "__file__": str(ROOT / "scripts/c79g_v16r2r63av_runtime_bundle_builder.py"),
        }
        exec(real_compile(text, str(TEMPLATE), "exec"), ns, ns)
        return int(ns["main"](sys.argv[1:] if argv is None else argv))
    finally:
        builtins.compile = real_compile


if __name__ == "__main__":
    raise SystemExit(main())
