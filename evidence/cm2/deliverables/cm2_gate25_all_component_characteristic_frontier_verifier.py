#!/usr/bin/env python3
"""Fail-closed verifier for the all-component characteristic certificate."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import cm2_gate25_all_component_characteristic_frontier_cert as certificate


Q = Fraction
HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate25.all-component-characteristic-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate25.all-component-characteristic-frontier.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate25-all-component-characteristic-frontier-manifest-2026-07-17.json"
)
CERTIFICATE = HERE / "cm2_gate25_all_component_characteristic_frontier_cert.py"


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
    else:
        for name, expected in certificate.DEPENDENCIES.items():
            path = HERE / name
            if not path.is_file() or sha256_path(path) != expected:
                errors.append(f"dependency {name}")

    result = manifest.get("result", {})
    if result.get("schema") != RESULT_SCHEMA:
        errors.append("result schema")
    if result.get("internal_replay_digest") != result_digest(result):
        errors.append("result digest")

    theorem = result.get("set_theoretic_boundary_inheritance", {})
    expected_theorem = {
        "boundary_inclusion_is_independent_of_nonemptiness_decision": True,
        "all_physical_branch_roots_are_isolated_on_canonical_unstable_curves": True,
        "one_root_upper_per_active_branch": True,
        "simultaneous_roots_charged_once": True,
        "curve_minus_m_roots_has_at_most_m_plus_one_open_intervals": True,
        "full_key_union_and_each_maximal_component_share_the_same_safe_upper": True,
        "component_enumeration_required_for_the_safe_upper": False,
        "curve_by_curve_numeric_root_order_required_for_the_safe_upper": False,
        "common_moving_DQ_atlas_constructed": False,
    }
    for key, expected in expected_theorem.items():
        if theorem.get(key) != expected:
            errors.append(f"boundary theorem {key}")

    registry = result.get("all_key_all_component_characteristic_registry", {})
    if registry.get("candidate_key_count_covered") != 441280:
        errors.append("key count")
    if registry.get("all_regular_key_fibres_covered_mod_declared_cemetery") is not True:
        errors.append("key coverage")
    if registry.get("all_maximal_connected_components_covered_without_enumeration") is not True:
        errors.append("component coverage")
    if registry.get("uniform_physical_boundary_root_upper_per_canonical_curve") != 289:
        errors.append("root upper")
    if registry.get("uniform_full_key_and_component_interval_upper_per_canonical_curve") != 290:
        errors.append("interval upper")
    if registry.get("uniform_unnormalized_characteristic_Z_multiplier_upper") != "580000/1999":
        errors.append("uniform Z")
    if registry.get("full_key_all_component_characteristic_boundary_Z") != "CERTIFIED":
        errors.append("full-key status")
    if registry.get("each_maximal_component_characteristic_boundary_Z") != "CERTIFIED":
        errors.append("component status")

    rows = registry.get("source_class_rows", [])
    if not isinstance(rows, list) or len(rows) != 2:
        errors.append("source rows")
    else:
        by_source = {row.get("source_obstacle"): row for row in rows}
        expected_rows = {
            "G": {
                "candidate_key_count": 224580,
                "physical_boundary_root_upper_per_canonical_curve": 289,
                "all_component_union_interval_upper_per_canonical_curve": 290,
                "all_component_unnormalized_characteristic_Z_multiplier_upper": "580000/1999",
                "restriction_then_physical_step_coefficient_upper": "208878184000000/720626832337",
            },
            "W": {
                "candidate_key_count": 216700,
                "physical_boundary_root_upper_per_canonical_curve": 285,
                "all_component_union_interval_upper_per_canonical_curve": 286,
                "all_component_unnormalized_characteristic_Z_multiplier_upper": "572000/1999",
                "restriction_then_physical_step_coefficient_upper": "205997105600000/720626832337",
            },
        }
        for source, expected in expected_rows.items():
            row = by_source.get(source, {})
            for key, value in expected.items():
                if row.get(key) != value:
                    errors.append(f"{source} {key}")
            if row.get("each_maximal_component_interval_upper_per_canonical_curve") != row.get(
                "all_component_union_interval_upper_per_canonical_curve"
            ):
                errors.append(f"{source} component inheritance")
            if row.get("restriction_then_physical_step_is_contraction") is not False:
                errors.append(f"{source} contraction scope")
            try:
                if Q(row["restriction_then_physical_step_coefficient_upper"]) <= 1:
                    errors.append(f"{source} noncontraction arithmetic")
            except Exception:
                errors.append(f"{source} fractions")

    fields = result.get("operator_field_frontier", {})
    expected_fields = {
        "full_key_field7_finite_characteristic_formula": "CERTIFIED",
        "same_formula_applies_to_each_eventual_homogeneous_slot": True,
        "field7_growth_contraction": False,
        "physical_homogeneous_subbranch_ids_materialized": False,
        "other_17_operator_fields_completed": False,
        "complete_18_field_operator_block_count": 0,
    }
    for key, expected in expected_fields.items():
        if fields.get(key) != expected:
            errors.append(f"field scope {key}")

    scope = result.get("strict_nonpromotion", {})
    for key in (
        "finite_characteristic_bound_implies_growth_contraction",
        "finite_characteristic_bound_implies_common_strong_space_DQ",
        "finite_characteristic_bound_implies_hereditary_repeated_recovery",
        "finite_characteristic_bound_implies_stable_quotient_or_PPE",
    ):
        if scope.get(key) is not False:
            errors.append(f"nonpromotion {key}")
    for key in ("Gate2", "Gate3", "Gate4", "Gate5"):
        if scope.get(key) != "NOT_CERTIFIED":
            errors.append(f"scope {key}")

    expected_verdict = {
        "all_441280_key_characteristic_boundary_Z": "CERTIFIED",
        "all_maximal_component_characteristic_boundary_Z": "CERTIFIED",
        "field7_growth_contraction": "NOT_CERTIFIED",
        "Gate2": "NOT_CERTIFIED",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
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

    mutate(("result", "set_theoretic_boundary_inheritance", "boundary_inclusion_is_independent_of_nonemptiness_decision"), False)
    mutate(("result", "set_theoretic_boundary_inheritance", "one_root_upper_per_active_branch"), False)
    mutate(("result", "set_theoretic_boundary_inheritance", "component_enumeration_required_for_the_safe_upper"), True)
    mutate(("result", "all_key_all_component_characteristic_registry", "candidate_key_count_covered"), 24)
    mutate(("result", "all_key_all_component_characteristic_registry", "uniform_physical_boundary_root_upper_per_canonical_curve"), 288)
    mutate(("result", "all_key_all_component_characteristic_registry", "uniform_full_key_and_component_interval_upper_per_canonical_curve"), 289)
    mutate(("result", "all_key_all_component_characteristic_registry", "uniform_unnormalized_characteristic_Z_multiplier_upper"), "1")
    mutate(("result", "all_key_all_component_characteristic_registry", "full_key_all_component_characteristic_boundary_Z"), "NOT_CERTIFIED")
    mutate(("result", "all_key_all_component_characteristic_registry", "source_class_rows"), [])
    mutate(("result", "operator_field_frontier", "field7_growth_contraction"), True)
    mutate(("result", "operator_field_frontier", "complete_18_field_operator_block_count"), 1)
    mutate(("result", "strict_nonpromotion", "finite_characteristic_bound_implies_common_strong_space_DQ"), True)
    mutate(("result", "strict_nonpromotion", "Gate5"), "CERTIFIED")
    mutate(("verdict", "Gate5"), "CERTIFIED")
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
    print("ALL_441280_KEYS_CHARACTERISTIC_BOUNDARY_Z: CERTIFIED")
    print("ALL_MAXIMAL_COMPONENTS_CHARACTERISTIC_BOUNDARY_Z: CERTIFIED")
    print("FIELD7_GROWTH_CONTRACTION: NOT_CERTIFIED")
    print("GATES_2_3_4_5: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
