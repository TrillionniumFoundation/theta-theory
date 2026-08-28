#!/usr/bin/env python3
"""Independent verifier for the Round-67 Gate-2/4 frontier leaf."""

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
RESULT_SCHEMA = "cm2.gate24.round67.actual-root-stable-tail-variation-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-gate24-round67-actual-root-stable-tail-variation-frontier"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
SIDECAR = HERE / f"{PREFIX}-manifest-2026-07-21.sha256"
REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
CERT = HERE / "cm2_gate24_round67_actual_root_stable_tail_variation_frontier_cert.py"
VERIFIER = Path(__file__).resolve()
EXPECTED_PIN_COUNT = 32
EXPECTED_PINS_DIGEST = "2c1914b3247018a9de88cb5549b61825a9fcdbe3d91592a94e827100882ef568"
EXPECTED_RESULT_DIGEST = "040670bbda45806b683ea159719f54e701b1012eb051717f4e07452da44dfa3c"


def integrity(data: dict[str, Any], files: bool = True) -> None:
    require(data.get("schema") == MANIFEST_SCHEMA, "manifest schema")
    pins = data.get("pins")
    require(isinstance(pins, dict) and len(pins) == EXPECTED_PIN_COUNT and
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
            provenance["external_theorem_promoted"] is False, "provenance")

    root = result["actual_graph_supported_pre_registry"]
    require(root["status"].startswith("CERTIFIED_LOCAL_ACTUAL_GRAPH_SUPPORTED"), "root status")
    require(root["root"]["S"] == ["-3/1600", "-1/640"] and
            root["root"]["I_equals_V"] == ["-1/25600", "1/25600"] and
            Q(root["root"]["fixed_parameter_mass_strict_lower"]) == Q(27, 4096000000) and
            Q(root["root"]["parameter_averaged_mass_strict_lower"]) == Q(27, 65536000000),
            "root replay")
    chart = root["affine_chart"]
    require(chart["D_t_p_over_u_v"] == [["1", "1"], ["3/2", "-3/2"]] and
            chart["determinant"] == "-3" and
            chart["squared_singular_values"] == ["2", "9/2"] and
            chart["metric_factor_strict_upper"] == "101/100", "chart values")
    guards = root["scope_guards"]
    require(all(value is False for value in guards.values()) and
            root["C1_upgrade"]["actual_epsilon_bound"] == "NOT_CERTIFIED",
            "root guards")

    anchors = result["distinct_physical_anchor_audit"]
    require(anchors["Round25_root"]["exact_collision_disintegration"] is True and
            anchors["Round25_root"]["actual_invariant_stable_plaque_family"] is False and
            anchors["Round15_59_root"]["actual_stable_plaque_crossing"] is True and
            anchors["Round15_59_root"]["stable_saturation"] is False and
            anchors["same_immutable_root_crosswalk"] == "NOT_CERTIFIED" and
            anchors["may_combine_exact_density_with_96_word_stable_crossing"] is False,
            "distinct anchors")

    hazard = result["all_depth_conditional_hazard"]
    require(hazard["status"] ==
            "CERTIFIED_EXACT_CONDITIONAL_HAZARD_IFF_AND_SHARP_ZERO_ACTUAL_BOUND",
            "hazard status")
    require(hazard["actual_collision_component_zero_rows"] == 96 and
            hazard["actual_full_conditional_hazard_rows"] == 0 and
            hazard["sharp_actual_survivor_lower_bound"] == "0" and
            hazard["physical_positive_all_depth_survivor"] == "NOT_CERTIFIED",
            "actual hazard guard")
    require(hazard["summable_replay"]["limit"] == "1/2" and
            hazard["summable_replay"]["rows"][-1] == {"N": 256, "product": "129/257"} and
            hazard["divergent_replay"]["rows"][-1] == {"N": 256, "product": "1/257"},
            "hazard replay")

    marker = result["marker_saturation_and_budget"]
    require(marker["stable_saturation"]["pre_registry_carries_actual_g_B"] is False and
            marker["stable_saturation"]["actual_P_eta_zero"] == "NOT_CERTIFIED" and
            marker["candidate_budget"]["physical_budget_paid"] is False and
            marker["zero_defect_implies_BV"] is False, "marker guards")

    strong = result["fixed_material_weighted_BV_recipient"]
    require(strong["boundedness_iff"] == "M_q:BV(I)->Y bounded iff S_q<infinity" and
            strong["moving_family"]["operator_norm_differentiability_iff"] ==
            "sum_r a_r||R_r(s)||_BV=o(|s|)", "strong iff")
    replay = strong["moving_family"]["replay"]
    require(Q(replay["S_q"]) == Q(9, 2) and replay["operator_norm_bounds"] == ["9/2", "9"] and
            replay["quadratic_remainder_rows"][-1]["weighted_BV_remainder_over_abs_s"] == "9/512",
            "strong replay")
    require(strong["same_root_as_Round25_pre_registry"] is False and
            strong["actual_global_weighted_BV_coefficient_sum"] == "NOT_CERTIFIED" and
            strong["actual_all_depth_strong_Piola_recipient"] == "NOT_CERTIFIED",
            "strong guards")

    actual = result["actual_product_tree_interface"]
    require(actual["actual_rows_complete"] == "0/7" and
            actual["partial_rows"] == [2, 4, 7] and len(actual["rows"]) == 7 and
            [row["row"] for row in actual["rows"]] == list(range(1, 8)),
            "actual interface")

    tech = result["latest_technology_boundary"]
    require(tech["external_theorem_promoted"] is False and
            tech["wrong_law_promoted"] is False and
            "sequential" in tech["arXiv_2502_07765v2"] and
            "wrong law" in tech["arXiv_2604_25881v1"], "technology")

    require(result["strict_status"] == {
        "Gate2": "NOT_CERTIFIED__OFFICIAL_FIELDS_0_OF_17",
        "Gate4": "NOT_CERTIFIED__LANDING_JOIN_1_OF_7_FIELDS_1_4_7_PARTIAL",
        "actual_stable_tree_instantiation": "0/7",
        "complete_composite_gates": "0/5",
        "CM2": "NO-GO_FOR_CLAIM",
    }, "strict status")


