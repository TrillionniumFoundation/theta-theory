#!/usr/bin/env python3
"""Construct the append-only r63ag successor with schema-stage alignment.

The r63af live run reached the inner composite and exposed a cross-surface
defect: its retagged authority staging path did not match the immutable
v16r2r62 closed-schema ``authoritySeal.staging_path`` const.  This wrapper
inherits the pinned r63af recipe, restores the schema's generic authority
stage spelling in the new consumer and all newly derived JSON witnesses, and
leaves every r63af byte untouched.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts/c79g_v16r2r63af_runtime_bundle_builder.py"
TEMPLATE_SHA256 = "481bfcabf4267aed2cc2e5e09ac42e931efd204e9e14ea66b2adbe17e134ea0b"


def main(argv: list[str] | None = None) -> int:
    raw = TEMPLATE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != TEMPLATE_SHA256:
        raise RuntimeError("immutable r63af builder template hash drift")
    text = raw.decode("utf-8").replace("r63af", "r63ag")
    nl = chr(10)

    # This patch is carried through the existing nested builder-loader chain
    # in the same way as r63af's v3 repair.  At the final source-construction
    # layer, consumer_text is the generated r63ag consumer; contract_value is
    # the newly retagged contract object.  The guarded contract rewrite also
    # makes the patch safe while it is being carried through intermediate
    # loader source strings where contract_value is not yet bound.
    stage_old = 'AUTHORITY_STAGE_PREFIX = ".c79g-v16r2r63ag-authority-stage-"' + nl
    stage_new = 'AUTHORITY_STAGE_PREFIX = ".c79g-v16r2-authority-stage-"' + nl
    generic_old = ".c79g-v16r2r63ag-authority-stage-"
    generic_new = ".c79g-v16r2-authority-stage-"
    stage_runtime_patch = (
        "    r63ag_stage_anchor = " + repr(stage_old) + nl
        + "    r63ag_stage_value = " + repr(stage_new) + nl
        + "    if consumer_text.count(r63ag_stage_anchor) != 1:" + nl
        + '        raise RuntimeError("r63ag authority-stage source anchor drift")' + nl
        + "    consumer_text = consumer_text.replace(" + nl
        + "        r63ag_stage_anchor, r63ag_stage_value, 1)" + nl
        + "    try:" + nl
        + "        r63ag_contract_value = contract_value" + nl
        + "    except NameError:" + nl
        + "        r63ag_contract_value = None" + nl
        + "    if r63ag_contract_value is not None:" + nl
        + "        def r63ag_stage_json(value):" + nl
        + "            if isinstance(value, dict):" + nl
        + "                return {key: r63ag_stage_json(item) for key, item in value.items()}" + nl
        + "            if isinstance(value, list):" + nl
        + "                return [r63ag_stage_json(item) for item in value]" + nl
        + "            if isinstance(value, str):" + nl
        + "                return value.replace(" + repr(generic_old) + ", " + repr(generic_new) + ")" + nl
        + "            return value" + nl
        + "        contract_value = r63ag_stage_json(r63ag_contract_value)" + nl
    )

    # r63af's loader already carries its v3 patch into the base recipe.  Add
    # the stage-alignment statements to that same carried patch, so the final
    # base builder applies them immediately before encoding the consumer.
    marker = '        + repr(v3_runtime_patch) + "+ r63ag_v3_consumer_needle, 1)" + nl'
    replacement = (
        '        + repr(v3_runtime_patch + ' + repr(stage_runtime_patch) + ') + '
        '"+ r63ag_v3_consumer_needle, 1)" + nl'
    )
    if text.count(marker) != 1:
        raise RuntimeError("r63ag v3 patch carrier anchor drift")
    text = text.replace(marker, replacement, 1)

    ns = {
        "__name__": "_c79g_r63ag_builder_template",
        "__file__": str(ROOT / "scripts/c79g_v16r2r63ag_runtime_bundle_builder.py"),
    }
    exec(compile(text, str(TEMPLATE), "exec"), ns, ns)
    return int(ns["main"](sys.argv[1:] if argv is None else argv))


if __name__ == "__main__":
    raise SystemExit(main())
