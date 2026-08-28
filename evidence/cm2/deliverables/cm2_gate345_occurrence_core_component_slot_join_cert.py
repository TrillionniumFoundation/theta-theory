#!/usr/bin/env python3
"""Join charged first-core cylinders to selected Gate-5 component slots.

This certificate materializes the exact finite join

    occurrence / parameter side -> destination 24-core
      -> selected maximal component -> fields 1, 3, 4 and 7.

The 128 hit/miss parameter cylinders belong to 64 occurrence owners and land
in 14 distinct roof-one cores.  Each core has one exact selected component
binding and existing field-3, field-4 and field-7 immutable slot IDs.  Field 1
is bound to the selected homogeneous component row itself; no fictitious
field-1 slot ID is created.

The certificate also freezes a type guard separating three superficially
equal-size axes: parameter side, forward/reverse recovery view, and the two
singular Kac output coordinates.  Recovery views are alternative and
nonadditive, the two Kac coordinates share one occurrence measure, and the
single q charge belongs to the occurrence owner.  No positional zip or
multiple q charge is allowed.

This is an exact data/interface join, not a common-strong-space operator,
physical recovery carrier, complete Kac closure, or new Gate-5 field.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate25_selected_component_chart_field_slots_cert as chart_slots
import cm2_gate34_all_occurrence_first_core_stopping_cert as first_stopping
import cm2_gate4_all_sheet_single_charge_schema_cert as single_charge
import cm2_gate4_product_same_occurrence_joint_moment_frontier_cert as product
import cm2_gate45_corrected_maximal_row_kac_ledger_cert as kac
import cm2_gate3_global_borel_current_assembly_cert as current


HERE = Path(__file__).resolve().parent

DEPENDENCIES = {
    "cm2-gate34-all-occurrence-first-core-stopping-manifest-2026-07-18.json": (
        "a40b52dcbeef8c9f3471115b2bbd2c438cc6e130c72bd619dd794d8925d97171"
    ),
    "cm2_gate34_all_occurrence_first_core_stopping_cert.py": (
        "8a22c1a2483822b849562acb06775298a8e9d3a84d753e29ebe86229d35ad1fb"
    ),
    "cm2-gate25-selected-component-chart-field-slots-manifest-2026-07-17.json": (
        "417464531cae76bf774bdc35f1d2f25799237d1efde39be8850cf3408740f271"
    ),
    "cm2_gate25_selected_component_chart_field_slots_cert.py": (
        "666e7f1ea4198528b143b522d2c5daf55ba4fecfd127d86663b23e0bb38a477f"
    ),
    "cm2-gate25-selected-component-field7-slot-frontier-manifest-2026-07-17.json": (
        "75de341183ef7fbcc7937f69bc7c6f276d06db0883397a7c99e4d54bbc5dc91a"
    ),
    "cm2-gate4-all-sheet-single-charge-schema-manifest-2026-07-15.json": (
        "7d66dcfdc607dcacd2e3800fccccf7700a162474325449e97e3643d8f84ab0f8"
    ),
    "cm2_gate4_all_sheet_single_charge_schema_cert.py": (
        "a49e4c670137ccfc580614fb35a9d2f004020840e479158392f8e210b46218a8"
    ),
    "cm2-gate4-product-same-occurrence-joint-moment-frontier-manifest-2026-07-16.json": (
        "67db1ec8aead4cbb0ff966e9136508636690074acb5959a6d705893eeef00eff"
    ),
    "cm2_gate4_product_same_occurrence_joint_moment_frontier_cert.py": (
        "759f6cb1d9cf97cb253326fe62bad6a00ae31beb9f6b1944ad41a0520f65bab3"
    ),
    "cm2-gate45-corrected-maximal-row-kac-ledger-manifest-2026-07-15.json": (
        "d5f563545c4ddaddfbb6b5cde5c4f5d8030247209e2284c06aeb9d3255a771f0"
    ),
    "cm2_gate45_corrected_maximal_row_kac_ledger_cert.py": (
        "319a83b0b4d2fb6bda31f4366fd68d713b89bc79c7734e2fc41e330b0a816b8b"
    ),
    "cm2_gate25_physical_return_core_registry_cert.py": (
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"
    ),
    "cm2_gate3_global_borel_current_assembly_cert.py": (
        "bf7e9f77063a0d390f8a0337e1591be368ffbc4d2588e9e4fb5c7cbc18859d1b"
    ),
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_dependencies() -> None:
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        assert path.is_file()
        assert sha256_path(path) == expected
    stopping = json.loads(
        (
            HERE
            / "cm2-gate34-all-occurrence-first-core-stopping-manifest-2026-07-18.json"
        ).read_text(encoding="utf-8")
    )
    assert stopping["verdict"][
        "charged_first_core_stopping_cylinders_128"
    ] == "CERTIFIED"
    chart_manifest = json.loads(
        (
            HERE
            / "cm2-gate25-selected-component-chart-field-slots-manifest-2026-07-17.json"
        ).read_text(encoding="utf-8")
    )
    assert chart_manifest["verdict"]["selected_component_level_maturity"] == (
        "4_OF_18"
    )
    assert chart_manifest["verdict"]["Gate5"] == "NOT_CERTIFIED"


def parameter_branch_rows(
    maximal_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, str]]:
    by_id = {row["occurrence_id"]: row for row in maximal_rows}
    specifications = first_stopping.occurrence_specifications(maximal_rows)
    first_stopping.all_charge.refresh_arb_constants()
    rows = []
    occurrence_to_core: dict[str, str] = {}
    for occurrence_id, specification in sorted(specifications.items()):
        source = by_id[occurrence_id]
        side_rows = []
        for side in ("hit", "miss"):
            replay = first_stopping.replay_first_stopping_branch(
                source,
                specification,
                side,
                "join-owner:" + occurrence_id,
            )
            side_rows.append({
                "occurrence_id": occurrence_id,
                "parameter_side": side,
                "parameter_sign": (
                    source["parameter_coarea_polarity"]
                    if side == "hit"
                    else -source["parameter_coarea_polarity"]
                ),
                "suffix_relative_first_core_time": replay[
                    "first_core_stopping_time_from_regular_suffix"
                ],
                "destination_core_id": replay["destination_core_id"],
                "first_stopping_branch_id": replay[
                    "first_stopping_branch_id"
                ],
            })
        assert len({row["destination_core_id"] for row in side_rows}) == 1
        occurrence_to_core[occurrence_id] = side_rows[0]["destination_core_id"]
        rows.extend(side_rows)
    rows.sort(key=canonical_json)
    assert len(rows) == 128
    assert len({(row["occurrence_id"], row["parameter_side"]) for row in rows}) == 128
    assert len(occurrence_to_core) == 64
    return rows, occurrence_to_core


def selected_slot_tables() -> tuple[
    dict[str, dict[str, Any]],
    dict[tuple[str, str, int, str], dict[str, Any]],
    dict[tuple[str, str, int], dict[str, Any]],
]:
    loaded = chart_slots.load_dependencies()
    selected = loaded[
        "cm2-gate25-selected-component-field7-slot-frontier-manifest-2026-07-17.json"
    ]
    walls = loaded[
        "cm2-gate25-roof-two-wall-chart-frontier-manifest-2026-07-16.json"
    ]
    universal = loaded[
        "cm2-gate25-universal-operator-endpoint-template-frontier-manifest-2026-07-16.json"
    ]
    chart_rows, _packets, chart_registry = chart_slots.materialize_chart_slots(
        selected, walls, universal
    )
    frozen_chart_manifest = json.loads(
        (
            HERE
            / "cm2-gate25-selected-component-chart-field-slots-manifest-2026-07-17.json"
        ).read_text(encoding="utf-8")
    )
    assert chart_registry == frozen_chart_manifest["result"][
        "selected_component_chart_slot_registry"
    ]
    selected_result = selected["result"]
    components = {
        canonical_json(row["physical_key"]): row
        for row in selected_result["selected_component_rows"]
    }
    assert len(components) == 24
    chart_by_key = {
        (
            row["maximal_component_id"],
            row["homogeneous_subbranch_id"],
            row["roof_level_j"],
            row["field_name"],
        ): row
        for row in chart_rows
    }
    assert len(chart_by_key) == 56
    field7_by_key = {
        (
            row["maximal_component_id"],
            row["homogeneous_subbranch_id"],
            row["roof_level_j"],
        ): row
        for row in selected_result["materialized_field7_level_slots"]
    }
    assert len(field7_by_key) == 28
    return components, chart_by_key, field7_by_key


def operator_bindings(
    destination_core_ids: set[str],
) -> tuple[list[dict[str, Any]], dict[str, str]]:
    cores_by_id = {
        first_stopping.core_id(core): core
        for core in core_cert.physical_cores()
    }
    assert len(cores_by_id) == 24
    assert destination_core_ids <= set(cores_by_id)
    components, chart_by_key, field7_by_key = selected_slot_tables()
    rows = []
    core_to_binding: dict[str, str] = {}
    for identifier in sorted(destination_core_ids):
        core = cores_by_id[identifier]
        physical_key = chart_slots.exact_key(core)
        component = components[canonical_json(physical_key)]
        assert component["roof"] == 1
        assert component["field_1_nonempty_or_empty_domain_proof"] == "NONEMPTY"
        component_id = component["maximal_component_id"]
        homogeneous_id = component["selected_homogeneous_component_row_id"]
        field3 = chart_by_key[
            (component_id, homogeneous_id, 0, "homogeneous_prefix_chart")
        ]
        field4 = chart_by_key[
            (component_id, homogeneous_id, 0, "homogeneous_suffix_chart")
        ]
        field7 = field7_by_key[(component_id, homogeneous_id, 0)]
        assert field3["word_key"] == physical_key
        assert field4["word_key"] == physical_key
        assert field7["word_key"] == physical_key
        payload = {
            "destination_core_id": identifier,
            "physical_key": physical_key,
            "maximal_component_id": component_id,
            "homogeneous_subbranch_id": homogeneous_id,
            "roof_level_j": 0,
            "field3_slot_id": field3["immutable_slot_id"],
            "field4_slot_id": field4["immutable_slot_id"],
            "field7_slot_id": field7["immutable_slot_id"],
        }
        binding_id = "operator-binding:" + canonical_digest(payload)
        core_to_binding[identifier] = binding_id
        rows.append({
            "operator_binding_id": binding_id,
            "destination_core_id": identifier,
            "physical_key": physical_key,
            "maximal_component_id": component_id,
            "selected_homogeneous_component_row_id": homogeneous_id,
            "roof": 1,
            "roof_level_j": 0,
            "field_1_entity_type": "selected_homogeneous_component_row",
            "field_1_entity_id": homogeneous_id,
            "field_1_has_separate_immutable_slot_id": False,
            "field_3_prefix_chart_slot_id": field3["immutable_slot_id"],
            "field_4_suffix_chart_slot_id": field4["immutable_slot_id"],
            "field_7_cut_growth_slot_id": field7["immutable_slot_id"],
            "bound_existing_field_count": 4,
            "required_field_count": 18,
        })
    rows.sort(key=canonical_json)
    assert len(rows) == 14
    assert len(core_to_binding) == 14
    assert len({row["maximal_component_id"] for row in rows}) == 14
    assert len({row["field_3_prefix_chart_slot_id"] for row in rows}) == 14
    assert len({row["field_4_suffix_chart_slot_id"] for row in rows}) == 14
    assert len({row["field_7_cut_growth_slot_id"] for row in rows}) == 14
    return rows, core_to_binding


def independent_axis_schema(maximal_rows: list[dict[str, Any]]) -> dict[str, Any]:
    contract = single_charge.universal_occurrence_contract()
    product_record = product.same_occurrence_product_record()
    kac_ledger = kac.corrected_occurrence_ledger(maximal_rows)
    assert contract["endpoint_views_are_nonadditive"] is True
    assert contract["charged_occurrence_count"] == 1
    assert contract["pre_recovery_single_charge"] == (
        "q_e=max(C_fw(e),C_rev(e),2)*m_e"
    )
    assert product_record[
        "forward_reverse_are_alternative_nonadditive_views"
    ] is True
    assert kac_ledger["singular_kac_coordinate_count"] == 128
    assert kac_ledger["one_corrected_m_per_occurrence"] is True
    assert kac_ledger["one_q_expression_per_occurrence"] is True
    return {
        "parameter_side_axis": {
            "values": ["hit", "miss"],
            "meaning": "actual_parameter_side_of_Gate34_germ",
            "record_count": 128,
        },
        "recovery_orientation_axis": {
            "values": ["fw", "rev"],
            "meaning": "alternative_views_of_one_occurrence_restriction",
            "views_are_alternative_nonadditive": True,
            "physical_carrier_join": "NOT_CERTIFIED",
            "common_restriction_id_join": "NOT_CERTIFIED",
        },
        "singular_kac_coordinate_axis": {
            "values": ["dot(S)h", "dot(r)*mu(h)"],
            "meaning": "two_linear_output_coordinates_sharing_one_m_e",
            "shared_mark": [1, -1],
            "record_count": 128,
            "complete_four_term_physical_Kac_typing": "NOT_CERTIFIED",
        },
        "charge_owner_axis": {
            "owner": "occurrence_id",
            "occurrence_count": 64,
            "single_q_formula": "q_e=max(C_fw(e),C_rev(e),2)*m_e",
            "q_charge_multiplicity_per_occurrence": 1,
        },
        "parameter_side_is_not_recovery_orientation": True,
        "parameter_side_is_not_kac_coordinate": True,
        "recovery_orientation_is_not_kac_coordinate": True,
        "axes_are_not_positionally_zipped": True,
        "flat_cross_product_rows_materialized": 0,
        "incorrect_multiple_q_charge_rows_materialized": 0,
    }


def joined_registry() -> dict[str, Any]:
    maximal_rows, _registry = current.load_maximal_rows()
    assert len(maximal_rows) == 64
    branches, occurrence_to_core = parameter_branch_rows(maximal_rows)
    bindings, core_to_binding = operator_bindings(set(occurrence_to_core.values()))
    branches_by_occurrence: dict[str, list[dict[str, Any]]] = {}
    for row in branches:
        branches_by_occurrence.setdefault(row["occurrence_id"], []).append(row)
    owners = []
    for occurrence_id in sorted(occurrence_to_core):
        parameter_rows = sorted(
            branches_by_occurrence[occurrence_id],
            key=lambda row: row["parameter_side"],
        )
        assert [row["parameter_side"] for row in parameter_rows] == ["hit", "miss"]
        core_id = occurrence_to_core[occurrence_id]
        payload = {
            "occurrence_id": occurrence_id,
            "destination_core_id": core_id,
            "operator_binding_id": core_to_binding[core_id],
            "parameter_branch_ids": [
                row["first_stopping_branch_id"] for row in parameter_rows
            ],
        }
        owners.append({
            "occurrence_join_owner_id": "occurrence-join:" + canonical_digest(payload),
            "occurrence_id": occurrence_id,
            "parameter_branches": parameter_rows,
            "hit_and_miss_share_destination_core": True,
            "destination_core_id": core_id,
            "operator_binding_id": core_to_binding[core_id],
            "q_charge_owner": occurrence_id,
            "q_charge_multiplicity": 1,
        })
    owners.sort(key=canonical_json)
    assert len(owners) == 64
    multiplicities = Counter(occurrence_to_core.values())
    multiplicity_histogram = Counter(multiplicities.values())
    expected_multiplicity_histogram = {
        "1": 2, "2": 4, "5": 1, "6": 3, "7": 1, "8": 3,
    }
    assert {
        str(key): value for key, value in sorted(multiplicity_histogram.items())
    } == expected_multiplicity_histogram
    assert sum(multiplicities.values()) == 64
    axes = independent_axis_schema(maximal_rows)
    return {
        "maximal_occurrence_owner_count": 64,
        "parameter_branch_count": 128,
        "distinct_destination_core_count": 14,
        "distinct_selected_maximal_component_count": 14,
        "all_destination_components_have_roof_one": True,
        "all_destination_bindings_have_roof_level_j_zero": True,
        "destination_core_occurrence_multiplicity_histogram": (
            expected_multiplicity_histogram
        ),
        "operator_binding_count": 14,
        "field_1_component_entity_binding_count": 14,
        "field_1_fictitious_slot_id_count": 0,
        "field_3_prefix_chart_slot_binding_count": 14,
        "field_4_suffix_chart_slot_binding_count": 14,
        "field_7_cut_growth_slot_binding_count": 14,
        "bound_existing_field_count_per_destination_component": 4,
        "required_field_count_per_component_level": 18,
        "occurrence_join_owners_sha256": canonical_digest(owners),
        "parameter_branch_rows_sha256": canonical_digest(branches),
        "operator_binding_rows_sha256": canonical_digest(bindings),
        "occurrence_to_core_sha256": canonical_digest(occurrence_to_core),
        "core_to_operator_binding_sha256": canonical_digest(core_to_binding),
        "first_occurrence_join_owner_id": owners[0]["occurrence_join_owner_id"],
        "last_occurrence_join_owner_id": owners[-1]["occurrence_join_owner_id"],
        "first_operator_binding_id": bindings[0]["operator_binding_id"],
        "last_operator_binding_id": bindings[-1]["operator_binding_id"],
        "independent_axis_typing_guard": axes,
    }


def build_result() -> dict[str, Any]:
    load_dependencies()
    result: dict[str, Any] = {
        "schema": "cm2.gate345.occurrence-core-component-slot-join.v1",
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "join_policy": "exact_canonical_key_unique_join",
        },
        "occurrence_core_component_slot_join_registry": joined_registry(),
        "Gate5_maturity_boundary": {
            "selected_component_level_maturity": "4_OF_18",
            "new_field_promotions_this_join": 0,
            "complete_key_homogeneity_table_count": 0,
            "complete_18_field_operator_block_count": 0,
            "first_missing_field": "physical_homogeneity_subbranch_table",
        },
        "strict_nonpromotion": {
            "parameter_branches_are_recovery_orientations": False,
            "parameter_branches_are_kac_coordinates": False,
            "forward_reverse_views_are_additive_charges": False,
            "field_1_has_a_separate_slot_id": False,
            "operator_binding_is_common_strong_space_operator": False,
            "physical_recovery_carrier_join": "NOT_CERTIFIED",
            "common_two_view_restriction_id": "NOT_CERTIFIED",
            "three_norm_intertwiners": "NOT_CERTIFIED",
            "complete_physical_Kac_typing": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
        },
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def main() -> None:
    print(json.dumps(build_result(), indent=2, sort_keys=True))
    print("OCCURRENCE_CORE_COMPONENT_SLOT_JOIN_64_128_14: CERTIFIED")
    print("DESTINATION_FIELD_1_3_4_7_BINDINGS_14: CERTIFIED")
    print("PARAMETER_RECOVERY_KAC_AXES_DISTINCT: CERTIFIED_TYPED")
    print("Q_CHARGE_MULTIPLICITY_PER_OCCURRENCE_1: CERTIFIED_TYPED")
    print("COMMON_STRONG_SPACE_OPERATOR: NOT_CERTIFIED")
    print("COMPLETE_PHYSICAL_KAC: NOT_CERTIFIED")
    print("GATE5: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
