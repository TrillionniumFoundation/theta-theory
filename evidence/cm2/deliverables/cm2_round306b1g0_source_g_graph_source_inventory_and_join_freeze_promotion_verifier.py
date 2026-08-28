#!/usr/bin/env python3
"""Independent fail-closed verifier for the Round306B1G0 source freeze.

The producer is never imported, executed, parsed, or tokenized.  It is only an
inert byte object pinned by size and SHA-256.  This verifier independently
reconstructs the R242/R245, R235/R248/R264 and R236/R248 joins, performs a
complete Round306B0 member scan/backbinding, and compares every candidate row
with that reconstruction.

Heavy reconstruction, candidate admission, and publication are deliberately
blocked by ``AUDIT_AUTHORIZED`` before any large source or candidate is opened
and before any output is written.  Lightweight contract and attack tests remain
available while the gate is false.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import ctypes
from dataclasses import dataclass
import errno
import fcntl
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat
import tempfile
from typing import Any, BinaryIO, Callable, Iterator, TextIO
import zlib


class VerificationBlocked(RuntimeError):
    """Fail-closed source, candidate, theorem-credit, or transaction error."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationBlocked(label)


def discover_root(source: Path) -> Path:
    resolved = source.resolve()
    for ancestor in (resolved.parent, *resolved.parents):
        if (ancestor / "deliverables").is_dir() and (ancestor / ".venv-cm2").is_dir():
            return ancestor
    raise VerificationBlocked("workspace root not found")


ROOT = discover_root(Path(__file__))
DATA = ROOT / "deliverables"
PRIVATE_ROOT = ROOT / ".cm2-round306b1g0-private-candidates"
PREFIX = "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze"
SCHEMA = "cm2.round306b1g0.source-g-graph-source-inventory-and-join-freeze.v1"
PRODUCER = PREFIX + ".py"
VERIFIER = PREFIX + "_promotion_verifier.py"
ATTACK = PREFIX + "_attack_suite.json"
VERIFICATION = PREFIX + "_verification.json"
EXPECTED_PRODUCER_SHA256 = "97f1d0736a616071dbb0dba3bf533e3fae96091fc6b165395436216bb69c9321"
EXPECTED_PRODUCER_SIZE = 90_721
AUDIT_AUTHORIZED = True

ENCODER = json.JSONEncoder(sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)
HEX64 = re.compile(r"^[0-9a-f]{64}$")
FILES = {
 "graph": PREFIX+"_graph_source_inventory.json.gz",
 "sheet": PREFIX+"_graph_sheet_join.json.gz",
 "side": PREFIX+"_graph_side_join.json.gz",
 "correction": PREFIX+"_r264_correction_disposition.json.gz",
 "member": PREFIX+"_b0_member_backbinding.json.gz",
 "gap": PREFIX+"_gap.json.gz", "result": PREFIX+"_result.json",
}
TABLES = {
 "graph":"graph_source_inventory_rows", "sheet":"graph_sheet_join_rows",
 "side":"graph_side_join_rows", "correction":"r264_correction_disposition_rows",
 "member":"b0_member_backbinding_rows", "gap":"gap_rows",
}
ID_FIELDS = {
 "graph":"Round306B1G0_graph_source_inventory_row_id",
 "sheet":"Round306B1G0_graph_sheet_join_row_id",
 "side":"Round306B1G0_graph_side_join_row_id",
 "correction":"Round306B1G0_R264_correction_disposition_row_id",
 "member":"Round306B1G0_B0_member_backbinding_row_id",
 "gap":"Round306B1G0_gap_row_id",
}
CANDIDATE_KINDS=("graph","sheet","side","correction","member","gap")
CANDIDATE_ORDER=tuple(FILES[k] for k in CANDIDATE_KINDS)+(FILES["result"],)
PROMOTION_ORDER=(ATTACK,*CANDIDATE_ORDER,VERIFICATION)

# Literal verifier pins, never obtained from producer code.
SOURCE_PINS: dict[str, tuple[str,int]] = {
"cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json":("e340fa1a071d85a36b54d10a45ae2fdb9d70b8c90f4c21f054c6fc9505e5e787",67_765_471),
"cm2_round235_source_g_single_endpoint_graph_word_key_partition_verification.json":("8009f857b45aa05848b84258f2081bd6de54ff04643387ea3e8fd9c74bdb0e2a",643),
"cm2_round235_source_g_single_endpoint_graph_word_key_partition_manifest.sha256":("cf58b7d2f419ea252c3398665302fe6f5ff06436af20a56beaaa47e5ef822ea0",566),
"cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json":("b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217",2_061_199),
"cm2_round236_source_g_wall_residual_closure_and_root_key_partition_verification.json":("153238a6a6678565b58c376c890b6f962af7b59d5572fd949836756c947cec55",616),
"cm2_round236_source_g_wall_residual_closure_and_root_key_partition_manifest.sha256":("28f6f6d2f5b0f10edba5cd473b4126a8fed098874849c2f579eadd92b30d324c",582),
"cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_certificate.json":("8d32c381e21c03aad6a531b7e5a527d295783b7e3e38baa1e6bcba20c40db22e",13_734_655),
"cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_verification.json":("76ff0d996fd3f3d3a06f625d74fc7302e2bf47366d5667b3adfc4f8568c7eced",810),
"cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_manifest.sha256":("6da30fe3f9438ec73dc9c7d1aac770d8e9730aa9564ab0c535f1596cdc09ef2f",897),
"cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json":("c76662f7cb068127f3612a3655ae720662eead9b9210b5757d771693149883c1",20_683_081),
"cm2_round245_source_g_retained_graph_mixed_sheet_quotient_verification.json":("7b116fce6abfad827a19da4e6637bac50c784c0e53b84e9bfd9567abb35bef14",1_016),
"cm2_round245_source_g_retained_graph_mixed_sheet_quotient_manifest.sha256":("1aff29f3a42b618ca85e5a1d3c537307e32326f8d5092b82d4253a5bf6e1c4ac",897),
"cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json":("fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311",205_148_977),
"cm2_round248_source_g_wall_finite_key_retained_quotient_verification.json":("5e20ada49b5bca2e7ebaf6b78835c4ca1a6051e24960b7d00b3ae9d596f11a10",1_028),
"cm2_round248_source_g_wall_finite_key_retained_quotient_manifest.sha256":("b1ddedd01041e71b5c12fa4989726815c8685e6df77f54d9dbddda64aaf89e07",885),
"cm2_round264_source_g_lower_dimensional_endpoint_correction_and_glue_closure_certificate.json":("ac9e9451e12621fd236fea39bc686e13b41ade62e5255de9c9cd98230763236f",406_539_851),
"cm2_round264_source_g_lower_dimensional_endpoint_correction_and_glue_closure_verification.json":("16930e5d790ff934b74f3c715d3bdda8c6053e8c14e457b30b11efce260154a3",2_799),
"cm2_round264_source_g_lower_dimensional_endpoint_correction_and_glue_closure_manifest.sha256":("34d5183f3e75989151cb5c918d907dc6bb6a33e23f8bd6ab262ded6e9542e534",933),
"cm2_round306b0_source_g_r306a_universe_support_source_freeze_member_support_source_index.json.gz":("c9a8649c8473bb6a170187e7f803e95748d2ff2198b1b846d97383dd5f0581af",162_499_140),
"cm2_round306b0_source_g_r306a_universe_support_source_freeze_result.json":("badc000c6fadd8807b26a7c3511edc51796c962f150b438956e4c549fd0d5735",9_450),
"cm2_round306b0_source_g_r306a_universe_support_source_freeze_verification.json":("f8acc3150d4663d92976a44ab1c3b35c7264f4c4d14808f9133f1184d3f4b590",7_003),
"cm2_round306b0_source_g_r306a_universe_support_source_freeze_manifest.sha256":("9846b36d28bb1507b273de3e613a5ecd5ac6515258042bf8b91b89e0c156b269",1_760),
}
VERIFIED_SOURCE_NAMES:set[str]=set()
EXPECTED={
"graph_count":38_624,"R242_graph_count":264,"R245_graph_sheet_join_count":264,
"R245_graph_side_join_count":528,"R245_incidence_count":792,
"R235_single_graph_count":38_328,"R248_single_graph_sheet_join_count":38_328,
"R248_single_pre_correction_side_count":76_656,"R264_correction_count":400,
"R264_invalid_absent_owner_edge_count":184,"R264_present_phantom_count":216,
"R248_single_graph_side_join_count":76_256,"R248_single_incidence_count":114_584,
"R236_double_partition_count":16,"R236_double_graph_count":32,
"R248_double_graph_sheet_join_count":32,"R248_double_distinct_side_member_count":48,
"R248_double_graph_side_join_count":64,"R248_double_incidence_count":96,
"graph_sheet_join_count":38_624,"graph_side_join_count":76_848,
"physical_incidence_count":115_472,"distinct_B0_member_backbinding_count":115_456,
"graph_definition_gap_count":38_624,"physical_incidence_gap_count":115_472,"gap_count":154_096,
}
R235="cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json"
R236="cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json"
R242="cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_certificate.json"
R245="cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json"
R248="cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json"
R264="cm2_round264_source_g_lower_dimensional_endpoint_correction_and_glue_closure_certificate.json"
B0="cm2_round306b0_source_g_r306a_universe_support_source_freeze_member_support_source_index.json.gz"

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
    need(claimed == digest(payload), label + ":row sha256")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in output, "duplicate JSON key:" + key)
        output[key] = value
    return output


def reject_noninteger(token: str) -> Any:
    raise VerificationBlocked("nonintegral JSON token:" + token)


DECODER = json.JSONDecoder(
    object_pairs_hook=unique_object,
    parse_float=reject_noninteger,
    parse_constant=reject_noninteger,
)


def strict_object(raw: bytes, label: str) -> dict[str, Any]:
    need(raw and not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
         "strict bytes:" + label)
    value = json.loads(
        raw.decode("utf-8"), object_pairs_hook=unique_object,
        parse_float=reject_noninteger, parse_constant=reject_noninteger,
    )
    need(type(value) is dict, "top object:" + label)
    return value


def stat_identity(info: os.stat_result) -> tuple[int, int, int, int, int, int, int]:
    return (
        info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size,
        info.st_mtime_ns, info.st_ctime_ns,
    )


def hash_fd(descriptor: int, maximum: int) -> tuple[str, os.stat_result]:
    before = os.fstat(descriptor)
    need(stat.S_ISREG(before.st_mode) and 0 < before.st_size <= maximum, "bounded regular fd")
    state = hashlib.sha256()
    os.lseek(descriptor, 0, os.SEEK_SET)
    total = 0
    while True:
        block = os.read(descriptor, 1 << 20)
        if not block:
            break
        total += len(block)
        need(total <= maximum, "bounded fd hash")
        state.update(block)
    after = os.fstat(descriptor)
    need(stat_identity(before) == stat_identity(after), "stable hashed fd")
    os.lseek(descriptor, 0, os.SEEK_SET)
    return state.hexdigest(), before


def open_exact_named(name: str, expected_sha256: str, expected_size: int) -> tuple[int, os.stat_result]:
    need(name == os.path.basename(name) and HEX64.fullmatch(expected_sha256) is not None,
         "direct pinned source")
    path = DATA / name
    before = os.lstat(path)
    need(
        stat.S_ISREG(before.st_mode) and not path.is_symlink()
        and before.st_nlink == 1 and before.st_size == expected_size,
        "source exact regular size:" + name,
    )
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        opened = os.fstat(descriptor)
        need(stat_identity(before) == stat_identity(opened), "source path/fd binding:" + name)
        observed, hashed = hash_fd(descriptor, expected_size)
        need(observed == expected_sha256 and stat_identity(hashed) == stat_identity(before),
             "source exact byte pin:" + name)
        need(stat_identity(os.lstat(path)) == stat_identity(before), "source named stability:" + name)
        return descriptor, before
    except Exception:
        os.close(descriptor)
        raise


def open_source(name: str) -> tuple[int, os.stat_result]:
    need(name in SOURCE_PINS, "known source pin:" + name)
    sha256, size = SOURCE_PINS[name]
    descriptor, before = open_exact_named(name, sha256, size)
    VERIFIED_SOURCE_NAMES.add(name)
    return descriptor, before


def close_source(descriptor: int, before: os.stat_result, name: str) -> None:
    try:
        need(stat_identity(os.fstat(descriptor)) == stat_identity(before),
             "source fd stable after parse:" + name)
        need(stat_identity(os.lstat(DATA / name)) == stat_identity(before),
             "source path stable after parse:" + name)
    finally:
        os.close(descriptor)


