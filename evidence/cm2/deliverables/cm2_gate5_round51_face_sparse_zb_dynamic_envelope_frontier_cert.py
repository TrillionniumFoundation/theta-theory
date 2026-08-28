#!/usr/bin/env python3
"""Round-51 face-local Z_B and common dynamic-envelope frontier.

This append-only layer sharpens, but does not promote, the Round-50 Gate-5
frontier.  It separates the five physical face kinds, proves a finite
full-rank (theta=1) bound on the *raw moving-occurrence seed coarea law*, and
shows exactly why owner-once incidence plus scalar +/- cancellation does not
transfer that bound to the arbitrary-R_n owner-leaf current.

It also constructs one common suffix-envelope test space on which every
finite regular suffix pullback has norm one.  This is an algebraic common
dynamic space, not the physical CM2/F17 space: no bounded inclusion of the
required physical C1 tests into the envelope is available.  Gate-5 maturity
therefore remains 10/18 and no complete field/operator block is promoted.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate5.round51-face-sparse-zb-dynamic-envelope-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate5-round51-face-sparse-zb-dynamic-envelope-frontier-manifest-2026-07-20.json"
)

DEPENDENCIES = {
    "cm2-gate5-round50-owner-boundary-zb-f17-frontier-manifest-2026-07-19.json": (
        "c848c67bb9f2c0793d793c2ab4dca754cad71c507b9f0a06b9c29be3eaafeb46"
    ),
    "cm2-gate5-round39-moving-occurrence-f10-l3over2-manifest-2026-07-19.json": (
        "19ad840a8cfbca2aa722cfd367d287fe36de67b9c7b6faf00a151ca2f2bf8a16"
    ),
    "cm2-gate3-bulk-jx-coarea-pairing-manifest-2026-07-15.json": (
        "a0e4d3f35d463b23c87cb1e676fbe732c9d15123b1674baf92f116d61669a1b7"
    ),
    "cm2-gate5-physical-prefix-kac-norm-frontier-manifest-2026-07-16.json": (
        "64f3820e2dc2f6d544be94bbe205fcf08f9517eef29131311e6fafa295060a93"
    ),
    "cm2-gate5-round44-all-face-suffix-two-trace-f13-manifest-2026-07-19.json": (
        "3cf6635532622427bcde0525205212e1970b92ee56b2eb290ed01c1984443a9d"
    ),
    "cm2-gate5-round47-regular-c1dual-f13-manifest-2026-07-19.json": (
        "3415f8533865e9ed907df823c1453ee981f3f1f1d5e04333fc14a90ddb2884d0"
    ),
    "cm2-gate5-round48-seven-boundary-f10-seed-frontier-manifest-2026-07-19.json": (
        "d2eb549656098abfc3fd57ae3eb5796e4ec3d57ebf579b21497ee3721ee3116c"
    ),
}

B0 = 14
K0 = 6121
COAREA_MASS = Q(8064, 5)
RANK_TAIL_COEFFICIENT = Q(9158592, 6875)
FORWARD_F10_COEFFICIENT = 68
REVERSE_F10_COEFFICIENT = 35
F13_OVER_D1 = Q(3816937, 47112000)
X_OVER_D1 = Q(25, 151)
FULL_SOURCE_OVER_D1 = Q(11616937, 47112000)
QUARTER_CDYN_THRESHOLD = Q(7961063, 7800000)
UNIT_CDYN_THRESHOLD = Q(43295063, 7800000)
SURVIVAL_R = Q(111718729, 111718750)
BLOCK_DEPTH = 9148


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate key: {key}")
        out[key] = value
    return out


def reject_json_constant(token: str) -> None:
    """Reject the non-RFC constants accepted by Python's JSON decoder."""
    raise ValueError(f"non-finite JSON constant: {token}")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), allow_nan=False
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def fraction_digest(value: Q) -> str:
    numerator = value.numerator.to_bytes(
        (value.numerator.bit_length() + 7) // 8, "big"
    )
    denominator = value.denominator.to_bytes(
        (value.denominator.bit_length() + 7) // 8, "big"
    )
    return hashlib.sha256(
        len(numerator).to_bytes(8, "big") + numerator + denominator
    ).hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def load(name: str) -> dict[str, Any]:
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


