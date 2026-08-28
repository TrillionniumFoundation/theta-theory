#!/usr/bin/env python3
"""Independent verifier for the Round-67 Gate-5 direct-potential frontier."""

from __future__ import annotations

import argparse
import copy
import json
import subprocess
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round67_common import (
    CertError, digest, replay_sidecar, require, semantic_mutation_test,
    sha256_path, strict_json_path, strict_json_self_test, validate_pins,
)


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate5.round67.direct-positive-potential-attenuation-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-gate5-round67-direct-positive-potential-attenuation-frontier"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
SIDECAR = HERE / f"{PREFIX}-manifest-2026-07-21.sha256"
REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
CERT = HERE / "cm2_gate5_round67_direct_positive_potential_attenuation_frontier_cert.py"
VERIFIER = Path(__file__).resolve()
COMMON = HERE / "cm2_round67_common.py"
EXPECTED_PINS_DIGEST = "e8df79c0f805558e3efa5d01e9579e33552c127f24542ec8843abce5448546e7"
EXPECTED_RESULT_DIGEST = "b4db01da995d0586b7e41288bcce90dd8493437adc3e26569d5507518f8e86dd"


def integrity(data: dict[str, Any], files: bool = True) -> None:
    require(data.get("schema") == MANIFEST_SCHEMA, "manifest schema")
    pins = data.get("pins")
    require(isinstance(pins, dict) and len(pins) == 32, "pin root/count")
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
            provenance["terminal_nesting_reused_as_contraction"] is False and
            digest(provenance["pinned_round66_owner_sector_flux_chain"])
            == EXPECTED_PINS_DIGEST, "provenance")

    direct = result["maximal_direct_potential"]
    require(direct["status"] == "CERTIFIED_EXACT" and
            direct["operator_criterion"] ==
            "A:L1(mu)->positive typed direct sum bounded iff H in Linfinity(mu)" and
            direct["operator_norm"] == "||A||=||H||_infinity" and
            direct["recordwise_G_Linfinity"] == "SUFFICIENT_NOT_NECESSARY" and
            direct["finite_actual_average"] == "INSUFFICIENT_FOR_STRONG_OPERATOR" and
            direct["signed_cancellation_pays_positive_norm"] is False and
            direct["time_coordinate_retained"] is True, "direct potential")
    require("sum_j w_Z^j" in direct["record_potential"] and
            "integral G(r)Q_x" in direct["conditional_potential"] and
            "superlevel" in direct["proof_mechanism"], "direct formulas")

    terminal = result["terminal_moment_identity"]
    require(terminal["status"] == "CERTIFIED_EXACT" and
            terminal["record_formula"] == "G_live=(w_Z^N-1)/(w_Z-1)" and
            terminal["conditional_formula"] == "H_live=(E_x[w_Z^N]-1)/(w_Z-1)" and
            terminal["exact_strong_condition"] ==
            "ess_sup_x E_x[w_Z^N]<infinity" and
            terminal["actual_terminal_exponential_moment"] == "NOT_CERTIFIED" and
            terminal["round39_clearance_rank_tail_is_terminal_depth_tail"] is False,
            "terminal identity")
    geom = terminal["geometric_model"]
    require((Q(geom["w_Z"]), Q(geom["tail_parameter_r"]), Q(geom["w_Z_r"])) ==
            (Q(3, 2), Q(1, 3), Q(1, 2)) and
            Q(geom["E_w_to_N"]) == 2 and Q(geom["H_live"]) == 2 and
            geom["survivor_full_label_RN_density"] == "1" and
            geom["direct_attenuation_succeeds"] is True and
            len(geom["rows"]) == 12, "geometric model")
    for row in geom["rows"]:
        j = row["j"]
        require(Q(row["conditional_survival"]) == Q(1, 3) ** j and
                Q(row["weighted_live_term"]) == Q(1, 2) ** j and
                row["survivor_full_label_density"] == "1", "geometric row")

    attenuation = result["lawful_attenuation"]
    sub = attenuation["sub_Markov"]
    require(sub["exact_potential"] == "sum_j w_Z^j P_(0:j)W_j" and
            sub["geometric_threshold"] == "w_Z*kappa<1" and
            sub["average_mass_decay_suffices"] is False and
            sub["actual_pointwise_charged_survival"] == "NOT_CERTIFIED",
            "sub-Markov")
    doob = attenuation["Doob_Lyapunov"]
    require(doob["source_requirement_for_unweighted_L1"] == "V_0 in Linfinity(mu)" and
            doob["integral_V_0_only_suffices"] is False and
            doob["minimal_resolvent"] == "H=W+w_Z P H" and
            doob["actual_bounded_supersolution"] == "NOT_CERTIFIED", "Doob")

    departure = result["one_shot_departure"]
    require(departure["status"] == "CERTIFIED_EXACT_WEIGHTED_TELESCOPE" and
            departure["limit_identity"] == "H_departure=x_0+(w_Z-1)H_live" and
            departure["requires_weighted_live_finite"] is True and
            departure["pays_owner_birth"] is False and
            departure["pays_pre_regularization_cemetery"] is False and
            departure["absorbing_occupancy_if_nonzero"] == "DIVERGES_FOR_w_Z_GT_1",
            "departure")
    separator = departure["harmonic_separator"]
    require(separator["x_j"] == "w_Z^(-j)/(j+1)" and
            separator["unweighted_departures_telescope"] is True and
            separator["weighted_live"] == "DIVERGES_HARMONIC" and
            separator["weighted_arrivals"] == "DIVERGES_HARMONIC" and
            len(separator["rows"]) == 12, "telescope separator")
    w = Q(3, 2)
    for row in separator["rows"]:
        j = row["j"]
        xj = (Q(2, 3) ** j) / (j + 1)
        xn = (Q(2, 3) ** (j + 1)) / (j + 2)
        require(Q(row["x_j"]) == xj and Q(row["x_next"]) == xn and
                Q(row["lost"]) == xj - xn and
                Q(row["weighted_live_term"]) == Q(1, j + 1) and
                Q(row["weighted_arrival_term"]) == w / (j + 1) - Q(1, j + 2),
                "telescope row")

    sectors = result["seven_sector_potential"]
    names = ["active-clock", "raw-Z", "power-Orlicz", "complement",
             "variation", "common-mode", "one-shot-cemetery"]
    require(sectors["status"] == "CERTIFIED_EXACT_TYPED" and
            sectors["sectors"] == names and
            sectors["finite_sector_equivalence"] ==
            "H_total in Linfinity iff every H_s in Linfinity" and
            sectors["base_survival_pays_unbounded_marks"] is False and
            sectors["actual_H_total"] == "NOT_EVALUABLE_OR_CERTIFIED" and
            len(sectors["actual_rows"]) == 7, "sectors")
    require([row["sector"] for row in sectors["actual_rows"]] == names, "sector rows")
    require([row["actual_fixed_j"] for row in sectors["actual_rows"]] == [
        "NOT_CERTIFIED_FINITE", "NOT_CERTIFIED_FINITE", "NOT_CERTIFIED_FINITE",
        "FINITE_COST_LAW", "FINITE_COST_LAW", "FINITE_COST_LAW",
        "PRE_REG_NOT_MATERIALIZED",
    ], "sector fixed-j statuses")
    require(all(row["actual_all_time_Linfinity"] == "NOT_CERTIFIED"
                for row in sectors["actual_rows"]), "sector all-time statuses")

    strong = result["strong_separator"]
    require(strong["status"] == "CERTIFIED_EXACT" and
            strong["mu"] == "mu{n}=3*4^(-n)" and Q(strong["w_Z"]) == Q(3, 2) and
            strong["survival"] == "P_(0:j)=3^(-j)Id" and
            strong["tag"] == "W_j(n)=2^n" and Q(strong["w_Z_kappa"]) == Q(1, 2) and
            Q(strong["one_time_actual_moment"]) == 3 and
            Q(strong["all_time_actual_moment"]) == 6 and
            strong["conditional_potential"] == "H(n)=2^(n+1)" and
            strong["H_in_Linfinity"] is False and len(strong["rows"]) == 12,
            "strong separator")
    for row in strong["rows"]:
        n = row["n"]
        require(Q(row["mu_atom"]) == Q(3, 4 ** n) and
                int(row["tag_charge"]) == 2 ** n and
                Q(row["one_time_integrand"]) == Q(3, 2 ** n) and
                int(row["conditional_potential"]) == 2 ** (n + 1),
                "strong row")

    oriented = result["oriented_positive_pair"]
    require(oriented["upstream_exact_mass_row"] == "xi_j^f(X)=m_p=xi_j^r(X)" and
            oriented["two_orientation_RN_rows"] == "NOT_CERTIFIED" and
            oriented["common_mode_equality"] == "NOT_CERTIFIED" and
            oriented["physical_immutable_carrier"] == "NOT_CERTIFIED" and
            oriented["positive_lower_bound_m_p"] == "NOT_CERTIFIED" and
            oriented["separate_upper_bounds_prove_exact_mass_row"] is False and
            oriented["signed_law_alone_pays_common_mode"] is False and
            oriented["physical_potentials_materialized"] is False, "oriented")
    require(oriented["positive_pair_decomposition"] ==
            "mu^+=J^++lambda; mu^-=J^-+lambda" and
            oriented["positive_sum"] == "mu^++mu^-=|J|+2lambda", "Jordan")

    actual = result["actual_frozen_status"]
    require(actual == {
        "fixed_j_base_owner_law": "FINITE",
        "fixed_j_complement_variation_common_cost": "FINITE",
        "active_clock_raw_Z_power_Orlicz_slice": "NOT_CERTIFIED_FINITE",
        "pre_regularization_cemetery_arrival": "NOT_MATERIALIZED",
        "conditional_terminal_or_charged_survivor_tail": "NOT_CERTIFIED",
        "graph_supported_common_physical_root_kernel": "NOT_CERTIFIED",
        "direct_H_total_Linfinity": "NOT_CERTIFIED",
    }, "actual status")

    fields = result["remaining_eight_fields"]
    require(fields["required_field_count"] == 18 and fields["certified_maturity"] == 10 and
            fields["open_count"] == 8 and fields["new_field_promoted"] is False and
            [row["field"] for row in fields["rows"]] ==
            ["F5", "F6", "F10", "F11", "F14", "F15", "F17", "F18"] and
            all(row["status"] == "OPEN" for row in fields["rows"]), "fields")

    tech = result["technology_boundary"]
    require(tech["dominated_kernel_and_Feynman_Kac_results_assume_physical_kernel_and_drift"] is True and
            tech["different_process_or_source_norm_imported"] is False and
            tech["external_theorem_promoted"] is False, "technology")
    require(result["strict_status"] == {
        "Gate5": "NOT_CERTIFIED",
        "Gate5_maturity": "10/18",
        "complete_18_field_blocks": 0,
        "complete_composite_gates": "0/5",
        "CM2": "NO-GO_FOR_CLAIM",
    }, "strict status")


