#!/usr/bin/env python3
"""Append-only r63bc successor with a serialized cold-bool repair.

r63bb is immutable and rejected: its compile hook changed a transient AST
after ``launcher_text.encode`` had already fixed the published bytes.  r63bc
injects an idempotent list-of-lists projection into the base constructor before
both launcher encodes, so static pins, the installed launcher, and the cold
runtime all see the same bytes.  The inherited declared/physical seal split is
checked on the consumer and never redirected to the generic seal inode.
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
    ".cm2-runtime/c79g-v16r2r63bb-rejections-"
    "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab/rejection.json"
)
PREDECESSOR_REJECTION_SHA256 = (
    "7d701b98eb5ad7bc30ba3b49242f12b773d4970ed92a7486ac823e78a9644d93"
)
MARKER = "_R63BC_SERIALIZED_BOOL_BEFORE_LAUNCHER_ENCODE_APPLIED_"

_BOOL_OLD = "'definite_truthy_nonbool_hard_callsites': sorted(observed_hard),"
_BOOL_NEW = (
    "'definite_truthy_nonbool_hard_callsites': "
    "[[role, line] for role, line in sorted(observed_hard)],"
)


def _consumer_path_assertion(source_text: str) -> str:
    """Check the inherited declared/physical projection without rewriting it."""
    if ("def construct_authority_seal(" not in source_text or
            "AUTHORITY_SEAL = AUTHORITY_HEADS" not in source_text or
            "c79g-v16r2r63bc-" not in source_text):
        return source_text
    required = (
        'AUTHORITY_SEAL = AUTHORITY_HEADS / ("c79g-v16r2r63bc-"',
        'AUTHORITY_SEAL_DECLARED_PATH = ".cm2-runtime/cm2-global-authority-heads/c79g-v16r2-"',
        'AUTHORITY_SEAL == ROOT / (".cm2-runtime/cm2-global-authority-heads/c79g-v16r2r63bc-"',
        '"target_path": AUTHORITY_SEAL_DECLARED_PATH',
        '"authority_seal": AUTHORITY_SEAL_DECLARED_PATH',
    )
    for anchor in required:
        if source_text.count(anchor) < 1:
            raise RuntimeError("r63bc declared/physical authority path anchor drift: " + anchor)
    if 'str(AUTHORITY_SEAL.relative_to(ROOT))' in source_text:
        raise RuntimeError("r63bc physical authority path leaked into declared projection")
    return source_text


def _patch_base_source(source_text: str) -> str:
    if MARKER in source_text:
        return _consumer_path_assertion(source_text)
    # The actual base constructor has exactly two launcher encode sites.  The
    # nested wrapper literals do not, so this cannot mutate a recipe layer.
    launcher_anchor = '    launcher_raw = launcher_text.encode("utf-8")\n'
    if ("def construct() -> tuple[dict[str, bytes], dict[str, Any]]:" not in source_text or
            source_text.count(launcher_anchor) != 2):
        return _consumer_path_assertion(source_text)
    helper = f'''    # {MARKER}
    _r63bc_bool_old = {_BOOL_OLD!r}
    _r63bc_bool_new = {_BOOL_NEW!r}
    _r63bc_old_count = launcher_text.count(_r63bc_bool_old)
    _r63bc_new_count = launcher_text.count(_r63bc_bool_new)
    if _r63bc_old_count == 1 and _r63bc_new_count == 0:
        launcher_text = launcher_text.replace(_r63bc_bool_old, _r63bc_bool_new, 1)
    elif _r63bc_old_count == 0 and _r63bc_new_count == 1:
        pass
    else:
        raise RuntimeError("r63bc strict-bool serializer anchor drift")
'''
    patched = source_text.replace(launcher_anchor, helper + launcher_anchor)
    return _consumer_path_assertion(patched)


def main(argv: list[str] | None = None) -> int:
    raw = TEMPLATE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != TEMPLATE_SHA256:
        raise RuntimeError("immutable r63ba builder template hash drift")
    if (not PREDECESSOR_REJECTION.is_file() or
            hashlib.sha256(PREDECESSOR_REJECTION.read_bytes()).hexdigest() !=
            PREDECESSOR_REJECTION_SHA256):
        raise RuntimeError("r63bb official rejection history is missing or mutated")

    text = raw.decode("utf-8").replace("r63ba", "r63bc").replace("R63BA", "R63BC")
    old_path_fragment = "r63az-rejections-"
    if text.count(old_path_fragment) != 1:
        raise RuntimeError("r63bc predecessor path anchor drift")
    text = text.replace(old_path_fragment, "r63bb-rejections-", 1)
    old_hash = "8ae9547c070bd9d16a552e30f920fdb24a85c2c158d80f50d56e9d71c6d5adb4"
    if text.count(old_hash) != 1:
        raise RuntimeError("r63bc predecessor hash anchor drift")
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
            "__name__": "_c79g_r63bc_builder_template",
            "__file__": str(ROOT / "scripts/c79g_v16r2r63bc_runtime_bundle_builder.py"),
        }
        exec(real_compile(text, str(TEMPLATE), "exec"), ns, ns)
        return int(ns["main"](sys.argv[1:] if argv is None else argv))
    finally:
        builtins.compile = real_compile


if __name__ == "__main__":
    raise SystemExit(main())
