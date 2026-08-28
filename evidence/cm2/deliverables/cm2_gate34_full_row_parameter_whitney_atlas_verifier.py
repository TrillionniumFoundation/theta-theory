#!/usr/bin/env python3
"""Fail-closed verifier for the full-row parameter Whitney germ atlas."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import cm2_gate34_full_row_parameter_whitney_atlas_cert as certificate


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate34.full-row-parameter-whitney-atlas.manifest.v1"
RESULT_SCHEMA = "cm2.gate34.full-row-parameter-whitney-atlas.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate34-full-row-parameter-whitney-atlas-manifest-2026-07-17.json"
)
CERTIFICATE = HERE / "cm2_gate34_full_row_parameter_whitney_atlas_cert.py"


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

    endpoints = result.get("endpoint_incidence_and_atoms", {})
    expected_endpoints = {
        "reference_maximal_row_count": 64,
        "endpoint_incidence_count": 128,
        "endpoint_incidence_histogram": {
            "parameter_polarity": 16,
            "physical_earlier_occlusion_boundary": 16,
            "physical_later_miss_switch_boundary": 64,
            "source_grazing": 32,
        },
        "source_grazing_density_vanishes_by_cp": True,
        "parameter_polarity_density_vanishes_by_abs_u_y": True,
        "first_visibility_and_miss_switch_endpoints_have_zero_base_mass": True,
        "extra_endpoint_atoms": 0,
    }
    for key, value in expected_endpoints.items():
        if endpoints.get(key) != value:
            errors.append(f"endpoint {key}")

    atlas = result.get("countable_full_row_parameter_germ_atlas", {})
    expected_true = (
        "countable_cells_cover_every_reference_row_interior_point",
        "every_cell_closure_is_compact_inside_one_constant_label_row",
        "strict_predicate_universe_is_finite_on_each_occurrence",
        "moving_centres_and_regular_competitor_roots_are_continuous",
        "correct_hit_side_tangent_discriminant_has_positive_linear_factor",
        "hit_tangent_miss_and_direct_miss_itineraries_persist_on_each_cell",
        "positive_cell_radius_exists_by_compactness",
        "dyadic_halving_of_parameter_radius_is_a_terminating_certificate_search",
        "all_interior_points_have_two_actual_parameter_all_scale_germs",
        "all_64_reference_rows_have_countable_actual_parameter_germ_atlas",
        "finite_prefix_positive_mass_tail_tends_to_zero",
        "finite_prefix_graph_TV_tail_tends_to_zero",
    )
    if atlas.get("reference_parameter") != "s=0":
        errors.append("atlas reference parameter")
    if atlas.get("normalized_row_domain") != "t in (0,1)":
        errors.append("atlas normalized domain")
    for key in expected_true:
        if atlas.get(key) is not True:
            errors.append(f"atlas {key}")
    if atlas.get("uniform_radius_over_all_cells_asserted") is not False:
        errors.append("atlas uniform radius nonclaim")

    prefix = result.get("materialized_level_16_prefix", {})
    expected_prefix = {
        "materialized_maximum_whitney_level": 16,
        "cells_per_row": 31,
        "materialized_whitney_cell_count": 1984,
        "materialized_oriented_parameter_germ_record_count": 3968,
        "covered_normalized_reference_row": [
            "1/131072", "131071/131072_open",
        ],
        "omitted_normalized_endpoint_length_per_row": "1/65536",
        "positive_coarea_mass_tail_upper": "63/2560",
        "hit_minus_miss_graph_TV_tail_upper": "63/1280",
        "tail_bounds_use_row_angle_width_strict_upper_2pi_lt_7": True,
    }
    for key, value in expected_prefix.items():
        if prefix.get(key) != value:
            errors.append(f"prefix {key}")
    for key in ("materialized_cells_sha256", "first_cell_id", "last_cell_id"):
        if not isinstance(prefix.get(key), str) or not prefix[key]:
            errors.append(f"prefix digest {key}")

    scope = result.get("strict_nonpromotion", {})
    for key in (
        "countable_pointwise_germ_atlas_is_finite_uniform_radius_atlas",
        "order_zero_tail_implies_common_strong_space_pushforward",
        "local_radius_existence_supplies_weighted_radius_summability",
    ):
        if scope.get(key) is not False:
            errors.append(f"nonpromotion {key}")
    for key in (
        "finite_s_future_singularity_atlas",
        "bounded_common_strong_space_grazing_pushforward",
        "strong_DQ_MT_DQ_FACE",
        "Gate3",
        "Gate4",
    ):
        if scope.get(key) != "NOT_CERTIFIED":
            errors.append(f"scope {key}")

    expected_verdict = {
        "reference_full_row_countable_parameter_germ_atlas_64": "CERTIFIED",
        "materialized_Whitney_cells_1984": "CERTIFIED",
        "materialized_oriented_parameter_germ_records_3968": "CERTIFIED",
        "level16_graph_TV_endpoint_tail_le_63_over_1280": "CERTIFIED",
        "bounded_common_strong_space_grazing_pushforward": "NOT_CERTIFIED",
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

    endpoint = ("result", "endpoint_incidence_and_atoms")
    mutate(endpoint + ("reference_maximal_row_count",), 63)
    mutate(endpoint + ("endpoint_incidence_count",), 127)
    mutate(endpoint + ("extra_endpoint_atoms",), 1)
    mutate(endpoint + ("source_grazing_density_vanishes_by_cp",), False)
    atlas = ("result", "countable_full_row_parameter_germ_atlas")
    mutate(atlas + ("normalized_row_domain",), "closed")
    mutate(atlas + ("countable_cells_cover_every_reference_row_interior_point",), False)
    mutate(atlas + ("positive_cell_radius_exists_by_compactness",), False)
    mutate(atlas + ("dyadic_halving_of_parameter_radius_is_a_terminating_certificate_search",), False)
    mutate(atlas + ("all_interior_points_have_two_actual_parameter_all_scale_germs",), False)
    mutate(atlas + ("uniform_radius_over_all_cells_asserted",), True)
    prefix = ("result", "materialized_level_16_prefix")
    mutate(prefix + ("materialized_maximum_whitney_level",), 15)
    mutate(prefix + ("cells_per_row",), 30)
    mutate(prefix + ("materialized_whitney_cell_count",), 1983)
    mutate(prefix + ("materialized_oriented_parameter_germ_record_count",), 3966)
    mutate(prefix + ("positive_coarea_mass_tail_upper",), "0")
    mutate(prefix + ("hit_minus_miss_graph_TV_tail_upper",), "0")
    scope = ("result", "strict_nonpromotion")
    mutate(scope + ("countable_pointwise_germ_atlas_is_finite_uniform_radius_atlas",), True)
    mutate(scope + ("order_zero_tail_implies_common_strong_space_pushforward",), True)
    mutate(scope + ("bounded_common_strong_space_grazing_pushforward",), "CERTIFIED")
    mutate(scope + ("strong_DQ_MT_DQ_FACE",), "CERTIFIED")
    mutate(scope + ("Gate3",), "CERTIFIED")
    mutate(("verdict", "bounded_common_strong_space_grazing_pushforward"), "CERTIFIED")
    mutate(("verdict", "Gate3"), "CERTIFIED")
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
    print("REFERENCE_FULL_ROW_COUNTABLE_PARAMETER_GERM_ATLAS_64: CERTIFIED")
    print("MATERIALIZED_WHITNEY_CELLS_1984: CERTIFIED")
    print("MATERIALIZED_ORIENTED_PARAMETER_GERM_RECORDS_3968: CERTIFIED")
    print("LEVEL16_GRAPH_TV_ENDPOINT_TAIL_LE_63_OVER_1280: CERTIFIED")
    print("BOUNDED_COMMON_STRONG_SPACE_GRAZING_PUSHFORWARD: NOT_CERTIFIED")
    print("GATE3: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
