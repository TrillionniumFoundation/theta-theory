#!/usr/bin/env python3
"""Independent cacheless verifier for the Round300-C edge promotion.

The Round300-C producer is never imported, executed, or parsed.  Its bytes
are used only as an inert SHA-256-pinned artifact.  Expected witness and edge
ledgers are rebuilt from the sealed Round234/235/236, Round245--248,
Round266, Round287, Round294, and Round299-A mathematical sources.
"""

from __future__ import annotations

import argparse
from bisect import bisect_left
from collections import Counter, defaultdict
from copy import deepcopy
from dataclasses import dataclass
from fractions import Fraction
import gzip
import hashlib
from io import BytesIO
import json
import mmap
import os
from pathlib import Path
import stat
import tempfile
from typing import Any, Callable, Iterable, Iterator
import zlib


HERE = Path(__file__).resolve().parent
PREFIX = (
    "cm2_round300c_source_g_virtual_stratum_new_occurrence_"
    "positive_volume_edge_promotion"
)
PRODUCER = HERE / f"{PREFIX}.py"
WITNESS_LEDGER = HERE / f"{PREFIX}_witness_ledger.json.gz"
EDGE_LEDGER = HERE / f"{PREFIX}_edge_ledger.json.gz"
RESULT = HERE / f"{PREFIX}_result.json"
ATTACKS = HERE / f"{PREFIX}_attack_suite.json"
VERIFICATION = HERE / f"{PREFIX}_verification.json"

SCHEMA = (
    "cm2.round300c.source-g-virtual-stratum-new-occurrence-"
    "positive-volume-edge-promotion.v1"
)
WITNESS_SCHEMA = SCHEMA + ".witness-ledger.v1"
EDGE_SCHEMA = SCHEMA + ".edge-ledger.v1"
ATTACK_SCHEMA = SCHEMA + ".independent-attack-suite.v1"
VERIFICATION_SCHEMA = SCHEMA + ".independent-verification.v1"

PRODUCER_SHA256 = (
    "116d51245d75b09db98b935979642977f973a801b8c7c5ca8962c454d182591b"
)
WITNESS_FILE_SHA256 = (
    "bbb690ba8236230bb99fa8c2dcf569f97c758d546c1ec56ae6d3f6c9d880c7e2"
)
EDGE_FILE_SHA256 = (
    "8c9ed8b09e994a00ca3ca4906c35b454523383b7d488f66e7a082dbbd4b1fcec"
)
RESULT_FILE_SHA256 = (
    "415705e38662fa12260320ae0daf77e5e154c38ee9a886ea82f03f22894b44ad"
)
RESULT_SELF_SHA256 = (
    "7c07180b4879bec521bc9a432bc9c7ed354de6d0f033429544a19bb1310645b2"
)

