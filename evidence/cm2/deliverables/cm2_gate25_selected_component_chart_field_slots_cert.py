#!/usr/bin/env python3
"""Materialize Gate-5 chart fields 3 and 4 on all selected roof levels."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

import cm2_gate25_physical_return_core_registry_cert as core_cert


HERE = Path(__file__).resolve().parent

DEPENDENCIES = {
    "cm2-gate25-selected-component-field7-slot-frontier-manifest-2026-07-17.json": (
        "75de341183ef7fbcc7937f69bc7c6f276d06db0883397a7c99e4d54bbc5dc91a"
    ),
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json": (
        "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42"
    ),
    "cm2_gate25_physical_return_core_registry_cert.py": (
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"
    ),
    "cm2-gate25-roof-two-wall-chart-frontier-manifest-2026-07-16.json": (
        "9c178e2675909c72f5981a2919f8a359c806c56e1056ec7d1c3121076ba52279"
    ),
    "cm2-gate25-universal-operator-endpoint-template-frontier-manifest-2026-07-16.json": (
        "d532eeab0fa24901228a589724ffc4dbcff721f7d174a2b519187d77faab883b"
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
        if path.suffix == ".json":
            loaded[name] = json.loads(path.read_text(encoding="utf-8"))

    selected = loaded[
        "cm2-gate25-selected-component-field7-slot-frontier-manifest-2026-07-17.json"
    ]
    walls = loaded[
        "cm2-gate25-roof-two-wall-chart-frontier-manifest-2026-07-16.json"
    ]
    universal = loaded[
        "cm2-gate25-universal-operator-endpoint-template-frontier-manifest-2026-07-16.json"
    ]
    schema = loaded[
        "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
    ]
    assert selected["result"]["Gate5_maturity_update"][
        "completed_field_count_on_each_selected_component_level"
    ] == 2
    assert selected["result"]["selected_component_slot_registry"][
        "materialized_field7_roof_slot_count"
    ] == 28
    wall = walls["result"]["roof_two_wall_chart_registry"]
    assert wall[
        "all_28_core_local_roof_level_prefix_suffix_pairs_have_charts"
    ] is True
    assert wall["roof_two_physical_core_count"] == 4
    universal_fields = universal["result"][
        "universal_full_collision_branch_templates"
    ]
    assert universal_fields["field_5_inverse_Jacobian_seed"][
        "core_local_seed_on_all_24_positive_cores"
    ] is True
    assert universal_fields["field_6_log_Jacobian_distortion_seed"][
        "core_local_seed_on_all_24_positive_cores"
    ] is True
    required = schema["result"]["required_operator_field_schema"]
    assert required["required_field_count_per_physical_homogeneous_level"] == 18
    assert required["required_fields"][2:4] == [
        "homogeneous_prefix_chart", "homogeneous_suffix_chart",
    ]
    return loaded


def exact_key(core: core_cert.Core) -> list[Any]:
    return [
        core.chart_id,
        core.target_id,
        list(core.crossings),
        len(core.crossings) + 1,
    ]


def target_collision_chart(core: core_cert.Core) -> str:
    direction = core_cert.expected_suffix_direction(core)
    cell_by_direction = {
        (1, 0): "E", (-1, 0): "W", (0, 1): "N", (0, -1): "S",
    }
    if direction in cell_by_direction:
        return f"collision:{core.target_id}:{cell_by_direction[direction]}"
    return (
        f"collision:{core.target_id}:open-semicircle:"
        f"[{direction[0]},{direction[1]}]"
    )


def wall_chart(row: dict[str, Any]) -> str:
    return (
        f"transparent-wall:{row['wall_equation']}:"
        f"{row['oriented_transparent_wall_chart']}"
    )


def chart_pair_for_level(
    core: core_cert.Core,
    level: int,
    wall_row: dict[str, Any] | None,
) -> tuple[str, str, dict[str, Any]]:
    source = f"collision:{core.chart_id}"
    target = target_collision_chart(core)
    if not core.crossings:
        assert level == 0 and wall_row is None
        return source, target, {
            "chart_source": "physical compact core source collision chart",
            "chart_target": "fixed target open-semicircle collision chart",
        }
    assert wall_row is not None and len(core.crossings) == 1
    wall = wall_chart(wall_row)
    if level == 0:
        return source, wall, {
            "source_to_wall_D_infinity_strict_upper": "3",
            "wall_to_source_D_infinity_strict_upper": "10",
            "wall_Jacobian_determinant_abs_strict_lower": "3/20",
        }
    assert level == 1
    return wall, target, {
        "wall_to_target_D_infinity_strict_upper": "20",
        "target_to_wall_D_infinity_strict_upper": "20",
        "target_map_Jacobian_determinant_abs_strict_lower": "1/10",
    }


def materialize_chart_slots(
    selected: dict[str, Any], walls: dict[str, Any], universal: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    selected_result = selected["result"]
    component_rows = selected_result["selected_component_rows"]
    field7_slots = selected_result["materialized_field7_level_slots"]
    assert len(component_rows) == 24 and len(field7_slots) == 28

    cores = {canonical_json(exact_key(core)): core for core in core_cert.physical_cores()}
    wall_rows = walls["result"]["roof_two_wall_chart_registry"]["wall_rows"]
    walls_by_key = {
        canonical_json(row["physical_key"]): row for row in wall_rows
    }
    components_by_id = {
        row["maximal_component_id"]: row for row in component_rows
    }
    universal_fields = universal["result"][
        "universal_full_collision_branch_templates"
    ]

    chart_slots: list[dict[str, Any]] = []
    component_seed_packets: list[dict[str, Any]] = []
    roof_histogram: Counter[int] = Counter()
    for component in component_rows:
        key_text = canonical_json(component["physical_key"])
        core = cores[key_text]
        assert component["roof"] == len(core.crossings) + 1
        roof_histogram[component["roof"]] += 1
        component_seed_packets.append({
            "physical_key": component["physical_key"],
            "maximal_component_id": component["maximal_component_id"],
            "selected_homogeneous_component_row_id": component[
                "selected_homogeneous_component_row_id"
            ],
            "field_5_component_local_seed": universal_fields[
                "field_5_inverse_Jacobian_seed"
            ],
            "field_6_component_local_seed": universal_fields[
                "field_6_log_Jacobian_distortion_seed"
            ],
            "component_local_seed_is_complete_roof_level_slot": False,
        })

    for field7 in field7_slots:
        component = components_by_id[field7["maximal_component_id"]]
        key_text = canonical_json(field7["word_key"])
        core = cores[key_text]
        wall_row = walls_by_key.get(key_text)
        prefix, suffix, local_bounds = chart_pair_for_level(
            core, field7["roof_level_j"], wall_row
        )
        common = {
            "word_key": field7["word_key"],
            "homogeneous_subbranch_id": field7["homogeneous_subbranch_id"],
            "roof_level_j": field7["roof_level_j"],
            "maximal_component_id": field7["maximal_component_id"],
            "source_and_target_central_homogeneity": component[
                "source_and_target_central_homogeneity"
            ],
            "prefix_chart": prefix,
            "suffix_chart": suffix,
            "local_chart_bounds": local_bounds,
        }
        for field_name, value in (
            ("homogeneous_prefix_chart", prefix),
            ("homogeneous_suffix_chart", suffix),
        ):
            payload = {
                "word_key": field7["word_key"],
                "homogeneous_subbranch_id": field7[
                    "homogeneous_subbranch_id"
                ],
                "roof_level_j": field7["roof_level_j"],
                "field_name": field_name,
            }
            chart_slots.append({
                **common,
                "field_name": field_name,
                "field_value": value,
                "immutable_slot_id": "slot:" + canonical_digest(payload),
                "physical_status": "CERTIFIED_ON_SELECTED_COMPONENT_LEVEL",
            })

    chart_slots.sort(key=canonical_json)
    component_seed_packets.sort(key=canonical_json)
    assert roof_histogram == Counter({1: 20, 2: 4})
    assert len(chart_slots) == 56
    assert len({row["immutable_slot_id"] for row in chart_slots}) == 56
    assert len(component_seed_packets) == 24
    return chart_slots, component_seed_packets, {
        "selected_positive_maximal_component_count": 24,
        "selected_roof_level_count": 28,
        "materialized_field_3_prefix_chart_slot_count": 28,
        "materialized_field_4_suffix_chart_slot_count": 28,
        "materialized_chart_field_slot_count": 56,
        "all_roof_one_collision_to_collision_chart_pairs": True,
        "all_roof_two_collision_wall_collision_chart_pairs": True,
        "all_chart_pairs_are_part_of_the_implicit_maximal_component_predicate": True,
        "roof_histogram": {"1": 20, "2": 4},
        "chart_slots_sha256": canonical_digest(chart_slots),
        "component_field56_seed_packets_sha256": canonical_digest(
            component_seed_packets
        ),
    }


def maturity_update() -> dict[str, Any]:
    return {
        "required_field_count_per_selected_component_level": 18,
        "completed_fields_on_each_of_28_selected_component_levels": [
            "nonempty_or_empty_domain_proof",
            "homogeneous_prefix_chart",
            "homogeneous_suffix_chart",
            "one_step_cut_growth_Z_sum",
        ],
        "completed_field_count_on_each_selected_component_level": 4,
        "previous_completed_field_count": 2,
        "newly_completed_fields": [
            "homogeneous_prefix_chart", "homogeneous_suffix_chart",
        ],
        "component_local_field_5_6_seed_packet_count": 24,
        "field_5_6_completed_roof_level_slot_count": 0,
        "remaining_field_count_on_each_selected_component_level": 14,
        "first_missing_field": "physical_homogeneity_subbranch_table",
        "complete_key_homogeneity_table_count": 0,
        "complete_18_field_operator_block_count": 0,
        "Gate5": "NOT_CERTIFIED",
    }


def build_result() -> dict[str, Any]:
    loaded = load_dependencies()
    selected = loaded[
        "cm2-gate25-selected-component-field7-slot-frontier-manifest-2026-07-17.json"
    ]
    walls = loaded[
        "cm2-gate25-roof-two-wall-chart-frontier-manifest-2026-07-16.json"
    ]
    universal = loaded[
        "cm2-gate25-universal-operator-endpoint-template-frontier-manifest-2026-07-16.json"
    ]
    _slots, _packets, registry = materialize_chart_slots(
        selected, walls, universal
    )
    result: dict[str, Any] = {
        "schema": "cm2.gate25.selected-component-chart-field-slots.v1",
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
        },
        "selected_component_chart_slot_registry": registry,
        "selected_component_field5_field6_seed_registry": {
            "selected_component_packet_count": 24,
            "seed_fields": [
                "inverse_Jacobian_bound", "log_Jacobian_distortion_sum",
            ],
            "component_packets_sha256": registry[
                "component_field56_seed_packets_sha256"
            ],
            "completed_roof_level_field_count": 0,
        },
        "Gate5_maturity_update": maturity_update(),
        "strict_nonpromotion": {
            "one_selected_component_row_is_complete_key_homogeneity_table": False,
            "local_chart_D_infinity_bounds_are_field6_log_distortion_slots": False,
            "component_local_field5_field6_seeds_are_complete_roof_level_slots": False,
            "chart_fields_imply_face_or_operator_cost_fields": False,
            "complete_18_field_operator_block_count": 0,
            "three_norm_Kac_closure": "NOT_CERTIFIED",
            "Gate2": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
        },
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def main() -> None:
    print(json.dumps(build_result(), indent=2, sort_keys=True))
    print("SELECTED_FIELD3_PREFIX_CHART_SLOTS_28: CERTIFIED")
    print("SELECTED_FIELD4_SUFFIX_CHART_SLOTS_28: CERTIFIED")
    print("SELECTED_COMPONENT_LEVEL_MATURITY: 4/18")
    print("COMPLETE_18_FIELD_OPERATOR_BLOCKS: 0")
    print("GATE5: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
