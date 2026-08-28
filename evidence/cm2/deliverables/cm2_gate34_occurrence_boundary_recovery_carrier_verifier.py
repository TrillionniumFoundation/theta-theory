#!/usr/bin/env python3
"""Fail-closed verifier for the 64 boundary recovery carriers."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import cm2_gate34_occurrence_boundary_recovery_carrier_cert as certificate


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate34.occurrence-boundary-recovery-carrier.manifest.v1"
RESULT_SCHEMA = "cm2.gate34.occurrence-boundary-recovery-carrier.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate34-occurrence-boundary-recovery-carrier-manifest-2026-07-17.json"
)
CERTIFICATE = HERE / "cm2_gate34_occurrence_boundary_recovery_carrier_cert.py"


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

    registry = result.get("boundary_recovery_carrier_registry", {})
    expected_registry = {
        "maximal_occurrence_row_count": 64,
        "oriented_hit_miss_trace_seed_count": 128,
        "common_boundary_recovery_carrier_count": 64,
        "distinct_shared_event_base_signature_count": 64,
        "Jx_reflection_carrier_pair_count": 32,
        "all_open_rows_have_analytic_boundary_continuation_carrier": True,
        "hit_collision_offset_to_common_carrier": 1,
        "miss_collision_offset_to_common_carrier": 0,
        "all_witness_common_collisions_strictly_regular": True,
    }
    for key, expected in expected_registry.items():
        if registry.get(key) != expected:
            errors.append(f"registry {key}")
    expected_types = {
        "G->W(graze)->G": 36,
        "G->W(graze)->W": 8,
        "W->G(graze)->G": 8,
        "W->G(graze)->W": 12,
    }
    if registry.get("type_histogram") != expected_types:
        errors.append("type histogram")
    if registry.get("epsilon_histogram") != {"-1": 32, "1": 32}:
        errors.append("epsilon histogram")
    expected_bounds = {
        "source_cosine_strict_lower": "3/20",
        "source_abs_p_strict_upper": "99/100",
        "post_tangent_flight_gap_strict_lower": "31/100",
        "common_miss_flight_strict_upper": "8/5",
        "common_miss_abs_p_strict_upper": "97/100",
        "common_miss_cosine_strict_lower": "6/25",
    }
    if registry.get("uniform_witness_bounds") != expected_bounds:
        errors.append("witness bounds")
    for key in (
        "carrier_rows_sha256",
        "reflection_pairs_sha256",
        "imported_maximal_rows_sha256",
        "first_carrier_id",
        "last_carrier_id",
    ):
        if not isinstance(registry.get(key), str) or not registry[key]:
            errors.append(f"registry digest {key}")

    frontier = result.get("physical_installation_frontier", {})
    for key in (
        "common_event_base_restriction_materialized",
        "boundary_collision_offsets_materialized",
    ):
        if frontier.get(key) is not True:
            errors.append(f"frontier {key}")
    for key in (
        "open_shell_neighborhood_transport",
        "uniform_full_open_row_homogeneity_margin",
        "first_24_core_destination",
        "native_2018_step_no_recut_dwell",
        "native_12108_step_no_recut_dwell",
        "bounded_pushforward_through_grazing_hit",
        "common_strong_space_restriction",
        "cemetery_payload",
        "Gate3",
        "Gate4",
    ):
        if frontier.get(key) != "NOT_CERTIFIED":
            errors.append(f"frontier scope {key}")

    scope = result.get("strict_nonpromotion", {})
    for key in (
        "boundary_carrier_equals_open_shell_recovery",
        "boundary_collision_offset_equals_native_transport_time",
        "witness_margin_equals_uniform_row_margin",
    ):
        if scope.get(key) is not False:
            errors.append(f"nonpromotion {key}")
    for key in (
        "transported_occurrence_to_24_core_incidence",
        "native_repeated_recovery",
        "Gate3",
        "Gate4",
    ):
        if scope.get(key) != "NOT_CERTIFIED":
            errors.append(f"scope {key}")

    expected_verdict = {
        "boundary_recovery_carriers_64": "CERTIFIED",
        "oriented_hit_miss_trace_seeds_128": "CERTIFIED",
        "boundary_hit_miss_collision_offsets_1_0": "CERTIFIED",
        "transported_occurrence_to_24_core_incidence": "NOT_CERTIFIED",
        "native_repeated_recovery": "NOT_CERTIFIED",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
    }
    if manifest.get("verdict") != expected_verdict:
        errors.append("verdict")
    return errors


def refresh(manifest: dict[str, Any]) -> None:
    manifest["result"]["internal_replay_digest"] = result_digest(manifest["result"])


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

    mutate(("result", "boundary_recovery_carrier_registry", "maximal_occurrence_row_count"), 63)
    mutate(("result", "boundary_recovery_carrier_registry", "oriented_hit_miss_trace_seed_count"), 64)
    mutate(("result", "boundary_recovery_carrier_registry", "common_boundary_recovery_carrier_count"), 63)
    mutate(("result", "boundary_recovery_carrier_registry", "Jx_reflection_carrier_pair_count"), 31)
    mutate(("result", "boundary_recovery_carrier_registry", "hit_collision_offset_to_common_carrier"), 0)
    mutate(("result", "boundary_recovery_carrier_registry", "all_witness_common_collisions_strictly_regular"), False)
    mutate(("result", "boundary_recovery_carrier_registry", "type_histogram", "G->W(graze)->G"), 35)
    mutate(("result", "boundary_recovery_carrier_registry", "epsilon_histogram", "-1"), 31)
    mutate(("result", "boundary_recovery_carrier_registry", "uniform_witness_bounds", "common_miss_abs_p_strict_upper"), "1")
    mutate(("result", "physical_installation_frontier", "common_event_base_restriction_materialized"), False)
    mutate(("result", "physical_installation_frontier", "first_24_core_destination"), "CERTIFIED")
    mutate(("result", "physical_installation_frontier", "native_2018_step_no_recut_dwell"), "CERTIFIED")
    mutate(("result", "physical_installation_frontier", "common_strong_space_restriction"), "CERTIFIED")
    mutate(("result", "strict_nonpromotion", "boundary_carrier_equals_open_shell_recovery"), True)
    mutate(("result", "strict_nonpromotion", "boundary_collision_offset_equals_native_transport_time"), True)
    mutate(("result", "strict_nonpromotion", "transported_occurrence_to_24_core_incidence"), "CERTIFIED")
    mutate(("result", "strict_nonpromotion", "Gate4"), "CERTIFIED")
    mutate(("verdict", "transported_occurrence_to_24_core_incidence"), "CERTIFIED")
    mutate(("verdict", "native_repeated_recovery"), "CERTIFIED")
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
    print("BOUNDARY_RECOVERY_CARRIERS_64: CERTIFIED")
    print("ORIENTED_TRACE_SEEDS_128: CERTIFIED")
    print("BOUNDARY_HIT_MISS_COLLISION_OFFSETS_1_0: CERTIFIED")
    print("FIRST_24_CORE_DESTINATION: NOT_CERTIFIED")
    print("GATE3: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
