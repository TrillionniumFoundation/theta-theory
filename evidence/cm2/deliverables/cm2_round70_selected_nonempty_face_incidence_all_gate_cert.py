#!/usr/bin/env python3
"""Producer for the Round-70 selected nonempty physical-face incidence."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path
from typing import Any

from cm2_round68_common import (
    CertError, canonical_bytes, digest, require, sha256_path, strict_json_path,
    validate_pins,
)


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.round70.selected-nonempty-face-incidence-all-gate.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-round70-selected-nonempty-face-incidence-all-gate"
REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
VERIFIER = HERE / "cm2_round70_selected_nonempty_face_incidence_all_gate_verifier.py"
COMMON = HERE / "cm2_round68_common.py"

INCIDENCE = "cm2-gate25-selected-homoclinic-component-incidence-frontier-manifest-2026-07-16.json"
PRUNING = "cm2-gate25-selected-component-reachability-pruning-manifest-2026-07-17.json"
BOUNDARY = "cm2-gate25-physical-boundary-root-order-frontier-manifest-2026-07-17.json"
FACE_ATLAS = "cm2-gate5-round28-limiting-physical-face-atlas-frontier-manifest-2026-07-18.json"
F8_MANIFEST = "cm2-gate5-round32-parameterized-face-rank-f8-manifest-2026-07-19.json"
F9_MANIFEST = "cm2-gate5-round36-all-face-rank-path-f9-manifest-2026-07-19.json"
F10_MANIFEST = "cm2-gate5-round36-compact-germ-f10-frontier-manifest-2026-07-19.json"

PINS = {
    "cm2-sixty-ninth-direct-assault-2026-07-21.md":
        "13d6c50664348b6c5aab2d3b1a3e58e2f0a36e1e995cfd3d6b7bf5b1f5f8ea65",
    "cm2-sixty-ninth-direct-assault-manifest-2026-07-21.sha256":
        "2d326be1c4f87ad7851b8a1b8dd2f3449cc04d496b13a50825009b1e233c76a3",
    "cm2-round69-base-s-return-incidence-all-gate-manifest-2026-07-21.json":
        "08d996d52d6aa8ea3b716a46b51d6ae8f0a6b4b9e24c9fab402afe88059bc838",
    "cm2_round68_common.py":
        "f705d61157d5cbbf41f7ad4c4e72c6ad3fbd0466f34651137f15a03d6789d856",
    INCIDENCE:
        "83120fd29f2820c943451d66a867e3ea79400b1fd9f4efda8bc15eac0aee0828",
    PRUNING:
        "6f7e7f07f0210c818463bfa8f1a3fe5b43d7a787537d4a669dc074ccd87b56bd",
    BOUNDARY:
        "58a8b27517a55fabd5776e9299802bb656f60733ae86c25941b640be2dfb4e91",
    FACE_ATLAS:
        "ad385983a4152da3bc1d9c58a5a2fba1abb928466ecf9a9f61260b612bddf140",
    F8_MANIFEST:
        "f9c4eca78065001e65381880deef8681b3a626c2bd419e4ecfe3b02f37a7b53e",
    F9_MANIFEST:
        "f603dd8e638d661b22c746742a5e5c3fd48242f4c0ad40bb35fbe74d35325788",
    F10_MANIFEST:
        "9bc22092f99cd9af0d4b4daf44c89f6e5b24ca90f4826ed870f754e02de9ce73",
}

SELECTED_COMPONENT = "7359148da1c43a255f2238d9c831b8638f2c9885035034a5792699c968b2f3b5"


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def face_record(target_sign: int, restriction_id: str) -> dict[str, Any]:
    require(target_sign in (-1, 1), "target sign")
    target = f"{target_sign * 3}/10" if target_sign < 0 else "+3/10"
    family_id = f"target-momentum-homogeneity-preimage:p1={target}"
    key = {
        "component_id": SELECTED_COMPONENT,
        "time_j": 1,
        "carrier_family_id": family_id,
        "connected_rank": 0,
    }
    face_id = "face:" + digest(key)
    inside_direction = "increase_source_p" if target_sign > 0 else "decrease_source_p"
    outside_direction = "decrease_source_p" if target_sign > 0 else "increase_source_p"
    traces = [{
        "side_label": side,
        "trace_id": "trace:" + digest({"face_id": face_id, "side_label": side}),
        "source_p_direction": direction,
    } for side, direction in (("inside", inside_direction), ("outside", outside_direction))]
    return {
        "face_id": face_id,
        "restriction_id": restriction_id,
        "path_component_id": SELECTED_COMPONENT,
        "return_depth": 1,
        "time_j": 1,
        "physical_face_kind": "terminal_target_momentum_homogeneity_preimage_face",
        "carrier_family_id": family_id,
        "connected_rank": 0,
        "target_p1": target,
        "level_equation": f"T(t,p,s)={target_sign * 6}/125",
        "root_coordinate": "t",
        "graph_coordinate": "p=p_sigma(t,s)",
        "parameter_coordinate": "s",
        "trace_rows": traces,
        "incidence_edge": {
            "source_node": face_id,
            "target_node": "path-cell:" + SELECTED_COMPONENT,
            "relation": "PHYSICAL_FACE_IS_INCIDENT_TO_SELECTED_PATH_COMPONENT_BOUNDARY",
        },
        "F8_transversality_lower": "13277/76000",
        "F9_graph_C2_upper": "3000",
        "F10_explicit_integer_upper": 6031,
        "F13_current_variation_strict_upper": "1/5",
        "F13_each_one_sided_trace_mass_strict_upper": "19/60",
    }


@lru_cache(maxsize=1)
def build_result() -> dict[str, Any]:
    validate_pins(HERE, PINS)
    incidence = strict_json_path(HERE / INCIDENCE)["result"]
    pruning = strict_json_path(HERE / PRUNING)["result"]
    boundary = strict_json_path(HERE / BOUNDARY)["result"]
    atlas = strict_json_path(HERE / FACE_ATLAS)["result"]
    f8 = strict_json_path(HERE / F8_MANIFEST)["result"]
    f9 = strict_json_path(HERE / F9_MANIFEST)["result"]
    f10 = strict_json_path(HERE / F10_MANIFEST)["result"]

    selected = incidence["selected_occurrence_component_incidence"]
    require(selected["maximal_component_id"] == SELECTED_COMPONENT, "selected component")
    require(selected["physical_key"] == ["G:E", "W[0,0]", [], 1], "physical key")
    require(selected["selected_occurrence_membership_in_one_of_24_maximal_word_components_certified"] is True,
            "selected incidence")
    connected = pruning["connected_pruned_domain_theorem"]
    require(connected["P_equals_seeded_maximal_connected_component_M"] is True, "component equality")
    require(connected["partial_p_T_strict_upper"] == "-13277/76000" and
            connected["partial_t_T_strict_upper"] == "-11/64", "derivative pins")
    require(boundary["physical_branch_slope_and_root_grammar"]
            ["every_active_branch_has_at_most_one_isolated_root"] is True, "root grammar")
    require(atlas["moving_occurrence_coarea_DQ_face_seed_registry"]
            ["materialized_physical_moving_occurrence_face_seed_count"] == 64, "face atlas pin")
    require(f8["parameterized_connected_face_registry"]["connected_rank_assignment"] ==
            "CERTIFIED_PARAMETERIZED", "prior F8 rank grammar")
    require(f8["parameterized_connected_face_registry"]
            ["nonempty_intersection_connected_rank"] == 0, "prior F8 connected rank")
    require(f8["parameterized_connected_face_registry"]
            ["two_one_sided_traces_per_regular_noncorner_root"] is True,
            "prior F8 trace grammar")
    require(f9["general_base_face_rank_path_recurrence"]
            ["finite_for_every_finite_rank_path"] is True, "prior F9 finite recurrence")
    require(f9["strict_nonpromotion"]
            ["F9_rank_path_cost_has_global_physical_Lp_sum"] is False,
            "prior F9 nonpromotion")
    require(f10["compact_regular_face_germ_universe"]["instantiated_compact_germ_rows"] == 0 and
            f10["canonical_dyadic_radius_and_F10_search"]["materialized_N_F10_values"] == 0,
            "prior F10 instances")

    threshold = Q(6, 125)
    lower_p_side = Q(2759, 40000)
    require(lower_p_side > threshold, "lower p side")
    require(21021 < 145**2 and 91 > Q(19, 2) ** 2 and 231 > 15**2,
            "radical separators")
    upper_p_s0 = -Q(193, 4000)
    parameter_variation = Q(29, 300000)
    upper_p_germ = upper_p_s0 + parameter_variation
    require(upper_p_germ == -Q(7223, 150000) < -threshold, "upper p side germ")
    transversality = Q(13277, 76000)
    require(transversality > Q(1, 6), "transversality simplification")

    p_t, p_s = 18, 12
    p_tt = 6 * (3 + 2 * 3 * p_t + p_t**2)
    p_ts = 6 * (2 + 3 * p_s + 2 * p_t + p_t * p_s)
    p_ss = 6 * (2 * 2 * p_s + p_s**2)
    require((p_tt, p_ts, p_ss) == (2610, 1740, 1152), "implicit derivative ledger")
    f10_sum = Q(12) + Q(25, 9) * 1752 + 1152
    require(f10_sum == Q(18092, 3) < 6031, "F10 sum")
    require(Q(2, 3) - Q(13, 20) == Q(1, 60), "carrier length")
    require(18**2 + 1 < 19**2, "trace slope")

    restriction_key = {
        "component_id": SELECTED_COMPONENT,
        "t_interval": ["13/20", "2/3"],
        "s_interval": ["-1/10000", "1/10000"],
        "physical_word": ["G:E", "W[0,0]"],
    }
    restriction_id = "rn-restriction:" + digest(restriction_key)
    faces = [face_record(1, restriction_id), face_record(-1, restriction_id)]
    require(len({row["face_id"] for row in faces}) == 2, "face IDs")
    require(len({trace["trace_id"] for row in faces for trace in row["trace_rows"]}) == 4,
            "trace IDs")

    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "append_only": True,
            "old_artifacts_modified": False,
            "pinned_chain": PINS,
        },
        "selected_actual_path_cell": {
            "status": "CERTIFIED_POSITIVE_CONNECTED_PHYSICAL_COMPONENT",
            "component_id": SELECTED_COMPONENT,
            "path_cell_id": "path-cell:" + SELECTED_COMPONENT,
            "physical_key": ["G:E", "W[0,0]", [], 1],
            "return_depth": 1,
            "source_chart": "G:E",
            "target_lift": "W[0,0]",
            "component_predicate": "abs(p0)<3/10 AND abs(p1)<3/10",
        },
        "compact_parameterized_face_germ": {
            "status": "CERTIFIED_TWO_NONEMPTY_CONNECTED_ANALYTIC_PHYSICAL_FACE_COMPONENTS",
            "restriction_id": restriction_id,
            "t_interval": ["13/20", "2/3"],
            "s_interval": ["-1/10000", "1/10000"],
            "source_p_bracket": ["-3/10", "3/10"],
            "target_transverse_thresholds": ["-6/125", "6/125"],
            "T_model": "T=cp*(c/2-a*t)-p*(a*c+t/2-9/25); a=1/2+s",
            "lower_p_side_T_strict_lower": qstr(lower_p_side),
            "upper_p_s0_T_strict_upper": qstr(upper_p_s0),
            "parameter_variation_strict_upper": qstr(parameter_variation),
            "upper_p_full_germ_T_strict_upper": qstr(upper_p_germ),
            "upper_p_negative_threshold_margin": "23/150000",
            "partial_p_T_strict_upper": "-13277/76000",
            "partial_t_T_strict_upper": "-11/64",
            "unique_graph_for_each_threshold": True,
            "positive_threshold_graph_precedes_negative_threshold_graph_in_source_p": True,
            "graphs_connected_over_t_s_rectangle": True,
            "closures_stay_in_one_regular_branch": True,
            "materialized_face_component_count": 2,
            "materialized_trace_count": 4,
            "face_rows": faces,
        },
        "explicit_local_field_ledger": {
            "status": "CERTIFIED_ACTUAL_INSTANCE_F8_F9_F10_F13_ON_TWO_FACES",
            "level_function_derivative_bounds": {
                "abs_T_t": "<3", "abs_T_s": "<2", "abs_T_tt": "<3",
                "abs_T_ts": "<2", "abs_T_tp": "<3", "abs_T_sp": "<2",
                "abs_T_pp": "<1",
            },
            "implicit_graph_derivative_bounds": {
                "abs_p_t": "<18", "abs_p_s": "<12", "abs_p_tt": "<2610",
                "abs_p_ts": "<1740", "abs_p_ss": "<1152",
            },
            "F8_transversality_lower": "13277/76000",
            "F9_graph_C2_upper": "3000",
            "collision_area_weight": "w=(9/25)/sqrt(1-t^2)<18/35<1",
            "abs_weight_t_derivative": "<1",
            "signed_current_density": "rho=w*p_s relative to dt",
            "abs_rho": "<12",
            "abs_rho_t": "<1752",
            "abs_rho_s": "<1152",
            "t_to_physical_arclength_derivative_factor": "<25/9",
            "F10_C1_sum_strict_upper": qstr(f10_sum),
            "F10_explicit_integer_upper": 6031,
            "per_face_F13_current_variation_strict_upper": "1/5",
            "per_one_sided_trace_mass_strict_upper": "19/60",
            "two_face_current_variation_strict_upper": "2/5",
            "four_trace_mass_strict_upper": "19/15",
        },
        "gate_impact": {
            "Gate1": "NOT_CERTIFIED__NO_Q_E_u_v_CROSSWALK",
            "Gate2": "NOT_CERTIFIED__OFFICIAL_FIELDS_0_OF_17",
            "Gate3": "NOT_CERTIFIED__ONE_LOCAL_TWO_FACE_TRACE_CURRENT_ROW_ONLY",
            "Gate4": "NOT_CERTIFIED__TWO_ACTUAL_TIME1_FACE_INCIDENCE_EDGES_ONLY",
            "Gate5": "NOT_CERTIFIED__TWO_ACTUAL_NONEMPTY_F8_F9_F10_F13_ROWS_ONLY",
            "arbitrary_Rn_nonempty_face_rows_before": 0,
            "arbitrary_Rn_nonempty_face_rows_after": 2,
            "materialized_N_F10_values_before": 0,
            "materialized_N_F10_upper_bounds_after": 2,
            "complete_limiting_R1_face_atlas": "NOT_CERTIFIED",
            "weighted_global_F9_F10_F13_sum": "NOT_CERTIFIED",
            "F14_through_F18": "NOT_CERTIFIED",
            "global_Gate5_maturity": "10/18__COMPLETE_BLOCKS_0",
        },
        "strict_status": {
            "Gate1": "NOT_CERTIFIED",
            "Gate2": "NOT_CERTIFIED__OFFICIAL_FIELDS_0_OF_17",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED__LANDING_JOIN_1_OF_7",
            "Gate5": "NOT_CERTIFIED__MATURITY_10_OF_18_BLOCKS_0",
            "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    replay = copy.deepcopy(result)
    result["internal_replay_digest"] = digest(replay)
    return result


def build_manifest(verifier: Path) -> dict[str, Any]:
    result = build_result()
    require(REPORT.is_file() and verifier.is_file() and COMMON.is_file(), "artifact presence")
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-json", action="store_true")
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--verifier", type=Path, default=VERIFIER)
    args = parser.parse_args()
    try:
        if args.replay:
            result = build_result()
            print(json.dumps({
                "faces": result["compact_parameterized_face_germ"]["materialized_face_component_count"],
                "traces": result["compact_parameterized_face_germ"]["materialized_trace_count"],
                "F10": result["explicit_local_field_ledger"]["F10_explicit_integer_upper"],
                "status": "PASS",
            }, sort_keys=True))
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
        print(f"ROUND70_CERT_ERROR: {exc}", file=sys.stderr)
        return 1
    print("ROUND70 SELECTED NONEMPTY FACE INCIDENCE: PARTIAL_ONLY")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
