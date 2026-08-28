#!/usr/bin/env python3
"""Independent cold verifier for the strict K2I1 R2 mechanical lane.

The producer is byte-pinned but never imported or executed.  This verifier
independently reparses every raw table, reconstructs all identity, owner, and
representation joins in an ephemeral SQLite database, and compares every
emitted ledger row with an independently generated expected row.
"""

from __future__ import annotations

import argparse
from collections import Counter
from contextlib import ExitStack
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import re
import sqlite3
import stat
import tempfile
from typing import Any, BinaryIO, Iterable, Iterator, TextIO


class VerificationBlocked(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationBlocked(label)


def type_strict_equal(actual: Any, expected: Any) -> bool:
    if type(actual) is not type(expected):
        return False
    if type(actual) is dict:
        return set(actual) == set(expected) and all(type_strict_equal(actual[key], expected[key]) for key in expected)
    if type(actual) in (list, tuple):
        return len(actual) == len(expected) and all(type_strict_equal(left, right) for left, right in zip(actual, expected))
    return bool(actual == expected)


def strict_need(actual: Any, expected: Any, label: str) -> None:
    need(type_strict_equal(actual, expected), label)


PREFIX = "cm2_round306b1af4k2i1_source_g_r2_identity_representation_index_"
SCHEMA = "cm2.round306b1af4k2i1.source-g-r2-identity-representation-index.v1"
EXPECTED_STATUS = "PASS_EXACT_R2_MECHANICAL_IDENTITY_REPRESENTATION_INDEX__ZERO_THEOREM_CREDIT"
DELIVERABLES = Path(__file__).resolve().parent
PRODUCER = PREFIX + "producer.py"
PRODUCER_SIZE = 48_923
PRODUCER_SHA256 = "9cc1bd314fcdce477b8376a29ed533f7894aaa31f0295b0f9221074bce9102d7"
RESULT = PREFIX + "result.json"
VERIFICATION = PREFIX + "verification.json"
OUTPUTS = {
    "member": PREFIX + "member_index.jsonl.gz",
    "representation": PREFIX + "representation_index.jsonl.gz",
    "wtail_gap": PREFIX + "wtail_blocked_obligation_index.jsonl.gz",
}
HEX64 = re.compile(r"^[0-9a-f]{64}$")
MAX_ROW = 8 << 20
CHARS = 1 << 18
BUFFER_CAP = MAX_ROW + 4 * CHARS

RAW_PINS: tuple[tuple[str, str, int, str], ...] = (
    ("AF2_RESULT", "cm2_round306b1af2_source_g_primitive_support_source_partition_primary_result.json", 2_540, "7238c245e79124e5bf3aa14c463fcc639efcde7431b03ac3a1cd035a4d1f7ebb"),
    ("AF4_TYPED_SCHEMA", "cm2_round306b1af4_source_g_normalized_support_representation_typed_schema_contract.py", 80_436, "ee095fe5db22c6a4dd0804eca0fb553a132546367dcb37fcd75733050aa52cf9"),
    ("AF4D1_SEMANTIC_DELTA", "cm2_round306b1af4d1_source_g_semantic_wire_delta_contract.py", 84_392, "5082df54ea4c514de906f4a923856adb20c6240c9be33401e784b2513a85f09f"),
    ("R287", "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_ledger.json.gz", 7_529_109, "29838e3e6b33f03bf623bbce8b87e6ba5c3306e66beb0b6634496503fb9a4f9a"),
    ("R288", "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_atom_dispositions.json.gz", 134_114_861, "6b0a8aa1cd38019322a61f5aaefc936006d10769cd21a5c8df374576f9ac570a"),
    ("R294_REGISTRY", "cm2_round294_source_g_occurrence_registry_atomic_promotion_registry_ledger.json.gz", 262_951_902, "c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb"),
    ("R294_BINDINGS", "cm2_round294_source_g_occurrence_registry_atomic_promotion_representation_binding_ledger.json.gz", 26_672_326, "f9fcc986771b1c3551420516cd9f2c5dde662f87d044666d9306404f30bb6833"),
    ("B0", "cm2_round306b0_source_g_r306a_universe_support_source_freeze_member_support_source_index.json.gz", 162_499_140, "c9a8649c8473bb6a170187e7f803e95748d2ff2198b1b846d97383dd5f0581af"),
    ("B1R0_CELLS", "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_predicate_source_cell.json.gz", 105_989_322, "19d13d93fc02296f673ca18cc2edbd96174985f7be8fb0e03694582b188b0f96"),
    ("B1R0_MEMBERS", "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_member_union.json.gz", 123_019_951, "4b3633782e4514f598cb9cce19930ba31616f7d42aab002df4f77f9b4601ddf7"),
)

EXPECTED_TABLES: dict[str, tuple[int, str]] = {
    "R287_REGION": (13_788, "7d07e90c481b1c511ccce1d56df67f95140aa8d9b5cf5ea30b1d962ace5d8765"),
    "R287_REFINEMENT": (7_616, "951e8d912a4bf9494c928fbbdc99663485c019cee79580df98f838e0157555c9"),
    "R288": (332_016, "8007b0c96e44c76bea6038fed8430134f9f424c7a81508f843d72d473f768849"),
    "R294_REGISTRY": (431_208, "33936ecd04cbce9f9a308b0da10381bd854b45028db53db5d3cbb9aa8b264044"),
    "R294_BINDINGS": (46_288, "ece198bf5e8b95448b09f60061677feafca3416525ba80f3b88a51e766414be7"),
    "B0": (564_492, "c7dfb5534fddeb22fffb81bf539fe44d837aced46577aa5f490a0ae14aba77f5"),
    "B1R0_CELLS": (295_340, "b89220807eef10bc8412be19c5037ea75fa3c6fdf4321c27938afec0c68c9246"),
    "B1R0_MEMBERS": (295_336, "6665fc8e72824fba7dbd1d1b7462ae419bb31c25149037da3183d74569b62a3d"),
}

ZERO_MEMBER_CREDIT = {"normalized_support": 0, "representation_cover": 0, "physical_incidence": 0, "A1_A2": 0, "B1A": 0, "B2": 0, "D02": 0, "CM2": 0}
ZERO_REPRESENTATION_CREDIT = {"normalized_support": 0, "representation_cover": 0, "physical_incidence": 0, "pullback_equivalence": 0, "B1A": 0, "B2": 0}
ZERO_GLOBAL_CREDIT = {"normalized_support": 0, "representation_cover": 0, "physical_incidence": 0, "pullback_equivalence": 0, "A1_A2": 0, "B1A": 0, "B2": 0, "maximality": 0, "fibre": 0, "global_disposition": 0, "D02": 0, "D03": 0, "D04": 0, "Gate5": 0, "CM2": 0}
EXPECTED_GAPS = {
    "R2_source_free_interval_predicate_equivalence_not_discharged": 295_336,
    "R2_W_tail_artificial_face_reglue_not_discharged_in_this_lane": 4,
    "R2_representation_handles_without_global_set_equality_theorem": 302_624,
    "remaining_coarse_families_not_emitted": ["PRESERVED", "NON_GRAPH", "R292", "G2A", "G2B"],
    "remaining_member_identity_rows_not_emitted": 269_156,
    "remaining_global_representation_rows_not_emitted": 309_280,
    "A1_A2_obligations_not_enumerated_in_this_lane": 80_092,
}
EXPECTED_ANTI_JOINS = {
    "cells_minus_member_edges": 0,
    "member_edges_minus_cells": 0,
    "members_minus_R294_registry": 0,
    "R294_registry_minus_R288_source": 0,
    "members_minus_B0": 0,
    "R2_aliases_minus_R287_source": 0,
    "R2_aliases_minus_R288_atom": 0,
    "R2_aliases_minus_member_owner": 0,
    "duplicate_member_ids": 0,
    "duplicate_representation_ids": 0,
    "orphan_owner_count": 0,
}


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in out, "duplicate JSON key:" + key)
        out[key] = value
    return out


