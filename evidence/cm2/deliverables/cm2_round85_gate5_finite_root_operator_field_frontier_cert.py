#!/usr/bin/env python3
"""Same-key F10/F13/F14--F18 audit on 152 finite-root material windows."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import cm2_gate5_round27_r1_empty_physical_face_join_cert as empty_cert


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round85.gate5-finite-root-operator-field-frontier.v1"
ROUND69 = HERE / "cm2-round69-base-s-return-incidence-all-gate-manifest-2026-07-21.json"
WINDOW = HERE / "cm2-round85-gate3-s0-two-sided-material-window-2026-07-22.json"
R1_FIELDS = HERE / "cm2-gate5-round25-r1-field-join-manifest-2026-07-18.json"
EMPTY = HERE / "cm2-gate5-round27-r1-empty-physical-face-join-manifest-2026-07-18.json"
ROUND73 = HERE / "cm2-round73-base-r1-shared-quotient-manifest-2026-07-21.json"
ROUND67 = HERE / "cm2-gate5-round67-direct-positive-potential-attenuation-frontier-manifest-2026-07-21.json"
FROZEN_PINS = {
    "round69_base_root": "08d996d52d6aa8ea3b716a46b51d6ae8f0a6b4b9e24c9fab402afe88059bc838",
    "round85_material_windows": "81356d91e1725c9f454ac010b264a0bd1fbd92b2892cca602f1ff5f9ae64b2c7",
    "round25_packet_registry": "f6950d0a6ccf6984f888a102d846557e807becfddf3a95a72565e514934783e4",
    "round27_empty_slots": "9d900f2d0fee5ab8ad1a7e1f999e640ef88edc928ba6208987d1a74c93ca0e38",
    "round27_empty_slot_source": "aabe7f375036e68b742695f27a3a274bc47f594e547579e3592cf97f46989c43",
    "round73_base_fibre": "960e05fdf246863aacfdaeb13e5729cad4303e516de4a6984c033889ed9c851c",
    "round67_terminal_frontier": "fa35f45bd9d31976b62d7dfd988b774ec5404a5bd3755994e627711857710cfd",
}


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_load(path: Path) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result: raise ValueError(f"duplicate key: {key}")
            result[key] = value
        return result
    value = json.loads(
        path.read_text(), object_pairs_hook=unique,
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
    )
    if not isinstance(value, dict): raise ValueError("top-level object")
    return value


def count_key(value: Any, target: str) -> int:
    if isinstance(value, dict):
        return int(target in value) + sum(count_key(child, target) for child in value.values())
    if isinstance(value, list):
        return sum(count_key(child, target) for child in value)
    return 0


def replay_empty_slots() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    loaded = empty_cert.load_dependencies()
    occurrence_rows, _carriers, _physical = empty_cert.replay_physical_rows(loaded)
    core_map, core_rows = empty_cert.replay_cores()
    packets = loaded["cm2-gate5-round25-r1-field-join-manifest-2026-07-18.json"][
        "result"
    ]["R1_inner_candidate_field_packet_rows"]
    return empty_cert.empty_face_slots(packets, occurrence_rows, core_map, core_rows)


def build() -> dict[str, Any]:
    actual_pins = {
        "round69_base_root": file_digest(ROUND69),
        "round85_material_windows": file_digest(WINDOW),
        "round25_packet_registry": file_digest(R1_FIELDS),
        "round27_empty_slots": file_digest(EMPTY),
        "round27_empty_slot_source": file_digest(HERE / "cm2_gate5_round27_r1_empty_physical_face_join_cert.py"),
        "round73_base_fibre": file_digest(ROUND73),
        "round67_terminal_frontier": file_digest(ROUND67),
    }
    if actual_pins != FROZEN_PINS: raise ValueError("frozen upstream pin mismatch")
    round69 = strict_load(ROUND69)
    window = strict_load(WINDOW)
    r1 = strict_load(R1_FIELDS)
    empty = strict_load(EMPTY)
    round73 = strict_load(ROUND73)
    round67 = strict_load(ROUND67)

    root = round69["result"]["gate5_same_root_local_packet"]
    if root["candidate_local_maturity"] != "13/18" or root["selected_empty_F10_F13_slot_count"] != 352:
        raise ValueError("Round69 packet maturity")
    windows = window["result"]["evidence"]["window_rows"]
    if len(windows) != 152: raise ValueError("material window census")
    window_ids = {row["positive_atom_id"] for row in windows}
    if len(window_ids) != 152: raise ValueError("material window atom keys")
    packets = r1["result"]["R1_inner_candidate_field_packet_rows"]
    packet_map = {row["atom_id"]: row for row in packets}
    if len(packet_map) != 4216 or not window_ids <= packet_map.keys():
        raise ValueError("same-key packet crosswalk")

    slots, slot_registry = replay_empty_slots()
    empty_manifest_registry = empty["result"]["R1_empty_physical_face_F10_F13_slot_registry"]
    if slot_registry != empty_manifest_registry: raise ValueError("Round27 slot exact replay")
    slot_map = {(row["atom_id"], row["field_name"]): row for row in slots}
    field10 = empty_cert.F10
    field13 = empty_cert.F13
    attachment_rows = []
    for material in sorted(windows, key=lambda row: row["positive_atom_id"]):
        atom_id = material["positive_atom_id"]
        packet = packet_map[atom_id]
        f10 = slot_map[(atom_id, field10)]
        f13 = slot_map[(atom_id, field13)]
        if f10["coarea_density_regular_cost"] != "0" or f10["physical_occurrence_intersection_count"] != 0:
            raise ValueError("same-key F10 empty slot")
        if f13["moving_boundary_current_on_fixed_R1_inner_restriction"] != "0" or f13["trace_pair_count"] != 0:
            raise ValueError("same-key F13 empty slot")
        attachment_rows.append({
            "atom_id": atom_id,
            "material_positive_atom_id": material["positive_atom_id"],
            "material_negative_atom_id": material["negative_atom_id"],
            "candidate_packet_id": packet["r1_candidate_field_packet_id"],
            "physical_homogeneity_subbranch_id": packet["physical_homogeneity_subbranch_id"],
            "F10_slot_id": f10["immutable_slot_id"],
            "F10_coarea_density_regular_cost": "0",
            "F13_slot_id": f13["immutable_slot_id"],
            "F13_current": "0",
            "F13_trace_pair_count": 0,
            "candidate_local_maturity": "13/18",
        })

    maturity_rows = empty["result"]["Gate5_R1_candidate_local_maturity"]["rows"]
    downstream = empty["result"]["F14_F18_frontier"]["F14_through_F18_rows"]
    if [row["candidate_local_R1_atom_slot_count"] for row in maturity_rows[13:18]] != [0] * 5:
        raise ValueError("F14--F18 slot frontier")
    if [row["index"] for row in downstream] != [14, 15, 16, 17, 18]:
        raise ValueError("F14--F18 field order")
    base_attachment = round73["result"]["base_fibre_field_attachment"]
    if base_attachment["F16_Piola_flux_sum_strict_upper"] != "4/125000000":
        raise ValueError("Round73 aggregate F16")
    if count_key(round73, "atom_id") != 0 or count_key(round73, "r1_candidate_field_packet_id") != 0:
        raise ValueError("unexpected Round73 atom-key attachment")
    terminal = round67["result"]["terminal_moment_identity"]
    if terminal["actual_terminal_exponential_moment"] != "NOT_CERTIFIED":
        raise ValueError("terminal moment frontier")

    field_rows = [
        {"index": 14, "field": "regular_density_operator_cost", "same_key_slot_count": 0,
         "status": "NOT_CERTIFIED", "obstruction": "F10=0 empty-face slots do not provide a recovered strong density-operator block"},
        {"index": 15, "field": "standard_family_operator_cost", "same_key_slot_count": 0,
         "status": "NOT_CERTIFIED", "obstruction": "no raw-Orlicz recovery, standard-family assembly, or positive cemetery cost on these atom keys"},
        {"index": 16, "field": "flux_face_operator_cost", "same_key_slot_count": 0,
         "status": "NOT_CERTIFIED", "obstruction": "Round73 has a base-fibre aggregate F16 bound but exports zero atom or candidate-packet keys"},
        {"index": 17, "field": "dynamic_test_operator_cost", "same_key_slot_count": 0,
         "status": "NOT_CERTIFIED", "obstruction": "no all-input anisotropic recipient, suffix bound, or atom-keyed bulk current operator"},
        {"index": 18, "field": "operator_phase_block", "same_key_slot_count": 0,
         "status": "NOT_CERTIFIED", "obstruction": "no complete preceding operator block and no actual terminal exponential moment/kernel"},
    ]
    evidence = {
        "finite_material_window_atom_count": len(window_ids),
        "same_key_candidate_packet_count": len(attachment_rows),
        "same_key_F10_empty_slot_count": len(attachment_rows),
        "same_key_F13_empty_slot_count": len(attachment_rows),
        "same_key_F14_through_F18_slot_counts": {f"F{index}": 0 for index in range(14, 19)},
        "round73_atom_id_key_count": count_key(round73, "atom_id"),
        "round73_candidate_packet_key_count": count_key(round73, "r1_candidate_field_packet_id"),
        "round73_unattached_base_fibre_F16_bound": base_attachment["F16_Piola_flux_sum_strict_upper"],
        "actual_terminal_exponential_moment": terminal["actual_terminal_exponential_moment"],
        "attachment_rows": attachment_rows,
        "field_rows": field_rows,
    }
    result = {
        "status": "CERTIFIED_SAME_KEY_AVAILABILITY_FRONTIER__152_PACKETS_REMAIN_13_OF_18",
        "scope": "152 Round69 owner atoms with Round85 finite-root two-sided material windows",
        "candidate_local_maturity_before": "13/18",
        "candidate_local_maturity_after": "13/18",
        "new_F14_through_F18_fields_installed": 0,
        "complete_18_field_operator_blocks": 0,
        "global_Gate5": "NOT_CERTIFIED__MATURITY_10_OF_18_BLOCKS_0",
        "strict_nonclaims": [
            "empty F10/F13 slots are not nonzero face operator costs",
            "the Round73 base-fibre aggregate is not attached without atom keys",
            "finite-root material windows do not imply all-depth terminal control",
            "no abstract operator or terminal-kernel model is imported",
        ],
        "evidence": evidence,
        "evidence_sha256": digest(evidence),
    }
    return {"schema": SCHEMA, "pins": dict(FROZEN_PINS), "result": result, "result_sha256": digest(result)}


def main() -> int:
    json.dump(build(), sys.stdout, sort_keys=True, indent=2, allow_nan=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__": raise SystemExit(main())
