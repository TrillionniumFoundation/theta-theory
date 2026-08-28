#!/usr/bin/env python3
"""Independent verifier for the Round-64 five-leaf core-frontier audit."""

from __future__ import annotations

import argparse
import copy
import json
import subprocess
import sys
from decimal import Decimal
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round64_common import (
    CertError, digest, replay_sidecar, require, semantic_mutation_test,
    sha256_path, strict_json_path, strict_json_self_test, validate_pins,
)


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.round64-independent-core-frontier-audit.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-round64-independent-core-frontier-audit"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
SIDECAR = HERE / f"{PREFIX}-manifest-2026-07-21.sha256"
REPORT = HERE / f"{PREFIX}-2026-07-21.md"
CERT = HERE / "cm2_round64_independent_core_frontier_audit_cert.py"
VERIFIER = Path(__file__).resolve()
COMMON = HERE / "cm2_round64_common.py"
EXPECTED_RESULT_DIGEST = "3237660d14a407a3c7a4ce9a62ab18b695b980d6ce135e6a1a6fcc7ab4503b5f"

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


def integrity(data: dict[str, Any], files: bool = True) -> None:
    if files:
        validate_pins(HERE, PINS)
    require(data.get("schema") == MANIFEST_SCHEMA and data.get("pins") == PINS,
            "manifest schema/pins")
    if files:
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
    require(data.get("verdict") == result.get("strict_final_state"), "verdict alias")


def semantics(result: dict[str, Any]) -> None:
    require(result["schema"] == RESULT_SCHEMA, "result schema")
    require(result["provenance"] == {
        "all_five_leaves_frozen_before_read": True,
        "audit_authored_source_leaf": False,
        "old_artifacts_modified": False,
        "pins": PINS,
    }, "provenance")
    require(result["gate13_primary"] == {
        "one_cross_term_regimes": "4/4", "samples": "40/40",
        "clock_closed_form": "501/501", "clock_separators": "6/6",
        "status": "INDEPENDENT_PASS",
    }, "Gate13 primary audit")
    require(result["gate13_supplement"] == {
        "resonant_loop": "PASS", "axis_wedges": "-1__-1",
        "BL_transport_rows": "12/12", "status": "INDEPENDENT_PASS",
    }, "Gate13 supplement audit")
    require(result["gate24_primary"] == {
        "weighted_tree_delta": "3/20", "pairwise_P": "19/200",
        "actual_fragments": "5/5", "physical_tree_rows": "0/7",
        "strong_separator": "5/5", "status": "INDEPENDENT_PASS",
    }, "Gate24 primary audit")
    require(result["gate24_supplement"] == {
        "atlas_delta": "6/5", "pairwise_P": "3/4",
        "tag_moment": "3", "tag_operator": "UNBOUNDED",
        "status": "INDEPENDENT_PASS",
    }, "Gate24 supplement audit")
    require(result["gate5"] == {
        "lineage_rows": "3/3", "q_trace_star_gt_2": "PASS",
        "N_cut_codes": "6/6", "harmonic_separators": "2/2",
        "suffix_atoms": "32/32", "status": "INDEPENDENT_PASS",
    }, "Gate5 audit")
    cross = result["cross_leaf_consistency"]
    require(cross["status"] == "PASS_NO_TYPE_SUBSTITUTION_OR_STATE_CONTRADICTION" and
            len(cross["rows"]) == 8 and digest(cross["rows"]) == cross["rows_sha256"],
            "cross-leaf rows")
    require(result["source_leaf_acceptance"] == {
        "syntax_including_common": "11/11",
        "dependency_pin_rows": "69/69",
        "SHA_artifact_rows": "23/23",
        "integrity_and_replay": "5/5",
        "reemit": "5/5_BYTE_IDENTICAL",
        "hostile_semantic": "1590/1590_REJECTED",
        "strict_JSON": "31/31_REJECTED",
        "default_entry_points": "10/10_EXIT_2",
    }, "source acceptance")
    require(result["latest_technology_boundary"]["external_theorem_promoted"] is False,
            "external theorem guard")
    require(result["strict_final_state"] == {
        "Gate1": "NOT_CERTIFIED",
        "Gate2": "NOT_CERTIFIED__OFFICIAL_FIELDS_0_OF_17",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED__LANDING_JOIN_1_OF_7_FIELDS_1_4_7_PARTIAL",
        "Gate5": "NOT_CERTIFIED__MATURITY_10_OF_18_BLOCKS_0",
        "complete_composite_gates": "0/5",
        "CM2": "NO-GO_FOR_CLAIM",
        "audit_verdict": "PASS__NO_FROZEN_LEAF_CORRECTION_REQUIRED",
    }, "strict state")


