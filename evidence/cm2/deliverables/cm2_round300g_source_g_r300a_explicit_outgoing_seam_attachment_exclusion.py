#!/usr/bin/env python3
"""Round300-G: fail-closed audit of the 128 explicit outgoing-seam pairs.

Round300-A isolated 128 canonical occurrence pairs with an exact R295-A
two-sided lower graph-sheet witness.  That fact proves incidence on the
graph sheet; it does not select either endpoint as an included one-sided
owner attachment.

This producer reopens the complete 3,232-pair Round300-A closure, selects
the exact 128-row explicit subset, and exhausts the only plausible
R246/R247 retained-stratum attachment channels.  Exact full-signature
matching is highly non-unique.  No selected R291 leaf child or containing
origin participates in a Round220 one-step split interface.  R247
signature candidates are geometrically disjoint, while the only R246
contacts are closure-only boundary touches.  Consequently all 128 rows
remain ineligible for component-edge or DSU credit.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
import gc
import gzip
import hashlib
from io import BytesIO
import json
import os
from pathlib import Path
import tempfile
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
PREFIX = (
    "cm2_round300g_source_g_"
    "r300a_explicit_outgoing_seam_attachment_exclusion"
)
LEDGER_PATH = HERE / f"{PREFIX}_ledger.json.gz"
RESULT_PATH = HERE / f"{PREFIX}_result.json"
SCHEMA = (
    "cm2.round300g.source-g-r300a-explicit-"
    "outgoing-seam-attachment-exclusion.v1"
)
LEDGER_SCHEMA = SCHEMA + ".ledger.v1"

FILES = {
    "R179": (
        "cm2_round179_source_g_residual_tube_arrangement_rows.json",
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    ),
    "R182": (
        "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json",
        "ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c",
    ),
    "R220": (
        "cm2_round220_source_g_round179_resolved_child_boundary_atlas_"
        "certificate.json",
        "569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974",
    ),
    "R232": (
        "cm2_round232_source_g_depth6_whole_origin_promotion_certificate.json",
        "a33d14fd7fd0ca0bb8e64efefd97be0839a5a8107b759f2219c14580ef3aa8c0",
    ),
    "R238": (
        "cm2_round238_source_g_source_chart_seam_whole_origin_promotion_"
        "certificate.json",
        "8200ba9c35ba32c938eb66beb7a4040908db9b81fc449881a55b09e67b517446",
    ),
    "R246": (
        "cm2_round246_source_g_whole_signature_retained_quotient_"
        "certificate.json",
        "a448359c0a9b4495e54afe6e2d860c20fb222684bae46ee108574782a5a33bc9",
    ),
    "R247": (
        "cm2_round247_source_g_crossing_and_source_seam_retained_quotient_"
        "certificate.json",
        "72188f5d99a220f44698f3023dd606633b364adbd02d5e20e5d4fa0ff6e1b2c7",
    ),
    "R279": (
        "cm2_round279_source_g_collar_atom_and_face_edge_freeze_atoms.json.gz",
        "283a10799e0c7d1156695c30cdb2533488602ca646a18804f93211c0a3132dbe",
    ),
    "R291": (
        "cm2_round291_source_g_complete_lower_stratum_local_disposition_"
        "freeze_ledger.json.gz",
        "412b616b2cf75ef1373d98086cfcb2eb90a8c544e9f6b4d16a673f6cfeeb57ab",
    ),
    "R293": (
        "cm2_round293_source_g_r289_r291_witness_binding_canonical_"
        "closure_ledger.json.gz",
        "0e7395a69844734cc51563882f471987cc566db28a55ccae6e6d15d045f9e53c",
    ),
    "R294": (
        "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
        "registry_ledger.json.gz",
        "c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb",
    ),
    "R295A": (
        "cm2_round295a_source_g_r291_positive_t_retained_continuation_"
        "closure_physical_witness_incidence_binding_ledger.json.gz",
        "2d9addfc9fca55366a58b29a7084c063674c3f556dd5398b038ae7d51fe97dcf",
    ),
    "R300A": (
        "cm2_round300a_source_g_r287_graph_zero_lower_frontier_"
        "exhaustion_ledger.json.gz",
        "ddc1a8bc53861afeb93d3569c6efa228f17d86f161db31a39fa9b72458ab8f2d",
    ),
}


class GateError(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise GateError(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def guard_input(label: str) -> None:
    filename, expected = FILES[label]
    path = HERE / filename
    need(path.is_file(), "missing input:" + filename)
    need(path.resolve().parent == HERE.resolve(), "input path escape:" + filename)
    need(file_sha256(path) == expected, "input byte pin:" + filename)


def read_json(label: str) -> dict[str, Any]:
    filename = FILES[label][0]
    with (HERE / filename).open("rb") as stream:
        value = json.load(stream)
    need(type(value) is dict, label + ":JSON object")
    return value


def read_gzip(label: str) -> dict[str, Any]:
    filename = FILES[label][0]
    with gzip.open(HERE / filename, "rt", encoding="utf-8") as stream:
        value = json.load(stream)
    need(type(value) is dict, label + ":GZIP JSON object")
    return value


def closed_result(label: str) -> dict[str, Any]:
    wrapper = read_json(label)
    need(
        set(wrapper) == {"schema", "result", "result_sha256"}
        and wrapper["result_sha256"] == digest(wrapper["result"])
        and type(wrapper["result"]) is dict,
        label + ":closed result wrapper",
    )
    return wrapper["result"]


def closed(payload: dict[str, Any]) -> dict[str, Any]:
    return {**payload, "row_sha256": digest(payload)}


def verify_row(row: dict[str, Any], label: str) -> None:
    need(type(row) is dict and "row_sha256" in row, label + ":row object")
    payload = {key: value for key, value in row.items() if key != "row_sha256"}
    need(row["row_sha256"] == digest(payload), label + ":row closure")


def verify_ledger(
    ledger: dict[str, Any],
    rows_key: str,
    count_key: str,
    ids_key: str,
    hashes_key: str,
    rows_sha_key: str,
    id_field: str,
    label: str,
) -> list[dict[str, Any]]:
    rows = ledger[rows_key]
    need(type(rows) is list, label + ":rows")
    need(ledger[count_key] == len(rows), label + ":row count")
    need(
        ledger[ids_key] == digest([row[id_field] for row in rows]),
        label + ":row IDs commitment",
    )
    need(
        ledger[hashes_key] == digest([row["row_sha256"] for row in rows]),
        label + ":row hashes commitment",
    )
    need(ledger[rows_sha_key] == digest(rows), label + ":rows commitment")
    return rows


def unpack(table: dict[str, Any]) -> list[dict[str, Any]]:
    columns = table["columns"]
    return [dict(zip(columns, row, strict=True)) for row in table["rows"]]


def unpack_named(result: dict[str, Any], name: str) -> list[dict[str, Any]]:
    columns = result["row_column_schemas"][name]
    return [dict(zip(columns, row, strict=True)) for row in result[name]]


def qbox(values: Iterable[str]) -> tuple[Q, Q, Q, Q, Q, Q]:
    box = tuple(Q(value) for value in values)
    need(
        len(box) == 6
        and box[0] < box[1]
        and box[2] < box[3]
        and box[4] < box[5],
        "strict positive rational box",
    )
    return box  # type: ignore[return-value]


def contains(
    outer: tuple[Q, Q, Q, Q, Q, Q],
    inner: tuple[Q, Q, Q, Q, Q, Q],
) -> bool:
    return all(
        outer[index] <= inner[index]
        and inner[index + 1] <= outer[index + 1]
        for index in (0, 2, 4)
    )


def box_relation(
    left: tuple[Q, Q, Q, Q, Q, Q],
    right: tuple[Q, Q, Q, Q, Q, Q],
) -> str:
    widths = [
        min(left[index + 1], right[index + 1])
        - max(left[index], right[index])
        for index in (0, 2, 4)
    ]
    if all(width > 0 for width in widths):
        return "STRICT_POSITIVE_VOLUME_INTERSECTION"
    if all(width >= 0 for width in widths):
        return "CLOSED_BOUNDARY_CONTACT"
    return "DISJOINT"


def histogram(counter: Counter[Any]) -> dict[str, int]:
    return {str(key): value for key, value in sorted(counter.items(), key=str)}


def build(producer_sha256: str) -> tuple[dict[str, Any], dict[str, Any]]:
    for label in FILES:
        guard_input(label)

    # Reopen the complete Round300-A pair closure and select the exact 128.
    r300a = read_gzip("R300A")
    source_rows = verify_ledger(
        r300a,
        "source_pair_expansion_rows",
        "source_pair_expansion_row_count",
        "source_pair_expansion_row_ids_sha256",
        "source_pair_expansion_row_hashes_sha256",
        "source_pair_expansion_rows_sha256",
        "Round300A_R287_source_pair_expansion_row_id",
        "R300A source expansion",
    )
    pair_rows = verify_ledger(
        r300a,
        "canonical_occurrence_pair_rows",
        "canonical_occurrence_pair_row_count",
        "canonical_occurrence_pair_row_ids_sha256",
        "canonical_occurrence_pair_row_hashes_sha256",
        "canonical_occurrence_pair_rows_sha256",
        "Round300A_canonical_occurrence_pair_row_id",
        "R300A canonical pairs",
    )
    for row in source_rows:
        verify_row(row, "R300A source")
    for row in pair_rows:
        verify_row(row, "R300A pair")
    need(len(source_rows) == 3_488 and len(pair_rows) == 3_232,
         "R300A complete census")
    explicit = [
        row for row in pair_rows
        if row["R295A_explicit_lower_graph_sheet_witness_present"] is True
    ]
    need(
        len(explicit) == 128
        and sum(
            row["R295A_explicit_lower_graph_sheet_witness_present"] is False
            for row in pair_rows
        ) == 3_104,
        "exact R300A explicit subset",
    )
    explicit.sort(
        key=lambda row: row["Round300A_canonical_occurrence_pair_row_id"]
    )
    binding_ids = {
        row["R295A_physical_incidence_binding_row_ids"][0]
        for row in explicit
    }
    need(
        len(binding_ids) == 128
        and all(
            len(row["R295A_physical_incidence_binding_row_ids"]) == 1
            and row["frontier_disposition"]
            == "PRIOR_R295A_EXPLICIT_LOWER_GRAPH_SHEET_WITNESS__"
               "NO_NEW_COMPONENT_EDGE_CREDIT"
            and row["formal_component_edge_credit"] == 0
            for row in explicit
        ),
        "R300A explicit row contract",
    )
    del source_rows, pair_rows, r300a
    gc.collect()

    # Bind the exact R295-A rows.
    r295a = read_gzip("R295A")
    need(r295a["row_count"] == 113_452, "R295A full census")
    bindings = {
        row["Round295A_R291_physical_incidence_binding_row_id"]: row
        for row in r295a["rows"]
        if row["Round295A_R291_physical_incidence_binding_row_id"]
        in binding_ids
    }
    need(set(bindings) == binding_ids, "R295A exact selected bindings")
    for row in bindings.values():
        verify_row(row, "R295A selected binding")
        need(
            row["Round295A_binding_classification"]
            == "FORMAL_ROUND294_REGISTRY_REBIND__"
               "EXACT_TWO_SIDED_GRAPH_SHEET_ATOM_INCIDENCE"
            and row["witness_kind"] == "ROUND182_GRAPH_SHEET_LEAF"
            and row["target_Round294_registry_reference_count"] == 2
            and row["formal_component_union_credit"] == 0
            and row["formal_DSU_rank_reduction_credit"] == 0,
            "R295A selected semantics",
        )
    r291_ids = {
        row["Round291_local_disposition_row_id"] for row in bindings.values()
    }
    r293_ids = {
        row["source_Round293_R291_physical_witness_binding_row_id"]
        for row in bindings.values()
    }
    occurrence_ids = {
        occurrence_id
        for row in explicit
        for occurrence_id
        in row["canonical_unordered_Round294_registry_occurrence_ids"]
    }
    need(len(occurrence_ids) == 256, "256 distinct endpoint occurrences")
    del r295a
    gc.collect()

    # Bind selected R291 dispositions and the exact physical witness cell.
    r291 = read_gzip("R291")
    need(r291["row_count"] == 55_428, "R291 complete row count")
    dispositions = {
        row["complete_lower_stratum_local_disposition_row_id"]: row
        for row in r291["rows"]
        if row["complete_lower_stratum_local_disposition_row_id"] in r291_ids
    }
    need(set(dispositions) == r291_ids, "R291 selected dispositions")
    for row in dispositions.values():
        verify_row(row, "R291 selected disposition")
        need(
            row["predicate_label"] == "outgoing_chart_seam"
            and row["predicate_equation"]
            == "target_normal_x^2-target_normal_y^2=0"
            and row["local_disposition"] == "WHOLE_PHYSICAL_SUPPORT"
            and row["evidence_basis"]
            == "ROUND182_EXPLICIT_FULL_OR_CLIPPED_2D_GRAPH_SHEET",
            "R291 outgoing-seam semantics",
        )
    del r291
    gc.collect()

    # Reopen the selected R293 rows and require the same exact two endpoints.
    r293 = read_gzip("R293")
    r293_rows = {
        row["Round292_R291_physical_witness_binding_row_id"]: row
        for row in r293["Round291_physical_witness_binding_rows"]
        if row["Round292_R291_physical_witness_binding_row_id"] in r293_ids
    }
    need(set(r293_rows) == r293_ids, "R293 selected rows")
    for row in r293_rows.values():
        verify_row(row, "R293 selected binding")
        need(
            row["binding_classification"]
            == "EXACT_TWO_SIDED_GRAPH_SHEET_ATOM_INCIDENCE"
            and row["terminal_registry_target_reference_count"] == 2
            and row["component_edge_credit"] == 0,
            "R293 selected semantics",
        )
    del r293
    gc.collect()

    # Reopen the exact Round294 endpoint registry rows.
    r294 = read_gzip("R294")
    need(r294["row_count"] == 431_208, "R294 complete registry census")
    registry = {
        row["registry_occurrence_id"]: row
        for row in r294["rows"]
        if row["registry_occurrence_id"] in occurrence_ids
    }
    need(set(registry) == occurrence_ids, "R294 exact endpoints")
    atom_ids = set()
    for row in registry.values():
        verify_row(row, "R294 selected registry row")
        need(
            row["registry_entry_kind"]
            == "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM"
            and row["formal_new_expanded_occurrence_credit"] == 1
            and row["positive_volume_rational_inner_support_box"] is not None,
            "R294 selected endpoint kind",
        )
        qbox(row["positive_volume_rational_inner_support_box"])
        atom_ids.add(row["canonical_atom_id"])
    need(len(atom_ids) == 256, "256 distinct canonical atoms")
    del r294
    gc.collect()

    # Reopen exact atoms and their complete ten-field signatures.
    r279 = read_gzip("R279")
    atoms = {
        row["canonical_atom_id"]: row
        for row in r279["rows"]
        if row["canonical_atom_id"] in atom_ids
    }
    need(set(atoms) == atom_ids, "R279 exact endpoint atoms")
    for row in atoms.values():
        verify_row(row, "R279 selected atom")
        need(
            row["new_occurrence_region_atom_candidate"] is True
            and row["support_classification"] == "WHOLE_ROUND182_LEAF"
            and row["complete_10_field_return_signature_sha256"]
            == digest(row["complete_10_field_return_signature"]),
            "R279 exact atom semantics",
        )
        qbox(row["whole_Round182_leaf_box"])
    leaf_ids = {row["Round182_leaf_row_id"] for row in atoms.values()}
    del r279
    gc.collect()

    # Reopen the exact R182 leaves.
    r182 = closed_result("R182")
    leaf_columns = r182["row_column_schemas"]["collar_leaf_rows"]
    leaves = {
        row["row_id"]: row
        for row in (
            dict(zip(leaf_columns, packed, strict=True))
            for packed in r182["collar_leaf_rows"]
        )
        if row["row_id"] in leaf_ids
    }
    need(set(leaves) == leaf_ids and len(leaves) == 128,
         "128 exact R182 leaves")
    selected_child_ids = {
        row["retained_child_row_id"] for row in leaves.values()
    }
    need(len(selected_child_ids) == 56, "56 selected retained children")
    for row in leaves.values():
        need(
            row["graph_classification"] == "CLIPPED_2D_BOUNDARY_1D"
            and row["two_dimensional_graph_sheet_count"] == 1
            and Q(row["base_coordinate_area"]) > 0,
            "R182 selected leaf graph sheet",
        )
        qbox(row["box"])
    del r182
    gc.collect()

    # Reopen selected R179 child metadata.
    r179 = closed_result("R179")
    retained_columns = r179["row_column_schemas"]["retained_3d_child_rows"]
    children = {
        row["row_id"]: row
        for row in (
            dict(zip(retained_columns, packed, strict=True))
            for packed in r179["retained_3d_child_rows"]
        )
        if row["row_id"] in selected_child_ids
    }
    need(set(children) == selected_child_ids, "R179 selected children")
    selected_origin_ids = {row["origin_row_id"] for row in children.values()}
    need(len(selected_origin_ids) == 48, "48 selected origins")
    del r179
    gc.collect()

    # Reopen retained-stratum candidates and their sealed origin promotions.
    r246 = closed_result("R246")
    r246_ledger = r246[
        "formal_new_whole_signature_retained_stratum_node_ledger"
    ]
    r246_nodes = verify_ledger(
        r246_ledger,
        "rows", "row_count", "row_ids_sha256", "row_hashes_sha256",
        "rows_sha256", "retained_stratum_node_id", "R246 nodes",
    )
    need(len(r246_nodes) == 2_220, "R246 node census")
    for row in r246_nodes:
        verify_row(row, "R246 node")

    r247 = closed_result("R247")
    r247_ledger = r247[
        "formal_new_crossing_and_source_seam_retained_stratum_node_ledger"
    ]
    r247_nodes = verify_ledger(
        r247_ledger,
        "rows", "row_count", "row_ids_sha256", "row_hashes_sha256",
        "rows_sha256", "retained_stratum_node_id", "R247 nodes",
    )
    need(len(r247_nodes) == 504, "R247 node census")
    for row in r247_nodes:
        verify_row(row, "R247 node")

    r232 = closed_result("R232")
    roots232 = {
        row["whole_origin_promotion_row_id"]: row
        for row in r232["whole_origin_promotion_rows"]
    }
    need(len(roots232) == 2_220, "R232 origin census")
    r238 = closed_result("R238")
    roots238 = {
        row["whole_origin_promotion_row_id"]: row
        for row in r238["whole_origin_promotion_rows"]
    }
    need(len(roots238) == 264, "R238 source-seam origin census")

    signature_sha256s = {
        row["complete_10_field_return_signature_sha256"]
        for row in atoms.values()
    }
    need(len(signature_sha256s) == 44, "44 endpoint signatures")
    by_signature_246: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_signature_247: dict[str, list[dict[str, Any]]] = defaultdict(list)
    selected_nodes_246: dict[str, dict[str, Any]] = {}
    selected_nodes_247: dict[str, dict[str, Any]] = {}
    for row in r246_nodes:
        signature_sha = digest(row["local_return_signature"])
        if signature_sha in signature_sha256s:
            by_signature_246[signature_sha].append(row)
            selected_nodes_246[row["retained_stratum_node_id"]] = row
    for row in r247_nodes:
        signature_sha = digest(row["local_return_signature"])
        if signature_sha in signature_sha256s:
            need(row["source_classification"] == "SOURCE_CHART_SEAM",
                 "R247 matching node is source seam")
            by_signature_247[signature_sha].append(row)
            selected_nodes_247[row["retained_stratum_node_id"]] = row
    for rows in by_signature_246.values():
        rows.sort(key=lambda row: row["retained_stratum_node_id"])
    for rows in by_signature_247.values():
        rows.sort(key=lambda row: row["retained_stratum_node_id"])
    need(
        len(selected_nodes_246) == 2_044
        and len(selected_nodes_247) == 216,
        "candidate node census",
    )

    candidate_interface_ids = {
        row["Round220_split_interface_id"]
        for row in selected_nodes_246.values()
    } | {
        row["Round220_split_interface_id"]
        for row in selected_nodes_247.values()
    }

    # Reopen the complete Round220 interface table.  Neither selected graph
    # child nor its containing origin occurs in any interface row.
    r220 = closed_result("R220")
    interface_table = r220["coordinate_boundary_atlas"]["tables"][
        "one_step_split_interface_rows"
    ]
    interface_rows = unpack(interface_table)
    need(len(interface_rows) == 13_076, "R220 complete interface census")
    interface_by_id = {
        row["split_interface_id"]: row for row in interface_rows
        if row["split_interface_id"] in candidate_interface_ids
    }
    all_interface_children = {
        child_id
        for row in interface_rows
        for child_id in (row["lower_child_row_id"], row["upper_child_row_id"])
    }
    all_interface_origins = {row["origin_row_id"] for row in interface_rows}
    need(
        set(interface_by_id) == candidate_interface_ids
        and selected_child_ids.isdisjoint(all_interface_children)
        and selected_origin_ids.isdisjoint(all_interface_origins),
        "R220 exact ancestor/interface exclusion",
    )
    del r220, interface_rows
    gc.collect()

    # Validate every candidate node back through its promotion and interface.
    r247_owner_relation_histogram: Counter[str] = Counter()
    for node in selected_nodes_246.values():
        root = roots232[node["Round232_whole_origin_promotion_row_id"]]
        interface = interface_by_id[node["Round220_split_interface_id"]]
        need(
            node["local_return_signature"] == root["local_return_signature"]
            and node["Round179_retained_child_row_id"]
            == root["Round179_retained_child_row_id"]
            and node["Round220_split_interface_id"]
            == root["Round220_split_interface_id"]
            and root["Round179_retained_child_row_id"]
            in {interface["lower_child_row_id"], interface["upper_child_row_id"]}
            and root["Round179_resolved_child_row_id"]
            in {interface["lower_child_row_id"], interface["upper_child_row_id"]},
            "R246 candidate ancestry",
        )
    for node in selected_nodes_247.values():
        root = roots238[node["source_whole_origin_promotion_row_id"]]
        interface = interface_by_id[node["Round220_split_interface_id"]]
        need(
            node["local_return_signature"]
            == root[
                "whole_box_signature_recomputation_ignoring_chart_class_precheck"
            ]
            and node["Round179_retained_child_row_id"]
            == root["Round179_retained_child_row_id"]
            and node["Round220_split_interface_id"]
            == root["Round220_split_interface_id"]
            and root["Round179_retained_child_row_id"]
            in {interface["lower_child_row_id"], interface["upper_child_row_id"]}
            and root["Round179_resolved_sibling_row_id"]
            in {interface["lower_child_row_id"], interface["upper_child_row_id"]},
            "R247 candidate ancestry",
        )

    # Construct one fail-closed ledger row per exact explicit pair.
    output_rows: list[dict[str, Any]] = []
    relation_246_whole: Counter[str] = Counter()
    relation_246_inner: Counter[str] = Counter()
    relation_247_whole: Counter[str] = Counter()
    relation_247_inner: Counter[str] = Counter()
    combined_multiplicity: Counter[str] = Counter()
    source_chart_histogram: Counter[str] = Counter()
    contact_same_parent: Counter[bool] = Counter()
    pair_contact_class: Counter[str] = Counter()
    physical_cell_index_histogram: Counter[int] = Counter()
    r246_relation_count = 0
    r247_relation_count = 0

    for source_pair in explicit:
        binding_id = source_pair[
            "R295A_physical_incidence_binding_row_ids"
        ][0]
        binding = bindings[binding_id]
        disposition = dispositions[binding["Round291_local_disposition_row_id"]]
        cell_index = binding["physical_witness_cell_index"]
        need(0 <= cell_index < len(disposition["physical_witness_cells"]),
             "selected physical cell index")
        cell = disposition["physical_witness_cells"][cell_index]
        leaf = leaves[cell["leaf_row_id"]]
        child = children[cell["retained_child_row_id"]]
        r293_row = r293_rows[
            binding["source_Round293_R291_physical_witness_binding_row_id"]
        ]
        pair_occurrences = source_pair[
            "canonical_unordered_Round294_registry_occurrence_ids"
        ]
        need(
            pair_occurrences == sorted(pair_occurrences)
            and binding["target_Round294_registry_occurrence_ids"]
            == pair_occurrences
            and r293_row["terminal_registry_target_references"]
            == pair_occurrences
            and cell["witness_kind"] == "ROUND182_GRAPH_SHEET_LEAF"
            and cell["graph_classification"] == "CLIPPED_2D_BOUNDARY_1D"
            and leaf["row_id"] == cell["leaf_row_id"]
            and leaf["retained_child_row_id"] == cell["retained_child_row_id"]
            and leaf["box"] == cell["exact_box"]
            and child["origin_row_id"]
            == disposition["containing_Round174_residual_row_id"]
            and child["parent_id"] == disposition["parent_id"]
            and child["chart"] == disposition["source_chart"],
            "exact pair witness lineage",
        )
        source_chart_histogram[disposition["source_chart"]] += 1
        physical_cell_index_histogram[cell_index] += 1
        leaf_box = qbox(cell["exact_box"])
        endpoint_rows: list[dict[str, Any]] = []
        pair_has_whole_contact = False
        pair_has_inner_contact = False
        pair_counts: list[int] = []

        for occurrence_id in pair_occurrences:
            registry_row = registry[occurrence_id]
            atom = atoms[registry_row["canonical_atom_id"]]
            signature_sha = atom[
                "complete_10_field_return_signature_sha256"
            ]
            inner_box = qbox(
                registry_row["positive_volume_rational_inner_support_box"]
            )
            need(
                atom["Round182_leaf_row_id"] == cell["leaf_row_id"]
                and atom["whole_Round182_leaf_box"] == cell["exact_box"]
                and atom["source_chart"] == disposition["source_chart"]
                and registry_row["Round182_leaf_row_id"] == cell["leaf_row_id"]
                and contains(leaf_box, inner_box),
                "endpoint atom and support lineage",
            )
            candidates246 = by_signature_246[signature_sha]
            candidates247 = by_signature_247[signature_sha]
            pair_counts.append(len(candidates246) + len(candidates247))
            r246_relation_count += len(candidates246)
            r247_relation_count += len(candidates247)
            contacts: list[dict[str, Any]] = []

            for node in candidates246:
                whole_relation = box_relation(
                    leaf_box, qbox(node["strict_positive_3D_witness_box"])
                )
                inner_relation = box_relation(
                    inner_box, qbox(node["strict_positive_3D_witness_box"])
                )
                relation_246_whole[whole_relation] += 1
                relation_246_inner[inner_relation] += 1
                need(
                    whole_relation
                    != "STRICT_POSITIVE_VOLUME_INTERSECTION"
                    and inner_relation
                    != "STRICT_POSITIVE_VOLUME_INTERSECTION",
                    "R246 strict volume intersection absent",
                )
                if whole_relation == "CLOSED_BOUNDARY_CONTACT":
                    pair_has_whole_contact = True
                    pair_has_inner_contact |= (
                        inner_relation == "CLOSED_BOUNDARY_CONTACT"
                    )
                    root = roots232[
                        node["Round232_whole_origin_promotion_row_id"]
                    ]
                    interface = interface_by_id[
                        node["Round220_split_interface_id"]
                    ]
                    same_parent = child["parent_id"] == root["parent_id"]
                    contact_same_parent[same_parent] += 1
                    need(
                        child["row_id"]
                        not in {
                            interface["lower_child_row_id"],
                            interface["upper_child_row_id"],
                        }
                        and child["origin_row_id"] != root["origin_row_id"]
                        and child["origin_row_id"] != interface["origin_row_id"],
                        "closed contact has no R220 ancestor attachment",
                    )
                    contacts.append({
                        "candidate_round": 246,
                        "retained_stratum_node_id":
                            node["retained_stratum_node_id"],
                        "node_strict_positive_3D_witness_box":
                            node["strict_positive_3D_witness_box"],
                        "Round220_split_interface_id":
                            node["Round220_split_interface_id"],
                        "interface_axis": interface["axis"],
                        "interface_fixed_coordinate":
                            interface["fixed_coordinate"],
                        "whole_leaf_box_relation": whole_relation,
                        "inner_support_box_relation": inner_relation,
                        "same_Round179_retained_child": False,
                        "same_Round174_origin": False,
                        "same_Round174_parent": same_parent,
                        "selected_child_is_interface_endpoint": False,
                        "selected_origin_is_interface_origin": False,
                        "closed_contact_implies_attachment": False,
                        "formal_component_edge_credit": 0,
                    })

            for node in candidates247:
                whole_relation = box_relation(
                    leaf_box,
                    qbox(node["strict_positive_3D_physical_witness_box"]),
                )
                inner_relation = box_relation(
                    inner_box,
                    qbox(node["strict_positive_3D_physical_witness_box"]),
                )
                relation_247_whole[whole_relation] += 1
                relation_247_inner[inner_relation] += 1
                need(
                    whole_relation == "DISJOINT"
                    and inner_relation == "DISJOINT",
                    "R247 exact geometric disjointness",
                )
                root = roots238[node["source_whole_origin_promotion_row_id"]]
                r247_owner_relation_histogram[
                    root["half_open_seam_owner_status"]
                ] += 1

            contacts.sort(key=lambda row: row["retained_stratum_node_id"])
            need(len(contacts) <= 1, "at most one closure-only contact")
            endpoint_rows.append({
                "Round294_registry_occurrence_id": occurrence_id,
                "Round294_occurrence_registry_row_id":
                    registry_row["Round294_occurrence_registry_row_id"],
                "Round294_occurrence_registry_row_sha256":
                    registry_row["row_sha256"],
                "Round279_canonical_atom_id": atom["canonical_atom_id"],
                "Round279_atom_row_sha256": atom["row_sha256"],
                "complete_10_field_return_signature":
                    atom["complete_10_field_return_signature"],
                "complete_10_field_return_signature_sha256": signature_sha,
                "whole_Round182_leaf_box": atom["whole_Round182_leaf_box"],
                "positive_volume_rational_inner_support_box":
                    registry_row["positive_volume_rational_inner_support_box"],
                "R246_exact_signature_candidate_node_count":
                    len(candidates246),
                "R246_exact_signature_candidate_node_ids_sha256": digest([
                    node["retained_stratum_node_id"] for node in candidates246
                ]),
                "R247_exact_signature_candidate_node_count":
                    len(candidates247),
                "R247_exact_signature_candidate_node_ids_sha256": digest([
                    node["retained_stratum_node_id"] for node in candidates247
                ]),
                "combined_signature_only_candidate_node_count":
                    len(candidates246) + len(candidates247),
                "R246_closure_only_contact_count": len(contacts),
                "R246_closure_only_contacts": contacts,
                "R246_strict_positive_volume_intersection_count": 0,
                "R247_closed_or_strict_intersection_count": 0,
                "signature_only_selection_eligible": False,
                "closed_contact_selection_eligible": False,
                "formal_owner_attachment_credit": 0,
            })

        contact_class = (
            "WHOLE_AND_INNER_CLOSED_CONTACT_ONLY"
            if pair_has_inner_contact
            else "WHOLE_CLOSED_CONTACT_ONLY"
            if pair_has_whole_contact
            else "NO_GEOMETRIC_CONTACT"
        )
        pair_contact_class[contact_class] += 1
        combined_multiplicity["|".join(map(str, pair_counts))] += 1
        payload = {
            "Round300G_explicit_outgoing_seam_exclusion_row_id":
                "round300g-explicit-outgoing-seam-exclusion:" + digest([
                    source_pair["Round300A_canonical_occurrence_pair_row_id"],
                    binding_id,
                    cell["leaf_row_id"],
                    pair_occurrences,
                ]),
            "source_Round300A_canonical_occurrence_pair_row_id":
                source_pair["Round300A_canonical_occurrence_pair_row_id"],
            "source_Round300A_canonical_occurrence_pair_row_sha256":
                source_pair["row_sha256"],
            "canonical_unordered_Round294_registry_occurrence_ids":
                pair_occurrences,
            "source_Round295A_physical_incidence_binding_row_id": binding_id,
            "source_Round295A_physical_incidence_binding_row_sha256":
                binding["row_sha256"],
            "source_Round293_physical_witness_binding_row_id":
                r293_row["Round292_R291_physical_witness_binding_row_id"],
            "source_Round293_physical_witness_binding_row_sha256":
                r293_row["row_sha256"],
            "source_Round291_local_disposition_row_id":
                disposition["complete_lower_stratum_local_disposition_row_id"],
            "source_Round291_local_disposition_row_sha256":
                disposition["row_sha256"],
            "physical_witness_cell_index": cell_index,
            "Round182_leaf_row_id": cell["leaf_row_id"],
            "Round179_retained_child_row_id": cell["retained_child_row_id"],
            "containing_Round174_residual_row_id":
                disposition["containing_Round174_residual_row_id"],
            "parent_id": disposition["parent_id"],
            "source_chart": disposition["source_chart"],
            "predicate_label": disposition["predicate_label"],
            "predicate_equation": disposition["predicate_equation"],
            "graph_classification": cell["graph_classification"],
            "exact_graph_leaf_box": cell["exact_box"],
            "endpoint_audits": endpoint_rows,
            "combined_signature_only_candidate_multiplicity": pair_counts,
            "selected_leaf_Round220_interface_count": 0,
            "selected_origin_Round220_interface_count": 0,
            "pair_geometric_contact_class": contact_class,
            "included_one_sided_owner_attachment_proved": False,
            "attachment_exclusion_reason":
                "NO_ROUND220_ANCESTOR_INTERFACE__NO_STRICT_VOLUME_"
                "INTERSECTION__CLOSED_CONTACT_INSUFFICIENT",
            "formal_component_edge_credit": 0,
            "formal_component_union_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_occurrence_identity_collapse_credit": 0,
            "formal_seam_edge_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
            "eligible_for_component_DSU_application": False,
        }
        output_rows.append(closed(payload))

    output_rows.sort(
        key=lambda row:
            row["Round300G_explicit_outgoing_seam_exclusion_row_id"]
    )
    need(
        len(output_rows) == 128
        and len({
            row["Round300G_explicit_outgoing_seam_exclusion_row_id"]
            for row in output_rows
        }) == 128,
        "output row census",
    )
    need(
        r246_relation_count == 18_108
        and r247_relation_count == 1_776
        and relation_246_whole
        == Counter({"DISJOINT": 18_076, "CLOSED_BOUNDARY_CONTACT": 32})
        and relation_246_inner
        == Counter({"DISJOINT": 18_092, "CLOSED_BOUNDARY_CONTACT": 16})
        and relation_247_whole == Counter({"DISJOINT": 1_776})
        and relation_247_inner == Counter({"DISJOINT": 1_776})
        and pair_contact_class == Counter({
            "NO_GEOMETRIC_CONTACT": 96,
            "WHOLE_CLOSED_CONTACT_ONLY": 16,
            "WHOLE_AND_INNER_CLOSED_CONTACT_ONLY": 16,
        })
        and contact_same_parent == Counter({True: 24, False: 8})
        and combined_multiplicity == Counter({
            "80|55": 31,
            "132|160": 27,
            "160|132": 17,
            "55|80": 13,
            "9|2": 10,
            "2|11": 8,
            "11|2": 8,
            "2|9": 6,
            "25|64": 4,
            "64|25": 4,
        })
        and source_chart_histogram
        == Counter({"G:E": 32, "G:N": 32, "G:S": 32, "G:W": 32})
        and r247_owner_relation_histogram == Counter({
            "E_OR_W_HALF_OPEN_OWNER": 844,
            "N_OR_S_EXCLUDES_DIAGONAL_TIE": 932,
        }),
        "complete rejection census",
    )

    row_ids = [
        row["Round300G_explicit_outgoing_seam_exclusion_row_id"]
        for row in output_rows
    ]
    ledger = {
        "schema": LEDGER_SCHEMA,
        "status":
            "FORMAL_128_EXPLICIT_OUTGOING_SEAM_ATTACHMENT_EXCLUSIONS__"
            "ZERO_COMPONENT_EDGE_CREDIT",
        "row_count": 128,
        "row_ids_sha256": digest(row_ids),
        "row_hashes_sha256": digest(
            [row["row_sha256"] for row in output_rows]
        ),
        "rows_sha256": digest(output_rows),
        "every_row_closed_by_own_SHA256": True,
        "rows": output_rows,
    }
    payload = {
        "schema": SCHEMA,
        "status":
            "PASS_ROUND300G_EXACT_128_R300A_EXPLICIT_OUTGOING_SEAM_"
            "CANDIDATES__ALL_ATTACHMENT_INELIGIBLE_FAIL_CLOSED",
        "producer_file_sha256": producer_sha256,
        "input_file_pins": {
            filename: sha256 for filename, sha256 in sorted(FILES.values())
        },
        "complete_selection_census": {
            "Round300A_canonical_pair_count": 3_232,
            "Round300A_explicit_selected_pair_count": 128,
            "Round300A_other_pair_count": 3_104,
            "selected_R295A_binding_count": 128,
            "selected_R293_binding_count": 128,
            "selected_R291_disposition_count": len(dispositions),
            "selected_R291_physical_witness_cell_count": 128,
            "selected_R182_leaf_count": 128,
            "selected_R179_retained_child_count": 56,
            "selected_Round174_origin_count": 48,
            "selected_Round294_endpoint_occurrence_count": 256,
            "selected_Round279_atom_count": 256,
            "distinct_complete_10_field_signature_count": 44,
            "source_chart_histogram": histogram(source_chart_histogram),
            "physical_witness_cell_index_histogram":
                histogram(physical_cell_index_histogram),
        },
        "candidate_exhaustion_census": {
            "R246_unique_signature_candidate_node_count": 2_044,
            "R247_unique_signature_candidate_node_count": 216,
            "R246_endpoint_node_relation_count": 18_108,
            "R247_endpoint_node_relation_count": 1_776,
            "combined_endpoint_node_relation_count": 19_884,
            "combined_pair_directional_multiplicity_histogram":
                histogram(combined_multiplicity),
            "R246_whole_leaf_box_relation_histogram":
                histogram(relation_246_whole),
            "R246_inner_support_box_relation_histogram":
                histogram(relation_246_inner),
            "R247_whole_leaf_box_relation_histogram":
                histogram(relation_247_whole),
            "R247_inner_support_box_relation_histogram":
                histogram(relation_247_inner),
            "pair_geometric_contact_class_histogram":
                histogram(pair_contact_class),
            "closure_only_contact_same_parent_histogram":
                histogram(contact_same_parent),
            "R247_candidate_owner_status_relation_histogram":
                histogram(r247_owner_relation_histogram),
        },
        "ancestor_and_geometry_exclusion": {
            "complete_Round220_one_step_split_interface_count": 13_076,
            "selected_leaf_child_with_Round220_interface_count": 0,
            "selected_origin_with_Round220_interface_count": 0,
            "R246_strict_positive_volume_intersection_count": 0,
            "R247_strict_positive_volume_intersection_count": 0,
            "R247_closed_boundary_contact_count": 0,
            "R246_closed_boundary_contact_count": 32,
            "R246_inner_support_closed_boundary_contact_count": 16,
            "R246_closed_contact_same_origin_count": 0,
            "R246_closed_contact_selected_child_is_interface_endpoint_count": 0,
            "closure_contact_implies_attachment": False,
            "signature_equality_implies_attachment": False,
            "owner_status_without_geometry_implies_attachment": False,
        },
        "exclusion_ledger": {
            "filename": LEDGER_PATH.name,
            "schema": ledger["schema"],
            "row_count": ledger["row_count"],
            "row_ids_sha256": ledger["row_ids_sha256"],
            "row_hashes_sha256": ledger["row_hashes_sha256"],
            "rows_sha256": ledger["rows_sha256"],
        },
        "strict_nonpromotion": {
            "formal_component_edge_credit": 0,
            "formal_component_union_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_occurrence_identity_collapse_credit": 0,
            "formal_seam_edge_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
            "eligible_pair_count_for_component_DSU_application": 0,
            "ineligible_pair_count": 128,
            "complete_component_frontier_claimed": False,
        },
    }
    result = {**payload, "result_sha256": digest(payload)}
    return ledger, result


def gzip_bytes(value: dict[str, Any]) -> bytes:
    output = BytesIO()
    with gzip.GzipFile(
        filename="",
        mode="wb",
        fileobj=output,
        compresslevel=9,
        mtime=0,
    ) as stream:
        stream.write(canonical(value))
    return output.getvalue()


def atomic_write(path: Path, data: bytes) -> None:
    with tempfile.NamedTemporaryFile(
        dir=HERE, prefix="." + path.name + ".", delete=False
    ) as stream:
        temporary = Path(stream.name)
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    os.chmod(temporary, 0o600)
    os.replace(temporary, path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    producer_sha256 = file_sha256(Path(__file__).resolve())
    ledger, result = build(producer_sha256)
    ledger_data = gzip_bytes(ledger)
    result_data = canonical(result) + b"\n"
    if args.no_write:
        for path, data in ((LEDGER_PATH, ledger_data), (RESULT_PATH, result_data)):
            need(
                path.exists() and path.read_bytes() == data,
                "deterministic replay:" + path.name,
            )
    else:
        atomic_write(LEDGER_PATH, ledger_data)
        atomic_write(RESULT_PATH, result_data)
    print(json.dumps({
        "status": result["status"],
        "excluded_pair_count": ledger["row_count"],
        "result_sha256": result["result_sha256"],
        "write": not args.no_write,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
