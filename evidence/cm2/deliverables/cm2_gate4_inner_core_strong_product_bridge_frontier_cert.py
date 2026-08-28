#!/usr/bin/env python3
"""Gate-4 inner-core strong/product bridge frontier.

This certificate performs one deliberately narrow type join.  The 24
positive rational inner cores have a one-interval characteristic theorem on
canonical short standard curves.  That theorem is strong enough to bound
the *unnormalised* standard-family source norm of the characteristic
multiplier.  It is not strong enough to reuse the existing product-kernel
recovery clock after a pre-recovery core clip: a retained interval may have
arbitrarily small conditional mass and hence unbounded normalised shape
cost.

The certificate therefore records both the genuine core-local strong bound
and the precise missing physical join to the 64 same-occurrence product
records.  It never promotes a rational inner core to a full return key or a
native stopping record, and it leaves complete C_fw, C_rev, q and Gate 4
fail-closed.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import cm2_gate25_maximal_word_characteristic_frontier_cert as core_cert
import cm2_gate4_numeric_invariant_family_growth_recovery_frontier_cert as growth_cert
import cm2_gate4_product_same_occurrence_joint_moment_frontier_cert as product_cert


Q = Fraction
HERE = Path(__file__).resolve().parent

DEPENDENCIES = {
    "cm2-gate25-maximal-word-characteristic-frontier-manifest-2026-07-16.json": (
        "bb09f99519813ec49172f0bbbcc9015c1e0fcb2de07df7af734b81d2996a3f40"
    ),
    "cm2-gate4-product-same-occurrence-joint-moment-frontier-manifest-2026-07-16.json": (
        "67db1ec8aead4cbb0ff966e9136508636690074acb5959a6d705893eeef00eff"
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


def load_dependencies() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    loaded: dict[str, Any] = {}
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        assert path.is_file()
        assert sha256_path(path) == expected
        if path.suffix == ".json":
            loaded[name] = json.loads(path.read_text(encoding="utf-8"))

    core_manifest = loaded[
        "cm2-gate25-maximal-word-characteristic-frontier-manifest-2026-07-16.json"
    ]
    product_manifest = loaded[
        "cm2-gate4-product-same-occurrence-joint-moment-frontier-manifest-2026-07-16.json"
    ]
    growth_manifest = loaded[
        "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json"
    ]

    assert sha256_path(HERE / "cm2_gate25_maximal_word_characteristic_frontier_cert.py") == core_manifest["certificate_sha256"]
    assert sha256_path(HERE / "cm2_gate4_product_same_occurrence_joint_moment_frontier_cert.py") == product_manifest["certificate_sha256"]
    assert sha256_path(HERE / "cm2_gate4_numeric_invariant_family_growth_recovery_frontier_cert.py") == growth_manifest["certificate_sha256"]

    assert core_manifest["verdict"]["positive_inner_core_characteristic_Z"] == "CERTIFIED"
    assert core_manifest["verdict"]["full_key_characteristic_Z"] == "NOT_CERTIFIED"
    assert product_manifest["verdict"]["product_same_occurrence_record"] == "CERTIFIED"
    assert product_manifest["verdict"]["complete_numeric_C_fw_C_rev_final_q"] == "NOT_CERTIFIED"
    assert growth_manifest["verdict"]["numeric_C_p_vartheta_p_A0_A1"] == "CERTIFIED"
    return core_manifest, product_manifest, growth_manifest


def core_local_strong_multiplier() -> dict[str, Any]:
    inner = core_cert.inner_core_characteristic_lemma()
    ratio = Q(2000, 1999)
    theta = Q(360134800, 360493663)
    restricted = ratio * theta
    margin = 1 - restricted

    assert inner["registered_inner_core_rectangle_count"] == 24
    assert inner["all_cross_chart_and_within_chart_cyclic_gaps_checked"] is True
    assert inner["global_pairwise_source_normal_angle_gap_strict_lower"] == "1/100"
    assert inner["global_pairwise_source_r_gap_strict_lower"] == "1/625"
    assert Q(inner["global_pairwise_source_r_gap_strict_lower"]) > Q(
        inner["short_curve_delta_1"]
    )
    assert inner["intersection_component_multiplicity_upper_per_short_curve"] == 1
    assert inner["artificial_boundary_endpoint_count_upper_per_nonempty_intersection"] == 2
    assert inner["invariant_density_ratio_upper"] == str(ratio)
    assert inner["log_density_regularity_preserved_by_interval_restriction"] is True
    assert inner["normalized_cost_uniform_after_conditioning_on_retained_mass"] is False
    assert restricted == Q(720269600000, 720626832337) < 1
    assert margin == Q(357232337, 720626832337)

    # If a positive measured curve has mass M, regularity Reg and length L,
    # its source cost is M(1+Reg+1/L).  The sole retained interval I obeys
    # M_I/|I| <= ratio*M/L while M_I<=M and Reg_I<=Reg.  Therefore the
    # characteristic multiplier has strong source norm at most ratio.
    return {
        "inner_core_count": 24,
        "cross_chart_and_within_chart_gap_audit": "CERTIFIED",
        "global_pairwise_source_normal_angle_gap_strict_lower": "1/100",
        "global_pairwise_source_r_gap_strict_lower": "1/625",
        "canonical_short_curve_meets_at_most_one_core": True,
        "retained_component_count_upper": 1,
        "new_endpoint_count_upper": 2,
        "source_norm": "M*(1+Reg_alpha(rho)+1/length)",
        "regularity_mark_type": (
            "the frozen scale-invariant log-density/dynamic regularity mark"
        ),
        "conditional_normalization_effect_on_regularity": (
            "normalizing rho restricted to I adds a carrierwise constant to "
            "log rho, so Reg_alpha is unchanged"
        ),
        "mass_term": "M_I<=M",
        "regular_density_term": "Reg_alpha(rho_I)<=Reg_alpha(rho)",
        "boundary_term": "M_I/|I|<=(2000/1999)*M/L",
        "positive_curve_source_cost_bound": (
            "M_I*(1+Reg_I+1/|I|)<=(2000/1999)*"
            "M*(1+Reg+1/L)"
        ),
        "signed_Jordan_completion_bound": True,
        "core_union_characteristic_strong_operator_norm_upper": str(ratio),
        "core_local_standard_family_source_multiplier": "CERTIFIED",
        "core_local_regular_density_restriction": "CERTIFIED",
        "physical_step_vartheta_p": str(theta),
        "core_restriction_then_physical_step_contraction": str(restricted),
        "core_restricted_contraction_margin": str(margin),
        "core_local_open_Growth_contraction": "CERTIFIED",
        "scope": (
            "union of the 24 rational positive inner rectangles on canonical "
            "short standard curves; not the seeded maximal components or full keys"
        ),
    }


def core_local_open_growth() -> dict[str, Any]:
    restricted = Q(720269600000, 720626832337)
    margin = 1 - restricted
    additive = Q(2 * 10**90)
    half_life_block = (margin.denominator + margin.numerator - 1) // margin.numerator
    assert half_life_block == 2018
    assert restricted**half_life_block < Q(1, 2)

    adapted_cp = 2 * additive / margin
    euclidean_cp = Q(141, 4) * adapted_cp
    assert adapted_cp == Q(
        2882507329348 * 10**90, 357232337
    )

    return {
        "substochastic_core_operator": (
            "T_* o M_core: first clip the source by the fixed 24-core "
            "characteristic, then take one physical step"
        ),
        "unnormalized_recurrence": (
            "Z_* next <=(720269600000/720626832337)*Z_* current+"
            "2e90*incoming_mass"
        ),
        "half_life_block": half_life_block,
        "half_life_check": "(720269600000/720626832337)^2018<1/2",
        "adapted_open_Growth_constant": str(adapted_cp),
        "euclidean_open_Growth_constant": str(euclidean_cp),
        "these_are_unnormalized_core_local_constants": True,
        "uniform_normalized_shape_after_arbitrarily_small_clip": False,
    }


def product_composition_frontier() -> dict[str, Any]:
    product = product_cert.certify()
    envelope = product["controlled_product_cost_envelope"]
    ratio = Q(2000, 1999)
    old_integral = Q(
        1087598065258783059015245434544676138185728521412801591795461,
        6710886400000,
    )
    old_boundary = Q(104979995960750899200)
    assert envelope["integral_C_prod_strict_upper_before_Z_N_inverse"] == str(old_integral)

    terminal_integral = ratio * old_integral
    terminal_boundary = ratio * old_boundary
    assert terminal_integral == Q(
        1087598065258783059015245434544676138185728521412801591795461,
        6707530956800,
    )
    assert terminal_boundary == Q(209959991921501798400000, 1999)

    return {
        "existing_product_envelope": envelope["declared_controlled_envelope"],
        "existing_product_occurrence_count": 64,
        "abstract_terminal_composition": (
            "post-recovery multiplication by the fixed 24-core union has "
            "strong source cost at most (2000/1999)*C_prod"
        ),
        "abstract_terminal_composed_integral_strict_upper_before_Z_N_inverse": str(
            terminal_integral
        ),
        "abstract_terminal_composed_one_cut_boundary_upper": str(terminal_boundary),
        "abstract_post_recovery_strong_composition_arithmetic": "CERTIFIED",
        "this_is_a_physical_core_to_occurrence_join": False,
        "this_reuses_the_clock_after_a_pre_recovery_core_clip": False,
    }


def exact_join_obstruction(
    core_manifest: dict[str, Any], product_manifest: dict[str, Any]
) -> dict[str, Any]:
    core_result = core_manifest["result"]
    inner = core_result["positive_inner_core_characteristic_Z"]
    rows = core_result["seeded_implicit_maximal_component_registry"]["rows"]
    assert len(rows) == 24
    assert inner["normalized_cost_uniform_after_conditioning_on_retained_mass"] is False
    assert product_manifest["replay_summary"]["product_same_occurrence_record"] is True

    # Freeze the exact ID mismatch in the current evidence: the core stack
    # supplies maximal_component_id/word-key rows, whereas the product stack
    # supplies only the 64 occurrence law and no core-to-occurrence relation.
    audit_rows = []
    for row in rows:
        audit_rows.append({
            "maximal_component_id": row["maximal_component_id"],
            "physical_key": row["definition"]["physical_key"],
            "certified_product_occurrence_id": None,
            "certified_forward_recovery_carrier_id": None,
            "certified_reverse_recovery_carrier_id": None,
        })
    audit_rows.sort(key=canonical_json)

    return {
        "certified_core_to_64_occurrence_mapping_count": 0,
        "immutable_same_restriction_forward_reverse_carrier_join": False,
        "reason_type_join_missing": (
            "the 24-core registry is indexed by return-word/maximal-component "
            "IDs; the product recovery registry is indexed by 64 singular "
            "occurrence IDs, and no frozen field identifies the two"
        ),
        "corner_clip_countersequence": (
            "a canonical curve can meet a rational core in intervals I_n with "
            "|I_n|->0; the unnormalised term M_I/|I| stays controlled but the "
            "normalised shape cost contains 1/|I_n|->infinity"
        ),
        "sup_normalized_shape_cost_after_nonempty_core_clip": "infinity",
        "existing_K_only_recovery_clock_survives_pre_recovery_core_clip": False,
        "missing_extra_record": (
            "a query-independent retained-fraction/depth shell, in both "
            "orientations on the same occurrence, with a joint mass-weighted "
            "recovery moment"
        ),
        "full_key_characteristic_Z": False,
        "Gate3_MT_DQ_physical_current_match": False,
        "complete_numeric_C_fw": False,
        "complete_numeric_C_rev": False,
        "final_same_occurrence_q": False,
        "gate4_certified": False,
        "audit_row_count": len(audit_rows),
        "audit_rows_sha256": canonical_digest(audit_rows),
    }


def certify() -> dict[str, Any]:
    core_manifest, product_manifest, _ = load_dependencies()
    strong = core_local_strong_multiplier()
    growth = core_local_open_growth()
    composition = product_composition_frontier()
    obstruction = exact_join_obstruction(core_manifest, product_manifest)
    return {
        "schema": "cm2.gate4.inner-core-strong-product-bridge-frontier.v1",
        "provenance": {
            "parameter_window": "|s|<=1/400",
            "dependency_sha256": DEPENDENCIES,
            "inner_core_count": 24,
            "product_occurrence_count": 64,
        },
        "core_local_strong_multiplier": strong,
        "core_local_open_growth": growth,
        "product_composition_frontier": composition,
        "exact_physical_join_obstruction": obstruction,
        "scope_limits": {
            "core_local_standard_family_source_multiplier": True,
            "core_local_regular_density_restriction": True,
            "core_local_open_Growth_contraction": True,
            "abstract_post_recovery_product_composition_arithmetic": True,
            "physical_core_to_product_occurrence_join": False,
            "uniform_pre_recovery_core_clip_clock": False,
            "full_key_characteristic_Z": False,
            "complete_numeric_C_fw_C_rev": False,
            "final_same_occurrence_q": False,
            "gate4_certified": False,
        },
    }


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE4_24_CORE_LOCAL_STRONG_MULTIPLIER: CERTIFIED")
    print("GATE4_24_CORE_LOCAL_OPEN_GROWTH: CERTIFIED")
    print("GATE4_PHYSICAL_CORE_TO_PRODUCT_OCCURRENCE_JOIN: NOT_CERTIFIED")
    print("GATE4_COMPLETE_C_FW_C_REV_FINAL_Q: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
