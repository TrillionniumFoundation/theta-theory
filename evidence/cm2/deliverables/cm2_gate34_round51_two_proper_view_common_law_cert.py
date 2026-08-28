#!/usr/bin/env python3
"""Round-51 two-proper-view common-law and short-endpoint frontier.

Round 50 correctly observed that the raw grouped kernel ``K_par`` is not in
general a proper standard family.  That fact does not prevent a once-charged
common-law moment.  On the full-measure regular set, the forward and reverse
recordwise properizations are two fibrewise Borel measure-space
isomorphisms from the *same* finite raw law to two proper pushforward laws.
Each orientation proves its survivor-clock moment in its own proper geometry;
the two functions are then pulled back to the raw law (equivalently, the
reverse function is transported to the forward proper law).  A pointwise
maximum inequality gives the common once-charge bound.

The variable preproperization clock still needs an exponential moment of the
minimum-length defect.  Existing data only imply that its tail tends to zero,
with no quantitative rate.  This certificate installs the exact conditional
tail bridge and an exact nonimplication model.  It does not promote complete
C_fw/C_rev, q, a proper intersection, strong cemetery, Gate 4, or CM2.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate34.round51-two-proper-view-common-law.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate34-round51-two-proper-view-common-law-manifest-2026-07-20.json"
)
DEFAULT_VERIFIER = HERE / "cm2_gate34_round51_two_proper_view_common_law_verifier.py"

DEPENDENCIES = {
    "cm2-gate34-round50-physical-whole-family-grouping-manifest-2026-07-19.json": (
        "79032e73e9b8d89fd3ecb8e60ac6b1899093e5cc35c8889a62ac47e168a90b73"
    ),
    "cm2-gate34-round49-sharp-common-law-recovery-manifest-2026-07-19.json": (
        "0cf5d0d6eac469a2ab6f1100a738384af2873473a4ef6457beb1bb45e734f00a"
    ),
    "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json": (
        "ece7c97beeeb0b527434dc430e247ad0af407dc58b82d634da9e34a2f9e9521c"
    ),
    "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json": (
        "988f364bd1e6943178238c072e725de01af36452ef25d179eae6aef4000f7916"
    ),
    "cm2-gate34-collision-srb-kac-return-baseline-manifest-2026-07-18.json": (
        "1213a6b66fca6d3a776a75244c334dacfeb822240f7c7eeadcb565553e62a53a"
    ),
}

CLOSED_A = Q(360134800, 360493663)
CLOSED_B = Q(2 * 10**90)
C_P = Q(4 * 10**90 * 360493663, 358863)
HALF_BLOCK = 696
ETA = Q(1, 4176)
RATIONAL_EXP_BASE = Q(6, 5)
CP_FLOOR_LOG2 = 310
DEFECT_OFFSET = 309


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
    round50 = load(
        "cm2-gate34-round50-physical-whole-family-grouping-manifest-2026-07-19.json"
    )["result"]
    grouping = round50["physical_Borel_whole_family_grouping"]
    proper = round50["recordwise_properization_and_common_parent_law"]
    if grouping["status"] != (
        "CERTIFIED_PHYSICAL_BOREL_WHOLE_STANDARD_FAMILY_GROUPING_WITH_RECORDWISE_FINITE_J"
    ):
        raise RuntimeError("Round50 grouping")
    if grouping["kernel_partition_identities_mod_null"] != [
        "sum_{k,j}K_fw(y,k,j;A)=K_par(y,A)",
        "sum_{k,j}K_rev(y,k,j;A)=K_par(y,A)",
    ]:
        raise RuntimeError("Round50 one-charge partitions")
    if grouping["physical_full_registry_reconstructed"] is not True:
        raise RuntimeError("Round50 physical reconstruction")
    if proper["raw_K_par_is_a_proper_whole_family"] is not False:
        raise RuntimeError("Round50 raw properness correction")
    if "measure-preserving" not in proper["recordwise_conclusion"]:
        raise RuntimeError("Round50 proper pushforwards")
    if proper["common_preproperization_clock"] != "R0(y)=696*Dbar(M(y))":
        raise RuntimeError("Round50 preclock")
    if proper["Borel_stopped_kernel_reason"] != (
        "Dbar is integer-valued Borel, so the stopped pushforward is the countable Borel union over {Dbar=d}"
    ):
        raise RuntimeError("Round50 stopped Borel kernel")
    if round50["strict_nonpromotion"]["global_preproperization_clock_moment"] != (
        "NOT_CERTIFIED"
    ):
        raise RuntimeError("Round50 moment frontier")

    round49 = load(
        "cm2-gate34-round49-sharp-common-law-recovery-manifest-2026-07-19.json"
    )["result"]
    shell = round49["sharp_per_orientation_whole_family_shell_theorem"]
    if shell["status"] != "CERTIFIED_CONDITIONAL_SHARP_WHOLE_FAMILY_SHELL_THEOREM":
        raise RuntimeError("Round49 shell theorem")
    if shell["sharp_clock"] != "C_sigma(H,k)=H+696*(318+k)=H+221328+696*k":
        raise RuntimeError("Round49 post clock")
    if shell["eta"] != "1/4176" or shell["fixed_H_scope"] is not True:
        raise RuntimeError("Round49 exponent scope")
    if shell["postcut_whole_survivor_inheritance"] != (
        "H_sigma(y) is the whole killed survivor family and Round47 gives Z(H_sigma)<=P*p(y) with P<2^317"
    ):
        raise RuntimeError("Round49 per-view envelope")
    common = round49["same_ID_common_parent_law_W_r_theorem"]
    if common["pointwise_once_charge"] != (
        "W_r^r<=1+1_Sfw*exp(C_fw/4176)+1_Srev*exp(C_rev/4176)"
    ):
        raise RuntimeError("Round49 max inequality")

    round35 = load(
        "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json"
    )["result"]
    pair = round35["common_forward_reverse_carrier_pair"]
    if pair["actual_parameterized_common_fw_rev_carrier_pair_registry"] != "CERTIFIED":
        raise RuntimeError("Round35 carrier pair")
    if pair["forward_and_reverse_share_identical_component_and_restriction"] is not True:
        raise RuntimeError("Round35 same restriction")
    if pair["forward_and_reverse_are_two_views_not_two_charges"] is not True:
        raise RuntimeError("Round35 once charge")
    if pair["equality_reason"] != "branch area preservation and billiard time reversibility":
        raise RuntimeError("Round35 view mass transport")

    round27 = load(
        "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json"
    )["result"]
    component = round27["canonical_regular_connected_component_schema"]
    if component["componentwise_forward_map_is_real_analytic_local_diffeomorphism"] is not True:
        raise RuntimeError("Round27 component branch")
    if component["componentwise_inverse_map_exists_on_regular_image"] is not True:
        raise RuntimeError("Round27 inverse branch")
    if component["collision_area_Jacobian_of_full_invertible_map"] != "1":
        raise RuntimeError("Round27 Jacobian")

    kac = load(
        "cm2-gate34-collision-srb-kac-return-baseline-manifest-2026-07-18.json"
    )["result"]["frozen_measure_space_contract"]
    if kac["map_invertible_and_measure_preserving_modulo_singular_null_set"] != (
        "standard_collision_map_theorem_on_the_frozen_fixed_configuration"
    ):
        raise RuntimeError("collision map isomorphism")
    if kac["regular_collision_step_coverage"] != "1_modulo_collision-SRB_null":
        raise RuntimeError("regular full mass")
    if "mu_s-null" not in kac["singular_orbit_cemetery"]:
        raise RuntimeError("singular cemetery")


def safe_defect(M: int) -> int:
    """The exact Round-50 safe common defect."""
    if M < 0:
        raise ValueError("M must be nonnegative")
    ratio = Q(2**M)
    if ratio <= C_P:
        return 0
    defect = 1
    while Q(1, 2**defect) * ratio >= C_P / 2:
        defect += 1
    return defect


def view_map_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for M in (0, 14, 310, 311, 319, 400):
        defect = safe_defect(M)
        rows.append(
            {
                "minimum_length_rank_M": M,
                "safe_defect_Dbar": defect,
                "stopped_time_R0": HALF_BLOCK * defect,
                "forward_view_map": f"P_fw=T_s^{HALF_BLOCK * defect} o V_fw",
                "reverse_view_map": f"P_rev=T_s^{HALF_BLOCK * defect} o V_rev",
                "inverse_time_exponent": -(HALF_BLOCK * defect),
            }
        )
    return rows


def two_proper_view_object_lemma() -> dict[str, Any]:
    rows = view_map_rows()
    assert CLOSED_B / (1 - CLOSED_A) == C_P / 2
    assert Q(2**CP_FLOOR_LOG2) < C_P < Q(2 ** (CP_FLOOR_LOG2 + 1))
    return {
        "raw_finite_law": (
            "m_raw(dy,dx)=lambda(dy)K_par(y,dx), with K_par(y,X)=p(y) and integral p dlambda<infinity"
        ),
        "raw_geometry_is_proper": False,
        "common_raw_record": (
            "one Round50 rn-whole-family ID y and one half-open-owned physical source point x; fw/rev partitions sum to this same K_par modulo the frozen null boundary"
        ),
        "initial_view_maps": {
            "V_fw": "the forward starting view of the Round35 common physical restriction",
            "V_rev": "I o H applied to the same source restriction, the reverse starting view I(B)",
            "H": "T_s^n on one regular component, with a real-analytic inverse on its image",
            "I": "the billiard time-reversal Borel involution",
        },
        "full_measure_regular_domain": (
            "remove the stopped-orbit singular preimages in both orientations; their countable Borel union over integer stopping strata is m_raw-null by the collision-SRB null theorem and the exact Round50 outer disintegration, and is assigned to the pre-existing singular cemetery"
        ),
        "stopped_view_maps": [
            "P_fw(y,x)=T_s^(696*Dbar(y))(V_fw(y,x))",
            "P_rev(y,x)=T_s^(696*Dbar(y))(V_rev(y,x))",
        ],
        "fibrewise_inverse_maps": [
            "P_fw^-1=V_fw^-1 o T_s^(-696*Dbar)",
            "P_rev^-1=V_rev^-1 o T_s^(-696*Dbar)"
        ],
        "Borel_isomorphism_reason": (
            "Dbar is integer-valued Borel; on each {Dbar=d}, H, I, and every finite regular T_s iterate and inverse are Borel.  Keeping y makes each map injective; Lusin-Souslin gives Borel images and Borel inverses"
        ),
        "measure_transport": (
            "K_sigma_star(y,.)=(P_sigma(y,.))_#K_par(y,.); hence P_sigma is a measure-space isomorphism modulo its null domain and K_sigma_star(y,X_sigma)=p(y)"
        ),
        "physical_measure_compatibility": (
            "after outer disintegration, H, I, and T_s preserve collision-SRB mass; the pushforward construction additionally gives the fibrewise integral identity by definition"
        ),
        "proper_view_conclusion": (
            "both K_fw_star and K_rev_star are whole proper standard-family kernels after their own 696*Dbar closed evolutions"
        ),
        "cuts_change_point_map_or_charge": False,
        "cut_policy": (
            "natural/image recuts only label half-open components of the pushforward; they neither duplicate nor normalize physical mass"
        ),
        "same_ID_once_charge": True,
        "sample_view_map_rows": rows,
        "sample_view_map_rows_sha256": digest(rows),
        "status": "CERTIFIED_PHYSICAL_BOREL_TWO_PROPER_VIEW_MEASURE_ISOMORPHISM",
    }


def selected_common_proper_law() -> dict[str, Any]:
    return {
        "selected_reference_law": (
            "m_star(dy,dz)=lambda(dy)K_fw_star(y,dz), a finite law whose fibres are proper"
        ),
        "view_transfer_map": (
            "Theta_y=P_rev,y o P_fw,y^-1 from the forward proper view to the reverse proper view"
        ),
        "Theta_is_Borel_mod_null": True,
        "Theta_pushforward_identity": "(Theta_y)_#K_fw_star(y,.)=K_rev_star(y,.)",
        "transported_reverse_predicate": (
            "S_rev_star(y,z)=S_rev(y,Theta_y(z)); zero survivors remain zero and are never normalized"
        ),
        "transported_reverse_clock": "C_rev_star(y,z)=C_rev(y,Theta_y(z))",
        "forward_predicate_and_clock": (
            "S_fw_star=S_fw and C_fw_star=C_fw on the selected forward proper view"
        ),
        "Borel_transport_reason": (
            "composition of the Round48 Borel survivor/clock functions with the Borel isomorphism Theta"
        ),
        "orientation_integral_identities": [
            "integral f_fw_star dm_star=integral f_fw(P_fw(y,x)) dm_raw",
            "integral f_rev_star dm_star=integral f_rev(P_rev(y,x)) dm_raw=integral f_rev d(lambda K_rev_star)",
        ],
        "same_restriction_ID_preserved": (
            "Theta changes only the view coordinate z and retains the outer rn-whole-family/restriction ID y"
        ),
        "separate_normalization_used": False,
        "parent_charged_once": True,
        "transported_reverse_subset_is_geometrically_proper_inside_forward_view": (
            "NOT_ASSERTED"
        ),
        "status": "CERTIFIED_SELECTED_FORWARD_PROPER_COMMON_LAW_WITH_BOREL_REVERSE_TRANSPORT",
    }


def postproperization_wr_join() -> dict[str, Any]:
    assert HALF_BLOCK * ETA == Q(1, 6)
    return {
        "scope": (
            "every fixed |s|<=1/400, finite return depth n, fixed finite terminal schedule, fixed finite terminal time H, and integer r>=1"
        ),
        "per_view_post_clock": (
            "C_sigma_post=H+221328+696*k_sigma on its own proper pushforward view"
        ),
        "per_view_envelope": (
            "Round49 gives integral 1_Ssigma*exp(C_sigma_post/4176) d(lambda K_sigma_star)<A_H*integral p dlambda"
        ),
        "A_H": "(6/5)^(318+ceil(H/696))",
        "common_reference_definition": (
            "W_r_star=max(1,1_Sfw_star*exp(C_fw_star/(4176*r)),1_Srev_star*exp(C_rev_star/(4176*r)))"
        ),
        "pointwise_once_charge": (
            "W_r_star^r<=1+1_Sfw_star*exp(C_fw_star/4176)+1_Srev_star*exp(C_rev_star/4176)"
        ),
        "integrated_bound": (
            "integral W_r_star^r dm_star<(1+2*A_H)*integral p dlambda"
        ),
        "raw_pullback_equivalent": (
            "the same W_r is obtained on m_raw by composing each orientation term with P_sigma; both descriptions charge K_par once"
        ),
        "physical_two_proper_view_join_installed": True,
        "raw_K_par_properness_used": False,
        "proper_intersection_used": False,
        "common_survivor_or_common_shell_used": False,
        "postproperization_clock_only": True,
        "status": "CERTIFIED_PHYSICAL_POSTPROPERIZATION_TWO_VIEW_W_R_ONCE_CHARGE_MOMENT",
    }


def full_clock_conditional_bridge() -> dict[str, Any]:
    return {
        "total_orientation_clock": (
            "C_sigma_total=696*Dbar+C_sigma_post"
        ),
        "total_weight": (
            "Wtilde_r_star=max(1,1_Sfw_star*exp(C_fw_total/(4176*r)),1_Srev_star*exp(C_rev_total/(4176*r)))"
        ),
        "exact_preclock_exponent": "696/4176=1/6",
        "required_same_kernel_moment": (
            "I_D=integral p(y)*exp(Dbar(y)/6) dlambda(y)<infinity"
        ),
        "conditional_integrated_bound": (
            "integral Wtilde_r_star^r dm_star<integral p dlambda+2*A_H*I_D"
        ),
        "rational_sufficient_moment": (
            "I_6over5=integral p(y)*(6/5)^Dbar(y) dlambda(y)<infinity"
        ),
        "rational_bound_reason": "exp(1/6)<6/5",
        "physical_I_D_certified": False,
        "complete_total_clock_W_r_certified": False,
        "status": "CERTIFIED_EXACT_FULL_CLOCK_FORMULA_CONDITIONAL_ON_MISSING_DEFECT_MOMENT",
    }


def exact_defect_tail_frontier() -> dict[str, Any]:
    a = RATIONAL_EXP_BASE
    assert Q(2**310) < C_P < Q(2**311)
    assert safe_defect(310) == 0
    assert all(safe_defect(M) == M - DEFECT_OFFSET for M in range(311, 420))

    # If nu(M>m)<=C*2^-m, exact layer cake for Dbar (which skips 1) gives
    # E a^Dbar <= nu(1) + (4/5)*C*2^-310.
    first_two = (a**2 - 1) * Q(1, 2**310)
    tail = Q(1, 2**309) * (a - 1) * (a / 2) ** 2 / (1 - a / 2)
    coefficient = (first_two + tail) * Q(2**310)
    assert coefficient == Q(4, 5)

    return {
        "exact_C_p_bracket": "2^310<C_p<2^311",
        "exact_defect_formula": [
            "Dbar(M)=0 for 0<=M<=310",
            "Dbar(M)=M-309 for every integer M>=311; in particular Dbar never equals 1",
        ],
        "unconditional_finite_ae": True,
        "strongest_unconditional_tail": (
            "because M and Dbar are finite Borel functions on the finite grouped law, mass{M>m}->0 and mass{Dbar>d}->0 by continuity from above"
        ),
        "quantitative_rate_from_current_fields": "NONE_CERTIFIED",
        "target_physical_tail": (
            "mass{M>m}=integral_{M>m}p dlambda<=C_len*2^-m for every integer m>=0"
        ),
        "target_tail_available": False,
        "exact_Dbar_layer_cake": (
            "integral (6/5)^Dbar p=mass_total+sum_{d>=0}((6/5)^(d+1)-(6/5)^d)*mass{Dbar>d}"
        ),
        "conditional_sharp_bound_from_target_tail": (
            "integral (6/5)^Dbar p<=mass_total+(4/5)*C_len*2^-310"
        ),
        "conditional_bound_coefficient": "(4/5)*2^-310",
        "therefore_exp_bound": (
            "integral exp(Dbar/6)p<=mass_total+(4/5)*C_len*2^-310"
        ),
        "truncated_exhaustion_bound": (
            "on {M<=L}, integral exp(Dbar/6)p<=(6/5)^max(0,L-309)*mass_total"
        ),
        "status": "CERTIFIED_EXACT_DEFECT_FORMULA_AND_CONDITIONAL_SHORT_TAIL_BRIDGE",
    }


def short_tail_nonimplication() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for n in (19, 20, 21, 22, 24):
        M = n * n
        defect = safe_defect(M)
        rows.append(
            {
                "band_n": n,
                "band_mass": f"2^-{n}",
                "group_count": f"2^{M}",
                "group_length": f"2^-{M}",
                "minimum_length_rank_M": M,
                "safe_defect_Dbar": defect,
                "tail_test_m": M - 1,
                "mass_over_2^-m_lower_ratio": f"2^{M-n-1}",
                "rational_moment_band_term": f"2^-{n}*(6/5)^{defect}",
            }
        )
    return {
        "construction": (
            "on disjoint b-bands of mass 2^-n, split a unit fibre into 2^(n^2) equal source intervals of length 2^(-n^2), take the reverse view and partition identical to the forward view, and use uniform area density with fixed incidence rank B=14"
        ),
        "compatibility_with_current_abstract_fields": (
            "finite total physical mass, standard-Borel countable grouping, finite cells per group, positive lengths, fixed D1 rank density, and recordwise finite J"
        ),
        "natural_recut_scope": (
            "for n>=19 these source intervals are shorter than 1e-90, so each is a single clipped endpoint cell; the example does not rely on infinitely many recuts inside one group"
        ),
        "tail_lower_test": (
            "at m=n^2-1, mass{M>m}>=2^-n, so any constant in mass{M>m}<=C_len*2^-m must satisfy C_len>=2^(n^2-n-1)"
        ),
        "linear_tail_consequence": "no finite C_len works in this model",
        "defect_moment_failure": (
            "Dbar(n^2)=n^2-309 and 2^-n*(6/5)^Dbar does not tend to zero"
        ),
        "even_required_exponential_moment_failure": (
            "exp(1/6)>7/6, so 2^-n*exp(Dbar/6)>=2^-n*(7/6)^Dbar does not tend to zero"
        ),
        "logical_scope": (
            "a nonimplication model for the fields currently certified, not a claim that actual billiard fibres realize this partition"
        ),
        "actual_billiard_short_tail_disproved": False,
        "rows": rows,
        "rows_sha256": digest(rows),
        "status": "CERTIFIED_EXACT_CURRENT_FIELDS_DO_NOT_IMPLY_SHORT_ENDPOINT_RATE",
    }


def intersection_and_gate_frontier() -> dict[str, Any]:
    return {
        "Borel_same_raw_point_joint_predicate": (
            "S_fw(P_fw(y,x)) and S_rev(P_rev(y,x)) can be intersected measurably on m_raw"
        ),
        "joint_predicate_is_a_proper_standard_family": "NOT_CERTIFIED",
        "reason": (
            "the two-proper-view lemma transports integrals, not boundary geometry; a thin overlap can have unbounded normalized Z even when both ambient views are proper"
        ),
        "proper_common_fw_rev_return": "NOT_CERTIFIED",
        "numeric_H_cover_and_actual_beta": "NOT_CERTIFIED",
        "complete_numeric_C_fw_C_rev": "NOT_CERTIFIED",
        "collision_time_q": "NOT_CERTIFIED",
        "strong_trace_current_cemetery": "NOT_CERTIFIED",
        "weak_mass_cemetery_inherited": "CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "CM2": "NO-GO_FOR_CLAIM",
        "status": "CERTIFIED_MEASURE_TRANSPORT_DOES_NOT_PROMOTE_GEOMETRIC_INTERSECTION_OR_GATE4",
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "parameter_scope": "parameterwise for every fixed |s|<=1/400",
            "depth_scope": "every fixed finite first-return depth n",
            "claim_type": (
                "physical two-proper-view measure transport, once-charge postproperization W_r join, and exact short-endpoint moment frontier"
            ),
        },
        "physical_two_proper_view_object_lemma": two_proper_view_object_lemma(),
        "selected_forward_proper_common_law": selected_common_proper_law(),
        "physical_postproperization_W_r_join": postproperization_wr_join(),
        "full_clock_conditional_bridge": full_clock_conditional_bridge(),
        "exact_defect_and_short_tail_frontier": exact_defect_tail_frontier(),
        "short_tail_nonimplication": short_tail_nonimplication(),
        "intersection_and_gate_frontier": intersection_and_gate_frontier(),
        "corrected_frontier": {
            "raw_K_par_proper": False,
            "physical_two_proper_view_pullback_lemma": "CERTIFIED",
            "selected_forward_proper_common_law": "CERTIFIED",
            "postproperization_same_ID_once_charge_W_r": "CERTIFIED_FIXED_H",
            "raw_parent_charged_once": True,
            "physical_preproperization_defect_exponential_moment": "NOT_CERTIFIED",
            "full_total_clock_common_law_Lp_join": "CONDITIONAL_NOT_CLOSED",
            "physical_linear_short_endpoint_tail": "NOT_CERTIFIED",
            "proper_common_fw_rev_intersection": "NOT_CERTIFIED",
            "complete_numeric_C_fw_C_rev_q": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
        },
        "strict_nonpromotion": {
            "two_proper_view_measure_isomorphism": "CERTIFIED",
            "postproperization_same_ID_common_parent_law": "CERTIFIED_MEASURE_THEORETIC_FIXED_H",
            "global_preproperization_clock_moment": "NOT_CERTIFIED",
            "full_total_clock_W_r": "CONDITIONAL_NOT_CLOSED",
            "proper_common_intersection": "NOT_CERTIFIED",
            "full_numeric_C_fw_C_rev": "NOT_CERTIFIED",
            "numeric_collision_time_q": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
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
    result = build_result()
    strict = result["strict_nonpromotion"]
    print("TWO_PROPER_VIEW:", strict["two_proper_view_measure_isomorphism"])
    print("POSTPROPERIZATION_W_R:", strict["postproperization_same_ID_common_parent_law"])
    print("FULL_CLOCK_MOMENT:", strict["global_preproperization_clock_moment"])
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
