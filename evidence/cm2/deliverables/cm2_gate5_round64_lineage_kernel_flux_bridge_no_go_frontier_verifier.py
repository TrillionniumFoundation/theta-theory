#!/usr/bin/env python3
"""Independent verifier for the Round-64 Gate-5 no-go frontier."""

from __future__ import annotations

import argparse
import copy
import json
import subprocess
import sys
from decimal import Decimal, localcontext
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round64_common import (
    CertError, digest, replay_sidecar, require, semantic_mutation_test,
    sha256_path, strict_json_path, strict_json_self_test, validate_pins,
)


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate5.round64.lineage-kernel-flux-bridge-no-go.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-gate5-round64-lineage-kernel-flux-bridge-no-go-frontier"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
SIDECAR = HERE / f"{PREFIX}-manifest-2026-07-21.sha256"
REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
CERT = HERE / "cm2_gate5_round64_lineage_kernel_flux_bridge_no_go_frontier_cert.py"
VERIFIER = Path(__file__).resolve()
COMMON = HERE / "cm2_round64_common.py"
EXPECTED_RESULT_DIGEST = "cbb5f6c2a5e706fa5eddaff6d3b6e1af79640dcb3942360ad1026a5d295c8205"

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


def integrity(data: dict[str, Any], files: bool = True) -> None:
    if files:
        validate_pins(HERE, PINS)
    require(data.get("schema") == MANIFEST_SCHEMA and data.get("pins") == PINS,
            "manifest schema/pins")
    if files:
        require(data.get("report_sha256") == sha256_path(REPORT), "report hash")
        require(data.get("certificate_sha256") == sha256_path(CERT), "cert hash")
        require(data.get("verifier_sha256") == sha256_path(VERIFIER), "verifier hash")
        require(data.get("common_sha256") == sha256_path(COMMON), "common hash")
    result = data.get("result")
    require(isinstance(result, dict), "result root")
    replay = copy.deepcopy(result)
    recorded = replay.pop("internal_replay_digest", None)
    require(recorded == EXPECTED_RESULT_DIGEST and digest(replay) == recorded,
            "result digest")
    require(data.get("verdict") == result.get("strict_status"), "verdict alias")


