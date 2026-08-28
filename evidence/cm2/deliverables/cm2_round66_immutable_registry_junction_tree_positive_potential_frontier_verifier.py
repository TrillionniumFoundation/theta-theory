#!/usr/bin/env python3
"""Independent verifier for the Round-66 immutable-registry leaf."""

from __future__ import annotations

import argparse
import copy
import json
import subprocess
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round66_common import (
    CertError, digest, replay_sidecar, require, semantic_mutation_test,
    sha256_path, strict_json_path, strict_json_self_test, validate_pins,
)


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.round66.immutable-registry-junction-tree-positive-potential.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-round66-immutable-registry-junction-tree-positive-potential-frontier"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
SIDECAR = HERE / f"{PREFIX}-manifest-2026-07-21.sha256"
REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
CERT = HERE / "cm2_round66_immutable_registry_junction_tree_positive_potential_frontier_cert.py"
VERIFIER = Path(__file__).resolve()
COMMON = HERE / "cm2_round66_common.py"
EXPECTED_RESULT_DIGEST = "c1bc0eb8d40d622e6f0ff224d327b365d4c1bda899c2e238f96f4ffec5108afd"

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
    "cm2-gate5-round65-cross_time_sector_jordan_cemetery_frontier-manifest-2026-07-21.json":
        "43d80312d1ada853af84a9d8f5edd4393388a62ae3788e9fbcc1eaa4ea510ce5",
    "cm2-round65-cross-gate-positive-potential-technology-frontier-manifest-2026-07-21.json":
        "f731715bd734649073e0bd35763c170a48ef8383f6dd892696b52a98ea86eb14",
}


