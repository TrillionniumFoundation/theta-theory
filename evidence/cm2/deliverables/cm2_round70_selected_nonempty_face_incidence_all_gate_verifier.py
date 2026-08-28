#!/usr/bin/env python3
"""Independent verifier for the Round-70 selected nonempty face incidence."""

from __future__ import annotations

import argparse
import copy
import json
import subprocess
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round68_common import (
    CertError, digest, require, semantic_mutation_test, sha256_path,
    strict_json_path, strict_json_self_test, validate_pins,
)
from cm2_round70_selected_nonempty_face_incidence_all_gate_cert import (
    COMMON, MANIFEST_SCHEMA, PINS, RESULT_SCHEMA, SELECTED_COMPONENT, build_result,
)


HERE = Path(__file__).resolve().parent
PREFIX = "cm2-round70-selected-nonempty-face-incidence-all-gate"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
CERT = HERE / "cm2_round70_selected_nonempty_face_incidence_all_gate_cert.py"
VERIFIER = Path(__file__).resolve()


def integrity(data: dict[str, Any], check_files: bool = True) -> None:
    require(data["schema"] == MANIFEST_SCHEMA, "manifest schema")
    require(data["result"]["schema"] == RESULT_SCHEMA, "result schema")
    require(data["pins"] == PINS, "manifest pins")
    if check_files:
        validate_pins(HERE, PINS)
        require(data["report_sha256"] == sha256_path(REPORT), "report hash")
        require(data["certificate_sha256"] == sha256_path(CERT), "certificate hash")
        require(data["verifier_sha256"] == sha256_path(VERIFIER), "verifier hash")
        require(data["common_sha256"] == sha256_path(COMMON), "common hash")
    replay = copy.deepcopy(data["result"])
    claimed = replay.pop("internal_replay_digest")
    require(claimed == digest(replay), "internal result digest")
    require(data["verdict"] == data["result"]["strict_status"], "verdict")


def semantics(result: dict[str, Any]) -> None:
    require(result == build_result(), "canonical producer result")
    cell = result["selected_actual_path_cell"]
    require(cell["status"] == "CERTIFIED_POSITIVE_CONNECTED_PHYSICAL_COMPONENT", "cell status")
    require(cell["component_id"] == SELECTED_COMPONENT, "component ID")
    require(cell["path_cell_id"] == "path-cell:" + SELECTED_COMPONENT, "path cell ID")
    require(cell["physical_key"] == ["G:E", "W[0,0]", [], 1], "physical key")
    require(cell["return_depth"] == 1 and cell["component_predicate"] ==
            "abs(p0)<3/10 AND abs(p1)<3/10", "cell scope")

    germ = result["compact_parameterized_face_germ"]
    require(germ["status"] ==
            "CERTIFIED_TWO_NONEMPTY_CONNECTED_ANALYTIC_PHYSICAL_FACE_COMPONENTS",
            "germ status")
    require(germ["t_interval"] == ["13/20", "2/3"] and
            germ["s_interval"] == ["-1/10000", "1/10000"], "germ box")
    require(germ["source_p_bracket"] == ["-3/10", "3/10"] and
            germ["target_transverse_thresholds"] == ["-6/125", "6/125"],
            "germ p thresholds")
    require(Q(germ["lower_p_side_T_strict_lower"]) == Q(2759, 40000) > Q(6, 125),
            "positive side")
    require(Q(germ["upper_p_s0_T_strict_upper"]) == -Q(193, 4000), "base negative side")
    require(Q(germ["parameter_variation_strict_upper"]) == Q(29, 300000),
            "parameter variation")
    require(Q(germ["upper_p_full_germ_T_strict_upper"]) == -Q(7223, 150000) < -Q(6, 125),
            "full negative side")
    require(Q(germ["upper_p_negative_threshold_margin"]) == Q(23, 150000),
            "negative margin")
    require(Q(germ["partial_p_T_strict_upper"]) == -Q(13277, 76000) and
            Q(germ["partial_t_T_strict_upper"]) == -Q(11, 64), "monotone derivatives")
    require(germ["unique_graph_for_each_threshold"] is True and
            germ["graphs_connected_over_t_s_rectangle"] is True and
            germ["closures_stay_in_one_regular_branch"] is True, "graph conclusions")
    require(germ["materialized_face_component_count"] == 2 and
            germ["materialized_trace_count"] == 4, "materialized counts")

    rows = germ["face_rows"]
    require(len(rows) == 2, "face rows")
    require({row["target_p1"] for row in rows} == {"+3/10", "-3/10"}, "target faces")
    require(len({row["face_id"] for row in rows}) == 2, "unique faces")
    require(all(row["restriction_id"] == germ["restriction_id"] for row in rows),
            "restriction incidence")
    trace_ids: set[str] = set()
    for row in rows:
        require(row["path_component_id"] == SELECTED_COMPONENT and row["return_depth"] == 1 and
                row["time_j"] == 1 and row["connected_rank"] == 0, "typed face key")
        require(row["physical_face_kind"] ==
                "terminal_target_momentum_homogeneity_preimage_face", "face type")
        require(row["incidence_edge"] == {
            "source_node": row["face_id"],
            "target_node": "path-cell:" + SELECTED_COMPONENT,
            "relation": "PHYSICAL_FACE_IS_INCIDENT_TO_SELECTED_PATH_COMPONENT_BOUNDARY",
        }, "incidence edge")
        require({trace["side_label"] for trace in row["trace_rows"]} == {"inside", "outside"},
                "two traces")
        trace_ids.update(trace["trace_id"] for trace in row["trace_rows"])
        require(Q(row["F8_transversality_lower"]) == Q(13277, 76000), "F8 row")
        require(row["F9_graph_C2_upper"] == "3000" and
                row["F10_explicit_integer_upper"] == 6031, "F9 F10 row")
        require(Q(row["F13_current_variation_strict_upper"]) == Q(1, 5) and
                Q(row["F13_each_one_sided_trace_mass_strict_upper"]) == Q(19, 60),
                "F13 row")
    require(len(trace_ids) == 4, "unique trace IDs")

    ledger = result["explicit_local_field_ledger"]
    require(ledger["status"] == "CERTIFIED_ACTUAL_INSTANCE_F8_F9_F10_F13_ON_TWO_FACES",
            "field status")
    require(Q(ledger["F8_transversality_lower"]) == Q(13277, 76000), "F8")
    require(ledger["F9_graph_C2_upper"] == "3000", "F9")
    require(Q(ledger["F10_C1_sum_strict_upper"]) == Q(18092, 3) and
            ledger["F10_explicit_integer_upper"] == 6031, "F10")
    require(Q(ledger["per_face_F13_current_variation_strict_upper"]) == Q(1, 5) and
            Q(ledger["two_face_current_variation_strict_upper"]) == Q(2, 5), "current mass")
    require(Q(ledger["per_one_sided_trace_mass_strict_upper"]) == Q(19, 60) and
            Q(ledger["four_trace_mass_strict_upper"]) == Q(19, 15), "trace mass")

    impact = result["gate_impact"]
    require(impact["arbitrary_Rn_nonempty_face_rows_before"] == 0 and
            impact["arbitrary_Rn_nonempty_face_rows_after"] == 2, "face impact")
    require(impact["materialized_N_F10_values_before"] == 0 and
            impact["materialized_N_F10_upper_bounds_after"] == 2, "F10 impact")
    status = result["strict_status"]
    require(status["complete_composite_gates"] == "0/5" and
            status["CM2"] == "NO-GO_FOR_CLAIM", "strict verdict")


