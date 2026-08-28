#!/usr/bin/env python3
"""Saturate same-signature wall t-chain adjacencies."""

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
    / "cm2_round250_source_g_wall_t_chain_patch_saturation_certificate.json"
)
SCHEMA = "cm2.round250.source-g-wall-t-chain-patch-saturation.v1"
PINS = {
    "cm2_round179_source_g_residual_tube_arrangement.py":
        "8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab",
    "cm2_round179_source_g_residual_tube_arrangement_rows.json":
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json":
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866",
    "cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json":
        "6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac",
    "cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json":
        "e340fa1a071d85a36b54d10a45ae2fdb9d70b8c90f4c21f054c6fc9505e5e787",
    "cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json":
        "b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217",
    "cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json":
        "5b08d568cccd302ac2dd62e7e9b6573ce83e015181ead168812159c9f882712f",
    "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json":
        "c76662f7cb068127f3612a3655ae720662eead9b9210b5757d771693149883c1",
    "cm2_round246_source_g_whole_signature_retained_quotient_certificate.json":
        "a448359c0a9b4495e54afe6e2d860c20fb222684bae46ee108574782a5a33bc9",
    "cm2_round247_source_g_crossing_and_source_seam_retained_quotient_certificate.json":
        "72188f5d99a220f44698f3023dd606633b364adbd02d5e20e5d4fa0ff6e1b2c7",
    "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json":
        "fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311",
    "cm2_round249_source_g_exact_key_quotient_fibre_frontier_rebuild_certificate.json":
        "a4d360f5adab92e70658f5c9d052b079707134f146e8e62a859050d80096a58f",
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


def unpack(document: dict[str, Any], table: str) -> list[dict[str, Any]]:
    columns = document["row_column_schemas"][table]
    return [
        dict(zip(columns, packed, strict=True))
        for packed in document[table]
    ]


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


def subinterval(
    lower: Q,
    upper: Q,
    depth: int,
    index: int,
) -> tuple[Q, Q]:
    width = (upper - lower) / (2 ** depth)
    return lower + index * width, lower + (index + 1) * width


class DisjointSet:
    def __init__(self, values: list[str]) -> None:
        self.parent = {value: value for value in values}

    def find(self, value: str) -> str:
        while self.parent[value] != value:
            self.parent[value] = self.parent[self.parent[value]]
            value = self.parent[value]
        return value

    def union(self, left: str, right: str) -> bool:
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root == right_root:
            return False
        smaller, larger = sorted((left_root, right_root))
        self.parent[larger] = smaller
        return True


def certify_patch(
    r179: Any,
    registry: dict[str, Any],
    left: dict[str, Any],
    right: dict[str, Any],
    local_signature: dict[str, Any],
) -> tuple[list[Q], list[Q], int, int, int, int]:
    fixed = left["box"][1]
    need(
        fixed == right["box"][0]
        and left["box"][2:] == right["box"][2:],
        "adjacent cell geometry",
    )
    base = left["box"]

    def certified(
        cell: dict[str, Any],
        corridor: list[Q],
        label: str,
        depth: int,
    ) -> bool:
        atlas_box = r179.r174.atlas.AtlasBox(
            *corridor,
            cell["adaptive_depth"] + depth,
            label,
        )
        result, reasons = r179.r174.certify_signature(
            cell["chart"],
            atlas_box,
            cell["owner_target"],
            registry,
        )
        return (
            result is not None
            and reasons == []
            and computed_signature(
                result,
                cell["chart"],
                cell["owner_target"],
            ) == local_signature
        )

    for t_depth in range(1, 7):
        left_width = (left["box"][1] - left["box"][0]) / (2 ** t_depth)
        right_width = (right["box"][1] - right["box"][0]) / (2 ** t_depth)
        for base_depth in range(0, 4):
            for p_index in range(2 ** base_depth):
                p0, p1 = subinterval(
                    base[2], base[3], base_depth, p_index
                )
                for s_index in range(2 ** base_depth):
                    s0, s1 = subinterval(
                        base[4], base[5], base_depth, s_index
                    )
                    left_corridor = [
                        fixed - left_width,
                        fixed,
                        p0,
                        p1,
                        s0,
                        s1,
                    ]
                    right_corridor = [
                        fixed,
                        fixed + right_width,
                        p0,
                        p1,
                        s0,
                        s1,
                    ]
                    refinement_depth = t_depth + 2 * base_depth
                    if (
                        certified(
                            left,
                            left_corridor,
                            (
                                "round250-left-wall-chain:"
                                f"{left['interface_id']}:{left['source_row_id']}:"
                                f"{right['source_row_id']}"
                            ),
                            refinement_depth,
                        )
                        and certified(
                            right,
                            right_corridor,
                            (
                                "round250-right-wall-chain:"
                                f"{left['interface_id']}:{left['source_row_id']}:"
                                f"{right['source_row_id']}"
                            ),
                            refinement_depth,
                        )
                    ):
                        return (
                            left_corridor,
                            right_corridor,
                            t_depth,
                            base_depth,
                            p_index,
                            s_index,
                        )
    raise RuntimeError(
        "no strict wall-chain patch:"
        f"{left['interface_id']}:{left['source_row_id']}:"
        f"{right['source_row_id']}"
    )


def build() -> dict[str, Any]:
    for name in PINS:
        read_pinned(name)

    round234 = load_result(
        "cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json"
    )
    frontiers = {
        row["frontier_row_id"]: row
        for row in round234["depth6_frontier_rows"]
    }
    resolved234 = round234["resolved_descendant_rows"]
    round235 = load_result(
        "cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json"
    )
    single235 = round235["single_endpoint_graph_partition_rows"]
    round236 = load_result(
        "cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json"
    )
    double236 = round236["double_endpoint_partition_rows"]
    crossing236 = round236["crossing_dependency_discharge_rows"]
    root236 = {
        row["Round220_split_interface_id"]: row
        for row in round236["whole_root_finite_key_partition_rows"]
    }
    need(
        len(resolved234) == 12_200
        and len(single235) == 38_328
        and len(double236) == 16
        and len(crossing236) == 32
        and len(root236) == 2_640,
        "wall source census",
    )

    round248 = load_result(
        "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json"
    )
    bulk_rows = round248[
        "formal_wall_positive_volume_bulk_ledger"
    ]["rows"]
    sheet_rows = round248[
        "formal_wall_half_open_sheet_owner_ledger"
    ]["rows"]
    contact_rows = round248[
        "formal_wall_resolved_contact_ledger"
    ]["rows"]
    bulk_by_id = {
        row["wall_bulk_node_id"]: row for row in bulk_rows
    }
    bulk_id_by_source_branch = {
        (row["source_partition_row_id"], row["branch_label"]):
            row["wall_bulk_node_id"]
        for row in bulk_rows
    }
    need(
        len(bulk_by_id) == 88_936
        and len(sheet_rows) == 38_360
        and len(contact_rows) == 2_640,
        "Round248 wall universe",
    )

    cells_by_interface: dict[str, list[dict[str, Any]]] = defaultdict(list)

    def add_cell(
        source: dict[str, Any],
        source_kind: str,
        source_row_id: str,
        lower_branch: str,
        upper_branch: str,
        lower_signature: dict[str, Any],
        upper_signature: dict[str, Any],
    ) -> None:
        interface_id = source["Round220_split_interface_id"]
        cells_by_interface[interface_id].append({
            "interface_id": interface_id,
            "source_kind": source_kind,
            "source_row_id": source_row_id,
            "box": box_values(source["box"]),
            "chart": source["chart"],
            "owner_target": source["owner_target"],
            "adaptive_depth": source["adaptive_depth"],
            "lower_branch": lower_branch,
            "upper_branch": upper_branch,
            "lower_bulk_node_id": bulk_id_by_source_branch[
                (source_row_id, lower_branch)
            ],
            "upper_bulk_node_id": bulk_id_by_source_branch[
                (source_row_id, upper_branch)
            ],
            "lower_signature": lower_signature,
            "upper_signature": upper_signature,
        })

    for row in resolved234:
        add_cell(
            row,
            "ROUND234_RESOLVED_DESCENDANT",
            row["materialized_row_id"],
            "RESOLVED_DESCENDANT",
            "RESOLVED_DESCENDANT",
            row["local_return_signature"],
            row["local_return_signature"],
        )
    for row in single235:
        frontier = frontiers[row["Round234_frontier_row_id"]]
        derivative = row["active_factor_strict_t_derivative_sign"]
        fixed_sign = row["fixed_endpoint_factor_sign"]
        lower_active_sign, upper_active_sign = (
            ("STRICT_NEGATIVE", "STRICT_POSITIVE")
            if derivative == "STRICT_POSITIVE"
            else ("STRICT_POSITIVE", "STRICT_NEGATIVE")
        )

        def single_branch(active_sign: str) -> str:
            return (
                "EVENT_PRESENT"
                if active_sign != fixed_sign
                else "EVENT_ABSENT"
            )

        lower_branch = single_branch(lower_active_sign)
        upper_branch = single_branch(upper_active_sign)
        signature_by_branch = {
            "EVENT_ABSENT": row["event_absent_signature"],
            "EVENT_PRESENT": row["event_present_signature"],
        }
        add_cell(
            frontier,
            "ROUND235_SINGLE_ENDPOINT_GRAPH_CELL",
            row["endpoint_graph_partition_row_id"],
            lower_branch,
            upper_branch,
            signature_by_branch[lower_branch],
            signature_by_branch[upper_branch],
        )
    for row in double236:
        frontier = frontiers[row["Round234_frontier_row_id"]]

        def endpoint_signs(derivative: str) -> tuple[str, str]:
            return (
                ("STRICT_NEGATIVE", "STRICT_POSITIVE")
                if derivative == "STRICT_POSITIVE"
                else ("STRICT_POSITIVE", "STRICT_NEGATIVE")
            )

        source_lower, source_upper = endpoint_signs(
            row["source_factor_strict_t_derivative_sign"]
        )
        target_lower, target_upper = endpoint_signs(
            row["target_factor_strict_t_derivative_sign"]
        )

        def double_branch(source_sign: str, target_sign: str) -> str:
            if source_sign == target_sign:
                return "SAME_SIGN_EVENT_ABSENT"
            return (
                "NEGATIVE_TO_POSITIVE"
                if source_sign == "STRICT_NEGATIVE"
                else "POSITIVE_TO_NEGATIVE"
            )

        lower_branch = double_branch(source_lower, target_lower)
        upper_branch = double_branch(source_upper, target_upper)
        signature_by_branch = {
            "SAME_SIGN_EVENT_ABSENT":
                row["same_sign_event_absent_signature"],
            "NEGATIVE_TO_POSITIVE":
                row["negative_to_positive_signature"],
            "POSITIVE_TO_NEGATIVE":
                row["positive_to_negative_signature"],
        }
        add_cell(
            frontier,
            "ROUND236_DOUBLE_ENDPOINT_ARRANGEMENT_CELL",
            row["double_endpoint_partition_row_id"],
            lower_branch,
            upper_branch,
            signature_by_branch[lower_branch],
            signature_by_branch[upper_branch],
        )
    for row in crossing236:
        frontier = frontiers[row["Round234_frontier_row_id"]]
        add_cell(
            frontier,
            "ROUND236_CROSSING_DISCHARGE_CELL",
            row["crossing_dependency_discharge_row_id"],
            "WHOLE_CROSSING_BOX",
            "WHOLE_CROSSING_BOX",
            row["local_return_signature"],
            row["local_return_signature"],
        )
    need(
        len(cells_by_interface) == 2_640
        and sum(len(rows) for rows in cells_by_interface.values()) == 50_576,
        "wall cell chain census",
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

    dsu = DisjointSet(list(bulk_by_id))
    edge_rows: list[dict[str, Any]] = []
    chain_edge_ids_by_root: dict[str, list[str]] = defaultdict(list)
    mismatch_descriptors: list[list[Any]] = []
    patch_depth_histogram: Counter[str] = Counter()
    source_pair_histogram: Counter[str] = Counter()
    boundary_count = 0
    exact_patch_area_sum = Q(0)
    exact_left_corridor_volume_sum = Q(0)
    exact_right_corridor_volume_sum = Q(0)

    for interface_id, cells in sorted(cells_by_interface.items()):
        cells.sort(
            key=lambda row: (
                row["box"][0],
                row["box"][1],
                row["source_row_id"],
            )
        )
        need(
            len(cells) >= 1
            and all(
                left["box"][1] == right["box"][0]
                and left["box"][2:] == right["box"][2:]
                for left, right in zip(cells, cells[1:])
            ),
            f"exact t chain:{interface_id}",
        )
        for left, right in zip(cells, cells[1:]):
            boundary_count += 1
            left_signature = left["upper_signature"]
            right_signature = right["lower_signature"]
            if left_signature != right_signature:
                mismatch_descriptors.append([
                    interface_id,
                    qstr(left["box"][1]),
                    left["source_row_id"],
                    left["upper_branch"],
                    digest(left_signature),
                    right["source_row_id"],
                    right["lower_branch"],
                    digest(right_signature),
                ])
                continue
            (
                left_corridor,
                right_corridor,
                t_depth,
                base_depth,
                p_index,
                s_index,
            ) = certify_patch(
                r179,
                registry,
                left,
                right,
                left_signature,
            )
            left_bulk_id = left["upper_bulk_node_id"]
            right_bulk_id = right["lower_bulk_node_id"]
            need(
                dsu.union(left_bulk_id, right_bulk_id),
                f"nonredundant wall-chain edge:{interface_id}",
            )
            base_rectangle = [
                left_corridor[2],
                left_corridor[3],
                left_corridor[4],
                left_corridor[5],
            ]
            edge_id = "round250-wall-chain-edge:" + digest([
                interface_id,
                left_bulk_id,
                right_bulk_id,
                qstr(left["box"][1]),
                [qstr(value) for value in base_rectangle],
            ])
            source_pair = f"{left['source_kind']}->{right['source_kind']}"
            edge_rows.append(closed({
                "wall_chain_edge_id": edge_id,
                "Round220_split_interface_id": interface_id,
                "left_source_partition_kind": left["source_kind"],
                "left_source_partition_row_id": left["source_row_id"],
                "left_endpoint_branch": left["upper_branch"],
                "left_wall_bulk_node_id": left_bulk_id,
                "right_source_partition_kind": right["source_kind"],
                "right_source_partition_row_id": right["source_row_id"],
                "right_endpoint_branch": right["lower_branch"],
                "right_wall_bulk_node_id": right_bulk_id,
                "shared_t_coordinate": qstr(left["box"][1]),
                "common_return_signature_sha256": digest(left_signature),
                "official_key_ordinal":
                    left_signature["official_key_ordinal"],
                "official_key_id": left_signature["official_key_id"],
                "exact_positive_2D_common_patch_rectangle":
                    [qstr(value) for value in base_rectangle],
                "exact_positive_2D_common_patch_area":
                    qstr(area(base_rectangle)),
                "left_strict_positive_3D_corridor_box":
                    [qstr(value) for value in left_corridor],
                "left_strict_positive_3D_corridor_volume":
                    qstr(volume(left_corridor)),
                "right_strict_positive_3D_corridor_box":
                    [qstr(value) for value in right_corridor],
                "right_strict_positive_3D_corridor_volume":
                    qstr(volume(right_corridor)),
                "t_dyadic_depth": t_depth,
                "base_dyadic_depth": base_depth,
                "base_p_index": p_index,
                "base_s_index": s_index,
                "interval_precision_bits": 256,
                "current_quotient_lower_bound_edge_credit": 1,
                "occurrence_known_block_incidence_credit": 0,
                "maximal_physical_component_credit": 0,
                "global_exact_key_fibre_credit": 0,
            }))
            chain_edge_ids_by_root[dsu.find(left_bulk_id)].append(edge_id)
            patch_depth_histogram[
                f"t{t_depth}:base{base_depth}:p{p_index}:s{s_index}"
            ] += 1
            source_pair_histogram[source_pair] += 1
            exact_patch_area_sum += area(base_rectangle)
            exact_left_corridor_volume_sum += volume(left_corridor)
            exact_right_corridor_volume_sum += volume(right_corridor)
    edge_rows.sort(key=lambda row: row["wall_chain_edge_id"])
    mismatch_descriptors.sort()
    need(
        boundary_count == 47_936
        and len(edge_rows) == 11_824
        and len(mismatch_descriptors) == 36_112
        and dict(patch_depth_histogram) == {
            "t1:base0:p0:s0": 11_184,
            "t1:base1:p0:s0": 640,
        },
        "wall-chain edge census",
    )

    bulk_ids_by_class: dict[str, list[str]] = defaultdict(list)
    for bulk_id in bulk_by_id:
        bulk_ids_by_class[dsu.find(bulk_id)].append(bulk_id)
    chain_edges_by_class: dict[str, list[str]] = defaultdict(list)
    for edge in edge_rows:
        root = dsu.find(edge["left_wall_bulk_node_id"])
        need(
            root == dsu.find(edge["right_wall_bulk_node_id"]),
            f"chain edge class:{edge['wall_chain_edge_id']}",
        )
        chain_edges_by_class[root].append(edge["wall_chain_edge_id"])
    need(
        len(bulk_ids_by_class) == 77_112,
        "saturated bulk class count",
    )

    sheets_by_owner: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for sheet in sheet_rows:
        sheets_by_owner[sheet["owner_wall_bulk_node_id"]].append(sheet)
    contact_by_class: dict[str, dict[str, Any]] = {}
    classes_by_old_component: dict[str, list[str]] = defaultdict(list)
    for contact in contact_rows:
        root = dsu.find(contact["selected_wall_bulk_node_id"])
        need(root not in contact_by_class, f"one contact per class:{root}")
        contact_by_class[root] = contact
        classes_by_old_component[
            contact["inherited_Round244_resolved_bulk_component_id"]
        ].append(root)
    need(len(contact_by_class) == 2_640, "contact class count")

    round179 = load_result(
        "cm2_round179_source_g_residual_tube_arrangement_rows.json"
    )
    resolved179 = {
        row["row_id"]: row
        for row in unpack(round179, "resolved_3d_child_rows")
    }
    del round179
    gc.collect()
    round244 = load_result(
        "cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json"
    )
    old_components = {
        row["resolved_bulk_component_row_id"]: row
        for row in round244["formal_resolved_bulk_component_ledger"]["rows"]
    }
    need(
        len(resolved179) == 17_192 and len(old_components) == 8_148,
        "resolved component binding",
    )

    round245 = load_result(
        "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json"
    )
    round246 = load_result(
        "cm2_round246_source_g_whole_signature_retained_quotient_certificate.json"
    )
    round247 = load_result(
        "cm2_round247_source_g_crossing_and_source_seam_retained_quotient_certificate.json"
    )
    prior_node_rows = (
        round245["formal_retained_stratum_node_ledger"]["rows"]
        + round246[
            "formal_new_whole_signature_retained_stratum_node_ledger"
        ]["rows"]
        + round247[
            "formal_new_crossing_and_source_seam_retained_stratum_node_ledger"
        ]["rows"]
    )
    prior_node_key = {
        row["retained_stratum_node_id"]: (
            row["official_key_ordinal"],
            row["official_key_id"],
        )
        for row in prior_node_rows
    }
    prior_components = {
        row["inherited_Round244_resolved_bulk_component_id"]: row
        for row in round247[
            "formal_post_Round247_mixed_sheet_component_ledger"
        ]["rows"]
    }
    need(
        len(prior_node_key) == 6_388
        and len(prior_components) == 8_148,
        "pre-wall mixed quotient binding",
    )
    del round245, round246, prior_node_rows
    gc.collect()

    component_rows: list[dict[str, Any]] = []
    component_ids_by_key: dict[str, list[str]] = defaultdict(list)
    inherited_component_ids_by_key: dict[str, list[str]] = defaultdict(list)
    new_wall_component_ids_by_key: dict[str, list[str]] = defaultdict(list)
    seeded_component_ids_by_key: dict[str, list[str]] = defaultdict(list)
    unseeded_component_ids_by_key: dict[str, list[str]] = defaultdict(list)
    component_member_count_by_key: Counter[str] = Counter()
    component_origin_histogram: Counter[str] = Counter()
    attached_wall_node_size_histogram: Counter[int] = Counter()
    new_wall_node_size_histogram: Counter[int] = Counter()
    attached_wall_bulk_count = 0
    attached_wall_sheet_count = 0
    new_wall_bulk_count = 0
    new_wall_sheet_count = 0
    inherited_chain_edge_count = 0
    new_chain_edge_count = 0
    total_virtual_node_count = 0
    total_mixed_edge_count = 0
    total_materialized_member_count = 0
    seeded_component_count = 0
    cumulative_seeded_virtual_node_count = 0

    for component_id, component in sorted(old_components.items()):
        resolved_member_ids = component[
            "member_Round179_resolved_child_row_ids"
        ]
        resolved_keys = {
            (
                resolved179[member_id]["official_key_ordinal"],
                resolved179[member_id]["official_key_id"],
            )
            for member_id in resolved_member_ids
        }
        need(
            len(resolved_keys) == 1,
            f"inherited resolved key purity:{component_id}",
        )
        key_ordinal, key_id = next(iter(resolved_keys))
        prior = prior_components[component_id]
        prior_nodes = prior["cumulative_virtual_stratum_node_ids"]
        prior_edges = prior["cumulative_mixed_sheet_edge_ids"]
        need(
            all(
                prior_node_key[node_id] == (key_ordinal, key_id)
                for node_id in prior_nodes
            ),
            f"inherited prior key purity:{component_id}",
        )
        wall_nodes: list[str] = []
        wall_edges: list[str] = []
        for root in classes_by_old_component.get(component_id, []):
            bulk_ids = sorted(bulk_ids_by_class[root])
            sheets = sorted(
                (
                    sheet
                    for bulk_id in bulk_ids
                    for sheet in sheets_by_owner.get(bulk_id, [])
                ),
                key=lambda row: row["wall_sheet_node_id"],
            )
            need(
                all(
                    (
                        bulk_by_id[bulk_id]["official_key_ordinal"],
                        bulk_by_id[bulk_id]["official_key_id"],
                    ) == (key_ordinal, key_id)
                    for bulk_id in bulk_ids
                )
                and all(
                    sheet["owner_official_key_id"] == key_id
                    for sheet in sheets
                ),
                f"attached wall key purity:{component_id}:{root}",
            )
            wall_nodes.extend(bulk_ids)
            wall_nodes.extend(
                sheet["wall_sheet_node_id"] for sheet in sheets
            )
            wall_edges.extend(chain_edges_by_class.get(root, []))
            wall_edges.extend(
                sheet["owner_mixed_sheet_edge_id"] for sheet in sheets
            )
            wall_edges.append(contact_by_class[root]["mixed_sheet_edge_id"])
            attached_wall_bulk_count += len(bulk_ids)
            attached_wall_sheet_count += len(sheets)
            attached_wall_node_size_histogram[
                len(bulk_ids) + len(sheets)
            ] += 1
            inherited_chain_edge_count += len(
                chain_edges_by_class.get(root, [])
            )
        virtual_nodes = sorted(prior_nodes + wall_nodes)
        mixed_edges = sorted(prior_edges + wall_edges)
        seed_blocks = component["seed_Round243_known_connectivity_block_ids"]
        member_count = len(resolved_member_ids) + len(virtual_nodes)
        need(
            len(virtual_nodes) == len(set(virtual_nodes))
            and len(mixed_edges) == len(set(mixed_edges)),
            f"inherited component unique members:{component_id}",
        )
        component_rows.append(closed({
            "mixed_sheet_component_row_id":
                "round250-mixed-sheet-component:"
                + digest([component_id, virtual_nodes]),
            "mixed_sheet_quotient_component_id": component_id,
            "component_origin":
                "INHERITED_ROUND244_COMPONENT_SATURATED_THROUGH_ROUND250",
            "official_key_ordinal": key_ordinal,
            "official_key_id": key_id,
            "member_Round179_resolved_child_count":
                len(resolved_member_ids),
            "member_Round179_resolved_child_row_ids_sha256":
                digest(sorted(resolved_member_ids)),
            "virtual_stratum_node_count": len(virtual_nodes),
            "virtual_stratum_node_ids": virtual_nodes,
            "virtual_stratum_node_ids_sha256": digest(virtual_nodes),
            "mixed_sheet_edge_count": len(mixed_edges),
            "mixed_sheet_edge_ids": mixed_edges,
            "mixed_sheet_edge_ids_sha256": digest(mixed_edges),
            "materialized_member_count": member_count,
            "new_Round250_wall_chain_edge_count":
                sum(
                    len(chain_edges_by_class.get(root, []))
                    for root in classes_by_old_component.get(
                        component_id, []
                    )
                ),
            "seed_known_connectivity_block_count": len(seed_blocks),
            "seed_known_connectivity_block_ids": seed_blocks,
            "virtual_stratum_known_block_incidence_count":
                len(virtual_nodes) if seed_blocks else 0,
            "component_exact_key_assignment_credit": 1,
            "certified_known_connectivity_only": True,
            "maximal_physical_component_claimed": False,
            "global_exact_key_fibre_credit": 0,
        }))
        component_ids_by_key[key_id].append(component_id)
        inherited_component_ids_by_key[key_id].append(component_id)
        if seed_blocks:
            seeded_component_ids_by_key[key_id].append(component_id)
            seeded_component_count += 1
            cumulative_seeded_virtual_node_count += len(virtual_nodes)
        else:
            unseeded_component_ids_by_key[key_id].append(component_id)
        component_member_count_by_key[key_id] += member_count
        component_origin_histogram[
            "INHERITED_ROUND244_COMPONENT_SATURATED_THROUGH_ROUND250"
        ] += 1
        total_virtual_node_count += len(virtual_nodes)
        total_mixed_edge_count += len(mixed_edges)
        total_materialized_member_count += member_count

    for root, bulk_ids_unsorted in sorted(bulk_ids_by_class.items()):
        if root in contact_by_class:
            continue
        bulk_ids = sorted(bulk_ids_unsorted)
        sheets = sorted(
            (
                sheet
                for bulk_id in bulk_ids
                for sheet in sheets_by_owner.get(bulk_id, [])
            ),
            key=lambda row: row["wall_sheet_node_id"],
        )
        keys = {
            (
                bulk_by_id[bulk_id]["official_key_ordinal"],
                bulk_by_id[bulk_id]["official_key_id"],
            )
            for bulk_id in bulk_ids
        }
        need(
            len(keys) == 1
            and all(
                sheet["owner_official_key_id"] == next(iter(keys))[1]
                for sheet in sheets
            ),
            f"new saturated wall key purity:{root}",
        )
        key_ordinal, key_id = next(iter(keys))
        virtual_nodes = sorted(
            bulk_ids
            + [sheet["wall_sheet_node_id"] for sheet in sheets]
        )
        mixed_edges = sorted(
            chain_edges_by_class.get(root, [])
            + [sheet["owner_mixed_sheet_edge_id"] for sheet in sheets]
        )
        component_id = "round250-saturated-wall-component:" + digest([
            bulk_ids,
            [sheet["wall_sheet_node_id"] for sheet in sheets],
        ])
        component_rows.append(closed({
            "mixed_sheet_component_row_id":
                "round250-mixed-sheet-component:"
                + digest([component_id, virtual_nodes]),
            "mixed_sheet_quotient_component_id": component_id,
            "component_origin": "ROUND250_NEW_SATURATED_WALL_COMPONENT",
            "official_key_ordinal": key_ordinal,
            "official_key_id": key_id,
            "member_Round179_resolved_child_count": 0,
            "member_Round179_resolved_child_row_ids_sha256": digest([]),
            "virtual_stratum_node_count": len(virtual_nodes),
            "virtual_stratum_node_ids": virtual_nodes,
            "virtual_stratum_node_ids_sha256": digest(virtual_nodes),
            "mixed_sheet_edge_count": len(mixed_edges),
            "mixed_sheet_edge_ids": mixed_edges,
            "mixed_sheet_edge_ids_sha256": digest(mixed_edges),
            "materialized_member_count": len(virtual_nodes),
            "new_Round250_wall_chain_edge_count":
                len(chain_edges_by_class.get(root, [])),
            "seed_known_connectivity_block_count": 0,
            "seed_known_connectivity_block_ids": [],
            "virtual_stratum_known_block_incidence_count": 0,
            "component_exact_key_assignment_credit": 1,
            "certified_known_connectivity_only": True,
            "maximal_physical_component_claimed": False,
            "global_exact_key_fibre_credit": 0,
        }))
        component_ids_by_key[key_id].append(component_id)
        new_wall_component_ids_by_key[key_id].append(component_id)
        unseeded_component_ids_by_key[key_id].append(component_id)
        component_member_count_by_key[key_id] += len(virtual_nodes)
        component_origin_histogram[
            "ROUND250_NEW_SATURATED_WALL_COMPONENT"
        ] += 1
        new_wall_bulk_count += len(bulk_ids)
        new_wall_sheet_count += len(sheets)
        new_wall_node_size_histogram[len(virtual_nodes)] += 1
        new_chain_edge_count += len(chain_edges_by_class.get(root, []))
        total_virtual_node_count += len(virtual_nodes)
        total_mixed_edge_count += len(mixed_edges)
        total_materialized_member_count += len(virtual_nodes)

    component_rows.sort(key=lambda row: row["mixed_sheet_component_row_id"])
    need(
        len(component_rows) == 82_620
        and dict(component_origin_histogram) == {
            "INHERITED_ROUND244_COMPONENT_SATURATED_THROUGH_ROUND250":
                8_148,
            "ROUND250_NEW_SATURATED_WALL_COMPONENT": 74_472,
        }
        and attached_wall_bulk_count == 14_464
        and attached_wall_sheet_count == 1_216
        and new_wall_bulk_count == 74_472
        and new_wall_sheet_count == 37_144
        and inherited_chain_edge_count == 11_824
        and new_chain_edge_count == 0
        and dict(attached_wall_node_size_histogram)
        == {1: 8, 2: 120, 3: 120, 4: 144, 5: 432, 6: 880,
            7: 480, 8: 408, 9: 48}
        and dict(new_wall_node_size_histogram)
        == {1: 37_344, 2: 37_112, 3: 16}
        and total_virtual_node_count == 133_684
        and total_mixed_edge_count == 59_212
        and total_materialized_member_count == 150_876,
        "Round250 component census",
    )

    round249 = load_result(
        "cm2_round249_source_g_exact_key_quotient_fibre_frontier_rebuild_certificate.json"
    )
    prior_fibres = {
        row["official_key_id"]: row
        for row in round249[
            "formal_exact_key_quotient_fibre_frontier_ledger"
        ]["rows"]
    }
    need(len(prior_fibres) == 116, "Round249 fibre binding")

    fibre_rows: list[dict[str, Any]] = []
    component_count_histogram: Counter[int] = Counter()
    fibre_status_histogram: Counter[str] = Counter()
    keys_with_blocks = 0
    keys_with_new_wall = 0
    for key_id, prior in sorted(
        prior_fibres.items(),
        key=lambda item: item[1]["official_key_ordinal"],
    ):
        component_ids = sorted(component_ids_by_key[key_id])
        inherited_ids = sorted(inherited_component_ids_by_key[key_id])
        new_wall_ids = sorted(new_wall_component_ids_by_key[key_id])
        seeded_ids = sorted(seeded_component_ids_by_key[key_id])
        unseeded_ids = sorted(unseeded_component_ids_by_key[key_id])
        need(
            component_ids
            and inherited_ids
            and len(seeded_ids) + len(unseeded_ids) == len(component_ids),
            f"Round250 fibre component partition:{key_id}",
        )
        fibre_rows.append(closed({
            "quotient_fibre_frontier_row_id":
                "round250-quotient-fibre-frontier:" + digest(key_id),
            "official_key_ordinal": prior["official_key_ordinal"],
            "official_key_id": key_id,
            "official_key_row": prior["official_key_row"],
            "local_occurrence_count": prior["local_occurrence_count"],
            "occurrences_with_known_block_incidence":
                prior["occurrences_with_known_block_incidence"],
            "occurrences_without_known_block_incidence":
                prior["occurrences_without_known_block_incidence"],
            "occurrence_ids_sha256": prior["occurrence_ids_sha256"],
            "unattached_occurrence_ids_sha256":
                prior["unattached_occurrence_ids_sha256"],
            "unattached_occurrence_gauge_histogram":
                prior["unattached_occurrence_gauge_histogram"],
            "Round249_mixed_sheet_quotient_component_count":
                prior["mixed_sheet_quotient_component_count"],
            "post_Round250_mixed_sheet_quotient_component_count":
                len(component_ids),
            "Round250_component_reduction":
                prior["mixed_sheet_quotient_component_count"]
                - len(component_ids),
            "mixed_sheet_quotient_component_ids_sha256":
                digest(component_ids),
            "inherited_Round244_component_count": len(inherited_ids),
            "new_Round250_wall_component_count": len(new_wall_ids),
            "seeded_quotient_component_count": len(seeded_ids),
            "unseeded_quotient_component_count": len(unseeded_ids),
            "materialized_component_member_count":
                component_member_count_by_key[key_id],
            "known_connectivity_block_count":
                prior["known_connectivity_block_count"],
            "known_connectivity_block_ids_sha256":
                prior["known_connectivity_block_ids_sha256"],
            "frontier_status": prior["frontier_status"],
            "quotient_fibre_component_inventory_complete": True,
            "all_local_occurrences_have_known_block_incidence": False,
            "all_quotient_components_proved_maximal": False,
            "global_exact_key_fibre_exhausted": False,
            "quotient_fibre_inventory_credit": 1,
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
            "global_exact_key_disposition_credit": 0,
        }))
        component_count_histogram[len(component_ids)] += 1
        fibre_status_histogram[prior["frontier_status"]] += 1
        keys_with_blocks += bool(prior["known_connectivity_block_count"])
        keys_with_new_wall += bool(new_wall_ids)
    fibre_rows.sort(key=lambda row: row["quotient_fibre_frontier_row_id"])
    need(
        len(fibre_rows) == 116
        and keys_with_blocks == 24
        and keys_with_new_wall == 92
        and dict(component_count_histogram) == {
            2: 8, 12: 4, 14: 4, 17: 4, 21: 4, 112: 4, 124: 4,
            316: 8, 319: 8, 325: 4, 330: 8, 506: 4, 641: 8,
            647: 8, 868: 4, 1_613: 8, 1_615: 8, 1_921: 8,
            1_924: 8,
        },
        "Round250 fibre census",
    )

    census = {
        "wall_root_count": 2_640,
        "wall_t_chain_cell_count": 50_576,
        "wall_t_chain_internal_boundary_count": boundary_count,
        "accepted_same_signature_wall_chain_edge_count": len(edge_rows),
        "unaccepted_different_signature_boundary_count":
            len(mismatch_descriptors),
        "different_signature_boundary_commitment_sha256":
            digest(mismatch_descriptors),
        "patch_depth_histogram": dict(sorted(patch_depth_histogram.items())),
        "source_pair_histogram": dict(sorted(source_pair_histogram.items())),
        "exact_common_patch_area_sum": qstr(exact_patch_area_sum),
        "exact_left_corridor_volume_sum":
            qstr(exact_left_corridor_volume_sum),
        "exact_right_corridor_volume_sum":
            qstr(exact_right_corridor_volume_sum),
        "Round249_mixed_sheet_quotient_component_count": 94_444,
        "post_Round250_mixed_sheet_quotient_component_count":
            len(component_rows),
        "Round250_mixed_sheet_quotient_component_reduction":
            94_444 - len(component_rows),
        "component_origin_histogram":
            dict(sorted(component_origin_histogram.items())),
        "attached_wall_bulk_node_count": attached_wall_bulk_count,
        "attached_wall_sheet_node_count": attached_wall_sheet_count,
        "attached_wall_node_size_histogram": {
            str(key): value
            for key, value in sorted(
                attached_wall_node_size_histogram.items()
            )
        },
        "new_saturated_wall_bulk_node_count": new_wall_bulk_count,
        "new_saturated_wall_sheet_node_count": new_wall_sheet_count,
        "new_saturated_wall_component_size_histogram": {
            str(key): value
            for key, value in sorted(new_wall_node_size_histogram.items())
        },
        "new_chain_edges_inside_inherited_components":
            inherited_chain_edge_count,
        "new_chain_edges_inside_new_wall_components":
            new_chain_edge_count,
        "cumulative_virtual_stratum_node_count": total_virtual_node_count,
        "Round249_cumulative_mixed_sheet_edge_count": 47_388,
        "cumulative_mixed_sheet_edge_count": total_mixed_edge_count,
        "materialized_component_member_count":
            total_materialized_member_count,
        "seeded_quotient_component_count": seeded_component_count,
        "unseeded_quotient_component_count":
            len(component_rows) - seeded_component_count,
        "cumulative_virtual_stratum_known_block_incidence_count":
            cumulative_seeded_virtual_node_count,
        "observed_exact_key_count": 116,
        "quotient_fibre_inventory_complete_count": len(fibre_rows),
        "mixed_sheet_quotient_component_count_histogram": {
            str(key): value
            for key, value in sorted(component_count_histogram.items())
        },
        "fibre_frontier_status_histogram":
            dict(sorted(fibre_status_histogram.items())),
        "post_Round250_occurrences_with_known_block_incidence": 36_200,
        "post_Round250_occurrences_without_known_block_incidence": 17_768,
        "new_occurrence_known_block_incidence_count": 0,
        "maximality_unproved_quotient_component_count":
            len(component_rows),
        "globally_exhausted_exact_key_fibre_count": 0,
        "global_exact_key_disposition_count": 0,
    }
    return {
        "status": (
            "CERTIFIED_11824_STRICT_WALL_T_CHAIN_PATCH_EDGES__"
            "QUOTIENT_COMPONENTS_94444_TO_82620__"
            "116_FIBRE_INVENTORIES_REFRESHED__ZERO_GLOBAL_PROMOTION"
        ),
        "census": census,
        "formal_input_binding": {
            name: PINS[name] for name in sorted(PINS)
        },
        "formal_wall_t_chain_positive_patch_edge_ledger":
            ledger(edge_rows, "wall_chain_edge_id"),
        "formal_post_Round250_mixed_sheet_component_ledger":
            ledger(component_rows, "mixed_sheet_component_row_id"),
        "formal_post_Round250_exact_key_quotient_fibre_frontier_ledger":
            ledger(fibre_rows, "quotient_fibre_frontier_row_id"),
        "scope_contract": {
            "all_47936_internal_t_boundaries_are_exactly_classified": True,
            "all_11824_same_signature_boundaries_have_256_bit_two_sided_positive_volume_patches": True,
            "all_36112_different_signature_boundaries_receive_no_bulk_edge": True,
            "all_new_edges_are_memberwise_exact_key_pure": True,
            "all_11824_new_edges_reduce_the_current_quotient_rank": True,
            "all_116_quotient_fibre_inventories_are_refreshed": True,
            "quotient_saturation_is_not_component_maximality": True,
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
            "materialize the remaining within-cell and p-interface physical "
            "adjacencies for the 74472 saturated wall components, then close "
            "the 17768 occurrence deficits before maximality or global-fibre "
            "promotion"
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
