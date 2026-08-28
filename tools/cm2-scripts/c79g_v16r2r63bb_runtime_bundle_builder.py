#!/usr/bin/env python3
"""Append-only r63bb successor for the cold strict-bool projection.

r63ba and its official rejection are immutable.  This wrapper delegates to
that recipe, pins the r63ba rejection as the immediate predecessor, and makes
one schema-facing correction: the hard-call-site witness is serialized as a
JSON-shaped list of lists (the closed schema's exact constant), rather than a
Python list of tuples.  The inherited declared/physical authority-seal path
projection is checked, not rewritten: the versioned physical inode is kept
distinct from the stable declared generic path and the generic seal is never a
write target.
"""
from __future__ import annotations

import builtins
import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts/c79g_v16r2r63ba_runtime_bundle_builder.py"
TEMPLATE_SHA256 = (
    "31639b742d7d96091c74e9710b555c2b42365c4f288f580cdecc182f1b140da1"
)
PREDECESSOR_REJECTION = ROOT / (
    ".cm2-runtime/c79g-v16r2r63ba-rejections-"
    "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab/rejection.json"
)
PREDECESSOR_REJECTION_SHA256 = (
    "01bcccbf082c1d05d887b015d0f9946495ef6e097a5289f624e4161b47ff7ef8"
)
MARKER = "_R63BB_COLD_BOOL_JSON_SHAPE_AND_PATH_ASSERTIONS_APPLIED_"

_BOOL_OLD = (
    "'definite_truthy_nonbool_hard_callsites': sorted(observed_hard),"
)
_BOOL_NEW = (
    "'definite_truthy_nonbool_hard_callsites': "
    "[[role, line] for role, line in sorted(observed_hard)],"
)


def _patch_base_source(source_text: str) -> str:
    """Patch only the final cold-launch source before its bytes are pinned."""
    if MARKER in source_text:
        return source_text
    # The nested builder wrappers contain these strings in literals, but only
    # the actual launcher source contains the live strict-bool serializer.
    if _BOOL_OLD not in source_text:
        # The consumer source has no strict-bool serializer.  It is checked
        # below for the declared/physical path split instead.
        return _assert_consumer_paths(source_text)
    if source_text.count(_BOOL_OLD) != 1:
        raise RuntimeError("r63bb strict-bool serializer anchor drift")
    # The old anchor disappears after replacement, so the hook is naturally
    # idempotent on later compile passes; no marker/comment byte is appended to
    # the immutable launcher source.
    return source_text.replace(_BOOL_OLD, _BOOL_NEW, 1)


def _assert_consumer_paths(source_text: str) -> str:
    """Verify the inherited r63an path projection on the consumer only."""
    if ("def construct_authority_seal(" not in source_text or
            "AUTHORITY_SEAL = AUTHORITY_HEADS" not in source_text):
        return source_text
    required = (
        'AUTHORITY_SEAL = AUTHORITY_HEADS / ("c79g-v16r2r63bb-"',
        'AUTHORITY_SEAL_DECLARED_PATH = ".cm2-runtime/cm2-global-authority-heads/c79g-v16r2-"',
        'AUTHORITY_SEAL == ROOT / (".cm2-runtime/cm2-global-authority-heads/c79g-v16r2r63bb-"',
        '"target_path": AUTHORITY_SEAL_DECLARED_PATH',
        '"authority_seal": AUTHORITY_SEAL_DECLARED_PATH',
    )
    for anchor in required:
        if source_text.count(anchor) < 1:
            raise RuntimeError("r63bb declared/physical authority path anchor drift: " + anchor)
    if 'str(AUTHORITY_SEAL.relative_to(ROOT))' in source_text:
        raise RuntimeError("r63bb physical authority path leaked into declared projection")
    return source_text


def main(argv: list[str] | None = None) -> int:
    raw = TEMPLATE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != TEMPLATE_SHA256:
        raise RuntimeError("immutable r63ba builder template hash drift")
    if (not PREDECESSOR_REJECTION.is_file() or
            hashlib.sha256(PREDECESSOR_REJECTION.read_bytes()).hexdigest() !=
            PREDECESSOR_REJECTION_SHA256):
        raise RuntimeError("r63ba official rejection history is missing or mutated")

    # Retag only the fresh successor surface.  Historical r63az/r63ay labels
    # inside the inherited recipe are intentionally preserved; only its
    # immediate predecessor guard is advanced to r63ba.
    text = raw.decode("utf-8").replace("r63ba", "r63bb").replace("R63BA", "R63BB")
    old_path_fragment = "r63az-rejections-"
    new_path_fragment = "r63ba-rejections-"
    if text.count(old_path_fragment) != 1:
        raise RuntimeError("r63bb predecessor path anchor drift")
    text = text.replace(old_path_fragment, new_path_fragment, 1)
    old_hash = "8ae9547c070bd9d16a552e30f920fdb24a85c2c158d80f50d56e9d71c6d5adb4"
    if text.count(old_hash) != 1:
        raise RuntimeError("r63bb predecessor hash anchor drift")
    text = text.replace(old_hash, PREDECESSOR_REJECTION_SHA256, 1)

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
        ns = {
            "__name__": "_c79g_r63bb_builder_template",
            "__file__": str(ROOT / "scripts/c79g_v16r2r63bb_runtime_bundle_builder.py"),
        }
        exec(real_compile(text, str(TEMPLATE), "exec"), ns, ns)
        return int(ns["main"](sys.argv[1:] if argv is None else argv))
    finally:
        builtins.compile = real_compile


if __name__ == "__main__":
    raise SystemExit(main())
