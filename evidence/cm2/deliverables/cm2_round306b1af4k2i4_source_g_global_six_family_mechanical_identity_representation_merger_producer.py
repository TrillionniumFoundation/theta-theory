#!/usr/bin/env python3
"""Global six-family mechanical identity/representation merger.

This program consumes only sealed K2I0/K2I1/K2I2/K2I3 packages plus the
frozen B0 universe and AF2 census.  It merges identities and mechanical
representation handles; it proves no support, representation-cover,
transition, maximality, fibre, disposition, D-gate, Gate5, or CM2 theorem.
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


PREFIX = "cm2_round306b1af4k2i4_source_g_global_six_family_mechanical_identity_representation_merger_"
PRODUCER_FILENAME = PREFIX + "producer.py"
SCHEMA = "cm2.round306b1af4k2i4.source-g-global-six-family-mechanical-identity-representation-merger.v1"
STATUS = "PASS_EXACT_GLOBAL_SIX_FAMILY_MECHANICAL_IDENTITY_REPRESENTATION_CENSUS__ZERO_THEOREM_CREDIT"
DELIVERABLES = Path(__file__).resolve().parent
HEX64 = re.compile(r"^[0-9a-f]{64}$")
MAX_ROW = 8 << 20
CHARS = 1 << 18
BUFFER_CAP = MAX_ROW + 4 * CHARS

FAMILY_ORDER = ("PRESERVED", "NON_GRAPH", "R2", "R292", "G2A", "G2B")
FAMILY_RANK = {family: rank for rank, family in enumerate(FAMILY_ORDER)}
FAMILY_LANE = {"PRESERVED": "I2", "NON_GRAPH": "I2", "R2": "I1", "R292": "I0", "G2A": "I3", "G2B": "I3"}
EXPECTED_MEMBER_COUNTS = {
    "PRESERVED": 126_468,
    "NON_GRAPH": 17_828,
    "R2": 295_336,
    "R292": 9_404,
    "G2A": 38_624,
    "G2B": 76_832,
}
EXPECTED_REPRESENTATION_COUNTS = {
    "PRESERVED": 165_744,
    "NON_GRAPH": 17_828,
    "R2": 302_624,
    "R292": 10_252,
    "G2A": 38_624,
    "G2B": 76_832,
}
EXPECTED_LANE_COUNTS = {
    "I0": (9_404, 10_252),
    "I1": (295_336, 302_624),
    "I2": (144_296, 183_572),
    "I3": (115_456, 115_456),
}
LANE_FAMILIES = {
    "I0": {"R292"},
    "I1": {"R2"},
    "I2": {"PRESERVED", "NON_GRAPH"},
    "I3": {"G2A", "G2B"},
}

ROOT_PINS: tuple[tuple[str, str, int, str], ...] = (
    ("AF2", "cm2_round306b1af2_source_g_primitive_support_source_partition_primary_result.json", 2_540, "7238c245e79124e5bf3aa14c463fcc639efcde7431b03ac3a1cd035a4d1f7ebb"),
    ("B0", "cm2_round306b0_source_g_r306a_universe_support_source_freeze_member_support_source_index.json.gz", 162_499_140, "c9a8649c8473bb6a170187e7f803e95748d2ff2198b1b846d97383dd5f0581af"),
    ("I0_MANIFEST", "cm2_round306b1af4k2i0_source_g_six_family_identity_representation_index_manifest.sha256", 1_438, "38510f1ec1c1c9ddcc73cb6f3f95b015faed98c295227d9c627564ff8fabc5fc"),
    ("I1_MANIFEST", "cm2_round306b1af4k2i1_source_g_r2_identity_representation_index_manifest.sha256", 1_631, "e06efae8395e96cf3c1d0489c4de58cbc5e05357b6789f6fb1e56906b6026970"),
    ("I2_MANIFEST", "cm2_round306b1af4k2i2_source_g_preserved_nongraph_identity_representation_index_manifest.sha256", 1_650, "32309d3649e50e5e79b2c9b6a91a97d4fc53c8fe352c5516425a03f33ffd57b4"),
    ("I3_MANIFEST", "cm2_round306b1af4k2i3_source_g_g2_identity_representation_index_manifest.sha256", 1_840, "304db35c33fa6c1ab989885b4aecde6d1ccc6d38d2578282a62365ef760f7a26"),
)

LANE_FILES = {
    "I0": {
        "manifest": "cm2_round306b1af4k2i0_source_g_six_family_identity_representation_index_manifest.sha256",
        "member": "cm2_round306b1af4k2i0_source_g_six_family_identity_representation_index_member_index.jsonl.gz",
        "representation": "cm2_round306b1af4k2i0_source_g_six_family_identity_representation_index_representation_index.jsonl.gz",
        "result": "cm2_round306b1af4k2i0_source_g_six_family_identity_representation_index_result.json",
    },
    "I1": {
        "manifest": "cm2_round306b1af4k2i1_source_g_r2_identity_representation_index_manifest.sha256",
        "member": "cm2_round306b1af4k2i1_source_g_r2_identity_representation_index_member_index.jsonl.gz",
        "representation": "cm2_round306b1af4k2i1_source_g_r2_identity_representation_index_representation_index.jsonl.gz",
        "result": "cm2_round306b1af4k2i1_source_g_r2_identity_representation_index_result.json",
    },
    "I2": {
        "manifest": "cm2_round306b1af4k2i2_source_g_preserved_nongraph_identity_representation_index_manifest.sha256",
        "member": "cm2_round306b1af4k2i2_source_g_preserved_nongraph_identity_representation_index_member_index.jsonl.gz",
        "representation": "cm2_round306b1af4k2i2_source_g_preserved_nongraph_identity_representation_index_representation_index.jsonl.gz",
        "result": "cm2_round306b1af4k2i2_source_g_preserved_nongraph_identity_representation_index_result.json",
    },
    "I3": {
        "manifest": "cm2_round306b1af4k2i3_source_g_g2_identity_representation_index_manifest.sha256",
        "member": "cm2_round306b1af4k2i3_source_g_g2_identity_representation_index_member_index.jsonl.gz",
        "representation": "cm2_round306b1af4k2i3_source_g_g2_identity_representation_index_representation_index.jsonl.gz",
        "result": "cm2_round306b1af4k2i3_source_g_g2_identity_representation_index_result.json",
    },
}

OUTPUTS = {
    "member": PREFIX + "global_member_ledger.jsonl.gz",
    "representation": PREFIX + "global_representation_ledger.jsonl.gz",
    "family": PREFIX + "family_census_disposition.jsonl.gz",
    "transition": PREFIX + "transition_ready_mechanical_handle_ledger.jsonl.gz",
    "gap": PREFIX + "semantic_gap_ledger.jsonl.gz",
    "result": PREFIX + "result.json",
}

ZERO_CREDIT = {
    "normalized_support": 0,
    "representation_cover": 0,
    "physical_incidence": 0,
    "pullback_equivalence": 0,
    "A1_A2": 0,
    "B1A": 0,
    "B2": 0,
    "transition": 0,
    "maximality": 0,
    "fibre": 0,
    "global_disposition": 0,
    "D02": 0,
    "D03": 0,
    "D04": 0,
    "Gate5": 0,
    "CM2": 0,
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


def strict_equal(left: Any, right: Any) -> bool:
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return left.keys() == right.keys() and all(strict_equal(left[key], right[key]) for key in left)
    if type(left) is list:
        return len(left) == len(right) and all(strict_equal(a, b) for a, b in zip(left, right))
    return left == right


def row_hash(row: dict[str, Any], label: str) -> str:
    need(type(row) is dict and type(row.get("row_sha256")) is str, label + ":closed row")
    body = dict(row)
    claimed = body.pop("row_sha256")
    need(HEX64.fullmatch(claimed) is not None and digest(body) == claimed, label + ":row hash")
    return claimed


def closed(body: dict[str, Any]) -> dict[str, Any]:
    need("row_sha256" not in body, "output body preclosed")
    return {**body, "row_sha256": digest(body)}


def zero_credit(value: Any, label: str) -> None:
    need(type(value) is dict and bool(value), label + ":credit map")
    for key, item in value.items():
        need(type(key) is str and type(item) is int and item == 0, label + ":strict zero credit:" + str(key))


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
    total = offset = 0
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


def iter_array(stream: TextIO, marker: str) -> Iterator[Any]:
    def append(buffer: str, label: str) -> str:
        block = stream.read(CHARS)
        need(bool(block), label)
        combined = buffer + block
        need(len(combined.encode("utf-8")) <= BUFFER_CAP, "parser buffer cap")
        return combined

    buffer = ""
    while True:
        at = buffer.find(marker)
        if at >= 0:
            buffer = buffer[at + len(marker):]
            break
        buffer = append(buffer[-max(1, len(marker) - 1):], "missing marker:" + marker)
    buffer = buffer.lstrip()
    need(buffer.startswith(":"), "marker missing colon")
    buffer = buffer[1:].lstrip()
    need(buffer.startswith("["), "marker not array")
    buffer = buffer[1:]
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
        while True:
            try:
                value, end = DECODER.raw_decode(buffer)
                break
            except json.JSONDecodeError:
                need(len(buffer.encode("utf-8")) <= MAX_ROW, "incomplete decoded row cap")
                buffer = append(buffer, "truncated JSON row")
        need(len(buffer[:end].encode("utf-8")) <= MAX_ROW, "successful decoded row cap")
        need(len(canonical(value)) <= MAX_ROW, "successful canonical row cap")
        yield value
        buffer = buffer[end:]
        comma = True


class PinnedInputs:
    def __init__(self) -> None:
        self.dirfd = -1
        self.dir_before: os.stat_result | None = None
        self.files: dict[str, tuple[int, os.stat_result, int, str, str]] = {}
        self.by_name: dict[str, str] = {}
        self.pin_rows: list[dict[str, Any]] = []
        self.package_members: dict[str, dict[str, str]] = {}

    def _pin(self, label: str, filename: str, expected_size: int | None, expected_sha: str | None) -> None:
        need(label not in self.files and filename not in self.by_name and filename == os.path.basename(filename), "pin label/path uniqueness:" + label)
        if expected_sha is not None:
            need(HEX64.fullmatch(expected_sha) is not None, "pin sha:" + label)
        before = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "regular single-link pin:" + label)
        if expected_size is not None:
            need(before.st_size == expected_size, "size pin:" + label)
        fd = os.open(filename, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0), dir_fd=self.dirfd)
        opened = os.fstat(fd)
        need(fingerprint(before) == fingerprint(opened), "path/open race:" + label)
        size, sha = hash_fd(fd, before.st_size)
        need(size == before.st_size and (expected_sha is None or sha == expected_sha), "first byte pin:" + label)
        self.files[label] = (fd, opened, size, sha, filename)
        self.by_name[filename] = label
        self.pin_rows.append({"label": label, "filename": filename, "exact_size": size, "sha256": sha, "pass1_sha256": sha, "regular": True, "nlink_one": True})

    def _bytes(self, label: str, cap: int) -> bytes:
        fd, before, size, _, _ = self.files[label]
        need(size <= cap, "bounded held read:" + label)
        raw = os.pread(fd, size, 0)
        need(len(raw) == size and fingerprint(os.fstat(fd)) == fingerprint(before), "held read stable:" + label)
        return raw

    def _manifest(self, lane: str, label: str) -> None:
        entries: dict[str, str] = {}
        text = self._bytes(label, 1 << 20).decode("ascii")
        for raw_line in text.splitlines():
            parts = raw_line.split(maxsplit=1)
            need(len(parts) == 2 and HEX64.fullmatch(parts[0]) is not None, "manifest line:" + lane)
            path = parts[1].lstrip("*")
            if path.startswith("deliverables/"):
                path = path[len("deliverables/"):]
            need(path == os.path.basename(path) and path not in entries, "manifest path:" + lane)
            entries[path] = parts[0]
        need(bool(entries), "nonempty manifest:" + lane)
        self.package_members[lane] = entries
        for filename, sha in sorted(entries.items()):
            self._pin(lane + ":" + filename, filename, None, sha)

    def __enter__(self) -> "PinnedInputs":
        named = os.stat(DELIVERABLES, follow_symlinks=False)
        need(stat.S_ISDIR(named.st_mode), "deliverables real directory")
        self.dirfd = os.open(DELIVERABLES, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
        self.dir_before = os.fstat(self.dirfd)
        need(directory_identity(named) == directory_identity(self.dir_before), "deliverables dirfd binding")
        try:
            need(Path(__file__).name == PRODUCER_FILENAME and Path(__file__).resolve().parent == DELIVERABLES, "running producer canonical path")
            self._pin("PRODUCER", PRODUCER_FILENAME, None, None)
            for label, filename, size, sha in ROOT_PINS:
                self._pin(label, filename, size, sha)
            for lane in ("I0", "I1", "I2", "I3"):
                self._manifest(lane, lane + "_MANIFEST")
                required = LANE_FILES[lane]
                for role in ("member", "representation", "result"):
                    need(required[role] in self.package_members[lane], lane + ":required manifest member:" + role)
            return self
        except Exception:
            self.close(False)
            raise

    def label_for_name(self, filename: str) -> str:
        label = self.by_name.get(filename)
        need(type(label) is str, "unheld filename:" + filename)
        return label

    def small_json(self, filename_or_label: str) -> Any:
        label = self.by_name.get(filename_or_label, filename_or_label)
        raw = self._bytes(label, MAX_ROW)
        value = DECODER.decode(raw.decode("utf-8"))
        need(len(canonical(value)) <= MAX_ROW, "small canonical cap:" + label)
        return value

    def _text(self, label: str) -> tuple[TextIO, BinaryIO]:
        fd, before, _, _, filename = self.files[label]
        raw = os.fdopen(os.dup(fd), "rb")
        binary: BinaryIO = gzip.GzipFile(fileobj=raw, mode="rb") if filename.endswith(".gz") else raw
        text = io.TextIOWrapper(binary, encoding="utf-8", newline="")
        need(fingerprint(os.fstat(fd)) == fingerprint(before), "held FD before parse:" + label)
        return text, raw

    def jsonl(self, filename: str) -> Iterator[Any]:
        label = self.label_for_name(filename)
        text, raw = self._text(label)
        fd, before, _, _, _ = self.files[label]
        try:
            for line in text:
                need(len(line.encode("utf-8")) <= MAX_ROW + 1, "JSONL decoded row cap:" + label)
                need(line.endswith("\n"), "JSONL final LF:" + label)
                value = DECODER.decode(line[:-1])
                need(len(canonical(value)) <= MAX_ROW, "JSONL canonical row cap:" + label)
                yield value
        finally:
            text.close()
            if not raw.closed:
                raw.close()
            need(fingerprint(os.fstat(fd)) == fingerprint(before), "held FD after JSONL:" + label)

    def array(self, label: str, marker: str) -> Iterator[Any]:
        text, raw = self._text(label)
        fd, before, _, _, _ = self.files[label]
        try:
            yield from iter_array(text, marker)
        finally:
            text.close()
            if not raw.closed:
                raw.close()
            need(fingerprint(os.fstat(fd)) == fingerprint(before), "held FD after array:" + label)

    def revalidate(self) -> None:
        for label, (fd, before, size, sha, filename) in self.files.items():
            n, h = hash_fd(fd, size)
            named = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
            need(n == size and h == sha and fingerprint(before) == fingerprint(os.fstat(fd)) == fingerprint(named), "final path/FD rebind:" + label)
            for row in self.pin_rows:
                if row["label"] == label:
                    row["pass2_sha256"] = h
                    row["final_path_bound"] = True
                    break
        assert self.dir_before is not None
        need(directory_identity(self.dir_before) == directory_identity(os.fstat(self.dirfd)) == directory_identity(os.stat(DELIVERABLES, follow_symlinks=False)), "deliverables directory replaced")

    def close(self, verify: bool = True) -> None:
        error: Exception | None = None
        if verify:
            try:
                self.revalidate()
            except Exception as exc:
                error = exc
        for fd, _, _, _, _ in self.files.values():
            os.close(fd)
        self.files.clear()
        if self.dirfd >= 0:
            os.close(self.dirfd)
            self.dirfd = -1
        if error is not None:
            raise error

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.close(exc_type is None)


def scalar(db: sqlite3.Connection, sql: str, parameters: tuple[Any, ...] = ()) -> Any:
    row = db.execute(sql, parameters).fetchone()
    need(row is not None, "scalar query empty")
    return row[0]


def insert_batch(db: sqlite3.Connection, sql: str, batch: list[tuple[Any, ...]], limit: int = 2048) -> None:
    if len(batch) >= limit:
        db.executemany(sql, batch)
        batch.clear()


def normalize_family(value: Any, lane: str) -> str:
    need(type(value) is str, lane + ":coarse family type")
    normalized = value.upper().replace("-", "_")
    aliases = {"NONGRAPH": "NON_GRAPH", "G2A_GRAPH_SHEET": "G2A", "G2B_GRAPH_SIDE": "G2B"}
    normalized = aliases.get(normalized, normalized)
    need(normalized in LANE_FAMILIES[lane], lane + ":coarse family authority")
    return normalized


def first_string(row: dict[str, Any], keys: tuple[str, ...], label: str, required: bool = True) -> str | None:
    found = [row[key] for key in keys if key in row and row[key] is not None]
    need(len(found) <= 1 and (bool(found) or not required), label + ":unique field")
    if not found:
        return None
    need(type(found[0]) is str and bool(found[0]), label + ":string field")
    return found[0]


def setup_database(db: sqlite3.Connection) -> None:
    db.executescript("""
      PRAGMA journal_mode=OFF; PRAGMA synchronous=OFF; PRAGMA temp_store=MEMORY;
      CREATE TABLE b0(ord INTEGER PRIMARY KEY, member_id TEXT UNIQUE NOT NULL, b0_row_id TEXT UNIQUE NOT NULL, component_id TEXT NOT NULL, row_sha TEXT NOT NULL);
      CREATE TABLE member(member_id TEXT PRIMARY KEY, family TEXT NOT NULL, family_rank INTEGER NOT NULL, lane TEXT NOT NULL, component_id TEXT NOT NULL, upstream_component_id TEXT, b0_row_id TEXT NOT NULL, b0_row_sha TEXT NOT NULL, primary_hint TEXT, source_file TEXT NOT NULL, source_file_sha TEXT NOT NULL, source_manifest_sha TEXT NOT NULL, source_row_sha TEXT NOT NULL, source_full_sha TEXT NOT NULL);
      CREATE TABLE representation(rep_id TEXT PRIMARY KEY, owner_member_id TEXT NOT NULL, family TEXT NOT NULL, family_rank INTEGER NOT NULL, lane TEXT NOT NULL, role TEXT NOT NULL, source_file TEXT NOT NULL, source_file_sha TEXT NOT NULL, source_manifest_sha TEXT NOT NULL, source_row_sha TEXT NOT NULL, source_full_sha TEXT NOT NULL);
      CREATE TABLE summary(owner_member_id TEXT PRIMARY KEY, representation_count INTEGER NOT NULL, representation_set_sha TEXT NOT NULL, primary_rep_id TEXT NOT NULL);
    """)


def validate_upstream_result(pins: PinnedInputs, lane: str) -> None:
    files = LANE_FILES[lane]
    result = pins.small_json(files["result"])
    need(type(result) is dict and type(result.get("status")) is str and result["status"].startswith("PASS"), lane + ":result status")
    zero_credit(result.get("formal_credit"), lane + ":result")
    ledgers = result.get("ledgers")
    need(type(ledgers) is dict, lane + ":ledger metadata")
    member_meta = ledgers.get("member")
    rep_meta = ledgers.get("representation")
    need(type(member_meta) is dict and type(rep_meta) is dict, lane + ":member/representation metadata")
    member_label = pins.label_for_name(files["member"])
    rep_label = pins.label_for_name(files["representation"])
    _, _, member_size, member_sha, _ = pins.files[member_label]
    _, _, rep_size, rep_sha, _ = pins.files[rep_label]
    expected_member, expected_rep = EXPECTED_LANE_COUNTS[lane]
    need(type(member_meta.get("row_count")) is int and member_meta["row_count"] == expected_member, lane + ":member result count")
    need(type(rep_meta.get("row_count")) is int and rep_meta["row_count"] == expected_rep, lane + ":representation result count")
    need(member_meta.get("file_sha256") == member_sha and member_meta.get("file_size") == member_size, lane + ":member result byte binding")
    need(rep_meta.get("file_sha256") == rep_sha and rep_meta.get("file_size") == rep_size, lane + ":representation result byte binding")


def build_database(pins: PinnedInputs, db: sqlite3.Connection) -> dict[str, Any]:
    setup_database(db)
    b0_audit = ListHash()
    batch: list[tuple[Any, ...]] = []
    for order, row in enumerate(pins.array("B0", '"member_support_source_rows"')):
        own_sha = row_hash(row, "B0")
        b0_audit.add(row)
        member_id = row.get("member_id")
        b0_row_id = row.get("Round306B0_member_support_source_row_id")
        component_id = row.get("Round306A_component_id")
        need(all(type(value) is str for value in (member_id, b0_row_id, component_id)), "B0 identity fields")
        batch.append((order, member_id, b0_row_id, component_id, own_sha))
        insert_batch(db, "INSERT INTO b0 VALUES(?,?,?,?,?)", batch)
    if batch:
        db.executemany("INSERT INTO b0 VALUES(?,?,?,?,?)", batch)
    need(b0_audit.count == 564_492 and b0_audit.finish() == "c7dfb5534fddeb22fffb81bf539fe44d837aced46577aa5f490a0ae14aba77f5", "B0 ordered table commitment")

    af2 = pins.small_json("AF2")
    need(type(af2) is dict and type(af2.get("member_count")) is int and af2["member_count"] == 564_492, "AF2 denominator")
    need(type(af2.get("formal_credit")) is int and af2["formal_credit"] == 0, "AF2 strict zero credit")
    need(strict_equal(af2.get("coarse_partition"), {
        "G2a_graph_sheet_members": 38_624,
        "G2b_graph_side_members": 76_832,
        "R292_transformed_cell_union_members": 9_404,
        "R2_predicate_union_members": 295_336,
        "direct_preserved_source_geometry": 126_468,
        "non_graph_virtual_bulk_members": 17_828,
    }), "AF2 exact coarse census")

    for lane in ("I0", "I1", "I2", "I3"):
        validate_upstream_result(pins, lane)
        files = LANE_FILES[lane]
        manifest_label = lane + "_MANIFEST"
        manifest_sha = pins.files[manifest_label][3]
        source_file_sha = pins.files[pins.label_for_name(files["member"])][3]
        batch = []
        count = 0
        for row in pins.jsonl(files["member"]):
            own_sha = row_hash(row, lane + ":member")
            zero_credit(row.get("formal_credit"), lane + ":member")
            full_sha = digest(row)
            member_id = row.get("member_id")
            family = normalize_family(row.get("coarse_family"), lane)
            need(type(member_id) is str, lane + ":member id")
            b0 = db.execute("SELECT b0_row_id,component_id,row_sha FROM b0 WHERE member_id=?", (member_id,)).fetchone()
            need(b0 is not None, lane + ":member outside B0")
            b0_row_id, component_id, b0_sha = b0
            need(row.get("source_B0_row_id") == b0_row_id and row.get("source_B0_row_sha256") == b0_sha, lane + ":B0 backbinding")
            upstream_component = first_string(row, ("component_id", "Round306A_component_id"), lane + ":component", required=False)
            primary_hint = first_string(row, ("primary_representation_cell_id", "primary_representation_handle_id", "primary_representation_id"), lane + ":primary hint", required=False)
            batch.append((member_id, family, FAMILY_RANK[family], lane, component_id, upstream_component, b0_row_id, b0_sha, primary_hint, files["member"], source_file_sha, manifest_sha, own_sha, full_sha))
            insert_batch(db, "INSERT INTO member VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)", batch)
            count += 1
        if batch:
            db.executemany("INSERT INTO member VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)", batch)
        need(count == EXPECTED_LANE_COUNTS[lane][0], lane + ":member stream count")

    need(scalar(db, "SELECT COUNT(*) FROM member") == 564_492, "global member count")
    need(scalar(db, "SELECT COUNT(*) FROM b0 b LEFT JOIN member m ON m.member_id=b.member_id WHERE m.member_id IS NULL") == 0, "B0 minus member union")
    member_counts = dict(db.execute("SELECT family,COUNT(*) FROM member GROUP BY family"))
    need(member_counts == EXPECTED_MEMBER_COUNTS, "six-family member census")

    for lane in ("I0", "I1", "I2", "I3"):
        files = LANE_FILES[lane]
        manifest_sha = pins.files[lane + "_MANIFEST"][3]
        source_file_sha = pins.files[pins.label_for_name(files["representation"])][3]
        batch = []
        count = 0
        for row in pins.jsonl(files["representation"]):
            own_sha = row_hash(row, lane + ":representation")
            zero_credit(row.get("formal_credit"), lane + ":representation")
            full_sha = digest(row)
            rep_id = first_string(row, ("representation_id", "representation_cell_id", "representation_handle_id"), lane + ":representation id")
            owner = row.get("owner_member_id")
            role = first_string(row, ("representation_role", "representation_kind", "role"), lane + ":representation role")
            need(type(owner) is str and type(rep_id) is str and type(role) is str, lane + ":representation fields")
            member = db.execute("SELECT family,lane FROM member WHERE member_id=?", (owner,)).fetchone()
            need(member is not None and member[1] == lane, lane + ":orphan/cross-lane owner")
            family = member[0]
            if "coarse_family" in row:
                need(normalize_family(row["coarse_family"], lane) == family, lane + ":representation family backbinding")
            if "owner_coarse_family" in row:
                need(normalize_family(row["owner_coarse_family"], lane) == family, lane + ":representation owner family backbinding")
            batch.append((rep_id, owner, family, FAMILY_RANK[family], lane, role, files["representation"], source_file_sha, manifest_sha, own_sha, full_sha))
            insert_batch(db, "INSERT INTO representation VALUES(?,?,?,?,?,?,?,?,?,?,?)", batch)
            count += 1
        if batch:
            db.executemany("INSERT INTO representation VALUES(?,?,?,?,?,?,?,?,?,?,?)", batch)
        need(count == EXPECTED_LANE_COUNTS[lane][1], lane + ":representation stream count")

    need(scalar(db, "SELECT COUNT(*) FROM representation") == 611_904, "global representation count")
    need(scalar(db, "SELECT COUNT(*) FROM representation r LEFT JOIN member m ON m.member_id=r.owner_member_id WHERE m.member_id IS NULL OR m.family<>r.family OR m.lane<>r.lane") == 0, "representation owner anti-join")
    representation_counts = dict(db.execute("SELECT family,COUNT(*) FROM representation GROUP BY family"))
    need(representation_counts == EXPECTED_REPRESENTATION_COUNTS, "six-family representation census")
    db.executescript("""
      CREATE INDEX member_family_order ON member(family_rank,member_id);
      CREATE INDEX representation_family_order ON representation(family_rank,rep_id);
      CREATE INDEX representation_owner_order ON representation(owner_member_id,rep_id);
    """)

    batch = []
    current_owner: str | None = None
    audit: ListHash | None = None
    rep_count = 0
    minimum: str | None = None
    hinted: str | None = None
    seen_hint = False

    def finish_owner() -> None:
        nonlocal current_owner, audit, rep_count, minimum, hinted, seen_hint, batch
        if current_owner is None:
            return
        need(audit is not None and rep_count > 0 and minimum is not None, "owner summary state")
        primary = hinted if hinted is not None else minimum
        if hinted is not None:
            need(seen_hint, "upstream primary hint absent from representations")
        batch.append((current_owner, rep_count, audit.finish(), primary))
        insert_batch(db, "INSERT INTO summary VALUES(?,?,?,?)", batch)

    for owner, rep_id, role, source_full_sha, primary_hint in db.execute("SELECT r.owner_member_id,r.rep_id,r.role,r.source_full_sha,m.primary_hint FROM representation r JOIN member m ON m.member_id=r.owner_member_id ORDER BY r.owner_member_id,r.rep_id"):
        if owner != current_owner:
            finish_owner()
            current_owner = owner
            audit = ListHash()
            rep_count = 0
            minimum = rep_id
            hinted = primary_hint
            seen_hint = False
        assert audit is not None
        audit.add({"representation_id": rep_id, "representation_role": role, "source_row_canonical_sha256": source_full_sha})
        rep_count += 1
        if rep_id == hinted:
            seen_hint = True
    finish_owner()
    if batch:
        db.executemany("INSERT INTO summary VALUES(?,?,?,?)", batch)
    need(scalar(db, "SELECT COUNT(*) FROM summary") == 564_492, "every member has representation summary")
    need(scalar(db, "SELECT SUM(representation_count) FROM summary") == 611_904, "summary representation sum")
    db.commit()

    coarse_stream = hashlib.sha256()
    for member_id, family in db.execute("SELECT b.member_id,m.family FROM b0 b JOIN member m ON m.member_id=b.member_id ORDER BY b.ord"):
        coarse_stream.update(canonical([member_id, family]) + b"\n")
    return {
        "B0_ordered_table_sha256": b0_audit.finish(),
        "AF2_status": af2["status"],
        "coarse_partition_stream_sha256": coarse_stream.hexdigest(),
        "member_counts": member_counts,
        "representation_counts": representation_counts,
    }


def producer_source_commitment(pins: PinnedInputs) -> dict[str, Any]:
    _, _, size, sha, filename = pins.files["PRODUCER"]
    return {
        "domain": SCHEMA + ".producer-source-input.v1",
        "filename": filename,
        "exact_size": size,
        "sha256": sha,
    }


def commitment_for_member(row: tuple[Any, ...], producer_commitment: dict[str, Any]) -> dict[str, Any]:
    member_id, family, lane, component_id, b0_row_id, b0_sha, source_file, source_file_sha, source_manifest_sha, source_row_sha, source_full_sha, rep_count, rep_set_sha, primary = row
    return {
        "domain": SCHEMA + ".global-member-input.v1",
        "producer_source_commitment": producer_commitment,
        "producer_source_commitment_sha256": digest(producer_commitment),
        "member_id": member_id,
        "coarse_family": family,
        "source_lane": lane,
        "source_manifest_sha256": source_manifest_sha,
        "source_member_file": source_file,
        "source_member_file_sha256": source_file_sha,
        "source_member_row_sha256": source_row_sha,
        "source_member_row_canonical_sha256": source_full_sha,
        "B0_row_id": b0_row_id,
        "B0_row_sha256": b0_sha,
        "Round306A_component_id": component_id,
        "representation_count": rep_count,
        "representation_set_sha256": rep_set_sha,
        "primary_mechanical_representation_id": primary,
    }


def member_query(db: sqlite3.Connection) -> Iterator[tuple[Any, ...]]:
    yield from db.execute("""SELECT m.member_id,m.family,m.lane,m.component_id,m.b0_row_id,m.b0_row_sha,m.source_file,m.source_file_sha,m.source_manifest_sha,m.source_row_sha,m.source_full_sha,s.representation_count,s.representation_set_sha,s.primary_rep_id FROM member m JOIN summary s ON s.owner_member_id=m.member_id ORDER BY m.family_rank,m.member_id""")


def member_rows(db: sqlite3.Connection, producer_commitment: dict[str, Any]) -> Iterator[dict[str, Any]]:
    for row in member_query(db):
        commitment = commitment_for_member(row, producer_commitment)
        yield closed({
            "schema": SCHEMA + ".global-member-row",
            "status": "MECHANICAL_IDENTITY_AND_OWNER_CENSUS_ONLY__SEMANTIC_SUPPORT_NOT_PROVED",
            "member_id": row[0],
            "coarse_family": row[1],
            "source_lane": row[2],
            "Round306A_component_id": row[3],
            "primary_mechanical_representation_id": row[13],
            "mechanical_representation_count": row[11],
            "mechanical_representation_set_sha256": row[12],
            "canonical_input_commitment": commitment,
            "canonical_input_commitment_sha256": digest(commitment),
            "formal_credit": ZERO_CREDIT,
        })


def representation_rows(db: sqlite3.Connection, producer_commitment: dict[str, Any]) -> Iterator[dict[str, Any]]:
    query = """SELECT rep_id,owner_member_id,family,lane,role,source_file,source_file_sha,source_manifest_sha,source_row_sha,source_full_sha FROM representation ORDER BY family_rank,rep_id"""
    for rep_id, owner, family, lane, role, source_file, source_file_sha, manifest_sha, source_row_sha, source_full_sha in db.execute(query):
        commitment = {
            "domain": SCHEMA + ".global-representation-input.v1",
            "producer_source_commitment": producer_commitment,
            "producer_source_commitment_sha256": digest(producer_commitment),
            "representation_id": rep_id,
            "owner_member_id": owner,
            "coarse_family": family,
            "mechanical_identity_authority_lane": FAMILY_LANE[family],
            "source_lane": lane,
            "source_manifest_sha256": manifest_sha,
            "source_representation_file": source_file,
            "source_representation_file_sha256": source_file_sha,
            "source_representation_row_sha256": source_row_sha,
            "source_representation_row_canonical_sha256": source_full_sha,
        }
        yield closed({
            "schema": SCHEMA + ".global-representation-row",
            "status": "MECHANICAL_REPRESENTATION_OWNER_INDEX_ONLY__SET_EQUALITY_NOT_PROVED",
            "representation_id": rep_id,
            "owner_member_id": owner,
            "coarse_family": family,
            "source_lane": lane,
            "representation_role": role,
            "canonical_input_commitment": commitment,
            "canonical_input_commitment_sha256": digest(commitment),
            "formal_credit": ZERO_CREDIT,
        })


def transition_rows(db: sqlite3.Connection, producer_commitment: dict[str, Any]) -> Iterator[dict[str, Any]]:
    for row in member_query(db):
        commitment = commitment_for_member(row, producer_commitment)
        handle_input = {
            "domain": SCHEMA + ".transition-ready-mechanical-handle-input.v1",
            "global_member_input_commitment_sha256": digest(commitment),
            "member_id": row[0],
            "coarse_family": row[1],
            "primary_mechanical_representation_id": row[13],
            "mechanical_representation_count": row[11],
            "mechanical_representation_set_sha256": row[12],
        }
        yield closed({
            "schema": SCHEMA + ".transition-ready-mechanical-handle-row",
            "status": "IDENTITY_ROUTABLE_MECHANICAL_HANDLE_ONLY__NO_TRANSITION_THEOREM_CREDIT",
            "member_id": row[0],
            "coarse_family": row[1],
            "transition_ready_mechanical_handle_id": "round306b1af4k2i4-mechanical-transition-handle:" + digest(handle_input),
            "handle_input_commitment": handle_input,
            "handle_input_commitment_sha256": digest(handle_input),
            "formal_credit": ZERO_CREDIT,
        })


def set_hash(db: sqlite3.Connection, family: str, table: str, field: str) -> str:
    audit = ListHash()
    for (value,) in db.execute(f"SELECT {field} FROM {table} WHERE family=? ORDER BY {field}", (family,)):
        audit.add(value)
    return audit.finish()


def family_rows(db: sqlite3.Connection, producer_commitment: dict[str, Any]) -> Iterator[dict[str, Any]]:
    for family in FAMILY_ORDER:
        members = EXPECTED_MEMBER_COUNTS[family]
        reps = EXPECTED_REPRESENTATION_COUNTS[family]
        member_set_sha = set_hash(db, family, "member", "member_id")
        representation_set_sha = set_hash(db, family, "representation", "rep_id")
        commitment = {
            "domain": SCHEMA + ".family-census-input.v1",
            "producer_source_commitment": producer_commitment,
            "producer_source_commitment_sha256": digest(producer_commitment),
            "coarse_family": family,
            "member_count": members,
            "representation_count": reps,
            "member_id_set_sha256": member_set_sha,
            "representation_id_set_sha256": representation_set_sha,
        }
        yield closed({
            "schema": SCHEMA + ".family-census-disposition-row",
            "status": "EXACT_MECHANICAL_CENSUS_CLOSED__SEMANTIC_THEOREM_GAPS_REMAIN",
            "coarse_family": family,
            "mechanical_identity_authority_lane": FAMILY_LANE[family],
            "member_count": members,
            "representation_count": reps,
            "member_id_set_sha256": member_set_sha,
            "representation_id_set_sha256": representation_set_sha,
            "closed_anti_joins": {"duplicate_members": 0, "duplicate_representations": 0, "members_outside_B0": 0, "orphan_representation_owners": 0},
            "canonical_input_commitment": commitment,
            "canonical_input_commitment_sha256": digest(commitment),
            "formal_credit": ZERO_CREDIT,
        })


FAMILY_GAPS = {
    "PRESERVED": ["DIRECT_SOURCE_GEOMETRY_FULL_SUPPORT_EQUALITY_NOT_PROVED", "REPRESENTATION_PULLBACK_EQUIVALENCE_NOT_PROVED", "A1_A2_NOT_DISCHARGED"],
    "NON_GRAPH": ["NON_GRAPH_FULL_SUPPORT_CONSTRUCTION_SEMANTICS_NOT_PROVED", "REPRESENTATION_PULLBACK_EQUIVALENCE_NOT_PROVED", "A1_A2_NOT_DISCHARGED"],
    "R2": ["SOURCE_FREE_INTERVAL_PREDICATE_EQUIVALENCE_NOT_PROVED", "W_TAIL_ARTIFICIAL_FACE_REGLUE_NOT_CREDITED_HERE", "A1_A2_NOT_DISCHARGED"],
    "R292": ["FIXED_SIGN_PULLBACK_EQUIVALENCE_NOT_PROVED", "SIGMA_BRANCH_AUTHORITY_NOT_PROVED", "REFINED_PHYSICAL_FACE_KRUSKAL_SEMANTICS_NOT_PROVED"],
    "G2A": ["GRAPH_DEFINITION_NOT_PROVED", "PHYSICAL_INCIDENCE_NOT_PROVED", "REPRESENTATION_PULLBACK_EQUIVALENCE_NOT_PROVED"],
    "G2B": ["GRAPH_DEFINITION_NOT_PROVED", "PHYSICAL_INCIDENCE_NOT_PROVED", "REPRESENTATION_PULLBACK_EQUIVALENCE_NOT_PROVED"],
}


def gap_rows(producer_commitment: dict[str, Any]) -> Iterator[dict[str, Any]]:
    for family in FAMILY_ORDER:
        commitment = {
            "domain": SCHEMA + ".semantic-gap-input.v1",
            "producer_source_commitment": producer_commitment,
            "producer_source_commitment_sha256": digest(producer_commitment),
            "coarse_family": family,
            "member_count": EXPECTED_MEMBER_COUNTS[family],
            "representation_count": EXPECTED_REPRESENTATION_COUNTS[family],
            "semantic_obligation_labels": FAMILY_GAPS[family],
        }
        yield closed({
            "schema": SCHEMA + ".semantic-gap-row",
            "status": "BLOCKED_FOR_SEMANTIC_AND_THEOREM_CREDIT",
            "coarse_family": family,
            "mechanically_indexed_member_count": EXPECTED_MEMBER_COUNTS[family],
            "mechanically_indexed_representation_count": EXPECTED_REPRESENTATION_COUNTS[family],
            "members_without_normalized_full_support_credit": EXPECTED_MEMBER_COUNTS[family],
            "representations_without_representation_cover_credit": EXPECTED_REPRESENTATION_COUNTS[family],
            "members_without_transition_theorem_credit": EXPECTED_MEMBER_COUNTS[family],
            "semantic_obligation_labels": FAMILY_GAPS[family],
            "theorem_obligation_census_824864_is_not_a_feature_ledger_row_count": True,
            "canonical_input_commitment": commitment,
            "canonical_input_commitment_sha256": digest(commitment),
            "formal_credit": ZERO_CREDIT,
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


def publish(scratch: Path, output_directory: Path, names: Iterable[str]) -> None:
    output_named = os.stat(output_directory, follow_symlinks=False)
    need(stat.S_ISDIR(output_named.st_mode), "real output directory")
    output_fd = os.open(output_directory, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
    scratch_named = os.stat(scratch, follow_symlinks=False)
    scratch_fd = os.open(scratch, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
    try:
        need(directory_identity(output_named) == directory_identity(os.fstat(output_fd)), "output dirfd binding")
        need(directory_identity(scratch_named) == directory_identity(os.fstat(scratch_fd)), "scratch dirfd binding")
        for name in names:
            staged = os.stat(name, dir_fd=scratch_fd, follow_symlinks=False)
            need(stat.S_ISREG(staged.st_mode) and staged.st_nlink == 1, "staged regular single-link:" + name)
            try:
                existing = os.stat(name, dir_fd=output_fd, follow_symlinks=False)
                need(stat.S_ISREG(existing.st_mode) and existing.st_nlink == 1, "replace target regular single-link:" + name)
            except FileNotFoundError:
                pass
            os.replace(name, name, src_dir_fd=scratch_fd, dst_dir_fd=output_fd)
            final = os.stat(name, dir_fd=output_fd, follow_symlinks=False)
            need(stat.S_ISREG(final.st_mode) and final.st_nlink == 1 and final.st_size == staged.st_size, "published file:" + name)
        os.fsync(output_fd)
        need(directory_identity(output_named) == directory_identity(os.fstat(output_fd)) == directory_identity(os.stat(output_directory, follow_symlinks=False)), "output final binding")
    finally:
        os.close(scratch_fd)
        os.close(output_fd)


def produce(output_directory: Path, _seed: str) -> dict[str, Any]:
    output_directory = Path(os.path.abspath(output_directory))
    root = Path("/tmp")
    need(os.path.realpath(root) == str(root), "explicit /tmp authority")
    root_named = os.stat(root, follow_symlinks=False)
    need(stat.S_ISDIR(root_named.st_mode), "/tmp real directory")
    root_fd = os.open(root, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
    need(directory_identity(root_named) == directory_identity(os.fstat(root_fd)), "/tmp dirfd binding")
    need(os.path.commonpath((str(root), str(output_directory))) != str(output_directory), "/tmp outside output")
    try:
        with tempfile.TemporaryDirectory(prefix="cm2-k2i4-global-", dir=root) as scratch_name:
            scratch = Path(os.path.realpath(scratch_name))
            need(scratch.parent == root, "scratch outside deliverables and under explicit /tmp")
            db = sqlite3.connect(scratch / "global-merger.sqlite3")
            try:
                with PinnedInputs() as pins:
                    receipts = build_database(pins, db)
                    producer_commitment = producer_source_commitment(pins)
                    ledger_meta = {
                        "member": write_jsonl_gzip(scratch / OUTPUTS["member"], member_rows(db, producer_commitment), "coarse_family_authority_order_THEN_member_id_unsigned_bytewise_ASCII_ASC"),
                        "representation": write_jsonl_gzip(scratch / OUTPUTS["representation"], representation_rows(db, producer_commitment), "coarse_family_authority_order_THEN_representation_id_unsigned_bytewise_ASCII_ASC"),
                        "family": write_jsonl_gzip(scratch / OUTPUTS["family"], family_rows(db, producer_commitment), "PRESERVED_NON_GRAPH_R2_R292_G2A_G2B"),
                        "transition": write_jsonl_gzip(scratch / OUTPUTS["transition"], transition_rows(db, producer_commitment), "coarse_family_authority_order_THEN_member_id_unsigned_bytewise_ASCII_ASC"),
                        "gap": write_jsonl_gzip(scratch / OUTPUTS["gap"], gap_rows(producer_commitment), "PRESERVED_NON_GRAPH_R2_R292_G2A_G2B"),
                    }
                    need(ledger_meta["member"]["row_count"] == 564_492, "member output count")
                    need(ledger_meta["representation"]["row_count"] == 611_904, "representation output count")
                    need(ledger_meta["family"]["row_count"] == 6 and ledger_meta["gap"]["row_count"] == 6, "six-family output count")
                    need(ledger_meta["transition"]["row_count"] == 564_492, "transition-handle output count")
                    pins.revalidate()
                    result = {
                        "schema": SCHEMA,
                        "status": STATUS,
                        "scope": "GLOBAL_SIX_FAMILY_MECHANICAL_IDENTITY_AND_REPRESENTATION_CENSUS_ONLY",
                        "seed_affects_output": False,
                        "producer_sha256": producer_commitment["sha256"],
                        "producer_byte_binding": "SELF_HELD_FD_TWO_PASS_PATH_REBIND_PLUS_INDEPENDENT_VERIFIER_STATIC_PIN",
                        "producer_source_commitment": producer_commitment,
                        "producer_source_commitment_sha256": digest(producer_commitment),
                        "input_pins": pins.pin_rows,
                        "upstream_package_manifest_sha256": {lane: pins.files[lane + "_MANIFEST"][3] for lane in ("I0", "I1", "I2", "I3")},
                        "authority_priority": ["B0_MEMBER_UNIVERSE", "AF2_SIX_FAMILY_CENSUS", "K2I0_R292", "K2I1_R2", "K2I2_PRESERVED_AND_NON_GRAPH", "K2I3_G2A_AND_G2B"],
                        "authority_receipts": receipts,
                        "exact_census": {
                            "member_count": 564_492,
                            "representation_count": 611_904,
                            "member_counts_by_family": EXPECTED_MEMBER_COUNTS,
                            "representation_counts_by_family": EXPECTED_REPRESENTATION_COUNTS,
                            "representation_equation": "183572_I2_PLUS_302624_I1_PLUS_10252_I0_PLUS_115456_I3_EQUALS_611904",
                            "member_equation": "126468_PRESERVED_PLUS_17828_NON_GRAPH_PLUS_295336_R2_PLUS_9404_R292_PLUS_38624_G2A_PLUS_76832_G2B_EQUALS_564492",
                        },
                        "ledgers": ledger_meta,
                        "closed_anti_joins": {
                            "duplicate_member_ids": 0,
                            "family_overlap_count": 0,
                            "AF2_coarse_census_mismatch_count": 0,
                            "members_minus_B0": 0,
                            "B0_minus_members": 0,
                            "duplicate_representation_ids": 0,
                            "orphan_representation_owners": 0,
                            "representation_owner_family_mismatches": 0,
                            "members_without_mechanical_representation": 0,
                            "upstream_primary_hints_missing_from_representation_set": 0,
                        },
                        "semantic_boundary": {
                            "normalized_full_support_credit": 0,
                            "representation_cover_credit": 0,
                            "A1_A2_credit": 0,
                            "B1A_credit": 0,
                            "B2_credit": 0,
                            "transition_family_credit": "0_OF_20",
                            "known_legal_edge_geometry_first_rediscovery_credit": "0_OF_478718",
                            "pair_routing_credit": "0_OF_158838084354",
                            "maximality_credit": "0_OF_92688_COMPONENTS",
                            "official_fibre_credit": "0_OF_124",
                            "Source_G_disposition_credit": "0_OF_224580",
                            "D02": "BLOCKED",
                            "D03": "NOT_REACHED",
                            "D04": "NOT_MINTED",
                            "Gate5": "10_OF_18_PREEXISTING__NO_NEW_CREDIT",
                            "CM2": "NO_GO_FOR_CLAIM",
                            "theorem_obligation_census_824864_is_not_feature_ledger_row_count": True,
                        },
                        "formal_credit": ZERO_CREDIT,
                    }
                    result_path = scratch / OUTPUTS["result"]
                    result_path.write_bytes(canonical(result) + b"\n")
                    with result_path.open("rb") as handle:
                        os.fsync(handle.fileno())
                    publish(scratch, output_directory, OUTPUTS.values())
                need(directory_identity(root_named) == directory_identity(os.fstat(root_fd)) == directory_identity(os.stat(root, follow_symlinks=False)), "/tmp final binding")
                return result
            finally:
                db.close()
    finally:
        os.close(root_fd)


def self_test() -> dict[str, Any]:
    need(strict_equal({"x": False}, {"x": 0}) is False, "false/int alias rejected")
    need(strict_equal({"x": True}, {"x": 1}) is False, "true/int alias rejected")
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
    need(len(wire) == MAX_ROW and list(iter_array(io.StringIO('{"rows":[' + wire.decode("ascii") + ']}'), '"rows"')) == [body], "exact decoded row cap accepted")
    overflow = {"x": body["x"] + "a"}
    cap_rejected = False
    try:
        list(iter_array(io.StringIO('{"rows":[' + canonical(overflow).decode("ascii") + ']}'), '"rows"'))
    except Blocked:
        cap_rejected = True
    need(cap_rejected, "decoded row cap plus one rejected")
    return {"schema": SCHEMA + ".producer-self-test", "status": "PASS", "false_int_alias_rejected": True, "true_int_alias_rejected": True, "decoded_row_exact_cap": MAX_ROW, "decoded_row_cap_plus_one_rejected": True, "candidate_is_formal": False}


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
    print(canonical({"status": result["status"], "result_object_sha256": digest(result)}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
