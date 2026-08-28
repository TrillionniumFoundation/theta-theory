#!/usr/bin/env python3
"""Bind field 7 to the 24 selected physical maximal components.

The all-key characteristic theorem supplies a finite field-7 formula for
every maximal component but previously had no materialized homogeneous slot
IDs.  The frozen seeded registry contains 24 positive maximal components,
each with a fixed word key and central source/target homogeneity predicate.
This certificate materializes one selected component-row ID per component
and all 28 roof-level field-7 slots.  It also attaches the new scheduled
12108-step dwell contraction as a conditional packet.  The complete
homogeneity table, the other 16 fields, and physical dwell installation are
not inferred.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent

DEPENDENCIES = {
    "cm2-gate25-maximal-word-characteristic-frontier-manifest-2026-07-16.json": (
        "bb09f99519813ec49172f0bbbcc9015c1e0fcb2de07df7af734b81d2996a3f40"
    ),
    "cm2-gate25-all-component-characteristic-frontier-manifest-2026-07-17.json": (
        "41c766d25b007944313db93b389a616d086a7318700a867e13d90aedd159be35"
    ),
    "cm2-gate25-selected-homoclinic-component-incidence-frontier-manifest-2026-07-16.json": (
        "83120fd29f2820c943451d66a867e3ea79400b1fd9f4efda8bc15eac0aee0828"
    ),
    "cm2-gate45-sparse-cut-dwell-contraction-frontier-manifest-2026-07-17.json": (
        "8fc54ac0484bdf3b97ed0d3d4b267f208ead4d762213f595c08f44c7ed84c98a"
    ),
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json": (
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866"
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

    maximal = loaded[
        "cm2-gate25-maximal-word-characteristic-frontier-manifest-2026-07-16.json"
    ]
    characteristic = loaded[
        "cm2-gate25-all-component-characteristic-frontier-manifest-2026-07-17.json"
    ]
    selected = loaded[
        "cm2-gate25-selected-homoclinic-component-incidence-frontier-manifest-2026-07-16.json"
    ]
    sparse = loaded[
        "cm2-gate45-sparse-cut-dwell-contraction-frontier-manifest-2026-07-17.json"
    ]
    gate5 = loaded[
        "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
    ]

    registry = maximal["result"]["seeded_implicit_maximal_component_registry"]
    assert registry["seeded_maximal_component_count"] == 24
    assert len(registry["rows"]) == 24
    assert maximal["verdict"]["positive_seeded_maximal_word_components"] == (
        "CERTIFIED_IMPLICIT"
    )

    all_components = characteristic["result"][
        "all_key_all_component_characteristic_registry"
    ]
    assert all_components["candidate_key_count_covered"] == 441280
    assert all_components[
        "each_maximal_component_characteristic_boundary_Z"
    ] == "CERTIFIED"
    assert characteristic["result"]["operator_field_frontier"][
        "full_key_field7_finite_characteristic_formula"
    ] == "CERTIFIED"

    incidence = selected["result"]["selected_occurrence_component_incidence"]
    assert incidence[
        "selected_occurrence_membership_in_one_of_24_maximal_word_components_certified"
    ] is True

    raw = sparse["result"]["raw_field7_scheduled_contraction"]
    assert raw["dwell_steps"] == 12108
    assert raw["scheduled_raw_field7_arbitrary_cut_count_contraction"] == (
        "CERTIFIED_ABSTRACTLY"
    )
    assert sparse["verdict"][
        "native_physical_no_hidden_cut_dwell_schedule"
    ] == "NOT_CERTIFIED"

    schema = gate5["result"]["required_operator_field_schema"]
    assert schema["required_field_count_per_physical_homogeneous_level"] == 18
    assert schema["required_fields"][0] == "nonempty_or_empty_domain_proof"
    assert schema["required_fields"][6] == "one_step_cut_growth_Z_sum"
    return loaded


def selected_component_slot_registry(
    maximal: dict[str, Any], characteristic: dict[str, Any]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    rows = maximal["result"]["seeded_implicit_maximal_component_registry"][
        "rows"
    ]
    source_constants = {
        row["source_obstacle"]: row[
            "all_component_unnormalized_characteristic_Z_multiplier_upper"
        ]
        for row in characteristic["result"][
            "all_key_all_component_characteristic_registry"
        ]["source_class_rows"]
    }
    assert source_constants == {"G": "580000/1999", "W": "572000/1999"}

    component_rows: list[dict[str, Any]] = []
    level_slots: list[dict[str, Any]] = []
    source_histogram: Counter[str] = Counter()
    roof_histogram: Counter[int] = Counter()
    key_ids: set[str] = set()
    component_ids: set[str] = set()

    for row in rows:
        definition = row["definition"]
        physical_key = definition["physical_key"]
        component_id = row["maximal_component_id"]
        assert component_id == canonical_digest(definition)
        assert row["component_nonempty_for_every_parameter_fibre"] is True
        assert row["seed_is_uniformly_physical_and_strict_first_hit"] is True
        assert row["seed_is_central_at_source_and_target"] is True

        source_chart, _target, wall_record, roof = physical_key
        source = source_chart.split(":")[0]
        assert roof == len(wall_record) + 1
        selected_h_payload = {
            "word_key": physical_key,
            "maximal_component_id": component_id,
            "source_homogeneity": "abs(p_source)<3/10",
            "target_homogeneity": "abs(p_target)<3/10",
            "component_predicate": definition["component_predicate"],
        }
        selected_h_id = "h:" + canonical_digest(selected_h_payload)
        key_id = canonical_digest(physical_key)
        assert key_id not in key_ids
        assert component_id not in component_ids
        key_ids.add(key_id)
        component_ids.add(component_id)
        source_histogram[source] += 1
        roof_histogram[roof] += 1

        component_rows.append({
            "word_key_id": key_id,
            "physical_key": physical_key,
            "maximal_component_id": component_id,
            "selected_homogeneous_component_row_id": selected_h_id,
            "source_obstacle": source,
            "roof": roof,
            "parameter_fibre_nonempty": "every |s|<=1/400",
            "source_and_target_central_homogeneity": True,
            "field_1_nonempty_or_empty_domain_proof": "NONEMPTY",
            "field_7_one_step_cut_growth_Z_sum_upper": source_constants[source],
            "selected_row_is_complete_key_homogeneity_table": False,
        })

        for level in range(roof):
            slot_payload = {
                "word_key": physical_key,
                "homogeneous_subbranch_id": selected_h_id,
                "roof_level_j": level,
                "field_name": "one_step_cut_growth_Z_sum",
            }
            level_slots.append({
                **slot_payload,
                "immutable_slot_id": "slot:" + canonical_digest(slot_payload),
                "maximal_component_id": component_id,
                "physical_field_7_status": "FINITE_FORMULA_CERTIFIED",
                "field_7_multiplier_upper": source_constants[source],
                "field_7_growth_contraction_without_dwell": False,
            })

    component_rows.sort(key=canonical_json)
    level_slots.sort(key=canonical_json)
    assert source_histogram == Counter({"G": 12, "W": 12})
    assert roof_histogram == Counter({1: 20, 2: 4})
    assert len(component_rows) == 24
    assert len(level_slots) == 28
    assert len({row["immutable_slot_id"] for row in level_slots}) == 28
    return component_rows, level_slots, {
        "selected_physical_word_key_count": 24,
        "selected_positive_maximal_component_count": 24,
        "selected_homogeneous_component_row_id_count": 24,
        "source_histogram": dict(sorted(source_histogram.items())),
        "roof_histogram": {
            str(key): value for key, value in sorted(roof_histogram.items())
        },
        "materialized_field7_roof_slot_count": 28,
        "component_rows_sha256": canonical_digest(component_rows),
        "field7_level_slots_sha256": canonical_digest(level_slots),
        "complete_all_key_homogeneity_table": False,
    }


def selected_homoclinic_binding(
    selected: dict[str, Any],
    component_rows: list[dict[str, Any]],
    level_slots: list[dict[str, Any]],
) -> dict[str, Any]:
    incidence = selected["result"]["selected_occurrence_component_incidence"]
    component_id = incidence["maximal_component_id"]
    components = [
        row for row in component_rows
        if row["maximal_component_id"] == component_id
    ]
    slots = [
        row for row in level_slots
        if row["maximal_component_id"] == component_id
    ]
    assert len(components) == 1
    assert len(slots) == 1
    assert components[0]["physical_key"] == incidence["physical_key"]
    return {
        "selected_QNL_homoclinic_maximal_component_id": component_id,
        "selected_QNL_homoclinic_physical_key": incidence["physical_key"],
        "selected_QNL_homoclinic_field7_slot_id": slots[0][
            "immutable_slot_id"
        ],
        "selected_QNL_homoclinic_field7_multiplier_upper": slots[0][
            "field_7_multiplier_upper"
        ],
        "selected_QNL_homoclinic_component_field7_slot": "CERTIFIED",
        "stable_quotient_branch_label_from_component_incidence": False,
    }


def scheduled_dwell_attachment(sparse: dict[str, Any]) -> dict[str, Any]:
    raw = sparse["result"]["raw_field7_scheduled_contraction"]
    return {
        "attached_to_each_of_28_selected_field7_slots": True,
        "registered_cut_factor_upper": raw["all_key_cut_factor_upper"],
        "required_fixed_core_dwell_steps": raw["dwell_steps"],
        "cycle_coefficient_strict_upper": raw[
            "cycle_coefficient_strict_upper"
        ],
        "rational_exponential_cut_weight": raw[
            "rational_exponential_cut_weight"
        ],
        "weighted_cycle_coefficient_strict_upper": raw[
            "weighted_cycle_coefficient_strict_upper"
        ],
        "weighted_Green_resolvent_strict_upper": raw[
            "weighted_Green_resolvent_simplified_strict_upper"
        ],
        "conditional_scheduled_contraction_packet": "CERTIFIED",
        "physical_occurrence_to_core_incidence": "NOT_CERTIFIED",
        "native_no_hidden_cut_12108_step_dwell": "NOT_CERTIFIED",
        "common_strong_operator_space": "NOT_CERTIFIED",
        "physical_scheduled_contraction_on_selected_slots": "NOT_CERTIFIED",
    }


def maturity_update() -> dict[str, Any]:
    return {
        "required_field_count_per_physical_homogeneous_level": 18,
        "completed_fields_on_each_selected_component_level": [
            "nonempty_or_empty_domain_proof",
            "one_step_cut_growth_Z_sum",
        ],
        "completed_field_count_on_each_selected_component_level": 2,
        "materialized_selected_component_level_count": 28,
        "selected_component_field7_physical_slot_count": 28,
        "prior_schema_only_all_key_formula_field_count": 1,
        "complete_key_homogeneity_tables": 0,
        "complete_18_field_operator_block_count": 0,
        "first_missing_field_on_selected_components": (
            "physical_homogeneity_subbranch_table"
        ),
        "remaining_field_count_on_each_selected_component_level": 16,
        "Gate5": "NOT_CERTIFIED",
    }


def build_result() -> dict[str, Any]:
    dependencies = load_dependencies()
    maximal = dependencies[
        "cm2-gate25-maximal-word-characteristic-frontier-manifest-2026-07-16.json"
    ]
    characteristic = dependencies[
        "cm2-gate25-all-component-characteristic-frontier-manifest-2026-07-17.json"
    ]
    selected = dependencies[
        "cm2-gate25-selected-homoclinic-component-incidence-frontier-manifest-2026-07-16.json"
    ]
    sparse = dependencies[
        "cm2-gate45-sparse-cut-dwell-contraction-frontier-manifest-2026-07-17.json"
    ]
    component_rows, level_slots, registry = selected_component_slot_registry(
        maximal, characteristic
    )
    result: dict[str, Any] = {
        "schema": "cm2.gate25.selected-component-field7-slot-frontier.v1",
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
        },
        "selected_component_slot_registry": registry,
        "selected_component_rows": component_rows,
        "materialized_field7_level_slots": level_slots,
        "selected_homoclinic_field7_binding": selected_homoclinic_binding(
            selected, component_rows, level_slots
        ),
        "scheduled_dwell_attachment": scheduled_dwell_attachment(sparse),
        "Gate5_maturity_update": maturity_update(),
        "strict_nonpromotion": {
            "one_selected_h_row_implies_complete_key_homogeneity_table": False,
            "field7_formula_implies_fields_2_to_6_or_8_to_18": False,
            "conditional_dwell_packet_implies_physical_dwell_schedule": False,
            "selected_component_incidence_implies_stable_quotient_branch": False,
            "complete_18_field_operator_block_count": 0,
            "stable_quotient_PPE": "NOT_CERTIFIED",
            "three_norm_Kac_closure": "NOT_CERTIFIED",
            "Gate2": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
        },
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def main() -> None:
    print(json.dumps(build_result(), indent=2, sort_keys=True))
    print("SELECTED_PHYSICAL_MAXIMAL_COMPONENT_ROWS: 24 CERTIFIED")
    print("MATERIALIZED_SELECTED_FIELD7_ROOF_SLOTS: 28 CERTIFIED")
    print("SELECTED_COMPONENT_FIELD_MATURITY: 2/18")
    print("COMPLETE_18_FIELD_OPERATOR_BLOCKS: 0")
    print("GATE2_GATE5: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
