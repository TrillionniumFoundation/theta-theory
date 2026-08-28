#!/usr/bin/env python3
"""Round-26 Gate-5 F10--F13 typed frontier on the 4,216 R1 atoms.

The frozen R1 atoms are strict one-collision central-to-central rectangles.
The physical-core certificate therefore gives a genuine fixed-parameter
``C^alpha`` test-pullback seed and a uniform derivative bound on every atom.
Restriction to an owned rectangle preserves those estimates.  This leaf
materializes candidate-local F11 slots and, on the four already registered
fixed-s coordinate faces, candidate-local F12 trace slots.

It deliberately does not manufacture F10 or F13.  The corrected coarea law
and its density-regularity costs live on the 64 physical occurrence faces,
whereas the four faces of an adaptive R1 atom are artificial coordinate
restrictions.  No occurrence-id/atom-id/face-id join exists.  Their zero
coordinate speed in the common fixed section is not a positive physical
coarea density.  Likewise half-open parameter guards are ownership records,
not a moving-boundary DQ atlas.  In particular, no R1 guard contains s=0 in
its relative interior, while the frozen complete DQ theorem is based at s=0.

Thus F10 is the first unfillable candidate-local field.  F11 and F12 are
installed independently, F13 and F14--F18 remain absent, complete blocks stay
zero, and global Gate 5 remains 4/18 and fail-closed.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

import cm2_gate25_physical_return_core_registry_cert as core_cert


Q = Fraction
HERE = Path(__file__).resolve().parent

DEPENDENCIES = {
    "cm2_gate25_physical_return_core_registry_cert.py": (
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"
    ),
    "cm2-gate5-round25-r1-field-join-manifest-2026-07-18.json": (
        "f6950d0a6ccf6984f888a102d846557e807becfddf3a95a72565e514934783e4"
    ),
    "cm2-gate5-round25-adaptive-face-f789-manifest-2026-07-18.json": (
        "6b9354026a1707a25971925e02acbb5ea7e459ca177190a28ff1b39857283d86"
    ),
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json": (
        "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42"
    ),
    "cm2-gate3-depth-one-fixed-gauge-dq-manifest-2026-07-15.json": (
        "284b25ac30dd86a01bd0faaa7c0a97ee47839670e3cde4309936235badf5fd52"
    ),
    "cm2-gate45-curvature-log-density-cost-manifest-2026-07-16.json": (
        "b38772a41d0b610e1e1cd4fb4509cfb76227cc8f4983af0699d2cf38e60650c5"
    ),
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json": (
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866"
    ),
}

F10 = "coarea_density_regular_bound"
F11 = "dynamic_Holder_test_pullback_bound"
F12 = "C1_face_trace_pullback_bound"
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


def qpair(values: Any) -> tuple[Q, Q]:
    require(isinstance(values, list) and len(values) == 2, "rational pair")
    lower, upper = Q(values[0]), Q(values[1])
    require(lower < upper, "positive rational interval")
    return lower, upper


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

    r1 = loaded[
        "cm2-gate5-round25-r1-field-join-manifest-2026-07-18.json"
    ]
    join = r1["result"]
    require(join["R1_inner_field_join_registry"]["R1_inner_atom_count"] == 4216, "R1 count")
    require(
        join["Gate5_R1_inner_18_field_maturity"]["candidate_local_maturity"]
        == "6/18",
        "prior F1-F6 maturity",
    )
    require(
        join["strict_nonpromotion"]["upstream_unresolved_outer_cover_nonempty"]
        is True,
        "unresolved cover",
    )

    f789 = loaded[
        "cm2-gate5-round25-adaptive-face-f789-manifest-2026-07-18.json"
    ]
    face_registry = f789["result"]["R1_candidate_local_F789_slot_registry"]
    require(face_registry["R1_inner_atom_count"] == 4216, "F789 atom count")
    require(face_registry["all_R1_atoms_have_four_straight_fixed_s_phase_faces"] is True, "faces")
    require(
        f789["result"]["Gate5_candidate_local_maturity_update"][
            "candidate_local_R1_maturity_after_exact_companion_join"
        ]
        == "9/18",
        "prior F1-F9 maturity",
    )

    core = loaded[
        "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json"
    ]["result"]["physical_return_core_registry"]
    require(core["physical_compact_homogeneous_core_count"] == 24, "core count")
    require(core["all_cores_uniform_on_full_parameter_window"] is True, "uniform cores")
    require(
        core["local_seed_bindings_on_each_core"][
            "full_collision_branch_Calpha_test_pullback_seed"
        ]
        == "CERTIFIED_LOCAL_FULL_RETURN_COST_LT_158",
        "Calpha seed",
    )
    core_rows = [core_cert.certify_core(row) for row in core_cert.physical_cores()]
    require(len(core_rows) == 24, "physical core row replay")
    require(
        all(row["forward_and_reverse_D_infinity_norm_strict_upper"] == "158" for row in core_rows),
        "core derivative replay",
    )
    require(
        all(
            row["local_Calpha_test_pullback_cost_strict_upper"]
            == "158 for 0<alpha<=1"
            for row in core_rows
        ),
        "core Calpha replay",
    )

    dq = loaded[
        "cm2-gate3-depth-one-fixed-gauge-dq-manifest-2026-07-15.json"
    ]
    require(dq["verdict"]["complete_depth_one_fixed_gauge_DQ"] == "CERTIFIED", "depth-one DQ")
    require(dq["verdict"]["dynamic_iterated_test_MT_DQ"] == "NOT_CERTIFIED", "dynamic DQ boundary")
    require(
        dq["result"]["collision_coordinate_correction"][
            "corrected_unnormalized_density_upper_bound"
        ]
        == "18/5",
        "coarea magnitude upper",
    )
    require(
        dq["result"]["fixed_gauge_depth_one_DQ"]["regular_radical_stitching"][
            "maximal_connected_face_rows"
        ]
        == 64,
        "occurrence face count",
    )

    curvature = loaded[
        "cm2-gate45-curvature-log-density-cost-manifest-2026-07-16.json"
    ]
    require(curvature["verdict"]["bidirectional_log_density_costs"] == "CERTIFIED", "density costs")
    require(
        curvature["result"]["scope_limits"]["physical_prefix_suffix_costs"]
        is False,
        "no prefix/suffix promotion",
    )

    schema = loaded[
        "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
    ]["result"]["required_operator_field_schema"]
    fields = schema["required_fields"]
    require(len(fields) == 18, "18-field schema")
    require(tuple(fields[9:13]) == (F10, F11, F12, F13), "F10-F13 order")
    return loaded


def phase_faces(packet: dict[str, Any]) -> list[dict[str, Any]]:
    domain = packet["candidate_local_slots"][
        "nonempty_or_empty_domain_proof"
    ]["payload"]["candidate_domain"]
    box = domain["closed_box_provenance"]
    t0, t1 = qpair(box["t"])
    p0, p1 = qpair(box["p"])
    specs = (
        ("t_lower", "r_constant", str(t0), "vertical"),
        ("t_upper", "r_constant", str(t1), "vertical"),
        ("p_lower", "phi_constant", str(p0), "horizontal"),
        ("p_upper", "phi_constant", str(p1), "horizontal"),
    )
    rows: list[dict[str, Any]] = []
    for name, equation, coordinate, tangent in specs:
        payload = {
            "atom_id": packet["atom_id"],
            "face_name": name,
            "fixed_s_Birkhoff_equation_type": equation,
            "source_coordinate_value": coordinate,
            "coordinate_line_tangent": tangent,
            "unit_speed_coordinate_line_C2_seminorm": "0",
        }
        payload["face_id"] = "face:r1:" + canonical_digest(payload)
        rows.append(payload)
    return rows


def field_templates() -> dict[str, dict[str, Any]]:
    f11 = {
        "field_name": F11,
        "test_class": "C^alpha on the target collision chart, 0<alpha<=1",
        "fixed_s_full_collision_branch_pullback_cost_strict_upper": "158",
        "source": "frozen 24-core local full-collision C^alpha seed",
        "restriction_to_owned_R1_atom_preserves_bound": True,
        "half_open_parameter_guard_role": "selects fibres only; no guard endpoint differentiation",
        "return_wide_dynamic_test_operator_cost_claimed": False,
    }
    f12 = {
        "field_name": F12,
        "fixed_s_phase_face_count": 4,
        "face_charts": "four unit-speed Birkhoff coordinate lines",
        "test_value_pullback_multiplier_upper": "1",
        "tangential_derivative_pullback_strict_upper": "158",
        "C1_sum_norm_pullback_strict_upper": "159",
        "derivation": "d(Phi o F)(e_face)=D Phi(F) DF(e_face)",
        "source": "frozen forward D_infinity strict upper 158 on every compact core",
        "corner_endpoints_are_not_extra_C1_faces": True,
        "physical_hit_miss_trace_or_DQ_current_claimed": False,
    }
    result = {"F11": f11, "F12": f12}
    for key, value in result.items():
        value["template_id"] = f"template:r1:{key.lower()}:" + canonical_digest(value)
    return result


def materialize_slots(
    r1: dict[str, Any], f789: dict[str, Any], templates: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    packets = r1["result"]["R1_inner_candidate_field_packet_rows"]
    require(isinstance(packets, list) and len(packets) == 4216, "packet count")
    face_registry = f789["result"]["R1_candidate_local_F789_slot_registry"]

    slots: list[dict[str, Any]] = []
    companion_packets: list[dict[str, Any]] = []
    atom_ids: set[str] = set()
    h_ids: set[str] = set()
    slot_ids: set[str] = set()
    source_ids: set[str] = set()
    destination_ids: set[str] = set()
    guard_histogram: Counter[tuple[str, str]] = Counter()
    touches_zero = 0
    owns_zero = 0
    zero_in_relative_interior = 0

    for packet in packets:
        atom_id = packet["atom_id"]
        h_id = packet["physical_homogeneity_subbranch_id"]
        require(atom_id not in atom_ids, "duplicate atom")
        atom_ids.add(atom_id)
        h_ids.add(h_id)
        require(packet["roof"] == 1 and packet["roof_level_j"] == 0, "roof one")
        require(packet["candidate_local_fields"] == [
            "nonempty_or_empty_domain_proof",
            "physical_homogeneity_subbranch_table",
            "homogeneous_prefix_chart",
            "homogeneous_suffix_chart",
            "inverse_Jacobian_bound",
            "log_Jacobian_distortion_sum",
        ], "F1-F6 packet")
        require(
            packet["candidate_local_slots"]["physical_homogeneity_subbranch_table"]
            ["payload"]["physical_homogeneity_subbranch_id"] == h_id,
            "homogeneity binding",
        )
        domain = packet["candidate_local_slots"][
            "nonempty_or_empty_domain_proof"
        ]["payload"]["candidate_domain"]
        box = domain["closed_box_provenance"]
        require(canonical_digest(box) == packet["source_box_sha256"], "source box digest")
        s0, s1 = qpair(box["s"])
        guard = packet["parameter_guard"]
        require(Q(guard["s_lower"]) == s0 and Q(guard["s_upper"]) == s1, "guard box join")
        require(guard["lower_closed"] is True, "lower owner")
        require(guard["upper_closed"] is (s1 == Q(1, 400)), "upper owner")
        guard_histogram[(str(s0), str(s1))] += 1
        if s0 <= 0 <= s1:
            touches_zero += 1
        if s0 == 0 or (s0 < 0 < s1) or (s1 == 0 and guard["upper_closed"]):
            owns_zero += 1
        if s0 < 0 < s1:
            zero_in_relative_interior += 1

        faces = phase_faces(packet)
        require(len(faces) == 4 and len({row["face_id"] for row in faces}) == 4, "four faces")
        common = {
            "atom_id": atom_id,
            "source_core_id": packet["source_core_id"],
            "destination_core_id": packet["destination_core_id"],
            "physical_homogeneity_subbranch_id": h_id,
            "roof_level_j": 0,
            "parameter_guard": [str(s0), str(s1)],
            "phase_face_ids": [row["face_id"] for row in faces],
            "phase_face_rows_sha256": canonical_digest(faces),
        }
        packet_slots: dict[str, str] = {}
        for key, field in (("F11", F11), ("F12", F12)):
            payload = {
                **common,
                "field_name": field,
                "template_id": templates[key]["template_id"],
            }
            slot_id = f"slot:r1:{key.lower()}:" + canonical_digest(payload)
            require(slot_id not in slot_ids, "duplicate slot")
            slot_ids.add(slot_id)
            slots.append({"immutable_slot_id": slot_id, **payload})
            packet_slots[field] = slot_id
        companion = {
            "atom_id": atom_id,
            "physical_homogeneity_subbranch_id": h_id,
            "roof_level_j": 0,
            "candidate_local_F11_F12_slots": packet_slots,
        }
        companion["candidate_local_F1112_packet_id"] = (
            "packet:r1:f1112:" + canonical_digest(companion)
        )
        companion_packets.append(companion)
        source_ids.add(packet["source_core_id"])
        destination_ids.add(packet["destination_core_id"])

    slots.sort(key=lambda row: (row["atom_id"], row["field_name"]))
    companion_packets.sort(key=lambda row: row["atom_id"])
    require(len(atom_ids) == len(h_ids) == 4216, "atom/h id counts")
    require(len(slots) == len(slot_ids) == 8432, "slot count")
    require(len(source_ids) == len(destination_ids) == 16, "core counts")
    require(len(guard_histogram) == 48, "guard interval count")
    require(touches_zero == 352, "s0 touching guards")
    require(owns_zero == 176, "s0 owners")
    require(zero_in_relative_interior == 0, "s0 relative interior")
    require(
        canonical_digest(sorted(atom_ids)) == face_registry["R1_atom_ids_sha256"],
        "exact F789 atom join",
    )
    sample_indices = (0, 1, len(slots) // 2, len(slots) - 1)
    return slots, {
        "R1_inner_atom_count": 4216,
        "exact_F1_F9_companion_atom_join": True,
        "prior_candidate_local_maturity": "9/18",
        "new_candidate_local_fields": [F11, F12],
        "new_candidate_local_field_count_per_atom": 2,
        "materialized_candidate_local_slot_count": len(slots),
        "materialized_candidate_local_slot_count_per_field": {F11: 4216, F12: 4216},
        "fixed_s_phase_face_incidence_count": 4 * 4216,
        "physical_homogeneity_subbranch_id_count": len(h_ids),
        "source_core_count": len(source_ids),
        "destination_core_count": len(destination_ids),
        "distinct_parameter_guard_interval_count": len(guard_histogram),
        "parameter_guards_touching_s0_count": touches_zero,
        "parameter_guards_owning_s0_count": owns_zero,
        "parameter_guards_with_s0_in_relative_interior_count": zero_in_relative_interior,
        "all_phase_coordinate_bounds_constant_on_each_parameter_guard": True,
        "all_artificial_phase_faces_have_zero_velocity_in_common_fixed_section_coordinates": True,
        "atom_ids_sha256": canonical_digest(sorted(atom_ids)),
        "homogeneity_ids_sha256": canonical_digest(sorted(h_ids)),
        "slot_ids_sha256": canonical_digest(sorted(slot_ids)),
        "slot_rows_sha256": canonical_digest(slots),
        "companion_packet_rows_sha256": canonical_digest(companion_packets),
        "parameter_guard_histogram_sha256": canonical_digest(
            {f"{key[0]}:{key[1]}": value for key, value in sorted(guard_histogram.items())}
        ),
        "representative_slot_rows": [slots[index] for index in sample_indices],
    }


def f10_obstruction(dq: dict[str, Any], curvature: dict[str, Any]) -> dict[str, Any]:
    correction = dq["result"]["collision_coordinate_correction"]
    stitching = dq["result"]["fixed_gauge_depth_one_DQ"]
    density = curvature["result"]["curvature_log_density_and_partial_cost"][
        "bidirectional_log_density_bounds"
    ]
    require(density["reverse_log_derivative_cost"] == "abs(d log(rho_rev)/dr_source)<27*2^B", "reverse density")
    require(density["forward_log_derivative_cost"] == "abs(d log(rho_fw)/dr_miss)<52*2^B", "forward density")
    return {
        "field_index": 10,
        "field_name": F10,
        "frozen_physical_occurrence_face_count": stitching["regular_radical_stitching"][
            "maximal_connected_face_rows"
        ],
        "physical_occurrence_density_law": correction["corrected_positive_row_law"],
        "physical_occurrence_density_magnitude_upper": correction[
            "corrected_unnormalized_density_upper_bound"
        ],
        "physical_occurrence_log_density_costs": [
            density["reverse_log_derivative_cost"],
            density["forward_log_derivative_cost"],
        ],
        "R1_artificial_fixed_s_phase_face_incidence_count": 16864,
        "materialized_occurrence_id_to_R1_atom_id_to_phase_face_id_join_count": 0,
        "wrong_type_1": (
            "18/5 is an L-infinity magnitude upper on physical occurrence rows, "
            "not an R1 artificial-face density-regularity slot"
        ),
        "wrong_type_2": (
            "27*2^B and 52*2^B use occurrence-specific endpoint rank and oriented "
            "source/miss carriers; no such B or carrier is joined to an R1 atom"
        ),
        "wrong_type_3": (
            "zero coordinate speed of a stationary adaptive face is not the positive "
            "coarea law of a moving collision occurrence"
        ),
        "incomplete_partition_prevents_global_artificial_face_trace_assembly": True,
        "F10_candidate_local_slot_count": 0,
        "F10_status": "NOT_CERTIFIED",
        "first_unfillable_candidate_local_field_after_F1_F9_join": F10,
    }


def f13_obstruction(dq: dict[str, Any], slot_registry: dict[str, Any]) -> dict[str, Any]:
    fixed = dq["result"]["fixed_gauge_depth_one_DQ"]
    return {
        "field_index": 13,
        "field_name": F13,
        "frozen_DQ_base_parameter": "s=0",
        "frozen_depth_one_DQ_occurrence_face_count": fixed[
            "regular_radical_stitching"
        ]["maximal_connected_face_rows"],
        "frozen_physical_face_term_has_hit_and_miss_traces": True,
        "frozen_target_test_class": fixed["source_and_test_classes"]["target_test"],
        "R1_parameter_guards_touching_s0_count": slot_registry[
            "parameter_guards_touching_s0_count"
        ],
        "R1_parameter_guards_owning_s0_count": slot_registry[
            "parameter_guards_owning_s0_count"
        ],
        "R1_parameter_guards_with_s0_in_relative_interior_count": slot_registry[
            "parameter_guards_with_s0_in_relative_interior_count"
        ],
        "half_open_guard_endpoint_is_DQ_atlas_row": False,
        "fixed_s_artificial_phase_face_zero_speed_is_physical_DQ_current": False,
        "chart_lift_zero_current_requires_global_quotient_trace_assembly": True,
        "global_quotient_trace_assembly_available_on_incomplete_R1_candidate_subcover": False,
        "materialized_occurrence_hit_miss_trace_to_R1_face_join_count": 0,
        "dynamic_iterated_test_MT_DQ": "NOT_CERTIFIED",
        "F13_candidate_local_slot_count": 0,
        "F13_status": "NOT_CERTIFIED",
    }


def downstream_frontier(fields: list[str]) -> dict[str, Any]:
    reasons = {
        fields[13]: "requires a complete branchwise regular-density cost including F10",
        fields[14]: "requires union-wide F7 and density/recovery control, not per-atom seeds",
        fields[15]: "requires assembled physical flux faces with F10, F12 and F13",
        fields[16]: "requires return-wide dynamic tests and the physical F13 current",
        fields[17]: "requires a complete operator block before phase registration",
    }
    rows = [
        {
            "index": index,
            "field": field,
            "candidate_local_slot_count": 0,
            "status": "NOT_CERTIFIED",
            "first_missing_dependency": reasons[field],
        }
        for index, field in enumerate(fields[13:18], start=14)
    ]
    return {
        "F14_through_F18_rows": rows,
        "F14_through_F18_rows_sha256": canonical_digest(rows),
        "F14_through_F18_materialized_slot_count": 0,
        "complete_regular_standard_flux_dynamic_operator_cost_tuple_count": 0,
        "operator_phase_block_count": 0,
    }


def maturity(fields: list[str]) -> dict[str, Any]:
    installed = set(fields[:9]) | {F11, F12}
    rows = []
    for index, field in enumerate(fields, start=1):
        if field in installed:
            status = "CANDIDATE_LOCAL_ON_EACH_OF_4216_R1_ATOMS"
            count = 4216
        else:
            status = "NOT_CERTIFIED_ON_R1_CANDIDATES"
            count = 0
        rows.append({
            "index": index,
            "field": field,
            "candidate_local_R1_atom_slot_count": count,
            "maturity": status,
            "global_complete_roof_level_slot_count_added": 0,
        })
    require(sum(row["candidate_local_R1_atom_slot_count"] == 4216 for row in rows) == 11, "11 fields")
    require(rows[9]["field"] == F10 and rows[9]["candidate_local_R1_atom_slot_count"] == 0, "F10 first gap")
    return {
        "required_field_count": 18,
        "prior_candidate_local_maturity": "9/18",
        "new_candidate_local_fields_installed": [F11, F12],
        "candidate_local_maturity_after_independent_join": "11/18",
        "first_missing_candidate_local_field": F10,
        "complete_18_field_R1_operator_block_count": 0,
        "global_Gate5_field_credit_added": 0,
        "global_Gate5_maturity_before_and_after": "4/18 -> 4/18",
        "rows": rows,
        "rows_sha256": canonical_digest(rows),
    }


def certify() -> dict[str, Any]:
    loaded = load_dependencies()
    r1 = loaded["cm2-gate5-round25-r1-field-join-manifest-2026-07-18.json"]
    f789 = loaded["cm2-gate5-round25-adaptive-face-f789-manifest-2026-07-18.json"]
    dq = loaded["cm2-gate3-depth-one-fixed-gauge-dq-manifest-2026-07-15.json"]
    curvature = loaded["cm2-gate45-curvature-log-density-cost-manifest-2026-07-16.json"]
    schema = loaded[
        "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
    ]["result"]["required_operator_field_schema"]
    fields = schema["required_fields"]
    templates = field_templates()
    _slots, slot_registry = materialize_slots(r1, f789, templates)
    result: dict[str, Any] = {
        "schema": "cm2.gate5.round26-r1-f10-f13-frontier.v1",
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "audit_policy": "typed fixed-s restriction; no zero-speed or area-Jacobian promotion",
        },
        "candidate_local_F11_F12_templates": templates,
        "R1_candidate_local_F11_F12_slot_registry": slot_registry,
        "F10_coarea_density_regular_obstruction": f10_obstruction(dq, curvature),
        "F13_moving_boundary_DQ_obstruction": f13_obstruction(dq, slot_registry),
        "F14_F18_frontier": downstream_frontier(fields),
        "Gate5_R1_candidate_local_maturity": maturity(fields),
        "strict_nonpromotion": {
            "F10_coarea_density_regular_bound": "NOT_CERTIFIED",
            "F13_moving_boundary_DQ_current_and_two_traces": "NOT_CERTIFIED",
            "zero_speed_artificial_face_used_as_physical_coarea_current": False,
            "collision_SRB_area_Jacobian_used_as_face_density_or_unstable_Jacobian": False,
            "occurrence_level_density_seed_copied_to_R1_atoms_without_join": False,
            "half_open_parameter_guard_promoted_to_dynamic_DQ_atlas": False,
            "F11_F12_candidate_slots_are_return_wide_operator_costs": False,
            "complete_R1_partition_modulo_null": "NOT_CERTIFIED",
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
    print("R1_CANDIDATE_LOCAL_F11_SLOTS: 4216 CERTIFIED")
    print("R1_CANDIDATE_LOCAL_F12_SLOTS: 4216 CERTIFIED")
    print("FIRST_UNFILLABLE_FIELD_F10: NOT_CERTIFIED")
    print("F13_MOVING_BOUNDARY_DQ: NOT_CERTIFIED")
    print("R1_CANDIDATE_LOCAL_MATURITY: 11/18")
    print("GLOBAL_GATE5: 4/18 NOT_CERTIFIED")


if __name__ == "__main__":
    main()
