#!/usr/bin/env python3
"""Materialize strict same-chart wall s-face and cross-root t-face patches."""

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
OUTPUT = HERE / "cm2_round252_source_g_wall_s_t_face_patch_saturation_certificate.json"
SCHEMA = "cm2.round252.source-g-wall-s-t-face-patch-saturation.v1"
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
    "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json":
        "fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311",
    "cm2_round251_source_g_wall_p_face_patch_saturation_certificate.json":
        "a1f1d04466585cc8b97fceaa98c1507b293696933af4a58dea3c76d92a0c480f",
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


def subinterval(
    lower: Q,
    upper: Q,
    depth: int,
    index: int,
) -> tuple[Q, Q]:
    width = (upper - lower) / (2 ** depth)
    return lower + index * width, lower + (index + 1) * width


def endpoint_first_indices(depth: int) -> list[int]:
    count = 2 ** depth
    return list(dict.fromkeys([0, count - 1, *range(count)]))


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


def certify_axis_patch(
    r179: Any,
    registry: dict[str, Any],
    left: dict[str, Any],
    right: dict[str, Any],
    axis: str,
) -> tuple[dict[str, Any], list[Q], list[Q], dict[str, int]] | None:
    axis_index = {"t": 0, "p": 1, "s": 2}[axis]
    normal_lo = 2 * axis_index
    normal_hi = normal_lo + 1
    tangential_axes = [index for index in range(3) if index != axis_index]
    left_box = left["box"]
    right_box = right["box"]
    fixed = left_box[normal_hi]
    need(
        fixed == right_box[normal_lo]
        and left["chart"] == right["chart"]
        and left["owner_target"] == right["owner_target"],
        f"{axis}-face cell geometry",
    )
    overlaps = {
        index: (
            max(left_box[2 * index], right_box[2 * index]),
            min(left_box[2 * index + 1], right_box[2 * index + 1]),
        )
        for index in tangential_axes
    }
    need(
        all(lo < hi for lo, hi in overlaps.values()),
        f"positive {axis}-face overlap",
    )

    def evaluate(
        cell: dict[str, Any],
        corridor: list[Q],
        refinement_depth: int,
        label: str,
    ) -> dict[str, Any] | None:
        atlas_box = r179.r174.atlas.AtlasBox(
            *corridor,
            cell["adaptive_depth"] + refinement_depth,
            label,
        )
        result, reasons = r179.r174.certify_signature(
            cell["chart"], atlas_box, cell["owner_target"], registry
        )
        if result is None or reasons:
            return None
        return computed_signature(
            result, cell["chart"], cell["owner_target"]
        )

    first_axis, second_axis = tangential_axes
    for normal_depth in range(1, 5):
        left_width = (
            left_box[normal_hi] - left_box[normal_lo]
        ) / (2 ** normal_depth)
        right_width = (
            right_box[normal_hi] - right_box[normal_lo]
        ) / (2 ** normal_depth)
        for first_depth in range(0, 5):
            for first_index in endpoint_first_indices(first_depth):
                first_interval = subinterval(
                    *overlaps[first_axis], first_depth, first_index
                )
                for second_depth in range(0, 5):
                    for second_index in endpoint_first_indices(second_depth):
                        second_interval = subinterval(
                            *overlaps[second_axis],
                            second_depth,
                            second_index,
                        )
                        intervals = {
                            first_axis: first_interval,
                            second_axis: second_interval,
                        }
                        left_corridor = [Q(0)] * 6
                        right_corridor = [Q(0)] * 6
                        for index in tangential_axes:
                            lo, hi = intervals[index]
                            left_corridor[2 * index:2 * index + 2] = [lo, hi]
                            right_corridor[2 * index:2 * index + 2] = [lo, hi]
                        left_corridor[normal_lo:normal_hi + 1] = [
                            fixed - left_width, fixed
                        ]
                        right_corridor[normal_lo:normal_hi + 1] = [
                            fixed, fixed + right_width
                        ]
                        refinement_depth = (
                            normal_depth + first_depth + second_depth
                        )
                        label = (
                            f"round252-wall-{axis}-face:"
                            f"{left['interface_id']}:{right['interface_id']}:"
                            f"{left['source_row_id']}:{right['source_row_id']}:"
                            f"{normal_depth}:{first_depth}:{first_index}:"
                            f"{second_depth}:{second_index}"
                        )
                        left_signature = evaluate(
                            left, left_corridor, refinement_depth, label + ":left"
                        )
                        if left_signature is None:
                            continue
                        signature_hash = digest(left_signature)
                        if (
                            signature_hash not in left["signature_map"]
                            or signature_hash not in right["signature_map"]
                        ):
                            continue
                        right_signature = evaluate(
                            right,
                            right_corridor,
                            refinement_depth,
                            label + ":right",
                        )
                        if right_signature == left_signature:
                            return (
                                left_signature,
                                left_corridor,
                                right_corridor,
                                {
                                    "normal_depth": normal_depth,
                                    "first_axis": first_axis,
                                    "first_depth": first_depth,
                                    "first_index": first_index,
                                    "second_axis": second_axis,
                                    "second_depth": second_depth,
                                    "second_index": second_index,
                                },
                            )
    return None


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
    round248 = load_result(
        "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json"
    )
    bulk_rows = round248["formal_wall_positive_volume_bulk_ledger"]["rows"]
    bulk_id_by_source_branch = {
        (row["source_partition_row_id"], row["branch_label"]):
            row["wall_bulk_node_id"]
        for row in bulk_rows
    }
    need(
        len(resolved234) == 12_200
        and len(single235) == 38_328
        and len(double236) == 16
        and len(crossing236) == 32
        and len(bulk_id_by_source_branch) == 88_936,
        "wall source binding",
    )

    cells_by_interface: dict[str, list[dict[str, Any]]] = defaultdict(list)

    def add_cell(
        source: dict[str, Any],
        source_kind: str,
        source_row_id: str,
        branches: list[tuple[str, dict[str, Any]]],
    ) -> None:
        signature_map = {
            digest(signature): {
                "branch_label": branch_label,
                "wall_bulk_node_id":
                    bulk_id_by_source_branch[(source_row_id, branch_label)],
                "signature": signature,
            }
            for branch_label, signature in branches
        }
        interface_id = source["Round220_split_interface_id"]
        cells_by_interface[interface_id].append({
            "interface_id": interface_id,
            "source_kind": source_kind,
            "source_row_id": source_row_id,
            "box": box_values(source["box"]),
            "chart": source["chart"],
            "owner_target": source["owner_target"],
            "adaptive_depth": source["adaptive_depth"],
            "signature_map": signature_map,
        })

    for row in resolved234:
        add_cell(
            row,
            "ROUND234_RESOLVED_DESCENDANT",
            row["materialized_row_id"],
            [("RESOLVED_DESCENDANT", row["local_return_signature"])],
        )
    for row in single235:
        add_cell(
            frontiers[row["Round234_frontier_row_id"]],
            "ROUND235_SINGLE_ENDPOINT_GRAPH_CELL",
            row["endpoint_graph_partition_row_id"],
            [
                ("EVENT_ABSENT", row["event_absent_signature"]),
                ("EVENT_PRESENT", row["event_present_signature"]),
            ],
        )
    for row in double236:
        add_cell(
            frontiers[row["Round234_frontier_row_id"]],
            "ROUND236_DOUBLE_ENDPOINT_ARRANGEMENT_CELL",
            row["double_endpoint_partition_row_id"],
            [
                (
                    "SAME_SIGN_EVENT_ABSENT",
                    row["same_sign_event_absent_signature"],
                ),
                (
                    "NEGATIVE_TO_POSITIVE",
                    row["negative_to_positive_signature"],
                ),
                (
                    "POSITIVE_TO_NEGATIVE",
                    row["positive_to_negative_signature"],
                ),
            ],
        )
    for row in crossing236:
        add_cell(
            frontiers[row["Round234_frontier_row_id"]],
            "ROUND236_CROSSING_DISCHARGE_CELL",
            row["crossing_dependency_discharge_row_id"],
            [("WHOLE_CROSSING_BOX", row["local_return_signature"])],
        )
    need(
        len(cells_by_interface) == 2_640
        and sum(len(rows) for rows in cells_by_interface.values()) == 50_576,
        "wall cell universe",
    )

    root_geometry: dict[str, list[Any]] = {}
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
            f"root t-chain:{interface_id}",
        )
        first_box = cells[0]["box"]
        root_geometry[interface_id] = [
            first_box[0],
            cells[-1]["box"][1],
            *first_box[2:],
            cells[0]["chart"],
            cells[0]["owner_target"],
        ]

    root_pairs: list[tuple[str, str, str]] = []
    for axis, axis_index in (("s", 2), ("t", 0)):
        normal_lo = 2 * axis_index
        normal_hi = normal_lo + 1
        tangential_axes = [
            index for index in range(3) if index != axis_index
        ]
        left_roots: dict[tuple[str, str, Q], list[str]] = defaultdict(list)
        right_roots: dict[tuple[str, str, Q], list[str]] = defaultdict(list)
        for interface_id, geometry in root_geometry.items():
            left_roots[(
                geometry[6], geometry[7], geometry[normal_hi]
            )].append(interface_id)
            right_roots[(
                geometry[6], geometry[7], geometry[normal_lo]
            )].append(interface_id)
        for key, left_ids in left_roots.items():
            for left_id in left_ids:
                left_geometry = root_geometry[left_id]
                for right_id in right_roots.get(key, []):
                    right_geometry = root_geometry[right_id]
                    if (
                        left_id != right_id
                        and all(
                            max(
                                left_geometry[2 * index],
                                right_geometry[2 * index],
                            )
                            < min(
                                left_geometry[2 * index + 1],
                                right_geometry[2 * index + 1],
                            )
                            for index in tangential_axes
                        )
                    ):
                        root_pairs.append((axis, left_id, right_id))
    root_pairs.sort()
    need(
        len(root_pairs) == len(set(root_pairs)) == 1_304
        and Counter(axis for axis, _, _ in root_pairs)
        == {"s": 1_048, "t": 256},
        "same-chart s/t-face root pairs",
    )

    del round234, round235, round236, round248, bulk_rows
    gc.collect()

    sys.path.insert(0, str(HERE))
    import cm2_round179_source_g_residual_tube_arrangement as r179

    need(
        Path(r179.__file__).resolve()
        == (HERE / "cm2_round179_source_g_residual_tube_arrangement.py").resolve(),
        "Round179 module identity",
    )
    registry = r179.load_inputs()["registry"]
    ctx.prec = 256

    patch_specs: list[dict[str, Any]] = []
    rejected_specs: list[dict[str, Any]] = []
    candidate_count_by_axis: Counter[str] = Counter()
    patch_count_by_root_pair: Counter[tuple[str, str, str]] = Counter()
    patch_count_by_axis: Counter[str] = Counter()
    patch_depth_histogram: Counter[str] = Counter()
    source_pair_histogram: Counter[str] = Counter()
    exact_patch_area_sum = Q(0)
    exact_left_corridor_volume_sum = Q(0)
    exact_right_corridor_volume_sum = Q(0)

    for axis, left_id, right_id in root_pairs:
        axis_index = {"t": 0, "p": 1, "s": 2}[axis]
        tangential_axes = [
            index for index in range(3) if index != axis_index
        ]
        for left in cells_by_interface[left_id]:
            for right in cells_by_interface[right_id]:
                left_box = left["box"]
                right_box = right["box"]
                if (
                    left_box[2 * axis_index + 1]
                    != right_box[2 * axis_index]
                    or not all(
                    max(left_box[2 * index], right_box[2 * index])
                    < min(
                        left_box[2 * index + 1],
                        right_box[2 * index + 1],
                    )
                    for index in tangential_axes
                    )
                ):
                    continue
                candidate_count_by_axis[axis] += 1
                certified = certify_axis_patch(
                    r179, registry, left, right, axis
                )
                if certified is None:
                    rejected_specs.append(closed({
                        "rejected_axis_face_contact_id":
                            "round252-rejected-axis-face-contact:"
                            + digest([
                                axis,
                                left_id,
                                right_id,
                                left["source_row_id"],
                                right["source_row_id"],
                            ]),
                        "face_axis": axis,
                        "left_Round220_split_interface_id": left_id,
                        "right_Round220_split_interface_id": right_id,
                        "left_source_partition_row_id":
                            left["source_row_id"],
                        "right_source_partition_row_id":
                            right["source_row_id"],
                        "shared_full_return_signature_count": len(
                            set(left["signature_map"])
                            & set(right["signature_map"])
                        ),
                        "disposition":
                            "REJECTED_NO_COMMON_STRICT_TWO_SIDED_"
                            "RETURN_SIGNATURE_CORRIDOR_DEPTH_LE_4",
                        "physical_glue_credit": 0,
                        "key_equality_used_as_glue": False,
                    }))
                    continue
                (
                    signature,
                    left_corridor,
                    right_corridor,
                    depth_data,
                ) = certified
                signature_hash = digest(signature)
                left_branch = left["signature_map"][signature_hash]
                right_branch = right["signature_map"][signature_hash]
                face_rectangle: list[Q] = []
                for index in tangential_axes:
                    face_rectangle.extend(
                        left_corridor[2 * index:2 * index + 2]
                    )
                edge_id = "round252-wall-axis-face-edge:" + digest([
                    axis,
                    left_id,
                    right_id,
                    left["source_row_id"],
                    right["source_row_id"],
                    left_branch["wall_bulk_node_id"],
                    right_branch["wall_bulk_node_id"],
                    [qstr(value) for value in face_rectangle],
                ])
                patch_specs.append({
                    "wall_axis_face_edge_id": edge_id,
                    "face_axis": axis,
                    "left_Round220_split_interface_id": left_id,
                    "right_Round220_split_interface_id": right_id,
                    "left_source_partition_kind": left["source_kind"],
                    "left_source_partition_row_id": left["source_row_id"],
                    "left_branch_label": left_branch["branch_label"],
                    "left_wall_bulk_node_id":
                        left_branch["wall_bulk_node_id"],
                    "right_source_partition_kind": right["source_kind"],
                    "right_source_partition_row_id": right["source_row_id"],
                    "right_branch_label": right_branch["branch_label"],
                    "right_wall_bulk_node_id":
                        right_branch["wall_bulk_node_id"],
                    "source_chart": left["chart"],
                    "owner_target": left["owner_target"],
                    "fixed_normal_coordinate":
                        qstr(left_corridor[2 * axis_index + 1]),
                    "common_return_signature_sha256": signature_hash,
                    "official_key_ordinal": signature["official_key_ordinal"],
                    "official_key_id": signature["official_key_id"],
                    "exact_positive_2D_common_face_rectangle":
                        [qstr(value) for value in face_rectangle],
                    "exact_positive_2D_common_face_area":
                        qstr(area(face_rectangle)),
                    "left_strict_positive_3D_corridor_box":
                        [qstr(value) for value in left_corridor],
                    "left_strict_positive_3D_corridor_volume":
                        qstr(volume(left_corridor)),
                    "right_strict_positive_3D_corridor_box":
                        [qstr(value) for value in right_corridor],
                    "right_strict_positive_3D_corridor_volume":
                        qstr(volume(right_corridor)),
                    "normal_dyadic_depth": depth_data["normal_depth"],
                    "first_tangential_axis":
                        "tps"[depth_data["first_axis"]],
                    "first_tangential_dyadic_depth":
                        depth_data["first_depth"],
                    "first_tangential_dyadic_index":
                        depth_data["first_index"],
                    "second_tangential_axis":
                        "tps"[depth_data["second_axis"]],
                    "second_tangential_dyadic_depth":
                        depth_data["second_depth"],
                    "second_tangential_dyadic_index":
                        depth_data["second_index"],
                    "interval_precision_bits": 256,
                    "same_global_source_chart_identity_transform": [
                        "t_left=t_right",
                        "p_left=p_right",
                        "s_left=s_right",
                    ],
                })
                patch_count_by_root_pair[(axis, left_id, right_id)] += 1
                patch_count_by_axis[axis] += 1
                patch_depth_histogram[
                    f"{axis}:n{depth_data['normal_depth']}:"
                    f"a{depth_data['first_axis']}:"
                    f"{depth_data['first_depth']}:"
                    f"{depth_data['first_index']}:"
                    f"b{depth_data['second_axis']}:"
                    f"{depth_data['second_depth']}:"
                    f"{depth_data['second_index']}"
                ] += 1
                source_pair_histogram[
                    f"{left['source_kind']}->{right['source_kind']}"
                ] += 1
                exact_patch_area_sum += area(face_rectangle)
                exact_left_corridor_volume_sum += volume(left_corridor)
                exact_right_corridor_volume_sum += volume(right_corridor)
    patch_specs.sort(key=lambda row: row["wall_axis_face_edge_id"])
    rejected_specs.sort(
        key=lambda row: row["rejected_axis_face_contact_id"]
    )
    need(
        len(patch_specs)
        == len({row["wall_axis_face_edge_id"] for row in patch_specs})
        and len(rejected_specs)
        == len({
            row["rejected_axis_face_contact_id"]
            for row in rejected_specs
        })
        and len(patch_specs) + len(rejected_specs) == 22_264
        and candidate_count_by_axis == {"s": 22_008, "t": 256}
        and patch_count_by_axis == {"s": 22_008, "t": 8}
        and Counter(row["face_axis"] for row in rejected_specs)
        == {"t": 248},
        "strict s/t-face patch census",
    )

    root_rows: list[dict[str, Any]] = []
    for axis, left_id, right_id in root_pairs:
        left_geometry = root_geometry[left_id]
        right_geometry = root_geometry[right_id]
        axis_index = {"t": 0, "p": 1, "s": 2}[axis]
        tangential_axes = [
            index for index in range(3) if index != axis_index
        ]
        rectangle: list[Q] = []
        for index in tangential_axes:
            rectangle.extend([
                max(
                    left_geometry[2 * index],
                    right_geometry[2 * index],
                ),
                min(
                    left_geometry[2 * index + 1],
                    right_geometry[2 * index + 1],
                ),
            ])
        root_rows.append(closed({
            "wall_axis_face_root_pair_id":
                "round252-wall-axis-face-root-pair:"
                + digest([
                    axis,
                    left_id,
                    right_id,
                    qstr(left_geometry[2 * axis_index + 1]),
                ]),
            "face_axis": axis,
            "left_Round220_split_interface_id": left_id,
            "right_Round220_split_interface_id": right_id,
            "source_chart": left_geometry[6],
            "owner_target": left_geometry[7],
            "fixed_normal_coordinate":
                qstr(left_geometry[2 * axis_index + 1]),
            "exact_positive_2D_root_common_refinement_rectangle":
                [qstr(value) for value in rectangle],
            "exact_positive_2D_root_common_refinement_area":
                qstr(area(rectangle)),
            "materialized_strict_cell_patch_count":
                patch_count_by_root_pair.get((axis, left_id, right_id), 0),
            "same_global_source_chart_identity_transform": [
                "t_left=t_right",
                "p_left=p_right",
                "s_left=s_right",
            ],
            "cross_chart_transport_used": False,
            "key_equality_used_as_glue": False,
        }))
    root_rows.sort(key=lambda row: row["wall_axis_face_root_pair_id"])

    round251 = load_result(
        "cm2_round251_source_g_wall_p_face_patch_saturation_certificate.json"
    )
    prior_component_rows = round251[
        "formal_post_Round251_mixed_sheet_component_ledger"
    ]["rows"]
    prior_components = {
        row["mixed_sheet_quotient_component_id"]: row
        for row in prior_component_rows
    }
    node_to_prior_component = {
        node_id: row["mixed_sheet_quotient_component_id"]
        for row in prior_component_rows
        for node_id in row["virtual_stratum_node_ids"]
    }
    need(
        len(prior_components) == 82_036
        and len(node_to_prior_component) == 133_684,
        "Round251 quotient binding",
    )

    quotient = DisjointSet(list(prior_components))
    rank_reduction_count = 0
    redundant_patch_count = 0
    for patch in patch_specs:
        left_component = node_to_prior_component[
            patch["left_wall_bulk_node_id"]
        ]
        right_component = node_to_prior_component[
            patch["right_wall_bulk_node_id"]
        ]
        reduced = quotient.union(left_component, right_component)
        patch["current_quotient_rank_reduction_credit"] = int(reduced)
        patch["current_quotient_lower_bound_edge_credit"] = 1
        patch["occurrence_known_block_incidence_credit"] = 0
        patch["maximal_physical_component_credit"] = 0
        patch["global_exact_key_fibre_credit"] = 0
        rank_reduction_count += reduced
        redundant_patch_count += not reduced
    patch_rows = [closed(row) for row in patch_specs]
    need(
        rank_reduction_count == 16_296
        and redundant_patch_count == 5_720,
        "Round252 quotient rank delta",
    )

    prior_ids_by_class: dict[str, list[str]] = defaultdict(list)
    for component_id in prior_components:
        prior_ids_by_class[quotient.find(component_id)].append(component_id)
    patch_ids_by_class: dict[str, list[str]] = defaultdict(list)
    for patch in patch_rows:
        root = quotient.find(
            node_to_prior_component[patch["left_wall_bulk_node_id"]]
        )
        need(
            root == quotient.find(
                node_to_prior_component[patch["right_wall_bulk_node_id"]]
            ),
            f"patch quotient class:{patch['wall_axis_face_edge_id']}",
        )
        patch_ids_by_class[root].append(patch["wall_axis_face_edge_id"])
    need(
        len(prior_ids_by_class)
        == len(prior_components) - rank_reduction_count,
        "Round252 quotient class count",
    )

    round244 = load_result(
        "cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json"
    )
    resolved_components = {
        row["resolved_bulk_component_row_id"]: row
        for row in round244["formal_resolved_bulk_component_ledger"]["rows"]
    }
    need(len(resolved_components) == 8_148, "Round244 resolved binding")

    component_rows: list[dict[str, Any]] = []
    component_ids_by_key: dict[str, list[str]] = defaultdict(list)
    inherited_ids_by_key: dict[str, list[str]] = defaultdict(list)
    wall_only_ids_by_key: dict[str, list[str]] = defaultdict(list)
    seeded_ids_by_key: dict[str, list[str]] = defaultdict(list)
    unseeded_ids_by_key: dict[str, list[str]] = defaultdict(list)
    member_count_by_key: Counter[str] = Counter()
    component_origin_histogram: Counter[str] = Counter()
    prior_class_size_histogram: Counter[int] = Counter()
    seed_block_count_histogram: Counter[int] = Counter()
    total_resolved_member_count = 0
    total_virtual_node_count = 0
    total_edge_count = 0
    total_materialized_member_count = 0
    seeded_component_count = 0
    seeded_virtual_node_count = 0

    for root, prior_ids_unsorted in sorted(prior_ids_by_class.items()):
        prior_ids = sorted(prior_ids_unsorted)
        rows = [prior_components[component_id] for component_id in prior_ids]
        keys = {
            (row["official_key_ordinal"], row["official_key_id"])
            for row in rows
        }
        need(len(keys) == 1, f"component key purity:{root}")
        key_ordinal, key_id = next(iter(keys))
        virtual_nodes = sorted(
            node_id
            for row in rows
            for node_id in row["virtual_stratum_node_ids"]
        )
        prior_edges = sorted(
            edge_id
            for row in rows
            for edge_id in row["mixed_sheet_edge_ids"]
        )
        new_edges = sorted(patch_ids_by_class.get(root, []))
        mixed_edges = sorted(prior_edges + new_edges)
        seed_blocks = sorted({
            block_id
            for row in rows
            for block_id in row["seed_known_connectivity_block_ids"]
        })
        resolved_ids = sorted(
            resolved_id
            for row in rows
            for constituent_id in row["constituent_Round250_component_ids"]
            if constituent_id in resolved_components
            for resolved_id in resolved_components[constituent_id][
                "member_Round179_resolved_child_row_ids"
            ]
        )
        need(
            len(virtual_nodes) == len(set(virtual_nodes))
            and len(mixed_edges) == len(set(mixed_edges))
            and len(resolved_ids) == len(set(resolved_ids))
            and sum(
                row["member_Round179_resolved_child_count"]
                for row in rows
            ) == len(resolved_ids),
            f"component member partition:{root}",
        )
        has_inherited = bool(resolved_ids)
        origin = (
            "ROUND252_COMPONENT_WITH_INHERITED_ROUND244_SEED"
            if has_inherited
            else "ROUND252_WALL_ONLY_S_T_FACE_SATURATED_COMPONENT"
        )
        component_id = "round252-axis-face-saturated-component:" + digest([
            prior_ids,
            virtual_nodes,
        ])
        member_count = len(resolved_ids) + len(virtual_nodes)
        component_rows.append(closed({
            "mixed_sheet_component_row_id":
                "round252-mixed-sheet-component:"
                + digest([component_id, prior_ids]),
            "mixed_sheet_quotient_component_id": component_id,
            "component_origin": origin,
            "official_key_ordinal": key_ordinal,
            "official_key_id": key_id,
            "constituent_Round251_component_count": len(prior_ids),
            "constituent_Round251_component_ids": prior_ids,
            "constituent_Round251_component_ids_sha256": digest(prior_ids),
            "member_Round179_resolved_child_count": len(resolved_ids),
            "member_Round179_resolved_child_row_ids_sha256":
                digest(resolved_ids),
            "virtual_stratum_node_count": len(virtual_nodes),
            "virtual_stratum_node_ids": virtual_nodes,
            "virtual_stratum_node_ids_sha256": digest(virtual_nodes),
            "mixed_sheet_edge_count": len(mixed_edges),
            "mixed_sheet_edge_ids": mixed_edges,
            "mixed_sheet_edge_ids_sha256": digest(mixed_edges),
            "new_Round252_wall_axis_face_edge_count": len(new_edges),
            "materialized_member_count": member_count,
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
        if has_inherited:
            inherited_ids_by_key[key_id].append(component_id)
        else:
            wall_only_ids_by_key[key_id].append(component_id)
        if seed_blocks:
            seeded_ids_by_key[key_id].append(component_id)
            seeded_component_count += 1
            seeded_virtual_node_count += len(virtual_nodes)
        else:
            unseeded_ids_by_key[key_id].append(component_id)
        member_count_by_key[key_id] += member_count
        component_origin_histogram[origin] += 1
        prior_class_size_histogram[len(prior_ids)] += 1
        seed_block_count_histogram[len(seed_blocks)] += 1
        total_resolved_member_count += len(resolved_ids)
        total_virtual_node_count += len(virtual_nodes)
        total_edge_count += len(mixed_edges)
        total_materialized_member_count += member_count
    component_rows.sort(key=lambda row: row["mixed_sheet_component_row_id"])
    need(
        len(component_rows) == 65_740
        and dict(component_origin_histogram) == {
            "ROUND252_COMPONENT_WITH_INHERITED_ROUND244_SEED": 7_932,
            "ROUND252_WALL_ONLY_S_T_FACE_SATURATED_COMPONENT": 57_808,
        }
        and dict(prior_class_size_histogram) == {1: 49_444, 2: 16_296}
        and dict(seed_block_count_histogram) == {0: 65_300, 1: 440}
        and total_resolved_member_count == 17_192
        and total_virtual_node_count == 133_684
        and total_edge_count == 62_452 + len(patch_rows)
        and total_materialized_member_count == 150_876
        and seeded_component_count == 440
        and seeded_virtual_node_count == 316,
        "Round252 component census",
    )

    prior_fibres = {
        row["official_key_id"]: row
        for row in round251[
            "formal_post_Round251_exact_key_quotient_fibre_frontier_ledger"
        ]["rows"]
    }
    need(len(prior_fibres) == 116, "Round251 fibre binding")
    fibre_rows: list[dict[str, Any]] = []
    component_count_histogram: Counter[int] = Counter()
    fibre_status_histogram: Counter[str] = Counter()
    keys_with_blocks = 0
    keys_with_wall_only_components = 0
    for key_id, prior in sorted(
        prior_fibres.items(),
        key=lambda item: item[1]["official_key_ordinal"],
    ):
        component_ids = sorted(component_ids_by_key[key_id])
        inherited_ids = sorted(inherited_ids_by_key[key_id])
        wall_only_ids = sorted(wall_only_ids_by_key[key_id])
        seeded_ids = sorted(seeded_ids_by_key[key_id])
        unseeded_ids = sorted(unseeded_ids_by_key[key_id])
        need(
            component_ids
            and inherited_ids
            and len(seeded_ids) + len(unseeded_ids) == len(component_ids),
            f"Round252 fibre partition:{key_id}",
        )
        fibre_rows.append(closed({
            "quotient_fibre_frontier_row_id":
                "round252-quotient-fibre-frontier:" + digest(key_id),
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
            "Round251_mixed_sheet_quotient_component_count":
                prior["post_Round251_mixed_sheet_quotient_component_count"],
            "post_Round252_mixed_sheet_quotient_component_count":
                len(component_ids),
            "Round252_component_reduction":
                prior["post_Round251_mixed_sheet_quotient_component_count"]
                - len(component_ids),
            "mixed_sheet_quotient_component_ids_sha256":
                digest(component_ids),
            "components_with_inherited_Round244_seed_count":
                len(inherited_ids),
            "wall_only_Round252_component_count": len(wall_only_ids),
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
        }))
        component_count_histogram[len(component_ids)] += 1
        fibre_status_histogram[prior["frontier_status"]] += 1
        keys_with_blocks += bool(prior["known_connectivity_block_count"])
        keys_with_wall_only_components += bool(wall_only_ids)
    fibre_rows.sort(key=lambda row: row["quotient_fibre_frontier_row_id"])
    need(
        len(fibre_rows) == 116
        and keys_with_blocks == 24
        and keys_with_wall_only_components <= 92
        and sum(component_count_histogram.values()) == 116,
        "Round252 fibre census",
    )

    census = {
        "wall_root_count": 2_640,
        "wall_cell_count": 50_576,
        "same_chart_same_target_axis_face_root_pair_count": len(root_rows),
        "same_chart_same_target_root_pair_count_by_axis": {
            axis: count
            for axis, count in sorted(
                Counter(row["face_axis"] for row in root_rows).items()
            )
        },
        "exact_positive_area_cell_common_refinement_count": len(patch_rows),
        "strict_same_signature_axis_face_patch_count": len(patch_rows),
        "strict_same_signature_patch_count_by_axis":
            dict(sorted(patch_count_by_axis.items())),
        "rejected_axis_face_contact_count": len(rejected_specs),
        "rejected_axis_face_contact_count_by_axis": {
            axis: count
            for axis, count in sorted(
                Counter(row["face_axis"] for row in rejected_specs).items()
            )
        },
        "rejected_disposition_histogram": dict(sorted(Counter(
            row["disposition"] for row in rejected_specs
        ).items())),
        "patch_count_per_root_pair_histogram": {
            str(key): value
            for key, value in sorted(
                Counter(patch_count_by_root_pair.values()).items()
            )
        },
        "patch_depth_histogram":
            dict(sorted(patch_depth_histogram.items())),
        "source_pair_histogram":
            dict(sorted(source_pair_histogram.items())),
        "exact_common_patch_area_sum": qstr(exact_patch_area_sum),
        "exact_left_corridor_volume_sum":
            qstr(exact_left_corridor_volume_sum),
        "exact_right_corridor_volume_sum":
            qstr(exact_right_corridor_volume_sum),
        "Round251_mixed_sheet_quotient_component_count": 82_036,
        "post_Round252_mixed_sheet_quotient_component_count":
            len(component_rows),
        "Round252_mixed_sheet_quotient_component_reduction":
            rank_reduction_count,
        "rank_reducing_axis_face_edge_count": rank_reduction_count,
        "quotient_redundant_physical_axis_face_edge_count":
            redundant_patch_count,
        "component_origin_histogram":
            dict(sorted(component_origin_histogram.items())),
        "Round251_component_class_size_histogram": {
            str(key): value
            for key, value in sorted(prior_class_size_histogram.items())
        },
        "cumulative_virtual_stratum_node_count":
            total_virtual_node_count,
        "Round251_cumulative_mixed_sheet_edge_count": 62_452,
        "cumulative_mixed_sheet_edge_count": total_edge_count,
        "materialized_component_member_count":
            total_materialized_member_count,
        "seeded_quotient_component_count": seeded_component_count,
        "unseeded_quotient_component_count":
            len(component_rows) - seeded_component_count,
        "cumulative_virtual_stratum_known_block_incidence_count":
            seeded_virtual_node_count,
        "observed_exact_key_count": 116,
        "quotient_fibre_inventory_complete_count": len(fibre_rows),
        "mixed_sheet_quotient_component_count_histogram": {
            str(key): value
            for key, value in sorted(component_count_histogram.items())
        },
        "fibre_frontier_status_histogram":
            dict(sorted(fibre_status_histogram.items())),
        "post_Round252_occurrences_with_known_block_incidence": 36_200,
        "post_Round252_occurrences_without_known_block_incidence": 17_768,
        "new_occurrence_known_block_incidence_count": 0,
        "maximality_unproved_quotient_component_count":
            len(component_rows),
        "globally_exhausted_exact_key_fibre_count": 0,
        "global_exact_key_disposition_count": 0,
    }
    return {
        "status": (
            f"CERTIFIED_{len(patch_rows)}_STRICT_WALL_S_T_FACE_PATCHES__"
            f"QUOTIENT_COMPONENTS_82036_TO_{len(component_rows)}__"
            "116_FIBRE_INVENTORIES_REFRESHED__ZERO_GLOBAL_PROMOTION"
        ),
        "census": census,
        "formal_input_binding": {
            name: PINS[name] for name in sorted(PINS)
        },
        "formal_same_chart_wall_axis_face_root_pair_ledger":
            ledger(root_rows, "wall_axis_face_root_pair_id"),
        "formal_wall_axis_face_positive_patch_edge_ledger":
            ledger(patch_rows, "wall_axis_face_edge_id"),
        "formal_rejected_axis_face_contact_ledger":
            ledger(rejected_specs, "rejected_axis_face_contact_id"),
        "formal_post_Round252_mixed_sheet_component_ledger":
            ledger(component_rows, "mixed_sheet_component_row_id"),
        "formal_post_Round252_exact_key_quotient_fibre_frontier_ledger":
            ledger(fibre_rows, "quotient_fibre_frontier_row_id"),
        "scope_contract": {
            "all_1304_same_chart_same_target_s_t_face_root_pairs_are_enumerated":
                True,
            "all_22264_cell_common_refinements_have_strict_256_bit_two_sided_patches":
                False,
            "all_22264_cell_contacts_are_reconciled_as_accepted_or_fail_closed":
                True,
            "all_248_rejected_t_face_contacts_have_zero_physical_glue_credit":
                True,
            "every_patch_has_equal_closed_ten_field_return_signature":
                True,
            "no_cross_chart_transport_is_used": True,
            "key_equality_is_never_used_as_glue": True,
            "all_new_rank_reductions_are_memberwise_exact_key_pure":
                True,
            "all_116_quotient_fibre_inventories_are_refreshed": True,
            "s_t_face_patch_batch_is_not_component_maximality": True,
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
            "close the 17768 Round179/Round204/Round208 occurrence deficits "
            "against the saturated key-pure quotient before maximality or "
            "global-fibre promotion"
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
