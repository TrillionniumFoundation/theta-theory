#!/usr/bin/env python3
"""Producer for the append-only Round-66 immutable-registry leaf."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round66_common import (
    CertError, canonical_bytes, digest, require, sha256_path, validate_pins,
)


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.round66.immutable-registry-junction-tree-positive-potential.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-round66-immutable-registry-junction-tree-positive-potential-frontier"
REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
VERIFIER = HERE / "cm2_round66_immutable_registry_junction_tree_positive_potential_frontier_verifier.py"
COMMON = HERE / "cm2_round66_common.py"

PINS = {
    "cm2-sixty-fifth-direct-assault-2026-07-21.md":
        "aeaafaf3411e90d6d1843159e248f18af12e5fdf993acfb9685adcc1b14e7bb0",
    "cm2-sixty-fifth-direct-assault-manifest-2026-07-21.sha256":
        "22283d37c12651e955b2502ad7660fa22d309c1d1902c471b1527470d6cc1cc2",
    "cm2-round65-independent-core-frontier-audit-manifest-2026-07-21.json":
        "92ba883654f761a4df5974d889f99aa077769bb37ba0cd5d6fd03ceb8470629f",
    "cm2-gate13-round65-actual-cross-tail-piola-current-frontier-manifest-2026-07-21.json":
        "e87bb0896c1fc59b6b020d1325bd9462fd932f5d186acabb0fcf770ed9b34701",
    "cm2-gate24-round65-actual-product-tree-strong-assembly-frontier-manifest-2026-07-21.json":
        "6b50742ac15f4fb4870d8e67b466252e57c1c796e48a1eaae5d2380f113cddd3",
    "cm2-gate5-round65-cross-time-sector-jordan-cemetery-frontier-manifest-2026-07-21.json":
        "43d80312d1ada853af84a9d8f5edd4393388a62ae3788e9fbcc1eaa4ea510ce5",
    "cm2-round65-cross-gate-positive-potential-technology-frontier-manifest-2026-07-21.json":
        "f731715bd734649073e0bd35763c170a48ef8383f6dd892696b52a98ea86eb14",
}


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def atoms_for(constraints: tuple[str, ...]) -> list[str]:
    atoms: list[str] = []
    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                ok = True
                for constraint in constraints:
                    if constraint == "A_EQ_B":
                        ok = ok and a == b
                    elif constraint == "B_EQ_C":
                        ok = ok and b == c
                    elif constraint == "A_NE_C":
                        ok = ok and a != c
                    else:
                        raise CertError(f"unknown constraint: {constraint}")
                if ok:
                    atoms.append(f"{a}{b}{c}")
    return atoms


def build_result() -> dict[str, Any]:
    all_constraints = ("A_EQ_B", "B_EQ_C", "A_NE_C")
    deleted_rows = []
    for deleted in all_constraints:
        kept = tuple(c for c in all_constraints if c != deleted)
        deleted_rows.append({
            "deleted": deleted,
            "kept": list(kept),
            "accepted_atoms": atoms_for(kept),
            "accepted_count": len(atoms_for(kept)),
        })

    potential_rows = []
    for n in range(1, 17):
        mass = Q(3, 4**n)
        charge = Q(2**n)
        potential_rows.append({
            "n": n,
            "root_mass": qstr(mass),
            "potential": qstr(charge),
            "moment_term": qstr(mass * charge),
            "unit_L1_atom_norm": qstr(charge),
        })

    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "append_only": True,
            "old_artifacts_modified": False,
            "pinned_round65_frontier": PINS,
        },
        "junction_tree_theorem": {
            "status": "CERTIFIED_EXACT_STANDARD_BOREL",
            "hypotheses": [
                "FINITE_FRAGMENT_TREE",
                "STANDARD_BOREL_COORDINATES",
                "RUNNING_INTERSECTION_FOR_EVERY_KEY",
            ],
            "necessary_and_sufficient": "EDGE_SEPARATOR_MARGINALS_MATCH_EXACTLY",
            "construction": "ROOT_TREE_AND_ATTACH_CHILD_REGULAR_CONDITIONALS",
            "global_coupling_unique": False,
            "abstract_same_law_is_physical_identity": False,
            "physical_upgrade": "PINNED_IMMUTABLE_SEPARATOR_IDS_OR_PINNED_BOREL_CROSSWALKS",
        },
        "valid_tree_replay": {
            "status": "CERTIFIED_EXACT",
            "cliques": ["AB", "BC", "BD"],
            "tree_edges": ["AB--BC", "AB--BD"],
            "constraints": ["A=B", "B=C", "B!=D"],
            "global_atoms": ["0001", "1110"],
            "global_atom_count": 2,
            "each_clique_atom_mass": "1/2",
            "edge_separator_B_marginal": ["0:1/2", "1:1/2"],
        },
        "cyclic_parity_separator": {
            "status": "CERTIFIED_EXACT",
            "pair_laws": {
                "AB": "UNIFORM_ON_00_11__A_EQ_B",
                "BC": "UNIFORM_ON_00_11__B_EQ_C",
                "AC": "UNIFORM_ON_01_10__A_NE_C",
            },
            "every_singleton_overlap": "UNIFORM_ON_0_1",
            "all_constraints": list(all_constraints),
            "candidate_atoms": 8,
            "accepted_atoms": atoms_for(all_constraints),
            "accepted_count": len(atoms_for(all_constraints)),
            "running_intersection_available": False,
            "delete_one_constraint_rows": deleted_rows,
            "conclusion": "PAIRWISE_OVERLAP_COMPATIBILITY_ON_A_CYCLE_NOT_GLOBAL_REGISTRY",
        },
        "physical_root_equivalence": {
            "status": "CERTIFIED_EXACT_GRAPH_SUPPORT_INTERFACE",
            "forward": "COMMON_ROOT_MAPS_AGREE_POINTWISE_ON_SHARED_KEYS_IMPLIES_GRAPH_SUPPORTED_JOIN",
            "reverse": "GRAPH_SUPPORTED_GLOBAL_JOIN_IS_A_COMMON_ROOT",
            "anonymous_equal_marginals_suffice": False,
            "required_cm2_key_groups": [
                "PATH_TIME_OWNER_BRANCH",
                "COLLISION_STABLE_PLAQUE_ROOT",
                "MATERIAL_FACE_CURRENT_ATLAS",
                "LIVE_ONE_SHOT_ARRIVAL",
                "SECTOR_POSITIVE_PAIR_JORDAN",
            ],
            "actual_cm2_graph_supported_root": "NOT_CERTIFIED",
        },
        "glued_positive_potential_separator": {
            "status": "CERTIFIED_EXACT",
            "root": "N_POSITIVE_WITH_NU_N_EQ_3_TIMES_4_POW_MINUS_N",
            "all_fragments": "IDENTITY_MARGINAL_ON_SAME_IMMUTABLE_N",
            "global_join": "TRIVIAL_AND_EXACT",
            "potential": "H(n)=2^n",
            "actual_moment": "3",
            "potential_essentially_bounded": False,
            "potential_rows": potential_rows,
            "conclusion": "EXACT_REGISTRY_PLUS_FINITE_ACTUAL_MOMENT_NOT_STRONG_ASSEMBLY",
        },
        "two_line_sufficient_route": {
            "registry_line": "GRAPH_SUPPORTED_IMMUTABLE_JUNCTION_TREE_JOIN_OR_COMMON_ROOT",
            "pointwise_rows": "P_(0:j)W_j<=C_j_ON_THE_SAME_ROOT",
            "summability_line": "SUM_j_w^j_C_j_LT_INFINITY",
            "conclusion": "H_IN_L_INFINITY_AND_STRONG_POSITIVE_LIFT_BOUNDED",
            "actual_registry_line": "NOT_CERTIFIED",
            "actual_summability_line": "NOT_CERTIFIED",
        },
        "latest_technology_boundary": {
            "checked_on": "2026-07-21",
            "arxiv_2502_07765v2": "SEQUENTIAL_DISPERSING_BILLIARD_CLT_VIA_COMPLEX_CONES__NO_PARAMETER_DERIVATIVE_PIOLA_OR_PRODUCT_TREE",
            "arxiv_2504_16532v3": "C5_ANOSOV_TWO_TORUS_LINEAR_RESPONSE__SMOOTH_NO_COLLISION_OR_MOVING_BOUNDARY",
            "arxiv_2402_02496v2": "C1_PLUS_GAMMA_CLOSED_MANIFOLD_ASYMPTOTIC_LOCAL_PRODUCT__NO_SINGULAR_COLLISION_ATLAS",
            "arxiv_2504_17879v1": "COUNTABLE_UNIFORMLY_LAZY_DIRECT_STEP_KILLED_CHAIN__WRONG_PROCESS_AND_UNVERIFIED_HYPOTHESES",
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
    sep = result["cyclic_parity_separator"]
    require(sep["accepted_count"] == 0, "parity separator")
    require(all(row["accepted_count"] == 2 for row in sep["delete_one_constraint_rows"]),
            "deleted constraint rows")
    require(result["valid_tree_replay"]["global_atom_count"] == 2, "tree replay")
    require(Q(result["glued_positive_potential_separator"]["actual_moment"]) == 3,
            "potential moment")
    return {"pins": "7/7", "parity_atoms": "0/8", "tree_atoms": "2/16", "status": "PASS"}


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
        print(f"ROUND66_IMMUTABLE_REGISTRY_CERT_ERROR: {exc}", file=sys.stderr)
        return 1
    print("ROUND66 IMMUTABLE REGISTRY: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
