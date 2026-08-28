#!/usr/bin/env python3
"""Independent verifier for the Round300-E half-open-owner edge package.

The producer is never imported, executed, or parsed.  Its bytes are used only
as an inert hash-pinned artifact.  Expected witness, all-edge, novel-edge, and
result objects are reconstructed from the sealed upstream mathematical data
before any candidate output is opened.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from copy import deepcopy
from fractions import Fraction
import gc
import gzip
import hashlib
from io import BytesIO
import json
import math
import os
from pathlib import Path
import stat
import tempfile
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
PREFIX = (
    "cm2_round300e_source_g_r248_half_open_owner_"
    "lower_component_edge_promotion"
)
PRODUCER = HERE / f"{PREFIX}.py"
WITNESS_LEDGER = HERE / f"{PREFIX}_witness_ledger.json.gz"
ALL_EDGE_LEDGER = HERE / f"{PREFIX}_all_edge_ledger.json.gz"
NOVEL_EDGE_LEDGER = HERE / f"{PREFIX}_novel_edge_ledger.json.gz"
RESULT = HERE / f"{PREFIX}_result.json"
ATTACKS = HERE / f"{PREFIX}_attack_suite.json"
VERIFICATION = HERE / f"{PREFIX}_verification.json"

SCHEMA = (
    "cm2.round300e.source-g-r248-half-open-owner-"
    "lower-component-edge-promotion.v1"
)
WITNESS_SCHEMA = SCHEMA + ".witness-ledger.v1"
ALL_EDGE_SCHEMA = SCHEMA + ".all-edge-ledger.v1"
NOVEL_EDGE_SCHEMA = SCHEMA + ".novel-edge-ledger.v1"
ATTACK_SCHEMA = SCHEMA + ".independent-attack-suite.v1"
VERIFICATION_SCHEMA = SCHEMA + ".independent-verification.v1"

PRODUCER_SHA256 = (
    "c4cc1e2eafe1f1db2da143da365a56a7907933a2df0d77dd433a16eede6f8dbe"
)
WITNESS_FILE_SHA256 = (
    "69f480da55e917b7b75bfe1efa823a9228d9b563f6f3aabd4e2a364c9e50eb9f"
)
ALL_EDGE_FILE_SHA256 = (
    "4aa7ae76d984d15b345d5d6805ec4f06a47e30a46fff1315f346e81f1f17122f"
)
NOVEL_EDGE_FILE_SHA256 = (
    "a5c37aad322be53b9135fcef429274812639ab456d73cd43c03e64eb0c572501"
)
RESULT_FILE_SHA256 = (
    "193c74535431789ba4fcdad598487916712d6ad1c04f191a083076e4a05f7e3e"
)
RESULT_SELF_SHA256 = (
    "58adb4b2ffb70601df69a833deca7106b2cc2d9a06c851b668be7aaae51913b9"
)

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

WITNESS_ID = "Round300E_half_open_owner_component_edge_witness_row_id"
ALL_EDGE_ID = "Round300E_half_open_owner_component_edge_row_id"
NOVEL_EDGE_ID = "Round300E_novel_half_open_owner_component_edge_row_id"


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


def check_regular(path: Path, expected: str, label: str) -> None:
    info = os.lstat(path)
    need(
        path.parent == HERE
        and path.name == path.resolve(strict=True).name
        and stat.S_ISREG(info.st_mode)
        and not path.is_symlink()
        and info.st_nlink == 1
        and 0 < info.st_size < 2_000_000_000,
        label + ":regular single-link confined file",
    )
    need(file_sha256(path) == expected, label + ":byte pin")


def strict_object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in output, "duplicate JSON key:" + key)
        output[key] = value
    return output


def reject_constant(value: str) -> Any:
    raise VerificationError("nonfinite JSON constant:" + value)


def strict_json_bytes(raw: bytes) -> Any:
    need(b"\x00" not in raw, "NUL JSON")
    return json.loads(
        raw,
        object_pairs_hook=strict_object_pairs,
        parse_constant=reject_constant,
    )


def read_json(path: Path) -> Any:
    return strict_json_bytes(path.read_bytes())


def read_gzip(path: Path) -> Any:
    raw = path.read_bytes()
    need(raw[:2] == b"\x1f\x8b", path.name + ":gzip magic")
    try:
        decoded = gzip.decompress(raw)
    except Exception as exc:
        raise VerificationError(path.name + ":gzip decode") from exc
    return strict_json_bytes(decoded)


def closed_result(filename: str) -> dict[str, Any]:
    document = read_json(HERE / filename)
    need(
        type(document) is dict
        and set(document) == {"schema", "result", "result_sha256"}
        and document["result_sha256"] == digest(document["result"]),
        filename + ":closed result",
    )
    return document["result"]


def verify_row(row: dict[str, Any], label: str) -> None:
    body = dict(row)
    claimed = body.pop("row_sha256", None)
    need(type(claimed) is str and claimed == digest(body), label + ":row hash")


def verify_table(
    document: dict[str, Any],
    field: str,
    count_field: str,
    hash_field: str,
    label: str,
) -> list[dict[str, Any]]:
    rows = document[field]
    need(
        type(rows) is list
        and len(rows) == document[count_field]
        and digest(rows) == document[hash_field],
        label + ":table commitment",
    )
    for row in rows:
        verify_row(row, label)
    return rows


def close(payload: dict[str, Any]) -> dict[str, Any]:
    row = dict(payload)
    row["row_sha256"] = digest(payload)
    return row


def make_ledger(
    schema: str,
    rows: list[dict[str, Any]],
    id_field: str,
) -> dict[str, Any]:
    ids = [row[id_field] for row in rows]
    hashes = [row["row_sha256"] for row in rows]
    need(ids == sorted(ids) and len(ids) == len(set(ids)), schema + ":IDs")
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


def gzip_encoding(value: Any) -> bytes:
    buffer = BytesIO()
    with gzip.GzipFile(
        filename="",
        mode="wb",
        compresslevel=9,
        fileobj=buffer,
        mtime=0,
    ) as stream:
        stream.write(canonical(value) + b"\n")
    return buffer.getvalue()


def plain_encoding(value: Any) -> bytes:
    return canonical(value) + b"\n"


def rational_box(values: list[str]) -> tuple[Fraction, ...]:
    need(len(values) in {4, 6}, "box arity")
    return tuple(Fraction(value) for value in values)


def includes(
    outer: tuple[Fraction, ...],
    inner: tuple[Fraction, ...],
) -> bool:
    need(len(outer) == len(inner), "box dimension")
    return all(
        outer[index] <= inner[index]
        and inner[index + 1] <= outer[index + 1]
        for index in range(0, len(outer), 2)
    )


def factor_data(reason: str, active: str) -> tuple[str, str]:
    marker = "wall_endpoint_or_count_transition:"
    need(reason.startswith(marker), "wall reason")
    axis, wall = reason[len(marker):].split(":")
    coordinate = axis.lower()
    equation = f"(source_{coordinate}-{wall})*(target_{coordinate}-{wall})=0"
    factor = f"{active}_{coordinate}-{wall}"
    return equation, factor


def collect_sheet_records() -> dict[str, list[dict[str, Any]]]:
    partition_result = closed_result(INPUTS["R235"][0])
    partition_rows = partition_result["single_endpoint_graph_partition_rows"]
    need(
        len(partition_rows) == 38_328
        and digest(partition_rows)
        == partition_result["single_endpoint_graph_partition_rows_sha256"],
        "R235 complete partitions",
    )
    partitions = {
        row["endpoint_graph_partition_row_id"]: row
        for row in partition_rows
    }

    frontier_result = closed_result(INPUTS["R234"][0])
    frontier_rows = frontier_result["depth6_frontier_rows"]
    need(
        len(frontier_rows) == 38_376
        and digest(frontier_rows)
        == frontier_result["depth6_frontier_rows_sha256"],
        "R234 complete frontier",
    )
    needed_frontiers = {
        row["Round234_frontier_row_id"] for row in partition_rows
    }
    frontiers = {
        row["frontier_row_id"]: row
        for row in frontier_rows
        if row["frontier_row_id"] in needed_frontiers
    }
    need(len(frontiers) == 38_328, "R234/R235 exact join")

    quotient = closed_result(INPUTS["R248"][0])
    sheets = quotient["formal_wall_half_open_sheet_owner_ledger"]["rows"]
    bulks = quotient["formal_wall_positive_volume_bulk_ledger"]["rows"]
    need(
        len(sheets) == 38_360
        and digest(sheets)
        == quotient["formal_wall_half_open_sheet_owner_ledger"]["rows_sha256"],
        "R248 sheet commitment",
    )
    by_bulk = {row["wall_bulk_node_id"]: row for row in bulks}
    need(len(by_bulk) == 88_936, "R248 bulk inventory")

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    selected = 0
    for sheet in sheets:
        verify_row(sheet, "R248 sheet")
        if sheet["source_partition_kind"] != "ROUND235_SINGLE_ENDPOINT_GRAPH_SHEET":
            continue
        selected += 1
        partition = partitions[sheet["source_partition_row_id"]]
        frontier = frontiers[partition["Round234_frontier_row_id"]]
        bulk = by_bulk[sheet["owner_wall_bulk_node_id"]]
        verify_row(bulk, "R248 bulk")
        absent_hash = digest(partition["event_absent_signature"])
        need(
            sheet["Round220_split_interface_id"]
            == partition["Round220_split_interface_id"]
            == frontier["Round220_split_interface_id"],
            "sheet interface ancestry",
        )
        need(
            sheet["endpoint_factor"] == partition["active_endpoint_factor"],
            "sheet endpoint factor",
        )
        need(
            sheet["owner_signature_sha256"]
            == absent_hash
            == bulk["local_return_signature_sha256"],
            "event-absent signature owner",
        )
        need(
            sheet["owner_official_key_id"]
            == partition["event_absent_signature"]["official_key_id"]
            == bulk["official_key_id"],
            "event-absent key owner",
        )
        need(
            bulk["branch_label"] == "EVENT_ABSENT"
            and sheet["assigned_mixed_sheet_quotient_component_id"]
            == bulk["assigned_mixed_sheet_quotient_component_id"],
            "R248 formal owner edge",
        )
        base = rational_box(sheet["exact_closed_base_rectangle"])
        frontier_box = rational_box(frontier["box"])
        need(base == frontier_box[2:6], "sheet/frontier base identity")
        grouped[frontier["Round179_retained_child_row_id"]].append({
            "sheet": sheet,
            "partition": partition,
            "frontier": frontier,
            "bulk": bulk,
            "base": base,
            "frontier_box": frontier_box,
        })
    need(selected == 38_328, "single-endpoint sheet inventory")
    return grouped


def collect_graph_records() -> tuple[
    list[dict[str, Any]],
    dict[str, tuple[dict[str, Any], dict[str, Any]]],
    dict[str, list[Any]],
]:
    promoted = read_gzip(HERE / INPUTS["R295A"][0])
    promoted_rows = verify_table(
        promoted, "rows", "row_count", "rows_sha256", "R295A"
    )
    bindings = [
        row for row in promoted_rows
        if row["source_Round293_binding_classification"]
        == "EXACT_TWO_SIDED_GRAPH_SHEET_ATOM_INCIDENCE"
    ]
    need(len(bindings) == 111_524, "R295A graph binding inventory")

    disposition_ids = {
        row["Round291_local_disposition_row_id"] for row in bindings
    }
    source_ids = {
        row["source_Round293_R291_physical_witness_binding_row_id"]
        for row in bindings
    }
    frozen = read_gzip(HERE / INPUTS["R291"][0])
    frozen_rows = verify_table(
        frozen, "rows", "row_count", "rows_sha256", "R291"
    )
    dispositions = {
        row["complete_lower_stratum_local_disposition_row_id"]: row
        for row in frozen_rows
        if row["complete_lower_stratum_local_disposition_row_id"]
        in disposition_ids
    }
    need(len(dispositions) == len(disposition_ids), "R291 disposition coverage")

    canonical = read_gzip(HERE / INPUTS["R293"][0])
    canonical_rows = verify_table(
        canonical,
        "Round291_physical_witness_binding_rows",
        "Round291_physical_witness_binding_row_count",
        "Round291_physical_witness_binding_rows_sha256",
        "R293",
    )
    sources = {
        row["Round292_R291_physical_witness_binding_row_id"]: row
        for row in canonical_rows
        if row["Round292_R291_physical_witness_binding_row_id"] in source_ids
    }
    need(len(sources) == len(source_ids), "R293 source coverage")

    cells: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}
    leaf_ids: set[str] = set()
    for binding in bindings:
        disposition = dispositions[binding["Round291_local_disposition_row_id"]]
        cell = disposition["physical_witness_cells"][
            binding["physical_witness_cell_index"]
        ]
        source = sources[
            binding["source_Round293_R291_physical_witness_binding_row_id"]
        ]
        need(
            source["row_sha256"]
            == binding["source_Round293_R291_physical_witness_binding_row_sha256"]
            and source["Round291_local_disposition_row_id"]
            == binding["Round291_local_disposition_row_id"]
            and source["physical_witness_cell_index"]
            == binding["physical_witness_cell_index"],
            "R293/R295A row lineage",
        )
        need(
            source["binding_classification"]
            == "EXACT_TWO_SIDED_GRAPH_SHEET_ATOM_INCIDENCE"
            and source["terminal_registry_target_references"]
            == binding["target_Round294_registry_occurrence_ids"],
            "R293/R295A endpoints",
        )
        need(
            cell["witness_kind"] == "ROUND182_GRAPH_SHEET_LEAF"
            and disposition["source_chart"] == binding["source_chart"],
            "R291 graph cell",
        )
        cells[binding["Round295A_R291_physical_incidence_binding_row_id"]] = (
            disposition,
            cell,
        )
        leaf_ids.add(cell["leaf_row_id"])

    arrangement = closed_result(INPUTS["R182"][0])
    packed_rows = arrangement["collar_leaf_rows"]
    need(
        len(packed_rows) == 202_840
        and digest(packed_rows)
        == arrangement["table_census_and_sha256"]["collar_leaf_rows"][
            "rows_sha256"
        ],
        "R182 leaf commitment",
    )
    columns = arrangement["row_column_schemas"]["collar_leaf_rows"]
    leaves = {
        packed[0]: packed for packed in packed_rows if packed[0] in leaf_ids
    }
    need(len(leaves) == len(leaf_ids), "R182 leaf coverage")
    for disposition, cell in cells.values():
        packed = leaves[cell["leaf_row_id"]]
        leaf = dict(zip(columns, packed, strict=True))
        need(
            leaf["retained_child_row_id"] == cell["retained_child_row_id"]
            and leaf["box"] == cell["exact_box"]
            and leaf["graph_classification"]
            in {"FULL_2D", "CLIPPED_2D_BOUNDARY_1D"},
            "R182/R291 leaf equality",
        )
    return bindings, cells, leaves


def reconstruct_expected() -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    set[tuple[str, str]],
]:
    for filename, expected in INPUTS.values():
        check_regular(HERE / filename, expected, filename)

    by_retained = collect_sheet_records()
    bindings, cells, leaves = collect_graph_records()

    joined: list[dict[str, Any]] = []
    multiplicity: Counter[int] = Counter()
    owner_counts: Counter[int] = Counter()
    wanted_nodes: set[str] = set()
    for binding in bindings:
        disposition, cell = cells[
            binding["Round295A_R291_physical_incidence_binding_row_id"]
        ]
        leaf_box = rational_box(cell["exact_box"])
        targets = binding["target_Round294_registry_rows"]
        need(len(targets) == 2, "two registry endpoints")
        local: list[dict[str, Any]] = []
        for sheet_record in by_retained.get(cell["retained_child_row_id"], []):
            partition = sheet_record["partition"]
            frontier = sheet_record["frontier"]
            expected_equation, active_factor = factor_data(
                partition["reason_label"],
                partition["active_endpoint_factor"],
            )
            if (
                frontier["chart"] != binding["source_chart"]
                or disposition["predicate_equation"] != expected_equation
                or sheet_record["base"] != leaf_box[2:6]
            ):
                continue
            need(
                includes(leaf_box, sheet_record["frontier_box"]),
                "six-coordinate frontier containment",
            )
            sheet = sheet_record["sheet"]
            matches = [
                index for index, target in enumerate(targets)
                if target["complete_10_field_return_signature_sha256"]
                == sheet["owner_signature_sha256"]
            ]
            owner_counts[len(matches)] += 1
            need(len(matches) == 1, "unique event-absent endpoint")
            owner_index = matches[0]
            owner = targets[owner_index]
            excluded = targets[1 - owner_index]
            need(
                owner["official_key_id"] == sheet["owner_official_key_id"]
                and excluded["complete_10_field_return_signature_sha256"]
                != sheet["owner_signature_sha256"],
                "owner key and present-side exclusion",
            )
            wanted_nodes.update({
                sheet["wall_sheet_node_id"],
                sheet["owner_wall_bulk_node_id"],
            })
            local.append({
                "binding": binding,
                "disposition": disposition,
                "cell": cell,
                "leaf": leaves[cell["leaf_row_id"]],
                "record": sheet_record,
                "owner": owner,
                "excluded": excluded,
                "active_factor": active_factor,
            })
        multiplicity[len(local)] += 1
        joined.extend(local)
    need(
        len(joined) == 12_992
        and owner_counts == {1: 12_992}
        and multiplicity[0] == 111_052
        and sum(
            count for amount, count in multiplicity.items() if amount
        ) == 472,
        "independent join census",
    )

    closure = closed_result(INPUTS["R266"][0])
    virtual_table = closure[
        "formal_post_Round266_valid_virtual_node_frontier_ledger"
    ]
    virtual_rows = virtual_table["rows"]
    need(
        len(virtual_rows) == virtual_table["row_count"] == 133_284
        and digest(virtual_rows) == virtual_table["rows_sha256"],
        "R266 virtual table",
    )
    virtual = {
        row["valid_virtual_stratum_node_id"]: row
        for row in virtual_rows
        if row["valid_virtual_stratum_node_id"] in wanted_nodes
    }
    need(len(virtual) == len(wanted_nodes), "R266 selected nodes")
    for row in virtual.values():
        verify_row(row, "R266 selected node")

    baseline = read_gzip(HERE / INPUTS["R300C"][0])
    baseline_rows = verify_table(
        baseline, "rows", "row_count", "rows_sha256", "R300C"
    )
    baseline_pairs = {
        tuple(row["canonical_component_edge_endpoint_pair"])
        for row in baseline_rows
    }
    need(len(baseline_pairs) == 6_314, "R300C baseline pair set")

    witnesses: list[dict[str, Any]] = []
    for item in joined:
        binding = item["binding"]
        disposition = item["disposition"]
        cell = item["cell"]
        record = item["record"]
        sheet = record["sheet"]
        partition = record["partition"]
        frontier = record["frontier"]
        bulk = record["bulk"]
        owner = item["owner"]
        excluded = item["excluded"]
        sheet_node = virtual[sheet["wall_sheet_node_id"]]
        bulk_node = virtual[sheet["owner_wall_bulk_node_id"]]
        need(
            sheet_node["post_Round266_quotient_component_id"]
            == bulk_node["post_Round266_quotient_component_id"],
            "sheet/bulk Round266 root",
        )
        root = sheet_node["post_Round266_quotient_component_id"]
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
                digest(item["leaf"]),
            "source_Round235_endpoint_graph_partition_row_id":
                partition["endpoint_graph_partition_row_id"],
            "source_Round235_endpoint_graph_partition_row_sha256":
                digest(partition),
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
                bulk["row_sha256"],
            "source_Round266_sheet_frontier_row_id":
                sheet_node[
                    "post_Round266_valid_virtual_node_frontier_row_id"
                ],
            "source_Round266_sheet_frontier_row_sha256":
                sheet_node["row_sha256"],
            "source_Round266_owner_bulk_frontier_row_id":
                bulk_node[
                    "post_Round266_valid_virtual_node_frontier_row_id"
                ],
            "source_Round266_owner_bulk_frontier_row_sha256":
                bulk_node["row_sha256"],
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
                excluded["registry_occurrence_id"],
            "excluded_present_side_complete_10_field_return_signature_sha256":
                excluded["complete_10_field_return_signature_sha256"],
            "exact_R182_R291_leaf_box": cell["exact_box"],
            "exact_R234_frontier_box": frontier["box"],
            "exact_R248_sheet_base_rectangle":
                sheet["exact_closed_base_rectangle"],
            "predicate_equation": disposition["predicate_equation"],
            "R235_reason_label": partition["reason_label"],
            "active_endpoint_factor": partition["active_endpoint_factor"],
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
        row_id = (
            "round300e-r248-half-open-owner-component-edge-witness:"
            + digest(payload)
        )
        witnesses.append(close({WITNESS_ID: row_id, **payload}))
    witnesses.sort(key=lambda row: row[WITNESS_ID])
    need(
        len(witnesses) == 12_992
        and len({row["source_Round248_wall_sheet_node_id"] for row in witnesses})
        == 12_992,
        "expected witness uniqueness",
    )

    all_edges: list[dict[str, Any]] = []
    for witness in witnesses:
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
                witness["owner_complete_10_field_return_signature_sha256"],
            "source_half_open_owner_witness_row_id": witness[WITNESS_ID],
            "source_half_open_owner_witness_row_sha256":
                witness["row_sha256"],
            "already_present_in_Round300C_positive_volume_edge_ledger":
                tuple(pair) in baseline_pairs,
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
        row_id = (
            "round300e-r248-half-open-owner-component-edge:"
            + digest(payload)
        )
        all_edges.append(close({ALL_EDGE_ID: row_id, **payload}))
    all_edges.sort(key=lambda row: row[ALL_EDGE_ID])
    all_pairs = [
        tuple(row["canonical_component_edge_endpoint_pair"])
        for row in all_edges
    ]
    need(
        len(all_edges) == len(set(all_pairs)) == 12_992,
        "expected all-edge dedupe",
    )

    all_by_pair = {
        tuple(row["canonical_component_edge_endpoint_pair"]): row
        for row in all_edges
    }
    novel_edges: list[dict[str, Any]] = []
    for pair in sorted(set(all_pairs) - baseline_pairs):
        source = all_by_pair[pair]
        payload = {
            "canonical_component_edge_endpoint_pair": list(pair),
            "source_Round300E_all_edge_row_id": source[ALL_EDGE_ID],
            "source_Round300E_all_edge_row_sha256": source["row_sha256"],
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
        row_id = (
            "round300e-r248-half-open-owner-novel-component-edge:"
            + digest(payload)
        )
        novel_edges.append(close({NOVEL_EDGE_ID: row_id, **payload}))
    novel_edges.sort(key=lambda row: row[NOVEL_EDGE_ID])
    overlap_count = sum(
        row["already_present_in_Round300C_positive_volume_edge_ledger"]
        for row in all_edges
    )
    need(
        overlap_count == 472 and len(novel_edges) == 12_520,
        "expected overlap/novel census",
    )

    witness_document = make_ledger(
        WITNESS_SCHEMA, witnesses, WITNESS_ID
    )
    all_edge_document = make_ledger(
        ALL_EDGE_SCHEMA, all_edges, ALL_EDGE_ID
    )
    novel_edge_document = make_ledger(
        NOVEL_EDGE_SCHEMA, novel_edges, NOVEL_EDGE_ID
    )

    def summary(document: dict[str, Any], filename: str) -> dict[str, Any]:
        return {
            "filename": filename,
            "schema": document["schema"],
            "row_count": document["row_count"],
            "row_ids_sha256": document["row_ids_sha256"],
            "row_hashes_sha256": document["row_hashes_sha256"],
            "rows_sha256": document["rows_sha256"],
        }

    result_payload = {
        "schema": SCHEMA,
        "status":
            "PASS_R300E_R248_HALF_OPEN_OWNER_COMPONENT_EDGE_PROMOTION__"
            "12992_ALL__472_R300C_OVERLAP__12520_NOVEL",
        "producer_file_sha256": PRODUCER_SHA256,
        "input_file_pins": {
            filename: expected for filename, expected in INPUTS.values()
        },
        "source_audit": {
            "R295A_two_sided_graph_sheet_binding_count": 111_524,
            "binding_with_R248_sheet_subset_count": 472,
            "binding_without_R248_sheet_subset_count": 111_052,
            "R248_matched_sheet_count": 12_992,
            "distinct_R248_matched_sheet_count": 12_992,
            "binding_matched_sheet_multiplicity_histogram": {
                str(key): value for key, value in sorted(multiplicity.items())
            },
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
        "witness_ledger": summary(witness_document, WITNESS_LEDGER.name),
        "all_edge_ledger": summary(all_edge_document, ALL_EDGE_LEDGER.name),
        "novel_edge_ledger": summary(novel_edge_document, NOVEL_EDGE_LEDGER.name),
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
    expected_result = dict(result_payload)
    expected_result["result_sha256"] = digest(result_payload)
    need(expected_result["result_sha256"] == RESULT_SELF_SHA256, "result pin")
    return (
        witness_document,
        all_edge_document,
        novel_edge_document,
        expected_result,
        baseline_pairs,
    )


def validate_ledger_shape(
    document: dict[str, Any],
    schema: str,
    count: int,
    id_field: str,
) -> None:
    need(
        type(document) is dict
        and document["schema"] == schema
        and document["status"] == "PASS"
        and document["row_count"] == count
        and document["every_row_closed_by_own_SHA256"] is True
        and len(document["rows"]) == count,
        schema + ":shape",
    )
    ids: list[str] = []
    hashes: list[str] = []
    for row in document["rows"]:
        verify_row(row, schema)
        ids.append(row[id_field])
        hashes.append(row["row_sha256"])
    need(
        ids == sorted(ids)
        and len(ids) == len(set(ids))
        and document["row_ids_sha256"] == digest(ids)
        and document["row_hashes_sha256"] == digest(hashes)
        and document["rows_sha256"] == digest(document["rows"]),
        schema + ":inventory closure",
    )


ZERO_EDGE_FIELDS = (
    "formal_occurrence_identity_collapse_credit",
    "formal_component_union_application_credit",
    "formal_DSU_rank_reduction_credit",
    "formal_quotient_credit",
    "formal_maximality_credit",
    "formal_fibre_credit",
    "formal_global_disposition_credit",
)


def validate_semantics(
    witness_document: dict[str, Any],
    all_edge_document: dict[str, Any],
    novel_edge_document: dict[str, Any],
    result: dict[str, Any],
    baseline_pairs: set[tuple[str, str]],
) -> None:
    validate_ledger_shape(
        witness_document, WITNESS_SCHEMA, 12_992, WITNESS_ID
    )
    validate_ledger_shape(
        all_edge_document, ALL_EDGE_SCHEMA, 12_992, ALL_EDGE_ID
    )
    validate_ledger_shape(
        novel_edge_document, NOVEL_EDGE_SCHEMA, 12_520, NOVEL_EDGE_ID
    )
    witnesses = {row[WITNESS_ID]: row for row in witness_document["rows"]}
    all_edges = {row[ALL_EDGE_ID]: row for row in all_edge_document["rows"]}
    witness_refs: list[str] = []
    all_pairs: set[tuple[str, str]] = set()
    for row in witness_document["rows"]:
        payload = {
            key: value for key, value in row.items()
            if key not in {WITNESS_ID, "row_sha256"}
        }
        need(
            row[WITNESS_ID]
            == "round300e-r248-half-open-owner-component-edge-witness:"
            + digest(payload),
            "witness content ID",
        )
        leaf = rational_box(row["exact_R182_R291_leaf_box"])
        frontier = rational_box(row["exact_R234_frontier_box"])
        base = rational_box(row["exact_R248_sheet_base_rectangle"])
        equation, factor = factor_data(
            row["R235_reason_label"], row["active_endpoint_factor"]
        )
        need(
            base == leaf[2:6]
            and frontier[2:6] == base
            and includes(leaf, frontier)
            and row["predicate_equation"] == equation
            and row["active_equation_factor"] == factor,
            "witness exact geometry/equation",
        )
        need(
            row["owner_Round294_registry_occurrence_id"]
            != row["excluded_present_side_Round294_registry_occurrence_id"]
            and row["owner_complete_10_field_return_signature_sha256"]
            != row[
                "excluded_present_side_complete_10_field_return_signature_sha256"
            ]
            and all(
                row[field] is True for field in (
                    "proof_exact_base_equality",
                    "proof_full_six_coordinate_box_containment",
                    "proof_active_factor_identity",
                    "proof_unique_event_absent_owner_signature",
                    "proof_owner_key_identity",
                    "proof_sheet_and_owner_bulk_same_Round266_root",
                )
            ),
            "witness unique owner proof",
        )
        need(
            row["half_open_owner_rule"]
            == "EVENT_ABSENT_BECAUSE_ENDPOINT_EVENT_TIME_IS_OUTSIDE_OPEN_0_1"
            and row["formal_half_open_owner_component_edge_witness_credit"] == 1
            and row["eligible_for_component_DSU_application"] is True
            and row["present_side_component_edge_credit"] == 0
            and row["mere_two_sided_incidence_component_edge_credit"] == 0
            and all(row[field] == 0 for field in ZERO_EDGE_FIELDS),
            "witness credit boundary",
        )
    for row in all_edge_document["rows"]:
        payload = {
            key: value for key, value in row.items()
            if key not in {ALL_EDGE_ID, "row_sha256"}
        }
        need(
            row[ALL_EDGE_ID]
            == "round300e-r248-half-open-owner-component-edge:"
            + digest(payload),
            "all-edge content ID",
        )
        witness = witnesses[row["source_half_open_owner_witness_row_id"]]
        pair = tuple(row["canonical_component_edge_endpoint_pair"])
        expected_pair = tuple(sorted([
            witness["post_Round266_quotient_component_id"],
            witness["owner_Round294_registry_occurrence_id"],
        ]))
        need(
            pair == expected_pair
            and row["source_half_open_owner_witness_row_sha256"]
            == witness["row_sha256"]
            and row["post_Round266_quotient_component_id"]
            == witness["post_Round266_quotient_component_id"]
            and row["owner_Round294_registry_occurrence_id"]
            == witness["owner_Round294_registry_occurrence_id"]
            and row["complete_10_field_return_signature_sha256"]
            == witness["owner_complete_10_field_return_signature_sha256"]
            and row["official_key_id"] == witness["owner_official_key_id"]
            and row["official_key_ordinal"]
            == witness["owner_official_key_ordinal"],
            "all-edge witness join",
        )
        need(
            row["already_present_in_Round300C_positive_volume_edge_ledger"]
            is (pair in baseline_pairs)
            and row["edge_semantics"]
            == "R248_EVENT_ABSENT_HALF_OPEN_OWNER_TO_ROUND266_ROOT__"
            "COMPONENT_CONNECTIVITY_NOT_OCCURRENCE_IDENTITY"
            and row["formal_half_open_owner_component_edge_credit"] == 1
            and row["eligible_for_component_DSU_application"] is True
            and row["present_side_component_edge_credit"] == 0
            and row["mere_two_sided_incidence_component_edge_credit"] == 0
            and all(row[field] == 0 for field in ZERO_EDGE_FIELDS),
            "all-edge credit boundary",
        )
        witness_refs.append(row["source_half_open_owner_witness_row_id"])
        need(pair not in all_pairs, "duplicate all-edge pair")
        all_pairs.add(pair)
    need(
        sorted(witness_refs) == sorted(witnesses)
        and len(all_pairs & baseline_pairs) == 472,
        "all-edge witness exhaustion/overlap",
    )
    novel_pairs: set[tuple[str, str]] = set()
    for row in novel_edge_document["rows"]:
        payload = {
            key: value for key, value in row.items()
            if key not in {NOVEL_EDGE_ID, "row_sha256"}
        }
        need(
            row[NOVEL_EDGE_ID]
            == "round300e-r248-half-open-owner-novel-component-edge:"
            + digest(payload),
            "novel-edge content ID",
        )
        source = all_edges[row["source_Round300E_all_edge_row_id"]]
        pair = tuple(row["canonical_component_edge_endpoint_pair"])
        need(
            pair == tuple(source["canonical_component_edge_endpoint_pair"])
            and row["source_Round300E_all_edge_row_sha256"]
            == source["row_sha256"]
            and pair not in baseline_pairs
            and row[
                "absence_from_Round300C_edge_ledger_proved_by_complete_pair_set"
            ] is True
            and row["formal_novel_component_edge_credit"] == 1
            and row["eligible_for_component_DSU_application"] is True
            and all(
                row[field] == 0 for field in (
                    "formal_component_union_application_credit",
                    "formal_DSU_rank_reduction_credit",
                    "formal_quotient_credit",
                    "formal_maximality_credit",
                    "formal_fibre_credit",
                    "formal_global_disposition_credit",
                )
            ),
            "novel-edge semantics",
        )
        need(pair not in novel_pairs, "duplicate novel pair")
        novel_pairs.add(pair)
    need(
        novel_pairs == all_pairs - baseline_pairs
        and len(novel_pairs) == 12_520,
        "complete novel set difference",
    )

    payload = dict(result)
    claimed = payload.pop("result_sha256", None)
    need(claimed == digest(payload) == RESULT_SELF_SHA256, "result closure")
    need(
        result["schema"] == SCHEMA
        and result["producer_file_sha256"] == PRODUCER_SHA256
        and result["source_audit"]["present_side_promoted_count"] == 0
        and result["edge_audit"]
        == {
            "all_canonical_half_open_owner_edge_count": 12_992,
            "duplicate_canonical_pair_count": 0,
            "already_in_Round300C_edge_count": 472,
            "novel_against_Round300C_edge_count": 12_520,
        }
        and result["strict_nonpromotion"]
        == {
            "occurrence_identity_collapse_credit": 0,
            "component_union_application_credit": 0,
            "DSU_rank_reduction_credit": 0,
            "quotient_credit": 0,
            "maximality_credit": 0,
            "fibre_credit": 0,
            "global_disposition_credit": 0,
            "post_Round300E_quotient_component_count": None,
        },
        "result exact credit boundary",
    )


def compare_exact(
    actual: tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]],
    expected: tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]],
) -> None:
    labels = ("witness", "all edge", "novel edge", "result")
    for label, actual_object, expected_object in zip(
        labels, actual, expected, strict=True
    ):
        need(actual_object == expected_object, "independent expected " + label)


def reclose_ledger(document: dict[str, Any], id_field: str) -> None:
    rows = document["rows"]
    for row in rows:
        body = dict(row)
        body.pop("row_sha256", None)
        row["row_sha256"] = digest(body)
    rows.sort(key=lambda row: row[id_field])
    document["row_count"] = len(rows)
    document["row_ids_sha256"] = digest([row[id_field] for row in rows])
    document["row_hashes_sha256"] = digest(
        [row["row_sha256"] for row in rows]
    )
    document["rows_sha256"] = digest(rows)


def reclose_result(
    result: dict[str, Any],
    witness: dict[str, Any],
    all_edges: dict[str, Any],
    novel: dict[str, Any],
) -> None:
    for field, document in (
        ("witness_ledger", witness),
        ("all_edge_ledger", all_edges),
        ("novel_edge_ledger", novel),
    ):
        result[field].update({
            "row_count": document["row_count"],
            "row_ids_sha256": document["row_ids_sha256"],
            "row_hashes_sha256": document["row_hashes_sha256"],
            "rows_sha256": document["rows_sha256"],
        })
    payload = dict(result)
    payload.pop("result_sha256", None)
    result["result_sha256"] = digest(payload)


def attack_suite(
    expected_witness: dict[str, Any],
    expected_all: dict[str, Any],
    expected_novel: dict[str, Any],
    expected_result: dict[str, Any],
    baseline_pairs: set[tuple[str, str]],
) -> dict[str, Any]:
    attacks: list[dict[str, Any]] = []

    def one_row_attack(
        name: str,
        target: str,
        mutate: Callable[[dict[str, Any]], None],
        expected_rejection: str,
    ) -> None:
        witness = deepcopy(expected_witness)
        all_edges = deepcopy(expected_all)
        novel = deepcopy(expected_novel)
        result = deepcopy(expected_result)
        documents = {
            "witness": (witness, WITNESS_ID),
            "all": (all_edges, ALL_EDGE_ID),
            "novel": (novel, NOVEL_EDGE_ID),
        }
        document, id_field = documents[target]
        mutate(document["rows"][0])
        reclose_ledger(document, id_field)
        reclose_result(result, witness, all_edges, novel)
        rejected = False
        reason = ""
        try:
            validate_semantics(witness, all_edges, novel, result, baseline_pairs)
            compare_exact(
                (witness, all_edges, novel, result),
                (expected_witness, expected_all, expected_novel, expected_result),
            )
        except Exception as exc:
            rejected = True
            reason = str(exc)
        need(rejected, "attack accepted:" + name)
        attacks.append({
            "attack_id": name,
            "attack_class": "FULLY_ROW_TABLE_RESULT_RECOMMITTED_SEMANTIC",
            "expected_rejection": expected_rejection,
            "actual_rejection": reason,
            "rejected": True,
        })

    witness_attacks: list[
        tuple[str, Callable[[dict[str, Any]], None], str]
    ] = [
        (
            "W01_PRESENT_SIDE_OCCURRENCE_SUBSTITUTION",
            lambda row: row.__setitem__(
                "owner_Round294_registry_occurrence_id",
                row["excluded_present_side_Round294_registry_occurrence_id"],
            ),
            "owner endpoint differs from independently rebuilt half-open owner",
        ),
        (
            "W02_PRESENT_SIDE_SIGNATURE_SUBSTITUTION",
            lambda row: row.__setitem__(
                "owner_complete_10_field_return_signature_sha256",
                row[
                    "excluded_present_side_complete_10_field_return_signature_sha256"
                ],
            ),
            "event-absent owner signature mismatch",
        ),
        (
            "W03_AMBIGUOUS_OWNER_SIGNATURE",
            lambda row: row.__setitem__(
                "excluded_present_side_complete_10_field_return_signature_sha256",
                row["owner_complete_10_field_return_signature_sha256"],
            ),
            "owner signature must be unique among two endpoints",
        ),
        (
            "W04_FALSE_FULL_BOX_CONTAINMENT",
            lambda row: row.__setitem__(
                "proof_full_six_coordinate_box_containment", False
            ),
            "full containment proof required",
        ),
        (
            "W05_SHIFTED_SHEET_BASE",
            lambda row: row["exact_R248_sheet_base_rectangle"].__setitem__(
                0, "999"
            ),
            "sheet base must equal leaf base",
        ),
        (
            "W06_WRONG_PREDICATE_EQUATION",
            lambda row: row.__setitem__("predicate_equation", "forged=0"),
            "active-factor equation identity",
        ),
        (
            "W07_WRONG_ACTIVE_FACTOR",
            lambda row: row.__setitem__(
                "active_equation_factor", "present_side_factor"
            ),
            "active factor identity",
        ),
        (
            "W08_PRESENT_SIDE_EDGE_CREDIT",
            lambda row: row.__setitem__("present_side_component_edge_credit", 1),
            "present side receives zero credit",
        ),
        (
            "W09_MERE_INCIDENCE_EDGE_CREDIT",
            lambda row: row.__setitem__(
                "mere_two_sided_incidence_component_edge_credit", 1
            ),
            "mere incidence is not connectivity",
        ),
        (
            "W10_OCCURRENCE_IDENTITY_COLLAPSE",
            lambda row: row.__setitem__(
                "formal_occurrence_identity_collapse_credit", 1
            ),
            "connectivity is not identity",
        ),
        (
            "W11_COMPONENT_UNION_APPLICATION",
            lambda row: row.__setitem__(
                "formal_component_union_application_credit", 1
            ),
            "DSU not applied in this round",
        ),
        (
            "W12_DSU_RANK_CREDIT",
            lambda row: row.__setitem__(
                "formal_DSU_rank_reduction_credit", 1
            ),
            "rank not computed",
        ),
        (
            "W13_QUOTIENT_CREDIT",
            lambda row: row.__setitem__("formal_quotient_credit", 1),
            "quotient not rebuilt",
        ),
        (
            "W14_MAXIMALITY_CREDIT",
            lambda row: row.__setitem__("formal_maximality_credit", 1),
            "maximality downstream",
        ),
        (
            "W15_FIBRE_CREDIT",
            lambda row: row.__setitem__("formal_fibre_credit", 1),
            "fibre exhaustion downstream",
        ),
        (
            "W16_GLOBAL_DISPOSITION_CREDIT",
            lambda row: row.__setitem__(
                "formal_global_disposition_credit", 1
            ),
            "global dispositions downstream",
        ),
        (
            "W17_DSU_ELIGIBILITY_REMOVED",
            lambda row: row.__setitem__(
                "eligible_for_component_DSU_application", False
            ),
            "legal edge eligibility is exact",
        ),
        (
            "W18_ROUND266_ROOT_SUBSTITUTION",
            lambda row: row.__setitem__(
                "post_Round266_quotient_component_id",
                "round266-curved-face-component:" + "0" * 64,
            ),
            "sheet and owner root lineage",
        ),
        (
            "W19_OWNER_KEY_SUBSTITUTION",
            lambda row: row.__setitem__(
                "owner_official_key_id", "gate5-word:forged"
            ),
            "owner key identity",
        ),
        (
            "W20_HALF_OPEN_RULE_SUBSTITUTION",
            lambda row: row.__setitem__(
                "half_open_owner_rule", "BOTH_SIDES"
            ),
            "event-absent half-open rule",
        ),
    ]
    for name, mutation, reason in witness_attacks:
        one_row_attack(name, "witness", mutation, reason)

    edge_attacks = [
        (
            "E01_CANONICAL_PAIR_SUBSTITUTION",
            lambda row: row["canonical_component_edge_endpoint_pair"].__setitem__(
                1, "source-g-expanded-occurrence:" + "f" * 64
            ),
            "edge pair must equal owner witness endpoints",
        ),
        (
            "E02_R300C_OVERLAP_FLAG_FLIP",
            lambda row: row.__setitem__(
                "already_present_in_Round300C_positive_volume_edge_ledger",
                not row[
                    "already_present_in_Round300C_positive_volume_edge_ledger"
                ],
            ),
            "complete R300C pair set decides overlap",
        ),
        (
            "E03_EDGE_IDENTITY_CLAIM",
            lambda row: row.__setitem__(
                "formal_occurrence_identity_collapse_credit", 1
            ),
            "edge is connectivity not identity",
        ),
        (
            "E04_EDGE_DSU_RANK_CLAIM",
            lambda row: row.__setitem__(
                "formal_DSU_rank_reduction_credit", 1
            ),
            "edge inventory does not apply DSU",
        ),
        (
            "E05_EDGE_MAXIMALITY_CLAIM",
            lambda row: row.__setitem__("formal_maximality_credit", 1),
            "maximality downstream",
        ),
        (
            "E06_EDGE_SEMANTICS_FORGERY",
            lambda row: row.__setitem__(
                "edge_semantics", "BOTH_ENDPOINTS_ARE_IDENTICAL"
            ),
            "narrow connectivity semantics",
        ),
    ]
    for name, mutation, reason in edge_attacks:
        one_row_attack(name, "all", mutation, reason)

    novel_attacks = [
        (
            "N01_NOVEL_CREDIT_REMOVED",
            lambda row: row.__setitem__("formal_novel_component_edge_credit", 0),
            "novel row exact credit",
        ),
        (
            "N02_NOVEL_DSU_RANK_CLAIM",
            lambda row: row.__setitem__(
                "formal_DSU_rank_reduction_credit", 1
            ),
            "novel inventory does not apply DSU",
        ),
        (
            "N03_ABSENCE_PROOF_REMOVED",
            lambda row: row.__setitem__(
                "absence_from_Round300C_edge_ledger_proved_by_complete_pair_set",
                False,
            ),
            "complete set-difference proof required",
        ),
    ]
    for name, mutation, reason in novel_attacks:
        one_row_attack(name, "novel", mutation, reason)

    result_mutations = [
        (
            "R01_EDGE_COUNT_FORGERY",
            lambda value: value["edge_audit"].__setitem__(
                "all_canonical_half_open_owner_edge_count", 12_993
            ),
            "exact edge census",
        ),
        (
            "R02_POST_QUOTIENT_FORGERY",
            lambda value: value["strict_nonpromotion"].__setitem__(
                "post_Round300E_quotient_component_count", 1
            ),
            "quotient not rebuilt",
        ),
        (
            "R03_PRESENT_SIDE_SCOPE_FORGERY",
            lambda value: value["scope_contract"].__setitem__(
                "present_side_is_never_promoted", False
            ),
            "present side exclusion",
        ),
    ]
    for name, mutation, reason in result_mutations:
        result = deepcopy(expected_result)
        mutation(result)
        payload = dict(result)
        payload.pop("result_sha256", None)
        result["result_sha256"] = digest(payload)
        rejected = False
        actual = ""
        try:
            validate_semantics(
                expected_witness,
                expected_all,
                expected_novel,
                result,
                baseline_pairs,
            )
            compare_exact(
                (
                    expected_witness,
                    expected_all,
                    expected_novel,
                    result,
                ),
                (
                    expected_witness,
                    expected_all,
                    expected_novel,
                    expected_result,
                ),
            )
        except Exception as exc:
            rejected = True
            actual = str(exc)
        need(rejected, "result attack accepted:" + name)
        attacks.append({
            "attack_id": name,
            "attack_class": "RESULT_RECOMMITTED_SEMANTIC",
            "expected_rejection": reason,
            "actual_rejection": actual,
            "rejected": True,
        })

    lexical_attacks = [
        ("F01_DUPLICATE_JSON_KEY", b'{"a":1,"a":2}', "duplicate JSON key"),
        ("F02_NONFINITE_NAN", b'{"a":NaN}', "nonfinite JSON"),
        ("F03_NUL_JSON", b'{"a":1}\\u0000', "NUL or trailing JSON"),
    ]
    for name, raw, reason in lexical_attacks:
        rejected = False
        actual = ""
        try:
            strict_json_bytes(raw)
        except Exception as exc:
            rejected = True
            actual = str(exc)
        need(rejected, "lexical attack accepted:" + name)
        attacks.append({
            "attack_id": name,
            "attack_class": "LEXICAL_FORMAT",
            "expected_rejection": reason,
            "actual_rejection": actual,
            "rejected": True,
        })

    try:
        gzip.decompress(b"\x1f\x8b\x08\x00")
        truncated_rejected = False
        truncated_reason = ""
    except Exception as exc:
        truncated_rejected = True
        truncated_reason = str(exc)
    need(truncated_rejected, "truncated gzip accepted")
    attacks.append({
        "attack_id": "F04_TRUNCATED_GZIP",
        "attack_class": "MALFORMED_GZIP",
        "expected_rejection": "gzip decode",
        "actual_rejection": truncated_reason,
        "rejected": True,
    })

    semantic_count = sum(
        item["attack_class"].endswith("SEMANTIC") for item in attacks
    )
    return {
        "schema": ATTACK_SCHEMA,
        "status":
            "PASS_ALL_TARGETED_HALF_OPEN_OWNER_ATTACKS_REJECTED",
        "attack_count": len(attacks),
        "semantic_recommitted_attack_count": semantic_count,
        "format_attack_count": len(attacks) - semantic_count,
        "all_attacks_rejected": all(item["rejected"] for item in attacks),
        "attacks": attacks,
    }


def safe_write(items: list[tuple[Path, bytes]]) -> None:
    staged: list[tuple[Path, Path]] = []
    try:
        for path, data in items:
            descriptor, name = tempfile.mkstemp(
                prefix=f".{path.name}.", suffix=".tmp", dir=HERE
            )
            temporary = Path(name)
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            staged.append((temporary, path))
        for temporary, path in staged:
            os.replace(temporary, path)
    finally:
        for temporary, _path in staged:
            if temporary.exists():
                temporary.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()

    expected_witness, expected_all, expected_novel, expected_result, baseline = (
        reconstruct_expected()
    )

    # Producer bytes remain inert: only this hash operation is permitted.
    check_regular(PRODUCER, PRODUCER_SHA256, "producer inert bytes")
    check_regular(WITNESS_LEDGER, WITNESS_FILE_SHA256, "candidate witness")
    check_regular(ALL_EDGE_LEDGER, ALL_EDGE_FILE_SHA256, "candidate all edges")
    check_regular(NOVEL_EDGE_LEDGER, NOVEL_EDGE_FILE_SHA256, "candidate novel")
    check_regular(RESULT, RESULT_FILE_SHA256, "candidate result")

    candidate_witness = read_gzip(WITNESS_LEDGER)
    candidate_all = read_gzip(ALL_EDGE_LEDGER)
    candidate_novel = read_gzip(NOVEL_EDGE_LEDGER)
    candidate_result = read_json(RESULT)
    validate_semantics(
        candidate_witness,
        candidate_all,
        candidate_novel,
        candidate_result,
        baseline,
    )
    compare_exact(
        (
            candidate_witness,
            candidate_all,
            candidate_novel,
            candidate_result,
        ),
        (
            expected_witness,
            expected_all,
            expected_novel,
            expected_result,
        ),
    )
    need(
        gzip_encoding(expected_witness) == WITNESS_LEDGER.read_bytes()
        and gzip_encoding(expected_all) == ALL_EDGE_LEDGER.read_bytes()
        and gzip_encoding(expected_novel) == NOVEL_EDGE_LEDGER.read_bytes()
        and plain_encoding(expected_result) == RESULT.read_bytes(),
        "candidate exact canonical bytes",
    )

    attacks = attack_suite(
        expected_witness,
        expected_all,
        expected_novel,
        expected_result,
        baseline,
    )
    attacks_payload = dict(attacks)
    attacks["attack_suite_sha256"] = digest(attacks_payload)
    attack_data = plain_encoding(attacks)

    verification_payload = {
        "schema": VERIFICATION_SCHEMA,
        "status":
            "PASS_INDEPENDENT_CACHELESS_R300E_HALF_OPEN_OWNER_EDGE__"
            "12992_ALL__472_OVERLAP__12520_NOVEL__ZERO_DSU_RANK_CREDIT",
        "verifier_file_sha256": file_sha256(Path(__file__).resolve()),
        "producer_inert_file_sha256": PRODUCER_SHA256,
        "candidate_file_pins": {
            WITNESS_LEDGER.name: WITNESS_FILE_SHA256,
            ALL_EDGE_LEDGER.name: ALL_EDGE_FILE_SHA256,
            NOVEL_EDGE_LEDGER.name: NOVEL_EDGE_FILE_SHA256,
            RESULT.name: RESULT_FILE_SHA256,
        },
        "independent_reconstruction": {
            "producer_imported": False,
            "producer_executed": False,
            "producer_parsed": False,
            "upstream_input_pin_count": len(INPUTS),
            "R295A_graph_binding_count": 111_524,
            "binding_with_sheet_count": 472,
            "witness_count": 12_992,
            "all_edge_count": 12_992,
            "Round300C_overlap_count": 472,
            "novel_edge_count": 12_520,
            "candidate_objects_equal_independently_rebuilt_objects": True,
            "candidate_bytes_equal_independently_rebuilt_bytes": True,
        },
        "attack_audit": {
            "attack_count": attacks["attack_count"],
            "semantic_recommitted_attack_count":
                attacks["semantic_recommitted_attack_count"],
            "format_attack_count": attacks["format_attack_count"],
            "all_attacks_rejected": attacks["all_attacks_rejected"],
            "attack_suite_sha256": attacks["attack_suite_sha256"],
        },
        "strict_nonpromotion": expected_result["strict_nonpromotion"],
        "hash_seed_independence_replay_required": True,
    }
    verification = dict(verification_payload)
    verification["verification_sha256"] = digest(verification_payload)
    verification_data = plain_encoding(verification)
    if not arguments.no_write:
        safe_write([
            (ATTACKS, attack_data),
            (VERIFICATION, verification_data),
        ])
    print(verification["status"])
    print(json.dumps({
        "attacks": attacks["attack_count"],
        "semantic_attacks": attacks["semantic_recommitted_attack_count"],
        "attack_file_sha256": hashlib.sha256(attack_data).hexdigest(),
        "attack_suite_sha256": attacks["attack_suite_sha256"],
        "verification_file_sha256":
            hashlib.sha256(verification_data).hexdigest(),
        "verification_sha256": verification["verification_sha256"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
