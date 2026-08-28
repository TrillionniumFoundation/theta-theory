#!/usr/bin/env python3
"""Promote exact positive-volume virtual/new-occurrence component edges.

This round has deliberately narrow scope.  It reconstructs retained
Round248 wall-bulk carriers and the positive 3D witness boxes of inherited
Round245--247 virtual strata, then intersects those supports with the formal
Round294 new-occurrence supports.  Every comparison is grouped by the full
ten-field return-signature commitment and rechecked with exact arithmetic.

The output grants component-edge witness credit only.  It does not claim a
complete virtual frontier, a quotient, maximality, fibre exhaustion, or a
global disposition.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction as Q
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
PREFIX = (
    "cm2_round300c_source_g_virtual_stratum_new_occurrence_"
    "positive_volume_edge_promotion"
)
WITNESS_LEDGER = HERE / f"{PREFIX}_witness_ledger.json.gz"
EDGE_LEDGER = HERE / f"{PREFIX}_edge_ledger.json.gz"
RESULT = HERE / f"{PREFIX}_result.json"

SCHEMA = (
    "cm2.round300c.source-g-virtual-stratum-new-occurrence-"
    "positive-volume-edge-promotion.v1"
)
WITNESS_SCHEMA = SCHEMA + ".witness-ledger.v1"
EDGE_SCHEMA = SCHEMA + ".edge-ledger.v1"

FILES = {
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
    "R236": (
        "cm2_round236_source_g_wall_residual_closure_and_root_key_"
        "partition_certificate.json",
        "b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217",
    ),
    "R245": (
        "cm2_round245_source_g_retained_graph_mixed_sheet_"
        "quotient_certificate.json",
        "c76662f7cb068127f3612a3655ae720662eead9b9210b5757d771693149883c1",
    ),
    "R246": (
        "cm2_round246_source_g_whole_signature_retained_"
        "quotient_certificate.json",
        "a448359c0a9b4495e54afe6e2d860c20fb222684bae46ee108574782a5a33bc9",
    ),
    "R247": (
        "cm2_round247_source_g_crossing_and_source_seam_retained_"
        "quotient_certificate.json",
        "72188f5d99a220f44698f3023dd606633b364adbd02d5e20e5d4fa0ff6e1b2c7",
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
    "R287": (
        "cm2_round287_source_g_rechart_terminal_occurrence_"
        "disposition_probe_ledger.json.gz",
        "29838e3e6b33f03bf623bbce8b87e6ba5c3306e66beb0b6634496503fb9a4f9a",
    ),
    "R294": (
        "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
        "registry_ledger.json.gz",
        "c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb",
    ),
    "R299A": (
        "cm2_round299a_source_g_refined_occurrence_official_key_"
        "binding_closure_ledger.json.gz",
        "ffea8120af2179990d5c9e7ff385193e2c5a08bed161cf5b570aa28b1f8b1ee0",
    ),
}

TABLES = {
    "R245": (
        3_664,
        "retained_stratum_node_id",
        "ef81a9a7d264961541edfb9ba9e8e4c37ddbf7dea01efa3eb72d500a82b44ed5",
        "86bad0d45642388bcac65633d47088b93184d77abdb2be68096cb139e192110c",
    ),
    "R246": (
        2_220,
        "retained_stratum_node_id",
        "488711dda41780ef47dbe34834ab8e3a41995a471260d7743b562c0190b6c86f",
        "f43d31209c552f275144ede960e49bd1ee4044cb40ee3050340e23d6d38bc671",
    ),
    "R247": (
        504,
        "retained_stratum_node_id",
        "8896ff95e8e1c4dd5eb7f53ce3dcf9f39abbcd883c2641846b69129fc7040143",
        "23e3495f9f481cc3f1d037741b27403d7bc4c0be8afe118201ba52a6fc4ce9a7",
    ),
    "R248": (
        88_936,
        "wall_bulk_node_id",
        "6106c39894a7947293934b0b061bcae04e1a2902976b63ccd1756d7790cb6154",
        "e46f242e15bcba4111e14aac3c1dc5d82a5350e9e1514f2b9f90cdbc853e525d",
    ),
    "R266": (
        133_284,
        "post_Round266_valid_virtual_node_frontier_row_id",
        "2d42533f48f864f01e6bd4a46470e7266c1a2cec590380483cfb7cbfb84634f2",
        "9c31ba929e13eeaea29a9f6abe7cf324222eacb25d123a9b12252b386c12a32e",
    ),
    "R294": (
        431_208,
        "Round294_occurrence_registry_row_id",
        "bbaca3ecbb804a87fd509aac2b8bd9f505d0c008e7bddbeb1a2ecb2a966f5509",
        "ea98de3dab7e6f308f5a07d04bc29ca0d9dcd265a5323d8ecdb728cc501eed56",
    ),
    "R299A": (
        9_404,
        "Round299A_refined_occurrence_official_key_binding_row_id",
        "a3786265b52feafd316cc81c71ab05ee32976b5ff7f1de091853d34a7b33e6e3",
        "65e6f22b9085685b20a50dedfcb62cd08dd01e1ea70a61ee850d74450402b333",
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
    row = dict(payload)
    row["row_sha256"] = digest(payload)
    return row


def verify_row(row: dict[str, Any], label: str) -> None:
    payload = {key: value for key, value in row.items() if key != "row_sha256"}
    need(
        set(row) == set(payload) | {"row_sha256"}
        and row["row_sha256"] == digest(payload),
        label + ":row closure",
    )


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


def closed_result(filename: str) -> dict[str, Any]:
    with (HERE / filename).open("rb") as stream:
        document = json.load(stream)
    need(
        set(document) == {"schema", "result", "result_sha256"}
        and digest(document["result"]) == document["result_sha256"],
        "closed result:" + filename,
    )
    return document["result"]


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


def stream_gzip_rows(filename: str) -> Iterator[dict[str, Any]]:
    with gzip.open(HERE / filename, "rt", encoding="utf-8") as stream:
        buffer = ""
        while '"rows":[' not in buffer:
            piece = stream.read(1 << 20)
            need(bool(piece), "gzip rows marker:" + filename)
            buffer += piece
        buffer = buffer.split('"rows":[', 1)[1]
        decoder = json.JSONDecoder()
        while True:
            buffer = buffer.lstrip()
            if not buffer:
                piece = stream.read(1 << 20)
                need(bool(piece), "unexpected gzip EOF:" + filename)
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
                need(bool(piece), "malformed gzip row:" + filename)
                buffer += piece
                continue
            need(type(row) is dict, "gzip row object:" + filename)
            yield row
            buffer = buffer[end:]


def audited(rows: Iterable[dict[str, Any]], table: str) -> Iterator[dict[str, Any]]:
    expected_count, id_field, expected_ids, expected_hashes = TABLES[table]
    ids = ListHasher()
    hashes = ListHasher()
    seen: set[str] = set()
    for row in rows:
        verify_row(row, table)
        row_id = row[id_field]
        need(row_id not in seen, table + ":duplicate row ID")
        seen.add(row_id)
        ids.add(row_id)
        hashes.add(row["row_sha256"])
        yield row
    need(
        len(seen) == expected_count
        and ids.count == hashes.count == expected_count
        and ids.finish() == expected_ids
        and hashes.finish() == expected_hashes,
        table + ":complete table commitment",
    )


def qstr(value: Q) -> str:
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


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


def box_text(box: tuple[Q, Q, Q, Q, Q, Q]) -> list[str]:
    return [qstr(value) for value in box]


def box_volume(box: tuple[Q, Q, Q, Q, Q, Q]) -> Q:
    return (
        (box[1] - box[0])
        * (box[3] - box[2])
        * (box[5] - box[4])
    )


def intersection(
    left: tuple[Q, Q, Q, Q, Q, Q],
    right: tuple[Q, Q, Q, Q, Q, Q],
) -> tuple[Q, Q, Q, Q, Q, Q] | None:
    values: list[Q] = []
    for axis in range(3):
        lower = max(left[2 * axis], right[2 * axis])
        upper = min(left[2 * axis + 1], right[2 * axis + 1])
        if lower >= upper:
            return None
        values.extend((lower, upper))
    return tuple(values)  # type: ignore[return-value]


def transformed_intersection(
    *,
    sign: int,
    cell: tuple[Q, Q, Q, Q, Q, Q],
    carrier: tuple[Q, Q, Q, Q, Q, Q],
) -> tuple[Q, Q, Q, Q, Q, Q] | None:
    need(sign in {-1, 1}, "physical t sign")
    p0 = max(cell[2], carrier[2])
    p1 = min(cell[3], carrier[3])
    s0 = max(cell[4], carrier[4])
    s1 = min(cell[5], carrier[5])
    if p0 >= p1 or s0 >= s1:
        return None
    if sign == 1:
        if carrier[1] <= 0:
            return None
        carrier_t2_lower = max(carrier[0], Q(0)) ** 2
        carrier_t2_upper = carrier[1] ** 2
    else:
        if carrier[0] >= 0:
            return None
        carrier_t2_lower = min(carrier[1], Q(0)) ** 2
        carrier_t2_upper = carrier[0] ** 2
    t0 = max(cell[0], carrier_t2_lower)
    t1 = min(cell[1], carrier_t2_upper)
    if t0 >= t1:
        return None
    return (t0, t1, p0, p1, s0, s1)


@dataclass(frozen=True, slots=True)
class Virtual:
    root_id: str
    frontier_row_id: str
    frontier_row_sha256: str
    kind: str
    official_key_id: str


@dataclass(frozen=True, slots=True)
class Piece:
    node_id: str
    virtual: Virtual
    signature_sha256: str
    official_key_id: str
    official_key_ordinal: int
    box: tuple[Q, Q, Q, Q, Q, Q]
    source_class: str
    source_row_id: str
    source_row_sha256: str
    carrier_proof: str


@dataclass(slots=True)
class IntervalNode:
    center: Q
    crossing_lower: list[Piece]
    crossing_upper_desc: list[Piece]
    left: "IntervalNode | None"
    right: "IntervalNode | None"
    axis: int


def build_tree(rows: list[Piece], axis: int) -> IntervalNode | None:
    if not rows:
        return None
    centers = sorted(
        (row.box[2 * axis] + row.box[2 * axis + 1]) / 2
        for row in rows
    )
    center = centers[len(centers) // 2]
    left: list[Piece] = []
    right: list[Piece] = []
    crossing: list[Piece] = []
    for row in rows:
        if row.box[2 * axis + 1] <= center:
            left.append(row)
        elif row.box[2 * axis] >= center:
            right.append(row)
        else:
            crossing.append(row)
    need(bool(crossing), "interval-tree pivot")
    return IntervalNode(
        center=center,
        crossing_lower=sorted(
            crossing, key=lambda row: (row.box[2 * axis], row.node_id)
        ),
        crossing_upper_desc=sorted(
            crossing,
            key=lambda row: (row.box[2 * axis + 1], row.node_id),
            reverse=True,
        ),
        left=build_tree(left, axis),
        right=build_tree(right, axis),
        axis=axis,
    )


def query_tree(
    node: IntervalNode | None,
    lower: Q,
    upper: Q,
) -> Iterator[Piece]:
    if node is None:
        return
    axis = node.axis
    if upper <= node.center:
        for row in node.crossing_lower:
            if row.box[2 * axis] >= upper:
                break
            yield row
        yield from query_tree(node.left, lower, upper)
    elif lower >= node.center:
        for row in node.crossing_upper_desc:
            if row.box[2 * axis + 1] <= lower:
                break
            yield row
        yield from query_tree(node.right, lower, upper)
    else:
        yield from node.crossing_lower
        yield from query_tree(node.left, lower, upper)
        yield from query_tree(node.right, lower, upper)


def load_virtuals() -> dict[str, Virtual]:
    result: dict[str, Virtual] = {}
    kinds: Counter[str] = Counter()
    filename = FILES["R266"][0]
    rows = stream_table(
        filename, "formal_post_Round266_valid_virtual_node_frontier_ledger"
    )
    for row in audited(rows, "R266"):
        node_id = row["valid_virtual_stratum_node_id"]
        need(node_id not in result, "unique valid virtual node")
        item = Virtual(
            root_id=row["post_Round266_quotient_component_id"],
            frontier_row_id=row[
                "post_Round266_valid_virtual_node_frontier_row_id"
            ],
            frontier_row_sha256=row["row_sha256"],
            kind=row["virtual_node_kind"],
            official_key_id=row["official_key_id"],
        )
        result[node_id] = item
        kinds[item.kind] += 1
    need(
        kinds
        == {
            "INHERITED_ROUND247_VIRTUAL_STRATUM": 6_388,
            "ROUND248_WALL_BULK": 88_536,
            "ROUND248_WALL_SHEET": 38_360,
        },
        "complete virtual kind census",
    )
    return result


def load_pieces(
    virtuals: dict[str, Virtual],
) -> tuple[dict[str, list[Piece]], dict[str, Any]]:
    r234 = closed_result(FILES["R234"][0])
    r235 = closed_result(FILES["R235"][0])
    r236 = closed_result(FILES["R236"][0])
    frontiers = {
        row["frontier_row_id"]: row for row in r234["depth6_frontier_rows"]
    }
    resolved = {
        row["materialized_row_id"]: row
        for row in r234["resolved_descendant_rows"]
    }
    single = {
        row["endpoint_graph_partition_row_id"]: row
        for row in r235["single_endpoint_graph_partition_rows"]
    }
    double = {
        row["double_endpoint_partition_row_id"]: row
        for row in r236["double_endpoint_partition_rows"]
    }
    crossing = {
        row["crossing_dependency_discharge_row_id"]: row
        for row in r236["crossing_dependency_discharge_rows"]
    }
    need(
        len(frontiers) == 38_376
        and len(resolved) == 12_200
        and len(single) == 38_328
        and len(double) == 16
        and len(crossing) == 32,
        "wall carrier source census",
    )

    groups: dict[str, list[Piece]] = defaultdict(list)
    source_histogram: Counter[str] = Counter()
    retained_wall = 0
    dropped_wall = 0
    filename = FILES["R248"][0]
    for row in audited(
        stream_table(filename, "formal_wall_positive_volume_bulk_ledger"),
        "R248",
    ):
        node_id = row["wall_bulk_node_id"]
        if node_id not in virtuals:
            dropped_wall += 1
            continue
        source_class = row["source_partition_kind"]
        source_id = row["source_partition_row_id"]
        if source_class == "ROUND234_RESOLVED_DESCENDANT":
            source = resolved[source_id]
            signature = source["local_return_signature"]
            carrier = qbox(row["exact_positive_3D_box"])
            proof = "EXACT_ROUND234_DYADIC_BOX_AND_SIGNATURE"
        elif source_class == "ROUND235_SINGLE_ENDPOINT_GRAPH_BRANCH":
            source = single[source_id]
            field = (
                "event_absent_signature"
                if row["branch_label"] == "EVENT_ABSENT"
                else "event_present_signature"
            )
            signature = source[field]
            carrier = qbox(
                frontiers[source["Round234_frontier_row_id"]]["box"]
            )
            proof = (
                "ROUND235_CARRIER_BOX_INTERSECTION_PLUS_"
                "EXACT_BRANCH_SIGNATURE"
            )
        elif source_class == "ROUND236_DOUBLE_ENDPOINT_ARRANGEMENT_BRANCH":
            source = double[source_id]
            field = {
                "SAME_SIGN_EVENT_ABSENT":
                    "same_sign_event_absent_signature",
                "NEGATIVE_TO_POSITIVE": "negative_to_positive_signature",
                "POSITIVE_TO_NEGATIVE": "positive_to_negative_signature",
            }[row["branch_label"]]
            signature = source[field]
            carrier = qbox(
                frontiers[source["Round234_frontier_row_id"]]["box"]
            )
            proof = (
                "ROUND236_CARRIER_BOX_INTERSECTION_PLUS_"
                "EXACT_BRANCH_SIGNATURE"
            )
        else:
            need(
                source_class == "ROUND236_CROSSING_DISCHARGE_BULK",
                "known wall source class",
            )
            source = crossing[source_id]
            signature = source["local_return_signature"]
            carrier = qbox(row["exact_positive_3D_box"])
            proof = "EXACT_ROUND236_CROSSING_DISCHARGE_BOX_AND_SIGNATURE"
        signature_sha256 = digest(signature)
        virtual = virtuals[node_id]
        need(
            signature_sha256 == row["local_return_signature_sha256"]
            and signature["official_key_id"] == row["official_key_id"]
            == virtual.official_key_id,
            "wall signature/key/virtual join",
        )
        groups[signature_sha256].append(
            Piece(
                node_id=node_id,
                virtual=virtual,
                signature_sha256=signature_sha256,
                official_key_id=signature["official_key_id"],
                official_key_ordinal=signature["official_key_ordinal"],
                box=carrier,
                source_class=source_class,
                source_row_id=source_id,
                source_row_sha256=row["row_sha256"],
                carrier_proof=proof,
            )
        )
        source_histogram[source_class] += 1
        retained_wall += 1
    need((retained_wall, dropped_wall) == (88_536, 400), "wall retention")

    inherited_specifications = (
        (
            "R245",
            "formal_retained_stratum_node_ledger",
            "strict_positive_3D_witness_box",
        ),
        (
            "R246",
            "formal_new_whole_signature_retained_stratum_node_ledger",
            "strict_positive_3D_witness_box",
        ),
        (
            "R247",
            "formal_new_crossing_and_source_seam_retained_stratum_node_ledger",
            "strict_positive_3D_physical_witness_box",
        ),
    )
    inherited_3d: Counter[str] = Counter()
    withheld_2d: Counter[str] = Counter()
    for round_name, table, box_field in inherited_specifications:
        filename = FILES[round_name][0]
        for row in audited(stream_table(filename, table), round_name):
            node_id = row["retained_stratum_node_id"]
            need(node_id in virtuals, "inherited virtual frontier join")
            box_value = row[box_field]
            if box_value is None:
                need(row["local_dimension"] == 2, "withheld inherited 2D")
                withheld_2d[round_name] += 1
                continue
            need(row["local_dimension"] == 3, "inherited positive 3D")
            signature = row["local_return_signature"]
            signature_sha256 = digest(signature)
            virtual = virtuals[node_id]
            need(
                signature["official_key_id"] == virtual.official_key_id,
                "inherited signature/key/virtual join",
            )
            source_class = round_name + "::" + row["stratum_kind"]
            groups[signature_sha256].append(
                Piece(
                    node_id=node_id,
                    virtual=virtual,
                    signature_sha256=signature_sha256,
                    official_key_id=signature["official_key_id"],
                    official_key_ordinal=signature["official_key_ordinal"],
                    box=qbox(box_value),
                    source_class=source_class,
                    source_row_id=row["retained_stratum_node_id"],
                    source_row_sha256=row["row_sha256"],
                    carrier_proof=(
                        "EXACT_INHERITED_STRICT_POSITIVE_3D_WITNESS_BOX"
                    ),
                )
            )
            source_histogram[source_class] += 1
            inherited_3d[round_name] += 1
    need(
        inherited_3d == {"R245": 3_400, "R246": 2_220, "R247": 504}
        and withheld_2d == {"R245": 264},
        "inherited witness census",
    )
    for rows in groups.values():
        rows.sort(key=lambda row: row.node_id)
    scope = {
        "retained_Round248_wall_bulk_count": retained_wall,
        "Round264_dropped_empty_wall_bulk_count": dropped_wall,
        "inherited_positive_3D_witness_count": sum(inherited_3d.values()),
        "withheld_inherited_2D_sheet_count": sum(withheld_2d.values()),
        "withheld_Round248_wall_sheet_count": 38_360,
        "signature_group_count": len(groups),
        "piece_histogram": dict(sorted(source_histogram.items())),
    }
    return groups, scope


def load_key_bindings() -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    filename = FILES["R299A"][0]
    for row in audited(stream_gzip_rows(filename), "R299A"):
        occurrence_id = row["registry_occurrence_id"]
        need(occurrence_id not in result, "unique refined key binding")
        result[occurrence_id] = {
            "official_key_id": row["official_key_id"],
            "official_key_ordinal": row["official_key_ordinal"],
            "binding_row_id":
                row["Round299A_refined_occurrence_official_key_binding_row_id"],
            "binding_row_sha256": row["row_sha256"],
        }
    need(len(result) == 9_404, "complete refined key binding")
    return result


def load_r287_signs() -> tuple[dict[str, int], dict[str, int], dict[str, str]]:
    filename = FILES["R287"][0]
    with gzip.open(HERE / filename, "rt", encoding="utf-8") as stream:
        document = json.load(stream)
    need(
        document["schema"]
        == "cm2.round287.source-g-rechart-terminal-occurrence-disposition.ledger.v1",
        "Round287 schema",
    )
    for field, count_field, sha_field in (
        ("region_rows", "region_row_count", "region_rows_sha256"),
        (
            "refinement_cell_rows",
            "refinement_cell_row_count",
            "refinement_cell_rows_sha256",
        ),
        (
            "potential_new_support_union_rows",
            "potential_new_support_union_row_count",
            "potential_new_support_union_rows_sha256",
        ),
    ):
        rows = document[field]
        need(
            len(rows) == document[count_field]
            and digest(rows) == document[sha_field],
            "Round287 list commitment:" + field,
        )
        for row in rows:
            verify_row(row, "Round287:" + field)
    region_sign = {
        row["Round275_region_id"]: row["physical_t_sign"]
        for row in document["region_rows"]
    }
    cell_sign = {
        row["Round286_refinement_cell_id"]: row["physical_t_sign"]
        for row in document["refinement_cell_rows"]
    }
    cell_hash = {
        row["Round286_refinement_cell_id"]: row["row_sha256"]
        for row in document["refinement_cell_rows"]
    }
    need(
        len(region_sign) == 13_788 and len(cell_sign) == len(cell_hash) == 7_616,
        "Round287 sign census",
    )
    return region_sign, cell_sign, cell_hash


def build_witnesses(
    pieces: dict[str, list[Piece]],
    refined_keys: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    region_sign, cell_sign, cell_hash = load_r287_signs()
    trees_t = {
        signature: build_tree(rows, axis=0)
        for signature, rows in pieces.items()
    }
    trees_p = {
        signature: build_tree(rows, axis=1)
        for signature, rows in pieces.items()
    }
    witnesses: list[dict[str, Any]] = []
    comparisons = Counter()
    occurrence_kinds: Counter[str] = Counter()
    incident_occurrences: set[str] = set()
    source_histogram: Counter[str] = Counter()
    filename = FILES["R294"][0]
    for row in audited(stream_gzip_rows(filename), "R294"):
        kind = row["registry_entry_kind"]
        occurrence_kinds[kind] += 1
        if kind == "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE":
            continue
        occurrence_id = row["registry_occurrence_id"]
        signature = row["complete_10_field_return_signature_sha256"]
        if kind == "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM":
            official_key_id = row["official_key_id"]
            official_key_ordinal = row["official_key_ordinal"]
            occurrence_box = qbox(
                row["positive_volume_rational_inner_support_box"]
            )
            for piece in query_tree(
                trees_t.get(signature), occurrence_box[0], occurrence_box[1]
            ):
                comparisons["ROUND288_RATIONAL"] += 1
                overlap = intersection(piece.box, occurrence_box)
                if overlap is None:
                    continue
                need(
                    piece.official_key_id == official_key_id
                    and piece.official_key_ordinal == official_key_ordinal,
                    "Round288 overlap exact key",
                )
                payload = {
                    "witness_class": "ROUND288_RATIONAL_INNER_BOX_OVERLAP",
                    "virtual_stratum_node_id": piece.node_id,
                    "post_Round266_quotient_component_id":
                        piece.virtual.root_id,
                    "source_Round266_virtual_frontier_row_id":
                        piece.virtual.frontier_row_id,
                    "source_Round266_virtual_frontier_row_sha256":
                        piece.virtual.frontier_row_sha256,
                    "virtual_node_kind": piece.virtual.kind,
                    "virtual_piece_source_class": piece.source_class,
                    "virtual_piece_source_row_id": piece.source_row_id,
                    "virtual_piece_source_row_sha256":
                        piece.source_row_sha256,
                    "virtual_piece_carrier_proof": piece.carrier_proof,
                    "virtual_piece_carrier_box": box_text(piece.box),
                    "Round294_registry_occurrence_id": occurrence_id,
                    "source_Round294_registry_row_id":
                        row["Round294_occurrence_registry_row_id"],
                    "source_Round294_registry_row_sha256": row["row_sha256"],
                    "Round294_registry_entry_kind": kind,
                    "occurrence_positive_rational_inner_support_box":
                        box_text(occurrence_box),
                    "complete_10_field_return_signature_sha256": signature,
                    "official_key_id": official_key_id,
                    "official_key_ordinal": official_key_ordinal,
                    "exact_intersection_coordinate_system": "(t,p,s)",
                    "exact_positive_intersection_box": box_text(overlap),
                    "exact_positive_intersection_volume":
                        qstr(box_volume(overlap)),
                    "same_complete_signature_required": True,
                    "same_official_key_required": True,
                    "positive_volume_physical_overlap": True,
                }
                witness_id = (
                    "round300c-virtual-occurrence-positive-volume-witness:"
                    + digest(payload)
                )
                witnesses.append(closed({
                    "Round300C_virtual_occurrence_positive_volume_witness_row_id":
                        witness_id,
                    **payload,
                }))
                incident_occurrences.add(occurrence_id)
                source_histogram[piece.source_class] += 1
            continue

        need(
            kind
            == "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT",
            "known registry kind",
        )
        binding = refined_keys[occurrence_id]
        need(
            binding["official_key_id"] is not None
            and row["official_key_id"] is None,
            "Round299A refined key completion",
        )
        for cell in row["member_refinement_cells"]:
            transformed = qbox(cell["exact_transformed_open_cell"])
            source_cell_id = cell["source_Round287_support_cell_id"]
            if source_cell_id.startswith("WHOLE:"):
                sign = region_sign[cell["Round275_region_id"]]
                source_cell_sha256 = cell["source_row_sha256"]
            else:
                sign = cell_sign[source_cell_id]
                source_cell_sha256 = cell_hash[source_cell_id]
            for piece in query_tree(
                trees_p.get(signature), transformed[2], transformed[3]
            ):
                comparisons["ROUND292_TRANSFORMED"] += 1
                overlap = transformed_intersection(
                    sign=sign, cell=transformed, carrier=piece.box
                )
                if overlap is None:
                    continue
                need(
                    piece.official_key_id == binding["official_key_id"]
                    and piece.official_key_ordinal
                    == binding["official_key_ordinal"],
                    "Round292 overlap exact key",
                )
                payload = {
                    "witness_class":
                        "ROUND292_EXACT_TRANSFORMED_CELL_OVERLAP",
                    "virtual_stratum_node_id": piece.node_id,
                    "post_Round266_quotient_component_id":
                        piece.virtual.root_id,
                    "source_Round266_virtual_frontier_row_id":
                        piece.virtual.frontier_row_id,
                    "source_Round266_virtual_frontier_row_sha256":
                        piece.virtual.frontier_row_sha256,
                    "virtual_node_kind": piece.virtual.kind,
                    "virtual_piece_source_class": piece.source_class,
                    "virtual_piece_source_row_id": piece.source_row_id,
                    "virtual_piece_source_row_sha256":
                        piece.source_row_sha256,
                    "virtual_piece_carrier_proof": piece.carrier_proof,
                    "virtual_piece_carrier_box": box_text(piece.box),
                    "Round294_registry_occurrence_id": occurrence_id,
                    "source_Round294_registry_row_id":
                        row["Round294_occurrence_registry_row_id"],
                    "source_Round294_registry_row_sha256": row["row_sha256"],
                    "Round294_registry_entry_kind": kind,
                    "source_Round287_support_cell_id": source_cell_id,
                    "source_Round287_support_cell_row_sha256":
                        source_cell_sha256,
                    "Round292_refinement_cell_id":
                        cell["Round292_refinement_cell_id"],
                    "Round275_region_id": cell["Round275_region_id"],
                    "physical_t_sign": sign,
                    "occurrence_exact_transformed_open_cell":
                        box_text(transformed),
                    "complete_10_field_return_signature_sha256": signature,
                    "official_key_id": binding["official_key_id"],
                    "official_key_ordinal": binding["official_key_ordinal"],
                    "source_Round299A_key_binding_row_id":
                        binding["binding_row_id"],
                    "source_Round299A_key_binding_row_sha256":
                        binding["binding_row_sha256"],
                    "exact_intersection_coordinate_system": "(t^2,p,s)",
                    "exact_positive_intersection_box": box_text(overlap),
                    "exact_positive_intersection_volume":
                        qstr(box_volume(overlap)),
                    "same_complete_signature_required": True,
                    "same_official_key_required": True,
                    "positive_volume_physical_overlap": True,
                }
                witness_id = (
                    "round300c-virtual-occurrence-positive-volume-witness:"
                    + digest(payload)
                )
                witnesses.append(closed({
                    "Round300C_virtual_occurrence_positive_volume_witness_row_id":
                        witness_id,
                    **payload,
                }))
                incident_occurrences.add(occurrence_id)
                source_histogram[piece.source_class] += 1
    need(
        occurrence_kinds
        == {
            "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE": 126_468,
            "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM": 295_336,
            "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT": 9_404,
        },
        "complete registry tranche census",
    )
    witnesses.sort(
        key=lambda row: row[
            "Round300C_virtual_occurrence_positive_volume_witness_row_id"
        ]
    )
    witness_ids = [
        row["Round300C_virtual_occurrence_positive_volume_witness_row_id"]
        for row in witnesses
    ]
    need(
        len(witnesses) == len(set(witness_ids)) == 6_322
        and len(incident_occurrences) == 6_314
        and comparisons
        == {"ROUND288_RATIONAL": 229_663, "ROUND292_TRANSFORMED": 1_840},
        "positive-volume witness census",
    )
    return witnesses, {
        "exact_candidate_comparison_histogram": dict(sorted(comparisons.items())),
        "incident_new_occurrence_count": len(incident_occurrences),
        "nonincident_new_occurrence_count":
            304_740 - len(incident_occurrences),
        "witness_histogram_by_virtual_piece_source":
            dict(sorted(source_histogram.items())),
    }


def build_edges(
    witnesses: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    roots_by_occurrence: dict[str, set[str]] = defaultdict(set)
    for witness in witnesses:
        root = witness["post_Round266_quotient_component_id"]
        occurrence = witness["Round294_registry_occurrence_id"]
        grouped[(root, occurrence)].append(witness)
        roots_by_occurrence[occurrence].add(root)
    need(
        len(grouped) == len(roots_by_occurrence) == 6_314
        and all(len(roots) == 1 for roots in roots_by_occurrence.values()),
        "one exact virtual root per incident occurrence",
    )
    edges: list[dict[str, Any]] = []
    multiplicity: Counter[int] = Counter()
    for (root, occurrence), rows in sorted(grouped.items()):
        rows.sort(
            key=lambda row: row[
                "Round300C_virtual_occurrence_positive_volume_witness_row_id"
            ]
        )
        keys = {row["official_key_id"] for row in rows}
        ordinals = {row["official_key_ordinal"] for row in rows}
        signatures = {
            row["complete_10_field_return_signature_sha256"] for row in rows
        }
        need(
            len(keys) == len(ordinals) == len(signatures) == 1,
            "edge witness signature/key agreement",
        )
        witness_ids = [
            row["Round300C_virtual_occurrence_positive_volume_witness_row_id"]
            for row in rows
        ]
        witness_hashes = [row["row_sha256"] for row in rows]
        multiplicity[len(rows)] += 1
        payload = {
            "post_Round266_quotient_component_id": root,
            "Round294_registry_occurrence_id": occurrence,
            "canonical_component_edge_endpoint_pair": [root, occurrence],
            "positive_volume_witness_count": len(rows),
            "positive_volume_witness_row_ids": witness_ids,
            "positive_volume_witness_row_ids_sha256": digest(witness_ids),
            "positive_volume_witness_row_hashes_sha256":
                digest(witness_hashes),
            "complete_10_field_return_signature_sha256": next(iter(signatures)),
            "official_key_id": next(iter(keys)),
            "official_key_ordinal": next(iter(ordinals)),
            "edge_semantics":
                "EXACT_POSITIVE_VOLUME_PHYSICAL_OVERLAP__"
                "COMPONENT_CONNECTIVITY_NOT_OCCURRENCE_IDENTITY",
            "formal_positive_volume_component_edge_witness_credit": 1,
            "formal_occurrence_identity_collapse_credit": 0,
            "formal_occurrence_alias_credit": 0,
            "formal_new_occurrence_ID_credit": 0,
            "formal_component_union_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
            "post_Round300C_quotient_component_id": None,
        }
        edge_id = (
            "round300c-virtual-occurrence-positive-volume-edge:"
            + digest(payload)
        )
        edges.append(closed({
            "Round300C_virtual_occurrence_positive_volume_edge_row_id":
                edge_id,
            **payload,
        }))
    edges.sort(
        key=lambda row: row[
            "Round300C_virtual_occurrence_positive_volume_edge_row_id"
        ]
    )
    edge_ids = [
        row["Round300C_virtual_occurrence_positive_volume_edge_row_id"]
        for row in edges
    ]
    need(
        len(edges) == len(set(edge_ids)) == 6_314
        and multiplicity == {1: 6_306, 2: 8},
        "canonical edge census",
    )
    return edges, {
        "canonical_root_occurrence_edge_count": len(edges),
        "edge_witness_multiplicity_histogram": {
            str(key): value for key, value in sorted(multiplicity.items())
        },
        "occurrence_identity_collapse_count": 0,
        "formal_DSU_rank_reduction_credit": 0,
    }


def ledger(
    rows: list[dict[str, Any]],
    *,
    schema: str,
    id_field: str,
    status: str,
) -> dict[str, Any]:
    ids = [row[id_field] for row in rows]
    need(len(ids) == len(set(ids)), "unique output IDs:" + id_field)
    return {
        "schema": schema,
        "status": status,
        "row_count": len(rows),
        "row_ids_sha256": digest(ids),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "rows_sha256": digest(rows),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }


def ledger_summary(
    value: dict[str, Any],
    filename: str,
) -> dict[str, Any]:
    return {
        "filename": filename,
        **{
            field: value[field]
            for field in (
                "schema",
                "row_count",
                "row_ids_sha256",
                "row_hashes_sha256",
                "rows_sha256",
            )
        },
    }


def build(producer_sha256: str) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    for filename, sha256 in FILES.values():
        guard_input(filename, sha256)
    virtuals = load_virtuals()
    pieces, scope = load_pieces(virtuals)
    refined_keys = load_key_bindings()
    witnesses, witness_audit = build_witnesses(pieces, refined_keys)
    edges, edge_audit = build_edges(witnesses)
    witness_ledger = ledger(
        witnesses,
        schema=WITNESS_SCHEMA,
        id_field=(
            "Round300C_virtual_occurrence_positive_volume_witness_row_id"
        ),
        status=(
            "FORMAL_6322_EXACT_POSITIVE_VOLUME_VIRTUAL_OCCURRENCE_WITNESSES__"
            "NO_FRONTIER_EXHAUSTION_CLAIM"
        ),
    )
    edge_ledger = ledger(
        edges,
        schema=EDGE_SCHEMA,
        id_field=(
            "Round300C_virtual_occurrence_positive_volume_edge_row_id"
        ),
        status=(
            "FORMAL_6314_CANONICAL_ROOT_OCCURRENCE_COMPONENT_EDGES__"
            "NO_QUOTIENT_OR_MAXIMALITY_CREDIT"
        ),
    )
    payload = {
        "schema": SCHEMA,
        "status": (
            "PASS_ROUND300C_EXACT_POSITIVE_VOLUME_EDGE_PROMOTION__"
            "6322_WITNESSES__6314_CANONICAL_EDGES__"
            "SCOPE_REMAINS_NONEXHAUSTIVE"
        ),
        "producer_file_sha256": producer_sha256,
        "input_file_pins": {
            filename: sha256 for filename, sha256 in sorted(FILES.values())
        },
        "scope": scope,
        "witness_audit": witness_audit,
        "edge_audit": edge_audit,
        "witness_ledger": ledger_summary(
            witness_ledger, WITNESS_LEDGER.name
        ),
        "edge_ledger": ledger_summary(edge_ledger, EDGE_LEDGER.name),
        "strict_nonpromotion": {
            "complete_virtual_new_occurrence_frontier_claimed": False,
            "withheld_Round248_wall_sheet_count": 38_360,
            "withheld_inherited_2D_sheet_count": 264,
            "nonincident_new_occurrence_count":
                witness_audit["nonincident_new_occurrence_count"],
            "occurrence_identity_collapse_count": 0,
            "component_union_credit": 0,
            "DSU_rank_reduction_credit": 0,
            "quotient_credit": 0,
            "maximality_credit": 0,
            "fibre_credit": 0,
            "global_disposition_credit": 0,
        },
    }
    result = {**payload, "result_sha256": digest(payload)}
    return witness_ledger, edge_ledger, result


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
    arguments = parser.parse_args()
    producer_sha256 = file_sha256(Path(__file__).resolve())
    witness, edge, result = build(producer_sha256)
    witness_data = gzip_bytes(witness)
    edge_data = gzip_bytes(edge)
    result_data = canonical(result) + b"\n"
    if arguments.no_write:
        for path, data in (
            (WITNESS_LEDGER, witness_data),
            (EDGE_LEDGER, edge_data),
            (RESULT, result_data),
        ):
            if path.exists():
                need(path.read_bytes() == data, "deterministic replay:" + path.name)
    else:
        atomic_write(WITNESS_LEDGER, witness_data)
        atomic_write(EDGE_LEDGER, edge_data)
        atomic_write(RESULT, result_data)
    print(
        json.dumps(
            {
                "status": result["status"],
                "witness_count": witness["row_count"],
                "edge_count": edge["row_count"],
                "result_sha256": result["result_sha256"],
                "write": not arguments.no_write,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
