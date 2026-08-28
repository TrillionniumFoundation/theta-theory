#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-1 local-jet obstruction frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import cm2_gate1_local_jet_gauge_obstruction_frontier_cert as certificate


HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = HERE / "cm2-gate1-local-jet-gauge-obstruction-frontier-manifest-2026-07-16.json"
CERTIFICATE = HERE / "cm2_gate1_local_jet_gauge_obstruction_frontier_cert.py"
REPORT = HERE / "cm2-gate1-local-jet-gauge-obstruction-frontier-assault-2026-07-16.md"
SCHEMA = "cm2.gate1.local-jet-gauge-obstruction-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate1.local-jet-gauge-obstruction-frontier.v1"
EXPECTED_INTERNAL_DIGEST = "65fbefa8e61d9a55f5da99bbdb2175732dde4136da5abbc61ca3236ad9879768"


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


def check_structure(data: Any, *, frozen_digest: bool = True) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["manifest is not an object"]
    if data.get("schema") != SCHEMA:
        errors.append("manifest schema mismatch")
    if data.get("certificate_sha256") != sha256_path(CERTIFICATE):
        errors.append("certificate hash mismatch")
    if data.get("verifier_sha256") != sha256_path(Path(__file__)):
        errors.append("verifier hash mismatch")
    if data.get("report_sha256") != sha256_path(REPORT):
        errors.append("report hash mismatch")

    dependencies = data.get("dependencies")
    if not isinstance(dependencies, dict) or len(dependencies) != 2:
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
    if frozen_digest and result.get("internal_replay_digest") != EXPECTED_INTERNAL_DIGEST:
        errors.append("frozen replay digest mismatch")

    provenance = result.get("provenance", {})
    if provenance.get("frozen_dependency_sha256") != dependencies:
        errors.append("result dependency binding mismatch")
    if provenance.get("shadow_arb_precision_bits") != 5000:
        errors.append("shadow precision mismatch")
    if provenance.get("connector_arb_precision_bits") != 1000:
        errors.append("connector precision mismatch")
    if provenance.get("old_artifacts_modified") is not False:
        errors.append("old-artifact scope mismatch")

    identity = result.get("periodic_local_jet_identity", {})
    expected_identity = {
        "periodic_return": "G(z_*)=z_*",
        "same_value_and_first_jet_give_same_gauged_return_and_derivative": True,
        "same_fiber_eigenbasis_and_resonant_mixed_coefficient": True,
        "higher_gauge_jets_enter_first_derivative": False,
    }
    for key, expected in expected_identity.items():
        if identity.get(key) != expected:
            errors.append(f"local-jet identity mismatch: {key}")
    if identity.get("data_used_by_A_D_and_dA_D") != [
        "D(z_*)", "dD(z_*)", "DG(z_*)", "dDG(z_*)"
    ]:
        errors.append("local-jet data list mismatch")

    shadow = result.get("shadow_first_jet_equivalence_class_obstruction", {})
    expected_shadow = {
        "periodic_shadow_collision_count": 96,
        "periodic_shadow_full_word": "Q^10 B^4 Q^10",
        "reference_coefficient_excludes_zero": True,
        "alternative_has_same_nonzero_mixed_coefficient": True,
        "alternative_stable_canonical_limit_on_nontrivial_shadow_tail": "DIVERGENT",
        "class_H_on_clean_horseshoe_containing_shadow_and_nontrivial_stable_tail": False,
        "modifications_supported_away_from_shadow_are_obstructed": True,
        "modifications_flat_through_first_order_at_shadow_are_obstructed": True,
        "isolated_periodic_orbit_alone_is_not_claimed_obstructed": True,
    }
    for key, expected in expected_shadow.items():
        if shadow.get(key) != expected:
            errors.append(f"shadow obstruction mismatch: {key}")
    coefficient = shadow.get("reference_compact_gauge_mixed_coefficient", "")
    if "-3.894455937406274" not in coefficient or "+/- 2.91e-94" not in coefficient:
        errors.append("shadow coefficient mismatch")

    connector = result.get("connector_locally_constant_gauge_obstruction", {})
    expected_connector = {
        "reference_mixed_jet_strict_interval": "(-1/20,-1/25)",
        "constant_local_gauge_changes_return_by_constant_conjugacy": True,
        "canonical_comparison_divergence_is_preserved_by_constant_conjugacy": True,
        "alternative_connector_stable_canonical_limit": "DIVERGENT",
        "class_H_on_common_basic_set_with_connector_and_nontrivial_stable_tail": False,
        "all_gauges_supported_inside_the_frozen_QNL_chart_are_obstructed_at_connector": True,
    }
    for key, expected in expected_connector.items():
        if connector.get(key) != expected:
            errors.append(f"connector obstruction mismatch: {key}")
    mixed = connector.get("reference_physical_mixed_jet", "")
    if "-0.042403922337495" not in mixed:
        errors.append("connector mixed jet mismatch")

    escape = result.get("necessary_escape_conditions_for_a_third_gauge", {})
    expected_escape = {
        "pure_QNL_local_cutoff_repair_can_close_class_H": False,
        "partition_of_unity_repair_unchanged_near_connector_and_first_order_at_shadow": "REFUTED",
        "any_surviving_third_gauge_must_change_connector_local_jet_or_cease_to_be_local": True,
        "any_surviving_third_gauge_must_change_shadow_value_or_first_jet": True,
        "simultaneous_global_stable_and_unstable_resonant_equations_solved": False,
        "arbitrary_global_jet_changing_gauge_excluded": False,
        "one_representative_with_class_H_and_twisting_certified": False,
    }
    for key, expected in expected_escape.items():
        if escape.get(key) != expected:
            errors.append(f"third-gauge frontier mismatch: {key}")

    boundary = result.get("strict_completion_boundary", {})
    expected_boundary = {
        "local_or_first_jet_flat_repairs": "REFUTED",
        "arbitrary_global_third_gauge": "NOT_CERTIFIED",
        "single_representative_class_H_plus_twisting": "NOT_CERTIFIED",
        "full_mass_physical_PPE": "NOT_CERTIFIED",
        "Gate1": "NOT_CERTIFIED",
    }
    for key, expected in expected_boundary.items():
        if boundary.get(key) != expected:
            errors.append(f"completion boundary mismatch: {key}")

    verdict = data.get("verdict", {})
    expected_verdict = {
        "periodic_gauge_first_jet_invariance": "CERTIFIED",
        "shadow_first_jet_equivalence_class_class_H": "REFUTED",
        "connector_locally_constant_gauge_class_H": "REFUTED",
        "arbitrary_global_third_gauge": "NOT_CERTIFIED",
        "Gate1": "NOT_CERTIFIED",
    }
    for key, expected in expected_verdict.items():
        if verdict.get(key) != expected:
            errors.append(f"top-level verdict mismatch: {key}")
    return errors


