#!/usr/bin/env python3
"""Fail-closed verifier for uniform boundary-carrier patches."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import cm2_gate34_uniform_boundary_carrier_patch_cert as certificate


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate34.uniform-boundary-carrier-patch.manifest.v1"
RESULT_SCHEMA = "cm2.gate34.uniform-boundary-carrier-patch.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate34-uniform-boundary-carrier-patch-manifest-2026-07-17.json"
)
CERTIFICATE = HERE / "cm2_gate34_uniform_boundary_carrier_patch_cert.py"


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

    registry = result.get("uniform_boundary_carrier_patch_registry", {})
    expected = {
        "uniform_positive_width_patch_count": 64,
        "patch_half_width_in_both_z_and_s": "1/1024",
        "per_patch_event_coordinate_area": "1/262144",
        "labelled_occurrence_sheet_coproduct_area": "1/4096",
        "all_patches_strictly_inside_parameter_and_chart_windows": True,
        "all_patches_have_one_immutable_physical_label": True,
        "all_patches_map_to_one_regular_suffix_collision_chart": True,
        "all_64_boundary_carriers_receive_one_patch": True,
    }
    for key, value in expected.items():
        if registry.get(key) != value:
            errors.append(f"registry {key}")
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
    expected_bounds = {
        "source_cosine_strict_lower": "1/10",
        "source_abs_p_strict_upper": "199/200",
        "post_tangent_flight_gap_strict_lower": "1/5",
        "common_miss_flight_strict_upper": "2",
        "common_miss_abs_p_strict_upper": "199/200",
        "common_miss_cosine_strict_lower": "1/10",
    }
    if registry.get("uniform_patch_bounds") != expected_bounds:
        errors.append("patch bounds")
    for key in (
        "patch_rows_sha256",
        "imported_carrier_rows_sha256",
        "imported_maximal_rows_sha256",
    ):
        if not isinstance(registry.get(key), str) or not registry[key]:
            errors.append(f"registry digest {key}")

    scope = result.get("strict_nonpromotion", {})
    for key in (
        "event_sheet_patch_is_two_sided_transverse_shell",
        "labelled_event_coordinate_area_is_collision_SRB_mass",
        "regular_suffix_chart_is_24_core_destination",
    ):
        if scope.get(key) is not False:
            errors.append(f"nonpromotion {key}")
    for key in (
        "two_sided_open_shell_transport",
        "first_24_core_destination",
        "native_no_recut_dwell",
        "common_strong_space_restriction",
        "Gate3",
        "Gate4",
    ):
        if scope.get(key) != "NOT_CERTIFIED":
            errors.append(f"scope {key}")

    expected_verdict = {
        "uniform_boundary_carrier_patches_64": "CERTIFIED",
        "regular_suffix_collision_charts_64": "CERTIFIED",
        "two_sided_open_shell_transport": "NOT_CERTIFIED",
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

    mutate(("result", "uniform_boundary_carrier_patch_registry", "uniform_positive_width_patch_count"), 63)
    mutate(("result", "uniform_boundary_carrier_patch_registry", "patch_half_width_in_both_z_and_s"), "0")
    mutate(("result", "uniform_boundary_carrier_patch_registry", "per_patch_event_coordinate_area"), "0")
    mutate(("result", "uniform_boundary_carrier_patch_registry", "all_patches_have_one_immutable_physical_label"), False)
    mutate(("result", "uniform_boundary_carrier_patch_registry", "all_patches_map_to_one_regular_suffix_collision_chart"), False)
    mutate(("result", "uniform_boundary_carrier_patch_registry", "suffix_regular_chart_histogram", "G:E"), 9)
    mutate(("result", "uniform_boundary_carrier_patch_registry", "uniform_patch_bounds", "common_miss_cosine_strict_lower"), "0")
    mutate(("result", "uniform_boundary_carrier_patch_registry", "patch_rows_sha256"), "")
    mutate(("result", "strict_nonpromotion", "event_sheet_patch_is_two_sided_transverse_shell"), True)
    mutate(("result", "strict_nonpromotion", "labelled_event_coordinate_area_is_collision_SRB_mass"), True)
    mutate(("result", "strict_nonpromotion", "regular_suffix_chart_is_24_core_destination"), True)
    mutate(("result", "strict_nonpromotion", "two_sided_open_shell_transport"), "CERTIFIED")
    mutate(("result", "strict_nonpromotion", "first_24_core_destination"), "CERTIFIED")
    mutate(("result", "strict_nonpromotion", "native_no_recut_dwell"), "CERTIFIED")
    mutate(("result", "strict_nonpromotion", "Gate3"), "CERTIFIED")
    mutate(("result", "strict_nonpromotion", "Gate4"), "CERTIFIED")
    mutate(("verdict", "first_24_core_destination"), "CERTIFIED")
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
    print("UNIFORM_BOUNDARY_CARRIER_PATCHES_64: CERTIFIED")
    print("REGULAR_SUFFIX_COLLISION_CHARTS_64: CERTIFIED")
    print("TWO_SIDED_OPEN_SHELL_TRANSPORT: NOT_CERTIFIED")
    print("FIRST_24_CORE_DESTINATION: NOT_CERTIFIED")
    print("GATE3: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