def runtime_snapshot(name: str, expected_sha256: str | None, expected_size: int | None) -> tuple[int, os.stat_result, str]:
    expected = DATA / name
    if name == VERIFIER:
        need(Path(__file__).resolve() == expected.resolve(), "runtime verifier canonical path")
        need(Path(__file__).absolute() == expected.absolute(), "runtime verifier exact path")
    before = os.lstat(expected)
    need(stat.S_ISREG(before.st_mode) and not expected.is_symlink() and before.st_nlink == 1,
         "runtime exact regular:" + name)
    if expected_size is not None:
        need(before.st_size == expected_size, "runtime exact size:" + name)
    descriptor = os.open(expected, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        observed, opened = hash_fd(descriptor, 5_000_000)
        need(stat_identity(before) == stat_identity(opened), "runtime path/fd binding:" + name)
        if expected_sha256 is not None:
            need(observed == expected_sha256, "runtime byte pin:" + name)
        return descriptor, opened, observed
    except Exception:
        os.close(descriptor)
        raise


def recheck_runtime(descriptor: int, before: os.stat_result, sha256: str, name: str) -> None:
    observed, after = hash_fd(descriptor, 5_000_000)
    need(stat_identity(after) == stat_identity(before) and observed == sha256,
         "runtime fd unchanged:" + name)
    need(stat_identity(os.lstat(DATA / name)) == stat_identity(before),
         "runtime path remains fd-bound:" + name)


def stream_find_marker(
    stream: TextIO,
    marker: str,
    initial: str = "",
    *,
    chunk_size: int = 1 << 20,
    scan_limit: int = 1 << 30,
    forbidden_before_marker: tuple[str, ...] = (),
) -> str:
    """Find an exact marker with bounded rolling overlap and constant memory.

    ``str.find`` performs the inner search in C.  Retaining the longest
    pattern minus one character is equivalent to a rolling/KMP boundary state:
    a match split at any read boundary cannot be lost, while arbitrary source
    prelude is never accumulated.
    """
    need(
        type(marker) is str and bool(marker)
        and type(chunk_size) is int and 0 < chunk_size <= (1 << 24)
        and type(scan_limit) is int and scan_limit > 0,
        "valid bounded stream-marker search",
    )
    forbidden = tuple(forbidden_before_marker)
    need(
        all(type(item) is str and item and item != marker for item in forbidden)
        and len(set(forbidden)) == len(forbidden),
        "valid distinct forbidden markers",
    )
    overlap = max(len(item) for item in (marker, *forbidden)) - 1
    need(
        type(initial) is str and len(initial) <= chunk_size + overlap,
        "bounded initial marker-search remainder",
    )
    carry = ""
    block = initial
    scanned = 0
    while True:
        if not block:
            remaining = scan_limit - scanned
            need(remaining > 0, "bounded stream marker scan:" + marker)
            block = stream.read(min(chunk_size, remaining))
            need(bool(block), "missing or truncated stream marker:" + marker)
        scanned += len(block)
        need(scanned <= scan_limit, "bounded stream marker scan:" + marker)
        window = carry + block
        target_at = window.find(marker)
        boundary = target_at + len(marker) if target_at >= 0 else len(window)
        for forbidden_marker in forbidden:
            forbidden_at = window.find(forbidden_marker)
            need(
                forbidden_at < 0 or forbidden_at >= boundary,
                "duplicate or forbidden marker before target:" + forbidden_marker,
            )
        if target_at >= 0:
            return window[target_at + len(marker):]
        carry = window[-overlap:] if overlap else ""
        block = ""


def iter_array(
    stream: TextIO,
    marker: str,
    initial: str = "",
    *,
    chunk_size: int = 1 << 20,
    marker_scan_limit: int = 1 << 30,
    forbidden_before_marker: tuple[str, ...] = (),
) -> Iterator[dict[str, Any]]:
    buffer = stream_find_marker(
        stream, marker, initial, chunk_size=chunk_size,
        scan_limit=marker_scan_limit,
        forbidden_before_marker=forbidden_before_marker,
    )
    require_comma = False
    while True:
        buffer = buffer.lstrip()
        while not buffer:
            block = stream.read(chunk_size)
            need(bool(block), "truncated streamed array")
            buffer += block
            buffer = buffer.lstrip()
        if buffer[0] == "]":
            return
        if require_comma:
            need(buffer[0] == ",", "missing streamed comma")
            buffer = buffer[1:].lstrip()
            while not buffer:
                block = stream.read(chunk_size)
                need(bool(block), "truncated streamed array after comma")
                buffer += block
                buffer = buffer.lstrip()
            need(buffer[0] != "]", "trailing streamed comma")
        else:
            need(buffer[0] != ",", "leading streamed comma")
        while True:
            try:
                row, end = DECODER.raw_decode(buffer)
                break
            except json.JSONDecodeError:
                block = stream.read(chunk_size)
                need(bool(block), "truncated streamed row")
                buffer += block
        need(type(row) is dict, "stream row object")
        yield row
        buffer = buffer[end:]
        require_comma = True


def stream_source_rows(
    name: str,
    marker: str,
    *,
    compressed: bool,
    table_anchor: str | None = None,
) -> Iterator[dict[str, Any]]:
    descriptor, before = open_source(name)
    raw = os.fdopen(descriptor, "rb", closefd=False)
    binary: BinaryIO = gzip.GzipFile(fileobj=raw, mode="rb") if compressed else raw
    text = io.TextIOWrapper(binary, encoding="utf-8", newline="")
    try:
        initial = ""
        forbidden: tuple[str, ...] = ()
        marker_scan_limit = SOURCE_PINS[name][1]
        if table_anchor is not None:
            initial = stream_find_marker(
                text, table_anchor, scan_limit=marker_scan_limit,
            )
            # A repeated table anchor before its rows array is an ambiguous or
            # malformed envelope and must fail rather than silently reroute.
            forbidden = (table_anchor,)
        yield from iter_array(
            text, marker, initial, marker_scan_limit=marker_scan_limit,
            forbidden_before_marker=forbidden,
        )
        try:
            text.detach()
        except Exception:
            pass
        if compressed:
            binary.close()
        raw.close()
        close_source(descriptor, before, name)
        descriptor = -1
    finally:
        try:
            text.detach()
        except Exception:
            pass
        if compressed and not binary.closed:
            binary.close()
        if not raw.closed:
            raw.close()
        if descriptor >= 0:
            close_source(descriptor, before, name)


def load_source_object(name: str) -> dict[str, Any]:
    descriptor, before = open_source(name)
    raw = os.fdopen(descriptor, "rb", closefd=False)
    try:
        value = json.load(
            raw, object_pairs_hook=unique_object,
            parse_float=reject_noninteger, parse_constant=reject_noninteger,
        )
        need(type(value) is dict, "source top object:" + name)
        raw.close()
        close_source(descriptor, before, name)
        descriptor = -1
        return value
    finally:
        if not raw.closed:
            raw.close()
        if descriptor >= 0:
            close_source(descriptor, before, name)


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


class ExpectedLedger:
    """Independent ordered row spool used only by the verifier."""

    def __init__(self, kind: str) -> None:
        need(kind in ID_FIELDS, "known expected ledger kind")
        self.kind = kind
        self.rows = ListHash()
        self.ids = ListHash()
        self.hashes = ListHash()
        self.seen: set[str] = set()
        self.file = tempfile.TemporaryFile(mode="w+b")

    def append(self, payload: dict[str, Any]) -> dict[str, Any]:
        row = close_row(payload)
        row_id = row.get(ID_FIELDS[self.kind])
        need(type(row_id) is str and row_id not in self.seen,
             "unique independently reconstructed row id:" + self.kind)
        self.seen.add(row_id)
        self.file.write(canonical(row) + b"\n")
        self.rows.add(row)
        self.ids.add(row_id)
        self.hashes.add(row["row_sha256"])
        return row

    def metadata(self) -> dict[str, Any]:
        return {
            "row_count": self.rows.count,
            "rows_sha256": self.rows.finish(),
            "row_ids_sha256": self.ids.finish(),
            "row_hashes_sha256": self.hashes.finish(),
        }

    def expected_lines(self) -> Iterator[bytes]:
        self.file.flush()
        self.file.seek(0)
        for line in self.file:
            need(line.endswith(b"\n"), "expected spool line")
            yield line[:-1]

    def close(self) -> None:
        self.file.close()


@dataclass(frozen=True)
class SourceFeature:
    member_id: str
    package: str
    filename: str
    table: str
    source_row_sha256: str
    feature_kind: str
    role: str
    branch: str | None
    official_key_id: str
    source_edge_id: str | None = None
    source_edge_sha256: str | None = None


@dataclass(frozen=True)
class SourceGraph:
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
    sheet: SourceFeature
    sides: tuple[SourceFeature, ...]
    correction_source_id: str | None = None


def ledger_rows(name: str, table: str, *, compressed: bool = False) -> Iterator[dict[str, Any]]:
    yield from stream_source_rows(
        name, '"rows":[', compressed=compressed, table_anchor='"'+table+'":'
    )


def plain_rows(name: str, table: str) -> Iterator[dict[str, Any]]:
    yield from stream_source_rows(name, '"'+table+'":[', compressed=False)


def source_feature(
    row: dict[str, Any], *, package: str, filename: str, table: str,
    id_field: str, feature_kind: str, role: str, branch: str | None,
    key_field: str = "official_key_id", edge: dict[str, Any] | None = None,
) -> SourceFeature:
    check_row(row, package + ":" + feature_kind)
    member = row.get(id_field)
    key = row.get(key_field)
    need(type(member) is str and type(key) is str, "feature identity and metadata key")
    return SourceFeature(
        member_id=member, package=package, filename=filename, table=table,
        source_row_sha256=row["row_sha256"], feature_kind=feature_kind,
        role=role, branch=branch, official_key_id=key,
        source_edge_id=(edge.get("mixed_sheet_edge_id") if edge else None),
        source_edge_sha256=(edge.get("row_sha256") if edge else None),
    )


def transition_graphs() -> list[SourceGraph]:
    patches: dict[str, dict[str, Any]] = {}
    for row in ledger_rows(R242, "formal_positive_2D_transition_sheet_patch_ledger"):
        check_row(row, "R242 transition graph")
        interface = row.get("Round220_split_interface_id")
        need(type(interface) is str and interface not in patches, "unique R242 interface")
        need(
            row.get("local_dimension") == 2
            and row.get("three_dimensional_coordinate_volume") == 0
            and row.get("local_positive_2D_transition_sheet_patch_credit") == 1,
            "R242 graph source facts",
        )
        patches[interface] = row
    need(len(patches) == 264, "R242 264 graph rows")

    allowed = {"OWNER_OPEN_BULK", "SHADOW_OPEN_BULK", "HALF_OPEN_TRANSITION_SHEET"}
    nodes: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    node_count = 0
    for row in ledger_rows(R245, "formal_retained_stratum_node_ledger"):
        check_row(row, "R245 retained node")
        kind = row.get("stratum_kind")
        if kind not in allowed:
            continue
        interface = row.get("Round220_split_interface_id")
        need(interface in patches and kind not in nodes[interface], "R245 lineage/node routing")
        nodes[interface][kind] = row
        node_count += 1
    need(node_count == 792 and set(nodes) == set(patches), "R245 264 sheets plus 528 sides")

    physical_edges: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in ledger_rows(R245, "formal_mixed_sheet_physical_edge_ledger"):
        check_row(row, "R245 physical edge")
        if row.get("edge_kind") not in {
            "OWNER_BULK_TO_HALF_OPEN_SHEET", "SHADOW_BULK_TO_HALF_OPEN_SHEET",
        }:
            continue
        interface = row.get("Round220_split_interface_id")
        need(interface in patches, "R245 edge lineage")
        physical_edges[interface].append(row)
    need(sum(map(len, physical_edges.values())) == 528 and set(physical_edges) == set(patches),
         "R245 exact 528 selected edges")

    result: list[SourceGraph] = []
    for interface in sorted(patches):
        patch = patches[interface]
        bundle = nodes[interface]
        need(set(bundle) == allowed and len(physical_edges[interface]) == 2,
             "R245 exact graph-local bundle")
        sheet = bundle["HALF_OPEN_TRANSITION_SHEET"]
        owner = bundle["OWNER_OPEN_BULK"]
        shadow = bundle["SHADOW_OPEN_BULK"]
        by_bulk: dict[str, dict[str, Any]] = {}
        sheet_id = sheet["retained_stratum_node_id"]
        for edge in physical_edges[interface]:
            endpoints = {edge.get("left_node_id"), edge.get("right_node_id")}
            need(sheet_id in endpoints and len(endpoints) == 2, "R245 edge contains selected sheet")
            endpoints.remove(sheet_id)
            bulk_id = next(iter(endpoints))
            need(
                bulk_id in {owner["retained_stratum_node_id"], shadow["retained_stratum_node_id"]}
                and bulk_id not in by_bulk,
                "R245 edge exact bulk endpoint",
            )
            by_bulk[bulk_id] = edge
        # Key equality is a post-routing consistency assertion only.
        need(
            patch["official_key_id"] == sheet["official_key_id"]
            == owner["official_key_id"] == shadow["official_key_id"],
            "R242/R245 official-key metadata consistency",
        )
        sheet_feature = source_feature(
            sheet, package="R245", filename=R245,
            table="formal_retained_stratum_node_ledger",
            id_field="retained_stratum_node_id", feature_kind="SHEET",
            role="GRAPH_SHEET", branch=None,
        )
        side_features = tuple(
            source_feature(
                bulk, package="R245", filename=R245,
                table="formal_retained_stratum_node_ledger",
                id_field="retained_stratum_node_id", feature_kind="POSITIVE_3D_SIDE",
                role=role, branch=role,
                edge=by_bulk[bulk["retained_stratum_node_id"]],
            )
            for role, bulk in (("OWNER_OPEN_BULK", owner), ("SHADOW_OPEN_BULK", shadow))
        )
        result.append(SourceGraph(
            graph_id=patch["transition_sheet_patch_row_id"],
            family="R242_UNIQUE_TRANSITION_GRAPH", source_round=242,
            filename=R242, table="formal_positive_2D_transition_sheet_patch_ledger",
            source_row_id=patch["transition_sheet_patch_row_id"],
            source_row_sha256=patch["row_sha256"], interface_id=interface,
            endpoint_factor="transition_graph",
            official_key_ids=(patch["official_key_id"],),
            sheet=sheet_feature, sides=side_features,
        ))
    need(len(result) == 264 and sum(len(g.sides) for g in result) == 528,
         "R242/R245 reconstructed totals")
    return result


def correction_rows() -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    labels: Counter[str] = Counter()
    dispositions: Counter[str] = Counter()
    invalid_owner = 0
    for row in ledger_rows(R264, "formal_endpoint_empty_branch_correction_disposition_ledger"):
        check_row(row, "R264 correction")
        source = row.get("source_partition_row_id")
        need(type(source) is str and source not in result, "unique R264 source partition")
        need(row.get("empty_branch_Round250_Round251_Round252_accepted_edge_incidence_count") == 0,
             "R264 no accepted empty-branch incidence")
        labels[row["empty_branch_label"]] += 1
        dispositions[row["disposition"]] += 1
        invalid_owner += row.get("invalid_Round248_owner_edge_id") is not None
        result[source] = row
    need(len(result) == 400, "R264 400 corrections")
    need(labels == {"EVENT_ABSENT": 184, "EVENT_PRESENT": 216}, "R264 184+216 split")
    need(invalid_owner == 184, "R264 184 absent-owner prunes")
    need(dispositions == {
        "PRUNE_EMPTY_ABSENT_BULK_NODE_AND_INVALID_OWNER_EDGE__RETAIN_T0_SHEET": 184,
        "DROP_EMPTY_PRESENT_SINGLETON_PHANTOM_COMPONENT": 216,
    }, "R264 exact dispositions")
    return result


def wall_features() -> tuple[
    dict[tuple[str, str, str], dict[str, Any]],
    dict[str, dict[str, dict[str, Any]]],
]:
    sheets: dict[tuple[str, str, str], dict[str, Any]] = {}
    sheet_hist: Counter[str] = Counter()
    for row in ledger_rows(R248, "formal_wall_half_open_sheet_owner_ledger"):
        check_row(row, "R248 sheet")
        kind = row.get("source_partition_kind")
        if kind not in {"ROUND235_SINGLE_ENDPOINT_GRAPH_SHEET", "ROUND236_DOUBLE_ENDPOINT_GRAPH_SHEET"}:
            continue
        key = (kind, row["source_partition_row_id"], row["endpoint_factor"])
        need(key not in sheets, "unique R248 selected sheet")
        sheets[key] = row
        sheet_hist[kind] += 1
    need(sheet_hist == {
        "ROUND235_SINGLE_ENDPOINT_GRAPH_SHEET": 38_328,
        "ROUND236_DOUBLE_ENDPOINT_GRAPH_SHEET": 32,
    }, "R248 sheet census")

    bulks: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    bulk_hist: Counter[str] = Counter()
    for row in ledger_rows(R248, "formal_wall_positive_volume_bulk_ledger"):
        check_row(row, "R248 bulk")
        kind = row.get("source_partition_kind")
        if kind not in {
            "ROUND235_SINGLE_ENDPOINT_GRAPH_BRANCH",
            "ROUND236_DOUBLE_ENDPOINT_ARRANGEMENT_BRANCH",
        }:
            continue
        source = row["source_partition_row_id"]
        branch = row["branch_label"]
        need(branch not in bulks[source], "unique R248 selected branch")
        bulks[source][branch] = row
        bulk_hist[kind] += 1
    need(bulk_hist == {
        "ROUND235_SINGLE_ENDPOINT_GRAPH_BRANCH": 76_656,
        "ROUND236_DOUBLE_ENDPOINT_ARRANGEMENT_BRANCH": 48,
    }, "R248 pre-correction side census")
    return sheets, bulks


def wall_sheet(row: dict[str, Any]) -> SourceFeature:
    return source_feature(
        row, package="R248", filename=R248,
        table="formal_wall_half_open_sheet_owner_ledger",
        id_field="wall_sheet_node_id", feature_kind="SHEET",
        role="GRAPH_SHEET", branch=None, key_field="owner_official_key_id",
    )


def wall_side(row: dict[str, Any], role: str, edge_id: str | None) -> SourceFeature:
    edge = {"mixed_sheet_edge_id": edge_id} if edge_id is not None else None
    return source_feature(
        row, package="R248", filename=R248,
        table="formal_wall_positive_volume_bulk_ledger",
        id_field="wall_bulk_node_id", feature_kind="POSITIVE_3D_SIDE",
        role=role, branch=row["branch_label"], edge=edge,
    )


def endpoint_graphs(corrections: dict[str, dict[str, Any]]) -> list[SourceGraph]:
    sheets, bulks = wall_features()
    result: list[SourceGraph] = []
    seen_single: set[str] = set()
    used_corrections: set[str] = set()
    single_sides = 0
    for row in plain_rows(R235, "single_endpoint_graph_partition_rows"):
        source = row["endpoint_graph_partition_row_id"]
        interface = row["Round220_split_interface_id"]
        endpoint = row["active_endpoint_factor"]
        need(endpoint in {"source", "target"} and source not in seen_single,
             "R235 exact graph identity")
        seen_single.add(source)
        sheet = sheets[("ROUND235_SINGLE_ENDPOINT_GRAPH_SHEET", source, endpoint)]
        branches = bulks[source]
        need(set(branches) == {"EVENT_ABSENT", "EVENT_PRESENT"}, "R235 exact pre-correction branches")
        need(
            sheet["Round220_split_interface_id"] == interface
            and all(b["Round220_split_interface_id"] == interface for b in branches.values()),
            "R235/R248 interface lineage",
        )
        need(sheet["owner_wall_bulk_node_id"] == branches["EVENT_ABSENT"]["wall_bulk_node_id"],
             "R248 absent sheet owner")
        correction = corrections.get(source)
        retained = dict(branches)
        if correction is not None:
            empty = correction["empty_branch_label"]
            need(
                correction["Round220_split_interface_id"] == interface
                and correction["empty_wall_bulk_node_id"] == branches[empty]["wall_bulk_node_id"]
                and correction["retained_t0_sheet_node_id"] == sheet["wall_sheet_node_id"],
                "R264 exact source/interface/node/sheet backjoin",
            )
            if empty == "EVENT_ABSENT":
                need(correction["invalid_Round248_owner_edge_id"] == sheet["owner_mixed_sheet_edge_id"],
                     "R264 absent invalid-edge backjoin")
            else:
                need(correction["invalid_Round248_owner_edge_id"] is None,
                     "R264 present phantom has no edge")
            del retained[empty]
            used_corrections.add(source)
        need(sheet["owner_official_key_id"] == row["event_absent_signature"]["official_key_id"],
             "R235/R248 sheet key metadata")
        for branch, bulk in branches.items():
            signature = row["event_absent_signature" if branch == "EVENT_ABSENT" else "event_present_signature"]
            need(bulk["official_key_id"] == signature["official_key_id"],
                 "R235/R248 branch key metadata")
        side_features = tuple(
            wall_side(
                bulk, branch,
                sheet["owner_mixed_sheet_edge_id"]
                if branch == "EVENT_ABSENT"
                and (correction is None or correction["empty_branch_label"] != "EVENT_ABSENT")
                else None,
            )
            for branch, bulk in sorted(retained.items())
        )
        result.append(SourceGraph(
            graph_id=source, family="R235_SINGLE_ENDPOINT_GRAPH", source_round=235,
            filename=R235, table="single_endpoint_graph_partition_rows",
            source_row_id=source, source_row_sha256=digest(row),
            interface_id=interface, endpoint_factor=endpoint,
            official_key_ids=tuple(sorted({
                row["event_absent_signature"]["official_key_id"],
                row["event_present_signature"]["official_key_id"],
            })),
            sheet=wall_sheet(sheet), sides=side_features,
            correction_source_id=(source if correction is not None else None),
        ))
        single_sides += len(side_features)
    need(len(seen_single) == 38_328 and single_sides == 76_256,
         "R235/R248 exact 38328 sheets and corrected 76256 sides")
    need(used_corrections == set(corrections), "every R264 correction consumed once")

    partitions = 0
    double_sides = 0
    distinct_double_side_members: set[str] = set()
    for row in plain_rows(R236, "double_endpoint_partition_rows"):
        source = row["double_endpoint_partition_row_id"]
        interface = row["Round220_split_interface_id"]
        need(
            row["source_factor_strict_t_derivative_sign"] == "STRICT_POSITIVE"
            and row["target_factor_strict_t_derivative_sign"] == "STRICT_POSITIVE",
            "R236 exact double routing condition",
        )
        branches = bulks[source]
        need(set(branches) == {
            "SAME_SIGN_EVENT_ABSENT", "NEGATIVE_TO_POSITIVE", "POSITIVE_TO_NEGATIVE",
        }, "R236 exact three branches")
        signatures = {
            "SAME_SIGN_EVENT_ABSENT": row["same_sign_event_absent_signature"],
            "NEGATIVE_TO_POSITIVE": row["negative_to_positive_signature"],
            "POSITIVE_TO_NEGATIVE": row["positive_to_negative_signature"],
        }
        for branch, bulk in branches.items():
            need(
                bulk["Round220_split_interface_id"] == interface
                and bulk["official_key_id"] == signatures[branch]["official_key_id"],
                "R236/R248 lineage then key metadata",
            )
        routing = {"source": "NEGATIVE_TO_POSITIVE", "target": "POSITIVE_TO_NEGATIVE"}
        for endpoint in ("source", "target"):
            sheet = sheets[("ROUND236_DOUBLE_ENDPOINT_GRAPH_SHEET", source, endpoint)]
            need(
                sheet["Round220_split_interface_id"] == interface
                and sheet["owner_wall_bulk_node_id"] == branches["SAME_SIGN_EVENT_ABSENT"]["wall_bulk_node_id"],
                "R236/R248 double sheet owner",
            )
            need(sheet["owner_official_key_id"] == signatures["SAME_SIGN_EVENT_ABSENT"]["official_key_id"],
                 "R236 double sheet key metadata")
            selected = ("SAME_SIGN_EVENT_ABSENT", routing[endpoint])
            side_features = tuple(
                wall_side(
                    branches[branch], endpoint + ":" + branch,
                    sheet["owner_mixed_sheet_edge_id"] if branch == "SAME_SIGN_EVENT_ABSENT" else None,
                )
                for branch in selected
            )
            distinct_double_side_members.update(feature.member_id for feature in side_features)
            result.append(SourceGraph(
                graph_id="round306b1g0-double-graph:" + digest([source, endpoint]),
                family="R236_DOUBLE_ENDPOINT_GRAPH", source_round=236,
                filename=R236, table="double_endpoint_partition_rows",
                source_row_id=source, source_row_sha256=digest(row),
                interface_id=interface, endpoint_factor=endpoint,
                official_key_ids=tuple(sorted({s["official_key_id"] for s in signatures.values()})),
                sheet=wall_sheet(sheet), sides=side_features,
            ))
            double_sides += 2
        partitions += 1
    need(partitions == 16 and len(result) == 38_360 and double_sides == 64,
         "R236 16 partitions to 32 graphs and 64 side references")
    need(len(distinct_double_side_members) == 48, "R236/R248 48 distinct side members")
    return result


def bind_complete_b0(graphs: list[SourceGraph]) -> tuple[
    dict[str, dict[str, Any]], dict[str, list[SourceFeature]],
]:
    references: dict[str, list[SourceFeature]] = defaultdict(list)
    for graph in graphs:
        references[graph.sheet.member_id].append(graph.sheet)
        for side in graph.sides:
            references[side.member_id].append(side)
    need(len(references) == 115_456, "115456 distinct B0 members referenced")

    bound: dict[str, dict[str, Any]] = {}
    full_census = 0
    for row in stream_source_rows(
        B0, '"member_support_source_rows":[', compressed=True,
    ):
        check_row(row, "B0 member")
        full_census += 1
        member = row.get("member_id")
        if member not in references:
            continue
        need(member not in bound, "unique selected B0 member")
        need(
            row.get("identity_class") == "VALID_VIRTUAL_STRATUM"
            and row.get("member_identity_preserved") is True,
            "B0 virtual identity",
        )
        need(
            row.get("formal_maximality_credit") == 0
            and row.get("formal_fibre_credit") == 0
            and row.get("formal_global_disposition_credit") == 0,
            "B0 zero downstream credit",
        )
        examples = references[member]
        first = examples[0]
        need(
            all(
                item.package == first.package
                and item.source_row_sha256 == first.source_row_sha256
                and item.feature_kind == first.feature_kind
                for item in examples
            ),
            "repeated feature references have identical source lineage",
        )
        if first.package == "R245":
            need(row["identity_tranche"] == "INHERITED_ROUND247_VIRTUAL_STRATUM",
                 "B0 R245 tranche")
            need(
                row["inherited_virtual_source_package"] == "R245"
                and row["inherited_virtual_source_row_id"] == member
                and row["inherited_virtual_source_row_sha256"] == first.source_row_sha256,
                "B0 exact R245 inherited lineage",
            )
        else:
            expected_tranche = (
                "ROUND248_WALL_SHEET" if first.feature_kind == "SHEET"
                else "ROUND248_WALL_BULK"
            )
            need(row["identity_tranche"] == expected_tranche, "B0 exact R248 tranche")
            need(
                row["inherited_virtual_source_package"] is None
                and row["inherited_virtual_source_row_id"] is None
                and row["inherited_virtual_source_row_sha256"] is None,
                "B0 R248 non-alias lineage",
            )
        need(
            row["pair_denominator_class"]
            == ("VIRTUAL_SHEET" if first.feature_kind == "SHEET" else "VIRTUAL_POSITIVE_3D")
            and row["physical_dimension_profile"]
            == ("HALF_OPEN_2D_SHEET" if first.feature_kind == "SHEET" else "POSITIVE_3D_CARRIER"),
            "B0 feature dimension profile",
        )
        # Never used for selection or routing: consistency only after exact ID lineage.
        need(all(row["official_key_id"] == item.official_key_id for item in examples),
             "B0 official-key metadata consistency")
        bound[member] = row
    need(full_census == 564_492, "full B0 scan denominator")
    need(set(bound) == set(references), "complete B0 backbinding")
    return bound, references


def zero_credit() -> dict[str, int]:
    return {
        "graph_definition": 0, "physical_incidence": 0, "full_support": 0,
        "maximality": 0, "fibre": 0, "global_disposition": 0,
    }


def assert_zero_credit(value: Any, label: str) -> None:
    if type(value) is dict:
        for key, item in value.items():
            if "credit" in key.lower():
                if type(item) is dict:
                    need(all(type(number) is int and number == 0 for number in item.values()),
                         label + ":credit-map")
                else:
                    need(type(item) is int and item == 0, label + ":credit")
            else:
                assert_zero_credit(item, label + ":" + key)
    elif type(value) is list:
        for index, item in enumerate(value):
            assert_zero_credit(item, label + ":" + str(index))


def graph_inventory_id(graph_id: str) -> str:
    return "round306b1g0-graph-source:" + digest(graph_id)


def backbinding_id(member_id: str) -> str:
    return "round306b1g0-b0-backbinding:" + digest(member_id)


def ledger_envelope(kind: str, ledger: ExpectedLedger) -> dict[str, Any]:
    payload = {
        "schema": SCHEMA + "." + kind + "-ledger.v1",
        "status": "PRIVATE_ZERO_CREDIT_GRAPH_SOURCE_INVENTORY_JOIN_FREEZE_CANDIDATE",
        **ledger.metadata(),
        "formal_credit": zero_credit(),
    }
    return {**payload, "ledger_sha256": digest(payload)}


def strict_boundary() -> dict[str, Any]:
    return {
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
    }


def verify_sealed_companions() -> None:
    b0_result = load_source_object(
        "cm2_round306b0_source_g_r306a_universe_support_source_freeze_result.json"
    )
    need(
        b0_result.get("status")
        == "PASS_ROUND306B0_CURRENT_UNIVERSE_AND_PAIR_DENOMINATOR_FREEZE__CREDIT_REQUIRES_INDEPENDENT_VERIFICATION_MARKER__ZERO_MAXIMALITY_FIBRE_AND_GLOBAL_CREDIT",
        "sealed B0 result status",
    )
    b0_verification = load_source_object(
        "cm2_round306b0_source_g_r306a_universe_support_source_freeze_verification.json"
    )
    need(
        b0_verification.get("status") == "PASS_EXACT_ROUND306B0_UNIVERSE_SUPPORT_SOURCE_FREEZE",
        "sealed B0 verification marker",
    )
    transition = b0_verification.get("formal_credit_transition_at_this_verification_marker")
    need(
        transition == {
            "fibre": 0, "global_disposition": 0, "maximality": 0,
            "member_universe_freeze": 1, "pair_denominator_freeze": 1,
        },
        "sealed B0 credit transition",
    )
    downstream = b0_verification.get("strict_downstream_boundary")
    need(
        type(downstream) is dict
        and downstream.get("D02_status") == "BLOCKED"
        and downstream.get("CM2_status") == "NO-GO_FOR_CLAIM",
        "sealed B0 downstream boundary",
    )


def reconstruct_expected() -> tuple[dict[str, ExpectedLedger], dict[str, Any]]:
    VERIFIED_SOURCE_NAMES.clear()
    corrections = correction_rows()
    graphs = transition_graphs() + endpoint_graphs(corrections)
    need(
        len(graphs) == 38_624 and len({graph.graph_id for graph in graphs}) == 38_624,
        "38624 unique graphs",
    )
    family_hist = Counter(graph.family for graph in graphs)
    need(family_hist == {
        "R242_UNIQUE_TRANSITION_GRAPH": 264,
        "R235_SINGLE_ENDPOINT_GRAPH": 38_328,
        "R236_DOUBLE_ENDPOINT_GRAPH": 32,
    }, "exact graph family partition")
    need(
        len(graphs) == 38_624
        and sum(len(graph.sides) for graph in graphs) == 76_848
        and len(graphs) + sum(len(graph.sides) for graph in graphs) == 115_472,
        "38624+76848=115472 physical incidence",
    )
    b0, references = bind_complete_b0(graphs)
    ledgers = {kind: ExpectedLedger(kind) for kind in CANDIDATE_KINDS}
    try:
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
                "feature_source_file_sha256": SOURCE_PINS[feature.filename][0],
                "feature_source_table": feature.table,
                "feature_source_row_sha256": feature.source_row_sha256,
                "Round306B0_member_support_source_row_id": source["Round306B0_member_support_source_row_id"],
                "Round306B0_member_support_source_row_sha256": source["row_sha256"],
                "Round306A_component_id": source["Round306A_component_id"],
                "identity_tranche": source["identity_tranche"],
                "physical_dimension_profile": source["physical_dimension_profile"],
                "official_key_id_metadata_only": source["official_key_id"],
                "official_key_used_as_join_or_routing_filter": False,
                "formal_credit": zero_credit(),
            }
            assert_zero_credit(payload, "member")
            ledgers["member"].append(payload)

        correction_ids: dict[str, str] = {}
        for source in sorted(corrections):
            row = corrections[source]
            output_id = "round306b1g0-r264-correction:" + digest(
                row["endpoint_empty_branch_disposition_row_id"]
            )
            correction_ids[source] = output_id
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
            assert_zero_credit(payload, "correction")
            ledgers["correction"].append(payload)

        incidence_hist: Counter[str] = Counter()
        for graph in sorted(graphs, key=lambda item: item.graph_id):
            inventory_id = graph_inventory_id(graph.graph_id)
            sheet_join_id = "round306b1g0-graph-sheet:" + digest(
                [graph.graph_id, graph.sheet.member_id]
            )
            graph_payload = {
                "schema": SCHEMA + ".graph-source-inventory-row.v1",
                ID_FIELDS["graph"]: inventory_id,
                "graph_id": graph.graph_id,
                "graph_family": graph.family,
                "source_round": graph.source_round,
                "source_filename": graph.filename,
                "source_file_sha256": SOURCE_PINS[graph.filename][0],
                "source_table": graph.table,
                "source_row_id": graph.source_row_id,
                "source_row_sha256": graph.source_row_sha256,
                "Round220_split_interface_id": graph.interface_id,
                "endpoint_factor": graph.endpoint_factor,
                "graph_local_dimension": 2,
                "graph_three_dimensional_coordinate_volume": 0,
                "graph_sheet_join_row_id": sheet_join_id,
                "graph_side_join_count": len(graph.sides),
                "R264_correction_disposition_row_id": correction_ids.get(graph.correction_source_id or ""),
                "official_key_ids_metadata_only": list(graph.official_key_ids),
                "official_key_used_as_join_or_routing_filter": False,
                "source_graph_definition_proved": False,
                "formal_credit": zero_credit(),
            }
            assert_zero_credit(graph_payload, "graph")
            ledgers["graph"].append(graph_payload)
            ledgers["gap"].append({
                "schema": SCHEMA + ".gap-row.v1",
                ID_FIELDS["gap"]: "round306b1g0-gap:graph:" + digest(graph.graph_id),
                "gap_kind": "SOURCE_FREE_GRAPH_DEFINITION_THEOREM_PENDING",
                "graph_source_inventory_row_id": inventory_id,
                "incidence_join_row_id": None,
                "member_id": graph.sheet.member_id,
                "required_closure": "derive and independently interval-verify the source-free graph equation on the complete base cell",
                "formal_credit": zero_credit(),
            })

            sheet_source = b0[graph.sheet.member_id]
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
                "sheet_source_file_sha256": SOURCE_PINS[graph.sheet.filename][0],
                "sheet_source_table": graph.sheet.table,
                "sheet_source_row_sha256": graph.sheet.source_row_sha256,
                "B0_member_backbinding_row_id": backbinding_id(graph.sheet.member_id),
                "Round306B0_member_support_source_row_id": sheet_source["Round306B0_member_support_source_row_id"],
                "join_basis": "SOURCE_ROW_ID_INTERFACE_AND_ENDPOINT_FACTOR",
                "official_key_id_metadata_only": graph.sheet.official_key_id,
                "official_key_used_as_join_or_routing_filter": False,
                "physical_incidence_proved": False,
                "formal_credit": zero_credit(),
            }
            assert_zero_credit(sheet_payload, "sheet")
            ledgers["sheet"].append(sheet_payload)
            ledgers["gap"].append({
                "schema": SCHEMA + ".gap-row.v1",
                ID_FIELDS["gap"]: "round306b1g0-gap:incidence:" + digest(sheet_join_id),
                "gap_kind": "GRAPH_TO_SHEET_PHYSICAL_IDENTIFICATION_THEOREM_PENDING",
                "graph_source_inventory_row_id": inventory_id,
                "incidence_join_row_id": sheet_join_id,
                "member_id": graph.sheet.member_id,
                "required_closure": "prove the source graph equals the sealed sheet member without using key metadata as a filter",
                "formal_credit": zero_credit(),
            })
            incidence_hist[graph.family + ":SHEET"] += 1

            for side in graph.sides:
                join_id = "round306b1g0-graph-side:" + digest(
                    [graph.graph_id, side.member_id, side.role]
                )
                side_source = b0[side.member_id]
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
                    "side_source_file_sha256": SOURCE_PINS[side.filename][0],
                    "side_source_table": side.table,
                    "side_source_row_sha256": side.source_row_sha256,
                    "source_edge_id_metadata_only": side.source_edge_id,
                    "source_edge_row_sha256_metadata_only": side.source_edge_sha256,
                    "B0_member_backbinding_row_id": backbinding_id(side.member_id),
                    "Round306B0_member_support_source_row_id": side_source["Round306B0_member_support_source_row_id"],
                    "join_basis": "SEALED_SOURCE_PARTITION_BRANCH_AND_R264_CORRECTION_DISPOSITION",
                    "official_key_id_metadata_only": side.official_key_id,
                    "official_key_used_as_join_or_routing_filter": False,
                    "physical_incidence_proved": False,
                    "formal_credit": zero_credit(),
                }
                assert_zero_credit(side_payload, "side")
                ledgers["side"].append(side_payload)
                ledgers["gap"].append({
                    "schema": SCHEMA + ".gap-row.v1",
                    ID_FIELDS["gap"]: "round306b1g0-gap:incidence:" + digest(join_id),
                    "gap_kind": "GRAPH_SIDE_POSITIVE_3D_PHYSICAL_INCIDENCE_THEOREM_PENDING",
                    "graph_source_inventory_row_id": inventory_id,
                    "incidence_join_row_id": join_id,
                    "member_id": side.member_id,
                    "required_closure": "derive a source-free one-sided embedding and verify physical incidence across the graph",
                    "formal_credit": zero_credit(),
                })
                incidence_hist[graph.family + ":SIDE"] += 1

        exact_counts = {
            "graph": 38_624, "sheet": 38_624, "side": 76_848,
            "correction": 400, "member": 115_456, "gap": 154_096,
        }
        need(
            all(ledgers[k].rows.count == count for k, count in exact_counts.items()),
            "exact six-ledger row counts",
        )
        verify_sealed_companions()
        for name in sorted(set(SOURCE_PINS) - VERIFIED_SOURCE_NAMES):
            descriptor, before = open_source(name)
            close_source(descriptor, before, name)
        need(VERIFIED_SOURCE_NAMES == set(SOURCE_PINS), "all 22 source pins observed")
        audit = {
            "graph_family_histogram": dict(sorted(family_hist.items())),
            "incidence_family_histogram": dict(sorted(incidence_hist.items())),
            "graph_count": 38_624,
            "graph_sheet_join_count": 38_624,
            "graph_side_join_count": 76_848,
            "physical_incidence_count": 115_472,
            "R264_correction_count": 400,
            "distinct_B0_member_backbinding_count": 115_456,
            "gap_count": 154_096,
            "official_key_used_as_join_or_routing_filter": False,
            "source_free_graph_definition_complete": False,
            "physical_incidence_theorem_complete": False,
            "all_output_formal_credit_zero": True,
        }
        return ledgers, audit
    except Exception:
        for ledger in ledgers.values():
            ledger.close()
        raise


