#!/usr/bin/env python3
"""Fixed-core Green kernel and exact unbounded-cut tail criterion.

The fixed 24-core open operator already has an unnormalised recurrence with
coefficient b_core<1.  This certificate upgrades that pointwise-in-time
bound to a summable transport-delay Green kernel, including exact zeroth and
first moments and a rational exponential-moment bound.

The upgrade controls an unbounded number of propagation delays after any
summable sequence of injections into the fixed core.  It does not create the
missing physical incidence from graph-current occurrences into that core.
Nor does it control an unbounded number of newly selected restrictions.  For
the latter it records the exact geometric count-tail threshold required by
the frozen one-cut factor 15/8 and, separately, by the all-component field-7
factor 580000/1999.
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
    "cm2-gate4-incidence-shell-repeated-frontier-manifest-2026-07-16.json": (
        "c452c07f70db7bac05f23b97491db283707a9d84b15dff9e542a7272e22cd644"
    ),
    "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json": (
        "b03c5ae0e400045f087cfbd1aa8c843990edebe517a4dde786b0718446db7c1d"
    ),
    "cm2-gate4-native-stopping-repeated-recovery-frontier-manifest-2026-07-16.json": (
        "20f595ed4bcf62cb5cc5c89c22ab31a3ca039f43fff29fd35855673dc970b4a2"
    ),
    "cm2-gate3-common-graph-current-carrier-frontier-manifest-2026-07-17.json": (
        "9abdc07cb0618f4a81b8e5591d8de83da7cce2c6d6a82fa41c834dd46c28412c"
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

    incidence = loaded[
        "cm2-gate4-incidence-shell-repeated-frontier-manifest-2026-07-16.json"
    ]
    growth = loaded[
        "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json"
    ]
    native = loaded[
        "cm2-gate4-native-stopping-repeated-recovery-frontier-manifest-2026-07-16.json"
    ]
    carrier = loaded[
        "cm2-gate3-common-graph-current-carrier-frontier-manifest-2026-07-17.json"
    ]

    assert incidence["verdict"][
        "fixed_core_unnormalized_arbitrary_n_propagation"
    ] == "CERTIFIED"
    assert incidence["verdict"][
        "one_cut_mass_weighted_corner_recovery_charge"
    ] == "CERTIFIED"
    assert incidence["verdict"][
        "transported_core_to_occurrence_physical_incidence"
    ] == "NOT_CERTIFIED"
    assert growth["replay_summary"]["native_gamma"] == "1/12060"
    assert growth["verdict"][
        "native_levelwise_unnormalized_recovery_moment"
    ] == "CERTIFIED"
    assert native["replay_summary"]["native_prefix_antichain"] == "CERTIFIED"
    assert native["verdict"]["hereditary_repeated_indicator_recovery"] == (
        "NOT_CERTIFIED"
    )
    assert carrier["result"]["finite_two_cut_algebra"][
        "positive_two_cut_current_TV_outer_upper"
    ] == "2590777728/5"
    assert carrier["verdict"]["physical_depth_two_strong_DQ"] == (
        "NOT_CERTIFIED"
    )
    return loaded


def fixed_core_green_kernel() -> dict[str, Any]:
    b = Q(720269600000, 720626832337)
    margin = 1 - b
    zeroth = 1 / margin
    first = b / margin**2
    half_life = 2018
    gamma = Q(1, 4036)

    assert b < 1
    assert margin == Q(357232337, 720626832337)
    assert b**half_life < Q(1, 2)
    assert zeroth == Q(720626832337, 357232337)
    assert first == Q(
        519045600276638055200000,
        127614942598481569,
    )
    assert gamma * half_life == Q(1, 2)

    # e < 1+1+1/2+1/6+(1/24)sum_{j>=0}4^-j = 49/18 < 25/9.
    e_upper = Q(49, 18)
    square_exp_upper = Q(5, 3)
    block_ratio_upper = Q(5, 6)
    assert e_upper < Q(25, 9)
    assert square_exp_upper**2 == Q(25, 9)
    assert Q(1, 2) * square_exp_upper == block_ratio_upper

    exponential_zeroth_upper = half_life * square_exp_upper / (
        1 - block_ratio_upper
    )
    exponential_first_upper = (
        half_life**2
        * square_exp_upper
        / (1 - block_ratio_upper) ** 2
    )
    assert exponential_zeroth_upper == 20180
    assert exponential_first_upper == 244339440

    return {
        "fixed_open_operator": "O=T_* o M_core on the 24-core union",
        "inherited_boundary_kernel": "g_k=b_core^k, k>=0",
        "b_core": str(b),
        "contraction_margin": str(margin),
        "exact_zeroth_delay_moment": (
            "sum_{k>=0} g_k=1/(1-b_core)"
        ),
        "exact_zeroth_delay_moment_value": str(zeroth),
        "exact_first_delay_moment": (
            "sum_{k>=0} k*g_k=b_core/(1-b_core)^2"
        ),
        "exact_first_delay_moment_value": str(first),
        "exact_unweighted_tail": (
            "sum_{k>L} g_k=b_core^(L+1)/(1-b_core)"
        ),
        "all_polynomial_delay_moments_finite": True,
        "rational_exponential_moment": {
            "gamma": str(gamma),
            "half_life_block": half_life,
            "exact_input": "b_core^2018<1/2",
            "elementary_e_bound": (
                "e<49/18<25/9, hence exp(1/2)<5/3"
            ),
            "weighted_block_ratio_upper": str(block_ratio_upper),
            "sum_exp_gamma_k_g_k_upper": str(exponential_zeroth_upper),
            "sum_k_exp_gamma_k_g_k_upper": str(exponential_first_upper),
            "block_tail_upper": (
                "sum_{k>=2018*q} exp(gamma*k)g_k"
                "<=20180*(5/6)^q"
            ),
        },
        "fixed_core_unbounded_transport_delay_Green_kernel": "CERTIFIED",
    }


def summable_injection_transport() -> dict[str, Any]:
    b = Q(720269600000, 720626832337)
    zeroth = 1 / (1 - b)
    first = b / (1 - b) ** 2
    two_cut_outer = Q(2590777728, 5)
    conditional_zeroth = two_cut_outer * zeroth
    conditional_first = two_cut_outer * first
    conditional_exp = two_cut_outer * 20180
    conditional_exp_first = two_cut_outer * 244339440

    assert conditional_zeroth == Q(
        24246544771660906368, 23196905
    )
    assert conditional_first == Q(
        3492809820813258473063362560000,
        1657336916863397,
    )
    assert conditional_exp == 10456378910208
    assert conditional_exp_first == 126605835844798464

    return {
        "nonnegative_injection_sequence": "J_j>=0 with sum_j J_j<infinity",
        "transported_ledger": (
            "G_n=sum_{0<=j<=n} b_core^(n-j) J_j"
        ),
        "Tonelli_zeroth_bound": (
            "sum_n G_n=(1/(1-b_core))*sum_j J_j"
        ),
        "Tonelli_delay_moment_bound": (
            "sum_n sum_{j<=n}(n-j)b_core^(n-j)J_j"
            "=(b_core/(1-b_core)^2)*sum_j J_j"
        ),
        "exponential_delay_bound": (
            "sum_n sum_{j<=n}exp((n-j)/4036)"
            "b_core^(n-j)J_j<=20180*sum_j J_j"
        ),
        "arbitrarily_many_injection_times_allowed_if_total_injection_is_summable": True,
        "unbounded_transport_delay_count": "CERTIFIED",
        "conditional_common_carrier_injection": {
            "input_two_cut_TV_outer": str(two_cut_outer),
            "requires_physical_incidence_with_norm_enlargement_at_most_one": True,
            "total_unweighted_delay_TV_upper": str(conditional_zeroth),
            "first_delay_moment_TV_upper": str(conditional_first),
            "exponential_delay_TV_upper": str(conditional_exp),
            "exponential_first_delay_TV_upper": str(conditional_exp_first),
            "physical_installation": "NOT_CERTIFIED",
        },
    }


def unbounded_new_cut_criterion() -> dict[str, Any]:
    shell_factor = Q(15, 8)
    field7_factor = Q(580000, 1999)
    assert 1 / shell_factor == Q(8, 15)
    assert 1 / field7_factor == Q(1999, 580000)
    return {
        "integer_cut_count": "H>=0",
        "tail_assumption": "P(H>=h)<=C*rho^h for every h>=1",
        "moment_identity": (
            "E[a^H]=1+(a-1)sum_{h>=1}a^(h-1)P(H>=h)"
        ),
        "geometric_tail_conclusion": (
            "E[a^H]<=1+C*(a-1)*rho/(1-a*rho) when a*rho<1"
        ),
        "one_cut_mass_weighted_shell": {
            "a": str(shell_factor),
            "necessary_strict_sufficient_threshold_for_this_bound": (
                "rho<8/15"
            ),
            "bound_under_threshold": (
                "E[(15/8)^H]<=1+C*(7/8)*rho/(1-(15/8)rho)"
            ),
        },
        "raw_all_component_field7": {
            "a": str(field7_factor),
            "necessary_strict_sufficient_threshold_for_this_bound": (
                "rho<1999/580000"
            ),
        },
        "certified_native_geometric_cut_count_rho": None,
        "native_cut_count_tail_below_8_over_15": "NOT_CERTIFIED",
        "native_cut_count_tail_below_1999_over_580000": "NOT_CERTIFIED",
        "unbounded_new_cut_criterion": "CERTIFIED",
        "unbounded_new_cut_hypothesis": "NOT_CERTIFIED",
    }


def build_result() -> dict[str, Any]:
    load_dependencies()
    result: dict[str, Any] = {
        "schema": "cm2.gate4.fixed-core-green-kernel-unbounded-cut-frontier.v1",
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
        },
        "fixed_core_green_kernel": fixed_core_green_kernel(),
        "summable_injection_transport": summable_injection_transport(),
        "unbounded_new_cut_criterion": unbounded_new_cut_criterion(),
        "strict_nonpromotion": {
            "unbounded_delay_implies_physical_occurrence_incidence": False,
            "summable_injections_imply_arbitrary_injections_are_summable": False,
            "finite_one_cut_factor_implies_native_cut_count_tail": False,
            "fixed_core_Green_kernel_implies_cemetery_payload": False,
            "transported_24_core_to_41444_graph_incidence": "NOT_CERTIFIED",
            "strong_complement_cemetery_payload": "NOT_CERTIFIED",
            "native_unbounded_repeated_cut_recovery": "NOT_CERTIFIED",
            "complete_C_fw_C_rev_q": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
        },
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def main() -> None:
    print(json.dumps(build_result(), indent=2, sort_keys=True))
    print("FIXED_CORE_UNBOUNDED_DELAY_GREEN_KERNEL: CERTIFIED")
    print("UNBOUNDED_NEW_CUT_TAIL_CRITERION: CERTIFIED")
    print("NATIVE_UNBOUNDED_REPEATED_CUT_RECOVERY: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