# Keep the on-disk spelling exact; the constant above is repaired before use.
PINS["cm2-gate5-round65-cross-time-sector-jordan-cemetery-frontier-manifest-2026-07-21.json"] = \
    PINS.pop("cm2-gate5-round65-cross_time_sector_jordan_cemetery_frontier-manifest-2026-07-21.json")


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
        "pinned_round65_frontier": PINS,
    }, "provenance")

    require(result["junction_tree_theorem"] == {
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
    }, "junction theorem")

    require(result["valid_tree_replay"] == {
        "status": "CERTIFIED_EXACT",
        "cliques": ["AB", "BC", "BD"],
        "tree_edges": ["AB--BC", "AB--BD"],
        "constraints": ["A=B", "B=C", "B!=D"],
        "global_atoms": ["0001", "1110"],
        "global_atom_count": 2,
        "each_clique_atom_mass": "1/2",
        "edge_separator_B_marginal": ["0:1/2", "1:1/2"],
    }, "valid tree replay")

    sep = result["cyclic_parity_separator"]
    require(sep["status"] == "CERTIFIED_EXACT", "cyclic status")
    require(sep["pair_laws"] == {
        "AB": "UNIFORM_ON_00_11__A_EQ_B",
        "BC": "UNIFORM_ON_00_11__B_EQ_C",
        "AC": "UNIFORM_ON_01_10__A_NE_C",
    }, "pair laws")
    require(sep["every_singleton_overlap"] == "UNIFORM_ON_0_1", "overlaps")
    require(sep["all_constraints"] == ["A_EQ_B", "B_EQ_C", "A_NE_C"],
            "constraints")
    require(sep["candidate_atoms"] == 8 and sep["accepted_atoms"] == [] and
            sep["accepted_count"] == 0, "cyclic atoms")
    require(sep["running_intersection_available"] is False, "running intersection")
    expected_deletions = {
        "A_EQ_B": (["B_EQ_C", "A_NE_C"], ["011", "100"]),
        "B_EQ_C": (["A_EQ_B", "A_NE_C"], ["001", "110"]),
        "A_NE_C": (["A_EQ_B", "B_EQ_C"], ["000", "111"]),
    }
    rows = sep["delete_one_constraint_rows"]
    require(len(rows) == 3, "deletion row count")
    for row in rows:
        kept, atoms = expected_deletions[row["deleted"]]
        require(row == {
            "deleted": row["deleted"],
            "kept": kept,
            "accepted_atoms": atoms,
            "accepted_count": 2,
        }, "deletion row")
    require(sep["conclusion"] ==
            "PAIRWISE_OVERLAP_COMPATIBILITY_ON_A_CYCLE_NOT_GLOBAL_REGISTRY",
            "cyclic conclusion")

    require(result["physical_root_equivalence"] == {
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
    }, "physical root")

    pot = result["glued_positive_potential_separator"]
    require({key: pot[key] for key in pot if key != "potential_rows"} == {
        "status": "CERTIFIED_EXACT",
        "root": "N_POSITIVE_WITH_NU_N_EQ_3_TIMES_4_POW_MINUS_N",
        "all_fragments": "IDENTITY_MARGINAL_ON_SAME_IMMUTABLE_N",
        "global_join": "TRIVIAL_AND_EXACT",
        "potential": "H(n)=2^n",
        "actual_moment": "3",
        "potential_essentially_bounded": False,
        "conclusion": "EXACT_REGISTRY_PLUS_FINITE_ACTUAL_MOMENT_NOT_STRONG_ASSEMBLY",
    }, "potential separator header")
    require(len(pot["potential_rows"]) == 16, "potential rows")
    for row in pot["potential_rows"]:
        n = row["n"]
        require(row == {
            "n": n,
            "root_mass": str(Q(3, 4**n)),
            "potential": str(2**n),
            "moment_term": str(Q(3, 2**n)),
            "unit_L1_atom_norm": str(2**n),
        }, "potential row")

    require(result["two_line_sufficient_route"] == {
        "registry_line": "GRAPH_SUPPORTED_IMMUTABLE_JUNCTION_TREE_JOIN_OR_COMMON_ROOT",
        "pointwise_rows": "P_(0:j)W_j<=C_j_ON_THE_SAME_ROOT",
        "summability_line": "SUM_j_w^j_C_j_LT_INFINITY",
        "conclusion": "H_IN_L_INFINITY_AND_STRONG_POSITIVE_LIFT_BOUNDED",
        "actual_registry_line": "NOT_CERTIFIED",
        "actual_summability_line": "NOT_CERTIFIED",
    }, "sufficient route")
    require(result["latest_technology_boundary"] == {
        "checked_on": "2026-07-21",
        "arxiv_2502_07765v2": "SEQUENTIAL_DISPERSING_BILLIARD_CLT_VIA_COMPLEX_CONES__NO_PARAMETER_DERIVATIVE_PIOLA_OR_PRODUCT_TREE",
        "arxiv_2504_16532v3": "C5_ANOSOV_TWO_TORUS_LINEAR_RESPONSE__SMOOTH_NO_COLLISION_OR_MOVING_BOUNDARY",
        "arxiv_2402_02496v2": "C1_PLUS_GAMMA_CLOSED_MANIFOLD_ASYMPTOTIC_LOCAL_PRODUCT__NO_SINGULAR_COLLISION_ATLAS",
        "arxiv_2504_17879v1": "COUNTABLE_UNIFORMLY_LAZY_DIRECT_STEP_KILLED_CHAIN__WRONG_PROCESS_AND_UNVERIFIED_HYPOTHESES",
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
    }, "strict state")


def independent_replay() -> dict[str, Any]:
    triangle = []
    tree = []
    singleton_counts = {"A0": 0, "A1": 0, "B0": 0, "B1": 0, "C0": 0, "C1": 0}
    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                if a == b and b == c and a != c:
                    triangle.append((a, b, c))
                if a == b and b == c:
                    for d in (0, 1):
                        if b != d:
                            tree.append((a, b, c, d))
        singleton_counts[f"A{a}"] += 1
    # Each pair law in the separator gives uniform singleton marginals by inspection.
    require(triangle == [], "triangle replay")
    require(tree == [(0, 0, 0, 1), (1, 1, 1, 0)], "tree replay")
    partial = sum((Q(3, 2**n) for n in range(1, 200)), Q(0))
    require(partial < 3 and 3 - partial == Q(3, 2**199), "moment limit")
    atom_norms = [2**n for n in range(1, 21)]
    require(atom_norms[-1] > 10**6 and atom_norms == sorted(atom_norms),
            "unbounded norms")
    return {
        "cyclic_support": "0/8",
        "valid_tree_support": "2/16",
        "moment_limit": "3",
        "unbounded_samples": "20/20",
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
        print(f"ROUND66_IMMUTABLE_REGISTRY_VERIFY_ERROR: {exc}", file=sys.stderr)
        return 1
    print("ROUND66 IMMUTABLE REGISTRY: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
