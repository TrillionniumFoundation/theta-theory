#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-3 branch-record/FACE_2CUT frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


SCHEMA = "cm2.gate3.branch-record-face-2cut-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate3.branch-record-face-2cut-frontier.v1"
HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = (
    HERE / "cm2-gate3-branch-record-face-2cut-frontier-manifest-2026-07-16.json"
)
CERTIFICATE = HERE / "cm2_gate3_branch_record_face_2cut_frontier_cert.py"


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
    if not isinstance(dependencies, dict) or not dependencies:
        errors.append("dependencies missing")
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
    provenance = result.get("provenance", {})
    expected_provenance = {
        "v52_manifest": "cm2-v52-manifest.sha256",
        "v52_tex_sha256": (
            "e4fd6c74c4be53ec97287b747e792ec8c32f9cd184cff05047189472481c5daa"
        ),
        "depth_one_DQ_manifest": (
            "cm2-gate3-depth-one-fixed-gauge-dq-manifest-2026-07-15.json"
        ),
        "moving_test_telescope_manifest": (
            "cm2-gate3-moving-test-telescope-frontier-manifest-2026-07-16.json"
        ),
        "product_depth_manifest": (
            "cm2-gate45-product-stopped-depth-kernel-manifest-2026-07-16.json"
        ),
        "recovery_bridge_manifest": (
            "cm2-gate45-density-regular-mesh-recovery-bridge-manifest-2026-07-16.json"
        ),
        "finite_s_common_mesh_recovery_manifest": (
            "cm2-gate45-finite-s-common-mesh-recovery-manifest-2026-07-16.json"
        ),
        "corrected_current_rows_sha256": (
            "5c03da290697ac25b814848c5aee50b22387866f9d72303a60649466cad896bd"
        ),
    }
    for key, expected in expected_provenance.items():
        if provenance.get(key) != expected:
            errors.append(f"provenance mismatch: {key}")

    cluster = result.get("limiting_face_product_centered_cluster", {})
    cluster_expected = {
        "graph_current_unnormalized_TV_upper": "16128/5",
        "common_probability_normalization": (
            "multiply every displayed current norm bound by Z_N^-1"
        ),
        "each_marginal_unnormalized_TV_upper": "16128/5",
        "scalar_mass_c_V": "0",
        "product_current_unnormalized_typed_norm_upper": "32256/5",
        "centered_cluster_unnormalized_typed_sum_norm_upper": "48384/5",
        "limiting_s0_face_product_cluster": "CERTIFIED",
        "finite_s_face_product_cluster_convergence": False,
    }
    for key, expected in cluster_expected.items():
        if cluster.get(key) != expected:
            errors.append(f"face-product cluster mismatch: {key}")
    for key in (
        "both_cluster_marginals_are_exactly_zero",
        "product_pairing_with_two_individually_centered_tests_is_zero",
        "cluster_pairing_equals_graph_pairing_on_centered_endpoint_tests",
        "uses_actual_marginals_not_substitute_measures",
    ):
        if cluster.get(key) is not True:
            errors.append(f"missing face-product algebra flag: {key}")
    try:
        tv = Fraction(cluster["graph_current_unnormalized_TV_upper"])
        prod = Fraction(cluster["product_current_unnormalized_typed_norm_upper"])
        typed = Fraction(cluster["centered_cluster_unnormalized_typed_sum_norm_upper"])
        scalar = Fraction(cluster["scalar_mass_c_V"])
        if prod != 2 * tv + abs(scalar):
            errors.append("face-product norm arithmetic mismatch")
        if typed != tv + prod:
            errors.append("centered-cluster typed norm arithmetic mismatch")
    except (KeyError, TypeError, ValueError, ZeroDivisionError):
        errors.append("invalid face-product rational arithmetic")

    depth = result.get("controlled_uniform_finite_s_auxiliary_depth_tail", {})
    depth_expected = {
        "parameter_window": "|s|<=1/400",
        "positive_charged_level_mass": "a_K=2^K*w_K=(3/4)*2^-K",
        "total_parent_normalization_charge": "sum_K a_K=3/2",
        "strict_tail_after_L": "sum_(K>L) a_K=(3/4)*2^-L",
        "bare_net_auxiliary_depth_exponent": "log(2)>0",
        "checked_depth_range": [0, 64],
        "depth_rows_sha256": (
            "7ce3a7688b3e102d800d811563079ff6c62dda480d93bf449f16c9228546caf2"
        ),
    }
    for key, expected in depth_expected.items():
        if depth.get(key) != expected:
            errors.append(f"auxiliary depth-tail mismatch: {key}")
    if depth.get("controlled_depth_is_auxiliary_K_not_physical_word_depth_ell") is not True:
        errors.append("auxiliary/physical depth distinction missing")
    if depth.get(
        "moving_dyadic_endpoints_registered_in_Gate3_common_DQ_atlas"
    ) is not False:
        errors.append("moving dyadic endpoints must remain outside Gate3 DQ atlas")

    recovery = result.get(
        "controlled_uniform_finite_s_auxiliary_recovery_tail", {}
    )
    recovery_expected = {
        "parameter_window": "|s|<=1/400",
        "certified_input": (
            "uniformly in |s|<=1/400, R_fw+R_rev<=2*A0+2*A1*K"
        ),
        "admissible_exponent": "choose 0<gamma<log(2)/(2*A1)",
        "charged_level_bound": (
            "(3/4)*exp(2*gamma*A0)*(exp(2*gamma*A1)/2)^K"
        ),
        "net_depth_recovery_exponent": "log(2)-2*gamma*A1>0",
        "finite_moment": (
            "sup_(|s|<=1/400) "
            "E_s[2^K*exp(gamma*(R_fw+R_rev))]<infinity"
        ),
        "uniform_finite_s_auxiliary_depth_recovery_tail": "CERTIFIED",
        "moving_dyadic_endpoints_move_with_u_e_s": True,
        "moving_dyadic_endpoints_registered_in_Gate3_common_DQ_atlas": False,
        "uniform_recovery_is_not_common_branch_record_MT_DQ": True,
        "physical_face_word_domination": False,
        "physical_word_depth_identified_with_K": False,
    }
    for key, expected in recovery_expected.items():
        if recovery.get(key) != expected:
            errors.append(f"auxiliary recovery-tail mismatch: {key}")

    clock = result.get("clock_only_two_time_summability", {})
    clock_expected = {
        "parameter_window": "|s|<=1/400",
        "moment_input": (
            "M_gamma=sup_(|s|<=1/400) "
            "E_s[2^K*exp(gamma*(R_fw+R_rev))]<infinity"
        ),
        "long_side_clock_tail": (
            "sup_s E_s[2^K*1_{R_o>delta*N}]"
            "<=M_gamma*exp(-gamma*delta*N), o=fw,rev"
        ),
        "uniform_coupling_hypothesis": (
            "given one c_mix>0 uniform in |s|<=1/400 for the matched "
            "proper-family current"
        ),
        "balanced_delta": "delta=c_mix/(gamma+c_mix)",
        "clock_rate": "kappa=gamma*c_mix/(gamma+c_mix)>0",
        "exact_double_sum_formula": (
            "sum_(m,n>=0) x^max(m,n)=(1+x)/(1-x)^2, x=exp(-kappa)<1"
        ),
        "clock_array_is_product_time_summable": True,
        "clock_array_uniform_for_abs_s_at_most_1_over_400": True,
        "same_s_K_j_record_has_both_oriented_recovery_clocks_uniformly": True,
        "clock_only_not_FACE_TIME_REC": True,
        "pair_shell_rows_sha256": (
            "59291ec28c7de6f10b3b48d9386f0766f307cb3c5b264300df7f02b78d5f6fcc"
        ),
    }
    for key, expected in clock_expected.items():
        if clock.get(key) != expected:
            errors.append(f"clock-only summability mismatch: {key}")
    for key in (
        "moving_dyadic_endpoints_registered_in_Gate3_common_DQ_atlas",
        "physical_signed_proper_family_factorization",
        "restrictionwise_propagated_q_domination",
        "physical_test_norm_lift",
    ):
        if clock.get(key) is not False:
            errors.append(f"unsupported physical clock application flag: {key}")

    branch = result.get("branch_source_nonimplication_countermodel", {})
    branch_expected = {
        "countermodel_rows_sha256": (
            "90bf276d89bcd9aef56d3a34c45b71c1607fc15d1a060ec9b7be95cf644c3627"
        ),
        "depth_two_failure": (
            "for h=e_1 and k>=2, P_s*A_k*h=0 but A_k*P0*h=e_1"
        ),
        "strong_source_not_invariant": (
            "P0 e_1=x notin Y because sum k^2|x_k|^2=sum 1=infinity"
        ),
    }
    for key, expected in branch_expected.items():
        if branch.get(key) != expected:
            errors.append(f"branch-source countermodel mismatch: {key}")

    atlas = result.get("common_atlas_boundary_countermodel", {})
    if atlas.get("pairing_failure") != "J_s(Phi)=1 while J_0(Phi)=0":
        errors.append("common-atlas boundary countermodel mismatch")
    if atlas.get("failed_required_clause") != (
        "sup_(0<s<rho) |J_s|([S]_rho)=1, so no C*rho^theta boundary tightness"
    ):
        errors.append("boundary-tightness failure mismatch")

    face = result.get("FACE_2CUT_vs_FACE_TIME_countermodel", {})
    face_expected = {
        "countermodel_rows_sha256": (
            "56900478016d946d8d78a8e4d9404f2142340de765f888abe15fb5e9718b04cb"
        ),
        "every_fixed_pair_FACE_2CUT_tail_is_exponential": True,
        "complete_pairing": "B_(m,n)=1_(m=n)",
        "product_time_absolute_sum": "sum_(m,n)|B_(m,n)|=infinity",
    }
    for key, expected in face_expected.items():
        if face.get(key) != expected:
            errors.append(f"FACE_2CUT/FACE_TIME countermodel mismatch: {key}")

    digests = result.get("internal_replay_digests", {})
    for key, expected in {
        "depth_rows": "7ce3a7688b3e102d800d811563079ff6c62dda480d93bf449f16c9228546caf2",
        "branch_countermodel_rows": (
            "90bf276d89bcd9aef56d3a34c45b71c1607fc15d1a060ec9b7be95cf644c3627"
        ),
        "face_time_countermodel_rows": (
            "56900478016d946d8d78a8e4d9404f2142340de765f888abe15fb5e9718b04cb"
        ),
    }.items():
        if digests.get(key) != expected:
            errors.append(f"internal replay digest mismatch: {key}")

    frontier = result.get("exact_remaining_frontier", {})
    for key, expected_length in {
        "certified_now": 5,
        "still_missing_for_branch_record_MT_DQ": 5,
        "still_missing_for_physical_FACE_2CUT": 5,
        "still_missing_for_FACE_TIME": 4,
    }.items():
        if len(frontier.get(key, [])) != expected_length:
            errors.append(f"frontier ledger mismatch: {key}")

    limits = result.get("scope_limits", {})
    for key in (
        "limiting_s0_face_product_centered_cluster",
        "numeric_limiting_face_product_typed_bounds",
        "controlled_uniform_finite_s_auxiliary_depth_tail",
        "controlled_uniform_finite_s_auxiliary_depth_recovery_tail",
        "uniform_finite_s_clock_only_two_time_array_summable",
        "physical_face_current_available_only_as_limiting_s0_cluster",
    ):
        if limits.get(key) is not True:
            errors.append(f"missing certified scope flag: {key}")
    for key in (
        "finite_s_face_product_cluster_convergence",
        "moving_dyadic_endpoints_registered_in_Gate3_common_DQ_atlas",
        "component_indexed_iterated_common_moving_atlas",
        "fixed_time_dynamic_branch_record_MT_DQ",
        "full_three_space_MT_DQ",
        "physical_FACE_2CUT",
        "physical_FACE_TIME_CM2_or_REC",
        "CM2_norm_lifts",
        "gate3_certified",
    ):
        if limits.get(key) is not False:
            errors.append(f"unsupported completion flag: {key}")

    verdict = data.get("verdict", {})
    expected_verdict = {
        "limiting_s0_face_product_centered_cluster": "CERTIFIED",
        "uniform_finite_s_auxiliary_depth_recovery_tail": "CERTIFIED",
        "uniform_finite_s_clock_only_two_time_summability": "CERTIFIED",
        "dynamic_branch_record_MT_DQ": "NOT_CERTIFIED",
        "physical_FACE_2CUT_and_FACE_TIME": "NOT_CERTIFIED",
        "gate3": "NOT_CERTIFIED",
    }
    for key, expected in expected_verdict.items():
        if verdict.get(key) != expected:
            errors.append(f"verdict mismatch: {key}")
    return errors