def validate_dependencies() -> dict[str, dict[str, Any]]:
    loaded = {name: load(name) for name in DEPENDENCIES}

    prior = loaded[
        "cm2-gate5-round50-owner-boundary-zb-f17-frontier-manifest-2026-07-19.json"
    ]["result"]
    if prior["full_ZB_homogeneity_majorant_frontier"][
        "full_theta_one_available_majorant"
    ] != "INFINITE":
        raise RuntimeError("Round50 theta-one frontier")
    if prior["dynamic_anisotropic_F17_frontier"][
        "branch_adapted_suffix_multiplier"
    ] != "C_dyn=1":
        raise RuntimeError("Round50 dynamic multiplier")
    if prior["strict_nonpromotion"]["Gate5_maturity"] != "10/18":
        raise RuntimeError("Round50 maturity")

    occurrence = loaded[
        "cm2-gate5-round39-moving-occurrence-f10-l3over2-manifest-2026-07-19.json"
    ]["result"]
    rank = occurrence["physical_rank_L3over2_derivation"]
    if rank["positive_coarea_total_mass_upper"] != qstr(COAREA_MASS):
        raise RuntimeError("occurrence coarea mass")
    if rank["rank_tail"] != (
        "m{B>b}<=(9158592/6875)*4^(-b) for every integer b>=14"
    ):
        raise RuntimeError("occurrence rank tail")
    seed = occurrence["moving_occurrence_seed_F10_L3over2_installation"]
    if seed["forward_raw_seed_cost"] != "<18/5+(8424/125)*2^B<68*2^B":
        raise RuntimeError("forward occurrence envelope")
    if seed["reverse_raw_seed_cost"] != "<18/5+(4374/125)*2^B<35*2^B":
        raise RuntimeError("reverse occurrence envelope")

    jx = loaded[
        "cm2-gate3-bulk-jx-coarea-pairing-manifest-2026-07-15.json"
    ]["result"]
    if jx["bulk_physical_scalar_mu_dot_r_from_certified_rows"] != "0":
        raise RuntimeError("Jx scalar cancellation")
    if jx["scope_limits"]["arbitrary_test_current_cancellation"] is not False:
        raise RuntimeError("Jx arbitrary-test scope")

    kac = loaded[
        "cm2-gate5-physical-prefix-kac-norm-frontier-manifest-2026-07-16.json"
    ]["result"]["corrected_Kac_borel_output"]
    if kac["global_signed_scalar_coarea_mass"] != "0":
        raise RuntimeError("Kac scalar cancellation")
    if kac[
        "scalar_roof_cancellation_is_not_arbitrary_test_current_cancellation"
    ] is not True:
        raise RuntimeError("Kac cancellation typing")

    f13 = loaded[
        "cm2-gate5-round44-all-face-suffix-two-trace-f13-manifest-2026-07-19.json"
    ]["result"]
    transport = f13["occurrence_suffix_two_trace_transport"]["suffix_transport"]
    if transport["signed_current_formula"] != (
        "J_(n,j,e)=sigma_e*(tau_hit-tau_miss)"
    ):
        raise RuntimeError("occurrence pair formula")
    if transport["constant_test_cancellation_preserved"] is not True:
        raise RuntimeError("constant cancellation")
    if f13["same_ID_physical_F13_trace_charge"][
        "exact_F13_over_D1_ratio"
    ] != qstr(F13_OVER_D1):
        raise RuntimeError("F13 ratio")

    core = loaded[
        "cm2-gate5-round47-regular-c1dual-f13-manifest-2026-07-19.json"
    ]["result"]["rank_zero_C24_core_edge_F10_seed"]
    if core["status"] != "CERTIFIED_RANK_ZERO_C24_CORE_EDGE_F10_SEED":
        raise RuntimeError("core rank-zero seed")
    if core["C24_output_edge_domain"] != [
        "abs(p)<=1/50", "c>19/20", "R>=4/25"
    ]:
        raise RuntimeError("core central domain")

    seven = loaded[
        "cm2-gate5-round48-seven-boundary-f10-seed-frontier-manifest-2026-07-19.json"
    ]["result"]
    if seven["five_zero_speed_F10_base_seeds"]["row_count"] != 5:
        raise RuntimeError("zero-speed face count")
    if seven["arbitrary_Rn_installation_frontier"][
        "all_seven_one_step_base_seed_types_have_numeric_values"
    ] != "CERTIFIED":
        raise RuntimeError("seven boundary seeds")
    return loaded


