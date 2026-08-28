#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-2/5 maximal-word/Z frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import cm2_gate25_maximal_word_characteristic_frontier_cert as certificate


HERE = Path(__file__).resolve().parent
Q = Fraction
SCHEMA = "cm2.gate25.maximal-word-characteristic-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate25.maximal-word-characteristic-frontier.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate25-maximal-word-characteristic-frontier-manifest-2026-07-16.json"
)
CERTIFICATE = HERE / "cm2_gate25_maximal_word_characteristic_frontier_cert.py"
EXPECTED_INTERNAL_DIGEST = (
    "14b171309b23e38a42cf6eccfb3005ba5c3f682b6735eb514ed133180c70f430"
)


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


def check_structure(data: Any, *, frozen_digest: bool = True) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["manifest is not an object"]
    if data.get("schema") != SCHEMA:
        errors.append("manifest schema mismatch")
    if data.get("certificate_sha256") != sha256_path(CERTIFICATE):
        errors.append("certificate hash mismatch")
    if data.get("verifier_sha256") != sha256_path(Path(__file__)):
        errors.append("verifier hash mismatch")

    dependencies = data.get("dependencies")
    if not isinstance(dependencies, dict) or len(dependencies) != 9:
        errors.append("dependency ledger mismatch")
    else:
        for name, expected in dependencies.items():
            path = HERE / name
            if not path.is_file():
                errors.append(f"missing dependency: {name}")
            elif sha256_path(path) != expected:
                errors.append(f"dependency hash mismatch: {name}")

    result = data.get("result")
    if not isinstance(result, dict):
        return errors + ["result missing"]
    if result.get("schema") != RESULT_SCHEMA:
        errors.append("result schema mismatch")
    if result.get("internal_replay_digest") != result_digest(result):
        errors.append("internal replay digest mismatch")
    if frozen_digest and result.get("internal_replay_digest") != EXPECTED_INTERNAL_DIGEST:
        errors.append("frozen replay digest mismatch")

    provenance = result.get("provenance", {})
    if provenance.get("frozen_dependency_sha256") != dependencies:
        errors.append("result dependency binding mismatch")
    if provenance.get("parameter_window") != ["-1/400", "1/400"]:
        errors.append("parameter window mismatch")
    if provenance.get("required_operator_field_schema_sha256") != (
        "bc7f3bfd5ff896e5de853cfa6f96327ec21fb983359becb40da9526be98c51a5"
    ):
        errors.append("operator schema digest mismatch")

    registry = result.get("seeded_implicit_maximal_component_registry", {})
    for key, expected in {
        "candidate_key_universe_size": 441280,
        "positive_distinct_key_count": 24,
        "seeded_maximal_component_count": 24,
        "roof_histogram": {"1": 20, "2": 4},
        "positive_collision_SRB_mass_strict_lower": "147/550000",
        "maximality_is_set_theoretic_connected_component_of_exact_predicate": True,
        "boundary_predicate_families_are_frozen": True,
        "boundary_root_order_and_intersection_multiplicity_resolved": False,
    }.items():
        if registry.get(key) != expected:
            errors.append(f"maximal registry mismatch: {key}")
    rows = registry.get("rows")
    if not isinstance(rows, list) or len(rows) != 24:
        errors.append("maximal component row count mismatch")
        rows = []
    if registry.get("rows_sha256") != digest(rows):
        errors.append("maximal component row digest mismatch")
    ids = [row.get("maximal_component_id") for row in rows if isinstance(row, dict)]
    if len(set(ids)) != 24:
        errors.append("maximal component IDs are not distinct")
    candidate_histogram: dict[int, int] = {}
    predicate_histogram: dict[int, int] = {}
    for row in rows:
        boundary = row.get("boundary_predicate_ledger", {})
        candidate_count = boundary.get("candidate_target_count")
        predicate_count = boundary.get("overcomplete_total_predicate_count")
        candidate_histogram[candidate_count] = candidate_histogram.get(candidate_count, 0) + 1
        predicate_histogram[predicate_count] = predicate_histogram.get(predicate_count, 0) + 1
        if boundary.get("predicate_ledger_sha256") != digest(
            {k: v for k, v in boundary.items() if k != "predicate_ledger_sha256"}
        ):
            errors.append("boundary predicate ledger digest mismatch")
        if row.get("component_nonempty_for_every_parameter_fibre") is not True:
            errors.append("seeded maximal component lost nonemptiness")
        if row.get("boundary_roots_on_arbitrary_short_standard_curves_isolated") is not False:
            errors.append("maximal boundary roots overtyped")
    if candidate_histogram != {55: 12, 57: 12}:
        errors.append("candidate-count histogram mismatch")
    if predicate_histogram != {394: 12, 402: 12}:
        errors.append("boundary predicate-count histogram mismatch")

    inner = result.get("positive_inner_core_characteristic_Z", {})
    expected_inner = {
        "registered_inner_core_rectangle_count": 24,
        "source_chart_count": 8,
        "minimum_inter_band_t_gap": "67/100",
        "minimum_inter_band_source_r_gap": "67/625",
        "all_cross_chart_and_within_chart_cyclic_gaps_checked": True,
        "global_pairwise_source_normal_angle_gap_strict_lower": "1/100",
        "global_pairwise_source_r_gap_strict_lower": "1/625",
        "physical_arc_order_ledger_sha256": (
            "dfc328aef242d3086f0c5bc240b2617d0a4251b4e2af1ced3f39bbfe75829244"
        ),
        "short_curve_delta_1": "1/37724355673552103994",
        "intersection_component_multiplicity_upper_per_short_curve": 1,
        "artificial_boundary_endpoint_count_upper_per_nonempty_intersection": 2,
        "invariant_density_ratio_upper": "2000/1999",
        "pre_restriction_Xi_strict_upper": "900337/901685",
        "physical_step_vartheta_p": "360134800/360493663",
        "restriction_then_physical_step_contraction_strict_upper": (
            "720269600000/720626832337"
        ),
        "restriction_then_physical_step_margin": "357232337/720626832337",
        "log_density_regularity_preserved_by_interval_restriction": True,
        "finite_unnormalized_characteristic_Z_on_positive_inner_subfamily": True,
        "normalized_cost_uniform_after_conditioning_on_retained_mass": False,
    }
    for key, expected in expected_inner.items():
        if inner.get(key) != expected:
            errors.append(f"inner characteristic-Z mismatch: {key}")
    try:
        density_ratio = Q(inner["invariant_density_ratio_upper"])
        xi = Q(inner["pre_restriction_Xi_strict_upper"])
        physical = Q(inner["physical_step_vartheta_p"])
        restricted = Q(inner["restriction_then_physical_step_contraction_strict_upper"])
        margin = Q(inner["restriction_then_physical_step_margin"])
        if physical != density_ratio * xi:
            errors.append("physical vartheta arithmetic mismatch")
        if restricted != density_ratio * physical or restricted >= 1:
            errors.append("restricted vartheta arithmetic mismatch")
        if margin != 1 - restricted:
            errors.append("restricted margin arithmetic mismatch")
    except Exception:
        errors.append("characteristic-Z rational arithmetic failed")

    frontier = result.get("full_key_characteristic_frontier", {})
    if frontier.get("maximal_component_boundary_intersection_multiplicity") is not None:
        errors.append("full-key multiplicity overtyped")
    if frontier.get("maximal_component_boundary_Z") is not None:
        errors.append("full-key boundary Z overtyped")
    for key in (
        "pre_restriction_Xi_promoted_to_full_key_field_7",
        "full_key_field_14_regular_density_operator_cost",
        "full_key_field_15_standard_family_operator_cost",
        "full_key_field_16_flux_face_operator_cost",
        "full_key_field_17_dynamic_test_operator_cost",
    ):
        if frontier.get(key) is not False:
            errors.append(f"full-key field overtyped: {key}")

    endpoint = result.get("selected_loop_stable_quotient_endpoint_frontier", {})
    wedges = endpoint.get("selected_four_nonzero_wedges")
    if not isinstance(wedges, dict) or len(wedges) != 4:
        errors.append("selected wedge packet mismatch")
    if endpoint.get("finite_faithful_horseshoe_coding_available") is not True:
        errors.append("faithful horseshoe coding missing")
    for key in (
        "collision_word_or_horseshoe_symbol_is_stable_quotient_branch_label",
        "selected_occurrence_membership_in_one_of_24_maximal_word_components_certified",
        "stable_saturated_product_base",
        "stable_projection_pi_s",
        "quotient_density_rho",
        "onto_inverse_branch_label_a",
        "physical_reverse_weight_p_a",
        "same_carrier_endpoint_maps_X_a_Y_a",
        "pointwise_endpoint_slope_identity",
        "endpoint_denominator_lower_bound",
        "Gate2_fields_9_to_12_completed",
    ):
        if endpoint.get(key) is not False:
            errors.append(f"endpoint packet overtyped: {key}")

    status = result.get("operator_schema_status", {})
    expected_status = {
        "full_key_field_count_completed_on_each_of_24_keys": 1,
        "implicit_maximal_component_ids_materialized_on_positive_subfamily": True,
        "core_local_fields_5_6_templates": True,
        "core_local_characteristic_field_7_seed": True,
        "core_local_fields_14_15_unnormalized_seeds": True,
        "these_core_local_seeds_are_full_key_fields": False,
        "complete_18_field_operator_block_count": 0,
    }
    for key, expected in expected_status.items():
        if status.get(key) != expected:
            errors.append(f"operator schema status mismatch: {key}")

    boundary = result.get("strict_completion_boundary", {})
    expected_boundary = {
        "positive_seeded_maximal_component_registry": "CERTIFIED_IMPLICIT",
        "positive_inner_core_characteristic_multiplicity_and_Z": "CERTIFIED",
        "full_key_characteristic_Z": "NOT_CERTIFIED",
        "full_key_fields_7_and_14_to_17": "NOT_CERTIFIED",
        "stable_quotient_endpoint_packet": "NOT_CERTIFIED",
        "Gate2": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
    }
    for key, expected in expected_boundary.items():
        if boundary.get(key) != expected:
            errors.append(f"strict completion boundary mismatch: {key}")

    verdict = data.get("verdict", {})
    expected_verdict = {
        "positive_seeded_maximal_word_components": "CERTIFIED_IMPLICIT",
        "positive_inner_core_characteristic_Z": "CERTIFIED",
        "full_key_characteristic_Z": "NOT_CERTIFIED",
        "stable_quotient_endpoint_packet": "NOT_CERTIFIED",
        "Gate2": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
    }
    for key, expected in expected_verdict.items():
        if verdict.get(key) != expected:
            errors.append(f"top-level verdict mismatch: {key}")
    return errors