def source_result(name: str) -> dict[str, Any]:
    data = strict_json_path(HERE / name)
    require(isinstance(data.get("result"), dict), f"source result: {name}")
    return data["result"]


def source_replays() -> dict[str, Any]:
    g13 = source_result(
        "cm2-gate13-round64-one-cross-term-dyadic-clock-frontier-manifest-2026-07-21.json"
    )
    regimes = g13["gate1"]["sharp_scalar_budget"]["regime_rows"]
    require([Q(row["q_cross"]) for row in regimes] == [Q(1, 2), Q(1), Q(1), Q(2)],
            "source Gate13 regimes")
    require(sum(len(row["samples"]) for row in regimes) == 40, "source Gate13 samples")
    clock = g13["gate3"]["safe_clock_closed_form"]
    require(Q(2)**310 < Q(clock["C_p"]) < Q(2)**311, "source Gate13 clock")

    g13s = source_result(
        "cm2-gate13-round64-resonant-tail-transport-current-clock-frontier-manifest-2026-07-21.json"
    )
    require(g13s["gate1"]["critical_SL2_replay"]["loop"] == [[1, 1], [-1, 0]],
            "source Gate13 resonant loop")
    require(Q(g13s["gate3"]["BL_transport_bound"]["finite_transport_sum"]) ==
            Q(4095, 4096), "source Gate13 transport")

    g24 = source_result(
        "cm2-gate24-round64-weighted-tree-saturation-actual-join-obstruction-frontier-manifest-2026-07-21.json"
    )
    tree = g24["finite_weighted_tree_saturation"]["finite_replay"]
    require(Q(tree["pairwise_dispersion_P"]) <= Q(tree["delta_T_source"]) <=
            2 * Q(tree["pairwise_dispersion_P"]), "source Gate24 tree")
    require(g24["actual_branch_owner_landing_join"]["replay"]
            ["physical_tree_instantiation_rows_complete"] == "0/7", "source Gate24 join")

    g24s = source_result(
        "cm2-gate24-round64-rooted-atlas-jacobian-tag-lift-frontier-manifest-2026-07-21.json"
    )
    atlas = g24s["rooted_atlas_saturation"]["replay"]
    require(Q(atlas["delta_atlas"]) == Q(6, 5) and Q(atlas["P"]) == Q(3, 4),
            "source Gate24 supplement")

    g5 = source_result(
        "cm2-gate5-round64-lineage-kernel-flux-bridge-no-go-frontier-manifest-2026-07-21.json"
    )
    require([row["c_star"] for row in g5["owner_lineage_kernel"]["rows"]] ==
            ["1/2", "1", "INFINITY"], "source Gate5 lineage")
    require(Decimal(g5["trace_density_threshold"]["q_trace_star"]) > 2 and
            len(g5["suffix_cube"]["rows"]) == 32, "source Gate5 threshold/suffix")
    return {
        "gate13_regimes_samples": "4/40",
        "gate13_clock_bracket": "PASS",
        "gate13_transport": "4095/4096",
        "gate24_tree": "PASS",
        "gate24_supplement": "PASS",
        "gate5_lineage_threshold_suffix": "PASS",
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
    source_replays()
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
            print("AUDIT_MODE: PASS")
            return 0
        if args.replay:
            integrity(data)
            semantics(data["result"])
            print(json.dumps(source_replays(), sort_keys=True))
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
                cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=240,
            )
            require(proc.returncode == 0, "reemit producer")
            args.reemit.write_bytes(proc.stdout)
            require(args.reemit.read_bytes() == MANIFEST.read_bytes(), "reemit bytes")
            return 0
    except (CertError, OSError, ValueError, KeyError, TypeError, ArithmeticError,
            subprocess.SubprocessError) as exc:
        print(f"ROUND64_AUDIT_VERIFY_ERROR: {exc}", file=sys.stderr)
        return 1
    print("AUDIT_VERDICT: PASS")
    print("GATES_1_TO_5: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