def semantics(result: dict[str, Any]) -> None:
    require(result["schema"] == RESULT_SCHEMA, "result schema")
    require(result["provenance"] == {
        "append_only": True, "old_artifacts_modified": False,
        "pinned_round63_and_gate5_inputs": PINS,
    }, "provenance")
    lineage = result["owner_lineage_kernel"]
    require(lineage["status"] == "CERTIFIED_EXACT_IFF", "lineage status")
    require(lineage["standard_Borel_disintegration_required"] is True, "disintegration")
    require(len(lineage["rows"]) == 3, "lineage rows")
    strict, stationary, singular = lineage["rows"]
    require([Q(x) for x in strict["RN_ratios"]] == [Q(1, 4), Q(1, 2)] and
            Q(strict["c_star"]) == Q(1, 2) and
            strict["kernel_exists_with_c_star"] is True, "strict lineage row")
    require(stationary["c_star"] == "1" and stationary["kernel_exists_with_c_star"] is True,
            "stationary lineage row")
    require(singular["c_star"] == "INFINITY" and
            singular["kernel_exists_with_c_star"] is False, "singular lineage row")
    require(len(lineage["nonuniform_replay"]) == 5, "nonuniform rows")
    require(lineage["submarkov_requires_r_j_le_1"] is True, "sub-Markov marginal row")
    kappas = [Q(1, 2), Q(1, 3), Q(1, 4), Q(1, 5)]
    product = Q(1)
    for j, row in enumerate(lineage["nonuniform_replay"]):
        require(Q(row["product_kappa_i_i<j"]) == product, "nonuniform product")
        require(Q(row["w_test_power_times_product"]) == Q(3, 2)**j * product,
                "nonuniform weighted product")
        if j < len(kappas):
            product *= kappas[j]
    require(lineage["actual_cross_j_same_label_domination"] == "NOT_CERTIFIED",
            "actual lineage guard")

    trace = result["trace_density_threshold"]
    with localcontext() as ctx:
        ctx.prec = 120
        rho = (Decimal(111718729) / Decimal(111718750)) ** Decimal(9148)
        w = (Decimal(1) + Decimal(1) / rho) / Decimal(2)
        ratio = w.ln() / (-rho.ln())
        qstar = Decimal(1) / (Decimal(1) - ratio)
        q2 = w * rho.sqrt()
        require(Decimal(trace["rho_decimal"]) == rho and Decimal(trace["w_Z_decimal"]) == w,
                "rho/w decimals")
        require(Decimal(trace["log_ratio"]) == ratio and
                Decimal(trace["q_trace_star"]) == qstar, "qstar decimal")
        require(Decimal(trace["q2_factor"]) == q2, "q2 decimal")
    require(trace["q_trace_star_gt_2"] is True and trace["q2_factor_gt_1"] is True and
            trace["all_q_le_2_fail_threshold"] is True, "trace threshold")
    require(trace["q_col_is_trace_RN_exponent"] is False and
            Decimal(trace["q_col_decimal"]) > 800, "q_col typing guard")

    sectors = result["sectorwise_Feynman_Kac"]
    require(len(sectors["required_sectors"]) == 7, "sector count")
    harmonic = sectors["separator"]["rows"]
    require(len(harmonic) == 14, "harmonic rows")
    for row in harmonic:
        j = row["j"]
        require(Q(row["base_mass"]) == Q(1, 3**j), "harmonic mass")
        require(Q(row["charge"]) == Q(2**j, j + 1), "harmonic charge")
        require(Q(row["weighted_base_term"]) == Q(1, 2**j), "base term")
        require(Q(row["weighted_charge_term"]) == Q(1, j + 1), "charge term")
    require(sectors["separator"]["base_weighted_sum"] == "2" and
            sectors["separator"]["charge_weighted_sum"] == "DIVERGES_HARMONIC",
            "harmonic separator verdict")
    require(sectors["actual_all_sector_positive_drift"] == "NOT_CERTIFIED",
            "sector drift guard")
    require(sectors["unified_positive_slice_upstream"] == {
        "fixed_j_complement_variation_common_mode": "FINITE_PINNED",
        "actual_raw_Z_power_Orlicz_finite_RHS": "NOT_CERTIFIED",
        "positive_pre_cemetery_slice_law": "NOT_MATERIALIZED",
        "unified_finite_Lambda_j_before_drift": "NOT_CERTIFIED",
    }, "unified positive upstream")

    gaps = result["small_gap_joint_criterion"]
    cuts = gaps["remaining_N_cut"]
    require(cuts["codes"] == [
        "chart_atlas", "homogeneity", "hole_cemetery_boundary",
        "owner_tie_change", "non_source_endpoint", "later_word_singularity_pullback",
    ], "N_cut codes")
    require(cuts["union_zero_iff_every_coded_row_zero"] is True and
            cuts["chi_ll_nu_only_transfers_already_proved_nu_zero"] is True and
            cuts["actual_all_coded_zero_rows"] == "NOT_CERTIFIED", "N_cut guards")
    require(gaps["G_zero_sets_Y_to_infinity"] is True and
            "G_j<=2^-k" in gaps["decreasing_sets"], "N_acc extended definition")
    require(gaps["accumulation_nullity_follows"] is True, "gap implication")
    gap_rows = gaps["separator"]["rows"]
    require(len(gap_rows) == 14, "gap rows")
    for row in gap_rows:
        j = row["j"]
        require(Q(row["gap"]) == Q(1, 2**j) and row["Y"] == j, "gap/Y")
        require(Q(row["mass"]) == Q(1, 3**j * (j + 1)), "gap mass")
        require(Q(row["weighted_exponential_charge"]) == Q(1, j + 1),
                "gap weighted charge")
        require(row["has_accumulation_atom"] is False, "gap atom")
    require(gaps["actual_same_law_joint_bound"] == "NOT_CERTIFIED", "gap guard")

    cemetery = result["cemetery_typing"]
    require(cemetery["positive_cemetery_must_be"] == "ONE_SHOT_ARRIVAL_LEDGER",
            "cemetery typing")
    require(cemetery["absorbing_occupancy_recounted_each_slice_diverges_for_w_Z_gt_1"] is True and
            cemetery["live_drift_pays_pre_regularization_cemetery"] is False,
            "cemetery guards")

    jordan = result["Jordan_bridge"]
    require("tag-preserving" in jordan["typed_crosswalk_required"], "Jordan crosswalk")
    require(jordan["exact_alignment"] == "T_*mu+=xi^f and T_*mu-=xi^r",
            "Jordan exact alignment")
    require("signed J equality and common-mode lambda equality" in jordan["alignment_iff"],
            "Jordan alignment")
    require("T_*mu+<=C_f" in jordan["lawful_domination"] and
            jordan["domination_variation_bound"] == "|T_*J|<=C_f xi^f+C_r xi^r" and
            jordan["domination_is_Jordan_alignment_or_F10"] is False,
            "Jordan domination tier")
    require(jordan["one_point_separator"]["signed_laws_equal_zero"] is True and
            jordan["one_point_separator"]["positive_totals_uniformly_comparable"] is False,
            "Jordan separator")
    require(jordan["Round54_Round61_common_carrier_token_RN_bridge"] == "NOT_CERTIFIED",
            "Jordan physical guard")

    suffix = result["suffix_cube"]
    require(suffix["Borel_atoms"] == 32 and len(suffix["rows"]) == 32, "suffix cube size")
    seen: set[tuple[bool, ...]] = set()
    for atom, row in enumerate(suffix["rows"]):
        require(row["atom"] == atom and row["fixed_bits"] == [True, True],
                "suffix fixed bits")
        bits = tuple(row["open_bits"])
        require(len(bits) == 5, "suffix bit count")
        seen.add(bits)
    require(len(seen) == 32 and suffix["typing_implies_remaining_values"] is False and
            suffix["typing_implies_R_ge_rK"] is False, "suffix independence")
    require("disjoint_union" in suffix["first_failure_partition"] and
            suffix["universal_R_ge_rK_iff_all_first_failure_cells_empty"] is True and
            suffix["drift_proves_first_failure_cells_empty"] is False,
            "suffix first-failure compression")
    require(result["latest_technology_boundary"]["external_theorem_promoted"] is False,
            "external theorem guard")
    require(result["strict_status"] == {
        "Gate5": "NOT_CERTIFIED", "Gate5_maturity": "10/18",
        "complete_18_field_blocks": 0, "complete_composite_gates": "0/5",
        "CM2": "NO-GO_FOR_CLAIM",
    }, "strict state")


