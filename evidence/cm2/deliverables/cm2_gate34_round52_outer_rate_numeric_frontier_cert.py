#!/usr/bin/env python3
"""Round-52 Gate-4 proof-level outer-rate numerical frontier.

Round 51 obtained a uniform but nonnumerical smooth-bump hit time.  This
certificate reopens the proof of Stenlund--Young--Zhang (SYZ), rather than
treating its final ``C, theta exist'' statement as a black box.  Once both
comparison measures are represented by proper regular unstable families,
the proof gives an outer prefactor and rate in terms of four constants:
``tilde_zeta, Delta, hat_c, Lambda``.  The last two are already numerical in
the frozen pilot.  For a Lipschitz observable the outer prefactor is therefore
exactly bounded by 3807/10, and only a positive numerical lower bound for the
magnet coupling fraction ``tilde_zeta`` and a finite numerical upper bound for
the coupling gap ``Delta`` remain in the rate.

The final displayed SYZ rate writes ``Lambda^(-gamma)/2``, while the
immediately preceding estimate is ``Lambda^(-gamma*n/2)``.  We do not use the
faster printed expression.  We independently extract the safe nth-root rate
``Lambda^(-gamma/2)`` and round it upward to 9/10 for gamma=1.

This does not numericalise tilde_zeta or Delta, does not turn the whole-family
bump hit into a proper-crossing leaf atlas, and does not certify H_cover,
beta, Gate 4, or CM2.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate34.round52-outer-rate-numeric-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate34-round52-outer-rate-numeric-frontier-manifest-2026-07-20.json"
)

DEPENDENCIES = {
    "cm2-gate34-round51-uniform-gauge-bump-frontier-manifest-2026-07-20.json": (
        "4248c215821ba6e23eb78c64158b1301e1b33d964fb0cd024e4b8e4427247b21"
    ),
    "cm2_gate34_round51_uniform_gauge_bump_frontier_cert.py": (
        "944493692aec2a48f9151f631672bef68956e84d85a35a257f6af0bebb2514ce"
    ),
    "cm2-gate4-numeric-growth-leaves-frontier-manifest-2026-07-16.json": (
        "4e0c8216892afe9ce0c19e22b9ecc5742f21e9e4512d949b88325e1ee1ff70d5"
    ),
    "cm2-gate34-c24-open-hole-geometry-manifest-2026-07-18.json": (
        "f0521bb84fc5b1c824d8361d375013aff024a89460cbc439f5aa7a04d7525183"
    ),
    "cm2_gate25_physical_return_core_registry_cert.py": (
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"
    ),
    "cm2-gate34-round51-two-proper-view-common-law-manifest-2026-07-20.json": (
        "028c5a8f59a6efffa9df93cfba841f3844d244988dc235038183eef222d21abc"
    ),
}

ARXIV_1210_ARCHIVE_SHA256 = (
    "b705ed4fc89a42ac8e78957d65873211c71f9566599bfba90173812fe5ffe5c5"
)
ARXIV_1210_MAIN_TEX_SHA256 = (
    "921fe3477c2f3280a256a459c9e2a2bc6b719a971016a8320e6d0d5e9cd25f44"
)
ARXIV_2606_ARCHIVE_SHA256 = (
    "d568ad1351593e1d33d7855079583dd28d3c1ff6a26f673ca01ebc2784c132a6"
)
ARXIV_2606_MAIN_TEX_SHA256 = (
    "e2b8cb694664ca74d88883e9daf65997d39d395619365776ff59ab98b4574c50"
)

HIT_GAP = Q(21, 111718750)
BUMP_NORM = Q(2724)
SAFE_FAMILY_MASS = Q(1999, 32000)
DIRECT_REQUIRED_FRACTION = Q(2688, 893303125)
HAT_C = Q(20, 3807)
LAMBDA = Q(180337, 144000)
SAFE_HYPERBOLIC_RATE = Q(9, 10)
OUTER_C = Q(3807, 10)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"duplicate key: {key}")
        value[key] = item
    return value


def reject_json_constant(token: str) -> None:
    raise ValueError(f"non-finite JSON constant: {token}")


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def load_json(name: str) -> dict[str, Any]:
    path = HERE / name
    if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
        raise RuntimeError(f"unsafe dependency: {name}")
    if sha(path) != DEPENDENCIES[name]:
        raise RuntimeError(f"dependency hash: {name}")
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_object,
        parse_constant=reject_json_constant,
    )
    if not isinstance(value, dict):
        raise RuntimeError(f"dependency root: {name}")
    return value


def checked_text(name: str, tokens: tuple[str, ...]) -> str:
    path = HERE / name
    if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
        raise RuntimeError(f"unsafe source dependency: {name}")
    if sha(path) != DEPENDENCIES[name]:
        raise RuntimeError(f"source dependency hash: {name}")
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        if token not in text:
            raise RuntimeError(f"source token {name}: {token}")
    return text


def validate_dependencies() -> dict[str, Any]:
    r51 = load_json(
        "cm2-gate34-round51-uniform-gauge-bump-frontier-manifest-2026-07-20.json"
    )
    if r51.get("schema") != (
        "cm2.gate34.round51-uniform-gauge-bump-frontier.v1.manifest.v1"
    ):
        raise RuntimeError("Round51 schema")
    result51 = r51["result"]
    bump = result51["uniform_standard_family_bump_minorisation"]
    if bump["status"] != "CERTIFIED_UNIFORM_EXISTENTIAL_TIME_WITH_NUMERIC_HIT_FRACTION":
        raise RuntimeError("Round51 bump status")
    if Q(bump["actual_whole_family_C24_hit_fraction_strict_lower_at_H_bump"]) != HIT_GAP:
        raise RuntimeError("Round51 hit gap")
    if bump["uniform_bump_theorem_norm"] != "norm_infinity(g)+Lipschitz_1(g)<2724":
        raise RuntimeError("Round51 bump norm")
    if any(bump[key] is not None for key in ("numeric_C_bump", "numeric_theta_bump", "numeric_H_bump")):
        raise RuntimeError("Round51 numerical scope")
    frontier51 = result51["cover_effectivity_frontier"]
    if frontier51["strict_inferable_uniform_cover_source_fraction_lower"] != "0":
        raise RuntimeError("Round51 cover fraction")
    if frontier51["numeric_H_cover"] is not None:
        raise RuntimeError("Round51 H_cover")
    rows51 = result51["literature_quantifier_audit"]["rows"]
    syz_rows = [row for row in rows51 if row["paper"].startswith("Stenlund--Young--Zhang")]
    if len(syz_rows) != 1:
        raise RuntimeError("Round51 SYZ row")
    if syz_rows[0]["official_source_sha256"] != ARXIV_1210_ARCHIVE_SHA256:
        raise RuntimeError("SYZ archive hash")
    if syz_rows[0]["main_tex_member_sha256"] != ARXIV_1210_MAIN_TEX_SHA256:
        raise RuntimeError("SYZ TeX hash")

    checked_text(
        "cm2_gate34_round51_uniform_gauge_bump_frontier_cert.py",
        (
            "ARXIV_1210_MAIN_TEX_SHA256",
            "one_uniform_finite_integer_H_bump_exists",
            "numeric_H_bump\": None",
            "strict_inferable_uniform_cover_source_fraction_lower\": \"0",
        ),
    )

    growth = load_json(
        "cm2-gate4-numeric-growth-leaves-frontier-manifest-2026-07-16.json"
    )
    replay = growth["replay_summary"]
    if Q(replay["c_hat"]) != HAT_C:
        raise RuntimeError("numeric hat_c")
    if Q(replay["Lambda"]) != LAMBDA:
        raise RuntimeError("numeric Lambda")
    if growth["verdict"]["numeric_adapted_metric_hyperbolicity_leaves"] != "CERTIFIED":
        raise RuntimeError("hyperbolicity status")

    hole = load_json(
        "cm2-gate34-c24-open-hole-geometry-manifest-2026-07-18.json"
    )["result"]
    if hole["frozen_core_inventory"]["core_count"] != 24:
        raise RuntimeError("C24 core count")
    if hole["collision_SRB_core_mass_interval"][
        "normalized_core_mass_strict_upper_simplification"
    ] != "1/2500":
        raise RuntimeError("C24 mass upper")
    checked_text(
        "cm2_gate25_physical_return_core_registry_cert.py",
        (
            "AXIS_T_LOWER = Q(1, 100)",
            "AXIS_T_UPPER = Q(1, 50)",
            "AXIS_P_HALF_WIDTH = Q(1, 500)",
            "DIAGONAL_T_LOWER = Q(69, 100)",
            "DIAGONAL_T_UPPER = Q(7, 10)",
            "DIAGONAL_P_HALF_WIDTH = Q(1, 50)",
        ),
    )

    two_view = load_json(
        "cm2-gate34-round51-two-proper-view-common-law-manifest-2026-07-20.json"
    )["result"]
    lemma = two_view["physical_two_proper_view_object_lemma"]
    reference = two_view["selected_forward_proper_common_law"]
    if lemma["same_ID_once_charge"] is not True:
        raise RuntimeError("two-view same ID")
    if "both K_fw_star and K_rev_star are whole proper" not in lemma[
        "proper_view_conclusion"
    ]:
        raise RuntimeError("two-view properness")
    if reference["parent_charged_once"] is not True:
        raise RuntimeError("two-view once charge")
    if reference["Theta_pushforward_identity"] != (
        "(Theta_y)_#K_fw_star(y,.)=K_rev_star(y,.)"
    ):
        raise RuntimeError("two-view pushforward")
    return {
        "round51": result51,
        "growth": growth,
        "hole": hole,
        "two_view": two_view,
    }


def conditional_block_time(zeta_lower: Q, delta_upper: int) -> dict[str, Any]:
    """Exact safe arithmetic interface once the two missing scalars exist.

    Taking H=2*delta_upper*m avoids any numerical evaluation of roots or
    logarithms.  Both comparisons below are rational and strict.
    """

    if not (0 < zeta_lower < 1):
        raise ValueError("zeta_lower")
    if not isinstance(delta_upper, int) or delta_upper < 1:
        raise ValueError("delta_upper")
    scale = BUMP_NORM * OUTER_C
    coupling_base = 1 - zeta_lower / 2
    m = 0
    while not (
        scale * coupling_base**m < HIT_GAP
        and scale * SAFE_HYPERBOLIC_RATE ** (2 * delta_upper * m) < HIT_GAP
    ):
        m += 1
    previous_passes = m > 0 and (
        scale * coupling_base ** (m - 1) < HIT_GAP
        and scale
        * SAFE_HYPERBOLIC_RATE ** (2 * delta_upper * (m - 1))
        < HIT_GAP
    )
    return {
        "zeta_lower": str(zeta_lower),
        "Delta_upper": delta_upper,
        "coupling_base_upper": str(coupling_base),
        "minimal_safe_block_count_m": m,
        "safe_collision_time_H": 2 * delta_upper * m,
        "coupling_branch_majorant_at_H": str(scale * coupling_base**m),
        "hyperbolic_branch_majorant_at_H": str(
            scale * SAFE_HYPERBOLIC_RATE ** (2 * delta_upper * m)
        ),
        "previous_block_passes_both_strict_tests": previous_passes,
    }


def proof_level_outer_rate() -> dict[str, Any]:
    assert 0 < HAT_C < 1 < LAMBDA
    assert 1 / HAT_C == Q(3807, 20) > 2
    assert OUTER_C == 2 / HAT_C
    assert 1 / LAMBDA < SAFE_HYPERBOLIC_RATE**2
    return {
        "official_source": {
            "paper": "Stenlund--Young--Zhang, arXiv:1210.0011v4",
            "whole_archive_sha256": ARXIV_1210_ARCHIVE_SHA256,
            "main_member": "Moving_final.tex",
            "main_member_sha256": ARXIV_1210_MAIN_TEX_SHA256,
            "proof_anchors": (
                "proper-start coupling bookkeeping at source lines 2636--2707; observable estimate and displayed outer constants at lines 2720--2769"
            ),
        },
        "proper_start_scope_reduction": {
            "canonical_input": (
                "Round51 starts from a normalized canonical proper family with finite numeric Z and dynamic log-density constant at most 2e27"
            ),
            "threshold_enlargement": (
                "the paper's finite regularity and properness thresholds may be enlarged to contain the frozen input constants; this preserves the relevant upper inequalities, while the resulting loss is absorbed into tilde_zeta and Delta"
            ),
            "comparison_law": (
                "Lemma 1'implies1 gives the common invariant collision law a finite-Z regular unstable representation; invariance plus eventual properness means that the same law admits a proper representation"
            ),
            "no_numeric_regularisation_shift_added_to_H": True,
            "reason": (
                "the proof may begin with proper representations of the same two laws; changing the allowed thresholds changes the hidden coupling geometry, not the outer hyperbolicity prefactor"
            ),
            "status": "CERTIFIED_EXISTENTIAL_PROPER_REPRESENTATION_REDUCTION",
        },
        "proof_level_formula_gamma_1": {
            "published_outer_prefactor_formula": (
                "C_1=2*max((1-tilde_zeta/2)^(-1),hat_c^(-1))"
            ),
            "published_coupling_rate_branch": (
                "(1-tilde_zeta/2)^(1/(2*Delta))"
            ),
            "immediately_preceding_hyperbolic_decay": (
                "2*Lip_1(f)*hat_c^(-1)*Lambda^(-n/2)"
            ),
            "printed_final_hyperbolic_factor": "Lambda^(-1)/2",
            "safe_extracted_hyperbolic_rate": "Lambda^(-1/2)",
            "printed_factor_used": False,
            "rate_guard": (
                "Lambda^(-n/2) has nth-root Lambda^(-1/2); the faster printed Lambda^(-1)/2 is not inferred from the preceding estimate"
            ),
        },
        "numeric_hyperbolicity": {
            "hat_c": str(HAT_C),
            "Lambda": str(LAMBDA),
            "Lambda_inverse": str(1 / LAMBDA),
            "rational_square_comparison": "14400000<14607297=81*180337",
            "safe_Lambda_inverse_square_root_upper": str(SAFE_HYPERBOLIC_RATE),
        },
        "numeric_outer_prefactor": {
            "coupling_prefactor_strict_upper_for_0_lt_zeta_lt_1": "2",
            "hat_c_inverse": str(1 / HAT_C),
            "C_bump_proof_outer_upper": str(OUTER_C),
            "status": "CERTIFIED_NUMERIC_PROOF_OUTER_PREFACTOR",
        },
        "safe_rate_with_two_hidden_scalars": (
            "theta_safe=max((1-tilde_zeta/2)^(1/(2*Delta)),9/10)"
        ),
        "status": "CERTIFIED_NUMERIC_OUTER_PREFACTOR_AND_TWO_SCALAR_RATE_REDUCTION",
    }


def two_scalar_effectivity_interface() -> dict[str, Any]:
    sample = conditional_block_time(Q(1, 2), 1)
    assert sample["minimal_safe_block_count_m"] == 140
    assert sample["safe_collision_time_H"] == 280
    assert sample["previous_block_passes_both_strict_tests"] is False
    scale_ratio = BUMP_NORM * OUTER_C / HIT_GAP
    assert scale_ratio == Q(38618445937500, 7)
    rows = [
        {
            "id": "tilde_zeta_lower",
            "meaning": (
                "one explicit positive lower bound for the minimum proper-family magnet coupling fraction after the compatible threshold enlargement"
            ),
            "value": None,
        },
        {
            "id": "Delta_upper",
            "meaning": (
                "one explicit finite integer upper bound for the maximum gap between coupling times, including mixing, recovery, and compact-configuration scheduling"
            ),
            "value": None,
        },
    ]
    return {
        "known_exact_scale_ratio_2724_C_over_epsilon": str(scale_ratio),
        "missing_rate_scalars": rows,
        "missing_rate_scalars_sha256": digest(rows),
        "exact_conditional_integer_interface": (
            "given 0<zeta0<=tilde_zeta and Delta<=D, choose the least m with (2724*3807/10)*(1-zeta0/2)^m<epsilon_hit and (2724*3807/10)*(9/10)^(2*D*m)<epsilon_hit; then H=2*D*m is safe"
        ),
        "formal_arithmetic_sample_not_a_physical_claim": sample,
        "numeric_tilde_zeta_lower": None,
        "numeric_Delta_upper": None,
        "numeric_H_bump": None,
        "status": "TWO_SCALAR_EFFECTIVITY_INTERFACE_EXACT_BUT_INPUTS_NOT_NUMERIC",
    }


def uniform_C24_outer_majorant() -> dict[str, Any]:
    """Construct a common Lipschitz majorant of all twenty-four C24 boxes."""

    axis_dt = Q(1, 1000)
    axis_dp = Q(1, 1000)
    diagonal_dt = Q(1, 1000)
    diagonal_dp = Q(1, 100)
    # The pinned registry has four axis rows per source and, for each source,
    # four positive-t plus four negative-t diagonal rows.  We record the six
    # aggregate types rather than importing the flint-based geometry replay;
    # its source and already replayed row digest are pinned dependencies.
    rows = [
        {
            "family": "axis_translate",
            "source": source,
            "radius": radius,
            "count": 4,
            "plateau_t": ["1/100", "1/50"],
            "plateau_p": ["-1/500", "1/500"],
            "support_t": ["9/1000", "21/1000"],
            "support_p": ["-3/1000", "3/1000"],
        }
        for source, radius in (("G", "9/25"), ("W", "4/25"))
    ]
    for source, radius in (("G", "9/25"), ("W", "4/25")):
        rows.extend(
            [
                {
                    "family": "diagonal_positive_t",
                    "source": source,
                    "radius": radius,
                    "count": 4,
                    "plateau_t": ["69/100", "7/10"],
                    "plateau_p": ["-1/50", "1/50"],
                    "support_t": ["689/1000", "701/1000"],
                    "support_p": ["-3/100", "3/100"],
                },
                {
                    "family": "diagonal_negative_t",
                    "source": source,
                    "radius": radius,
                    "count": 4,
                    "plateau_t": ["-7/10", "-69/100"],
                    "plateau_p": ["-1/50", "1/50"],
                    "support_t": ["-701/1000", "-689/1000"],
                    "support_p": ["-3/100", "3/100"],
                },
            ]
        )

    assert sum(row["count"] for row in rows if row["family"] == "axis_translate") == 8
    assert sum(row["count"] for row in rows if row["family"].startswith("diagonal_")) == 16
    axis_base = Q(117, 781250)
    diagonal_base = Q(234, 78125)
    replay_axis_base = (
        4 * (Q(9, 25) + Q(4, 25)) * Q(3, 250) * Q(3, 500)
    )
    replay_diagonal_base = (
        8 * (Q(9, 25) + Q(4, 25)) * Q(3, 250) * Q(3, 50)
    )
    assert replay_axis_base == axis_base
    assert replay_diagonal_base == diagonal_base

    # On the padded supports, dtheta/dt=(1-t^2)^(-1/2).
    axis_t_abs = Q(21, 1000)
    diagonal_t_abs = Q(701, 1000)
    axis_dtheta = Q(1001, 1000)
    diagonal_dtheta = Q(141, 100)
    assert axis_dtheta**2 * (1 - axis_t_abs**2) > 1
    assert diagonal_dtheta**2 * (1 - diagonal_t_abs**2) > 1
    raw_upper = axis_base * axis_dtheta + diagonal_base * diagonal_dtheta
    assert raw_upper == Q(3416517, 781250000)
    normalization_lower = 4 * Q(3) * (Q(9, 25) + Q(4, 25))
    assert normalization_lower == Q(156, 25)
    normalized_upper = raw_upper / normalization_lower
    assert normalized_upper == Q(87603, 125000000) < Q(1, 1000)

    # Each one-dimensional trapezoid is one on the plateau and decreases
    # linearly to zero across its padding.  The product has coordinate
    # Lipschitz cost at most the sum of the two reciprocal paddings.
    # Since |dt/dr|<=1/R<=25/4 and |dp/dphi|<=1, every axis product has
    # physical Lip_1<7250 and every diagonal product has Lip_1<6350.
    # A finite maximum preserves the maximum Lipschitz constant.
    axis_lipschitz = Q(25, 4) / axis_dt + 1 / axis_dp
    diagonal_lipschitz = Q(25, 4) / diagonal_dt + 1 / diagonal_dp
    assert axis_lipschitz == 7250
    assert diagonal_lipschitz == 6350
    theorem_norm_upper = Q(7251)

    return {
        "construction": {
            "one_box_function": (
                "product of the two piecewise-linear trapezoids that equal one on the closed C24 coordinate rectangle and taper to zero across the displayed t,p padding"
            ),
            "global_function": "g_out=max of the twenty-four one-box products",
            "pointwise_relation": "1_C24<=g_out<=1",
            "parameter_uniformity": (
                "the intrinsic fixed-label (r,phi) gauge and all plateau/support coordinates are independent of s"
            ),
            "axis_padding": {"t": str(axis_dt), "p": str(axis_dp)},
            "diagonal_padding": {
                "t": str(diagonal_dt),
                "p": str(diagonal_dp),
            },
            "box_rows": rows,
            "box_rows_sha256": digest(rows),
        },
        "support_mass": {
            "axis_padded_unnormalized_base": str(axis_base),
            "diagonal_padded_unnormalized_base": str(diagonal_base),
            "axis_abs_t_upper": str(axis_t_abs),
            "diagonal_abs_t_upper": str(diagonal_t_abs),
            "axis_dtheta_dt_strict_upper": str(axis_dtheta),
            "diagonal_dtheta_dt_strict_upper": str(diagonal_dtheta),
            "padded_union_unnormalized_mass_strict_upper_by_sum": str(raw_upper),
            "normalization_strict_lower_using_pi_gt_3": str(normalization_lower),
            "mu_s_support_strict_upper": str(normalized_upper),
            "mu_s_g_out_strict_upper": str(normalized_upper),
            "simple_uniform_upper": "1/1000",
        },
        "Lipschitz_bound": {
            "coordinate_relations": (
                "t=sin(boundary-normal angle), p=sin(phi), so abs(dt/dr)<=1/R<=25/4 and abs(dp/dphi)<=1"
            ),
            "axis_Lip_1_upper": str(axis_lipschitz),
            "diagonal_Lip_1_upper": str(diagonal_lipschitz),
            "finite_max_preserves_maximum_Lipschitz_constant": True,
            "norm_infinity_plus_Lip_1_strict_upper": str(theorem_norm_upper),
        },
        "uniform_existential_small_terminal_hit": {
            "normalization_scope": (
                "all displayed terminal masses in this subsection are fractions of the normalized proper-view/once-charged parent law; for parent mass p the absolute common nonhit mass is >249*p/250"
            ),
            "mixing_test": (
                "use the same proper-family SYZ comparison with g_out and choose one common finite H_out so that the error is strictly below 1/1000"
            ),
            "numeric_H_out": None,
            "per_proper_view_terminal_C24_mass_strict_upper": "1/500",
            "per_proper_view_terminal_nonhit_mass_strict_lower": "499/500",
            "same_ID_two_view_input": (
                "Round51 transports the two individually proper views to one once-charged reference law"
            ),
            "same_parent_common_terminal_nonhit_mass_strict_lower": "249/250",
            "union_bound": "1-1/500-1/500=249/250",
            "status": "CERTIFIED_UNIFORM_EXISTENTIAL_TIME_COMMON_TERMINAL_NONHIT",
        },
        "strict_scope": {
            "terminal_test_only": True,
            "intermediate_C24_avoidance": "NOT_CERTIFIED",
            "properness_of_common_nonhit_restriction": "NOT_CERTIFIED",
            "proper_same_ID_fw_rev_return": "NOT_CERTIFIED",
            "numeric_H_out": "NOT_CERTIFIED",
        },
        "status": "CERTIFIED_NUMERIC_OUTER_MAJORANT_AND_EXISTENTIAL_COMMON_TERMINAL_SURVIVOR",
    }


def sharp_non_effectivity() -> dict[str, Any]:
    majorant_floor = BUMP_NORM * OUTER_C * Q(3, 4)
    assert majorant_floor == Q(7777701, 10) > HIT_GAP
    return {
        "fixed_numeric_data": {
            "C_outer": str(OUTER_C),
            "hyperbolic_rate_upper": str(SAFE_HYPERBOLIC_RATE),
            "bump_norm_upper": str(BUMP_NORM),
            "required_error_gap": str(HIT_GAP),
        },
        "no_Delta_upper_model": (
            "for any proposed H0>=0 keep tilde_zeta=1/2 and take Delta=H0+1; then the coupling branch at H0 is (3/4)^(H0/(2*(H0+1)))>3/4"
        ),
        "no_zeta_lower_model": (
            "for any proposed H0>=0 keep Delta=1 and take tilde_zeta=1/(2*(H0+1)^2); direct checking for H0=0,1 and Bernoulli for H0>=2 give the coupling branch at H0>3/4"
        ),
        "corresponding_RHS_majorant_strict_lower": str(majorant_floor),
        "majorant_still_exceeds_required_gap": True,
        "logical_scope": (
            "these are admissible formal choices of the unpublished proof constants, not physical billiard counterexamples; they show that neither qualitative positivity of tilde_zeta nor qualitative finiteness of Delta can certify an integer"
        ),
        "both_numeric_rows_are_individually_necessary_for_this_proof_route": True,
        "status": "CERTIFIED_SHARP_TWO_SCALAR_NONEFFECTIVITY_OF_AVAILABLE_PROOF_DATA",
    }


def cover_type_separation() -> dict[str, Any]:
    assert SAFE_FAMILY_MASS * DIRECT_REQUIRED_FRACTION == HIT_GAP
    return {
        "whole_family_bump_route": {
            "output_type": "total C24 mass of the entire normalized family at one time",
            "existential_hit_fraction_strict_lower": str(HIT_GAP),
            "needs_proper_crossing_atlas": False,
        },
        "sufficient_rectangles_route": {
            "output_type": (
                "once-counted source fraction on every retained long leaf whose image properly crosses one typed direct-C24 Cantor rectangle"
            ),
            "retained_family_mass_strict_lower": str(SAFE_FAMILY_MASS),
            "required_per_leaf_direct_fraction": str(DIRECT_REQUIRED_FRACTION),
            "actual_numeric_fraction": None,
            "strict_inferable_lower": "0",
        },
        "nonimplication_model": (
            "a regular unstable segment may lie wholly inside an open C24 box, giving target mass one while crossing neither pair of stable sides of any registered Cantor rectangle; scalar target mass therefore does not imply the proper-crossing predicate"
        ),
        "numeric_H_bump_cannot_be_renamed_H_cover": True,
        "tilde_zeta_is_not_beta": (
            "tilde_zeta couples proper images through a time-dependent SYZ magnet; beta counts direct-C24 proper-crossing source bundles in the project registry"
        ),
        "numeric_H_cover": None,
        "numeric_beta": None,
        "status": "CERTIFIED_OBJECT_TYPE_SEPARATION_NO_COVER_PROMOTION",
    }


def literature_audit() -> dict[str, Any]:
    rows = [
        {
            "paper": "Stenlund--Young--Zhang, arXiv:1210.0011v4",
            "archive_sha256": ARXIV_1210_ARCHIVE_SHA256,
            "main_member": "Moving_final.tex",
            "main_member_sha256": ARXIV_1210_MAIN_TEX_SHA256,
            "finding": (
                "proof-level outer constants are algebraic in tilde_zeta, Delta, hat_c, Lambda, but Proposition 31 and the compact reference scheduling do not publish numerical tilde_zeta or Delta"
            ),
        },
        {
            "paper": "Demers--Liverani review, arXiv:2606.10155v1",
            "archive_sha256": ARXIV_2606_ARCHIVE_SHA256,
            "main_member": "billiard.survey_submited.tex",
            "main_member_sha256": ARXIV_2606_MAIN_TEX_SHA256,
            "finding": (
                "the review records Lambda=1+2*kappa_min*tau_min and surveys coupling/transfer-operator rates, but supplies no computer-assisted numerical magnet fraction, coupling gap, or C24 crossing atlas for this pilot"
            ),
        },
        {
            "paper": "Climenhaga--Day, arXiv:2604.25881v1",
            "finding": (
                "the sufficient-rectangles mechanism remains qualitative and supplies neither a numerical common iterate nor source width"
            ),
        },
    ]
    return {
        "official_versions_rechecked_2026_07_20": [
            "arXiv:2606.10155v1",
            "arXiv:2604.25881v1",
            "arXiv:2604.19671v2",
            "arXiv:1210.0011v4",
        ],
        "rows": rows,
        "rows_sha256": digest(rows),
        "newer_official_numeric_rate_or_cover_theorem_found": False,
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "claim_type": (
                "numeric proof-level outer prefactor, safe hyperbolic rate extraction, exact two-scalar H_bump interface, and fail-closed H_cover/beta type separation"
            ),
        },
        "proof_level_outer_rate": proof_level_outer_rate(),
        "two_scalar_effectivity_interface": two_scalar_effectivity_interface(),
        "uniform_C24_outer_majorant_and_common_terminal_survivor": (
            uniform_C24_outer_majorant()
        ),
        "sharp_non_effectivity": sharp_non_effectivity(),
        "H_bump_H_cover_beta_type_separation": cover_type_separation(),
        "latest_technology_audit": literature_audit(),
        "corrected_frontier": {
            "numeric_C_bump_proof_outer_upper": str(OUTER_C),
            "numeric_safe_hyperbolic_rate_upper": str(SAFE_HYPERBOLIC_RATE),
            "numeric_tilde_zeta_lower": None,
            "numeric_Delta_upper": None,
            "numeric_theta_bump": None,
            "numeric_H_bump": None,
            "numeric_outer_majorant_mass_upper": "87603/125000000",
            "numeric_outer_majorant_theorem_norm_upper": "7251",
            "uniform_existential_H_out": "CERTIFIED_NONNUMERIC",
            "numeric_H_out": None,
            "same_parent_common_terminal_nonhit_mass": "relative fraction >249/250 (absolute mass >249*p/250)",
            "proper_common_terminal_nonhit_restriction": "NOT_CERTIFIED",
            "numeric_H_cover": None,
            "numeric_beta": None,
            "complete_numeric_C_fw_C_rev_q": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
        },
        "strict_nonpromotion": {
            "numeric_proof_outer_C_bump_upper": "CERTIFIED_3807/10",
            "safe_hyperbolic_rate_upper": "CERTIFIED_9/10",
            "numeric_magnet_tilde_zeta_Delta": "NOT_CERTIFIED",
            "numeric_H_bump": "NOT_CERTIFIED",
            "uniform_existential_common_terminal_nonhit": "CERTIFIED_RELATIVE_FRACTION_>249/250",
            "numeric_H_out": "NOT_CERTIFIED",
            "proper_common_terminal_nonhit_restriction": "NOT_CERTIFIED",
            "uniform_numeric_H_cover_and_actual_beta": "NOT_CERTIFIED",
            "complete_numeric_C_fw_C_rev": "NOT_CERTIFIED",
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
    parser.add_argument(
        "--verifier",
        type=Path,
        default=HERE / "cm2_gate34_round52_outer_rate_numeric_frontier_verifier.py",
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    result = build_result()
    if args.summary:
        outer = result["proof_level_outer_rate"]
        frontier = result["corrected_frontier"]
        print(
            "C_BUMP_PROOF_OUTER_UPPER:",
            outer["numeric_outer_prefactor"]["C_bump_proof_outer_upper"],
        )
        print("SAFE_HYPERBOLIC_RATE:", frontier["numeric_safe_hyperbolic_rate_upper"])
        print("NUMERIC_H_BUMP:", frontier["numeric_H_bump"])
        print(
            "COMMON_TERMINAL_NONHIT_MASS:",
            frontier["same_parent_common_terminal_nonhit_mass"],
        )
        print("NUMERIC_H_COVER:", frontier["numeric_H_cover"])
        print("GATE4: NOT_CERTIFIED")
        print("CM2: NO-GO_FOR_CLAIM")
        return 0
    print("GATE4: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
