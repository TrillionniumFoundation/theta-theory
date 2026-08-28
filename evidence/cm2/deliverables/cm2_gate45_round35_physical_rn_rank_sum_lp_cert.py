#!/usr/bin/env python3
"""Physical L^(6/5) tail for the additive incidence-rank R_n charge."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate45.round35-physical-rn-rank-sum-lp.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate45-round35-physical-rn-rank-sum-lp-manifest-2026-07-19.json"
)
DEPENDENCIES = {
    "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json": (
        "ece7c97beeeb0b527434dc430e247ad0af407dc58b82d634da9e34a2f9e9521c"
    ),
    "cm2-gate34-c24-sparse-hit-gap-manifest-2026-07-18.json": (
        "02277a2c10ea905fd8a4cf9998ae364a4b024087624fd3bea0a8a4175405727d"
    ),
    "cm2-gate34-collision-srb-kac-return-baseline-manifest-2026-07-18.json": (
        "1213a6b66fca6d3a776a75244c334dacfeb822240f7c7eeadcb565553e62a53a"
    ),
    "cm2-gate45-endpoint-rank-first-order-cost-manifest-2026-07-16.json": (
        "7594afb9fc37660e8ce7c47d57bfd385dde65bcedfbdab5872f52699f5a4e72d"
    ),
    "cm2-gate45-round28-weighted-tail-transfer-frontier-manifest-2026-07-18.json": (
        "eef1071c1f4973892bf5e450421f3b91de7a2b426165e6a8c6f8bb4404eeac57"
    ),
    "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json": (
        "988f364bd1e6943178238c072e725de01af36452ef25d179eae6aef4000f7916"
    ),
    "cm2-gate45-round34-weighted-tail-interface-refresh-manifest-2026-07-19.json": (
        "d5f595b67a437f60d7e8d65070667495eeaba0f248042980fadebec9107cd371"
    ),
}

TAIL_A = Q(550000, 147)
TAIL_EPSILON = Q(21, 111718750)
TAIL_R = 1 - TAIL_EPSILON
RANK_MOMENT = Q(134217735, 64)
P = Q(6, 5)
Q0 = Q(3, 2)
RANK_COST = 151
K_RANK = Q(22801) * TAIL_A * RANK_MOMENT * Q(250) / TAIL_EPSILON**3


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
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def rank_moment_derivation() -> dict[str, Any]:
    base = Q(1 << 21)
    tail = Q(7, 64)
    if base + tail != RANK_MOMENT:
        raise RuntimeError("rank moment arithmetic")
    return {
        "rank": (
            "B_inc(x)=max(14,ceil(log2(1/cp(x))),"
            "ceil(log2(1/cp(T_s*x))))"
        ),
        "collision_coordinate": "p=sin(phi), cp=sqrt(1-p^2)",
        "one_endpoint_exact_probability": (
            "mu_s{cp<2^-b}=1-sqrt(1-4^-b)<4^-b"
        ),
        "invariance_union_bound": "mu_s{B_inc>b}<2*4^-b for every integer b>=14",
        "chosen_q0": qstr(Q0),
        "layer_cake_identity": (
            "integral(a^B)dmu=a^14+sum_{b>=14}(a^(b+1)-a^b)"
            "*mu{B>b}"
        ),
        "a": "2^(3/2)=2*sqrt(2)",
        "a_power_14": qstr(base),
        "rational_majorants": [
            "a-1<2",
            "a/4=1/sqrt(2)",
            "(a/4)^14=1/128",
            "sum_{b>=14}(a/4)^b<7/256",
        ],
        "tail_contribution_strict_upper": qstr(tail),
        "global_collision_SRB_integral_2^(3B_inc/2)_strict_upper": qstr(
            RANK_MOMENT
        ),
        "status": "CERTIFIED_PHYSICAL_GLOBAL_Q0_MOMENT",
    }


def build_result() -> dict[str, Any]:
    carrier = load(
        "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json"
    )["result"]
    sparse = load(
        "cm2-gate34-c24-sparse-hit-gap-manifest-2026-07-18.json"
    )
    kac = load(
        "cm2-gate34-collision-srb-kac-return-baseline-manifest-2026-07-18.json"
    )["result"]
    endpoint = load(
        "cm2-gate45-endpoint-rank-first-order-cost-manifest-2026-07-16.json"
    )["result"]["endpoint_rank_tail_and_first_order_cost"]
    transfer = load(
        "cm2-gate45-round28-weighted-tail-transfer-frontier-manifest-2026-07-18.json"
    )["result"]
    path = load(
        "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json"
    )["result"]
    refresh = load(
        "cm2-gate45-round34-weighted-tail-interface-refresh-manifest-2026-07-19.json"
    )["result"]

    if carrier["common_forward_reverse_carrier_pair"][
        "actual_parameterized_common_fw_rev_carrier_pair_registry"
    ] != "CERTIFIED":
        raise RuntimeError("common carrier")
    if carrier["strict_nonpromotion"]["final_same_ID_q"] != "NOT_CERTIFIED":
        raise RuntimeError("carrier scope")
    if sparse["result"]["uniform_recovered_cone_hit_gap"][
        "explicit_per_block_hit_gap_epsilon"
    ] != qstr(TAIL_EPSILON):
        raise RuntimeError("epsilon")
    if sparse["result"]["uniform_recovered_cone_hit_gap"][
        "explicit_per_block_survival_factor"
    ] != qstr(TAIL_R):
        raise RuntimeError("survival factor")
    if kac["frozen_measure_space_contract"]["invariant_probability"] != (
        "mu_s=normalized_cos(phi)dr_dphi=normalized_dr_dp"
    ):
        raise RuntimeError("collision probability")
    if endpoint["one_collision_birkhoff_derivative"][
        "forward_derivative_bound"
    ] != "||DF_e||_infinity<150/cp_miss":
        raise RuntimeError("forward derivative")
    if endpoint["one_collision_birkhoff_derivative"][
        "reverse_derivative_bound"
    ] != "||DF_e^-1||_infinity<150/cp_source":
        raise RuntimeError("reverse derivative")
    if transfer["weighted_tail_transfer_theorem"]["global_Lp_transfer"][
        "status"
    ] != "CERTIFIED_CONDITIONAL_TRANSFER_THEOREM":
        raise RuntimeError("Lp transfer")
    if path["arbitrary_n_Rn_Qn_level_and_mass_schema"][
        "unweighted_exponential_Rn_Qn_mass_ledger"
    ] != "CERTIFIED_SYMBOLIC":
        raise RuntimeError("Rn ledger")
    if refresh["one_collision_endpoint_coarea_L3over2_seed"][
        "physical_first_return_Lp_transfer_hypothesis_filled"
    ] is not False:
        raise RuntimeError("round34 scope")
    if K_RANK != Q(
        3055930500533353804145008325576782226562500, 453789
    ):
        raise RuntimeError("K rank arithmetic")

    rank_moment = rank_moment_derivation()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": DEPENDENCIES,
            "old_artifacts_modified": False,
            "parameter_scope": "uniformly for every fixed |s|<=1/400",
            "return_depth_scope": "every finite n>=1 and the full first-return partition",
        },
        "physical_collision_incidence_rank": rank_moment,
        "arbitrary_Rn_additive_rank_sum_charge": {
            "regular_point": "x in a regular rank-refined component of R_n",
            "orbit_ranks": "B_i(x)=B_inc(T_s^(i-1)x), 1<=i<=n",
            "pointwise_density": "c_D1,n(x)=151*sum_{i=1}^n 2^B_i(x)",
            "forward_reverse_policy": (
                "one common physical charge on the shared carrier, not one charge per view"
            ),
            "component_charge": "q_D1,n,k=integral_{R_n,k}c_D1,n(x)dmu_s(x)",
            "component_mean_density": "cbar_D1,n,k=q_D1,n,k/mu_s(R_n,k)",
            "zero_mass_policy": "zero mass components carry zero charge",
            "Jensen_bridge": (
                "mbar_n,k*cbar_D1,n,k^p<="
                "mu_s(C_s)^-1*integral_{R_n,k}c_D1,n(x)^p*dmu_s"
            ),
            "physical_first_return_component_charge": "CERTIFIED",
            "full_C_fw_or_C_rev_cost": False,
            "dominates_final_same_ID_q": False,
        },
        "levelwise_physical_L6over5_bound": {
            "p": qstr(P),
            "q0": qstr(Q0),
            "p_over_q0": qstr(P / Q0),
            "one_minus_p_over_q0": qstr(1 - P / Q0),
            "power_sum_inequality": (
                "(sum_{i=1}^n x_i)^p<=n^(p-1)*sum_{i=1}^n x_i^p"
            ),
            "restricted_holder_step": (
                "integral_Rn 2^(pB_i)dnu_s<="
                "A^(4/5)*M_rank^(4/5)*nu_s(R_n)^(1/5)"
            ),
            "normalized_measure": "dnu_s=dmu_s/mu_s(C_s)",
            "level_mass_domination": "nu_s(R_n)<=S_(n-1)",
            "survivor_input": (
                "S_(n-1)<A*r^floor((n-1)/N_open)"
            ),
            "safe_rational_relaxations": [
                "151^(6/5)<151^2=22801",
                "n^(6/5)<=n^2",
                "M_rank^(4/5)<=M_rank",
            ],
            "level_bound": (
                "integral_Rn c_D1,n^(6/5)dnu_s<"
                "22801*A*M_rank*n^2*r^(floor((n-1)/N_open)/5)"
            ),
            "status": "CERTIFIED_PHYSICAL_LEVELWISE_BOUND",
        },
        "global_physical_L6over5_moment": {
            "block_index": "b=floor((n-1)/N_open)",
            "block_polynomial_sum": (
                "sum_{b*N_open<n<=(b+1)*N_open}n^2<="
                "N_open^3*(b+1)^2"
            ),
            "h": "r^(1/5)",
            "concavity_bound": "h=(1-epsilon)^(1/5)<=1-epsilon/5",
            "exact_series": "sum_{b>=0}(b+1)^2*h^b=(1+h)/(1-h)^3",
            "series_upper": "(1+h)/(1-h)^3<250/epsilon^3",
            "A": qstr(TAIL_A),
            "epsilon": qstr(TAIL_EPSILON),
            "r": qstr(TAIL_R),
            "M_rank": qstr(RANK_MOMENT),
            "K_rank_exact": qstr(K_RANK),
            "global_component_moment_bound": (
                "sum_{n,k}mbar_n,k*cbar_D1,n,k^(6/5)<K_rank*N_open^3"
            ),
            "N_open_type": "one uniform theorem-supplied integer>=1, not numeric",
            "status": "CERTIFIED_PHYSICAL_GLOBAL_L6OVER5_MOMENT",
        },
        "physical_rank_sum_weighted_tail": {
            "normalized_tail": "Wbar_D1(n)=sum_{j>n,k}qbar_D1,j,k",
            "transfer_theorem": "Round28 global_Lp_transfer with p=6/5",
            "moment_input": "M_p=K_rank*N_open^3",
            "strict_bound": (
                "Wbar_D1(n)<(K_rank*N_open^3)^(5/6)*A^(1/6)"
                "*r^(floor(n/N_open)/6)"
            ),
            "physical_unnormalized_tail": "W_D1,phys(n)<=Wbar_D1(n)",
            "block_exponent": "1/6",
            "uniform_exponential_tail": "CERTIFIED_FOR_ADDITIVE_D1_RANK_SUM_CHARGE",
        },
        "same_ID_interface_update": {
            "arbitrary_Rn_common_fw_rev_carrier": "CERTIFIED_PARAMETERIZED_SCHEMA",
            "physical_first_return_Lp_interface": (
                "CERTIFIED_FOR_ADDITIVE_D1_RANK_SUM_CHARGE"
            ),
            "round34_coarea_measure_mismatch_bypassed": (
                "yes, by direct collision-SRB incidence-rank integration"
            ),
            "complete_numeric_C_fw_C_rev": "NOT_CERTIFIED",
            "final_same_ID_q": "NOT_CERTIFIED",
            "physical_global_recovery_depth_D_moment": "NOT_CERTIFIED",
            "strong_cemetery_charge": "NOT_CERTIFIED",
            "F14_through_F18": "NOT_CERTIFIED",
        },
        "strict_nonpromotion": {
            "D1_rank_sum_is_full_branch_C1_pullback_cost": False,
            "D1_rank_sum_dominates_complete_C_fw_C_rev": False,
            "D1_tail_is_final_q_weighted_tail": False,
            "complete_numeric_C_fw_C_rev": "NOT_CERTIFIED",
            "final_same_ID_q": "NOT_CERTIFIED",
            "q_weighted_excursion_cemetery_tail": "NOT_CERTIFIED",
            "complete_18_field_operator_block_count": 0,
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
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
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument(
        "--verifier",
        type=Path,
        default=HERE / "cm2_gate45_round35_physical_rn_rank_sum_lp_verifier.py",
    )
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        return 0
    result = build_result()
    print(result["global_physical_L6over5_moment"]["status"])
    print(result["physical_rank_sum_weighted_tail"]["uniform_exponential_tail"])
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
