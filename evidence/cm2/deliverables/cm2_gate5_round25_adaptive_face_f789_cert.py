#!/usr/bin/env python3
"""Adaptive R1-face F7--F9 certificate and unresolved split plan.

Each strict ``RETURN_AT_1_INNER`` leaf of the round-25 adaptive C24
calculation is a rectangular ``(t,p)`` source box on every fixed parameter
fibre.  On a canonical unstable graph, both ``t`` and ``p=sin(phi)`` are
strictly monotone.  Its intersection with one such rectangle is therefore
empty or one interval.  This prices the adaptive restriction in the
unnormalised characteristic ``Z_*`` norm by the already certified density
ratio ``2000/1999``.

The four phase faces are the coordinate lines ``r=constant`` and
``phi=constant`` in fixed-s Birkhoff coordinates.  The invariant cone
``25/9<V=dphi/dr<29`` gives normalized face transversality strictly above
``1/30``; each coordinate-line face has exact C2 seminorm zero.  Parameter
guard faces do not cut a fixed-s phase curve, and the destination-core test
introduces no extra face because the whole closed interval box was admitted
strictly inside one destination core.

The certificate materializes compact replay digests for one F7, F8 and F9
candidate-local slot on every one of the 4,216 strict R1-inner atoms.  It
does not price the union of all atoms, fill F10--F18, or complete Gate 5.

Separately, every current unresolved leaf receives a deterministic next
binary split record.  This proves exact next-generation mass conservation
and freezes a fair recursive policy; it does not pretend that the finite
unresolved cover has already disappeared or provide a numerical decay rate.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any


Q = Fraction
HERE = Path(__file__).resolve().parent

DEPENDENCIES = {
    "cm2-gate34-full-core-return-adaptive-frontier-manifest-2026-07-18.json": (
        "f79010c757e687cec2e8d7a8d617f3d94a3814731c58e960195c69107c446ad0"
    ),
    "cm2-gate25-maximal-word-characteristic-frontier-manifest-2026-07-16.json": (
        "bb09f99519813ec49172f0bbbcc9015c1e0fcb2de07df7af734b81d2996a3f40"
    ),
    "cm2-gate45-global-invariant-cone-manifest-2026-07-16.json": (
        "173949cb9cde01ae1326576c2a9a48b268a80bce2e48954a49efa46ccd9759f9"
    ),
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json": (
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866"
    ),
}

FIELD7 = "one_step_cut_growth_Z_sum"
FIELD8 = "face_transversality_lower"
FIELD9 = "face_C2_atlas_bound"
FIELDS = (FIELD7, FIELD8, FIELD9)
PARAMETER_WIDTH = Q(1, 200)
DENSITY_RATIO = Q(2000, 1999)
PHYSICAL_STEP = Q(360134800, 360493663)
RESTRICTION_STEP = DENSITY_RATIO * PHYSICAL_STEP


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
    require(lower < upper, "positive interval")
    return lower, upper


def load_dependencies() -> dict[str, dict[str, Any]]:
    loaded: dict[str, dict[str, Any]] = {}
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        require(path.is_file(), f"missing dependency: {name}")
        require(not path.is_symlink(), f"symlink dependency: {name}")
        require(path.resolve().parent == HERE, f"unsafe dependency: {name}")
        require(sha256_path(path) == expected, f"dependency hash: {name}")
        value = parse_json_text(path.read_text(encoding="utf-8"))
        require(isinstance(value, dict), f"dependency type: {name}")
        loaded[name] = value

    adaptive = loaded[
        "cm2-gate34-full-core-return-adaptive-frontier-manifest-2026-07-18.json"
    ]
    registry = adaptive["result"]["adaptive_full_core_step1_registry"]
    require(
        adaptive["verdict"]["positive_full_dimensional_R1_inner_branches"]
        == "CERTIFIED",
        "adaptive R1 verdict",
    )
    require(registry["classification_histogram"]["RETURN_AT_1_INNER"] == 4216, "R1 count")
    require(registry["classification_histogram"]["UNRESOLVED_OUTER"] == 26876, "unresolved count")
    require(registry["strict_Arb_admission_only"] is True, "strict Arb admission")
    require(registry["step1_collision_singular_atom_count"] == 0, "step1 singular")
    require(
        registry["unresolved_atoms_are_only_core_membership_or_chart_boundary_outer_boxes"]
        is True,
        "unresolved typing",
    )

    characteristic = loaded[
        "cm2-gate25-maximal-word-characteristic-frontier-manifest-2026-07-16.json"
    ]
    inner = characteristic["result"]["positive_inner_core_characteristic_Z"]
    require(inner["registered_inner_core_rectangle_count"] == 24, "inner core count")
    require(inner["intersection_component_multiplicity_upper_per_short_curve"] == 1, "core multiplicity")
    require(inner["artificial_boundary_endpoint_count_upper_per_nonempty_intersection"] == 2, "endpoint upper")
    require(inner["invariant_density_ratio_upper"] == "2000/1999", "density ratio")
    require(inner["physical_step_vartheta_p"] == "360134800/360493663", "physical step")
    require(
        inner["standard_curve_monotonicity_contract"]
        == "t is monotone in boundary arclength and p is strictly monotone on either oriented graph chart",
        "monotonicity contract",
    )

    cone = loaded[
        "cm2-gate45-global-invariant-cone-manifest-2026-07-16.json"
    ]["result"]["global_invariant_geometric_cone"]
    require(cone["fixed_geometric_unstable_cone"] == "25/9<V=dphi/dr<4108425/145348<29", "cone")
    require(cone["strict_forward_invariance"] is True, "cone invariance")

    schema = loaded[
        "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
    ]["result"]["required_operator_field_schema"]
    require(schema["required_field_count_per_physical_homogeneous_level"] == 18, "schema count")
    require(tuple(schema["required_fields"][6:9]) == FIELDS, "F7-F9 schema order")
    require(RESTRICTION_STEP == Q(720269600000, 720626832337), "coefficient")
    require(RESTRICTION_STEP < 1, "contraction")
    return loaded


def parent_boxes(rows: list[dict[str, Any]]) -> dict[int, dict[str, tuple[Q, Q]]]:
    grouped: dict[int, list[dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(int(row["source_core_index"]), []).append(row)
    require(set(grouped) == set(range(24)), "source core indices")
    result: dict[int, dict[str, tuple[Q, Q]]] = {}
    for index, source_rows in grouped.items():
        result[index] = {}
        for coordinate in ("t", "p", "s"):
            pairs = [qpair(row["source_box"][coordinate]) for row in source_rows]
            result[index][coordinate] = (
                min(pair[0] for pair in pairs),
                max(pair[1] for pair in pairs),
            )
    require(all(box["s"] == (Q(-1, 400), Q(1, 400)) for box in result.values()), "parameter parents")
    return result


def r1_homogeneity_id(row: dict[str, Any]) -> str:
    payload = {
        "atom_id": row["atom_id"],
        "source_core_id": row["source_core_id"],
        "destination_core_id": row["destination_core_id"],
        "source_label": "H0:abs(p)<3/10",
        "target_label": "H0:abs(p)<3/10",
        "intermediate_solid_collision_count": 0,
        "transparent_wall_level_count": 0,
        "complete_table_row_count": 1,
    }
    return "h:r1:" + canonical_digest(payload)


def phase_faces(row: dict[str, Any]) -> list[dict[str, Any]]:
    t0, t1 = qpair(row["source_box"]["t"])
    p0, p1 = qpair(row["source_box"]["p"])
    specs = (
        ("t_lower", "r_constant", str(t0), "vertical"),
        ("t_upper", "r_constant", str(t1), "vertical"),
        ("p_lower", "phi_constant", str(p0), "horizontal"),
        ("p_upper", "phi_constant", str(p1), "horizontal"),
    )
    rows: list[dict[str, Any]] = []
    for name, equation, coordinate, tangent in specs:
        payload = {
            "atom_id": row["atom_id"],
            "face_name": name,
            "fixed_s_Birkhoff_equation_type": equation,
            "source_coordinate_value": coordinate,
            "coordinate_line_tangent": tangent,
            "unit_speed_coordinate_line_C2_seminorm": "0",
        }
        payload["face_id"] = "face:r1:" + canonical_digest(payload)
        rows.append(payload)
    return rows


def common_templates() -> dict[str, dict[str, Any]]:
    f7 = {
        "field_name": FIELD7,
        "fixed_s_intersection_component_upper": 1,
        "artificial_endpoint_upper_per_nonempty_intersection": 2,
        "invariant_density_ratio_upper": "2000/1999",
        "unnormalized_characteristic_restriction": (
            "Z_*(1_A F)<=(2000/1999) Z_*(F) for one adaptive R1 atom A"
        ),
        "physical_step_vartheta_p": "360134800/360493663",
        "restriction_then_physical_step_strict_upper": "720269600000/720626832337",
        "restriction_then_physical_step_is_contraction": True,
        "normalized_after_conditioning_on_arbitrarily_small_atom": False,
    }
    f8 = {
        "field_name": FIELD8,
        "fixed_s_phase_face_count": 4,
        "unstable_graph_slope": "25/9<V=dphi/dr<29",
        "vertical_face_normalized_wedge": "1/sqrt(1+V^2)>1/sqrt(842)>1/30",
        "horizontal_face_normalized_wedge": "V/sqrt(1+V^2)>1/sqrt(2)>1/30",
        "common_normalized_face_transversality_strict_lower": "1/30",
        "parameter_guard_faces_cut_fixed_s_phase_curve": False,
        "destination_core_preimage_active_face_count": 0,
    }
    f9 = {
        "field_name": FIELD9,
        "fixed_s_phase_face_count": 4,
        "atlas": "four unit-speed Birkhoff coordinate-line charts",
        "common_face_C2_seminorm_upper": "0",
        "individual_face_charts_are_exactly_affine": True,
        "corner_set_role": "codimension_two_endpoints_not_a_C2_face",
        "global_coincident_face_assembly_claimed": False,
    }
    result = {"F7": f7, "F8": f8, "F9": f9}
    for key, value in result.items():
        value["template_id"] = f"template:r1:{key.lower()}:" + canonical_digest(value)
    return result


def materialize_slots(
    rows: list[dict[str, Any]],
    parents: dict[int, dict[str, tuple[Q, Q]]],
    templates: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    r1_rows = [row for row in rows if row["classification"] == "RETURN_AT_1_INNER"]
    require(len(r1_rows) == 4216, "R1 rows")
    all_core_ids = {row["source_core_id"] for row in rows}
    slots: list[dict[str, Any]] = []
    packets: list[dict[str, Any]] = []
    atom_ids: set[str] = set()
    slot_ids: set[str] = set()
    depth_histogram: Counter[int] = Counter()
    source_histogram: Counter[str] = Counter()
    destination_histogram: Counter[str] = Counter()
    for row in r1_rows:
        require(row["atom_id"] not in atom_ids, "duplicate atom")
        atom_ids.add(row["atom_id"])
        require(row["destination_core_id"] in all_core_ids, "destination core")
        require(row["output_enclosures"] is not None, "output enclosure")
        require(row["positive_two_dimensional_source_rectangle_at_each_s"] is True, "positive phase box")
        require(row["positive_parameter_interval"] is True, "positive parameter guard")
        require(row["depth"] == len(row["dyadic_path"]), "dyadic depth")
        source_parent = parents[int(row["source_core_index"])]
        artificial = any(
            qpair(row["source_box"][coordinate]) != source_parent[coordinate]
            for coordinate in ("t", "p", "s")
        )
        require(artificial, "adaptive artificial boundary")
        faces = phase_faces(row)
        require(len({face["face_id"] for face in faces}) == 4, "face ids")
        h_id = r1_homogeneity_id(row)
        common = {
            "atom_id": row["atom_id"],
            "source_core_id": row["source_core_id"],
            "destination_core_id": row["destination_core_id"],
            "physical_homogeneity_subbranch_id": h_id,
            "roof_level_j": 0,
            "parameter_guard": row["source_box"]["s"],
            "phase_face_ids": [face["face_id"] for face in faces],
            "phase_face_rows_sha256": canonical_digest(faces),
            "destination_core_membership_role": "strict_whole_closed_box_admission_not_an_active_face",
        }
        packet_slots: dict[str, str] = {}
        for key, field in zip(("F7", "F8", "F9"), FIELDS, strict=True):
            payload = {
                **common,
                "field_name": field,
                "template_id": templates[key]["template_id"],
            }
            slot_id = f"slot:r1:{key.lower()}:" + canonical_digest(payload)
            require(slot_id not in slot_ids, "duplicate slot")
            slot_ids.add(slot_id)
            slot = {"immutable_slot_id": slot_id, **payload}
            slots.append(slot)
            packet_slots[field] = slot_id
        packet = {
            "atom_id": row["atom_id"],
            "physical_homogeneity_subbranch_id": h_id,
            "roof_level_j": 0,
            "candidate_local_F7_F8_F9_slots": packet_slots,
        }
        packet["candidate_local_F789_packet_id"] = "packet:r1:f789:" + canonical_digest(packet)
        packets.append(packet)
        depth_histogram[int(row["depth"])] += 1
        source_histogram[row["source_core_id"]] += 1
        destination_histogram[row["destination_core_id"]] += 1

    slots.sort(key=lambda value: (value["atom_id"], value["field_name"]))
    packets.sort(key=lambda value: value["atom_id"])
    require(len(slots) == 3 * 4216, "slot count")
    require(len(slot_ids) == len(slots), "unique slots")
    require(depth_histogram == {13: 304, 14: 2588, 15: 1324}, "R1 depth histogram")
    require(len(source_histogram) == len(destination_histogram) == 16, "core histograms")
    sample_indices = (0, len(slots) // 2, len(slots) - 1)
    return slots, {
        "R1_inner_atom_count": 4216,
        "candidate_local_field_count_added_per_R1_atom": 3,
        "candidate_local_fields_added": list(FIELDS),
        "materialized_candidate_local_slot_count": len(slots),
        "materialized_candidate_local_slot_count_per_field": {
            field: 4216 for field in FIELDS
        },
        "physical_homogeneity_subbranch_id_count": len(packets),
        "R1_depth_histogram": {str(key): value for key, value in sorted(depth_histogram.items())},
        "R1_source_core_count": len(source_histogram),
        "R1_destination_core_count": len(destination_histogram),
        "R1_atom_ids_sha256": canonical_digest(sorted(atom_ids)),
        "candidate_local_slot_ids_sha256": canonical_digest(sorted(slot_ids)),
        "candidate_local_slot_rows_sha256": canonical_digest(slots),
        "candidate_local_packet_rows_sha256": canonical_digest(packets),
        "representative_slot_rows": [slots[index] for index in sample_indices],
        "all_destination_core_preimage_active_face_counts_are_zero": True,
        "all_parameter_guard_faces_are_inactive_on_fixed_s_phase_fibres": True,
        "all_R1_atoms_have_four_straight_fixed_s_phase_faces": True,
    }


def choose_split_axis(
    row: dict[str, Any], parent: dict[str, tuple[Q, Q]],
) -> str:
    scales: dict[str, Q] = {}
    for coordinate in ("t", "p", "s"):
        lower, upper = qpair(row["source_box"][coordinate])
        parent_lower, parent_upper = parent[coordinate]
        scales[coordinate] = (upper - lower) / (parent_upper - parent_lower)
    if scales["t"] >= scales["p"] and scales["t"] >= scales["s"]:
        return "t"
    if scales["p"] >= scales["s"]:
        return "p"
    return "s"


def child_boxes(row: dict[str, Any], axis: str) -> list[dict[str, list[str]]]:
    source = {coordinate: list(row["source_box"][coordinate]) for coordinate in ("t", "p", "s")}
    lower, upper = qpair(source[axis])
    middle = (lower + upper) / 2
    children: list[dict[str, list[str]]] = []
    for side in (0, 1):
        box = {coordinate: list(values) for coordinate, values in source.items()}
        box[axis] = [str(lower), str(middle)] if side == 0 else [str(middle), str(upper)]
        children.append(box)
    return children


def unresolved_split_plan(
    rows: list[dict[str, Any]], parents: dict[int, dict[str, tuple[Q, Q]]],
) -> dict[str, Any]:
    unresolved = [row for row in rows if row["classification"] == "UNRESOLVED_OUTER"]
    require(len(unresolved) == 26876, "unresolved rows")
    split_rows: list[dict[str, Any]] = []
    axis_histogram: Counter[str] = Counter()
    depth_histogram: Counter[int] = Counter()
    total_mass = Q(0)
    for row in unresolved:
        axis = choose_split_axis(row, parents[int(row["source_core_index"])])
        children = child_boxes(row, axis)
        parent_mass = Q(row["parameter_averaged_unnormalized_base_mass"])
        require(parent_mass > 0, "unresolved mass")
        child_mass = parent_mass / 2
        payload = {
            "parent_atom_id": row["atom_id"],
            "source_core_id": row["source_core_id"],
            "parent_dyadic_path": row["dyadic_path"],
            "parent_depth": row["depth"],
            "split_axis": axis,
            "child_dyadic_paths": [row["dyadic_path"] + "0", row["dyadic_path"] + "1"],
            "child_source_boxes_sha256": canonical_digest(children),
            "parent_base_mass": str(parent_mass),
            "each_child_base_mass": str(child_mass),
            "exact_child_mass_sum_equals_parent": True,
            "children_require_fresh_strict_Arb_classification": True,
        }
        payload["split_record_id"] = "split:r1q1:" + canonical_digest(payload)
        split_rows.append(payload)
        axis_histogram[axis] += 1
        depth_histogram[int(row["depth"])] += 1
        total_mass += parent_mass
    split_rows.sort(key=lambda value: value["parent_atom_id"])
    require(total_mass == Q(44519, 256000000), "unresolved mass total")
    require(depth_histogram == {12: 6816, 15: 20060}, "unresolved depth histogram")
    require(sum(axis_histogram.values()) == 26876, "split axes")
    return {
        "current_unresolved_parent_count": len(unresolved),
        "planned_next_generation_child_count": 2 * len(unresolved),
        "current_unresolved_parameter_averaged_base_mass": str(total_mass),
        "planned_next_generation_base_mass": str(total_mass),
        "next_split_axis_histogram": dict(sorted(axis_histogram.items())),
        "current_unresolved_depth_histogram": {
            str(key): value for key, value in sorted(depth_histogram.items())
        },
        "split_policy": "bisect the largest parent-normalized side; tie order t,p,s",
        "every_planned_split_is_prefix_free_and_mass_conservative_modulo_shared_faces": True,
        "planned_split_record_rows_sha256": canonical_digest(split_rows),
        "representative_split_records": [
            split_rows[0], split_rows[len(split_rows) // 2], split_rows[-1]
        ],
        "fair_recursive_policy_contract": {
            "every_infinite_unresolved_lineage_has_t_p_s_diameters_tending_to_zero": True,
            "fresh_whole_child_Arb_replay_required_before_terminal_classification": True,
            "midpoint_value_may_only_propose_refinement": True,
            "terminal_classes": ["RETURN_AT_1_INNER", "SURVIVE_THROUGH_1_INNER"],
            "finite_depth_unresolved_cover_may_remain_nonempty": True,
        },
        "strict_nonpromotion": {
            "next_generation_children_strictly_classified_in_this_leaf": 0,
            "numerical_unresolved_mass_decay_rate": "NOT_CERTIFIED",
            "finite_depth_exhaustion_of_unresolved_outer_cover": "NOT_CERTIFIED",
            "complete_finite_raw_R1_Q1_branch_ledger": "NOT_MATERIALIZED",
            "arbitrary_n_Rn_Qn_physical_partition": "NOT_CERTIFIED",
        },
    }


def certify() -> dict[str, Any]:
    loaded = load_dependencies()
    adaptive = loaded[
        "cm2-gate34-full-core-return-adaptive-frontier-manifest-2026-07-18.json"
    ]
    rows = adaptive["result"]["adaptive_full_core_step1_raw_leaf_rows"]
    require(isinstance(rows, list) and len(rows) == 33960, "adaptive rows")
    parents = parent_boxes(rows)
    templates = common_templates()
    _slots, registry = materialize_slots(rows, parents, templates)
    split_plan = unresolved_split_plan(rows, parents)
    result: dict[str, Any] = {
        "schema": "cm2.gate5.round25-adaptive-face-f789.v1",
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "source_scope": "4216 strict full-dimensional RETURN_AT_1_INNER atoms only",
            "parameter_scope": "fibrewise for every |s|<=1/400 with half-open ownership on internal guards",
            "old_artifacts_modified": False,
        },
        "fixed_s_adaptive_face_theorem": {
            "source_domain": "one rectangular (t,p) box inside one frozen C24 core",
            "canonical_curve_contract": "t(r) monotone and p(r)=sin(phi(r)) strictly monotone",
            "intersection_with_one_atom": "empty_or_one_interval",
            "phase_cut_face_types": ["r=constant", "phi=constant"],
            "phase_cut_face_count_per_atom": 4,
            "parameter_guard_faces_cut_fixed_s_phase_curve": False,
            "destination_core_preimage_face_is_redundant_after_strict_whole_box_admission": True,
            "new_artificial_endpoint_upper": 2,
            "unnormalized_Z_multiplier_upper": "2000/1999",
            "normalized_face_transversality_strict_lower": "1/30",
            "individual_coordinate_face_C2_seminorm_upper": "0",
        },
        "candidate_local_field_templates": templates,
        "R1_candidate_local_F789_slot_registry": registry,
        "unresolved_outer_next_generation_split_plan": split_plan,
        "Gate5_candidate_local_maturity_update": {
            "round25_R1_F1_to_F6_companion_leaf_required_for_join": True,
            "candidate_local_fields_available_from_this_leaf": list(FIELDS),
            "candidate_local_R1_maturity_after_exact_companion_join": "9/18",
            "global_Gate5_maturity_before_and_after": "4/18 -> 4/18",
            "global_Gate5_field_credit_added": 0,
            "first_missing_candidate_local_field_after_join": "coarea_density_regular_bound",
            "F10_through_F18_slots_materialized": 0,
            "complete_18_field_R1_operator_block_count": 0,
        },
        "strict_nonpromotion": {
            "F7_bound_for_union_of_all_4216_atoms": "NOT_CERTIFIED",
            "normalized_conditioned_Z_bound_uniform_in_atom_mass": "NOT_CERTIFIED",
            "coincident_face_global_flux_assembly": "NOT_CERTIFIED",
            "F10_coarea_density_regular_bound": "NOT_CERTIFIED",
            "complete_R1_partition_modulo_null_from_finite_raw_rows": "NOT_CERTIFIED",
            "complete_arbitrary_n_Rn_Qn_partition": "NOT_CERTIFIED",
            "return_wide_three_CM2_norm_intertwiners": "NOT_CERTIFIED",
            "induced_strong_Lasota_Yorke_coefficient": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("R1_ADAPTIVE_FACE_F7_SLOTS: 4216")
    print("R1_ADAPTIVE_FACE_F8_SLOTS: 4216")
    print("R1_ADAPTIVE_FACE_F9_SLOTS: 4216")
    print("R1_CANDIDATE_LOCAL_MATURITY_AFTER_COMPANION_JOIN: 9/18")
    print("UNRESOLVED_NEXT_SPLIT_RECORDS: 26876")
    print("GATE5_GLOBAL_MATURITY: 4/18 (UNCHANGED)")
    print("GATE5: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