def face_local_rank_audit() -> dict[str, Any]:
    rows = [
        {
            "physical_face_kind": "source_core_clipping_face",
            "one_step_parameter_current": "zero in fixed common source coordinates",
            "rank_weight_role": "none",
            "available_route": "zero current",
            "full_theta_one_ZB_needed": False,
        },
        {
            "physical_face_kind": "intermediate_core_avoidance_preimage_face",
            "one_step_parameter_current": "affine C24 core-edge flux",
            "rank_weight_role": "rank-zero central C24 seed",
            "available_route": "fixed ordinary-Z insertion cost before suffix",
            "full_theta_one_ZB_needed": False,
        },
        {
            "physical_face_kind": "terminal_core_preimage_face",
            "one_step_parameter_current": "affine C24 core-edge flux",
            "rank_weight_role": "rank-zero central C24 seed",
            "available_route": "fixed ordinary-Z insertion cost before suffix",
            "full_theta_one_ZB_needed": False,
        },
        {
            "physical_face_kind": "collision_singularity_or_owner_change_face",
            "one_step_parameter_current": "seven frozen boundary-kind regular seeds",
            "rank_weight_role": "fixed tangency/corner costs; five zero-speed kinds vanish",
            "available_route": "fixed ordinary-Z insertion cost before suffix",
            "full_theta_one_ZB_needed": False,
        },
        {
            "physical_face_kind": "moving_occurrence_face",
            "one_step_parameter_current": "sigma*(tau_hit-tau_miss)",
            "rank_weight_role": "raw bidirectional seed cost <103*2^B",
            "available_route": "occurrence-only Z_B or a paired-current separation theorem",
            "full_theta_one_ZB_needed": True,
        },
    ]
    return {
        "rows": rows,
        "rows_sha256": digest(rows),
        "five_physical_face_kinds_exhausted": True,
        "only_full_rank_face_kind": "moving_occurrence_face",
        "artificial_chart_or_homogeneity_faces": (
            "assembled before absolute values and excluded from the physical ledger"
        ),
        "scope": (
            "one-step insertion ledger only; suffix bulk/tangential growth and the "
            "arbitrary-R_n same-measure join are separate"
        ),
        "status": "CERTIFIED_FACE_LOCAL_RANK_DECOMPOSITION",
    }


def raw_seed_theta_one_bound() -> dict[str, Any]:
    # Integer layer cake:
    # 2^B=2^14+sum_{b=14}^{B-1}2^b and
    # sum_{b>=14}2^b*4^{-b}=sum_{b>=14}2^{-b}=2^{-13}.
    rank_l1 = (1 << B0) * COAREA_MASS + RANK_TAIL_COEFFICIENT * Q(1, 1 << 13)
    forward = FORWARD_F10_COEFFICIENT * rank_l1
    reverse = REVERSE_F10_COEFFICIENT * rank_l1
    bidirectional = forward + reverse
    if rank_l1 != Q(23253221519103, 880000):
        raise RuntimeError("rank L1 arithmetic")
    if forward != Q(395304765824751, 220000):
        raise RuntimeError("forward L1 arithmetic")
    if reverse != Q(162772550633721, 176000):
        raise RuntimeError("reverse L1 arithmetic")
    if bidirectional != Q(2395081816467609, 880000):
        raise RuntimeError("bidirectional L1 arithmetic")
    return {
        "measure": "unnormalized positive endpoint coarea seed measure m_occ",
        "rank_scope": "integer B>=14 on the unique active endpoint collar",
        "inputs": {
            "mass_upper": qstr(COAREA_MASS),
            "tail": "m_occ{B>b}<=(9158592/6875)*4^(-b), b>=14",
            "forward_seed_cost": "F10_fw<68*2^B",
            "reverse_seed_cost": "F10_rev<35*2^B",
        },
        "integer_layer_cake": (
            "2^B=2^14+sum_(b=14)^(B-1)2^b and "
            "sum_(b>=14)2^b*4^(-b)=2^(-13)"
        ),
        "integral_2^B_dm_occ_strict_upper": qstr(rank_l1),
        "forward_F10_L1_strict_upper": qstr(forward),
        "reverse_F10_L1_strict_upper": qstr(reverse),
        "bidirectional_F10_L1_strict_upper": qstr(bidirectional),
        "full_theta_one_raw_seed_coarea_integrability": "CERTIFIED",
        "arbitrary_Rn_owner_leaf_law_is_this_measure": False,
        "return_depth_weighted_owner_coarea_integrability": "NOT_CERTIFIED",
        "logical_scope": (
            "this repairs no Round50 recurrence coefficient; it proves that the "
            "physical seed coarea law itself is not the source of the generic divergence"
        ),
        "status": "CERTIFIED_RAW_SEED_THETA_ONE_L1_BOUND",
    }


