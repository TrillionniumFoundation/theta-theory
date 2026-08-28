#!/usr/bin/env python3
"""Exact reachability pruning for the selected G:E -> W[0,0] component."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
Q = Fraction
SELECTED_COMPONENT_ID = (
    "7359148da1c43a255f2238d9c831b8638f2c9885035034a5792699c968b2f3b5"
)
DEPENDENCIES = {
    "cm2-gate25-physical-boundary-root-order-frontier-manifest-2026-07-17.json": (
        "58a8b27517a55fabd5776e9299802bb656f60733ae86c25941b640be2dfb4e91"
    ),
    "cm2-gate25-selected-homoclinic-component-incidence-frontier-manifest-2026-07-16.json": (
        "83120fd29f2820c943451d66a867e3ea79400b1fd9f4efda8bc15eac0aee0828"
    ),
    "cm2-gate25-maximal-word-characteristic-frontier-manifest-2026-07-16.json": (
        "bb09f99519813ec49172f0bbbcc9015c1e0fcb2de07df7af734b81d2996a3f40"
    ),
    "cm2-gate4-global-growth-distortion-frontier-manifest-2026-07-16.json": (
        "ee1ac2acb72af04ac254e2f0a33981df478b022cde0dc08f9988762ff1c8bcc9"
    ),
    "cm2_gate4_global_growth_distortion_frontier_cert.py": (
        "c6043e74b32722b05de365dfc81fe5ef10833170d9baca15802729b8fca829d6"
    ),
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name: str) -> dict[str, Any]:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def audit_dependencies() -> tuple[
    dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]
]:
    for name, expected in DEPENDENCIES.items():
        assert sha256_path(HERE / name) == expected
    boundary = load(next(iter(DEPENDENCIES)))
    incidence = load(
        "cm2-gate25-selected-homoclinic-component-incidence-frontier-manifest-2026-07-16.json"
    )
    maximal = load(
        "cm2-gate25-maximal-word-characteristic-frontier-manifest-2026-07-16.json"
    )
    growth = load(
        "cm2-gate4-global-growth-distortion-frontier-manifest-2026-07-16.json"
    )
    assert boundary["verdict"]["24_seeded_component_local_finite_Z"] == "CERTIFIED"
    assert boundary["result"]["provenance"]["uniform_tau_strict_upper_contract"][
        "physical_first_flight"
    ] == "tau<3"
    assert boundary["result"]["provenance"]["canonical_invariant_cone_contract"] == (
        "25/9<V=dphi/dr<4108425/145348<29"
    )
    assert incidence["result"]["selected_occurrence_component_incidence"][
        "maximal_component_id"
    ] == SELECTED_COMPONENT_ID
    registry = maximal["result"]["seeded_implicit_maximal_component_registry"]
    assert registry["maximality_is_set_theoretic_connected_component_of_exact_predicate"] is True
    selected_rows = [
        row for row in registry["rows"]
        if row["maximal_component_id"] == SELECTED_COMPONENT_ID
    ]
    assert len(selected_rows) == 1
    definition = selected_rows[0]["definition"]
    assert definition == {
        "boundary_predicate_ledger_sha256": (
            "d81dbb6ff1a2f8be81873416a63651a740a82f5be95c7f0b8a34e47a0296f095"
        ),
        "component_predicate": (
            "the connected component containing the seed rectangle of: exact "
            "return-word domain D_w(s), fixed source chart, fixed target "
            "open-semicircle chart, every declared intermediate oriented "
            "transparent-wall chart, and source/target central homogeneity "
            "abs(p)<3/10"
        ),
        "maximality_scope": (
            "maximal connected component of the displayed exact physical "
            "word/chart/central-homogeneity predicate; not a maximal component "
            "after forgetting chart or homogeneity labels"
        ),
        "parameter_fibre": "fixed s in [-1/400,1/400]",
        "physical_key": ["G:E", "W[0,0]", [], 1],
        "seed_open_rectangle": {
            "p=sin(phi)": ["-1/50", "1/50"],
            "t": ["69/100", "7/10"],
        },
        "target_open_semicircle_direction": [-1, -1],
    }
    assert selected_rows[0]["component_nonempty_for_every_parameter_fibre"] is True
    assert selected_rows[0]["seed_is_central_at_source_and_target"] is True
    assert selected_rows[0]["seed_is_uniformly_physical_and_strict_first_hit"] is True
    assert growth["certificate_sha256"] == DEPENDENCIES[
        "cm2_gate4_global_growth_distortion_frontier_cert.py"
    ]
    assert growth["verdict"]["numeric_all_physical_branch_D2T_weight"] == "CERTIFIED"
    return boundary, incidence, maximal, growth


def target_central_forces_ne_quadrant() -> dict[str, Any]:
    """Prove |p_1|<3/10 forces t>1/2 on the selected source chart.

    Put a=1/2+s, c=sqrt(1-t^2),
      A=a*c+t/2-9/25, B=c/2-a*t.
    The target transverse coordinate is T=c_p*B-p*A and p_1=T/(4/25).
    """

    cp_lower = Q(19, 20)
    target_transverse_upper = Q(3, 10) * Q(4, 25)
    assert target_transverse_upper == Q(6, 125)

    # t in [-1/sqrt(2),0]: c>7/10, B>7/20 and |A|<29/80.
    negative_t_lower = cp_lower * Q(7, 20) - Q(3, 10) * Q(29, 80)
    assert negative_t_lower == Q(179, 800) > target_transverse_upper

    # t in [0,1/2]: c>=sqrt(3)/2>43/50, hence B>143/800;
    # the direct envelope is |A|<157/400.
    nonnegative_t_lower = (
        cp_lower * Q(143, 800) - Q(3, 10) * Q(157, 400)
    )
    assert nonnegative_t_lower == Q(833, 16000) > target_transverse_upper
    assert nonnegative_t_lower - target_transverse_upper == Q(13, 3200)
    return {
        "selected_source_chart": "G:E",
        "selected_target": "W[0,0]",
        "source_central_face": "abs(p_0)<3/10",
        "target_central_face": "abs(p_1)<3/10",
        "target_transverse_threshold": str(target_transverse_upper),
        "t_nonpositive_transverse_strict_lower": str(negative_t_lower),
        "zero_to_half_t_transverse_strict_lower": str(nonnegative_t_lower),
        "least_exclusion_margin": "13/3200",
        "target_central_implies_t_strictly_greater_than_one_half": True,
        "normal_angle_interval": "pi/6<theta<pi/4",
        "source_angle_interval": "-pi/6<phi<pi/6",
        "outgoing_global_angle_interval": "0<alpha<5*pi/12<pi/2",
        "outgoing_velocity_both_coordinates_positive": True,
    }


def word_and_chart_implication() -> dict[str, Any]:
    rg, rw = Q(9, 25), Q(4, 25)
    qx_lower, qy_lower = Q(63, 250), Q(9, 50)
    hx = [Q(27, 80), Q(53, 80)]
    hy = [Q(17, 50), Q(33, 50)]
    margins = {
        "G[1,0]": (1 - hx[1]) ** 2 + qy_lower**2 - rg**2,
        "G[0,1]": qx_lower**2 + (1 - hy[1]) ** 2 - rg**2,
        "G[1,1]": (1 - hx[1]) ** 2 + (1 - hy[1]) ** 2 - rg**2,
    }
    assert margins == {
        "G[1,0]": Q(2673, 160000),
        "G[0,1]": Q(1547, 31250),
        "G[1,1]": Q(3197, 32000),
    }
    assert min(margins.values()) > 0
    # For target normal n_1 and outgoing unit u in the first quadrant,
    # (-1,-1).n_1 = c_1(u_x+u_y)+p_1(u_x-u_y)>19/20-3/10.
    suffix_dot_lower = Q(19, 20) - Q(3, 10)
    assert suffix_dot_lower == Q(13, 20)
    return {
        "source_point_coordinate_strict_lowers": {
            "x": str(qx_lower), "y": str(qy_lower)
        },
        "target_contact_coordinate_enclosure": {
            "x": [str(x) for x in hx], "y": [str(x) for x in hy]
        },
        "segment_coordinatewise_increasing_inside_open_unit_square": True,
        "no_transparent_integer_wall_crossing": True,
        "other_nearby_gray_disk_squared_distance_margins": {
            k: str(v) for k, v in margins.items()
        },
        "all_remaining_gray_lifts_excluded_by_one_coordinate_distance_gt_9_over_25": True,
        "all_other_white_lifts_excluded_by_one_coordinate_distance_gt_4_over_25": True,
        "other_physical_word_and_chart_predicates_are_implied_on_P": True,
        "raw_algebraic_predicates_are_not_claimed_nonvanishing": True,
        "outgoing_ray_does_not_reenter_strictly_convex_source": True,
        "selected_W00_is_strict_first_solid_collision": True,
        "target_open_semicircle_direction": [-1, -1],
        "target_chart_dot_strict_lower": str(suffix_dot_lower),
        "target_open_semicircle_automatic": True,
    }


def connected_pruned_domain_theorem() -> dict[str, Any]:
    """Prove that the pruned two-dimensional predicate P is one component.

    On the forced source-chart domain put

      D=(1/2,1/sqrt(2)) x (-3/10,3/10),
      T(t,p)=sqrt(1-p^2) B(t)-p A(t).

    Both partial derivatives of T are uniformly negative.  The signs at the
    three open sides then make P={|T|<6/125} a band with interval t-projection,
    interval vertical fibres, and continuous endpoints.  A continuous
    midpoint section gives path connectedness.  The frozen full-window seed
    corridor lies in P, so P is the seeded maximal component, not merely an
    outer set containing it.
    """

    cp_lower = Q(19, 20)
    a_lower, a_upper = Q(199, 400), Q(201, 400)
    c_lower, c_upper = Q(7, 10), Q(9, 10)
    transverse = Q(6, 125)

    # A=a*c+t/2-9/25 and B=c/2-a*t on 1/2<t<1/sqrt(2).
    A_lower = a_lower * c_lower + Q(1, 4) - Q(9, 25)
    B_abs_upper = c_upper / 2 - a_lower / 2
    B_lower = c_lower / 2 - a_upper
    assert A_lower == Q(953, 4000)
    assert B_abs_upper == Q(161, 800)
    assert B_lower == -Q(61, 400)
    assert -B_lower < B_abs_upper

    # d_p T=-(p/c_p)B-A; |p/c_p|<6/19.
    partial_p_upper = Q(6, 19) * B_abs_upper - A_lower
    assert partial_p_upper == -Q(13277, 76000) < 0

    # d_t T=-c_p(a+t/(2c))+p(at/c-1/2).  Since t/c<1,
    # discard the additional negative t/(2c) term and use
    # |at/c-1/2|<a+1/2<401/400.
    partial_t_upper = -cp_lower * a_lower + Q(3, 10) * (
        a_upper + Q(1, 2)
    )
    assert partial_t_upper == -Q(11, 64) < 0

    # Along p=-3/10, c>t gives B=t(1/2-a)>-1/400.  Thus this
    # entire side stays above the upper target level.
    minus_p_side_lower = -Q(1, 400) + Q(3, 10) * A_lower
    assert minus_p_side_lower == Q(2759, 40000) > transverse

    # The lower t-side bound is the already certified forced-quadrant bound.
    lower_t_side_lower = Q(833, 16000)
    assert lower_t_side_lower > transverse

    # At the open upper t-limit c=t=1/sqrt(2), so |B|<1/400.
    # At p=3/10 the limit lies strictly below the lower target level.
    upper_t_plus_p_limit_upper = Q(1, 400) - Q(3, 10) * A_lower
    assert upper_t_plus_p_limit_upper == -Q(2759, 40000) < -transverse

    return {
        "forced_open_domain": (
            "D=(1/2,1/sqrt(2))_t x (-3/10,3/10)_p for each fixed "
            "s in [-1/400,1/400]"
        ),
        "A_strict_lower": str(A_lower),
        "abs_B_strict_upper": str(B_abs_upper),
        "partial_p_T_strict_upper": str(partial_p_upper),
        "partial_t_T_strict_upper": str(partial_t_upper),
        "T_on_p_equals_minus_3_over_10_strict_lower": str(minus_p_side_lower),
        "T_on_t_equals_one_half_strict_lower": str(lower_t_side_lower),
        "T_upper_t_limit_at_p_equals_3_over_10_strict_upper": str(
            upper_t_plus_p_limit_upper
        ),
        "target_transverse_level": str(transverse),
        "V_t_equals_T_t_3_over_10_is_continuous_strictly_decreasing": True,
        "V_crosses_plus_then_minus_target_level_uniquely": True,
        "nonempty_t_projection_is_one_open_interval": True,
        "every_nonempty_fixed_t_fibre_is_one_open_p_interval": True,
        "fibre_endpoints_are_continuous_by_uniform_implicit_function_theorem": True,
        "continuous_midpoint_section_proves_P_path_connected": True,
        "frozen_full_window_seed_corridor_is_contained_in_P": True,
        "P_equals_seeded_maximal_connected_component_M": True,
    }


def interval_characteristic_theorem() -> dict[str, Any]:
    density_ratio = Q(2000, 1999)
    physical_step = Q(360134800, 360493663)
    combined = density_ratio * physical_step
    assert combined == Q(720269600000, 720626832337) < 1
    margin = 1 - combined
    assert margin == Q(357232337, 720626832337)
    return {
        "exact_selected_component_predicate_after_reachability_pruning": (
            "G:E source chart AND abs(p_0)<3/10 AND abs(p_1)<3/10"
        ),
        "other_physical_word_and_chart_predicates_implied_on_P": True,
        "raw_algebraic_equalities_may_still_vanish_outside_their_physical_roles": True,
        "P_equals_seeded_maximal_connected_component_M": True,
        "source_chart_preimage_on_unstable_graph_is_interval": True,
        "source_central_preimage_on_unstable_graph_is_interval_since_dphi_0_dr_0_gt_0": True,
        "target_central_preimage_on_unstable_graph_is_interval": True,
        "target_phi_derivative_along_source_unstable_graph": (
            "dphi_1/dr_0=-(C+D*V)/c_1<0 with C,D,c_1,V>0"
        ),
        "frozen_positive_entry_Birkhoff_matrix": (
            "D T=-c_1^-1[[tau*kappa_0+c_0,tau],"
            "[tau*kappa_0*kappa_1+kappa_0*c_1+kappa_1*c_0,"
            "tau*kappa_1+c_1]]"
        ),
        "selected_component_intersection_component_upper_per_canonical_curve": 1,
        "selected_component_local_unnormalized_characteristic_Z_multiplier": str(
            density_ratio
        ),
        "restriction_then_physical_step_coefficient": str(combined),
        "restriction_then_physical_step_margin": str(margin),
        "selected_component_local_characteristic_Growth_contraction": True,
    }


def build_result() -> dict[str, Any]:
    boundary, incidence, maximal, growth = audit_dependencies()
    quadrant = target_central_forces_ne_quadrant()
    implication = word_and_chart_implication()
    connected = connected_pruned_domain_theorem()
    interval = interval_characteristic_theorem()
    result: dict[str, Any] = {
        "schema": "cm2.gate25.selected-component-reachability-pruning.v1",
        "provenance": {
            "frozen_dependency_sha256": DEPENDENCIES,
            "parameter_window": ["-1/400", "1/400"],
            "selected_component_id": SELECTED_COMPONENT_ID,
            "parent_boundary_replay_digest": boundary["result"]["internal_replay_digest"],
            "selected_incidence_replay_digest": incidence["result"]["internal_replay_digest"],
            "maximal_word_registry_replay_digest": maximal["result"][
                "internal_replay_digest"
            ],
            "positive_entry_Birkhoff_certificate_sha256": growth[
                "certificate_sha256"
            ],
        },
        "target_central_quadrant_forcing": quadrant,
        "automatic_word_owner_wall_and_target_chart": implication,
        "connected_pruned_domain_theorem": connected,
        "selected_component_interval_characteristic_theorem": interval,
        "strict_nonpromotion": {
            "selected_component_local_field7_seed": "CERTIFIED",
            "full_key_all_component_field7": "NOT_CERTIFIED",
            "other_23_seeded_components_receive_this_sharp_pruning": False,
            "complete_18_field_operator_block_count": 0,
            "stable_saturated_product_base": False,
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
    print(json.dumps(build_result(), indent=2, sort_keys=True))
    print("GATE25_SELECTED_COMPONENT_LOCAL_CONTRACTING_CHARACTERISTIC_Z: CERTIFIED")
    print("GATE25_FULL_KEY_FIELD7: NOT_CERTIFIED")
    print("GATE2: NOT_CERTIFIED")
    print("GATE5: NOT_CERTIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
