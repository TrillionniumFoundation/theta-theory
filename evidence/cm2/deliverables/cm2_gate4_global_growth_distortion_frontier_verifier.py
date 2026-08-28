#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-4 global growth/distortion frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import cm2_gate4_global_growth_distortion_frontier_cert as cert


SCHEMA = "cm2.gate4.global-growth-distortion-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate4.global-growth-distortion-frontier.v1"
HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = (
    HERE / "cm2-gate4-global-growth-distortion-frontier-manifest-2026-07-16.json"
)
CERTIFICATE = HERE / "cm2_gate4_global_growth_distortion_frontier_cert.py"


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_structure(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["manifest is not an object"]
    if data.get("schema") != SCHEMA:
        errors.append("schema mismatch")
    if data.get("certificate_sha256") != sha256_path(CERTIFICATE):
        errors.append("certificate hash mismatch")
    if data.get("verifier_sha256") != sha256_path(Path(__file__)):
        errors.append("verifier hash mismatch")
    dependencies = data.get("dependencies")
    if not isinstance(dependencies, dict) or len(dependencies) != 6:
        errors.append("dependency ledger mismatch")
    else:
        for name, expected in dependencies.items():
            path = HERE / name
            if not path.is_file():
                errors.append(f"missing dependency: {name}")
            elif sha256_path(path) != expected:
                errors.append(f"dependency hash mismatch: {name}")

    try:
        result = cert.certify()
    except Exception as exc:
        return errors + [f"certificate replay failed: {type(exc).__name__}: {exc}"]
    if result.get("schema") != RESULT_SCHEMA:
        errors.append("result schema mismatch")
    if data.get("result_sha256") != cert.canonical_digest(result):
        errors.append("result digest mismatch")

    complexity = result.get("true_singularity_complexity", {})
    universe = complexity.get("finite_horizon_target_registry", {})
    derivative = result.get("all_branch_birkhoff_second_derivatives", {})
    distortion = result.get("homogeneous_oriented_carrier_log_distortion", {})
    frontier = result.get("exact_growth_frontier", {})
    limits = result.get("scope_limits", {})

    expected_universe = {
        "chart_target_pairs": 1296,
        "retained_chart_target_pairs": 448,
        "global_gray_target_union": 76,
        "global_white_target_union": 68,
        "signed_tangency_sheets_gray_source": 152,
        "signed_tangency_sheets_white_source": 136,
        "global_signed_tangency_sheets": 288,
    }
    for key, expected in expected_universe.items():
        if universe.get(key) != expected:
            errors.append(f"target-universe mismatch: {key}")
    expected_complexity = {
        "one_step_true_singularity_intersection_upper": 152,
        "one_step_true_continuity_component_upper": 153,
        "n_step_true_component_crude_upper": "153^n",
        "one_true_branch_homogeneity_cut_sum_strict_upper": "900337/901685",
        "crude_global_one_step_Xi_upper": "137751561/901685",
        "crude_bound_is_a_contraction": False,
        "numeric_true_branch_complexity_leaf": "CERTIFIED",
        "numeric_global_Growth_contraction": "NOT_CERTIFIED",
    }
    for key, expected in expected_complexity.items():
        if complexity.get(key) != expected:
            errors.append(f"complexity mismatch: {key}")
    transversality = complexity.get("sheet_curve_transversality", {})
    if transversality.get(
        "one_unstable_graph_intersects_one_signed_sheet_at_most_once"
    ) is not True:
        errors.append("sheet transversality guard missing")

    d2 = derivative.get("coordinate_second_derivative_envelope", {})
    expected_d2 = {
        "r_differentiated_entries": "<18493/c_1^3",
        "phi_differentiated_entries": "<2843/c_1^3",
        "D2T_coordinate_infinity_operator": "<42672/c_1^3",
    }
    if d2 != expected_d2:
        errors.append("D2T envelope mismatch")
    if derivative.get("matrix_r_derivative_coefficients") != [
        "10795/4", "411", "295875/16", "11315/4"
    ]:
        errors.append("r-differentiated matrix ledger mismatch")
    if derivative.get("matrix_phi_derivative_coefficients") != [
        "1659/4", "63", "45475/16", "1735/4"
    ]:
        errors.append("phi-differentiated matrix ledger mismatch")
    if derivative.get("all_physical_branch_D2T_grazing_weight_leaf") != "CERTIFIED":
        errors.append("all-branch D2T verdict mismatch")

    expected_distortion = {
        "r_jacobian_numerator_strict_lower": "36337/144000",
        "log_r_jacobian_derivative_exact_coefficient_upper": "388021610/5191",
        "all_128_oriented_carrier_log_r_jacobian_distortion_leaf": "CERTIFIED",
        "arbitrary_iterated_standard_curve_distortion_leaf": "NOT_CERTIFIED",
    }
    for key, expected in expected_distortion.items():
        if distortion.get(key) != expected:
            errors.append(f"distortion mismatch: {key}")
    if distortion.get("high_strip_geometry", {}).get(
        "uniform_one_third_log_distortion_constant"
    ) != "1024000":
        errors.append("high-strip distortion constant mismatch")
    if distortion.get("central_strip_geometry", {}).get(
        "one_third_log_distortion_constant"
    ) != "6000000000000":
        errors.append("central-strip distortion constant mismatch")

    if len(frontier.get("new_numeric_leaves", [])) != 4:
        errors.append("new-leaf ledger mismatch")
    if len(frontier.get("minimal_missing_growth_leaves", [])) != 4:
        errors.append("missing-leaf ledger mismatch")
    for key in (
        "numeric_global_theta_star",
        "numeric_delta_n",
        "numeric_C_p_vartheta_p",
        "complete_numeric_C_fw_C_rev_q",
        "gate4_certified",
    ):
        if frontier.get(key) is not False:
            errors.append(f"frontier overclaim: {key}")

    for key in (
        "numeric_true_singularity_complexity",
        "numeric_all_physical_branch_D2T_weight",
        "numeric_all_oriented_carrier_one_step_log_r_jacobian_distortion",
    ):
        if limits.get(key) is not True:
            errors.append(f"certified scope missing: {key}")
    for key in (
        "numeric_arbitrary_iterated_standard_curve_distortion",
        "numeric_delta_n",
        "numeric_global_Growth_contraction",
        "numeric_C_p_vartheta_p",
        "complete_numeric_C_fw_C_rev_q",
        "gate4_certified",
    ):
        if limits.get(key) is not False:
            errors.append(f"fail-closed scope mismatch: {key}")

    # Independent exact arithmetic guards.
    q = Fraction(900337, 901685)
    if 153 * q != Fraction(137751561, 901685) or not 153 * q > 1:
        errors.append("global crude Xi arithmetic failed")
    a0 = 2 * Fraction(25, 9) * Fraction(36337, 800000)
    if a0 != Fraction(36337, 144000):
        errors.append("r-Jacobian numerator arithmetic failed")
    c_log = Fraction(18683) / a0 + 710
    if c_log != Fraction(388021610, 5191) or not c_log < 74750:
        errors.append("log-Jacobian coefficient arithmetic failed")
    if 2 * 18493 + 2 * 2843 != 42672:
        errors.append("D2T operator arithmetic failed")

    summary = data.get("replay_summary", {})
    expected_summary = {
        "horizon_leaf_boxes": 35024,
        "oriented_views": 128,
        "retained_chart_target_pairs": 448,
        "true_singularity_intersection_upper": 152,
        "true_continuity_component_upper": 153,
        "crude_global_one_step_Xi_upper": "137751561/901685",
        "D2T_coordinate_infinity_operator": "<42672/c_1^3",
        "oriented_carrier_distortion_constant": "6000000000000",
        "numeric_global_Growth_contraction": False,
        "gate4_certified": False,
    }
    if summary != expected_summary:
        errors.append("replay summary mismatch")

    expected_verdict = {
        "numeric_true_singularity_complexity": "CERTIFIED",
        "numeric_all_physical_branch_D2T_weight": "CERTIFIED",
        "numeric_oriented_carrier_one_step_log_r_jacobian_distortion": "CERTIFIED",
        "numeric_global_Growth_contraction": "NOT_CERTIFIED",
        "numeric_C_p_vartheta_p_and_q": "NOT_CERTIFIED",
        "gate4": "NOT_CERTIFIED",
    }
    if data.get("verdict") != expected_verdict:
        errors.append("verdict mismatch")
    return errors


def mutation_self_test(baseline: dict[str, Any]) -> list[str]:
    cases: list[tuple[str, Any]] = []

    def add(name: str, mutate: Any) -> None:
        candidate = copy.deepcopy(baseline)
        mutate(candidate)
        cases.append((name, candidate))

    add("schema", lambda d: d.__setitem__("schema", "mutated"))
    add("certificate_hash", lambda d: d.__setitem__("certificate_sha256", "0" * 64))
    add("verifier_hash", lambda d: d.__setitem__("verifier_sha256", "0" * 64))
    add(
        "dependency_hash",
        lambda d: d["dependencies"].__setitem__(next(iter(d["dependencies"])), "0" * 64),
    )
    add("result_digest", lambda d: d.__setitem__("result_sha256", "0" * 64))
    add(
        "complexity",
        lambda d: d["replay_summary"].__setitem__("true_continuity_component_upper", 1),
    )
    add(
        "D2T",
        lambda d: d["replay_summary"].__setitem__(
            "D2T_coordinate_infinity_operator", "<1"
        ),
    )
    add(
        "growth",
        lambda d: d["replay_summary"].__setitem__(
            "numeric_global_Growth_contraction", True
        ),
    )
    add("verdict", lambda d: d["verdict"].__setitem__("gate4", "CERTIFIED"))
    failures = []
    for name, candidate in cases:
        if not check_structure(candidate):
            failures.append(name)
    return failures


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"MANIFEST_READ: FAIL ({type(exc).__name__}: {exc})")
        raise SystemExit(1)
    errors = check_structure(data)
    if errors:
        for error in errors:
            print(f"VERIFY: FAIL: {error}")
        raise SystemExit(1)
    if args.self_test:
        failures = mutation_self_test(data)
        if failures:
            print("MUTATION_SELF_TEST: FAIL: " + ", ".join(failures))
            raise SystemExit(1)
        print("MUTATION_SELF_TEST: PASS (9/9 mutations rejected)")
        return
    if args.replay or args.integrity_only:
        print("REPLAY_AND_INTEGRITY: PASS")
        return
    print("GATE4_NUMERIC_TRUE_SINGULARITY_COMPLEXITY: CERTIFIED")
    print("GATE4_ALL_PHYSICAL_BRANCH_D2T_WEIGHT: CERTIFIED")
    print("GATE4_ORIENTED_CARRIER_ONE_STEP_LOG_R_JACOBIAN_DISTORTION: CERTIFIED")
    print("GATE4_GLOBAL_GROWTH_CONTRACTION: NOT_CERTIFIED")
    print("GATE4_NUMERIC_C_P_VARTTHETA_P_AND_Q: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")
    raise SystemExit(2)


if __name__ == "__main__":
    main()
