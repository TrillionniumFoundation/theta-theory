#!/usr/bin/env python3
"""Strict mechanical R2 identity/representation index (zero theorem credit).

This producer recomputes the R2 lane directly from byte-pinned raw authority.
It emits 295,336 member-union identity handles and 7,288 R287 alias handles,
for the exact R2 representation census 302,624.  The four two-cell W-tail
unions remain explicit blocked semantic obligations in this lane.  No emitted
row is a normalized-support theorem, a representation-cover theorem, or B1A.

The hash seed is accepted only for the double-seed replay contract and never
affects output.  Python artifacts are pinned as inert bytes; none is imported.
"""

from __future__ import annotations

import argparse
from collections import Counter
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


class Blocked(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise Blocked(label)


PREFIX = "cm2_round306b1af4k2i1_source_g_r2_identity_representation_index_"
SCHEMA = "cm2.round306b1af4k2i1.source-g-r2-identity-representation-index.v1"
STATUS = "PASS_EXACT_R2_MECHANICAL_IDENTITY_REPRESENTATION_INDEX__ZERO_THEOREM_CREDIT"
DELIVERABLES = Path(__file__).resolve().parent
HEX64 = re.compile(r"^[0-9a-f]{64}$")
MAX_ROW = 8 << 20
CHARS = 1 << 18
BUFFER_CAP = MAX_ROW + 4 * CHARS

INPUT_PINS: tuple[tuple[str, str, int, str], ...] = (
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

OUTPUTS = {
    "member": PREFIX + "member_index.jsonl.gz",
    "representation": PREFIX + "representation_index.jsonl.gz",
    "wtail_gap": PREFIX + "wtail_blocked_obligation_index.jsonl.gz",
    "result": PREFIX + "result.json",
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
    raise Blocked("nonintegral JSON token:" + token)


DECODER = json.JSONDecoder(object_pairs_hook=unique_object, parse_float=reject_number, parse_constant=reject_number)


def row_hash(row: dict[str, Any], label: str) -> str:
    need(type(row) is dict and type(row.get("row_sha256")) is str, label + ":closed row")
    body = dict(row)
    claimed = body.pop("row_sha256")
    need(HEX64.fullmatch(claimed) is not None and digest(body) == claimed, label + ":row hash")
    return claimed


def closed(body: dict[str, Any]) -> dict[str, Any]:
    need("row_sha256" not in body, "output body preclosed")
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
        offset += len(block)
        total += len(block)
        need(total <= limit, "held FD grew while hashing")
        state.update(block)
    return total, state.hexdigest()


def iter_array(stream: TextIO, marker: str, *, anchor: str | None = None) -> Iterator[Any]:
    def append(buffer: str, label: str) -> str:
        block = stream.read(CHARS)
        need(bool(block), label)
        combined = buffer + block
        need(len(combined.encode("utf-8")) <= BUFFER_CAP, "parser buffer cap")
        return combined

    def seek(token: str, initial: str) -> str:
        buffer = initial
        while True:
            at = buffer.find(token)
            if at >= 0:
                return buffer[at + len(token):]
            buffer = append(buffer, "missing marker:" + token)
            at = buffer.find(token)
            if at >= 0:
                return buffer[at + len(token):]
            buffer = buffer[-max(1, len(token) - 1):]

    buffer = ""
    if anchor is not None:
        buffer = seek(anchor, buffer)
    buffer = seek(marker, buffer)
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
                need(len(buffer.encode("utf-8")) <= MAX_ROW, "incomplete row source cap")
                buffer = append(buffer, "truncated JSON row")
        need(len(buffer[:end].encode("utf-8")) <= MAX_ROW, "successful source row cap")
        need(len(canonical(value)) <= MAX_ROW, "successful canonical row cap")
        yield value
        buffer = buffer[end:]
        comma = True


class PinnedInputs:
    def __init__(self) -> None:
        self.dirfd = -1
        self.dir_before: os.stat_result | None = None
        self.files: dict[str, tuple[int, os.stat_result, int, str, str]] = {}
        self.pin_rows: list[dict[str, Any]] = []

    def __enter__(self) -> "PinnedInputs":
        named = os.stat(DELIVERABLES, follow_symlinks=False)
        need(stat.S_ISDIR(named.st_mode), "deliverables real directory")
        self.dirfd = os.open(DELIVERABLES, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
        self.dir_before = os.fstat(self.dirfd)
        need(directory_identity(named) == directory_identity(self.dir_before), "deliverables dirfd binding")
        try:
            for label, filename, size, sha in INPUT_PINS:
                before = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
                need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and before.st_size == size, "regular single-link size pin:" + label)
                fd = os.open(filename, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0), dir_fd=self.dirfd)
                opened = os.fstat(fd)
                need(fingerprint(before) == fingerprint(opened), "path/open race:" + label)
                n, h = hash_fd(fd, size)
                need(n == size and h == sha, "first byte pin:" + label)
                self.files[label] = (fd, opened, size, sha, filename)
                self.pin_rows.append({"label": label, "filename": filename, "exact_size": size, "sha256": sha, "pass1_sha256": h, "regular": True, "nlink_one": True})
            return self
        except Exception:
            self.close(False)
            raise

    def stream(self, label: str, marker: str, *, anchor: str | None = None) -> Iterator[Any]:
        fd, before, _, _, filename = self.files[label]
        os.lseek(fd, 0, os.SEEK_SET)
        raw = os.fdopen(os.dup(fd), "rb")
        binary: BinaryIO = gzip.GzipFile(fileobj=raw, mode="rb") if filename.endswith(".gz") else raw
        text = io.TextIOWrapper(binary, encoding="utf-8", newline="")
        try:
            yield from iter_array(text, marker, anchor=anchor)
        finally:
            text.close()
            if not raw.closed:
                raw.close()
            need(fingerprint(os.fstat(fd)) == fingerprint(before), "held FD stable after parse:" + label)

    def small_json(self, label: str) -> Any:
        fd, before, size, _, _ = self.files[label]
        need(size <= MAX_ROW, "small JSON cap")
        raw = os.pread(fd, size, 0)
        need(len(raw) == size and fingerprint(os.fstat(fd)) == fingerprint(before), "small held read")
        value = DECODER.decode(raw.decode("utf-8"))
        need(len(canonical(value)) <= MAX_ROW, "small canonical cap")
        return value

    def close(self, verify: bool = True) -> None:
        error: Exception | None = None
        for label, (fd, before, size, sha, filename) in list(self.files.items()):
            try:
                if verify:
                    n, h = hash_fd(fd, size)
                    named = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
                    need(n == size and h == sha and fingerprint(before) == fingerprint(os.fstat(fd)) == fingerprint(named), "final path/FD rebind:" + label)
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
                    need(directory_identity(self.dir_before) == directory_identity(os.fstat(self.dirfd)) == directory_identity(os.stat(DELIVERABLES, follow_symlinks=False)), "deliverables directory replaced")
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


def table_finish(label: str, audit: ListHash) -> dict[str, Any]:
    count, sha = EXPECTED_TABLES[label]
    observed = audit.finish()
    need(audit.count == count and observed == sha, label + ":ordered table commitment")
    return {"table": label, "row_count": count, "rows_sha256": sha, "all_rows_own_sha256_checked": True}


def insert_many(db: sqlite3.Connection, sql: str, batch: list[tuple[Any, ...]], threshold: int = 2048) -> None:
    if len(batch) >= threshold:
        db.executemany(sql, batch)
        batch.clear()


def scalar(db: sqlite3.Connection, sql: str, parameters: tuple[Any, ...] = ()) -> Any:
    row = db.execute(sql, parameters).fetchone()
    need(row is not None, "scalar query empty")
    return row[0]


ZERO_MEMBER_CREDIT = {"normalized_support": 0, "representation_cover": 0, "physical_incidence": 0, "A1_A2": 0, "B1A": 0, "B2": 0, "D02": 0, "CM2": 0}
ZERO_REPRESENTATION_CREDIT = {"normalized_support": 0, "representation_cover": 0, "physical_incidence": 0, "pullback_equivalence": 0, "B1A": 0, "B2": 0}


def source_cell_commitments(db: sqlite3.Connection, cell_ids: list[str]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for cell_id in cell_ids:
        row = db.execute("SELECT row_sha FROM cell WHERE cell_id=?", (cell_id,)).fetchone()
        need(row is not None, "source cell commitment missing")
        out.append({"cell_id": cell_id, "row_sha256": row[0]})
    return out


def primary_input_commitment(
    member_id: str,
    union_row_id: str,
    member_row_sha: str,
    cell_rows: list[dict[str, str]],
    registry_row_id: str,
    registry_row_sha: str,
    r288_row_id: str,
    r288_row_sha: str,
    canonical_atom_id: str,
    b0_row_id: str,
    b0_row_sha: str,
) -> dict[str, Any]:
    return {
        "domain": SCHEMA + ".primary-handle-input.v2",
        "member_id": member_id,
        "member_union_row_id": union_row_id,
        "member_union_row_sha256": member_row_sha,
        "predicate_source_cells": cell_rows,
        "R294_registry_row_id": registry_row_id,
        "R294_registry_row_sha256": registry_row_sha,
        "R288_atom_row_id": r288_row_id,
        "R288_atom_row_sha256": r288_row_sha,
        "R288_canonical_atom_id": canonical_atom_id,
        "B0_row_id": b0_row_id,
        "B0_row_sha256": b0_row_sha,
    }


def primary_handle(commitment: dict[str, Any]) -> tuple[str, str]:
    sha = digest(commitment)
    return "round306b1af4k2i1-r2-primary:" + sha, sha


def member_rows(db: sqlite3.Connection) -> Iterator[dict[str, Any]]:
    query = """
      SELECT m.member_id,m.component_id,m.union_row_id,m.multiplicity,m.cell_ids_json,m.row_sha,
             r.registry_row_id,r.row_sha,r.source_row_id,r.source_row_sha,r.atom_id,b.b0_row_id,b.row_sha
      FROM member m JOIN registry r ON r.member_id=m.member_id
      JOIN b0 b ON b.member_id=m.member_id ORDER BY m.member_id
    """
    for member_id, component_id, union_id, multiplicity, cell_json, member_sha, registry_id, registry_sha, r288_id, r288_sha, atom_id, b0_id, b0_sha in db.execute(query):
        cell_ids = json.loads(cell_json)
        cell_rows = source_cell_commitments(db, cell_ids)
        input_commitment = primary_input_commitment(member_id, union_id, member_sha, cell_rows, registry_id, registry_sha, r288_id, r288_sha, atom_id, b0_id, b0_sha)
        handle, commitment = primary_handle(input_commitment)
        yield closed({
            "schema": SCHEMA + ".member-row",
            "status": "MECHANICAL_IDENTITY_JOINED__SEMANTIC_SUPPORT_NOT_PROVED",
            "coarse_family": "R2",
            "member_id": member_id,
            "component_id": component_id,
            "member_union_row_id": union_id,
            "primary_representation_handle_id": handle,
            "primary_representation_input_commitment_sha256": commitment,
            "canonical_input_commitment": input_commitment,
            "predicate_source_cell_count": multiplicity,
            "predicate_source_cell_row_ids": cell_ids,
            "source_B1R0_member_row_sha256": member_sha,
            "source_R294_registry_row_id": registry_id,
            "source_R294_registry_row_sha256": registry_sha,
            "source_R288_atom_row_id": r288_id,
            "source_R288_atom_row_sha256": r288_sha,
            "source_R288_canonical_atom_id": atom_id,
            "source_B0_row_id": b0_id,
            "source_B0_row_sha256": b0_sha,
            "transition_ready_handle_status": "IDENTITY_ROUTABLE_ONLY__NO_TRANSITION_THEOREM_CREDIT",
            "formal_credit": ZERO_MEMBER_CREDIT,
        })


def representation_rows(db: sqlite3.Connection) -> Iterator[dict[str, Any]]:
    query = """SELECT m.member_id,m.union_row_id,m.cell_ids_json,m.row_sha,r.registry_row_id,r.row_sha,
                      r.source_row_id,r.source_row_sha,r.atom_id,b.b0_row_id,b.row_sha
               FROM member m JOIN registry r ON r.member_id=m.member_id
               JOIN b0 b ON b.member_id=m.member_id ORDER BY m.member_id"""
    for member_id, union_id, cell_json, member_sha, registry_id, registry_sha, r288_id, r288_sha, atom_id, b0_id, b0_sha in db.execute(query):
        cell_ids = json.loads(cell_json)
        cell_rows = source_cell_commitments(db, cell_ids)
        input_commitment = primary_input_commitment(member_id, union_id, member_sha, cell_rows, registry_id, registry_sha, r288_id, r288_sha, atom_id, b0_id, b0_sha)
        handle, commitment = primary_handle(input_commitment)
        cell_commitment = digest({"ordered_cell_rows": cell_rows})
        yield closed({
            "schema": SCHEMA + ".representation-row",
            "status": "TRANSITION_READY_IDENTITY_HANDLE__SEMANTIC_SUPPORT_BLOCKED",
            "representation_role": "PRIMARY_MEMBER_PREDICATE_UNION_HANDLE",
            "representation_id": handle,
            "owner_member_id": member_id,
            "coverage_semantics": "MECHANICAL_MEMBER_UNION_IDENTITY_ONLY__FULL_SET_EQUALITY_NOT_PROVED",
            "transition_payload_sha256": commitment,
            "canonical_input_commitment": input_commitment,
            "predicate_source_cell_count": len(cell_ids),
            "predicate_source_cell_ids_sha256": cell_commitment,
            "source_B1R0_member_union_row_id": union_id,
            "source_B1R0_member_row_sha256": member_sha,
            "source_R294_binding_row_id": None,
            "source_R294_binding_row_sha256": None,
            "source_R287_row_id": None,
            "source_R287_row_sha256": None,
            "source_R294_target_registry_row_id": registry_id,
            "source_R294_target_registry_row_sha256": registry_sha,
            "source_R288_atom_row_id": r288_id,
            "source_R288_atom_row_sha256": r288_sha,
            "source_B0_row_id": b0_id,
            "source_B0_row_sha256": b0_sha,
            "formal_credit": ZERO_REPRESENTATION_CREDIT,
        })
    query = """
      SELECT b.source_rep_id,b.target_member_id,b.source_kind,b.source_row_id,b.source_row_sha,
             b.binding_row_id,b.row_sha,b.source_atom_row_id,b.source_atom_row_sha,
             r.registry_row_id,r.row_sha,x.b0_row_id,x.row_sha
      FROM binding b JOIN member m ON m.member_id=b.target_member_id
      JOIN registry r ON r.member_id=b.target_member_id JOIN b0 x ON x.member_id=b.target_member_id
      ORDER BY b.source_rep_id
    """
    for rep_id, owner, kind, source_row_id, source_row_sha, binding_id, binding_sha, r288_id, r288_sha, registry_id, registry_sha, b0_id, b0_sha in db.execute(query):
        payload = {"domain": SCHEMA + ".alias-handle-input.v2", "representation_id": rep_id, "owner_member_id": owner, "source_kind": kind, "R287_source_row_id": source_row_id, "R287_source_row_sha256": source_row_sha, "R294_binding_row_id": binding_id, "R294_binding_row_sha256": binding_sha, "R288_atom_row_id": r288_id, "R288_atom_row_sha256": r288_sha, "R294_target_registry_row_id": registry_id, "R294_target_registry_row_sha256": registry_sha, "B0_row_id": b0_id, "B0_row_sha256": b0_sha}
        yield closed({
            "schema": SCHEMA + ".representation-row",
            "status": "TRANSITION_READY_IDENTITY_HANDLE__GLOBAL_SUPPORT_EQUIVALENCE_BLOCKED",
            "representation_role": "R287_EXACT_SUBCOVER_ALIAS",
            "representation_id": rep_id,
            "owner_member_id": owner,
            "coverage_semantics": "UPSTREAM_EXACT_SUBCOVER_ALIAS_IDENTITY_ONLY__GLOBAL_SET_EQUALITY_NOT_PROVED",
            "transition_payload_sha256": digest(payload),
            "canonical_input_commitment": payload,
            "predicate_source_cell_count": None,
            "predicate_source_cell_ids_sha256": None,
            "source_B1R0_member_union_row_id": None,
            "source_B1R0_member_row_sha256": None,
            "source_R294_binding_row_id": binding_id,
            "source_R294_binding_row_sha256": binding_sha,
            "source_R287_row_id": source_row_id,
            "source_R287_row_sha256": source_row_sha,
            "source_R294_target_registry_row_id": registry_id,
            "source_R294_target_registry_row_sha256": registry_sha,
            "source_R288_atom_row_id": r288_id,
            "source_R288_atom_row_sha256": r288_sha,
            "source_B0_row_id": b0_id,
            "source_B0_row_sha256": b0_sha,
            "formal_credit": ZERO_REPRESENTATION_CREDIT,
        })


def wtail_rows(db: sqlite3.Connection) -> Iterator[dict[str, Any]]:
    for member_id, union_id, cell_json, normalization_json, member_sha in db.execute("SELECT member_id,union_row_id,cell_ids_json,normalization_json,row_sha FROM member WHERE multiplicity=2 ORDER BY member_id"):
        cell_ids = json.loads(cell_json)
        normalization = json.loads(normalization_json)
        cell_rows = source_cell_commitments(db, cell_ids)
        input_commitment = {"domain": SCHEMA + ".wtail-gap-input.v2", "member_id": member_id, "member_union_row_id": union_id, "member_union_row_sha256": member_sha, "predicate_source_cells": cell_rows, "parent_normalization": normalization}
        yield closed({
            "schema": SCHEMA + ".wtail-blocked-obligation-row",
            "status": "BLOCKED_IN_THIS_MECHANICAL_LANE__SEMANTIC_KERNEL_NOT_CONSUMED",
            "obligation_kind": "W_TAIL_TWO_CHILD_ARTIFICIAL_FACE_REGLUE_PHYSICAL_EQUIVALENCE",
            "member_id": member_id,
            "source_B1R0_member_union_row_id": union_id,
            "source_B1R0_member_row_sha256": member_sha,
            "predicate_source_cell_row_ids": cell_ids,
            "source_parent_normalization": normalization,
            "canonical_input_commitment": input_commitment,
            "canonical_input_commitment_sha256": digest(input_commitment),
            "external_semantic_kernel_status": "NOT_CONSUMED_BY_THIS_MECHANICAL_IDENTITY_LANE",
            "formal_credit": {"artificial_face_reglue": 0, "physical_incidence": 0, "pullback_equivalence": 0, "normalized_support": 0, "representation_cover": 0},
        })


def write_jsonl_gzip(path: Path, rows: Iterable[dict[str, Any]], order: str) -> dict[str, Any]:
    raw_sha = hashlib.sha256()
    raw_size = count = 0
    with path.open("wb") as target:
        with gzip.GzipFile(filename="", mode="wb", fileobj=target, compresslevel=9, mtime=0) as zipped:
            for row in rows:
                wire = canonical(row) + b"\n"
                need(len(wire) <= MAX_ROW + 1, "output row cap")
                raw_sha.update(wire)
                raw_size += len(wire)
                count += 1
                zipped.write(wire)
        target.flush()
        os.fsync(target.fileno())
    named = os.stat(path, follow_symlinks=False)
    need(stat.S_ISREG(named.st_mode) and named.st_nlink == 1, "staged ledger regular single-link")
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
    try:
        opened = os.fstat(fd)
        need(fingerprint(named) == fingerprint(opened), "staged ledger open binding")
        size, sha = hash_fd(fd, named.st_size)
        need(fingerprint(opened) == fingerprint(os.fstat(fd)) == fingerprint(os.stat(path, follow_symlinks=False)), "staged ledger final binding")
    finally:
        os.close(fd)
    return {"filename": path.name, "row_count": count, "uncompressed_jsonl_size": raw_size, "uncompressed_jsonl_sha256": raw_sha.hexdigest(), "file_size": size, "file_sha256": sha, "order": order}


def build_database(pins: PinnedInputs, db: sqlite3.Connection) -> tuple[list[dict[str, Any]], dict[str, Any]]:
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
        audit = ListHash()
        batch: list[tuple[Any, ...]] = []
        for row in pins.stream("R287", marker):
            row_hash(row, label)
            audit.add(row)
            batch.append((row[id_field], kind, row[rep_field], row["row_sha256"]))
            insert_many(db, "INSERT INTO r287 VALUES(?,?,?,?)", batch)
        if batch:
            db.executemany("INSERT INTO r287 VALUES(?,?,?,?)", batch)
        receipts.append(table_finish(label, audit))

    audit = ListHash()
    batch = []
    for row in pins.stream("R288", '"rows"'):
        row_hash(row, "R288")
        audit.add(row)
        candidate = row["reserved_candidate_occurrence_id__not_issued"]
        need(candidate is None or type(candidate) is str, "R288 candidate member ID type")
        if candidate is not None:
            batch.append((row["Round288_atom_disposition_row_id"], row["canonical_atom_id"], candidate, row["row_sha256"]))
            insert_many(db, "INSERT INTO r288 VALUES(?,?,?,?)", batch)
    if batch:
        db.executemany("INSERT INTO r288 VALUES(?,?,?,?)", batch)
    receipts.append(table_finish("R288", audit))

    audit = ListHash()
    batch = []
    for row in pins.stream("R294_REGISTRY", '"rows"'):
        row_hash(row, "R294 registry")
        audit.add(row)
        if row["registry_entry_kind"] != "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM":
            continue
        need(type(row["formal_new_expanded_occurrence_credit"]) is int and row["formal_new_expanded_occurrence_credit"] == 1, "R294 R2 formal identity credit")
        need(row["registry_identity_status"] == "FORMALLY_ISSUED_ROUND294_ATOMIC_OCCURRENCE_ID" and row["registry_promotion_status"] == "FORMALLY_PROMOTED_ROUND294_ATOMIC_OCCURRENCE_REGISTRY", "R294 R2 registry identity status")
        batch.append((row["Round294_occurrence_registry_row_id"], row["registry_occurrence_id"], row["source_row_id"], row["source_row_sha256"], row["canonical_atom_id"], row["row_sha256"]))
        insert_many(db, "INSERT INTO registry VALUES(?,?,?,?,?,?)", batch)
    if batch:
        db.executemany("INSERT INTO registry VALUES(?,?,?,?,?,?)", batch)
    receipts.append(table_finish("R294_REGISTRY", audit))

    audit = ListHash()
    batch = []
    for row in pins.stream("R294_BINDINGS", '"rows"'):
        row_hash(row, "R294 binding")
        audit.add(row)
        if row["alias_source_kind"] not in ("ROUND287_R275_REGION_INCLUSION_SUBCOVER", "ROUND287_R286_SIGNED_CELL_INCLUSION_SUBCOVER"):
            continue
        need(row["support_representation_kind"] == "EXACT_SAME_POSITIVE_OPEN_REGION_INCLUSION_SUBCOVER", "R287 alias support kind")
        need(type(row["formal_occurrence_alias_credit"]) is int and row["formal_occurrence_alias_credit"] == 1 and row["does_not_issue_new_occurrence_id"] is True and row["does_not_collapse_distinct_occurrence_ids"] is True, "R294 alias identity authority")
        batch.append((row["Round294_occurrence_representation_binding_row_id"], row["source_representation_id"], row["alias_source_kind"], row["source_row_id"], row["source_row_sha256"], row["source_Round288_atom_disposition_row_id"], row["source_Round288_atom_disposition_row_sha256"], row["target_registry_occurrence_id"], row["row_sha256"]))
        insert_many(db, "INSERT INTO binding VALUES(?,?,?,?,?,?,?,?,?)", batch)
    if batch:
        db.executemany("INSERT INTO binding VALUES(?,?,?,?,?,?,?,?,?)", batch)
    receipts.append(table_finish("R294_BINDINGS", audit))

    audit = ListHash()
    batch = []
    for row in pins.stream("B1R0_CELLS", '"predicate_source_cell_rows"'):
        row_hash(row, "B1R0 cell")
        audit.add(row)
        need(row["formal_full_support_credit"] == 0, "B1R0 cell zero support credit")
        batch.append((row["Round306B1R0_predicate_source_cell_row_id"], row["formal_member_id"], row["row_sha256"]))
        insert_many(db, "INSERT INTO cell VALUES(?,?,?)", batch)
    if batch:
        db.executemany("INSERT INTO cell VALUES(?,?,?)", batch)
    receipts.append(table_finish("B1R0_CELLS", audit))

    audit = ListHash()
    members: list[tuple[Any, ...]] = []
    edges: list[tuple[Any, ...]] = []
    for row in pins.stream("B1R0_MEMBERS", '"member_union_rows"'):
        row_hash(row, "B1R0 member")
        audit.add(row)
        n = row["predicate_source_cell_multiplicity"]
        ids = row["predicate_source_cell_row_ids"]
        need(type(n) is int and n in (1, 2) and type(ids) is list and len(ids) == n and len(set(ids)) == n, "member cell list")
        need((n == 2) is (row["Round271_W_tail_parent_normalization"] is not None), "W-tail normalization iff two-cell member")
        need(row["formal_full_support_credit"] == 0 and row["full_support_union_theorem_status"] == "PENDING_SOURCE_FREE_INTERVAL_PREDICATE_EQUIVALENCE", "member zero support theorem")
        members.append((row["member_id"], row["Round306B1R0_member_union_row_id"], row["Round294_registry_row_id"], row["Round306B0_member_source_row_id"], row["Round306A_component_id"], n, canonical(ids).decode("ascii"), canonical(row["Round271_W_tail_parent_normalization"]).decode("ascii") if row["Round271_W_tail_parent_normalization"] is not None else None, row["row_sha256"]))
        edges.extend((cell_id, row["member_id"]) for cell_id in ids)
        insert_many(db, "INSERT INTO member VALUES(?,?,?,?,?,?,?,?,?)", members)
        insert_many(db, "INSERT INTO edge VALUES(?,?)", edges)
    if members:
        db.executemany("INSERT INTO member VALUES(?,?,?,?,?,?,?,?,?)", members)
    if edges:
        db.executemany("INSERT INTO edge VALUES(?,?)", edges)
    receipts.append(table_finish("B1R0_MEMBERS", audit))

    audit = ListHash()
    batch = []
    for row in pins.stream("B0", '"member_support_source_rows"'):
        row_hash(row, "B0")
        audit.add(row)
        if row["identity_tranche"] != "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM":
            continue
        need(row["primary_source_package"] == "R294" and row["identity_class"] == "FORMAL_OCCURRENCE" and row["member_identity_preserved"] is True, "B0 R2 identity authority")
        batch.append((row["member_id"], row["Round306B0_member_support_source_row_id"], row["Round306A_component_id"], row["primary_source_row_id"], row["primary_source_row_sha256"], row["row_sha256"]))
        insert_many(db, "INSERT INTO b0 VALUES(?,?,?,?,?,?)", batch)
    if batch:
        db.executemany("INSERT INTO b0 VALUES(?,?,?,?,?,?)", batch)
    receipts.append(table_finish("B0", audit))
    db.commit()
    db.executescript("""
      CREATE INDEX binding_target ON binding(target_member_id);
      CREATE INDEX binding_source_row ON binding(source_row_id);
      CREATE INDEX edge_member ON edge(member_id);
    """)

    need(scalar(db, "SELECT COUNT(*) FROM cell") == 295_340, "R2 source-cell count")
    need(scalar(db, "SELECT COUNT(*) FROM member") == 295_336, "R2 member count")
    need(dict(db.execute("SELECT multiplicity,COUNT(*) FROM member GROUP BY multiplicity")) == {1: 295_332, 2: 4}, "R2 member multiplicity")
    need(scalar(db, "SELECT COUNT(*) FROM edge") == 295_340, "R2 edge count")
    need(scalar(db, "SELECT COUNT(*) FROM edge e LEFT JOIN cell c ON c.cell_id=e.cell_id WHERE c.cell_id IS NULL OR c.member_id<>e.member_id") == 0, "member/cell edge join")
    need(scalar(db, "SELECT COUNT(*) FROM cell c LEFT JOIN edge e ON e.cell_id=c.cell_id WHERE e.cell_id IS NULL OR e.member_id<>c.member_id") == 0, "cell/member exhaustion")
    need(scalar(db, "SELECT COUNT(*) FROM registry") == 295_336, "R2 registry count")
    need(scalar(db, "SELECT COUNT(*) FROM r288") == 295_336, "R288 candidate identity count")
    need(scalar(db, "SELECT COUNT(*) FROM registry r LEFT JOIN r288 a ON a.source_row_id=r.source_row_id WHERE a.source_row_id IS NULL OR a.row_sha<>r.source_row_sha OR a.atom_id<>r.atom_id OR a.candidate_member_id<>r.member_id") == 0, "registry/R288 source join")
    need(scalar(db, "SELECT COUNT(*) FROM member m LEFT JOIN registry r ON r.registry_row_id=m.registry_row_id WHERE r.registry_row_id IS NULL OR r.member_id<>m.member_id") == 0, "member/registry join")
    need(scalar(db, "SELECT COUNT(*) FROM b0") == 295_336, "R2 B0 count")
    need(scalar(db, "SELECT COUNT(*) FROM member m LEFT JOIN b0 b ON b.member_id=m.member_id LEFT JOIN registry r ON r.member_id=m.member_id WHERE b.member_id IS NULL OR b.b0_row_id<>m.b0_row_id OR b.component_id<>m.component_id OR b.registry_row_id<>r.registry_row_id OR b.registry_row_sha<>r.row_sha") == 0, "member/B0/registry join")

    r2_alias_where = "EXISTS(SELECT 1 FROM member m WHERE m.member_id=binding.target_member_id)"
    need(scalar(db, "SELECT COUNT(*) FROM binding WHERE " + r2_alias_where) == 7_288, "R2 alias count")
    alias_counts = dict(db.execute("SELECT source_kind,COUNT(*) FROM binding b WHERE EXISTS(SELECT 1 FROM member m WHERE m.member_id=b.target_member_id) GROUP BY source_kind"))
    need(alias_counts == {"ROUND287_R275_REGION_INCLUSION_SUBCOVER": 2_476, "ROUND287_R286_SIGNED_CELL_INCLUSION_SUBCOVER": 4_812}, "R2 alias source census")
    need(scalar(db, "SELECT COUNT(DISTINCT source_rep_id) FROM binding b WHERE EXISTS(SELECT 1 FROM member m WHERE m.member_id=b.target_member_id)") == 7_288, "R2 alias source uniqueness")
    need(scalar(db, "SELECT COUNT(DISTINCT target_member_id) FROM binding b WHERE EXISTS(SELECT 1 FROM member m WHERE m.member_id=b.target_member_id)") == 384, "R2 alias owner count")
    need(scalar(db, "SELECT COUNT(*) FROM binding b JOIN member m ON m.member_id=b.target_member_id LEFT JOIN r287 s ON s.source_row_id=b.source_row_id WHERE s.source_row_id IS NULL OR s.row_sha<>b.source_row_sha OR s.source_kind<>b.source_kind OR s.source_rep_id<>b.source_rep_id") == 0, "R2 alias/R287 source join")
    need(scalar(db, "SELECT COUNT(*) FROM binding b JOIN member m ON m.member_id=b.target_member_id LEFT JOIN r288 a ON a.source_row_id=b.source_atom_row_id WHERE a.source_row_id IS NULL OR a.row_sha<>b.source_atom_row_sha") == 0, "R2 alias/R288 atom join")
    need(scalar(db, "SELECT COUNT(*) FROM binding b JOIN registry r ON r.member_id=b.target_member_id WHERE b.source_atom_row_id<>r.source_row_id OR b.source_atom_row_sha<>r.source_row_sha") == 0, "R2 alias atom/target-registry owner backbinding")

    handle_ids: set[str] = set()
    for member_id, union_id, cell_json, member_sha, registry_id, registry_sha, r288_id, r288_sha, atom_id, b0_id, b0_sha in db.execute("SELECT m.member_id,m.union_row_id,m.cell_ids_json,m.row_sha,r.registry_row_id,r.row_sha,r.source_row_id,r.source_row_sha,r.atom_id,b.b0_row_id,b.row_sha FROM member m JOIN registry r ON r.member_id=m.member_id JOIN b0 b ON b.member_id=m.member_id"):
        ids = json.loads(cell_json)
        input_commitment = primary_input_commitment(member_id, union_id, member_sha, source_cell_commitments(db, ids), registry_id, registry_sha, r288_id, r288_sha, atom_id, b0_id, b0_sha)
        handle, _ = primary_handle(input_commitment)
        need(handle not in handle_ids, "primary handle collision")
        handle_ids.add(handle)
    need(scalar(db, "SELECT COUNT(*) FROM binding b JOIN member m ON m.member_id=b.target_member_id WHERE b.source_rep_id LIKE 'round306b1af4k2i1-r2-primary:%'") == 0, "primary/alias representation ID disjointness")

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


def produce(output_directory: Path, _seed: str) -> dict[str, Any]:
    output_directory = Path(os.path.abspath(output_directory))
    output_named = os.stat(output_directory, follow_symlinks=False)
    need(stat.S_ISDIR(output_named.st_mode), "real output directory")
    output_fd = os.open(output_directory, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
    need(directory_identity(output_named) == directory_identity(os.fstat(output_fd)), "output held-dirfd binding")
    root = "/tmp"
    need(os.path.realpath(root) == root, "explicit /tmp authority")
    root_named = os.stat(root, follow_symlinks=False)
    need(stat.S_ISDIR(root_named.st_mode), "/tmp real directory")
    root_fd = os.open(root, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
    need(directory_identity(root_named) == directory_identity(os.fstat(root_fd)), "/tmp held-dirfd binding")
    need(os.path.commonpath((root, str(output_directory))) != str(output_directory), "/tmp outside output")
    try:
        with tempfile.TemporaryDirectory(prefix="cm2-k2i1-r2-", dir=root) as scratch_name:
            scratch_real = os.path.realpath(scratch_name)
            need(os.path.dirname(scratch_real) == root, "scratch placement")
            scratch = Path(scratch_real)
            scratch_named = os.stat(scratch, follow_symlinks=False)
            scratch_fd = os.open(scratch, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
            need(directory_identity(scratch_named) == directory_identity(os.fstat(scratch_fd)), "scratch held-dirfd binding")
            try:
                db = sqlite3.connect(scratch / "r2-index.sqlite3")
                try:
                    with PinnedInputs() as pins:
                        af2 = pins.small_json("AF2_RESULT")
                        need(af2["member_count"] == 564_492 and af2["coarse_partition"]["R2_predicate_union_members"] == 295_336 and af2["R2"]["predicate_cell_reference_count"] == 295_340 and af2["formal_credit"] == 0, "AF2 R2 denominator/credit")
                        source_receipts, census = build_database(pins, db)
                        pin_rows = pins.pin_rows
                    ledger_meta = {
                        "member": write_jsonl_gzip(scratch / OUTPUTS["member"], member_rows(db), "member_id_unsigned_bytewise_ASCII_ASC"),
                        "representation": write_jsonl_gzip(scratch / OUTPUTS["representation"], representation_rows(db), "PRIMARY_BY_member_id_THEN_ALIAS_BY_source_representation_id__unsigned_bytewise_ASCII_ASC"),
                        "wtail_gap": write_jsonl_gzip(scratch / OUTPUTS["wtail_gap"], wtail_rows(db), "member_id_unsigned_bytewise_ASCII_ASC"),
                    }
                finally:
                    db.close()

                need(ledger_meta["member"]["row_count"] == 295_336, "member ledger count")
                need(ledger_meta["representation"]["row_count"] == 302_624, "representation ledger count")
                need(ledger_meta["wtail_gap"]["row_count"] == 4, "W-tail gap ledger count")
                result = {
                    "schema": SCHEMA,
                    "status": STATUS,
                    "scope": "R2_ONLY_MECHANICAL_IDENTITY_REPRESENTATION_LANE",
                    "producer_sha256": None,
                    "producer_byte_binding": "EXTERNAL_INDEPENDENT_VERIFIER_STATIC_PIN_ONLY",
                    "seed_affects_output": False,
                    "input_pins": pin_rows,
                    "source_table_commitments": source_receipts,
                    "exact_census": census,
                    "ledgers": ledger_meta,
                    "closed_anti_joins": {
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
                    },
                    "known_gaps": {
                        "R2_source_free_interval_predicate_equivalence_not_discharged": 295_336,
                        "R2_W_tail_artificial_face_reglue_not_discharged_in_this_lane": 4,
                        "R2_representation_handles_without_global_set_equality_theorem": 302_624,
                        "remaining_coarse_families_not_emitted": ["PRESERVED", "NON_GRAPH", "R292", "G2A", "G2B"],
                        "remaining_member_identity_rows_not_emitted": 269_156,
                        "remaining_global_representation_rows_not_emitted": 309_280,
                        "A1_A2_obligations_not_enumerated_in_this_lane": 80_092,
                    },
                    "availability_boundary": {"bounded_memory_claim": False, "runtime_or_RSS_upper_bound_proved": False, "failure_before_result_marker_mints_credit": False},
                    "formal_credit": {"normalized_support": 0, "representation_cover": 0, "physical_incidence": 0, "pullback_equivalence": 0, "A1_A2": 0, "B1A": 0, "B2": 0, "maximality": 0, "fibre": 0, "global_disposition": 0, "D02": 0, "D03": 0, "D04": 0, "Gate5": 0, "CM2": 0},
                }
                result_path = scratch / OUTPUTS["result"]
                result_path.write_bytes(canonical(result) + b"\n")
                with result_path.open("rb") as handle:
                    os.fsync(handle.fileno())
                for key in ("member", "representation", "wtail_gap", "result"):
                    name = OUTPUTS[key]
                    staged = os.stat(name, dir_fd=scratch_fd, follow_symlinks=False)
                    need(stat.S_ISREG(staged.st_mode) and staged.st_nlink == 1, "staged regular single-link:" + key)
                    os.replace(name, name, src_dir_fd=scratch_fd, dst_dir_fd=output_fd)
                    published = os.stat(name, dir_fd=output_fd, follow_symlinks=False)
                    need(stat.S_ISREG(published.st_mode) and published.st_nlink == 1 and published.st_size == staged.st_size, "published file:" + key)
                os.fsync(output_fd)
                need(directory_identity(scratch_named) == directory_identity(os.fstat(scratch_fd)), "scratch final binding")
            finally:
                os.close(scratch_fd)
        need(directory_identity(root_named) == directory_identity(os.fstat(root_fd)) == directory_identity(os.stat(root, follow_symlinks=False)), "/tmp final binding")
        need(directory_identity(output_named) == directory_identity(os.fstat(output_fd)) == directory_identity(os.stat(output_directory, follow_symlinks=False)), "output final binding")
        return result
    finally:
        os.close(root_fd)
        os.close(output_fd)


def self_test() -> dict[str, Any]:
    row = closed({"x": 0, "flag": False})
    need(row_hash(row, "self-test") == row["row_sha256"], "closed row positive")
    broken = dict(row)
    broken["x"] = 1
    rejected = False
    try:
        row_hash(broken, "mutated")
    except Blocked:
        rejected = True
    need(rejected, "mutated row rejected")
    body = {"x": "a" * (MAX_ROW - len(canonical({"x": ""})))}
    wire = canonical(body)
    need(len(wire) == MAX_ROW and list(iter_array(io.StringIO('{"rows":[' + wire.decode("ascii") + ']}' ), '"rows"')) == [body], "exact row cap accepted")
    overflow = {"x": body["x"] + "a"}
    cap_rejected = False
    try:
        list(iter_array(io.StringIO('{"rows":[' + canonical(overflow).decode("ascii") + ']}' ), '"rows"'))
    except Blocked:
        cap_rejected = True
    need(cap_rejected, "cap plus one rejected")
    return {"schema": SCHEMA + ".producer-self-test", "status": "PASS", "mutation_rejected": True, "decoded_row_exact_cap": MAX_ROW, "decoded_row_cap_plus_one_rejected": True, "candidate_is_formal": False}


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--produce", action="store_true")
    parser.add_argument("--output-directory")
    parser.add_argument("--hash-seed", default="0")
    args = parser.parse_args()
    if args.self_test:
        need(args.output_directory is None, "self-test filesystem inert")
        print(canonical(self_test()).decode("ascii"))
        return 0
    need(args.output_directory is not None, "production output directory required")
    result = produce(Path(args.output_directory), args.hash_seed)
    print(canonical({"status": result["status"], "result_sha256": digest(result)}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