def cancellation_and_owner_nonimplication() -> dict[str, Any]:
    rows = []
    for count in (1, 16, 64, 256):
        partial_mass = Q(count, K0 * (K0 + count))
        rows.append(
            {
                "active_strip_count": count,
                "ordinary_positive_mass": qstr(partial_mass),
                "owner_event_count_per_parent": 1,
                "signed_scalar_mass": "0",
                "C1_test_response_strict_lower": str(count),
            }
        )
    return {
        "countermodel": {
            "parent_index": "one disjoint parent W_k for every k>=6121",
            "base_mass": "a_k=1/(k*(k+1)); sum_(k>=6121)a_k=1/6121",
            "rank": "Bbar(k)=ceil(log2(2(k+1)^2))",
            "owned_pair_current": (
                "nu_k=a_k*2^Bbar(k)*(delta_1-delta_0); exactly one owned event on W_k"
            ),
            "constant_test": "nu_k(1)=0 for every k",
            "unit_C1_test": (
                "phi(y)=y/2 on [0,1], with norm_infinity(phi)+norm_infinity(phi')=1"
            ),
            "rank_response_lower": (
                "nu_k(phi)=a_k*2^Bbar(k)/2 >=(k+1)/k>1"
            ),
            "full_C1_partial_response": "sum of first N responses>N",
            "rows": rows,
            "rows_sha256": digest(rows),
        },
        "certified_inputs_satisfied_by_countermodel": [
            "finite ordinary mass",
            "one active rank strip and one owner event per parent",
            "pairwise plus/minus scalar cancellation on constants",
            "Bbar(k)=ceil(log2(2(k+1)^2))",
        ],
        "logical_conclusion": (
            "owner-once incidence and exact scalar +/- cancellation do not imply a "
            "finite theta=1 C1-dual or TV current"
        ),
        "does_not_claim_actual_billiard_current_diverges": True,
        "missing_pair_interface": (
            "for each same-ID hit/miss pair, a common-target image-distance d_k "
            "or an equivalent anisotropic test estimate"
        ),
        "sufficient_model_separation": (
            "sum_k d_k<infinity; in particular d_k=O(k^(-1-epsilon)) or "
            "d_k=O(c_target)=O(k^-2)"
        ),
        "global_Jx_reflection_supplies_same_target_small_separation": False,
        "raw_seed_tail_transfer_needed": (
            "alternatively transfer the 4^(-b) occurrence coarea tail to the "
            "same-ID arbitrary-R_n owner-leaf law uniformly in insertion time"
        ),
        "same_ID_full_ZB_one_step_recurrence": "NOT_CERTIFIED",
        "status": "CERTIFIED_OWNER_AND_SCALAR_CANCELLATION_NONIMPLICATION",
    }


def conditional_resolvent_update() -> dict[str, Any]:
    rho = SURVIVAL_R**BLOCK_DEPTH
    threshold = 2 * rho / (1 + rho)
    if not Q(99914, 100000) < threshold < Q(99915, 100000):
        raise RuntimeError("resolvent threshold")
    return {
        "sharp_requirement": "kappa_B<2rho/(1+rho)",
        "rho": "(111718729/111718750)^9148",
        "threshold_strict_bracket": (
            "99914/100000 < 2rho/(1+rho) < 99915/100000"
        ),
        "threshold_fraction_binary_sha256": fraction_digest(threshold),
        "finite_raw_seed_theta_one_injection_available": True,
        "finite_raw_seed_injection_is_recurrence_contraction": False,
        "owner_ZB_recurrence_coefficient_kappa_B": None,
        "unconditional_aggregate_ZB_resolvent": "NOT_CERTIFIED",
        "return_depth_face_tower_moment": "NOT_CERTIFIED",
        "status": "UNCHANGED_CONDITIONAL_RESOLVENT_WITH_REFINED_FORCING_SCOPE",
    }


