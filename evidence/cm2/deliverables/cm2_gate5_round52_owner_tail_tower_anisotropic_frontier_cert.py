#!/usr/bin/env python3
"""Round-52 Gate-5 owner-tail, face-tower and anisotropic frontier.

This append-only certificate closes one deliberately narrow measure-theoretic
join left open in Round 51.  At a *fixed insertion time*, with the terminal
depth restricted to the registered owner range ``j<n``, the owner-selected
regular arbitrary-R_n occurrence restrictions form disjoint source-marked
pieces and the owner operation only deletes representations.  Positivity
therefore transfers the raw occurrence 4^{-b} source-rank tail, with constant
one, to their aggregate marked law.  Each finite suffix pushforward preserves
record total mass and the retained source-rank mark.  Because the suffix maps
depend on the record, no domination on a common target Borel set is claimed.

The certificate does not turn this uniform-in-time bound into a face-tower
moment.  An exact nested-tube countermodel shows that exponentially decaying
two-dimensional survivor mass can coexist with constant trace mass on the
collision-null never-return set.  For the currently fixed aggregate weight,
this forces any recurrence deducible from the certified inputs to allow
kappa_B >= 1.  A separate exact interpolation audit shows that even granting
trace-mass decay at rate rho, every L^q bridge with q <= 2 misses the Round-50
threshold.

Finally, a stable-curve test candidate is typed and falsified for the full
Eulerian divergence current: stable-tangential tests do not control the
transverse derivative.  Thus no physical F17 or downstream field is promoted.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate5.round52-owner-tail-tower-anisotropic-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate5-round52-owner-tail-tower-anisotropic-frontier-manifest-2026-07-20.json"
)

DEPENDENCIES = {
    "cm2-gate5-round51-face-sparse-zb-dynamic-envelope-frontier-manifest-2026-07-20.json": (
        "1c4437a3c237739bacb823f0a9309626bea06b6f6562c1e268d589ed7debb7c5"
    ),
    "cm2-gate5-round50-owner-boundary-zb-f17-frontier-manifest-2026-07-19.json": (
        "c848c67bb9f2c0793d793c2ab4dca754cad71c507b9f0a06b9c29be3eaafeb46"
    ),
    "cm2-gate5-round49-typed-measure-f10-f17-frontier-manifest-2026-07-19.json": (
        "1a53a0bac41f6c0d6f8155c69b67daf31337b5f13578af9fb9f497d16277d6ad"
    ),
    "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json": (
        "988f364bd1e6943178238c072e725de01af36452ef25d179eae6aef4000f7916"
    ),
    "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json": (
        "ece7c97beeeb0b527434dc430e247ad0af407dc58b82d634da9e34a2f9e9521c"
    ),
    "cm2-gate45-endpoint-rank-first-order-cost-manifest-2026-07-16.json": (
        "7594afb9fc37660e8ce7c47d57bfd385dde65bcedfbdab5872f52699f5a4e72d"
    ),
    "cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json": (
        "86a63f3fa7b5b9cd7569bda0caf07d6e3637ba01eb0a3e2fdae9a9ba1c4a9db4"
    ),
    "cm2-gate5-round44-all-face-suffix-two-trace-f13-manifest-2026-07-19.json": (
        "3cf6635532622427bcde0525205212e1970b92ee56b2eb290ed01c1984443a9d"
    ),
}

B0 = 14
COAREA_MASS = Q(8064, 5)
RANK_TAIL_COEFFICIENT = Q(9158592, 6875)
FORWARD_F10_COEFFICIENT = 68
REVERSE_F10_COEFFICIENT = 35
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

    r51 = loaded[
        "cm2-gate5-round51-face-sparse-zb-dynamic-envelope-frontier-manifest-2026-07-20.json"
    ]["result"]
    seed51 = r51["raw_occurrence_seed_theta_one_bound"]
    if seed51["integral_2^B_dm_occ_strict_upper"] != (
        "23253221519103/880000"
    ):
        raise RuntimeError("Round51 theta-one seed")
    if seed51["arbitrary_Rn_owner_leaf_law_is_this_measure"] is not False:
        raise RuntimeError("Round51 measure boundary")
    if r51["strict_nonpromotion"]["Gate5_maturity"] != "10/18":
        raise RuntimeError("Round51 maturity")

    r50 = loaded[
        "cm2-gate5-round50-owner-boundary-zb-f17-frontier-manifest-2026-07-19.json"
    ]["result"]
    owner = r50["global_owner_aware_boundary_ZB_kernel"]
    if owner["owner_sets_pairwise_disjoint"] is not True:
        raise RuntimeError("Round50 owner disjointness")
    if owner["owner_sets_cover_all_regular_active_representations"] is not True:
        raise RuntimeError("Round50 owner coverage")
    if "time j<n" not in owner["global_index_space"]:
        raise RuntimeError("Round50 registered insertion-time range")
    if owner["corner_or_simultaneous_event_policy"] != (
        "cemetery, before owner minimization"
    ):
        raise RuntimeError("Round50 corner policy")

    r49 = loaded[
        "cm2-gate5-round49-typed-measure-f10-f17-frontier-manifest-2026-07-19.json"
    ]["result"]
    typed = r49["fixed_record_typed_measure_kernel"]
    if typed["occurrence_coarea_kernel"] != (
        "K_occ(y,e,A)=Z_N^-1*integral 1_(A intersect R_y)(iota_e(theta))*w_e(theta)dtheta"
    ):
        raise RuntimeError("Round49 occurrence restriction")
    if typed["recordwise_Radon_Nikodym_typing"] is not True:
        raise RuntimeError("Round49 typed kernel")

    path = loaded[
        "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json"
    ]["result"]
    arbitrary = path["C24_full_dimensional_arbitrary_n_candidate_path_join"]
    if arbitrary["path_universe_over_all_finite_n_is_countable"] is not True:
        raise RuntimeError("Round27 countability")
    levels = path["arbitrary_n_Rn_Qn_level_and_mass_schema"]
    if levels["infinite_first_return_partition_mod_null"] != (
        "C_s=disjoint_union_{n>=1}R_n; intersection_n Q_n has mu_s-mass 0"
    ):
        raise RuntimeError("Round27 return partition")
    if levels["path_fibre_refinement"][
        "same_level_fibres_pairwise_disjoint_by_frozen_exact_key_ownership"
    ] is not True:
        raise RuntimeError("Round27 fibre disjointness")

    carrier = loaded[
        "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json"
    ]["result"]
    if carrier["collision_SRB_leaf_disintegration"][
        "integrating_leaf_weights_recovers_mu_s_restricted_to_component"
    ] is not True:
        raise RuntimeError("Round35 leaf disintegration")
    if carrier["common_forward_reverse_carrier_pair"][
        "forward_and_reverse_share_identical_component_and_restriction"
    ] is not True:
        raise RuntimeError("Round35 same restriction")

    endpoint = loaded[
        "cm2-gate45-endpoint-rank-first-order-cost-manifest-2026-07-16.json"
    ]["result"]["endpoint_rank_tail_and_first_order_cost"]
    if endpoint["endpoint_tail"]["global_tail_constant"] != qstr(
        RANK_TAIL_COEFFICIENT
    ):
        raise RuntimeError("endpoint tail")
    if endpoint["raw_rank_moment"][
        "positive_coarea_mass_upper_before_Z_N_inverse"
    ] != qstr(COAREA_MASS):
        raise RuntimeError("endpoint mass")

    block = loaded[
        "cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json"
    ]["result"]["aggregate_canonical_Z_resolvent"]
    if block["mass_factor_rho"] != "(111718729/111718750)^9148":
        raise RuntimeError("Round42 rho")
    if block["explicit_block_index_weight"] != "w_Z=(1+rho^(-1))/2":
        raise RuntimeError("Round42 weight")

    f13 = loaded[
        "cm2-gate5-round44-all-face-suffix-two-trace-f13-manifest-2026-07-19.json"
    ]["result"]["occurrence_suffix_two_trace_transport"]["suffix_transport"]
    if f13["suffix_positive_pushforward_mass_constant"] != "1":
        raise RuntimeError("Round44 suffix mass")
    return loaded


def fixed_insertion_owner_tail_transfer() -> dict[str, Any]:
    rank_l1 = (1 << B0) * COAREA_MASS + RANK_TAIL_COEFFICIENT * Q(
        1, 1 << 13
    )
    forward = FORWARD_F10_COEFFICIENT * rank_l1
    reverse = REVERSE_F10_COEFFICIENT * rank_l1
    total = forward + reverse
    if rank_l1 != Q(23253221519103, 880000):
        raise RuntimeError("rank L1 arithmetic")
    if total != Q(2395081816467609, 880000):
        raise RuntimeError("F10 L1 arithmetic")
    rows = [
        {
            "operation": "restrict_to_regular_Rn_record",
            "measure_effect": "1_R*m_occ<=m_occ",
            "can_increase_positive_tail": False,
        },
        {
            "operation": "owner_minimization",
            "measure_effect": "owner set is a measurable subset of active representations",
            "can_increase_positive_tail": False,
        },
        {
            "operation": "sum_disjoint_owner_selected_source_pieces",
            "measure_effect": "marked source total and source-rank tail are <= those of m_occ",
            "can_increase_positive_tail": False,
        },
        {
            "operation": "finite_regular_suffix_pushforward",
            "measure_effect": (
                "record total mass and retained source-rank mark are preserved; "
                "common-target-set domination is not claimed"
            ),
            "can_increase_positive_tail": False,
        },
    ]
    return {
        "source_measure": "global positive raw occurrence coarea law m_occ over all 64 seeds",
        "fixed_index": (
            "one insertion time j; aggregate over the countable regular arbitrary-R_n "
            "records with n>j and over their owner-selected representations"
        ),
        "same_ID_restriction_formula": "m_(j,a)^owner=1_(E_(j,a)^owner intersect R_(j,a)^reg)*m_occ",
        "positivity_and_disjointness_inequality": (
            "on the source-marked disjoint union, sum_a m_(j,a)^owner{B>b}"
            "<=m_occ{B>b}; the same holds for total mass"
        ),
        "target_Borel_set_domination_after_distinct_suffixes": False,
        "operations": rows,
        "operations_sha256": digest(rows),
        "transferred_rank_tail": (
            "sum_a m_(j,a)^owner{B>b}<=(9158592/6875)*4^(-b), b>=14"
        ),
        "transferred_integral_2^B_strict_upper": qstr(rank_l1),
        "transferred_forward_F10_L1_strict_upper": qstr(forward),
        "transferred_reverse_F10_L1_strict_upper": qstr(reverse),
        "transferred_bidirectional_F10_L1_strict_upper": qstr(total),
        "transfer_constant": "1",
        "arbitrary_finite_regular_suffix_TV_scope": True,
        "uniform_in_j_bound_has_decay_in_j": False,
        "sums_over_insertion_times": False,
        "return_depth_face_tower_moment": "NOT_CERTIFIED",
        "status": "CERTIFIED_FIXED_INSERTION_SAME_ID_OWNER_TAIL_TRANSFER_ONLY",
    }


def null_survivor_face_tower_countermodel() -> dict[str, Any]:
    rho = SURVIVAL_R**BLOCK_DEPTH
    w = (1 + 1 / rho) / 2
    threshold = 1 / w
    if not Q(0) < rho < 1:
        raise RuntimeError("rho range")
    if not Q(1) < w < 1 / rho:
        raise RuntimeError("weight range")
    if w * rho != (1 + rho) / 2 or not w * rho < 1:
        raise RuntimeError("forcing summability")
    rows = []
    for p in (0, 1, 4, 16):
        rows.append(
            {
                "block_index": p,
                "collision_survivor_mass": "1" if p == 0 else f"rho^{p}",
                "trace_survivor_mass": "1",
                "constant_rank": B0,
                "owner_ZB_charge": str(1 << B0),
            }
        )
    return {
        "space": "X=[0,1]^2 with collision volume mu=dx*dy",
        "face": "Gamma={0}x[0,1] with trace law nu=H^1|Gamma",
        "survivors": "Q_p=[0,rho^p]x[0,1]",
        "return_layers": "R_p=Q_(p-1)\\Q_p for p>=1",
        "never_return_set": "intersection_p Q_p=Gamma",
        "collision_mass": "mu(Q_p)=rho^p and mu(Gamma)=0",
        "trace_mass": "nu(Q_p)=nu(Gamma)=1 for every p",
        "rank": "B=14 identically on Gamma",
        "fixed_time_raw_tail_and_all_q_moments": "finite (the tail above rank 14 is zero)",
        "same_ID_owner_restriction": "one owner event on the same face ID in each block",
        "rows": rows,
        "rows_sha256": digest(rows),
        "owner_charge_sequence": "b_p=2^14 for every p",
        "ordinary_forcing_model": "z_p=m_p=rho^p",
        "weighted_forcing_sum": "sum_p w_Z^p*rho^p=1/(1-w_Z*rho)<infinity",
        "weighted_owner_charge_sum": "sum_p w_Z^p*2^14=infinity because w_Z>1",
        "recurrence_conclusion": (
            "for any finite A_B,C_B and 0<=kappa_B<1, b_(p+1)<=kappa_B*b_p+"
            "A_B*z_p+C_B*m_p fails for all sufficiently large p"
        ),
        "minimal_asymptotic_kappa_allowed_by_current_inputs": ">=1",
        "Round50_threshold": "2rho/(1+rho)<1",
        "threshold_fraction_binary_sha256": fraction_digest(threshold),
        "logical_scope": (
            "exact nonimplication model only; it does not assert that the physical "
            "billiard trace charges concentrate on its never-return set"
        ),
        "new_missing_interface": (
            "trace-nullity of the collision-null never-return/cemetery set or a "
            "quantitative trace-survivor contraction"
        ),
        "status": "CERTIFIED_NULL_SURVIVOR_FACE_TOWER_NONIMPLICATION",
    }


def lp_interpolation_threshold_audit() -> dict[str, Any]:
    rho = SURVIVAL_R**BLOCK_DEPTH
    threshold = 2 * rho / (1 + rho)
    # threshold < sqrt(rho) is equivalent to
    # 4*rho < (1+rho)^2, i.e. (1-rho)^2>0.
    if not threshold * threshold < rho:
        raise RuntimeError("AM-GM threshold separation")
    rows = [
        {
            "q": "3/2",
            "Holder_decay_exponent": "1/3",
            "effective_kappa": "rho^(1/3)",
            "below_fixed_Round50_threshold": False,
        },
        {
            "q": "2 (even if endpoint were granted)",
            "Holder_decay_exponent": "1/2",
            "effective_kappa": "sqrt(rho)",
            "below_fixed_Round50_threshold": False,
        },
    ]
    return {
        "hypothetical_extra_input": (
            "trace mass nu_p(total)<=rho^p*nu_0(total), which is not currently certified"
        ),
        "Holder_bound": (
            "if ||2^B||_(L^q(nu_0))<infinity then b_p<=C_q*rho^(p*(1-1/q))"
        ),
        "effective_recurrence_factor": "kappa_q=rho^(1-1/q)",
        "available_raw_moment_range": "q<2; q=3/2 is explicitly certified",
        "fixed_threshold": "2rho/(1+rho)",
        "exact_endpoint_separation": (
            "2rho/(1+rho)<sqrt(rho), equivalent to (1-rho)^2>0"
        ),
        "all_q_at_most_two_fail_fixed_threshold": True,
        "rows": rows,
        "rows_sha256": digest(rows),
        "required_for_fixed_weight_route": (
            "a genuine q>2 owner-law moment together with trace-survivor decay, "
            "or a direct recurrence/cancellation sharper than Holder interpolation"
        ),
        "weaker_weight_route": (
            "if trace-survivor decay were proved, q=3/2 could use "
            "w_face=(1+rho^(-1/3))/2<w_Z, since w_face*rho^(1/3)="
            "(1+rho^(1/3))/2<1"
        ),
        "weaker_weight_route_is_currently_certified": False,
        "status": "CERTIFIED_FIXED_WEIGHT_LQ_INTERPOLATION_OBSTRUCTION",
    }


def anisotropic_f17_candidate_audit() -> dict[str, Any]:
    rows = []
    for scale in (1, 16, 256, 4096, 65536):
        rows.append(
            {
                "L": scale,
                "domain": f"[0,1/{scale}]x[0,1]",
                "stable_direction": "e_2",
                "test": f"phi_L(u,s)={scale}*u",
                "stable_curve_test_norm": "1",
                "vector_current": "K=e_1",
                "source_L1_vector_mass": qstr(Q(1, scale)),
                "divergence_pairing": "1",
                "pairing_to_source_mass_ratio": str(scale),
            }
        )
    return {
        "literature_candidate": (
            "Demers--Liverani stable-curve anisotropic norms: distributions are "
            "tested against Holder observables on stable curves, with a separate "
            "transverse/unstable comparison seminorm"
        ),
        "candidate_scalar_test_norm": (
            "norm(phi)_sc=norm(phi)_infinity+norm(partial_stable phi)_infinity"
        ),
        "candidate_suffix_advantage": (
            "stable directions contract under the matched inverse/transfer geometry"
        ),
        "full_Eulerian_current_pairing_needed": (
            "T_K(phi)=integral K dot grad(phi) dmu for K=X*(P_j h), not only a "
            "stable-tangential derivative"
        ),
        "transverse_pairing_countermodel": {
            "rows": rows,
            "rows_sha256": digest(rows),
            "conclusion": (
                "no finite constant controls the full divergence pairing by the "
                "stable-curve scalar test norm and the source L1 vector mass"
            ),
        },
        "physical_alignment_available": (
            "no certified identity forces the Eulerian generator X to have zero "
            "transverse component on every arbitrary-R_n branch"
        ),
        "adding_uniform_full_gradient_repairs_source_pairing": True,
        "adding_uniform_full_gradient_preserves_suffix_multiplier": False,
        "reason_full_gradient_fails": (
            "the Round51 area-preserving diagonal family makes the full-gradient "
            "pullback multiplier unbounded"
        ),
        "required_vector_current_space": (
            "one common anisotropic H(div)-type graph space containing -div(K)+B, "
            "with an explicit source injection for both components of K, trace "
            "injection for B, physical CM2 observable pairing, and suffix pushforward "
            "constant below 7961063/7800000"
        ),
        "official_source_checked": (
            "Demers--Liverani, arXiv:2606.10155v1, Sections 3.5 and the stable/"
            "unstable norm discussion"
        ),
        "official_source_supplies_required_vector_current_injection": False,
        "unified_physical_anisotropic_CM2_F17_space": "NOT_CERTIFIED",
        "F17_dynamic_test_operator_cost": "NOT_CERTIFIED",
        "status": "CERTIFIED_STABLE_CURVE_CANDIDATE_TRANSVERSE_CURRENT_OBSTRUCTION",
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
                "all finite arbitrary-R_n regular records at each fixed insertion "
                "time j<n, followed by an unbounded face-tower nonimplication audit"
            ),
            "claim_type": (
                "fixed-insertion same-ID owner-tail transfer, exact null-survivor "
                "and fixed-weight interpolation obstructions, and a typed "
                "stable-curve F17 candidate audit"
            ),
        },
        "fixed_insertion_same_ID_owner_tail_transfer": (
            fixed_insertion_owner_tail_transfer()
        ),
        "null_survivor_face_tower_countermodel": (
            null_survivor_face_tower_countermodel()
        ),
        "fixed_weight_Lq_interpolation_audit": lp_interpolation_threshold_audit(),
        "physical_anisotropic_F17_candidate_audit": (
            anisotropic_f17_candidate_audit()
        ),
        "latest_technology_audit": {
            "official_version_checked_2026_07_20": "2606.10155v1",
            "relevant_mechanism": (
                "stable-curve Holder tests and strong stable/unstable anisotropic norms"
            ),
            "direct_same_ID_face_tower_or_vector_current_F17_upgrade_found": False,
            "status": "CHECKED_NO_DIRECT_TYPED_UPGRADE",
        },
        "Gate5_maturity_update": {
            "previous_global_maturity": "10/18",
            "new_global_field_completed": None,
            "newly_certified_sublayers": [
                "constant-one same-ID owner tail transfer at each fixed insertion time",
                "collision-null never-return set can retain full trace mass countermodel",
                "q<=2 Holder interpolation misses the fixed Round50 kappa threshold",
                "stable-curve scalar test norms do not control the transverse Eulerian current",
            ],
            "reason_no_new_field_credit": (
                "the owner bound has no insertion-time decay, the face-tower/"
                "cemetery trace contraction is absent, and no vector-current "
                "anisotropic F17 space with an explicit physical constant is installed"
            ),
            "current_global_maturity": "10/18",
            "complete_18_field_operator_block_count": 0,
        },
        "strict_nonpromotion": {
            "fixed_insertion_same_ID_owner_tail_transfer": "CERTIFIED",
            "all_insertion_time_owner_tail_sum": "NOT_CERTIFIED",
            "same_ID_full_ZB_one_step_recurrence": "NOT_CERTIFIED",
            "owner_ZB_kappa_below_fixed_threshold": "NOT_CERTIFIED",
            "unconditional_aggregate_ZB_resolvent": "NOT_CERTIFIED",
            "return_depth_weighted_face_integrability": "NOT_CERTIFIED",
            "trace_nullity_of_never_return_cemetery": "NOT_CERTIFIED",
            "unified_physical_anisotropic_CM2_F17_space": "NOT_CERTIFIED",
            "F17_bulk_dynamic_test": "NOT_CERTIFIED",
            "complete_all_face_F10": "NOT_CERTIFIED",
            "strong_F13": "NOT_CERTIFIED",
            "F14_F15_F17_F18": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
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
            / "cm2_gate5_round52_owner_tail_tower_anisotropic_frontier_verifier.py"
        ),
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    strict = build_result()["strict_nonpromotion"]
    print(
        "FIXED_INSERTION_OWNER_TAIL:",
        strict["fixed_insertion_same_ID_owner_tail_transfer"],
    )
    print("OWNER_KAPPA:", strict["owner_ZB_kappa_below_fixed_threshold"])
    print("FACE_TOWER:", strict["return_depth_weighted_face_integrability"])
    print("F17:", strict["F17_bulk_dynamic_test"])
    print("GATE5_MATURITY:", strict["Gate5_maturity"])
    print("CM2:", strict["CM2"])
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
