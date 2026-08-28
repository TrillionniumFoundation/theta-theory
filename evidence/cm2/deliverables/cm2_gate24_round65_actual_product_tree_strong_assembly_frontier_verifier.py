#!/usr/bin/env python3
"""Independent verifier for the Round-65 Gate-2/4 frontier leaf."""

from __future__ import annotations

import argparse
import copy
import json
import subprocess
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round64_common import (
    CertError, digest, replay_sidecar, require, semantic_mutation_test,
    sha256_path, strict_json_path, strict_json_self_test, validate_pins,
)


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate24.round65.actual-product-tree-strong-assembly-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-gate24-round65-actual-product-tree-strong-assembly-frontier"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
SIDECAR = HERE / f"{PREFIX}-manifest-2026-07-21.sha256"
REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
CERT = HERE / "cm2_gate24_round65_actual_product_tree_strong_assembly_frontier_cert.py"
VERIFIER = Path(__file__).resolve()
EXPECTED_PINS_DIGEST = "c2124672dfb279f23017acbb80c3369699e62bbb12ad673490517b6d923072ed"
EXPECTED_RESULT_DIGEST = "b0d5b42f78c085281f7d2f9da1b3cd3e84d1ffc385edc94ec51d51de07075061"


def integrity(data: dict[str, Any], files: bool = True) -> None:
    require(data.get("schema") == MANIFEST_SCHEMA, "manifest schema")
    pins = data.get("pins")
    require(isinstance(pins, dict) and digest(pins) == EXPECTED_PINS_DIGEST,
            "pinned dependency set")
    if files:
        validate_pins(HERE, pins)
        require(data.get("report_sha256") == sha256_path(REPORT), "report hash")
        require(data.get("certificate_sha256") == sha256_path(CERT), "cert hash")
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

    plaque = result["standard_Borel_plaque_law_saturation"]
    require(plaque["status"] ==
            "CERTIFIED_EXACT_STANDARD_BOREL_PLAQUE_LAW_INTERFACE__ACTUAL_TRIVIALISATION_ABSENT",
            "plaque-law status")
    require(plaque["sharp_sandwich"] == "P_eta<=delta_eta<=2*P_eta" and
            "P_eta=0" in plaque["zero_criterion"], "plaque theorem")
    p = plaque["finite_replay"]
    require(Q(p["delta_eta"]) == Q(2, 5) and Q(p["P_eta"]) == Q(19, 80) and
            p["strict_sandwich"] is True, "plaque replay values")
    require(plaque["actual_P_eta_zero"] == "NOT_CERTIFIED", "actual marker guard")

    depth = result["all_depth_stable_transform"]
    require(depth["status"] ==
            "CERTIFIED_EXACT_FIRST_FAILURE_CRITERION_AND_TWO_FINITE_DEPTH_NONIMPLICATIONS",
            "all-depth status")
    require(depth["good_first_failure_replay"]["infinite_survivor_mass"] == "3/4" and
            depth["positive_every_finite_depth_separator"]["infinite_survivor_mass"] == "0",
            "survivor limits")
    d97 = depth["depth97_separator"]
    require(d97["accepted_prefix_count"] == 96 and
            d97["first_unconstrained_depth"] == 97 and
            d97["sample"][-1] == {"depth": 97, "survives": False},
            "depth97 separator")
    require(depth["physical_all_depth_base"] == "NOT_CERTIFIED", "all-depth guard")

    actual = result["actual_product_tree_interface"]
    require(len(actual["rows"]) == 7 and actual["actual_rows_complete"] == "0/7",
            "actual interface count")
    require([row["row"] for row in actual["rows"]] == list(range(1, 8)),
            "actual interface row IDs")
    require(all(row["state"] != "CERTIFIED" for row in actual["rows"]),
            "no actual tree promotion")
    require("esssup_u" in actual["nonatomic_path_budget"], "nonatomic budget")

    strong = result["tag_graph_to_BV_strong_frontier"]
    require(strong["trace_factorisation_no_go"]["status"] ==
            "FALSE_BY_SMOOTH_EXACT_TRACE_SEPARATOR", "trace no-go")
    bridge = strong["countable_tagged_BV_bridge"]
    require(bridge["status"] == "CERTIFIED_CONDITIONAL_WEIGHTED_TAGGED_BV_LIFT" and
            "A_0+A_1" in bridge["bound"], "tagged BV bridge")
    sample = bridge["sample"]
    require(Q(sample["A_0"]) == 2 and Q(sample["A_1"]) == 3 and
            Q(sample["tagged_output_BV_norm"]) == Q(37, 6) and
            Q(sample["upper_bound"]) == Q(25, 2), "tagged BV sample")
    sep = strong["W_D_Linfinity_not_BV_separator"]
    require(all(row["W_D"] == "1" and
                int(row["weighted_kernel_variation"]) == 4 * row["N"]
                for row in sep["rows"]), "oscillatory kernel separator")
    require(strong["actual_weighted_kernel_A0_A1"] == "NOT_CERTIFIED" and
            strong["physical_Piola_intertwining_recipient"] == "NOT_CERTIFIED",
            "physical strong guards")

    tech = result["latest_technology_boundary"]
    require(tech["external_theorem_promoted"] is False and
            "boundaryless" in tech["arXiv_2604_25746v1"] and
            "MME" in tech["arXiv_2604_25881v1"], "technology type guards")
    require(result["strict_status"] == {
        "Gate2": "NOT_CERTIFIED__OFFICIAL_FIELDS_0_OF_17",
        "Gate4": "NOT_CERTIFIED__LANDING_JOIN_1_OF_7_FIELDS_1_4_7_PARTIAL",
        "actual_stable_tree_instantiation": "0/7",
        "complete_composite_gates": "0/5",
        "CM2": "NO-GO_FOR_CLAIM",
    }, "strict state")