def candidate_snapshot(
    descriptor: int,
) -> tuple[
    tuple[int, int, int, int, int, int, int],
    dict[str, tuple[int, int, int, int, int, int, int]],
]:
    directory = os.fstat(descriptor)
    need(
        stat.S_ISDIR(directory.st_mode) and stat.S_IMODE(directory.st_mode) == 0o700,
        "candidate directory mode700",
    )
    names = tuple(sorted(os.listdir(descriptor)))
    need(names == tuple(sorted(CANDIDATE_ORDER)), "candidate exact seven-file census")
    files: dict[str, tuple[int, int, int, int, int, int, int]] = {}
    for name in names:
        info = os.stat(name, dir_fd=descriptor, follow_symlinks=False)
        need(
            stat.S_ISREG(info.st_mode) and stat.S_IMODE(info.st_mode) == 0o600
            and info.st_nlink == 1 and 0 < info.st_size <= 3_000_000_000,
            "candidate regular mode600 nlink1 bounded:" + name,
        )
        files[name] = stat_identity(info)
    return stat_identity(directory), files


def recheck_candidate_name_binding(
    candidate: Path,
    candidate_fd: int,
    root_identity: tuple[int, int, int, int, int, int, int],
) -> None:
    root_info = os.lstat(PRIVATE_ROOT)
    need(
        stat_identity(root_info) == root_identity
        and stat.S_ISDIR(root_info.st_mode)
        and stat.S_IMODE(root_info.st_mode) == 0o700
        and not PRIVATE_ROOT.is_symlink(),
        "private root remains exact bound directory",
    )
    root_fd = os.open(
        PRIVATE_ROOT,
        os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        need(stat_identity(os.fstat(root_fd)) == root_identity,
             "private root path/fd remains bound")
        named = os.stat(candidate.name, dir_fd=root_fd, follow_symlinks=False)
        opened = os.fstat(candidate_fd)
        need(
            stat_identity(named) == stat_identity(opened)
            and stat.S_ISDIR(named.st_mode)
            and stat.S_IMODE(named.st_mode) == 0o700,
            "candidate name remains exact fd-bound direct child",
        )
    finally:
        os.close(root_fd)


def open_candidate_after_reconstruction(candidate: Path) -> tuple[Path, int, Any]:
    root = Path(os.path.abspath(os.fspath(PRIVATE_ROOT)))
    requested = Path(os.path.abspath(os.fspath(candidate)))
    need(requested.parent == root and requested.name not in {"", ".", ".."},
         "candidate direct child of dedicated private root")
    need(root != DATA and DATA not in root.parents and root not in DATA.parents,
         "private root isolated from deliverables")
    root_info = os.lstat(root)
    need(
        stat.S_ISDIR(root_info.st_mode) and not root.is_symlink()
        and stat.S_IMODE(root_info.st_mode) == 0o700,
        "private candidate root exact directory",
    )
    root_fd = os.open(
        root,
        os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0),
    )
    descriptor = -1
    try:
        root_identity = stat_identity(root_info)
        need(stat_identity(os.fstat(root_fd)) == root_identity, "private root path/fd binding")
        path_info = os.stat(requested.name, dir_fd=root_fd, follow_symlinks=False)
        need(
            stat.S_ISDIR(path_info.st_mode)
            and stat.S_IMODE(path_info.st_mode) == 0o700,
            "candidate exact direct-child directory",
        )
        descriptor = os.open(
            requested.name,
            os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0),
            dir_fd=root_fd,
        )
        need(stat_identity(os.fstat(descriptor)) == stat_identity(path_info),
             "candidate dirfd name/fd binding")
        snapshot = candidate_snapshot(descriptor)
        recheck_candidate_name_binding(requested, descriptor, root_identity)
        return requested, descriptor, (snapshot, root_identity)
    except Exception:
        if descriptor >= 0:
            os.close(descriptor)
        raise
    finally:
        os.close(root_fd)


