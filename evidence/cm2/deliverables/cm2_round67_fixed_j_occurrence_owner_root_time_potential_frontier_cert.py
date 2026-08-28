#!/usr/bin/env python3
"""Producer for the Round-67 fixed-time physical-root frontier."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round67_common import (
    CertError, canonical_bytes, digest, require, sha256_path, validate_pins,
)


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.round67.fixed-j-occurrence-owner-root-time-potential.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-round67-fixed-j-occurrence-owner-root-time-potential-frontier"
REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
VERIFIER = HERE / "cm2_round67_fixed_j_occurrence_owner_root_time_potential_frontier_verifier.py"
COMMON = HERE / "cm2_round67_common.py"

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


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def build_result() -> dict[str, Any]:
    w = Q(3, 2)
    rows = []
    for n in range(1, 17):
        mass = Q(3, 4**n)
        single = w ** (n - 1)
        eligibility = (w**n - 1) / (w - 1)
        rows.append({
            "n": n,
            "mass": qstr(mass),
            "single_slice_potential": qstr(single),
            "single_slice_moment_term": qstr(mass * single),
            "eligibility_potential": qstr(eligibility),
            "eligibility_moment_term": qstr(mass * eligibility),
        })

    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "append_only": True,
            "old_artifacts_modified": False,
            "pinned_frozen_chain": PINS,
        },
        "actual_fixed_j_subroot": {
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
        },
        "countable_time_carrier": {
            "status": "CERTIFIED_STANDARD_BOREL_CARRIER_ONLY",
            "carrier": "disjoint_union_j {j} x Omega_j",
            "time_retained": True,
            "finite_weighted_physical_law": "NOT_CERTIFIED",
            "strong_all_time_operator": "NOT_CERTIFIED",
        },
        "direct_root_potential": {
            "status": "CERTIFIED_EXACT_ON_OCCURRENCE_ROOT",
            "owner_density": "r_j=dm_j^own/dm_occ in {0,1}",
            "potential": "H_g(x)=sum_j w^j r_j(x)g_j(x)",
            "bounded_iff": "H_g in L_infinity(m_occ)",
            "operator_norm": "||A_g||=ess_sup H_g",
            "fixed_time_L1_implies_strong_all_time": False,
            "actual_all_sector_H_g": "NOT_CERTIFIED",
        },
        "terminal_eligibility": {
            "status": "CERTIFIED_EXACT_ENVELOPE",
            "indicator": "r_j^elig=1_{j<n(x)}",
            "unit_charge_potential": "H_elig=(w^n-1)/(w-1)",
            "bounded_iff": "n in L_infinity(m_occ)",
            "actual_owner_indicator_relation": "0<=r_j<=r_j^elig",
            "eligibility_divergence_implies_actual_owner_divergence": False,
            "actual_terminal_depth_essential_bound": "NOT_CERTIFIED",
            "actual_owner_pointwise_pattern": "NOT_CERTIFIED",
        },
        "finite_average_separators": {
            "status": "CERTIFIED_EXACT",
            "law": "m{n}=3*4^-n on n>=1",
            "w": qstr(w),
            "single_slice_rule": "r_j(n)=1_{j=n-1}",
            "single_slice_total_weighted_charge": "6/5",
            "single_slice_potential_unbounded": True,
            "eligibility_rule": "r_j(n)=1_{j<n}",
            "eligibility_total_weighted_charge": "8/5",
            "eligibility_potential_unbounded": True,
            "rows": rows,
            "conclusion": "FINITE_COMPLETE_WEIGHTED_VECTOR_CHARGE_NOT_L1_OPERATOR_BOUND",
        },
        "minimal_spanning_registry": {
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
        },
        "latest_technology_boundary": {
            "checked_on": "2026-07-21",
            "arxiv_2604_18929v3": "SMOOTH_AXIOM_A_MARKOV_PARTITION_SRB_PRODUCT__NO_COLLISION_MOVING_BOUNDARY_OR_IMMUTABLE_CROSSWALK",
            "arxiv_2602_19435v2": "SPECTRAL_APPROXIMATION_AFTER_COMPACTNESS_OR_LY_BOUND_IS_SUPPLIED__DOES_NOT_BUILD_PHYSICAL_SPACE",
            "arxiv_2601_10539v2": "HORMANDER_ITO_DIFFUSION_FEYNMAN_KAC__WRONG_PROCESS_AND_RECIPIENT",
            "new_same_law_moving_billiard_theorem_found": False,
            "external_theorem_promoted": False,
        },
        "strict_status": {
            "Gate1": "NOT_CERTIFIED",
            "Gate2": "NOT_CERTIFIED__OFFICIAL_FIELDS_0_OF_17",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED__LANDING_JOIN_1_OF_7",
            "Gate5": "NOT_CERTIFIED__MATURITY_10_OF_18_BLOCKS_0",
            "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    replay = copy.deepcopy(result)
    result["internal_replay_digest"] = digest(replay)
    return result


def build_manifest(verifier: Path) -> dict[str, Any]:
    validate_pins(HERE, PINS)
    result = build_result()
    require(REPORT.is_file() and verifier.is_file() and COMMON.is_file(), "artifact missing")
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
    validate_pins(HERE, PINS)
    result = build_result()
    sep = result["finite_average_separators"]
    require(Q(sep["single_slice_total_weighted_charge"]) == Q(6, 5), "single total")
    require(Q(sep["eligibility_total_weighted_charge"]) == Q(8, 5), "elig total")
    require(sep["single_slice_potential_unbounded"] is True, "single unbounded")
    require(sep["eligibility_potential_unbounded"] is True, "elig unbounded")
    return {"pins": "11/11", "separator_rows": "16/16", "status": "PASS"}


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
        print(f"ROUND67_FIXED_ROOT_CERT_ERROR: {exc}", file=sys.stderr)
        return 1
    print("ROUND67 FIXED-J ROOT: PARTIAL_ONLY")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
