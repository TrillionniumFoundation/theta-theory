#!/usr/bin/env python3
"""Fail-closed verifier for the critical graph owner-typing frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate3.critical-graph-owner-typing-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate3.critical-graph-owner-typing-frontier.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate3-critical-graph-owner-typing-frontier-manifest-2026-07-16.json"
)
CERTIFICATE = HERE / "cm2_gate3_critical_graph_owner_typing_frontier_cert.py"
EXPECTED_INTERNAL_DIGEST = "db6322dda77d8df1966ed2a86e9e3651fed33346b3de561f72600cda5ac49a12"


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
    errors = []
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
        "cm2-gate3-cancellation-free-current-frontier-manifest-2026-07-16.json",
        "cm2_gate3_cancellation_free_current_frontier_cert.py",
        "cm2_gate3_deep_scaled_resultant_frontier_cert.py",
        "cm2_gate3_physical_first_unresolved_frontier_cert.py",
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

    export = result.get("critical_coordinate_export", {})
    for key, expected in {
        "coarse_candidate_task_count": 444,
        "audit_call_count": 3196,
        "Delta_strict_excluded_leaf_count": 932,
        "transverse_graph_leaf_count": 888,
        "regular_fold_leaf_count": 0,
        "unresolved_leaf_count": 0,
        "Delta_excluded_coordinate_ledger_sha256": "312eeb20213df7ae338520d1c0eedada50976651a82351d1887a5f0fdf63ecf9",
        "transverse_graph_coordinate_ledger_sha256": "671c858d37b288bedac021dd9d3ae2f99d3665c0281f1ec5b07be0830eb1aa0e",
    }.items():
        if export.get(key) != expected:
            errors.append(f"coordinate export mismatch: {key}")

    typing = result.get("critical_graph_owner_typing", {})
    for key, expected in {
        "input_graph_leaf_count": 888,
        "typing_audit_call_count": 888,
        "typed_graph_leaf_count": 0,
        "Delta_strict_excluded_descendant_count": 840,
        "strict_nonphysical_time_graph_descendant_count": 48,
        "untyped_graph_leaf_count": 0,
        "encountered_failure_counts": {},
        "all_888_conservative_graph_leaves_resolved_without_physical_future_face": True,
        "marked_current_TV_contribution_from_critical_graph_class": "0",
        "physical_FACE_2CUT_contribution_from_critical_graph_class": "0",
        "physical_FACE_TIME_contribution_from_critical_graph_class": "0",
        "Delta_excluded_ledger_sha256": "8f46609691db1f1017ae007c247a5f6c380a88228e6785e1d816dc8e5d2b47ce",
        "strict_nonphysical_time_ledger_sha256": "b4aa4ca02345708dd7140623d0ca916db1df7277b8e0fa9f478b81e6b0c1b0f9",
    }.items():
        if typing.get(key) != expected:
            errors.append(f"critical typing mismatch: {key}")

    frontier = result.get("remaining_frontier", {})
    for key, expected in {
        "frozen_unexported_untyped_graph_count": 164,
        "critical_untyped_graph_count_after_this_audit": 0,
        "combined_untyped_graph_count_upper": 164,
        "safe_maximum_candidate_graph_charts_on_one_fixed_s_slice": 592,
        "safe_maximum_candidate_graph_normalized_slope_sum_on_one_fixed_s_slice": 51404,
        "safe_uniform_fixed_s_candidate_zero_set_Leb_Z_linear_coefficient": "1184",
        "safe_uniform_fixed_s_candidate_zero_set_row_law_Z_linear_coefficient": "149184/5",
        "partial_genuine_physical_marked_current_TV_upper_unchanged": "518152320",
        "complete_side_owner_current": False,
        "strong_DQ_MT_DQ_FACE": False,
        "gate3": False,
    }.items():
        if frontier.get(key) != expected:
            errors.append(f"remaining frontier mismatch: {key}")
    if len(result.get("exact_remaining_blockers", [])) != 3:
        errors.append("blocker ledger mismatch")

    expected_verdict = {
        "critical_graph_coordinate_export": "CERTIFIED",
        "critical_graph_physical_future_exclusion": "CERTIFIED",
        "complete_side_owner_current": "NOT_CERTIFIED",
        "strong_DQ_MT_DQ_FACE": "NOT_CERTIFIED",
        "gate3": "NOT_CERTIFIED",
    }
    if data.get("verdict") != expected_verdict:
        errors.append("verdict mismatch")
    return errors


def replay_result() -> dict[str, Any]:
    import cm2_gate3_critical_graph_owner_typing_frontier_cert as cert
    return cert.build_result()


def self_test(data: dict[str, Any]) -> list[str]:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("tasks", lambda x: x["result"]["critical_coordinate_export"].__setitem__("coarse_candidate_task_count", 443)),
        ("graphs", lambda x: x["result"]["critical_coordinate_export"].__setitem__("transverse_graph_leaf_count", 887)),
        ("graph digest", lambda x: x["result"]["critical_coordinate_export"].__setitem__("transverse_graph_coordinate_ledger_sha256", "0" * 64)),
        ("typing input", lambda x: x["result"]["critical_graph_owner_typing"].__setitem__("input_graph_leaf_count", 887)),
        ("Delta exclusions", lambda x: x["result"]["critical_graph_owner_typing"].__setitem__("Delta_strict_excluded_descendant_count", 839)),
        ("nonphysical", lambda x: x["result"]["critical_graph_owner_typing"].__setitem__("strict_nonphysical_time_graph_descendant_count", 47)),
        ("untyped", lambda x: x["result"]["critical_graph_owner_typing"].__setitem__("untyped_graph_leaf_count", 1)),
        ("current charge", lambda x: x["result"]["critical_graph_owner_typing"].__setitem__("marked_current_TV_contribution_from_critical_graph_class", "1")),
        ("remaining", lambda x: x["result"]["remaining_frontier"].__setitem__("combined_untyped_graph_count_upper", 163)),
        ("candidate count", lambda x: x["result"]["remaining_frontier"].__setitem__("safe_maximum_candidate_graph_charts_on_one_fixed_s_slice", 591)),
        ("slope", lambda x: x["result"]["remaining_frontier"].__setitem__("safe_maximum_candidate_graph_normalized_slope_sum_on_one_fixed_s_slice", 51403)),
        ("current overclaim", lambda x: x["result"]["remaining_frontier"].__setitem__("complete_side_owner_current", True)),
        ("DQ overclaim", lambda x: x["result"]["remaining_frontier"].__setitem__("strong_DQ_MT_DQ_FACE", True)),
        ("gate overclaim", lambda x: x["result"]["remaining_frontier"].__setitem__("gate3", True)),
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
        print("SELF-TEST: PASS 15/15")
    if args.integrity_only or args.replay or args.self_test:
        return 0
    print("complete_side_owner_current: NOT_CERTIFIED")
    print("strong_DQ_MT_DQ_FACE: NOT_CERTIFIED")
    print("gate3: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    sys.exit(main())
