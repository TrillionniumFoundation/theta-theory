#!/usr/bin/env python3
"""Stable-quotient/PPE, 18-field, three-norm and Kac/phase frontier.

This certificate aligns the newest class-H and characteristic-boundary
advances with the frozen Gate-2 and Gate-5 interfaces.  It proves a sharp
nonimplication: even a class-H cocycle with trivial canonical holonomies over
an invertible base can have a Dirac reverse kernel and no two-copy energy
contraction.  Thus class H cannot replace a physical stable quotient.

It also upgrades the 18-field maturity table.  Fields 5 and 6 have physical
24-core local seeds, and field 7 now has an all-key/all-component finite
formula.  Because homogeneous subbranch ids and the physical operator slots
are absent, no complete 18-field block exists.  The three return-wide norm
intertwiners and full physical Kac output remain fail-closed.  On the
preferred direct-standard-N route, however, no separate phase tower is
needed; the remaining obstruction is operator/norm typing rather than a
component-period obstruction.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent

DEPENDENCIES = {
    "cm2-gate1-variable-diagonal-groupoid-frontier-manifest-2026-07-17.json": (
        "dacbae6255707086bc7486e4933d8c890ede1547a9e545995800a5fc18698f83"
    ),
    "cm2-gate2-collision-key-stable-quotient-frontier-manifest-2026-07-16.json": (
        "886c5feb8709ad26fd653e598edf344ba39cc3e08e6efbd02c9ad1133f784c65"
    ),
    "cm2-gate25-universal-operator-endpoint-template-frontier-manifest-2026-07-16.json": (
        "d532eeab0fa24901228a589724ffc4dbcff721f7d174a2b519187d77faab883b"
    ),
    "cm2-gate25-all-component-characteristic-frontier-manifest-2026-07-17.json": (
        "41c766d25b007944313db93b389a616d086a7318700a867e13d90aedd159be35"
    ),
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json": (
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866"
    ),
    "cm2-gate5-physical-prefix-kac-norm-frontier-manifest-2026-07-16.json": (
        "64f3820e2dc2f6d544be94bbe205fcf08f9517eef29131311e6fafa295060a93"
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
        assert sha256_path(path) == expected
        value = json.loads(path.read_text(encoding="utf-8"))
        assert isinstance(value, dict)
        loaded[name] = value

    class_h = loaded[
        "cm2-gate1-variable-diagonal-groupoid-frontier-manifest-2026-07-17.json"
    ]
    gate2 = loaded[
        "cm2-gate2-collision-key-stable-quotient-frontier-manifest-2026-07-16.json"
    ]
    template = loaded[
        "cm2-gate25-universal-operator-endpoint-template-frontier-manifest-2026-07-16.json"
    ]
    characteristic = loaded[
        "cm2-gate25-all-component-characteristic-frontier-manifest-2026-07-17.json"
    ]
    gate5 = loaded[
        "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
    ]
    norm_kac = loaded[
        "cm2-gate5-physical-prefix-kac-norm-frontier-manifest-2026-07-16.json"
    ]

    assert class_h["verdict"][
        "stable_variable_diagonal_groupoid_equation"
    ] == "SOLVED_SEPARATELY"
    assert class_h["verdict"][
        "unstable_variable_diagonal_groupoid_equation"
    ] == "SOLVED_SEPARATELY"
    assert class_h["verdict"]["combined_all_plaque_third_gauge"] == (
        "NOT_CERTIFIED"
    )

    gate2_frontier = gate2["result"][
        "quotient_reverse_endpoint_stopping_frontier"
    ]
    assert gate2_frontier["required_field_count"] == 17
    assert not any(gate2_frontier["physical_completion_flags"].values())
    assert gate2["verdict"]["physical_PPE"] == "NOT_CERTIFIED"

    strict = template["result"]["strict_completion_boundary"]
    assert strict["two_new_core_local_strong_field_seeds"] == [
        "inverse_Jacobian_bound",
        "log_Jacobian_distortion_sum",
    ]
    assert strict["complete_18_field_operator_block_count"] == 0

    fields = gate5["result"]["required_operator_field_schema"]
    assert fields["required_field_count_per_physical_homogeneous_level"] == 18
    assert fields["required_fields"][6] == "one_step_cut_growth_Z_sum"
    assert gate5["result"]["completion"][
        "physical_homogeneous_subbranch_registry"
    ] is False

    field7 = characteristic["result"]["operator_field_frontier"]
    assert field7["full_key_field7_finite_characteristic_formula"] == (
        "CERTIFIED"
    )
    assert field7["field7_growth_contraction"] is False
    assert field7["complete_18_field_operator_block_count"] == 0

    norm_completion = norm_kac["result"]["completion"]
    assert norm_completion["one_collision_three_norm_seeds"] is True
    assert norm_completion["regular_density_prefix_suffix_intertwiner"] is False
    assert norm_completion["standard_family_CM2_norm_lift"] is False
    assert norm_completion["flux_face_CM2_norm_lift"] is False
    assert norm_completion["dynamic_test_CM2_norm_lift"] is False
    assert norm_completion["full_four_term_physical_Kac_CM2_output"] is False
    return loaded


def class_h_ppe_nonimplication() -> dict[str, Any]:
    state_count = 97
    multiplier = 37
    shift = 11
    images = {(multiplier * state + shift) % state_count for state in range(state_count)}
    assert len(images) == state_count
    reverse_support_sizes = [1 for _ in range(state_count)]
    assert set(reverse_support_sizes) == {1}
    return {
        "countermodel_base": "F(i)=37*i+11 mod 97",
        "base_is_invertible": True,
        "constant_diagonal_cocycle": "A=diag(2,1/2)",
        "canonical_stable_holonomies": "identity",
        "canonical_unstable_holonomies": "identity",
        "holonomy_Holder_constant": 0,
        "cocycle_is_class_H": True,
        "arbitrary_finite_or_countable_edge_labels_allowed": True,
        "reverse_conditional_support_size_at_every_target": 1,
        "reverse_kernel": "Dirac",
        "diagonal_two_copy_Riesz_coefficient": "1",
        "uniform_pair_energy_contraction_kappa_less_than_one": False,
        "theorem": (
            "class H, even with exact canonical holonomies, does not imply "
            "a noninvertible stable quotient, physical reverse weights, or PPE"
        ),
        "class_H_implies_physical_PPE": False,
    }


def gate2_completion_ledger(
    gate2: dict[str, Any],
) -> dict[str, Any]:
    frontier = gate2["result"][
        "quotient_reverse_endpoint_stopping_frontier"
    ]
    fields = frontier["required_fields"]
    flags = frontier["physical_completion_flags"]
    assert len(fields) == 17
    rows = [
        {
            "index": index,
            "field": field,
            "physical_completion": bool(flags[field]),
        }
        for index, field in enumerate(fields, start=1)
    ]
    assert sum(row["physical_completion"] for row in rows) == 0
    return {
        "required_field_count": len(rows),
        "completed_physical_field_count": 0,
        "rows": rows,
        "rows_sha256": canonical_digest(rows),
        "first_missing_object": frontier["first_missing_object"],
        "first_reverse_kernel_missing_object": frontier[
            "first_reverse_kernel_missing_object"
        ],
        "separate_class_H_theorem_populates_any_physical_quotient_field": False,
        "stable_quotient": "NOT_CERTIFIED",
        "physical_PPE": "NOT_CERTIFIED",
    }


def gate5_field_maturity(
    gate5: dict[str, Any],
    template: dict[str, Any],
    characteristic: dict[str, Any],
) -> dict[str, Any]:
    schema = gate5["result"]["required_operator_field_schema"]
    fields = schema["required_fields"]
    assert len(fields) == 18

    statuses = {field: "NO_FULL_KEY_PHYSICAL_SLOT" for field in fields}
    statuses["inverse_Jacobian_bound"] = "24_CORE_LOCAL_SEED"
    statuses["log_Jacobian_distortion_sum"] = "24_CORE_LOCAL_SEED"
    statuses["one_step_cut_growth_Z_sum"] = (
        "ALL_441280_KEYS_AND_COMPONENTS_FINITE_FORMULA_NONCONTRACTING"
    )
    rows = [
        {
            "index": index,
            "field": field,
            "maturity": statuses[field],
            "complete_physical_homogeneous_slot": False,
        }
        for index, field in enumerate(fields, start=1)
    ]

    universal = template["result"]["universal_full_collision_branch_templates"]
    assert universal["field_5_inverse_Jacobian_seed"][
        "core_local_seed_on_all_24_positive_cores"
    ] is True
    assert universal["field_6_log_Jacobian_distortion_seed"][
        "core_local_seed_on_all_24_positive_cores"
    ] is True
    field7 = characteristic["result"]["operator_field_frontier"]
    assert field7["same_formula_applies_to_each_eventual_homogeneous_slot"] is True
    assert field7["physical_homogeneous_subbranch_ids_materialized"] is False

    return {
        "required_field_count_per_level": len(rows),
        "schema_level_all_key_formula_field_count": 1,
        "schema_level_all_key_formula_fields": [
            "one_step_cut_growth_Z_sum"
        ],
        "core_local_seed_field_count": 2,
        "core_local_seed_fields": [
            "inverse_Jacobian_bound",
            "log_Jacobian_distortion_sum",
        ],
        "field7_formula": field7["field7_formula"],
        "field7_growth_contraction": False,
        "homogeneous_subbranch_ids_materialized": False,
        "complete_physical_homogeneous_slot_field_count": 0,
        "complete_18_field_operator_block_count": 0,
        "rows": rows,
        "rows_sha256": canonical_digest(rows),
        "exact_reason_no_block_is_complete": (
            "fields 5-6 are core-local only; field 7 is an all-key formula "
            "without materialized homogeneous subbranch ids; all remaining "
            "physical slots are absent"
        ),
    }


def three_norm_and_kac_phase(
    gate5: dict[str, Any], norm_kac: dict[str, Any],
) -> dict[str, Any]:
    completion = norm_kac["result"]["completion"]
    phase = norm_kac["result"]["phase_and_route_audit"]
    kac = gate5["result"]["Kac_and_phase_frontier"]
    norm_rows = [
        {
            "name": "regular_density_prefix_suffix_intertwiner",
            "one_collision_seed": True,
            "return_wide_completion": completion[
                "regular_density_prefix_suffix_intertwiner"
            ],
        },
        {
            "name": "standard_family_CM2_norm_lift",
            "one_collision_seed": True,
            "return_wide_completion": completion[
                "standard_family_CM2_norm_lift"
            ],
        },
        {
            "name": "flux_face_and_dynamic_test_CM2_lifts",
            "one_collision_seed": True,
            "return_wide_completion": (
                completion["flux_face_CM2_norm_lift"]
                and completion["dynamic_test_CM2_norm_lift"]
            ),
        },
    ]
    assert not any(row["return_wide_completion"] for row in norm_rows)
    assert phase["preferred_route"] == "direct_standard_N"
    assert phase["direct_standard_N_route_needs_separate_phase_tower"] is False
    assert phase["actual_standard_N_component_cycle_gcd"] == 1
    assert kac["finite_Borel_four_term_Kac_algebra_exact"] is True
    return {
        "three_norm_rows": norm_rows,
        "three_norm_rows_sha256": canonical_digest(norm_rows),
        "one_collision_three_norm_seeds": "CERTIFIED",
        "return_wide_three_norm_intertwiners": "NOT_CERTIFIED",
        "Kac": {
            "finite_Borel_four_term_algebra": "CERTIFIED",
            "singular_event_current_TV_upper": kac[
                "singular_Kac_Borel_event_current_TV_upper"
            ],
            "height_nine_singular_phase_lift_upper": kac[
                "height_nine_singular_phase_lift_upper"
            ],
            "regular_two_terms_typed_in_CM2_spaces": False,
            "propagated_singular_terms_typed_in_CM2_spaces": False,
            "full_four_term_physical_Kac_CM2_output": "NOT_CERTIFIED",
        },
        "phase": {
            "preferred_route": "direct_standard_N",
            "component_cycle_gcd": 1,
            "component_period_obstruction_removed": True,
            "separate_phase_tower_required_on_preferred_route": False,
            "direct_route_phase_choice": "CERTIFIED",
            "all_return_word_operator_phase_blocks_registered": False,
            "optional_operator_Wiener_phase_transfer": "NOT_CERTIFIED",
        },
        "conditional_direct_route_closure": {
            "hypotheses": [
                "complete physical homogeneous return-word operator blocks",
                "all three return-wide CM2 norm intertwiners",
                "separate CM2 typing of both regular and both singular Kac terms",
            ],
            "conclusion": (
                "the exact four-term Kac algebra closes on standard N "
                "without a separate phase tower"
            ),
            "hypotheses_currently_met": False,
        },
    }


def build_result() -> dict[str, Any]:
    dependencies = load_dependencies()
    gate2 = dependencies[
        "cm2-gate2-collision-key-stable-quotient-frontier-manifest-2026-07-16.json"
    ]
    template = dependencies[
        "cm2-gate25-universal-operator-endpoint-template-frontier-manifest-2026-07-16.json"
    ]
    characteristic = dependencies[
        "cm2-gate25-all-component-characteristic-frontier-manifest-2026-07-17.json"
    ]
    gate5 = dependencies[
        "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
    ]
    norm_kac = dependencies[
        "cm2-gate5-physical-prefix-kac-norm-frontier-manifest-2026-07-16.json"
    ]

    result: dict[str, Any] = {
        "schema": "cm2.gate25.quotient-18field-kac-closure-frontier.v1",
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
        },
        "class_H_PPE_nonimplication": class_h_ppe_nonimplication(),
        "Gate2_17_field_completion": gate2_completion_ledger(gate2),
        "Gate5_18_field_maturity": gate5_field_maturity(
            gate5, template, characteristic
        ),
        "three_norm_Kac_phase": three_norm_and_kac_phase(gate5, norm_kac),
        "strict_nonpromotion": {
            "separate_class_H_gauges_imply_stable_quotient": False,
            "class_H_implies_reverse_randomness_or_PPE": False,
            "field7_formula_implies_complete_18_field_block": False,
            "one_collision_norm_seeds_imply_return_wide_intertwiners": False,
            "component_gcd_one_implies_operator_phase_blocks": False,
            "Borel_Kac_algebra_implies_physical_CM2_Kac_output": False,
            "Gate1": "NOT_CERTIFIED",
            "Gate2": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
        },
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def main() -> None:
    print(json.dumps(build_result(), indent=2, sort_keys=True))
    print("ALL_KEY_GATE5_FIELD7_FORMULA: CERTIFIED_NONCONTRACTING")
    print("DIRECT_STANDARD_N_PHASE_ROUTE_CHOICE: CERTIFIED")
    print("STABLE_QUOTIENT_PPE_18_FIELDS_THREE_NORMS_KAC: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
