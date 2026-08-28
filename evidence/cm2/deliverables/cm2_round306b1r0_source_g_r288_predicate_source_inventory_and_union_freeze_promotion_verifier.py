#!/usr/bin/env python3
"""Independent fail-closed verifier for the Round306B1R0 source freeze.

The producer is never imported, executed, parsed, or tokenized.  It is only an
inert byte object pinned by size and SHA-256.  This verifier independently
streams the sealed Round288 dispositions, reconstructs the Round269--Round272
predicate-source partition, rebinds it to Round294 and sealed Round306B0, and
then compares every candidate row with that reconstruction.

Heavy reconstruction, candidate admission, and publication are deliberately
blocked by ``AUDIT_AUTHORIZED`` before any large source or candidate is opened
and before any output is written.  Lightweight contract and attack tests remain
available while the gate is false.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import ctypes
import errno
import fcntl
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
PRIVATE_ROOT = ROOT / ".cm2-round306b1r0-private-candidates"
PREFIX = "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze"
SCHEMA = "cm2.round306b1r0.source-g-r288-predicate-source-inventory-and-union-freeze.v1"
PRODUCER = PREFIX + ".py"
VERIFIER = PREFIX + "_promotion_verifier.py"
ATTACK = PREFIX + "_attack_suite.json"
VERIFICATION = PREFIX + "_verification.json"
EXPECTED_PRODUCER_SHA256 = "3538e17fd523384d31a2fbf46505ff4ee5bf7ba8f41db14534e55edaa04eabca"
EXPECTED_PRODUCER_SIZE = 73_458
AUDIT_AUTHORIZED = True

ENCODER = json.JSONEncoder(
    sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False
)
HEX64 = re.compile(r"^[0-9a-f]{64}$")
RAW_GZIP_INPUT_CHUNK_BYTES = 1 << 20
RAW_GZIP_OUTPUT_CHUNK_BYTES = 1 << 20
CANDIDATE_TEXT_CHUNK_CHARACTERS = 1 << 16
CANDIDATE_TOKEN_SYNTAX_MARGIN_CHARACTERS = 1 << 16

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
CANDIDATE_ORDER = (FILES["cell"], FILES["member"], FILES["gap"], FILES["result"])
PROMOTION_ORDER = (
    ATTACK, FILES["cell"], FILES["member"], FILES["gap"], FILES["result"],
    VERIFICATION,
)

# Exact size is part of every immutable source pin; this is deliberately not
# shared with or loaded from producer code.
SOURCE_PINS: dict[str, tuple[str, int]] = {
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json":
        ("ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c", 158_815_476),
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_verification.json":
        ("b008c2208891374696b88506e87957bbb754d95d62677d9406c466405b311f36", 4_956),
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_manifest.sha256":
        ("32dea92dd0de87d3ded6ed69a908b58b01402ddcdef3f0e2b5ffde096a9383c5", 946),
    "cm2_round269_source_g_closed_collar_direct_signature_materialization_certificate.json":
        ("472df3ac65c490b79924beaabb382435f5b74ea8ac6c13d71b1d0ab54ffe01d3", 319_672_585),
    "cm2_round269_source_g_closed_collar_direct_signature_materialization_verification.json":
        ("3435ad2ad0d76f881e7b49fd052fb64035776a991b0f92a542b054f224860982", 895),
    "cm2_round269_source_g_closed_collar_direct_signature_materialization_manifest.sha256":
        ("99d8eb8260775b3f2e00bfb51790a6db45a1307753183d61173a2307033c407d", 885),
    "cm2_round270_source_g_outgoing_g_factor_signature_materialization_certificate.json":
        ("72a47e53ff601660cb63fe8062403e41a54450fa4a432638faf18a2c76b3efea", 56_705_100),
    "cm2_round270_source_g_outgoing_g_factor_signature_materialization_verification.json":
        ("6af01780481224f8c9fd690c46886321be4f5b294c33e3f6515cf20dc7cb0513", 888),
    "cm2_round270_source_g_outgoing_g_factor_signature_materialization_manifest.sha256":
        ("a23fc6c40b6a29314a9ed7eded86e10242d88a657a321df0c6cfd1b081a8e851", 867),
    "cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_certificate.json":
        ("c2a6b66c6fc6ac0b353b36254339a90b91f18c52246c324307ee49569bd7b747", 112_741_715),
    "cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_verification.json":
        ("26eed04f887f8b6a4ec8fcc88f1112f7382e079d9c53a33dd37a53f7417a29f9", 896),
    "cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_manifest.sha256":
        ("6c6b710b3d04c24f962ecb00399ea7d2bccf64650b5e78af36a59c2a754f0697", 897),
    "cm2_round272_source_g_boundary_dual_factor_wall_closure_certificate.json":
        ("16050c7087deb546d39b2c7922274ccae7cec24a799ecafd9a8304ae1186d8f2", 1_250_159),
    "cm2_round272_source_g_boundary_dual_factor_wall_closure_verification.json":
        ("a40f79823dcf07155eec1ecd12cc367dae6b7bdc7a6e8e7cf8680d29d4dade10", 877),
    "cm2_round272_source_g_boundary_dual_factor_wall_closure_manifest.sha256":
        ("82124ccbc3fa88fadb1f2a3239634dca332ccc959f7338c44cd27908e4957e5a", 807),
    "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_atom_dispositions.json.gz":
        ("6b0a8aa1cd38019322a61f5aaefc936006d10769cd21a5c8df374576f9ac570a", 134_114_861),
    "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_result.json":
        ("9b5875777f3937efe05a4d871a8c8b76c92ca69d0f636eb014542f59dfe49569", 8_981),
    "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_verification.json":
        ("f08749d2f90ea63a696c482a342489c12e2c86436734a59c6a2e2b79d9cf9b23", 9_874),
    "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_manifest.sha256":
        ("c15e4657051318f1a4e6aadcf80fa679840969c7f2c776e65460ac05cc2eb1eb", 1_203),
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_registry_ledger.json.gz":
        ("c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb", 262_951_902),
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_result.json":
        ("dc93ef564ce1aec4aabbc7ff717ac76749b92899e210179a00dba63f2d32d626", 6_958),
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_verification.json":
        ("13dcb461f269a8e346c220b85cad0e87a0392b5e2682b7dd70132fd8bd7a1245", 6_529),
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_manifest.sha256":
        ("90d5cda0271610bf95a72f94e9bae8e192425580019dd3c823b5a69d20e52131", 1_275),
    "cm2_round306b0_source_g_r306a_universe_support_source_freeze_member_support_source_index.json.gz":
        ("c9a8649c8473bb6a170187e7f803e95748d2ff2198b1b846d97383dd5f0581af", 162_499_140),
    "cm2_round306b0_source_g_r306a_universe_support_source_freeze_result.json":
        ("badc000c6fadd8807b26a7c3511edc51796c962f150b438956e4c549fd0d5735", 9_450),
    "cm2_round306b0_source_g_r306a_universe_support_source_freeze_verification.json":
        ("f8acc3150d4663d92976a44ab1c3b35c7264f4c4d14808f9133f1184d3f4b590", 7_003),
    "cm2_round306b0_source_g_r306a_universe_support_source_freeze_manifest.sha256":
        ("9846b36d28bb1507b273de3e613a5ecd5ac6515258042bf8b91b89e0c156b269", 1_760),
}
VERIFIED_SOURCE_NAMES: set[str] = set()

EXPECTED = {
    "Round288_atom_identities": 332_016,
    "existing_Round208_identities": 36_040,
    "Round204_alias_identities": 640,
    "new_member_identities": 295_336,
    "source_side_partition_rows": 332_020,
    "new_predicate_source_cells": 295_340,
    "multiplicity_one_new_members": 295_332,
    "multiplicity_two_new_members": 4,
    "Round269_cells": 187_128,
    "Round270_cells": 37_712,
    "Round271_cells": 70_356,
    "Round272_cells": 144,
    "W_tail_parent_normalizations": 4,
    "cell_theorem_gaps": 295_340,
    "member_union_theorem_gaps": 295_336,
    "total_gaps": 590_676,
}
SOURCE_TABLES = (
    (269, "cm2_round269_source_g_closed_collar_direct_signature_materialization_certificate.json", "formal_direct_side_signature_ledger", 187_128),
    (270, "cm2_round270_source_g_outgoing_g_factor_signature_materialization_certificate.json", "formal_direct_side_signature_ledger", 37_712),
    (271, "cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_certificate.json", "formal_side_signature_ledger", 70_420),
    (272, "cm2_round272_source_g_boundary_dual_factor_wall_closure_certificate.json", "formal_side_signature_ledger", 720),
)
NEW_STATES = frozenset({
    "NEW_DISJOINT_PROMOTION_READY_CANDIDATE__ROUND279_STRICT_INWARD_CORRIDOR_INNER_SUPPORT__PENDING_INDEPENDENT_ROUND288_VERIFIER",
    "NEW_DISJOINT_CANDIDATE__POSITIVE_VOLUME_RATIONAL_INNER_SUPPORT_NOT_MATERIALIZED",
})
R208_STATE = "EXISTING_ROUND208_OCCURRENCE_ID_PRESERVED"
R204_STATE = "EXACT_ALIAS_OF_EXISTING_ROUND204_OCCURRENCE"


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


def iter_array(stream: TextIO, marker: str, initial: str = "") -> Iterator[dict[str, Any]]:
    buffer = initial
    while marker not in buffer:
        block = stream.read(1 << 20)
        need(bool(block), "missing array marker:" + marker)
        buffer += block
        need(len(buffer) <= (1 << 25), "bounded marker prelude")
    buffer = buffer.split(marker, 1)[1]
    require_comma = False
    while True:
        buffer = buffer.lstrip()
        while not buffer:
            block = stream.read(1 << 20)
            need(bool(block), "truncated streamed array")
            buffer += block
            buffer = buffer.lstrip()
        if buffer[0] == "]":
            return
        if require_comma:
            need(buffer[0] == ",", "missing streamed comma")
            buffer = buffer[1:].lstrip()
            while not buffer:
                block = stream.read(1 << 20)
                need(bool(block), "truncated streamed array after comma")
                buffer += block
                buffer = buffer.lstrip()
            need(buffer and buffer[0] != "]", "trailing streamed comma")
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
        if table_anchor is not None:
            while table_anchor not in initial:
                block = text.read(1 << 20)
                need(bool(block), "missing table anchor:" + table_anchor)
                initial += block
                need(len(initial) <= (1 << 25), "bounded table prelude")
            initial = initial.split(table_anchor, 1)[1]
        yield from iter_array(text, marker, initial)
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
        self.total_canonical_row_bytes = 0
        self.maximum_canonical_row_bytes = 0
        self.file = tempfile.TemporaryFile(mode="w+b")

    def append(self, payload: dict[str, Any]) -> dict[str, Any]:
        row = close_row(payload)
        row_id = row.get(ID_FIELDS[self.kind])
        need(type(row_id) is str and row_id not in self.seen,
             "unique independently reconstructed row id:" + self.kind)
        self.seen.add(row_id)
        row_wire = canonical(row)
        self.file.write(row_wire + b"\n")
        self.total_canonical_row_bytes += len(row_wire)
        self.maximum_canonical_row_bytes = max(
            self.maximum_canonical_row_bytes, len(row_wire)
        )
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


def source_round(source_id: str) -> int:
    match = re.match(r"^round(269|270|271|272)-", source_id)
    need(match is not None, "known predicate-source prefix:" + source_id)
    return int(match.group(1))


def rational_box(value: Any, label: str) -> tuple[Fraction, ...]:
    need(type(value) is list and len(value) == 6, label + ":box arity")
    try:
        box = tuple(Fraction(item) for item in value)
    except (ValueError, ZeroDivisionError, TypeError) as error:
        raise VerificationBlocked(label + ":rational box") from error
    need(all(box[2 * axis] < box[2 * axis + 1] for axis in range(3)), label + ":positive box")
    return box


def box_strings(box: tuple[Fraction, ...]) -> list[str]:
    return [str(item) for item in box]


def exact_box_union(boxes: list[list[str]]) -> list[list[str]]:
    work = sorted(set(rational_box(box, "box union") for box in boxes))
    while True:
        replacement: tuple[int, int, tuple[Fraction, ...]] | None = None
        for left_index, left in enumerate(work):
            for right_index in range(left_index + 1, len(work)):
                right = work[right_index]
                for axis in range(3):
                    other_axes_equal = all(
                        left[2 * other:2 * other + 2] == right[2 * other:2 * other + 2]
                        for other in range(3) if other != axis
                    )
                    if not other_axes_equal:
                        continue
                    if left[2 * axis + 1] == right[2 * axis]:
                        merged = list(left)
                        merged[2 * axis + 1] = right[2 * axis + 1]
                    elif right[2 * axis + 1] == left[2 * axis]:
                        merged = list(right)
                        merged[2 * axis + 1] = left[2 * axis + 1]
                    else:
                        continue
                    replacement = left_index, right_index, tuple(merged)
                    break
                if replacement is not None:
                    break
            if replacement is not None:
                break
        if replacement is None:
            return [box_strings(box) for box in work]
        left_index, right_index, merged = replacement
        work = [box for index, box in enumerate(work) if index not in {left_index, right_index}]
        work.append(merged)
        work.sort()


def independently_normalize_w_tail(
    atom_id: str,
    outer_envelopes: list[list[str]],
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    need(len(rows) == 2 and {row.get("t_child") for row in rows} == {0, 1},
         "W-tail two-child partition:" + atom_id)
    ordered = sorted(rows, key=lambda row: row["t_child"])
    lower = rational_box(ordered[0]["t_child_box"], "W-tail lower")
    upper = rational_box(ordered[1]["t_child_box"], "W-tail upper")
    need(lower[1] == upper[0] and lower[2:] == upper[2:],
         "W-tail artificial interface:" + atom_id)
    normalized = exact_box_union([ordered[0]["t_child_box"], ordered[1]["t_child_box"]])
    need(normalized == outer_envelopes and len(normalized) == 1,
         "W-tail parent envelope:" + atom_id)
    return {
        "normalization_kind": "ROUND271_ARTIFICIAL_T_BISECTION_PARENT_NORMALIZATION",
        "artificial_interface": {"axis": "t", "value": str(lower[1])},
        "interface_is_not_a_physical_support_boundary": True,
        "normalized_parent_box": normalized[0],
        "source_children": [row["signed_region_row_id"] for row in ordered],
        "full_support_credit": 0,
    }


def independently_unpack_round182() -> dict[str, dict[str, Any]]:
    document = load_source_object(
        "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json"
    )
    result = document.get("result")
    need(type(result) is dict and document.get("result_sha256") == digest(result),
         "Round182 result self hash")
    table = "collar_leaf_rows"
    rows = result.get(table)
    schemas = result.get("row_column_schemas")
    census_map = result.get("table_census_and_sha256")
    need(type(rows) is list and type(schemas) is dict and type(census_map) is dict,
         "Round182 leaf tables")
    columns = schemas.get(table)
    census = census_map.get(table)
    need(
        type(columns) is list and type(census) is dict
        and len(rows) == census.get("row_count")
        and digest(rows) == census.get("rows_sha256")
        and "row_id" in columns,
        "Round182 leaf commitment",
    )
    leaves: dict[str, dict[str, Any]] = {}
    for packed in rows:
        need(type(packed) is list and len(packed) == len(columns), "Round182 packed leaf")
        row = dict(zip(columns, packed, strict=True))
        row_id = row["row_id"]
        need(type(row_id) is str and row_id not in leaves, "Round182 unique leaf")
        leaves[row_id] = row
    return leaves


def independent_predicate_descriptor(round_number: int, row: dict[str, Any]) -> dict[str, Any]:
    signature = row.get("local_return_signature")
    need(type(signature) is dict and row.get("complete_10_field_return_signature_sha256") == digest(signature),
         "source signature self hash")
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


def verify_small_sealed_markers() -> None:
    """Require the pinned upstream markers, without trusting their prose alone."""
    b0 = load_source_object(
        "cm2_round306b0_source_g_r306a_universe_support_source_freeze_verification.json"
    )
    payload = dict(b0)
    claimed = payload.pop("verification_sha256", None)
    need(claimed == digest(payload), "sealed Round306B0 marker self hash")
    transition = b0.get("formal_credit_transition_at_this_verification_marker")
    boundary = b0.get("strict_downstream_boundary")
    need(
        b0.get("status") == "PASS_EXACT_ROUND306B0_UNIVERSE_SUPPORT_SOURCE_FREEZE"
        and type(transition) is dict
        and transition.get("member_universe_freeze") == 1
        and transition.get("pair_denominator_freeze") == 1
        and transition.get("maximality") == 0
        and transition.get("fibre") == 0
        and transition.get("global_disposition") == 0
        and type(boundary) is dict
        and boundary.get("D02_status") == "BLOCKED"
        and boundary.get("CM2_status") == "NO-GO_FOR_CLAIM",
        "sealed Round306B0 credit boundary",
    )
    for name, status_prefix in (
        (
            "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_verification.json",
            "PASS_INDEPENDENT_CACHELESS_ROUND288__332020_SOURCE_ROWS__332016_ATOMS__",
        ),
        (
            "cm2_round294_source_g_occurrence_registry_atomic_promotion_verification.json",
            "PASS_INDEPENDENT_CACHELESS_ROUND294_STAGE_A_REGISTRY__431208_ROWS__",
        ),
    ):
        marker = load_source_object(name)
        marker_payload = dict(marker)
        marker_claimed = marker_payload.pop("verification_sha256", None)
        need(marker_claimed == digest(marker_payload), "upstream marker self hash:" + name)
        need(type(marker.get("status")) is str and marker["status"].startswith(status_prefix),
             "upstream marker status:" + name)


def ledger_envelope(kind: str, ledger: ExpectedLedger) -> dict[str, Any]:
    payload = {
        "schema": SCHEMA + "." + kind + "-ledger.v1",
        "status": "PRIVATE_ZERO_CREDIT_SOURCE_INVENTORY_CANDIDATE",
        **ledger.metadata(),
        "formal_credit": {
            "full_support": 0,
            "maximality": 0,
            "fibre": 0,
            "global_disposition": 0,
        },
    }
    return {**payload, "ledger_sha256": digest(payload)}


def expected_ledger_wire_contract(
    kind: str, ledger: ExpectedLedger
) -> dict[str, Any]:
    envelope_wire = canonical(ledger_envelope(kind, ledger))
    marker_wire = (',"' + TABLES[kind] + '":[').encode("ascii")
    need(envelope_wire.endswith(b"}"), "canonical ledger envelope close:" + kind)
    comma_bytes = max(ledger.rows.count - 1, 0)
    uncompressed_bytes = (
        len(envelope_wire) - 1
        + len(marker_wire)
        + ledger.total_canonical_row_bytes
        + comma_bytes
        + len(b"]}")
    )
    need(
        ledger.rows.count > 0
        and ledger.total_canonical_row_bytes >= ledger.maximum_canonical_row_bytes > 0
        and uncompressed_bytes > ledger.total_canonical_row_bytes,
        "positive independently reconstructed ledger wire bounds:" + kind,
    )
    return {
        "envelope_wire": envelope_wire,
        "marker_wire": marker_wire,
        "uncompressed_bytes": uncompressed_bytes,
        "total_canonical_row_bytes": ledger.total_canonical_row_bytes,
        "maximum_canonical_row_bytes": ledger.maximum_canonical_row_bytes,
        "maximum_candidate_token_characters": (
            ledger.maximum_canonical_row_bytes
            + CANDIDATE_TOKEN_SYNTAX_MARGIN_CHARACTERS
        ),
    }


def strict_boundary() -> dict[str, Any]:
    return {
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
    }


def reconstruct_expected() -> tuple[dict[str, ExpectedLedger], dict[str, Any]]:
    """Freshly reconstruct every candidate row from sealed non-producer bytes."""
    VERIFIED_SOURCE_NAMES.clear()
    verify_small_sealed_markers()
    ledgers = {kind: ExpectedLedger(kind) for kind in ("cell", "member", "gap")}
    atoms: dict[str, dict[str, Any]] = {}
    source_owner: dict[str, str] = {}
    existing_208_sources: set[str] = set()
    alias_204_sources: set[str] = set()
    multiplicity: Counter[int] = Counter()
    new_rounds: Counter[int] = Counter()
    identity_count = 0

    round288 = (
        "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_"
        "atom_dispositions.json.gz"
    )
    for row in stream_source_rows(round288, '"rows":[', compressed=True):
        check_row(row, "Round288 disposition")
        identity_count += 1
        state = row.get("occurrence_identity_disposition")
        sources = row.get("source_signature_row_ids")
        need(
            type(sources) is list and sources == sorted(sources)
            and len(sources) in {1, 2} and all(type(item) is str for item in sources),
            "Round288 ordered source list",
        )
        if state in NEW_STATES:
            atom_id = row.get("canonical_atom_id")
            need(type(atom_id) is str and atom_id not in atoms, "unique new Round288 atom")
            atoms[atom_id] = row
            multiplicity[len(sources)] += 1
            for source_id in sources:
                need(
                    source_id not in source_owner
                    and source_id not in existing_208_sources
                    and source_id not in alias_204_sources,
                    "new source-side cell disjoint",
                )
                source_owner[source_id] = atom_id
                new_rounds[source_round(source_id)] += 1
        elif state == R208_STATE:
            need(
                len(sources) == 1
                and sources[0] not in existing_208_sources
                and sources[0] not in alias_204_sources
                and sources[0] not in source_owner,
                "unique existing Round208 identity source",
            )
            existing_208_sources.add(sources[0])
        elif state == R204_STATE:
            need(
                len(sources) == 1
                and sources[0] not in alias_204_sources
                and sources[0] not in existing_208_sources
                and sources[0] not in source_owner,
                "unique Round204 alias identity source",
            )
            alias_204_sources.add(sources[0])
        else:
            raise VerificationBlocked("unknown Round288 disposition state")

    need(identity_count == EXPECTED["Round288_atom_identities"],
         "332016 atom-identity census")
    need(
        identity_count
        == len(existing_208_sources) + len(alias_204_sources) + len(atoms)
        == EXPECTED["Round288_atom_identities"],
        "Round288 identity partition 36040+640+295336",
    )
    need(len(existing_208_sources) == EXPECTED["existing_Round208_identities"],
         "Round208 identity census")
    need(len(alias_204_sources) == EXPECTED["Round204_alias_identities"],
         "Round204 alias identity census")
    need(len(atoms) == EXPECTED["new_member_identities"], "new-member identity census")
    need(len(source_owner) == EXPECTED["new_predicate_source_cells"],
         "new predicate-source-cell census")
    need(
        len(existing_208_sources) + len(alias_204_sources) + len(source_owner)
        == EXPECTED["source_side_partition_rows"],
        "332020 source-side partition; four W-tail cells are not identities",
    )
    need(
        multiplicity == {
            1: EXPECTED["multiplicity_one_new_members"],
            2: EXPECTED["multiplicity_two_new_members"],
        },
        "new-member source multiplicity",
    )
    need(
        new_rounds == {
            269: EXPECTED["Round269_cells"],
            270: EXPECTED["Round270_cells"],
            271: EXPECTED["Round271_cells"],
            272: EXPECTED["Round272_cells"],
        },
        "exact source round census",
    )

    registry: dict[str, dict[str, Any]] = {}
    round294 = "cm2_round294_source_g_occurrence_registry_atomic_promotion_registry_ledger.json.gz"
    for row in stream_source_rows(round294, '"rows":[', compressed=True):
        check_row(row, "Round294 registry")
        if row.get("registry_entry_kind") != "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM":
            continue
        atom_id = row.get("canonical_atom_id")
        need(type(atom_id) is str and atom_id in atoms and atom_id not in registry,
             "Round294 exact new atom set")
        atom = atoms[atom_id]
        need(
            row.get("registry_occurrence_id")
            == atom.get("reserved_candidate_occurrence_id__not_issued")
            and row.get("source_signature_row_ids") == atom.get("source_signature_row_ids")
            and row.get("source_row_id") == atom.get("Round288_atom_disposition_row_id")
            and row.get("source_row_sha256") == atom.get("row_sha256"),
            "Round294/Round288 row-exact rebinding",
        )
        registry[atom_id] = row
    need(set(registry) == set(atoms), "complete Round294 new atom registry")

    b0_by_member: dict[str, dict[str, Any]] = {}
    b0_name = (
        "cm2_round306b0_source_g_r306a_universe_support_source_freeze_"
        "member_support_source_index.json.gz"
    )
    for row in stream_source_rows(b0_name, '"member_support_source_rows":[', compressed=True):
        check_row(row, "Round306B0 member source")
        if row.get("identity_tranche") != "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM":
            continue
        member_id = row.get("member_id")
        need(type(member_id) is str and member_id not in b0_by_member,
             "unique Round306B0 R288 member")
        b0_by_member[member_id] = row
    registry_members = {row["registry_occurrence_id"] for row in registry.values()}
    need(
        set(b0_by_member) == registry_members
        and len(b0_by_member) == EXPECTED["new_member_identities"],
        "Round294/Round306B0 new member set equality",
    )
    for atom_id, registry_row in registry.items():
        atom = atoms[atom_id]
        b0 = b0_by_member[registry_row["registry_occurrence_id"]]
        need(
            b0.get("identity_class") == "FORMAL_OCCURRENCE"
            and b0.get("pair_denominator_class") == "OCCURRENCE"
            and b0.get("primary_source_package") == "R294"
            and b0.get("primary_source_row_id")
            == registry_row.get("Round294_occurrence_registry_row_id")
            and b0.get("primary_source_row_sha256") == registry_row.get("row_sha256")
            and b0.get("official_key_id")
            == registry_row.get("official_key_id")
            == atom.get("official_key_id"),
            "Round306B0/Round294/Round288 exact member binding",
        )

    leaves = independently_unpack_round182()
    source_rows: dict[str, dict[str, Any]] = {}
    round_counts: Counter[int] = Counter()
    seen_204: set[str] = set()
    boxes_by_atom: dict[str, list[list[str]]] = defaultdict(list)
    cells_by_atom: dict[str, list[str]] = defaultdict(list)

    for round_number, name, table, complete_count in SOURCE_TABLES:
        observed_complete = 0
        for row in stream_source_rows(
            name, '"rows":[', compressed=False, table_anchor='"' + table + '":{',
        ):
            observed_complete += 1
            check_row(row, "predicate-source row")
            source_id = row.get("signed_region_row_id")
            need(type(source_id) is str, "source row id")
            if source_id not in source_owner:
                need(
                    source_id in alias_204_sources and round_number in {271, 272},
                    "only exact Round204 aliases excluded from source certificates",
                )
                seen_204.add(source_id)
                continue
            need(
                source_round(source_id) == round_number and source_id not in source_rows,
                "source round and global uniqueness",
            )
            atom_id = source_owner[source_id]
            atom = atoms[atom_id]
            signature = row.get("local_return_signature")
            need(type(signature) is dict, "source return signature")
            need(
                row.get("Round182_leaf_row_id") == atom.get("Round182_leaf_row_id")
                and row.get("complete_10_field_return_signature_sha256")
                == atom.get("complete_10_field_return_signature_sha256")
                and signature.get("source_chart") == atom.get("source_chart")
                and signature.get("target_lift") == atom.get("owner_target"),
                "source/atom exact metadata join",
            )
            leaf_id = row["Round182_leaf_row_id"]
            need(leaf_id in leaves, "source Round182 leaf exists")
            box = row.get("t_child_box", leaves[leaf_id]["box"])
            rational_box(box, "source cell")
            descriptor = independent_predicate_descriptor(round_number, row)
            cell_id = "round306b1r0-predicate-source-cell:" + digest(
                [source_id, atom_id, box, descriptor]
            )
            cell = ledgers["cell"].append({
                "schema": SCHEMA + ".predicate-source-cell-row.v1",
                "Round306B1R0_predicate_source_cell_row_id": cell_id,
                "member_canonical_atom_id": atom_id,
                "formal_member_id": registry[atom_id]["registry_occurrence_id"],
                "source_round": round_number,
                "source_filename": name,
                "source_file_sha256": SOURCE_PINS[name][0],
                "source_table": table,
                "source_signature_row_id": source_id,
                "source_signature_row_sha256": row["row_sha256"],
                "Round182_leaf_row_id": leaf_id,
                "outer_carrier_box": box,
                "predicate_source_inventory": descriptor,
                "official_key_metadata_only": {
                    "official_key_id": signature["official_key_id"],
                    "official_key_ordinal": signature["official_key_ordinal"],
                    "complete_10_field_return_signature_sha256":
                        row["complete_10_field_return_signature_sha256"],
                },
                "official_key_used_as_join_or_routing_filter": False,
                "source_free_interval_predicate_ast_materialized": False,
                "outer_carrier_box_claimed_as_full_support": False,
                "formal_full_support_credit": 0,
                "formal_maximality_credit": 0,
                "formal_fibre_credit": 0,
                "formal_global_disposition_credit": 0,
            })
            ledgers["gap"].append({
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
            round_counts[round_number] += 1
            boxes_by_atom[atom_id].append(box)
            cells_by_atom[atom_id].append(cell_id)
        need(observed_complete == complete_count, "complete source certificate row count")

    need(set(source_rows) == set(source_owner), "complete new source-cell set equality")
    need(seen_204 == alias_204_sources, "all and only Round204 aliases excluded")
    need(round_counts == new_rounds, "source reconstruction round histogram")

    w_tail_count = 0
    for atom_id in sorted(atoms):
        atom = atoms[atom_id]
        registry_row = registry[atom_id]
        member_id = registry_row["registry_occurrence_id"]
        b0 = b0_by_member[member_id]
        source_ids = atom["source_signature_row_ids"]
        independently_derived_cell_ids: list[str] = []
        for source_id in source_ids:
            row = source_rows[source_id]
            box = row.get("t_child_box", leaves[row["Round182_leaf_row_id"]]["box"])
            descriptor = independent_predicate_descriptor(source_round(source_id), row)
            independently_derived_cell_ids.append(
                "round306b1r0-predicate-source-cell:"
                + digest([source_id, atom_id, box, descriptor])
            )
        need(cells_by_atom[atom_id] == independently_derived_cell_ids,
             "member source/cell order")
        normalized_boxes = exact_box_union(boxes_by_atom[atom_id])
        need(normalized_boxes == atom["frozen_positive_rational_support_envelopes"],
             "source outer-envelope union")
        normalization = None
        if len(source_ids) == 2:
            need(all(item.startswith("round271-W-tail-side:") for item in source_ids),
                 "only W-tail multiplicity two")
            normalization = independently_normalize_w_tail(
                atom_id, atom["frozen_positive_rational_support_envelopes"],
                [source_rows[item] for item in source_ids],
            )
            w_tail_count += 1
        union_id = "round306b1r0-member-union:" + digest(
            [member_id, source_ids, cells_by_atom[atom_id]]
        )
        ledgers["member"].append({
            "schema": SCHEMA + ".member-union-row.v1",
            "Round306B1R0_member_union_row_id": union_id,
            "member_id": member_id,
            "canonical_atom_id": atom_id,
            "Round306A_component_id": b0["Round306A_component_id"],
            "Round294_registry_row_id": registry_row["Round294_occurrence_registry_row_id"],
            "Round306B0_member_source_row_id": b0["Round306B0_member_support_source_row_id"],
            "source_signature_row_ids": source_ids,
            "predicate_source_cell_row_ids": cells_by_atom[atom_id],
            "predicate_source_cell_multiplicity": len(source_ids),
            "outer_envelope_union_structurally_exact": True,
            "normalized_outer_envelopes": normalized_boxes,
            "Round271_W_tail_parent_normalization": normalization,
            "official_key_metadata_only": atom["official_key_id"],
            "official_key_used_as_join_or_routing_filter": False,
            "full_support_union_theorem_status":
                "PENDING_SOURCE_FREE_INTERVAL_PREDICATE_EQUIVALENCE",
            "formal_full_support_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
        })
        ledgers["gap"].append({
            "schema": SCHEMA + ".gap-row.v1",
            "Round306B1R0_gap_row_id": "round306b1r0-gap:member:" + digest(member_id),
            "gap_kind": "MEMBER_FULL_SUPPORT_UNION_THEOREM_PENDING",
            "member_union_row_id": union_id,
            "member_id": member_id,
            "source_cell_count": len(source_ids),
            "required_closure": "prove the exact source-free cell predicates cover the member support with no missing physical locus",
            "formal_credit": 0,
        })

    need(w_tail_count == EXPECTED["W_tail_parent_normalizations"],
         "four W-tail parent normalizations")
    need(ledgers["cell"].rows.count == EXPECTED["new_predicate_source_cells"],
         "cell ledger count")
    need(ledgers["member"].rows.count == EXPECTED["new_member_identities"],
         "member ledger count")
    need(ledgers["gap"].rows.count == EXPECTED["total_gaps"], "gap ledger count")

    audit = {
        "Round288_new_atom_count": len(atoms),
        "predicate_source_cell_count": len(source_rows),
        "source_round_histogram": {
            str(key): value for key, value in sorted(round_counts.items())
        },
        "source_multiplicity_histogram": {
            str(key): value for key, value in sorted(multiplicity.items())
        },
        "excluded_Round208_existing_atom_count": len(existing_208_sources),
        "excluded_Round204_existing_atom_count": len(alias_204_sources),
        "Round294_member_set_equals_Round306B0_member_set": True,
        "Round271_W_tail_parent_normalization_count": w_tail_count,
        "outer_envelope_union_exact_for_every_member": True,
        "source_free_interval_predicate_theorem_complete": False,
        "full_support_union_theorem_complete": False,
    }
    # Hash/size-bind small companion results and manifests that are not row
    # sources but are nevertheless part of the immutable dependency snapshot.
    for name in sorted(set(SOURCE_PINS) - VERIFIED_SOURCE_NAMES):
        descriptor, before = open_source(name)
        close_source(descriptor, before, name)
    need(VERIFIED_SOURCE_NAMES == set(SOURCE_PINS), "all source pins observed")
    return ledgers, audit


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
    need(names == tuple(sorted(CANDIDATE_ORDER)), "candidate exact four-file census")
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


def iter_exact_candidate_array(
    text: TextIO,
    initial: str,
    maximum_token_characters: int = 1 << 20,
    text_chunk_characters: int = CANDIDATE_TEXT_CHUNK_CHARACTERS,
) -> Iterator[dict[str, Any]]:
    need(
        0 < text_chunk_characters <= CANDIDATE_TEXT_CHUNK_CHARACTERS
        and maximum_token_characters >= text_chunk_characters,
        "bounded candidate parser parameters",
    )
    buffer = initial
    need(len(buffer) <= maximum_token_characters,
         "candidate row/token buffer bounded")
    require_comma = False
    while True:
        buffer = buffer.lstrip()
        while not buffer:
            block = text.read(text_chunk_characters)
            need(bool(block), "truncated candidate array")
            buffer += block
            buffer = buffer.lstrip()
            need(len(buffer) <= maximum_token_characters,
                 "candidate row/token buffer bounded")
        if buffer[0] == "]":
            buffer = buffer[1:].lstrip()
            while not buffer:
                block = text.read(text_chunk_characters)
                need(bool(block), "candidate ledger missing outer close")
                buffer += block
                buffer = buffer.lstrip()
                need(len(buffer) <= maximum_token_characters,
                     "candidate row/token buffer bounded")
            need(buffer[0] == "}", "candidate ledger outer close")
            need(not buffer[1:].strip(), "candidate ledger trailing bytes")
            while True:
                trailing = text.read(text_chunk_characters)
                if not trailing:
                    break
                need(not trailing.strip(), "candidate ledger trailing bytes or gzip member")
            return
        if require_comma:
            need(buffer[0] == ",", "candidate array missing comma")
            buffer = buffer[1:].lstrip()
            while not buffer:
                block = text.read(text_chunk_characters)
                need(bool(block), "candidate array truncated after comma")
                buffer += block
                buffer = buffer.lstrip()
                need(len(buffer) <= maximum_token_characters,
                     "candidate row/token buffer bounded")
            need(buffer[0] != "]", "candidate array trailing comma")
        else:
            need(buffer[0] != ",", "candidate array leading comma")
        while True:
            try:
                row, end = DECODER.raw_decode(buffer)
                break
            except json.JSONDecodeError:
                block = text.read(text_chunk_characters)
                need(bool(block), "truncated candidate row")
                buffer += block
                need(len(buffer) <= maximum_token_characters,
                     "candidate row/token buffer bounded")
        need(type(row) is dict, "candidate row object")
        yield row
        buffer = buffer[end:]
        require_comma = True


def validate_single_gzip_member_at(
    directory_fd: int,
    descriptor: int,
    name: str,
    before: os.stat_result,
    expected_decompressed_bytes: int,
    *,
    input_chunk_bytes: int = RAW_GZIP_INPUT_CHUNK_BYTES,
    output_chunk_bytes: int = RAW_GZIP_OUTPUT_CHUNK_BYTES,
) -> dict[str, int]:
    """Stream-validate one complete gzip member on an already-bound fd.

    ``gzip.GzipFile`` deliberately accepts concatenated members, so JSON-level
    trailing-data checks cannot distinguish an empty second member from no
    second member.  This raw pass uses one RFC 1952-aware zlib decoder, never
    retains more than one MiB of decompressed output, rejects every byte after
    that decoder reaches EOF, and restores the shared descriptor to offset 0.
    """
    need(name == os.path.basename(name), "direct gzip candidate name")
    need(
        expected_decompressed_bytes > 0
        and 0 < input_chunk_bytes <= RAW_GZIP_INPUT_CHUNK_BYTES
        and 0 < output_chunk_bytes <= RAW_GZIP_OUTPUT_CHUNK_BYTES,
        "bounded raw gzip validation parameters:" + name,
    )
    opened = os.fstat(descriptor)
    named = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
    need(
        stat_identity(opened) == stat_identity(named) == stat_identity(before),
        "candidate gzip raw pre-scan fd/name binding:" + name,
    )
    need(os.lseek(descriptor, 0, os.SEEK_CUR) == 0,
         "candidate gzip raw pre-scan offset zero:" + name)

    decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
    compressed_bytes = 0
    decompressed_bytes = 0
    unconsumed_tail_drain_count = 0
    try:
        while True:
            block = os.read(descriptor, input_chunk_bytes)
            if not block:
                break
            compressed_bytes += len(block)
            need(compressed_bytes <= before.st_size,
                 "candidate gzip raw scan bounded:" + name)
            need(not decoder.eof,
                 "candidate gzip second member or trailing bytes:" + name)
            pending = block
            while pending:
                previous = len(pending)
                output = decoder.decompress(pending, output_chunk_bytes)
                decompressed_bytes += len(output)
                need(
                    decompressed_bytes <= expected_decompressed_bytes,
                    "candidate gzip decompressed exact-size cap:" + name,
                )
                if decoder.eof:
                    need(not decoder.unused_data,
                         "candidate gzip second member or trailing bytes:" + name)
                    need(not decoder.unconsumed_tail,
                         "candidate gzip EOF unconsumed compressed bytes:" + name)
                    pending = b""
                else:
                    pending = decoder.unconsumed_tail
                    if pending:
                        unconsumed_tail_drain_count += 1
                    need(
                        bool(output) or len(pending) < previous,
                        "candidate gzip decoder forward progress:" + name,
                    )
    except zlib.error as error:
        raise VerificationBlocked("candidate gzip invalid or corrupt:" + name) from error

    need(compressed_bytes == before.st_size,
         "candidate gzip raw scan exact size:" + name)
    need(decoder.eof, "candidate gzip truncated member:" + name)
    need(not decoder.unused_data,
         "candidate gzip second member or trailing bytes:" + name)
    need(not decoder.unconsumed_tail,
         "candidate gzip final unconsumed compressed bytes:" + name)
    need(
        decompressed_bytes == expected_decompressed_bytes,
        "candidate gzip exact canonical uncompressed wire size:" + name,
    )
    after = os.fstat(descriptor)
    named_after = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
    need(
        stat_identity(after) == stat_identity(named_after) == stat_identity(before),
        "candidate gzip raw post-scan fd/name binding:" + name,
    )
    need(os.lseek(descriptor, 0, os.SEEK_CUR) == before.st_size,
         "candidate gzip raw post-scan offset EOF:" + name)
    os.lseek(descriptor, 0, os.SEEK_SET)
    need(os.lseek(descriptor, 0, os.SEEK_CUR) == 0,
         "candidate gzip raw reset offset zero:" + name)
    return {
        "compressed_bytes": compressed_bytes,
        "decompressed_bytes": decompressed_bytes,
        "unconsumed_tail_drain_count": unconsumed_tail_drain_count,
    }


def compare_candidate_ledger(
    candidate_fd: int,
    kind: str,
    expected: ExpectedLedger,
) -> None:
    name = FILES[kind]
    descriptor = os.open(
        name, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=candidate_fd,
    )
    raw: BinaryIO | None = None
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
        wire_contract = expected_ledger_wire_contract(kind, expected)
        validate_single_gzip_member_at(
            candidate_fd,
            descriptor,
            name,
            before,
            wire_contract["uncompressed_bytes"],
        )
        raw = os.fdopen(descriptor, "rb", buffering=0, closefd=False)
        zipped = gzip.GzipFile(fileobj=raw, mode="rb")
        text = io.TextIOWrapper(zipped, encoding="utf-8", newline="")
        marker = wire_contract["marker_wire"].decode("ascii")
        prelude = ""
        while marker not in prelude:
            block = text.read(CANDIDATE_TEXT_CHUNK_CHARACTERS)
            need(bool(block), "candidate ledger table marker:" + kind)
            prelude += block
            need(
                len(prelude)
                <= len(wire_contract["envelope_wire"])
                + len(marker)
                + CANDIDATE_TEXT_CHUNK_CHARACTERS,
                "bounded candidate ledger header",
            )
        need(prelude.count(marker) == 1, "unique candidate ledger marker")
        prefix, initial = prelude.split(marker, 1)
        envelope = strict_object((prefix + "}").encode("utf-8"), kind + " envelope")
        need(envelope == ledger_envelope(kind, expected), "exact ledger envelope:" + kind)
        need(
            (prefix + "}").encode("utf-8") == wire_contract["envelope_wire"],
            "exact canonical ledger envelope wire:" + kind,
        )
        expected_lines = iter(expected.expected_lines())
        observed_count = 0
        for row in iter_exact_candidate_array(
            text,
            initial,
            wire_contract["maximum_candidate_token_characters"],
        ):
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
        need(os.lseek(descriptor, 0, os.SEEK_CUR) == before.st_size,
             "candidate gzip JSON parse consumed exact raw fd:" + kind)
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
        if raw is not None and not raw.closed:
            raw.close()
        os.close(descriptor)


def expected_result(
    ledgers: dict[str, ExpectedLedger],
    audit: dict[str, Any],
    hashes: dict[str, str],
) -> dict[str, Any]:
    output_ledgers: dict[str, Any] = {}
    for kind in ("cell", "member", "gap"):
        envelope = ledger_envelope(kind, ledgers[kind])
        output_ledgers[kind] = {
            "filename": FILES[kind],
            "file_sha256": hashes[FILES[kind]],
            **ledgers[kind].metadata(),
            "ledger_sha256": envelope["ledger_sha256"],
        }
    payload = {
        "schema": SCHEMA,
        "status": "PRIVATE_ZERO_CREDIT_R288_SOURCE_INVENTORY_AND_UNION_FREEZE_CANDIDATE",
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
        for kind in ("cell", "member", "gap"):
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
    need(
        set(value) == {
            "atom_identities", "source_partition_rows", "existing_208",
            "aliases_204", "new_members", "source_cells", "multiplicity_one",
            "multiplicity_two", "R269", "R270", "R271", "R272",
            "cell_gaps", "member_gaps", "full_support_credit",
            "maximality_credit", "fibre_credit", "global_credit",
            "official_key_filter", "D02", "CM2",
        },
        "semantic exact key set",
    )
    need(value["atom_identities"] == 332_016, "semantic identity denominator")
    need(value["source_partition_rows"] == 332_020, "semantic source denominator")
    need(
        value["existing_208"] == 36_040 and value["aliases_204"] == 640
        and value["new_members"] == 295_336,
        "semantic identity partition",
    )
    need(
        value["existing_208"] + value["aliases_204"] + value["new_members"]
        == value["atom_identities"],
        "semantic identities close",
    )
    need(
        value["source_cells"] == 295_340
        and value["existing_208"] + value["aliases_204"] + value["source_cells"]
        == value["source_partition_rows"],
        "semantic source-side partition closes",
    )
    need(
        value["multiplicity_one"] == 295_332
        and value["multiplicity_two"] == 4
        and value["multiplicity_one"] + value["multiplicity_two"] == value["new_members"]
        and value["multiplicity_one"] + 2 * value["multiplicity_two"] == value["source_cells"],
        "semantic W-tail multiplicity",
    )
    need(
        (value["R269"], value["R270"], value["R271"], value["R272"])
        == (187_128, 37_712, 70_356, 144)
        and value["R269"] + value["R270"] + value["R271"] + value["R272"]
        == value["source_cells"],
        "semantic source round partition",
    )
    need(
        value["cell_gaps"] == 295_340 and value["member_gaps"] == 295_336,
        "semantic exact gap counts",
    )
    need(
        value["full_support_credit"] == value["maximality_credit"]
        == value["fibre_credit"] == value["global_credit"] == 0,
        "semantic zero-credit boundary",
    )
    need(
        value["official_key_filter"] is False
        and value["D02"] == "BLOCKED" and value["CM2"] == "NO-GO_FOR_CLAIM",
        "semantic routing and downstream boundary",
    )


def semantic_baseline() -> dict[str, Any]:
    return {
        "atom_identities": 332_016,
        "source_partition_rows": 332_020,
        "existing_208": 36_040,
        "aliases_204": 640,
        "new_members": 295_336,
        "source_cells": 295_340,
        "multiplicity_one": 295_332,
        "multiplicity_two": 4,
        "R269": 187_128,
        "R270": 37_712,
        "R271": 70_356,
        "R272": 144,
        "cell_gaps": 295_340,
        "member_gaps": 295_336,
        "full_support_credit": 0,
        "maximality_credit": 0,
        "fibre_credit": 0,
        "global_credit": 0,
        "official_key_filter": False,
        "D02": "BLOCKED",
        "CM2": "NO-GO_FOR_CLAIM",
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


def transaction_attack_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="cm2-b1r0-verifier-selftest-") as temporary:
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
        finally:
            os.close(fd)
    return rows


def exercise_raw_gzip_fixture(
    raw_bytes: bytes,
    expected_decompressed_bytes: int,
    *,
    input_chunk_bytes: int = RAW_GZIP_INPUT_CHUNK_BYTES,
    output_chunk_bytes: int = RAW_GZIP_OUTPUT_CHUNK_BYTES,
) -> dict[str, int]:
    need(type(raw_bytes) is bytes and bool(raw_bytes), "nonempty raw gzip fixture")
    with tempfile.TemporaryDirectory(prefix="cm2-b1r0-gzip-selftest-") as temporary:
        directory_fd = os.open(
            temporary, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
        )
        descriptor = -1
        try:
            descriptor = os.open(
                "fixture.gz", os.O_RDWR | os.O_CREAT | os.O_EXCL,
                0o600, dir_fd=directory_fd,
            )
            remaining = memoryview(raw_bytes)
            while remaining:
                written = os.write(descriptor, remaining)
                need(written > 0, "raw gzip fixture write progress")
                remaining = remaining[written:]
            os.fsync(descriptor)
            before = os.fstat(descriptor)
            need(
                stat.S_ISREG(before.st_mode)
                and stat.S_IMODE(before.st_mode) == 0o600
                and before.st_nlink == 1
                and before.st_size == len(raw_bytes),
                "raw gzip fixture exact file",
            )
            os.lseek(descriptor, 0, os.SEEK_SET)
            result = validate_single_gzip_member_at(
                directory_fd,
                descriptor,
                "fixture.gz",
                before,
                expected_decompressed_bytes,
                input_chunk_bytes=input_chunk_bytes,
                output_chunk_bytes=output_chunk_bytes,
            )
            need(os.lseek(descriptor, 0, os.SEEK_CUR) == 0,
                 "raw gzip fixture validator restored offset")
            return result
        finally:
            if descriptor >= 0:
                os.close(descriptor)
            os.close(directory_fd)


def wire_attack_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    legal_payload = b'{"rows":[{"a":1}]}'
    legal_member = gzip.compress(legal_payload, mtime=0)
    legal_result = exercise_raw_gzip_fixture(legal_member, len(legal_payload))
    need(
        legal_result["compressed_bytes"] == len(legal_member)
        and legal_result["decompressed_bytes"] == len(legal_payload),
        "single legal gzip member accepted exactly",
    )
    boundary_result = exercise_raw_gzip_fixture(
        legal_member,
        len(legal_payload),
        input_chunk_bytes=len(legal_member),
    )
    need(
        boundary_result["compressed_bytes"] == legal_result["compressed_bytes"]
        and boundary_result["decompressed_bytes"] == legal_result["decompressed_bytes"],
         "single legal gzip member ending at raw chunk boundary")
    drain_payload = b"unconsumed-tail-drain:" + b"x" * 4096
    drain_member = gzip.compress(drain_payload, mtime=0)
    drain_result = exercise_raw_gzip_fixture(
        drain_member,
        len(drain_payload),
        input_chunk_bytes=min(len(drain_member), 31),
        output_chunk_bytes=7,
    )
    need(
        drain_result["decompressed_bytes"] == len(drain_payload)
        and drain_result["unconsumed_tail_drain_count"] > 0,
        "raw gzip unconsumed-tail drain accepted exactly",
    )
    synthetic = ExpectedLedger("cell")
    try:
        synthetic_row = synthetic.append({
            ID_FIELDS["cell"]: "round306b1r0-selftest-synthetic-row",
        })
        synthetic_contract = expected_ledger_wire_contract("cell", synthetic)
        synthetic_wire = (
            synthetic_contract["envelope_wire"][:-1]
            + synthetic_contract["marker_wire"]
            + canonical(synthetic_row)
            + b"]}"
        )
        need(
            len(synthetic_wire) == synthetic_contract["uncompressed_bytes"],
            "independent canonical ledger wire-size formula",
        )
        synthetic_result = exercise_raw_gzip_fixture(
            gzip.compress(synthetic_wire, mtime=0), len(synthetic_wire)
        )
        need(
            synthetic_result["decompressed_bytes"] == len(synthetic_wire),
            "independent canonical ledger wire-size positive fixture",
        )
    finally:
        synthetic.close()

    def flipped(raw_bytes: bytes, index: int) -> bytes:
        return (
            raw_bytes[:index]
            + bytes((raw_bytes[index] ^ 1,))
            + raw_bytes[index + 1:]
        )

    raw_gzip_attacks: tuple[tuple[str, bytes, int, int, int], ...] = (
        (
            "candidate_second_empty_gzip_member",
            legal_member + gzip.compress(b"", mtime=0),
            len(legal_payload),
            RAW_GZIP_INPUT_CHUNK_BYTES,
            RAW_GZIP_OUTPUT_CHUNK_BYTES,
        ),
        (
            "candidate_second_whitespace_gzip_member",
            legal_member + gzip.compress(b" \n\t", mtime=0),
            len(legal_payload),
            RAW_GZIP_INPUT_CHUNK_BYTES,
            RAW_GZIP_OUTPUT_CHUNK_BYTES,
        ),
        (
            "candidate_second_JSON_gzip_member",
            legal_member + gzip.compress(b'{"evil":1}', mtime=0),
            len(legal_payload),
            RAW_GZIP_INPUT_CHUNK_BYTES,
            RAW_GZIP_OUTPUT_CHUNK_BYTES,
        ),
        (
            "candidate_raw_trailing_garbage",
            legal_member + b"raw-trailing-garbage",
            len(legal_payload),
            RAW_GZIP_INPUT_CHUNK_BYTES,
            RAW_GZIP_OUTPUT_CHUNK_BYTES,
        ),
        (
            "candidate_raw_trailing_NUL_padding",
            legal_member + b"\x00\x00",
            len(legal_payload),
            RAW_GZIP_INPUT_CHUNK_BYTES,
            RAW_GZIP_OUTPUT_CHUNK_BYTES,
        ),
        (
            "candidate_corrupt_gzip_CRC32",
            flipped(legal_member, len(legal_member) - 8),
            len(legal_payload),
            RAW_GZIP_INPUT_CHUNK_BYTES,
            RAW_GZIP_OUTPUT_CHUNK_BYTES,
        ),
        (
            "candidate_corrupt_gzip_ISIZE",
            flipped(legal_member, len(legal_member) - 4),
            len(legal_payload),
            RAW_GZIP_INPUT_CHUNK_BYTES,
            RAW_GZIP_OUTPUT_CHUNK_BYTES,
        ),
        (
            "candidate_truncated_gzip_header",
            legal_member[:9],
            len(legal_payload),
            RAW_GZIP_INPUT_CHUNK_BYTES,
            RAW_GZIP_OUTPUT_CHUNK_BYTES,
        ),
        (
            "candidate_truncated_gzip_deflate_body",
            legal_member[:len(legal_member) // 2],
            len(legal_payload),
            RAW_GZIP_INPUT_CHUNK_BYTES,
            RAW_GZIP_OUTPUT_CHUNK_BYTES,
        ),
        (
            "candidate_truncated_gzip_before_CRC32",
            legal_member[:-8],
            len(legal_payload),
            RAW_GZIP_INPUT_CHUNK_BYTES,
            RAW_GZIP_OUTPUT_CHUNK_BYTES,
        ),
        (
            "candidate_truncated_gzip_ISIZE",
            legal_member[:-1],
            len(legal_payload),
            RAW_GZIP_INPUT_CHUNK_BYTES,
            RAW_GZIP_OUTPUT_CHUNK_BYTES,
        ),
        (
            "candidate_second_member_at_raw_chunk_boundary",
            legal_member + gzip.compress(b"", mtime=0),
            len(legal_payload),
            len(legal_member),
            RAW_GZIP_OUTPUT_CHUNK_BYTES,
        ),
        (
            "candidate_trailing_byte_at_raw_chunk_boundary",
            legal_member + b"X",
            len(legal_payload),
            len(legal_member),
            RAW_GZIP_OUTPUT_CHUNK_BYTES,
        ),
        (
            "candidate_decompressed_exact_size_cap_exceeded",
            legal_member,
            len(legal_payload) - 1,
            RAW_GZIP_INPUT_CHUNK_BYTES,
            3,
        ),
        (
            "candidate_decompressed_exact_size_underflow",
            legal_member,
            len(legal_payload) + 1,
            RAW_GZIP_INPUT_CHUNK_BYTES,
            RAW_GZIP_OUTPUT_CHUNK_BYTES,
        ),
    )
    rows: list[dict[str, Any]] = []
    for name, raw_bytes, expected_bytes, input_chunk, output_chunk in raw_gzip_attacks:
        need(
            rejected(
                lambda raw_bytes=raw_bytes, expected_bytes=expected_bytes,
                input_chunk=input_chunk, output_chunk=output_chunk:
                exercise_raw_gzip_fixture(
                    raw_bytes,
                    expected_bytes,
                    input_chunk_bytes=input_chunk,
                    output_chunk_bytes=output_chunk,
                )
            ),
            "raw gzip attack rejected:" + name,
        )
        rows.append(close_row({
            "attack_name": name,
            "attack_class": "STRICT_RAW_SINGLE_GZIP_MEMBER",
            "expected": "REJECT",
            "observed": "REJECT",
        }))

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
            "candidate_giant_unclosed_row_token",
            lambda: list(iter_exact_candidate_array(
                io.StringIO("x" * 512),
                '{"a":"',
                maximum_token_characters=128,
                text_chunk_characters=32,
            )),
        ),
    )
    for name, callback in attacks:
        need(rejected(callback), "wire attack rejected:" + name)
        rows.append(close_row({
            "attack_name": name,
            "attack_class": "STRICT_WIRE_GRAMMAR",
            "expected": "REJECT",
            "observed": "REJECT",
        }))
    return rows, {
        "single_gzip_member_enforced": True,
        "raw_streaming_validation_before_JSON_parse": True,
        "maximum_retained_decompressed_chunk_bytes": RAW_GZIP_OUTPUT_CHUNK_BYTES,
        "exact_decompressed_wire_size_required": True,
        "candidate_row_token_buffer_bounded": True,
        "positive_fixture_count": 4,
        "negative_fixture_count": len(raw_gzip_attacks),
        "negative_fixture_rejected_count": len(raw_gzip_attacks),
        "raw_gzip_fixture_count": 4 + len(raw_gzip_attacks),
        "independent_ledger_wire_size_positive_fixture_count": 1,
        "giant_unclosed_row_negative_fixture_count": 1,
        "fixture_count": 5 + len(raw_gzip_attacks),
    }


def build_attack_suite(
    candidate_file_sha256s: dict[str, str] | None,
    verifier_sha256: str,
) -> dict[str, Any]:
    baseline = semantic_baseline()
    semantic_contract(baseline)
    mutations: tuple[tuple[str, str, Any], ...] = (
        ("identity_denominator_forgery", "atom_identities", 332_020),
        ("source_denominator_forgery", "source_partition_rows", 332_016),
        ("Round208_count_forgery", "existing_208", 36_039),
        ("Round204_alias_count_forgery", "aliases_204", 641),
        ("new_member_count_forgery", "new_members", 295_340),
        ("source_cell_count_forgery", "source_cells", 295_336),
        ("multiplicity_two_forgery", "multiplicity_two", 0),
        ("Round269_count_forgery", "R269", 187_127),
        ("Round270_count_forgery", "R270", 37_713),
        ("Round271_count_forgery", "R271", 70_352),
        ("Round272_count_forgery", "R272", 148),
        ("cell_gap_drop", "cell_gaps", 0),
        ("member_gap_drop", "member_gaps", 0),
        ("full_support_credit_forgery", "full_support_credit", 1),
        ("maximality_credit_forgery", "maximality_credit", 1),
        ("fibre_credit_forgery", "fibre_credit", 124),
        ("global_credit_forgery", "global_credit", 224_580),
        ("official_key_filter_forgery", "official_key_filter", True),
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
    grammar_rows, raw_gzip_fixtures = wire_attack_rows()
    rows = semantic_rows + filesystem_rows + grammar_rows
    payload = {
        "schema": SCHEMA + ".attack-suite.v1",
        "status": "PASS_ROUND306B1R0_FAIL_CLOSED_DEFENSE_IN_DEPTH_ATTACKS",
        "binding_mode": (
            "EXACT_PRIVATE_CANDIDATE" if candidate_file_sha256s is not None
            else "LIGHTWEIGHT_BLOCKED_SCAFFOLD_SELF_TEST"
        ),
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
        "raw_single_gzip_member_fixtures": raw_gzip_fixtures,
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
        "status": "PASS_EXACT_ROUND306B1R0_R288_PREDICATE_SOURCE_INVENTORY_AND_UNION_FREEZE__ZERO_THEOREM_CREDIT",
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
        },
        "independent_reconstruction": {
            "Round288_atom_identity_count": 332_016,
            "identity_partition": {
                "existing_Round208": 36_040,
                "Round204_exact_alias": 640,
                "new_Round288_member": 295_336,
            },
            "source_side_partition_row_count": 332_020,
            "source_side_partition_explanation":
                "36040 existing plus 640 aliases plus 295340 predicate cells; four additional cells are artificial W-tail splits, not identities",
            "new_member_count": 295_336,
            "new_predicate_source_cell_count": 295_340,
            "source_multiplicity": {"1": 295_332, "2": 4},
            "source_round_counts": {
                "269": 187_128, "270": 37_712, "271": 70_356, "272": 144,
            },
            "Round271_W_tail_parent_normalization_count": 4,
            "cell_gap_count": 295_340,
            "member_union_gap_count": 295_336,
            "total_gap_count": 590_676,
            "audit": audit,
            "producer_code_used_for_reconstruction": False,
        },
        "candidate": {
            "dedicated_private_root": PRIVATE_ROOT.name,
            "exact_four_file_set": list(CANDIDATE_ORDER),
            "exact_file_sha256s": dict(sorted(hashes.items())),
            "result_self_sha256": result["result_sha256"],
            "candidate_opened_only_after_full_independent_reconstruction": True,
            "all_295340_cell_rows_equal_reconstruction": True,
            "all_295336_member_rows_equal_reconstruction": True,
            "all_590676_gap_rows_equal_reconstruction": True,
            "strict_gzip_and_JSON_grammar": True,
            "exactly_one_complete_raw_gzip_member_per_ledger": True,
            "raw_gzip_validation_streaming_before_JSON_parse": True,
            "raw_gzip_trailing_bytes_and_truncation_rejected": True,
            "raw_gzip_decompressed_size_equals_independent_canonical_wire_size": True,
            "candidate_row_token_buffer_bounded_by_independent_maximum_row": True,
            "raw_gzip_fd_name_identity_and_offsets_rechecked": True,
            "mode600_nlink1_inode_stability_required": True,
        },
        "attack_suite": {
            "filename": ATTACK,
            "file_sha256": hashlib.sha256(canonical(attacks)).hexdigest(),
            "object_self_sha256": attacks["attack_suite_sha256"],
            "attack_count": attacks["attack_count"],
            "rejected_count": attacks["rejected_count"],
            "wire_attack_count": attacks["wire_attack_count"],
            "raw_single_gzip_member_fixtures": attacks[
                "raw_single_gzip_member_fixtures"
            ],
            "all_rejected": True,
        },
        "formal_credit_without_this_verification_marker": {
            "full_support": 0,
            "maximality": 0,
            "fibre": 0,
            "global_disposition": 0,
        },
        "formal_credit_transition_at_this_verification_marker": {
            "full_support": 0,
            "maximality": 0,
            "fibre": 0,
            "global_disposition": 0,
        },
        "strict_downstream_boundary": strict_boundary(),
        "atomic_publication": {
            "promotion_order": list(PROMOTION_ORDER),
            "attack_first": True,
            "verification_last_and_sole_package_marker": True,
            "verification_marker_grants_theorem_credit": False,
            "renameat2_RENAME_NOREPLACE": True,
            "stage_and_output_directory_fsync_after_each_rename": True,
            "exact_prefix_recovery_only": True,
            "no_clobber": True,
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
        states: list[bool] = []
        seen_absent = False
        for name in PROMOTION_ORDER:
            try:
                info = os.stat(name, dir_fd=data_fd, follow_symlinks=False)
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
            need(stage_hash_at(data_fd, name) == expected_hashes[name],
                 "formal prefix exact hash:" + name)
            states.append(True)
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
                try:
                    current = os.stat(VERIFICATION, dir_fd=data_fd, follow_symlinks=False)
                except FileNotFoundError:
                    pass
                else:
                    if (
                        (current.st_dev, current.st_ino) == marker_identity
                        and stage_hash_at(data_fd, VERIFICATION)
                        == expected_hashes[VERIFICATION]
                    ):
                        os.unlink(VERIFICATION, dir_fd=data_fd)
                        os.fsync(data_fd)
            raise
    finally:
        if stage_fd >= 0:
            os.close(stage_fd)
        try:
            fcntl.flock(data_fd, fcntl.LOCK_UN)
        finally:
            os.close(data_fd)


def contract() -> dict[str, Any]:
    return {
        "schema": SCHEMA + ".independent-verifier-contract.v1",
        "status": (
            "READY_FOR_HEAVY_INDEPENDENT_RECONSTRUCTION_AND_PRIVATE_CANDIDATE_ADMISSION"
            if AUDIT_AUTHORIZED
            else "IMPLEMENTED_BUT_HOSTILE_AUDIT_AUTHORIZATION_FALSE__HEAVY_RECONSTRUCTION_CANDIDATE_AND_PROMOTION_HARD_BLOCKED"
        ),
        "implementation_present": True,
        "audit_authorized": AUDIT_AUTHORIZED,
        "hard_gate": {
            "checked_before_any_large_source_open": True,
            "checked_before_candidate_path_lstat_or_open": True,
            "checked_before_any_candidate_or_formal_write": True,
            "candidate_admission_enabled": AUDIT_AUTHORIZED,
            "promotion_enabled": AUDIT_AUTHORIZED,
        },
        "independence": {
            "producer_filename": PRODUCER,
            "producer_file_sha256": EXPECTED_PRODUCER_SHA256,
            "producer_file_size": EXPECTED_PRODUCER_SIZE,
            "producer_treated_as_inert_bytes_only": True,
            "producer_imported_executed_parsed_or_tokenized": False,
            "reconstruction_written_in_verifier": True,
            "candidate_opened_only_after_independent_reconstruction": True,
        },
        "exact_expected": dict(EXPECTED),
        "identity_vs_source_denominator_boundary": {
            "Round288_atom_identities": 332_016,
            "source_side_partition_rows": 332_020,
            "difference": 4,
            "difference_is_exactly_four_W_tail_artificial_split_cells": True,
            "difference_is_not_extra_identities": True,
        },
        "source_pins": {
            name: {"file_sha256": pin[0], "file_size": pin[1]}
            for name, pin in sorted(SOURCE_PINS.items())
        },
        "candidate_contract": {
            "dedicated_private_root": PRIVATE_ROOT.name,
            "exact_files": list(CANDIDATE_ORDER),
            "strict_JSON_duplicate_float_nonfinite_and_comma_rejection": True,
            "deterministic_gzip_header_required": True,
            "exactly_one_complete_raw_gzip_member_required": True,
            "second_empty_whitespace_or_nonempty_gzip_member_rejected": True,
            "raw_trailing_bytes_and_truncated_gzip_rejected": True,
            "raw_gzip_validation_streaming_before_JSON_parse": True,
            "maximum_retained_decompressed_validation_chunk_bytes":
                RAW_GZIP_OUTPUT_CHUNK_BYTES,
            "exact_independently_reconstructed_uncompressed_wire_size_required": True,
            "candidate_row_token_buffer_bounded_by_expected_maximum_row": True,
            "candidate_text_read_chunk_characters": CANDIDATE_TEXT_CHUNK_CHARACTERS,
            "candidate_token_fixed_syntax_margin_characters":
                CANDIDATE_TOKEN_SYNTAX_MARGIN_CHARACTERS,
            "raw_gzip_fd_name_identity_and_offsets_rechecked": True,
            "regular_mode600_nlink1_required": True,
            "directory_and_file_inode_stability_required": True,
            "every_row_compared_to_independent_reconstruction": True,
        },
        "lightweight_raw_gzip_fixture_contract": {
            "single_legal_member_positive_fixtures": 1,
            "single_legal_member_at_raw_chunk_boundary_positive_fixtures": 1,
            "unconsumed_tail_drain_positive_fixtures": 1,
            "independent_ledger_wire_size_positive_fixtures": 1,
            "second_empty_member_negative_fixtures": 1,
            "second_whitespace_member_negative_fixtures": 1,
            "second_JSON_member_negative_fixtures": 1,
            "raw_trailing_garbage_negative_fixtures": 1,
            "raw_trailing_NUL_padding_negative_fixtures": 1,
            "CRC32_corruption_negative_fixtures": 1,
            "ISIZE_corruption_negative_fixtures": 1,
            "truncated_header_negative_fixtures": 1,
            "truncated_deflate_negative_fixtures": 1,
            "truncated_before_CRC32_negative_fixtures": 1,
            "truncated_ISIZE_negative_fixtures": 1,
            "second_member_at_raw_chunk_boundary_negative_fixtures": 1,
            "trailing_byte_at_raw_chunk_boundary_negative_fixtures": 1,
            "decompressed_exact_size_cap_exceeded_negative_fixtures": 1,
            "decompressed_exact_size_underflow_negative_fixtures": 1,
            "giant_unclosed_row_token_negative_fixtures": 1,
        },
        "publication_contract": {
            "promotion_order": list(PROMOTION_ORDER),
            "attack_first": True,
            "verification_last": True,
            "verification_is_sole_package_marker": True,
            "verification_grants_theorem_credit": False,
            "exact_committed_prefix_recovery": True,
            "renameat2_noreplace": True,
            "precise_owned_marker_rollback": True,
        },
        "strict_zero_credit_boundary": strict_boundary(),
        "known_unimplemented_or_residual_risks": {
            "SIGKILL_or_power_loss_orphan_stage_cleanup_automated": False,
            "same_uid_namespace_mutation_after_last_check_eliminated": False,
            "source_free_predicate_AST_materialized": False,
            "source_free_interval_equivalence_proved": False,
            "member_full_support_union_theorem_proved": False,
            "full_maximality_proved": False,
        },
    }


def self_test() -> dict[str, Any]:
    need(
        EXPECTED["existing_Round208_identities"]
        + EXPECTED["Round204_alias_identities"]
        + EXPECTED["new_member_identities"]
        == EXPECTED["Round288_atom_identities"],
        "identity partition arithmetic",
    )
    need(
        EXPECTED["existing_Round208_identities"]
        + EXPECTED["Round204_alias_identities"]
        + EXPECTED["new_predicate_source_cells"]
        == EXPECTED["source_side_partition_rows"],
        "source partition arithmetic",
    )
    need(
        EXPECTED["multiplicity_one_new_members"]
        + EXPECTED["multiplicity_two_new_members"]
        == EXPECTED["new_member_identities"]
        and EXPECTED["multiplicity_one_new_members"]
        + 2 * EXPECTED["multiplicity_two_new_members"]
        == EXPECTED["new_predicate_source_cells"],
        "multiplicity arithmetic",
    )
    need(
        sum(EXPECTED["Round" + str(number) + "_cells"] for number in (269, 270, 271, 272))
        == EXPECTED["new_predicate_source_cells"],
        "round arithmetic",
    )
    need(
        EXPECTED["cell_theorem_gaps"] + EXPECTED["member_union_theorem_gaps"]
        == EXPECTED["total_gaps"],
        "gap arithmetic",
    )
    need(
        HEX64.fullmatch(EXPECTED_PRODUCER_SHA256) is not None
        and EXPECTED_PRODUCER_SIZE > 0
        and all(HEX64.fullmatch(pin[0]) is not None and pin[1] > 0 for pin in SOURCE_PINS.values()),
        "pin syntax and positive sizes",
    )
    need(
        list(iter_array(io.StringIO('{"b":2}]'), "MARK", 'MARK{"a":1},'))
        == [{"a": 1}, {"b": 2}],
        "source parser comma at block boundary",
    )
    need(
        list(iter_array(io.StringIO('\n\t{"b":2}]'), "MARK", 'MARK{"a":1},   '))
        == [{"a": 1}, {"b": 2}],
        "source parser comma and whitespace across block boundary",
    )
    need(
        rejected(
            lambda: list(
                iter_array(io.StringIO(""), "MARK", 'MARK{"a":1},]')
            )
        ),
        "source parser true trailing comma rejected",
    )
    semantic_contract(semantic_baseline())
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
            "PASS_LIGHTWEIGHT_B1R0_INDEPENDENT_VERIFIER_CONTRACT_AND_ATTACKS__HEAVY_PATH_AUTHORIZED"
            if AUDIT_AUTHORIZED
            else "PASS_LIGHTWEIGHT_B1R0_INDEPENDENT_VERIFIER_CONTRACT_AND_ATTACKS__HEAVY_PATH_HARD_BLOCKED"
        ),
        "producer_file_sha256": producer_sha256,
        "runtime_verifier_file_sha256": verifier_sha256,
        "semantic_attack_count": attacks["semantic_attack_count"],
        "filesystem_attack_count": attacks["filesystem_attack_count"],
        "wire_attack_count": attacks["wire_attack_count"],
        "raw_single_gzip_member_fixtures": attacks[
            "raw_single_gzip_member_fixtures"
        ],
        "attack_count": attacks["attack_count"],
        "rejected_count": attacks["rejected_count"],
        "all_rejected": True,
        "identity_denominator_regression": 332_016,
        "source_side_denominator_regression": 332_020,
        "source_stream_parser_positive_boundary_regressions": 2,
        "source_stream_parser_true_trailing_comma_rejected": True,
        "large_source_opened": False,
        "candidate_path_opened": False,
        "candidate_or_formal_artifact_written": False,
        "audit_authorized": AUDIT_AUTHORIZED,
        "formal_full_support_credit": 0,
        "formal_maximality_credit": 0,
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
    need(
        AUDIT_AUTHORIZED,
        "candidate/promotion mode blocked before any large source or candidate open and before any write: hostile audit authorization is false",
    )
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
                "status": "PASS_EXACT_B1R0_PRIVATE_CANDIDATE_ADMISSION__ZERO_FORMAL_THEOREM_CREDIT",
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
