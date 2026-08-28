#!/usr/bin/env python3
"""Round-53 Gate-4 effective-clock and relative-atlas frontier.

This leaf does two things that were not explicit in Round 52.

First, it opens the hidden SYZ coupling-gap integer.  For the frozen pilot the
project's numerical Growth recurrence gives a genuine upper bound for the
``eventually proper again'' constant n_p.  In the Euclidean SYZ convention,

    n_p <= 696*317 = 220632.

The remaining coupling gap is then reduced to five typed, nonnumerical rows
instead of one opaque Delta.  This reduction is exact and does not pretend
that the magnet fraction or mixing/recovery data have been numericalised.

Second, it extracts a fixed-parameter relative-thickening consequence of the
sufficient-rectangles proof.  Compactness of the long-curve class and
openness of a strict finite-time crossing imply a pointwise adapted
eta_s^*>0 for the relative adapted source length.  This is qualitative and
fixed-map only.  The exact
conditional direct-C24 comparison threshold is
eta_s^* >= 43008/14285703575.  No numerical eta_s^*,
uniform parameter atlas, H_cover, or beta is claimed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate4_numeric_invariant_family_growth_recovery_frontier_cert as growth_cert


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate34.round53-effective-clock-relative-atlas-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate34-round53-effective-clock-relative-atlas-frontier-manifest-2026-07-20.json"
)

DEPENDENCIES = {
    "cm2-gate34-round52-outer-rate-numeric-frontier-manifest-2026-07-20.json": (
        "b86b5c74c8dcf4d2415ad28715a55ea98bf42bb191f7926684009ebbb8c8da34"
    ),
    "cm2_gate34_round52_outer_rate_numeric_frontier_cert.py": (
        "00e56e2a3ea639257df9445949ce6cf83e8d4c42f835b6ee5e285c666fa61439"
    ),
    "cm2-gate34-round51-uniform-gauge-bump-frontier-manifest-2026-07-20.json": (
        "4248c215821ba6e23eb78c64158b1301e1b33d964fb0cd024e4b8e4427247b21"
    ),
    "cm2-gate34-round49-incidence-safe-long-leaf-atlas-manifest-2026-07-19.json": (
        "f8117b4d6b91c85597953366bc1eee26652a6ff7c3bd5486d3a3a38694550c18"
    ),
    "cm2_gate34_round49_incidence_safe_long_leaf_atlas_cert.py": (
        "9ebbc356673f90c95f698716b787f638ebf6c36d8da461d439382218130aa159"
    ),
    "cm2-gate34-round50-same-cover-target-adjunction-manifest-2026-07-19.json": (
        "03b9850b0dc3e2631b47e44ceb966cbf7b1b2b49263ca328662a03a0b8a7fc07"
    ),
    "cm2_gate34_round50_same_cover_target_adjunction_cert.py": (
        "60d50f3d6656511c6f52de267d8cd718de0d4265d57a82e796c4773fbfab619b"
    ),
    "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json": (
        "b03c5ae0e400045f087cfbd1aa8c843990edebe517a4dde786b0718446db7c1d"
    ),
    "cm2_gate4_numeric_invariant_family_growth_recovery_frontier_cert.py": (
        "01e32ca209818f4077443a7692622c4202ab7f1066e2f95802185e2be7a2cc9a"
    ),
}

ARXIV_1210_ARCHIVE_SHA256 = (
    "b705ed4fc89a42ac8e78957d65873211c71f9566599bfba90173812fe5ffe5c5"
)
ARXIV_1210_MAIN_TEX_SHA256 = (
    "921fe3477c2f3280a256a459c9e2a2bc6b719a971016a8320e6d0d5e9cd25f44"
)
ARXIV_2604_MAIN_TEX_SHA256 = (
    "b8f79a99f5f98648f91848cd7b4e489846f4512d6ed35ebd042229da3c89ee94"
)
ARXIV_2502_ARCHIVE_SHA256 = (
    "a703115d1c2b943b82303a9f9f5d728ff819f2fa86365e663c8c2419ff02f60f"
)
ARXIV_2502_MAIN_TEX_SHA256 = (
    "1e4dfee91d2c7e2fc418b9a9b298be0afe78e9547a7729eaecadf88f73991951"
)

HIT_GAP = Q(21, 111718750)
BUMP_NORM = Q(2724)
OUT_NORM = Q(7251)
OUT_ERROR = Q(1, 1000)
OUTER_C = Q(3807, 10)
SAFE_HYPERBOLIC_RATE = Q(9, 10)
RETAINED_MASS = Q(1999, 32000)
DENSITY_LOWER_RATIO = Q(1999, 2000)
DIRECT_REQUIRED_FRACTION = Q(2688, 893303125)
RELATIVE_THICKNESS_THRESHOLD = Q(43008, 14285703575)
DELTA_RECT = Q(
    119621,
    41476958890128 * 10**90,
)
GROWTH_A = Q(360134800, 360493663)
HALF_BLOCK = 696
EUCLIDEAN_CP = Q(141 * 10**90 * 360493663, 358863)
EUCLIDEAN_CP_POWER_UPPER = 317
N_P_UPPER = HALF_BLOCK * EUCLIDEAN_CP_POWER_UPPER


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
    outer = load_json(
        "cm2-gate34-round52-outer-rate-numeric-frontier-manifest-2026-07-20.json"
    )
    if outer.get("schema") != (
        "cm2.gate34.round52-outer-rate-numeric-frontier.v1.manifest.v1"
    ):
        raise RuntimeError("Round52 schema")
    outer_result = outer["result"]
    frontier = outer_result["corrected_frontier"]
    if frontier["numeric_C_bump_proof_outer_upper"] != "3807/10":
        raise RuntimeError("Round52 outer C")
    if frontier["numeric_safe_hyperbolic_rate_upper"] != "9/10":
        raise RuntimeError("Round52 safe rate")
    for key in ("numeric_tilde_zeta_lower", "numeric_Delta_upper", "numeric_H_bump"):
        if frontier[key] is not None:
            raise RuntimeError(f"Round52 numerical scope: {key}")
    checked_text(
        "cm2_gate34_round52_outer_rate_numeric_frontier_cert.py",
        (
            "C_1=2*max((1-tilde_zeta/2)^(-1),hat_c^(-1))",
            "numeric_tilde_zeta_lower\": None",
            "numeric_H_bump_cannot_be_renamed_H_cover",
        ),
    )

    gauge = load_json(
        "cm2-gate34-round51-uniform-gauge-bump-frontier-manifest-2026-07-20.json"
    )["result"]["instance_specific_fixed_gauge"]
    if gauge["uniform_numeric_m_s"] != "1":
        raise RuntimeError("Round51 gauge")
    if Q(gauge["numeric_reference_delta_rect"]) != DELTA_RECT:
        raise RuntimeError("Round51 delta")

    atlas = load_json(
        "cm2-gate34-round49-incidence-safe-long-leaf-atlas-manifest-2026-07-19.json"
    )
    if atlas.get("schema") != (
        "cm2.gate34.round49-incidence-safe-long-leaf-atlas.v1.manifest.v1"
    ):
        raise RuntimeError("Round49 schema")
    atlas_result = atlas["result"]
    core = atlas_result["incidence_safe_long_leaf_compact_core"]
    thresholds = atlas_result["exact_remaining_cover_thresholds"]
    if Q(core["incidence_safe_family_mass_strict_lower"]) != RETAINED_MASS:
        raise RuntimeError("Round49 retained mass")
    if Q(core["incidence_safe_piece_Euclidean_length_strict_lower"]) != DELTA_RECT:
        raise RuntimeError("Round49 piece length")
    if Q(thresholds["incidence_safe_required_direct_C24_fraction"]) != DIRECT_REQUIRED_FRACTION:
        raise RuntimeError("Round49 direct fraction")
    if thresholds["actual_fraction_certified"] is not False:
        raise RuntimeError("Round49 nonpromotion")
    checked_text(
        "cm2_gate34_round49_incidence_safe_long_leaf_atlas_cert.py",
        ("Q(2688, 893303125)", "incidence_safe_piece_Euclidean_length_strict_lower"),
    )

    cover = load_json(
        "cm2-gate34-round50-same-cover-target-adjunction-manifest-2026-07-19.json"
    )
    if cover.get("schema") != (
        "cm2.gate34.round50-same-cover-target-adjunction.v2.manifest.v1"
    ):
        raise RuntimeError("Round50 schema")
    target = cover["result"]["fixed_parameter_enlarged_cover_target_adjunction"]
    if target["enlarged_cover_bridge_installed_fixed_s"] is not True:
        raise RuntimeError("Round50 cover bridge")
    if target["fixed_s_finite_target_hit_iterate_exists"] is not True:
        raise RuntimeError("Round50 finite iterate")
    if target["numeric_N_s"] is not None or target["numeric_source_subcurve_fraction"] is not None:
        raise RuntimeError("Round50 numeric scope")
    checked_text(
        "cm2_gate34_round50_same_cover_target_adjunction_cert.py",
        ("fixed_s_finite_target_hit_iterate_exists", "numeric_source_subcurve_fraction"),
    )

    growth_manifest = load_json(
        "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json"
    )
    replay = growth_manifest["replay_summary"]
    if Q(replay["vartheta_p"]) != GROWTH_A:
        raise RuntimeError("Growth coefficient")
    checked_text(
        "cm2_gate4_numeric_invariant_family_growth_recovery_frontier_cert.py",
        (
            "euclidean_SYZ_form",
            "Z_n^E/mass<=(C_p/2)*(1+a^n Z_0^E/mass)",
            "euclidean_C_p",
        ),
    )
    numeric_growth = growth_cert.numeric_growth_and_recovery()
    constants = numeric_growth["numeric_Growth_Lemma_constants"]
    if Q(constants["euclidean_C_p"]) != EUCLIDEAN_CP:
        raise RuntimeError("Euclidean C_p")
    if Q(constants["vartheta_p"]) != GROWTH_A:
        raise RuntimeError("module Growth coefficient")
    return {
        "outer": outer_result,
        "atlas": atlas_result,
        "cover": cover["result"],
        "growth": numeric_growth,
    }


def numerical_proper_return_bound() -> dict[str, Any]:
    assert 2 * 360134800**HALF_BLOCK < 360493663**HALF_BLOCK
    assert EUCLIDEAN_CP < 2**EUCLIDEAN_CP_POWER_UPPER
    assert N_P_UPPER == 220632
    return {
        "metric_scope": (
            "Euclidean Z convention used by the SYZ proper-family definition; this is the project's certified Euclidean Growth recurrence, not the adapted C_p value"
        ),
        "growth_recurrence": (
            "Z_n^E/mass <= (C_p^E/2)*(1+a^n*Z_0^E/mass)"
        ),
        "a": str(GROWTH_A),
        "C_p_E": str(EUCLIDEAN_CP),
        "C_p_E_power_two_strict_upper": "2^317",
        "half_block": HALF_BLOCK,
        "exact_half_block_test": "2*360134800^696<360493663^696",
        "derivation": (
            "if Z_0^E/mass<C_p^E, then a^(696*317)*Z_0^E/mass<2^-317*2^317=1, so the displayed Growth upper is strictly below C_p^E"
        ),
        "numeric_n_p_upper": N_P_UPPER,
        "status": "CERTIFIED_NUMERIC_SYZ_PROPER_RETURN_UPPER_FOR_THE_FROZEN_PROJECT_CLASS",
    }


def coupling_gap_decomposition() -> dict[str, Any]:
    rows = [
        {
            "id": "zeta0",
            "meaning": "positive lower bound for tilde_zeta=min_q zeta(K_q), with the harmless convention 0<zeta0<=tilde_zeta<=1/2; the source crossing bound in fact makes each chosen zeta smaller than 1/4",
            "domain": "0<zeta0<=1/2",
            "value": None,
        },
        {
            "id": "S",
            "meaning": "integer upper bound for max_q s(K_q), including the fixed-map mixing/super-proper-crossing time",
            "domain": "S is a nonnegative integer",
            "value": None,
        },
        {
            "id": "R",
            "meaning": "integer upper bound for max_q max(r_gap_top(K_q),s_prime(K_q))",
            "domain": "R is a nonnegative integer",
            "value": None,
        },
        {
            "id": "C",
            "meaning": "finite upper bound for max_q C(K_q) in the rank-gap proper-recovery tail",
            "domain": "C>=1",
            "value": None,
        },
        {
            "id": "lambda",
            "meaning": "one numerical upper bound below one for the uniform gap-recovery base",
            "domain": "0<lambda<1",
            "value": None,
        },
    ]
    return {
        "source_formula": (
            "SYZ source lines 2518--2565 and 2636--2694: Delta=2*max(s)+2*max(r)+Delta0 and Delta0=L_rec+max(s)+n_p"
        ),
        "remaining_atomic_rows": rows,
        "remaining_atomic_rows_sha256": digest(rows),
        "integer_only_recovery_wait": (
            "L_rec is the least integer L>=0 such that 2*C*lambda^L<=zeta0*(1-zeta0)"
        ),
        "monotonicity_guard": (
            "on 0<zeta<=1/2 the function zeta*(1-zeta) is increasing, so zeta0<=tilde_zeta makes the integer test conservative"
        ),
        "exact_conditional_upper": (
            "D=3*S+2*R+220632+L_rec is a safe upper bound for Delta"
        ),
        "newly_numeric_component": "n_p<=220632",
        "why_project_Growth_does_not_fill_the_other_rows": (
            "the post-coupling gap law starts with arbitrarily short rank gaps and may have infinite aggregate Z; the finite-Z Growth recurrence alone supplies neither the rank-tail constant C nor a numerical magnet mixing fraction"
        ),
        "numeric_Delta_upper": None,
        "status": "OPAQUE_DELTA_REDUCED_TO_FIVE_TYPED_ROWS_PLUS_NUMERIC_N_P",
    }


def conditional_block_time(norm: Q, error: Q, zeta_lower: Q, delta_upper: int) -> dict[str, Any]:
    if not (0 < zeta_lower < 1):
        raise ValueError("zeta_lower")
    if not isinstance(delta_upper, int) or delta_upper < 1:
        raise ValueError("delta_upper")
    scale = norm * OUTER_C
    coupling_base = 1 - zeta_lower / 2
    m = 0
    while not (
        scale * coupling_base**m < error
        and scale * SAFE_HYPERBOLIC_RATE ** (2 * delta_upper * m) < error
    ):
        m += 1
    previous_passes = m > 0 and (
        scale * coupling_base ** (m - 1) < error
        and scale * SAFE_HYPERBOLIC_RATE ** (2 * delta_upper * (m - 1)) < error
    )
    return {
        "norm_upper": str(norm),
        "required_error": str(error),
        "zeta_lower": str(zeta_lower),
        "Delta_upper": delta_upper,
        "minimal_safe_block_count_m": m,
        "safe_time_H": 2 * delta_upper * m,
        "previous_block_passes_both_tests": previous_passes,
    }


def effective_clock_interface() -> dict[str, Any]:
    bump_sample = conditional_block_time(BUMP_NORM, HIT_GAP, Q(1, 2), 1)
    outer_sample = conditional_block_time(OUT_NORM, OUT_ERROR, Q(1, 2), 1)
    assert bump_sample["minimal_safe_block_count_m"] == 140
    assert bump_sample["safe_time_H"] == 280
    assert outer_sample["minimal_safe_block_count_m"] == 104
    assert outer_sample["safe_time_H"] == 208
    return {
        "conditional_D_builder": (
            "given the five atomic rows, compute L_rec by the exact integer inequality and D=3*S+2*R+220632+L_rec"
        ),
        "H_bump_integer_test": (
            "least m with (2724*3807/10)*(1-zeta0/2)^m<21/111718750 and (2724*3807/10)*(9/10)^(2*D*m)<21/111718750; H_bump=2*D*m"
        ),
        "H_out_integer_test": (
            "least m with (7251*3807/10)*(1-zeta0/2)^m<1/1000 and (7251*3807/10)*(9/10)^(2*D*m)<1/1000; H_out=2*D*m"
        ),
        "arithmetic_samples_not_physical_claims": {
            "H_bump_zeta_half_D_one": bump_sample,
            "H_out_zeta_half_D_one": outer_sample,
        },
        "numeric_H_bump": None,
        "numeric_H_out": None,
        "status": "EXACT_CONDITIONAL_CLOCKS_WITH_FIVE_NONNUMERIC_MAGNET_ROWS",
    }


def fixed_parameter_relative_atlas() -> dict[str, Any]:
    assert RETAINED_MASS * DIRECT_REQUIRED_FRACTION == HIT_GAP
    assert (
        DIRECT_REQUIRED_FRACTION / DENSITY_LOWER_RATIO
        == RELATIVE_THICKNESS_THRESHOLD
    )
    hit_coefficient = RETAINED_MASS * DENSITY_LOWER_RATIO
    assert hit_coefficient == Q(3996001, 64000000)
    assert HIT_GAP / hit_coefficient == RELATIVE_THICKNESS_THRESHOLD
    steps = [
        {
            "step": 1,
            "claim": (
                "fix one parameter sigma and the finite N_sigma from the enlarged sufficient-cover theorem; every admissible V selected by the Euclidean condition |V|>=delta_rect contains a nondegenerate U whose N_sigma image strictly crosses the direct-C24 Cantor rectangle"
            ),
        },
        {
            "step": 2,
            "claim": (
                "on the smooth N_sigma branch, strict crossing of two stable sides is open under the curve topology used in the sufficient-rectangles compactness argument"
            ),
        },
        {
            "step": 3,
            "claim": (
                "for each V choose a smaller crossing core with positive side and singularity margins; continuity and uniform equivalence of the adapted line element make ell_*(U)/ell_*(V) stay above half its value at V in a sufficiently small neighborhood"
            ),
        },
        {
            "step": 4,
            "claim": (
                "the Euclidean-selected class V_delta is compact, so finitely many such neighborhoods give eta_sigma^*=inf_V sup_U ell_*(U)/ell_*(V)>0"
            ),
        },
    ]
    return {
        "scope": (
            "one fixed parameter sigma and the pulled-back admissible u-curve class only; conditional per canonical proper standard family"
        ),
        "input_length": str(DELTA_RECT),
        "input_selection_metric": "Euclidean |V|>=delta_rect",
        "pointwise_finite_time": "N_sigma<infinity, nonnumerical",
        "compact_open_thickening_steps": steps,
        "compact_open_thickening_steps_sha256": digest(steps),
        "adapted_relative_width_definition": (
            "eta_sigma^*=inf_{V in V_delta} sup{ell_*(U)/ell_*(V): U subset V and T_sigma^N_sigma U strictly crosses R_*}, while V_delta is selected by Euclidean |V|>=delta_rect"
        ),
        "fixed_sigma_eta_star_positive": True,
        "numeric_eta_sigma_star": None,
        "density_conversion": (
            "the conditional density ratio <2000/1999 is with respect to adapted line length, hence gives crossing mass fraction > (1999/2000)*eta_sigma^* on every retained piece"
        ),
        "conditional_beta_definition": (
            "beta_sigma is the conditional crossing source fraction on each retained piece, before multiplying by retained family mass 1999/32000"
        ),
        "conditional_beta_strict_lower_symbolic": (
            "beta_sigma>(1999/2000)*eta_sigma^*"
        ),
        "aggregate_hit_mass_strict_lower_symbolic": (
            "h_sigma>(1999/32000)*beta_sigma>(3996001/64000000)*eta_sigma^*"
        ),
        "exact_eta_threshold_for_conditional_direct_C24_fraction": str(
            RELATIVE_THICKNESS_THRESHOLD
        ),
        "equivalent_eta_threshold_for_aggregate_hit_gap": str(
            RELATIVE_THICKNESS_THRESHOLD
        ),
        "threshold_logic": (
            "eta_sigma^*>=43008/14285703575 makes (1999/2000)*eta_sigma^*=2688/893303125 and (3996001/64000000)*eta_sigma^*=21/111718750; both mass comparisons are strict, so beta_sigma and h_sigma strictly exceed their respective benchmarks"
        ),
        "conditional_distortion_lower": (
            "using adapted-compatible rows, if target transverse width w_sigma^*>0, smooth-branch adapted derivative upper J_sigma^*, adapted maximum source length L_max^*, and N_sigma are certified, then eta_sigma^*>=w_sigma^*/((J_sigma^*)^N_sigma*L_max^*); singularity clearance is required to make J_sigma^* finite"
        ),
        "numeric_rows_still_missing": [
            "adapted-compatible target stable-side transverse width w_sigma^*",
            "finite integer N_sigma",
            "N_sigma-step branch/singularity clearance",
            "adapted derivative/distortion upper J_sigma^* on every selected branch and adapted L_max^*",
            "parameter-persistence modulus and finite rational subdivision",
        ],
        "numeric_H_cover": None,
        "numeric_beta": None,
        "uniform_parameter_window_eta_star_positive": "NOT_CERTIFIED",
        "status": "CERTIFIED_FIXED_PARAMETER_QUALITATIVE_RELATIVE_THICKNESS_ONLY",
    }


def strict_separators() -> dict[str, Any]:
    return {
        "arbitrarily_thin_crossing_model": (
            "for each epsilon>0 take one compact singleton source class V=[0,1] with adapted line element equal to Euclidean length, let U=[0,epsilon], and a smooth branch mapping U across a unit target; all fixed-map existence and openness statements hold but eta^*=epsilon, so qualitative crossing has strict inferable numerical lower zero"
        ),
        "whole_family_hit_not_crossing_model": (
            "an unstable segment can lie inside an open C24 box and have target mass one while meeting neither pair of stable sides of a registered Cantor rectangle"
        ),
        "pointwise_parameter_compactness_warning": (
            "eta_sigma^*>0 and N_sigma<infinity for each sigma do not yield inf_sigma eta_sigma^*>0 or sup_sigma N_sigma<infinity without open branch persistence across sigma"
        ),
        "whole_family_hit_renamed_crossing": False,
        "fixed_sigma_positive_eta_star_renamed_numeric_beta": False,
        "strict_inferable_uniform_numeric_eta_star_lower": "0",
        "status": "CERTIFIED_NONPROMOTION",
    }


def literature_audit() -> dict[str, Any]:
    rows = [
        {
            "paper": "Stenlund--Young--Zhang, arXiv:1210.0011v4",
            "archive_sha256": ARXIV_1210_ARCHIVE_SHA256,
            "main_member": "Moving_final.tex",
            "main_member_sha256": ARXIV_1210_MAIN_TEX_SHA256,
            "anchors": "source lines 2518--2565 and 2636--2694",
            "finding": (
                "the source exposes the exact Delta scheduling algebra, but magnet mixing zeta,s, stable schedule s_prime, and gap/top constants r,C,lambda remain qualitative"
            ),
        },
        {
            "paper": "Climenhaga--Day, arXiv:2604.25881v1",
            "main_member": "billiard-mme-arXiv-v1.tex",
            "main_member_sha256": ARXIV_2604_MAIN_TEX_SHA256,
            "anchors": "Proposition 3.19 and proof sketch, source lines 1568--1586",
            "finding": (
                "compactness and strict finite-time crossing give fixed-map qualitative relative thickness, but no numeric N, rectangle width, branch clearance, derivative bound, or parameter modulus"
            ),
        },
        {
            "paper": "Demers--Liverani, arXiv:2502.07765v2",
            "archive_sha256": ARXIV_2502_ARCHIVE_SHA256,
            "main_member": "sequential-revision1.tex",
            "main_member_sha256": ARXIV_2502_MAIN_TEX_SHA256,
            "anchors": "billiard cone application and Theorem 6.12 interface, source lines 2483--2699",
            "finding": (
                "the complex-projective-cone CLT route imports existential N_F(delta), epsilon and finite cone diameter from DL22; it publishes no pilot-specific numerical mixing time or C24 rectangle/source-width constants"
            ),
        },
    ]
    return {
        "official_versions_rechecked_2026_07_20": [
            "arXiv:2606.10155v1",
            "arXiv:2604.25881v1",
            "arXiv:2604.19671v2",
            "arXiv:2502.07765v2",
            "arXiv:1210.0011v4",
        ],
        "rows": rows,
        "rows_sha256": digest(rows),
        "new_numeric_pilot_magnet_or_rectangle_atlas_found": False,
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "claim_type": (
                "numeric n_p component of the SYZ coupling schedule, exact five-row Delta reduction, and fixed-parameter qualitative relative-crossing thickness"
            ),
        },
        "numeric_SYZ_eventual_proper_return": numerical_proper_return_bound(),
        "coupling_gap_five_row_decomposition": coupling_gap_decomposition(),
        "conditional_H_bump_H_out": effective_clock_interface(),
        "fixed_parameter_relative_crossing_atlas": fixed_parameter_relative_atlas(),
        "strict_type_and_effectivity_separators": strict_separators(),
        "latest_technology_audit": literature_audit(),
        "corrected_frontier": {
            "numeric_SYZ_n_p_upper": N_P_UPPER,
            "numeric_tilde_zeta_lower": None,
            "numeric_Delta_upper": None,
            "numeric_H_bump": None,
            "numeric_H_out": None,
            "fixed_parameter_eta_sigma_star_positive": "CERTIFIED_NONNUMERIC",
            "numeric_eta_sigma_star": None,
            "uniform_parameter_window_eta_star": "NOT_CERTIFIED",
            "numeric_H_cover": None,
            "numeric_beta": None,
            "proper_same_ID_return": "NOT_CERTIFIED",
            "complete_numeric_C_fw_C_rev_q": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
        },
        "strict_nonpromotion": {
            "numeric_SYZ_n_p_upper_220632": "CERTIFIED",
            "numeric_full_Delta": "NOT_CERTIFIED",
            "numeric_H_bump": "NOT_CERTIFIED",
            "numeric_H_out": "NOT_CERTIFIED",
            "fixed_sigma_qualitative_relative_crossing_thickness": "CERTIFIED_CONDITIONAL_PER_ADMISSIBLE_FAMILY",
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
        default=HERE / "cm2_gate34_round53_effective_clock_relative_atlas_frontier_verifier.py",
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    result = build_result()
    if args.summary:
        frontier = result["corrected_frontier"]
        print("NUMERIC_SYZ_N_P_UPPER:", frontier["numeric_SYZ_n_p_upper"])
        print("NUMERIC_DELTA:", frontier["numeric_Delta_upper"])
        print("FIXED_SIGMA_ETA_STAR_POSITIVE:", frontier["fixed_parameter_eta_sigma_star_positive"])
        print("NUMERIC_H_COVER:", frontier["numeric_H_cover"])
        print("GATE4: NOT_CERTIFIED")
        print("CM2: NO-GO_FOR_CLAIM")
        return 0
    print("GATE4: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
