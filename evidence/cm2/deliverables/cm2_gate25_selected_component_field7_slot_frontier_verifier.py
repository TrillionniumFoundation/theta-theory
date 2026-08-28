#!/usr/bin/env python3
"""Fail-closed verifier for selected physical field-7 slots."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import cm2_gate25_selected_component_field7_slot_frontier_cert as certificate


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate25.selected-component-field7-slot-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate25.selected-component-field7-slot-frontier.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate25-selected-component-field7-slot-frontier-manifest-2026-07-17.json"
)
CERTIFICATE = HERE / "cm2_gate25_selected_component_field7_slot_frontier_cert.py"


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
    else:
        for name, expected in certificate.DEPENDENCIES.items():
            path = HERE / name
            if not path.is_file() or sha256_path(path) != expected:
                errors.append(f"dependency {name}")

    result = manifest.get("result", {})
    if result.get("schema") != RESULT_SCHEMA:
        errors.append("result schema")
    if result.get("internal_replay_digest") != result_digest(result):
        errors.append("result digest")

    registry = result.get("selected_component_slot_registry", {})
    expected_registry = {
        "selected_physical_word_key_count": 24,
        "selected_positive_maximal_component_count": 24,
        "selected_homogeneous_component_row_id_count": 24,
        "source_histogram": {"G": 12, "W": 12},
        "roof_histogram": {"1": 20, "2": 4},
        "materialized_field7_roof_slot_count": 28,
        "component_rows_sha256": (
            "a02b90fa85b3ef4dc0bb02062d0e94ba890b31bd6d9032bbad7e3e1a2dc5aa86"
        ),
        "field7_level_slots_sha256": (
            "ad37d694a6fa2dbd455c0ef865c2ea07d97d7bcc7a940cf526d8c272c46259d4"
        ),
        "complete_all_key_homogeneity_table": False,
    }
    for key, expected in expected_registry.items():
        if registry.get(key) != expected:
            errors.append(f"registry {key}")

    components = result.get("selected_component_rows", [])
    slots = result.get("materialized_field7_level_slots", [])
    if not isinstance(components, list) or len(components) != 24:
        errors.append("component rows")
    else:
        for row in components:
            if row.get("field_1_nonempty_or_empty_domain_proof") != "NONEMPTY":
                errors.append("component field1")
                break
            if row.get("selected_row_is_complete_key_homogeneity_table") is not False:
                errors.append("component table nonpromotion")
                break
            expected = "580000/1999" if row.get("source_obstacle") == "G" else "572000/1999"
            if row.get("field_7_one_step_cut_growth_Z_sum_upper") != expected:
                errors.append("component field7")
                break
    if not isinstance(slots, list) or len(slots) != 28:
        errors.append("field7 slots")
    else:
        if len({row.get("immutable_slot_id") for row in slots}) != 28:
            errors.append("field7 slot uniqueness")
        for row in slots:
            if row.get("field_name") != "one_step_cut_growth_Z_sum":
                errors.append("field7 slot name")
                break
            if row.get("physical_field_7_status") != "FINITE_FORMULA_CERTIFIED":
                errors.append("field7 slot status")
                break
            if row.get("field_7_growth_contraction_without_dwell") is not False:
                errors.append("field7 no dwell contraction")
                break

    selected = result.get("selected_homoclinic_field7_binding", {})
    expected_selected = {
        "selected_QNL_homoclinic_maximal_component_id": (
            "7359148da1c43a255f2238d9c831b8638f2c9885035034a5792699c968b2f3b5"
        ),
        "selected_QNL_homoclinic_field7_slot_id": (
            "slot:530fb5797b653dca584f9c9ac32ce70328dea04f8fca3db195349dd663948c8f"
        ),
        "selected_QNL_homoclinic_field7_multiplier_upper": "580000/1999",
        "selected_QNL_homoclinic_component_field7_slot": "CERTIFIED",
        "stable_quotient_branch_label_from_component_incidence": False,
    }
    for key, expected in expected_selected.items():
        if selected.get(key) != expected:
            errors.append(f"selected {key}")

    dwell = result.get("scheduled_dwell_attachment", {})
    expected_dwell = {
        "attached_to_each_of_28_selected_field7_slots": True,
        "registered_cut_factor_upper": "580000/1999",
        "required_fixed_core_dwell_steps": 12108,
        "cycle_coefficient_strict_upper": "13213125/16375808",
        "rational_exponential_cut_weight": "6/5",
        "weighted_cycle_coefficient_strict_upper": "7927875/8187904",
        "weighted_Green_resolvent_strict_upper": "32",
        "conditional_scheduled_contraction_packet": "CERTIFIED",
        "physical_occurrence_to_core_incidence": "NOT_CERTIFIED",
        "native_no_hidden_cut_12108_step_dwell": "NOT_CERTIFIED",
        "common_strong_operator_space": "NOT_CERTIFIED",
        "physical_scheduled_contraction_on_selected_slots": "NOT_CERTIFIED",
    }
    for key, expected in expected_dwell.items():
        if dwell.get(key) != expected:
            errors.append(f"dwell {key}")

    maturity = result.get("Gate5_maturity_update", {})
    expected_maturity = {
        "required_field_count_per_physical_homogeneous_level": 18,
        "completed_field_count_on_each_selected_component_level": 2,
        "materialized_selected_component_level_count": 28,
        "selected_component_field7_physical_slot_count": 28,
        "complete_key_homogeneity_tables": 0,
        "complete_18_field_operator_block_count": 0,
        "remaining_field_count_on_each_selected_component_level": 16,
        "Gate5": "NOT_CERTIFIED",
    }
    for key, expected in expected_maturity.items():
        if maturity.get(key) != expected:
            errors.append(f"maturity {key}")

    scope = result.get("strict_nonpromotion", {})
    for key in (
        "one_selected_h_row_implies_complete_key_homogeneity_table",
        "field7_formula_implies_fields_2_to_6_or_8_to_18",
        "conditional_dwell_packet_implies_physical_dwell_schedule",
        "selected_component_incidence_implies_stable_quotient_branch",
    ):
        if scope.get(key) is not False:
            errors.append(f"nonpromotion {key}")
    if scope.get("complete_18_field_operator_block_count") != 0:
        errors.append("scope blocks")
    for key in ("stable_quotient_PPE", "three_norm_Kac_closure", "Gate2", "Gate5"):
        if scope.get(key) != "NOT_CERTIFIED":
            errors.append(f"scope {key}")

    expected_verdict = {
        "selected_positive_maximal_components": "24_CERTIFIED",
        "selected_homogeneous_component_row_ids": "24_CERTIFIED",
        "selected_field7_physical_roof_slots": "28_CERTIFIED",
        "selected_QNL_homoclinic_field7_slot": "CERTIFIED",
        "scheduled_dwell_packet_on_selected_slots": "CONDITIONAL_CERTIFIED",
        "complete_key_homogeneity_tables": 0,
        "complete_18_field_operator_blocks": 0,
        "Gate2": "NOT_CERTIFIED",
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

    def mutate(path: tuple[Any, ...], value: Any) -> None:
        candidate = copy.deepcopy(manifest)
        target: Any = candidate
        for part in path[:-1]:
            target = target[part]
        target[path[-1]] = value
        if path[0] == "result":
            refresh(candidate)
        mutations.append(candidate)

    mutate(("result", "selected_component_slot_registry", "selected_positive_maximal_component_count"), 23)
    mutate(("result", "selected_component_slot_registry", "materialized_field7_roof_slot_count"), 27)
    mutate(("result", "selected_component_slot_registry", "complete_all_key_homogeneity_table"), True)
    mutate(("result", "selected_component_rows", 0, "field_1_nonempty_or_empty_domain_proof"), "EMPTY")
    mutate(("result", "selected_component_rows", 0, "selected_row_is_complete_key_homogeneity_table"), True)
    mutate(("result", "materialized_field7_level_slots", 0, "physical_field_7_status"), "NOT_CERTIFIED")
    mutate(("result", "materialized_field7_level_slots", 0, "field_7_growth_contraction_without_dwell"), True)
    mutate(("result", "selected_homoclinic_field7_binding", "selected_QNL_homoclinic_component_field7_slot"), "NOT_CERTIFIED")
    mutate(("result", "selected_homoclinic_field7_binding", "stable_quotient_branch_label_from_component_incidence"), True)
    mutate(("result", "scheduled_dwell_attachment", "required_fixed_core_dwell_steps"), 0)
    mutate(("result", "scheduled_dwell_attachment", "physical_scheduled_contraction_on_selected_slots"), "CERTIFIED")
    mutate(("result", "Gate5_maturity_update", "completed_field_count_on_each_selected_component_level"), 18)
    mutate(("result", "Gate5_maturity_update", "complete_18_field_operator_block_count"), 24)
    mutate(("result", "strict_nonpromotion", "conditional_dwell_packet_implies_physical_dwell_schedule"), True)
    mutate(("result", "strict_nonpromotion", "Gate2"), "CERTIFIED")
    mutate(("result", "strict_nonpromotion", "Gate5"), "CERTIFIED")
    mutate(("verdict", "complete_18_field_operator_blocks"), 24)
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
    print("SELECTED_PHYSICAL_MAXIMAL_COMPONENT_ROWS: 24 CERTIFIED")
    print("MATERIALIZED_SELECTED_FIELD7_ROOF_SLOTS: 28 CERTIFIED")
    print("SELECTED_COMPONENT_FIELD_MATURITY: 2/18")
    print("COMPLETE_18_FIELD_OPERATOR_BLOCKS: 0")
    print("GATE2_GATE5: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