def reject_number(token: str) -> Any:
    raise VerificationBlocked("nonintegral JSON token:" + token)


DECODER = json.JSONDecoder(object_pairs_hook=unique_object, parse_float=reject_number, parse_constant=reject_number)


def closed_hash(row: dict[str, Any], label: str) -> str:
    need(type(row) is dict and type(row.get("row_sha256")) is str, label + ":closed row")
    body = dict(row)
    claimed = body.pop("row_sha256")
    need(HEX64.fullmatch(claimed) is not None and digest(body) == claimed, label + ":row hash")
    return claimed


def close_row(body: dict[str, Any]) -> dict[str, Any]:
    return {**body, "row_sha256": digest(body)}


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


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink, value.st_size, value.st_mtime_ns, value.st_ctime_ns)


def directory_identity(value: os.stat_result) -> tuple[int, int, int]:
    return (value.st_dev, value.st_ino, value.st_mode)


def hash_fd(fd: int, limit: int) -> tuple[int, str]:
    total = 0
    offset = 0
    state = hashlib.sha256()
    while True:
        block = os.pread(fd, 1 << 20, offset)
        if not block:
            break
        total += len(block)
        offset += len(block)
        need(total <= limit, "file grew while hashing")
        state.update(block)
    return total, state.hexdigest()


def iter_array(stream: TextIO, marker: str) -> Iterator[Any]:
    def append(buffer: str, label: str) -> str:
        block = stream.read(CHARS)
        need(bool(block), label)
        result = buffer + block
        need(len(result.encode("utf-8")) <= BUFFER_CAP, "parser buffer cap")
        return result

    buffer = ""
    while True:
        at = buffer.find(marker)
        if at >= 0:
            buffer = buffer[at + len(marker):]
            break
        buffer = append(buffer, "missing marker:" + marker)
        at = buffer.find(marker)
        if at >= 0:
            buffer = buffer[at + len(marker):]
            break
        buffer = buffer[-max(1, len(marker) - 1):]
    stripped = buffer.lstrip()
    if stripped.startswith(":"):
        stripped = stripped[1:].lstrip()
        need(stripped.startswith("["), "marker not array")
        buffer = stripped[1:]
    comma = False
    while True:
        buffer = buffer.lstrip()
        while not buffer:
            buffer = append(buffer, "truncated array")
            buffer = buffer.lstrip()
        if buffer[0] == "]":
            return
        if comma:
            need(buffer[0] == ",", "missing comma")
            buffer = buffer[1:].lstrip()
            while not buffer:
                buffer = append(buffer, "truncated row")
                buffer = buffer.lstrip()
            need(buffer[0] != "]", "trailing comma")
        else:
            need(buffer[0] != ",", "leading comma")
        while True:
            try:
                value, end = DECODER.raw_decode(buffer)
                break
            except json.JSONDecodeError:
                need(len(buffer.encode("utf-8")) <= MAX_ROW, "incomplete row cap")
                buffer = append(buffer, "truncated JSON")
        need(len(buffer[:end].encode("utf-8")) <= MAX_ROW and len(canonical(value)) <= MAX_ROW, "final canonical row cap")
        yield value
        buffer = buffer[end:]
        comma = True


class RawPins:
    def __init__(self) -> None:
        self.dirfd = -1
        self.dir_before: os.stat_result | None = None
        self.files: dict[str, tuple[int, os.stat_result, int, str, str]] = {}
        self.pin_rows: list[dict[str, Any]] = []

    def __enter__(self) -> "RawPins":
        named = os.stat(DELIVERABLES, follow_symlinks=False)
        need(stat.S_ISDIR(named.st_mode), "deliverables directory")
        self.dirfd = os.open(DELIVERABLES, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0))
        self.dir_before = os.fstat(self.dirfd)
        need(directory_identity(named) == directory_identity(self.dir_before), "deliverables dirfd binding")
        try:
            for label, filename, size, sha in RAW_PINS:
                before = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
                need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and before.st_size == size, "raw path pin:" + label)
                fd = os.open(filename, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=self.dirfd)
                opened = os.fstat(fd)
                need(fingerprint(before) == fingerprint(opened), "raw open race:" + label)
                n, h = hash_fd(fd, size)
                need(n == size and h == sha, "raw byte pin:" + label)
                self.files[label] = (fd, opened, size, sha, filename)
                self.pin_rows.append({"label": label, "filename": filename, "exact_size": size, "sha256": sha, "pass1_sha256": h, "regular": True, "nlink_one": True})
            return self
        except Exception:
            self.close(False)
            raise

    def rows(self, label: str, marker: str) -> Iterator[dict[str, Any]]:
        fd, before, _, _, filename = self.files[label]
        os.lseek(fd, 0, os.SEEK_SET)
        raw = os.fdopen(os.dup(fd), "rb")
        binary: BinaryIO = gzip.GzipFile(fileobj=raw, mode="rb") if filename.endswith(".gz") else raw
        text = io.TextIOWrapper(binary, encoding="utf-8", newline="")
        try:
            yield from iter_array(text, marker)
        finally:
            text.close()
            if not raw.closed:
                raw.close()
            need(fingerprint(os.fstat(fd)) == fingerprint(before), "raw held FD stable:" + label)

    def small_json(self, label: str) -> Any:
        fd, before, size, _, _ = self.files[label]
        raw = os.pread(fd, size, 0)
        need(size <= MAX_ROW and len(raw) == size and fingerprint(os.fstat(fd)) == fingerprint(before), "small JSON held read")
        value = DECODER.decode(raw.decode("utf-8"))
        need(len(canonical(value)) <= MAX_ROW, "small JSON cap")
        return value

    def revalidate_held_snapshot(self) -> None:
        """Perform the advertised second pass without releasing any FD."""
        for label, (fd, before, size, sha, filename) in self.files.items():
            n, h = hash_fd(fd, size)
            named = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
            need(n == size and h == sha and fingerprint(before) == fingerprint(os.fstat(fd)) == fingerprint(named), "raw held snapshot rebind:" + label)
            for row in self.pin_rows:
                if row["label"] == label:
                    row["pass2_sha256"] = h
                    row["final_path_bound"] = True
        assert self.dir_before is not None
        need(directory_identity(self.dir_before) == directory_identity(os.fstat(self.dirfd)) == directory_identity(os.stat(DELIVERABLES, follow_symlinks=False)), "deliverables held snapshot directory binding")

    def close(self, verify: bool = True) -> None:
        error: Exception | None = None
        for label, (fd, before, size, sha, filename) in list(self.files.items()):
            try:
                if verify:
                    n, h = hash_fd(fd, size)
                    named = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
                    need(n == size and h == sha and fingerprint(before) == fingerprint(os.fstat(fd)) == fingerprint(named), "raw final path/FD binding:" + label)
                    for row in self.pin_rows:
                        if row["label"] == label:
                            row["pass2_sha256"] = h
                            row["final_path_bound"] = True
            except Exception as exc:
                if error is None:
                    error = exc
            finally:
                os.close(fd)
        self.files.clear()
        if self.dirfd >= 0:
            try:
                if verify:
                    assert self.dir_before is not None
                    need(directory_identity(self.dir_before) == directory_identity(os.fstat(self.dirfd)) == directory_identity(os.stat(DELIVERABLES, follow_symlinks=False)), "deliverables final binding")
            except Exception as exc:
                if error is None:
                    error = exc
            finally:
                os.close(self.dirfd)
                self.dirfd = -1
        if error is not None:
            raise error

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.close(exc_type is None)


