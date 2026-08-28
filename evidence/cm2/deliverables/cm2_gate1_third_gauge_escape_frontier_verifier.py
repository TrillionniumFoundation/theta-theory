#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-1 third-gauge escape frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Callable

import cm2_gate1_third_gauge_escape_frontier_cert as certificate


HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = HERE / "cm2-gate1-third-gauge-escape-frontier-manifest-2026-07-17.json"
SCHEMA = "cm2.gate1.third-gauge-escape-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate1.third-gauge-escape-frontier.v1"


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("manifest root is not an object")
    return value


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("schema") != SCHEMA:
        errors.append("manifest schema mismatch")

    result = data.get("result", {})
    if result.get("schema") != RESULT_SCHEMA:
        errors.append("result schema mismatch")

    repair = result.get("periodic_first_jet_repair", {})
    expected_repair = {
        "lower_left_coefficient_update": "c_E=c+(nu-1)*X_21",
        "surjectivity_condition": "nu!=1",
        "exact_canceling_jet": "X_21=c/(1-nu)",
        "substitution": "c+(nu-1)*c/(1-nu)=0",
        "periodic_product_value_and_pinching_unchanged": True,
        "shadow_current_nonzero_coefficient_witness_can_be_removed": True,
        "connector_current_nonzero_coefficient_witness_can_be_removed": True,
        "removing_the_witness_proves_canonical_convergence": False,
    }
    for key, expected in expected_repair.items():
        if repair.get(key) != expected:
            errors.append(f"periodic repair mismatch: {key}")

    bump = result.get("disjoint_SL2_bump_escape", {})
    expected_bump = {
        "shadow_and_connector_orbits_disjoint_from_K": True,
        "finite_periodic_orbits_have_positive_distance_from_K": True,
        "two_bump_supports_are_mutually_disjoint": True,
        "each_support_avoids_all_other_points_of_both_periodic_orbits": True,
        "cutoff_is_one_near_basepoint": True,
        "cutoff_jet_at_basepoint": "chi(q_*)=1 and dchi(q_*)=0",
        "realized_first_jet": "dE_{q_*}[v_s]=M",
        "independent_shadow_and_connector_jets": True,
        "combined_correction_equals_identity_on_a_neighbourhood_of_K": True,
        "one_collision_cocycle_on_selected_orbit_unchanged": True,
        "all_selected_finite_holonomy_approximants_unchanged": True,
        "selected_infinite_loop_and_four_wedges_unchanged": True,
        "all_plaque_class_H_after_the_bumps": "NOT_CERTIFIED",
    }
    for key, expected in expected_bump.items():
        if bump.get(key) != expected:
            errors.append(f"disjoint bump mismatch: {key}")

    model = result.get("explicit_cohomologous_class_H_twisting_model", {})
    if model.get("rho") != "1/4":
        errors.append("toy rho mismatch")
    if model.get("constant_diagonal_cocycle_A") != [["2", "0"], ["0", "1/2"]]:
        errors.append("toy A mismatch")
    if model.get("A_belongs_to_Butler_Park_class_H") is not True:
        errors.append("toy diagonal class-H mismatch")
    if model.get("B_belongs_to_Butler_Park_class_H") is not True:
        errors.append("toy class-H mismatch")
    if model.get("B_is_weakly_typical") is not True:
        errors.append("toy weak typicality mismatch")
    if model.get("A_and_B_are_holder_cohomologous") is not True:
        errors.append("toy cohomology mismatch")
    if model.get("class_H_membership_changes_in_this_model") is not False:
        errors.append("toy class-H membership scope mismatch")
    if model.get("this_model_refutes_class_H_membership_invariance") is not False:
        errors.append("toy class-H invariance overclaim")
    if model.get("canonical_holonomy_family_is_holder_cohomology_invariant") is not False:
        errors.append("toy canonical holonomy invariance mismatch")
    if model.get("weak_typicality_is_holder_cohomology_invariant") is not False:
        errors.append("toy weak typicality invariance mismatch")
    global_h = model.get("global_holonomies", {})
    if global_h.get("H_s_z_p") != [["1", "0"], ["-1", "1"]]:
        errors.append("toy stable holonomy mismatch")
    if global_h.get("H_u_p_z") != [["1", "1"], ["0", "1"]]:
        errors.append("toy unstable holonomy mismatch")
    if global_h.get("psi_z=H_s_z_p*H_u_p_z") != [["1", "1"], ["-1", "0"]]:
        errors.append("toy loop mismatch")
    wedges = model.get("twisting_wedges", {})
    if wedges.get("det(e_u,psi_z*e_u)") != "-1":
        errors.append("toy unstable-axis wedge mismatch")
    if wedges.get("det(e_s,psi_z*e_s)") != "-1":
        errors.append("toy stable-axis wedge mismatch")
    if wedges.get("both_periodic_eigenaxes_twisted") is not True:
        errors.append("toy twisting mismatch")
    distinct = model.get("two_distinct_witness_assignment", {})
    if distinct.get("psi_z_minus") != [["1", "1/4"], ["-4", "0"]]:
        errors.append("toy second loop mismatch")
    if distinct.get("det(e_s,psi_z_minus*e_s)") != "-1/4":
        errors.append("toy second wedge mismatch")
    if distinct.get("witnesses_are_distinct") is not True:
        errors.append("toy witness distinctness mismatch")

    scope = result.get("butler_park_scope", {})
    if scope.get("canonical_holonomy_family_is_representative_dependent") is not True:
        errors.append("Butler--Park canonical-family scope mismatch")
    if scope.get("both_toy_representatives_belong_to_class_H") is not True:
        errors.append("Butler--Park class-H membership mismatch")
    if scope.get("toy_model_makes_no_claim_against_class_H_membership_invariance") is not True:
        errors.append("Butler--Park class-H invariance scope mismatch")
    if scope.get("continuous_conjugacy_preserves_canonical_holonomies_without_a_tail_condition") is not False:
        errors.append("canonical transport scope mismatch")
    if scope.get("toy_model_refutes_canonical_holonomy_and_weak_typicality_invariance") is not True:
        errors.append("toy canonical/typicality no-go scope mismatch")

    frontier = result.get("actual_billiard_frontier", {})
    expected_frontier = {
        "finite_shadow_and_connector_witnesses_are_universal_obstructions": False,
        "one_third_gauge_passing_the_known_finite_witnesses_exists": True,
        "selected_twisting_can_be_kept_during_those_local_repairs": True,
        "actual_variable_diagonal_stable_groupoid_resonant_equation": "NOT_SOLVED",
        "actual_variable_diagonal_unstable_groupoid_resonant_equation": "NOT_SOLVED",
        "uniform_all_plaque_holder_constants": "NOT_CERTIFIED",
        "actual_same_representative_class_H_plus_twisting": "NOT_CERTIFIED",
        "Gate1": "NOT_CERTIFIED",
    }
    for key, expected in expected_frontier.items():
        if frontier.get(key) != expected:
            errors.append(f"actual frontier mismatch: {key}")

    verdict = data.get("verdict", {})
    expected_verdict = {
        "finite_periodic_jet_blockers_universal": "REFUTED",
        "selected_loop_preserved_by_disjoint_local_repairs": "CERTIFIED",
        "canonical_holonomy_family_cohomology_invariance": "REFUTED",
        "weak_typicality_cohomology_invariance": "REFUTED",
        "class_H_membership_cohomology_invariance": "NOT_ADDRESSED",
        "actual_all_plaque_third_gauge": "NOT_CERTIFIED",
        "Gate1": "NOT_CERTIFIED",
    }
    for key, expected in expected_verdict.items():
        if verdict.get(key) != expected:
            errors.append(f"verdict mismatch: {key}")

    replay_digest = result.get("internal_replay_digest")
    without_digest = copy.deepcopy(result)
    without_digest.pop("internal_replay_digest", None)
    if replay_digest != certificate.digest(without_digest):
        errors.append("internal replay digest mismatch")
    return errors


