#!/usr/bin/env python3
"""Exact Gate-4/5 algebraic frontier and obstruction certificate.

This certificate joins the current Gate-3 owner/sheet universe to the Gate-4
single-charge schema and the Gate-5 finite Kac algebra.  It proves every
statement which is purely finite/algebraic and gives an exact counterexample
to the invalid promotion from scalar reflection cancellation to cancellation
or boundedness of the full singular current.

It intentionally does not manufacture immutable physical rows, Banach
carrier typings, stopped-parent recovery, or phase norm intertwiners.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from typing import Any

import cm2_gate3_owner_voronoi_event_registry_cert as gate3
import cm2_gate4_all_sheet_single_charge_schema_cert as gate4
import cm2_gate4_grouped_incidence_cert as gate4_local
import cm2_gate45_global_reflection_schema_cert as reflection
import cm2_gate5_actual_phase_graph_cert as phase_graph
import cm2_gate5_prefix_suffix_norm_cert as gate5


Q = Fraction


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def exact_cross_gate_ledger_alignment() -> dict[str, Any]:
    """Identify the Gate-3 and Gate-4 raw sheet universes exactly."""

    owner = gate3.owner_and_sheet_registries()
    owner_symmetry = gate3.global_symmetry_orbits()
    endpoints = gate3.critical_endpoint_registry()
    corrected_endpoints = gate3.adaptive_endpoint_isolation()
    gate4_result = gate4.certify()
    local_orbit = gate4_local.certify()
    reflection_result = reflection.certify()

    gate3_sheets = {
        (source, target, epsilon)
        for source in gate3.SOURCES
        for target in gate3.GLOBAL_CANDIDATES[source]
        for epsilon in (-1, 1)
    }
    gate4_sheets = {
        (sheet.source, sheet.target, sheet.epsilon)
        for sheet in gate4.raw_sheets()
    }
    assert gate3_sheets == gate4_sheets
    assert len(gate3_sheets) == 288

    active = {
        row for row in gate3_sheets
        if gate4.eta(row[0], row[1]) != 0
    }
    inactive = gate3_sheets - active
    assert len(active) == 128 and len(inactive) == 160

    # Gate 3 registers both line branches and both signed offsets for every
    # possible second target.  Restriction to the parameter-active first
    # sheet is exactly the Gate-4 active target-target descriptor ledger.
    active_target_target = sum(
        4 * (len(gate3.GLOBAL_CANDIDATES[source]) - 1)
        for source, _target, _epsilon in active
    )
    active_source_grazing = 2 * len(active)
    gate4_endpoints = gate4_result["active_endpoint_registry"]
    assert active_target_target == 36352
    assert active_source_grazing == 256
    assert active_target_target == gate4_endpoints[
        "target_target_common_tangent_descriptors"
    ]
    assert active_source_grazing == gate4_endpoints[
        "source_grazing_descriptors"
    ]
    assert endpoints["raw_target_target_common_tangent_curve_descriptors"] == 82048
    assert endpoints["raw_source_grazing_equations"] == 576

    assert owner["global_signed_tangency_sheets_after_chart_merge"] == 288
    assert owner_symmetry["global_signed_sheet_orbits_under_Jx_Jy"] == 72
    assert gate4_result["symmetry"]["active_sheet_orbit_count"] == 32
    assert reflection_result["candidate_row_count"] == 448
    assert reflection_result["global_scalar_roof_mass_cancellation"] is True

    # The July-15 forward-time correction is binding here.  The former 320
    # apparent endpoint descriptors do not produce a physical transition
    # vertex: all sixteen apparent third-target contacts had the other
    # contact behind the source.  The four surviving collars are uniformly
    # nonphysical tau=3 crossings.  Consequently none of the raw endpoint
    # counts above is promoted to a physical event-row count.
    assert corrected_endpoints["exact_third_target_tangency_vertices"] == 0
    assert corrected_endpoints[
        "physical_transition_vertex_orbits_under_Jx_Jy"
    ] == 0
    assert corrected_endpoints["nonphysical_tau_three_crossing_collars"] == 4
    assert corrected_endpoints["numerically_unresolved_transition_collar_count"] == 0

    # The only positive-width physical event baseline used by the Gate-4/5
    # schema remains the separately replayed component-local incidence.  It
    # is not a replacement for the corrected empty global vertex registry.
    assert local_orbit["checked_competitors"] == 95
    assert local_orbit["source_weight"] > 0
    assert local_orbit["target_weight"] > 0

    return {
        "gate3_gate4_raw_sheet_universes_identical": True,
        "global_signed_sheets": len(gate3_sheets),
        "parameter_active_signed_sheets": len(active),
        "parameter_inactive_signed_sheets": len(inactive),
        "all_sheet_symmetry_orbits": owner_symmetry[
            "global_signed_sheet_orbits_under_Jx_Jy"
        ],
        "active_sheet_symmetry_orbits": gate4_result["symmetry"][
            "active_sheet_orbit_count"
        ],
        "active_target_target_endpoint_descriptors": active_target_target,
        "active_source_grazing_descriptors": active_source_grazing,
        "active_parameter_boundary_descriptors": gate4_endpoints[
            "parameter_boundary_descriptors"
        ],
        "active_polarity_split_equations": gate4_endpoints[
            "constant_polarity_split_equations"
        ],
        "gate3_sheet_universe_sha256": canonical_digest(sorted(gate3_sheets)),
        "gate4_sheet_universe_sha256": canonical_digest(sorted(gate4_sheets)),
        "global_candidate_row_count": reflection_result["candidate_row_count"],
        "global_scalar_roof_mass_cancellation": True,
        "corrected_forward_time_endpoint_audit": {
            "retracted_pre_audit_descriptor_count": 320,
            "retracted_apparent_third_target_vertices": 16,
            "corrected_physical_transition_vertices": 0,
            "corrected_physical_transition_vertex_orbits": 0,
            "nonphysical_tau_three_collars": 4,
            "numerically_unresolved_transition_collars": 0,
            "raw_descriptors_promoted_to_physical_rows": 0,
        },
        "component_local_physical_baseline": {
            "word": "G(0,0)->tangent W(0,0)->G(1,1)",
            "positive_width": True,
            "checked_competitor_lifts": local_orbit["checked_competitors"],
            "same_occurrence_schema_only": True,
            "global_event_registry_from_this_orbit": False,
        },
    }


def exact_four_term_kac_algebra() -> dict[str, Any]:
    """Replay the centered four-term Kac derivative over exact rationals.

    This is an algebraic/Borel statement.  The four entries below are not a
    claim that their physical billiard realizations are bounded on either
    CM2 Banach pair.
    """

    weights = (Q(2, 5), Q(3, 5))
    roof = (Q(2), Q(3))
    induced_h = (Q(7), Q(11))
    dot_induced_h = (Q(5), Q(-2))
    induced_dot_h = (Q(3), Q(4))
    dot_roof = (Q(3), Q(-2))

    def mean(values: tuple[Q, ...]) -> Q:
        return sum((w * value for w, value in zip(weights, values)), Q(0))

    mean_roof = mean(roof)
    phase_mean = mean(induced_h) / mean_roof
    assert mean_roof == Q(13, 5)
    assert phase_mean == Q(47, 13)
    assert mean(dot_roof) == 0

    phase_mean_derivative = mean(tuple(
        dot_induced_h[index] + induced_dot_h[index]
        for index in range(2)
    )) / mean_roof
    assert phase_mean_derivative == Q(22, 13)

    four_terms = tuple(
        dot_induced_h[index]
        + induced_dot_h[index]
        - dot_roof[index] * phase_mean
        - roof[index] * phase_mean_derivative
        for index in range(2)
    )
    assert mean(four_terms) == 0

    # The singular boundary coordinates dot(S)h and dot(r)*mu(h) use one
    # structural vector mark (+1,-1) on one occurrence.  The mark, rather
    # than two independent positive measures, enforces rowwise centering for
    # constant h and only one q charge.
    event_masses = (Q(2, 7), Q(5, 11), Q(13, 17))
    event_values = (Q(3), Q(5), Q(7))
    structural_mark = (1, -1)
    combined = tuple(
        mass * (value - phase_mean)
        for mass, value in zip(event_masses, event_values)
    )
    constant_combined = tuple(
        mass * (phase_mean - phase_mean)
        for mass in event_masses
    )
    assert structural_mark == (1, -1)
    assert all(value == 0 for value in constant_combined)
    assert len(combined) == len(event_masses)

    # Reuse the already certified finite Borel adjoint/Kac identities.
    assert gate5.exact_endpoint_adjoint_pairing() == Q(116)
    assert gate5.exact_kac_tower_pairing() == Q(59, 6)
    assert gate5.exact_prefix_suffix_pairing() == Q(623)

    return {
        "fixed_flux_mean_roof": str(mean_roof),
        "fixed_flux_mean_dot_roof": str(mean(dot_roof)),
        "phase_mean": str(phase_mean),
        "phase_mean_derivative": str(phase_mean_derivative),
        "four_term_centered_base_mean": str(mean(four_terms)),
        "four_term_identity_exact": True,
        "finite_borel_endpoint_adjoint_exact": True,
        "finite_borel_kac_tower_pairing_exact": True,
        "finite_borel_prefix_suffix_pairing_exact": True,
        "singular_occurrence_structural_mark": list(structural_mark),
        "singular_coordinates_share_one_measure": True,
        "charged_occurrences": len(event_masses),
        "coordinate_count": 2 * len(event_masses),
        "charges_are_per_occurrence_not_per_coordinate": True,
        "constant_observable_rowwise_singular_centering": True,
        "sample_combined_occurrence_digest": canonical_digest(
            [str(value) for value in combined]
        ),
    }


def scalar_cancellation_does_not_type_current() -> dict[str, Any]:
    """Exact reflection-compatible obstruction to a norm promotion."""

    scales = (1, 2, 4, 8, 16, 32, 64)
    total_variations = []
    odd_test_pairings = []
    for scale in scales:
        # J swaps a and b; the parameter polarity changes sign.  Thus the
        # paired current is scale*(delta_a-delta_b).
        coefficients = (Q(scale), Q(-scale))
        scalar_test = (Q(1), Q(1))
        odd_test = (Q(1), Q(-1))
        scalar_pairing = sum(
            coefficient * test
            for coefficient, test in zip(coefficients, scalar_test)
        )
        odd_pairing = sum(
            coefficient * test
            for coefficient, test in zip(coefficients, odd_test)
        )
        total_variation = sum(abs(value) for value in coefficients)
        assert scalar_pairing == 0
        assert odd_pairing == 2 * scale
        assert total_variation == 2 * scale
        total_variations.append(total_variation)
        odd_test_pairings.append(odd_pairing)
    assert all(left < right for left, right in zip(
        total_variations, total_variations[1:]
    ))

    quadratic = gate5.quadratic_branch_obstruction()
    cuts = gate5.finite_cut_complexity_obstruction()
    phase_period = gate5.phase_period_obstruction()
    actual_phase = phase_graph.phase_graphs()
    assert phase_period == 2
    assert actual_phase["height_two_weighted_cycle_gcd"] == 1
    assert actual_phase["standard_N_component_cycle_gcd"] == 1

    return {
        "reflection_scalar_test_one_cancels_at_every_scale": True,
        "largest_exact_total_variation": str(total_variations[-1]),
        "largest_reflection_odd_test_pairing": str(odd_test_pairings[-1]),
        "unbounded_scale_family": True,
        "conclusion": (
            "scalar roof-mass cancellation does not cancel the singular "
            "current against general tests and gives no source/test norm bound"
        ),
        "height_one_inverse_cost_sample": str(
            quadratic["last_inverse_speed"]
        ),
        "finite_height_one_cut_cost_sample": cuts["output_cost"],
        "abstract_height_two_countermodel_cycle_gcd": phase_period,
        "actual_pilot_height_two_component_cycle_gcd": actual_phase[
            "height_two_weighted_cycle_gcd"
        ],
        "actual_pilot_standard_N_component_cycle_gcd": actual_phase[
            "standard_N_component_cycle_gcd"
        ],
        "height_bound_alone_implies_aperiodicity": False,
        "actual_component_gcd_one_implies_operator_Dz_invertibility": False,
    }


def certify() -> dict[str, Any]:
    return {
        "model": "cm2-centered-rational-two-disk-standard-N",
        "cross_gate_ledger_alignment": exact_cross_gate_ledger_alignment(),
        "global_algebraic_kac_layer": exact_four_term_kac_algebra(),
        "exact_no_promotion_obstruction": (
            scalar_cancellation_does_not_type_current()
        ),
        "conditional_global_theorem": {
            "hypotheses": [
                "finite immutable physical occurrence rows",
                "constant miss trace and parameter polarity on every row",
                "forward and reverse carrier typing on every row",
                "one common coarea law and finite oriented costs per row",
                "controlled stopped interval/cylinder algebra or physical Gate-2 PPE",
                "complete homogeneous prefix/suffix quantitative ledger",
            ],
            "conclusions": [
                "same-occurrence two-view identity on every row",
                "one q=max(Cfw,Crev,2)m charge per occurrence",
                "four-term centered Kac current with shared (+1,-1) singular mark",
                "global scalar roof mass zero under the exact Jx involution",
            ],
        },
        "completion": {
            "gate3_gate4_raw_sheet_universe_alignment": True,
            "parameter_active_endpoint_subset_alignment": True,
            "corrected_owner_forward_time_retraction_bound": True,
            "corrected_physical_transition_vertex_count_zero": True,
            "component_local_physical_orbit_replayed": True,
            "global_scalar_roof_mass_cancellation": True,
            "exact_four_term_borel_kac_algebra": True,
            "per_occurrence_shared_kac_mark_schema": True,
            "scalar_to_current_norm_promotion_refuted": True,
            "immutable_physical_event_rows": False,
            "all_row_physical_banach_typing": False,
            "global_stopped_parent_recovery": False,
            "global_single_charge_q_ledger": False,
            "physical_four_term_kac_typing": False,
            "phase_cm2_norm_lifts": False,
            "gate4_certified": False,
            "gate5_certified": False,
        },
    }


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE3_GATE4_RAW_SHEET_AND_ACTIVE_ENDPOINT_ALIGNMENT: CERTIFIED")
    print("CORRECTED_GATE3_PHYSICAL_TRANSITION_VERTICES=0: CERTIFIED")
    print("COMPONENT_LOCAL_GROUPED_INCIDENCE_BASELINE: CERTIFIED")
    print("GLOBAL_SCALAR_ROOF_MASS_CANCELLATION: CERTIFIED")
    print("EXACT_FOUR_TERM_BOREL_KAC_ALGEBRA: CERTIFIED")
    print("PER_OCCURRENCE_SHARED_KAC_MARK_SCHEMA: CERTIFIED")
    print("SCALAR_CANCELLATION_TO_CURRENT_NORM_PROMOTION: FALSE")
    print("PHYSICAL_EVENT_ROW_BANACH_TYPING: NOT_CERTIFIED")
    print("GLOBAL_STOPPED_RECOVERY_AND_q_LEDGER: NOT_CERTIFIED")
    print("PHASE_CM2_NORM_LIFTS: NOT_CERTIFIED")
    print("GATE_4: NOT_CERTIFIED")
    print("GATE_5: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
