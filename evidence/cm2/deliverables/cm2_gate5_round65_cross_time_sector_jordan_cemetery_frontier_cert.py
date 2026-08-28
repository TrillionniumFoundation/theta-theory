#!/usr/bin/env python3
"""Producer for the append-only Round-65 Gate-5 frontier."""

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
RESULT_SCHEMA = "cm2.gate5.round65.cross-time-sector-jordan-cemetery-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-gate5-round65-cross-time-sector-jordan-cemetery-frontier"
REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
VERIFIER = HERE / "cm2_gate5_round65_cross_time_sector_jordan_cemetery_frontier_verifier.py"
COMMON = HERE / "cm2_round64_common.py"

PINS = {
    "cm2-sixty-fourth-direct-assault-2026-07-21.md":
        "bbd52eed540e4e91566a7d0b9fda2b381b35860640e23a0a45d29b73fabb8b61",
    "cm2-sixty-fourth-direct-assault-manifest-2026-07-21.sha256":
        "5d2174cee61c0fdf5573dedaece38950c0261fe05aa835b66c4363d974e52932",
    "cm2-round64-independent-core-frontier-audit-2026-07-21.md":
        "786922ef94b522498440cf90df562c77a65d991a03c01637d9740a22f0dcae49",
    "cm2-round64-independent-core-frontier-audit-manifest-2026-07-21.json":
        "e775720b2891146a39421d515280e119f42b075d0783650e879abe1370ff8779",
    "cm2-round64-independent-core-frontier-audit-manifest-2026-07-21.sha256":
        "d61e8f2ea2d3e5b172846a16fdfa75373058ec8b91759aea0e393c500ea0740b",
    "cm2-gate5-round64-lineage-kernel-flux-bridge-no-go-frontier-assault-2026-07-21.md":
        "94b1e0fc00d108500acdf3e5b8a3349a5834c6362635b976ab0d797df9ff7536",
    "cm2-gate5-round64-lineage-kernel-flux-bridge-no-go-frontier-manifest-2026-07-21.json":
        "7a67d2225b699c6cffb798298123469eeae6a5d5ded9d1ee9079afb9e8222e70",
    "cm2-gate5-round64-lineage-kernel-flux-bridge-no-go-frontier-manifest-2026-07-21.sha256":
        "148ad7b7a0e2384fb602adcbb8cefdb86022ef18130ae73fd438c7aaf06461bb",
    "cm2-gate5-round63-killed-trace-kernel-jordan-join-frontier-assault-2026-07-21.md":
        "74e60854d18e34b8fd5bf089deffcb13d37751b59268277e4f4e254b3653a477",
    "cm2-gate5-round63-killed-trace-kernel-jordan-join-frontier-manifest-2026-07-21.json":
        "a052e9c278a6359bdcd554020de28b2e8d821eb0e1267758a702bf3dff130ab8",
    "cm2-gate5-round63-killed-trace-kernel-jordan-join-frontier-manifest-2026-07-21.sha256":
        "605487e4aee375b589f5fd13e9de85ab716e41d8db285cb3327529c7cc857a9e",
    "cm2-gate5-round62-all-time-owner-trace-decay-frontier-assault-2026-07-21.md":
        "cd90cc734264c34d518365f219dce3fbe058232d91213002cc8dd9d04b766f46",
    "cm2-gate5-round62-all-time-owner-trace-decay-frontier-manifest-2026-07-21.json":
        "ddbe8545e6471977ac7bd06b584717cbe7ffeeb62df2ac3baeb8cb70f0ad27d9",
    "cm2-gate5-round62-all-time-owner-trace-decay-frontier-manifest-2026-07-21.sha256":
        "ce399f98596b9906eb89d1bd68b80d5f49a5ed29471ba2b8d9648c250a805e61",
    "cm2-gate5-round61-complement-rn-borel-orlicz-frontier-assault-2026-07-20.md":
        "9554ac9dbf51d617ce01a442015613394cdc6e345cf021b88e1f20bdbd1e0065",
    "cm2-gate5-round61-complement-rn-borel-orlicz-frontier-manifest-2026-07-20.json":
        "59bce010748cccc1ffb829a9c232cab77185e6467433b3fed34988913649ae75",
    "cm2-gate5-round61-complement-rn-borel-orlicz-frontier-manifest-2026-07-20.sha256":
        "27f936d543d7b0f4794741f6896387ab0dcbc4b5d2e729f3412beb6ddc190d26",
    "cm2-gate5-round60-owner-trace-suffix-positive-anchor-frontier-assault-2026-07-20.md":
        "2833e9ab87ee325da13847eb4cf660f52e015a7e1cadb7ebe6a9ddaf0ef8d9d9",
    "cm2-gate5-round60-owner-trace-suffix-positive-anchor-frontier-manifest-2026-07-20.json":
        "d519ad15a870fe7820839828347140e4bae3b5752a95fab4c18263c67e2ab778",
    "cm2-gate5-round60-owner-trace-suffix-positive-anchor-frontier-manifest-2026-07-20.sha256":
        "ba1fc62efa4ed68df1d1ac0e9117642880768f0cd0374b95f8a1dc557274c483",
    "cm2-gate5-round56-optimal-collar-recovery-clock-frontier-assault-2026-07-20.md":
        "d1cb72f74aa30480567d7202b8b1b7e88ff943a8ce56d187d63bb0b8fcc70039",
    "cm2-gate5-round56-optimal-collar-recovery-clock-frontier-manifest-2026-07-20.json":
        "c2d872c1f430bae123f9c4171bd459cd11d12e6cc15425521777da71047c2479",
    "cm2-gate5-round56-optimal-collar-recovery-clock-frontier-manifest-2026-07-20.sha256":
        "0b9b94d1911d3774dca5a6877282417a3ec008e58f9fa7796e56cac95cf0cd53",
    "cm2-gate5-round54-collar-pairing-directional-bv-frontier-assault-2026-07-20.md":
        "81aa5bdd1071dc10cbce0ab4690c2a1da29eee2e7a238e8e8aa9b3db5256bf1a",
    "cm2-gate5-round54-collar-pairing-directional-bv-frontier-manifest-2026-07-20.json":
        "87e052dbfc369195becc5f2d4ac641c8250d72266bb73f47281b8b923d584ab5",
    "cm2-gate5-round54-collar-pairing-directional-bv-frontier-manifest-2026-07-20.sha256":
        "3ebe362d484687c64a087905cc1d29388208f13fe00f165c0623b370c3110976",
    "cm2-gate5-round52-owner-tail-tower-anisotropic-frontier-assault-2026-07-20.md":
        "7dedcec5532721e7a8144cc350ffab1689213b250fa5f877051aba06a04a8c55",
    "cm2-gate5-round52-owner-tail-tower-anisotropic-frontier-manifest-2026-07-20.json":
        "ca623e4c350b75f0fec889d0909b052bb0493613ff2f983ac71fd2fca40e016b",
    "cm2-gate5-round52-owner-tail-tower-anisotropic-frontier-manifest-2026-07-20.sha256":
        "b59d52e17d9ed7c6696a3ff9a6298c7beac5925f330942dd96ea0bf559111f5e",
    "cm2-gate5-round50-owner-boundary-zb-f17-frontier-assault-2026-07-19.md":
        "cee818d80dbbadc3fd8037b0daabb8c3a10974a7b37fb01dae5d9854e82d57e8",
    "cm2-gate5-round50-owner-boundary-zb-f17-frontier-manifest-2026-07-19.json":
        "c848c67bb9f2c0793d793c2ab4dca754cad71c507b9f0a06b9c29be3eaafeb46",
    "cm2-gate5-round50-owner-boundary-zb-f17-frontier-manifest-2026-07-19.sha256":
        "a899f6e156044b54ca8bd3f06b13bccae5dcf74dad2b2e0984cd6eaec0fd30a6",
    "cm2-gate5-round44-all-face-suffix-two-trace-f13-assault-2026-07-19.md":
        "81f1fe9ed37507764f94bc16e97316fc9039115aa426c1947b224b59eee6a6b9",
    "cm2-gate5-round44-all-face-suffix-two-trace-f13-manifest-2026-07-19.json":
        "3cf6635532622427bcde0525205212e1970b92ee56b2eb290ed01c1984443a9d",
    "cm2-gate5-round44-all-face-suffix-two-trace-f13-manifest-2026-07-19.sha256":
        "07dc2b60d6b8003f0fa3ed7bd7a69167777e8a78958811169caff847ac31480c",
    "cm2-gate5-round39-moving-occurrence-f10-l3over2-assault-2026-07-19.md":
        "8cd35cff02f4cc3a812ad7a88004688a983ca1c1e960370ef87df349c19e1ac6",
    "cm2-gate5-round39-moving-occurrence-f10-l3over2-manifest-2026-07-19.json":
        "19ad840a8cfbca2aa722cfd367d287fe36de67b9c7b6faf00a151ca2f2bf8a16",
    "cm2-gate5-round39-moving-occurrence-f10-l3over2-manifest-2026-07-19.sha256":
        "de39ac6cefce8e77f43969cb5f965afa1a8de22eb7d8cceffabecb8d38a08961",
}


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def physical_constants() -> dict[str, str]:
    with localcontext() as ctx:
        ctx.prec = 120
        rho = (Decimal(111718729) / Decimal(111718750)) ** Decimal(9148)
        w = (Decimal(1) + Decimal(1) / rho) / Decimal(2)
        gamma = ((Decimal(2000) / Decimal(1999)) * Decimal(1 + 48 * 9148)
                 * (Decimal(900337) / Decimal(901685)) ** Decimal(9148))
        beta = Decimal(2).ln() / (-gamma.ln())
        q_col = Decimal(2).ln() / (beta * w.ln())
        c_col = (q_col * w.ln()).exp()
        return {
            "rho": str(rho), "w_Z": str(w), "w_Z_inverse": str(Decimal(1) / w),
            "gamma": str(gamma), "beta": str(beta), "q_col": str(q_col),
            "C_col": str(c_col), "C_col_formula": "w_Z^q_col=2^(1/beta)",
        }