def independent_replay() -> dict[str, Any]:
    beta = [Q(4), Q(2)]
    beta_next = [Q(1), Q(1)]
    ratios = [b / a for a, b in zip(beta, beta_next)]
    require(max(ratios) == Q(1, 2), "independent lineage cstar")
    with localcontext() as ctx:
        ctx.prec = 100
        rho = (Decimal(111718729) / Decimal(111718750)) ** Decimal(9148)
        w = (Decimal(1) + Decimal(1) / rho) / Decimal(2)
        require(w * rho.sqrt() > 1, "independent q2 obstruction")
    base_prefix = sum((Q(1, 2**j) for j in range(30)), Q(0))
    harmonic_prefix = sum((Q(1, j + 1) for j in range(30)), Q(0))
    require(base_prefix < 2 and harmonic_prefix > 3, "independent harmonic separator")
    suffixes = {tuple(bool((atom >> bit) & 1) for bit in range(5)) for atom in range(32)}
    require(len(suffixes) == 32, "independent suffix cube")
    return {"lineage_c_star": "1/2", "q2_obstruction": "PASS", "suffix_atoms": 32}


def deterministic(data: dict[str, Any]) -> None:
    proc = subprocess.run(
        [sys.executable, str(CERT), "--manifest-json", "--verifier", str(VERIFIER)],
        cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=180,
    )
    require(proc.returncode == 0, f"producer: {proc.stderr.decode().strip()}")
    require(proc.stdout == MANIFEST.read_bytes() and strict_json_path(MANIFEST) == data,
            "deterministic producer")


def run_audit(data: dict[str, Any], regenerate: bool = True) -> None:
    integrity(data)
    semantics(data["result"])
    independent_replay()
    if SIDECAR.exists():
        replay_sidecar(HERE, SIDECAR, 5)
    if regenerate:
        deterministic(data)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--reemit", type=Path)
    args = parser.parse_args()
    try:
        data = strict_json_path(MANIFEST)
        if args.audit:
            run_audit(data)
            print("AUDIT: PASS")
            return 0
        if args.replay:
            integrity(data)
            semantics(data["result"])
            print(json.dumps(independent_replay(), sort_keys=True))
            return 0
        if args.self_test:
            run_audit(data)
            semantic = semantic_mutation_test(data, integrity, semantics)
            strict = strict_json_self_test()
            print(f"HOSTILE_SEMANTIC_REJECTED: {semantic}/{semantic}")
            print(f"HOSTILE_JSON_REJECTED: {strict}/{strict}")
            return 0
        if args.reemit is not None:
            run_audit(data, regenerate=False)
            proc = subprocess.run(
                [sys.executable, str(CERT), "--manifest-json", "--verifier", str(VERIFIER)],
                cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=180,
            )
            require(proc.returncode == 0, "reemit producer")
            args.reemit.write_bytes(proc.stdout)
            require(args.reemit.read_bytes() == MANIFEST.read_bytes(), "reemit bytes")
            return 0
    except (CertError, OSError, ValueError, KeyError, TypeError, ArithmeticError,
            subprocess.SubprocessError) as exc:
        print(f"ROUND64_GATE5_VERIFY_ERROR: {exc}", file=sys.stderr)
        return 1
    print("Gate5 maturity: 10/18")
    print("complete blocks: 0")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
