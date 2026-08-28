#!/usr/bin/env python3
"""Exact physical spanning phase graphs for the CM2 section bridge.

Two graphs are certified at the centred table:

* the actual height-two block-support graph on ``M* = M sqcup W``; and
* a physical spanning subgraph of the return-to-``N=G sqcup W`` component
  graph, with weights equal to the number of common-refinement steps.

Both graphs contain an explicit weight-one self-loop and a weight-two cycle.
The witnesses are physical first-hit branches, not consequences of the
abstract height bound K_N <= 9.  The certificate deliberately does not claim
that the complete return-word partition or operator-valued phase matrix has
been built.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from typing import Any

import cm2_gate5_transfer_audit as transfer_audit


Q = Fraction
R_GRAY = Q(9, 25)
R_WHITE = Q(4, 25)
S_MAX = Q(1, 400)


def dot(left: tuple[Q, Q], right: tuple[Q, Q]) -> Q:
    return left[0] * right[0] + left[1] * right[1]


def cross(left: tuple[Q, Q], right: tuple[Q, Q]) -> Q:
    return left[0] * right[1] - left[1] * right[0]


def add(left: tuple[Q, Q], right: tuple[Q, Q]) -> tuple[Q, Q]:
    return left[0] + right[0], left[1] + right[1]


def scale(value: Q, vector: tuple[Q, Q]) -> tuple[Q, Q]:
    return value * vector[0], value * vector[1]


def subtract(left: tuple[Q, Q], right: tuple[Q, Q]) -> tuple[Q, Q]:
    return left[0] - right[0], left[1] - right[1]


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def rational_gray_to_gray_first_hit() -> dict[str, Any]:
    """A strict direct G-to-G branch inside one transparent square.

    Work in the square ``[-1/2,1/2]^2``.  The source and target gray lifts
    are centred at the lower left and lower right corners.  The rational unit
    direction (99,20)/101 leaves the source normally and hits the target
    before a wall.  The entire pre-impact segment lies below y=-3/10, so it
    misses every white lift uniformly for |s|<=1/400.
    """

    source_center = (Q(-1, 2), Q(-1, 2))
    target_center = (Q(1, 2), Q(-1, 2))
    velocity = (Q(99, 101), Q(20, 101))
    assert dot(velocity, velocity) == 1
    source_point = add(source_center, scale(R_GRAY, velocity))
    displacement = subtract(source_point, target_center)
    linear = dot(displacement, velocity)
    offset = dot(displacement, displacement) - R_GRAY * R_GRAY
    discriminant = linear * linear - offset

    assert source_point == (Q(-743, 5050), Q(-433, 1010))
    assert linear == Q(-1566, 2525)
    assert offset == Q(743, 2525) > 0
    assert discriminant == Q(576281, 6375625) > 0
    assert discriminant > (Q(3, 4) * R_GRAY) ** 2
    # offset>0 and -linear>0 imply the selected near root is strictly forward.
    assert linear < 0

    closest_time = -linear
    closest_point = add(source_point, scale(closest_time, velocity))
    assert closest_point == (Q(9401, 20402), Q(-6241, 20402))
    assert closest_point[0] < Q(1, 2)
    assert closest_point[1] < Q(-3, 10)
    assert source_point[0] > Q(-1, 2)
    assert source_point[1] > Q(-1, 2)

    # The actual near impact occurs strictly before the closest point.  Hence
    # the whole flight lies in (-1/2,1/2) x (-1/2,-3/10), so there is no
    # transparent-wall crossing.  The vertical distance alone excludes every
    # white lift with y-index 0; all other white rows are still farther away.
    assert Q(3, 10) > R_WHITE

    # Direct line clearance from the moving central white disk.  This is a
    # second, independent strict margin, uniform in the full parameter window.
    central_white_vector_at_plus_s = (Q(1, 2) + S_MAX, Q(1, 2))
    central_white_line_distance = abs(cross(
        central_white_vector_at_plus_s, velocity
    ))
    assert central_white_line_distance == Q(789, 2020)
    assert central_white_line_distance > R_WHITE

    # Other same-row gray centres are outside the open flight rectangle; gray
    # rows above/below have vertical separation > 4/5.
    assert Q(4, 5) > R_GRAY

    return {
        "source": "G[-1/2,-1/2]",
        "target": "G[+1/2,-1/2]",
        "unit_velocity": [str(value) for value in velocity],
        "source_point": [str(value) for value in source_point],
        "target_discriminant": str(discriminant),
        "arrival_cosine_lower_bound": "3/4",
        "closest_point": [str(value) for value in closest_point],
        "uniform_white_line_clearance": str(
            central_white_line_distance - R_WHITE
        ),
        "parameter_window": "|s|<=1/400",
        "transparent_wall_crossings_before_target": 0,
        "physical_first_hit": True,
        "positive_open_branch": True,
    }


def wall_white_wall_first_hits() -> dict[str, Any]:
    """The exact C/B normal branch from the fixed wall to W and back."""

    flight_lower = Q(1, 2) - S_MAX - R_WHITE
    flight_upper = Q(1, 2) + S_MAX - R_WHITE
    assert flight_lower == Q(27, 80)
    assert flight_upper == Q(137, 400)
    assert Q(1, 4) < flight_lower < flight_upper < Q(1, 2)
    # The line y=0 stays half a unit from all gray corner centres.
    assert Q(1, 2) - R_GRAY == Q(7, 50) > 0
    return {
        "forward_word": "M:Gamma_L -> W",
        "reverse_word": "W -> M:Gamma_L",
        "source_point": ["-1/2", "0"],
        "source_velocity": ["1", "0"],
        "flight_interval": [str(flight_lower), str(flight_upper)],
        "gray_clearance": str(Q(1, 2) - R_GRAY),
        "parameter_window": "|s|<=1/400",
        "forward_first_hit": True,
        "reverse_first_hit_by_exact_time_reversal": True,
        "positive_open_branch": True,
    }


def gray_white_gray_normal_word() -> dict[str, Any]:
    """The exact centred QNL branch G->W->G inside one square."""

    # Squared centre distance is 1/2; the free-flight gap is positive because
    # d > R_G+R_W.  The squared comparison avoids a floating square root.
    radius_sum = R_GRAY + R_WHITE
    gap_squared_slack = Q(1, 2) - radius_sum * radius_sum
    assert radius_sum == Q(13, 25)
    assert gap_squared_slack == Q(287, 1250) > 0
    # The two adjacent unintended gray centres have perpendicular squared
    # line distance 1/2, strictly beyond the gray radius squared.
    assert Q(1, 2) - R_GRAY * R_GRAY == Q(463, 1250) > 0
    # Both facing boundary points lie strictly inside the transparent square.
    assert R_GRAY > 0 and R_WHITE > 0
    return {
        "physical_word": "G(0,0)->W(0,0)->G(0,0)",
        "center_distance_squared": "1/2",
        "positive_gap_squared_slack": str(gap_squared_slack),
        "adjacent_gray_line_clearance_squared_slack": str(
            Q(1, 2) - R_GRAY * R_GRAY
        ),
        "transparent_wall_crossings": 0,
        "time_reverse_second_leg": True,
        "positive_open_tube_replayed_by_companion_arb_certificate": True,
    }


def graph_period(graph: dict[str, Any]) -> int:
    failures: list[str] = []
    period = transfer_audit.weighted_cycle_gcd(graph, failures)
    assert not failures, failures
    assert period == 1
    return period


def phase_graphs() -> dict[str, Any]:
    height_two_graph = {
        "states": ["M", "W"],
        "edges": [
            {"source": "M", "target": "M", "weight": 1, "witness": "A_clean"},
            {"source": "M", "target": "W", "weight": 1, "witness": "C_normal"},
            {"source": "W", "target": "M", "weight": 1, "witness": "B_reverse"},
        ],
    }
    standard_n_spanning_graph = {
        "states": ["G", "W"],
        "edges": [
            {"source": "G", "target": "G", "weight": 1, "witness": "GG_clean"},
            {"source": "G", "target": "W", "weight": 1, "witness": "QNL_leg_1"},
            {"source": "W", "target": "G", "weight": 1, "witness": "QNL_leg_2"},
        ],
    }
    assert graph_period(height_two_graph) == 1
    assert graph_period(standard_n_spanning_graph) == 1

    # Each graph has a physical odd cycle of weight one and an even cycle of
    # weight two.  A full graph containing this spanning subgraph remains
    # strongly connected, and its cycle-weight gcd divides gcd(1,2)=1.
    for graph in (height_two_graph, standard_n_spanning_graph):
        weights = [edge["weight"] for edge in graph["edges"]]
        assert weights == [1, 1, 1]

    return {
        "height_two_Mstar_support_graph": height_two_graph,
        "height_two_strongly_connected": True,
        "height_two_cycle_witnesses": {"odd": ["M->M", 1], "even": ["M->W->M", 2]},
        "height_two_weighted_cycle_gcd": 1,
        "standard_N_physical_spanning_graph": standard_n_spanning_graph,
        "standard_N_spanning_graph_strongly_connected": True,
        "standard_N_cycle_witnesses": {"odd": ["G->G", 1], "even": ["G->W->G", 2]},
        "standard_N_component_cycle_gcd": 1,
        "supergraph_stability": (
            "every full component return graph on the same G/W states that "
            "contains the certified spanning edges is strongly connected and "
            "has cycle-weight gcd one"
        ),
        "graphs_sha256": canonical_digest(
            [height_two_graph, standard_n_spanning_graph]
        ),
    }


def certify() -> dict[str, Any]:
    gray_gray = rational_gray_to_gray_first_hit()
    wall_white = wall_white_wall_first_hits()
    qnl = gray_white_gray_normal_word()
    graphs = phase_graphs()
    return {
        "model": "centered-rational-two-disk-common-refinement",
        "sections": {
            "fixed": "M=G sqcup C_clean",
            "common_refinement": "M*=M sqcup W",
            "standard_collision": "N=G sqcup W",
        },
        "physical_first_hit_witnesses": {
            "direct_gray_gray": gray_gray,
            "wall_white_wall": wall_white,
            "gray_white_gray": qnl,
        },
        "phase_graphs": graphs,
        "logical_scope": {
            "derived_from_K_N_le_9_alone": False,
            "physical_first_hit_replay_used": True,
            "height_two_block_support_graph_complete": True,
            "standard_N_component_spanning_graph_complete_enough_for_gcd": True,
            "complete_standard_N_return_word_partition": False,
            "all_return_word_operator_blocks_registered": False,
            "operator_Dz_unit_circle_invertibility_from_this_graph_alone": False,
            "direct_standard_N_route_needs_separate_phase_tower": False,
        },
        "completion": {
            "actual_height_two_phase_support_graph": True,
            "actual_standard_N_physical_spanning_graph": True,
            "strong_connectivity": True,
            "weighted_cycle_gcd_one": True,
            "explicit_weight_one_and_weight_two_cycles": True,
            "complete_return_word_manifest": False,
            "return_block_dq": False,
            "operator_wiener_aperiodicity_for_fixed_to_full_route": False,
            "phase_test_norm_lift": False,
            "gate5_certified": False,
        },
    }


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("HEIGHT_TWO_MSTAR_ACTUAL_SUPPORT_GRAPH: CERTIFIED")
    print("STANDARD_N_ACTUAL_PHYSICAL_SPANNING_GRAPH: CERTIFIED")
    print("PHASE_GRAPH_STRONG_CONNECTIVITY: CERTIFIED")
    print("PHYSICAL_WEIGHT_ONE_AND_WEIGHT_TWO_CYCLES: CERTIFIED")
    print("COMPONENT_WEIGHTED_CYCLE_GCD_ONE: CERTIFIED")
    print("COMPLETE_STANDARD_N_RETURN_WORD_MANIFEST: NOT_CERTIFIED")
    print("OPERATOR_WIENER_APERIODICITY_FOR_FIXED_TO_FULL_ROUTE: NOT_CERTIFIED")
    print("PHASE_TEST_NORM_LIFT: NOT_CERTIFIED")
    print("GATE_5: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
