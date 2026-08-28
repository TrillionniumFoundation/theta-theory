#!/usr/bin/env python3
"""Gate-2 obstruction after the round-23 core/Kac entrance join.

Round 23 adds genuine physical data: 128 charged first-core entrance
cylinders, 14 reached destination cores/components, and four local
post-core return-current boxes.  This certificate audits those objects,
the positive 24-core collision-SRB registry, and the corrected Borel Kac
ledger against the frozen 17-field stable-quotient/PPE interface.

The result is exact and fail-closed.  None of the new objects is a
stable-saturated product base, stable projection, quotient density, reverse
weight, or native scale-stopping record.  A finite deterministic countermodel
also shows that positive core mass, complete labels, and exact signed Kac
centering can coexist with a Dirac reverse kernel and no pair-energy
contraction.  The countermodel is logical, not a CM2 dynamics model.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


Q = Fraction
HERE = Path(__file__).resolve().parent

DEPENDENCIES = {
    "cm2-gate2-collision-key-stable-quotient-frontier-manifest-2026-07-16.json": (
        "886c5feb8709ad26fd653e598edf344ba39cc3e08e6efbd02c9ad1133f784c65"
    ),
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json": (
        "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42"
    ),
    "cm2-gate45-corrected-maximal-row-kac-ledger-manifest-2026-07-15.json": (
        "d5f563545c4ddaddfbb6b5cde5c4f5d8030247209e2284c06aeb9d3255a771f0"
    ),
    "cm2-gate2-actual-stable-plaque-continuation-manifest-2026-07-15.json": (
        "1bfc3ea9f5eb587b41a94ba4fd808c03c309389269f8d5e903f9bfce09a4f871"
    ),
    "cm2-gate2-stable-saturation-scale-gap-manifest-2026-07-15.json": (
        "57bed82ae496750fa3c7d7202428c647e59b11029f823dc1752c93b9433ca0a7"
    ),
    "cm2-gate34-all-occurrence-first-core-stopping-manifest-2026-07-18.json": (
        "a40b52dcbeef8c9f3471115b2bbd2c438cc6e130c72bd619dd794d8925d97171"
    ),
    "cm2-gate34-local-core-return-tail-manifest-2026-07-18.json": (
        "d66c8da53846ae86c373de5917e706fa183bfca265f0e4fb83a9be1c204dd053"
    ),
    "cm2-gate345-occurrence-core-component-slot-join-manifest-2026-07-18.json": (
        "826c7773b2a4989df8293e79419561fd4f7768f7fcf9434905b3a2032241cd0a"
    ),
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_dependencies() -> dict[str, dict[str, Any]]:
    loaded: dict[str, dict[str, Any]] = {}
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        assert path.is_file()
        assert not path.is_symlink()
        assert path.resolve().parent == HERE
        assert sha256_path(path) == expected
        value = json.loads(path.read_text(encoding="utf-8"))
        assert isinstance(value, dict)
        loaded[name] = value

    gate2 = loaded[
        "cm2-gate2-collision-key-stable-quotient-frontier-manifest-2026-07-16.json"
    ]
    assert gate2["verdict"]["full_mass_2d_return_path_key_schema"] == "CERTIFIED"
    assert gate2["verdict"]["key_refined_2d_reverse_kernel"] == (
        "DIRAC_NO_CONTRACTION"
    )
    assert gate2["verdict"]["physical_PPE"] == "NOT_CERTIFIED"

    core = loaded[
        "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json"
    ]
    assert core["verdict"]["positive_mass_physical_core_registry"] == "CERTIFIED"
    assert core["verdict"]["stable_quotient_PPE"] == "NOT_CERTIFIED"

    kac = loaded[
        "cm2-gate45-corrected-maximal-row-kac-ledger-manifest-2026-07-15.json"
    ]
    assert kac["verdict"]["corrected_128_coordinate_Borel_Kac_layer"] == (
        "CERTIFIED"
    )
    assert kac["verdict"]["physical_recovery_and_CM2_norm_lifts"] == (
        "NOT_CERTIFIED"
    )

    plaque = loaded[
        "cm2-gate2-actual-stable-plaque-continuation-manifest-2026-07-15.json"
    ]
    assert plaque["proved_layers"]["two_local_physical_branches_in_common_rectangle"]
    assert plaque["physical_inputs"]["common_invariant_stable_holonomy"] is False

    stopping = loaded[
        "cm2-gate34-all-occurrence-first-core-stopping-manifest-2026-07-18.json"
    ]
    assert stopping["verdict"]["charged_first_core_stopping_cylinders_128"] == (
        "CERTIFIED"
    )

    local = loaded[
        "cm2-gate34-local-core-return-tail-manifest-2026-07-18.json"
    ]
    assert local["verdict"]["local_first_return_current_cylinders_3"] == (
        "CERTIFIED"
    )
    assert local["verdict"]["full_24_core_induced_operator"] == "NOT_CERTIFIED"

    join = loaded[
        "cm2-gate345-occurrence-core-component-slot-join-manifest-2026-07-18.json"
    ]
    assert join["verdict"]["occurrence_core_component_slot_join_64_128_14"] == (
        "CERTIFIED"
    )
    assert join["verdict"]["complete_physical_Kac"] == "NOT_CERTIFIED"
    return loaded


def round23_precursor_inventory(
    loaded: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    core = loaded[
        "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json"
    ]["result"]
    stopping = loaded[
        "cm2-gate34-all-occurrence-first-core-stopping-manifest-2026-07-18.json"
    ]["result"]
    local = loaded[
        "cm2-gate34-local-core-return-tail-manifest-2026-07-18.json"
    ]["result"]
    join = loaded[
        "cm2-gate345-occurrence-core-component-slot-join-manifest-2026-07-18.json"
    ]["result"]
    kac = loaded[
        "cm2-gate45-corrected-maximal-row-kac-ledger-manifest-2026-07-15.json"
    ]["result"]

    core_registry = core["physical_return_core_registry"]
    stop_registry = stopping["all_occurrence_first_core_stopping_registry"]
    return_registry = local["local_core_return_tail_registry"]
    join_registry = join["occurrence_core_component_slot_join_registry"]
    kac_ledger = kac["corrected_global_occurrence_ledger"]
    kac_layer = kac["corrected_global_finite_borel_kac_layer"]

    assert core_registry["physical_compact_homogeneous_core_count"] == 24
    assert core_registry[
        "collision_SRB_normalized_mass_strict_lower_using_pi_lt_22_over_7"
    ] == "147/550000"
    assert stop_registry["first_core_stopping_cylinder_count"] == 128
    assert stop_registry["distinct_destination_core_count"] == 14
    assert stopping["strict_nonpromotion"][
        "positive_cylinders_cover_entire_maximal_rows"
    ] is False
    assert return_registry["materialized_source_current_box_count"] == 4
    assert return_registry["finite_first_return_current_cylinder_count"] == 3
    assert local["strict_nonpromotion"][
        "source_current_boxes_are_full_collision_core_rectangles"
    ] is False
    assert join_registry["maximal_occurrence_owner_count"] == 64
    assert join_registry["parameter_branch_count"] == 128
    assert join_registry["distinct_destination_core_count"] == 14
    assert kac_ledger["maximal_physical_occurrence_count"] == 64
    assert kac_ledger["singular_kac_coordinate_count"] == 128
    assert kac_layer["four_term_centered_algebra_exact"] is True
    assert kac["completion"]["physical_four_term_Kac_CM2_typing"] is False

    return {
        "positive_collision_core_count": 24,
        "positive_collision_SRB_mass_strict_lower": "147/550000",
        "core_registry_scope": core_registry["strict_scope"],
        "charged_first_core_entrance_cylinder_count": 128,
        "entrance_destination_core_count": 14,
        "entrance_cylinders_cover_entire_occurrence_rows": False,
        "local_source_current_box_count": 4,
        "local_finite_first_return_current_cylinder_count": 3,
        "local_boxes_are_full_2d_collision_core_rectangles": False,
        "local_equal_coordinate_fraction_is_collision_SRB_probability": False,
        "occurrence_owner_count": 64,
        "parameter_side_record_count": 128,
        "reached_selected_component_count": 14,
        "corrected_positive_occurrence_law_count": 64,
        "singular_Kac_coordinate_count": 128,
        "finite_Borel_four_term_Kac_algebra": "CERTIFIED",
        "physical_four_term_Kac_CM2_typing": "NOT_CERTIFIED",
        "core_rows_sha256": core_registry["rows_sha256"],
        "first_stopping_branch_rows_sha256": stop_registry[
            "first_stopping_branch_rows_sha256"
        ],
        "local_return_rows_sha256": return_registry["local_return_ledger_rows_sha256"],
        "occurrence_to_core_sha256": join_registry["occurrence_to_core_sha256"],
        "corrected_occurrence_rows_sha256": kac_ledger[
            "corrected_occurrence_rows_sha256"
        ],
    }


def axis_type_guard(loaded: dict[str, dict[str, Any]]) -> dict[str, Any]:
    registry = loaded[
        "cm2-gate345-occurrence-core-component-slot-join-manifest-2026-07-18.json"
    ]["result"]["occurrence_core_component_slot_join_registry"]
    axes = registry["independent_axis_typing_guard"]
    assert axes["parameter_side_axis"]["values"] == ["hit", "miss"]
    assert axes["recovery_orientation_axis"]["values"] == ["fw", "rev"]
    assert axes["singular_kac_coordinate_axis"]["values"] == [
        "dot(S)h",
        "dot(r)*mu(h)",
    ]
    assert axes["axes_are_not_positionally_zipped"] is True
    return {
        "parameter_side_axis": ["hit", "miss"],
        "recovery_orientation_axis": ["fw", "rev"],
        "singular_Kac_coordinate_axis": ["dot(S)h", "dot(r)*mu(h)"],
        "Gate2_inverse_branch_axis": "a in connected stable-quotient return branches",
        "Gate2_reverse_weight_axis": "p_a(x) over physical inverse branches",
        "parameter_side_is_Gate2_inverse_branch": False,
        "recovery_orientation_is_Gate2_inverse_branch": False,
        "singular_Kac_coordinate_is_Gate2_inverse_branch": False,
        "destination_core_label_is_stable_projection_fibre": False,
        "axes_are_not_positionally_zipped": True,
        "fake_Gate2_branch_rows_materialized": 0,
    }


def gate2_field_nonpromotion(
    loaded: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    gate2 = loaded[
        "cm2-gate2-collision-key-stable-quotient-frontier-manifest-2026-07-16.json"
    ]["result"]
    frontier = gate2["quotient_reverse_endpoint_stopping_frontier"]
    fields = frontier["required_fields"]
    flags = frontier["physical_completion_flags"]
    assert len(fields) == 17
    assert set(fields) == set(flags)
    assert not any(flags.values())

    candidate_and_reason = {
        "stable_saturated_product_base_Lambda_A": (
            "24_core_union",
            "positive compact collision subcores are not a stable-saturated product base",
        ),
        "reference_unstable_interval_I_A": (
            "actual_unstable_curve_candidate",
            "candidate is not registered as the quotient reference of Lambda_A",
        ),
        "stable_holonomy_projection_pi_s": (
            "destination_core_label",
            "a finite core label is not a stable-leaf projection map",
        ),
        "stable_holonomy_conditional_SRB_Jacobian": (
            "collision_SRB_area_Jacobian_seed",
            "area invariance is not the conditional stable-holonomy Jacobian",
        ),
        "connected_first_return_strip_partition": (
            "three_local_return_current_cylinders",
            "fixed-parameter source curves are not full 2d stable-saturated strips",
        ),
        "onto_full_image_quotient_branches_h_a": (
            "128_first_core_entrance_cylinders",
            "entrance cylinders are neither returns nor onto quotient inverse branches",
        ),
        "quotient_density_rho_with_upper_lower_bounds": (
            "positive_collision_SRB_core_mass",
            "a mass lower bound is not a quotient density with pointwise bounds",
        ),
        "physical_reverse_weights_p_a": (
            "hit_miss_and_fw_rev_axes",
            "parameter sides and recovery views are not conditional reverse weights",
        ),
        "transported_projective_matrix_M_a_in_one_trivialisation": (
            "core_component_operator_binding",
            "the binding has no complete homogeneous derivative/operator block",
        ),
        "same_carrier_endpoint_maps_X_Y": (
            "source_target_core_charts",
            "local charts do not identify two endpoint maps on one quotient carrier",
        ),
        "endpoint_denominator_lower_bound": (
            "local_first_hit_margins",
            "collision margins do not bound the quotient projective denominator",
        ),
        "nonzero_endpoint_wedge": (
            "selected_Gate1_twisting_wedges",
            "Gate1 cocycle wedges are not typed on Gate2 quotient branch labels",
        ),
        "inverse_cylinder_diameter_registry": (
            "first_core_stopping_times",
            "time-to-core is not a two-sided inverse-cylinder diameter bound",
        ),
        "native_scale_prefix_stopping_antichain": (
            "128_first_core_stopping_words",
            "first-core stopping is not native quotient scale stopping",
        ),
        "overshoot_cemetery_and_two_sided_scale_comparison": (
            "one_local_survivor_through_2018",
            "a censored local survivor is not an overshoot cemetery or scale comparison",
        ),
        "off_diagonal_projective_near_collision_bound": (
            "Gate2_pair_energy_theorem",
            "the theorem is conditional and the current reverse kernel remains Dirac",
        ),
        "parentwise_normalized_amplitude_moment": (
            "single_q_and_Borel_Kac_ledgers",
            "occurrence charge and Kac centering are not parentwise quotient amplitudes",
        ),
    }
    assert set(candidate_and_reason) == set(fields)
    rows = [
        {
            "index": index,
            "field": field,
            "candidate_precursor": candidate_and_reason[field][0],
            "nonpromotion_reason": candidate_and_reason[field][1],
            "physical_completion": False,
        }
        for index, field in enumerate(fields, start=1)
    ]
    assert len(rows) == 17
    return {
        "required_field_count": 17,
        "completed_physical_field_count_before_round23": 0,
        "completed_physical_field_count_after_round23": 0,
        "new_physical_Gate2_field_promotions": 0,
        "first_missing_object": "stable_saturated_product_base_Lambda_A",
        "first_reverse_kernel_missing_object": "stable_holonomy_projection_pi_s",
        "field_rows": rows,
        "field_rows_sha256": canonical_digest(rows),
        "all_fields_share_one_physical_branch_registry": False,
    }


def exact_core_kac_nonimplication_countermodel() -> dict[str, Any]:
    # 128 deterministic tagged states carry full positive mass.  Their
    # identity dynamics has a Dirac reverse law.  Group them into 64 owners,
    # attach the two signed Kac coordinates (+1,-1), and map them onto 14
    # destination labels.  Positivity, label coverage and exact Kac centering
    # all hold, while no stable collapse or pair-energy contraction appears.
    state_count = 128
    owner_count = 64
    destination_label_count = 14
    state_mass = Q(1, state_count)
    total_mass = state_count * state_mass
    signed_kac_sum = owner_count * (Q(1) - Q(1))
    reverse_support_sizes = [1] * state_count
    reverse_weight_square_sums = [Q(1)] * state_count

    assert total_mass == 1
    assert signed_kac_sum == 0
    assert set(reverse_support_sizes) == {1}
    assert set(reverse_weight_square_sums) == {Q(1)}
    assert state_count >= destination_label_count

    payload = {
        "state_count": state_count,
        "map": "identity_on_128_tagged_states",
        "state_mass": str(state_mass),
        "owner_count": owner_count,
        "parameter_tags_per_owner": ["hit", "miss"],
        "destination_label_count": destination_label_count,
        "Kac_mark_per_owner": [1, -1],
    }
    return {
        **payload,
        "total_positive_mass": str(total_mass),
        "global_signed_Kac_sum": str(signed_kac_sum),
        "reverse_support_size_at_every_state": 1,
        "reverse_weight_square_sum_at_every_state": "1",
        "two_copy_diagonal_pair_energy_coefficient": "1",
        "strict_pair_energy_contraction_kappa_lt_1": False,
        "stable_saturated_product_base_created": False,
        "positive_core_mass_plus_exact_Kac_implies_PPE": False,
        "countermodel_scope": (
            "logical type nonimplication only; not a CM2 dynamics counterexample"
        ),
        "countermodel_payload_sha256": canonical_digest(payload),
    }


def shortest_new_physical_input() -> dict[str, Any]:
    return {
        "first_required_object": "stable_saturated_product_base_Lambda_A",
        "minimal_payload": [
            "positive-SRB product rectangle Lambda_A with interval-indexed invariant stable plaques",
            "reference unstable interval I_A",
            "physical stable projection pi_s:Lambda_A->I_A",
            "conditional SRB stable-holonomy Jacobian with explicit bounds",
        ],
        "next_dependent_payload": [
            "connected first-return strips saturated by those plaques",
            "onto quotient inverse branches h_a on I_A",
            "quotient density rho and reverse weights p_a",
        ],
        "why_no_current_substitute": (
            "collision cores, source-current boxes, occurrence charges and Borel Kac "
            "coordinates live on different carriers and do not define stable fibres"
        ),
    }


def build_result() -> dict[str, Any]:
    loaded = load_dependencies()
    result: dict[str, Any] = {
        "schema": "cm2.gate2.round23-core-kac-quotient-obstruction.v1",
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "audit_policy": "carrier_and_branch_type_exact_nonpromotion",
        },
        "round23_precursor_inventory": round23_precursor_inventory(loaded),
        "axis_type_guard": axis_type_guard(loaded),
        "Gate2_17_field_nonpromotion": gate2_field_nonpromotion(loaded),
        "exact_core_kac_nonimplication_countermodel": (
            exact_core_kac_nonimplication_countermodel()
        ),
        "shortest_new_physical_input": shortest_new_physical_input(),
        "strict_nonpromotion": {
            "24_core_union_is_stable_saturated_product_base": False,
            "destination_core_id_is_stable_projection": False,
            "first_core_stopping_word_is_native_scale_stop": False,
            "local_return_current_box_is_stable_saturated_return_strip": False,
            "collision_SRB_core_mass_is_quotient_density": False,
            "parameter_or_recovery_axis_is_reverse_branch_axis": False,
            "Borel_Kac_coordinates_are_parentwise_PPE_amplitudes": False,
            "new_Gate2_fields_promoted": 0,
            "physical_PPE": "NOT_CERTIFIED",
            "Gate2": "NOT_CERTIFIED",
        },
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def main() -> None:
    print(json.dumps(build_result(), indent=2, sort_keys=True))
    print("ROUND23_CORE_KAC_GATE2_PRECURSOR_AUDIT: CERTIFIED")
    print("GATE2_FIELD_PROMOTION_AFTER_ROUND23: 0/17")
    print("CORE_KAC_TO_PPE_NONIMPLICATION: CERTIFIED")
    print("PHYSICAL_STABLE_QUOTIENT_PPE: NOT_CERTIFIED")
    print("GATE2: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
