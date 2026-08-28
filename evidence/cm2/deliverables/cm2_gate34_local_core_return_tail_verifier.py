#!/usr/bin/env python3
"""Fail-closed verifier for the four-box local core-return tail ledger."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import cm2_gate34_local_core_return_tail_cert as certificate


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate34.local-core-return-tail.manifest.v1"
RESULT_SCHEMA = "cm2.gate34.local-core-return-tail.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate34-local-core-return-tail-manifest-2026-07-18.json"
)
CERTIFICATE = HERE / "cm2_gate34_local_core_return_tail_cert.py"


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def strict_equal(left: Any, right: Any) -> bool:
    return canonical_json(left) == canonical_json(right)


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
        "materialized_source_current_box_count": 4,
        "Arb_precision_bits": 8192,
        "post_core_classification_horizon": 2018,
        "whole_box_core_classification_count": 8072,
        "ambiguous_core_classification_count": 0,
        "strict_outside_core_state_count": 8068,
        "strict_core_reentry_state_count": 4,
        "finite_first_return_current_cylinder_count": 3,
        "unresolved_excursion_survivor_box_count_after_2018": 1,
        "branch_key_to_return_outcome": {
            "occ:c5fde0378e6e76eec93a0ceb|hit": {
                "first_return_time": 545,
                "first_return_core_id": (
                    "core:a968ac5f95f455fe76aff0024641a68d464a645501166361c1175687adeb846c"
                ),
                "all_core_reentry_times_through_2018": [545, 1604],
            },
            "occ:c5fde0378e6e76eec93a0ceb|miss": {
                "first_return_time": 1531,
                "first_return_core_id": (
                    "core:2b055512b81ba06c4dd1beca2decab18d849bd593c3ab220cda4f593e96de67c"
                ),
                "all_core_reentry_times_through_2018": [1531],
            },
            "occ:f2b4833eb8dccd403eec3485|hit": {
                "first_return_time": ">2018",
                "first_return_core_id": None,
                "all_core_reentry_times_through_2018": [],
            },
            "occ:f2b4833eb8dccd403eec3485|miss": {
                "first_return_time": 649,
                "first_return_core_id": (
                    "core:918cc822d8c651e9204626b632ad4178ef695ba5a5c66db972823eff8508aee3"
                ),
                "all_core_reentry_times_through_2018": [649],
            },
        },
        "first_return_time_multiset": [545, 649, 1531, ">2018"],
        "exact_labelled_coordinate_tail": [
            {"horizon_range": "0<=n<=544", "fraction_tau_C_plus_gt_n": "1"},
            {"horizon_range": "545<=n<=648", "fraction_tau_C_plus_gt_n": "3/4"},
            {"horizon_range": "649<=n<=1530", "fraction_tau_C_plus_gt_n": "1/2"},
            {"horizon_range": "1531<=n<=2018", "fraction_tau_C_plus_gt_n": "1/4"},
        ],
        "return_by_2018_labelled_coordinate_fraction": "3/4",
        "unresolved_after_2018_labelled_coordinate_fraction": "1/4",
        "singular_cemetery_labelled_coordinate_fraction_through_2018": "0",
        "total_labelled_coordinate_volume": "2^-15996",
        "finite_return_labelled_coordinate_volume": "3*2^-15998",
        "survivor_labelled_coordinate_volume": "2^-15998",
        "all_8072_collisions_unique_and_regular_on_entire_boxes": True,
        "all_8072_states_strictly_classified_against_all_24_cores": True,
        "local_return_ledger_rows_sha256": (
            "7c78345d23089d95f8742d71b738e3617a23d2cfd1b4fb5633b820309951ac14"
        ),
        "branch_key_to_return_outcome_sha256": (
            "333b9cc5f38ba2d9d51e51f2b7a5564a7f70c8aebd1af03225be82d6cf8b3a0e"
        ),
        "first_local_return_ledger_id": (
            "local-return:289f72b671e7c33ddca8f0916385c83c1f96807c8a047cea70a3f9f8d43ebb9d"
        ),
        "last_local_return_ledger_id": (
            "local-return:519ce83cf7131fefa216d52b853764d16408162a230703a767a1cb571a5271f8"
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
    if not strict_equal(manifest.get("dependencies"), certificate.DEPENDENCIES):
        errors.append("dependency table")
    result = manifest.get("result", {})
    if result.get("schema") != RESULT_SCHEMA:
        errors.append("result schema")
    if result.get("internal_replay_digest") != result_digest(result):
        errors.append("result digest")
    expected_provenance = {
        "dependency_sha256": certificate.DEPENDENCIES,
        "old_artifacts_modified": False,
        "floating_pilot_role": "itinerary_proposal_only",
        "admission_engine": "python-flint Arb",
        "precision_bits": 8192,
    }
    if not strict_equal(result.get("provenance"), expected_provenance):
        errors.append("provenance")
    if not strict_equal(
        result.get("local_core_return_tail_registry"), expected_registry()
    ):
        errors.append("local return registry")
    expected_scope = {
        "labelled_coordinate_fraction_is_collision_SRB_probability": False,
        "source_current_boxes_are_full_collision_core_rectangles": False,
        "three_local_returns_construct_the_24_core_induced_operator": False,
        "unresolved_survivor_is_nonreturning_cemetery": False,
        "quantitative_global_cemetery_tail": "NOT_CERTIFIED",
        "new_strong_Lasota_Yorke_coefficient": "NOT_CERTIFIED",
        "common_two_view_restriction": "NOT_CERTIFIED",
        "common_strong_space_induced_recovery_operator": "NOT_CERTIFIED",
        "native_global_2018_12108_dwell": "NOT_CERTIFIED",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
    }
    if not strict_equal(result.get("strict_nonpromotion"), expected_scope):
        errors.append("strict nonpromotion")
    expected_verdict = {
        "local_first_return_current_cylinders_3": "CERTIFIED",
        "local_tau_core_plus_gt_2018_survivor_boxes_1": "CERTIFIED",
        "local_labelled_return_fraction_by_2018_3_over_4": "CERTIFIED",
        "singular_cemetery_through_2018_on_four_boxes_0": "CERTIFIED",
        "full_24_core_induced_operator": "NOT_CERTIFIED",
        "global_cemetery_tail": "NOT_CERTIFIED",
        "common_strong_space_induced_operator": "NOT_CERTIFIED",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
    }
    if not strict_equal(manifest.get("verdict"), expected_verdict):
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

    registry = ("result", "local_core_return_tail_registry")
    mutate(registry + ("materialized_source_current_box_count",), 3)
    mutate(registry + ("Arb_precision_bits",), 4096)
    mutate(registry + ("post_core_classification_horizon",), 2017)
    mutate(registry + ("whole_box_core_classification_count",), 8071)
    mutate(registry + ("ambiguous_core_classification_count",), 1)
    mutate(registry + ("strict_outside_core_state_count",), 8067)
    mutate(registry + ("strict_core_reentry_state_count",), 3)
    mutate(registry + ("finite_first_return_current_cylinder_count",), 4)
    mutate(registry + ("unresolved_excursion_survivor_box_count_after_2018",), 0)
    outcomes = registry + ("branch_key_to_return_outcome",)
    mutate(outcomes + ("occ:c5fde0378e6e76eec93a0ceb|hit", "first_return_time"), 546)
    mutate(outcomes + ("occ:c5fde0378e6e76eec93a0ceb|miss", "first_return_time"), 545)
    mutate(outcomes + ("occ:f2b4833eb8dccd403eec3485|hit", "first_return_time"), 2018)
    mutate(outcomes + ("occ:f2b4833eb8dccd403eec3485|miss", "first_return_time"), 648)
    mutate(outcomes + ("occ:c5fde0378e6e76eec93a0ceb|hit", "first_return_core_id"), "core:" + "0" * 64)
    mutate(outcomes + ("occ:f2b4833eb8dccd403eec3485|hit", "first_return_core_id"), "core:" + "0" * 64)
    swapped = copy.deepcopy(manifest)
    mapping = swapped["result"]["local_core_return_tail_registry"]["branch_key_to_return_outcome"]
    left = "occ:c5fde0378e6e76eec93a0ceb|hit"
    right = "occ:f2b4833eb8dccd403eec3485|miss"
    mapping[left], mapping[right] = mapping[right], mapping[left]
    refresh(swapped)
    mutations.append(swapped)
    mutate(registry + ("first_return_time_multiset",), [545, 649, 1530, ">2018"])
    mutate(registry + ("return_by_2018_labelled_coordinate_fraction",), "1")
    mutate(registry + ("unresolved_after_2018_labelled_coordinate_fraction",), "0")
    mutate(registry + ("singular_cemetery_labelled_coordinate_fraction_through_2018",), "1/4")
    mutate(registry + ("total_labelled_coordinate_volume",), "2^-15995")
    mutate(registry + ("finite_return_labelled_coordinate_volume",), "4*2^-15998")
    mutate(registry + ("all_8072_collisions_unique_and_regular_on_entire_boxes",), False)
    mutate(registry + ("all_8072_states_strictly_classified_against_all_24_cores",), False)
    mutate(registry + ("local_return_ledger_rows_sha256",), "0" * 64)
    mutate(registry + ("branch_key_to_return_outcome_sha256",), "0" * 64)
    mutate(("result", "provenance", "precision_bits"), 4096)
    mutate(("result", "provenance", "floating_pilot_role"), "evidence")
    scope = ("result", "strict_nonpromotion")
    mutate(scope + ("labelled_coordinate_fraction_is_collision_SRB_probability",), True)
    mutate(scope + ("source_current_boxes_are_full_collision_core_rectangles",), True)
    mutate(scope + ("three_local_returns_construct_the_24_core_induced_operator",), True)
    mutate(scope + ("unresolved_survivor_is_nonreturning_cemetery",), True)
    mutate(scope + ("quantitative_global_cemetery_tail",), "CERTIFIED")
    mutate(scope + ("new_strong_Lasota_Yorke_coefficient",), "CERTIFIED")
    mutate(scope + ("common_two_view_restriction",), "CERTIFIED")
    mutate(scope + ("common_strong_space_induced_recovery_operator",), "CERTIFIED")
    mutate(scope + ("native_global_2018_12108_dwell",), "CERTIFIED")
    mutate(scope + ("Gate4",), "CERTIFIED")
    mutate(("verdict", "full_24_core_induced_operator"), "CERTIFIED")
    mutate(("verdict", "global_cemetery_tail"), "CERTIFIED")
    mutate(("verdict", "common_strong_space_induced_operator"), "CERTIFIED")
    mutate(("verdict", "Gate4"), "CERTIFIED")
    # Strict type mutation: canonical JSON distinguishes true from 1.
    mutate(registry + ("all_8072_states_strictly_classified_against_all_24_cores",), 1)
    rejected = sum(bool(check(candidate)) for candidate in mutations)
    return rejected, len(mutations)


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON number: {value}")


def main() -> int:
    if sys.flags.optimize != 0:
        print("ERROR: optimized Python disables proof assertions", file=sys.stderr)
        return 1
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--replay", action="store_true")
    modes.add_argument("--integrity-only", action="store_true")
    modes.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        manifest = json.loads(
            args.manifest.read_text(encoding="utf-8"),
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_constant,
        )
    except Exception as error:
        print(f"MANIFEST_READ_ERROR: {error}", file=sys.stderr)
        return 1
    errors = check(manifest)
    if errors:
        print("ERROR: " + "; ".join(errors), file=sys.stderr)
        return 1
    if args.replay and canonical_json(certificate.build_result()) != canonical_json(
        manifest["result"]
    ):
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
    print("LOCAL_FIRST_RETURN_CURRENT_CYLINDERS_3: CERTIFIED")
    print("LOCAL_TAU_CORE_PLUS_GREATER_THAN_2018_SURVIVOR_BOXES_1: CERTIFIED")
    print("LOCAL_LABELLED_RETURN_FRACTION_BY_2018_3_OVER_4: CERTIFIED")
    print("SINGULAR_CEMETERY_THROUGH_2018_ON_FOUR_BOXES_0: CERTIFIED")
    print("FULL_24_CORE_INDUCED_OPERATOR: NOT_CERTIFIED")
    print("GLOBAL_CEMETERY_TAIL: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
