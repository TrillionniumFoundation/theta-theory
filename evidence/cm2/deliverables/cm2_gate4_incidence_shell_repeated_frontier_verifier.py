#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-4 incidence/shell/repeated frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable

import cm2_gate4_incidence_shell_repeated_frontier_cert as cert


Q = Fraction
HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "cm2-gate4-incidence-shell-repeated-frontier-manifest-2026-07-16.json"
CERTIFICATE = HERE / "cm2_gate4_incidence_shell_repeated_frontier_cert.py"
SCHEMA = "cm2.gate4.incidence-shell-repeated-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate4.incidence-shell-repeated-frontier.v1"


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def expected_summary(result: dict[str, Any]) -> dict[str, Any]:
    incidence = result["physical_incidence_type_audit"]
    shell = result["same_occurrence_retained_fraction_shell"]
    corner = result["corner_clip_mass_weighted_alternative"]
    repeated = result["fixed_core_unnormalized_repeated_propagation"]
    conditional = result["conditional_product_join_arithmetic"]
    return {
        "direct_core_occurrence_pair_universe": incidence[
            "direct_set_theoretic_core_occurrence_pair_universe"
        ],
        "direct_core_occurrence_intersection_count": incidence[
            "direct_set_theoretic_core_occurrence_intersection_count"
        ],
        "source_target_label_candidate_pair_count": incidence[
            "source_target_label_candidate_pair_count"
        ],
        "transported_physical_incidence_count": incidence[
            "certified_transported_core_to_occurrence_incidence_count"
        ],
        "same_occurrence_Borel_mass_shell": shell["borel_mass_shell_ledger"]
        == "CERTIFIED",
        "one_cut_mass_clock_factor_upper": corner[
            "one_cut_mass_weighted_factor_strict_upper"
        ],
        "fixed_core_unnormalized_arbitrary_n": repeated[
            "fixed_core_unnormalized_repeated_propagation"
        ]
        == "CERTIFIED",
        "conditional_joined_one_cut_integral_upper": conditional[
            "conditional_joined_one_cut_integral_upper_before_Z_N_inverse"
        ],
        "native_or_arbitrary_unbounded_repeated_recovery": False,
        "complete_numeric_C_fw_C_rev": False,
        "final_q": False,
        "gate4_certified": False,
    }


