#!/usr/bin/env python3
"""Producer for the append-only Round-66 Gate-5 owner-overlap frontier."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round66_common import (
    CertError, canonical_bytes, digest, require, sha256_path, validate_pins,
)


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate5.round66.owner-overlap-sector-flux-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-gate5-round66-owner-overlap-sector-flux-frontier"
REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
VERIFIER = HERE / "cm2_gate5_round66_owner_overlap_sector_flux_frontier_verifier.py"
COMMON = HERE / "cm2_round66_common.py"

PINS = {
    "cm2-sixty-fifth-direct-assault-2026-07-21.md":
        "aeaafaf3411e90d6d1843159e248f18af12e5fdf993acfb9685adcc1b14e7bb0",
    "cm2-sixty-fifth-direct-assault-manifest-2026-07-21.sha256":
        "22283d37c12651e955b2502ad7660fa22d309c1d1902c471b1527470d6cc1cc2",
    "cm2-round65-independent-core-frontier-audit-2026-07-21.md":
        "b33405043f505f3f6323a6faf0de8f33e3f4c1f28db7ac891a56b2242a4df9e4",
    "cm2-round65-independent-core-frontier-audit-manifest-2026-07-21.json":
        "92ba883654f761a4df5974d889f99aa077769bb37ba0cd5d6fd03ceb8470629f",
    "cm2-round65-independent-core-frontier-audit-manifest-2026-07-21.sha256":
        "56cdbe5748338979e03eca9a859f119fda8c88d7b6663f530400f00f69583ed9",
    "cm2-round65-cross-gate-positive-potential-technology-frontier-assault-2026-07-21.md":
        "9bcf25242a4190e591919bd38233da4e036be22fc2c84739540a555f5f56b0ab",
    "cm2-round65-cross-gate-positive-potential-technology-frontier-manifest-2026-07-21.json":
        "f731715bd734649073e0bd35763c170a48ef8383f6dd892696b52a98ea86eb14",
    "cm2-round65-cross-gate-positive-potential-technology-frontier-manifest-2026-07-21.sha256":
        "ba3e550ac55d7e482d15817cdb9011c7a118100d90158d1c7aabdfeb94785b5a",
    "cm2-gate5-round65-cross-time-sector-jordan-cemetery-frontier-assault-2026-07-21.md":
        "345215404cd3c2e634a614682fc7404fbca57721b3ddd1ab2959699734efd154",
    "cm2-gate5-round65-cross-time-sector-jordan-cemetery-frontier-manifest-2026-07-21.json":
        "43d80312d1ada853af84a9d8f5edd4393388a62ae3788e9fbcc1eaa4ea510ce5",
    "cm2-gate5-round65-cross-time-sector-jordan-cemetery-frontier-manifest-2026-07-21.sha256":
        "f9863eda87a427723183896815fda5c2036f826c93be789a1189e0f85b8fbdc1",
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
    "cm2-gate34-round27-arbitrary-n-path-schema-assault-2026-07-18.md":
        "54e65330ddac06604da734fe358fad78e7182fea04a1cd0615ae54e3f0cb2400",
    "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json":
        "988f364bd1e6943178238c072e725de01af36452ef25d179eae6aef4000f7916",
    "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.sha256":
        "632ea2ac0a83f3beec42fcc993d8ed7f5d6d7e51d079b84b1ee6b2ac7490b8a0",
}


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def overlap_rows() -> list[dict[str, Any]]:
    return [
        {"atom": "a", "relative_n": 1, "mass": 2, "in_j": True,
         "in_next": False, "role": "terminal_exit"},
        {"atom": "b", "relative_n": 2, "mass": 3, "in_j": True,
         "in_next": True, "role": "overlap"},
        {"atom": "c", "relative_n": 3, "mass": 5, "in_j": True,
         "in_next": False, "role": "owner_departure"},
        {"atom": "d", "relative_n": 3, "mass": 7, "in_j": False,
         "in_next": True, "role": "owner_birth"},
        {"atom": "e", "relative_n": 4, "mass": 11, "in_j": True,
         "in_next": True, "role": "overlap"},
        {"atom": "f", "relative_n": 4, "mass": 13, "in_j": False,
         "in_next": False, "role": "inactive"},
    ]


def sector_rows() -> list[dict[str, Any]]:
    data = [
        ("active-clock", [Q(4), Q(2)], [Q(2), Q(1)]),
        ("raw-Z", [Q(2), Q(4)], [Q(4), Q(4)]),
        ("power-Orlicz", [Q(8), Q(8)], [Q(4), Q(16)]),
        ("complement", [Q(1), Q(2)], [Q(1), Q(1)]),
        ("variation", [Q(2), Q(1)], [Q(1), Q(2)]),
        ("common-mode", [Q(1), Q(1)], [Q(1), Q(1)]),
        ("one-shot-cemetery", [Q(1), Q(1)], [Q(1), Q(1)]),
    ]
    rows = []
    for name, before, after in data:
        ratios = [after[i] / before[i] for i in range(2)]
        rows.append({
            "sector": name,
            "h_j_on_overlap": [qstr(x) for x in before],
            "h_next_on_overlap": [qstr(x) for x in after],
            "overlap_ratios": [qstr(x) for x in ratios],
            "birth_free_kappa_star": qstr(max(ratios)),
            "positive_birth_kappa_star": "INFINITY",
        })
    return rows


def raw_truncation_rows(count: int = 12) -> list[dict[str, Any]]:
    return [{"N": n, "K_truncated": n, "raw_mark": str(2 ** (n + 1)),
             "finite": True} for n in range(count)]


def open_fields() -> list[dict[str, str]]:
    return [
        {"field": "F5", "name": "inverse_Jacobian_bound",
         "first_unpaid": "global homogeneous return-word inverse-Jacobian row"},
        {"field": "F6", "name": "log_Jacobian_distortion_sum",
         "first_unpaid": "global same-block all-record distortion sum"},
        {"field": "F10", "name": "coarea_density_regular_bound",
         "first_unpaid": "birth/raw/cemetery/all-time positive ledger"},
        {"field": "F11", "name": "dynamic_Holder_test_pullback_bound",
         "first_unpaid": "branch-uniform physical dynamic test embedding"},
        {"field": "F14", "name": "regular_density_operator_cost",
         "first_unpaid": "complete F10 and one recovered strong block"},
        {"field": "F15", "name": "standard_family_operator_cost",
         "first_unpaid": "raw-Orlicz recovery and positive cemetery"},
        {"field": "F17", "name": "dynamic_test_operator_cost",
         "first_unpaid": "all-input vector-current strong recipient"},
        {"field": "F18", "name": "operator_phase_block",
         "first_unpaid": "all preceding rows on one physical block"},
    ]


def build_result() -> dict[str, Any]:
    rows = overlap_rows()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "append_only": True,
            "old_artifacts_modified": False,
            "pinned_round65_owner_cemetery_jordan_chain": PINS,
        },
        "actual_fixed_time_input": {
            "formula": "m_(j,a)^own=1_(E_(j,a)^owner intersect R_(j,a)^reg)m_occ for n(a)>j",
            "same_raw_occurrence_law": True,
            "owner_pieces_disjoint_at_each_fixed_j": True,
            "owner_sets_nested_across_j": "NOT_CERTIFIED",
            "time_j_deleted_or_deduplicated": False,
            "actual_overlap_departure_birth_masses": "NOT_CERTIFIED",
        },
        "terminal_record_crosswalk": {
            "status": "CERTIFIED_EXACT_BOREL_MAXIMAL_OVERLAP",
            "ambient_measure": "M=sum_a delta_a tensor m_occ on immutable terminal-record copies",
            "time_update": "U_j(j,a,x)=(j+1,a,x) for n(a)>j+1",
            "time_coordinate_retained": True,
            "terminal_eligibility_nested": "{n>j+1} subset {n>j}",
            "terminal_eligibility_implies_owner_set_nesting": False,
            "overlap": "O_j=S_j intersect S_next intersect {bar(ell)_j=bar(ell)_next}",
            "terminal_departure": "Dterm_j=S_j intersect {n=j+1}",
            "switch_departure": "Dswitch_j=S_j minus (O_j union Dterm_j)",
            "owner_birth": "B_next=S_next minus O_j",
            "owner_label_switch_is_death_plus_birth": True,
            "cross_time_owner_deduplication": "ILLEGAL",
        },
        "rn_frontier": {
            "status": "CERTIFIED_EXACT_ON_FULL_TERMINAL_SOURCE_OWNER_LABEL",
            "live_coefficient": {
                "positive_birth": "INFINITY",
                "birth_free_positive_overlap": "1",
                "zero_target": "0",
            },
            "birth_free_live_plus_departure_coefficient": "1",
            "birth_free_density_on_overlap": "1",
            "positive_overlap_route_coefficient_below_w_Z_inverse": False,
            "reason": "w_Z>1 and full-label surviving density is one",
            "total_mass_ratio_is_Linfinity_RN_ratio": False,
            "finite_replay": {
                "rows": rows,
                "source_total": 21,
                "next_total": 21,
                "overlap_total": 14,
                "terminal_departure_total": 2,
                "switch_departure_total": 5,
                "birth_total": 7,
                "with_birth_c_live_star": "INFINITY",
                "birth_free_next_source_mass_ratio": "2/3",
                "birth_free_full_label_c_live_star": "1",
                "birth_free_accounting_c_star": "1",
            },
            "actual_c_live_star": "NOT_EVALUABLE_WITH_FROZEN_MASSES",
        },
        "seven_sector_overlap": {
            "status": "CERTIFIED_EXACT_TYPED_RN_FORMULA",
            "sectors": [
                "active-clock", "raw-Z", "power-Orlicz", "complement",
                "variation", "common-mode", "one-shot-cemetery",
            ],
            "formula": "kappa_s_star=ess_sup_O h_next^s/h_j^s after zero-denominator and positive-birth singular parts vanish",
            "common_tagged_coefficient": "max_s kappa_s_star on the disjoint sector-tagged carrier",
            "positive_target_sector_birth": "INFINITY",
            "sum_marks_first_is_typed_safe": False,
            "finite_replay": sector_rows(),
            "actual_fixed_j_base_owner": "FINITE",
            "actual_fixed_j_complement_variation_common_mode": "FINITE",
            "actual_active_clock_raw_Z_power_Orlicz": "NOT_CERTIFIED_FINITE",
            "actual_pre_regularization_cemetery": "NOT_MATERIALIZED",
            "actual_finite_seven_sector_slice": "NOT_CERTIFIED",
            "actual_sector_drift_coefficients": "NOT_CERTIFIED",
        },
        "raw_Orlicz_frontier": {
            "same_slice_comparison": "H_raw<=H_Orl<C_col H_raw",
            "comparison_creates_finiteness": False,
            "comparison_creates_cross_j_coefficient": False,
            "finite_truncations_uniform": False,
            "truncation_rows": raw_truncation_rows(),
            "actual_raw_Z_Orlicz_drift": "NOT_CERTIFIED",
        },
        "arrival_typing": {
            "terminal_exit_is_pre_regularization_cemetery": False,
            "switch_departure_is_one_shot": True,
            "absorbing_occupancy_for_w_Z_gt_1": "DIVERGES_IF_NONZERO",
            "weighted_departure_payment_needed": "sum_j w_Z^(j+1)sigma_j(Dterm_j union Dswitch_j)<infinity",
            "live_plus_departure_identity_supplies_decay": False,
            "pre_regularization_cemetery": "NOT_MATERIALIZED",
        },
        "oriented_positive_frontier": {
            "Round54_source_pair": "mu^+,mu^- with equal total m_p",
            "Round61_target_pair": "xi_j^f,xi_j^r on the orientation-cost owner law",
            "exact_mass_crosswalk_necessary_row": "xi_j^f(X)=m_p=xi_j^r(X)",
            "forward_reverse_equality_is_only_first_scalar_test": True,
            "forward_strict_upper": "395304765824751/220000",
            "reverse_strict_upper": "162772550633721/176000",
            "upper_sum": "2395081816467609/880000",
            "upper_difference": "69759664557309/80000",
            "unequal_upper_bounds_imply_unequal_actual_totals": False,
            "positive_lower_bound_for_m_p": "NOT_CERTIFIED",
            "two_RN_rows": "NOT_CERTIFIED",
            "common_mode_equality": "NOT_CERTIFIED",
            "terminal_crosswalk_identifies_abs_lambda_with_m_owner": False,
            "physical_oriented_carrier": "NOT_CERTIFIED",
        },
        "remaining_eight_fields": {
            "required_field_count": 18,
            "certified_maturity": 10,
            "open_count": 8,
            "rows": open_fields(),
            "new_field_promoted": False,
        },
        "latest_technology_boundary": {
            "dominated_kernel_theorems_assume_domination_and_Lyapunov_rows": True,
            "dominated_kernel_theorems_remove_owner_birth_singularity": False,
            "killing_branching_diffusions_are_same_process_recipient": False,
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
    finite = result["rn_frontier"]["finite_replay"]
    require(len(PINS) == 47, "pin count")
    require(finite["source_total"] == finite["next_total"] == 21, "finite totals")
    require(finite["overlap_total"] == 14 and finite["birth_total"] == 7,
            "overlap/birth")
    require(len(result["seven_sector_overlap"]["finite_replay"]) == 7, "sector count")
    require(len(result["remaining_eight_fields"]["rows"]) == 8, "field count")
    return {
        "pins": "47/47",
        "overlap_rows": 6,
        "sector_rows": 7,
        "raw_truncation_rows": 12,
        "open_field_rows": 8,
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
        print(f"ROUND66_GATE5_CERT_ERROR: {exc}", file=sys.stderr)
        return 1
    print("Gate5 maturity: 10/18")
    print("complete blocks: 0")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
