#!/usr/bin/env python3
"""Fail-closed verifier for the numeric invariant-family Gate-4 frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import cm2_gate4_numeric_invariant_family_growth_recovery_frontier_cert as cert


Q = Fraction
HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate4.numeric-invariant-family-growth-recovery-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate4.numeric-invariant-family-growth-recovery-frontier.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json"
)
CERTIFICATE = (
    HERE / "cm2_gate4_numeric_invariant_family_growth_recovery_frontier_cert.py"
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

    curvature = result.get("phase_typed_curvature_family", {})
    exact = curvature.get("exact_graph_transform", {})
    products = curvature.get("correlated_curvature_products", {})
    phases = curvature.get("four_phase_invariant_family", {})
    if exact.get("inhomogeneous_exact_upper") != "182549800/729":
        errors.append("curvature inhomogeneous arithmetic mismatch")
    if exact.get("inhomogeneous_round_upper") != "251000":
        errors.append("curvature round upper mismatch")
    if products.get("endpoint_factor_strict_upper") != "12/5":
        errors.append("curvature endpoint factor mismatch")
    if products.get("internal_factor_strict_upper") != "64/125":
        errors.append("curvature internal factor mismatch")
    if products.get("four_step_D0_coefficient_strict_upper") != (
        "3145728/9765625"
    ):
        errors.append("four-step product mismatch")
    if phases.get("phase_curvature_ceilings") != [
        "2000000", "5051000", "12373400", "29947160"
    ]:
        errors.append("phase ceilings mismatch")
    if phases.get("four_step_return_strict_upper") != "49099736/25":
        errors.append("four-step return mismatch")
    if phases.get("global_D_std_strict_upper") != "30000000":
        errors.append("D_std mismatch")
    if phases.get("numeric_phase_typed_curvature_invariance") != "CERTIFIED":
        errors.append("curvature verdict mismatch")
    if phases.get("cuts_preserve_phase_and_do_not_change_graph_curvature") is not True:
        errors.append("cut/phase typing guard missing")

    density = result.get("invariant_density_and_distortion", {})
    distortion = density.get("all_standard_curve_log_jacobian", {})
    cone = density.get("invariant_adapted_density_cone", {})
    if distortion.get("C_log_D_std_exact") != "12960578183270/36337":
        errors.append("C_log(D_std) mismatch")
    if distortion.get("high_strip_one_third_constant") != "5000000000":
        errors.append("high-strip distortion mismatch")
    if distortion.get("central_strip_one_third_constant") != (
        "14000000000000000000000000"
    ):
        errors.append("central-strip distortion mismatch")
    if distortion.get("adapted_one_step_one_third_constant") != (
        "15000000000000000000000000"
    ):
        errors.append("adapted distortion mismatch")
    if distortion.get("numeric_all_iterated_standard_curve_distortion") != (
        "CERTIFIED"
    ):
        errors.append("iterated distortion verdict mismatch")
    if cone.get("density_constant") != "500000000000000000000000000":
        errors.append("density constant mismatch")
    if cone.get("canonical_maximum_adapted_curve_length") != (
        "1/1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
    ):
        errors.append("delta-star mismatch")
    if cone.get("per_curve_log_density_oscillation_upper") != "1/2000":
        errors.append("density oscillation mismatch")
    if cone.get("per_curve_density_ratio_upper") != "2000/1999":
        errors.append("density ratio mismatch")
    if cone.get("every_canonical_curve_is_inside_delta_1_scope") is not True:
        errors.append("delta-star to delta-1 scope guard missing")
    if cone.get("numeric_regular_density_invariance") != "CERTIFIED":
        errors.append("density invariance verdict mismatch")

    growth = result.get("numeric_growth_and_recovery", {})
    recurrence = growth.get("adapted_boundary_Growth_recurrence", {})
    constants = growth.get("numeric_Growth_Lemma_constants", {})
    clock = growth.get("numeric_recovery_clock", {})
    if recurrence.get("one_step_contraction_vartheta_p") != (
        "360134800/360493663"
    ):
        errors.append("Growth contraction mismatch")
    if recurrence.get("one_step_contraction_margin") != (
        "358863/360493663"
    ):
        errors.append("Growth margin mismatch")
    if recurrence.get("additive_mass_coefficient") != str(2 * 10**90):
        errors.append("Growth additive mismatch")
    if recurrence.get("numeric_linear_Growth_recurrence") != "CERTIFIED":
        errors.append("Growth recurrence verdict mismatch")
    if recurrence.get(
        "artificial_chop_additive_is_once_on_total_long_child_mass"
    ) is not True:
        errors.append("artificial chop total-mass guard missing")
    expected_cp_star = str(Q(4 * 10**90 * 360493663, 358863))
    expected_cp_e = str(Q(141 * 10**90 * 360493663, 358863))
    if constants.get("adapted_C_p") != expected_cp_star:
        errors.append("adapted C_p mismatch")
    if constants.get("euclidean_C_p") != expected_cp_e:
        errors.append("Euclidean C_p mismatch")
    if constants.get("vartheta_p") != "360134800/360493663":
        errors.append("C_p/vartheta mismatch")
    if constants.get("numeric_C_p_vartheta_p") != "CERTIFIED":
        errors.append("numeric C_p/vartheta verdict mismatch")
    if clock.get("half_life_block") != 1005:
        errors.append("half-life block mismatch")
    if clock.get("A0") != 301500 or clock.get("A1") != 1005:
        errors.append("A0/A1 mismatch")
    if clock.get("initial_constant_power_two_upper") != "2^300":
        errors.append("initial recovery power mismatch")
    if clock.get("per_orientation_clock") != "R(D)<=301500+1005*D":
        errors.append("recovery target logic mismatch")
    if clock.get("numeric_A0_A1") != "CERTIFIED":
        errors.append("A0/A1 verdict mismatch")

    native = result.get("native_levelwise_recovery_frontier", {})
    level = native.get("native_prefix_levelwise_unnormalized_recovery", {})
    native_limits = native.get("strict_remaining_native_boundary", {})
    if level.get("two_orientation_recovery") != (
        "R_fw+R_rev<=607020+6030*K"
    ):
        errors.append("native recovery clock mismatch")
    if level.get("certified_gamma") != "1/12060":
        errors.append("native gamma mismatch")
    if level.get("geometric_ratio_strict_upper") != "7/8":
        errors.append("native moment ratio mismatch")
    if level.get("payload_moment_strict_upper") != str(2 * 3**52):
        errors.append("native moment upper mismatch")
    if level.get("leafwise_inverse_mass_or_2_to_D_charge_used") is not False:
        errors.append("forbidden leafwise normalization introduced")
    if level.get("record_preserving_levelwise_unnormalized_recovery_moment") != (
        "CERTIFIED"
    ):
        errors.append("native levelwise verdict mismatch")
    if native_limits.get("single_global_native_partition_Z_is_finite") is not False:
        errors.append("native infinite-Z boundary lost")
    if native_limits.get("full_unnormalized_reweighted_native_recovery_contract") != (
        "NOT_CERTIFIED"
    ):
        errors.append("native recovery overclaim")

    frontier = result.get("cost_and_same_occurrence_q_frontier", {})
    if len(frontier.get("still_missing_before_C_fw_C_rev", [])) != 4:
        errors.append("cost frontier field count mismatch")
    for key in ("numeric_C_fw", "numeric_C_rev", "final_same_occurrence_q"):
        if frontier.get(key) is not False:
            errors.append(f"cost/q overclaim: {key}")

    limits = result.get("scope_limits", {})
    for key in (
        "numeric_all_iterated_D_std",
        "numeric_all_iterated_standard_curve_distortion",
        "numeric_regular_density_invariance",
        "numeric_linear_Growth_recurrence",
        "numeric_C_p_vartheta_p",
        "numeric_A0_A1",
        "native_levelwise_unnormalized_payload_recovery_moment",
    ):
        if limits.get(key) is not True:
            errors.append(f"certified scope missing: {key}")
    for key in (
        "single_global_finite_Z_native_family",
        "complete_unnormalized_reweighted_native_recovery",
        "complete_numeric_C_fw_C_rev",
        "final_same_occurrence_q",
        "gate4_certified",
    ):
        if limits.get(key) is not False:
            errors.append(f"fail-closed scope mismatch: {key}")

    # Independent exact arithmetic guards.
    beta = Q(12, 5)
    q = Q(64, 125)
    p4 = beta * q**3
    suffix = 1 + beta * (1 + q + q**2)
    d4 = Q(251000) * suffix + p4 * Q(2_000_000)
    if p4 != Q(3145728, 9765625) or not p4 < 1:
        errors.append("independent phase-product arithmetic failed")
    if d4 != Q(49099736, 25) or not d4 < 2_000_000:
        errors.append("independent phase-return arithmetic failed")
    xi = Q(900337, 901685)
    ratio = Q(2000, 1999)
    a = ratio * xi
    if a != Q(360134800, 360493663) or not a < 1:
        errors.append("independent Growth arithmetic failed")
    if 1 - a != Q(358863, 360493663):
        errors.append("independent Growth margin failed")
    if a**1005 > Q(1, 2):
        errors.append("independent half-life failed")

    expected_summary = {
        "global_D_std_strict_upper": "30000000",
        "phase_zero_four_step_return": "49099736/25",
        "adapted_one_step_distortion": "15000000000000000000000000",
        "density_ratio": "2000/1999",
        "vartheta_p": "360134800/360493663",
        "A0": 301500,
        "A1": 1005,
        "native_gamma": "1/12060",
        "native_payload_moment": True,
        "numeric_C_fw_C_rev": False,
        "final_q": False,
        "gate4_certified": False,
    }
    if data.get("replay_summary") != expected_summary:
        errors.append("replay summary mismatch")
    if data.get("replay_summary_sha256") != cert.canonical_digest(
        data.get("replay_summary", {})
    ):
        errors.append("replay summary digest mismatch")
    expected_verdict = {
        "numeric_all_iterated_D_std": "CERTIFIED",
        "numeric_all_standard_curve_distortion": "CERTIFIED",
        "numeric_C_p_vartheta_p_A0_A1": "CERTIFIED",
        "native_levelwise_unnormalized_recovery_moment": "CERTIFIED",
        "complete_unnormalized_reweighted_native_recovery": "NOT_CERTIFIED",
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
        # Recompute the manifest-internal digest so mutations cannot be
        # rejected merely because a stale summary hash was left behind.
        candidate["replay_summary_sha256"] = cert.canonical_digest(
            candidate.get("replay_summary", {})
        )
        cases.append((name, candidate))

    add("schema", lambda d: d.__setitem__("schema", "mutated"))
    add("certificate_hash", lambda d: d.__setitem__("certificate_sha256", "0" * 64))
    add("verifier_hash", lambda d: d.__setitem__("verifier_sha256", "0" * 64))
    add(
        "dependency_hash",
        lambda d: d["dependencies"].__setitem__(next(iter(d["dependencies"])), "0" * 64),
    )
    add("result_digest", lambda d: d.__setitem__("result_sha256", "0" * 64))
    add("D_std", lambda d: d["replay_summary"].__setitem__("global_D_std_strict_upper", "1"))
    add("phase_return", lambda d: d["replay_summary"].__setitem__("phase_zero_four_step_return", "3"))
    add("distortion", lambda d: d["replay_summary"].__setitem__("adapted_one_step_distortion", "1"))
    add("density", lambda d: d["replay_summary"].__setitem__("density_ratio", "2"))
    add("vartheta", lambda d: d["replay_summary"].__setitem__("vartheta_p", "1"))
    add("A0", lambda d: d["replay_summary"].__setitem__("A0", 1))
    add("A1", lambda d: d["replay_summary"].__setitem__("A1", 1))
    add("gamma", lambda d: d["replay_summary"].__setitem__("native_gamma", "1"))
    add("native_moment", lambda d: d["replay_summary"].__setitem__("native_payload_moment", False))
    add("Cfw_overclaim", lambda d: d["replay_summary"].__setitem__("numeric_C_fw_C_rev", True))
    add("q_overclaim", lambda d: d["replay_summary"].__setitem__("final_q", True))
    add("gate4_overclaim", lambda d: d["verdict"].__setitem__("gate4", "CERTIFIED"))
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
        print("MUTATION_SELF_TEST: PASS (17/17 mutations rejected)")
        return
    if args.replay or args.integrity_only:
        print("REPLAY_AND_INTEGRITY: PASS")
        return
    print("GATE4_NUMERIC_ALL_ITERATED_D_STD: CERTIFIED")
    print("GATE4_NUMERIC_ALL_STANDARD_CURVE_DISTORTION: CERTIFIED")
    print("GATE4_NUMERIC_C_P_VARTTHETA_P_A0_A1: CERTIFIED")
    print("GATE4_NATIVE_LEVELWISE_UNNORMALIZED_RECOVERY_MOMENT: CERTIFIED")
    print("GATE4_COMPLETE_C_FW_C_REV_FINAL_Q: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")
    raise SystemExit(2)


if __name__ == "__main__":
    main()
