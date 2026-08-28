#!/usr/bin/env python3
"""Fail-closed verifier for the fixed-core absorption obstruction."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import cm2_gate34_fixed_core_absorption_obstruction_cert as certificate


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate34.fixed-core-absorption-obstruction.manifest.v1"
RESULT_SCHEMA = "cm2.gate34.fixed-core-absorption-obstruction.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate34-fixed-core-absorption-obstruction-manifest-2026-07-17.json"
)
CERTIFICATE = HERE / "cm2_gate34_fixed_core_absorption_obstruction_cert.py"


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

    cores = result.get("frozen_core_coordinate_envelope", {})
    expected_cores = {
        "physical_core_count": 24,
        "axis_core_count": 8,
        "diagonal_core_count": 16,
        "axis_t_interval": ["1/100", "1/50"],
        "diagonal_absolute_t_interval": ["69/100", "7/10"],
        "every_core_absolute_t_strict_upper_or_equal": "7/10",
    }
    for key, value in expected_cores.items():
        if cores.get(key) != value:
            errors.append(f"core {key}")
    if not isinstance(cores.get("core_rows_sha256"), str):
        errors.append("core rows digest")

    qnl = result.get("exact_qnl_core_avoidance", {})
    expected_qnl = {
        "parameter": "s=0",
        "exact_period": 2,
        "physical_word": "G(0,0)->W(0,0)->G(0,0)",
        "dominant_chart_seam_at_both_collisions": True,
        "seam_ownership_independent_collision_coordinate": "abs(t)=1/sqrt(2)",
        "qnl_orbit_intersects_frozen_24_core_union": False,
        "first_24_core_entrance_time": "infinity",
        "finite_periodic_orbit_collision_SRB_mass": "0",
    }
    for key, value in expected_qnl.items():
        if qnl.get(key) != value:
            errors.append(f"qnl {key}")
    separation = qnl.get("exact_separation", {})
    if separation.get(
        "one_over_sqrt_two_strictly_greater_than_7_over_10"
    ) != "1/2>(7/10)^2=49/100":
        errors.append("qnl exact separation")
    if separation.get(
        "therefore_outside_every_axis_and_diagonal_core_t_interval"
    ) is not True:
        errors.append("qnl core exclusion")

    consequence = result.get("first_core_absorption_consequence", {})
    expected_consequence = {
        "frozen_24_core_union_is_positive_collision_SRB_mass": True,
        "frozen_24_core_union_is_global_absorbing_trap": False,
        "claim_every_regular_collision_state_has_finite_first_core_entrance": (
            "REFUTED_BY_EXACT_QNL_PERIOD_TWO_ORBIT"
        ),
        "uniform_first_core_time_over_entire_regular_section": "IMPOSSIBLE",
        "the_displayed_qnl_cemetery_subset_has_zero_SRB_mass": True,
        "total_cemetery_mass_or_tail_from_this_counterexample": "NOT_QUANTIFIED",
        "selected_128_parameter_germs_may_still_admit_branchwise_core_or_cemetery_typing": True,
        "selected_128_parameter_germ_first_core_destinations": "NOT_CERTIFIED",
        "deterministic_all-state_core_propagation_is_not_a_valid_next_lemma": True,
    }
    for key, value in expected_consequence.items():
        if consequence.get(key) != value:
            errors.append(f"consequence {key}")

    scope = result.get("strict_nonpromotion", {})
    for key in (
        "qnl_counterexample_lies_in_one_of_selected_128_parameter_germs",
        "selected_germ_core_reachability_refuted",
    ):
        if scope.get(key) is not False:
            errors.append(f"nonpromotion {key}")
    for key in (
        "quantitative_cemetery_payload",
        "native_2018_step_no_recut_dwell",
        "native_12108_step_no_recut_dwell",
        "Gate3",
        "Gate4",
    ):
        if scope.get(key) != "NOT_CERTIFIED":
            errors.append(f"scope {key}")

    expected_verdict = {
        "exact_QNL_period_two_avoids_24_core": "CERTIFIED",
        "global_all_state_first_24_core_absorption": "REFUTED",
        "selected_parameter_germ_core_or_cemetery_ledger": "NOT_CERTIFIED",
        "native_2018_12108_no_recut_dwell": "NOT_CERTIFIED",
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

    core = ("result", "frozen_core_coordinate_envelope")
    mutate(core + ("physical_core_count",), 23)
    mutate(core + ("axis_core_count",), 9)
    mutate(core + ("diagonal_absolute_t_interval",), ["0", "1"])
    qnl = ("result", "exact_qnl_core_avoidance")
    mutate(qnl + ("exact_period",), 1)
    mutate(qnl + ("physical_word",), "GG")
    mutate(qnl + ("dominant_chart_seam_at_both_collisions",), False)
    mutate(qnl + ("qnl_orbit_intersects_frozen_24_core_union",), True)
    mutate(qnl + ("first_24_core_entrance_time",), "0")
    mutate(qnl + ("finite_periodic_orbit_collision_SRB_mass",), "1")
    consequence = ("result", "first_core_absorption_consequence")
    mutate(consequence + ("frozen_24_core_union_is_global_absorbing_trap",), True)
    mutate(consequence + ("uniform_first_core_time_over_entire_regular_section",), "FINITE")
    mutate(consequence + ("total_cemetery_mass_or_tail_from_this_counterexample",), "0")
    mutate(consequence + ("selected_128_parameter_germ_first_core_destinations",), "CERTIFIED")
    scope = ("result", "strict_nonpromotion")
    mutate(scope + ("qnl_counterexample_lies_in_one_of_selected_128_parameter_germs",), True)
    mutate(scope + ("selected_germ_core_reachability_refuted",), True)
    mutate(scope + ("quantitative_cemetery_payload",), "CERTIFIED")
    mutate(scope + ("native_2018_step_no_recut_dwell",), "CERTIFIED")
    mutate(scope + ("Gate4",), "CERTIFIED")
    mutate(("verdict", "global_all_state_first_24_core_absorption"), "CERTIFIED")
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
    print("EXACT_QNL_PERIOD_TWO_AVOIDS_24_CORE: CERTIFIED")
    print("GLOBAL_ALL_STATE_FIRST_24_CORE_ABSORPTION: REFUTED")
    print("SELECTED_PARAMETER_GERM_CORE_OR_CEMETERY_LEDGER: NOT_CERTIFIED")
    print("NATIVE_2018_12108_NO_RECUT_DWELL: NOT_CERTIFIED")
    print("GATE3: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
