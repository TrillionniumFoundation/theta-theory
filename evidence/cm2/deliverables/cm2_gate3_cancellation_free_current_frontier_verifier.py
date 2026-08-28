#!/usr/bin/env python3
"""Fail-closed verifier for the sixteenth Gate-3 cancellation-free layer."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate3.cancellation-free-current-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate3.cancellation-free-current-frontier.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate3-cancellation-free-current-frontier-manifest-2026-07-16.json"
)
CERTIFICATE = HERE / "cm2_gate3_cancellation_free_current_frontier_cert.py"
EXPECTED_INTERNAL_DIGEST = "30c2c5cfb23d4483825b896cf964e62305a043ae4e2aab1be22d00723c30e08e"


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")).hexdigest()


def refresh_digest(result: dict[str, Any]) -> None:
    result.pop("internal_replay_digest", None)
    result["internal_replay_digest"] = canonical_digest(result)


def check_structure(data: Any, *, enforce_hashes: bool = True) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["manifest is not an object"]
    if data.get("schema") != SCHEMA:
        errors.append("schema mismatch")
    if enforce_hashes:
        if data.get("certificate_sha256") != sha256_path(CERTIFICATE):
            errors.append("certificate hash mismatch")
        if data.get("verifier_sha256") != sha256_path(Path(__file__)):
            errors.append("verifier hash mismatch")
    dependencies = data.get("dependencies")
    expected_dependencies = {
        "cm2-gate3-deep-scaled-resultant-frontier-manifest-2026-07-16.json",
        "cm2_gate3_deep_scaled_resultant_frontier_cert.py",
        "cm2_gate3_physical_first_unresolved_frontier_cert.py",
        "cm2_gate3_finite_s_future_singularity_outer_atlas_cert.py",
    }
    if not isinstance(dependencies, dict) or set(dependencies) != expected_dependencies:
        errors.append("dependency ledger mismatch")
    elif enforce_hashes:
        for name, digest in dependencies.items():
            path = HERE / name
            if not path.is_file() or sha256_path(path) != digest:
                errors.append(f"dependency hash mismatch: {name}")

    result = data.get("result")
    if not isinstance(result, dict):
        return errors + ["result missing"]
    if result.get("schema") != RESULT_SCHEMA:
        errors.append("result schema mismatch")
    payload = copy.deepcopy(result)
    digest = payload.pop("internal_replay_digest", None)
    if digest != canonical_digest(payload) or digest != EXPECTED_INTERNAL_DIGEST:
        errors.append("internal replay digest mismatch")

    raw = result.get("raw_interval_exception_reconstruction", {})
    for key, expected in {
        "deep_t_cell_count": 2048,
        "deep_parameter_cell_count": 128,
        "searched_endpoint_t_cells_per_active_row": 512,
        "active_matching_later_miss_endpoint_row_count": 32,
        "distinct_raw_sqrt_miss_delta_exception_leaf_count": 151500,
        "equals_frozen_aggregate_and_therefore_exhausts_it": True,
        "raw_exception_coordinate_ledger_sha256": "31397ea96a50bee7209580a04b505f7db5af7ff0420ecb53f4115a1c97e5f3db",
        "per_row_summary_ledger_sha256": "876cddac8b15b8656805e6db9b261db294a1d4a5b56406dc0fac5b009f81462a",
    }.items():
        if raw.get(key) != expected:
            errors.append(f"raw reconstruction mismatch: {key}")
    if raw.get("per_row_summary_count") != 64:
        errors.append("per-row summary count mismatch")

    replay = result.get("cancellation_free_downstream_replay", {})
    expected_replay = {
        # Filled with immutable clean-replay constants below.
        "classification_counts": {"immutable_owner_component": 156108},
        "final_refined_leaf_count": 156108,
        "rescued_refinement_call_count": 160716,
        "positive_width_terminal_retained_count": 0,
        "all_151500_boxes_have_strict_factor_and_root_gap_witnesses": True,
        "maximum_additional_t_depth": 6,
        "maximum_additional_parameter_depth": 2,
        "maximum_t_depth_reached": 8,
        "maximum_parameter_depth_reached": 4,
        "classified_record_ledger_sha256": "1d076f8cca4d43345ce248debeafc8af7183d1f5753490c421cfe56e35a3f25a",
        "retained_record_ledger_sha256": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945",
    }
    for key, expected in expected_replay.items():
        if replay.get(key) != expected:
            errors.append(f"downstream replay mismatch: {key}")
    if replay.get("immutable_owner_leaf_counts") != {
        "G[-1,0]": 2304,
        "G[0,-1]": 2560,
        "G[0,0]": 14523,
        "G[0,1]": 17083,
        "G[1,0]": 16827,
        "G[1,1]": 14523,
        "W[-1,-1]": 22072,
        "W[-1,0]": 22072,
        "W[0,-1]": 22072,
        "W[0,0]": 22072,
    }:
        errors.append("immutable owner count ledger mismatch")

    identity = result.get("exact_cancellation_free_identity_audit", {})
    for key, expected in {
        "active_matching_later_miss_endpoint_row_count": 32,
        "deduced_endpoint_identity": "w(0,s)=epsilon_other*r_m",
        "rounded_orientation_guard_count": 32,
        "rounded_orientation_guard_ledger_sha256": "102697a8634631d56d68231adfbb19bf6142447b7ee95ddeeecb576ad2cdb8fc",
        "exact_identity_is_descriptor_algebra_not_numerical_zero_inference": True,
    }.items():
        if identity.get(key) != expected:
            errors.append(f"identity audit mismatch: {key}")

    frontier = result.get("updated_outer_frontier", {})
    for key, expected in {
        "frozen_positive_width_interval_geometry_box_count": 151500,
        "frozen_uniform_fixed_s_positive_t_width_outer": "595/1024",
        "remaining_positive_width_terminal_box_count": 0,
        "remaining_positive_width_terminal_reason_counts": {},
        "uniform_fixed_s_positive_t_width_outer": "0",
        "zero_intercept_complete_future_candidate_boundary": True,
        "no_parameter_area_is_relabelled_as_physical_mass": True,
    }.items():
        if frontier.get(key) != expected:
            errors.append(f"updated frontier mismatch: {key}")

    graphs = result.get("post_replay_candidate_graph_and_current_frontier", {})
    for key, expected in {
        "new_conditionally_physical_first_graph_count": 0,
        "new_untyped_candidate_graph_count": 0,
        "frozen_conditionally_physical_first_graph_chart_count": 41344,
        "frozen_nonempty_physical_first_root_arc_count": 11678,
        "remaining_untyped_candidate_graph_chart_count": 1052,
        "safe_maximum_candidate_graph_charts_on_one_fixed_s_slice": 1480,
        "safe_maximum_candidate_graph_normalized_slope_sum_on_one_fixed_s_slice": 52292,
        "partial_genuine_physical_marked_current_TV_upper": "518152320",
        "complete_side_owner_current_still_blocked_only_by_graph_typing_and_assembly": True,
    }.items():
        if graphs.get(key) != expected:
            errors.append(f"graph/current frontier mismatch: {key}")

    branch = result.get("resolved_interval_common_branch_record", {})
    for key, expected in {
        "input_exception_box_count": 151500,
        "final_uniform_owner_leaf_count": 156108,
        "analytic_future_face_graph_count_contributed_by_this_class": 0,
        "marked_current_TV_contribution_by_this_class": "0",
        "physical_FACE_2CUT_contribution_by_this_class": "0",
        "physical_FACE_TIME_contribution_by_this_class": "0",
        "artificial_refinement_edges_are_not_physical_faces": True,
        "common_owner_branch_record_complete_for_resolved_interval_class": True,
        "global_strong_DQ_or_MT_DQ_not_inferred_from_local_immutability": True,
    }.items():
        if branch.get(key) != expected:
            errors.append(f"resolved branch record mismatch: {key}")

    scope = result.get("scope_limits", {})
    if scope.get("all_interval_geometry_exception_boxes_resolved") is not True:
        errors.append("interval frontier closure mismatch")
    if scope.get("resolved_interval_common_owner_branch_record") is not True:
        errors.append("resolved branch scope mismatch")
    if scope.get("resolved_interval_class_adds_no_physical_current_or_FACE") is not True:
        errors.append("resolved current/FACE scope mismatch")
    required_false = {
        "all_candidate_graph_charts_typed_physical_first",
        "complete_side_owner_current",
        "strong_component_restriction_DQ",
        "branch_record_MT_DQ",
        "physical_FACE_2CUT",
        "physical_FACE_TIME",
        "gate3_certified",
    }
    if any(scope.get(key) is not False for key in required_false):
        errors.append("fail-closed scope mismatch")
    if len(result.get("exact_remaining_blockers", [])) != 3:
        errors.append("blocker ledger mismatch")

    expected_verdict = {
        "cancellation_free_interval_frontier": "CERTIFIED",
        "complete_side_owner_current": "NOT_CERTIFIED",
        "strong_DQ_MT_DQ_FACE": "NOT_CERTIFIED",
        "gate3": "NOT_CERTIFIED",
    }
    if data.get("verdict") != expected_verdict:
        errors.append("verdict mismatch")
    return errors


def replay_result() -> dict[str, Any]:
    import cm2_gate3_cancellation_free_current_frontier_cert as cert
    return cert.build_result()


def self_test(data: dict[str, Any]) -> list[str]:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("raw count", lambda x: x["result"]["raw_interval_exception_reconstruction"].__setitem__("distinct_raw_sqrt_miss_delta_exception_leaf_count", 151499)),
        ("active rows", lambda x: x["result"]["raw_interval_exception_reconstruction"].__setitem__("active_matching_later_miss_endpoint_row_count", 31)),
        ("exhaustion", lambda x: x["result"]["raw_interval_exception_reconstruction"].__setitem__("equals_frozen_aggregate_and_therefore_exhausts_it", False)),
        ("collar", lambda x: x["result"]["raw_interval_exception_reconstruction"].__setitem__("searched_endpoint_t_cells_per_active_row", 511)),
        ("classification", lambda x: x["result"]["cancellation_free_downstream_replay"].__setitem__("classification_counts", {})),
        ("leaf count", lambda x: x["result"]["cancellation_free_downstream_replay"].__setitem__("final_refined_leaf_count", 156107)),
        ("calls", lambda x: x["result"]["cancellation_free_downstream_replay"].__setitem__("rescued_refinement_call_count", 160715)),
        ("terminal", lambda x: x["result"]["cancellation_free_downstream_replay"].__setitem__("positive_width_terminal_retained_count", 1)),
        ("factor", lambda x: x["result"]["cancellation_free_downstream_replay"].__setitem__("all_151500_boxes_have_strict_factor_and_root_gap_witnesses", False)),
        ("t budget", lambda x: x["result"]["cancellation_free_downstream_replay"].__setitem__("maximum_additional_t_depth", 5)),
        ("v budget", lambda x: x["result"]["cancellation_free_downstream_replay"].__setitem__("maximum_additional_parameter_depth", 1)),
        ("frontier", lambda x: x["result"]["scope_limits"].__setitem__("all_interval_geometry_exception_boxes_resolved", False)),
        ("zero width", lambda x: x["result"]["updated_outer_frontier"].__setitem__("uniform_fixed_s_positive_t_width_outer", "1/2048")),
        ("untyped", lambda x: x["result"]["post_replay_candidate_graph_and_current_frontier"].__setitem__("remaining_untyped_candidate_graph_chart_count", 0)),
        ("branch records", lambda x: x["result"]["resolved_interval_common_branch_record"].__setitem__("final_uniform_owner_leaf_count", 156107)),
        ("branch current", lambda x: x["result"]["resolved_interval_common_branch_record"].__setitem__("marked_current_TV_contribution_by_this_class", "1")),
        ("current overclaim", lambda x: x["result"]["scope_limits"].__setitem__("complete_side_owner_current", True)),
        ("DQ overclaim", lambda x: x["result"]["scope_limits"].__setitem__("strong_component_restriction_DQ", True)),
        ("MT overclaim", lambda x: x["result"]["scope_limits"].__setitem__("branch_record_MT_DQ", True)),
        ("FACE2 overclaim", lambda x: x["result"]["scope_limits"].__setitem__("physical_FACE_2CUT", True)),
        ("FACET overclaim", lambda x: x["result"]["scope_limits"].__setitem__("physical_FACE_TIME", True)),
        ("gate overclaim", lambda x: x["result"]["scope_limits"].__setitem__("gate3_certified", True)),
        ("verdict frontier", lambda x: x["verdict"].__setitem__("cancellation_free_interval_frontier", "NOT_CERTIFIED")),
        ("verdict current", lambda x: x["verdict"].__setitem__("complete_side_owner_current", "CERTIFIED")),
        ("verdict gate", lambda x: x["verdict"].__setitem__("gate3", "CERTIFIED")),
    ]
    failures = []
    for name, mutate in mutations:
        trial = copy.deepcopy(data)
        mutate(trial)
        refresh_digest(trial["result"])
        if not check_structure(trial, enforce_hashes=False):
            failures.append(name)
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    errors = check_structure(data)
    if errors:
        print("INTEGRITY: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    if args.replay:
        if replay_result() != data["result"]:
            print("REPLAY: FAIL")
            return 1
        print("REPLAY: PASS")
    print("INTEGRITY: PASS")
    if args.self_test:
        failures = self_test(data)
        if failures:
            print("SELF-TEST: FAIL " + ", ".join(failures))
            return 1
        print("SELF-TEST: PASS 25/25")
    if args.integrity_only or args.replay or args.self_test:
        return 0
    print("complete_side_owner_current: NOT_CERTIFIED")
    print("strong_DQ_MT_DQ_FACE: NOT_CERTIFIED")
    print("gate3: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    sys.exit(main())
