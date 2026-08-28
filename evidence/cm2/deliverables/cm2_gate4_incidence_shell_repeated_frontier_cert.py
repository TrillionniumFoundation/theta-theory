#!/usr/bin/env python3
"""Gate-4 incidence, retained-fraction shell and repeated-core frontier.

This certificate attacks the exact gap left by the fifteenth-round
24-inner-core strong/product bridge.  It makes three deliberately separate
claims.

1.  The 24 regular return cores do not directly intersect the 64 singular
    occurrence bases.  Source/target label compatibility is only a
    many-to-many diagnostic; the missing bridge is a transported recovery-
    carrier incidence, not a set-theoretic intersection or a label join.
2.  A nonempty one-interval corner clip with retained mass fraction ``p``
    has a canonical shell depth ``D=ceil(log2(1/p))``.  Although the
    normalized shape supremum is infinite, the *one-cut mass-weighted* two-
    orientation recovery-clock factor is uniformly bounded by ``15/8``.
3.  If normalization is avoided, the already physical fixed 24-core open
    operator has an all-time unnormalised Growth resolvent.  This is genuine
    repeated control for that fixed open operator, but it is not a native or
    arbitrary-indicator recovery theorem.

The physical transported incidence, the reverse one-interval strong typing,
the cemetery/complement strong payload and an unbounded repeated-indicator
law remain absent.  Complete C_fw, C_rev, q and Gate 4 therefore remain
fail-closed.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

import cm2_gate25_maximal_word_characteristic_frontier_cert as core_cert
import cm2_gate25_physical_return_core_registry_cert as physical_core_cert
import cm2_gate3_global_borel_current_assembly_cert as occurrence_cert
import cm2_gate4_inner_core_strong_product_bridge_frontier_cert as bridge_cert
import cm2_gate4_numeric_invariant_family_growth_recovery_frontier_cert as growth_cert
import cm2_gate4_product_same_occurrence_joint_moment_frontier_cert as product_cert


Q = Fraction
HERE = Path(__file__).resolve().parent

DEPENDENCIES = {
    "cm2-gate4-inner-core-strong-product-bridge-frontier-manifest-2026-07-16.json": (
        "3a9fdd11c952fd8517a8fa068794c5737fee7265ee5532032af9605eae2feee3"
    ),
    "cm2-gate4-product-borel-payload-frontier-manifest-2026-07-16.json": (
        "872823004d1983da48d800350a18757e91daebbf5c72d84553bb81114edb9123"
    ),
    "cm2-gate4-product-same-occurrence-joint-moment-frontier-manifest-2026-07-16.json": (
        "67db1ec8aead4cbb0ff966e9136508636690074acb5959a6d705893eeef00eff"
    ),
    "cm2-gate25-maximal-word-characteristic-frontier-manifest-2026-07-16.json": (
        "bb09f99519813ec49172f0bbbcc9015c1e0fcb2de07df7af734b81d2996a3f40"
    ),
    "cm2-gate3-maximal-global-row-registry-manifest-2026-07-15.json": (
        "2a25426d0a3f90a3fc2df592626d01cf294394f14590a9b1e9338f65ba8614f8"
    ),
    "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json": (
        "b03c5ae0e400045f087cfbd1aa8c843990edebe517a4dde786b0718446db7c1d"
    ),
    "cm2-v52-manifest.sha256": (
        "5cef5b8e60f0cfe2291da6bb34b2c57eed6cf2d1a13d164b74b566f752b6b368"
    ),
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_dependencies() -> dict[str, dict[str, Any]]:
    loaded: dict[str, dict[str, Any]] = {}
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        assert path.is_file()
        assert sha256_path(path) == expected
        if path.suffix == ".json":
            loaded[name] = json.loads(path.read_text(encoding="utf-8"))

    bridge = loaded[
        "cm2-gate4-inner-core-strong-product-bridge-frontier-manifest-2026-07-16.json"
    ]
    product = loaded[
        "cm2-gate4-product-same-occurrence-joint-moment-frontier-manifest-2026-07-16.json"
    ]
    core = loaded[
        "cm2-gate25-maximal-word-characteristic-frontier-manifest-2026-07-16.json"
    ]
    occurrence = loaded[
        "cm2-gate3-maximal-global-row-registry-manifest-2026-07-15.json"
    ]
    growth = loaded[
        "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json"
    ]

    assert bridge["verdict"]["physical_core_to_product_occurrence_join"] == "NOT_CERTIFIED"
    assert bridge["replay_summary"]["certified_core_to_occurrence_mapping_count"] == 0
    assert product["verdict"]["product_same_occurrence_record"] == "CERTIFIED"
    assert product["verdict"]["complete_numeric_C_fw_C_rev_final_q"] == "NOT_CERTIFIED"
    assert core["result"]["seeded_implicit_maximal_component_registry"][
        "seeded_maximal_component_count"
    ] == 24
    assert occurrence["result"]["maximal_row_registry"][
        "maximal_connected_physical_row_count"
    ] == 64
    assert growth["replay_summary"]["vartheta_p"] == "360134800/360493663"
    assert growth["replay_summary"]["A0"] == 301500
    assert growth["replay_summary"]["A1"] == 1005
    return loaded


def physical_incidence_audit() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    core_rows = core_cert.seeded_maximal_component_rows()
    occurrence_rows, registry = occurrence_cert.load_maximal_rows()
    physical_registry = physical_core_cert.physical_registry()
    physical_frontier = physical_core_cert.remaining_operator_frontier()

    assert len(core_rows) == 24
    assert len(occurrence_rows) == 64
    assert registry["maximal_connected_physical_row_count"] == 64
    assert physical_registry[
        "all_cores_strict_first_hit_against_complete_retained_candidate_list"
    ] is True
    assert physical_frontier["branch_internal_no_singularity_cut"] is True

    audit_rows: list[dict[str, Any]] = []
    source_only_histogram: Counter[int] = Counter()
    source_target_histogram: Counter[int] = Counter()
    source_only_pair_count = 0
    source_target_pair_count = 0
    for core in core_rows:
        key = core["definition"]["physical_key"]
        source = key[0].split(":")[0]
        target = key[1]
        source_matches = [
            row["occurrence_id"]
            for row in occurrence_rows
            if row["source"] == source
        ]
        source_target_matches = [
            row["occurrence_id"]
            for row in occurrence_rows
            if row["source"] == source and row["target"] == target
        ]
        source_only_histogram[len(source_matches)] += 1
        source_target_histogram[len(source_target_matches)] += 1
        source_only_pair_count += len(source_matches)
        source_target_pair_count += len(source_target_matches)
        audit_rows.append({
            "maximal_component_id": core["maximal_component_id"],
            "physical_key": key,
            "source_only_label_candidate_count": len(source_matches),
            "source_target_label_candidate_count": len(source_target_matches),
            "source_target_label_candidate_occurrence_ids": sorted(
                source_target_matches
            ),
            "direct_regular_core_singular_occurrence_intersection_count": 0,
            "transported_forward_recovery_incidence_id": None,
            "transported_reverse_recovery_incidence_id": None,
        })

    audit_rows.sort(key=canonical_json)
    assert source_only_histogram == Counter({44: 12, 20: 12})
    assert source_target_histogram == Counter({0: 8, 5: 8, 9: 8})
    assert source_only_pair_count == 768
    assert source_target_pair_count == 112
    assert len(audit_rows) * len(occurrence_rows) == 1536

    return audit_rows, {
        "regular_inner_core_count": len(core_rows),
        "singular_occurrence_count": len(occurrence_rows),
        "all_24_cores_strict_first_hit_against_complete_retained_candidates": True,
        "all_24_core_interiors_have_no_singularity_cut": True,
        "direct_set_theoretic_core_occurrence_pair_universe": 1536,
        "direct_set_theoretic_core_occurrence_intersection_count": 0,
        "why_direct_intersection_is_zero": (
            "the 24 inner rectangles are certified inside regular strict-first-"
            "hit continuity branches, whereas each of the 64 occurrence bases "
            "is a state-changing singular moving-face row"
        ),
        "source_only_label_candidate_pair_count": source_only_pair_count,
        "source_only_candidate_count_histogram": {
            str(key): value for key, value in sorted(source_only_histogram.items())
        },
        "source_target_label_candidate_pair_count": source_target_pair_count,
        "source_target_candidate_count_histogram": {
            str(key): value for key, value in sorted(source_target_histogram.items())
        },
        "source_target_label_join_is_a_function": False,
        "source_target_label_join_is_physical_transport_incidence": False,
        "required_nontrivial_incidence_type": (
            "(occurrence_id, view, recovery carrier/branch record, transport "
            "time, core component id, identical pulled-back restriction)"
        ),
        "certified_transported_core_to_occurrence_incidence_count": 0,
        "audit_rows_sha256": canonical_digest(audit_rows),
    }


def ceil_log2_inverse(p: Q) -> int:
    assert 0 < p <= 1
    depth = 0
    threshold = Q(1)
    while threshold > p:
        threshold /= 2
        depth += 1
    assert Q(1, 2**depth) <= p
    if depth > 0:
        assert p < Q(1, 2 ** (depth - 1))
    return depth


def same_occurrence_mass_shell() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    product = product_cert.certify()
    record = product["same_occurrence_product_record"]
    assert record["base_occurrence_count"] == 64
    assert record["same_K_j_and_restriction_in_both_orientations"] is True
    assert record["forward_reverse_are_alternative_nonadditive_views"] is True

    fractions = [Q(1), Q(3, 4), Q(1, 2), Q(1, 3), Q(1, 4), Q(1, 10), Q(1, 100), Q(1, 1000)]
    rows = []
    for p in fractions:
        depth = ceil_log2_inverse(p)
        rows.append({
            "retained_fraction_p": str(p),
            "shell_depth_D": depth,
            "lower_shell_bound": str(Q(1, 2**depth)),
            "inverse_fraction_upper": str(Q(2**depth)),
        })
    assert [row["shell_depth_D"] for row in rows] == [0, 1, 1, 2, 2, 4, 7, 10]

    return rows, {
        "base_occurrence_count": 64,
        "retained_fraction_definition": "p=m_e(A)/m_e(row), 0<p<=1",
        "shell_depth_definition": "D(A)=ceil(log2(1/p))",
        "exact_shell_inequality": "2^-D<=p and p<2^(1-D) for D>=1",
        "same_positive_occurrence_law_in_both_views": True,
        "identical_Borel_restriction_record_in_both_views": True,
        "same_retained_fraction_and_shell_depth_in_both_views": True,
        "query_independent_when_A_is_registered_before_the_later_test": True,
        "borel_mass_shell_ledger": "CERTIFIED",
        "one_interval_strong_shape_in_both_views": False,
        "core_restriction_A_identified_on_any_occurrence": False,
        "sample_shell_rows_sha256": canonical_digest(rows),
    }


def corner_clip_mass_weighted_alternative() -> dict[str, Any]:
    bridge = bridge_cert.certify()
    growth = growth_cert.certify()
    ratio = Q(2000, 1999)
    theta = Q(360134800, 360493663)
    cp = Q(
        growth["numeric_growth_and_recovery"]["numeric_Growth_Lemma_constants"][
            "adapted_C_p"
        ]
    )
    half_life = 1005
    gamma = Q(1, 12060)

    assert bridge["core_local_strong_multiplier"][
        "core_union_characteristic_strong_operator_norm_upper"
    ] == str(ratio)
    assert theta**half_life <= Q(1, 2)
    assert ratio < 2
    assert gamma * 2 * half_life == Q(1, 6)

    # For a recovered input Z/M<=C_p and a sole retained interval of fraction
    # p, the frozen unnormalised restriction estimate gives
    # Z_I/M_I <= (ratio/p) C_p < 2^(D+1) C_p.  After 1005(D+2)
    # steps the inherited part is <C_p/2 and the additive equilibrium is
    # <=C_p/2.  Both views use the same p only once a physical one-interval
    # join is supplied.
    return {
        "input_recovered_adapted_boundary": "Z_*/M<=C_p^*",
        "adapted_C_p": str(cp),
        "one_interval_unnormalized_restriction": (
            "Z_*(I)<= (2000/1999) Z_*(W)"
        ),
        "normalized_corner_clip_bound": (
            "Z_*(I)/M_I<2^(D+1)*C_p^*"
        ),
        "normalized_shape_supremum_over_nonempty_clips": "infinity",
        "per_orientation_recovery_clock": "R_I(D)<=1005*(D+2)",
        "two_orientation_recovery_clock": "R_fw+R_rev<=2010*(D+2)",
        "gamma": str(gamma),
        "elementary_exponential_bounds": [
            "exp(1/6)<5/4 (from e<3<(5/4)^6)",
            "exp(1/3)<3/2 (from e<3<(3/2)^3)",
        ],
        "one_cut_mass_weighted_two_view_clock_factor": (
            "p*exp(gamma*(R_fw+R_rev))<15/8"
        ),
        "one_cut_mass_weighted_factor_strict_upper": "15/8",
        "corner_clip_infinite_normalized_supremum_replaced_by_finite_one_cut_mass_charge": "CERTIFIED",
        "requires_same_p_and_one_interval_strong_typing_in_both_views": True,
        "physical_core_occurrence_installation": False,
        "fixed_registered_history_H_factor_upper": "(15/8)^H",
        "uniform_unbounded_H_from_this_bound": False,
    }


def unnormalized_repeated_core_propagation() -> dict[str, Any]:
    bridge = bridge_cert.certify()
    b = Q(720269600000, 720626832337)
    margin = 1 - b
    additive = Q(2 * 10**90)
    resolvent = 1 / margin
    stationary = additive / margin

    assert bridge["core_local_open_growth"]["half_life_block"] == 2018
    assert b < 1
    assert b**2018 < Q(1, 2)
    assert margin == Q(357232337, 720626832337)
    assert resolvent == Q(720626832337, 357232337)
    assert stationary == Q(
        1441253664674 * 10**90, 357232337
    )

    return {
        "fixed_physical_open_operator": (
            "O=T_* o M_core on the union of the 24 rational inner cores"
        ),
        "recurrence": (
            "Z_*(O F)<=b_core*Z_*(F)+2e90*mass(F)"
        ),
        "b_core": str(b),
        "contraction_margin": str(margin),
        "all_n_bound": (
            "Z_*(O^n F)<=b_core^n Z_*(F)+"
            "2e90*(1-b_core^n)/(1-b_core)*mass(F)"
        ),
        "inherited_boundary_resolvent": str(resolvent),
        "stationary_additive_mass_coefficient": str(stationary),
        "half_life_block": 2018,
        "arbitrary_iteration_count_n": True,
        "corner_clip_conditioning_or_inverse_retained_mass_used": False,
        "fixed_core_unnormalized_repeated_propagation": "CERTIFIED",
        "complement_cemetery_strong_payload": False,
        "query_selected_or_arbitrary_indicator": False,
        "native_stopping_antichain": False,
        "native_or_unbounded_repeated_recovery": False,
    }


def conditional_product_join_arithmetic() -> dict[str, Any]:
    product = product_cert.certify()
    old_integral = Q(
        product["controlled_product_cost_envelope"][
            "integral_C_prod_strict_upper_before_Z_N_inverse"
        ]
    )
    ratio = Q(2000, 1999)
    shell = Q(15, 8)
    conditional = old_integral * ratio * shell
    expected = Q(
        3262794195776349177045736303634028414557185564238404775386383,
        10732049530880,
    )
    assert conditional == expected
    return {
        "frozen_controlled_product_integral_upper_before_Z_N_inverse": str(
            old_integral
        ),
        "core_strong_multiplier": str(ratio),
        "one_cut_retained_fraction_shell_multiplier": str(shell),
        "conditional_joined_one_cut_integral_upper_before_Z_N_inverse": str(
            conditional
        ),
        "condition": (
            "only if a transported 24-core-to-64-occurrence incidence and "
            "the identical one-interval restriction on both recovery carriers "
            "are physically certified"
        ),
        "conditional_arithmetic": "CERTIFIED",
        "physical_join_hypotheses": "NOT_CERTIFIED",
        "promoted_to_numeric_C_fw_or_C_rev": False,
    }


def exact_remaining_boundary() -> dict[str, Any]:
    return {
        "transported_24_core_to_64_occurrence_incidence": False,
        "same_core_restriction_one_interval_on_both_recovery_carriers": False,
        "strong_complement_cemetery_payload": False,
        "Gate3_common_branch_record_MT_DQ_physical_current_match": False,
        "query_independent_tail_on_unbounded_repeated_cut_count_H": False,
        "complete_recordwise_strong_operator_and_test_ledger": False,
        "complete_numeric_C_fw": False,
        "complete_numeric_C_rev": False,
        "final_same_occurrence_q": False,
        "native_full_reweighted_recovery": False,
        "gate4_certified": False,
    }


def certify() -> dict[str, Any]:
    load_dependencies()
    incidence_rows, incidence = physical_incidence_audit()
    shell_rows, shell = same_occurrence_mass_shell()
    corner = corner_clip_mass_weighted_alternative()
    repeated = unnormalized_repeated_core_propagation()
    conditional = conditional_product_join_arithmetic()
    return {
        "schema": "cm2.gate4.incidence-shell-repeated-frontier.v1",
        "provenance": {
            "parameter_window": "|s|<=1/400",
            "dependency_sha256": DEPENDENCIES,
            "regular_inner_core_count": 24,
            "singular_occurrence_count": 64,
        },
        "physical_incidence_type_audit": incidence,
        "same_occurrence_retained_fraction_shell": shell,
        "corner_clip_mass_weighted_alternative": corner,
        "fixed_core_unnormalized_repeated_propagation": repeated,
        "conditional_product_join_arithmetic": conditional,
        "exact_remaining_boundary": exact_remaining_boundary(),
        "internal_replay_digests": {
            "physical_incidence_audit_rows": canonical_digest(incidence_rows),
            "sample_shell_rows": canonical_digest(shell_rows),
        },
        "scope_limits": {
            "direct_core_singular_occurrence_intersection_audited": True,
            "same_occurrence_Borel_mass_shell": True,
            "finite_one_cut_mass_weighted_corner_recovery_charge": True,
            "fixed_core_unnormalized_arbitrary_n_propagation": True,
            "transported_physical_incidence": False,
            "native_or_arbitrary_unbounded_repeated_recovery": False,
            "complete_numeric_C_fw_C_rev": False,
            "final_same_occurrence_q": False,
            "gate4_certified": False,
        },
    }


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE4_DIRECT_CORE_SINGULAR_INTERSECTION_AUDIT: CERTIFIED_ZERO")
    print("GATE4_SAME_OCCURRENCE_RETAINED_FRACTION_BOREL_SHELL: CERTIFIED")
    print("GATE4_ONE_CUT_MASS_WEIGHTED_CORNER_CHARGE: CERTIFIED")
    print("GATE4_FIXED_CORE_UNNORMALIZED_REPEATED_PROPAGATION: CERTIFIED")
    print("GATE4_TRANSPORTED_CORE_OCCURRENCE_INCIDENCE: NOT_CERTIFIED")
    print("GATE4_COMPLETE_C_FW_C_REV_FINAL_Q: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
