#!/usr/bin/env python3
"""Fail-closed verifier for the common free graph-current carrier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import cm2_gate3_common_graph_current_carrier_frontier_cert as certificate


Q = Fraction
HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate3.common-graph-current-carrier-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate3.common-graph-current-carrier-frontier.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate3-common-graph-current-carrier-frontier-manifest-2026-07-17.json"
)
CERTIFICATE = HERE / "cm2_gate3_common_graph_current_carrier_frontier_cert.py"


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

    audit = result.get("frozen_input_audit", {})
    expected_audit = {
        "depth_one_fixed_gauge_DQ": "CERTIFIED",
        "depth_one_current_slot_count": 64,
        "complete_future_side_owner_current": "CERTIFIED",
        "future_graph_slot_count": 41444,
        "all_441280_key_component_characteristic_Z": "CERTIFIED",
        "uniform_characteristic_multiplier_upper": "580000/1999",
    }
    for key, expected in expected_audit.items():
        if audit.get(key) != expected:
            errors.append(f"input audit {key}")

    carrier = result.get("common_free_carrier", {})
    expected_carrier = {
        "initial_face_slot_count": 64,
        "future_face_slot_count": 41444,
        "total_fixed_slot_count": 41508,
        "finite_slot_pullback_is_isometric_in_TV": True,
        "common_free_graph_current_carrier": "CERTIFIED",
    }
    for key, expected in expected_carrier.items():
        if carrier.get(key) != expected:
            errors.append(f"carrier {key}")
    triple = carrier.get("candidate_nested_free_triple", {})
    if triple.get("continuous_injections") != "X2_hat -> X1_hat -> X0_hat":
        errors.append("free triple injections")
    if triple.get("is_a_fixed_Banach_triple") is not True:
        errors.append("free triple fixed")
    if triple.get("is_the_physical_Demers_Zhang_triple") is not False:
        errors.append("free triple physical scope")
    assembly = carrier.get("assembly_to_static_test_dual", {})
    if assembly.get("operator_norm_upper_from_l1_TV") != (
        "1 for sup-normalized tests"
    ):
        errors.append("assembly norm")
    if assembly.get("physical_strong_B0_assembly_bound_proved") is not False:
        errors.append("assembly physical scope")

    algebra = result.get("finite_two_cut_algebra", {})
    expected_algebra = {
        "number_of_additive_single_face_insertions": 2,
        "product_of_two_delta_currents_occurs": False,
        "initial_face_current_TV_upper": "16128/5",
        "future_side_owner_current_TV_upper": "518152320",
        "positive_two_cut_current_TV_outer_upper": "2590777728/5",
        "complete_finite_depth_occurrence_slots": True,
        "complete_finite_depth_positive_TV_outer": True,
        "algebraic_FACE_2CUT_at_depth_at_most_2": "CERTIFIED",
        "strong_operator_DQ_at_depth_2": "NOT_CERTIFIED",
    }
    for key, expected in expected_algebra.items():
        if algebra.get(key) != expected:
            errors.append(f"two-cut algebra {key}")
    try:
        if Q(algebra["initial_face_current_TV_upper"]) + Q(
            algebra["future_side_owner_current_TV_upper"]
        ) != Q(algebra["positive_two_cut_current_TV_outer_upper"]):
            errors.append("two-cut TV arithmetic")
    except Exception:
        errors.append("two-cut TV fractions")

    bridge = result.get("physical_bridge_frontier", {})
    expected_bridge = {
        "available_component_restriction_field": 7,
        "available_component_restriction_multiplier_upper": "580000/1999",
        "available_component_restriction_is_contracting": False,
        "missing_operator_fields": 17,
        "complete_18_field_blocks": 0,
        "bounded_physical_lift_quotient_pair": "NOT_CERTIFIED",
        "this_is_the_exact_free_to_physical_gap": True,
    }
    for key, expected in expected_bridge.items():
        if bridge.get(key) != expected:
            errors.append(f"bridge {key}")

    scope = result.get("strict_nonpromotion", {})
    for key in (
        "free_carrier_implies_physical_strong_space",
        "finite_TV_implies_operator_norm_DQ",
        "finite_depth_algebra_implies_MT_DQ",
        "finite_depth_algebra_implies_FACE_2CUT",
        "all_component_field7_implies_18_fields",
        "all_component_field7_implies_unbounded_cut_recovery",
    ):
        if scope.get(key) is not False:
            errors.append(f"nonpromotion {key}")
    for key in (
        "physical_depth_two_strong_DQ",
        "MT_DQ",
        "FACE_2CUT",
        "FACE_TIME",
        "Gate3",
        "Gate4",
        "Gate5",
    ):
        if scope.get(key) != "NOT_CERTIFIED":
            errors.append(f"scope {key}")

    expected_verdict = {
        "common_free_graph_current_carrier": "CERTIFIED",
        "finite_two_cut_additive_face_algebra": "CERTIFIED",
        "positive_two_cut_TV_outer": "2590777728/5",
        "physical_depth_two_strong_DQ": "NOT_CERTIFIED",
        "MT_DQ_FACE": "NOT_CERTIFIED",
        "Gate3": "NOT_CERTIFIED",
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

    mutate(("result", "frozen_input_audit", "future_graph_slot_count"), 41443)
    mutate(("result", "common_free_carrier", "total_fixed_slot_count"), 41507)
    mutate(("result", "common_free_carrier", "finite_slot_pullback_is_isometric_in_TV"), False)
    mutate(("result", "common_free_carrier", "candidate_nested_free_triple", "is_the_physical_Demers_Zhang_triple"), True)
    mutate(("result", "common_free_carrier", "assembly_to_static_test_dual", "physical_strong_B0_assembly_bound_proved"), True)
    mutate(("result", "finite_two_cut_algebra", "number_of_additive_single_face_insertions"), 1)
    mutate(("result", "finite_two_cut_algebra", "product_of_two_delta_currents_occurs"), True)
    mutate(("result", "finite_two_cut_algebra", "positive_two_cut_current_TV_outer_upper"), "1")
    mutate(("result", "finite_two_cut_algebra", "strong_operator_DQ_at_depth_2"), "CERTIFIED")
    mutate(("result", "physical_bridge_frontier", "missing_operator_fields"), 0)
    mutate(("result", "physical_bridge_frontier", "bounded_physical_lift_quotient_pair"), "CERTIFIED")
    mutate(("result", "strict_nonpromotion", "finite_depth_algebra_implies_MT_DQ"), True)
    mutate(("result", "strict_nonpromotion", "MT_DQ"), "CERTIFIED")
    mutate(("verdict", "Gate3"), "CERTIFIED")
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
    print("COMMON_FREE_GRAPH_CURRENT_CARRIER: CERTIFIED")
    print("FINITE_TWO_CUT_ADDITIVE_FACE_ALGEBRA: CERTIFIED")
    print("PHYSICAL_STRONG_DQ_MT_DQ_FACE: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
