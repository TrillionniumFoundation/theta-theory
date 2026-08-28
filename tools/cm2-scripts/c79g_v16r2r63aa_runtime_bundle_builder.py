#!/usr/bin/env python3
"""Construct the append-only r63aa successor with registry schema repaired."""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts/c79g_v16r2r63z_runtime_bundle_builder.py"
TEMPLATE_SHA256 = "b5ae6ccffb97e575f7cc3fd095963e743c332d2c1f6b3e9f545f22f599fb40c0"


def main(argv: list[str] | None = None) -> int:
    raw = TEMPLATE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != TEMPLATE_SHA256:
        raise RuntimeError("immutable r63z builder template hash drift")
    text = raw.decode("utf-8").replace("r63z", "r63aa")
    nl = chr(10)

    # Inject a producer-source repair into the z loader.  The old producer
    # exposed the V14 twelve-FD labels and persisted internal census fields in
    # the public registry; the independent consumer's closed 74-key schema
    # requires the ten-incident labels plus one aggregate history count.
    old_key_a = "twelve_v14_inherited_authority_inputs_inherited_as_held_fds"
    new_key_a = "ten_incident_authority_inputs_inherited_as_held_fds"
    old_key_b = "twelve_v14_inherited_authority_held_fds_path_identity_mount_and_hash_revalidated"
    new_key_b = "ten_incident_held_fds_path_identity_mount_and_hash_revalidated"
    old_census = (
        '        "v16r2_predecessor_unique_live_identity_count":\n'
        '            static_trust["v16r2_predecessor_unique_live_identity_count"],\n'
        '        "v16r2_prepublication_unique_live_identity_count":\n'
        '            static_trust["v16r2_prepublication_unique_live_identity_count"],\n'
        '        "v16r2_terminal_unique_live_identity_count":\n'
        '            static_trust["v16r2_terminal_unique_live_identity_count"],\n'
        '        "v16r2_terminal_group_vector":\n'
        '            static_trust["v16r2_terminal_group_vector"],\n'
    )
    new_census = (
        '        "append_only_history_unique_file_identity_count":\n'
        '            V16R2_TERMINAL_UNIQUE_LIVE_IDENTITY_COUNT,\n'
    )
    producer_patch = (
        "    old_registry_execution_key_a = " + repr(old_key_a) + nl
        + "    old_registry_execution_key_b = " + repr(old_key_b) + nl
        + "    if producer_text.count(old_registry_execution_key_a) < 1 or "
          "producer_text.count(old_registry_execution_key_b) < 1:" + nl
        + '        raise RuntimeError("r63aa producer execution-key anchors missing")' + nl
        + "    producer_text = producer_text.replace(" + repr(old_key_a) + ", " + repr(new_key_a) + ")" + nl
        + "    producer_text = producer_text.replace(" + repr(old_key_b) + ", " + repr(new_key_b) + ")" + nl
        + "    old_registry_census = " + repr(old_census) + nl
        + "    new_registry_census = " + repr(new_census) + nl
        + "    if producer_text.count(old_registry_census) != 1:" + nl
        + '        raise RuntimeError("r63aa registry census anchor not unique")' + nl
        + "    producer_text = producer_text.replace(old_registry_census, new_registry_census, 1)" + nl
    )

    # r63z's loader already injects the consumer-side patch into the original
    # recipe.  Append this producer patch to that loader-code expression.
    producer_loader_code = (
        "    producer_needle = " + repr(
            '    producer_raw = producer_text.encode("utf-8")\n') + nl
        + "    if text.count(producer_needle) != 1:" + nl
        + '        raise RuntimeError("r63aa producer source insertion anchor drift")' + nl
        + "    text = text.replace(producer_needle, " + repr(producer_patch) +
        "+ producer_needle, 1)" + nl
    )
    loader_anchor = (
        '        "+ consumer_needle, 1)" + nl\n'
        '    )')
    loader_replacement = (
        '        "+ consumer_needle, 1)" + nl\n'
        '        + ' + repr(producer_loader_code) + '\n'
        '    )')
    if text.count(loader_anchor) != 1:
        raise RuntimeError("r63aa builder-loader injection anchor drift")
    text = text.replace(loader_anchor, loader_replacement, 1)
    ns = {
        "__name__": "_c79g_r63aa_builder_template",
        "__file__": str(ROOT / "scripts/c79g_v16r2r63aa_runtime_bundle_builder.py"),
    }
    exec(compile(text, str(TEMPLATE), "exec"), ns, ns)
    return int(ns["main"](sys.argv[1:] if argv is None else argv))


if __name__ == "__main__":
    raise SystemExit(main())
