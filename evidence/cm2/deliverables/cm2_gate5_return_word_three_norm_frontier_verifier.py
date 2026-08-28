#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-5 return-word/three-norm frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = (
    HERE / "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
)
CERTIFICATE = HERE / "cm2_gate5_return_word_three_norm_frontier_cert.py"
VERIFIER = Path(__file__).resolve()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("manifest root is not an object")
    return value


def validate(data: dict[str, Any], *, check_integrity: bool) -> list[str]:
    errors: list[str] = []
    if data.get("schema") != "cm2.gate5.return-word-three-norm-frontier.manifest.v1":
        errors.append("manifest schema mismatch")

    result = data.get("result")
    if not isinstance(result, dict):
        return errors + ["result missing"]
    if result.get("schema") != "cm2.gate5.return-word-three-norm-frontier.v1":
        errors.append("result schema mismatch")

    grammar = result.get("crossing_grammar", {})
    grammar_expected = {
        "crossing_pattern_count": 985,
        "crossing_pattern_rows_sha256": "2d655b1b83918b0cc42845e465d05f7309657b776f0acbd3d3003e8ae17bb39d",
        "maximum_recorded_crossings_per_axis": 4,
        "straight_flight_monotone_sign_per_axis": True,
        "singular_simultaneous_corner_crossings_sent_to_cemetery": True,
    }
    for key, expected in grammar_expected.items():
        if grammar.get(key) != expected:
            errors.append(f"crossing grammar mismatch: {key}")
    expected_wall_histogram = {
        "0": 1, "1": 4, "2": 12, "3": 28, "4": 60,
        "5": 120, "6": 200, "7": 280, "8": 280,
    }
    if grammar.get("wall_count_histogram") != expected_wall_histogram:
        errors.append("crossing wall histogram mismatch")

    registry = result.get("immutable_candidate_key_registry", {})
    registry_expected = {
        "source_chart_count": 8,
        "conservative_target_lift_count": 162,
        "retained_chart_target_pair_count": 448,
        "certified_empty_chart_target_pair_count": 848,
        "crossing_pattern_count_per_pair": 985,
        "candidate_return_word_key_count": 441280,
        "candidate_word_key_rows_sha256": "841cb96798c9bd41e1440c8b2cdd93af5d80f2f64d693f2aa00175a440045ab9",
        "chart_target_pair_rows_sha256": "ccf4e9e42c7b17f6ebb7f33ec707616bb49ec1d755a817ce141dc92d47056f75",
        "exact_nonempty_candidate_key_count": None,
        "complete_physical_operator_block_count": 0,
    }
    for key, expected in registry_expected.items():
        if registry.get(key) != expected:
            errors.append(f"candidate registry mismatch: {key}")
    expected_roof_histogram = {
        "1": 448,
        "2": 1792,
        "3": 5376,
        "4": 12544,
        "5": 26880,
        "6": 53760,
        "7": 89600,
        "8": 125440,
        "9": 125440,
    }
    if registry.get("roof_histogram") != expected_roof_histogram:
        errors.append("return roof histogram mismatch")
    domain = registry.get("domain_contract", {})
    for key in (
        "regular_domain_partition",
        "all_parameter_fibres_share_one_key_universe",
    ):
        if domain.get(key) is not True:
            errors.append(f"domain contract missing: {key}")
    factor = registry.get("prefix_suffix_factor_contract", {})
    factor_expected = {
        "roof_level_prefix_suffix_factor_pair_count": 3286976,
        "including_endpoint_boundary_split_count": 3728256,
        "symbolic_factorisation_complete_on_every_candidate_key": True,
        "homogeneous_subbranch_index_instantiated": False,
    }
    for key, expected in factor_expected.items():
        if factor.get(key) != expected:
            errors.append(f"factor registry mismatch: {key}")

    fields = result.get("required_operator_field_schema", {})
    required_fields = fields.get("required_fields")
    if not isinstance(required_fields, list) or len(required_fields) != 18:
        errors.append("required operator field list mismatch")
    if fields.get("required_field_count_per_physical_homogeneous_level") != 18:
        errors.append("required field count mismatch")
    if fields.get("required_field_schema_sha256") != (
        "bc7f3bfd5ff896e5de853cfa6f96327ec21fb983359becb40da9526be98c51a5"
    ):
        errors.append("required field schema digest mismatch")
    for key, expected in {
        "word_key_and_symbolic_level_slots_declared": True,
        "homogeneous_subbranch_ids_materialized": False,
        "all_required_fields_populated": False,
        "no_occurrence_level_seed_is_silently_copied_to_all_word_keys": True,
        "first_missing_field": "nonempty_or_empty_domain_proof",
        "first_strong_norm_missing_field": "physical_homogeneity_subbranch_table",
    }.items():
        if fields.get(key) != expected:
            errors.append(f"operator field frontier mismatch: {key}")
    seeds = fields.get("seed_bindings", {})
    if seeds.get("seeds_bound_to_every_return_word_key") is not False:
        errors.append("occurrence seed illegally promoted to every word")
    if seeds.get("C_mesh") != "69986663973833932800":
        errors.append("C_mesh seed mismatch")

    counter = result.get("exact_nonpromotion_countermodels", {})
    for key, expected in {
        "quadratic_last_inverse_speed": "64",
        "fragment_count": 64,
        "curve_cost_amplification": "65/2",
        "component_cycle_gcd": 1,
        "hidden_fibre_operator": "diag(1,-1)",
        "hidden_centered_unit_phase_resonance": "z=-1",
        "finite_word_keys_imply_three_CM2_intertwiners": False,
        "component_gcd_one_implies_operator_Wiener_invertibility": False,
        "countermodel_rows_sha256": "03d529636ee4a8ca7f989d944de7a62b2687154c82870a27e9d2f21fcbbfd79a",
    }.items():
        if counter.get(key) != expected:
            errors.append(f"countermodel mismatch: {key}")

    kac = result.get("Kac_and_phase_frontier", {})
    for key, expected in {
        "finite_Borel_four_term_Kac_algebra_exact": True,
        "singular_Kac_Borel_event_current_TV_upper": "16128/5",
        "height_nine_singular_phase_lift_upper": "290304/5",
        "actual_component_cycle_gcd": 1,
        "regular_two_Kac_terms_typed_in_CM2_spaces": False,
        "return_word_propagated_singular_terms_typed_in_CM2_spaces": False,
        "full_four_term_physical_Kac_CM2_output": False,
        "all_return_word_operator_phase_blocks_registered": False,
        "operator_Wiener_phase_transfer": False,
    }.items():
        if kac.get(key) != expected:
            errors.append(f"Kac/phase frontier mismatch: {key}")

    gate2 = result.get("Gate2_nonpromotion_audit", {})
    for key in (
        "registry_is_stable_saturated_Young_base",
        "stable_holonomy_quotient_constructed",
        "stable_quotient_density_rho_constructed",
        "physical_reverse_kernel_constructed",
        "one_state_full_branch_quotient_constructed",
        "native_stopping_antichain_constructed",
        "candidate_Borel_return_keys_feed_Gate2_one_state_quotient",
        "gate2_certified",
    ):
        if gate2.get(key) is not False:
            errors.append(f"Gate2 nonpromotion mismatch: {key}")
    if gate2.get("unregistered_common_rectangle_fraction_lower") != "0.903":
        errors.append("Gate2 unregistered-mass lower bound mismatch")

    completion = result.get("completion", {})
    true_keys = (
        "complete_regular_return_word_candidate_key_envelope",
        "immutable_candidate_word_key_digest",
        "symbolic_prefix_suffix_factorization_every_roof_level",
        "physical_Borel_TV_Linf_prefix_suffix_constants",
    )
    false_keys = (
        "complete_nonempty_return_word_domain_decisions",
        "physical_homogeneous_subbranch_registry",
        "immutable_complete_return_word_operator_registry",
        "regular_density_prefix_suffix_intertwiner",
        "standard_family_CM2_norm_lift",
        "flux_face_CM2_norm_lift",
        "dynamic_test_CM2_norm_lift",
        "full_four_term_physical_Kac_CM2_output",
        "operator_Wiener_phase_transfer",
        "gate5_certified",
    )
    for key in true_keys:
        if completion.get(key) is not True:
            errors.append(f"certified completion flag mismatch: {key}")
    for key in false_keys:
        if completion.get(key) is not False:
            errors.append(f"fail-closed completion flag mismatch: {key}")

    verdict = data.get("verdict", {})
    expected_verdict = {
        "regular_return_word_candidate_key_envelope": "CERTIFIED",
        "symbolic_prefix_suffix_level_registry": "CERTIFIED",
        "physical_homogeneous_operator_registry": "NOT_CERTIFIED",
        "physical_three_CM2_norm_lifts": "NOT_CERTIFIED",
        "full_Kac_operator_phase_transfer": "NOT_CERTIFIED",
        "gate5": "NOT_CERTIFIED",
    }
    if verdict != expected_verdict:
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
        import cm2_gate5_return_word_three_norm_frontier_cert as cert

        actual = cert.certify()
    except Exception as exc:  # pragma: no cover - fail closed
        return [f"certificate replay raised: {exc}"]
    if actual != data.get("result"):
        return ["certificate replay differs from frozen result"]
    return []


