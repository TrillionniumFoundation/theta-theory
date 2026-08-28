#!/usr/bin/env python3
"""Independent verifier for the Round-65 Gate-5 frontier."""

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
RESULT_SCHEMA = "cm2.gate5.round65.cross-time-sector-jordan-cemetery-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-gate5-round65-cross-time-sector-jordan-cemetery-frontier"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
SIDECAR = HERE / f"{PREFIX}-manifest-2026-07-21.sha256"
REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
CERT = HERE / "cm2_gate5_round65_cross_time_sector_jordan_cemetery_frontier_cert.py"
VERIFIER = Path(__file__).resolve()
COMMON = HERE / "cm2_round64_common.py"
EXPECTED_PINS_DIGEST = "5bd8482b14d47d5092bfeb317cc7762f9715d45b10b45be3b7b8f57496ab5ce0"
EXPECTED_RESULT_DIGEST = "987d3771d352fca2f14191ec5cfc58a8693435e8118ff1542d1da51ad54a0819"


def integrity(data: dict[str, Any], files: bool = True) -> None:
    require(data.get("schema") == MANIFEST_SCHEMA, "manifest schema")
    pins = data.get("pins")
    require(isinstance(pins, dict) and len(pins) == 38, "pin root/count")
    require(digest(pins) == EXPECTED_PINS_DIGEST, "pin-set digest")
    if files:
        validate_pins(HERE, pins)
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
    provenance = result["provenance"]
    require(provenance["append_only"] is True and
            provenance["old_artifacts_modified"] is False and
            digest(provenance["pinned_round64_round61_63_and_physical_inputs"])
            == EXPECTED_PINS_DIGEST, "provenance")

    actual = result["actual_frozen_audit"]
    require(actual == {
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
    }, "actual frozen audit")

    constants = result["physical_constants"]
    with localcontext() as ctx:
        ctx.prec = 120
        rho = (Decimal(111718729) / Decimal(111718750)) ** Decimal(9148)
        w = (Decimal(1) + Decimal(1) / rho) / Decimal(2)
        gamma = ((Decimal(2000) / Decimal(1999)) * Decimal(1 + 48 * 9148)
                 * (Decimal(900337) / Decimal(901685)) ** Decimal(9148))
        beta = Decimal(2).ln() / (-gamma.ln())
        q_col = Decimal(2).ln() / (beta * w.ln())
        c_col = (q_col * w.ln()).exp()
        require(Decimal(constants["rho"]) == rho and Decimal(constants["w_Z"]) == w,
                "rho/w")
        require(Decimal(constants["w_Z_inverse"]) == Decimal(1) / w, "w inverse")
        require(Decimal(constants["gamma"]) == gamma and
                Decimal(constants["beta"]) == beta, "gamma/beta")
        require(Decimal(constants["q_col"]) == q_col and
                Decimal(constants["C_col"]) == c_col, "q/C col")
        require(constants["C_col_formula"] == "w_Z^q_col=2^(1/beta)", "C formula")

    split = result["live_arrival_split"]
    require(split["status"] == "CERTIFIED_EXACT_IFF" and
            "beta_next+alpha_next<=c beta" in split["criterion"] and
            split["one_shot_arrival_required"] is True, "split theorem")
    require(split["sharp_coefficient"] ==
            "||d(beta_next+alpha_next)/d beta||_infinity; infinity if singular",
            "split coefficient")
    require(len(split["rows"]) == 3, "split row count")
    strict, stationary, singular = split["rows"]
    require([Q(x) for x in strict["combined_ratios"]] == [Q(1, 2), Q(1, 2)] and
            Q(strict["c_split_star"]) == Q(1, 2) and
            strict["submarkov_split_exists"] is True, "strict split")
    require([Q(x) for x in stationary["combined_ratios"]] == [Q(3, 2), Q(1)] and
            stationary["c_split_star"] == "3/2" and
            stationary["submarkov_split_exists"] is False, "stationary split")
    require(singular["combined_ratios"] == ["0", "SINGULAR"] and
            singular["c_split_star"] == "INFINITY" and
            singular["submarkov_split_exists"] is False, "singular split")
    require(split["bound_requires_arrival_generated_from_live_split"] is True and
            split["actual_split_inputs"] == "NOT_MATERIALIZED", "arrival guard")

    sectors = result["sectorwise_common_kernel"]
    expected_sectors = [
        "active-clock", "raw-Z", "power-Orlicz", "complement",
        "variation", "common-mode", "one-shot-cemetery",
    ]
    require(sectors["status"] == "CERTIFIED_EXACT_FOR_FIBRE_CONSTANT_MARKS" and
            sectors["sectors"] == expected_sectors, "sector schema")
    require(sectors["finite_replay_r_j"] == ["1/4", "1/2"] and
            len(sectors["finite_replay"]) == 7, "sector replay")
    expected_kappa = [Q(1, 4), Q(1), Q(1, 2), Q(1, 4), Q(1, 2), Q(1, 2), Q(1)]
    for name, kappa, row in zip(expected_sectors, expected_kappa, sectors["finite_replay"]):
        require(row["sector"] == name and Q(row["kappa_star"]) == kappa,
                f"sector kappa {name}")
        pointwise = [Q(x) for x in row["pointwise_coefficients"]]
        require(max(pointwise) == kappa, f"sector max {name}")
    require(sectors["charge_marginal_tier_is_common_physical_kernel"] is False and
            sectors["actual_cross_j_ratio_and_sector_coefficients"] == "NOT_CERTIFIED" and
            sectors["unified_finite_positive_slice"] == "NOT_CERTIFIED", "sector guards")

    active = result["active_raw_Orlicz"]
    require(active["pointwise_comparison"] == "H_raw<=H_Orl<C_col H_raw" and
            active["q_col_is_trace_RN_exponent"] is False and
            active["base_drift_implies_raw_drift"] is False, "raw/Orlicz typing")
    separator = active["separator"]
    require(separator["w_test"] == "3/2" and separator["base_coefficient"] == "1/3" and
            separator["raw_coefficient"] == "2/3" and
            separator["raw_coefficient_times_w"] == "1", "raw separator constants")
    require(len(separator["rows"]) == 16, "raw separator rows")
    for row in separator["rows"]:
        j = row["j"]
        require(Q(row["beta_j"]) == Q(1, 3**j) and row["K_j"] == j,
                "raw beta/K")
        require(Q(row["base_weighted_term"]) == Q(1, 2**j) and
                Q(row["raw_mark"]) == Q(2 ** (j + 1)) and
                Q(row["raw_weighted_term"]) == Q(2), "raw terms")
    require(active["actual_clock_raw_Orlicz_finite"] == "NOT_CERTIFIED" and
            active["actual_drift_coefficients"] == "NOT_CERTIFIED", "active guards")

    cemetery = result["cemetery_resolvent"]
    require("/(1-w_Z q)" in cemetery["exact_identity"] and
            cemetery["absorbing_q_1_with_nonzero_arrival"] == "DIVERGES_FOR_w_Z_gt_1",
            "cemetery resolvent")
    replay = cemetery["finite_replay"]
    require(replay["w_test"] == "3/2" and replay["q_test"] == "1/3" and
            replay["arrival_weighted_sum"] == "8/5" and
            replay["occupancy_weighted_sum"] == "16/5", "cemetery totals")
    occupancy = Q(0)
    for row in replay["rows"]:
        j = row["j"]
        arrival = Q(1, 4**j)
        occupancy = arrival + Q(1, 3) * occupancy
        require(Q(row["arrival"]) == arrival and Q(row["leaky_occupancy"]) == occupancy,
                "cemetery recurrence")
        require(Q(row["weighted_arrival"]) == Q(3, 2)**j * arrival and
                Q(row["weighted_occupancy"]) == Q(3, 2)**j * occupancy,
                "cemetery weights")
    require(cemetery["actual_one_shot_pre_regularization_arrival"] == "NOT_MATERIALIZED",
            "cemetery guard")

    bridge = result["oriented_positive_bridge"]
    require(bridge["status"] == "CERTIFIED_EXACT_IFF" and
            bridge["sharp_coefficient"] == "max of the two RN essential suprema",
            "oriented theorem")
    strict_bridge = bridge["strict_replay"]
    require([Q(x) for x in strict_bridge["forward_ratios"]] == [Q(1, 4), Q(1, 2)] and
            [Q(x) for x in strict_bridge["reverse_ratios"]] == [Q(1, 2), Q(1, 4)] and
            strict_bridge["c_star"] == "1/2", "oriented replay")
    require(bridge["Round54_source_equal_positive_masses"] is True and
            bridge["Round61_target_forward_reverse_total_equality"] == "NOT_CERTIFIED" and
            bridge["positive_sum_identity"] == "S=|J|+2lambda" and
            bridge["signed_only_controls_common_mode"] is False and
            bridge["Round54_Round61_carrier_RN_common_mode_bridge"] == "NOT_CERTIFIED",
            "oriented guards")

    fields = result["remaining_eight_fields"]
    names = [
        ("F5", "inverse_Jacobian_bound"),
        ("F6", "log_Jacobian_distortion_sum"),
        ("F10", "coarea_density_regular_bound"),
        ("F11", "dynamic_Holder_test_pullback_bound"),
        ("F14", "regular_density_operator_cost"),
        ("F15", "standard_family_operator_cost"),
        ("F17", "dynamic_test_operator_cost"),
        ("F18", "operator_phase_block"),
    ]
    require(fields["required_field_count"] == 18 and fields["certified_maturity"] == 10 and
            fields["open_count"] == 8 and fields["new_field_promoted"] is False and
            [(row["field"], row["name"]) for row in fields["rows"]] == names,
            "remaining fields")

    tech = result["latest_technology_boundary"]
    require(tech["arXiv_2510_19573v3"]["supplies_measure_side_owner_domination"] is False and
            tech["arXiv_2605_07824"]["is_CM2_owner_trace_process"] is False and
            tech["external_theorem_promoted"] is False, "technology guard")
    require(result["strict_status"] == {
        "Gate5": "NOT_CERTIFIED", "Gate5_maturity": "10/18",
        "complete_18_field_blocks": 0, "complete_composite_gates": "0/5",
        "CM2": "NO-GO_FOR_CLAIM",
    }, "strict state")


