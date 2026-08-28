#!/usr/bin/env python3
"""Integrate the reverse-line closure into the registered rank-three frontier."""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round79_tangency_intersection_generator import digest
import cm2_round84_reverse_common_tangent_closure_generator as reverse_generator


HERE = Path(__file__).resolve().parent
PREFILTER = HERE / "cm2-round82-rank3-intersection-prefilter-2026-07-21.json"
JOINS = HERE / "cm2-round82-rank3-cross-tube-joins-2026-07-21.json"
PRIMARY = HERE / "cm2-round83-common-tangent-line-krawczyk-2026-07-22.json"
DEGENERATE = HERE / "cm2-round83-degenerate-interface-resolution-2026-07-22.json"
CENTERED = HERE / "cm2-round83-centered-line-refinement-2026-07-22.json"
ROUND83_MANIFEST = HERE / "cm2-round83-common-tangent-frontier-manifest-2026-07-22.json"
ROUND83_SHA = HERE / "cm2-eighty-third-direct-assault-manifest-2026-07-22.sha256"
ROUND82_SHA = HERE / "cm2-eighty-second-direct-assault-manifest-2026-07-21.sha256"
REVERSE = HERE / "cm2-round84-reverse-common-tangent-closure-2026-07-22.json"
ROUND83_SHA_LEDGER_SHA256 = "b8892b6c7f3f32c5a4835519c8e86309df9faec08263fba79efcc4ce9ff8526d"
ROUND82_SHA_LEDGER_SHA256 = "ba6856a54f5a112fb349d3a8d3961b7c6e21f021529bb86af521b1d3293ec93d"


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_document(document: dict[str, Any]) -> None:
    if document.get("result_sha256") != digest(document.get("result")):
        raise RuntimeError(f"bad result digest for schema {document.get('schema')}")


def ledger_entries(path: Path, expected_digest: str) -> dict[str, str]:
    if file_digest(path) != expected_digest:
        raise RuntimeError(f"frozen ledger digest changed: {path.name}")
    entries = {}
    for line in path.read_text().splitlines():
        sha256, relative = line.split("  ", 1)
        if relative in entries or len(sha256) != 64:
            raise RuntimeError(f"malformed frozen ledger: {path.name}")
        entries[relative] = sha256
    return entries


def require_ledger_pin(entries: dict[str, str], path: Path) -> None:
    relative = str(path.relative_to(HERE.parent))
    if entries.get(relative) != file_digest(path):
        raise RuntimeError(f"frozen ledger pin mismatch: {relative}")


def validate_reverse_document(document: dict[str, Any]) -> None:
    if set(document) != {"schema", "result", "result_sha256"}:
        raise RuntimeError("Round-84 reverse evidence top-level schema is not closed")
    if document["schema"] != "cm2.round84.reverse-common-tangent-closure.v1":
        raise RuntimeError("Round-84 reverse evidence schema")
    verify_document(document)
    if document != reverse_generator.build(512):
        raise RuntimeError("Round-84 reverse evidence is not the exact 512-bit closed-schema producer output")


