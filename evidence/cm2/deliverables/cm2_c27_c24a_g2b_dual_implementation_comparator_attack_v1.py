#!/usr/bin/env python3
"""Closure-preserving coherent attacks for the C24A G2B comparator."""

from __future__ import annotations

import argparse
from collections.abc import Callable
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
COMPARATOR = ROOT / "deliverables/cm2_c27_c24a_g2b_dual_implementation_comparator_v1.py"
COMPARATOR_SHA256 = "4eff31f89e85d7849e0d8e609950efb2dc234ac80168a511e90f8bddee992043"


class HarnessFailure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise HarnessFailure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def rows(path: Path, expected: str) -> list[dict[str, Any]]:
    need(file_sha(path) == expected, "input pin:" + path.name)
    output: list[dict[str, Any]] = []
    with gzip.open(path, "rb") as stream:
        for line in stream:
            row = json.loads(line)
            body = dict(row)
            claimed = body.pop("row_sha256")
            need(claimed == digest(body), "input row closure")
            output.append(row)
    return output


def reclose(row: dict[str, Any], key: str, value: Any) -> dict[str, Any]:
    body = dict(row)
    body.pop("row_sha256")
    body[key] = value
    body["row_sha256"] = digest(body)
    return body


def changed(values: list[dict[str, Any]], index: int, key: str, value: Any) -> list[dict[str, Any]]:
    output = list(values)
    output[index] = reclose(output[index], key, value)
    return output


