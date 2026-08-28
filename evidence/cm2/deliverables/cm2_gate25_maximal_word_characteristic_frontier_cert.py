#!/usr/bin/env python3
"""Gate-2/5 seeded maximal-word and characteristic-Z frontier.

This replay makes two deliberately different registries.

* For each of the twenty-four certified positive return cores it defines the
  unique maximal connected physical word/chart/central-homogeneity component
  containing that core.  The component is immutable by its exact predicate
  grammar and seed rectangle.  This is a genuine *implicit* maximal-component
  registry, but its boundary roots along arbitrary standard curves have not
  been isolated.
* On the smaller rational core rectangles themselves, monotonicity of the
  standard-curve graph gives at most one retained interval.  This closes a
  finite unnormalised characteristic-Z estimate on the positive inner
  subfamily.  It is not promoted to the maximal components or to full keys.

The selected QNL loop is also audited against the Gate-2 endpoint schema.
No stable-saturated base, quotient branch, rho, reverse weight or endpoint
carrier is invented, so Gates 2 and 5 remain fail-closed.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any

from flint import arb

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate3_candidate_first_hit_cert as first_hit


HERE = Path(__file__).resolve().parent
Q = Fraction

DEPENDENCIES = (
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json",
    "cm2-gate25-roof-two-wall-chart-frontier-manifest-2026-07-16.json",
    "cm2-gate25-universal-operator-endpoint-template-frontier-manifest-2026-07-16.json",
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json",
    "cm2-gate4-componentwise-global-growth-recovery-frontier-manifest-2026-07-16.json",
    "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json",
    "cm2-gate1-numeric-holonomy-tail-twisting-frontier-manifest-2026-07-16.json",
    "cm2-gate1-global-coding-class-h-separation-frontier-manifest-2026-07-16.json",
    "cm2-gate2-collision-key-stable-quotient-frontier-manifest-2026-07-16.json",
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


def dependency_hashes() -> dict[str, str]:
    return {name: sha256_path(HERE / name) for name in DEPENDENCIES}


def exact_core_key(core: core_cert.Core) -> list[Any]:
    return [
        core.chart_id,
        core.target_id,
        list(core.crossings),
        len(core.crossings) + 1,
    ]


def boundary_predicate_ledger(core: core_cert.Core) -> dict[str, Any]:
    """A finite over-ledger for every possible boundary of the component.

    The ledger is intentionally overcomplete.  Candidate roots may disappear
    only through discriminant/forward-time/horizon equalities, or exchange
    ownership through a root equality.  A clean straight wall record can
    change only at a zero velocity, an endpoint on an integer wall, or an
    equal vertical/horizontal wall time.  The target-lift universe lies in
    [-4,4]^2 and all radii are <1, so the integer ledger [-5,5] is exhaustive.
    Counting predicate *families* does not bound their intersections with a
    moving standard curve; that missing root-isolation is kept explicit.
    """

    candidates = tuple(first_hit.candidate_ids(core.chart_id))
    assert core.target_id in candidates
    candidate_count = len(candidates)
    assert candidate_count in (55, 57)

    integer_walls = tuple(range(-5, 6))
    endpoint_on_wall = 4 * len(integer_walls)  # q_x,h_x,q_y,h_y
    corner_time_ties = len(integer_walls) ** 2
    velocity_zeros = 2
    word_count = endpoint_on_wall + corner_time_ties + velocity_zeros
    assert word_count == 167

    # For each retained candidate: discriminant=0, root=0 and root=3.
    # For every competitor: selected-root=competitor-root.
    owner_count = 3 * candidate_count + (candidate_count - 1)
    assert owner_count == 4 * candidate_count - 1

    ledger = {
        "candidate_target_count": candidate_count,
        "owner_predicates": {
            "candidate_discriminant_zero": candidate_count,
            "candidate_forward_root_zero": candidate_count,
            "candidate_horizon_root_three": candidate_count,
            "selected_competitor_root_tie": candidate_count - 1,
            "overcomplete_owner_predicate_count": owner_count,
        },
        "transparent_word_predicates": {
            "integer_wall_index_range": [-5, 5],
            "endpoint_on_integer_wall": endpoint_on_wall,
            "vertical_horizontal_wall_time_tie": corner_time_ties,
            "coordinate_velocity_zero": velocity_zeros,
            "overcomplete_word_predicate_count": word_count,
        },
        "source_chart_seam_predicates": 2,
        "target_chart_seam_predicates": 2,
        "source_and_target_central_homogeneity_predicates": 4,
        "roof_two_oriented_wall_chart_is_part_of_word_predicates": True,
    }
    ledger["overcomplete_total_predicate_count"] = (
        owner_count + word_count + 2 + 2 + 4
    )
    ledger["predicate_ledger_sha256"] = canonical_digest(ledger)
    return ledger


def seeded_maximal_component_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for core in core_cert.physical_cores():
        suffix_direction = core_cert.expected_suffix_direction(core)
        boundary = boundary_predicate_ledger(core)
        definition = {
            "physical_key": exact_core_key(core),
            "parameter_fibre": "fixed s in [-1/400,1/400]",
            "seed_open_rectangle": {
                "t": [str(core.t0), str(core.t1)],
                "p=sin(phi)": [str(core.p0), str(core.p1)],
            },
            "component_predicate": (
                "the connected component containing the seed rectangle of: "
                "exact return-word domain D_w(s), fixed source chart, fixed "
                "target open-semicircle chart, every declared intermediate "
                "oriented transparent-wall chart, and source/target central "
                "homogeneity abs(p)<3/10"
            ),
            "maximality_scope": (
                "maximal connected component of the displayed exact physical "
                "word/chart/central-homogeneity predicate; not a maximal "
                "component after forgetting chart or homogeneity labels"
            ),
            "target_open_semicircle_direction": list(suffix_direction),
            "boundary_predicate_ledger_sha256": boundary[
                "predicate_ledger_sha256"
            ],
        }
        row = {
            "maximal_component_id": canonical_digest(definition),
            "definition": definition,
            "boundary_predicate_ledger": boundary,
            "seed_is_uniformly_physical_and_strict_first_hit": True,
            "seed_is_central_at_source_and_target": True,
            "seed_supplies_strictly_positive_collision_SRB_mass": True,
            "component_nonempty_for_every_parameter_fibre": True,
            "boundary_roots_on_arbitrary_short_standard_curves_isolated": False,
        }
        rows.append(row)
    rows.sort(key=lambda row: canonical_json(row["definition"]["physical_key"]))
    assert len(rows) == 24
    assert len({row["maximal_component_id"] for row in rows}) == 24
    assert len({canonical_json(row["definition"]["physical_key"]) for row in rows}) == 24
    counts = Counter(
        row["boundary_predicate_ledger"]["candidate_target_count"] for row in rows
    )
    assert counts == {55: 12, 57: 12}
    totals = Counter(
        row["boundary_predicate_ledger"]["overcomplete_total_predicate_count"]
        for row in rows
    )
    assert totals == {394: 12, 402: 12}
    return rows


def core_normal_angle_interval(core: core_cert.Core) -> tuple[arb, arb]:
    """Return the physical source-normal angle interval in ``[0,2*pi)``."""

    cell = core.chart_id.split(":")[1]
    t0 = core_cert.arbq(core.t0)
    t1 = core_cert.arbq(core.t1)
    pi = arb.pi()
    if cell == "E":
        lo, hi = t0.asin(), t1.asin()
        if core.t1 < 0:
            lo, hi = lo + 2 * pi, hi + 2 * pi
    elif cell == "N":
        lo, hi = pi / 2 - t1.asin(), pi / 2 - t0.asin()
    elif cell == "W":
        lo, hi = pi - t1.asin(), pi - t0.asin()
    elif cell == "S":
        lo, hi = 3 * pi / 2 + t0.asin(), 3 * pi / 2 + t1.asin()
    else:  # pragma: no cover - the frozen chart alphabet is exhaustive.
        raise ValueError(cell)
    assert bool(lo >= 0) and bool(hi < 2 * pi) and bool(lo < hi)
    return lo, hi


def global_core_arclength_separation() -> dict[str, Any]:
    """Audit all cross-chart as well as within-chart core separations.

    Standard curves live on one component of the disjoint collision section
    ``G sqcup W`` but may cross a normal-chart seam.  We therefore order all
    twelve physical normal arcs on each source obstacle, rather than relying
    only on the three-band calculation inside one chart.
    """

    rows = []
    pi = arb.pi()
    for source in ("G", "W"):
        intervals = []
        for core in core_cert.physical_cores():
            if core.source != source:
                continue
            lo, hi = core_normal_angle_interval(core)
            intervals.append((lo, hi, exact_core_key(core)))
        intervals.sort(key=lambda row: float(row[0].mid()))
        assert len(intervals) == 12
        for index, (lo, hi, key) in enumerate(intervals):
            next_lo = intervals[(index + 1) % len(intervals)][0]
            gap = next_lo - hi if index + 1 < len(intervals) else next_lo + 2 * pi - hi
            # The closest cross-chart diagonal pair has angular gap
            # pi/2-2*asin(7/10)>1/100.  The exhaustive interval ordering
            # verifies that no other pair is closer.
            assert bool(gap > core_cert.arbq(Q(1, 100)))
            rows.append({
                "source": source,
                "physical_key": key,
                "normal_angle_interval": [str(lo), str(hi)],
                "cyclic_gap_to_next_strict_lower": "1/100",
            })
    assert len(rows) == 24
    # Boundary arclength is R*dtheta and min(R_G,R_W)=4/25.
    source_r_gap = Q(4, 25) * Q(1, 100)
    assert source_r_gap == Q(1, 625)
    return {
        "source_collision_components": ["G", "W"],
        "physical_normal_arc_count_per_source": 12,
        "all_cross_chart_and_within_chart_cyclic_gaps_checked": True,
        "global_pairwise_source_normal_angle_gap_strict_lower": "1/100",
        "global_pairwise_source_r_gap_strict_lower": str(source_r_gap),
        "physical_arc_order_ledger_sha256": canonical_digest(rows),
    }


def inner_core_characteristic_lemma() -> dict[str, Any]:
    cores = core_cert.physical_cores()
    by_chart: dict[str, list[tuple[Q, Q]]] = defaultdict(list)
    for core in cores:
        by_chart[core.chart_id].append((core.t0, core.t1))
    assert len(by_chart) == 8

    expected_bands = {
        (Q(-7, 10), Q(-69, 100)),
        (Q(1, 100), Q(1, 50)),
        (Q(69, 100), Q(7, 10)),
    }
    for bands in by_chart.values():
        assert set(bands) == expected_bands
        assert len(bands) == 3

    # The least t-gap between the three bands is 67/100.  Since
    # dr/dt=R/sqrt(1-t^2)>=R and R>=4/25, the r-gap is at least 67/625.
    minimum_t_gap = Q(67, 100)
    minimum_r_gap = Q(4, 25) * minimum_t_gap
    delta_1 = Q(1, 37724355673552103994)
    assert minimum_r_gap == Q(67, 625)
    assert delta_1 < minimum_r_gap

    global_separation = global_core_arclength_separation()
    assert Q(global_separation["global_pairwise_source_r_gap_strict_lower"]) > delta_1

    # On either oriented standard-curve chart, p is strictly monotone in r;
    # t is strictly monotone in r on the source normal chart.  Intersecting
    # the graph with a t interval and a p interval therefore gives an interval.
    component_multiplicity = 1
    artificial_endpoint_upper = 2

    density_ratio = Q(2000, 1999)
    xi = Q(900337, 901685)
    physical_vartheta = density_ratio * xi
    restricted_vartheta = density_ratio * physical_vartheta
    assert physical_vartheta == Q(360134800, 360493663)
    assert restricted_vartheta == Q(720269600000, 720626832337)
    assert restricted_vartheta < 1

    # If rho has sup/inf<=R on W and I is the sole retained interval, then
    # p_I/|I| <= R p_W/|W|.  This is an unnormalised source estimate and does
    # not claim a uniform bound after conditioning on an arbitrarily tiny
    # retained mass.
    return {
        "registered_inner_core_rectangle_count": 24,
        "source_chart_count": 8,
        "three_t_bands_per_source_chart": [
            ["-7/10", "-69/100"],
            ["1/100", "1/50"],
            ["69/100", "7/10"],
        ],
        "minimum_inter_band_t_gap": str(minimum_t_gap),
        "minimum_inter_band_source_r_gap": str(minimum_r_gap),
        "all_cross_chart_and_within_chart_cyclic_gaps_checked": True,
        "global_pairwise_source_normal_angle_gap_strict_lower": "1/100",
        "global_pairwise_source_r_gap_strict_lower": "1/625",
        "physical_arc_order_ledger_sha256": global_separation[
            "physical_arc_order_ledger_sha256"
        ],
        "short_curve_delta_1": str(delta_1),
        "standard_curve_monotonicity_contract": (
            "t is monotone in boundary arclength and p is strictly monotone "
            "on either oriented graph chart"
        ),
        "intersection_component_multiplicity_upper_per_short_curve": (
            component_multiplicity
        ),
        "artificial_boundary_endpoint_count_upper_per_nonempty_intersection": (
            artificial_endpoint_upper
        ),
        "invariant_density_ratio_upper": str(density_ratio),
        "unnormalized_characteristic_Z_restriction": (
            "Z_*(1_core F)<= (2000/1999) Z_*(F)"
        ),
        "pre_restriction_Xi_strict_upper": str(xi),
        "physical_step_vartheta_p": str(physical_vartheta),
        "restriction_then_physical_step_contraction_strict_upper": str(
            restricted_vartheta
        ),
        "restriction_then_physical_step_margin": str(1 - restricted_vartheta),
        "log_density_regularity_preserved_by_interval_restriction": True,
        "finite_unnormalized_characteristic_Z_on_positive_inner_subfamily": True,
        "normalized_cost_uniform_after_conditioning_on_retained_mass": False,
        "reason_normalized_cost_not_uniform": (
            "the retained mass can tend to zero when a curve clips a core corner"
        ),
    }


def endpoint_packet_frontier(
    twisting: dict[str, Any], coding: dict[str, Any], gate2: dict[str, Any]
) -> dict[str, Any]:
    twist = twisting["result"]
    assert len(twist["four_selected_twisting_wedges"]) == 4
    coding_result = coding["result"]
    assert coding_result["scope_limits"][
        "finite_faithful_clean_horseshoe_coding"
    ] is True
    assert coding_result["scope_limits"][
        "single_representative_class_H_and_weak_typicality"
    ] is False
    gate2_result = gate2["result"]
    assert gate2_result["completion"]["gate2_certified"] is False
    return {
        "selected_common_fiber_loop_matrix": twist[
            "selected_homoclinic_holonomy"
        ]["infinite_matrix_enclosure"],
        "selected_four_nonzero_wedges": twist["four_selected_twisting_wedges"],
        "finite_faithful_horseshoe_coding_available": True,
        "collision_word_or_horseshoe_symbol_is_stable_quotient_branch_label": False,
        "selected_occurrence_membership_in_one_of_24_maximal_word_components_certified": False,
        "stable_saturated_product_base": False,
        "stable_projection_pi_s": False,
        "quotient_density_rho": False,
        "onto_inverse_branch_label_a": False,
        "physical_reverse_weight_p_a": False,
        "same_carrier_endpoint_maps_X_a_Y_a": False,
        "pointwise_endpoint_slope_identity": False,
        "endpoint_denominator_lower_bound": False,
        "Gate2_fields_9_to_12_completed": False,
        "strict_reason": (
            "a common-fiber cocycle loop and a collision-word component do not "
            "define the stable quotient carrier or its reverse kernel"
        ),
    }


def build_result() -> dict[str, Any]:
    core_manifest = load(DEPENDENCIES[0])
    wall_manifest = load(DEPENDENCIES[1])
    template_manifest = load(DEPENDENCIES[2])
    gate5 = load(DEPENDENCIES[3])
    componentwise = load(DEPENDENCIES[4])
    numeric = load(DEPENDENCIES[5])
    twisting = load(DEPENDENCIES[6])
    coding = load(DEPENDENCIES[7])
    gate2 = load(DEPENDENCIES[8])

    frozen_core = core_manifest["result"]["physical_return_core_registry"]
    assert frozen_core["physical_compact_homogeneous_core_count"] == 24
    assert frozen_core[
        "collision_SRB_normalized_mass_strict_lower_using_pi_lt_22_over_7"
    ] == "147/550000"
    assert wall_manifest["result"]["roof_two_wall_chart_registry"][
        "all_28_core_local_roof_level_prefix_suffix_pairs_have_charts"
    ] is True
    template = template_manifest["result"]
    assert template["physical_return_registry_binding"][
        "complete_18_field_block_count"
    ] == 0
    assert gate5["result"]["required_operator_field_schema"][
        "required_field_count_per_physical_homogeneous_level"
    ] == 18
    assert componentwise["replay_summary"]["global_one_step_Xi_strict_upper"] == (
        "900337/901685"
    )
    assert numeric["replay_summary"]["density_ratio"] == "2000/1999"

    rows = seeded_maximal_component_rows()
    inner = inner_core_characteristic_lemma()
    endpoint = endpoint_packet_frontier(twisting, coding, gate2)

    result: dict[str, Any] = {
        "schema": "cm2.gate25.maximal-word-characteristic-frontier.v1",
        "provenance": {
            "frozen_dependency_sha256": dependency_hashes(),
            "parameter_window": ["-1/400", "1/400"],
            "required_operator_field_schema_sha256": gate5["result"][
                "required_operator_field_schema"
            ]["required_field_schema_sha256"],
        },
        "seeded_implicit_maximal_component_registry": {
            "candidate_key_universe_size": 441280,
            "positive_distinct_key_count": 24,
            "seeded_maximal_component_count": 24,
            "roof_histogram": {"1": 20, "2": 4},
            "positive_collision_SRB_mass_strict_lower": "147/550000",
            "maximality_is_set_theoretic_connected_component_of_exact_predicate": True,
            "boundary_predicate_families_are_frozen": True,
            "boundary_root_order_and_intersection_multiplicity_resolved": False,
            "rows": rows,
            "rows_sha256": canonical_digest(rows),
        },
        "positive_inner_core_characteristic_Z": inner,
        "full_key_characteristic_frontier": {
            "maximal_component_boundary_intersection_multiplicity": None,
            "maximal_component_boundary_Z": None,
            "pre_restriction_Xi_promoted_to_full_key_field_7": False,
            "full_key_field_14_regular_density_operator_cost": False,
            "full_key_field_15_standard_family_operator_cost": False,
            "full_key_field_16_flux_face_operator_cost": False,
            "full_key_field_17_dynamic_test_operator_cost": False,
            "why_inner_result_does_not_promote": (
                "the maximal components may meet their word/owner/chart boundary "
                "many times; the one-interval proof uses the artificial rational "
                "inner rectangles and is not a boundary theorem for the full key"
            ),
            "first_missing_executable_interface": (
                "root-isolated ordered intersections of every frozen maximal-word "
                "boundary predicate with every canonical short standard curve"
            ),
        },
        "selected_loop_stable_quotient_endpoint_frontier": endpoint,
        "operator_schema_status": {
            "full_key_field_count_completed_on_each_of_24_keys": 1,
            "full_key_completed_field": "nonempty_or_empty_domain_proof=NONEMPTY",
            "implicit_maximal_component_ids_materialized_on_positive_subfamily": True,
            "core_local_fields_5_6_templates": True,
            "core_local_characteristic_field_7_seed": True,
            "core_local_fields_14_15_unnormalized_seeds": True,
            "these_core_local_seeds_are_full_key_fields": False,
            "complete_18_field_operator_block_count": 0,
        },
        "strict_completion_boundary": {
            "positive_seeded_maximal_component_registry": "CERTIFIED_IMPLICIT",
            "positive_inner_core_characteristic_multiplicity_and_Z": "CERTIFIED",
            "full_key_characteristic_Z": "NOT_CERTIFIED",
            "full_key_fields_7_and_14_to_17": "NOT_CERTIFIED",
            "stable_quotient_endpoint_packet": "NOT_CERTIFIED",
            "Gate2": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
        },
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def main() -> int:
    result = build_result()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE5_POSITIVE_SEEDED_MAXIMAL_WORD_COMPONENTS: CERTIFIED_IMPLICIT")
    print("GATE5_POSITIVE_INNER_CORE_CHARACTERISTIC_Z: CERTIFIED")
    print("GATE5_FULL_KEY_CHARACTERISTIC_Z: NOT_CERTIFIED")
    print("GATE2_STABLE_QUOTIENT_ENDPOINT_PACKET: NOT_CERTIFIED")
    print("GATE2: NOT_CERTIFIED")
    print("GATE5: NOT_CERTIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