def common_dynamic_envelope() -> dict[str, Any]:
    rows = []
    for exponent in (0, 4, 8, 12, 16):
        scale = 1 << exponent
        rows.append(
            {
                "L": scale,
                "branch": f"diag({scale},1/{scale})",
                "determinant": "1",
                "source_domain": f"[0,1/{scale}]x[0,1]",
                "target_domain": f"[0,1]x[0,1/{scale}]",
                "physical_test": "phi(y)=y_1/2",
                "physical_C1_sum_norm": "<=1 on the unit chart",
                "envelope_pullback_gradient_lower": qstr(Q(scale, 2)),
            }
        )
    if not Q(1) < QUARTER_CDYN_THRESHOLD < UNIT_CDYN_THRESHOLD:
        raise RuntimeError("dynamic thresholds")
    return {
        "regular_suffix_registry": (
            "S_reg is the standard-Borel registry of all finite regular suffix "
            "branches, including the identity branch"
        ),
        "finite_norm_pre_space": (
            "E_0={physical C1 tests phi: sup_(S in S_reg) "
            "norm(phi composed S)_C1(source(S))<infinity}"
        ),
        "common_test_space": (
            "T_env is the norm completion of E_0 for "
            "norm(phi)_env=sup_S norm(phi composed S)_C1"
        ),
        "branch_uniform_embedding": (
            "for every S, C_S:T_env->C1(source(S)), C_S phi=phi composed S, "
            "has operator norm <=1"
        ),
        "dual_pushforward": (
            "for T in (C1(source(S)))^*, S_*T belongs to T_env^* and "
            "norm(S_*T)<=norm(T)"
        ),
        "common_envelope_suffix_multiplier": "C_dyn=1",
        "branch_uniform_embedding_on_T_env": "CERTIFIED",
        "thresholds": {
            "preserve_source_quarter": qstr(QUARTER_CDYN_THRESHOLD),
            "preserve_subunit": qstr(UNIT_CDYN_THRESHOLD),
            "unit_multiplier_passes_both": True,
            "quarter_multiplier_slack": qstr(QUARTER_CDYN_THRESHOLD - 1),
        },
        "source_current_ratio": qstr(FULL_SOURCE_OVER_D1),
        "physical_compatibility_obstruction": {
            "claim": (
                "area preservation alone does not bound physical C1 into T_env"
            ),
            "rows": rows,
            "rows_sha256": digest(rows),
            "bounded_inclusion_C1_physical_into_T_env_from_current_inputs": False,
        },
        "billiard_specific_possible_replacement": (
            "a stable-curve/dynamic-Holder anisotropic test space with a proved "
            "full-gradient source-current pairing and an explicit comparison constant"
        ),
        "required_physical_CM2_test_algebra_contained_with_finite_constant": (
            "NOT_CERTIFIED"
        ),
        "F17_dynamic_test_operator_cost": "NOT_CERTIFIED",
        "complete_strong_F13_operator_intertwiner": "NOT_CERTIFIED",
        "logical_scope": (
            "T_env is a genuine common algebraic envelope and improves the "
            "branch-dependent formulation, but it may be too small for the physical tests"
        ),
        "status": "CERTIFIED_COMMON_ENVELOPE_ONLY_NOT_PHYSICAL_F17",
    }


