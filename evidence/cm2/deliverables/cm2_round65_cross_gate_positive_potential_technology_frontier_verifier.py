#!/usr/bin/env python3
"""Independent verifier for the Round-65 cross-gate positive-potential leaf."""

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
RESULT_SCHEMA = "cm2.round65.cross-gate-positive-potential-technology.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-round65-cross-gate-positive-potential-technology-frontier"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
SIDECAR = HERE / f"{PREFIX}-manifest-2026-07-21.sha256"
REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
CERT = HERE / "cm2_round65_cross_gate_positive_potential_technology_frontier_cert.py"
VERIFIER = Path(__file__).resolve()
COMMON = HERE / "cm2_round65_common.py"
EXPECTED_RESULT_DIGEST = "c7546afdf62f16ca0a8158d75bce34910a6feb98559fcb2de29e1c53c8fd262d"

PINS = {
    "cm2-sixty-fourth-direct-assault-2026-07-21.md":
        "bbd52eed540e4e91566a7d0b9fda2b381b35860640e23a0a45d29b73fabb8b61",
    "cm2-sixty-fourth-direct-assault-manifest-2026-07-21.sha256":
        "5d2174cee61c0fdf5573dedaece38950c0261fe05aa835b66c4363d974e52932",
    "cm2-round64-independent-core-frontier-audit-manifest-2026-07-21.json":
        "e775720b2891146a39421d515280e119f42b075d0783650e879abe1370ff8779",
    "cm2-gate13-round64-one-cross-term-dyadic-clock-frontier-manifest-2026-07-21.json":
        "df730945a80aad801b5923729e5c8239148b040a6983cf001e19ad569d880880",
    "cm2-gate24-round64-rooted-atlas-jacobian-tag-lift-frontier-manifest-2026-07-21.json":
        "6eb0dbe73b21b5822e9e589b5f6a047b47966a349ec54e8e3b150b9bf203b1af",
    "cm2-gate5-round64-lineage-kernel-flux-bridge-no-go-frontier-manifest-2026-07-21.json":
        "7a67d2225b699c6cffb798298123469eeae6a5d5ded9d1ee9079afb9e8222e70",
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
    require(data.get("verdict") == result.get("strict_status"), "verdict alias")


def semantics(result: dict[str, Any]) -> None:
    require(result["schema"] == RESULT_SCHEMA, "result schema")
    require(result["provenance"] == {
        "append_only": True,
        "old_artifacts_modified": False,
        "pinned_round64_frontier": PINS,
    }, "provenance")

    theorem = result["positive_path_potential_theorem"]
    require(theorem["status"] == "CERTIFIED_EXACT_STANDARD_BOREL_INTERFACE",
            "theorem status")
    require(theorem["bounded_iff"] == "H in L_infinity(mu)", "bounded iff")
    require(theorem["operator_norm"] == "||A||=ess_sup_mu H", "operator norm")
    require(theorem["positive_equality"] is True, "positive equality")
    require(theorem["sector_sum_is_lawful_only_for_typed_positive_charges"] is True,
            "sector typing")
    require(theorem["signed_cancellation_pays_positive_norm"] is False,
            "signed cancellation guard")

    sep = result["two_factor_separator"]
    require(sep["status"] == "CERTIFIED_EXACT", "separator status")
    require(Q(sep["w"]) == Q(3, 2) and Q(sep["kappa"]) == Q(1, 3),
            "separator constants")
    require(Q(sep["w_times_kappa"]) == Q(1, 2), "separator contraction")
    require(Q(sep["full_mass"]) == 1 and Q(sep["one_time_actual_moment"]) == 3,
            "separator fixed vector")
    require(Q(sep["all_time_actual_one_vector_charge"]) == 6,
            "separator all-time vector")
    require(sep["conditional_potential"] == "H(n)=2^(n+1)" and
            sep["conditional_potential_unbounded"] is True, "separator potential")
    require(len(sep["time_rows"]) == 12 and len(sep["tag_rows"]) == 12,
            "separator rows")
    for row in sep["time_rows"]:
        j = row["j"]
        require(Q(row["survival"]) == Q(1, 3)**j, "time survival")
        require(Q(row["outer_times_survival"]) == Q(1, 2)**j,
                "time weighted survival")
        require(Q(row["weighted_one_vector_charge"]) == 3 * Q(1, 2)**j,
                "time vector charge")
    for row in sep["tag_rows"]:
        n = row["n"]
        require(Q(row["mu_mass"]) == Q(3, 4**n), "tag mass")
        require(Q(row["tag_weight"]) == Q(2**n), "tag weight")
        require(Q(row["one_time_moment_term"]) == Q(3, 2**n),
                "tag moment")
        require(Q(row["conditional_path_potential"]) == Q(2**(n + 1)),
                "tag path potential")
        require(Q(row["unit_L1_atom_lift_norm"]) == Q(2**(n + 1)),
                "tag atom norm")

    opposite = result["opposite_separator"]
    require(opposite["status"] == "CERTIFIED_EXACT" and
            opposite["potential"] == "sum_j w^j=infinity", "opposite separator")
    require(result["sharp_sufficient_interface"] == {
        "hypothesis": "P_(0:j)W_j(x)<=C kappa^j mu-a.e.; w kappa<1",
        "conclusion": "H(x)<=C/(1-w kappa)",
        "actual_joint_pointwise_estimate": "NOT_CERTIFIED",
    }, "sufficient interface")
    require(result["cemetery_typing"] == {
        "absorbing_occupancy_after_positive_arrival": "DIVERGES_FOR_W_GT_1",
        "lawful_positive_cemetery": "ONE_SHOT_ARRIVAL_LEDGER",
        "arrival_potential_L_infinity": "STILL_REQUIRED",
        "actual_pre_regularization_arrival_bound": "NOT_CERTIFIED",
    }, "cemetery typing")
    require(result["gate_crosswalk"] == {
        "Gate3": "POSITIVE_VARIATION_INTERFACE_ONLY__PHYSICAL_PIOLA_RQ_MTDQ_NOT_CERTIFIED",
        "Gate4": "ROUND64_W_D_L_INFINITY_IS_ONE_TIME_SPECIALIZATION__ALL_TIME_PATH_BOUND_NOT_CERTIFIED",
        "Gate5": "SAME_LABEL_MASS_CONTRACTION_ALONE_DOES_NOT_CONTROL_TAG_CURRENT_SECTOR_CHARGE",
    }, "gate crosswalk")
    tech = result["latest_technology_boundary"]
    require(tech["external_theorem_promoted"] is False, "external theorem guard")
    require("NO_BILLIARD_PIOLA" in tech["arxiv_2603_19509v3"], "nonautonomous boundary")
    require("FIXED_POINT_NOT_COLLISION" in tech["arxiv_2604_25746v1"], "SRB boundary")
    require("ASSUMES_MISSING" in tech["arxiv_2510_19573v3"], "kernel boundary")
    require("WRONG_PROCESS" in tech["arxiv_2605_07824"], "diffusion boundary")
    require(result["strict_status"] == {
        "Gate1": "NOT_CERTIFIED",
        "Gate2": "NOT_CERTIFIED__OFFICIAL_FIELDS_0_OF_17",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED__LANDING_JOIN_1_OF_7",
        "Gate5": "NOT_CERTIFIED__MATURITY_10_OF_18_BLOCKS_0",
        "complete_composite_gates": "0/5",
        "CM2": "NO-GO_FOR_CLAIM",
    }, "strict state")


def independent_replay() -> dict[str, Any]:
    one_time = sum((Q(3, 2**n) for n in range(1, 200)), Q(0))
    require(one_time < 3 and 3 - one_time == Q(3, 2**199), "finite tag prefix")
    all_time = sum((3 * Q(1, 2)**j for j in range(200)), Q(0))
    require(all_time < 6 and 6 - all_time == Q(6, 2**200), "finite time prefix")
    samples = [2**(n + 1) for n in range(1, 21)]
    require(samples == sorted(samples) and samples[-1] > 10**6,
            "unbounded sample replay")
    return {
        "one_time_limit": "3",
        "all_time_limit": "6",
        "potential_samples": "20/20",
        "status": "PASS",
    }


def deterministic(data: dict[str, Any]) -> None:
    proc = subprocess.run(
        [sys.executable, str(CERT), "--manifest-json", "--verifier", str(VERIFIER)],
        cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=180,
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
        print(f"ROUND65_CROSS_GATE_VERIFY_ERROR: {exc}", file=sys.stderr)
        return 1
    print("ROUND65 CROSS-GATE: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