def hash_at(directory_fd: int, name: str, maximum: int = 3_000_000_000) -> str:
    descriptor = os.open(
        name, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=directory_fd,
    )
    try:
        before = os.fstat(descriptor)
        need(
            stat.S_ISREG(before.st_mode) and stat.S_IMODE(before.st_mode) == 0o600
            and before.st_nlink == 1 and 0 < before.st_size <= maximum,
            "hash-at exact candidate file:" + name,
        )
        observed, after = hash_fd(descriptor, maximum)
        named = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
        need(stat_identity(before) == stat_identity(after) == stat_identity(named),
             "hash-at fd/name stability:" + name)
        return observed
    finally:
        os.close(descriptor)


def candidate_hashes(candidate_fd: int) -> dict[str, str]:
    return {name: hash_at(candidate_fd, name) for name in CANDIDATE_ORDER}


def read_bytes_at(directory_fd: int, name: str, maximum: int) -> bytes:
    descriptor = os.open(
        name, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=directory_fd,
    )
    try:
        before = os.fstat(descriptor)
        need(
            stat.S_ISREG(before.st_mode) and stat.S_IMODE(before.st_mode) == 0o600
            and before.st_nlink == 1 and 0 < before.st_size <= maximum,
            "bounded candidate bytes:" + name,
        )
        blocks: list[bytes] = []
        total = 0
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            total += len(block)
            need(total <= maximum, "bounded candidate read:" + name)
            blocks.append(block)
        named = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
        need(stat_identity(before) == stat_identity(os.fstat(descriptor)) == stat_identity(named),
             "candidate read fd/name stability:" + name)
        return b"".join(blocks)
    finally:
        os.close(descriptor)


