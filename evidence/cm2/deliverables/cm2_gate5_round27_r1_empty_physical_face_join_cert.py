#!/usr/bin/env python3
"""Round-27 Gate-5 F10/F13 empty physical-face join on R1 inner atoms.

The 64 frozen collision-occurrence carriers are genuine moving grazing
faces.  They must not be identified with the four stationary dyadic faces of
an adaptive R1 box.  This certificate instead audits the actual physical
intersection.  Every R1 inner atom inherits one of the 24 compact cores.  On
each core the selected first collision is strict against the complete
retained candidate list and its target coordinate satisfies |p|<3/10.  On an
occurrence carrier the event target is tangent and p=epsilon, hence |p|=1.
If the event target differs from the selected target, strict first ownership
also excludes the carrier.  Thus all 64 physical occurrence faces have empty
intersection with every one of the 4,216 R1-inner atoms.

The empty intersection is a positive typed result, not a missing join.  It
installs candidate-local F10 as the regularity cost of an empty physical
coarea family (empty sum zero), and F13 as the corresponding empty moving
current with an empty trace-pair family.  No artificial phase face is used as
a physical carrier.  The result is local to strict inner rectangles: it does
not construct the singular faces of the limiting R1 partition, a global DQ
atlas, F14--F18, or any Gate-5 credit.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as adaptive_cert
import cm2_gate34_occurrence_boundary_recovery_carrier_cert as recovery_cert
import cm2_gate3_depth_one_fixed_gauge_dq_cert as dq_cert
import cm2_gate5_round26_r1_f10_f13_frontier_cert as round26_cert


HERE = Path(__file__).resolve().parent

DEPENDENCIES = {
    "cm2_gate5_round26_r1_f10_f13_frontier_cert.py": (
        "aaf30efeb424cf2ab9903e52902bc5335452e2c707216765a6e87e833bd29ee4"
    ),
    "cm2-gate5-round26-r1-f10-f13-frontier-manifest-2026-07-18.json": (
        "2078787d2f4bb990be8a20570a1ca5722ed7bca5f5ff4e0fbf77408c2ca30b4a"
    ),
    "cm2-gate5-round25-r1-field-join-manifest-2026-07-18.json": (
        "f6950d0a6ccf6984f888a102d846557e807becfddf3a95a72565e514934783e4"
    ),
    "cm2_gate25_physical_return_core_registry_cert.py": (
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"
    ),
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json": (
        "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42"
    ),
    "cm2_gate34_full_core_return_adaptive_frontier_cert.py": (
        "d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24"
    ),
    "cm2_gate3_depth_one_fixed_gauge_dq_cert.py": (
        "8ce2490ee2b2bdfc251ac1892cb260e40f3eb5d87ce7f232c2076a10c4a9c066"
    ),
    "cm2-gate3-depth-one-fixed-gauge-dq-manifest-2026-07-15.json": (
        "284b25ac30dd86a01bd0faaa7c0a97ee47839670e3cde4309936235badf5fd52"
    ),
    "cm2_gate34_occurrence_boundary_recovery_carrier_cert.py": (
        "9e69879f921681da4a8eeda9a2af8755c3713151128027784e72cd12896a053a"
    ),
    "cm2-gate34-occurrence-boundary-recovery-carrier-manifest-2026-07-17.json": (
        "dd16bd1e3407a6f886ddbf1270ca7ff7289a7d6792e81235f69014cafaf49cb5"
    ),
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json": (
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866"
    ),
}

F10 = "coarea_density_regular_bound"
F13 = "moving_boundary_DQ_current_and_two_traces"


class DuplicateKeyError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def no_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def parse_json_text(text: str) -> Any:
    return json.loads(
        text,
        object_pairs_hook=no_duplicate_pairs,
        parse_constant=lambda token: (_ for _ in ()).throw(
            ValueError(f"non-finite JSON constant: {token}")
        ),
    )


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_dependencies() -> dict[str, dict[str, Any]]:
    loaded: dict[str, dict[str, Any]] = {}
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        require(path.is_file(), f"missing dependency: {name}")
        require(not path.is_symlink(), f"symlink dependency: {name}")
        require(path.resolve().parent == HERE, f"unsafe dependency: {name}")
        require(sha256_path(path) == expected, f"dependency hash: {name}")
        if path.suffix == ".json":
            value = parse_json_text(path.read_text(encoding="utf-8"))
            require(isinstance(value, dict), f"dependency type: {name}")
            loaded[name] = value

    prior = loaded[
        "cm2-gate5-round26-r1-f10-f13-frontier-manifest-2026-07-18.json"
    ]
    require(
        prior["result"]["Gate5_R1_candidate_local_maturity"]
        ["candidate_local_maturity_after_independent_join"] == "11/18",
        "round26 maturity",
    )
    require(prior["verdict"]["global_Gate5_maturity"] == "4/18_UNCHANGED", "Gate5")

    core_manifest = loaded[
        "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json"
    ]
    core_registry = core_manifest["result"]["physical_return_core_registry"]
    require(core_registry["physical_compact_homogeneous_core_count"] == 24, "cores")
    require(core_registry["all_cores_uniform_on_full_parameter_window"] is True, "uniform")
    require(
        core_registry["all_cores_strict_first_hit_against_complete_retained_candidate_list"]
        is True,
        "first owner",
    )
    require(
        core_manifest["result"]["remaining_operator_frontier"]
        ["branch_internal_no_singularity_cut"] is True,
        "no internal singularity cut",
    )

    dq = loaded["cm2-gate3-depth-one-fixed-gauge-dq-manifest-2026-07-15.json"]
    require(dq["verdict"]["complete_depth_one_fixed_gauge_DQ"] == "CERTIFIED", "DQ")
    require(
        dq["result"]["fixed_gauge_depth_one_DQ"]["regular_radical_stitching"]
        ["maximal_connected_face_rows"] == 64,
        "occurrence count",
    )
    require(
        dq["result"]["collision_coordinate_correction"]
        ["corrected_unnormalized_density_upper_bound"] == "18/5",
        "coarea input",
    )

    recovery = loaded[
        "cm2-gate34-occurrence-boundary-recovery-carrier-manifest-2026-07-17.json"
    ]["result"]["boundary_recovery_carrier_registry"]
    require(recovery["maximal_occurrence_row_count"] == 64, "recovery rows")
    require(recovery["oriented_hit_miss_trace_seed_count"] == 128, "trace seeds")
    require(
        recovery["all_open_rows_have_analytic_boundary_continuation_carrier"] is True,
        "analytic carriers",
    )

    schema = loaded[
        "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
    ]["result"]["required_operator_field_schema"]
    fields = schema["required_fields"]
    require(len(fields) == 18 and fields[9] == F10 and fields[12] == F13, "schema")
    return loaded


def replay_physical_rows(
    loaded: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    occurrence_rows, _row_registry = dq_cert.load_rows()
    typed_rows, typed_registry = dq_cert.corrected_current_rows(occurrence_rows)
    carrier_rows, carrier_registry = recovery_cert.build_carrier_registry()
    require(len(occurrence_rows) == len(typed_rows) == len(carrier_rows) == 64, "64 rows")
    require(typed_registry["strict_hit_and_miss_trace_attached_to_every_row"] is True, "traces")

    by_occurrence = {row["occurrence_id"]: row for row in carrier_rows}
    require(len(by_occurrence) == 64, "unique carrier rows")
    require(
        carrier_registry["carrier_rows_sha256"]
        == loaded[
            "cm2-gate34-occurrence-boundary-recovery-carrier-manifest-2026-07-17.json"
        ]["result"]["boundary_recovery_carrier_registry"]["carrier_rows_sha256"],
        "carrier replay digest",
    )
    trace_ids = {
        trace_id
        for row in carrier_rows
        for trace_id in (row["hit_trace_seed_id"], row["miss_trace_seed_id"])
    }
    require(len(trace_ids) == 128, "trace id uniqueness")
    require(
        all(row["witness_replay"]["tangent_target_p_is_epsilon_exactly"] is True for row in carrier_rows),
        "grazing p",
    )
    return occurrence_rows, carrier_rows, {
        "occurrence_row_count": 64,
        "physical_hit_trace_seed_count": 64,
        "physical_miss_trace_seed_count": 64,
        "distinct_trace_seed_count": 128,
        "occurrence_ids_sha256": canonical_digest(sorted(by_occurrence)),
        "carrier_rows_sha256": canonical_digest(carrier_rows),
        "trace_ids_sha256": canonical_digest(sorted(trace_ids)),
        "every_occurrence_target_is_grazing_with_p_equal_epsilon": True,
        "grazing_target_abs_p": "1",
    }


def replay_cores() -> tuple[dict[str, core_cert.Core], dict[str, dict[str, Any]]]:
    cores = core_cert.physical_cores()
    require(len(cores) == 24, "24 core replay")
    core_map: dict[str, core_cert.Core] = {}
    row_map: dict[str, dict[str, Any]] = {}
    for core in cores:
        core_id = adaptive_cert.core_id(core)
        require(core_id not in core_map, "duplicate core id")
        row = core_cert.certify_core(core)
        require(row["strict_first_hit"] is True, "strict first hit")
        require(row["incoming_and_outgoing_abs_p_strict_upper"] == "3/10", "p gap")
        require(row["incoming_and_outgoing_cos_phi_strict_lower"] == "19/20", "cos gap")
        require(row["retained_competitors_missed"] + row["retained_competitors_strictly_later"] > 0, "competitors")
        core_map[core_id] = core
        row_map[core_id] = row
    return core_map, row_map


def empty_face_slots(
    packets: list[dict[str, Any]],
    occurrence_rows: list[dict[str, Any]],
    core_map: dict[str, core_cert.Core],
    core_rows: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    require(len(packets) == 4216, "R1 packet count")
    slots: list[dict[str, Any]] = []
    atom_ids: set[str] = set()
    h_ids: set[str] = set()
    slot_ids: set[str] = set()
    used_core_ids: set[str] = set()
    pair_reasons: Counter[str] = Counter()
    source_histogram: Counter[str] = Counter()
    target_histogram: Counter[str] = Counter()

    for packet in packets:
        atom_id = packet["atom_id"]
        h_id = packet["physical_homogeneity_subbranch_id"]
        source_core_id = packet["source_core_id"]
        require(atom_id not in atom_ids, "duplicate atom")
        require(h_id not in h_ids, "duplicate homogeneity")
        require(source_core_id in core_map, "source core id")
        require(packet["roof"] == 1 and packet["roof_level_j"] == 0, "roof one")
        atom_ids.add(atom_id)
        h_ids.add(h_id)
        used_core_ids.add(source_core_id)
        core = core_map[source_core_id]
        core_row = core_rows[source_core_id]
        require(core_row["strict_first_hit"] is True, "atom first owner")
        source_histogram[core.source] += 1
        target_histogram[core.target_id] += 1

        local_reasons: Counter[str] = Counter()
        for occurrence in occurrence_rows:
            if occurrence["source"] != core.source:
                reason = "different_collision_section_component"
            elif occurrence["target"] != core.target_id:
                reason = "different_first_target_excluded_by_strict_first_owner"
            else:
                reason = "same_target_grazing_abs_p_1_disjoint_from_core_abs_p_lt_3_over_10"
            pair_reasons[reason] += 1
            local_reasons[reason] += 1
        require(sum(local_reasons.values()) == 64, "local occurrence exhaustion")

        common = {
            "atom_id": atom_id,
            "physical_homogeneity_subbranch_id": h_id,
            "roof_level_j": 0,
            "source_core_id": source_core_id,
            "destination_core_id": packet["destination_core_id"],
            "physical_occurrence_universe_count": 64,
            "intersecting_physical_occurrence_ids": [],
            "physical_occurrence_intersection_count": 0,
            "empty_intersection_proof": {
                "source_core_strict_first_owner_against_complete_retained_candidate_list": True,
                "selected_target_incoming_and_outgoing_abs_p_strict_upper": "3/10",
                "occurrence_event_target_abs_p": "1",
                "same_target_gap_strict": "1-3/10=7/10",
                "pair_reason_histogram": dict(sorted(local_reasons.items())),
            },
            "artificial_R1_phase_faces_used_as_physical_occurrence_faces": False,
        }

        f10_payload = {
            **common,
            "field_name": F10,
            "carrier_type": "empty_family_of_intersecting_physical_collision_occurrence_faces",
            "coarea_density_regular_cost": "0",
            "empty_sum_convention": True,
            "global_occurrence_density_magnitude_seed_copied_to_atom": False,
        }
        f10_id = "slot:r1:f10-empty:" + canonical_digest(f10_payload)
        require(f10_id not in slot_ids, "duplicate F10 slot")
        slot_ids.add(f10_id)
        slots.append({"immutable_slot_id": f10_id, **f10_payload})

        f13_payload = {
            **common,
            "field_name": F13,
            "moving_boundary_current_on_fixed_R1_inner_restriction": "0",
            "physical_hit_trace_seed_ids": [],
            "physical_miss_trace_seed_ids": [],
            "trace_pair_count": 0,
            "every_intersecting_physical_face_has_one_hit_and_one_miss_trace": True,
            "vacuous_truth_on_certified_empty_physical_face_family": True,
            "smooth_branch_parameter_derivative_is_zero_claimed": False,
            "smooth_branch_parameter_derivative_is_carried_by_F11": True,
        }
        f13_id = "slot:r1:f13-empty:" + canonical_digest(f13_payload)
        require(f13_id not in slot_ids, "duplicate F13 slot")
        slot_ids.add(f13_id)
        slots.append({"immutable_slot_id": f13_id, **f13_payload})

    slots.sort(key=lambda row: (row["atom_id"], row["field_name"]))
    require(len(atom_ids) == len(h_ids) == 4216, "atom/h ids")
    require(len(used_core_ids) == 16, "used source cores")
    require(len(slots) == len(slot_ids) == 8432, "slot count")
    require(sum(pair_reasons.values()) == 4216 * 64, "pair audit count")
    require(pair_reasons == Counter({
        "different_collision_section_component": 133568,
        "different_first_target_excluded_by_strict_first_owner": 106520,
        "same_target_grazing_abs_p_1_disjoint_from_core_abs_p_lt_3_over_10": 29736,
    }), "pair reason histogram")
    require(source_histogram == Counter({"G": 2164, "W": 2052}), "source histogram")
    sample_indices = (0, 1, len(slots) // 2, len(slots) - 1)
    return slots, {
        "R1_inner_atom_count": 4216,
        "physical_homogeneity_subbranch_id_count": 4216,
        "used_source_core_count": 16,
        "physical_occurrence_face_count": 64,
        "atom_occurrence_pair_audit_count": 4216 * 64,
        "atom_occurrence_pair_reason_histogram": dict(sorted(pair_reasons.items())),
        "certified_intersecting_atom_occurrence_pair_count": 0,
        "materialized_candidate_local_slot_count": 8432,
        "materialized_candidate_local_slot_count_per_field": {F10: 4216, F13: 4216},
        "empty_physical_face_F10_slot_count": 4216,
        "empty_physical_face_F13_slot_count": 4216,
        "artificial_R1_phase_face_incidence_count": 16864,
        "artificial_R1_phase_faces_used_as_physical_carriers": False,
        "source_obstacle_histogram": dict(sorted(source_histogram.items())),
        "selected_target_histogram_sha256": canonical_digest(dict(sorted(target_histogram.items()))),
        "atom_ids_sha256": canonical_digest(sorted(atom_ids)),
        "homogeneity_ids_sha256": canonical_digest(sorted(h_ids)),
        "slot_ids_sha256": canonical_digest(sorted(slot_ids)),
        "slot_rows_sha256": canonical_digest(slots),
        "representative_slot_rows": [slots[index] for index in sample_indices],
    }


def maturity(fields: list[str]) -> dict[str, Any]:
    installed = set(fields[:13])
    rows: list[dict[str, Any]] = []
    for index, field in enumerate(fields, start=1):
        count = 4216 if field in installed else 0
        rows.append({
            "index": index,
            "field": field,
            "candidate_local_R1_atom_slot_count": count,
            "maturity": (
                "CANDIDATE_LOCAL_ON_EACH_OF_4216_R1_ATOMS"
                if count else "NOT_CERTIFIED_ON_R1_CANDIDATES"
            ),
            "global_complete_roof_level_slot_count_added": 0,
        })
    require(sum(row["candidate_local_R1_atom_slot_count"] == 4216 for row in rows) == 13, "13 fields")
    require(rows[13]["candidate_local_R1_atom_slot_count"] == 0, "F14 gap")
    return {
        "required_field_count": 18,
        "prior_candidate_local_maturity": "11/18",
        "new_candidate_local_fields_installed": [F10, F13],
        "candidate_local_maturity_after_exact_empty_face_join": "13/18",
        "first_missing_candidate_local_field": fields[13],
        "complete_18_field_R1_operator_block_count": 0,
        "global_Gate5_field_credit_added": 0,
        "global_Gate5_maturity_before_and_after": "4/18 -> 4/18",
        "rows": rows,
        "rows_sha256": canonical_digest(rows),
    }


def downstream(fields: list[str]) -> dict[str, Any]:
    reasons = {
        fields[13]: "requires a complete limiting-R1 branchwise density assembly, not inner-box empty faces",
        fields[14]: "requires union-wide recovery and standard-family control",
        fields[15]: "requires the nonempty physical faces of the limiting R1 partition",
        fields[16]: "requires return-wide dynamic tests and the global physical DQ atlas",
        fields[17]: "requires a complete operator block before phase registration",
    }
    rows = [{
        "index": index,
        "field": field,
        "candidate_local_slot_count": 0,
        "status": "NOT_CERTIFIED",
        "first_missing_dependency": reasons[field],
    } for index, field in enumerate(fields[13:18], start=14)]
    return {
        "F14_through_F18_rows": rows,
        "F14_through_F18_rows_sha256": canonical_digest(rows),
        "F14_through_F18_materialized_slot_count": 0,
        "complete_operator_phase_block_count": 0,
    }


def certify() -> dict[str, Any]:
    loaded = load_dependencies()
    occurrence_rows, _carrier_rows, physical_registry = replay_physical_rows(loaded)
    core_map, core_rows = replay_cores()
    r1 = loaded[
        "cm2-gate5-round25-r1-field-join-manifest-2026-07-18.json"
    ]
    packets = r1["result"]["R1_inner_candidate_field_packet_rows"]
    _slots, slot_registry = empty_face_slots(packets, occurrence_rows, core_map, core_rows)
    fields = loaded[
        "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
    ]["result"]["required_operator_field_schema"]["required_fields"]

    result: dict[str, Any] = {
        "schema": "cm2.gate5.round27-r1-empty-physical-face-join.v1",
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "audit_policy": "exact physical carrier intersection; empty families typed positively",
        },
        "physical_occurrence_and_trace_replay": physical_registry,
        "R1_empty_physical_face_F10_F13_slot_registry": slot_registry,
        "Gate5_R1_candidate_local_maturity": maturity(fields),
        "F14_F18_frontier": downstream(fields),
        "strict_nonpromotion": {
            "empty_join_is_missing_join": False,
            "artificial_phase_face_used_as_physical_occurrence_face": False,
            "stationary_artificial_face_speed_used_as_coarea_density": False,
            "occurrence_density_seed_copied_to_empty_atom_face_family": False,
            "empty_local_current_claimed_as_global_depth_one_DQ_current": False,
            "smooth_branch_parameter_derivative_claimed_zero": False,
            "limiting_R1_physical_boundary_face_atlas": "NOT_CERTIFIED",
            "transported_occurrence_to_24_core_incidence": "NOT_CERTIFIED",
            "complete_18_field_R1_operator_block_count": 0,
            "return_wide_three_CM2_norm_intertwiners": "NOT_CERTIFIED",
            "induced_strong_Lasota_Yorke_coefficient": "NOT_CERTIFIED",
            "global_Gate5_maturity": "4/18_UNCHANGED",
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("R1_F10_EMPTY_PHYSICAL_FACE_SLOTS: 4216 CERTIFIED")
    print("R1_F13_EMPTY_PHYSICAL_CURRENT_SLOTS: 4216 CERTIFIED")
    print("R1_CANDIDATE_LOCAL_MATURITY: 13/18")
    print("LIMITING_R1_PHYSICAL_FACE_ATLAS: NOT_CERTIFIED")
    print("GLOBAL_GATE5: 4/18 NOT_CERTIFIED")
    print("CM2: NO-GO FOR CLAIM")


if __name__ == "__main__":
    main()
