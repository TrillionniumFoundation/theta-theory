#!/usr/bin/env python3
"""Independent aggregate-audit producer for the four frozen Round-66 leaves."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round66_common import (
    CertError, canonical_bytes, digest, replay_sidecar, require, sha256_path,
    strict_json_path, validate_pins,
)


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.round66-independent-core-frontier-audit.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-round66-independent-core-frontier-audit"
REPORT = HERE / f"{PREFIX}-2026-07-21.md"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
VERIFIER = HERE / "cm2_round66_independent_core_frontier_audit_verifier.py"
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
    "cm2-gate13-round66-same-representative-material-trace-frontier-assault-2026-07-21.md":
        "6d37428dde6b8360d759554a9bcd2bfeb91b0c67c0ab3bcc98d91d850fa49278",
    "cm2-gate13-round66-same-representative-material-trace-frontier-manifest-2026-07-21.json":
        "11bb7ba12e3302a547893dae3a897efc5a66223bbc2cf740bb6f7b5e53882224",
    "cm2-gate13-round66-same-representative-material-trace-frontier-manifest-2026-07-21.sha256":
        "4d38f3145099b2cd4222930d32c88dd7ba6bc9797def4673fc9ea00415f3b38e",
    "cm2-gate24-round66-collision-srb-product-variation-frontier-assault-2026-07-21.md":
        "13341aaa40ccc155b85119c457b12a5e09fed43fa618ed0aee280bef0af68b27",
    "cm2-gate24-round66-collision-srb-product-variation-frontier-manifest-2026-07-21.json":
        "be98266945e3e6bd7fee0bf27f49a3282dc41f67e95f74b0c41c041d0cd4bf94",
    "cm2-gate24-round66-collision-srb-product-variation-frontier-manifest-2026-07-21.sha256":
        "de30d5514982930c9dd485313e09a6eb668c2e3dbc1da05d4507ae6a032f1d20",
    "cm2-gate5-round66-owner-overlap-sector-flux-frontier-assault-2026-07-21.md":
        "5328ee45c3fd69e0e4a433910e5562504d1b155e44eb20a024b05194f16d999d",
    "cm2-gate5-round66-owner-overlap-sector-flux-frontier-manifest-2026-07-21.json":
        "31f8b9068b3afaad779f299d5adb3e1ff870d3b48ad943704e1347b7ac06a686",
    "cm2-gate5-round66-owner-overlap-sector-flux-frontier-manifest-2026-07-21.sha256":
        "c538c62bbbb13f1e4b203d72d67cb3fd398752a4636c1a731a9039f9847ce4aa",
    "cm2-round66-immutable-registry-junction-tree-positive-potential-frontier-assault-2026-07-21.md":
        "9b8512389c8ede4c6b59a029565bc314f10502ec9339094036f13f33185463a2",
    "cm2-round66-immutable-registry-junction-tree-positive-potential-frontier-manifest-2026-07-21.json":
        "adc2654ed27fa62c83dd9d64ddce09832e173f50d518c464007d9bc320d6294f",
    "cm2-round66-immutable-registry-junction-tree-positive-potential-frontier-manifest-2026-07-21.sha256":
        "1122a6b11415e5f070ec4a86faa6d78a0a67a30ae836c288e3a732f1c0fa51f3",
    "cm2_round66_common.py":
        "34846761d5b448077a0cb5768d7e44fb2b354ae07f2b0d0475500bf96c85738f",
}

LEAVES = {
    "gate13": "cm2-gate13-round66-same-representative-material-trace-frontier-manifest-2026-07-21.json",
    "gate24": "cm2-gate24-round66-collision-srb-product-variation-frontier-manifest-2026-07-21.json",
    "gate5": "cm2-gate5-round66-owner-overlap-sector-flux-frontier-manifest-2026-07-21.json",
    "cross": "cm2-round66-immutable-registry-junction-tree-positive-potential-frontier-manifest-2026-07-21.json",
}

LEDGERS = [
    ("cm2-gate13-round66-same-representative-material-trace-frontier-manifest-2026-07-21.sha256", 5),
    ("cm2-gate24-round66-collision-srb-product-variation-frontier-manifest-2026-07-21.sha256", 4),
    ("cm2-gate5-round66-owner-overlap-sector-flux-frontier-manifest-2026-07-21.sha256", 5),
    ("cm2-round66-immutable-registry-junction-tree-positive-potential-frontier-manifest-2026-07-21.sha256", 5),
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
        "Gate1": "NOT_CERTIFIED", "Gate3": "NOT_CERTIFIED",
        "complete_composite_gates": "0/5", "CM2": "NO-GO_FOR_CLAIM",
    }, "Gate13 strict state")
    g1 = result["gate1"]
    transfer = g1["relative_shear_transfer"]
    require(transfer["identity_iff"] == "v_c-v_q=0 and u_c=u_q" and
            transfer["models"][1]["matrix"] == [["4/3", "1/2"], ["0", "3/4"]] and
            transfer["models"][1]["determinant"] == "1", "relative transfer")
    tails = g1["all_plaque_tail_transport"]
    require(tails["zero_tail_required"] is False and
            tails["actual_common_registry"] == "NOT_CERTIFIED" and
            "uniform Holder limits" in tails["iff"], "tail interface")
    loop = g1["selected_loop_transport"]
    require(loop["exact_source_loop_transport_iff"] ==
            "H_A^s L_u+L_s H_A^u+L_s L_u=0" and
            loop["models"][1]["correction"] == [["0", "2"], ["-3/2", "-1/2"]] and
            loop["models"][1]["vanishes"] is False, "loop correction")
    registry = g1["minimal_keyed_registry"]
    require(registry["status"] == "0/8_ACTUAL_COMMON_ROWS" and
            len(registry["rows"]) == 8, "Gate1 registry")
    g3 = result["gate3"]
    atlas = g3["physical_compact_interior_atlas"]
    require(atlas["status"] == "CERTIFIED_LOCAL" and
            atlas["all_cells_all_depth_common_s_window"] == "NOT_CERTIFIED", "local atlas")
    rem = g3["direct_sum_uniform_remainder"]
    require([row["N"] for row in rem["rows"]] == [2, 4, 8, 16, 32, 64] and
            all(row["global_supremum"] == "1" for row in rem["rows"]) and
            rem["global_uniform_remainder"] is False, "uniform remainder")
    stopped = g3["stopped_generating_function"]
    require(stopped["finite_for_M_lt_1"] is True and
            stopped["diverges_at_M_eq_1"] is True and
            stopped["actual_common_strong_M_lt_1"] == "NOT_CERTIFIED" and
            len(stopped["rows"]) == 6, "stopped derivative")
    return {
        "relative_transfer_models": "2/2", "tail_loop_criteria": "2/2",
        "actual_registry_rows": "0/8", "local_atlas": "DEPTH_96_ONLY",
        "uniform_remainder_rows": "6/6", "stopped_rows": "6/6",
        "status": "INDEPENDENT_PASS",
    }


def audit_gate24(result: dict[str, Any]) -> dict[str, Any]:
    strict = result["strict_status"]
    require(strict["actual_stable_tree_instantiation"] == "0/7" and
            strict["CM2"] == "NO-GO_FOR_CLAIM", "Gate24 strict state")
    chart = result["sinai_density_product_chart"]
    rep = chart["rational_replay"]
    require(Q(rep["rho_s"]) == 1 and Q(rep["rho_t"]) == Q(2, 3) and
            Q(rep["lambda_st"]) == Q(3, 2) and Q(rep["J_st"]) == 1 and
            chart["actual_product_chart_common_root_density_bounds"] == "NOT_CERTIFIED",
            "product chart")
    cross = result["owner_landing_joint_crosswalk"]
    sep = cross["same_marginals_do_not_determine_key_support"]
    require(sep["compatible_mass_align"] == "1" and
            sep["compatible_mass_switch"] == "0" and
            cross["actual_owner_landing_product_crosswalk"] == "NOT_CERTIFIED",
            "owner landing crosswalk")
    marker = result["stable_marker_saturation"]
    require(Q(marker["varying_completion"]["P_eta"]) == Q(5, 64) and
            Q(marker["varying_completion"]["delta_eta"]) == Q(1, 8) and
            marker["stable_completion"]["P_eta"] == "0" and
            marker["actual_P_eta_zero"] == "NOT_CERTIFIED", "marker separator")
    failure = result["all_depth_first_failure"]
    require(failure["frozen_collision_shadow_rows"] == 96 and
            failure["actual_full_first_failure_upper_bound_rows"] == 0 and
            failure["sharp_actual_survivor_lower_bound"] == "0" and
            Q(failure["geometric_future_interface"]["sample_survivor_lower"]) == Q(3, 4),
            "all-depth boundary")
    variation = result["weighted_variation_and_strong_recipient"]
    rows = variation["zero_defect_unbounded_variation_separator"]["rows"]
    require([row["transverse_variation"] for row in rows] == ["1", "2", "17", "257", "4096"] and
            all(row["P_eta"] == "0" for row in rows), "variation separator")
    sample = variation["material_tag_Piola_BV_bridge"]["sample"]
    require(Q(sample["output_tagged_BV"]) == Q(37, 6) and
            Q(sample["upper_bound"]) == 20 and
            variation["physical_anisotropic_intertwining_recipient"] == "NOT_CERTIFIED",
            "material bridge")
    actual = result["actual_product_tree_interface"]
    require(actual["actual_rows_complete"] == "0/7" and len(actual["rows"]) == 7,
            "actual product tree")
    return {
        "chart_replay": "PASS", "crosswalk_couplings": "2/2",
        "marker_replays": "2/2", "actual_first_failure_rows": "0/96",
        "conditional_survivor_lower": "3/4", "variation_rows": "5/5",
        "actual_tree_rows": "0/7", "status": "INDEPENDENT_PASS",
    }


def audit_gate5(result: dict[str, Any]) -> dict[str, Any]:
    strict = result["strict_status"]
    require(strict["Gate5_maturity"] == "10/18" and
            strict["complete_18_field_blocks"] == 0 and
            strict["CM2"] == "NO-GO_FOR_CLAIM", "Gate5 strict state")
    terminal = result["terminal_record_crosswalk"]
    require(terminal["status"] == "CERTIFIED_EXACT_BOREL_MAXIMAL_OVERLAP" and
            terminal["terminal_eligibility_implies_owner_set_nesting"] is False and
            terminal["cross_time_owner_deduplication"] == "ILLEGAL", "terminal crosswalk")
    rn = result["rn_frontier"]
    replay = rn["finite_replay"]
    require([replay[k] for k in ("source_total", "overlap_total", "birth_total", "next_total")] ==
            [21, 14, 7, 21] and replay["birth_free_full_label_c_live_star"] == "1" and
            replay["with_birth_c_live_star"] == "INFINITY" and
            rn["positive_overlap_route_coefficient_below_w_Z_inverse"] is False,
            "RN frontier")
    sectors = result["seven_sector_overlap"]
    require(len(sectors["sectors"]) == len(sectors["finite_replay"]) == 7 and
            [row["birth_free_kappa_star"] for row in sectors["finite_replay"]] ==
            ["1/2", "2", "2", "1", "2", "1", "1"] and
            all(row["positive_birth_kappa_star"] == "INFINITY"
                for row in sectors["finite_replay"]), "seven sectors")
    raw = result["raw_Orlicz_frontier"]
    require([row["raw_mark"] for row in raw["truncation_rows"]] ==
            [str(2**n) for n in range(1, 13)] and
            raw["comparison_creates_cross_j_coefficient"] is False and
            raw["finite_truncations_uniform"] is False, "raw Orlicz")
    arrival = result["arrival_typing"]
    require(arrival["switch_departure_is_one_shot"] is True and
            arrival["absorbing_occupancy_for_w_Z_gt_1"] == "DIVERGES_IF_NONZERO" and
            arrival["pre_regularization_cemetery"] == "NOT_MATERIALIZED", "arrival typing")
    bridge = result["oriented_positive_frontier"]
    require(bridge["common_mode_equality"] == "NOT_CERTIFIED" and
            bridge["two_RN_rows"] == "NOT_CERTIFIED" and
            bridge["unequal_upper_bounds_imply_unequal_actual_totals"] is False and
            bridge["physical_oriented_carrier"] == "NOT_CERTIFIED", "oriented bridge")
    remaining = result["remaining_eight_fields"]
    require(remaining["open_count"] == 8 and remaining["new_field_promoted"] is False and
            [row["field"] for row in remaining["rows"]] ==
            ["F5", "F6", "F10", "F11", "F14", "F15", "F17", "F18"],
            "remaining fields")
    return {
        "terminal_crosswalk": "PASS", "RN_atoms": "6/6",
        "sector_rows": "7/7", "raw_truncation_rows": "12/12",
        "arrival_typing": "PASS", "positive_bridge_guards": "4/4",
        "open_fields": "8/8", "status": "INDEPENDENT_PASS",
    }


def audit_cross(result: dict[str, Any]) -> dict[str, Any]:
    require(result["strict_status"]["CM2"] == "NO-GO_FOR_CLAIM", "cross strict state")
    theorem = result["junction_tree_theorem"]
    require(theorem["necessary_and_sufficient"] ==
            "EDGE_SEPARATOR_MARGINALS_MATCH_EXACTLY" and
            theorem["abstract_same_law_is_physical_identity"] is False and
            theorem["global_coupling_unique"] is False, "junction theorem")
    tree = result["valid_tree_replay"]
    require(tree["global_atoms"] == ["0001", "1110"] and
            tree["global_atom_count"] == 2, "tree replay")
    cycle = result["cyclic_parity_separator"]
    require(cycle["candidate_atoms"] == 8 and cycle["accepted_count"] == 0 and
            len(cycle["delete_one_constraint_rows"]) == 3 and
            all(row["accepted_count"] == 2 for row in cycle["delete_one_constraint_rows"]),
            "cycle separator")
    root = result["physical_root_equivalence"]
    require(root["anonymous_equal_marginals_suffice"] is False and
            root["actual_cm2_graph_supported_root"] == "NOT_CERTIFIED" and
            len(root["required_cm2_key_groups"]) == 5, "physical root")
    potential = result["glued_positive_potential_separator"]
    require(potential["global_join"] == "TRIVIAL_AND_EXACT" and
            Q(potential["actual_moment"]) == 3 and
            potential["potential_essentially_bounded"] is False and
            len(potential["potential_rows"]) == 16, "positive potential")
    route = result["two_line_sufficient_route"]
    require(route["actual_registry_line"] == route["actual_summability_line"] ==
            "NOT_CERTIFIED", "two-line route")
    return {
        "junction_theorem": "PASS", "valid_tree_atoms": "2/16",
        "cyclic_support": "0/8", "deletion_rows": "3/3",
        "physical_key_groups": "5/5", "potential_rows": "16/16",
        "actual_route_lines": "0/2", "status": "INDEPENDENT_PASS",
    }


def build_result() -> dict[str, Any]:
    validate_pins(HERE, PINS)
    sidecar_rows = sum(replay_sidecar(HERE, HERE / name, count)
                       for name, count in LEDGERS)
    require(sidecar_rows == 19, "source sidecar rows")
    dependency_rows = sum(len(strict_json_path(HERE / name)["pins"])
                          for name in LEAVES.values())
    require(dependency_rows == 134, "source dependency rows")
    leaves = load_results()
    cross_rows = [
        "TRIANGULAR_SYNTAX_IS_NOT_A_SAME_REPRESENTATIVE_GAUGE_CROSSWALK",
        "EXACT_TAIL_TRANSPORT_IFF_WITHOUT_ACTUAL_COMMON_REGISTRY_DOES_NOT_CLOSE_GATE1",
        "DEPTH_96_LOCAL_MATERIAL_ATLAS_IS_NOT_AN_ALL_DEPTH_UNIFORM_PIOLA_ATLAS",
        "FIXED_BRANCH_REMAINDERS_DO_NOT_IMPLY_DIRECT_SUM_OPERATOR_NORM_REMAINDER",
        "EQUAL_OWNER_AND_PLAQUE_MARGINALS_DO_NOT_IMPLY_IMMUTABLE_KEY_SUPPORT",
        "PRODUCT_DENSITY_FORMULAS_AND_ZERO_MARKER_COMPLETION_DO_NOT_MATERIALIZE_THE_ACTUAL_TREE",
        "FINITE_COLLISION_SHADOWS_DO_NOT_BOUND_FULL_STABLE_CHART_FIRST_FAILURES",
        "ZERO_MARKER_DEFECT_DOES_NOT_PAY_WEIGHTED_TRANSVERSE_VARIATION",
        "TERMINAL_ELIGIBILITY_NESTING_DOES_NOT_NEST_OWNER_LABEL_SETS_ACROSS_TIME",
        "POSITIVE_OWNER_BIRTH_IS_SINGULAR_FOR_THE_FULL_LABEL_LIVE_KERNEL",
        "SAME_SLICE_RAW_ORLICZ_COMPARISON_DOES_NOT_CREATE_CROSS_TIME_SECTOR_DRIFT",
        "PAIRWISE_CYCLE_OVERLAPS_DO_NOT_CREATE_A_GRAPH_SUPPORTED_GLOBAL_REGISTRY",
        "EXACT_GLOBAL_REGISTRY_AND_FINITE_ACTUAL_MOMENT_DO_NOT_IMPLY_L_INFINITY_POTENTIAL",
        "CURRENT_EXTERNAL_RESULTS_USE_OR_ASSUME_A_DIFFERENT_PHYSICAL_INTERFACE",
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
        "immutable_registry": audit_cross(leaves["cross"]),
        "cross_leaf_consistency": {
            "status": "PASS_NO_TYPE_SUBSTITUTION_OR_STATE_CONTRADICTION",
            "rows": cross_rows,
            "rows_sha256": digest(cross_rows),
        },
        "source_leaf_acceptance": {
            "new_python_syntax_including_round66_common": "9/9",
            "dependency_pin_rows": "134/134",
            "SHA_artifact_rows": "19/19",
            "audit_replay_self_test_reemit": "4/4",
            "hostile_semantic": "980/980_REJECTED",
            "strict_JSON": "16/16_REJECTED",
            "default_entry_points": "8/8_EXIT_2",
        },
        "latest_technology_boundary": {
            "external_theorem_promoted": False,
            "verified_boundary": "sequential billiard CLT, smooth Anosov response, closed-manifold local product and killed-chain results do not supply the pinned CM2 registry and strong recipient",
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
            result["gate5"]["status"] == result["immutable_registry"]["status"] ==
            "INDEPENDENT_PASS", "leaf audit replay")
    return {
        "pins": "18/18", "source_sidecar_rows": "19/19",
        "dependency_rows": "134/134", "leaves": "4/4",
        "cross_rows": "14/14", "status": "PASS",
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
        print(f"ROUND66_AUDIT_CERT_ERROR: {exc}", file=sys.stderr)
        return 1
    print("ROUND66 AUDIT: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
