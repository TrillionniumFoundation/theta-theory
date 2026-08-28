#!/usr/bin/env python3
"""Append-only r63as successor of the r63ar recipe.

r63ar's physical surface, independent verification, and terminal replay all
passed, but the second live authorize correctly rejected the inner composite:
the historical v4 predecessor pin witnesses contain ``mode`` and ``nlink``
while the closed v16r2 schema's object/file pin definitions do not.  This
successor keeps the historical receipt and every raw/static replay byte intact
and projects only the schema-facing ``ordered_provisional_exact8`` member.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts/c79g_v16r2r63ar_runtime_bundle_builder.py"
TEMPLATE_SHA256 = "2696a3e642f860f964964eb01488814fff93906357ca0f7edac7d7a843d319d3"
MARKER = "_R63AS_V4_EXACT8_SCHEMA_PROJECTION_APPLIED_"


def _v4_consumer_patch_code() -> str:
    """Source appended to the generated compile-hook consumer patch.

    The generated consumer continues to use the raw v4 list for all historical
    receipt/transition/audit checks.  Only the value serialized by
    ``v4_rejection_supersession_proof`` is copied and stripped for the closed
    inner schema.
    """
    return r"""    # _R63AS_V4_EXACT8_SCHEMA_PROJECTION_APPLIED_
    _r63as_v4_call = "            v4_rejection_supersession_proof(freeze_proof),"
    if consumer_text.count(_r63as_v4_call) != 1:
        raise RuntimeError("r63as v4 serializer anchor drift")
    _r63as_v4_anchor = "\ndef _static_freeze_is_valid("
    if consumer_text.count(_r63as_v4_anchor) != 1:
        raise RuntimeError("r63as v4 helper insertion anchor drift")
    _r63as_v4_helper = r'''
def _r63as_project_v4_exact8_for_schema(freeze_proof):
    raw = _expected_v4_provisional_exact8()
    if not isinstance(raw, list) or len(raw) != 8:
        raise RuntimeError("r63as v4 exact8 historical shape drift")
    projected = []
    for member in raw:
        if not isinstance(member, dict):
            raise RuntimeError("r63as v4 exact8 member is not an object")
        if "mode" not in member or "nlink" not in member:
            raise RuntimeError("r63as v4 historical mode/nlink witness missing")
        projected.append({key: value for key, value in member.items()
                          if key not in ("mode", "nlink")})
    return projected
'''
    consumer_text = consumer_text.replace(
        _r63as_v4_anchor,
        "\n" + _r63as_v4_helper + _r63as_v4_anchor,
        1,
    )
    consumer_text = consumer_text.replace(
        _r63as_v4_call,
        "            _r63as_project_v4_exact8_for_schema(freeze_proof),",
        1,
    )
"""


def main(argv: list[str] | None = None) -> int:
    raw = TEMPLATE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != TEMPLATE_SHA256:
        raise RuntimeError("immutable r63ar builder template hash drift")

    # Retag only the fresh publication namespace.  The r63ar file, its seal,
    # rejection, and all predecessor bytes remain untouched and hash-pinned.
    text = raw.decode("utf-8").replace("r63ar", "r63as").replace("R63AR", "R63AS")
    # First hook the transformed r63ar wrapper's unique r63aq-retag line.  The
    # injected code then hooks the r63aq wrapper's r63ap-retag line one layer
    # later, when its ``text`` value is the actual r63ap recipe source.
    needle = (
        'text = raw.decode("utf-8").replace("r63aq", "r63as").replace("R63AQ", "R63AS")'
    )
    if text.count(needle) != 1:
        raise RuntimeError("r63as nested retag insertion anchor drift")

    patch_code = _v4_consumer_patch_code()
    nested_needle = (
        'text = raw.decode("utf-8").replace("r63ap", "r63as").replace("R63AP", "R63AS")'
    )
    nested_replacement = (
        nested_needle + "\n"
        '    text = text.replace("O_CREAT_EXCL_FIXED_TARGET_NO_FALLBACK",\n'
        '                        "O_CREAT_O_EXCL_FIXED_TARGET_NO_FALLBACK")\n'
        '    _r63as_consumer_anchor = "    consumer_patch_def = (\\n"\n'
        '    _r63as_patch = ' + repr(patch_code) + "\n"
        '    if text.count(_r63as_consumer_anchor) != 1:\n'
        '        raise RuntimeError("r63as generated consumer patch anchor drift")\n'
        '    if ' + repr(MARKER) + ' in text:\n'
        '        raise RuntimeError("r63as v4 projection already present")\n'
        '    text = text.replace(\n'
        '        _r63as_consumer_anchor,\n'
        '        "    consumer_patch_code += " + repr(_r63as_patch) + "\\n" +\n'
        '        _r63as_consumer_anchor,\n'
        '        1,\n'
        '    )'
    )
    replacement = (
        needle + "\n"
        '    _r63as_nested_needle = ' + repr(nested_needle) + "\n"
        '    _r63as_nested_replacement = ' + repr(nested_replacement) + "\n"
        '    if text.count(_r63as_nested_needle) != 1:\n'
        '        raise RuntimeError("r63as r63ap retag anchor drift")\n'
        '    text = text.replace(_r63as_nested_needle,\n'
        '                        _r63as_nested_replacement, 1)'
    )
    text = text.replace(needle, replacement, 1)

    ns = {
        "__name__": "_c79g_r63as_builder_template",
        "__file__": str(ROOT / "scripts/c79g_v16r2r63as_runtime_bundle_builder.py"),
    }
    exec(compile(text, str(TEMPLATE), "exec"), ns, ns)
    return int(ns["main"](sys.argv[1:] if argv is None else argv))


if __name__ == "__main__":
    raise SystemExit(main())
