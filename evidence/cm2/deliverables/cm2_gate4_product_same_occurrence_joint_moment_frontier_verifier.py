#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-4 product joint-moment frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import cm2_gate4_product_same_occurrence_joint_moment_frontier_cert as cert


Q = Fraction
HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate4.product-same-occurrence-joint-moment-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate4.product-same-occurrence-joint-moment-frontier.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate4-product-same-occurrence-joint-moment-frontier-manifest-2026-07-16.json"
)
CERTIFICATE = (
    HERE / "cm2_gate4_product_same_occurrence_joint_moment_frontier_cert.py"
)


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
    if data.get("dependencies") != cert.DEPENDENCIES:
        errors.append("dependency ledger mismatch")
    else:
        for name, expected in cert.DEPENDENCIES.items():
            path = HERE / name
            if not path.is_file() or sha256_path(path) != expected:
                errors.append(f"dependency hash mismatch: {name}")

    try:
        result = cert.certify()
    except Exception as exc:
        return errors + [f"certificate replay failed: {type(exc).__name__}: {exc}"]
    if result.get("schema") != RESULT_SCHEMA:
        errors.append("result schema mismatch")
    if data.get("result_sha256") != cert.canonical_digest(result):
        errors.append("result digest mismatch")

    record = result.get("same_occurrence_product_record", {})
    if record.get("base_occurrence_count") != 64:
        errors.append("occurrence count mismatch")
    if record.get("K_independent_of_physical_point_and_B") is not True:
        errors.append("K/B independence missing")
    if record.get("same_K_j_and_restriction_in_both_orientations") is not True:
        errors.append("bidirectional record identity missing")
    if record.get("forward_reverse_are_alternative_nonadditive_views") is not True:
        errors.append("nonadditive-view guard missing")
    if record.get("query_independent_same_occurrence_product_record") != "CERTIFIED":
        errors.append("product record verdict mismatch")
    if record.get("native_physical_antichain") is not False:
        errors.append("product/native scope confusion")

    joint = result.get("numeric_joint_rank_depth_moment", {})
    if joint.get("finite_s_rank_moment_upper") != (
        "43293270343755613/25600000"
    ):
        errors.append("rank moment mismatch")
    if joint.get("two_orientation_recovery_clock") != (
        "R_fw+R_rev<=603000+2010*K"
    ):
        errors.append("product recovery clock mismatch")
    if joint.get("gamma") != "1/12060":
        errors.append("gamma mismatch")
    if joint.get("constant_exponential_bound") != "exp(50)<3^50":
        errors.append("constant exponential bound mismatch")
    if joint.get("level_exponential_bound") != "exp(K/6)<(5/4)^K":
        errors.append("level exponential bound mismatch")
    if joint.get("clocked_depth_series_ratio_strict_upper") != "5/8":
        errors.append("depth ratio mismatch")
    if joint.get("clocked_depth_moment_strict_upper") != str(2 * 3**50):
        errors.append("clocked depth moment mismatch")
    expected_joint = str(
        Q(31080151660381513756308599682583861157637, 12800000)
    )
    if joint.get("joint_B_K_moment_strict_upper_before_Z_N_inverse") != expected_joint:
        errors.append("joint B/K moment mismatch")
    if joint.get("numeric_product_kernel_joint_B_K_moment") != "CERTIFIED":
        errors.append("joint B/K verdict mismatch")

    history = result.get("registered_repeated_cut_frontier", {})
    if history.get("C_mesh") != "69986663973833932800":
        errors.append("C_mesh mismatch")
    if history.get("exact_E_2K") != "3/2":
        errors.append("E2K mismatch")
    if history.get(
        "one_registered_cut_levelwise_boundary_numerator_coefficient_per_unit_incoming_mass"
    ) != (
        "104979995960750899200"
    ):
        errors.append("levelwise boundary numerator mismatch")
    if history.get("both_orientations_use_one_max_not_an_additive_double_charge") is not True:
        errors.append("single-charge boundary guard missing")
    if history.get("fixed_finite_H_registered_restart_moment") != "CERTIFIED":
        errors.append("fixed-H restart verdict mismatch")
    if history.get("one_universal_kernel_for_query_selected_H") is not False:
        errors.append("query-selected H overclaim")
    if history.get("arbitrary_physical_indicator") is not False:
        errors.append("arbitrary-indicator overclaim")
    if history.get("unbounded_H_uniform_moment") is not False:
        errors.append("unbounded-H overclaim")

    envelope = result.get("controlled_product_cost_envelope", {})
    if envelope.get("one_maximum_charged_once_on_the_common_product_law") is not True:
        errors.append("controlled single-charge guard missing")
    if envelope.get("integral_C_prod_strict_upper_before_Z_N_inverse") != (
        "1087598065258783059015245434544676138185728521412801591795461/6710886400000"
    ):
        errors.append("controlled envelope integral mismatch")
    for key in (
        "numeric_controlled_product_forward_subcost",
        "numeric_controlled_product_reverse_subcost",
        "controlled_product_single_charge",
    ):
        if envelope.get(key) != "CERTIFIED":
            errors.append(f"controlled sublayer verdict mismatch: {key}")
    for key in ("complete_C_fw", "complete_C_rev", "final_same_occurrence_q"):
        if envelope.get(key) is not False:
            errors.append(f"complete-cost overclaim: {key}")
    if len(envelope.get("not_included", [])) != 4:
        errors.append("controlled envelope exclusion count mismatch")

    boundary = result.get("exact_remaining_boundary", {})
    if boundary.get("native_countable_initial_partition_time_zero_Z") != "infinity":
        errors.append("native time-zero Z obstruction lost")
    if boundary.get("one_arbitrary_open_indicator_can_have_Z") != "infinity":
        errors.append("one-indicator obstruction lost")
    if boundary.get("quarter_cut_counterexample") != "Z_h=4^h":
        errors.append("quarter-cut obstruction lost")
    for key in (
        "complete_same_occurrence_operator_ledger",
        "Gate3_common_branch_record_MT_DQ",
        "complete_numeric_C_fw_C_rev",
        "final_q_max_Cfw_Crev_2_m",
        "gate4_certified",
    ):
        if boundary.get(key) is not False:
            errors.append(f"remaining-boundary overclaim: {key}")

    limits = result.get("scope_limits", {})
    for key in (
        "query_independent_product_same_occurrence_record",
        "numeric_joint_B_K_recovery_moment",
        "one_registered_cut_finite_levelwise_boundary_numerator",
        "fixed_finite_H_registered_restart_moment",
        "numeric_controlled_product_geometric_Z_clock_subcosts",
    ):
        if limits.get(key) is not True:
            errors.append(f"certified scope missing: {key}")
    for key in (
        "native_full_reweighted_recovery",
        "arbitrary_or_unbounded_repeated_indicator_recovery",
        "complete_numeric_C_fw_C_rev",
        "final_same_occurrence_q",
        "gate4_certified",
    ):
        if limits.get(key) is not False:
            errors.append(f"fail-closed scope mismatch: {key}")

    digests = result.get("internal_replay_digests", {})
    if digests.get("joint_cutoff_rows") != joint.get("cutoff_rows_sha256"):
        errors.append("joint cutoff digest mismatch")
    if digests.get("fixed_history_rows") != history.get("history_rows_sha256"):
        errors.append("fixed-history digest mismatch")

    # Independent exact-arithmetic replay.
    EB = Q(43293270343755613, 25600000)
    if Q(3) >= Q(5, 4) ** 6:
        errors.append("rational exponential comparison failed")
    kernel_sum = Q(3, 4) / (1 - Q(5, 8))
    if kernel_sum != 2:
        errors.append("geometric kernel sum failed")
    if EB * kernel_sum * 3**50 != Q(expected_joint):
        errors.append("independent joint moment arithmetic failed")
    if Q(3, 2) * Q(69986663973833932800) != Q(104979995960750899200):
        errors.append("independent boundary numerator arithmetic failed")

    expected_summary = {
        "product_same_occurrence_record": True,
        "gamma": "1/12060",
        "joint_B_K_moment_upper": expected_joint,
        "one_cut_levelwise_boundary_numerator": "104979995960750899200",
        "fixed_finite_H_registered_restart": True,
        "controlled_product_subcosts": True,
        "native_time_zero_Z_finite": False,
        "arbitrary_repeated_indicator_recovery": False,
        "complete_numeric_C_fw_C_rev": False,
        "final_q": False,
        "gate4_certified": False,
    }
    if data.get("replay_summary") != expected_summary:
        errors.append("replay summary mismatch")
    if data.get("replay_summary_sha256") != cert.canonical_digest(
        data.get("replay_summary", {})
    ):
        errors.append("replay summary digest mismatch")
    expected_verdict = {
        "product_same_occurrence_record": "CERTIFIED",
        "numeric_joint_B_K_recovery_moment": "CERTIFIED",
        "one_cut_levelwise_boundary_numerator": "CERTIFIED",
        "fixed_finite_H_registered_restart_moment": "CERTIFIED",
        "controlled_product_geometric_Z_clock_subcosts": "CERTIFIED",
        "native_full_reweighted_recovery": "NOT_CERTIFIED",
        "arbitrary_or_unbounded_repeated_indicator_recovery": "NOT_CERTIFIED",
        "complete_numeric_C_fw_C_rev_final_q": "NOT_CERTIFIED",
        "gate4": "NOT_CERTIFIED",
    }
    if data.get("verdict") != expected_verdict:
        errors.append("verdict mismatch")
    return errors