class SealedFile:
    def __init__(self, path: Path, expected_size: int | None = None, expected_sha: str | None = None) -> None:
        self.path = path
        self.expected_size = expected_size
        self.expected_sha = expected_sha
        self.fd = -1
        self.before: os.stat_result | None = None

    def __enter__(self) -> "SealedFile":
        named = os.stat(self.path, follow_symlinks=False)
        need(stat.S_ISREG(named.st_mode) and named.st_nlink == 1, "sealed regular single-link:" + self.path.name)
        if self.expected_size is not None:
            need(named.st_size == self.expected_size, "sealed size:" + self.path.name)
        self.fd = os.open(self.path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        self.before = os.fstat(self.fd)
        need(fingerprint(named) == fingerprint(self.before), "sealed open race:" + self.path.name)
        n, h = hash_fd(self.fd, named.st_size)
        if self.expected_sha is not None:
            need(h == self.expected_sha, "sealed SHA:" + self.path.name)
        self.expected_size = n
        self.expected_sha = h
        return self

    def bytes(self) -> bytes:
        assert self.expected_size is not None
        return os.pread(self.fd, self.expected_size, 0)

    def jsonl(self) -> Iterator[dict[str, Any]]:
        raw = os.fdopen(os.dup(self.fd), "rb")
        binary = gzip.GzipFile(fileobj=raw, mode="rb")
        text = io.TextIOWrapper(binary, encoding="ascii", newline="")
        try:
            for line in text:
                need(line.endswith("\n") and len(line.encode("ascii")) <= MAX_ROW + 1, "output JSONL wire cap")
                row = DECODER.decode(line[:-1])
                need(canonical(row) == line[:-1].encode("ascii"), "output canonical JSONL")
                yield row
        finally:
            text.close()
            if not raw.closed:
                raw.close()

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        if self.fd >= 0:
            try:
                if exc_type is None:
                    assert self.before is not None and self.expected_size is not None and self.expected_sha is not None
                    n, h = hash_fd(self.fd, self.expected_size)
                    named = os.stat(self.path, follow_symlinks=False)
                    need(n == self.expected_size and h == self.expected_sha and fingerprint(self.before) == fingerprint(os.fstat(self.fd)) == fingerprint(named), "sealed final path binding:" + self.path.name)
            finally:
                os.close(self.fd)


def table_finish(label: str, audit: ListHash) -> dict[str, Any]:
    count, sha = EXPECTED_TABLES[label]
    observed = audit.finish()
    need(audit.count == count and observed == sha, label + ":table commitment")
    return {"table": label, "row_count": count, "rows_sha256": sha, "all_rows_own_sha256_checked": True}


def flush(db: sqlite3.Connection, sql: str, batch: list[tuple[Any, ...]], threshold: int = 2048) -> None:
    if len(batch) >= threshold:
        db.executemany(sql, batch)
        batch.clear()


def scalar(db: sqlite3.Connection, sql: str) -> Any:
    row = db.execute(sql).fetchone()
    need(row is not None, "scalar query empty")
    return row[0]


def source_cell_commitments(db: sqlite3.Connection, cell_ids: list[str]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for cell_id in cell_ids:
        source = db.execute("SELECT row_sha FROM cell WHERE cell_id=?", (cell_id,)).fetchone()
        need(source is not None, "source cell commitment missing")
        rows.append({"cell_id": cell_id, "row_sha256": source[0]})
    return rows


def primary_input_commitment(member_id: str, union_row_id: str, member_row_sha: str, cell_rows: list[dict[str, str]], registry_row_id: str, registry_row_sha: str, r288_row_id: str, r288_row_sha: str, canonical_atom_id: str, b0_row_id: str, b0_row_sha: str) -> dict[str, Any]:
    return {"domain": SCHEMA + ".primary-handle-input.v2", "member_id": member_id, "member_union_row_id": union_row_id, "member_union_row_sha256": member_row_sha, "predicate_source_cells": cell_rows, "R294_registry_row_id": registry_row_id, "R294_registry_row_sha256": registry_row_sha, "R288_atom_row_id": r288_row_id, "R288_atom_row_sha256": r288_row_sha, "R288_canonical_atom_id": canonical_atom_id, "B0_row_id": b0_row_id, "B0_row_sha256": b0_row_sha}


def primary_handle(commitment: dict[str, Any]) -> tuple[str, str]:
    sha = digest(commitment)
    return "round306b1af4k2i1-r2-primary:" + sha, sha


def rebuild(pins: RawPins, db: sqlite3.Connection) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    db.executescript("""
      PRAGMA journal_mode=OFF; PRAGMA synchronous=OFF; PRAGMA temp_store=MEMORY;
      CREATE TABLE r287(source_row_id TEXT PRIMARY KEY, source_kind TEXT NOT NULL, source_rep_id TEXT NOT NULL, row_sha TEXT NOT NULL);
      CREATE TABLE r288(source_row_id TEXT PRIMARY KEY, atom_id TEXT NOT NULL, candidate_member_id TEXT UNIQUE NOT NULL, row_sha TEXT NOT NULL);
      CREATE TABLE registry(registry_row_id TEXT PRIMARY KEY, member_id TEXT UNIQUE NOT NULL, source_row_id TEXT NOT NULL, source_row_sha TEXT NOT NULL, atom_id TEXT NOT NULL, row_sha TEXT NOT NULL);
      CREATE TABLE binding(binding_row_id TEXT PRIMARY KEY, source_rep_id TEXT UNIQUE NOT NULL, source_kind TEXT NOT NULL, source_row_id TEXT NOT NULL, source_row_sha TEXT NOT NULL, source_atom_row_id TEXT NOT NULL, source_atom_row_sha TEXT NOT NULL, target_member_id TEXT NOT NULL, row_sha TEXT NOT NULL);
      CREATE TABLE cell(cell_id TEXT PRIMARY KEY, member_id TEXT NOT NULL, row_sha TEXT NOT NULL);
      CREATE TABLE member(member_id TEXT PRIMARY KEY, union_row_id TEXT UNIQUE NOT NULL, registry_row_id TEXT UNIQUE NOT NULL, b0_row_id TEXT UNIQUE NOT NULL, component_id TEXT NOT NULL, multiplicity INTEGER NOT NULL, cell_ids_json TEXT NOT NULL, normalization_json TEXT, row_sha TEXT NOT NULL);
      CREATE TABLE edge(cell_id TEXT PRIMARY KEY, member_id TEXT NOT NULL);
      CREATE TABLE b0(member_id TEXT PRIMARY KEY, b0_row_id TEXT UNIQUE NOT NULL, component_id TEXT NOT NULL, registry_row_id TEXT UNIQUE NOT NULL, registry_row_sha TEXT NOT NULL, row_sha TEXT NOT NULL);
    """)
    receipts: list[dict[str, Any]] = []
    for marker, label, kind, id_field, rep_field in (
        ('"region_rows"', "R287_REGION", "ROUND287_R275_REGION_INCLUSION_SUBCOVER", "Round287_region_disposition_row_id", "Round275_region_id"),
        ('"refinement_cell_rows"', "R287_REFINEMENT", "ROUND287_R286_SIGNED_CELL_INCLUSION_SUBCOVER", "Round287_refinement_cell_disposition_row_id", "Round286_refinement_cell_id"),
    ):
        audit = ListHash(); batch: list[tuple[Any, ...]] = []
        for row in pins.rows("R287", marker):
            closed_hash(row, label); audit.add(row)
            batch.append((row[id_field], kind, row[rep_field], row["row_sha256"])); flush(db, "INSERT INTO r287 VALUES(?,?,?,?)", batch)
        if batch: db.executemany("INSERT INTO r287 VALUES(?,?,?,?)", batch)
        receipts.append(table_finish(label, audit))

    audit = ListHash(); batch = []
    for row in pins.rows("R288", '"rows"'):
        closed_hash(row, "R288"); audit.add(row)
        candidate = row["reserved_candidate_occurrence_id__not_issued"]
        need(candidate is None or type(candidate) is str, "R288 candidate type")
        if candidate is not None:
            batch.append((row["Round288_atom_disposition_row_id"], row["canonical_atom_id"], candidate, row["row_sha256"])); flush(db, "INSERT INTO r288 VALUES(?,?,?,?)", batch)
    if batch: db.executemany("INSERT INTO r288 VALUES(?,?,?,?)", batch)
    receipts.append(table_finish("R288", audit))

    audit = ListHash(); batch = []
    for row in pins.rows("R294_REGISTRY", '"rows"'):
        closed_hash(row, "R294 registry"); audit.add(row)
        if row["registry_entry_kind"] == "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM":
            need(type_strict_equal(row["formal_new_expanded_occurrence_credit"], 1), "R294 R2 identity credit")
            need(row["registry_identity_status"] == "FORMALLY_ISSUED_ROUND294_ATOMIC_OCCURRENCE_ID" and row["registry_promotion_status"] == "FORMALLY_PROMOTED_ROUND294_ATOMIC_OCCURRENCE_REGISTRY", "R294 R2 registry status")
            batch.append((row["Round294_occurrence_registry_row_id"], row["registry_occurrence_id"], row["source_row_id"], row["source_row_sha256"], row["canonical_atom_id"], row["row_sha256"])); flush(db, "INSERT INTO registry VALUES(?,?,?,?,?,?)", batch)
    if batch: db.executemany("INSERT INTO registry VALUES(?,?,?,?,?,?)", batch)
    receipts.append(table_finish("R294_REGISTRY", audit))

    audit = ListHash(); batch = []
    for row in pins.rows("R294_BINDINGS", '"rows"'):
        closed_hash(row, "R294 binding"); audit.add(row)
        if row["alias_source_kind"] in ("ROUND287_R275_REGION_INCLUSION_SUBCOVER", "ROUND287_R286_SIGNED_CELL_INCLUSION_SUBCOVER"):
            need(row["support_representation_kind"] == "EXACT_SAME_POSITIVE_OPEN_REGION_INCLUSION_SUBCOVER", "R287 alias support kind")
            need(type_strict_equal(row["formal_occurrence_alias_credit"], 1) and row["does_not_issue_new_occurrence_id"] is True and row["does_not_collapse_distinct_occurrence_ids"] is True, "R294 alias identity authority")
            batch.append((row["Round294_occurrence_representation_binding_row_id"], row["source_representation_id"], row["alias_source_kind"], row["source_row_id"], row["source_row_sha256"], row["source_Round288_atom_disposition_row_id"], row["source_Round288_atom_disposition_row_sha256"], row["target_registry_occurrence_id"], row["row_sha256"])); flush(db, "INSERT INTO binding VALUES(?,?,?,?,?,?,?,?,?)", batch)
    if batch: db.executemany("INSERT INTO binding VALUES(?,?,?,?,?,?,?,?,?)", batch)
    receipts.append(table_finish("R294_BINDINGS", audit))

    audit = ListHash(); batch = []
    for row in pins.rows("B1R0_CELLS", '"predicate_source_cell_rows"'):
        closed_hash(row, "B1R0 cell"); audit.add(row)
        need(type_strict_equal(row["formal_full_support_credit"], 0), "B1R0 cell zero credit")
        batch.append((row["Round306B1R0_predicate_source_cell_row_id"], row["formal_member_id"], row["row_sha256"])); flush(db, "INSERT INTO cell VALUES(?,?,?)", batch)
    if batch: db.executemany("INSERT INTO cell VALUES(?,?,?)", batch)
    receipts.append(table_finish("B1R0_CELLS", audit))

    audit = ListHash(); members: list[tuple[Any, ...]] = []; edges: list[tuple[Any, ...]] = []
    for row in pins.rows("B1R0_MEMBERS", '"member_union_rows"'):
        closed_hash(row, "B1R0 member"); audit.add(row)
        n = row["predicate_source_cell_multiplicity"]; ids = row["predicate_source_cell_row_ids"]
        need(type(n) is int and n in (1, 2) and type(ids) is list and len(ids) == n and len(ids) == len(set(ids)), "member cell list")
        need((n == 2) is (row["Round271_W_tail_parent_normalization"] is not None), "W-tail normalization iff two-cell member")
        need(type_strict_equal(row["formal_full_support_credit"], 0) and row["full_support_union_theorem_status"] == "PENDING_SOURCE_FREE_INTERVAL_PREDICATE_EQUIVALENCE", "member theorem boundary")
        members.append((row["member_id"], row["Round306B1R0_member_union_row_id"], row["Round294_registry_row_id"], row["Round306B0_member_source_row_id"], row["Round306A_component_id"], n, canonical(ids).decode("ascii"), canonical(row["Round271_W_tail_parent_normalization"]).decode("ascii") if row["Round271_W_tail_parent_normalization"] is not None else None, row["row_sha256"]))
        edges.extend((cell_id, row["member_id"]) for cell_id in ids)
        flush(db, "INSERT INTO member VALUES(?,?,?,?,?,?,?,?,?)", members); flush(db, "INSERT INTO edge VALUES(?,?)", edges)
    if members: db.executemany("INSERT INTO member VALUES(?,?,?,?,?,?,?,?,?)", members)
    if edges: db.executemany("INSERT INTO edge VALUES(?,?)", edges)
    receipts.append(table_finish("B1R0_MEMBERS", audit))

    audit = ListHash(); batch = []
    for row in pins.rows("B0", '"member_support_source_rows"'):
        closed_hash(row, "B0"); audit.add(row)
        if row["identity_tranche"] == "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM":
            need(row["primary_source_package"] == "R294" and row["identity_class"] == "FORMAL_OCCURRENCE" and row["member_identity_preserved"] is True, "B0 R2 identity authority")
            batch.append((row["member_id"], row["Round306B0_member_support_source_row_id"], row["Round306A_component_id"], row["primary_source_row_id"], row["primary_source_row_sha256"], row["row_sha256"])); flush(db, "INSERT INTO b0 VALUES(?,?,?,?,?,?)", batch)
    if batch: db.executemany("INSERT INTO b0 VALUES(?,?,?,?,?,?)", batch)
    receipts.append(table_finish("B0", audit))
    db.commit(); db.executescript("CREATE INDEX binding_target ON binding(target_member_id); CREATE INDEX edge_member ON edge(member_id);")

    strict_need(dict(db.execute("SELECT multiplicity,COUNT(*) FROM member GROUP BY multiplicity")), {1: 295_332, 2: 4}, "multiplicity histogram")
    need(scalar(db, "SELECT COUNT(*) FROM cell") == 295_340 and scalar(db, "SELECT COUNT(*) FROM member") == 295_336 and scalar(db, "SELECT COUNT(*) FROM edge") == 295_340, "R2 base census")
    need(scalar(db, "SELECT COUNT(*) FROM edge e LEFT JOIN cell c ON c.cell_id=e.cell_id WHERE c.cell_id IS NULL OR c.member_id<>e.member_id") == 0, "edge/cell join")
    need(scalar(db, "SELECT COUNT(*) FROM cell c LEFT JOIN edge e ON e.cell_id=c.cell_id WHERE e.cell_id IS NULL OR e.member_id<>c.member_id") == 0, "cell/edge exhaustion")
    need(scalar(db, "SELECT COUNT(*) FROM registry") == 295_336 and scalar(db, "SELECT COUNT(*) FROM r288") == 295_336 and scalar(db, "SELECT COUNT(*) FROM b0") == 295_336, "registry/R288/B0 census")
    need(scalar(db, "SELECT COUNT(*) FROM registry r LEFT JOIN r288 a ON a.source_row_id=r.source_row_id WHERE a.source_row_id IS NULL OR a.row_sha<>r.source_row_sha OR a.atom_id<>r.atom_id OR a.candidate_member_id<>r.member_id") == 0, "registry/R288 join")
    need(scalar(db, "SELECT COUNT(*) FROM member m LEFT JOIN registry r ON r.registry_row_id=m.registry_row_id LEFT JOIN b0 b ON b.member_id=m.member_id WHERE r.registry_row_id IS NULL OR r.member_id<>m.member_id OR b.member_id IS NULL OR b.b0_row_id<>m.b0_row_id OR b.component_id<>m.component_id OR b.registry_row_id<>r.registry_row_id OR b.registry_row_sha<>r.row_sha") == 0, "member/registry/B0 join")
    alias_counts = dict(db.execute("SELECT source_kind,COUNT(*) FROM binding b WHERE EXISTS(SELECT 1 FROM member m WHERE m.member_id=b.target_member_id) GROUP BY source_kind"))
    strict_need(alias_counts, {"ROUND287_R275_REGION_INCLUSION_SUBCOVER": 2_476, "ROUND287_R286_SIGNED_CELL_INCLUSION_SUBCOVER": 4_812}, "alias source census")
    need(scalar(db, "SELECT COUNT(*) FROM binding b WHERE EXISTS(SELECT 1 FROM member m WHERE m.member_id=b.target_member_id)") == 7_288, "alias count")
    need(scalar(db, "SELECT COUNT(DISTINCT source_rep_id) FROM binding b WHERE EXISTS(SELECT 1 FROM member m WHERE m.member_id=b.target_member_id)") == 7_288, "alias uniqueness")
    need(scalar(db, "SELECT COUNT(DISTINCT target_member_id) FROM binding b WHERE EXISTS(SELECT 1 FROM member m WHERE m.member_id=b.target_member_id)") == 384, "alias owner count")
    need(scalar(db, "SELECT COUNT(*) FROM binding b JOIN member m ON m.member_id=b.target_member_id LEFT JOIN r287 s ON s.source_row_id=b.source_row_id WHERE s.source_row_id IS NULL OR s.row_sha<>b.source_row_sha OR s.source_kind<>b.source_kind OR s.source_rep_id<>b.source_rep_id") == 0, "alias/R287 join")
    need(scalar(db, "SELECT COUNT(*) FROM binding b JOIN registry r ON r.member_id=b.target_member_id LEFT JOIN r288 a ON a.source_row_id=b.source_atom_row_id WHERE a.source_row_id IS NULL OR a.row_sha<>b.source_atom_row_sha OR b.source_atom_row_id<>r.source_row_id OR b.source_atom_row_sha<>r.source_row_sha") == 0, "alias/R288/owner join")
    census = {
        "R2_predicate_source_cell_count": 295_340,
        "R2_member_count": 295_336,
        "R2_member_multiplicity_histogram": {"1": 295_332, "2": 4},
        "R2_primary_member_union_handle_count": 295_336,
        "R2_R287_alias_representation_count": 7_288,
        "R2_representation_count": 302_624,
        "R2_R287_alias_source_kind_counts": dict(sorted(alias_counts.items())),
        "R2_alias_owner_member_count": 384,
        "R2_W_tail_two_cell_member_count": 4,
        "representation_census_equation": "295336_PRIMARY_MEMBER_UNION_HANDLES_PLUS_7288_R287_ALIASES_EQUALS_302624",
    }
    return receipts, census


def expected_member_rows(db: sqlite3.Connection) -> Iterator[dict[str, Any]]:
    query = "SELECT m.member_id,m.component_id,m.union_row_id,m.multiplicity,m.cell_ids_json,m.row_sha,r.registry_row_id,r.row_sha,r.source_row_id,r.source_row_sha,r.atom_id,b.b0_row_id,b.row_sha FROM member m JOIN registry r ON r.member_id=m.member_id JOIN b0 b ON b.member_id=m.member_id ORDER BY m.member_id"
    for member_id, component_id, union_id, n, cell_json, member_sha, registry_id, registry_sha, r288_id, r288_sha, atom_id, b0_id, b0_sha in db.execute(query):
        ids = json.loads(cell_json); cells = source_cell_commitments(db, ids)
        input_commitment = primary_input_commitment(member_id, union_id, member_sha, cells, registry_id, registry_sha, r288_id, r288_sha, atom_id, b0_id, b0_sha)
        handle, commitment = primary_handle(input_commitment)
        yield close_row({"schema": SCHEMA + ".member-row", "status": "MECHANICAL_IDENTITY_JOINED__SEMANTIC_SUPPORT_NOT_PROVED", "coarse_family": "R2", "member_id": member_id, "component_id": component_id, "member_union_row_id": union_id, "primary_representation_handle_id": handle, "primary_representation_input_commitment_sha256": commitment, "canonical_input_commitment": input_commitment, "predicate_source_cell_count": n, "predicate_source_cell_row_ids": ids, "source_B1R0_member_row_sha256": member_sha, "source_R294_registry_row_id": registry_id, "source_R294_registry_row_sha256": registry_sha, "source_R288_atom_row_id": r288_id, "source_R288_atom_row_sha256": r288_sha, "source_R288_canonical_atom_id": atom_id, "source_B0_row_id": b0_id, "source_B0_row_sha256": b0_sha, "transition_ready_handle_status": "IDENTITY_ROUTABLE_ONLY__NO_TRANSITION_THEOREM_CREDIT", "formal_credit": ZERO_MEMBER_CREDIT})


def expected_representation_rows(db: sqlite3.Connection) -> Iterator[dict[str, Any]]:
    query = "SELECT m.member_id,m.union_row_id,m.cell_ids_json,m.row_sha,r.registry_row_id,r.row_sha,r.source_row_id,r.source_row_sha,r.atom_id,b.b0_row_id,b.row_sha FROM member m JOIN registry r ON r.member_id=m.member_id JOIN b0 b ON b.member_id=m.member_id ORDER BY m.member_id"
    for member_id, union_id, cell_json, member_sha, registry_id, registry_sha, r288_id, r288_sha, atom_id, b0_id, b0_sha in db.execute(query):
        ids = json.loads(cell_json); cells = source_cell_commitments(db, ids)
        input_commitment = primary_input_commitment(member_id, union_id, member_sha, cells, registry_id, registry_sha, r288_id, r288_sha, atom_id, b0_id, b0_sha)
        handle, commitment = primary_handle(input_commitment)
        yield close_row({"schema": SCHEMA + ".representation-row", "status": "TRANSITION_READY_IDENTITY_HANDLE__SEMANTIC_SUPPORT_BLOCKED", "representation_role": "PRIMARY_MEMBER_PREDICATE_UNION_HANDLE", "representation_id": handle, "owner_member_id": member_id, "coverage_semantics": "MECHANICAL_MEMBER_UNION_IDENTITY_ONLY__FULL_SET_EQUALITY_NOT_PROVED", "transition_payload_sha256": commitment, "canonical_input_commitment": input_commitment, "predicate_source_cell_count": len(ids), "predicate_source_cell_ids_sha256": digest({"ordered_cell_rows": cells}), "source_B1R0_member_union_row_id": union_id, "source_B1R0_member_row_sha256": member_sha, "source_R294_binding_row_id": None, "source_R294_binding_row_sha256": None, "source_R287_row_id": None, "source_R287_row_sha256": None, "source_R294_target_registry_row_id": registry_id, "source_R294_target_registry_row_sha256": registry_sha, "source_R288_atom_row_id": r288_id, "source_R288_atom_row_sha256": r288_sha, "source_B0_row_id": b0_id, "source_B0_row_sha256": b0_sha, "formal_credit": ZERO_REPRESENTATION_CREDIT})
    query = "SELECT b.source_rep_id,b.target_member_id,b.source_kind,b.source_row_id,b.source_row_sha,b.binding_row_id,b.row_sha,b.source_atom_row_id,b.source_atom_row_sha,r.registry_row_id,r.row_sha,x.b0_row_id,x.row_sha FROM binding b JOIN member m ON m.member_id=b.target_member_id JOIN registry r ON r.member_id=b.target_member_id JOIN b0 x ON x.member_id=b.target_member_id ORDER BY b.source_rep_id"
    for rep_id, owner, kind, source_id, source_sha, binding_id, binding_sha, r288_id, r288_sha, registry_id, registry_sha, b0_id, b0_sha in db.execute(query):
        payload = {"domain": SCHEMA + ".alias-handle-input.v2", "representation_id": rep_id, "owner_member_id": owner, "source_kind": kind, "R287_source_row_id": source_id, "R287_source_row_sha256": source_sha, "R294_binding_row_id": binding_id, "R294_binding_row_sha256": binding_sha, "R288_atom_row_id": r288_id, "R288_atom_row_sha256": r288_sha, "R294_target_registry_row_id": registry_id, "R294_target_registry_row_sha256": registry_sha, "B0_row_id": b0_id, "B0_row_sha256": b0_sha}
        yield close_row({"schema": SCHEMA + ".representation-row", "status": "TRANSITION_READY_IDENTITY_HANDLE__GLOBAL_SUPPORT_EQUIVALENCE_BLOCKED", "representation_role": "R287_EXACT_SUBCOVER_ALIAS", "representation_id": rep_id, "owner_member_id": owner, "coverage_semantics": "UPSTREAM_EXACT_SUBCOVER_ALIAS_IDENTITY_ONLY__GLOBAL_SET_EQUALITY_NOT_PROVED", "transition_payload_sha256": digest(payload), "canonical_input_commitment": payload, "predicate_source_cell_count": None, "predicate_source_cell_ids_sha256": None, "source_B1R0_member_union_row_id": None, "source_B1R0_member_row_sha256": None, "source_R294_binding_row_id": binding_id, "source_R294_binding_row_sha256": binding_sha, "source_R287_row_id": source_id, "source_R287_row_sha256": source_sha, "source_R294_target_registry_row_id": registry_id, "source_R294_target_registry_row_sha256": registry_sha, "source_R288_atom_row_id": r288_id, "source_R288_atom_row_sha256": r288_sha, "source_B0_row_id": b0_id, "source_B0_row_sha256": b0_sha, "formal_credit": ZERO_REPRESENTATION_CREDIT})


def expected_wtail_rows(db: sqlite3.Connection) -> Iterator[dict[str, Any]]:
    for member_id, union_id, cell_json, normalization_json, member_sha in db.execute("SELECT member_id,union_row_id,cell_ids_json,normalization_json,row_sha FROM member WHERE multiplicity=2 ORDER BY member_id"):
        ids = json.loads(cell_json); normalization = json.loads(normalization_json)
        input_commitment = {"domain": SCHEMA + ".wtail-gap-input.v2", "member_id": member_id, "member_union_row_id": union_id, "member_union_row_sha256": member_sha, "predicate_source_cells": source_cell_commitments(db, ids), "parent_normalization": normalization}
        yield close_row({"schema": SCHEMA + ".wtail-blocked-obligation-row", "status": "BLOCKED_IN_THIS_MECHANICAL_LANE__SEMANTIC_KERNEL_NOT_CONSUMED", "obligation_kind": "W_TAIL_TWO_CHILD_ARTIFICIAL_FACE_REGLUE_PHYSICAL_EQUIVALENCE", "member_id": member_id, "source_B1R0_member_union_row_id": union_id, "source_B1R0_member_row_sha256": member_sha, "predicate_source_cell_row_ids": ids, "source_parent_normalization": normalization, "canonical_input_commitment": input_commitment, "canonical_input_commitment_sha256": digest(input_commitment), "external_semantic_kernel_status": "NOT_CONSUMED_BY_THIS_MECHANICAL_IDENTITY_LANE", "formal_credit": {"artificial_face_reglue": 0, "physical_incidence": 0, "pullback_equivalence": 0, "normalized_support": 0, "representation_cover": 0}})


def compare_ledger(key: str, sealed: SealedFile, meta: dict[str, Any], expected: Iterable[dict[str, Any]], expected_count: int, expected_order: str) -> dict[str, Any]:
    strict_need(set(meta), {"filename", "row_count", "uncompressed_jsonl_size", "uncompressed_jsonl_sha256", "file_size", "file_sha256", "order"}, "ledger meta keys:" + key)
    strict_need(meta["filename"], OUTPUTS[key], "ledger filename:" + key)
    strict_need(meta["row_count"], expected_count, "ledger count receipt:" + key)
    strict_need(meta["order"], expected_order, "ledger order receipt:" + key)
    need(type(meta["file_size"]) is int and meta["file_size"] > 0 and type(meta["uncompressed_jsonl_size"]) is int and meta["uncompressed_jsonl_size"] > 0, "strict ledger sizes:" + key)
    need(type(meta["file_sha256"]) is str and HEX64.fullmatch(meta["file_sha256"]) is not None and type(meta["uncompressed_jsonl_sha256"]) is str and HEX64.fullmatch(meta["uncompressed_jsonl_sha256"]) is not None, "ledger digest syntax:" + key)
    state = hashlib.sha256(); raw_size = count = 0
    expected_iter = iter(expected)
    for actual in sealed.jsonl():
        closed_hash(actual, "output " + key)
        try:
            wanted = next(expected_iter)
        except StopIteration as exc:
            raise VerificationBlocked("extra output row:" + key) from exc
        strict_need(actual, wanted, "exact output row:" + key + ":" + str(count))
        wire = canonical(actual) + b"\n"; state.update(wire); raw_size += len(wire); count += 1
    exhausted = False
    try:
        next(expected_iter)
    except StopIteration:
        exhausted = True
    need(exhausted and count == expected_count, "output exhaustion:" + key)
    strict_need(meta["uncompressed_jsonl_size"], raw_size, "raw size:" + key)
    strict_need(meta["uncompressed_jsonl_sha256"], state.hexdigest(), "raw SHA:" + key)
    return {"filename": OUTPUTS[key], "row_count": count, "file_size": meta["file_size"], "file_sha256": meta["file_sha256"], "uncompressed_jsonl_size": raw_size, "uncompressed_jsonl_sha256": state.hexdigest()}


def verify_with_stack(stack: ExitStack) -> dict[str, Any]:
    need(PRODUCER_SIZE > 0 and HEX64.fullmatch(PRODUCER_SHA256) is not None, "verifier producer static pin finalized")
    stack.enter_context(SealedFile(DELIVERABLES / PRODUCER, PRODUCER_SIZE, PRODUCER_SHA256))
    result_file = stack.enter_context(SealedFile(DELIVERABLES / RESULT))
    raw = result_file.bytes()
    need(raw.endswith(b"\n") and len(raw) <= MAX_ROW, "result wire")
    result = DECODER.decode(raw[:-1].decode("ascii"))
    need(canonical(result) + b"\n" == raw, "canonical result")
    result_file_sha = result_file.expected_sha
    strict_need(set(result), {"schema", "status", "scope", "producer_sha256", "producer_byte_binding", "seed_affects_output", "input_pins", "source_table_commitments", "exact_census", "ledgers", "closed_anti_joins", "known_gaps", "availability_boundary", "formal_credit"}, "result keys")
    need(result["schema"] == SCHEMA and result["status"] == EXPECTED_STATUS and result["scope"] == "R2_ONLY_MECHANICAL_IDENTITY_REPRESENTATION_LANE", "result identity")
    strict_need(result["producer_sha256"], None, "producer does not self-attest")
    need(result["producer_byte_binding"] == "EXTERNAL_INDEPENDENT_VERIFIER_STATIC_PIN_ONLY" and result["seed_affects_output"] is False, "producer byte/seed boundary")
    strict_need(result["formal_credit"], ZERO_GLOBAL_CREDIT, "global zero credit")
    strict_need(result["known_gaps"], EXPECTED_GAPS, "known gaps")
    strict_need(result["closed_anti_joins"], EXPECTED_ANTI_JOINS, "anti joins")
    strict_need(result["availability_boundary"], {"bounded_memory_claim": False, "runtime_or_RSS_upper_bound_proved": False, "failure_before_result_marker_mints_credit": False}, "availability boundary")
    strict_need(set(result["ledgers"]), set(OUTPUTS), "ledger key allowlist")
    held_outputs: dict[str, SealedFile] = {}
    for key, filename in OUTPUTS.items():
        meta = result["ledgers"][key]
        need(type(meta) is dict and type(meta.get("file_size")) is int and type(meta.get("file_sha256")) is str, "ledger snapshot metadata:" + key)
        held_outputs[key] = stack.enter_context(SealedFile(DELIVERABLES / filename, meta["file_size"], meta["file_sha256"]))
    pins = stack.enter_context(RawPins())

    root = "/tmp"
    need(os.path.realpath(root) == root, "explicit /tmp authority")
    root_named = os.stat(root, follow_symlinks=False)
    root_fd = os.open(root, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0))
    need(directory_identity(root_named) == directory_identity(os.fstat(root_fd)), "held /tmp dirfd")
    try:
        with tempfile.TemporaryDirectory(prefix="cm2-k2i1-r2-verify-", dir=root) as temporary:
            db = sqlite3.connect(Path(temporary) / "independent.sqlite3")
            try:
                af2 = pins.small_json("AF2_RESULT")
                need(type_strict_equal(af2["member_count"], 564_492) and type_strict_equal(af2["coarse_partition"]["R2_predicate_union_members"], 295_336) and type_strict_equal(af2["R2"]["predicate_cell_reference_count"], 295_340) and type_strict_equal(af2["formal_credit"], 0), "AF2 R2 denominator/credit")
                receipts, census = rebuild(pins, db)
                pins.revalidate_held_snapshot()
                pin_rows = pins.pin_rows
                strict_need(result["input_pins"], pin_rows, "input pin receipt")
                strict_need(result["source_table_commitments"], receipts, "table receipt")
                strict_need(result["exact_census"], census, "exact census")
                verified = {
                    "member": compare_ledger("member", held_outputs["member"], result["ledgers"]["member"], expected_member_rows(db), 295_336, "member_id_unsigned_bytewise_ASCII_ASC"),
                    "representation": compare_ledger("representation", held_outputs["representation"], result["ledgers"]["representation"], expected_representation_rows(db), 302_624, "PRIMARY_BY_member_id_THEN_ALIAS_BY_source_representation_id__unsigned_bytewise_ASCII_ASC"),
                    "wtail_gap": compare_ledger("wtail_gap", held_outputs["wtail_gap"], result["ledgers"]["wtail_gap"], expected_wtail_rows(db), 4, "member_id_unsigned_bytewise_ASCII_ASC"),
                }
            finally:
                db.close()
        need(directory_identity(root_named) == directory_identity(os.fstat(root_fd)) == directory_identity(os.stat(root, follow_symlinks=False)), "/tmp final binding")
    finally:
        os.close(root_fd)
    return {
        "schema": SCHEMA + ".independent-verification.v1",
        "status": "PASS_INDEPENDENT_COLD_REPLAY_EXACT_R2_MECHANICAL_INDEX__ZERO_THEOREM_CREDIT",
        "producer_imported_or_executed": False,
        "producer_sha256": PRODUCER_SHA256,
        "result_file_sha256": result_file_sha,
        "source_table_commitments": receipts,
        "verified_ledgers": verified,
        "verified_census": census,
        "anti_join_gaps": EXPECTED_ANTI_JOINS,
        "known_gaps_reproduced_exactly": EXPECTED_GAPS,
        "formal_credit": ZERO_GLOBAL_CREDIT,
    }


def verify(*, publish_receipt: bool) -> dict[str, Any]:
    # Producer, result, and all three output ledgers stay held from the entry
    # snapshot through the complete reconstruction.  Ordinary --verify is
    # deliberately no-write; receipt publication requires the explicit
    # --verify-and-publish mode.
    with ExitStack() as stack:
        document = verify_with_stack(stack)
        if publish_receipt:
            publish(document)
        return document


def self_test() -> dict[str, Any]:
    base = {"x": 0, "flag": False}
    row = close_row(base)
    need(closed_hash(row, "self-test") == row["row_sha256"], "closed positive")
    broken = dict(row); broken["x"] = 1
    rejected = False
    try:
        closed_hash(broken, "mutation")
    except VerificationBlocked:
        rejected = True
    need(rejected, "row mutation rejected")
    attacks = [
        ({"formal_credit": {"CM2": False}}, {"formal_credit": {"CM2": 0}}),
        ({"formal_credit": {"B1A": False}}, {"formal_credit": {"B1A": 0}}),
        ({"exact_census": {"R2_member_count": True}}, {"exact_census": {"R2_member_count": 1}}),
        ({"predicate_source_cell_count": False}, {"predicate_source_cell_count": 0}),
        ({"seed_affects_output": 0}, {"seed_affects_output": False}),
        ({"row_count": True}, {"row_count": 1}),
        ({"formal_credit": {"representation_cover": False}}, {"formal_credit": {"representation_cover": 0}}),
        ({"formal_credit": {"physical_incidence": False}}, {"formal_credit": {"physical_incidence": 0}}),
        ({"formal_credit": {"pullback_equivalence": False}}, {"formal_credit": {"pullback_equivalence": 0}}),
        ({"availability_boundary": {"failure_before_result_marker_mints_credit": 0}}, {"availability_boundary": {"failure_before_result_marker_mints_credit": False}}),
    ]
    for actual, expected in attacks:
        need(not type_strict_equal(actual, expected), "bool/int alias attack")
    need(type_strict_equal({"x": [0, "a", False]}, {"x": [0, "a", False]}), "strict equality positive")
    commitment_regressions = [
        ({"domain": "primary", "member": "m", "R288_sha": "0" * 64}, {"domain": "primary", "member": "m", "R288_sha": "1" * 64}),
        ({"domain": "primary", "member": "m", "B0_sha": "0" * 64}, {"domain": "primary", "member": "m", "B0_sha": "1" * 64}),
        ({"domain": "alias", "owner": "a", "binding_sha": "0" * 64}, {"domain": "alias", "owner": "b", "binding_sha": "0" * 64}),
        ({"domain": "wtail", "cells": [{"id": "c", "sha": "0" * 64}]}, {"domain": "wtail", "cells": [{"id": "c", "sha": "1" * 64}]}),
    ]
    for left, right in commitment_regressions:
        need(digest(left) != digest(right), "distinct canonical input certificates require distinct digest")
    grammar_attacks = ['{"x":0,"x":0}', '{"x":1.5}', '{"x":NaN}']
    for wire in grammar_attacks:
        grammar_rejected = False
        try:
            DECODER.decode(wire)
        except (VerificationBlocked, json.JSONDecodeError):
            grammar_rejected = True
        need(grammar_rejected, "JSON grammar attack rejected")
    exact = {"x": "a" * (MAX_ROW - len(canonical({"x": ""})))}
    need(len(canonical(exact)) == MAX_ROW and list(iter_array(io.StringIO('{"rows":[' + canonical(exact).decode("ascii") + ']}' ), '"rows"')) == [exact], "exact cap")
    over_rejected = False
    try:
        list(iter_array(io.StringIO('{"rows":[' + canonical({"x": exact["x"] + "a"}).decode("ascii") + ']}' ), '"rows"'))
    except VerificationBlocked:
        over_rejected = True
    need(over_rejected, "cap plus one")
    return {"schema": SCHEMA + ".independent-verifier-self-test", "status": "PASS", "producer_imported_or_executed": False, "row_mutation_rejected": True, "recursive_bool_int_alias_attacks_rejected": len(attacks), "canonical_input_commitment_cross_certificate_regressions": len(commitment_regressions), "json_grammar_attacks_rejected": len(grammar_attacks), "false_equals_zero_rejected": True, "true_equals_one_rejected": True, "decoded_row_exact_cap": MAX_ROW, "decoded_row_cap_plus_one_rejected": True}


def publish(document: dict[str, Any]) -> None:
    root = "/tmp"
    need(os.path.realpath(root) == root, "explicit /tmp")
    root_named = os.stat(root, follow_symlinks=False)
    output_named = os.stat(DELIVERABLES, follow_symlinks=False)
    root_fd = os.open(root, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0))
    output_fd = os.open(DELIVERABLES, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0))
    need(directory_identity(root_named) == directory_identity(os.fstat(root_fd)), "held root")
    need(directory_identity(output_named) == directory_identity(os.fstat(output_fd)), "held output")
    try:
        with tempfile.TemporaryDirectory(prefix="cm2-k2i1-r2-publish-", dir=root) as temporary:
            staged = Path(temporary)
            staged_named = os.stat(staged, follow_symlinks=False)
            staged_fd = os.open(staged, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0))
            need(directory_identity(staged_named) == directory_identity(os.fstat(staged_fd)), "held staging")
            try:
                path = staged / VERIFICATION
                path.write_bytes(canonical(document) + b"\n")
                with path.open("rb") as handle: os.fsync(handle.fileno())
                info = os.stat(VERIFICATION, dir_fd=staged_fd, follow_symlinks=False)
                need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "staged verification")
                os.replace(VERIFICATION, VERIFICATION, src_dir_fd=staged_fd, dst_dir_fd=output_fd)
                os.fsync(output_fd)
                published = os.stat(VERIFICATION, dir_fd=output_fd, follow_symlinks=False)
                need(stat.S_ISREG(published.st_mode) and published.st_nlink == 1 and published.st_size == info.st_size, "published verification")
            finally:
                os.close(staged_fd)
        need(directory_identity(root_named) == directory_identity(os.fstat(root_fd)) == directory_identity(os.stat(root, follow_symlinks=False)), "root final")
        need(directory_identity(output_named) == directory_identity(os.fstat(output_fd)) == directory_identity(os.stat(DELIVERABLES, follow_symlinks=False)), "output final")
    finally:
        os.close(root_fd); os.close(output_fd)


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--verify", action="store_true")
    group.add_argument("--verify-and-publish", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        print(canonical(self_test()).decode("ascii")); return 0
    document = verify(publish_receipt=args.verify_and_publish)
    print(canonical({"status": document["status"], "verification_sha256": digest(document)}).decode("ascii")); return 0


if __name__ == "__main__":
    raise SystemExit(main())
