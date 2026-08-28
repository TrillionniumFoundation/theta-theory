#!/usr/bin/env python3
"""Independent verifier for the Round-68 common-root/all-gate certificate."""

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
from cm2_round68_common_root_all_gate_frontier_cert import build_result


HERE = Path(__file__).resolve().parent
PREFIX = "cm2-round68-common-root-all-gate-frontier"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
CERT = HERE / "cm2_round68_common_root_all_gate_frontier_cert.py"
VERIFIER = Path(__file__).resolve()
COMMON = HERE / "cm2_round68_common.py"
RESULT_SCHEMA = "cm2.round68.common-root-all-gate-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"


def integrity(data: dict[str, Any], check_files: bool = True) -> None:
    require(data["schema"] == MANIFEST_SCHEMA, "manifest schema")
    require(data["result"]["schema"] == RESULT_SCHEMA, "result schema")
    if check_files:
        validate_pins(HERE, data["pins"])
        require(data["report_sha256"] == sha256_path(REPORT), "report hash")
        require(data["certificate_sha256"] == sha256_path(CERT), "cert hash")
        require(data["verifier_sha256"] == sha256_path(VERIFIER), "verifier hash")
        require(data["common_sha256"] == sha256_path(COMMON), "common hash")
    replay = copy.deepcopy(data["result"])
    claimed = replay.pop("internal_replay_digest")
    require(claimed == digest(replay), "internal digest")
    require(data["verdict"] == data["result"]["strict_status"], "verdict")


def semantics(result: dict[str, Any]) -> None:
    require(result["provenance"] == {
        "append_only": True, "old_artifacts_modified": False,
        "pinned_round67_chain": {
            "cm2-sixty-seventh-direct-assault-2026-07-21.md": "fd47134878ae5fbc239ac2a648dd8dd074181162da88d4ba011fea9d98503b82",
            "cm2-sixty-seventh-direct-assault-manifest-2026-07-21.sha256": "a0f335e434caa65b1d9a99f9daf92dbb180f407cee1724e83aaabbe34fce27eb",
            "cm2-round67-independent-core-frontier-audit-manifest-2026-07-21.json": "95a08ffbb4ead8a56b43de95fb73756db9635adb7ca99a3bea65190a15c97d48",
        },
    }, "provenance")
    join = result["common_root_join"]
    require(join["status"] == "EXACT_JOIN_CRITERION_CERTIFIED__ACTUAL_CROSSWALK_ABSENT", "join status")
    require(len(join["required_fields"]) == 12 and len(set(join["required_fields"])) == 12, "join fields")
    require(join["actual_joined_fields"] == "0/12", "actual join")
    require(join["equal_marginals_sufficient"] is False and
            join["abstract_measure_isomorphism_sufficient"] is False and
            join["forgetful_key_equality_sufficient"] is False, "join negatives")
    separator = join["four_atom_separator"]
    require(sorted(separator["left_key_multiset"]) == list(range(4)), "left marginal")
    require(sorted(separator["right_key_multiset"]) == list(range(4)), "right marginal")
    require(len(separator["atoms"]) == 4 and all(not row["diagonal"] for row in separator["atoms"]), "off diagonal")
    require(sum(Q(row["mass"]) for row in separator["atoms"]) == 1, "separator mass")
    require(separator["diagonal_graph_mass"] == "0", "diagonal mass")

    gate13 = result["gate13_uniform_frontier"]
    require(gate13["actual_contract_rows"] == "0/5" and len(gate13["sufficient_contract"]) == 5, "gate13 contract")
    require(gate13["finite_selection_separator"] == {
        "construction": "depth_n_has_one_unobserved_cell_with_unit_error",
        "every_fixed_selected_cell_eventually_zero": True,
        "uniform_error_each_depth": "1",
        "uniform_convergence": False,
    }, "finite separator")
    require(len(gate13["perturbation_rows"]) == 12, "perturbation count")
    for row in gate13["perturbation_rows"]:
        n = row["n"]
        delta_a, delta_b = Q(1, 2**n), Q(1, 3**n)
        require(Q(row["delta_A"]) == delta_a and Q(row["delta_B"]) == delta_b, "deltas")
        require(Q(row["product_error_bound"]) == 2 * delta_a + 3 * delta_b + delta_a * delta_b, "product bound")

    gate24 = result["gate24_tail_frontier"]
    require(len(gate24["hazard_rows"]) == 16, "hazard count")
    square, harmonic = Q(1), Q(1)
    for row in gate24["hazard_rows"]:
        n = row["n"]
        square *= 1 - Q(1, (n + 1) ** 2)
        harmonic *= 1 - Q(1, n + 1)
        require(Q(row["square_survival"]) == square == Q(n + 2, 2 * (n + 1)), "square survival")
        require(Q(row["harmonic_survival"]) == harmonic == Q(1, n + 1), "harmonic survival")
    require(gate24["square_limit"] == "1/2" and gate24["harmonic_limit"] == "0", "hazard limits")
    require(gate24["actual_full_hazard_rows"] == "0" and gate24["gate2_official_fields"] == "0/17", "gate24 actual")
    variation = gate24["alternating_variation_separator"]
    require(variation["increments_tend_to_zero"] is True and variation["total_absolute_variation"] == "infinity", "variation separator")

    gate5 = result["gate5_positive_potential_frontier"]
    require(len(gate5["required_sectors"]) == 7 and len(set(gate5["required_sectors"])) == 7, "gate5 sectors")
    require(Q(gate5["charge_weight"]) * Q(gate5["attenuated_example"]["beta"]) == Q(1, 2), "attenuated ratio")
    require(Q(gate5["attenuated_example"]["total_potential"]) == 2, "attenuated total")
    require(Q(gate5["charge_weight"]) * Q(gate5["critical_example"]["beta"]) == 1, "critical ratio")
    require(gate5["critical_example"]["total_potential"] == "infinity", "critical divergence")
    require(gate5["actual_new_sectors_closed"] == "0/7" and
            gate5["conditional_terminal_killing_equals_deterministic_eligibility"] is False and
            gate5["finite_integrated_charge_implies_L_infinity_operator_bound"] is False, "gate5 negatives")

    technology = result["technology_boundary"]
    require(technology["checked_on"] == "2026-07-21" and len(technology["queries"]) == 4, "technology search")
    require(technology["new_same_law_moving_billiard_response_theorem_found"] is False and
            technology["external_theorem_promoted"] is False, "technology boundary")
    require(result["strict_status"] == {
        "Gate1": "NOT_CERTIFIED",
        "Gate2": "NOT_CERTIFIED__OFFICIAL_FIELDS_0_OF_17",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED__LANDING_JOIN_1_OF_7",
        "Gate5": "NOT_CERTIFIED__MATURITY_10_OF_18_BLOCKS_0",
        "complete_composite_gates": "0/5",
        "CM2": "NO-GO_FOR_CLAIM",
    }, "strict status")
    require(result == build_result(), "canonical full-result semantics")


