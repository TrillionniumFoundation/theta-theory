#!/usr/bin/env python3
"""Fail-closed verifier for the physical Gate-2/5 boundary reduction."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import cm2_gate25_physical_boundary_root_order_frontier_cert as certificate


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate25.physical-boundary-root-order-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate25.physical-boundary-root-order-frontier.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate25-physical-boundary-root-order-frontier-manifest-2026-07-17.json"
)
CERTIFICATE = HERE / "cm2_gate25_physical_boundary_root_order_frontier_cert.py"
Q = Fraction


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


def check_structure(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["manifest is not an object"]
    if data.get("schema") != SCHEMA:
        errors.append("manifest schema mismatch")
    if data.get("certificate_sha256") != sha256_path(CERTIFICATE):
        errors.append("certificate hash mismatch")
    if data.get("verifier_sha256") != sha256_path(Path(__file__)):
        errors.append("verifier hash mismatch")
    if data.get("dependencies") != certificate.DEPENDENCIES:
        errors.append("dependency ledger mismatch")
    else:
        for name, expected in certificate.DEPENDENCIES.items():
            path = HERE / name
            if not path.is_file() or sha256_path(path) != expected:
                errors.append(f"dependency hash mismatch: {name}")

    result = data.get("result")
    if not isinstance(result, dict):
        return errors + ["result missing"]
    if result.get("schema") != RESULT_SCHEMA:
        errors.append("result schema mismatch")
    if result.get("internal_replay_digest") != result_digest(result):
        errors.append("internal replay digest mismatch")
    if result.get("provenance", {}).get("frozen_dependency_sha256") != (
        certificate.DEPENDENCIES
    ):
        errors.append("result dependency binding mismatch")
    provenance = result.get("provenance", {})
    if provenance.get("uniform_tau_strict_upper_contract") != {
        "explicit_SYZ_horizon": "(t,phi)=(3,1/512)",
        "every_open_length_3_segment_hits_strictly": True,
        "physical_first_flight": "tau<3",
    }:
        errors.append("uniform tau<3 contract mismatch")
    if provenance.get("canonical_invariant_cone_contract") != (
        "25/9<V=dphi/dr<4108425/145348<29"
    ):
        errors.append("canonical invariant-cone contract mismatch")

    separation = result.get("global_disk_separation", {})
    expected_separation = {
        "same_G_squared_center_minus_radius_sum_margin": "301/625",
        "same_W_squared_center_minus_radius_sum_margin": "561/625",
        "cross_colour_squared_center_minus_radius_sum_margin": "36337/160000",
        "global_strict_squared_separation_margin": "36337/160000",
        "distinct_lifted_closed_disks_are_pairwise_disjoint": True,
        "equal_positive_ray_root_for_two_distinct_targets_is_impossible": True,
        "zero_ray_root_for_a_distinct_target_is_impossible": True,
    }
    for key, expected in expected_separation.items():
        if separation.get(key) != expected:
            errors.append(f"separation mismatch: {key}")

    grammar = result.get("physical_branch_slope_and_root_grammar", {})
    expected_grammar = {
        "canonical_unstable_slope_strict_lower": "25/9",
        "stable_branch_slope_strict_upper": "-25/9",
        "stable_unstable_transversality_gap_strict_lower": "50/9",
        "branch_type_count": 7,
        "every_active_branch_has_at_most_one_isolated_root": True,
        "simultaneous_branch_roots_are_coalesced_into_one_geometric_cut": True,
        "roots_admit_weak_total_order_by_source_r": True,
        "curve_by_curve_numeric_root_sequence_materialized": False,
    }
    for key, expected in expected_grammar.items():
        if grammar.get(key) != expected:
            errors.append(f"root grammar mismatch: {key}")
    types = grammar.get("branch_types", [])
    if not isinstance(types, list) or len(types) != 7:
        errors.append("branch type ledger mismatch")
    elif grammar.get("branch_types_sha256") != digest(types):
        errors.append("branch type digest mismatch")
    else:
        names = {row.get("type") for row in types}
        required = {
            "candidate_signed_tangency",
            "target_endpoint_on_wall_or_target_chart_seam",
            "target_momentum_homogeneity_face",
            "forward_integer_corner_ray",
            "coordinate_velocity_zero",
            "source_endpoint_on_wall_or_source_chart_seam",
            "source_momentum_homogeneity_face",
        }
        if names != required:
            errors.append("branch type names mismatch")
        for row in types:
            if "root" not in str(row.get("root_kind", "")):
                errors.append("branch root typing missing")

    wall = result.get("endpoint_wall_root_lemma", {})
    for key, expected in {
        "gray_radius": "9/25",
        "white_radius": "4/25",
        "white_x_center_distance_to_integer_wall_lower": "199/400",
        "white_y_center_distance_to_integer_wall_lower": "1/2",
        "white_endpoint_never_lies_on_integer_wall": True,
        "one_root_upper_per_each_of_44_endpoint_wall_equalities": True,
    }.items():
        if wall.get(key) != expected:
            errors.append(f"endpoint-wall lemma mismatch: {key}")

    registry = result.get("positive_seeded_component_boundary_reduction", {})
    expected_registry = {
        "positive_seeded_component_count": 24,
        "raw_overledger_histogram": {"394": 12, "402": 12},
        "physical_boundary_root_upper_histogram": {"285": 12, "289": 12},
        "intersection_component_upper_histogram": {"286": 12, "290": 12},
        "uniform_component_local_unnormalized_characteristic_Z_multiplier_upper": "580000/1999",
        "selected_homoclinic_component_id": certificate.SELECTED_COMPONENT_ID,
        "selected_component_intersection_component_upper": 290,
        "selected_component_unnormalized_characteristic_Z_multiplier_upper": "580000/1999",
    }
    for key, expected in expected_registry.items():
        if registry.get(key) != expected:
            errors.append(f"reduction registry mismatch: {key}")
    ids = registry.get("seeded_maximal_component_ids", [])
    if not isinstance(ids, list) or len(ids) != 24 or len(set(ids)) != 24:
        errors.append("component id registry mismatch")
    elif registry.get("seeded_maximal_component_ids_sha256") != digest(ids):
        errors.append("component id digest mismatch")
    classes = registry.get("source_class_records", [])
    if not isinstance(classes, list) or len(classes) != 2:
        errors.append("source-class records missing")
    elif registry.get("source_class_records_sha256") != digest(classes):
        errors.append("source-class digest mismatch")
    else:
        for record in classes:
            source = record.get("source_obstacle")
            row = record.get("common_physical_reduction", {})
            candidates = 57 if source == "G" else 55
            if source not in {"G", "W"} or record.get("seeded_component_count") != 12:
                errors.append("source-class multiplicity mismatch")
            expected_root = 2 * candidates + 167 + 8
            expected_components = expected_root + 1
            if row.get("raw_owner_predicate_count") != 4 * candidates - 1:
                errors.append("raw owner arithmetic mismatch")
            inactive = row.get(
                "raw_owner_predicates_physically_inactive_on_exact_first_owner_boundary",
                {},
            )
            if inactive.get("total") != 3 * candidates - 1:
                errors.append("inactive owner arithmetic mismatch")
            if row.get("physical_signed_tangency_branch_upper") != 2 * candidates:
                errors.append("signed tangency count mismatch")
            frozen = row.get("frozen_word_chart_homogeneity_grammar", {})
            expected_frozen = {
                "endpoint_on_integer_wall": 44,
                "vertical_horizontal_wall_time_tie": 121,
                "coordinate_velocity_zero": 2,
                "transparent_word_total": 167,
                "source_chart_seams": 2,
                "target_chart_seams": 2,
                "source_target_central_homogeneity_faces": 4,
                "roof_two_oriented_wall_chart_in_word_grammar": True,
            }
            if frozen != expected_frozen:
                errors.append("frozen word/chart grammar mismatch")
            if row.get("frozen_word_chart_homogeneity_grammar_sha256") != digest(frozen):
                errors.append("frozen word/chart grammar digest mismatch")
            if row.get("distinct_physical_boundary_root_upper_per_canonical_curve") != expected_root:
                errors.append("physical root upper mismatch")
            if row.get("intersection_component_upper_per_canonical_curve") != expected_components:
                errors.append("component upper mismatch")
            expected_z = Q(expected_components) * Q(2000, 1999)
            if row.get("component_local_unnormalized_characteristic_Z_multiplier_upper") != str(expected_z):
                errors.append("component-local Z arithmetic mismatch")
            if row.get("restriction_then_physical_step_is_a_contraction") is not False:
                errors.append("false contraction promotion")
            try:
                combined = Q(row["restriction_then_physical_step_coefficient_upper"])
                if combined <= 1:
                    errors.append("combined coefficient unexpectedly contracts")
            except Exception:
                errors.append("combined coefficient malformed")

    scope = result.get("strict_scope_boundary", {})
    expected_scope = {
        "physical_reduction_of_394_402_raw_overledger": "CERTIFIED",
        "uniform_isolated_root_and_weak_order_theorem": "CERTIFIED",
        "finite_component_local_unnormalized_characteristic_Z_on_24_seeded_components": "CERTIFIED",
        "curve_by_curve_numeric_root_sequence": "NOT_MATERIALIZED",
        "exact_active_boundary_count_on_each_seeded_component": "NOT_CERTIFIED",
        "full_key_all_component_characteristic_Z": "NOT_CERTIFIED",
        "pre_restriction_Xi_promoted_to_full_key_field_7": False,
        "complete_18_field_operator_block_count": 0,
        "stable_saturated_product_base": False,
        "PPE": False,
        "Gate2": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
    }
    for key, expected in expected_scope.items():
        if scope.get(key) != expected:
            errors.append(f"scope mismatch: {key}")

    expected_verdict = {
        "physical_394_402_overledger_reduction": "CERTIFIED",
        "24_seeded_component_local_finite_Z": "CERTIFIED",
        "full_key_field7_and_contraction": "NOT_CERTIFIED",
        "Gate2": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
    }
    if data.get("verdict") != expected_verdict:
        errors.append("top-level verdict mismatch")
    return errors


def refresh_digest(data: dict[str, Any]) -> None:
    data["result"]["internal_replay_digest"] = result_digest(data["result"])


def self_test(data: dict[str, Any]) -> tuple[int, int]:
    mutations: list[dict[str, Any]] = []

    def mutate(path: tuple[Any, ...], value: Any) -> None:
        candidate = copy.deepcopy(data)
        node: Any = candidate
        for part in path[:-1]:
            node = node[part]
        node[path[-1]] = value
        if path[0] == "result":
            refresh_digest(candidate)
        mutations.append(candidate)

    mutate(("result", "global_disk_separation", "global_strict_squared_separation_margin"), "0")
    mutate(("result", "global_disk_separation", "equal_positive_ray_root_for_two_distinct_targets_is_impossible"), False)
    mutate(("result", "provenance", "uniform_tau_strict_upper_contract", "physical_first_flight"), "tau<=3")
    mutate(("result", "provenance", "canonical_invariant_cone_contract"), "V>0")
    mutate(("result", "physical_branch_slope_and_root_grammar", "canonical_unstable_slope_strict_lower"), "0")
    mutate(("result", "physical_branch_slope_and_root_grammar", "stable_branch_slope_strict_upper"), "1")
    mutate(("result", "physical_branch_slope_and_root_grammar", "stable_unstable_transversality_gap_strict_lower"), "0")
    mutate(("result", "physical_branch_slope_and_root_grammar", "every_active_branch_has_at_most_one_isolated_root"), False)
    mutate(("result", "physical_branch_slope_and_root_grammar", "roots_admit_weak_total_order_by_source_r"), False)
    mutate(("result", "physical_branch_slope_and_root_grammar", "curve_by_curve_numeric_root_sequence_materialized"), True)
    mutate(("result", "physical_branch_slope_and_root_grammar", "branch_types", 0, "source_slope"), "positive")
    mutate(("result", "endpoint_wall_root_lemma", "white_endpoint_never_lies_on_integer_wall"), False)
    mutate(("result", "endpoint_wall_root_lemma", "one_root_upper_per_each_of_44_endpoint_wall_equalities"), False)
    mutate(("result", "positive_seeded_component_boundary_reduction", "raw_overledger_histogram"), {"394": 24})
    mutate(("result", "positive_seeded_component_boundary_reduction", "physical_boundary_root_upper_histogram"), {"1": 24})
    mutate(("result", "positive_seeded_component_boundary_reduction", "selected_component_intersection_component_upper"), 1)
    mutate(("result", "positive_seeded_component_boundary_reduction", "uniform_component_local_unnormalized_characteristic_Z_multiplier_upper"), "1")
    mutate(("result", "positive_seeded_component_boundary_reduction", "source_class_records", 0, "common_physical_reduction", "physical_signed_tangency_branch_upper"), 1)
    mutate(("result", "positive_seeded_component_boundary_reduction", "source_class_records", 0, "common_physical_reduction", "frozen_word_chart_homogeneity_grammar", "transparent_word_total"), 166)
    mutate(("result", "positive_seeded_component_boundary_reduction", "source_class_records", 1, "common_physical_reduction", "frozen_word_chart_homogeneity_grammar", "roof_two_oriented_wall_chart_in_word_grammar"), False)
    mutate(("result", "positive_seeded_component_boundary_reduction", "source_class_records", 0, "common_physical_reduction", "restriction_then_physical_step_is_a_contraction"), True)
    mutate(("result", "strict_scope_boundary", "full_key_all_component_characteristic_Z"), "CERTIFIED")
    mutate(("result", "strict_scope_boundary", "PPE"), True)
    mutate(("result", "strict_scope_boundary", "complete_18_field_operator_block_count"), 1)
    mutate(("result", "strict_scope_boundary", "Gate2"), "CERTIFIED")
    mutate(("verdict", "Gate5"), "CERTIFIED")
    rejected = sum(bool(check_structure(candidate)) for candidate in mutations)
    return rejected, len(mutations)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"MANIFEST_READ_ERROR: {exc}", file=sys.stderr)
        return 1
    errors = check_structure(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    if args.replay and certificate.build_result() != data["result"]:
        print("ERROR: full replay mismatch", file=sys.stderr)
        return 1
    if args.self_test:
        rejected, total = self_test(data)
        if rejected != total:
            print(f"SELF_TEST: FAIL ({rejected}/{total})", file=sys.stderr)
            return 1
        print(f"SELF_TEST: PASS ({rejected}/{total} mutations rejected)")
        return 0
    if args.replay or args.integrity_only:
        print("REPLAY_AND_INTEGRITY: PASS")
        return 0
    print("GATE25_PHYSICAL_394_402_OVERLEDGER_REDUCTION: CERTIFIED")
    print("GATE25_24_SEEDED_COMPONENT_LOCAL_FINITE_Z: CERTIFIED")
    print("GATE25_FULL_KEY_FIELD7_AND_CONTRACTION: NOT_CERTIFIED")
    print("GATE2: NOT_CERTIFIED")
    print("GATE5: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
