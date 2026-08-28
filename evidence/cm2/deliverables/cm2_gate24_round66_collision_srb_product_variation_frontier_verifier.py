#!/usr/bin/env python3
"""Independent verifier for the Round-66 Gate-2/4 frontier leaf."""

from __future__ import annotations

import argparse
import copy
import json
import subprocess
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round66_common import (
    CertError, digest, replay_sidecar, require, semantic_mutation_test,
    sha256_path, strict_json_path, strict_json_self_test, validate_pins,
)


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate24.round66.collision-srb-product-variation-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-gate24-round66-collision-srb-product-variation-frontier"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
SIDECAR = HERE / f"{PREFIX}-manifest-2026-07-21.sha256"
REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
CERT = HERE / "cm2_gate24_round66_collision_srb_product_variation_frontier_cert.py"
VERIFIER = Path(__file__).resolve()
EXPECTED_PINS_DIGEST = "4689954689d675c51ed060000313e506c083c5ae7ea1d167fe828d792b45e1ff"
EXPECTED_RESULT_DIGEST = "0f1358c6ef6b4b56ccc15663a369a667f18072d6be0e601c7f9fffc133ba86aa"


def integrity(data: dict[str, Any], files: bool = True) -> None:
    require(data.get("schema") == MANIFEST_SCHEMA, "manifest schema")
    pins = data.get("pins")
    require(isinstance(pins, dict) and len(pins) == 54 and
            digest(pins) == EXPECTED_PINS_DIGEST, "pinned dependency set")
    if files:
        validate_pins(HERE, pins)
        require(data.get("report_sha256") == sha256_path(REPORT), "report hash")
        require(data.get("certificate_sha256") == sha256_path(CERT), "certificate hash")
        require(data.get("verifier_sha256") == sha256_path(VERIFIER), "verifier hash")
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
            provenance["external_theorem_promoted"] is False,
            "provenance guards")

    chart = result["sinai_density_product_chart"]
    require(chart["status"] ==
            "CERTIFIED_EXACT_CONDITIONAL_DENSITY_RN_ARCLENGTH_CROSSWALK__ACTUAL_CHART_ABSENT",
            "chart status")
    require("cos(phi)" in chart["physical_invariant_density"] and
            chart["conditional_arclength_density"] == "rho_s=q/(Z(s)*a)",
            "Sinai/chart formula")
    rep = chart["rational_replay"]
    require(Q(rep["rho_s"]) == 1 and Q(rep["rho_t"]) == Q(2, 3) and
            Q(rep["lambda_st"]) == Q(3, 2) and Q(rep["J_st"]) == 1,
            "chart replay")
    require(rep["rho_envelope"] == ["4/9", "3/2"] and
            rep["J_envelope"] == ["4/9", "9/4"] and
            rep["metric_path_factor"] == "27/8", "chart envelope")
    require(chart["round25_affine_chart_is_physical_stable_chart"] is False and
            chart["actual_product_chart_common_root_density_bounds"] == "NOT_CERTIFIED",
            "actual chart guards")

    cross = result["owner_landing_joint_crosswalk"]
    require(cross["status"] ==
            "CERTIFIED_EXACT_CROSSWALK_REQUIREMENT_AND_MARGINAL_NONIMPLICATION",
            "crosswalk status")
    sep = cross["same_marginals_do_not_determine_key_support"]
    require(sep["compatible_mass_align"] == "1" and
            sep["compatible_mass_switch"] == "0" and
            sep["status"] == "FALSE_BY_EXACT_TWO_COUPLING_SEPARATOR",
            "crosswalk separator")
    require(cross["actual_owner_landing_product_crosswalk"] == "NOT_CERTIFIED",
            "actual crosswalk guard")

    marker = result["stable_marker_saturation"]
    require(marker["status"] == "FALSE_BY_SMOOTH_POSITIVE_SAME_MASS_MARKER_SEPARATOR",
            "marker status")
    require(marker["same_total_landing_mass"] == "1/2" and
            marker["stable_completion"]["P_eta"] == "0" and
            Q(marker["varying_completion"]["P_eta"]) == Q(5, 64) and
            Q(marker["varying_completion"]["delta_eta"]) == Q(1, 8) and
            marker["varying_completion"]["strict_sandwich"] is True,
            "marker replay")
    require(marker["actual_P_eta_zero"] == "NOT_CERTIFIED", "actual marker guard")

    failure = result["all_depth_first_failure"]
    require(failure["status"] ==
            "CERTIFIED_ZERO_ACTUAL_LOWER_BOUND_AND_SHORTEST_GEOMETRIC_FAILURE_INTERFACE",
            "failure status")
    require(failure["frozen_collision_shadow_rows"] == 96 and
            failure["actual_full_first_failure_upper_bound_rows"] == 0 and
            failure["frozen_graph_transform_chart_survival"] == "NOT_CERTIFIED" and
            failure["sharp_actual_survivor_lower_bound"] == "0",
            "actual failure audit")
    geo = failure["geometric_future_interface"]
    require(Q(geo["sample_A"]) == Q(1, 4) and Q(geo["sample_sigma"]) == Q(1, 2) and
            Q(geo["sample_total_failure_upper"]) == Q(1, 4) and
            Q(geo["sample_survivor_lower"]) == Q(3, 4), "failure replay")
    require(failure["physical_positive_all_depth_survivor"] == "NOT_CERTIFIED",
            "physical survivor guard")

    variation = result["weighted_variation_and_strong_recipient"]
    require(variation["status"] ==
            "CERTIFIED_VARIATION_SEPARATOR_AND_CONDITIONAL_MATERIAL_BRIDGE__PHYSICAL_RECIPIENT_ABSENT",
            "variation status")
    rows = variation["zero_defect_unbounded_variation_separator"]["rows"]
    require(all(row["P_eta"] == "0" and
                int(row["transverse_variation"]) == row["N"] for row in rows),
            "variation separator")
    bridge = variation["material_tag_Piola_BV_bridge"]
    sample = bridge["sample"]
    require(bridge["status"] ==
            "CERTIFIED_CONDITIONAL_FIXED_MATERIAL_BV_MULTIPLIER_BRIDGE" and
            Q(sample["B_0"]) == 2 and Q(sample["B_inf"]) == 3 and
            Q(sample["B_1"]) == 3 and Q(sample["output_tagged_BV"]) == Q(37, 6) and
            Q(sample["upper_bound"]) == 20, "material BV replay")
    require(variation["actual_weighted_transverse_variation"] == "NOT_CERTIFIED" and
            variation["actual_physical_Piola_coefficients_and_remainder"] == "NOT_CERTIFIED" and
            variation["physical_anisotropic_intertwining_recipient"] == "NOT_CERTIFIED",
            "physical strong guards")

    actual = result["actual_product_tree_interface"]
    require(actual["status"] == "AUDITED_0_OF_7__NO_PRODUCT_TREE_PROMOTION" and
            actual["actual_rows_complete"] == "0/7" and len(actual["rows"]) == 7 and
            [row["row"] for row in actual["rows"]] == list(range(1, 8)) and
            actual["formula_rows_are_not_actual_materializations"] is True,
            "actual interface")

    tech = result["latest_technology_boundary"]
    require(tech["external_theorem_promoted"] is False and
            tech["wrong_law_or_smooth_flow_promoted"] is False and
            "MME" in tech["arXiv_2604_25881v1"] and
            tech["fresh_official_API_query"] == "RATE_EXCEEDED__NO_RESULT_PROMOTED",
            "technology guards")

    require(result["strict_status"] == {
        "Gate2": "NOT_CERTIFIED__OFFICIAL_FIELDS_0_OF_17",
        "Gate4": "NOT_CERTIFIED__LANDING_JOIN_1_OF_7_FIELDS_1_4_7_PARTIAL",
        "actual_stable_tree_instantiation": "0/7",
        "complete_composite_gates": "0/5",
        "CM2": "NO-GO_FOR_CLAIM",
    }, "strict state")