def split_rows() -> list[dict[str, Any]]:
    return [
        {
            "name": "strict_live_arrival_split", "beta_source": ["4", "2"],
            "beta_live_next": ["1", "1"], "alpha_arrival_next": ["1", "0"],
            "combined_ratios": ["1/2", "1/2"], "c_split_star": "1/2",
            "submarkov_split_exists": True,
        },
        {
            "name": "stationary_plus_positive_arrival", "beta_source": ["2", "2"],
            "beta_live_next": ["2", "2"], "alpha_arrival_next": ["1", "0"],
            "combined_ratios": ["3/2", "1"], "c_split_star": "3/2",
            "submarkov_split_exists": False,
        },
        {
            "name": "singular_new_cemetery_label", "beta_source": ["1", "0"],
            "beta_live_next": ["0", "0"], "alpha_arrival_next": ["0", "1"],
            "combined_ratios": ["0", "SINGULAR"], "c_split_star": "INFINITY",
            "submarkov_split_exists": False,
        },
    ]


def sector_rows() -> list[dict[str, Any]]:
    ratio = [Q(1, 4), Q(1, 2)]
    data = [
        ("active-clock", [Q(4), Q(2)], [Q(2), Q(1)]),
        ("raw-Z", [Q(8), Q(4)], [Q(8), Q(8)]),
        ("power-Orlicz", [Q(16), Q(8)], [Q(8), Q(8)]),
        ("complement", [Q(2), Q(2)], [Q(1), Q(1)]),
        ("variation", [Q(1), Q(4)], [Q(2), Q(2)]),
        ("common-mode", [Q(1), Q(1)], [Q(1), Q(1)]),
        ("one-shot-cemetery", [Q(1), Q(2)], [Q(1), Q(4)]),
    ]
    rows = []
    for name, before, after in data:
        pointwise = [ratio[i] * after[i] / before[i] for i in range(2)]
        rows.append({
            "sector": name, "h_j": [qstr(x) for x in before],
            "h_next": [qstr(x) for x in after],
            "pointwise_coefficients": [qstr(x) for x in pointwise],
            "kappa_star": qstr(max(pointwise)),
        })
    return rows


