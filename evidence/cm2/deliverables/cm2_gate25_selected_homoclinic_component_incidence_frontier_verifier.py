#!/usr/bin/env python3
"""Fail-closed verifier for selected QNL/component incidence."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import cm2_gate25_selected_homoclinic_component_incidence_frontier_cert as certificate


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate25.selected-homoclinic-component-incidence-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate25.selected-homoclinic-component-incidence-frontier.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate25-selected-homoclinic-component-incidence-frontier-manifest-2026-07-16.json"
)
CERTIFICATE = (
    HERE / "cm2_gate25_selected_homoclinic_component_incidence_frontier_cert.py"
)


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
    if dependencies != certificate.EXPECTED_HASHES:
        errors.append("dependency ledger mismatch")
    else:
        for name, expected in dependencies.items():
            path = HERE / name
            if not path.is_file() or sha256_path(path) != expected:
                errors.append(f"dependency hash mismatch: {name}")

    result = data.get("result")
    if not isinstance(result, dict):
        return errors + ["result missing"]
    if result.get("schema") != RESULT_SCHEMA:
        errors.append("result schema mismatch")
    if result.get("internal_replay_digest") != result_digest(result):
        errors.append("internal replay digest mismatch")
    provenance = result.get("provenance", {})
    if provenance.get("frozen_dependency_sha256") != dependencies:
        errors.append("result dependency binding mismatch")

    point = result.get("selected_point_physical_enclosure", {})
    if point.get("physical_source_obstacle") != "G[0,0]":
        errors.append("source obstacle mismatch")
    if point.get("physical_parameter") != "s=0":
        errors.append("selected parameter mismatch")
    if point.get("first_Q5_collision_target") != "W[0,0]":
        errors.append("first Q5 target mismatch")
    strict = point.get("strict_rational_enclosure", {})
    if strict.get("t") != ["69/100", "35355339059327/50000000000000"]:
        errors.append("selected t enclosure mismatch")
    if strict.get("p=sin(phi)") != ["-1/50", "1/50"]:
        errors.append("selected p enclosure mismatch")

    corridor = result.get("connected_physical_corridor_replay", {})
    if corridor.get("parameter_window") != ["-1/400", "1/400"]:
        errors.append("corridor parameter window mismatch")
    if corridor.get("physical_key") != ["G:E", "W[0,0]", [], 1]:
        errors.append("corridor key mismatch")
    replay = corridor.get("complete_retained_first_hit_replay", {})
    for key, expected in {
        "strict_first_hit": True,
        "transparent_wall_record": [],
        "incoming_and_outgoing_abs_p_strict_upper": "3/10",
        "incoming_and_outgoing_cos_phi_strict_lower": "19/20",
    }.items():
        if replay.get(key) != expected:
            errors.append(f"corridor replay mismatch: {key}")
    if corridor.get(
        "corridor_uniformly_inside_exact_word_chart_homogeneity_predicate"
    ) is not True:
        errors.append("corridor predicate inclusion missing")

    incidence = result.get("selected_occurrence_component_incidence", {})
    expected_incidence = {
        "physical_key": ["G:E", "W[0,0]", [], 1],
        "maximal_component_id": (
            "7359148da1c43a255f2238d9c831b8638f2c9885035034a5792699c968b2f3b5"
        ),
        "original_positive_seed_is_contained_in_corridor": True,
        "selected_homoclinic_point_is_strictly_inside_corridor_at_s0": True,
        "corridor_is_connected": True,
        "corridor_stays_strictly_below_E_N_source_chart_seam": True,
        "corridor_stays_inside_defining_component_predicate": True,
        "selected_occurrence_membership_in_one_of_24_maximal_word_components_certified": True,
    }
    for key, expected in expected_incidence.items():
        if incidence.get(key) != expected:
            errors.append(f"component incidence mismatch: {key}")

    nonpromotion = result.get("strict_nonpromotion", {})
    for key in (
        "collision_occurrence_incidence_is_a_stable_quotient_branch_label",
        "stable_saturated_product_base",
        "stable_projection_pi_s",
        "quotient_density_rho",
        "physical_reverse_weight_p_a",
        "same_carrier_endpoint_maps_X_a_Y_a",
        "PPE",
        "full_key_characteristic_boundary_Z",
    ):
        if nonpromotion.get(key) is not False:
            errors.append(f"overpromotion detected: {key}")
    if nonpromotion.get("complete_18_field_operator_block_count") != 0:
        errors.append("operator block overclaim")
    if nonpromotion.get("Gate2") != "NOT_CERTIFIED":
        errors.append("Gate2 overclaim")
    if nonpromotion.get("Gate5") != "NOT_CERTIFIED":
        errors.append("Gate5 overclaim")

    verdict = data.get("verdict", {})
    expected_verdict = {
        "selected_QNL_homoclinic_component_incidence": "CERTIFIED",
        "Gate2_stable_quotient_PPE": "NOT_CERTIFIED",
        "Gate5_complete_operator_blocks": "NOT_CERTIFIED",
        "Gate2": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
    }
    if verdict != expected_verdict:
        errors.append("top-level verdict mismatch")
    return errors


def refresh_digest(data: dict[str, Any]) -> None:
    data["result"]["internal_replay_digest"] = result_digest(data["result"])


def self_test(data: dict[str, Any]) -> tuple[int, int]:
    mutations: list[dict[str, Any]] = []

    def mutate(path: tuple[Any, ...], value: Any) -> None:
        candidate = copy.deepcopy(data)
        node: Any = candidate
        for part in path[:-1]:
            node = node[part]
        node[path[-1]] = value
        if path[0] == "result":
            refresh_digest(candidate)
        mutations.append(candidate)

    mutate(("result", "selected_point_physical_enclosure", "physical_parameter"), "all s")
    mutate(("result", "selected_point_physical_enclosure", "first_Q5_collision_target"), "G[0,0]")
    mutate(("result", "selected_point_physical_enclosure", "strict_rational_enclosure", "t"), ["0", "1"])
    mutate(("result", "connected_physical_corridor_replay", "parameter_window"), ["0", "0"])
    mutate(("result", "connected_physical_corridor_replay", "physical_key"), ["G:E", "W[1,1]", [], 1])
    mutate(("result", "connected_physical_corridor_replay", "complete_retained_first_hit_replay", "strict_first_hit"), False)
    mutate(("result", "connected_physical_corridor_replay", "complete_retained_first_hit_replay", "transparent_wall_record"), ["X+"])
    mutate(("result", "connected_physical_corridor_replay", "corridor_uniformly_inside_exact_word_chart_homogeneity_predicate"), False)
    mutate(("result", "selected_occurrence_component_incidence", "maximal_component_id"), "0" * 64)
    mutate(("result", "selected_occurrence_component_incidence", "selected_homoclinic_point_is_strictly_inside_corridor_at_s0"), False)
    mutate(("result", "selected_occurrence_component_incidence", "corridor_stays_strictly_below_E_N_source_chart_seam"), False)
    mutate(("result", "selected_occurrence_component_incidence", "selected_occurrence_membership_in_one_of_24_maximal_word_components_certified"), False)
    mutate(("result", "strict_nonpromotion", "stable_saturated_product_base"), True)
    mutate(("result", "strict_nonpromotion", "PPE"), True)
    mutate(("result", "strict_nonpromotion", "complete_18_field_operator_block_count"), 1)
    mutate(("result", "strict_nonpromotion", "Gate2"), "CERTIFIED")
    mutate(("verdict", "Gate5"), "CERTIFIED")
    rejected = sum(bool(check_structure(candidate)) for candidate in mutations)
    return rejected, len(mutations)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"MANIFEST_READ_ERROR: {exc}", file=sys.stderr)
        return 1
    errors = check_structure(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    if args.replay and certificate.build_result() != data["result"]:
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
    print("SELECTED_QNL_HOMOCLINIC_PHYSICAL_COMPONENT_INCIDENCE: CERTIFIED")
    print("GATE2_STABLE_QUOTIENT_PPE: NOT_CERTIFIED")
    print("GATE5_COMPLETE_OPERATOR_BLOCKS: NOT_CERTIFIED")
    print("GATE2: NOT_CERTIFIED")
    print("GATE5: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
