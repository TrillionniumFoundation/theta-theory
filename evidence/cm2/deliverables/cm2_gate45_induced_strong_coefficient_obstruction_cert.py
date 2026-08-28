#!/usr/bin/env python3
"""Fail-closed Gate-4/5 open-to-induced operator obstruction.

Round 23 supplies an exact entrance join from 64 occurrence owners and 128
parameter-side cylinders to 14 selected roof-one core components.  This leaf
audits that join against the frozen fixed-core Growth coefficient and the
Gate-5 18-field schema.

The coefficient ``b_core`` belongs to the open operator ``O=L M_C``.  A
first-return operator instead contains complementary intermediate guards,

    R_n = M_C L (M_{C^c} L)^(n-1) M_C.

An exact two-state countermodel proves that a power bound for ``O`` alone
cannot be transferred to ``R_n``: for a map swapping the core and its
complement, ``O^2=0`` while ``R_2=M_C`` has l1 operator norm one.  This is a
logical operator-signature countermodel, not a counterexample to CM2.

The leaf also freezes the exact 4/18 selected-component maturity boundary,
including the fact that fields 5 and 6 are component-local seeds rather than
completed homogeneous roof-level slots.  No physical trajectory is promoted
to a common strong-space induced operator.
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
    "cm2-gate345-occurrence-core-component-slot-join-manifest-2026-07-18.json": (
        "826c7773b2a4989df8293e79419561fd4f7768f7fcf9434905b3a2032241cd0a"
    ),
    "cm2-gate34-local-core-return-tail-manifest-2026-07-18.json": (
        "d66c8da53846ae86c373de5917e706fa183bfca265f0e4fb83a9be1c204dd053"
    ),
    "cm2-gate4-fixed-core-green-kernel-unbounded-cut-frontier-manifest-2026-07-17.json": (
        "3475b2cf6af105b4d229e9683eb2f61433be2e4cefc8f1e8f2318c07762f3dd5"
    ),
    "cm2-gate45-sparse-cut-dwell-contraction-frontier-manifest-2026-07-17.json": (
        "8fc54ac0484bdf3b97ed0d3d4b267f208ead4d762213f595c08f44c7ed84c98a"
    ),
    "cm2-gate25-selected-component-chart-field-slots-manifest-2026-07-17.json": (
        "417464531cae76bf774bdc35f1d2f25799237d1efde39be8850cf3408740f271"
    ),
    "cm2-gate25-quotient-18field-kac-closure-frontier-manifest-2026-07-17.json": (
        "7e54075f64a44a19dbf12599314d0ad7044d4463cfe90cc81c6499c5a3af793b"
    ),
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json": (
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866"
    ),
    "cm2-gate5-physical-prefix-kac-norm-frontier-manifest-2026-07-16.json": (
        "64f3820e2dc2f6d544be94bbe205fcf08f9517eef29131311e6fafa295060a93"
    ),
}

BOUND_SELECTED_FIELDS = (
    "nonempty_or_empty_domain_proof",
    "homogeneous_prefix_chart",
    "homogeneous_suffix_chart",
    "one_step_cut_growth_Z_sum",
)


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

    join = loaded[
        "cm2-gate345-occurrence-core-component-slot-join-manifest-2026-07-18.json"
    ]
    assert join["verdict"]["occurrence_core_component_slot_join_64_128_14"] == (
        "CERTIFIED"
    )
    assert join["verdict"]["common_strong_space_operator"] == "NOT_CERTIFIED"

    local = loaded[
        "cm2-gate34-local-core-return-tail-manifest-2026-07-18.json"
    ]
    assert local["verdict"]["local_first_return_current_cylinders_3"] == (
        "CERTIFIED"
    )
    assert local["verdict"]["full_24_core_induced_operator"] == "NOT_CERTIFIED"

    fixed = loaded[
        "cm2-gate4-fixed-core-green-kernel-unbounded-cut-frontier-manifest-2026-07-17.json"
    ]
    assert fixed["verdict"]["fixed_core_unbounded_transport_delay_Green_kernel"] == (
        "CERTIFIED"
    )
    assert fixed["verdict"]["transported_occurrence_to_core_incidence"] == (
        "NOT_CERTIFIED"
    )

    sparse = loaded[
        "cm2-gate45-sparse-cut-dwell-contraction-frontier-manifest-2026-07-17.json"
    ]
    assert sparse["verdict"]["core_2018_step_upper_3_over_8"] == "CERTIFIED"
    assert sparse["verdict"]["native_physical_no_hidden_cut_dwell_schedule"] == (
        "NOT_CERTIFIED"
    )

    selected = loaded[
        "cm2-gate25-selected-component-chart-field-slots-manifest-2026-07-17.json"
    ]
    maturity = selected["result"]["Gate5_maturity_update"]
    assert maturity["completed_field_count_on_each_selected_component_level"] == 4
    assert maturity["field_5_6_completed_roof_level_slot_count"] == 0

    quotient = loaded[
        "cm2-gate25-quotient-18field-kac-closure-frontier-manifest-2026-07-17.json"
    ]
    assert quotient["verdict"]["Gate5_complete_physical_operator_blocks"] == 0

    norm = loaded[
        "cm2-gate5-physical-prefix-kac-norm-frontier-manifest-2026-07-16.json"
    ]
    assert norm["verdict"]["one_collision_three_norm_seeds"] == "CERTIFIED"
    assert norm["verdict"]["physical_three_CM2_norm_lifts"] == "NOT_CERTIFIED"
    return loaded


def matmul(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    assert len(left) == 2 and len(right) == 2
    assert all(len(row) == 2 for row in left + right)
    return [
        [sum(left[i][k] * right[k][j] for k in range(2)) for j in range(2)]
        for i in range(2)
    ]


def l1_operator_norm(matrix: list[list[int]]) -> int:
    return max(sum(abs(matrix[i][j]) for i in range(2)) for j in range(2))


def exact_operator_signature_countermodel() -> dict[str, Any]:
    # Column vectors in the ordered basis (delta_core, delta_exterior).
    m_core = [[1, 0], [0, 0]]
    m_exterior = [[0, 0], [0, 1]]
    transfer = [[0, 1], [1, 0]]
    open_operator = matmul(transfer, m_core)
    open_square = matmul(open_operator, open_operator)
    induced_return_two = matmul(
        m_core,
        matmul(
            transfer,
            matmul(m_exterior, matmul(transfer, m_core)),
        ),
    )

    assert open_operator == [[0, 0], [1, 0]]
    assert open_square == [[0, 0], [0, 0]]
    assert induced_return_two == m_core
    assert l1_operator_norm(open_square) == 0
    assert l1_operator_norm(induced_return_two) == 1

    b_core = Q(720269600000, 720626832337)
    assert 0 < b_core < 1
    assert Q(l1_operator_norm(open_square)) <= b_core**2
    assert Q(l1_operator_norm(induced_return_two)) > b_core**2

    payload = {
        "basis": ["delta_core", "delta_exterior"],
        "M_core": m_core,
        "M_complement": m_exterior,
        "L_swap": transfer,
        "O_equals_L_M_core": open_operator,
        "O_squared": open_square,
        "R_2_equals_M_core_L_M_complement_L_M_core": induced_return_two,
    }
    return {
        **payload,
        "l1_operator_norm_O_squared": 0,
        "l1_operator_norm_R_2": 1,
        "frozen_b_core": str(b_core),
        "O_squared_norm_le_b_core_squared": True,
        "R_2_norm_gt_b_core_squared": True,
        "formal_implication_open_power_bound_to_induced_return_bound": False,
        "countermodel_scope": (
            "logical operator-signature countermodel only; not a CM2 dynamics counterexample"
        ),
        "matrix_payload_sha256": canonical_digest(payload),
    }


def round23_join_and_field_boundary(
    loaded: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    join = loaded[
        "cm2-gate345-occurrence-core-component-slot-join-manifest-2026-07-18.json"
    ]["result"]
    registry = join["occurrence_core_component_slot_join_registry"]
    axes = registry["independent_axis_typing_guard"]
    selected = loaded[
        "cm2-gate25-selected-component-chart-field-slots-manifest-2026-07-17.json"
    ]["result"]
    quotient = loaded[
        "cm2-gate25-quotient-18field-kac-closure-frontier-manifest-2026-07-17.json"
    ]["result"]
    required = loaded[
        "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
    ]["result"]["required_operator_field_schema"]["required_fields"]

    assert len(required) == 18
    assert tuple(field for field in required if field in BOUND_SELECTED_FIELDS) == (
        BOUND_SELECTED_FIELDS
    )
    missing = [field for field in required if field not in BOUND_SELECTED_FIELDS]
    assert len(missing) == 14
    assert missing[0] == "physical_homogeneity_subbranch_table"
    assert missing[1:3] == ["inverse_Jacobian_bound", "log_Jacobian_distortion_sum"]

    seed_registry = selected["selected_component_field5_field6_seed_registry"]
    maturity = selected["Gate5_maturity_update"]
    assert seed_registry["selected_component_packet_count"] == 24
    assert seed_registry["completed_roof_level_field_count"] == 0
    assert maturity["completed_fields_on_each_of_28_selected_component_levels"] == (
        list(BOUND_SELECTED_FIELDS)
    )
    assert quotient["Gate5_18_field_maturity"]["core_local_seed_field_count"] == 2
    assert quotient["Gate5_18_field_maturity"][
        "complete_physical_homogeneous_slot_field_count"
    ] == 0

    assert registry["maximal_occurrence_owner_count"] == 64
    assert registry["parameter_branch_count"] == 128
    assert registry["distinct_destination_core_count"] == 14
    assert registry["distinct_selected_maximal_component_count"] == 14
    assert registry["bound_existing_field_count_per_destination_component"] == 4
    assert axes["recovery_orientation_axis"]["common_restriction_id_join"] == (
        "NOT_CERTIFIED"
    )
    assert axes["singular_kac_coordinate_axis"][
        "complete_four_term_physical_Kac_typing"
    ] == "NOT_CERTIFIED"

    rows = [
        {
            "index": index,
            "field": field,
            "selected_destination_status": (
                "BOUND_EXISTING_SELECTED_LEVEL"
                if field in BOUND_SELECTED_FIELDS
                else (
                    "COMPONENT_LOCAL_SEED_NOT_COMPLETED_SLOT"
                    if field in {
                        "inverse_Jacobian_bound",
                        "log_Jacobian_distortion_sum",
                    }
                    else "MISSING_COMPLETED_SELECTED_LEVEL_SLOT"
                )
            ),
        }
        for index, field in enumerate(required, start=1)
    ]
    return {
        "occurrence_owner_count": 64,
        "parameter_side_branch_count": 128,
        "destination_core_count": 14,
        "selected_roof_one_component_count": 14,
        "entrance_incidence_join": "CERTIFIED",
        "bound_completed_selected_level_fields": list(BOUND_SELECTED_FIELDS),
        "bound_completed_selected_level_field_count": 4,
        "missing_completed_selected_level_fields": missing,
        "missing_completed_selected_level_field_count": 14,
        "field5_field6_component_local_seed_packet_count": 24,
        "field5_field6_completed_roof_level_slot_count": 0,
        "field5_field6_seed_to_slot_promotion": "NOT_CERTIFIED",
        "complete_18_field_operator_block_count": 0,
        "common_fw_rev_restriction_id": "NOT_CERTIFIED",
        "complete_four_term_physical_Kac_typing": "NOT_CERTIFIED",
        "field_status_rows_sha256": canonical_digest(rows),
        "operator_binding_rows_sha256": registry["operator_binding_rows_sha256"],
        "occurrence_to_core_sha256": registry["occurrence_to_core_sha256"],
    }


def open_vs_induced_semantic_audit(
    loaded: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    fixed = loaded[
        "cm2-gate4-fixed-core-green-kernel-unbounded-cut-frontier-manifest-2026-07-17.json"
    ]["result"]["fixed_core_green_kernel"]
    sparse = loaded[
        "cm2-gate45-sparse-cut-dwell-contraction-frontier-manifest-2026-07-17.json"
    ]["result"]
    local = loaded[
        "cm2-gate34-local-core-return-tail-manifest-2026-07-18.json"
    ]["result"]["local_core_return_tail_registry"]

    assert fixed["fixed_open_operator"] == "O=T_* o M_core on the 24-core union"
    assert fixed["b_core"] == "720269600000/720626832337"
    assert sparse["core_block_sharpening"]["exact_statement"] == (
        "b_core^2018<3/8<1/2"
    )
    assert local["first_return_time_multiset"] == [545, 649, 1531, ">2018"]
    assert local["all_8072_states_strictly_classified_against_all_24_cores"] is True

    # Every frozen local box is outside C at post-core time one because every
    # first positive return is later than one and the replay is fail-closed.
    first_times = local["first_return_time_multiset"]
    assert all(item == ">2018" or item > 1 for item in first_times)

    return {
        "frozen_open_operator": "O=L M_C",
        "frozen_open_Growth_coefficient": fixed["b_core"],
        "frozen_open_2018_power_upper": "3/8",
        "target_first_return_operator": "R_n=M_C L (M_complement L)^(n-1) M_C",
        "target_survivor_operator": "Q_n=(M_complement L)^n M_C",
        "open_operator_has_intermediate_complement_guards": False,
        "first_return_operator_requires_intermediate_complement_guards": True,
        "open_operator_has_terminal_core_projection": False,
        "first_return_operator_requires_terminal_core_projection": True,
        "operator_signatures_identical": False,
        "four_local_boxes_first_positive_return_times": first_times,
        "four_local_boxes_strictly_outside_core_at_post_core_time_one": True,
        "repeated_open_power_tracks_these_excursions_until_return": False,
        "local_return_current_cylinders_form_full_source_partition": False,
        "native_no_hidden_recut_dwell_schedule": sparse[
            "physical_installation_frontier"
        ]["native_no_hidden_cut_dwell_schedule"],
        "strong_complement_cemetery_payload": sparse[
            "physical_installation_frontier"
        ]["strong_complement_cemetery_payload"],
        "b_core_reusable_as_induced_Lasota_Yorke_coefficient": False,
    }


def missing_induced_strong_interface() -> dict[str, Any]:
    fields = [
        {
            "field": "complete_collision_SRB_source_partition",
            "required_for": "all_source_mass",
            "current_status": "NOT_CERTIFIED",
        },
        {
            "field": "raw_first_return_branch_records",
            "required_for": "R_n_and_Q_n_materialization",
            "current_status": "NOT_CERTIFIED",
        },
        {
            "field": "all_preterminal_complement_guards",
            "required_for": "first_return_disjointness",
            "current_status": "NOT_CERTIFIED_GLOBALLY",
        },
        {
            "field": "homogeneity_and_hidden_recut_margins",
            "required_for": "common_refinement_atom",
            "current_status": "NOT_CERTIFIED",
        },
        {
            "field": "branch_source_mass_m_n",
            "required_for": "mass_conservation",
            "current_status": "NOT_CERTIFIED",
        },
        {
            "field": "unstable_Jacobian_and_inverse",
            "required_for": "regular_density_intertwiner",
            "current_status": "LOCAL_SEED_ONLY",
        },
        {
            "field": "log_Jacobian_distortion_sum",
            "required_for": "strong_Lasota_Yorke_bound",
            "current_status": "LOCAL_SEED_ONLY",
        },
        {
            "field": "regular_standard_flux_dynamic_operator_costs",
            "required_for": "three_CM2_norm_lifts",
            "current_status": "NOT_CERTIFIED",
        },
        {
            "field": "common_fw_rev_restriction_id_and_carriers",
            "required_for": "same_occurrence_recovery_charge",
            "current_status": "NOT_CERTIFIED",
        },
        {
            "field": "physical_four_term_Kac_typing",
            "required_for": "Kac_output_in_common_spaces",
            "current_status": "NOT_CERTIFIED",
        },
        {
            "field": "singular_cemetery_and_survivor_outer_mass",
            "required_for": "source_mass_identity",
            "current_status": "NOT_CERTIFIED_GLOBALLY",
        },
        {
            "field": "weighted_q_excursion_tail",
            "required_for": "summable_induced_strong_forcing",
            "current_status": "NOT_CERTIFIED",
        },
        {
            "field": "induced_common_space_contraction_coefficient",
            "required_for": "Gate4_Gate5_operator_closure",
            "current_status": "NOT_CERTIFIED",
        },
    ]
    assert len(fields) == 13
    assert all(row["current_status"] != "CERTIFIED" for row in fields)
    return {
        "required_record_count": len(fields),
        "certified_complete_record_count": 0,
        "records": fields,
        "records_sha256": canonical_digest(fields),
        "mass_identity_target": (
            "source_mass=sum_first_return_mass+singular_cemetery_mass+survivor_mass"
        ),
        "weighted_tail_target": "sum_{tau>n}q_tau<=C*rho^n",
        "coefficient_compatibility_target": "rho*exp(A_loss)<1",
        "shortest_next_certificate": (
            "materialize R_n/Q_n raw branch rows with guards, Jacobians, m_n, q_n, "
            "three-norm costs, common restriction IDs, and cemetery/survivor payloads"
        ),
    }


def build_result() -> dict[str, Any]:
    loaded = load_dependencies()
    result: dict[str, Any] = {
        "schema": "cm2.gate45.induced-strong-coefficient-obstruction.v1",
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "audit_policy": "exact_manifest_join_plus_finite_state_countermodel",
        },
        "round23_join_and_field_boundary": round23_join_and_field_boundary(loaded),
        "open_vs_induced_semantic_audit": open_vs_induced_semantic_audit(loaded),
        "exact_operator_signature_countermodel": (
            exact_operator_signature_countermodel()
        ),
        "missing_induced_strong_interface": missing_induced_strong_interface(),
        "strict_nonpromotion": {
            "entrance_incidence_join_implies_common_recovery_carrier": False,
            "component_local_field5_field6_seeds_imply_completed_slots": False,
            "open_operator_power_bound_implies_first_return_operator_bound": False,
            "four_local_return_boxes_imply_full_collision_SRB_partition": False,
            "Borel_TV_Linf_constants_imply_three_CM2_norm_intertwiners": False,
            "b_core_is_induced_Lasota_Yorke_coefficient": False,
            "complete_18_field_operator_blocks": 0,
            "induced_strong_coefficient": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
        },
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def main() -> None:
    print(json.dumps(build_result(), indent=2, sort_keys=True))
    print("ROUND23_ENTRANCE_INCIDENCE_JOIN_64_128_14: CERTIFIED")
    print("SELECTED_COMPONENT_FIELD_MATURITY: 4/18")
    print("OPEN_TO_INDUCED_COEFFICIENT_NONIMPLICATION: CERTIFIED")
    print("INDUCED_STRONG_COEFFICIENT: NOT_CERTIFIED")
    print("GATE4_GATE5: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