def refresh_result_digest(data: dict[str, Any]) -> None:
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
            refresh_result_digest(candidate)
        mutations.append(candidate)

    mutate(("result", "seeded_implicit_maximal_component_registry", "positive_distinct_key_count"), 25)
    mutate(("result", "seeded_implicit_maximal_component_registry", "positive_collision_SRB_mass_strict_lower"), "1")
    mutate(("result", "seeded_implicit_maximal_component_registry", "boundary_root_order_and_intersection_multiplicity_resolved"), True)
    mutate(("result", "seeded_implicit_maximal_component_registry", "rows", 0, "boundary_roots_on_arbitrary_short_standard_curves_isolated"), True)
    mutate(("result", "seeded_implicit_maximal_component_registry", "rows", 0, "boundary_predicate_ledger", "overcomplete_total_predicate_count"), 1)
    mutate(("result", "positive_inner_core_characteristic_Z", "minimum_inter_band_source_r_gap"), "1/100")
    mutate(("result", "positive_inner_core_characteristic_Z", "global_pairwise_source_r_gap_strict_lower"), "0")
    mutate(("result", "positive_inner_core_characteristic_Z", "intersection_component_multiplicity_upper_per_short_curve"), 2)
    mutate(("result", "positive_inner_core_characteristic_Z", "artificial_boundary_endpoint_count_upper_per_nonempty_intersection"), 4)
    mutate(("result", "positive_inner_core_characteristic_Z", "invariant_density_ratio_upper"), "1")
    mutate(("result", "positive_inner_core_characteristic_Z", "restriction_then_physical_step_contraction_strict_upper"), "1")
    mutate(("result", "positive_inner_core_characteristic_Z", "finite_unnormalized_characteristic_Z_on_positive_inner_subfamily"), False)
    mutate(("result", "positive_inner_core_characteristic_Z", "normalized_cost_uniform_after_conditioning_on_retained_mass"), True)
    mutate(("result", "full_key_characteristic_frontier", "maximal_component_boundary_intersection_multiplicity"), 1)
    mutate(("result", "full_key_characteristic_frontier", "maximal_component_boundary_Z"), "1")
    mutate(("result", "full_key_characteristic_frontier", "pre_restriction_Xi_promoted_to_full_key_field_7"), True)
    mutate(("result", "full_key_characteristic_frontier", "full_key_field_14_regular_density_operator_cost"), True)
    mutate(("result", "selected_loop_stable_quotient_endpoint_frontier", "stable_saturated_product_base"), True)
    mutate(("result", "selected_loop_stable_quotient_endpoint_frontier", "Gate2_fields_9_to_12_completed"), True)
    mutate(("result", "operator_schema_status", "full_key_field_count_completed_on_each_of_24_keys"), 2)
    mutate(("result", "operator_schema_status", "these_core_local_seeds_are_full_key_fields"), True)
    mutate(("result", "operator_schema_status", "complete_18_field_operator_block_count"), 1)
    mutate(("result", "strict_completion_boundary", "Gate2"), "CERTIFIED")
    mutate(("result", "strict_completion_boundary", "Gate5"), "CERTIFIED")
    mutate(("verdict", "Gate2"), "CERTIFIED")
    mutate(("verdict", "Gate5"), "CERTIFIED")

    rejected = sum(bool(check_structure(candidate, frozen_digest=False)) for candidate in mutations)
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

    if args.replay:
        if certificate.build_result() != data["result"]:
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

    print("GATE5_POSITIVE_SEEDED_MAXIMAL_WORD_COMPONENTS: CERTIFIED_IMPLICIT")
    print("GATE5_POSITIVE_INNER_CORE_CHARACTERISTIC_Z: CERTIFIED")
    print("GATE5_FULL_KEY_CHARACTERISTIC_Z: NOT_CERTIFIED")
    print("GATE2_STABLE_QUOTIENT_ENDPOINT_PACKET: NOT_CERTIFIED")
    print("GATE2: NOT_CERTIFIED")
    print("GATE5: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
