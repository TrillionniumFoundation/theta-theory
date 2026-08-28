#!/usr/bin/env python3
"""Round306B1G0: freeze the real graph-source inventory and source joins.

This private, zero-credit producer joins the 38,624 finite graph sources to
their 38,624 sheet members and 76,848 graph-side incidences.  The joins are
source inventory only: they do not replace a source-free graph theorem or a
physical-incidence proof.  Those 154,096 missing theorems remain explicit
gap rows.  Official keys are copied only after ID/lineage joins and are never
used for routing.

The heavy implementation is present, but candidate publication is disabled
until a separate hostile audit sets ``AUDIT_AUTHORIZED``.  That gate is the
first candidate-mode operation, before any large input is opened and before
any directory or file is created.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
import ctypes
import errno
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat
import tempfile
from typing import Any, BinaryIO, Iterator, TextIO


class FreezeBlocked(RuntimeError):
    """Fail-closed byte, row, join, credit, or transaction violation."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise FreezeBlocked(label)


def discover_root(source: Path) -> Path:
    resolved = source.resolve()
    for ancestor in (resolved.parent, *resolved.parents):
        if (ancestor / "deliverables").is_dir() and (ancestor / ".venv-cm2").is_dir():
            return ancestor
    raise FreezeBlocked("workspace root not found")


ROOT = discover_root(Path(__file__))
DATA = ROOT / "deliverables"
PRIVATE_ROOT = ROOT / ".cm2-round306b1g0-private-candidates"
PREFIX = "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze"
SCHEMA = "cm2.round306b1g0.source-g-graph-source-inventory-and-join-freeze.v1"
ENCODER = json.JSONEncoder(sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)
HEX64 = re.compile(r"^[0-9a-f]{64}$")

R235 = "cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json"
R236 = "cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json"
R242 = "cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_certificate.json"
R245 = "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json"
R248 = "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json"
R264 = "cm2_round264_source_g_lower_dimensional_endpoint_correction_and_glue_closure_certificate.json"
B0 = "cm2_round306b0_source_g_r306a_universe_support_source_freeze_member_support_source_index.json.gz"

# Exact byte pins for every consumed source and every authority seal checked
# by candidate mode.  Certificate sizes are also frozen to catch truncation
# before hashing.
INPUT_PINS = {
    R235: "e340fa1a071d85a36b54d10a45ae2fdb9d70b8c90f4c21f054c6fc9505e5e787",
    "cm2_round235_source_g_single_endpoint_graph_word_key_partition_verification.json": "8009f857b45aa05848b84258f2081bd6de54ff04643387ea3e8fd9c74bdb0e2a",
    "cm2_round235_source_g_single_endpoint_graph_word_key_partition_manifest.sha256": "cf58b7d2f419ea252c3398665302fe6f5ff06436af20a56beaaa47e5ef822ea0",
    R236: "b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217",
    "cm2_round236_source_g_wall_residual_closure_and_root_key_partition_verification.json": "153238a6a6678565b58c376c890b6f962af7b59d5572fd949836756c947cec55",
    "cm2_round236_source_g_wall_residual_closure_and_root_key_partition_manifest.sha256": "28f6f6d2f5b0f10edba5cd473b4126a8fed098874849c2f579eadd92b30d324c",
    R242: "8d32c381e21c03aad6a531b7e5a527d295783b7e3e38baa1e6bcba20c40db22e",
    "cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_verification.json": "76ff0d996fd3f3d3a06f625d74fc7302e2bf47366d5667b3adfc4f8568c7eced",
    "cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_manifest.sha256": "6da30fe3f9438ec73dc9c7d1aac770d8e9730aa9564ab0c535f1596cdc09ef2f",
    R245: "c76662f7cb068127f3612a3655ae720662eead9b9210b5757d771693149883c1",
    "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_verification.json": "7b116fce6abfad827a19da4e6637bac50c784c0e53b84e9bfd9567abb35bef14",
    "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_manifest.sha256": "1aff29f3a42b618ca85e5a1d3c537307e32326f8d5092b82d4253a5bf6e1c4ac",
    R248: "fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311",
    "cm2_round248_source_g_wall_finite_key_retained_quotient_verification.json": "5e20ada49b5bca2e7ebaf6b78835c4ca1a6051e24960b7d00b3ae9d596f11a10",
    "cm2_round248_source_g_wall_finite_key_retained_quotient_manifest.sha256": "b1ddedd01041e71b5c12fa4989726815c8685e6df77f54d9dbddda64aaf89e07",
    R264: "ac9e9451e12621fd236fea39bc686e13b41ade62e5255de9c9cd98230763236f",
    "cm2_round264_source_g_lower_dimensional_endpoint_correction_and_glue_closure_verification.json": "16930e5d790ff934b74f3c715d3bdda8c6053e8c14e457b30b11efce260154a3",
    "cm2_round264_source_g_lower_dimensional_endpoint_correction_and_glue_closure_manifest.sha256": "34d5183f3e75989151cb5c918d907dc6bb6a33e23f8bd6ab262ded6e9542e534",
    B0: "c9a8649c8473bb6a170187e7f803e95748d2ff2198b1b846d97383dd5f0581af",
    "cm2_round306b0_source_g_r306a_universe_support_source_freeze_result.json": "badc000c6fadd8807b26a7c3511edc51796c962f150b438956e4c549fd0d5735",
    "cm2_round306b0_source_g_r306a_universe_support_source_freeze_verification.json": "f8acc3150d4663d92976a44ab1c3b35c7264f4c4d14808f9133f1184d3f4b590",
    "cm2_round306b0_source_g_r306a_universe_support_source_freeze_manifest.sha256": "9846b36d28bb1507b273de3e613a5ecd5ac6515258042bf8b91b89e0c156b269",
}
EXACT_SOURCE_SIZES = {R235: 67_765_471, R236: 2_061_199, R242: 13_734_655, R245: 20_683_081, R248: 205_148_977, R264: 406_539_851, B0: 162_499_140}

EXPECTED = {
    "graph_count": 38_624,
    "R242_graph_count": 264,
    "R245_graph_sheet_join_count": 264,
    "R245_graph_side_join_count": 528,
    "R245_incidence_count": 792,
    "R235_single_graph_count": 38_328,
    "R248_single_graph_sheet_join_count": 38_328,
    "R248_single_pre_correction_side_count": 76_656,
    "R264_correction_count": 400,
    "R264_invalid_absent_owner_edge_count": 184,
    "R264_present_phantom_count": 216,
    "R248_single_graph_side_join_count": 76_256,
    "R248_single_incidence_count": 114_584,
    "R236_double_partition_count": 16,
    "R236_double_graph_count": 32,
    "R248_double_graph_sheet_join_count": 32,
    "R248_double_distinct_side_member_count": 48,
    "R248_double_graph_side_join_count": 64,
    "R248_double_incidence_count": 96,
    "graph_sheet_join_count": 38_624,
    "graph_side_join_count": 76_848,
    "physical_incidence_count": 115_472,
    "distinct_B0_member_backbinding_count": 115_456,
    "graph_definition_gap_count": 38_624,
    "physical_incidence_gap_count": 115_472,
    "gap_count": 154_096,
}

IMPLEMENTATION_PRESENT = True
AUDIT_AUTHORIZED = True

FILES = {kind: PREFIX + suffix for kind, suffix in {
    "graph": "_graph_source_inventory.json.gz",
    "sheet": "_graph_sheet_join.json.gz",
    "side": "_graph_side_join.json.gz",
    "correction": "_r264_correction_disposition.json.gz",
    "member": "_b0_member_backbinding.json.gz",
    "gap": "_gap.json.gz",
    "result": "_result.json",
}.items()}
TABLES = {"graph": "graph_source_inventory_rows", "sheet": "graph_sheet_join_rows", "side": "graph_side_join_rows", "correction": "r264_correction_disposition_rows", "member": "b0_member_backbinding_rows", "gap": "gap_rows"}
ID_FIELDS = {"graph": "Round306B1G0_graph_source_inventory_row_id", "sheet": "Round306B1G0_graph_sheet_join_row_id", "side": "Round306B1G0_graph_side_join_row_id", "correction": "Round306B1G0_R264_correction_disposition_row_id", "member": "Round306B1G0_B0_member_backbinding_row_id", "gap": "Round306B1G0_gap_row_id"}


def canonical(value: Any) -> bytes:
    return ENCODER.encode(value).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def close_row(payload: dict[str, Any]) -> dict[str, Any]:
    need("row_sha256" not in payload, "row already closed")
    return {**payload, "row_sha256": digest(payload)}


def check_row(row: dict[str, Any], label: str) -> None:
    need(type(row) is dict and type(row.get("row_sha256")) is str, label + ":closed")
    payload = dict(row)
    claimed = payload.pop("row_sha256")
    need(claimed == digest(payload), label + ":row sha")


def _identity(info: os.stat_result) -> tuple[int, int, int, int]:
    return info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns


def open_pinned_fd(name: str) -> tuple[int, os.stat_result]:
    path = DATA / name
    info = os.lstat(path)
    need(path.parent == DATA and stat.S_ISREG(info.st_mode) and not path.is_symlink(), "regular input:" + name)
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0))
    try:
        before = os.fstat(descriptor)
        need(_identity(before) == _identity(info) and before.st_nlink == 1, "fd/path identity:" + name)
        if name in EXACT_SOURCE_SIZES:
            need(before.st_size == EXACT_SOURCE_SIZES[name], "exact source size:" + name)
        state = hashlib.sha256()
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            state.update(block)
        need(state.hexdigest() == INPUT_PINS[name], "input byte pin:" + name)
        need(_identity(os.fstat(descriptor)) == _identity(before), "stable hash fd:" + name)
        os.lseek(descriptor, 0, os.SEEK_SET)
        return descriptor, before
    except Exception:
        os.close(descriptor)
        raise


def verify_all_input_pins() -> None:
    for name in sorted(INPUT_PINS):
        descriptor, _ = open_pinned_fd(name)
        os.close(descriptor)


def inode_identity(info: os.stat_result) -> tuple[int, int]:
    return info.st_dev, info.st_ino


def hash_descriptor(descriptor: int) -> tuple[str, os.stat_result]:
    """Hash one already-open regular fd and prove byte/stat stability."""
    before = os.fstat(descriptor)
    need(stat.S_ISREG(before.st_mode), "hash descriptor regular")
    state = hashlib.sha256()
    os.lseek(descriptor, 0, os.SEEK_SET)
    while True:
        block = os.read(descriptor, 1 << 20)
        if not block:
            break
        state.update(block)
    after = os.fstat(descriptor)
    need(_identity(before) == _identity(after), "stable hashed descriptor")
    os.lseek(descriptor, 0, os.SEEK_SET)
    return state.hexdigest(), before


def formal_producer_path() -> Path:
    return DATA / (PREFIX + ".py")


