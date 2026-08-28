#!/usr/bin/env python3
"""Independently verify the Round250 wall-chain saturation."""

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
    / "cm2_round250_source_g_wall_t_chain_patch_saturation_verification.json"
)
SCHEMA = (
    "cm2.round250.source-g-wall-t-chain-patch-saturation.verification.v1"
)
SOURCE_PINS = {
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
PINS = {
    **SOURCE_PINS,
    "cm2_round250_source_g_wall_t_chain_patch_saturation.py":
        "2e663d7f60461db5966513bc6de7335489acfa22546f9eaac3030e8db1d95eb0",
    "cm2_round250_source_g_wall_t_chain_patch_saturation_certificate.json":
        "07eb8ab4f5fbcec7df4a891f3e55b3990c8400a01bbbff8950f05519e886ca8a",
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


def validate_ledger(
    value: dict[str, Any],
    id_field: str,
) -> list[dict[str, Any]]:
    rows = value["rows"]
    row_ids = [row[id_field] for row in rows]
    need(
        value["row_count"] == len(rows)
        and len(rows) == len(set(row_ids))
        and row_ids == sorted(row_ids)
        and value["rows_sha256"] == digest(rows)
        and value["row_ids_sha256"] == digest(row_ids)
        and value["row_hashes_sha256"]
        == digest([row["row_sha256"] for row in rows])
        and value["every_row_closed_by_own_SHA256"] is True
        and all(
            row["row_sha256"]
            == digest({
                key: item
                for key, item in row.items()
                if key != "row_sha256"
            })
            for row in rows
        ),
        f"ledger:{id_field}",
    )
    return rows


def exact_row(candidate: dict[str, Any], expected: dict[str, Any], label: str) -> None:
    need(
        {
            key: value
            for key, value in candidate.items()
            if key != "row_sha256"
        } == expected,
        label,
    )


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
    return (
        (rectangle[1] - rectangle[0])
        * (rectangle[3] - rectangle[2])
    )


def signature_from_kernel(
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


def dyadic_subinterval(
    lower: Q,
    upper: Q,
    depth: int,
    index: int,
) -> tuple[Q, Q]:
    width = (upper - lower) / (2 ** depth)
    return lower + index * width, lower + (index + 1) * width


class DSU:
    def __init__(self, values: list[str]) -> None:
        self.parent = {value: value for value in values}

    def find(self, value: str) -> str:
        while self.parent[value] != value:
            self.parent[value] = self.parent[self.parent[value]]
            value = self.parent[value]
        return value

    def join(self, left: str, right: str) -> bool:
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root == right_root:
            return False
        smaller, larger = sorted((left_root, right_root))
        self.parent[larger] = smaller
        return True


def independent_patch(
    r179: Any,
    registry: dict[str, Any],
    left: dict[str, Any],
    right: dict[str, Any],
    target_signature: dict[str, Any],
) -> tuple[list[Q], list[Q], int, int, int, int]:
    fixed = left["box"][1]
    need(
        fixed == right["box"][0]
        and left["box"][2:] == right["box"][2:],
        "patch adjacency",
    )

    def certify(
        cell: dict[str, Any],
        corridor: list[Q],
        refinement: int,
        label: str,
    ) -> bool:
        atlas_box = r179.r174.atlas.AtlasBox(
            *corridor,
            cell["adaptive_depth"] + refinement,
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
            and signature_from_kernel(
                result,
                cell["chart"],
                cell["owner_target"],
            ) == target_signature
        )

    for t_depth in range(1, 7):
        left_width = (left["box"][1] - left["box"][0]) / (2 ** t_depth)
        right_width = (right["box"][1] - right["box"][0]) / (2 ** t_depth)
        for base_depth in range(0, 4):
            for p_index in range(2 ** base_depth):
                p0, p1 = dyadic_subinterval(
                    left["box"][2],
                    left["box"][3],
                    base_depth,
                    p_index,
                )
                for s_index in range(2 ** base_depth):
                    s0, s1 = dyadic_subinterval(
                        left["box"][4],
                        left["box"][5],
                        base_depth,
                        s_index,
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
                    refinement = t_depth + 2 * base_depth
                    if (
                        certify(
                            left,
                            left_corridor,
                            refinement,
                            "round250-independent-left",
                        )
                        and certify(
                            right,
                            right_corridor,
                            refinement,
                            "round250-independent-right",
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
        f"independent patch:{left['interface_id']}:"
        f"{left['source_row_id']}:{right['source_row_id']}"
    )


def verify() -> dict[str, Any]:
    for name in PINS:
        read_pinned(name)
    candidate = load_result(
        "cm2_round250_source_g_wall_t_chain_patch_saturation_certificate.json"
    )
    need(
        candidate["formal_input_binding"]
        == {name: SOURCE_PINS[name] for name in sorted(SOURCE_PINS)},
        "candidate source binding",
    )
    edge_rows = validate_ledger(
        candidate["formal_wall_t_chain_positive_patch_edge_ledger"],
        "wall_chain_edge_id",
    )
    component_rows = validate_ledger(
        candidate["formal_post_Round250_mixed_sheet_component_ledger"],
        "mixed_sheet_component_row_id",
    )
    fibre_rows = validate_ledger(
        candidate[
            "formal_post_Round250_exact_key_quotient_fibre_frontier_ledger"
        ],
        "quotient_fibre_frontier_row_id",
    )
    need(
        len(edge_rows) == 11_824
        and len(component_rows) == 82_620
        and len(fibre_rows) == 116,
        "candidate census",
    )
    edge_by_source_pair = {
        (
            row["Round220_split_interface_id"],
            row["left_source_partition_row_id"],
            row["right_source_partition_row_id"],
        ): row
        for row in edge_rows
    }
    component_by_id = {
        row["mixed_sheet_quotient_component_id"]: row
        for row in component_rows
    }
    fibre_by_key = {
        row["official_key_id"]: row for row in fibre_rows
    }

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
    source_roots = round236["whole_root_finite_key_partition_rows"]
    need(
        len(resolved234) == 12_200
        and len(single235) == 38_328
        and len(double236) == 16
        and len(crossing236) == 32
        and len(source_roots) == 2_640,
        "wall sources",
    )

    round248 = load_result(
        "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json"
    )
    wall_bulks = round248[
        "formal_wall_positive_volume_bulk_ledger"
    ]["rows"]
    wall_sheets = round248[
        "formal_wall_half_open_sheet_owner_ledger"
    ]["rows"]
    contacts = round248["formal_wall_resolved_contact_ledger"]["rows"]
    bulk_by_id = {
        row["wall_bulk_node_id"]: row for row in wall_bulks
    }
    bulk_id_by_source_branch = {
        (row["source_partition_row_id"], row["branch_label"]):
            row["wall_bulk_node_id"]
        for row in wall_bulks
    }
    need(
        len(bulk_by_id) == 88_936
        and len(wall_sheets) == 38_360
        and len(contacts) == 2_640,
        "Round248 wall inputs",
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
        cells_by_interface[source["Round220_split_interface_id"]].append({
            "interface_id": source["Round220_split_interface_id"],
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
        lower_sign, upper_sign = (
            ("STRICT_NEGATIVE", "STRICT_POSITIVE")
            if row["active_factor_strict_t_derivative_sign"]
            == "STRICT_POSITIVE"
            else ("STRICT_POSITIVE", "STRICT_NEGATIVE")
        )

        def branch(active_sign: str) -> str:
            return (
                "EVENT_PRESENT"
                if active_sign != row["fixed_endpoint_factor_sign"]
                else "EVENT_ABSENT"
            )

        lower_branch = branch(lower_sign)
        upper_branch = branch(upper_sign)
        signatures = {
            "EVENT_ABSENT": row["event_absent_signature"],
            "EVENT_PRESENT": row["event_present_signature"],
        }
        add_cell(
            frontier,
            "ROUND235_SINGLE_ENDPOINT_GRAPH_CELL",
            row["endpoint_graph_partition_row_id"],
            lower_branch,
            upper_branch,
            signatures[lower_branch],
            signatures[upper_branch],
        )
    for row in double236:
        frontier = frontiers[row["Round234_frontier_row_id"]]

        def signs(derivative: str) -> tuple[str, str]:
            return (
                ("STRICT_NEGATIVE", "STRICT_POSITIVE")
                if derivative == "STRICT_POSITIVE"
                else ("STRICT_POSITIVE", "STRICT_NEGATIVE")
            )

        source_lower, source_upper = signs(
            row["source_factor_strict_t_derivative_sign"]
        )
        target_lower, target_upper = signs(
            row["target_factor_strict_t_derivative_sign"]
        )

        def branch(source_sign: str, target_sign: str) -> str:
            if source_sign == target_sign:
                return "SAME_SIGN_EVENT_ABSENT"
            return (
                "NEGATIVE_TO_POSITIVE"
                if source_sign == "STRICT_NEGATIVE"
                else "POSITIVE_TO_NEGATIVE"
            )

        lower_branch = branch(source_lower, target_lower)
        upper_branch = branch(source_upper, target_upper)
        signatures = {
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
            signatures[lower_branch],
            signatures[upper_branch],
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
        and sum(len(cells) for cells in cells_by_interface.values())
        == 50_576,
        "cell partition",
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

    dsu = DSU(list(bulk_by_id))
    mismatch_descriptors: list[list[Any]] = []
    patch_histogram: Counter[str] = Counter()
    source_pair_histogram: Counter[str] = Counter()
    boundary_count = 0
    patch_area_sum = Q(0)
    left_volume_sum = Q(0)
    right_volume_sum = Q(0)
    expected_edge_ids: set[str] = set()

    for interface_id, cells in cells_by_interface.items():
        cells.sort(
            key=lambda row: (
                row["box"][0],
                row["box"][1],
                row["source_row_id"],
            )
        )
        need(
            all(
                left["box"][1] == right["box"][0]
                and left["box"][2:] == right["box"][2:]
                for left, right in zip(cells, cells[1:])
            ),
            f"cell chain:{interface_id}",
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
            ) = independent_patch(
                r179,
                registry,
                left,
                right,
                left_signature,
            )
            left_bulk_id = left["upper_bulk_node_id"]
            right_bulk_id = right["lower_bulk_node_id"]
            need(
                dsu.join(left_bulk_id, right_bulk_id),
                f"rank edge:{interface_id}",
            )
            rectangle = [
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
                [qstr(value) for value in rectangle],
            ])
            expected = {
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
                    [qstr(value) for value in rectangle],
                "exact_positive_2D_common_patch_area":
                    qstr(area(rectangle)),
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
            }
            key = (
                interface_id,
                left["source_row_id"],
                right["source_row_id"],
            )
            exact_row(edge_by_source_pair[key], expected, f"edge:{key}")
            expected_edge_ids.add(edge_id)
            patch_histogram[
                f"t{t_depth}:base{base_depth}:p{p_index}:s{s_index}"
            ] += 1
            source_pair_histogram[
                f"{left['source_kind']}->{right['source_kind']}"
            ] += 1
            patch_area_sum += area(rectangle)
            left_volume_sum += volume(left_corridor)
            right_volume_sum += volume(right_corridor)
    mismatch_descriptors.sort()
    need(
        boundary_count == 47_936
        and len(expected_edge_ids) == len(edge_rows) == 11_824
        and expected_edge_ids == {
            row["wall_chain_edge_id"] for row in edge_rows
        }
        and len(mismatch_descriptors) == 36_112,
        "edge universe",
    )

    bulk_ids_by_class: dict[str, list[str]] = defaultdict(list)
    for bulk_id in bulk_by_id:
        bulk_ids_by_class[dsu.find(bulk_id)].append(bulk_id)
    chain_edges_by_class: dict[str, list[str]] = defaultdict(list)
    for edge in edge_rows:
        root = dsu.find(edge["left_wall_bulk_node_id"])
        need(root == dsu.find(edge["right_wall_bulk_node_id"]), "edge class")
        chain_edges_by_class[root].append(edge["wall_chain_edge_id"])
    need(len(bulk_ids_by_class) == 77_112, "bulk classes")

    sheets_by_owner: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for sheet in wall_sheets:
        sheets_by_owner[sheet["owner_wall_bulk_node_id"]].append(sheet)
    contact_by_class: dict[str, dict[str, Any]] = {}
    classes_by_old: dict[str, list[str]] = defaultdict(list)
    for contact in contacts:
        root = dsu.find(contact["selected_wall_bulk_node_id"])
        need(root not in contact_by_class, f"contact class:{root}")
        contact_by_class[root] = contact
        classes_by_old[
            contact["inherited_Round244_resolved_bulk_component_id"]
        ].append(root)
    need(len(contact_by_class) == 2_640, "contact classes")

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
    round245 = load_result(
        "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json"
    )
    round246 = load_result(
        "cm2_round246_source_g_whole_signature_retained_quotient_certificate.json"
    )
    round247 = load_result(
        "cm2_round247_source_g_crossing_and_source_seam_retained_quotient_certificate.json"
    )
    prior_nodes = (
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
        for row in prior_nodes
    }
    prior_components = {
        row["inherited_Round244_resolved_bulk_component_id"]: row
        for row in round247[
            "formal_post_Round247_mixed_sheet_component_ledger"
        ]["rows"]
    }
    del round245, round246, prior_nodes
    gc.collect()
    need(
        len(old_components) == len(prior_components) == 8_148
        and len(prior_node_key) == 6_388,
        "old component inputs",
    )

    component_ids_by_key: dict[str, list[str]] = defaultdict(list)
    inherited_ids_by_key: dict[str, list[str]] = defaultdict(list)
    new_ids_by_key: dict[str, list[str]] = defaultdict(list)
    seeded_ids_by_key: dict[str, list[str]] = defaultdict(list)
    unseeded_ids_by_key: dict[str, list[str]] = defaultdict(list)
    member_count_by_key: Counter[str] = Counter()
    origin_histogram: Counter[str] = Counter()
    attached_size_histogram: Counter[int] = Counter()
    new_size_histogram: Counter[int] = Counter()
    attached_bulk_count = 0
    attached_sheet_count = 0
    new_bulk_count = 0
    new_sheet_count = 0
    inherited_chain_edges = 0
    new_chain_edges = 0
    total_virtual_nodes = 0
    total_edges = 0
    total_members = 0
    seeded_component_count = 0
    seeded_virtual_nodes = 0
    expected_component_ids: set[str] = set()

    for component_id, component in old_components.items():
        resolved_ids = component["member_Round179_resolved_child_row_ids"]
        keys = {
            (
                resolved179[row_id]["official_key_ordinal"],
                resolved179[row_id]["official_key_id"],
            )
            for row_id in resolved_ids
        }
        need(len(keys) == 1, f"resolved component purity:{component_id}")
        key_ordinal, key_id = next(iter(keys))
        prior = prior_components[component_id]
        prior_node_ids = prior["cumulative_virtual_stratum_node_ids"]
        prior_edge_ids = prior["cumulative_mixed_sheet_edge_ids"]
        need(
            all(
                prior_node_key[node_id] == (key_ordinal, key_id)
                for node_id in prior_node_ids
            ),
            f"prior component purity:{component_id}",
        )
        wall_node_ids: list[str] = []
        wall_edge_ids: list[str] = []
        component_chain_count = 0
        for root in classes_by_old.get(component_id, []):
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
                f"attached class purity:{root}",
            )
            wall_node_ids.extend(bulk_ids)
            wall_node_ids.extend(
                sheet["wall_sheet_node_id"] for sheet in sheets
            )
            wall_edge_ids.extend(chain_edges_by_class.get(root, []))
            wall_edge_ids.extend(
                sheet["owner_mixed_sheet_edge_id"] for sheet in sheets
            )
            wall_edge_ids.append(contact_by_class[root]["mixed_sheet_edge_id"])
            attached_bulk_count += len(bulk_ids)
            attached_sheet_count += len(sheets)
            attached_size_histogram[len(bulk_ids) + len(sheets)] += 1
            component_chain_count += len(chain_edges_by_class.get(root, []))
            inherited_chain_edges += len(chain_edges_by_class.get(root, []))
        virtual_ids = sorted(prior_node_ids + wall_node_ids)
        edge_ids = sorted(prior_edge_ids + wall_edge_ids)
        seed_blocks = component["seed_Round243_known_connectivity_block_ids"]
        member_count = len(resolved_ids) + len(virtual_ids)
        expected = {
            "mixed_sheet_component_row_id":
                "round250-mixed-sheet-component:"
                + digest([component_id, virtual_ids]),
            "mixed_sheet_quotient_component_id": component_id,
            "component_origin":
                "INHERITED_ROUND244_COMPONENT_SATURATED_THROUGH_ROUND250",
            "official_key_ordinal": key_ordinal,
            "official_key_id": key_id,
            "member_Round179_resolved_child_count": len(resolved_ids),
            "member_Round179_resolved_child_row_ids_sha256":
                digest(sorted(resolved_ids)),
            "virtual_stratum_node_count": len(virtual_ids),
            "virtual_stratum_node_ids": virtual_ids,
            "virtual_stratum_node_ids_sha256": digest(virtual_ids),
            "mixed_sheet_edge_count": len(edge_ids),
            "mixed_sheet_edge_ids": edge_ids,
            "mixed_sheet_edge_ids_sha256": digest(edge_ids),
            "materialized_member_count": member_count,
            "new_Round250_wall_chain_edge_count": component_chain_count,
            "seed_known_connectivity_block_count": len(seed_blocks),
            "seed_known_connectivity_block_ids": seed_blocks,
            "virtual_stratum_known_block_incidence_count":
                len(virtual_ids) if seed_blocks else 0,
            "component_exact_key_assignment_credit": 1,
            "certified_known_connectivity_only": True,
            "maximal_physical_component_claimed": False,
            "global_exact_key_fibre_credit": 0,
        }
        exact_row(
            component_by_id[component_id],
            expected,
            f"inherited component:{component_id}",
        )
        expected_component_ids.add(component_id)
        component_ids_by_key[key_id].append(component_id)
        inherited_ids_by_key[key_id].append(component_id)
        if seed_blocks:
            seeded_ids_by_key[key_id].append(component_id)
            seeded_component_count += 1
            seeded_virtual_nodes += len(virtual_ids)
        else:
            unseeded_ids_by_key[key_id].append(component_id)
        member_count_by_key[key_id] += member_count
        origin_histogram[
            "INHERITED_ROUND244_COMPONENT_SATURATED_THROUGH_ROUND250"
        ] += 1
        total_virtual_nodes += len(virtual_ids)
        total_edges += len(edge_ids)
        total_members += member_count

    for root, bulk_ids_unsorted in bulk_ids_by_class.items():
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
        need(len(keys) == 1, f"new class purity:{root}")
        key_ordinal, key_id = next(iter(keys))
        need(
            all(sheet["owner_official_key_id"] == key_id for sheet in sheets),
            f"new sheet purity:{root}",
        )
        virtual_ids = sorted(
            bulk_ids
            + [sheet["wall_sheet_node_id"] for sheet in sheets]
        )
        edge_ids = sorted(
            chain_edges_by_class.get(root, [])
            + [sheet["owner_mixed_sheet_edge_id"] for sheet in sheets]
        )
        component_id = "round250-saturated-wall-component:" + digest([
            bulk_ids,
            [sheet["wall_sheet_node_id"] for sheet in sheets],
        ])
        expected = {
            "mixed_sheet_component_row_id":
                "round250-mixed-sheet-component:"
                + digest([component_id, virtual_ids]),
            "mixed_sheet_quotient_component_id": component_id,
            "component_origin": "ROUND250_NEW_SATURATED_WALL_COMPONENT",
            "official_key_ordinal": key_ordinal,
            "official_key_id": key_id,
            "member_Round179_resolved_child_count": 0,
            "member_Round179_resolved_child_row_ids_sha256": digest([]),
            "virtual_stratum_node_count": len(virtual_ids),
            "virtual_stratum_node_ids": virtual_ids,
            "virtual_stratum_node_ids_sha256": digest(virtual_ids),
            "mixed_sheet_edge_count": len(edge_ids),
            "mixed_sheet_edge_ids": edge_ids,
            "mixed_sheet_edge_ids_sha256": digest(edge_ids),
            "materialized_member_count": len(virtual_ids),
            "new_Round250_wall_chain_edge_count":
                len(chain_edges_by_class.get(root, [])),
            "seed_known_connectivity_block_count": 0,
            "seed_known_connectivity_block_ids": [],
            "virtual_stratum_known_block_incidence_count": 0,
            "component_exact_key_assignment_credit": 1,
            "certified_known_connectivity_only": True,
            "maximal_physical_component_claimed": False,
            "global_exact_key_fibre_credit": 0,
        }
        exact_row(
            component_by_id[component_id],
            expected,
            f"new component:{component_id}",
        )
        expected_component_ids.add(component_id)
        component_ids_by_key[key_id].append(component_id)
        new_ids_by_key[key_id].append(component_id)
        unseeded_ids_by_key[key_id].append(component_id)
        member_count_by_key[key_id] += len(virtual_ids)
        origin_histogram["ROUND250_NEW_SATURATED_WALL_COMPONENT"] += 1
        new_bulk_count += len(bulk_ids)
        new_sheet_count += len(sheets)
        new_size_histogram[len(virtual_ids)] += 1
        new_chain_edges += len(chain_edges_by_class.get(root, []))
        total_virtual_nodes += len(virtual_ids)
        total_edges += len(edge_ids)
        total_members += len(virtual_ids)
    need(
        expected_component_ids == set(component_by_id)
        and len(expected_component_ids) == 82_620,
        "component universe",
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
    need(
        len(prior_fibres) == len(fibre_by_key) == 116,
        "fibre universe",
    )
    component_count_histogram: Counter[int] = Counter()
    fibre_status_histogram: Counter[str] = Counter()
    keys_with_blocks = 0
    keys_with_new_wall = 0
    for key_id, prior in prior_fibres.items():
        component_ids = sorted(component_ids_by_key[key_id])
        inherited_ids = sorted(inherited_ids_by_key[key_id])
        new_ids = sorted(new_ids_by_key[key_id])
        seeded_ids = sorted(seeded_ids_by_key[key_id])
        unseeded_ids = sorted(unseeded_ids_by_key[key_id])
        expected = {
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
            "new_Round250_wall_component_count": len(new_ids),
            "seeded_quotient_component_count": len(seeded_ids),
            "unseeded_quotient_component_count": len(unseeded_ids),
            "materialized_component_member_count":
                member_count_by_key[key_id],
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
        }
        exact_row(fibre_by_key[key_id], expected, f"fibre:{key_id}")
        component_count_histogram[len(component_ids)] += 1
        fibre_status_histogram[prior["frontier_status"]] += 1
        keys_with_blocks += bool(prior["known_connectivity_block_count"])
        keys_with_new_wall += bool(new_ids)

    expected_census = {
        "wall_root_count": 2_640,
        "wall_t_chain_cell_count": 50_576,
        "wall_t_chain_internal_boundary_count": boundary_count,
        "accepted_same_signature_wall_chain_edge_count": len(edge_rows),
        "unaccepted_different_signature_boundary_count":
            len(mismatch_descriptors),
        "different_signature_boundary_commitment_sha256":
            digest(mismatch_descriptors),
        "patch_depth_histogram": dict(sorted(patch_histogram.items())),
        "source_pair_histogram": dict(sorted(source_pair_histogram.items())),
        "exact_common_patch_area_sum": qstr(patch_area_sum),
        "exact_left_corridor_volume_sum": qstr(left_volume_sum),
        "exact_right_corridor_volume_sum": qstr(right_volume_sum),
        "Round249_mixed_sheet_quotient_component_count": 94_444,
        "post_Round250_mixed_sheet_quotient_component_count":
            len(component_rows),
        "Round250_mixed_sheet_quotient_component_reduction":
            94_444 - len(component_rows),
        "component_origin_histogram": dict(sorted(origin_histogram.items())),
        "attached_wall_bulk_node_count": attached_bulk_count,
        "attached_wall_sheet_node_count": attached_sheet_count,
        "attached_wall_node_size_histogram": {
            str(key): value
            for key, value in sorted(attached_size_histogram.items())
        },
        "new_saturated_wall_bulk_node_count": new_bulk_count,
        "new_saturated_wall_sheet_node_count": new_sheet_count,
        "new_saturated_wall_component_size_histogram": {
            str(key): value
            for key, value in sorted(new_size_histogram.items())
        },
        "new_chain_edges_inside_inherited_components":
            inherited_chain_edges,
        "new_chain_edges_inside_new_wall_components": new_chain_edges,
        "cumulative_virtual_stratum_node_count": total_virtual_nodes,
        "Round249_cumulative_mixed_sheet_edge_count": 47_388,
        "cumulative_mixed_sheet_edge_count": total_edges,
        "materialized_component_member_count": total_members,
        "seeded_quotient_component_count": seeded_component_count,
        "unseeded_quotient_component_count":
            len(component_rows) - seeded_component_count,
        "cumulative_virtual_stratum_known_block_incidence_count":
            seeded_virtual_nodes,
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
    need(
        candidate["census"] == expected_census
        and dict(patch_histogram)
        == {
            "t1:base0:p0:s0": 11_184,
            "t1:base1:p0:s0": 640,
        }
        and attached_bulk_count == 14_464
        and attached_sheet_count == 1_216
        and new_bulk_count == 74_472
        and new_sheet_count == 37_144
        and inherited_chain_edges == 11_824
        and new_chain_edges == 0
        and total_virtual_nodes == 133_684
        and total_edges == 59_212
        and total_members == 150_876
        and seeded_component_count == 440
        and seeded_virtual_nodes == 316
        and keys_with_blocks == 24
        and keys_with_new_wall == 92,
        "census",
    )
    scope = candidate["scope_contract"]
    strict = candidate["strict_nonpromotion"]
    need(
        all(scope.values())
        and strict["new_occurrence_known_block_incidence_credit"] == 0
        and strict["maximal_physical_component_credit"] == 0
        and strict["global_exact_key_fibre_credit"] == 0
        and strict["CM2"] == "NO-GO_FOR_CLAIM",
        "scope and nonpromotion",
    )
    return {
        "status": "PASS_INDEPENDENT_ROUND250",
        "verified_wall_t_chain_boundary_count": 47_936,
        "verified_strict_same_signature_patch_edge_count": 11_824,
        "verified_different_signature_boundary_count": 36_112,
        "verified_post_Round250_mixed_sheet_quotient_component_count":
            82_620,
        "verified_Round250_component_reduction": 11_824,
        "verified_cumulative_virtual_stratum_node_count": 133_684,
        "verified_cumulative_mixed_sheet_edge_count": 59_212,
        "verified_exact_key_quotient_fibre_inventory_count": 116,
        "verified_occurrences_without_known_block_incidence": 17_768,
        "verified_globally_exhausted_exact_key_fibre_count": 0,
        "candidate_result_sha256": digest(candidate),
        "producer_imported_or_executed": False,
        "CM2": "NO-GO_FOR_CLAIM",
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
    result = verify()
    document = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    raw = canonical(document) + b"\n"
    if not arguments.no_write:
        safe_write(raw)
    print(result["status"])
    print(json.dumps(result, sort_keys=True))
    print(f"result_sha256={document['result_sha256']}")
    print(f"verification_sha256={hashlib.sha256(raw).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