def build() -> dict[str, Any]:
    prefilter_document = load(PREFILTER)
    joins_document = load(JOINS)
    primary_document = load(PRIMARY)
    degenerate_document = load(DEGENERATE)
    centered_document = load(CENTERED)
    reverse_document = load(REVERSE)
    for document in (
        prefilter_document, joins_document, primary_document,
        degenerate_document, centered_document, reverse_document,
    ):
        verify_document(document)
    round82_entries = ledger_entries(ROUND82_SHA, ROUND82_SHA_LEDGER_SHA256)
    round83_entries = ledger_entries(ROUND83_SHA, ROUND83_SHA_LEDGER_SHA256)
    for path in (PREFILTER, JOINS):
        require_ledger_pin(round82_entries, path)
    for path in (PRIMARY, DEGENERATE, CENTERED, ROUND83_MANIFEST):
        require_ledger_pin(round83_entries, path)
    validate_reverse_document(reverse_document)
    prefilter = prefilter_document["result"]
    joins = joins_document["result"]
    primary = primary_document["result"]
    degenerate = degenerate_document["result"]
    centered = centered_document["result"]
    reverse = reverse_document["result"]

    live_pairs = {
        (row["left_physical_root_component_id"], row["right_physical_root_component_id"])
        for row in centered["pair_rows"] if row["unresolved_leaf_count"]
    }
    reverse_live_rows = [
        row for row in reverse["pair_rows"]
        if (row["left_physical_root_component_id"], row["right_physical_root_component_id"]) in live_pairs
    ]
    live_pair_ranks = {row["pair_rank"] for row in reverse_live_rows}
    live_target_histogram = Counter(
        row["status"] for row in reverse["target_rows"] if row["pair_rank"] in live_pair_ranks
    )
    live_box_count = sum(row["input_hard_box_count"] for row in reverse_live_rows)
    live_input_area = sum(
        Q(row["input_hard_box_area"])
        for row in centered["pair_rows"] if row["unresolved_leaf_count"]
    )
    live_leaf_count = sum(row["unresolved_leaf_count"] for row in centered["pair_rows"])

    partition = {
        "different_candidate_unique_overlap_box_count": prefilter["different_candidate_unique_overlap_box_count"],
        "round82_strictly_excluded_box_count": prefilter["strictly_excluded_overlap_box_count"],
        "round83_positive_area_strictly_disjoint_box_count": primary["box_status_histogram"]["CERTIFIED_DISJOINT"],
        "round83_degenerate_interface_strictly_disjoint_box_count": degenerate["certified_disjoint_degenerate_box_count"],
        "round84_reverse_preimage_strictly_disjoint_box_count": reverse["certified_disjoint_hard_box_count"],
        "identity": "165608=127732+21154+16108+614",
    }
    result = {
        "fixed_parameter": "s=0",
        "round83_accounting_correction": {
            "input_hard_component_pair_count": reverse["input_hard_component_pair_count"],
            "input_hard_box_count": reverse["input_hard_box_count"],
            "centered_closed_component_pair_count": reverse["post_centered_closed_component_pair_count"],
            "centered_closed_input_hard_box_count": reverse["input_hard_box_count"] - live_box_count,
            "post_centered_live_component_pair_count": reverse["post_centered_live_component_pair_count"],
            "post_centered_live_input_hard_box_count": live_box_count,
            "post_centered_live_input_area": str(live_input_area),
            "post_centered_unresolved_leaf_count": live_leaf_count,
        },
        "reverse_common_tangent_closure": {
            "precision_bits": reverse["precision_bits"],
            "oriented_target_count": reverse["oriented_common_tangent_target_count"],
            "unit_normal_identity_overlap_count": reverse["unit_normal_identity_overlap_count"],
            "candidate_signed_distance_identity_overlap_count": reverse["candidate_signed_distance_identity_overlap_count"],
            "target_status_histogram": reverse["target_status_histogram"],
            "inverse_enclosure_count": reverse["inverse_enclosure_count"],
            "forward_replay_overlap_count": reverse["forward_replay_overlap_count"],
            "source_core_separation_count": reverse["uniformly_source_core_separated_inverse_count"],
            "source_core_coordinate_separation_lower": reverse["uniform_core_coordinate_separation_lower"],
            "hard_box_comparison_count": reverse["inverse_hard_box_comparison_count"],
            "hard_box_coordinate_separation_lower": reverse["uniform_coordinate_separation_lower"],
            "strictly_separated_hard_box_comparison_count": reverse["uniformly_separated_box_comparison_count"],
            "unresolved_target_count": reverse["unresolved_target_count"],
            "live_40_target_status_histogram": dict(sorted(live_target_histogram.items())),
        },
        "complete_registered_intersection_atlas": {
            "box_partition": partition,
            "round82_box_connectivity_aggregate_count": joins["joined_physical_root_component_count"],
            "registered_zero_set_component_count": "NOT_CERTIFIED",
            "different_candidate_registered_aggregate_pair_count": prefilter["different_candidate_component_pair_count"],
            "registered_different_candidate_intersection_count": 0,
            "cross_candidate_registered_patch_identification_count": 0,
            "remaining_unresolved_overlap_box_count": reverse["remaining_hard_box_count"],
            "status": "CERTIFIED_RELATIVE_TO_PINNED_PATCH_REGISTRY",
        },
        "face_and_RN_eligibility": {
            "same_candidate_local_zero_set_connectivity": "NOT_CERTIFIED",
            "same_candidate_uncovered_gap_continuation": "NOT_CERTIFIED",
            "internal_endpoint_atlas": "NOT_CERTIFIED",
            "complete_physical_rank3_face_rows": 0,
            "rank3_F8_F9_F10_F13_F16_rows": 0,
            "rank3_return_face_RN_rows": 0,
            "uniform_physical_rank_transition_contraction": "NOT_CERTIFIED",
            "all_rank_RN_summability": "NOT_CERTIFIED",
        },
        "gate4_frontier": {
            "fixed_s0_depth2_cellular_square": "CERTIFIED_ROUND81",
            "same_key_all_depth_stable_material_crosswalk": "NOT_CERTIFIED",
            "all_depth_commuting_square_family": "NOT_CERTIFIED",
        },
        "legacy_round83_audit_scope": {
            "frozen_bytes_preserved": True,
            "configured_hostile_semantic_suite": "12/12_REJECTED",
            "strict_json_suite": "4/4_REJECTED",
            "closed_schema_all_scalar_semantic_coverage": "NOT_CERTIFIED",
            "round84_requires_exact_closed_schema_validation": True,
        },
        "strict_state": {
            "gate1": "NOT_CERTIFIED",
            "gate2": "0/17",
            "gate3": "NOT_CERTIFIED",
            "gate4": "1/7",
            "gate5": "10/18",
            "gate5_complete_blocks": 0,
            "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "strict_nonclaims": [
            "registered different-candidate intersection closure is relative to the pinned certified patch registry",
            "intersection closure does not certify same-candidate uncovered-gap continuation or internal endpoints",
            "the 1672 Round-82 rows are box-connectivity aggregates, not certified zero-set components or complete physical faces",
            "rank-three tangency subdivision components are not renamed return-face RN rows",
            "fixed-s=0 intersection closure is not an all-depth Gate-4 crosswalk",
            "finite rank-three intersection closure is not a physical rank-transition tail contraction",
        ],
    }
    expected_live_histogram = {
        "INVERSE_STRICTLY_SEPARATED": 40,
        "MISS_FIRST": 108,
        "MISS_SECOND": 168,
        "MISS_SOURCE": 4,
    }
    if result["round83_accounting_correction"] != {
        "input_hard_component_pair_count": 42,
        "input_hard_box_count": 614,
        "centered_closed_component_pair_count": 2,
        "centered_closed_input_hard_box_count": 54,
        "post_centered_live_component_pair_count": 40,
        "post_centered_live_input_hard_box_count": 560,
        "post_centered_live_input_area": "173/20480000",
        "post_centered_unresolved_leaf_count": 11840,
    }:
        raise RuntimeError("Round-83 prospective accounting correction")
    if dict(live_target_histogram) != expected_live_histogram:
        raise RuntimeError("post-centered live target histogram")
    if partition != {
        "different_candidate_unique_overlap_box_count": 165608,
        "round82_strictly_excluded_box_count": 127732,
        "round83_positive_area_strictly_disjoint_box_count": 21154,
        "round83_degenerate_interface_strictly_disjoint_box_count": 16108,
        "round84_reverse_preimage_strictly_disjoint_box_count": 614,
        "identity": "165608=127732+21154+16108+614",
    }:
        raise RuntimeError("complete overlap partition")
    if reverse["remaining_hard_box_count"] != 0 or reverse["unresolved_target_count"] != 0:
        raise RuntimeError("reverse frontier is not closed")
    pins = {
        "round82_intersection_prefilter": file_digest(PREFILTER),
        "round82_cross_tube_joins": file_digest(JOINS),
        "round83_common_tangent_primary": file_digest(PRIMARY),
        "round83_degenerate_interfaces": file_digest(DEGENERATE),
        "round83_centered_frontier": file_digest(CENTERED),
        "round83_integrated_manifest": file_digest(ROUND83_MANIFEST),
        "round83_sha_ledger": file_digest(ROUND83_SHA),
        "round82_sha_ledger": file_digest(ROUND82_SHA),
        "round84_reverse_closure": file_digest(REVERSE),
    }
    return {
        "schema": "cm2.round84.registered-intersection-frontier.v1",
        "pins": pins,
        "result": result,
        "result_sha256": digest(result),
    }


def main() -> int:
    json.dump(build(), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