def independent_replay() -> dict[str, str]:
    threshold = Q(6, 125)
    lower = Q(2759, 40000)
    require(lower - threshold == Q(839, 40000) > 0, "independent positive margin")

    radical_upper = Q(145, 400) - Q(13, 400) * Q(19, 2) - Q(3, 400) * 15 + Q(21, 2000)
    require(21021 < 145**2 and Q(19, 2) ** 2 < 91 and 15**2 < 231,
            "independent radical separators")
    require(radical_upper == -Q(193, 4000), "independent base upper")
    full_upper = radical_upper + Q(29, 300000)
    require(full_upper == -Q(7223, 150000) and -threshold - full_upper == Q(23, 150000),
            "independent full upper")
    require(Q(13277, 76000) > Q(1, 6), "independent transversality")

    p_t, p_s = 18, 12
    p_tt = 6 * (3 + 2 * 3 * p_t + p_t**2)
    p_ts = 6 * (2 + 3 * p_s + 2 * p_t + p_t * p_s)
    p_ss = 6 * (2 * 2 * p_s + p_s**2)
    require((p_tt, p_ts, p_ss) == (2610, 1740, 1152), "independent graph C2")
    f10 = Q(12) + Q(25, 9) * 1752 + 1152
    require(f10 == Q(18092, 3) < 6031, "independent F10")
    require(Q(2, 3) - Q(13, 20) == Q(1, 60), "independent interval")
    require(18**2 + 1 < 19**2, "independent trace length")

    restriction_key = {
        "component_id": SELECTED_COMPONENT,
        "t_interval": ["13/20", "2/3"],
        "s_interval": ["-1/10000", "1/10000"],
        "physical_word": ["G:E", "W[0,0]"],
    }
    restriction_id = "rn-restriction:" + digest(restriction_key)
    face_ids = []
    trace_ids = []
    for target in ("+3/10", "-3/10"):
        family_id = f"target-momentum-homogeneity-preimage:p1={target}"
        face_id = "face:" + digest({
            "component_id": SELECTED_COMPONENT,
            "time_j": 1,
            "carrier_family_id": family_id,
            "connected_rank": 0,
        })
        face_ids.append(face_id)
        trace_ids.extend("trace:" + digest({"face_id": face_id, "side_label": side})
                         for side in ("inside", "outside"))
    require(len(set(face_ids)) == 2 and len(set(trace_ids)) == 4, "independent IDs")
    require(restriction_id.startswith("rn-restriction:"), "independent restriction")
    return {
        "nonempty_faces": "2/2",
        "time1_incidence_edges": "2/2",
        "one_sided_traces": "4/4",
        "local_fields": "F8_F9_F10_F13",
        "status": "PASS",
    }


def deterministic(data: dict[str, Any]) -> None:
    proc = subprocess.run(
        [sys.executable, str(CERT), "--manifest-json", "--verifier", str(VERIFIER)],
        cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=300,
    )
    require(proc.returncode == 0, f"producer: {proc.stderr.decode().strip()}")
    require(proc.stdout == MANIFEST.read_bytes() and strict_json_path(MANIFEST) == data,
            "deterministic producer")


def run_audit(data: dict[str, Any], regenerate: bool = True) -> None:
    integrity(data)
    semantics(data["result"])
    independent_replay()
    require(data["result"] == build_result(), "canonical producer result")
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
                cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=300,
            )
            require(proc.returncode == 0, "reemit producer")
            args.reemit.write_bytes(proc.stdout)
            require(args.reemit.read_bytes() == MANIFEST.read_bytes(), "reemit bytes")
            return 0
    except (CertError, OSError, ValueError, KeyError, TypeError, ArithmeticError,
            subprocess.SubprocessError) as exc:
        print(f"ROUND70_VERIFY_ERROR: {exc}", file=sys.stderr)
        return 1
    print("ROUND70 SELECTED NONEMPTY FACE INCIDENCE: PARTIAL_ONLY")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
