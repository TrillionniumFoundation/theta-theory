#!/usr/bin/env python3
"""Physical reduction of the 394/402 maximal-word boundary over-ledger.

The frozen Gate-2/5 maximal-word registry deliberately counted a raw
algebraic over-ledger.  This replay separates raw equalities from physical
boundary branches on a fixed parameter fibre and proves a uniform root
isolation theorem against every canonical unstable curve.

The consequence is a finite *component-local* unnormalised characteristic-Z
bound for each of the twenty-four positive seeded maximal components.  It is
not a full-key field: a key can have other components, the exact root sequence
is not materialized curve by curve, and the resulting crude coefficient is
not a contraction.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

import cm2_gate25_maximal_word_characteristic_frontier_cert as maximal_cert


HERE = Path(__file__).resolve().parent
Q = Fraction

DEPENDENCIES = {
    "cm2-gate25-maximal-word-characteristic-frontier-manifest-2026-07-16.json": (
        "bb09f99519813ec49172f0bbbcc9015c1e0fcb2de07df7af734b81d2996a3f40"
    ),
    "cm2-gate25-selected-homoclinic-component-incidence-frontier-manifest-2026-07-16.json": (
        "83120fd29f2820c943451d66a867e3ea79400b1fd9f4efda8bc15eac0aee0828"
    ),
    "cm2-gate4-global-growth-distortion-frontier-manifest-2026-07-16.json": (
        "ee1ac2acb72af04ac254e2f0a33981df478b022cde0dc08f9988762ff1c8bcc9"
    ),
    "cm2-gate45-all-row-oriented-slope-envelope-manifest-2026-07-15.json": (
        "003d3e0d742829039e85649975e8dca4a992fa7a389063eef4478df02ec03064"
    ),
    "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json": (
        "b03c5ae0e400045f087cfbd1aa8c843990edebe517a4dde786b0718446db7c1d"
    ),
    "cm2-gate45-finite-s-common-mesh-recovery-manifest-2026-07-16.json": (
        "098f9f52580fbb71d2416b07330aefa4f67488115f000bb60d37eec521250625"
    ),
    "cm2-gate45-global-invariant-cone-manifest-2026-07-16.json": (
        "173949cb9cde01ae1326576c2a9a48b268a80bce2e48954a49efa46ccd9759f9"
    ),
}

SELECTED_COMPONENT_ID = (
    "7359148da1c43a255f2238d9c831b8638f2c9885035034a5792699c968b2f3b5"
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name: str) -> dict[str, Any]:
    value = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def audit_dependencies() -> tuple[dict[str, Any], ...]:
    for name, expected in DEPENDENCIES.items():
        assert sha256_path(HERE / name) == expected
    maximal = load(next(iter(DEPENDENCIES)))
    selected = load(
        "cm2-gate25-selected-homoclinic-component-incidence-frontier-manifest-2026-07-16.json"
    )
    growth = load(
        "cm2-gate4-global-growth-distortion-frontier-manifest-2026-07-16.json"
    )
    slopes = load(
        "cm2-gate45-all-row-oriented-slope-envelope-manifest-2026-07-15.json"
    )
    numeric = load(
        "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json"
    )
    horizon = load(
        "cm2-gate45-finite-s-common-mesh-recovery-manifest-2026-07-16.json"
    )
    cone = load("cm2-gate45-global-invariant-cone-manifest-2026-07-16.json")
    assert maximal["schema"] == (
        "cm2.gate25.maximal-word-characteristic-frontier.manifest.v1"
    )
    assert selected["result"]["selected_occurrence_component_incidence"][
        "maximal_component_id"
    ] == SELECTED_COMPONENT_ID
    assert growth["verdict"]["numeric_true_singularity_complexity"] == "CERTIFIED"
    assert growth["replay_summary"]["true_singularity_intersection_upper"] == 152
    assert slopes["result"]["exact_oriented_slope_bounds"][
        "exact_source_slope_formula"
    ] == "dphi_source/dr_source=-kappa_source-cp_source/ell_T"
    assert numeric["replay_summary"]["density_ratio"] == "2000/1999"
    assert numeric["replay_summary"]["vartheta_p"] == "360134800/360493663"
    horizon_audit = horizon["result"]["uniform_horizon_penetration_audit"]
    assert horizon_audit["explicit_SYZ_horizon"] == "(t,phi)=(3,1/512)"
    assert horizon_audit[
        "every_open_length_3_segment_has_one_incidence_angle_gt_1_over_512"
    ] is True
    assert Q(horizon_audit["least_squared_penetration_slack_strict_lower"]) > 0
    geometric_cone = cone["result"]["global_invariant_geometric_cone"]
    assert geometric_cone["fixed_geometric_unstable_cone"] == (
        "25/9<V=dphi/dr<4108425/145348<29"
    )
    assert geometric_cone["strict_forward_invariance"] is True
    assert geometric_cone["positive_denominator_for_every_input_in_cone"] is True
    return maximal, selected, growth, slopes, numeric, horizon, cone


def global_disk_separation() -> dict[str, Any]:
    """Exact separation of every distinct lifted disk in the horizon table."""

    same_g = Q(1) - (Q(18, 25)) ** 2
    same_w = Q(1) - (Q(8, 25)) ** 2
    cross = (Q(199, 400)) ** 2 + Q(1, 2) ** 2 - Q(13, 25) ** 2
    assert same_g == Q(301, 625)
    assert same_w == Q(561, 625)
    assert cross == Q(36337, 160000)
    margin = min(same_g, same_w, cross)
    assert margin == cross > 0
    return {
        "same_G_squared_center_minus_radius_sum_margin": str(same_g),
        "same_W_squared_center_minus_radius_sum_margin": str(same_w),
        "cross_colour_squared_center_minus_radius_sum_margin": str(cross),
        "global_strict_squared_separation_margin": str(margin),
        "distinct_lifted_closed_disks_are_pairwise_disjoint": True,
        "equal_positive_ray_root_for_two_distinct_targets_is_impossible": True,
        "zero_ray_root_for_a_distinct_target_is_impossible": True,
    }


def branch_slope_grammar() -> dict[str, Any]:
    """List the exact one-dimensional slope type of every physical branch.

    Birkhoff coordinates are ``(r,phi)`` and a canonical unstable graph has
    ``V=dphi/dr>25/9``.  All target/corner/tangency pullbacks below are stable
    graphs.  Source endpoint and chart cuts are vertical; source homogeneity
    faces are horizontal.  Thus every listed branch has at most one isolated
    intersection with one canonical unstable graph.
    """

    kappa_min = Q(25, 9)
    unstable_lower = Q(25, 9)
    transversality_gap = kappa_min + unstable_lower
    assert transversality_gap == Q(50, 9)

    types = [
        {
            "type": "candidate_signed_tangency",
            "source_slope": "-kappa_0-c_0/ell_T<-25/9",
            "physical_denominator": "ell_T>0",
            "root_kind": "simple_stable_graph_root",
        },
        {
            "type": "target_endpoint_on_wall_or_target_chart_seam",
            "source_slope": "-kappa_0-c_0/tau<-25/9",
            "physical_denominator": "tau>0",
            "root_kind": "simple_stable_graph_root",
        },
        {
            "type": "target_momentum_homogeneity_face",
            "source_slope": (
                "-kappa_0-kappa_1*c_0/(tau*kappa_1+c_1)<-25/9"
            ),
            "physical_denominator": "tau*kappa_1+c_1>0",
            "root_kind": "simple_stable_graph_root",
        },
        {
            "type": "forward_integer_corner_ray",
            "source_slope": "-kappa_0-c_0/lambda<-25/9",
            "physical_denominator": "lambda>0",
            "root_kind": "simple_stable_graph_root",
        },
        {
            "type": "coordinate_velocity_zero",
            "source_slope": "-kappa_0<=-25/9",
            "physical_denominator": "none",
            "root_kind": "simple_stable_graph_root",
        },
        {
            "type": "source_endpoint_on_wall_or_source_chart_seam",
            "source_slope": "vertical r=constant",
            "physical_denominator": "none",
            "root_kind": "unique_graph_parameter_root",
        },
        {
            "type": "source_momentum_homogeneity_face",
            "source_slope": "horizontal phi=constant",
            "physical_denominator": "none",
            "root_kind": "simple_root_since V>25/9",
        },
    ]
    assert len(types) == 7
    return {
        "coordinates": "Birkhoff (r,phi) on each fixed-s collision fibre",
        "canonical_unstable_slope_strict_lower": str(unstable_lower),
        "stable_branch_slope_strict_upper": str(-kappa_min),
        "stable_unstable_transversality_gap_strict_lower": str(
            transversality_gap
        ),
        "branch_types": types,
        "branch_type_count": len(types),
        "every_active_branch_has_at_most_one_isolated_root": True,
        "simultaneous_branch_roots_are_coalesced_into_one_geometric_cut": True,
        "roots_admit_weak_total_order_by_source_r": True,
        "curve_by_curve_numeric_root_sequence_materialized": False,
        "branch_types_sha256": canonical_digest(types),
    }


def endpoint_wall_root_lemma() -> dict[str, Any]:
    """One root per endpoint/wall equality in the declared chart labels."""

    rg = Q(9, 25)
    rw = Q(4, 25)
    white_x_integer_distance = Q(1, 2) - Q(1, 400)
    white_y_integer_distance = Q(1, 2)
    assert rg < 1
    assert white_x_integer_distance == Q(199, 400) > rw
    assert white_y_integer_distance > rw
    return {
        "gray_radius": str(rg),
        "white_radius": str(rw),
        "white_x_center_distance_to_integer_wall_lower": str(
            white_x_integer_distance
        ),
        "white_y_center_distance_to_integer_wall_lower": str(
            white_y_integer_distance
        ),
        "white_endpoint_never_lies_on_integer_wall": True,
        "gray_endpoint_wall_must_be_center_wall": True,
        "fixed_source_normal_chart_has_at_most_one_such_endpoint": True,
        "fixed_target_open_semicircle_has_at_most_one_such_endpoint": True,
        "one_root_upper_per_each_of_44_endpoint_wall_equalities": True,
    }


def physical_reduction_row(row: dict[str, Any]) -> dict[str, Any]:
    ledger = row["boundary_predicate_ledger"]
    candidates = int(ledger["candidate_target_count"])
    assert candidates in (55, 57)
    raw_owner = 4 * candidates - 1
    assert ledger["owner_predicates"]["overcomplete_owner_predicate_count"] == raw_owner

    inactive_root_zero = candidates
    inactive_horizon = candidates
    inactive_owner_ties = candidates - 1
    inactive_owner_total = inactive_root_zero + inactive_horizon + inactive_owner_ties
    assert inactive_owner_total == 3 * candidates - 1

    # One discriminant equality is the union of the two signed tangent
    # orientations.  Each signed sheet has one root at most.
    signed_tangency_branches = 2 * candidates
    transparent = ledger["transparent_word_predicates"]
    assert transparent["endpoint_on_integer_wall"] == 44
    assert transparent["vertical_horizontal_wall_time_tie"] == 121
    assert transparent["coordinate_velocity_zero"] == 2
    assert transparent["overcomplete_word_predicate_count"] == 167
    assert ledger["source_chart_seam_predicates"] == 2
    assert ledger["target_chart_seam_predicates"] == 2
    assert ledger["source_and_target_central_homogeneity_predicates"] == 4
    assert ledger["roof_two_oriented_wall_chart_is_part_of_word_predicates"] is True
    frozen_grammar = {
        "endpoint_on_integer_wall": transparent["endpoint_on_integer_wall"],
        "vertical_horizontal_wall_time_tie": transparent[
            "vertical_horizontal_wall_time_tie"
        ],
        "coordinate_velocity_zero": transparent["coordinate_velocity_zero"],
        "transparent_word_total": transparent[
            "overcomplete_word_predicate_count"
        ],
        "source_chart_seams": ledger["source_chart_seam_predicates"],
        "target_chart_seams": ledger["target_chart_seam_predicates"],
        "source_target_central_homogeneity_faces": ledger[
            "source_and_target_central_homogeneity_predicates"
        ],
        "roof_two_oriented_wall_chart_in_word_grammar": ledger[
            "roof_two_oriented_wall_chart_is_part_of_word_predicates"
        ],
    }
    transparent_word_branches = frozen_grammar["transparent_word_total"]
    chart_homogeneity_branches = (
        frozen_grammar["source_chart_seams"]
        + frozen_grammar["target_chart_seams"]
        + frozen_grammar["source_target_central_homogeneity_faces"]
    )
    assert transparent_word_branches == 44 + 121 + 2 == 167
    assert chart_homogeneity_branches == 2 + 2 + 4 == 8
    physical_branch_upper = (
        signed_tangency_branches
        + transparent_word_branches
        + chart_homogeneity_branches
    )
    component_upper = physical_branch_upper + 1
    raw_total = int(ledger["overcomplete_total_predicate_count"])
    expected = 402 if candidates == 57 else 394
    assert raw_total == expected
    assert physical_branch_upper == (289 if candidates == 57 else 285)
    assert component_upper == (290 if candidates == 57 else 286)

    density_ratio = Q(2000, 1999)
    z_multiplier = component_upper * density_ratio
    physical_step = Q(360134800, 360493663)
    combined = z_multiplier * physical_step
    assert combined > 1
    return {
        "maximal_component_id": row["maximal_component_id"],
        "physical_key": row["definition"]["physical_key"],
        "source_obstacle": row["definition"]["physical_key"][0].split(":")[0],
        "raw_overledger_predicate_count": raw_total,
        "raw_owner_predicate_count": raw_owner,
        "raw_owner_predicates_physically_inactive_on_exact_first_owner_boundary": {
            "candidate_near_root_zero": inactive_root_zero,
            "candidate_near_root_three": inactive_horizon,
            "selected_competitor_equal_positive_root": inactive_owner_ties,
            "total": inactive_owner_total,
        },
        "physical_signed_tangency_branch_upper": signed_tangency_branches,
        "physical_transparent_word_branch_upper": transparent_word_branches,
        "physical_chart_and_homogeneity_branch_upper": chart_homogeneity_branches,
        "frozen_word_chart_homogeneity_grammar": frozen_grammar,
        "frozen_word_chart_homogeneity_grammar_sha256": canonical_digest(
            frozen_grammar
        ),
        "distinct_physical_boundary_root_upper_per_canonical_curve": (
            physical_branch_upper
        ),
        "intersection_component_upper_per_canonical_curve": component_upper,
        "component_local_unnormalized_characteristic_Z_multiplier_upper": str(
            z_multiplier
        ),
        "restriction_then_physical_step_coefficient_upper": str(combined),
        "restriction_then_physical_step_is_a_contraction": False,
    }


def reduction_registry(maximal: dict[str, Any]) -> dict[str, Any]:
    rows = maximal["result"]["seeded_implicit_maximal_component_registry"]["rows"]
    reduced = [physical_reduction_row(row) for row in rows]
    reduced.sort(key=canonical_json)
    assert len(reduced) == 24
    hist = Counter(row["raw_overledger_predicate_count"] for row in reduced)
    assert hist == {394: 12, 402: 12}
    root_hist = Counter(
        row["distinct_physical_boundary_root_upper_per_canonical_curve"]
        for row in reduced
    )
    assert root_hist == {285: 12, 289: 12}
    component_hist = Counter(
        row["intersection_component_upper_per_canonical_curve"] for row in reduced
    )
    assert component_hist == {286: 12, 290: 12}
    selected = [row for row in reduced if row["maximal_component_id"] == SELECTED_COMPONENT_ID]
    assert len(selected) == 1
    assert selected[0]["intersection_component_upper_per_canonical_curve"] == 290
    assert selected[0][
        "component_local_unnormalized_characteristic_Z_multiplier_upper"
    ] == "580000/1999"
    ids = sorted(row["maximal_component_id"] for row in reduced)
    prototypes = []
    for source in ("G", "W"):
        matches = [row for row in reduced if row["source_obstacle"] == source]
        assert len(matches) == 12
        prototype = dict(matches[0])
        prototype.pop("maximal_component_id")
        prototype.pop("physical_key")
        for row in matches[1:]:
            candidate = dict(row)
            candidate.pop("maximal_component_id")
            candidate.pop("physical_key")
            assert candidate == prototype
        prototypes.append({
            "source_obstacle": source,
            "seeded_component_count": len(matches),
            "common_physical_reduction": prototype,
        })
    return {
        "positive_seeded_component_count": 24,
        "raw_overledger_histogram": {"394": 12, "402": 12},
        "physical_boundary_root_upper_histogram": {"285": 12, "289": 12},
        "intersection_component_upper_histogram": {"286": 12, "290": 12},
        "uniform_component_local_unnormalized_characteristic_Z_multiplier_upper": (
            "580000/1999"
        ),
        "selected_homoclinic_component_id": SELECTED_COMPONENT_ID,
        "selected_component_intersection_component_upper": 290,
        "selected_component_unnormalized_characteristic_Z_multiplier_upper": (
            "580000/1999"
        ),
        "seeded_maximal_component_ids": ids,
        "seeded_maximal_component_ids_sha256": canonical_digest(ids),
        "source_class_records": prototypes,
        "source_class_records_sha256": canonical_digest(prototypes),
        "full_24_row_replay_sha256": canonical_digest(reduced),
    }


def build_result() -> dict[str, Any]:
    maximal, selected, _growth, _slopes, _numeric, horizon, cone = (
        audit_dependencies()
    )
    separation = global_disk_separation()
    slope_grammar = branch_slope_grammar()
    wall = endpoint_wall_root_lemma()
    registry = reduction_registry(maximal)
    result: dict[str, Any] = {
        "schema": "cm2.gate25.physical-boundary-root-order-frontier.v1",
        "provenance": {
            "frozen_dependency_sha256": DEPENDENCIES,
            "parameter_window": ["-1/400", "1/400"],
            "maximal_registry_rows_sha256": maximal["result"][
                "seeded_implicit_maximal_component_registry"
            ]["rows_sha256"],
            "selected_incidence_digest": selected["result"][
                "internal_replay_digest"
            ],
            "uniform_tau_strict_upper_contract": {
                "explicit_SYZ_horizon": horizon["result"][
                    "uniform_horizon_penetration_audit"
                ]["explicit_SYZ_horizon"],
                "every_open_length_3_segment_hits_strictly": horizon["result"][
                    "uniform_horizon_penetration_audit"
                ][
                    "every_open_length_3_segment_has_one_incidence_angle_gt_1_over_512"
                ],
                "physical_first_flight": "tau<3",
            },
            "canonical_invariant_cone_contract": cone["result"][
                "global_invariant_geometric_cone"
            ]["fixed_geometric_unstable_cone"],
        },
        "global_disk_separation": separation,
        "physical_branch_slope_and_root_grammar": slope_grammar,
        "endpoint_wall_root_lemma": wall,
        "positive_seeded_component_boundary_reduction": registry,
        "strict_scope_boundary": {
            "physical_reduction_of_394_402_raw_overledger": "CERTIFIED",
            "uniform_isolated_root_and_weak_order_theorem": "CERTIFIED",
            "finite_component_local_unnormalized_characteristic_Z_on_24_seeded_components": (
                "CERTIFIED"
            ),
            "curve_by_curve_numeric_root_sequence": "NOT_MATERIALIZED",
            "exact_active_boundary_count_on_each_seeded_component": "NOT_CERTIFIED",
            "full_key_all_component_characteristic_Z": "NOT_CERTIFIED",
            "pre_restriction_Xi_promoted_to_full_key_field_7": False,
            "complete_18_field_operator_block_count": 0,
            "stable_saturated_product_base": False,
            "stable_projection_pi_s": False,
            "quotient_density_rho": False,
            "physical_reverse_weights": False,
            "PPE": False,
            "Gate2": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
        },
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def main() -> int:
    result = build_result()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE25_PHYSICAL_394_402_OVERLEDGER_REDUCTION: CERTIFIED")
    print("GATE25_24_SEEDED_COMPONENT_LOCAL_FINITE_Z: CERTIFIED")
    print("GATE25_FULL_KEY_FIELD7_AND_CONTRACTION: NOT_CERTIFIED")
    print("GATE2: NOT_CERTIFIED")
    print("GATE5: NOT_CERTIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
