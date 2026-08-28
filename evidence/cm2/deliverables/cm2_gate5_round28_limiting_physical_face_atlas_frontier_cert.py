#!/usr/bin/env python3
"""Round-28 limiting R1/R2 physical coarea/DQ face-atlas frontier.

This append-only leaf separates four objects that must never be conflated:

* the certified-empty physical occurrence-face families on strict R1 atoms;
* stationary artificial faces of the adaptive dyadic boxes;
* the 96 genuine faces of the 24 physical C24 collision cores and their
  physical pullbacks by a regular billiard branch;
* the 64 genuine moving collision-occurrence faces, with their oriented
  hit/miss traces and corrected parameter-coarea currents.

For R1 the 24 frozen source branches permit an exhaustive finite registry of
1,152 candidate terminal-core-preimage equation families.  Each family gets
an immutable family ID, two immutable one-sided trace-family IDs and the
correct symbolic parameter-DQ/coarea type.  Empty and disconnected families
are allowed: component IDs, nonempty incidence and numerical current bounds
are not invented.

For R2 and arbitrary n the previously certified limiting partitions provide
the boundary-carrier grammar, but nonempty regular components were never
enumerated.  This leaf therefore freezes immutable ID grammars and the first
missing interface only.  It does not claim a complete limiting face atlas,
F14--F18, a complete Gate-5 block, or any new global Gate-5 credit.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as adaptive_cert
import cm2_gate34_occurrence_boundary_recovery_carrier_cert as recovery_cert
import cm2_gate34_parameter_dq_all_scale_shell_cert as parameter_cert
import cm2_gate3_depth_one_fixed_gauge_dq_cert as dq_cert


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate5.round28-limiting-physical-face-atlas-frontier.v3"
MANIFEST_SCHEMA = (
    "cm2.gate5.round28-limiting-physical-face-atlas-frontier.manifest.v3"
)

DEPENDENCIES = {
    "cm2_gate5_round27_r1_empty_physical_face_join_cert.py": (
        "aabe7f375036e68b742695f27a3a274bc47f594e547579e3592cf97f46989c43"
    ),
    "cm2-gate5-round27-r1-empty-physical-face-join-manifest-2026-07-18.json": (
        "9d900f2d0fee5ab8ad1a7e1f999e640ef88edc928ba6208987d1a74c93ca0e38"
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
    "cm2-gate5-round25-r1-field-join-manifest-2026-07-18.json": (
        "f6950d0a6ccf6984f888a102d846557e807becfddf3a95a72565e514934783e4"
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
    "cm2_gate34_parameter_dq_all_scale_shell_cert.py": (
        "ea5b6b7fa265990b1eaa1c106e2c0f82f024b58951bbe65ff55757cbc23df458"
    ),
    "cm2-gate34-parameter-dq-all-scale-shell-manifest-2026-07-17.json": (
        "2f374298785c74525e0bbb66b39e30be503ad9af05a913fa3175063196d883a8"
    ),
    "cm2-gate3-global-borel-current-assembly-manifest-2026-07-15.json": (
        "dce243c64d4e4fef44a023e8145b22c68233fcce7a8447d83ff86aa0a2d32bdf"
    ),
    "cm2-gate34-round26-boundary-tube-decay-manifest-2026-07-18.json": (
        "6ee5be1c2b60438043284c26837eef7681c94f95290abee33e52b7cab893e1d3"
    ),
    "cm2-gate34-round27-time2-boundary-tube-manifest-2026-07-18.json": (
        "a6d7c9dad800a7df7aa17b4f94f9bf45363d2839ff3711f35075ea998de07089"
    ),
    "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json": (
        "988f364bd1e6943178238c072e725de01af36452ef25d179eae6aef4000f7916"
    ),
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json": (
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866"
    ),
}


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


def digest(value: Any) -> str:
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
        "cm2-gate5-round27-r1-empty-physical-face-join-manifest-2026-07-18.json"
    ]
    require(prior["verdict"]["R1_candidate_local_maturity"] == "13/18", "R1 maturity")
    require(prior["verdict"]["intersecting_atom_occurrence_pairs"] == 0, "empty join")
    require(prior["verdict"]["global_Gate5_maturity"] == "4/18_UNCHANGED", "Gate5")

    core = loaded[
        "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json"
    ]["result"]
    require(core["physical_return_core_registry"]["physical_compact_homogeneous_core_count"] == 24, "cores")
    require(core["remaining_operator_frontier"]["branch_internal_no_singularity_cut"] is True, "regular cores")

    dq = loaded[
        "cm2-gate3-depth-one-fixed-gauge-dq-manifest-2026-07-15.json"
    ]
    require(dq["verdict"]["complete_depth_one_fixed_gauge_DQ"] == "CERTIFIED", "DQ")
    require(dq["result"]["collision_coordinate_correction"]["corrected_unnormalized_density_upper_bound"] == "18/5", "density")

    recovery = loaded[
        "cm2-gate34-occurrence-boundary-recovery-carrier-manifest-2026-07-17.json"
    ]["result"]["boundary_recovery_carrier_registry"]
    require(recovery["maximal_occurrence_row_count"] == 64, "occurrences")
    require(recovery["oriented_hit_miss_trace_seed_count"] == 128, "traces")

    parameter = loaded[
        "cm2-gate34-parameter-dq-all-scale-shell-manifest-2026-07-17.json"
    ]["result"]["selected_parameter_dq_all_scale_germ_registry"]
    require(parameter["selected_occurrence_parameter_germ_count"] == 64, "germs")
    require(parameter["oriented_actual_parameter_tube_germ_count"] == 128, "germ sides")

    step1 = loaded[
        "cm2-gate34-round26-boundary-tube-decay-manifest-2026-07-18.json"
    ]
    require(step1["verdict"]["limiting_step1_R1_Q1_partition_mod_collision_null_set"] == "CERTIFIED", "R1 partition")
    require(step1["result"]["fair_dyadic_boundary_tube_theorem"]["physical_t_face_count"] == 48, "t faces")
    require(step1["result"]["fair_dyadic_boundary_tube_theorem"]["physical_p_face_count"] == 48, "p faces")

    step2 = loaded[
        "cm2-gate34-round27-time2-boundary-tube-manifest-2026-07-18.json"
    ]
    require(step2["verdict"]["limiting_full_physical_R2_Q2_partition_mod_collision_null_set"] == "CERTIFIED", "R2 partition")

    arbitrary = loaded[
        "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json"
    ]
    require(arbitrary["verdict"]["arbitrary_n_regular_connected_component_existence_schema"] == "CERTIFIED_NONCONSTRUCTIVE", "Rn components")
    require(arbitrary["verdict"]["nonempty_component_enumeration_and_numeric_payload"] == "NOT_CERTIFIED", "no enumeration")

    fields = loaded[
        "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
    ]["result"]["required_operator_field_schema"]["required_fields"]
    require(len(fields) == 18, "18 fields")
    require(fields[13:18] == [
        "regular_density_operator_cost",
        "standard_family_operator_cost",
        "flux_face_operator_cost",
        "dynamic_test_operator_cost",
        "operator_phase_block",
    ], "F14-F18 schema")
    return loaded


def core_face_registry() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    face_ids: set[str] = set()
    trace_ids: set[str] = set()
    core_ids: set[str] = set()
    for core in core_cert.physical_cores():
        core_id = adaptive_cert.core_id(core)
        require(core_id not in core_ids, "duplicate core")
        core_ids.add(core_id)
        sides = (
            ("t_lower", "t", str(core.t0), -1, f"t>{core.t0}"),
            ("t_upper", "t", str(core.t1), 1, f"t<{core.t1}"),
            ("p_lower", "p", str(core.p0), -1, f"p>{core.p0}"),
            ("p_upper", "p", str(core.p1), 1, f"p<{core.p1}"),
        )
        for side, coordinate, value, outward, inside in sides:
            payload = {
                "core_id": core_id,
                "core_chart_id": core.chart_id,
                "core_source_obstacle": core.source,
                "side": side,
                "coordinate": coordinate,
                "coordinate_value": value,
                "outward_normal_sign": outward,
            }
            face_id = "physical-core-face:" + digest(payload)
            hit_id = "physical-core-trace:" + digest({"face_id": face_id, "side": "inside"})
            miss_id = "physical-core-trace:" + digest({"face_id": face_id, "side": "outside"})
            require(face_id not in face_ids, "duplicate core face")
            require(hit_id not in trace_ids and miss_id not in trace_ids, "duplicate core trace")
            face_ids.add(face_id)
            trace_ids.update((hit_id, miss_id))
            rows.append({
                "immutable_face_id": face_id,
                **payload,
                "physical_carrier_type": "stationary_C24_core_boundary_face_at_level_zero",
                "parameter_fibre": ["-1/400", "1/400"],
                "inside_trace_id": hit_id,
                "outside_trace_id": miss_id,
                "inside_trace_predicate": inside,
                "outside_trace_predicate": f"not({inside}) locally across this face",
                "corner_endpoint_policy": "zero_collision_line_measure_cemetery",
                "level_zero_coordinate_speed_ds": "0",
                "level_zero_parameter_DQ_current": "0",
                "stationary_parameter_current_means_collision_trace_measure_zero": False,
                "collision_trace_measure_type": "one_dimensional_collision_flux_trace",
                "artificial_dyadic_face": False,
            })
    rows.sort(key=canonical_json)
    require(len(rows) == len(face_ids) == 96, "96 core faces")
    require(len(trace_ids) == 192, "192 core traces")
    histogram = Counter(row["side"] for row in rows)
    require(histogram == Counter({"t_lower": 24, "t_upper": 24, "p_lower": 24, "p_upper": 24}), "side histogram")
    return rows, {
        "physical_C24_core_count": 24,
        "materialized_physical_core_face_count": 96,
        "materialized_one_sided_core_trace_count": 192,
        "side_histogram": dict(sorted(histogram.items())),
        "all_face_ids_immutable_and_distinct": True,
        "all_trace_ids_immutable_and_distinct": True,
        "all_level_zero_core_faces_stationary_in_fixed_t_p_coordinates": True,
        "zero_parameter_current_not_retyped_as_zero_collision_trace_measure": True,
        "face_ids_sha256": digest(sorted(face_ids)),
        "trace_ids_sha256": digest(sorted(trace_ids)),
        "face_rows_sha256": digest(rows),
        "representative_face_rows": [rows[0], rows[1], rows[-2], rows[-1]],
    }


def r1_core_preimage_seed_registry(
    core_faces: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    family_ids: set[str] = set()
    trace_ids: set[str] = set()
    source_histogram: Counter[str] = Counter()
    destination_face_histogram: Counter[str] = Counter()

    for source in core_cert.physical_cores():
        source_id = adaptive_cert.core_id(source)
        source_row = core_cert.certify_core(source)
        require(source_row["strict_first_hit"] is True, "source first owner")
        require(source_row["absolute_inverse_area_Jacobian"] == "1", "local diffeo")
        target_obstacle = source.target_id[0]
        compatible = [
            face for face in core_faces
            if face["core_source_obstacle"] == target_obstacle
        ]
        require(len(compatible) == 48, "48 obstacle-compatible core faces")
        for face in compatible:
            inward_level = (
                f"{face['coordinate']}(T_s(x))-{face['coordinate_value']}"
                if face["side"].endswith("lower")
                else f"{face['coordinate_value']}-{face['coordinate']}(T_s(x))"
            )
            payload = {
                "level": 1,
                "source_core_id": source_id,
                "source_regular_word_key_sha256": source_row["key_row_sha256"],
                "destination_core_face_id": face["immutable_face_id"],
                "destination_core_id": face["core_id"],
                "inward_level_function": inward_level,
            }
            family_id = "physical-r1-core-preimage-family:" + digest(payload)
            hit_id = "physical-r1-trace-family:" + digest({"family_id": family_id, "side": "inside"})
            miss_id = "physical-r1-trace-family:" + digest({"family_id": family_id, "side": "outside"})
            require(family_id not in family_ids, "duplicate R1 family")
            require(hit_id not in trace_ids and miss_id not in trace_ids, "duplicate R1 trace")
            family_ids.add(family_id)
            trace_ids.update((hit_id, miss_id))
            source_histogram[source_id] += 1
            destination_face_histogram[face["immutable_face_id"]] += 1
            rows.append({
                "immutable_face_family_id": family_id,
                **payload,
                "physical_carrier_type": "regular_branch_pullback_of_stationary_destination_core_face",
                "inside_hit_trace_family_id": hit_id,
                "outside_miss_trace_family_id": miss_id,
                "one_sided_trace_definition": "limits from inward_level_function>0 and <0",
                "parameter_DQ_current_type": "symbolic_regular_level_set_current",
                "signed_current_template": "partial_s(F_s)*delta_0(F_s)*dmu_collision",
                "positive_coarea_density_template": "abs(partial_s(F_s))/norm(grad_collision(F_s)) relative to collision line trace",
                "regular_gradient_nonzero_reason": "destination coordinate covector composed with invertible regular billiard derivative",
                "candidate_family_may_be_empty": True,
                "candidate_family_may_have_multiple_clipped_components": True,
                "nonempty_component_ids_materialized": False,
                "numeric_coarea_density_or_trace_norm_bound": "NOT_CERTIFIED",
                "artificial_dyadic_face": False,
            })
    rows.sort(key=canonical_json)
    require(len(rows) == len(family_ids) == 1152, "1152 R1 families")
    require(len(trace_ids) == 2304, "2304 R1 traces")
    require(set(source_histogram.values()) == {48}, "48 per source")
    require(set(destination_face_histogram.values()) == {12}, "12 per destination face")
    return rows, {
        "regular_source_core_count": 24,
        "obstacle_compatible_destination_core_face_count_per_source": 48,
        "materialized_candidate_R1_core_preimage_equation_family_count": 1152,
        "materialized_candidate_R1_one_sided_trace_family_count": 2304,
        "family_ids_sha256": digest(sorted(family_ids)),
        "trace_family_ids_sha256": digest(sorted(trace_ids)),
        "family_rows_sha256": digest(rows),
        "every_family_has_one_inside_hit_and_one_outside_miss_trace_type": True,
        "every_nonempty_regular_piece_has_symbolic_parameter_DQ_current": True,
        "numeric_coarea_density_bounds_materialized": 0,
        "nonempty_connected_face_component_ids_materialized": 0,
        "candidate_family_id_is_not_face_component_id": True,
        "representative_family_rows": [rows[0], rows[1], rows[-2], rows[-1]],
    }


def moving_occurrence_face_registry() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    occurrence_rows, _ = dq_cert.load_rows()
    typed_rows, typed_registry = dq_cert.corrected_current_rows(occurrence_rows)
    carrier_rows, carrier_registry = recovery_cert.build_carrier_registry()
    parameter_rows = [parameter_cert.certify_germ(row) for row in occurrence_rows]

    typed = {row["occurrence_id"]: row for row in typed_rows}
    carriers = {row["occurrence_id"]: row for row in carrier_rows}
    germs = {row["occurrence_id"]: row for row in parameter_rows}
    require(len(typed) == len(carriers) == len(germs) == 64, "64-way occurrence join")
    require(typed_registry["strict_hit_and_miss_trace_attached_to_every_row"] is True, "typed traces")
    require(carrier_registry["oriented_hit_miss_trace_seed_count"] == 128, "carrier traces")

    rows: list[dict[str, Any]] = []
    face_ids: set[str] = set()
    trace_ids: set[str] = set()
    germ_ids: set[str] = set()
    for occurrence in occurrence_rows:
        occurrence_id = occurrence["occurrence_id"]
        current = typed[occurrence_id]
        carrier = carriers[occurrence_id]
        germ = germs[occurrence_id]
        payload = {
            "occurrence_id": occurrence_id,
            "global_physical_label": occurrence["global_physical_label"],
            "source": occurrence["source"],
            "tangent_target": occurrence["target"],
            "epsilon": occurrence["epsilon"],
            "miss_target": occurrence["miss_target"],
        }
        face_id = "physical-moving-occurrence-face-seed:" + digest(payload)
        require(face_id not in face_ids, "duplicate occurrence face")
        face_ids.add(face_id)
        hit_id = carrier["hit_trace_seed_id"]
        miss_id = carrier["miss_trace_seed_id"]
        require(hit_id not in trace_ids and miss_id not in trace_ids, "duplicate occurrence trace")
        trace_ids.update((hit_id, miss_id))
        require(germ["germ_id"] not in germ_ids, "duplicate germ")
        germ_ids.add(germ["germ_id"])
        require(germ["hit_parameter_sign"] == current["signed_current"]["polarity"], "hit polarity")
        require(germ["miss_parameter_sign"] == -current["signed_current"]["polarity"], "miss polarity")
        rows.append({
            "immutable_global_occurrence_face_seed_id": face_id,
            **payload,
            "physical_carrier_type": "moving_first_event_grazing_occurrence_face",
            "immutable_hit_trace_seed_id": hit_id,
            "immutable_miss_trace_seed_id": miss_id,
            "common_boundary_recovery_carrier_id": carrier["common_boundary_recovery_carrier_id"],
            "selected_all_scale_parameter_germ_id": germ["germ_id"],
            "selected_all_scale_germ_exhausts_whole_maximal_row": False,
            "hit_parameter_sign": germ["hit_parameter_sign"],
            "miss_parameter_sign": germ["miss_parameter_sign"],
            "positive_coarea_law": current["positive_coarea_law"],
            "signed_parameter_DQ_current": current["signed_current"],
            "corrected_unnormalized_density_upper_bound_wrt_dtheta": "18/5",
            "artificial_dyadic_face": False,
            "core_preimage_face": False,
        })
    rows.sort(key=canonical_json)
    require(len(rows) == len(face_ids) == 64, "64 occurrence faces")
    require(len(trace_ids) == 128, "128 occurrence traces")

    # The compact source cores have one strict regular owner throughout.
    # This repeats the round-27 trichotomy on all 24 full cores, not merely
    # on the 4,216 strict inner atoms.
    reasons: Counter[str] = Counter()
    for core in core_cert.physical_cores():
        certified = core_cert.certify_core(core)
        require(certified["strict_first_hit"] is True, "core owner")
        require(certified["incoming_and_outgoing_abs_p_strict_upper"] == "3/10", "core p")
        for occurrence in occurrence_rows:
            if occurrence["source"] != core.source:
                reasons["different_collision_section_component"] += 1
            elif occurrence["target"] != core.target_id:
                reasons["different_first_target_excluded_by_strict_first_owner"] += 1
            else:
                reasons["same_target_grazing_abs_p_1_disjoint_from_core_abs_p_lt_3_over_10"] += 1
    require(sum(reasons.values()) == 24 * 64, "full core occurrence audit")
    return rows, {
        "materialized_physical_moving_occurrence_face_seed_count": 64,
        "materialized_oriented_hit_miss_trace_seed_count": 128,
        "materialized_selected_all_scale_parameter_germ_count": 64,
        "face_ids_sha256": digest(sorted(face_ids)),
        "trace_seed_ids_sha256": digest(sorted(trace_ids)),
        "parameter_germ_ids_sha256": digest(sorted(germ_ids)),
        "face_rows_sha256": digest(rows),
        "corrected_positive_coarea_law": "R_source*cp*abs(u_y)/ell_T*dtheta",
        "signed_current_type": "sigma*integral(Phi(hit)-Phi(miss))*dm",
        "corrected_unnormalized_density_upper_bound_wrt_dtheta": "18/5",
        "full_C24_core_occurrence_pair_audit_count": 1536,
        "full_C24_core_occurrence_pair_reason_histogram": dict(sorted(reasons.items())),
        "intersecting_full_C24_core_occurrence_face_pairs": 0,
        "moving_occurrence_faces_are_internal_R1_boundary_faces": False,
        "representative_face_rows": [rows[0], rows[1], rows[-2], rows[-1]],
    }


def artificial_dyadic_face_registry(
    loaded: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    packets = loaded[
        "cm2-gate5-round25-r1-field-join-manifest-2026-07-18.json"
    ]["result"]["R1_inner_candidate_field_packet_rows"]
    require(len(packets) == 4216, "R1 packets")
    rows: list[dict[str, Any]] = []
    face_ids: set[str] = set()
    trace_ids: set[str] = set()
    for packet in packets:
        domain = packet["candidate_local_slots"]["nonempty_or_empty_domain_proof"]["payload"]["candidate_domain"]
        box = domain["closed_box_provenance"]
        for side, coordinate, value in (
            ("t_lower", "t", box["t"][0]),
            ("t_upper", "t", box["t"][1]),
            ("p_lower", "p", box["p"][0]),
            ("p_upper", "p", box["p"][1]),
        ):
            payload = {
                "atom_id": packet["atom_id"],
                "source_box_sha256": packet["source_box_sha256"],
                "side": side,
                "coordinate": coordinate,
                "coordinate_value": value,
            }
            face_id = "artificial-dyadic-R1-phase-face:" + digest(payload)
            lower_id = "artificial-dyadic-trace:" + digest({"face_id": face_id, "side": "lower"})
            upper_id = "artificial-dyadic-trace:" + digest({"face_id": face_id, "side": "upper"})
            require(face_id not in face_ids, "duplicate artificial face")
            require(lower_id not in trace_ids and upper_id not in trace_ids, "duplicate artificial trace")
            face_ids.add(face_id)
            trace_ids.update((lower_id, upper_id))
            rows.append({
                "immutable_artificial_face_id": face_id,
                **payload,
                "lower_computational_trace_id": lower_id,
                "upper_computational_trace_id": upper_id,
                "carrier_type": "stationary_adaptive_dyadic_box_face",
                "physical_collision_event_face": False,
                "physical_core_face": False,
                "parameter_coarea_density": "NOT_APPLICABLE",
                "physical_parameter_DQ_current": "NOT_APPLICABLE",
                "zero_coordinate_speed_may_be_used_as_physical_zero_current": False,
            })
    rows.sort(key=canonical_json)
    require(len(rows) == len(face_ids) == 16864, "16864 artificial faces")
    require(len(trace_ids) == 33728, "artificial traces")
    return rows, {
        "strict_R1_inner_atom_count": 4216,
        "artificial_phase_face_count_per_atom": 4,
        "materialized_artificial_dyadic_phase_face_count": 16864,
        "materialized_artificial_computational_trace_count": 33728,
        "parameter_guard_endpoint_incidence_count_not_retyped_as_phase_faces": 8432,
        "artificial_face_ids_sha256": digest(sorted(face_ids)),
        "artificial_trace_ids_sha256": digest(sorted(trace_ids)),
        "artificial_face_rows_sha256": digest(rows),
        "artificial_faces_used_as_physical_carriers": False,
        "stationary_artificial_speed_used_as_physical_coarea_density": False,
        "representative_face_rows": [rows[0], rows[1], rows[-2], rows[-1]],
    }


def higher_level_face_grammar() -> dict[str, Any]:
    kinds = [
        {
            "kind": "source_core_clipping_face",
            "carrier_family_id_grammar": "source-core-face-family:(source_core_face_id)",
            "time_index_contract": "time_j=0",
            "side_label_contract": "inside_or_outside",
        },
        {
            "kind": "intermediate_core_avoidance_preimage_face",
            "carrier_family_id_grammar": "intermediate-core-preimage-family:(time_j,core_face_id)",
            "time_index_contract": "1<=time_j<n",
            "side_label_contract": "avoid_or_enter",
        },
        {
            "kind": "terminal_core_preimage_face",
            "carrier_family_id_grammar": "terminal-core-preimage-family:(time_n,core_face_id)",
            "time_index_contract": "time_j=n",
            "side_label_contract": "return_or_survive",
        },
        {
            "kind": "collision_singularity_or_owner_change_face",
            "carrier_family_id_grammar": "collision-boundary-family:(time_j,frozen_step_boundary_key)",
            "time_index_contract": "1<=time_j<=n",
            "side_label_contract": "left_owner_or_right_owner_or_cemetery",
        },
        {
            "kind": "moving_occurrence_face",
            "global_seed_id_grammar": (
                "physical-moving-occurrence-face-seed:(occurrence_id)"
            ),
            "carrier_family_id_grammar": "occurrence-pullback-family:(time_j,occurrence_face_seed_id)",
            "time_index_contract": "1<=time_j<=n",
            "side_label_contract": "hit_or_miss",
            "global_seed_is_pullback_component_id": False,
        },
    ]
    for row in kinds:
        row["instance_face_id_grammar"] = (
            "face:(component_id,time_j,carrier_family_or_seed_id,connected_rank)"
        )
        row["instance_trace_id_grammar"] = (
            "trace:(component_id,time_j,carrier_family_or_seed_id,"
            "connected_rank,side_label)"
        )
        row["connected_rank_domain"] = "N"
        row["connected_rank_rule"] = (
            "least natural-number index in a fixed bijective enumeration of "
            "rational dyadic intervals in a canonical 1D carrier parameter "
            "whose closure is contained in the connected piece"
        )
        row["connected_rank_rule_status"] = (
            "NOT_CERTIFIED_BEFORE_CANONICAL_1D_PARAMETERIZATION_AND_PIECE_ENUMERATION"
        )
        row["carrier_family_or_seed_id_is_instance_face_component_id"] = False
        row["immutable_grammar_id"] = "physical-face-id-grammar:" + digest(row)
        row["parameter_DQ_current_type"] = (
            "regular_level_set_current after a nonempty regular component is instantiated"
            if row["kind"] != "moving_occurrence_face"
            else "frozen corrected occurrence current"
        )
        row["coarea_trace_typing"] = (
            "inside/outside one-sided collision trace; intersections and corners go to cemetery"
        )
    require(len({row["immutable_grammar_id"] for row in kinds}) == len(kinds), "grammar ids")
    return {
        "boundary_carrier_kind_rows": kinds,
        "boundary_carrier_kind_rows_sha256": digest(kinds),
        "R2_limiting_partition_mod_collision_null": "CERTIFIED",
        "R2_boundary_model": (
            "time1 regular pullbacks, complete retained second-flight tangencies/owner changes, and time2 core-face preimages"
        ),
        "R2_nonempty_regular_component_registry_materialized": False,
        "R2_instantiated_face_component_id_count": 0,
        "R2_instantiated_one_sided_trace_component_id_count": 0,
        "R2_instantiated_occurrence_pullback_face_component_id_count": 0,
        "R2_complete_physical_coarea_DQ_face_atlas": "NOT_CERTIFIED",
        "all_five_instance_face_grammars_include_connected_rank": True,
        "all_five_instance_trace_grammars_include_connected_rank": True,
        "connected_rank_assignment_certified_on_instantiated_faces": False,
        "grammar_certification_level": "CARRIER_FAMILY_GRAMMAR_ONLY",
        "arbitrary_n_candidate_path_universe": "24*441280^n",
        "arbitrary_n_terminal_core_face_candidate_family_universe": "24*441280^n*96",
        "arbitrary_n_component_id_prerequisite": (
            "c24-component:(source_core_id,n,path_key,least_dyadic_basis_index)"
        ),
        "arbitrary_n_nonempty_component_coordinates_enumerated": False,
        "arbitrary_n_instantiated_face_component_id_count": 0,
        "arbitrary_n_instantiated_occurrence_pullback_face_component_id_count": 0,
        "uniform_joint_parameter_face_atlas": "NOT_CERTIFIED",
        "first_missing_interface": (
            "enumerate nonempty adaptive regular components with common homogeneity/canonical-recut IDs; construct a canonical 1D parameter on every carrier family; split every intersection into connected pieces and certify each closure-contained least dyadic-basis index; then certify numeric transversality/coarea/trace bounds"
        ),
    }


def f14_f18_frontier(fields: list[str]) -> dict[str, Any]:
    first_missing = {
        fields[13]: "complete limiting-Rn branchwise density assembly and summable numeric coarea/trace costs",
        fields[14]: "survivor-conditioned standard-family recovery on a common forward/reverse strong restriction",
        fields[15]: "complete nonempty physical face-component atlas plus a CM2 flux-face norm lift",
        fields[16]: "dynamic-C1 test pairing and return-wide current tightness, not only bounded-Borel pairing",
        fields[17]: "all preceding fields on one common nonempty operator block",
    }
    rows = []
    for index, field in enumerate(fields[13:18], start=14):
        rows.append({
            "index": index,
            "field": field,
            "materialized_candidate_local_slot_count": 0,
            "status": "NOT_CERTIFIED",
            "first_missing_interface": first_missing[field],
        })
    return {
        "rows": rows,
        "rows_sha256": digest(rows),
        "F14_through_F18_materialized_slot_count": 0,
        "F16_occurrence_Borel_current_seed_rows_available": 64,
        "F16_symbolic_R1_core_preimage_current_family_seeds_available": 1152,
        "F17_arbitrary_bounded_Borel_test_pairing_available": True,
        "F17_dynamic_C1_CM2_test_bound_available": False,
        "complete_18_field_operator_block_count": 0,
        "R1_candidate_local_maturity_before_and_after": "13/18 -> 13/18",
        "global_Gate5_maturity_before_and_after": "4/18 -> 4/18",
    }


def build_result() -> dict[str, Any]:
    loaded = load_dependencies()
    core_faces, core_registry = core_face_registry()
    r1_families, r1_registry = r1_core_preimage_seed_registry(core_faces)
    occurrence_faces, occurrence_registry = moving_occurrence_face_registry()
    artificial_faces, artificial_registry = artificial_dyadic_face_registry(loaded)

    physical_ids = {
        *(row["immutable_face_id"] for row in core_faces),
        *(row["immutable_global_occurrence_face_seed_id"] for row in occurrence_faces),
    }
    artificial_ids = {row["immutable_artificial_face_id"] for row in artificial_faces}
    require(physical_ids.isdisjoint(artificial_ids), "physical/artificial namespace collision")
    require(len(r1_families) == 1152, "R1 replay")

    prior = loaded[
        "cm2-gate5-round27-r1-empty-physical-face-join-manifest-2026-07-18.json"
    ]["result"]
    fields = loaded[
        "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
    ]["result"]["required_operator_field_schema"]["required_fields"]

    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "atlas_policy": "immutable typed seeds first; component and norm claims fail closed",
            "collision_area_coordinates": "(r,p=sin(phi))",
        },
        "physical_C24_core_face_and_trace_registry": core_registry,
        "R1_regular_core_preimage_face_family_seed_registry": r1_registry,
        "moving_occurrence_coarea_DQ_face_seed_registry": occurrence_registry,
        "artificial_dyadic_face_separation_registry": artificial_registry,
        "strict_inner_R1_certified_empty_F10_F13_family": {
            "R1_inner_atom_count": prior["R1_empty_physical_face_F10_F13_slot_registry"]["R1_inner_atom_count"],
            "F10_empty_physical_face_slot_count": prior["R1_empty_physical_face_F10_F13_slot_registry"]["empty_physical_face_F10_slot_count"],
            "F13_empty_physical_current_slot_count": prior["R1_empty_physical_face_F10_F13_slot_registry"]["empty_physical_face_F13_slot_count"],
            "atom_occurrence_pair_audit_count": prior["R1_empty_physical_face_F10_F13_slot_registry"]["atom_occurrence_pair_audit_count"],
            "intersecting_atom_occurrence_pair_count": prior["R1_empty_physical_face_F10_F13_slot_registry"]["certified_intersecting_atom_occurrence_pair_count"],
            "candidate_local_maturity": "13/18",
            "empty_family_slots_are_not_missing_joins": True,
        },
        "limiting_R1_face_seed_coverage": {
            "limiting_R1_Q1_partition_mod_collision_null": "CERTIFIED",
            "source_C24_stationary_physical_face_count": 96,
            "regular_time1_core_preimage_candidate_equation_family_count": 1152,
            "moving_occurrence_faces_intersecting_full_C24_source_cores": 0,
            "chart_seam_is_physical_face": False,
            "boundary_type_seed_coverage": (
                "source core faces plus regular time1 pullbacks of obstacle-compatible destination core faces"
            ),
            "nonempty_connected_face_component_ids_materialized": 0,
            "common_face_subdivision_and_incidence_atlas": "NOT_CERTIFIED",
            "numeric_return_wide_coarea_and_trace_bounds": "NOT_CERTIFIED",
            "complete_limiting_R1_physical_coarea_DQ_face_atlas": "NOT_CERTIFIED",
        },
        "R2_and_arbitrary_n_physical_face_ID_grammar_frontier": higher_level_face_grammar(),
        "F14_F18_frontier": f14_f18_frontier(fields),
        "strict_nonpromotion": {
            "candidate_face_family_id_claimed_as_nonempty_component_id": False,
            "symbolic_DQ_current_claimed_as_numeric_current_bound": False,
            "stationary_core_face_claimed_to_have_zero_collision_trace_measure": False,
            "artificial_dyadic_face_used_as_physical_carrier": False,
            "selected_all_scale_occurrence_germ_claimed_to_exhaust_maximal_row": False,
            "R1_complete_limiting_face_atlas": "NOT_CERTIFIED",
            "R2_complete_limiting_face_atlas": "NOT_CERTIFIED",
            "arbitrary_n_uniform_joint_parameter_face_atlas": "NOT_CERTIFIED",
            "F14_through_F18_materialized_slot_count": 0,
            "complete_18_field_operator_block_count": 0,
            "R1_candidate_local_maturity": "13/18_UNCHANGED",
            "global_Gate5_maturity": "4/18_UNCHANGED",
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    payload = copy.deepcopy(result)
    result["internal_replay_digest"] = digest(payload)
    return result


def verdict() -> dict[str, Any]:
    return {
        "physical_C24_core_faces": "CERTIFIED_96",
        "physical_C24_one_sided_core_traces": "CERTIFIED_192",
        "R1_candidate_core_preimage_face_equation_families": "CERTIFIED_1152",
        "R1_candidate_core_preimage_one_sided_trace_families": "CERTIFIED_2304",
        "moving_occurrence_coarea_DQ_faces": "CERTIFIED_64",
        "moving_occurrence_oriented_hit_miss_traces": "CERTIFIED_128",
        "artificial_dyadic_phase_faces_separated": "CERTIFIED_16864",
        "limiting_R1_complete_physical_face_component_atlas": "NOT_CERTIFIED",
        "limiting_R2_complete_physical_face_component_atlas": "NOT_CERTIFIED",
        "arbitrary_n_face_ID_grammar": (
            "CARRIER_FAMILY_GRAMMAR_ONLY_CONNECTED_RANK_ASSIGNMENT_NOT_CERTIFIED"
        ),
        "F14_through_F18": "NOT_CERTIFIED",
        "R1_candidate_local_maturity": "13/18_UNCHANGED",
        "complete_18_field_operator_blocks": 0,
        "global_Gate5_maturity": "4/18_UNCHANGED",
        "Gate5": "NOT_CERTIFIED",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def manifest(verifier_path: Path) -> dict[str, Any]:
    return {
        "schema": MANIFEST_SCHEMA,
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier_path.resolve()),
        "dependencies": DEPENDENCIES,
        "result": build_result(),
        "verdict": verdict(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit-manifest", action="store_true")
    parser.add_argument(
        "--verifier",
        type=Path,
        default=HERE / "cm2_gate5_round28_limiting_physical_face_atlas_frontier_verifier.py",
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.emit_manifest:
        print(json.dumps(manifest(args.verifier), indent=2, sort_keys=True))
        return 0
    result = build_result()
    print("PHYSICAL_C24_CORE_FACES: CERTIFIED_96")
    print("R1_CORE_PREIMAGE_FACE_FAMILY_SEEDS: CERTIFIED_1152")
    print("MOVING_OCCURRENCE_COAREA_DQ_FACES: CERTIFIED_64")
    print("ARTIFICIAL_DYADIC_FACES_SEPARATED: CERTIFIED_16864")
    print("LIMITING_R1_R2_COMPLETE_FACE_COMPONENT_ATLAS: NOT_CERTIFIED")
    print("F14_F18: NOT_CERTIFIED")
    print("GLOBAL_GATE5: 4/18_UNCHANGED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.summary else 2


if __name__ == "__main__":
    sys.exit(main())
