#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-2 collision-key quotient frontier."""

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
    HERE / "cm2-gate2-collision-key-stable-quotient-frontier-manifest-2026-07-16.json"
)
CERTIFICATE = HERE / "cm2_gate2_collision_key_stable_quotient_frontier_cert.py"
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


def validate(data: dict[str, Any], *, integrity: bool) -> list[str]:
    errors: list[str] = []
    if data.get("schema") != "cm2.gate2.collision-key-stable-quotient-frontier.manifest.v1":
        errors.append("manifest schema mismatch")
    result = data.get("result")
    if not isinstance(result, dict):
        return errors + ["result missing"]
    if result.get("schema") != "cm2.gate2.collision-key-stable-quotient-frontier.v1":
        errors.append("result schema mismatch")

    path = result.get("full_mass_2d_path_key_schema", {})
    for key, expected in {
        "countable_full_measure_2d_path_key_schema": True,
        "exact_nonempty_path_keys_enumerated": False,
        "homogeneous_connected_return_components_enumerated": False,
        "full_image_stable_quotient_branches_enumerated": False,
        "normalized_source_return_mass": "1 modulo the singular cemetery",
        "path_key_grammar_sha256": "fa64b3d66dfe1b9416419396176f41c796c3da7bd4d32d173c04cb24ba42de6c",
    }.items():
        if path.get(key) != expected:
            errors.append(f"2d path schema mismatch: {key}")
    expected_counts = {
        "1": "441280",
        "2": "194728038400",
        "3": "85929588785152000",
        "4": "37919008939111874560000",
        "5": "16732900264651288005836800000",
        "6": "7383894228785320371215663104000000",
        "7": "3258364845278386173410047814533120000000",
        "8": "1437851238924446250602385899597175193600000000",
        "9": "634494994712579641465820849774241469431808000000000",
    }
    if path.get("fixed_depth_candidate_counts_n_1_to_9") != expected_counts:
        errors.append("candidate path counts mismatch")
    grammar = path.get("path_key_grammar", {})
    if grammar.get("base_alphabet_size") != 441280:
        errors.append("base key count mismatch")
    if grammar.get("base_alphabet_digest") != (
        "841cb96798c9bd41e1440c8b2cdd93af5d80f2f64d693f2aa00175a440045ab9"
    ):
        errors.append("base key digest mismatch")

    dirac = result.get("exact_dirac_refinement_theorem", {})
    for key, expected in {
        "finite_replay_state_count": 97,
        "finite_replay_affine_permutation": "F(i)=37*i+11 mod 97",
        "declared_label_universe_size": 441280,
        "physical_reverse_support_size_at_every_target": 1,
        "physical_reverse_weight_l2_sum_at_every_target": "1",
        "pair_energy_exponent": "1/20",
        "strict_pair_energy_contraction_kappa_lt_1": False,
        "countable_key_refinement_changes_dirac_reverse_kernel": False,
        "randomizing_by_forgetting_the_physical_state_is_stable_quotient": False,
        "genuine_noninvertible_stable_collapse_required": True,
    }.items():
        if dirac.get(key) != expected:
            errors.append(f"Dirac refinement mismatch: {key}")

    mass = result.get("physical_mass_and_registration_ledger", {})
    for key, expected in {
        "collision_SRB_regular_step_key_coverage_fraction": "1 modulo null",
        "q_anchored_2d_return_path_key_coverage_fraction": "1 modulo null",
        "complete_physical_Gate5_operator_block_count": 0,
        "current_two_raw_strips_common_rectangle_fraction_upper": "0.097",
        "unregistered_common_rectangle_fraction_lower": "0.903",
        "stable_quotient_branch_probability_mass": "UNDEFINED_BEFORE_QUOTIENT",
        "endpoint_typed_PPE_probability_mass": "UNDEFINED_BEFORE_ENDPOINT_REGISTRY",
        "Gate5_key_envelope_increases_stable_saturated_registered_mass": False,
        "do_not_replace_undefined_quotient_mass_by_zero": True,
    }.items():
        if mass.get(key) != expected:
            errors.append(f"mass ledger mismatch: {key}")

    frontier = result.get("quotient_reverse_endpoint_stopping_frontier", {})
    if frontier.get("required_field_count") != 17:
        errors.append("required frontier field count mismatch")
    if frontier.get("required_field_schema_sha256") != (
        "72cdcd5a9da5056d90243419b6c6c0b2533ed4fe34d90beda71a49308803c2e8"
    ):
        errors.append("frontier field schema digest mismatch")
    fields = frontier.get("required_fields")
    flags = frontier.get("physical_completion_flags")
    if not isinstance(fields, list) or len(fields) != 17:
        errors.append("required frontier fields missing")
    if not isinstance(flags, dict) or set(flags) != set(fields or []):
        errors.append("completion flag key set mismatch")
    elif any(value is not False for value in flags.values()):
        errors.append("physical frontier field illegally promoted")
    for key, expected in {
        "first_missing_object": "stable_saturated_product_base_Lambda_A",
        "first_reverse_kernel_missing_object": "stable_holonomy_projection_pi_s",
        "first_endpoint_missing_object": "transported_projective_matrix_M_a_in_one_trivialisation",
        "first_native_stopping_missing_object": "inverse_cylinder_diameter_registry",
        "all_fields_share_one_branch_label_registry": False,
    }.items():
        if frontier.get(key) != expected:
            errors.append(f"frontier order mismatch: {key}")

    counter = result.get("exact_no_cardinality_promotion_countermodel", {})
    for key, expected in {
        "label_count": 441280,
        "mass_per_label": "1/441280",
        "total_registered_Borel_mass": "1",
        "reverse_kernel": "delta_x",
        "stable_saturated_product_base_from_labels": False,
        "rho_h_a_p_a_from_labels": False,
        "native_stopping_from_labels": False,
        "PPE_from_full_label_coverage": False,
        "countermodel_sha256": "3f5ad31dc234a324a01450738e1c1fc6f6252685c8f40ab889bb2602effbd342",
    }.items():
        if counter.get(key) != expected:
            errors.append(f"cardinality countermodel mismatch: {key}")

    completion = result.get("completion", {})
    true_keys = (
        "countable_full_measure_2d_first_return_path_key_schema",
        "exact_2d_reverse_kernel_is_dirac",
        "Gate5_key_refinement_preserves_dirac_reverse_kernel",
    )
    false_keys = (
        "stable_saturated_young_rectangle",
        "one_state_full_branch_stable_quotient",
        "stable_quotient_density_rho",
        "physical_reverse_weight_registry",
        "same_carrier_endpoint_typing",
        "actual_native_stopping_antichain",
        "full_countable_pair_energy_drift",
        "physical_PPE",
        "gate2_certified",
    )
    for key in true_keys:
        if completion.get(key) is not True:
            errors.append(f"positive completion mismatch: {key}")
    for key in false_keys:
        if completion.get(key) is not False:
            errors.append(f"fail-closed completion mismatch: {key}")

    expected_verdict = {
        "full_mass_2d_return_path_key_schema": "CERTIFIED",
        "key_refined_2d_reverse_kernel": "DIRAC_NO_CONTRACTION",
        "stable_quotient_reverse_weights_endpoint_native_stopping": "NOT_CERTIFIED",
        "physical_PPE": "NOT_CERTIFIED",
        "gate2": "NOT_CERTIFIED",
    }
    if data.get("verdict") != expected_verdict:
        errors.append("verdict mismatch")

    if integrity:
        if data.get("certificate_sha256") != sha256_path(CERTIFICATE):
            errors.append("certificate SHA mismatch")
        if data.get("verifier_sha256") != sha256_path(VERIFIER):
            errors.append("verifier SHA mismatch")
        dependencies = data.get("dependencies")
        if not isinstance(dependencies, dict):
            errors.append("dependency table missing")
        else:
            for name, expected in dependencies.items():
                dependency = HERE / name
                if not dependency.is_file():
                    errors.append(f"dependency missing: {name}")
                elif sha256_path(dependency) != expected:
                    errors.append(f"dependency SHA mismatch: {name}")
    return errors


