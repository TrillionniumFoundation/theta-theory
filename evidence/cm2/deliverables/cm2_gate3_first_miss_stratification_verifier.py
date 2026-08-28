#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-3 first/miss stratification."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


SCHEMA = "cm2.gate3.first-miss-stratification.manifest.v1"
HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = (
    HERE / "cm2-gate3-first-miss-stratification-manifest-2026-07-15.json"
)
CERTIFICATE = HERE / "cm2_gate3_first_miss_stratification_cert.py"


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
    if result.get("precision_bits") != 192:
        errors.append("precision mismatch")
    if result.get("remaining_two_dimensional_unresolved_parameter_area") != "0":
        errors.append("two-dimensional residual must be zero")
    if result.get("physical_transition_curve_parameter_measure") != "0":
        errors.append("transition-curve measure mismatch")

    claims = result.get("dependency_claims", {})
    for key, expected in {
        "target_target_descriptor_universe": 82048,
        "corrected_unresolved_descriptors_physically_empty": 320,
        "physical_joint_vertices": 0,
        "predecessor_residual_first_or_miss_area": "18081/1638400",
    }.items():
        if claims.get(key) != expected:
            errors.append(f"dependency claim mismatch: {key}")

    descriptors = result.get("physical_common_tangent_descriptor_registry", {})
    for key, expected in {
        "strict_full_window_physical_earlier_descriptor_count": 48,
        "strict_full_window_physical_later_descriptor_count": 48,
        "corrected_first_pass_unresolved_descriptor_count": 288,
        "physical_descriptor_rows_sha256": "dc4a51acfc65872543b57bba2e4104fc1b040c02ee7483983344e589e6257b41",
    }.items():
        if descriptors.get(key) != expected:
            errors.append(f"descriptor registry mismatch: {key}")

    residual = result.get("depth_thirteen_residual_input", {})
    for key, expected in {
        "initial_depth_nine_first_or_miss_box_count": 17912,
        "maximum_refinement_depth": 13,
        "residual_box_count_before_stratification": 72324,
        "residual_ambient_box_area_before_stratification": "18081/1638400",
    }.items():
        if residual.get(key) != expected:
            errors.append(f"residual input mismatch: {key}")
    counts = residual.get("final_classification_counts", {})
    for key, expected in {
        "unresolved_first_visibility": 13216,
        "unresolved_miss_owner": 59108,
        "unresolved_parameter_polarity": 768,
        "physical_immutable_subrow": 50144,
        "empty_target_strictly_occluded": 4680,
    }.items():
        if counts.get(key) != expected:
            errors.append(f"depth-thirteen count mismatch: {key}")
    try:
        areas = residual["final_classification_ambient_areas"]
        if Fraction(areas["unresolved_first_visibility"]) + Fraction(
            areas["unresolved_miss_owner"]
        ) != Fraction(18081, 1638400):
            errors.append("depth-thirteen residual-area identity mismatch")
    except (KeyError, TypeError, ValueError):
        errors.append("invalid depth-thirteen area ledger")

    matching = result.get("residual_box_transition_matching", {})
    for key, expected in {
        "boxes_meeting_no_physical_transition_curve": 59028,
        "boxes_meeting_exactly_one_physical_transition_curve": 13296,
        "boxes_meeting_two_or_more_physical_transition_curves": 0,
        "active_physical_transition_descriptor_count": 48,
        "active_descriptor_box_hit_minimum": 256,
        "active_descriptor_box_hit_maximum": 310,
        "boundary_free_constant_state_rows_sha256": "1aad2d973d1a085fb37a464a47d4b608755bcd236da654e2e534837ae3e5bf14",
    }.items():
        if matching.get(key) != expected:
            errors.append(f"transition matching mismatch: {key}")
    if matching.get("boundary_free_counts_by_kind") != {
        "unresolved_first_visibility": 8900,
        "unresolved_miss_owner": 50128,
    }:
        errors.append("boundary-free kind counts mismatch")
    if matching.get("one_curve_counts_by_kind") != {
        "unresolved_first_visibility": 4316,
        "unresolved_miss_owner": 8980,
    }:
        errors.append("one-curve kind counts mismatch")

    curves = result.get("analytic_curve_strip_stratification", {})
    for key, expected in {
        "analytic_transition_curve_count": 48,
        "physical_earlier_transition_curve_count": 16,
        "physical_later_transition_curve_count": 32,
        "full_window_strips_per_curve": 256,
        "curve_strip_group_count": 12288,
        "curve_groups_strictly_inside_z_envelopes": 12288,
        "curve_groups_with_strict_distinct_side_states": 12288,
        "transition_pattern_count": 34,
        "transition_patterns_sha256": "2fa0e74db4c550aaafb254de5ed952b8f87cda024a385c630d828bf0aa3a0403",
        "curve_strip_rows_sha256": "6c495645d32564f0c4f17b6b933c3549f311e7d910a6c60322cd2fdc2e20eb44",
        "descriptor_full_window_coverage_sha256": "109a234fa70c85c23a5037c5028d22ed1b80c61b70cc39c5c08c5fb82b88556d",
    }.items():
        if curves.get(key) != expected:
            errors.append(f"curve stratification mismatch: {key}")
    if curves.get("source_box_multiplicity_counts") != {
        "1": 11280,
        "2": 1008,
    }:
        errors.append("curve source-box multiplicity mismatch")
    try:
        if curves["analytic_transition_curve_count"] * curves[
            "full_window_strips_per_curve"
        ] != curves["curve_strip_group_count"]:
            errors.append("curve-strip coverage identity mismatch")
        if matching["boxes_meeting_no_physical_transition_curve"] + matching[
            "boxes_meeting_exactly_one_physical_transition_curve"
        ] != residual["residual_box_count_before_stratification"]:
            errors.append("residual-box matching partition mismatch")
    except (KeyError, TypeError):
        errors.append("invalid finite partition ledger")

    limits = result.get("scope_limits", {})
    for key in (
        "active_sheet_first_visibility_stratification_complete",
        "active_sheet_miss_owner_stratification_complete",
        "all_residual_boxes_have_constant_or_two_sided_strict_labels",
        "physical_transition_curves_retained_as_dq_faces",
    ):
        if limits.get(key) is not True:
            errors.append(f"missing certified scope flag: {key}")
    for key in (
        "maximal_connected_event_rows",
        "chart_seams_quotiented",
        "global_coarea_current_assembled",
        "global_dq",
        "global_scalar_matching",
    ):
        if limits.get(key) is not False:
            errors.append(f"unsupported completion flag: {key}")

    verdict = data.get("verdict", {})
    if verdict.get("active_first_visibility_stratification") != "CERTIFIED":
        errors.append("first-visibility verdict mismatch")
    if verdict.get("active_miss_owner_stratification") != "CERTIFIED":
        errors.append("miss-owner verdict mismatch")
    if verdict.get("remaining_two_dimensional_unresolved_parameter_area") != "ZERO":
        errors.append("two-dimensional residual verdict mismatch")
    if verdict.get("maximal_connected_event_rows") != "NOT_CERTIFIED":
        errors.append("maximal-row verdict must fail-close")
    if verdict.get("global_DQ_and_scalar_matching") != "NOT_CERTIFIED":
        errors.append("global-DQ verdict must fail-close")
    return errors


