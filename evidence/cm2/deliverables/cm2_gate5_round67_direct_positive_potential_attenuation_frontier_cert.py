#!/usr/bin/env python3
"""Producer for the append-only Round-67 Gate-5 direct-potential frontier."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round67_common import (
    CertError, canonical_bytes, digest, require, sha256_path, validate_pins,
)


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate5.round67.direct-positive-potential-attenuation-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-gate5-round67-direct-positive-potential-attenuation-frontier"
REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
VERIFIER = HERE / "cm2_gate5_round67_direct_positive_potential_attenuation_frontier_verifier.py"
COMMON = HERE / "cm2_round67_common.py"

PINS = {
    "cm2-sixty-sixth-direct-assault-2026-07-21.md":
        "690cfeb13108314a3a05f5e4cd342d573c41e66551464ebf7f4b5576f374b811",
    "cm2-sixty-sixth-direct-assault-manifest-2026-07-21.sha256":
        "b437761fb84aa431e468af587e2207adadf6e0a996ee593a93df467147be3b5d",
    "cm2-round66-independent-core-frontier-audit-2026-07-21.md":
        "68d9b65f843c6e35e9f8c5e6954fb76e87970fc9bc558e691cecaafeb9850ebd",
    "cm2-round66-independent-core-frontier-audit-manifest-2026-07-21.json":
        "b67b76e52d073989fac6fb41eaf3e49167aa1e166d32003c72129e08ec6d46b3",
    "cm2-round66-independent-core-frontier-audit-manifest-2026-07-21.sha256":
        "6d09b81b683464dcf45815ed9e98635c6c3a94087c19b0e4528eaf4c1659175e",
    "cm2-round66-immutable-registry-junction-tree-positive-potential-frontier-assault-2026-07-21.md":
        "9b8512389c8ede4c6b59a029565bc314f10502ec9339094036f13f33185463a2",
    "cm2-round66-immutable-registry-junction-tree-positive-potential-frontier-manifest-2026-07-21.json":
        "adc2654ed27fa62c83dd9d64ddce09832e173f50d518c464007d9bc320d6294f",
    "cm2-round66-immutable-registry-junction-tree-positive-potential-frontier-manifest-2026-07-21.sha256":
        "1122a6b11415e5f070ec4a86faa6d78a0a67a30ae836c288e3a732f1c0fa51f3",
    "cm2-gate5-round66-owner-overlap-sector-flux-frontier-assault-2026-07-21.md":
        "5328ee45c3fd69e0e4a433910e5562504d1b155e44eb20a024b05194f16d999d",
    "cm2-gate5-round66-owner-overlap-sector-flux-frontier-manifest-2026-07-21.json":
        "31f8b9068b3afaad779f299d5adb3e1ff870d3b48ad943704e1347b7ac06a686",
    "cm2-gate5-round66-owner-overlap-sector-flux-frontier-manifest-2026-07-21.sha256":
        "c538c62bbbb13f1e4b203d72d67cb3fd398752a4636c1a731a9039f9847ce4aa",
    "cm2-gate5-round65-cross-time-sector-jordan-cemetery-frontier-assault-2026-07-21.md":
        "345215404cd3c2e634a614682fc7404fbca57721b3ddd1ab2959699734efd154",
    "cm2-gate5-round65-cross-time-sector-jordan-cemetery-frontier-manifest-2026-07-21.json":
        "43d80312d1ada853af84a9d8f5edd4393388a62ae3788e9fbcc1eaa4ea510ce5",
    "cm2-gate5-round65-cross-time-sector-jordan-cemetery-frontier-manifest-2026-07-21.sha256":
        "f9863eda87a427723183896815fda5c2036f826c93be789a1189e0f85b8fbdc1",
    "cm2-round65-cross-gate-positive-potential-technology-frontier-assault-2026-07-21.md":
        "9bcf25242a4190e591919bd38233da4e036be22fc2c84739540a555f5f56b0ab",
    "cm2-round65-cross-gate-positive-potential-technology-frontier-manifest-2026-07-21.json":
        "f731715bd734649073e0bd35763c170a48ef8383f6dd892696b52a98ea86eb14",
    "cm2-round65-cross-gate-positive-potential-technology-frontier-manifest-2026-07-21.sha256":
        "ba3e550ac55d7e482d15817cdb9011c7a118100d90158d1c7aabdfeb94785b5a",
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
    "cm2-gate5-round54-collar-pairing-directional-bv-frontier-assault-2026-07-20.md":
        "81aa5bdd1071dc10cbce0ab4690c2a1da29eee2e7a238e8e8aa9b3db5256bf1a",
    "cm2-gate5-round54-collar-pairing-directional-bv-frontier-manifest-2026-07-20.json":
        "87e052dbfc369195becc5f2d4ac641c8250d72266bb73f47281b8b923d584ab5",
    "cm2-gate5-round54-collar-pairing-directional-bv-frontier-manifest-2026-07-20.sha256":
        "3ebe362d484687c64a087905cc1d29388208f13fe00f165c0623b370c3110976",
}


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def geometric_rows(count: int = 12) -> list[dict[str, Any]]:
    w, r = Q(3, 2), Q(1, 3)
    return [
        {
            "j": j,
            "conditional_survival": qstr(r ** j),
            "weighted_live_term": qstr((w * r) ** j),
            "survivor_full_label_density": "1",
        }
        for j in range(count)
    ]


def telescoping_rows(count: int = 12) -> list[dict[str, Any]]:
    w = Q(3, 2)
    rows: list[dict[str, Any]] = []
    for j in range(count):
        xj = (Q(2, 3) ** j) / (j + 1)
        xn = (Q(2, 3) ** (j + 1)) / (j + 2)
        lost = xj - xn
        rows.append({
            "j": j,
            "x_j": qstr(xj),
            "x_next": qstr(xn),
            "lost": qstr(lost),
            "weighted_live_term": qstr((w ** j) * xj),
            "weighted_arrival_term": qstr((w ** (j + 1)) * lost),
        })
    return rows


def strong_rows(count: int = 12) -> list[dict[str, Any]]:
    return [
        {
            "n": n,
            "mu_atom": qstr(Q(3, 4 ** n)),
            "tag_charge": str(2 ** n),
            "one_time_integrand": qstr(Q(3, 2 ** n)),
            "conditional_potential": str(2 ** (n + 1)),
        }
        for n in range(1, count + 1)
    ]


def sector_rows() -> list[dict[str, str]]:
    return [
        {"sector": "active-clock", "actual_fixed_j": "NOT_CERTIFIED_FINITE",
         "actual_all_time_Linfinity": "NOT_CERTIFIED"},
        {"sector": "raw-Z", "actual_fixed_j": "NOT_CERTIFIED_FINITE",
         "actual_all_time_Linfinity": "NOT_CERTIFIED"},
        {"sector": "power-Orlicz", "actual_fixed_j": "NOT_CERTIFIED_FINITE",
         "actual_all_time_Linfinity": "NOT_CERTIFIED"},
        {"sector": "complement", "actual_fixed_j": "FINITE_COST_LAW",
         "actual_all_time_Linfinity": "NOT_CERTIFIED"},
        {"sector": "variation", "actual_fixed_j": "FINITE_COST_LAW",
         "actual_all_time_Linfinity": "NOT_CERTIFIED"},
        {"sector": "common-mode", "actual_fixed_j": "FINITE_COST_LAW",
         "actual_all_time_Linfinity": "NOT_CERTIFIED"},
        {"sector": "one-shot-cemetery", "actual_fixed_j": "PRE_REG_NOT_MATERIALIZED",
         "actual_all_time_Linfinity": "NOT_CERTIFIED"},
    ]


def open_fields() -> list[dict[str, str]]:
    return [
        {"field": "F5", "round67_effect": "no global inverse-Jacobian row", "status": "OPEN"},
        {"field": "F6", "round67_effect": "no all-record distortion sum", "status": "OPEN"},
        {"field": "F10", "round67_effect": "exact H target; actual marks and tails absent", "status": "OPEN"},
        {"field": "F11", "round67_effect": "no branch-uniform physical test pullback", "status": "OPEN"},
        {"field": "F14", "round67_effect": "needs F10 and bounded recovered strong block", "status": "OPEN"},
        {"field": "F15", "round67_effect": "raw-Orlicz-recovery-cemetery sectors unpaid", "status": "OPEN"},
        {"field": "F17", "round67_effect": "physical oriented carrier/all-input current absent", "status": "OPEN"},
        {"field": "F18", "round67_effect": "preceding rows do not coexist on one block", "status": "OPEN"},
    ]


def build_result() -> dict[str, Any]:
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "append_only": True,
            "old_artifacts_modified": False,
            "terminal_nesting_reused_as_contraction": False,
            "pinned_round66_owner_sector_flux_chain": PINS,
        },
        "maximal_direct_potential": {
            "status": "CERTIFIED_EXACT",
            "record_carrier": "maximal time-retaining terminal/root/owner/event/side/branch/insertion carrier R",
            "root_kernel": "graph-supported Q_x from physical root law mu to R",
            "record_potential": "G(r)=sum_j w_Z^j sum_s g_j^s(r)",
            "conditional_potential": "H(x)=integral G(r)Q_x(dr)",
            "operator_criterion": "A:L1(mu)->positive typed direct sum bounded iff H in Linfinity(mu)",
            "operator_norm": "||A||=||H||_infinity",
            "proof_mechanism": "Tonelli positivity and normalized superlevel indicators",
            "recordwise_G_Linfinity": "SUFFICIENT_NOT_NECESSARY",
            "finite_actual_average": "INSUFFICIENT_FOR_STRONG_OPERATOR",
            "signed_cancellation_pays_positive_norm": False,
            "time_coordinate_retained": True,
        },
        "terminal_moment_identity": {
            "status": "CERTIFIED_EXACT",
            "unit_live_charge": "g_j(r)=1_{j<N(r)}",
            "record_formula": "G_live=(w_Z^N-1)/(w_Z-1)",
            "conditional_formula": "H_live=(E_x[w_Z^N]-1)/(w_Z-1)",
            "exact_strong_condition": "ess_sup_x E_x[w_Z^N]<infinity",
            "geometric_model": {
                "w_Z": "3/2",
                "tail_parameter_r": "1/3",
                "w_Z_r": "1/2",
                "E_w_to_N": "2",
                "H_live": "2",
                "survivor_full_label_RN_density": "1",
                "direct_attenuation_succeeds": True,
                "rows": geometric_rows(),
            },
            "actual_terminal_exponential_moment": "NOT_CERTIFIED",
            "round39_clearance_rank_tail_is_terminal_depth_tail": False,
        },
        "lawful_attenuation": {
            "sub_Markov": {
                "exact_potential": "sum_j w_Z^j P_(0:j)W_j",
                "pointwise_sufficient_row": "P_(0:j)W_j<=C kappa_j and sum_j w_Z^j kappa_j<infinity",
                "geometric_threshold": "w_Z*kappa<1",
                "average_mass_decay_suffices": False,
                "actual_pointwise_charged_survival": "NOT_CERTIFIED",
            },
            "Doob_Lyapunov": {
                "drift": "P_j V_(j+1)<=kappa_j V_j with V_j>=W_j",
                "source_requirement_for_unweighted_L1": "V_0 in Linfinity(mu)",
                "series_requirement": "sum_j w_Z^j product_(i<j)kappa_i<infinity",
                "integral_V_0_only_suffices": False,
                "minimal_resolvent": "H=W+w_Z P H",
                "actual_bounded_supersolution": "NOT_CERTIFIED",
            },
        },
        "one_shot_departure": {
            "status": "CERTIFIED_EXACT_WEIGHTED_TELESCOPE",
            "lost_charge": "d_(j+1)=x_j-x_(j+1)>=0",
            "finite_identity": "sum_(j=0)^N w_Z^(j+1)d_(j+1)=w_Z*x_0+(w_Z-1)sum_(j=1)^N w_Z^j*x_j-w_Z^(N+1)x_(N+1)",
            "limit_identity": "H_departure=x_0+(w_Z-1)H_live",
            "requires_weighted_live_finite": True,
            "pays_owner_birth": False,
            "pays_pre_regularization_cemetery": False,
            "absorbing_occupancy_if_nonzero": "DIVERGES_FOR_w_Z_GT_1",
            "harmonic_separator": {
                "x_j": "w_Z^(-j)/(j+1)",
                "unweighted_departures_telescope": True,
                "weighted_live": "DIVERGES_HARMONIC",
                "weighted_arrivals": "DIVERGES_HARMONIC",
                "rows": telescoping_rows(),
            },
        },
        "seven_sector_potential": {
            "status": "CERTIFIED_EXACT_TYPED",
            "sectors": [row["sector"] for row in sector_rows()],
            "formula": "H_total=sum_s H_s; H_s=sum_j w_Z^j P_(0:j)W_j^s",
            "finite_sector_equivalence": "H_total in Linfinity iff every H_s in Linfinity",
            "base_survival_pays_unbounded_marks": False,
            "actual_rows": sector_rows(),
            "actual_H_total": "NOT_EVALUABLE_OR_CERTIFIED",
        },
        "strong_separator": {
            "status": "CERTIFIED_EXACT",
            "mu": "mu{n}=3*4^(-n)",
            "w_Z": "3/2",
            "survival": "P_(0:j)=3^(-j)Id",
            "tag": "W_j(n)=2^n",
            "w_Z_kappa": "1/2",
            "one_time_actual_moment": "3",
            "all_time_actual_moment": "6",
            "conditional_potential": "H(n)=2^(n+1)",
            "H_in_Linfinity": False,
            "rows": strong_rows(),
        },
        "oriented_positive_pair": {
            "upstream_exact_mass_row": "xi_j^f(X)=m_p=xi_j^r(X)",
            "two_orientation_RN_rows": "NOT_CERTIFIED",
            "common_mode_equality": "NOT_CERTIFIED",
            "physical_immutable_carrier": "NOT_CERTIFIED",
            "positive_lower_bound_m_p": "NOT_CERTIFIED",
            "separate_upper_bounds_prove_exact_mass_row": False,
            "post_bridge_potential_requirement": "H^+,H^-,H^common in Linfinity on the same root",
            "positive_pair_decomposition": "mu^+=J^++lambda; mu^-=J^-+lambda",
            "positive_sum": "mu^++mu^-=|J|+2lambda",
            "signed_law_alone_pays_common_mode": False,
            "physical_potentials_materialized": False,
        },
        "actual_frozen_status": {
            "fixed_j_base_owner_law": "FINITE",
            "fixed_j_complement_variation_common_cost": "FINITE",
            "active_clock_raw_Z_power_Orlicz_slice": "NOT_CERTIFIED_FINITE",
            "pre_regularization_cemetery_arrival": "NOT_MATERIALIZED",
            "conditional_terminal_or_charged_survivor_tail": "NOT_CERTIFIED",
            "graph_supported_common_physical_root_kernel": "NOT_CERTIFIED",
            "direct_H_total_Linfinity": "NOT_CERTIFIED",
        },
        "remaining_eight_fields": {
            "required_field_count": 18,
            "certified_maturity": 10,
            "open_count": 8,
            "new_field_promoted": False,
            "rows": open_fields(),
        },
        "technology_boundary": {
            "dominated_kernel_and_Feynman_Kac_results_assume_physical_kernel_and_drift": True,
            "different_process_or_source_norm_imported": False,
            "external_theorem_promoted": False,
        },
        "strict_status": {
            "Gate5": "NOT_CERTIFIED",
            "Gate5_maturity": "10/18",
            "complete_18_field_blocks": 0,
            "complete_composite_gates": "0/5",
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
        "schema": MANIFEST_SCHEMA,
        "pins": PINS,
        "report_sha256": sha256_path(REPORT),
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier.resolve()),
        "common_sha256": sha256_path(COMMON),
        "result": result,
        "verdict": result["strict_status"],
    }


def replay() -> dict[str, Any]:
    validate_pins(HERE, PINS)
    result = build_result()
    require(len(PINS) == 32, "pin count")
    require(len(result["terminal_moment_identity"]["geometric_model"]["rows"]) == 12,
            "geometric rows")
    require(len(result["one_shot_departure"]["harmonic_separator"]["rows"]) == 12,
            "telescoping rows")
    require(len(result["seven_sector_potential"]["actual_rows"]) == 7, "sector rows")
    require(len(result["strong_separator"]["rows"]) == 12, "strong rows")
    require(len(result["remaining_eight_fields"]["rows"]) == 8, "field rows")
    return {
        "pins": "32/32",
        "geometric_rows": 12,
        "telescoping_rows": 12,
        "sector_rows": 7,
        "strong_rows": 12,
        "field_rows": 8,
        "status": "PASS",
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
        print(f"ROUND67_GATE5_CERT_ERROR: {exc}", file=sys.stderr)
        return 1
    print("Gate5 maturity: 10/18")
    print("complete blocks: 0")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
