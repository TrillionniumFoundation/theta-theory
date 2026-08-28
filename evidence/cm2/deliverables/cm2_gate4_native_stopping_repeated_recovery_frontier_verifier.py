#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-4 native/repeated-recovery frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import cm2_gate4_native_stopping_repeated_recovery_frontier_cert as cert


SCHEMA = "cm2.gate4.native-stopping-repeated-recovery-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate4.native-stopping-repeated-recovery-frontier.v1"
HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate4-native-stopping-repeated-recovery-frontier-manifest-2026-07-16.json"
)
CERTIFICATE = HERE / "cm2_gate4_native_stopping_repeated_recovery_frontier_cert.py"


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay_result() -> dict[str, Any]:
    return cert.certify()


def check_structure(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["manifest is not an object"]
    if data.get("schema") != SCHEMA:
        errors.append("schema mismatch")
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

    try:
        result = replay_result()
    except Exception as exc:  # fail closed on any replay problem
        return errors + [f"certificate replay failed: {type(exc).__name__}: {exc}"]
    if result.get("schema") != RESULT_SCHEMA:
        errors.append("result schema mismatch")
    if data.get("result_sha256") != cert.canonical_digest(result):
        errors.append("result digest mismatch")

    summary = data.get("replay_summary")
    if not isinstance(summary, dict):
        errors.append("replay summary missing")
        summary = {}
    antichain = result.get("native_physical_mass_coordinate_prefix_antichain", {})
    obstruction = result.get("native_recovery_charge_obstruction", {})
    repeated = result.get("repeated_indicator_countermodels", {})
    constants = result.get("numeric_growth_constant_dependency_audit", {})
    limits = result.get("scope_limits", {})

    expected_summary = {
        "native_prefix_antichain": antichain.get(
            "physical_mass_coordinate_native_antichain"
        ),
        "native_level_law": antichain.get("native_level_law"),
        "native_leaf_depth": antichain.get("leaf_depth"),
        "native_partial_charge": obstruction.get(
            "native_partial_charge_through_N"
        ),
        "native_recovery_target": obstruction.get(
            "native_depth_plus_recovery_target"
        ),
        "single_indicator_Z": repeated.get(
            "single_open_indicator_normalized_Z"
        ),
        "repeated_cut_Z": repeated.get("repeated_cut_normalized_Z"),
        "slow_theta_A1_lower": constants.get(
            "slow_example_forces_A1_at_least"
        ),
        "numeric_propagated_costs": limits.get(
            "complete_propagated_numeric_C_fw_C_rev_q"
        ),
        "gate4_certified": limits.get("gate4_certified"),
    }
    for key, expected in expected_summary.items():
        if summary.get(key) != expected:
            errors.append(f"replay summary mismatch: {key}")

    for key in (
        "prefix_free",
        "binary_filtration_stopping_time",
        "full_mass_except_u_equals_zero",
        "zero_cemetery_mass",
        "query_independent",
        "record_fixed_before_orientation_time_mode_and_final_test",
        "same_occurrence_and_same_restricted_measure_in_both_orientations",
        "no_auxiliary_randomness",
    ):
        if antichain.get(key) is not True:
            errors.append(f"native antichain contract missing: {key}")
    if antichain.get("orbit_return_word_stopping_antichain") is not False:
        errors.append("static mass-coordinate antichain overtyped as orbit stopping")
    if antichain.get("checked_level_range") != [0, 64]:
        errors.append("native checked range mismatch")

    expected_obstruction = {
        "native_level_charge": (
            "w_K*2^(D_K)=3*2^K, equivalently one unit per nonempty leaf"
        ),
        "native_partial_charge_through_N": "3*(2^(N+1)-1)",
        "native_full_parent_normalization_moment": "infinity",
        "shell_only_normalization_moment": "infinity",
        "level_K_counting_form": (
            "if level K has 2^K positive-mass native leaves, that level contributes "
            "2^K to the expected inverse-leaf-mass charge, independently of w_K"
        ),
        "why_product_kernel_escapes_counting_no_go": (
            "K is an external mark of mass w_K; conditional on K the physical row is "
            "cut only into 2^K atoms and pays 2^K, so the charge is sum_K w_K*2^K=3/2, "
            "not the inverse joint-atom cost (w_K*2^-K)^-1"
        ),
        "native_depth_plus_recovery_target": "DIVERGES_BEFORE_RECOVERY",
    }
    for key, expected in expected_obstruction.items():
        if obstruction.get(key) != expected:
            errors.append(f"native obstruction mismatch: {key}")
    if obstruction.get(
        "countably_infinite_native_partition_has_finite_inverse_mass_moment"
    ) is not False:
        errors.append("inverse-mass partition obstruction lost")
    if obstruction.get(
        "native_antichain_replaces_auxiliary_product_recovery_moment"
    ) is not False:
        errors.append("native recovery moment overclaimed")
    if "sum_a 1=infinity" not in obstruction.get(
        "full_mass_native_countable_partition_no_go", ""
    ):
        errors.append("general native counting no-go missing")
    if "unnormalized/reweighted" not in obstruction.get(
        "possible_unnormalized_escape_not_certified", ""
    ):
        errors.append("unnormalized escape boundary missing")
    if len(obstruction.get("other_possible_escapes_not_certified", [])) != 3:
        errors.append("native escape ledger mismatch")

    if repeated.get("repeated_cut_normalized_Z") != "Z_h=4^h":
        errors.append("quarter-cut Z mismatch")
    if repeated.get("single_open_indicator_mass") != "1/12":
        errors.append("open-indicator mass mismatch")
    if repeated.get("single_open_indicator_normalized_Z") != "infinity":
        errors.append("open-indicator infinite-Z mismatch")
    if repeated.get(
        "arbitrary_characteristic_restriction_preserves_finite_Z"
    ) is not False:
        errors.append("arbitrary restriction incorrectly certified")

    if constants.get("slow_example_forces_A1_at_least") != 524288:
        errors.append("slow-theta A1 lower bound mismatch")
    if constants.get("qualitative_existence_determines_numeric_A1") is not False:
        errors.append("qualitative theorem used as numerical input")
    if constants.get("complete_propagated_numeric_C_fw_C_rev_q") is not False:
        errors.append("propagated numerical costs overclaimed")
    if len(constants.get("SYZ_nonnumeric_leaf_constants", [])) != 8:
        errors.append("SYZ dependency ledger mismatch")
    if len(constants.get("Canestrari_6_13_6_14_nonnumeric_leaf_constants", [])) != 4:
        errors.append("Canestrari dependency ledger mismatch")

    digests = result.get("internal_replay_digests", {})
    source_digests = {
        "native_rows": antichain.get("rows_sha256"),
        "native_cutoff_rows": obstruction.get("cutoff_rows_sha256"),
        "quarter_cut_rows": repeated.get("quarter_rows_sha256"),
        "open_indicator_rows": repeated.get("open_set_rows_sha256"),
    }
    for key, expected in source_digests.items():
        if digests.get(key) != expected:
            errors.append(f"internal digest mismatch: {key}")

    for key in (
        "native_physical_mass_coordinate_prefix_antichain",
        "query_independent_same_occurrence_bidirectional_record",
        "finite_registered_separated_cut_restart_schema",
    ):
        if limits.get(key) is not True:
            errors.append(f"certified scope missing: {key}")
    for key in (
        "native_antichain_finite_normalization_recovery_moment",
        "native_orbit_return_word_stopping_antichain",
        "hereditary_repeated_indicator_recovery",
        "theorem_recovery_constants_numeric",
        "complete_propagated_numeric_C_fw_C_rev_q",
        "gate4_certified",
    ):
        if limits.get(key) is not False:
            errors.append(f"fail-closed scope mismatch: {key}")

    verdict = data.get("verdict", {})
    expected_verdict = {
        "native_physical_mass_coordinate_prefix_antichain": "CERTIFIED",
        "native_depth_plus_recovery_moment": "NOT_CERTIFIED",
        "hereditary_repeated_indicator_recovery": "NOT_CERTIFIED",
        "complete_propagated_numeric_C_fw_C_rev_q": "NOT_CERTIFIED",
        "gate4": "NOT_CERTIFIED",
    }
    if verdict != expected_verdict:
        errors.append("verdict mismatch")

    # Independent exact arithmetic guards for the two finite countermodels.
    for level in range(17):
        components = 1 << level
        length = Fraction(1, 4**level)
        mass = components * length
        if mass != Fraction(1, 1 << level):
            errors.append("quarter-cut mass arithmetic failed")
            break
        if components * (length / mass) / length != 4**level:
            errors.append("quarter-cut Z arithmetic failed")
            break
    if sum((Fraction(1, 1 << (2 * n + 2)) for n in range(1, 257))) >= Fraction(1, 12):
        errors.append("open-indicator partial mass must stay below 1/12")
    return errors


def mutation_self_test(baseline: dict[str, Any]) -> list[str]:
    cases: list[tuple[str, Any]] = []

    def add(name: str, mutate: Any) -> None:
        candidate = copy.deepcopy(baseline)
        mutate(candidate)
        cases.append((name, candidate))

    add("schema", lambda d: d.__setitem__("schema", "mutated"))
    add("certificate_hash", lambda d: d.__setitem__("certificate_sha256", "0" * 64))
    add(
        "dependency_hash",
        lambda d: d["dependencies"].__setitem__(next(iter(d["dependencies"])), "0" * 64),
    )
    add("result_digest", lambda d: d.__setitem__("result_sha256", "0" * 64))
    add(
        "native_antichain",
        lambda d: d["replay_summary"].__setitem__("native_prefix_antichain", "NO"),
    )
    add(
        "native_charge",
        lambda d: d["replay_summary"].__setitem__("native_partial_charge", "finite"),
    )
    add(
        "indicator_Z",
        lambda d: d["replay_summary"].__setitem__("single_indicator_Z", "1"),
    )
    add(
        "numeric_costs",
        lambda d: d["replay_summary"].__setitem__("numeric_propagated_costs", True),
    )
    add("verdict", lambda d: d["verdict"].__setitem__("gate4", "CERTIFIED"))

    failures = []
    for name, candidate in cases:
        if not check_structure(candidate):
            failures.append(name)
    return failures


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"MANIFEST_READ: FAIL ({type(exc).__name__}: {exc})")
        raise SystemExit(1)
    errors = check_structure(data)
    if errors:
        for error in errors:
            print(f"VERIFY: FAIL: {error}")
        raise SystemExit(1)
    if args.self_test:
        failures = mutation_self_test(data)
        if failures:
            print("MUTATION_SELF_TEST: FAIL: " + ", ".join(failures))
            raise SystemExit(1)
        print("MUTATION_SELF_TEST: PASS (9/9 mutations rejected)")
        return
    if args.replay or args.integrity_only:
        print("REPLAY_AND_INTEGRITY: PASS")
        return
    print("GATE4_NATIVE_PHYSICAL_MASS_COORDINATE_PREFIX_ANTICHAIN: CERTIFIED")
    print("GATE4_NATIVE_DEPTH_PLUS_RECOVERY_MOMENT: NOT_CERTIFIED")
    print("GATE4_HEREDITARY_REPEATED_INDICATOR_RECOVERY: NOT_CERTIFIED")
    print("GATE4_PROPAGATED_NUMERIC_C_FW_C_REV_Q: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")
    raise SystemExit(2)


if __name__ == "__main__":
    main()
