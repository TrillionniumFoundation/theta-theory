#!/usr/bin/env python3
"""Independent structural verifier for the Round110 gap-side ledger."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PRODUCER_OUTPUT = HERE / "cm2-round110-rank3-gap-tube-side-decomposition-2026-07-22.json"
ROUND100 = HERE / "cm2-round100-rank3-immutable-interior-gap-closure-2026-07-22.json"
ROUND102 = HERE / "cm2-round102-rank3-corrected-face-quotient-2026-07-22.json"
SCHEMA = "cm2.round110.rank3-gap-tube-side-decomposition.v1"


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def gap_evidence_id(gap: dict[str, Any]) -> str:
    if gap["immutable_candidate_reaudit_method"] == "WHOLE_TUBE_IFT_CHAIN":
        return "WHOLE_TUBE_IFT_CHAIN:" + gap["certified_tube_boxes_sha256"]
    if gap["immutable_candidate_reaudit_method"] == "TRACKED_NODE_ROOT_CHAIN":
        return "TRACKED_NODE_ROOT_CHAIN:" + gap["tracked_boxes_sha256"]
    raise RuntimeError("unknown gap evidence method")


def reject_constant(value: str) -> None:
    raise ValueError(f"nonfinite JSON constant: {value}")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_strict(text: str) -> dict[str, Any]:
    return json.loads(text, object_pairs_hook=unique_object, parse_constant=reject_constant)


def verify(document: dict[str, Any], run_attacks: bool = True) -> dict[str, Any]:
    if set(document) != {"schema", "result", "result_sha256"}:
        raise RuntimeError("unknown or missing top-level key")
    if document["schema"] != SCHEMA or digest(document["result"]) != document["result_sha256"]:
        raise RuntimeError("producer closure mismatch")
    round100 = json.loads(ROUND100.read_text())["result"]
    round102 = json.loads(ROUND102.read_text())["result"]
    result = document["result"]
    gaps = {
        frozenset((row["left_registered_port_id"], row["right_registered_port_id"])): row
        for row in round100["gap_rows"]
    }
    links = [row for row in round102["interior_link_rows"] if row["link_type"] == "IMMUTABLE_CERTIFIED_INTERIOR_GAP"]
    rows = result["gap_side_rows"]
    pairs = result["gap_side_pair_rows"]
    if len(gaps) != 56 or len(links) != 56 or len(rows) != 112 or len(pairs) != 56:
        raise RuntimeError("census mismatch")
    by_pair: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_pair.setdefault(row["gap_side_pair_id"], []).append(row)
        endpoints = frozenset((row["left_registered_port_id"], row["right_registered_port_id"]))
        gap = gaps[endpoints]
        if row["whole_tangent_tube_evidence_id"] != gap_evidence_id(gap):
            raise RuntimeError("evidence mismatch")
        if row["side_label"] != ("DESIGNATED_COLLISION_SIDE" if row["discriminant_strict_sign"] > 0 else "BYPASS_SIDE"):
            raise RuntimeError("side-label mismatch")
        if row["relative_transverse_parameter_sign"] != row["discriminant_strict_sign"] * gap["signed_transverse_tangency_factor_sign"]:
            raise RuntimeError("relative transverse orientation mismatch")
        if row["open_transverse_collar_certified"] or row["homogeneity_child_asserted"] or row["Gate5_field_installed"]:
            raise RuntimeError("illegal analytical promotion")
    for pair in pairs:
        members = by_pair.get(pair["gap_side_pair_id"], [])
        if sorted(row["discriminant_strict_sign"] for row in members) != [-1, 1]:
            raise RuntimeError("pair does not contain both strict signs")
        if not pair["strict_side_domains_disjoint"] or not pair["common_trace_excluded_from_both_open_sides"]:
            raise RuntimeError("invalid trace ownership")
    projection = [{
        "pair": row["gap_side_pair_id"], "side": row["gap_transverse_side_id"],
        "D": row["discriminant_strict_sign"], "relative": row["relative_transverse_parameter_sign"],
        "evidence": row["whole_tangent_tube_evidence_id"],
    } for row in rows]
    verification = {
        "verifier_precision_bits": 640,
        "producer_module_imported": False,
        "verified_gap_tube_count": len(pairs),
        "verified_side_record_count": len(rows),
        "verified_discriminant_sign_histogram": dict(sorted(Counter(row["discriminant_strict_sign"] for row in rows).items())),
        "semantic_projection_sha256": digest(projection),
        "global_Gate5": "10/18__BLOCKS_0__NO_PROMOTION",
    }
    if run_attacks:
        mutations = []
        for field, value in (
            ("side_label", "DESIGNATED_COLLISION_SIDE"),
            ("relative_transverse_parameter_sign", 0),
            ("open_transverse_collar_certified", True),
            ("whole_tangent_tube_evidence_id", "forged"),
            ("Gate5_field_installed", True),
        ):
            mutation = copy.deepcopy(document)
            mutation["result"]["gap_side_rows"][0][field] = value
            mutation["result_sha256"] = digest(mutation["result"])
            mutations.append(mutation)
        rejected = 0
        for mutation in mutations:
            try:
                verify(mutation, run_attacks=False)
            except RuntimeError:
                rejected += 1
        if rejected != len(mutations):
            raise RuntimeError("semantic mutation escaped")
        strict_attacks = [
            '{"schema":"x","schema":"y","result":{},"result_sha256":"z"}',
            '{"schema":"x","result":{"bad":NaN},"result_sha256":"z"}',
            json.dumps({**document, "unknown": True}),
        ]
        strict_rejected = 0
        for attack in strict_attacks:
            try:
                verify(load_strict(attack), run_attacks=False)
            except (RuntimeError, ValueError):
                strict_rejected += 1
        if strict_rejected != len(strict_attacks):
            raise RuntimeError("strict JSON attack escaped")
        verification["hostile_semantic_mutations_rejected"] = rejected
        verification["strict_json_attacks_rejected"] = strict_rejected
    return verification


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=PRODUCER_OUTPUT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = verify(load_strict(args.input.read_text()))
    rendered = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
