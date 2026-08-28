#!/usr/bin/env python3
"""Certify full-face occupancy for the immediately decidable curved regions."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import importlib
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
from typing import Any


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "cm2_round259_source_g_curved_region_full_face_saturation_certificate.json"
SCHEMA = "cm2.round259.source-g-curved-region-full-face-saturation.v1"
PINS = {
    "cm2_round179_source_g_residual_tube_arrangement_rows.json":
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    "cm2_round204_source_g_wall_return_signature_local_replacement.py":
        "7e4b81846155c1edad0807362c7086a290702da7ce6680d7c449b7193635da77",
    "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json":
        "e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818",
    "cm2_round208_source_g_outgoing_direct_signature_materialization.py":
        "c9fe0cdfb4631c31702473d705b04fa89fb8d51e4c71c9b2b652dc98e4641913",
    "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json":
        "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938",
    "cm2_round258_source_g_whole_box_boundary_face_saturation_certificate.json":
        "11d546a00cf27ae1fe5e146a18a64436676ec73214cd15dd294bb03bfb0359bb",
}


def need(value: bool, label: str) -> None:
    if not value:
        raise RuntimeError(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False,
    ).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def read_pinned(name: str) -> bytes:
    path = HERE / name
    info = path.lstat()
    need(
        stat.S_ISREG(info.st_mode) and not path.is_symlink()
        and 0 < info.st_size <= 500_000_000,
        f"regular:{name}",
    )
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == PINS[name], f"pin:{name}")
    return raw


def load_result(name: str) -> dict[str, Any]:
    document = json.loads(read_pinned(name))
    need(
        set(document) == {"schema", "result", "result_sha256"}
        and digest(document["result"]) == document["result_sha256"],
        f"envelope:{name}",
    )
    return document["result"]


def closed(row: dict[str, Any]) -> dict[str, Any]:
    result = dict(row)
    result["row_sha256"] = digest(result)
    return result


def ledger(rows: list[dict[str, Any]], id_field: str) -> dict[str, Any]:
    need(len(rows) == len({row[id_field] for row in rows}), f"unique:{id_field}")
    return {
        "row_count": len(rows),
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest([row[id_field] for row in rows]),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }


def text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


class DSU:
    def __init__(self, values: list[str]) -> None:
        self.parent = {value: value for value in values}

    def find(self, value: str) -> str:
        parent = self.parent[value]
        if parent != value:
            self.parent[value] = self.find(parent)
        return self.parent[value]

    def union(self, left: str, right: str) -> bool:
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root == right_root:
            return False
        if left_root > right_root:
            left_root, right_root = right_root, left_root
        self.parent[right_root] = left_root
        return True


def load_geometry() -> tuple[Any, ...]:
    read_pinned("cm2_round204_source_g_wall_return_signature_local_replacement.py")
    read_pinned("cm2_round208_source_g_outgoing_direct_signature_materialization.py")
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    round208_module = importlib.import_module(
        "cm2_round208_source_g_outgoing_direct_signature_materialization"
    )
    round204_module = importlib.import_module(
        "cm2_round204_source_g_wall_return_signature_local_replacement"
    )
    round207, _frozen = round208_module.load_evaluator()
    round198 = round207.r203.r198
    round195 = round198.r195
    round174_208 = round195.r191.r189.r188.r186.r179.r174
    _outgoing, collars208, _source = round195.r191.r189.load_scope()
    formal204 = round204_module.load_formal_inputs()
    evaluator204 = formal204["evaluator"]
    round179_204 = evaluator204.r179
    round174_204 = round179_204.r174
    scope182 = round204_module.extract_round182_scope(formal204["attachment182"])
    scope179 = round204_module.extract_round179_scope(
        formal204["source179"], scope182["occurrence_ids"], scope182["origin_ids"]
    )
    return (
        round208_module, round198, round174_208, collars208,
        round204_module, round179_204, round174_204, scope182, scope179,
    )


def occurrence_boxes(
    round204: dict[str, Any], round208: dict[str, Any]
) -> dict[str, tuple[Fraction, ...]]:
    rows179 = load_result("cm2_round179_source_g_residual_tube_arrangement_rows.json")
    columns = rows179["row_column_schemas"]["resolved_3d_child_rows"]
    boxes: dict[str, tuple[Fraction, ...]] = {}
    for packed in rows179["resolved_3d_child_rows"]:
        row = dict(zip(columns, packed))
        boxes[row["row_id"]] = tuple(Fraction(value) for value in row["box"])
    for row in round204["formal_local_open_3D_region_ledger"]["rows"]:
        boxes[row["region_row_id"]] = tuple(Fraction(value) for value in row["leaf_exact_box"])
    for row in round208["formal_local_open_3D_signature_ledger"]["rows"]:
        boxes[row["region_row_id"]] = tuple(Fraction(value) for value in row["Round182_leaf_box"])
    need(len(boxes) == 53_968, "occurrence box census")
    return boxes


def face_values(
    row: dict[str, Any], boxes: dict[str, tuple[Fraction, ...]]
) -> list[Fraction]:
    left, right = (boxes[value] for value in row["occurrence_row_ids"])
    axis = row["face_axis"]
    coordinate = Fraction(row["face_coordinate"])
    values: list[Fraction] = []
    for candidate in range(3):
        if candidate == axis:
            values.extend((coordinate, coordinate))
        else:
            values.extend((
                max(left[2 * candidate], right[2 * candidate]),
                min(left[2 * candidate + 1], right[2 * candidate + 1]),
            ))
    need(Fraction(row["exact_common_face_area"]) > 0, "positive face area")
    return values


def corridor_values(
    occurrence_id: str,
    face: list[Fraction],
    axis: int,
    coordinate: Fraction,
    depth: int,
    boxes: dict[str, tuple[Fraction, ...]],
) -> tuple[list[Fraction], Fraction, str]:
    source = boxes[occurrence_id]
    values = list(face)
    span = source[2 * axis + 1] - source[2 * axis]
    corridor_depth = span / (2 ** depth)
    if source[2 * axis + 1] == coordinate:
        values[2 * axis] = coordinate - corridor_depth
        values[2 * axis + 1] = coordinate
        side = "LOWER_SIDE_CORRIDOR"
    elif source[2 * axis] == coordinate:
        values[2 * axis] = coordinate
        values[2 * axis + 1] = coordinate + corridor_depth
        side = "UPPER_SIDE_CORRIDOR"
    else:
        raise RuntimeError(f"face incidence:{occurrence_id}")
    return values, corridor_depth, side


def evaluate_round204(
    region: dict[str, Any], values: list[Fraction], label: str,
    round204_module: Any, round179: Any, round174: Any,
    scope182: dict[str, Any], scope179: dict[str, Any],
) -> dict[str, Any]:
    collar = scope182["collars"][region["occurrence_row_id"]]
    wall = scope179["walls"][region["occurrence_row_id"]]
    box = round174.atlas.AtlasBox(*values, 0, label)
    geometry = round179.independent_geometry(collar["chart"], collar["owner_target"], box)
    source_name = round204_module.CHART_CONTRACT[collar["chart"]][2]
    target_name = "hit_x" if wall["axis"] == "X" else "hit_y"
    source_value = round179.subtract_wall(geometry[source_name], 0)[0]
    target_value = round179.subtract_wall(
        geometry[target_name], wall["integer_wall"]
    )[0]
    source_sign = round179.arb_sign(source_value)
    target_sign = round179.arb_sign(target_value)
    expected_source = "STRICT_" + region["source_sign"]
    expected_target = "STRICT_" + region["target_factor_sign"]
    return {
        "source_factor": source_name,
        "target_factor": target_name,
        "source_sign": source_sign,
        "target_sign": target_sign,
        "expected_source_sign": expected_source,
        "expected_target_sign": expected_target,
        "strict_region_match": source_sign == expected_source and target_sign == expected_target,
    }


def build() -> dict[str, Any]:
    round204 = load_result(
        "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json"
    )
    round208 = load_result(
        "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json"
    )
    round258 = load_result(
        "cm2_round258_source_g_whole_box_boundary_face_saturation_certificate.json"
    )
    need(
        round258["census"]["post_Round258_unified_quotient_component_count"] == 73_544
        and round258["census"]["curved_region_deferred_face_count"] == 13_836,
        "Round258 baseline",
    )
    (
        _round208_module, round198, round174_208, collars208,
        round204_module, round179_204, round174_204, scope182, scope179,
    ) = load_geometry()
    regions204 = {
        row["region_row_id"]: row
        for row in round204["formal_local_open_3D_region_ledger"]["rows"]
    }
    regions208 = {
        row["region_row_id"]: row
        for row in round208["formal_local_open_3D_signature_ledger"]["rows"]
    }
    boxes = occurrence_boxes(round204, round208)
    deferred258 = [
        row for row in round258["formal_rejected_or_deferred_boundary_face_ledger"]["rows"]
        if row["disposition"] == "DEFER_CURVED_REGION_FACE_OCCUPANCY_UNPROVED"
    ]
    need(len(deferred258) == 13_836, "Round258 deferred ledger")

    map258 = {
        row["Round257_quotient_component_id"]: row["post_Round258_quotient_component_id"]
        for row in round258["formal_Round257_to_Round258_component_map_ledger"]["rows"]
    }
    accepted_rows: list[dict[str, Any]] = []
    deferred_rows: list[dict[str, Any]] = []
    accepted_pairs: set[tuple[str, str]] = set()
    counts: Counter[str] = Counter()
    corridor_depth_counts: Counter[int] = Counter()
    area_sum = Fraction(0)
    corridor_volume_sum = Fraction(0)

    for index, source in enumerate(deferred258, 1):
        occurrence_ids = source["occurrence_row_ids"]
        axis = source["face_axis"]
        coordinate = Fraction(source["face_coordinate"])
        face = face_values(source, boxes)
        kinds = [
            "ROUND208" if occurrence_id in regions208
            else "ROUND204" if occurrence_id in regions204
            else "ROUND179"
            for occurrence_id in occurrence_ids
        ]
        face_proofs: dict[str, Any] = {}
        face_pass = False
        channel = ""
        if kinds.count("ROUND208") == 1:
            channel = "ROUND208_FACTOR_REGION_VS_WHOLE_BOX"
            curved_id = occurrence_ids[kinds.index("ROUND208")]
            region = regions208[curved_id]
            face_object = {
                "axis": ("t", "p", "s")[axis],
                "candidate_side": "UPPER",
                "anchor_side": "LOWER",
                "box": [text(value) for value in face],
            }
            proof = round198.compatible_strict_cell_patch(
                collars208[region["occurrence_row_id"]], face_object,
                region["HPLUS_sign"], region["HMINUS_sign"],
                f"round259-face:{index}:{curved_id}",
            )
            face_pass = proof["compatible_nonempty_relative_open_cell_patch"]
            face_proofs[curved_id] = proof
        elif all(kind == "ROUND204" for kind in kinds):
            channel = "ROUND204_TARGET_GRAPH_REGIONS"
            for occurrence_id in occurrence_ids:
                face_proofs[occurrence_id] = evaluate_round204(
                    regions204[occurrence_id], face,
                    f"round259-face:{index}:{occurrence_id}",
                    round204_module, round179_204, round174_204, scope182, scope179,
                )
            face_pass = all(proof["strict_region_match"] for proof in face_proofs.values())
        else:
            channel = "ROUND208_COMMON_FACE_REFINEMENT"

        corridor_rows: list[dict[str, Any]] = []
        corridor_pass = face_pass
        if face_pass:
            for occurrence_id, kind in zip(occurrence_ids, kinds):
                found: dict[str, Any] | None = None
                for depth in range(1, 9):
                    values, exact_depth, side = corridor_values(
                        occurrence_id, face, axis, coordinate, depth, boxes
                    )
                    if kind == "ROUND208":
                        region = regions208[occurrence_id]
                        profiles = round198.selected_factor_profiles(
                            collars208[region["occurrence_row_id"]],
                            round174_208.atlas.AtlasBox(
                                *values, 0,
                                f"round259-corridor:{index}:{occurrence_id}:{depth}",
                            ),
                        )
                        matched = (
                            profiles["HPLUS"]["selected_sign"] == region["HPLUS_sign"]
                            and profiles["HMINUS"]["selected_sign"] == region["HMINUS_sign"]
                        )
                        proof_object = profiles
                    elif kind == "ROUND204":
                        proof_object = evaluate_round204(
                            regions204[occurrence_id], values,
                            f"round259-corridor:{index}:{occurrence_id}:{depth}",
                            round204_module, round179_204, round174_204, scope182, scope179,
                        )
                        matched = proof_object["strict_region_match"]
                    else:
                        proof_object = {"whole_box_strict_open_corridor": True}
                        matched = True
                    if matched:
                        found = {
                            "occurrence_row_id": occurrence_id,
                            "corridor_side": side,
                            "dyadic_normal_depth": depth,
                            "exact_normal_depth": text(exact_depth),
                            "exact_corridor_box": [text(value) for value in values],
                            "strict_region_proof": proof_object,
                        }
                        break
                if found is None:
                    corridor_pass = False
                    break
                corridor_rows.append(found)

        if face_pass and corridor_pass:
            current_pair = tuple(sorted(
                map258[component_id] for component_id in source["pre_Round258_component_ids"]
            ))
            if current_pair[0] != current_pair[1]:
                accepted_pairs.add(current_pair)
            face_area = Fraction(source["exact_common_face_area"])
            area_sum += face_area
            for corridor in corridor_rows:
                depth = corridor["dyadic_normal_depth"]
                corridor_depth_counts[depth] += 1
                corridor_volume_sum += face_area * Fraction(corridor["exact_normal_depth"])
            counts["accepted"] += 1
            counts[f"accepted_{channel}"] += 1
            counts[f"accepted_axis_{axis}"] += 1
            accepted_rows.append(closed({
                "accepted_curved_face_row_id": "round259-accepted-curved-face:" + digest([
                    source["rejected_face_row_id"]
                ]),
                "Round258_boundary_face_candidate_id": source["rejected_face_row_id"],
                "official_key_id": source["official_key_id"],
                "source_chart": source["source_chart"],
                "identity_chart_transition": True,
                "face_axis": axis,
                "face_coordinate": source["face_coordinate"],
                "occurrence_row_ids": occurrence_ids,
                "pre_Round259_component_ids": list(current_pair),
                "already_internal_to_Round258_component": current_pair[0] == current_pair[1],
                "geometry_channel": channel,
                "exact_common_face_widths": source["exact_common_face_widths"],
                "exact_common_face_area": source["exact_common_face_area"],
                "full_relative_open_face_region_proofs": face_proofs,
                "strict_two_sided_corridor_proofs": corridor_rows,
                "disposition": "ACCEPT_STRICT_CURVED_REGION_FULL_FACE_WITH_TWO_SIDED_CORRIDOR",
                "physical_glue_credit": 1,
                "maximality_credit": 0,
            }))
        else:
            disposition = (
                "DEFER_R208_COMMON_FACE_REFINEMENT_REQUIRED"
                if channel == "ROUND208_COMMON_FACE_REFINEMENT"
                else "DEFER_R204_COMMON_FACE_REFINEMENT_REQUIRED"
                if channel == "ROUND204_TARGET_GRAPH_REGIONS"
                else "DEFER_R208_COMMON_FACE_REFINEMENT_REQUIRED"
            )
            counts["deferred"] += 1
            counts[disposition] += 1
            deferred_rows.append(closed({
                "Round259_deferred_face_row_id": "round259-deferred-face:" + digest([
                    source["rejected_face_row_id"]
                ]),
                "Round258_boundary_face_candidate_id": source["rejected_face_row_id"],
                "official_key_id": source["official_key_id"],
                "source_chart": source["source_chart"],
                "face_axis": axis,
                "face_coordinate": source["face_coordinate"],
                "occurrence_row_ids": occurrence_ids,
                "pre_Round259_component_ids": sorted(
                    map258[component_id] for component_id in source["pre_Round258_component_ids"]
                ),
                "geometry_channel": channel,
                "exact_common_face_widths": source["exact_common_face_widths"],
                "exact_common_face_area": source["exact_common_face_area"],
                "full_face_region_proofs": face_proofs,
                "disposition": disposition,
                "physical_glue_credit": 0,
                "maximality_credit": 0,
            }))

    accepted_rows.sort(key=lambda row: row["accepted_curved_face_row_id"])
    deferred_rows.sort(key=lambda row: row["Round259_deferred_face_row_id"])
    need(
        counts["accepted"] == 1_988
        and counts["accepted_ROUND208_FACTOR_REGION_VS_WHOLE_BOX"] == 1_764
        and counts["accepted_ROUND204_TARGET_GRAPH_REGIONS"] == 224
        and counts["accepted_axis_0"] == 904
        and counts["accepted_axis_1"] == 1_068
        and counts["accepted_axis_2"] == 16
        and counts["deferred"] == 11_848
        and counts["DEFER_R208_COMMON_FACE_REFINEMENT_REQUIRED"] == 10_784
        and counts["DEFER_R204_COMMON_FACE_REFINEMENT_REQUIRED"] == 1_064
        and corridor_depth_counts == Counter({1: 3_548, 2: 424, 3: 4})
        and area_sum == Fraction(2_374_447, 3_276_800_000)
        and corridor_volume_sum == Fraction(19_879_047, 1_677_721_600_000)
        and len(accepted_pairs) == 1_504,
        "curved face census",
    )

    source_components = round258["formal_post_Round258_component_commitment_ledger"]["rows"]
    component_keys = {
        row["post_Round258_quotient_component_id"]: (
            row["official_key_id"], row["official_key_ordinal"]
        )
        for row in source_components
    }
    need(len(component_keys) == 73_544, "Round258 component universe")
    dsu = DSU(sorted(component_keys))
    rank_reductions = 0
    for left, right in sorted(accepted_pairs):
        need(component_keys[left] == component_keys[right], f"key-pure edge:{left}:{right}")
        rank_reductions += int(dsu.union(left, right))
    need(rank_reductions == 1_480, "rank reduction census")
    members: dict[str, list[str]] = defaultdict(list)
    for component_id in sorted(component_keys):
        members[dsu.find(component_id)].append(component_id)
    need(len(members) == 72_064, "post Round259 component census")

    post_id_by_old: dict[str, str] = {}
    component_rows: list[dict[str, Any]] = []
    for constituent_ids in sorted(members.values(), key=lambda values: values[0]):
        keys = {component_keys[value] for value in constituent_ids}
        need(len(keys) == 1, "post Round259 key purity")
        key_id, ordinal = next(iter(keys))
        post_id = (
            constituent_ids[0] if len(constituent_ids) == 1
            else "round259-curved-full-face-component:" + digest(constituent_ids)
        )
        for old_id in constituent_ids:
            post_id_by_old[old_id] = post_id
        component_rows.append(closed({
            "post_Round259_component_row_id": "round259-component-row:" + digest([post_id]),
            "post_Round259_quotient_component_id": post_id,
            "official_key_id": key_id,
            "official_key_ordinal": ordinal,
            "constituent_Round258_component_count": len(constituent_ids),
            "constituent_Round258_component_ids": constituent_ids,
            "constituent_Round258_component_ids_sha256": digest(constituent_ids),
            "curved_full_face_edge_count": sum(
                1 for pair in accepted_pairs
                if pair[0] in constituent_ids and pair[1] in constituent_ids
            ),
            "certified_known_connectivity_only": True,
            "maximal_physical_component_claimed": False,
        }))
    component_rows.sort(key=lambda row: row["post_Round259_quotient_component_id"])

    map_rows = [closed({
        "Round258_to_Round259_component_map_row_id": "round259-component-map:" + digest([old_id]),
        "Round258_quotient_component_id": old_id,
        "post_Round259_quotient_component_id": post_id_by_old[old_id],
        "component_rank_reduction_credit": int(old_id != post_id_by_old[old_id]),
    }) for old_id in sorted(component_keys)]

    frontier258 = round258["formal_post_Round258_occurrence_quotient_frontier_ledger"]["rows"]
    post_frontier: list[dict[str, Any]] = []
    for row in frontier258:
        post = dict(row)
        post.pop("row_sha256")
        old_id = row["post_Round258_quotient_component_id"]
        post["post_Round259_quotient_component_id"] = post_id_by_old[old_id]
        post["Round259_curved_full_face_attachment_credit"] = int(
            old_id != post_id_by_old[old_id]
        )
        post_frontier.append(closed(post))
    post_frontier.sort(key=lambda row: row["post_frontier_row_id"])

    component_count_by_key = Counter(row["official_key_id"] for row in component_rows)
    accepted_by_key = Counter(row["official_key_id"] for row in accepted_rows)
    deferred_by_key = Counter(row["official_key_id"] for row in deferred_rows)
    key_rows: list[dict[str, Any]] = []
    for source in round258["formal_post_Round258_key_quotient_frontier_ledger"]["rows"]:
        key_id = source["official_key_id"]
        key_rows.append(closed({
            "post_Round259_key_frontier_row_id": "round259-key-frontier:" + digest([key_id]),
            "official_key_id": key_id,
            "official_key_ordinal": source["official_key_ordinal"],
            "local_occurrence_count": source["local_occurrence_count"],
            "post_Round259_quotient_component_count": component_count_by_key[key_id],
            "accepted_curved_full_face_count": accepted_by_key[key_id],
            "curved_common_refinement_deferred_face_count": deferred_by_key[key_id],
            "occurrence_quotient_assignment_complete": True,
            "all_quotient_components_proved_maximal": False,
            "global_exact_key_fibre_exhausted": False,
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
        }))
    key_rows.sort(key=lambda row: row["official_key_ordinal"])
    need(len(post_frontier) == 53_968 and len(key_rows) == 116, "frontier census")

    census = {
        "Round258_curved_region_deferred_face_count": 13_836,
        "accepted_curved_full_face_count": 1_988,
        "accepted_Round208_factor_region_vs_whole_box_face_count": 1_764,
        "accepted_Round204_target_graph_face_count": 224,
        "accepted_curved_full_face_count_by_axis": {"x": 904, "y": 1_068, "z": 16},
        "remaining_common_face_refinement_count": 11_848,
        "remaining_Round208_common_face_refinement_count": 10_784,
        "remaining_Round204_common_face_refinement_count": 1_064,
        "strict_corridor_dyadic_normal_depth_histogram": {
            str(key): corridor_depth_counts[key] for key in sorted(corridor_depth_counts)
        },
        "accepted_distinct_current_component_pair_count": 1_504,
        "rank_reducing_component_pair_count": 1_480,
        "redundant_certified_component_pair_count": 24,
        "post_Round258_unified_quotient_component_count": 73_544,
        "post_Round259_unified_quotient_component_count": 72_064,
        "exact_accepted_face_area_sum": text(area_sum),
        "exact_two_sided_corridor_volume_sum": text(corridor_volume_sum),
        "accepted_Round258_candidate_ids_sha256": digest(sorted(
            row["Round258_boundary_face_candidate_id"] for row in accepted_rows
        )),
        "occurrence_quotient_assignment_count": 53_968,
        "observed_exact_key_count": 116,
        "maximal_physical_component_assignment_count": 0,
        "globally_exhausted_exact_key_fibre_count": 0,
        "global_exact_key_disposition_count": 0,
    }
    need(
        census["accepted_Round258_candidate_ids_sha256"]
        == "974458059739191f495b73d8a88bca32797c6c9d79a21e85cce3b4f1d41dccdc",
        "accepted candidate commitment",
    )
    return {
        "status": (
            "CERTIFIED_1988_STRICT_CURVED_REGION_FULL_FACES__"
            "1480_RANK_REDUCTIONS__QUOTIENT_73544_TO_72064"
        ),
        "census": census,
        "formal_input_binding": {name: PINS[name] for name in sorted(PINS)},
        "formal_accepted_curved_region_full_face_ledger": ledger(
            accepted_rows, "accepted_curved_face_row_id"
        ),
        "formal_deferred_common_face_refinement_ledger": ledger(
            deferred_rows, "Round259_deferred_face_row_id"
        ),
        "formal_Round258_to_Round259_component_map_ledger": ledger(
            map_rows, "Round258_to_Round259_component_map_row_id"
        ),
        "formal_post_Round259_component_commitment_ledger": ledger(
            component_rows, "post_Round259_component_row_id"
        ),
        "formal_post_Round259_occurrence_quotient_frontier_ledger": ledger(
            post_frontier, "post_frontier_row_id"
        ),
        "formal_post_Round259_key_quotient_frontier_ledger": ledger(
            key_rows, "post_Round259_key_frontier_row_id"
        ),
        "scope_contract": {
            "only_full_relative_open_face_region_proofs_receive_glue": True,
            "every_accepted_face_has_an_explicit_strict_two_sided_3D_corridor": True,
            "all_11848_unresolved_faces_remain_fail_closed": True,
            "box_contact_or_exact_key_equality_alone_is_never_used_as_glue": True,
            "full_face_saturation_is_not_component_maximality": True,
        },
        "strict_nonpromotion": {
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
            "global_exact_key_disposition_credit": 0,
            "Gate5_filled_field_slot_count": 10,
            "Gate5_total_field_slot_count": 18,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": (
            "materialize dyadic common face refinements for the remaining 10784 Round208 "
            "and 1064 Round204 candidates, then audit pinned cross-chart transitions"
        ),
    }


def safe_write(raw: bytes) -> None:
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{OUTPUT.name}.", dir=OUTPUT.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, OUTPUT)
    finally:
        if temporary.exists():
            temporary.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()
    result = build()
    document = {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}
    raw = canonical(document) + b"\n"
    if not arguments.no_write:
        safe_write(raw)
    print(result["status"])
    print(json.dumps(result["census"], sort_keys=True))
    print(f"result_sha256={document['result_sha256']}")
    print(f"certificate_sha256={hashlib.sha256(raw).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