def iter_exact_candidate_array(text: TextIO, initial: str) -> Iterator[dict[str, Any]]:
    buffer = initial
    require_comma = False
    while True:
        buffer = buffer.lstrip()
        while not buffer:
            block = text.read(1 << 20)
            need(bool(block), "truncated candidate array")
            buffer += block
            buffer = buffer.lstrip()
        if buffer[0] == "]":
            buffer = buffer[1:].lstrip()
            while not buffer:
                block = text.read(1 << 20)
                need(bool(block), "candidate ledger missing outer close")
                buffer += block
                buffer = buffer.lstrip()
            need(buffer[0] == "}", "candidate ledger outer close")
            need(not buffer[1:].strip(), "candidate ledger trailing bytes")
            while True:
                trailing = text.read(1 << 20)
                if not trailing:
                    break
                need(not trailing.strip(), "candidate ledger trailing bytes or gzip member")
            return
        if require_comma:
            need(buffer[0] == ",", "candidate array missing comma")
            buffer = buffer[1:].lstrip()
            while not buffer:
                block = text.read(1 << 20)
                need(bool(block), "candidate array truncated after comma")
                buffer += block
                buffer = buffer.lstrip()
            need(buffer[0] != "]", "candidate array trailing comma")
        else:
            need(buffer[0] != ",", "candidate array leading comma")
        while True:
            try:
                row, end = DECODER.raw_decode(buffer)
                break
            except json.JSONDecodeError:
                block = text.read(1 << 20)
                need(bool(block), "truncated candidate row")
                buffer += block
                need(len(buffer) <= (1 << 24), "bounded candidate row")
        need(type(row) is dict, "candidate row object")
        yield row
        buffer = buffer[end:]
        require_comma = True


def validate_single_gzip_member(descriptor: int, name: str) -> None:
    """Reject truncation and every concatenated gzip member, even whitespace."""
    os.lseek(descriptor, 0, os.SEEK_SET)
    inflater = zlib.decompressobj(16 + zlib.MAX_WBITS)
    expanded = 0
    while True:
        block = os.read(descriptor, 1 << 20)
        if not block:
            break
        pending = block
        while pending:
            chunk = inflater.decompress(pending, 1 << 20)
            expanded += len(chunk)
            need(expanded <= (16 << 30), "bounded gzip expansion:" + name)
            need(not inflater.unused_data, "single gzip member required:" + name)
            remainder = inflater.unconsumed_tail
            need(remainder != pending or bool(chunk) or inflater.eof,
                 "gzip decoder progress:" + name)
            pending = remainder
            if inflater.eof:
                need(not pending, "gzip trailing member bytes:" + name)
                break
    need(inflater.eof and not inflater.unused_data and not inflater.unconsumed_tail,
         "complete single gzip member:" + name)
    inflater.flush()
    os.lseek(descriptor, 0, os.SEEK_SET)


def compare_candidate_ledger(
    candidate_fd: int,
    kind: str,
    expected: ExpectedLedger,
) -> None:
    name = FILES[kind]
    descriptor = os.open(
        name, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=candidate_fd,
    )
    raw = os.fdopen(descriptor, "rb", closefd=False)
    zipped: gzip.GzipFile | None = None
    text: TextIO | None = None
    try:
        before = os.fstat(descriptor)
        need(
            stat.S_ISREG(before.st_mode) and stat.S_IMODE(before.st_mode) == 0o600
            and before.st_nlink == 1,
            "candidate ledger exact file:" + name,
        )
        need(
            os.pread(descriptor, 10, 0) == b"\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xff",
            "deterministic gzip header:" + name,
        )
        validate_single_gzip_member(descriptor, name)
        zipped = gzip.GzipFile(fileobj=raw, mode="rb")
        text = io.TextIOWrapper(zipped, encoding="utf-8", newline="")
        marker = ',"' + TABLES[kind] + '":['
        prelude = ""
        while marker not in prelude:
            block = text.read(1 << 16)
            need(bool(block), "candidate ledger table marker:" + kind)
            prelude += block
            need(len(prelude) <= (1 << 20), "bounded candidate ledger header")
        need(prelude.count(marker) == 1, "unique candidate ledger marker")
        prefix, initial = prelude.split(marker, 1)
        envelope = strict_object((prefix + "}").encode("utf-8"), kind + " envelope")
        need(envelope == ledger_envelope(kind, expected), "exact ledger envelope:" + kind)
        expected_lines = iter(expected.expected_lines())
        observed_count = 0
        for row in iter_exact_candidate_array(text, initial):
            check_row(row, "candidate " + kind + " row")
            try:
                expected_line = next(expected_lines)
            except StopIteration as error:
                raise VerificationBlocked("candidate ledger has extra row:" + kind) from error
            need(canonical(row) == expected_line, "candidate row equals reconstruction:" + kind)
            observed_count += 1
        try:
            next(expected_lines)
        except StopIteration:
            pass
        else:
            raise VerificationBlocked("candidate ledger missing reconstructed row:" + kind)
        need(observed_count == expected.rows.count, "candidate exact row count:" + kind)
        named = os.stat(name, dir_fd=candidate_fd, follow_symlinks=False)
        need(stat_identity(before) == stat_identity(os.fstat(descriptor)) == stat_identity(named),
             "candidate ledger fd/name stable:" + kind)
    finally:
        if text is not None:
            try:
                text.detach()
            except Exception:
                pass
        if zipped is not None and not zipped.closed:
            zipped.close()
        if not raw.closed:
            raw.close()
        os.close(descriptor)


def expected_result(
    ledgers: dict[str, ExpectedLedger],
    audit: dict[str, Any],
    hashes: dict[str, str],
) -> dict[str, Any]:
    output_ledgers: dict[str, Any] = {}
    for kind in CANDIDATE_KINDS:
        envelope = ledger_envelope(kind, ledgers[kind])
        output_ledgers[kind] = {
            "filename": FILES[kind],
            "file_sha256": hashes[FILES[kind]],
            **ledgers[kind].metadata(),
            "ledger_sha256": envelope["ledger_sha256"],
        }
    payload = {
        "schema": SCHEMA,
        "status": "PRIVATE_ZERO_CREDIT_GRAPH_SOURCE_INVENTORY_AND_JOIN_FREEZE_CANDIDATE",
        "producer_file_sha256": EXPECTED_PRODUCER_SHA256,
        "audit": audit,
        "output_ledgers": output_ledgers,
        "strict_boundary": strict_boundary(),
        "candidate_is_formal": False,
    }
    return {**payload, "result_sha256": digest(payload)}


def admit_candidate(
    candidate: Path,
    producer_runtime: tuple[int, os.stat_result, str],
    verifier_runtime: tuple[int, os.stat_result, str],
) -> tuple[Path, int, dict[str, str], dict[str, Any], dict[str, Any], dict[str, ExpectedLedger]]:
    # This function is called only after the main hard gate.  Reconstruction
    # deliberately completes before the candidate path is even lstat'ed.
    ledgers, audit = reconstruct_expected()
    candidate_path = Path()
    candidate_fd = -1
    try:
        candidate_path, candidate_fd, admission = open_candidate_after_reconstruction(candidate)
        before, root_identity = admission
        hashes = candidate_hashes(candidate_fd)
        for kind in CANDIDATE_KINDS:
            compare_candidate_ledger(candidate_fd, kind, ledgers[kind])
        result = strict_object(
            read_bytes_at(candidate_fd, FILES["result"], 20_000_000),
            "candidate result",
        )
        need(result == expected_result(ledgers, audit, hashes),
             "candidate result exact independent reconstruction")
        need(hashlib.sha256(canonical(result)).hexdigest() == hashes[FILES["result"]],
             "candidate result exact canonical wire bytes")
        need(candidate_snapshot(candidate_fd) == before, "candidate snapshot stable")
        need(candidate_hashes(candidate_fd) == hashes, "candidate hashes stable")
        recheck_candidate_name_binding(candidate_path, candidate_fd, root_identity)
        recheck_runtime(*producer_runtime, PRODUCER)
        recheck_runtime(*verifier_runtime, VERIFIER)
        return candidate_path, candidate_fd, hashes, result, audit, ledgers
    except Exception:
        if candidate_fd >= 0:
            os.close(candidate_fd)
        for ledger in ledgers.values():
            ledger.close()
        raise


def rejected(callback: Callable[[], None]) -> bool:
    try:
        callback()
    except (VerificationBlocked, ValueError, OSError, json.JSONDecodeError):
        return True
    return False


def semantic_contract(value: dict[str, Any]) -> None:
    keys = {
        "graphs", "sheets", "sides", "incidence", "R242_graphs",
        "R245_sheets", "R245_sides", "R235_graphs", "R248_single_pre_sides",
        "R264_total", "R264_absent_prunes", "R264_present_drops",
        "R248_single_sides", "R236_partitions", "R236_graphs",
        "R236_distinct_side_members", "R236_side_refs", "B0_members",
        "graph_gaps", "incidence_gaps", "total_gaps",
        "graph_definition_credit", "physical_incidence_credit",
        "full_support_credit", "maximality_credit", "fibre_credit",
        "global_credit", "official_key_filter", "D02", "CM2",
        "attack_first", "verification_last", "candidate_is_formal",
        "formal_marker_required", "verification_grants_theorem_credit",
    }
    need(set(value) == keys, "semantic exact key set")
    need(
        value["graphs"] == value["sheets"] == 38_624
        and value["sides"] == 76_848
        and value["incidence"] == value["sheets"] + value["sides"] == 115_472,
        "semantic graph/sheet/side incidence arithmetic",
    )
    need(
        value["R242_graphs"] == value["R245_sheets"] == 264
        and value["R245_sides"] == 528
        and value["R245_sheets"] + value["R245_sides"] == 792,
        "semantic R242/R245 join",
    )
    need(
        value["R235_graphs"] == 38_328
        and value["R248_single_pre_sides"] == 76_656
        and value["R264_total"] == 400
        and value["R264_absent_prunes"] == 184
        and value["R264_present_drops"] == 216
        and value["R264_absent_prunes"] + value["R264_present_drops"] == value["R264_total"]
        and value["R248_single_pre_sides"] - value["R264_total"]
        == value["R248_single_sides"] == 76_256
        and value["R235_graphs"] + value["R248_single_sides"] == 114_584,
        "semantic R235/R248/R264 corrected join",
    )
    need(
        value["R236_partitions"] == 16
        and value["R236_graphs"] == 32
        and value["R236_distinct_side_members"] == 48
        and value["R236_side_refs"] == 64
        and value["R236_graphs"] + value["R236_side_refs"] == 96,
        "semantic R236/R248 double join",
    )
    need(
        value["R242_graphs"] + value["R235_graphs"] + value["R236_graphs"]
        == value["graphs"]
        and value["R245_sides"] + value["R248_single_sides"] + value["R236_side_refs"]
        == value["sides"],
        "semantic family totals",
    )
    need(value["B0_members"] == 115_456, "semantic complete B0 backbinding")
    need(
        value["graph_gaps"] == 38_624
        and value["incidence_gaps"] == 115_472
        and value["total_gaps"] == 154_096
        and value["graph_gaps"] + value["incidence_gaps"] == value["total_gaps"],
        "semantic gap denominator",
    )
    need(
        value["graph_definition_credit"] == value["physical_incidence_credit"]
        == value["full_support_credit"] == value["maximality_credit"]
        == value["fibre_credit"] == value["global_credit"] == 0,
        "semantic all theorem/credit zero",
    )
    need(
        value["official_key_filter"] is False
        and value["D02"] == "BLOCKED"
        and value["CM2"] == "NO-GO_FOR_CLAIM",
        "semantic metadata-only key and downstream boundary",
    )
    need(
        value["attack_first"] is True
        and value["verification_last"] is True
        and value["candidate_is_formal"] is False
        and value["formal_marker_required"] is True
        and value["verification_grants_theorem_credit"] is False,
        "semantic candidate-credit and publication boundary",
    )


def semantic_baseline() -> dict[str, Any]:
    return {
        "graphs": 38_624, "sheets": 38_624, "sides": 76_848,
        "incidence": 115_472, "R242_graphs": 264, "R245_sheets": 264,
        "R245_sides": 528, "R235_graphs": 38_328,
        "R248_single_pre_sides": 76_656, "R264_total": 400,
        "R264_absent_prunes": 184, "R264_present_drops": 216,
        "R248_single_sides": 76_256, "R236_partitions": 16,
        "R236_graphs": 32, "R236_distinct_side_members": 48,
        "R236_side_refs": 64, "B0_members": 115_456,
        "graph_gaps": 38_624, "incidence_gaps": 115_472,
        "total_gaps": 154_096, "graph_definition_credit": 0,
        "physical_incidence_credit": 0, "full_support_credit": 0,
        "maximality_credit": 0, "fibre_credit": 0, "global_credit": 0,
        "official_key_filter": False, "D02": "BLOCKED",
        "CM2": "NO-GO_FOR_CLAIM", "attack_first": True,
        "verification_last": True, "candidate_is_formal": False,
        "formal_marker_required": True,
        "verification_grants_theorem_credit": False,
    }


def rename_noreplace(old_fd: int, old_name: str, new_fd: int, new_name: str) -> None:
    libc = ctypes.CDLL(None, use_errno=True)
    function = getattr(libc, "renameat2", None)
    need(function is not None, "renameat2 required")
    function.argtypes = [
        ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint,
    ]
    function.restype = ctypes.c_int
    if function(old_fd, os.fsencode(old_name), new_fd, os.fsencode(new_name), 1) != 0:
        code = ctypes.get_errno()
        if code == errno.EEXIST:
            raise FileExistsError(code, os.strerror(code), new_name)
        raise OSError(code, os.strerror(code), new_name)


def exact_prefix_states(
    directory_fd: int,
    order: tuple[str, ...],
    expected_hashes: dict[str, str],
) -> list[bool]:
    states: list[bool] = []
    seen_absent = False
    for name in order:
        try:
            info = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
        except FileNotFoundError:
            seen_absent = True
            states.append(False)
            continue
        need(not seen_absent, "formal bundle must be exact committed prefix")
        need(
            stat.S_ISREG(info.st_mode) and stat.S_IMODE(info.st_mode) == 0o600
            and info.st_nlink == 1,
            "formal prefix exact file:" + name,
        )
        need(hash_at(directory_fd, name) == expected_hashes[name],
             "formal prefix exact hash:" + name)
        states.append(True)
    return states


def unlink_owned_exact(
    directory_fd: int,
    name: str,
    identity: tuple[int, int],
    expected_sha256: str,
) -> bool:
    try:
        current = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
    except FileNotFoundError:
        return False
    if (current.st_dev, current.st_ino) != identity:
        return False
    if hash_at(directory_fd, name) != expected_sha256:
        return False
    os.unlink(name, dir_fd=directory_fd)
    os.fsync(directory_fd)
    return True