def raw_separator_rows(count: int = 16) -> list[dict[str, Any]]:
    rows = []
    for j in range(count):
        mass = Q(1, 3**j)
        rows.append({
            "j": j, "beta_j": qstr(mass), "K_j": j,
            "base_weighted_term": qstr(Q(3, 2)**j * mass),
            "raw_mark": str(2 ** (j + 1)),
            "raw_weighted_term": "2",
        })
    return rows


def cemetery_rows(count: int = 10) -> list[dict[str, Any]]:
    q = Q(1, 3)
    occupancy = Q(0)
    rows = []
    for j in range(count):
        arrival = Q(1, 4**j)
        occupancy = arrival + q * occupancy
        rows.append({
            "j": j, "arrival": qstr(arrival), "leaky_occupancy": qstr(occupancy),
            "weighted_arrival": qstr(Q(3, 2)**j * arrival),
            "weighted_occupancy": qstr(Q(3, 2)**j * occupancy),
        })
    return rows


def open_fields() -> list[dict[str, str]]:
    return [
        {"field": "F5", "name": "inverse_Jacobian_bound",
         "status": "NOT_CERTIFIED_GLOBAL", "first_unpaid": "global homogeneous return-word row"},
        {"field": "F6", "name": "log_Jacobian_distortion_sum",
         "status": "NOT_CERTIFIED_GLOBAL", "first_unpaid": "global same-block distortion sum"},
        {"field": "F10", "name": "coarea_density_regular_bound",
         "status": "NOT_CERTIFIED", "first_unpaid": "all-time positive sector/cut/cemetery ledger"},
        {"field": "F11", "name": "dynamic_Holder_test_pullback_bound",
         "status": "NOT_CERTIFIED", "first_unpaid": "branch-uniform physical dynamic test embedding"},
        {"field": "F14", "name": "regular_density_operator_cost",
         "status": "NOT_CERTIFIED", "first_unpaid": "F10 and common recovered strong block"},
        {"field": "F15", "name": "standard_family_operator_cost",
         "status": "NOT_CERTIFIED", "first_unpaid": "raw-Z/Orlicz recovery and positive cemetery"},
        {"field": "F17", "name": "dynamic_test_operator_cost",
         "status": "NOT_CERTIFIED", "first_unpaid": "all-input vector-current strong recipient"},
        {"field": "F18", "name": "operator_phase_block",
         "status": "NOT_CERTIFIED", "first_unpaid": "all preceding rows on one block"},
    ]


