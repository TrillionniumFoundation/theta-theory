#!/usr/bin/env python3
"""Construct the append-only r63af successor with v3 preseal binding repair.

The r63ae surface reached assemble and exposed the next live-only defect: the
exact-v3 helper returned a nested proof wrapper, while preseal/authority
consumers read the official rejection fields at the top level.  This wrapper
inherits the immutable r63ae recipe and adds those raw fields without
discarding the existing proof members.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts/c79g_v16r2r63ae_runtime_bundle_builder.py"
TEMPLATE_SHA256 = "df7562556aa76edf517ba0524c3d48cb3085f154a28c5a925001f26c24c56db8"


def main(argv: list[str] | None = None) -> int:
    raw = TEMPLATE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != TEMPLATE_SHA256:
        raise RuntimeError("immutable r63ae builder template hash drift")
    text = raw.decode("utf-8").replace("r63ae", "r63af")
    nl = chr(10)

    # Patch the generated consumer source at the existing consumer insertion
    # point.  Merging the raw value first preserves the nested proof while
    # exposing object_sha256/effective_checkpoint/status to live consumers.
    old_line = '        "official_v3_rejection": value,\n'
    new_lines = (
        "        **copy.deepcopy(value),\n"
        '        "official_v3_rejection": copy.deepcopy(value),\n')
    v3_runtime_patch = (
        "    r63af_v3_return_anchor = " + repr(old_line) + nl
        + "    r63af_v3_return_value = " + repr(new_lines) + nl
        + "    if consumer_text.count(r63af_v3_return_anchor) != 1:" + nl
        + '        raise RuntimeError("r63af exact-v3 return anchor drift")' + nl
        + "    consumer_text = consumer_text.replace(" + nl
        + "        r63af_v3_return_anchor, r63af_v3_return_value, 1)" + nl
    )
    # Inject the v3 statements into the generated builder's consumer source;
    # do not execute them in this outer loader scope where consumer_text is not
    # yet bound.
    outer_v3_injection = (
        "    r63af_v3_consumer_needle = " + repr(
            '    consumer_raw = consumer_text.encode("utf-8")\n') + nl
        + "    if text.count(r63af_v3_consumer_needle) != 1:" + nl
        + '        raise RuntimeError("r63af v3 consumer insertion anchor drift")' + nl
        + "    text = text.replace(r63af_v3_consumer_needle, "
        + repr(v3_runtime_patch) + "+ r63af_v3_consumer_needle, 1)" + nl
    )
    loader_anchor = (
        '        + "    text = text.replace(r63af_consumer_needle, " + repr(consumer_runtime_patch) + "+ r63af_consumer_needle, 1)" + nl\n'
    )
    loader_replacement = loader_anchor + '        + ' + repr(outer_v3_injection) + '\n'
    if text.count(loader_anchor) != 1:
        raise RuntimeError("r63af consumer-loader injection anchor drift")
    text = text.replace(loader_anchor, loader_replacement, 1)
    ns = {
        "__name__": "_c79g_r63af_builder_template",
        "__file__": str(ROOT / "scripts/c79g_v16r2r63af_runtime_bundle_builder.py"),
    }
    exec(compile(text, str(TEMPLATE), "exec"), ns, ns)
    return int(ns["main"](sys.argv[1:] if argv is None else argv))


if __name__ == "__main__":
    raise SystemExit(main())
