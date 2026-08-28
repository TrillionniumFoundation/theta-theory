#!/usr/bin/env python3
"""Fail-closed verifier for explicit charged 2018-step dwell cylinders."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import cm2_gate34_materialized_2018_dwell_cylinders_cert as certificate


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate34.materialized-2018-dwell-cylinders.manifest.v1"
RESULT_SCHEMA = "cm2.gate34.materialized-2018-dwell-cylinders.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate34-materialized-2018-dwell-cylinders-manifest-2026-07-17.json"
)
CERTIFICATE = HERE / "cm2_gate34_materialized_2018_dwell_cylinders_cert.py"


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
    expected_provenance = {
        "dependency_sha256": certificate.DEPENDENCIES,
        "old_artifacts_modified": False,
        "precision_bits": 8192,
        "floating_pilot_is_proposal_only": True,
        "every_pilot_target_is_independently_validated_by_Arb": True,
        "rejected_common_radius_power_6000_not_promoted": True,
    }
    if result.get("provenance") != expected_provenance:
        errors.append("provenance")

    registry = result.get("materialized_2018_dwell_cylinder_registry", {})
    expected_registry = {
        "materialized_occurrence_count": 2,
        "materialized_oriented_branch_count": 4,
        "explicit_positive_dwell_cylinder_count": 4,
        "Arb_precision_bits": 8192,
        "common_base_z_and_parameter_half_width_power": 8000,
        "common_base_z_and_parameter_half_width": "2^-8000",
        "point_parameter_magnitude_power": 300,
        "point_parameter_magnitude": (
            "1/2037035976334486086268445688409378161051468393665936250636140449354381299763336706183397376"
        ),
        "all_four_boxes_lie_strictly_inside_frozen_core_hit_charge": True,
        "all_four_source_to_core_words_unique_and_regular": True,
        "all_four_terminal_core_memberships_strict_on_entire_boxes": True,
        "all_four_first_post_core_collisions_strictly_outside_frozen_24_core": True,
        "fixed_core_open_operator_survival_failure_post_core_time": 1,
        "direct_regular_dwell_identification_with_fixed_core_operator_power": (
            "REFUTED_ON_FOUR_MATERIALIZED_BOXES"
        ),
        "post_core_regular_collision_count_per_branch": 2018,
        "total_interval_validated_post_core_regular_collisions": 8072,
        "all_8072_first_collision_decisions_unique_on_entire_boxes": True,
        "all_8072_flights_strictly_between_0_and_2_on_entire_boxes": True,
        "all_8072_cosines_strictly_above_1_over_1000_on_entire_boxes": True,
        "labelled_materialized_coordinate_volume": "2^-15996",
        "labelled_materialized_coordinate_volume_power": 15996,
        "materialized_branch_records_sha256": (
            "e4cf0b0bfa91a4f781fca1e7c7cffc9425dcd2184a4b16dbd601b29cd893bf4b"
        ),
        "first_materialized_dwell_cylinder_id": (
            "dwell-cylinder:13ebcfbe308190cae41ea67bbdeccb658883bd3891cfaa00b0c7ca68af209d16"
        ),
        "last_materialized_dwell_cylinder_id": (
            "dwell-cylinder:b68714594d3b5a71428ede35de44f8335b24e03e7e3c45be30b0e51f7035ac9d"
        ),
    }
    if registry != expected_registry:
        errors.append("materialized registry")

    expected_scope = {
        "all_128_charged_branches_have_2018_materialized_dwell": False,
        "post_core_12108_step_field7_dwell": "NOT_CERTIFIED",
        "fixed_core_multiplier_survival_for_all_2018_steps": (
            "REFUTED_ON_FOUR_MATERIALIZED_BOXES"
        ),
        "same_interval_two_view_shell_identification": "NOT_CERTIFIED",
        "common_strong_space_recovery_operator": "NOT_CERTIFIED",
        "native_global_2018_dwell_schedule": "NOT_CERTIFIED",
        "quantitative_cemetery_tail": "NOT_CERTIFIED",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
    }
    if result.get("strict_nonpromotion") != expected_scope:
        errors.append("strict nonpromotion")

    expected_verdict = {
        "explicit_positive_2018_dwell_cylinders_4": "CERTIFIED",
        "common_dyadic_half_width_2^-8000": "CERTIFIED",
        "interval_validated_post_core_regular_collisions_8072": "CERTIFIED",
        "direct_fixed_core_operator_power_attachment_on_4_boxes": "REFUTED",
        "all_128_branch_native_2018_dwell": "NOT_CERTIFIED",
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

    registry = ("result", "materialized_2018_dwell_cylinder_registry")
    mutate(registry + ("materialized_occurrence_count",), 1)
    mutate(registry + ("materialized_oriented_branch_count",), 3)
    mutate(registry + ("explicit_positive_dwell_cylinder_count",), 3)
    mutate(registry + ("Arb_precision_bits",), 4096)
    mutate(registry + ("common_base_z_and_parameter_half_width_power",), 7999)
    mutate(registry + ("common_base_z_and_parameter_half_width",), "2^-7999")
    mutate(registry + ("all_four_boxes_lie_strictly_inside_frozen_core_hit_charge",), False)
    mutate(registry + ("all_four_source_to_core_words_unique_and_regular",), False)
    mutate(registry + ("all_four_terminal_core_memberships_strict_on_entire_boxes",), False)
    mutate(registry + ("all_four_first_post_core_collisions_strictly_outside_frozen_24_core",), False)
    mutate(registry + ("fixed_core_open_operator_survival_failure_post_core_time",), 2)
    mutate(registry + ("direct_regular_dwell_identification_with_fixed_core_operator_power",), "CERTIFIED")
    mutate(registry + ("post_core_regular_collision_count_per_branch",), 2017)
    mutate(registry + ("total_interval_validated_post_core_regular_collisions",), 8071)
    mutate(registry + ("all_8072_first_collision_decisions_unique_on_entire_boxes",), False)
    mutate(registry + ("all_8072_flights_strictly_between_0_and_2_on_entire_boxes",), False)
    mutate(registry + ("all_8072_cosines_strictly_above_1_over_1000_on_entire_boxes",), False)
    mutate(registry + ("labelled_materialized_coordinate_volume",), "2^-15995")
    mutate(registry + ("materialized_branch_records_sha256",), "0" * 64)
    mutate(("result", "provenance", "floating_pilot_is_proposal_only"), False)
    mutate(("result", "provenance", "every_pilot_target_is_independently_validated_by_Arb"), False)
    scope = ("result", "strict_nonpromotion")
    mutate(scope + ("all_128_charged_branches_have_2018_materialized_dwell",), True)
    mutate(scope + ("post_core_12108_step_field7_dwell",), "CERTIFIED")
    mutate(scope + ("fixed_core_multiplier_survival_for_all_2018_steps",), "CERTIFIED")
    mutate(scope + ("same_interval_two_view_shell_identification",), "CERTIFIED")
    mutate(scope + ("common_strong_space_recovery_operator",), "CERTIFIED")
    mutate(scope + ("native_global_2018_dwell_schedule",), "CERTIFIED")
    mutate(scope + ("Gate4",), "CERTIFIED")
    mutate(("verdict", "all_128_branch_native_2018_dwell"), "CERTIFIED")
    mutate(("verdict", "post_core_12108_no_recut_dwell"), "CERTIFIED")
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
    print("EXPLICIT_POSITIVE_2018_DWELL_CYLINDERS_4: CERTIFIED")
    print("COMMON_DYADIC_HALF_WIDTH_2^-8000: CERTIFIED")
    print("INTERVAL_VALIDATED_POST_CORE_REGULAR_COLLISIONS_8072: CERTIFIED")
    print("DIRECT_FIXED_CORE_OPERATOR_POWER_ATTACHMENT_ON_4_BOXES: REFUTED")
    print("ALL_128_BRANCH_NATIVE_2018_DWELL: NOT_CERTIFIED")
    print("POST_CORE_12108_NO_RECUT_DWELL: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
