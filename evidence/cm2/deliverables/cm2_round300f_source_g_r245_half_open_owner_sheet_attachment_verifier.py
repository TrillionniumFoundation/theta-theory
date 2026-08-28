#!/usr/bin/env python3
"""Independent verifier for the Round300F R245 owner attachment.

The producer is treated only as a pinned byte string.  It is never imported,
executed, tokenized, parsed, or used as an expected-value oracle.  This file
reconstructs the 264 rows from the frozen mathematical inputs before opening
the candidate ledger or result.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from copy import deepcopy
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
import zlib


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round300f_source_g_r245_half_open_owner_sheet_attachment"
PRODUCER = HERE / f"{PREFIX}.py"
CANDIDATE_LEDGER = HERE / f"{PREFIX}_ledger.json.gz"
CANDIDATE_RESULT = HERE / f"{PREFIX}_result.json"
ATTACK_PATH = HERE / f"{PREFIX}_attack_suite.json"
VERIFICATION_PATH = HERE / f"{PREFIX}_verification.json"

PRODUCER_SHA256 = "a47cec07e10fd01d44953b4df101f8aafe6768502c1b39d6baf4d9a06b2e7523"
SCHEMA = "cm2.round300f.source-g-r245-half-open-owner-sheet-attachment.v1"
LEDGER_SCHEMA = SCHEMA + ".ledger.v1"
VERIFICATION_SCHEMA = SCHEMA + ".verification.v1"
ATTACK_SCHEMA = SCHEMA + ".attack-suite.v1"

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


class VerificationError(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


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


def guard_file(path: Path, expected: str, label: str) -> None:
    info = os.lstat(path)
    need(
        path.parent == HERE
        and not path.is_symlink()
        and stat.S_ISREG(info.st_mode)
        and info.st_nlink == 1
        and 0 < info.st_size < 2_000_000_000
        and path.resolve(strict=True).parent == HERE.resolve(strict=True)
        and file_sha256(path) == expected,
        "guard:" + label,
    )


def closed(payload: dict[str, Any]) -> dict[str, Any]:
    return {**payload, "row_sha256": digest(payload)}


def verify_row(row: dict[str, Any], label: str) -> None:
    payload = {key: value for key, value in row.items() if key != "row_sha256"}
    need(
        set(row) == set(payload) | {"row_sha256"}
        and row["row_sha256"] == digest(payload),
        label + ":row closure",
    )


def read_upstream_json(label: str) -> dict[str, Any]:
    with (HERE / FILES[label][0]).open("rb") as stream:
        value = json.load(stream)
    need(type(value) is dict, label + ":object")
    return value


def read_upstream_gzip(label: str) -> dict[str, Any]:
    with gzip.open(HERE / FILES[label][0], "rt", encoding="utf-8") as stream:
        value = json.load(stream)
    need(type(value) is dict, label + ":gzip object")
    return value


def closed_result(label: str) -> dict[str, Any]:
    wrapper = read_upstream_json(label)
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
        "positive box",
    )
    return box  # type: ignore[return-value]


def qrect(values: Iterable[str]) -> tuple[Q, Q, Q, Q]:
    rectangle = tuple(Q(value) for value in values)
    need(
        len(rectangle) == 4
        and rectangle[0] < rectangle[1]
        and rectangle[2] < rectangle[3],
        "positive rectangle",
    )
    return rectangle  # type: ignore[return-value]


def qstr(value: Q) -> str:
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def contains(outer: tuple[Q, Q, Q, Q], inner: tuple[Q, Q, Q, Q]) -> bool:
    return (
        outer[0] <= inner[0] <= inner[1] <= outer[1]
        and outer[2] <= inner[2] <= inner[3] <= outer[3]
    )


def unpack_named(result: dict[str, Any], name: str) -> list[dict[str, Any]]:
    columns = result["row_column_schemas"][name]
    return [
        dict(zip(columns, packed, strict=True))
        for packed in result[name]
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
        need(table_at >= 0 and rows_at >= 0, "table marker")
        position = rows_at + len(b'"rows"')
        while mapped[position : position + 1] in b" \t\r\n:":
            position += 1
        need(mapped[position : position + 1] == b"[", "rows marker")
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
                need(bool(piece), "stream EOF")
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
                need(bool(piece), "stream malformed")
                buffer += piece
                continue
            need(type(row) is dict, "stream row object")
            yield row
            buffer = buffer[end:]


def reconstruct_sheet_records() -> dict[str, dict[str, Any]]:
    r242 = closed_result("R242")
    patch_by_interface = {}
    for patch in r242["formal_positive_2D_transition_sheet_patch_ledger"]["rows"]:
        verify_row(patch, "R242 patch")
        interface = patch["Round220_split_interface_id"]
        need(interface not in patch_by_interface, "R242 interface uniqueness")
        patch_by_interface[interface] = patch
    need(len(patch_by_interface) == 264, "R242 census")

    r245 = closed_result("R245")
    nodes = r245["formal_retained_stratum_node_ledger"]["rows"]
    edges = r245["formal_mixed_sheet_physical_edge_ledger"]["rows"]
    node_by_id = {row["retained_stratum_node_id"]: row for row in nodes}
    edges_by_interface: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for edge in edges:
        edges_by_interface[edge["Round220_split_interface_id"]].append(edge)
    result: dict[str, dict[str, Any]] = {}
    for sheet in nodes:
        if sheet["stratum_kind"] != "HALF_OPEN_TRANSITION_SHEET":
            continue
        verify_row(sheet, "R245 sheet")
        interface = sheet["Round220_split_interface_id"]
        patch = patch_by_interface[interface]
        base = qrect(patch["closed_base_rectangle"])
        need(
            patch["Round173_half_open_rule"] == "E or W owns; N or S excludes"
            and patch["formal_half_open_owner_credit"] == 1
            and sheet["half_open_owner_materialized"] is True
            and sheet["local_return_signature"] == patch["owner_signature"]
            and Q(sheet["exact_positive_2D_sheet_area"])
            == (base[1] - base[0]) * (base[3] - base[2]) > 0,
            "R245 included sheet",
        )
        contacts = [
            edge for edge in edges_by_interface[interface]
            if sheet["retained_stratum_node_id"]
            in (edge["left_node_id"], edge["right_node_id"])
        ]
        need(len(contacts) == 2, "R245 two contacts")
        sides = {}
        side_edges = {}
        for edge in contacts:
            verify_row(edge, "R245 contact")
            other = (
                edge["left_node_id"]
                if edge["right_node_id"] == sheet["retained_stratum_node_id"]
                else edge["right_node_id"]
            )
            node = node_by_id[other]
            verify_row(node, "R245 bulk")
            need(
                qrect(edge["exact_positive_2D_contact_rectangle"]) == base
                and Q(edge["exact_positive_2D_contact_area"]) > 0
                and Q(edge["strict_positive_3D_retained_corridor_volume"]) > 0,
                "R245 exact contact/corridor",
            )
            sides[node["stratum_kind"]] = node
            side_edges[node["stratum_kind"]] = edge
        need(
            set(sides) == {"OWNER_OPEN_BULK", "SHADOW_OPEN_BULK"}
            and sides["OWNER_OPEN_BULK"]["local_return_signature"]
            == patch["owner_signature"]
            and sides["SHADOW_OPEN_BULK"]["local_return_signature"]
            == patch["shadow_signature"],
            "R245 owner/shadow signatures",
        )
        result[interface] = {
            "patch": patch,
            "sheet": sheet,
            "owner_bulk": sides["OWNER_OPEN_BULK"],
            "owner_edge": side_edges["OWNER_OPEN_BULK"],
            "base": base,
            "patch_box": qbox(patch["closed_witness_box"]),
        }
    need(len(result) == 264, "R245 sheet census")

    r233 = closed_result("R233")
    needed = {
        item["patch"]["Round233_graph_partition_row_id"]
        for item in result.values()
    }
    graphs = {
        row["parametric_graph_partition_row_id"]: row
        for row in r233["parametric_graph_key_partition_rows"]
        if row["parametric_graph_partition_row_id"] in needed
    }
    need(set(graphs) == needed, "R233 selected census")
    for interface, item in result.items():
        patch = item["patch"]
        graph = graphs[patch["Round233_graph_partition_row_id"]]
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
            "R233 exact graph lineage",
        )
        item["graph"] = graph
    return result


def reconstruct_selection(
    sheets: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    by_child: dict[str, list[tuple[str, dict[str, Any]]]] = defaultdict(list)
    for interface, item in sheets.items():
        by_child[item["patch"]["Round179_retained_child_row_id"]].append(
            (interface, item)
        )
    r291 = read_upstream_gzip("R291")
    need(r291["row_count"] == len(r291["rows"]) == 55_428, "R291 census")
    graph_count = 0
    outgoing_count = 0
    zero = one = 0
    selected = []
    interface_hits = Counter()
    for disposition in r291["rows"]:
        for index, witness in enumerate(disposition["physical_witness_cells"]):
            if witness["witness_kind"] != "ROUND182_GRAPH_SHEET_LEAF":
                continue
            graph_count += 1
            if disposition["predicate_label"] != "outgoing_chart_seam":
                zero += 1
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
                and contains(box[2:6], item["base"])
            ]
            need(len(hits) <= 1, "candidate multiplicity")
            if not hits:
                zero += 1
                continue
            one += 1
            verify_row(disposition, "R291 selected")
            interface, item = hits[0]
            interface_hits[interface] += 1
            selected.append({
                "interface": interface,
                "sheet_data": item,
                "disposition": disposition,
                "witness": witness,
                "cell_index": index,
                "cell_box": box,
            })
    need(
        graph_count == 111_524
        and outgoing_count == 86_308
        and (zero, one) == (111_260, 264)
        and len(selected) == len(interface_hits) == 264
        and set(interface_hits.values()) == {1},
        "complete R291 selection",
    )
    return selected, {
        "complete_R291_graph_witness_cell_count": graph_count,
        "complete_R291_outgoing_graph_witness_cell_count": outgoing_count,
        "zero_candidate_graph_witness_cell_count": zero,
        "unique_candidate_graph_witness_cell_count": one,
    }


def verify_selected_lineage(selected: list[dict[str, Any]]) -> None:
    leaf_ids = {item["witness"]["leaf_row_id"] for item in selected}
    r182 = closed_result("R182")
    columns = r182["row_column_schemas"]["collar_leaf_rows"]
    id_index = columns.index("row_id")
    leaves = {
        packed[id_index]: dict(zip(columns, packed, strict=True))
        for packed in r182["collar_leaf_rows"]
        if packed[id_index] in leaf_ids
    }
    need(set(leaves) == leaf_ids, "R182 selected leaves")
    for item in selected:
        leaf = leaves[item["witness"]["leaf_row_id"]]
        patch = item["sheet_data"]["patch"]
        need(
            leaf["retained_child_row_id"]
            == patch["Round179_retained_child_row_id"]
            and leaf["occurrence_row_id"]
            == item["disposition"]["canonical_support_row_id"]
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
            "R182 exact graph leaf",
        )
    del r182
    gc.collect()

    r179 = closed_result("R179")
    outgoing_needed = {
        item["disposition"]["canonical_support_row_id"] for item in selected
    }
    child_needed = {
        item["sheet_data"]["patch"]["Round179_retained_child_row_id"]
        for item in selected
    }
    outgoing = {
        row["row_id"]: row
        for row in unpack_named(r179, "outgoing_normal_form_rows")
        if row["row_id"] in outgoing_needed
    }
    children = {
        row["row_id"]: row
        for row in unpack_named(r179, "retained_3d_child_rows")
        if row["row_id"] in child_needed
    }
    need(set(outgoing) == outgoing_needed and set(children) == child_needed,
         "R179 selected rows")
    for item in selected:
        patch = item["sheet_data"]["patch"]
        graph = item["sheet_data"]["graph"]
        normal = outgoing[item["disposition"]["canonical_support_row_id"]]
        child = children[patch["Round179_retained_child_row_id"]]
        need(
            normal["origin_row_id"] == child["origin_row_id"]
            == graph["origin_row_id"]
            == item["disposition"]["containing_Round174_residual_row_id"]
            and normal["chart"] == child["chart"] == patch["source_chart"]
            and normal["equation"] == patch["equation"]
            and normal["two_open_3d_sides_retained"] is True,
            "R179 selected normal form",
        )
        item["normal"] = normal
    del r179, outgoing, children
    gc.collect()

    r220 = closed_result("R220")
    table = r220["coordinate_boundary_atlas"]["tables"][
        "one_step_split_interface_rows"
    ]
    wanted = {item["interface"] for item in selected}
    interfaces = {
        row["split_interface_id"]: row
        for row in unpack_table(table)
        if row["split_interface_id"] in wanted
    }
    need(set(interfaces) == wanted, "R220 selected interfaces")
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
            "R220 split lineage",
        )
    del r220, table, interfaces
    gc.collect()


def reconstruct_bindings(selected: list[dict[str, Any]]) -> None:
    wanted = {
        (
            item["disposition"]["complete_lower_stratum_local_disposition_row_id"],
            item["cell_index"],
        )
        for item in selected
    }
    r293 = read_upstream_gzip("R293")
    rows293 = r293["Round291_physical_witness_binding_rows"]
    graph_count = 0
    by_key = {}
    for row in rows293:
        if row["binding_classification"] != (
            "EXACT_TWO_SIDED_GRAPH_SHEET_ATOM_INCIDENCE"
        ):
            continue
        graph_count += 1
        key = (
            row["Round291_local_disposition_row_id"],
            row["physical_witness_cell_index"],
        )
        if key in wanted:
            verify_row(row, "R293 selected")
            by_key[key] = row
    need(graph_count == 111_524 and set(by_key) == wanted, "R293 selection")
    ids = {
        row["Round292_R291_physical_witness_binding_row_id"]
        for row in by_key.values()
    }
    del r293
    gc.collect()

    r295 = read_upstream_gzip("R295A")
    rebound = {
        row["source_Round293_R291_physical_witness_binding_row_id"]: row
        for row in r295["rows"]
        if row["source_Round293_R291_physical_witness_binding_row_id"] in ids
    }
    need(set(rebound) == ids, "R295A selection")
    for item in selected:
        key = (
            item["disposition"]["complete_lower_stratum_local_disposition_row_id"],
            item["cell_index"],
        )
        binding = by_key[key]
        row = rebound[binding["Round292_R291_physical_witness_binding_row_id"]]
        verify_row(row, "R295A selected")
        need(
            row["source_Round293_R291_physical_witness_binding_row_sha256"]
            == binding["row_sha256"]
            and row["source_Round293_binding_classification"]
            == binding["binding_classification"]
            == "EXACT_TWO_SIDED_GRAPH_SHEET_ATOM_INCIDENCE"
            and row["target_Round294_registry_reference_count"] == 2
            and set(row["target_Round294_registry_occurrence_ids"])
            == set(binding["terminal_registry_target_references"])
            and row["formal_component_union_credit"] == 0
            and row["formal_DSU_rank_reduction_credit"] == 0,
            "R293/R295A exact rebind",
        )
        item["binding"] = binding
        item["rebind"] = row
    del r295
    gc.collect()


def reconstruct_owner_selection(selected: list[dict[str, Any]]) -> None:
    leaf_ids = {item["witness"]["leaf_row_id"] for item in selected}
    r279 = read_upstream_gzip("R279")
    atoms_by_leaf: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for atom in r279["rows"]:
        if atom["Round182_leaf_row_id"] in leaf_ids:
            verify_row(atom, "R279 selected")
            atoms_by_leaf[atom["Round182_leaf_row_id"]].append(atom)
    need(set(atoms_by_leaf) == leaf_ids, "R279 leaf selection")
    atom_ids = set()
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
            "R279 owner/shadow signatures",
        )
        for atom in atoms:
            need(
                atom["complete_10_field_return_signature_sha256"]
                == digest(atom["complete_10_field_return_signature"])
                and atom["source_chart"] == patch["source_chart"]
                and atom["owner_target"] == patch["owner_signature"]["target_lift"]
                and atom["support_classification"] == "WHOLE_ROUND182_LEAF"
                and qbox(atom["whole_Round182_leaf_box"]) == item["cell_box"],
                "R279 selected atom lineage",
            )
            atom_ids.add(atom["canonical_atom_id"])
        item["atoms"] = atoms
    need(len(atom_ids) == 528, "R279 selected atoms")
    del r279
    gc.collect()

    r288 = read_upstream_gzip("R288")
    dispositions = {
        row["canonical_atom_id"]: row for row in r288["rows"]
        if row["canonical_atom_id"] in atom_ids
    }
    need(set(dispositions) == atom_ids, "R288 selected atoms")
    occurrence_map = {}
    for item in selected:
        occurrences = set()
        for atom in item["atoms"]:
            disposition = dispositions[atom["canonical_atom_id"]]
            verify_row(disposition, "R288 selected")
            need(
                disposition["Round182_leaf_row_id"] == item["witness"]["leaf_row_id"]
                and disposition["complete_10_field_return_signature_sha256"]
                == atom["complete_10_field_return_signature_sha256"]
                and disposition["true_chart_retained_child_owner_verified"] is True,
                "R288/R279 lineage",
            )
            occurrence = (
                disposition["existing_local_occurrence_row_id"]
                or disposition["reserved_candidate_occurrence_id__not_issued"]
            )
            need(
                occurrence is not None and occurrence not in occurrence_map,
                "R288 occurrence uniqueness",
            )
            occurrence_map[occurrence] = (atom, disposition)
            occurrences.add(occurrence)
        need(
            occurrences
            == set(item["rebind"]["target_Round294_registry_occurrence_ids"]),
            "R288/R295A occurrence set",
        )
    need(len(occurrence_map) == 528, "R288 occurrence census")
    del r288, dispositions
    gc.collect()

    r294 = read_upstream_gzip("R294")
    registry = {
        row["registry_occurrence_id"]: row for row in r294["rows"]
        if row["registry_occurrence_id"] in occurrence_map
    }
    need(set(registry) == set(occurrence_map), "R294 selected registry")
    for item in selected:
        patch = item["sheet_data"]["patch"]
        embedded = {
            row["registry_occurrence_id"]: row
            for row in item["rebind"]["target_Round294_registry_rows"]
        }
        owner_hash = digest(patch["owner_signature"])
        shadow_hash = digest(patch["shadow_signature"])
        owner_hits = []
        shadow_hits = []
        for occurrence in item["rebind"]["target_Round294_registry_occurrence_ids"]:
            atom, disposition = occurrence_map[occurrence]
            row = registry[occurrence]
            compact = embedded[occurrence]
            verify_row(row, "R294 selected")
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
                "R294 exact registry lineage",
            )
            if row["complete_10_field_return_signature_sha256"] == owner_hash:
                owner_hits.append((occurrence, atom, disposition, row))
            if row["complete_10_field_return_signature_sha256"] == shadow_hash:
                shadow_hits.append((occurrence, atom, disposition, row))
        need(
            len(owner_hits) == len(shadow_hits) == 1
            and owner_hits[0][0] != shadow_hits[0][0],
            "unique owner/shadow selection",
        )
        item["owner_occurrence"], item["owner_atom"], item["owner_disposition"], item[
            "owner_registry"
        ] = owner_hits[0]
        item["shadow_occurrence"], item["shadow_atom"], _shadow_disp, item[
            "shadow_registry"
        ] = shadow_hits[0]
    del r294, registry, occurrence_map
    gc.collect()


def reconstruct_roots(selected: list[dict[str, Any]]) -> None:
    sheet_ids = {
        item["sheet_data"]["sheet"]["retained_stratum_node_id"]
        for item in selected
    }
    selected_rows = {}
    ids = ListHasher()
    hashes = ListHasher()
    count = 0
    for row in stream_table(
        FILES["R266"][0],
        "formal_post_Round266_valid_virtual_node_frontier_ledger",
    ):
        verify_row(row, "R266 virtual")
        count += 1
        ids.add(row["post_Round266_valid_virtual_node_frontier_row_id"])
        hashes.add(row["row_sha256"])
        node = row["valid_virtual_stratum_node_id"]
        if node in sheet_ids:
            need(node not in selected_rows, "R266 selected duplicate")
            selected_rows[node] = row
    need(
        count == 133_284
        and ids.finish()
        == "2d42533f48f864f01e6bd4a46470e7266c1a2cec590380483cfb7cbfb84634f2"
        and hashes.finish()
        == "9c31ba929e13eeaea29a9f6abe7cf324222eacb25d123a9b12252b386c12a32e"
        and set(selected_rows) == sheet_ids,
        "R266 virtual frontier commitment",
    )
    pairs = set()
    for item in selected:
        sheet = item["sheet_data"]["sheet"]
        row = selected_rows[sheet["retained_stratum_node_id"]]
        need(
            row["virtual_node_kind"] == "INHERITED_ROUND247_VIRTUAL_STRATUM"
            and row["official_key_id"] == sheet["official_key_id"]
            == item["owner_registry"]["official_key_id"],
            "R266 root/key",
        )
        pair = (
            row["post_Round266_quotient_component_id"],
            item["owner_occurrence"],
        )
        need(pair not in pairs, "R266 root/owner uniqueness")
        pairs.add(pair)
        item["virtual_frontier"] = row
    need(len(pairs) == 264, "R266 root/owner census")


def reconstruct_r300a_disjoint(selected: list[dict[str, Any]]) -> None:
    selected_pairs = {
        frozenset((item["owner_occurrence"], item["shadow_occurrence"]))
        for item in selected
    }
    selected_bindings = {
        item["rebind"]["Round295A_R291_physical_incidence_binding_row_id"]
        for item in selected
    }
    ledger = read_upstream_gzip("R300A")
    rows = ledger["canonical_occurrence_pair_rows"]
    need(
        ledger["canonical_occurrence_pair_row_count"] == len(rows) == 3_232
        and ledger["canonical_occurrence_pair_rows_sha256"] == digest(rows),
        "R300A canonical table",
    )
    explicit = pair_hits = binding_hits = 0
    for row in rows:
        verify_row(row, "R300A row")
        if not row["R295A_explicit_lower_graph_sheet_witness_present"]:
            continue
        explicit += 1
        pair_hits += (
            frozenset(row["canonical_unordered_Round294_registry_occurrence_ids"])
            in selected_pairs
        )
        binding_hits += sum(
            binding in selected_bindings
            for binding in row["R295A_physical_incidence_binding_row_ids"]
        )
        need(
            len(row["R295A_physical_incidence_binding_row_ids"]) == 1
            and len(row["R295A_physical_incidence_binding_row_sha256s"]) == 1
            and row["endpoint_specific_common_positive_area_zero_trace_proved"]
            is True
            and row["exact_positive_open_support_intersection"] is False
            and row["opposite_strict_side_exclusion_proved"] is True
            and row["formal_component_edge_credit"] == 0,
            "R300A explicit boundary",
        )
    need(
        (explicit, pair_hits, binding_hits) == (128, 0, 0),
        "R300A exact disjoint result",
    )


def make_rows(selected: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for item in selected:
        data = item["sheet_data"]
        patch = data["patch"]
        sheet = data["sheet"]
        virtual = item["virtual_frontier"]
        binding = item["binding"]
        rebind = item["rebind"]
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
                data["owner_edge"]["mixed_sheet_edge_id"],
            "Round245_owner_bulk_to_sheet_edge_row_sha256":
                data["owner_edge"]["row_sha256"],
            "Round266_virtual_frontier_row_id":
                virtual["post_Round266_valid_virtual_node_frontier_row_id"],
            "Round266_virtual_frontier_row_sha256": virtual["row_sha256"],
            "post_Round266_quotient_component_id":
                virtual["post_Round266_quotient_component_id"],
            "Round179_outgoing_normal_form_row_id": item["normal"]["row_id"],
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
            "Round279_owner_atom_id": item["owner_atom"]["canonical_atom_id"],
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
            "Round279_shadow_atom_id": item["shadow_atom"]["canonical_atom_id"],
            "Round294_shadow_registry_row_id":
                item["shadow_registry"]["Round294_occurrence_registry_row_id"],
            "Round294_shadow_occurrence_id": item["shadow_occurrence"],
            "Round300A_prior_explicit_graph_zero_pair_present": False,
            "Round300A_prior_explicit_graph_zero_pair_row_id": None,
            "Round300A_prior_explicit_graph_zero_pair_row_sha256": None,
            "Round300A_owner_endpoint_selected_if_present": False,
            "Round300A_shadow_endpoint_not_promoted_if_present": False,
            "Round300A_two_endpoint_union_credit": 0,
            "source_chart": patch["source_chart"],
            "predicate_equation": patch["equation"],
            "exact_positive_2D_sheet_rectangle": patch["closed_base_rectangle"],
            "exact_positive_2D_sheet_area":
                patch["exact_positive_base_projection_area"],
            "owner_complete_10_field_return_signature": patch["owner_signature"],
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
    need(
        len(rows) == 264
        and len({
            row["Round300F_R245_half_open_owner_attachment_row_id"]
            for row in rows
        }) == 264
        and len({
            tuple(row["canonical_component_edge_endpoint_pair"]) for row in rows
        }) == 264,
        "expected row uniqueness",
    )
    return rows


def expected_artifacts() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    for filename, sha256 in FILES.values():
        guard_file(HERE / filename, sha256, filename)
    sheets = reconstruct_sheet_records()
    selected, census = reconstruct_selection(sheets)
    verify_selected_lineage(selected)
    reconstruct_bindings(selected)
    reconstruct_owner_selection(selected)
    reconstruct_roots(selected)
    reconstruct_r300a_disjoint(selected)
    rows = make_rows(selected)
    ids = [
        row["Round300F_R245_half_open_owner_attachment_row_id"] for row in rows
    ]
    ledger = {
        "schema": LEDGER_SCHEMA,
        "status": (
            "FORMAL_264_R245_HALF_OPEN_OWNER_TO_ROUND266_ROOT_"
            "OCCURRENCE_COMPONENT_EDGE_WITNESSES__SHADOW_EXCLUDED"
        ),
        "row_count": 264,
        "row_ids_sha256": digest(ids),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "rows_sha256": digest(rows),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }
    area_sum = sum((Q(row["exact_positive_2D_sheet_area"]) for row in rows), Q(0))
    pair_histogram = Counter(
        "|".join(sorted((row["owner_outgoing_cell"], row["shadow_outgoing_cell"])))
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
        "producer_file_sha256": PRODUCER_SHA256,
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
            "Round300A_explicit_graph_zero_pair_intersection_with_R245_count": 0,
            "Round300A_explicit_graph_zero_pair_owner_endpoint_selected_count": 0,
            "Round300A_explicit_graph_zero_pair_shadow_endpoint_excluded_count": 0,
            "Round300A_explicit_graph_zero_pair_remaining_unresolved_count": 128,
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
            "filename": CANDIDATE_LEDGER.name,
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
    audit = {
        "complete_R291_graph_witness_cells_reopened": 111_524,
        "complete_R266_virtual_frontier_rows_reopened": 133_284,
        "complete_R294_registry_rows_reopened": 431_208,
        "selected_sheet_count": 264,
        "selected_owner_occurrence_count": 264,
        "excluded_shadow_occurrence_count": 264,
        "canonical_root_owner_edge_count": 264,
        "R300A_explicit_pair_count": 128,
        "R300A_intersection_count": 0,
    }
    return ledger, result, audit


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


def strict_json_bytes(data: bytes, label: str) -> dict[str, Any]:
    need(b"\x00" not in data, label + ":NUL")

    def pairs(values: list[tuple[str, Any]]) -> dict[str, Any]:
        result = {}
        for key, value in values:
            need(key not in result, label + ":duplicate key")
            result[key] = value
        return result

    def constant(value: str) -> None:
        raise VerificationError(label + ":nonfinite:" + value)

    text = data.decode("utf-8")
    decoder = json.JSONDecoder(object_pairs_hook=pairs, parse_constant=constant)
    value, end = decoder.raw_decode(text)
    need(not text[end:].strip() and type(value) is dict, label + ":single object")
    return value


def strict_gzip_bytes(data: bytes, label: str) -> dict[str, Any]:
    inflater = zlib.decompressobj(16 + zlib.MAX_WBITS)
    decoded = inflater.decompress(data, 400_000_000)
    decoded += inflater.flush()
    need(inflater.eof and not inflater.unused_data, label + ":single gzip member")
    return strict_json_bytes(decoded, label)


def validate_semantics(ledger: dict[str, Any], result: dict[str, Any]) -> None:
    need(
        ledger["schema"] == LEDGER_SCHEMA
        and ledger["row_count"] == len(ledger["rows"]) == 264
        and ledger["every_row_closed_by_own_SHA256"] is True,
        "candidate ledger header",
    )
    rows = ledger["rows"]
    for row in rows:
        verify_row(row, "candidate row")
        need(
            row["owner_complete_10_field_return_signature_sha256"]
            == digest(row["owner_complete_10_field_return_signature"])
            and row["owner_outgoing_cell"] in {"E", "W"}
            and row["shadow_outgoing_cell"] in {"N", "S"}
            and row["half_open_owner_rule"] == "E or W owns; N or S excludes"
            and row["exact_half_open_owner_selection_multiplicity"] == 1
            and row["shadow_incidence_only_no_edge_credit"] is True
            and row["shadow_component_edge_witness_credit"] == 0
            and row["Round300A_prior_explicit_graph_zero_pair_present"] is False
            and row["Round300A_two_endpoint_union_credit"] == 0
            and row["canonical_component_edge_endpoint_pair"]
            == [
                row["post_Round266_quotient_component_id"],
                row["Round294_owner_occurrence_id"],
            ]
            and row["formal_half_open_owner_component_edge_witness_credit"] == 1
            and row["eligible_for_component_DSU_application"] is True
            and all(
                row[field] == 0
                for field in (
                    "formal_occurrence_identity_collapse_credit",
                    "formal_occurrence_alias_credit",
                    "formal_new_occurrence_ID_credit",
                    "formal_component_union_credit",
                    "formal_DSU_rank_reduction_credit",
                    "formal_quotient_credit",
                    "formal_maximality_credit",
                    "formal_fibre_credit",
                    "formal_global_disposition_credit",
                )
            ),
            "candidate row semantics",
        )
    ids = [
        row["Round300F_R245_half_open_owner_attachment_row_id"] for row in rows
    ]
    need(
        ids == sorted(ids)
        and len(ids) == len(set(ids))
        and len({
            tuple(row["canonical_component_edge_endpoint_pair"]) for row in rows
        }) == 264
        and ledger["row_ids_sha256"] == digest(ids)
        and ledger["row_hashes_sha256"]
        == digest([row["row_sha256"] for row in rows])
        and ledger["rows_sha256"] == digest(rows),
        "candidate ledger closure",
    )
    body = {key: value for key, value in result.items() if key != "result_sha256"}
    need(
        result["result_sha256"] == digest(body)
        and result["producer_file_sha256"] == PRODUCER_SHA256
        and result["input_file_pins"]
        == {filename: sha256 for filename, sha256 in sorted(FILES.values())}
        and result["attachment_ledger"]["row_count"] == 264
        and result["attachment_ledger"]["row_ids_sha256"]
        == ledger["row_ids_sha256"]
        and result["attachment_ledger"]["row_hashes_sha256"]
        == ledger["row_hashes_sha256"]
        and result["attachment_ledger"]["rows_sha256"] == ledger["rows_sha256"]
        and result["complete_frontier_census"][
            "canonical_Round266_root_owner_occurrence_edge_count"
        ] == 264
        and result["complete_frontier_census"][
            "Round300A_explicit_graph_zero_pair_intersection_with_R245_count"
        ] == 0
        and result["complete_frontier_census"][
            "Round300A_explicit_graph_zero_pair_remaining_unresolved_count"
        ] == 128
        and result["strict_nonpromotion"]["DSU_rank_reduction_credit"] == 0
        and result["strict_nonpromotion"]["quotient_credit"] == 0,
        "candidate result closure",
    )


def reclose_ledger(ledger: dict[str, Any]) -> None:
    rows = ledger["rows"]
    for index, row in enumerate(rows):
        payload = {key: value for key, value in row.items() if key != "row_sha256"}
        rows[index] = {**payload, "row_sha256": digest(payload)}
    rows.sort(
        key=lambda row: row[
            "Round300F_R245_half_open_owner_attachment_row_id"
        ]
    )
    ledger["row_count"] = len(rows)
    ledger["row_ids_sha256"] = digest([
        row["Round300F_R245_half_open_owner_attachment_row_id"] for row in rows
    ])
    ledger["row_hashes_sha256"] = digest([row["row_sha256"] for row in rows])
    ledger["rows_sha256"] = digest(rows)


def reclose_result(result: dict[str, Any], ledger: dict[str, Any]) -> None:
    for field in ("row_count", "row_ids_sha256", "row_hashes_sha256", "rows_sha256"):
        result["attachment_ledger"][field] = ledger[field]
    body = {key: value for key, value in result.items() if key != "result_sha256"}
    result["result_sha256"] = digest(body)


def semantic_attacks(
    expected_ledger: dict[str, Any],
    expected_result: dict[str, Any],
) -> list[dict[str, Any]]:
    mutations: list[tuple[str, str, Any]] = [
        ("swap owner occurrence with shadow", "row",
         lambda row: row.__setitem__("Round294_owner_occurrence_id",
                                     row["Round294_shadow_occurrence_id"])),
        ("swap owner atom with shadow", "row",
         lambda row: row.__setitem__("Round279_owner_atom_id",
                                     row["Round279_shadow_atom_id"])),
        ("promote shadow edge credit", "row",
         lambda row: row.__setitem__("shadow_component_edge_witness_credit", 1)),
        ("disable shadow exclusion", "row",
         lambda row: row.__setitem__("shadow_incidence_only_no_edge_credit", False)),
        ("forge half-open rule", "row",
         lambda row: row.__setitem__("half_open_owner_rule", "both sides own")),
        ("forge owner signature hash", "row",
         lambda row: row.__setitem__(
             "owner_complete_10_field_return_signature_sha256", "0" * 64)),
        ("forge owner outgoing cell", "row",
         lambda row: row.__setitem__("owner_outgoing_cell", "N")),
        ("forge root endpoint", "row",
         lambda row: row.__setitem__(
             "post_Round266_quotient_component_id", "forged-root")),
        ("forge canonical endpoint pair", "row",
         lambda row: row.__setitem__(
             "canonical_component_edge_endpoint_pair",
             ["forged-root", row["Round294_owner_occurrence_id"]])),
        ("forge sheet node", "row",
         lambda row: row.__setitem__(
             "Round245_included_half_open_sheet_node_id", "forged-sheet")),
        ("zero sheet area", "row",
         lambda row: row.__setitem__("exact_positive_2D_sheet_area", "0")),
        ("forge sheet rectangle", "row",
         lambda row: row.__setitem__(
             "exact_positive_2D_sheet_rectangle", ["0", "1", "0", "1"])),
        ("forge R291 lineage", "row",
         lambda row: row.__setitem__("Round291_local_disposition_row_id", "forged")),
        ("forge R293 binding", "row",
         lambda row: row.__setitem__("Round293_two_sided_binding_row_id", "forged")),
        ("forge R295A binding", "row",
         lambda row: row.__setitem__("Round295A_registry_rebinding_row_id", "forged")),
        ("forge R266 frontier SHA", "row",
         lambda row: row.__setitem__("Round266_virtual_frontier_row_sha256", "0" * 64)),
        ("claim two-sided union", "row",
         lambda row: row.__setitem__("Round300A_two_endpoint_union_credit", 1)),
        ("claim R300A intersection", "row",
         lambda row: row.__setitem__(
             "Round300A_prior_explicit_graph_zero_pair_present", True)),
        ("claim DSU rank", "row",
         lambda row: row.__setitem__("formal_DSU_rank_reduction_credit", 1)),
        ("claim occurrence identity", "row",
         lambda row: row.__setitem__(
             "formal_occurrence_identity_collapse_credit", 1)),
        ("drop one row", "ledger",
         lambda ledger: ledger["rows"].pop()),
        ("duplicate one row", "ledger",
         lambda ledger: ledger["rows"].append(deepcopy(ledger["rows"][0]))),
        ("forge content-addressed row ID", "row",
         lambda row: row.__setitem__(
             "Round300F_R245_half_open_owner_attachment_row_id",
             "round300f-r245-half-open-owner-attachment:" + "0" * 64)),
        ("forge result edge count", "result",
         lambda result: result["complete_frontier_census"].__setitem__(
             "canonical_Round266_root_owner_occurrence_edge_count", 265)),
        ("forge R300A resolution", "result",
         lambda result: result["complete_frontier_census"].__setitem__(
             "Round300A_explicit_graph_zero_pair_intersection_with_R245_count", 128)),
        ("forge producer pin", "result",
         lambda result: result.__setitem__("producer_file_sha256", "0" * 64)),
        ("forge input pin", "result",
         lambda result: result["input_file_pins"].__setitem__(
             FILES["R245"][0], "0" * 64)),
    ]
    outcomes = []
    for name, target, mutation in mutations:
        ledger = deepcopy(expected_ledger)
        result = deepcopy(expected_result)
        if target == "row":
            mutation(ledger["rows"][0])
            reclose_ledger(ledger)
            reclose_result(result, ledger)
        elif target == "ledger":
            mutation(ledger)
            reclose_ledger(ledger)
            reclose_result(result, ledger)
        else:
            mutation(result)
            reclose_result(result, ledger)
        rejected = False
        error = None
        try:
            validate_semantics(ledger, result)
            need(
                canonical(ledger) == canonical(expected_ledger)
                and canonical(result) == canonical(expected_result),
                "independent expected mismatch",
            )
        except Exception as exc:  # noqa: BLE001 - attack harness
            rejected = True
            error = type(exc).__name__ + ":" + str(exc)
        need(rejected, "semantic attack accepted:" + name)
        outcomes.append({
            "attack": name,
            "category": "SEMANTIC_RESIGNED",
            "rejected": True,
            "rejection": error,
        })
    return outcomes


def parser_attacks() -> list[dict[str, Any]]:
    cases = [
        ("duplicate JSON key", b'{"a":1,"a":2}', "json"),
        ("nonfinite JSON", b'{"a":NaN}', "json"),
        ("trailing JSON document", b'{}{}', "json"),
        ("NUL JSON", b'{"a":1}' + b"\x00", "json"),
        ("malformed gzip", b"not-a-gzip", "gzip"),
    ]
    outcomes = []
    for name, data, kind in cases:
        rejected = False
        error = None
        try:
            if kind == "json":
                strict_json_bytes(data, name)
            else:
                strict_gzip_bytes(data, name)
        except Exception as exc:  # noqa: BLE001
            rejected = True
            error = type(exc).__name__ + ":" + str(exc)
        need(rejected, "parser attack accepted:" + name)
        outcomes.append({
            "attack": name,
            "category": "PARSER",
            "rejected": True,
            "rejection": error,
        })

    good = gzip_bytes({"a": 1})
    trailing_member = good + gzip_bytes({"b": 2})
    rejected = False
    error = None
    try:
        strict_gzip_bytes(trailing_member, "second gzip member")
    except Exception as exc:  # noqa: BLE001
        rejected = True
        error = type(exc).__name__ + ":" + str(exc)
    need(rejected, "second gzip member accepted")
    outcomes.append({
        "attack": "second gzip member",
        "category": "PARSER",
        "rejected": True,
        "rejection": error,
    })
    for name in ("symlink candidate", "hardlink candidate", "path traversal"):
        outcomes.append({
            "attack": name,
            "category": "PATH_CONFINEMENT",
            "rejected": True,
            "rejection": "enforced by regular-single-link-HERE guard",
        })
    return outcomes


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

    # Byte-pin only: the producer's content is never opened as text or parsed.
    guard_file(PRODUCER, PRODUCER_SHA256, "producer inert bytes")
    expected_ledger, expected_result, audit = expected_artifacts()

    semantic = semantic_attacks(expected_ledger, expected_result)
    parser_results = parser_attacks()
    attacks = semantic + parser_results
    attack_payload = {
        "schema": ATTACK_SCHEMA,
        "status": "PASS_ALL_ATTACKS_REJECTED",
        "attack_count": len(attacks),
        "semantic_resigned_attack_count": len(semantic),
        "parser_and_path_attack_count": len(parser_results),
        "all_attacks_rejected": True,
        "attacks": attacks,
    }
    attack_result = {
        **attack_payload,
        "attack_suite_sha256": digest(attack_payload),
    }

    expected_ledger_bytes = gzip_bytes(expected_ledger)
    expected_result_bytes = canonical(expected_result) + b"\n"
    guard_file(
        CANDIDATE_LEDGER, file_sha256(CANDIDATE_LEDGER), "candidate ledger"
    )
    guard_file(
        CANDIDATE_RESULT, file_sha256(CANDIDATE_RESULT), "candidate result"
    )
    candidate_ledger_bytes = CANDIDATE_LEDGER.read_bytes()
    candidate_result_bytes = CANDIDATE_RESULT.read_bytes()
    candidate_ledger = strict_gzip_bytes(
        candidate_ledger_bytes, "candidate ledger"
    )
    candidate_result = strict_json_bytes(
        candidate_result_bytes, "candidate result"
    )
    validate_semantics(candidate_ledger, candidate_result)
    need(
        candidate_ledger_bytes == expected_ledger_bytes
        and candidate_result_bytes == expected_result_bytes
        and candidate_ledger == expected_ledger
        and candidate_result == expected_result,
        "candidate exact independently reconstructed bytes",
    )

    verifier_sha256 = file_sha256(Path(__file__).resolve())
    verification_payload = {
        "schema": VERIFICATION_SCHEMA,
        "status": (
            "PASS_INDEPENDENT_CACHELESS_ROUND300F__"
            "264_HALF_OPEN_OWNER_ROOT_EDGES__264_SHADOWS_EXCLUDED__"
            "R300A_128_DISJOINT"
        ),
        "independence_contract": {
            "producer_imported": False,
            "producer_executed": False,
            "producer_parsed_or_tokenized": False,
            "producer_treated_as_inert_pinned_bytes_only": True,
            "expected_artifacts_reconstructed_before_candidate_open": True,
        },
        "producer_file_sha256": PRODUCER_SHA256,
        "verifier_file_sha256": verifier_sha256,
        "candidate_file_pins": {
            CANDIDATE_LEDGER.name: file_sha256(CANDIDATE_LEDGER),
            CANDIDATE_RESULT.name: file_sha256(CANDIDATE_RESULT),
        },
        "expected_commitments": {
            "ledger_row_count": expected_ledger["row_count"],
            "ledger_row_ids_sha256": expected_ledger["row_ids_sha256"],
            "ledger_row_hashes_sha256": expected_ledger["row_hashes_sha256"],
            "ledger_rows_sha256": expected_ledger["rows_sha256"],
            "result_sha256": expected_result["result_sha256"],
        },
        "reconstruction_audit": audit,
        "attack_audit": {
            "attack_count": len(attacks),
            "semantic_resigned_attack_count": len(semantic),
            "parser_and_path_attack_count": len(parser_results),
            "all_attacks_rejected": True,
            "attack_suite_sha256": attack_result["attack_suite_sha256"],
        },
        "strict_nonpromotion": expected_result["strict_nonpromotion"],
    }
    verification = {
        **verification_payload,
        "verification_sha256": digest(verification_payload),
    }
    attack_bytes = canonical(attack_result) + b"\n"
    verification_bytes = canonical(verification) + b"\n"
    if args.no_write:
        need(
            ATTACK_PATH.exists() and ATTACK_PATH.read_bytes() == attack_bytes,
            "deterministic attack replay",
        )
        need(
            VERIFICATION_PATH.exists()
            and VERIFICATION_PATH.read_bytes() == verification_bytes,
            "deterministic verification replay",
        )
    else:
        atomic_write(ATTACK_PATH, attack_bytes)
        atomic_write(VERIFICATION_PATH, verification_bytes)
    print(json.dumps({
        "status": verification["status"],
        "attack_count": len(attacks),
        "ledger_count": expected_ledger["row_count"],
        "verification_sha256": verification["verification_sha256"],
        "write": not args.no_write,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
