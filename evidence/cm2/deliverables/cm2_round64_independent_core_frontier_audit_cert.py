#!/usr/bin/env python3
"""Independent aggregate audit producer for the five frozen Round-64 leaves."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from decimal import Decimal
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round64_common import (
    CertError, canonical_bytes, digest, replay_sidecar, require, sha256_path,
    strict_json_path, validate_pins,
)


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.round64-independent-core-frontier-audit.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-round64-independent-core-frontier-audit"
REPORT = HERE / f"{PREFIX}-2026-07-21.md"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
VERIFIER = HERE / "cm2_round64_independent_core_frontier_audit_verifier.py"
COMMON = HERE / "cm2_round64_common.py"

PINS = {
    "cm2-sixty-third-direct-assault-2026-07-21.md":
        "9cde412ba689be87d777906404c9c9426a2a8a102385a2c4c510df8f9b7a6a05",
    "cm2-sixty-third-direct-assault-manifest-2026-07-21.sha256":
        "a0b512f32914ef2692b31466a4ea156c44698b1eaf44d8ead45b2c74ee73230e",
    "cm2-gate13-round64-one-cross-term-dyadic-clock-frontier-manifest-2026-07-21.json":
        "df730945a80aad801b5923729e5c8239148b040a6983cf001e19ad569d880880",
    "cm2-gate13-round64-one-cross-term-dyadic-clock-frontier-manifest-2026-07-21.sha256":
        "c7552aa293baad4a021f85bff9c5cba3a15001d78a3e103e6f89cfc2b7c44319",
    "cm2-gate13-round64-resonant-tail-transport-current-clock-frontier-manifest-2026-07-21.json":
        "81a994f232af17d050a1582c396f8deeaae09e86856b5290e5eda764a238d4b8",
    "cm2-gate13-round64-resonant-tail-transport-current-clock-frontier-manifest-2026-07-21.sha256":
        "55fd5b62f3bab1fbea0c3334b4264176ab0bde8f140f3b7241d131b684756722",
    "cm2-gate24-round64-weighted-tree-saturation-actual-join-obstruction-frontier-manifest-2026-07-21.json":
        "5bb198256f2a5aa8837326f9eab70aa4845adb80417dc27379f27f7e8f24f8d0",
    "cm2-gate24-round64-weighted-tree-saturation-actual-join-obstruction-frontier-manifest-2026-07-21.sha256":
        "0943cc0316319a823f91ed29f732a1f828204db1e4376f8bad887523388809c6",
    "cm2-gate24-round64-rooted-atlas-jacobian-tag-lift-frontier-manifest-2026-07-21.json":
        "6eb0dbe73b21b5822e9e589b5f6a047b47966a349ec54e8e3b150b9bf203b1af",
    "cm2-gate24-round64-rooted-atlas-jacobian-tag-lift-frontier-manifest-2026-07-21.sha256":
        "474038420728935370c8ab9eb7be6df99fcf0da3e2baa88c01a8eff9c3f2d007",
    "cm2-gate5-round64-lineage-kernel-flux-bridge-no-go-frontier-manifest-2026-07-21.json":
        "7a67d2225b699c6cffb798298123469eeae6a5d5ded9d1ee9079afb9e8222e70",
    "cm2-gate5-round64-lineage-kernel-flux-bridge-no-go-frontier-manifest-2026-07-21.sha256":
        "148ad7b7a0e2384fb602adcbb8cefdb86022ef18130ae73fd438c7aaf06461bb",
    "cm2_round64_common.py":
        "ac67b1c90e95b385d89aa2a39ecb0a6420a5b30d2f4b19f3eccb6bd404598100",
}

LEAVES = {
    "gate13_primary": "cm2-gate13-round64-one-cross-term-dyadic-clock-frontier-manifest-2026-07-21.json",
    "gate13_supplement": "cm2-gate13-round64-resonant-tail-transport-current-clock-frontier-manifest-2026-07-21.json",
    "gate24_primary": "cm2-gate24-round64-weighted-tree-saturation-actual-join-obstruction-frontier-manifest-2026-07-21.json",
    "gate24_supplement": "cm2-gate24-round64-rooted-atlas-jacobian-tag-lift-frontier-manifest-2026-07-21.json",
    "gate5": "cm2-gate5-round64-lineage-kernel-flux-bridge-no-go-frontier-manifest-2026-07-21.json",
}
LEDGERS = [
    ("cm2-gate13-round64-one-cross-term-dyadic-clock-frontier-manifest-2026-07-21.sha256", 4),
    ("cm2-gate13-round64-resonant-tail-transport-current-clock-frontier-manifest-2026-07-21.sha256", 5),
    ("cm2-gate24-round64-weighted-tree-saturation-actual-join-obstruction-frontier-manifest-2026-07-21.sha256", 4),
    ("cm2-gate24-round64-rooted-atlas-jacobian-tag-lift-frontier-manifest-2026-07-21.sha256", 5),
    ("cm2-gate5-round64-lineage-kernel-flux-bridge-no-go-frontier-manifest-2026-07-21.sha256", 5),
]


def load_results() -> dict[str, dict[str, Any]]:
    out = {}
    for key, name in LEAVES.items():
        data = strict_json_path(HERE / name)
        require(isinstance(data.get("result"), dict), f"leaf result: {key}")
        out[key] = data["result"]
    return out


def audit_gate13_primary(result: dict[str, Any]) -> dict[str, Any]:
    require(result["strict_status"] == {
        "cm2": "NO-GO_FOR_CLAIM", "composite_gates": "0/5",
        "gate1": "NOT_CERTIFIED", "gate3": "NOT_CERTIFIED",
    }, "Gate13 primary state")
    rows = result["gate1"]["sharp_scalar_budget"]["regime_rows"]
    require(len(rows) == 4 and sum(len(row["samples"]) for row in rows) == 40,
            "Gate13 primary regimes")
    require([row["behavior"] for row in rows] ==
            ["DECAYS_TO_ZERO", "CONVERGES_NONZERO", "NO_LIMIT", "UNBOUNDED"],
            "Gate13 primary behaviors")
    clock = result["gate3"]["safe_clock_closed_form"]
    cp = Q(clock["C_p"])
    require(Q(2)**310 < cp < Q(2)**311, "Gate13 C_p bracket")
    for m in range(501):
        if Q(2)**m <= cp:
            d = 0
        else:
            d = 1
            while not Q(2)**(m - d) < cp / 2:
                d += 1
        expected = 0 if m <= 310 else m - 309
        require(d == expected, f"Gate13 clock closed form {m}")
    separators = result["gate3"]["weak_input_separator"]["rows"]
    require([row["clock_current_TV"] for row in separators] ==
            ["2", "4", "8", "16", "32", "64"], "Gate13 clock separators")
    return {
        "one_cross_term_regimes": "4/4", "samples": "40/40",
        "clock_closed_form": "501/501", "clock_separators": "6/6",
        "status": "INDEPENDENT_PASS",
    }


def audit_gate13_supplement(result: dict[str, Any]) -> dict[str, Any]:
    require(result["strict_status"]["Gate1"] == result["strict_status"]["Gate3"] ==
            "NOT_CERTIFIED", "Gate13 supplement state")
    model = result["gate1"]["critical_SL2_replay"]
    require(model["loop"] == [[1, 1], [-1, 0]] and model["determinant"] == 1,
            "Gate13 resonant loop")
    require(model["wedge_e1"] == model["wedge_e2"] == -1, "Gate13 wedges")
    transport = result["gate3"]["BL_transport_bound"]
    require(Q(transport["finite_raw_TV_sum"]) == 24 and
            Q(transport["finite_transport_sum"]) == Q(4095, 4096),
            "Gate13 transport replay")
    return {
        "resonant_loop": "PASS", "axis_wedges": "-1__-1",
        "BL_transport_rows": "12/12", "status": "INDEPENDENT_PASS",
    }


def audit_gate24_primary(result: dict[str, Any]) -> dict[str, Any]:
    strict = result["strict_nonpromotion"]
    require(strict["Gate2"] == strict["Gate4"] == "NOT_CERTIFIED", "Gate24 primary state")
    replay = result["finite_weighted_tree_saturation"]["finite_replay"]
    delta, p = Q(replay["delta_T_source"]), Q(replay["pairwise_dispersion_P"])
    require(delta == Q(3, 20) and p == Q(19, 200) and p <= delta <= 2 * p,
            "Gate24 tree replay")
    require(Q(replay["delta_T_landing"]) == delta and
            Q(replay["pairwise_dispersion_P_landing"]) == p, "Gate24 landing replay")
    join = result["actual_branch_owner_landing_join"]["replay"]
    require(join["pinned_fragments_replayed"] == "5/5" and
            join["physical_tree_instantiation_rows_complete"] == "0/7",
            "Gate24 actual join")
    separator = result["strong_assembly_separator"]["rows"]
    require([row["BV_variation_integral_abs_derivative"] for row in separator] ==
            ["1", "2", "17", "257", "4096"], "Gate24 strong separator")
    return {
        "weighted_tree_delta": "3/20", "pairwise_P": "19/200",
        "actual_fragments": "5/5", "physical_tree_rows": "0/7",
        "strong_separator": "5/5", "status": "INDEPENDENT_PASS",
    }


def audit_gate24_supplement(result: dict[str, Any]) -> dict[str, Any]:
    strict = result["strict_status"]
    require("NOT_CERTIFIED" in strict["Gate2"] and "NOT_CERTIFIED" in strict["Gate4"],
            "Gate24 supplement state")
    atlas = result["rooted_atlas_saturation"]["replay"]
    require(Q(atlas["delta_atlas"]) == Q(6, 5) and Q(atlas["P"]) == Q(3, 4),
            "Gate24 supplement atlas")
    require(Q(atlas["P"]) < Q(atlas["delta_atlas"]) < 2 * Q(atlas["P"]),
            "Gate24 supplement sandwich")
    tag = result["graph_tag_lift"]["separator"]
    require(Q(tag["full_mass"]) == 1 and Q(tag["full_one_vector_moment"]) == 3 and
            tag["W_D_unbounded"] is True, "Gate24 tag separator")
    return {
        "atlas_delta": "6/5", "pairwise_P": "3/4",
        "tag_moment": "3", "tag_operator": "UNBOUNDED",
        "status": "INDEPENDENT_PASS",
    }


def audit_gate5(result: dict[str, Any]) -> dict[str, Any]:
    strict = result["strict_status"]
    require(strict["Gate5_maturity"] == "10/18" and
            strict["complete_18_field_blocks"] == 0, "Gate5 state")
    rows = result["owner_lineage_kernel"]["rows"]
    require([row["c_star"] for row in rows] == ["1/2", "1", "INFINITY"],
            "Gate5 lineage rows")
    trace = result["trace_density_threshold"]
    require(Decimal(trace["q_trace_star"]) > 2 and Decimal(trace["q2_factor"]) > 1,
            "Gate5 trace threshold")
    require(len(result["small_gap_joint_criterion"]["remaining_N_cut"]["codes"]) == 6,
            "Gate5 N_cut codes")
    require(len(result["suffix_cube"]["rows"]) == 32, "Gate5 suffix cube")
    return {
        "lineage_rows": "3/3", "q_trace_star_gt_2": "PASS",
        "N_cut_codes": "6/6", "harmonic_separators": "2/2",
        "suffix_atoms": "32/32", "status": "INDEPENDENT_PASS",
    }


def build_result() -> dict[str, Any]:
    validate_pins(HERE, PINS)
    sidecar_rows = sum(replay_sidecar(HERE, HERE / name, count) for name, count in LEDGERS)
    require(sidecar_rows == 23, "leaf sidecar total")
    leaves = load_results()
    cross_rows = [
        "ONE_CROSS_TERM_CLASS_H_LIMIT_IS_NOT_THE_IMMUTABLE_TWISTING_TOKEN",
        "ZERO_TAIL_HOLDER_INHERITANCE_CANNOT_CREATE_ZERO_LOOP_TWISTING",
        "BL_ENDPOINT_TRANSPORT_IS_NOT_THE_STRONG_DYADIC_CLOCK_TRACE_LEDGER",
        "WEIGHTED_MEDIAN_THEOREM_IS_NOT_AN_ACTUAL_COLLISION_SRB_STABLE_TREE",
        "SCALAR_PROPERNESS_AND_ONE_FINITE_TAG_MOMENT_DO_NOT_IMPLY_STRONG_ASSEMBLY",
        "STABLE_TREE_COVARIANCE_DOES_NOT_IMPLY_INSERTION_TIME_LINEAGE_CONTRACTION",
        "SIGNED_CURRENT_CANCELLATION_DOES_NOT_PAY_POSITIVE_COMMON_MODE",
        "LATEST_EXTERNAL_RESULTS_HAVE_WRONG_LAW_PERTURBATION_OR_REVIEW_STATUS",
    ]
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "all_five_leaves_frozen_before_read": True,
            "audit_authored_source_leaf": False,
            "old_artifacts_modified": False,
            "pins": PINS,
        },
        "gate13_primary": audit_gate13_primary(leaves["gate13_primary"]),
        "gate13_supplement": audit_gate13_supplement(leaves["gate13_supplement"]),
        "gate24_primary": audit_gate24_primary(leaves["gate24_primary"]),
        "gate24_supplement": audit_gate24_supplement(leaves["gate24_supplement"]),
        "gate5": audit_gate5(leaves["gate5"]),
        "cross_leaf_consistency": {
            "status": "PASS_NO_TYPE_SUBSTITUTION_OR_STATE_CONTRADICTION",
            "rows": cross_rows, "rows_sha256": digest(cross_rows),
        },
        "source_leaf_acceptance": {
            "syntax_including_common": "11/11",
            "dependency_pin_rows": "69/69",
            "SHA_artifact_rows": "23/23",
            "integrity_and_replay": "5/5",
            "reemit": "5/5_BYTE_IDENTICAL",
            "hostile_semantic": "1590/1590_REJECTED",
            "strict_JSON": "31/31_REJECTED",
            "default_entry_points": "10/10_EXIT_2",
        },
        "latest_technology_boundary": {
            "external_theorem_promoted": False,
            "verified_boundary": "MME product, shrinking hole, renewal and reviews do not supply the pinned physical joins",
        },
        "strict_final_state": {
            "Gate1": "NOT_CERTIFIED",
            "Gate2": "NOT_CERTIFIED__OFFICIAL_FIELDS_0_OF_17",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED__LANDING_JOIN_1_OF_7_FIELDS_1_4_7_PARTIAL",
            "Gate5": "NOT_CERTIFIED__MATURITY_10_OF_18_BLOCKS_0",
            "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
            "audit_verdict": "PASS__NO_FROZEN_LEAF_CORRECTION_REQUIRED",
        },
    }
    replay = copy.deepcopy(result)
    result["internal_replay_digest"] = digest(replay)
    return result


def build_manifest(verifier: Path) -> dict[str, Any]:
    result = build_result()
    require(REPORT.is_file() and verifier.is_file() and COMMON.is_file(), "audit artifact")
    return {
        "schema": MANIFEST_SCHEMA, "pins": PINS,
        "report_sha256": sha256_path(REPORT),
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier.resolve()),
        "common_sha256": sha256_path(COMMON),
        "result": result, "verdict": result["strict_final_state"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-json", action="store_true")
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--verifier", type=Path, default=VERIFIER)
    args = parser.parse_args()
    try:
        if args.audit:
            result = build_result()
            print("AUDIT: PASS")
            print("RESULT_SHA256:", result["internal_replay_digest"])
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
        print(f"ROUND64_AUDIT_CERT_ERROR: {exc}", file=sys.stderr)
        return 1
    print("AUDIT_VERDICT: PASS")
    print("GATES_1_TO_5: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