def build_result() -> dict[str, Any]:
    constants = physical_constants()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "append_only": True, "old_artifacts_modified": False,
            "pinned_round64_round61_63_and_physical_inputs": PINS,
        },
        "actual_frozen_audit": {
            "fixed_j_owner_root_law": "FINITE",
            "fixed_j_orientation_cost_forward_reverse": "FINITE",
            "fixed_j_cost_variation_common_mode_complement": "FINITE",
            "fixed_j_source_exact_grazing_charge": "ZERO",
            "fixed_j_raw_Z_col_power_Orlicz_RHS": "NOT_CERTIFIED_FINITE",
            "pre_regularization_cemetery_arrival_law": "NOT_MATERIALIZED",
            "Round52_owner_formula": "m_(j,a)^owner=1_(E_owner intersect R_reg)m_occ for n>j",
            "Round52_cross_j_Borel_map": "NOT_MATERIALIZED",
            "actual_beta_next_ll_beta": "NOT_CERTIFIED",
            "actual_c_below_w_Z_inverse": "NOT_CERTIFIED",
        },
        "physical_constants": constants,
        "live_arrival_split": {
            "status": "CERTIFIED_EXACT_IFF",
            "criterion": "exists label-preserving live/arrival kernels with total row mass<=c iff beta_next+alpha_next<=c beta",
            "sharp_coefficient": "||d(beta_next+alpha_next)/d beta||_infinity; infinity if singular",
            "one_shot_arrival_required": True,
            "rows": split_rows(),
            "arrival_drift_bound": "sum_j w_Z^(j+1)A_(j+1)(1)<=w_Z Lambda_0(V_0)/(1-w_Z kappa)",
            "bound_requires_arrival_generated_from_live_split": True,
            "actual_split_inputs": "NOT_MATERIALIZED",
        },
        "sectorwise_common_kernel": {
            "status": "CERTIFIED_EXACT_FOR_FIBRE_CONSTANT_MARKS",
            "sectors": [
                "active-clock", "raw-Z", "power-Orlicz", "complement",
                "variation", "common-mode", "one-shot-cemetery",
            ],
            "criterion": "r_j<=1 and r_j h_next^s<=kappa_(j,s)h_j^s for every s",
            "sharp_coefficient": "ess_sup r_j h_next^s/h_j^s",
            "uniform_threshold": "max_s kappa_s_star<w_Z^-1",
            "nonuniform_payment": "sum_j w_Z^j product_(i<j)kappa_(i,s)<infinity",
            "charge_marginal_tier": "gamma_next^s<=kappa gamma_j^s is necessary for a common physical kernel and exact iff for sector-specific charge transport",
            "charge_marginal_tier_is_common_physical_kernel": False,
            "finite_replay_r_j": ["1/4", "1/2"],
            "finite_replay": sector_rows(),
            "actual_cross_j_ratio_and_sector_coefficients": "NOT_CERTIFIED",
            "unified_finite_positive_slice": "NOT_CERTIFIED",
        },
        "active_raw_Orlicz": {
            "marks": {
                "clock": "H_clock=w_Z^r_K", "raw": "H_raw=2^(K+1)",
                "Orlicz": "H_Orl=H_clock^q_col",
            },
            "pointwise_comparison": "H_raw<=H_Orl<C_col H_raw",
            "drift_comparison": "C_col^-1 kappa_raw_star<=kappa_Orl_star<=C_col kappa_raw_star",
            "q_col_is_trace_RN_exponent": False,
            "base_drift_implies_raw_drift": False,
            "separator": {
                "w_test": "3/2", "base_coefficient": "1/3",
                "raw_coefficient": "2/3", "raw_coefficient_times_w": "1",
                "base_weighted_sum": "2", "raw_weighted_sum": "DIVERGES_CONSTANT",
                "rows": raw_separator_rows(),
            },
            "actual_clock_raw_Orlicz_finite": "NOT_CERTIFIED",
            "actual_drift_coefficients": "NOT_CERTIFIED",
        },
        "cemetery_resolvent": {
            "one_shot_arrival_ledger": "sum_i w_Z^i A_i",
            "leaky_occupancy": "O_j=sum_(i<=j)q^(j-i)A_i",
            "exact_identity": "sum_j w_Z^j O_j=[sum_i w_Z^i A_i]/(1-w_Z q) for w_Z q<1",
            "absorbing_q_1_with_nonzero_arrival": "DIVERGES_FOR_w_Z_gt_1",
            "finite_replay": {
                "w_test": "3/2", "q_test": "1/3",
                "arrival_weighted_sum": "8/5", "occupancy_weighted_sum": "16/5",
                "rows": cemetery_rows(),
            },
            "actual_one_shot_pre_regularization_arrival": "NOT_MATERIALIZED",
        },
        "oriented_positive_bridge": {
            "status": "CERTIFIED_EXACT_IFF",
            "criterion": "xi^f_label<=c mu^+_label and xi^r_label<=c mu^-_label",
            "sharp_coefficient": "max of the two RN essential suprema",
            "strict_replay": {
                "source_plus": ["4", "2"], "target_forward": ["1", "1"],
                "source_minus": ["2", "4"], "target_reverse": ["1", "1"],
                "forward_ratios": ["1/4", "1/2"],
                "reverse_ratios": ["1/2", "1/4"], "c_star": "1/2",
            },
            "mass_preserving_scalar_necessity": "mu^+(X)=mu^-(X) implies xi^f(X)=xi^r(X)",
            "Round54_source_equal_positive_masses": True,
            "Round61_target_forward_reverse_total_equality": "NOT_CERTIFIED",
            "pair_determined_by": ["signed_J_and_positive_sum_S", "signed_J_and_common_mode_lambda"],
            "positive_sum_identity": "S=|J|+2lambda",
            "signed_only_controls_common_mode": False,
            "Round54_Round61_carrier_RN_common_mode_bridge": "NOT_CERTIFIED",
        },
        "remaining_eight_fields": {
            "required_field_count": 18, "certified_maturity": 10,
            "open_count": 8, "rows": open_fields(), "new_field_promoted": False,
        },
        "latest_technology_boundary": {
            "arXiv_2510_19573v3": {
                "title": "Quasi-compactness for dominated kernels with application to quasi-stationary distribution theory",
                "useful_side": "weighted-Linfinity function-side domination, Lyapunov and local compactness criteria",
                "assumes": "0<=P<=Q kernels plus Lyapunov/local domination",
                "supplies_measure_side_owner_domination": False,
            },
            "arXiv_2605_07824": {
                "title": "Tamed Feynman-Kac diffusion processes: Killing-branching intertwine",
                "process": "one-dimensional drifted diffusion with killing/branching",
                "is_CM2_owner_trace_process": False,
            },
            "external_theorem_promoted": False,
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
    require(len(PINS) == 38, "pin count")
    require(result["live_arrival_split"]["rows"][0]["c_split_star"] == "1/2", "split")
    require(len(result["sectorwise_common_kernel"]["finite_replay"]) == 7, "sectors")
    require(len(result["remaining_eight_fields"]["rows"]) == 8, "open fields")
    return {
        "pins": "38/38", "split_rows": 3, "sector_rows": 7,
        "raw_separator_rows": 16, "cemetery_rows": 10,
        "open_field_rows": 8, "status": "PASS",
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
        print(f"ROUND65_GATE5_CERT_ERROR: {exc}", file=sys.stderr)
        return 1
    print("Gate5 maturity: 10/18")
    print("complete blocks: 0")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
