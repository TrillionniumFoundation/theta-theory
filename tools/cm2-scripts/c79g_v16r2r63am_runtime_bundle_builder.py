#!/usr/bin/env python3
"""Construct r63am with the closed binding-equalities key set.

The r63al target-path repair reaches the live two-phase protocol, but its
inner composite reports two diagnostic v10/v11 equality keys that are not in
the frozen ``bindingEqualities`` closed schema (which requires the aggregate
``all_root_conjuncts_true`` key instead).  This successor removes only those
two extra reported keys before the consumer source is hashed.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts/c79g_v16r2r63al_runtime_bundle_builder.py"
TEMPLATE_SHA256 = "47dd4db8511d7a6e4cce5076a16ce08b25fd2f3d05888231f3933caccf2d305c"


def main(argv: list[str] | None = None) -> int:
    raw = TEMPLATE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != TEMPLATE_SHA256:
        raise RuntimeError("immutable r63al builder template hash drift")
    text = raw.decode("utf-8").replace("r63al", "r63am")

    # The r63al wrapper already injects the target-path repair into the nested
    # compile hook.  Append one more narrowly-scoped injection immediately
    # after that hook: remove the two non-schema diagnostic keys from the
    # generated consumer's binding-equalities dictionary.  r63al also
    # consumed the schema's singleton *declared* seal path.  Its failed live
    # attempt left that inode occupied, so this successor keeps the frozen
    # declared path in all serialized witnesses while using a fresh,
    # round-specific physical target for the append-only NOCLOBBER commit.
    needle = (
        "                consumer_anchor, consumer_anchor + consumer_helper, 1)\n"
        "\"\"\"\n")
    extra = r'''            close_anchor = '    consumer_raw = consumer_text.encode("utf-8")\n'
            close_helper = (
                '    _r63am_decl_pos = consumer_text.index("AUTHORITY_SEAL = AUTHORITY_HEADS / (")\n'
                '    _r63am_decl_tail = consumer_text[_r63am_decl_pos:]\n'
                '    _r63am_decl_tail = _r63am_decl_tail.replace(\n'
                '        "\\\"c79g-v16r2-\\\" + UPSTREAM_CHECKPOINT_OBJECT_PIN",\n'
                '        "\\\"c79g-v16r2r63am-\\\" + UPSTREAM_CHECKPOINT_OBJECT_PIN", 1)\n'
                '    consumer_text = consumer_text[:_r63am_decl_pos] + _r63am_decl_tail\n'
                '    _r63am_schema_pos = consumer_text.index("AUTHORITY_SEAL_SCHEMA =")\n'
                '    _r63am_declared_path = (\n'
                '        "AUTHORITY_SEAL_DECLARED_PATH = " + chr(34) +\n'
                '        ".cm2-runtime/cm2-global-authority-heads/c79g-v16r2-" +\n'
                '        chr(34) + " + UPSTREAM_CHECKPOINT_OBJECT_PIN + " + chr(34) + ".seal" + chr(34) + "\\n")\n'
                '    consumer_text = (consumer_text[:_r63am_schema_pos] +\n'
                '                     _r63am_declared_path +\n'
                '                     consumer_text[_r63am_schema_pos:])\n'
                '    consumer_text = consumer_text.replace(\n'
                '        "str(AUTHORITY_SEAL.relative_to(ROOT))",\n'
                '        "AUTHORITY_SEAL_DECLARED_PATH")\n'
                '    consumer_text = consumer_text.replace(\n'
                '        "AUTHORITY_SEAL == ROOT / (\\\".cm2-runtime/cm2-global-authority-heads/c79g-v16r2-\\\" +",\n'
                '        "AUTHORITY_SEAL == ROOT / (\\\".cm2-runtime/cm2-global-authority-heads/c79g-v16r2r63am-\\\" +", 1)\n'
                '    _r63am_extra_start = consumer_text.index("        " + chr(34) + "published_then_officially_rejected_predecessor_v10_equal_across_static_preseal_consumer_seal_and_postseal" + chr(34) + ":")\n'
                '    _r63am_extra_end = consumer_text.index("        " + chr(34) + "preseal_contract_and_schema_hashes_equal_contract" + chr(34) + ":", _r63am_extra_start)\n'
                '    consumer_text = consumer_text[:_r63am_extra_start] + consumer_text[_r63am_extra_end:]\n')
            if source_text.count(close_anchor) != 1:
                raise RuntimeError("r63am consumer close anchor drift")
            source_text = source_text.replace(
                close_anchor, close_helper + close_anchor, 1)
'''
    if text.count(needle) != 1:
        raise RuntimeError("r63am consumer injection anchor drift")
    text = text.replace(needle, needle[:-4] + extra + "\"\"\"\n", 1)

    ns = {
        "__name__": "_c79g_r63am_builder_template",
        "__file__": str(ROOT / "scripts/c79g_v16r2r63am_runtime_bundle_builder.py"),
    }
    exec(compile(text, str(TEMPLATE), "exec"), ns, ns)
    return int(ns["main"](sys.argv[1:] if argv is None else argv))


if __name__ == "__main__":
    raise SystemExit(main())
