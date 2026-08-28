#!/usr/bin/env python3
"""Fail-closed verifier for selected Gate-5 chart-field slots."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import cm2_gate25_selected_component_chart_field_slots_cert as certificate


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate25.selected-component-chart-field-slots.manifest.v1"
RESULT_SCHEMA = "cm2.gate25.selected-component-chart-field-slots.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate25-selected-component-chart-field-slots-manifest-2026-07-17.json"
)
CERTIFICATE = HERE / "cm2_gate25_selected_component_chart_field_slots_cert.py"


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def result_digest(result: dict[str, Any]) -> str:
    payload = copy.deepcopy(result)
    payload.pop("internal_replay_digest", None)
    return digest(payload)


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
    if manifest.get("dependencies") != certificate.DEPENDENCIES:
        errors.append("dependency table")
    result = manifest.get("result", {})
    if result.get("schema") != RESULT_SCHEMA:
        errors.append("result schema")
    if result.get("internal_replay_digest") != result_digest(result):
        errors.append("result digest")

    registry = result.get("selected_component_chart_slot_registry", {})
    expected_registry = {
        "selected_positive_maximal_component_count": 24,
        "selected_roof_level_count": 28,
        "materialized_field_3_prefix_chart_slot_count": 28,
        "materialized_field_4_suffix_chart_slot_count": 28,
        "materialized_chart_field_slot_count": 56,
        "all_roof_one_collision_to_collision_chart_pairs": True,
        "all_roof_two_collision_wall_collision_chart_pairs": True,
        "all_chart_pairs_are_part_of_the_implicit_maximal_component_predicate": True,
        "roof_histogram": {"1": 20, "2": 4},
    }
    for key, value in expected_registry.items():
        if registry.get(key) != value:
            errors.append(f"registry {key}")
    for key in ("chart_slots_sha256", "component_field56_seed_packets_sha256"):
        if not isinstance(registry.get(key), str) or not registry[key]:
            errors.append(f"registry digest {key}")

    seeds = result.get("selected_component_field5_field6_seed_registry", {})
    expected_seeds = {
        "selected_component_packet_count": 24,
        "seed_fields": [
            "inverse_Jacobian_bound", "log_Jacobian_distortion_sum",
        ],
        "completed_roof_level_field_count": 0,
    }
    for key, value in expected_seeds.items():
        if seeds.get(key) != value:
            errors.append(f"seed {key}")
    if seeds.get("component_packets_sha256") != registry.get(
        "component_field56_seed_packets_sha256"
    ):
        errors.append("seed digest join")

    maturity = result.get("Gate5_maturity_update", {})
    expected_maturity = {
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
    for key, value in expected_maturity.items():
        if maturity.get(key) != value:
            errors.append(f"maturity {key}")

    scope = result.get("strict_nonpromotion", {})
    for key in (
        "one_selected_component_row_is_complete_key_homogeneity_table",
        "local_chart_D_infinity_bounds_are_field6_log_distortion_slots",
        "component_local_field5_field6_seeds_are_complete_roof_level_slots",
        "chart_fields_imply_face_or_operator_cost_fields",
    ):
        if scope.get(key) is not False:
            errors.append(f"nonpromotion {key}")
    if scope.get("complete_18_field_operator_block_count") != 0:
        errors.append("scope complete blocks")
    for key in ("three_norm_Kac_closure", "Gate2", "Gate5"):
        if scope.get(key) != "NOT_CERTIFIED":
            errors.append(f"scope {key}")

    expected_verdict = {
        "selected_field3_prefix_chart_slots": "28_CERTIFIED",
        "selected_field4_suffix_chart_slots": "28_CERTIFIED",
        "selected_component_level_maturity": "4_OF_18",
        "complete_key_homogeneity_tables": 0,
        "complete_18_field_operator_blocks": 0,
        "Gate5": "NOT_CERTIFIED",
    }
    if manifest.get("verdict") != expected_verdict:
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

    registry = ("result", "selected_component_chart_slot_registry")
    mutate(registry + ("selected_positive_maximal_component_count",), 23)
    mutate(registry + ("selected_roof_level_count",), 27)
    mutate(registry + ("materialized_field_3_prefix_chart_slot_count",), 27)
    mutate(registry + ("materialized_field_4_suffix_chart_slot_count",), 27)
    mutate(registry + ("materialized_chart_field_slot_count",), 55)
    mutate(registry + ("all_roof_two_collision_wall_collision_chart_pairs",), False)
    mutate(registry + ("roof_histogram", "2"), 3)
    seeds = ("result", "selected_component_field5_field6_seed_registry")
    mutate(seeds + ("selected_component_packet_count",), 23)
    mutate(seeds + ("completed_roof_level_field_count",), 28)
    maturity = ("result", "Gate5_maturity_update")
    mutate(maturity + ("completed_field_count_on_each_selected_component_level",), 6)
    mutate(maturity + ("previous_completed_field_count",), 4)
    mutate(maturity + ("remaining_field_count_on_each_selected_component_level",), 12)
    mutate(maturity + ("first_missing_field",), "none")
    mutate(maturity + ("complete_key_homogeneity_table_count",), 24)
    mutate(maturity + ("complete_18_field_operator_block_count",), 28)
    scope = ("result", "strict_nonpromotion")
    mutate(scope + ("one_selected_component_row_is_complete_key_homogeneity_table",), True)
    mutate(scope + ("local_chart_D_infinity_bounds_are_field6_log_distortion_slots",), True)
    mutate(scope + ("component_local_field5_field6_seeds_are_complete_roof_level_slots",), True)
    mutate(scope + ("Gate5",), "CERTIFIED")
    mutate(("verdict", "selected_component_level_maturity"), "18_OF_18")
    mutate(("verdict", "Gate5"), "CERTIFIED")
    rejected = sum(bool(check(candidate)) for candidate in mutations)
    return rejected, len(mutations)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
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
    if args.replay and certificate.build_result() != manifest["result"]:
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
    print("SELECTED_FIELD3_PREFIX_CHART_SLOTS_28: CERTIFIED")
    print("SELECTED_FIELD4_SUFFIX_CHART_SLOTS_28: CERTIFIED")
    print("SELECTED_COMPONENT_LEVEL_MATURITY: 4/18")
    print("COMPLETE_18_FIELD_OPERATOR_BLOCKS: 0")
    print("GATE5: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