def integrity_errors(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for group in ("files", "dependencies"):
        mapping = data.get(group, {})
        if not isinstance(mapping, dict):
            errors.append(f"{group} mapping missing")
            continue
        for name, expected in mapping.items():
            path = HERE / name
            if not path.is_file():
                errors.append(f"missing {group} file: {name}")
            elif sha256_path(path) != expected:
                errors.append(f"{group} hash mismatch: {name}")
    return errors


def replay_errors(data: dict[str, Any]) -> list[str]:
    rebuilt = certificate.build_result()
    if rebuilt != data.get("result"):
        return ["certificate replay differs from frozen result"]
    return []


def set_path(value: dict[str, Any], path: tuple[str, ...], replacement: Any) -> None:
    cursor: Any = value
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement


def self_test(data: dict[str, Any]) -> tuple[int, int, list[str]]:
    mutations: list[tuple[str, tuple[str, ...], Any]] = [
        ("manifest schema", ("schema",), "bad.schema"),
        ("repair sign", ("result", "periodic_first_jet_repair", "lower_left_coefficient_update"), "c_E=c+(1-nu)*X_21"),
        ("canceling jet", ("result", "periodic_first_jet_repair", "exact_canceling_jet"), "X_21=-c/(1-nu)"),
        ("convergence overclaim", ("result", "periodic_first_jet_repair", "removing_the_witness_proves_canonical_convergence"), True),
        ("orbit disjointness", ("result", "disjoint_SL2_bump_escape", "shadow_and_connector_orbits_disjoint_from_K"), False),
        ("cutoff first jet", ("result", "disjoint_SL2_bump_escape", "cutoff_jet_at_basepoint"), "chi(q_*)=1"),
        ("selected loop", ("result", "disjoint_SL2_bump_escape", "selected_infinite_loop_and_four_wedges_unchanged"), False),
        ("bump class H", ("result", "disjoint_SL2_bump_escape", "all_plaque_class_H_after_the_bumps"), "CERTIFIED"),
        ("toy rho", ("result", "explicit_cohomologous_class_H_twisting_model", "rho"), "1/2"),
        ("toy A", ("result", "explicit_cohomologous_class_H_twisting_model", "constant_diagonal_cocycle_A"), [["3", "0"], ["0", "1/3"]]),
        ("toy stable H", ("result", "explicit_cohomologous_class_H_twisting_model", "global_holonomies", "H_s_z_p"), [["1", "0"], ["0", "1"]]),
        ("toy unstable H", ("result", "explicit_cohomologous_class_H_twisting_model", "global_holonomies", "H_u_p_z"), [["1", "0"], ["0", "1"]]),
        ("toy loop", ("result", "explicit_cohomologous_class_H_twisting_model", "global_holonomies", "psi_z=H_s_z_p*H_u_p_z"), [["1", "0"], ["0", "1"]]),
        ("toy wedge", ("result", "explicit_cohomologous_class_H_twisting_model", "twisting_wedges", "det(e_u,psi_z*e_u)"), "0"),
        ("toy class H", ("result", "explicit_cohomologous_class_H_twisting_model", "B_belongs_to_Butler_Park_class_H"), False),
        ("toy class H overclaim", ("result", "explicit_cohomologous_class_H_twisting_model", "this_model_refutes_class_H_membership_invariance"), True),
        ("toy canonical invariance", ("result", "explicit_cohomologous_class_H_twisting_model", "canonical_holonomy_family_is_holder_cohomology_invariant"), True),
        ("canonical transport", ("result", "butler_park_scope", "continuous_conjugacy_preserves_canonical_holonomies_without_a_tail_condition"), True),
        ("stable groupoid overclaim", ("result", "actual_billiard_frontier", "actual_variable_diagonal_stable_groupoid_resonant_equation"), "SOLVED"),
        ("Gate 1 overclaim", ("verdict", "Gate1"), "CERTIFIED"),
    ]
    passed = 0
    failures: list[str] = []
    for label, path, replacement in mutations:
        mutated = copy.deepcopy(data)
        set_path(mutated, path, replacement)
        if validate(mutated):
            passed += 1
        else:
            failures.append(label)
    return passed, len(mutations), failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    data = load(args.manifest)
    errors = integrity_errors(data)
    if not args.integrity_only:
        errors.extend(validate(data))
    if args.replay:
        errors.extend(replay_errors(data))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    if args.self_test:
        passed, total, failures = self_test(data)
        print(f"MUTATION_SELF_TEST: {passed}/{total}")
        if failures:
            print("UNCAUGHT_MUTATIONS: " + ", ".join(failures))
            return 1
        return 0

    if args.integrity_only:
        print("INTEGRITY: OK")
        if args.replay:
            print("REPLAY: OK")
        return 0

    print("FINITE_PERIODIC_JET_BLOCKERS_UNIVERSAL: REFUTED")
    print("SELECTED_LOOP_PRESERVED_BY_DISJOINT_LOCAL_REPAIRS: CERTIFIED")
    print("CANONICAL_HOLONOMY_FAMILY_COHOMOLOGY_INVARIANCE: REFUTED")
    print("WEAK_TYPICALITY_COHOMOLOGY_INVARIANCE: REFUTED")
    print("CLASS_H_MEMBERSHIP_COHOMOLOGY_INVARIANCE: NOT_ADDRESSED")
    print("ACTUAL_ALL_PLAQUE_THIRD_GAUGE: NOT_CERTIFIED")
    print("GATE1: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
