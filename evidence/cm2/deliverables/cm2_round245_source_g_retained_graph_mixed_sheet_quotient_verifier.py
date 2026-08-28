#!/usr/bin/env python3
"""Independently verify the Round245 retained mixed-sheet quotient."""

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
    / "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_verification.json"
)
SCHEMA = (
    "cm2.round245.source-g-retained-graph-mixed-sheet-quotient."
    "verification.v1"
)
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
    "cm2_round245_source_g_retained_graph_mixed_sheet_quotient.py":
        "797ad3a9436740a9832c819b64cc42f3a282dc7634754cf7c2361ffb19703b1e",
    "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json":
        "c76662f7cb068127f3612a3655ae720662eead9b9210b5757d771693149883c1",
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


def tangential(box: list[Q], axis: str) -> list[Q]:
    index = {"t": 0, "p": 1, "s": 2}[axis]
    keep = [item for item in range(3) if item != index]
    return [
        box[2 * keep[0]],
        box[2 * keep[0] + 1],
        box[2 * keep[1]],
        box[2 * keep[1] + 1],
    ]


def certify_box(
    r179: Any,
    registry: dict[str, Any],
    retained: dict[str, Any],
    box: list[Q],
    expected: dict[str, Any],
    label: str,
) -> None:
    atlas_box = r179.r174.atlas.AtlasBox(
        *box,
        len(retained["refinement_path"]) + 20,
        f"round245-verifier:{label}",
    )
    computed, reasons = r179.r174.certify_signature(
        retained["chart"],
        atlas_box,
        expected["target_lift"],
        registry,
    )
    need(
        computed is not None
        and reasons == []
        and computed_signature(
            computed,
            retained["chart"],
            expected["target_lift"],
        ) == expected,
        f"strict box:{label}",
    )


