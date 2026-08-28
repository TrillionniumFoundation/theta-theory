#!/usr/bin/env python3
"""Round302-A exact exclusion of the withheld R248 double-endpoint sheets.

Round300-C explicitly withheld every two-dimensional virtual sheet and
Round300-E audited only the 38,328 Round235 single-endpoint sheets.  This
package closes the remaining 32 Round236 double-endpoint sheets.  It
independently reopens their complete source rows and proves that none has an
eligible occurrence attachment through the complete Round291/Round295-A
lower-physical frontier.

The eight Round300-C witnesses on related owner-bulk nodes are preserved as
non-transferable context.  A bulk witness never supplies sheet attachment
credit.  This package performs no DSU union and issues no maximality credit.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import stat
from typing import Any, Iterable, Iterator, TextIO


HERE = Path(__file__).resolve().parent
PREFIX = (
    "cm2_round302a_source_g_r248_double_endpoint_sheet_"
    "attachment_exclusion"
)
LEDGER = PREFIX + "_ledger.json.gz"
RESULT = PREFIX + "_result.json"
SCHEMA = (
    "cm2.round302a.source-g-r248-double-endpoint-sheet-"
    "attachment-exclusion.v1"
)

R234_CERT = (
    "cm2_round234_source_g_wall_endpoint_order_depth6_"
    "materialization_certificate.json"
)
R234_MANIFEST = (
    "cm2_round234_source_g_wall_endpoint_order_depth6_"
    "materialization_manifest.sha256"
)
R236_CERT = (
    "cm2_round236_source_g_wall_residual_closure_and_"
    "root_key_partition_certificate.json"
)
R236_MANIFEST = (
    "cm2_round236_source_g_wall_residual_closure_and_"
    "root_key_partition_manifest.sha256"
)
R248_CERT = (
    "cm2_round248_source_g_wall_finite_key_retained_"
    "quotient_certificate.json"
)
R248_MANIFEST = (
    "cm2_round248_source_g_wall_finite_key_retained_"
    "quotient_manifest.sha256"
)
R266_CERT = (
    "cm2_round266_source_g_expanded_curved_face_closure_certificate.json"
)
R266_MANIFEST = (
    "cm2_round266_source_g_expanded_curved_face_closure_manifest.sha256"
)
R291_LEDGER = (
    "cm2_round291_source_g_complete_lower_stratum_local_"
    "disposition_freeze_ledger.json.gz"
)
R291_MANIFEST = (
    "cm2_round291_source_g_complete_lower_stratum_local_"
    "disposition_freeze_manifest.sha256"
)
R295A_LEDGER = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_"
    "closure_physical_witness_incidence_binding_ledger.json.gz"
)
R295A_MANIFEST = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_"
    "closure_manifest.sha256"
)
R300C_WITNESS = (
    "cm2_round300c_source_g_virtual_stratum_new_occurrence_positive_"
    "volume_edge_promotion_witness_ledger.json.gz"
)
R300C_MANIFEST = (
    "cm2_round300c_source_g_virtual_stratum_new_occurrence_positive_"
    "volume_edge_promotion_manifest.sha256"
)

MANIFEST_PINS = {
    R234_MANIFEST:
        "f8714ecdf804657fc6633136544f567b07e7d8503095d17fcda19226feefc432",
    R236_MANIFEST:
        "28f6f6d2f5b0f10edba5cd473b4126a8fed098874849c2f579eadd92b30d324c",
    R248_MANIFEST:
        "b1ddedd01041e71b5c12fa4989726815c8685e6df77f54d9dbddda64aaf89e07",
    R266_MANIFEST:
        "63fb5b25d52ca5de579256499629d04d15f6a313e0a73f7e80fcb463385cbe09",
    R291_MANIFEST:
        "d655907a45cfb7b47ebdc822d35a0e604fc27fa38547c300139c116d7a2191ce",
    R295A_MANIFEST:
        "b25f11c0090c56d2ad2d3b2cd0b172e7c089f044ae5722eb9e82ae04b129094a",
    R300C_MANIFEST:
        "cd327de2702ac209b0b0a03d09b3744596a901c2d65794dd86231d31a0be3503",
}
FILE_PINS = {
    R234_CERT:
        "6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac",
    R236_CERT:
        "b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217",
    R248_CERT:
        "fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311",
    R266_CERT:
        "2d30be104dc522ebb1664129894acf851180b9e5f51dd8471c33137447b599bf",
    R291_LEDGER:
        "412b616b2cf75ef1373d98086cfcb2eb90a8c544e9f6b4d16a673f6cfeeb57ab",
    R295A_LEDGER:
        "2d9addfc9fca55366a58b29a7084c063674c3f556dd5398b038ae7d51fe97dcf",
    R300C_WITNESS:
        "bbb690ba8236230bb99fa8c2dcf569f97c758d546c1ec56ae6d3f6c9d880c7e2",
}
MANIFEST_MEMBERS = {
    R234_MANIFEST: (R234_CERT, FILE_PINS[R234_CERT]),
    R236_MANIFEST: (R236_CERT, FILE_PINS[R236_CERT]),
    R248_MANIFEST: ("deliverables/" + R248_CERT, FILE_PINS[R248_CERT]),
    R266_MANIFEST: (R266_CERT, FILE_PINS[R266_CERT]),
    R291_MANIFEST: (R291_LEDGER, FILE_PINS[R291_LEDGER]),
    R295A_MANIFEST: (R295A_LEDGER, FILE_PINS[R295A_LEDGER]),
    R300C_MANIFEST: (R300C_WITNESS, FILE_PINS[R300C_WITNESS]),
}

COMMITMENTS = {
    "R248_SHEET": {
        "row_count": 38_360,
        "row_ids_sha256":
            "fbb15ef7122367925c72f9d0e396141d3f04a271b78064af41e1f68d9d06cd61",
        "row_hashes_sha256":
            "be2e8b880f3a0c8fb833a7ba8dce0bd86d5526b400569377f0fcb66692a8c7e0",
        "rows_sha256":
            "e61754dc51732c4c82876d1c2e83fa040747d23253addd64350728169f5ae44b",
    },
    "R266_VIRTUAL": {
        "row_count": 133_284,
        "row_ids_sha256":
            "2d42533f48f864f01e6bd4a46470e7266c1a2cec590380483cfb7cbfb84634f2",
        "row_hashes_sha256":
            "9c31ba929e13eeaea29a9f6abe7cf324222eacb25d123a9b12252b386c12a32e",
        "rows_sha256":
            "8c394c1d1b2b42025c25a00ef24ecba748981ed93c75b9aba20ddf15ff8597d5",
    },
    "R291": {
        "row_count": 55_428,
        "row_ids_sha256":
            "dc1abc74dde77cf7d114cacbd942a55527d90cf722efc6c679de58beffe8d11e",
        "row_hashes_sha256":
            "3c47783f6e00c7c0aa3c1ee577f31ba6ca37a4a73ddea420e1211705fc8576fa",
        "rows_sha256":
            "a347c5423b857d4b8aeaae6f48e5d2f6ef81caf15a9329ff0909df77258a4279",
    },
    "R295A": {
        "row_count": 113_452,
        "row_ids_sha256":
            "a0f471c84148d57eba4511efd8b343eb152c9378a24e018b9f0be10e41525805",
        "row_hashes_sha256":
            "7eab57334f6f5170ffaef60316250078cd6774cdabdb7279d3585267345e5258",
        "rows_sha256":
            "e8b00ffa431d7609d97e7e3cae00f656d2386643acc22d49bdc4a018ed295946",
    },
    "R300C": {
        "row_count": 6_322,
        "row_ids_sha256":
            "54147f135d32ab8326d2bee9d75994086cb7e137dd3350d75a9a2663d56699b6",
        "row_hashes_sha256":
            "b1c09d20d57ff7f4fee44a0f915929be5810fcbdc6d3014e66467a6e747f5800",
        "rows_sha256":
            "849b2b8d51571c2be4280354b7b260d8d9f52e2793ae08cd393d1dcf9e97e5b2",
    },
}


class GateError(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise GateError(label)


ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
)


def pieces(value: Any) -> Iterable[bytes]:
    for token in ENCODER.iterencode(value):
        yield token.encode("utf-8")


def canonical(value: Any) -> bytes:
    return b"".join(pieces(value))


def digest(value: Any) -> str:
    state = hashlib.sha256()
    for token in pieces(value):
        state.update(token)
    return state.hexdigest()


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def safe_file(path: Path, maximum: int = 3_000_000_000) -> None:
    need(path.parent.resolve() == HERE.resolve(), "HERE-only input")
    info = os.lstat(path)
    need(
        stat.S_ISREG(info.st_mode)
        and not path.is_symlink()
        and info.st_nlink == 1
        and 0 < info.st_size <= maximum,
        "single-link regular bounded input:" + path.name,
    )


def parse_manifest(name: str) -> dict[str, str]:
    path = HERE / name
    safe_file(path, 300_000)
    entries: dict[str, str] = {}
    for line in path.read_text(encoding="ascii").splitlines():
        if not line:
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\n]+)", line)
        need(match is not None, "manifest syntax:" + name)
        pin, member = match.groups()
        need(member not in entries, "unique manifest member:" + name)
        entries[member] = pin
    need(bool(entries), "nonempty manifest:" + name)
    return entries


def validate_input_boundary() -> None:
    for manifest, pin in MANIFEST_PINS.items():
        safe_file(HERE / manifest)
        need(file_sha256(HERE / manifest) == pin, "manifest pin:" + manifest)
        entries = parse_manifest(manifest)
        member, member_pin = MANIFEST_MEMBERS[manifest]
        need(entries.get(member) == member_pin, "manifest member:" + member)
    for name, pin in FILE_PINS.items():
        safe_file(HERE / name)
        need(file_sha256(HERE / name) == pin, "file pin:" + name)


def validate_row(row: dict[str, Any], label: str) -> None:
    payload = dict(row)
    claimed = payload.pop("row_sha256", None)
    need(
        isinstance(claimed, str) and digest(payload) == claimed,
        "row closure:" + label,
    )


class ListHash:
    def __init__(self) -> None:
        self.state = hashlib.sha256(b"[")
        self.count = 0

    def add(self, value: Any) -> None:
        if self.count:
            self.state.update(b",")
        for token in pieces(value):
            self.state.update(token)
        self.count += 1

    def finish(self) -> str:
        state = self.state.copy()
        state.update(b"]")
        return state.hexdigest()


def iter_array(
    stream: TextIO,
    *,
    marker: str,
    nested_table: bool,
) -> Iterator[dict[str, Any]]:
    buffer = ""
    while marker not in buffer:
        block = stream.read(1 << 20)
        need(bool(block), "missing streamed marker:" + marker)
        buffer = (buffer + block)[-(len(marker) + (2 << 20)) :]
    buffer = buffer.split(marker, 1)[1]
    if nested_table:
        while '"rows":[' not in buffer:
            block = stream.read(1 << 20)
            need(bool(block), "missing nested rows:" + marker)
            buffer += block
        buffer = buffer.split('"rows":[', 1)[1]

    decoder = json.JSONDecoder(
        parse_float=lambda token: (_ for _ in ()).throw(
            GateError("stream float:" + token)
        ),
        parse_constant=lambda token: (_ for _ in ()).throw(
            GateError("stream constant:" + token)
        ),
    )
    while True:
        buffer = buffer.lstrip()
        if not buffer:
            block = stream.read(1 << 20)
            need(bool(block), "truncated streamed array")
            buffer = block
            continue
        if buffer[0] == ",":
            buffer = buffer[1:]
            continue
        if buffer[0] == "]":
            return
        while True:
            try:
                row, end = decoder.raw_decode(buffer)
                break
            except json.JSONDecodeError:
                block = stream.read(1 << 20)
                need(bool(block), "truncated streamed row")
                buffer += block
        need(type(row) is dict, "streamed row object")
        yield row
        buffer = buffer[end:]


def validated_rows(
    name: str,
    id_field: str,
    commitment: dict[str, Any],
    *,
    table: str | None = None,
) -> Iterator[dict[str, Any]]:
    rows = ListHash()
    ids = ListHash()
    hashes = ListHash()
    seen: set[str] = set()
    opener = (
        (lambda: gzip.open(HERE / name, "rt", encoding="utf-8"))
        if name.endswith(".gz")
        else (lambda: (HERE / name).open("rt", encoding="utf-8"))
    )
    with opener() as stream:
        marker = f'"{table}":' if table else '"rows":['
        for row in iter_array(
            stream,
            marker=marker,
            nested_table=table is not None,
        ):
            validate_row(row, name)
            row_id = row[id_field]
            need(
                isinstance(row_id, str) and row_id not in seen,
                "unique row ID:" + name,
            )
            seen.add(row_id)
            rows.add(row)
            ids.add(row_id)
            hashes.add(row["row_sha256"])
            yield row
    need(
        {
            "row_count": rows.count,
            "row_ids_sha256": ids.finish(),
            "row_hashes_sha256": hashes.finish(),
            "rows_sha256": rows.finish(),
        } == commitment,
        "complete table commitment:" + name,
    )


def load_closed_result(name: str) -> dict[str, Any]:
    safe_file(HERE / name)
    document = json.loads((HERE / name).read_text(encoding="utf-8"))
    need(type(document) is dict and type(document.get("result")) is dict,
         "closed result wrapper:" + name)
    need(
        document.get("result_sha256") == digest(document["result"]),
        "closed result self digest:" + name,
    )
    return document["result"]


def relation(
    sheet_rectangle: list[str],
    cell_rectangle: list[str],
) -> str:
    sheet = [Fraction(value) for value in sheet_rectangle]
    cell = [Fraction(value) for value in cell_rectangle]
    overlap_p = min(sheet[1], cell[1]) - max(sheet[0], cell[0])
    overlap_s = min(sheet[3], cell[3]) - max(sheet[2], cell[2])
    if sheet == cell:
        return "EXACT_EQUAL"
    if overlap_p > 0 and overlap_s > 0:
        return "STRICT_POSITIVE_AREA_INTERSECTION"
    if overlap_p >= 0 and overlap_s >= 0:
        return "CLOSED_BOUNDARY_CONTACT_ONLY"
    return "DISJOINT"


def close_row(payload: dict[str, Any]) -> dict[str, Any]:
    row = dict(payload)
    need("row_sha256" not in row, "fresh row")
    row["row_sha256"] = digest(payload)
    return row


def reconstruct() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    validate_input_boundary()

    r236 = load_closed_result(R236_CERT)
    double_list = r236["double_endpoint_partition_rows"]
    need(
        len(double_list) == 16
        and digest(double_list)
        == "68f41212de0da7f3468a321a682978daa052cb65a611d756a901ca095bcc0bf6",
        "complete R236 double partition list",
    )
    doubles = {
        row["double_endpoint_partition_row_id"]: row
        for row in double_list
    }
    need(len(doubles) == 16, "unique R236 double partitions")

    r234 = load_closed_result(R234_CERT)
    frontier_rows = r234["depth6_frontier_rows"]
    need(
        len(frontier_rows) == 38_376
        and digest(frontier_rows)
        == "a1b3bf193ad10045f52244c3e40c52f78e0aeacffa3ba52c262bc8912fc9b5a6",
        "complete R234 frontier list",
    )
    wanted_frontiers = {
        row["Round234_frontier_row_id"] for row in double_list
    }
    frontiers = {
        row["frontier_row_id"]: row
        for row in frontier_rows
        if row["frontier_row_id"] in wanted_frontiers
    }
    need(len(frontiers) == 16, "complete R234/R236 join")

    selected_sheets: list[dict[str, Any]] = []
    source_histogram: Counter[str] = Counter()
    for sheet in validated_rows(
        R248_CERT,
        "wall_sheet_node_id",
        COMMITMENTS["R248_SHEET"],
        table="formal_wall_half_open_sheet_owner_ledger",
    ):
        source_histogram[sheet["source_partition_kind"]] += 1
        if (
            sheet["source_partition_kind"]
            == "ROUND236_DOUBLE_ENDPOINT_GRAPH_SHEET"
        ):
            selected_sheets.append(sheet)
    need(
        source_histogram
        == {
            "ROUND235_SINGLE_ENDPOINT_GRAPH_SHEET": 38_328,
            "ROUND236_DOUBLE_ENDPOINT_GRAPH_SHEET": 32,
        }
        and len(selected_sheets) == 32,
        "complete R248 sheet-kind partition",
    )

    sheets_by_id: dict[str, dict[str, Any]] = {}
    by_lineage: dict[tuple[str, str], list[str]] = defaultdict(list)
    partition_factor_histogram: Counter[int] = Counter()
    by_partition: dict[str, set[str]] = defaultdict(set)
    for sheet in selected_sheets:
        source = doubles[sheet["source_partition_row_id"]]
        frontier = frontiers[source["Round234_frontier_row_id"]]
        need(
            sheet["Round220_split_interface_id"]
            == source["Round220_split_interface_id"]
            == frontier["Round220_split_interface_id"],
            "R248/R236/R234 interface lineage",
        )
        need(
            sheet["endpoint_factor"] in {"source", "target"}
            and sheet["owner_signature_sha256"]
            == digest(source["same_sign_event_absent_signature"])
            and sheet["owner_official_key_id"]
            == source["same_sign_event_absent_signature"][
                "official_key_id"
            ],
            "double sheet exact owner policy",
        )
        need(
            sheet["exact_closed_base_rectangle"]
            == frontier["box"][2:6]
            and Fraction(sheet["exact_positive_2D_sheet_area"]) > 0
            and sheet["sheet_three_dimensional_coordinate_volume"] == "0"
            and sheet["half_open_owner_rule"]
            == (
                "EVENT_ABSENT_BECAUSE_ENDPOINT_EVENT_TIME_IS_"
                "OUTSIDE_OPEN_0_1"
            ),
            "double sheet exact 2D geometry",
        )
        sheet_id = sheet["wall_sheet_node_id"]
        need(sheet_id not in sheets_by_id, "unique selected sheet")
        sheets_by_id[sheet_id] = {
            "sheet": sheet,
            "source": source,
            "frontier": frontier,
        }
        by_lineage[
            (
                frontier["Round179_retained_child_row_id"],
                frontier["chart"],
            )
        ].append(sheet_id)
        by_partition[source["double_endpoint_partition_row_id"]].add(
            sheet["endpoint_factor"]
        )
    for factors in by_partition.values():
        partition_factor_histogram[len(factors)] += 1
        need(factors == {"source", "target"}, "two endpoint factors")
    need(
        len(sheets_by_id) == 32
        and len(by_partition) == 16
        and partition_factor_histogram == {2: 16},
        "32 sheet / 16 partition exact factor census",
    )

    selected_node_ids = set(sheets_by_id)
    selected_node_ids.update(
        item["sheet"]["owner_wall_bulk_node_id"]
        for item in sheets_by_id.values()
    )
    virtual: dict[str, dict[str, Any]] = {}
    for row in validated_rows(
        R266_CERT,
        "post_Round266_valid_virtual_node_frontier_row_id",
        COMMITMENTS["R266_VIRTUAL"],
        table="formal_post_Round266_valid_virtual_node_frontier_ledger",
    ):
        node_id = row["valid_virtual_stratum_node_id"]
        if node_id in selected_node_ids:
            virtual[node_id] = row
    need(len(virtual) == 48, "32 sheet + 16 bulk virtual join")
    for sheet_id, item in sheets_by_id.items():
        sheet = item["sheet"]
        sheet_virtual = virtual[sheet_id]
        bulk_virtual = virtual[sheet["owner_wall_bulk_node_id"]]
        need(
            sheet_virtual["virtual_node_kind"] == "ROUND248_WALL_SHEET"
            and bulk_virtual["virtual_node_kind"] == "ROUND248_WALL_BULK"
            and sheet_virtual["post_Round266_quotient_component_id"]
            == bulk_virtual["post_Round266_quotient_component_id"],
            "pinned internal sheet-owner base component",
        )
        item["sheet_virtual"] = sheet_virtual
        item["bulk_virtual"] = bulk_virtual

    lineage_counts: Counter[str] = Counter()
    positive_counts: Counter[str] = Counter()
    closed_counts: Counter[str] = Counter()
    relation_histogram: Counter[str] = Counter()
    positive_R291_keys: set[tuple[str, int]] = set()
    for disposition in validated_rows(
        R291_LEDGER,
        "complete_lower_stratum_local_disposition_row_id",
        COMMITMENTS["R291"],
    ):
        disposition_id = disposition[
            "complete_lower_stratum_local_disposition_row_id"
        ]
        for index, cell in enumerate(disposition["physical_witness_cells"]):
            box = cell.get("exact_box")
            if not isinstance(box, list) or len(box) != 6:
                continue
            sheet_ids = by_lineage.get(
                (
                    cell["retained_child_row_id"],
                    disposition["source_chart"],
                ),
                [],
            )
            for sheet_id in sheet_ids:
                lineage_counts[sheet_id] += 1
                value = relation(
                    sheets_by_id[sheet_id]["sheet"][
                        "exact_closed_base_rectangle"
                    ],
                    box[2:6],
                )
                relation_histogram[value] += 1
                if value in {
                    "EXACT_EQUAL",
                    "STRICT_POSITIVE_AREA_INTERSECTION",
                }:
                    positive_counts[sheet_id] += 1
                    positive_R291_keys.add((disposition_id, index))
                elif value == "CLOSED_BOUNDARY_CONTACT_ONLY":
                    closed_counts[sheet_id] += 1
    need(
        not lineage_counts
        and not positive_counts
        and not closed_counts
        and not relation_histogram
        and not positive_R291_keys,
        "zero R291 same-lineage sheet candidates",
    )

    binding_candidate_count = 0
    for row in validated_rows(
        R295A_LEDGER,
        "Round295A_R291_physical_incidence_binding_row_id",
        COMMITMENTS["R295A"],
    ):
        if (
            row["Round291_local_disposition_row_id"],
            row["physical_witness_cell_index"],
        ) in positive_R291_keys:
            binding_candidate_count += 1
    need(binding_candidate_count == 0, "zero R295A occurrence candidates")

    direct_witnesses: dict[str, list[dict[str, Any]]] = defaultdict(list)
    bulk_witnesses: dict[str, list[dict[str, Any]]] = defaultdict(list)
    owner_bulk_ids = {
        item["sheet"]["owner_wall_bulk_node_id"]
        for item in sheets_by_id.values()
    }
    for row in validated_rows(
        R300C_WITNESS,
        "Round300C_virtual_occurrence_positive_volume_witness_row_id",
        COMMITMENTS["R300C"],
    ):
        node_id = row["virtual_stratum_node_id"]
        if node_id in sheets_by_id:
            direct_witnesses[node_id].append(row)
        if node_id in owner_bulk_ids:
            bulk_witnesses[node_id].append(row)
    need(
        not direct_witnesses
        and sum(map(len, bulk_witnesses.values())) == 8
        and len(bulk_witnesses) == 8
        and all(len(rows) == 1 for rows in bulk_witnesses.values()),
        "R300C zero direct sheet / eight owner-bulk context witnesses",
    )

    output_rows: list[dict[str, Any]] = []
    for sheet_id in sorted(sheets_by_id):
        item = sheets_by_id[sheet_id]
        sheet = item["sheet"]
        source = item["source"]
        frontier = item["frontier"]
        sheet_virtual = item["sheet_virtual"]
        bulk_virtual = item["bulk_virtual"]
        bulk_context = bulk_witnesses.get(
            sheet["owner_wall_bulk_node_id"], []
        )
        payload = {
            "Round302A_double_endpoint_sheet_exclusion_row_id":
                "round302a-double-endpoint-sheet-exclusion:"
                + digest([sheet_id, sheet["row_sha256"]]),
            "source_Round248_wall_sheet_node_id": sheet_id,
            "source_Round248_wall_sheet_row_sha256": sheet["row_sha256"],
            "source_Round236_double_endpoint_partition_row_id":
                source["double_endpoint_partition_row_id"],
            "source_Round234_frontier_row_id":
                frontier["frontier_row_id"],
            "Round220_split_interface_id":
                sheet["Round220_split_interface_id"],
            "Round179_retained_child_row_id":
                frontier["Round179_retained_child_row_id"],
            "source_chart": frontier["chart"],
            "endpoint_factor": sheet["endpoint_factor"],
            "exact_closed_base_rectangle":
                sheet["exact_closed_base_rectangle"],
            "owner_signature_sha256":
                sheet["owner_signature_sha256"],
            "owner_official_key_id":
                sheet["owner_official_key_id"],
            "owner_wall_bulk_node_id":
                sheet["owner_wall_bulk_node_id"],
            "post_Round266_sheet_component_id":
                sheet_virtual["post_Round266_quotient_component_id"],
            "post_Round266_owner_bulk_component_id":
                bulk_virtual["post_Round266_quotient_component_id"],
            "sheet_owner_bulk_already_internal_in_Round266": True,
            "R291_same_retained_child_and_chart_cell_count": 0,
            "R291_strict_positive_area_or_equal_base_candidate_count": 0,
            "R291_closed_boundary_contact_only_count": 0,
            "R295A_occurrence_attachment_candidate_count": 0,
            "R300C_direct_sheet_positive_volume_witness_count": 0,
            "R300C_owner_bulk_context_witness_count": len(bulk_context),
            "R300C_owner_bulk_context_witness_row_ids": [
                row[
                    "Round300C_virtual_occurrence_"
                    "positive_volume_witness_row_id"
                ]
                for row in bulk_context
            ],
            "R300C_owner_bulk_context_occurrence_ids": [
                row["Round294_registry_occurrence_id"]
                for row in bulk_context
            ],
            "owner_bulk_witness_transfer_to_sheet_credit": 0,
            "raw_owner_edge_reissued_as_occurrence_attachment_credit": 0,
            "attachment_exclusion_reason":
                "NO_ROUND291_SAME_LINEAGE_PHYSICAL_CELL__"
                "NO_R295A_OCCURRENCE_CANDIDATE__"
                "NO_R300C_DIRECT_SHEET_WITNESS",
            "eligible_for_component_DSU_application": False,
            "formal_component_edge_credit": 0,
            "formal_component_union_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_occurrence_identity_collapse_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
        }
        output_rows.append(close_row(payload))

    need(
        len(output_rows) == 32
        and len({
            row["Round302A_double_endpoint_sheet_exclusion_row_id"]
            for row in output_rows
        }) == 32,
        "complete output row census",
    )

    result = {
        "schema": SCHEMA,
        "status":
            "PASS_ROUND302A_EXACT_32_R248_DOUBLE_ENDPOINT_SHEETS__"
            "ALL_OCCURRENCE_ATTACHMENTS_EXCLUDED_FAIL_CLOSED",
        "input_manifest_pins": dict(sorted(MANIFEST_PINS.items())),
        "input_file_pins": dict(sorted(FILE_PINS.items())),
        "complete_frontier_census": {
            "Round236_double_endpoint_partition_count": 16,
            "Round248_complete_wall_sheet_count": 38_360,
            "Round248_single_endpoint_sheet_count": 38_328,
            "Round248_double_endpoint_sheet_count": 32,
            "Round248_double_endpoint_owner_bulk_count": 16,
            "Round266_selected_virtual_node_count": 48,
            "Round266_sheet_owner_internal_component_pair_count": 32,
            "Round291_same_retained_child_and_chart_cell_count": 0,
            "Round291_positive_area_or_equal_base_candidate_count": 0,
            "Round291_closed_boundary_contact_only_count": 0,
            "Round295A_occurrence_attachment_candidate_count": 0,
            "Round300C_direct_sheet_positive_volume_witness_count": 0,
            "Round300C_owner_bulk_context_witness_count": 8,
            "Round300C_owner_bulk_context_witnessed_bulk_count": 8,
            "unresolved_sheet_count": 0,
        },
        "scope_contract": {
            "all_32_double_endpoint_sheets_reconstructed_from_R248": True,
            "both_source_and_target_factor_sheets_per_R236_partition": True,
            "R291_complete_physical_cell_frontier_streamed": True,
            "R295A_complete_physical_binding_frontier_streamed": True,
            "R300C_complete_positive_volume_witness_frontier_streamed": True,
            "R300E_legal_graph_attachment_predicate_reopened": True,
            "same_retained_child_and_source_chart_are_mandatory_first_stage":
                True,
            "exact_base_predicate_equation_and_owner_signature_are_required_"
            "after_first_stage": True,
            "first_stage_candidate_count_is_zero_so_later_predicates_cannot_"
            "be_bypassed": True,
            "owner_bulk_positive_volume_witness_is_not_sheet_attachment":
                True,
            "Round266_internal_sheet_owner_edge_is_not_occurrence_attachment":
                True,
            "no_spike_import_execute_or_parse": True,
        },
        "formal_credit_transition": {
            "formal_component_edge_credit": 0,
            "formal_component_union_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_occurrence_identity_collapse_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
        },
        "ledger": {
            "filename": LEDGER,
            "row_count": len(output_rows),
            "row_ids_sha256": digest([
                row[
                    "Round302A_double_endpoint_sheet_exclusion_row_id"
                ]
                for row in output_rows
            ]),
            "row_hashes_sha256": digest([
                row["row_sha256"] for row in output_rows
            ]),
            "rows_sha256": digest(output_rows),
            "schema": SCHEMA + ".ledger.v1",
        },
        "provenance": {
            "seed_affects_output": False,
            "Round301_or_R302_maximality_artifact_read": False,
            "spike_imported_executed_or_parsed": False,
        },
    }
    result["result_sha256"] = digest(result)
    return output_rows, result


def write_ledger(rows: list[dict[str, Any]]) -> None:
    document = {
        "every_row_closed_by_own_SHA256": True,
        "row_count": len(rows),
        "row_hashes_sha256": digest([
            row["row_sha256"] for row in rows
        ]),
        "row_ids_sha256": digest([
            row["Round302A_double_endpoint_sheet_exclusion_row_id"]
            for row in rows
        ]),
        "rows": rows,
        "rows_sha256": digest(rows),
        "schema": SCHEMA + ".ledger.v1",
        "status": "COMPLETE_32_ROW_FAIL_CLOSED_EXCLUSION",
    }
    path = HERE / LEDGER
    work = HERE / (LEDGER + ".incomplete")
    if work.exists():
        work.unlink()
    with work.open("xb") as raw:
        with gzip.GzipFile(
            filename="",
            mode="wb",
            fileobj=raw,
            compresslevel=9,
            mtime=0,
        ) as stream:
            stream.write(canonical(document))
    os.replace(work, path)


def write_result(result: dict[str, Any]) -> None:
    path = HERE / RESULT
    work = HERE / (RESULT + ".incomplete")
    if work.exists():
        work.unlink()
    work.write_bytes(canonical(result))
    os.replace(work, path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", default="302101")
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    need(bool(args.seed), "nonempty seed bookkeeping")
    rows, result = reconstruct()
    if not args.no_write:
        write_ledger(rows)
        write_result(result)
    print(canonical({
        "status": result["status"],
        "result_sha256": result["result_sha256"],
        "ledger_rows_sha256": result["ledger"]["rows_sha256"],
        "seed_affects_output": False,
        "artifact_written": not args.no_write,
    }).decode("utf-8"))


if __name__ == "__main__":
    main()