def flip(value: str) -> str:
    need(value in {"STRICT_POSITIVE", "STRICT_NEGATIVE"}, "strict sign to flip")
    return "STRICT_NEGATIVE" if value == "STRICT_POSITIVE" else "STRICT_POSITIVE"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--primary", required=True)
    parser.add_argument("--secondary", required=True)
    parser.add_argument("--priority", required=True)
    parser.add_argument("--cross", required=True)
    parser.add_argument("--edges", required=True)
    parser.add_argument("--seed", required=True, type=int)
    args = parser.parse_args()
    try:
        need(file_sha(COMPARATOR) == COMPARATOR_SHA256, "comparator source pin")
        spec = importlib.util.spec_from_file_location("cm2_c24a_comparator_pinned", COMPARATOR)
        need(spec is not None and spec.loader is not None, "comparator module spec")
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)

        p = rows(Path(args.primary), "c3dbfb3363af18dc79b27aeb4245266102914de5a8c2cab980c019337776d899")
        s = rows(Path(args.secondary), "f72c792fdca47ba1e5b92498a43995d16d76b758647a8f444da9af349d3654c7")
        r = rows(Path(args.priority), "6a59b0822c8a27eb5f44609cd5edd33038dadf17aa8fe7841d2c7277c8c5ec95")
        c = rows(Path(args.cross), "0f3924d4a9f0b029d4c82879ec453bb280232c13d870ac28157b5a20dd5585c8")
        e = rows(Path(args.edges), "d922bbf6d8f487df1e826271b0d65d2d9765432f6d4a02919fe1157b94c117ef")
        baseline = module.semantic_compare(p, s, r, c, e)
        need(baseline["dual_pair_count"] == 18_800, "baseline comparator")

        Attack = tuple[str, Callable[[], tuple[list[dict[str, Any]], ...]]]
        attacks: list[Attack] = []
        attacks.extend([
            ("primary_missing_row", lambda: (p[:-1], s, r, c, e)),
            ("primary_duplicate_row", lambda: (p + [p[0]], s, r, c, e)),
            ("primary_pair_authority_flip", lambda: (changed(p, 0, "candidate_ledger_row_sha256", "0" * 64), s, r, c, e)),
            ("primary_C24_row_flip", lambda: (changed(p, 0, "C24_row_sha256", "1" * 64), s, r, c, e)),
            ("primary_target_row_flip", lambda: (changed(p, 0, "C22_target_row_sha256", "2" * 64), s, r, c, e)),
            ("primary_source_member_flip", lambda: (changed(p, 0, "c24_member_id", "attack:source"), s, r, c, e)),
            ("primary_target_member_flip", lambda: (changed(p, 0, "target_member_id", "attack:target"), s, r, c, e)),
            ("primary_authority_role_flip", lambda: (changed(p, 0, "C11_or_C12_authority_role", "C12A" if p[0]["C11_or_C12_authority_role"] != "C12A" else "C11B"), s, r, c, e)),
            ("primary_component_equality_flip", lambda: (changed(p, 0, "current_C15_components_equal", not p[0]["current_C15_components_equal"]), s, r, c, e)),
            ("primary_R300C_flag_flip", lambda: (changed(p, 0, "R300C_validation_pair", not p[0]["R300C_validation_pair"]), s, r, c, e)),
            ("primary_disposition_flip", lambda: (changed(p, 0, "disposition", "EXACT_EMPTY_INTERSECTION" if p[0]["disposition"] == "EXACT_POSITIVE_SUPPORT" else "EXACT_POSITIVE_SUPPORT"), s, r, c, e)),
            ("primary_required_sign_flip", lambda: (changed(p, 0, "predicate_required_sign", flip(p[0]["predicate_required_sign"])), s, r, c, e)),
            ("primary_target_sign_flip", lambda: (changed(p, 0, "target_region_product_sign" if p[0]["target_region_product_sign"] is not None else "factor_sign_on_target_open_box", flip(p[0]["target_region_product_sign"] if p[0]["target_region_product_sign"] is not None else p[0]["factor_sign_on_target_open_box"])), s, r, c, e)),
            ("secondary_missing_row", lambda: (p, s[:-1], r, c, e)),
            ("secondary_duplicate_row", lambda: (p, s + [s[0]], r, c, e)),
            ("secondary_pair_authority_flip", lambda: (p, changed(s, 0, "pair_row_sha256", "3" * 64), r, c, e)),
            ("secondary_C24_row_flip", lambda: (p, changed(s, 0, "c24_row_sha256", "4" * 64), r, c, e)),
            ("secondary_target_row_flip", lambda: (p, changed(s, 0, "target_row_sha256", "5" * 64), r, c, e)),
            ("secondary_source_member_flip", lambda: (p, changed(s, 0, "c24_member_id", "attack:source"), r, c, e)),
            ("secondary_authority_role_flip", lambda: (p, changed(s, 0, "authority_role", "C12A" if s[0]["authority_role"] != "C12A" else "C11B"), r, c, e)),
            ("secondary_component_equality_flip", lambda: (p, changed(s, 0, "current_C15_components_equal", not s[0]["current_C15_components_equal"]), r, c, e)),
            ("secondary_R300C_flag_flip", lambda: (p, changed(s, 0, "R300C_validation_pair_not_used_as_universe_or_classifier", not s[0]["R300C_validation_pair_not_used_as_universe_or_classifier"]), r, c, e)),
            ("secondary_disposition_flip", lambda: (p, changed(s, 0, "disposition", "SUPPORT_EMPTY" if s[0]["disposition"] == "SUPPORT_POSITIVE" else "SUPPORT_POSITIVE"), r, c, e)),
            ("secondary_source_sign_flip", lambda: (p, changed(s, 0, "c24_side_sign", flip(s[0]["c24_side_sign"])), r, c, e)),
            ("secondary_target_sign_flip", lambda: (p, changed(s, 0, "target_whole_box_sign", flip(s[0]["target_whole_box_sign"])), r, c, e)),
            ("priority_missing_row", lambda: (p, s, r[:-1], c, e)),
            ("priority_SIGNED_overlap_injection", lambda: (p, s, changed(r, 0, "raw_signed_exact_pair", True), c, e)),
            ("priority_COMPLETE_overlap_injection", lambda: (p, s, changed(r, 0, "raw_complete_exact_pair", True), c, e)),
            ("priority_terminal_flip", lambda: (p, s, changed(r, 0, "assigned_terminal", "SIGNED_BOUNDARY_FACES"), c, e)),
            ("priority_source_receipt_flip", lambda: (p, s, changed(r, 0, "source_C24A_C22A_disposition_row_sha256", "6" * 64), c, e)),
            ("cross_missing_row", lambda: (p, s, r, c[:-1], e)),
            ("cross_component_pair_flip", lambda: (p, s, r, changed(c, 0, "ordered_C15_component_pair", list(reversed(c[0]["ordered_C15_component_pair"]))), e)),
            ("cross_source_receipt_flip", lambda: (p, s, r, changed(c, 0, "source_C24A_C22A_disposition_row_sha256", "7" * 64), e)),
            ("edge_missing_row", lambda: (p, s, r, c, e[:-1])),
            ("edge_overlap_flip", lambda: (p, s, r, c, changed(e, 0, "overlaps_C27R1D_strict_volume_edge", False))),
            ("edge_source_count_flip", lambda: (p, s, r, c, changed(e, 0, "source_member_pair_count", e[0]["source_member_pair_count"] + 1))),
            ("edge_source_pairs_drop", lambda: (p, s, r, c, changed(e, 0, "source_member_pairs", e[0]["source_member_pairs"][:-1]))),
        ])

        receipts: list[dict[str, Any]] = []
        for ordinal, (name, make) in enumerate(attacks):
            rejected = False
            reason = ""
            try:
                module.semantic_compare(*make())
            except (module.Failure, KeyError, TypeError, ValueError) as error:
                rejected = True
                reason = type(error).__name__ + ":" + str(error)
            need(rejected, "attack accepted:" + name)
            receipts.append({"ordinal": ordinal, "attack": name,
                             "closure_recomputed": name not in {
                                 "primary_missing_row", "primary_duplicate_row",
                                 "secondary_missing_row", "secondary_duplicate_row",
                                 "priority_missing_row", "cross_missing_row", "edge_missing_row"},
                             "expected": "REJECT", "observed": "REJECT",
                             "reason": reason})

        body = {
            "schema": "cm2.c27-independent.c24a-g2b-dual-comparator-attacks.v1",
            "status": "PASS_37_OF_37_COHERENT_ATTACKS_REJECTED__ZERO_CREDIT",
            "invocation_seed": args.seed,
            "baseline": baseline,
            "attack_count": len(receipts),
            "accepted_attack_count": 0,
            "rejected_attack_count": len(receipts),
            "receipts": receipts,
            "comparator_source_sha256": COMPARATOR_SHA256,
            "formal_credit": 0,
            "manifest_authorized": False,
            "CM2": "NO-GO_FOR_CLAIM",
        }
        need(len(receipts) == 37, "attack census")
        result = dict(body)
        result["semantic_projection_sha256"] = digest({
            key: value for key, value in body.items() if key != "invocation_seed"
        })
        result["result_sha256"] = digest(result)
        out = Path(args.out_dir)
        out.mkdir(parents=True, exist_ok=False)
        (out / "result.json").write_bytes(canonical(result) + b"\n")
    except (HarnessFailure, KeyError, TypeError, ValueError, OSError) as error:
        print("FAIL:" + str(error))
        return 2
    print(canonical({"status": result["status"],
                     "semantic_projection_sha256": result["semantic_projection_sha256"],
                     "result_sha256": result["result_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