INPUTS = {
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

MAX_FILE_BYTES = 2_000_000_000
MAX_GZIP_BYTES = 512_000_000
Q = Fraction
Box = tuple[Q, Q, Q, Q, Q, Q]


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
        for piece in iter(lambda: stream.read(1 << 20), b""):
            state.update(piece)
    return state.hexdigest()


def safe_regular(path: Path, expected_name: str | None = None) -> None:
    need(path.parent == HERE, "HERE-only path")
    need(path.parent.resolve(strict=True) == HERE.resolve(strict=True), "HERE")
    if expected_name is not None:
        need(path.name == expected_name, "exact basename")
    info = os.lstat(path)
    need(
        not path.is_symlink()
        and stat.S_ISREG(info.st_mode)
        and info.st_nlink == 1
        and 0 < info.st_size <= MAX_FILE_BYTES
        and path.resolve(strict=True).parent == HERE.resolve(strict=True),
        "regular single-link confined file:" + path.name,
    )


def pin(path: Path, expected: str) -> None:
    safe_regular(path, path.name)
    need(file_sha256(path) == expected, "byte pin:" + path.name)


def close_row(payload: dict[str, Any]) -> dict[str, Any]:
    row = dict(payload)
    row["row_sha256"] = digest(payload)
    return row


def verify_closed_row(row: dict[str, Any], label: str) -> None:
    need(type(row) is dict and "row_sha256" in row, label + ":closed row")
    payload = {key: value for key, value in row.items() if key != "row_sha256"}
    need(
        set(row) == set(payload) | {"row_sha256"}
        and row["row_sha256"] == digest(payload),
        label + ":row SHA-256",
    )


class SequenceHasher:
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


def stream_json_table(filename: str, table: str) -> Iterator[dict[str, Any]]:
    path = HERE / filename
    marker = ('"' + table + '"').encode("ascii")
    with path.open("rb") as raw:
        mapped = mmap.mmap(raw.fileno(), 0, access=mmap.ACCESS_READ)
        table_at = mapped.find(marker)
        need(table_at >= 0, "missing table:" + table)
        rows_at = mapped.find(b'"rows"', table_at)
        need(rows_at >= 0, "missing rows:" + table)
        position = rows_at + len(b'"rows"')
        while mapped[position : position + 1] in b" \t\r\n:":
            position += 1
        need(mapped[position : position + 1] == b"[", "row array:" + table)
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
                need(bool(piece), "malformed row:" + table)
                buffer += piece
                continue
            need(type(row) is dict, "row object:" + table)
            yield row
            buffer = buffer[end:]


def stream_gzip_table(filename: str) -> Iterator[dict[str, Any]]:
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
                need(bool(piece), "gzip table EOF:" + filename)
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


def audited_rows(rows: Iterable[dict[str, Any]], tag: str) -> Iterator[dict[str, Any]]:
    expected_count, id_field, ids_pin, hashes_pin = TABLES[tag]
    ids = SequenceHasher()
    hashes = SequenceHasher()
    seen: set[str] = set()
    for row in rows:
        verify_closed_row(row, tag)
        row_id = row[id_field]
        need(type(row_id) is str and row_id not in seen, tag + ":unique row ID")
        seen.add(row_id)
        ids.add(row_id)
        hashes.add(row["row_sha256"])
        yield row
    need(
        len(seen) == expected_count
        and ids.count == hashes.count == expected_count
        and ids.finish() == ids_pin
        and hashes.finish() == hashes_pin,
        tag + ":full table commitments",
    )


def closed_certificate(tag: str) -> dict[str, Any]:
    filename = INPUTS[tag][0]
    with (HERE / filename).open("rb") as stream:
        document = json.load(stream)
    need(
        type(document) is dict
        and set(document) == {"schema", "result", "result_sha256"}
        and document["result_sha256"] == digest(document["result"]),
        tag + ":certificate self-closure",
    )
    return document["result"]


def committed_list(
    result: dict[str, Any],
    field: str,
    count: int,
    id_field: str,
    label: str,
) -> list[dict[str, Any]]:
    rows = result[field]
    need(
        type(rows) is list
        and len(rows) == count
        and result[field + "_sha256"] == digest(rows)
        and len({row[id_field] for row in rows}) == count,
        label + ":list commitment",
    )
    return rows


def qbox(values: Iterable[str]) -> Box:
    box = tuple(Q(value) for value in values)
    need(
        len(box) == 6
        and box[0] < box[1]
        and box[2] < box[3]
        and box[4] < box[5],
        "strict positive rational box",
    )
    return box  # type: ignore[return-value]


def qtext(value: Q) -> str:
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def box_text(box: Box) -> list[str]:
    return [qtext(value) for value in box]


def volume(box: Box) -> Q:
    return (
        (box[1] - box[0])
        * (box[3] - box[2])
        * (box[5] - box[4])
    )


def ordinary_overlap(left: Box, right: Box) -> Box | None:
    answer: list[Q] = []
    for axis in range(3):
        lower = max(left[2 * axis], right[2 * axis])
        upper = min(left[2 * axis + 1], right[2 * axis + 1])
        if lower >= upper:
            return None
        answer.extend((lower, upper))
    return tuple(answer)  # type: ignore[return-value]


def transformed_overlap(sign: int, cell: Box, carrier: Box) -> Box | None:
    need(sign in {-1, 1}, "physical t sign")
    p0, p1 = max(cell[2], carrier[2]), min(cell[3], carrier[3])
    s0, s1 = max(cell[4], carrier[4]), min(cell[5], carrier[5])
    if p0 >= p1 or s0 >= s1:
        return None
    if sign == 1:
        if carrier[1] <= 0:
            return None
        lower, upper = max(carrier[0], Q(0)) ** 2, carrier[1] ** 2
    else:
        if carrier[0] >= 0:
            return None
        lower, upper = min(carrier[1], Q(0)) ** 2, carrier[0] ** 2
    t0, t1 = max(cell[0], lower), min(cell[1], upper)
    if t0 >= t1:
        return None
    return (t0, t1, p0, p1, s0, s1)


@dataclass(frozen=True, slots=True)
class VirtualNode:
    root: str
    frontier_id: str
    frontier_hash: str
    kind: str
    key: str


@dataclass(frozen=True, slots=True)
class Carrier:
    node: str
    virtual: VirtualNode
    signature: str
    key: str
    ordinal: int
    box: Box
    source_class: str
    source_id: str
    source_hash: str
    proof: str


@dataclass(slots=True)
class IntervalIndex:
    center: Q
    by_lower: list[Carrier]
    by_upper_desc: list[Carrier]
    left: "IntervalIndex | None"
    right: "IntervalIndex | None"
    axis: int


def make_index(rows: list[Carrier], axis: int) -> IntervalIndex | None:
    if not rows:
        return None
    centers = sorted(
        (row.box[2 * axis] + row.box[2 * axis + 1]) / 2 for row in rows
    )
    center = centers[len(centers) // 2]
    left: list[Carrier] = []
    right: list[Carrier] = []
    middle: list[Carrier] = []
    for row in rows:
        if row.box[2 * axis + 1] <= center:
            left.append(row)
        elif row.box[2 * axis] >= center:
            right.append(row)
        else:
            middle.append(row)
    need(bool(middle), "interval index pivot")
    return IntervalIndex(
        center,
        sorted(middle, key=lambda row: (row.box[2 * axis], row.node)),
        sorted(
            middle,
            key=lambda row: (row.box[2 * axis + 1], row.node),
            reverse=True,
        ),
        make_index(left, axis),
        make_index(right, axis),
        axis,
    )


def interval_candidates(
    node: IntervalIndex | None, lower: Q, upper: Q
) -> Iterator[Carrier]:
    if node is None:
        return
    axis = node.axis
    if upper <= node.center:
        for row in node.by_lower:
            if row.box[2 * axis] >= upper:
                break
            yield row
        yield from interval_candidates(node.left, lower, upper)
    elif lower >= node.center:
        for row in node.by_upper_desc:
            if row.box[2 * axis + 1] <= lower:
                break
            yield row
        yield from interval_candidates(node.right, lower, upper)
    else:
        yield from node.by_lower
        yield from interval_candidates(node.left, lower, upper)
        yield from interval_candidates(node.right, lower, upper)


def load_virtual_nodes() -> dict[str, VirtualNode]:
    rows = stream_json_table(
        INPUTS["R266"][0],
        "formal_post_Round266_valid_virtual_node_frontier_ledger",
    )
    virtuals: dict[str, VirtualNode] = {}
    kinds: Counter[str] = Counter()
    for row in audited_rows(rows, "R266"):
        node = row["valid_virtual_stratum_node_id"]
        need(node not in virtuals, "unique virtual node")
        item = VirtualNode(
            row["post_Round266_quotient_component_id"],
            row["post_Round266_valid_virtual_node_frontier_row_id"],
            row["row_sha256"],
            row["virtual_node_kind"],
            row["official_key_id"],
        )
        virtuals[node] = item
        kinds[item.kind] += 1
    need(
        kinds
        == {
            "INHERITED_ROUND247_VIRTUAL_STRATUM": 6_388,
            "ROUND248_WALL_BULK": 88_536,
            "ROUND248_WALL_SHEET": 38_360,
        },
        "virtual-node kind inventory",
    )
    return virtuals


def load_wall_source_maps() -> tuple[
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, Any],
]:
    r234 = closed_certificate("R234")
    frontiers_rows = committed_list(
        r234, "depth6_frontier_rows", 38_376, "frontier_row_id", "R234"
    )
    resolved_rows = committed_list(
        r234,
        "resolved_descendant_rows",
        12_200,
        "materialized_row_id",
        "R234",
    )
    need(
        r234["guard_descendant_rows"] == []
        and r234["guard_descendant_rows_sha256"] == digest([]),
        "R234 empty guard commitment",
    )
    frontiers = {row["frontier_row_id"]: row for row in frontiers_rows}
    resolved = {row["materialized_row_id"]: row for row in resolved_rows}

    r235 = closed_certificate("R235")
    single_rows = committed_list(
        r235,
        "single_endpoint_graph_partition_rows",
        38_328,
        "endpoint_graph_partition_row_id",
        "R235",
    )
    deferred_rows = committed_list(
        r235,
        "double_endpoint_deferred_rows",
        16,
        "deferred_row_id",
        "R235",
    )
    single = {
        row["endpoint_graph_partition_row_id"]: row for row in single_rows
    }

    r236 = closed_certificate("R236")
    double_rows = committed_list(
        r236,
        "double_endpoint_partition_rows",
        16,
        "double_endpoint_partition_row_id",
        "R236",
    )
    crossing_rows = committed_list(
        r236,
        "crossing_dependency_discharge_rows",
        32,
        "crossing_dependency_discharge_row_id",
        "R236",
    )
    double = {
        row["double_endpoint_partition_row_id"]: row for row in double_rows
    }
    crossing = {
        row["crossing_dependency_discharge_row_id"]: row
        for row in crossing_rows
    }
    need(
        {row["Round234_frontier_row_id"] for row in deferred_rows}
        == {row["Round234_frontier_row_id"] for row in double_rows},
        "R235/R236 deferred frontier conservation",
    )
    audit = {
        "R234_depth6_frontier_count": len(frontiers),
        "R234_resolved_descendant_count": len(resolved),
        "R235_single_endpoint_count": len(single),
        "R235_deferred_count": len(deferred_rows),
        "R236_double_endpoint_count": len(double),
        "R236_crossing_discharge_count": len(crossing),
    }
    return frontiers, resolved, single, double, crossing, audit


def load_carriers(
    virtuals: dict[str, VirtualNode],
) -> tuple[dict[str, list[Carrier]], dict[str, Any], dict[str, Any]]:
    (
        frontiers,
        resolved,
        single,
        double,
        crossing,
        source_audit,
    ) = load_wall_source_maps()
    groups: dict[str, list[Carrier]] = defaultdict(list)
    source_histogram: Counter[str] = Counter()
    retained = 0
    dropped = 0
    for row in audited_rows(
        stream_json_table(
            INPUTS["R248"][0], "formal_wall_positive_volume_bulk_ledger"
        ),
        "R248",
    ):
        node = row["wall_bulk_node_id"]
        if node not in virtuals:
            dropped += 1
            continue
        source_class = row["source_partition_kind"]
        source_id = row["source_partition_row_id"]
        if source_class == "ROUND234_RESOLVED_DESCENDANT":
            source = resolved[source_id]
            signature_value = source["local_return_signature"]
            carrier_box = qbox(row["exact_positive_3D_box"])
            proof = "EXACT_ROUND234_DYADIC_BOX_AND_SIGNATURE"
        elif source_class == "ROUND235_SINGLE_ENDPOINT_GRAPH_BRANCH":
            source = single[source_id]
            signature_value = source[
                "event_absent_signature"
                if row["branch_label"] == "EVENT_ABSENT"
                else "event_present_signature"
            ]
            carrier_box = qbox(
                frontiers[source["Round234_frontier_row_id"]]["box"]
            )
            proof = (
                "ROUND235_CARRIER_BOX_INTERSECTION_PLUS_"
                "EXACT_BRANCH_SIGNATURE"
            )
        elif source_class == "ROUND236_DOUBLE_ENDPOINT_ARRANGEMENT_BRANCH":
            source = double[source_id]
            field = {
                "SAME_SIGN_EVENT_ABSENT": "same_sign_event_absent_signature",
                "NEGATIVE_TO_POSITIVE": "negative_to_positive_signature",
                "POSITIVE_TO_NEGATIVE": "positive_to_negative_signature",
            }[row["branch_label"]]
            signature_value = source[field]
            carrier_box = qbox(
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
            signature_value = source["local_return_signature"]
            carrier_box = qbox(row["exact_positive_3D_box"])
            proof = "EXACT_ROUND236_CROSSING_DISCHARGE_BOX_AND_SIGNATURE"
        signature = digest(signature_value)
        virtual = virtuals[node]
        need(
            signature == row["local_return_signature_sha256"]
            and signature_value["official_key_id"]
            == row["official_key_id"]
            == virtual.key,
            "wall signature/key joins",
        )
        groups[signature].append(
            Carrier(
                node,
                virtual,
                signature,
                signature_value["official_key_id"],
                signature_value["official_key_ordinal"],
                carrier_box,
                source_class,
                source_id,
                row["row_sha256"],
                proof,
            )
        )
        retained += 1
        source_histogram[source_class] += 1
    need((retained, dropped) == (88_536, 400), "Round248 retention")

    inherited_3d: Counter[str] = Counter()
    withheld_2d: Counter[str] = Counter()
    specifications = (
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
    for tag, table, box_field in specifications:
        for row in audited_rows(
            stream_json_table(INPUTS[tag][0], table), tag
        ):
            node = row["retained_stratum_node_id"]
            need(node in virtuals, "inherited virtual join")
            box_value = row[box_field]
            if box_value is None:
                need(row["local_dimension"] == 2, "withheld 2D stratum")
                withheld_2d[tag] += 1
                continue
            need(row["local_dimension"] == 3, "strict inherited 3D stratum")
            signature_value = row["local_return_signature"]
            signature = digest(signature_value)
            virtual = virtuals[node]
            need(
                signature_value["official_key_id"] == virtual.key,
                "inherited key join",
            )
            source_class = tag + "::" + row["stratum_kind"]
            groups[signature].append(
                Carrier(
                    node,
                    virtual,
                    signature,
                    signature_value["official_key_id"],
                    signature_value["official_key_ordinal"],
                    qbox(box_value),
                    source_class,
                    node,
                    row["row_sha256"],
                    "EXACT_INHERITED_STRICT_POSITIVE_3D_WITNESS_BOX",
                )
            )
            inherited_3d[tag] += 1
            source_histogram[source_class] += 1
    need(
        inherited_3d == {"R245": 3_400, "R246": 2_220, "R247": 504}
        and withheld_2d == {"R245": 264},
        "inherited dimensional inventory",
    )
    for rows in groups.values():
        rows.sort(key=lambda row: row.node)
    need(
        sum(map(len, groups.values())) == 94_660 and len(groups) == 156,
        "complete retained carrier inventory",
    )
    scope = {
        "retained_Round248_wall_bulk_count": retained,
        "Round264_dropped_empty_wall_bulk_count": dropped,
        "inherited_positive_3D_witness_count": sum(inherited_3d.values()),
        "withheld_inherited_2D_sheet_count": sum(withheld_2d.values()),
        "withheld_Round248_wall_sheet_count": 38_360,
        "signature_group_count": len(groups),
        "piece_histogram": dict(sorted(source_histogram.items())),
    }
    return groups, scope, source_audit


def load_refined_keys() -> dict[str, dict[str, Any]]:
    bindings: dict[str, dict[str, Any]] = {}
    for row in audited_rows(
        stream_gzip_table(INPUTS["R299A"][0]), "R299A"
    ):
        occurrence = row["registry_occurrence_id"]
        need(occurrence not in bindings, "unique Round299A occurrence")
        bindings[occurrence] = {
            "official_key_id": row["official_key_id"],
            "official_key_ordinal": row["official_key_ordinal"],
            "binding_row_id":
                row["Round299A_refined_occurrence_official_key_binding_row_id"],
            "binding_row_sha256": row["row_sha256"],
        }
    need(len(bindings) == 9_404, "Round299A full binding inventory")
    return bindings


def load_physical_signs() -> tuple[dict[str, int], dict[str, int], dict[str, str]]:
    with gzip.open(HERE / INPUTS["R287"][0], "rt", encoding="utf-8") as stream:
        document = json.load(stream)
    need(
        document["schema"]
        == (
            "cm2.round287.source-g-rechart-terminal-occurrence-"
            "disposition.ledger.v1"
        ),
        "Round287 schema",
    )
    for field, count_field, hash_field in (
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
            and digest(rows) == document[hash_field],
            "Round287 list commitment:" + field,
        )
        for row in rows:
            verify_closed_row(row, "Round287:" + field)
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
        len(region_sign) == 13_788
        and len(cell_sign) == len(cell_hash) == 7_616,
        "Round287 sign inventory",
    )
    return region_sign, cell_sign, cell_hash


def reconstruct_witnesses(
    carriers: dict[str, list[Carrier]],
    refined_keys: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    region_sign, cell_sign, cell_hash = load_physical_signs()
    time_indexes = {
        signature: make_index(rows, 0) for signature, rows in carriers.items()
    }
    p_indexes = {
        signature: make_index(rows, 1) for signature, rows in carriers.items()
    }
    witnesses: list[dict[str, Any]] = []
    comparisons: Counter[str] = Counter()
    kinds: Counter[str] = Counter()
    incident: set[str] = set()
    source_histogram: Counter[str] = Counter()
    for registry in audited_rows(
        stream_gzip_table(INPUTS["R294"][0]), "R294"
    ):
        kind = registry["registry_entry_kind"]
        kinds[kind] += 1
        if kind == "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE":
            continue
        occurrence = registry["registry_occurrence_id"]
        signature = registry["complete_10_field_return_signature_sha256"]
        if kind == "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM":
            occurrence_box = qbox(
                registry["positive_volume_rational_inner_support_box"]
            )
            key = registry["official_key_id"]
            ordinal = registry["official_key_ordinal"]
            for carrier in interval_candidates(
                time_indexes.get(signature),
                occurrence_box[0],
                occurrence_box[1],
            ):
                comparisons["ROUND288_RATIONAL"] += 1
                overlap = ordinary_overlap(carrier.box, occurrence_box)
                if overlap is None:
                    continue
                need(
                    carrier.key == key and carrier.ordinal == ordinal,
                    "Round288 overlap key/signature identity",
                )
                payload = {
                    "witness_class": "ROUND288_RATIONAL_INNER_BOX_OVERLAP",
                    "virtual_stratum_node_id": carrier.node,
                    "post_Round266_quotient_component_id":
                        carrier.virtual.root,
                    "source_Round266_virtual_frontier_row_id":
                        carrier.virtual.frontier_id,
                    "source_Round266_virtual_frontier_row_sha256":
                        carrier.virtual.frontier_hash,
                    "virtual_node_kind": carrier.virtual.kind,
                    "virtual_piece_source_class": carrier.source_class,
                    "virtual_piece_source_row_id": carrier.source_id,
                    "virtual_piece_source_row_sha256": carrier.source_hash,
                    "virtual_piece_carrier_proof": carrier.proof,
                    "virtual_piece_carrier_box": box_text(carrier.box),
                    "Round294_registry_occurrence_id": occurrence,
                    "source_Round294_registry_row_id":
                        registry["Round294_occurrence_registry_row_id"],
                    "source_Round294_registry_row_sha256":
                        registry["row_sha256"],
                    "Round294_registry_entry_kind": kind,
                    "occurrence_positive_rational_inner_support_box":
                        box_text(occurrence_box),
                    "complete_10_field_return_signature_sha256": signature,
                    "official_key_id": key,
                    "official_key_ordinal": ordinal,
                    "exact_intersection_coordinate_system": "(t,p,s)",
                    "exact_positive_intersection_box": box_text(overlap),
                    "exact_positive_intersection_volume": qtext(
                        volume(overlap)
                    ),
                    "same_complete_signature_required": True,
                    "same_official_key_required": True,
                    "positive_volume_physical_overlap": True,
                }
                witness_id = (
                    "round300c-virtual-occurrence-positive-volume-witness:"
                    + digest(payload)
                )
                witnesses.append(
                    close_row(
                        {
                            "Round300C_virtual_occurrence_positive_volume_"
                            "witness_row_id": witness_id,
                            **payload,
                        }
                    )
                )
                incident.add(occurrence)
                source_histogram[carrier.source_class] += 1
            continue

        need(
            kind
            == "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT",
            "known Round294 registry kind",
        )
        binding = refined_keys[occurrence]
        need(
            binding["official_key_id"] is not None
            and registry["official_key_id"] is None,
            "Round299A supplies refined key",
        )
        for cell in registry["member_refinement_cells"]:
            transformed = qbox(cell["exact_transformed_open_cell"])
            source_cell_id = cell["source_Round287_support_cell_id"]
            if source_cell_id.startswith("WHOLE:"):
                sign = region_sign[cell["Round275_region_id"]]
                source_cell_hash = cell["source_row_sha256"]
            else:
                sign = cell_sign[source_cell_id]
                source_cell_hash = cell_hash[source_cell_id]
            for carrier in interval_candidates(
                p_indexes.get(signature), transformed[2], transformed[3]
            ):
                comparisons["ROUND292_TRANSFORMED"] += 1
                overlap = transformed_overlap(sign, transformed, carrier.box)
                if overlap is None:
                    continue
                need(
                    carrier.key == binding["official_key_id"]
                    and carrier.ordinal == binding["official_key_ordinal"],
                    "Round292 overlap key/signature identity",
                )
                payload = {
                    "witness_class":
                        "ROUND292_EXACT_TRANSFORMED_CELL_OVERLAP",
                    "virtual_stratum_node_id": carrier.node,
                    "post_Round266_quotient_component_id":
                        carrier.virtual.root,
                    "source_Round266_virtual_frontier_row_id":
                        carrier.virtual.frontier_id,
                    "source_Round266_virtual_frontier_row_sha256":
                        carrier.virtual.frontier_hash,
                    "virtual_node_kind": carrier.virtual.kind,
                    "virtual_piece_source_class": carrier.source_class,
                    "virtual_piece_source_row_id": carrier.source_id,
                    "virtual_piece_source_row_sha256": carrier.source_hash,
                    "virtual_piece_carrier_proof": carrier.proof,
                    "virtual_piece_carrier_box": box_text(carrier.box),
                    "Round294_registry_occurrence_id": occurrence,
                    "source_Round294_registry_row_id":
                        registry["Round294_occurrence_registry_row_id"],
                    "source_Round294_registry_row_sha256":
                        registry["row_sha256"],
                    "Round294_registry_entry_kind": kind,
                    "source_Round287_support_cell_id": source_cell_id,
                    "source_Round287_support_cell_row_sha256":
                        source_cell_hash,
                    "Round292_refinement_cell_id":
                        cell["Round292_refinement_cell_id"],
                    "Round275_region_id": cell["Round275_region_id"],
                    "physical_t_sign": sign,
                    "occurrence_exact_transformed_open_cell":
                        box_text(transformed),
                    "complete_10_field_return_signature_sha256": signature,
                    "official_key_id": binding["official_key_id"],
                    "official_key_ordinal":
                        binding["official_key_ordinal"],
                    "source_Round299A_key_binding_row_id":
                        binding["binding_row_id"],
                    "source_Round299A_key_binding_row_sha256":
                        binding["binding_row_sha256"],
                    "exact_intersection_coordinate_system": "(t^2,p,s)",
                    "exact_positive_intersection_box": box_text(overlap),
                    "exact_positive_intersection_volume": qtext(
                        volume(overlap)
                    ),
                    "same_complete_signature_required": True,
                    "same_official_key_required": True,
                    "positive_volume_physical_overlap": True,
                }
                witness_id = (
                    "round300c-virtual-occurrence-positive-volume-witness:"
                    + digest(payload)
                )
                witnesses.append(
                    close_row(
                        {
                            "Round300C_virtual_occurrence_positive_volume_"
                            "witness_row_id": witness_id,
                            **payload,
                        }
                    )
                )
                incident.add(occurrence)
                source_histogram[carrier.source_class] += 1
    need(
        kinds
        == {
            "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE": 126_468,
            "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM": 295_336,
            "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT": 9_404,
        },
        "complete Round294 tranche inventory",
    )
    id_field = (
        "Round300C_virtual_occurrence_positive_volume_witness_row_id"
    )
    witnesses.sort(key=lambda row: row[id_field])
    need(
        len(witnesses) == len({row[id_field] for row in witnesses}) == 6_322
        and len(incident) == 6_314
        and comparisons
        == {"ROUND288_RATIONAL": 229_663, "ROUND292_TRANSFORMED": 1_840},
        "exact comparison/witness inventory",
    )
    audit = {
        "exact_candidate_comparison_histogram":
            dict(sorted(comparisons.items())),
        "incident_new_occurrence_count": len(incident),
        "nonincident_new_occurrence_count": 304_740 - len(incident),
        "witness_histogram_by_virtual_piece_source":
            dict(sorted(source_histogram.items())),
    }
    return witnesses, audit


def reconstruct_edges(
    witnesses: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    witness_id_field = (
        "Round300C_virtual_occurrence_positive_volume_witness_row_id"
    )
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    roots: dict[str, set[str]] = defaultdict(set)
    for row in witnesses:
        root = row["post_Round266_quotient_component_id"]
        occurrence = row["Round294_registry_occurrence_id"]
        grouped[(root, occurrence)].append(row)
        roots[occurrence].add(root)
    need(
        len(grouped) == len(roots) == 6_314
        and all(len(value) == 1 for value in roots.values()),
        "one virtual root per incident occurrence",
    )
    edges: list[dict[str, Any]] = []
    multiplicity: Counter[int] = Counter()
    for (root, occurrence), rows in sorted(grouped.items()):
        rows.sort(key=lambda row: row[witness_id_field])
        keys = {row["official_key_id"] for row in rows}
        ordinals = {row["official_key_ordinal"] for row in rows}
        signatures = {
            row["complete_10_field_return_signature_sha256"] for row in rows
        }
        need(
            len(keys) == len(ordinals) == len(signatures) == 1,
            "edge signature/key agreement",
        )
        ids = [row[witness_id_field] for row in rows]
        hashes = [row["row_sha256"] for row in rows]
        multiplicity[len(rows)] += 1
        payload = {
            "post_Round266_quotient_component_id": root,
            "Round294_registry_occurrence_id": occurrence,
            "canonical_component_edge_endpoint_pair": [root, occurrence],
            "positive_volume_witness_count": len(rows),
            "positive_volume_witness_row_ids": ids,
            "positive_volume_witness_row_ids_sha256": digest(ids),
            "positive_volume_witness_row_hashes_sha256": digest(hashes),
            "complete_10_field_return_signature_sha256":
                next(iter(signatures)),
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
        edges.append(
            close_row(
                {
                    "Round300C_virtual_occurrence_positive_volume_edge_row_id":
                        edge_id,
                    **payload,
                }
            )
        )
    edge_id_field = (
        "Round300C_virtual_occurrence_positive_volume_edge_row_id"
    )
    edges.sort(key=lambda row: row[edge_id_field])
    need(
        len(edges) == len({row[edge_id_field] for row in edges}) == 6_314
        and multiplicity == {1: 6_306, 2: 8},
        "canonical edge inventory and multiplicity",
    )
    return edges, {
        "canonical_root_occurrence_edge_count": len(edges),
        "edge_witness_multiplicity_histogram": {
            str(key): value for key, value in sorted(multiplicity.items())
        },
        "occurrence_identity_collapse_count": 0,
        "formal_DSU_rank_reduction_credit": 0,
    }


def make_ledger(
    rows: list[dict[str, Any]],
    schema: str,
    id_field: str,
    status: str,
) -> dict[str, Any]:
    ids = [row[id_field] for row in rows]
    need(len(ids) == len(set(ids)), "unique output IDs")
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


def ledger_summary(value: dict[str, Any], filename: str) -> dict[str, Any]:
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


def deterministic_gzip(value: dict[str, Any]) -> bytes:
    output = BytesIO()
    with gzip.GzipFile(
        filename="", mode="wb", fileobj=output, compresslevel=9, mtime=0
    ) as stream:
        stream.write(canonical(value))
    return output.getvalue()


def reconstruct_expected() -> dict[str, Any]:
    for filename, expected in INPUTS.values():
        pin(HERE / filename, expected)
    pin(PRODUCER, PRODUCER_SHA256)
    virtuals = load_virtual_nodes()
    carriers, scope, source_audit = load_carriers(virtuals)
    refined = load_refined_keys()
    witnesses, witness_audit = reconstruct_witnesses(carriers, refined)
    edges, edge_audit = reconstruct_edges(witnesses)
    witness_ledger = make_ledger(
        witnesses,
        WITNESS_SCHEMA,
        "Round300C_virtual_occurrence_positive_volume_witness_row_id",
        (
            "FORMAL_6322_EXACT_POSITIVE_VOLUME_VIRTUAL_OCCURRENCE_WITNESSES__"
            "NO_FRONTIER_EXHAUSTION_CLAIM"
        ),
    )
    edge_ledger = make_ledger(
        edges,
        EDGE_SCHEMA,
        "Round300C_virtual_occurrence_positive_volume_edge_row_id",
        (
            "FORMAL_6314_CANONICAL_ROOT_OCCURRENCE_COMPONENT_EDGES__"
            "NO_QUOTIENT_OR_MAXIMALITY_CREDIT"
        ),
    )
    payload = {
        "schema": SCHEMA,
        "status":
            "PASS_ROUND300C_EXACT_POSITIVE_VOLUME_EDGE_PROMOTION__"
            "6322_WITNESSES__6314_CANONICAL_EDGES__"
            "SCOPE_REMAINS_NONEXHAUSTIVE",
        "producer_file_sha256": PRODUCER_SHA256,
        "input_file_pins": {
            filename: expected
            for filename, expected in sorted(INPUTS.values())
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
    return {
        "witness": witness_ledger,
        "edge": edge_ledger,
        "result": result,
        "witness_bytes": deterministic_gzip(witness_ledger),
        "edge_bytes": deterministic_gzip(edge_ledger),
        "result_bytes": canonical(result) + b"\n",
        "source_audit": source_audit,
    }


def _reject_json_number(value: str) -> Any:
    raise VerificationError("non-integral or nonfinite JSON number:" + value)


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in result, "duplicate JSON key:" + key)
        result[key] = value
    return result


def strict_json(data: bytes) -> Any:
    need(b"\x00" not in data, "NUL-free JSON")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise VerificationError("UTF-8 JSON") from exc
    decoder = json.JSONDecoder(
        object_pairs_hook=_unique_object,
        parse_float=_reject_json_number,
        parse_constant=_reject_json_number,
    )
    try:
        value, end = decoder.raw_decode(text)
    except (json.JSONDecodeError, VerificationError) as exc:
        raise VerificationError("strict JSON document") from exc
    need(text[end:].strip() == "", "single trailing-free JSON document")
    return value


def strict_gzip(data: bytes, limit: int = MAX_GZIP_BYTES) -> bytes:
    need(len(data) >= 18, "minimum GZIP member")
    decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
    try:
        output = decoder.decompress(data, limit + 1)
        need(len(output) <= limit, "GZIP size cap")
        output += decoder.flush(limit + 1 - len(output))
    except zlib.error as exc:
        raise VerificationError("valid GZIP") from exc
    need(
        len(output) <= limit
        and decoder.eof
        and decoder.unconsumed_tail == b""
        and decoder.unused_data == b"",
        "one complete trailing-free GZIP member",
    )
    return output


def validate_ledger(
    ledger: dict[str, Any],
    *,
    schema: str,
    row_count: int,
    id_field: str,
) -> None:
    need(
        type(ledger) is dict
        and ledger["schema"] == schema
        and ledger["row_count"] == row_count
        and ledger["every_row_closed_by_own_SHA256"] is True
        and type(ledger["rows"]) is list
        and len(ledger["rows"]) == row_count,
        "ledger schema/inventory",
    )
    rows = ledger["rows"]
    ids: list[str] = []
    hashes: list[str] = []
    for row in rows:
        verify_closed_row(row, schema)
        ids.append(row[id_field])
        hashes.append(row["row_sha256"])
    need(
        ids == sorted(ids)
        and len(ids) == len(set(ids))
        and ledger["row_ids_sha256"] == digest(ids)
        and ledger["row_hashes_sha256"] == digest(hashes)
        and ledger["rows_sha256"] == digest(rows),
        "ledger ordering/dedup/list commitments",
    )


def validate_witness_semantics(ledger: dict[str, Any]) -> None:
    id_field = (
        "Round300C_virtual_occurrence_positive_volume_witness_row_id"
    )
    class_histogram: Counter[str] = Counter()
    incident: set[str] = set()
    for row in ledger["rows"]:
        payload = {
            key: value
            for key, value in row.items()
            if key not in {id_field, "row_sha256"}
        }
        need(
            row[id_field]
            == (
                "round300c-virtual-occurrence-positive-volume-witness:"
                + digest(payload)
            ),
            "witness content-addressed ID",
        )
        carrier = qbox(row["virtual_piece_carrier_box"])
        claimed = qbox(row["exact_positive_intersection_box"])
        witness_class = row["witness_class"]
        if witness_class == "ROUND288_RATIONAL_INNER_BOX_OVERLAP":
            occurrence = qbox(
                row["occurrence_positive_rational_inner_support_box"]
            )
            actual = ordinary_overlap(carrier, occurrence)
            need(
                row["exact_intersection_coordinate_system"] == "(t,p,s)"
                and row["Round294_registry_entry_kind"]
                == "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM",
                "Round288 witness coordinate/kind",
            )
        else:
            need(
                witness_class == "ROUND292_EXACT_TRANSFORMED_CELL_OVERLAP",
                "known witness class",
            )
            cell = qbox(row["occurrence_exact_transformed_open_cell"])
            actual = transformed_overlap(
                row["physical_t_sign"], cell, carrier
            )
            need(
                row["exact_intersection_coordinate_system"] == "(t^2,p,s)"
                and row["Round294_registry_entry_kind"]
                == (
                    "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT"
                )
                and row["source_Round299A_key_binding_row_id"],
                "Round292 witness coordinate/kind/key source",
            )
        need(
            actual == claimed
            and row["exact_positive_intersection_volume"]
            == qtext(volume(claimed))
            and volume(claimed) > 0
            and row["same_complete_signature_required"] is True
            and row["same_official_key_required"] is True
            and row["positive_volume_physical_overlap"] is True
            and type(row["complete_10_field_return_signature_sha256"]) is str
            and len(row["complete_10_field_return_signature_sha256"]) == 64
            and type(row["official_key_id"]) is str
            and type(row["official_key_ordinal"]) is int,
            "exact positive-volume witness semantics",
        )
        class_histogram[witness_class] += 1
        incident.add(row["Round294_registry_occurrence_id"])
    need(
        class_histogram
        == {
            "ROUND288_RATIONAL_INNER_BOX_OVERLAP": 6_214,
            "ROUND292_EXACT_TRANSFORMED_CELL_OVERLAP": 108,
        }
        and len(incident) == 6_314,
        "witness class and incidence inventory",
    )


def validate_edge_semantics(
    edge_ledger: dict[str, Any], witness_ledger: dict[str, Any]
) -> None:
    witness_id_field = (
        "Round300C_virtual_occurrence_positive_volume_witness_row_id"
    )
    edge_id_field = (
        "Round300C_virtual_occurrence_positive_volume_edge_row_id"
    )
    witnesses = {
        row[witness_id_field]: row for row in witness_ledger["rows"]
    }
    used: list[str] = []
    multiplicity: Counter[int] = Counter()
    occurrences: set[str] = set()
    roots_by_occurrence: dict[str, set[str]] = defaultdict(set)
    zero_fields = (
        "formal_occurrence_identity_collapse_credit",
        "formal_occurrence_alias_credit",
        "formal_new_occurrence_ID_credit",
        "formal_component_union_credit",
        "formal_DSU_rank_reduction_credit",
        "formal_maximality_credit",
        "formal_fibre_credit",
        "formal_global_disposition_credit",
    )
    for row in edge_ledger["rows"]:
        payload = {
            key: value
            for key, value in row.items()
            if key not in {edge_id_field, "row_sha256"}
        }
        need(
            row[edge_id_field]
            == (
                "round300c-virtual-occurrence-positive-volume-edge:"
                + digest(payload)
            ),
            "edge content-addressed ID",
        )
        root = row["post_Round266_quotient_component_id"]
        occurrence = row["Round294_registry_occurrence_id"]
        ids = row["positive_volume_witness_row_ids"]
        selected = [witnesses[witness_id] for witness_id in ids]
        hashes = [item["row_sha256"] for item in selected]
        need(
            ids == sorted(ids)
            and len(ids) == len(set(ids))
            and row["canonical_component_edge_endpoint_pair"]
            == [root, occurrence]
            and row["positive_volume_witness_count"] == len(ids)
            and row["positive_volume_witness_row_ids_sha256"] == digest(ids)
            and row["positive_volume_witness_row_hashes_sha256"]
            == digest(hashes)
            and all(
                item["post_Round266_quotient_component_id"] == root
                and item["Round294_registry_occurrence_id"] == occurrence
                and item["complete_10_field_return_signature_sha256"]
                == row["complete_10_field_return_signature_sha256"]
                and item["official_key_id"] == row["official_key_id"]
                and item["official_key_ordinal"] == row["official_key_ordinal"]
                for item in selected
            ),
            "edge exact witness grouping",
        )
        need(
            row["edge_semantics"]
            == (
                "EXACT_POSITIVE_VOLUME_PHYSICAL_OVERLAP__"
                "COMPONENT_CONNECTIVITY_NOT_OCCURRENCE_IDENTITY"
            )
            and row["formal_positive_volume_component_edge_witness_credit"]
            == 1
            and all(row[field] == 0 for field in zero_fields)
            and row["post_Round300C_quotient_component_id"] is None,
            "edge credit and strict nonpromotion",
        )
        used.extend(ids)
        multiplicity[len(ids)] += 1
        occurrences.add(occurrence)
        roots_by_occurrence[occurrence].add(root)
    need(
        sorted(used) == sorted(witnesses)
        and multiplicity == {1: 6_306, 2: 8}
        and len(occurrences) == 6_314
        and all(len(roots) == 1 for roots in roots_by_occurrence.values()),
        "edge witness exhaustion/multiplicity/root uniqueness",
    )


def validate_result(
    result: dict[str, Any],
    witness: dict[str, Any],
    edge: dict[str, Any],
) -> None:
    payload = dict(result)
    claimed = payload.pop("result_sha256", None)
    need(
        claimed == digest(payload) == RESULT_SELF_SHA256
        and result["schema"] == SCHEMA
        and result["producer_file_sha256"] == PRODUCER_SHA256
        and result["witness_ledger"]
        == ledger_summary(witness, WITNESS_LEDGER.name)
        and result["edge_ledger"] == ledger_summary(edge, EDGE_LEDGER.name),
        "result closure and ledger joins",
    )
    need(
        result["scope"]["retained_Round248_wall_bulk_count"] == 88_536
        and result["scope"]["inherited_positive_3D_witness_count"] == 6_124
        and result["scope"]["withheld_Round248_wall_sheet_count"] == 38_360
        and result["scope"]["withheld_inherited_2D_sheet_count"] == 264
        and result["scope"]["signature_group_count"] == 156
        and result["witness_audit"]["exact_candidate_comparison_histogram"]
        == {"ROUND288_RATIONAL": 229_663, "ROUND292_TRANSFORMED": 1_840}
        and result["witness_audit"]["incident_new_occurrence_count"] == 6_314
        and result["witness_audit"]["nonincident_new_occurrence_count"]
        == 298_426
        and result["edge_audit"]["canonical_root_occurrence_edge_count"]
        == 6_314
        and result["edge_audit"]["edge_witness_multiplicity_histogram"]
        == {"1": 6_306, "2": 8},
        "result exact census",
    )
    nonpromotion = result["strict_nonpromotion"]
    need(
        nonpromotion
        == {
            "complete_virtual_new_occurrence_frontier_claimed": False,
            "withheld_Round248_wall_sheet_count": 38_360,
            "withheld_inherited_2D_sheet_count": 264,
            "nonincident_new_occurrence_count": 298_426,
            "occurrence_identity_collapse_count": 0,
            "component_union_credit": 0,
            "DSU_rank_reduction_credit": 0,
            "quotient_credit": 0,
            "maximality_credit": 0,
            "fibre_credit": 0,
            "global_disposition_credit": 0,
        },
        "strict zero-credit nonpromotion",
    )


def validate_bundle(
    witness: dict[str, Any],
    edge: dict[str, Any],
    result: dict[str, Any],
    expected: dict[str, Any] | None = None,
) -> None:
    validate_ledger(
        witness,
        schema=WITNESS_SCHEMA,
        row_count=6_322,
        id_field=(
            "Round300C_virtual_occurrence_positive_volume_witness_row_id"
        ),
    )
    validate_witness_semantics(witness)
    validate_ledger(
        edge,
        schema=EDGE_SCHEMA,
        row_count=6_314,
        id_field=(
            "Round300C_virtual_occurrence_positive_volume_edge_row_id"
        ),
    )
    validate_edge_semantics(edge, witness)
    validate_result(result, witness, edge)
    if expected is not None:
        need(
            witness == expected["witness"]
            and edge == expected["edge"]
            and result == expected["result"],
            "candidate equals independent reconstruction",
        )


def read_candidate(expected: dict[str, Any]) -> None:
    for path, expected_hash in (
        (WITNESS_LEDGER, WITNESS_FILE_SHA256),
        (EDGE_LEDGER, EDGE_FILE_SHA256),
        (RESULT, RESULT_FILE_SHA256),
    ):
        pin(path, expected_hash)
    witness_raw = WITNESS_LEDGER.read_bytes()
    edge_raw = EDGE_LEDGER.read_bytes()
    result_raw = RESULT.read_bytes()
    witness = strict_json(strict_gzip(witness_raw))
    edge = strict_json(strict_gzip(edge_raw))
    result = strict_json(result_raw)
    need(
        witness_raw == expected["witness_bytes"]
        and edge_raw == expected["edge_bytes"]
        and result_raw == expected["result_bytes"],
        "candidate deterministic canonical bytes",
    )
    validate_bundle(witness, edge, result, expected)


def rebuild_ledger(ledger: dict[str, Any], id_field: str) -> None:
    ledger["rows"].sort(key=lambda row: row[id_field])
    ids = [row[id_field] for row in ledger["rows"]]
    ledger["row_count"] = len(ledger["rows"])
    ledger["row_ids_sha256"] = digest(ids)
    ledger["row_hashes_sha256"] = digest(
        [row["row_sha256"] for row in ledger["rows"]]
    )
    ledger["rows_sha256"] = digest(ledger["rows"])


def reclose_content_id(row: dict[str, Any], id_field: str, prefix: str) -> None:
    payload = {
        key: value
        for key, value in row.items()
        if key not in {id_field, "row_sha256"}
    }
    row[id_field] = prefix + digest(payload)
    row["row_sha256"] = digest(
        {key: value for key, value in row.items() if key != "row_sha256"}
    )


def reclose_result(
    result: dict[str, Any],
    witness: dict[str, Any],
    edge: dict[str, Any],
) -> None:
    result["witness_ledger"] = ledger_summary(witness, WITNESS_LEDGER.name)
    result["edge_ledger"] = ledger_summary(edge, EDGE_LEDGER.name)
    result["result_sha256"] = digest(
        {key: value for key, value in result.items() if key != "result_sha256"}
    )


def set_value(field: str, value: Any) -> Callable[[dict[str, Any]], None]:
    def mutate(row: dict[str, Any]) -> None:
        row[field] = value
    return mutate


def _semantic_mutation(
    expected: dict[str, Any],
    channel: str,
    mutator: Callable[[dict[str, Any]], None],
    *,
    predicate: Callable[[dict[str, Any]], bool] | None = None,
) -> None:
    witness = {**expected["witness"], "rows": list(expected["witness"]["rows"])}
    edge = {**expected["edge"], "rows": list(expected["edge"]["rows"])}
    result = deepcopy(expected["result"])
    if channel == "witness":
        index = next(
            (
                index
                for index, row in enumerate(witness["rows"])
                if predicate is None or predicate(row)
            ),
            None,
        )
        need(index is not None, "semantic attack witness selector")
        row = deepcopy(witness["rows"][index])
        mutator(row)
        reclose_content_id(
            row,
            "Round300C_virtual_occurrence_positive_volume_witness_row_id",
            "round300c-virtual-occurrence-positive-volume-witness:",
        )
        witness["rows"][index] = row
        rebuild_ledger(
            witness,
            "Round300C_virtual_occurrence_positive_volume_witness_row_id",
        )
    elif channel == "edge":
        index = next(
            (
                index
                for index, row in enumerate(edge["rows"])
                if predicate is None or predicate(row)
            ),
            None,
        )
        need(index is not None, "semantic attack edge selector")
        row = deepcopy(edge["rows"][index])
        mutator(row)
        reclose_content_id(
            row,
            "Round300C_virtual_occurrence_positive_volume_edge_row_id",
            "round300c-virtual-occurrence-positive-volume-edge:",
        )
        edge["rows"][index] = row
        rebuild_ledger(
            edge,
            "Round300C_virtual_occurrence_positive_volume_edge_row_id",
        )
    elif channel == "result":
        mutator(result)
    elif channel == "witness_delete":
        witness["rows"] = witness["rows"][1:]
        rebuild_ledger(
            witness,
            "Round300C_virtual_occurrence_positive_volume_witness_row_id",
        )
    elif channel == "witness_duplicate":
        witness["rows"].append(deepcopy(witness["rows"][0]))
        rebuild_ledger(
            witness,
            "Round300C_virtual_occurrence_positive_volume_witness_row_id",
        )
    elif channel == "edge_delete":
        edge["rows"] = edge["rows"][1:]
        rebuild_ledger(
            edge,
            "Round300C_virtual_occurrence_positive_volume_edge_row_id",
        )
    elif channel == "edge_duplicate":
        edge["rows"].append(deepcopy(edge["rows"][0]))
        rebuild_ledger(
            edge,
            "Round300C_virtual_occurrence_positive_volume_edge_row_id",
        )
    else:
        raise VerificationError("unknown semantic attack channel")
    reclose_result(result, witness, edge)
    validate_bundle(witness, edge, result, expected)


def rejected_attack(
    attack_id: str,
    category: str,
    description: str,
    action: Callable[[], None],
    *,
    reclosed: bool,
) -> dict[str, Any]:
    reason = ""
    try:
        action()
    except (
        VerificationError,
        KeyError,
        ValueError,
        TypeError,
        OSError,
        zlib.error,
    ) as exc:
        # Deliberately omit temporary path names and other runtime-local
        # details so a distinct seed/hash seed produces byte-identical output.
        reason = type(exc).__name__ + ":REJECTED_" + category
    need(bool(reason), "attack must be rejected:" + attack_id)
    return close_row(
        {
            "attack_id": attack_id,
            "category": category,
            "description": description,
            "cryptographic_reclosure_completed": reclosed,
            "independent_verification_status": "REJECTED",
            "rejection_reason": reason[:300],
        }
    )


def build_attacks(expected: dict[str, Any]) -> dict[str, Any]:
    specs: list[
        tuple[
            str,
            str,
            str,
            Callable[[], None],
            bool,
        ]
    ] = []

    def semantic(
        attack_id: str,
        category: str,
        description: str,
        channel: str,
        mutator: Callable[[dict[str, Any]], None],
        predicate: Callable[[dict[str, Any]], bool] | None = None,
    ) -> None:
        specs.append(
            (
                attack_id,
                category,
                description,
                lambda c=channel, m=mutator, p=predicate:
                    _semantic_mutation(expected, c, m, predicate=p),
                True,
            )
        )

    semantic(
        "S01_WITNESS_DELETE",
        "INVENTORY",
        "delete one witness and reclose ledger/result commitments",
        "witness_delete",
        lambda row: None,
    )
    semantic(
        "S02_WITNESS_DUPLICATE",
        "DEDUP",
        "duplicate one witness and reclose ledger/result commitments",
        "witness_duplicate",
        lambda row: None,
    )
    semantic(
        "S03_EDGE_DELETE",
        "INVENTORY",
        "delete one canonical edge and reclose ledger/result commitments",
        "edge_delete",
        lambda row: None,
    )
    semantic(
        "S04_EDGE_DUPLICATE",
        "DEDUP",
        "duplicate one edge and reclose ledger/result commitments",
        "edge_duplicate",
        lambda row: None,
    )
    semantic(
        "S05_R288_INTERSECTION_BOX",
        "GEOMETRY",
        "replace an exact rational intersection by its carrier box",
        "witness",
        lambda row: row.__setitem__(
            "exact_positive_intersection_box",
            row["virtual_piece_carrier_box"],
        ),
        lambda row: row["witness_class"]
        == "ROUND288_RATIONAL_INNER_BOX_OVERLAP",
    )
    semantic(
        "S06_R292_INTERSECTION_BOX",
        "GEOMETRY",
        "replace a transformed intersection by its carrier box",
        "witness",
        lambda row: row.__setitem__(
            "exact_positive_intersection_box",
            row["virtual_piece_carrier_box"],
        ),
        lambda row: row["witness_class"]
        == "ROUND292_EXACT_TRANSFORMED_CELL_OVERLAP",
    )
    semantic(
        "S07_INTERSECTION_VOLUME",
        "GEOMETRY",
        "forge exact positive volume while preserving row/list hashes",
        "witness",
        set_value("exact_positive_intersection_volume", "1"),
    )
    semantic(
        "S08_PHYSICAL_T_SIGN",
        "GEOMETRY",
        "flip the exact physical-t sign of a transformed witness",
        "witness",
        lambda row: row.__setitem__(
            "physical_t_sign", -row["physical_t_sign"]
        ),
        lambda row: row["witness_class"]
        == "ROUND292_EXACT_TRANSFORMED_CELL_OVERLAP",
    )
    semantic(
        "S09_COORDINATE_SYSTEM",
        "GEOMETRY",
        "swap exact coordinate-system label",
        "witness",
        set_value("exact_intersection_coordinate_system", "(p,s,t)"),
    )
    semantic(
        "S10_POSITIVE_OVERLAP_FLAG",
        "GEOMETRY",
        "clear positive physical-overlap assertion",
        "witness",
        set_value("positive_volume_physical_overlap", False),
    )
    semantic(
        "S11_COMPLETE_SIGNATURE",
        "SIGNATURE",
        "replace complete ten-field signature hash",
        "witness",
        set_value(
            "complete_10_field_return_signature_sha256", "0" * 64
        ),
    )
    semantic(
        "S12_OFFICIAL_KEY_ID",
        "KEY",
        "replace exact official key ID",
        "witness",
        set_value("official_key_id", "round300c-forged-key"),
    )
    semantic(
        "S13_OFFICIAL_KEY_ORDINAL",
        "KEY",
        "increment exact official key ordinal",
        "witness",
        lambda row: row.__setitem__(
            "official_key_ordinal", row["official_key_ordinal"] + 1
        ),
    )
    semantic(
        "S14_VIRTUAL_ROOT",
        "JOIN",
        "replace post-Round266 virtual quotient root",
        "witness",
        set_value(
            "post_Round266_quotient_component_id", "forged-virtual-root"
        ),
    )
    semantic(
        "S15_OCCURRENCE_ID",
        "JOIN",
        "replace Round294 occurrence endpoint",
        "witness",
        set_value("Round294_registry_occurrence_id", "forged-occurrence"),
    )
    semantic(
        "S16_R266_FRONTIER_HASH",
        "COMMITMENT",
        "replace pinned virtual-frontier row hash",
        "witness",
        set_value("source_Round266_virtual_frontier_row_sha256", "0" * 64),
    )
    semantic(
        "S17_R294_REGISTRY_HASH",
        "COMMITMENT",
        "replace pinned Round294 registry row hash",
        "witness",
        set_value("source_Round294_registry_row_sha256", "0" * 64),
    )
    semantic(
        "S18_R299A_BINDING_HASH",
        "COMMITMENT",
        "replace refined key-binding row hash",
        "witness",
        set_value("source_Round299A_key_binding_row_sha256", "0" * 64),
        lambda row: row["witness_class"]
        == "ROUND292_EXACT_TRANSFORMED_CELL_OVERLAP",
    )
    semantic(
        "S19_EDGE_WITNESS_COUNT",
        "INVENTORY",
        "increment edge witness multiplicity",
        "edge",
        lambda row: row.__setitem__(
            "positive_volume_witness_count",
            row["positive_volume_witness_count"] + 1,
        ),
    )
    semantic(
        "S20_EDGE_WITNESS_IDS_HASH",
        "COMMITMENT",
        "replace edge witness-ID list hash",
        "edge",
        set_value("positive_volume_witness_row_ids_sha256", "0" * 64),
    )
    semantic(
        "S21_EDGE_WITNESS_HASHES",
        "COMMITMENT",
        "replace edge witness-row hash commitment",
        "edge",
        set_value("positive_volume_witness_row_hashes_sha256", "0" * 64),
    )
    semantic(
        "S22_EDGE_ENDPOINT_PAIR",
        "JOIN",
        "reverse the typed canonical endpoint pair",
        "edge",
        lambda row: row.__setitem__(
            "canonical_component_edge_endpoint_pair",
            list(reversed(row["canonical_component_edge_endpoint_pair"])),
        ),
    )
    semantic(
        "S23_EDGE_SIGNATURE",
        "SIGNATURE",
        "replace edge complete-signature commitment",
        "edge",
        set_value(
            "complete_10_field_return_signature_sha256", "f" * 64
        ),
    )
    semantic(
        "S24_EDGE_KEY",
        "KEY",
        "replace edge official key",
        "edge",
        set_value("official_key_id", "forged-edge-key"),
    )
    semantic(
        "S25_EDGE_SEMANTICS",
        "SEMANTICS",
        "promote overlap to occurrence identity",
        "edge",
        set_value("edge_semantics", "OCCURRENCE_IDENTITY"),
    )
    semantic(
        "S26_IDENTITY_CREDIT",
        "NONPROMOTION",
        "grant forbidden occurrence-identity collapse credit",
        "edge",
        set_value("formal_occurrence_identity_collapse_credit", 1),
    )
    semantic(
        "S27_COMPONENT_UNION_CREDIT",
        "NONPROMOTION",
        "grant forbidden component-union credit",
        "edge",
        set_value("formal_component_union_credit", 1),
    )
    semantic(
        "S28_DSU_RANK_CREDIT",
        "NONPROMOTION",
        "grant forbidden DSU rank reduction",
        "edge",
        set_value("formal_DSU_rank_reduction_credit", 1),
    )
    semantic(
        "S29_POST_QUOTIENT_ID",
        "NONPROMOTION",
        "invent a post-Round300C quotient component",
        "edge",
        set_value("post_Round300C_quotient_component_id", "forged-quotient"),
    )
    semantic(
        "S30_FRONTIER_EXHAUSTION",
        "NONPROMOTION",
        "claim the withheld frontier is complete",
        "result",
        lambda row: row["strict_nonpromotion"].__setitem__(
            "complete_virtual_new_occurrence_frontier_claimed", True
        ),
    )
    semantic(
        "S31_WITHHELD_SHEETS",
        "INVENTORY",
        "erase withheld Round248 wall-sheet inventory",
        "result",
        lambda row: row["strict_nonpromotion"].__setitem__(
            "withheld_Round248_wall_sheet_count", 0
        ),
    )
    semantic(
        "S32_NONINCIDENT_COUNT",
        "INVENTORY",
        "change exact nonincident new-occurrence denominator",
        "result",
        lambda row: row["strict_nonpromotion"].__setitem__(
            "nonincident_new_occurrence_count", 298_425
        ),
    )
    semantic(
        "S33_QUOTIENT_CREDIT",
        "NONPROMOTION",
        "grant forbidden quotient credit",
        "result",
        lambda row: row["strict_nonpromotion"].__setitem__(
            "quotient_credit", 1
        ),
    )
    semantic(
        "S34_MAXIMALITY_CREDIT",
        "NONPROMOTION",
        "grant forbidden maximality credit",
        "result",
        lambda row: row["strict_nonpromotion"].__setitem__(
            "maximality_credit", 1
        ),
    )
    semantic(
        "S35_FIBRE_CREDIT",
        "NONPROMOTION",
        "grant forbidden fibre credit",
        "result",
        lambda row: row["strict_nonpromotion"].__setitem__(
            "fibre_credit", 1
        ),
    )
    semantic(
        "S36_GLOBAL_DISPOSITION",
        "NONPROMOTION",
        "grant forbidden global-disposition credit",
        "result",
        lambda row: row["strict_nonpromotion"].__setitem__(
            "global_disposition_credit", 1
        ),
    )

    specs.extend(
        [
            (
                "B01_DUPLICATE_JSON_KEY",
                "JSON_BOUNDARY",
                "duplicate JSON object key",
                lambda: strict_json(b'{"x":1,"x":2}'),
                False,
            ),
            (
                "B02_NONFINITE_JSON",
                "JSON_BOUNDARY",
                "nonfinite JSON number",
                lambda: strict_json(b'{"x":NaN}'),
                False,
            ),
            (
                "B03_NUL_JSON",
                "JSON_BOUNDARY",
                "NUL-appended JSON",
                lambda: strict_json(b'{"x":1}' + bytes([0])),
                False,
            ),
            (
                "B04_GZIP_TRAILING",
                "GZIP_BOUNDARY",
                "valid member with trailing bytes",
                lambda: strict_gzip(
                    deterministic_gzip({"x": 1}) + b"trailing"
                ),
                False,
            ),
            (
                "B05_GZIP_MULTIMEMBER",
                "GZIP_BOUNDARY",
                "two concatenated GZIP members",
                lambda: strict_gzip(
                    deterministic_gzip({"x": 1})
                    + deterministic_gzip({"x": 2})
                ),
                False,
            ),
            (
                "B06_GZIP_TRUNCATED",
                "GZIP_BOUNDARY",
                "truncated GZIP member",
                lambda: strict_gzip(deterministic_gzip({"x": 1})[:-5]),
                False,
            ),
            (
                "B07_GZIP_SIZE_CAP",
                "GZIP_BOUNDARY",
                "compressed payload exceeding explicit cap",
                lambda: strict_gzip(
                    deterministic_gzip({"x": "a" * 100}), limit=16
                ),
                False,
            ),
        ]
    )

    boundary_rows: list[dict[str, Any]] = []
    for attack_id, category, description, action, reclosed in specs:
        boundary_rows.append(
            rejected_attack(
                attack_id,
                category,
                description,
                action,
                reclosed=reclosed,
            )
        )

    with tempfile.NamedTemporaryFile(dir=HERE, delete=False) as stream:
        target = Path(stream.name)
        stream.write(b"x")
    symlink = HERE / (".round300c_symlink_" + target.name)
    hardlink = HERE / (".round300c_hardlink_" + target.name)
    try:
        os.symlink(target.name, symlink)
        os.link(target, hardlink)
        for attack_id, category, description, path in (
            (
                "B08_SYMLINK_PATH",
                "PATH_BOUNDARY",
                "symlink input object",
                symlink,
            ),
            (
                "B09_HARDLINK_PATH",
                "PATH_BOUNDARY",
                "multiply linked input object",
                hardlink,
            ),
            (
                "B10_TRAVERSAL_PATH",
                "PATH_BOUNDARY",
                "lexical parent traversal",
                HERE / ".." / HERE.name / target.name,
            ),
        ):
            boundary_rows.append(
                rejected_attack(
                    attack_id,
                    category,
                    description,
                    lambda p=path: safe_regular(p),
                    reclosed=False,
                )
            )
    finally:
        for path in (symlink, hardlink, target):
            if path.is_symlink() or path.exists():
                path.unlink()

    need(
        len(boundary_rows) == 46
        and sum(
            row["cryptographic_reclosure_completed"]
            for row in boundary_rows
        )
        == 36
        and all(
            row["independent_verification_status"] == "REJECTED"
            for row in boundary_rows
        ),
        "46 attacks rejected, 36 semantic fully reclosed",
    )
    value = {
        "schema": ATTACK_SCHEMA,
        "status":
            "PASS_46_OF_46_REJECTED__36_FULLY_RECLOSED_SEMANTIC__"
            "10_JSON_GZIP_PATH_BOUNDARY",
        "execution_status": "EXECUTED_BY_INDEPENDENT_CACHELESS_VERIFIER",
        "candidate_basis": {
            PRODUCER.name: PRODUCER_SHA256,
            WITNESS_LEDGER.name: WITNESS_FILE_SHA256,
            EDGE_LEDGER.name: EDGE_FILE_SHA256,
            RESULT.name: RESULT_FILE_SHA256,
            "result_sha256": RESULT_SELF_SHA256,
        },
        "attack_count": 46,
        "rejected_count": 46,
        "accepted_count": 0,
        "fully_reclosed_semantic_attack_count": 36,
        "JSON_GZIP_path_boundary_attack_count": 10,
        "all_attacks_independently_rejected": True,
        "producer_imported_executed_or_parsed": False,
        "row_hashes_sha256": digest(
            [row["row_sha256"] for row in boundary_rows]
        ),
        "rows_sha256": digest(boundary_rows),
        "attacks": boundary_rows,
        "seed_affects_output": False,
    }
    value["attack_suite_sha256"] = digest(value)
    return value


def build_verification(
    expected: dict[str, Any],
    attack_value: dict[str, Any],
    attack_bytes: bytes,
) -> dict[str, Any]:
    result = expected["result"]
    value = {
        "schema": VERIFICATION_SCHEMA,
        "status":
            "PASS_INDEPENDENT_CACHELESS_ROUND300C__"
            "94660_POSITIVE_3D_CARRIERS__"
            "231503_EXACT_CANDIDATE_COMPARISONS__"
            "6322_WITNESSES__6314_CANONICAL_EDGES__"
            "46_OF_46_ATTACKS_REJECTED__STRICT_NONPROMOTION",
        "artifact_pins": {
            **{
                filename: expected_hash
                for filename, expected_hash in sorted(INPUTS.values())
            },
            PRODUCER.name: PRODUCER_SHA256,
            WITNESS_LEDGER.name: WITNESS_FILE_SHA256,
            EDGE_LEDGER.name: EDGE_FILE_SHA256,
            RESULT.name: RESULT_FILE_SHA256,
            ATTACKS.name: hashlib.sha256(attack_bytes).hexdigest(),
            Path(__file__).name: file_sha256(Path(__file__).resolve()),
        },
        "independence_contract": {
            "Round300C_producer_imported_or_executed": False,
            "Round300C_producer_parsed_as_Python": False,
            "Round300C_producer_bytes_used_only_as_inert_SHA256_pin": True,
            "candidate_ledgers_or_result_used_as_expected_row_oracle": False,
            "cache_pickle_or_bytecode_input_used": False,
            "expected_objects_rebuilt_before_candidate_open": True,
            "exact_rational_arithmetic_used": True,
            "all_selected_input_files_byte_pinned": True,
            "all_selected_source_table_and_row_commitments_recomputed": True,
        },
        "candidate_exact_equality": {
            "witness_ledger_object_equal_to_reconstruction": True,
            "witness_ledger_deterministic_GZIP_bytes_equal": True,
            "witness_ledger_file_sha256": WITNESS_FILE_SHA256,
            "edge_ledger_object_equal_to_reconstruction": True,
            "edge_ledger_deterministic_GZIP_bytes_equal": True,
            "edge_ledger_file_sha256": EDGE_FILE_SHA256,
            "result_object_equal_to_reconstruction": True,
            "result_canonical_JSON_bytes_equal": True,
            "result_file_sha256": RESULT_FILE_SHA256,
            "result_self_sha256": RESULT_SELF_SHA256,
        },
        "source_reconstruction": {
            **expected["source_audit"],
            "Round266_valid_virtual_node_count": 133_284,
            "Round266_inherited_virtual_stratum_count": 6_388,
            "Round266_Round248_wall_bulk_count": 88_536,
            "Round266_Round248_wall_sheet_count": 38_360,
            "Round248_positive_wall_bulk_table_count": 88_936,
            "retained_Round248_positive_wall_bulk_count": 88_536,
            "dropped_empty_Round248_positive_wall_bulk_count": 400,
            "inherited_positive_3D_witness_count": 6_124,
            "withheld_inherited_2D_sheet_count": 264,
            "retained_positive_3D_carrier_count": 94_660,
            "complete_signature_group_count": 156,
            "Round294_registry_row_count": 431_208,
            "Round299A_refined_key_binding_row_count": 9_404,
        },
        "exact_geometry_audit": {
            "Round288_exact_rational_interval_candidate_comparison_count":
                229_663,
            "Round292_exact_transformed_interval_candidate_comparison_count":
                1_840,
            "total_exact_candidate_comparison_count": 231_503,
            "Round288_exact_t_p_s_positive_overlap_witness_count": 6_214,
            "Round292_exact_t2_p_s_physical_sign_overlap_witness_count": 108,
            "exact_positive_volume_witness_count": 6_322,
            "every_intersection_recomputed_from_source_boxes": True,
            "every_intersection_volume_recomputed_as_rational": True,
            "same_complete_signature_required": True,
            "same_official_key_required": True,
        },
        "edge_audit": {
            "canonical_root_occurrence_edge_count": 6_314,
            "incident_new_occurrence_count": 6_314,
            "nonincident_new_occurrence_count": 298_426,
            "edge_witness_multiplicity_histogram": {
                "1": 6_306,
                "2": 8,
            },
            "one_virtual_root_per_incident_occurrence": True,
            "every_witness_consumed_exactly_once": True,
            "occurrence_identity_collapse_count": 0,
        },
        "source_histograms": {
            "retained_carriers":
                result["scope"]["piece_histogram"],
            "positive_overlap_witnesses":
                result["witness_audit"][
                    "witness_histogram_by_virtual_piece_source"
                ],
        },
        "attack_audit": {
            "attack_suite_file_sha256":
                hashlib.sha256(attack_bytes).hexdigest(),
            "attack_suite_sha256": attack_value["attack_suite_sha256"],
            "attack_count": 46,
            "rejected_count": 46,
            "accepted_count": 0,
            "fully_reclosed_semantic_attack_count": 36,
            "JSON_GZIP_path_boundary_attack_count": 10,
            "semantic_inventory_geometry_key_signature_dedup_covered": True,
            "all_attacks_independently_rejected": True,
        },
        "strict_document_file_boundary": {
            "duplicate_free_integral_finite_single_document_JSON": True,
            "NUL_and_nonfinite_JSON_rejected": True,
            "single_member_trailing_free_bounded_GZIP": True,
            "GZIP_uncompressed_size_cap_bytes": MAX_GZIP_BYTES,
            "HERE_only_regular_non_symlink_non_hardlink_files": True,
            "file_size_cap_bytes": MAX_FILE_BYTES,
        },
        "strict_nonpromotion": {
            "complete_virtual_new_occurrence_frontier_claimed": False,
            "withheld_Round248_wall_sheet_count": 38_360,
            "withheld_inherited_2D_sheet_count": 264,
            "formal_occurrence_identity_collapse_credit": 0,
            "formal_occurrence_alias_credit": 0,
            "formal_new_occurrence_ID_credit": 0,
            "formal_component_union_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_quotient_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
            "post_Round300C_component_count": None,
            "component_DSU_status": "NOT_REBUILT",
            "maximality_status": "NOT_CERTIFIED",
            "exact_key_fibre_exhaustion_status": "NOT_CERTIFIED",
            "global_disposition_status": "NOT_CERTIFIED",
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "replay_contract": {
            "seed_argument_affects_output": False,
            "external_PYTHONHASHSEED_affects_output": False,
            "dual_seed_cacheless_byte_identical_replay_required": True,
        },
    }
    value["verification_sha256"] = digest(value)
    return value


def safe_write(path: Path, payload: bytes) -> None:
    need(
        path.parent == HERE
        and path.parent.resolve(strict=True) == HERE.resolve(strict=True)
        and not path.is_symlink(),
        "safe output path",
    )
    if path.exists():
        info = path.lstat()
        need(
            stat.S_ISREG(info.st_mode) and info.st_nlink == 1,
            "safe existing output file",
        )
    with tempfile.NamedTemporaryFile(
        mode="wb",
        dir=HERE,
        prefix="." + path.name + ".",
        delete=False,
    ) as stream:
        temporary = Path(stream.name)
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
    os.chmod(temporary, 0o600)
    os.replace(temporary, path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=300_311)
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()
    _ = arguments.seed

    safe_regular(Path(__file__).resolve(), Path(__file__).name)
    expected = reconstruct_expected()
    read_candidate(expected)
    attack_value = build_attacks(expected)
    attack_bytes = canonical(attack_value) + b"\n"
    verification = build_verification(expected, attack_value, attack_bytes)
    verification_bytes = canonical(verification) + b"\n"
    if arguments.no_write:
        safe_regular(ATTACKS, ATTACKS.name)
        safe_regular(VERIFICATION, VERIFICATION.name)
        need(
            ATTACKS.read_bytes() == attack_bytes
            and VERIFICATION.read_bytes() == verification_bytes,
            "byte-identical independent no-write replay",
        )
    else:
        safe_write(ATTACKS, attack_bytes)
        safe_write(VERIFICATION, verification_bytes)
    print(
        json.dumps(
            {
                "status": verification["status"],
                "attack_suite_file_sha256":
                    hashlib.sha256(attack_bytes).hexdigest(),
                "attack_suite_sha256": attack_value["attack_suite_sha256"],
                "verification_file_sha256":
                    hashlib.sha256(verification_bytes).hexdigest(),
                "verification_sha256":
                    verification["verification_sha256"],
                "exact_geometry_audit":
                    verification["exact_geometry_audit"],
                "edge_audit": verification["edge_audit"],
                "strict_nonpromotion": verification["strict_nonpromotion"],
                "write": not arguments.no_write,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
