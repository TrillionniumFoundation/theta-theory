#!/usr/bin/env python3
"""Attach the Round232 whole-signature retained roots to the quotient."""

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
    / "cm2_round246_source_g_whole_signature_retained_quotient_certificate.json"
)
SCHEMA = "cm2.round246.source-g-whole-signature-retained-quotient.v1"
PINS = {
    "cm2_round179_source_g_residual_tube_arrangement_rows.json":
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json":
        "569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974",
    "cm2_round232_source_g_depth6_whole_origin_promotion_certificate.json":
        "a33d14fd7fd0ca0bb8e64efefd97be0839a5a8107b759f2219c14580ef3aa8c0",
    "cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json":
        "5b08d568cccd302ac2dd62e7e9b6573ce83e015181ead168812159c9f882712f",
    "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json":
        "c76662f7cb068127f3612a3655ae720662eead9b9210b5757d771693149883c1",
}
MAXIMUM_BYTES = {name: 400_000_000 for name in PINS}


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


def build() -> dict[str, Any]:
    for name in PINS:
        read_pinned(name)

    round232 = load_result(
        "cm2_round232_source_g_depth6_whole_origin_promotion_certificate.json"
    )
    roots = round232["whole_origin_promotion_rows"]
    interface_ids = {row["Round220_split_interface_id"] for row in roots}
    retained_ids = {row["Round179_retained_child_row_id"] for row in roots}
    resolved_ids = {row["Round179_resolved_child_row_id"] for row in roots}
    need(
        len(roots) == len(interface_ids) == len(retained_ids)
        == len(resolved_ids) == 2_220
        and round232["census"]["promoted_whole_origin_count"] == 2_220,
        "Round232 census",
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
    need(len(interfaces) == 2_220, "Round220 selected interfaces")
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
    need(len(retained) == len(resolved) == 2_220, "Round179 selected rows")
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

    round245 = load_result(
        "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json"
    )
    prior_components = {
        row["inherited_Round244_resolved_bulk_component_id"]: row
        for row in round245[
            "formal_post_Round245_mixed_sheet_component_ledger"
        ]["rows"]
    }
    occurrence_commitment = round245["unchanged_occurrence_frontier_commitment"]
    key_commitment = round245["unchanged_key_frontier_commitment"]
    need(
        len(prior_components) == 8_148
        and round245["census"]["remaining_Round239_interface_count"] == 5_364
        and round245["census"]["materialized_virtual_retained_stratum_node_count"]
        == 3_664,
        "Round245 quotient binding",
    )

    node_rows: list[dict[str, Any]] = []
    edge_rows: list[dict[str, Any]] = []
    new_nodes_by_component: dict[str, list[str]] = defaultdict(list)
    new_edges_by_component: dict[str, list[str]] = defaultdict(list)
    new_roots_by_component: Counter[str] = Counter()
    axis_histogram: Counter[str] = Counter()
    chart_histogram: Counter[str] = Counter()
    seeded_new_node_count = 0

    for root in sorted(roots, key=lambda row: row["whole_origin_promotion_row_id"]):
        interface_id = root["Round220_split_interface_id"]
        interface = interfaces[interface_id]
        retained_row = retained[root["Round179_retained_child_row_id"]]
        resolved_row = resolved[root["Round179_resolved_child_row_id"]]
        signature = resolved_signature(resolved_row)
        box = box_values(retained_row["box"])
        contact = tangential_rectangle(box, interface["axis"])
        component_id = component_by_child[resolved_row["row_id"]]
        seed_blocks = old_component_by_id[component_id][
            "seed_Round243_known_connectivity_block_ids"
        ]
        need(
            root["local_return_signature"] == signature
            and root["whole_origin_local_return_signature_credit"] == 1
            and root["whole_origin_positive_3D_occurrence_credit"] == 1
            and Q(root["original_coordinate_volume"])
            > Q(retained_row["coordinate_volume"])
            and retained_row["origin_row_id"] == resolved_row["origin_row_id"]
            == root["origin_row_id"]
            and retained_row["parent_id"] == resolved_row["parent_id"]
            == root["parent_id"]
            and retained_row["chart"] == resolved_row["chart"] == root["chart"]
            and {interface["lower_child_row_id"], interface["upper_child_row_id"]}
            == {retained_row["row_id"], resolved_row["row_id"]}
            and Q(interface["fixed_coordinate"])
            in {
                box[2 * {"t": 0, "p": 1, "s": 2}[interface["axis"]]],
                box[2 * {"t": 0, "p": 1, "s": 2}[interface["axis"]] + 1],
            },
            f"whole-root lineage:{interface_id}",
        )
        node_id = "round246-retained-stratum:" + digest([
            interface_id,
            retained_row["row_id"],
            signature,
        ])
        edge_id = "round246-resolved-retained-edge:" + digest([
            interface_id,
            resolved_row["row_id"],
            node_id,
            [qstr(value) for value in contact],
        ])
        node_rows.append(closed({
            "retained_stratum_node_id": node_id,
            "Round232_whole_origin_promotion_row_id":
                root["whole_origin_promotion_row_id"],
            "Round220_split_interface_id": interface_id,
            "Round179_retained_child_row_id": retained_row["row_id"],
            "inherited_Round244_resolved_bulk_component_id": component_id,
            "stratum_kind": "WHOLE_ORIGIN_SINGLE_SIGNATURE_RETAINED_BULK",
            "local_dimension": 3,
            "local_return_signature": signature,
            "official_key_ordinal": signature["official_key_ordinal"],
            "official_key_id": signature["official_key_id"],
            "strict_positive_3D_witness_box": retained_row["box"],
            "strict_positive_3D_witness_volume": qstr(volume(box)),
            "seed_known_connectivity_block_ids": seed_blocks,
            "virtual_stratum_known_block_incidence_credit": 1 if seed_blocks else 0,
            "occurrence_known_block_incidence_credit": 0,
            "physical_component_credit": 0,
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
        }))
        edge_rows.append(closed({
            "mixed_sheet_edge_id": edge_id,
            "Round220_split_interface_id": interface_id,
            "inherited_Round244_resolved_bulk_component_id": component_id,
            "resolved_occurrence_node_id": resolved_row["row_id"],
            "retained_stratum_node_id": node_id,
            "edge_kind": "RESOLVED_TO_WHOLE_SIGNATURE_RETAINED_BULK",
            "contact_proof_kind": "ROUND232_WHOLE_ORIGIN_EXACT_INTERFACE_FACE",
            "exact_positive_2D_contact_rectangle":
                [qstr(value) for value in contact],
            "exact_positive_2D_contact_area": qstr(area(contact)),
            "strict_positive_3D_retained_corridor_box": retained_row["box"],
            "strict_positive_3D_retained_corridor_volume": qstr(volume(box)),
            "current_quotient_lower_bound_edge_credit": 1,
            "occurrence_known_block_incidence_credit": 0,
            "physical_component_credit": 0,
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
        }))
        new_nodes_by_component[component_id].append(node_id)
        new_edges_by_component[component_id].append(edge_id)
        new_roots_by_component[component_id] += 1
        seeded_new_node_count += bool(seed_blocks)
        axis_histogram[interface["axis"]] += 1
        chart_histogram[root["chart"]] += 1

    node_rows.sort(key=lambda row: row["retained_stratum_node_id"])
    edge_rows.sort(key=lambda row: row["mixed_sheet_edge_id"])
    need(
        len(node_rows) == len(edge_rows) == 2_220
        and dict(axis_histogram) == {"t": 1_624, "p": 592, "s": 4}
        and dict(chart_histogram)
        == {"G:E": 696, "G:W": 696, "G:N": 414, "G:S": 414}
        and seeded_new_node_count == 100,
        "Round246 node and edge census",
    )

    component_rows: list[dict[str, Any]] = []
    new_touched = 0
    overlap_touched = 0
    cumulative_touched = 0
    cumulative_seeded_virtual_nodes = 0
    cumulative_root_histogram: Counter[int] = Counter()
    for component_id, prior in sorted(prior_components.items()):
        new_node_ids = sorted(new_nodes_by_component.get(component_id, []))
        new_edge_ids = sorted(new_edges_by_component.get(component_id, []))
        prior_node_ids = prior["new_virtual_stratum_node_ids"]
        prior_edge_ids = prior["new_mixed_sheet_edge_ids"]
        cumulative_nodes = sorted(prior_node_ids + new_node_ids)
        cumulative_edges = sorted(prior_edge_ids + new_edge_ids)
        prior_roots = prior["new_Round245_retained_root_count"]
        new_roots = new_roots_by_component[component_id]
        cumulative_roots = prior_roots + new_roots
        seed_blocks = prior["seed_known_connectivity_block_ids"]
        new_touched += bool(new_roots)
        overlap_touched += bool(new_roots and prior_roots)
        cumulative_touched += bool(cumulative_roots)
        cumulative_seeded_virtual_nodes += len(cumulative_nodes) if seed_blocks else 0
        cumulative_root_histogram[cumulative_roots] += 1
        component_rows.append(closed({
            "mixed_sheet_component_row_id":
                "round246-mixed-sheet-component:"
                + digest([component_id, cumulative_nodes]),
            "inherited_Round244_resolved_bulk_component_id": component_id,
            "Round245_retained_root_count": prior_roots,
            "new_Round246_whole_signature_retained_root_count": new_roots,
            "cumulative_retained_root_count": cumulative_roots,
            "Round245_virtual_stratum_node_count": len(prior_node_ids),
            "new_Round246_virtual_stratum_node_count": len(new_node_ids),
            "cumulative_virtual_stratum_node_count": len(cumulative_nodes),
            "cumulative_virtual_stratum_node_ids": cumulative_nodes,
            "cumulative_virtual_stratum_node_ids_sha256": digest(cumulative_nodes),
            "Round245_mixed_sheet_edge_count": len(prior_edge_ids),
            "new_Round246_mixed_sheet_edge_count": len(new_edge_ids),
            "cumulative_mixed_sheet_edge_count": len(cumulative_edges),
            "cumulative_mixed_sheet_edge_ids": cumulative_edges,
            "cumulative_mixed_sheet_edge_ids_sha256": digest(cumulative_edges),
            "seed_known_connectivity_block_ids": seed_blocks,
            "cumulative_virtual_stratum_known_block_incidence_count": (
                len(cumulative_nodes) if seed_blocks else 0
            ),
            "new_occurrence_known_block_incidence_count": 0,
            "certified_known_connectivity_only": True,
            "maximal_physical_component_claimed": False,
            "global_exact_key_fibre_credit": 0,
        }))
    component_rows.sort(key=lambda row: row["mixed_sheet_component_row_id"])
    need(
        len(component_rows) == 8_148
        and new_touched == 1_852
        and overlap_touched == 388
        and cumulative_touched == 3_976
        and cumulative_seeded_virtual_nodes == 316
        and dict(cumulative_root_histogram)
        == {0: 4_172, 1: 2_768, 2: 1_056, 3: 136, 4: 12, 5: 4},
        "Round246 component census",
    )

    census = {
        "Round232_whole_signature_retained_interface_count": 2_220,
        "new_virtual_retained_stratum_node_count": 2_220,
        "new_positive_area_physical_edge_count": 2_220,
        "interface_axis_histogram": dict(sorted(axis_histogram.items())),
        "source_chart_histogram": dict(sorted(chart_histogram.items())),
        "new_touched_Round244_component_count": new_touched,
        "Round245_Round246_touched_component_overlap_count": overlap_touched,
        "cumulative_touched_Round244_component_count": cumulative_touched,
        "Round245_virtual_retained_stratum_node_count": 3_664,
        "cumulative_virtual_retained_stratum_node_count": 5_884,
        "Round245_mixed_sheet_edge_count": 3_664,
        "cumulative_mixed_sheet_edge_count": 5_884,
        "new_virtual_stratum_known_block_incidence_count": seeded_new_node_count,
        "cumulative_virtual_stratum_known_block_incidence_count":
            cumulative_seeded_virtual_nodes,
        "Round246_mixed_sheet_component_count": 8_148,
        "Round246_mixed_sheet_component_reduction": 0,
        "new_occurrence_known_block_incidence_count": 0,
        "known_connectivity_block_count": 7_388,
        "post_Round246_occurrences_with_known_block_incidence": 36_200,
        "post_Round246_occurrences_without_known_block_incidence": 17_768,
        "remaining_Round239_interface_count": 3_144,
        "maximal_physical_component_assignment_count": 0,
        "global_exact_key_fibre_exhausted_count": 0,
    }
    return {
        "status": (
            "CERTIFIED_2220_WHOLE_SIGNATURE_RETAINED_FACE_CONTACTS__"
            "5884_CUMULATIVE_VIRTUAL_STRATA_AND_EDGES__"
            "ZERO_NEW_OCCURRENCE_INCIDENCE__3144_INTERFACES_REMAIN"
        ),
        "census": census,
        "formal_input_binding": {name: PINS[name] for name in sorted(PINS)},
        "formal_new_whole_signature_retained_stratum_node_ledger":
            ledger(node_rows, "retained_stratum_node_id"),
        "formal_new_whole_signature_physical_edge_ledger":
            ledger(edge_rows, "mixed_sheet_edge_id"),
        "formal_post_Round246_mixed_sheet_component_ledger":
            ledger(component_rows, "mixed_sheet_component_row_id"),
        "unchanged_occurrence_frontier_commitment": occurrence_commitment,
        "unchanged_key_frontier_commitment": key_commitment,
        "scope_contract": {
            "all_2220_Round232_roots_have_one_exact_whole_root_signature": True,
            "all_2220_signatures_equal_their_resolved_sibling_signature": True,
            "all_2220_interfaces_have_exact_positive_area_face_contact": True,
            "all_2220_retained_roots_have_strict_positive_3D_volume": True,
            "virtual_retained_stratum_incidence_is_not_occurrence_incidence": True,
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
            "process the final 3144 Round239 wall, crossing-time, and "
            "source-chart-seam retained interfaces by materializing every "
            "finite-key branch as a positive-volume retained stratum and "
            "attaching only exact positive-area sibling contacts"
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
