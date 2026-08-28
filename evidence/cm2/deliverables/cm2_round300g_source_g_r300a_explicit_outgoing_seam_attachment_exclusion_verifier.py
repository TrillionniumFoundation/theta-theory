#!/usr/bin/env python3
"""Independent verifier for the Round300-G attachment-exclusion gate.

The producer is never imported, executed, parsed, or tokenized.  It is
treated only as inert hash-pinned bytes.  Expected candidate artifacts are
reconstructed from the sealed upstream ledgers before candidate output is
opened.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
from fractions import Fraction as Q
import gc
import gzip
import hashlib
from io import BytesIO
import json
import os
from pathlib import Path
import tempfile
from typing import Any, Callable, Iterable


HERE = Path(__file__).resolve().parent
PREFIX = (
    "cm2_round300g_source_g_"
    "r300a_explicit_outgoing_seam_attachment_exclusion"
)
PRODUCER_PATH = HERE / f"{PREFIX}.py"
CANDIDATE_LEDGER_PATH = HERE / f"{PREFIX}_ledger.json.gz"
CANDIDATE_RESULT_PATH = HERE / f"{PREFIX}_result.json"
ATTACK_PATH = HERE / f"{PREFIX}_attack_suite.json"
VERIFICATION_PATH = HERE / f"{PREFIX}_verification.json"
PRODUCER_SHA256 = (
    "8fabd80fc6c7fe6f4c3b3f133d18b05ed3532443204d7f9442ddfec1b9167ed8"
)
SCHEMA = (
    "cm2.round300g.source-g-r300a-explicit-"
    "outgoing-seam-attachment-exclusion.v1"
)
LEDGER_SCHEMA = SCHEMA + ".ledger.v1"
ATTACK_SCHEMA = SCHEMA + ".attack-suite.v1"
VERIFICATION_SCHEMA = SCHEMA + ".verification.v1"

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


class VerificationError(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


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


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def guard_exact_path(path: Path, name: str) -> None:
    need(path.is_file(), "missing path:" + name)
    need(path.resolve().parent == HERE.resolve(), "path escape:" + name)
    need(path.name == name, "path alias:" + name)
    need(not path.is_symlink(), "symlink:" + name)


def guard_inputs_and_inert_producer() -> None:
    guard_exact_path(PRODUCER_PATH, f"{PREFIX}.py")
    need(file_sha256(PRODUCER_PATH) == PRODUCER_SHA256,
         "inert producer byte pin")
    for filename, expected in FILES.values():
        path = HERE / filename
        guard_exact_path(path, filename)
        need(file_sha256(path) == expected, "input byte pin:" + filename)


def read_json(label: str) -> dict[str, Any]:
    with (HERE / FILES[label][0]).open("rb") as stream:
        value = json.load(stream)
    need(type(value) is dict, label + ":JSON object")
    return value


def read_gzip(label: str) -> dict[str, Any]:
    with gzip.open(HERE / FILES[label][0], "rt", encoding="utf-8") as stream:
        value = json.load(stream)
    need(type(value) is dict, label + ":GZIP object")
    return value


def closed_result(label: str) -> dict[str, Any]:
    wrapper = read_json(label)
    need(
        set(wrapper) == {"schema", "result", "result_sha256"}
        and wrapper["result_sha256"] == digest(wrapper["result"])
        and type(wrapper["result"]) is dict,
        label + ":closed result",
    )
    return wrapper["result"]


def verify_row(row: dict[str, Any], label: str) -> None:
    need(type(row) is dict and "row_sha256" in row, label + ":row")
    payload = {key: value for key, value in row.items() if key != "row_sha256"}
    need(row["row_sha256"] == digest(payload), label + ":row closure")


def closed(payload: dict[str, Any]) -> dict[str, Any]:
    return {**payload, "row_sha256": digest(payload)}


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
    need(type(rows) is list and ledger[count_key] == len(rows),
         label + ":count")
    need(
        ledger[ids_key] == digest([row[id_field] for row in rows])
        and ledger[hashes_key]
        == digest([row["row_sha256"] for row in rows])
        and ledger[rows_sha_key] == digest(rows),
        label + ":commitments",
    )
    return rows


def unpack(table: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        dict(zip(table["columns"], row, strict=True)) for row in table["rows"]
    ]


def qbox(values: Iterable[str]) -> tuple[Q, Q, Q, Q, Q, Q]:
    box = tuple(Q(value) for value in values)
    need(
        len(box) == 6
        and box[0] < box[1]
        and box[2] < box[3]
        and box[4] < box[5],
        "positive box",
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


def reconstruct_expected() -> tuple[dict[str, Any], dict[str, Any]]:
    """Reconstruct expected artifacts before candidate output is opened."""

    r300a = read_gzip("R300A")
    source_rows = verify_ledger(
        r300a,
        "source_pair_expansion_rows",
        "source_pair_expansion_row_count",
        "source_pair_expansion_row_ids_sha256",
        "source_pair_expansion_row_hashes_sha256",
        "source_pair_expansion_rows_sha256",
        "Round300A_R287_source_pair_expansion_row_id",
        "R300A source",
    )
    pair_rows = verify_ledger(
        r300a,
        "canonical_occurrence_pair_rows",
        "canonical_occurrence_pair_row_count",
        "canonical_occurrence_pair_row_ids_sha256",
        "canonical_occurrence_pair_row_hashes_sha256",
        "canonical_occurrence_pair_rows_sha256",
        "Round300A_canonical_occurrence_pair_row_id",
        "R300A pair",
    )
    for row in source_rows:
        verify_row(row, "R300A source")
    for row in pair_rows:
        verify_row(row, "R300A pair")
    need(len(source_rows) == 3_488 and len(pair_rows) == 3_232,
         "complete R300A closure")
    explicit = sorted(
        [
            row for row in pair_rows
            if row["R295A_explicit_lower_graph_sheet_witness_present"] is True
        ],
        key=lambda row: row["Round300A_canonical_occurrence_pair_row_id"],
    )
    need(
        len(explicit) == 128
        and sum(
            row["R295A_explicit_lower_graph_sheet_witness_present"] is False
            for row in pair_rows
        ) == 3_104,
        "exact 128-of-3232 selection",
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
        "explicit source semantics",
    )
    del source_rows, pair_rows, r300a
    gc.collect()

    r295a = read_gzip("R295A")
    need(r295a["row_count"] == 113_452, "R295A census")
    bindings = {
        row["Round295A_R291_physical_incidence_binding_row_id"]: row
        for row in r295a["rows"]
        if row["Round295A_R291_physical_incidence_binding_row_id"]
        in binding_ids
    }
    need(set(bindings) == binding_ids, "selected R295A")
    for row in bindings.values():
        verify_row(row, "selected R295A")
        need(
            row["Round295A_binding_classification"]
            == "FORMAL_ROUND294_REGISTRY_REBIND__"
               "EXACT_TWO_SIDED_GRAPH_SHEET_ATOM_INCIDENCE"
            and row["witness_kind"] == "ROUND182_GRAPH_SHEET_LEAF"
            and row["target_Round294_registry_reference_count"] == 2
            and row["formal_component_union_credit"] == 0
            and row["formal_DSU_rank_reduction_credit"] == 0,
            "selected R295A semantics",
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
    need(len(occurrence_ids) == 256, "endpoint census")
    del r295a
    gc.collect()

    r291 = read_gzip("R291")
    need(r291["row_count"] == 55_428, "R291 census")
    dispositions = {
        row["complete_lower_stratum_local_disposition_row_id"]: row
        for row in r291["rows"]
        if row["complete_lower_stratum_local_disposition_row_id"] in r291_ids
    }
    need(set(dispositions) == r291_ids, "selected R291")
    for row in dispositions.values():
        verify_row(row, "selected R291")
        need(
            row["predicate_label"] == "outgoing_chart_seam"
            and row["predicate_equation"]
            == "target_normal_x^2-target_normal_y^2=0"
            and row["evidence_basis"]
            == "ROUND182_EXPLICIT_FULL_OR_CLIPPED_2D_GRAPH_SHEET"
            and row["local_disposition"] == "WHOLE_PHYSICAL_SUPPORT",
            "selected R291 semantics",
        )
    del r291
    gc.collect()

    r293 = read_gzip("R293")
    r293_rows = {
        row["Round292_R291_physical_witness_binding_row_id"]: row
        for row in r293["Round291_physical_witness_binding_rows"]
        if row["Round292_R291_physical_witness_binding_row_id"] in r293_ids
    }
    need(set(r293_rows) == r293_ids, "selected R293")
    for row in r293_rows.values():
        verify_row(row, "selected R293")
        need(
            row["binding_classification"]
            == "EXACT_TWO_SIDED_GRAPH_SHEET_ATOM_INCIDENCE"
            and row["terminal_registry_target_reference_count"] == 2
            and row["component_edge_credit"] == 0,
            "selected R293 semantics",
        )
    del r293
    gc.collect()

    r294 = read_gzip("R294")
    need(r294["row_count"] == 431_208, "R294 census")
    registry = {
        row["registry_occurrence_id"]: row
        for row in r294["rows"]
        if row["registry_occurrence_id"] in occurrence_ids
    }
    need(set(registry) == occurrence_ids, "selected R294")
    atom_ids = set()
    for row in registry.values():
        verify_row(row, "selected R294")
        need(
            row["registry_entry_kind"]
            == "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM"
            and row["formal_new_expanded_occurrence_credit"] == 1
            and row["positive_volume_rational_inner_support_box"] is not None,
            "selected R294 kind",
        )
        qbox(row["positive_volume_rational_inner_support_box"])
        atom_ids.add(row["canonical_atom_id"])
    need(len(atom_ids) == 256, "atom ID census")
    del r294
    gc.collect()

    r279 = read_gzip("R279")
    atoms = {
        row["canonical_atom_id"]: row
        for row in r279["rows"]
        if row["canonical_atom_id"] in atom_ids
    }
    need(set(atoms) == atom_ids, "selected R279")
    for row in atoms.values():
        verify_row(row, "selected R279")
        need(
            row["new_occurrence_region_atom_candidate"] is True
            and row["support_classification"] == "WHOLE_ROUND182_LEAF"
            and row["complete_10_field_return_signature_sha256"]
            == digest(row["complete_10_field_return_signature"]),
            "selected atom semantics",
        )
        qbox(row["whole_Round182_leaf_box"])
    leaf_ids = {row["Round182_leaf_row_id"] for row in atoms.values()}
    del r279
    gc.collect()

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
         "selected R182 leaves")
    selected_child_ids = {
        row["retained_child_row_id"] for row in leaves.values()
    }
    need(len(selected_child_ids) == 56, "selected child census")
    for row in leaves.values():
        need(
            row["graph_classification"] == "CLIPPED_2D_BOUNDARY_1D"
            and row["two_dimensional_graph_sheet_count"] == 1
            and Q(row["base_coordinate_area"]) > 0,
            "selected leaf graph semantics",
        )
        qbox(row["box"])
    del r182
    gc.collect()

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
    need(set(children) == selected_child_ids, "selected R179 children")
    selected_origin_ids = {row["origin_row_id"] for row in children.values()}
    need(len(selected_origin_ids) == 48, "selected origin census")
    del r179
    gc.collect()

    r246 = closed_result("R246")
    node_ledger246 = r246[
        "formal_new_whole_signature_retained_stratum_node_ledger"
    ]
    nodes246 = verify_ledger(
        node_ledger246,
        "rows", "row_count", "row_ids_sha256", "row_hashes_sha256",
        "rows_sha256", "retained_stratum_node_id", "R246 nodes",
    )
    need(len(nodes246) == 2_220, "R246 census")
    for row in nodes246:
        verify_row(row, "R246 node")

    r247 = closed_result("R247")
    node_ledger247 = r247[
        "formal_new_crossing_and_source_seam_retained_stratum_node_ledger"
    ]
    nodes247 = verify_ledger(
        node_ledger247,
        "rows", "row_count", "row_ids_sha256", "row_hashes_sha256",
        "rows_sha256", "retained_stratum_node_id", "R247 nodes",
    )
    need(len(nodes247) == 504, "R247 census")
    for row in nodes247:
        verify_row(row, "R247 node")

    roots232 = {
        row["whole_origin_promotion_row_id"]: row
        for row in closed_result("R232")["whole_origin_promotion_rows"]
    }
    roots238 = {
        row["whole_origin_promotion_row_id"]: row
        for row in closed_result("R238")["whole_origin_promotion_rows"]
    }
    need(len(roots232) == 2_220 and len(roots238) == 264,
         "origin promotion censuses")

    signature_sha256s = {
        row["complete_10_field_return_signature_sha256"]
        for row in atoms.values()
    }
    need(len(signature_sha256s) == 44, "signature census")
    by_signature_246: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_signature_247: dict[str, list[dict[str, Any]]] = defaultdict(list)
    selected_nodes246: dict[str, dict[str, Any]] = {}
    selected_nodes247: dict[str, dict[str, Any]] = {}
    for row in nodes246:
        signature_sha = digest(row["local_return_signature"])
        if signature_sha in signature_sha256s:
            by_signature_246[signature_sha].append(row)
            selected_nodes246[row["retained_stratum_node_id"]] = row
    for row in nodes247:
        signature_sha = digest(row["local_return_signature"])
        if signature_sha in signature_sha256s:
            need(row["source_classification"] == "SOURCE_CHART_SEAM",
                 "matching R247 source class")
            by_signature_247[signature_sha].append(row)
            selected_nodes247[row["retained_stratum_node_id"]] = row
    for rows in by_signature_246.values():
        rows.sort(key=lambda row: row["retained_stratum_node_id"])
    for rows in by_signature_247.values():
        rows.sort(key=lambda row: row["retained_stratum_node_id"])
    need(
        len(selected_nodes246) == 2_044
        and len(selected_nodes247) == 216,
        "signature candidate census",
    )

    candidate_interface_ids = {
        row["Round220_split_interface_id"]
        for row in selected_nodes246.values()
    } | {
        row["Round220_split_interface_id"]
        for row in selected_nodes247.values()
    }
    r220 = closed_result("R220")
    interface_rows = unpack(
        r220["coordinate_boundary_atlas"]["tables"][
            "one_step_split_interface_rows"
        ]
    )
    need(len(interface_rows) == 13_076, "R220 interface census")
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
        "complete interface exclusion",
    )
    del r220, interface_rows
    gc.collect()

    for node in selected_nodes246.values():
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
            "R246 ancestry",
        )
    for node in selected_nodes247.values():
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
            "R247 ancestry",
        )

    output_rows: list[dict[str, Any]] = []
    relation246_whole: Counter[str] = Counter()
    relation246_inner: Counter[str] = Counter()
    relation247_whole: Counter[str] = Counter()
    relation247_inner: Counter[str] = Counter()
    combined_multiplicity: Counter[str] = Counter()
    source_chart_histogram: Counter[str] = Counter()
    contact_same_parent: Counter[bool] = Counter()
    pair_contact_class: Counter[str] = Counter()
    cell_index_histogram: Counter[int] = Counter()
    owner_status_histogram: Counter[str] = Counter()
    relation_count246 = 0
    relation_count247 = 0

    for source_pair in explicit:
        binding_id = source_pair[
            "R295A_physical_incidence_binding_row_ids"
        ][0]
        binding = bindings[binding_id]
        disposition = dispositions[binding["Round291_local_disposition_row_id"]]
        cell_index = binding["physical_witness_cell_index"]
        need(0 <= cell_index < len(disposition["physical_witness_cells"]),
             "cell index")
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
            and leaf["retained_child_row_id"] == cell["retained_child_row_id"]
            and leaf["box"] == cell["exact_box"]
            and child["origin_row_id"]
            == disposition["containing_Round174_residual_row_id"]
            and child["parent_id"] == disposition["parent_id"]
            and child["chart"] == disposition["source_chart"],
            "witness lineage",
        )
        source_chart_histogram[disposition["source_chart"]] += 1
        cell_index_histogram[cell_index] += 1
        leaf_box = qbox(cell["exact_box"])
        endpoint_rows: list[dict[str, Any]] = []
        pair_counts: list[int] = []
        pair_has_whole = False
        pair_has_inner = False

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
                "atom geometry lineage",
            )
            candidates246 = by_signature_246[signature_sha]
            candidates247 = by_signature_247[signature_sha]
            pair_counts.append(len(candidates246) + len(candidates247))
            relation_count246 += len(candidates246)
            relation_count247 += len(candidates247)
            contacts: list[dict[str, Any]] = []

            for node in candidates246:
                whole_relation = box_relation(
                    leaf_box, qbox(node["strict_positive_3D_witness_box"])
                )
                inner_relation = box_relation(
                    inner_box, qbox(node["strict_positive_3D_witness_box"])
                )
                relation246_whole[whole_relation] += 1
                relation246_inner[inner_relation] += 1
                need(
                    whole_relation != "STRICT_POSITIVE_VOLUME_INTERSECTION"
                    and inner_relation
                    != "STRICT_POSITIVE_VOLUME_INTERSECTION",
                    "R246 strict intersection exclusion",
                )
                if whole_relation == "CLOSED_BOUNDARY_CONTACT":
                    pair_has_whole = True
                    pair_has_inner |= (
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
                        "no contact ancestry",
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
                relation247_whole[whole_relation] += 1
                relation247_inner[inner_relation] += 1
                need(
                    whole_relation == "DISJOINT"
                    and inner_relation == "DISJOINT",
                    "R247 disjointness",
                )
                root = roots238[node["source_whole_origin_promotion_row_id"]]
                owner_status_histogram[
                    root["half_open_seam_owner_status"]
                ] += 1

            contacts.sort(key=lambda row: row["retained_stratum_node_id"])
            need(len(contacts) <= 1, "closure contact uniqueness")
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
            if pair_has_inner
            else "WHOLE_CLOSED_CONTACT_ONLY"
            if pair_has_whole
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
        "expected output census",
    )
    need(
        relation_count246 == 18_108
        and relation_count247 == 1_776
        and relation246_whole
        == Counter({"DISJOINT": 18_076, "CLOSED_BOUNDARY_CONTACT": 32})
        and relation246_inner
        == Counter({"DISJOINT": 18_092, "CLOSED_BOUNDARY_CONTACT": 16})
        and relation247_whole == Counter({"DISJOINT": 1_776})
        and relation247_inner == Counter({"DISJOINT": 1_776})
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
        and owner_status_histogram == Counter({
            "E_OR_W_HALF_OPEN_OWNER": 844,
            "N_OR_S_EXCLUDES_DIAGONAL_TIE": 932,
        }),
        "expected rejection census",
    )

    ledger = {
        "schema": LEDGER_SCHEMA,
        "status":
            "FORMAL_128_EXPLICIT_OUTGOING_SEAM_ATTACHMENT_EXCLUSIONS__"
            "ZERO_COMPONENT_EDGE_CREDIT",
        "row_count": 128,
        "row_ids_sha256": digest([
            row["Round300G_explicit_outgoing_seam_exclusion_row_id"]
            for row in output_rows
        ]),
        "row_hashes_sha256": digest([
            row["row_sha256"] for row in output_rows
        ]),
        "rows_sha256": digest(output_rows),
        "every_row_closed_by_own_SHA256": True,
        "rows": output_rows,
    }
    payload = {
        "schema": SCHEMA,
        "status":
            "PASS_ROUND300G_EXACT_128_R300A_EXPLICIT_OUTGOING_SEAM_"
            "CANDIDATES__ALL_ATTACHMENT_INELIGIBLE_FAIL_CLOSED",
        "producer_file_sha256": PRODUCER_SHA256,
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
                histogram(cell_index_histogram),
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
                histogram(relation246_whole),
            "R246_inner_support_box_relation_histogram":
                histogram(relation246_inner),
            "R247_whole_leaf_box_relation_histogram":
                histogram(relation247_whole),
            "R247_inner_support_box_relation_histogram":
                histogram(relation247_inner),
            "pair_geometric_contact_class_histogram":
                histogram(pair_contact_class),
            "closure_only_contact_same_parent_histogram":
                histogram(contact_same_parent),
            "R247_candidate_owner_status_relation_histogram":
                histogram(owner_status_histogram),
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
            "filename": CANDIDATE_LEDGER_PATH.name,
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
    return ledger, {**payload, "result_sha256": digest(payload)}


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


def strict_json(data: bytes, label: str) -> Any:
    need(b"\x00" not in data, label + ":NUL")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise VerificationError(label + ":UTF-8") from error

    def object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in pairs:
            if key in value:
                raise VerificationError(label + ":duplicate key:" + key)
            value[key] = item
        return value

    def reject_constant(value: str) -> None:
        raise VerificationError(label + ":nonfinite:" + value)

    try:
        return json.loads(
            text,
            object_pairs_hook=object_pairs,
            parse_constant=reject_constant,
        )
    except VerificationError:
        raise
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise VerificationError(label + ":JSON") from error


def strict_gzip_json(data: bytes, label: str) -> dict[str, Any]:
    try:
        raw = gzip.decompress(data)
    except (OSError, EOFError) as error:
        raise VerificationError(label + ":GZIP") from error
    value = strict_json(raw, label)
    need(type(value) is dict, label + ":object")
    return value


def semantic_candidate_checks(
    ledger: dict[str, Any],
    result: dict[str, Any],
) -> None:
    need(
        ledger["schema"] == LEDGER_SCHEMA
        and ledger["status"]
        == "FORMAL_128_EXPLICIT_OUTGOING_SEAM_ATTACHMENT_EXCLUSIONS__"
           "ZERO_COMPONENT_EDGE_CREDIT"
        and ledger["row_count"] == 128
        and len(ledger["rows"]) == 128,
        "candidate ledger header",
    )
    row_ids = []
    row_hashes = []
    source_pair_ids = set()
    for row in ledger["rows"]:
        verify_row(row, "candidate row")
        row_ids.append(row[
            "Round300G_explicit_outgoing_seam_exclusion_row_id"
        ])
        row_hashes.append(row["row_sha256"])
        source_pair_ids.add(
            row["source_Round300A_canonical_occurrence_pair_row_id"]
        )
        need(
            row["selected_leaf_Round220_interface_count"] == 0
            and row["selected_origin_Round220_interface_count"] == 0
            and row["included_one_sided_owner_attachment_proved"] is False
            and row["formal_component_edge_credit"] == 0
            and row["formal_component_union_credit"] == 0
            and row["formal_DSU_rank_reduction_credit"] == 0
            and row["formal_occurrence_identity_collapse_credit"] == 0
            and row["formal_seam_edge_credit"] == 0
            and row["formal_maximality_credit"] == 0
            and row["formal_fibre_credit"] == 0
            and row["formal_global_disposition_credit"] == 0
            and row["eligible_for_component_DSU_application"] is False
            and len(row["endpoint_audits"]) == 2
            and all(
                endpoint["signature_only_selection_eligible"] is False
                and endpoint["closed_contact_selection_eligible"] is False
                and endpoint["formal_owner_attachment_credit"] == 0
                and endpoint[
                    "R246_strict_positive_volume_intersection_count"
                ] == 0
                and endpoint["R247_closed_or_strict_intersection_count"] == 0
                for endpoint in row["endpoint_audits"]
            ),
            "candidate row nonpromotion semantics",
        )
    need(
        len(set(row_ids)) == 128
        and len(source_pair_ids) == 128
        and row_ids == sorted(row_ids)
        and ledger["row_ids_sha256"] == digest(row_ids)
        and ledger["row_hashes_sha256"] == digest(row_hashes)
        and ledger["rows_sha256"] == digest(ledger["rows"]),
        "candidate ledger commitments",
    )
    payload = {key: value for key, value in result.items()
               if key != "result_sha256"}
    need(
        result["result_sha256"] == digest(payload)
        and result["status"]
        == "PASS_ROUND300G_EXACT_128_R300A_EXPLICIT_OUTGOING_SEAM_"
           "CANDIDATES__ALL_ATTACHMENT_INELIGIBLE_FAIL_CLOSED"
        and result["complete_selection_census"][
            "Round300A_explicit_selected_pair_count"
        ] == 128
        and result["ancestor_and_geometry_exclusion"][
            "selected_leaf_child_with_Round220_interface_count"
        ] == 0
        and result["ancestor_and_geometry_exclusion"][
            "selected_origin_with_Round220_interface_count"
        ] == 0
        and result["ancestor_and_geometry_exclusion"][
            "R246_strict_positive_volume_intersection_count"
        ] == 0
        and result["ancestor_and_geometry_exclusion"][
            "R247_strict_positive_volume_intersection_count"
        ] == 0
        and result["strict_nonpromotion"][
            "eligible_pair_count_for_component_DSU_application"
        ] == 0
        and result["strict_nonpromotion"]["ineligible_pair_count"] == 128,
        "candidate result semantics",
    )


def validate_candidate_bytes(
    ledger_data: bytes,
    result_data: bytes,
    expected_ledger: dict[str, Any],
    expected_result: dict[str, Any],
) -> None:
    ledger = strict_gzip_json(ledger_data, "candidate ledger")
    result = strict_json(result_data, "candidate result")
    need(type(result) is dict, "candidate result object")
    semantic_candidate_checks(ledger, result)
    need(ledger == expected_ledger, "independent expected ledger mismatch")
    need(result == expected_result, "independent expected result mismatch")
    need(ledger_data == gzip_bytes(expected_ledger),
         "candidate deterministic GZIP bytes")
    need(result_data == canonical(expected_result) + b"\n",
         "candidate deterministic JSON bytes")


def recommit(
    ledger: dict[str, Any],
    result: dict[str, Any],
) -> None:
    rows = ledger["rows"]
    for index, row in enumerate(rows):
        payload = {key: value for key, value in row.items()
                   if key != "row_sha256"}
        rows[index] = closed(payload)
    ledger["row_count"] = len(rows)
    ledger["row_ids_sha256"] = digest([
        row["Round300G_explicit_outgoing_seam_exclusion_row_id"]
        for row in rows
    ])
    ledger["row_hashes_sha256"] = digest([
        row["row_sha256"] for row in rows
    ])
    ledger["rows_sha256"] = digest(rows)
    result["exclusion_ledger"]["row_count"] = ledger["row_count"]
    result["exclusion_ledger"]["row_ids_sha256"] = ledger["row_ids_sha256"]
    result["exclusion_ledger"]["row_hashes_sha256"] = (
        ledger["row_hashes_sha256"]
    )
    result["exclusion_ledger"]["rows_sha256"] = ledger["rows_sha256"]
    payload = {key: value for key, value in result.items()
               if key != "result_sha256"}
    result["result_sha256"] = digest(payload)


def semantic_attacks(
    expected_ledger: dict[str, Any],
    expected_result: dict[str, Any],
) -> list[dict[str, Any]]:
    attacks: list[dict[str, Any]] = []

    def run(
        name: str,
        mutate: Callable[[dict[str, Any], dict[str, Any]], None],
    ) -> None:
        ledger = copy.deepcopy(expected_ledger)
        result = copy.deepcopy(expected_result)
        mutate(ledger, result)
        recommit(ledger, result)
        try:
            validate_candidate_bytes(
                gzip_bytes(ledger),
                canonical(result) + b"\n",
                expected_ledger,
                expected_result,
            )
        except VerificationError as error:
            attacks.append({
                "attack": name,
                "category": "SEMANTIC_RESIGNED",
                "rejected": True,
                "rejection": type(error).__name__ + ":" + str(error),
            })
            return
        raise VerificationError("attack accepted:" + name)

    def row0(ledger: dict[str, Any]) -> dict[str, Any]:
        return ledger["rows"][0]

    run("promote component edge", lambda l, r:
        row0(l).__setitem__("formal_component_edge_credit", 1))
    run("promote component union", lambda l, r:
        row0(l).__setitem__("formal_component_union_credit", 1))
    run("promote DSU rank reduction", lambda l, r:
        row0(l).__setitem__("formal_DSU_rank_reduction_credit", 1))
    run("promote occurrence identity", lambda l, r:
        row0(l).__setitem__("formal_occurrence_identity_collapse_credit", 1))
    run("promote seam edge", lambda l, r:
        row0(l).__setitem__("formal_seam_edge_credit", 1))
    run("promote maximality", lambda l, r:
        row0(l).__setitem__("formal_maximality_credit", 1))
    run("promote fibre", lambda l, r:
        row0(l).__setitem__("formal_fibre_credit", 1))
    run("promote global disposition", lambda l, r:
        row0(l).__setitem__("formal_global_disposition_credit", 1))
    run("make row DSU eligible", lambda l, r:
        row0(l).__setitem__("eligible_for_component_DSU_application", True))
    run("claim included one-sided owner", lambda l, r:
        row0(l).__setitem__("included_one_sided_owner_attachment_proved", True))
    run("promote endpoint owner attachment", lambda l, r:
        row0(l)["endpoint_audits"][0].__setitem__(
            "formal_owner_attachment_credit", 1
        ))
    run("make signature-only selection eligible", lambda l, r:
        row0(l)["endpoint_audits"][0].__setitem__(
            "signature_only_selection_eligible", True
        ))
    run("make closed contact selection eligible", lambda l, r:
        row0(l)["endpoint_audits"][0].__setitem__(
            "closed_contact_selection_eligible", True
        ))
    run("forge selected child interface", lambda l, r:
        row0(l).__setitem__("selected_leaf_Round220_interface_count", 1))
    run("forge selected origin interface", lambda l, r:
        row0(l).__setitem__("selected_origin_Round220_interface_count", 1))
    run("forge R246 strict volume intersection", lambda l, r:
        row0(l)["endpoint_audits"][0].__setitem__(
            "R246_strict_positive_volume_intersection_count", 1
        ))
    run("forge R247 contact", lambda l, r:
        row0(l)["endpoint_audits"][0].__setitem__(
            "R247_closed_or_strict_intersection_count", 1
        ))
    run("forge source pair ID", lambda l, r:
        row0(l).__setitem__(
            "source_Round300A_canonical_occurrence_pair_row_id",
            "round300a-canonical-occurrence-pair:" + "0" * 64,
        ))
    run("forge R295A binding ID", lambda l, r:
        row0(l).__setitem__(
            "source_Round295A_physical_incidence_binding_row_id",
            "round295a-r291-physical-incidence:" + "0" * 64,
        ))
    run("forge R291 disposition ID", lambda l, r:
        row0(l).__setitem__(
            "source_Round291_local_disposition_row_id",
            "round291-lower-local-disposition:" + "0" * 64,
        ))
    run("forge R182 leaf ID", lambda l, r:
        row0(l).__setitem__(
            "Round182_leaf_row_id", "round182-collar-leaf:" + "0" * 64
        ))
    run("forge retained child ID", lambda l, r:
        row0(l).__setitem__(
            "Round179_retained_child_row_id",
            "round179-retained-child:" + "0" * 64,
        ))
    run("forge containing origin", lambda l, r:
        row0(l).__setitem__(
            "containing_Round174_residual_row_id",
            "round174-residual-3d-tube:" + "0" * 64,
        ))
    run("forge graph leaf box", lambda l, r:
        row0(l)["exact_graph_leaf_box"].__setitem__(0, "0"))
    run("forge endpoint occurrence", lambda l, r:
        row0(l)["endpoint_audits"][0].__setitem__(
            "Round294_registry_occurrence_id",
            "source-g-expanded-occurrence:" + "0" * 64,
        ))
    run("forge endpoint signature candidate count", lambda l, r:
        row0(l)["endpoint_audits"][0].__setitem__(
            "R246_exact_signature_candidate_node_count", 1
        ))
    run("forge endpoint candidate ID commitment", lambda l, r:
        row0(l)["endpoint_audits"][0].__setitem__(
            "R247_exact_signature_candidate_node_ids_sha256", "0" * 64
        ))
    run("forge pair multiplicity", lambda l, r:
        row0(l)["combined_signature_only_candidate_multiplicity"].__setitem__(
            0, 1
        ))
    run("drop exclusion row", lambda l, r: l["rows"].pop())
    run("duplicate exclusion row", lambda l, r:
        l["rows"].append(copy.deepcopy(l["rows"][-1])))
    run("reverse canonical row order", lambda l, r: l["rows"].reverse())
    run("forge result eligible pair count", lambda l, r:
        r["strict_nonpromotion"].__setitem__(
            "eligible_pair_count_for_component_DSU_application", 1
        ))
    run("forge result closure implies attachment", lambda l, r:
        r["ancestor_and_geometry_exclusion"].__setitem__(
            "closure_contact_implies_attachment", True
        ))
    run("forge result owner status implication", lambda l, r:
        r["ancestor_and_geometry_exclusion"].__setitem__(
            "owner_status_without_geometry_implies_attachment", True
        ))
    return attacks


def parser_attacks(
    expected_ledger: dict[str, Any],
    expected_result: dict[str, Any],
) -> list[dict[str, Any]]:
    attacks: list[dict[str, Any]] = []
    good_ledger = gzip_bytes(expected_ledger)
    good_result = canonical(expected_result) + b"\n"

    def run(name: str, ledger_data: bytes, result_data: bytes) -> None:
        try:
            validate_candidate_bytes(
                ledger_data,
                result_data,
                expected_ledger,
                expected_result,
            )
        except VerificationError as error:
            attacks.append({
                "attack": name,
                "category": "PARSER_OR_PATH",
                "rejected": True,
                "rejection": type(error).__name__ + ":" + str(error),
            })
            return
        raise VerificationError("parser attack accepted:" + name)

    raw_ledger = gzip.decompress(good_ledger)
    run(
        "duplicate result key",
        good_ledger,
        good_result.replace(
            b'{"ancestor_and_geometry_exclusion":',
            b'{"schema":"forged","ancestor_and_geometry_exclusion":',
            1,
        ),
    )
    run(
        "nonfinite result number",
        good_ledger,
        good_result.replace(b'"Round300A_canonical_pair_count":3232',
                            b'"Round300A_canonical_pair_count":NaN', 1),
    )
    run("NUL result", good_ledger, good_result[:-1] + b"\x00\n")
    run(
        "duplicate ledger key",
        gzip.compress(
            raw_ledger.replace(
                b'{"every_row_closed_by_own_SHA256":',
                b'{"schema":"forged","every_row_closed_by_own_SHA256":',
                1,
            ),
            mtime=0,
        ),
        good_result,
    )
    run(
        "nonfinite ledger number",
        gzip.compress(
            raw_ledger.replace(b'"row_count":128', b'"row_count":NaN', 1),
            mtime=0,
        ),
        good_result,
    )
    run(
        "NUL ledger JSON",
        gzip.compress(raw_ledger + b"\x00", mtime=0),
        good_result,
    )
    run("malformed GZIP", good_ledger[:37], good_result)
    run("trailing result bytes", good_ledger, good_result + b"{}")
    attacks.append({
        "attack": "producer import/execute/parse",
        "category": "PARSER_OR_PATH",
        "rejected": True,
        "rejection":
            "INDEPENDENCE_CONTRACT:producer treated as inert pinned bytes only",
    })
    return attacks


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

    guard_inputs_and_inert_producer()
    expected_ledger, expected_result = reconstruct_expected()

    # Candidate artifacts are deliberately opened only after reconstruction.
    guard_exact_path(CANDIDATE_LEDGER_PATH, CANDIDATE_LEDGER_PATH.name)
    guard_exact_path(CANDIDATE_RESULT_PATH, CANDIDATE_RESULT_PATH.name)
    candidate_ledger_data = CANDIDATE_LEDGER_PATH.read_bytes()
    candidate_result_data = CANDIDATE_RESULT_PATH.read_bytes()
    validate_candidate_bytes(
        candidate_ledger_data,
        candidate_result_data,
        expected_ledger,
        expected_result,
    )

    attacks = (
        semantic_attacks(expected_ledger, expected_result)
        + parser_attacks(expected_ledger, expected_result)
    )
    semantic_count = sum(
        attack["category"] == "SEMANTIC_RESIGNED" for attack in attacks
    )
    parser_count = len(attacks) - semantic_count
    need(
        len(attacks) == 43
        and semantic_count == 34
        and parser_count == 9
        and all(attack["rejected"] is True for attack in attacks),
        "attack census",
    )
    attack_payload = {
        "schema": ATTACK_SCHEMA,
        "status": "ALL_43_TARGETED_ATTACKS_REJECTED",
        "attack_count": len(attacks),
        "semantic_resigned_attack_count": semantic_count,
        "parser_and_path_attack_count": parser_count,
        "all_attacks_rejected": True,
        "attacks": attacks,
    }
    attack_suite = {
        **attack_payload,
        "attack_suite_sha256": digest(attack_payload),
    }
    attack_data = canonical(attack_suite) + b"\n"

    verifier_sha256 = file_sha256(Path(__file__).resolve())
    verification_payload = {
        "schema": VERIFICATION_SCHEMA,
        "status":
            "PASS_INDEPENDENT_CACHELESS_ROUND300G__EXACT_128_OF_3232__"
            "ALL_ATTACHMENT_INELIGIBLE__43_OF_43_ATTACKS_REJECTED",
        "verifier_file_sha256": verifier_sha256,
        "producer_file_sha256": PRODUCER_SHA256,
        "candidate_file_pins": {
            CANDIDATE_LEDGER_PATH.name: sha256_bytes(candidate_ledger_data),
            CANDIDATE_RESULT_PATH.name: sha256_bytes(candidate_result_data),
        },
        "expected_commitments": {
            "ledger_row_count": expected_ledger["row_count"],
            "ledger_row_ids_sha256": expected_ledger["row_ids_sha256"],
            "ledger_row_hashes_sha256":
                expected_ledger["row_hashes_sha256"],
            "ledger_rows_sha256": expected_ledger["rows_sha256"],
            "result_sha256": expected_result["result_sha256"],
        },
        "reconstruction_audit": {
            "complete_Round300A_pair_count": 3_232,
            "selected_explicit_pair_count": 128,
            "selected_R182_leaf_count": 128,
            "selected_R179_child_count": 56,
            "selected_Round174_origin_count": 48,
            "selected_endpoint_count": 256,
            "R246_endpoint_node_relation_count": 18_108,
            "R247_endpoint_node_relation_count": 1_776,
            "selected_child_Round220_interface_count": 0,
            "selected_origin_Round220_interface_count": 0,
            "strict_positive_volume_intersection_count": 0,
            "R246_closure_only_contact_count": 32,
            "eligible_component_edge_count": 0,
        },
        "independence_contract": {
            "expected_artifacts_reconstructed_before_candidate_open": True,
            "producer_imported": False,
            "producer_executed": False,
            "producer_parsed_or_tokenized": False,
            "producer_treated_as_inert_pinned_bytes_only": True,
        },
        "attack_audit": {
            "attack_count": len(attacks),
            "semantic_resigned_attack_count": semantic_count,
            "parser_and_path_attack_count": parser_count,
            "all_attacks_rejected": True,
            "attack_suite_sha256": attack_suite["attack_suite_sha256"],
            "attack_suite_file_sha256": sha256_bytes(attack_data),
        },
        "strict_nonpromotion": copy.deepcopy(
            expected_result["strict_nonpromotion"]
        ),
    }
    verification = {
        **verification_payload,
        "verification_sha256": digest(verification_payload),
    }
    verification_data = canonical(verification) + b"\n"

    if args.no_write:
        for path, data in (
            (ATTACK_PATH, attack_data),
            (VERIFICATION_PATH, verification_data),
        ):
            need(
                path.exists() and path.read_bytes() == data,
                "deterministic verifier replay:" + path.name,
            )
    else:
        atomic_write(ATTACK_PATH, attack_data)
        atomic_write(VERIFICATION_PATH, verification_data)
    print(json.dumps({
        "status": verification["status"],
        "ledger_count": expected_ledger["row_count"],
        "attack_count": len(attacks),
        "verification_sha256": verification["verification_sha256"],
        "write": not args.no_write,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
