#!/usr/bin/env python3
"""Freeze the strict transverse-side ownership ledger for all rank-three gap tubes."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
FILES = {
    "round100": "cm2-round100-rank3-immutable-interior-gap-closure-2026-07-22.json",
    "round102": "cm2-round102-rank3-corrected-face-quotient-2026-07-22.json",
    "round107": "cm2-round107-rank3-adjacent-smooth-cell-atlas-2026-07-22.json",
    "round109": "cm2-round109-rank3-registered-arc-immutable-whole-tube-reaudit-2026-07-22.json",
}
PINS = {
    FILES["round100"]: "097849bf3da9d34a83ce9693ca68093ed2de7460cc51dcb26ce484c589f278d6",
    FILES["round102"]: "85069546fbc29f45af93eb65e2c2979bc83bfb5d744199771e234c2f7a1f0edb",
    FILES["round107"]: "bb6aeaa821174a1e1994eff2eb10046811b66dd7cf41c4e2d1c898b74d9dea74",
    FILES["round109"]: "fa5231f91f71da8014f9ca606702e3a59499adf78ce86ce09954bb424dae540e",
}
SCHEMA = "cm2.round110.rank3-gap-tube-side-decomposition.v1"


def digest(value: Any) -> str:
    rendered = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(rendered.encode()).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name: str, schema: str) -> dict[str, Any]:
    path = HERE / FILES[name]
    if sha256(path) != PINS[path.name]:
        raise RuntimeError(f"pin mismatch: {path.name}")
    document = json.loads(path.read_text())
    if document["schema"] != schema or digest(document["result"]) != document["result_sha256"]:
        raise RuntimeError(f"invalid closed document: {path.name}")
    return document["result"]


def gap_evidence_id(gap: dict[str, Any]) -> str:
    if gap["immutable_candidate_reaudit_method"] == "WHOLE_TUBE_IFT_CHAIN":
        return "WHOLE_TUBE_IFT_CHAIN:" + gap["certified_tube_boxes_sha256"]
    if gap["immutable_candidate_reaudit_method"] == "TRACKED_NODE_ROOT_CHAIN":
        return "TRACKED_NODE_ROOT_CHAIN:" + gap["tracked_boxes_sha256"]
    raise RuntimeError("unknown gap evidence method")


def gap_chain_status(gap: dict[str, Any]) -> str:
    return gap.get("whole_chain_third_event_status", gap.get("whole_chain_status", ""))


def build() -> dict[str, Any]:
    round100 = load("round100", "cm2.round100.rank3-immutable-interior-gap-closure.v1")
    round102 = load("round102", "cm2.round102.rank3-corrected-face-quotient.v1")
    round107 = load("round107", "cm2.round107.rank3-adjacent-smooth-cell-atlas.v1")
    round109 = load("round109", "cm2.round109.rank3-registered-arc-immutable-whole-tube-reaudit.v1")

    gap_by_endpoints = {
        frozenset((row["left_registered_port_id"], row["right_registered_port_id"])): row
        for row in round100["gap_rows"]
    }
    gap_links = sorted(
        (row for row in round102["interior_link_rows"] if row["link_type"] == "IMMUTABLE_CERTIFIED_INTERIOR_GAP"),
        key=lambda row: (row["face_id"], row["link_rank"]),
    )
    if len(gap_links) != 56 or len(gap_by_endpoints) != 56:
        raise RuntimeError("gap census changed")

    side_rows = []
    pair_rows = []
    for link in gap_links:
        endpoints = frozenset((link["left_registered_port_id"], link["right_registered_port_id"]))
        gap = gap_by_endpoints.get(endpoints)
        if gap is None or link["evidence_id"] != gap_evidence_id(gap):
            raise RuntimeError("Round102 gap incidence does not match Round100 evidence")
        pair_id = "physical-s0-rank3-gap-side-pair:" + digest({
            "face_id": link["face_id"], "link_rank": link["link_rank"], "endpoints": sorted(endpoints)
        })
        member_ids = []
        for discriminant_sign, side_label in ((-1, "BYPASS_SIDE"), (1, "DESIGNATED_COLLISION_SIDE")):
            row_key = {
                "pair_id": pair_id,
                "discriminant_strict_sign": discriminant_sign,
                "side_label": side_label,
            }
            side_id = "physical-s0-rank3-gap-transverse-side:" + digest(row_key)
            member_ids.append(side_id)
            side_rows.append({
                "gap_transverse_side_id": side_id,
                "gap_side_pair_id": pair_id,
                "face_id": link["face_id"],
                "link_rank": link["link_rank"],
                "left_registered_port_id": link["left_registered_port_id"],
                "right_registered_port_id": link["right_registered_port_id"],
                "source_core_index": gap["source_core_index"],
                "second_selected_target_id": gap["second_selected_target_id"],
                "third_candidate_id": gap["third_candidate_id"],
                "signed_transverse_tangency_factor_sign": gap["signed_transverse_tangency_factor_sign"],
                "discriminant_strict_sign": discriminant_sign,
                "side_label": side_label,
                "relative_transverse_parameter_sign": discriminant_sign * gap["signed_transverse_tangency_factor_sign"],
                "trace_boundary_owner": "ROUND102_CANONICAL_TANGENT_FACE",
                "side_domain_relation": "STRICT_D_LT_ZERO" if discriminant_sign < 0 else "STRICT_D_GT_ZERO",
                "whole_tangent_tube_evidence_id": gap_evidence_id(gap),
                "immutable_candidate_chain_status": gap_chain_status(gap),
                "open_transverse_collar_certified": False,
                "homogeneity_child_asserted": False,
                "Gate5_field_installed": False,
            })
        pair_rows.append({
            "gap_side_pair_id": pair_id,
            "face_id": link["face_id"],
            "link_rank": link["link_rank"],
            "member_side_ids": member_ids,
            "member_discriminant_signs": [-1, 1],
            "strict_side_domains_disjoint": True,
            "common_trace_excluded_from_both_open_sides": True,
            "common_trace_owner": "ROUND102_CANONICAL_TANGENT_FACE",
            "whole_tangent_tube_evidence_id": gap_evidence_id(gap),
        })

    factor_histogram = Counter(gap_by_endpoints[frozenset((row["left_registered_port_id"], row["right_registered_port_id"]))]["signed_transverse_tangency_factor_sign"] for row in gap_links)
    side_rows.sort(key=lambda row: (row["face_id"], row["link_rank"], row["discriminant_strict_sign"]))
    result = {
        "input_gap_tube_count": len(gap_links),
        "materialized_strict_transverse_side_record_count": len(side_rows),
        "complete_two_sided_gap_pair_count": len(pair_rows),
        "discriminant_sign_histogram": dict(sorted(Counter(row["discriminant_strict_sign"] for row in side_rows).items())),
        "side_label_histogram": dict(sorted(Counter(row["side_label"] for row in side_rows).items())),
        "signed_transverse_factor_histogram": dict(sorted(factor_histogram.items())),
        "trace_owned_by_canonical_face_count": len(pair_rows),
        "remaining_unsplit_gap_tube_count": len(gap_links) - len(pair_rows),
        "registered_arc_reaudit_count_carried": round109["certified_registered_arc_whole_tube_count"],
        "round107_local_face_pair_count_carried": round107["complete_two_sided_face_pair_count"],
        "gap_side_rows": side_rows,
        "gap_side_rows_sha256": digest(side_rows),
        "gap_side_pair_rows": pair_rows,
        "gap_side_pair_rows_sha256": digest(pair_rows),
        "strict_scope": "combinatorial strict-D side ownership decomposition of all 56 immutable-certified rank-three tangent gap tubes",
        "strict_nonclaims": [
            "the side rows are ownership records, not interval-certified positive-width transverse collars",
            "no whole-collar 57-candidate ordering is inferred from tangent-tube ordering",
            "no homogeneity child, canonical recut, F1-F6 slot, RN block, or global Gate5 promotion is installed",
            "the eight exterior endpoint collars and countable grazing families remain pending",
        ],
        "upstream_pins": PINS,
    }
    if Counter(row["discriminant_strict_sign"] for row in side_rows) != Counter({-1: 56, 1: 56}):
        raise RuntimeError("incomplete two-sided sign decomposition")
    if factor_histogram != Counter({-1: 28, 1: 28}):
        raise RuntimeError("transverse-factor census changed")
    result = json.loads(json.dumps(result, sort_keys=True))
    return {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(build(), sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
