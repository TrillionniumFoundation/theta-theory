#!/usr/bin/env python3
"""Materialize the final wall finite-key retained quotient."""

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
import sys
import tempfile
from typing import Any

from flint import ctx


HERE = Path(__file__).resolve().parent
OUTPUT = (
    HERE
    / "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json"
)
SCHEMA = "cm2.round248.source-g-wall-finite-key-retained-quotient.v1"
PINS = {
    "cm2_round179_source_g_residual_tube_arrangement.py":
        "8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab",
    "cm2_round179_source_g_residual_tube_arrangement_rows.json":
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json":
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866",
    "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json":
        "569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974",
    "cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json":
        "6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac",
    "cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json":
        "e340fa1a071d85a36b54d10a45ae2fdb9d70b8c90f4c21f054c6fc9505e5e787",
    "cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json":
        "b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217",
    "cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json":
        "5b08d568cccd302ac2dd62e7e9b6573ce83e015181ead168812159c9f882712f",
    "cm2_round247_source_g_crossing_and_source_seam_retained_quotient_certificate.json":
        "72188f5d99a220f44698f3023dd606633b364adbd02d5e20e5d4fa0ff6e1b2c7",
}
MAXIMUM_BYTES = {
    name: 5_000_000 if name.endswith(".py") or "manifest" in name
    else 400_000_000
    for name in PINS
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


def unpack_table(value: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        dict(zip(value["columns"], packed, strict=True))
        for packed in value["rows"]
    ]


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
        len(rectangle) == 4
        and rectangle[0] < rectangle[1]
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


def computed_signature(
    result: dict[str, Any],
    chart: str,
    target: str,
) -> dict[str, Any]:
    return {
        "source_chart": chart,
        "target_lift": target,
        "ordered_integer_wall_events": result["events"],
        "signed_wall_word": list(result["pattern"]),
        "roof": result["roof"],
        "outgoing_cell": result["outgoing"],
        "target_chart": result["target_chart"],
        "official_key_row": result["key"]["row"],
        "official_key_ordinal": result["key"]["ordinal"],
        "official_key_id": result["key"]["identifier"],
    }


def bulk_node_id(
    source_kind: str,
    source_row_id: str,
    branch_label: str,
    signature: dict[str, Any],
) -> str:
    return "round248-wall-bulk:" + digest([
        source_kind,
        source_row_id,
        branch_label,
        digest(signature),
    ])


def sheet_node_id(
    source_kind: str,
    source_row_id: str,
    endpoint_factor: str,
    owner_signature: dict[str, Any],
) -> str:
    return "round248-wall-sheet:" + digest([
        source_kind,
        source_row_id,
        endpoint_factor,
        digest(owner_signature),
    ])


def interval_contact_corridor(
    r179: Any,
    registry: dict[str, Any],
    frontier: dict[str, Any],
    interface: dict[str, Any],
    signature: dict[str, Any],
) -> tuple[list[Q], int, int, str]:
    box = box_values(frontier["box"])
    fixed = Q(interface["fixed_coordinate"])
    need(
        interface["axis"] == "p" and fixed in {box[2], box[3]},
        f"p-interface frontier:{interface['split_interface_id']}",
    )
    for p_depth in range(1, 8):
        p_width = (box[3] - box[2]) / (2 ** p_depth)
        p0, p1 = (
            (box[2], box[2] + p_width)
            if fixed == box[2]
            else (box[3] - p_width, box[3])
        )
        for t_depth in range(1, 9):
            t_width = (box[1] - box[0]) / (2 ** t_depth)
            for side in ("LOWER_T_SIDE", "UPPER_T_SIDE"):
                t0, t1 = (
                    (box[0], box[0] + t_width)
                    if side == "LOWER_T_SIDE"
                    else (box[1] - t_width, box[1])
                )
                corridor = [t0, t1, p0, p1, box[4], box[5]]
                atlas_box = r179.r174.atlas.AtlasBox(
                    *corridor,
                    frontier["adaptive_depth"] + p_depth + t_depth,
                    (
                        "round248-wall-p-corridor:"
                        f"{interface['split_interface_id']}:{p_depth}:"
                        f"{t_depth}:{side}"
                    ),
                )
                computed, reasons = r179.r174.certify_signature(
                    frontier["chart"],
                    atlas_box,
                    frontier["owner_target"],
                    registry,
                )
                if (
                    computed is not None
                    and reasons == []
                    and computed_signature(
                        computed,
                        frontier["chart"],
                        frontier["owner_target"],
                    ) == signature
                ):
                    return corridor, p_depth, t_depth, side
    raise RuntimeError(
        f"strict p-interface wall corridor:{interface['split_interface_id']}"
    )


def build() -> dict[str, Any]:
    for name in PINS:
        read_pinned(name)

    round236 = load_result(
        "cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json"
    )
    root_sources = round236["whole_root_finite_key_partition_rows"]
    interface_ids = {
        row["Round220_split_interface_id"] for row in root_sources
    }
    need(
        len(root_sources) == len(interface_ids) == 2_640,
        "Round236 root universe",
    )

    round220 = load_result(
        "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json"
    )
    interface_table = round220["coordinate_boundary_atlas"]["tables"][
        "one_step_split_interface_rows"
    ]
    interfaces = {
        row["split_interface_id"]: row
        for row in unpack_table(interface_table)
        if row["split_interface_id"] in interface_ids
    }
    need(len(interfaces) == 2_640, "Round220 wall interfaces")
    del round220
    gc.collect()

    retained_ids: set[str] = set()
    resolved_ids: set[str] = set()
    for interface in interfaces.values():
        need(
            {interface["lower_child_kind"], interface["upper_child_kind"]}
            == {"RESOLVED", "RETAINED"}
            and interface["event_trace_materialized_on_interface"] is False,
            f"interface lineage:{interface['split_interface_id']}",
        )
        retained_ids.add(
            interface["lower_child_row_id"]
            if interface["lower_child_kind"] == "RETAINED"
            else interface["upper_child_row_id"]
        )
        resolved_ids.add(
            interface["lower_child_row_id"]
            if interface["lower_child_kind"] == "RESOLVED"
            else interface["upper_child_row_id"]
        )
    need(
        len(retained_ids) == len(resolved_ids) == 2_640,
        "wall child universe",
    )

    round179 = load_result(
        "cm2_round179_source_g_residual_tube_arrangement_rows.json"
    )
    retained = unpack_selected(
        round179, "retained_3d_child_rows", "row_id", retained_ids
    )
    resolved = unpack_selected(
        round179, "resolved_3d_child_rows", "row_id", resolved_ids
    )
    need(
        len(retained) == len(resolved) == 2_640,
        "Round179 wall children",
    )
    del round179
    gc.collect()

    round234 = load_result(
        "cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json"
    )
    resolved234 = round234["resolved_descendant_rows"]
    frontiers = {
        row["frontier_row_id"]: row
        for row in round234["depth6_frontier_rows"]
    }
    need(
        len(resolved234) == 12_200
        and len(frontiers) == 38_376,
        "Round234 wall partition",
    )

    round235 = load_result(
        "cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json"
    )
    single235 = round235["single_endpoint_graph_partition_rows"]
    need(len(single235) == 38_328, "Round235 single graph partition")

    double236 = round236["double_endpoint_partition_rows"]
    crossing236 = round236["crossing_dependency_discharge_rows"]
    need(
        len(double236) == 16 and len(crossing236) == 32,
        "Round236 residual partition",
    )

    round244 = load_result(
        "cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json"
    )
    old_components = {
        row["resolved_bulk_component_row_id"]: row
        for row in round244["formal_resolved_bulk_component_ledger"]["rows"]
    }
    component_by_resolved = {
        child_id: component_id
        for component_id, component in old_components.items()
        for child_id in component["member_Round179_resolved_child_row_ids"]
    }
    need(
        len(old_components) == 8_148
        and len(component_by_resolved) == 17_192,
        "Round244 component partition",
    )
    del round244
    gc.collect()

    round247 = load_result(
        "cm2_round247_source_g_crossing_and_source_seam_retained_quotient_certificate.json"
    )
    prior_components = {
        row["inherited_Round244_resolved_bulk_component_id"]: row
        for row in round247[
            "formal_post_Round247_mixed_sheet_component_ledger"
        ]["rows"]
    }
    occurrence_commitment = round247["unchanged_occurrence_frontier_commitment"]
    key_commitment = round247["unchanged_key_frontier_commitment"]
    need(
        len(prior_components) == 8_148
        and round247["census"]["remaining_Round239_interface_count"] == 2_640
        and round247["census"]["cumulative_virtual_stratum_node_count"]
        == 6_388,
        "Round247 quotient binding",
    )

    sys.path.insert(0, str(HERE))
    import cm2_round179_source_g_residual_tube_arrangement as r179

    need(
        Path(r179.__file__).resolve()
        == (HERE / "cm2_round179_source_g_residual_tube_arrangement.py").resolve(),
        "Round179 module identity",
    )
    registry = r179.load_inputs()["registry"]
    ctx.prec = 256

    bulk_specs: list[dict[str, Any]] = []
    bulk_id_by_source_branch: dict[tuple[str, str], str] = {}
    bulk_ids_by_interface: dict[str, list[str]] = defaultdict(list)
    signatures_by_interface: dict[str, list[dict[str, Any]]] = defaultdict(list)
    source_kind_histogram: Counter[str] = Counter()
    exact_bulk_volume_sum: Counter[str] = Counter()

    def add_bulk(
        interface_id: str,
        source_kind: str,
        source_row_id: str,
        branch_label: str,
        signature: dict[str, Any],
        proof_kind: str,
        exact_box: list[str] | None,
    ) -> str:
        node_id = bulk_node_id(
            source_kind,
            source_row_id,
            branch_label,
            signature,
        )
        need(
            (source_row_id, branch_label) not in bulk_id_by_source_branch,
            f"unique bulk source:{source_row_id}:{branch_label}",
        )
        exact_volume = (
            qstr(volume(box_values(exact_box)))
            if exact_box is not None
            else None
        )
        bulk_specs.append({
            "wall_bulk_node_id": node_id,
            "Round220_split_interface_id": interface_id,
            "source_partition_kind": source_kind,
            "source_partition_row_id": source_row_id,
            "branch_label": branch_label,
            "local_return_signature_sha256": digest(signature),
            "official_key_ordinal": signature["official_key_ordinal"],
            "official_key_id": signature["official_key_id"],
            "positive_volume_proof_kind": proof_kind,
            "exact_positive_3D_box": exact_box,
            "exact_positive_3D_volume": exact_volume,
        })
        bulk_id_by_source_branch[(source_row_id, branch_label)] = node_id
        bulk_ids_by_interface[interface_id].append(node_id)
        signatures_by_interface[interface_id].append(signature)
        source_kind_histogram[source_kind] += 1
        if exact_box is not None:
            exact_bulk_volume_sum[source_kind] += volume(box_values(exact_box))
        return node_id

    for row in resolved234:
        add_bulk(
            row["Round220_split_interface_id"],
            "ROUND234_RESOLVED_DESCENDANT",
            row["materialized_row_id"],
            "RESOLVED_DESCENDANT",
            row["local_return_signature"],
            "ROUND234_EXACT_DYADIC_POSITIVE_3D_BOX",
            row["box"],
        )
    for row in single235:
        add_bulk(
            row["Round220_split_interface_id"],
            "ROUND235_SINGLE_ENDPOINT_GRAPH_BRANCH",
            row["endpoint_graph_partition_row_id"],
            "EVENT_ABSENT",
            row["event_absent_signature"],
            "ROUND235_STRICT_MONOTONE_GRAPH_ABSENT_OPEN_SIDE",
            None,
        )
        add_bulk(
            row["Round220_split_interface_id"],
            "ROUND235_SINGLE_ENDPOINT_GRAPH_BRANCH",
            row["endpoint_graph_partition_row_id"],
            "EVENT_PRESENT",
            row["event_present_signature"],
            "ROUND235_STRICT_MONOTONE_GRAPH_PRESENT_OPEN_SIDE",
            None,
        )
    for row in double236:
        add_bulk(
            row["Round220_split_interface_id"],
            "ROUND236_DOUBLE_ENDPOINT_ARRANGEMENT_BRANCH",
            row["double_endpoint_partition_row_id"],
            "SAME_SIGN_EVENT_ABSENT",
            row["same_sign_event_absent_signature"],
            "ROUND236_TWO_ENDPOINT_GRAPHS_SAME_SIGN_OPEN_REGION",
            None,
        )
        add_bulk(
            row["Round220_split_interface_id"],
            "ROUND236_DOUBLE_ENDPOINT_ARRANGEMENT_BRANCH",
            row["double_endpoint_partition_row_id"],
            "NEGATIVE_TO_POSITIVE",
            row["negative_to_positive_signature"],
            "ROUND236_TWO_ENDPOINT_GRAPHS_NEGATIVE_TO_POSITIVE_OPEN_REGION",
            None,
        )
        add_bulk(
            row["Round220_split_interface_id"],
            "ROUND236_DOUBLE_ENDPOINT_ARRANGEMENT_BRANCH",
            row["double_endpoint_partition_row_id"],
            "POSITIVE_TO_NEGATIVE",
            row["positive_to_negative_signature"],
            "ROUND236_TWO_ENDPOINT_GRAPHS_POSITIVE_TO_NEGATIVE_OPEN_REGION",
            None,
        )
    for row in crossing236:
        frontier = frontiers[row["Round234_frontier_row_id"]]
        add_bulk(
            row["Round220_split_interface_id"],
            "ROUND236_CROSSING_DISCHARGE_BULK",
            row["crossing_dependency_discharge_row_id"],
            "WHOLE_CROSSING_BOX",
            row["local_return_signature"],
            "ROUND236_ENDPOINT_OPPOSITION_WHOLE_POSITIVE_3D_BOX",
            frontier["box"],
        )
    need(
        len(bulk_specs) == 88_936
        and dict(source_kind_histogram) == {
            "ROUND234_RESOLVED_DESCENDANT": 12_200,
            "ROUND235_SINGLE_ENDPOINT_GRAPH_BRANCH": 76_656,
            "ROUND236_CROSSING_DISCHARGE_BULK": 32,
            "ROUND236_DOUBLE_ENDPOINT_ARRANGEMENT_BRANCH": 48,
        },
        "positive-volume wall piece census",
    )

    sheet_specs: list[dict[str, Any]] = []
    owner_sheet_ids_by_bulk: dict[str, list[str]] = defaultdict(list)
    owner_edge_ids_by_bulk: dict[str, list[str]] = defaultdict(list)
    sheet_source_histogram: Counter[str] = Counter()

    def add_sheet(
        interface_id: str,
        source_kind: str,
        source_row_id: str,
        endpoint_factor: str,
        owner_signature: dict[str, Any],
        owner_bulk_id: str,
        frontier_id: str,
    ) -> None:
        frontier = frontiers[frontier_id]
        box = box_values(frontier["box"])
        base = [box[2], box[3], box[4], box[5]]
        node_id = sheet_node_id(
            source_kind,
            source_row_id,
            endpoint_factor,
            owner_signature,
        )
        edge_id = "round248-wall-sheet-owner-edge:" + digest([
            interface_id,
            owner_bulk_id,
            node_id,
            [qstr(value) for value in base],
        ])
        sheet_specs.append({
            "wall_sheet_node_id": node_id,
            "owner_mixed_sheet_edge_id": edge_id,
            "Round220_split_interface_id": interface_id,
            "source_partition_kind": source_kind,
            "source_partition_row_id": source_row_id,
            "endpoint_factor": endpoint_factor,
            "owner_wall_bulk_node_id": owner_bulk_id,
            "owner_signature_sha256": digest(owner_signature),
            "owner_official_key_id": owner_signature["official_key_id"],
            "exact_closed_base_rectangle":
                [qstr(value) for value in base],
            "exact_positive_2D_sheet_area": qstr(area(base)),
            "sheet_three_dimensional_coordinate_volume": "0",
            "half_open_owner_rule":
                "EVENT_ABSENT_BECAUSE_ENDPOINT_EVENT_TIME_IS_OUTSIDE_OPEN_0_1",
        })
        owner_sheet_ids_by_bulk[owner_bulk_id].append(node_id)
        owner_edge_ids_by_bulk[owner_bulk_id].append(edge_id)
        sheet_source_histogram[source_kind] += 1

    for row in single235:
        owner_bulk_id = bulk_id_by_source_branch[
            (row["endpoint_graph_partition_row_id"], "EVENT_ABSENT")
        ]
        add_sheet(
            row["Round220_split_interface_id"],
            "ROUND235_SINGLE_ENDPOINT_GRAPH_SHEET",
            row["endpoint_graph_partition_row_id"],
            row["active_endpoint_factor"],
            row["event_absent_signature"],
            owner_bulk_id,
            row["Round234_frontier_row_id"],
        )
    for row in double236:
        owner_bulk_id = bulk_id_by_source_branch[
            (row["double_endpoint_partition_row_id"], "SAME_SIGN_EVENT_ABSENT")
        ]
        for endpoint_factor in ("source", "target"):
            add_sheet(
                row["Round220_split_interface_id"],
                "ROUND236_DOUBLE_ENDPOINT_GRAPH_SHEET",
                row["double_endpoint_partition_row_id"],
                endpoint_factor,
                row["same_sign_event_absent_signature"],
                owner_bulk_id,
                row["Round234_frontier_row_id"],
            )
    need(
        len(sheet_specs) == 38_360
        and dict(sheet_source_histogram) == {
            "ROUND235_SINGLE_ENDPOINT_GRAPH_SHEET": 38_328,
            "ROUND236_DOUBLE_ENDPOINT_GRAPH_SHEET": 32,
        },
        "wall sheet census",
    )

    released_by_interface: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in resolved234:
        released_by_interface[row["Round220_split_interface_id"]].append(row)
    graph_by_interface: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in single235:
        graph_by_interface[row["Round220_split_interface_id"]].append(row)

    contact_specs: list[dict[str, Any]] = []
    contact_bulk_ids: set[str] = set()
    contact_nodes_by_component: dict[str, list[str]] = defaultdict(list)
    contact_edges_by_component: dict[str, list[str]] = defaultdict(list)
    wall_roots_by_component: Counter[str] = Counter()
    contact_kind_histogram: Counter[str] = Counter()
    contact_axis_histogram: Counter[str] = Counter()
    interval_depth_histogram: Counter[str] = Counter()
    interval_corridor_volume_sum = Q(0)

    root_source_by_interface = {
        row["Round220_split_interface_id"]: row for row in root_sources
    }
    for interface_id in sorted(interface_ids):
        interface = interfaces[interface_id]
        retained_id = (
            interface["lower_child_row_id"]
            if interface["lower_child_kind"] == "RETAINED"
            else interface["upper_child_row_id"]
        )
        resolved_id = (
            interface["lower_child_row_id"]
            if interface["lower_child_kind"] == "RESOLVED"
            else interface["upper_child_row_id"]
        )
        retained_row = retained[retained_id]
        resolved_row = resolved[resolved_id]
        target_signature = resolved_signature(resolved_row)
        component_id = component_by_resolved[resolved_id]
        fixed = Q(interface["fixed_coordinate"])
        axis_index = {"t": 0, "p": 1, "s": 2}[interface["axis"]]
        need(
            retained_row["origin_row_id"] == resolved_row["origin_row_id"]
            == interface["origin_row_id"]
            and retained_row["parent_id"] == resolved_row["parent_id"]
            == interface["parent_id"]
            and retained_row["chart"] == resolved_row["chart"]
            == interface["chart"],
            f"wall lineage:{interface_id}",
        )
        direct = sorted(
            (
                row for row in released_by_interface[interface_id]
                if row["local_return_signature"] == target_signature
                and fixed in {
                    Q(row["box"][2 * axis_index]),
                    Q(row["box"][2 * axis_index + 1]),
                }
            ),
            key=lambda row: row["materialized_row_id"],
        )
        if direct:
            selected = direct[0]
            selected_source_kind = "ROUND234_RESOLVED_DESCENDANT"
            selected_source_row_id = selected["materialized_row_id"]
            selected_branch = "RESOLVED_DESCENDANT"
            corridor = box_values(selected["box"])
            proof_kind = "ROUND234_EXACT_RESOLVED_DESCENDANT_INTERFACE_FACE"
            p_depth = None
            t_depth = None
            t_side = None
        else:
            need(interface["axis"] == "p", f"non-p contact miss:{interface_id}")
            selected_graph = None
            selected_branch = None
            for graph in sorted(
                graph_by_interface[interface_id],
                key=lambda row: row["endpoint_graph_partition_row_id"],
            ):
                frontier = frontiers[graph["Round234_frontier_row_id"]]
                frontier_box = box_values(frontier["box"])
                if (
                    fixed not in {frontier_box[2], frontier_box[3]}
                    or target_signature not in (
                        graph["event_absent_signature"],
                        graph["event_present_signature"],
                    )
                ):
                    continue
                corridor, p_depth, t_depth, t_side = (
                    interval_contact_corridor(
                        r179,
                        registry,
                        frontier,
                        interface,
                        target_signature,
                    )
                )
                selected_graph = graph
                selected_branch = (
                    "EVENT_ABSENT"
                    if target_signature == graph["event_absent_signature"]
                    else "EVENT_PRESENT"
                )
                break
            need(
                selected_graph is not None and selected_branch is not None,
                f"interval contact:{interface_id}",
            )
            selected_source_kind = "ROUND235_SINGLE_ENDPOINT_GRAPH_BRANCH"
            selected_source_row_id = selected_graph[
                "endpoint_graph_partition_row_id"
            ]
            proof_kind = "256_BIT_STRICT_DYADIC_P_INTERFACE_CORRIDOR"
            interval_depth_histogram[
                f"p{p_depth}:t{t_depth}:{t_side}"
            ] += 1
            interval_corridor_volume_sum += volume(corridor)
        selected_bulk_id = bulk_id_by_source_branch[
            (selected_source_row_id, selected_branch)
        ]
        need(
            selected_bulk_id not in contact_bulk_ids,
            f"unique contact bulk:{interface_id}",
        )
        contact_bulk_ids.add(selected_bulk_id)
        contact = tangential_rectangle(corridor, interface["axis"])
        edge_id = "round248-wall-resolved-contact-edge:" + digest([
            interface_id,
            resolved_id,
            selected_bulk_id,
            [qstr(value) for value in contact],
        ])
        contact_id = "round248-wall-resolved-contact:" + digest([
            interface_id,
            selected_bulk_id,
            edge_id,
        ])
        contact_specs.append({
            "wall_resolved_contact_row_id": contact_id,
            "mixed_sheet_edge_id": edge_id,
            "Round220_split_interface_id": interface_id,
            "Round179_retained_child_row_id": retained_id,
            "Round179_resolved_sibling_row_id": resolved_id,
            "inherited_Round244_resolved_bulk_component_id": component_id,
            "selected_wall_bulk_node_id": selected_bulk_id,
            "selected_source_partition_kind": selected_source_kind,
            "selected_source_partition_row_id": selected_source_row_id,
            "selected_branch_label": selected_branch,
            "resolved_signature_sha256": digest(target_signature),
            "contact_proof_kind": proof_kind,
            "exact_positive_2D_contact_rectangle":
                [qstr(value) for value in contact],
            "exact_positive_2D_contact_area": qstr(area(contact)),
            "strict_positive_3D_retained_corridor_box":
                [qstr(value) for value in corridor],
            "strict_positive_3D_retained_corridor_volume":
                qstr(volume(corridor)),
            "interval_p_depth": p_depth,
            "interval_t_depth": t_depth,
            "interval_t_side": t_side,
            "interval_precision_bits": 256 if p_depth is not None else None,
        })
        contact_nodes_by_component[component_id].append(selected_bulk_id)
        contact_edges_by_component[component_id].append(edge_id)
        wall_roots_by_component[component_id] += 1
        contact_kind_histogram[proof_kind] += 1
        contact_axis_histogram[interface["axis"]] += 1

    need(
        len(contact_specs) == len(contact_bulk_ids) == 2_640
        and dict(contact_kind_histogram) == {
            "256_BIT_STRICT_DYADIC_P_INTERFACE_CORRIDOR": 8,
            "ROUND234_EXACT_RESOLVED_DESCENDANT_INTERFACE_FACE": 2_632,
        }
        and dict(contact_axis_histogram) == {"p": 656, "t": 1_984}
        and dict(interval_depth_histogram)
        == {"p1:t1:LOWER_T_SIDE": 8},
        "resolved contact census",
    )

    component_by_bulk: dict[str, str] = {}
    for spec in bulk_specs:
        bulk_id = spec["wall_bulk_node_id"]
        if bulk_id in contact_bulk_ids:
            interface = interfaces[spec["Round220_split_interface_id"]]
            resolved_id = (
                interface["lower_child_row_id"]
                if interface["lower_child_kind"] == "RESOLVED"
                else interface["upper_child_row_id"]
            )
            component_id = component_by_resolved[resolved_id]
        else:
            component_id = "round248-wall-virtual-component:" + digest([
                bulk_id,
                sorted(owner_sheet_ids_by_bulk.get(bulk_id, [])),
            ])
        component_by_bulk[bulk_id] = component_id

    bulk_rows: list[dict[str, Any]] = []
    for spec in bulk_specs:
        bulk_id = spec["wall_bulk_node_id"]
        owner_sheets = sorted(owner_sheet_ids_by_bulk.get(bulk_id, []))
        bulk_rows.append(closed({
            **spec,
            "assigned_mixed_sheet_quotient_component_id":
                component_by_bulk[bulk_id],
            "attached_to_inherited_Round244_component":
                bulk_id in contact_bulk_ids,
            "owned_half_open_wall_sheet_count": len(owner_sheets),
            "owned_half_open_wall_sheet_ids_sha256": digest(owner_sheets),
            "occurrence_known_block_incidence_credit": 0,
            "physical_component_credit": 0,
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
        }))
    bulk_rows.sort(key=lambda row: row["wall_bulk_node_id"])

    sheet_rows: list[dict[str, Any]] = []
    sheet_ids_by_interface: dict[str, list[str]] = defaultdict(list)
    for spec in sheet_specs:
        component_id = component_by_bulk[spec["owner_wall_bulk_node_id"]]
        need(
            not component_id.startswith("round244-resolved-bulk-component:"),
            f"wall sheet must remain unseeded:{spec['wall_sheet_node_id']}",
        )
        sheet_rows.append(closed({
            **spec,
            "assigned_mixed_sheet_quotient_component_id": component_id,
            "owner_edge_current_quotient_lower_bound_credit": 1,
            "occurrence_known_block_incidence_credit": 0,
            "physical_component_credit": 0,
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
        }))
        sheet_ids_by_interface[spec["Round220_split_interface_id"]].append(
            spec["wall_sheet_node_id"]
        )
    sheet_rows.sort(key=lambda row: row["wall_sheet_node_id"])

    contact_rows = [
        closed({
            **spec,
            "current_quotient_lower_bound_edge_credit": 1,
            "occurrence_known_block_incidence_credit": 0,
            "physical_component_credit": 0,
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
        })
        for spec in contact_specs
    ]
    contact_rows.sort(key=lambda row: row["wall_resolved_contact_row_id"])

    root_rows: list[dict[str, Any]] = []
    contact_by_interface = {
        row["Round220_split_interface_id"]: row for row in contact_rows
    }
    positive_piece_count_histogram: Counter[int] = Counter()
    sheet_count_histogram: Counter[int] = Counter()
    key_count_histogram: Counter[int] = Counter()
    for interface_id in sorted(interface_ids):
        source = root_source_by_interface[interface_id]
        bulk_ids = sorted(bulk_ids_by_interface[interface_id])
        sheet_ids = sorted(sheet_ids_by_interface[interface_id])
        signatures = signatures_by_interface[interface_id]
        key_pairs = sorted({
            (item["official_key_ordinal"], item["official_key_id"])
            for item in signatures
        })
        need(
            len(bulk_ids) == source["finite_partition_piece_count"]
            and [item[0] for item in key_pairs]
            == source["candidate_exact_key_ordinals"]
            and [item[1] for item in key_pairs]
            == source["candidate_exact_key_ids"],
            f"root conservation:{interface_id}",
        )
        contact = contact_by_interface[interface_id]
        positive_piece_count_histogram[len(bulk_ids)] += 1
        sheet_count_histogram[len(sheet_ids)] += 1
        key_count_histogram[len(key_pairs)] += 1
        root_rows.append(closed({
            "wall_root_attachment_row_id":
                "round248-wall-root-attachment:" + digest(interface_id),
            "Round236_whole_root_partition_row_id":
                source["whole_root_partition_row_id"],
            "Round220_split_interface_id": interface_id,
            "inherited_Round244_resolved_bulk_component_id":
                contact["inherited_Round244_resolved_bulk_component_id"],
            "positive_volume_bulk_node_count": len(bulk_ids),
            "positive_volume_bulk_node_ids_sha256": digest(bulk_ids),
            "half_open_wall_sheet_node_count": len(sheet_ids),
            "half_open_wall_sheet_node_ids_sha256": digest(sheet_ids),
            "candidate_exact_key_count": len(key_pairs),
            "candidate_exact_key_ordinals": [item[0] for item in key_pairs],
            "candidate_exact_key_ids": [item[1] for item in key_pairs],
            "selected_resolved_contact_bulk_node_id":
                contact["selected_wall_bulk_node_id"],
            "selected_resolved_contact_row_id":
                contact["wall_resolved_contact_row_id"],
            "whole_retained_root_locally_exhausted": True,
            "occurrence_known_block_incidence_credit": 0,
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
        }))
    root_rows.sort(key=lambda row: row["wall_root_attachment_row_id"])
    need(
        len(root_rows) == 2_640
        and dict(key_count_histogram) == {1: 408, 2: 2_216, 3: 16},
        "wall root attachment ledger",
    )

    component_rows: list[dict[str, Any]] = []
    new_touched = 0
    overlap = 0
    cumulative_touched = 0
    cumulative_seeded_nodes = 0
    cumulative_root_histogram: Counter[int] = Counter()
    for component_id, prior in sorted(prior_components.items()):
        new_nodes = sorted(contact_nodes_by_component.get(component_id, []))
        new_edges = sorted(contact_edges_by_component.get(component_id, []))
        prior_nodes = prior["cumulative_virtual_stratum_node_ids"]
        prior_edges = prior["cumulative_mixed_sheet_edge_ids"]
        cumulative_nodes = sorted(prior_nodes + new_nodes)
        cumulative_edges = sorted(prior_edges + new_edges)
        prior_roots = prior["cumulative_retained_root_count"]
        new_roots = wall_roots_by_component[component_id]
        cumulative_roots = prior_roots + new_roots
        seed_blocks = prior["seed_known_connectivity_block_ids"]
        need(
            not (new_roots and seed_blocks),
            f"wall contact component must be unseeded:{component_id}",
        )
        new_touched += bool(new_roots)
        overlap += bool(new_roots and prior_roots)
        cumulative_touched += bool(cumulative_roots)
        cumulative_seeded_nodes += len(cumulative_nodes) if seed_blocks else 0
        cumulative_root_histogram[cumulative_roots] += 1
        component_rows.append(closed({
            "mixed_sheet_component_row_id":
                "round248-inherited-mixed-sheet-component:"
                + digest([component_id, cumulative_nodes]),
            "inherited_Round244_resolved_bulk_component_id": component_id,
            "Round247_cumulative_retained_root_count": prior_roots,
            "new_Round248_wall_retained_root_count": new_roots,
            "cumulative_retained_root_count": cumulative_roots,
            "Round247_cumulative_virtual_stratum_node_count":
                len(prior_nodes),
            "new_Round248_wall_bulk_node_count": len(new_nodes),
            "cumulative_virtual_stratum_node_count": len(cumulative_nodes),
            "cumulative_virtual_stratum_node_ids": cumulative_nodes,
            "cumulative_virtual_stratum_node_ids_sha256":
                digest(cumulative_nodes),
            "Round247_cumulative_mixed_sheet_edge_count": len(prior_edges),
            "new_Round248_wall_contact_edge_count": len(new_edges),
            "cumulative_mixed_sheet_edge_count": len(cumulative_edges),
            "cumulative_mixed_sheet_edge_ids": cumulative_edges,
            "cumulative_mixed_sheet_edge_ids_sha256":
                digest(cumulative_edges),
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
        and new_touched == 1_480
        and overlap == 0
        and cumulative_touched == 5_760
        and cumulative_seeded_nodes == 316
        and dict(cumulative_root_histogram)
        == {0: 2_388, 1: 3_272, 2: 2_300, 3: 144, 4: 32, 5: 4, 6: 8},
        "inherited component enrichment census",
    )

    new_component_descriptors: list[dict[str, Any]] = []
    new_component_size_histogram: Counter[int] = Counter()
    new_component_member_count = 0
    for bulk in bulk_rows:
        if bulk["attached_to_inherited_Round244_component"]:
            continue
        bulk_id = bulk["wall_bulk_node_id"]
        sheet_ids = sorted(owner_sheet_ids_by_bulk.get(bulk_id, []))
        members = [bulk_id, *sheet_ids]
        component_id = component_by_bulk[bulk_id]
        internal_edges = sorted(owner_edge_ids_by_bulk.get(bulk_id, []))
        descriptor = {
            "mixed_sheet_quotient_component_id": component_id,
            "official_key_id": bulk["official_key_id"],
            "member_node_ids": members,
            "member_node_count": len(members),
            "internal_sheet_owner_edge_ids": internal_edges,
        }
        new_component_descriptors.append(descriptor)
        new_component_size_histogram[len(members)] += 1
        new_component_member_count += len(members)
    new_component_descriptors.sort(
        key=lambda row: row["mixed_sheet_quotient_component_id"]
    )
    need(
        len(new_component_descriptors) == 86_296
        and new_component_member_count == 124_656
        and dict(new_component_size_histogram)
        == {1: 47_952, 2: 38_328, 3: 16},
        "new virtual component census",
    )
    new_component_commitment = {
        "component_count": len(new_component_descriptors),
        "component_ids_sha256": digest([
            row["mixed_sheet_quotient_component_id"]
            for row in new_component_descriptors
        ]),
        "component_descriptors_sha256": digest(new_component_descriptors),
        "member_node_count": new_component_member_count,
        "internal_sheet_owner_edge_count": len(sheet_rows),
        "component_size_histogram": {
            str(key): value
            for key, value in sorted(new_component_size_histogram.items())
        },
        "every_component_is_unseeded_known_connectivity_lower_bound_only": True,
        "no_cross_key_glue": True,
    }

    census = {
        "Round236_wall_retained_root_count": 2_640,
        "positive_volume_wall_bulk_node_count": len(bulk_rows),
        "wall_bulk_source_kind_histogram":
            dict(sorted(source_kind_histogram.items())),
        "half_open_wall_sheet_node_count": len(sheet_rows),
        "wall_sheet_source_kind_histogram":
            dict(sorted(sheet_source_histogram.items())),
        "new_wall_virtual_stratum_node_count":
            len(bulk_rows) + len(sheet_rows),
        "new_wall_mixed_sheet_edge_count":
            len(contact_rows) + len(sheet_rows),
        "resolved_contact_edge_count": len(contact_rows),
        "resolved_contact_proof_kind_histogram":
            dict(sorted(contact_kind_histogram.items())),
        "resolved_contact_axis_histogram":
            dict(sorted(contact_axis_histogram.items())),
        "interval_contact_depth_histogram":
            dict(sorted(interval_depth_histogram.items())),
        "interval_contact_exact_corridor_volume_sum":
            qstr(interval_corridor_volume_sum),
        "Round234_exact_bulk_volume_sum":
            qstr(exact_bulk_volume_sum["ROUND234_RESOLVED_DESCENDANT"]),
        "Round236_crossing_exact_bulk_volume_sum":
            qstr(exact_bulk_volume_sum["ROUND236_CROSSING_DISCHARGE_BULK"]),
        "positive_piece_count_per_root_histogram": {
            str(key): value
            for key, value in sorted(positive_piece_count_histogram.items())
        },
        "sheet_count_per_root_histogram": {
            str(key): value
            for key, value in sorted(sheet_count_histogram.items())
        },
        "candidate_key_count_per_root_histogram": {
            str(key): value
            for key, value in sorted(key_count_histogram.items())
        },
        "new_touched_Round244_component_count": new_touched,
        "prior_and_wall_touched_component_overlap_count": overlap,
        "cumulative_touched_Round244_component_count": cumulative_touched,
        "inherited_Round244_component_count": 8_148,
        "new_unseeded_wall_virtual_component_count":
            len(new_component_descriptors),
        "post_Round248_mixed_sheet_quotient_component_count":
            8_148 + len(new_component_descriptors),
        "new_unseeded_wall_virtual_component_member_count":
            new_component_member_count,
        "Round247_cumulative_virtual_stratum_node_count": 6_388,
        "cumulative_virtual_stratum_node_count":
            6_388 + len(bulk_rows) + len(sheet_rows),
        "Round247_cumulative_mixed_sheet_edge_count": 6_388,
        "cumulative_mixed_sheet_edge_count":
            6_388 + len(contact_rows) + len(sheet_rows),
        "new_virtual_stratum_known_block_incidence_count": 0,
        "cumulative_virtual_stratum_known_block_incidence_count":
            cumulative_seeded_nodes,
        "new_occurrence_known_block_incidence_count": 0,
        "known_connectivity_block_count": 7_388,
        "post_Round248_occurrences_with_known_block_incidence": 36_200,
        "post_Round248_occurrences_without_known_block_incidence": 17_768,
        "remaining_Round239_interface_count": 0,
        "maximal_physical_component_assignment_count": 0,
        "global_exact_key_fibre_exhausted_count": 0,
    }
    return {
        "status": (
            "CERTIFIED_2640_WALL_RETAINED_ROOTS__"
            "88936_POSITIVE_VOLUME_BULKS__38360_HALF_OPEN_SHEETS__"
            "ALL_8500_ROUND239_UNACCEPTED_INTERFACES_LOCALLY_MAPPED__"
            "ZERO_NEW_OCCURRENCE_INCIDENCE"
        ),
        "census": census,
        "formal_input_binding": {
            name: PINS[name] for name in sorted(PINS)
        },
        "formal_wall_positive_volume_bulk_ledger":
            ledger(bulk_rows, "wall_bulk_node_id"),
        "formal_wall_half_open_sheet_owner_ledger":
            ledger(sheet_rows, "wall_sheet_node_id"),
        "formal_wall_resolved_contact_ledger":
            ledger(contact_rows, "wall_resolved_contact_row_id"),
        "formal_wall_root_attachment_ledger":
            ledger(root_rows, "wall_root_attachment_row_id"),
        "formal_post_Round248_inherited_component_enrichment_ledger":
            ledger(component_rows, "mixed_sheet_component_row_id"),
        "formal_new_unseeded_wall_virtual_component_commitment":
            new_component_commitment,
        "unchanged_occurrence_frontier_commitment": occurrence_commitment,
        "unchanged_key_frontier_commitment": key_commitment,
        "scope_contract": {
            "all_2640_Round236_roots_have_exhaustive_positive_volume_and_sheet_materialization": True,
            "all_88936_positive_volume_pieces_are_materialized_once": True,
            "all_38360_endpoint_graph_sheets_are_half_open_owned_by_event_absent_bulk": True,
            "all_2640_roots_have_one_positive_area_resolved_contact": True,
            "all_8_missing_exact_face_contacts_have_256_bit_strict_positive_volume_corridors": True,
            "all_8500_Round239_unaccepted_interfaces_are_now_locally_mapped": True,
            "exact_key_equality_alone_never_supplies_glue": True,
            "virtual_stratum_incidence_is_not_occurrence_incidence": True,
            "mixed_sheet_components_are_known_connectivity_lower_bounds_only": True,
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
            "rebuild all 116 exact-key fibres over the expanded mixed-sheet "
            "known-connectivity quotient, then prove component maximality and "
            "complete the remaining occurrence incidence without treating "
            "local interface closure or exact-key equality as global glue"
        ),
    }


def safe_write(raw: bytes) -> None:
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{OUTPUT.name}.",
        dir=OUTPUT.parent,
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