def self_test(data: dict[str, Any]) -> list[str]:
    mutations: list[tuple[str, dict[str, Any]]] = []

    bad = copy.deepcopy(data)
    bad["result"]["immutable_candidate_key_registry"]["candidate_return_word_key_count"] += 1
    mutations.append(("word-count", bad))

    bad = copy.deepcopy(data)
    bad["result"]["immutable_candidate_key_registry"]["candidate_word_key_rows_sha256"] = "0" * 64
    mutations.append(("word-digest", bad))

    bad = copy.deepcopy(data)
    bad["result"]["immutable_candidate_key_registry"]["roof_histogram"]["9"] -= 1
    mutations.append(("roof-histogram", bad))

    bad = copy.deepcopy(data)
    bad["result"]["immutable_candidate_key_registry"]["prefix_suffix_factor_contract"][
        "homogeneous_subbranch_index_instantiated"
    ] = True
    mutations.append(("homogeneous-promotion", bad))

    bad = copy.deepcopy(data)
    bad["result"]["required_operator_field_schema"]["required_fields"].pop()
    mutations.append(("field-deletion", bad))

    bad = copy.deepcopy(data)
    bad["result"]["completion"]["standard_family_CM2_norm_lift"] = True
    mutations.append(("strong-norm-promotion", bad))

    bad = copy.deepcopy(data)
    bad["result"]["Kac_and_phase_frontier"]["operator_Wiener_phase_transfer"] = True
    mutations.append(("operator-phase-promotion", bad))

    bad = copy.deepcopy(data)
    bad["result"]["Gate2_nonpromotion_audit"][
        "candidate_Borel_return_keys_feed_Gate2_one_state_quotient"
    ] = True
    mutations.append(("Gate2-promotion", bad))

    bad = copy.deepcopy(data)
    first_dependency = sorted(bad["dependencies"])[0]
    bad["dependencies"][first_dependency] = "f" * 64
    mutations.append(("dependency-sha", bad))

    failures: list[str] = []
    for name, mutated in mutations:
        if not validate(mutated, check_integrity=True):
            failures.append(f"mutation accepted: {name}")
    if len(mutations) < 6:
        failures.append("fewer than six mutations exercised")
    return failures


