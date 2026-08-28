#!/usr/bin/env python3
"""Round306B1R0: freeze the R288 predicate-source inventory and unions.

This is a private, zero-credit producer.  It implements the exact joins from
the 295,336 new Round288 atoms to 295,340 Round269--Round272 source rows, then
rebinds those atoms to the formal Round294 registry and the sealed Round306B0
member universe.  It deliberately does *not* claim that a source row's outer
box is its full physical support.  That missing source-free interval theorem
is emitted as an explicit gap for every source cell and every member union.

Candidate publication is disabled until a separate hostile audit changes the
single ``AUDIT_AUTHORIZED`` constant.  The disabled branch is checked before
any large input is opened and before the private candidate root is created.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import ctypes
import errno
from fractions import Fraction
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
    """Fail-closed source, join, geometry, or transaction violation."""


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
PRIVATE_ROOT = ROOT / ".cm2-round306b1r0-private-candidates"
PREFIX = "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze"
SCHEMA = "cm2.round306b1r0.source-g-r288-predicate-source-inventory-and-union-freeze.v1"
ENCODER = json.JSONEncoder(
    sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False
)
HEX64 = re.compile(r"^[0-9a-f]{64}$")

FILES = {
    "cell": PREFIX + "_predicate_source_cell.json.gz",
    "member": PREFIX + "_member_union.json.gz",
    "gap": PREFIX + "_gap.json.gz",
    "result": PREFIX + "_result.json",
}
TABLES = {
    "cell": "predicate_source_cell_rows",
    "member": "member_union_rows",
    "gap": "gap_rows",
}
ID_FIELDS = {
    "cell": "Round306B1R0_predicate_source_cell_row_id",
    "member": "Round306B1R0_member_union_row_id",
    "gap": "Round306B1R0_gap_row_id",
}

# Every byte source named below is immutable input to the implemented loader.
INPUT_PINS = {
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json":
        "ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c",
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_verification.json":
        "b008c2208891374696b88506e87957bbb754d95d62677d9406c466405b311f36",
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_manifest.sha256":
        "32dea92dd0de87d3ded6ed69a908b58b01402ddcdef3f0e2b5ffde096a9383c5",
    "cm2_round269_source_g_closed_collar_direct_signature_materialization_certificate.json":
        "472df3ac65c490b79924beaabb382435f5b74ea8ac6c13d71b1d0ab54ffe01d3",
    "cm2_round269_source_g_closed_collar_direct_signature_materialization_verification.json":
        "3435ad2ad0d76f881e7b49fd052fb64035776a991b0f92a542b054f224860982",
    "cm2_round269_source_g_closed_collar_direct_signature_materialization_manifest.sha256":
        "99d8eb8260775b3f2e00bfb51790a6db45a1307753183d61173a2307033c407d",
    "cm2_round270_source_g_outgoing_g_factor_signature_materialization_certificate.json":
        "72a47e53ff601660cb63fe8062403e41a54450fa4a432638faf18a2c76b3efea",
    "cm2_round270_source_g_outgoing_g_factor_signature_materialization_verification.json":
        "6af01780481224f8c9fd690c46886321be4f5b294c33e3f6515cf20dc7cb0513",
    "cm2_round270_source_g_outgoing_g_factor_signature_materialization_manifest.sha256":
        "a23fc6c40b6a29314a9ed7eded86e10242d88a657a321df0c6cfd1b081a8e851",
    "cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_certificate.json":
        "c2a6b66c6fc6ac0b353b36254339a90b91f18c52246c324307ee49569bd7b747",
    "cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_verification.json":
        "26eed04f887f8b6a4ec8fcc88f1112f7382e079d9c53a33dd37a53f7417a29f9",
    "cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_manifest.sha256":
        "6c6b710b3d04c24f962ecb00399ea7d2bccf64650b5e78af36a59c2a754f0697",
    "cm2_round272_source_g_boundary_dual_factor_wall_closure_certificate.json":
        "16050c7087deb546d39b2c7922274ccae7cec24a799ecafd9a8304ae1186d8f2",
    "cm2_round272_source_g_boundary_dual_factor_wall_closure_verification.json":
        "a40f79823dcf07155eec1ecd12cc367dae6b7bdc7a6e8e7cf8680d29d4dade10",
    "cm2_round272_source_g_boundary_dual_factor_wall_closure_manifest.sha256":
        "82124ccbc3fa88fadb1f2a3239634dca332ccc959f7338c44cd27908e4957e5a",
    "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_atom_dispositions.json.gz":
        "6b0a8aa1cd38019322a61f5aaefc936006d10769cd21a5c8df374576f9ac570a",
    "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_result.json":
        "9b5875777f3937efe05a4d871a8c8b76c92ca69d0f636eb014542f59dfe49569",
    "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_verification.json":
        "f08749d2f90ea63a696c482a342489c12e2c86436734a59c6a2e2b79d9cf9b23",
    "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_manifest.sha256":
        "c15e4657051318f1a4e6aadcf80fa679840969c7f2c776e65460ac05cc2eb1eb",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_registry_ledger.json.gz":
        "c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_result.json":
        "dc93ef564ce1aec4aabbc7ff717ac76749b92899e210179a00dba63f2d32d626",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_verification.json":
        "13dcb461f269a8e346c220b85cad0e87a0392b5e2682b7dd70132fd8bd7a1245",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_manifest.sha256":
        "90d5cda0271610bf95a72f94e9bae8e192425580019dd3c823b5a69d20e52131",
    "cm2_round306b0_source_g_r306a_universe_support_source_freeze_member_support_source_index.json.gz":
        "c9a8649c8473bb6a170187e7f803e95748d2ff2198b1b846d97383dd5f0581af",
    "cm2_round306b0_source_g_r306a_universe_support_source_freeze_result.json":
        "badc000c6fadd8807b26a7c3511edc51796c962f150b438956e4c549fd0d5735",
    "cm2_round306b0_source_g_r306a_universe_support_source_freeze_verification.json":
        "f8acc3150d4663d92976a44ab1c3b35c7264f4c4d14808f9133f1184d3f4b590",
    "cm2_round306b0_source_g_r306a_universe_support_source_freeze_manifest.sha256":
        "9846b36d28bb1507b273de3e613a5ecd5ac6515258042bf8b91b89e0c156b269",
}

EXPECTED = {
    "Round288_total_atoms": 332_016,
    "new_members": 295_336,
    "predicate_source_cells": 295_340,
    "multiplicity_one_members": 295_332,
    "multiplicity_two_members": 4,
    "excluded_Round208_members": 36_040,
    "excluded_Round204_members": 640,
    "Round269_cells": 187_128,
    "Round270_cells": 37_712,
    "Round271_cells": 70_356,
    "Round272_cells": 144,
    "W_tail_parent_normalizations": 4,
    "cell_theorem_gaps": 295_340,
    "member_union_theorem_gaps": 295_336,
    "total_gaps": 590_676,
}

IMPLEMENTATION_PRESENT = True
AUDIT_AUTHORIZED = True

NEW_STATES = {
    (
        "NEW_DISJOINT_PROMOTION_READY_CANDIDATE__"
        "ROUND279_STRICT_INWARD_CORRIDOR_INNER_SUPPORT__"
        "PENDING_INDEPENDENT_ROUND288_VERIFIER"
    ),
    (
        "NEW_DISJOINT_CANDIDATE__"
        "POSITIVE_VOLUME_RATIONAL_INNER_SUPPORT_NOT_MATERIALIZED"
    ),
}
R208_STATE = "EXISTING_ROUND208_OCCURRENCE_ID_PRESERVED"
R204_STATE = "EXACT_ALIAS_OF_EXISTING_ROUND204_OCCURRENCE"
SOURCE_TABLES = (
    (269, "cm2_round269_source_g_closed_collar_direct_signature_materialization_certificate.json", "formal_direct_side_signature_ledger"),
    (270, "cm2_round270_source_g_outgoing_g_factor_signature_materialization_certificate.json", "formal_direct_side_signature_ledger"),
    (271, "cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_certificate.json", "formal_side_signature_ledger"),
    (272, "cm2_round272_source_g_boundary_dual_factor_wall_closure_certificate.json", "formal_side_signature_ledger"),
)


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


def open_pinned_fd(name: str) -> tuple[int, os.stat_result]:
    path = DATA / name
    info = os.lstat(path)
    need(path.parent == DATA and stat.S_ISREG(info.st_mode) and not path.is_symlink(), "regular input:" + name)
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    before = os.fstat(descriptor)
    state = hashlib.sha256()
    while True:
        block = os.read(descriptor, 1 << 20)
        if not block:
            break
        state.update(block)
    need(state.hexdigest() == INPUT_PINS[name], "input byte pin:" + name)
    after_hash = os.fstat(descriptor)
    need(
        (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
        == (after_hash.st_dev, after_hash.st_ino, after_hash.st_size, after_hash.st_mtime_ns),
        "stable hash fd:" + name,
    )
    os.lseek(descriptor, 0, os.SEEK_SET)
    return descriptor, before


def verify_all_input_pins() -> None:
    for name in INPUT_PINS:
        descriptor, _ = open_pinned_fd(name)
        os.close(descriptor)


def inode_identity(info: os.stat_result) -> tuple[int, int]:
    return info.st_dev, info.st_ino


def stable_identity(info: os.stat_result) -> tuple[int, int, int, int, int, int, int]:
    return (
        info.st_dev,
        info.st_ino,
        info.st_mode,
        info.st_nlink,
        info.st_size,
        info.st_mtime_ns,
        info.st_ctime_ns,
    )


def hash_descriptor(descriptor: int) -> tuple[str, os.stat_result]:
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
    need(stable_identity(before) == stable_identity(after), "stable hashed descriptor")
    os.lseek(descriptor, 0, os.SEEK_SET)
    return state.hexdigest(), before


def open_verified_running_producer() -> tuple[int, os.stat_result, str]:
    expected = DATA / (PREFIX + ".py")
    need(
        Path(__file__).resolve() == expected.resolve()
        and Path(__file__).absolute() == expected.absolute(),
        "running producer exact canonical path",
    )
    path_info = os.lstat(expected)
    need(
        stat.S_ISREG(path_info.st_mode)
        and not expected.is_symlink()
        and path_info.st_nlink == 1,
        "running producer regular single-link path",
    )
    descriptor = os.open(expected, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        producer_sha256, descriptor_info = hash_descriptor(descriptor)
        need(
            stable_identity(path_info) == stable_identity(descriptor_info),
            "running producer path/fd identity",
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
    observed_sha256, observed_info = hash_descriptor(descriptor)
    need(
        inode_identity(observed_info) == inode_identity(expected_info)
        and observed_sha256 == expected_sha256,
        "running producer fd remains byte-identical",
    )
    path = DATA / (PREFIX + ".py")
    path_info = os.stat(path, follow_symlinks=False)
    need(
        stat.S_ISREG(path_info.st_mode)
        and path_info.st_nlink == 1
        and stable_identity(path_info) == stable_identity(expected_info),
        "running producer path remains fd-bound single-link",
    )


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in result, "duplicate JSON key:" + key)
        result[key] = value
    return result


DECODER = json.JSONDecoder(
    object_pairs_hook=unique_object,
    parse_float=lambda value: (_ for _ in ()).throw(FreezeBlocked("float:" + value)),
    parse_constant=lambda value: (_ for _ in ()).throw(FreezeBlocked("constant:" + value)),
)


def load_pinned_json(name: str, *, compressed: bool = False) -> Any:
    descriptor, before = open_pinned_fd(name)
    raw = os.fdopen(descriptor, "rb", closefd=True)
    stream: BinaryIO = gzip.GzipFile(fileobj=raw, mode="rb") if compressed else raw
    text = io.TextIOWrapper(stream, encoding="utf-8")
    try:
        value = json.load(
            text,
            object_pairs_hook=unique_object,
            parse_float=lambda raw_value: (_ for _ in ()).throw(
                FreezeBlocked("float:" + raw_value)
            ),
            parse_constant=lambda raw_value: (_ for _ in ()).throw(
                FreezeBlocked("constant:" + raw_value)
            ),
        )
        try:
            text.detach()
        except Exception:
            pass
        after = os.fstat(raw.fileno())
        need(
            (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
            == (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns),
            "stable parse fd:" + name,
        )
        return value
    finally:
        if compressed and not stream.closed:
            stream.close()
        if not raw.closed:
            raw.close()


def iter_array(stream: TextIO, marker: str, initial: str = "") -> Iterator[dict[str, Any]]:
    buffer = initial
    while marker not in buffer:
        block = stream.read(1 << 20)
        need(bool(block), "missing array marker:" + marker)
        buffer += block
        if len(buffer) > (1 << 24):
            buffer = buffer[-(1 << 23):]
    buffer = buffer.split(marker, 1)[1]
    comma = False
    while True:
        buffer = buffer.lstrip()
        while not buffer:
            block = stream.read(1 << 20)
            need(bool(block), "truncated streamed array")
            buffer += block
            buffer = buffer.lstrip()
        if buffer[0] == "]":
            return
        if comma:
            need(buffer[0] == ",", "missing streamed comma")
            buffer = buffer[1:].lstrip()
        else:
            need(buffer[0] != ",", "leading streamed comma")
        while True:
            try:
                row, end = DECODER.raw_decode(buffer)
                break
            except json.JSONDecodeError:
                block = stream.read(1 << 20)
                need(bool(block), "truncated streamed row")
                buffer += block
        need(type(row) is dict, "streamed row object")
        yield row
        buffer = buffer[end:]
        comma = True


def stream_rows(
    name: str,
    marker: str,
    *,
    compressed: bool,
    table_anchor: str | None = None,
) -> Iterator[dict[str, Any]]:
    descriptor, before = open_pinned_fd(name)
    raw = os.fdopen(descriptor, "rb", closefd=True)
    binary: BinaryIO = gzip.GzipFile(fileobj=raw, mode="rb") if compressed else raw
    text = io.TextIOWrapper(binary, encoding="utf-8", newline="")
    try:
        initial = ""
        if table_anchor is not None:
            while table_anchor not in initial:
                block = text.read(1 << 20)
                need(bool(block), "missing table anchor:" + table_anchor)
                initial += block
                if len(initial) > (1 << 24):
                    initial = initial[-(1 << 23):]
            initial = initial.split(table_anchor, 1)[1]
        yield from iter_array(text, marker, initial)
        after = os.fstat(raw.fileno())
        need(
            (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
            == (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns),
            "stable streamed fd:" + name,
        )
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
        self.rows = ListHash()
        self.ids = ListHash()
        self.hashes = ListHash()
        self.seen: set[str] = set()

    def add(self, payload: dict[str, Any]) -> dict[str, Any]:
        row = close_row(payload)
        row_id = row.get(self.id_field)
        need(type(row_id) is str and row_id not in self.seen, "unique spool row id")
        self.seen.add(row_id)
        if self.rows.count:
            self.stream.write(b",")
        self.stream.write(canonical(row))
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

    def close(self) -> None:
        self.stream.close()


def source_round(source_id: str) -> int:
    match = re.match(r"^round(269|270|271|272)-", source_id)
    need(match is not None, "known R288 source row prefix:" + source_id)
    return int(match.group(1))


def positive_box(box: Any, label: str) -> tuple[Fraction, ...]:
    need(type(box) is list and len(box) == 6, label + ":box arity")
    values = tuple(Fraction(item) for item in box)
    need(all(values[2 * axis] < values[2 * axis + 1] for axis in range(3)), label + ":positive")
    return values


def box_text(box: tuple[Fraction, ...]) -> list[str]:
    return [str(item) for item in box]


def merge_boxes(boxes: list[list[str]]) -> list[list[str]]:
    work = sorted(set(positive_box(box, "merge") for box in boxes))
    changed = True
    while changed:
        changed = False
        for left_index, left in enumerate(work):
            for right_index in range(left_index + 1, len(work)):
                right = work[right_index]
                for axis in range(3):
                    if any(
                        left[2 * other:2 * other + 2] != right[2 * other:2 * other + 2]
                        for other in range(3) if other != axis
                    ):
                        continue
                    if left[2 * axis + 1] == right[2 * axis]:
                        merged = list(left)
                        merged[2 * axis + 1] = right[2 * axis + 1]
                    elif right[2 * axis + 1] == left[2 * axis]:
                        merged = list(right)
                        merged[2 * axis + 1] = left[2 * axis + 1]
                    else:
                        continue
                    work = [item for index, item in enumerate(work) if index not in (left_index, right_index)]
                    work.append(tuple(merged))
                    work.sort()
                    changed = True
                    break
                if changed:
                    break
            if changed:
                break
    return [box_text(box) for box in work]


def w_tail_parent_normalization(
    atom_id: str,
    outer_envelopes: list[list[str]],
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    need(len(rows) == 2, "W-tail alias multiplicity:" + atom_id)
    need({row.get("t_child") for row in rows} == {0, 1}, "W-tail child pair:" + atom_id)
    ordered = sorted(rows, key=lambda row: row["t_child"])
    lower = positive_box(ordered[0]["t_child_box"], "W-tail lower")
    upper = positive_box(ordered[1]["t_child_box"], "W-tail upper")
    need(lower[1] == upper[0] and lower[2:] == upper[2:], "W-tail artificial t interface")
    normalized = merge_boxes([ordered[0]["t_child_box"], ordered[1]["t_child_box"]])
    need(normalized == outer_envelopes, "W-tail parent envelope equality:" + atom_id)
    return {
        "normalization_kind": "ROUND271_ARTIFICIAL_T_BISECTION_PARENT_NORMALIZATION",
        "artificial_interface": {"axis": "t", "value": str(lower[1])},
        "interface_is_not_a_physical_support_boundary": True,
        "normalized_parent_box": normalized[0],
        "source_children": [row["signed_region_row_id"] for row in ordered],
        "full_support_credit": 0,
    }


def unpack_round182() -> dict[str, dict[str, Any]]:
    document = load_pinned_json("cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json")
    result = document["result"]
    need(document.get("result_sha256") == digest(result), "Round182 result digest")
    table = "collar_leaf_rows"
    rows = result[table]
    columns = result["row_column_schemas"][table]
    census = result["table_census_and_sha256"][table]
    need(len(rows) == census["row_count"] and digest(rows) == census["rows_sha256"], "Round182 leaf table")
    leaves = {row[columns.index("row_id")]: dict(zip(columns, row, strict=True)) for row in rows}
    need(len(leaves) == len(rows), "unique Round182 leaves")
    return leaves


def source_descriptor(round_number: int, row: dict[str, Any]) -> dict[str, Any]:
    signature = row["local_return_signature"]
    need(row["complete_10_field_return_signature_sha256"] == digest(signature), "source signature digest")
    if round_number in {269, 270}:
        return {
            "predicate_family": "OUTGOING_EXACT_HPLUS_HMINUS_SIGN_CELL",
            "HPLUS_sign": row["HPLUS_sign"],
            "HMINUS_sign": row["HMINUS_sign"],
            "region_factor_sign": row["region_factor_sign"],
        }
    if row.get("collar_kind") == "WALL":
        return {
            "predicate_family": "WALL_SOURCE_FACTOR_TIMES_HIT_FACTOR_SIGN_CELL",
            "reason_label": row["reason_label"],
            "equation": row["equation"],
            "region_product_sign": row["region_product_sign"],
            "witness_source_factor_sign": row["witness_source_factor_sign"],
            "witness_target_factor_sign": row["witness_target_factor_sign"],
        }
    if row["signed_region_row_id"].startswith("round271-W-tail-side:"):
        return {
            "predicate_family": "OUTGOING_W_TAIL_CHILD_FACTOR_CELL",
            "region_product_sign": row["region_product_sign"],
            "t_child": row["t_child"],
        }
    return {
        "predicate_family": "OUTGOING_G_ONE_SIDED_INTERIOR_CELL",
        "excluded_transition_face": row["excluded_transition_face"],
        "one_sided_extension": row["one_sided_extension"],
    }


def build_inventory() -> tuple[dict[str, RowSpool], dict[str, Any]]:
    spools = {kind: RowSpool(kind) for kind in ("cell", "member", "gap")}

    atoms: dict[str, dict[str, Any]] = {}
    source_to_atom: dict[str, str] = {}
    excluded_204: set[str] = set()
    excluded_208: set[str] = set()
    multiplicity = Counter()
    new_round_histogram = Counter()
    disposition_count = 0
    r288_name = "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_atom_dispositions.json.gz"
    for row in stream_rows(r288_name, '"rows":[', compressed=True):
        check_row(row, "Round288 atom")
        disposition_count += 1
        state = row["occurrence_identity_disposition"]
        source_ids = row["source_signature_row_ids"]
        need(source_ids == sorted(source_ids) and len(source_ids) in {1, 2}, "Round288 source list")
        if state in NEW_STATES:
            atom_id = row["canonical_atom_id"]
            need(atom_id not in atoms, "unique new atom")
            atoms[atom_id] = row
            multiplicity[len(source_ids)] += 1
            for source_id in source_ids:
                need(source_id not in source_to_atom, "source belongs to one new atom")
                source_to_atom[source_id] = atom_id
                new_round_histogram[source_round(source_id)] += 1
        elif state == R208_STATE:
            need(
                len(source_ids) == 1
                and source_ids[0] not in excluded_208
                and source_ids[0] not in excluded_204,
                "unique singleton Round208 exclusion source",
            )
            excluded_208.add(source_ids[0])
        elif state == R204_STATE:
            need(
                len(source_ids) == 1
                and source_ids[0] not in excluded_204
                and source_ids[0] not in excluded_208,
                "unique singleton Round204 exclusion source",
            )
            excluded_204.add(source_ids[0])
        else:
            raise FreezeBlocked("unknown Round288 disposition:" + state)
    need(disposition_count == EXPECTED["Round288_total_atoms"], "Round288 atom census")
    need(len(atoms) == EXPECTED["new_members"] and len(source_to_atom) == EXPECTED["predicate_source_cells"], "new atom/source census")
    need(multiplicity == {1: EXPECTED["multiplicity_one_members"], 2: EXPECTED["multiplicity_two_members"]}, "source multiplicity")
    need(len(excluded_208) == EXPECTED["excluded_Round208_members"] and len(excluded_204) == EXPECTED["excluded_Round204_members"], "existing exclusion census")
    need(
        len(source_to_atom) + len(excluded_208) + len(excluded_204)
        == EXPECTED["Round288_total_atoms"] + EXPECTED["multiplicity_two_members"],
        "all 332020 source rows partition exactly",
    )
    need(new_round_histogram == {269: 187_128, 270: 37_712, 271: 70_356, 272: 144}, "source round census")
    need(not (set(source_to_atom) & excluded_204) and not (set(source_to_atom) & excluded_208), "new/existing disjoint")

    registry_by_atom: dict[str, dict[str, Any]] = {}
    r294_name = "cm2_round294_source_g_occurrence_registry_atomic_promotion_registry_ledger.json.gz"
    for row in stream_rows(r294_name, '"rows":[', compressed=True):
        check_row(row, "Round294 registry")
        if row["registry_entry_kind"] != "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM":
            continue
        atom_id = row["canonical_atom_id"]
        need(atom_id in atoms and atom_id not in registry_by_atom, "Round294 atom join")
        atom = atoms[atom_id]
        need(
            row["registry_occurrence_id"] == atom["reserved_candidate_occurrence_id__not_issued"]
            and row["source_signature_row_ids"] == atom["source_signature_row_ids"]
            and row["source_row_id"] == atom["Round288_atom_disposition_row_id"]
            and row["source_row_sha256"] == atom["row_sha256"],
            "Round294 exact R288 rebinding",
        )
        registry_by_atom[atom_id] = row
    need(set(registry_by_atom) == set(atoms), "Round294 complete new atom set")

    b0_by_member: dict[str, dict[str, Any]] = {}
    b0_name = "cm2_round306b0_source_g_r306a_universe_support_source_freeze_member_support_source_index.json.gz"
    for row in stream_rows(b0_name, '"member_support_source_rows":[', compressed=True):
        check_row(row, "Round306B0 member")
        if row["identity_tranche"] != "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM":
            continue
        member_id = row["member_id"]
        need(member_id not in b0_by_member, "unique B0 R288 member")
        b0_by_member[member_id] = row
    registry_member_ids = {row["registry_occurrence_id"] for row in registry_by_atom.values()}
    need(set(b0_by_member) == registry_member_ids and len(b0_by_member) == EXPECTED["new_members"], "Round294/B0 member set equality")
    for atom_id, registry in registry_by_atom.items():
        atom = atoms[atom_id]
        b0 = b0_by_member[registry["registry_occurrence_id"]]
        need(
            b0["identity_class"] == "FORMAL_OCCURRENCE"
            and b0["pair_denominator_class"] == "OCCURRENCE"
            and b0["primary_source_package"] == "R294"
            and b0["primary_source_row_id"]
            == registry["Round294_occurrence_registry_row_id"]
            and b0["primary_source_row_sha256"] == registry["row_sha256"]
            and b0["official_key_id"]
            == registry["official_key_id"]
            == atom["official_key_id"],
            "Round306B0/Round294/Round288 row-exact member rebinding",
        )

    leaves = unpack_round182()
    source_rows: dict[str, dict[str, Any]] = {}
    source_round_counts = Counter()
    excluded_204_seen: set[str] = set()
    cell_boxes: dict[str, list[list[str]]] = defaultdict(list)
    cell_ids_by_atom: dict[str, list[str]] = defaultdict(list)
    # Exact nested-table parsing uses the pinned documents.  Keeping it after
    # all set joins makes source admission independent of official keys.
    for round_number, name, table in SOURCE_TABLES:
        total_source_rows = 0
        for row in stream_rows(
            name,
            '"rows":[',
            compressed=False,
            table_anchor='"' + table + '":{',
        ):
            total_source_rows += 1
            check_row(row, "source row")
            source_id = row["signed_region_row_id"]
            if source_id not in source_to_atom:
                need(source_id in excluded_204 and round_number in {271, 272}, "only Round204 rows excluded from R269-R272")
                excluded_204_seen.add(source_id)
                continue
            need(source_round(source_id) == round_number and source_id not in source_rows, "source round and uniqueness")
            atom_id = source_to_atom[source_id]
            atom = atoms[atom_id]
            need(
                row["Round182_leaf_row_id"] == atom["Round182_leaf_row_id"]
                and row["complete_10_field_return_signature_sha256"] == atom["complete_10_field_return_signature_sha256"]
                and row["local_return_signature"]["source_chart"] == atom["source_chart"]
                and row["local_return_signature"]["target_lift"] == atom["owner_target"],
                "source/atom exact geometry metadata join",
            )
            leaf = leaves[row["Round182_leaf_row_id"]]
            box = row.get("t_child_box", leaf["box"])
            positive_box(box, "source cell")
            descriptor = source_descriptor(round_number, row)
            cell_id = "round306b1r0-predicate-source-cell:" + digest([source_id, atom_id, box, descriptor])
            cell = spools["cell"].add({
                "schema": SCHEMA + ".predicate-source-cell-row.v1",
                "Round306B1R0_predicate_source_cell_row_id": cell_id,
                "member_canonical_atom_id": atom_id,
                "formal_member_id": registry_by_atom[atom_id]["registry_occurrence_id"],
                "source_round": round_number,
                "source_filename": name,
                "source_file_sha256": INPUT_PINS[name],
                "source_table": table,
                "source_signature_row_id": source_id,
                "source_signature_row_sha256": row["row_sha256"],
                "Round182_leaf_row_id": row["Round182_leaf_row_id"],
                "outer_carrier_box": box,
                "predicate_source_inventory": descriptor,
                "official_key_metadata_only": {
                    "official_key_id": row["local_return_signature"]["official_key_id"],
                    "official_key_ordinal": row["local_return_signature"]["official_key_ordinal"],
                    "complete_10_field_return_signature_sha256": row["complete_10_field_return_signature_sha256"],
                },
                "official_key_used_as_join_or_routing_filter": False,
                "source_free_interval_predicate_ast_materialized": False,
                "outer_carrier_box_claimed_as_full_support": False,
                "formal_full_support_credit": 0,
                "formal_maximality_credit": 0,
                "formal_fibre_credit": 0,
                "formal_global_disposition_credit": 0,
            })
            spools["gap"].add({
                "schema": SCHEMA + ".gap-row.v1",
                "Round306B1R0_gap_row_id": "round306b1r0-gap:cell:" + digest(source_id),
                "gap_kind": "SOURCE_FREE_INTERVAL_PREDICATE_EQUIVALENCE_NOT_YET_PROVED",
                "predicate_source_cell_row_id": cell_id,
                "member_id": cell["formal_member_id"],
                "source_signature_row_id": source_id,
                "required_closure": "independently derive and interval-verify the exact source-free predicate on the whole cell",
                "formal_credit": 0,
            })
            source_rows[source_id] = row
            source_round_counts[round_number] += 1
            cell_boxes[atom_id].append(box)
            cell_ids_by_atom[atom_id].append(cell_id)
        need(
            total_source_rows
            == {269: 187_128, 270: 37_712, 271: 70_420, 272: 720}[round_number],
            "complete source ledger row count",
        )
    need(set(source_rows) == set(source_to_atom), "complete source row set equality")
    need(excluded_204_seen == excluded_204, "all and only Round204 aliases excluded")
    need(source_round_counts == new_round_histogram, "source reconstruction histogram")

    w_tail_normalizations = 0
    for atom_id in sorted(atoms):
        atom = atoms[atom_id]
        registry = registry_by_atom[atom_id]
        member_id = registry["registry_occurrence_id"]
        b0 = b0_by_member[member_id]
        source_ids = atom["source_signature_row_ids"]
        need(cell_ids_by_atom[atom_id] == [
            "round306b1r0-predicate-source-cell:" + digest([
                source_id,
                atom_id,
                source_rows[source_id].get("t_child_box", leaves[source_rows[source_id]["Round182_leaf_row_id"]]["box"]),
                source_descriptor(source_round(source_id), source_rows[source_id]),
            ]) for source_id in source_ids
        ], "member source/cell order")
        normalized_boxes = merge_boxes(cell_boxes[atom_id])
        need(normalized_boxes == atom["frozen_positive_rational_support_envelopes"], "source outer-envelope union:" + atom_id)
        normalization = None
        if len(source_ids) == 2:
            rows = [source_rows[source_id] for source_id in source_ids]
            need(all(source_id.startswith("round271-W-tail-side:") for source_id in source_ids), "only W-tail multiplicity two")
            normalization = w_tail_parent_normalization(
                atom_id, atom["frozen_positive_rational_support_envelopes"], rows
            )
            w_tail_normalizations += 1
        union_id = "round306b1r0-member-union:" + digest([member_id, source_ids, cell_ids_by_atom[atom_id]])
        spools["member"].add({
            "schema": SCHEMA + ".member-union-row.v1",
            "Round306B1R0_member_union_row_id": union_id,
            "member_id": member_id,
            "canonical_atom_id": atom_id,
            "Round306A_component_id": b0["Round306A_component_id"],
            "Round294_registry_row_id": registry["Round294_occurrence_registry_row_id"],
            "Round306B0_member_source_row_id": b0["Round306B0_member_support_source_row_id"],
            "source_signature_row_ids": source_ids,
            "predicate_source_cell_row_ids": cell_ids_by_atom[atom_id],
            "predicate_source_cell_multiplicity": len(source_ids),
            "outer_envelope_union_structurally_exact": True,
            "normalized_outer_envelopes": normalized_boxes,
            "Round271_W_tail_parent_normalization": normalization,
            "official_key_metadata_only": atom["official_key_id"],
            "official_key_used_as_join_or_routing_filter": False,
            "full_support_union_theorem_status": "PENDING_SOURCE_FREE_INTERVAL_PREDICATE_EQUIVALENCE",
            "formal_full_support_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
        })
        spools["gap"].add({
            "schema": SCHEMA + ".gap-row.v1",
            "Round306B1R0_gap_row_id": "round306b1r0-gap:member:" + digest(member_id),
            "gap_kind": "MEMBER_FULL_SUPPORT_UNION_THEOREM_PENDING",
            "member_union_row_id": union_id,
            "member_id": member_id,
            "source_cell_count": len(source_ids),
            "required_closure": "prove the exact source-free cell predicates cover the member support with no missing physical locus",
            "formal_credit": 0,
        })
    need(w_tail_normalizations == EXPECTED["W_tail_parent_normalizations"], "W-tail normalization census")
    need(spools["cell"].rows.count == EXPECTED["predicate_source_cells"], "cell spool count")
    need(spools["member"].rows.count == EXPECTED["new_members"], "member spool count")
    need(spools["gap"].rows.count == EXPECTED["total_gaps"], "gap spool count")

    audit = {
        "Round288_new_atom_count": len(atoms),
        "predicate_source_cell_count": len(source_rows),
        "source_round_histogram": {str(key): value for key, value in sorted(source_round_counts.items())},
        "source_multiplicity_histogram": {str(key): value for key, value in sorted(multiplicity.items())},
        "excluded_Round208_existing_atom_count": len(excluded_208),
        "excluded_Round204_existing_atom_count": len(excluded_204),
        "Round294_member_set_equals_Round306B0_member_set": True,
        "Round271_W_tail_parent_normalization_count": w_tail_normalizations,
        "outer_envelope_union_exact_for_every_member": True,
        "source_free_interval_predicate_theorem_complete": False,
        "full_support_union_theorem_complete": False,
    }
    return spools, audit


def contract() -> dict[str, Any]:
    return {
        "schema": SCHEMA + ".contract.v1",
        "status": (
            "IMPLEMENTED_AND_AUDIT_AUTHORIZED__PRIVATE_ZERO_CREDIT_CANDIDATE_MODE_ENABLED"
            if AUDIT_AUTHORIZED
            else "IMPLEMENTED_NOT_AUDIT_AUTHORIZED__CANDIDATE_HARD_BLOCKED_ZERO_CREDIT"
        ),
        "implementation_present": IMPLEMENTATION_PRESENT,
        "audit_authorized": AUDIT_AUTHORIZED,
        "candidate_authorization_gate_occurs_before_large_input_open": True,
        "candidate_authorization_gate_occurs_before_any_write": True,
        "candidate_mode_enabled": AUDIT_AUTHORIZED,
        "candidate_transaction_hardening_implemented": True,
        "candidate_transaction_hardening_required_before_authorization": False,
        "transaction_contract": {
            "running_script_path_and_fd_bytes_bound": True,
            "all_candidate_writes_are_stage_dirfd_bound": True,
            "every_output_requires_regular_mode600_nlink1": True,
            "every_output_inode_and_sha256_rechecked_before_publish": True,
            "stage_name_inode_checked_before_publish": True,
            "candidate_name_inode_checked_after_publish": True,
            "failed_transaction_cleanup_is_exact_inode_scoped": True,
            "private_root_and_stage_directory_fsync_required": True,
            "SIGKILL_or_power_loss_orphan_recovery_implemented": False,
            "same_uid_namespace_mutation_after_final_check_eliminated": False,
            "independent_verifier_still_required": True,
        },
        "exact_expected": dict(EXPECTED),
        "input_file_pins": dict(sorted(INPUT_PINS.items())),
        "implemented_joins": [
            "Round288 dispositions to exact Round269/Round270/Round271/Round272 source rows",
            "exclude exactly 36040 Round208 and 640 Round204 existing atoms",
            "Round288 atoms to formal Round294 member IDs",
            "Round294 member set equality with sealed Round306B0 tranche",
            "295340 source cells grouped into 295336 member unions",
            "four Round271 W-tail artificial t-bisection parent normalizations",
        ],
        "strict_boundary": {
            "outer_envelope_union_inventory_frozen": True,
            "source_free_interval_predicate_theorem_complete": False,
            "member_full_support_union_theorem_complete": False,
            "cell_gap_count": EXPECTED["cell_theorem_gaps"],
            "member_gap_count": EXPECTED["member_union_theorem_gaps"],
            "official_key_is_metadata_only": True,
            "formal_full_support_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "candidate_files": list(FILES.values()),
        "private_candidate_root": PRIVATE_ROOT.name,
    }


def self_test() -> dict[str, Any]:
    need(IMPLEMENTATION_PRESENT, "implementation present")
    need(sum(EXPECTED[f"Round{number}_cells"] for number in (269, 270, 271, 272)) == EXPECTED["predicate_source_cells"], "round sum")
    need(EXPECTED["multiplicity_one_members"] + EXPECTED["multiplicity_two_members"] == EXPECTED["new_members"], "member multiplicity sum")
    need(EXPECTED["multiplicity_one_members"] + 2 * EXPECTED["multiplicity_two_members"] == EXPECTED["predicate_source_cells"], "cell multiplicity sum")
    need(EXPECTED["cell_theorem_gaps"] + EXPECTED["member_union_theorem_gaps"] == EXPECTED["total_gaps"], "gap sum")
    need(all(HEX64.fullmatch(value) for value in INPUT_PINS.values()), "pin syntax")
    lower = {"signed_region_row_id": "round271-W-tail-side:a", "t_child": 0, "t_child_box": ["0", "1", "0", "1", "0", "1"]}
    upper = {"signed_region_row_id": "round271-W-tail-side:b", "t_child": 1, "t_child_box": ["1", "2", "0", "1", "0", "1"]}
    normalized = w_tail_parent_normalization("synthetic", [["0", "2", "0", "1", "0", "1"]], [upper, lower])
    need(normalized["artificial_interface"]["value"] == "1", "synthetic W-tail interface")
    probe = contract()
    need(
        probe["strict_boundary"]["formal_maximality_credit"] == 0
        and probe["strict_boundary"]["official_key_is_metadata_only"]
        and probe["candidate_transaction_hardening_implemented"] is True
        and probe["candidate_transaction_hardening_required_before_authorization"] is False,
        "zero credit and transaction contract",
    )
    return {
        "schema": SCHEMA + ".self-test.v1",
        "status": (
            "PASS_LIGHTWEIGHT_ROUND306B1R0_CONTRACT_AND_NORMALIZATION_SELF_TEST__CANDIDATE_AUTHORIZED"
            if AUDIT_AUTHORIZED
            else "PASS_LIGHTWEIGHT_ROUND306B1R0_CONTRACT_AND_NORMALIZATION_SELF_TEST__CANDIDATE_BLOCKED"
        ),
        "tests_passed": 13,
        "large_input_opened": False,
        "candidate_written": False,
        "implementation_present": True,
        "audit_authorized": AUDIT_AUTHORIZED,
        "formal_maximality_credit": 0,
    }


def ledger_envelope(kind: str, spool: RowSpool) -> dict[str, Any]:
    payload = {
        "schema": SCHEMA + "." + kind + "-ledger.v1",
        "status": "PRIVATE_ZERO_CREDIT_SOURCE_INVENTORY_CANDIDATE",
        **spool.metadata(),
        "formal_credit": {"full_support": 0, "maximality": 0, "fibre": 0, "global_disposition": 0},
    }
    return {**payload, "ledger_sha256": digest(payload)}


def checked_output_info(descriptor: int, label: str) -> os.stat_result:
    info = os.fstat(descriptor)
    need(
        stat.S_ISREG(info.st_mode)
        and stat.S_IMODE(info.st_mode) == 0o600
        and info.st_nlink == 1,
        "private output regular mode600 nlink1:" + label,
    )
    return info


def register_created_file(
    created: dict[str, dict[str, Any]],
    name: str,
    descriptor: int,
) -> dict[str, Any]:
    # Filename admission must have happened before O_EXCL creation.  Once the
    # inode exists, register it before any fallible mode/link admission so the
    # outer exact cleanup can always identify this transaction's object.
    need(name in FILES.values() and name not in created, "pre-admitted unique candidate filename")
    info = os.fstat(descriptor)
    record = {
        "filename": name,
        "device": info.st_dev,
        "inode": info.st_ino,
        "file_sha256": None,
    }
    created[name] = record
    checked_output_info(descriptor, name)
    return record


def preflight_output_name(created: dict[str, dict[str, Any]], name: str) -> None:
    need(name in FILES.values() and name not in created, "expected unique candidate filename")


def validate_created_file(stage_fd: int, record: dict[str, Any]) -> os.stat_result:
    name = record["filename"]
    descriptor = os.open(
        name,
        os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0),
        dir_fd=stage_fd,
    )
    try:
        info = checked_output_info(descriptor, name)
        need(
            inode_identity(info) == (record["device"], record["inode"]),
            "candidate file inode remains bound:" + name,
        )
        observed_sha256, after = hash_descriptor(descriptor)
        named_after = os.stat(name, dir_fd=stage_fd, follow_symlinks=False)
        need(
            inode_identity(after) == (record["device"], record["inode"])
            and inode_identity(named_after) == (record["device"], record["inode"])
            and stat.S_ISREG(named_after.st_mode)
            and stat.S_IMODE(named_after.st_mode) == 0o600
            and named_after.st_nlink == 1
            and observed_sha256 == record["file_sha256"],
            "candidate file bytes and post-hash filename remain fd-bound:" + name,
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
    preflight_output_name(created, name)
    descriptor = os.open(
        name,
        os.O_WRONLY
        | os.O_CREAT
        | os.O_EXCL
        | getattr(os, "O_NOFOLLOW", 0),
        0o600,
        dir_fd=stage_fd,
    )
    raw: BinaryIO | None = None
    state = hashlib.sha256()

    class Sink:
        def write(self, block: bytes) -> int:
            state.update(block)
            need(raw is not None, "ledger raw output initialized")
            return raw.write(block)

        def flush(self) -> None:
            need(raw is not None, "ledger raw output initialized")
            raw.flush()

    prefix = canonical(envelope)[:-1] + b',"' + TABLES[kind].encode("ascii") + b'":['
    try:
        record = register_created_file(created, name, descriptor)
        raw = os.fdopen(descriptor, "wb", closefd=True)
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
        if raw is None:
            os.close(descriptor)
        else:
            raw.close()
    record["file_sha256"] = state.hexdigest()
    validate_created_file(stage_fd, record)
    return {
        "filename": name,
        "file_sha256": record["file_sha256"],
        **spool.metadata(),
        "ledger_sha256": envelope["ledger_sha256"],
    }


def exclusive_bytes(
    stage_fd: int,
    name: str,
    payload: bytes,
    created: dict[str, dict[str, Any]],
) -> str:
    preflight_output_name(created, name)
    descriptor = os.open(
        name,
        os.O_WRONLY
        | os.O_CREAT
        | os.O_EXCL
        | getattr(os, "O_NOFOLLOW", 0),
        0o600,
        dir_fd=stage_fd,
    )
    try:
        record = register_created_file(created, name, descriptor)
        offset = 0
        while offset < len(payload):
            written = os.write(descriptor, payload[offset:])
            need(written > 0, "candidate output write progress:" + name)
            offset += written
        os.fsync(descriptor)
        checked_output_info(descriptor, name)
    finally:
        os.close(descriptor)
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


def create_stage(
    candidate: Path,
    *,
    _self_test_fail_after_mkdir: bool = False,
) -> tuple[str, str, int, int, tuple[int, int]]:
    if not os.path.lexists(PRIVATE_ROOT):
        parent_fd = os.open(
            ROOT,
            os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0),
        )
        try:
            os.mkdir(PRIVATE_ROOT.name, 0o700, dir_fd=parent_fd)
            os.fsync(parent_fd)
        finally:
            os.close(parent_fd)
    info = os.lstat(PRIVATE_ROOT)
    need(stat.S_ISDIR(info.st_mode) and not PRIVATE_ROOT.is_symlink() and stat.S_IMODE(info.st_mode) == 0o700, "private root")
    target = Path(os.path.abspath(os.fspath(candidate)))
    need(target.parent == PRIVATE_ROOT and target.name not in {"", ".", ".."}, "direct private child")
    need(not os.path.lexists(target), "candidate target absent")
    root_fd = os.open(PRIVATE_ROOT, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0))
    stage_fd = -1
    created_stage_identity: tuple[int, int] | None = None
    try:
        root_info = os.fstat(root_fd)
        need(inode_identity(root_info) == inode_identity(info), "private root path/fd identity")
        stage_name = "." + target.name + ".stage." + digest(
            [os.getpid(), target.name, os.urandom(32).hex()]
        )[:24]
        os.mkdir(stage_name, 0o700, dir_fd=root_fd)
        created_stage_info = os.stat(stage_name, dir_fd=root_fd, follow_symlinks=False)
        # Register the created inode immediately after the first successful
        # identity observation, before mode admission or any other fallible
        # post-mkdir check.
        created_stage_identity = inode_identity(created_stage_info)
        if _self_test_fail_after_mkdir:
            raise FreezeBlocked("injected post-mkdir admission failure")
        need(
            stat.S_ISDIR(created_stage_info.st_mode)
            and stat.S_IMODE(created_stage_info.st_mode) == 0o700,
            "created stage mode700 directory",
        )
        os.fsync(root_fd)
        stage_fd = os.open(
            stage_name,
            os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0),
            dir_fd=root_fd,
        )
        stage_info = assert_directory_name_bound(root_fd, stage_name, stage_fd, "new stage")
        need(
            inode_identity(stage_info) == created_stage_identity
            and not os.listdir(stage_fd),
            "opened stage is exact empty created inode",
        )
        return stage_name, target.name, root_fd, stage_fd, inode_identity(stage_info)
    except Exception:
        if stage_fd >= 0:
            os.close(stage_fd)
        if created_stage_identity is not None:
            for name in list(os.listdir(root_fd)):
                try:
                    candidate_info = os.stat(
                        name,
                        dir_fd=root_fd,
                        follow_symlinks=False,
                    )
                except FileNotFoundError:
                    continue
                if (
                    stat.S_ISDIR(candidate_info.st_mode)
                    and inode_identity(candidate_info) == created_stage_identity
                ):
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
    tracked = {
        (record["device"], record["inode"])
        for record in created.values()
    }
    for name in list(os.listdir(stage_fd)):
        try:
            info = os.stat(name, dir_fd=stage_fd, follow_symlinks=False)
        except FileNotFoundError:
            continue
        if inode_identity(info) in tracked and stat.S_ISREG(info.st_mode):
            os.unlink(name, dir_fd=stage_fd)
    os.fsync(stage_fd)
    for name in list(os.listdir(root_fd)):
        try:
            info = os.stat(name, dir_fd=root_fd, follow_symlinks=False)
        except FileNotFoundError:
            continue
        if inode_identity(info) != directory_identity or not stat.S_ISDIR(info.st_mode):
            continue
        try:
            os.rmdir(name, dir_fd=root_fd)
        except OSError as error:
            if error.errno not in {errno.ENOTEMPTY, errno.EEXIST}:
                raise
    os.fsync(root_fd)


def transaction_self_test() -> dict[str, Any]:
    global PRIVATE_ROOT

    original_private_root = PRIVATE_ROOT
    checks: list[str] = []
    producer_fd, producer_info, producer_sha256 = open_verified_running_producer()
    try:
        recheck_running_producer(producer_fd, producer_info, producer_sha256)
        checks.append("running-producer-path-fd-bytes-bound")
    finally:
        os.close(producer_fd)
    with tempfile.TemporaryDirectory(
        prefix=".round306b1r0-transaction-self-test.",
        dir=ROOT,
    ) as temporary_name:
        PRIVATE_ROOT = Path(temporary_name)
        try:
            # Normal dirfd-bound write, strict census, publish, post-publish
            # inode binding, and exact cleanup.
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
                extra_fd = os.open(
                    "unexpected",
                    os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
                    0o600,
                    dir_fd=stage_fd,
                )
                os.close(extra_fd)
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
                checks.append("normal-publish-inode-bound")
                cleanup_exact_transaction(
                    root_fd,
                    stage_fd,
                    directory_identity,
                    created,
                )
                need(not os.path.lexists(candidate), "normal self-test exact cleanup")
                checks.append("published-exact-cleanup-passed")
            finally:
                os.close(stage_fd)
                os.close(root_fd)

            # A filename rejected by preflight must fail before O_EXCL creates
            # any inode.  This covers the pre-registration admission boundary.
            candidate = PRIVATE_ROOT / "pre-registration-candidate"
            stage_name, _target_name, root_fd, stage_fd, directory_identity = create_stage(candidate)
            victim = next(iter(FILES.values()))
            try:
                synthetic_created = {
                    victim: {
                        "filename": victim,
                        "device": -1,
                        "inode": -1,
                        "file_sha256": None,
                    }
                }
                try:
                    exclusive_bytes(stage_fd, victim, b"must-not-exist", synthetic_created)
                except FreezeBlocked:
                    checks.append("pre-registration-name-attack-rejected-before-create")
                else:
                    raise FreezeBlocked("pre-registration name attack accepted")
                need(not os.listdir(stage_fd), "pre-registration rejection created no file")
                cleanup_exact_transaction(root_fd, stage_fd, directory_identity, {})
                need(not os.path.lexists(PRIVATE_ROOT / stage_name),
                     "pre-registration stage exact cleanup")
            finally:
                os.close(stage_fd)
                os.close(root_fd)

            # Inject a mode failure through the real exclusive_bytes path.
            # The inode must already be registered, its descriptor must close,
            # and exact cleanup must remove only that owned inode.
            candidate = PRIVATE_ROOT / "post-create-mode-candidate"
            stage_name, _target_name, root_fd, stage_fd, directory_identity = create_stage(candidate)
            created = {}
            victim = next(iter(FILES.values()))
            original_checked_output_info = checked_output_info
            fd_count_before = len(os.listdir("/proc/self/fd"))

            def injected_mode_failure(descriptor: int, label: str) -> os.stat_result:
                os.fchmod(descriptor, 0o640)
                return original_checked_output_info(descriptor, label)

            try:
                globals()["checked_output_info"] = injected_mode_failure
                try:
                    exclusive_bytes(stage_fd, victim, b"mode-admission-failure", created)
                except FreezeBlocked:
                    checks.append("function-path-post-create-mode-failure-fd-closed-and-registered")
                else:
                    raise FreezeBlocked("post-create mode attack accepted")
                finally:
                    globals()["checked_output_info"] = original_checked_output_info
                need(victim in created, "failed mode admission inode registered")
                need(
                    len(os.listdir("/proc/self/fd")) == fd_count_before,
                    "failed register admission leaked no descriptor",
                )
                cleanup_exact_transaction(root_fd, stage_fd, directory_identity, created)
                need(not os.path.lexists(PRIVATE_ROOT / stage_name),
                     "post-create mode failure exact cleanup")
            finally:
                globals()["checked_output_info"] = original_checked_output_info
                os.close(stage_fd)
                os.close(root_fd)

            # Exercise the separate emit_ledger fd-to-fileobj transition under
            # the same post-create admission failure; it must not leak the raw
            # descriptor before os.fdopen takes ownership.
            candidate = PRIVATE_ROOT / "ledger-post-create-mode-candidate"
            stage_name, _target_name, root_fd, stage_fd, directory_identity = create_stage(candidate)
            created = {}
            spool = RowSpool("cell")
            spool.add({
                "schema": SCHEMA + ".transaction-self-test-row.v1",
                ID_FIELDS["cell"]: "round306b1r0-transaction-self-test:cell",
            })
            fd_count_before = len(os.listdir("/proc/self/fd"))
            try:
                globals()["checked_output_info"] = injected_mode_failure
                try:
                    emit_ledger(stage_fd, FILES["cell"], "cell", spool, created)
                except FreezeBlocked:
                    checks.append("function-path-ledger-mode-failure-fd-closed-and-registered")
                else:
                    raise FreezeBlocked("ledger post-create mode attack accepted")
                finally:
                    globals()["checked_output_info"] = original_checked_output_info
                need(FILES["cell"] in created, "failed ledger admission inode registered")
                need(
                    len(os.listdir("/proc/self/fd")) == fd_count_before,
                    "failed ledger register admission leaked no descriptor",
                )
                cleanup_exact_transaction(root_fd, stage_fd, directory_identity, created)
                need(not os.path.lexists(PRIVATE_ROOT / stage_name),
                     "ledger mode failure exact cleanup")
            finally:
                globals()["checked_output_info"] = original_checked_output_info
                spool.close()
                os.close(stage_fd)
                os.close(root_fd)

            # Inject a failure immediately after the first post-mkdir inode
            # observation.  create_stage must remove exactly that directory.
            candidate = PRIVATE_ROOT / "post-mkdir-failure-candidate"
            try:
                create_stage(candidate, _self_test_fail_after_mkdir=True)
            except FreezeBlocked:
                checks.append("post-mkdir-admission-failure-exact-cleanup")
            else:
                raise FreezeBlocked("post-mkdir failure injection accepted")
            need(not os.listdir(PRIVATE_ROOT), "post-mkdir failure left no stage")

            # Replace a tracked filename with a different inode.  Validation
            # must reject it, while cleanup removes only the original tracked
            # inode and leaves the untracked replacement intact.
            candidate = PRIVATE_ROOT / "file-replacement-candidate"
            stage_name, _target_name, root_fd, stage_fd, directory_identity = create_stage(candidate)
            created = {}
            victim = next(iter(FILES.values()))
            try:
                exclusive_bytes(stage_fd, victim, b"original", created)
                os.rename(
                    victim,
                    "held-original",
                    src_dir_fd=stage_fd,
                    dst_dir_fd=stage_fd,
                )
                replacement_fd = os.open(
                    victim,
                    os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
                    0o600,
                    dir_fd=stage_fd,
                )
                os.write(replacement_fd, b"replacement")
                os.fsync(replacement_fd)
                os.close(replacement_fd)
                try:
                    validate_created_file(stage_fd, created[victim])
                except FreezeBlocked:
                    checks.append("file-inode-replacement-attack-rejected")
                else:
                    raise FreezeBlocked("file inode replacement accepted")
                cleanup_exact_transaction(
                    root_fd,
                    stage_fd,
                    directory_identity,
                    created,
                )
                need(
                    set(os.listdir(stage_fd)) == {victim},
                    "cleanup preserves untracked replacement",
                )
                checks.append("cleanup-exact-file-inode-scoped")
                os.unlink(victim, dir_fd=stage_fd)
                os.fsync(stage_fd)
                assert_directory_name_bound(root_fd, stage_name, stage_fd, "file attack cleanup")
                os.rmdir(stage_name, dir_fd=root_fd)
                os.fsync(root_fd)
            finally:
                os.close(stage_fd)
                os.close(root_fd)

            # Replace the stage name after opening it.  The name/fd binding
            # must fail; exact cleanup finds the original inode even under a
            # different name and does not remove the replacement directory.
            candidate = PRIVATE_ROOT / "stage-replacement-candidate"
            stage_name, _target_name, root_fd, stage_fd, directory_identity = create_stage(candidate)
            held_name = stage_name + ".held"
            try:
                os.rename(
                    stage_name,
                    held_name,
                    src_dir_fd=root_fd,
                    dst_dir_fd=root_fd,
                )
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
                    stage_name in os.listdir(root_fd)
                    and held_name not in os.listdir(root_fd),
                    "cleanup exact directory inode scoped",
                )
                checks.append("cleanup-exact-directory-inode-scoped")
                os.rmdir(stage_name, dir_fd=root_fd)
                os.fsync(root_fd)
            finally:
                os.close(stage_fd)
                os.close(root_fd)
            need(not os.listdir(PRIVATE_ROOT), "transaction self-test private root empty")
        finally:
            PRIVATE_ROOT = original_private_root

    need(len(checks) == 13, "transaction self-test count")
    return {
        "schema": SCHEMA + ".transaction-self-test.v1",
        "status": "PASS_LIGHTWEIGHT_ROUND306B1R0_DIRFD_INODE_BOUND_TRANSACTION_SELF_TEST",
        "tests_passed": checks,
        "large_input_opened": False,
        "formal_candidate_written": False,
        "audit_authorized": AUDIT_AUTHORIZED,
    }


def build_private_candidate(candidate: Path) -> dict[str, Any]:
    need(IMPLEMENTATION_PRESENT, "heavy loader not implemented")
    need(
        AUDIT_AUTHORIZED,
        "candidate mode blocked before any large-input open or write: hostile audit authorization is false",
    )
    producer_fd = -1
    root_fd = -1
    stage_fd = -1
    spools: dict[str, RowSpool] = {}
    created: dict[str, dict[str, Any]] = {}
    transaction_complete = False
    directory_identity = (-1, -1)
    try:
        producer_fd, producer_info, producer_sha256 = open_verified_running_producer()
        verify_all_input_pins()
        spools, audit = build_inventory()
        (
            stage_name,
            target_name,
            root_fd,
            stage_fd,
            directory_identity,
        ) = create_stage(candidate)
        metadata: dict[str, Any] = {}
        for kind in ("cell", "member", "gap"):
            metadata[kind] = emit_ledger(
                stage_fd,
                FILES[kind],
                kind,
                spools[kind],
                created,
            )
            os.fsync(stage_fd)
        payload = {
            "schema": SCHEMA,
            "status": "PRIVATE_ZERO_CREDIT_R288_SOURCE_INVENTORY_AND_UNION_FREEZE_CANDIDATE",
            "producer_file_sha256": producer_sha256,
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
        recheck_running_producer(producer_fd, producer_info, producer_sha256)
        verify_all_input_pins()
        strict_candidate_file_census(stage_fd, created)
        assert_directory_name_bound(root_fd, stage_name, stage_fd, "pre-publish stage")
        rename_noreplace(root_fd, stage_name, root_fd, target_name)
        os.fsync(root_fd)
        assert_directory_name_bound(root_fd, target_name, stage_fd, "post-publish candidate")
        strict_candidate_file_census(stage_fd, created)
        recheck_running_producer(producer_fd, producer_info, producer_sha256)
        assert_directory_name_bound(root_fd, target_name, stage_fd, "final candidate")
        strict_candidate_file_census(stage_fd, created)
        transaction_complete = True
        return {
            "status": "PASS_PRIVATE_ZERO_CREDIT_CANDIDATE_WRITTEN",
            "result_sha256": result["result_sha256"],
            "result_file_sha256": result_file_sha256,
            "formal_artifact_written": False,
        }
    finally:
        if not transaction_complete and root_fd >= 0 and stage_fd >= 0:
            cleanup_exact_transaction(
                root_fd,
                stage_fd,
                directory_identity,
                created,
            )
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
        )
        == 1,
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
