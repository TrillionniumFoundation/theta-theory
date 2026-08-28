#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-2/5 physical return-core registry."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = HERE / "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json"
CERTIFICATE = HERE / "cm2_gate25_physical_return_core_registry_cert.py"
VERIFIER = Path(__file__).resolve()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("manifest root is not an object")
    return value


def validate(data: dict[str, Any], *, check_integrity: bool) -> list[str]:
    errors: list[str] = []
    if data.get("schema") != "cm2.gate25.physical-return-core-registry.manifest.v1":
        errors.append("manifest schema mismatch")
    result = data.get("result")
    if not isinstance(result, dict):
        return errors + ["result missing"]
    if result.get("schema") != "cm2.gate25.physical-return-core-registry.v1":
        errors.append("result schema mismatch")

    registry = result.get("physical_return_core_registry", {})
    expected_registry = {
        "candidate_key_universe_size": 441280,
        "distinct_certified_nonempty_key_lower_bound": 24,
        "physical_compact_homogeneous_core_count": 24,
        "roof_histogram": {"1": 20, "2": 4},
        "registered_roof_level_prefix_suffix_pairs": 28,
        "registered_endpoint_boundary_splits": 52,
        "all_cores_uniform_on_full_parameter_window": True,
        "all_24_keys_members_of_frozen_441280_envelope": True,
        "all_cores_strict_first_hit_against_complete_retained_candidate_list": True,
        "all_wall_records_physically_replayed": True,
        "all_cores_central_incoming_and_outgoing_homogeneity": True,
        "all_cores_have_local_prefix_and_suffix_collision_charts": True,
        "all_24_core_domains_pairwise_disjoint_by_distinct_regular_word_keys": True,
        "mass_lower_bound_sums_only_pairwise_disjoint_core_domains": True,
        "collision_SRB_unnormalized_mass_rational_lower": "273/156250",
        "collision_SRB_normalized_mass_strict_lower_using_pi_lt_22_over_7": "147/550000",
        "rows_sha256": "c3042515b4a244b064f1aaef97ee236c5d3f6078a53fe3fb9e865a1976853b2f",
        "distinct_key_rows_sha256": "aca0fdeb894604f1a96b30d427ef68413def6fc1cded0f99e0d25cd0a84b9d9c",
    }
    for key, expected in expected_registry.items():
        if registry.get(key) != expected:
            errors.append(f"physical registry mismatch: {key}")
    seeds = registry.get("local_seed_bindings_on_each_core", {})
    expected_seeds = {
        "nonempty_or_empty_domain_proof": "CERTIFIED_NONEMPTY",
        "compact_central_homogeneity_core": "CERTIFIED_LOCAL_SUBCORE_ONLY",
        "source_collision_endpoint_chart": "CERTIFIED",
        "target_collision_endpoint_chart": "CERTIFIED_LOCAL_SEMICIRCLE",
        "collision_SRB_area_Jacobian_identity": "CERTIFIED_SEED:1",
        "log_collision_SRB_area_Jacobian_identity": "CERTIFIED_SEED:0",
        "full_collision_branch_Calpha_test_pullback_seed": (
            "CERTIFIED_LOCAL_FULL_RETURN_COST_LT_158"
        ),
    }
    if seeds != expected_seeds:
        errors.append("seven local-seed binding mismatch")
    full_key = registry.get("full_key_schema_field_completion", {})
    expected_full_key = {
        "completed_field_count_on_each_of_24_keys": 1,
        "completed_field": "nonempty_or_empty_domain_proof=NONEMPTY",
        "seven_local_seed_types_are_not_seven_completed_schema_fields": True,
        "physical_homogeneity_subbranch_table_completed": False,
        "all_roof_level_prefix_suffix_charts_completed": False,
        "roof_two_intermediate_transparent_wall_chart_completed": False,
        "area_Jacobian_seed_is_not_unstable_curve_inverse_Jacobian_field": True,
        "log_area_seed_is_not_log_unstable_Jacobian_distortion_field": True,
    }
    if full_key != expected_full_key:
        errors.append("full-key schema-field typing mismatch")

    frontier = result.get("remaining_operator_frontier", {})
    if frontier.get("one_full_key_schema_field_decided_on_each_of_24_keys") is not True:
        errors.append("full-key nonempty field flag missing")
    if frontier.get("seven_typed_local_seed_types_on_each_of_24_cores") is not True:
        errors.append("seven local-seed flag missing")
    for key in (
        "seven_physical_schema_fields_bound_on_each_core",
        "physical_homogeneity_subbranch_table_on_full_key",
        "all_roof_level_prefix_suffix_charts",
        "roof_two_intermediate_transparent_wall_chart_and_costs",
        "global_one_step_cut_growth_Z_sum",
        "face_transversality_C2_coarea_fields",
        "C1_face_trace_and_moving_boundary_DQ",
        "global_regular_density_operator_cost_after_characteristic_restriction",
        "standard_family_operator_cost",
        "flux_face_operator_cost",
        "global_dynamic_test_operator_cost",
        "operator_phase_block",
        "three_CM2_norm_lifts",
        "full_Kac_operator_phase_transfer",
        "gate5_certified",
    ):
        if frontier.get(key) is not False:
            errors.append(f"frontier promotion mismatch: {key}")
    if frontier.get("complete_18_field_physical_operator_block_count") != 0:
        errors.append("complete block count mismatch")
    if frontier.get("exact_total_nonempty_key_count") is not None:
        errors.append("exact total key count overclaimed")

    gate2 = result.get("Gate2_nonpromotion", {})
    if gate2.get("new_positive_collision_SRB_key_mass_lower") != "147/550000":
        errors.append("Gate2 mass typing mismatch")
    if gate2.get("raw_two_strip_common_rectangle_unregistered_fraction_lower") != "0.903":
        errors.append("Gate2 old gap mismatch")
    if gate2.get("key_refined_two_dimensional_reverse_kernel_remains_Dirac") is not True:
        errors.append("Dirac reverse audit missing")
    for key in (
        "stable_saturated_product_base", "stable_projection",
        "quotient_density_rho", "onto_quotient_inverse_branches",
        "physical_reverse_weights", "same_carrier_endpoint_maps",
        "native_stopping_antichain", "PPE", "gate2_certified",
    ):
        if gate2.get(key) is not False:
            errors.append(f"Gate2 illegal promotion: {key}")

    completion = result.get("completion", {})
    for key in (
        "at_least_24_candidate_keys_certified_nonempty",
        "positive_collision_SRB_mass_physical_core_registry",
        "one_full_key_schema_field_decided_on_each_of_24_keys",
        "seven_typed_local_seed_types_on_registered_cores",
    ):
        if completion.get(key) is not True:
            errors.append(f"completion flag missing: {key}")
    for key in (
        "seven_physical_word_schema_fields_bound_on_registered_cores",
        "all_roof_level_prefix_suffix_slots_bound",
        "complete_nonempty_word_domain_decision",
        "complete_18_field_operator_registry", "stable_quotient_or_PPE",
        "gate2_certified", "gate5_certified",
    ):
        if completion.get(key) is not False:
            errors.append(f"completion overclaim: {key}")

    expected_verdict = {
        "physical_nonempty_return_key_lower_bound": "CERTIFIED_AT_LEAST_24",
        "positive_mass_physical_core_registry": "CERTIFIED",
        "complete_18_field_operator_registry": "NOT_CERTIFIED",
        "stable_quotient_PPE": "NOT_CERTIFIED",
        "gate2": "NOT_CERTIFIED",
        "gate5": "NOT_CERTIFIED",
    }
    if data.get("verdict") != expected_verdict:
        errors.append("verdict mismatch")

    if check_integrity:
        if data.get("certificate_sha256") != sha256_path(CERTIFICATE):
            errors.append("certificate SHA mismatch")
        if data.get("verifier_sha256") != sha256_path(VERIFIER):
            errors.append("verifier SHA mismatch")
        dependencies = data.get("dependencies")
        if not isinstance(dependencies, dict):
            errors.append("dependency SHA table missing")
        else:
            for name, expected in dependencies.items():
                path = HERE / name
                if not path.is_file():
                    errors.append(f"dependency missing: {name}")
                elif sha256_path(path) != expected:
                    errors.append(f"dependency SHA mismatch: {name}")
    return errors


