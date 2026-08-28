#!/usr/bin/env python3
"""Certify strict corridors for the twelve Round230 remote sheet references."""

from __future__ import annotations

import argparse
import gc
import hashlib
import json
import os
import stat
import sys
import tempfile
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import ctx


HERE = Path(__file__).resolve().parent
OUTPUT = (
    HERE
    / "cm2_round240_source_g_remote_sheet_interface_corridor_incidence_certificate.json"
)
SCHEMA = "cm2.round240.source-g-remote-sheet-interface-corridor-incidence.v1"
PINS = {
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_verifier.py":
        "c7ead7c9cb8b4d7b8680e64bfb7870e5c5f5e39277e7c7d3d08a62b600f5c058",
    "cm2_round179_source_g_residual_tube_arrangement.py":
        "8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab",
    "cm2_round179_source_g_residual_tube_arrangement_rows.json":
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json":
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866",
    "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json":
        "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938",
    "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json":
        "569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974",
    "cm2_round225_source_g_certified_connectivity_rebuild_certificate.json":
        "0d040af30906f22f600820e14867c45115e679e33b6ee6f052c51a914cf7d841",
    "cm2_round229_source_g_global_occurrence_known_block_frontier_certificate.json":
        "c4152f4764ed7fe977046ef728e8257344803433053e06c0ac11ec68b86ff11a",
    "cm2_round230_source_g_resolved_retained_bulk_continuation_certificate.json":
        "88d9d826bd985635d42820c7b66389603ab56a48717531ace525ee2eaf6d3a73",
    "cm2_round233_source_g_outgoing_seam_parametric_graph_key_partition_certificate.json":
        "cb2f74daa9836841ce311d8d555c2d94ba897f346a63c1e29551d7f99e8d1a41",
    "cm2_round239_source_g_unaccepted_interface_local_classification_ledger_certificate.json":
        "08d392f43fbc7a8d88c6d70b2c36aed7f8d710aac2f6569cf5910dba240ed9cf",
}
MAXIMUM_BYTES = {
    name: (
        5_000_000
        if name.endswith(".py") or "manifest" in name
        else 400_000_000
    )
    for name in PINS
}
SIGNATURE_FIELDS = (
    "source_chart",
    "target_lift",
    "ordered_integer_wall_events",
    "signed_wall_word",
    "roof",
    "outgoing_cell",
    "target_chart",
    "official_key_row",
    "official_key_ordinal",
    "official_key_id",
)
STRICT_SIGNS = {"STRICT_NEGATIVE", "STRICT_POSITIVE"}