def open_verified_running_producer() -> tuple[int, os.stat_result, str]:
    """Bind the canonical runtime path to one opened producer fd and bytes."""
    expected = formal_producer_path()
    need(expected.resolve(strict=True) == expected, "formal producer path is canonical")
    need(Path(__file__).resolve(strict=True) == expected, "runtime canonical path equals formal producer path")
    before_path = os.lstat(expected)
    need(
        stat.S_ISREG(before_path.st_mode)
        and not expected.is_symlink()
        and before_path.st_nlink == 1,
        "running producer regular single-link path",
    )
    descriptor = os.open(
        expected,
        os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0),
    )
    try:
        producer_sha256, descriptor_info = hash_descriptor(descriptor)
        after_path = os.lstat(expected)
        need(
            inode_identity(before_path) == inode_identity(descriptor_info)
            == inode_identity(after_path),
            "running producer path/fd inode identity",
        )
        need(
            _identity(before_path) == _identity(descriptor_info) == _identity(after_path),
            "running producer path/fd byte-stat stability",
        )
        return descriptor, descriptor_info, producer_sha256
    except Exception:
        os.close(descriptor)
        raise


def recheck_running_producer(
    descriptor: int,
    expected_info: os.stat_result,
    expected_sha256: str,
) -> None:
    """Recheck both the held fd and the formal pathname against admission."""
    observed_sha256, observed_info = hash_descriptor(descriptor)
    need(
        _identity(observed_info) == _identity(expected_info)
        and observed_sha256 == expected_sha256,
        "running producer fd remains byte-identical",
    )
    path = formal_producer_path()
    need(path.resolve(strict=True) == path, "formal producer path remains canonical")
    path_info = os.stat(path, follow_symlinks=False)
    need(
        stat.S_ISREG(path_info.st_mode)
        and path_info.st_nlink == 1
        and _identity(path_info) == _identity(expected_info),
        "running producer path remains bound to same fd bytes",
    )


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in result, "duplicate JSON key:" + key)
        result[key] = value
    return result


def _reject_number(label: str, value: str) -> Any:
    raise FreezeBlocked(label + ":" + value)


STRICT_DECODER = json.JSONDecoder(
    object_pairs_hook=unique_object,
    parse_float=lambda value: _reject_number("float", value),
    parse_constant=lambda value: _reject_number("constant", value),
)


def _seek_marker(stream: TextIO, marker: str, initial: str = "", *, scan_limit: int | None = None) -> str:
    need(marker != "", "nonempty marker")
    buffer = initial
    scanned = len(initial)
    while True:
        position = buffer.find(marker)
        if position >= 0:
            return buffer[position + len(marker):]
        block = stream.read(1 << 20)
        need(bool(block), "missing JSON marker:" + marker)
        scanned += len(block)
        need(scan_limit is None or scanned <= scan_limit, "JSON marker scan bound:" + marker)
        keep = max(0, len(marker) - 1)
        buffer = (buffer[-keep:] if keep else "") + block


def iter_strict_json_rows(stream: TextIO, initial: str = "", *, row_limit: int = 1 << 24) -> Iterator[dict[str, Any]]:
    """Parse one located JSON array strictly, one object at a time.

    Duplicate keys, floats, NaN/Infinity, non-object elements, leading or
    trailing commas, missing commas, truncation, and oversized rows all fail.
    The caller locates the exact source-table marker first.
    """
    buffer = initial
    first = True
    after_comma = False
    while True:
        buffer = buffer.lstrip()
        while not buffer:
            block = stream.read(1 << 20)
            need(bool(block), "truncated JSON row array")
            buffer += block
            buffer = buffer.lstrip()
        if buffer[0] == "]":
            need(not after_comma, "trailing JSON array comma")
            return
        if not first:
            need(buffer[0] == ",", "missing JSON row comma")
            buffer = buffer[1:]
            after_comma = True
            buffer = buffer.lstrip()
            while not buffer:
                block = stream.read(1 << 20)
                need(bool(block), "truncated row after comma")
                buffer += block
                buffer = buffer.lstrip()
            need(buffer[0] != "]", "trailing JSON array comma")
        else:
            need(buffer[0] != ",", "leading JSON array comma")
        while True:
            try:
                row, end = STRICT_DECODER.raw_decode(buffer)
                break
            except json.JSONDecodeError:
                need(len(buffer) <= row_limit, "JSON row size bound")
                block = stream.read(1 << 20)
                need(bool(block), "invalid or truncated JSON row")
                buffer += block
        need(type(row) is dict, "JSON row must be object")
        yield row
        buffer = buffer[end:]
        first = False
        after_comma = False


def stream_pinned_rows(name: str, markers: tuple[str, ...], *, compressed: bool = False) -> Iterator[dict[str, Any]]:
    """Hash and parse from the same open-file description (no path reopen)."""
    descriptor, before = open_pinned_fd(name)
    raw = os.fdopen(descriptor, "rb", closefd=True)
    binary: BinaryIO = gzip.GzipFile(fileobj=raw, mode="rb") if compressed else raw
    text = io.TextIOWrapper(binary, encoding="utf-8", errors="strict", newline="")
    try:
        buffer = ""
        for index, marker in enumerate(markers):
            buffer = _seek_marker(text, marker, buffer, scan_limit=(EXACT_SOURCE_SIZES.get(name) if index == 0 else 16_384))
        yield from iter_strict_json_rows(text, buffer)
        need(_identity(os.fstat(raw.fileno())) == _identity(before), "stable parse fd:" + name)
    finally:
        try:
            text.detach()
        except Exception:
            pass
        if compressed:
            binary.close()
        raw.close()


class ListHash:
    def __init__(self) -> None:
        self.state = hashlib.sha256(b"[")
        self.count = 0

    def add(self, value: Any) -> None:
        if self.count:
            self.state.update(b",")
        self.state.update(canonical(value))
        self.count += 1

    def finish(self) -> str:
        state = self.state.copy()
        state.update(b"]")
        return state.hexdigest()


class RowSpool:
    def __init__(self, kind: str) -> None:
        need(kind in ID_FIELDS, "known spool kind")
        self.kind = kind
        self.id_field = ID_FIELDS[kind]
        self.stream = tempfile.TemporaryFile(mode="w+b")
        self.rows, self.ids, self.hashes = ListHash(), ListHash(), ListHash()
        self.seen: set[str] = set()

    def add(self, payload: dict[str, Any]) -> dict[str, Any]:
        row = close_row(payload)
        row_id = row.get(self.id_field)
        need(type(row_id) is str and row_id not in self.seen, "unique spool row id:" + self.kind)
        self.seen.add(row_id)
        if self.rows.count:
            self.stream.write(b",")
        self.stream.write(canonical(row))
        self.rows.add(row)
        self.ids.add(row_id)
        self.hashes.add(row["row_sha256"])
        return row

    def metadata(self) -> dict[str, Any]:
        return {"row_count": self.rows.count, "row_ids_sha256": self.ids.finish(), "row_hashes_sha256": self.hashes.finish(), "rows_sha256": self.rows.finish()}

    def close(self) -> None:
        self.stream.close()


@dataclass(frozen=True)
class Feature:
    member_id: str
    package: str
    filename: str
    table: str
    row_sha256: str
    feature_kind: str
    role: str
    branch: str | None
    official_key_id: str
    source_edge_id: str | None = None
    source_edge_sha256: str | None = None


@dataclass(frozen=True)
class Graph:
    graph_id: str
    family: str
    source_round: int
    filename: str
    table: str
    source_row_id: str
    source_row_sha256: str
    interface_id: str
    endpoint_factor: str
    official_key_ids: tuple[str, ...]
    sheet: Feature
    sides: tuple[Feature, ...]
    correction_source_id: str | None = None


def graph_inventory_id(graph_id: str) -> str:
    return "round306b1g0-graph-source:" + digest(graph_id)


def backbinding_id(member_id: str) -> str:
    return "round306b1g0-b0-backbinding:" + digest(member_id)


def _ledger_rows(name: str, ledger_name: str) -> Iterator[dict[str, Any]]:
    return stream_pinned_rows(name, (f'"{ledger_name}":', '"rows":['))


def _plain_rows(name: str, array_name: str) -> Iterator[dict[str, Any]]:
    return stream_pinned_rows(name, (f'"{array_name}":[',))


def _feature(
    row: dict[str, Any], *, package: str, filename: str, table: str,
    id_field: str, kind: str, role: str, branch: str | None,
    key_field: str = "official_key_id", edge: dict[str, Any] | None = None,
) -> Feature:
    check_row(row, package + ":" + kind)
    return Feature(
        member_id=row[id_field], package=package, filename=filename,
        table=table, row_sha256=row["row_sha256"], feature_kind=kind,
        role=role, branch=branch, official_key_id=row[key_field],
        source_edge_id=(edge["mixed_sheet_edge_id"] if edge is not None else None),
        source_edge_sha256=(edge.get("row_sha256") if edge is not None else None),
    )


