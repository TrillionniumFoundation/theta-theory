#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-2/5 universal template frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import cm2_gate25_universal_operator_endpoint_template_frontier_cert as certificate


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate25.universal-operator-endpoint-template-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate25.universal-operator-endpoint-template-frontier.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate25-universal-operator-endpoint-template-frontier-manifest-2026-07-16.json"
)
CERTIFICATE = HERE / "cm2_gate25_universal_operator_endpoint_template_frontier_cert.py"
EXPECTED_INTERNAL_DIGEST = (
    "bfc40167b61438c7ae5a3bd80e98616a94126bfd16f5ca85320e0b1e7310db39"
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
    if not isinstance(dependencies, dict) or len(dependencies) != 8:
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
    if provenance.get("Gate5_required_field_schema_sha256") != (
        "bc7f3bfd5ff896e5de853cfa6f96327ec21fb983359becb40da9526be98c51a5"
    ):
        errors.append("Gate5 field schema digest mismatch")

    registry = result.get("physical_return_registry_binding", {})
    expected_registry = {
        "candidate_key_universe_size": 441280,
        "certified_nonempty_key_lower_bound": 24,
        "positive_core_count": 24,
        "all_24_cores_central_incoming_and_outgoing": True,
        "all_28_core_local_roof_level_chart_pairs_physical": True,
        "all_52_core_local_split_slots_physical": True,
        "completed_full_key_field_count_on_each_of_24_keys": 1,
        "complete_18_field_block_count": 0,
    }
    for key, expected in expected_registry.items():
        if registry.get(key) != expected:
            errors.append(f"registry field mismatch: {key}")

    templates = result.get("universal_full_collision_branch_templates", {})
    if templates.get("canonical_adapted_length_upper") != "1e-90":
        errors.append("canonical adapted length mismatch")
    if templates.get("canonical_euclidean_length_strict_upper") != (
        "27/5000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
    ):
        errors.append("canonical Euclidean length mismatch")
    if templates.get("inside_componentwise_delta_1") is not True:
        errors.append("delta_1 inclusion mismatch")

    field5 = templates.get("field_5_inverse_Jacobian_seed", {})
    expected_field5 = {
        "central_child_adapted_inverse_strict_upper": "144000/180337",
        "high_strip_rank_k_adapted_inverse_strict_upper": "4/k^2",
        "universal_adapted_inverse_strict_upper": "144000/180337",
        "adapted_to_Euclidean_metric_factor_upper": "3807/20",
        "universal_Euclidean_inverse_Jacobian_strict_upper": "27410400/180337",
        "physical_type": "adapted unstable one-dimensional Jacobian",
        "core_local_seed_on_all_24_positive_cores": True,
        "completed_full_key_roof_level_field": False,
    }
    for key, expected in expected_field5.items():
        if field5.get(key) != expected:
            errors.append(f"field 5 seed mismatch: {key}")

    field6 = templates.get("field_6_log_Jacobian_distortion_seed", {})
    expected_field6 = {
        "all_standard_curve_constant": "15000000000000000000000000",
        "Holder_exponent": "1/3",
        "canonical_curve_log_variation_strict_upper": "3/200000",
        "core_local_seed_on_all_24_positive_cores": True,
        "completed_full_key_roof_level_field": False,
    }
    for key, expected in expected_field6.items():
        if field6.get(key) != expected:
            errors.append(f"field 6 seed mismatch: {key}")

    growth = templates.get("pre_restriction_Growth_template", {})
    for key, expected in {
        "central_multiplicity_upper": 1,
        "high_strip_tail_strict_upper": "1/5",
        "one_step_Xi_strict_upper": "900337/901685",
        "margin": "1348/901685",
        "not_field_7_after_word_restriction": True,
    }.items():
        if growth.get(key) != expected:
            errors.append(f"Growth template mismatch: {key}")

    restriction = result.get("characteristic_restriction_blocker", {})
    for key in (
        "word_domain_boundary_Z_bound",
        "chart_seam_and_owner_boundary_multiplicity_bound",
        "characteristic_restriction_preserves_regular_density_space",
        "characteristic_restriction_preserves_standard_family_cost",
        "Gate5_field_7_one_step_cut_growth_Z_sum_completed",
        "Gate5_fields_14_to_17_completed",
    ):
        if restriction.get(key) is not False:
            errors.append(f"restriction blocker overtyped: {key}")

    endpoint = result.get("selected_common_fiber_endpoint_seed", {})
    if endpoint.get("selected_loop_numeric_matrix_seed") is not True:
        errors.append("selected loop matrix seed missing")
    if endpoint.get("selected_loop_twisting_seed") is not True:
        errors.append("selected loop twisting seed missing")
    wedges = endpoint.get("four_nonzero_QNL_eigen_axis_wedges")
    if not isinstance(wedges, dict) or len(wedges) != 4:
        errors.append("selected wedge ledger mismatch")
    for key in (
        "physical_quotient_branch_label_a",
        "pointwise_endpoint_slope_identity",
        "same_carrier_endpoint_maps_X_Y",
        "endpoint_denominator_lower_bound",
        "Gate2_fields_9_to_12_completed",
    ):
        if endpoint.get(key) is not False:
            errors.append(f"endpoint packet overtyped: {key}")

    boundary = result.get("strict_completion_boundary", {})
    if boundary.get("two_new_core_local_strong_field_seeds") != [
        "inverse_Jacobian_bound",
        "log_Jacobian_distortion_sum",
    ]:
        errors.append("new local seed list mismatch")
    for key in (
        "maximal_homogeneous_word_domains",
        "physical_homogeneity_subbranch_registry",
        "return_word_characteristic_boundary_Z",
        "stable_saturated_product_base",
        "quotient_rho_reverse_weights",
    ):
        if boundary.get(key) is not False:
            errors.append(f"completion boundary overtyped: {key}")
    if boundary.get("complete_18_field_operator_block_count") != 0:
        errors.append("complete Gate5 block count overtyped")
    if boundary.get("Gate2_completed_physical_field_count") != 0:
        errors.append("Gate2 physical field count overtyped")
    if boundary.get("Gate2") != "NOT_CERTIFIED":
        errors.append("Gate2 verdict mismatch")
    if boundary.get("Gate5") != "NOT_CERTIFIED":
        errors.append("Gate5 verdict mismatch")

    verdict = data.get("verdict", {})
    expected_verdict = {
        "Gate5_core_local_inverse_Jacobian_seed": "CERTIFIED",
        "Gate5_core_local_log_Jacobian_distortion_seed": "CERTIFIED",
        "Gate5_return_word_characteristic_boundary_Z": "NOT_CERTIFIED",
        "Gate2_selected_common_fiber_loop_wedge_seed": "CERTIFIED",
        "Gate2_stable_quotient_endpoint_packet": "NOT_CERTIFIED",
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

    mutate(("result", "physical_return_registry_binding", "certified_nonempty_key_lower_bound"), 25)
    mutate(("result", "physical_return_registry_binding", "complete_18_field_block_count"), 1)
    mutate(("result", "universal_full_collision_branch_templates", "field_5_inverse_Jacobian_seed", "universal_adapted_inverse_strict_upper"), "1")
    mutate(("result", "universal_full_collision_branch_templates", "field_5_inverse_Jacobian_seed", "universal_Euclidean_inverse_Jacobian_strict_upper"), "1")
    mutate(("result", "universal_full_collision_branch_templates", "field_5_inverse_Jacobian_seed", "completed_full_key_roof_level_field"), True)
    mutate(("result", "universal_full_collision_branch_templates", "field_6_log_Jacobian_distortion_seed", "canonical_curve_log_variation_strict_upper"), "1/100")
    mutate(("result", "universal_full_collision_branch_templates", "field_6_log_Jacobian_distortion_seed", "completed_full_key_roof_level_field"), True)
    mutate(("result", "universal_full_collision_branch_templates", "pre_restriction_Growth_template", "one_step_Xi_strict_upper"), "1")
    mutate(("result", "universal_full_collision_branch_templates", "pre_restriction_Growth_template", "not_field_7_after_word_restriction"), False)
    mutate(("result", "characteristic_restriction_blocker", "word_domain_boundary_Z_bound"), True)
    mutate(("result", "characteristic_restriction_blocker", "Gate5_field_7_one_step_cut_growth_Z_sum_completed"), True)
    mutate(("result", "selected_common_fiber_endpoint_seed", "pointwise_endpoint_slope_identity"), True)
    mutate(("result", "selected_common_fiber_endpoint_seed", "Gate2_fields_9_to_12_completed"), True)
    mutate(("result", "strict_completion_boundary", "stable_saturated_product_base"), True)
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
        replayed = certificate.build_result()
        if replayed != data["result"]:
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

    print("GATE5_TWO_CORE_LOCAL_STRONG_FIELD_SEEDS: CERTIFIED")
    print("GATE5_RETURN_WORD_CHARACTERISTIC_BOUNDARY_Z: NOT_CERTIFIED")
    print("GATE2_SELECTED_COMMON_FIBER_LOOP_WEDGE_SEED: CERTIFIED")
    print("GATE2_STABLE_QUOTIENT_ENDPOINT_PACKET: NOT_CERTIFIED")
    print("GATE2: NOT_CERTIFIED")
    print("GATE5: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
