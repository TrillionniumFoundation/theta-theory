#!/usr/bin/env python3
"""Construct the append-only r63ae successor with assemble-surface repair.

The r63ad candidate and both independent verifications are retained.  The
remaining failure is in the frozen consumer's assemble path: it passes a
combined candidate+verification guard to ``candidate()``, whose exact-surface
predicate must select the candidate subset before checking it.  This wrapper
rebuilds from the immutable r63ab recipe, carries the r63ad Kraft fix, and
adds that narrowly scoped consumer-side filter.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts/c79g_v16r2r63ab_runtime_bundle_builder.py"
TEMPLATE_SHA256 = "d2523a57b4a2c6ae63dbd56d32b0bec6189fa509af97e3b06739d4fe010fea04"


def main(argv: list[str] | None = None) -> int:
    raw = TEMPLATE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != TEMPLATE_SHA256:
        raise RuntimeError("immutable r63ab builder template hash drift")
    text = raw.decode("utf-8").replace("r63ab", "r63ae")
    nl = chr(10)

    helper_patch = '''def r63ae_normalize_kraft_registry(value: dict[str, Any]) -> dict[str, Any]:
    dropped = {
        "C42_candidate_observed_physical_policy",
        "C42_independent_audit_observed_physical_policy",
        "C42_installation_receipt_observed_physical_policy",
        "held_direct_input_identity_count",
        "C42_rows_by_pair",
        "C53_projections_by_pair",
    }
    normalized = {
        key: copy.deepcopy(item)
        for key, item in value.items()
        if key not in dropped
    }
    normalized.update({
        "C42_held_directory_count": 3,
        "C42_candidate_directory_expected_mode": "0755",
        "C42_candidate_directory_expected_nlink": 2,
        "C42_independent_audit_directory_expected_mode": "0700",
        "C42_independent_audit_directory_expected_nlink": 2,
        "C42_installation_receipt_directory_expected_mode": "0500",
        "C42_installation_receipt_directory_expected_nlink": 2,
        "C42_auxiliary_directory_exact_member_count_each": 1,
        "historical_directory_modes_are_exact_observed_snapshot_guards_not_immutability_claims": True,
    })
    return normalized
'''

    producer_helper_patch = (
        "    r63ae_producer_future_anchor = "
        + repr("from __future__ import annotations\n") + nl
        + "    r63ae_producer_helper_source = " + repr(helper_patch) + nl
        + "    if producer_text.count(r63ae_producer_future_anchor) != 1:" + nl
        + '        raise RuntimeError("r63ae producer future-import anchor drift")' + nl
        + "    producer_text = producer_text.replace(" + nl
        + "        r63ae_producer_future_anchor, " + nl
        + "        r63ae_producer_future_anchor + r63ae_producer_helper_source, 1)" + nl
    )
    old_expr = (
        '        "C42_C53_direct_Kraft_reconstruction": copy.deepcopy('
        'state["C42_C53_Kraft_chain"]),\n')
    new_expr = (
        '        "C42_C53_direct_Kraft_reconstruction": '
        'r63ae_normalize_kraft_registry(state["C42_C53_Kraft_chain"]),\n')
    producer_runtime_patch = (
        producer_helper_patch
        + "    r63ae_kraft_expr_anchor = " + repr(old_expr) + nl
        + "    r63ae_kraft_expr_value = " + repr(new_expr) + nl
        + "    if producer_text.count(r63ae_kraft_expr_anchor) != 1:" + nl
        + '        raise RuntimeError("r63ae C42/C53 registry expression anchor drift")' + nl
        + "    producer_text = producer_text.replace(" + nl
        + "        r63ae_kraft_expr_anchor, r63ae_kraft_expr_value, 1)" + nl
    )

    # The assemble/authority paths intentionally hold candidate and
    # verification surfaces together.  Filter only the candidate() view so its
    # exact 18-member predicate remains strict while the caller can retain
    # the verification files for later chronology and identity checks.
    old_candidate_view = (
        "    by_path = {item.path: item for item in candidate_guard.files}\n"
        "    by_directory = {item.path: item for item in candidate_guard.directories}\n"
        "    expected_paths = ({candidate_dir / name for name in MEMBERS} |\n"
        "                      {peer_candidate_dir / name for name in MEMBERS})\n")
    new_candidate_view = (
        "    expected_paths = ({candidate_dir / name for name in MEMBERS} |\n"
        "                      {peer_candidate_dir / name for name in MEMBERS})\n"
        "    by_path = {item.path: item for item in candidate_guard.files\n"
        "               if item.path in expected_paths}\n"
        "    by_directory = {item.path: item for item in candidate_guard.directories\n"
        "                    if item.path in {candidate_dir, peer_candidate_dir}}\n")
    consumer_runtime_patch = (
        "    r63ae_candidate_view_anchor = " + repr(old_candidate_view) + nl
        + "    r63ae_candidate_view_value = " + repr(new_candidate_view) + nl
        + "    if consumer_text.count(r63ae_candidate_view_anchor) != 1:" + nl
        + '        raise RuntimeError("r63ae candidate-view anchor drift")' + nl
        + "    consumer_text = consumer_text.replace(" + nl
        + "        r63ae_candidate_view_anchor, r63ae_candidate_view_value, 1)" + nl
    )

    extra_loader_code = (
        "    r63ae_construct_anchor = " + repr(
            'def construct() -> tuple[dict[str, bytes], dict[str, Any]]:\n') + nl
        + "    if text.count(r63ae_construct_anchor) != 1:" + nl
        + '        raise RuntimeError("r63ae construct definition anchor drift")' + nl
        + "    text = text.replace(r63ae_construct_anchor, " + repr(helper_patch) + "+ r63ae_construct_anchor, 1)" + nl
        + "    r63ae_producer_needle = " + repr(
            '    producer_raw = producer_text.encode("utf-8")\n') + nl
        + "    if text.count(r63ae_producer_needle) != 1:" + nl
        + '        raise RuntimeError("r63ae producer insertion anchor drift")' + nl
        + "    text = text.replace(r63ae_producer_needle, " + repr(producer_runtime_patch) + "+ r63ae_producer_needle, 1)" + nl
        + "    r63ae_consumer_needle = " + repr(
            '    consumer_raw = consumer_text.encode("utf-8")\n') + nl
        + "    if text.count(r63ae_consumer_needle) != 1:" + nl
        + '        raise RuntimeError("r63ae consumer insertion anchor drift")' + nl
        + "    text = text.replace(r63ae_consumer_needle, " + repr(consumer_runtime_patch) + "+ r63ae_consumer_needle, 1)" + nl
    )

    loader_anchor = (
        '        + "    text = text.replace(r63ae_audit_needle, " + repr(audit_patch) + "+ r63ae_audit_needle, 1)" + nl\n'
        '    )')
    loader_replacement = (
        '        + "    text = text.replace(r63ae_audit_needle, " + repr(audit_patch) + "+ r63ae_audit_needle, 1)" + nl\n'
        '        + ' + repr(extra_loader_code) + '\n'
        '    )')
    if text.count(loader_anchor) != 1:
        raise RuntimeError("r63ae builder-loader injection anchor drift")
    text = text.replace(loader_anchor, loader_replacement, 1)
    ns = {
        "__name__": "_c79g_r63ae_builder_template",
        "__file__": str(ROOT / "scripts/c79g_v16r2r63ae_runtime_bundle_builder.py"),
    }
    exec(compile(text, str(TEMPLATE), "exec"), ns, ns)
    return int(ns["main"](sys.argv[1:] if argv is None else argv))


if __name__ == "__main__":
    raise SystemExit(main())