def verify() -> dict[str, Any]:
    for name in PINS:
        read_pinned(name)

    candidate = load_result(
        "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json"
    )
    nodes = validate_ledger(
        candidate["formal_retained_stratum_node_ledger"],
        "retained_stratum_node_id",
    )
    edges = validate_ledger(
        candidate["formal_mixed_sheet_physical_edge_ledger"],
        "mixed_sheet_edge_id",
    )
    mixed_components = validate_ledger(
        candidate["formal_post_Round245_mixed_sheet_component_ledger"],
        "mixed_sheet_component_row_id",
    )
    need(len(nodes) == len(edges) == 3_664 and len(mixed_components) == 8_148,
         "candidate ledger census")

    round242 = load_result(
        "cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_certificate.json"
    )
    roots = round242["formal_root_existence_classification_ledger"]["rows"]
    patches = {
        row["transition_sheet_patch_row_id"]: row
        for row in round242["formal_positive_2D_transition_sheet_patch_ledger"]["rows"]
    }
    interface_ids = {row["Round220_split_interface_id"] for row in roots}
    retained_ids = {row["Round179_retained_child_row_id"] for row in roots}
    resolved_ids = {row["Round179_resolved_sibling_row_id"] for row in roots}
    need(
        len(roots) == len(interface_ids) == len(retained_ids)
        == len(resolved_ids) == 3_136
        and len(patches) == 264,
        "Round242 root census",
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
    need(len(interfaces) == 3_136, "Round220 interface census")
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
    del round179
    gc.collect()
    need(len(retained) == len(resolved) == 3_136, "Round179 row census")

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
    old_frontier = round244[
        "formal_post_Round244_occurrence_known_block_frontier_ledger"
    ]
    old_key_frontier = round244["formal_post_Round244_key_frontier_ledger"]
    need(
        len(old_components) == 8_148
        and len(component_by_child) == 17_192
        and candidate["unchanged_occurrence_frontier_commitment"]
        == {
            key: old_frontier[key]
            for key in ("row_count", "rows_sha256", "row_ids_sha256", "row_hashes_sha256")
        }
        and candidate["unchanged_key_frontier_commitment"]
        == {
            key: old_key_frontier[key]
            for key in ("row_count", "rows_sha256", "row_ids_sha256", "row_hashes_sha256")
        },
        "Round244 commitments",
    )
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

    nodes_by_interface: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    for node in nodes:
        interface_id = node["Round220_split_interface_id"]
        kind = node["stratum_kind"]
        need(kind not in nodes_by_interface[interface_id], f"node kind:{interface_id}:{kind}")
        nodes_by_interface[interface_id][kind] = node
    edges_by_interface: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    for edge in edges:
        interface_id = edge["Round220_split_interface_id"]
        kind = edge["edge_kind"]
        need(kind not in edges_by_interface[interface_id], f"edge kind:{interface_id}:{kind}")
        edges_by_interface[interface_id][kind] = edge

    expected_nodes_by_component: dict[str, list[str]] = defaultdict(list)
    expected_edges_by_component: dict[str, list[str]] = defaultdict(list)
    contact_histogram: Counter[str] = Counter()
    node_histogram: Counter[str] = Counter()
    axis_histogram: Counter[str] = Counter()
    p_volume = Q(0)

    for root in roots:
        interface_id = root["Round220_split_interface_id"]
        interface = interfaces[interface_id]
        retained_row = retained[root["Round179_retained_child_row_id"]]
        resolved_row = resolved[root["Round179_resolved_sibling_row_id"]]
        expected_signature = signature(resolved_row)
        component_id = component_by_child[resolved_row["row_id"]]
        component = old_components[component_id]
        root_box = box_values(retained_row["box"])
        node_set = nodes_by_interface[interface_id]
        edge_set = edges_by_interface[interface_id]
        axis_histogram[interface["axis"]] += 1
        need(
            {interface["lower_child_row_id"], interface["upper_child_row_id"]}
            == {retained_row["row_id"], resolved_row["row_id"]}
            and interface["event_trace_materialized_on_interface"] is False
            and expected_signature["official_key_id"] == root["official_key_id"],
            f"lineage:{interface_id}",
        )

        if root["transition_sheet_patch_row_id"] is None:
            need(
                set(node_set) == {"WHOLE_ROOT_ZERO_ABSENCE_BULK"}
                and set(edge_set) == {"RESOLVED_TO_RETAINED_BULK"}
                and root["whole_root_local_return_signature"] == expected_signature,
                f"zero-root topology:{interface_id}",
            )
            node = node_set["WHOLE_ROOT_ZERO_ABSENCE_BULK"]
            edge = edge_set["RESOLVED_TO_RETAINED_BULK"]
            expected_node_id = "round245-retained-stratum:" + digest([
                interface_id,
                retained_row["row_id"],
                "WHOLE_ROOT_ZERO_ABSENCE_BULK",
                expected_signature,
            ])
            contact = tangential(root_box, interface["axis"])
            need(
                node["retained_stratum_node_id"] == expected_node_id
                and node["local_return_signature"] == expected_signature
                and node["strict_positive_3D_witness_box"] == retained_row["box"]
                and Q(node["strict_positive_3D_witness_volume"]) == volume(root_box)
                and edge["left_node_id"] == resolved_row["row_id"]
                and edge["right_node_id"] == expected_node_id
                and [Q(value) for value in edge["exact_positive_2D_contact_rectangle"]]
                == contact
                and Q(edge["exact_positive_2D_contact_area"]) == area(contact),
                f"zero-root evidence:{interface_id}",
            )
        else:
            patch = patches[root["transition_sheet_patch_row_id"]]
            need(
                set(node_set) == {
                    "OWNER_OPEN_BULK",
                    "SHADOW_OPEN_BULK",
                    "HALF_OPEN_TRANSITION_SHEET",
                }
                and set(edge_set) == {
                    "OWNER_BULK_TO_HALF_OPEN_SHEET",
                    "SHADOW_BULK_TO_HALF_OPEN_SHEET",
                    "RESOLVED_TO_MATCHING_GRAPH_SIDE_BULK",
                }
                and expected_signature in (
                    patch["owner_signature"], patch["shadow_signature"]
                ),
                f"graph topology:{interface_id}",
            )
            base = [Q(value) for value in patch["closed_base_rectangle"]]
            owner_node = node_set["OWNER_OPEN_BULK"]
            shadow_node = node_set["SHADOW_OPEN_BULK"]
            sheet_node = node_set["HALF_OPEN_TRANSITION_SHEET"]
            for kind, node, expected in (
                ("OWNER_OPEN_BULK", owner_node, patch["owner_signature"]),
                ("SHADOW_OPEN_BULK", shadow_node, patch["shadow_signature"]),
            ):
                witness = box_values(node["strict_positive_3D_witness_box"])
                need(
                    node["retained_stratum_node_id"]
                    == "round245-retained-stratum:" + digest([
                        interface_id, retained_row["row_id"], kind, expected
                    ])
                    and node["local_return_signature"] == expected
                    and Q(node["strict_positive_3D_witness_volume"])
                    == volume(witness)
                    and witness[2:] == [base[0], base[1], base[2], base[3]],
                    f"graph bulk node:{interface_id}:{kind}",
                )
                certify_box(
                    r179, registry, retained_row, witness, expected,
                    interface_id + ":" + kind,
                )
            need(
                sheet_node["retained_stratum_node_id"]
                == "round245-retained-stratum:" + digest([
                    interface_id,
                    retained_row["row_id"],
                    "HALF_OPEN_TRANSITION_SHEET",
                    patch["owner_signature"],
                ])
                and sheet_node["local_return_signature"] == patch["owner_signature"]
                and Q(sheet_node["exact_positive_2D_sheet_area"]) == area(base)
                and sheet_node["half_open_owner_materialized"] is True,
                f"graph sheet node:{interface_id}",
            )
            for edge_kind, bulk_node in (
                ("OWNER_BULK_TO_HALF_OPEN_SHEET", owner_node),
                ("SHADOW_BULK_TO_HALF_OPEN_SHEET", shadow_node),
            ):
                edge = edge_set[edge_kind]
                need(
                    edge["left_node_id"] == bulk_node["retained_stratum_node_id"]
                    and edge["right_node_id"] == sheet_node["retained_stratum_node_id"]
                    and [Q(value) for value in edge["exact_positive_2D_contact_rectangle"]]
                    == base
                    and Q(edge["exact_positive_2D_contact_area"]) == area(base),
                    f"graph sheet edge:{interface_id}:{edge_kind}",
                )
            contact_edge = edge_set["RESOLVED_TO_MATCHING_GRAPH_SIDE_BULK"]
            matching_node = (
                owner_node if expected_signature == patch["owner_signature"]
                else shadow_node
            )
            corridor = box_values(contact_edge["strict_positive_3D_retained_corridor_box"])
            contact = [Q(value) for value in contact_edge[
                "exact_positive_2D_contact_rectangle"
            ]]
            need(
                contact_edge["left_node_id"] == resolved_row["row_id"]
                and contact_edge["right_node_id"]
                == matching_node["retained_stratum_node_id"]
                and Q(contact_edge["strict_positive_3D_retained_corridor_volume"])
                == volume(corridor)
                and Q(contact_edge["exact_positive_2D_contact_area"]) == area(contact),
                f"resolved graph contact:{interface_id}",
            )
            if interface["axis"] == "t":
                need(
                    contact == base
                    and Q(interface["fixed_coordinate"])
                    in {corridor[0], corridor[1]},
                    f"t-interface contact:{interface_id}",
                )
            else:
                need(
                    interface["axis"] == "p"
                    and contact == tangential(corridor, "p")
                    and Q(interface["fixed_coordinate"])
                    in {corridor[2], corridor[3]},
                    f"p-interface contact:{interface_id}",
                )
                certify_box(
                    r179, registry, retained_row, corridor, expected_signature,
                    interface_id + ":p-contact",
                )
                p_volume += volume(corridor)

        for node in node_set.values():
            need(
                node["inherited_Round244_resolved_bulk_component_id"] == component_id
                and node["seed_known_connectivity_block_ids"]
                == component["seed_Round243_known_connectivity_block_ids"]
                and node["occurrence_known_block_incidence_credit"] == 0
                and node["maximal_physical_component_credit"] == 0,
                f"node scope:{node['retained_stratum_node_id']}",
            )
            expected_nodes_by_component[component_id].append(
                node["retained_stratum_node_id"]
            )
            node_histogram[node["stratum_kind"]] += 1
        for edge in edge_set.values():
            need(
                edge["inherited_Round244_resolved_bulk_component_id"] == component_id
                and edge["current_quotient_lower_bound_edge_credit"] == 1
                and edge["occurrence_known_block_incidence_credit"] == 0
                and edge["maximal_physical_component_credit"] == 0,
                f"edge scope:{edge['mixed_sheet_edge_id']}",
            )
            expected_edges_by_component[component_id].append(edge["mixed_sheet_edge_id"])
            contact_histogram[edge["contact_proof_kind"]] += 1

    mixed_by_old = {
        row["inherited_Round244_resolved_bulk_component_id"]: row
        for row in mixed_components
    }
    need(set(mixed_by_old) == set(old_components), "mixed component partition")
    touched = 0
    seeded_touched = 0
    seeded_nodes = 0
    root_count_histogram: Counter[int] = Counter()
    roots_by_component: Counter[str] = Counter(
        component_by_child[root["Round179_resolved_sibling_row_id"]]
        for root in roots
    )
    for component_id, old in old_components.items():
        row = mixed_by_old[component_id]
        node_ids = sorted(expected_nodes_by_component.get(component_id, []))
        edge_ids = sorted(expected_edges_by_component.get(component_id, []))
        root_count = roots_by_component[component_id]
        seed_blocks = old["seed_Round243_known_connectivity_block_ids"]
        touched += bool(node_ids)
        seeded_touched += bool(node_ids and seed_blocks)
        seeded_nodes += len(node_ids) if seed_blocks else 0
        root_count_histogram[root_count] += 1
        need(
            row["mixed_sheet_component_row_id"]
            == "round245-mixed-sheet-component:" + digest([component_id, node_ids])
            and row["new_Round245_retained_root_count"] == root_count
            and row["new_virtual_stratum_node_ids"] == node_ids
            and row["new_mixed_sheet_edge_ids"] == edge_ids
            and row["seed_known_connectivity_block_ids"] == seed_blocks
            and row["new_virtual_stratum_known_block_incidence_count"]
            == (len(node_ids) if seed_blocks else 0)
            and row["new_occurrence_known_block_incidence_count"] == 0
            and row["maximal_physical_component_claimed"] is False,
            f"mixed component:{component_id}",
        )

    expected_census = {
        "Round242_retained_interface_count": 3_136,
        "whole_root_zero_absence_continuation_count": 2_872,
        "positive_2D_graph_patch_interface_count": 264,
        "graph_patch_t_interface_count": 252,
        "graph_patch_p_interface_count": 12,
        "materialized_virtual_retained_stratum_node_count": 3_664,
        "materialized_mixed_sheet_edge_count": 3_664,
        "retained_stratum_node_kind_histogram": dict(sorted(node_histogram.items())),
        "contact_proof_kind_histogram": dict(sorted(contact_histogram.items())),
        "interface_axis_histogram": dict(sorted(axis_histogram.items())),
        "strict_p_interface_corridor_exact_volume_sum": (
            str(p_volume.numerator) if p_volume.denominator == 1
            else f"{p_volume.numerator}/{p_volume.denominator}"
        ),
        "Round244_resolved_bulk_component_count": 8_148,
        "Round245_mixed_sheet_component_count": 8_148,
        "Round245_mixed_sheet_component_reduction": 0,
        "touched_Round244_component_count": touched,
        "seeded_touched_Round244_component_count": seeded_touched,
        "new_virtual_stratum_known_block_incidence_count": seeded_nodes,
        "new_occurrence_known_block_incidence_count": 0,
        "known_connectivity_block_count": 7_388,
        "post_Round245_occurrences_with_known_block_incidence": 36_200,
        "post_Round245_occurrences_without_known_block_incidence": 17_768,
        "remaining_Round239_interface_count": 5_364,
        "maximal_physical_component_assignment_count": 0,
        "global_exact_key_fibre_exhausted_count": 0,
    }
    need(
        touched == 2_512
        and seeded_touched == 108
        and seeded_nodes == 216
        and dict(root_count_histogram) == {0: 5_636, 1: 1_892, 2: 616, 3: 4}
        and candidate["census"] == expected_census
        and candidate["strict_nonpromotion"]["CM2"] == "NO-GO_FOR_CLAIM"
        and candidate["strict_nonpromotion"]["physical_component_credit"] == 0
        and candidate["strict_nonpromotion"]["global_exact_key_fibre_credit"] == 0,
        "census and nonpromotion",
    )

    return {
        "status": "PASS_INDEPENDENT_ROUND245",
        "verified_Round242_retained_interface_count": 3_136,
        "verified_virtual_retained_stratum_node_count": 3_664,
        "verified_mixed_sheet_physical_edge_count": 3_664,
        "verified_strict_graph_bulk_corridor_count": 528,
        "verified_strict_p_interface_contact_corridor_count": 12,
        "verified_mixed_sheet_component_count": 8_148,
        "verified_touched_component_count": 2_512,
        "verified_virtual_stratum_known_block_incidence_count": 216,
        "verified_new_occurrence_known_block_incidence_count": 0,
        "verified_post_Round245_occurrence_incidence_count": 36_200,
        "verified_remaining_interface_count": 5_364,
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
