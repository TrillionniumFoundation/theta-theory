#!/usr/bin/env python3
"""Construct the append-only r63z successor with both install surfaces closed."""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts/c79g_v16r2r63x_runtime_bundle_builder.py"
TEMPLATE_SHA256 = "1c7fda53ef0370b9c34638ae570fc1738331790563e690d14e681368e34b16e2"


def main(argv: list[str] | None = None) -> int:
    raw = TEMPLATE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != TEMPLATE_SHA256:
        raise RuntimeError("immutable r63x builder template hash drift")
    text = raw.decode("utf-8").replace("r63x", "r63z")

    # Inject the consumer-side half of the same descriptor repair into the
    # in-memory template.  repr() keeps all source quoting/escape boundaries
    # explicit; no generated file is edited in place.
    nl = chr(10)
    consumer_anchor = '        "held_parent_path": str(RUNTIME.relative_to(ROOT)),\n'
    consumer_value = (
        '        "held_parent_path": str(RUNTIME.relative_to(ROOT)),\n'
        '        "launcher_owned_coordination_parent_fd_required": True,\n'
        '        "official_writer_coordination_lock_api": "launcher_owned_fcntl.flock(LOCK_EX)",\n'
        '        "all_official_runtime_writers_must_share_coordination_lock": True,\n'
        '        "coordination_lock_not_claimed_as_same_uid_or_filesystem_admin_security_boundary": True,\n'
        '        "fixed_target_prechecked_absent_before_stage_creation": True,\n'
        '        "absence_precheck_is_only_orphan_avoidance_not_race_commit_gate": True,\n'
    )
    consumer_patch = (
        "    old_consumer_install_anchor = " + repr(consumer_anchor) + nl
        + "    new_consumer_install_anchor = " + repr(consumer_value) + nl
        + "    if consumer_text.count(old_consumer_install_anchor) != 1:" + nl
        + '        raise RuntimeError("r63z consumer-install anchor not unique")' + nl
        + "    consumer_text = consumer_text.replace(" + nl
        + "        old_consumer_install_anchor, new_consumer_install_anchor, 1)" + nl
    )
    # The x wrapper itself loads the original r62 recipe at runtime.  Inject
    # a small second transformation into that loader, so the consumer patch
    # is applied to the loaded recipe (not to this wrapper's own source).
    loader_anchor = '    text = text.replace(needle, patch + needle, 1)\n'
    loader_code = (
        "    consumer_needle = " + repr(
            '    consumer_raw = consumer_text.encode("utf-8")\n') + nl
        + "    if text.count(consumer_needle) != 1:" + nl
        + '        raise RuntimeError("r63z consumer source insertion anchor drift")' + nl
        + "    text = text.replace(consumer_needle, " + repr(consumer_patch) +
        "+ consumer_needle, 1)" + nl
    )
    if text.count(loader_anchor) != 1:
        raise RuntimeError("builder-loader injection anchor drift")
    text = text.replace(loader_anchor, loader_anchor + loader_code, 1)
    ns = {
        "__name__": "_c79g_r63z_builder_template",
        "__file__": str(ROOT / "scripts/c79g_v16r2r63z_runtime_bundle_builder.py"),
    }
    exec(compile(text, str(TEMPLATE), "exec"), ns, ns)
    return int(ns["main"](sys.argv[1:] if argv is None else argv))


if __name__ == "__main__":
    raise SystemExit(main())