def independent_replay() -> dict[str, Any]:
    # Nontrivial flat-density product-chart sample.
    a_s, a_t = Q(1), Q(3, 2)
    q_s, q_t, z_s, z_t = a_s, a_t, a_s, a_t
    rho_s = q_s / (z_s * a_s)
    rho_t = q_t / (z_t * a_t)
    lam = a_t / a_s
    jac = q_s * z_t / (q_t * z_s)
    require(jac * rho_t == rho_s / lam == Q(2, 3), "independent chart identity")

    # Same marginals, opposite immutable-key support.
    align = {(0, 0): Q(1, 2), (1, 1): Q(1, 2)}
    switch = {(0, 1): Q(1, 2), (1, 0): Q(1, 2)}
    for axis in (0, 1):
        for key in (0, 1):
            require(sum((m for pair, m in align.items() if pair[axis] == key), Q(0)) ==
                    sum((m for pair, m in switch.items() if pair[axis] == key), Q(0)) == Q(1, 2),
                    "independent crosswalk marginals")
    require(sum((m for (o, s), m in align.items() if o == s), Q(0)) == 1 and
            sum((m for (o, s), m in switch.items() if o == s), Q(0)) == 0,
            "independent key split")

    values = [Q(5, 16), Q(7, 16), Q(9, 16), Q(11, 16)]
    weights = [Q(1, 4)] * 4
    p_eta = sum((weights[i] * weights[j] * abs(values[i] - values[j])
                 for i in range(4) for j in range(i + 1, 4)), Q(0))
    median = values[1]
    delta = sum((w * abs(v - median) for w, v in zip(weights, values)), Q(0))
    require(p_eta == Q(5, 64) and delta == Q(1, 8), "independent marker")

    a, sigma = Q(1, 4), Q(1, 2)
    tail80 = sum((a * sigma**k for k in range(1, 81)), Q(0))
    require(Q(1, 4) - tail80 == Q(1, 2**82), "independent failure tail")

    b0, binf, b1, f_bv, output = Q(2), Q(3), Q(3), Q(5, 2), Q(37, 6)
    require(output <= (b0 + binf + b1) * f_bv == 20, "independent BV bound")
    return {
        "chart_RN_arclength": "PASS",
        "crosswalk_two_couplings": "PASS",
        "P_eta": "5/64",
        "delta_eta": "1/8",
        "failure_survivor_lower": "3/4",
        "material_BV": "PASS",
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
        replay_sidecar(HERE, SIDECAR, 4)
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
            rejected = semantic_mutation_test(data, integrity, semantics)
            strict = strict_json_self_test()
            print(f"HOSTILE_SEMANTIC_REJECTED: {rejected}/{rejected}")
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
    except (CertError, OSError, ValueError, KeyError, TypeError, IndexError,
            ArithmeticError, subprocess.SubprocessError) as exc:
        print(f"ROUND66_GATE24_VERIFY_ERROR: {exc}", file=sys.stderr)
        return 1
    print("Gate2/Gate4: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