def independent_replay() -> dict[str, Any]:
    weights = [Q(1, 10), Q(1, 5), Q(1, 5), Q(1, 4), Q(1, 4)]
    markers = [
        [0, 0, 1, 1], [0, 1, 1, 0], [1, 1, 0, 0],
        [0, 1, 0, 1], [1, 0, 1, 0],
    ]
    medians = [0, 1, 1, 0]
    delta = sum(
        (sum((weights[i] * abs(markers[i][x] - medians[x]) for i in range(5)), Q(0))
         for x in range(4)), Q(0)
    ) / 4
    pairwise = Q(0)
    for i in range(5):
        for j in range(i + 1, 5):
            distance = sum(abs(markers[i][x] - markers[j][x]) for x in range(4)) / Q(4)
            pairwise += weights[i] * weights[j] * distance
    require(delta == Q(2, 5) and pairwise == Q(19, 80), "independent plaque law")

    good_total = sum((Q(1, 2 ** (n + 2)) for n in range(1, 80)), Q(0))
    bad_total = sum((Q(1, 2**n) for n in range(1, 80)), Q(0))
    require(good_total < Q(1, 4) and bad_total < 1 and
            Q(1, 4) - good_total == Q(1, 2**81) and
            1 - bad_total == Q(1, 2**79), "first-failure tails")

    # k1=x, k2=1-x, weights 1 and 2, f=1+x.
    output = (Q(5, 6) + 2) + 2 * (Q(2, 3) + 1)
    f_bv = Q(3, 2) + 1
    require(output == Q(37, 6) and f_bv == Q(5, 2) and output <= 5 * f_bv,
            "independent tagged BV sample")
    return {"delta_eta": "2/5", "P_eta": "19/80",
            "all_depth": "PASS", "tagged_BV": "PASS"}


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
        print(f"ROUND65_GATE24_VERIFY_ERROR: {exc}", file=sys.stderr)
        return 1
    print("Gate2/Gate4: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