def check_replay(data: dict[str, Any]) -> list[str]:
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    try:
        import cm2_gate3_branch_record_face_2cut_frontier_cert as cert

        actual = cert.certify()
    except Exception as exc:
        return [f"certificate replay failed: {exc}"]
    return [] if data.get("result") == actual else ["full certificate replay mismatch"]


def run_self_test(data: dict[str, Any]) -> int:
    mutations: list[tuple[str, dict[str, Any]]] = []

    tampered = copy.deepcopy(data)
    tampered["result"]["limiting_face_product_centered_cluster"][
        "product_current_unnormalized_typed_norm_upper"
    ] = "16128/5"
    mutations.append(("face-product norm tamper", tampered))

    tampered = copy.deepcopy(data)
    tampered["result"]["controlled_uniform_finite_s_auxiliary_depth_tail"][
        "strict_tail_after_L"
    ] = "sum_(K>L) a_K=2^-L"
    mutations.append(("auxiliary depth-tail tamper", tampered))

    tampered = copy.deepcopy(data)
    tampered["result"]["controlled_uniform_finite_s_auxiliary_recovery_tail"][
        "parameter_window"
    ] = "s=0"
    mutations.append(("finite-s parameter-window tamper", tampered))

    tampered = copy.deepcopy(data)
    tampered["result"]["branch_source_nonimplication_countermodel"][
        "depth_two_failure"
    ] = "no failure"
    mutations.append(("branch-source countermodel tamper", tampered))

    tampered = copy.deepcopy(data)
    tampered["result"]["FACE_2CUT_vs_FACE_TIME_countermodel"][
        "product_time_absolute_sum"
    ] = "finite"
    mutations.append(("FACE_TIME countermodel tamper", tampered))

    tampered = copy.deepcopy(data)
    tampered["result"]["scope_limits"]["physical_FACE_2CUT"] = True
    mutations.append(("unsupported physical FACE_2CUT", tampered))

    tampered = copy.deepcopy(data)
    tampered["result"]["scope_limits"][
        "moving_dyadic_endpoints_registered_in_Gate3_common_DQ_atlas"
    ] = True
    mutations.append(("unsupported moving-endpoint DQ-atlas registration", tampered))

    tampered = copy.deepcopy(data)
    tampered["result"]["scope_limits"]["gate3_certified"] = True
    mutations.append(("unsupported Gate-3 completion", tampered))

    for label, mutation in mutations:
        if not check_structure(mutation):
            print(f"SELF_TEST: FAIL ({label} accepted)")
            return 1
    print("SELF_TEST: PASS")
    for label, _ in mutations:
        print(f"  {label} rejected")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"MANIFEST_READ_ERROR: {exc}", file=sys.stderr)
        return 1
    errors = check_structure(data)
    if args.replay and not errors:
        errors.extend(check_replay(data))
    if errors:
        print("GATE3_BRANCH_RECORD_FACE_2CUT_FRONTIER_INTEGRITY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1
    if args.self_test:
        return run_self_test(data)
    print("GATE3_LIMITING_FACE_PRODUCT_CENTERED_CLUSTER: CERTIFIED")
    print("GATE3_UNIFORM_FINITE_S_AUXILIARY_DEPTH_RECOVERY_TAIL: CERTIFIED")
    print("GATE3_UNIFORM_FINITE_S_CLOCK_ONLY_TWO_TIME_ARRAY: CERTIFIED")
    if args.integrity_only:
        print("GATE3_BRANCH_RECORD_FACE_2CUT_FRONTIER_INTEGRITY: PASS")
        return 0
    print("GATE3_DYNAMIC_BRANCH_RECORD_MT_DQ_AND_PHYSICAL_FACE_2CUT: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
