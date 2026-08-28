#!/usr/bin/env python3
"""Independently verify Round251 wall p-face patch saturation."""

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
    / "cm2_round251_source_g_wall_p_face_patch_saturation_verification.json"
)
SCHEMA = "cm2.round251.source-g-wall-p-face-patch-saturation.verification.v1"
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
    "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json":
        "fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311",
    "cm2_round250_source_g_wall_t_chain_patch_saturation_certificate.json":
        "07eb8ab4f5fbcec7df4a891f3e55b3990c8400a01bbbff8950f05519e886ca8a",
}
PINS = {
    **SOURCE_PINS,
    "cm2_round251_source_g_wall_p_face_patch_saturation.py":
        "8ab8fe59c48fa03e33e8d6c607a52958d07f120eef8b04f3abf6f9eb118c03e1",
    "cm2_round251_source_g_wall_p_face_patch_saturation_certificate.json":
        "a1f1d04466585cc8b97fceaa98c1507b293696933af4a58dea3c76d92a0c480f",
}
MAXIMUM_BYTES = {
    name: 5_000_000 if name.endswith(".py") or "manifest" in name
    else 400_000_000
    for name in PINS
}


def require(value: bool, label: str) -> None:
    if not value:
        raise RuntimeError(label)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode()


def hash_object(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def rational_text(value: Q) -> str:
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def pinned_bytes(name: str) -> bytes:
    path = HERE / name
    info = path.lstat()
    require(
        stat.S_ISREG(info.st_mode)
        and not path.is_symlink()
        and info.st_nlink == 1
        and 0 < info.st_size <= MAXIMUM_BYTES[name],
        f"regular:{name}",
    )
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == PINS[name], f"pin:{name}")
    return raw


def pinned_result(name: str) -> dict[str, Any]:
    document = json.loads(pinned_bytes(name))
    require(
        set(document) == {"schema", "result", "result_sha256"}
        and hash_object(document["result"]) == document["result_sha256"],
        f"envelope:{name}",
    )
    return document["result"]


def unpack_rows(
    document: dict[str, Any],
    table: str,
) -> list[dict[str, Any]]:
    columns = document["row_column_schemas"][table]
    return [
        dict(zip(columns, packed, strict=True))
        for packed in document[table]
    ]


def close_row(row: dict[str, Any]) -> dict[str, Any]:
    result = dict(row)
    result["row_sha256"] = hash_object(result)
    return result


def make_ledger(
    rows: list[dict[str, Any]],
    id_field: str,
) -> dict[str, Any]:
    require(
        len(rows) == len({row[id_field] for row in rows}),
        f"unique:{id_field}",
    )
    return {
        "row_count": len(rows),
        "rows_sha256": hash_object(rows),
        "row_ids_sha256": hash_object([row[id_field] for row in rows]),
        "row_hashes_sha256":
            hash_object([row["row_sha256"] for row in rows]),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }


def validate_ledger(
    value: dict[str, Any],
    id_field: str,
) -> list[dict[str, Any]]:
    rows = value["rows"]
    row_ids = [row[id_field] for row in rows]
    require(
        value == make_ledger(rows, id_field)
        and row_ids == sorted(row_ids)
        and all(
            row["row_sha256"]
            == hash_object({
                key: item
                for key, item in row.items()
                if key != "row_sha256"
            })
            for row in rows
        ),
        f"ledger:{id_field}",
    )
    return rows


def rational_box(values: list[str]) -> list[Q]:
    box = [Q(value) for value in values]
    require(
        len(box) == 6
        and box[0] < box[1]
        and box[2] < box[3]
        and box[4] < box[5],
        "positive box",
    )
    return box


def box_volume(box: list[Q]) -> Q:
    return (
        (box[1] - box[0])
        * (box[3] - box[2])
        * (box[5] - box[4])
    )


def rectangle_area(rectangle: list[Q]) -> Q:
    require(
        len(rectangle) == 4
        and rectangle[0] < rectangle[1]
        and rectangle[2] < rectangle[3],
        "positive rectangle",
    )
    return (
        (rectangle[1] - rectangle[0])
        * (rectangle[3] - rectangle[2])
    )


def dyadic_interval(
    lower: Q,
    upper: Q,
    depth: int,
    index: int,
) -> tuple[Q, Q]:
    width = (upper - lower) / (2 ** depth)
    return lower + index * width, lower + (index + 1) * width


