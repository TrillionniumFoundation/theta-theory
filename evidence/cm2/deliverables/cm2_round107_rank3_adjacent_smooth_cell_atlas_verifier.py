#!/usr/bin/env python3
"""Independent 640-bit verifier for the Round107 two-sided local cell atlas.

This module intentionally does not import the Round107 producer.  It rebuilds
the face/word/chart crosswalk from frozen upstream documents and replays every
stored rational witness box with a complete immutable candidate tuple.
"""
from __future__ import annotations

import copy
import hashlib
import json
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
CERTIFICATE = HERE / "cm2-round107-rank3-adjacent-smooth-cell-atlas-2026-07-22.json"
SCHEMA = "cm2.round107.rank3-adjacent-smooth-cell-atlas.v1"
VERIFY_SCHEMA = "cm2.round107.rank3-adjacent-smooth-cell-atlas-verification.v1"
REBUILD_PRECISION_BITS = 640
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

TOP_KEYS = {"schema", "result", "result_sha256"}
RESULT_KEYS = {
    "precision_bits", "input_corrected_face_count", "canonical_anchor_port_count",
    "materialized_adjacent_side_germ_count", "complete_two_sided_face_pair_count",
    "partial_topological_side_germ_skeleton_count",
    "materialized_complete_smooth_operator_child_count", "atlas_completion_status",
    "positive_dimensional_open_smooth_cell_germ_count",
    "materialized_face_trace_incidence_count", "side_label_histogram",
    "third_owner_histogram", "cell_germ_rows", "cell_germ_rows_sha256",
    "face_pair_rows", "face_pair_rows_sha256", "F5_installation_status",
    "F6_installation_status", "new_immutable_F5_slot_count",
    "new_immutable_F6_slot_count", "rank3_face_local_maturity",
    "rank3_cell_local_maturity",
    "complete_18_field_operator_block_count", "global_Gate5", "strict_scope",
    "strict_nonclaims", "upstream_pins",
}
ROW_KEYS = {
    "cell_germ_id", "face_id", "trace_id", "trace_side_label",
    "discriminant_side_sign", "anchor_registered_port_id", "source_core_index",
    "incident_face_word_key", "cell_word_key", "ordered_collision_owner_ids",
    "word_key_scope",
    "first_owner_id", "second_owner_id", "third_owner_id",
    "designated_tangent_candidate_id", "bypass_side_owner_id", "prefix_chart",
    "suffix_chart", "face_suffix_chart", "outgoing_direction_component_strict_signs",
    "chart_scope",
    "source_coordinate_witness_box", "witness_split_depth", "local_trace_root_bracket",
    "local_trace_root_endpoint_signs", "IFT_parameter_derivative_sign",
    "IFT_normal_derivative_sign", "IFT_implicit_root_slope_sign",
    "local_domain_definition", "cell_dimension", "incident_face_dimension",
    "positive_dimensional_open_smooth_cell_germ", "closure_contains_local_face_trace",
    "maximal_global_cell_asserted", "grazing_endpoint_included_in_closed_cell",
    "two_collision_classification", "two_collision_owner_status", "second_outgoing_chart",
    "witness_outgoing_direction_component_strict_signs",
    "discriminant_strict_sign", "source_core_strict_rational_margin",
    "complete_candidate_ids", "complete_candidate_ids_sha256", "complete_candidate_count",
    "candidate_root_rows", "candidate_root_rows_sha256", "unique_strict_third_owner",
}
PAIR_KEYS = {
    "face_id", "anchor_registered_port_id", "adjacent_cell_germ_ids", "trace_ids",
    "side_signs", "two_sided_trace_pair_complete", "face_has_source_grazing_endpoint",
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


def strict_load(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_pairs,
        parse_constant=reject_nonfinite,
    )
    if not isinstance(value, dict):
        raise ValueError("top-level JSON is not an object")
    return value


def dependency_documents() -> dict[str, dict[str, Any]]:
    documents: dict[str, dict[str, Any]] = {}
    for alias, name in FILES.items():
        path = HERE / name
        if sha256(path) != PINS[name]:
            raise ValueError(f"dependency pin mismatch: {name}")
        documents[alias] = strict_load(path)
    return documents


def chart(target: str, signs: list[int]) -> str:
    return f"collision:{target}:open-semicircle:[{signs[0]},{signs[1]}]"


def margin(source: Any, box: tuple[Q, Q, Q, Q]) -> Q:
    t0, t1, p0, p1 = box
    return min(t0 - source.t0, source.t1 - t1, p0 - source.p0, source.p1 - p1)


def canonical_anchor(face: dict[str, Any], ports: dict[str, dict[str, Any]]) -> dict[str, Any]:
    choices = [ports[port_id] for port_id in face["ordered_registered_port_ids"]]
    return min(
        choices,
        key=lambda row: (
            -Q(row["continuation_slab"]["source_core_strict_rational_margin"]),
            row["registered_port_id"],
        ),
    )


def expected_witness_box(row: dict[str, Any], port: dict[str, Any]) -> tuple[Q, Q, Q, Q]:
    slab = tuple(Q(value) for value in port["continuation_slab"]["source_coordinate_box"])
    parameter_index = 2 if port["boundary_axis"] == "p" else 0
    lower, upper = slab[parameter_index:parameter_index + 2]
    depth = row["witness_split_depth"]
    if not isinstance(depth, int) or not 2 <= depth <= 96:
        raise ValueError("invalid witness split depth")
    endpoint_signs = port["isolated_root_endpoint_signs"]
    if sorted(endpoint_signs) != [-1, 1]:
        raise ValueError("invalid IFT endpoint signs")
    width = (upper - lower) / (2 ** depth)
    expected = list(slab)
    if endpoint_signs[0] == row["discriminant_side_sign"]:
        expected[parameter_index + 1] = lower + width
    else:
        expected[parameter_index] = upper - width
    return tuple(expected)


def recompute_geometry(
    row: dict[str, Any], face: dict[str, Any], source: Any,
) -> tuple[list[str], list[dict[str, Any]], str, list[int]]:
    box = tuple(Q(value) for value in row["source_coordinate_witness_box"])
    atom = step1.Atom(
        face["source_core_index"], source, *box, Q(0), Q(0),
        f"round107-independent-640:{row['cell_germ_id']}",
    )
    cores = tuple(core_cert.physical_cores())
    classification, owner_status, destination, state1, owner2 = (
        time3.homogeneity_cert.classify_with_geometry(atom, cores)
    )
    if classification != "SURVIVE_THROUGH_2_INNER" or destination is not None or owner2 is None:
        raise ValueError("640-bit witness fails two-collision survival")
    if owner_status != row["two_collision_owner_status"]:
        raise ValueError("640-bit owner status mismatch")
    if owner2["selected_target_id"] != face["second_selected_target_id"]:
        raise ValueError("640-bit second owner mismatch")
    state2 = time3.second_outgoing_state(atom, state1, owner2)
    if state2 is None or state2["chart"] != row["second_outgoing_chart"]:
        raise ValueError("640-bit second outgoing chart mismatch")
    jet = third_tangency_jet(
        source, face["second_selected_target_id"], face["third_candidate_id"], *box
    )
    if strict_sign(jet.value) != row["discriminant_side_sign"]:
        raise ValueError("640-bit discriminant sign mismatch")
    candidates = tuple(time3.time2_cert.translated_candidate_ids(
        face["second_selected_target_id"], state2["chart"]
    ))
    if len(candidates) != len(set(candidates)):
        raise ValueError("640-bit candidate tuple is not unique")
    root_rows: list[dict[str, Any]] = []
    future: list[tuple[str, Any]] = []
    for candidate_id in candidates:
        candidate = time3.time2_cert.candidate_root(
            state2["contact_x"], state2["contact_y"],
            state2["outgoing_x"], state2["outgoing_y"], state2["s"], candidate_id,
        )
        classification = candidate["classification"]
        if classification == "strict_future_near_root":
            future.append((candidate_id, candidate["near"]))
        elif classification not in ("no_real_intersection", "intersection_strictly_behind"):
            raise ValueError("640-bit unresolved candidate root")
        root_rows.append({"candidate_id": candidate_id, "root_classification": classification})
    winners = [
        candidate_id for candidate_id, near in future
        if all(candidate_id == other_id or bool(near < other_near) for other_id, other_near in future)
    ]
    if len(winners) != 1:
        raise ValueError("640-bit third owner is not unique")
    root_rows.sort(key=lambda item: item["candidate_id"])
    output_signs = [strict_sign(state2["outgoing_x"]), strict_sign(state2["outgoing_y"])]
    return list(candidates), root_rows, winners[0], output_signs


def validate(document: dict[str, Any], documents: dict[str, dict[str, Any]], geometry: bool) -> str:
    if set(document) != TOP_KEYS or document.get("schema") != SCHEMA:
        raise ValueError("closed top-level schema mismatch")
    result = document["result"]
    if not isinstance(result, dict) or set(result) != RESULT_KEYS:
        raise ValueError("closed result schema mismatch")
    if digest(result) != document["result_sha256"]:
        raise ValueError("result digest mismatch")
    if result["upstream_pins"] != PINS:
        raise ValueError("upstream pin ledger mismatch")
    rows = result["cell_germ_rows"]
    pairs = result["face_pair_rows"]
    if digest(rows) != result["cell_germ_rows_sha256"] or digest(pairs) != result["face_pair_rows_sha256"]:
        raise ValueError("row digest mismatch")
    if len(rows) != 24 or len(pairs) != 12:
        raise ValueError("atlas count mismatch")
    if result["partial_topological_side_germ_skeleton_count"] != 24:
        raise ValueError("partial skeleton count mismatch")
    if result["materialized_complete_smooth_operator_child_count"] != 0:
        raise ValueError("illegal complete operator-child claim")
    if result["rank3_cell_local_maturity"] != "0/18":
        raise ValueError("illegal cell-local field maturity claim")
    if any(set(row) != ROW_KEYS for row in rows) or any(set(pair) != PAIR_KEYS for pair in pairs):
        raise ValueError("closed row schema mismatch")
    if len({row["cell_germ_id"] for row in rows}) != 24 or len({row["trace_id"] for row in rows}) != 24:
        raise ValueError("duplicate cell/trace ID")
    by_face: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_face.setdefault(row["face_id"], []).append(row)
    if len(by_face) != 12 or any(sorted(row["discriminant_side_sign"] for row in group) != [-1, 1] for group in by_face.values()):
        raise ValueError("two-sided face pairing mismatch")
    if result["new_immutable_F5_slot_count"] != 0 or result["new_immutable_F6_slot_count"] != 0:
        raise ValueError("illegal F5/F6 promotion")
    if result["global_Gate5"] != "NOT_CERTIFIED__10/18_BLOCKS_0":
        raise ValueError("illegal Gate5 promotion")

    faces = {row["face_id"]: row for row in documents["r102"]["result"]["face_rows"]}
    bindings = {row["face_id"]: row for row in documents["r103"]["result"]["binding_rows"]}
    f3s = {row["homogeneous_subbranch_id"]: row for row in documents["r104"]["result"]["F3_slot_rows"]}
    f4s = {row["homogeneous_subbranch_id"]: row for row in documents["r105"]["result"]["F4_slot_rows"]}
    ports = {row["registered_port_id"]: row for row in documents["r87"]["result"]["port_event_rows"]}
    audits = {row["registered_port_id"]: row for row in documents["r99"]["result"]["audit_rows"]}
    cores = tuple(core_cert.physical_cores())
    projection: list[dict[str, Any]] = []
    for face_id, group in sorted(by_face.items()):
        if face_id not in faces:
            raise ValueError("unknown face ID")
        face = faces[face_id]
        binding = bindings[face_id]
        anchor = canonical_anchor(face, ports)
        audit = audits[anchor["registered_port_id"]]
        if audit["corrected_local_event_classification"] != "PHYSICAL_NEXT_TANGENCY__LOCAL_CONTINUATION":
            raise ValueError("anchor is not corrected physical")
        bypass_owner = audit["corrected_unique_strict_future_competitor_winner"]
        pair = next((pair for pair in pairs if pair["face_id"] == face_id), None)
        if pair is None or pair["side_signs"] != [-1, 1] or not pair["two_sided_trace_pair_complete"]:
            raise ValueError("missing face-pair row")
        for row in group:
            sign = row["discriminant_side_sign"]
            side_name = "DESIGNATED_COLLISION_SIDE" if sign > 0 else "BYPASS_SIDE"
            third_owner = face["third_candidate_id"] if sign > 0 else bypass_owner
            owners = [binding["ordered_collision_owner_ids"][0], face["second_selected_target_id"], third_owner]
            word_key = "physical-s0-rank3-return-word:" + digest({
                "ordered_collision_owner_ids": owners, "rank": 3,
            })
            expected_identity = {
                "face_id": face_id, "anchor_registered_port_id": anchor["registered_port_id"],
                "discriminant_side_sign": sign, "cell_word_key": word_key,
            }
            germ_id = "physical-s0-rank3-adjacent-cell-germ:" + digest(expected_identity)
            trace_id = "physical-s0-rank3-face-trace:" + digest({
                "face_id": face_id, "cell_germ_id": germ_id, "side_sign": sign,
            })
            signs = f4s[face_id]["outgoing_direction_component_strict_signs"]
            expected_box = expected_witness_box(row, anchor)
            stored_box = tuple(Q(value) for value in row["source_coordinate_witness_box"])
            expected_semantics = {
                "anchor_registered_port_id": anchor["registered_port_id"],
                "trace_side_label": side_name, "third_owner_id": third_owner,
                "bypass_side_owner_id": bypass_owner, "ordered_collision_owner_ids": owners,
                "cell_word_key": word_key, "incident_face_word_key": binding["word_key"],
                "word_key_scope": (
                    "PROVISIONAL_ORDERED_OWNER_TUPLE_KEY__OFFICIAL_GATE5_WORD_GRAMMAR_CROSSWALK_PENDING"
                ),
                "cell_germ_id": germ_id, "trace_id": trace_id,
                "prefix_chart": f3s[face_id]["field_value"],
                "suffix_chart": chart(third_owner, signs),
                "face_suffix_chart": f4s[face_id]["field_value"],
                "chart_scope": (
                    "LOCAL_WITNESS_LABELS__CELL_KEYED_F3_F4_RESTRICTION_AND_WHOLE_TUBE_ENCLOSURE_PENDING"
                ),
            }
            for key, expected in expected_semantics.items():
                if row[key] != expected:
                    raise ValueError(f"semantic crosswalk mismatch: {key}")
            if stored_box != expected_box:
                raise ValueError("witness box is not the canonical endpoint band")
            box_margin = margin(cores[face["source_core_index"]], stored_box)
            if box_margin <= 0 or str(box_margin) != row["source_core_strict_rational_margin"]:
                raise ValueError("witness box core margin mismatch")
            if not (stored_box[0] < stored_box[1] and stored_box[2] < stored_box[3]):
                raise ValueError("witness box is not positive dimensional")
            if not row["positive_dimensional_open_smooth_cell_germ"] or row["cell_dimension"] != 2:
                raise ValueError("cell germ dimension/smoothness mismatch")
            if row["incident_face_dimension"] != 1 or not row["closure_contains_local_face_trace"]:
                raise ValueError("face trace incidence mismatch")
            if row["maximal_global_cell_asserted"] or row["grazing_endpoint_included_in_closed_cell"]:
                raise ValueError("illegal global/closed-grazing scope assertion")
            if row["witness_outgoing_direction_component_strict_signs"] != signs:
                raise ValueError("local witness/face chart sign mismatch")
            if len(row["complete_candidate_ids"]) != row["complete_candidate_count"]:
                raise ValueError("complete candidate count mismatch")
            if digest(row["complete_candidate_ids"]) != row["complete_candidate_ids_sha256"]:
                raise ValueError("complete candidate tuple digest mismatch")
            if digest(row["candidate_root_rows"]) != row["candidate_root_rows_sha256"]:
                raise ValueError("candidate root ledger digest mismatch")
            if sorted(row["complete_candidate_ids"]) != sorted(
                item["candidate_id"] for item in row["candidate_root_rows"]
            ):
                raise ValueError("candidate tuple/root-ledger key mismatch")
            if geometry:
                candidate_ids, root_rows, winner, output_signs = recompute_geometry(
                    row, face, cores[face["source_core_index"]]
                )
                if candidate_ids != row["complete_candidate_ids"] or digest(candidate_ids) != row["complete_candidate_ids_sha256"]:
                    raise ValueError("640-bit immutable candidate tuple mismatch")
                if root_rows != row["candidate_root_rows"] or digest(root_rows) != row["candidate_root_rows_sha256"]:
                    raise ValueError("640-bit candidate root ledger mismatch")
                if winner != row["unique_strict_third_owner"] or winner != third_owner:
                    raise ValueError("640-bit third owner mismatch")
                if output_signs != row["witness_outgoing_direction_component_strict_signs"]:
                    raise ValueError("640-bit outgoing chart-sign mismatch")
            projection.append({
                "face_id": face_id, "side_sign": sign, "cell_germ_id": germ_id,
                "trace_id": trace_id, "cell_word_key": word_key, "owners": owners,
                "prefix_chart": f3s[face_id]["field_value"],
                "suffix_chart": chart(third_owner, signs),
            })
        if sorted(pair["adjacent_cell_germ_ids"]) != sorted(row["cell_germ_id"] for row in group):
            raise ValueError("pair cell IDs mismatch")
        if sorted(pair["trace_ids"]) != sorted(row["trace_id"] for row in group):
            raise ValueError("pair trace IDs mismatch")
    projection.sort(key=lambda row: (row["face_id"], row["side_sign"]))
    return digest(projection)


def mutation_rejection_count(document: dict[str, Any], documents: dict[str, dict[str, Any]]) -> int:
    mutations: list[dict[str, Any]] = []
    first = document["result"]["cell_germ_rows"][0]

    missing = copy.deepcopy(document)
    missing["result"]["cell_germ_rows"].pop()
    mutations.append(missing)

    duplicate_side = copy.deepcopy(document)
    same_face = [row for row in duplicate_side["result"]["cell_germ_rows"] if row["face_id"] == first["face_id"]]
    same_face[1]["discriminant_side_sign"] = same_face[0]["discriminant_side_sign"]
    mutations.append(duplicate_side)

    wrong_owner = copy.deepcopy(document)
    wrong_owner["result"]["cell_germ_rows"][0]["third_owner_id"] = "W[999,999]"
    mutations.append(wrong_owner)

    wrong_chart = copy.deepcopy(document)
    wrong_chart["result"]["cell_germ_rows"][0]["prefix_chart"] = "collision:BAD:BAD"
    mutations.append(wrong_chart)

    bad_box = copy.deepcopy(document)
    bad_box["result"]["cell_germ_rows"][0]["source_coordinate_witness_box"] = ["0", "0", "0", "0"]
    mutations.append(bad_box)

    truncated = copy.deepcopy(document)
    truncated["result"]["cell_germ_rows"][0]["complete_candidate_ids"].pop()
    mutations.append(truncated)

    promoted = copy.deepcopy(document)
    promoted["result"]["new_immutable_F5_slot_count"] = 12
    promoted["result"]["global_Gate5"] = "CERTIFIED"
    mutations.append(promoted)

    rejected = 0
    for mutation in mutations:
        mutation["result"]["cell_germ_rows_sha256"] = digest(mutation["result"]["cell_germ_rows"])
        mutation["result"]["face_pair_rows_sha256"] = digest(mutation["result"]["face_pair_rows"])
        mutation["result_sha256"] = digest(mutation["result"])
        try:
            validate(mutation, documents, geometry=False)
        except (ValueError, KeyError, TypeError, ArithmeticError):
            rejected += 1
    return rejected


def strict_json_attack_count(raw: str) -> int:
    attacks = [
        raw[:-1] + ',"schema":"duplicate"}',
        '{"schema":NaN,"result":{},"result_sha256":"x"}',
        raw[:-1] + ',"unknown_top_level":true}',
    ]
    rejected = 0
    for attack in attacks:
        try:
            value = json.loads(attack, object_pairs_hook=strict_pairs, parse_constant=reject_nonfinite)
            if set(value) != TOP_KEYS:
                raise ValueError("unknown top-level key")
        except (ValueError, TypeError):
            rejected += 1
    return rejected


def build() -> dict[str, Any]:
    ctx.prec = REBUILD_PRECISION_BITS
    documents = dependency_documents()
    raw = CERTIFICATE.read_text(encoding="utf-8")
    document = strict_load(CERTIFICATE)
    projection_sha256 = validate(document, documents, geometry=True)
    mutations = mutation_rejection_count(document, documents)
    json_attacks = strict_json_attack_count(raw)
    if mutations != 7 or json_attacks != 3:
        raise RuntimeError("hostile test accounting")
    result = {
        "status": "PASS",
        "producer_precision_bits": document["result"]["precision_bits"],
        "independent_rebuild_precision_bits": REBUILD_PRECISION_BITS,
        "producer_module_imported": False,
        "reconstructed_face_count": 12,
        "reconstructed_cell_germ_count": 24,
        "reconstructed_trace_pair_count": 12,
        "complete_immutable_candidate_replays": 24,
        "semantic_projection_sha256": projection_sha256,
        "hostile_semantic_mutations_rejected": f"{mutations}/7",
        "strict_json_attacks_rejected": f"{json_attacks}/3",
        "certificate_json_sha256": sha256(CERTIFICATE),
        "upstream_pins": PINS,
    }
    return {"schema": VERIFY_SCHEMA, "result": result, "result_sha256": digest(result)}


if __name__ == "__main__":
    print(json.dumps(build(), sort_keys=True, indent=2))