def load_r242_r245_graphs() -> list[Graph]:
    """Join 264 R242 graph rows to 264 sheets and 528 R245 sides."""
    patches: dict[str, dict[str, Any]] = {}
    for row in _ledger_rows(R242, "formal_positive_2D_transition_sheet_patch_ledger"):
        check_row(row, "R242 graph")
        interface = row["Round220_split_interface_id"]
        need(interface not in patches, "unique R242 graph interface")
        need(row["local_dimension"] == 2 and row["three_dimensional_coordinate_volume"] == 0, "R242 graph dimension")
        need(row["local_positive_2D_transition_sheet_patch_credit"] == 1, "R242 source local credit")
        patches[interface] = row
    need(len(patches) == EXPECTED["R242_graph_count"], "R242 graph census")

    nodes: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    graph_kinds = {"OWNER_OPEN_BULK", "SHADOW_OPEN_BULK", "HALF_OPEN_TRANSITION_SHEET"}
    node_count = 0
    for row in _ledger_rows(R245, "formal_retained_stratum_node_ledger"):
        check_row(row, "R245 node")
        kind = row["stratum_kind"]
        if kind not in graph_kinds:
            continue
        interface = row["Round220_split_interface_id"]
        need(interface in patches and kind not in nodes[interface], "R245 graph node routing")
        nodes[interface][kind] = row
        node_count += 1
    need(node_count == 3 * EXPECTED["R242_graph_count"] and set(nodes) == set(patches), "R245 graph node census")

    edges: dict[str, list[dict[str, Any]]] = defaultdict(list)
    edge_count = 0
    for row in _ledger_rows(R245, "formal_mixed_sheet_physical_edge_ledger"):
        check_row(row, "R245 edge")
        if row["edge_kind"] not in {"OWNER_BULK_TO_HALF_OPEN_SHEET", "SHADOW_BULK_TO_HALF_OPEN_SHEET"}:
            continue
        interface = row["Round220_split_interface_id"]
        need(interface in patches, "R245 graph edge interface")
        edges[interface].append(row)
        edge_count += 1
    need(edge_count == EXPECTED["R245_graph_side_join_count"] and set(edges) == set(patches), "R245 side-edge census")

    output: list[Graph] = []
    for interface in sorted(patches):
        patch = patches[interface]
        by_kind = nodes[interface]
        sheet = by_kind["HALF_OPEN_TRANSITION_SHEET"]
        owner = by_kind["OWNER_OPEN_BULK"]
        shadow = by_kind["SHADOW_OPEN_BULK"]
        need(len(edges[interface]) == 2, "two R245 sheet-side edges")
        edge_by_bulk: dict[str, dict[str, Any]] = {}
        for edge in edges[interface]:
            endpoints = {edge["left_node_id"], edge["right_node_id"]}
            need(sheet["retained_stratum_node_id"] in endpoints, "R245 edge contains sheet")
            endpoints.remove(sheet["retained_stratum_node_id"])
            need(len(endpoints) == 1, "R245 edge other endpoint")
            bulk = next(iter(endpoints))
            need(bulk in {owner["retained_stratum_node_id"], shadow["retained_stratum_node_id"]} and bulk not in edge_by_bulk, "R245 exact bulk endpoint")
            edge_by_bulk[bulk] = edge
        # Key equality is checked only after lineage/edge routing.
        need(patch["official_key_id"] == sheet["official_key_id"] == owner["official_key_id"] == shadow["official_key_id"], "R242/R245 key metadata consistency")
        sheet_feature = _feature(sheet, package="R245", filename=R245, table="formal_retained_stratum_node_ledger", id_field="retained_stratum_node_id", kind="SHEET", role="GRAPH_SHEET", branch=None)
        side_features = tuple(
            _feature(row, package="R245", filename=R245, table="formal_retained_stratum_node_ledger", id_field="retained_stratum_node_id", kind="POSITIVE_3D_SIDE", role=role, branch=role, edge=edge_by_bulk[row["retained_stratum_node_id"]])
            for role, row in (("OWNER_OPEN_BULK", owner), ("SHADOW_OPEN_BULK", shadow))
        )
        output.append(Graph(
            graph_id=patch["transition_sheet_patch_row_id"], family="R242_UNIQUE_TRANSITION_GRAPH",
            source_round=242, filename=R242, table="formal_positive_2D_transition_sheet_patch_ledger",
            source_row_id=patch["transition_sheet_patch_row_id"], source_row_sha256=patch["row_sha256"],
            interface_id=interface, endpoint_factor="transition_graph",
            official_key_ids=(patch["official_key_id"],), sheet=sheet_feature, sides=side_features,
        ))
    need(len(output) == EXPECTED["R242_graph_count"] and sum(len(row.sides) for row in output) == EXPECTED["R245_graph_side_join_count"], "complete R242/R245 join")
    return output


def load_r264_corrections() -> dict[str, dict[str, Any]]:
    corrections: dict[str, dict[str, Any]] = {}
    labels: Counter[str] = Counter()
    dispositions: Counter[str] = Counter()
    invalid_edges = 0
    for row in _ledger_rows(R264, "formal_endpoint_empty_branch_correction_disposition_ledger"):
        check_row(row, "R264 correction")
        source = row["source_partition_row_id"]
        need(source not in corrections, "unique R264 correction source")
        need(row["empty_branch_Round250_Round251_Round252_accepted_edge_incidence_count"] == 0, "R264 empty incidence zero")
        labels[row["empty_branch_label"]] += 1
        dispositions[row["disposition"]] += 1
        invalid_edges += row["invalid_Round248_owner_edge_id"] is not None
        corrections[source] = row
    need(len(corrections) == EXPECTED["R264_correction_count"], "R264 correction census")
    need(labels == {"EVENT_ABSENT": 184, "EVENT_PRESENT": 216}, "R264 400=184+216")
    need(invalid_edges == EXPECTED["R264_invalid_absent_owner_edge_count"], "R264 invalid edge census")
    need(dispositions == {
        "PRUNE_EMPTY_ABSENT_BULK_NODE_AND_INVALID_OWNER_EDGE__RETAIN_T0_SHEET": 184,
        "DROP_EMPTY_PRESENT_SINGLETON_PHANTOM_COMPONENT": 216,
    }, "R264 disposition census")
    return corrections


def _load_r248_graph_features() -> tuple[dict[tuple[str, str, str], dict[str, Any]], dict[str, dict[str, dict[str, Any]]]]:
    sheets: dict[tuple[str, str, str], dict[str, Any]] = {}
    sheet_histogram: Counter[str] = Counter()
    for row in _ledger_rows(R248, "formal_wall_half_open_sheet_owner_ledger"):
        check_row(row, "R248 sheet")
        kind = row["source_partition_kind"]
        if kind not in {"ROUND235_SINGLE_ENDPOINT_GRAPH_SHEET", "ROUND236_DOUBLE_ENDPOINT_GRAPH_SHEET"}:
            continue
        key = (kind, row["source_partition_row_id"], row["endpoint_factor"])
        need(key not in sheets, "unique R248 graph sheet")
        sheets[key] = row
        sheet_histogram[kind] += 1
    need(sheet_histogram == {"ROUND235_SINGLE_ENDPOINT_GRAPH_SHEET": 38_328, "ROUND236_DOUBLE_ENDPOINT_GRAPH_SHEET": 32}, "R248 graph sheet census")

    bulks: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    bulk_histogram: Counter[str] = Counter()
    for row in _ledger_rows(R248, "formal_wall_positive_volume_bulk_ledger"):
        check_row(row, "R248 bulk")
        kind = row["source_partition_kind"]
        if kind not in {"ROUND235_SINGLE_ENDPOINT_GRAPH_BRANCH", "ROUND236_DOUBLE_ENDPOINT_ARRANGEMENT_BRANCH"}:
            continue
        source, branch = row["source_partition_row_id"], row["branch_label"]
        need(branch not in bulks[source], "unique R248 graph branch")
        bulks[source][branch] = row
        bulk_histogram[kind] += 1
    need(bulk_histogram == {"ROUND235_SINGLE_ENDPOINT_GRAPH_BRANCH": 76_656, "ROUND236_DOUBLE_ENDPOINT_ARRANGEMENT_BRANCH": 48}, "R248 graph bulk census")
    return sheets, bulks


def _r248_sheet_feature(row: dict[str, Any]) -> Feature:
    return _feature(row, package="R248", filename=R248, table="formal_wall_half_open_sheet_owner_ledger", id_field="wall_sheet_node_id", kind="SHEET", role="GRAPH_SHEET", branch=None, key_field="owner_official_key_id")


def _r248_side_feature(row: dict[str, Any], role: str, edge: dict[str, Any] | None = None) -> Feature:
    return _feature(row, package="R248", filename=R248, table="formal_wall_positive_volume_bulk_ledger", id_field="wall_bulk_node_id", kind="POSITIVE_3D_SIDE", role=role, branch=row["branch_label"], edge=edge)


def load_r235_r236_r248_graphs(corrections: dict[str, dict[str, Any]]) -> list[Graph]:
    """Join 38,328 single and 32 double graphs through corrected R248."""
    sheets, bulks = _load_r248_graph_features()
    output: list[Graph] = []
    seen_single_sources: set[str] = set()
    seen_corrections: set[str] = set()
    single_count = 0
    single_sides = 0
    for row in _plain_rows(R235, "single_endpoint_graph_partition_rows"):
        source = row["endpoint_graph_partition_row_id"]
        interface = row["Round220_split_interface_id"]
        endpoint = row["active_endpoint_factor"]
        need(endpoint in {"source", "target"} and source not in seen_single_sources, "R235 graph identity")
        seen_single_sources.add(source)
        sheet = sheets[("ROUND235_SINGLE_ENDPOINT_GRAPH_SHEET", source, endpoint)]
        branches = bulks[source]
        need(set(branches) == {"EVENT_ABSENT", "EVENT_PRESENT"}, "R235 two R248 branches")
        need(sheet["Round220_split_interface_id"] == interface and all(item["Round220_split_interface_id"] == interface for item in branches.values()), "R235/R248 interface join")
        need(sheet["owner_wall_bulk_node_id"] == branches["EVENT_ABSENT"]["wall_bulk_node_id"], "R248 half-open absent owner")
        correction = corrections.get(source)
        kept = dict(branches)
        if correction is not None:
            need(correction["Round220_split_interface_id"] == interface, "R264 interface backjoin")
            empty = correction["empty_branch_label"]
            need(correction["empty_wall_bulk_node_id"] == branches[empty]["wall_bulk_node_id"] and correction["retained_t0_sheet_node_id"] == sheet["wall_sheet_node_id"], "R264 exact node/sheet backjoin")
            if empty == "EVENT_ABSENT":
                need(correction["invalid_Round248_owner_edge_id"] == sheet["owner_mixed_sheet_edge_id"], "R264 invalid owner edge backjoin")
            else:
                need(correction["invalid_Round248_owner_edge_id"] is None, "R264 phantom has no owner edge")
            del kept[empty]
            seen_corrections.add(source)
        # All key comparisons occur after source IDs, interface, branch, and
        # correction disposition have fixed the join.
        need(sheet["owner_official_key_id"] == row["event_absent_signature"]["official_key_id"], "R235/R248 sheet key metadata")
        for branch, bulk in branches.items():
            signature = row["event_absent_signature" if branch == "EVENT_ABSENT" else "event_present_signature"]
            need(bulk["official_key_id"] == signature["official_key_id"], "R235/R248 branch key metadata")
        absent_edge_valid = correction is None or correction["empty_branch_label"] != "EVENT_ABSENT"
        side_features = tuple(
            _r248_side_feature(bulk, branch, {"mixed_sheet_edge_id": sheet["owner_mixed_sheet_edge_id"]} if branch == "EVENT_ABSENT" and absent_edge_valid else None)
            for branch, bulk in sorted(kept.items())
        )
        output.append(Graph(
            graph_id=source, family="R235_SINGLE_ENDPOINT_GRAPH", source_round=235,
            filename=R235, table="single_endpoint_graph_partition_rows", source_row_id=source,
            source_row_sha256=digest(row), interface_id=interface, endpoint_factor=endpoint,
            official_key_ids=tuple(sorted({row["event_absent_signature"]["official_key_id"], row["event_present_signature"]["official_key_id"]})),
            sheet=_r248_sheet_feature(sheet), sides=side_features,
            correction_source_id=(source if correction is not None else None),
        ))
        single_count += 1
        single_sides += len(side_features)
    need(single_count == EXPECTED["R235_single_graph_count"] and single_sides == EXPECTED["R248_single_graph_side_join_count"], "complete R235/R248 single join")
    need(seen_corrections == set(corrections), "all R264 corrections consumed")

    double_partitions = 0
    double_sides = 0
    for row in _plain_rows(R236, "double_endpoint_partition_rows"):
        source = row["double_endpoint_partition_row_id"]
        interface = row["Round220_split_interface_id"]
        need(row["source_factor_strict_t_derivative_sign"] == row["target_factor_strict_t_derivative_sign"] == "STRICT_POSITIVE", "R236 exact double routing rule")
        branches = bulks[source]
        need(set(branches) == {"SAME_SIGN_EVENT_ABSENT", "NEGATIVE_TO_POSITIVE", "POSITIVE_TO_NEGATIVE"}, "R236 three R248 branches")
        routing = {"source": "NEGATIVE_TO_POSITIVE", "target": "POSITIVE_TO_NEGATIVE"}
        signatures = {"SAME_SIGN_EVENT_ABSENT": row["same_sign_event_absent_signature"], "NEGATIVE_TO_POSITIVE": row["negative_to_positive_signature"], "POSITIVE_TO_NEGATIVE": row["positive_to_negative_signature"]}
        for branch, bulk in branches.items():
            need(bulk["Round220_split_interface_id"] == interface and bulk["official_key_id"] == signatures[branch]["official_key_id"], "R236/R248 branch lineage then key metadata")
        for endpoint in ("source", "target"):
            sheet = sheets[("ROUND236_DOUBLE_ENDPOINT_GRAPH_SHEET", source, endpoint)]
            need(sheet["Round220_split_interface_id"] == interface and sheet["owner_wall_bulk_node_id"] == branches["SAME_SIGN_EVENT_ABSENT"]["wall_bulk_node_id"], "R236/R248 double sheet owner")
            need(sheet["owner_official_key_id"] == signatures["SAME_SIGN_EVENT_ABSENT"]["official_key_id"], "R236/R248 sheet key metadata")
            selected = ("SAME_SIGN_EVENT_ABSENT", routing[endpoint])
            sides = tuple(
                _r248_side_feature(branches[branch], endpoint + ":" + branch, {"mixed_sheet_edge_id": sheet["owner_mixed_sheet_edge_id"]} if branch == "SAME_SIGN_EVENT_ABSENT" else None)
                for branch in selected
            )
            graph_id = "round306b1g0-double-graph:" + digest([source, endpoint])
            output.append(Graph(
                graph_id=graph_id, family="R236_DOUBLE_ENDPOINT_GRAPH", source_round=236,
                filename=R236, table="double_endpoint_partition_rows", source_row_id=source,
                source_row_sha256=digest(row), interface_id=interface, endpoint_factor=endpoint,
                official_key_ids=tuple(sorted({item["official_key_id"] for item in signatures.values()})),
                sheet=_r248_sheet_feature(sheet), sides=sides,
            ))
            double_sides += len(sides)
        double_partitions += 1
    need(double_partitions == EXPECTED["R236_double_partition_count"] and double_sides == EXPECTED["R248_double_graph_side_join_count"], "complete R236/R248 double join")
    return output