def endpoint_first(depth: int) -> list[int]:
    count = 2 ** depth
    return list(dict.fromkeys([0, count - 1, *range(count)]))


def kernel_signature(
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


class Partition:
    def __init__(self, values: list[str]) -> None:
        self.parent = {value: value for value in values}

    def root(self, value: str) -> str:
        while self.parent[value] != value:
            self.parent[value] = self.parent[self.parent[value]]
            value = self.parent[value]
        return value

    def join(self, left: str, right: str) -> bool:
        left_root = self.root(left)
        right_root = self.root(right)
        if left_root == right_root:
            return False
        lower, upper = sorted((left_root, right_root))
        self.parent[upper] = lower
        return True


def independent_patch_search(
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
    require(
        fixed == right_box[2]
        and t_range[0] < t_range[1]
        and s_range[0] < s_range[1]
        and left["chart"] == right["chart"]
        and left["owner_target"] == right["owner_target"],
        "independent p-face geometry",
    )

    def evaluate(
        cell: dict[str, Any],
        corridor: list[Q],
        added_depth: int,
        label: str,
    ) -> dict[str, Any] | None:
        atlas_box = r179.r174.atlas.AtlasBox(
            *corridor,
            cell["adaptive_depth"] + added_depth,
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
        return kernel_signature(
            result,
            cell["chart"],
            cell["owner_target"],
        )

    for normal_depth in range(1, 5):
        left_width = (
            left_box[3] - left_box[2]
        ) / (2 ** normal_depth)
        right_width = (
            right_box[3] - right_box[2]
        ) / (2 ** normal_depth)
        for t_depth in range(0, 5):
            for t_index in endpoint_first(t_depth):
                t0, t1 = dyadic_interval(
                    t_range[0], t_range[1], t_depth, t_index
                )
                for s_depth in range(0, 3):
                    for s_index in endpoint_first(s_depth):
                        s0, s1 = dyadic_interval(
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
                        added_depth = normal_depth + t_depth + s_depth
                        label = (
                            "round251-verifier-p-face:"
                            f"{left['interface_id']}:{right['interface_id']}:"
                            f"{left['source_row_id']}:{right['source_row_id']}:"
                            f"{normal_depth}:{t_depth}:{t_index}:"
                            f"{s_depth}:{s_index}"
                        )
                        left_signature = evaluate(
                            left,
                            left_corridor,
                            added_depth,
                            label + ":left",
                        )
                        if left_signature is None:
                            continue
                        signature_hash = hash_object(left_signature)
                        if (
                            signature_hash not in left["signature_map"]
                            or signature_hash not in right["signature_map"]
                        ):
                            continue
                        right_signature = evaluate(
                            right,
                            right_corridor,
                            added_depth,
                            label + ":right",
                        )
                        if right_signature == left_signature:
                            return (
                                left_signature,
                                left_corridor,
                                right_corridor,
                                normal_depth,
                                t_depth,
                                t_index,
                                s_depth,
                                s_index,
                            )
    raise RuntimeError(
        "independent patch miss:"
        f"{left['interface_id']}:{right['interface_id']}:"
        f"{left['source_row_id']}:{right['source_row_id']}"
    )


def verify() -> dict[str, Any]:
    for name in PINS:
        pinned_bytes(name)
    candidate_document = json.loads(pinned_bytes(
        "cm2_round251_source_g_wall_p_face_patch_saturation_certificate.json"
    ))
    require(
        set(candidate_document) == {"schema", "result", "result_sha256"}
        and candidate_document["schema"]
        == "cm2.round251.source-g-wall-p-face-patch-saturation.v1"
        and hash_object(candidate_document["result"])
        == candidate_document["result_sha256"],
        "candidate envelope",
    )
    candidate = candidate_document["result"]
    validate_ledger(
        candidate["formal_same_chart_wall_p_face_root_pair_ledger"],
        "wall_p_face_root_pair_id",
    )
    validate_ledger(
        candidate["formal_wall_p_face_positive_patch_edge_ledger"],
        "wall_p_face_edge_id",
    )
    validate_ledger(
        candidate["formal_post_Round251_mixed_sheet_component_ledger"],
        "mixed_sheet_component_row_id",
    )
    validate_ledger(
        candidate[
            "formal_post_Round251_exact_key_quotient_fibre_frontier_ledger"
        ],
        "quotient_fibre_frontier_row_id",
    )

    round234 = pinned_result(
        "cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json"
    )
    frontiers = {
        row["frontier_row_id"]: row
        for row in round234["depth6_frontier_rows"]
    }
    resolved234 = round234["resolved_descendant_rows"]
    round235 = pinned_result(
        "cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json"
    )
    single235 = round235["single_endpoint_graph_partition_rows"]
    round236 = pinned_result(
        "cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json"
    )
    double236 = round236["double_endpoint_partition_rows"]
    crossing236 = round236["crossing_dependency_discharge_rows"]
    round248 = pinned_result(
        "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json"
    )
    bulk_id = {
        (row["source_partition_row_id"], row["branch_label"]):
            row["wall_bulk_node_id"]
        for row in round248[
            "formal_wall_positive_volume_bulk_ledger"
        ]["rows"]
    }
    require(
        len(resolved234) == 12_200
        and len(single235) == 38_328
        and len(double236) == 16
        and len(crossing236) == 32
        and len(bulk_id) == 88_936,
        "source census",
    )

    cells: dict[str, list[dict[str, Any]]] = defaultdict(list)

    def register(
        source: dict[str, Any],
        source_kind: str,
        source_row_id: str,
        branches: list[tuple[str, dict[str, Any]]],
    ) -> None:
        signature_map = {
            hash_object(signature): {
                "branch_label": branch,
                "wall_bulk_node_id": bulk_id[(source_row_id, branch)],
                "signature": signature,
            }
            for branch, signature in branches
        }
        interface_id = source["Round220_split_interface_id"]
        cells[interface_id].append({
            "interface_id": interface_id,
            "source_kind": source_kind,
            "source_row_id": source_row_id,
            "box": rational_box(source["box"]),
            "chart": source["chart"],
            "owner_target": source["owner_target"],
            "adaptive_depth": source["adaptive_depth"],
            "signature_map": signature_map,
        })

    for row in resolved234:
        register(
            row,
            "ROUND234_RESOLVED_DESCENDANT",
            row["materialized_row_id"],
            [("RESOLVED_DESCENDANT", row["local_return_signature"])],
        )
    for row in single235:
        register(
            frontiers[row["Round234_frontier_row_id"]],
            "ROUND235_SINGLE_ENDPOINT_GRAPH_CELL",
            row["endpoint_graph_partition_row_id"],
            [
                ("EVENT_ABSENT", row["event_absent_signature"]),
                ("EVENT_PRESENT", row["event_present_signature"]),
            ],
        )
    for row in double236:
        register(
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
        register(
            frontiers[row["Round234_frontier_row_id"]],
            "ROUND236_CROSSING_DISCHARGE_CELL",
            row["crossing_dependency_discharge_row_id"],
            [("WHOLE_CROSSING_BOX", row["local_return_signature"])],
        )
    require(
        len(cells) == 2_640
        and sum(len(rows) for rows in cells.values()) == 50_576,
        "independent wall cell universe",
    )

    roots: dict[str, list[Any]] = {}
    for interface_id, rows in cells.items():
        rows.sort(
            key=lambda row: (
                row["box"][0],
                row["box"][1],
                row["source_row_id"],
            )
        )
        require(
            all(
                left["box"][1] == right["box"][0]
                and left["box"][2:] == right["box"][2:]
                for left, right in zip(rows, rows[1:])
            ),
            f"independent t-chain:{interface_id}",
        )
        first = rows[0]["box"]
        roots[interface_id] = [
            first[0],
            rows[-1]["box"][1],
            *first[2:],
            rows[0]["chart"],
            rows[0]["owner_target"],
        ]
    lower_side: dict[tuple[str, str, Q], list[str]] = defaultdict(list)
    upper_side: dict[tuple[str, str, Q], list[str]] = defaultdict(list)
    for interface_id, geometry in roots.items():
        lower_side[(geometry[6], geometry[7], geometry[3])].append(
            interface_id
        )
        upper_side[(geometry[6], geometry[7], geometry[2])].append(
            interface_id
        )
    root_pairs: list[tuple[str, str]] = []
    for key, left_ids in lower_side.items():
        for left_id in left_ids:
            left_geometry = roots[left_id]
            for right_id in upper_side.get(key, []):
                right_geometry = roots[right_id]
                if (
                    left_id != right_id
                    and max(left_geometry[0], right_geometry[0])
                    < min(left_geometry[1], right_geometry[1])
                    and max(left_geometry[4], right_geometry[4])
                    < min(left_geometry[5], right_geometry[5])
                ):
                    root_pairs.append((left_id, right_id))
    root_pairs.sort()
    require(
        len(root_pairs) == len(set(root_pairs)) == 408,
        "independent root-pair census",
    )

    del round234, round235, round236, round248
    gc.collect()

    sys.path.insert(0, str(HERE))
    import cm2_round179_source_g_residual_tube_arrangement as r179

    require(
        Path(r179.__file__).resolve()
        == (HERE / "cm2_round179_source_g_residual_tube_arrangement.py").resolve(),
        "independent Round179 identity",
    )
    registry = r179.load_inputs()["registry"]
    ctx.prec = 256

    patch_specs: list[dict[str, Any]] = []
    per_root: Counter[tuple[str, str]] = Counter()
    depth_histogram: Counter[str] = Counter()
    source_histogram: Counter[str] = Counter()
    area_sum = Q(0)
    left_volume_sum = Q(0)
    right_volume_sum = Q(0)
    for left_id, right_id in root_pairs:
        for left in cells[left_id]:
            for right in cells[right_id]:
                left_box = left["box"]
                right_box = right["box"]
                if (
                    max(left_box[0], right_box[0])
                    >= min(left_box[1], right_box[1])
                    or max(left_box[4], right_box[4])
                    >= min(left_box[5], right_box[5])
                ):
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
                ) = independent_patch_search(
                    r179,
                    registry,
                    left,
                    right,
                )
                signature_hash = hash_object(signature)
                left_branch = left["signature_map"][signature_hash]
                right_branch = right["signature_map"][signature_hash]
                rectangle = [
                    left_corridor[0],
                    left_corridor[1],
                    left_corridor[4],
                    left_corridor[5],
                ]
                edge_id = "round251-wall-p-face-edge:" + hash_object([
                    left_id,
                    right_id,
                    left["source_row_id"],
                    right["source_row_id"],
                    left_branch["wall_bulk_node_id"],
                    right_branch["wall_bulk_node_id"],
                    [rational_text(value) for value in rectangle],
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
                    "right_source_partition_row_id":
                        right["source_row_id"],
                    "right_branch_label": right_branch["branch_label"],
                    "right_wall_bulk_node_id":
                        right_branch["wall_bulk_node_id"],
                    "source_chart": left["chart"],
                    "owner_target": left["owner_target"],
                    "fixed_p_coordinate": rational_text(left_corridor[3]),
                    "common_return_signature_sha256": signature_hash,
                    "official_key_ordinal":
                        signature["official_key_ordinal"],
                    "official_key_id": signature["official_key_id"],
                    "exact_positive_2D_common_face_rectangle":
                        [rational_text(value) for value in rectangle],
                    "exact_positive_2D_common_face_area":
                        rational_text(rectangle_area(rectangle)),
                    "left_strict_positive_3D_corridor_box":
                        [rational_text(value) for value in left_corridor],
                    "left_strict_positive_3D_corridor_volume":
                        rational_text(box_volume(left_corridor)),
                    "right_strict_positive_3D_corridor_box":
                        [rational_text(value) for value in right_corridor],
                    "right_strict_positive_3D_corridor_volume":
                        rational_text(box_volume(right_corridor)),
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
                per_root[(left_id, right_id)] += 1
                depth_histogram[
                    f"p{p_depth}:t{t_depth}:{t_index}:"
                    f"s{s_depth}:{s_index}"
                ] += 1
                source_histogram[
                    f"{left['source_kind']}->{right['source_kind']}"
                ] += 1
                area_sum += rectangle_area(rectangle)
                left_volume_sum += box_volume(left_corridor)
                right_volume_sum += box_volume(right_corridor)
    patch_specs.sort(key=lambda row: row["wall_p_face_edge_id"])
    require(
        len(patch_specs) == 3_240
        and dict(Counter(per_root.values())) == {7: 392, 31: 16}
        and dict(depth_histogram) == {
            "p1:t0:0:s0:0": 2_832,
            "p1:t1:0:s0:0": 204,
            "p1:t1:1:s0:0": 204,
        },
        "independent patch census",
    )

    root_rows: list[dict[str, Any]] = []
    for left_id, right_id in root_pairs:
        left_geometry = roots[left_id]
        right_geometry = roots[right_id]
        rectangle = [
            max(left_geometry[0], right_geometry[0]),
            min(left_geometry[1], right_geometry[1]),
            max(left_geometry[4], right_geometry[4]),
            min(left_geometry[5], right_geometry[5]),
        ]
        root_rows.append(close_row({
            "wall_p_face_root_pair_id":
                "round251-wall-p-face-root-pair:"
                + hash_object([
                    left_id,
                    right_id,
                    rational_text(left_geometry[3]),
                ]),
            "left_Round220_split_interface_id": left_id,
            "right_Round220_split_interface_id": right_id,
            "source_chart": left_geometry[6],
            "owner_target": left_geometry[7],
            "fixed_p_coordinate": rational_text(left_geometry[3]),
            "exact_positive_2D_root_common_refinement_rectangle":
                [rational_text(value) for value in rectangle],
            "exact_positive_2D_root_common_refinement_area":
                rational_text(rectangle_area(rectangle)),
            "materialized_strict_cell_patch_count":
                per_root[(left_id, right_id)],
            "same_global_source_chart_identity_transform": [
                "t_left=t_right",
                "p_left=p_right",
                "s_left=s_right",
            ],
            "cross_chart_transport_used": False,
            "key_equality_used_as_glue": False,
        }))
    root_rows.sort(key=lambda row: row["wall_p_face_root_pair_id"])

    round250 = pinned_result(
        "cm2_round250_source_g_wall_t_chain_patch_saturation_certificate.json"
    )
    prior_rows = round250[
        "formal_post_Round250_mixed_sheet_component_ledger"
    ]["rows"]
    prior = {
        row["mixed_sheet_quotient_component_id"]: row
        for row in prior_rows
    }
    node_component = {
        node_id: row["mixed_sheet_quotient_component_id"]
        for row in prior_rows
        for node_id in row["virtual_stratum_node_ids"]
    }
    require(
        len(prior) == 82_620 and len(node_component) == 133_684,
        "independent Round250 quotient binding",
    )
    partition = Partition(list(prior))
    rank_delta = 0
    redundant = 0
    for patch in patch_specs:
        reduced = partition.join(
            node_component[patch["left_wall_bulk_node_id"]],
            node_component[patch["right_wall_bulk_node_id"]],
        )
        patch["current_quotient_rank_reduction_credit"] = int(reduced)
        patch["current_quotient_lower_bound_edge_credit"] = 1
        patch["occurrence_known_block_incidence_credit"] = 0
        patch["maximal_physical_component_credit"] = 0
        patch["global_exact_key_fibre_credit"] = 0
        rank_delta += reduced
        redundant += not reduced
    patch_rows = [close_row(row) for row in patch_specs]
    require(
        rank_delta == 584 and redundant == 2_656,
        "independent quotient delta",
    )

    prior_by_class: dict[str, list[str]] = defaultdict(list)
    for component_id in prior:
        prior_by_class[partition.root(component_id)].append(component_id)
    patch_by_class: dict[str, list[str]] = defaultdict(list)
    for patch in patch_rows:
        root = partition.root(
            node_component[patch["left_wall_bulk_node_id"]]
        )
        require(
            root == partition.root(
                node_component[patch["right_wall_bulk_node_id"]]
            ),
            f"independent patch class:{patch['wall_p_face_edge_id']}",
        )
        patch_by_class[root].append(patch["wall_p_face_edge_id"])
    require(len(prior_by_class) == 82_036, "independent class count")

    round244 = pinned_result(
        "cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json"
    )
    resolved_components = {
        row["resolved_bulk_component_row_id"]: row
        for row in round244["formal_resolved_bulk_component_ledger"]["rows"]
    }
    require(len(resolved_components) == 8_148, "Round244 binding")

    component_rows: list[dict[str, Any]] = []
    component_ids_by_key: dict[str, list[str]] = defaultdict(list)
    inherited_ids_by_key: dict[str, list[str]] = defaultdict(list)
    wall_only_ids_by_key: dict[str, list[str]] = defaultdict(list)
    seeded_ids_by_key: dict[str, list[str]] = defaultdict(list)
    unseeded_ids_by_key: dict[str, list[str]] = defaultdict(list)
    member_count_by_key: Counter[str] = Counter()
    origin_histogram: Counter[str] = Counter()
    class_size_histogram: Counter[int] = Counter()
    block_count_histogram: Counter[int] = Counter()
    total_resolved = 0
    total_virtual = 0
    total_edges = 0
    total_members = 0
    seeded_count = 0
    seeded_virtual = 0
    for root, prior_ids_unsorted in sorted(prior_by_class.items()):
        prior_ids = sorted(prior_ids_unsorted)
        rows = [prior[component_id] for component_id in prior_ids]
        keys = {
            (row["official_key_ordinal"], row["official_key_id"])
            for row in rows
        }
        require(len(keys) == 1, f"independent key purity:{root}")
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
        new_edges = sorted(patch_by_class.get(root, []))
        mixed_edges = sorted(prior_edges + new_edges)
        blocks = sorted({
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
        require(
            len(virtual_nodes) == len(set(virtual_nodes))
            and len(mixed_edges) == len(set(mixed_edges))
            and len(resolved_ids) == len(set(resolved_ids))
            and sum(
                row["member_Round179_resolved_child_count"]
                for row in rows
            ) == len(resolved_ids),
            f"independent member partition:{root}",
        )
        inherited = bool(resolved_ids)
        origin = (
            "ROUND251_COMPONENT_WITH_INHERITED_ROUND244_SEED"
            if inherited
            else "ROUND251_WALL_ONLY_P_FACE_SATURATED_COMPONENT"
        )
        component_id = (
            "round251-p-face-saturated-component:"
            + hash_object([prior_ids, virtual_nodes])
        )
        member_count = len(resolved_ids) + len(virtual_nodes)
        component_rows.append(close_row({
            "mixed_sheet_component_row_id":
                "round251-mixed-sheet-component:"
                + hash_object([component_id, prior_ids]),
            "mixed_sheet_quotient_component_id": component_id,
            "component_origin": origin,
            "official_key_ordinal": key_ordinal,
            "official_key_id": key_id,
            "constituent_Round250_component_count": len(prior_ids),
            "constituent_Round250_component_ids": prior_ids,
            "constituent_Round250_component_ids_sha256":
                hash_object(prior_ids),
            "member_Round179_resolved_child_count": len(resolved_ids),
            "member_Round179_resolved_child_row_ids_sha256":
                hash_object(resolved_ids),
            "virtual_stratum_node_count": len(virtual_nodes),
            "virtual_stratum_node_ids": virtual_nodes,
            "virtual_stratum_node_ids_sha256":
                hash_object(virtual_nodes),
            "mixed_sheet_edge_count": len(mixed_edges),
            "mixed_sheet_edge_ids": mixed_edges,
            "mixed_sheet_edge_ids_sha256": hash_object(mixed_edges),
            "new_Round251_wall_p_face_edge_count": len(new_edges),
            "materialized_member_count": member_count,
            "seed_known_connectivity_block_count": len(blocks),
            "seed_known_connectivity_block_ids": blocks,
            "virtual_stratum_known_block_incidence_count":
                len(virtual_nodes) if blocks else 0,
            "component_exact_key_assignment_credit": 1,
            "certified_known_connectivity_only": True,
            "maximal_physical_component_claimed": False,
            "global_exact_key_fibre_credit": 0,
        }))
        component_ids_by_key[key_id].append(component_id)
        if inherited:
            inherited_ids_by_key[key_id].append(component_id)
        else:
            wall_only_ids_by_key[key_id].append(component_id)
        if blocks:
            seeded_ids_by_key[key_id].append(component_id)
            seeded_count += 1
            seeded_virtual += len(virtual_nodes)
        else:
            unseeded_ids_by_key[key_id].append(component_id)
        member_count_by_key[key_id] += member_count
        origin_histogram[origin] += 1
        class_size_histogram[len(prior_ids)] += 1
        block_count_histogram[len(blocks)] += 1
        total_resolved += len(resolved_ids)
        total_virtual += len(virtual_nodes)
        total_edges += len(mixed_edges)
        total_members += member_count
    component_rows.sort(key=lambda row: row["mixed_sheet_component_row_id"])
    require(
        len(component_rows) == 82_036
        and dict(origin_histogram) == {
            "ROUND251_COMPONENT_WITH_INHERITED_ROUND244_SEED": 7_932,
            "ROUND251_WALL_ONLY_P_FACE_SATURATED_COMPONENT": 74_104,
        }
        and dict(class_size_histogram)
        == {1: 81_956, 2: 16, 3: 24, 4: 16, 5: 8, 6: 8, 51: 8}
        and dict(block_count_histogram) == {0: 81_596, 1: 440}
        and total_resolved == 17_192
        and total_virtual == 133_684
        and total_edges == 62_452
        and total_members == 150_876
        and seeded_count == 440
        and seeded_virtual == 316,
        "independent component census",
    )

    prior_fibres = {
        row["official_key_id"]: row
        for row in round250[
            "formal_post_Round250_exact_key_quotient_fibre_frontier_ledger"
        ]["rows"]
    }
    require(len(prior_fibres) == 116, "independent fibre binding")
    fibre_rows: list[dict[str, Any]] = []
    component_count_histogram: Counter[int] = Counter()
    status_histogram: Counter[str] = Counter()
    keys_with_blocks = 0
    keys_with_wall = 0
    for key_id, prior_fibre in sorted(
        prior_fibres.items(),
        key=lambda item: item[1]["official_key_ordinal"],
    ):
        component_ids = sorted(component_ids_by_key[key_id])
        inherited_ids = sorted(inherited_ids_by_key[key_id])
        wall_ids = sorted(wall_only_ids_by_key[key_id])
        seeded_ids = sorted(seeded_ids_by_key[key_id])
        unseeded_ids = sorted(unseeded_ids_by_key[key_id])
        require(
            component_ids
            and inherited_ids
            and len(seeded_ids) + len(unseeded_ids) == len(component_ids),
            f"independent fibre partition:{key_id}",
        )
        fibre_rows.append(close_row({
            "quotient_fibre_frontier_row_id":
                "round251-quotient-fibre-frontier:" + hash_object(key_id),
            "official_key_ordinal": prior_fibre["official_key_ordinal"],
            "official_key_id": key_id,
            "official_key_row": prior_fibre["official_key_row"],
            "local_occurrence_count": prior_fibre["local_occurrence_count"],
            "occurrences_with_known_block_incidence":
                prior_fibre["occurrences_with_known_block_incidence"],
            "occurrences_without_known_block_incidence":
                prior_fibre["occurrences_without_known_block_incidence"],
            "occurrence_ids_sha256": prior_fibre["occurrence_ids_sha256"],
            "unattached_occurrence_ids_sha256":
                prior_fibre["unattached_occurrence_ids_sha256"],
            "unattached_occurrence_gauge_histogram":
                prior_fibre["unattached_occurrence_gauge_histogram"],
            "Round250_mixed_sheet_quotient_component_count":
                prior_fibre[
                    "post_Round250_mixed_sheet_quotient_component_count"
                ],
            "post_Round251_mixed_sheet_quotient_component_count":
                len(component_ids),
            "Round251_component_reduction":
                prior_fibre[
                    "post_Round250_mixed_sheet_quotient_component_count"
                ] - len(component_ids),
            "mixed_sheet_quotient_component_ids_sha256":
                hash_object(component_ids),
            "components_with_inherited_Round244_seed_count":
                len(inherited_ids),
            "wall_only_Round251_component_count": len(wall_ids),
            "seeded_quotient_component_count": len(seeded_ids),
            "unseeded_quotient_component_count": len(unseeded_ids),
            "materialized_component_member_count":
                member_count_by_key[key_id],
            "known_connectivity_block_count":
                prior_fibre["known_connectivity_block_count"],
            "known_connectivity_block_ids_sha256":
                prior_fibre["known_connectivity_block_ids_sha256"],
            "frontier_status": prior_fibre["frontier_status"],
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
        status_histogram[prior_fibre["frontier_status"]] += 1
        keys_with_blocks += bool(
            prior_fibre["known_connectivity_block_count"]
        )
        keys_with_wall += bool(wall_ids)
    fibre_rows.sort(key=lambda row: row["quotient_fibre_frontier_row_id"])
    require(
        len(fibre_rows) == 116
        and keys_with_blocks == 24
        and keys_with_wall == 92
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
        "independent fibre census",
    )

    census = {
        "wall_root_count": 2_640,
        "wall_cell_count": 50_576,
        "same_chart_same_target_p_face_root_pair_count": len(root_rows),
        "exact_positive_area_cell_common_refinement_count": len(patch_rows),
        "strict_same_signature_p_face_patch_count": len(patch_rows),
        "patch_count_per_root_pair_histogram": {
            str(key): value
            for key, value in sorted(Counter(per_root.values()).items())
        },
        "patch_depth_histogram": dict(sorted(depth_histogram.items())),
        "source_pair_histogram": dict(sorted(source_histogram.items())),
        "exact_common_patch_area_sum": rational_text(area_sum),
        "exact_left_corridor_volume_sum": rational_text(left_volume_sum),
        "exact_right_corridor_volume_sum": rational_text(right_volume_sum),
        "Round250_mixed_sheet_quotient_component_count": 82_620,
        "post_Round251_mixed_sheet_quotient_component_count":
            len(component_rows),
        "Round251_mixed_sheet_quotient_component_reduction": rank_delta,
        "rank_reducing_p_face_edge_count": rank_delta,
        "quotient_redundant_physical_p_face_edge_count": redundant,
        "component_origin_histogram": dict(sorted(origin_histogram.items())),
        "Round250_component_class_size_histogram": {
            str(key): value
            for key, value in sorted(class_size_histogram.items())
        },
        "cumulative_virtual_stratum_node_count": total_virtual,
        "Round250_cumulative_mixed_sheet_edge_count": 59_212,
        "cumulative_mixed_sheet_edge_count": total_edges,
        "materialized_component_member_count": total_members,
        "seeded_quotient_component_count": seeded_count,
        "unseeded_quotient_component_count":
            len(component_rows) - seeded_count,
        "cumulative_virtual_stratum_known_block_incidence_count":
            seeded_virtual,
        "observed_exact_key_count": 116,
        "quotient_fibre_inventory_complete_count": len(fibre_rows),
        "mixed_sheet_quotient_component_count_histogram": {
            str(key): value
            for key, value in sorted(component_count_histogram.items())
        },
        "fibre_frontier_status_histogram":
            dict(sorted(status_histogram.items())),
        "post_Round251_occurrences_with_known_block_incidence": 36_200,
        "post_Round251_occurrences_without_known_block_incidence": 17_768,
        "new_occurrence_known_block_incidence_count": 0,
        "maximality_unproved_quotient_component_count":
            len(component_rows),
        "globally_exhausted_exact_key_fibre_count": 0,
        "global_exact_key_disposition_count": 0,
    }
    expected = {
        "status": (
            "CERTIFIED_3240_STRICT_WALL_P_FACE_PATCHES__"
            "QUOTIENT_COMPONENTS_82620_TO_82036__"
            "116_FIBRE_INVENTORIES_REFRESHED__ZERO_GLOBAL_PROMOTION"
        ),
        "census": census,
        "formal_input_binding": {
            name: SOURCE_PINS[name] for name in sorted(SOURCE_PINS)
        },
        "formal_same_chart_wall_p_face_root_pair_ledger":
            make_ledger(root_rows, "wall_p_face_root_pair_id"),
        "formal_wall_p_face_positive_patch_edge_ledger":
            make_ledger(patch_rows, "wall_p_face_edge_id"),
        "formal_post_Round251_mixed_sheet_component_ledger":
            make_ledger(component_rows, "mixed_sheet_component_row_id"),
        "formal_post_Round251_exact_key_quotient_fibre_frontier_ledger":
            make_ledger(fibre_rows, "quotient_fibre_frontier_row_id"),
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
    require(candidate == expected, "complete independent reconstruction")
    return {
        "status": "PASS_INDEPENDENT_ROUND251",
        "producer_imported_or_executed": False,
        "candidate_result_sha256": candidate_document["result_sha256"],
        "verified_same_chart_p_face_root_pair_count": len(root_rows),
        "verified_strict_p_face_patch_count": len(patch_rows),
        "verified_Round251_component_reduction": rank_delta,
        "verified_post_Round251_mixed_sheet_quotient_component_count":
            len(component_rows),
        "verified_cumulative_virtual_stratum_node_count": total_virtual,
        "verified_cumulative_mixed_sheet_edge_count": total_edges,
        "verified_exact_key_quotient_fibre_inventory_count":
            len(fibre_rows),
        "verified_occurrences_without_known_block_incidence": 17_768,
        "verified_globally_exhausted_exact_key_fibre_count": 0,
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
        "result_sha256": hash_object(result),
    }
    raw = canonical_bytes(document) + b"\n"
    if not arguments.no_write:
        safe_write(raw)
    print("PASS_INDEPENDENT_ROUND251")
    print(json.dumps(result, sort_keys=True))
    print(f"result_sha256={document['result_sha256']}")
    print(f"verification_sha256={hashlib.sha256(raw).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
