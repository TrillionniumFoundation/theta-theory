#!/usr/bin/env python3
"""Fail-closed verifier for the dyadic transverse recovery shells."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import cm2_gate34_dyadic_transverse_recovery_shell_cert as certificate


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate34.dyadic-transverse-recovery-shell.manifest.v1"
RESULT_SCHEMA = "cm2.gate34.dyadic-transverse-recovery-shell.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate34-dyadic-transverse-recovery-shell-manifest-2026-07-17.json"
)
CERTIFICATE = HERE / "cm2_gate34_dyadic_transverse_recovery_shell_cert.py"


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

    registry = result.get("dyadic_transverse_recovery_shell_registry", {})
    expected = {
        "occurrence_shell_count": 64,
        "oriented_transverse_tube_count": 128,
        "angle_magnitude_interval": ["1/65536", "1/32768"],
        "hit_angle_sign_equals_tangency_epsilon": True,
        "miss_angle_sign_equals_negative_tangency_epsilon": True,
        "base_half_width_power_histogram": {"10": 36, "11": 24, "12": 4},
        "labelled_base_event_coordinate_area": "169/1048576",
        "labelled_two_side_coordinate_volume": "169/34359738368",
        "all_hit_tubes_first_hit_tangent_target": True,
        "all_hit_tubes_next_hit_fixed_miss_target": True,
        "all_miss_tubes_first_hit_fixed_miss_target": True,
        "all_two_side_successors_regular": True,
        "all_two_side_successors_share_one_suffix_chart_per_occurrence": True,
    }
    for key, value in expected.items():
        if registry.get(key) != value:
            errors.append(f"registry {key}")
    universe = registry.get("complete_local_candidate_universe", {})
    if universe.get("candidate_count_after_exclusion") != 161:
        errors.append("candidate count")
    if universe.get("window_radius_4_exceeds_required_center_offset") is not True:
        errors.append("candidate completeness")
    expected_bounds = {
        "cosine_strict_lower": "1/20",
        "abs_p_strict_upper": "999/1000",
        "each_owner_flight_strict_upper": "2",
    }
    if registry.get("uniform_suffix_bounds") != expected_bounds:
        errors.append("suffix bounds")
    expected_suffix = {
        "G:E": 10,
        "G:N": 12,
        "G:S": 12,
        "G:W": 10,
        "W:E": 4,
        "W:N": 6,
        "W:S": 6,
        "W:W": 4,
    }
    if registry.get("suffix_regular_chart_histogram") != expected_suffix:
        errors.append("suffix histogram")
    for key in ("shell_rows_sha256", "imported_maximal_rows_sha256"):
        if not isinstance(registry.get(key), str) or not registry[key]:
            errors.append(f"registry digest {key}")

    scope = result.get("strict_nonpromotion", {})
    for key in (
        "phase_angle_shell_is_actual_parameter_DQ_transverse_coordinate",
        "one_dyadic_shell_is_uniform_all_scale_shell_family",
        "common_suffix_chart_means_identical_hit_miss_state",
    ):
        if scope.get(key) is not False:
            errors.append(f"nonpromotion {key}")
    for key in (
        "bounded_grazing_pushforward",
        "first_24_core_destination",
        "native_no_recut_dwell",
        "common_strong_space_restriction",
        "Gate3",
        "Gate4",
    ):
        if scope.get(key) != "NOT_CERTIFIED":
            errors.append(f"scope {key}")

    expected_verdict = {
        "dyadic_transverse_recovery_shells_64": "CERTIFIED",
        "oriented_phase_space_tubes_128": "CERTIFIED",
        "common_regular_suffix_charts_64": "CERTIFIED",
        "parameter_DQ_transverse_shell_family": "NOT_CERTIFIED",
        "first_24_core_destination": "NOT_CERTIFIED",
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

    mutate(("result", "dyadic_transverse_recovery_shell_registry", "occurrence_shell_count"), 63)
    mutate(("result", "dyadic_transverse_recovery_shell_registry", "oriented_transverse_tube_count"), 126)
    mutate(("result", "dyadic_transverse_recovery_shell_registry", "angle_magnitude_interval"), ["0", "0"])
    mutate(("result", "dyadic_transverse_recovery_shell_registry", "base_half_width_power_histogram", "10"), 35)
    mutate(("result", "dyadic_transverse_recovery_shell_registry", "all_hit_tubes_first_hit_tangent_target"), False)
    mutate(("result", "dyadic_transverse_recovery_shell_registry", "all_hit_tubes_next_hit_fixed_miss_target"), False)
    mutate(("result", "dyadic_transverse_recovery_shell_registry", "all_miss_tubes_first_hit_fixed_miss_target"), False)
    mutate(("result", "dyadic_transverse_recovery_shell_registry", "all_two_side_successors_regular"), False)
    mutate(("result", "dyadic_transverse_recovery_shell_registry", "uniform_suffix_bounds", "cosine_strict_lower"), "0")
    mutate(("result", "dyadic_transverse_recovery_shell_registry", "complete_local_candidate_universe", "candidate_count_after_exclusion"), 160)
    mutate(("result", "strict_nonpromotion", "phase_angle_shell_is_actual_parameter_DQ_transverse_coordinate"), True)
    mutate(("result", "strict_nonpromotion", "one_dyadic_shell_is_uniform_all_scale_shell_family"), True)
    mutate(("result", "strict_nonpromotion", "common_suffix_chart_means_identical_hit_miss_state"), True)
    mutate(("result", "strict_nonpromotion", "bounded_grazing_pushforward"), "CERTIFIED")
    mutate(("result", "strict_nonpromotion", "first_24_core_destination"), "CERTIFIED")
    mutate(("result", "strict_nonpromotion", "native_no_recut_dwell"), "CERTIFIED")
    mutate(("result", "strict_nonpromotion", "Gate3"), "CERTIFIED")
    mutate(("result", "strict_nonpromotion", "Gate4"), "CERTIFIED")
    mutate(("verdict", "parameter_DQ_transverse_shell_family"), "CERTIFIED")
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
    print("DYADIC_TRANSVERSE_RECOVERY_SHELLS_64: CERTIFIED")
    print("ORIENTED_PHASE_SPACE_TUBES_128: CERTIFIED")
    print("COMMON_REGULAR_SUFFIX_CHARTS_64: CERTIFIED")
    print("PARAMETER_DQ_TRANSVERSE_SHELL_FAMILY: NOT_CERTIFIED")
    print("FIRST_24_CORE_DESTINATION: NOT_CERTIFIED")
    print("GATE3: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
