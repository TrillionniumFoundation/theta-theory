#!/usr/bin/env python3
"""Independent verifier for the Round-67 fixed-time physical-root frontier."""

from __future__ import annotations

import argparse
import copy
import json
import subprocess
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round67_common import (
    CertError, digest, replay_sidecar, require, semantic_mutation_test,
    sha256_path, strict_json_path, strict_json_self_test, validate_pins,
)


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.round67.fixed-j-occurrence-owner-root-time-potential.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-round67-fixed-j-occurrence-owner-root-time-potential-frontier"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
SIDECAR = HERE / f"{PREFIX}-manifest-2026-07-21.sha256"
REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
CERT = HERE / "cm2_round67_fixed_j_occurrence_owner_root_time_potential_frontier_cert.py"
VERIFIER = Path(__file__).resolve()
COMMON = HERE / "cm2_round67_common.py"
EXPECTED_RESULT_DIGEST = "114060c5debf597c6d127e0a5a502a43ccef266300eb19723ebfddbddacf922c"

PINS = {
    "cm2-sixty-sixth-direct-assault-2026-07-21.md":
        "690cfeb13108314a3a05f5e4cd342d573c41e66551464ebf7f4b5576f374b811",
    "cm2-sixty-sixth-direct-assault-manifest-2026-07-21.sha256":
        "b437761fb84aa431e468af587e2207adadf6e0a996ee593a93df467147be3b5d",
    "cm2-round66-independent-core-frontier-audit-manifest-2026-07-21.json":
        "b67b76e52d073989fac6fb41eaf3e49167aa1e166d32003c72129e08ec6d46b3",
    "cm2-round66-immutable-registry-junction-tree-positive-potential-frontier-manifest-2026-07-21.json":
        "adc2654ed27fa62c83dd9d64ddce09832e173f50d518c464007d9bc320d6294f",
    "cm2-gate13-round66-same-representative-material-trace-frontier-manifest-2026-07-21.json":
        "11bb7ba12e3302a547893dae3a897efc5a66223bbc2cf740bb6f7b5e53882224",
    "cm2-gate24-round66-collision-srb-product-variation-frontier-manifest-2026-07-21.json":
        "be98266945e3e6bd7fee0bf27f49a3282dc41f67e95f74b0c41c041d0cd4bf94",
    "cm2-gate5-round66-owner-overlap-sector-flux-frontier-manifest-2026-07-21.json":
        "31f8b9068b3afaad779f299d5adb3e1ff870d3b48ad943704e1347b7ac06a686",
    "cm2-gate5-round44-all-face-suffix-two-trace-f13-manifest-2026-07-19.json":
        "3cf6635532622427bcde0525205212e1970b92ee56b2eb290ed01c1984443a9d",
    "cm2-gate5-round52-owner-tail-tower-anisotropic-frontier-manifest-2026-07-20.json":
        "ca623e4c350b75f0fec889d0909b052bb0493613ff2f983ac71fd2fca40e016b",
    "cm2-gate5-round60-owner-trace-suffix-positive-anchor-frontier-manifest-2026-07-20.json":
        "d519ad15a870fe7820839828347140e4bae3b5752a95fab4c18263c67e2ab778",
    "cm2-gate5-round61-complement-rn-borel-orlicz-frontier-manifest-2026-07-20.json":
        "59bce010748cccc1ffb829a9c232cab77185e6467433b3fed34988913649ae75",
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
        "pinned_frozen_chain": PINS,
    }, "provenance")
    require(result["actual_fixed_j_subroot"] == {
        "status": "CERTIFIED_GRAPH_SUPPORTED_PHYSICAL_SUBROOT",
        "base_law": "finite standard-Borel endpoint-coarea occurrence law m_occ",
        "root": "Omega_j={(a,x):x in E_(j,a)^owner intersect R_(j,a)^reg}",
        "root_measure": "M_j=m_j^own",
        "owner_law": "nu_j=(q_j)_#M_j",
        "occurrence_view": "identity restriction of m_occ",
        "owner_view": "deterministic Borel q_j",
        "retained_keys": [
            "restriction-id", "time-j", "physical-event-signature",
            "primitive-key", "connected-rank-0", "side-label",
            "word-cell", "endpoint/root coordinates",
        ],
        "time_deleted_or_deduplicated": False,
        "forward_cost_RN": "C_j^f=d(q_j#(c_f M_j))/dnu_j",
        "reverse_cost_RN": "C_j^r=d(q_j#(c_r M_j))/dnu_j",
        "fixed_j_cost_integrals_finite": True,
        "Round54_Jordan_common_mode_identified": False,
    }, "fixed-j subroot")
    require(result["countable_time_carrier"] == {
        "status": "CERTIFIED_STANDARD_BOREL_CARRIER_ONLY",
        "carrier": "disjoint_union_j {j} x Omega_j",
        "time_retained": True,
        "finite_weighted_physical_law": "NOT_CERTIFIED",
        "strong_all_time_operator": "NOT_CERTIFIED",
    }, "time carrier")
    require(result["direct_root_potential"] == {
        "status": "CERTIFIED_EXACT_ON_OCCURRENCE_ROOT",
        "owner_density": "r_j=dm_j^own/dm_occ in {0,1}",
        "potential": "H_g(x)=sum_j w^j r_j(x)g_j(x)",
        "bounded_iff": "H_g in L_infinity(m_occ)",
        "operator_norm": "||A_g||=ess_sup H_g",
        "fixed_time_L1_implies_strong_all_time": False,
        "actual_all_sector_H_g": "NOT_CERTIFIED",
    }, "direct potential")
    require(result["terminal_eligibility"] == {
        "status": "CERTIFIED_EXACT_ENVELOPE",
        "indicator": "r_j^elig=1_{j<n(x)}",
        "unit_charge_potential": "H_elig=(w^n-1)/(w-1)",
        "bounded_iff": "n in L_infinity(m_occ)",
        "actual_owner_indicator_relation": "0<=r_j<=r_j^elig",
        "eligibility_divergence_implies_actual_owner_divergence": False,
        "actual_terminal_depth_essential_bound": "NOT_CERTIFIED",
        "actual_owner_pointwise_pattern": "NOT_CERTIFIED",
    }, "eligibility")

    sep = result["finite_average_separators"]
    require({k: sep[k] for k in sep if k != "rows"} == {
        "status": "CERTIFIED_EXACT",
        "law": "m{n}=3*4^-n on n>=1",
        "w": "3/2",
        "single_slice_rule": "r_j(n)=1_{j=n-1}",
        "single_slice_total_weighted_charge": "6/5",
        "single_slice_potential_unbounded": True,
        "eligibility_rule": "r_j(n)=1_{j<n}",
        "eligibility_total_weighted_charge": "8/5",
        "eligibility_potential_unbounded": True,
        "conclusion": "FINITE_COMPLETE_WEIGHTED_VECTOR_CHARGE_NOT_L1_OPERATOR_BOUND",
    }, "separator header")
    require(len(sep["rows"]) == 16, "separator row count")
    w = Q(3, 2)
    for row in sep["rows"]:
        n = row["n"]
        mass = Q(3, 4**n)
        single = w ** (n - 1)
        elig = (w**n - 1) / (w - 1)
        require(row == {
            "n": n,
            "mass": str(mass),
            "single_slice_potential": str(single),
            "single_slice_moment_term": str(mass * single),
            "eligibility_potential": str(elig),
            "eligibility_moment_term": str(mass * elig),
        }, "separator row")

    require(result["minimal_spanning_registry"] == {
        "status": "ONE_PHYSICAL_SUBROOT_CERTIFIED__FOUR_CROSSWALKS_OPEN",
        "certified_node": "MOVING_OCCURRENCE_PLUS_FIXED_J_OWNER_COLLAR",
        "open_edges": [
            "OWNER_TO_EXACT_RETURN_GRAPH_PATH_COMPONENT",
            "RETURN_PATH_TO_ALL_CELL_ALL_DEPTH_MATERIAL_ATLAS",
            "RETURN_PATH_TO_COLLISION_SRB_STABLE_PRODUCT_ROOT",
            "STABLE_PLAQUE_TO_COMBINED_GREEN_QNL_REPRESENTATIVE",
        ],
        "Gate1_actual_common_rows": "0/8",
        "Gate24_actual_tree_rows": "0/7",
        "global_graph_supported_root": "NOT_CERTIFIED",
    }, "spanning registry")
    require(result["latest_technology_boundary"] == {
        "checked_on": "2026-07-21",
        "arxiv_2604_18929v3": "SMOOTH_AXIOM_A_MARKOV_PARTITION_SRB_PRODUCT__NO_COLLISION_MOVING_BOUNDARY_OR_IMMUTABLE_CROSSWALK",
        "arxiv_2602_19435v2": "SPECTRAL_APPROXIMATION_AFTER_COMPACTNESS_OR_LY_BOUND_IS_SUPPLIED__DOES_NOT_BUILD_PHYSICAL_SPACE",
        "arxiv_2601_10539v2": "HORMANDER_ITO_DIFFUSION_FEYNMAN_KAC__WRONG_PROCESS_AND_RECIPIENT",
        "new_same_law_moving_billiard_theorem_found": False,
        "external_theorem_promoted": False,
    }, "technology boundary")
    require(result["strict_status"] == {
        "Gate1": "NOT_CERTIFIED",
        "Gate2": "NOT_CERTIFIED__OFFICIAL_FIELDS_0_OF_17",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED__LANDING_JOIN_1_OF_7",
        "Gate5": "NOT_CERTIFIED__MATURITY_10_OF_18_BLOCKS_0",
        "complete_composite_gates": "0/5",
        "CM2": "NO-GO_FOR_CLAIM",
    }, "strict status")


def independent_replay() -> dict[str, Any]:
    w = Q(3, 2)
    single = sum((Q(3, 4**n) * w**(n - 1) for n in range(1, 240)), Q(0))
    elig = sum((Q(3, 4**n) * (w**n - 1) / (w - 1)
                for n in range(1, 240)), Q(0))
    require(single < Q(6, 5) and elig < Q(8, 5), "finite prefixes")
    require(Q(6, 5) - single > 0 and Q(8, 5) - elig > 0, "positive tails")
    single_samples = [w**(n - 1) for n in range(1, 25)]
    elig_samples = [(w**n - 1) / (w - 1) for n in range(1, 25)]
    require(single_samples == sorted(single_samples) and
            elig_samples == sorted(elig_samples) and
            single_samples[-1] > 10**4 and elig_samples[-1] > 10**4,
            "unbounded samples")
    return {
        "single_total_limit": "6/5",
        "eligibility_total_limit": "8/5",
        "potential_samples": "48/48",
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
        print(f"ROUND67_FIXED_ROOT_VERIFY_ERROR: {exc}", file=sys.stderr)
        return 1
    print("ROUND67 FIXED-J ROOT: PARTIAL_ONLY")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