def independent_replay() -> dict[str, Any]:
    source = [Q(4), Q(2)]
    live = [Q(1), Q(1)]
    arrivals = [Q(1), Q(0)]
    split_ratios = [(live[i] + arrivals[i]) / source[i] for i in range(2)]
    require(max(split_ratios) == Q(1, 2), "independent split")

    r = [Q(1, 4), Q(1, 2)]
    raw_before, raw_after = [Q(8), Q(4)], [Q(8), Q(8)]
    require(max(r[i] * raw_after[i] / raw_before[i] for i in range(2)) == 1,
            "independent raw sector")

    base_prefix = sum((Q(1, 2**j) for j in range(40)), Q(0))
    raw_prefix = sum((Q(2) for _ in range(40)), Q(0))
    require(base_prefix < 2 and raw_prefix == 80, "independent raw separator")

    w, q = Q(3, 2), Q(1, 3)
    arrival_sum = Q(1) / (Q(1) - w / 4)
    occupancy_sum = arrival_sum / (Q(1) - w * q)
    require(arrival_sum == Q(8, 5) and occupancy_sum == Q(16, 5),
            "independent cemetery resolvent")

    forward = max(Q(1, 4), Q(1, 2))
    reverse = max(Q(1, 2), Q(1, 4))
    require(max(forward, reverse) == Q(1, 2), "independent oriented bridge")
    return {
        "split_c_star": "1/2", "sector_raw_kappa": "1",
        "raw_separator_prefix": "80", "cemetery_weighted": "16/5",
        "oriented_c_star": "1/2", "open_fields": 8,
    }


def deterministic(data: dict[str, Any]) -> None:
    proc = subprocess.run(
        [sys.executable, str(CERT), "--manifest-json", "--verifier", str(VERIFIER)],
        cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=240,
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
                cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                check=False, timeout=240,
            )
            require(proc.returncode == 0, "reemit producer")
            args.reemit.write_bytes(proc.stdout)
            require(args.reemit.read_bytes() == MANIFEST.read_bytes(), "reemit bytes")
            return 0
    except (CertError, OSError, ValueError, KeyError, TypeError, ArithmeticError,
            subprocess.SubprocessError) as exc:
        print(f"ROUND65_GATE5_VERIFY_ERROR: {exc}", file=sys.stderr)
        return 1
    print("Gate5 maturity: 10/18")
    print("complete blocks: 0")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
