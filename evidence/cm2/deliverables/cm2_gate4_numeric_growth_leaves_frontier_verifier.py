#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-4 numeric Growth-leaf frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import cm2_gate4_numeric_growth_leaves_frontier_cert as cert


SCHEMA = "cm2.gate4.numeric-growth-leaves-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate4.numeric-growth-leaves-frontier.v1"
HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = (
    HERE / "cm2-gate4-numeric-growth-leaves-frontier-manifest-2026-07-16.json"
)
CERTIFICATE = HERE / "cm2_gate4_numeric_growth_leaves_frontier_cert.py"


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
    if not isinstance(dependencies, dict) or len(dependencies) != 3:
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

    leaves = result.get("adapted_metric_numeric_leaves", {})
    local = result.get("single_true_branch_homogeneity_expansion_sum", {})
    branch = result.get("branch_multiplicity_nonimplication", {})
    distortion = result.get("distortion_nonimplication", {})
    frontier = result.get("exact_growth_dependency_frontier", {})
    limits = result.get("scope_limits", {})
    summary = data.get("replay_summary", {})
    expected_summary = {
        "adapted_expansion": leaves.get("uniform_adapted_expansion_strict_lower"),
        "inverse_contraction": leaves.get(
            "uniform_adapted_inverse_contraction_strict_upper"
        ),
        "c_hat": leaves.get("explicit_c_hat"),
        "Lambda": leaves.get("explicit_Lambda"),
        "C_s": leaves.get("explicit_separation_metric_C_s"),
        "single_branch_cut_sum": local.get(
            "single_true_branch_one_step_cut_sum_strict_upper"
        ),
        "single_branch_margin": local.get("single_true_branch_contraction_margin"),
        "numeric_C_p_vartheta_p": limits.get("numeric_C_p_vartheta_p"),
        "gate4_certified": limits.get("gate4_certified"),
    }
    for key, expected in expected_summary.items():
        if summary.get(key) != expected:
            errors.append(f"summary mismatch: {key}")

    leaf_expected = {
        "uniform_adapted_expansion_strict_lower": "180337/144000",
        "uniform_adapted_inverse_contraction_strict_upper": "144000/180337",
        "safe_common_C_metric": "141/4",
        "carrier_projection_constant_C_cone": "30",
        "explicit_c_hat": "20/3807",
        "explicit_Lambda": "180337/144000",
        "maximum_homogeneous_unstable_curve_length_strict_upper": "68",
        "explicit_separation_metric_C_s": "1296803367/80000",
        "numeric_SYZ_Lemma_6_cone_hyperbolicity_leaf": "CERTIFIED",
        "numeric_C_metric_C_cone_L0_C_s_leaves": "CERTIFIED",
    }
    for key, expected in leaf_expected.items():
        if leaves.get(key) != expected:
            errors.append(f"numeric leaf mismatch: {key}")
    if leaves.get("identity_matches_frozen_Birkhoff_matrix") is not True:
        errors.append("adapted expansion identity guard missing")

    local_expected = {
        "declared_cut_sum_k0": 41,
        "central_component_contraction_upper": "144000/180337",
        "two_sided_tail_upper": "1/5",
        "single_true_branch_one_step_cut_sum_strict_upper": "900337/901685",
        "single_true_branch_contraction_margin": "1348/901685",
        "single_true_branch_one_step_expansion_sum": "CERTIFIED",
        "k0_41_compatibility_with_full_distortion_regular_atlas": False,
        "full_true_singularity_weighted_sum": False,
        "global_Growth_Lemma_contraction": False,
    }
    for key, expected in local_expected.items():
        if local.get(key) != expected:
            errors.append(f"local cut-sum mismatch: {key}")

    if branch.get("pointwise_expansion_determines_weighted_cut_sum") is not False:
        errors.append("branch multiplicity nonimplication lost")
    if branch.get("first_failing_branch_count") != 2:
        errors.append("branch countermodel threshold mismatch")
    if distortion.get("cone_and_first_derivative_bounds_determine_distortion") is not False:
        errors.append("distortion nonimplication lost")
    if distortion.get(
        "existing_carrier_C2_bound_is_not_a_D2F_distortion_bound"
    ) is not True:
        errors.append("carrier/map C2 distinction missing")

    if len(frontier.get("numeric_leaves_now_closed", [])) != 6:
        errors.append("closed-leaf ledger mismatch")
    if len(frontier.get("minimal_undetermined_growth_leaves", [])) != 5:
        errors.append("missing-leaf ledger mismatch")
    for key in (
        "numeric_C_gr_vartheta_gr",
        "numeric_C_p_vartheta_p",
        "numeric_A0_A1",
        "complete_propagated_numeric_C_fw_C_rev_q",
        "gate4_certified",
    ):
        if frontier.get(key) is not False:
            errors.append(f"frontier overclaim: {key}")

    for key in (
        "numeric_adapted_metric_expansion",
        "numeric_metric_equivalence_and_Euclidean_hyperbolicity",
        "numeric_C_metric_C_cone_L0_C_s",
        "numeric_single_true_branch_homogeneity_cut_sum",
    ):
        if limits.get(key) is not True:
            errors.append(f"certified scope missing: {key}")
    for key in (
        "numeric_full_true_singularity_weighted_sum",
        "numeric_n_step_delta_n",
        "numeric_distortion_constants",
        "numeric_C_gr_vartheta_gr",
        "numeric_C_p_vartheta_p",
        "complete_propagated_numeric_C_fw_C_rev_q",
        "gate4_certified",
    ):
        if limits.get(key) is not False:
            errors.append(f"fail-closed scope mismatch: {key}")

    digests = result.get("internal_replay_digests", {})
    if digests.get("branch_countermodel_rows") != branch.get("rows_sha256"):
        errors.append("branch countermodel digest mismatch")
    if digests.get("distortion_countermodel_rows") != distortion.get("rows_sha256"):
        errors.append("distortion countermodel digest mismatch")

    # Independent exact arithmetic guards.
    expansion = 1 + 2 * Fraction(25, 9) * Fraction(36337, 800000)
    if expansion != Fraction(180337, 144000):
        errors.append("adapted expansion arithmetic failed")
    theta = 1 / expansion
    total = theta + Fraction(8, 40)
    if total != Fraction(900337, 901685) or not total < 1:
        errors.append("single-branch cut-sum arithmetic failed")
    if 1 - total != Fraction(1348, 901685):
        errors.append("single-branch margin arithmetic failed")

    verdict = data.get("verdict", {})
    expected_verdict = {
        "numeric_adapted_metric_hyperbolicity_leaves": "CERTIFIED",
        "numeric_single_true_branch_cut_sum": "CERTIFIED",
        "numeric_global_Growth_constants": "NOT_CERTIFIED",
        "numeric_C_p_vartheta_p": "NOT_CERTIFIED",
        "complete_propagated_numeric_C_fw_C_rev_q": "NOT_CERTIFIED",
        "gate4": "NOT_CERTIFIED",
    }
    if verdict != expected_verdict:
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
    add(
        "dependency_hash",
        lambda d: d["dependencies"].__setitem__(next(iter(d["dependencies"])), "0" * 64),
    )
    add("result_digest", lambda d: d.__setitem__("result_sha256", "0" * 64))
    add(
        "expansion",
        lambda d: d["replay_summary"].__setitem__("adapted_expansion", "1"),
    )
    add(
        "cut_sum",
        lambda d: d["replay_summary"].__setitem__("single_branch_cut_sum", "2"),
    )
    add(
        "numeric_Cp",
        lambda d: d["replay_summary"].__setitem__("numeric_C_p_vartheta_p", True),
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
        print("MUTATION_SELF_TEST: PASS (8/8 mutations rejected)")
        return
    if args.replay or args.integrity_only:
        print("REPLAY_AND_INTEGRITY: PASS")
        return
    print("GATE4_NUMERIC_ADAPTED_METRIC_HYPERBOLICITY_LEAVES: CERTIFIED")
    print("GATE4_NUMERIC_SINGLE_TRUE_BRANCH_CUT_SUM: CERTIFIED")
    print("GATE4_NUMERIC_GLOBAL_GROWTH_CONSTANTS: NOT_CERTIFIED")
    print("GATE4_NUMERIC_C_P_VARTTHETA_P_AND_PROPAGATED_Q: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")
    raise SystemExit(2)


if __name__ == "__main__":
    main()
