#!/usr/bin/env python3
"""Fail-closed verifier for the componentwise global Growth frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import cm2_gate4_componentwise_global_growth_recovery_frontier_cert as cert


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate4.componentwise-global-growth-recovery-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate4.componentwise-global-growth-recovery-frontier.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate4-componentwise-global-growth-recovery-frontier-manifest-2026-07-16.json"
)
CERTIFICATE = (
    HERE / "cm2_gate4_componentwise_global_growth_recovery_frontier_cert.py"
)


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
    if data.get("dependencies") != cert.DEPENDENCIES:
        errors.append("dependency ledger mismatch")
    else:
        for name, expected in cert.DEPENDENCIES.items():
            path = HERE / name
            if not path.is_file() or sha256_path(path) != expected:
                errors.append(f"dependency hash mismatch: {name}")

    try:
        result = cert.certify()
    except Exception as exc:
        return errors + [f"certificate replay failed: {type(exc).__name__}: {exc}"]
    if result.get("schema") != RESULT_SCHEMA:
        errors.append("result schema mismatch")
    if data.get("result_sha256") != cert.canonical_digest(result):
        errors.append("result digest mismatch")

    outer = result.get("typed_outer_universe", {})
    incidence = result.get("short_curve_central_incidence_theorem", {})
    weighted = result.get("componentwise_weighted_growth_join", {})
    recovery = result.get("recovery_and_propagation_frontier", {})
    limits = result.get("scope_limits", {})

    horizon = outer.get("horizon_witness_ledger", {})
    candidate = outer.get("candidate_owner_ledger", {})
    chart_sheets = outer.get("chart_raw_sheet_incidence_ledger", {})
    owners = outer.get("global_owner_ledger", {})
    sheets = outer.get("global_raw_sheet_ledger", {})
    if horizon.get("leaf_count") != 35024:
        errors.append("horizon count mismatch")
    if horizon.get("has_short_curve_or_component_key") is not False:
        errors.append("horizon ledger overtyped")
    if candidate.get("row_count") != 448:
        errors.append("candidate count mismatch")
    if candidate.get("chart_counts") != {
        "G:E": 57,
        "G:W": 57,
        "G:N": 57,
        "G:S": 57,
        "W:E": 55,
        "W:W": 55,
        "W:N": 55,
        "W:S": 55,
    }:
        errors.append("candidate chart counts mismatch")
    if candidate.get("typed_rows_are_conservative_not_physical") is not True:
        errors.append("candidate typing guard missing")
    if chart_sheets.get("row_count") != 896:
        errors.append("chart sheet incidence count mismatch")
    if owners.get("row_count") != 144 or owners.get("source_counts") != {
        "G": 76,
        "W": 68,
    }:
        errors.append("global owner quotient mismatch")
    if sheets.get("row_count") != 288:
        errors.append("raw sheet count mismatch")
    if sheets.get("source_sheet_counts") != {"G": 152, "W": 136}:
        errors.append("source sheet counts mismatch")
    if sheets.get("maximum_true_continuity_components") != 153:
        errors.append("true component upper mismatch")

    expected_incidence = {
        "homogeneity_cutoff_k0": 6121,
        "central_cosine_strict_lower": "1/74933282",
        "central_discriminant_strict_lower": "4/877343242389300625",
        "discriminant_r_derivative_strict_upper": "53748/625",
        "central_to_selected_tangency_r_distance_strict_lower": (
            "1/18862177836776051997"
        ),
        "two_signed_tangent_angle_gap_strict_lower": "2/21",
        "curve_minus_sheet_r_derivative_strict_upper": "8323517/145348",
        "two_signed_sheet_crossing_r_separation_strict_lower": "41528/24970551",
        "uniform_small_curve_threshold_delta_1": "1/37724355673552103994",
        "at_most_one_central_child_for_length_at_most_delta_1": True,
        "central_child_global_multiplicity_upper": 1,
        "compressed_sheet_separation_incidence_theorem": "CERTIFIED",
    }
    for key, expected in expected_incidence.items():
        if incidence.get(key) != expected:
            errors.append(f"incidence theorem mismatch: {key}")
    if incidence.get("chart_seams_are_not_physical_cuts") is not True:
        errors.append("chart seam typing guard missing")

    expected_weighted = {
        "central_child_multiplicity_upper": 1,
        "high_child_multiplicity_upper_per_sign_and_rank": 153,
        "central_inverse_expansion_strict_upper": "144000/180337",
        "high_child_inverse_expansion_strict_upper": "4/k^2",
        "global_high_strip_tail_strict_upper": "1/5",
        "global_one_step_weighted_sum_strict_upper": "900337/901685",
        "global_one_step_weighted_sum_margin": "1348/901685",
        "componentwise_multiplicity_inverse_expansion_join": "CERTIFIED_COMPRESSED",
        "numeric_global_one_step_weighted_Growth_contraction": "CERTIFIED",
        "this_is_not_q_branch_repetition": True,
        "this_is_not_final_same_occurrence_q": True,
    }
    for key, expected in expected_weighted.items():
        if weighted.get(key) != expected:
            errors.append(f"weighted join mismatch: {key}")
    if weighted.get("every_true_and_homogeneity_cut_counted_once") is not True:
        errors.append("cut completeness guard missing")
    if weighted.get("conservative_candidates_not_charged_as_physical_children") is not True:
        errors.append("candidate charge typing guard missing")
    if len(weighted.get("join_fields", [])) != 6:
        errors.append("typed join field count mismatch")
    if len(weighted.get("typed_component_templates", [])) != 2:
        errors.append("typed component template count mismatch")
    if weighted.get("typed_component_templates_sha256") != cert.canonical_digest(
        weighted.get("typed_component_templates", [])
    ):
        errors.append("typed component template digest mismatch")

    propagation = recovery.get("propagation_status", {})
    for key in (
        "numeric_C_p",
        "numeric_vartheta_p",
        "numeric_A0_A1",
        "numeric_C_fw",
        "numeric_C_rev",
        "final_same_occurrence_q",
    ):
        if propagation.get(key) is not False:
            errors.append(f"propagation overclaim: {key}")
    unnormalized = recovery.get("unnormalized_reweighted_native_recovery_contract", {})
    if len(unnormalized.get("required_fields", [])) != 5:
        errors.append("unnormalized recovery contract mismatch")
    if unnormalized.get("fields_present_in_frozen_manifests") != 0:
        errors.append("unnormalized recovery field overclaim")
    if unnormalized.get("finite_cemetery_no_go_applies_to_this_contract") is not False:
        errors.append("finite-cemetery scope widened incorrectly")
    if unnormalized.get("unnormalized_reweighted_recovery") != "NOT_CERTIFIED":
        errors.append("unnormalized recovery verdict mismatch")
    if len(recovery.get("still_missing_before_numeric_C_p_vartheta_p", [])) != 4:
        errors.append("numeric recovery frontier mismatch")

    for key in (
        "typed_horizon_candidate_raw_sheet_audit",
        "compressed_physical_component_join",
        "numeric_delta_1",
        "at_most_one_global_central_child",
        "single_global_high_strip_tail",
        "numeric_global_one_step_weighted_Growth_contraction",
    ):
        if limits.get(key) is not True:
            errors.append(f"certified scope missing: {key}")
    for key in (
        "full_numeric_Growth_Lemma_constants",
        "numeric_C_p_vartheta_p",
        "unnormalized_reweighted_native_recovery",
        "complete_numeric_C_fw_C_rev_final_q",
        "gate4_certified",
    ):
        if limits.get(key) is not False:
            errors.append(f"fail-closed scope mismatch: {key}")

    # Independent exact arithmetic guards.
    k0 = 6121
    component_upper = 153
    global_tail = component_upper * Fraction(8, k0 - 1)
    theta = Fraction(144000, 180337)
    xi = theta + global_tail
    if global_tail != Fraction(1, 5):
        errors.append("global tail arithmetic failed")
    if xi != Fraction(900337, 901685) or not xi < 1:
        errors.append("global Xi arithmetic failed")
    if 1 - xi != Fraction(1348, 901685):
        errors.append("global Xi margin arithmetic failed")
    derivative = 2 * Fraction(9, 25) * (
        1 + Fraction(84, 25) * (Fraction(25, 4) + 29)
    )
    central_delta = Fraction(4, 625 * k0**4)
    collar = central_delta / derivative
    delta_1 = collar / 2
    if derivative != Fraction(53748, 625):
        errors.append("discriminant derivative arithmetic failed")
    if collar != Fraction(1, 18862177836776051997):
        errors.append("central collar arithmetic failed")
    if delta_1 != Fraction(1, 37724355673552103994):
        errors.append("delta_1 arithmetic failed")
    sheet_slope = Fraction(29) + Fraction(25, 4) + Fraction(800000, 36337)
    sheet_separation = Fraction(2, 21) / sheet_slope
    if sheet_separation != Fraction(41528, 24970551) or not delta_1 < sheet_separation:
        errors.append("signed sheet separation arithmetic failed")

    expected_summary = {
        "horizon_leaf_boxes": 35024,
        "retained_candidate_rows": 448,
        "global_owner_rows": 144,
        "global_raw_signed_sheets": 288,
        "true_continuity_component_upper": 153,
        "homogeneity_cutoff_k0": 6121,
        "delta_1": "1/37724355673552103994",
        "central_child_multiplicity_upper": 1,
        "global_high_strip_tail_strict_upper": "1/5",
        "global_one_step_Xi_strict_upper": "900337/901685",
        "global_one_step_Xi_margin": "1348/901685",
        "compressed_componentwise_join": True,
        "global_one_step_weighted_Growth_contraction": True,
        "numeric_C_p_vartheta_p": False,
        "unnormalized_reweighted_native_recovery": False,
        "gate4_certified": False,
    }
    if data.get("replay_summary") != expected_summary:
        errors.append("replay summary mismatch")
    expected_verdict = {
        "typed_componentwise_growth_join": "CERTIFIED_COMPRESSED",
        "global_one_step_weighted_Growth_contraction": "CERTIFIED",
        "full_numeric_Growth_Lemma_constants": "NOT_CERTIFIED",
        "numeric_C_p_vartheta_p": "NOT_CERTIFIED",
        "unnormalized_reweighted_native_recovery": "NOT_CERTIFIED",
        "complete_numeric_C_fw_C_rev_final_q": "NOT_CERTIFIED",
        "gate4": "NOT_CERTIFIED",
    }
    if data.get("verdict") != expected_verdict:
        errors.append("verdict mismatch")
    return errors


def mutation_self_test(baseline: dict[str, Any]) -> list[str]:
    cases: list[tuple[str, dict[str, Any]]] = []

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
    add("horizon", lambda d: d["replay_summary"].__setitem__("horizon_leaf_boxes", 1))
    add("candidate", lambda d: d["replay_summary"].__setitem__("retained_candidate_rows", 1))
    add("raw_sheet", lambda d: d["replay_summary"].__setitem__("global_raw_signed_sheets", 1))
    add("k0", lambda d: d["replay_summary"].__setitem__("homogeneity_cutoff_k0", 41))
    add("delta_1", lambda d: d["replay_summary"].__setitem__("delta_1", "1"))
    add(
        "central_multiplicity",
        lambda d: d["replay_summary"].__setitem__("central_child_multiplicity_upper", 2),
    )
    add(
        "global_tail",
        lambda d: d["replay_summary"].__setitem__("global_high_strip_tail_strict_upper", "2"),
    )
    add(
        "global_xi",
        lambda d: d["replay_summary"].__setitem__("global_one_step_Xi_strict_upper", "2"),
    )
    add(
        "Cp_overclaim",
        lambda d: d["replay_summary"].__setitem__("numeric_C_p_vartheta_p", True),
    )
    add("verdict", lambda d: d["verdict"].__setitem__("gate4", "CERTIFIED"))
    return [name for name, candidate in cases if not check_structure(candidate)]


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
        print("MUTATION_SELF_TEST: PASS (15/15 mutations rejected)")
        return
    if args.replay or args.integrity_only:
        print("REPLAY_AND_INTEGRITY: PASS")
        return
    print("GATE4_TYPED_COMPONENTWISE_JOIN: CERTIFIED_COMPRESSED")
    print("GATE4_GLOBAL_ONE_STEP_WEIGHTED_GROWTH_CONTRACTION: CERTIFIED")
    print("GATE4_NUMERIC_C_P_VARTTHETA_P: NOT_CERTIFIED")
    print("GATE4_UNNORMALIZED_REWEIGHTED_NATIVE_RECOVERY: NOT_CERTIFIED")
    print("GATE4_COMPLETE_C_FW_C_REV_FINAL_Q: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")
    raise SystemExit(2)


if __name__ == "__main__":
    main()
