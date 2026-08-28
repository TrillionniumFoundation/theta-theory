#!/usr/bin/env python3
"""Independently verify the Round247 quotient extension."""

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
    / "cm2_round247_source_g_crossing_and_source_seam_retained_quotient_verification.json"
)
SCHEMA = (
    "cm2.round247.source-g-crossing-and-source-seam-retained-quotient."
    "verification.v1"
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
    "cm2_round247_source_g_crossing_and_source_seam_retained_quotient.py":
        "36de859af799a02be1db22406c339a376ee752f12a563e6fbc242ef1b9340405",
    "cm2_round247_source_g_crossing_and_source_seam_retained_quotient_certificate.json":
        "72188f5d99a220f44698f3023dd606633b364adbd02d5e20e5d4fa0ff6e1b2c7",
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


def validate_ledger(
    value: dict[str, Any],
    id_field: str,
) -> list[dict[str, Any]]:
    rows = value["rows"]
    need(
        value["row_count"] == len(rows)
        and len(rows) == len({row[id_field] for row in rows})
        and value["rows_sha256"] == digest(rows)
        and value["row_ids_sha256"] == digest([row[id_field] for row in rows])
        and value["row_hashes_sha256"]
        == digest([row["row_sha256"] for row in rows])
        and value["every_row_closed_by_own_SHA256"] is True
        and all(
            row["row_sha256"]
            == digest({
                key: item for key, item in row.items()
                if key != "row_sha256"
            })
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


def tangential(box: list[Q]) -> list[Q]:
    return [box[2], box[3], box[4], box[5]]


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


def seam_corridor(
    box: list[Q],
    fixed: Q,
) -> tuple[list[Q], int]:
    lower = 2 * box[0] * box[0] - 1
    upper = 2 * box[1] * box[1] - 1
    need(lower * upper < 0, "seam opposition")
    physical_lower = lower < 0
    need(fixed == (box[0] if physical_lower else box[1]), "physical endpoint")
    for depth in (1, 2):
        width = (box[1] - box[0]) / (2 ** depth)
        t0, t1 = (
            (box[0], box[0] + width)
            if physical_lower
            else (box[1] - width, box[1])
        )
        if 2 * t0 * t0 - 1 < 0 and 2 * t1 * t1 - 1 < 0:
            return [t0, t1, box[2], box[3], box[4], box[5]], depth
    raise RuntimeError("seam corridor")


def verify() -> dict[str, Any]:
    for name in PINS:
        read_pinned(name)
    candidate = load_result(
        "cm2_round247_source_g_crossing_and_source_seam_retained_quotient_certificate.json"
    )
    nodes = validate_ledger(
        candidate[
            "formal_new_crossing_and_source_seam_retained_stratum_node_ledger"
        ],
        "retained_stratum_node_id",
    )
    edges = validate_ledger(
        candidate[
            "formal_new_crossing_and_source_seam_physical_edge_ledger"
        ],
        "mixed_sheet_edge_id",
    )
    components = validate_ledger(
        candidate["formal_post_Round247_mixed_sheet_component_ledger"],
        "mixed_sheet_component_row_id",
    )
    need(len(nodes) == len(edges) == 504 and len(components) == 8_148,
         "candidate census")

    round237 = load_result(
        "cm2_round237_source_g_crossing_time_whole_origin_promotion_certificate.json"
    )
    round238 = load_result(
        "cm2_round238_source_g_source_chart_seam_whole_origin_promotion_certificate.json"
    )
    roots = {
        row["Round220_split_interface_id"]: ("CROSSING_TIME", row)
        for row in round237["whole_origin_promotion_rows"]
    }
    for row in round238["whole_origin_promotion_rows"]:
        interface_id = row["Round220_split_interface_id"]
        need(interface_id not in roots, f"disjoint roots:{interface_id}")
        roots[interface_id] = ("SOURCE_CHART_SEAM", row)
    interface_ids = set(roots)
    retained_ids = {
        row["Round179_retained_child_row_id"] for _, row in roots.values()
    }
    resolved_ids = {
        row["Round179_resolved_sibling_row_id"] for _, row in roots.values()
    }
    need(
        len(roots) == len(retained_ids) == len(resolved_ids) == 504,
        "source roots",
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
    need(len(interfaces) == 504, "interfaces")

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
    need(len(retained) == len(resolved) == 504, "Round179 rows")

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
    need(
        len(old_components) == 8_148
        and len(component_by_child) == 17_192,
        "Round244 components",
    )

    round246 = load_result(
        "cm2_round246_source_g_whole_signature_retained_quotient_certificate.json"
    )
    prior_components = {
        row["inherited_Round244_resolved_bulk_component_id"]: row
        for row in round246[
            "formal_post_Round246_mixed_sheet_component_ledger"
        ]["rows"]
    }
    need(
        candidate["unchanged_occurrence_frontier_commitment"]
        == round246["unchanged_occurrence_frontier_commitment"]
        and candidate["unchanged_key_frontier_commitment"]
        == round246["unchanged_key_frontier_commitment"]
        and len(prior_components) == 8_148,
        "Round246 commitments",
    )

    node_by_interface = {
        row["Round220_split_interface_id"]: row for row in nodes
    }
    edge_by_interface = {
        row["Round220_split_interface_id"]: row for row in edges
    }
    need(
        set(node_by_interface) == set(edge_by_interface) == interface_ids,
        "candidate root partition",
    )
    nodes_by_component: dict[str, list[str]] = defaultdict(list)
    edges_by_component: dict[str, list[str]] = defaultdict(list)
    roots_by_component: Counter[str] = Counter()
    kind_histogram: Counter[str] = Counter()
    depth_histogram: Counter[int] = Counter()
    owner_histogram: Counter[str] = Counter()
    chart_histogram: Counter[str] = Counter()
    physical_volume: Counter[str] = Counter()

    for interface_id, (kind, root) in roots.items():
        interface = interfaces[interface_id]
        retained_row = retained[root["Round179_retained_child_row_id"]]
        resolved_row = resolved[root["Round179_resolved_sibling_row_id"]]
        expected_signature = signature(resolved_row)
        component_id = component_by_child[resolved_row["row_id"]]
        seed_blocks = old_components[component_id][
            "seed_Round243_known_connectivity_block_ids"
        ]
        box = box_values(retained_row["box"])
        need(
            retained_row["origin_row_id"] == resolved_row["origin_row_id"]
            == root["origin_row_id"]
            and {interface["lower_child_row_id"], interface["upper_child_row_id"]}
            == {retained_row["row_id"], resolved_row["row_id"]}
            and interface["axis"] == "t",
            f"lineage:{interface_id}",
        )
        if kind == "CROSSING_TIME":
            need(
                root["whole_origin_local_return_signature"] == expected_signature
                and root[
                    "exact_endpoint_opposition_proves_crossing_time_in_open_unit_interval"
                ] is True,
                f"crossing:{interface_id}",
            )
            corridor = box
            source_signature = "CROSSING_TIME"
            proof_kind = "ROUND237_WHOLE_ROOT_EXACT_INTERFACE_FACE"
        else:
            need(
                root[
                    "whole_box_signature_recomputation_ignoring_chart_class_precheck"
                ] == expected_signature
                and root["seam_equation"] == "2*t^2-1=0",
                f"source seam:{interface_id}",
            )
            corridor, depth = seam_corridor(
                box,
                Q(interface["fixed_coordinate"]),
            )
            depth_histogram[depth] += 1
            owner_histogram[root["half_open_seam_owner_status"]] += 1
            source_signature = "SOURCE_CHART_SEAM"
            proof_kind = "ROUND238_EXACT_PHYSICAL_SIDE_DYADIC_CORRIDOR"
        contact = tangential(corridor)
        expected_node_id = "round247-retained-stratum:" + digest([
            kind,
            interface_id,
            retained_row["row_id"],
            expected_signature,
            [qstr(value) for value in corridor],
        ])
        expected_edge_id = "round247-resolved-retained-edge:" + digest([
            kind,
            interface_id,
            resolved_row["row_id"],
            expected_node_id,
            [qstr(value) for value in contact],
        ])
        node = node_by_interface[interface_id]
        edge = edge_by_interface[interface_id]
        need(
            node["retained_stratum_node_id"] == expected_node_id
            and node["source_classification"] == source_signature
            and node["local_return_signature"] == expected_signature
            and [Q(value) for value in node[
                "strict_positive_3D_physical_witness_box"
            ]] == corridor
            and Q(node["strict_positive_3D_physical_witness_volume"])
            == volume(corridor)
            and node["seed_known_connectivity_block_ids"] == seed_blocks
            and node["occurrence_known_block_incidence_credit"] == 0
            and node["maximal_physical_component_credit"] == 0,
            f"node:{interface_id}",
        )
        need(
            edge["mixed_sheet_edge_id"] == expected_edge_id
            and edge["source_classification"] == source_signature
            and edge["resolved_occurrence_node_id"] == resolved_row["row_id"]
            and edge["retained_stratum_node_id"] == expected_node_id
            and edge["contact_proof_kind"] == proof_kind
            and [Q(value) for value in edge[
                "exact_positive_2D_contact_rectangle"
            ]] == contact
            and Q(edge["exact_positive_2D_contact_area"]) == area(contact)
            and [Q(value) for value in edge[
                "strict_positive_3D_retained_corridor_box"
            ]] == corridor
            and edge["current_quotient_lower_bound_edge_credit"] == 1
            and edge["occurrence_known_block_incidence_credit"] == 0
            and edge["maximal_physical_component_credit"] == 0,
            f"edge:{interface_id}",
        )
        nodes_by_component[component_id].append(expected_node_id)
        edges_by_component[component_id].append(expected_edge_id)
        roots_by_component[component_id] += 1
        kind_histogram[kind] += 1
        chart_histogram[retained_row["chart"]] += 1
        physical_volume[kind] += volume(corridor)

    mixed_by_old = {
        row["inherited_Round244_resolved_bulk_component_id"]: row
        for row in components
    }
    need(set(mixed_by_old) == set(prior_components), "component partition")
    new_touched = 0
    overlap = 0
    cumulative_touched = 0
    cumulative_seeded_nodes = 0
    cumulative_root_histogram: Counter[int] = Counter()
    for component_id, prior in prior_components.items():
        row = mixed_by_old[component_id]
        new_nodes = sorted(nodes_by_component.get(component_id, []))
        new_edges = sorted(edges_by_component.get(component_id, []))
        cumulative_nodes = sorted(
            prior["cumulative_virtual_stratum_node_ids"] + new_nodes
        )
        cumulative_edges = sorted(
            prior["cumulative_mixed_sheet_edge_ids"] + new_edges
        )
        prior_roots = prior["cumulative_retained_root_count"]
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
            == "round247-mixed-sheet-component:"
            + digest([component_id, cumulative_nodes])
            and row["new_Round247_retained_root_count"] == new_roots
            and row["cumulative_virtual_stratum_node_ids"] == cumulative_nodes
            and row["cumulative_mixed_sheet_edge_ids"] == cumulative_edges
            and row["seed_known_connectivity_block_ids"] == seed_blocks
            and row["new_occurrence_known_block_incidence_count"] == 0
            and row["maximal_physical_component_claimed"] is False,
            f"component:{component_id}",
        )

    expected_census = {
        "crossing_time_retained_interface_count": 240,
        "source_chart_seam_retained_interface_count": 264,
        "new_virtual_retained_stratum_node_count": 504,
        "new_positive_area_physical_edge_count": 504,
        "source_seam_physical_corridor_depth_histogram":
            {str(key): value for key, value in sorted(depth_histogram.items())},
        "source_seam_half_open_owner_status_histogram":
            dict(sorted(owner_histogram.items())),
        "source_chart_histogram": dict(sorted(chart_histogram.items())),
        "crossing_time_exact_physical_volume_sum":
            qstr(physical_volume["CROSSING_TIME"]),
        "source_seam_exact_physical_corridor_volume_sum":
            qstr(physical_volume["SOURCE_CHART_SEAM"]),
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
    need(
        dict(kind_histogram)
        == {"CROSSING_TIME": 240, "SOURCE_CHART_SEAM": 264}
        and new_touched == 304
        and overlap == 0
        and cumulative_touched == 4_280
        and cumulative_seeded_nodes == 316
        and dict(cumulative_root_histogram)
        == {0: 3_868, 1: 2_888, 2: 1_228, 3: 144, 4: 16, 5: 4}
        and candidate["census"] == expected_census
        and candidate["strict_nonpromotion"]["CM2"] == "NO-GO_FOR_CLAIM"
        and candidate["strict_nonpromotion"]["physical_component_credit"] == 0,
        "census and nonpromotion",
    )
    return {
        "status": "PASS_INDEPENDENT_ROUND247",
        "verified_crossing_time_interface_count": 240,
        "verified_source_chart_seam_interface_count": 264,
        "verified_new_virtual_retained_stratum_node_count": 504,
        "verified_new_positive_area_physical_edge_count": 504,
        "verified_cumulative_virtual_stratum_node_count": 6_388,
        "verified_cumulative_mixed_sheet_edge_count": 6_388,
        "verified_mixed_sheet_component_count": 8_148,
        "verified_new_occurrence_known_block_incidence_count": 0,
        "verified_post_Round247_occurrence_incidence_count": 36_200,
        "verified_remaining_wall_interface_count": 2_640,
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
