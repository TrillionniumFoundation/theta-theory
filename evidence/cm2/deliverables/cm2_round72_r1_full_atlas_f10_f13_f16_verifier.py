#!/usr/bin/env python3
"""Independent verifier for the Round-72 base-R1 full family atlas."""

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
from cm2_round72_r1_full_atlas_f10_f13_f16_cert import (
    ARTIFACT_HASHES, COMMON, FAMILY_PROOF, FIELD_PROOF, MANIFEST_SCHEMA,
    MONO_PROOF, PINS, RESULT_SCHEMA, build_result, validate_artifacts,
)


HERE = Path(__file__).resolve().parent
PREFIX = "cm2-round72-r1-full-atlas-f10-f13-f16"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
CERT = HERE / "cm2_round72_r1_full_atlas_f10_f13_f16_cert.py"
VERIFIER = Path(__file__).resolve()
WITNESSES = HERE / "cm2-round71-r1-nonempty-face-witnesses-2026-07-21.json"


def prefix_cover(paths: list[str]) -> None:
    require(len(paths) == len(set(paths)), "unique paths")
    ordered = sorted(paths)
    require(all(not right.startswith(left) for index, left in enumerate(ordered)
                for right in ordered[index + 1:]), "prefix free")
    require(sum(Q(1, 2 ** len(path)) for path in paths) == 1, "complete prefix cover")


def integrity(data: dict[str, Any], check_files: bool = True) -> None:
    require(data["schema"] == MANIFEST_SCHEMA, "manifest schema")
    require(data["result"]["schema"] == RESULT_SCHEMA, "result schema")
    require(data["pins"] == PINS and data["proof_and_generator_hashes"] == ARTIFACT_HASHES,
            "pins and artifacts")
    if check_files:
        validate_pins(HERE, PINS)
        validate_artifacts()
        require(data["report_sha256"] == sha256_path(REPORT), "report hash")
        require(data["certificate_sha256"] == sha256_path(CERT), "certificate hash")
        require(data["verifier_sha256"] == sha256_path(VERIFIER), "verifier hash")
        require(data["common_sha256"] == sha256_path(COMMON), "common hash")
    replay = copy.deepcopy(data["result"])
    claimed = replay.pop("internal_replay_digest")
    require(claimed == digest(replay), "result digest")
    require(data["verdict"] == data["result"]["strict_frontier"], "verdict")


def semantics(result: dict[str, Any]) -> None:
    require(result == build_result(), "canonical result")
    atlas = result["complete_base_fibre_terminal_preimage_family_atlas"]
    require(atlas["status"] == "CERTIFIED_COMPLETE_1152_FAMILY_CLASSIFICATION",
            "atlas status")
    require(atlas["candidate_family_count"] == 1152 and atlas["positive_family_count"] == 32 and
            atlas["certified_empty_family_count"] == 1120 and
            atlas["unresolved_family_count"] == atlas["corner_residual_count"] == 0,
            "atlas counts")
    require(atlas["interval_map_test_count"] == 824 and atlas["interval_leaf_count"] == 424 and
            atlas["maximum_interval_depth"] == 13, "atlas tree")
    components = result["complete_positive_component_registry"]
    require(components["status"] == "CERTIFIED_32_UNIQUE_FULL_CLIPPED_CONNECTED_COMPONENTS",
            "component status")
    require(components["component_count"] == 32 and components["one_sided_trace_count"] == 64 and
            components["derivative_interval_test_count"] == 112 and
            components["derivative_leaf_count"] == 64 and
            components["maximum_derivative_depth"] == 2, "component counts")
    fields = result["numeric_local_field_registry"]
    require(fields["status"] == "CERTIFIED_32_ACTUAL_F10_F13_F16_COMPONENT_ROWS",
            "field status")
    require(fields["F10_numeric_rows"] == 32 and fields["F10_integer_minimum"] == 3 and
            fields["F10_integer_maximum"] == 39 and fields["F10_integer_sum"] == 480,
            "F10 summary")
    require(fields["F13_numeric_rows"] == fields["F16_numeric_rows"] == 32 and
            Q(fields["F13_32_face_current_variation_strict_upper"]) == Q(4, 125000000) and
            Q(fields["F16_32_face_flux_cost_strict_upper"]) == Q(4, 125000000),
            "F13 F16 summary")
    require(len(fields["component_field_rows"]) == 32 and
            sum(row["F10_integer_upper"] for row in fields["component_field_rows"]) == 480,
            "field rows")
    frontier = result["strict_frontier"]
    require(frontier["base_fibre_terminal_preimage_family_classification"] ==
            "CERTIFIED_COMPLETE" and frontier["arbitrary_depth_Rn_face_atlas"] ==
            "NOT_CERTIFIED", "scope frontier")
    require(frontier["complete_composite_gates"] == "0/5" and
            frontier["CM2"] == "NO-GO_FOR_CLAIM", "strict verdict")


