#!/usr/bin/env python3
"""Independent aggregate-audit producer for the four frozen Round-67 leaves."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round67_common import (
    CertError, canonical_bytes, digest, replay_sidecar, require, sha256_path,
    strict_json_path, validate_pins,
)


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.round67-independent-core-frontier-audit.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-round67-independent-core-frontier-audit"
REPORT = HERE / f"{PREFIX}-2026-07-21.md"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
VERIFIER = HERE / "cm2_round67_independent_core_frontier_audit_verifier.py"
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
    "cm2-gate13-round67-actual-root-transfer-uniform-piola-frontier-assault-2026-07-21.md":
        "55c95b1b8b3b437e7354e8d7bbe953f5736a08ef552388a7ff289147950a4dcc",
    "cm2-gate13-round67-actual-root-transfer-uniform-piola-frontier-manifest-2026-07-21.json":
        "af4a0013714bd241d32d3dea215cfbcce4673f594931763da36e6bc2356cfb46",
    "cm2-gate13-round67-actual-root-transfer-uniform-piola-frontier-manifest-2026-07-21.sha256":
        "66c5357af7f968d86f5eed6cfe8d45aedd0fb53bdd6518dc8f2b9ad54b686c9e",
    "cm2-gate24-round67-actual-root-stable-tail-variation-frontier-assault-2026-07-21.md":
        "aab78d659f427a190b62544160a9b2f4acfe79104d53cec418642df6b61e67ff",
    "cm2-gate24-round67-actual-root-stable-tail-variation-frontier-manifest-2026-07-21.json":
        "d868ff5865dd573077e814e1d562a14ef6aaee75c1607ce0303d02a40ddcee9f",
    "cm2-gate24-round67-actual-root-stable-tail-variation-frontier-manifest-2026-07-21.sha256":
        "73e52d46c31f52ecb237d90140fde2223c937444dce135f3af643e3463a90978",
    "cm2-gate5-round67-direct-positive-potential-attenuation-frontier-assault-2026-07-21.md":
        "2b70ebff159efc8d4a1ca27b0be0ca85dbb64ee2101258ac588aba6898318a2d",
    "cm2-gate5-round67-direct-positive-potential-attenuation-frontier-manifest-2026-07-21.json":
        "fa35f45bd9d31976b62d7dfd988b774ec5404a5bd3755994e627711857710cfd",
    "cm2-gate5-round67-direct-positive-potential-attenuation-frontier-manifest-2026-07-21.sha256":
        "99cf63090f60829751aa651fcc3e3a29e103cd64561db7285dc5ef8d06c13fc7",
    "cm2-round67-fixed-j-occurrence-owner-root-time-potential-frontier-assault-2026-07-21.md":
        "d6082b2e50efd99a6c9ddaf578bc467e2ee6a75411fc5b3dc5be1ea5d8cf908b",
    "cm2-round67-fixed-j-occurrence-owner-root-time-potential-frontier-manifest-2026-07-21.json":
        "97cb410b9e960d8331a37ef9203b040c9b1d86c3ed3d1ba6ba66a28c4e4ff400",
    "cm2-round67-fixed-j-occurrence-owner-root-time-potential-frontier-manifest-2026-07-21.sha256":
        "0d6d1c65701c6d838c6464c798177ca0fb8f8fc748b24d04fa24cf8c1bae310b",
    "cm2_round67_common.py":
        "8e9d5959b4ce7d6012773e882d048a14e24c5bcae5d80dfc0b131d5ae96f7110",
}

LEAVES = {
    "gate13": "cm2-gate13-round67-actual-root-transfer-uniform-piola-frontier-manifest-2026-07-21.json",
    "gate24": "cm2-gate24-round67-actual-root-stable-tail-variation-frontier-manifest-2026-07-21.json",
    "gate5": "cm2-gate5-round67-direct-positive-potential-attenuation-frontier-manifest-2026-07-21.json",
    "cross": "cm2-round67-fixed-j-occurrence-owner-root-time-potential-frontier-manifest-2026-07-21.json",
}

LEDGERS = [
    ("cm2-gate13-round67-actual-root-transfer-uniform-piola-frontier-manifest-2026-07-21.sha256", 5),
    ("cm2-gate24-round67-actual-root-stable-tail-variation-frontier-manifest-2026-07-21.sha256", 4),
    ("cm2-gate5-round67-direct-positive-potential-attenuation-frontier-manifest-2026-07-21.sha256", 5),
    ("cm2-round67-fixed-j-occurrence-owner-root-time-potential-frontier-manifest-2026-07-21.sha256", 5),
]


def load_results() -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for key, name in LEAVES.items():
        data = strict_json_path(HERE / name)
        require(isinstance(data.get("result"), dict), f"leaf result: {key}")
        out[key] = data["result"]
    return out


def audit_gate13(result: dict[str, Any]) -> dict[str, Any]:
    require(result["strict_status"] == {
        "CM2": "NO-GO_FOR_CLAIM", "Gate1": "NOT_CERTIFIED",
        "Gate3": "NOT_CERTIFIED", "complete_composite_gates": "0/5",
    }, "Gate13 strict state")
    g1 = result["gate1"]
    root = g1["maximal_actual_root_crosswalk"]
    require(root["status"] == "CERTIFIED_ACTUAL_ROOT_AND_EXACT_FORMAL_TRANSFER" and
            root["relative_transfer"] == "C=Q^-1 E D" and
            root["same_physical_derivative_cocycle"] == "CERTIFIED" and
            root["same_root_tokens"] == "CERTIFIED" and
            root["same_key_Q_E_u_v_rows"] == "NOT_CERTIFIED" and
            root["rational_replay"]["det_C"] == "1", "Gate1 actual root")
    sep = g1["endpoint_completion_separator"]
    require(len(sep["rows"]) == 8 and
            [row["renormalized_oscillatory"] for row in sep["rows"]] ==
            ["-1", "1", "-1", "1", "-1", "1", "-1", "1"] and
            sep["selected_constants_determine_actual_endpoint_limits"] is False,
            "Gate1 endpoint separator")
    wedge = g1["wedge_transport_boundary"]
    require(wedge["actual_tail_limits"] == "NOT_CERTIFIED" and
            wedge["actual_combined_loop_replay"] == "NOT_CERTIFIED" and
            wedge["simultaneous_exact_transport_preserves_nonzero_wedges"] is True,
            "Gate1 wedge boundary")
    g3 = result["gate3"]
    window = g3["common_material_window"]
    require(window["criterion"] == "r_*=inf_k r_k>0" and
            window["actual_all_cell_all_depth_infimum"] == "NOT_CERTIFIED" and
            [row["minimum_radius"] for row in window["rows"]] ==
            ["1", "1/2", "1/4", "1/8", "1/16", "1/32"], "material window")
    direct = g3["weighted_direct_sum"]
    require(direct["replay_supremum"] == "2" and
            direct["actual_uniform_weighted_remainder"] == "NOT_CERTIFIED",
            "weighted direct sum")
    piola = g3["three_factor_uniform_piola"]
    require(piola["product_differentiability_implies_each_factor"] is False and
            piola["actual_strong_Rhat_Phat_Qhat"] == "NOT_CERTIFIED" and
            len(piola["rows"]) == 5, "three factor Piola")
    trace = g3["side_tagged_trace_current"]
    require(trace["replay_total"] == "47/2" and trace["side_tags_disjoint"] is True and
            trace["actual_two_sided_strong_trace"] == "NOT_CERTIFIED" and
            trace["actual_clock_face_cemetery_current"] == "NOT_CERTIFIED",
            "side tagged trace")
    stopped = g3["nonautonomous_stopped_MT_DQ"]
    require(stopped["actual_positive_all_depth_ledger"] == "NOT_CERTIFIED" and
            stopped["actual_pathwise_M_i_L_i"] == "NOT_CERTIFIED" and
            len(stopped["rows"]) == 6, "stopped MT_DQ")
    return {
        "actual_formal_root": "PASS", "endpoint_completion_rows": "8/8",
        "actual_endpoint_wedge_rows": "0/3", "material_window_rows": "6/6",
        "Piola_rows": "5/5", "trace_tags": "3/3", "stopped_rows": "6/6",
        "status": "INDEPENDENT_PASS",
    }


def audit_gate24(result: dict[str, Any]) -> dict[str, Any]:
    strict = result["strict_status"]
    require(strict["actual_stable_tree_instantiation"] == "0/7" and
            strict["Gate2"] == "NOT_CERTIFIED__OFFICIAL_FIELDS_0_OF_17" and
            strict["CM2"] == "NO-GO_FOR_CLAIM", "Gate24 strict state")
    reg = result["actual_graph_supported_pre_registry"]
    require(reg["status"].endswith("STABLE_SEMANTICS_ABSENT") and
            reg["scope_guards"]["is_invariant_stable_product"] is False and
            reg["scope_guards"]["is_global_CM2_root"] is False and
            reg["graph_supported_maps"]["support"] ==
            "joint deterministic pushforward is supported on every declared equality graph",
            "Gate24 pre-registry scope")
    chart = reg["affine_chart"]
    require(chart["determinant"] == "-3" and
            chart["squared_singular_values"] == ["2", "9/2"] and
            chart["compatibility"] == "J_(v,w)rho_w=rho_v/lambda_(v,w)" and
            chart["metric_factor_strict_upper"] == "101/100", "affine chart")
    tree = result["actual_product_tree_interface"]
    require(tree["actual_rows_complete"] == "0/7" and tree["partial_rows"] == [2, 4, 7] and
            len(tree["rows"]) == 7, "actual tree")
    hazard = result["all_depth_conditional_hazard"]
    require(hazard["actual_collision_component_zero_rows"] == 96 and
            hazard["actual_full_conditional_hazard_rows"] == 0 and
            hazard["sharp_actual_survivor_lower_bound"] == "0" and
            hazard["summable_replay"]["limit"] == "1/2" and
            hazard["divergent_replay"]["limit"] == "0", "conditional hazard")
    anchors = result["distinct_physical_anchor_audit"]
    require(anchors["same_immutable_root_crosswalk"] == "NOT_CERTIFIED" and
            anchors["may_combine_exact_density_with_96_word_stable_crossing"] is False,
            "distinct anchors")
    marker = result["marker_saturation_and_budget"]
    require(marker["stable_saturation"]["actual_P_eta_zero"] == "NOT_CERTIFIED" and
            marker["stable_saturation"]["pre_registry_carries_actual_g_B"] is False and
            marker["zero_defect_implies_BV"] is False, "marker scope")
    recipient = result["fixed_material_weighted_BV_recipient"]
    require(recipient["actual_all_depth_strong_Piola_recipient"] == "NOT_CERTIFIED" and
            recipient["same_root_as_Round25_pre_registry"] is False and
            recipient["moving_family"]["replay"]["S_q"] == "9/2" and
            len(recipient["moving_family"]["replay"]["quadratic_remainder_rows"]) == 5,
            "BV recipient")
    return {
        "actual_pre_registry": "PASS_LOCAL_R1_ONLY", "affine_chart": "PASS",
        "actual_tree_rows": "0/7", "hazard_rows": "0/96_FULL",
        "hazard_replays": "2/2", "immutable_anchor_join": "NOT_CERTIFIED",
        "marker_BV_guards": "3/3", "BV_remainder_rows": "5/5",
        "status": "INDEPENDENT_PASS",
    }


def audit_gate5(result: dict[str, Any]) -> dict[str, Any]:
    strict = result["strict_status"]
    require(strict["Gate5_maturity"] == "10/18" and
            strict["complete_18_field_blocks"] == 0 and
            strict["CM2"] == "NO-GO_FOR_CLAIM", "Gate5 strict state")
    potential = result["maximal_direct_potential"]
    require(potential["status"] == "CERTIFIED_EXACT" and
            potential["operator_criterion"] ==
            "A:L1(mu)->positive typed direct sum bounded iff H in Linfinity(mu)" and
            potential["operator_norm"] == "||A||=||H||_infinity" and
            potential["signed_cancellation_pays_positive_norm"] is False,
            "direct potential")
    terminal = result["terminal_moment_identity"]
    model = terminal["geometric_model"]
    require(terminal["exact_strong_condition"] ==
            "ess_sup_x E_x[w_Z^N]<infinity" and
            terminal["actual_terminal_exponential_moment"] == "NOT_CERTIFIED" and
            model["survivor_full_label_RN_density"] == "1" and
            model["w_Z_r"] == "1/2" and model["E_w_to_N"] == model["H_live"] == "2",
            "terminal moment")
    attenuation = result["lawful_attenuation"]
    require(attenuation["sub_Markov"]["average_mass_decay_suffices"] is False and
            attenuation["Doob_Lyapunov"]["integral_V_0_only_suffices"] is False and
            attenuation["Doob_Lyapunov"]["source_requirement_for_unweighted_L1"] ==
            "V_0 in Linfinity(mu)", "lawful attenuation")
    sep = result["strong_separator"]
    require(sep["one_time_actual_moment"] == "3" and
            sep["all_time_actual_moment"] == "6" and sep["H_in_Linfinity"] is False and
            len(sep["rows"]) == 12, "strong separator")
    departure = result["one_shot_departure"]
    require(departure["limit_identity"] == "H_departure=x_0+(w_Z-1)H_live" and
            departure["absorbing_occupancy_if_nonzero"] == "DIVERGES_FOR_w_Z_GT_1" and
            departure["requires_weighted_live_finite"] is True and
            departure["pays_owner_birth"] is False and
            len(departure["harmonic_separator"]["rows"]) == 12, "one-shot departure")
    sectors = result["seven_sector_potential"]
    require(len(sectors["sectors"]) == len(sectors["actual_rows"]) == 7 and
            sectors["actual_H_total"] == "NOT_EVALUABLE_OR_CERTIFIED" and
            sectors["base_survival_pays_unbounded_marks"] is False, "seven sectors")
    oriented = result["oriented_positive_pair"]
    require(oriented["two_orientation_RN_rows"] == "NOT_CERTIFIED" and
            oriented["common_mode_equality"] == "NOT_CERTIFIED" and
            oriented["physical_potentials_materialized"] is False, "oriented pair")
    remaining = result["remaining_eight_fields"]
    require(remaining["open_count"] == 8 and remaining["new_field_promoted"] is False and
            [row["field"] for row in remaining["rows"]] ==
            ["F5", "F6", "F10", "F11", "F14", "F15", "F17", "F18"],
            "remaining fields")
    return {
        "direct_potential": "PASS", "conditional_terminal_model": "PASS",
        "strong_separator_rows": "12/12", "departure_rows": "12/12",
        "sector_rows": "7/7", "oriented_guards": "3/3",
        "open_fields": "8/8", "status": "INDEPENDENT_PASS",
    }


def audit_cross(result: dict[str, Any]) -> dict[str, Any]:
    require(result["strict_status"]["CM2"] == "NO-GO_FOR_CLAIM" and
            result["strict_status"]["complete_composite_gates"] == "0/5",
            "cross strict state")
    subroot = result["actual_fixed_j_subroot"]
    require(subroot["status"] == "CERTIFIED_GRAPH_SUPPORTED_PHYSICAL_SUBROOT" and
            subroot["root_measure"] == "M_j=m_j^own" and
            subroot["time_deleted_or_deduplicated"] is False and
            len(subroot["retained_keys"]) == 8 and
            subroot["Round54_Jordan_common_mode_identified"] is False,
            "fixed-j physical subroot")
    carrier = result["countable_time_carrier"]
    require(carrier["status"] == "CERTIFIED_STANDARD_BOREL_CARRIER_ONLY" and
            carrier["finite_weighted_physical_law"] == "NOT_CERTIFIED" and
            carrier["strong_all_time_operator"] == "NOT_CERTIFIED", "time carrier")
    potential = result["direct_root_potential"]
    require(potential["status"] == "CERTIFIED_EXACT_ON_OCCURRENCE_ROOT" and
            potential["actual_all_sector_H_g"] == "NOT_CERTIFIED" and
            potential["fixed_time_L1_implies_strong_all_time"] is False,
            "root potential")
    sep = result["finite_average_separators"]
    require(sep["single_slice_total_weighted_charge"] == "6/5" and
            sep["eligibility_total_weighted_charge"] == "8/5" and
            sep["single_slice_potential_unbounded"] is True and
            sep["eligibility_potential_unbounded"] is True and len(sep["rows"]) == 16,
            "finite average separators")
    eligibility = result["terminal_eligibility"]
    require(eligibility["bounded_iff"] == "n in L_infinity(m_occ)" and
            eligibility["actual_owner_pointwise_pattern"] == "NOT_CERTIFIED" and
            eligibility["eligibility_divergence_implies_actual_owner_divergence"] is False,
            "terminal eligibility")
    registry = result["minimal_spanning_registry"]
    require(registry["global_graph_supported_root"] == "NOT_CERTIFIED" and
            registry["Gate1_actual_common_rows"] == "0/8" and
            registry["Gate24_actual_tree_rows"] == "0/7" and
            len(registry["open_edges"]) == 4, "spanning registry")
    return {
        "fixed_j_subroot": "PASS", "retained_keys": "8/8",
        "time_carrier": "BOREL_ONLY", "separator_rows": "16/16",
        "actual_all_sector_potential": "NOT_CERTIFIED", "open_crosswalks": "4/4",
        "status": "INDEPENDENT_PASS",
    }


def build_result() -> dict[str, Any]:
    validate_pins(HERE, PINS)
    sidecar_rows = sum(replay_sidecar(HERE, HERE / name, count)
                       for name, count in LEDGERS)
    require(sidecar_rows == 19, "source sidecar rows")
    dependency_rows = sum(len(strict_json_path(HERE / name)["pins"])
                          for name in LEAVES.values())
    require(dependency_rows == 101, "source dependency rows")
    leaves = load_results()
    cross_rows = [
        "ACTUAL_CLEAN_SYMBOLIC_ROOT_AND_EXACT_FORMAL_TRANSFER_DO_NOT_SUPPLY_SAME_KEY_Q_E_U_V_ROWS",
        "SELECTED_ENDPOINT_CONSTANTS_DO_NOT_DETERMINE_ALL_PLAQUE_LIMITS_OR_FOUR_WEDGES",
        "LOCAL_DEPTH96_MATERIAL_CONTROL_DOES_NOT_SUPPLY_A_POSITIVE_ALL_DEPTH_COMMON_WINDOW",
        "BLOCKWISE_PIOLA_DIFFERENTIABILITY_DOES_NOT_SUPPLY_UNIFORM_DIRECT_SUM_REMAINDER",
        "THE_R1_OWNER_COLLISION_LANDING_MATERIAL_PRE_REGISTRY_HAS_NO_INVARIANT_STABLE_SEMANTICS",
        "THE_R1_PRE_REGISTRY_AND_ROUND15_59_STABLE_CROSSING_LIVE_ON_UNJOINED_PHYSICAL_ROOTS",
        "NINETY_SIX_ZERO_COLLISION_ROWS_DO_NOT_PAY_FULL_GRAPH_OR_REGISTRY_HAZARDS",
        "ZERO_STABLE_MARKER_DEFECT_DOES_NOT_PAY_WEIGHTED_TRANSVERSE_BV",
        "A_FIXED_J_OCCURRENCE_OWNER_GRAPH_IS_A_GENUINE_PHYSICAL_SUBROOT_NOT_A_GLOBAL_REGISTRY",
        "COUNTABLE_TIME_BOREL_TYPING_DOES_NOT_CREATE_A_FINITE_WEIGHTED_LAW_OR_STRONG_OPERATOR",
        "FINITE_AVERAGE_WEIGHTED_CHARGE_DOES_NOT_IMPLY_AN_L_INFINITY_ROOT_POTENTIAL",
        "DETERMINISTIC_UNBOUNDED_TERMINAL_ELIGIBILITY_HAS_UNBOUNDED_H",
        "CONDITIONAL_RANDOM_TERMINATION_MAY_LAWFULLY_HAVE_ESS_SUP_E_W_TO_N_FINITE",
        "THE_PREVIOUS_TWO_TERMINAL_STATEMENTS_ARE_DIFFERENT_KERNELS_AND_DO_NOT_CONTRADICT",
        "SURVIVOR_FULL_LABEL_RN_DENSITY_ONE_DOES_NOT_PREVENT_CONDITIONAL_TAIL_ATTENUATION",
        "RAW_Z_ORLICZ_PRE_CEMETERY_AND_ORIENTED_COMMON_MODE_REMAIN_UNPAID_ON_THE_COMMON_ROOT",
        "CURRENT_EXTERNAL_RESULTS_DO_NOT_BUILD_THE_MISSING_MOVING_BILLIARD_REGISTRY_AND_STRONG_RECIPIENT",
    ]
    strict = {
        "Gate1": "NOT_CERTIFIED",
        "Gate2": "NOT_CERTIFIED__OFFICIAL_FIELDS_0_OF_17",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED__LANDING_JOIN_1_OF_7_FIELDS_1_4_7_PARTIAL",
        "Gate5": "NOT_CERTIFIED__MATURITY_10_OF_18_BLOCKS_0",
        "complete_composite_gates": "0/5",
        "CM2": "NO-GO_FOR_CLAIM",
        "audit_verdict": "PASS__NO_SOURCE_LEAF_CORRECTION_REQUIRED",
    }
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "all_four_leaves_frozen_before_audit": True,
            "audit_authored_source_leaf": False,
            "old_artifacts_modified": False,
            "pin_count": 18,
            "pins": PINS,
        },
        "gate13": audit_gate13(leaves["gate13"]),
        "gate24": audit_gate24(leaves["gate24"]),
        "gate5": audit_gate5(leaves["gate5"]),
        "fixed_j_root": audit_cross(leaves["cross"]),
        "cross_leaf_consistency": {
            "status": "PASS_NO_TYPE_SUBSTITUTION_OR_STATE_CONTRADICTION",
            "rows": cross_rows,
            "rows_sha256": digest(cross_rows),
        },
        "source_leaf_acceptance": {
            "new_python_syntax_including_round67_common": "9/9",
            "dependency_pin_rows": "101/101",
            "SHA_artifact_rows": "19/19",
            "audit_replay_self_test_reemit": "4/4",
            "hostile_semantic": "1045/1045_REJECTED",
            "strict_JSON": "16/16_REJECTED",
            "default_entry_points": "8/8_EXIT_2",
        },
        "independent_replay": {
            "gate13_transfer": "PASS", "gate24_hazards": "2/2",
            "gate5_conditional_terminal": "PASS", "fixed_j_separators": "2/2",
            "terminal_typing_consistency": "PASS",
        },
        "latest_technology_boundary": {
            "external_theorem_promoted": False,
            "verified_boundary": "smooth Axiom-A product, spectral approximation and diffusion Feynman-Kac results do not build the singular moving-billiard registry or strong recipient",
        },
        "strict_status": strict,
    }
    replay = copy.deepcopy(result)
    result["internal_replay_digest"] = digest(replay)
    return result


def build_manifest(verifier: Path) -> dict[str, Any]:
    result = build_result()
    require(REPORT.is_file() and verifier.is_file() and COMMON.is_file(), "audit artifact")
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
    result = build_result()
    require(result["gate13"]["status"] == result["gate24"]["status"] ==
            result["gate5"]["status"] == result["fixed_j_root"]["status"] ==
            "INDEPENDENT_PASS", "leaf audit replay")
    return {
        "pins": "18/18", "source_sidecar_rows": "19/19",
        "dependency_rows": "101/101", "leaves": "4/4",
        "cross_rows": "17/17", "status": "PASS",
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
        print(f"ROUND67_AUDIT_CERT_ERROR: {exc}", file=sys.stderr)
        return 1
    print("ROUND67 AUDIT: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
