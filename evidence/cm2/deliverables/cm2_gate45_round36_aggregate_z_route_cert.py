#!/usr/bin/env python3
"""Aggregate-Z route selection and exact new-face injection recurrence.

Round 35 supplied same-ID forward/reverse carriers and a physical additive
rank charge, but not the retained-depth moment needed after cellwise
normalization.  This certificate compares the two remaining routes without
silently strengthening either one.

The aggregate route keeps the survivor/return family unnormalised.  Its
boundary functional obeys the exact abstract recurrence

    Z_(n+1) <= a Z_n + b m_n + J_n,

where ``a<1`` and ``b`` are the frozen closed-map Growth constants and J_n
is the unnormalised cost of genuinely new physical face endpoints.  The
certificate solves this recurrence pointwise and in weighted l1.  Thus a
uniform or weighted bound for J_n is sufficient; no inverse component mass
or cellwise 2^D factor is then used.

The retained-depth fallback is not derivable from the current one-time rank
moment.  An explicit perfectly correlated rank process has the certified
one-time 4^-b tail and every D1 L^(6/5) moment, while every fixed positive
moment of the n-step image-recut product fails for sufficiently large n.
This is a logical countermodel to an inference, not a claim about the
physical billiard.

Round 36 all-face F9 fills the geometric C2 part of J_n.  F10, global trace
pullback, cemetery and F14--F18 still prevent a numerical J bound, so Gate 4
and Gate 5 remain fail-closed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate45.round36-aggregate-z-route.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate45-round36-aggregate-z-route-manifest-2026-07-19.json"
)
DEPENDENCIES = {
    "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json": (
        "ece7c97beeeb0b527434dc430e247ad0af407dc58b82d634da9e34a2f9e9521c"
    ),
    "cm2-gate45-round35-physical-rn-rank-sum-lp-manifest-2026-07-19.json": (
        "7980e90ce45edfd3012b265315e6877e38eb4604ab0219205ec966ad43a8cd75"
    ),
    "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json": (
        "b03c5ae0e400045f087cfbd1aa8c843990edebe517a4dde786b0718446db7c1d"
    ),
    "cm2-gate25-all-component-characteristic-frontier-manifest-2026-07-17.json": (
        "41c766d25b007944313db93b389a616d086a7318700a867e13d90aedd159be35"
    ),
    "cm2-gate34-c24-sparse-hit-gap-manifest-2026-07-18.json": (
        "02277a2c10ea905fd8a4cf9998ae364a4b024087624fd3bea0a8a4175405727d"
    ),
    "cm2-gate4-fixed-core-green-kernel-unbounded-cut-frontier-manifest-2026-07-17.json": (
        "3475b2cf6af105b4d229e9683eb2f61433be2e4cefc8f1e8f2318c07762f3dd5"
    ),
    "cm2-gate5-round36-all-face-rank-path-f9-manifest-2026-07-19.json": (
        "f603dd8e638d661b22c746742a5e5c3fd48242f4c0ad40bb35fbe74d35325788"
    ),
}

A = Q(360134800, 360493663)
B = Q(2 * 10**90)
MARGIN = 1 - A
RESOLVENT = 1 / MARGIN
FIELD7_FACTOR = Q(580000, 1999)
HIT_EPSILON = Q(21, 111718750)
SURVIVAL_FACTOR = 1 - HIT_EPSILON


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def load(name: str) -> dict[str, Any]:
    path = HERE / name
    if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
        raise RuntimeError(f"unsafe dependency: {name}")
    if sha(path) != DEPENDENCIES[name]:
        raise RuntimeError(f"dependency hash: {name}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"dependency root: {name}")
    return value


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else (
        f"{value.numerator}/{value.denominator}"
    )


def aggregate_recurrence() -> dict[str, Any]:
    if MARGIN != Q(358863, 360493663):
        raise RuntimeError("margin")
    if RESOLVENT != Q(360493663, 358863):
        raise RuntimeError("resolvent")
    weighted_base = Q(A.denominator + A.numerator, 2 * A.numerator)
    weighted_ratio = weighted_base * A
    weighted_margin = 1 - weighted_ratio
    if not weighted_base > 1 or not weighted_ratio < 1:
        raise RuntimeError("weighted ratio")
    if weighted_ratio != Q(720628463, 720987326):
        raise RuntimeError("weighted ratio exact")
    if weighted_margin != Q(358863, 720987326):
        raise RuntimeError("weighted margin exact")

    return {
        "aggregate_family": (
            "one unnormalised same-ID standard-family representation of the "
            "whole physical survivor/return level, retaining branch labels"
        ),
        "closed_map_step": "Z(T_*F)<=a*Z(F)+b*mass(F)",
        "a": qstr(A),
        "b": qstr(B),
        "contraction_margin": qstr(MARGIN),
        "new_face_injection": (
            "J_n is the unnormalised boundary numerator created at time n by "
            "C24 complement, owner/singularity, moving occurrence and cemetery faces"
        ),
        "recurrence": "Z_(n+1)<=a*Z_n+b*m_n+J_n",
        "pointwise_solution": (
            "Z_n<=a^n*Z_0+sum_{j=0}^{n-1}a^(n-1-j)*(b*m_j+J_j)"
        ),
        "uniform_forcing_conclusion": (
            "if m_j<=m_* and J_j<=J_*, then "
            "sup_n Z_n<=Z_0+(b*m_*+J_*)/(1-a)"
        ),
        "exact_resolvent": qstr(RESOLVENT),
        "one_explicit_growth_compatible_weight": qstr(weighted_base),
        "weighted_growth_ratio": qstr(weighted_ratio),
        "weighted_growth_margin": qstr(weighted_margin),
        "weighted_l1_conclusion": (
            "for any 1<w<1/a, sum_n w^n Z_n is bounded by the geometric "
            "resolvent whenever sum_n w^n m_n and sum_n w^n J_n are finite"
        ),
        "inverse_component_mass_used": False,
        "cellwise_retained_depth_D_used": False,
        "abstract_aggregate_Z_transfer": "CERTIFIED",
    }


def current_j_interface() -> dict[str, Any]:
    return {
        "decomposition": "J_n=J_core,n+J_owner,n+J_occurrence,n+J_cemetery,n",
        "same_ID_requirements": [
            "the face instance and both one-sided traces use the same R_n component ID",
            "the forward/reverse views charge one physical face injection, not two",
            "the unnormalised trace weight is integrated before any leaf normalization",
        ],
        "available": {
            "common_arbitrary_Rn_fw_rev_carrier": "CERTIFIED",
            "all_five_face_kind_F8_transversality": "CERTIFIED_1/5",
            "all_five_face_kind_F9_rank_path_C2": "CERTIFIED_PARAMETERIZED",
            "moving_occurrence_seed_F10": "CERTIFIED_64_SEEDS",
            "fixed_core_delay_Green_kernel": "CERTIFIED",
        },
        "missing": {
            "all_pullback_F10_coarea_density_regular_bound": "NOT_CERTIFIED",
            "return_wide_C1_face_trace_pullback_F12": "NOT_CERTIFIED",
            "moving_boundary_current_F13_on_all_Rn_IDs": "NOT_CERTIFIED",
            "regular_density_operator_cost_F14": "NOT_CERTIFIED",
            "standard_family_operator_cost_F15": "NOT_CERTIFIED",
            "flux_face_operator_cost_F16": "NOT_CERTIFIED",
            "dynamic_test_operator_cost_F17": "NOT_CERTIFIED",
            "operator_phase_block_F18": "NOT_CERTIFIED",
            "strong_cemetery_payload": "NOT_CERTIFIED",
        },
        "uniform_J_upper": "NOT_CERTIFIED",
        "weighted_J_l1": "NOT_CERTIFIED",
        "first_remaining_equation": (
            "prove sum/trace bounds for J_n on the parameterized all-face F9 atlas"
        ),
    }


def correlated_rank_countermodel() -> dict[str, Any]:
    # Put P(B=14)=1-4^-14 and P(B=b)=3*4^-b for b>=15.
    # Then P(B>b)=4^-b for every integer b>=14.
    atom_14 = 1 - Q(1, 4**14)
    tail_mass = Q(1, 4**14)
    if atom_14 + tail_mass != 1:
        raise RuntimeError("rank law normalization")

    # A rational upper for the finite 3/2 moment.  For b>=15,
    # 3*4^-b*2^(3b/2)=3*2^(-b/2).  Pair b=2k,2k+1 and use
    # 2^(-1/2)<1 to majorize each pair by 6*2^-k.
    tail_moment_upper = Q(12, 1 << 8)
    base_moment = Q(1 << 21) * atom_14
    moment_upper = base_moment + tail_moment_upper
    if not moment_upper < Q(134217735, 64):
        raise RuntimeError("rank countermodel moment")

    return {
        "purpose": (
            "logical non-implication: one-time rank tails and D1 moments do "
            "not control arbitrary-time image-recut products"
        ),
        "law": [
            "P(B=14)=1-4^-14",
            "P(B=b)=3*4^-b for every integer b>=15",
        ],
        "exact_tail": "P(B>b)=4^-b for every integer b>=14",
        "tail_is_stronger_than_physical_input": "4^-b<2*4^-b",
        "finite_one_time_moment": (
            "E[2^(3B/2)] is finite and below the frozen rational rank upper"
        ),
        "frozen_rank_moment_upper": "134217735/64",
        "countermodel_rank_moment_rational_upper": qstr(moment_upper),
        "perfect_time_correlation": "B_i=B for every i>=1",
        "D1_property": (
            "for every fixed n, (sum_{i=1}^n 2^B_i) has finite L^(6/5) moment"
        ),
        "image_recut_lower_model": "N_recut,n proportional to 2^(sum_i B_i)=2^(nB)",
        "failure": (
            "for every beta>0, E[N_recut,n^beta]=infinity once beta*n>=2"
        ),
        "reason": "the tail series contains sum_{b>=15}3*2^((beta*n-2)*b)",
        "claims_physical_rank_process_has_perfect_correlation": False,
        "conclusion": (
            "the current marginal rank/D1 evidence cannot certify a uniform "
            "positive retained-depth or image-recut product moment"
        ),
    }


def route_decision() -> dict[str, Any]:
    naive = FIELD7_FACTOR * A
    if not naive > 1:
        raise RuntimeError("naive F7")
    return {
        "naive_all_key_characteristic_factor": qstr(FIELD7_FACTOR),
        "naive_restriction_then_step_coefficient": qstr(naive),
        "naive_cellwise_F7_is_contraction": False,
        "physical_survivor_block_factor": qstr(SURVIVAL_FACTOR),
        "physical_sparse_block_length": "N_open_exists_uniformly_but_is_not_numeric",
        "cellwise_D_route": (
            "DEFERRED: current D1 marginal control does not dominate common-carrier image recuts"
        ),
        "aggregate_Z_route": (
            "SELECTED_PRIMARY: it removes inverse mass and image-recut count from the recovery weight"
        ),
        "route_selection_status": "CERTIFIED_LOGICAL_FRONTIER",
        "next_shortest_interface": (
            "all-pullback F10 followed by same-ID F12/F13 trace assembly and a weighted J_n bound"
        ),
    }


def build_result() -> dict[str, Any]:
    carrier = load(
        "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json"
    )["result"]
    rank = load(
        "cm2-gate45-round35-physical-rn-rank-sum-lp-manifest-2026-07-19.json"
    )["result"]
    growth = load(
        "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json"
    )
    characteristic = load(
        "cm2-gate25-all-component-characteristic-frontier-manifest-2026-07-17.json"
    )["result"]
    sparse = load(
        "cm2-gate34-c24-sparse-hit-gap-manifest-2026-07-18.json"
    )["result"]
    green = load(
        "cm2-gate4-fixed-core-green-kernel-unbounded-cut-frontier-manifest-2026-07-17.json"
    )["result"]
    f9 = load(
        "cm2-gate5-round36-all-face-rank-path-f9-manifest-2026-07-19.json"
    )["result"]

    if carrier["common_forward_reverse_carrier_pair"][
        "actual_parameterized_common_fw_rev_carrier_pair_registry"
    ] != "CERTIFIED":
        raise RuntimeError("carrier")
    if rank["physical_rank_sum_weighted_tail"]["uniform_exponential_tail"] != (
        "CERTIFIED_FOR_ADDITIVE_D1_RANK_SUM_CHARGE"
    ):
        raise RuntimeError("D1")
    if growth["replay_summary"]["vartheta_p"] != qstr(A):
        raise RuntimeError("growth a")
    if characteristic["all_key_all_component_characteristic_registry"][
        "uniform_unnormalized_characteristic_Z_multiplier_upper"
    ] != qstr(FIELD7_FACTOR):
        raise RuntimeError("F7 factor")
    if sparse["uniform_recovered_cone_hit_gap"][
        "explicit_per_block_hit_gap_epsilon"
    ] != qstr(HIT_EPSILON):
        raise RuntimeError("hit epsilon")
    if green["fixed_core_green_kernel"][
        "fixed_core_unbounded_transport_delay_Green_kernel"
    ] != "CERTIFIED":
        raise RuntimeError("green kernel")
    if f9["strict_nonpromotion"][
        "complete_F9_physical_face_C2_parameterized_atlas"
    ] != "CERTIFIED":
        raise RuntimeError("F9")

    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": DEPENDENCIES,
            "old_artifacts_modified": False,
            "parameter_scope": "uniformly for every fixed |s|<=1/400",
            "depth_scope": "all finite C24 return/survivor levels",
        },
        "aggregate_Z_new_face_recurrence": aggregate_recurrence(),
        "same_ID_new_face_injection_interface": current_j_interface(),
        "retained_depth_marginal_countermodel": correlated_rank_countermodel(),
        "round36_route_decision": route_decision(),
        "strict_nonpromotion": {
            "abstract_recurrence_supplies_physical_J_bound": False,
            "all_face_F9_supplies_all_face_F10_or_trace_cost": False,
            "D1_tail_dominates_image_recut_product": False,
            "physical_aggregate_Z_uniform_bound": "NOT_CERTIFIED",
            "complete_numeric_C_fw_C_rev": "NOT_CERTIFIED",
            "final_same_ID_q": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "Gate5_maturity": "7/18",
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    result["internal_replay_digest"] = digest(result)
    return result


def manifest(verifier: Path) -> dict[str, Any]:
    result = build_result()
    return {
        "schema": MANIFEST_SCHEMA,
        "certificate_sha256": sha(Path(__file__).resolve()),
        "verifier_sha256": sha(verifier.resolve()),
        "dependencies": DEPENDENCIES,
        "result": result,
        "verdict": result["strict_nonpromotion"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--print-manifest", action="store_true")
    parser.add_argument(
        "--verifier",
        type=Path,
        default=HERE / "cm2_gate45_round36_aggregate_z_route_verifier.py",
    )
    args = parser.parse_args()
    if args.print_manifest:
        print(json.dumps(manifest(args.verifier), indent=2, sort_keys=True))
        return 0
    result = build_result()
    print("AGGREGATE_Z_RECURRENCE: CERTIFIED_ABSTRACTLY")
    print(result["round36_route_decision"]["aggregate_Z_route"])
    print("PHYSICAL_J_BOUND: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