def refresh_result_digest(data: dict[str, Any]) -> None:
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
            refresh_result_digest(candidate)
        mutations.append(candidate)

    mutate(("result", "provenance", "shadow_arb_precision_bits"), 1000)
    mutate(("result", "periodic_local_jet_identity", "same_value_and_first_jet_give_same_gauged_return_and_derivative"), False)
    mutate(("result", "periodic_local_jet_identity", "higher_gauge_jets_enter_first_derivative"), True)
    mutate(("result", "shadow_first_jet_equivalence_class_obstruction", "periodic_shadow_collision_count"), 95)
    mutate(("result", "shadow_first_jet_equivalence_class_obstruction", "reference_coefficient_excludes_zero"), False)
    mutate(("result", "shadow_first_jet_equivalence_class_obstruction", "alternative_stable_canonical_limit_on_nontrivial_shadow_tail"), "CONVERGENT")
    mutate(("result", "shadow_first_jet_equivalence_class_obstruction", "isolated_periodic_orbit_alone_is_not_claimed_obstructed"), False)
    mutate(("result", "connector_locally_constant_gauge_obstruction", "reference_mixed_jet_strict_interval"), "unknown")
    mutate(("result", "connector_locally_constant_gauge_obstruction", "alternative_connector_stable_canonical_limit"), "CONVERGENT")
    mutate(("result", "connector_locally_constant_gauge_obstruction", "all_gauges_supported_inside_the_frozen_QNL_chart_are_obstructed_at_connector"), False)
    mutate(("result", "necessary_escape_conditions_for_a_third_gauge", "pure_QNL_local_cutoff_repair_can_close_class_H"), True)
    mutate(("result", "necessary_escape_conditions_for_a_third_gauge", "arbitrary_global_jet_changing_gauge_excluded"), True)
    mutate(("result", "strict_completion_boundary", "arbitrary_global_third_gauge"), "REFUTED")
    mutate(("result", "strict_completion_boundary", "Gate1"), "CERTIFIED")
    mutate(("verdict", "arbitrary_global_third_gauge"), "REFUTED")
    mutate(("verdict", "Gate1"), "CERTIFIED")

    rejected = sum(bool(check_structure(candidate, frozen_digest=False)) for candidate in mutations)
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

    print("PERIODIC_GAUGE_FIRST_JET_INVARIANCE: CERTIFIED")
    print("SHADOW_FIRST_JET_EQUIVALENCE_CLASS_CLASS_H: REFUTED")
    print("CONNECTOR_LOCALLY_CONSTANT_GAUGE_CLASS_H: REFUTED")
    print("ARBITRARY_GLOBAL_THIRD_GAUGE: NOT_CERTIFIED")
    print("GATE1: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
