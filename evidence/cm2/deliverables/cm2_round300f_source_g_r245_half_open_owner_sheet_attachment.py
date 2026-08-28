#!/usr/bin/env python3
"""Promote the unique half-open owner of each Round245 transition sheet.

The construction is intentionally narrow.  It reopens the complete
Round291 graph-witness and Round266 virtual-node frontiers, identifies the
264 Round245 sheets by exact Round179/Round182 lineage and geometry, and
selects exactly one Round294 occurrence per sheet by full-signature equality
with the Round242 half-open owner.  The opposite shadow occurrence is retained
as incidence-only evidence and receives no component-edge credit.
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
import mmap
import os
from pathlib import Path
import stat
import tempfile
from typing import Any, Iterable, Iterator


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round300f_source_g_r245_half_open_owner_sheet_attachment"
LEDGER_PATH = HERE / f"{PREFIX}_ledger.json.gz"
RESULT_PATH = HERE / f"{PREFIX}_result.json"

SCHEMA = "cm2.round300f.source-g-r245-half-open-owner-sheet-attachment.v1"
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
        "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json",
        "569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974",
    ),
    "R233": (
        "cm2_round233_source_g_outgoing_seam_parametric_graph_key_partition_certificate.json",
        "cb2f74daa9836841ce311d8d555c2d94ba897f346a63c1e29551d7f99e8d1a41",
    ),
    "R242": (
        "cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_certificate.json",
        "8d32c381e21c03aad6a531b7e5a527d295783b7e3e38baa1e6bcba20c40db22e",
    ),
    "R245": (
        "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json",
        "c76662f7cb068127f3612a3655ae720662eead9b9210b5757d771693149883c1",
    ),
    "R266": (
        "cm2_round266_source_g_expanded_curved_face_closure_certificate.json",
        "2d30be104dc522ebb1664129894acf851180b9e5f51dd8471c33137447b599bf",
    ),
    "R279": (
        "cm2_round279_source_g_collar_atom_and_face_edge_freeze_atoms.json.gz",
        "283a10799e0c7d1156695c30cdb2533488602ca646a18804f93211c0a3132dbe",
    ),
    "R288": (
        "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_atom_dispositions.json.gz",
        "6b0a8aa1cd38019322a61f5aaefc936006d10769cd21a5c8df374576f9ac570a",
    ),
    "R291": (
        "cm2_round291_source_g_complete_lower_stratum_local_disposition_freeze_ledger.json.gz",
        "412b616b2cf75ef1373d98086cfcb2eb90a8c544e9f6b4d16a673f6cfeeb57ab",
    ),
    "R293": (
        "cm2_round293_source_g_r289_r291_witness_binding_canonical_closure_ledger.json.gz",
        "0e7395a69844734cc51563882f471987cc566db28a55ccae6e6d15d045f9e53c",
    ),
    "R294": (
        "cm2_round294_source_g_occurrence_registry_atomic_promotion_registry_ledger.json.gz",
        "c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb",
    ),
    "R295A": (
        "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_physical_witness_incidence_binding_ledger.json.gz",
        "2d9addfc9fca55366a58b29a7084c063674c3f556dd5398b038ae7d51fe97dcf",
    ),
    "R300A": (
        "cm2_round300a_source_g_r287_graph_zero_lower_frontier_exhaustion_ledger.json.gz",
        "ddc1a8bc53861afeb93d3569c6efa228f17d86f161db31a39fa9b72458ab8f2d",
    ),
}


class BuildError(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise BuildError(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for piece in iter(lambda: stream.read(1 << 20), b""):
            state.update(piece)
    return state.hexdigest()


def guard_input(filename: str, expected_sha256: str) -> None:
    path = HERE / filename
    info = os.lstat(path)
    need(
        path.name == filename
        and path.parent == HERE
        and not path.is_symlink()
        and stat.S_ISREG(info.st_mode)
        and info.st_nlink == 1
        and 0 < info.st_size < 2_000_000_000
        and path.resolve(strict=True).parent == HERE.resolve(strict=True),
        "regular single-link confined input:" + filename,
    )
    need(file_sha256(path) == expected_sha256, "byte pin:" + filename)


def closed(payload: dict[str, Any]) -> dict[str, Any]:
    return {**payload, "row_sha256": digest(payload)}


def verify_row(row: dict[str, Any], label: str) -> None:
    payload = {key: value for key, value in row.items() if key != "row_sha256"}
    need(
        set(row) == set(payload) | {"row_sha256"}
        and row["row_sha256"] == digest(payload),
        label + ":row closure",
    )


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
        and wrapper["result_sha256"] == digest(wrapper["result"]),
        label + ":closed result",
    )
    return wrapper["result"]


def qbox(values: Iterable[str]) -> tuple[Q, Q, Q, Q, Q, Q]:
    box = tuple(Q(value) for value in values)
    need(
        len(box) == 6
        and box[0] < box[1]
        and box[2] < box[3]
        and box[4] < box[5],
        "positive rational box",
    )
    return box  # type: ignore[return-value]


def qrect(values: Iterable[str]) -> tuple[Q, Q, Q, Q]:
    rectangle = tuple(Q(value) for value in values)
    need(
        len(rectangle) == 4
        and rectangle[0] < rectangle[1]
        and rectangle[2] < rectangle[3],
        "positive rational rectangle",
    )
    return rectangle  # type: ignore[return-value]


def qstr(value: Q) -> str:
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def rect_contains(
    outer: tuple[Q, Q, Q, Q],
    inner: tuple[Q, Q, Q, Q],
) -> bool:
    return (
        outer[0] <= inner[0] <= inner[1] <= outer[1]
        and outer[2] <= inner[2] <= inner[3] <= outer[3]
    )


def unpack_named(result: dict[str, Any], table: str) -> list[dict[str, Any]]:
    columns = result["row_column_schemas"][table]
    return [
        dict(zip(columns, packed, strict=True))
        for packed in result[table]
    ]


def unpack_table(table: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [
        dict(zip(table["columns"], packed, strict=True))
        for packed in table["rows"]
    ]
    need(len(rows) == table["row_count"], "packed table count")
    return rows


class ListHasher:
    def __init__(self) -> None:
        self.state = hashlib.sha256(b"[")
        self.count = 0

    def add(self, value: Any) -> None:
        if self.count:
            self.state.update(b",")
        self.state.update(canonical(value))
        self.count += 1

    def finish(self) -> str:
        self.state.update(b"]")
        return self.state.hexdigest()


def stream_table(filename: str, table: str) -> Iterator[dict[str, Any]]:
    path = HERE / filename
    marker = ('"' + table + '"').encode("ascii")
    with path.open("rb") as raw:
        mapped = mmap.mmap(raw.fileno(), 0, access=mmap.ACCESS_READ)
        table_at = mapped.find(marker)
        rows_at = mapped.find(b'"rows"', table_at)
        need(table_at >= 0 and rows_at >= 0, "table marker:" + table)
        position = rows_at + len(b'"rows"')
        while mapped[position : position + 1] in b" \t\r\n:":
            position += 1
        need(mapped[position : position + 1] == b"[", "rows array:" + table)
        position += 1
        mapped.close()
    decoder = json.JSONDecoder()
    buffer = ""
    with path.open("rt", encoding="utf-8") as stream:
        stream.seek(position)
        while True:
            buffer = buffer.lstrip()
            if not buffer:
                piece = stream.read(1 << 20)
                need(bool(piece), "unexpected table EOF:" + table)
                buffer = piece
                continue
            if buffer[0] == ",":
                buffer = buffer[1:]
                continue
            if buffer[0] == "]":
                return
            try:
                row, end = decoder.raw_decode(buffer)
            except json.JSONDecodeError:
                piece = stream.read(1 << 20)
                need(bool(piece), "malformed table row:" + table)
                buffer += piece
                continue
            need(type(row) is dict, "table row object:" + table)
            yield row
            buffer = buffer[end:]


def build_sheet_frontier() -> dict[str, dict[str, Any]]:
    r242 = closed_result("R242")
    patches = r242["formal_positive_2D_transition_sheet_patch_ledger"]["rows"]
    need(len(patches) == 264, "R242 patch census")
    patch_by_interface: dict[str, dict[str, Any]] = {}
    for patch in patches:
        verify_row(patch, "R242 patch")
        interface = patch["Round220_split_interface_id"]
        need(interface not in patch_by_interface, "R242 unique interface")
        patch_by_interface[interface] = patch

    r245 = closed_result("R245")
    nodes = r245["formal_retained_stratum_node_ledger"]["rows"]
    edges = r245["formal_mixed_sheet_physical_edge_ledger"]["rows"]
    need(len(nodes) == len(edges) == 3_664, "R245 node/edge census")
    node_by_id = {row["retained_stratum_node_id"]: row for row in nodes}
    edge_by_interface: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for edge in edges:
        edge_by_interface[edge["Round220_split_interface_id"]].append(edge)

    output: dict[str, dict[str, Any]] = {}
    for sheet in nodes:
        if sheet["stratum_kind"] != "HALF_OPEN_TRANSITION_SHEET":
            continue
        verify_row(sheet, "R245 sheet")
        interface = sheet["Round220_split_interface_id"]
        patch = patch_by_interface[interface]
        base = qrect(patch["closed_base_rectangle"])
        need(
            patch["formal_half_open_owner_credit"] == 1
            and patch["unique_graph_point_for_every_closed_base_point"] is True
            and patch["Round173_half_open_rule"]
            == "E or W owns; N or S excludes"
            and sheet["half_open_owner_materialized"] is True
            and sheet["Round179_retained_child_row_id"]
            == patch["Round179_retained_child_row_id"]
            and sheet["local_return_signature"] == patch["owner_signature"]
            and Q(sheet["exact_positive_2D_sheet_area"])
            == (base[1] - base[0]) * (base[3] - base[2]) > 0,
            "R242/R245 included owner sheet",
        )
        incident = [
            edge for edge in edge_by_interface[interface]
            if sheet["retained_stratum_node_id"]
            in (edge["left_node_id"], edge["right_node_id"])
        ]
        need(len(incident) == 2, "R245 sheet two bulk contacts")
        bulk: dict[str, dict[str, Any]] = {}
        bulk_edge: dict[str, dict[str, Any]] = {}
        for edge in incident:
            verify_row(edge, "R245 selected edge")
            other = (
                edge["left_node_id"]
                if edge["right_node_id"] == sheet["retained_stratum_node_id"]
                else edge["right_node_id"]
            )
            node = node_by_id[other]
            verify_row(node, "R245 selected bulk")
            need(
                qrect(edge["exact_positive_2D_contact_rectangle"]) == base
                and Q(edge["exact_positive_2D_contact_area"]) > 0
                and Q(edge["strict_positive_3D_retained_corridor_volume"]) > 0,
                "R245 positive exact contact",
            )
            bulk[node["stratum_kind"]] = node
            bulk_edge[node["stratum_kind"]] = edge
        need(
            set(bulk) == {"OWNER_OPEN_BULK", "SHADOW_OPEN_BULK"}
            and bulk["OWNER_OPEN_BULK"]["local_return_signature"]
            == patch["owner_signature"]
            and bulk["SHADOW_OPEN_BULK"]["local_return_signature"]
            == patch["shadow_signature"],
            "R245 exact owner/shadow bulk pair",
        )
        output[interface] = {
            "patch": patch,
            "sheet": sheet,
            "owner_bulk": bulk["OWNER_OPEN_BULK"],
            "shadow_bulk": bulk["SHADOW_OPEN_BULK"],
            "owner_edge": bulk_edge["OWNER_OPEN_BULK"],
            "shadow_edge": bulk_edge["SHADOW_OPEN_BULK"],
            "base": base,
            "patch_box": qbox(patch["closed_witness_box"]),
        }
    need(len(output) == 264 and set(output) == set(patch_by_interface), "sheet census")

    r233 = closed_result("R233")
    needed = {
        item["patch"]["Round233_graph_partition_row_id"]
        for item in output.values()
    }
    graph_rows = {
        row["parametric_graph_partition_row_id"]: row
        for row in r233["parametric_graph_key_partition_rows"]
        if row["parametric_graph_partition_row_id"] in needed
    }
    need(set(graph_rows) == needed, "R233 selected rows")
    for interface, item in output.items():
        patch = item["patch"]
        graph = graph_rows[patch["Round233_graph_partition_row_id"]]
        need(
            graph["Round220_split_interface_id"] == interface
            and graph["Round179_retained_child_row_id"]
            == patch["Round179_retained_child_row_id"]
            and graph["source_chart"] == patch["source_chart"]
            and graph["equation"] == patch["equation"]
            and {
                digest(graph["x_dominant_signature"]),
                digest(graph["y_dominant_signature"]),
            }
            == {
                digest(patch["owner_signature"]),
                digest(patch["shadow_signature"]),
            },
            "R233/R242 exact graph/signature lineage",
        )
        item["graph"] = graph
    return output


def select_r291(
    sheets: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    by_child: dict[str, list[tuple[str, dict[str, Any]]]] = defaultdict(list)
    for interface, item in sheets.items():
        by_child[item["patch"]["Round179_retained_child_row_id"]].append(
            (interface, item)
        )
    ledger = read_gzip("R291")
    need(ledger["row_count"] == len(ledger["rows"]) == 55_428, "R291 census")
    graph_count = 0
    outgoing_count = 0
    multiplicity: Counter[int] = Counter()
    selected: list[dict[str, Any]] = []
    sheet_hits = Counter()
    for disposition in ledger["rows"]:
        for index, witness in enumerate(disposition["physical_witness_cells"]):
            if witness["witness_kind"] != "ROUND182_GRAPH_SHEET_LEAF":
                continue
            graph_count += 1
            if disposition["predicate_label"] != "outgoing_chart_seam":
                multiplicity[0] += 1
                continue
            outgoing_count += 1
            box = qbox(witness["exact_box"])
            hits = [
                (interface, item)
                for interface, item in by_child.get(
                    witness["retained_child_row_id"], []
                )
                if disposition["source_chart"] == item["patch"]["source_chart"]
                and disposition["predicate_equation"]
                == item["patch"]["equation"]
                and rect_contains(box[2:6], item["base"])
            ]
            multiplicity[len(hits)] += 1
            for interface, item in hits:
                verify_row(disposition, "R291 selected disposition")
                sheet_hits[interface] += 1
                selected.append({
                    "interface": interface,
                    "sheet_data": item,
                    "disposition": disposition,
                    "cell_index": index,
                    "witness": witness,
                    "cell_box": box,
                })
    need(
        graph_count == 111_524
        and outgoing_count == 86_308
        and multiplicity == {0: 111_260, 1: 264}
        and len(selected) == len(sheet_hits) == 264
        and set(sheet_hits.values()) == {1},
        "R291/R245 exact bijection",
    )
    return selected, {
        "complete_R291_graph_witness_cell_count": graph_count,
        "complete_R291_outgoing_graph_witness_cell_count": outgoing_count,
        "zero_candidate_graph_witness_cell_count": multiplicity[0],
        "unique_candidate_graph_witness_cell_count": multiplicity[1],
    }


def verify_geometry_lineage(selected: list[dict[str, Any]]) -> None:
    leaf_ids = {item["witness"]["leaf_row_id"] for item in selected}
    r182 = closed_result("R182")
    columns = r182["row_column_schemas"]["collar_leaf_rows"]
    index = columns.index("row_id")
    leaves = {
        packed[index]: dict(zip(columns, packed, strict=True))
        for packed in r182["collar_leaf_rows"]
        if packed[index] in leaf_ids
    }
    need(set(leaves) == leaf_ids, "R182 selected leaves")
    for item in selected:
        leaf = leaves[item["witness"]["leaf_row_id"]]
        patch = item["sheet_data"]["patch"]
        disposition = item["disposition"]
        need(
            leaf["retained_child_row_id"]
            == patch["Round179_retained_child_row_id"]
            and leaf["occurrence_row_id"]
            == disposition["canonical_support_row_id"]
            and qbox(leaf["box"]) == item["cell_box"]
            and leaf["graph_classification"] == "CLIPPED_2D_BOUNDARY_1D"
            and leaf["two_dimensional_graph_sheet_count"] == 1
            and item["cell_box"][0:2]
            == item["sheet_data"]["patch_box"][0:2]
            and all(
                item["cell_box"][2 * axis]
                <= item["sheet_data"]["patch_box"][2 * axis]
                < item["sheet_data"]["patch_box"][2 * axis + 1]
                <= item["cell_box"][2 * axis + 1]
                for axis in range(3)
            ),
            "R182 exact leaf/patch geometry",
        )
        item["leaf"] = leaf
    del r182
    gc.collect()

    r179 = closed_result("R179")
    outgoing_needed = {
        item["disposition"]["canonical_support_row_id"] for item in selected
    }
    retained_needed = {
        item["sheet_data"]["patch"]["Round179_retained_child_row_id"]
        for item in selected
    }
    outgoing = {
        row["row_id"]: row
        for row in unpack_named(r179, "outgoing_normal_form_rows")
        if row["row_id"] in outgoing_needed
    }
    retained = {
        row["row_id"]: row
        for row in unpack_named(r179, "retained_3d_child_rows")
        if row["row_id"] in retained_needed
    }
    need(set(outgoing) == outgoing_needed and set(retained) == retained_needed,
         "R179 selected rows")
    for item in selected:
        patch = item["sheet_data"]["patch"]
        graph = item["sheet_data"]["graph"]
        disposition = item["disposition"]
        normal = outgoing[disposition["canonical_support_row_id"]]
        child = retained[patch["Round179_retained_child_row_id"]]
        need(
            normal["origin_row_id"]
            == child["origin_row_id"]
            == graph["origin_row_id"]
            == disposition["containing_Round174_residual_row_id"]
            and normal["chart"] == child["chart"] == patch["source_chart"]
            and normal["equation"] == patch["equation"]
            and normal["two_open_3d_sides_retained"] is True,
            "R179 exact normal-form lineage",
        )
        item["normal"] = normal
    del r179, outgoing, retained
    gc.collect()

    r220 = closed_result("R220")
    table = r220["coordinate_boundary_atlas"]["tables"][
        "one_step_split_interface_rows"
    ]
    interfaces = {
        row["split_interface_id"]: row
        for row in unpack_table(table)
        if row["split_interface_id"] in {
            item["interface"] for item in selected
        }
    }
    need(len(interfaces) == 264, "R220 selected interfaces")
    for item in selected:
        row = interfaces[item["interface"]]
        graph = item["sheet_data"]["graph"]
        need(
            {row["lower_child_row_id"], row["upper_child_row_id"]}
            == {
                graph["Round179_retained_child_row_id"],
                graph["Round179_resolved_sibling_row_id"],
            }
            and row["chart"] == graph["source_chart"]
            and row["event_trace_materialized_on_interface"] is False
            and row["retained_incidence_count"] == 1
            and row["resolved_incidence_count"] == 1,
            "R220 selected split interface",
        )
        item["split_interface"] = row
    del r220, table, interfaces
    gc.collect()


def bind_registry(selected: list[dict[str, Any]]) -> None:
    keys = {
        (
            item["disposition"]["complete_lower_stratum_local_disposition_row_id"],
            item["cell_index"],
        )
        for item in selected
    }
    r293 = read_gzip("R293")
    physical = r293["Round291_physical_witness_binding_rows"]
    need(len(physical) == 113_452, "R293 physical census")
    graph_count = 0
    binding_by_key: dict[tuple[str, int], dict[str, Any]] = {}
    for row in physical:
        if row["binding_classification"] != (
            "EXACT_TWO_SIDED_GRAPH_SHEET_ATOM_INCIDENCE"
        ):
            continue
        graph_count += 1
        key = (
            row["Round291_local_disposition_row_id"],
            row["physical_witness_cell_index"],
        )
        if key in keys:
            verify_row(row, "R293 selected binding")
            binding_by_key[key] = row
    need(graph_count == 111_524 and set(binding_by_key) == keys,
         "R293 selected exact bindings")
    binding_ids = {
        row["Round292_R291_physical_witness_binding_row_id"]
        for row in binding_by_key.values()
    }
    del r293
    gc.collect()

    r295 = read_gzip("R295A")
    need(r295["row_count"] == len(r295["rows"]) == 113_452, "R295A census")
    rebound: dict[str, dict[str, Any]] = {}
    for row in r295["rows"]:
        source = row["source_Round293_R291_physical_witness_binding_row_id"]
        if source in binding_ids:
            verify_row(row, "R295A selected binding")
            rebound[source] = row
    need(set(rebound) == binding_ids, "R295A selected rebindings")
    for item in selected:
        key = (
            item["disposition"]["complete_lower_stratum_local_disposition_row_id"],
            item["cell_index"],
        )
        binding = binding_by_key[key]
        row = rebound[binding["Round292_R291_physical_witness_binding_row_id"]]
        need(
            row["source_Round293_R291_physical_witness_binding_row_sha256"]
            == binding["row_sha256"]
            and row["source_Round293_binding_classification"]
            == binding["binding_classification"]
            == "EXACT_TWO_SIDED_GRAPH_SHEET_ATOM_INCIDENCE"
            and row["Round295A_binding_classification"]
            == (
                "FORMAL_ROUND294_REGISTRY_REBIND__"
                "EXACT_TWO_SIDED_GRAPH_SHEET_ATOM_INCIDENCE"
            )
            and row["target_Round294_registry_reference_count"] == 2
            and len(row["target_Round294_registry_rows"]) == 2
            and set(row["target_Round294_registry_occurrence_ids"])
            == set(binding["terminal_registry_target_references"])
            and row["formal_component_union_credit"] == 0
            and row["formal_DSU_rank_reduction_credit"] == 0,
            "R293/R295A exact two-sided rebind",
        )
        item["binding"] = binding
        item["rebind"] = row


def select_owner_atoms(selected: list[dict[str, Any]]) -> None:
    leaf_ids = {item["witness"]["leaf_row_id"] for item in selected}
    r279 = read_gzip("R279")
    need(r279["row_count"] == len(r279["rows"]) == 332_016, "R279 census")
    atoms_by_leaf: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for atom in r279["rows"]:
        if atom["Round182_leaf_row_id"] in leaf_ids:
            verify_row(atom, "R279 selected atom")
            atoms_by_leaf[atom["Round182_leaf_row_id"]].append(atom)
    need(set(atoms_by_leaf) == leaf_ids, "R279 selected leaves")
    atom_ids: set[str] = set()
    for item in selected:
        atoms = atoms_by_leaf[item["witness"]["leaf_row_id"]]
        patch = item["sheet_data"]["patch"]
        need(
            len(atoms) == 2
            and {
                atom["complete_10_field_return_signature_sha256"]
                for atom in atoms
            }
            == {
                digest(patch["owner_signature"]),
                digest(patch["shadow_signature"]),
            },
            "R279 exact owner/shadow atom pair",
        )
        for atom in atoms:
            need(
                atom["complete_10_field_return_signature_sha256"]
                == digest(atom["complete_10_field_return_signature"])
                and atom["source_chart"] == patch["source_chart"]
                and atom["owner_target"] == patch["owner_signature"]["target_lift"]
                and atom["support_classification"] == "WHOLE_ROUND182_LEAF"
                and qbox(atom["whole_Round182_leaf_box"]) == item["cell_box"],
                "R279 atom signature/geometry",
            )
            atom_ids.add(atom["canonical_atom_id"])
        item["atoms"] = atoms
    need(len(atom_ids) == 528, "R279 selected atom census")
    del r279
    gc.collect()

    r288 = read_gzip("R288")
    need(r288["row_count"] == len(r288["rows"]) == 332_016, "R288 census")
    dispositions = {}
    for row in r288["rows"]:
        if row["canonical_atom_id"] in atom_ids:
            verify_row(row, "R288 selected atom")
            dispositions[row["canonical_atom_id"]] = row
    need(set(dispositions) == atom_ids, "R288 selected dispositions")
    occurrence_to_atom: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}
    for item in selected:
        occurrences = set()
        for atom in item["atoms"]:
            disposition = dispositions[atom["canonical_atom_id"]]
            need(
                disposition["Round182_leaf_row_id"] == item["witness"]["leaf_row_id"]
                and disposition["complete_10_field_return_signature_sha256"]
                == atom["complete_10_field_return_signature_sha256"]
                and disposition["true_chart_retained_child_owner_verified"] is True,
                "R288/R279 atom lineage",
            )
            occurrence = (
                disposition["existing_local_occurrence_row_id"]
                or disposition["reserved_candidate_occurrence_id__not_issued"]
            )
            need(
                occurrence is not None
                and occurrence not in occurrence_to_atom,
                "R288 selected occurrence uniqueness",
            )
            occurrence_to_atom[occurrence] = (atom, disposition)
            occurrences.add(occurrence)
        need(
            occurrences
            == set(item["rebind"]["target_Round294_registry_occurrence_ids"]),
            "R288/R295A occurrence crosswalk",
        )
    need(len(occurrence_to_atom) == 528, "selected occurrence census")
    del r288, dispositions
    gc.collect()

    r294 = read_gzip("R294")
    need(r294["row_count"] == len(r294["rows"]) == 431_208, "R294 census")
    registry: dict[str, dict[str, Any]] = {}
    for row in r294["rows"]:
        occurrence = row["registry_occurrence_id"]
        if occurrence in occurrence_to_atom:
            verify_row(row, "R294 selected registry")
            registry[occurrence] = row
    need(set(registry) == set(occurrence_to_atom), "R294 selected registry")
    for item in selected:
        patch = item["sheet_data"]["patch"]
        embedded = {
            row["registry_occurrence_id"]: row
            for row in item["rebind"]["target_Round294_registry_rows"]
        }
        owner_signature = digest(patch["owner_signature"])
        shadow_signature = digest(patch["shadow_signature"])
        owner_hits = []
        shadow_hits = []
        for occurrence in item["rebind"]["target_Round294_registry_occurrence_ids"]:
            atom, disposition = occurrence_to_atom[occurrence]
            row = registry[occurrence]
            compact = embedded[occurrence]
            need(
                compact["Round294_occurrence_registry_row_id"]
                == row["Round294_occurrence_registry_row_id"]
                and compact["Round294_occurrence_registry_row_sha256"]
                == row["row_sha256"]
                and compact["complete_10_field_return_signature_sha256"]
                == row["complete_10_field_return_signature_sha256"]
                == atom["complete_10_field_return_signature_sha256"]
                and compact["official_key_id"] == row["official_key_id"]
                == patch["official_key_id"]
                and compact["physical_support_chart"]
                == row["physical_support_chart"] == patch["source_chart"]
                and row["registry_entry_kind"]
                == "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM"
                and row["canonical_atom_id"] == atom["canonical_atom_id"],
                "R294/R295A/R279 selected registry lineage",
            )
            signature = row["complete_10_field_return_signature_sha256"]
            if signature == owner_signature:
                owner_hits.append((occurrence, atom, disposition, row))
            if signature == shadow_signature:
                shadow_hits.append((occurrence, atom, disposition, row))
        need(
            len(owner_hits) == len(shadow_hits) == 1
            and owner_hits[0][0] != shadow_hits[0][0],
            "unique full-signature half-open selection",
        )
        item["owner_occurrence"], item["owner_atom"], item["owner_disposition"], item[
            "owner_registry"
        ] = owner_hits[0]
        item["shadow_occurrence"], item["shadow_atom"], item["shadow_disposition"], item[
            "shadow_registry"
        ] = shadow_hits[0]
    del r294, registry, occurrence_to_atom
    gc.collect()


def bind_round266_roots(selected: list[dict[str, Any]]) -> None:
    sheet_ids = {
        item["sheet_data"]["sheet"]["retained_stratum_node_id"]
        for item in selected
    }
    rows: dict[str, dict[str, Any]] = {}
    ids = ListHasher()
    hashes = ListHasher()
    count = 0
    filename = FILES["R266"][0]
    for row in stream_table(
        filename, "formal_post_Round266_valid_virtual_node_frontier_ledger"
    ):
        verify_row(row, "R266 virtual frontier")
        count += 1
        ids.add(row["post_Round266_valid_virtual_node_frontier_row_id"])
        hashes.add(row["row_sha256"])
        node_id = row["valid_virtual_stratum_node_id"]
        if node_id in sheet_ids:
            need(node_id not in rows, "R266 selected virtual uniqueness")
            rows[node_id] = row
    need(
        count == 133_284
        and ids.finish()
        == "2d42533f48f864f01e6bd4a46470e7266c1a2cec590380483cfb7cbfb84634f2"
        and hashes.finish()
        == "9c31ba929e13eeaea29a9f6abe7cf324222eacb25d123a9b12252b386c12a32e"
        and set(rows) == sheet_ids,
        "R266 complete virtual frontier and selected coverage",
    )
    pairs = set()
    for item in selected:
        sheet = item["sheet_data"]["sheet"]
        row = rows[sheet["retained_stratum_node_id"]]
        need(
            row["virtual_node_kind"] == "INHERITED_ROUND247_VIRTUAL_STRATUM"
            and row["official_key_id"] == sheet["official_key_id"]
            == item["owner_registry"]["official_key_id"],
            "R266 sheet root/key lineage",
        )
        item["virtual_frontier"] = row
        pair = (
            row["post_Round266_quotient_component_id"],
            item["owner_occurrence"],
        )
        need(pair not in pairs, "canonical root/owner pair uniqueness")
        pairs.add(pair)
    need(len(pairs) == 264, "canonical root/owner pair census")


def bind_round300a_crosscheck(selected: list[dict[str, Any]]) -> None:
    pair_to_item = {
        frozenset((item["owner_occurrence"], item["shadow_occurrence"])): item
        for item in selected
    }
    need(len(pair_to_item) == 264, "selected owner/shadow pair uniqueness")
    ledger = read_gzip("R300A")
    rows = ledger["canonical_occurrence_pair_rows"]
    need(
        ledger["canonical_occurrence_pair_row_count"] == len(rows) == 3_232
        and ledger["canonical_occurrence_pair_rows_sha256"] == digest(rows),
        "R300A canonical pair table",
    )
    hits = 0
    explicit_pair_match_count = 0
    explicit_binding_match_count = 0
    selected_binding_ids = {
        item["rebind"]["Round295A_R291_physical_incidence_binding_row_id"]
        for item in selected
    }
    seen_items: set[str] = set()
    for row in rows:
        verify_row(row, "R300A canonical pair")
        if not row["R295A_explicit_lower_graph_sheet_witness_present"]:
            continue
        hits += 1
        pair = frozenset(
            row["canonical_unordered_Round294_registry_occurrence_ids"]
        )
        explicit_binding_match_count += sum(
            binding_id in selected_binding_ids
            for binding_id in row[
                "R295A_physical_incidence_binding_row_ids"
            ]
        )
        need(
            len(row["R295A_physical_incidence_binding_row_ids"]) == 1
            and len(row["R295A_physical_incidence_binding_row_sha256s"]) == 1
            and row["endpoint_specific_common_positive_area_zero_trace_proved"]
            is True
            and row["exact_positive_open_support_intersection"] is False
            and row["opposite_strict_side_exclusion_proved"] is True
            and row["formal_component_edge_credit"] == 0
            and row["formal_DSU_rank_reduction_credit"] == 0,
            "R300A explicit pair exact R295A cross-reference",
        )
        if pair in pair_to_item:
            explicit_pair_match_count += 1
            item = pair_to_item[pair]
            item["round300a_pair"] = row
            seen_items.add(
                item["sheet_data"]["sheet"]["retained_stratum_node_id"]
            )
    need(
        hits == 128
        and explicit_pair_match_count == len(seen_items) == 0
        and explicit_binding_match_count == 0,
        "R300A exact disjoint crosscheck:"
        + json.dumps({
            "explicit": hits,
            "pair_matches": explicit_pair_match_count,
            "binding_matches": explicit_binding_match_count,
        }, sort_keys=True),
    )
    for item in selected:
        item.setdefault("round300a_pair", None)


def output_rows(selected: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in selected:
        data = item["sheet_data"]
        patch = data["patch"]
        sheet = data["sheet"]
        owner_edge = data["owner_edge"]
        virtual = item["virtual_frontier"]
        binding = item["binding"]
        rebind = item["rebind"]
        round300a = item["round300a_pair"]
        payload = {
            "Round242_transition_sheet_patch_row_id":
                patch["transition_sheet_patch_row_id"],
            "Round245_included_half_open_sheet_node_id":
                sheet["retained_stratum_node_id"],
            "Round245_included_half_open_sheet_node_row_sha256":
                sheet["row_sha256"],
            "Round245_owner_bulk_node_id":
                data["owner_bulk"]["retained_stratum_node_id"],
            "Round245_owner_bulk_node_row_sha256":
                data["owner_bulk"]["row_sha256"],
            "Round245_owner_bulk_to_sheet_edge_id":
                owner_edge["mixed_sheet_edge_id"],
            "Round245_owner_bulk_to_sheet_edge_row_sha256":
                owner_edge["row_sha256"],
            "Round266_virtual_frontier_row_id":
                virtual["post_Round266_valid_virtual_node_frontier_row_id"],
            "Round266_virtual_frontier_row_sha256": virtual["row_sha256"],
            "post_Round266_quotient_component_id":
                virtual["post_Round266_quotient_component_id"],
            "Round179_outgoing_normal_form_row_id":
                item["normal"]["row_id"],
            "Round179_retained_child_row_id":
                patch["Round179_retained_child_row_id"],
            "Round182_graph_leaf_row_id": item["witness"]["leaf_row_id"],
            "Round291_local_disposition_row_id":
                item["disposition"][
                    "complete_lower_stratum_local_disposition_row_id"
                ],
            "Round291_local_disposition_row_sha256":
                item["disposition"]["row_sha256"],
            "Round291_physical_witness_cell_index": item["cell_index"],
            "Round293_two_sided_binding_row_id":
                binding["Round292_R291_physical_witness_binding_row_id"],
            "Round293_two_sided_binding_row_sha256": binding["row_sha256"],
            "Round295A_registry_rebinding_row_id":
                rebind["Round295A_R291_physical_incidence_binding_row_id"],
            "Round295A_registry_rebinding_row_sha256": rebind["row_sha256"],
            "Round279_owner_atom_id":
                item["owner_atom"]["canonical_atom_id"],
            "Round279_owner_atom_row_sha256": item["owner_atom"]["row_sha256"],
            "Round288_owner_atom_disposition_row_id":
                item["owner_disposition"]["Round288_atom_disposition_row_id"],
            "Round288_owner_atom_disposition_row_sha256":
                item["owner_disposition"]["row_sha256"],
            "Round294_owner_registry_row_id":
                item["owner_registry"]["Round294_occurrence_registry_row_id"],
            "Round294_owner_registry_row_sha256":
                item["owner_registry"]["row_sha256"],
            "Round294_owner_occurrence_id": item["owner_occurrence"],
            "Round279_shadow_atom_id":
                item["shadow_atom"]["canonical_atom_id"],
            "Round294_shadow_registry_row_id":
                item["shadow_registry"]["Round294_occurrence_registry_row_id"],
            "Round294_shadow_occurrence_id": item["shadow_occurrence"],
            "Round300A_prior_explicit_graph_zero_pair_present":
                round300a is not None,
            "Round300A_prior_explicit_graph_zero_pair_row_id": (
                round300a["Round300A_canonical_occurrence_pair_row_id"]
                if round300a is not None else None
            ),
            "Round300A_prior_explicit_graph_zero_pair_row_sha256": (
                round300a["row_sha256"] if round300a is not None else None
            ),
            "Round300A_owner_endpoint_selected_if_present":
                round300a is not None,
            "Round300A_shadow_endpoint_not_promoted_if_present":
                round300a is not None,
            "Round300A_two_endpoint_union_credit": 0,
            "source_chart": patch["source_chart"],
            "predicate_equation": patch["equation"],
            "exact_positive_2D_sheet_rectangle":
                patch["closed_base_rectangle"],
            "exact_positive_2D_sheet_area":
                patch["exact_positive_base_projection_area"],
            "owner_complete_10_field_return_signature":
                patch["owner_signature"],
            "owner_complete_10_field_return_signature_sha256":
                digest(patch["owner_signature"]),
            "shadow_complete_10_field_return_signature_sha256":
                digest(patch["shadow_signature"]),
            "official_key_id": patch["official_key_id"],
            "official_key_ordinal": patch["official_key_ordinal"],
            "half_open_owner_rule": patch["Round173_half_open_rule"],
            "owner_outgoing_cell": patch["owner_outgoing_cell"],
            "shadow_outgoing_cell": patch["shadow_outgoing_cell"],
            "two_sided_incidence_reference_count": 2,
            "exact_half_open_owner_selection_multiplicity": 1,
            "shadow_incidence_only_no_edge_credit": True,
            "shadow_component_edge_witness_credit": 0,
            "canonical_component_edge_endpoint_pair": [
                virtual["post_Round266_quotient_component_id"],
                item["owner_occurrence"],
            ],
            "edge_semantics":
                "EXACT_R242_HALF_OPEN_OWNER_SHEET_SUBPATCH_OF_"
                "SAME_R182_GRAPH_LEAF__FULL_SIGNATURE_OWNER_SELECTION__"
                "SHADOW_EXCLUDED",
            "formal_half_open_owner_component_edge_witness_credit": 1,
            "eligible_for_component_DSU_application": True,
            "formal_occurrence_identity_collapse_credit": 0,
            "formal_occurrence_alias_credit": 0,
            "formal_new_occurrence_ID_credit": 0,
            "formal_component_union_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_quotient_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
        }
        row_id = "round300f-r245-half-open-owner-attachment:" + digest(payload)
        rows.append(closed({
            "Round300F_R245_half_open_owner_attachment_row_id": row_id,
            **payload,
        }))
    rows.sort(
        key=lambda row: row[
            "Round300F_R245_half_open_owner_attachment_row_id"
        ]
    )
    ids = [
        row["Round300F_R245_half_open_owner_attachment_row_id"] for row in rows
    ]
    pairs = [tuple(row["canonical_component_edge_endpoint_pair"]) for row in rows]
    need(
        len(rows) == len(set(ids)) == len(set(pairs)) == 264,
        "output row/pair census",
    )
    return rows


def build(producer_sha256: str) -> tuple[dict[str, Any], dict[str, Any]]:
    for filename, sha256 in FILES.values():
        guard_input(filename, sha256)
    sheets = build_sheet_frontier()
    selected, census = select_r291(sheets)
    verify_geometry_lineage(selected)
    bind_registry(selected)
    select_owner_atoms(selected)
    bind_round266_roots(selected)
    bind_round300a_crosscheck(selected)
    rows = output_rows(selected)
    ids = [
        row["Round300F_R245_half_open_owner_attachment_row_id"] for row in rows
    ]
    ledger = {
        "schema": LEDGER_SCHEMA,
        "status": (
            "FORMAL_264_R245_HALF_OPEN_OWNER_TO_ROUND266_ROOT_"
            "OCCURRENCE_COMPONENT_EDGE_WITNESSES__SHADOW_EXCLUDED"
        ),
        "row_count": len(rows),
        "row_ids_sha256": digest(ids),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "rows_sha256": digest(rows),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }
    area_sum = sum((Q(row["exact_positive_2D_sheet_area"]) for row in rows), Q(0))
    pair_histogram = Counter(
        "|".join(sorted((
            row["owner_outgoing_cell"], row["shadow_outgoing_cell"]
        )))
        for row in rows
    )
    payload = {
        "schema": SCHEMA,
        "status": (
            "PASS_ROUND300F_R245_HALF_OPEN_OWNER_ATTACHMENT__"
            "264_UNIQUE_SHEETS__264_UNIQUE_OWNER_ROOT_EDGES__"
            "264_SHADOW_INCIDENCES_EXCLUDED__"
            "R300A_EXPLICIT_128_DISJOINT_FAIL_CLOSED"
        ),
        "producer_file_sha256": producer_sha256,
        "input_file_pins": {
            filename: sha256 for filename, sha256 in sorted(FILES.values())
        },
        "complete_frontier_census": {
            **census,
            "R245_half_open_transition_sheet_count": 264,
            "selected_R291_graph_leaf_count": 264,
            "selected_R293_two_sided_binding_count": 264,
            "two_sided_registry_reference_count": 528,
            "selected_R279_atom_count": 528,
            "selected_Round294_occurrence_count": 528,
            "unique_half_open_owner_occurrence_count": 264,
            "shadow_incidence_only_occurrence_count": 264,
            "canonical_Round266_root_owner_occurrence_edge_count": 264,
            "Round300A_explicit_graph_zero_pair_crosscheck_count": 128,
            "Round300A_explicit_graph_zero_pair_intersection_with_R245_count":
                0,
            "Round300A_explicit_graph_zero_pair_owner_endpoint_selected_count":
                0,
            "Round300A_explicit_graph_zero_pair_shadow_endpoint_excluded_count":
                0,
            "Round300A_explicit_graph_zero_pair_remaining_unresolved_count":
                128,
            "Round300A_explicit_graph_zero_pair_two_endpoint_union_count": 0,
            "unresolved_sheet_count": 0,
            "unresolved_owner_selection_count": 0,
        },
        "geometry_and_selection_audit": {
            "R242_witness_t_interval_equals_R182_leaf_t_interval_count": 264,
            "R242_witness_box_contained_in_R182_leaf_count": 264,
            "exact_positive_2D_sheet_area_sum": qstr(area_sum),
            "owner_shadow_outgoing_cell_pair_histogram":
                dict(sorted(pair_histogram.items())),
            "selection_contract":
                "EXACT_FULL_SIGNATURE_MATCH_TO_R242_HALF_OPEN_OWNER_ONLY",
            "shadow_selection_contract":
                "EXACT_FULL_SIGNATURE_MATCH_RETAINED_AS_INCIDENCE_ONLY__"
                "NO_EDGE_CREDIT",
            "canonical_DSU_endpoint_contract":
                "[post_Round266_quotient_component_id,"
                "Round294_owner_occurrence_id]",
        },
        "attachment_ledger": {
            "filename": LEDGER_PATH.name,
            "schema": ledger["schema"],
            "row_count": ledger["row_count"],
            "row_ids_sha256": ledger["row_ids_sha256"],
            "row_hashes_sha256": ledger["row_hashes_sha256"],
            "rows_sha256": ledger["rows_sha256"],
        },
        "strict_nonpromotion": {
            "formal_half_open_owner_component_edge_witness_credit": 264,
            "shadow_component_edge_witness_credit": 0,
            "occurrence_identity_collapse_credit": 0,
            "component_union_credit": 0,
            "DSU_rank_reduction_credit": 0,
            "quotient_credit": 0,
            "maximality_credit": 0,
            "fibre_credit": 0,
            "global_disposition_credit": 0,
            "complete_component_frontier_claimed": False,
            "Round300A_explicit_pair_edge_credit": 0,
            "Round300A_explicit_pair_resolved_by_Round300F_count": 0,
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
            need(path.exists() and path.read_bytes() == data,
                 "deterministic replay:" + path.name)
    else:
        atomic_write(LEDGER_PATH, ledger_data)
        atomic_write(RESULT_PATH, result_data)
    print(json.dumps({
        "status": result["status"],
        "attachment_count": ledger["row_count"],
        "result_sha256": result["result_sha256"],
        "write": not args.no_write,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
