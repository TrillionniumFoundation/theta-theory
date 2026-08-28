#!/usr/bin/env python3
"""Fail-closed verifier for the fixed-core Green-kernel frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import cm2_gate4_fixed_core_green_kernel_unbounded_cut_frontier_cert as certificate


Q = Fraction
HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate4.fixed-core-green-kernel-unbounded-cut-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate4.fixed-core-green-kernel-unbounded-cut-frontier.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate4-fixed-core-green-kernel-unbounded-cut-frontier-manifest-2026-07-17.json"
)
CERTIFICATE = (
    HERE / "cm2_gate4_fixed_core_green_kernel_unbounded_cut_frontier_cert.py"
)


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

    kernel = result.get("fixed_core_green_kernel", {})
    expected_kernel = {
        "b_core": "720269600000/720626832337",
        "contraction_margin": "357232337/720626832337",
        "exact_zeroth_delay_moment_value": "720626832337/357232337",
        "exact_first_delay_moment_value": (
            "519045600276638055200000/127614942598481569"
        ),
        "all_polynomial_delay_moments_finite": True,
        "fixed_core_unbounded_transport_delay_Green_kernel": "CERTIFIED",
    }
    for key, expected in expected_kernel.items():
        if kernel.get(key) != expected:
            errors.append(f"kernel {key}")
    exponential = kernel.get("rational_exponential_moment", {})
    expected_exponential = {
        "gamma": "1/4036",
        "half_life_block": 2018,
        "weighted_block_ratio_upper": "5/6",
        "sum_exp_gamma_k_g_k_upper": "20180",
        "sum_k_exp_gamma_k_g_k_upper": "244339440",
    }
    for key, expected in expected_exponential.items():
        if exponential.get(key) != expected:
            errors.append(f"exponential {key}")

    transport = result.get("summable_injection_transport", {})
    if transport.get("arbitrarily_many_injection_times_allowed_if_total_injection_is_summable") is not True:
        errors.append("summable injection count")
    if transport.get("unbounded_transport_delay_count") != "CERTIFIED":
        errors.append("transport status")
    conditional = transport.get("conditional_common_carrier_injection", {})
    expected_conditional = {
        "input_two_cut_TV_outer": "2590777728/5",
        "requires_physical_incidence_with_norm_enlargement_at_most_one": True,
        "total_unweighted_delay_TV_upper": (
            "24246544771660906368/23196905"
        ),
        "first_delay_moment_TV_upper": (
            "3492809820813258473063362560000/1657336916863397"
        ),
        "exponential_delay_TV_upper": "10456378910208",
        "exponential_first_delay_TV_upper": "126605835844798464",
        "physical_installation": "NOT_CERTIFIED",
    }
    for key, expected in expected_conditional.items():
        if conditional.get(key) != expected:
            errors.append(f"conditional transport {key}")

    criterion = result.get("unbounded_new_cut_criterion", {})
    if criterion.get("unbounded_new_cut_criterion") != "CERTIFIED":
        errors.append("cut criterion status")
    if criterion.get("unbounded_new_cut_hypothesis") != "NOT_CERTIFIED":
        errors.append("cut hypothesis scope")
    shell = criterion.get("one_cut_mass_weighted_shell", {})
    if shell.get("a") != "15/8":
        errors.append("shell factor")
    if shell.get("necessary_strict_sufficient_threshold_for_this_bound") != (
        "rho<8/15"
    ):
        errors.append("shell threshold")
    field7 = criterion.get("raw_all_component_field7", {})
    if field7.get("a") != "580000/1999":
        errors.append("field7 factor")
    if field7.get("necessary_strict_sufficient_threshold_for_this_bound") != (
        "rho<1999/580000"
    ):
        errors.append("field7 threshold")
    if criterion.get("certified_native_geometric_cut_count_rho") is not None:
        errors.append("invented cut rho")

    scope = result.get("strict_nonpromotion", {})
    for key in (
        "unbounded_delay_implies_physical_occurrence_incidence",
        "summable_injections_imply_arbitrary_injections_are_summable",
        "finite_one_cut_factor_implies_native_cut_count_tail",
        "fixed_core_Green_kernel_implies_cemetery_payload",
    ):
        if scope.get(key) is not False:
            errors.append(f"nonpromotion {key}")
    for key in (
        "transported_24_core_to_41444_graph_incidence",
        "strong_complement_cemetery_payload",
        "native_unbounded_repeated_cut_recovery",
        "complete_C_fw_C_rev_q",
        "Gate4",
    ):
        if scope.get(key) != "NOT_CERTIFIED":
            errors.append(f"scope {key}")

    try:
        b = Q(kernel["b_core"])
        if 1 / (1 - b) != Q(kernel["exact_zeroth_delay_moment_value"]):
            errors.append("zeroth arithmetic")
        if b / (1 - b) ** 2 != Q(
            kernel["exact_first_delay_moment_value"]
        ):
            errors.append("first arithmetic")
        if b**2018 >= Q(1, 2):
            errors.append("half-life arithmetic")
    except Exception:
        errors.append("kernel fractions")

    expected_verdict = {
        "fixed_core_unbounded_transport_delay_Green_kernel": "CERTIFIED",
        "summable_injection_convolution_ledger": "CERTIFIED",
        "unbounded_new_cut_geometric_tail_criterion": "CERTIFIED",
        "transported_occurrence_to_core_incidence": "NOT_CERTIFIED",
        "native_unbounded_repeated_cut_recovery": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
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

    mutate(("result", "fixed_core_green_kernel", "b_core"), "1")
    mutate(("result", "fixed_core_green_kernel", "exact_zeroth_delay_moment_value"), "1")
    mutate(("result", "fixed_core_green_kernel", "all_polynomial_delay_moments_finite"), False)
    mutate(("result", "fixed_core_green_kernel", "rational_exponential_moment", "gamma"), "1")
    mutate(("result", "fixed_core_green_kernel", "rational_exponential_moment", "weighted_block_ratio_upper"), "1")
    mutate(("result", "summable_injection_transport", "unbounded_transport_delay_count"), "NOT_CERTIFIED")
    mutate(("result", "summable_injection_transport", "conditional_common_carrier_injection", "physical_installation"), "CERTIFIED")
    mutate(("result", "unbounded_new_cut_criterion", "one_cut_mass_weighted_shell", "necessary_strict_sufficient_threshold_for_this_bound"), "rho<1")
    mutate(("result", "unbounded_new_cut_criterion", "raw_all_component_field7", "a"), "1")
    mutate(("result", "unbounded_new_cut_criterion", "certified_native_geometric_cut_count_rho"), "1/2")
    mutate(("result", "unbounded_new_cut_criterion", "unbounded_new_cut_hypothesis"), "CERTIFIED")
    mutate(("result", "strict_nonpromotion", "finite_one_cut_factor_implies_native_cut_count_tail"), True)
    mutate(("result", "strict_nonpromotion", "native_unbounded_repeated_cut_recovery"), "CERTIFIED")
    mutate(("verdict", "Gate4"), "CERTIFIED")
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
    print("FIXED_CORE_UNBOUNDED_DELAY_GREEN_KERNEL: CERTIFIED")
    print("UNBOUNDED_NEW_CUT_TAIL_CRITERION: CERTIFIED")
    print("NATIVE_UNBOUNDED_REPEATED_CUT_RECOVERY: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
