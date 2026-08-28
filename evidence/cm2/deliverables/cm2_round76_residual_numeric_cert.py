#!/usr/bin/env python3
"""Round-76 residual refinement and R2 numeric-field certificate."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round68_common import canonical_bytes, digest, require, sha256_path, strict_json_path


HERE = Path(__file__).resolve().parent
DEPTH16 = HERE / "cm2-round74-s0-depth2-adaptive-2026-07-21.json"
DEPTH20 = HERE / "cm2-round76-s0-depth20-residual-refinement-2026-07-21.json"
WITNESSES = HERE / "cm2-round74-s0-r2-pair-witnesses-2026-07-21.json"
ROUND75 = HERE / "cm2-round75-r2-physical-subquotient-manifest-2026-07-21.json"
NUMERIC = HERE / "cm2-round76-r2-numeric-fields-2026-07-21.json"
ROUND71 = HERE / "cm2-round71-r1-nonempty-face-germs-manifest-2026-07-21.json"
ROUND72 = HERE / "cm2-round72-r1-full-atlas-f10-f13-f16-manifest-2026-07-21.json"
RESIDUAL_GENERATOR = HERE / "cm2_round76_s0_depth20_residual_generator.py"
ADAPTIVE_GENERATOR = HERE / "cm2_round74_s0_depth2_adaptive_generator.py"
NUMERIC_GENERATOR = HERE / "cm2_round76_r2_numeric_fields_generator.py"
MANIFEST = HERE / "cm2-round76-residual-numeric-manifest-2026-07-21.json"
SCHEMA = "cm2.round76.residual-numeric.v1"


def build() -> dict[str, Any]:
    depth16 = strict_json_path(DEPTH16)["result"]
    depth20 = strict_json_path(DEPTH20)["result"]
    witnesses = strict_json_path(WITNESSES)["result"]
    round75 = strict_json_path(ROUND75)["result"]
    numeric = strict_json_path(NUMERIC)["result"]
    round71 = strict_json_path(ROUND71)["result"]["actual_local_field_attachment"]
    round72 = strict_json_path(ROUND72)["result"]["numeric_local_field_registry"]

    require(depth16["maximum_binary_depth"] == 16 and depth20["maximum_binary_depth"] == 20, "depths")
    require(depth20["terminal_leaf_count"] == 670724, "depth20 leaves")
    require(depth20["R2_strict_leaf_count"] == 23184, "depth20 R2 leaves")
    require(depth20["R2_rows_sha256"] == digest(depth20["R2_rows"]), "depth20 R2 digest")
    require(depth20["normalized_24_core_area_ledger"]["DEPTH2_OUTER"] == "8221/32768", "depth20 outer")
    require(depth20["normalized_24_core_area_ledger"]["R2_INNER"] == "5501/65536", "depth20 R2 area")

    expected_pairs = {(row["source_core_index"], row["destination_core_id"]): row["branch"] for row in witnesses["rows"]}
    observed_pairs = {(row["source_core_index"], row["destination_core_id"]) for row in depth20["R2_rows"]}
    require(observed_pairs == set(expected_pairs), "depth20 pair registry")
    branch_histogram = Counter(expected_pairs[(row["source_core_index"], row["destination_core_id"])] for row in depth20["R2_rows"])
    require(branch_histogram == {"main": 23136, "narrow_corner": 48}, "depth20 branch leaves")
    require(round75["physical_R2_curve_atlas"]["certified_components"] == len(observed_pairs) == 16, "Round75 pair join")

    outer16 = Q(depth16["normalized_24_core_area_ledger"]["DEPTH2_OUTER"])
    outer20 = Q(depth20["normalized_24_core_area_ledger"]["DEPTH2_OUTER"])
    r2_16 = Q(depth16["normalized_24_core_area_ledger"]["R2_INNER"])
    r2_20 = Q(depth20["normalized_24_core_area_ledger"]["R2_INNER"])
    require(outer20 < outer16 / 3 and r2_20 > r2_16, "refinement monotonicity")

    require(numeric["physical_R2_face_count"] == 32, "numeric face count")
    require(numeric["rows_sha256"] == digest(numeric["rows"]), "numeric rows digest")
    require(numeric["F8_common_normalized_transversality_dyadic_lower"] == "1/2", "F8")
    require(numeric["F9_32_face_integer_sum"] == numeric["F10_32_face_integer_sum"] == 32, "F9 F10 sums")
    require(numeric["F13_32_face_current_variation_strict_upper"] == numeric["F16_32_face_Piola_flux_cost_strict_upper"] == "5354421251/250000000000", "F13 F16")
    require(round71["F9_32_face_finite_sum_upper"] == "22138859900062518371942400", "R1 F9 pin")
    require(round72["F10_integer_sum"] == 480, "R1 F10 pin")

    result = {
        "scope": "fixed s=0 depth-20 residual refinement plus full numeric F8/F9/F10/F13/F16 rows on the 32 certified physical R2 faces",
        "depth20_residual_refinement": {
            "source_cores": depth20["source_core_count"],
            "maximum_binary_depth": depth20["maximum_binary_depth"],
            "terminal_leaves": depth20["terminal_leaf_count"],
            "classification_histogram": depth20["classification_histogram"],
            "normalized_area_ledger": depth20["normalized_24_core_area_ledger"],
            "certified_inner_normalized_area": str(Q(24) - outer20),
            "depth16_outer_area": str(outer16),
            "depth20_outer_area": str(outer20),
            "outer_contraction_ratio": str(outer20 / outer16),
            "outer_contraction_strictly_below_one_third": True,
            "depth16_R2_area_lower": str(r2_16),
            "depth20_R2_area_lower": str(r2_20),
            "R2_area_lower_gain": str(r2_20 - r2_16),
        },
        "strict_R2_pair_registry": {
            "strict_R2_leaves": depth20["R2_strict_leaf_count"],
            "source_cores": depth20["R2_source_core_count"],
            "source_destination_pairs": depth20["R2_source_destination_pair_count"],
            "known_Round75_component_pairs_recovered": len(observed_pairs),
            "new_strict_pairs_outside_Round75": 0,
            "main_branch_strict_leaves": branch_histogram["main"],
            "narrow_corner_strict_leaves": branch_histogram["narrow_corner"],
            "narrow_corner_pairs_first_visible_as_strict_leaves": 8,
            "R2_rows_sha256": depth20["R2_rows_sha256"],
            "status": "ALL_DEPTH20_STRICT_R2_LEAVES_LAND_IN_THE_16_ROUND75_PAIR_LABELS",
        },
        "physical_R2_numeric_fields": {
            "face_rows": numeric["physical_R2_face_count"],
            "F8_common_normalized_transversality_dyadic_lower": numeric["F8_common_normalized_transversality_dyadic_lower"],
            "F9_integer_range": [numeric["F9_integer_minimum"], numeric["F9_integer_maximum"]],
            "F9_32_face_integer_sum": numeric["F9_32_face_integer_sum"],
            "F10_integer_range": [numeric["F10_integer_minimum"], numeric["F10_integer_maximum"]],
            "F10_32_face_integer_sum": numeric["F10_32_face_integer_sum"],
            "F13_32_face_current_variation_strict_upper": numeric["F13_32_face_current_variation_strict_upper"],
            "F16_32_face_Piola_flux_cost_strict_upper": numeric["F16_32_face_Piola_flux_cost_strict_upper"],
            "second_order_Jet_variables": ["source_t", "source_p", "moving_parameter_s"],
            "rows_sha256": numeric["rows_sha256"],
        },
        "finite_cross_rank_field_sums": {
            "counting_measure": numeric["finite_cross_rank_counting_sum"],
            "geometric_depth_weight": numeric["finite_cross_rank_geometric_depth_weight_sum"],
            "geometric_weight_status": "CERTIFIED_FINITE_TWO_RANK_DEMONSTRATION",
            "official_limiting_path_law_status": "NOT_CERTIFIED",
        },
        "gate_effect": {
            "F8_F9_F10_F13_F16_on_all_32_R2_faces": "CERTIFIED",
            "F17_boundary_sector": round75["F14_F15_F17_attack"]["F17_boundary_sector"],
            "F17_official": "NOT_CERTIFIED",
            "complete_depth2_face_atlas": "NOT_CERTIFIED__DEPTH20_OUTER_AREA_8221_OVER_32768_REMAINS",
            "limiting_weighted_face_sum": "NOT_CERTIFIED__FINITE_GEOMETRIC_DEPTH_WEIGHT_IS_NOT_THE_PHYSICAL_PATH_LAW",
            "Gate4": "NOT_CERTIFIED__LANDING_JOIN_1_OF_7",
            "Gate5": "NOT_CERTIFIED__MATURITY_10_OF_18_BLOCKS_0",
            "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "strict_frontier": {
            "residual_candidate_exhaustion": "NOT_CERTIFIED__NO_NEW_STRICT_PAIR_AT_DEPTH20_DOES_NOT_EXCLUDE_AN_OPEN_COMPONENT_INSIDE_OUTER",
            "all_16_known_pair_labels_visible_in_strict_tree": "CERTIFIED_DEPTH20",
            "numeric_R2_field_rows": "CERTIFIED_32_OF_32",
            "finite_cross_rank_geometric_depth_sum": "CERTIFIED_TWO_RANK_ONLY",
            "arbitrary_depth_Rn_atlas": "NOT_CERTIFIED",
            "official_all_depth_weighted_sum": "NOT_CERTIFIED",
        },
    }
    pins = {
        path.name: sha256_path(path)
        for path in (
            DEPTH16,
            DEPTH20,
            WITNESSES,
            ROUND75,
            NUMERIC,
            ROUND71,
            ROUND72,
            RESIDUAL_GENERATOR,
            ADAPTIVE_GENERATOR,
            NUMERIC_GENERATOR,
        )
    }
    return {"schema": SCHEMA, "pins": pins, "result": result, "result_sha256": digest(result)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-json", action="store_true")
    args = parser.parse_args()
    document = build()
    if args.manifest_json:
        sys.stdout.buffer.write(canonical_bytes(document))
    else:
        print(json.dumps(document, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
