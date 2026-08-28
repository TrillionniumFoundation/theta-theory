#!/usr/bin/env python3
"""Fail-closed verifier for the biprojective Gate-1 frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import cm2_gate1_biprojective_half_density_frontier_cert as certificate


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate1.biprojective-half-density-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate1.biprojective-half-density-frontier.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate1-biprojective-half-density-frontier-manifest-2026-07-17.json"
)
CERTIFICATE = HERE / "cm2_gate1_biprojective_half_density_frontier_cert.py"


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

    algebra = result.get("exact_biprojective_algebra", {})
    expected_algebra = {
        "D_x_determinant": "1",
        "D_y_determinant": "1",
        "upper_off_diagonal_is_clean_dv": True,
        "lower_off_diagonal_is_clean_du": True,
        "cubic_base_value_cross_terms_present": False,
    }
    for key, expected in expected_algebra.items():
        if algebra.get(key) != expected:
            errors.append(f"algebra {key}")
    if algebra.get("sample_x", {}).get("q") != "9/16":
        errors.append("sample x q")
    if algebra.get("sample_y", {}).get("q") != "4/9":
        errors.append("sample y q")

    reduction = result.get("canonical_limit_reduction", {})
    expected_reduction = {
        "stable_conjugated_relative_limit": "I+c_s(x,y)E_21",
        "unstable_conjugated_relative_limit": "I+c_u(x,y)E_12",
        "combined_class_H_if_all_clauses_hold": True,
    }
    for key, expected in expected_reduction.items():
        if reduction.get(key) != expected:
            errors.append(f"reduction {key}")
    for key in (
        "exact_stable_pair_equation",
        "exact_unstable_pair_equation",
        "iterated_stable_consequence",
        "iterated_unstable_consequence",
        "sufficient_Holder_clause",
    ):
        if not isinstance(reduction.get(key), str) or not reduction[key]:
            errors.append(f"reduction formula {key}")

    comparison = result.get("comparison_with_shear_product", {})
    expected_comparison = {
        "old_unstable_cross_term": "-v_y(u_y-u_x)v_x",
        "new_off_diagonal_cross_term": "0 exactly",
        "new_scalar_terminal_factor": "(q_y q_x)^-1/2",
        "this_is_an_equivalent_nonlinear_compatibility_target_not_a_solution": True,
    }
    for key, expected in expected_comparison.items():
        if comparison.get(key) != expected:
            errors.append(f"comparison {key}")

    scope = result.get("strict_nonpromotion", {})
    for key in (
        "clean_off_diagonals_imply_half_density_equations_solved",
        "formal_sufficient_criterion_implies_actual_physical_solution",
    ):
        if scope.get(key) is not False:
            errors.append(f"nonpromotion {key}")
    for key in (
        "uniform_big_cell_q_lower_bound",
        "coupled_half_density_groupoid_solution",
        "combined_all_plaque_class_H_representative",
        "same_representative_class_H_plus_twisting",
        "Gate1",
    ):
        if scope.get(key) != "NOT_CERTIFIED":
            errors.append(f"scope {key}")

    expected_verdict = {
        "biprojective_off_diagonal_cross_terms": "ELIMINATED_EXACTLY",
        "combined_class_H_sufficient_half_density_criterion": "CERTIFIED",
        "coupled_half_density_groupoid_solution": "NOT_CERTIFIED",
        "same_representative_class_H_plus_twisting": "NOT_CERTIFIED",
        "Gate1": "NOT_CERTIFIED",
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

    mutate(("result", "exact_biprojective_algebra", "D_x_determinant"), "0")
    mutate(("result", "exact_biprojective_algebra", "upper_off_diagonal_is_clean_dv"), False)
    mutate(("result", "exact_biprojective_algebra", "cubic_base_value_cross_terms_present"), True)
    mutate(("result", "exact_biprojective_algebra", "sample_x", "q"), "1")
    mutate(("result", "canonical_limit_reduction", "stable_conjugated_relative_limit"), "diverges")
    mutate(("result", "canonical_limit_reduction", "combined_class_H_if_all_clauses_hold"), False)
    mutate(("result", "comparison_with_shear_product", "new_off_diagonal_cross_term"), "nonzero")
    mutate(("result", "comparison_with_shear_product", "this_is_an_equivalent_nonlinear_compatibility_target_not_a_solution"), False)
    mutate(("result", "strict_nonpromotion", "clean_off_diagonals_imply_half_density_equations_solved"), True)
    mutate(("result", "strict_nonpromotion", "coupled_half_density_groupoid_solution"), "CERTIFIED")
    mutate(("result", "strict_nonpromotion", "combined_all_plaque_class_H_representative"), "CERTIFIED")
    mutate(("result", "strict_nonpromotion", "Gate1"), "CERTIFIED")
    mutate(("verdict", "coupled_half_density_groupoid_solution"), "CERTIFIED")
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
    print("BIPROJECTIVE_OFF_DIAGONAL_CROSS_TERMS: ELIMINATED_EXACTLY")
    print("COUPLED_HALF_DENSITY_GROUPOID_EQUATIONS: NOT_CERTIFIED")
    print("GATE1: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
