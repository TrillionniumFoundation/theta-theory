#!/usr/bin/env python3
"""Materialize two side-labelled smooth rank-three cell germs per corrected face.

The construction is deliberately local.  A canonical registered port in the
interior of each corrected face supplies a strict IFT slab.  The slab is cut
by the third-candidate discriminant into a collision side and a bypass side.
Each side receives a positive-area rational witness box, a complete immutable
candidate table, its actual third owner, return word, collision charts, and a
trace-incidence ID.  No F5/F6 field is installed here: the collision-side
germs accumulate on a genuine grazing trace and still require a homogeneity
collar recut before the universal pre-restriction templates can be joined.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as step1
import cm2_gate34_round29_q2_time3_anchor_registry_cert as time3
from cm2_round79_tangency_intersection_generator import digest, strict_sign
from cm2_round80_time3_tangency_curve_generator import third_tangency_jet


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round107.rank3-adjacent-smooth-cell-atlas.v1"
PRECISION_BITS = 512
MAX_WITNESS_SPLIT_DEPTH = 96

FILES = {
    "r102": "cm2-round102-rank3-corrected-face-quotient-2026-07-22.json",
    "r103": "cm2-round103-rank3-rn-f1-f2-binding-2026-07-22.json",
    "r104": "cm2-round104-rank3-rn-f3-prefix-chart-2026-07-22.json",
    "r105": "cm2-round105-rank3-rn-f4-suffix-chart-2026-07-22.json",
    "r106": "cm2-round106-rank3-f5-adjacent-cell-scope-audit-2026-07-22.json",
    "r87": "cm2-round87-rank3-port-event-continuation-2026-07-22.json",
    "r99": "cm2-round99-rank3-registered-port-candidate-audit-2026-07-22.json",
    "universal": "cm2-gate25-universal-operator-endpoint-template-frontier-manifest-2026-07-16.json",
}
PINS = {
    FILES["r102"]: "85069546fbc29f45af93eb65e2c2979bc83bfb5d744199771e234c2f7a1f0edb",
    FILES["r103"]: "76ac1099805e5fb3d9eac9984a078ed52f1f6ec706a5a12ec880de28a262c8e8",
    FILES["r104"]: "d6d47ac6b7cb03f70d483536a31ca031718f9aa96bd8adfce072866870bb9c5d",
    FILES["r105"]: "ef747bcd760bf8fe0a8bd8ac3bc65f9df4cf381898ffe98afcdb823f19c44b28",
    FILES["r106"]: "d3fbf85017f173e609a34b8b202d09d1fb0e5a664b922951c1c0730836d8f57e",
    FILES["r87"]: "f63f5d627def35f87dd3dfac075f8ecc0e8a5adfa725ddbe0eb692a39b54393b",
    FILES["r99"]: "e1f0ea00d48e9eae553d5bb24ce140d27f696fd071cb19270e023263aac32f5e",
    FILES["universal"]: "d532eeab0fa24901228a589724ffc4dbcff721f7d174a2b519187d77faab883b",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_nonfinite(token: str) -> Any:
    raise ValueError(f"nonfinite JSON number: {token}")


def load_documents() -> dict[str, dict[str, Any]]:
    documents: dict[str, dict[str, Any]] = {}
    for alias, name in FILES.items():
        path = HERE / name
        if sha256(path) != PINS[name]:
            raise RuntimeError(f"pin mismatch: {name}")
        document = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=strict_pairs,
            parse_constant=reject_nonfinite,
        )
        if not isinstance(document, dict):
            raise RuntimeError(f"non-object dependency: {name}")
        documents[alias] = document
    return documents


def target_chart(target: str, signs: list[int]) -> str:
    if len(signs) != 2 or any(sign not in (-1, 1) for sign in signs):
        raise RuntimeError("invalid outgoing direction signs")
    return f"collision:{target}:open-semicircle:[{signs[0]},{signs[1]}]"


def source_margin(source: Any, box: tuple[Q, Q, Q, Q]) -> Q:
    t0, t1, p0, p1 = box
    return min(t0 - source.t0, source.t1 - t1, p0 - source.p0, source.p1 - p1)


def candidate_analysis(
    state2: dict[str, Any], current_target: str,
) -> tuple[tuple[str, ...], list[dict[str, Any]], str]:
    candidates = tuple(time3.time2_cert.translated_candidate_ids(current_target, state2["chart"]))
    if len(candidates) != len(set(candidates)):
        raise RuntimeError("candidate table is not an immutable unique tuple")
    rows: list[dict[str, Any]] = []
    future: list[tuple[str, Any]] = []
    for candidate_id in candidates:
        candidate = time3.time2_cert.candidate_root(
            state2["contact_x"], state2["contact_y"],
            state2["outgoing_x"], state2["outgoing_y"],
            state2["s"], candidate_id,
        )
        classification = candidate["classification"]
        if classification == "strict_future_near_root":
            future.append((candidate_id, candidate["near"]))
        elif classification not in ("no_real_intersection", "intersection_strictly_behind"):
            raise RuntimeError(f"unresolved candidate root: {candidate_id}:{classification}")
        rows.append({"candidate_id": candidate_id, "root_classification": classification})
    winners = [
        candidate_id for candidate_id, near in future
        if all(candidate_id == other_id or bool(near < other_near) for other_id, other_near in future)
    ]
    if len(winners) != 1:
        raise RuntimeError(f"nonunique third owner: {winners}")
    rows.sort(key=lambda row: row["candidate_id"])
    return candidates, rows, winners[0]


def classify_witness(
    source: Any, face: dict[str, Any], box: tuple[Q, Q, Q, Q],
    expected_discriminant_sign: int, expected_third_owner: str,
    precision_bits: int,
) -> dict[str, Any]:
    ctx.prec = precision_bits
    atom = step1.Atom(
        face["source_core_index"], source, *box, Q(0), Q(0),
        f"round107-side-witness:{face['face_id']}:{expected_discriminant_sign}",
    )
    classification, owner_status, destination, state1, owner2 = (
        time3.homogeneity_cert.classify_with_geometry(atom, tuple(core_cert.physical_cores()))
    )
    if classification != "SURVIVE_THROUGH_2_INNER" or destination is not None or owner2 is None:
        raise RuntimeError("side witness does not survive through two collisions")
    if owner2["selected_target_id"] != face["second_selected_target_id"]:
        raise RuntimeError("side witness second owner mismatch")
    state2 = time3.second_outgoing_state(atom, state1, owner2)
    if state2 is None:
        raise RuntimeError("missing second outgoing state")
    jet = third_tangency_jet(
        source, face["second_selected_target_id"], face["third_candidate_id"], *box
    )
    discriminant_sign = strict_sign(jet.value)
    if discriminant_sign != expected_discriminant_sign:
        raise RuntimeError("side witness discriminant sign mismatch")
    candidates, candidate_rows, winner = candidate_analysis(
        state2, face["second_selected_target_id"]
    )
    if winner != expected_third_owner:
        raise RuntimeError(f"side witness third owner mismatch: {winner} != {expected_third_owner}")
    target_row = next(row for row in candidate_rows if row["candidate_id"] == face["third_candidate_id"])
    expected_target_classification = (
        "strict_future_near_root" if expected_discriminant_sign > 0 else "no_real_intersection"
    )
    if target_row["root_classification"] != expected_target_classification:
        raise RuntimeError("designated candidate side classification mismatch")
    margin = source_margin(source, box)
    if margin <= 0 or not (box[0] < box[1] and box[2] < box[3]):
        raise RuntimeError("nonpositive side witness dimension or core margin")
    witness_output_signs = [strict_sign(state2["outgoing_x"]), strict_sign(state2["outgoing_y"])]
    if any(sign not in (-1, 1) for sign in witness_output_signs):
        raise RuntimeError("side witness outgoing direction crosses a collision-chart boundary")
    return {
        "two_collision_classification": classification,
        "two_collision_owner_status": owner_status,
        "second_outgoing_chart": state2["chart"],
        "witness_outgoing_direction_component_strict_signs": witness_output_signs,
        "discriminant_strict_sign": discriminant_sign,
        "source_core_strict_rational_margin": str(margin),
        "complete_candidate_ids": list(candidates),
        "complete_candidate_ids_sha256": digest(list(candidates)),
        "complete_candidate_count": len(candidates),
        "candidate_root_rows": candidate_rows,
        "candidate_root_rows_sha256": digest(candidate_rows),
        "unique_strict_third_owner": winner,
    }


def witness_box(
    source: Any, face: dict[str, Any], port: dict[str, Any],
    discriminant_sign: int, expected_third_owner: str, precision_bits: int,
) -> tuple[tuple[Q, Q, Q, Q], int, dict[str, Any]]:
    slab = tuple(Q(value) for value in port["continuation_slab"]["source_coordinate_box"])
    boundary_axis = port["boundary_axis"]
    parameter_index = 2 if boundary_axis == "p" else 0
    parameter_lower, parameter_upper = slab[parameter_index:parameter_index + 2]
    if parameter_lower >= parameter_upper:
        raise RuntimeError("empty IFT parameter interval")
    endpoint_signs = tuple(port["isolated_root_endpoint_signs"])
    if sorted(endpoint_signs) != [-1, 1]:
        raise RuntimeError("IFT root bracket does not have opposite endpoint signs")
    use_lower_endpoint = endpoint_signs[0] == discriminant_sign
    last_error = "no attempt"
    for depth in range(2, MAX_WITNESS_SPLIT_DEPTH + 1):
        width = (parameter_upper - parameter_lower) / (2 ** depth)
        box = list(slab)
        if use_lower_endpoint:
            box[parameter_index + 1] = parameter_lower + width
        else:
            box[parameter_index] = parameter_upper - width
        candidate_box = tuple(box)
        try:
            evidence = classify_witness(
                source, face, candidate_box, discriminant_sign,
                expected_third_owner, precision_bits,
            )
            return candidate_box, depth, evidence
        except (ValueError, ZeroDivisionError, RuntimeError) as exc:
            last_error = f"{type(exc).__name__}:{exc}"
            continue
    raise RuntimeError(
        f"failed side witness split: {face['face_id']}:{discriminant_sign}:{last_error}"
    )


def choose_anchor(face: dict[str, Any], r87_map: dict[str, dict[str, Any]]) -> dict[str, Any]:
    candidates = [r87_map[port_id] for port_id in face["ordered_registered_port_ids"]]
    candidates.sort(
        key=lambda row: (
            -Q(row["continuation_slab"]["source_core_strict_rational_margin"]),
            row["registered_port_id"],
        )
    )
    return candidates[0]


def build(precision_bits: int = PRECISION_BITS) -> dict[str, Any]:
    ctx.prec = precision_bits
    documents = load_documents()
    faces = documents["r102"]["result"]["face_rows"]
    bindings = {row["face_id"]: row for row in documents["r103"]["result"]["binding_rows"]}
    f3_rows = {
        row["homogeneous_subbranch_id"]: row
        for row in documents["r104"]["result"]["F3_slot_rows"]
    }
    f4_rows = {
        row["homogeneous_subbranch_id"]: row
        for row in documents["r105"]["result"]["F4_slot_rows"]
    }
    r87_map = {
        row["registered_port_id"]: row
        for row in documents["r87"]["result"]["port_event_rows"]
    }
    r99_map = {
        row["registered_port_id"]: row
        for row in documents["r99"]["result"]["audit_rows"]
    }
    universal = documents["universal"]["result"]["universal_full_collision_branch_templates"]
    if universal["field_5_inverse_Jacobian_seed"]["completed_full_key_roof_level_field"]:
        raise RuntimeError("unexpected completed universal F5 field")
    if universal["field_6_log_Jacobian_distortion_seed"]["completed_full_key_roof_level_field"]:
        raise RuntimeError("unexpected completed universal F6 field")
    if documents["r106"]["result"]["required_adjacent_side_germ_count"] != 24:
        raise RuntimeError("Round106 adjacent-germ contract changed")

    cores = tuple(core_cert.physical_cores())
    rows: list[dict[str, Any]] = []
    face_pairs: list[dict[str, Any]] = []
    for face in faces:
        binding = bindings[face["face_id"]]
        f3 = f3_rows[face["face_id"]]
        f4 = f4_rows[face["face_id"]]
        anchor = choose_anchor(face, r87_map)
        corrected = r99_map[anchor["registered_port_id"]]
        if corrected["corrected_local_event_classification"] != "PHYSICAL_NEXT_TANGENCY__LOCAL_CONTINUATION":
            raise RuntimeError("canonical anchor is not corrected physical")
        if [
            anchor["source_core_index"], anchor["second_selected_target_id"],
            anchor["third_candidate_id"],
        ] != [
            face["source_core_index"], face["second_selected_target_id"],
            face["third_candidate_id"],
        ]:
            raise RuntimeError("anchor/face key mismatch")
        bypass_owner = corrected["corrected_unique_strict_future_competitor_winner"]
        if not bypass_owner:
            raise RuntimeError("physical anchor lacks bypass-side third owner")
        output_signs = f4["outgoing_direction_component_strict_signs"]
        face_row_ids: list[str] = []
        trace_ids: list[str] = []
        for side_sign, side_name, third_owner in (
            (-1, "BYPASS_SIDE", bypass_owner),
            (1, "DESIGNATED_COLLISION_SIDE", face["third_candidate_id"]),
        ):
            box, split_depth, evidence = witness_box(
                cores[face["source_core_index"]], face, anchor,
                side_sign, third_owner, precision_bits,
            )
            witness_output_signs = evidence["witness_outgoing_direction_component_strict_signs"]
            if witness_output_signs != output_signs:
                raise RuntimeError("local witness output chart does not restrict the incident face chart")
            owners = [binding["ordered_collision_owner_ids"][0], face["second_selected_target_id"], third_owner]
            cell_word_key = "physical-s0-rank3-return-word:" + digest({
                "ordered_collision_owner_ids": owners, "rank": 3,
            })
            suffix = target_chart(third_owner, witness_output_signs)
            identity = {
                "face_id": face["face_id"], "anchor_registered_port_id": anchor["registered_port_id"],
                "discriminant_side_sign": side_sign, "cell_word_key": cell_word_key,
            }
            germ_id = "physical-s0-rank3-adjacent-cell-germ:" + digest(identity)
            trace_id = "physical-s0-rank3-face-trace:" + digest({
                "face_id": face["face_id"], "cell_germ_id": germ_id, "side_sign": side_sign,
            })
            row = {
                "cell_germ_id": germ_id,
                "face_id": face["face_id"],
                "trace_id": trace_id,
                "trace_side_label": side_name,
                "discriminant_side_sign": side_sign,
                "anchor_registered_port_id": anchor["registered_port_id"],
                "source_core_index": face["source_core_index"],
                "incident_face_word_key": binding["word_key"],
                "cell_word_key": cell_word_key,
                "word_key_scope": (
                    "PROVISIONAL_ORDERED_OWNER_TUPLE_KEY__OFFICIAL_GATE5_WORD_GRAMMAR_CROSSWALK_PENDING"
                ),
                "ordered_collision_owner_ids": owners,
                "first_owner_id": owners[0],
                "second_owner_id": owners[1],
                "third_owner_id": owners[2],
                "designated_tangent_candidate_id": face["third_candidate_id"],
                "bypass_side_owner_id": bypass_owner,
                "prefix_chart": f3["field_value"],
                "suffix_chart": suffix,
                "face_suffix_chart": f4["field_value"],
                "chart_scope": (
                    "LOCAL_WITNESS_LABELS__CELL_KEYED_F3_F4_RESTRICTION_AND_WHOLE_TUBE_ENCLOSURE_PENDING"
                ),
                "outgoing_direction_component_strict_signs": output_signs,
                "source_coordinate_witness_box": list(map(str, box)),
                "witness_split_depth": split_depth,
                "local_trace_root_bracket": anchor["isolated_root_bracket"],
                "local_trace_root_endpoint_signs": anchor["isolated_root_endpoint_signs"],
                "IFT_parameter_derivative_sign": anchor["continuation_slab"]["parameter_derivative_sign"],
                "IFT_normal_derivative_sign": anchor["continuation_slab"]["normal_derivative_sign"],
                "IFT_implicit_root_slope_sign": anchor["continuation_slab"]["implicit_root_slope_sign"],
                "local_domain_definition": (
                    "open component of the pinned IFT slab with "
                    f"discriminant sign {side_sign:+d}"
                ),
                "cell_dimension": 2,
                "incident_face_dimension": 1,
                "positive_dimensional_open_smooth_cell_germ": True,
                "closure_contains_local_face_trace": True,
                "maximal_global_cell_asserted": False,
                "grazing_endpoint_included_in_closed_cell": False,
                **evidence,
            }
            if side_sign > 0 and cell_word_key != binding["word_key"]:
                raise RuntimeError("collision-side word key does not equal incident face word key")
            if side_sign < 0 and cell_word_key == binding["word_key"]:
                raise RuntimeError("bypass-side word unexpectedly equals face word")
            rows.append(row)
            face_row_ids.append(germ_id)
            trace_ids.append(trace_id)
        face_pairs.append({
            "face_id": face["face_id"],
            "anchor_registered_port_id": anchor["registered_port_id"],
            "adjacent_cell_germ_ids": face_row_ids,
            "trace_ids": trace_ids,
            "side_signs": [-1, 1],
            "two_sided_trace_pair_complete": True,
            "face_has_source_grazing_endpoint": "SOURCE_GRAZING" in face["endpoint_type_pair"],
        })

    rows.sort(key=lambda row: row["cell_germ_id"])
    face_pairs.sort(key=lambda row: row["face_id"])
    side_histogram = Counter(row["trace_side_label"] for row in rows)
    third_owner_histogram = Counter(row["third_owner_id"] for row in rows)
    if len(faces) != 12 or len(rows) != 24 or len(face_pairs) != 12:
        raise RuntimeError("atlas accounting")
    if len({row["cell_germ_id"] for row in rows}) != 24 or len({row["trace_id"] for row in rows}) != 24:
        raise RuntimeError("atlas ID uniqueness")
    if side_histogram != Counter({"BYPASS_SIDE": 12, "DESIGNATED_COLLISION_SIDE": 12}):
        raise RuntimeError("atlas side accounting")
    result = {
        "precision_bits": precision_bits,
        "input_corrected_face_count": len(faces),
        "canonical_anchor_port_count": len(face_pairs),
        "materialized_adjacent_side_germ_count": len(rows),
        "partial_topological_side_germ_skeleton_count": len(rows),
        "materialized_complete_smooth_operator_child_count": 0,
        "atlas_completion_status": "PARTIAL_LOCAL_LOWER_BOUND__WHOLE_FACE_SIDE_TUBES_AND_HOMOGENEITY_CHILDREN_PENDING",
        "complete_two_sided_face_pair_count": len(face_pairs),
        "positive_dimensional_open_smooth_cell_germ_count": sum(
            row["positive_dimensional_open_smooth_cell_germ"] for row in rows
        ),
        "materialized_face_trace_incidence_count": len(rows),
        "side_label_histogram": dict(sorted(side_histogram.items())),
        "third_owner_histogram": dict(sorted(third_owner_histogram.items())),
        "cell_germ_rows": rows,
        "cell_germ_rows_sha256": digest(rows),
        "face_pair_rows": face_pairs,
        "face_pair_rows_sha256": digest(face_pairs),
        "F5_installation_status": "NOT_INSTALLED__HOMOGENEITY_COLLAR_RECUT_AND_CHARACTERISTIC_RESTRICTION_JOIN_PENDING",
        "F6_installation_status": "NOT_INSTALLED__HOMOGENEITY_COLLAR_RECUT_AND_CHARACTERISTIC_RESTRICTION_JOIN_PENDING",
        "new_immutable_F5_slot_count": 0,
        "new_immutable_F6_slot_count": 0,
        "rank3_face_local_maturity": "4/18",
        "rank3_cell_local_maturity": "0/18",
        "complete_18_field_operator_block_count": 0,
        "global_Gate5": "NOT_CERTIFIED__10/18_BLOCKS_0",
        "strict_scope": (
            "twelve canonical local IFT trace patches with two side-labelled positive-dimensional "
            "smooth rank-three cell germs, complete immutable candidate replays, provisional "
            "ordered-owner tuple keys, and local collision-chart witness labels"
        ),
        "strict_nonclaims": [
            "the local germs are not promoted to maximal global operator cells",
            "twenty-four side germs are a geometric lower-bound skeleton, not the final homogeneity-refined row count",
            "the provisional ordered-owner tuple keys are not official Gate5 word keys; the frozen word-grammar crosswalk is pending",
            "face-local F1-F4 slots are not inherited as cell-keyed slots; cell restrictions and whole-tube chart enclosures are pending",
            "the designated-collision side approaches a genuine grazing trace and is not one finite homogeneous child",
            "the universal F5/F6 templates remain pre-characteristic-restriction seeds and are not installed",
            "no grazing endpoint is included in a closed finite inverse-Jacobian or distortion domain",
            "the global gate vector remains unchanged",
        ],
        "upstream_pins": PINS,
    }
    result = json.loads(json.dumps(result, sort_keys=True))
    return {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--precision-bits", type=int, default=PRECISION_BITS)
    args = parser.parse_args()
    print(json.dumps(build(args.precision_bits), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