def transaction_attack_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="cm2-b1g0-verifier-selftest-") as temporary:
        directory = Path(temporary)
        fd = os.open(directory, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            source_fd = os.open("source", os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600, dir_fd=fd)
            os.write(source_fd, b"source")
            os.fsync(source_fd)
            source_info = os.fstat(source_fd)
            os.close(source_fd)
            target_fd = os.open("target", os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600, dir_fd=fd)
            os.write(target_fd, b"target")
            os.close(target_fd)
            blocked = False
            try:
                rename_noreplace(fd, "source", fd, "target")
            except FileExistsError:
                blocked = True
            need(blocked, "rename no-clobber attack rejected")
            rows.append(close_row({
                "attack_name": "renameat2_existing_target_no_clobber",
                "attack_class": "FILESYSTEM_TRANSACTION",
                "expected": "REJECT",
                "observed": "REJECT",
            }))
            os.unlink("target", dir_fd=fd)
            rename_noreplace(fd, "source", fd, "published")
            published = os.stat("published", dir_fd=fd, follow_symlinks=False)
            need((published.st_dev, published.st_ino) == (source_info.st_dev, source_info.st_ino),
                 "rename inode preservation")
            os.unlink("published", dir_fd=fd)

            os.mkdir("copy-source", 0o700, dir_fd=fd)
            os.mkdir("copy-stage", 0o700, dir_fd=fd)
            copy_source_fd = os.open(
                "copy-source", os.O_RDONLY | getattr(os, "O_DIRECTORY", 0), dir_fd=fd
            )
            copy_stage_fd = os.open(
                "copy-stage", os.O_RDONLY | getattr(os, "O_DIRECTORY", 0), dir_fd=fd
            )
            try:
                for directory_fd, payload in (
                    (copy_source_fd, b"candidate"),
                    (copy_stage_fd, b"preexisting-stage-target"),
                ):
                    item_fd = os.open(
                        "bundle", os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                        0o600, dir_fd=directory_fd,
                    )
                    os.write(item_fd, payload)
                    os.close(item_fd)
                descriptor_count = len(os.listdir("/proc/self/fd"))
                try:
                    copy_candidate_to_stage(
                        copy_source_fd,
                        copy_stage_fd,
                        "bundle",
                        hashlib.sha256(b"candidate").hexdigest(),
                    )
                except FileExistsError:
                    pass
                else:
                    raise VerificationBlocked("stage-copy existing-target attack accepted")
                need(
                    len(os.listdir("/proc/self/fd")) == descriptor_count,
                    "stage-copy O_EXCL rejection leaked no source descriptor",
                )
                target_check = os.open("bundle", os.O_RDONLY, dir_fd=copy_stage_fd)
                try:
                    need(os.read(target_check, 100) == b"preexisting-stage-target",
                         "stage-copy existing target unchanged")
                finally:
                    os.close(target_check)
                rows.append(close_row({
                    "attack_name": "candidate_stage_copy_existing_target_no_clobber_no_fd_leak",
                    "attack_class": "FILESYSTEM_TRANSACTION",
                    "expected": "REJECT",
                    "observed": "REJECT",
                }))
            finally:
                os.close(copy_source_fd)
                os.close(copy_stage_fd)

            late_fd = os.open(
                "prefix-second", os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                0o600, dir_fd=fd,
            )
            os.write(late_fd, b"second")
            os.close(late_fd)
            prefix_hashes = {
                "prefix-first": hashlib.sha256(b"first").hexdigest(),
                "prefix-second": hashlib.sha256(b"second").hexdigest(),
            }
            need(
                rejected(lambda: exact_prefix_states(
                    fd, ("prefix-first", "prefix-second"), prefix_hashes
                )),
                "out-of-order recovery prefix rejected",
            )
            os.unlink("prefix-second", dir_fd=fd)
            rows.append(close_row({
                "attack_name": "verification_transaction_out_of_order_prefix_recovery",
                "attack_class": "FILESYSTEM_TRANSACTION",
                "expected": "REJECT",
                "observed": "REJECT",
            }))

            marker_raw = b"owned-marker"
            marker_fd = os.open(
                "marker", os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                0o600, dir_fd=fd,
            )
            os.write(marker_fd, marker_raw)
            os.fsync(marker_fd)
            marker_info = os.fstat(marker_fd)
            os.close(marker_fd)
            need(unlink_owned_exact(
                fd, "marker", (marker_info.st_dev, marker_info.st_ino),
                hashlib.sha256(marker_raw).hexdigest(),
            ), "owned marker exact rollback")
            rows.append(close_row({
                "attack_name": "verification_marker_owned_inode_exact_rollback",
                "attack_class": "FILESYSTEM_TRANSACTION",
                "expected": "REMOVE_EXACT_OWNED_MARKER",
                "observed": "REMOVE_EXACT_OWNED_MARKER",
            }))

            old_fd = os.open(
                "marker", os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                0o600, dir_fd=fd,
            )
            os.write(old_fd, marker_raw)
            os.fsync(old_fd)
            old_info = os.fstat(old_fd)
            os.unlink("marker", dir_fd=fd)
            foreign_raw = b"foreign-marker"
            foreign_fd = os.open(
                "marker", os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                0o600, dir_fd=fd,
            )
            os.write(foreign_fd, foreign_raw)
            os.fsync(foreign_fd)
            os.close(foreign_fd)
            need(not unlink_owned_exact(
                fd, "marker", (old_info.st_dev, old_info.st_ino),
                hashlib.sha256(marker_raw).hexdigest(),
            ), "foreign replacement marker preserved")
            check_fd = os.open("marker", os.O_RDONLY, dir_fd=fd)
            try:
                need(os.read(check_fd, 100) == foreign_raw,
                     "foreign marker bytes preserved")
            finally:
                os.close(check_fd)
                os.close(old_fd)
            os.unlink("marker", dir_fd=fd)
            rows.append(close_row({
                "attack_name": "verification_marker_foreign_inode_not_rolled_back",
                "attack_class": "FILESYSTEM_TRANSACTION",
                "expected": "PRESERVE_FOREIGN_REPLACEMENT",
                "observed": "PRESERVE_FOREIGN_REPLACEMENT",
            }))
        finally:
            os.close(fd)
    return rows


def wire_attack_rows() -> list[dict[str, Any]]:
    def gzip_fixture(raw: bytes) -> None:
        with tempfile.TemporaryFile(mode="w+b") as fixture:
            fixture.write(raw)
            fixture.flush()
            validate_single_gzip_member(fixture.fileno(), "wire fixture")

    attacks: tuple[tuple[str, Callable[[], None]], ...] = (
        ("duplicate_top_key", lambda: strict_object(b'{"a":1,"a":1}', "dup")),
        ("floating_number", lambda: strict_object(b'{"a":1.0}', "float")),
        ("NaN_constant", lambda: strict_object(b'{"a":NaN}', "nan")),
        ("top_level_array", lambda: strict_object(b'[]', "array")),
        ("utf8_BOM", lambda: strict_object(b'\xef\xbb\xbf{}', "bom")),
        ("NUL_byte", lambda: strict_object(b'{"a":1}\x00', "nul")),
        (
            "candidate_array_trailing_comma",
            lambda: list(iter_exact_candidate_array(io.StringIO(""), '{"a":1},]}')),
        ),
        (
            "candidate_array_missing_comma",
            lambda: list(iter_exact_candidate_array(io.StringIO(""), '{"a":1}{"b":2}]}')),
        ),
        (
            "concatenated_second_gzip_member",
            lambda: gzip_fixture(
                gzip.compress(b"{}", compresslevel=9, mtime=0)
                + gzip.compress(b" ", compresslevel=9, mtime=0)
            ),
        ),
        (
            "truncated_gzip_member",
            lambda: gzip_fixture(gzip.compress(b"{}", compresslevel=9, mtime=0)[:-3]),
        ),
    )
    rows: list[dict[str, Any]] = []
    for name, callback in attacks:
        need(rejected(callback), "wire attack rejected:" + name)
        rows.append(close_row({
            "attack_name": name,
            "attack_class": "STRICT_WIRE_GRAMMAR",
            "expected": "REJECT",
            "observed": "REJECT",
        }))
    return rows


def build_attack_suite(
    candidate_file_sha256s: dict[str, str] | None,
    verifier_sha256: str,
) -> dict[str, Any]:
    baseline = semantic_baseline()
    semantic_contract(baseline)
    mutations: tuple[tuple[str, str, Any], ...] = (
        ("graph_denominator_forgery", "graphs", 38_623),
        ("sheet_denominator_forgery", "sheets", 38_623),
        ("side_denominator_forgery", "sides", 76_847),
        ("incidence_denominator_forgery", "incidence", 115_471),
        ("R242_graph_drop", "R242_graphs", 263),
        ("R245_sheet_drop", "R245_sheets", 263),
        ("R245_side_drop", "R245_sides", 527),
        ("R235_graph_drop", "R235_graphs", 38_327),
        ("R248_pre_side_drop", "R248_single_pre_sides", 76_655),
        ("R264_correction_drop", "R264_total", 399),
        ("R264_absent_present_swap", "R264_absent_prunes", 183),
        ("R264_phantom_drop", "R264_present_drops", 215),
        ("R248_retained_side_forgery", "R248_single_sides", 76_656),
        ("R236_partition_drop", "R236_partitions", 15),
        ("R236_graph_drop", "R236_graphs", 31),
        ("R236_distinct_side_forgery", "R236_distinct_side_members", 64),
        ("R236_side_reference_drop", "R236_side_refs", 63),
        ("B0_backbinding_drop", "B0_members", 115_455),
        ("graph_gap_drop", "graph_gaps", 0),
        ("incidence_gap_drop", "incidence_gaps", 0),
        ("total_gap_drop", "total_gaps", 0),
        ("graph_definition_credit_forgery", "graph_definition_credit", 1),
        ("physical_incidence_credit_forgery", "physical_incidence_credit", 1),
        ("full_support_credit_forgery", "full_support_credit", 1),
        ("maximality_credit_forgery", "maximality_credit", 1),
        ("fibre_credit_forgery", "fibre_credit", 124),
        ("global_credit_forgery", "global_credit", 224_580),
        ("official_key_filter_forgery", "official_key_filter", True),
        ("attack_first_forgery", "attack_first", False),
        ("verification_last_forgery", "verification_last", False),
        ("candidate_formality_forgery", "candidate_is_formal", True),
        ("formal_marker_bypass", "formal_marker_required", False),
        ("marker_credit_forgery", "verification_grants_theorem_credit", True),
        ("D02_forgery", "D02", "PASS"),
        ("CM2_forgery", "CM2", "GO_FOR_CLAIM"),
    )
    semantic_rows: list[dict[str, Any]] = []
    for name, field, replacement in mutations:
        forged = dict(baseline)
        forged[field] = replacement
        need(rejected(lambda forged=forged: semantic_contract(forged)),
             "semantic mutation rejected:" + name)
        semantic_rows.append(close_row({
            "attack_name": name,
            "attack_class": "SEMANTIC_CONTRACT_UNIT",
            "mutated_field": field,
            "expected": "REJECT",
            "observed": "REJECT",
        }))
    filesystem_rows = transaction_attack_rows()
    grammar_rows = wire_attack_rows()
    rows = semantic_rows + filesystem_rows + grammar_rows
    payload = {
        "schema": SCHEMA + ".attack-suite.v1",
        "status": "PASS_ROUND306B1G0_FAIL_CLOSED_DEFENSE_IN_DEPTH_ATTACKS",
        "binding_mode": (
            "EXACT_PRIVATE_CANDIDATE" if candidate_file_sha256s is not None
            else "LIGHTWEIGHT_BLOCKED_SCAFFOLD_SELF_TEST"
        ),
        "attack_scope": {
            "semantic_rows_are_contract_unit_mutations": True,
            "wire_rows_are_strict_grammar_unit_mutations": True,
            "filesystem_rows_execute_real_temporary_directory_transaction_paths": True,
            "reconstruction_attack_count": 0,
            "full_source_reconstruction_is_not_claimed_by_this_lightweight_suite": True,
        },
        "producer": {
            "filename": PRODUCER,
            "file_sha256": EXPECTED_PRODUCER_SHA256,
            "file_size": EXPECTED_PRODUCER_SIZE,
            "treated_as_inert_bytes_only": True,
            "imported_executed_parsed_or_tokenized": False,
        },
        "runtime_verifier": {"filename": VERIFIER, "file_sha256": verifier_sha256},
        "candidate_file_sha256s": (
            dict(sorted(candidate_file_sha256s.items()))
            if candidate_file_sha256s is not None else None
        ),
        "semantic_attack_count": len(semantic_rows),
        "semantic_rejected_count": len(semantic_rows),
        "filesystem_attack_count": len(filesystem_rows),
        "filesystem_rejected_count": len(filesystem_rows),
        "wire_attack_count": len(grammar_rows),
        "wire_rejected_count": len(grammar_rows),
        "attack_count": len(rows),
        "rejected_count": len(rows),
        "all_rejected": True,
        "attack_rows_sha256": digest(rows),
        "attack_rows": rows,
    }
    return {**payload, "attack_suite_sha256": digest(payload)}


def build_verification(
    hashes: dict[str, str],
    result: dict[str, Any],
    audit: dict[str, Any],
    attacks: dict[str, Any],
    verifier_sha256: str,
) -> dict[str, Any]:
    attack_payload = dict(attacks)
    attack_claimed = attack_payload.pop("attack_suite_sha256", None)
    need(attack_claimed == digest(attack_payload), "attack suite self hash")
    payload = {
        "schema": SCHEMA + ".independent-verification.v1",
        "status": "PASS_EXACT_ROUND306B1G0_GRAPH_SOURCE_INVENTORY_AND_JOIN_FREEZE__ZERO_THEOREM_CREDIT",
        "producer": {
            "filename": PRODUCER,
            "file_sha256": EXPECTED_PRODUCER_SHA256,
            "file_size": EXPECTED_PRODUCER_SIZE,
            "treated_as_inert_pinned_bytes_only": True,
            "imported_executed_parsed_or_tokenized": False,
        },
        "runtime_verifier": {"filename": VERIFIER, "file_sha256": verifier_sha256},
        "source_snapshot": {
            "exact_file_count": len(SOURCE_PINS),
            "every_source_size_and_sha256_pinned": True,
            "pins": {
                name: {"file_sha256": pin[0], "file_size": pin[1]}
                for name, pin in sorted(SOURCE_PINS.items())
            },
            "sealed_Round306B0_verification_required": True,
            "source_fds_hash_parse_and_postread_stability_bound": True,
        },
        "independent_reconstruction": {
            "R242_R245": {
                "graphs": 264, "sheets": 264, "sides": 528, "incidence": 792,
            },
            "R235_R248_before_R264": {
                "graphs": 38_328, "sheets": 38_328, "pre_correction_sides": 76_656,
            },
            "R264_exact_corrections": {
                "total": 400, "absent_owner_prunes": 184,
                "present_phantom_drops": 216,
            },
            "R235_R248_after_R264": {
                "sides": 76_256, "incidence": 114_584,
            },
            "R236_R248": {
                "partitions": 16, "graphs": 32, "sheets": 32,
                "distinct_side_members": 48, "side_references": 64, "incidence": 96,
            },
            "totals": {
                "graphs": 38_624, "sheets": 38_624, "sides": 76_848,
                "physical_incidence": 115_472,
                "distinct_B0_member_backbindings": 115_456,
                "graph_definition_gaps": 38_624,
                "physical_incidence_gaps": 115_472, "gaps": 154_096,
            },
            "complete_B0_row_scan_count": 564_492,
            "official_key_used_only_as_post_lineage_metadata_consistency": True,
            "audit": audit,
            "producer_code_used_for_reconstruction": False,
        },
        "candidate": {
            "dedicated_private_root": PRIVATE_ROOT.name,
            "exact_seven_file_set": list(CANDIDATE_ORDER),
            "exact_file_sha256s": dict(sorted(hashes.items())),
            "result_self_sha256": result["result_sha256"],
            "candidate_opened_only_after_full_independent_reconstruction": True,
            "exact_reconstructed_row_counts": {
                "graph": 38_624, "sheet": 38_624, "side": 76_848,
                "correction": 400, "member": 115_456, "gap": 154_096,
            },
            "every_candidate_row_equal_to_reconstruction": True,
            "strict_gzip_and_JSON_grammar": True,
            "mode600_nlink1_inode_stability_required": True,
        },
        "attack_suite": {
            "filename": ATTACK,
            "file_sha256": hashlib.sha256(canonical(attacks)).hexdigest(),
            "object_self_sha256": attacks["attack_suite_sha256"],
            "attack_count": attacks["attack_count"],
            "rejected_count": attacks["rejected_count"],
            "all_rejected": True,
            "reconstruction_attack_count": 0,
            "unit_and_transaction_scope_reported_honestly": True,
        },
        "formal_credit_without_this_verification_marker": zero_credit(),
        "formal_credit_transition_at_this_verification_marker": zero_credit(),
        "strict_downstream_boundary": strict_boundary(),
        "atomic_publication": {
            "promotion_order": list(PROMOTION_ORDER),
            "attack_first": True,
            "verification_last_and_sole_package_marker": True,
            "verification_marker_grants_theorem_credit": False,
            "renameat2_RENAME_NOREPLACE": True,
            "stage_and_output_directory_fsync_after_each_rename": True,
            "exact_prefix_recovery_only": True,
            "precise_owned_marker_rollback": True,
            "no_clobber": True,
            "downstream_must_validate_complete_marker_bound_bundle": True,
            "power_loss_can_leave_recoverable_prefix_without_marker": True,
            "same_UID_hostile_namespace_races_not_cryptographically_eliminated": True,
        },
    }
    return {**payload, "verification_sha256": digest(payload)}


def exclusive_write_at(directory_fd: int, name: str, raw: bytes) -> None:
    descriptor = os.open(
        name,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
        0o600,
        dir_fd=directory_fd,
    )
    created: os.stat_result | None = None
    complete = False
    try:
        created = os.fstat(descriptor)
        offset = 0
        while offset < len(raw):
            written = os.write(descriptor, raw[offset:])
            need(written > 0, "exclusive write progress:" + name)
            offset += written
        os.fsync(descriptor)
        info = os.fstat(descriptor)
        need(
            stat.S_ISREG(info.st_mode) and stat.S_IMODE(info.st_mode) == 0o600
            and info.st_nlink == 1 and info.st_size == len(raw),
            "exclusive stage output:" + name,
        )
        complete = True
    finally:
        os.close(descriptor)
        if not complete and created is not None:
            try:
                named = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
            except FileNotFoundError:
                pass
            else:
                if (named.st_dev, named.st_ino) == (created.st_dev, created.st_ino):
                    os.unlink(name, dir_fd=directory_fd)
                    os.fsync(directory_fd)


def copy_candidate_to_stage(
    candidate_fd: int,
    stage_fd: int,
    name: str,
    expected_sha256: str,
) -> None:
    source_fd = os.open(
        name, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=candidate_fd,
    )
    target_fd = -1
    target_created: os.stat_result | None = None
    complete = False
    state = hashlib.sha256()
    try:
        target_fd = os.open(
            name,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
            0o600,
            dir_fd=stage_fd,
        )
        target_created = os.fstat(target_fd)
        source_before = os.fstat(source_fd)
        need(
            stat.S_ISREG(source_before.st_mode)
            and stat.S_IMODE(source_before.st_mode) == 0o600
            and source_before.st_nlink == 1,
            "candidate copy source exact:" + name,
        )
        while True:
            block = os.read(source_fd, 1 << 20)
            if not block:
                break
            state.update(block)
            offset = 0
            while offset < len(block):
                written = os.write(target_fd, block[offset:])
                need(written > 0, "candidate copy progress:" + name)
                offset += written
        os.fsync(target_fd)
        source_after = os.fstat(source_fd)
        target = os.fstat(target_fd)
        need(
            state.hexdigest() == expected_sha256
            and stat_identity(source_before) == stat_identity(source_after)
            and source_before.st_size == target.st_size
            and stat.S_ISREG(target.st_mode) and stat.S_IMODE(target.st_mode) == 0o600
            and target.st_nlink == 1,
            "candidate exact stage copy:" + name,
        )
        complete = True
    finally:
        os.close(source_fd)
        if target_fd >= 0:
            os.close(target_fd)
        if not complete and target_created is not None:
            try:
                named = os.stat(name, dir_fd=stage_fd, follow_symlinks=False)
            except FileNotFoundError:
                pass
            else:
                if (
                    (named.st_dev, named.st_ino)
                    == (target_created.st_dev, target_created.st_ino)
                ):
                    os.unlink(name, dir_fd=stage_fd)
                    os.fsync(stage_fd)


def stage_hash_at(directory_fd: int, name: str) -> str:
    return hash_at(directory_fd, name)


def verify_every_source_pin_again() -> None:
    for name in sorted(SOURCE_PINS):
        descriptor, before = open_source(name)
        close_source(descriptor, before, name)


def publish_formal(
    candidate_fd: int,
    hashes: dict[str, str],
    attack_raw: bytes,
    verification_raw: bytes,
    producer_runtime: tuple[int, os.stat_result, str],
    verifier_runtime: tuple[int, os.stat_result, str],
) -> None:
    expected_hashes = {
        ATTACK: hashlib.sha256(attack_raw).hexdigest(),
        **hashes,
        VERIFICATION: hashlib.sha256(verification_raw).hexdigest(),
    }
    data_fd = os.open(
        DATA,
        os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0),
    )
    stage_fd = -1
    marker_renamed = False
    marker_identity: tuple[int, int] | None = None
    try:
        fcntl.flock(data_fd, fcntl.LOCK_EX)
        states = exact_prefix_states(data_fd, PROMOTION_ORDER, expected_hashes)
        need(not states[-1], "verification marker already exists")

        stage_name = "." + PREFIX + ".promotion-stage." + digest(expected_hashes)[:24]
        try:
            os.mkdir(stage_name, 0o700, dir_fd=data_fd)
            os.fsync(data_fd)
        except FileExistsError:
            pass
        stage_info = os.stat(stage_name, dir_fd=data_fd, follow_symlinks=False)
        need(
            stat.S_ISDIR(stage_info.st_mode) and stat.S_IMODE(stage_info.st_mode) == 0o700,
            "promotion stage mode700 directory",
        )
        stage_fd = os.open(
            stage_name,
            os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0),
            dir_fd=data_fd,
        )
        need(
            (os.fstat(stage_fd).st_dev, os.fstat(stage_fd).st_ino)
            == (stage_info.st_dev, stage_info.st_ino),
            "promotion stage path/fd binding",
        )
        expected_stage = {
            name for index, name in enumerate(PROMOTION_ORDER) if not states[index]
        }
        existing_stage = set(os.listdir(stage_fd))
        need(existing_stage <= expected_stage, "promotion stage contains no foreign names")
        for name in PROMOTION_ORDER:
            if name not in expected_stage:
                continue
            if name in existing_stage:
                need(stage_hash_at(stage_fd, name) == expected_hashes[name],
                     "recovered stage file exact:" + name)
                continue
            if name == ATTACK:
                exclusive_write_at(stage_fd, name, attack_raw)
            elif name == VERIFICATION:
                exclusive_write_at(stage_fd, name, verification_raw)
            else:
                copy_candidate_to_stage(candidate_fd, stage_fd, name, hashes[name])
            need(stage_hash_at(stage_fd, name) == expected_hashes[name],
                 "new stage file exact:" + name)
            os.fsync(stage_fd)
        need(set(os.listdir(stage_fd)) == expected_stage, "complete exact promotion stage")

        candidate_before = candidate_snapshot(candidate_fd)
        recheck_runtime(*producer_runtime, PRODUCER)
        recheck_runtime(*verifier_runtime, VERIFIER)
        verify_every_source_pin_again()
        need(candidate_snapshot(candidate_fd) == candidate_before, "candidate stable before commit")
        need(candidate_hashes(candidate_fd) == hashes, "candidate hashes stable before commit")

        try:
            for index, name in enumerate(PROMOTION_ORDER):
                if states[index]:
                    continue
                need(stage_hash_at(stage_fd, name) == expected_hashes[name],
                     "pre-rename stage hash:" + name)
                source_info = os.stat(name, dir_fd=stage_fd, follow_symlinks=False)
                rename_noreplace(stage_fd, name, data_fd, name)
                if name == VERIFICATION:
                    # Record ownership immediately after rename, before any
                    # fallible postcondition, so marker rollback is precise.
                    marker_renamed = True
                    marker_identity = (source_info.st_dev, source_info.st_ino)
                os.fsync(stage_fd)
                os.fsync(data_fd)
                target_info = os.stat(name, dir_fd=data_fd, follow_symlinks=False)
                need(
                    (target_info.st_dev, target_info.st_ino)
                    == (source_info.st_dev, source_info.st_ino)
                    and stage_hash_at(data_fd, name) == expected_hashes[name],
                    "post-rename inode/hash:" + name,
                )
            need(candidate_snapshot(candidate_fd) == candidate_before,
                 "candidate stable after marker")
            need(candidate_hashes(candidate_fd) == hashes, "candidate hashes stable after marker")
            recheck_runtime(*producer_runtime, PRODUCER)
            recheck_runtime(*verifier_runtime, VERIFIER)
            for name in PROMOTION_ORDER:
                need(stage_hash_at(data_fd, name) == expected_hashes[name],
                     "complete formal bundle after marker:" + name)
            need(not os.listdir(stage_fd), "promotion stage empty after commit")
            os.rmdir(stage_name, dir_fd=data_fd)
            os.fsync(data_fd)
        except Exception:
            if marker_renamed and marker_identity is not None:
                unlink_owned_exact(
                    data_fd, VERIFICATION, marker_identity,
                    expected_hashes[VERIFICATION],
                )
            raise
    finally:
        if stage_fd >= 0:
            os.close(stage_fd)
        try:
            fcntl.flock(data_fd, fcntl.LOCK_UN)
        finally:
            os.close(data_fd)


