#!/usr/bin/env python3
"""Numeric invariant-family/Growth/recovery frontier for CM2 Gate 4.

This certificate starts from the already frozen componentwise one-step
weighted contraction.  It supplies the missing curvature layer by using the
exact graph-transform recurrence, not the grazing-singular coordinate D2T
envelope.  Four phase-typed curvature ceilings cover every iterate.  They in
turn give an invariant adapted-density cone and a fully numerical Growth
recurrence.

The certificate also aggregates the native physical prefix antichain by its
unnormalised shell masses.  It never charges a leaf by the inverse of its
mass.  The resulting levelwise recovery-clock moment is finite, but the
recordwise strong-operator costs and final same-occurrence q are deliberately
left open.
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
    "cm2-gate4-componentwise-global-growth-recovery-frontier-manifest-2026-07-16.json": (
        "34ff376dafa9f95f7b03df661655240657b114ffc4e1bc20fca036c84f1dd691"
    ),
    "cm2-gate4-global-growth-distortion-frontier-manifest-2026-07-16.json": (
        "ee1ac2acb72af04ac254e2f0a33981df478b022cde0dc08f9988762ff1c8bcc9"
    ),
    "cm2-gate4-numeric-growth-leaves-frontier-manifest-2026-07-16.json": (
        "4e0c8216892afe9ce0c19e22b9ecc5742f21e9e4512d949b88325e1ee1ff70d5"
    ),
    "cm2-gate45-global-invariant-cone-manifest-2026-07-16.json": (
        "173949cb9cde01ae1326576c2a9a48b268a80bce2e48954a49efa46ccd9759f9"
    ),
    "cm2-gate45-finite-s-common-mesh-recovery-manifest-2026-07-16.json": (
        "098f9f52580fbb71d2416b07330aefa4f67488115f000bb60d37eec521250625"
    ),
    "cm2-gate45-curvature-log-density-cost-manifest-2026-07-16.json": (
        "b38772a41d0b610e1e1cd4fb4509cfb76227cc8f4983af0699d2cf38e60650c5"
    ),
    "cm2-gate4-native-stopping-repeated-recovery-frontier-manifest-2026-07-16.json": (
        "20f595ed4bcf62cb5cc5c89c22ab31a3ca039f43fff29fd35855673dc970b4a2"
    ),
    "cm2-gate4-finite-cemetery-resolution-tradeoff-manifest-2026-07-16.json": (
        "f9b12df851f9cfd5115c7810ec37349583e4a53ef9e312447b647cc3ae21b30d"
    ),
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_dependencies() -> dict[str, dict[str, Any]]:
    data: dict[str, dict[str, Any]] = {}
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        assert path.is_file()
        assert sha256_path(path) == expected
        data[name] = json.loads(path.read_text(encoding="utf-8"))

    componentwise = data[
        "cm2-gate4-componentwise-global-growth-recovery-frontier-manifest-2026-07-16.json"
    ]
    global_growth = data[
        "cm2-gate4-global-growth-distortion-frontier-manifest-2026-07-16.json"
    ]
    numeric = data[
        "cm2-gate4-numeric-growth-leaves-frontier-manifest-2026-07-16.json"
    ]
    cone = data[
        "cm2-gate45-global-invariant-cone-manifest-2026-07-16.json"
    ]
    finite_s = data[
        "cm2-gate45-finite-s-common-mesh-recovery-manifest-2026-07-16.json"
    ]
    native = data[
        "cm2-gate4-native-stopping-repeated-recovery-frontier-manifest-2026-07-16.json"
    ]
    cemetery = data[
        "cm2-gate4-finite-cemetery-resolution-tradeoff-manifest-2026-07-16.json"
    ]

    assert componentwise["replay_summary"][
        "global_one_step_Xi_strict_upper"
    ] == "900337/901685"
    assert componentwise["replay_summary"]["delta_1"] == (
        "1/37724355673552103994"
    )
    assert global_growth["replay_summary"]["D2T_coordinate_infinity_operator"] == (
        "<42672/c_1^3"
    )
    assert numeric["replay_summary"]["inverse_contraction"] == (
        "144000/180337"
    )
    assert cone["result"]["global_invariant_geometric_cone"][
        "fixed_geometric_unstable_cone"
    ] == "25/9<V=dphi/dr<4108425/145348<29"
    assert finite_s["result"]["finite_s_density_mesh_and_numeric_C_mesh"][
        "explicit_initial_C_mesh"
    ] == "69986663973833932800"
    assert native["replay_summary"]["native_leaf_depth"] == "D_K=3K+2"
    assert cemetery["replay_summary"][
        "unnormalized_reweighted_escape_refuted"
    ] is False
    return data


def phase_typed_curvature_family() -> dict[str, Any]:
    # Uniform billiard geometry.
    tau_min = Q(36337, 800000)
    kappa_min = Q(25, 9)
    slope_min = Q(25, 9)
    slope_max = Q(29)
    b_min = kappa_min + slope_min
    expansion_numerator = b_min * tau_min
    assert b_min == Q(50, 9)
    assert expansion_numerator == Q(36337, 144000) > Q(1, 4)
    assert tau_min > Q(9, 200)
    assert b_min > 5

    # For B=kappa_0+V_0, h=tau+c_0/B and A=B*h, the exact recurrence is
    # V_1=kappa_1+c_1/h and |dr_1/dr_0|=A/c_1.  Differentiating and using
    # |tau'_W|<108/c_1 gives D_1<A_bar+b(c_0,c_1)D_0.
    inhomogeneous_exact_upper = (
        slope_max / Q(9, 200)
        + Q(108) / (5 * Q(9, 200) ** 3)
        + slope_max / (25 * Q(9, 200) ** 3)
    )
    assert inhomogeneous_exact_upper == Q(182549800, 729)
    inhomogeneous_round_upper = Q(251000)
    assert inhomogeneous_exact_upper < inhomogeneous_round_upper

    # b_j=c_j*c_(j+1)^2/A_j^3.  The endpoint maximum is bounded by
    # 4/(27*a^2)<64/27<12/5 for a>1/4.  Every internal cosine contributes
    # [c/(a+c)]^3<(4/5)^3=64/125.
    endpoint_beta = Q(12, 5)
    internal_q = Q(64, 125)
    four_step_product = endpoint_beta * internal_q**3
    assert four_step_product == Q(3145728, 9765625) < 1
    four_step_suffix_sum = 1 + endpoint_beta * (
        1 + internal_q + internal_q**2
    )
    assert four_step_suffix_sum == Q(410777, 78125)

    phase_ceilings = [Q(2_000_000)]
    for _ in range(3):
        phase_ceilings.append(
            inhomogeneous_round_upper + endpoint_beta * phase_ceilings[-1]
        )
    assert phase_ceilings == [
        Q(2_000_000),
        Q(5_051_000),
        Q(12_373_400),
        Q(29_947_160),
    ]
    phase_four_return = (
        inhomogeneous_round_upper * four_step_suffix_sum
        + four_step_product * phase_ceilings[0]
    )
    assert phase_four_return == Q(49099736, 25) < phase_ceilings[0]
    global_ceiling = Q(30_000_000)
    assert max(phase_ceilings) < global_ceiling
    assert Q(4949) < phase_ceilings[0]

    return {
        "exact_graph_transform": {
            "definitions": (
                "B=kappa_0+V_0; h=tau+c_0/B; A=B*h; "
                "abs(dr_1/dr_0)=A/c_1; V_1=kappa_1+c_1/h"
            ),
            "curvature_recurrence": (
                "D_1<251000+b(c_0,c_1)D_0, "
                "b=c_0*c_1^2/(tau*(kappa_0+V_0)+c_0)^3"
            ),
            "inhomogeneous_exact_upper": str(inhomogeneous_exact_upper),
            "inhomogeneous_round_upper": str(inhomogeneous_round_upper),
            "why_coordinate_D2T_is_not_used": (
                "the determinant/graph recurrence keeps the endpoint cosines "
                "that cancel the grazing blow-up"
            ),
        },
        "correlated_curvature_products": {
            "expansion_numerator_strict_lower": str(expansion_numerator),
            "endpoint_factor_strict_upper": str(endpoint_beta),
            "internal_factor_strict_upper": str(internal_q),
            "n_step_D0_coefficient_strict_upper": (
                "(12/5)*(64/125)^(n-1)"
            ),
            "four_step_D0_coefficient_strict_upper": str(four_step_product),
            "four_step_suffix_sum": str(four_step_suffix_sum),
        },
        "four_phase_invariant_family": {
            "phase_curvature_ceilings": [str(x) for x in phase_ceilings],
            "phase_3_actual_upper": str(phase_ceilings[3]),
            "four_step_return_strict_upper": str(phase_four_return),
            "phase_zero_ceiling": str(phase_ceilings[0]),
            "global_D_std_strict_upper": str(global_ceiling),
            "cuts_preserve_phase_and_do_not_change_graph_curvature": True,
            "initial_128_carriers_fit_phase_zero": True,
            "every_iterated_homogeneous_standard_curve_covered": True,
            "numeric_phase_typed_curvature_invariance": "CERTIFIED",
        },
    }


def invariant_density_and_distortion() -> dict[str, Any]:
    D_std = Q(30_000_000)
    expansion_numerator = Q(36337, 144000)
    adapted_inverse = Q(144000, 180337)
    assert adapted_inverse < Q(93, 100) ** 3

    # This is the frozen conditional log-r-Jacobian formula with D=D_std.
    log_r_exact = Q(710) + (Q(3836) + 3 * D_std) / expansion_numerator
    assert log_r_exact == Q(12960578183270, 36337)
    log_r_round = Q(360_000_000)
    assert log_r_exact < log_r_round

    # Re-run the frozen homogeneous-strip cubed comparisons at k0=6121.
    k0 = 6121
    high_width = Q(9, 25) * Q(
        2 * k0 + 1, k0 * k0 * (k0 + 1) * (k0 + 1)
    )
    high_linear = (
        4 * log_r_round * Q((k0 + 1) ** 4, k0 * k0)
        / expansion_numerator
    )
    high_candidate = Q(5_000_000_000)
    assert high_candidate**3 > high_linear**3 * high_width**2

    circumference = Q(396, 175)
    central_linear = log_r_round * 4 * k0**4 / expansion_numerator
    central_candidate = Q(14_000_000_000_000_000_000_000_000)
    assert central_candidate**3 > central_linear**3 * circumference**2

    # Passing from the projected r-Jacobian to the adapted Jacobian adds
    # log(kappa+V) at source and target.  D_std/(2*kappa_min)=5.4e6;
    # the source/target coordinate comparison is <1269/200.  1.5e25 safely
    # dominates the r bound and both additions.
    log_u_derivative = D_std * Q(9, 50)
    assert log_u_derivative == Q(5_400_000)
    one_step_adapted_distortion = Q(15_000_000_000_000_000_000_000_000)
    assert one_step_adapted_distortion > central_candidate + Q(41_000_000)

    invariant_density_constant = Q(500_000_000_000_000_000_000_000_000)
    assert (
        Q(93, 100) * invariant_density_constant
        + one_step_adapted_distortion
        < invariant_density_constant
    )
    maximum_adapted_length = Q(1, 10**90)
    delta_1 = Q(1, 37724355673552103994)
    # Since dell_*=(kappa+V)|dr| and kappa+V>5, Euclidean graph length is
    # <(27/5)dell_*.  Thus every canonical standard curve is far shorter
    # than the delta_1 required by the componentwise Xi theorem.
    assert Q(27, 5) * maximum_adapted_length < delta_1
    log_density_oscillation = (
        invariant_density_constant * Q(1, 10**30)
    )
    assert log_density_oscillation == Q(1, 2000)
    density_ratio = Q(2000, 1999)
    # exp(x)<=1/(1-x), 0<=x<1.
    assert 1 / (1 - log_density_oscillation) == density_ratio

    return {
        "all_standard_curve_log_jacobian": {
            "conditional_log_r_formula": (
                "C_log(D)=710+(3836+3D)*(144000/36337)"
            ),
            "C_log_D_std_exact": str(log_r_exact),
            "C_log_D_std_round_upper": str(log_r_round),
            "homogeneity_cutoff_k0": k0,
            "high_strip_one_third_constant": str(high_candidate),
            "central_strip_one_third_constant": str(central_candidate),
            "adapted_one_step_one_third_constant": str(
                one_step_adapted_distortion
            ),
            "all_phase_typed_standard_curves": True,
            "numeric_all_iterated_standard_curve_distortion": "CERTIFIED",
        },
        "invariant_adapted_density_cone": {
            "adapted_line_element": (
                "dell_*=(kappa+V)*abs(dr), with "
                "(5/27)dell_E<dell_*<(141/4)dell_E"
            ),
            "density_regular_class": (
                "abs(log rho(x)-log rho(y))<="
                "5e26*ell_*(x,y)^(1/3)"
            ),
            "density_constant": str(invariant_density_constant),
            "inverse_contraction_cube_root_strict_upper": "93/100",
            "one_step_invariance_arithmetic": (
                "(93/100)*5e26+1.5e25=4.8e26<5e26"
            ),
            "canonical_maximum_adapted_curve_length": str(
                maximum_adapted_length
            ),
            "euclidean_length_strict_upper": "(27/5)*10^-90",
            "componentwise_Xi_short_curve_threshold_delta_1": str(delta_1),
            "every_canonical_curve_is_inside_delta_1_scope": True,
            "per_curve_log_density_oscillation_upper": str(
                log_density_oscillation
            ),
            "per_curve_density_ratio_upper": str(density_ratio),
            "numeric_regular_density_invariance": "CERTIFIED",
        },
    }


def numeric_growth_and_recovery() -> dict[str, Any]:
    xi = Q(900337, 901685)
    density_ratio = Q(2000, 1999)
    contraction = density_ratio * xi
    margin = 1 - contraction
    assert contraction == Q(360134800, 360493663) < 1
    assert margin == Q(358863, 360493663)

    delta_star = Q(1, 10**90)
    additive = 2 / delta_star
    assert additive == 2 * 10**90

    # Z_* is the weight divided by adapted length.  The artificial split of a
    # long child into equal pieces in [delta_*/2,delta_*] contributes at most
    # 2 mass/delta_*; true/homogeneity cuts are already in Xi.
    cp_adapted = 2 * additive / margin
    euclidean_metric_upper = Q(141, 4)
    cp_euclidean = euclidean_metric_upper * cp_adapted
    assert cp_adapted == Q(4 * 10**90 * 360493663, 358863)
    assert cp_euclidean == Q(141 * 10**90 * 360493663, 358863)

    recovery_block = 1005
    assert recovery_block * margin >= 1
    assert contraction**recovery_block <= Q(1, 2)
    c_mesh = 69986663973833932800
    assert c_mesh < 2**66
    # Initial canonical delta_* chopping adds at most 2/delta_*.
    # Convert the frozen Euclidean/projection boundary to Z_* with the safe
    # metric factor 27/5, then pay the first canonical delta_* chop.
    initial_chopped_constant = Q(27, 5) * c_mesh + additive
    assert initial_chopped_constant < 2**300
    recovery_A0 = recovery_block * 300
    recovery_A1 = recovery_block
    assert recovery_A0 == 301500
    assert recovery_A1 == 1005

    return {
        "adapted_boundary_Growth_recurrence": {
            "boundary_functional": "Z_*=sum_a p_a/ell_*(W_a)",
            "true_and_homogeneity_child_sum_strict_upper": str(xi),
            "regular_density_ratio_upper": str(density_ratio),
            "one_step_contraction_vartheta_p": str(contraction),
            "one_step_contraction_margin": str(margin),
            "canonical_artificial_chop_length_delta_star": str(delta_star),
            "additive_mass_coefficient": str(additive),
            "linear_recurrence": (
                "Z_*(T F)<=vartheta_p*Z_*(F)+2e90*mass(F)"
            ),
            "every_true_and_homogeneity_cut_counted_by_Xi_once": True,
            "artificial_max_length_chops_paid_only_by_additive_term": True,
            "artificial_chop_additive_is_once_on_total_long_child_mass": True,
            "numeric_linear_Growth_recurrence": "CERTIFIED",
        },
        "numeric_Growth_Lemma_constants": {
            "adapted_C_p": str(cp_adapted),
            "euclidean_C_p": str(cp_euclidean),
            "vartheta_p": str(contraction),
            "adapted_Growth_bound": (
                "Z_n^*/mass<=a^n Z_0^*/mass+(2e90)/(1-a)"
            ),
            "euclidean_SYZ_form": (
                "Z_n^E/mass<=(C_p/2)*(1+a^n Z_0^E/mass)"
            ),
            "numeric_C_p_vartheta_p": "CERTIFIED",
        },
        "numeric_recovery_clock": {
            "C_mesh": str(c_mesh),
            "initial_delta_star_chopped_Z_constant": str(
                initial_chopped_constant
            ),
            "initial_constant_power_two_upper": "2^300",
            "half_life_block": recovery_block,
            "A0": recovery_A0,
            "A1": recovery_A1,
            "recovery_target": (
                "a^R*(Z_0^*/mass)<1, hence Z_R^*<C_p^* and "
                "Z_R^E<C_p^E"
            ),
            "initial_to_clock_logic": (
                "Z_0^*/mass<(2e90+(27/5)C_mesh)*2^D<2^(D+300); "
                "a^1005<=1/2; therefore R(D)<=1005*(D+300)"
            ),
            "per_orientation_clock": "R(D)<=301500+1005*D",
            "numeric_A0_A1": "CERTIFIED",
        },
    }


def native_levelwise_recovery_frontier() -> dict[str, Any]:
    # Native prefix shell K has mass (3/4)4^-K and leaf depth D_K=3K+2.
    A0 = 301500
    A1 = 1005
    constant_two_orientation = 2 * (A0 + 2 * A1)
    slope_two_orientation = 2 * 3 * A1
    assert constant_two_orientation == 607020
    assert slope_two_orientation == 6030

    gamma = Q(1, 12060)
    assert gamma * slope_two_orientation == Q(1, 2)
    assert gamma * constant_two_orientation == Q(151, 3)
    # e<3 implies exp(1/2)<sqrt(3)<7/4 and exp(151/3)<3^51.
    ratio_upper = Q(7, 8)
    moment_upper = 2 * 3**52

    return {
        "native_prefix_levelwise_unnormalized_recovery": {
            "native_shell_mass": "w_K=(3/4)*4^-K",
            "native_leaf_depth": "D_K=3K+2",
            "orientation_shared_record": "(e,s,K,q,j)",
            "per_orientation_recovery": "R(D_K)<=303510+3015*K",
            "two_orientation_recovery": "R_fw+R_rev<=607020+6030*K",
            "certified_gamma": str(gamma),
            "payload_moment": (
                "sum_K w_K*2^K*exp(gamma*(R_fw+R_rev))"
            ),
            "geometric_ratio_strict_upper": str(ratio_upper),
            "payload_moment_strict_upper": str(moment_upper),
            "leafwise_inverse_mass_or_2_to_D_charge_used": False,
            "record_preserving_levelwise_unnormalized_recovery_moment": (
                "CERTIFIED"
            ),
        },
        "strict_remaining_native_boundary": {
            "single_global_native_partition_Z_is_finite": False,
            "reason": (
                "the countably infinite native leaf partition has infinite "
                "time-zero Z; recovery is certified levelwise and aggregated "
                "by shell mass, not as one initially finite-Z family"
            ),
            "recordwise_strong_operator_cost_aggregates_without_2_to_D": False,
            "query_independent_repeated_indicator_regularizer": False,
            "full_unnormalized_reweighted_native_recovery_contract": (
                "NOT_CERTIFIED"
            ),
        },
    }


def cost_and_q_frontier() -> dict[str, Any]:
    return {
        "newly_numeric_propagation_inputs": {
            "all_iterated_D_std": True,
            "all_iterated_adapted_distortion": True,
            "regular_density_cone": True,
            "linear_Growth_recurrence": True,
            "numeric_C_p_vartheta_p": True,
            "numeric_A0_A1": True,
            "native_levelwise_payload_recovery_moment": True,
        },
        "still_missing_before_C_fw_C_rev": [
            "an unnormalised recordwise strong-operator norm showing that each physical indicator/test cost aggregates with the shell mass and payload 2^K, rather than the forbidden leaf normalization 2^D_K",
            "a query-independent decomposition for every repeated physical indicator with a finite levelwise boundary numerator",
            "a forward/reverse same-occurrence propagation ledger carrying identical coefficient and restriction records through their possibly different recovery clocks",
            "the Gate-3 common branch-record MT_DQ interface needed to identify the recovered operator factors with the physical current",
        ],
        "numeric_C_fw": False,
        "numeric_C_rev": False,
        "final_same_occurrence_q": False,
        "symbol_guard": (
            "vartheta_p is the Growth coefficient; it is neither the old "
            "q_branch nor the final q=max(C_fw,C_rev,2)m"
        ),
    }


def certify() -> dict[str, Any]:
    load_dependencies()
    curvature = phase_typed_curvature_family()
    density = invariant_density_and_distortion()
    growth = numeric_growth_and_recovery()
    native = native_levelwise_recovery_frontier()
    frontier = cost_and_q_frontier()
    result = {
        "schema": "cm2.gate4.numeric-invariant-family-growth-recovery-frontier.v1",
        "provenance": {
            "parameter_window": "|s|<=1/400",
            "map_scope": "constant fixed-configuration maps T_s=F_(K_s,K_s)",
            "dependency_sha256": DEPENDENCIES,
        },
        "phase_typed_curvature_family": curvature,
        "invariant_density_and_distortion": density,
        "numeric_growth_and_recovery": growth,
        "native_levelwise_recovery_frontier": native,
        "cost_and_same_occurrence_q_frontier": frontier,
        "scope_limits": {
            "numeric_all_iterated_D_std": True,
            "numeric_all_iterated_standard_curve_distortion": True,
            "numeric_regular_density_invariance": True,
            "numeric_linear_Growth_recurrence": True,
            "numeric_C_p_vartheta_p": True,
            "numeric_A0_A1": True,
            "native_levelwise_unnormalized_payload_recovery_moment": True,
            "single_global_finite_Z_native_family": False,
            "complete_unnormalized_reweighted_native_recovery": False,
            "complete_numeric_C_fw_C_rev": False,
            "final_same_occurrence_q": False,
            "gate4_certified": False,
        },
    }
    return result


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE4_NUMERIC_ALL_ITERATED_D_STD: CERTIFIED")
    print("GATE4_NUMERIC_ALL_STANDARD_CURVE_DISTORTION: CERTIFIED")
    print("GATE4_NUMERIC_C_P_VARTTHETA_P_A0_A1: CERTIFIED")
    print("GATE4_NATIVE_LEVELWISE_UNNORMALIZED_RECOVERY_MOMENT: CERTIFIED")
    print("GATE4_COMPLETE_C_FW_C_REV_FINAL_Q: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
