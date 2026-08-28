#!/usr/bin/env python3
"""Construct the append-only r63x successor of the r63w runtime repair.

The large, already-audited r63 repair recipe is treated as an immutable
template.  This thin successor wrapper changes only the round namespace and
adds the four launcher-owned coordination-lock fields that the independent
consumer requires in the persisted candidate-install descriptor.  The
template still rebuilds every object from the immutable r62 witnesses and
closes a fresh exact8/outer/receipt chain; no r63w artifact is overwritten.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts/c79g_v16r2r63_runtime_bundle_builder.py"
TEMPLATE_SHA256 = "5eaf49cf525f8b431d83d53cc1956d460f8bfb6c2d50785d379e6d7c2432a27f"


def load_template() -> dict[str, object]:
    raw = TEMPLATE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != TEMPLATE_SHA256:
        raise RuntimeError("immutable r63w builder template hash drift")
    text = raw.decode("utf-8")
    # The template's lowercase round tag occurs only in its successor output
    # namespace/labels.  Historical r62 inputs remain untouched.
    text = text.replace("r63w", "r63x")
    needle = '    producer_raw = producer_text.encode("utf-8")\n'
    nl = chr(10)
    esc_n = chr(92) + "n"
    patch = (
        "    # r63x repair: persist the launcher-owned coordination protocol in" + nl
        + "    # the candidate outer descriptor so the independent consumer can compare" + nl
        + "    # the producer and consumer surfaces byte-for-byte." + nl
        + "    old_candidate_install_anchor = '            \\\"held_parent_path\\\": str(RUNTIME.relative_to(ROOT))," + esc_n + "'" + nl
        + "    new_candidate_install_anchor = (" + nl
        + "        '            \\\"held_parent_path\\\": str(RUNTIME.relative_to(ROOT))," + esc_n + "'" + nl
        + "        '            \\\"launcher_owned_coordination_parent_fd_required\\\": True," + esc_n + "'" + nl
        + "        '            \\\"official_writer_coordination_lock_api\\\": \\\"launcher_owned_fcntl.flock(LOCK_EX)\\\"," + esc_n + "'" + nl
        + "        '            \\\"all_official_runtime_writers_must_share_coordination_lock\\\": True," + esc_n + "'" + nl
        + "        '            \\\"coordination_lock_not_claimed_as_same_uid_or_filesystem_admin_security_boundary\\\": True," + esc_n + "'" + nl
        + "    )" + nl
        + "    if producer_text.count(old_candidate_install_anchor) != 1:" + nl
        + '        raise RuntimeError("r63x candidate-install anchor not unique")' + nl
        + "    producer_text = producer_text.replace(" + nl
        + "        old_candidate_install_anchor, new_candidate_install_anchor, 1)" + nl
    )
    if text.count(needle) != 1:
        raise RuntimeError("r63w template producer insertion anchor drift")
    text = text.replace(needle, patch + needle, 1)
    namespace = {
        "__name__": "_c79g_r63x_builder_template",
        "__file__": str(ROOT / "scripts/c79g_v16r2r63x_runtime_bundle_builder.py"),
    }
    exec(compile(text, str(TEMPLATE), "exec"), namespace, namespace)
    return namespace


def main(argv: list[str] | None = None) -> int:
    ns = load_template()
    # Delegate the public preflight/install CLI to the proven recipe.  It uses
    # the rewritten in-memory source, so all output paths are r63x and all
    # writes remain O_EXCL/0444/append-only.
    return int(ns["main"](sys.argv[1:] if argv is None else argv))


if __name__ == "__main__":
    raise SystemExit(main())
