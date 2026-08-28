#!/usr/bin/env python3
"""Executable join diagnostic for the missing Gate-4 weighted Growth sum.

This certificate does not manufacture a Growth contraction.  It answers the
more basic question whether the frozen horizon, candidate-row, complexity,
and one-branch ledgers already contain enough *linked* data to evaluate one.

The answer is no.  The 35,024 horizon leaves and the 448 retained chart-target
pairs occur in different schemas and have no common short-unstable-curve,
continuity-component, homogeneity-child, or inverse-expansion key.  Exact
rational completions of the currently available aggregate inequalities give
both contracting and noncontracting sums.  Thus the aggregate data are
non-identifying; a physical componentwise join is genuinely required.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


Q = Fraction
HERE = Path(__file__).resolve().parent

FINITE_S_MANIFEST = (
    HERE / "cm2-gate45-finite-s-common-mesh-recovery-manifest-2026-07-16.json"
)
FIRST_HIT_MANIFEST = (
    HERE / "cm2-gate3-first-hit-atlas-manifest-2026-07-15.json"
)
NUMERIC_GROWTH_MANIFEST = (
    HERE / "cm2-gate4-numeric-growth-leaves-frontier-manifest-2026-07-16.json"
)
GLOBAL_GROWTH_MANIFEST = (
    HERE / "cm2-gate4-global-growth-distortion-frontier-manifest-2026-07-16.json"
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def load_dependencies() -> tuple[dict[str, Any], ...]:
    finite_s = json.loads(FINITE_S_MANIFEST.read_text(encoding="utf-8"))
    first_hit = json.loads(FIRST_HIT_MANIFEST.read_text(encoding="utf-8"))
    numeric = json.loads(NUMERIC_GROWTH_MANIFEST.read_text(encoding="utf-8"))
    global_growth = json.loads(
        GLOBAL_GROWTH_MANIFEST.read_text(encoding="utf-8")
    )

    assert finite_s["schema"] == (
        "cm2.gate45.finite-s-common-mesh-recovery.manifest.v1"
    )
    assert first_hit["schema"] == "cm2.gate3.first-hit-atlas.v1"
    assert numeric["schema"] == (
        "cm2.gate4.numeric-growth-leaves-frontier.manifest.v1"
    )
    assert global_growth["schema"] == (
        "cm2.gate4.global-growth-distortion-frontier.manifest.v1"
    )

    assert finite_s["result"]["uniform_horizon_penetration_audit"][
        "replayed_leaf_count"
    ] == 35024
    assert first_hit["candidate_reduction"]["retained_pair_count"] == 448
    assert numeric["replay_summary"]["single_branch_cut_sum"] == (
        "900337/901685"
    )
    assert global_growth["replay_summary"][
        "true_continuity_component_upper"
    ] == 153
    assert global_growth["replay_summary"][
        "numeric_global_Growth_contraction"
    ] is False
    return finite_s, first_hit, numeric, global_growth


def recursive_keys(value: Any) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            keys.add(key)
            keys.update(recursive_keys(child))
    elif isinstance(value, list):
        for child in value:
            keys.update(recursive_keys(child))
    return keys


def frozen_schema_join_audit(
    finite_s: dict[str, Any],
    first_hit: dict[str, Any],
    numeric: dict[str, Any],
    global_growth: dict[str, Any],
) -> dict[str, Any]:
    horizon = finite_s["result"]["uniform_horizon_penetration_audit"]
    candidate = first_hit["candidate_reduction"]
    completion = first_hit["global_completion"]
    global_summary = global_growth["replay_summary"]

    assert horizon["replayed_leaf_count"] == 35024
    assert "horizon_leaf_rows_sha256" in horizon
    assert "horizon_leaf_rows" not in horizon
    assert candidate["retained_pair_count"] == 448
    assert all(
        "candidate_sha256" in row and "retained" in row
        for row in candidate["charts"]
    )
    assert not any("candidate_rows" in row for row in candidate["charts"])
    assert completion["all_retained_event_rows"] is None
    assert completion["all_first_hit_partitions"] is None
    assert global_summary["true_continuity_component_upper"] == 153

    required_join_fields = (
        "short_unstable_curve_cell_id",
        "uniform_small_curve_threshold_delta_1",
        "physical_continuity_component_id",
        "parent_short_curve_cell_id",
        "homogeneity_child_id",
        "physical_component_multiplicity",
        "inverse_expansion_sup_upper",
        "componentwise_weighted_sum_upper",
        "componentwise_weighted_sum_margin",
    )
    all_keys = (
        recursive_keys(finite_s)
        | recursive_keys(first_hit)
        | recursive_keys(numeric)
        | recursive_keys(global_growth)
    )
    absent = [field for field in required_join_fields if field not in all_keys]
    assert tuple(absent) == required_join_fields

    return {
        "horizon_ledger": {
            "leaf_count": 35024,
            "row_digest_present": True,
            "materialized_rows_in_manifest": False,
            "typed_role": (
                "ambient position-direction cover proving tau<3 and penetration slack"
            ),
            "continuity_component_or_weight_fields": False,
        },
        "candidate_ledger": {
            "retained_chart_target_pair_count": 448,
            "per_chart_candidate_digests_present": True,
            "materialized_physical_continuity_rows_in_manifest": False,
            "typed_role": (
                "conservative source-chart/target necessary-condition registry"
            ),
            "all_retained_event_rows": None,
            "all_first_hit_partitions": None,
            "inverse_expansion_fields": False,
        },
        "complexity_ledger": {
            "true_singularity_intersection_upper": 152,
            "true_continuity_component_upper": 153,
            "typed_role": "unweighted global count envelope",
            "component_identifiers_or_weights": False,
        },
        "required_join_fields_absent": absent,
        "common_componentwise_join_key_present": False,
        "multiplicity_times_inverse_expansion_join_present": False,
        "digest_is_not_a_typed_join_relation": True,
        "frozen_ledgers_are_pairwise_count_compatible_but_not_row_linked": True,
    }


def exact_aggregate_identifiability() -> dict[str, Any]:
    theta = Q(144000, 180337)
    high_strip_tail = Q(1, 5)
    q_one_branch = theta + high_strip_tail
    component_upper = 153
    crude_upper = component_upper * q_one_branch

    assert q_one_branch == Q(900337, 901685) < 1
    assert crude_upper == Q(137751561, 901685) > 1

    # Two completions of precisely the same aggregate schema.  They are not
    # claimed to be physical billiard ledgers.  Their purpose is to prove that
    # counts plus a uniform per-component upper do not identify the missing
    # sum.  Both use 153 positive weights and every weight is strictly below
    # theta, hence also below q_one_branch.
    contracting_weight = q_one_branch / (2 * component_upper)
    noncontracting_weight = Q(3, 4)
    contracting_sum = component_upper * contracting_weight
    noncontracting_sum = component_upper * noncontracting_weight
    assert Q(0) < contracting_weight < theta < q_one_branch
    assert Q(0) < noncontracting_weight < theta < q_one_branch
    assert contracting_sum == q_one_branch / 2 < 1
    assert noncontracting_sum == Q(459, 4) > 1

    two_central_envelope = 2 * theta
    central_budget_with_declared_tail = 1 - high_strip_tail
    margin = central_budget_with_declared_tail - theta
    assert two_central_envelope == Q(288000, 180337) > 1
    assert central_budget_with_declared_tail == Q(4, 5)
    assert margin == Q(1348, 901685) > 0

    return {
        "frozen_exact_constants": {
            "uniform_central_inverse_contraction_upper": str(theta),
            "one_true_branch_two_sided_high_strip_tail_upper": str(
                high_strip_tail
            ),
            "one_true_branch_cut_sum_strict_upper": str(q_one_branch),
            "true_continuity_component_count_upper": component_upper,
            "aggregate_crude_sum_upper": str(crude_upper),
        },
        "schema_sharp_interval_diagnostic": {
            "weight_constraint_used": "0<w_j<900337/901685",
            "component_constraint_used": "1<=N<=153",
            "sum_infimum_from_these_constraints": "0",
            "sum_non_strict_envelope_from_these_constraints": str(crude_upper),
            "envelope_is_below_one": False,
            "aggregate_constraints_identify_contraction": False,
        },
        "same_count_abstract_completions": {
            "component_count_in_both_completions": component_upper,
            "contracting_completion": {
                "common_positive_weight": str(contracting_weight),
                "sum": str(contracting_sum),
                "sum_is_below_one": True,
            },
            "noncontracting_completion": {
                "common_positive_weight": str(noncontracting_weight),
                "sum": str(noncontracting_sum),
                "sum_is_below_one": False,
            },
            "every_completion_weight_strictly_below_theta": True,
            "abstract_schema_completions_not_physical_billiard_claims": True,
            "aggregate_nonidentifiability": "CERTIFIED",
        },
        "actionable_contraction_budget": {
            "frozen_single_true_branch_tail_envelope_at_k0_41": str(
                high_strip_tail
            ),
            "current_global_tail_budget_certified": False,
            "hypothetical_single_global_tail_budget_required": str(
                high_strip_tail
            ),
            "conditional_central_weight_budget_if_global_tail_proved": str(
                central_budget_with_declared_tail
            ),
            "one_central_uniform_envelope": str(theta),
            "conditional_one_central_plus_single_global_tail": str(q_one_branch),
            "conditional_strict_margin": str(margin),
            "two_repeated_central_uniform_envelopes": str(
                two_central_envelope
            ),
            "uniform_bound_method_first_ceases_to_contract_at_central_count": 2,
            "sufficient_missing_alternative_A": (
                "for one explicit delta_1, prove at most one central child and a "
                "single global high-strip tail <=1/5"
            ),
            "sufficient_missing_alternative_B": (
                "enumerate every physical child and prove the joined central-plus-"
                "homogeneity weight sum is <1"
            ),
        },
    }


def executable_missing_join_contract() -> dict[str, Any]:
    return {
        "short_curve_cover_fields": [
            "short_unstable_curve_cell_id",
            "uniform_small_curve_threshold_delta_1",
            "configuration_parameter_interval",
            "source_collision_chart",
            "complete_physical_child_count",
        ],
        "physical_child_fields": [
            "parent_short_curve_cell_id",
            "physical_continuity_component_id",
            "target_obstacle_lift",
            "homogeneity_child_id_or_central_tag",
            "physical_component_multiplicity",
            "inverse_expansion_sup_upper",
        ],
        "completion_guards": [
            "every true singularity and homogeneity cut represented exactly once",
            "no conservative candidate row charged as a physical child",
            "all weights use the same adapted metric and finite-s map",
            "componentwise_weighted_sum_upper < 1 with an exact positive margin",
        ],
        "acceptable_compressed_replacement": (
            "a replayable sheet-separation/incidence theorem at explicit delta_1 "
            "that proves at most one central child and charges all other children "
            "to one global grazing tail"
        ),
        "existing_D2T_envelope_is_not_this_join": "<42672/c_1^3",
        "existing_oriented_carrier_distortion_is_not_this_join": "6000000000000",
    }


def certify() -> dict[str, Any]:
    finite_s, first_hit, numeric, global_growth = load_dependencies()
    join_audit = frozen_schema_join_audit(
        finite_s, first_hit, numeric, global_growth
    )
    identifiability = exact_aggregate_identifiability()
    missing_contract = executable_missing_join_contract()
    assert numeric["verdict"]["numeric_global_Growth_constants"] == (
        "NOT_CERTIFIED"
    )
    return {
        "schema": "cm2.gate4.weighted-growth-join-diagnostic.v1",
        "provenance": {
            "finite_s_horizon_manifest": FINITE_S_MANIFEST.name,
            "first_hit_candidate_manifest": FIRST_HIT_MANIFEST.name,
            "numeric_growth_manifest": NUMERIC_GROWTH_MANIFEST.name,
            "global_growth_manifest": GLOBAL_GROWTH_MANIFEST.name,
        },
        "frozen_schema_join_audit": join_audit,
        "exact_aggregate_identifiability": identifiability,
        "executable_missing_join_contract": missing_contract,
        "scope_limits": {
            "aggregate_nonidentifiability_certified": True,
            "componentwise_multiplicity_inverse_expansion_join": False,
            "numeric_delta_1": False,
            "numeric_global_Growth_contraction": False,
            "numeric_C_p_vartheta_p": False,
            "complete_numeric_C_fw_C_rev_q": False,
            "gate4_certified": False,
        },
    }


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE4_AGGREGATE_GROWTH_DATA_NONIDENTIFIABILITY: CERTIFIED")
    print("GATE4_COMPONENTWISE_WEIGHTED_JOIN: NOT_CERTIFIED")
    print("GATE4_GLOBAL_GROWTH_CONTRACTION: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
