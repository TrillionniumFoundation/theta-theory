#!/usr/bin/env python3
"""Construct the append-only r63ac successor with normalized C42/C53 proof."""
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
    text = raw.decode("utf-8").replace("r63ab", "r63ac")
    nl = chr(10)

    # The independent consumer exposes the canonical C42/C53 summary shape:
    # retain semantic pins/counts, discard raw physical-observation payloads,
    # and persist the normalized directory-policy facts it re-derives.
    helper_patch = '''def r63ac_normalize_kraft_registry(value: dict[str, Any]) -> dict[str, Any]:
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
    old_expr = (
        '        "C42_C53_direct_Kraft_reconstruction": copy.deepcopy('
        'state["C42_C53_Kraft_chain"]),\n')
    new_expr = (
        '        "C42_C53_direct_Kraft_reconstruction": '
        'r63ac_normalize_kraft_registry(state["C42_C53_Kraft_chain"]),\n')
    producer_runtime_patch = (
        "    r63ac_kraft_expr_anchor = " + repr(old_expr) + nl
        + "    r63ac_kraft_expr_value = " + repr(new_expr) + nl
        + "    if producer_text.count(r63ac_kraft_expr_anchor) != 1:" + nl
        + '        raise RuntimeError("r63ac C42/C53 registry expression anchor drift")' + nl
        + "    producer_text = producer_text.replace(" + nl
        + "        r63ac_kraft_expr_anchor, r63ac_kraft_expr_value, 1)" + nl
    )
    extra_loader_code = (
        "    r63ac_construct_anchor = " + repr(
            'def construct() -> tuple[dict[str, bytes], dict[str, Any]]:\n') + nl
        + "    if text.count(r63ac_construct_anchor) != 1:" + nl
        + '        raise RuntimeError("r63ac construct definition anchor drift")' + nl
        + "    text = text.replace(r63ac_construct_anchor, " + repr(helper_patch) + "+ r63ac_construct_anchor, 1)" + nl
        + "    r63ac_producer_needle = " + repr(
            '    producer_raw = producer_text.encode("utf-8")\n') + nl
        + "    if text.count(r63ac_producer_needle) != 1:" + nl
        + '        raise RuntimeError("r63ac producer insertion anchor drift")' + nl
        + "    text = text.replace(r63ac_producer_needle, " + repr(producer_runtime_patch) + "+ r63ac_producer_needle, 1)" + nl
    )

    # r63ab's loader string is the final bridge into the immutable base
    # recipe.  Append this patch after the earlier producer/consumer/audit
    # patches, so it edits only the in-memory source graph.
    loader_anchor = (
        '        + "    text = text.replace(r63ac_audit_needle, " + repr(audit_patch) + "+ r63ac_audit_needle, 1)" + nl\n'
        '    )')
    loader_replacement = (
        '        + "    text = text.replace(r63ac_audit_needle, " + repr(audit_patch) + "+ r63ac_audit_needle, 1)" + nl\n'
        '        + ' + repr(extra_loader_code) + '\n'
        '    )')
    if text.count(loader_anchor) != 1:
        raise RuntimeError("r63ac builder-loader injection anchor drift")
    text = text.replace(loader_anchor, loader_replacement, 1)
    ns = {
        "__name__": "_c79g_r63ac_builder_template",
        "__file__": str(ROOT / "scripts/c79g_v16r2r63ac_runtime_bundle_builder.py"),
    }
    exec(compile(text, str(TEMPLATE), "exec"), ns, ns)
    return int(ns["main"](sys.argv[1:] if argv is None else argv))


if __name__ == "__main__":
    raise SystemExit(main())
