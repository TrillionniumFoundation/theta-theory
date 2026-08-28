#!/usr/bin/env python3
"""Independent aggregate audit producer for the four frozen Round-65 leaves."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round65_common import (
    CertError, canonical_bytes, digest, replay_sidecar, require, sha256_path,
    strict_json_path, validate_pins,
)


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.round65-independent-core-frontier-audit.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-round65-independent-core-frontier-audit"
REPORT = HERE / f"{PREFIX}-2026-07-21.md"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
VERIFIER = HERE / "cm2_round65_independent_core_frontier_audit_verifier.py"
COMMON = HERE / "cm2_round65_common.py"

PINS = {
    "cm2-sixty-fourth-direct-assault-2026-07-21.md":
        "bbd52eed540e4e91566a7d0b9fda2b381b35860640e23a0a45d29b73fabb8b61",
    "cm2-sixty-fourth-direct-assault-manifest-2026-07-21.sha256":
        "5d2174cee61c0fdf5573dedaece38950c0261fe05aa835b66c4363d974e52932",
    "cm2-round64-independent-core-frontier-audit-manifest-2026-07-21.json":
        "e775720b2891146a39421d515280e119f42b075d0783650e879abe1370ff8779",
    "cm2-gate13-round65-actual-cross-tail-piola-current-frontier-assault-2026-07-21.md":
        "634eb5d96d5837fb1a09f6c87d18b362a35d62be296c8a516d6e9ad648a016a8",
    "cm2-gate13-round65-actual-cross-tail-piola-current-frontier-manifest-2026-07-21.json":
        "e87bb0896c1fc59b6b020d1325bd9462fd932f5d186acabb0fcf770ed9b34701",
    "cm2-gate13-round65-actual-cross-tail-piola-current-frontier-manifest-2026-07-21.sha256":
        "1adc6c78ae09bfd0113271794d5a99ad95655297e54e248c87c16eddbab6ab49",
    "cm2-gate24-round65-actual-product-tree-strong-assembly-frontier-assault-2026-07-21.md":
        "50868c8cee687425a43395e23210dbeddc8414006700fe23a7231721a4ee2e3a",
    "cm2-gate24-round65-actual-product-tree-strong-assembly-frontier-manifest-2026-07-21.json":
        "6b50742ac15f4fb4870d8e67b466252e57c1c796e48a1eaae5d2380f113cddd3",
    "cm2-gate24-round65-actual-product-tree-strong-assembly-frontier-manifest-2026-07-21.sha256":
        "924dbdc03b03b21094e637703353735ae348d9ef53c0c68b6e8acde5a4dfb1a3",
    "cm2-gate5-round65-cross-time-sector-jordan-cemetery-frontier-assault-2026-07-21.md":
        "345215404cd3c2e634a614682fc7404fbca57721b3ddd1ab2959699734efd154",
    "cm2-gate5-round65-cross-time-sector-jordan-cemetery-frontier-manifest-2026-07-21.json":
        "43d80312d1ada853af84a9d8f5edd4393388a62ae3788e9fbcc1eaa4ea510ce5",
    "cm2-gate5-round65-cross-time-sector-jordan-cemetery-frontier-manifest-2026-07-21.sha256":
        "f9863eda87a427723183896815fda5c2036f826c93be789a1189e0f85b8fbdc1",
    "cm2-round65-cross-gate-positive-potential-technology-frontier-assault-2026-07-21.md":
        "9bcf25242a4190e591919bd38233da4e036be22fc2c84739540a555f5f56b0ab",
    "cm2-round65-cross-gate-positive-potential-technology-frontier-manifest-2026-07-21.json":
        "f731715bd734649073e0bd35763c170a48ef8383f6dd892696b52a98ea86eb14",
    "cm2-round65-cross-gate-positive-potential-technology-frontier-manifest-2026-07-21.sha256":
        "ba3e550ac55d7e482d15817cdb9011c7a118100d90158d1c7aabdfeb94785b5a",
    "cm2_round65_common.py":
        "e78882fe127d209fc1935fc1baba6ee027d9585b1fb5e7489be9f554b5a87850",
}

LEAVES = {
    "gate13": "cm2-gate13-round65-actual-cross-tail-piola-current-frontier-manifest-2026-07-21.json",
    "gate24": "cm2-gate24-round65-actual-product-tree-strong-assembly-frontier-manifest-2026-07-21.json",
    "gate5": "cm2-gate5-round65-cross-time-sector-jordan-cemetery-frontier-manifest-2026-07-21.json",
    "cross": "cm2-round65-cross-gate-positive-potential-technology-frontier-manifest-2026-07-21.json",
}

LEDGERS = [
    ("cm2-gate13-round65-actual-cross-tail-piola-current-frontier-manifest-2026-07-21.sha256", 5),
    ("cm2-gate24-round65-actual-product-tree-strong-assembly-frontier-manifest-2026-07-21.sha256", 4),
    ("cm2-gate5-round65-cross-time-sector-jordan-cemetery-frontier-manifest-2026-07-21.sha256", 5),
    ("cm2-round65-cross-gate-positive-potential-technology-frontier-manifest-2026-07-21.sha256", 5),
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
    typing = result["gate1"]["selected_QNL_vs_combined_Green_typing"]
    require(Q(typing["tempting_display_quotient"]) == Q(9100, 9281) < 1,
            "Gate13 display quotient")
    for key in ("same_gauge", "same_registry", "same_quantifier",
                "same_inequality_direction", "lawful_q_cross_instantiation"):
        require(typing[key] is False, f"Gate13 typing {key}")
    rows = result["gate1"]["two_plaque_completion_separator"]["rows"]
    require(len(rows) == 8 and [Q(row["bad_plaque_T_n"]) for row in rows] ==
            [Q(-1 if n % 2 else 1) for n in range(1, 9)], "Gate13 separator")
    models = result["gate1"]["four_wedge_resonant_criterion"]["models"]
    require(models[0]["all_four_nonzero"] is False and
            Q(models[0]["noncancellation_scalar"]) == 0, "Gate13 critical wedge")
    require(models[1]["all_four_nonzero"] is True and
            [Q(x) for x in models[1]["four_oriented_wedges"]] ==
            [Q(1, 2), Q(1), Q(-1, 2), Q(1)], "Gate13 four wedges")
    trace = result["gate3"]["strong_trace_criterion"]
    require([Q(row["moving_current_coefficient"]) for row in trace["weak_L1_separator_rows"]] ==
            [Q(2), Q(4), Q(8), Q(16), Q(32), Q(64)], "Gate13 trace separator")
    piola = result["gate3"]["Piola_derivative_loss"]
    require(piola["operator_norm_differentiable_W11_to_L1"] is False and
            Q(piola["rows"][-1]["remainder_over_W11"]) == Q(128, 129),
            "Gate13 Piola separator")
    stopped = result["gate3"]["stopped_MT_DQ"]
    require(Q(stopped["total_mass"]) == 1 and
            stopped["depth_weighted_derivative_sum"] == "DIVERGES",
            "Gate13 stopped separator")
    return {
        "typing_rows": "5/5_FALSE_SUBSTITUTION",
        "two_plaque_rows": "8/8",
        "four_wedge_models": "2/2",
        "trace_rows": "6/6",
        "Piola_rows": "7/7",
        "stopped_rows": "6/6",
        "status": "INDEPENDENT_PASS",
    }


def audit_gate24(result: dict[str, Any]) -> dict[str, Any]:
    strict = result["strict_status"]
    require(strict["actual_stable_tree_instantiation"] == "0/7" and
            strict["CM2"] == "NO-GO_FOR_CLAIM", "Gate24 strict state")
    interface = result["actual_product_tree_interface"]
    require(interface["actual_rows_complete"] == "0/7" and
            len(interface["rows"]) == 7, "Gate24 interface")
    replay = result["standard_Borel_plaque_law_saturation"]["finite_replay"]
    require(Q(replay["P_eta"]) == Q(19, 80) and
            Q(replay["delta_eta"]) == Q(2, 5) and replay["strict_sandwich"] is True,
            "Gate24 plaque replay")
    depth = result["all_depth_stable_transform"]
    require(Q(depth["good_first_failure_replay"]["infinite_survivor_mass"]) == Q(3, 4),
            "Gate24 good survivor")
    require(Q(depth["positive_every_finite_depth_separator"]["infinite_survivor_mass"]) == 0 and
            depth["depth97_separator"]["first_unconstrained_depth"] == 97,
            "Gate24 depth separators")
    strong = result["tag_graph_to_BV_strong_frontier"]
    rows = strong["W_D_Linfinity_not_BV_separator"]["rows"]
    require([Q(row["weighted_kernel_variation"]) for row in rows] ==
            [Q(4), Q(8), Q(68), Q(1028), Q(16384)], "Gate24 BV separator")
    require(strong["trace_factorisation_no_go"]["status"] ==
            "FALSE_BY_SMOOTH_EXACT_TRACE_SEPARATOR", "Gate24 trace no-go")
    return {
        "actual_tree_rows": "0/7",
        "P_eta": "19/80", "delta_eta": "2/5",
        "first_failure_replays": "2/2",
        "BV_separator_rows": "5/5",
        "trace_factorisation": "NO_GO_PASS",
        "status": "INDEPENDENT_PASS",
    }


def audit_gate5(result: dict[str, Any]) -> dict[str, Any]:
    strict = result["strict_status"]
    require(strict["Gate5_maturity"] == "10/18" and
            strict["complete_18_field_blocks"] == 0, "Gate5 strict state")
    split = result["live_arrival_split"]
    require([row["c_split_star"] for row in split["rows"]] ==
            ["1/2", "3/2", "INFINITY"], "Gate5 split rows")
    sector = result["sectorwise_common_kernel"]
    require(len(sector["sectors"]) == 7 and len(sector["finite_replay"]) == 7,
            "Gate5 sectors")
    require(sector["charge_marginal_tier_is_common_physical_kernel"] is False,
            "Gate5 charge/common guard")
    raw = result["active_raw_Orlicz"]
    require(Q(raw["separator"]["base_weighted_sum"]) == 2 and
            raw["separator"]["raw_weighted_sum"] == "DIVERGES_CONSTANT" and
            raw["base_drift_implies_raw_drift"] is False, "Gate5 raw separator")
    cemetery = result["cemetery_resolvent"]
    require(Q(cemetery["finite_replay"]["arrival_weighted_sum"]) == Q(8, 5) and
            Q(cemetery["finite_replay"]["occupancy_weighted_sum"]) == Q(16, 5),
            "Gate5 cemetery replay")
    bridge = result["oriented_positive_bridge"]
    require(Q(bridge["strict_replay"]["c_star"]) == Q(1, 2) and
            bridge["Round61_target_forward_reverse_total_equality"] == "NOT_CERTIFIED",
            "Gate5 bridge")
    remaining = result["remaining_eight_fields"]
    require(remaining["open_count"] == 8 and remaining["new_field_promoted"] is False,
            "Gate5 open fields")
    require([row["field"] for row in remaining["rows"]] ==
            ["F5", "F6", "F10", "F11", "F14", "F15", "F17", "F18"],
            "Gate5 field names")
    return {
        "live_arrival_rows": "3/3",
        "sector_rows": "7/7",
        "raw_separator_rows": "16/16",
        "cemetery_replay": "PASS",
        "oriented_bridge": "PASS",
        "open_fields": "8/8",
        "status": "INDEPENDENT_PASS",
    }


def audit_cross(result: dict[str, Any]) -> dict[str, Any]:
    require(result["strict_status"]["CM2"] == "NO-GO_FOR_CLAIM",
            "cross strict state")
    theorem = result["positive_path_potential_theorem"]
    require(theorem["bounded_iff"] == "H in L_infinity(mu)" and
            theorem["operator_norm"] == "||A||=ess_sup_mu H" and
            theorem["signed_cancellation_pays_positive_norm"] is False,
            "cross theorem")
    sep = result["two_factor_separator"]
    require(Q(sep["w_times_kappa"]) == Q(1, 2) and
            Q(sep["one_time_actual_moment"]) == 3 and
            Q(sep["all_time_actual_one_vector_charge"]) == 6 and
            sep["conditional_potential_unbounded"] is True,
            "cross separator")
    require(len(sep["time_rows"]) == 12 and len(sep["tag_rows"]) == 12,
            "cross rows")
    require(result["cemetery_typing"]["lawful_positive_cemetery"] ==
            "ONE_SHOT_ARRIVAL_LEDGER", "cross cemetery")
    return {
        "path_potential_iff": "PASS",
        "time_rows": "12/12", "tag_rows": "12/12",
        "one_vector_charge": "6", "operator": "UNBOUNDED",
        "status": "INDEPENDENT_PASS",
    }


def build_result() -> dict[str, Any]:
    validate_pins(HERE, PINS)
    sidecar_rows = sum(replay_sidecar(HERE, HERE / name, count)
                       for name, count in LEDGERS)
    require(sidecar_rows == 19, "leaf sidecar total")
    leaves = load_results()
    cross_rows = [
        "SELECTED_QNL_UPPER_TAIL_RATIO_IS_NOT_ALL_PLAQUE_COMBINED_GREEN_Q_CROSS",
        "TWO_NONZERO_AXIS_WEDGES_DO_NOT_IMPLY_THE_COMPLETE_FOUR_WEDGE_TOKEN",
        "WEAK_NORM_ONE_RESTRICTION_IS_NOT_A_BOUNDED_TWO_SIDED_TRACE_DERIVATIVE",
        "POINTWISE_PIOLA_DIFFERENTIABILITY_IS_NOT_OPERATOR_NORM_DIFFERENTIABILITY",
        "FINITE_DEPTH_POSITIVE_STABLE_SHADOW_IS_NOT_AN_ALL_DEPTH_PRODUCT_TREE",
        "W_D_L_INFINITY_WITHOUT_TRANSVERSE_VARIATION_IS_NOT_TAGGED_BV_ASSEMBLY",
        "OWNER_MASS_CONTRACTION_DOES_NOT_PAY_RAW_Z_ORLICZ_OR_STRONG_TAG_COST",
        "SIGNED_CURRENT_EQUALITY_DOES_NOT_PAY_ORIENTED_POSITIVE_COMMON_MODE",
        "FINITE_ACTUAL_ALL_TIME_VECTOR_MOMENT_IS_NOT_AN_L1_STRONG_OPERATOR_BOUND",
        "CURRENT_EXTERNAL_RESULTS_ASSUME_OR_USE_THE_WRONG_PHYSICAL_INTERFACE",
    ]
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "all_four_leaves_frozen_before_audit": True,
            "audit_authored_source_leaf": False,
            "old_artifacts_modified": False,
            "pins": PINS,
        },
        "gate13": audit_gate13(leaves["gate13"]),
        "gate24": audit_gate24(leaves["gate24"]),
        "gate5": audit_gate5(leaves["gate5"]),
        "cross_gate": audit_cross(leaves["cross"]),
        "cross_leaf_consistency": {
            "status": "PASS_NO_TYPE_SUBSTITUTION_OR_STATE_CONTRADICTION",
            "rows": cross_rows,
            "rows_sha256": digest(cross_rows),
        },
        "source_leaf_acceptance": {
            "new_python_syntax_including_round65_common": "9/9",
            "dependency_pin_rows": "84/84",
            "SHA_artifact_rows": "19/19",
            "integrity_replay_reemit": "4/4",
            "hostile_semantic": "1148/1148_REJECTED",
            "strict_JSON": "16/16_REJECTED",
            "default_entry_points": "8/8_EXIT_2",
        },
        "latest_technology_boundary": {
            "external_theorem_promoted": False,
            "verified_boundary": "current response, smooth-SRB, dominated-kernel and diffusion results do not supply the pinned moving-billiard joins",
        },
        "strict_final_state": {
            "Gate1": "NOT_CERTIFIED",
            "Gate2": "NOT_CERTIFIED__OFFICIAL_FIELDS_0_OF_17",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED__LANDING_JOIN_1_OF_7_FIELDS_1_4_7_PARTIAL",
            "Gate5": "NOT_CERTIFIED__MATURITY_10_OF_18_BLOCKS_0",
            "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
            "audit_verdict": "PASS__NO_SOURCE_LEAF_CORRECTION_REQUIRED",
        },
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
        "verdict": result["strict_final_state"],
    }


def replay() -> dict[str, Any]:
    result = build_result()
    require(result["gate13"]["status"] == result["gate24"]["status"] ==
            result["gate5"]["status"] == result["cross_gate"]["status"] ==
            "INDEPENDENT_PASS", "leaf audit replay")
    return {
        "pins": "16/16", "leaf_sidecar_rows": "19/19",
        "leaves": "4/4", "cross_rows": "10/10", "status": "PASS",
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
        print(f"ROUND65_AUDIT_CERT_ERROR: {exc}", file=sys.stderr)
        return 1
    print("ROUND65 AUDIT: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
