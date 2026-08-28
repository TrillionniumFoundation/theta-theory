#!/usr/bin/env python3
"""Independent verifier for the Round-65 aggregate core-frontier audit."""

from __future__ import annotations

import argparse
import copy
import json
import subprocess
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round65_common import (
    CertError, digest, replay_sidecar, require, semantic_mutation_test,
    sha256_path, strict_json_path, strict_json_self_test, validate_pins,
)


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.round65-independent-core-frontier-audit.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-round65-independent-core-frontier-audit"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
SIDECAR = HERE / f"{PREFIX}-manifest-2026-07-21.sha256"
REPORT = HERE / f"{PREFIX}-2026-07-21.md"
CERT = HERE / "cm2_round65_independent_core_frontier_audit_cert.py"
VERIFIER = Path(__file__).resolve()
COMMON = HERE / "cm2_round65_common.py"
EXPECTED_RESULT_DIGEST = "b5df189e2812dde3468435873d4e3f472dfb964fa73c17d272e01cd1524f07b2"

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
        "all_four_leaves_frozen_before_audit": True,
        "audit_authored_source_leaf": False,
        "old_artifacts_modified": False,
        "pins": PINS,
    }, "provenance")
    require(result["gate13"] == {
        "typing_rows": "5/5_FALSE_SUBSTITUTION", "two_plaque_rows": "8/8",
        "four_wedge_models": "2/2", "trace_rows": "6/6",
        "Piola_rows": "7/7", "stopped_rows": "6/6",
        "status": "INDEPENDENT_PASS",
    }, "Gate13 audit")
    require(result["gate24"] == {
        "actual_tree_rows": "0/7", "P_eta": "19/80", "delta_eta": "2/5",
        "first_failure_replays": "2/2", "BV_separator_rows": "5/5",
        "trace_factorisation": "NO_GO_PASS", "status": "INDEPENDENT_PASS",
    }, "Gate24 audit")
    require(result["gate5"] == {
        "live_arrival_rows": "3/3", "sector_rows": "7/7",
        "raw_separator_rows": "16/16", "cemetery_replay": "PASS",
        "oriented_bridge": "PASS", "open_fields": "8/8",
        "status": "INDEPENDENT_PASS",
    }, "Gate5 audit")
    require(result["cross_gate"] == {
        "path_potential_iff": "PASS", "time_rows": "12/12",
        "tag_rows": "12/12", "one_vector_charge": "6",
        "operator": "UNBOUNDED", "status": "INDEPENDENT_PASS",
    }, "cross audit")
    cross = result["cross_leaf_consistency"]
    require(cross["status"] == "PASS_NO_TYPE_SUBSTITUTION_OR_STATE_CONTRADICTION" and
            len(cross["rows"]) == 10 and digest(cross["rows"]) == cross["rows_sha256"],
            "cross consistency")
    require(result["source_leaf_acceptance"] == {
        "new_python_syntax_including_round65_common": "9/9",
        "dependency_pin_rows": "84/84",
        "SHA_artifact_rows": "19/19",
        "integrity_replay_reemit": "4/4",
        "hostile_semantic": "1148/1148_REJECTED",
        "strict_JSON": "16/16_REJECTED",
        "default_entry_points": "8/8_EXIT_2",
    }, "source acceptance")
    require(result["latest_technology_boundary"]["external_theorem_promoted"] is False,
            "technology guard")
    require(result["strict_final_state"] == {
        "Gate1": "NOT_CERTIFIED",
        "Gate2": "NOT_CERTIFIED__OFFICIAL_FIELDS_0_OF_17",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED__LANDING_JOIN_1_OF_7_FIELDS_1_4_7_PARTIAL",
        "Gate5": "NOT_CERTIFIED__MATURITY_10_OF_18_BLOCKS_0",
        "complete_composite_gates": "0/5",
        "CM2": "NO-GO_FOR_CLAIM",
        "audit_verdict": "PASS__NO_SOURCE_LEAF_CORRECTION_REQUIRED",
    }, "strict state")


def independent_replay() -> dict[str, Any]:
    # Gate 1 full-wedge replay.
    a = b = u = Q(1)
    l = Q(-1, 2)
    loop = [[a * b, a * u], [l * b, l * u + Q(1, a * b)]]
    wedges = [-l * b, a * b, -(l * u + Q(1, a * b)), a * u]
    require(loop == [[Q(1), Q(1)], [Q(-1, 2), Q(1, 2)]] and
            all(value != 0 for value in wedges), "independent wedge")

    # Gate 2/4 finite outer-law sandwich and all-depth limits.
    require(Q(19, 80) <= Q(2, 5) <= 2 * Q(19, 80), "independent median sandwich")
    failure_good = sum((Q(1, 2**(n + 2)) for n in range(1, 200)), Q(0))
    require(failure_good < Q(1, 4), "independent positive survivor prefix")
    require(Q(1, 2**200) > 0, "independent finite-depth positive")

    # Gate 5 live/arrival and raw-sector boundary.
    ratios = [Q(1 + 1, 4), Q(1 + 0, 2)]
    require(max(ratios) == Q(1, 2), "independent split")
    raw_prefix = sum((Q(2) for _ in range(40)), Q(0))
    require(raw_prefix == 80, "independent raw divergence prefix")

    # Cross-gate conditional potential separator.
    tag_moment_prefix = sum((Q(3, 2**n) for n in range(1, 200)), Q(0))
    time_charge_prefix = sum((Q(3, 2**j) for j in range(200)), Q(0))
    require(tag_moment_prefix < 3 and time_charge_prefix < 6,
            "independent positive potential prefix")
    return {
        "wedge": "PASS", "median": "PASS", "all_depth": "PASS",
        "split": "PASS", "raw_prefix": "80",
        "positive_potential": "PASS", "status": "PASS",
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
            print("AUDIT_MODE: PASS")
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
                cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=240,
            )
            require(proc.returncode == 0, "reemit producer")
            args.reemit.write_bytes(proc.stdout)
            require(args.reemit.read_bytes() == MANIFEST.read_bytes(), "reemit bytes")
            return 0
    except (CertError, OSError, ValueError, KeyError, TypeError, ArithmeticError,
            subprocess.SubprocessError) as exc:
        print(f"ROUND65_AUDIT_VERIFY_ERROR: {exc}", file=sys.stderr)
        return 1
    print("ROUND65 AUDIT: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