def marker_search_regressions() -> list[str]:
    marker = '"formal_target_table":'
    array_marker = '"rows":['
    passed: list[str] = []

    cross_prefix = "x" * ((1 << 20) - 3)
    remainder = stream_find_marker(
        io.StringIO(cross_prefix + marker + "TAIL"), marker,
        chunk_size=1 << 20,
        scan_limit=len(cross_prefix) + len(marker) + 4,
    )
    need(remainder == "TAIL", "marker crossing exact 1MiB read boundary")
    passed.append("marker-crosses-1MiB-read-boundary")

    chained_stream = io.StringIO(
        "abcde" + marker + "zzzzz" + array_marker + '{"ok":1}]'
    )
    chained_initial = stream_find_marker(
        chained_stream, marker, chunk_size=7, scan_limit=200,
    )
    chained_rows = list(iter_array(
        chained_stream, array_marker, chained_initial,
        chunk_size=7, marker_scan_limit=200,
        forbidden_before_marker=(marker,),
    ))
    need(chained_rows == [{"ok": 1}], "chained table and array marker boundaries")
    passed.append("table-and-array-markers-cross-small-read-boundaries")

    class LongPrelude:
        def __init__(self, prefix_length: int, suffix: str) -> None:
            self.remaining = prefix_length
            self.suffix = suffix
            self.offset = 0

        def read(self, size: int = -1) -> str:
            need(size > 0, "parameterized marker test read size")
            if self.remaining:
                count = min(size, self.remaining)
                self.remaining -= count
                return "x" * count
            if self.offset >= len(self.suffix):
                return ""
            end = min(len(self.suffix), self.offset + size)
            block = self.suffix[self.offset:end]
            self.offset = end
            return block

    long_prefix = (1 << 25) + 12_345
    long_stream = LongPrelude(long_prefix, marker + "LONG-TAIL")
    remainder = stream_find_marker(
        long_stream, marker, chunk_size=4_093,
        scan_limit=long_prefix + len(marker) + len("LONG-TAIL"),
    )
    need(remainder == "LONG-TAIL", "legal prelude beyond 32MiB")
    passed.append("over-32MiB-prelude-small-chunk-constant-memory")

    need(rejected(lambda: stream_find_marker(
        io.StringIO("no target table here"), marker,
        chunk_size=7, scan_limit=100,
    )), "missing marker rejected")
    passed.append("missing-marker-rejected")

    near = marker[:-2] + "X" + marker[-1]
    need(rejected(lambda: stream_find_marker(
        io.StringIO(near), marker, chunk_size=3, scan_limit=100,
    )), "near marker rejected")
    passed.append("near-marker-rejected")

    need(rejected(lambda: stream_find_marker(
        io.StringIO(marker[:-1]), marker, chunk_size=5, scan_limit=100,
    )), "truncated marker rejected")
    passed.append("truncated-marker-at-EOF-rejected")

    duplicate_stream = io.StringIO(marker + "padding" + marker + array_marker)
    first_tail = stream_find_marker(
        duplicate_stream, marker,
        chunk_size=5, scan_limit=200,
    )
    need(rejected(lambda: stream_find_marker(
        duplicate_stream, array_marker, first_tail,
        chunk_size=5, scan_limit=200,
        forbidden_before_marker=(marker,),
    )), "duplicate table anchor before rows rejected")
    passed.append("duplicate-table-anchor-before-array-rejected")

    need(rejected(lambda: list(iter_array(
        io.StringIO(array_marker + array_marker + '{"a":1}]'), array_marker,
        chunk_size=3, marker_scan_limit=200,
    ))), "duplicate array marker rejected by strict array grammar")
    passed.append("duplicate-array-marker-rejected")

    wrong_table = '"formal_wrong_table":"rows":[]'
    need(rejected(lambda: stream_find_marker(
        io.StringIO(wrong_table), marker, chunk_size=4, scan_limit=200,
    )), "wrong table rejected")
    passed.append("wrong-table-rejected")

    malformed_arrays = (
        ("source-array-leading-comma-rejected", marker + ',{"a":1}]'),
        ("source-array-trailing-comma-rejected", marker + '{"a":1},]'),
        ("source-array-missing-comma-rejected", marker + '{"a":1}{"b":2}]'),
        ("source-array-duplicate-key-rejected", marker + '{"a":1,"a":2}]'),
        ("source-array-float-rejected", marker + '{"a":1.5}]'),
    )
    for label, wire in malformed_arrays:
        need(rejected(lambda wire=wire: list(iter_array(
            io.StringIO(wire), marker,
            chunk_size=3, marker_scan_limit=1_000,
        ))), label)
        passed.append(label)
    need(len(passed) == 14, "exact marker/parser regression count")
    return passed


