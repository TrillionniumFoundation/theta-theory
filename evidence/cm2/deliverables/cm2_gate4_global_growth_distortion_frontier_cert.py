#!/usr/bin/env python3
"""Global true-branch complexity and one-collision distortion leaves for Gate 4.

The certificate has three deliberately separate layers.

* The frozen horizon/owner registries give 76 possible target lifts from a
  gray source and 68 from a white source.  Each target has at most two signed
  tangency sheets.  Their exact source slope is strictly stable, whereas an
  admissible unstable curve has positive slope.  This gives a numerical
  all-table one-step true-singularity complexity bound.
* Differentiating the exact circular Birkhoff matrix gives explicit first and
  second derivative envelopes on every physical continuity branch.  The only
  singular factor is the target cosine c_1.
* For the already certified bidirectional carriers, |V'|<4949.  Substitution
  into the exact r-Jacobian produces an explicit homogeneous 1/3-log-
  distortion constant, including the central strip.

The resulting true-branch/homogeneity estimate is greater than one.  It is a
rigorous upper bound, not a Growth-Lemma contraction.  No value is assigned
to C_p, vartheta_p, C_fw, C_rev, or q.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


Q = Fraction
HERE = Path(__file__).resolve().parent

OWNER_MANIFEST = (
    HERE / "cm2-gate3-owner-voronoi-event-registry-manifest-2026-07-15.json"
)
FIRST_HIT_MANIFEST = (
    HERE / "cm2-gate3-first-hit-atlas-manifest-2026-07-15.json"
)
SLOPE_MANIFEST = (
    HERE / "cm2-gate45-all-row-oriented-slope-envelope-manifest-2026-07-15.json"
)
FINITE_S_MANIFEST = (
    HERE / "cm2-gate45-finite-s-common-mesh-recovery-manifest-2026-07-16.json"
)
CURVATURE_MANIFEST = (
    HERE / "cm2-gate45-curvature-log-density-cost-manifest-2026-07-16.json"
)
NUMERIC_GROWTH_MANIFEST = (
    HERE / "cm2-gate4-numeric-growth-leaves-frontier-manifest-2026-07-16.json"
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def load_dependencies() -> tuple[dict[str, Any], ...]:
    owner = json.loads(OWNER_MANIFEST.read_text(encoding="utf-8"))
    first_hit = json.loads(FIRST_HIT_MANIFEST.read_text(encoding="utf-8"))
    slope = json.loads(SLOPE_MANIFEST.read_text(encoding="utf-8"))
    finite_s = json.loads(FINITE_S_MANIFEST.read_text(encoding="utf-8"))
    curvature = json.loads(CURVATURE_MANIFEST.read_text(encoding="utf-8"))
    growth = json.loads(NUMERIC_GROWTH_MANIFEST.read_text(encoding="utf-8"))

    assert owner["scope"]["global_G_candidate_union"] == 76
    assert owner["scope"]["global_W_candidate_union"] == 68
    assert owner["scope"]["global_signed_tangency_sheets"] == 288
    assert owner["owner_partition"]["status"] == (
        "CERTIFIED_FINITE_BOOLEAN_SINGLE_OWNER_PARTITION"
    )
    assert first_hit["candidate_reduction"]["retained_pair_count"] == 448
    assert slope["result"]["exact_oriented_slope_bounds"][
        "exact_source_slope_formula"
    ] == "dphi_source/dr_source=-kappa_source-cp_source/ell_T"
    assert finite_s["result"]["uniform_horizon_penetration_audit"][
        "replayed_leaf_count"
    ] == 35024
    assert finite_s["result"]["finite_s_endpoint_collar_audit"][
        "endpoint_incidence_count"
    ] == 128
    assert curvature["verdict"]["bidirectional_carrier_C2_costs"] == "CERTIFIED"
    assert growth["verdict"]["numeric_single_true_branch_cut_sum"] == "CERTIFIED"
    return owner, first_hit, slope, finite_s, curvature, growth


def true_singularity_complexity(
    owner: dict[str, Any], first_hit: dict[str, Any], growth: dict[str, Any]
) -> dict[str, Any]:
    gray_targets = owner["scope"]["global_G_candidate_union"]
    white_targets = owner["scope"]["global_W_candidate_union"]
    gray_signed_sheets = 2 * gray_targets
    white_signed_sheets = 2 * white_targets
    total_signed_sheets = gray_signed_sheets + white_signed_sheets
    assert total_signed_sheets == owner["scope"]["global_signed_tangency_sheets"]

    # A target circle has two tangent orientations.  On either lifted sheet,
    # phi'_tan=-kappa_source-cp_source/ell_T<-25/9, while V_unstable>25/9.
    # Hence one unstable graph intersects each sheet at most once.
    maximum_intersections = max(gray_signed_sheets, white_signed_sheets)
    maximum_components = maximum_intersections + 1
    assert maximum_intersections == 152
    assert maximum_components == 153

    q_one_branch = Q(
        growth["replay_summary"]["single_branch_cut_sum"]
    )
    one_step_crude = maximum_components * q_one_branch
    assert q_one_branch == Q(900337, 901685)
    assert one_step_crude == Q(137751561, 901685) > 1

    return {
        "finite_horizon_target_registry": {
            "chart_target_pairs": first_hit["candidate_reduction"][
                "chart_target_pair_count"
            ],
            "retained_chart_target_pairs": first_hit["candidate_reduction"][
                "retained_pair_count"
            ],
            "global_gray_target_union": gray_targets,
            "global_white_target_union": white_targets,
            "signed_tangency_sheets_gray_source": gray_signed_sheets,
            "signed_tangency_sheets_white_source": white_signed_sheets,
            "global_signed_tangency_sheets": total_signed_sheets,
        },
        "sheet_curve_transversality": {
            "tangent_sheet_slope": (
                "dphi_tan/dr=-kappa_source-cp_source/ell_T<-25/9"
            ),
            "unstable_curve_slope": "V>25/9",
            "one_unstable_graph_intersects_one_signed_sheet_at_most_once": True,
        },
        "one_step_true_singularity_intersection_upper": maximum_intersections,
        "one_step_true_continuity_component_upper": maximum_components,
        "n_step_true_component_crude_upper": "153^n",
        "one_true_branch_homogeneity_cut_sum_strict_upper": str(q_one_branch),
        "crude_global_one_step_Xi_upper": str(one_step_crude),
        "crude_iterated_Xi_upper": (
            "(137751561/901685)^n, before any sharper weighted multiplicity gain"
        ),
        "crude_bound_is_a_contraction": False,
        "numeric_true_branch_complexity_leaf": "CERTIFIED",
        "numeric_global_Growth_contraction": "NOT_CERTIFIED",
    }


def all_branch_birkhoff_derivatives() -> dict[str, Any]:
    # Uniform physical bounds on a constant configuration T_s.
    kappa = Q(25, 4)
    tau = Q(3)
    a = tau * kappa + 1
    b = tau
    c = tau * kappa * kappa + 2 * kappa
    d = tau * kappa + 1
    assert (a, b, c, d) == (Q(79, 4), Q(3), Q(2075, 16), Q(79, 4))

    # From d tau = sin(phi_1) d r_1 - sin(phi_0) d r_0 and the first row
    # of the exact Birkhoff matrix.
    tau_r = Q(21)
    tau_phi = Q(3)
    cp1_r = Q(130)
    cp1_phi = Q(20)

    # Derivatives of the four numerators M=(a,b;c,d), after absorbing one
    # factor c_1^-1 (c_1<=1).
    m_r = (
        kappa * tau_r,
        tau_r,
        kappa * kappa * tau_r + kappa * cp1_r,
        kappa * tau_r + cp1_r,
    )
    m_phi = (
        kappa * tau_phi + 1,
        tau_phi,
        kappa * kappa * tau_phi + kappa * cp1_phi + kappa,
        kappa * tau_phi + cp1_phi,
    )
    assert m_r == (Q(525, 4), Q(21), Q(26125, 16), Q(1045, 4))
    assert m_phi == (Q(79, 4), Q(3), Q(3975, 16), Q(155, 4))

    numerators = (a, b, c, d)
    h_r = tuple(x + cp1_r * y for x, y in zip(m_r, numerators))
    h_phi = tuple(x + cp1_phi * y for x, y in zip(m_phi, numerators))
    assert h_r == (Q(10795, 4), Q(411), Q(295875, 16), Q(11315, 4))
    assert h_phi == (Q(1659, 4), Q(63), Q(45475, 16), Q(1735, 4))
    assert max(h_r) < 18493
    assert max(h_phi) < 2843
    tensor_infinity = 2 * 18493 + 2 * 2843
    assert tensor_infinity == 42672

    return {
        "exact_matrix": (
            "D T=-c_1^-1[[tau*kappa_0+c_0,tau],"
            "[tau*kappa_0*kappa_1+kappa_0*c_1+kappa_1*c_0,"
            "tau*kappa_1+c_1]]"
        ),
        "uniform_matrix_numerator_entry_uppers": [
            str(a), str(b), str(c), str(d)
        ],
        "flight_derivative_bounds": {
            "abs(partial_r tau)": "<21/c_1",
            "abs(partial_phi tau)": "<3/c_1",
        },
        "target_cosine_derivative_bounds": {
            "abs(partial_r c_1)": "<130/c_1",
            "abs(partial_phi c_1)": "<20/c_1",
        },
        "matrix_r_derivative_coefficients": [str(x) for x in h_r],
        "matrix_phi_derivative_coefficients": [str(x) for x in h_phi],
        "coordinate_second_derivative_envelope": {
            "r_differentiated_entries": "<18493/c_1^3",
            "phi_differentiated_entries": "<2843/c_1^3",
            "D2T_coordinate_infinity_operator": "<42672/c_1^3",
        },
        "validity": (
            "every physical continuity branch of every T_s, |s|<=1/400; "
            "all such branches lie in the finite retained target universe"
        ),
        "all_physical_branch_D2T_grazing_weight_leaf": "CERTIFIED",
    }


def homogeneous_log_jacobian_distortion() -> dict[str, Any]:
    k0 = 41
    tau_min = Q(36337, 800000)
    kappa_min = Q(25, 9)
    expansion_numerator_lower = 2 * kappa_min * tau_min
    assert expansion_numerator_lower == Q(36337, 144000)

    slope_upper = Q(29)
    curvature_upper = Q(4949)
    # A=tau*(kappa_0+V)+c_0.  Along a carrier parameterised by source r:
    # |tau'|<108/c_1, kappa_0+V<=141/4, tau<=3, |c_0'|<=29.
    tau_curve_coefficient = 21 + 3 * slope_upper
    assert tau_curve_coefficient == 108
    first_term = tau_curve_coefficient * Q(141, 4)
    regular_terms = 3 * curvature_upper + slope_upper
    a_prime_coefficient = first_term + regular_terms
    assert a_prime_coefficient == 18683
    cp1_curve_coefficient = 130 + 20 * slope_upper
    assert cp1_curve_coefficient == 710
    log_r_jacobian_coefficient = (
        a_prime_coefficient / expansion_numerator_lower
        + cp1_curve_coefficient
    )
    assert log_r_jacobian_coefficient == Q(388021610, 5191) < 74750

    # High strips: c_1>1/(2(k+1)^2), c_1<k^-2 and
    # |Delta r_1| <= [k^-2-(k+1)^-2]/kappa_min.  Cubing removes the only
    # fractional exponent.  For k>=41, (k+1)/k<=42/41 and
    # (2k+1)/k<=83/41, so the k=41 expression is a uniform rational upper.
    high_candidate = Q(1024000)
    high_width = Q(9, 25) * Q(
        2 * k0 + 1, k0 * k0 * (k0 + 1) * (k0 + 1)
    )
    high_linear = (
        4
        * Q(74750)
        * Q((k0 + 1) ** 4, k0 * k0)
        / expansion_numerator_lower
    )
    assert high_candidate**3 > high_linear**3 * high_width**2

    circumference = Q(396, 175)
    central_linear = (
        Q(74750)
        * 4
        * k0**4
        / expansion_numerator_lower
    )
    central_candidate = Q(6_000_000_000_000)
    assert central_candidate**3 > central_linear**3 * circumference**2

    # Keep the conditional formula explicit for any future invariant
    # standard-curve curvature ceiling D_std.
    conditional_constant = (
        "C_log(D)=710+(3836+3*D)*(144000/36337), "
        "so abs(d_r log|r_1,W'|)<C_log(D)/c_1^2"
    )
    return {
        "carrier_class": {
            "oriented_view_count": 128,
            "slope_interval": "25/9<V<29 after the certified orientation",
            "graph_curvature_strict_upper": "4949",
        },
        "exact_r_jacobian": (
            "abs(r_1,W')=[tau*(kappa_0+V)+c_0]/c_1"
        ),
        "r_jacobian_numerator_strict_lower": str(expansion_numerator_lower),
        "log_r_jacobian_derivative_exact_coefficient_upper": str(
            log_r_jacobian_coefficient
        ),
        "log_r_jacobian_derivative_round_upper": (
            "abs(d_r log|r_1,W'|)<74750/c_1^2"
        ),
        "conditional_standard_curve_formula": conditional_constant,
        "high_strip_geometry": {
            "strip_index": "k>=41",
            "target_cosine_bounds": "1/(2(k+1)^2)<c_1<k^-2",
            "target_r_projection_length_upper": (
                "(9/25)*(2k+1)/(k^2*(k+1)^2)"
            ),
            "uniform_one_third_log_distortion_constant": str(high_candidate),
        },
        "central_strip_geometry": {
            "target_cosine_lower": "c_1>1/(2*41^2)",
            "target_boundary_r_length_upper": str(circumference),
            "one_third_log_distortion_constant": str(central_candidate),
        },
        "all_homogeneous_oriented_carrier_one_step_distortion": (
            "abs(log(J(x)/J(y)))<6000000000000*abs(r_1(x)-r_1(y))^(1/3)"
        ),
        "all_128_oriented_carrier_log_r_jacobian_distortion_leaf": "CERTIFIED",
        "arbitrary_iterated_standard_curve_distortion_leaf": "NOT_CERTIFIED",
    }


def exact_frontier() -> dict[str, Any]:
    return {
        "new_numeric_leaves": [
            "global one-step true-singularity intersection bound 152 and component bound 153",
            "all-physical-branch D2T coordinate envelope 42672/c_1^3",
            "all 128 oriented carriers: one-step homogeneous log-r-Jacobian 1/3 distortion",
            "conditional explicit C_log(D) for a future invariant standard-curve curvature ceiling",
        ],
        "minimal_missing_growth_leaves": [
            "a weighted true-singularity ledger sharper than the 153-component count",
            "an executable n-step delta_n/root-separation ledger through finite s",
            "a numerical invariant curvature ceiling D_std for every iterated standard curve",
            "the resulting global theta_*<1 and regular-density recovery constants",
        ],
        "why_the_new_complexity_does_not_close_growth": (
            "153*(900337/901685)=137751561/901685>1; finite branch count "
            "without physical contraction weights is far too coarse"
        ),
        "numeric_global_theta_star": False,
        "numeric_delta_n": False,
        "numeric_C_p_vartheta_p": False,
        "complete_numeric_C_fw_C_rev_q": False,
        "gate4_certified": False,
    }


def certify() -> dict[str, Any]:
    owner, first_hit, slope, finite_s, curvature, growth = load_dependencies()
    complexity = true_singularity_complexity(owner, first_hit, growth)
    derivatives = all_branch_birkhoff_derivatives()
    distortion = homogeneous_log_jacobian_distortion()
    frontier = exact_frontier()
    assert finite_s["result"]["scope_limits"][
        "uniform_one_collision_geometric_cost_coefficients"
    ] is True
    assert curvature["result"]["curvature_log_density_and_partial_cost"][
        "bidirectional_carrier_C2_bounds"
    ]["miss_forward_curvature_strict_upper"] == "4949"
    assert slope["result"]["exact_oriented_slope_bounds"][
        "common_broad_oriented_slope_envelope"
    ] == "29"
    return {
        "schema": "cm2.gate4.global-growth-distortion-frontier.v1",
        "provenance": {
            "owner_registry_manifest": OWNER_MANIFEST.name,
            "first_hit_manifest": FIRST_HIT_MANIFEST.name,
            "oriented_slope_manifest": SLOPE_MANIFEST.name,
            "finite_s_common_mesh_manifest": FINITE_S_MANIFEST.name,
            "carrier_curvature_manifest": CURVATURE_MANIFEST.name,
            "numeric_growth_leaves_manifest": NUMERIC_GROWTH_MANIFEST.name,
            "parameter_window": "|s|<=1/400",
            "map_scope": "constant fixed-configuration maps T_s=F_(K_s,K_s)",
        },
        "true_singularity_complexity": complexity,
        "all_branch_birkhoff_second_derivatives": derivatives,
        "homogeneous_oriented_carrier_log_distortion": distortion,
        "exact_growth_frontier": frontier,
        "scope_limits": {
            "numeric_true_singularity_complexity": True,
            "numeric_all_physical_branch_D2T_weight": True,
            "numeric_all_oriented_carrier_one_step_log_r_jacobian_distortion": True,
            "numeric_arbitrary_iterated_standard_curve_distortion": False,
            "numeric_delta_n": False,
            "numeric_global_Growth_contraction": False,
            "numeric_C_p_vartheta_p": False,
            "complete_numeric_C_fw_C_rev_q": False,
            "gate4_certified": False,
        },
    }


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE4_NUMERIC_TRUE_SINGULARITY_COMPLEXITY: CERTIFIED")
    print("GATE4_ALL_PHYSICAL_BRANCH_D2T_WEIGHT: CERTIFIED")
    print("GATE4_ORIENTED_CARRIER_ONE_STEP_LOG_R_JACOBIAN_DISTORTION: CERTIFIED")
    print("GATE4_GLOBAL_GROWTH_CONTRACTION: NOT_CERTIFIED")
    print("GATE4_NUMERIC_C_P_VARTTHETA_P_AND_Q: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