def independent_replay() -> dict[str, Any]:
    w, r = Q(3, 2), Q(1, 3)
    require(w * r == Q(1, 2), "geometric threshold")
    expected_wN = w * (1 - r) / (1 - w * r)
    h_live = (expected_wN - 1) / (w - 1)
    require(expected_wN == 2 and h_live == 2, "terminal moment identity")

    count = 12
    xs = [(Q(2, 3) ** j) / (j + 1) for j in range(count + 1)]
    arrivals = sum((w ** (j + 1)) * (xs[j] - xs[j + 1]) for j in range(count))
    live_inner = sum((w ** j) * xs[j] for j in range(1, count))
    rhs = w * xs[0] + (w - 1) * live_inner - (w ** count) * xs[count]
    require(arrivals == rhs, "finite weighted telescope")

    one_time = sum(Q(3, 2 ** n) for n in range(1, 80))
    require(one_time < 3 and Q(3) - one_time == Q(3, 2 ** 79), "strong partial moment")
    require(2 * Q(3) == 6, "all-time actual moment")
    return {
        "geometric_w_r": "1/2",
        "geometric_E_wN": "2",
        "geometric_H_live": "2",
        "finite_telescope_rows": count,
        "one_time_moment_limit": "3",
        "all_time_actual_moment": "6",
        "conditional_potential": "UNBOUNDED",
        "sectors": 7,
        "open_fields": 8,
    }


def deterministic(data: dict[str, Any]) -> None:
    proc = subprocess.run(
        [sys.executable, str(CERT), "--manifest-json", "--verifier", str(VERIFIER)],
        cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        check=False, timeout=240,
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
        print(f"ROUND67_GATE5_VERIFY_ERROR: {exc}", file=sys.stderr)
        return 1
    print("Gate5 maturity: 10/18")
    print("complete blocks: 0")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
