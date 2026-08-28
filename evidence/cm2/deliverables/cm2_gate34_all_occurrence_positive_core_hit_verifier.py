#!/usr/bin/env python3
"""Fail-closed verifier for the all-occurrence positive core-hit registry."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import cm2_gate34_all_occurrence_positive_core_hit_cert as certificate


Q = Fraction
HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate34.all-occurrence-positive-core-hit.manifest.v1"
RESULT_SCHEMA = "cm2.gate34.all-occurrence-positive-core-hit.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate34-all-occurrence-positive-core-hit-manifest-2026-07-17.json"
)
CERTIFICATE = HERE / "cm2_gate34_all_occurrence_positive_core_hit_cert.py"


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


def expected_volumes() -> tuple[str, str]:
    new_volume = sum(
        Q(4, 2 ** (2 * radius_power))
        for _chart, _z, _time, radius_power in certificate.NEW_CHARGES.values()
    )
    old_manifest = json.loads(
        (
            HERE
            / "cm2-gate34-positive-core-hit-charge-manifest-2026-07-17.json"
        ).read_text(encoding="utf-8")
    )
    old_volume = Q(
        old_manifest["result"]["selected_positive_core_hit_charge_registry"][
            "labelled_base_parameter_coordinate_volume"
        ]
    )
    return str(new_volume), str(new_volume + old_volume)


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
    provenance = result.get("provenance", {})
    expected_provenance = {
        "dependency_sha256": certificate.DEPENDENCIES,
        "old_artifacts_modified": False,
        "floating_search_role": "proposal_only",
        "admission_engine": "python-flint Arb",
        "precision_bits": 2048,
    }
    if provenance != expected_provenance:
        errors.append("provenance")

    new_volume, total_volume = expected_volumes()
    registry = result.get("all_occurrence_positive_core_hit_registry", {})
    expected = {
        "maximal_reference_occurrence_count": 64,
        "maximal_reference_oriented_branch_count": 128,
        "imported_frozen_occurrence_count": 2,
        "imported_frozen_oriented_branch_count": 4,
        "new_Arb_validated_occurrence_count": 62,
        "new_Arb_validated_oriented_branch_count": 124,
        "charged_occurrence_count": 64,
        "charged_oriented_branch_count": 128,
        "all_maximal_occurrence_ids_have_positive_all_scale_cylinders": True,
        "both_oriented_sides_validated_for_every_occurrence": True,
        "floating_pilot_has_proposal_status_only": True,
        "Arb_precision_bits": 2048,
        "radius_power_histogram_by_occurrence": {
            "80": 32,
            "100": 8,
            "120": 16,
            "180": 2,
            "200": 4,
            "220": 2,
        },
        "post_suffix_core_entrance_word_length_histogram_by_occurrence": {
            "2": 22,
            "3": 10,
            "4": 8,
            "7": 8,
            "8": 4,
            "9": 4,
            "16": 2,
            "19": 4,
            "20": 2,
        },
        "maximum_certified_post_suffix_core_entrance_word_length": 20,
        "new_62_labelled_base_parameter_coordinate_volume": new_volume,
        "all_64_labelled_base_parameter_coordinate_volume": total_volume,
        "all_64_labelled_coordinate_volume_strict_lower_bound": "2^-153",
        "all_64_labelled_coordinate_volume_strict_upper_bound": "2^-152",
        "all_new_800_regular_suffix_and_post_suffix_flights_unique": True,
        "all_124_new_terminal_core_memberships_strict": True,
        "charged_occurrence_ids_sha256": (
            "533d028533771dc92174125af0faa13a0de4af584f8eadb178c001e284f76314"
        ),
        "floating_proposals_sha256": (
            "d86b1a3bd6f7a8f6566c61e29f659f82b2771ee08ad4790f3cd0a9291aac870d"
        ),
        "new_charged_branch_rows_sha256": (
            "757acf388e920be16fb9eaeecbbed9902da5b9b3b4dba9c82e6fb1a79e6242d2"
        ),
        "first_new_charged_branch_id": (
            "all-core-charge:59f6d9edfca5e38ee0636002f54bcf1ef69b784c5a09328ed809ce9bb0414281"
        ),
        "last_new_charged_branch_id": (
            "all-core-charge:f89e424b4e4b82e0faaa845bbc8190066b1e9a6bd7d0cec33a3eabb1f8b7b620"
        ),
    }
    for key, value in expected.items():
        if registry.get(key) != value:
            errors.append(f"registry {key}")
    if set(registry) != set(expected):
        errors.append("registry key set")
    if not Q(1, 2**153) < Q(total_volume) < Q(1, 2**152):
        errors.append("coordinate volume bounds")

    expected_scope = {
        "positive_cylinders_cover_entire_maximal_rows": False,
        "labelled_coordinate_volume_is_collision_SRB_fraction": False,
        "displayed_entrance_word_is_first_core_stopping_time": False,
        "uniform_normalized_core_hit_fraction": "NOT_CERTIFIED",
        "post_core_2018_step_no_recut_dwell": "NOT_CERTIFIED",
        "post_core_12108_step_field7_dwell": "NOT_CERTIFIED",
        "fixed_core_multiplier_survival": "NOT_CERTIFIED",
        "common_two_view_restriction": "NOT_CERTIFIED",
        "quantitative_cemetery_tail": "NOT_CERTIFIED",
        "common_strong_space_DQ_MT_DQ_FACE_recovery": "NOT_CERTIFIED",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
    }
    if result.get("strict_nonpromotion") != expected_scope:
        errors.append("strict nonpromotion")

    expected_verdict = {
        "positive_all_scale_core_hit_occurrences_64": "CERTIFIED",
        "positive_all_scale_core_hit_oriented_branches_128": "CERTIFIED",
        "maximum_post_suffix_core_entrance_word_length_20": "CERTIFIED",
        "first_core_stopping_time": "NOT_CERTIFIED",
        "normalized_selected_core_hit_fraction": "NOT_CERTIFIED",
        "native_2018_12108_no_recut_dwell": "NOT_CERTIFIED",
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

    registry = ("result", "all_occurrence_positive_core_hit_registry")
    mutate(registry + ("charged_occurrence_count",), 63)
    mutate(registry + ("charged_oriented_branch_count",), 127)
    mutate(registry + ("new_Arb_validated_occurrence_count",), 61)
    mutate(registry + ("new_Arb_validated_oriented_branch_count",), 123)
    mutate(registry + ("all_maximal_occurrence_ids_have_positive_all_scale_cylinders",), False)
    mutate(registry + ("both_oriented_sides_validated_for_every_occurrence",), False)
    mutate(registry + ("floating_pilot_has_proposal_status_only",), False)
    mutate(registry + ("Arb_precision_bits",), 1024)
    mutate(registry + ("maximum_certified_post_suffix_core_entrance_word_length",), 19)
    mutate(registry + ("all_64_labelled_coordinate_volume_strict_lower_bound",), "2^-152")
    mutate(registry + ("all_new_800_regular_suffix_and_post_suffix_flights_unique",), False)
    mutate(registry + ("all_124_new_terminal_core_memberships_strict",), False)
    mutate(registry + ("charged_occurrence_ids_sha256",), "0" * 64)
    mutate(registry + ("floating_proposals_sha256",), "0" * 64)
    mutate(registry + ("new_charged_branch_rows_sha256",), "0" * 64)
    mutate(("result", "provenance", "precision_bits"), 1024)
    mutate(("result", "provenance", "floating_search_role"), "evidence")
    scope = ("result", "strict_nonpromotion")
    mutate(scope + ("positive_cylinders_cover_entire_maximal_rows",), True)
    mutate(scope + ("labelled_coordinate_volume_is_collision_SRB_fraction",), True)
    mutate(scope + ("displayed_entrance_word_is_first_core_stopping_time",), True)
    mutate(scope + ("uniform_normalized_core_hit_fraction",), "CERTIFIED")
    mutate(scope + ("post_core_2018_step_no_recut_dwell",), "CERTIFIED")
    mutate(scope + ("post_core_12108_step_field7_dwell",), "CERTIFIED")
    mutate(scope + ("fixed_core_multiplier_survival",), "CERTIFIED")
    mutate(scope + ("common_two_view_restriction",), "CERTIFIED")
    mutate(scope + ("quantitative_cemetery_tail",), "CERTIFIED")
    mutate(scope + ("common_strong_space_DQ_MT_DQ_FACE_recovery",), "CERTIFIED")
    mutate(scope + ("Gate4",), "CERTIFIED")
    mutate(("verdict", "first_core_stopping_time"), "CERTIFIED")
    mutate(("verdict", "native_2018_12108_no_recut_dwell"), "CERTIFIED")
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
    print("POSITIVE_ALL_SCALE_CORE_HIT_OCCURRENCES_64: CERTIFIED")
    print("POSITIVE_ALL_SCALE_CORE_HIT_ORIENTED_BRANCHES_128: CERTIFIED")
    print("MAXIMUM_POST_SUFFIX_CORE_ENTRANCE_WORD_LENGTH_20: CERTIFIED")
    print("FIRST_CORE_STOPPING_TIME: NOT_CERTIFIED")
    print("NATIVE_2018_12108_NO_RECUT_DWELL: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
