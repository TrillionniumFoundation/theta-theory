#!/usr/bin/env python3
"""Fail-closed verifier for the fifteenth Gate-3 deep scaled frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate3.deep-scaled-resultant-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate3.deep-scaled-resultant-frontier.v1"
DEFAULT_MANIFEST = HERE / "cm2-gate3-deep-scaled-resultant-frontier-manifest-2026-07-16.json"
CERTIFICATE = HERE / "cm2_gate3_deep_scaled_resultant_frontier_cert.py"
EXPECTED_INTERNAL_DIGEST = "ff021b4409974baa95e0928092cdbfc77365513f840946465b22aa474b20d8ba"


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
        "cm2-gate3-endpoint-scaled-resultant-frontier-manifest-2026-07-16.json",
        "cm2_gate3_endpoint_scaled_resultant_frontier_cert.py",
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

    old = result.get("old_source_terminal_coordinate_ledger", {})
    for key, expected in {
        "source_tagged_record_count": 1536,
        "source_tagged_row_count": 24,
        "canonical_source_band_count": 32,
        "closed_v1_record_count": 24,
        "coordinatewise_containment_certified_for_every_record": True,
        "old_records_equal_canonical_cells": True,
        "targeted_terminal_record_ledger_sha256": "6958598bb8c8e4d7a3b80c4c0674d7cd96c8e196905695f155ea5eb082d458e2",
    }.items():
        if old.get(key) != expected:
            errors.append(f"old source ledger mismatch: {key}")
    deep = result.get("deep_source_terminal_coordinate_ledger", {})
    for key, expected in {
        "source_tagged_record_count": 2048,
        "source_tagged_row_count": 16,
        "canonical_source_band_count": 32,
        "closed_v1_record_count": 16,
        "coordinatewise_containment_certified_for_every_record": True,
        "deep_records_contained_in_canonical_cells": True,
        "deep_record_to_unique_old_parent_containment_certified": True,
        "old_parent_with_deep_source_children_count": 1024,
        "deep_source_children_per_such_old_parent": 2,
        "targeted_terminal_record_ledger_sha256": "8cce8a761c621abab3e6666aa2a2745a06ae97cdfaa236367a6319c4ccc90efc",
    }.items():
        if deep.get(key) != expected:
            errors.append(f"deep source ledger mismatch: {key}")

    reclassified = result.get("deep_source_downstream_reclassification", {})
    for key, expected in {
        "input_deep_source_tagged_record_count": 2048,
        "classification_counts": {"immutable_owner_component": 2048},
        "positive_width_terminal_retained_count": 0,
        "all_deep_source_tagged_records_downstream_classified_without_positive_width_terminal": True,
        "uniform_source_terminal_width_before_override": "1/128",
        "classified_record_ledger_sha256": "2bf469f35f5ee515614321c52668e9bc42d57af4010e8d9ad1663d628c1d3f05",
    }.items():
        if reclassified.get(key) != expected:
            errors.append(f"source reclassification mismatch: {key}")

    critical = result.get("critical_resultant_refinement", {})
    for key, expected in {
        "critical_terminal_box_count": 12,
        "coarse_possible_critical_candidate_count": 444,
        "refinement_audit_call_count": 3196,
        "Delta_strict_excluded_leaf_count": 932,
        "transverse_candidate_graph_leaf_count": 888,
        "transverse_candidate_graph_normalized_slope_sum_upper": 888,
        "regular_fold_leaf_count": 0,
        "unresolved_critical_leaf_count": 0,
        "all_coarse_critical_boxes_replaced_by_Delta_exclusions_or_strict_dt_graphs": True,
        "no_simultaneous_Delta_Delta_t_zero_on_the_twelve_boxes": True,
        "complete_refinement_ledger_sha256": "9ff1368a866fe7805c5037542b05683885d2f23e93c66dc305ded845c103bb62",
    }.items():
        if critical.get(key) != expected:
            errors.append(f"critical refinement mismatch: {key}")

    frontier = result.get("updated_outer_frontier", {})
    for key, expected in {
        "positive_width_terminal_reason_counts": {"interval_geometry_exception": 151500},
        "positive_width_terminal_box_count": 151500,
        "positive_width_terminal_nonphysical_parameter_area_upper_cover": "37875/65536",
        "uniform_fixed_s_positive_t_width_outer": "595/1024",
        "source_terminal_width_removed_after_exact_containment_and_reclassification": "1/128",
        "critical_positive_width_terminal_boxes_removed_after_exhaustive_refinement": 12,
        "zero_intercept_complete_future_boundary": False,
    }.items():
        if frontier.get(key) != expected:
            errors.append(f"frontier mismatch: {key}")

    graphs = result.get("expanded_candidate_graph_atlas", {})
    for key, expected in {
        "frozen_conditionally_physical_first_graph_chart_count": 41344,
        "frozen_nonempty_physical_first_root_arc_count": 11678,
        "frozen_untyped_candidate_graph_chart_count": 164,
        "new_untyped_transverse_candidate_graph_leaf_count": 888,
        "combined_untyped_candidate_graph_chart_count": 1052,
        "safe_maximum_candidate_graph_charts_on_one_fixed_s_slice": 1480,
        "safe_maximum_candidate_graph_normalized_slope_sum_on_one_fixed_s_slice": 52292,
        "safe_uniform_fixed_s_actual_candidate_zero_set_Leb_Z_linear_coefficient": "2960",
        "safe_uniform_fixed_s_actual_candidate_zero_set_row_law_Z_linear_coefficient": "74592",
        "new_critical_graphs_are_physical_first_typed": False,
        "partial_genuine_physical_marked_current_TV_upper_unchanged": "518152320",
    }.items():
        if graphs.get(key) != expected:
            errors.append(f"graph atlas mismatch: {key}")

    tech = result.get("latest_technology_applicability_audit", {})
    for key, expected in {
        "arxiv_id": "2607.13785v1",
        "direct_lemma_for_twelve_billiard_resultant_boxes": False,
        "direct_lemma_for_interval_physical_first_owner_typing": False,
        "strategy_analogy_only": True,
        "used_to_remove_or_reclassify_any_box": False,
    }.items():
        if tech.get(key) != expected:
            errors.append(f"technology audit mismatch: {key}")
    if len(tech.get("fatal_hypothesis_mismatches", [])) != 6:
        errors.append("technology mismatch ledger malformed")

    scope = result.get("scope_limits", {})
    required_true = {
        "old_source_record_coordinatewise_containment",
        "deep_source_record_coordinatewise_containment",
        "deep_source_downstream_immutable_reclassification",
        "all_twelve_coarse_critical_boxes_resolved_to_transverse_graph_atlas",
        "all_simultaneous_Delta_Delta_t_critical_zeros_excluded",
    }
    required_false = {
        "interval_geometry_exception_boxes_resolved",
        "all_candidate_graph_charts_typed_physical_first",
        "complete_side_owner_current", "strong_component_restriction_DQ",
        "branch_record_MT_DQ", "physical_FACE_2CUT", "physical_FACE_TIME",
        "gate3_certified",
    }
    if any(scope.get(key) is not True for key in required_true):
        errors.append("positive scope mismatch")
    if any(scope.get(key) is not False for key in required_false):
        errors.append("fail-closed scope mismatch")
    if len(result.get("exact_remaining_blockers", [])) != 4:
        errors.append("blocker ledger mismatch")

    expected_verdict = {
        "source_endpoint_containment_and_downstream_reclassification": "CERTIFIED",
        "critical_resultant_boxes_resolved": "CERTIFIED",
        "complete_side_owner_current": "NOT_CERTIFIED",
        "strong_DQ_MT_DQ_FACE": "NOT_CERTIFIED",
        "gate3": "NOT_CERTIFIED",
    }
    if data.get("verdict") != expected_verdict:
        errors.append("verdict mismatch")
    return errors


def replay_result() -> dict[str, Any]:
    import cm2_gate3_deep_scaled_resultant_frontier_cert as cert
    return cert.build_result()


def self_test(data: dict[str, Any]) -> list[str]:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("old count", lambda x: x["result"]["old_source_terminal_coordinate_ledger"].__setitem__("source_tagged_record_count", 1535)),
        ("old containment", lambda x: x["result"]["old_source_terminal_coordinate_ledger"].__setitem__("old_records_equal_canonical_cells", False)),
        ("deep count", lambda x: x["result"]["deep_source_terminal_coordinate_ledger"].__setitem__("source_tagged_record_count", 2047)),
        ("parent link", lambda x: x["result"]["deep_source_terminal_coordinate_ledger"].__setitem__("deep_record_to_unique_old_parent_containment_certified", False)),
        ("source terminal", lambda x: x["result"]["deep_source_downstream_reclassification"].__setitem__("positive_width_terminal_retained_count", 1)),
        ("source class", lambda x: x["result"]["deep_source_downstream_reclassification"].__setitem__("classification_counts", {"immutable_owner_component": 2047})),
        ("critical boxes", lambda x: x["result"]["critical_resultant_refinement"].__setitem__("critical_terminal_box_count", 11)),
        ("critical candidates", lambda x: x["result"]["critical_resultant_refinement"].__setitem__("coarse_possible_critical_candidate_count", 443)),
        ("critical unresolved", lambda x: x["result"]["critical_resultant_refinement"].__setitem__("unresolved_critical_leaf_count", 1)),
        ("critical overcount", lambda x: x["result"]["critical_resultant_refinement"].__setitem__("transverse_candidate_graph_leaf_count", 887)),
        ("terminal count", lambda x: x["result"]["updated_outer_frontier"].__setitem__("positive_width_terminal_box_count", 151499)),
        ("width overclaim", lambda x: x["result"]["updated_outer_frontier"].__setitem__("uniform_fixed_s_positive_t_width_outer", "0")),
        ("untyped", lambda x: x["result"]["expanded_candidate_graph_atlas"].__setitem__("combined_untyped_candidate_graph_chart_count", 0)),
        ("candidate Z", lambda x: x["result"]["expanded_candidate_graph_atlas"].__setitem__("safe_uniform_fixed_s_actual_candidate_zero_set_Leb_Z_linear_coefficient", "0")),
        ("tech bridge", lambda x: x["result"]["latest_technology_applicability_audit"].__setitem__("direct_lemma_for_twelve_billiard_resultant_boxes", True)),
        ("tech use", lambda x: x["result"]["latest_technology_applicability_audit"].__setitem__("used_to_remove_or_reclassify_any_box", True)),
        ("current overclaim", lambda x: x["result"]["scope_limits"].__setitem__("complete_side_owner_current", True)),
        ("gate overclaim", lambda x: x["result"]["scope_limits"].__setitem__("gate3_certified", True)),
        ("verdict overclaim", lambda x: x["verdict"].__setitem__("gate3", "CERTIFIED")),
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
        print("SELF-TEST: PASS 19/19")
    if args.integrity_only or args.replay or args.self_test:
        return 0
    print("complete_side_owner_current: NOT_CERTIFIED")
    print("strong_DQ_MT_DQ_FACE: NOT_CERTIFIED")
    print("gate3: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    sys.exit(main())
