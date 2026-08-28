#!/usr/bin/env python3
"""Independently verify the Round246 whole-signature quotient extension."""

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
    / "cm2_round246_source_g_whole_signature_retained_quotient_verification.json"
)
SCHEMA = (
    "cm2.round246.source-g-whole-signature-retained-quotient."
    "verification.v1"
)
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
    "cm2_round246_source_g_whole_signature_retained_quotient.py":
        "9bfa9b7cc78e510ccebba6a9184366ad4481645b0ce89d1516aa86f222981dd0",
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


def validate_ledger(
    value: dict[str, Any],
    id_field: str,
) -> list[dict[str, Any]]:
    rows = value["rows"]
    need(
        value["row_count"] == len(rows)
        and len(rows) == len({row[id_field] for row in rows})
        and value["rows_sha256"] == digest(rows)
        and value["row_ids_sha256"]
        == digest([row[id_field] for row in rows])
        and value["row_hashes_sha256"]
        == digest([row["row_sha256"] for row in rows])
        and value["every_row_closed_by_own_SHA256"] is True
        and all(
            row["row_sha256"]
            == digest({key: item for key, item in row.items() if key != "row_sha256"})
            for row in rows
        ),
        f"ledger:{id_field}",
    )
    return rows


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


def tangential(box: list[Q], axis: str) -> list[Q]:
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


def signature(row: dict[str, Any]) -> dict[str, Any]:
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


