#!/usr/bin/env python3
"""Attach crossing-time and source-chart-seam retained roots."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
import gc
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile
from typing import Any


HERE = Path(__file__).resolve().parent
OUTPUT = (
    HERE
    / "cm2_round247_source_g_crossing_and_source_seam_retained_quotient_certificate.json"
)
SCHEMA = (
    "cm2.round247.source-g-crossing-and-source-seam-retained-quotient.v1"
)
PINS = {
    "cm2_round179_source_g_residual_tube_arrangement_rows.json":
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json":
        "569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974",
    "cm2_round237_source_g_crossing_time_whole_origin_promotion_certificate.json":
        "5fa46f8c6d8074770ebbf8cbdb2f0590dbdf5710254d05c6a0a3aca0953359f3",
    "cm2_round238_source_g_source_chart_seam_whole_origin_promotion_certificate.json":
        "8200ba9c35ba32c938eb66beb7a4040908db9b81fc449881a55b09e67b517446",
    "cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json":
        "5b08d568cccd302ac2dd62e7e9b6573ce83e015181ead168812159c9f882712f",
    "cm2_round246_source_g_whole_signature_retained_quotient_certificate.json":
        "a448359c0a9b4495e54afe6e2d860c20fb222684bae46ee108574782a5a33bc9",
}


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
        and 0 < info.st_size <= 400_000_000,
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
    table: str,
    id_field: str,
    selected: set[str],
) -> dict[str, dict[str, Any]]:
    columns = document["row_column_schemas"][table]
    index = columns.index(id_field)
    return {
        packed[index]: dict(zip(columns, packed, strict=True))
        for packed in document[table]
        if packed[index] in selected
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


def box_values(box: list[str]) -> list[Q]:
    values = [Q(value) for value in box]
    need(
        len(values) == 6
        and values[0] < values[1]
        and values[2] < values[3]
        and values[4] < values[5],
        "positive box",
    )
    return values


def volume(box: list[Q]) -> Q:
    return (
        (box[1] - box[0])
        * (box[3] - box[2])
        * (box[5] - box[4])
    )


def tangential_rectangle(box: list[Q], axis: str) -> list[Q]:
    index = {"t": 0, "p": 1, "s": 2}[axis]
    keep = [item for item in range(3) if item != index]
    return [
        box[2 * keep[0]],
        box[2 * keep[0] + 1],
        box[2 * keep[1]],
        box[2 * keep[1] + 1],
    ]


def area(rectangle: list[Q]) -> Q:
    need(
        rectangle[0] < rectangle[1]
        and rectangle[2] < rectangle[3],
        "positive rectangle",
    )
    return (
        (rectangle[1] - rectangle[0])
        * (rectangle[3] - rectangle[2])
    )


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


def source_seam_physical_corridor(
    box: list[Q],
    interface: dict[str, Any],
) -> tuple[list[Q], int]:
    need(interface["axis"] == "t", "source seam t interface")
    lower_value = 2 * box[0] * box[0] - 1
    upper_value = 2 * box[1] * box[1] - 1
    need(lower_value * upper_value < 0, "source seam endpoint opposition")
    physical_lower = lower_value < 0
    physical_endpoint = box[0] if physical_lower else box[1]
    need(
        Q(interface["fixed_coordinate"]) == physical_endpoint,
        "source seam interface enters physical side",
    )
    for depth in (1, 2):
        width = (box[1] - box[0]) / (2 ** depth)
        t0, t1 = (
            (box[0], box[0] + width)
            if physical_lower
            else (box[1] - width, box[1])
        )
        if 2 * t0 * t0 - 1 < 0 and 2 * t1 * t1 - 1 < 0:
            corridor = [t0, t1, box[2], box[3], box[4], box[5]]
            return corridor, depth
    raise RuntimeError("source seam dyadic physical corridor")


def build() -> dict[str, Any]:
    for name in PINS:
        read_pinned(name)

    round237 = load_result(
        "cm2_round237_source_g_crossing_time_whole_origin_promotion_certificate.json"
    )
    round238 = load_result(
        "cm2_round238_source_g_source_chart_seam_whole_origin_promotion_certificate.json"
    )
    roots: list[tuple[str, dict[str, Any]]] = [
        ("CROSSING_TIME", row)
        for row in round237["whole_origin_promotion_rows"]
    ] + [
        ("SOURCE_CHART_SEAM", row)
        for row in round238["whole_origin_promotion_rows"]
    ]
    interface_ids = {row["Round220_split_interface_id"] for _, row in roots}
    retained_ids = {row["Round179_retained_child_row_id"] for _, row in roots}
    resolved_ids = {row["Round179_resolved_sibling_row_id"] for _, row in roots}
    need(
        len(round237["whole_origin_promotion_rows"]) == 240
        and len(round238["whole_origin_promotion_rows"]) == 264
        and len(roots) == len(interface_ids) == len(retained_ids)
        == len(resolved_ids) == 504,
        "Round237/Round238 census",
    )

    round220 = load_result(
        "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json"
    )
    table = round220["coordinate_boundary_atlas"]["tables"][
        "one_step_split_interface_rows"
    ]
    columns = table["columns"]
    index = columns.index("split_interface_id")
    interfaces = {
        packed[index]: dict(zip(columns, packed, strict=True))
        for packed in table["rows"]
        if packed[index] in interface_ids
    }
    need(len(interfaces) == 504, "Round220 selected interfaces")
    del round220
    gc.collect()

    round179 = load_result(
        "cm2_round179_source_g_residual_tube_arrangement_rows.json"
    )
    retained = unpack_selected(
        round179, "retained_3d_child_rows", "row_id", retained_ids
    )
    resolved = unpack_selected(
        round179, "resolved_3d_child_rows", "row_id", resolved_ids
    )
    need(len(retained) == len(resolved) == 504, "Round179 selected rows")
    del round179
    gc.collect()

    round244 = load_result(
        "cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json"
    )
    old_component_by_id = {
        row["resolved_bulk_component_row_id"]: row
        for row in round244["formal_resolved_bulk_component_ledger"]["rows"]
    }
    component_by_child = {
        child_id: component_id
        for component_id, component in old_component_by_id.items()
        for child_id in component["member_Round179_resolved_child_row_ids"]
    }
    need(
        len(old_component_by_id) == 8_148
        and len(component_by_child) == 17_192,
        "Round244 component partition",
    )
    del round244
    gc.collect()

    round246 = load_result(
        "cm2_round246_source_g_whole_signature_retained_quotient_certificate.json"
    )
    prior_components = {
        row["inherited_Round244_resolved_bulk_component_id"]: row
        for row in round246[
            "formal_post_Round246_mixed_sheet_component_ledger"
        ]["rows"]
    }
    occurrence_commitment = round246["unchanged_occurrence_frontier_commitment"]
    key_commitment = round246["unchanged_key_frontier_commitment"]
    need(
        len(prior_components) == 8_148
        and round246["census"]["remaining_Round239_interface_count"] == 3_144
        and round246["census"]["cumulative_virtual_retained_stratum_node_count"]
        == 5_884,
        "Round246 quotient binding",
    )

    node_rows: list[dict[str, Any]] = []
    edge_rows: list[dict[str, Any]] = []
    nodes_by_component: dict[str, list[str]] = defaultdict(list)
    edges_by_component: dict[str, list[str]] = defaultdict(list)
    roots_by_component: Counter[str] = Counter()
    kind_histogram: Counter[str] = Counter()
    seam_depth_histogram: Counter[int] = Counter()
    seam_owner_histogram: Counter[str] = Counter()
    chart_histogram: Counter[str] = Counter()
    physical_volume_by_kind: Counter[str] = Counter()

    for kind, root in sorted(
        roots,
        key=lambda item: item[1]["whole_origin_promotion_row_id"],
    ):
        interface_id = root["Round220_split_interface_id"]
        interface = interfaces[interface_id]
        retained_row = retained[root["Round179_retained_child_row_id"]]
        resolved_row = resolved[root["Round179_resolved_sibling_row_id"]]
        signature = resolved_signature(resolved_row)
        box = box_values(retained_row["box"])
        component_id = component_by_child[resolved_row["row_id"]]
        seed_blocks = old_component_by_id[component_id][
            "seed_Round243_known_connectivity_block_ids"
        ]
        need(
            retained_row["origin_row_id"] == resolved_row["origin_row_id"]
            == root["origin_row_id"]
            and retained_row["parent_id"] == resolved_row["parent_id"]
            and retained_row["chart"] == resolved_row["chart"]
            and {interface["lower_child_row_id"], interface["upper_child_row_id"]}
            == {retained_row["row_id"], resolved_row["row_id"]}
            and interface["event_trace_materialized_on_interface"] is False,
            f"lineage:{interface_id}",
        )
        if kind == "CROSSING_TIME":
            need(
                root["whole_origin_local_return_signature"] == signature
                and root["whole_origin_local_return_signature_credit"] == 1
                and root[
                    "exact_endpoint_opposition_proves_crossing_time_in_open_unit_interval"
                ] is True
                and interface["axis"] == "t",
                f"crossing signature:{interface_id}",
            )
            corridor = box
            stratum_kind = "CROSSING_TIME_WHOLE_SIGNATURE_RETAINED_BULK"
            proof_kind = "ROUND237_WHOLE_ROOT_EXACT_INTERFACE_FACE"
            source_row_id = root["whole_origin_promotion_row_id"]
        else:
            need(
                root[
                    "whole_box_signature_recomputation_ignoring_chart_class_precheck"
                ] == signature
                and root["whole_origin_local_return_signature_credit"] == 1
                and root["seam_equation"] == "2*t^2-1=0"
                and root["seam_three_dimensional_coordinate_volume"] == 0,
                f"source seam signature:{interface_id}",
            )
            corridor, depth = source_seam_physical_corridor(box, interface)
            seam_depth_histogram[depth] += 1
            seam_owner_histogram[root["half_open_seam_owner_status"]] += 1
            stratum_kind = "SOURCE_CHART_SEAM_PHYSICAL_SIDE_RETAINED_BULK"
            proof_kind = "ROUND238_EXACT_PHYSICAL_SIDE_DYADIC_CORRIDOR"
            source_row_id = root["whole_origin_promotion_row_id"]
        contact = tangential_rectangle(corridor, "t")
        node_id = "round247-retained-stratum:" + digest([
            kind,
            interface_id,
            retained_row["row_id"],
            signature,
            [qstr(value) for value in corridor],
        ])
        edge_id = "round247-resolved-retained-edge:" + digest([
            kind,
            interface_id,
            resolved_row["row_id"],
            node_id,
            [qstr(value) for value in contact],
        ])
        node_rows.append(closed({
            "retained_stratum_node_id": node_id,
            "source_classification": kind,
            "source_whole_origin_promotion_row_id": source_row_id,
            "Round220_split_interface_id": interface_id,
            "Round179_retained_child_row_id": retained_row["row_id"],
            "inherited_Round244_resolved_bulk_component_id": component_id,
            "stratum_kind": stratum_kind,
            "local_dimension": 3,
            "local_return_signature": signature,
            "official_key_ordinal": signature["official_key_ordinal"],
            "official_key_id": signature["official_key_id"],
            "strict_positive_3D_physical_witness_box":
                [qstr(value) for value in corridor],
            "strict_positive_3D_physical_witness_volume":
                qstr(volume(corridor)),
            "seed_known_connectivity_block_ids": seed_blocks,
            "virtual_stratum_known_block_incidence_credit":
                1 if seed_blocks else 0,
            "occurrence_known_block_incidence_credit": 0,
            "physical_component_credit": 0,
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
        }))
        edge_rows.append(closed({
            "mixed_sheet_edge_id": edge_id,
            "source_classification": kind,
            "Round220_split_interface_id": interface_id,
            "inherited_Round244_resolved_bulk_component_id": component_id,
            "resolved_occurrence_node_id": resolved_row["row_id"],
            "retained_stratum_node_id": node_id,
            "edge_kind": "RESOLVED_TO_WHOLE_SIGNATURE_PHYSICAL_RETAINED_BULK",
            "contact_proof_kind": proof_kind,
            "exact_positive_2D_contact_rectangle":
                [qstr(value) for value in contact],
            "exact_positive_2D_contact_area": qstr(area(contact)),
            "strict_positive_3D_retained_corridor_box":
                [qstr(value) for value in corridor],
            "strict_positive_3D_retained_corridor_volume":
                qstr(volume(corridor)),
            "current_quotient_lower_bound_edge_credit": 1,
            "occurrence_known_block_incidence_credit": 0,
            "physical_component_credit": 0,
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
        }))
        nodes_by_component[component_id].append(node_id)
        edges_by_component[component_id].append(edge_id)
        roots_by_component[component_id] += 1
        kind_histogram[kind] += 1
        chart_histogram[retained_row["chart"]] += 1
        physical_volume_by_kind[kind] += volume(corridor)

    node_rows.sort(key=lambda row: row["retained_stratum_node_id"])
    edge_rows.sort(key=lambda row: row["mixed_sheet_edge_id"])
    need(
        len(node_rows) == len(edge_rows) == 504
        and dict(kind_histogram) == {"CROSSING_TIME": 240, "SOURCE_CHART_SEAM": 264}
        and dict(seam_depth_histogram) == {1: 232, 2: 32}
        and dict(seam_owner_histogram) == {
            "E_OR_W_HALF_OPEN_OWNER": 128,
            "N_OR_S_EXCLUDES_DIAGONAL_TIE": 136,
        },
        "Round247 node and edge census",
    )

    component_rows: list[dict[str, Any]] = []
    new_touched = 0
    overlap = 0
    cumulative_touched = 0
    cumulative_seeded_nodes = 0
    cumulative_root_histogram: Counter[int] = Counter()
    for component_id, prior in sorted(prior_components.items()):
        new_nodes = sorted(nodes_by_component.get(component_id, []))
        new_edges = sorted(edges_by_component.get(component_id, []))
        prior_nodes = prior["cumulative_virtual_stratum_node_ids"]
        prior_edges = prior["cumulative_mixed_sheet_edge_ids"]
        cumulative_nodes = sorted(prior_nodes + new_nodes)
        cumulative_edges = sorted(prior_edges + new_edges)
        prior_roots = prior["cumulative_retained_root_count"]
        new_roots = roots_by_component[component_id]
        cumulative_roots = prior_roots + new_roots
        seed_blocks = prior["seed_known_connectivity_block_ids"]
        new_touched += bool(new_roots)
        overlap += bool(new_roots and prior_roots)
        cumulative_touched += bool(cumulative_roots)
        cumulative_seeded_nodes += len(cumulative_nodes) if seed_blocks else 0
        cumulative_root_histogram[cumulative_roots] += 1
        component_rows.append(closed({
            "mixed_sheet_component_row_id":
                "round247-mixed-sheet-component:"
                + digest([component_id, cumulative_nodes]),
            "inherited_Round244_resolved_bulk_component_id": component_id,
            "Round246_cumulative_retained_root_count": prior_roots,
            "new_Round247_retained_root_count": new_roots,
            "cumulative_retained_root_count": cumulative_roots,
            "Round246_cumulative_virtual_stratum_node_count": len(prior_nodes),
            "new_Round247_virtual_stratum_node_count": len(new_nodes),
            "cumulative_virtual_stratum_node_count": len(cumulative_nodes),
            "cumulative_virtual_stratum_node_ids": cumulative_nodes,
            "cumulative_virtual_stratum_node_ids_sha256": digest(cumulative_nodes),
            "Round246_cumulative_mixed_sheet_edge_count": len(prior_edges),
            "new_Round247_mixed_sheet_edge_count": len(new_edges),
            "cumulative_mixed_sheet_edge_count": len(cumulative_edges),
            "cumulative_mixed_sheet_edge_ids": cumulative_edges,
            "cumulative_mixed_sheet_edge_ids_sha256": digest(cumulative_edges),
            "seed_known_connectivity_block_ids": seed_blocks,
            "cumulative_virtual_stratum_known_block_incidence_count":
                len(cumulative_nodes) if seed_blocks else 0,
            "new_occurrence_known_block_incidence_count": 0,
            "certified_known_connectivity_only": True,
            "maximal_physical_component_claimed": False,
            "global_exact_key_fibre_credit": 0,
        }))
    component_rows.sort(key=lambda row: row["mixed_sheet_component_row_id"])
    need(
        len(component_rows) == 8_148
        and new_touched == 304
        and overlap == 0
        and cumulative_touched == 4_280
        and cumulative_seeded_nodes == 316
        and dict(cumulative_root_histogram)
        == {0: 3_868, 1: 2_888, 2: 1_228, 3: 144, 4: 16, 5: 4},
        "Round247 component census",
    )

    census = {
        "crossing_time_retained_interface_count": 240,
        "source_chart_seam_retained_interface_count": 264,
        "new_virtual_retained_stratum_node_count": 504,
        "new_positive_area_physical_edge_count": 504,
        "source_seam_physical_corridor_depth_histogram":
            {str(key): value for key, value in sorted(seam_depth_histogram.items())},
        "source_seam_half_open_owner_status_histogram":
            dict(sorted(seam_owner_histogram.items())),
        "source_chart_histogram": dict(sorted(chart_histogram.items())),
        "crossing_time_exact_physical_volume_sum":
            qstr(physical_volume_by_kind["CROSSING_TIME"]),
        "source_seam_exact_physical_corridor_volume_sum":
            qstr(physical_volume_by_kind["SOURCE_CHART_SEAM"]),
        "new_touched_Round244_component_count": new_touched,
        "Round246_Round247_touched_component_overlap_count": overlap,
        "cumulative_touched_Round244_component_count": cumulative_touched,
        "Round246_cumulative_virtual_stratum_node_count": 5_884,
        "cumulative_virtual_stratum_node_count": 6_388,
        "Round246_cumulative_mixed_sheet_edge_count": 5_884,
        "cumulative_mixed_sheet_edge_count": 6_388,
        "new_virtual_stratum_known_block_incidence_count": 0,
        "cumulative_virtual_stratum_known_block_incidence_count":
            cumulative_seeded_nodes,
        "Round247_mixed_sheet_component_count": 8_148,
        "Round247_mixed_sheet_component_reduction": 0,
        "new_occurrence_known_block_incidence_count": 0,
        "known_connectivity_block_count": 7_388,
        "post_Round247_occurrences_with_known_block_incidence": 36_200,
        "post_Round247_occurrences_without_known_block_incidence": 17_768,
        "remaining_Round239_interface_count": 2_640,
        "maximal_physical_component_assignment_count": 0,
        "global_exact_key_fibre_exhausted_count": 0,
    }
    return {
        "status": (
            "CERTIFIED_504_CROSSING_AND_SOURCE_SEAM_PHYSICAL_CONTACTS__"
            "6388_CUMULATIVE_VIRTUAL_STRATA_AND_EDGES__"
            "ZERO_NEW_OCCURRENCE_INCIDENCE__2640_WALL_INTERFACES_REMAIN"
        ),
        "census": census,
        "formal_input_binding": {name: PINS[name] for name in sorted(PINS)},
        "formal_new_crossing_and_source_seam_retained_stratum_node_ledger":
            ledger(node_rows, "retained_stratum_node_id"),
        "formal_new_crossing_and_source_seam_physical_edge_ledger":
            ledger(edge_rows, "mixed_sheet_edge_id"),
        "formal_post_Round247_mixed_sheet_component_ledger":
            ledger(component_rows, "mixed_sheet_component_row_id"),
        "unchanged_occurrence_frontier_commitment": occurrence_commitment,
        "unchanged_key_frontier_commitment": key_commitment,
        "scope_contract": {
            "all_240_crossing_roots_have_whole_root_equal_sibling_signature": True,
            "all_264_source_seam_roots_have_equal_sibling_signature": True,
            "all_264_source_seam_corridors_are_strictly_inside_2t2_minus_1_negative": True,
            "all_504_interfaces_have_exact_positive_area_physical_contact": True,
            "coordinate_guard_volume_never_receives_physical_credit": True,
            "virtual_retained_stratum_incidence_is_not_occurrence_incidence": True,
        },
        "strict_nonpromotion": {
            "new_occurrence_known_block_incidence_credit": 0,
            "known_block_membership_assignment_credit": 0,
            "physical_component_credit": 0,
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
            "global_exact_key_disposition_credit": 0,
            "Gate5_complete_field_block_count": 0,
            "Gate5_filled_field_slot_count": 10,
            "Gate5_total_field_slot_count": 18,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": (
            "materialize the final 2640 wall finite-key retained partitions, "
            "including every positive-volume endpoint/count-transition branch "
            "and every half-open wall sheet, then rebuild the mixed quotient"
        ),
    }


def safe_write(raw: bytes) -> None:
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{OUTPUT.name}.", dir=OUTPUT.parent
    )
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
    document = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
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
