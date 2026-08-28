#!/usr/bin/env python3
"""Construct the append-only r63al successor with target-path closure.

The r63ak runtime restored the schema-fixed authority staging path, but its
live consumer still retagged the persisted authority-seal target itself.
Keep r63ak immutable and repair only that target binding in the next
successor: candidate/verification/completion/rejection namespaces remain
round-specific, while the authority seal uses the schema's fixed path.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts/c79g_v16r2r63ak_runtime_bundle_builder.py"
TEMPLATE_SHA256 = "afdc5f344da782b9428a8182c5e05a513f07c21b9625d4a9bc6ea3ab1997f8bc"


def main(argv: list[str] | None = None) -> int:
    raw = TEMPLATE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != TEMPLATE_SHA256:
        raise RuntimeError("immutable r63ak builder template hash drift")
    text = raw.decode("utf-8").replace("r63ak", "r63al")

    # Keep the schema-fixed authority path in the contract after the nested
    # retag pass.  The stage-path repair is inherited from r63ak.
    helper_lines = text.splitlines(keepends=True)
    helper_index = next(
        (index for index, line in enumerate(helper_lines)
         if '_r63al_paths[' in line and 'authority_staging_prefix' in line),
        None)
    if helper_index is None:
        raise RuntimeError("r63al contract target helper anchor drift")
    helper_lines[helper_index + 1:helper_index + 1] = [
        "        + " + repr(
            '        "        _r63al_paths[\\"authority_seal\\"] = (\\n"\n'),
        "        + " + repr(
            '        "            \\".cm2-runtime/cm2-global-authority-heads/c79g-v16r2-\\" + CHECKPOINT + \\".seal\\")\\n"\n'),
    ]
    text = "".join(helper_lines)

    # Inject a narrowly-scoped source rewrite into the base builder.  It is
    # applied after the live consumer paths are retagged, and changes only the
    # AUTHORITY_SEAL declaration and its fixed-path self-check; all other
    # round-specific runtime targets remain untouched.
    old_insert_line = (
        '    new_insert = "            source_text = '
        'source_text.replace(anchor, anchor + helper, 1)\\n"\n')
    consumer_patch_source = r"""            consumer_anchor = (
                '    consumer_text = retag_current_runtime_targets(\n'
                '        consumer_text, NEW["consumer"])\n')
            consumer_helper = (
                '    _r63al_decl_pos = consumer_text.index("AUTHORITY_SEAL = AUTHORITY_HEADS / (")\n'
                '    _r63al_decl_tail = consumer_text[_r63al_decl_pos:]\n'
                '    _r63al_decl_tail = _r63al_decl_tail.replace(\n'
                '        RUNTIME_TARGET_PREFIX_NEW, "c79g-v16r2-", 1)\n'
                '    consumer_text = consumer_text[:_r63al_decl_pos] + _r63al_decl_tail\n'
                '    _r63al_assert_pos = consumer_text.index("AUTHORITY_SEAL == ROOT / (")\n'
                '    _r63al_assert_tail = consumer_text[_r63al_assert_pos:]\n'
                '    _r63al_assert_tail = _r63al_assert_tail.replace(\n'
                '        RUNTIME_TARGET_PREFIX_NEW, "c79g-v16r2-", 1)\n'
                '    consumer_text = consumer_text[:_r63al_assert_pos] + _r63al_assert_tail\n')
            if source_text.count(consumer_anchor) != 1:
                raise RuntimeError("r63al consumer target anchor drift")
            source_text = source_text.replace(
                consumer_anchor, consumer_anchor + consumer_helper, 1)
"""
    new_insert_value = (
        '            source_text = source_text.replace(anchor, anchor + helper, 1)\n'
        + consumer_patch_source)
    new_insert_line = '    new_insert = ' + repr(new_insert_value) + '\n'
    if text.count(old_insert_line) != 1:
        raise RuntimeError("r63al consumer insertion anchor drift")
    text = text.replace(old_insert_line, new_insert_line, 1)

    ns = {
        "__name__": "_c79g_r63al_builder_template",
        "__file__": str(ROOT / "scripts/c79g_v16r2r63al_runtime_bundle_builder.py"),
    }
    exec(compile(text, str(TEMPLATE), "exec"), ns, ns)
    return int(ns["main"](sys.argv[1:] if argv is None else argv))


if __name__ == "__main__":
    raise SystemExit(main())
