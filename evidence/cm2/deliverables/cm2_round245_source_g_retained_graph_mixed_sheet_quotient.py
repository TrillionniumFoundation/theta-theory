#!/usr/bin/env python3
"""Attach the Round242 retained strata to the mixed-sheet quotient."""

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
    / "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json"
)
SCHEMA = "cm2.round245.source-g-retained-graph-mixed-sheet-quotient.v1"
PINS = {
    "cm2_round179_source_g_residual_tube_arrangement.py":
        "8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab",
    "cm2_round179_source_g_residual_tube_arrangement_rows.json":
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json":
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866",
    "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json":
        "569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974",
    "cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_certificate.json":
        "8d32c381e21c03aad6a531b7e5a527d295783b7e3e38baa1e6bcba20c40db22e",
    "cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json":
        "5b08d568cccd302ac2dd62e7e9b6573ce83e015181ead168812159c9f882712f",
}
MAXIMUM_BYTES = {
    name: 5_000_000 if name.endswith(".py") or "manifest" in name
    else 400_000_000
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
    return str(value.numerator) if value.denominator == 1 else (
        f"{value.numerator}/{value.denominator}"
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


def rectangle_area(rectangle: list[Q]) -> Q:
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
    row: dict[str, Any],
    chart: str,
    target: str,
) -> dict[str, Any]:
    return {
        "source_chart": chart,
        "target_lift": target,
        "ordered_integer_wall_events": row["events"],
        "signed_wall_word": list(row["pattern"]),
        "roof": row["roof"],
        "outgoing_cell": row["outgoing"],
        "target_chart": row["target_chart"],
        "official_key_row": row["key"]["row"],
        "official_key_ordinal": row["key"]["ordinal"],
        "official_key_id": row["key"]["identifier"],
    }


def tangential_rectangle(
    box: list[Q],
    axis: str,
) -> list[Q]:
    axes = ["t", "p", "s"]
    index = axes.index(axis)
    tangential = [item for item in range(3) if item != index]
    return [
        box[2 * tangential[0]],
        box[2 * tangential[0] + 1],
        box[2 * tangential[1]],
        box[2 * tangential[1] + 1],
    ]


def p_interface_corridor(
    r179: Any,
    registry: dict[str, Any],
    retained: dict[str, Any],
    interface: dict[str, Any],
    patch: dict[str, Any],
    signature: dict[str, Any],
) -> list[Q]:
    root = box_values(retained["box"])
    fixed = Q(interface["fixed_coordinate"])
    owner_match = signature == patch["owner_signature"]
    need(
        owner_match or signature == patch["shadow_signature"],
        f"p-interface signature:{interface['split_interface_id']}",
    )
    owner_lower = patch["owner_t_side"] == "LOWER_T_SIDE"
    matching_lower = owner_lower if owner_match else not owner_lower
    t_width = (root[1] - root[0]) / 2
    p_width = (root[3] - root[2]) / 2
    t0, t1 = (
        (root[0], root[0] + t_width)
        if matching_lower else (root[1] - t_width, root[1])
    )
    if fixed == root[2]:
        p0, p1 = root[2], root[2] + p_width
    elif fixed == root[3]:
        p0, p1 = root[3] - p_width, root[3]
    else:
        raise RuntimeError(f"p-interface endpoint:{interface['split_interface_id']}")
    corridor = [t0, t1, p0, p1, root[4], root[5]]
    atlas_box = r179.r174.atlas.AtlasBox(
        *corridor,
        len(retained["refinement_path"]) + 2,
        f"round245-p-corridor:{interface['split_interface_id']}",
    )
    computed, reasons = r179.r174.certify_signature(
        retained["chart"],
        atlas_box,
        signature["target_lift"],
        registry,
    )
    need(
        computed is not None
        and reasons == []
        and computed_signature(
            computed,
            retained["chart"],
            signature["target_lift"],
        ) == signature,
        f"strict p-interface corridor:{interface['split_interface_id']}",
    )
    return corridor


def strict_graph_side_corridor(
    r179: Any,
    registry: dict[str, Any],
    retained: dict[str, Any],
    base: list[Q],
    lower_side: bool,
    signature: dict[str, Any],
    label: str,
) -> list[Q]:
    root = box_values(retained["box"])
    for depth in range(1, 17):
        width = (root[1] - root[0]) / (2 ** depth)
        t0, t1 = (
            (root[0], root[0] + width)
            if lower_side else (root[1] - width, root[1])
        )
        corridor = [t0, t1, base[0], base[1], base[2], base[3]]
        atlas_box = r179.r174.atlas.AtlasBox(
            *corridor,
            len(retained["refinement_path"]) + depth,
            f"round245-graph-side:{label}:{depth}",
        )
        computed, reasons = r179.r174.certify_signature(
            retained["chart"],
            atlas_box,
            signature["target_lift"],
            registry,
        )
        if (
            computed is not None
            and reasons == []
            and computed_signature(
                computed,
                retained["chart"],
                signature["target_lift"],
            ) == signature
        ):
            return corridor
    raise RuntimeError(f"strict graph side corridor:{label}")


def build() -> dict[str, Any]:
    for name in PINS:
        read_pinned(name)

    round242 = load_result(
        "cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_certificate.json"
    )
    roots = round242["formal_root_existence_classification_ledger"]["rows"]
    patches = {
        row["transition_sheet_patch_row_id"]: row
        for row in round242["formal_positive_2D_transition_sheet_patch_ledger"]["rows"]
    }
    need(len(roots) == 3_136 and len(patches) == 264, "Round242 census")
    interface_ids = {row["Round220_split_interface_id"] for row in roots}
    retained_ids = {row["Round179_retained_child_row_id"] for row in roots}
    resolved_ids = {row["Round179_resolved_sibling_row_id"] for row in roots}
    need(
        len(interface_ids) == len(retained_ids) == len(resolved_ids) == 3_136,
        "Round242 one-to-one roots",
    )

    round220 = load_result(
        "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json"
    )
    table = round220["coordinate_boundary_atlas"]["tables"][
        "one_step_split_interface_rows"
    ]
    columns = table["columns"]
    id_index = columns.index("split_interface_id")
    interfaces = {
        packed[id_index]: dict(zip(columns, packed, strict=True))
        for packed in table["rows"]
        if packed[id_index] in interface_ids
    }
    need(len(interfaces) == 3_136, "Round220 selected interfaces")
    del round220
    gc.collect()

    round179 = load_result(
        "cm2_round179_source_g_residual_tube_arrangement_rows.json"
    )
    retained = unpack_selected(
        round179,
        "retained_3d_child_rows",
        "row_id",
        retained_ids,
    )
    resolved = unpack_selected(
        round179,
        "resolved_3d_child_rows",
        "row_id",
        resolved_ids,
    )
    need(len(retained) == len(resolved) == 3_136, "Round179 selected rows")
    del round179
    gc.collect()

    round244 = load_result(
        "cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json"
    )
    old_components = round244["formal_resolved_bulk_component_ledger"]["rows"]
    component_by_resolved: dict[str, str] = {}
    old_component_by_id: dict[str, dict[str, Any]] = {}
    for component in old_components:
        component_id = component["resolved_bulk_component_row_id"]
        old_component_by_id[component_id] = component
        for child_id in component["member_Round179_resolved_child_row_ids"]:
            need(child_id not in component_by_resolved, f"component partition:{child_id}")
            component_by_resolved[child_id] = component_id
    frontier = round244[
        "formal_post_Round244_occurrence_known_block_frontier_ledger"
    ]
    key_frontier = round244["formal_post_Round244_key_frontier_ledger"]
    need(
        len(old_components) == 8_148
        and len(component_by_resolved) == 17_192
        and frontier["row_count"] == 53_968
        and key_frontier["row_count"] == 116
        and round244["census"][
            "post_Round244_occurrences_with_known_block_incidence"
        ] == 36_200,
        "Round244 quotient binding",
    )
    frontier_commitment = {
        key: frontier[key]
        for key in (
            "row_count",
            "rows_sha256",
            "row_ids_sha256",
            "row_hashes_sha256",
        )
    }
    key_frontier_commitment = {
        key: key_frontier[key]
        for key in (
            "row_count",
            "rows_sha256",
            "row_ids_sha256",
            "row_hashes_sha256",
        )
    }
    del round244
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
            HERE / "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json",
            5_000_000,
        )
    )
    ctx.prec = 256

    node_rows: list[dict[str, Any]] = []
    edge_rows: list[dict[str, Any]] = []
    virtual_nodes_by_component: dict[str, list[str]] = defaultdict(list)
    edge_ids_by_component: dict[str, list[str]] = defaultdict(list)
    interface_histogram: Counter[str] = Counter()
    contact_kind_histogram: Counter[str] = Counter()
    node_kind_histogram: Counter[str] = Counter()
    seeded_virtual_node_count = 0
    p_corridor_volume_sum = Q(0)

    def add_node(
        root: dict[str, Any],
        component: dict[str, Any],
        kind: str,
        local_dimension: int,
        signature: dict[str, Any],
        witness_box: list[Q] | None,
        sheet_area: Q | None,
    ) -> str:
        node_id = "round245-retained-stratum:" + digest([
            root["Round220_split_interface_id"],
            root["Round179_retained_child_row_id"],
            kind,
            signature,
        ])
        seed_blocks = component["seed_Round243_known_connectivity_block_ids"]
        node_rows.append(closed({
            "retained_stratum_node_id": node_id,
            "Round220_split_interface_id": root["Round220_split_interface_id"],
            "Round179_retained_child_row_id": root["Round179_retained_child_row_id"],
            "inherited_Round244_resolved_bulk_component_id":
                component["resolved_bulk_component_row_id"],
            "stratum_kind": kind,
            "local_dimension": local_dimension,
            "local_return_signature": signature,
            "official_key_ordinal": signature["official_key_ordinal"],
            "official_key_id": signature["official_key_id"],
            "strict_positive_3D_witness_box": (
                [qstr(value) for value in witness_box]
                if witness_box is not None else None
            ),
            "strict_positive_3D_witness_volume": (
                qstr(volume(witness_box)) if witness_box is not None else "0"
            ),
            "exact_positive_2D_sheet_area": (
                qstr(sheet_area) if sheet_area is not None else "0"
            ),
            "half_open_owner_materialized": kind == "HALF_OPEN_TRANSITION_SHEET",
            "seed_known_connectivity_block_ids": seed_blocks,
            "virtual_stratum_known_block_incidence_credit": 1 if seed_blocks else 0,
            "occurrence_known_block_incidence_credit": 0,
            "physical_component_credit": 0,
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
        }))
        virtual_nodes_by_component[component["resolved_bulk_component_row_id"]].append(node_id)
        node_kind_histogram[kind] += 1
        return node_id

    def add_edge(
        root: dict[str, Any],
        component_id: str,
        left_id: str,
        right_id: str,
        edge_kind: str,
        contact_kind: str,
        contact_rectangle: list[Q],
        corridor: list[Q] | None,
    ) -> str:
        area = rectangle_area(contact_rectangle)
        edge_id = "round245-mixed-sheet-edge:" + digest([
            root["Round220_split_interface_id"],
            left_id,
            right_id,
            edge_kind,
            [qstr(value) for value in contact_rectangle],
        ])
        edge_rows.append(closed({
            "mixed_sheet_edge_id": edge_id,
            "Round220_split_interface_id": root["Round220_split_interface_id"],
            "inherited_Round244_resolved_bulk_component_id": component_id,
            "left_node_id": left_id,
            "right_node_id": right_id,
            "edge_kind": edge_kind,
            "contact_proof_kind": contact_kind,
            "exact_positive_2D_contact_rectangle":
                [qstr(value) for value in contact_rectangle],
            "exact_positive_2D_contact_area": qstr(area),
            "strict_positive_3D_retained_corridor_box": (
                [qstr(value) for value in corridor] if corridor is not None else None
            ),
            "strict_positive_3D_retained_corridor_volume": (
                qstr(volume(corridor)) if corridor is not None else "0"
            ),
            "current_quotient_lower_bound_edge_credit": 1,
            "occurrence_known_block_incidence_credit": 0,
            "physical_component_credit": 0,
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
        }))
        edge_ids_by_component[component_id].append(edge_id)
        contact_kind_histogram[contact_kind] += 1
        return edge_id

    for root in sorted(roots, key=lambda row: row["root_existence_row_id"]):
        interface_id = root["Round220_split_interface_id"]
        interface = interfaces[interface_id]
        retained_row = retained[root["Round179_retained_child_row_id"]]
        resolved_row = resolved[root["Round179_resolved_sibling_row_id"]]
        signature = resolved_signature(resolved_row)
        component_id = component_by_resolved[resolved_row["row_id"]]
        component = old_component_by_id[component_id]
        root_box = box_values(retained_row["box"])
        need(
            retained_row["origin_row_id"] == resolved_row["origin_row_id"]
            and retained_row["parent_id"] == resolved_row["parent_id"]
            and retained_row["chart"] == resolved_row["chart"]
            and {interface["lower_child_row_id"], interface["upper_child_row_id"]}
            == {retained_row["row_id"], resolved_row["row_id"]}
            and interface["event_trace_materialized_on_interface"] is False
            and signature["official_key_id"] == root["official_key_id"],
            f"root lineage:{interface_id}",
        )
        interface_histogram[interface["axis"]] += 1

        if root["existence_classification"].startswith("WHOLE_ROOT"):
            need(
                root["whole_root_local_return_signature"] == signature
                and root["whole_root_local_return_signature_credit"] == 1
                and root["zero_absence_partition_exact_base_area"]
                == root["root_exact_base_area"],
                f"whole-root signature:{interface_id}",
            )
            bulk_node = add_node(
                root,
                component,
                "WHOLE_ROOT_ZERO_ABSENCE_BULK",
                3,
                signature,
                root_box,
                None,
            )
            contact = tangential_rectangle(root_box, interface["axis"])
            add_edge(
                root,
                component_id,
                resolved_row["row_id"],
                bulk_node,
                "RESOLVED_TO_RETAINED_BULK",
                "WHOLE_INTERFACE_FACE_FROM_WHOLE_ROOT_ZERO_ABSENCE",
                contact,
                root_box,
            )
            continue

        patch = patches[root["transition_sheet_patch_row_id"]]
        need(
            patch["Round220_split_interface_id"] == interface_id
            and patch["unique_graph_point_for_every_closed_base_point"] is True
            and patch["formal_half_open_owner_credit"] == 1
            and patch["owner_signature"]["official_key_id"]
            == patch["shadow_signature"]["official_key_id"]
            == signature["official_key_id"]
            and signature in (patch["owner_signature"], patch["shadow_signature"]),
            f"graph patch:{interface_id}",
        )
        base = [Q(value) for value in patch["closed_base_rectangle"]]
        sheet_area = rectangle_area(base)
        owner_lower = patch["owner_t_side"] == "LOWER_T_SIDE"
        owner_box = strict_graph_side_corridor(
            r179,
            registry,
            retained_row,
            base,
            owner_lower,
            patch["owner_signature"],
            interface_id + ":owner",
        )
        shadow_box = strict_graph_side_corridor(
            r179,
            registry,
            retained_row,
            base,
            not owner_lower,
            patch["shadow_signature"],
            interface_id + ":shadow",
        )
        owner_node = add_node(
            root,
            component,
            "OWNER_OPEN_BULK",
            3,
            patch["owner_signature"],
            owner_box,
            None,
        )
        shadow_node = add_node(
            root,
            component,
            "SHADOW_OPEN_BULK",
            3,
            patch["shadow_signature"],
            shadow_box,
            None,
        )
        sheet_node = add_node(
            root,
            component,
            "HALF_OPEN_TRANSITION_SHEET",
            2,
            patch["owner_signature"],
            None,
            sheet_area,
        )
        add_edge(
            root,
            component_id,
            owner_node,
            sheet_node,
            "OWNER_BULK_TO_HALF_OPEN_SHEET",
            "ROUND242_POSITIVE_2D_UNIQUE_GRAPH_PATCH",
            base,
            owner_box,
        )
        add_edge(
            root,
            component_id,
            shadow_node,
            sheet_node,
            "SHADOW_BULK_TO_HALF_OPEN_SHEET",
            "ROUND242_POSITIVE_2D_UNIQUE_GRAPH_PATCH",
            base,
            shadow_box,
        )

        matching_node = (
            owner_node if signature == patch["owner_signature"] else shadow_node
        )
        if interface["axis"] == "t":
            fixed = Q(interface["fixed_coordinate"])
            matching_lower = (
                patch["owner_t_side"] == "LOWER_T_SIDE"
                if matching_node == owner_node else
                patch["owner_t_side"] != "LOWER_T_SIDE"
            )
            need(
                fixed == (root_box[0] if matching_lower else root_box[1]),
                f"matching t interface:{interface_id}",
            )
            corridor = owner_box if matching_node == owner_node else shadow_box
            contact = base
            contact_kind = "ROUND242_GRAPH_SIDE_AT_T_INTERFACE"
        elif interface["axis"] == "p":
            corridor = p_interface_corridor(
                r179,
                registry,
                retained_row,
                interface,
                patch,
                signature,
            )
            contact = tangential_rectangle(corridor, "p")
            contact_kind = "256_BIT_STRICT_DYADIC_CORRIDOR_AT_P_INTERFACE"
            p_corridor_volume_sum += volume(corridor)
        else:
            raise RuntimeError(f"unexpected graph interface axis:{interface_id}")
        add_edge(
            root,
            component_id,
            resolved_row["row_id"],
            matching_node,
            "RESOLVED_TO_MATCHING_GRAPH_SIDE_BULK",
            contact_kind,
            contact,
            corridor,
        )

    node_rows.sort(key=lambda row: row["retained_stratum_node_id"])
    edge_rows.sort(key=lambda row: row["mixed_sheet_edge_id"])
    need(
        len(node_rows) == len(edge_rows) == 3_664
        and dict(node_kind_histogram) == {
            "WHOLE_ROOT_ZERO_ABSENCE_BULK": 2_872,
            "OWNER_OPEN_BULK": 264,
            "SHADOW_OPEN_BULK": 264,
            "HALF_OPEN_TRANSITION_SHEET": 264,
        }
        and dict(interface_histogram) == {"t": 2_528, "p": 540, "s": 68}
        and dict(contact_kind_histogram) == {
            "WHOLE_INTERFACE_FACE_FROM_WHOLE_ROOT_ZERO_ABSENCE": 2_872,
            "ROUND242_POSITIVE_2D_UNIQUE_GRAPH_PATCH": 528,
            "ROUND242_GRAPH_SIDE_AT_T_INTERFACE": 252,
            "256_BIT_STRICT_DYADIC_CORRIDOR_AT_P_INTERFACE": 12,
        },
        "mixed stratum and edge census",
    )

    component_rows: list[dict[str, Any]] = []
    touched_component_count = 0
    seeded_touched_component_count = 0
    virtual_count_histogram: Counter[int] = Counter()
    root_count_histogram: Counter[int] = Counter()
    for component_id, component in sorted(old_component_by_id.items()):
        node_ids = sorted(virtual_nodes_by_component.get(component_id, []))
        edge_ids = sorted(edge_ids_by_component.get(component_id, []))
        root_count = sum(
            1 for row in roots
            if component_by_resolved[row["Round179_resolved_sibling_row_id"]]
            == component_id
        )
        need(
            len(node_ids) == len(edge_ids)
            and len(node_ids) == root_count + 2 * sum(
                1 for row in roots
                if component_by_resolved[row["Round179_resolved_sibling_row_id"]]
                == component_id
                and row["transition_sheet_patch_row_id"] is not None
            ),
            f"component enrichment:{component_id}",
        )
        seed_blocks = component["seed_Round243_known_connectivity_block_ids"]
        touched_component_count += bool(node_ids)
        seeded_touched_component_count += bool(node_ids and seed_blocks)
        if seed_blocks:
            seeded_virtual_node_count += len(node_ids)
        virtual_count_histogram[len(node_ids)] += 1
        root_count_histogram[root_count] += 1
        component_rows.append(closed({
            "mixed_sheet_component_row_id":
                "round245-mixed-sheet-component:" + digest([component_id, node_ids]),
            "inherited_Round244_resolved_bulk_component_id": component_id,
            "member_Round179_resolved_child_count":
                component["member_Round179_resolved_child_count"],
            "member_Round179_resolved_child_row_ids_sha256":
                component["member_Round179_resolved_child_row_ids_sha256"],
            "new_Round245_retained_root_count": root_count,
            "new_virtual_stratum_node_count": len(node_ids),
            "new_virtual_stratum_node_ids": node_ids,
            "new_virtual_stratum_node_ids_sha256": digest(node_ids),
            "new_mixed_sheet_edge_count": len(edge_ids),
            "new_mixed_sheet_edge_ids": edge_ids,
            "new_mixed_sheet_edge_ids_sha256": digest(edge_ids),
            "seed_known_connectivity_block_ids": seed_blocks,
            "new_virtual_stratum_known_block_incidence_count": (
                len(node_ids) if seed_blocks else 0
            ),
            "new_occurrence_known_block_incidence_count": 0,
            "certified_known_connectivity_only": True,
            "maximal_physical_component_claimed": False,
            "global_exact_key_fibre_credit": 0,
        }))
    component_rows.sort(key=lambda row: row["mixed_sheet_component_row_id"])
    need(
        len(component_rows) == 8_148
        and touched_component_count == 2_512
        and seeded_touched_component_count == 108
        and seeded_virtual_node_count == 216
        and dict(root_count_histogram) == {0: 5_636, 1: 1_892, 2: 616, 3: 4},
        "mixed quotient component census",
    )

    census = {
        "Round242_retained_interface_count": 3_136,
        "whole_root_zero_absence_continuation_count": 2_872,
        "positive_2D_graph_patch_interface_count": 264,
        "graph_patch_t_interface_count": 252,
        "graph_patch_p_interface_count": 12,
        "materialized_virtual_retained_stratum_node_count": len(node_rows),
        "materialized_mixed_sheet_edge_count": len(edge_rows),
        "retained_stratum_node_kind_histogram":
            dict(sorted(node_kind_histogram.items())),
        "contact_proof_kind_histogram":
            dict(sorted(contact_kind_histogram.items())),
        "interface_axis_histogram": dict(sorted(interface_histogram.items())),
        "strict_p_interface_corridor_exact_volume_sum": qstr(p_corridor_volume_sum),
        "Round244_resolved_bulk_component_count": 8_148,
        "Round245_mixed_sheet_component_count": len(component_rows),
        "Round245_mixed_sheet_component_reduction": 0,
        "touched_Round244_component_count": touched_component_count,
        "seeded_touched_Round244_component_count": seeded_touched_component_count,
        "new_virtual_stratum_known_block_incidence_count":
            seeded_virtual_node_count,
        "new_occurrence_known_block_incidence_count": 0,
        "known_connectivity_block_count": 7_388,
        "post_Round245_occurrences_with_known_block_incidence": 36_200,
        "post_Round245_occurrences_without_known_block_incidence": 17_768,
        "remaining_Round239_interface_count": 5_364,
        "maximal_physical_component_assignment_count": 0,
        "global_exact_key_fibre_exhausted_count": 0,
    }
    return {
        "status": (
            "CERTIFIED_3136_ROUND242_RETAINED_INTERFACES_IN_MIXED_SHEET_"
            "QUOTIENT__3664_VIRTUAL_STRATA__3664_PHYSICAL_EDGES__"
            "ZERO_NEW_OCCURRENCE_INCIDENCE__5364_INTERFACES_REMAIN"
        ),
        "census": census,
        "formal_input_binding": {name: PINS[name] for name in sorted(PINS)},
        "formal_retained_stratum_node_ledger":
            ledger(node_rows, "retained_stratum_node_id"),
        "formal_mixed_sheet_physical_edge_ledger":
            ledger(edge_rows, "mixed_sheet_edge_id"),
        "formal_post_Round245_mixed_sheet_component_ledger":
            ledger(component_rows, "mixed_sheet_component_row_id"),
        "unchanged_occurrence_frontier_commitment": frontier_commitment,
        "unchanged_key_frontier_commitment": key_frontier_commitment,
        "scope_contract": {
            "all_3136_Round242_roots_have_positive_area_resolved_retained_contact": True,
            "all_264_graph_roots_materialize_owner_sheet_shadow_connectivity": True,
            "all_12_p_interface_graph_roots_have_256_bit_strict_positive_volume_corridors": True,
            "virtual_retained_stratum_incidence_is_not_occurrence_incidence": True,
            "mixed_sheet_components_are_known_connectivity_lower_bounds_only": True,
            "exact_key_equality_alone_never_supplies_glue": True,
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
            "process the remaining 5364 Round239 whole-signature, wall, "
            "crossing-time, and source-seam retained interfaces with the same "
            "positive-area or positive-volume physical-contact standard; then "
            "rebuild the mixed quotient and occurrence/key frontiers"
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