def independent_replay() -> dict[str, Any]:
    # Exact affine root geometry.
    a = [[Q(1), Q(1)], [Q(3, 2), Q(-3, 2)]]
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    diag = a[0][0] ** 2 + a[1][0] ** 2
    off = a[0][0] * a[0][1] + a[1][0] * a[1][1]
    require(det == -3 and [diag + off, diag - off] == [Q(2), Q(9, 2)],
            "independent chart")

    radius = Q(9, 25)
    t_lo, t_hi = Q(8957, 12800), Q(8959, 12800)
    lo = radius**2 / (1 - t_lo**2) + Q(9, 4)
    hi = radius**2 / (1 - t_hi**2) + Q(9, 4)
    require((hi / lo) ** 3 < Q(101, 100) ** 2, "independent path factor")

    # Conditional hazards, independently multiplied through 512.
    p1 = Q(1)
    p2 = Q(1)
    for n in range(1, 513):
        p1 *= 1 - Q(1, (n + 1) ** 2)
        p2 *= 1 - Q(1, n + 1)
    require(p1 == Q(257, 513) and p2 == Q(1, 513), "independent hazards")

    # Weighted BV multiplier ledger on [0,1].
    s_q = Q(3, 2) + 2 * Q(3, 2)
    require(s_q == Q(9, 2) and 2 * s_q == 9, "independent BV ledger")
    return {
        "graph_root_det": "-3",
        "squared_singular_values": ["2", "9/2"],
        "candidate_metric_factor": "PASS_LT_101_OVER_100",
        "summable_hazard_product_N512": "257/513",
        "divergent_hazard_product_N512": "1/513",
        "weighted_BV_S_q": "9/2",
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
        print(f"ROUND67_GATE24_VERIFY_ERROR: {exc}", file=sys.stderr)
        return 1
    print("Gate2/Gate4: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
