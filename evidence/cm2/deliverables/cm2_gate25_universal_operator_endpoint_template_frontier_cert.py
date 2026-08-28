#!/usr/bin/env python3
"""Gate-2/5 universal operator and selected-endpoint template frontier.

This certificate binds the all-physical-branch Gate-4 estimates to the
Gate-5 field schema and binds the selected Gate-1 homoclinic loop to the
Gate-2 endpoint frontier.  It deliberately distinguishes universal/local
templates from completed word-indexed fields.  Characteristic restriction
to a return word, stable saturation and a common quotient branch remain
uncertified.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
Q = Fraction

DEPENDENCIES = (
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json",
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json",
    "cm2-gate25-roof-two-wall-chart-frontier-manifest-2026-07-16.json",
    "cm2-gate4-componentwise-global-growth-recovery-frontier-manifest-2026-07-16.json",
    "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json",
    "cm2-gate1-immutable-homoclinic-plaque-entry-frontier-manifest-2026-07-16.json",
    "cm2-gate1-numeric-holonomy-tail-twisting-frontier-manifest-2026-07-16.json",
    "cm2-gate2-collision-key-stable-quotient-frontier-manifest-2026-07-16.json",
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name: str) -> dict[str, Any]:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def build_result() -> dict[str, Any]:
    gate5 = load(DEPENDENCIES[0])
    cores = load(DEPENDENCIES[1])
    walls = load(DEPENDENCIES[2])
    growth = load(DEPENDENCIES[3])
    numeric = load(DEPENDENCIES[4])
    immutable = load(DEPENDENCIES[5])
    twisting = load(DEPENDENCIES[6])
    gate2 = load(DEPENDENCIES[7])

    schema = gate5["result"]["required_operator_field_schema"]
    assert schema["required_field_count_per_physical_homogeneous_level"] == 18
    assert schema["required_fields"][4:7] == [
        "inverse_Jacobian_bound",
        "log_Jacobian_distortion_sum",
        "one_step_cut_growth_Z_sum",
    ]
    assert schema["homogeneous_subbranch_ids_materialized"] is False

    core = cores["result"]["physical_return_core_registry"]
    assert core["candidate_key_universe_size"] == 441280
    assert core["distinct_certified_nonempty_key_lower_bound"] == 24
    assert core["physical_compact_homogeneous_core_count"] == 24
    assert core["all_cores_central_incoming_and_outgoing_homogeneity"] is True
    assert core["full_key_schema_field_completion"][
        "completed_field_count_on_each_of_24_keys"
    ] == 1

    wall = walls["result"]["roof_two_wall_chart_registry"]
    assert wall["all_28_core_local_roof_level_prefix_suffix_pairs_have_charts"]
    assert wall["all_52_core_local_split_slots_have_charts"]

    growth_summary = growth["replay_summary"]
    numeric_summary = numeric["replay_summary"]
    theta = Q(144000, 180337)
    tail = Q(1, 5)
    xi = theta + tail
    euclidean_inverse = Q(3807, 20) * theta
    assert xi == Q(900337, 901685)
    assert euclidean_inverse == Q(27410400, 180337)
    assert growth_summary["global_one_step_Xi_strict_upper"] == str(xi)
    assert growth_summary["delta_1"] == "1/37724355673552103994"
    assert numeric_summary["global_D_std_strict_upper"] == "30000000"
    assert numeric_summary["adapted_one_step_distortion"] == (
        "15000000000000000000000000"
    )
    assert numeric_summary["density_ratio"] == "2000/1999"

    adapted_distortion = 15_000_000_000_000_000_000_000_000
    canonical_length = Q(1, 10**90)
    canonical_log_variation = Q(adapted_distortion, 10**30)
    assert canonical_log_variation == Q(3, 200000)
    euclidean_length_upper = Q(27, 5) * canonical_length
    assert euclidean_length_upper < Q(1, 37724355673552103994)

    orbit = immutable["result"]["immutable_homoclinic_orbit"]
    loop = twisting["result"]
    assert orbit["selected_point_is_regular"] is True
    assert orbit["full_word_collision_count"] == 96
    assert loop["scope_limits"]["selected_immutable_homoclinic_loop_numeric_enclosure"]
    assert loop["scope_limits"]["four_selected_QNL_eigen_axis_twisting_wedges"]
    assert loop["scope_limits"]["global_faithful_coding"] is False
    assert loop["scope_limits"]["butler_park_class_H"] is False
    wedges = loop["four_selected_twisting_wedges"]
    assert len(wedges) == 4

    gate2_result = gate2["result"]
    assert gate2_result["quotient_reverse_endpoint_stopping_frontier"][
        "required_field_count"
    ] == 17
    assert gate2_result["completion"]["gate2_certified"] is False

    dependencies = {
        name: file_sha256(HERE / name) for name in DEPENDENCIES
    }
    result: dict[str, Any] = {
        "schema": "cm2.gate25.universal-operator-endpoint-template-frontier.v1",
        "provenance": {
            "frozen_dependency_sha256": dependencies,
            "parameter_window": ["-1/400", "1/400"],
            "Gate5_required_field_schema_sha256": schema[
                "required_field_schema_sha256"
            ],
        },
        "physical_return_registry_binding": {
            "candidate_key_universe_size": 441280,
            "certified_nonempty_key_lower_bound": 24,
            "positive_core_count": 24,
            "all_24_cores_central_incoming_and_outgoing": True,
            "all_28_core_local_roof_level_chart_pairs_physical": True,
            "all_52_core_local_split_slots_physical": True,
            "completed_full_key_field_count_on_each_of_24_keys": 1,
            "complete_18_field_block_count": 0,
        },
        "universal_full_collision_branch_templates": {
            "scope": (
                "every actual homogeneous physical solid-collision child on "
                "a canonical adapted standard curve; before return-word "
                "characteristic restriction"
            ),
            "canonical_adapted_length_upper": "1e-90",
            "canonical_euclidean_length_strict_upper": str(
                euclidean_length_upper
            ),
            "inside_componentwise_delta_1": True,
            "field_5_inverse_Jacobian_seed": {
                "central_child_adapted_inverse_strict_upper": str(theta),
                "high_strip_rank_k_adapted_inverse_strict_upper": "4/k^2",
                "universal_adapted_inverse_strict_upper": str(theta),
                "adapted_to_Euclidean_metric_factor_upper": "3807/20",
                "universal_Euclidean_inverse_Jacobian_strict_upper": str(
                    euclidean_inverse
                ),
                "physical_type": "adapted unstable one-dimensional Jacobian",
                "core_local_seed_on_all_24_positive_cores": True,
                "completed_full_key_roof_level_field": False,
            },
            "field_6_log_Jacobian_distortion_seed": {
                "all_standard_curve_constant": str(adapted_distortion),
                "Holder_exponent": "1/3",
                "canonical_curve_log_variation_strict_upper": str(
                    canonical_log_variation
                ),
                "core_local_seed_on_all_24_positive_cores": True,
                "completed_full_key_roof_level_field": False,
            },
            "pre_restriction_Growth_template": {
                "central_multiplicity_upper": 1,
                "high_strip_tail_strict_upper": str(tail),
                "one_step_Xi_strict_upper": str(xi),
                "margin": str(1 - xi),
                "not_field_7_after_word_restriction": True,
            },
        },
        "characteristic_restriction_blocker": {
            "word_domain_boundary_Z_bound": False,
            "chart_seam_and_owner_boundary_multiplicity_bound": False,
            "characteristic_restriction_preserves_regular_density_space": False,
            "characteristic_restriction_preserves_standard_family_cost": False,
            "reason": (
                "the global physical singularity/homogeneity Xi theorem does "
                "not charge the extra return-word/chart-owner characteristic "
                "boundaries"
            ),
            "Gate5_field_7_one_step_cut_growth_Z_sum_completed": False,
            "Gate5_fields_14_to_17_completed": False,
        },
        "selected_common_fiber_endpoint_seed": {
            "selected_physical_homoclinic_itinerary": orbit[
                "bi_infinite_itinerary"
            ],
            "selected_loop_matrix_in_QNL_eigenfiber_E_p": loop[
                "selected_homoclinic_holonomy"
            ]["infinite_matrix_enclosure"],
            "four_nonzero_QNL_eigen_axis_wedges": wedges,
            "selected_loop_numeric_matrix_seed": True,
            "selected_loop_twisting_seed": True,
            "physical_quotient_branch_label_a": False,
            "pointwise_endpoint_slope_identity": False,
            "same_carrier_endpoint_maps_X_Y": False,
            "endpoint_denominator_lower_bound": False,
            "Gate2_fields_9_to_12_completed": False,
        },
        "strict_completion_boundary": {
            "two_new_core_local_strong_field_seeds": [
                "inverse_Jacobian_bound",
                "log_Jacobian_distortion_sum",
            ],
            "universal_pre_restriction_Growth_template": True,
            "selected_common_fiber_loop_and_wedge_seed": True,
            "maximal_homogeneous_word_domains": False,
            "physical_homogeneity_subbranch_registry": False,
            "return_word_characteristic_boundary_Z": False,
            "stable_saturated_product_base": False,
            "quotient_rho_reverse_weights": False,
            "complete_18_field_operator_block_count": 0,
            "Gate2_completed_physical_field_count": 0,
            "Gate2": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
        },
    }
    result["internal_replay_digest"] = digest(result)
    return result


def main() -> int:
    result = build_result()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE5_CORE_LOCAL_INVERSE_JACOBIAN_SEED: CERTIFIED")
    print("GATE5_CORE_LOCAL_LOG_DISTORTION_SEED: CERTIFIED")
    print("RETURN_WORD_CHARACTERISTIC_BOUNDARY_Z: NOT_CERTIFIED")
    print("GATE2_SELECTED_COMMON_FIBER_LOOP_WEDGE_SEED: CERTIFIED")
    print("GATE2_STABLE_QUOTIENT_ENDPOINT_PACKET: NOT_CERTIFIED")
    print("GATE2: NOT_CERTIFIED")
    print("GATE5: NOT_CERTIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