def mutation_self_test(baseline: dict[str, Any]) -> list[str]:
    cases: list[tuple[str, dict[str, Any]]] = []

    def add(name: str, mutate: Any) -> None:
        candidate = copy.deepcopy(baseline)
        mutate(candidate)
        candidate["replay_summary_sha256"] = cert.canonical_digest(
            candidate.get("replay_summary", {})
        )
        cases.append((name, candidate))

    add("schema", lambda d: d.__setitem__("schema", "mutated"))
    add("certificate_hash", lambda d: d.__setitem__("certificate_sha256", "0" * 64))
    add("verifier_hash", lambda d: d.__setitem__("verifier_sha256", "0" * 64))
    add(
        "dependency_hash",
        lambda d: d["dependencies"].__setitem__(next(iter(d["dependencies"])), "0" * 64),
    )
    add("result_digest", lambda d: d.__setitem__("result_sha256", "0" * 64))
    add("record", lambda d: d["replay_summary"].__setitem__("product_same_occurrence_record", False))
    add("gamma", lambda d: d["replay_summary"].__setitem__("gamma", "1"))
    add("joint", lambda d: d["replay_summary"].__setitem__("joint_B_K_moment_upper", "1"))
    add("boundary", lambda d: d["replay_summary"].__setitem__("one_cut_levelwise_boundary_numerator", "1"))
    add("fixed_H", lambda d: d["replay_summary"].__setitem__("fixed_finite_H_registered_restart", False))
    add("controlled", lambda d: d["replay_summary"].__setitem__("controlled_product_subcosts", False))
    add("native_overclaim", lambda d: d["replay_summary"].__setitem__("native_time_zero_Z_finite", True))
    add("indicator_overclaim", lambda d: d["replay_summary"].__setitem__("arbitrary_repeated_indicator_recovery", True))
    add("Cfw_overclaim", lambda d: d["replay_summary"].__setitem__("complete_numeric_C_fw_C_rev", True))
    add("q_overclaim", lambda d: d["replay_summary"].__setitem__("final_q", True))
    add("gate4_summary", lambda d: d["replay_summary"].__setitem__("gate4_certified", True))
    add("gate4_verdict", lambda d: d["verdict"].__setitem__("gate4", "CERTIFIED"))
    add(
        "native_verdict",
        lambda d: d["verdict"].__setitem__("native_full_reweighted_recovery", "CERTIFIED"),
    )
    return [name for name, candidate in cases if not check_structure(candidate)]


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
        print("MUTATION_SELF_TEST: PASS (18/18 mutations rejected)")
        return
    if args.replay or args.integrity_only:
        print("REPLAY_AND_INTEGRITY: PASS")
        return
    print("GATE4_PRODUCT_SAME_OCCURRENCE_RECORD: CERTIFIED")
    print("GATE4_NUMERIC_JOINT_B_K_RECOVERY_MOMENT: CERTIFIED")
    print("GATE4_FIXED_FINITE_REGISTERED_RESTART_MOMENT: CERTIFIED")
    print("GATE4_COMPLETE_C_FW_C_REV_FINAL_Q: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")
    raise SystemExit(2)


if __name__ == "__main__":
    main()