def verify() -> dict[str, Any]:
    for name in PINS:
        read_pinned(name)
    candidate = load_result(
        "cm2_round246_source_g_whole_signature_retained_quotient_certificate.json"
    )
    nodes = validate_ledger(
        candidate["formal_new_whole_signature_retained_stratum_node_ledger"],
        "retained_stratum_node_id",
    )
    edges = validate_ledger(
        candidate["formal_new_whole_signature_physical_edge_ledger"],
        "mixed_sheet_edge_id",
    )
    mixed_components = validate_ledger(
        candidate["formal_post_Round246_mixed_sheet_component_ledger"],
        "mixed_sheet_component_row_id",
    )
    need(len(nodes) == len(edges) == 2_220 and len(mixed_components) == 8_148,
         "candidate ledger census")

    round232 = load_result(
        "cm2_round232_source_g_depth6_whole_origin_promotion_certificate.json"
    )
    roots = round232["whole_origin_promotion_rows"]
    root_by_interface = {row["Round220_split_interface_id"]: row for row in roots}
    interface_ids = set(root_by_interface)
    retained_ids = {row["Round179_retained_child_row_id"] for row in roots}
    resolved_ids = {row["Round179_resolved_child_row_id"] for row in roots}
    need(
        len(roots) == len(interface_ids) == len(retained_ids)
        == len(resolved_ids) == 2_220,
        "Round232 root census",
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
    del round220
    gc.collect()
    need(len(interfaces) == 2_220, "Round220 interface census")

    round179 = load_result(
        "cm2_round179_source_g_residual_tube_arrangement_rows.json"
    )
    retained = unpack_selected(
        round179, "retained_3d_child_rows", "row_id", retained_ids
    )
    resolved = unpack_selected(
        round179, "resolved_3d_child_rows", "row_id", resolved_ids
    )
    del round179
    gc.collect()
    need(len(retained) == len(resolved) == 2_220, "Round179 row census")

    round244 = load_result(
        "cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json"
    )
    old_components = {
        row["resolved_bulk_component_row_id"]: row
        for row in round244["formal_resolved_bulk_component_ledger"]["rows"]
    }
    component_by_child = {
        child_id: component_id
        for component_id, component in old_components.items()
        for child_id in component["member_Round179_resolved_child_row_ids"]
    }
    del round244
    gc.collect()
    need(len(old_components) == 8_148 and len(component_by_child) == 17_192,
         "Round244 component census")

    round245 = load_result(
        "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json"
    )
    prior_components = {
        row["inherited_Round244_resolved_bulk_component_id"]: row
        for row in round245[
            "formal_post_Round245_mixed_sheet_component_ledger"
        ]["rows"]
    }
    need(
        candidate["unchanged_occurrence_frontier_commitment"]
        == round245["unchanged_occurrence_frontier_commitment"]
        and candidate["unchanged_key_frontier_commitment"]
        == round245["unchanged_key_frontier_commitment"]
        and len(prior_components) == 8_148,
        "Round245 commitments",
    )

    nodes_by_interface = {row["Round220_split_interface_id"]: row for row in nodes}
    edges_by_interface = {row["Round220_split_interface_id"]: row for row in edges}
    need(
        set(nodes_by_interface) == set(edges_by_interface) == interface_ids,
        "candidate interface partition",
    )
    expected_nodes_by_component: dict[str, list[str]] = defaultdict(list)
    expected_edges_by_component: dict[str, list[str]] = defaultdict(list)
    roots_by_component: Counter[str] = Counter()
    axis_histogram: Counter[str] = Counter()
    chart_histogram: Counter[str] = Counter()
    seeded_new_nodes = 0

    for interface_id, root in root_by_interface.items():
        interface = interfaces[interface_id]
        retained_row = retained[root["Round179_retained_child_row_id"]]
        resolved_row = resolved[root["Round179_resolved_child_row_id"]]
        expected_signature = signature(resolved_row)
        component_id = component_by_child[resolved_row["row_id"]]
        seed_blocks = old_components[component_id][
            "seed_Round243_known_connectivity_block_ids"
        ]
        box = box_values(retained_row["box"])
        contact = tangential(box, interface["axis"])
        expected_node_id = "round246-retained-stratum:" + digest([
            interface_id, retained_row["row_id"], expected_signature
        ])
        expected_edge_id = "round246-resolved-retained-edge:" + digest([
            interface_id,
            resolved_row["row_id"],
            expected_node_id,
            [str(value.numerator) if value.denominator == 1 else
             f"{value.numerator}/{value.denominator}" for value in contact],
        ])
        node = nodes_by_interface[interface_id]
        edge = edges_by_interface[interface_id]
        axis_index = {"t": 0, "p": 1, "s": 2}[interface["axis"]]
        need(
            root["local_return_signature"] == expected_signature
            and root["whole_origin_local_return_signature_credit"] == 1
            and root["whole_origin_positive_3D_occurrence_credit"] == 1
            and retained_row["origin_row_id"] == resolved_row["origin_row_id"]
            == root["origin_row_id"]
            and {interface["lower_child_row_id"], interface["upper_child_row_id"]}
            == {retained_row["row_id"], resolved_row["row_id"]}
            and Q(interface["fixed_coordinate"])
            in {box[2 * axis_index], box[2 * axis_index + 1]},
            f"source lineage:{interface_id}",
        )
        need(
            node["retained_stratum_node_id"] == expected_node_id
            and node["local_return_signature"] == expected_signature
            and node["strict_positive_3D_witness_box"] == retained_row["box"]
            and Q(node["strict_positive_3D_witness_volume"]) == volume(box)
            and node["seed_known_connectivity_block_ids"] == seed_blocks
            and node["virtual_stratum_known_block_incidence_credit"]
            == (1 if seed_blocks else 0)
            and node["occurrence_known_block_incidence_credit"] == 0
            and node["maximal_physical_component_credit"] == 0,
            f"candidate node:{interface_id}",
        )
        need(
            edge["mixed_sheet_edge_id"] == expected_edge_id
            and edge["resolved_occurrence_node_id"] == resolved_row["row_id"]
            and edge["retained_stratum_node_id"] == expected_node_id
            and [Q(value) for value in edge["exact_positive_2D_contact_rectangle"]]
            == contact
            and Q(edge["exact_positive_2D_contact_area"]) == area(contact)
            and edge["strict_positive_3D_retained_corridor_box"]
            == retained_row["box"]
            and Q(edge["strict_positive_3D_retained_corridor_volume"])
            == volume(box)
            and edge["current_quotient_lower_bound_edge_credit"] == 1
            and edge["occurrence_known_block_incidence_credit"] == 0
            and edge["maximal_physical_component_credit"] == 0,
            f"candidate edge:{interface_id}",
        )
        expected_nodes_by_component[component_id].append(expected_node_id)
        expected_edges_by_component[component_id].append(expected_edge_id)
        roots_by_component[component_id] += 1
        seeded_new_nodes += bool(seed_blocks)
        axis_histogram[interface["axis"]] += 1
        chart_histogram[root["chart"]] += 1

    mixed_by_old = {
        row["inherited_Round244_resolved_bulk_component_id"]: row
        for row in mixed_components
    }
    need(set(mixed_by_old) == set(prior_components), "mixed component partition")
    new_touched = 0
    overlap = 0
    cumulative_touched = 0
    cumulative_seeded_nodes = 0
    cumulative_root_histogram: Counter[int] = Counter()
    for component_id, prior in prior_components.items():
        row = mixed_by_old[component_id]
        new_nodes = sorted(expected_nodes_by_component.get(component_id, []))
        new_edges = sorted(expected_edges_by_component.get(component_id, []))
        cumulative_nodes = sorted(prior["new_virtual_stratum_node_ids"] + new_nodes)
        cumulative_edges = sorted(prior["new_mixed_sheet_edge_ids"] + new_edges)
        prior_roots = prior["new_Round245_retained_root_count"]
        new_roots = roots_by_component[component_id]
        cumulative_roots = prior_roots + new_roots
        seed_blocks = prior["seed_known_connectivity_block_ids"]
        new_touched += bool(new_roots)
        overlap += bool(new_roots and prior_roots)
        cumulative_touched += bool(cumulative_roots)
        cumulative_seeded_nodes += len(cumulative_nodes) if seed_blocks else 0
        cumulative_root_histogram[cumulative_roots] += 1
        need(
            row["mixed_sheet_component_row_id"]
            == "round246-mixed-sheet-component:"
            + digest([component_id, cumulative_nodes])
            and row["Round245_retained_root_count"] == prior_roots
            and row["new_Round246_whole_signature_retained_root_count"]
            == new_roots
            and row["cumulative_virtual_stratum_node_ids"] == cumulative_nodes
            and row["cumulative_mixed_sheet_edge_ids"] == cumulative_edges
            and row["seed_known_connectivity_block_ids"] == seed_blocks
            and row["new_occurrence_known_block_incidence_count"] == 0
            and row["maximal_physical_component_claimed"] is False,
            f"component:{component_id}",
        )

    expected_census = {
        "Round232_whole_signature_retained_interface_count": 2_220,
        "new_virtual_retained_stratum_node_count": 2_220,
        "new_positive_area_physical_edge_count": 2_220,
        "interface_axis_histogram": dict(sorted(axis_histogram.items())),
        "source_chart_histogram": dict(sorted(chart_histogram.items())),
        "new_touched_Round244_component_count": new_touched,
        "Round245_Round246_touched_component_overlap_count": overlap,
        "cumulative_touched_Round244_component_count": cumulative_touched,
        "Round245_virtual_retained_stratum_node_count": 3_664,
        "cumulative_virtual_retained_stratum_node_count": 5_884,
        "Round245_mixed_sheet_edge_count": 3_664,
        "cumulative_mixed_sheet_edge_count": 5_884,
        "new_virtual_stratum_known_block_incidence_count": seeded_new_nodes,
        "cumulative_virtual_stratum_known_block_incidence_count":
            cumulative_seeded_nodes,
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
    need(
        new_touched == 1_852
        and overlap == 388
        and cumulative_touched == 3_976
        and seeded_new_nodes == 100
        and cumulative_seeded_nodes == 316
        and dict(cumulative_root_histogram)
        == {0: 4_172, 1: 2_768, 2: 1_056, 3: 136, 4: 12, 5: 4}
        and candidate["census"] == expected_census
        and candidate["strict_nonpromotion"]["CM2"] == "NO-GO_FOR_CLAIM"
        and candidate["strict_nonpromotion"]["physical_component_credit"] == 0,
        "census and nonpromotion",
    )
    return {
        "status": "PASS_INDEPENDENT_ROUND246",
        "verified_whole_signature_retained_interface_count": 2_220,
        "verified_new_virtual_retained_stratum_node_count": 2_220,
        "verified_new_positive_area_physical_edge_count": 2_220,
        "verified_cumulative_virtual_stratum_node_count": 5_884,
        "verified_cumulative_mixed_sheet_edge_count": 5_884,
        "verified_mixed_sheet_component_count": 8_148,
        "verified_new_occurrence_known_block_incidence_count": 0,
        "verified_post_Round246_occurrence_incidence_count": 36_200,
        "verified_remaining_interface_count": 3_144,
        "verified_maximal_physical_component_credit": 0,
        "verified_global_exact_key_fibre_credit": 0,
        "candidate_result_sha256": digest(candidate),
        "producer_imported_or_executed": False,
        "CM2": "NO-GO_FOR_CLAIM",
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