def replay(data: dict[str, Any]) -> list[str]:
    try:
        import cm2_gate25_physical_return_core_registry_cert as cert
        actual = cert.certify()
    except Exception as exc:
        return [f"certificate replay raised: {exc}"]
    return [] if actual == data.get("result") else ["certificate replay differs"]


def self_test(data: dict[str, Any]) -> list[str]:
    mutations: list[tuple[str, dict[str, Any]]] = []

    def mutate(name: str, fn) -> None:
        bad = copy.deepcopy(data)
        fn(bad)
        mutations.append((name, bad))

    mutate("key-count", lambda d: d["result"]["physical_return_core_registry"].__setitem__(
        "distinct_certified_nonempty_key_lower_bound", 25))
    mutate("mass", lambda d: d["result"]["physical_return_core_registry"].__setitem__(
        "collision_SRB_normalized_mass_strict_lower_using_pi_lt_22_over_7", "1"))
    mutate("row-digest", lambda d: d["result"]["physical_return_core_registry"].__setitem__(
        "rows_sha256", "0" * 64))
    mutate("wall-replay", lambda d: d["result"]["physical_return_core_registry"].__setitem__(
        "all_wall_records_physically_replayed", False))
    mutate("field-promotion", lambda d: d["result"]["remaining_operator_frontier"].__setitem__(
        "standard_family_operator_cost", True))
    mutate("seven-field-overclaim", lambda d: d["result"]["remaining_operator_frontier"].__setitem__(
        "seven_physical_schema_fields_bound_on_each_core", True))
    mutate("wall-level-overclaim", lambda d: d["result"]["physical_return_core_registry"][
        "full_key_schema_field_completion"].__setitem__(
            "roof_two_intermediate_transparent_wall_chart_completed", True))
    mutate("exact-total", lambda d: d["result"]["remaining_operator_frontier"].__setitem__(
        "exact_total_nonempty_key_count", 24))
    mutate("Gate2-promotion", lambda d: d["result"]["Gate2_nonpromotion"].__setitem__(
        "quotient_density_rho", True))
    mutate("complete-block", lambda d: d["result"]["remaining_operator_frontier"].__setitem__(
        "complete_18_field_physical_operator_block_count", 24))
    mutate("dependency-sha", lambda d: d["dependencies"].__setitem__(
        sorted(d["dependencies"])[0], "f" * 64))

    failures = []
    for name, bad in mutations:
        if not validate(bad, check_integrity=True):
            failures.append(f"mutation accepted: {name}")
    return failures


def print_status() -> None:
    print("GATE5_PHYSICAL_NONEMPTY_RETURN_KEYS_AT_LEAST_24: CERTIFIED")
    print("GATE5_POSITIVE_MASS_PHYSICAL_CORE_REGISTRY: CERTIFIED")
    print("GATE5_SEVEN_LOCAL_SEEDS_ARE_NOT_SEVEN_SCHEMA_FIELDS: CERTIFIED")
    print("GATE5_COMPLETE_18_FIELD_OPERATOR_REGISTRY: NOT_CERTIFIED")
    print("GATE2_STABLE_QUOTIENT_PPE: NOT_CERTIFIED")
    print("GATE5: NOT_CERTIFIED")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        data = load_json(args.manifest)
    except Exception as exc:
        print(f"manifest load failed: {exc}", file=sys.stderr)
        return 1
    errors = validate(data, check_integrity=True)
    if args.replay:
        errors.extend(replay(data))
    if args.self_test:
        errors.extend(self_test(data))
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    if args.replay:
        print("replay: OK")
    if args.self_test:
        print("self-test: 11/11 mutations rejected")
    if args.integrity_only or args.replay or args.self_test:
        return 0
    print_status()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
