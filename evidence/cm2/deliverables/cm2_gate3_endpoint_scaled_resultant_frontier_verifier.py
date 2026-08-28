#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-3 endpoint/resultant frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate3.endpoint-scaled-resultant-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate3.endpoint-scaled-resultant-frontier.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate3-endpoint-scaled-resultant-frontier-manifest-2026-07-16.json"
)
CERTIFICATE = HERE / "cm2_gate3_endpoint_scaled_resultant_frontier_cert.py"


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def refresh_digest(result: dict[str, Any]) -> None:
    result.pop("internal_replay_digest", None)
    result["internal_replay_digest"] = canonical_digest(result)


def check_structure(data: Any, *, enforce_file_hashes: bool = True) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["manifest is not an object"]
    if data.get("schema") != SCHEMA:
        errors.append("schema mismatch")
    if enforce_file_hashes:
        if data.get("certificate_sha256") != sha256_path(CERTIFICATE):
            errors.append("certificate hash mismatch")
        if data.get("verifier_sha256") != sha256_path(Path(__file__)):
            errors.append("verifier hash mismatch")
    dependencies = data.get("dependencies")
    if not isinstance(dependencies, dict) or set(dependencies) != {
        "cm2-gate3-physical-first-unresolved-frontier-manifest-2026-07-16.json",
        "cm2_gate3_physical_first_unresolved_frontier_cert.py",
    }:
        errors.append("dependency ledger mismatch")
    elif enforce_file_hashes:
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
    if digest != canonical_digest(payload):
        errors.append("internal replay digest mismatch")

    provenance = result.get("provenance", {})
    frozen_manifest = HERE / (
        "cm2-gate3-physical-first-unresolved-frontier-manifest-2026-07-16.json"
    )
    frozen_cert = HERE / "cm2_gate3_physical_first_unresolved_frontier_cert.py"
    if provenance.get("frozen_physical_first_manifest_sha256") != sha256_path(
        frozen_manifest
    ):
        errors.append("frozen manifest provenance mismatch")
    if provenance.get("frozen_physical_first_certificate_sha256") != sha256_path(
        frozen_cert
    ):
        errors.append("frozen certificate provenance mismatch")

    endpoint = result.get("endpoint_scaled_source_incidence", {})
    for key, expected in {
        "canonical_endpoint_band_parameter_cell_count": 1536,
        "frozen_source_tagged_terminal_count_for_comparison_only": 1536,
        "canonical_source_grazing_row_count": 24,
        "parameter_cells_per_source_row": 64,
        "terminal_t_width_per_source_row": "1/1024",
        "canonical_endpoint_band_fixed_s_width": "3/128",
        "closed_v1_endpoint_included": True,
        "canonical_endpoint_bands_have_strictly_positive_source_cp": True,
        "frozen_terminal_record_to_endpoint_band_containment_certified": False,
        "frozen_terminal_boxes_removed_or_reclassified": False,
    }.items():
        if endpoint.get(key) != expected:
            errors.append(f"endpoint field mismatch: {key}")
    indices = endpoint.get("source_incidence_row_indices")
    if not isinstance(indices, list) or len(indices) != 24 or len(set(indices)) != 24:
        errors.append("endpoint row ledger mismatch")
    if not isinstance(endpoint.get("endpoint_scaled_record_ledger_sha256"), str):
        errors.append("endpoint record digest missing")

    resultant = result.get("critical_resultant_reduction", {})
    for key, expected in {
        "candidate_discriminant": "Delta=r^2-w^2",
        "critical_zero_equations": ["w=sigma*r", "w_t=0"],
        "critical_jacobian_determinant": "-4*r^2*w_s*w_tt",
        "coefficient_ledger": {"r^2*w_s*w_tt": -4},
        "algebraic_reduction_certified": True,
        "interval_nonvanishing_on_all_critical_boxes_certified": False,
        "absence_of_critical_junctions_certified": False,
    }.items():
        if resultant.get(key) != expected:
            errors.append(f"resultant field mismatch: {key}")

    deep = result.get("deeper_selective_frontier", {})
    for key, expected in {
        "selective_terminal_t_depth": 6,
        "selective_terminal_parameter_depth": 4,
        "terminal_reason_counts": {
            "candidate_zero_with_dt_containing_zero": 12,
            "interval_geometry_exception": 151500,
            "source_cp_not_strict": 2048,
        },
        "terminal_reason_nonphysical_parameter_areas": {
            "candidate_zero_with_dt_containing_zero": "3/65536",
            "interval_geometry_exception": "37875/65536",
            "source_cp_not_strict": "1/128",
        },
        "uniform_fixed_s_terminal_reason_t_width_outers": {
            "candidate_zero_with_dt_containing_zero": "1/1024",
            "interval_geometry_exception": "595/1024",
            "source_cp_not_strict": "1/128",
        },
        "uniform_fixed_s_terminal_positive_t_width_outer": "603/1024",
        "conditionally_physical_first_graph_chart_count": 41344,
        "nonempty_physical_first_root_arc_count": 11678,
        "untyped_candidate_graph_chart_count": 164,
        "untyped_graph_failure_counts": {
            "additional_ambiguous_candidate_may_precede": 60,
            "untyped_candidate_graph_cover": 104,
        },
        "total_audit_call_count": 1722936,
        "partial_current_definition": (
            "sum_i (partial_s_Delta_i/abs(partial_t_Delta_i)) "
            "rho_e(t_i,s) "
            "[delta_grazing_hit_i-delta_first_miss_side_owner_i]"
        ),
        "graph_velocity_current_orientation_identity": (
            "partial_s_Delta/abs(partial_t_Delta)="
            "-sign(partial_t_Delta)*dt_graph/ds"
        ),
        "closed_final_v_endpoint_explicitly_included_in_all_sweeps": True,
    }.items():
        if deep.get(key) != expected:
            errors.append(f"deep replay mismatch: {key}")
    dt_signs = deep.get("conditionally_physical_first_dt_sign_counts", {})
    if (
        set(dt_signs) != {"-1", "1"}
        or sum(dt_signs.values()) != 41344
        or min(dt_signs.values()) <= 0
    ):
        errors.append("deep current orientation ledger mismatch")
    try:
        slope = deep["maximum_normalized_absolute_root_slope_sum_on_one_fixed_s_slice"]
        tv = Fraction(deep["partial_genuine_physical_marked_current_TV_upper"])
        if tv != 2 * Fraction(126, 5) * 200 * slope:
            errors.append("deep partial-current TV arithmetic mismatch")
    except (KeyError, TypeError, ValueError, ZeroDivisionError):
        errors.append("deep partial-current fields malformed")
    for key in (
        "complete_replay_sha256",
        "ordered_row_summary_ledger_sha256",
    ):
        if not isinstance(deep.get(key), str) or len(deep[key]) != 64:
            errors.append(f"deep digest malformed: {key}")

    adjusted = result.get("retained_fail_closed_terminal_frontier", {})
    for key, expected in {
        "frozen_thirteenth_terminal_box_count": 93080,
        "frozen_thirteenth_source_tagged_terminal_count_retained": 1536,
        "deep_replay_source_tagged_descendant_count_pending_downstream_reclassification": 2048,
        "deep_replay_terminal_box_count_retained_fail_closed": 153560,
        "deep_replay_terminal_reason_counts_retained_fail_closed": {
            "candidate_zero_with_dt_containing_zero": 12,
            "interval_geometry_exception": 151500,
            "source_cp_not_strict": 2048,
        },
        "frozen_uniform_fixed_s_positive_t_width_outer": "373/256",
        "raw_deep_replay_uniform_fixed_s_positive_t_width_outer": "603/1024",
        "deep_replay_uniform_fixed_s_positive_t_width_outer_retained_fail_closed": "603/1024",
        "parent_to_deep_source_descendant_containment_ledger_certified": False,
        "deep_source_descendant_downstream_miss_root_owner_classification_certified": False,
        "zero_intercept": False,
    }.items():
        if adjusted.get(key) != expected:
            errors.append(f"adjusted frontier mismatch: {key}")

    scope = result.get("scope_limits", {})
    required_true = {
        "canonical_endpoint_band_source_cp_positivity",
        "canonical_endpoint_band_coordinate_regular_on_full_parameter_window",
        "critical_resultant_algebraic_reduction",
    }
    required_false = {
        "all_frozen_source_incidence_terminal_boxes_resolved",
        "frozen_terminal_record_to_endpoint_band_containment_certified",
        "all_deeper_source_tagged_descendants_covered_and_reclassified",
        "critical_resultant_interval_nonvanishing",
        "interval_geometry_exception_boxes_resolved",
        "critical_root_boxes_resolved",
        "all_candidate_graph_charts_typed",
        "complete_side_owner_current",
        "strong_component_restriction_DQ",
        "branch_record_MT_DQ",
        "physical_FACE_2CUT",
        "physical_FACE_TIME",
        "gate3_certified",
    }
    if any(scope.get(key) is not True for key in required_true):
        errors.append("positive scope flag mismatch")
    if any(scope.get(key) is not False for key in required_false):
        errors.append("fail-closed scope flag mismatch")
    expected_blockers = [
        "resolve the 151,500 deeper-replay interval-geometry boxes in analogous cancellation-free miss/root-gap coordinates",
        "interval-certify w_s*w_tt nonvanishing or isolate every zero of the critical resultant on the 12 remaining critical boxes",
        "type the 164 remaining candidate graph charts by a unique miss-side owner",
        "freeze coordinatewise containment for the 1,536 frozen source-tagged records and the 2,048 deeper descendants, then continue downstream miss-delta/root-gap/candidate/owner classification",
        "assemble the complete side-owner current with coefficient partial_s_Delta/abs(partial_t_Delta)",
        "prove strong component restriction DQ, branch-record MT_DQ, FACE_2CUT, and FACE_TIME",
    ]
    blockers = result.get("exact_remaining_blockers")
    if blockers != expected_blockers:
        errors.append("remaining blocker ledger mismatch")

    verdict = data.get("verdict")
    expected_verdict = {
        "canonical_endpoint_band_source_cp_positivity": "CERTIFIED",
        "critical_resultant_algebraic_reduction": "CERTIFIED",
        "complete_side_owner_current": "NOT_CERTIFIED",
        "strong_DQ_MT_DQ_FACE": "NOT_CERTIFIED",
        "gate3": "NOT_CERTIFIED",
    }
    if verdict != expected_verdict:
        errors.append("verdict mismatch")
    return errors