def bind_b0_members(graphs: list[Graph]) -> tuple[dict[str, dict[str, Any]], dict[str, list[Feature]]]:
    """Backbind every distinct sheet/side member into the sealed B0 universe."""
    references: dict[str, list[Feature]] = defaultdict(list)
    for graph in graphs:
        references[graph.sheet.member_id].append(graph.sheet)
        for side in graph.sides:
            references[side.member_id].append(side)
    need(len(references) == EXPECTED["distinct_B0_member_backbinding_count"], "distinct feature member census")

    bound: dict[str, dict[str, Any]] = {}
    total_rows = 0
    for row in stream_pinned_rows(B0, ('"member_support_source_rows":[',), compressed=True):
        check_row(row, "Round306B0 member")
        total_rows += 1
        member = row["member_id"]
        if member not in references:
            continue
        need(member not in bound, "unique targeted B0 member")
        need(row["identity_class"] == "VALID_VIRTUAL_STRATUM" and row["member_identity_preserved"] is True, "B0 virtual identity")
        need(row["formal_maximality_credit"] == row["formal_fibre_credit"] == row["formal_global_disposition_credit"] == 0, "B0 zero credit")
        examples = references[member]
        first = examples[0]
        need(all(item.package == first.package and item.row_sha256 == first.row_sha256 and item.feature_kind == first.feature_kind for item in examples), "consistent repeated feature reference")
        if first.package == "R245":
            need(row["identity_tranche"] == "INHERITED_ROUND247_VIRTUAL_STRATUM", "B0 R245 tranche")
            need(row["inherited_virtual_source_package"] == "R245" and row["inherited_virtual_source_row_id"] == member and row["inherited_virtual_source_row_sha256"] == first.row_sha256, "B0 exact R245 lineage")
        else:
            tranche = "ROUND248_WALL_SHEET" if first.feature_kind == "SHEET" else "ROUND248_WALL_BULK"
            need(row["identity_tranche"] == tranche, "B0 R248 tranche")
            need(row["inherited_virtual_source_package"] is None and row["inherited_virtual_source_row_id"] is None and row["inherited_virtual_source_row_sha256"] is None, "B0 R248 has no inherited alias")
        denominator = "VIRTUAL_SHEET" if first.feature_kind == "SHEET" else "VIRTUAL_POSITIVE_3D"
        profile = "HALF_OPEN_2D_SHEET" if first.feature_kind == "SHEET" else "POSITIVE_3D_CARRIER"
        need(row["pair_denominator_class"] == denominator and row["physical_dimension_profile"] == profile, "B0 feature dimension")
        # This consistency check occurs after member-ID/source-lineage routing.
        need(all(row["official_key_id"] == item.official_key_id for item in examples), "B0 official-key metadata consistency")
        bound[member] = row
    need(total_rows == 564_492, "B0 complete row census")
    need(set(bound) == set(references), "complete B0 feature backbinding")
    return bound, references


def zero_credit() -> dict[str, int]:
    return {"graph_definition": 0, "physical_incidence": 0, "full_support": 0, "maximality": 0, "fibre": 0, "global_disposition": 0}


def _assert_zero_credit(value: Any, label: str = "root") -> None:
    if type(value) is dict:
        for key, item in value.items():
            if "credit" in key.lower():
                if type(item) is dict:
                    need(all(type(number) is int and number == 0 for number in item.values()), label + ":credit map")
                else:
                    need(type(item) is int and item == 0, label + ":credit scalar")
            else:
                _assert_zero_credit(item, label + ":" + key)
    elif type(value) is list:
        for index, item in enumerate(value):
            _assert_zero_credit(item, label + f":[{index}]")


