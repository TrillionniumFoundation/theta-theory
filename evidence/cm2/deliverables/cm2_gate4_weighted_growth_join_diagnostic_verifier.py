#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-4 weighted Growth join diagnostic."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import cm2_gate4_weighted_growth_join_diagnostic_cert as cert


SCHEMA = "cm2.gate4.weighted-growth-join-diagnostic.manifest.v1"
RESULT_SCHEMA = "cm2.gate4.weighted-growth-join-diagnostic.v1"
HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = (
    HERE / "cm2-gate4-weighted-growth-join-diagnostic-manifest-2026-07-16.json"
)
CERTIFICATE = HERE / "cm2_gate4_weighted_growth_join_diagnostic_cert.py"


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
    if not isinstance(dependencies, dict) or len(dependencies) != 4:
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

    join = result.get("frozen_schema_join_audit", {})
    expected_join_flags = {
        "common_componentwise_join_key_present": False,
        "multiplicity_times_inverse_expansion_join_present": False,
        "digest_is_not_a_typed_join_relation": True,
        "frozen_ledgers_are_pairwise_count_compatible_but_not_row_linked": True,
    }
    for key, expected in expected_join_flags.items():
        if join.get(key) is not expected:
            errors.append(f"join-audit mismatch: {key}")
    if join.get("horizon_ledger", {}).get("leaf_count") != 35024:
        errors.append("horizon count mismatch")
    if join.get("candidate_ledger", {}).get(
        "retained_chart_target_pair_count"
    ) != 448:
        errors.append("candidate count mismatch")
    if join.get("complexity_ledger", {}).get(
        "true_continuity_component_upper"
    ) != 153:
        errors.append("component count mismatch")
    required_fields = join.get("required_join_fields_absent", [])
    if len(required_fields) != 9 or len(set(required_fields)) != 9:
        errors.append("missing-field ledger mismatch")
    for field in (
        "short_unstable_curve_cell_id",
        "physical_continuity_component_id",
        "inverse_expansion_sup_upper",
        "componentwise_weighted_sum_upper",
    ):
        if field not in required_fields:
            errors.append(f"required missing field absent from audit: {field}")

    diagnostic = result.get("exact_aggregate_identifiability", {})
    constants = diagnostic.get("frozen_exact_constants", {})
    expected_constants = {
        "uniform_central_inverse_contraction_upper": "144000/180337",
        "one_true_branch_two_sided_high_strip_tail_upper": "1/5",
        "one_true_branch_cut_sum_strict_upper": "900337/901685",
        "true_continuity_component_count_upper": 153,
        "aggregate_crude_sum_upper": "137751561/901685",
    }
    if constants != expected_constants:
        errors.append("exact constant ledger mismatch")

    interval = diagnostic.get("schema_sharp_interval_diagnostic", {})
    if interval.get("sum_infimum_from_these_constraints") != "0":
        errors.append("aggregate infimum mismatch")
    if interval.get("sum_non_strict_envelope_from_these_constraints") != (
        "137751561/901685"
    ):
        errors.append("aggregate envelope mismatch")
    if interval.get("aggregate_constraints_identify_contraction") is not False:
        errors.append("aggregate-identifiability overclaim")

    completions = diagnostic.get("same_count_abstract_completions", {})
    if completions.get("component_count_in_both_completions") != 153:
        errors.append("completion count mismatch")
    if completions.get("contracting_completion", {}).get(
        "sum_is_below_one"
    ) is not True:
        errors.append("contracting completion mismatch")
    if completions.get("noncontracting_completion", {}).get(
        "sum_is_below_one"
    ) is not False:
        errors.append("noncontracting completion mismatch")
    if completions.get("aggregate_nonidentifiability") != "CERTIFIED":
        errors.append("aggregate nonidentifiability verdict mismatch")
    if completions.get(
        "abstract_schema_completions_not_physical_billiard_claims"
    ) is not True:
        errors.append("abstract-completion scope guard missing")

    budget = diagnostic.get("actionable_contraction_budget", {})
    expected_budget = {
        "frozen_single_true_branch_tail_envelope_at_k0_41": "1/5",
        "current_global_tail_budget_certified": False,
        "hypothetical_single_global_tail_budget_required": "1/5",
        "conditional_central_weight_budget_if_global_tail_proved": "4/5",
        "one_central_uniform_envelope": "144000/180337",
        "conditional_one_central_plus_single_global_tail": "900337/901685",
        "conditional_strict_margin": "1348/901685",
        "two_repeated_central_uniform_envelopes": "288000/180337",
        "uniform_bound_method_first_ceases_to_contract_at_central_count": 2,
    }
    for key, expected in expected_budget.items():
        if budget.get(key) != expected:
            errors.append(f"contraction-budget mismatch: {key}")

    contract = result.get("executable_missing_join_contract", {})
    if len(contract.get("short_curve_cover_fields", [])) != 5:
        errors.append("short-curve contract mismatch")
    if len(contract.get("physical_child_fields", [])) != 6:
        errors.append("physical-child contract mismatch")
    if len(contract.get("completion_guards", [])) != 4:
        errors.append("completion guard mismatch")
    if contract.get("existing_D2T_envelope_is_not_this_join") != (
        "<42672/c_1^3"
    ):
        errors.append("D2T typing guard mismatch")

    limits = result.get("scope_limits", {})
    if limits.get("aggregate_nonidentifiability_certified") is not True:
        errors.append("certified diagnostic scope missing")
    for key in (
        "componentwise_multiplicity_inverse_expansion_join",
        "numeric_delta_1",
        "numeric_global_Growth_contraction",
        "numeric_C_p_vartheta_p",
        "complete_numeric_C_fw_C_rev_q",
        "gate4_certified",
    ):
        if limits.get(key) is not False:
            errors.append(f"fail-closed scope mismatch: {key}")

    # Independent exact arithmetic guards.
    theta = Fraction(144000, 180337)
    tail = Fraction(1, 5)
    q = theta + tail
    if q != Fraction(900337, 901685) or not q < 1:
        errors.append("one-branch arithmetic failed")
    if 153 * q != Fraction(137751561, 901685) or not 153 * q > 1:
        errors.append("crude global arithmetic failed")
    if Fraction(4, 5) - theta != Fraction(1348, 901685):
        errors.append("central-budget arithmetic failed")
    if not 2 * theta > 1:
        errors.append("two-central diagnostic failed")
    if 153 * Fraction(3, 4) != Fraction(459, 4):
        errors.append("noncontracting completion arithmetic failed")

    summary = data.get("replay_summary", {})
    expected_summary = {
        "horizon_leaf_boxes": 35024,
        "retained_chart_target_pairs": 448,
        "true_continuity_component_upper": 153,
        "componentwise_weighted_join_present": False,
        "aggregate_nonidentifiability_certified": True,
        "current_global_tail_budget_certified": False,
        "single_true_branch_tail_envelope": "1/5",
        "conditional_central_budget_if_single_global_tail": "4/5",
        "one_true_branch_cut_sum": "900337/901685",
        "crude_global_sum_upper": "137751561/901685",
        "numeric_global_Growth_contraction": False,
        "gate4_certified": False,
    }
    if summary != expected_summary:
        errors.append("replay summary mismatch")

    expected_verdict = {
        "aggregate_growth_data_nonidentifiability": "CERTIFIED",
        "componentwise_multiplicity_inverse_expansion_join": "NOT_CERTIFIED",
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
    add(
        "certificate_hash",
        lambda d: d.__setitem__("certificate_sha256", "0" * 64),
    )
    add("verifier_hash", lambda d: d.__setitem__("verifier_sha256", "0" * 64))
    add(
        "dependency_hash",
        lambda d: d["dependencies"].__setitem__(
            next(iter(d["dependencies"])), "0" * 64
        ),
    )
    add("result_digest", lambda d: d.__setitem__("result_sha256", "0" * 64))
    add(
        "horizon_count",
        lambda d: d["replay_summary"].__setitem__("horizon_leaf_boxes", 1),
    )
    add(
        "candidate_count",
        lambda d: d["replay_summary"].__setitem__(
            "retained_chart_target_pairs", 1
        ),
    )
    add(
        "join_overclaim",
        lambda d: d["replay_summary"].__setitem__(
            "componentwise_weighted_join_present", True
        ),
    )
    add(
        "global_tail_overclaim",
        lambda d: d["replay_summary"].__setitem__(
            "current_global_tail_budget_certified", True
        ),
    )
    add(
        "growth_overclaim",
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
        print("MUTATION_SELF_TEST: PASS (11/11 mutations rejected)")
        return
    if args.replay or args.integrity_only:
        print("REPLAY_AND_INTEGRITY: PASS")
        return
    print("GATE4_AGGREGATE_GROWTH_DATA_NONIDENTIFIABILITY: CERTIFIED")
    print("GATE4_COMPONENTWISE_WEIGHTED_JOIN: NOT_CERTIFIED")
    print("GATE4_GLOBAL_GROWTH_CONTRACTION: NOT_CERTIFIED")
    print("GATE4_NUMERIC_C_P_VARTTHETA_P_AND_Q: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")
    raise SystemExit(2)


if __name__ == "__main__":
    main()