def contract() -> dict[str, Any]:
    return {
        "schema": SCHEMA + ".independent-verifier-contract.v1",
        "status": (
            "READY_FOR_HEAVY_INDEPENDENT_RECONSTRUCTION_CANDIDATE_ADMISSION_AND_OPTIONAL_PROMOTION"
            if AUDIT_AUTHORIZED else
            "IMPLEMENTED_AUDIT_NOT_AUTHORIZED__HEAVY_SOURCE_CANDIDATE_AND_PROMOTION_HARD_BLOCKED"
        ),
        "implementation_present": True,
        "audit_authorized": AUDIT_AUTHORIZED,
        "hard_gate": {
            "checked_before_any_large_source_lstat_or_open": True,
            "checked_before_candidate_path_lstat_or_open": True,
            "checked_before_reconstruction_spool_or_any_candidate_or_formal_write": True,
            "lightweight_temporary_transaction_fixtures_allowed": True,
            "candidate_admission_enabled": AUDIT_AUTHORIZED,
            "promotion_enabled": AUDIT_AUTHORIZED,
            "lightweight_contract_and_attack_tests_only_when_false": not AUDIT_AUTHORIZED,
        },
        "independence": {
            "producer_filename": PRODUCER,
            "producer_file_sha256": EXPECTED_PRODUCER_SHA256,
            "producer_file_size": EXPECTED_PRODUCER_SIZE,
            "producer_treated_as_inert_bytes_only": True,
            "producer_imported_executed_parsed_or_tokenized": False,
            "all_source_join_reconstruction_implemented_in_this_verifier": True,
            "candidate_opened_only_after_full_independent_reconstruction": True,
        },
        "source_snapshot": {
            "pin_count": len(SOURCE_PINS),
            "every_file_has_literal_sha256_and_size": True,
            "fd_hash_parse_postread_and_name_stability_bound": True,
            "streaming_marker_search": {
                "algorithm": "BOUNDED_ROLLING_OVERLAP_STR_FIND",
                "memory_bound": "chunk_size_plus_longest_marker_minus_one",
                "table_anchor_scan_limit_comes_from_exact_source_size": True,
                "array_marker_scan_limit_comes_from_exact_source_size": True,
                "cross_read_boundary_matches_preserved": True,
                "duplicate_table_anchor_before_rows_rejected": True,
                "missing_near_wrong_and_truncated_markers_rejected": True,
                "source_array_strict_JSON_and_comma_grammar_unchanged": True,
            },
            "pins": {
                name: {"file_sha256": pin[0], "file_size": pin[1]}
                for name, pin in sorted(SOURCE_PINS.items())
            },
        },
        "exact_expected": dict(EXPECTED),
        "independent_join_contract": {
            "R242_R245": {
                "graphs": 264, "sheets": 264, "sides": 528, "incidence": 792,
            },
            "R235_R248_R264": {
                "graphs": 38_328, "sheets": 38_328,
                "pre_correction_sides": 76_656,
                "corrections": {
                    "total": 400, "absent_owner_prunes": 184,
                    "present_phantom_drops": 216,
                },
                "final_sides": 76_256, "incidence": 114_584,
            },
            "R236_R248": {
                "partitions": 16, "graphs": 32, "sheets": 32,
                "distinct_side_members": 48, "side_references": 64,
                "incidence": 96,
            },
            "totals": {
                "graphs": 38_624, "sheets": 38_624, "sides": 76_848,
                "incidence": 115_472, "distinct_B0_members": 115_456,
                "gaps": 154_096,
            },
            "B0_full_scan_and_exact_lineage_backbinding": True,
            "official_key_metadata_only_never_selection_or_routing": True,
        },
        "candidate_contract": {
            "dedicated_private_root": PRIVATE_ROOT.name,
            "exact_seven_files": list(CANDIDATE_ORDER),
            "strict_duplicate_float_nonfinite_BOM_NUL_and_comma_rejection": True,
            "deterministic_single_member_gzip_required": True,
            "result_and_six_ledger_envelopes_exact": True,
            "regular_mode600_nlink1_required": True,
            "private_root_and_candidate_mode700_dirfd_bound": True,
            "directory_file_inode_and_hash_stability_rechecked": True,
            "every_row_byte_equal_to_independent_reconstruction": True,
        },
        "attack_contract": {
            "semantic_contract_unit_mutations": True,
            "strict_wire_unit_mutations": True,
            "real_temporary_filesystem_transaction_paths": True,
            "these_are_not_reconstruction_attacks": True,
            "formal_attack_suite_built_before_verification_marker": True,
        },
        "publication_contract": {
            "promotion_order": list(PROMOTION_ORDER),
            "attack_first": True,
            "verification_last": True,
            "verification_is_sole_package_marker": True,
            "verification_grants_theorem_credit": False,
            "exact_committed_prefix_recovery_only": True,
            "renameat2_noreplace": True,
            "stage_and_deliverables_fsync_after_each_rename": True,
            "precise_owned_marker_rollback": True,
            "downstream_requires_complete_marker_bound_bundle": True,
        },
        "strict_zero_credit_boundary": strict_boundary(),
        "honest_residuals": {
            "SIGKILL_or_power_loss_can_leave_recoverable_prefix_or_stage": True,
            "orphan_stage_auto_reaping_implemented": False,
            "same_UID_namespace_mutation_after_last_check_eliminated": False,
            "source_free_graph_definition_proved": False,
            "physical_incidence_theorem_proved": False,
            "full_support_maximality_fibre_and_global_credit": 0,
        },
    }


def require_heavy_authorization() -> None:
    need(
        AUDIT_AUTHORIZED,
        "candidate/promotion mode blocked before any large source or candidate open and before any write: hostile audit authorization is false",
    )


def self_test() -> dict[str, Any]:
    need(
        EXPECTED["R245_graph_sheet_join_count"] + EXPECTED["R245_graph_side_join_count"]
        == EXPECTED["R245_incidence_count"] == 792,
        "R242/R245 arithmetic",
    )
    need(
        EXPECTED["R248_single_pre_correction_side_count"] - EXPECTED["R264_correction_count"]
        == EXPECTED["R248_single_graph_side_join_count"] == 76_256
        and EXPECTED["R264_invalid_absent_owner_edge_count"]
        + EXPECTED["R264_present_phantom_count"] == EXPECTED["R264_correction_count"],
        "R235/R248/R264 arithmetic",
    )
    need(
        EXPECTED["R236_double_graph_count"] + EXPECTED["R248_double_graph_side_join_count"]
        == EXPECTED["R248_double_incidence_count"] == 96,
        "R236/R248 arithmetic",
    )
    need(
        EXPECTED["R242_graph_count"] + EXPECTED["R235_single_graph_count"]
        + EXPECTED["R236_double_graph_count"] == EXPECTED["graph_count"]
        and EXPECTED["R245_graph_side_join_count"]
        + EXPECTED["R248_single_graph_side_join_count"]
        + EXPECTED["R248_double_graph_side_join_count"]
        == EXPECTED["graph_side_join_count"]
        and EXPECTED["graph_sheet_join_count"] + EXPECTED["graph_side_join_count"]
        == EXPECTED["physical_incidence_count"],
        "global join arithmetic",
    )
    need(
        EXPECTED["graph_definition_gap_count"]
        + EXPECTED["physical_incidence_gap_count"] == EXPECTED["gap_count"],
        "gap arithmetic",
    )
    need(
        HEX64.fullmatch(EXPECTED_PRODUCER_SHA256) is not None
        and EXPECTED_PRODUCER_SIZE == 90_721
        and len(SOURCE_PINS) == 22
        and all(
            HEX64.fullmatch(pin[0]) is not None and pin[1] > 0
            for pin in SOURCE_PINS.values()
        ),
        "pin syntax/count/positive sizes",
    )
    semantic_contract(semantic_baseline())
    marker_regressions = marker_search_regressions()
    comma_boundary_rows = list(iter_array(
        io.StringIO('{"second":2}]'), "@rows@", '@rows@{"first":1},'
    ))
    need(
        comma_boundary_rows == [{"first": 1}, {"second": 2}],
        "source-stream comma exactly at read boundary",
    )
    gate_rejected = rejected(require_heavy_authorization)
    need(gate_rejected is (not AUDIT_AUTHORIZED), "dynamic authorization-gate probe")

    # Only the small inert producer bytes and this running verifier are opened.
    # No sealed source, candidate path, reconstruction spool, or formal path is
    # touched.  The named filesystem attacks use only auto-cleaned temp dirs.
    verifier_fd, verifier_info, verifier_sha256 = runtime_snapshot(VERIFIER, None, None)
    producer_fd, producer_info, producer_sha256 = runtime_snapshot(
        PRODUCER, EXPECTED_PRODUCER_SHA256, EXPECTED_PRODUCER_SIZE
    )
    try:
        attacks = build_attack_suite(None, verifier_sha256)
        attack_payload = dict(attacks)
        claimed = attack_payload.pop("attack_suite_sha256")
        need(claimed == digest(attack_payload), "lightweight attack suite self hash")
        recheck_runtime(verifier_fd, verifier_info, verifier_sha256, VERIFIER)
        recheck_runtime(producer_fd, producer_info, producer_sha256, PRODUCER)
    finally:
        os.close(verifier_fd)
        os.close(producer_fd)
    return {
        "schema": SCHEMA + ".independent-verifier-self-test.v1",
        "status": (
            "PASS_LIGHTWEIGHT_B1G0_CONTRACT_AND_ATTACKS__HEAVY_PATH_AUTHORIZED"
            if AUDIT_AUTHORIZED else
            "PASS_LIGHTWEIGHT_B1G0_CONTRACT_AND_ATTACKS__HEAVY_PATH_HARD_BLOCKED"
        ),
        "producer_file_sha256": producer_sha256,
        "runtime_verifier_file_sha256": verifier_sha256,
        "semantic_attack_count": attacks["semantic_attack_count"],
        "filesystem_attack_count": attacks["filesystem_attack_count"],
        "wire_attack_count": attacks["wire_attack_count"],
        "reconstruction_attack_count": 0,
        "attack_count": attacks["attack_count"],
        "rejected_count": attacks["rejected_count"],
        "all_rejected": True,
        "graph_count_regression": 38_624,
        "physical_incidence_count_regression": 115_472,
        "B0_backbinding_count_regression": 115_456,
        "gap_count_regression": 154_096,
        "sealed_large_source_opened": False,
        "candidate_path_lstat_or_open": False,
        "reconstruction_spool_or_candidate_or_formal_artifact_written": False,
        "lightweight_temporary_transaction_fixtures_written_and_removed": True,
        "authorization_gate_rejected": gate_rejected,
        "source_stream_comma_boundary_regression": True,
        "marker_search_regression_count": len(marker_regressions),
        "marker_search_regressions": marker_regressions,
        "audit_authorized": AUDIT_AUTHORIZED,
        "formal_credit": zero_credit(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--print-contract", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--candidate-dir", type=Path)
    parser.add_argument("--promote", action="store_true")
    arguments = parser.parse_args()
    need(
        sum((
            arguments.print_contract,
            arguments.self_test,
            arguments.candidate_dir is not None,
        )) == 1,
        "choose exactly one explicit verifier mode",
    )
    need(not arguments.promote or arguments.candidate_dir is not None,
         "--promote requires --candidate-dir")
    if arguments.print_contract:
        print(canonical(contract()).decode("ascii"))
        return
    if arguments.self_test:
        print(canonical(self_test()).decode("ascii"))
        return

    # Sole authorization gate for every heavy/actionable path.  Keep this
    # before runtime hashing, source lstat/open, candidate lstat/open, tempfile
    # creation, or publication setup.
    require_heavy_authorization()
    assert arguments.candidate_dir is not None
    producer_runtime = runtime_snapshot(
        PRODUCER, EXPECTED_PRODUCER_SHA256, EXPECTED_PRODUCER_SIZE
    )
    verifier_runtime = runtime_snapshot(VERIFIER, None, None)
    candidate_fd = -1
    ledgers: dict[str, ExpectedLedger] = {}
    try:
        (
            _candidate_path,
            candidate_fd,
            hashes,
            result,
            audit,
            ledgers,
        ) = admit_candidate(
            arguments.candidate_dir, producer_runtime, verifier_runtime
        )
        verifier_sha256 = verifier_runtime[2]
        attacks = build_attack_suite(hashes, verifier_sha256)
        attack_raw = canonical(attacks)
        verification = build_verification(
            hashes, result, audit, attacks, verifier_sha256
        )
        verification_raw = canonical(verification)
        if arguments.promote:
            publish_formal(
                candidate_fd,
                hashes,
                attack_raw,
                verification_raw,
                producer_runtime,
                verifier_runtime,
            )
            print(verification_raw.decode("ascii"))
        else:
            print(canonical({
                "status": "PASS_EXACT_B1G0_PRIVATE_CANDIDATE_ADMISSION__ZERO_FORMAL_THEOREM_CREDIT",
                "candidate_file_sha256s": dict(sorted(hashes.items())),
                "candidate_result_sha256": result["result_sha256"],
                "attack_suite_file_sha256": hashlib.sha256(attack_raw).hexdigest(),
                "verification_file_sha256": hashlib.sha256(verification_raw).hexdigest(),
                "formal_full_support_credit": 0,
                "formal_maximality_credit": 0,
                "formal_fibre_credit": 0,
                "formal_global_disposition_credit": 0,
                "formal_artifact_written": False,
            }).decode("ascii"))
    finally:
        if candidate_fd >= 0:
            os.close(candidate_fd)
        for ledger in ledgers.values():
            ledger.close()
        os.close(producer_runtime[0])
        os.close(verifier_runtime[0])


if __name__ == "__main__":
    main()