def build_spools() -> tuple[dict[str, RowSpool], dict[str, Any]]:
    corrections = load_r264_corrections()
    graphs = load_r242_r245_graphs() + load_r235_r236_r248_graphs(corrections)
    need(len(graphs) == EXPECTED["graph_count"] and len({item.graph_id for item in graphs}) == len(graphs), "complete unique graph inventory")
    family_counts = Counter(item.family for item in graphs)
    need(family_counts == {"R242_UNIQUE_TRANSITION_GRAPH": 264, "R235_SINGLE_ENDPOINT_GRAPH": 38_328, "R236_DOUBLE_ENDPOINT_GRAPH": 32}, "graph family census")
    sheet_count = len(graphs)
    side_count = sum(len(item.sides) for item in graphs)
    need(sheet_count == EXPECTED["graph_sheet_join_count"] and side_count == EXPECTED["graph_side_join_count"] and sheet_count + side_count == EXPECTED["physical_incidence_count"], "incidence arithmetic")
    b0, references = bind_b0_members(graphs)

    spools = {kind: RowSpool(kind) for kind in ("graph", "sheet", "side", "correction", "member", "gap")}

    for member in sorted(references):
        source = b0[member]
        feature = references[member][0]
        payload = {
            "schema": SCHEMA + ".b0-member-backbinding-row.v1",
            ID_FIELDS["member"]: backbinding_id(member),
            "member_id": member,
            "feature_kind": feature.feature_kind,
            "feature_source_package": feature.package,
            "feature_source_filename": feature.filename,
            "feature_source_file_sha256": INPUT_PINS[feature.filename],
            "feature_source_table": feature.table,
            "feature_source_row_sha256": feature.row_sha256,
            "Round306B0_member_support_source_row_id": source["Round306B0_member_support_source_row_id"],
            "Round306B0_member_support_source_row_sha256": source["row_sha256"],
            "Round306A_component_id": source["Round306A_component_id"],
            "identity_tranche": source["identity_tranche"],
            "physical_dimension_profile": source["physical_dimension_profile"],
            "official_key_id_metadata_only": source["official_key_id"],
            "official_key_used_as_join_or_routing_filter": False,
            "formal_credit": zero_credit(),
        }
        _assert_zero_credit(payload, "member payload")
        spools["member"].add(payload)

    correction_output_ids: dict[str, str] = {}
    for source in sorted(corrections):
        row = corrections[source]
        output_id = "round306b1g0-r264-correction:" + digest(row["endpoint_empty_branch_disposition_row_id"])
        correction_output_ids[source] = output_id
        payload = {
            "schema": SCHEMA + ".r264-correction-disposition-row.v1",
            ID_FIELDS["correction"]: output_id,
            "R264_correction_disposition_row_id": row["endpoint_empty_branch_disposition_row_id"],
            "R264_correction_disposition_row_sha256": row["row_sha256"],
            "source_partition_row_id": source,
            "empty_branch_label": row["empty_branch_label"],
            "empty_wall_bulk_node_id": row["empty_wall_bulk_node_id"],
            "nonempty_branch_label": row["nonempty_branch_label"],
            "nonempty_wall_bulk_node_id": row["nonempty_wall_bulk_node_id"],
            "retained_t0_sheet_node_id": row["retained_t0_sheet_node_id"],
            "invalid_Round248_owner_edge_id": row["invalid_Round248_owner_edge_id"],
            "disposition": row["disposition"],
            "source_component_count_delta": -1 if row["empty_branch_label"] == "EVENT_PRESENT" else 0,
            "empty_side_join_suppressed": True,
            "official_key_used_as_join_or_routing_filter": False,
            "formal_credit": zero_credit(),
        }
        _assert_zero_credit(payload, "correction payload")
        spools["correction"].add(payload)

    incidence_family_counts: Counter[str] = Counter()
    for graph in sorted(graphs, key=lambda item: item.graph_id):
        inventory_id = graph_inventory_id(graph.graph_id)
        sheet_join_id = "round306b1g0-graph-sheet:" + digest([graph.graph_id, graph.sheet.member_id])
        graph_payload = {
            "schema": SCHEMA + ".graph-source-inventory-row.v1",
            ID_FIELDS["graph"]: inventory_id,
            "graph_id": graph.graph_id,
            "graph_family": graph.family,
            "source_round": graph.source_round,
            "source_filename": graph.filename,
            "source_file_sha256": INPUT_PINS[graph.filename],
            "source_table": graph.table,
            "source_row_id": graph.source_row_id,
            "source_row_sha256": graph.source_row_sha256,
            "Round220_split_interface_id": graph.interface_id,
            "endpoint_factor": graph.endpoint_factor,
            "graph_local_dimension": 2,
            "graph_three_dimensional_coordinate_volume": 0,
            "graph_sheet_join_row_id": sheet_join_id,
            "graph_side_join_count": len(graph.sides),
            "R264_correction_disposition_row_id": correction_output_ids.get(graph.correction_source_id or ""),
            "official_key_ids_metadata_only": list(graph.official_key_ids),
            "official_key_used_as_join_or_routing_filter": False,
            "source_graph_definition_proved": False,
            "formal_credit": zero_credit(),
        }
        _assert_zero_credit(graph_payload, "graph payload")
        spools["graph"].add(graph_payload)
        spools["gap"].add({
            "schema": SCHEMA + ".gap-row.v1",
            ID_FIELDS["gap"]: "round306b1g0-gap:graph:" + digest(graph.graph_id),
            "gap_kind": "SOURCE_FREE_GRAPH_DEFINITION_THEOREM_PENDING",
            "graph_source_inventory_row_id": inventory_id,
            "incidence_join_row_id": None,
            "member_id": graph.sheet.member_id,
            "required_closure": "derive and independently interval-verify the source-free graph equation on the complete base cell",
            "formal_credit": zero_credit(),
        })

        sheet_b0 = b0[graph.sheet.member_id]
        sheet_payload = {
            "schema": SCHEMA + ".graph-sheet-join-row.v1",
            ID_FIELDS["sheet"]: sheet_join_id,
            "graph_source_inventory_row_id": inventory_id,
            "graph_id": graph.graph_id,
            "graph_family": graph.family,
            "Round220_split_interface_id": graph.interface_id,
            "endpoint_factor": graph.endpoint_factor,
            "sheet_member_id": graph.sheet.member_id,
            "sheet_source_package": graph.sheet.package,
            "sheet_source_filename": graph.sheet.filename,
            "sheet_source_file_sha256": INPUT_PINS[graph.sheet.filename],
            "sheet_source_table": graph.sheet.table,
            "sheet_source_row_sha256": graph.sheet.row_sha256,
            "B0_member_backbinding_row_id": backbinding_id(graph.sheet.member_id),
            "Round306B0_member_support_source_row_id": sheet_b0["Round306B0_member_support_source_row_id"],
            "join_basis": "SOURCE_ROW_ID_INTERFACE_AND_ENDPOINT_FACTOR",
            "official_key_id_metadata_only": graph.sheet.official_key_id,
            "official_key_used_as_join_or_routing_filter": False,
            "physical_incidence_proved": False,
            "formal_credit": zero_credit(),
        }
        _assert_zero_credit(sheet_payload, "sheet payload")
        spools["sheet"].add(sheet_payload)
        spools["gap"].add({
            "schema": SCHEMA + ".gap-row.v1",
            ID_FIELDS["gap"]: "round306b1g0-gap:incidence:" + digest(sheet_join_id),
            "gap_kind": "GRAPH_TO_SHEET_PHYSICAL_IDENTIFICATION_THEOREM_PENDING",
            "graph_source_inventory_row_id": inventory_id,
            "incidence_join_row_id": sheet_join_id,
            "member_id": graph.sheet.member_id,
            "required_closure": "prove the source graph equals the sealed sheet member without using key metadata as a filter",
            "formal_credit": zero_credit(),
        })
        incidence_family_counts[graph.family + ":SHEET"] += 1

        for side in graph.sides:
            join_id = "round306b1g0-graph-side:" + digest([graph.graph_id, side.member_id, side.role])
            side_b0 = b0[side.member_id]
            side_payload = {
                "schema": SCHEMA + ".graph-side-join-row.v1",
                ID_FIELDS["side"]: join_id,
                "graph_source_inventory_row_id": inventory_id,
                "graph_id": graph.graph_id,
                "graph_family": graph.family,
                "Round220_split_interface_id": graph.interface_id,
                "endpoint_factor": graph.endpoint_factor,
                "side_role": side.role,
                "side_branch_label": side.branch,
                "side_member_id": side.member_id,
                "side_source_package": side.package,
                "side_source_filename": side.filename,
                "side_source_file_sha256": INPUT_PINS[side.filename],
                "side_source_table": side.table,
                "side_source_row_sha256": side.row_sha256,
                "source_edge_id_metadata_only": side.source_edge_id,
                "source_edge_row_sha256_metadata_only": side.source_edge_sha256,
                "B0_member_backbinding_row_id": backbinding_id(side.member_id),
                "Round306B0_member_support_source_row_id": side_b0["Round306B0_member_support_source_row_id"],
                "join_basis": "SEALED_SOURCE_PARTITION_BRANCH_AND_R264_CORRECTION_DISPOSITION",
                "official_key_id_metadata_only": side.official_key_id,
                "official_key_used_as_join_or_routing_filter": False,
                "physical_incidence_proved": False,
                "formal_credit": zero_credit(),
            }
            _assert_zero_credit(side_payload, "side payload")
            spools["side"].add(side_payload)
            spools["gap"].add({
                "schema": SCHEMA + ".gap-row.v1",
                ID_FIELDS["gap"]: "round306b1g0-gap:incidence:" + digest(join_id),
                "gap_kind": "GRAPH_SIDE_POSITIVE_3D_PHYSICAL_INCIDENCE_THEOREM_PENDING",
                "graph_source_inventory_row_id": inventory_id,
                "incidence_join_row_id": join_id,
                "member_id": side.member_id,
                "required_closure": "derive a source-free one-sided embedding and verify physical incidence across the graph",
                "formal_credit": zero_credit(),
            })
            incidence_family_counts[graph.family + ":SIDE"] += 1

    expected_spool_counts = {"graph": 38_624, "sheet": 38_624, "side": 76_848, "correction": 400, "member": 115_456, "gap": 154_096}
    need(all(spools[kind].rows.count == count for kind, count in expected_spool_counts.items()), "exact spool counts")
    audit = {
        "graph_family_histogram": dict(sorted(family_counts.items())),
        "incidence_family_histogram": dict(sorted(incidence_family_counts.items())),
        "graph_count": spools["graph"].rows.count,
        "graph_sheet_join_count": spools["sheet"].rows.count,
        "graph_side_join_count": spools["side"].rows.count,
        "physical_incidence_count": spools["sheet"].rows.count + spools["side"].rows.count,
        "R264_correction_count": spools["correction"].rows.count,
        "distinct_B0_member_backbinding_count": spools["member"].rows.count,
        "gap_count": spools["gap"].rows.count,
        "official_key_used_as_join_or_routing_filter": False,
        "source_free_graph_definition_complete": False,
        "physical_incidence_theorem_complete": False,
        "all_output_formal_credit_zero": True,
    }
    return spools, audit


