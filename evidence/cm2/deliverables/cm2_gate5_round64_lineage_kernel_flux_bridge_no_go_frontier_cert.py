#!/usr/bin/env python3
"""Producer for the append-only Round-64 Gate-5 no-go frontier."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from decimal import Decimal, localcontext
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round64_common import (
    CertError, canonical_bytes, digest, require, sha256_path, validate_pins,
)


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate5.round64.lineage-kernel-flux-bridge-no-go.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-gate5-round64-lineage-kernel-flux-bridge-no-go-frontier"
REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
VERIFIER = HERE / "cm2_gate5_round64_lineage_kernel_flux_bridge_no_go_frontier_verifier.py"
COMMON = HERE / "cm2_round64_common.py"

PINS = {
    "cm2-sixty-third-direct-assault-2026-07-21.md":
        "9cde412ba689be87d777906404c9c9426a2a8a102385a2c4c510df8f9b7a6a05",
    "cm2-sixty-third-direct-assault-manifest-2026-07-21.sha256":
        "a0b512f32914ef2692b31466a4ea156c44698b1eaf44d8ead45b2c74ee73230e",
    "cm2-round63-independent-core-frontier-audit-manifest-2026-07-21.json":
        "3aae6d018fc15aaab47116d311eed8333c56b87542b0b5761b849221cbf76d6b",
    "cm2-round63-independent-core-frontier-audit-manifest-2026-07-21.sha256":
        "8227dd32e36d2879f9dbbdced54f3c50b3eac1536ce8fceac480d22cb8617bfd",
    "cm2-round63-independent-core-frontier-audit-2026-07-21.md":
        "b30aff208e9e5707e443f59abd07507f7f9d93d765ecaf3fd675f4150c5bf978",
    "cm2-gate5-round63-killed-trace-kernel-jordan-join-frontier-assault-2026-07-21.md":
        "74e60854d18e34b8fd5bf089deffcb13d37751b59268277e4f4e254b3653a477",
    "cm2-gate5-round63-killed-trace-kernel-jordan-join-frontier-manifest-2026-07-21.json":
        "a052e9c278a6359bdcd554020de28b2e8d821eb0e1267758a702bf3dff130ab8",
    "cm2-gate5-round63-killed-trace-kernel-jordan-join-frontier-manifest-2026-07-21.sha256":
        "605487e4aee375b589f5fd13e9de85ab716e41d8db285cb3327529c7cc857a9e",
    "cm2-gate5-round44-all-face-suffix-two-trace-f13-manifest-2026-07-19.json":
        "3cf6635532622427bcde0525205212e1970b92ee56b2eb290ed01c1984443a9d",
    "cm2-gate5-round44-all-face-suffix-two-trace-f13-manifest-2026-07-19.sha256":
        "07dc2b60d6b8003f0fa3ed7bd7a69167777e8a78958811169caff847ac31480c",
    "cm2-gate5-round50-owner-boundary-zb-f17-frontier-manifest-2026-07-19.json":
        "c848c67bb9f2c0793d793c2ab4dca754cad71c507b9f0a06b9c29be3eaafeb46",
    "cm2-gate5-round50-owner-boundary-zb-f17-frontier-manifest-2026-07-19.sha256":
        "a899f6e156044b54ca8bd3f06b13bccae5dcf74dad2b2e0984cd6eaec0fd30a6",
    "cm2-gate5-round52-owner-tail-tower-anisotropic-frontier-manifest-2026-07-20.json":
        "ca623e4c350b75f0fec889d0909b052bb0493613ff2f983ac71fd2fca40e016b",
    "cm2-gate5-round52-owner-tail-tower-anisotropic-frontier-manifest-2026-07-20.sha256":
        "b59d52e17d9ed7c6696a3ff9a6298c7beac5925f330942dd96ea0bf559111f5e",
    "cm2-gate5-round54-collar-pairing-directional-bv-frontier-manifest-2026-07-20.json":
        "87e052dbfc369195becc5f2d4ac641c8250d72266bb73f47281b8b923d584ab5",
    "cm2-gate5-round54-collar-pairing-directional-bv-frontier-manifest-2026-07-20.sha256":
        "3ebe362d484687c64a087905cc1d29388208f13fe00f165c0623b370c3110976",
    "cm2-gate5-round56-optimal-collar-recovery-clock-frontier-manifest-2026-07-20.json":
        "c2d872c1f430bae123f9c4171bd459cd11d12e6cc15425521777da71047c2479",
    "cm2-gate5-round56-optimal-collar-recovery-clock-frontier-manifest-2026-07-20.sha256":
        "0b9b94d1911d3774dca5a6877282417a3ec008e58f9fa7796e56cac95cf0cd53",
    "cm2-gate5-round60-owner-trace-suffix-positive-anchor-frontier-manifest-2026-07-20.json":
        "d519ad15a870fe7820839828347140e4bae3b5752a95fab4c18263c67e2ab778",
    "cm2-gate5-round60-owner-trace-suffix-positive-anchor-frontier-manifest-2026-07-20.sha256":
        "ba1fc62efa4ed68df1d1ac0e9117642880768f0cd0374b95f8a1dc557274c483",
    "cm2-gate5-round61-complement-rn-borel-orlicz-frontier-manifest-2026-07-20.json":
        "59bce010748cccc1ffb829a9c232cab77185e6467433b3fed34988913649ae75",
    "cm2-gate5-round61-complement-rn-borel-orlicz-frontier-manifest-2026-07-20.sha256":
        "27f936d543d7b0f4794741f6896387ab0dcbc4b5d2e729f3412beb6ddc190d26",
    "cm2-gate5-round62-all-time-owner-trace-decay-frontier-manifest-2026-07-21.json":
        "ddbe8545e6471977ac7bd06b584717cbe7ffeeb62df2ac3baeb8cb70f0ad27d9",
    "cm2-gate5-round62-all-time-owner-trace-decay-frontier-manifest-2026-07-21.sha256":
        "ce399f98596b9906eb89d1bd68b80d5f49a5ed29471ba2b8d9648c250a805e61",
}


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def trace_threshold() -> dict[str, str]:
    with localcontext() as ctx:
        ctx.prec = 120
        rho = (Decimal(111718729) / Decimal(111718750)) ** Decimal(9148)
        w = (Decimal(1) + Decimal(1) / rho) / Decimal(2)
        ratio = w.ln() / (-rho.ln())
        q_star = Decimal(1) / (Decimal(1) - ratio)
        q2_factor = w * rho.sqrt()
        return {
            "rho_decimal": str(rho),
            "w_Z_decimal": str(w),
            "log_ratio": str(ratio),
            "q_trace_star": str(q_star),
            "q2_factor": str(q2_factor),
        }


def harmonic_rows(count: int = 14) -> list[dict[str, Any]]:
    rows = []
    for j in range(count):
        rows.append({
            "j": j,
            "base_mass": qstr(Q(1, 3**j)),
            "charge": qstr(Q(2**j, j + 1)),
            "weighted_base_term": qstr(Q(1, 2**j)),
            "weighted_charge_term": qstr(Q(1, j + 1)),
        })
    return rows


def gap_rows(count: int = 14) -> list[dict[str, Any]]:
    rows = []
    for j in range(count):
        rows.append({
            "j": j, "gap": qstr(Q(1, 2**j)), "Y": j,
            "mass": qstr(Q(1, 3**j * (j + 1))),
            "weighted_exponential_charge": qstr(Q(1, j + 1)),
            "has_accumulation_atom": False,
        })
    return rows


def build_result() -> dict[str, Any]:
    threshold = trace_threshold()
    lineage_rows = [
        {
            "name": "strict_contraction", "beta_j": ["4", "2"],
            "beta_next": ["1", "1"], "RN_ratios": ["1/4", "1/2"],
            "c_star": "1/2", "kernel_exists_with_c_star": True,
        },
        {
            "name": "stationary", "beta_j": ["4", "2"],
            "beta_next": ["4", "2"], "RN_ratios": ["1", "1"],
            "c_star": "1", "kernel_exists_with_c_star": True,
        },
        {
            "name": "singular_label_switch", "beta_j": ["1", "0"],
            "beta_next": ["0", "1"], "RN_ratios": ["0", "SINGULAR"],
            "c_star": "INFINITY", "kernel_exists_with_c_star": False,
        },
    ]
    kappa = [Q(1, 2), Q(1, 3), Q(1, 4), Q(1, 5)]
    nonuniform_rows = []
    product = Q(1)
    for j in range(5):
        nonuniform_rows.append({
            "j": j, "product_kappa_i_i<j": qstr(product),
            "w_test_power_times_product": qstr(Q(3, 2)**j * product),
        })
        if j < len(kappa):
            product *= kappa[j]

    suffix_rows = []
    for atom in range(32):
        suffix_rows.append({
            "atom": atom,
            "fixed_bits": [True, True],
            "open_bits": [bool((atom >> bit) & 1) for bit in range(5)],
        })

    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "append_only": True, "old_artifacts_modified": False,
            "pinned_round63_and_gate5_inputs": PINS,
        },
        "owner_lineage_kernel": {
            "status": "CERTIFIED_EXACT_IFF",
            "criterion": "exists label-preserving K with Lambda_next=Lambda K and K1<=c iff beta_next<=c beta",
            "minimal_coefficient": "c_star=||d beta_next/d beta||_infinity; infinity if singular",
            "standard_Borel_disintegration_required": True,
            "rows": lineage_rows,
            "fibre_constant_Lyapunov": "r_j v_next<=kappa_j v_j",
            "submarkov_requires_r_j_le_1": True,
            "nonuniform_weighted_criterion": "sum_j w_Z^j product_(i<j)kappa_i<infinity",
            "nonuniform_replay": nonuniform_rows,
            "actual_cross_j_same_label_domination": "NOT_CERTIFIED",
        },
        "trace_density_threshold": {
            "rho_exact": "(111718729/111718750)^9148",
            "w_Z_exact": "(1+rho^-1)/2",
            **threshold,
            "q_trace_star_formula": "1/(1-log(w_Z)/(-log(rho)))",
            "q_trace_star_gt_2": Decimal(threshold["q_trace_star"]) > 2,
            "q2_factor_identity": "(sqrt(rho)+1/sqrt(rho))/2",
            "q2_factor_gt_1": Decimal(threshold["q2_factor"]) > 1,
            "all_q_le_2_fail_threshold": True,
            "q_col_decimal":
                "806.02499399415683003064474204689664379045349858576951942226554061893741931007400927795846878097969404280491041058360256449333129488880276687",
            "q_col_is_trace_RN_exponent": False,
        },
        "sectorwise_Feynman_Kac": {
            "required_sectors": [
                "active-clock", "raw-Z", "Orlicz", "complement",
                "variation", "common-mode", "pre-cemetery",
            ],
            "required_row": "P_j H_next<=kappa_H H_j and w_Z kappa_H<1",
            "separator": {
                "w_test": "3/2", "base_law": "mu_j=3^-j",
                "charge": "H_j=2^j/(j+1)", "rows": harmonic_rows(),
                "base_weighted_sum": "2", "charge_weighted_sum": "DIVERGES_HARMONIC",
            },
            "actual_all_sector_positive_drift": "NOT_CERTIFIED",
            "unified_positive_slice_upstream": {
                "fixed_j_complement_variation_common_mode": "FINITE_PINNED",
                "actual_raw_Z_power_Orlicz_finite_RHS": "NOT_CERTIFIED",
                "positive_pre_cemetery_slice_law": "NOT_MATERIALIZED",
                "unified_finite_Lambda_j_before_drift": "NOT_CERTIFIED",
            },
        },
        "small_gap_joint_criterion": {
            "remaining_N_cut": {
                "codes": [
                    "chart_atlas", "homogeneity", "hole_cemetery_boundary",
                    "owner_tie_change", "non_source_endpoint",
                    "later_word_singularity_pullback",
                ],
                "union_zero_iff_every_coded_row_zero": True,
                "chi_ll_nu_only_transfers_already_proved_nu_zero": True,
                "actual_all_coded_zero_rows": "NOT_CERTIFIED",
            },
            "criterion": "sum_j w_Z^j integral 2^(aY_j)dchi_j<infinity",
            "G_zero_sets_Y_to_infinity": True,
            "decreasing_sets": "A_jk={all individual gaps positive and G_j<=2^-k} decreases to N_acc",
            "accumulation_nullity_follows": True,
            "tail": "chi_j(Y_j>=k)<=2^(-ak) integral 2^(aY_j)dchi_j",
            "separator": {
                "w_test": "3/2", "a_test": "1",
                "law": "gap_j=2^-j; mass_j=3^-j/(j+1)",
                "rows": gap_rows(), "weighted_charge_sum": "DIVERGES_HARMONIC",
            },
            "actual_same_law_joint_bound": "NOT_CERTIFIED",
        },
        "cemetery_typing": {
            "positive_cemetery_must_be": "ONE_SHOT_ARRIVAL_LEDGER",
            "absorbing_occupancy_recounted_each_slice_diverges_for_w_Z_gt_1": True,
            "live_drift_pays_pre_regularization_cemetery": False,
            "actual_pre_regularization_arrival_bound": "NOT_CERTIFIED",
        },
        "Jordan_bridge": {
            "exact_pair_decomposition": "(mu+,mu-)=(J+ + lambda,J- + lambda)",
            "typed_crosswalk_required": "tag-preserving T with p-to-j index crosswalk",
            "exact_alignment": "T_*mu+=xi^f and T_*mu-=xi^r",
            "alignment_iff": "same typed carrier and signed J equality and common-mode lambda equality",
            "lawful_domination": "T_*mu+<=C_f xi^f and T_*mu-<=C_r xi^r",
            "domination_variation_bound": "|T_*J|<=C_f xi^f+C_r xi^r",
            "domination_is_Jordan_alignment_or_F10": False,
            "one_point_separator": {
                "pair_1": ["1", "1"], "pair_M": ["M", "M"],
                "signed_laws_equal_zero": True, "positive_totals_uniformly_comparable": False,
            },
            "Round54_Round61_common_carrier_token_RN_bridge": "NOT_CERTIFIED",
        },
        "suffix_cube": {
            "Borel_atoms": 32, "fixed_true_bits": 2, "open_bits": 5,
            "rows": suffix_rows,
            "typing_implies_remaining_values": False,
            "typing_implies_R_ge_rK": False,
            "first_failure_partition": "{R<r_K}=disjoint_union_(b,s)(F_b,s intersect {b<r_K})",
            "universal_R_ge_rK_iff_all_first_failure_cells_empty": True,
            "drift_proves_first_failure_cells_empty": False,
        },
        "latest_technology_boundary": {
            "external_theorem_promoted": False,
            "reason": "small-hole, renewal and signed-transport results do not supply owner-lineage marginal contraction or positive common mode",
        },
        "strict_status": {
            "Gate5": "NOT_CERTIFIED", "Gate5_maturity": "10/18",
            "complete_18_field_blocks": 0, "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    replay = copy.deepcopy(result)
    result["internal_replay_digest"] = digest(replay)
    return result


def build_manifest(verifier: Path) -> dict[str, Any]:
    validate_pins(HERE, PINS)
    result = build_result()
    require(REPORT.is_file() and verifier.is_file() and COMMON.is_file(), "artifact missing")
    return {
        "schema": MANIFEST_SCHEMA, "pins": PINS,
        "report_sha256": sha256_path(REPORT),
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier.resolve()),
        "common_sha256": sha256_path(COMMON),
        "result": result, "verdict": result["strict_status"],
    }


def replay() -> dict[str, Any]:
    validate_pins(HERE, PINS)
    result = build_result()
    require(result["owner_lineage_kernel"]["rows"][0]["c_star"] == "1/2", "lineage replay")
    require(result["trace_density_threshold"]["q_trace_star_gt_2"] is True, "q threshold")
    require(len(result["suffix_cube"]["rows"]) == 32, "suffix cube")
    return {
        "pins": "24/24", "lineage_rows": 3, "harmonic_rows": 14,
        "gap_rows": 14, "suffix_atoms": 32, "status": "PASS",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-json", action="store_true")
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--verifier", type=Path, default=VERIFIER)
    args = parser.parse_args()
    try:
        if args.replay:
            print(json.dumps(replay(), sort_keys=True))
            return 0
        manifest = build_manifest(args.verifier)
        payload = canonical_bytes(manifest)
        if args.manifest_json:
            sys.stdout.buffer.write(payload)
            return 0
        if args.write_manifest is not None:
            args.write_manifest.write_bytes(payload)
            return 0
    except (CertError, OSError, ValueError, KeyError, TypeError, ArithmeticError) as exc:
        print(f"ROUND64_GATE5_CERT_ERROR: {exc}", file=sys.stderr)
        return 1
    print("Gate5 maturity: 10/18")
    print("complete blocks: 0")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
