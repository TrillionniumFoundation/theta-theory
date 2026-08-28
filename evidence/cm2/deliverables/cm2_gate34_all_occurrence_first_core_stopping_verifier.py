#!/usr/bin/env python3
"""Fail-closed verifier for all-occurrence first-core stopping cylinders."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import cm2_gate34_all_occurrence_first_core_stopping_cert as certificate


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate34.all-occurrence-first-core-stopping.manifest.v1"
RESULT_SCHEMA = "cm2.gate34.all-occurrence-first-core-stopping.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate34-all-occurrence-first-core-stopping-manifest-2026-07-18.json"
)
CERTIFICATE = HERE / "cm2_gate34_all_occurrence_first_core_stopping_cert.py"


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


def expected_registry() -> dict[str, Any]:
    return {
        "maximal_reference_occurrence_count": 64,
        "charged_oriented_cylinder_count": 128,
        "exact_source_boxes_reclassified_as_physical_immutable_subrows": 64,
        "hit_global_first_owner_audits": 64,
        "miss_global_first_owner_audits": 64,
        "old_frozen_boxes_strictly_contained_in_predecessor_germs": 2,
        "all_hit_tangent_targets_are_global_first_collisions": True,
        "all_hit_regular_suffix_targets_are_global_second_collisions": True,
        "all_miss_regular_suffix_targets_are_global_first_collisions": True,
        "all_hit_miss_pairs_share_the_same_regular_suffix_chart": True,
        "first_core_stopping_cylinder_count": 128,
        "first_core_stopping_clock_origin": "regular_suffix_state_at_time_0",
        "source_to_regular_suffix_collisions_are_not_in_stopping_clock": True,
        "first_core_stopping_time_histogram_by_oriented_cylinder": {
            "2": 44,
            "3": 20,
            "4": 16,
            "7": 16,
            "8": 8,
            "9": 8,
            "16": 4,
            "19": 8,
            "20": 4,
        },
        "maximum_first_core_stopping_time_from_regular_suffix": 20,
        "strict_preterminal_outside_all_24_core_state_count": 756,
        "strict_terminal_inside_one_core_state_count": 128,
        "ambiguous_core_classification_count": 0,
        "distinct_destination_core_count": 14,
        "all_128_displayed_entrance_words_are_first_core_stopping_words": True,
        "source_owner_audit_rows_sha256": (
            "288e2cdad8b1dd771f1cc552c56823f8f252e11c787481a2ca216e6d26d386ff"
        ),
        "first_stopping_branch_rows_sha256": (
            "46cb6480f28f202fc94ed85393138bffbcb2045a5ef79c4564e90372edaaf5d2"
        ),
        "branch_key_to_suffix_relative_first_time_and_core_sha256": (
            "a1cea9b5b07336560a62943a5b0d800ddbe98a425500579979af67ff2c3d82b2"
        ),
        "destination_core_ids_sha256": (
            "5db145b1b1e93eb7286ca3ee6bf85862cbdf18f4f3e766a3d9fafad26413046b"
        ),
        "first_source_owner_audit_id": (
            "source-owner:947d4f24b7e24567c9f5e9cfcd18756173a187a8a747439ef31c3fdbe1c059a7"
        ),
        "last_source_owner_audit_id": (
            "source-owner:554973f49488d7fc3b6e5b84e2b786c86c9e42a3fdcbc7ab28ae82917bec5a7d"
        ),
        "first_stopping_branch_id": (
            "first-core:93a08e3e3c25bb66399b4dc4f0b1e57a78867f2aa50588e4e6848d51364ee6f3"
        ),
        "last_stopping_branch_id": (
            "first-core:c4881d110746fa8082bdb925a98ecfe60d83c56cec286ee8e0e51822016ea86a"
        ),
    }


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

    result = manifest.get("result", {})
    if result.get("schema") != RESULT_SCHEMA:
        errors.append("result schema")
    if result.get("internal_replay_digest") != result_digest(result):
        errors.append("result digest")
    expected_provenance = {
        "dependency_sha256": certificate.DEPENDENCIES,
        "old_artifacts_modified": False,
        "floating_search_role": "proposal_only",
        "admission_engine": "python-flint Arb",
        "precision_bits": 2048,
        "candidate_universe_radius_in_lattice_cells": 4,
    }
    if result.get("provenance") != expected_provenance:
        errors.append("provenance")
    if result.get("all_occurrence_first_core_stopping_registry") != (
        expected_registry()
    ):
        errors.append("first stopping registry")
    expected_scope = {
        "positive_cylinders_cover_entire_maximal_rows": False,
        "labelled_coordinate_volume_is_collision_SRB_fraction": False,
        "whole_germ_domain_first_core_stopping": "NOT_CERTIFIED",
        "normalized_selected_core_hit_fraction": "NOT_CERTIFIED",
        "quantitative_cemetery_tail": "NOT_CERTIFIED",
        "post_core_first_return_operator": "NOT_CERTIFIED",
        "common_two_view_restriction": "NOT_CERTIFIED",
        "common_strong_space_DQ_MT_DQ_FACE_recovery": "NOT_CERTIFIED",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
    }
    if result.get("strict_nonpromotion") != expected_scope:
        errors.append("strict nonpromotion")
    expected_verdict = {
        "charged_first_core_stopping_cylinders_128": "CERTIFIED",
        "maximum_first_core_stopping_time_20": "CERTIFIED",
        "global_hit_source_owner_audits_64": "CERTIFIED",
        "global_miss_source_owner_audits_64": "CERTIFIED",
        "whole_germ_first_core_stopping": "NOT_CERTIFIED",
        "normalized_selected_core_hit_fraction": "NOT_CERTIFIED",
        "quantitative_cemetery_tail": "NOT_CERTIFIED",
        "induced_core_return_operator": "NOT_CERTIFIED",
        "Gate3": "NOT_CERTIFIED",
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

    registry = ("result", "all_occurrence_first_core_stopping_registry")
    mutate(registry + ("maximal_reference_occurrence_count",), 63)
    mutate(registry + ("charged_oriented_cylinder_count",), 127)
    mutate(
        registry
        + ("exact_source_boxes_reclassified_as_physical_immutable_subrows",),
        63,
    )
    mutate(registry + ("hit_global_first_owner_audits",), 63)
    mutate(registry + ("miss_global_first_owner_audits",), 63)
    mutate(registry + ("all_hit_tangent_targets_are_global_first_collisions",), False)
    mutate(registry + ("all_hit_regular_suffix_targets_are_global_second_collisions",), False)
    mutate(registry + ("all_miss_regular_suffix_targets_are_global_first_collisions",), False)
    mutate(registry + ("all_hit_miss_pairs_share_the_same_regular_suffix_chart",), False)
    mutate(registry + ("first_core_stopping_cylinder_count",), 127)
    mutate(registry + ("first_core_stopping_clock_origin",), "source_state_at_time_0")
    mutate(registry + ("source_to_regular_suffix_collisions_are_not_in_stopping_clock",), False)
    mutate(registry + ("maximum_first_core_stopping_time_from_regular_suffix",), 19)
    mutate(registry + ("strict_preterminal_outside_all_24_core_state_count",), 755)
    mutate(registry + ("strict_terminal_inside_one_core_state_count",), 127)
    mutate(registry + ("ambiguous_core_classification_count",), 1)
    mutate(registry + ("distinct_destination_core_count",), 13)
    mutate(registry + ("all_128_displayed_entrance_words_are_first_core_stopping_words",), False)
    mutate(registry + ("source_owner_audit_rows_sha256",), "0" * 64)
    mutate(registry + ("first_stopping_branch_rows_sha256",), "0" * 64)
    mutate(registry + ("branch_key_to_suffix_relative_first_time_and_core_sha256",), "0" * 64)
    mutate(registry + ("destination_core_ids_sha256",), "0" * 64)
    mutate(("result", "provenance", "floating_search_role"), "evidence")
    mutate(("result", "provenance", "precision_bits"), 1024)
    mutate(("result", "provenance", "candidate_universe_radius_in_lattice_cells"), 3)
    scope = ("result", "strict_nonpromotion")
    mutate(scope + ("positive_cylinders_cover_entire_maximal_rows",), True)
    mutate(scope + ("labelled_coordinate_volume_is_collision_SRB_fraction",), True)
    mutate(scope + ("whole_germ_domain_first_core_stopping",), "CERTIFIED")
    mutate(scope + ("normalized_selected_core_hit_fraction",), "CERTIFIED")
    mutate(scope + ("quantitative_cemetery_tail",), "CERTIFIED")
    mutate(scope + ("post_core_first_return_operator",), "CERTIFIED")
    mutate(scope + ("common_two_view_restriction",), "CERTIFIED")
    mutate(scope + ("common_strong_space_DQ_MT_DQ_FACE_recovery",), "CERTIFIED")
    mutate(scope + ("Gate4",), "CERTIFIED")
    mutate(("verdict", "whole_germ_first_core_stopping"), "CERTIFIED")
    mutate(("verdict", "quantitative_cemetery_tail"), "CERTIFIED")
    mutate(("verdict", "induced_core_return_operator"), "CERTIFIED")
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
    print("CHARGED_FIRST_CORE_STOPPING_CYLINDERS_128: CERTIFIED")
    print("MAXIMUM_FIRST_CORE_STOPPING_TIME_20: CERTIFIED")
    print("GLOBAL_HIT_SOURCE_OWNER_AUDITS_64: CERTIFIED")
    print("GLOBAL_MISS_SOURCE_OWNER_AUDITS_64: CERTIFIED")
    print("WHOLE_GERM_FIRST_CORE_STOPPING: NOT_CERTIFIED")
    print("QUANTITATIVE_CEMETERY_TAIL: NOT_CERTIFIED")
    print("INDUCED_CORE_RETURN_OPERATOR: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
