#!/usr/bin/env python3
"""Round-52 Gate-4 defect-threshold and same-ID return frontier.

Round 51 reduced the variable preproperisation clock to the same-kernel
moment ``integral exp(Dbar/6)`` and supplied a much stronger, but unnecessarily
strong, linear endpoint-tail interface.  This append-only certificate finds
the exact exponential tail threshold.  In particular the rational four-step
tail ``mass{M>m} <= C*2^(-floor(m/4))`` already suffices.

An explicit Lipschitz outer majorant of C24 also turns the qualitative SYZ
memory-loss theorem into a common existential terminal time at which both
orientation survivors have mass above 499/500.  Their once-charged Borel
intersection therefore has mass above 249/250 and both dyadic shells are
zero.  This removes the old marginal-shell obstruction: parent mass is now
dominated by either survivor mass, so the survivor-supported clock estimate
does transfer back to the parent law.  Once the physical defect exponential
moment is supplied, it also gives an integrable total ambient max-clock
envelope and its absolutely-continuous Borel-exhaustion tail.  This envelope
is not the physical return variable q: the Round-51 view transfer is only
Borel, the intersection is not geometrically proper, and no common-refinement
boundary-Z or strong singular/current cemetery interface is installed.

Finally, reindexing by individual Round-35 restrictions is audited directly.
It is a valid once-charge singleton-family retyping and removes the artificial
"one short endpoint poisons a long group" effect, but its Hölder estimate is
on outer-measure times counting-measure.  The missing cell-multiplicity term
can diverge even with bounded leaf density.  No physical defect moment,
proper same-ID return, complete q, strong cemetery, Gate 4, or CM2 is
promoted.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate34.round52-defect-threshold-same-id-return-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate34-round52-defect-threshold-same-id-return-frontier-manifest-2026-07-20.json"
)
DEFAULT_VERIFIER = (
    HERE / "cm2_gate34_round52_defect_threshold_same_id_return_frontier_verifier.py"
)

DEPENDENCIES = {
    "cm2-gate34-round51-two-proper-view-common-law-manifest-2026-07-20.json": (
        "028c5a8f59a6efffa9df93cfba841f3844d244988dc235038183eef222d21abc"
    ),
    "cm2-gate34-round48-borel-survivor-kernel-manifest-2026-07-19.json": (
        "68f0ee7595688ef4ea1ab5eb1e101ab8c2ccd327d3bcf40876ccbd40a5d9bfab"
    ),
    "cm2-gate45-round28-weighted-tail-transfer-frontier-manifest-2026-07-18.json": (
        "eef1071c1f4973892bf5e450421f3b91de7a2b426165e6a8c6f8bb4404eeac57"
    ),
    "cm2-gate34-round51-uniform-gauge-bump-frontier-manifest-2026-07-20.json": (
        "4248c215821ba6e23eb78c64158b1301e1b33d964fb0cd024e4b8e4427247b21"
    ),
    "cm2-gate34-c24-open-hole-geometry-manifest-2026-07-18.json": (
        "f0521bb84fc5b1c824d8361d375013aff024a89460cbc439f5aa7a04d7525183"
    ),
    "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json": (
        "ece7c97beeeb0b527434dc430e247ad0af407dc58b82d634da9e34a2f9e9521c"
    ),
    "cm2-gate34-round50-physical-whole-family-grouping-manifest-2026-07-19.json": (
        "79032e73e9b8d89fd3ecb8e60ac6b1899093e5cc35c8889a62ac47e168a90b73"
    ),
    "cm2-gate34-round52-outer-rate-numeric-frontier-manifest-2026-07-20.json": (
        "b86b5c74c8dcf4d2415ad28715a55ea98bf42bb191f7926684009ebbb8c8da34"
    ),
}

EXP_LOWER = Q(7, 6)
EXP_UPPER_SHARP = Q(241, 204)
EXP_UPPER = Q(13, 11)
QUARTER_BLOCK_RATIO = EXP_UPPER**4 / 2
DEFECT_OFFSET = 309
CP_EXACT = Q(4 * 10**90 * 360493663, 358863)
OVERLAP_RANK = 312
HIT_GAP = Q(21, 111718750)
OUTER_SUPPORT_MASS = Q(87603, 125000000)
OUTER_MIXING_ERROR = Q(1, 1000)
OUTER_HIT_UPPER = Q(1, 500)
SURVIVOR_LOWER = 1 - OUTER_HIT_UPPER
COMMON_SURVIVOR_LOWER = 1 - 2 * OUTER_HIT_UPPER
OUTER_NORM_UPPER = 7251
POSTCUT_BASE = 221328


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def qstr(value: Q) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def reject_constant(token: str) -> None:
    raise ValueError(f"non-finite JSON constant: {token}")


def load(name: str) -> dict[str, Any]:
    path = HERE / name
    if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
        raise RuntimeError(f"unsafe dependency: {name}")
    if sha(path) != DEPENDENCIES[name]:
        raise RuntimeError(f"dependency hash: {name}")
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_object,
        parse_constant=reject_constant,
    )
    if not isinstance(value, dict):
        raise RuntimeError(f"dependency root: {name}")
    return value


def validate_dependencies() -> None:
    round51 = load(
        "cm2-gate34-round51-two-proper-view-common-law-manifest-2026-07-20.json"
    )["result"]
    if round51["physical_two_proper_view_object_lemma"]["status"] != (
        "CERTIFIED_PHYSICAL_BOREL_TWO_PROPER_VIEW_MEASURE_ISOMORPHISM"
    ):
        raise RuntimeError("Round51 two-view law")
    if round51["physical_postproperization_W_r_join"]["status"] != (
        "CERTIFIED_PHYSICAL_POSTPROPERIZATION_TWO_VIEW_W_R_ONCE_CHARGE_MOMENT"
    ):
        raise RuntimeError("Round51 survivor-supported W_r")
    full = round51["full_clock_conditional_bridge"]
    if full["exact_preclock_exponent"] != "696/4176=1/6":
        raise RuntimeError("Round51 preclock exponent")
    if full["physical_I_D_certified"] is not False:
        raise RuntimeError("Round51 defect frontier")
    defect = round51["exact_defect_and_short_tail_frontier"]
    if defect["exact_defect_formula"] != [
        "Dbar(M)=0 for 0<=M<=310",
        "Dbar(M)=M-309 for every integer M>=311; in particular Dbar never equals 1",
    ]:
        raise RuntimeError("Round51 defect formula")
    if round51["intersection_and_gate_frontier"][
        "proper_common_fw_rev_return"
    ] != "NOT_CERTIFIED":
        raise RuntimeError("Round51 common-return frontier")
    if round51["intersection_and_gate_frontier"]["collision_time_q"] != (
        "NOT_CERTIFIED"
    ):
        raise RuntimeError("Round51 physical-q frontier")
    if round51["intersection_and_gate_frontier"][
        "strong_trace_current_cemetery"
    ] != "NOT_CERTIFIED":
        raise RuntimeError("Round51 strong-cemetery frontier")

    round48 = load(
        "cm2-gate34-round48-borel-survivor-kernel-manifest-2026-07-19.json"
    )["result"]
    nonpromotion = round48["exact_nonpromotion_countermodels"]
    if nonpromotion["common_intersection_inherits_properness"] is not False:
        raise RuntimeError("Round48 intersection type")
    if nonpromotion["marginal_survivor_moments_imply_parent_q_moment"] is not False:
        raise RuntimeError("Round48 q type")
    common = round48["same_ID_common_intersection_ambient_clock_moment"]
    if common["same_ID_joint_return_or_q_inferred"] is not False:
        raise RuntimeError("Round48 no joint promotion")

    round28 = load(
        "cm2-gate45-round28-weighted-tail-transfer-frontier-manifest-2026-07-18.json"
    )["result"]
    definitions = round28["weighted_tail_transfer_theorem"]["definitions"]
    if definitions["two_views_charge_policy"] != (
        "q=max(C_fw,C_rev,2)*m is charged once, never once per view"
    ):
        raise RuntimeError("Round28 q definition")
    if definitions["scope"] != (
        "regular first-return components; cemetery strong charge is accounted separately"
    ):
        raise RuntimeError("Round28 first-return/strong-cemetery scope")
    global_lp = round28["weighted_tail_transfer_theorem"]["global_Lp_transfer"]
    if "sum_{j>=1,k} mbar_j,k*c_j,k^p <= M_p" not in global_lp["hypotheses"]:
        raise RuntimeError("Round28 global Lp interface")
    survivor_lp = round28["weighted_tail_transfer_theorem"][
        "survivor_conditioned_Lp_transfer"
    ]
    if (
        "all qbar_j,k are on the same physical first-return component and common fw/rev restriction"
        not in survivor_lp["hypotheses"]
    ):
        raise RuntimeError("Round28 common physical carrier")
    if round28["strict_nonpromotion"]["q_weighted_excursion_cemetery_tail"] != (
        "NOT_CERTIFIED"
    ):
        raise RuntimeError("Round28 q frontier")

    uniform = load(
        "cm2-gate34-round51-uniform-gauge-bump-frontier-manifest-2026-07-20.json"
    )["result"]
    bump = uniform["uniform_standard_family_bump_minorisation"]
    if bump["status"] != "CERTIFIED_UNIFORM_EXISTENTIAL_TIME_WITH_NUMERIC_HIT_FRACTION":
        raise RuntimeError("Round51 uniform memory loss")
    if Q(bump["actual_whole_family_C24_hit_fraction_strict_lower_at_H_bump"]) != HIT_GAP:
        raise RuntimeError("Round51 inner hit")
    if bump["one_uniform_finite_integer_H_bump_exists"] is not True:
        raise RuntimeError("Round51 common time")
    if bump["numeric_H_bump"] is not None:
        raise RuntimeError("Round51 effectivity boundary")

    hole = load(
        "cm2-gate34-c24-open-hole-geometry-manifest-2026-07-18.json"
    )["result"]
    inventory = hole["frozen_core_inventory"]
    mass = hole["collision_SRB_core_mass_interval"]
    if inventory["core_count"] != 24:
        raise RuntimeError("C24 core count")
    if mass["collision_SRB_axis_unnormalized_base"] != "13/156250":
        raise RuntimeError("C24 axis base")
    if mass["collision_SRB_diagonal_unnormalized_base"] != "26/15625":
        raise RuntimeError("C24 diagonal base")
    if mass["normalization_denominator_strict_lower_using_pi_gt_3"] != "156/25":
        raise RuntimeError("C24 normalization")

    carrier = load(
        "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json"
    )["result"]
    pair = carrier["common_forward_reverse_carrier_pair"]
    if pair["common_physical_restriction_id"] != (
        "rn-restriction:(component-id):(source-parent-W-id):(image-recut-rank)"
    ):
        raise RuntimeError("Round35 full restriction ID")
    if pair["forward_and_reverse_are_two_views_not_two_charges"] is not True:
        raise RuntimeError("Round35 once charge")
    if carrier["collision_SRB_leaf_disintegration"]["conditional_density_wrt_dell"] != (
        "cp/sqrt(17)"
    ):
        raise RuntimeError("Round35 leaf density")

    round50 = load(
        "cm2-gate34-round50-physical-whole-family-grouping-manifest-2026-07-19.json"
    )["result"]
    grouping = round50["physical_Borel_whole_family_grouping"]
    if grouping["kernel_partition_identities_mod_null"] != [
        "sum_{k,j}K_fw(y,k,j;A)=K_par(y,A)",
        "sum_{k,j}K_rev(y,k,j;A)=K_par(y,A)",
    ]:
        raise RuntimeError("Round50 cell partitions")
    if grouping["finite_fibre_Borel_projection"].find("Round35 record space is Borel") < 0:
        raise RuntimeError("Round50 Borel record space")

    round52_outer = load(
        "cm2-gate34-round52-outer-rate-numeric-frontier-manifest-2026-07-20.json"
    )["result"]
    outer = round52_outer["uniform_C24_outer_majorant_and_common_terminal_survivor"]
    if outer["status"] != (
        "CERTIFIED_NUMERIC_OUTER_MAJORANT_AND_EXISTENTIAL_COMMON_TERMINAL_SURVIVOR"
    ):
        raise RuntimeError("Round52 outer status")
    if outer["construction"]["global_function"] != (
        "g_out=max of the twenty-four one-box products"
    ):
        raise RuntimeError("Round52 outer construction")
    if Q(outer["support_mass"]["mu_s_g_out_strict_upper"]) != OUTER_SUPPORT_MASS:
        raise RuntimeError("Round52 outer support mass")
    if outer["Lipschitz_bound"]["norm_infinity_plus_Lip_1_strict_upper"] != str(
        OUTER_NORM_UPPER
    ):
        raise RuntimeError("Round52 outer norm")
    terminal = outer["uniform_existential_small_terminal_hit"]
    if Q(terminal["per_proper_view_terminal_C24_mass_strict_upper"]) != (
        OUTER_HIT_UPPER
    ):
        raise RuntimeError("Round52 terminal hit")
    if Q(terminal["per_proper_view_terminal_nonhit_mass_strict_lower"]) != (
        SURVIVOR_LOWER
    ):
        raise RuntimeError("Round52 terminal survivor")
    if Q(terminal["same_parent_common_terminal_nonhit_mass_strict_lower"]) != (
        COMMON_SURVIVOR_LOWER
    ):
        raise RuntimeError("Round52 common terminal survivor")
    scope = outer["strict_scope"]
    if scope["terminal_test_only"] is not True:
        raise RuntimeError("Round52 terminal-only scope")
    if scope["intermediate_C24_avoidance"] != "NOT_CERTIFIED":
        raise RuntimeError("Round52 intermediate-avoidance frontier")
    if scope["properness_of_common_nonhit_restriction"] != "NOT_CERTIFIED":
        raise RuntimeError("Round52 common-properness frontier")


def safe_defect(M: int) -> int:
    if M < 0:
        raise ValueError("M must be nonnegative")
    return 0 if M <= 310 else M - DEFECT_OFFSET


def exponential_bracket() -> dict[str, Any]:
    # For k>=2, k! >= 2*3^(k-2).  Hence the exponential tail is bounded
    # by (1/72)*sum_j (1/18)^j = 1/68.
    tail_upper = Q(1, 72) / (1 - Q(1, 18))
    series_upper = 1 + Q(1, 6) + tail_upper
    assert tail_upper == Q(1, 68)
    assert series_upper == EXP_UPPER_SHARP
    assert EXP_LOWER < EXP_UPPER_SHARP < EXP_UPPER
    assert EXP_UPPER**4 < 2
    return {
        "lower_bound": "exp(1/6)>1+1/6=7/6",
        "upper_series_factorial_bound": "for k>=2, k!>=2*3^(k-2)",
        "upper_tail_sum": "sum_{k>=2}(1/6)^k/k!<=(1/72)/(1-1/18)=1/68",
        "upper_bound": "exp(1/6)<241/204<13/11",
        "cross_product_gap_for_241_over_204_below_13_over_11": 1,
        "quarter_block_power": qstr(EXP_UPPER**4),
        "quarter_block_strict_gap_to_2": qstr(2 - EXP_UPPER**4),
        "quarter_block_ratio": qstr(QUARTER_BLOCK_RATIO),
        "status": "CERTIFIED_EXACT_RATIONAL_BRACKET_FOR_EXP_ONE_SIXTH",
    }


def quarter_tail_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for m in (0, 4, 16, 310, 311, 312, 315, 316, 320):
        rows.append(
            {
                "tail_index_m": m,
                "quarter_block_index": m // 4,
                "tail_majorant": f"C_quarter*2^-{m // 4}",
                "positive_defect_tail_event": (
                    "{Dbar>0}={M>310}"
                    if m == 310
                    else (f"{{Dbar>{m - 309}}}={{M>{m}}}" if m >= 311 else "not_used")
                ),
            }
        )
    return rows


def sharp_defect_tail_threshold() -> dict[str, Any]:
    A = EXP_UPPER
    assert Q(2**310) < CP_EXACT < Q(2**311)
    # Exact rational upper coefficient for the quarter-block tail.
    # Sum from m=311: one k=0 term followed by four-residue blocks.
    grouped_sum_without_2pow77 = A**2 + Q(1, 2) * A**3 * (
        1 + A + A**2 + A**3
    ) / (1 - A**4 / 2)
    coefficient_without_2pow77 = (
        A**2 - 1 + (A - 1) * grouped_sum_without_2pow77
    )
    coefficient = coefficient_without_2pow77 / Q(2**77)
    assert coefficient_without_2pow77 == Q(23446, 721)
    assert coefficient == Q(11723, 54477219746384227185197056)
    rows = quarter_tail_rows()
    return {
        "measure": "nu(dy)=p(y)dlambda(y), a finite law on integer M>=0",
        "defect": [
            "Dbar=0 on M<=310",
            "Dbar=M-309 on M>=311, so the positive values start at 2",
        ],
        "exact_layer_cake": (
            "I_D=nu(X)+(a^2-1)T_310+(a-1)*sum_{m>=311}a^(m-309)T_m, "
            "where a=exp(1/6) and T_m=nu{M>m}"
        ),
        "general_exponential_tail_bridge": (
            "if T_m<=C*b^m and 0<b<exp(-1/6), then I_D<infinity"
        ),
        "critical_tail_base": "b_c=exp(-1/6)",
        "critical_dyadic_exponent": "alpha_c=log_2(exp(1/6))=1/(6*log(2))",
        "critical_decimal_for_orientation_only": "0.2404491734814939...",
        "sharpness_scope": (
            "this is the exact threshold for a pure exponential tail upper bound; at equality a finite probability countermodel has infinite I_D"
        ),
        "old_round51_sufficient_tail": "T_m<=C_len*2^-m",
        "strictly_weaker_rational_sufficient_tail": (
            "T_m<=C_quarter*2^(-floor(m/4)) for every integer m>=0"
        ),
        "rational_majorant_base": "a<13/11",
        "rational_group_ratio": "(13/11)^4/2=28561/29282<1",
        "quarter_tail_integrated_bound": (
            "I_D<=nu(X)+(11723/54477219746384227185197056)*C_quarter"
        ),
        "quarter_tail_coefficient": qstr(coefficient),
        "quarter_tail_rows": rows,
        "quarter_tail_rows_sha256": digest(rows),
        "actual_physical_quarter_tail_available": False,
        "actual_physical_I_D_certified": False,
        "status": "CERTIFIED_SHARP_DEFECT_EXPONENTIAL_TAIL_THRESHOLD_AND_RATIONAL_QUARTER_TAIL_BRIDGE",
    }


def critical_counter_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for k in (0, 1, 2, 4, 8, 16):
        mass = Q(1, 7) * Q(6, 7) ** k
        rows.append(
            {
                "k": k,
                "M": 311 + k,
                "Dbar": 2 + k,
                "rational_atom_mass": qstr(mass),
                "required_moment_term_strict_lower": "7/36",
                "tail_at_m_equals_310_plus_k": qstr(Q(6, 7) ** k),
            }
        )
    return rows


def critical_tail_countermodels() -> dict[str, Any]:
    rows = critical_counter_rows()
    return {
        "sharp_symbolic_probability_law": (
            "for a=exp(1/6), put M_k=311+k and w_k=(1-a^-1)*a^-k, k>=0"
        ),
        "sharp_symbolic_total_mass": "sum_k w_k=1",
        "sharp_symbolic_tail": (
            "T_m=a^(-(m-310)) for every m>=310, exactly the critical base b_c=a^-1"
        ),
        "sharp_symbolic_moment_failure": (
            "w_k*a^Dbar(M_k)=(1-a^-1)*a^2 for every k, so I_D=infinity"
        ),
        "subcritical_exponents_also_fail": (
            "the same critical law obeys a C*2^(-alpha*m) upper tail for every alpha<=alpha_c"
        ),
        "fully_rational_replay_law": (
            "M_k=311+k and w_k=(1/7)*(6/7)^k; its total mass is one"
        ),
        "rational_tail": "T_(310+k)=(6/7)^k",
        "rational_failure_reason": (
            "exp(1/6)>7/6 gives w_k*exp((k+2)/6)>7/36 for every k"
        ),
        "rows": rows,
        "rows_sha256": digest(rows),
        "logical_scope": (
            "exact nonimplication for endpoint-tail fields, not a claim that the physical billiard realizes either atomic law"
        ),
        "actual_billiard_defect_moment_disproved": False,
        "status": "CERTIFIED_CRITICAL_AND_RATIONAL_BELOW_THRESHOLD_COUNTERMODELS",
    }


def uniform_outer_majorant_terminal_join() -> dict[str, Any]:
    assert OUTER_SUPPORT_MASS < Q(1, 1000)
    assert OUTER_SUPPORT_MASS + OUTER_MIXING_ERROR < OUTER_HIT_UPPER
    assert SURVIVOR_LOWER == Q(499, 500)
    assert COMMON_SURVIVOR_LOWER == Q(249, 250)
    assert HIT_GAP < Q(1, 1000) < OUTER_HIT_UPPER
    return {
        "outer_observable": (
            "g_out=max of the 24 parameter-uniform trapezoid-product majorants, with 1_C24<=g_out<=1"
        ),
        "padding": {
            "axis_delta_t_delta_p": ["1/1000", "1/1000"],
            "diagonal_delta_t_delta_p": ["1/1000", "1/100"],
        },
        "collision_SRB_support_mass_strict_upper": qstr(OUTER_SUPPORT_MASS),
        "support_mass_comparison": "87603/125000000<1/1000",
        "outer_theorem_norm_strict_upper": "norm_infinity(g_out)+Lipschitz_1(g_out)<7251",
        "uniform_SYZ_error_strict_upper": qstr(OUTER_MIXING_ERROR),
        "simultaneous_terminal_time": (
            "choose one finite H_joint beyond both uniform SYZ thresholds for the Round51 inner bump and the outer majorant"
        ),
        "H_joint_exists_uniformly_for_all_parameters_and_proper_views": True,
        "numeric_H_joint": None,
        "per_orientation_terminal_C24_hit_fraction": (
            "21/111718750<h_sigma,hit/p<1/500"
        ),
        "inner_strict_lower": qstr(HIT_GAP),
        "outer_strict_upper": qstr(OUTER_HIT_UPPER),
        "per_orientation_terminal_survivor_fraction_strict_lower": qstr(
            SURVIVOR_LOWER
        ),
        "same_ID_once_charged_common_terminal_survivor_fraction_strict_lower": qstr(
            COMMON_SURVIVOR_LOWER
        ),
        "common_mass_reason": (
            "on the Round51 raw once-charged law, the union of the two terminal-hit events has mass <2p/500"
        ),
        "dyadic_shells": "k_fw=k_rev=0 because h_fw/p,h_rev/p>499/500>1/2",
        "equal_postproperization_clocks": (
            "C_fw,post=C_rev,post=H_joint+221328"
        ),
        "parent_mass_domination": (
            "p<(500/499)h_fw and p<(500/499)h_rev on every nonzero parent record"
        ),
        "old_marginal_shell_obstruction": "ELIMINATED_FOR_THIS_COMMON_TERMINAL_SCHEDULE",
        "parent_charged_postclock_ambient_max_envelope_L6over5": (
            "CERTIFIED_QUALITATIVELY_FINITE because H_joint is one finite constant and integral p is finite"
        ),
        "total_orientation_clock": (
            "C_sigma,total=696*Dbar+H_joint+221328"
        ),
        "conditional_total_ambient_max_clock_envelope": (
            "if I_D=integral p*exp(Dbar/6)<infinity, then the parent-charged total ambient two-view max-clock exponential moment and its L^(6/5) envelope are finite"
        ),
        "conditional_ambient_envelope_Borel_exhaustion_tail": (
            "under the same I_D hypothesis, the absolutely-continuous ambient envelope is integrable, so its mass outside any increasing full-mass Borel exhaustion tends to zero"
        ),
        "physical_q_requires": (
            "a proper same-ID common return/common-refinement boundary-Z theorem and the moment for every additional recovery clock on that physical carrier"
        ),
        "physical_collision_time_q_L6over5": "NOT_CERTIFIED",
        "strong_singular_current_cemetery": "NOT_CERTIFIED",
        "terminal_not_intermediate": (
            "the conclusion controls the C24 predicate at the single terminal collision only; it does not assert avoidance at intermediate collisions"
        ),
        "common_terminal_subkernel_is_Borel_and_positive": True,
        "common_terminal_subkernel_is_geometrically_proper": False,
        "status": "CERTIFIED_UNIFORM_LARGE_COMMON_TERMINAL_SURVIVOR_AND_AMBIENT_CLOCK_TRANSFER",
    }


def cell_retyping_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for n in (18, 19, 20, 24):
        M = n * n
        Dbar = safe_defect(M)
        lower = Q(1, 2**n) * EXP_LOWER**Dbar
        ratio = Q(1, 2) * EXP_LOWER ** (2 * n + 1)
        rows.append(
            {
                "band_n": n,
                "band_mass": f"2^-{n}",
                "cell_count": f"2^{M}",
                "each_cell_length": f"2^-{M}",
                "leaf_density_rho_j": "1",
                "fixed_physical_D1_density_d_D1": "D0 (one fixed finite positive constant)",
                "cell_length_rank_M": M,
                "safe_defect_Dbar": Dbar,
                "band_defect_moment_strict_lower": qstr(lower),
                "next_band_lower_term_ratio": qstr(ratio),
            }
        )
    return rows


def cell_level_retyping_audit() -> dict[str, Any]:
    rows = cell_retyping_rows()
    return {
        "reindexing": (
            "retain natural-short-cell-k and image-recut-rank in the Round35 restriction ID instead of forgetting them in the Round50 whole-group projection"
        ),
        "Borel_and_once_charge": (
            "CERTIFIED: the fibres are finite, the half-open cells partition K_par modulo the frozen null boundary, and the fw/rev representatives remain two views of one charge"
        ),
        "singleton_family_typing": (
            "CERTIFIED: one measured standard pair is a singleton whole standard family; if initially nonproper it becomes an eligible whole proper family after its own closed 696*Dbar evolution"
        ),
        "real_gain": (
            "the defect is charged to each cell's own length rank, so one short cell no longer assigns its worst M to unrelated long cells in the former group"
        ),
        "failed_inference": (
            "p_j<=rho_j*ell_j followed by outer Hölder needs an integral of sum_j rho_j against the outer base measure; physical D1 instead integrates its separately typed density d_D1^(6/5) against cell mass p_j"
        ),
        "missing_counting_density_interface": (
            "integral sum_j rho_j db<infinity (or a quantitatively equivalent cell-count/packing tail)"
        ),
        "exact_countermodel": (
            "on a b-band of width 2^-n, split a unit fibre into N_n=2^(n^2) half-open cells of length 2^(-n^2), with leaf density rho_j=1 and a separately fixed finite physical D1 density d_D1=D0 (compatible with a fixed rank such as B=14)"
        ),
        "once_charge_check": (
            "N_n*ell_n=1, so band mass is exactly 2^-n and the sum over all bands is finite"
        ),
        "physical_D1_type_moment": (
            "D0^(6/5)*sum_n 2^-n is finite because d_D1=D0 is fixed and D1 charges cell mass"
        ),
        "outer_counting_density": (
            "on band n, sum_j rho_j gives 2^-n*2^(n^2), so the missing outer counting-density integral diverges"
        ),
        "cellwise_defect_moment": (
            "for n>=18 its band contribution is 2^-n*exp((n^2-309)/6); successive ratios are (1/2)*exp((2n+1)/6)>1 and tend to infinity"
        ),
        "rows": rows,
        "rows_sha256": digest(rows),
        "logical_scope": (
            "an exact standard-Borel partition countermodel for the currently certified fields, not an assertion that the billiard realizes these multiplicities"
        ),
        "physical_defect_moment_disproved": False,
        "cell_retyping_closes_I_D": False,
        "status": "CERTIFIED_CELL_REINDEXING_REMOVES_GROUP_MIN_POISONING_BUT_NOT_CELL_MULTIPLICITY_DEFECT",
    }


def large_common_mass_geometric_nonpromotion() -> dict[str, Any]:
    block_mass = Q(999, 1000)
    common_mass = Q(499, 500)
    assert block_mass > SURVIVOR_LOWER
    assert common_mass > COMMON_SURVIVOR_LOWER
    assert Q(1, 1000) < OUTER_HIT_UPPER
    assert Q(1, 1000) > HIT_GAP
    return {
        "ambient_law": "Lebesgue probability on [0,1) in each proper view",
        "forward_survivor": "F=[0,999/1000)",
        "reverse_survivor_in_reverse_view": "R=[0,999/1000)",
        "each_terminal_hit_fraction": "1/1000",
        "outer_and_inner_hit_bounds_satisfied": (
            "21/111718750<1/1000<1/500"
        ),
        "both_marginal_survivor_fractions": qstr(block_mass),
        "fragmented_pullback_construction": (
            "for k>=1 partition [0,999/1000) into blocks of length (999/1000)2^-k; in block k retain an interval A_k of length (998/1000)2^-k and then a gap of length (1/1000)2^-k; put A=(union_k A_k) union [999/1000,1)"
        ),
        "Borel_measure_isomorphism": (
            "a countable interval-by-interval translation Theta sends A onto R and its complement onto [999/1000,1), hence Theta preserves Lebesgue measure and is a Borel isomorphism"
        ),
        "transported_reverse_survivor": "Theta^-1(R)=A",
        "same_ID_common_survivor": "F intersect A=union_k A_k",
        "same_ID_common_mass": qstr(common_mass),
        "common_mass_exceeds_physical_union_bound": "499/500>249/250",
        "marginal_geometry": (
            "F and R are each one interval with normalized boundary numerator 1000/999<C_p"
        ),
        "common_boundary_numerator": (
            "sum_k mass(A_k)/length(A_k)=sum_k 1=infinity"
        ),
        "positive_gap_forces_distinct_regular_components": (
            "a positive regular density has full support on its connected W, so the positive-length gaps prevent W from joining two A_k; for the representation fibre I_k over A_k, |W_a|<=|A_k| and integral_(I_k)dlam=mu(A_k)=|A_k|, hence integral_(I_k)|W_a|^-1 dlam>=1 and summing k gives J=infinity"
        ),
        "common_standard_family_proper": False,
        "what_mass_does_certify": (
            "the physical Round52 common terminal subkernel is nonzero with a uniform mass margin"
        ),
        "what_is_still_missing": (
            "a physical curvewise regularity/common-refinement estimate for Theta and the two terminal predicates that makes the common boundary-Z numerator finite (with the required moment or uniform bound)"
        ),
        "logical_scope": (
            "the model separates the currently installed Borel two-view and terminal-mass fields from boundary geometry; it is not a physical billiard counterexample"
        ),
        "physical_proper_common_return_disproved": False,
        "proper_same_ID_fw_rev_return_inferred": False,
        "status": "CERTIFIED_LARGE_COMMON_MASS_BOREL_TWO_VIEW_FIELDS_DO_NOT_IMPLY_PROPER_INTERSECTION",
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "parameter_scope": "inherits the fixed-|s|<=1/400 scope of Round51; countermodels are logical abstract models",
            "claim_type": (
                "sharp defect-tail threshold, rational quarter-tail bridge, uniform large terminal survivor join, cell-retyping audit, and exact separation of common mass from common boundary geometry"
            ),
        },
        "exp_one_sixth_rational_bracket": exponential_bracket(),
        "sharp_defect_moment_tail_threshold": sharp_defect_tail_threshold(),
        "critical_tail_countermodels": critical_tail_countermodels(),
        "uniform_outer_majorant_terminal_join": (
            uniform_outer_majorant_terminal_join()
        ),
        "cell_level_retyping_audit": cell_level_retyping_audit(),
        "large_common_mass_geometric_nonpromotion": (
            large_common_mass_geometric_nonpromotion()
        ),
        "compressed_physical_frontier": {
            "two_proper_view_measure_transport": "CERTIFIED_IN_ROUND51",
            "uniform_common_terminal_survivor_mass_gt_249_over_250": "CERTIFIED",
            "same_ID_geometric_return": "POSITIVE_BOREL_SUBKERNEL_CERTIFIED__PROPERNESS_NOT_CERTIFIED",
            "cell_level_once_charge_retyping": "CERTIFIED_BUT_I_D_STILL_NOT_CLOSED",
            "old_linear_short_endpoint_tail_needed": False,
            "sharp_pure_exponential_tail_threshold": "alpha>1/(6*log(2))",
            "rational_quarter_block_tail_would_suffice": True,
            "physical_quarter_block_tail": "NOT_CERTIFIED",
            "physical_defect_moment": "NOT_CERTIFIED",
            "full_total_ambient_max_clock_Lp_envelope": "CONDITIONAL_ON_PHYSICAL_I_D",
            "old_marginal_shell_q_obstruction": "ELIMINATED_BY_x_sigma_gt_499_over_500",
            "parent_charged_postclock_ambient_max_envelope_L6over5": "CERTIFIED_QUALITATIVELY_FINITE",
            "parent_charged_total_ambient_max_envelope_L6over5": "CONDITIONAL_ON_PHYSICAL_I_D",
            "ambient_envelope_Borel_exhaustion_tail": "CONDITIONAL_ON_PHYSICAL_I_D",
            "physical_collision_time_q_L6over5": "NOT_CERTIFIED_REQUIRES_PROPER_COMMON_RETURN_AND_RECOVERY_JOIN",
            "strong_singular_current_cemetery": "NOT_CERTIFIED",
            "complete_numeric_C_fw_C_rev": "NOT_CERTIFIED",
            "numeric_collision_time_q": "NOT_CERTIFIED",
            "common_intersection_boundary_Z": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "strict_nonpromotion": {
            "sharp_defect_tail_threshold": "CERTIFIED",
            "rational_quarter_tail_conditional_bridge": "CERTIFIED",
            "uniform_large_common_terminal_survivor": "CERTIFIED",
            "cell_level_once_charge_retyping": "CERTIFIED",
            "physical_quarter_tail_or_defect_moment": "NOT_CERTIFIED",
            "proper_same_ID_geometric_return": "NOT_CERTIFIED",
            "parent_charged_postclock_ambient_max_envelope_L6over5": "CERTIFIED_QUALITATIVELY_FINITE",
            "parent_charged_total_ambient_max_envelope_L6over5": "CONDITIONAL_NOT_CLOSED",
            "ambient_envelope_Borel_exhaustion_tail": "CONDITIONAL_NOT_CLOSED",
            "physical_collision_time_q_L6over5": "NOT_CERTIFIED",
            "full_numeric_C_fw_C_rev": "NOT_CERTIFIED",
            "numeric_collision_time_q": "NOT_CERTIFIED",
            "strong_singular_current_cemetery": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    result["internal_replay_digest"] = digest(result)
    return result


def write_manifest(path: Path, verifier: Path) -> None:
    result = build_result()
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "certificate_sha256": sha(Path(__file__).resolve()),
        "verifier_sha256": sha(verifier.resolve()),
        "dependencies": DEPENDENCIES,
        "result": result,
        "verdict": result["strict_nonpromotion"],
    }
    path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument("--verifier", type=Path, default=DEFAULT_VERIFIER)
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    strict = build_result()["strict_nonpromotion"]
    print("DEFECT_TAIL_THRESHOLD:", strict["sharp_defect_tail_threshold"])
    print("PHYSICAL_DEFECT_MOMENT:", strict["physical_quarter_tail_or_defect_moment"])
    print("COMMON_TERMINAL_SURVIVOR:", strict["uniform_large_common_terminal_survivor"])
    print("PROPER_SAME_ID_RETURN:", strict["proper_same_ID_geometric_return"])
    print(
        "TOTAL_AMBIENT_MAX_CLOCK_ENVELOPE_L6OVER5:",
        strict["parent_charged_total_ambient_max_envelope_L6over5"],
    )
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