def load_manifest(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def replay_result() -> dict[str, Any]:
    import cm2_gate3_endpoint_scaled_resultant_frontier_cert as cert
    return cert.build_result()


def self_test(data: dict[str, Any]) -> list[str]:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("endpoint count", lambda x: x["result"]["endpoint_scaled_source_incidence"].__setitem__("canonical_endpoint_band_parameter_cell_count", 1535)),
        ("endpoint width", lambda x: x["result"]["endpoint_scaled_source_incidence"].__setitem__("canonical_endpoint_band_fixed_s_width", "1/128")),
        ("endpoint positivity", lambda x: x["result"]["endpoint_scaled_source_incidence"].__setitem__("canonical_endpoint_bands_have_strictly_positive_source_cp", False)),
        ("containment overclaim", lambda x: x["result"]["endpoint_scaled_source_incidence"].__setitem__("frozen_terminal_record_to_endpoint_band_containment_certified", True)),
        ("resultant coefficient", lambda x: x["result"]["critical_resultant_reduction"].__setitem__("coefficient_ledger", {"r^2*w_s*w_tt": 4})),
        ("resultant overclaim", lambda x: x["result"]["critical_resultant_reduction"].__setitem__("interval_nonvanishing_on_all_critical_boxes_certified", True)),
        ("critical count", lambda x: x["result"]["deeper_selective_frontier"]["terminal_reason_counts"].__setitem__("candidate_zero_with_dt_containing_zero", 0)),
        ("interval area", lambda x: x["result"]["deeper_selective_frontier"]["terminal_reason_nonphysical_parameter_areas"].__setitem__("interval_geometry_exception", "0")),
        ("untyped charts", lambda x: x["result"]["deeper_selective_frontier"].__setitem__("untyped_candidate_graph_chart_count", 0)),
        ("orientation", lambda x: x["result"]["deeper_selective_frontier"].__setitem__("partial_current_definition", "unsigned")),
        ("partial TV", lambda x: x["result"]["deeper_selective_frontier"].__setitem__("partial_genuine_physical_marked_current_TV_upper", "0")),
        ("remaining width", lambda x: x["result"]["retained_fail_closed_terminal_frontier"].__setitem__("deep_replay_uniform_fixed_s_positive_t_width_outer_retained_fail_closed", "149/256")),
        ("complete current", lambda x: x["result"]["scope_limits"].__setitem__("complete_side_owner_current", True)),
        ("gate overclaim", lambda x: x["result"]["scope_limits"].__setitem__("gate3_certified", True)),
        ("stale blocker count", lambda x: x["result"].__setitem__("exact_remaining_blockers", ["resolve 79,660 old boxes"] * 6)),
        ("verdict overclaim", lambda x: x["verdict"].__setitem__("gate3", "CERTIFIED")),
    ]
    failures: list[str] = []
    for name, mutate in mutations:
        trial = copy.deepcopy(data)
        mutate(trial)
        refresh_digest(trial["result"])
        if not check_structure(trial, enforce_file_hashes=False):
            failures.append(name)
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    data = load_manifest(args.manifest)
    errors = check_structure(data)
    if errors:
        print("INTEGRITY: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    if args.replay:
        replay = replay_result()
        if replay != data["result"]:
            print("REPLAY: FAIL")
            return 1
        print("REPLAY: PASS")
    print("INTEGRITY: PASS")
    if args.self_test:
        failures = self_test(data)
        if failures:
            print("SELF-TEST: FAIL " + ", ".join(failures))
            return 1
        print("SELF-TEST: PASS 16/16")
    if args.integrity_only or args.replay or args.self_test:
        return 0
    print("complete_side_owner_current: NOT_CERTIFIED")
    print("strong_DQ_MT_DQ_FACE: NOT_CERTIFIED")
    print("gate3: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    sys.exit(main())