def replay(data: dict[str, Any]) -> list[str]:
    try:
        import cm2_gate2_collision_key_stable_quotient_frontier_cert as cert

        actual = cert.certify()
    except Exception as exc:  # pragma: no cover
        return [f"certificate replay raised: {exc}"]
    return [] if actual == data.get("result") else ["certificate replay mismatch"]


def self_test(data: dict[str, Any]) -> list[str]:
    mutations: list[tuple[str, dict[str, Any]]] = []

    bad = copy.deepcopy(data)
    bad["result"]["full_mass_2d_path_key_schema"]["path_key_grammar"][
        "base_alphabet_size"
    ] += 1
    mutations.append(("key-count", bad))

    bad = copy.deepcopy(data)
    bad["result"]["full_mass_2d_path_key_schema"][
        "fixed_depth_candidate_counts_n_1_to_9"
    ]["9"] = "0"
    mutations.append(("path-count", bad))

    bad = copy.deepcopy(data)
    bad["result"]["exact_dirac_refinement_theorem"][
        "physical_reverse_support_size_at_every_target"
    ] = 2
    mutations.append(("Dirac-support", bad))

    bad = copy.deepcopy(data)
    bad["result"]["exact_dirac_refinement_theorem"][
        "strict_pair_energy_contraction_kappa_lt_1"
    ] = True
    mutations.append(("false-contraction", bad))

    bad = copy.deepcopy(data)
    bad["result"]["physical_mass_and_registration_ledger"][
        "stable_quotient_branch_probability_mass"
    ] = "1"
    mutations.append(("undefined-mass-promotion", bad))

    bad = copy.deepcopy(data)
    bad["result"]["quotient_reverse_endpoint_stopping_frontier"][
        "physical_completion_flags"
    ]["stable_holonomy_projection_pi_s"] = True
    mutations.append(("stable-quotient-promotion", bad))

    bad = copy.deepcopy(data)
    bad["result"]["completion"]["actual_native_stopping_antichain"] = True
    mutations.append(("native-stopping-promotion", bad))

    bad = copy.deepcopy(data)
    bad["result"]["completion"]["physical_PPE"] = True
    mutations.append(("PPE-promotion", bad))

    bad = copy.deepcopy(data)
    dependency = sorted(bad["dependencies"])[0]
    bad["dependencies"][dependency] = "0" * 64
    mutations.append(("dependency-SHA", bad))

    failures: list[str] = []
    for label, bad in mutations:
        if not validate(bad, integrity=True):
            failures.append(f"mutation accepted: {label}")
    return failures


def print_status() -> None:
    print("GATE2_FULL_MASS_2D_RETURN_PATH_KEY_SCHEMA: CERTIFIED")
    print("GATE2_KEY_REFINED_2D_REVERSE_KERNEL: DIRAC_NO_CONTRACTION")
    print("GATE2_STABLE_QUOTIENT_REVERSE_WEIGHTS_ENDPOINT_NATIVE_STOPPING: NOT_CERTIFIED")
    print("GATE2_PHYSICAL_PPE: NOT_CERTIFIED")
    print("GATE2: NOT_CERTIFIED")


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
    errors = validate(data, integrity=True)
    if args.replay:
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