def independent_replay() -> dict[str, Any]:
    square = Q(1)
    harmonic = Q(1)
    for n in range(1, 400):
        square *= 1 - Q(1, (n + 1) ** 2)
        harmonic *= 1 - Q(1, n + 1)
    require(square == Q(401, 800) and harmonic == Q(1, 400), "long hazard replay")
    partial = sum((Q(1, 2) ** n for n in range(300)), Q(0))
    require(partial < 2 and 2 - partial == Q(1, 2**299), "resolvent replay")
    harmonic_abs = sum((Q(1, n) for n in range(1, 400)), Q(0))
    require(harmonic_abs > 6, "variation divergence witness")
    return {"hazard_rows": "798/798", "resolvent_terms": "300/300", "status": "PASS"}


def deterministic(data: dict[str, Any]) -> None:
    proc = subprocess.run(
        [sys.executable, str(CERT), "--manifest-json", "--verifier", str(VERIFIER)],
        cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=180,
    )
    require(proc.returncode == 0, f"producer: {proc.stderr.decode().strip()}")
    require(proc.stdout == MANIFEST.read_bytes() and strict_json_path(MANIFEST) == data, "deterministic producer")


def run_audit(data: dict[str, Any], regenerate: bool = True) -> None:
    integrity(data)
    semantics(data["result"])
    independent_replay()
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
                cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=180,
            )
            require(proc.returncode == 0, "reemit producer")
            args.reemit.write_bytes(proc.stdout)
            require(args.reemit.read_bytes() == MANIFEST.read_bytes(), "reemit bytes")
            return 0
    except (CertError, OSError, ValueError, KeyError, TypeError, ArithmeticError,
            subprocess.SubprocessError) as exc:
        print(f"ROUND68_VERIFY_ERROR: {exc}", file=sys.stderr)
        return 1
    print("ROUND68 COMMON ROOT AND ALL GATES: FRONTIER_ONLY")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
