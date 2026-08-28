#!/usr/bin/env python3
"""Fail-closed verifier for the completed future side-owner current."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate3.remaining-graph-complete-current-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate3.remaining-graph-complete-current-frontier.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate3-remaining-graph-complete-current-frontier-manifest-2026-07-17.json"
)
CERTIFICATE = HERE / "cm2_gate3_remaining_graph_complete_current_frontier_cert.py"
EXPECTED_INTERNAL_DIGEST = "83b2b65b5e7489a481bc4a41ca44f4c2965f7acd5a3033a6b7b476e67b88567f"


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")).hexdigest()


def refresh_digest(result: dict[str, Any]) -> None:
    result.pop("internal_replay_digest", None)
    result["internal_replay_digest"] = canonical_digest(result)


def check_structure(
    data: Any, *, enforce_hashes: bool = True,
    enforce_expected_digest: bool = True,
) -> list[str]:
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
        "cm2-gate3-critical-graph-owner-typing-frontier-manifest-2026-07-16.json",
        "cm2-gate3-endpoint-scaled-resultant-frontier-manifest-2026-07-16.json",
        "cm2_gate3_critical_graph_owner_typing_frontier_cert.py",
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
    if (
        digest != canonical_digest(payload)
        or (enforce_expected_digest and digest != EXPECTED_INTERNAL_DIGEST)
    ):
        errors.append("internal replay digest mismatch")

    export = result.get("last_164_coordinate_export", {})
    for key, expected in {
        "target_row_indices": [8, 15, 36, 51],
        "target_row_count": 4,
        "exported_untyped_graph_count": 164,
        "equals_frozen_aggregate_and_therefore_exhausts_it": True,
        "coordinate_ledger_sha256": "fc05d693e7f7419644f07cd268ee7355e940761f2bde962cf4651025a31b50e4",
        "per_row_summary_ledger_sha256": "6c216faff9c6ec5370ad275c3370424117e09d368d9f2e03516eb678bed133ac",
    }.items():
        if export.get(key) != expected:
            errors.append(f"coordinate export mismatch: {key}")
    rows = export.get("per_row_summaries", [])
    expected_row_digests = {
        8: "ea14c3d45d1321d8fe74660aae21e54d9092ae6c9e66fca1cfe91370c8f0f115",
        15: "ce1e15b1c1478ba0f72f64d67a0499b0200f6931c5f9f9cc6983a448111cc1ad",
        36: "2ae8af19087d89c323a15d97fa8c15167ddf69305f73b100fa8b3acabb6b0877",
        51: "f90b5efc94370fa6c01b2662d850c288231249f987ce31e3e1a50052fe666e2b",
    }
    if len(rows) != 4:
        errors.append("row summary count mismatch")
    else:
        for row in rows:
            index = row.get("row_index")
            expected = {
                "additional_ambiguous_candidate_may_precede": 15,
                "untyped_candidate_graph_cover": 26,
            }
            if (
                index not in expected_row_digests
                or row.get("initial_cell_task_count") != 256
                or row.get("audit_call_count") != 39648
                or row.get("untyped_graph_count") != 41
                or row.get("untyped_graph_failure_counts") != expected
                or row.get("untyped_graph_ledger_sha256")
                != expected_row_digests.get(index)
            ):
                errors.append(f"row summary mismatch: {index}")

    typing = result.get("last_164_owner_typing", {})
    for key, expected in {
        "input_graph_count": 164,
        "typing_audit_call_count": 8908,
        "typed_graph_leaf_count": 100,
        "Delta_strict_excluded_descendant_count": 2372,
        "strict_nonphysical_time_descendant_count": 0,
        "strict_preemption_audit_input_count": 2064,
        "strictly_preempted_nonphysical_descendant_count": 2064,
        "total_nonphysical_descendant_count": 2064,
        "untyped_graph_leaf_count": 0,
        "strict_preemption_root_branch_requirements": "full-box discriminant>0, positive near root, near root<3",
        "strict_preemption_inequality": "upper(other_positive_near_root)<lower(candidate_tangent_projection)",
        "one_strict_preemptor_suffices_without_unique_owner": True,
        "typed_graph_ledger_sha256": "8f19cec28f01f7a52a4cfeda896a357c109621d1b86781264cd38896d4bc30f4",
        "Delta_excluded_ledger_sha256": "14351c6c162cfd34d0591e23000b5e8bd531fe675d6b1c4a3335c5a149f0e04f",
        "strictly_preempted_nonphysical_ledger_sha256": "8f436d0af8fb574586269551fc50a4520efd40821e113488a6e988e2a62859c0",
        "total_nonphysical_ledger_sha256": "8f436d0af8fb574586269551fc50a4520efd40821e113488a6e988e2a62859c0",
        "untyped_graph_ledger_sha256": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945",
    }.items():
        if typing.get(key) != expected:
            errors.append(f"owner typing mismatch: {key}")
    if typing.get("encountered_failure_counts") != {
        "additional_ambiguous_candidate_may_precede": 164,
        "candidate_tangent_not_before_alternative_owner": 6272,
    }:
        errors.append("encountered failure ledger mismatch")

    frontier = result.get("complete_current_frontier", {})
    for key, expected in {
        "all_1052_predecessor_untyped_graphs_resolved": True,
        "remaining_untyped_graph_count": 0,
        "complete_conditionally_physical_first_graph_chart_count": 41444,
        "complete_marked_current_TV_upper": "518152320",
        "predecessor_candidate_graph_fixed_s_count_upper": 592,
        "predecessor_candidate_graph_fixed_s_normalized_slope_sum_upper": 51404,
        "refining_or_excluding_old_candidate_charts_cannot_increase_these_outers": True,
        "TV_outer_was_frozen_on_complete_physical_plus_1052_candidate_graph_atlas": True,
        "complete_side_owner_current": True,
        "strong_DQ_MT_DQ_FACE": False,
        "gate3": False,
    }.items():
        if frontier.get(key) != expected:
            errors.append(f"complete current mismatch: {key}")

    expected_verdict = {
        "last_164_coordinate_export": "CERTIFIED",
        "all_1052_candidate_graphs_resolved": "CERTIFIED",
        "complete_side_owner_current": "CERTIFIED",
        "strong_DQ_MT_DQ_FACE": "NOT_CERTIFIED",
        "gate3": "NOT_CERTIFIED",
    }
    if data.get("verdict") != expected_verdict:
        errors.append("verdict mismatch")
    return errors


def replay_result() -> dict[str, Any]:
    import cm2_gate3_remaining_graph_complete_current_frontier_cert as cert
    return cert.build_result()


def self_test(data: dict[str, Any]) -> list[str]:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("row set", lambda x: x["result"]["last_164_coordinate_export"].__setitem__("target_row_indices", [8, 15, 36])),
        ("export count", lambda x: x["result"]["last_164_coordinate_export"].__setitem__("exported_untyped_graph_count", 163)),
        ("coordinate digest", lambda x: x["result"]["last_164_coordinate_export"].__setitem__("coordinate_ledger_sha256", "0" * 64)),
        ("row calls", lambda x: x["result"]["last_164_coordinate_export"]["per_row_summaries"][0].__setitem__("audit_call_count", 39647)),
        ("typing calls", lambda x: x["result"]["last_164_owner_typing"].__setitem__("typing_audit_call_count", 8907)),
        ("typed", lambda x: x["result"]["last_164_owner_typing"].__setitem__("typed_graph_leaf_count", 99)),
        ("excluded", lambda x: x["result"]["last_164_owner_typing"].__setitem__("Delta_strict_excluded_descendant_count", 2371)),
        ("preemption input", lambda x: x["result"]["last_164_owner_typing"].__setitem__("strict_preemption_audit_input_count", 2063)),
        ("preempted", lambda x: x["result"]["last_164_owner_typing"].__setitem__("strictly_preempted_nonphysical_descendant_count", 2063)),
        ("root branch", lambda x: x["result"]["last_164_owner_typing"].__setitem__("strict_preemption_root_branch_requirements", "positive root")),
        ("inequality", lambda x: x["result"]["last_164_owner_typing"].__setitem__("strict_preemption_inequality", "root<=candidate")),
        ("uniqueness overclaim", lambda x: x["result"]["last_164_owner_typing"].__setitem__("one_strict_preemptor_suffices_without_unique_owner", False)),
        ("untyped", lambda x: x["result"]["last_164_owner_typing"].__setitem__("untyped_graph_leaf_count", 1)),
        ("complete count", lambda x: x["result"]["complete_current_frontier"].__setitem__("complete_conditionally_physical_first_graph_chart_count", 41443)),
        ("TV", lambda x: x["result"]["complete_current_frontier"].__setitem__("complete_marked_current_TV_upper", "518152319")),
        ("candidate slope", lambda x: x["result"]["complete_current_frontier"].__setitem__("predecessor_candidate_graph_fixed_s_normalized_slope_sum_upper", 51403)),
        ("current", lambda x: x["result"]["complete_current_frontier"].__setitem__("complete_side_owner_current", False)),
        ("DQ overclaim", lambda x: x["result"]["complete_current_frontier"].__setitem__("strong_DQ_MT_DQ_FACE", True)),
        ("gate overclaim", lambda x: x["result"]["complete_current_frontier"].__setitem__("gate3", True)),
        ("verdict overclaim", lambda x: x["verdict"].__setitem__("gate3", "CERTIFIED")),
    ]
    failures = []
    for name, mutate in mutations:
        trial = copy.deepcopy(data)
        mutate(trial)
        refresh_digest(trial["result"])
        if not check_structure(
            trial, enforce_hashes=False, enforce_expected_digest=False
        ):
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
        print("SELF-TEST: PASS 20/20")
    if args.integrity_only or args.replay or args.self_test:
        return 0
    print("complete_side_owner_current: CERTIFIED")
    print("strong_DQ_MT_DQ_FACE: NOT_CERTIFIED")
    print("gate3: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    sys.exit(main())
