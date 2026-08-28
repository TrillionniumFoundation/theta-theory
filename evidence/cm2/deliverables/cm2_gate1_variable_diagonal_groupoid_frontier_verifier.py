#!/usr/bin/env python3
"""Fail-closed verifier for the variable-diagonal groupoid frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import cm2_gate1_variable_diagonal_groupoid_frontier_cert as certificate


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate1.variable-diagonal-groupoid-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate1.variable-diagonal-groupoid-frontier.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate1-variable-diagonal-groupoid-frontier-manifest-2026-07-17.json"
)
CERTIFICATE = HERE / "cm2_gate1_variable_diagonal_groupoid_frontier_cert.py"


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
        errors.append("dependencies")
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

    replay = result.get("exact_variable_ratio_replay", {})
    for key in (
        "stable_critical_conjugation_cancels_variable_product_exactly",
        "unstable_critical_conjugation_cancels_variable_product_exactly",
    ):
        if replay.get(key) is not True:
            errors.append(f"ratio replay {key}")
    if replay.get("constant_periodic_ratio_assumption_used") is not False:
        errors.append("constant ratio scope")

    theorem = result.get("one_sided_all_plaque_green_theorems", {})
    normalisation = theorem.get("sinai_one_sided_normalisation", {})
    if normalisation.get("holder_transfer_functions") is not True:
        errors.append("Sinai transfer")
    if normalisation.get("periodic_products_and_pinching_preserved") is not True:
        errors.append("pinching preservation")
    stable = theorem.get("stable_green_gauge", {})
    unstable = theorem.get("unstable_green_gauge", {})
    expected_stable = {
        "opposite_unstable_defect_is_uniformly_contracted": True,
        "all_local_and_global_stable_plaques": "CERTIFIED_THEOREM",
        "both_canonical_families_holder_for_the_lower_shear_representative": True,
        "lower_shear_representative_in_class_H": True,
    }
    expected_unstable = {
        "opposite_stable_defect_is_uniformly_contracted": True,
        "all_local_and_global_unstable_plaques": "CERTIFIED_THEOREM",
        "both_canonical_families_holder_for_the_upper_shear_representative": True,
        "upper_shear_representative_in_class_H": True,
    }
    for key, expected in expected_stable.items():
        if stable.get(key) != expected:
            errors.append(f"stable theorem {key}")
    for key, expected in expected_unstable.items():
        if unstable.get(key) != expected:
            errors.append(f"unstable theorem {key}")
    if theorem.get("former_two_variable_diagonal_linear_groupoid_equations") != "SOLVED_SEPARATELY":
        errors.append("linear groupoid status")

    algebra = result.get("noncommutative_shear_gluing_algebra", {})
    expected_algebra = {
        "upper_then_lower_stable_critical_coordinate_is_clean_du": True,
        "upper_then_lower_unstable_critical_coordinate_has_cross_term": "-v_y du v_x",
        "lower_then_upper_unstable_critical_coordinate_is_clean_dv": True,
        "lower_then_upper_stable_critical_coordinate_has_cross_term": "-u_y u_x dv",
        "sample_upper_then_lower_identity_exact": True,
        "sample_lower_then_upper_identity_exact": True,
        "noncommutative_cross_term_can_be_dropped": False,
    }
    for key, expected in expected_algebra.items():
        if algebra.get(key) != expected:
            errors.append(f"gluing algebra {key}")

    frontier = result.get("nonlinear_third_gauge_compatibility_frontier", {})
    expected_frontier = {
        "third_diagonal_or_nonlinear_correction_may_cancel_cross_term": True,
        "actual_cross_term_limit_computed_on_all_physical_plaques": False,
        "one_same_representative_with_both_green_families": "NOT_CERTIFIED",
        "uniform_all_plaque_class_H_for_the_combined_third_gauge": "NOT_CERTIFIED",
        "selected_nonzero_twisting_in_that_same_family": "NOT_CERTIFIED",
    }
    for key, expected in expected_frontier.items():
        if frontier.get(key) != expected:
            errors.append(f"frontier {key}")

    scope = result.get("strict_scope", {})
    expected_scope = {
        "stable_variable_diagonal_groupoid_equation": "SOLVED_SEPARATELY",
        "unstable_variable_diagonal_groupoid_equation": "SOLVED_SEPARATELY",
        "lower_shear_all_plaque_class_H_representative": "CERTIFIED_THEOREM",
        "upper_shear_all_plaque_class_H_representative": "CERTIFIED_THEOREM",
        "combined_all_plaque_third_gauge": "NOT_CERTIFIED",
        "same_representative_class_H_plus_twisting": "NOT_CERTIFIED",
        "full_mass_physical_PPE": "NOT_CERTIFIED",
        "Gate1": "NOT_CERTIFIED",
    }
    for key, expected in expected_scope.items():
        if scope.get(key) != expected:
            errors.append(f"scope {key}")

    expected_verdict = {
        "stable_variable_diagonal_groupoid_equation": "SOLVED_SEPARATELY",
        "unstable_variable_diagonal_groupoid_equation": "SOLVED_SEPARATELY",
        "combined_all_plaque_third_gauge": "NOT_CERTIFIED",
        "same_representative_class_H_plus_twisting": "NOT_CERTIFIED",
        "Gate1": "NOT_CERTIFIED",
    }
    if manifest.get("verdict") != expected_verdict:
        errors.append("verdict")
    return errors


def refresh(manifest: dict[str, Any]) -> None:
    manifest["result"]["internal_replay_digest"] = result_digest(manifest["result"])


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

    mutate(("result", "exact_variable_ratio_replay", "stable_critical_conjugation_cancels_variable_product_exactly"), False)
    mutate(("result", "exact_variable_ratio_replay", "constant_periodic_ratio_assumption_used"), True)
    mutate(("result", "one_sided_all_plaque_green_theorems", "sinai_one_sided_normalisation", "holder_transfer_functions"), False)
    mutate(("result", "one_sided_all_plaque_green_theorems", "stable_green_gauge", "all_local_and_global_stable_plaques"), "NOT_CERTIFIED")
    mutate(("result", "one_sided_all_plaque_green_theorems", "stable_green_gauge", "lower_shear_representative_in_class_H"), False)
    mutate(("result", "one_sided_all_plaque_green_theorems", "unstable_green_gauge", "upper_shear_representative_in_class_H"), False)
    mutate(("result", "one_sided_all_plaque_green_theorems", "former_two_variable_diagonal_linear_groupoid_equations"), "NOT_SOLVED")
    mutate(("result", "noncommutative_shear_gluing_algebra", "upper_then_lower_unstable_critical_coordinate_has_cross_term"), "0")
    mutate(("result", "noncommutative_shear_gluing_algebra", "noncommutative_cross_term_can_be_dropped"), True)
    mutate(("result", "nonlinear_third_gauge_compatibility_frontier", "actual_cross_term_limit_computed_on_all_physical_plaques"), True)
    mutate(("result", "nonlinear_third_gauge_compatibility_frontier", "uniform_all_plaque_class_H_for_the_combined_third_gauge"), "CERTIFIED")
    mutate(("result", "strict_scope", "combined_all_plaque_third_gauge"), "CERTIFIED")
    mutate(("result", "strict_scope", "Gate1"), "CERTIFIED")
    mutate(("verdict", "Gate1"), "CERTIFIED")
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
    print("VARIABLE_DIAGONAL_STABLE_GREEN_EQUATION: SOLVED_SEPARATELY")
    print("VARIABLE_DIAGONAL_UNSTABLE_GREEN_EQUATION: SOLVED_SEPARATELY")
    print("NONLINEAR_THIRD_GAUGE_GLUING: NOT_CERTIFIED")
    print("GATE1: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
