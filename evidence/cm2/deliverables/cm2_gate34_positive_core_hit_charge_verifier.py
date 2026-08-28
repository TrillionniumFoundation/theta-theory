#!/usr/bin/env python3
"""Fail-closed verifier for the positive all-scale core-hit charge."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import cm2_gate34_positive_core_hit_charge_cert as certificate


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate34.positive-core-hit-charge.manifest.v1"
RESULT_SCHEMA = "cm2.gate34.positive-core-hit-charge.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate34-positive-core-hit-charge-manifest-2026-07-17.json"
)
CERTIFICATE = HERE / "cm2_gate34_positive_core_hit_charge_cert.py"


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
    if provenance.get("precision_bits") != 1024:
        errors.append("precision")
    if provenance.get("old_artifacts_modified") is not False:
        errors.append("append-only provenance")

    registry = result.get("selected_positive_core_hit_charge_registry", {})
    expected = {
        "charged_occurrence_count": 2,
        "charged_oriented_branch_count": 4,
        "all_four_branches_cover_every_scale_below_radius": True,
        "selected_reference_z_shifts": {
            "occ:c5fde0378e6e76eec93a0ceb": "1/4503599627370496",
            "occ:f2b4833eb8dccd403eec3485": "3/2251799813685248",
        },
        "base_z_half_width_power": 220,
        "base_z_half_width": str(certificate.BASE_HALF_WIDTH),
        "parameter_radius_power": 220,
        "parameter_radius": str(certificate.PARAMETER_RADIUS),
        "post_suffix_collision_count_to_core": 20,
        "destination_core_count": 2,
        "all_84_suffix_and_post_suffix_flights_strictly_between_0_and_2": True,
        "all_four_words_avoid_intermediate_collision_singularities": True,
        "all_four_destinations_are_strict_core_interiors": True,
        "labelled_base_parameter_coordinate_volume_power": 437,
    }
    for key, value in expected.items():
        if registry.get(key) != value:
            errors.append(f"registry {key}")
    expected_volume = str(
        2
        * (2 * certificate.BASE_HALF_WIDTH)
        * (2 * certificate.PARAMETER_RADIUS)
    )
    if registry.get("labelled_base_parameter_coordinate_volume") != expected_volume:
        errors.append("coordinate volume")
    for key in (
        "charged_branch_rows_sha256",
        "first_charged_branch_id",
        "last_charged_branch_id",
    ):
        if not isinstance(registry.get(key), str) or not registry[key]:
            errors.append(f"registry digest {key}")

    scope = result.get("strict_nonpromotion", {})
    for key in (
        "four_charged_branches_are_all_128_selected_branches",
        "positive_coordinate_volume_is_collision_SRB_fraction",
        "two_occurrences_imply_uniform_core_hit_fraction",
    ):
        if scope.get(key) is not False:
            errors.append(f"nonpromotion {key}")
    for key in (
        "post_core_2018_step_no_recut_dwell",
        "post_core_12108_step_no_recut_dwell",
        "quantitative_cemetery_tail",
        "common_strong_space_recovery_operator",
        "Gate3",
        "Gate4",
    ):
        if scope.get(key) != "NOT_CERTIFIED":
            errors.append(f"scope {key}")

    expected_verdict = {
        "positive_all_scale_core_hit_occurrences_2": "CERTIFIED",
        "positive_all_scale_core_hit_oriented_branches_4": "CERTIFIED",
        "post_suffix_collision_time_to_core_20": "CERTIFIED",
        "global_selected_core_hit_fraction": "NOT_CERTIFIED",
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

    registry = ("result", "selected_positive_core_hit_charge_registry")
    mutate(registry + ("charged_occurrence_count",), 1)
    mutate(registry + ("charged_oriented_branch_count",), 3)
    mutate(registry + ("all_four_branches_cover_every_scale_below_radius",), False)
    mutate(registry + ("base_z_half_width_power",), 219)
    mutate(registry + ("parameter_radius_power",), 219)
    mutate(registry + ("post_suffix_collision_count_to_core",), 19)
    mutate(registry + ("destination_core_count",), 1)
    mutate(registry + ("all_84_suffix_and_post_suffix_flights_strictly_between_0_and_2",), False)
    mutate(registry + ("all_four_words_avoid_intermediate_collision_singularities",), False)
    mutate(registry + ("all_four_destinations_are_strict_core_interiors",), False)
    mutate(registry + ("labelled_base_parameter_coordinate_volume_power",), 436)
    mutate(registry + ("labelled_base_parameter_coordinate_volume",), "0")
    mutate(("result", "provenance", "precision_bits"), 512)
    scope = ("result", "strict_nonpromotion")
    mutate(scope + ("four_charged_branches_are_all_128_selected_branches",), True)
    mutate(scope + ("positive_coordinate_volume_is_collision_SRB_fraction",), True)
    mutate(scope + ("two_occurrences_imply_uniform_core_hit_fraction",), True)
    mutate(scope + ("post_core_2018_step_no_recut_dwell",), "CERTIFIED")
    mutate(scope + ("post_core_12108_step_no_recut_dwell",), "CERTIFIED")
    mutate(scope + ("quantitative_cemetery_tail",), "CERTIFIED")
    mutate(scope + ("common_strong_space_recovery_operator",), "CERTIFIED")
    mutate(scope + ("Gate4",), "CERTIFIED")
    mutate(("verdict", "global_selected_core_hit_fraction"), "CERTIFIED")
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
    print("POSITIVE_ALL_SCALE_CORE_HIT_OCCURRENCES_2: CERTIFIED")
    print("POSITIVE_ALL_SCALE_CORE_HIT_ORIENTED_BRANCHES_4: CERTIFIED")
    print("POST_SUFFIX_COLLISION_TIME_TO_CORE_20: CERTIFIED")
    print("GLOBAL_SELECTED_CORE_HIT_FRACTION: NOT_CERTIFIED")
    print("NATIVE_2018_12108_NO_RECUT_DWELL: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
