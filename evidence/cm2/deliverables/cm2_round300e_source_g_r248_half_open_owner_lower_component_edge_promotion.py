#!/usr/bin/env python3
"""Promote only the R248 half-open owner side of lower graph-sheet contacts.

The sealed R295-A graph-sheet incidence rows name two adjacent occurrence
atoms.  This round intersects those rows with the sealed R235/R248 endpoint
sheet partition, proves exact leaf/frontier containment and active-factor
identity, selects the unique event-absent owner signature, and attaches only
that occurrence to the common Round266 virtual-stratum root.

The output is an edge-eligibility package.  It does not apply a DSU, identify
occurrences, compute a quotient, prove maximality, exhaust fibres, or assign
global dispositions.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import gc
import gzip
import hashlib
from io import BytesIO
import json
import os
from pathlib import Path
import stat
import tempfile
from typing import Any


HERE = Path(__file__).resolve().parent
PREFIX = (
    "cm2_round300e_source_g_r248_half_open_owner_"
    "lower_component_edge_promotion"
)
WITNESS_LEDGER = HERE / f"{PREFIX}_witness_ledger.json.gz"
ALL_EDGE_LEDGER = HERE / f"{PREFIX}_all_edge_ledger.json.gz"
NOVEL_EDGE_LEDGER = HERE / f"{PREFIX}_novel_edge_ledger.json.gz"
RESULT = HERE / f"{PREFIX}_result.json"

SCHEMA = (
    "cm2.round300e.source-g-r248-half-open-owner-"
    "lower-component-edge-promotion.v1"
)
WITNESS_SCHEMA = SCHEMA + ".witness-ledger.v1"
ALL_EDGE_SCHEMA = SCHEMA + ".all-edge-ledger.v1"
NOVEL_EDGE_SCHEMA = SCHEMA + ".novel-edge-ledger.v1"

INPUTS = {
    "R182": (
        "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json",
        "ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c",
    ),
    "R234": (
        "cm2_round234_source_g_wall_endpoint_order_depth6_"
        "materialization_certificate.json",
        "6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac",
    ),
    "R235": (
        "cm2_round235_source_g_single_endpoint_graph_word_key_"
        "partition_certificate.json",
        "e340fa1a071d85a36b54d10a45ae2fdb9d70b8c90f4c21f054c6fc9505e5e787",
    ),
    "R248": (
        "cm2_round248_source_g_wall_finite_key_retained_quotient_"
        "certificate.json",
        "fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311",
    ),
    "R266": (
        "cm2_round266_source_g_expanded_curved_face_closure_certificate.json",
        "2d30be104dc522ebb1664129894acf851180b9e5f51dd8471c33137447b599bf",
    ),
    "R291": (
        "cm2_round291_source_g_complete_lower_stratum_"
        "local_disposition_freeze_ledger.json.gz",
        "412b616b2cf75ef1373d98086cfcb2eb90a8c544e9f6b4d16a673f6cfeeb57ab",
    ),
    "R293": (
        "cm2_round293_source_g_r289_r291_witness_binding_"
        "canonical_closure_ledger.json.gz",
        "0e7395a69844734cc51563882f471987cc566db28a55ccae6e6d15d045f9e53c",
    ),
    "R295A": (
        "cm2_round295a_source_g_r291_positive_t_retained_continuation_"
        "closure_physical_witness_incidence_binding_ledger.json.gz",
        "2d9addfc9fca55366a58b29a7084c063674c3f556dd5398b038ae7d51fe97dcf",
    ),
    "R300C": (
        "cm2_round300c_source_g_virtual_stratum_new_occurrence_"
        "positive_volume_edge_promotion_edge_ledger.json.gz",
        "8c9ed8b09e994a00ca3ca4906c35b454523383b7d488f66e7a082dbbd4b1fcec",
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
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            state.update(block)
    return state.hexdigest()


def guard_file(filename: str, expected: str) -> None:
    path = HERE / filename
    info = os.lstat(path)
    need(
        path.name == filename
        and path.parent == HERE
        and stat.S_ISREG(info.st_mode)
        and not path.is_symlink()
        and info.st_nlink == 1
        and 0 < info.st_size < 2_000_000_000
        and path.resolve(strict=True).parent == HERE.resolve(strict=True),
        "confined regular input:" + filename,
    )
    need(file_sha256(path) == expected, "byte pin:" + filename)


def load_json(filename: str) -> Any:
    with (HERE / filename).open("r", encoding="utf-8") as stream:
        return json.load(stream)


def load_gzip(filename: str) -> Any:
    with gzip.open(HERE / filename, "rt", encoding="utf-8") as stream:
        return json.load(stream)


def closed_result(filename: str) -> dict[str, Any]:
    document = load_json(filename)
    need(
        type(document) is dict
        and set(document) == {"schema", "result", "result_sha256"}
        and digest(document["result"]) == document["result_sha256"],
        "closed result:" + filename,
    )
    return document["result"]


def verify_row(row: dict[str, Any], label: str) -> None:
    body = dict(row)
    claimed = body.pop("row_sha256", None)
    need(type(claimed) is str and claimed == digest(body), label + ":row closure")


def verify_rows(
    document: dict[str, Any],
    *,
    field: str,
    count_field: str,
    sha_field: str,
    label: str,
) -> list[dict[str, Any]]:
    rows = document[field]
    need(
        type(rows) is list
        and len(rows) == document[count_field]
        and digest(rows) == document[sha_field],
        label + ":table closure",
    )
    for row in rows:
        verify_row(row, label)
    return rows


def closed(payload: dict[str, Any]) -> dict[str, Any]:
    row = dict(payload)
    row["row_sha256"] = digest(payload)
    return row


def ledger(
    schema: str,
    rows: list[dict[str, Any]],
    id_field: str,
) -> dict[str, Any]:
    ids = [row[id_field] for row in rows]
    hashes = [row["row_sha256"] for row in rows]
    need(ids == sorted(ids) and len(ids) == len(set(ids)), schema + ":sorted IDs")
    return {
        "schema": schema,
        "status": "PASS",
        "row_count": len(rows),
        "row_ids_sha256": digest(ids),
        "row_hashes_sha256": digest(hashes),
        "rows_sha256": digest(rows),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }


def gzip_bytes(value: Any) -> bytes:
    output = BytesIO()
    with gzip.GzipFile(
        filename="",
        mode="wb",
        compresslevel=9,
        fileobj=output,
        mtime=0,
    ) as stream:
        stream.write(canonical(value) + b"\n")
    return output.getvalue()


def json_bytes(value: Any) -> bytes:
    return canonical(value) + b"\n"


def write_bundle(items: list[tuple[Path, bytes]]) -> None:
    staged: list[tuple[Path, Path]] = []
    try:
        for destination, data in items:
            descriptor, name = tempfile.mkstemp(
                prefix=f".{destination.name}.",
                suffix=".tmp",
                dir=HERE,
            )
            temporary = Path(name)
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            staged.append((temporary, destination))
        for temporary, destination in staged:
            os.replace(temporary, destination)
    finally:
        for temporary, _destination in staged:
            if temporary.exists():
                temporary.unlink()


def qbox(values: list[str]) -> tuple[Fraction, ...]:
    need(len(values) in {4, 6}, "box coordinate count")
    return tuple(Fraction(value) for value in values)


def contains(
    outer: tuple[Fraction, ...],
    inner: tuple[Fraction, ...],
) -> bool:
    need(len(outer) == len(inner), "containment dimension")
    return all(
        outer[index] <= inner[index]
        and inner[index + 1] <= outer[index + 1]
        for index in range(0, len(outer), 2)
    )


def equation_from_reason(reason: str) -> tuple[str, str]:
    prefix = "wall_endpoint_or_count_transition:"
    need(reason.startswith(prefix), "R235 wall reason")
    axis, wall = reason.removeprefix(prefix).split(":")
    coordinate = axis.lower()
    equation = f"(source_{coordinate}-{wall})*(target_{coordinate}-{wall})=0"
    return equation, coordinate


def sheet_source_index() -> tuple[
    dict[str, list[dict[str, Any]]],
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
]:
    r235 = closed_result(INPUTS["R235"][0])
    partition_rows = r235["single_endpoint_graph_partition_rows"]
    need(
        len(partition_rows) == 38_328
        and digest(partition_rows)
        == r235["single_endpoint_graph_partition_rows_sha256"],
        "R235 partition commitment",
    )
    partitions = {
        row["endpoint_graph_partition_row_id"]: row for row in partition_rows
    }

    r234 = closed_result(INPUTS["R234"][0])
    frontier_rows = r234["depth6_frontier_rows"]
    need(
        len(frontier_rows) == 38_376
        and digest(frontier_rows) == r234["depth6_frontier_rows_sha256"],
        "R234 frontier commitment",
    )
    wanted_frontiers = {
        row["Round234_frontier_row_id"] for row in partition_rows
    }
    frontiers = {
        row["frontier_row_id"]: row
        for row in frontier_rows
        if row["frontier_row_id"] in wanted_frontiers
    }
    need(len(frontiers) == 38_328, "R235/R234 frontier join")

    r248 = closed_result(INPUTS["R248"][0])
    sheet_table = r248["formal_wall_half_open_sheet_owner_ledger"]
    sheet_rows = sheet_table["rows"]
    need(
        sheet_table["row_count"] == len(sheet_rows) == 38_360
        and digest(sheet_rows) == sheet_table["rows_sha256"],
        "R248 sheet table commitment",
    )
    bulk_rows = r248["formal_wall_positive_volume_bulk_ledger"]["rows"]
    bulk_by_id = {
        row["wall_bulk_node_id"]: row for row in bulk_rows
    }
    need(len(bulk_by_id) == 88_936, "R248 bulk inventory")

    by_retained: dict[str, list[dict[str, Any]]] = defaultdict(list)
    singles = 0
    for sheet in sheet_rows:
        verify_row(sheet, "R248 sheet")
        if (
            sheet["source_partition_kind"]
            != "ROUND235_SINGLE_ENDPOINT_GRAPH_SHEET"
        ):
            continue
        singles += 1
        source = partitions[sheet["source_partition_row_id"]]
        frontier = frontiers[source["Round234_frontier_row_id"]]
        owner_bulk = bulk_by_id[sheet["owner_wall_bulk_node_id"]]
        verify_row(owner_bulk, "R248 owner bulk")
        need(
            sheet["Round220_split_interface_id"]
            == source["Round220_split_interface_id"]
            == frontier["Round220_split_interface_id"],
            "sheet/interface lineage",
        )
        need(
            sheet["endpoint_factor"] == source["active_endpoint_factor"],
            "sheet active factor",
        )
        need(
            sheet["owner_signature_sha256"]
            == digest(source["event_absent_signature"])
            == owner_bulk["local_return_signature_sha256"],
            "sheet unique event-absent owner signature",
        )
        need(
            sheet["owner_official_key_id"]
            == source["event_absent_signature"]["official_key_id"]
            == owner_bulk["official_key_id"],
            "sheet owner official key",
        )
        need(
            owner_bulk["branch_label"] == "EVENT_ABSENT"
            and sheet["assigned_mixed_sheet_quotient_component_id"]
            == owner_bulk["assigned_mixed_sheet_quotient_component_id"],
            "R248 owner edge component",
        )
        base = qbox(sheet["exact_closed_base_rectangle"])
        frontier_box = qbox(frontier["box"])
        need(base == frontier_box[2:6], "sheet/frontier exact base")
        by_retained[frontier["Round179_retained_child_row_id"]].append({
            "sheet": sheet,
            "source": source,
            "frontier": frontier,
            "owner_bulk": owner_bulk,
            "base": base,
            "frontier_box": frontier_box,
        })
    need(singles == 38_328, "R248 single-endpoint sheet census")
    for values in by_retained.values():
        values.sort(key=lambda item: item["sheet"]["wall_sheet_node_id"])
    return by_retained, partitions, frontiers


def graph_bindings() -> tuple[
    list[dict[str, Any]],
    dict[str, tuple[dict[str, Any], dict[str, Any]]],
    dict[str, list[Any]],
]:
    r295 = load_gzip(INPUTS["R295A"][0])
    rows295 = verify_rows(
        r295,
        field="rows",
        count_field="row_count",
        sha_field="rows_sha256",
        label="R295A",
    )
    graph_rows = [
        row for row in rows295
        if row["source_Round293_binding_classification"]
        == "EXACT_TWO_SIDED_GRAPH_SHEET_ATOM_INCIDENCE"
    ]
    need(len(graph_rows) == 111_524, "R295A graph binding census")
    wanted_dispositions = {
        row["Round291_local_disposition_row_id"] for row in graph_rows
    }
    wanted_r293 = {
        row["source_Round293_R291_physical_witness_binding_row_id"]
        for row in graph_rows
    }

    r291 = load_gzip(INPUTS["R291"][0])
    rows291 = verify_rows(
        r291,
        field="rows",
        count_field="row_count",
        sha_field="rows_sha256",
        label="R291",
    )
    dispositions = {
        row["complete_lower_stratum_local_disposition_row_id"]: row
        for row in rows291
        if row["complete_lower_stratum_local_disposition_row_id"]
        in wanted_dispositions
    }
    need(len(dispositions) == len(wanted_dispositions), "R291 disposition join")

    r293 = load_gzip(INPUTS["R293"][0])
    rows293 = verify_rows(
        r293,
        field="Round291_physical_witness_binding_rows",
        count_field="Round291_physical_witness_binding_row_count",
        sha_field="Round291_physical_witness_binding_rows_sha256",
        label="R293 physical",
    )
    sources293 = {
        row["Round292_R291_physical_witness_binding_row_id"]: row
        for row in rows293
        if row["Round292_R291_physical_witness_binding_row_id"]
        in wanted_r293
    }
    need(len(sources293) == len(wanted_r293), "R293 graph source join")

    cells: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}
    leaf_ids: set[str] = set()
    for row in graph_rows:
        disposition = dispositions[row["Round291_local_disposition_row_id"]]
        cell = disposition["physical_witness_cells"][
            row["physical_witness_cell_index"]
        ]
        source293 = sources293[
            row["source_Round293_R291_physical_witness_binding_row_id"]
        ]
        need(
            source293["row_sha256"]
            == row["source_Round293_R291_physical_witness_binding_row_sha256"]
            and source293["Round291_local_disposition_row_id"]
            == row["Round291_local_disposition_row_id"]
            and source293["physical_witness_cell_index"]
            == row["physical_witness_cell_index"],
            "R293/R295A exact lineage",
        )
        need(
            source293["binding_classification"]
            == "EXACT_TWO_SIDED_GRAPH_SHEET_ATOM_INCIDENCE"
            and source293["terminal_registry_target_references"]
            == row["target_Round294_registry_occurrence_ids"],
            "R293/R295A endpoint identity",
        )
        need(
            cell["witness_kind"] == "ROUND182_GRAPH_SHEET_LEAF"
            and disposition["source_chart"] == row["source_chart"],
            "R291 graph witness identity",
        )
        cells[row["Round295A_R291_physical_incidence_binding_row_id"]] = (
            disposition,
            cell,
        )
        leaf_ids.add(cell["leaf_row_id"])

    r182 = closed_result(INPUTS["R182"][0])
    packed_rows = r182["collar_leaf_rows"]
    need(
        len(packed_rows) == 202_840
        and digest(packed_rows)
        == r182["table_census_and_sha256"]["collar_leaf_rows"]["rows_sha256"],
        "R182 leaf table commitment",
    )
    columns = r182["row_column_schemas"]["collar_leaf_rows"]
    leaves = {
        packed[0]: packed
        for packed in packed_rows
        if packed[0] in leaf_ids
    }
    need(len(leaves) == len(leaf_ids), "R182 leaf join")
    for _binding_id, (_disposition, cell) in cells.items():
        packed = leaves[cell["leaf_row_id"]]
        leaf = dict(zip(columns, packed, strict=True))
        need(
            leaf["retained_child_row_id"] == cell["retained_child_row_id"]
            and leaf["box"] == cell["exact_box"]
            and leaf["graph_classification"]
            in {"FULL_2D", "CLIPPED_2D_BOUNDARY_1D"},
            "R182/R291 exact leaf identity",
        )
    return graph_rows, cells, leaves


def build() -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
]:
    for filename, expected in INPUTS.values():
        guard_file(filename, expected)

    sheets_by_retained, _partitions, _frontiers = sheet_source_index()
    graph_rows, cells, packed_leaves = graph_bindings()

    candidate_node_ids: set[str] = set()
    preliminary: list[dict[str, Any]] = []
    graph_binding_multiplicity: Counter[int] = Counter()
    owner_signature_match_histogram: Counter[int] = Counter()
    for binding in graph_rows:
        disposition, cell = cells[
            binding["Round295A_R291_physical_incidence_binding_row_id"]
        ]
        cell_box = qbox(cell["exact_box"])
        targets = binding["target_Round294_registry_rows"]
        need(len(targets) == 2, "R295A two endpoint rows")
        local: list[dict[str, Any]] = []
        for joined in sheets_by_retained.get(
            cell["retained_child_row_id"], []
        ):
            sheet = joined["sheet"]
            source = joined["source"]
            frontier = joined["frontier"]
            equation, coordinate = equation_from_reason(source["reason_label"])
            if (
                frontier["chart"] != binding["source_chart"]
                or equation != disposition["predicate_equation"]
            ):
                continue
            base = joined["base"]
            if base != cell_box[2:6]:
                continue
            need(
                contains(cell_box, joined["frontier_box"]),
                "full R234 frontier box contained in R182/R291 leaf",
            )
            matching = [
                index for index, target in enumerate(targets)
                if target["complete_10_field_return_signature_sha256"]
                == sheet["owner_signature_sha256"]
            ]
            owner_signature_match_histogram[len(matching)] += 1
            need(len(matching) == 1, "unique owner endpoint signature")
            owner_index = matching[0]
            owner = targets[owner_index]
            present = targets[1 - owner_index]
            need(
                owner["official_key_id"] == sheet["owner_official_key_id"],
                "owner endpoint exact key",
            )
            need(
                present["complete_10_field_return_signature_sha256"]
                != sheet["owner_signature_sha256"],
                "present-side signature excluded",
            )
            active_factor = (
                f"{source['active_endpoint_factor']}_{coordinate}-"
                + source["reason_label"].rsplit(":", 1)[1]
            )
            candidate_node_ids.update({
                sheet["wall_sheet_node_id"],
                sheet["owner_wall_bulk_node_id"],
            })
            local.append({
                "binding": binding,
                "disposition": disposition,
                "cell": cell,
                "leaf_packed": packed_leaves[cell["leaf_row_id"]],
                "sheet": sheet,
                "source": source,
                "frontier": frontier,
                "owner_bulk": joined["owner_bulk"],
                "owner": owner,
                "present": present,
                "cell_box": cell_box,
                "frontier_box": joined["frontier_box"],
                "base": base,
                "active_factor": active_factor,
            })
        graph_binding_multiplicity[len(local)] += 1
        preliminary.extend(local)

    need(
        len(preliminary) == 12_992
        and graph_binding_multiplicity[0] == 111_052
        and sum(
            count for multiplicity, count in graph_binding_multiplicity.items()
            if multiplicity
        ) == 472
        and owner_signature_match_histogram == {1: 12_992},
        "exact half-open-owner join census",
    )

    r266 = closed_result(INPUTS["R266"][0])
    virtual_table = r266[
        "formal_post_Round266_valid_virtual_node_frontier_ledger"
    ]
    virtual_rows = virtual_table["rows"]
    need(
        virtual_table["row_count"] == len(virtual_rows) == 133_284
        and digest(virtual_rows) == virtual_table["rows_sha256"],
        "R266 virtual frontier commitment",
    )
    virtual = {
        row["valid_virtual_stratum_node_id"]: row
        for row in virtual_rows
        if row["valid_virtual_stratum_node_id"] in candidate_node_ids
    }
    need(len(virtual) == len(candidate_node_ids), "R266 node join")
    for row in virtual.values():
        verify_row(row, "R266 virtual node")

    r300c = load_gzip(INPUTS["R300C"][0])
    rows300c = verify_rows(
        r300c,
        field="rows",
        count_field="row_count",
        sha_field="rows_sha256",
        label="R300C edge",
    )
    pairs300c = {
        tuple(row["canonical_component_edge_endpoint_pair"])
        for row in rows300c
    }
    need(len(pairs300c) == 6_314, "R300C canonical edge census")

    witness_rows: list[dict[str, Any]] = []
    for item in preliminary:
        binding = item["binding"]
        disposition = item["disposition"]
        cell = item["cell"]
        sheet = item["sheet"]
        source = item["source"]
        frontier = item["frontier"]
        owner_bulk = item["owner_bulk"]
        owner = item["owner"]
        present = item["present"]
        sheet_frontier = virtual[sheet["wall_sheet_node_id"]]
        bulk_frontier = virtual[sheet["owner_wall_bulk_node_id"]]
        need(
            sheet_frontier["post_Round266_quotient_component_id"]
            == bulk_frontier["post_Round266_quotient_component_id"],
            "R266 sheet/owner root identity",
        )
        root = sheet_frontier["post_Round266_quotient_component_id"]
        payload = {
            "source_Round295A_physical_incidence_binding_row_id":
                binding["Round295A_R291_physical_incidence_binding_row_id"],
            "source_Round295A_physical_incidence_binding_row_sha256":
                binding["row_sha256"],
            "source_Round293_physical_witness_binding_row_id":
                binding[
                    "source_Round293_R291_physical_witness_binding_row_id"
                ],
            "source_Round293_physical_witness_binding_row_sha256":
                binding[
                    "source_Round293_R291_physical_witness_binding_row_sha256"
                ],
            "source_Round291_local_disposition_row_id":
                binding["Round291_local_disposition_row_id"],
            "source_Round291_local_disposition_row_sha256":
                disposition["row_sha256"],
            "physical_witness_cell_index":
                binding["physical_witness_cell_index"],
            "source_Round182_collar_leaf_row_id": cell["leaf_row_id"],
            "source_Round182_collar_leaf_packed_row_sha256":
                digest(item["leaf_packed"]),
            "source_Round235_endpoint_graph_partition_row_id":
                source["endpoint_graph_partition_row_id"],
            "source_Round235_endpoint_graph_partition_row_sha256":
                digest(source),
            "source_Round234_frontier_row_id": frontier["frontier_row_id"],
            "source_Round234_frontier_row_sha256": digest(frontier),
            "source_Round248_wall_sheet_node_id":
                sheet["wall_sheet_node_id"],
            "source_Round248_wall_sheet_row_sha256": sheet["row_sha256"],
            "source_Round248_owner_edge_id":
                sheet["owner_mixed_sheet_edge_id"],
            "source_Round248_owner_wall_bulk_node_id":
                sheet["owner_wall_bulk_node_id"],
            "source_Round248_owner_wall_bulk_row_sha256":
                owner_bulk["row_sha256"],
            "source_Round266_sheet_frontier_row_id":
                sheet_frontier[
                    "post_Round266_valid_virtual_node_frontier_row_id"
                ],
            "source_Round266_sheet_frontier_row_sha256":
                sheet_frontier["row_sha256"],
            "source_Round266_owner_bulk_frontier_row_id":
                bulk_frontier[
                    "post_Round266_valid_virtual_node_frontier_row_id"
                ],
            "source_Round266_owner_bulk_frontier_row_sha256":
                bulk_frontier["row_sha256"],
            "post_Round266_quotient_component_id": root,
            "owner_Round294_registry_occurrence_id":
                owner["registry_occurrence_id"],
            "owner_Round294_registry_row_id":
                owner["Round294_occurrence_registry_row_id"],
            "owner_Round294_registry_row_sha256":
                owner["Round294_occurrence_registry_row_sha256"],
            "owner_complete_10_field_return_signature_sha256":
                owner["complete_10_field_return_signature_sha256"],
            "owner_official_key_id": owner["official_key_id"],
            "owner_official_key_ordinal": owner["official_key_ordinal"],
            "excluded_present_side_Round294_registry_occurrence_id":
                present["registry_occurrence_id"],
            "excluded_present_side_complete_10_field_return_signature_sha256":
                present["complete_10_field_return_signature_sha256"],
            "exact_R182_R291_leaf_box": cell["exact_box"],
            "exact_R234_frontier_box": frontier["box"],
            "exact_R248_sheet_base_rectangle":
                sheet["exact_closed_base_rectangle"],
            "predicate_equation": disposition["predicate_equation"],
            "R235_reason_label": source["reason_label"],
            "active_endpoint_factor": source["active_endpoint_factor"],
            "active_equation_factor": item["active_factor"],
            "half_open_owner_rule": sheet["half_open_owner_rule"],
            "proof_exact_base_equality": True,
            "proof_full_six_coordinate_box_containment": True,
            "proof_active_factor_identity": True,
            "proof_unique_event_absent_owner_signature": True,
            "proof_owner_key_identity": True,
            "proof_sheet_and_owner_bulk_same_Round266_root": True,
            "present_side_component_edge_credit": 0,
            "mere_two_sided_incidence_component_edge_credit": 0,
            "formal_half_open_owner_component_edge_witness_credit": 1,
            "eligible_for_component_DSU_application": True,
            "formal_occurrence_identity_collapse_credit": 0,
            "formal_component_union_application_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_quotient_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
        }
        witness_id = (
            "round300e-r248-half-open-owner-component-edge-witness:"
            + digest(payload)
        )
        witness_rows.append(closed({
            "Round300E_half_open_owner_component_edge_witness_row_id":
                witness_id,
            **payload,
        }))
    witness_rows.sort(
        key=lambda row:
        row["Round300E_half_open_owner_component_edge_witness_row_id"]
    )
    need(
        len(witness_rows) == 12_992
        and len({
            row["source_Round248_wall_sheet_node_id"] for row in witness_rows
        }) == 12_992,
        "witness and sheet uniqueness",
    )

    all_edge_rows: list[dict[str, Any]] = []
    for witness in witness_rows:
        root = witness["post_Round266_quotient_component_id"]
        occurrence = witness["owner_Round294_registry_occurrence_id"]
        pair = sorted([root, occurrence])
        payload = {
            "canonical_component_edge_endpoint_pair": pair,
            "post_Round266_quotient_component_id": root,
            "owner_Round294_registry_occurrence_id": occurrence,
            "official_key_id": witness["owner_official_key_id"],
            "official_key_ordinal": witness["owner_official_key_ordinal"],
            "complete_10_field_return_signature_sha256":
                witness[
                    "owner_complete_10_field_return_signature_sha256"
                ],
            "source_half_open_owner_witness_row_id":
                witness[
                    "Round300E_half_open_owner_component_edge_witness_row_id"
                ],
            "source_half_open_owner_witness_row_sha256":
                witness["row_sha256"],
            "already_present_in_Round300C_positive_volume_edge_ledger":
                tuple(pair) in pairs300c,
            "edge_semantics":
                "R248_EVENT_ABSENT_HALF_OPEN_OWNER_TO_ROUND266_ROOT__"
                "COMPONENT_CONNECTIVITY_NOT_OCCURRENCE_IDENTITY",
            "formal_half_open_owner_component_edge_credit": 1,
            "eligible_for_component_DSU_application": True,
            "present_side_component_edge_credit": 0,
            "mere_two_sided_incidence_component_edge_credit": 0,
            "formal_occurrence_identity_collapse_credit": 0,
            "formal_component_union_application_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_quotient_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
        }
        edge_id = (
            "round300e-r248-half-open-owner-component-edge:"
            + digest(payload)
        )
        all_edge_rows.append(closed({
            "Round300E_half_open_owner_component_edge_row_id": edge_id,
            **payload,
        }))
    all_edge_rows.sort(
        key=lambda row: row["Round300E_half_open_owner_component_edge_row_id"]
    )
    pairs = [
        tuple(row["canonical_component_edge_endpoint_pair"])
        for row in all_edge_rows
    ]
    need(
        len(all_edge_rows) == len(set(pairs)) == 12_992,
        "canonical all-edge dedupe",
    )

    novel_edge_rows: list[dict[str, Any]] = []
    all_by_pair = {
        tuple(row["canonical_component_edge_endpoint_pair"]): row
        for row in all_edge_rows
    }
    for pair in sorted(set(pairs) - pairs300c):
        source_edge = all_by_pair[pair]
        payload = {
            "canonical_component_edge_endpoint_pair": list(pair),
            "source_Round300E_all_edge_row_id":
                source_edge["Round300E_half_open_owner_component_edge_row_id"],
            "source_Round300E_all_edge_row_sha256":
                source_edge["row_sha256"],
            "absence_from_Round300C_edge_ledger_proved_by_complete_pair_set":
                True,
            "formal_novel_component_edge_credit": 1,
            "eligible_for_component_DSU_application": True,
            "formal_component_union_application_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_quotient_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
        }
        novel_id = (
            "round300e-r248-half-open-owner-novel-component-edge:"
            + digest(payload)
        )
        novel_edge_rows.append(closed({
            "Round300E_novel_half_open_owner_component_edge_row_id":
                novel_id,
            **payload,
        }))
    novel_edge_rows.sort(
        key=lambda row:
        row["Round300E_novel_half_open_owner_component_edge_row_id"]
    )
    overlap_count = sum(
        row["already_present_in_Round300C_positive_volume_edge_ledger"]
        for row in all_edge_rows
    )
    need(
        overlap_count == 472
        and len(novel_edge_rows) == 12_520,
        "R300C overlap/novel census",
    )

    witness_document = ledger(
        WITNESS_SCHEMA,
        witness_rows,
        "Round300E_half_open_owner_component_edge_witness_row_id",
    )
    all_edge_document = ledger(
        ALL_EDGE_SCHEMA,
        all_edge_rows,
        "Round300E_half_open_owner_component_edge_row_id",
    )
    novel_edge_document = ledger(
        NOVEL_EDGE_SCHEMA,
        novel_edge_rows,
        "Round300E_novel_half_open_owner_component_edge_row_id",
    )

    def summary(
        document: dict[str, Any], filename: str
    ) -> dict[str, Any]:
        return {
            "filename": filename,
            "schema": document["schema"],
            "row_count": document["row_count"],
            "row_ids_sha256": document["row_ids_sha256"],
            "row_hashes_sha256": document["row_hashes_sha256"],
            "rows_sha256": document["rows_sha256"],
        }

    multiplicity = {
        str(key): value for key, value
        in sorted(graph_binding_multiplicity.items())
    }
    result_payload = {
        "schema": SCHEMA,
        "status":
            "PASS_R300E_R248_HALF_OPEN_OWNER_COMPONENT_EDGE_PROMOTION__"
            "12992_ALL__472_R300C_OVERLAP__12520_NOVEL",
        "producer_file_sha256": file_sha256(Path(__file__).resolve()),
        "input_file_pins": {
            filename: expected for filename, expected in INPUTS.values()
        },
        "source_audit": {
            "R295A_two_sided_graph_sheet_binding_count": 111_524,
            "binding_with_R248_sheet_subset_count": 472,
            "binding_without_R248_sheet_subset_count": 111_052,
            "R248_matched_sheet_count": 12_992,
            "distinct_R248_matched_sheet_count": 12_992,
            "binding_matched_sheet_multiplicity_histogram": multiplicity,
            "exact_equal_base_rectangle_count": 12_992,
            "full_six_coordinate_box_containment_count": 12_992,
            "active_factor_equation_identity_count": 12_992,
            "unique_event_absent_owner_signature_count": 12_992,
            "owner_official_key_identity_count": 12_992,
            "sheet_owner_bulk_same_Round266_root_count": 12_992,
            "ambiguous_owner_signature_count": 0,
            "present_side_promoted_count": 0,
        },
        "edge_audit": {
            "all_canonical_half_open_owner_edge_count": 12_992,
            "duplicate_canonical_pair_count": 0,
            "already_in_Round300C_edge_count": 472,
            "novel_against_Round300C_edge_count": 12_520,
        },
        "witness_ledger": summary(
            witness_document, WITNESS_LEDGER.name
        ),
        "all_edge_ledger": summary(
            all_edge_document, ALL_EDGE_LEDGER.name
        ),
        "novel_edge_ledger": summary(
            novel_edge_document, NOVEL_EDGE_LEDGER.name
        ),
        "scope_contract": {
            "only_event_absent_half_open_owner_endpoint_is_promoted": True,
            "present_side_is_never_promoted": True,
            "mere_two_sided_graph_incidence_is_not_an_edge": True,
            "full_R234_frontier_containment_in_R182_R291_leaf_required": True,
            "active_equation_factor_identity_required": True,
            "unique_owner_signature_and_owner_key_required": True,
            "R248_sheet_owner_bulk_and_R266_root_lineage_required": True,
            "edge_means_component_connectivity_not_occurrence_identity": True,
        },
        "strict_nonpromotion": {
            "occurrence_identity_collapse_credit": 0,
            "component_union_application_credit": 0,
            "DSU_rank_reduction_credit": 0,
            "quotient_credit": 0,
            "maximality_credit": 0,
            "fibre_credit": 0,
            "global_disposition_credit": 0,
            "post_Round300E_quotient_component_count": None,
        },
        "required_next":
            "freeze remaining legal edge channels, then apply the complete "
            "deduplicated edge set in one expanded-registry DSU rebuild",
    }
    result_document = dict(result_payload)
    result_document["result_sha256"] = digest(result_payload)
    return (
        witness_document,
        all_edge_document,
        novel_edge_document,
        result_document,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()
    witness, all_edges, novel_edges, result = build()
    witness_data = gzip_bytes(witness)
    all_edge_data = gzip_bytes(all_edges)
    novel_edge_data = gzip_bytes(novel_edges)
    result_data = json_bytes(result)
    if not arguments.no_write:
        write_bundle([
            (WITNESS_LEDGER, witness_data),
            (ALL_EDGE_LEDGER, all_edge_data),
            (NOVEL_EDGE_LEDGER, novel_edge_data),
            (RESULT, result_data),
        ])
    print(result["status"])
    print(json.dumps({
        "witness_rows": witness["row_count"],
        "all_edges": all_edges["row_count"],
        "novel_edges": novel_edges["row_count"],
        "witness_file_sha256": hashlib.sha256(witness_data).hexdigest(),
        "all_edge_file_sha256": hashlib.sha256(all_edge_data).hexdigest(),
        "novel_edge_file_sha256": hashlib.sha256(novel_edge_data).hexdigest(),
        "result_file_sha256": hashlib.sha256(result_data).hexdigest(),
        "result_sha256": result["result_sha256"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
