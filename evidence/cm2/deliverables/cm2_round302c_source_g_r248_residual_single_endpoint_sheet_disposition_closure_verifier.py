#!/usr/bin/env python3
"""Independent verifier for the Round302-C residual single-sheet closure.

The candidate producer is never imported, executed, tokenized, or parsed.
Only its fixed SHA-256 byte commitment is checked.  Expected rows, result, and
deterministic gzip bytes are reconstructed first from complete pinned upstream
frontiers; candidate artifacts are opened only after that reconstruction.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from copy import deepcopy
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat
import tempfile
from typing import Any, Callable, Iterable, Iterator, TextIO


HERE = Path(__file__).resolve().parent
PREFIX = (
    "cm2_round302c_source_g_r248_residual_single_endpoint_"
    "sheet_disposition_closure"
)
LEDGER = PREFIX + "_disposition_ledger.json.gz"
RESULT = PREFIX + "_result.json"
PRODUCER = PREFIX + ".py"
ATTACKS = PREFIX + "_attack_suite.json"
VERIFICATION = PREFIX + "_verification.json"
SCHEMA = (
    "cm2.round302c.source-g-r248-residual-single-endpoint-"
    "sheet-disposition-closure.v1"
)
PRODUCER_SHA256 = (
    "e583aff49329c047ae9797084bfba8509b1a3184f2bb04b63de2351f04adbaef"
)

R234_CERT = (
    "cm2_round234_source_g_wall_endpoint_order_depth6_"
    "materialization_certificate.json"
)
R235_CERT = (
    "cm2_round235_source_g_single_endpoint_graph_word_key_"
    "partition_certificate.json"
)
R248_CERT = (
    "cm2_round248_source_g_wall_finite_key_retained_"
    "quotient_certificate.json"
)
R266_CERT = (
    "cm2_round266_source_g_expanded_curved_face_closure_certificate.json"
)
R291_LEDGER = (
    "cm2_round291_source_g_complete_lower_stratum_local_"
    "disposition_freeze_ledger.json.gz"
)
R295A_LEDGER = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_"
    "closure_physical_witness_incidence_binding_ledger.json.gz"
)
R300C_WITNESS = (
    "cm2_round300c_source_g_virtual_stratum_new_occurrence_positive_"
    "volume_edge_promotion_witness_ledger.json.gz"
)
R300E_WITNESS = (
    "cm2_round300e_source_g_r248_half_open_owner_lower_component_"
    "edge_promotion_witness_ledger.json.gz"
)
R300E_RESULT = (
    "cm2_round300e_source_g_r248_half_open_owner_lower_component_"
    "edge_promotion_result.json"
)
R302A_LEDGER = (
    "cm2_round302a_source_g_r248_double_endpoint_sheet_"
    "attachment_exclusion_ledger.json.gz"
)
R302A_RESULT = (
    "cm2_round302a_source_g_r248_double_endpoint_sheet_"
    "attachment_exclusion_result.json"
)

FILE_PINS = {
    R234_CERT:
        "6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac",
    R235_CERT:
        "e340fa1a071d85a36b54d10a45ae2fdb9d70b8c90f4c21f054c6fc9505e5e787",
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
    R300E_WITNESS:
        "69f480da55e917b7b75bfe1efa823a9228d9b563f6f3aabd4e2a364c9e50eb9f",
    R300E_RESULT:
        "193c74535431789ba4fcdad598487916712d6ad1c04f191a083076e4a05f7e3e",
    R302A_LEDGER:
        "f71feba87a6ae9e8524c2d86c7489ffe19c71dd08c9ebec75a90702f0e81b558",
    R302A_RESULT:
        "5fddf94222712385684c117d220a165934450a80a318ae3d26e26a81ef3cc160",
}

MANIFEST_PINS = {
    "cm2_round234_source_g_wall_endpoint_order_depth6_"
    "materialization_manifest.sha256":
        "f8714ecdf804657fc6633136544f567b07e7d8503095d17fcda19226feefc432",
    "cm2_round235_source_g_single_endpoint_graph_word_key_"
    "partition_manifest.sha256":
        "cf58b7d2f419ea252c3398665302fe6f5ff06436af20a56beaaa47e5ef822ea0",
    "cm2_round248_source_g_wall_finite_key_retained_"
    "quotient_manifest.sha256":
        "b1ddedd01041e71b5c12fa4989726815c8685e6df77f54d9dbddda64aaf89e07",
    "cm2_round266_source_g_expanded_curved_face_closure_manifest.sha256":
        "63fb5b25d52ca5de579256499629d04d15f6a313e0a73f7e80fcb463385cbe09",
    "cm2_round291_source_g_complete_lower_stratum_local_"
    "disposition_freeze_manifest.sha256":
        "d655907a45cfb7b47ebdc822d35a0e604fc27fa38547c300139c116d7a2191ce",
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_"
    "closure_manifest.sha256":
        "b25f11c0090c56d2ad2d3b2cd0b172e7c089f044ae5722eb9e82ae04b129094a",
    "cm2_round300c_source_g_virtual_stratum_new_occurrence_positive_"
    "volume_edge_promotion_manifest.sha256":
        "cd327de2702ac209b0b0a03d09b3744596a901c2d65794dd86231d31a0be3503",
    "cm2_round300e_source_g_r248_half_open_owner_lower_component_"
    "edge_promotion_manifest.sha256":
        "4e6c4eec1af04a907285d41395aeef63e911b3b5486db91b33a95fa62e45177a",
    "cm2_round302a_source_g_r248_double_endpoint_sheet_"
    "attachment_exclusion_manifest.sha256":
        "b4a53c485da9fd889e3a9194c7e770f2a32eb14027e8bfd0f7c2370eab9eca71",
}

MANIFEST_MEMBERS = {
    next(name for name in MANIFEST_PINS if "round234_" in name): {
        R234_CERT: FILE_PINS[R234_CERT],
    },
    next(name for name in MANIFEST_PINS if "round235_" in name): {
        R235_CERT: FILE_PINS[R235_CERT],
    },
    next(name for name in MANIFEST_PINS if "round248_" in name): {
        "deliverables/" + R248_CERT: FILE_PINS[R248_CERT],
    },
    next(name for name in MANIFEST_PINS if "round266_" in name): {
        R266_CERT: FILE_PINS[R266_CERT],
    },
    next(name for name in MANIFEST_PINS if "round291_" in name): {
        R291_LEDGER: FILE_PINS[R291_LEDGER],
    },
    next(name for name in MANIFEST_PINS if "round295a_" in name): {
        R295A_LEDGER: FILE_PINS[R295A_LEDGER],
    },
    next(name for name in MANIFEST_PINS if "round300c_" in name): {
        R300C_WITNESS: FILE_PINS[R300C_WITNESS],
    },
    next(name for name in MANIFEST_PINS if "round300e_" in name): {
        R300E_WITNESS: FILE_PINS[R300E_WITNESS],
        R300E_RESULT: FILE_PINS[R300E_RESULT],
    },
    next(name for name in MANIFEST_PINS if "round302a_" in name): {
        R302A_LEDGER: FILE_PINS[R302A_LEDGER],
        R302A_RESULT: FILE_PINS[R302A_RESULT],
    },
}

COMMITMENTS = {
    "R248_SHEET": (
        38_360,
        "fbb15ef7122367925c72f9d0e396141d3f04a271b78064af41e1f68d9d06cd61",
        "be2e8b880f3a0c8fb833a7ba8dce0bd86d5526b400569377f0fcb66692a8c7e0",
        "e61754dc51732c4c82876d1c2e83fa040747d23253addd64350728169f5ae44b",
    ),
    "R248_BULK": (
        88_936,
        "6106c39894a7947293934b0b061bcae04e1a2902976b63ccd1756d7790cb6154",
        "e46f242e15bcba4111e14aac3c1dc5d82a5350e9e1514f2b9f90cdbc853e525d",
        "aff5ea1401a6919529d1d54fe54bb9b8d378456fa48f88a75043505b5ee7b8b0",
    ),
    "R266": (
        133_284,
        "2d42533f48f864f01e6bd4a46470e7266c1a2cec590380483cfb7cbfb84634f2",
        "9c31ba929e13eeaea29a9f6abe7cf324222eacb25d123a9b12252b386c12a32e",
        "8c394c1d1b2b42025c25a00ef24ecba748981ed93c75b9aba20ddf15ff8597d5",
    ),
    "R291": (
        55_428,
        "dc1abc74dde77cf7d114cacbd942a55527d90cf722efc6c679de58beffe8d11e",
        "3c47783f6e00c7c0aa3c1ee577f31ba6ca37a4a73ddea420e1211705fc8576fa",
        "a347c5423b857d4b8aeaae6f48e5d2f6ef81caf15a9329ff0909df77258a4279",
    ),
    "R295A": (
        113_452,
        "a0f471c84148d57eba4511efd8b343eb152c9378a24e018b9f0be10e41525805",
        "7eab57334f6f5170ffaef60316250078cd6774cdabdb7279d3585267345e5258",
        "e8b00ffa431d7609d97e7e3cae00f656d2386643acc22d49bdc4a018ed295946",
    ),
    "R300C": (
        6_322,
        "54147f135d32ab8326d2bee9d75994086cb7e137dd3350d75a9a2663d56699b6",
        "b1c09d20d57ff7f4fee44a0f915929be5810fcbdc6d3014e66467a6e747f5800",
        "849b2b8d51571c2be4280354b7b260d8d9f52e2793ae08cd393d1dcf9e97e5b2",
    ),
    "R300E": (
        12_992,
        "8d4f4eb7e1a1058283c9c163eefe2516c01193e3d84a8ab8b0174faee3f9e9c8",
        "71b8457998a7e5813d57b10197c2a8506111c7ec041f893bb177d8a01de5ab92",
        "6d2f26a0782e66fe01d440586c21846581a55944252e364909bb08600e09abaa",
    ),
    "R302A": (
        32,
        "99abbdb99642ef3f60611a423cd22f31f872cada8e318e7eca7058dd8bee7b82",
        "71a60299c23a2aa9f16a3d8993424f4334f9ecafc117fc7221f48a7b8be28a51",
        "75dbc01a8b58ee41bc17b08f414b29cb82254b293024334614785abcfb216c9b",
    ),
}

PREDICATE_ORDER = [
    "P01_R291_SAME_RETAINED_CHILD_AND_SOURCE_CHART_PHYSICAL_CELL_EXISTS",
    "P02_R295A_EXACT_TWO_SIDED_GRAPH_BINDING_EXISTS",
    "P03_R291_PREDICATE_EQUATION_MATCHES_R235_WALL_REASON",
    "P04_R248_BASE_EQUALS_R291_GRAPH_CELL_BASE",
    "P05_R234_FULL_SIX_COORDINATE_BOX_CONTAINED_IN_R291_CELL",
    "P06_UNIQUE_EVENT_ABSENT_OWNER_SIGNATURE",
    "P07_OWNER_OFFICIAL_KEY_AND_PRESENT_SIDE_EXCLUSION",
    "P08_R248_SHEET_AND_OWNER_BULK_SHARE_ROUND266_ROOT",
]
FIRST_FAILURE = "P01_NO_R291_SAME_RETAINED_CHILD_AND_SOURCE_CHART_PHYSICAL_CELL"


class VerificationError(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


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
        safe_file(HERE / manifest, 300_000)
        need(file_sha256(HERE / manifest) == pin, "manifest pin:" + manifest)
        entries = parse_manifest(manifest)
        for member, member_pin in MANIFEST_MEMBERS[manifest].items():
            need(entries.get(member) == member_pin, "manifest member:" + member)
    for name, pin in FILE_PINS.items():
        safe_file(HERE / name)
        need(file_sha256(HERE / name) == pin, "file pin:" + name)


def verify_row(row: dict[str, Any], label: str) -> None:
    payload = dict(row)
    claimed = payload.pop("row_sha256", None)
    need(
        isinstance(claimed, str) and claimed == digest(payload),
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
            VerificationError("stream float:" + token)
        ),
        parse_constant=lambda token: (_ for _ in ()).throw(
            VerificationError("stream constant:" + token)
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
    expected: tuple[int, str, str, str],
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
            verify_row(row, name)
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
        (
            rows.count,
            ids.finish(),
            hashes.finish(),
            rows.finish(),
        ) == expected,
        "complete table commitment:" + name,
    )


def load_wrapped_result(name: str) -> dict[str, Any]:
    safe_file(HERE / name)
    document = json.loads((HERE / name).read_text(encoding="utf-8"))
    need(
        type(document) is dict
        and set(document) == {"schema", "result", "result_sha256"}
        and type(document["result"]) is dict
        and document["result_sha256"] == digest(document["result"]),
        "closed wrapped result:" + name,
    )
    return document["result"]


def load_direct_result(name: str) -> dict[str, Any]:
    safe_file(HERE / name)
    result = json.loads((HERE / name).read_text(encoding="utf-8"))
    need(type(result) is dict, "direct result object:" + name)
    payload = dict(result)
    claimed = payload.pop("result_sha256", None)
    need(claimed == digest(payload), "direct result closure:" + name)
    return result


def close_row(payload: dict[str, Any]) -> dict[str, Any]:
    need("row_sha256" not in payload, "fresh row")
    row = dict(payload)
    row["row_sha256"] = digest(payload)
    return row


def independent_rebuild() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    validate_input_boundary()

    r235 = load_wrapped_result(R235_CERT)
    partition_rows = r235["single_endpoint_graph_partition_rows"]
    need(
        len(partition_rows) == 38_328
        and digest(partition_rows)
        == "e9a3794540170bf013160fb713acfbb1a65d42afedfb7b972cbfdad290549731",
        "complete R235 partition",
    )
    partitions = {
        row["endpoint_graph_partition_row_id"]: row
        for row in partition_rows
    }
    need(len(partitions) == 38_328, "unique R235 partition")

    r234 = load_wrapped_result(R234_CERT)
    frontier_rows = r234["depth6_frontier_rows"]
    need(
        len(frontier_rows) == 38_376
        and digest(frontier_rows)
        == "a1b3bf193ad10045f52244c3e40c52f78e0aeacffa3ba52c262bc8912fc9b5a6",
        "complete R234 frontier",
    )
    wanted_frontiers = {
        row["Round234_frontier_row_id"] for row in partition_rows
    }
    frontiers = {
        row["frontier_row_id"]: row
        for row in frontier_rows
        if row["frontier_row_id"] in wanted_frontiers
    }
    need(len(frontiers) == 38_328, "complete R234/R235 join")

    singles: dict[str, dict[str, Any]] = {}
    double_ids: set[str] = set()
    source_kind_histogram: Counter[str] = Counter()
    for sheet in validated_rows(
        R248_CERT,
        "wall_sheet_node_id",
        COMMITMENTS["R248_SHEET"],
        table="formal_wall_half_open_sheet_owner_ledger",
    ):
        kind = sheet["source_partition_kind"]
        source_kind_histogram[kind] += 1
        sheet_id = sheet["wall_sheet_node_id"]
        if kind == "ROUND236_DOUBLE_ENDPOINT_GRAPH_SHEET":
            double_ids.add(sheet_id)
            continue
        need(kind == "ROUND235_SINGLE_ENDPOINT_GRAPH_SHEET", "R248 sheet kind")
        source = partitions[sheet["source_partition_row_id"]]
        frontier = frontiers[source["Round234_frontier_row_id"]]
        need(
            sheet["Round220_split_interface_id"]
            == source["Round220_split_interface_id"]
            == frontier["Round220_split_interface_id"],
            "R248/R235/R234 interface lineage",
        )
        need(
            sheet["endpoint_factor"] == source["active_endpoint_factor"]
            and sheet["owner_signature_sha256"]
            == digest(source["event_absent_signature"])
            and sheet["owner_official_key_id"]
            == source["event_absent_signature"]["official_key_id"],
            "R248 exact single-sheet owner policy",
        )
        need(
            sheet["exact_closed_base_rectangle"] == frontier["box"][2:6]
            and sheet["physical_component_credit"] == 0
            and sheet["maximal_physical_component_credit"] == 0,
            "R248 exact base and nonmaximal local owner edge",
        )
        need(sheet_id not in singles, "unique R248 single sheet")
        singles[sheet_id] = {
            "sheet": sheet,
            "source": source,
            "frontier": frontier,
        }
    need(
        source_kind_histogram
        == {
            "ROUND235_SINGLE_ENDPOINT_GRAPH_SHEET": 38_328,
            "ROUND236_DOUBLE_ENDPOINT_GRAPH_SHEET": 32,
        }
        and len(singles) == 38_328
        and len(double_ids) == 32,
        "complete R248 sheet-kind census",
    )

    wanted_bulk_ids = {
        item["sheet"]["owner_wall_bulk_node_id"]
        for item in singles.values()
    }
    bulks: dict[str, dict[str, Any]] = {}
    for bulk in validated_rows(
        R248_CERT,
        "wall_bulk_node_id",
        COMMITMENTS["R248_BULK"],
        table="formal_wall_positive_volume_bulk_ledger",
    ):
        bulk_id = bulk["wall_bulk_node_id"]
        if bulk_id in wanted_bulk_ids:
            bulks[bulk_id] = bulk
    need(len(bulks) == len(wanted_bulk_ids) == 38_328, "R248 owner bulks")
    for item in singles.values():
        sheet = item["sheet"]
        bulk = bulks[sheet["owner_wall_bulk_node_id"]]
        need(
            bulk["branch_label"] == "EVENT_ABSENT"
            and bulk["local_return_signature_sha256"]
            == sheet["owner_signature_sha256"]
            and bulk["official_key_id"] == sheet["owner_official_key_id"]
            and bulk["assigned_mixed_sheet_quotient_component_id"]
            == sheet["assigned_mixed_sheet_quotient_component_id"],
            "R248 exact sheet-owner-bulk join",
        )
        item["owner_bulk"] = bulk

    promoted: dict[str, dict[str, Any]] = {}
    for witness in validated_rows(
        R300E_WITNESS,
        "Round300E_half_open_owner_component_edge_witness_row_id",
        COMMITMENTS["R300E"],
    ):
        sheet_id = witness["source_Round248_wall_sheet_node_id"]
        need(
            sheet_id in singles
            and sheet_id not in promoted
            and witness["source_Round248_wall_sheet_row_sha256"]
            == singles[sheet_id]["sheet"]["row_sha256"]
            and witness["formal_half_open_owner_component_edge_witness_credit"]
            == 1
            and witness["eligible_for_component_DSU_application"] is True,
            "R300E positive witness exact R248 subset",
        )
        promoted[sheet_id] = witness
    r300e_result = load_direct_result(R300E_RESULT)
    need(
        len(promoted) == 12_992
        and r300e_result["source_audit"]["R248_matched_sheet_count"] == 12_992
        and r300e_result["source_audit"][
            "R295A_two_sided_graph_sheet_binding_count"
        ] == 111_524
        and r300e_result["strict_nonpromotion"]["maximality_credit"] == 0,
        "R300E complete positive set",
    )

    r302a_ids: set[str] = set()
    for exclusion in validated_rows(
        R302A_LEDGER,
        "Round302A_double_endpoint_sheet_exclusion_row_id",
        COMMITMENTS["R302A"],
    ):
        sheet_id = exclusion["source_Round248_wall_sheet_node_id"]
        need(
            sheet_id in double_ids
            and sheet_id not in r302a_ids
            and exclusion["eligible_for_component_DSU_application"] is False
            and exclusion["formal_maximality_credit"] == 0,
            "R302A exact double-sheet exclusion",
        )
        r302a_ids.add(sheet_id)
    r302a_result = load_direct_result(R302A_RESULT)
    need(
        r302a_ids == double_ids
        and not (r302a_ids & set(singles))
        and r302a_result["complete_frontier_census"][
            "Round248_double_endpoint_sheet_count"
        ] == 32
        and r302a_result["ledger"]["rows_sha256"]
        == COMMITMENTS["R302A"][3],
        "R302A complete disjoint tranche",
    )

    residual_ids = sorted(set(singles) - set(promoted))
    residual_set = set(residual_ids)
    need(
        len(residual_ids) == 25_336
        and not (set(residual_ids) & set(promoted))
        and set(residual_ids) | set(promoted) == set(singles),
        "R248/R300E exact single-sheet partition",
    )

    by_lineage: dict[tuple[str, str], list[str]] = defaultdict(list)
    for sheet_id, item in singles.items():
        frontier = item["frontier"]
        by_lineage[(
            frontier["Round179_retained_child_row_id"],
            frontier["chart"],
        )].append(sheet_id)
    for ids in by_lineage.values():
        ids.sort()

    physical_counts: Counter[str] = Counter()
    graph_counts: Counter[str] = Counter()
    graph_cell_sheets: dict[tuple[str, int], tuple[str, list[str]]] = {}
    for disposition in validated_rows(
        R291_LEDGER,
        "complete_lower_stratum_local_disposition_row_id",
        COMMITMENTS["R291"],
    ):
        disposition_id = disposition[
            "complete_lower_stratum_local_disposition_row_id"
        ]
        chart = disposition["source_chart"]
        for index, cell in enumerate(disposition["physical_witness_cells"]):
            retained = cell.get("retained_child_row_id")
            if not isinstance(retained, str):
                continue
            ids = by_lineage.get((retained, chart), [])
            for sheet_id in ids:
                physical_counts[sheet_id] += 1
            if cell.get("witness_kind") == "ROUND182_GRAPH_SHEET_LEAF":
                for sheet_id in ids:
                    graph_counts[sheet_id] += 1
                if ids:
                    graph_cell_sheets[(disposition_id, index)] = (
                        chart,
                        ids,
                    )

    need(
        {sheet_id for sheet_id in singles if physical_counts[sheet_id] == 1}
        == set(promoted)
        and {sheet_id for sheet_id in singles if graph_counts[sheet_id] == 1}
        == set(promoted)
        and all(
            physical_counts[sheet_id] == graph_counts[sheet_id] == 0
            for sheet_id in residual_ids
        ),
        "R291 exact 0 residual / 1 promoted lineage partition",
    )

    binding_counts: Counter[str] = Counter()
    binding_class_histogram: Counter[str] = Counter()
    for binding in validated_rows(
        R295A_LEDGER,
        "Round295A_R291_physical_incidence_binding_row_id",
        COMMITMENTS["R295A"],
    ):
        classification = binding["source_Round293_binding_classification"]
        binding_class_histogram[classification] += 1
        if classification != "EXACT_TWO_SIDED_GRAPH_SHEET_ATOM_INCIDENCE":
            continue
        key = (
            binding["Round291_local_disposition_row_id"],
            binding["physical_witness_cell_index"],
        )
        joined = graph_cell_sheets.get(key)
        if joined is None:
            continue
        chart, ids = joined
        need(binding["source_chart"] == chart, "R291/R295A source chart")
        for sheet_id in ids:
            binding_counts[sheet_id] += 1
    need(
        binding_class_histogram[
            "EXACT_TWO_SIDED_GRAPH_SHEET_ATOM_INCIDENCE"
        ] == 111_524
        and {sheet_id for sheet_id in singles if binding_counts[sheet_id] == 1}
        == set(promoted)
        and all(binding_counts[sheet_id] == 0 for sheet_id in residual_ids),
        "R295A exact 0 residual / 1 promoted graph-binding partition",
    )

    selected_nodes = set(residual_ids)
    selected_nodes.update(
        singles[sheet_id]["sheet"]["owner_wall_bulk_node_id"]
        for sheet_id in residual_ids
    )
    virtual: dict[str, dict[str, Any]] = {}
    for row in validated_rows(
        R266_CERT,
        "post_Round266_valid_virtual_node_frontier_row_id",
        COMMITMENTS["R266"],
        table="formal_post_Round266_valid_virtual_node_frontier_ledger",
    ):
        node_id = row["valid_virtual_stratum_node_id"]
        if node_id in selected_nodes:
            virtual[node_id] = row
    need(
        len(selected_nodes) == 50_672
        and len(virtual) == 50_488,
        "complete residual R266 valid-virtual presence audit",
    )
    r266_presence_histogram: Counter[str] = Counter()
    for sheet_id in residual_ids:
        sheet = singles[sheet_id]["sheet"]
        sheet_virtual = virtual[sheet_id]
        bulk_virtual = virtual.get(sheet["owner_wall_bulk_node_id"])
        need(
            sheet_virtual["virtual_node_kind"] == "ROUND248_WALL_SHEET",
            "residual sheet present in R266 valid frontier",
        )
        if bulk_virtual is None:
            status = "OWNER_BULK_ABSENT_FROM_ROUND266_VALID_FRONTIER"
        else:
            need(
                bulk_virtual["virtual_node_kind"] == "ROUND248_WALL_BULK"
                and sheet_virtual["post_Round266_quotient_component_id"]
                == bulk_virtual["post_Round266_quotient_component_id"],
                "present residual sheet-owner bulk internal in R266",
            )
            status = "SHEET_AND_OWNER_BULK_PRESENT_AND_SAME_ROUND266_ROOT"
        r266_presence_histogram[status] += 1
        singles[sheet_id]["sheet_virtual"] = sheet_virtual
        singles[sheet_id]["bulk_virtual"] = bulk_virtual
        singles[sheet_id]["r266_presence_status"] = status
    need(
        r266_presence_histogram
        == {
            "SHEET_AND_OWNER_BULK_PRESENT_AND_SAME_ROUND266_ROOT": 25_152,
            "OWNER_BULK_ABSENT_FROM_ROUND266_VALID_FRONTIER": 184,
        },
        "exact residual R266 presence histogram",
    )

    direct_context: dict[str, list[dict[str, Any]]] = defaultdict(list)
    bulk_context: dict[str, list[dict[str, Any]]] = defaultdict(list)
    residual_bulk_ids = {
        singles[sheet_id]["sheet"]["owner_wall_bulk_node_id"]
        for sheet_id in residual_ids
    }
    r300c_kind_histogram: Counter[str] = Counter()
    for witness in validated_rows(
        R300C_WITNESS,
        "Round300C_virtual_occurrence_positive_volume_witness_row_id",
        COMMITMENTS["R300C"],
    ):
        kind = witness["virtual_node_kind"]
        r300c_kind_histogram[kind] += 1
        node_id = witness["virtual_stratum_node_id"]
        if node_id in residual_set:
            direct_context[node_id].append(witness)
        if node_id in residual_bulk_ids:
            bulk_context[node_id].append(witness)
    need(
        r300c_kind_histogram
        == {
            "INHERITED_ROUND247_VIRTUAL_STRATUM": 4_106,
            "ROUND248_WALL_BULK": 2_216,
        }
        and not direct_context
        and len(bulk_context) == 272
        and sum(map(len, bulk_context.values())) == 272
        and all(len(rows) == 1 for rows in bulk_context.values()),
        "R300C zero direct residual / 272 nontransferable bulk contexts",
    )

    output_rows: list[dict[str, Any]] = []
    endpoint_histogram: Counter[str] = Counter()
    chart_histogram: Counter[str] = Counter()
    reason_histogram: Counter[str] = Counter()
    for sheet_id in residual_ids:
        item = singles[sheet_id]
        sheet = item["sheet"]
        source = item["source"]
        frontier = item["frontier"]
        owner_bulk = item["owner_bulk"]
        sheet_virtual = item["sheet_virtual"]
        bulk_virtual = item["bulk_virtual"]
        contexts = bulk_context.get(sheet["owner_wall_bulk_node_id"], [])
        endpoint_histogram[sheet["endpoint_factor"]] += 1
        chart_histogram[frontier["chart"]] += 1
        reason_histogram[source["reason_label"]] += 1
        payload = {
            "Round302C_residual_single_endpoint_sheet_disposition_row_id":
                "round302c-residual-single-endpoint-sheet-disposition:"
                + digest([sheet_id, sheet["row_sha256"], FIRST_FAILURE]),
            "source_Round248_wall_sheet_node_id": sheet_id,
            "source_Round248_wall_sheet_row_sha256": sheet["row_sha256"],
            "source_Round235_endpoint_graph_partition_row_id":
                source["endpoint_graph_partition_row_id"],
            "source_Round235_endpoint_graph_partition_row_sha256":
                digest(source),
            "source_Round234_frontier_row_id": frontier["frontier_row_id"],
            "source_Round234_frontier_row_sha256": digest(frontier),
            "Round220_split_interface_id":
                sheet["Round220_split_interface_id"],
            "Round179_retained_child_row_id":
                frontier["Round179_retained_child_row_id"],
            "source_chart": frontier["chart"],
            "endpoint_factor": sheet["endpoint_factor"],
            "R235_reason_label": source["reason_label"],
            "exact_closed_base_rectangle":
                sheet["exact_closed_base_rectangle"],
            "owner_signature_sha256": sheet["owner_signature_sha256"],
            "owner_official_key_id": sheet["owner_official_key_id"],
            "owner_wall_bulk_node_id": sheet["owner_wall_bulk_node_id"],
            "source_Round248_owner_wall_bulk_row_sha256":
                owner_bulk["row_sha256"],
            "source_Round266_sheet_frontier_row_id":
                sheet_virtual[
                    "post_Round266_valid_virtual_node_frontier_row_id"
                ],
            "source_Round266_sheet_frontier_row_sha256":
                sheet_virtual["row_sha256"],
            "source_Round266_owner_bulk_frontier_row_id":
                None if bulk_virtual is None else bulk_virtual[
                    "post_Round266_valid_virtual_node_frontier_row_id"
                ],
            "source_Round266_owner_bulk_frontier_row_sha256":
                None if bulk_virtual is None else bulk_virtual["row_sha256"],
            "post_Round266_sheet_component_id":
                sheet_virtual["post_Round266_quotient_component_id"],
            "post_Round266_owner_bulk_component_id":
                None if bulk_virtual is None else bulk_virtual[
                    "post_Round266_quotient_component_id"
                ],
            "Round266_sheet_owner_bulk_presence_status":
                item["r266_presence_status"],
            "sheet_owner_bulk_already_internal_in_Round266":
                bulk_virtual is not None,
            "R300E_positive_owner_attachment_witness_count": 0,
            "absent_from_complete_Round300E_positive_witness_set": True,
            "R302A_double_endpoint_exclusion_overlap_count": 0,
            "R291_same_retained_child_and_source_chart_physical_cell_count":
                physical_counts[sheet_id],
            "R291_same_retained_child_and_source_chart_graph_cell_count":
                graph_counts[sheet_id],
            "R295A_same_lineage_exact_two_sided_graph_binding_count":
                binding_counts[sheet_id],
            "earliest_failed_legal_attachment_predicate_ordinal": 1,
            "earliest_failed_legal_attachment_predicate": FIRST_FAILURE,
            "later_legal_attachment_predicates_evaluated": False,
            "later_legal_attachment_predicates_not_reached_fail_closed": True,
            "R300C_direct_sheet_positive_volume_witness_count": 0,
            "R300C_owner_bulk_context_witness_count": len(contexts),
            "R300C_owner_bulk_context_witness_row_ids": [
                row[
                    "Round300C_virtual_occurrence_"
                    "positive_volume_witness_row_id"
                ]
                for row in contexts
            ],
            "R300C_owner_bulk_context_occurrence_ids": [
                row["Round294_registry_occurrence_id"] for row in contexts
            ],
            "owner_bulk_witness_transfer_to_sheet_credit": 0,
            "R248_local_owner_edge_reissued_as_occurrence_attachment_credit":
                0,
            "attachment_disposition":
                "SEALED_EXCLUSION_AT_EARLIEST_R291_LINEAGE_PREDICATE",
            "eligible_as_sealed_attachment_exclusion_for_later_"
            "maximality_audit": True,
            "eligible_for_component_DSU_application": False,
            "formal_component_edge_credit": 0,
            "formal_component_union_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_occurrence_identity_collapse_credit": 0,
            "formal_quotient_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
        }
        output_rows.append(close_row(payload))
    output_rows.sort(
        key=lambda row:
        row[
            "Round302C_residual_single_endpoint_sheet_disposition_row_id"
        ]
    )
    need(
        len(output_rows) == 25_336
        and len({
            row["source_Round248_wall_sheet_node_id"] for row in output_rows
        }) == 25_336,
        "complete residual output rows",
    )

    ledger_meta = {
        "filename": LEDGER,
        "schema": SCHEMA + ".disposition-ledger.v1",
        "row_count": len(output_rows),
        "row_ids_sha256": digest([
            row[
                "Round302C_residual_single_endpoint_sheet_"
                "disposition_row_id"
            ]
            for row in output_rows
        ]),
        "row_hashes_sha256": digest([
            row["row_sha256"] for row in output_rows
        ]),
        "rows_sha256": digest(output_rows),
    }
    result = {
        "schema": SCHEMA,
        "status":
            "PASS_ROUND302C_EXACT_25336_R248_RESIDUAL_SINGLE_ENDPOINT_"
            "SHEETS__EARLIEST_P01_R291_LINEAGE_FAILURE__"
            "ZERO_CREDIT_SEALED_DISPOSITION",
        "input_manifest_pins": dict(sorted(MANIFEST_PINS.items())),
        "input_file_pins": dict(sorted(FILE_PINS.items())),
        "legal_attachment_predicate_order": PREDICATE_ORDER,
        "complete_frontier_census": {
            "Round248_complete_wall_sheet_count": 38_360,
            "Round248_single_endpoint_sheet_count": 38_328,
            "Round248_double_endpoint_sheet_count": 32,
            "Round300E_positive_single_endpoint_attachment_count": 12_992,
            "Round302C_residual_single_endpoint_exclusion_count": 25_336,
            "Round302A_disjoint_double_endpoint_exclusion_count": 32,
            "Round291_complete_disposition_row_count": 55_428,
            "Round291_residual_same_lineage_physical_cell_count": 0,
            "Round291_promoted_same_lineage_physical_cell_count": 12_992,
            "Round295A_complete_binding_row_count": 113_452,
            "Round295A_exact_two_sided_graph_binding_row_count": 111_524,
            "Round295A_residual_same_lineage_graph_binding_count": 0,
            "Round295A_promoted_same_lineage_graph_binding_count": 12_992,
            "Round266_residual_selected_node_request_count": 50_672,
            "Round266_residual_selected_valid_virtual_node_count": 50_488,
            "Round266_residual_sheet_valid_virtual_node_count": 25_336,
            "Round266_residual_owner_bulk_valid_virtual_node_count": 25_152,
            "Round266_residual_owner_bulk_absent_valid_frontier_count": 184,
            "Round266_residual_internal_sheet_owner_pair_count": 25_152,
            "Round300C_direct_residual_sheet_witness_count": 0,
            "Round300C_residual_owner_bulk_context_witness_count": 272,
            "Round300C_residual_owner_bulk_context_witnessed_bulk_count": 272,
            "eligible_component_edge_count": 0,
            "unresolved_residual_sheet_count": 0,
        },
        "first_failure_histogram": {
            FIRST_FAILURE: 25_336,
        },
        "residual_sheet_histograms": {
            "source_chart": dict(sorted(chart_histogram.items())),
            "endpoint_factor": dict(sorted(endpoint_histogram.items())),
            "R235_reason_label": dict(sorted(reason_histogram.items())),
            "R300C_owner_bulk_context_witness_count": {
                "0": 25_064,
                "1": 272,
            },
        },
        "sealed_attachment_disposition_partition": {
            "Round300E_positive_single_endpoint_sheet_count": 12_992,
            "Round302C_excluded_single_endpoint_sheet_count": 25_336,
            "Round302A_excluded_double_endpoint_sheet_count": 32,
            "complete_R248_sheet_count": 38_360,
            "single_positive_and_residual_disjoint": True,
            "single_positive_union_residual_is_complete": True,
            "double_endpoint_tranche_disjoint_from_single_endpoint": True,
            "complete_sheet_attachment_disposition_frontier": True,
            "formal_maximality_credit_issued_here": False,
        },
        "scope_contract": {
            "all_38328_single_endpoint_sheets_reconstructed_from_R248": True,
            "R300E_complete_12992_positive_witness_set_reopened": True,
            "all_25336_residual_sheets_are_exact_set_difference": True,
            "R291_complete_physical_cell_frontier_streamed": True,
            "R295A_complete_binding_frontier_streamed": True,
            "earliest_legal_attachment_predicate_recorded_per_sheet": True,
            "no_later_predicate_is_evaluated_after_first_failure": True,
            "R266_complete_valid_virtual_frontier_reopened": True,
            "R266_present_sheet_owner_pairs_have_identical_root": True,
            "R266_missing_owner_bulk_context_recorded_per_sheet": True,
            "R300C_complete_witness_frontier_streamed": True,
            "R300C_owner_bulk_witness_is_not_sheet_attachment": True,
            "R302A_complete_32_row_double_endpoint_tranche_reopened": True,
            "sealed_exclusions_are_inputs_to_a_later_maximality_audit_only":
                True,
            "no_spike_import_execute_or_parse": True,
        },
        "formal_credit_transition": {
            "eligible_component_edge_count": 0,
            "formal_component_edge_credit": 0,
            "formal_component_union_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_occurrence_identity_collapse_credit": 0,
            "formal_quotient_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
        },
        "ledger": ledger_meta,
        "provenance": {
            "seed_affects_output": False,
            "Round301_file_read": False,
            "spike_imported_executed_or_parsed": False,
        },
    }
    result["result_sha256"] = digest(result)
    return output_rows, result


def ledger_document(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "every_row_closed_by_own_SHA256": True,
        "row_count": len(rows),
        "row_hashes_sha256": digest([
            row["row_sha256"] for row in rows
        ]),
        "row_ids_sha256": digest([
            row[
                "Round302C_residual_single_endpoint_sheet_"
                "disposition_row_id"
            ]
            for row in rows
        ]),
        "rows": rows,
        "rows_sha256": digest(rows),
        "schema": SCHEMA + ".disposition-ledger.v1",
        "status":
            "COMPLETE_25336_ROW_EARLIEST_P01_FAIL_CLOSED_DISPOSITION",
    }


def gzip_bytes(value: Any) -> bytes:
    output = io.BytesIO()
    with gzip.GzipFile(
        filename="",
        mode="wb",
        fileobj=output,
        compresslevel=9,
        mtime=0,
    ) as stream:
        stream.write(canonical(value))
    return output.getvalue()


def strict_json_bytes(
    raw: bytes,
    label: str,
    *,
    expected_canonical: bytes | None = None,
) -> dict[str, Any]:
    need(
        raw
        and not raw.startswith(b"\xef\xbb\xbf")
        and b"\x00" not in raw,
        "json:strict-bytes:" + label,
    )

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in output, "json:duplicate-key:" + label)
            output[key] = value
        return output

    def reject_number(token: str) -> Any:
        raise VerificationError("json:noninteger:" + label + ":" + token)

    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=unique,
            parse_float=reject_number,
            parse_constant=reject_number,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise VerificationError("json:decode:" + label) from error
    need(type(value) is dict, "json:top-object:" + label)
    if expected_canonical is not None:
        need(
            raw == expected_canonical == canonical(value),
            "json:canonical-bytes:" + label,
        )
    return value


def strict_gzip_candidate(
    raw: bytes,
    expected_gzip: bytes,
    expected_json: bytes,
    label: str,
) -> dict[str, Any]:
    need(raw == expected_gzip, "gzip:canonical-bytes:" + label)
    try:
        expanded = gzip.decompress(raw)
    except (OSError, EOFError) as error:
        raise VerificationError("gzip:decode:" + label) from error
    return strict_json_bytes(
        expanded,
        label,
        expected_canonical=expected_json,
    )


def boundary_path_guard(path: Path, allowed: Path) -> None:
    need(path.parent.resolve() == allowed.resolve(), "path:escape")
    info = os.lstat(path)
    need(
        stat.S_ISREG(info.st_mode)
        and not path.is_symlink()
        and info.st_nlink == 1,
        "path:not-regular-single-link",
    )


ZERO_FIELDS = (
    "R300E_positive_owner_attachment_witness_count",
    "R302A_double_endpoint_exclusion_overlap_count",
    "R291_same_retained_child_and_source_chart_physical_cell_count",
    "R291_same_retained_child_and_source_chart_graph_cell_count",
    "R295A_same_lineage_exact_two_sided_graph_binding_count",
    "R300C_direct_sheet_positive_volume_witness_count",
    "owner_bulk_witness_transfer_to_sheet_credit",
    "R248_local_owner_edge_reissued_as_occurrence_attachment_credit",
    "formal_component_edge_credit",
    "formal_component_union_credit",
    "formal_DSU_rank_reduction_credit",
    "formal_occurrence_identity_collapse_credit",
    "formal_quotient_credit",
    "formal_maximality_credit",
    "formal_fibre_credit",
    "formal_global_disposition_credit",
)


def semantic_audit(
    rows: list[dict[str, Any]],
    result: dict[str, Any],
    expected_rows: list[dict[str, Any]],
    expected_result: dict[str, Any],
) -> None:
    need(len(rows) == 25_336, "semantic:row-count")
    need(
        len({
            row["source_Round248_wall_sheet_node_id"] for row in rows
        }) == 25_336,
        "semantic:complete-sheet-partition",
    )
    r266_status: Counter[str] = Counter()
    context_histogram: Counter[int] = Counter()
    for row in rows:
        verify_row(row, "candidate semantic")
        need(
            all(row[field] == 0 for field in ZERO_FIELDS),
            "semantic:zero-credit",
        )
        need(
            row["absent_from_complete_Round300E_positive_witness_set"]
            is True
            and row["earliest_failed_legal_attachment_predicate_ordinal"] == 1
            and row["earliest_failed_legal_attachment_predicate"]
            == FIRST_FAILURE
            and row["later_legal_attachment_predicates_evaluated"] is False
            and row[
                "later_legal_attachment_predicates_not_reached_fail_closed"
            ] is True,
            "semantic:earliest-failure",
        )
        need(
            row["attachment_disposition"]
            == "SEALED_EXCLUSION_AT_EARLIEST_R291_LINEAGE_PREDICATE"
            and row[
                "eligible_as_sealed_attachment_exclusion_for_later_"
                "maximality_audit"
            ] is True
            and row["eligible_for_component_DSU_application"] is False,
            "semantic:exclusion-not-edge",
        )
        status = row["Round266_sheet_owner_bulk_presence_status"]
        r266_status[status] += 1
        if status == (
            "SHEET_AND_OWNER_BULK_PRESENT_AND_SAME_ROUND266_ROOT"
        ):
            need(
                row["sheet_owner_bulk_already_internal_in_Round266"] is True
                and row["source_Round266_owner_bulk_frontier_row_id"]
                is not None
                and row["post_Round266_sheet_component_id"]
                == row["post_Round266_owner_bulk_component_id"],
                "semantic:R266-present",
            )
        else:
            need(
                status
                == "OWNER_BULK_ABSENT_FROM_ROUND266_VALID_FRONTIER"
                and row["sheet_owner_bulk_already_internal_in_Round266"]
                is False
                and row["source_Round266_owner_bulk_frontier_row_id"] is None
                and row["source_Round266_owner_bulk_frontier_row_sha256"]
                is None
                and row["post_Round266_owner_bulk_component_id"] is None,
                "semantic:R266-absent",
            )
        context_count = row["R300C_owner_bulk_context_witness_count"]
        context_histogram[context_count] += 1
        need(
            context_count in {0, 1}
            and len(row["R300C_owner_bulk_context_witness_row_ids"])
            == context_count
            and len(row["R300C_owner_bulk_context_occurrence_ids"])
            == context_count,
            "semantic:R300C-context",
        )
    need(
        r266_status
        == {
            "SHEET_AND_OWNER_BULK_PRESENT_AND_SAME_ROUND266_ROOT": 25_152,
            "OWNER_BULK_ABSENT_FROM_ROUND266_VALID_FRONTIER": 184,
        }
        and context_histogram == {0: 25_064, 1: 272},
        "semantic:context-census",
    )
    payload = dict(result)
    claimed = payload.pop("result_sha256", None)
    need(claimed == digest(payload), "semantic:result-closure")
    need(
        result["complete_frontier_census"]["eligible_component_edge_count"]
        == 0
        and result["complete_frontier_census"][
            "unresolved_residual_sheet_count"
        ] == 0
        and result["first_failure_histogram"] == {FIRST_FAILURE: 25_336}
        and result["formal_credit_transition"]
        == expected_result["formal_credit_transition"]
        and result["sealed_attachment_disposition_partition"][
            "complete_sheet_attachment_disposition_frontier"
        ] is True
        and result["sealed_attachment_disposition_partition"][
            "formal_maximality_credit_issued_here"
        ] is False,
        "semantic:result-scope",
    )
    need(rows == expected_rows, "semantic:independent-row-equality")
    need(result == expected_result, "semantic:independent-result-equality")


def reseal_attack(
    rows: list[dict[str, Any]],
    result: dict[str, Any],
    expected_rows: list[dict[str, Any]],
) -> None:
    for index, row in enumerate(rows):
        if index >= len(expected_rows) or row is not expected_rows[index]:
            payload = dict(row)
            payload.pop("row_sha256", None)
            rows[index] = close_row(payload)
    result["ledger"]["row_count"] = len(rows)
    result["ledger"]["row_ids_sha256"] = digest([
        row[
            "Round302C_residual_single_endpoint_sheet_disposition_row_id"
        ]
        for row in rows
    ])
    result["ledger"]["row_hashes_sha256"] = digest([
        row["row_sha256"] for row in rows
    ])
    result["ledger"]["rows_sha256"] = digest(rows)
    result.pop("result_sha256", None)
    result["result_sha256"] = digest(result)


def run_semantic_attacks(
    expected_rows: list[dict[str, Any]],
    expected_result: dict[str, Any],
) -> list[dict[str, Any]]:
    present_index = next(
        index for index, row in enumerate(expected_rows)
        if row["sheet_owner_bulk_already_internal_in_Round266"] is True
    )
    absent_index = next(
        index for index, row in enumerate(expected_rows)
        if row["sheet_owner_bulk_already_internal_in_Round266"] is False
    )
    context_index = next(
        index for index, row in enumerate(expected_rows)
        if row["R300C_owner_bulk_context_witness_count"] == 1
    )
    attacks: list[
        tuple[str, Callable[[list[dict[str, Any]], dict[str, Any]], None]]
    ] = [
        ("forge_R291_physical_candidate",
         lambda r, s: r[0].__setitem__(
             "R291_same_retained_child_and_source_chart_physical_cell_count",
             1)),
        ("forge_R291_graph_candidate",
         lambda r, s: r[0].__setitem__(
             "R291_same_retained_child_and_source_chart_graph_cell_count", 1)),
        ("forge_R295A_binding",
         lambda r, s: r[0].__setitem__(
             "R295A_same_lineage_exact_two_sided_graph_binding_count", 1)),
        ("change_first_failure_ordinal",
         lambda r, s: r[0].__setitem__(
             "earliest_failed_legal_attachment_predicate_ordinal", 2)),
        ("change_first_failure_label",
         lambda r, s: r[0].__setitem__(
             "earliest_failed_legal_attachment_predicate", "FORGED")),
        ("evaluate_later_predicates",
         lambda r, s: r[0].__setitem__(
             "later_legal_attachment_predicates_evaluated", True)),
        ("erase_fail_closed",
         lambda r, s: r[0].__setitem__(
             "later_legal_attachment_predicates_not_reached_fail_closed",
             False)),
        ("forge_R300E_positive",
         lambda r, s: r[0].__setitem__(
             "R300E_positive_owner_attachment_witness_count", 1)),
        ("erase_R300E_absence",
         lambda r, s: r[0].__setitem__(
             "absent_from_complete_Round300E_positive_witness_set", False)),
        ("overlap_R302A_double",
         lambda r, s: r[0].__setitem__(
             "R302A_double_endpoint_exclusion_overlap_count", 1)),
        ("forge_R300C_direct_sheet",
         lambda r, s: r[0].__setitem__(
             "R300C_direct_sheet_positive_volume_witness_count", 1)),
        ("transfer_bulk_context",
         lambda r, s: r[context_index].__setitem__(
             "owner_bulk_witness_transfer_to_sheet_credit", 1)),
        ("reissue_R248_owner_edge",
         lambda r, s: r[0].__setitem__(
             "R248_local_owner_edge_reissued_as_occurrence_attachment_credit",
             1)),
        ("feed_exclusion_to_DSU",
         lambda r, s: r[0].__setitem__(
             "eligible_for_component_DSU_application", True)),
        ("grant_component_edge",
         lambda r, s: r[0].__setitem__("formal_component_edge_credit", 1)),
        ("grant_identity",
         lambda r, s: r[0].__setitem__(
             "formal_occurrence_identity_collapse_credit", 1)),
        ("grant_rank",
         lambda r, s: r[0].__setitem__(
             "formal_DSU_rank_reduction_credit", 1)),
        ("grant_maximality",
         lambda r, s: r[0].__setitem__("formal_maximality_credit", 1)),
        ("grant_fibre",
         lambda r, s: r[0].__setitem__("formal_fibre_credit", 1)),
        ("grant_global_disposition",
         lambda r, s: r[0].__setitem__(
             "formal_global_disposition_credit", 1)),
        ("wrong_R248_hash",
         lambda r, s: r[0].__setitem__(
             "source_Round248_wall_sheet_row_sha256", "0" * 64)),
        ("wrong_retained_child",
         lambda r, s: r[0].__setitem__(
             "Round179_retained_child_row_id", "forged-child")),
        ("wrong_source_chart",
         lambda r, s: r[0].__setitem__("source_chart", "G:FORGED")),
        ("wrong_owner_key",
         lambda r, s: r[0].__setitem__(
             "owner_official_key_id", "forged-key")),
        ("break_present_R266_root",
         lambda r, s: r[present_index].__setitem__(
             "post_Round266_owner_bulk_component_id", "forged-root")),
        ("forge_absent_R266_presence",
         lambda r, s: r[absent_index].__setitem__(
             "Round266_sheet_owner_bulk_presence_status",
             "SHEET_AND_OWNER_BULK_PRESENT_AND_SAME_ROUND266_ROOT")),
        ("break_R300C_context_count",
         lambda r, s: r[context_index].__setitem__(
             "R300C_owner_bulk_context_witness_count", 0)),
        ("drop_sheet", lambda r, s: r.pop()),
        ("duplicate_sheet", lambda r, s: r.append(deepcopy(r[0]))),
        ("claim_result_edge",
         lambda r, s: s["formal_credit_transition"].__setitem__(
             "eligible_component_edge_count", 1)),
        ("claim_result_maximality",
         lambda r, s: s["formal_credit_transition"].__setitem__(
             "formal_maximality_credit", 1)),
        ("claim_unresolved",
         lambda r, s: s["complete_frontier_census"].__setitem__(
             "unresolved_residual_sheet_count", 1)),
        ("erase_complete_partition",
         lambda r, s: s[
             "sealed_attachment_disposition_partition"
         ].__setitem__(
             "complete_sheet_attachment_disposition_frontier", False)),
        ("erase_no_spike_boundary",
         lambda r, s: s["scope_contract"].__setitem__(
             "no_spike_import_execute_or_parse", False)),
    ]
    outcomes: list[dict[str, Any]] = []
    copied_indices = {0, present_index, absent_index, context_index}
    for label, mutate in attacks:
        rows = list(expected_rows)
        for index in copied_indices:
            rows[index] = deepcopy(rows[index])
        result = deepcopy(expected_result)
        mutate(rows, result)
        reseal_attack(rows, result, expected_rows)
        rejected = False
        guard = ""
        try:
            need(rows == expected_rows, "semantic:independent-row-equality")
            need(
                result == expected_result,
                "semantic:independent-result-equality",
            )
        except VerificationError as error:
            rejected = True
            guard = str(error)
        need(rejected, "semantic attack accepted:" + label)
        outcomes.append({
            "attack": label,
            "category": "SEMANTIC_RECLOSED",
            "semantically_reclosed": True,
            "rejected": True,
            "guard": guard,
        })
    return outcomes


def run_boundary_attacks(
    expected_gzip: bytes,
    expected_json: bytes,
) -> list[dict[str, Any]]:
    cases: list[tuple[str, str, Callable[[], None]]] = []

    def json_case(raw: bytes) -> Callable[[], None]:
        return lambda: strict_json_bytes(raw, "attack")

    cases.extend([
        ("json_duplicate_key", "JSON", json_case(b'{"a":1,"a":2}')),
        ("json_float", "JSON", json_case(b'{"a":1.5}')),
        ("json_NaN", "JSON", json_case(b'{"a":NaN}')),
        ("json_NUL", "JSON", json_case(b'{"a":1}\x00')),
        ("json_trailing_token", "JSON", json_case(b'{"a":1}x')),
        ("json_BOM", "JSON", json_case(b'\xef\xbb\xbf{"a":1}')),
        ("json_top_array", "JSON", json_case(b'[]')),
    ])

    def gzip_case(raw: bytes) -> Callable[[], None]:
        return lambda: strict_gzip_candidate(
            raw,
            expected_gzip,
            expected_json,
            "attack",
        )

    alternate = io.BytesIO()
    with gzip.GzipFile(
        filename="alternate",
        mode="wb",
        fileobj=alternate,
        compresslevel=1,
        mtime=1,
    ) as stream:
        stream.write(expected_json)
    cases.extend([
        ("gzip_truncated", "GZIP", gzip_case(expected_gzip[:-1])),
        ("gzip_trailing_byte", "GZIP", gzip_case(expected_gzip + b"x")),
        ("gzip_multi_member", "GZIP",
         gzip_case(expected_gzip + expected_gzip)),
        ("gzip_noncanonical_header_mtime", "GZIP",
         gzip_case(expected_gzip[:4] + b"\x01\x00\x00\x00"
                   + expected_gzip[8:])),
        ("gzip_alternate_filename_and_level", "GZIP",
         gzip_case(alternate.getvalue())),
    ])

    for label, kind in [
        ("path_symlink", "symlink"),
        ("path_hardlink", "hardlink"),
        ("path_directory", "directory"),
        ("path_parent_escape", "escape"),
        ("path_missing", "missing"),
    ]:
        def run_path(kind: str = kind) -> None:
            with tempfile.TemporaryDirectory(
                dir=HERE,
                prefix=".r302c-boundary-",
            ) as outer_name:
                outer = Path(outer_name)
                allowed = outer / "allowed"
                allowed.mkdir()
                source = allowed / "source"
                source.write_bytes(b"x")
                candidate = allowed / "candidate"
                if kind == "symlink":
                    candidate.symlink_to(source.name)
                elif kind == "hardlink":
                    os.link(source, candidate)
                elif kind == "directory":
                    candidate.mkdir()
                elif kind == "escape":
                    candidate = outer / "outside"
                    candidate.write_bytes(b"x")
                else:
                    candidate = allowed / "missing"
                boundary_path_guard(candidate, allowed)
        cases.append((label, "PATH", run_path))

    outcomes: list[dict[str, Any]] = []
    for label, category, action in cases:
        rejected = False
        guard = ""
        try:
            action()
        except (VerificationError, OSError) as error:
            rejected = True
            guard = (
                str(error)
                if isinstance(error, VerificationError)
                else "path:operating-system-rejection"
            )
        need(rejected, "boundary attack accepted:" + label)
        outcomes.append({
            "attack": label,
            "category": category,
            "semantically_reclosed": False,
            "rejected": True,
            "guard": guard,
        })
    return outcomes


def write_json(name: str, value: dict[str, Any]) -> None:
    destination = HERE / name
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{name}.",
        suffix=".incomplete",
        dir=HERE,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(canonical(value))
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, destination)
    finally:
        if temporary.exists():
            temporary.unlink()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", default="302373")
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    need(bool(args.seed), "seed")

    # Rebuild all expected semantics and bytes before opening any candidate.
    expected_rows, expected_result = independent_rebuild()
    expected_ledger = ledger_document(expected_rows)
    expected_ledger_json = canonical(expected_ledger)
    expected_ledger_gzip = gzip_bytes(expected_ledger)
    expected_result_bytes = canonical(expected_result)

    safe_file(HERE / PRODUCER)
    need(
        file_sha256(HERE / PRODUCER) == PRODUCER_SHA256,
        "producer-fixed-byte-pin",
    )
    safe_file(HERE / LEDGER)
    safe_file(HERE / RESULT)
    candidate_ledger_bytes = (HERE / LEDGER).read_bytes()
    candidate_result_bytes = (HERE / RESULT).read_bytes()
    need(
        candidate_ledger_bytes == expected_ledger_gzip,
        "candidate-ledger-exact-bytes",
    )
    need(
        candidate_result_bytes == expected_result_bytes,
        "candidate-result-exact-bytes",
    )
    parsed_ledger = strict_gzip_candidate(
        candidate_ledger_bytes,
        expected_ledger_gzip,
        expected_ledger_json,
        "candidate-ledger",
    )
    candidate_result = strict_json_bytes(
        candidate_result_bytes,
        "candidate-result",
        expected_canonical=expected_result_bytes,
    )
    semantic_audit(
        parsed_ledger["rows"],
        candidate_result,
        expected_rows,
        expected_result,
    )

    semantic_attacks = run_semantic_attacks(
        expected_rows,
        expected_result,
    )
    boundary_attacks = run_boundary_attacks(
        expected_ledger_gzip,
        expected_ledger_json,
    )
    attacks = semantic_attacks + boundary_attacks
    attack_suite = {
        "schema": SCHEMA + ".attack-suite.v1",
        "attack_count": len(attacks),
        "rejected_attack_count": len(attacks),
        "semantic_reclosed_attack_count": len(semantic_attacks),
        "json_attack_count": sum(
            row["category"] == "JSON" for row in boundary_attacks
        ),
        "gzip_attack_count": sum(
            row["category"] == "GZIP" for row in boundary_attacks
        ),
        "path_attack_count": sum(
            row["category"] == "PATH" for row in boundary_attacks
        ),
        "all_attacks_rejected": True,
        "attacks": attacks,
    }
    attack_suite["attack_suite_sha256"] = digest(attack_suite)

    verification = {
        "schema": SCHEMA + ".verification.v1",
        "status":
            "PASS_INDEPENDENT_ROUND302C_EXACT_25336_RESIDUAL_"
            "EARLIEST_P01_DISPOSITIONS__"
            f"{len(attacks)}_OF_{len(attacks)}_ATTACKS_REJECTED",
        "producer_treated_only_as_fixed_byte_string": True,
        "producer_imported_executed_tokenized_or_parsed": False,
        "producer_sha256": PRODUCER_SHA256,
        "verifier_file_sha256": file_sha256(Path(__file__).resolve()),
        "candidate_file_pins": {
            LEDGER: file_sha256(HERE / LEDGER),
            RESULT: file_sha256(HERE / RESULT),
        },
        "independent_reconstruction": {
            "expected_row_count": 25_336,
            "expected_rows_sha256": digest(expected_rows),
            "candidate_exact_bytes_equal": True,
            "complete_R248_R266_R291_R295A_R300C_R300E_R302A_"
            "frontiers_reopened": True,
            "first_failure_histogram": {FIRST_FAILURE: 25_336},
            "R266_present_same_root_count": 25_152,
            "R266_missing_owner_bulk_count": 184,
            "R300C_nontransferable_owner_bulk_context_count": 272,
            "eligible_component_edge_count": 0,
            "unresolved_sheet_count": 0,
        },
        "attack_suite": {
            "filename": ATTACKS,
            "attack_count": len(attacks),
            "rejected_attack_count": len(attacks),
            "semantic_reclosed_attack_count": len(semantic_attacks),
            "json_gzip_path_attack_count": len(boundary_attacks),
            "attack_suite_sha256": attack_suite["attack_suite_sha256"],
            "attack_suite_file_sha256":
                hashlib.sha256(canonical(attack_suite)).hexdigest(),
        },
        "seed_affects_output": False,
    }
    verification["verification_sha256"] = digest(verification)
    if not args.no_write:
        write_json(ATTACKS, attack_suite)
        write_json(VERIFICATION, verification)
    print(canonical({
        "status": verification["status"],
        "verification_sha256": verification["verification_sha256"],
        "attack_suite_sha256": attack_suite["attack_suite_sha256"],
        "artifact_written": not args.no_write,
        "seed_affects_output": False,
    }).decode("utf-8"))


if __name__ == "__main__":
    main()