def need(value: bool, label: str) -> None:
    if not value:
        raise RuntimeError(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def qstr(value: Q) -> str:
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def read_pinned(name: str) -> bytes:
    path = HERE / name
    info = path.lstat()
    need(
        stat.S_ISREG(info.st_mode)
        and not path.is_symlink()
        and info.st_nlink == 1
        and 0 < info.st_size <= MAXIMUM_BYTES[name],
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


def unpack_selected(
    document: dict[str, Any],
    table_name: str,
    id_field: str,
    selected_ids: set[str],
) -> dict[str, dict[str, Any]]:
    columns = document["row_column_schemas"][table_name]
    index = columns.index(id_field)
    return {
        packed[index]: dict(zip(columns, packed, strict=True))
        for packed in document[table_name]
        if packed[index] in selected_ids
    }


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


def zero_credits() -> dict[str, int]:
    return {
        "known_block_membership_assignment_credit": 0,
        "physical_component_credit": 0,
        "maximal_physical_component_credit": 0,
        "global_exact_key_disposition_credit": 0,
    }


def resolved_signature(row: dict[str, Any]) -> dict[str, Any]:
    return {
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


def computed_signature(
    data: dict[str, Any],
    chart: str,
    owner_target: str,
) -> dict[str, Any]:
    return {
        "source_chart": chart,
        "target_lift": owner_target,
        "ordered_integer_wall_events": data["events"],
        "signed_wall_word": list(data["pattern"]),
        "roof": data["roof"],
        "outgoing_cell": data["outgoing"],
        "target_chart": data["target_chart"],
        "official_key_row": data["key"]["row"],
        "official_key_ordinal": data["key"]["ordinal"],
        "official_key_id": data["key"]["identifier"],
    }


def volume(box: list[Q]) -> Q:
    return (
        (box[1] - box[0])
        * (box[3] - box[2])
        * (box[5] - box[4])
    )


def intersection_volume(left: list[Q], right: list[Q]) -> tuple[list[Q], Q]:
    result: list[Q] = []
    for index in range(3):
        lower = max(left[2 * index], right[2 * index])
        upper = min(left[2 * index + 1], right[2 * index + 1])
        need(lower < upper, "strict three-dimensional intersection")
        result.extend((lower, upper))
    return result, volume(result)


def exact_positive_area_face(
    left_values: list[str],
    right: list[Q],
) -> dict[str, Any]:
    left = [Q(value) for value in left_values]
    touching: list[tuple[int, str, str]] = []
    intersection: list[Q] = []
    for index in range(3):
        left_lower, left_upper = left[2 * index:2 * index + 2]
        right_lower, right_upper = right[2 * index:2 * index + 2]
        lower = max(left_lower, right_lower)
        upper = min(left_upper, right_upper)
        need(lower <= upper, "nonempty face intersection")
        if lower == upper:
            if left_upper == right_lower:
                touching.append((index, "UPPER", "LOWER"))
            elif right_upper == left_lower:
                touching.append((index, "LOWER", "UPPER"))
            else:
                raise RuntimeError("non-boundary zero-width intersection")
        intersection.extend((lower, upper))
    need(len(touching) == 1, "one touching axis")
    axis_index, resolved_side, retained_side = touching[0]
    lengths = [
        intersection[2 * index + 1] - intersection[2 * index]
        for index in range(3)
    ]
    positive = [length for length in lengths if length > 0]
    need(len(positive) == 2, "positive two-dimensional face")
    return {
        "axis": "tps"[axis_index],
        "resolved_side": resolved_side,
        "retained_side": retained_side,
        "fixed_coordinate": qstr(intersection[2 * axis_index]),
        "intersection_box": [qstr(value) for value in intersection],
        "exact_positive_area": qstr(positive[0] * positive[1]),
    }


def safe_write(data: bytes) -> None:
    descriptor, name = tempfile.mkstemp(
        prefix=".round240.",
        suffix=".tmp",
        dir=HERE,
    )
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, OUTPUT)
    finally:
        if temporary.exists():
            temporary.unlink()


def build() -> dict[str, Any]:
    for name in PINS:
        read_pinned(name)

    round230 = load_result(
        "cm2_round230_source_g_resolved_retained_bulk_continuation_certificate.json"
    )
    remote_rows = [
        row
        for row in round230[
            "formal_rejected_local_bulk_candidate_ledger"
        ]["rows"]
        if row["reject_classification"]
        == "FULL_SIGNATURE_REMOTE_WITHOUT_EXACT_POSITIVE_AREA_FACE_OVERLAP"
    ]
    need(
        len(remote_rows) == 12
        and len({
            row["Round220_split_interface_id"] for row in remote_rows
        }) == 12,
        "Round230 remote frontier",
    )
    interface_ids = {
        row["Round220_split_interface_id"] for row in remote_rows
    }
    region_ids = {row["Round208_region_row_id"] for row in remote_rows}
    resolved_ids = {row["resolved_child_row_id"] for row in remote_rows}
    retained_ids = {row["retained_child_row_id"] for row in remote_rows}
    sheet_ids = {row["Round211_sheet_row_id"] for row in remote_rows}
    block_ids = {row["Round225_known_block_id"] for row in remote_rows}
    need(
        None not in sheet_ids
        and None not in block_ids
        and len(resolved_ids) == len(retained_ids) == len(sheet_ids)
        == len(block_ids) == 12,
        "unique remote lineage",
    )

    round239 = load_result(
        "cm2_round239_source_g_unaccepted_interface_local_classification_ledger_certificate.json"
    )
    classification_rows = {
        row["Round220_split_interface_id"]: row
        for row in round239["classification_ledger_rows"]
    }
    need(
        len(classification_rows) == 8_512
        and all(
            classification_rows[interface_id]["classification_type"]
            == "OUTGOING_SEAM_GRAPH_SHARED_KEY"
            for interface_id in interface_ids
        ),
        "Round239 remote classification",
    )

    round233 = load_result(
        "cm2_round233_source_g_outgoing_seam_parametric_graph_key_partition_certificate.json"
    )
    graph_rows = {
        row["Round220_split_interface_id"]: row
        for row in round233["parametric_graph_key_partition_rows"]
        if row["Round220_split_interface_id"] in interface_ids
    }
    need(
        len(graph_rows) == 12
        and all(
            row["retained_root_exact_key_constant_off_seam"]
            and row["known_block_incidence_credit"] == 0
            for row in graph_rows.values()
        ),
        "Round233 remote graph rows",
    )
    del round233
    gc.collect()

    round229 = load_result(
        "cm2_round229_source_g_global_occurrence_known_block_frontier_certificate.json"
    )
    occurrence_frontier = {
        row["local_occurrence_row_id"]: row
        for row in round229[
            "formal_occurrence_known_block_attachment_frontier_ledger"
        ]["rows"]
        if row["local_occurrence_row_id"] in resolved_ids
    }
    lineage_rows = {
        row["Round220_split_interface_id"]: row
        for row in round229[
            "formal_Round220_resolved_retained_coordinate_lineage_frontier_ledger"
        ]["rows"]
    }
    need(
        len(occurrence_frontier) == 12
        and all(
            row["known_block_incidence_attachment_credit"] == 0
            and row["Round225_known_connectivity_block_id"] is None
            for row in occurrence_frontier.values()
        ),
        "Round229 unresolved occurrence frontier",
    )
    no_block_reference_ids = sorted(
        interface_id
        for interface_id in classification_rows
        if lineage_rows[interface_id]["Round225_referenced_known_block_count"]
        == 0
    )
    direct_reference_ids = sorted(
        interface_id
        for interface_id in classification_rows
        if lineage_rows[interface_id]["Round225_referenced_known_block_count"]
        > 0
    )
    need(
        len(no_block_reference_ids) == 8_500
        and set(direct_reference_ids) == interface_ids,
        "Round239/Round229 P2 split",
    )
    del round229, lineage_rows
    gc.collect()

    round225 = load_result(
        "cm2_round225_source_g_certified_connectivity_rebuild_certificate.json"
    )
    sheet_to_block = {
        row["Round211_sheet_row_id"]: row["known_connectivity_block_id"]
        for row in round225["formal_Round211_sheet_assignment_ledger"]["rows"]
        if row["Round211_sheet_row_id"] in sheet_ids
    }
    known_blocks = {
        row["known_connectivity_block_id"]: row
        for row in round225[
            "formal_certified_known_connectivity_block_ledger"
        ]["rows"]
        if row["known_connectivity_block_id"] in block_ids
    }
    need(
        len(sheet_to_block) == len(known_blocks) == 12
        and all(
            row["certified_known_connectivity"]
            and not row["maximal_physical_component_claimed"]
            for row in known_blocks.values()
        ),
        "Round225 direct sheet block seeds",
    )
    del round225
    gc.collect()

    round220 = load_result(
        "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json"
    )
    interface_table = round220[
        "coordinate_boundary_atlas"
    ]["tables"]["one_step_split_interface_rows"]
    interface_columns = interface_table["columns"]
    interface_index = interface_columns.index("split_interface_id")
    interfaces = {
        packed[interface_index]:
            dict(zip(interface_columns, packed, strict=True))
        for packed in interface_table["rows"]
        if packed[interface_index] in interface_ids
    }
    need(
        len(interfaces) == 12
        and all(
            row["axis"] == "s"
            and {
                row["lower_child_kind"],
                row["upper_child_kind"],
            } == {"RESOLVED", "RETAINED"}
            for row in interfaces.values()
        ),
        "Round220 remote interfaces",
    )
    del round220
    gc.collect()

    round179 = load_result(
        "cm2_round179_source_g_residual_tube_arrangement_rows.json"
    )
    retained_rows = unpack_selected(
        round179,
        "retained_3d_child_rows",
        "row_id",
        retained_ids,
    )
    resolved_rows = unpack_selected(
        round179,
        "resolved_3d_child_rows",
        "row_id",
        resolved_ids,
    )
    origin_ids = {
        row["origin_row_id"] for row in retained_rows.values()
    }
    origin_rows = unpack_selected(
        round179,
        "origin_tube_rows",
        "origin_row_id",
        origin_ids,
    )
    need(
        len(retained_rows) == len(resolved_rows) == len(origin_rows) == 12,
        "Round179 remote rows",
    )
    del round179
    gc.collect()

    round208 = load_result(
        "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json"
    )
    retained_regions = {
        row["region_row_id"]: row
        for row in round208["formal_local_open_3D_signature_ledger"]["rows"]
        if row["region_row_id"] in region_ids
    }
    need(
        len(retained_regions) == 12
        and all(
            row["leaf_classification"] == "CLIPPED_2D_BOUNDARY_1D"
            and row["F_sign"] in STRICT_SIGNS
            and row["HPLUS_sign"] in STRICT_SIGNS
            and row["HMINUS_sign"] in STRICT_SIGNS
            for row in retained_regions.values()
        ),
        "Round208 remote regions",
    )
    del round208
    gc.collect()

    sys.path.insert(0, str(HERE))
    import cm2_round179_source_g_residual_tube_arrangement as r179

    need(
        Path(r179.__file__).resolve()
        == (HERE / "cm2_round179_source_g_residual_tube_arrangement.py").resolve(),
        "Round179 module identity",
    )
    registry = r179.r174.rebuild_registry(
        r179.strict_load(
            HERE
            / "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json",
            5_000_000,
        )
    )
    ctx.prec = 256

    corridor_rows: list[dict[str, Any]] = []
    incidence_rows: list[dict[str, Any]] = []
    factor_profiles: Counter[tuple[str, str, str]] = Counter()
    for remote in sorted(
        remote_rows,
        key=lambda row: row["Round220_split_interface_id"],
    ):
        interface_id = remote["Round220_split_interface_id"]
        interface = interfaces[interface_id]
        retained = retained_rows[remote["retained_child_row_id"]]
        resolved = resolved_rows[remote["resolved_child_row_id"]]
        origin = origin_rows[retained["origin_row_id"]]
        region = retained_regions[remote["Round208_region_row_id"]]
        graph = graph_rows[interface_id]
        classification = classification_rows[interface_id]
        frontier = occurrence_frontier[resolved["row_id"]]
        sheet_id = remote["Round211_sheet_row_id"]
        block_id = remote["Round225_known_block_id"]
        signature = resolved_signature(resolved)
        need(
            region["local_return_signature"] == signature
            and set(signature) == set(SIGNATURE_FIELDS)
            and classification["candidate_exact_key_ids"]
            == [signature["official_key_id"]]
            and classification["candidate_exact_key_ordinals"]
            == [signature["official_key_ordinal"]]
            and graph["shared_official_key_id"]
            == signature["official_key_id"]
            and graph["shared_official_key_ordinal"]
            == signature["official_key_ordinal"]
            and frontier["official_key_id"] == signature["official_key_id"]
            and frontier["official_key_ordinal"]
            == signature["official_key_ordinal"]
            and sheet_to_block[sheet_id] == block_id,
            f"exact lineage:{interface_id}",
        )
        need(
            retained["origin_row_id"] == origin["origin_row_id"]
            and resolved["origin_row_id"] == origin["origin_row_id"]
            and retained["chart"] == resolved["chart"] == origin["chart"]
            and origin["original_reason_labels"] == ["outgoing_chart_seam"],
            f"Round179 sibling binding:{interface_id}",
        )
        lower_id = interface["lower_child_row_id"]
        upper_id = interface["upper_child_row_id"]
        need(
            {lower_id, upper_id} == {retained["row_id"], resolved["row_id"]}
            and interface["event_trace_materialized_on_interface"] is False,
            f"Round220 sibling binding:{interface_id}",
        )

        root_box = [Q(value) for value in retained["box"]]
        leaf_box = [Q(value) for value in region["Round182_leaf_box"]]
        fixed = Q(interface["fixed_coordinate"])
        need(
            root_box[0] <= leaf_box[0] < leaf_box[1] <= root_box[1]
            and root_box[2] <= leaf_box[2] < leaf_box[3] <= root_box[3]
            and root_box[4] <= leaf_box[4] < leaf_box[5] <= root_box[5]
            and fixed in {root_box[4], root_box[5]},
            f"box nesting:{interface_id}",
        )

        root = r179.box_from(
            retained["box"],
            len(retained["refinement_path"]),
            retained["row_id"],
        )
        root_geometry = r179.interval_geometry(
            retained["chart"],
            origin["owner_target"],
            root,
        )
        derivative_sign = r179.sign(
            root_geometry["outgoing_equality"][1][0]
        )
        need(derivative_sign in STRICT_SIGNS, f"strict derivative:{interface_id}")
        x_dominant = signature["outgoing_cell"] in {"E", "W"}
        upper_t_lane = x_dominant == (
            derivative_sign == "STRICT_POSITIVE"
        )
        lane_width = (root_box[1] - root_box[0]) / 4
        if upper_t_lane:
            lane_t0 = root_box[1] - lane_width
            lane_t1 = root_box[1]
        else:
            lane_t0 = root_box[0]
            lane_t1 = root_box[0] + lane_width
        lane_box = [
            lane_t0,
            lane_t1,
            leaf_box[2],
            leaf_box[3],
            min(leaf_box[4], fixed),
            max(leaf_box[5], fixed),
        ]
        need(volume(lane_box) > 0, f"positive corridor:{interface_id}")

        lane = r179.r174.atlas.AtlasBox(
            *lane_box,
            len(retained["refinement_path"]) + 2,
            f"round240-corridor:{interface_id}",
        )
        computed, reasons = r179.r174.certify_signature(
            retained["chart"],
            lane,
            origin["owner_target"],
            registry,
        )
        need(
            computed is not None
            and reasons == []
            and computed_signature(
                computed,
                retained["chart"],
                origin["owner_target"],
            ) == signature,
            f"strict corridor signature:{interface_id}",
        )
        geometry = r179.interval_geometry(
            retained["chart"],
            origin["owner_target"],
            lane,
        )
        factor_signs = {
            "F": r179.sign(geometry["outgoing_equality"][0]),
            "HPLUS": r179.sign(
                r179.dual_add(
                    geometry["outgoing_x"],
                    geometry["outgoing_y"],
                )[0]
            ),
            "HMINUS": r179.sign(
                r179.dual_sub(
                    geometry["outgoing_x"],
                    geometry["outgoing_y"],
                )[0]
            ),
        }
        need(
            set(factor_signs.values()) <= STRICT_SIGNS
            and factor_signs["F"] == region["F_sign"]
            and factor_signs["HPLUS"] == region["HPLUS_sign"]
            and factor_signs["HMINUS"] == region["HMINUS_sign"],
            f"strict factor-region inclusion:{interface_id}",
        )
        factor_profiles[(
            factor_signs["F"],
            factor_signs["HPLUS"],
            factor_signs["HMINUS"],
        )] += 1

        overlap_box, overlap_volume = intersection_volume(
            lane_box,
            leaf_box,
        )
        face = exact_positive_area_face(
            resolved["box"],
            lane_box,
        )
        need(
            overlap_volume > 0
            and face["axis"] == interface["axis"] == "s"
            and face["fixed_coordinate"] == interface["fixed_coordinate"],
            f"corridor contacts:{interface_id}",
        )
        tangential = [Q(value) for value in interface["tangential_half_open_box"]]
        face_box = [Q(value) for value in face["intersection_box"]]
        need(
            tangential[0] <= face_box[0] < face_box[1] <= tangential[1]
            and tangential[2] <= face_box[2] < face_box[3] <= tangential[3]
            and face_box[4] == face_box[5] == fixed,
            f"interface patch containment:{interface_id}",
        )

        corridor_id = (
            "round240-strict-sheet-interface-corridor:"
            + digest([
                interface_id,
                region["region_row_id"],
                [qstr(value) for value in lane_box],
            ])
        )
        corridor_rows.append(closed({
            "strict_corridor_row_id": corridor_id,
            "Round220_split_interface_id": interface_id,
            "Round230_remote_reject_row_id": remote["reject_row_id"],
            "Round233_graph_partition_row_id":
                graph["parametric_graph_partition_row_id"],
            "Round239_classification_ledger_row_id":
                classification["classification_ledger_row_id"],
            "resolved_child_row_id": resolved["row_id"],
            "retained_child_row_id": retained["row_id"],
            "Round208_region_row_id": region["region_row_id"],
            "Round208_leaf_row_id": region["leaf_row_id"],
            "Round211_sheet_row_id": sheet_id,
            "Round225_known_connectivity_block_id": block_id,
            "axis": "s",
            "fixed_coordinate": interface["fixed_coordinate"],
            "t_lane_dyadic_depth": 2,
            "t_lane_uses_upper_quarter": upper_t_lane,
            "strict_t_derivative_sign": derivative_sign,
            "strict_corridor_box": [qstr(value) for value in lane_box],
            "strict_corridor_exact_coordinate_volume":
                qstr(volume(lane_box)),
            "Round208_region_positive_volume_overlap_box":
                [qstr(value) for value in overlap_box],
            "Round208_region_positive_volume_overlap":
                qstr(overlap_volume),
            "resolved_interface_patch": face["intersection_box"],
            "resolved_interface_patch_exact_positive_area":
                face["exact_positive_area"],
            "resolved_side": face["resolved_side"],
            "retained_side": face["retained_side"],
            "strict_F_sign": factor_signs["F"],
            "strict_HPLUS_sign": factor_signs["HPLUS"],
            "strict_HMINUS_sign": factor_signs["HMINUS"],
            "Round208_factor_signs_exactly_equal_on_corridor": True,
            "all_10_return_signature_fields_exactly_equal": True,
            "return_signature_sha256": digest(signature),
            "direct_Round211_sheet_seeded_known_block": True,
            "known_block_incidence_bridge_credit": 1,
            "whole_interface_certified": False,
            **zero_credits(),
        }))
        incidence_rows.append(closed({
            "incidence_delta_row_id":
                "round240-known-block-incidence-delta:"
                + digest([resolved["row_id"], block_id, corridor_id]),
            "local_occurrence_row_id": resolved["row_id"],
            "local_occurrence_gauge": "ROUND179_RESOLVED_CHILD",
            "official_key_ordinal": signature["official_key_ordinal"],
            "official_key_id": signature["official_key_id"],
            "Round225_known_connectivity_block_id": block_id,
            "strict_corridor_row_id": corridor_id,
            "derivation": (
                "STRICT_3D_CORRIDOR_FROM_ROUND211_SHEET_SEED_TO_"
                "EXACT_POSITIVE_AREA_RESOLVED_INTERFACE_PATCH"
            ),
            "known_block_incidence_attachment_credit": 1,
            **zero_credits(),
        }))

    corridor_rows.sort(key=lambda row: row["strict_corridor_row_id"])
    incidence_rows.sort(key=lambda row: row["incidence_delta_row_id"])
    need(
        len(corridor_rows) == len(incidence_rows) == 12
        and len({
            row["local_occurrence_row_id"] for row in incidence_rows
        }) == 12,
        "Round240 exact delta",
    )
    previous_delta_ids = {
        row["local_occurrence_row_id"]
        for row in round230[
            "formal_occurrence_known_block_incidence_delta_ledger"
        ]["rows"]
    }
    need(
        not (
            previous_delta_ids
            & {
                row["local_occurrence_row_id"] for row in incidence_rows
            }
        ),
        "Round230/Round240 incidence disjointness",
    )
    pre_round230 = 35_432
    round230_delta = round230["census"][
        "derived_occurrence_known_block_incidence_delta_count"
    ]
    need(
        round230_delta == 464
        and round230["census"][
            "post_bridge_occurrences_with_known_block_incidence"
        ] == pre_round230 + round230_delta == 35_896,
        "pre-Round240 incidence account",
    )
    post_incidence = pre_round230 + round230_delta + len(incidence_rows)
    total_occurrences = 53_968
    remaining = total_occurrences - post_incidence
    remaining_rows = [
        classification_rows[interface_id]
        for interface_id in no_block_reference_ids
    ]
    remaining_type_histogram = Counter(
        row["classification_type"] for row in remaining_rows
    )
    remaining_key_count_histogram = Counter(
        len(row["candidate_exact_key_ids"]) for row in remaining_rows
    )

    return {
        "status": (
            "CERTIFIED_12_REMOTE_SHEET_TO_INTERFACE_STRICT_CORRIDORS__"
            "12_NEW_KNOWN_BLOCK_INCIDENCES__8500_INTERFACES_REQUIRE_"
            "NEW_EVENT_COMMON_REFINEMENT_MATERIALIZATION"
        ),
        "census": {
            "Round230_remote_exact_signature_reference_count": 12,
            "strict_depth2_corridor_count": len(corridor_rows),
            "positive_3D_Round208_region_overlap_count": len(corridor_rows),
            "positive_2D_resolved_interface_patch_count": len(corridor_rows),
            "direct_Round211_sheet_seeded_block_count": len(block_ids),
            "distinct_exact_key_count": len({
                row["official_key_ordinal"] for row in incidence_rows
            }),
            "new_occurrence_known_block_incidence_count":
                len(incidence_rows),
            "pre_Round240_occurrences_with_known_block_incidence": 35_896,
            "post_Round240_occurrences_with_known_block_incidence":
                post_incidence,
            "post_Round240_occurrences_without_known_block_incidence":
                remaining,
            "local_occurrence_count": total_occurrences,
            "remaining_Round239_interface_without_Round225_block_reference_count":
                len(no_block_reference_ids),
            "remaining_classification_type_histogram":
                dict(sorted(remaining_type_histogram.items())),
            "remaining_candidate_key_count_histogram": {
                str(key): value
                for key, value in sorted(
                    remaining_key_count_histogram.items()
                )
            },
            "strict_factor_profile_histogram": {
                "|".join(profile): count
                for profile, count in sorted(factor_profiles.items())
            },
        },
        "formal_strict_sheet_interface_corridor_ledger":
            ledger(corridor_rows, "strict_corridor_row_id"),
        "formal_occurrence_known_block_incidence_delta_ledger":
            ledger(incidence_rows, "incidence_delta_row_id"),
        "remaining_no_block_reference_interface_ids_sha256":
            digest(no_block_reference_ids),
        "scope_contract": {
            "every_promoted_occurrence_was_unattached_before_Round240": True,
            "every_corridor_has_positive_3D_overlap_with_its_direct_sheet_seed_region":
                True,
            "every_corridor_has_positive_2D_overlap_with_its_resolved_sibling":
                True,
            "every_corridor_recomputes_the_same_strict_10_field_return_signature":
                True,
            "exact_key_equality_alone_was_not_used_as_physical_glue": True,
            "remaining_8500_interfaces_need_new_event_or_common_refinement_materialization":
                True,
        },
        "strict_nonpromotion": {
            "known_block_membership_assignment_credit": 0,
            "physical_component_credit": 0,
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
            "Gate5": "10/18",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": (
            "materialize the first missing retained event/common-refinement "
            "strata for the 8500 Round239 interfaces with no Round225 block "
            "reference; do not attach by exact-key equality"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()
    result = build()
    document = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    data = canonical(document) + b"\n"
    if not arguments.no_write:
        safe_write(data)
    print(result["status"])
    print(json.dumps(result["census"], sort_keys=True))
    print(f"result_sha256={document['result_sha256']}")
    print(f"certificate_sha256={hashlib.sha256(data).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
