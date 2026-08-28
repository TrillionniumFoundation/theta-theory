#!/usr/bin/env python3
"""Independent verifier for the Round-69 base-s return/incidence frontier."""

from __future__ import annotations

import argparse
import copy
import json
import subprocess
import sys
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round68_common import (
    CertError, digest, require, semantic_mutation_test, sha256_path,
    strict_json_path, strict_json_self_test, validate_pins,
)
from cm2_round69_base_s_return_incidence_all_gate_cert import (
    COMMON, EMPTY_FACE, FACE_ATLAS, FULL_CORE, MANIFEST_SCHEMA, PINS,
    RESULT_SCHEMA, build_result,
)


HERE = Path(__file__).resolve().parent
PREFIX = "cm2-round69-base-s-return-incidence-all-gate"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
CERT = HERE / "cm2_round69_base_s_return_incidence_all_gate_cert.py"
VERIFIER = Path(__file__).resolve()


def integrity(data: dict[str, Any], check_files: bool = True) -> None:
    require(data["schema"] == MANIFEST_SCHEMA, "manifest schema")
    require(data["result"]["schema"] == RESULT_SCHEMA, "result schema")
    require(data["pins"] == PINS, "manifest pins")
    if check_files:
        validate_pins(HERE, PINS)
        require(data["report_sha256"] == sha256_path(REPORT), "report hash")
        require(data["certificate_sha256"] == sha256_path(CERT), "certificate hash")
        require(data["verifier_sha256"] == sha256_path(VERIFIER), "verifier hash")
        require(data["common_sha256"] == sha256_path(COMMON), "common hash")
    replay = copy.deepcopy(data["result"])
    claimed = replay.pop("internal_replay_digest")
    require(claimed == digest(replay), "internal result digest")
    require(data["verdict"] == data["result"]["strict_status"], "verdict")