def print_status() -> None:
    print("GATE5_COMPLETE_REGULAR_RETURN_WORD_CANDIDATE_KEY_ENVELOPE: CERTIFIED")
    print("GATE5_SYMBOLIC_PREFIX_SUFFIX_LEVEL_REGISTRY: CERTIFIED")
    print("GATE5_PHYSICAL_HOMOGENEOUS_OPERATOR_REGISTRY: NOT_CERTIFIED")
    print("GATE5_THREE_CM2_NORM_INTERTWINERS: NOT_CERTIFIED")
    print("GATE5_FULL_KAC_OPERATOR_PHASE_TRANSFER: NOT_CERTIFIED")
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
        print(f"VERIFY: FAIL ({exc})")
        return 2

    errors = validate(data, check_integrity=True)
    if args.replay and not args.integrity_only:
        errors.extend(replay(data))
    elif args.replay and args.integrity_only:
        # The combined mode used by the assault scripts checks both the frozen
        # chain and a fresh generator replay.
        errors.extend(replay(data))
    if args.self_test:
        errors.extend(self_test(data))

    if errors:
        print("VERIFY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 2

    if args.self_test:
        print("SELF_TEST: PASS (9 mutations rejected)")
        return 0
    if args.replay or args.integrity_only:
        print("VERIFY: PASS")
        return 0

    print_status()
    return 2


if __name__ == "__main__":
    sys.exit(main())