def contract() -> dict[str, Any]:
    authorization_state = "AUDIT_AUTHORIZED" if AUDIT_AUTHORIZED else "AUDIT_NOT_AUTHORIZED"
    return {
        "schema": SCHEMA + ".contract.v1",
        "status": (
            "IMPLEMENTED_AUDIT_AUTHORIZED__TRANSACTION_READY_ZERO_CREDIT"
            if AUDIT_AUTHORIZED else
            "IMPLEMENTED_AUDIT_NOT_AUTHORIZED__CANDIDATE_HARD_BLOCKED_ZERO_CREDIT"
        ),
        "implementation_present": IMPLEMENTATION_PRESENT,
        "audit_authorized": AUDIT_AUTHORIZED,
        "authorization_state": authorization_state,
        "candidate_mode_expected_to_block": not AUDIT_AUTHORIZED,
        "candidate_block_occurs_before_large_input_open": not AUDIT_AUTHORIZED,
        "candidate_block_occurs_before_any_write": not AUDIT_AUTHORIZED,
        "candidate_transaction_hardening_implemented": True,
        "candidate_transaction_hardening_required_before_authorization": False,
        "transaction_contract": {
            "runtime_canonical_path_equals_formal_producer_path": True,
            "running_script_path_fd_inode_bytes_and_sha256_bound": True,
            "running_script_stability_rechecked_before_and_after_publish": True,
            "all_candidate_writes_are_stage_dirfd_bound": True,
            "all_output_creation_uses_O_NOFOLLOW_and_O_EXCL": True,
            "created_output_inode_registered_before_strict_admission": True,
            "created_output_fd_closed_on_every_writer_exception": True,
            "every_output_requires_regular_mode0600_nlink1": True,
            "every_output_name_inode_and_sha256_rechecked_before_publish": True,
            "random_nonce_stage_name": True,
            "created_stage_inode_bound_before_mode_admission": True,
            "exact_candidate_file_census_required": True,
            "stage_name_inode_checked_before_publish": True,
            "candidate_name_inode_checked_after_publish": True,
            "post_rename_file_inode_and_sha256_checks_required": True,
            "failed_transaction_cleanup_is_exact_inode_scoped": True,
            "private_root_stage_and_candidate_directory_fsync_required": True,
            "SIGKILL_or_power_loss_orphan_recovery_implemented": False,
            "orphan_stage_auto_reaping_implemented": False,
            "same_uid_namespace_mutation_after_final_check_eliminated": False,
            "independent_verifier_still_required": True,
            "lightweight_transaction_self_test_claim_count": 14,
        },
        "fd_bound_hash_and_parse": True,
        "strict_json_row_parser": {
            "duplicate_keys_rejected": True,
            "floats_and_nonfinite_constants_rejected": True,
            "non_object_rows_rejected": True,
            "leading_trailing_or_missing_commas_rejected": True,
            "truncation_and_row_size_overflow_rejected": True,
        },
        "exact_input_file_pins": dict(sorted(INPUT_PINS.items())),
        "exact_large_source_sizes": dict(sorted(EXACT_SOURCE_SIZES.items())),
        "exact_expected": dict(EXPECTED),
        "implemented_source_joins": {
            "R242_to_R245": {
                "graph_count": 264,
                "sheet_join_count": 264,
                "side_join_count": 528,
                "incidence_count": 792,
                "join_keys": ["Round220_split_interface_id", "R245 node kind", "R245 physical edge endpoints"],
            },
            "R235_to_R248_after_R264": {
                "single_graph_count": 38_328,
                "sheet_join_count": 38_328,
                "pre_correction_side_count": 76_656,
                "suppressed_empty_side_count": 400,
                "side_join_count": 76_256,
                "incidence_count": 114_584,
            },
            "R236_to_R248": {
                "double_partition_count": 16,
                "double_graph_count": 32,
                "sheet_join_count": 32,
                "distinct_side_member_count": 48,
                "side_join_count": 64,
                "incidence_count": 96,
                "source_graph_side_branches": ["SAME_SIGN_EVENT_ABSENT", "NEGATIVE_TO_POSITIVE"],
                "target_graph_side_branches": ["SAME_SIGN_EVENT_ABSENT", "POSITIVE_TO_NEGATIVE"],
            },
            "R264_correction_dispositions": {
                "total": 400,
                "prune_empty_EVENT_ABSENT_and_invalid_owner_edge": 184,
                "drop_empty_EVENT_PRESENT_phantom": 216,
                "retained_t0_sheet_count": 400,
            },
            "Round306B0_member_backbinding": {
                "distinct_member_count": 115_456,
                "R245_lineage_bound_by_inherited_source_row": True,
                "R248_lineage_bound_by_member_id_and_identity_tranche": True,
            },
        },
        "output_spool_schema": {
            kind: {"filename": FILES[kind], "table": TABLES[kind], "id_field": ID_FIELDS[kind]}
            for kind in ("graph", "sheet", "side", "correction", "member", "gap")
        },
        "gap_schema": {
            "id_field": ID_FIELDS["gap"],
            "required_fields": ["schema", ID_FIELDS["gap"], "gap_kind", "graph_source_inventory_row_id", "incidence_join_row_id", "member_id", "required_closure", "formal_credit", "row_sha256"],
            "graph_definition_gap_count": 38_624,
            "physical_incidence_gap_count": 115_472,
            "total_gap_count": 154_096,
        },
        "strict_boundary": {
            "inventory_and_source_joins_frozen": True,
            "source_free_graph_definition_complete": False,
            "physical_incidence_theorem_complete": False,
            "official_key_is_metadata_only": True,
            "official_key_used_as_join_or_routing_filter": False,
            "all_output_formal_credit_zero": True,
            "formal_graph_definition_credit": 0,
            "formal_physical_incidence_credit": 0,
            "formal_full_support_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
            "root_theorem_claimed": False,
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "candidate_files": [FILES[kind] for kind in ("graph", "sheet", "side", "correction", "member", "gap", "result")],
        "private_candidate_root": PRIVATE_ROOT.name,
    }


def _must_reject_json(initial: str, label: str) -> None:
    try:
        list(iter_strict_json_rows(io.StringIO(""), initial))
    except FreezeBlocked:
        return
    raise FreezeBlocked("strict parser accepted:" + label)


def self_test() -> dict[str, Any]:
    need(IMPLEMENTATION_PRESENT, "implementation present")
    need(264 + 38_328 + 32 == EXPECTED["graph_count"], "38624 graph arithmetic")
    need(264 + 528 == EXPECTED["R245_incidence_count"], "R245 incidence arithmetic")
    need(38_328 + 76_256 == EXPECTED["R248_single_incidence_count"], "R248 single incidence arithmetic")
    need(32 + 64 == EXPECTED["R248_double_incidence_count"], "R248 double incidence arithmetic")
    need(792 + 114_584 + 96 == EXPECTED["physical_incidence_count"], "115472 incidence arithmetic")
    need(184 + 216 == EXPECTED["R264_correction_count"], "400=184+216")
    need(76_656 - 400 == EXPECTED["R248_single_graph_side_join_count"], "corrected single sides")
    need(38_624 + 76_848 == EXPECTED["physical_incidence_count"], "sheet plus side incidences")
    need(792 + 114_584 + 80 == EXPECTED["distinct_B0_member_backbinding_count"], "distinct B0 member arithmetic")
    need(38_624 + 115_472 == EXPECTED["gap_count"], "gap arithmetic")
    need(all(HEX64.fullmatch(value) is not None for value in INPUT_PINS.values()), "pin syntax")
    valid = list(iter_strict_json_rows(io.StringIO(""), '{"a":1},{"b":[true,false,null]}]'))
    need(valid == [{"a": 1}, {"b": [True, False, None]}], "strict parser valid rows")
    _must_reject_json('{"a":1,"a":2}]', "duplicate key")
    _must_reject_json('{"a":1.5}]', "float")
    _must_reject_json('{"a":NaN}]', "constant")
    _must_reject_json('[1]]', "nonobject")
    _must_reject_json(',{"a":1}]', "leading comma")
    _must_reject_json('{"a":1},]', "trailing comma")
    _must_reject_json('{"a":1}{"b":2}]', "missing comma")
    _must_reject_json('{"a":', "truncation")
    credit_probe = {"formal_credit": zero_credit(), "nested": {"formal_maximality_credit": 0}}
    _assert_zero_credit(credit_probe, "self-test")
    probe = contract()
    need(
        probe["implementation_present"] is True
        and probe["audit_authorized"] is AUDIT_AUTHORIZED
        and probe["candidate_mode_expected_to_block"] is (not AUDIT_AUTHORIZED)
        and probe["candidate_block_occurs_before_large_input_open"] is (not AUDIT_AUTHORIZED)
        and probe["candidate_block_occurs_before_any_write"] is (not AUDIT_AUTHORIZED)
        and probe["exact_expected"]["graph_count"] == 38_624
        and probe["exact_expected"]["physical_incidence_count"] == 115_472
        and probe["strict_boundary"]["official_key_is_metadata_only"] is True
        and probe["strict_boundary"]["all_output_formal_credit_zero"] is True
        and probe["candidate_transaction_hardening_implemented"] is True
        and probe["candidate_transaction_hardening_required_before_authorization"] is False
        and probe["transaction_contract"]["runtime_canonical_path_equals_formal_producer_path"] is True
        and probe["transaction_contract"]["created_output_inode_registered_before_strict_admission"] is True
        and probe["transaction_contract"]["created_stage_inode_bound_before_mode_admission"] is True
        and probe["transaction_contract"]["lightweight_transaction_self_test_claim_count"] == 14
        and probe["transaction_contract"]["SIGKILL_or_power_loss_orphan_recovery_implemented"] is False
        and all(value == 0 for key, value in probe["strict_boundary"].items() if key.startswith("formal_") and key.endswith("_credit")),
        "contract boundary",
    )
    authorization_status = (
        "AUDIT_AUTHORIZED__LIGHTWEIGHT_TEST_ONLY__HEAVY_CANDIDATE_NOT_RUN"
        if AUDIT_AUTHORIZED else
        "AUDIT_NOT_AUTHORIZED__CANDIDATE_BLOCKED"
    )
    return {
        "schema": SCHEMA + ".self-test.v1",
        "status": "PASS_LIGHTWEIGHT_ROUND306B1G0_SOURCE_JOIN_CONTRACT_SELF_TEST__" + authorization_status,
        "test_groups_passed": 23,
        "large_input_opened": False,
        "candidate_written": False,
        "implementation_present": True,
        "audit_authorized": AUDIT_AUTHORIZED,
        "candidate_mode_expected_to_block": not AUDIT_AUTHORIZED,
        "graph_count": 38_624,
        "physical_incidence_count": 115_472,
        "R264_correction_count": 400,
        "R264_correction_split": {"invalid_absent_owner_edge": 184, "present_phantom": 216},
        "all_output_formal_credit_zero": True,
        "official_key_is_metadata_only": True,
        "formal_maximality_credit": 0,
    }


def ledger_envelope(kind: str, spool: RowSpool) -> dict[str, Any]:
    payload = {
        "schema": SCHEMA + "." + kind + "-ledger.v1",
        "status": "PRIVATE_ZERO_CREDIT_GRAPH_SOURCE_INVENTORY_JOIN_FREEZE_CANDIDATE",
        **spool.metadata(),
        "formal_credit": zero_credit(),
    }
    return {**payload, "ledger_sha256": digest(payload)}


def checked_output_info(descriptor: int, label: str) -> os.stat_result:
    info = os.fstat(descriptor)
    need(
        stat.S_ISREG(info.st_mode)
        and stat.S_IMODE(info.st_mode) == 0o600
        and info.st_nlink == 1,
        "private output regular mode0600 nlink1:" + label,
    )
    return info


def preflight_created_file_name(
    created: dict[str, dict[str, Any]],
    name: str,
) -> None:
    """Perform every fallible logical name check before O_EXCL creation."""
    need(name in FILES.values() and name not in created, "expected unique candidate filename")


def register_created_file(
    created: dict[str, dict[str, Any]],
    name: str,
    descriptor: int,
) -> dict[str, Any]:
    """Capture the raw created inode before any strict file admission.

    Name/uniqueness preflight must already have run.  In particular, mode,
    link-count, regular-file and SHA admission happens only *after* this
    cleanup record exists.
    """
    info = os.fstat(descriptor)
    record = {
        "filename": name,
        "device": info.st_dev,
        "inode": info.st_ino,
        "file_sha256": None,
    }
    created[name] = record
    return record


def validate_created_file(stage_fd: int, record: dict[str, Any]) -> os.stat_result:
    """Reopen by stage dirfd and bind name, inode, mode, link count and SHA."""
    name = record["filename"]
    descriptor = os.open(
        name,
        os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0),
        dir_fd=stage_fd,
    )
    try:
        info = checked_output_info(descriptor, name)
        need(
            inode_identity(info) == (record["device"], record["inode"]),
            "candidate file inode remains bound:" + name,
        )
        observed_sha256, after = hash_descriptor(descriptor)
        need(
            inode_identity(after) == (record["device"], record["inode"])
            and observed_sha256 == record["file_sha256"],
            "candidate file bytes remain bound:" + name,
        )
        named = os.stat(name, dir_fd=stage_fd, follow_symlinks=False)
        need(
            _identity(named) == _identity(after),
            "candidate filename remains bound to verified fd:" + name,
        )
        return after
    finally:
        os.close(descriptor)


def strict_candidate_file_census(
    stage_fd: int,
    created: dict[str, dict[str, Any]],
) -> None:
    expected = set(FILES.values())
    need(set(os.listdir(stage_fd)) == expected, "exact candidate file census")
    need(set(created) == expected, "exact transaction-created file census")
    for name in sorted(expected):
        need(type(created[name]["file_sha256"]) is str, "candidate file hash recorded:" + name)
        validate_created_file(stage_fd, created[name])


