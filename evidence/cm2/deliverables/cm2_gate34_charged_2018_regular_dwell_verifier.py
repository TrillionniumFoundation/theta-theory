#!/usr/bin/env python3
"""Fail-closed verifier for the charged 2018 regular-dwell witness."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import cm2_gate34_charged_2018_regular_dwell_cert as certificate


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate34.charged-2018-regular-dwell.manifest.v1"
RESULT_SCHEMA = "cm2.gate34.charged-2018-regular-dwell.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate34-charged-2018-regular-dwell-manifest-2026-07-17.json"
)
CERTIFICATE = HERE / "cm2_gate34_charged_2018_regular_dwell_cert.py"


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

    result = manifest.get("result", {})
    if result.get("schema") != RESULT_SCHEMA:
        errors.append("result schema")
    if result.get("internal_replay_digest") != result_digest(result):
        errors.append("result digest")
    provenance = result.get("provenance", {})
    if provenance.get("precision_bits") != 8192:
        errors.append("precision")
    if provenance.get("floating_pilot_is_proposal_only") is not True:
        errors.append("pilot scope")
    if provenance.get("every_pilot_target_is_independently_validated_by_Arb") is not True:
        errors.append("Arb validation")
    if provenance.get("old_artifacts_modified") is not False:
        errors.append("append-only provenance")

    registry = result.get("charged_2018_regular_dwell_registry", {})
    expected = {
        "charged_occurrence_count": 2,
        "charged_oriented_branch_count": 4,
        "point_parameter_magnitude_power": 300,
        "point_parameter_magnitude": str(certificate.POINT_PARAMETER_MAGNITUDE),
        "post_core_regular_collision_count_per_branch": 2018,
        "total_validated_post_core_regular_collisions": 8072,
        "positive_open_no_singularity_subcylinder_count": 4,
        "all_four_points_lie_strictly_inside_the_existing_core_hit_charge": True,
        "all_8072_post_core_flights_strictly_between_0_and_2": True,
        "all_8072_post_core_cosines_strictly_above_1_over_1000": True,
        "all_8072_first_collision_decisions_unique": True,
        "finite_strict_analytic_itinerary_implies_positive_open_subcylinder": True,
        "post_core_itinerary_digest_table": {
            f"{occurrence_id}:{side}": value
            for (occurrence_id, side), value in sorted(
                certificate.EXPECTED_ITINERARY_DIGESTS.items()
            )
        },
    }
    for key, value in expected.items():
        if registry.get(key) != value:
            errors.append(f"registry {key}")
    if not isinstance(registry.get("branch_records_sha256"), str):
        errors.append("branch digest")

    scalar = result.get("frozen_scalar_attachment", {})
    if scalar != {
        "abstract_same_interval_shell_cycle_upper": "45/64",
        "abstract_shell_dwell_steps": 2018,
        "local_regular_dwell_witness_does_not_install_common_strong_operator": True,
    }:
        errors.append("scalar attachment")

    scope = result.get("strict_nonpromotion", {})
    if scope.get("positive_open_subcylinder_radii") != "EXIST_BUT_NOT_MATERIALIZED":
        errors.append("radius scope")
    for key in (
        "whole_four_branch_core_hit_charge_has_2018_common_itinerary",
        "all_128_selected_branches_have_positive_core_hit_charge",
    ):
        if scope.get(key) is not False:
            errors.append(f"nonpromotion {key}")
    for key in (
        "post_core_12108_step_no_recut_dwell",
        "fixed_core_multiplier_survival_for_all_2018_steps",
        "same_interval_two_view_shell_identification",
        "common_strong_space_recovery_operator",
        "native_global_2018_dwell_schedule",
        "Gate3",
        "Gate4",
        "Gate5",
    ):
        if scope.get(key) != "NOT_CERTIFIED":
            errors.append(f"scope {key}")

    expected_verdict = {
        "positive_open_2018_regular_dwell_subcylinders_4": "CERTIFIED",
        "validated_post_core_regular_collisions_8072": "CERTIFIED",
        "native_global_2018_dwell_schedule": "NOT_CERTIFIED",
        "post_core_12108_no_recut_dwell": "NOT_CERTIFIED",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
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

    registry = ("result", "charged_2018_regular_dwell_registry")
    mutate(registry + ("charged_occurrence_count",), 1)
    mutate(registry + ("charged_oriented_branch_count",), 3)
    mutate(registry + ("point_parameter_magnitude_power",), 299)
    mutate(registry + ("post_core_regular_collision_count_per_branch",), 2017)
    mutate(registry + ("total_validated_post_core_regular_collisions",), 8071)
    mutate(registry + ("positive_open_no_singularity_subcylinder_count",), 3)
    mutate(registry + ("all_four_points_lie_strictly_inside_the_existing_core_hit_charge",), False)
    mutate(registry + ("all_8072_post_core_flights_strictly_between_0_and_2",), False)
    mutate(registry + ("all_8072_post_core_cosines_strictly_above_1_over_1000",), False)
    mutate(registry + ("all_8072_first_collision_decisions_unique",), False)
    mutate(registry + ("finite_strict_analytic_itinerary_implies_positive_open_subcylinder",), False)
    mutate(("result", "provenance", "precision_bits"), 4096)
    mutate(("result", "provenance", "floating_pilot_is_proposal_only"), False)
    mutate(("result", "provenance", "every_pilot_target_is_independently_validated_by_Arb"), False)
    scope = ("result", "strict_nonpromotion")
    mutate(scope + ("positive_open_subcylinder_radii",), "MATERIALIZED")
    mutate(scope + ("whole_four_branch_core_hit_charge_has_2018_common_itinerary",), True)
    mutate(scope + ("all_128_selected_branches_have_positive_core_hit_charge",), True)
    mutate(scope + ("post_core_12108_step_no_recut_dwell",), "CERTIFIED")
    mutate(scope + ("fixed_core_multiplier_survival_for_all_2018_steps",), "CERTIFIED")
    mutate(scope + ("same_interval_two_view_shell_identification",), "CERTIFIED")
    mutate(scope + ("common_strong_space_recovery_operator",), "CERTIFIED")
    mutate(scope + ("native_global_2018_dwell_schedule",), "CERTIFIED")
    mutate(scope + ("Gate4",), "CERTIFIED")
    mutate(("verdict", "native_global_2018_dwell_schedule"), "CERTIFIED")
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
    print("POSITIVE_OPEN_2018_REGULAR_DWELL_SUBCYLINDERS_4: CERTIFIED")
    print("VALIDATED_POST_CORE_REGULAR_COLLISIONS_8072: CERTIFIED")
    print("NATIVE_GLOBAL_2018_DWELL_SCHEDULE: NOT_CERTIFIED")
    print("POST_CORE_12108_NO_RECUT_DWELL: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
