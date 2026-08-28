#!/usr/bin/env python3
"""Fail-closed verifier for source-relative first-core stopping."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import cm2_gate34_source_relative_first_core_stopping_cert as certificate


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate34.source-relative-first-core-stopping.manifest.v1"
RESULT_SCHEMA = "cm2.gate34.source-relative-first-core-stopping.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate34-source-relative-first-core-stopping-manifest-2026-07-18.json"
)
CERTIFICATE = HERE / "cm2_gate34_source_relative_first_core_stopping_cert.py"
EXPECTED_CERTIFICATE_SHA256 = (
    "0e4aaf50f2221d81a78706da3f8c6a85ccbf678db622df62c275c00fa3b991a6"
)


def canonical_json(value: Any) -> str:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), allow_nan=False
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def result_digest(result: dict[str, Any]) -> str:
    payload = copy.deepcopy(result)
    payload.pop("internal_replay_digest", None)
    return digest(payload)


def same(left: Any, right: Any) -> bool:
    try:
        return canonical_json(left) == canonical_json(right)
    except (TypeError, ValueError):
        return False


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def expected_registry() -> dict[str, Any]:
    return {
        "maximal_reference_occurrence_count": 64,
        "charged_oriented_cylinder_count": 128,
        "shared_source_state_classification_count": 64,
        "source_state_branch_reference_count": 128,
        "hit_pre_suffix_intermediate_state_classification_count": 64,
        "unique_pre_suffix_classification_row_count": 128,
        "all_64_source_states_strictly_outside_all_24_cores": True,
        "all_64_hit_intermediate_states_strictly_outside_all_24_cores": True,
        "all_hit_intermediate_targets_retain_global_first_owner_audit": True,
        "hit_intermediate_closed_enclosure_contains_r0_boundary_trace": True,
        "hit_intermediate_regularity_claim_restricted_to_r_greater_than_0": True,
        "first_core_stopping_clock_origin": "source_collision_state_at_time_0",
        "source_to_regular_suffix_collisions_are_in_stopping_clock": True,
        "hit_source_to_regular_suffix_collision_offset": 2,
        "miss_source_to_regular_suffix_collision_offset": 1,
        "source_relative_first_core_stopping_cylinder_count": 128,
        "source_relative_first_core_time_histogram_by_oriented_cylinder": {
            "3": 22,
            "4": 32,
            "5": 18,
            "6": 8,
            "8": 8,
            "9": 12,
            "10": 8,
            "11": 4,
            "17": 2,
            "18": 2,
            "20": 4,
            "21": 6,
            "22": 2,
        },
        "maximum_source_relative_first_core_time": 22,
        "strict_preterminal_outside_all_24_core_state_count": 948,
        "strict_terminal_inside_one_core_state_count": 128,
        "total_source_relative_state_classification_count": 1076,
        "ambiguous_core_classification_count": 0,
        "distinct_destination_core_count": 14,
        "all_128_labelled_positive_cylinders_have_source_relative_first_core_stops": True,
        "source_state_rows_sha256": (
            "3ab17a4345afa5f46f18506a01aec3a6b37a5fc9b43110376eecf1462d936bb4"
        ),
        "hit_intermediate_state_rows_sha256": (
            "cf737396d2dd94041aa11788114dc972b98d4677fd7294f64f91a313cd8732a9"
        ),
        "source_relative_branch_rows_sha256": (
            "9010cb9515af8b3afe42f970434d74ab00f8278c664b85095312000efb43068a"
        ),
        "branch_key_to_source_relative_time_and_core_sha256": (
            "70ac25818c2652c3a3d518d5c25e1a638fb7a04b1faa3854943eb4dde9ef59ef"
        ),
        "parent_suffix_relative_branch_rows_sha256": (
            "46cb6480f28f202fc94ed85393138bffbcb2045a5ef79c4564e90372edaaf5d2"
        ),
        "destination_core_ids_sha256": (
            "5db145b1b1e93eb7286ca3ee6bf85862cbdf18f4f3e766a3d9fafad26413046b"
        ),
        "first_source_relative_branch_id": (
            "source-first-core:6cf00e1b10145761e269be6bda1270a42d9561875cc3f9423d659860b629e928"
        ),
        "last_source_relative_branch_id": (
            "source-first-core:e92651668f2092c7605bec8237e10357f9701b7fdcdfbe10ac5a8126e9dc841b"
        ),
    }


def expected_provenance() -> dict[str, Any]:
    return {
        "dependency_sha256": certificate.DEPENDENCIES,
        "old_artifacts_modified": False,
        "floating_search_role": "none_new_exact_Arb_replay",
        "admission_engine": "python-flint Arb",
        "precision_bits": 2048,
        "classification_policy": "strict_trichotomy_fail_closed",
    }


def expected_scope() -> dict[str, Any]:
    return {
        "positive_cylinders_cover_entire_maximal_rows": False,
        "positive_cylinders_cover_whole_all_scale_germs": False,
        "labelled_coordinate_volume_is_collision_SRB_fraction": False,
        "singular_r0_boundary_is_a_regular_collision": False,
        "full_physical_source_core_first_return_partition": "NOT_CERTIFIED",
        "quantitative_collision_SRB_cemetery_tail": "NOT_CERTIFIED",
        "post_core_induced_return_operator": "NOT_CERTIFIED",
        "common_two_view_strong_restriction": "NOT_CERTIFIED",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
    }


def expected_verdict() -> dict[str, Any]:
    return {
        "source_relative_first_core_stopping_cylinders_128": "CERTIFIED",
        "source_states_outside_core_64": "CERTIFIED",
        "hit_pre_suffix_states_outside_core_64": "CERTIFIED",
        "maximum_source_relative_first_core_time_22": "CERTIFIED",
        "full_physical_first_return_partition": "NOT_CERTIFIED",
        "collision_SRB_cemetery_tail": "NOT_CERTIFIED",
        "induced_core_return_operator": "NOT_CERTIFIED",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
    }


def check(manifest: Any) -> list[str]:
    errors: list[str] = []
    if sys.flags.optimize != 0:
        errors.append("optimized Python disabled")
    if not isinstance(manifest, dict):
        return errors + ["manifest type"]
    if set(manifest) != {
        "schema",
        "certificate_sha256",
        "verifier_sha256",
        "dependencies",
        "result",
        "verdict",
    }:
        errors.append("manifest key set")
    if manifest.get("schema") != SCHEMA:
        errors.append("manifest schema")
    actual_certificate_hash = sha256_path(CERTIFICATE)
    if actual_certificate_hash != EXPECTED_CERTIFICATE_SHA256:
        errors.append("frozen certificate hash")
    if manifest.get("certificate_sha256") != EXPECTED_CERTIFICATE_SHA256:
        errors.append("certificate hash")
    if manifest.get("verifier_sha256") != sha256_path(Path(__file__)):
        errors.append("verifier hash")
    if not same(manifest.get("dependencies"), certificate.DEPENDENCIES):
        errors.append("dependency table")

    result = manifest.get("result")
    if not isinstance(result, dict):
        return errors + ["result type"]
    if set(result) != {
        "schema",
        "provenance",
        "source_relative_first_core_stopping_registry",
        "strict_nonpromotion",
        "internal_replay_digest",
    }:
        errors.append("result key set")
    if result.get("schema") != RESULT_SCHEMA:
        errors.append("result schema")
    if result.get("internal_replay_digest") != result_digest(result):
        errors.append("result digest")
    if not same(result.get("provenance"), expected_provenance()):
        errors.append("provenance")
    if not same(
        result.get("source_relative_first_core_stopping_registry"),
        expected_registry(),
    ):
        errors.append("source-relative registry")
    if not same(result.get("strict_nonpromotion"), expected_scope()):
        errors.append("strict nonpromotion")
    if not same(manifest.get("verdict"), expected_verdict()):
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

    registry = ("result", "source_relative_first_core_stopping_registry")
    mutate(registry + ("maximal_reference_occurrence_count",), 63)
    mutate(registry + ("charged_oriented_cylinder_count",), 127)
    mutate(registry + ("shared_source_state_classification_count",), 63)
    mutate(registry + ("source_state_branch_reference_count",), 127)
    mutate(
        registry + ("hit_pre_suffix_intermediate_state_classification_count",),
        63,
    )
    mutate(registry + ("unique_pre_suffix_classification_row_count",), 127)
    mutate(
        registry + ("all_64_source_states_strictly_outside_all_24_cores",),
        False,
    )
    mutate(
        registry
        + ("all_64_hit_intermediate_states_strictly_outside_all_24_cores",),
        False,
    )
    mutate(
        registry + ("all_hit_intermediate_targets_retain_global_first_owner_audit",),
        False,
    )
    mutate(
        registry + ("hit_intermediate_closed_enclosure_contains_r0_boundary_trace",),
        False,
    )
    mutate(
        registry + ("hit_intermediate_regularity_claim_restricted_to_r_greater_than_0",),
        False,
    )
    mutate(registry + ("first_core_stopping_clock_origin",), "regular_suffix_state_at_time_0")
    mutate(registry + ("source_to_regular_suffix_collisions_are_in_stopping_clock",), False)
    mutate(registry + ("hit_source_to_regular_suffix_collision_offset",), 1)
    mutate(registry + ("miss_source_to_regular_suffix_collision_offset",), 2)
    mutate(registry + ("source_relative_first_core_stopping_cylinder_count",), 127)
    changed_histogram = copy.deepcopy(
        expected_registry()[
            "source_relative_first_core_time_histogram_by_oriented_cylinder"
        ]
    )
    changed_histogram["3"] = 21
    changed_histogram["4"] = 33
    mutate(
        registry + ("source_relative_first_core_time_histogram_by_oriented_cylinder",),
        changed_histogram,
    )
    mutate(registry + ("maximum_source_relative_first_core_time",), 21)
    mutate(registry + ("strict_preterminal_outside_all_24_core_state_count",), 947)
    mutate(registry + ("strict_terminal_inside_one_core_state_count",), 127)
    mutate(registry + ("total_source_relative_state_classification_count",), 1075)
    mutate(registry + ("ambiguous_core_classification_count",), 1)
    mutate(registry + ("distinct_destination_core_count",), 13)
    mutate(
        registry
        + ("all_128_labelled_positive_cylinders_have_source_relative_first_core_stops",),
        False,
    )
    for field in (
        "source_state_rows_sha256",
        "hit_intermediate_state_rows_sha256",
        "source_relative_branch_rows_sha256",
        "branch_key_to_source_relative_time_and_core_sha256",
        "parent_suffix_relative_branch_rows_sha256",
        "destination_core_ids_sha256",
    ):
        mutate(registry + (field,), "0" * 64)
    mutate(registry + ("first_source_relative_branch_id",), "source-first-core:" + "0" * 64)
    mutate(registry + ("last_source_relative_branch_id",), "source-first-core:" + "0" * 64)
    mutate(("result", "provenance", "precision_bits"), 1024)
    mutate(("result", "provenance", "classification_policy"), "infer_outside")
    mutate(("result", "provenance", "old_artifacts_modified"), True)
    scope = ("result", "strict_nonpromotion")
    mutate(scope + ("positive_cylinders_cover_entire_maximal_rows",), True)
    mutate(scope + ("positive_cylinders_cover_whole_all_scale_germs",), True)
    mutate(scope + ("labelled_coordinate_volume_is_collision_SRB_fraction",), True)
    mutate(scope + ("singular_r0_boundary_is_a_regular_collision",), True)
    mutate(scope + ("full_physical_source_core_first_return_partition",), "CERTIFIED")
    mutate(scope + ("quantitative_collision_SRB_cemetery_tail",), "CERTIFIED")
    mutate(scope + ("post_core_induced_return_operator",), "CERTIFIED")
    mutate(scope + ("common_two_view_strong_restriction",), "CERTIFIED")
    mutate(scope + ("Gate4",), "CERTIFIED")
    mutate(("verdict", "full_physical_first_return_partition"), "CERTIFIED")
    mutate(("verdict", "collision_SRB_cemetery_tail"), "CERTIFIED")
    mutate(("verdict", "induced_core_return_operator"), "CERTIFIED")
    mutate(("verdict", "Gate4"), "CERTIFIED")

    boolean_as_integer = copy.deepcopy(manifest)
    boolean_as_integer["result"]["source_relative_first_core_stopping_registry"][
        "all_64_source_states_strictly_outside_all_24_cores"
    ] = 1
    refresh(boolean_as_integer)
    mutations.append(boolean_as_integer)
    unknown_key = copy.deepcopy(manifest)
    unknown_key["result"]["source_relative_first_core_stopping_registry"][
        "unknown"
    ] = 0
    refresh(unknown_key)
    mutations.append(unknown_key)
    unknown_top = copy.deepcopy(manifest)
    unknown_top["unknown"] = 0
    mutations.append(unknown_top)
    rejected = sum(bool(check(candidate)) for candidate in mutations)
    return rejected, len(mutations)


def load_manifest(path: Path) -> dict[str, Any]:
    if path.is_symlink():
        raise ValueError("manifest symlink rejected")
    return json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=reject_duplicate_keys,
        parse_constant=lambda token: (_ for _ in ()).throw(
            ValueError(f"invalid JSON constant: {token}")
        ),
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--replay", action="store_true")
    modes.add_argument("--integrity-only", action="store_true")
    modes.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        manifest = load_manifest(args.manifest)
    except Exception as error:
        print(f"MANIFEST_READ_ERROR: {error}", file=sys.stderr)
        return 1
    errors = check(manifest)
    if errors:
        print("ERROR: " + "; ".join(errors), file=sys.stderr)
        return 1
    if args.replay and not same(certificate.build_result(), manifest["result"]):
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
    print("SOURCE_RELATIVE_FIRST_CORE_STOPPING_CYLINDERS_128: CERTIFIED")
    print("SOURCE_STATES_OUTSIDE_CORE_64: CERTIFIED")
    print("HIT_PRE_SUFFIX_STATES_OUTSIDE_CORE_64: CERTIFIED")
    print("MAXIMUM_SOURCE_RELATIVE_FIRST_CORE_TIME_22: CERTIFIED")
    print("FULL_PHYSICAL_FIRST_RETURN_PARTITION: NOT_CERTIFIED")
    print("COLLISION_SRB_CEMETERY_TAIL: NOT_CERTIFIED")
    print("INDUCED_CORE_RETURN_OPERATOR: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