def emit_ledger(
    stage_fd: int,
    name: str,
    kind: str,
    spool: RowSpool,
    created: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    envelope = ledger_envelope(kind, spool)
    spool.stream.flush()
    spool.stream.seek(0)
    preflight_created_file_name(created, name)
    descriptor = os.open(
        name,
        os.O_WRONLY
        | os.O_CREAT
        | os.O_EXCL
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_CLOEXEC", 0),
        0o600,
        dir_fd=stage_fd,
    )
    record: dict[str, Any] | None = None
    raw: BinaryIO | None = None
    state = hashlib.sha256()

    class Sink:
        def write(self, block: bytes) -> int:
            state.update(block)
            assert raw is not None
            return raw.write(block)

        def flush(self) -> None:
            assert raw is not None
            raw.flush()

    prefix = canonical(envelope)[:-1] + b',"' + TABLES[kind].encode("ascii") + b'":['
    try:
        # Registration itself is inside the fd-closing finally: even fstat or
        # record-construction failure cannot leak the O_EXCL-created fd.
        record = register_created_file(created, name, descriptor)
        # Strict admission is deliberately after raw inode registration.
        checked_output_info(descriptor, name)
        raw = os.fdopen(descriptor, "wb", closefd=True)
        descriptor = -1
        with gzip.GzipFile(fileobj=Sink(), mode="wb", filename="", mtime=0, compresslevel=9) as zipped:
            zipped.write(prefix)
            while True:
                block = spool.stream.read(1 << 20)
                if not block:
                    break
                zipped.write(block)
            zipped.write(b"]}")
        raw.flush()
        os.fsync(raw.fileno())
        checked_output_info(raw.fileno(), name)
    finally:
        if raw is not None:
            raw.close()
        elif descriptor >= 0:
            os.close(descriptor)
    need(record is not None, "ledger transaction inode record exists")
    record["file_sha256"] = state.hexdigest()
    validate_created_file(stage_fd, record)
    return {
        "filename": name,
        "file_sha256": record["file_sha256"],
        "ledger_sha256": envelope["ledger_sha256"],
        **spool.metadata(),
    }


def exclusive_bytes(
    stage_fd: int,
    name: str,
    payload: bytes,
    created: dict[str, dict[str, Any]],
) -> str:
    preflight_created_file_name(created, name)
    descriptor = os.open(
        name,
        os.O_WRONLY
        | os.O_CREAT
        | os.O_EXCL
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_CLOEXEC", 0),
        0o600,
        dir_fd=stage_fd,
    )
    record: dict[str, Any] | None = None
    try:
        # Registration itself is inside the fd-closing finally.
        record = register_created_file(created, name, descriptor)
        # Strict admission is deliberately after raw inode registration.
        checked_output_info(descriptor, name)
        offset = 0
        while offset < len(payload):
            written = os.write(descriptor, payload[offset:])
            need(written > 0, "candidate output write progress:" + name)
            offset += written
        os.fsync(descriptor)
        checked_output_info(descriptor, name)
    finally:
        os.close(descriptor)
    need(record is not None, "result transaction inode record exists")
    record["file_sha256"] = hashlib.sha256(payload).hexdigest()
    validate_created_file(stage_fd, record)
    return record["file_sha256"]


def rename_noreplace(old_fd: int, old_name: str, new_fd: int, new_name: str) -> None:
    libc = ctypes.CDLL(None, use_errno=True)
    function = getattr(libc, "renameat2", None)
    need(function is not None, "renameat2 required")
    function.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
    function.restype = ctypes.c_int
    if function(old_fd, os.fsencode(old_name), new_fd, os.fsencode(new_name), 1) != 0:
        code = ctypes.get_errno()
        if code == errno.EEXIST:
            raise FileExistsError(code, os.strerror(code), new_name)
        raise OSError(code, os.strerror(code), new_name)


def assert_directory_name_bound(
    root_fd: int,
    name: str,
    directory_fd: int,
    label: str,
) -> os.stat_result:
    named = os.stat(name, dir_fd=root_fd, follow_symlinks=False)
    opened = os.fstat(directory_fd)
    need(
        stat.S_ISDIR(named.st_mode)
        and stat.S_ISDIR(opened.st_mode)
        and stat.S_IMODE(named.st_mode) == 0o700
        and stat.S_IMODE(opened.st_mode) == 0o700
        and inode_identity(named) == inode_identity(opened),
        label + ":directory name/fd identity",
    )
    return opened


def create_stage(candidate: Path) -> tuple[str, str, int, int, tuple[int, int]]:
    if not os.path.lexists(PRIVATE_ROOT):
        parent_fd = os.open(
            ROOT,
            os.O_RDONLY
            | getattr(os, "O_DIRECTORY", 0)
            | getattr(os, "O_NOFOLLOW", 0)
            | getattr(os, "O_CLOEXEC", 0),
        )
        try:
            os.mkdir(PRIVATE_ROOT.name, 0o700, dir_fd=parent_fd)
            os.fsync(parent_fd)
        finally:
            os.close(parent_fd)
    information = os.lstat(PRIVATE_ROOT)
    need(stat.S_ISDIR(information.st_mode) and not PRIVATE_ROOT.is_symlink() and stat.S_IMODE(information.st_mode) == 0o700, "private root")
    target = Path(os.path.abspath(os.fspath(candidate)))
    need(target.parent == PRIVATE_ROOT and target.name not in {"", ".", ".."}, "direct private child")
    need(not os.path.lexists(target), "candidate target absent")
    root_fd = os.open(
        PRIVATE_ROOT,
        os.O_RDONLY
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_CLOEXEC", 0),
    )
    stage_fd = -1
    created_stage_identity: tuple[int, int] | None = None
    try:
        root_info = os.fstat(root_fd)
        need(
            inode_identity(root_info) == inode_identity(information)
            and stat.S_IMODE(root_info.st_mode) == 0o700,
            "private root path/fd identity",
        )
        stage_name = "." + target.name + ".stage." + digest(
            [os.getpid(), target.name, os.urandom(32).hex()]
        )[:32]
        os.mkdir(stage_name, 0o700, dir_fd=root_fd)
        created_stage_info = os.stat(stage_name, dir_fd=root_fd, follow_symlinks=False)
        # Bind the just-created directory inode before any strict admission;
        # a restrictive umask/mode failure below is therefore removable by
        # exact inode rather than by an unsafe pathname guess.
        created_stage_identity = inode_identity(created_stage_info)
        need(
            stat.S_ISDIR(created_stage_info.st_mode)
            and stat.S_IMODE(created_stage_info.st_mode) == 0o700,
            "created stage mode0700 directory",
        )
        os.fsync(root_fd)
        stage_fd = os.open(
            stage_name,
            os.O_RDONLY
            | getattr(os, "O_DIRECTORY", 0)
            | getattr(os, "O_NOFOLLOW", 0)
            | getattr(os, "O_CLOEXEC", 0),
            dir_fd=root_fd,
        )
        stage_info = assert_directory_name_bound(root_fd, stage_name, stage_fd, "new stage")
        need(
            inode_identity(stage_info) == created_stage_identity
            and not os.listdir(stage_fd),
            "opened stage is exact empty created inode",
        )
        return stage_name, target.name, root_fd, stage_fd, created_stage_identity
    except Exception:
        if stage_fd >= 0:
            os.close(stage_fd)
        if created_stage_identity is not None:
            for name in list(os.listdir(root_fd)):
                try:
                    candidate_info = os.stat(name, dir_fd=root_fd, follow_symlinks=False)
                except FileNotFoundError:
                    continue
                if stat.S_ISDIR(candidate_info.st_mode) and inode_identity(candidate_info) == created_stage_identity:
                    try:
                        os.rmdir(name, dir_fd=root_fd)
                    except OSError as error:
                        if error.errno not in {errno.ENOTEMPTY, errno.EEXIST}:
                            raise
            os.fsync(root_fd)
        os.close(root_fd)
        raise


def cleanup_exact_transaction(
    root_fd: int,
    stage_fd: int,
    directory_identity: tuple[int, int],
    created: dict[str, dict[str, Any]],
) -> None:
    """Remove only transaction-recorded inodes and the exact stage inode."""
    tracked = {(record["device"], record["inode"]) for record in created.values()}
    for name in list(os.listdir(stage_fd)):
        try:
            info = os.stat(name, dir_fd=stage_fd, follow_symlinks=False)
        except FileNotFoundError:
            continue
        if stat.S_ISREG(info.st_mode) and inode_identity(info) in tracked:
            os.unlink(name, dir_fd=stage_fd)
    os.fsync(stage_fd)
    for name in list(os.listdir(root_fd)):
        try:
            info = os.stat(name, dir_fd=root_fd, follow_symlinks=False)
        except FileNotFoundError:
            continue
        if not stat.S_ISDIR(info.st_mode) or inode_identity(info) != directory_identity:
            continue
        try:
            os.rmdir(name, dir_fd=root_fd)
        except OSError as error:
            if error.errno not in {errno.ENOTEMPTY, errno.EEXIST}:
                raise
    os.fsync(root_fd)


def transaction_self_test() -> dict[str, Any]:
    """Exercise the transaction layer without opening any pinned heavy input."""
    global PRIVATE_ROOT

    original_private_root = PRIVATE_ROOT
    checks: list[str] = []
    producer_fd, producer_info, producer_hash = open_verified_running_producer()
    try:
        recheck_running_producer(producer_fd, producer_info, producer_hash)
        checks.append("running-producer-path-fd-bytes-bound")
    finally:
        os.close(producer_fd)

    with tempfile.TemporaryDirectory(
        prefix=".round306b1g0-transaction-self-test.",
        dir=ROOT,
    ) as temporary_name:
        PRIVATE_ROOT = Path(temporary_name)
        try:
            # Normal dirfd-only write, unexpected-file rejection, exact
            # census, inode-bound publish, post-rename recheck, and cleanup.
            candidate = PRIVATE_ROOT / "normal-candidate"
            stage_name, target_name, root_fd, stage_fd, directory_identity = create_stage(candidate)
            created: dict[str, dict[str, Any]] = {}
            try:
                for name in FILES.values():
                    exclusive_bytes(
                        stage_fd,
                        name,
                        canonical({"transaction_self_test_file": name}),
                        created,
                    )
                unexpected_fd = os.open(
                    "unexpected",
                    os.O_WRONLY
                    | os.O_CREAT
                    | os.O_EXCL
                    | getattr(os, "O_NOFOLLOW", 0)
                    | getattr(os, "O_CLOEXEC", 0),
                    0o600,
                    dir_fd=stage_fd,
                )
                os.close(unexpected_fd)
                try:
                    strict_candidate_file_census(stage_fd, created)
                except FreezeBlocked:
                    checks.append("extra-file-census-attack-rejected")
                else:
                    raise FreezeBlocked("extra-file census attack accepted")
                os.unlink("unexpected", dir_fd=stage_fd)
                os.fsync(stage_fd)
                strict_candidate_file_census(stage_fd, created)
                checks.append("exact-file-census-passed")
                assert_directory_name_bound(root_fd, stage_name, stage_fd, "self-test pre-publish")
                rename_noreplace(root_fd, stage_name, root_fd, target_name)
                os.fsync(root_fd)
                assert_directory_name_bound(root_fd, target_name, stage_fd, "self-test post-publish")
                strict_candidate_file_census(stage_fd, created)
                os.fsync(stage_fd)
                checks.append("normal-publish-inode-and-files-bound")
                cleanup_exact_transaction(root_fd, stage_fd, directory_identity, created)
                need(not os.path.lexists(candidate), "normal self-test exact cleanup")
                checks.append("published-exact-cleanup-passed")
            finally:
                os.close(stage_fd)
                os.close(root_fd)

            # Replace one tracked filename by another inode.  Validation must
            # reject it.  Rollback removes the moved original tracked inode
            # and preserves the untracked replacement.
            candidate = PRIVATE_ROOT / "file-replacement-candidate"
            stage_name, _target_name, root_fd, stage_fd, directory_identity = create_stage(candidate)
            created = {}
            victim = next(iter(FILES.values()))
            try:
                exclusive_bytes(stage_fd, victim, b"original", created)
                os.rename(victim, "held-original", src_dir_fd=stage_fd, dst_dir_fd=stage_fd)
                replacement_fd = os.open(
                    victim,
                    os.O_WRONLY
                    | os.O_CREAT
                    | os.O_EXCL
                    | getattr(os, "O_NOFOLLOW", 0)
                    | getattr(os, "O_CLOEXEC", 0),
                    0o600,
                    dir_fd=stage_fd,
                )
                try:
                    need(os.write(replacement_fd, b"replacement") == len(b"replacement"), "replacement write")
                    os.fsync(replacement_fd)
                finally:
                    os.close(replacement_fd)
                try:
                    validate_created_file(stage_fd, created[victim])
                except FreezeBlocked:
                    checks.append("file-inode-replacement-attack-rejected")
                else:
                    raise FreezeBlocked("file inode replacement accepted")
                cleanup_exact_transaction(root_fd, stage_fd, directory_identity, created)
                need(set(os.listdir(stage_fd)) == {victim}, "rollback preserves untracked replacement")
                checks.append("rollback-exact-file-inode-scoped")
                os.unlink(victim, dir_fd=stage_fd)
                os.fsync(stage_fd)
                assert_directory_name_bound(root_fd, stage_name, stage_fd, "file attack cleanup")
                os.rmdir(stage_name, dir_fd=root_fd)
                os.fsync(root_fd)
            finally:
                os.close(stage_fd)
                os.close(root_fd)

            # Force strict mode0600 admission to fail after O_EXCL creation
            # for both raw result and gzip-ledger writers.  The raw inode must
            # already be registered, every fd must close, and exact rollback
            # must remove moved tracked inodes while preserving a replacement.
            candidate = PRIVATE_ROOT / "pre-admission-mode-failure-candidate"
            stage_name, _target_name, root_fd, stage_fd, directory_identity = create_stage(candidate)
            created = {}
            spool = RowSpool("graph")
            spool.add({
                "schema": SCHEMA + ".transaction-self-test-row.v1",
                ID_FIELDS["graph"]: "round306b1g0-transaction-self-test:graph",
            })
            result_name = FILES["result"]
            ledger_name = FILES["graph"]
            fd_directory = Path("/proc/self/fd")
            need(fd_directory.is_dir(), "proc fd census available")
            descriptor_count_before = len(os.listdir(fd_directory))
            prior_umask = os.umask(0o777)
            try:
                try:
                    exclusive_bytes(stage_fd, result_name, b"mode-failure", created)
                except FreezeBlocked:
                    need(
                        result_name in created
                        and type(created[result_name]["inode"]) is int
                        and created[result_name]["file_sha256"] is None,
                        "exclusive pre-admission inode registered",
                    )
                    checks.append("exclusive-pre-admission-mode-failure-recorded")
                else:
                    raise FreezeBlocked("exclusive restrictive-umask admission accepted")
                try:
                    emit_ledger(stage_fd, ledger_name, "graph", spool, created)
                except FreezeBlocked:
                    need(
                        ledger_name in created
                        and type(created[ledger_name]["inode"]) is int
                        and created[ledger_name]["file_sha256"] is None,
                        "ledger pre-admission inode registered",
                    )
                    checks.append("ledger-pre-admission-mode-failure-recorded")
                else:
                    raise FreezeBlocked("ledger restrictive-umask admission accepted")
            finally:
                os.umask(prior_umask)
            need(
                len(os.listdir(fd_directory)) == descriptor_count_before,
                "pre-admission writer descriptors closed",
            )
            checks.append("pre-admission-failure-fds-closed")
            spool.close()
            try:
                os.rename(
                    result_name,
                    "held-mode-failed-original",
                    src_dir_fd=stage_fd,
                    dst_dir_fd=stage_fd,
                )
                replacement_fd = os.open(
                    result_name,
                    os.O_WRONLY
                    | os.O_CREAT
                    | os.O_EXCL
                    | getattr(os, "O_NOFOLLOW", 0)
                    | getattr(os, "O_CLOEXEC", 0),
                    0o600,
                    dir_fd=stage_fd,
                )
                try:
                    need(os.write(replacement_fd, b"untracked-replacement") == len(b"untracked-replacement"), "mode failure replacement write")
                    os.fsync(replacement_fd)
                finally:
                    os.close(replacement_fd)
                cleanup_exact_transaction(root_fd, stage_fd, directory_identity, created)
                need(
                    set(os.listdir(stage_fd)) == {result_name},
                    "mode-failure rollback preserves only untracked replacement",
                )
                checks.append("pre-admission-exact-rollback-no-orphan-preserves-replacement")
                os.unlink(result_name, dir_fd=stage_fd)
                os.fsync(stage_fd)
                assert_directory_name_bound(root_fd, stage_name, stage_fd, "mode failure cleanup")
                os.rmdir(stage_name, dir_fd=root_fd)
                os.fsync(root_fd)
            finally:
                os.close(stage_fd)
                os.close(root_fd)

            # A restrictive umask makes the just-mkdir'd stage fail mode0700
            # admission.  Its inode was captured first, so create_stage must
            # remove that exact empty inode and leave no ordinary orphan.
            prior_umask = os.umask(0o777)
            try:
                try:
                    create_stage(PRIVATE_ROOT / "post-mkdir-admission-failure")
                except FreezeBlocked:
                    pass
                else:
                    raise FreezeBlocked("post-mkdir restrictive-umask admission accepted")
            finally:
                os.umask(prior_umask)
            need(not os.listdir(PRIVATE_ROOT), "post-mkdir admission failure leaves no stage orphan")
            checks.append("post-mkdir-stage-admission-failure-no-orphan")

            # Replace the stage pathname after its fd is open.  The name/fd
            # check must reject the substitute; rollback removes only the
            # original directory inode, wherever it was renamed.
            candidate = PRIVATE_ROOT / "stage-replacement-candidate"
            stage_name, _target_name, root_fd, stage_fd, directory_identity = create_stage(candidate)
            held_name = stage_name + ".held"
            try:
                os.rename(stage_name, held_name, src_dir_fd=root_fd, dst_dir_fd=root_fd)
                os.mkdir(stage_name, 0o700, dir_fd=root_fd)
                os.fsync(root_fd)
                try:
                    assert_directory_name_bound(root_fd, stage_name, stage_fd, "stage replacement attack")
                except FreezeBlocked:
                    checks.append("stage-name-replacement-attack-rejected")
                else:
                    raise FreezeBlocked("stage name replacement accepted")
                cleanup_exact_transaction(root_fd, stage_fd, directory_identity, {})
                need(
                    stage_name in os.listdir(root_fd) and held_name not in os.listdir(root_fd),
                    "rollback exact directory inode scoped",
                )
                checks.append("rollback-exact-directory-inode-scoped")
                os.rmdir(stage_name, dir_fd=root_fd)
                os.fsync(root_fd)
            finally:
                os.close(stage_fd)
                os.close(root_fd)
            need(not os.listdir(PRIVATE_ROOT), "transaction self-test private root empty")
        finally:
            PRIVATE_ROOT = original_private_root

    need(len(checks) == 14, "transaction self-test count")
    return {
        "schema": SCHEMA + ".transaction-self-test.v1",
        "status": "PASS_LIGHTWEIGHT_ROUND306B1G0_DIRFD_INODE_BOUND_TRANSACTION_SELF_TEST",
        "tests_passed": checks,
        "large_input_opened": False,
        "formal_candidate_written": False,
        "audit_authorized": AUDIT_AUTHORIZED,
        "crash_or_SIGKILL_orphan_recovery_tested": False,
    }


def build_private_candidate(candidate: Path) -> dict[str, Any]:
    # These are deliberately the first operations.  With authorization false,
    # no source fd, tempfile/spool, directory, or output file can be opened.
    need(IMPLEMENTATION_PRESENT, "graph source loader not implemented")
    need(AUDIT_AUTHORIZED, "candidate mode blocked before any large-input open or write: hostile audit authorization is false")
    producer_fd = -1
    root_fd = -1
    stage_fd = -1
    spools: dict[str, RowSpool] = {}
    created: dict[str, dict[str, Any]] = {}
    transaction_complete = False
    directory_identity = (-1, -1)
    try:
        producer_fd, producer_info, producer_hash = open_verified_running_producer()
        verify_all_input_pins()
        spools, audit = build_spools()
        stage_name, target_name, root_fd, stage_fd, directory_identity = create_stage(candidate)
        metadata: dict[str, Any] = {}
        for kind in ("graph", "sheet", "side", "correction", "member", "gap"):
            metadata[kind] = emit_ledger(stage_fd, FILES[kind], kind, spools[kind], created)
            os.fsync(stage_fd)
        payload = {
            "schema": SCHEMA,
            "status": "PRIVATE_ZERO_CREDIT_GRAPH_SOURCE_INVENTORY_AND_JOIN_FREEZE_CANDIDATE",
            "producer_file_sha256": producer_hash,
            "audit": audit,
            "output_ledgers": metadata,
            "strict_boundary": contract()["strict_boundary"],
            "candidate_is_formal": False,
        }
        result = {**payload, "result_sha256": digest(payload)}
        result_file_sha256 = exclusive_bytes(
            stage_fd,
            FILES["result"],
            canonical(result),
            created,
        )
        os.fsync(stage_fd)
        strict_candidate_file_census(stage_fd, created)
        recheck_running_producer(producer_fd, producer_info, producer_hash)
        verify_all_input_pins()
        strict_candidate_file_census(stage_fd, created)
        assert_directory_name_bound(root_fd, stage_name, stage_fd, "pre-publish stage")
        rename_noreplace(root_fd, stage_name, root_fd, target_name)
        os.fsync(root_fd)
        assert_directory_name_bound(root_fd, target_name, stage_fd, "post-publish candidate")
        strict_candidate_file_census(stage_fd, created)
        os.fsync(stage_fd)
        recheck_running_producer(producer_fd, producer_info, producer_hash)
        assert_directory_name_bound(root_fd, target_name, stage_fd, "final candidate")
        strict_candidate_file_census(stage_fd, created)
        os.fsync(stage_fd)
        os.fsync(root_fd)
        transaction_complete = True
        return {
            "status": "PASS_PRIVATE_ZERO_CREDIT_CANDIDATE_WRITTEN",
            "result_sha256": result["result_sha256"],
            "result_file_sha256": result_file_sha256,
            "formal_artifact_written": False,
        }
    finally:
        if not transaction_complete and root_fd >= 0 and stage_fd >= 0:
            cleanup_exact_transaction(root_fd, stage_fd, directory_identity, created)
        for spool in spools.values():
            spool.close()
        if stage_fd >= 0:
            os.close(stage_fd)
        if root_fd >= 0:
            os.close(root_fd)
        if producer_fd >= 0:
            os.close(producer_fd)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--print-contract", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--transaction-self-test", action="store_true")
    parser.add_argument("--candidate-dir", type=Path)
    arguments = parser.parse_args()
    need(
        sum(
            (
                arguments.print_contract,
                arguments.self_test,
                arguments.transaction_self_test,
                arguments.candidate_dir is not None,
            )
        ) == 1,
        "choose exactly one mode",
    )
    if arguments.print_contract:
        print(canonical(contract()).decode("ascii"))
    elif arguments.self_test:
        print(canonical(self_test()).decode("ascii"))
    elif arguments.transaction_self_test:
        print(canonical(transaction_self_test()).decode("ascii"))
    else:
        assert arguments.candidate_dir is not None
        print(canonical(build_private_candidate(arguments.candidate_dir)).decode("ascii"))


if __name__ == "__main__":
    main()
