#!/usr/bin/env python3
"""Producer for the Round-69 base-s return/incidence all-gate frontier."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from collections import Counter
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path
from typing import Any

from cm2_round68_common import (
    CertError, canonical_bytes, digest, require, sha256_path, strict_json_path,
    validate_pins,
)


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.round69.base-s-return-incidence-all-gate.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-round69-base-s-return-incidence-all-gate"
REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
VERIFIER = HERE / "cm2_round69_base_s_return_incidence_all_gate_verifier.py"
COMMON = HERE / "cm2_round68_common.py"

FULL_CORE = "cm2-gate34-full-core-return-adaptive-frontier-manifest-2026-07-18.json"
R1_FIELDS = "cm2-gate5-round25-r1-field-join-manifest-2026-07-18.json"
EMPTY_FACE = "cm2-gate5-round27-r1-empty-physical-face-join-manifest-2026-07-18.json"
FACE_ATLAS = "cm2-gate5-round28-limiting-physical-face-atlas-frontier-manifest-2026-07-18.json"
FIXED_ROOT = "cm2-round67-fixed-j-occurrence-owner-root-time-potential-frontier-manifest-2026-07-21.json"

PINS = {
    "cm2-sixty-eighth-direct-assault-2026-07-21.md":
        "ba769f9a2181321649124ca6a78bdc43a5c9d1740261c6b32bf54410adcd1fe7",
    "cm2-sixty-eighth-direct-assault-manifest-2026-07-21.sha256":
        "37f3fe971774519b6f938a709cb0838f36cbc5358fbcf7325bba8381f4b21078",
    "cm2-round68-common-root-all-gate-frontier-manifest-2026-07-21.json":
        "a9dd3e825f384f0a36db2745a8677505fb852a76fef2dd2fb9682bdc4573214f",
    "cm2_round68_common.py":
        "f705d61157d5cbbf41f7ad4c4e72c6ad3fbd0466f34651137f15a03d6789d856",
    FULL_CORE:
        "f79010c757e687cec2e8d7a8d617f3d94a3814731c58e960195c69107c446ad0",
    R1_FIELDS:
        "f6950d0a6ccf6984f888a102d846557e807becfddf3a95a72565e514934783e4",
    EMPTY_FACE:
        "9d900f2d0fee5ab8ad1a7e1f999e640ef88edc928ba6208987d1a74c93ca0e38",
    FACE_ATLAS:
        "ad385983a4152da3bc1d9c58a5a2fba1abb928466ecf9a9f61260b612bddf140",
    FIXED_ROOT:
        "97cb410b9e960d8331a37ef9203b040c9b1d86c3ed3d1ba6ba66a28c4e4ff400",
}


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def collect_return_atoms(value: Any, out: list[dict[str, Any]]) -> None:
    if isinstance(value, dict):
        if value.get("classification") == "RETURN_AT_1_INNER" and "source_box" in value:
            out.append(value)
        for child in value.values():
            collect_return_atoms(child, out)
    elif isinstance(value, list):
        for child in value:
            collect_return_atoms(child, out)


def compact_atom(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "absolute_inverse_invariant_area_Jacobian": row["absolute_inverse_invariant_area_Jacobian"],
        "atom_id": row["atom_id"],
        "classification": row["classification"],
        "depth": row["depth"],
        "destination_core_id": row["destination_core_id"],
        "dyadic_path": row["dyadic_path"],
        "log_invariant_area_Jacobian_distortion": row["log_invariant_area_Jacobian_distortion"],
        "source_box": row["source_box"],
        "source_core_id": row["source_core_id"],
    }


@lru_cache(maxsize=1)
def build_result() -> dict[str, Any]:
    validate_pins(HERE, PINS)
    full = strict_json_path(HERE / FULL_CORE)
    field_manifest = strict_json_path(HERE / R1_FIELDS)
    empty_manifest = strict_json_path(HERE / EMPTY_FACE)
    atlas_manifest = strict_json_path(HERE / FACE_ATLAS)
    fixed_manifest = strict_json_path(HERE / FIXED_ROOT)

    atoms: list[dict[str, Any]] = []
    collect_return_atoms(full, atoms)
    require(len(atoms) == 4216 and len({row["atom_id"] for row in atoms}) == 4216,
            "return atom count")
    touching = [row for row in atoms if Q(row["source_box"]["s"][0]) <= 0 <= Q(row["source_box"]["s"][1])]
    owned = [row for row in touching if Q(row["source_box"]["s"][0]) == 0]
    excluded = [row for row in touching if Q(row["source_box"]["s"][1]) == 0]
    require(len(touching) == 352 and len(owned) == len(excluded) == 176, "base fibre ownership")
    owned_ids = {row["atom_id"] for row in owned}
    require(owned_ids.isdisjoint({row["atom_id"] for row in excluded}), "owned/excluded disjoint")

    packets = field_manifest["result"]["R1_inner_candidate_field_packet_rows"]
    packet_map = {row["atom_id"]: row for row in packets}
    require(len(packet_map) == 4216 and owned_ids <= packet_map.keys(), "field packet map")
    selected_packets = [packet_map[atom_id] for atom_id in sorted(owned_ids)]
    for packet in selected_packets:
        atom = next(row for row in owned if row["atom_id"] == packet["atom_id"])
        domain = packet["candidate_local_slots"]["nonempty_or_empty_domain_proof"]["payload"]["candidate_domain"]
        guard = packet["parameter_guard"]
        require(domain["closed_box_provenance"] == atom["source_box"], "packet source box")
        require(guard == {
            "internal_boundary_owner": "right_leaf_via_lower_closed_upper_open_convention",
            "lower_closed": True, "s_lower": "0", "s_upper": atom["source_box"]["s"][1],
            "upper_closed": False,
        }, "half-open base owner")
        require(packet["roof"] == 1 and packet["roof_level_j"] == 0, "depth-one packet")

    lower_mass = Q(0)
    upper_mass = Q(0)
    global_window = Q(1, 200)
    for row in owned:
        s_lo, s_hi = map(Q, row["source_box"]["s"])
        parameter_fraction = (s_hi - s_lo) / global_window
        lower_mass += Q(row["parameter_averaged_unnormalized_collision_mass_lower"]) / parameter_fraction
        upper_mass += Q(row["parameter_averaged_unnormalized_collision_mass_upper"]) / parameter_fraction
        require(row["absolute_inverse_invariant_area_Jacobian"] == "1", "area Jacobian")
        require(row["log_invariant_area_Jacobian_distortion"] == "0", "area distortion")
        require(row["strict_next_collision_owner_inherited_from_whole_parent_core"] is True,
                "strict owner")
        require(row["positive_two_dimensional_source_rectangle_at_each_s"] is True,
                "positive source rectangle")
    require(lower_mass == Q(191, 8000000) and upper_mass == Q(267591, 8000000000),
            "fixed-s mass ledger")

    edge_counts = Counter((row["source_core_id"], row["destination_core_id"]) for row in owned)
    edge_rows = [{"source_core_id": source, "destination_core_id": destination, "atom_count": count}
                 for (source, destination), count in sorted(edge_counts.items())]
    require(len(edge_rows) == 16 and len({row["source_core_id"] for row in edge_rows}) == 16,
            "core edge graph")
    require(all((destination, source) in edge_counts for source, destination in edge_counts),
            "reciprocal edges")
    reciprocal_pairs = {tuple(sorted((source, destination))) for source, destination in edge_counts}
    require(len(reciprocal_pairs) == 8, "reciprocal pair count")

    depth_histogram = dict(sorted(Counter(row["depth"] for row in owned).items()))
    require(depth_histogram == {13: 16, 14: 116, 15: 44}, "depth histogram")
    compact_rows = sorted((compact_atom(row) for row in owned), key=lambda row: row["atom_id"])
    require(digest(compact_rows) == "d4df19750422881dce4947ff16c0d5889706a4ee0487cefc7ae09c8ea370a228",
            "compact root digest")

    empty = empty_manifest["result"]["R1_empty_physical_face_F10_F13_slot_registry"]
    maturity = empty_manifest["result"]["Gate5_R1_candidate_local_maturity"]
    require(empty["R1_inner_atom_count"] == 4216 and
            empty["physical_occurrence_face_count"] == 64 and
            empty["atom_occurrence_pair_audit_count"] == 269824 and
            empty["certified_intersecting_atom_occurrence_pair_count"] == 0,
            "all-atom occurrence audit")
    require(maturity["candidate_local_maturity_after_exact_empty_face_join"] == "13/18",
            "local maturity")

    occurrence = atlas_manifest["result"]["moving_occurrence_coarea_DQ_face_seed_registry"]
    require(occurrence["full_C24_core_occurrence_pair_audit_count"] == 1536 and
            occurrence["intersecting_full_C24_core_occurrence_face_pairs"] == 0,
            "core occurrence disjointness")
    fixed = fixed_manifest["result"]["actual_fixed_j_subroot"]
    require(fixed["base_law"] == "finite standard-Borel endpoint-coarea occurrence law m_occ",
            "fixed-j source law")

    local_fields = [row["field"] for row in maturity["rows"][:13]]
    require(len(local_fields) == 13 and maturity["rows"][13]["candidate_local_R1_atom_slot_count"] == 0,
            "F14 frontier")

    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "append_only": True,
            "old_artifacts_modified": False,
            "pinned_chain": PINS,
        },
        "actual_base_s_return_root": {
            "status": "CERTIFIED_POSITIVE_GRAPH_SUPPORTED_BASE_PARAMETER_DEPTH1_RETURN_ROOT",
            "parameter": "s=0",
            "all_return_atoms": 4216,
            "closed_parameter_boxes_touching_zero": 352,
            "owned_by_lower_closed_upper_open_rule": 176,
            "excluded_boxes_ending_at_zero": 176,
            "atom_ids_sha256": digest(sorted(owned_ids)),
            "compact_atom_rows_sha256": digest(compact_rows),
            "packet_ids_sha256": digest(sorted(row["r1_candidate_field_packet_id"] for row in selected_packets)),
            "homogeneity_ids_sha256": digest(sorted(row["physical_homogeneity_subbranch_id"] for row in selected_packets)),
            "depth_histogram": {str(key): value for key, value in depth_histogram.items()},
            "source_core_count": len({row["source_core_id"] for row in owned}),
            "destination_core_count": len({row["destination_core_id"] for row in owned}),
            "directed_core_edge_count": len(edge_rows),
            "reciprocal_unordered_core_pair_count": len(reciprocal_pairs),
            "edge_rows": edge_rows,
            "fixed_s_unnormalized_collision_mass_strict_lower": qstr(lower_mass),
            "fixed_s_unnormalized_collision_mass_upper": qstr(upper_mass),
            "every_atom_strict_first_owner": True,
            "every_atom_lands_inside_declared_core_at_time1": True,
            "every_atom_inverse_collision_area_Jacobian": "1",
            "every_atom_log_collision_area_Jacobian_distortion": "0",
            "all_depth_invariant_return_graph": "NOT_CERTIFIED",
        },
        "direct_equality_obstruction": {
            "status": "CERTIFIED_TYPED_SUPPORT_DISJOINTNESS__ROUND68_DIRECT_EQUALITY_ROUTE_REJECTED",
            "raw_occurrence_carrier_type": "moving_first_event_grazing_occurrence_face",
            "return_carrier_type": "strict_C24_core_interior_return_atom",
            "full_core_occurrence_pair_count": 1536,
            "full_core_occurrence_reason_histogram": occurrence["full_C24_core_occurrence_pair_reason_histogram"],
            "full_core_occurrence_intersection_count": 0,
            "all_atom_occurrence_pair_count": 269824,
            "all_atom_occurrence_intersection_count": 0,
            "selected_base_root_occurrence_pair_count": 176 * 64,
            "selected_base_root_occurrence_intersection_count": 0,
            "owner_restriction_can_create_source_support": False,
            "recordwise_source_point_equality_is_correct_join": False,
        },
        "typed_incidence_correction": {
            "status": "EXACT_REGISTRY_TYPE_CORRECTION_CERTIFIED__FIRST_NONEMPTY_PULLBACK_COMPONENT_OPEN",
            "node_sorts": ["path_cell", "physical_face", "one_sided_trace"],
            "path_cell_key": ["component_id", "return_depth", "path_key", "owner_atom"],
            "face_key": ["component_id", "time_j", "carrier_family_or_seed_id", "connected_rank"],
            "trace_key": ["component_id", "time_j", "carrier_family_or_seed_id", "connected_rank", "side_label"],
            "edge_semantics": "FACE_IS_BOUNDARY_OR_PULLBACK_CARRIER_INCIDENT_TO_PATH_CELL__NOT_EQUAL_TO_INTERIOR_POINT",
            "R1_inner_moving_occurrence_incidence": "CERTIFIED_EMPTY",
            "arbitrary_Rn_occurrence_pullback_component_ids_materialized": 0,
            "arbitrary_Rn_connected_ranks_materialized": 0,
            "next_required_object": "ONE_NONEMPTY_TIME_QUALIFIED_PULLBACK_COMPONENT_WITH_CONNECTED_RANK_AND_TWO_TRACES",
        },
        "gate13_attachment_audit": {
            "status": "ACTUAL_BASE_ROOT_AVAILABLE__KEYED_REPRESENTATIVE_AND_UNIFORM_OPERATOR_ROWS_ABSENT",
            "base_root_exports": [
                "restriction_id", "return_component", "collision_index", "primitive_key",
                "owner_key", "rank_zero_component", "word_cell", "endpoint_coordinate",
                "root_coordinate",
            ],
            "missing_on_same_keys": [
                "Gate1_Q_E_u_v_representative", "actual_stable_plaque_side",
                "positive_all_cell_material_radius", "uniform_Piola_remainder",
                "two_sided_physical_trace_current_bound", "stopped_MT_DQ_bound",
            ],
            "Gate1_actual_common_rows": "0/8",
            "Gate3": "NOT_CERTIFIED",
        },
        "gate24_depth1_graph_audit": {
            "status": "CERTIFIED_ACTUAL_BASE_PARAMETER_DEPTH1_GRAPH__ALL_DEPTH_STABLE_PRODUCT_OPEN",
            "owned_atom_nodes": 176,
            "core_nodes": 16,
            "directed_core_edges": 16,
            "reciprocal_core_pairs": 8,
            "Gate4_field4": "PARTIAL_ACTUAL_DEPTH1_BASE_PARAMETER_GRAPH",
            "actual_invariant_stable_plaques": 0,
            "actual_stable_holonomy_rows": 0,
            "all_depth_commuting_square": "NOT_CERTIFIED",
            "marker_saturation": "NOT_CERTIFIED",
            "strict_path_budget": "NOT_CERTIFIED",
            "physical_strong_recipient": "NOT_CERTIFIED",
            "Gate2_official_fields": "0/17",
            "Gate4_landing_join": "1/7__FIELDS_1_4_7_PARTIAL",
        },
        "gate5_same_root_local_packet": {
            "status": "CERTIFIED_176_ACTUAL_BASE_ROOT_PACKETS_F1_THROUGH_F13__NO_GLOBAL_BLOCK",
            "candidate_local_fields": local_fields,
            "selected_candidate_local_slot_count": 176 * 13,
            "selected_empty_F10_slots": 176,
            "selected_empty_F13_current_trace_slots": 176,
            "selected_empty_F10_F13_slot_count": 352,
            "candidate_local_maturity": "13/18",
            "first_missing_candidate_local_field": "regular_density_operator_cost",
            "F14_through_F18": "NOT_CERTIFIED",
            "complete_18_field_operator_blocks": 0,
            "global_Gate5_maturity": "10/18__COMPLETE_BLOCKS_0",
            "seven_missing_positive_potential_sectors_closed": "0/7",
        },
        "technology_boundary": {
            "checked_on": "2026-07-21",
            "moving_scatterers_linear_response_results": 1,
            "moving_scatterers_result_relevant": False,
            "dispersing_billiards_stable_holonomy_results": 0,
            "time_dependent_billiards_transfer_operator_results": 0,
            "sequential_dispersing_billiards_results": ["2502.07765v2", "2104.06947v3"],
            "new_typed_incidence_or_moving_boundary_operator_theorem_found": False,
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
    result = build_result()
    require(REPORT.is_file() and verifier.is_file() and COMMON.is_file(), "artifact presence")
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-json", action="store_true")
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--verifier", type=Path, default=VERIFIER)
    args = parser.parse_args()
    try:
        if args.replay:
            result = build_result()
            print(json.dumps({
                "owned_atoms": result["actual_base_s_return_root"]["owned_by_lower_closed_upper_open_rule"],
                "selected_pair_audit": result["direct_equality_obstruction"]["selected_base_root_occurrence_pair_count"],
                "status": "PASS",
            }, sort_keys=True))
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
        print(f"ROUND69_CERT_ERROR: {exc}", file=sys.stderr)
        return 1
    print("ROUND69 BASE-S RETURN AND INCIDENCE: PARTIAL_ONLY")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