def latest_technology_audit() -> dict[str, Any]:
    rows = [
        {
            "source": "Demers-Liverani arXiv:2606.10155v1",
            "relevant_mechanism": (
                "stable-curve Holder test norms and strong stable/unstable "
                "anisotropic Lasota-Yorke inequalities"
            ),
            "missing_here": (
                "no explicit arbitrary-suffix full-gradient F17 comparison constant "
                "below 7961063/7800000"
            ),
        },
        {
            "source": "Canestrari arXiv:2604.19671v2",
            "relevant_mechanism": "fixed-map standard-family Growth and small-hole response",
            "missing_here": (
                "no same-ID occurrence coarea-to-owner-leaf tail transfer and no "
                "common physical current test embedding"
            ),
        },
        {
            "source": "Climenhaga-Day arXiv:2604.25881v1",
            "relevant_mechanism": "qualitative sufficient rectangles and MME coding",
            "missing_here": "no quantitative boundary-Z_B recurrence or F17 test constant",
        },
    ]
    return {
        "rows": rows,
        "rows_sha256": digest(rows),
        "official_versions_checked_2026_07_20": [
            "2606.10155v1", "2604.19671v2", "2604.25881v1"
        ],
        "direct_gate5_upgrade_found": False,
        "status": "CHECKED_NO_DIRECT_NUMERIC_INTERFACE",
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "parameter_scope": "base parameter s=0",
            "depth_scope": (
                "raw depth-one occurrence seeds plus all finite regular suffixes; "
                "unbounded arbitrary-R_n owner-depth remains audited but unclosed"
            ),
            "claim_type": (
                "face-local rank isolation, raw-seed theta-one bound, exact "
                "owner/scalar nonimplication and common suffix-envelope frontier"
            ),
        },
        "five_face_rank_localization": face_local_rank_audit(),
        "raw_occurrence_seed_theta_one_bound": raw_seed_theta_one_bound(),
        "owner_scalar_cancellation_nonimplication": (
            cancellation_and_owner_nonimplication()
        ),
        "conditional_aggregate_ZB_update": conditional_resolvent_update(),
        "common_dynamic_suffix_envelope": common_dynamic_envelope(),
        "latest_technology_audit": latest_technology_audit(),
        "Gate5_maturity_update": {
            "previous_global_maturity": "10/18",
            "new_global_field_completed": None,
            "newly_certified_sublayers": [
                "five-face localization of the only full-rank insertion cost",
                "exact theta=1 L1 bound on the raw moving-occurrence seed coarea law",
                "owner-once plus scalar-cancellation C1-current nonimplication",
                "one common all-regular-suffix envelope with algebraic C_dyn=1",
            ],
            "reason_no_new_field_credit": (
                "the raw coarea tail is not transferred to the arbitrary-R_n owner "
                "leaf law, kappa_B is absent, and the common envelope lacks a "
                "bounded physical CM2 test inclusion"
            ),
            "current_global_maturity": "10/18",
            "complete_18_field_operator_block_count": 0,
        },
        "strict_nonpromotion": {
            "five_face_full_rank_localization": "CERTIFIED_MOVING_OCCURRENCE_ONLY",
            "raw_occurrence_seed_theta_one_L1": "CERTIFIED",
            "arbitrary_Rn_owner_theta_one_recurrence": "NOT_CERTIFIED",
            "same_ID_full_ZB_one_step_recurrence": "NOT_CERTIFIED",
            "unconditional_aggregate_ZB_resolvent": "NOT_CERTIFIED",
            "return_depth_weighted_face_integrability": "NOT_CERTIFIED",
            "common_algebraic_suffix_envelope_Cdyn_one": "CERTIFIED",
            "branch_uniform_physical_dynamic_test_embedding": "NOT_CERTIFIED",
            "complete_all_face_F10": "NOT_CERTIFIED",
            "F17_bulk_dynamic_test": "NOT_CERTIFIED",
            "strong_F13": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
            "F14_F15_F17_F18": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
            "Gate5_maturity": "10/18",
            "complete_18_field_operator_block_count": 0,
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
        "dependencies": dict(DEPENDENCIES),
        "result": result,
        "verdict": result["strict_nonpromotion"],
    }
    path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument(
        "--verifier",
        type=Path,
        default=(
            HERE
            / "cm2_gate5_round51_face_sparse_zb_dynamic_envelope_frontier_verifier.py"
        ),
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    result = build_result()
    strict = result["strict_nonpromotion"]
    print("RAW_SEED_THETA_ONE:", strict["raw_occurrence_seed_theta_one_L1"])
    print("OWNER_ZB_RECURRENCE:", strict["same_ID_full_ZB_one_step_recurrence"])
    print("COMMON_ENVELOPE:", strict["common_algebraic_suffix_envelope_Cdyn_one"])
    print("F17:", strict["F17_bulk_dynamic_test"])
    print("GATE5_MATURITY:", strict["Gate5_maturity"])
    print("CM2:", strict["CM2"])
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
