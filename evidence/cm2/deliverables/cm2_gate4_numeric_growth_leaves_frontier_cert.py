#!/usr/bin/env python3
"""Numeric Growth-Lemma leaves for the finite-s Gate-4 configuration class.

The certificate extracts every constant that follows directly from the
already certified collision matrix, invariant slope cone, curvature range,
flight gap, circular geometry, and homogeneity-strip definition.  In
particular it gives an explicit adapted-metric expansion, metric equivalence,
Euclidean hyperbolicity constants, a separation-time metric constant, and a
one-true-branch homogeneity-cut sum strictly below one.

It deliberately does not identify that local sum with the global Growth
Lemma coefficient.  The physical true-singularity weighted multiplicity,
the n-step small-curve thresholds delta_n, and a second-derivative distortion
ledger are absent.  Exact countermodels show that neither branch sums nor
distortion constants follow from expansion/cone data alone.
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
CONE_MANIFEST = (
    HERE / "cm2-gate45-global-invariant-cone-manifest-2026-07-16.json"
)
CURVATURE_MANIFEST = (
    HERE / "cm2-gate45-curvature-log-density-cost-manifest-2026-07-16.json"
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def load_dependencies() -> tuple[dict[str, Any], ...]:
    finite_s = json.loads(FINITE_S_MANIFEST.read_text(encoding="utf-8"))
    cone = json.loads(CONE_MANIFEST.read_text(encoding="utf-8"))
    curvature = json.loads(CURVATURE_MANIFEST.read_text(encoding="utf-8"))
    assert finite_s["verdict"]["finite_s_common_endpoint_mesh"] == "CERTIFIED"
    assert finite_s["result"]["uniform_configuration_and_recovery"][
        "compact_configuration_path"
    ]["one_compact_SYZ_configuration_class"] is True
    assert cone["result"]["scope_limits"][
        "fixed_global_geometric_unstable_cone"
    ] is True
    assert curvature["verdict"]["bidirectional_carrier_C2_costs"] == "CERTIFIED"
    return finite_s, cone, curvature


def adapted_metric_numeric_leaves() -> dict[str, Any]:
    kappa_min = Q(25, 9)
    kappa_max = Q(25, 4)
    tau_min = Q(36337, 800000)
    slope_upper = Q(4108425, 145348)
    assert slope_upper < 29

    # For the adapted p-metric used in Canestrari (6.11),
    # N_*(dr,dphi)=(kappa+V)|dr| when V=dphi/dr.
    # The frozen Birkhoff matrix gives the exact expansion identity below.
    tau = Q(7, 10)
    kappa_0 = Q(25, 9)
    kappa_1 = Q(25, 4)
    cp_0 = Q(3, 5)
    cp_1 = Q(4, 5)
    slope_0 = Q(5)
    a = kappa_0 + slope_0
    dr_ratio = (tau * a + cp_0) / cp_1
    slope_1 = kappa_1 + cp_1 * a / (tau * a + cp_0)
    metric_ratio = (kappa_1 + slope_1) * dr_ratio / a
    metric_ratio_formula = 1 + 2 * kappa_1 * (tau + cp_0 / a) / cp_1
    assert metric_ratio == metric_ratio_formula

    p_expansion = 1 + 2 * kappa_min * tau_min
    assert p_expansion == Q(180337, 144000)
    p_inverse_contraction = 1 / p_expansion
    metric_lower = Q(5, 27)
    metric_upper = Q(141, 4)
    common_metric_equivalence = metric_upper
    assert 1 / metric_lower < common_metric_equivalence
    euclidean_prefactor = metric_lower / metric_upper
    assert euclidean_prefactor == Q(20, 3807)

    # A regular unstable curve is a graph over one circular boundary.  The
    # largest radius is at most 9/25 and pi<22/7.  Since |V|<29, its arclength
    # projection factor is <30.
    boundary_circumference_upper = Q(396, 175)
    carrier_length_upper = 30 * boundary_circumference_upper
    assert carrier_length_upper == Q(2376, 35) < 68
    separation_metric_constant = 68 * p_expansion / euclidean_prefactor
    assert separation_metric_constant == Q(1296803367, 80000)
    return {
        "adapted_metric": (
            "N_*(dr,dphi)=(kappa+V)*abs(dr), V=dphi/dr"
        ),
        "exact_one_collision_expansion_identity": (
            "N_1/N_0=1+(2*kappa_1/cp_1)*(tau+cp_0/(kappa_0+V_0))"
        ),
        "identity_matches_frozen_Birkhoff_matrix": True,
        "uniform_adapted_expansion_strict_lower": str(p_expansion),
        "uniform_adapted_inverse_contraction_strict_upper": str(
            p_inverse_contraction
        ),
        "metric_equivalence": (
            "(5/27)*norm_2 < N_* < (141/4)*norm_2 on the invariant cone"
        ),
        "safe_common_C_metric": str(common_metric_equivalence),
        "carrier_projection_constant_C_cone": "30",
        "Euclidean_hyperbolicity": (
            "norm(D F^n v)_2 > (20/3807)*(180337/144000)^n*norm(v)_2"
        ),
        "explicit_c_hat": str(euclidean_prefactor),
        "explicit_Lambda": str(p_expansion),
        "maximum_circular_boundary_circumference_upper": str(
            boundary_circumference_upper
        ),
        "maximum_homogeneous_unstable_curve_length_strict_upper": "68",
        "explicit_separation_metric_C_s": str(separation_metric_constant),
        "numeric_SYZ_Lemma_6_cone_hyperbolicity_leaf": "CERTIFIED",
        "numeric_C_metric_C_cone_L0_C_s_leaves": "CERTIFIED",
    }


def single_true_branch_homogeneity_sum() -> dict[str, Any]:
    theta = Q(144000, 180337)
    k0 = 41
    tail = Q(8, k0 - 1)
    total = theta + tail
    assert tail == Q(1, 5)
    assert total == Q(900337, 901685) < 1
    margin = 1 - total
    assert margin == Q(1348, 901685)
    return {
        "homogeneity_strips": (
            "H_+/-k have cp=cos(phi)<k^-2 for every k>=k0"
        ),
        "high_strip_inverse_contraction": (
            "norm(D F^-1)_* < cp/(2*kappa_min*tau_min) < 4*k^-2"
        ),
        "one_connected_true_branch_crosses_each_horizontal_strip_at_most_once": True,
        "two_sided_high_strip_tail": (
            "sum_(sign=+/-) sum_(k>=k0) 4*k^-2 < 8/(k0-1)"
        ),
        "declared_cut_sum_k0": k0,
        "central_component_contraction_upper": str(theta),
        "two_sided_tail_upper": str(tail),
        "single_true_branch_one_step_cut_sum_strict_upper": str(total),
        "single_true_branch_contraction_margin": str(margin),
        "single_true_branch_one_step_expansion_sum": "CERTIFIED",
        "k0_41_compatibility_with_full_distortion_regular_atlas": False,
        "full_true_singularity_weighted_sum": False,
        "global_Growth_Lemma_contraction": False,
    }


def branch_multiplicity_countermodel() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    theta = Q(144000, 180337)
    rows = []
    for branches in (1, 2, 4, 8, 16, 32, 76):
        inverse_sum = branches * theta
        rows.append({
            "affine_branch_count_M": branches,
            "one_branch_inverse_contraction": str(theta),
            "total_inverse_branch_sum": str(inverse_sum),
            "sum_is_below_one": inverse_sum < 1,
        })
    assert rows[0]["sum_is_below_one"] is True
    assert all(row["sum_is_below_one"] is False for row in rows[1:])
    return rows, {
        "countermodel": (
            "M disjoint affine continuity branches can all have the same certified "
            "pointwise expansion while their inverse-branch sum is M*theta"
        ),
        "pointwise_expansion_determines_weighted_cut_sum": False,
        "first_failing_branch_count": 2,
        "required_physical_leaf": (
            "Xi_n(delta)=sup_(abs(W)<=delta) sum_j inf_(W_n,j) "
            "norm(D F^-n)_* with every true singularity and homogeneity cut registered"
        ),
        "rows_sha256": canonical_digest(rows),
    }


def distortion_countermodel() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = []
    for frequency in (1, 2, 4, 8, 16, 32, 64, 128):
        # f_N(x)=2x+(2N)^-1 sin(Nx).  Then f'_N in [3/2,5/2],
        # but at x=pi/(2N), |(log f'_N)'|=N/4.
        rows.append({
            "frequency_N": frequency,
            "uniform_derivative_interval": ["3/2", "5/2"],
            "log_derivative_at_pi_over_2N": str(Q(frequency, 4)),
        })
    return rows, {
        "countermodel_family": "f_N(x)=2x+(1/(2N))*sin(Nx)",
        "uniform_pointwise_expansion_lower": "3/2",
        "uniform_pointwise_derivative_upper": "5/2",
        "log_Jacobian_derivative": (
            "at x=pi/(2N), abs((log f_N')')=N/4 -> infinity"
        ),
        "cone_and_first_derivative_bounds_determine_distortion": False,
        "existing_carrier_C2_bound_is_not_a_D2F_distortion_bound": True,
        "required_physical_leaf": (
            "an all-homogeneity-branch D2F/log-Jacobian oscillation ledger, "
            "including grazing weights"
        ),
        "rows_sha256": canonical_digest(rows),
    }


def exact_growth_dependency_frontier() -> dict[str, Any]:
    return {
        "numeric_leaves_now_closed": [
            "adapted p-metric one-collision expansion",
            "two-sided p-metric/Euclidean equivalence",
            "Euclidean c_hat and Lambda on the invariant cone",
            "C_metric, C_cone, maximum curve length and separation C_s",
            "high-homogeneity-strip inverse-contraction tail",
            "one-continuity-branch one-step expansion/cut sum below one",
        ],
        "minimal_undetermined_growth_leaves": [
            "one numerical homogeneity cutoff simultaneously valid for the distortion/regularity lemmas",
            "the full physical true-singularity weighted branch sum Xi_n(delta)",
            "an explicit n-step small-curve threshold delta_n and complexity recurrence",
            "numeric D2F/log-Jacobian distortion constants C_d0,C_d",
            "the resulting regular-density constant C_r",
        ],
        "why_C_p_vartheta_p_still_do_not_follow": (
            "Lemma 16 needs the global Growth contraction and regular-density ratio; "
            "the certified local branch sum and pointwise hyperbolicity do not supply either"
        ),
        "numeric_C_gr_vartheta_gr": False,
        "numeric_C_p_vartheta_p": False,
        "numeric_A0_A1": False,
        "complete_propagated_numeric_C_fw_C_rev_q": False,
        "gate4_certified": False,
    }


def certify() -> dict[str, Any]:
    finite_s, cone, curvature = load_dependencies()
    leaves = adapted_metric_numeric_leaves()
    local_sum = single_true_branch_homogeneity_sum()
    branch_rows, branch_countermodel = branch_multiplicity_countermodel()
    distortion_rows, distortion = distortion_countermodel()
    frontier = exact_growth_dependency_frontier()
    assert cone["result"]["global_invariant_geometric_cone"]["cone_upper"] == (
        "4108425/145348"
    )
    assert finite_s["result"]["uniform_configuration_and_recovery"][
        "compact_configuration_path"
    ]["uniform_minimum_free_flight_strict_lower"] == "36337/800000"
    assert curvature["result"]["scope_limits"][
        "all_row_bidirectional_carrier_C2_bounds"
    ] is True
    return {
        "schema": "cm2.gate4.numeric-growth-leaves-frontier.v1",
        "provenance": {
            "finite_s_common_mesh_recovery_manifest": FINITE_S_MANIFEST.name,
            "global_invariant_cone_manifest": CONE_MANIFEST.name,
            "curvature_log_density_manifest": CURVATURE_MANIFEST.name,
            "parameter_window": "|s|<=1/400",
            "map_scope": "constant fixed-configuration maps T_s=F_(K_s,K_s)",
        },
        "adapted_metric_numeric_leaves": leaves,
        "single_true_branch_homogeneity_expansion_sum": local_sum,
        "branch_multiplicity_nonimplication": branch_countermodel,
        "distortion_nonimplication": distortion,
        "exact_growth_dependency_frontier": frontier,
        "scope_limits": {
            "numeric_adapted_metric_expansion": True,
            "numeric_metric_equivalence_and_Euclidean_hyperbolicity": True,
            "numeric_C_metric_C_cone_L0_C_s": True,
            "numeric_single_true_branch_homogeneity_cut_sum": True,
            "numeric_full_true_singularity_weighted_sum": False,
            "numeric_n_step_delta_n": False,
            "numeric_distortion_constants": False,
            "numeric_C_gr_vartheta_gr": False,
            "numeric_C_p_vartheta_p": False,
            "complete_propagated_numeric_C_fw_C_rev_q": False,
            "gate4_certified": False,
        },
        "internal_replay_digests": {
            "branch_countermodel_rows": canonical_digest(branch_rows),
            "distortion_countermodel_rows": canonical_digest(distortion_rows),
        },
    }


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE4_NUMERIC_ADAPTED_METRIC_HYPERBOLICITY_LEAVES: CERTIFIED")
    print("GATE4_NUMERIC_SINGLE_TRUE_BRANCH_CUT_SUM: CERTIFIED")
    print("GATE4_NUMERIC_GLOBAL_GROWTH_CONSTANTS: NOT_CERTIFIED")
    print("GATE4_NUMERIC_C_P_VARTTHETA_P_AND_PROPAGATED_Q: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
