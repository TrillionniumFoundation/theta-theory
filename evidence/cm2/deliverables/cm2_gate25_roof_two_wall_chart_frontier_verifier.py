#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-2/5 roof-two wall-chart frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import cm2_gate25_roof_two_wall_chart_frontier_cert as certificate


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate25.roof-two-wall-chart-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate25.roof-two-wall-chart-frontier.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate25-roof-two-wall-chart-frontier-manifest-2026-07-16.json"
)
CERTIFICATE = HERE / "cm2_gate25_roof_two_wall_chart_frontier_cert.py"
EXPECTED_INTERNAL_REPLAY_DIGEST = (
    "d40503e8bf2fa322c2d93674c5a5e83d0465910fdeb68f6de644ad73ef1bd484"
)
EXPECTED_WALL_ROWS_DIGEST = (
    "d90848fb771435ea1a4117b95ff2165d83da24e4f87fa49c4be367f039500490"
)
EXPECTED_SUFFIX_SUBDIVISION_DIGEST = (
    "120d25d2b27ddc1f41a5aa4e19858751bfbaf3ea25245afe82d425d4170ccd47"
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def result_digest(result: dict[str, Any]) -> str:
    payload = copy.deepcopy(result)
    payload.pop("internal_replay_digest", None)
    return canonical_digest(payload)


def check_structure(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["manifest is not an object"]
    if data.get("schema") != SCHEMA:
        errors.append("manifest schema mismatch")
    if data.get("certificate_sha256") != sha256_path(CERTIFICATE):
        errors.append("certificate hash mismatch")
    if data.get("verifier_sha256") != sha256_path(Path(__file__)):
        errors.append("verifier hash mismatch")

    dependencies = data.get("dependencies")
    if not isinstance(dependencies, dict) or len(dependencies) != 4:
        errors.append("dependency ledger mismatch")
    else:
        for name, expected in dependencies.items():
            path = HERE / name
            if not path.is_file():
                errors.append(f"missing dependency: {name}")
            elif sha256_path(path) != expected:
                errors.append(f"dependency hash mismatch: {name}")

    result = data.get("result")
    if not isinstance(result, dict):
        return errors + ["result missing"]
    if result.get("schema") != RESULT_SCHEMA:
        errors.append("result schema mismatch")
    if result.get("internal_replay_digest") != result_digest(result):
        errors.append("internal replay digest mismatch")
    if result.get("internal_replay_digest") != EXPECTED_INTERNAL_REPLAY_DIGEST:
        errors.append("frozen replay digest mismatch")

    provenance = result.get("provenance", {})
    if provenance.get("frozen_dependency_sha256") != dependencies:
        errors.append("result dependency binding mismatch")
    if provenance.get("arithmetic") != (
        "384-bit Arb first-order automatic differentiation"
    ):
        errors.append("arithmetic declaration mismatch")
    if provenance.get("parameter_window") != ["-1/400", "1/400"]:
        errors.append("parameter window mismatch")

    registry = result.get("roof_two_wall_chart_registry", {})
    expected_registry = {
        "roof_one_physical_core_count": 20,
        "roof_two_physical_core_count": 4,
        "intermediate_transparent_wall_chart_count": 4,
        "all_four_wall_crossings_unique_and_away_from_corners": True,
        "all_four_wall_charts_uniform_on_full_parameter_window": True,
        "all_four_wall_chart_maps_local_diffeomorphisms": True,
        "all_four_suffix_maps_certified_by_2x2x2_subdivision": True,
        "total_suffix_subdivision_cell_count": 32,
        "all_28_core_local_roof_level_prefix_suffix_pairs_have_charts": True,
        "all_52_core_local_split_slots_have_charts": True,
        "roof_two_wall_adjacent_local_chart_D_infinity_upper": "20",
        "wall_rows_sha256": EXPECTED_WALL_ROWS_DIGEST,
        "suffix_subdivision_digest_ledger_sha256": (
            EXPECTED_SUFFIX_SUBDIVISION_DIGEST
        ),
    }
    for key, expected in expected_registry.items():
        if registry.get(key) != expected:
            errors.append(f"registry field mismatch: {key}")

    wall_rows = registry.get("wall_rows")
    if not isinstance(wall_rows, list) or len(wall_rows) != 4:
        errors.append("wall row count mismatch")
    else:
        if canonical_digest(wall_rows) != registry.get("wall_rows_sha256"):
            errors.append("wall row digest mismatch")
        tokens = {row.get("wall_token") for row in wall_rows}
        if tokens != {"X+", "X-", "Y+", "Y-"}:
            errors.append("oriented wall token set mismatch")
        charts = {row.get("physical_key", [None])[0] for row in wall_rows}
        if charts != {"W:E", "W:W", "W:N", "W:S"}:
            errors.append("roof-two source chart set mismatch")
        for row in wall_rows:
            for key, expected in {
                "wall_time_strict_bounds": ["1/3", "7/20"],
                "wall_to_target_time_strict_bounds": ["33/100", "7/20"],
                "full_flight_time_strict_bounds": ["2/3", "7/10"],
                "wall_coordinate_strict_bounds": ["1/2", "53/100"],
                "distance_from_either_integer_corner_strict_lower": "47/100",
                "absolute_normal_velocity_strict_lower": "99/100",
                "absolute_tangential_velocity_strict_upper": "1/40",
                "source_core_to_wall_chart_D_infinity_strict_upper": "3",
                "wall_chart_to_source_core_D_infinity_strict_upper": "10",
                "absolute_chart_Jacobian_determinant_strict_lower_in_t_p": "3/20",
                "suffix_subdivision_t_p_s": [2, 2, 2],
                "suffix_subdivision_cell_count": 8,
                "all_suffix_cells_target_abs_t_and_p_strict_upper": "1/4",
                "all_suffix_cells_target_map_determinant_strict_lower": "1/10",
                "wall_to_target_local_collision_chart_D_infinity_strict_upper": "20",
                "target_local_collision_chart_to_wall_D_infinity_strict_upper": "20",
            }.items():
                if row.get(key) != expected:
                    errors.append(f"wall row field mismatch: {key}")

    suffix_ledger = registry.get("suffix_subdivision_digest_ledger")
    if not isinstance(suffix_ledger, list) or len(suffix_ledger) != 4:
        errors.append("suffix subdivision ledger count mismatch")
    elif canonical_digest(suffix_ledger) != registry.get(
        "suffix_subdivision_digest_ledger_sha256"
    ):
        errors.append("suffix subdivision ledger digest mismatch")

    limits = result.get("typing_limits", {})
    expected_limits = {
        "transparent_wall_is_not_a_collision_or_singularity": True,
        "wall_chart_cost_is_in_local_t_p_and_z_eta_coordinates": True,
        "wall_chart_cost_is_not_a_CM2_strong_operator_cost": True,
        "compact_cores_are_not_maximal_word_domains": True,
        "complete_full_key_18_field_block_count": 0,
        "completed_full_key_schema_field_count_on_each_of_24_keys": 1,
        "stable_saturated_Young_base": False,
        "stable_quotient_rho_reverse_kernel_PPE": False,
        "gate2": False,
        "gate5": False,
    }
    for key, expected in expected_limits.items():
        if limits.get(key) != expected:
            errors.append(f"typing limit mismatch: {key}")
    return errors


def refresh_result_digest(data: dict[str, Any]) -> None:
    result = data["result"]
    result["internal_replay_digest"] = result_digest(result)


def self_test(data: dict[str, Any]) -> tuple[int, int]:
    mutations: list[tuple[str, Any]] = []

    def mutate(name: str, path: tuple[Any, ...], value: Any) -> None:
        candidate = copy.deepcopy(data)
        node: Any = candidate
        for part in path[:-1]:
            node = node[part]
        node[path[-1]] = value
        if path[0] == "result":
            refresh_result_digest(candidate)
        mutations.append((name, candidate))

    mutate("roof-two count", ("result", "roof_two_wall_chart_registry", "roof_two_physical_core_count"), 5)
    mutate("wall chart count", ("result", "roof_two_wall_chart_registry", "intermediate_transparent_wall_chart_count"), 3)
    mutate("roof pair promotion", ("result", "roof_two_wall_chart_registry", "all_28_core_local_roof_level_prefix_suffix_pairs_have_charts"), False)
    mutate("split promotion", ("result", "roof_two_wall_chart_registry", "all_52_core_local_split_slots_have_charts"), False)
    mutate("chart cost", ("result", "roof_two_wall_chart_registry", "roof_two_wall_adjacent_local_chart_D_infinity_upper"), "21")
    mutate("wall rows digest", ("result", "roof_two_wall_chart_registry", "wall_rows_sha256"), "0" * 64)
    mutate("suffix ledger digest", ("result", "roof_two_wall_chart_registry", "suffix_subdivision_digest_ledger_sha256"), "0" * 64)
    mutate("strong cost overtype", ("result", "typing_limits", "wall_chart_cost_is_not_a_CM2_strong_operator_cost"), False)
    mutate("full block overtype", ("result", "typing_limits", "complete_full_key_18_field_block_count"), 1)
    mutate("full-key field overtype", ("result", "typing_limits", "completed_full_key_schema_field_count_on_each_of_24_keys"), 2)
    mutate("Gate2 overtype", ("result", "typing_limits", "gate2"), True)
    mutate("Gate5 overtype", ("result", "typing_limits", "gate5"), True)

    rejected = sum(bool(check_structure(candidate)) for _, candidate in mutations)
    return rejected, len(mutations)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    try:
        data = json.loads(args.manifest.read_text())
    except Exception as exc:
        print(f"MANIFEST_READ_ERROR: {exc}", file=sys.stderr)
        return 1
    errors = check_structure(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    if args.replay:
        replayed = certificate.build_result()
        if replayed != data["result"]:
            print("ERROR: full replay mismatch", file=sys.stderr)
            return 1

    if args.self_test:
        rejected, total = self_test(data)
        if rejected != total:
            print(f"SELF_TEST: FAIL ({rejected}/{total})", file=sys.stderr)
            return 1
        print(f"SELF_TEST: PASS ({rejected}/{total} mutations rejected)")
        return 0

    if args.replay or args.integrity_only:
        print("REPLAY_AND_INTEGRITY: PASS")
        return 0

    print("ROOF_TWO_INTERMEDIATE_TRANSPARENT_WALL_CHARTS: CERTIFIED")
    print("ALL_28_CORE_LOCAL_ROOF_LEVEL_CHART_PAIRS: CERTIFIED")
    print("ALL_52_CORE_LOCAL_SPLIT_CHART_SLOTS: CERTIFIED")
    print("COMPLETE_FULL_KEY_18_FIELD_BLOCK_COUNT: 0")
    print("GATE2_STABLE_QUOTIENT_PPE: NOT_CERTIFIED")
    print("GATE5: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