def independent_replay() -> dict[str, str]:
    family = strict_json_path(FAMILY_PROOF)
    mono = strict_json_path(MONO_PROOF)
    fields = strict_json_path(FIELD_PROOF)
    witnesses = strict_json_path(WITNESSES)["rows"]

    classification = family["classification"]
    positive = classification["positive_family_ids"]
    empty = classification["certified_empty_family_ids"]
    require(len(positive) == len(set(positive)) == 32, "positive IDs")
    require(len(empty) == len(set(empty)) == 1120, "empty IDs")
    require(set(positive).isdisjoint(empty), "classification disjoint")
    all_ids = sorted(positive + empty)
    require(len(all_ids) == 1152 and digest(all_ids) ==
            classification["frozen_registry_family_ids_sha256"], "classification exhaustion")
    require(set(positive) == {row["candidate_family_id"] for row in witnesses},
            "positive witness join")

    tree = family["tree_audit"]
    source_rows = tree["source_rows"]
    require(len(source_rows) == 24, "source tree rows")
    require(sum(row["tree_test_count"] for row in source_rows) == 824 and
            sum(row["leaf_count"] for row in source_rows) == 424 and
            max(row["maximum_depth"] for row in source_rows) == 13, "tree totals")
    require(sum(row["certified_empty_family_count"] for row in source_rows) == 1120 and
            sum(row["positive_family_count"] for row in source_rows) == 32, "source totals")
    for source in source_rows:
        leaves = source["leaf_rows"]
        require(len(leaves) == source["leaf_count"], "leaf count")
        prefix_cover([row["dyadic_path"] for row in leaves])
        require(all(row["possible_unknown_family_count"] == 0 for row in leaves),
                "empty leaves")
        require(all(sum(row["exclusion_reason_histogram"].values()) ==
                    row["excluded_candidate_count"] for row in leaves), "leaf exclusion sums")

    derivative = mono["audit"]
    derivative_rows = derivative["source_rows"]
    require(len(derivative_rows) == 16 and
            sum(row["tree_test_count"] for row in derivative_rows) == 112 and
            sum(row["leaf_count"] for row in derivative_rows) == 64, "derivative totals")
    for source in derivative_rows:
        prefix_cover([row["dyadic_path"] for row in source["leaf_rows"]])
        pattern = source["common_sign_pattern"]
        require(len(pattern) == 5 and all(value in (-1, 1) for value in pattern),
                "derivative signs")
        require(pattern[1] != 0 and pattern[3] != 0 and pattern[4] != 0,
                "monotonicity and Jacobian")
        require(all(row["signs"] == pattern for row in source["leaf_rows"]),
                "common derivative signs")

    field_result = fields["result"]
    rows = field_result["rows"]
    require(len(rows) == 32 and len({row["component_id"] for row in rows}) == 32,
            "numeric component rows")
    require({row["candidate_family_id"] for row in rows} == set(positive), "numeric positive join")
    require(min(row["F10_integer_upper"] for row in rows) == 3 and
            max(row["F10_integer_upper"] for row in rows) == 39 and
            sum(row["F10_integer_upper"] for row in rows) == 480, "numeric F10 replay")
    require(all(row["lower_p_level_sign"] * row["upper_p_level_sign"] == -1 and
                row["F_p_sign"] in (-1, 1) for row in rows), "numeric germ regularity")
    require(sum(Q(row["F13_current_variation_strict_upper"]) for row in rows) ==
            Q(4, 125000000), "F13 finite sum")
    require(sum(Q(row["F16_Piola_flux_cost_strict_upper"]) for row in rows) ==
            Q(4, 125000000), "F16 finite sum")
    return {
        "family_classification": "1152/1152",
        "positive_components": "32/32",
        "empty_families": "1120/1120",
        "numeric_F10_F13_F16_rows": "32/32",
        "status": "PASS",
    }


def deterministic(data: dict[str, Any]) -> None:
    proc = subprocess.run(
        [sys.executable, str(CERT), "--manifest-json", "--verifier", str(VERIFIER)],
        cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=300,
    )
    require(proc.returncode == 0, f"producer: {proc.stderr.decode().strip()}")
    require(proc.stdout == MANIFEST.read_bytes() and strict_json_path(MANIFEST) == data,
            "deterministic producer")


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
                cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=300,
            )
            require(proc.returncode == 0, "reemit producer")
            args.reemit.write_bytes(proc.stdout)
            require(args.reemit.read_bytes() == MANIFEST.read_bytes(), "reemit bytes")
            return 0
    except (CertError, OSError, ValueError, KeyError, TypeError, ArithmeticError,
            subprocess.SubprocessError) as exc:
        print(f"ROUND72_VERIFY_ERROR: {exc}", file=sys.stderr)
        return 1
    print("ROUND72 BASE-R1 FULL FAMILY ATLAS: PARTIAL_GLOBAL_ONLY")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