def check_replay(data: dict[str, Any]) -> list[str]:
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    try:
        import cm2_gate3_first_miss_stratification_cert as cert
        actual = cert.certify()
    except Exception as exc:
        return [f"certificate replay failed: {exc}"]
    return [] if data.get("result") == actual else ["full certificate replay mismatch"]


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
        print("GATE3_FIRST_MISS_STRATIFICATION_INTEGRITY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1
    if args.self_test:
        tampered = copy.deepcopy(data)
        tampered["result"]["remaining_two_dimensional_unresolved_parameter_area"] = "1"
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (residual-area tamper accepted)")
            return 1
        tampered = copy.deepcopy(data)
        tampered["result"]["scope_limits"]["global_dq"] = True
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (unsupported global DQ accepted)")
            return 1
        print("SELF_TEST: PASS")
        print("  residual-area tamper rejected")
        print("  unsupported global DQ rejected")
        return 0
    print("GATE3_ACTIVE_FIRST_VISIBILITY_STRATIFICATION: CERTIFIED")
    print("GATE3_ACTIVE_MISS_OWNER_STRATIFICATION: CERTIFIED")
    print("GATE3_TWO_DIMENSIONAL_UNRESOLVED_PARAMETER_AREA: ZERO")
    if args.integrity_only:
        print("GATE3_FIRST_MISS_STRATIFICATION_INTEGRITY: PASS")
        return 0
    print("GATE3_MAXIMAL_ROWS_GLOBAL_DQ_SCALAR_MATCHING: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
