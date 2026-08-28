#!/usr/bin/env python3
"""Saturate exact same-chart boundary faces between whole-box regions."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile
from typing import Any


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "cm2_round258_source_g_whole_box_boundary_face_saturation_certificate.json"
SCHEMA = "cm2.round258.source-g-whole-box-boundary-face-saturation.v1"
PINS = {
    "cm2_round179_source_g_residual_tube_arrangement_rows.json":
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json":
        "e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818",
    "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json":
        "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938",
    "cm2_round254_source_g_seed_block_quotient_closure_certificate.json":
        "b3823b57ba6112c37b63fa1eab85507659038170277634853eb0453f418c47cf",
    "cm2_round255_source_g_block_carrier_quotient_augmentation_certificate.json":
        "d7a2ad5175d1671ca4000e287c0c201826e41e4da718fa5af3c840a80417db0d",
    "cm2_round256_source_g_local_occurrence_carrier_completion_certificate.json":
        "b72ed5f3c4d28a9ea9fea1eda1e7259db08c3a2bdda40d0959aaee6bf0482772",
    "cm2_round257_source_g_occurrence_fibre_volume_overlap_saturation_certificate.json":
        "320d8221dcc11d227f667a9e7efbd64c5e40f1de214b22ddd5264079b93504fb",
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


def signature_tuple(signature: dict[str, Any]) -> tuple[Any, ...]:
    return (
        signature["source_chart"], signature["target_lift"],
        tuple(tuple(event) for event in signature["ordered_integer_wall_events"]),
        tuple(signature["signed_wall_word"]), signature["roof"],
        signature["outgoing_cell"], signature["target_chart"],
        tuple(signature["official_key_row"]), signature["official_key_ordinal"],
        signature["official_key_id"],
    )


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


def occurrence_metadata() -> dict[str, dict[str, Any]]:
    rows179 = load_result("cm2_round179_source_g_residual_tube_arrangement_rows.json")
    round204 = load_result(
        "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json"
    )
    round208 = load_result(
        "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json"
    )
    metadata: dict[str, dict[str, Any]] = {}
    columns = rows179["row_column_schemas"]["resolved_3d_child_rows"]
    for packed in rows179["resolved_3d_child_rows"]:
        row = dict(zip(columns, packed))
        signature = {
            "source_chart": row["chart"],
            "target_lift": row["owner_target"],
            "ordered_integer_wall_events": row["ordered_integer_wall_events"],
            "signed_wall_word": row["signed_wall_word"],
            "roof": row["roof"],
            "outgoing_cell": row["outgoing_cell"],
            "target_chart": row["target_chart"],
            "official_key_row": row["official_key_row"],
            "official_key_ordinal": row["official_key_ordinal"],
            "official_key_id": row["official_key_id"],
        }
        metadata[row["row_id"]] = {
            "chart": row["chart"], "box_values": row["box"],
            "box": tuple(Fraction(value) for value in row["box"]),
            "geometry_class": "ROUND179_RESOLVED_WHOLE_BOX",
            "whole_box_region": True, "signature": signature_tuple(signature),
            "signature_object": signature,
        }

    regions204 = round204["formal_local_open_3D_region_ledger"]["rows"]
    regions204_by_leaf: Counter[str] = Counter(row["leaf_row_id"] for row in regions204)
    for row in regions204:
        whole = (
            row["graph_classification"] == "EMPTY"
            and row["region_kind"] == "NO_TARGET_SHEET_REGION"
            and regions204_by_leaf[row["leaf_row_id"]] == 1
        )
        signature = {
            "source_chart": row["chart"], "target_lift": row["owner_target"],
            "ordered_integer_wall_events": row["ordered_integer_wall_events"],
            "signed_wall_word": row["signed_wall_word"], "roof": row["roof"],
            "outgoing_cell": row["outgoing_cell"], "target_chart": row["target_chart"],
            "official_key_row": row["official_key_row"],
            "official_key_ordinal": row["official_key_ordinal"],
            "official_key_id": row["official_key_id"],
        }
        metadata[row["region_row_id"]] = {
            "chart": row["chart"], "box_values": row["leaf_exact_box"],
            "box": tuple(Fraction(value) for value in row["leaf_exact_box"]),
            "geometry_class": f"ROUND204_{row['graph_classification']}_{row['region_kind']}",
            "whole_box_region": whole, "signature": signature_tuple(signature),
            "signature_object": signature,
        }

    regions208 = round208["formal_local_open_3D_signature_ledger"]["rows"]
    regions208_by_leaf: Counter[str] = Counter(row["leaf_row_id"] for row in regions208)
    for row in regions208:
        whole = row["leaf_classification"] == "EMPTY" and regions208_by_leaf[row["leaf_row_id"]] == 1
        signature = row["local_return_signature"]
        metadata[row["region_row_id"]] = {
            "chart": signature["source_chart"], "box_values": row["Round182_leaf_box"],
            "box": tuple(Fraction(value) for value in row["Round182_leaf_box"]),
            "geometry_class": f"ROUND208_{row['F_sign']}_{row['leaf_classification']}",
            "whole_box_region": whole, "signature": signature_tuple(signature),
            "signature_object": signature,
        }
    need(len(metadata) == 53_968, "metadata census")
    return metadata


def build() -> dict[str, Any]:
    round254 = load_result("cm2_round254_source_g_seed_block_quotient_closure_certificate.json")
    round255 = load_result("cm2_round255_source_g_block_carrier_quotient_augmentation_certificate.json")
    round256 = load_result("cm2_round256_source_g_local_occurrence_carrier_completion_certificate.json")
    round257 = load_result("cm2_round257_source_g_occurrence_fibre_volume_overlap_saturation_certificate.json")
    need(
        round257["census"]["post_Round257_unified_quotient_component_count"] == 74_012
        and round257["census"]["cross_component_positive_volume_overlap_count"] == 0,
        "Round257 baseline",
    )
    frontier = round256["formal_post_Round256_complete_occurrence_quotient_frontier_ledger"]["rows"]
    metadata = occurrence_metadata()
    need(
        len(frontier) == 53_968
        and set(metadata) == {row["local_occurrence_row_id"] for row in frontier},
        "frontier/metadata bijection",
    )

    component_keys: dict[str, tuple[str, int]] = {}
    for row in round254["formal_post_Round254_component_commitment_ledger"]["rows"]:
        component_keys[row["post_Round254_mixed_sheet_quotient_component_id"]] = (
            row["official_key_id"], row["official_key_ordinal"]
        )
    for row in round255["formal_new_known_block_carrier_component_ledger"]["rows"]:
        component_keys[row["post_Round255_quotient_component_id"]] = (
            row["official_key_id"], row["official_key_ordinal"]
        )
    for row in round256["formal_new_local_occurrence_carrier_ledger"]["rows"]:
        component_keys[row["post_Round256_quotient_component_id"]] = (
            row["official_key_id"], row["official_key_ordinal"]
        )
    need(len(component_keys) == 74_012, "component universe")

    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for occurrence in frontier:
        occurrence_id = occurrence["local_occurrence_row_id"]
        item = metadata[occurrence_id]
        need(
            item["signature_object"]["official_key_id"] == occurrence["official_key_id"],
            f"key:{occurrence_id}",
        )
        groups[(occurrence["official_key_id"], item["chart"])].append({
            "occurrence_id": occurrence_id,
            "component_id": occurrence["post_Round256_quotient_component_id"],
            **item,
        })
    need(len(groups) == 116, "key/chart groups")

    accepted_rows: list[dict[str, Any]] = []
    rejected_rows: list[dict[str, Any]] = []
    candidate_counts: Counter[str] = Counter()
    accepted_component_pairs: set[tuple[str, str]] = set()
    area_sum = Fraction(0)
    corridor_volume_sum = Fraction(0)
    for (key_id, chart), rows in sorted(groups.items()):
        for axis in range(3):
            lower: dict[Fraction, list[dict[str, Any]]] = defaultdict(list)
            upper: dict[Fraction, list[dict[str, Any]]] = defaultdict(list)
            for row in rows:
                lower[row["box"][2 * axis]].append(row)
                upper[row["box"][2 * axis + 1]].append(row)
            for coordinate in sorted(set(lower) & set(upper)):
                for left in sorted(upper[coordinate], key=lambda row: row["occurrence_id"]):
                    for right in sorted(lower[coordinate], key=lambda row: row["occurrence_id"]):
                        if (
                            left["occurrence_id"] == right["occurrence_id"]
                            or left["component_id"] == right["component_id"]
                        ):
                            continue
                        transverse = [candidate for candidate in range(3) if candidate != axis]
                        widths = [
                            min(left["box"][2 * candidate + 1], right["box"][2 * candidate + 1])
                            - max(left["box"][2 * candidate], right["box"][2 * candidate])
                            for candidate in transverse
                        ]
                        if min(widths) <= 0:
                            continue
                        pair_ids = sorted([left["occurrence_id"], right["occurrence_id"]])
                        candidate_id = "round258-boundary-face-candidate:" + digest(
                            [key_id, chart, axis, text(coordinate), pair_ids]
                        )
                        face_area = widths[0] * widths[1]
                        signature_equal = left["signature"] == right["signature"]
                        both_whole = left["whole_box_region"] and right["whole_box_region"]
                        candidate_counts["candidate_count"] += 1
                        candidate_counts[f"axis_{axis}_candidate_count"] += 1
                        if not signature_equal:
                            disposition = "REJECT_FULL_RETURN_SIGNATURE_MISMATCH"
                        elif not both_whole:
                            disposition = "DEFER_CURVED_REGION_FACE_OCCUPANCY_UNPROVED"
                        else:
                            disposition = "ACCEPT_STRICT_TWO_SIDED_WHOLE_BOX_FACE"
                            left_depth = (left["box"][2 * axis + 1] - left["box"][2 * axis]) / 2
                            right_depth = (right["box"][2 * axis + 1] - right["box"][2 * axis]) / 2
                            left_volume = face_area * left_depth
                            right_volume = face_area * right_depth
                            component_pair = tuple(sorted([left["component_id"], right["component_id"]]))
                            accepted_component_pairs.add(component_pair)
                            area_sum += face_area
                            corridor_volume_sum += left_volume + right_volume
                            accepted_rows.append(closed({
                                "accepted_face_row_id": candidate_id,
                                "official_key_id": key_id,
                                "official_key_ordinal": left["signature_object"]["official_key_ordinal"],
                                "source_chart": chart,
                                "identity_chart_transition": True,
                                "face_axis": axis,
                                "face_coordinate": text(coordinate),
                                "occurrence_row_ids": pair_ids,
                                "pre_Round258_component_ids": list(component_pair),
                                "left_geometry_class": left["geometry_class"],
                                "right_geometry_class": right["geometry_class"],
                                "complete_ten_field_return_signature": left["signature_object"],
                                "exact_common_face_widths": [text(width) for width in widths],
                                "exact_common_face_area": text(face_area),
                                "left_strict_corridor_depth": text(left_depth),
                                "right_strict_corridor_depth": text(right_depth),
                                "left_strict_corridor_volume": text(left_volume),
                                "right_strict_corridor_volume": text(right_volume),
                                "half_open_face_owner_occurrence_id": min(pair_ids),
                                "disposition": disposition,
                                "physical_glue_credit": 1,
                            }))
                            candidate_counts["accepted_count"] += 1
                            candidate_counts[f"axis_{axis}_accepted_count"] += 1
                            continue
                        rejected_rows.append(closed({
                            "rejected_face_row_id": candidate_id,
                            "official_key_id": key_id,
                            "source_chart": chart,
                            "face_axis": axis,
                            "face_coordinate": text(coordinate),
                            "occurrence_row_ids": pair_ids,
                            "pre_Round258_component_ids": sorted([
                                left["component_id"], right["component_id"]
                            ]),
                            "left_geometry_class": left["geometry_class"],
                            "right_geometry_class": right["geometry_class"],
                            "exact_common_face_widths": [text(width) for width in widths],
                            "exact_common_face_area": text(face_area),
                            "complete_ten_field_return_signature_equal": signature_equal,
                            "both_regions_certified_whole_box": both_whole,
                            "disposition": disposition,
                            "physical_glue_credit": 0,
                        }))
                        candidate_counts[
                            "signature_mismatch_count" if not signature_equal
                            else "curved_region_deferred_count"
                        ] += 1

    accepted_rows.sort(key=lambda row: row["accepted_face_row_id"])
    rejected_rows.sort(key=lambda row: row["rejected_face_row_id"])
    need(
        candidate_counts["candidate_count"] == 27_288
        and candidate_counts["signature_mismatch_count"] == 12_548
        and candidate_counts["curved_region_deferred_count"] == 13_836
        and candidate_counts["accepted_count"] == 904
        and len(accepted_component_pairs) == 852,
        "face candidate census",
    )

    dsu = DSU(sorted(component_keys))
    rank_reductions = 0
    for left, right in sorted(accepted_component_pairs):
        need(component_keys[left] == component_keys[right], f"component key pair:{left}:{right}")
        rank_reductions += int(dsu.union(left, right))
    need(rank_reductions == 468, "rank reduction census")
    members: dict[str, list[str]] = defaultdict(list)
    for component_id in sorted(component_keys):
        members[dsu.find(component_id)].append(component_id)
    need(len(members) == 73_544, "post component census")
    post_id_by_old: dict[str, str] = {}
    component_rows: list[dict[str, Any]] = []
    for constituent_ids in sorted(members.values(), key=lambda values: values[0]):
        keys = {component_keys[value] for value in constituent_ids}
        need(len(keys) == 1, "post component key purity")
        key_id, ordinal = next(iter(keys))
        post_id = (
            constituent_ids[0] if len(constituent_ids) == 1
            else "round258-whole-box-face-component:" + digest(constituent_ids)
        )
        for old_id in constituent_ids:
            post_id_by_old[old_id] = post_id
        component_rows.append(closed({
            "post_Round258_component_row_id": "round258-component-row:" + digest([post_id]),
            "post_Round258_quotient_component_id": post_id,
            "official_key_id": key_id,
            "official_key_ordinal": ordinal,
            "constituent_Round257_component_count": len(constituent_ids),
            "constituent_Round257_component_ids": constituent_ids,
            "constituent_Round257_component_ids_sha256": digest(constituent_ids),
            "whole_box_face_edge_count": sum(
                1 for pair in accepted_component_pairs
                if pair[0] in constituent_ids and pair[1] in constituent_ids
            ),
            "certified_known_connectivity_only": True,
            "maximal_physical_component_claimed": False,
        }))
    component_rows.sort(key=lambda row: row["post_Round258_quotient_component_id"])

    map_rows = [closed({
        "Round257_to_Round258_component_map_row_id": "round258-component-map:" + digest([old_id]),
        "Round257_quotient_component_id": old_id,
        "post_Round258_quotient_component_id": post_id_by_old[old_id],
        "component_rank_reduction_credit": int(old_id != post_id_by_old[old_id]),
    }) for old_id in sorted(component_keys)]

    post_frontier: list[dict[str, Any]] = []
    for row in frontier:
        post = dict(row)
        post.pop("row_sha256")
        old_id = row["post_Round256_quotient_component_id"]
        post["post_Round258_quotient_component_id"] = post_id_by_old[old_id]
        post["Round258_whole_box_face_attachment_credit"] = int(old_id != post_id_by_old[old_id])
        post_frontier.append(closed(post))
    post_frontier.sort(key=lambda row: row["post_frontier_row_id"])

    component_count_by_key: Counter[str] = Counter(
        row["official_key_id"] for row in component_rows
    )
    accepted_by_key: Counter[str] = Counter(row["official_key_id"] for row in accepted_rows)
    deferred_by_key: Counter[str] = Counter(
        row["official_key_id"] for row in rejected_rows
        if row["disposition"] == "DEFER_CURVED_REGION_FACE_OCCUPANCY_UNPROVED"
    )
    mismatch_by_key: Counter[str] = Counter(
        row["official_key_id"] for row in rejected_rows
        if row["disposition"] == "REJECT_FULL_RETURN_SIGNATURE_MISMATCH"
    )
    source_key_rows = round256["formal_post_Round256_complete_key_quotient_frontier_ledger"]["rows"]
    key_rows = []
    for row in source_key_rows:
        key_id = row["official_key_id"]
        key_rows.append(closed({
            "post_Round258_key_frontier_row_id": "round258-key-frontier:" + digest([key_id]),
            "official_key_id": key_id,
            "official_key_ordinal": row["official_key_ordinal"],
            "local_occurrence_count": row["local_occurrence_count"],
            "post_Round258_quotient_component_count": component_count_by_key[key_id],
            "accepted_whole_box_face_count": accepted_by_key[key_id],
            "signature_mismatch_face_count": mismatch_by_key[key_id],
            "curved_region_deferred_face_count": deferred_by_key[key_id],
            "occurrence_quotient_assignment_complete": True,
            "all_quotient_components_proved_maximal": False,
            "global_exact_key_fibre_exhausted": False,
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
        }))
    key_rows.sort(key=lambda row: row["official_key_ordinal"])

    census = {
        "boundary_face_candidate_count": 27_288,
        "boundary_face_candidate_count_by_axis": {
            "x": candidate_counts["axis_0_candidate_count"],
            "y": candidate_counts["axis_1_candidate_count"],
            "z": candidate_counts["axis_2_candidate_count"],
        },
        "accepted_whole_box_face_count": 904,
        "accepted_whole_box_face_count_by_axis": {
            "x": candidate_counts["axis_0_accepted_count"],
            "y": candidate_counts["axis_1_accepted_count"],
            "z": candidate_counts["axis_2_accepted_count"],
        },
        "signature_mismatch_face_count": 12_548,
        "curved_region_deferred_face_count": 13_836,
        "accepted_distinct_component_pair_count": 852,
        "rank_reducing_component_pair_count": 468,
        "redundant_certified_component_pair_count": 384,
        "post_Round257_unified_quotient_component_count": 74_012,
        "post_Round258_unified_quotient_component_count": 73_544,
        "exact_accepted_face_area_sum": text(area_sum),
        "exact_two_sided_corridor_volume_sum": text(corridor_volume_sum),
        "occurrence_quotient_assignment_count": 53_968,
        "observed_exact_key_count": 116,
        "maximal_physical_component_assignment_count": 0,
        "globally_exhausted_exact_key_fibre_count": 0,
        "global_exact_key_disposition_count": 0,
    }
    return {
        "status": (
            "CERTIFIED_904_STRICT_WHOLE_BOX_BOUNDARY_FACES__"
            "468_RANK_REDUCTIONS__QUOTIENT_74012_TO_73544"
        ),
        "census": census,
        "formal_input_binding": {name: PINS[name] for name in sorted(PINS)},
        "formal_accepted_whole_box_boundary_face_ledger": ledger(
            accepted_rows, "accepted_face_row_id"
        ),
        "formal_rejected_or_deferred_boundary_face_ledger": ledger(
            rejected_rows, "rejected_face_row_id"
        ),
        "formal_Round257_to_Round258_component_map_ledger": ledger(
            map_rows, "Round257_to_Round258_component_map_row_id"
        ),
        "formal_post_Round258_component_commitment_ledger": ledger(
            component_rows, "post_Round258_component_row_id"
        ),
        "formal_post_Round258_occurrence_quotient_frontier_ledger": ledger(
            post_frontier, "post_frontier_row_id"
        ),
        "formal_post_Round258_key_quotient_frontier_ledger": ledger(
            key_rows, "post_Round258_key_frontier_row_id"
        ),
        "scope_contract": {
            "all_27288_same_chart_boundary_box_contacts_are_reconciled": True,
            "all_904_accepted_faces_have_exact_positive_area": True,
            "all_904_accepted_faces_have_strict_two_sided_corridors": True,
            "all_904_accepted_faces_have_equal_closed_ten_field_signatures": True,
            "all_12548_signature_mismatches_have_zero_glue_credit": True,
            "all_13836_curved_region_faces_remain_fail_closed_pending_face_occupancy": True,
            "exact_key_equality_alone_is_never_used_as_glue": True,
            "whole_box_face_saturation_is_not_component_maximality": True,
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
            "materialize exact face occupancy and two-sided corridors for the 13836 "
            "same-signature curved-region face candidates, then audit pinned cross-chart transitions"
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
