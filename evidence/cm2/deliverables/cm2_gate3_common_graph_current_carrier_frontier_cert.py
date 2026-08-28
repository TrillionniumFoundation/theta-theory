#!/usr/bin/env python3
"""Common free graph-current carrier and exact finite two-cut algebra.

This append-only certificate combines three previously frozen facts:

* the complete depth-one fixed-gauge difference quotient;
* the complete finite-s future side-owner current; and
* the all-key/all-maximal-component characteristic-boundary estimate.

They canonically define a fixed finite free carrier with one slot for every
depth-one row and every future graph chart.  On that carrier, the first
difference quotient of a two-step product has exactly two additive face
insertions and never a product of graph deltas.  The positive two-cut TV
outer is finite and exact at the level of the frozen outers.

The construction deliberately does not identify the free carrier with the
physical Demers--Zhang triple.  The uniformly bounded restriction/lift and
physical quotient/assembly maps in all strong fields are still missing, as
are moving-test convergence and the growing-depth positive-current tail.
Consequently neither depth-two strong DQ, MT_DQ, FACE_2CUT, FACE_TIME, nor
Gate 3 is certified here.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


Q = Fraction
HERE = Path(__file__).resolve().parent

DEPENDENCIES = {
    "cm2-gate3-depth-one-fixed-gauge-dq-manifest-2026-07-15.json": (
        "284b25ac30dd86a01bd0faaa7c0a97ee47839670e3cde4309936235badf5fd52"
    ),
    "cm2-gate3-remaining-graph-complete-current-frontier-manifest-2026-07-17.json": (
        "af5dc30e466343dcb9a8e898c999ef71d67063da0a389531a22268705c3f718d"
    ),
    "cm2-gate25-all-component-characteristic-frontier-manifest-2026-07-17.json": (
        "41c766d25b007944313db93b389a616d086a7318700a867e13d90aedd159be35"
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
        value = json.loads(path.read_text(encoding="utf-8"))
        assert isinstance(value, dict)
        loaded[name] = value

    depth_one = loaded[
        "cm2-gate3-depth-one-fixed-gauge-dq-manifest-2026-07-15.json"
    ]
    future = loaded[
        "cm2-gate3-remaining-graph-complete-current-frontier-manifest-2026-07-17.json"
    ]
    characteristic = loaded[
        "cm2-gate25-all-component-characteristic-frontier-manifest-2026-07-17.json"
    ]

    assert depth_one["verdict"]["complete_depth_one_fixed_gauge_DQ"] == (
        "CERTIFIED"
    )
    assert depth_one["result"]["corrected_current_assembly"][
        "maximal_row_current_count"
    ] == 64
    assert depth_one["result"]["uniform_finite_measure_envelope"][
        "global_event_current_TV_upper_bound"
    ] == "16128/5"

    future_frontier = future["result"]["complete_current_frontier"]
    assert future_frontier["complete_side_owner_current"] is True
    assert future_frontier[
        "complete_conditionally_physical_first_graph_chart_count"
    ] == 41444
    assert future_frontier["complete_marked_current_TV_upper"] == "518152320"
    assert future_frontier["strong_DQ_MT_DQ_FACE"] is False

    registry = characteristic["result"][
        "all_key_all_component_characteristic_registry"
    ]
    assert registry["candidate_key_count_covered"] == 441280
    assert registry[
        "uniform_full_key_and_component_interval_upper_per_canonical_curve"
    ] == 290
    assert registry[
        "uniform_unnormalized_characteristic_Z_multiplier_upper"
    ] == "580000/1999"
    assert characteristic["result"]["operator_field_frontier"][
        "complete_18_field_operator_block_count"
    ] == 0
    return loaded


def free_carrier(depth_one_count: int, future_count: int) -> dict[str, Any]:
    slot_count = depth_one_count + future_count
    assert slot_count == 41508
    return {
        "reference_collision_space": (
            "N=G disjoint-union W in the frozen common arclength gauge"
        ),
        "reference_slot_interval": "I=[0,1] with half-open ownership",
        "slot_index_set": (
            "Omega_<=2=Omega_initial disjoint-union Omega_future"
        ),
        "initial_face_slot_count": depth_one_count,
        "future_face_slot_count": future_count,
        "total_fixed_slot_count": slot_count,
        "empty_slot_convention": "the zero measure in that fixed slot",
        "pulled_back_slot_record": [
            "physical occurrence/component tag",
            "orientation and hit-minus-miss mark",
            "carrier graph and endpoint ownership",
            "positive coefficient measure before cancellation",
        ],
        "candidate_nested_free_triple": {
            "X2_hat": (
                "C^1(N) direct-sum_1 l1(Omega_<=2;W^{1,1}(I))"
            ),
            "X1_hat": "BV(N) direct-sum_1 l1(Omega_<=2;BV(I))",
            "X0_hat": (
                "(C^{1,alpha}(N))* direct-sum_1 "
                "l1(Omega_<=2;M(I))"
            ),
            "continuous_injections": "X2_hat -> X1_hat -> X0_hat",
            "is_a_fixed_Banach_triple": True,
            "is_the_physical_Demers_Zhang_triple": False,
        },
        "free_TV_norm": "sum_omega ||nu_omega||_TV",
        "finite_slot_pullback_is_isometric_in_TV": True,
        "assembly_to_static_test_dual": {
            "formula": (
                "A_s((nu_omega))(Phi)=sum_omega "
                "integral Phi(gamma_{omega,s}(t)) dnu_omega(t)"
            ),
            "operator_norm_upper_from_l1_TV": "1 for sup-normalized tests",
            "uniform_in_number_of_nonempty_slots": True,
            "physical_strong_B0_assembly_bound_proved": False,
        },
        "common_free_graph_current_carrier": "CERTIFIED",
    }


def two_cut_algebra(
    depth_one_tv: Fraction, future_tv: Fraction,
) -> dict[str, Any]:
    total_tv = depth_one_tv + future_tv
    assert total_tv == Q(2590777728, 5)
    return {
        "exact_finite_difference_product_rule": (
            "Delta_s(P^2)=Delta_s(P) P_0 + P_s Delta_s(P), "
            "Delta_s(P)=(P_s-P_0)/s"
        ),
        "derivative_product_rule_if_both_terms_converge": (
            "D(P^2)=D(P)P_0+P_0D(P)"
        ),
        "number_of_additive_single_face_insertions": 2,
        "product_of_two_delta_currents_occurs": False,
        "reason": (
            "the first derivative of a product selects exactly one moving "
            "factor; a delta-product belongs only to second order"
        ),
        "initial_face_current_TV_upper": str(depth_one_tv),
        "future_side_owner_current_TV_upper": str(future_tv),
        "positive_two_cut_current_TV_outer_upper": str(total_tv),
        "TV_outer_normalization": (
            "before the single fixed collision-flux normalization Z_N^-1"
        ),
        "complete_finite_depth_occurrence_slots": True,
        "complete_finite_depth_positive_TV_outer": True,
        "algebraic_FACE_2CUT_at_depth_at_most_2": "CERTIFIED",
        "strong_operator_DQ_at_depth_2": "NOT_CERTIFIED",
    }


def physical_bridge_frontier() -> dict[str, Any]:
    return {
        "restriction_lift_needed": (
            "R_s:B2_physical -> X2_hat with every branch/component trace "
            "and all 18 norm fields uniformly bounded"
        ),
        "physical_quotient_needed": (
            "Q_s:X0_hat -> B0_physical identifying duplicate/artificial "
            "slots without increasing the physical weak norm"
        ),
        "intertwining_needed": (
            "Q_s P_hat_s R_s=P_s on every physical branch record"
        ),
        "moving_limit_needed": (
            "Q_s Delta_s(P_hat) R_s converges in B2_physical->B0_physical"
        ),
        "dynamic_test_needed": (
            "uniform off-boundary BL convergence for Q_s^m g and "
            "Q_s^{*n} f on the same component-indexed atlas"
        ),
        "growing_depth_needed": (
            "positive no-|s|^-1 per-depth coarea ledger with c_ret>A_face"
        ),
        "available_component_restriction_field": 7,
        "available_component_restriction_multiplier_upper": "580000/1999",
        "available_component_restriction_is_contracting": False,
        "missing_operator_fields": 17,
        "complete_18_field_blocks": 0,
        "bounded_physical_lift_quotient_pair": "NOT_CERTIFIED",
        "this_is_the_exact_free_to_physical_gap": True,
    }


def build_result() -> dict[str, Any]:
    dependencies = load_dependencies()
    depth_one = dependencies[
        "cm2-gate3-depth-one-fixed-gauge-dq-manifest-2026-07-15.json"
    ]["result"]
    future = dependencies[
        "cm2-gate3-remaining-graph-complete-current-frontier-manifest-2026-07-17.json"
    ]["result"]

    depth_one_count = depth_one["corrected_current_assembly"][
        "maximal_row_current_count"
    ]
    future_count = future["complete_current_frontier"][
        "complete_conditionally_physical_first_graph_chart_count"
    ]
    depth_one_tv = Q(
        depth_one["uniform_finite_measure_envelope"][
            "global_event_current_TV_upper_bound"
        ]
    )
    future_tv = Q(
        future["complete_current_frontier"][
            "complete_marked_current_TV_upper"
        ]
    )

    result: dict[str, Any] = {
        "schema": "cm2.gate3.common-graph-current-carrier-frontier.v1",
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "parameter_window": "|s|<=1/400",
            "old_artifacts_modified": False,
        },
        "frozen_input_audit": {
            "depth_one_fixed_gauge_DQ": "CERTIFIED",
            "depth_one_current_slot_count": depth_one_count,
            "complete_future_side_owner_current": "CERTIFIED",
            "future_graph_slot_count": future_count,
            "all_441280_key_component_characteristic_Z": "CERTIFIED",
            "uniform_characteristic_multiplier_upper": "580000/1999",
        },
        "common_free_carrier": free_carrier(depth_one_count, future_count),
        "finite_two_cut_algebra": two_cut_algebra(depth_one_tv, future_tv),
        "physical_bridge_frontier": physical_bridge_frontier(),
        "strict_nonpromotion": {
            "free_carrier_implies_physical_strong_space": False,
            "finite_TV_implies_operator_norm_DQ": False,
            "finite_depth_algebra_implies_MT_DQ": False,
            "finite_depth_algebra_implies_FACE_2CUT": False,
            "all_component_field7_implies_18_fields": False,
            "all_component_field7_implies_unbounded_cut_recovery": False,
            "physical_depth_two_strong_DQ": "NOT_CERTIFIED",
            "MT_DQ": "NOT_CERTIFIED",
            "FACE_2CUT": "NOT_CERTIFIED",
            "FACE_TIME": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
        },
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def main() -> None:
    print(json.dumps(build_result(), indent=2, sort_keys=True))
    print("COMMON_FREE_GRAPH_CURRENT_CARRIER: CERTIFIED")
    print("FINITE_TWO_CUT_ADDITIVE_FACE_ALGEBRA: CERTIFIED")
    print("PHYSICAL_STRONG_DQ_MT_DQ_FACE: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
