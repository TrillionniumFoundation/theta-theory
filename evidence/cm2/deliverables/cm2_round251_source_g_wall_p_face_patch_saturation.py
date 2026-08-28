#!/usr/bin/env python3
"""Materialize strict same-chart wall p-face patches."""

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
OUTPUT = HERE / "cm2_round251_source_g_wall_p_face_patch_saturation_certificate.json"
SCHEMA = "cm2.round251.source-g-wall-p-face-patch-saturation.v1"
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


def certify_p_patch(
    r179: Any,
    registry: dict[str, Any],
    left: dict[str, Any],
    right: dict[str, Any],
) -> tuple[dict[str, Any], list[Q], list[Q], int, int, int, int, int]:
    left_box = left["box"]
    right_box = right["box"]
    fixed = left_box[3]
    t_range = (
        max(left_box[0], right_box[0]),
        min(left_box[1], right_box[1]),
    )
    s_range = (
        max(left_box[4], right_box[4]),
        min(left_box[5], right_box[5]),
    )
    need(
        fixed == right_box[2]
        and t_range[0] < t_range[1]
        and s_range[0] < s_range[1]
        and left["chart"] == right["chart"]
        and left["owner_target"] == right["owner_target"],
        "p-face cell geometry",
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
            cell["chart"],
            atlas_box,
            cell["owner_target"],
            registry,
        )
        if result is None or reasons:
            return None
        return computed_signature(
            result,
            cell["chart"],
            cell["owner_target"],
        )

    for p_depth in range(1, 5):
        left_width = (left_box[3] - left_box[2]) / (2 ** p_depth)
        right_width = (right_box[3] - right_box[2]) / (2 ** p_depth)
        for t_depth in range(0, 5):
            for t_index in endpoint_first_indices(t_depth):
                t0, t1 = subinterval(
                    t_range[0], t_range[1], t_depth, t_index
                )
                for s_depth in range(0, 3):
                    for s_index in endpoint_first_indices(s_depth):
                        s0, s1 = subinterval(
                            s_range[0], s_range[1], s_depth, s_index
                        )
                        left_corridor = [
                            t0,
                            t1,
                            fixed - left_width,
                            fixed,
                            s0,
                            s1,
                        ]
                        right_corridor = [
                            t0,
                            t1,
                            fixed,
                            fixed + right_width,
                            s0,
                            s1,
                        ]
                        refinement_depth = p_depth + t_depth + s_depth
                        label = (
                            "round251-wall-p-face:"
                            f"{left['interface_id']}:{right['interface_id']}:"
                            f"{left['source_row_id']}:{right['source_row_id']}:"
                            f"{p_depth}:{t_depth}:{t_index}:"
                            f"{s_depth}:{s_index}"
                        )
                        left_signature = evaluate(
                            left,
                            left_corridor,
                            refinement_depth,
                            label + ":left",
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
                                p_depth,
                                t_depth,
                                t_index,
                                s_depth,
                                s_index,
                            )
    raise RuntimeError(
        "no strict p-face patch:"
        f"{left['interface_id']}:{right['interface_id']}:"
        f"{left['source_row_id']}:{right['source_row_id']}"
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

    left_roots: dict[tuple[str, str, Q], list[str]] = defaultdict(list)
    right_roots: dict[tuple[str, str, Q], list[str]] = defaultdict(list)
    for interface_id, geometry in root_geometry.items():
        left_roots[(geometry[6], geometry[7], geometry[3])].append(
            interface_id
        )
        right_roots[(geometry[6], geometry[7], geometry[2])].append(
            interface_id
        )
    root_pairs: list[tuple[str, str]] = []
    for key, left_ids in left_roots.items():
        for left_id in left_ids:
            left_geometry = root_geometry[left_id]
            for right_id in right_roots.get(key, []):
                right_geometry = root_geometry[right_id]
                if (
                    left_id != right_id
                    and max(left_geometry[0], right_geometry[0])
                    < min(left_geometry[1], right_geometry[1])
                    and max(left_geometry[4], right_geometry[4])
                    < min(left_geometry[5], right_geometry[5])
                ):
                    root_pairs.append((left_id, right_id))
    root_pairs.sort()
    need(
        len(root_pairs) == len(set(root_pairs)) == 408,
        "same-chart p-face root pairs",
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
    patch_count_by_root_pair: Counter[tuple[str, str]] = Counter()
    patch_depth_histogram: Counter[str] = Counter()
    source_pair_histogram: Counter[str] = Counter()
    exact_patch_area_sum = Q(0)
    exact_left_corridor_volume_sum = Q(0)
    exact_right_corridor_volume_sum = Q(0)

    for left_id, right_id in root_pairs:
        for left in cells_by_interface[left_id]:
            for right in cells_by_interface[right_id]:
                left_box = left["box"]
                right_box = right["box"]
                t0 = max(left_box[0], right_box[0])
                t1 = min(left_box[1], right_box[1])
                s0 = max(left_box[4], right_box[4])
                s1 = min(left_box[5], right_box[5])
                if t0 >= t1 or s0 >= s1:
                    continue
                (
                    signature,
                    left_corridor,
                    right_corridor,
                    p_depth,
                    t_depth,
                    t_index,
                    s_depth,
                    s_index,
                ) = certify_p_patch(r179, registry, left, right)
                signature_hash = digest(signature)
                left_branch = left["signature_map"][signature_hash]
                right_branch = right["signature_map"][signature_hash]
                face_rectangle = [
                    left_corridor[0],
                    left_corridor[1],
                    left_corridor[4],
                    left_corridor[5],
                ]
                edge_id = "round251-wall-p-face-edge:" + digest([
                    left_id,
                    right_id,
                    left["source_row_id"],
                    right["source_row_id"],
                    left_branch["wall_bulk_node_id"],
                    right_branch["wall_bulk_node_id"],
                    [qstr(value) for value in face_rectangle],
                ])
                patch_specs.append({
                    "wall_p_face_edge_id": edge_id,
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
                    "fixed_p_coordinate": qstr(left_corridor[3]),
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
                    "p_dyadic_depth": p_depth,
                    "t_dyadic_depth": t_depth,
                    "t_dyadic_index": t_index,
                    "s_dyadic_depth": s_depth,
                    "s_dyadic_index": s_index,
                    "interval_precision_bits": 256,
                    "same_global_source_chart_identity_transform": [
                        "t_left=t_right",
                        "p_left=p_right",
                        "s_left=s_right",
                    ],
                })
                patch_count_by_root_pair[(left_id, right_id)] += 1
                patch_depth_histogram[
                    f"p{p_depth}:t{t_depth}:{t_index}:"
                    f"s{s_depth}:{s_index}"
                ] += 1
                source_pair_histogram[
                    f"{left['source_kind']}->{right['source_kind']}"
                ] += 1
                exact_patch_area_sum += area(face_rectangle)
                exact_left_corridor_volume_sum += volume(left_corridor)
                exact_right_corridor_volume_sum += volume(right_corridor)
    patch_specs.sort(key=lambda row: row["wall_p_face_edge_id"])
    need(
        len(patch_specs)
        == len({row["wall_p_face_edge_id"] for row in patch_specs})
        == 3_240
        and dict(Counter(patch_count_by_root_pair.values()))
        == {7: 392, 31: 16}
        and dict(patch_depth_histogram) == {
            "p1:t0:0:s0:0": 2_832,
            "p1:t1:0:s0:0": 204,
            "p1:t1:1:s0:0": 204,
        },
        "strict p-face patch census",
    )

    root_rows: list[dict[str, Any]] = []
    for left_id, right_id in root_pairs:
        left_geometry = root_geometry[left_id]
        right_geometry = root_geometry[right_id]
        rectangle = [
            max(left_geometry[0], right_geometry[0]),
            min(left_geometry[1], right_geometry[1]),
            max(left_geometry[4], right_geometry[4]),
            min(left_geometry[5], right_geometry[5]),
        ]
        root_rows.append(closed({
            "wall_p_face_root_pair_id":
                "round251-wall-p-face-root-pair:"
                + digest([left_id, right_id, qstr(left_geometry[3])]),
            "left_Round220_split_interface_id": left_id,
            "right_Round220_split_interface_id": right_id,
            "source_chart": left_geometry[6],
            "owner_target": left_geometry[7],
            "fixed_p_coordinate": qstr(left_geometry[3]),
            "exact_positive_2D_root_common_refinement_rectangle":
                [qstr(value) for value in rectangle],
            "exact_positive_2D_root_common_refinement_area":
                qstr(area(rectangle)),
            "materialized_strict_cell_patch_count":
                patch_count_by_root_pair[(left_id, right_id)],
            "same_global_source_chart_identity_transform": [
                "t_left=t_right",
                "p_left=p_right",
                "s_left=s_right",
            ],
            "cross_chart_transport_used": False,
            "key_equality_used_as_glue": False,
        }))
    root_rows.sort(key=lambda row: row["wall_p_face_root_pair_id"])

    round250 = load_result(
        "cm2_round250_source_g_wall_t_chain_patch_saturation_certificate.json"
    )
    prior_component_rows = round250[
        "formal_post_Round250_mixed_sheet_component_ledger"
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
        len(prior_components) == 82_620
        and len(node_to_prior_component) == 133_684,
        "Round250 quotient binding",
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
        rank_reduction_count == 584
        and redundant_patch_count == 2_656,
        "Round251 quotient rank delta",
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
            f"patch quotient class:{patch['wall_p_face_edge_id']}",
        )
        patch_ids_by_class[root].append(patch["wall_p_face_edge_id"])
    need(len(prior_ids_by_class) == 82_036, "Round251 quotient class count")

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
            if row["member_Round179_resolved_child_count"]
            for resolved_id in resolved_components[
                row["mixed_sheet_quotient_component_id"]
            ]["member_Round179_resolved_child_row_ids"]
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
            "ROUND251_COMPONENT_WITH_INHERITED_ROUND244_SEED"
            if has_inherited
            else "ROUND251_WALL_ONLY_P_FACE_SATURATED_COMPONENT"
        )
        component_id = "round251-p-face-saturated-component:" + digest([
            prior_ids,
            virtual_nodes,
        ])
        member_count = len(resolved_ids) + len(virtual_nodes)
        component_rows.append(closed({
            "mixed_sheet_component_row_id":
                "round251-mixed-sheet-component:"
                + digest([component_id, prior_ids]),
            "mixed_sheet_quotient_component_id": component_id,
            "component_origin": origin,
            "official_key_ordinal": key_ordinal,
            "official_key_id": key_id,
            "constituent_Round250_component_count": len(prior_ids),
            "constituent_Round250_component_ids": prior_ids,
            "constituent_Round250_component_ids_sha256": digest(prior_ids),
            "member_Round179_resolved_child_count": len(resolved_ids),
            "member_Round179_resolved_child_row_ids_sha256":
                digest(resolved_ids),
            "virtual_stratum_node_count": len(virtual_nodes),
            "virtual_stratum_node_ids": virtual_nodes,
            "virtual_stratum_node_ids_sha256": digest(virtual_nodes),
            "mixed_sheet_edge_count": len(mixed_edges),
            "mixed_sheet_edge_ids": mixed_edges,
            "mixed_sheet_edge_ids_sha256": digest(mixed_edges),
            "new_Round251_wall_p_face_edge_count": len(new_edges),
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
        len(component_rows) == 82_036
        and dict(component_origin_histogram) == {
            "ROUND251_COMPONENT_WITH_INHERITED_ROUND244_SEED": 7_932,
            "ROUND251_WALL_ONLY_P_FACE_SATURATED_COMPONENT": 74_104,
        }
        and dict(prior_class_size_histogram)
        == {1: 81_956, 2: 16, 3: 24, 4: 16, 5: 8, 6: 8, 51: 8}
        and dict(seed_block_count_histogram) == {0: 81_596, 1: 440}
        and total_resolved_member_count == 17_192
        and total_virtual_node_count == 133_684
        and total_edge_count == 62_452
        and total_materialized_member_count == 150_876
        and seeded_component_count == 440
        and seeded_virtual_node_count == 316,
        "Round251 component census",
    )

    prior_fibres = {
        row["official_key_id"]: row
        for row in round250[
            "formal_post_Round250_exact_key_quotient_fibre_frontier_ledger"
        ]["rows"]
    }
    need(len(prior_fibres) == 116, "Round250 fibre binding")
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
            f"Round251 fibre partition:{key_id}",
        )
        fibre_rows.append(closed({
            "quotient_fibre_frontier_row_id":
                "round251-quotient-fibre-frontier:" + digest(key_id),
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
            "Round250_mixed_sheet_quotient_component_count":
                prior["post_Round250_mixed_sheet_quotient_component_count"],
            "post_Round251_mixed_sheet_quotient_component_count":
                len(component_ids),
            "Round251_component_reduction":
                prior["post_Round250_mixed_sheet_quotient_component_count"]
                - len(component_ids),
            "mixed_sheet_quotient_component_ids_sha256":
                digest(component_ids),
            "components_with_inherited_Round244_seed_count":
                len(inherited_ids),
            "wall_only_Round251_component_count": len(wall_only_ids),
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
        and keys_with_wall_only_components == 92
        and dict(component_count_histogram) == {
            2: 8,
            12: 4,
            14: 4,
            15: 4,
            19: 4,
            112: 4,
            124: 4,
            316: 8,
            319: 8,
            323: 8,
            324: 4,
            505: 4,
            641: 8,
            646: 8,
            760: 4,
            1_610: 8,
            1_615: 8,
            1_918: 8,
            1_922: 8,
        },
        "Round251 fibre census",
    )

    census = {
        "wall_root_count": 2_640,
        "wall_cell_count": 50_576,
        "same_chart_same_target_p_face_root_pair_count": len(root_rows),
        "exact_positive_area_cell_common_refinement_count": len(patch_rows),
        "strict_same_signature_p_face_patch_count": len(patch_rows),
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
        "Round250_mixed_sheet_quotient_component_count": 82_620,
        "post_Round251_mixed_sheet_quotient_component_count":
            len(component_rows),
        "Round251_mixed_sheet_quotient_component_reduction":
            rank_reduction_count,
        "rank_reducing_p_face_edge_count": rank_reduction_count,
        "quotient_redundant_physical_p_face_edge_count":
            redundant_patch_count,
        "component_origin_histogram":
            dict(sorted(component_origin_histogram.items())),
        "Round250_component_class_size_histogram": {
            str(key): value
            for key, value in sorted(prior_class_size_histogram.items())
        },
        "cumulative_virtual_stratum_node_count":
            total_virtual_node_count,
        "Round250_cumulative_mixed_sheet_edge_count": 59_212,
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
        "post_Round251_occurrences_with_known_block_incidence": 36_200,
        "post_Round251_occurrences_without_known_block_incidence": 17_768,
        "new_occurrence_known_block_incidence_count": 0,
        "maximality_unproved_quotient_component_count":
            len(component_rows),
        "globally_exhausted_exact_key_fibre_count": 0,
        "global_exact_key_disposition_count": 0,
    }
    return {
        "status": (
            "CERTIFIED_3240_STRICT_WALL_P_FACE_PATCHES__"
            "QUOTIENT_COMPONENTS_82620_TO_82036__"
            "116_FIBRE_INVENTORIES_REFRESHED__ZERO_GLOBAL_PROMOTION"
        ),
        "census": census,
        "formal_input_binding": {
            name: PINS[name] for name in sorted(PINS)
        },
        "formal_same_chart_wall_p_face_root_pair_ledger":
            ledger(root_rows, "wall_p_face_root_pair_id"),
        "formal_wall_p_face_positive_patch_edge_ledger":
            ledger(patch_rows, "wall_p_face_edge_id"),
        "formal_post_Round251_mixed_sheet_component_ledger":
            ledger(component_rows, "mixed_sheet_component_row_id"),
        "formal_post_Round251_exact_key_quotient_fibre_frontier_ledger":
            ledger(fibre_rows, "quotient_fibre_frontier_row_id"),
        "scope_contract": {
            "all_408_same_chart_same_target_p_face_root_pairs_are_enumerated":
                True,
            "all_3240_cell_common_refinements_have_strict_256_bit_two_sided_patches":
                True,
            "every_patch_has_equal_closed_ten_field_return_signature":
                True,
            "no_cross_chart_transport_is_used": True,
            "key_equality_is_never_used_as_glue": True,
            "all_584_new_rank_reductions_are_memberwise_exact_key_pure":
                True,
            "all_116_quotient_fibre_inventories_are_refreshed": True,
            "p_face_patch_batch_is_not_component_maximality": True,
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
            "materialize the remaining same-chart wall s-face and cross-root "
            "t-face strict patches, then close the 17768 occurrence deficits "
            "before maximality or global-fibre promotion"
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
