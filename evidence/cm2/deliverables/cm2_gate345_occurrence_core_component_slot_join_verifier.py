#!/usr/bin/env python3
"""Fail-closed verifier for the occurrence/core/component/slot join."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import cm2_gate345_occurrence_core_component_slot_join_cert as certificate


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate345.occurrence-core-component-slot-join.manifest.v1"
RESULT_SCHEMA = "cm2.gate345.occurrence-core-component-slot-join.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate345-occurrence-core-component-slot-join-manifest-2026-07-18.json"
)
CERTIFICATE = HERE / "cm2_gate345_occurrence_core_component_slot_join_cert.py"


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def strict_equal(left: Any, right: Any) -> bool:
    return canonical_json(left) == canonical_json(right)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def result_digest(result: dict[str, Any]) -> str:
    payload = copy.deepcopy(result)
    payload.pop("internal_replay_digest", None)
    return digest(payload)


def expected_axes() -> dict[str, Any]:
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


def expected_registry() -> dict[str, Any]:
    return {
        "maximal_occurrence_owner_count": 64,
        "parameter_branch_count": 128,
        "distinct_destination_core_count": 14,
        "distinct_selected_maximal_component_count": 14,
        "all_destination_components_have_roof_one": True,
        "all_destination_bindings_have_roof_level_j_zero": True,
        "destination_core_occurrence_multiplicity_histogram": {
            "1": 2,
            "2": 4,
            "5": 1,
            "6": 3,
            "7": 1,
            "8": 3,
        },
        "operator_binding_count": 14,
        "field_1_component_entity_binding_count": 14,
        "field_1_fictitious_slot_id_count": 0,
        "field_3_prefix_chart_slot_binding_count": 14,
        "field_4_suffix_chart_slot_binding_count": 14,
        "field_7_cut_growth_slot_binding_count": 14,
        "bound_existing_field_count_per_destination_component": 4,
        "required_field_count_per_component_level": 18,
        "occurrence_join_owners_sha256": (
            "e2a9ed3abd6c751d6ae624f1d43bf49e3b1f950c1280a41c84ae0a0d64e9ac12"
        ),
        "parameter_branch_rows_sha256": (
            "8bf9b91e592593c51ccad2e5b362f878936f24dfed452e89b1a727689a5277df"
        ),
        "operator_binding_rows_sha256": (
            "cd6f78d00aea0a60987ed5fd2c5c55c2000890692f16e7d65fe34d7aa482ee6a"
        ),
        "occurrence_to_core_sha256": (
            "4228179de0846e606a71270042cc5ce83b8fb3829e2f86d69617333fefa0cd4e"
        ),
        "core_to_operator_binding_sha256": (
            "758eec11c8aea9618786c28468e79c136dde5f7d9e5037027c748f888489f906"
        ),
        "first_occurrence_join_owner_id": (
            "occurrence-join:60950cad18918fd05583c8610e969dc41382598150b5c375f8563d87ac0e3e81"
        ),
        "last_occurrence_join_owner_id": (
            "occurrence-join:af963be4ddb94b1ad072ee5c60bf10bb5809e61a4bf0111df55765f03bceab9e"
        ),
        "first_operator_binding_id": (
            "operator-binding:cc9130889e5c8026c52091dbcaa22ec53e6d65ec18e8f5aa917f68b02315b071"
        ),
        "last_operator_binding_id": (
            "operator-binding:73ccd0a3c38ab512f085b98f424ab4d06727fc2d1695a9e821a39f8ba7d3c2b0"
        ),
        "independent_axis_typing_guard": expected_axes(),
    }


def check(manifest: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(manifest, dict):
        return ["manifest type"]
    if manifest.get("schema") != SCHEMA:
        errors.append("manifest schema")
    if manifest.get("certificate_sha256") != sha256_path(CERTIFICATE):
        errors.append("certificate hash")
    if manifest.get("verifier_sha256") != sha256_path(Path(__file__)):
        errors.append("verifier hash")
    if not strict_equal(manifest.get("dependencies"), certificate.DEPENDENCIES):
        errors.append("dependency table")
    result = manifest.get("result", {})
    if result.get("schema") != RESULT_SCHEMA:
        errors.append("result schema")
    if result.get("internal_replay_digest") != result_digest(result):
        errors.append("result digest")
    expected_provenance = {
        "dependency_sha256": certificate.DEPENDENCIES,
        "old_artifacts_modified": False,
        "join_policy": "exact_canonical_key_unique_join",
    }
    if not strict_equal(result.get("provenance"), expected_provenance):
        errors.append("provenance")
    if not strict_equal(
        result.get("occurrence_core_component_slot_join_registry"),
        expected_registry(),
    ):
        errors.append("join registry")
    expected_maturity = {
        "selected_component_level_maturity": "4_OF_18",
        "new_field_promotions_this_join": 0,
        "complete_key_homogeneity_table_count": 0,
        "complete_18_field_operator_block_count": 0,
        "first_missing_field": "physical_homogeneity_subbranch_table",
    }
    if not strict_equal(result.get("Gate5_maturity_boundary"), expected_maturity):
        errors.append("Gate5 maturity boundary")
    expected_scope = {
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
    }
    if not strict_equal(result.get("strict_nonpromotion"), expected_scope):
        errors.append("strict nonpromotion")
    expected_verdict = {
        "occurrence_core_component_slot_join_64_128_14": "CERTIFIED",
        "destination_field_1_3_4_7_bindings_14": "CERTIFIED",
        "parameter_recovery_kac_axes_distinct": "CERTIFIED_TYPED",
        "q_charge_multiplicity_per_occurrence_1": "CERTIFIED_TYPED",
        "common_strong_space_operator": "NOT_CERTIFIED",
        "complete_physical_Kac": "NOT_CERTIFIED",
        "complete_18_field_operator_blocks": 0,
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
    }
    if not strict_equal(manifest.get("verdict"), expected_verdict):
        errors.append("verdict")
    return errors


def refresh(manifest: dict[str, Any]) -> None:
    manifest["result"]["internal_replay_digest"] = result_digest(
        manifest["result"]
    )


def self_test(manifest: dict[str, Any]) -> tuple[int, int]:
    mutations: list[dict[str, Any]] = []

    def mutate(path: tuple[str, ...], value: Any) -> None:
        candidate = copy.deepcopy(manifest)
        target: Any = candidate
        for part in path[:-1]:
            target = target[part]
        target[path[-1]] = value
        if path[0] == "result":
            refresh(candidate)
        mutations.append(candidate)

    registry = ("result", "occurrence_core_component_slot_join_registry")
    mutate(registry + ("maximal_occurrence_owner_count",), 63)
    mutate(registry + ("parameter_branch_count",), 127)
    mutate(registry + ("distinct_destination_core_count",), 13)
    mutate(registry + ("distinct_selected_maximal_component_count",), 13)
    mutate(registry + ("all_destination_components_have_roof_one",), False)
    mutate(registry + ("all_destination_bindings_have_roof_level_j_zero",), False)
    mutate(registry + ("operator_binding_count",), 13)
    mutate(registry + ("field_1_component_entity_binding_count",), 13)
    mutate(registry + ("field_1_fictitious_slot_id_count",), 14)
    mutate(registry + ("field_3_prefix_chart_slot_binding_count",), 13)
    mutate(registry + ("field_4_suffix_chart_slot_binding_count",), 13)
    mutate(registry + ("field_7_cut_growth_slot_binding_count",), 13)
    mutate(registry + ("bound_existing_field_count_per_destination_component",), 5)
    mutate(registry + ("required_field_count_per_component_level",), 17)
    mutate(registry + ("occurrence_join_owners_sha256",), "0" * 64)
    mutate(registry + ("parameter_branch_rows_sha256",), "0" * 64)
    mutate(registry + ("operator_binding_rows_sha256",), "0" * 64)
    mutate(registry + ("occurrence_to_core_sha256",), "0" * 64)
    mutate(registry + ("core_to_operator_binding_sha256",), "0" * 64)
    axes = registry + ("independent_axis_typing_guard",)
    mutate(axes + ("axes_are_not_positionally_zipped",), False)
    mutate(axes + ("parameter_side_is_not_recovery_orientation",), False)
    mutate(axes + ("parameter_side_is_not_kac_coordinate",), False)
    mutate(axes + ("recovery_orientation_is_not_kac_coordinate",), False)
    mutate(axes + ("flat_cross_product_rows_materialized",), 512)
    mutate(axes + ("incorrect_multiple_q_charge_rows_materialized",), 128)
    mutate(axes + ("charge_owner_axis", "q_charge_multiplicity_per_occurrence"), 8)
    mutate(axes + ("recovery_orientation_axis", "views_are_alternative_nonadditive"), False)
    mutate(axes + ("singular_kac_coordinate_axis", "complete_four_term_physical_Kac_typing"), "CERTIFIED")
    mutate(("result", "Gate5_maturity_boundary", "selected_component_level_maturity"), "5_OF_18")
    mutate(("result", "Gate5_maturity_boundary", "new_field_promotions_this_join"), 1)
    mutate(("result", "Gate5_maturity_boundary", "complete_18_field_operator_block_count"), 14)
    scope = ("result", "strict_nonpromotion")
    mutate(scope + ("parameter_branches_are_recovery_orientations",), True)
    mutate(scope + ("parameter_branches_are_kac_coordinates",), True)
    mutate(scope + ("forward_reverse_views_are_additive_charges",), True)
    mutate(scope + ("field_1_has_a_separate_slot_id",), True)
    mutate(scope + ("operator_binding_is_common_strong_space_operator",), True)
    mutate(scope + ("physical_recovery_carrier_join",), "CERTIFIED")
    mutate(scope + ("common_two_view_restriction_id",), "CERTIFIED")
    mutate(scope + ("three_norm_intertwiners",), "CERTIFIED")
    mutate(scope + ("complete_physical_Kac_typing",), "CERTIFIED")
    mutate(scope + ("Gate5",), "CERTIFIED")
    mutate(("verdict", "common_strong_space_operator"), "CERTIFIED")
    mutate(("verdict", "complete_physical_Kac"), "CERTIFIED")
    mutate(("verdict", "complete_18_field_operator_blocks"), 14)
    mutate(("verdict", "Gate5"), "CERTIFIED")
    mutate(registry + ("all_destination_components_have_roof_one",), 1)
    rejected = sum(bool(check(candidate)) for candidate in mutations)
    return rejected, len(mutations)


def main() -> int:
    if sys.flags.optimize != 0:
        print("ERROR: optimized Python disables proof assertions", file=sys.stderr)
        return 1
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--replay", action="store_true")
    modes.add_argument("--integrity-only", action="store_true")
    modes.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    except Exception as error:
        print(f"MANIFEST_READ_ERROR: {error}", file=sys.stderr)
        return 1
    errors = check(manifest)
    if errors:
        print("ERROR: " + "; ".join(errors), file=sys.stderr)
        return 1
    if args.replay and canonical_json(certificate.build_result()) != canonical_json(
        manifest["result"]
    ):
        print("ERROR: replay mismatch", file=sys.stderr)
        return 1
    if args.self_test:
        rejected, total = self_test(manifest)
        status = "PASS" if rejected == total else "FAIL"
        print(f"SELF_TEST: {status} ({rejected}/{total} mutations rejected)")
        return 0 if rejected == total else 1
    if args.replay or args.integrity_only:
        print("REPLAY_AND_INTEGRITY: PASS")
        return 0
    print("OCCURRENCE_CORE_COMPONENT_SLOT_JOIN_64_128_14: CERTIFIED")
    print("DESTINATION_FIELD_1_3_4_7_BINDINGS_14: CERTIFIED")
    print("PARAMETER_RECOVERY_KAC_AXES_DISTINCT: CERTIFIED_TYPED")
    print("Q_CHARGE_MULTIPLICITY_PER_OCCURRENCE_1: CERTIFIED_TYPED")
    print("COMMON_STRONG_SPACE_OPERATOR: NOT_CERTIFIED")
    print("COMPLETE_PHYSICAL_KAC: NOT_CERTIFIED")
    print("GATE5: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