def verify_result(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if result.get("schema") != RESULT_SCHEMA:
        errors.append("result schema mismatch")

    incidence = result.get("physical_incidence_type_audit", {})
    exact_incidence = {
        "regular_inner_core_count": 24,
        "singular_occurrence_count": 64,
        "direct_set_theoretic_core_occurrence_pair_universe": 1536,
        "direct_set_theoretic_core_occurrence_intersection_count": 0,
        "source_only_label_candidate_pair_count": 768,
        "source_target_label_candidate_pair_count": 112,
        "source_only_candidate_count_histogram": {"20": 12, "44": 12},
        "source_target_candidate_count_histogram": {"0": 8, "5": 8, "9": 8},
        "source_target_label_join_is_a_function": False,
        "source_target_label_join_is_physical_transport_incidence": False,
        "certified_transported_core_to_occurrence_incidence_count": 0,
    }
    for key, value in exact_incidence.items():
        if incidence.get(key) != value:
            errors.append(f"incidence mismatch: {key}")

    shell = result.get("same_occurrence_retained_fraction_shell", {})
    exact_shell = {
        "base_occurrence_count": 64,
        "shell_depth_definition": "D(A)=ceil(log2(1/p))",
        "same_positive_occurrence_law_in_both_views": True,
        "identical_Borel_restriction_record_in_both_views": True,
        "same_retained_fraction_and_shell_depth_in_both_views": True,
        "borel_mass_shell_ledger": "CERTIFIED",
        "one_interval_strong_shape_in_both_views": False,
        "core_restriction_A_identified_on_any_occurrence": False,
    }
    for key, value in exact_shell.items():
        if shell.get(key) != value:
            errors.append(f"shell mismatch: {key}")

    corner = result.get("corner_clip_mass_weighted_alternative", {})
    if corner.get("normalized_shape_supremum_over_nonempty_clips") != "infinity":
        errors.append("normalized corner obstruction lost")
    if corner.get("per_orientation_recovery_clock") != "R_I(D)<=1005*(D+2)":
        errors.append("per-orientation shell clock mismatch")
    if corner.get("two_orientation_recovery_clock") != "R_fw+R_rev<=2010*(D+2)":
        errors.append("two-orientation shell clock mismatch")
    if corner.get("gamma") != "1/12060":
        errors.append("shell gamma mismatch")
    if corner.get("one_cut_mass_weighted_factor_strict_upper") != "15/8":
        errors.append("one-cut shell factor mismatch")
    if corner.get(
        "corner_clip_infinite_normalized_supremum_replaced_by_finite_one_cut_mass_charge"
    ) != "CERTIFIED":
        errors.append("one-cut corner charge verdict mismatch")
    if corner.get("physical_core_occurrence_installation") is not False:
        errors.append("physical shell installation overclaim")
    if corner.get("uniform_unbounded_H_from_this_bound") is not False:
        errors.append("unbounded-H shell overclaim")

    repeated = result.get("fixed_core_unnormalized_repeated_propagation", {})
    b = Q(repeated.get("b_core", "0"))
    margin = Q(repeated.get("contraction_margin", "0"))
    if b != Q(720269600000, 720626832337) or 1 - b != margin:
        errors.append("fixed-core contraction arithmetic mismatch")
    if Q(repeated.get("inherited_boundary_resolvent", "0")) != 1 / margin:
        errors.append("fixed-core resolvent mismatch")
    if repeated.get("half_life_block") != 2018 or b**2018 >= Q(1, 2):
        errors.append("fixed-core half-life mismatch")
    if repeated.get("arbitrary_iteration_count_n") is not True:
        errors.append("arbitrary-n fixed-core propagation missing")
    if repeated.get("fixed_core_unnormalized_repeated_propagation") != "CERTIFIED":
        errors.append("fixed-core repeated verdict mismatch")
    for key in (
        "complement_cemetery_strong_payload",
        "query_selected_or_arbitrary_indicator",
        "native_stopping_antichain",
        "native_or_unbounded_repeated_recovery",
    ):
        if repeated.get(key) is not False:
            errors.append(f"fixed-core scope overclaim: {key}")

    conditional = result.get("conditional_product_join_arithmetic", {})
    expected_integral = Q(
        3262794195776349177045736303634028414557185564238404775386383,
        10732049530880,
    )
    if Q(
        conditional.get(
            "conditional_joined_one_cut_integral_upper_before_Z_N_inverse", "0"
        )
    ) != expected_integral:
        errors.append("conditional joined integral mismatch")
    if conditional.get("physical_join_hypotheses") != "NOT_CERTIFIED":
        errors.append("conditional physical hypotheses overclaim")
    if conditional.get("promoted_to_numeric_C_fw_or_C_rev") is not False:
        errors.append("conditional arithmetic promoted to complete cost")

    boundary = result.get("exact_remaining_boundary", {})
    for key in (
        "transported_24_core_to_64_occurrence_incidence",
        "same_core_restriction_one_interval_on_both_recovery_carriers",
        "strong_complement_cemetery_payload",
        "Gate3_common_branch_record_MT_DQ_physical_current_match",
        "query_independent_tail_on_unbounded_repeated_cut_count_H",
        "complete_recordwise_strong_operator_and_test_ledger",
        "complete_numeric_C_fw",
        "complete_numeric_C_rev",
        "final_same_occurrence_q",
        "native_full_reweighted_recovery",
        "gate4_certified",
    ):
        if boundary.get(key) is not False:
            errors.append(f"remaining boundary overclaim: {key}")

    digests = result.get("internal_replay_digests", {})
    if digests.get("physical_incidence_audit_rows") != incidence.get(
        "audit_rows_sha256"
    ):
        errors.append("physical incidence digest mismatch")
    if digests.get("sample_shell_rows") != shell.get("sample_shell_rows_sha256"):
        errors.append("sample shell digest mismatch")

    limits = result.get("scope_limits", {})
    for key in (
        "direct_core_singular_occurrence_intersection_audited",
        "same_occurrence_Borel_mass_shell",
        "finite_one_cut_mass_weighted_corner_recovery_charge",
        "fixed_core_unnormalized_arbitrary_n_propagation",
    ):
        if limits.get(key) is not True:
            errors.append(f"certified scope missing: {key}")
    for key in (
        "transported_physical_incidence",
        "native_or_arbitrary_unbounded_repeated_recovery",
        "complete_numeric_C_fw_C_rev",
        "final_same_occurrence_q",
        "gate4_certified",
    ):
        if limits.get(key) is not False:
            errors.append(f"fail-closed scope mismatch: {key}")

    # Independent exact arithmetic for the two new numerical statements.
    theta = Q(360134800, 360493663)
    if theta**1005 > Q(1, 2):
        errors.append("independent recovery half-life check failed")
    old = Q(
        1087598065258783059015245434544676138185728521412801591795461,
        6710886400000,
    )
    if old * Q(2000, 1999) * Q(15, 8) != expected_integral:
        errors.append("independent conditional envelope arithmetic failed")
    return errors


def verify_manifest(data: Any, result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["manifest is not an object"]
    if data.get("schema") != SCHEMA:
        errors.append("manifest schema mismatch")
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
    if data.get("result_sha256") != cert.canonical_digest(result):
        errors.append("result digest mismatch")
    errors.extend(verify_result(result))

    summary = expected_summary(result)
    if data.get("replay_summary") != summary:
        errors.append("replay summary mismatch")
    if data.get("replay_summary_sha256") != cert.canonical_digest(
        data.get("replay_summary", {})
    ):
        errors.append("replay summary digest mismatch")
    expected_verdict = {
        "direct_regular_core_singular_occurrence_intersection_audit": "CERTIFIED_ZERO",
        "same_occurrence_Borel_retained_fraction_shell": "CERTIFIED",
        "one_cut_mass_weighted_corner_recovery_charge": "CERTIFIED",
        "fixed_core_unnormalized_arbitrary_n_propagation": "CERTIFIED",
        "transported_core_to_occurrence_physical_incidence": "NOT_CERTIFIED",
        "native_or_arbitrary_unbounded_repeated_recovery": "NOT_CERTIFIED",
        "complete_numeric_C_fw_C_rev_final_q": "NOT_CERTIFIED",
        "gate4": "NOT_CERTIFIED",
    }
    if data.get("verdict") != expected_verdict:
        errors.append("verdict mismatch")
    return errors


def mutation_self_test(
    baseline: dict[str, Any], result: dict[str, Any]
) -> list[str]:
    cases: list[tuple[str, dict[str, Any]]] = []

    def add(name: str, mutate: Callable[[dict[str, Any]], None]) -> None:
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
    add("pair_universe", lambda d: d["replay_summary"].__setitem__("direct_core_occurrence_pair_universe", 1))
    add("direct_intersection", lambda d: d["replay_summary"].__setitem__("direct_core_occurrence_intersection_count", 1))
    add("label_pairs", lambda d: d["replay_summary"].__setitem__("source_target_label_candidate_pair_count", 111))
    add("transported_incidence", lambda d: d["replay_summary"].__setitem__("transported_physical_incidence_count", 1))
    add("mass_shell", lambda d: d["replay_summary"].__setitem__("same_occurrence_Borel_mass_shell", False))
    add("corner_factor", lambda d: d["replay_summary"].__setitem__("one_cut_mass_clock_factor_upper", "1"))
    add("fixed_core", lambda d: d["replay_summary"].__setitem__("fixed_core_unnormalized_arbitrary_n", False))
    add("conditional_integral", lambda d: d["replay_summary"].__setitem__("conditional_joined_one_cut_integral_upper", "1"))
    add("native_overclaim", lambda d: d["replay_summary"].__setitem__("native_or_arbitrary_unbounded_repeated_recovery", True))
    add("cost_overclaim", lambda d: d["replay_summary"].__setitem__("complete_numeric_C_fw_C_rev", True))
    add("q_overclaim", lambda d: d["replay_summary"].__setitem__("final_q", True))
    add("gate4_summary", lambda d: d["replay_summary"].__setitem__("gate4_certified", True))
    add("transported_verdict", lambda d: d["verdict"].__setitem__("transported_core_to_occurrence_physical_incidence", "CERTIFIED"))
    add("native_verdict", lambda d: d["verdict"].__setitem__("native_or_arbitrary_unbounded_repeated_recovery", "CERTIFIED"))
    add("cost_verdict", lambda d: d["verdict"].__setitem__("complete_numeric_C_fw_C_rev_final_q", "CERTIFIED"))
    add("gate4_verdict", lambda d: d["verdict"].__setitem__("gate4", "CERTIFIED"))

    return [
        name for name, candidate in cases
        if not verify_manifest(candidate, result)
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
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
    try:
        result = cert.certify()
    except Exception as exc:
        print(f"CERTIFICATE_REPLAY: FAIL ({type(exc).__name__}: {exc})")
        raise SystemExit(1)
    errors = verify_manifest(data, result)
    if errors:
        for error in errors:
            print(f"VERIFY: FAIL: {error}")
        raise SystemExit(1)
    if args.self_test:
        failures = mutation_self_test(data, result)
        if failures:
            print("MUTATION_SELF_TEST: FAIL: " + ", ".join(failures))
            raise SystemExit(1)
        print("MUTATION_SELF_TEST: PASS (21/21 mutations rejected)")
        return
    if args.replay or args.integrity_only:
        print("REPLAY_AND_INTEGRITY: PASS")
        return
    print("GATE4_SAME_OCCURRENCE_RETAINED_FRACTION_SHELL: CERTIFIED")
    print("GATE4_FIXED_CORE_UNNORMALIZED_REPEATED_PROPAGATION: CERTIFIED")
    print("GATE4_TRANSPORTED_CORE_OCCURRENCE_INCIDENCE: NOT_CERTIFIED")
    print("GATE4_COMPLETE_C_FW_C_REV_FINAL_Q: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")
    raise SystemExit(2)


if __name__ == "__main__":
    main()