def semantics(result: dict[str, Any]) -> None:
    root = result["actual_base_s_return_root"]
    require(root["status"] == "CERTIFIED_POSITIVE_GRAPH_SUPPORTED_BASE_PARAMETER_DEPTH1_RETURN_ROOT",
            "root status")
    require(root["parameter"] == "s=0" and root["all_return_atoms"] == 4216, "root scope")
    require(root["closed_parameter_boxes_touching_zero"] == 352 and
            root["owned_by_lower_closed_upper_open_rule"] == 176 and
            root["excluded_boxes_ending_at_zero"] == 176, "half-open split")
    require(root["depth_histogram"] == {"13": 16, "14": 116, "15": 44}, "depths")
    require(root["source_core_count"] == root["destination_core_count"] == 16 and
            root["directed_core_edge_count"] == 16 and
            root["reciprocal_unordered_core_pair_count"] == 8, "edge graph")
    require(sum(row["atom_count"] for row in root["edge_rows"]) == 176, "edge mass")
    edges = {(row["source_core_id"], row["destination_core_id"]) for row in root["edge_rows"]}
    require(len(edges) == 16 and all((destination, source) in edges for source, destination in edges),
            "edge reciprocity")
    require(Q(root["fixed_s_unnormalized_collision_mass_strict_lower"]) == Q(191, 8000000),
            "mass lower")
    require(Q(root["fixed_s_unnormalized_collision_mass_upper"]) == Q(267591, 8000000000),
            "mass upper")
    require(root["every_atom_strict_first_owner"] is True and
            root["every_atom_lands_inside_declared_core_at_time1"] is True and
            root["every_atom_inverse_collision_area_Jacobian"] == "1" and
            root["every_atom_log_collision_area_Jacobian_distortion"] == "0",
            "root physical rows")

    obstruction = result["direct_equality_obstruction"]
    require(obstruction["full_core_occurrence_pair_count"] == 24 * 64 and
            obstruction["all_atom_occurrence_pair_count"] == 4216 * 64 and
            obstruction["selected_base_root_occurrence_pair_count"] == 176 * 64,
            "pair counts")
    require(obstruction["full_core_occurrence_intersection_count"] == 0 and
            obstruction["all_atom_occurrence_intersection_count"] == 0 and
            obstruction["selected_base_root_occurrence_intersection_count"] == 0,
            "pair disjointness")
    require(sum(obstruction["full_core_occurrence_reason_histogram"].values()) == 1536,
            "reason exhaustion")
    require(obstruction["owner_restriction_can_create_source_support"] is False and
            obstruction["recordwise_source_point_equality_is_correct_join"] is False,
            "typed negative")

    incidence = result["typed_incidence_correction"]
    require(incidence["node_sorts"] == ["path_cell", "physical_face", "one_sided_trace"],
            "node sorts")
    require(len(incidence["path_cell_key"]) == 4 and len(incidence["face_key"]) == 4 and
            len(incidence["trace_key"]) == 5, "incidence key arity")
    require(incidence["R1_inner_moving_occurrence_incidence"] == "CERTIFIED_EMPTY" and
            incidence["arbitrary_Rn_occurrence_pullback_component_ids_materialized"] == 0 and
            incidence["arbitrary_Rn_connected_ranks_materialized"] == 0,
            "incidence frontier")

    gate13 = result["gate13_attachment_audit"]
    require(len(gate13["base_root_exports"]) == 9 and len(gate13["missing_on_same_keys"]) == 6,
            "Gate13 fields")
    require(gate13["Gate1_actual_common_rows"] == "0/8" and gate13["Gate3"] == "NOT_CERTIFIED",
            "Gate13 state")
    gate24 = result["gate24_depth1_graph_audit"]
    require(gate24["owned_atom_nodes"] == 176 and gate24["core_nodes"] == 16 and
            gate24["directed_core_edges"] == 16 and gate24["reciprocal_core_pairs"] == 8,
            "Gate24 graph")
    require(gate24["actual_invariant_stable_plaques"] == 0 and
            gate24["actual_stable_holonomy_rows"] == 0 and
            gate24["Gate2_official_fields"] == "0/17", "Gate24 nonpromotion")
    gate5 = result["gate5_same_root_local_packet"]
    require(len(gate5["candidate_local_fields"]) == 13 and
            gate5["selected_candidate_local_slot_count"] == 176 * 13 and
            gate5["selected_empty_F10_slots"] == gate5["selected_empty_F13_current_trace_slots"] == 176 and
            gate5["selected_empty_F10_F13_slot_count"] == 352, "Gate5 packet")
    require(gate5["candidate_local_maturity"] == "13/18" and
            gate5["first_missing_candidate_local_field"] == "regular_density_operator_cost" and
            gate5["complete_18_field_operator_blocks"] == 0 and
            gate5["seven_missing_positive_potential_sectors_closed"] == "0/7", "Gate5 frontier")

    technology = result["technology_boundary"]
    require(technology["checked_on"] == "2026-07-21" and
            technology["moving_scatterers_linear_response_results"] == 1 and
            technology["moving_scatterers_result_relevant"] is False and
            technology["dispersing_billiards_stable_holonomy_results"] == 0 and
            technology["time_dependent_billiards_transfer_operator_results"] == 0 and
            technology["sequential_dispersing_billiards_results"] == ["2502.07765v2", "2104.06947v3"] and
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
    data = strict_json_path(HERE / FULL_CORE)
    atoms: list[dict[str, Any]] = []

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            if value.get("classification") == "RETURN_AT_1_INNER" and "source_box" in value:
                atoms.append(value)
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(data)
    touching = [row for row in atoms if Q(row["source_box"]["s"][0]) <= 0 <= Q(row["source_box"]["s"][1])]
    owned = [row for row in touching if Q(row["source_box"]["s"][0]) == 0]
    excluded = [row for row in touching if Q(row["source_box"]["s"][1]) == 0]
    require((len(atoms), len(touching), len(owned), len(excluded)) == (4216, 352, 176, 176),
            "independent ownership replay")
    lower = Q(0)
    upper = Q(0)
    edges: Counter[tuple[str, str]] = Counter()
    compact = []
    for row in owned:
        s_lo, s_hi = map(Q, row["source_box"]["s"])
        fraction = (s_hi - s_lo) / Q(1, 200)
        lower += Q(row["parameter_averaged_unnormalized_collision_mass_lower"]) / fraction
        upper += Q(row["parameter_averaged_unnormalized_collision_mass_upper"]) / fraction
        edges[(row["source_core_id"], row["destination_core_id"])] += 1
        compact.append({key: row[key] for key in (
            "absolute_inverse_invariant_area_Jacobian", "atom_id", "classification", "depth",
            "destination_core_id", "dyadic_path", "log_invariant_area_Jacobian_distortion",
            "source_box", "source_core_id",
        )})
    compact.sort(key=lambda row: row["atom_id"])
    require(lower == Q(191, 8000000) and upper == Q(267591, 8000000000), "independent mass")
    require(len(edges) == 16 and all(reverse in edges for reverse in ((b, a) for a, b in edges)),
            "independent graph")
    require(digest(compact) == "d4df19750422881dce4947ff16c0d5889706a4ee0487cefc7ae09c8ea370a228",
            "independent compact digest")
    atlas = strict_json_path(HERE / FACE_ATLAS)["result"]["moving_occurrence_coarea_DQ_face_seed_registry"]
    empty = strict_json_path(HERE / EMPTY_FACE)["result"]["R1_empty_physical_face_F10_F13_slot_registry"]
    require(atlas["intersecting_full_C24_core_occurrence_face_pairs"] == 0 and
            empty["certified_intersecting_atom_occurrence_pair_count"] == 0, "independent disjointness")
    return {
        "return_atoms": "4216/4216",
        "base_owned_atoms": "176/176",
        "selected_occurrence_pairs": "11264/11264_DISJOINT",
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
        print(f"ROUND69_VERIFY_ERROR: {exc}", file=sys.stderr)
        return 1
    print("ROUND69 BASE-S RETURN AND INCIDENCE: PARTIAL_ONLY")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
