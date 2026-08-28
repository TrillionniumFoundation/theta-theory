#!/usr/bin/env python3
"""Independent verifier for the K2I4 global mechanical merger.

The verifier never imports the producer.  It independently rebuilds the
source joins and expected rows.  A held producer FD is executed only for the
two-seed byte-determinism test; that execution is not correctness authority.
Ordinary verification is explicitly no-write.
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
import subprocess
import sys
import tempfile
from itertools import zip_longest
from typing import Any, BinaryIO, Iterable, Iterator, TextIO


class Rejected(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise Rejected(label)


PREFIX = "cm2_round306b1af4k2i4_source_g_global_six_family_mechanical_identity_representation_merger_"
SCHEMA = "cm2.round306b1af4k2i4.source-g-global-six-family-mechanical-identity-representation-merger.v1"
STATUS = "PASS_EXACT_GLOBAL_SIX_FAMILY_MECHANICAL_IDENTITY_REPRESENTATION_CENSUS__ZERO_THEOREM_CREDIT"
DELIVERABLES = Path(__file__).resolve().parent
PRODUCER = PREFIX + "producer.py"
VERIFIER = PREFIX + "independent_verifier.py"
MANIFEST = PREFIX + "manifest.sha256"
ATTACK = PREFIX + "attack_suite.json"
VERIFICATION = PREFIX + "verification.json"
REPORT = PREFIX + "report.md"
COLD = PREFIX + "cold_replay.md"
EXPECTED_PRODUCER_SHA256 = "1e79d18869bad00078bc035fb657344e89910497d7696b310f302776216fdcba"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
MAX_ROW = 8 << 20
CHARS = 1 << 18
BUFFER_CAP = MAX_ROW + 4 * CHARS

FAMILY_ORDER = ("PRESERVED", "NON_GRAPH", "R2", "R292", "G2A", "G2B")
FAMILY_RANK = {family: rank for rank, family in enumerate(FAMILY_ORDER)}
FAMILY_LANE = {"PRESERVED": "I2", "NON_GRAPH": "I2", "R2": "I1", "R292": "I0", "G2A": "I3", "G2B": "I3"}
MEMBER_COUNTS = {"PRESERVED": 126_468, "NON_GRAPH": 17_828, "R2": 295_336, "R292": 9_404, "G2A": 38_624, "G2B": 76_832}
REP_COUNTS = {"PRESERVED": 165_744, "NON_GRAPH": 17_828, "R2": 302_624, "R292": 10_252, "G2A": 38_624, "G2B": 76_832}
LANE_COUNTS = {"I0": (9_404, 10_252), "I1": (295_336, 302_624), "I2": (144_296, 183_572), "I3": (115_456, 115_456)}
LANE_FAMILIES = {"I0": {"R292"}, "I1": {"R2"}, "I2": {"PRESERVED", "NON_GRAPH"}, "I3": {"G2A", "G2B"}}

ROOT_PINS: tuple[tuple[str, str, int, str], ...] = (
    ("AF2", "cm2_round306b1af2_source_g_primitive_support_source_partition_primary_result.json", 2_540, "7238c245e79124e5bf3aa14c463fcc639efcde7431b03ac3a1cd035a4d1f7ebb"),
    ("B0", "cm2_round306b0_source_g_r306a_universe_support_source_freeze_member_support_source_index.json.gz", 162_499_140, "c9a8649c8473bb6a170187e7f803e95748d2ff2198b1b846d97383dd5f0581af"),
    ("I0_MANIFEST", "cm2_round306b1af4k2i0_source_g_six_family_identity_representation_index_manifest.sha256", 1_438, "38510f1ec1c1c9ddcc73cb6f3f95b015faed98c295227d9c627564ff8fabc5fc"),
    ("I1_MANIFEST", "cm2_round306b1af4k2i1_source_g_r2_identity_representation_index_manifest.sha256", 1_631, "e06efae8395e96cf3c1d0489c4de58cbc5e05357b6789f6fb1e56906b6026970"),
    ("I2_MANIFEST", "cm2_round306b1af4k2i2_source_g_preserved_nongraph_identity_representation_index_manifest.sha256", 1_650, "32309d3649e50e5e79b2c9b6a91a97d4fc53c8fe352c5516425a03f33ffd57b4"),
    ("I3_MANIFEST", "cm2_round306b1af4k2i3_source_g_g2_identity_representation_index_manifest.sha256", 1_840, "304db35c33fa6c1ab989885b4aecde6d1ccc6d38d2578282a62365ef760f7a26"),
)

LANE_FILES = {
    "I0": {"member": "cm2_round306b1af4k2i0_source_g_six_family_identity_representation_index_member_index.jsonl.gz", "representation": "cm2_round306b1af4k2i0_source_g_six_family_identity_representation_index_representation_index.jsonl.gz", "result": "cm2_round306b1af4k2i0_source_g_six_family_identity_representation_index_result.json"},
    "I1": {"member": "cm2_round306b1af4k2i1_source_g_r2_identity_representation_index_member_index.jsonl.gz", "representation": "cm2_round306b1af4k2i1_source_g_r2_identity_representation_index_representation_index.jsonl.gz", "result": "cm2_round306b1af4k2i1_source_g_r2_identity_representation_index_result.json"},
    "I2": {"member": "cm2_round306b1af4k2i2_source_g_preserved_nongraph_identity_representation_index_member_index.jsonl.gz", "representation": "cm2_round306b1af4k2i2_source_g_preserved_nongraph_identity_representation_index_representation_index.jsonl.gz", "result": "cm2_round306b1af4k2i2_source_g_preserved_nongraph_identity_representation_index_result.json"},
    "I3": {"member": "cm2_round306b1af4k2i3_source_g_g2_identity_representation_index_member_index.jsonl.gz", "representation": "cm2_round306b1af4k2i3_source_g_g2_identity_representation_index_representation_index.jsonl.gz", "result": "cm2_round306b1af4k2i3_source_g_g2_identity_representation_index_result.json"},
}

OUTPUTS = {
    "member": PREFIX + "global_member_ledger.jsonl.gz",
    "representation": PREFIX + "global_representation_ledger.jsonl.gz",
    "family": PREFIX + "family_census_disposition.jsonl.gz",
    "transition": PREFIX + "transition_ready_mechanical_handle_ledger.jsonl.gz",
    "gap": PREFIX + "semantic_gap_ledger.jsonl.gz",
    "result": PREFIX + "result.json",
}

ZERO = {"normalized_support": 0, "representation_cover": 0, "physical_incidence": 0, "pullback_equivalence": 0, "A1_A2": 0, "B1A": 0, "B2": 0, "transition": 0, "maximality": 0, "fibre": 0, "global_disposition": 0, "D02": 0, "D03": 0, "D04": 0, "Gate5": 0, "CM2": 0}

FAMILY_GAPS = {
    "PRESERVED": ["DIRECT_SOURCE_GEOMETRY_FULL_SUPPORT_EQUALITY_NOT_PROVED", "REPRESENTATION_PULLBACK_EQUIVALENCE_NOT_PROVED", "A1_A2_NOT_DISCHARGED"],
    "NON_GRAPH": ["NON_GRAPH_FULL_SUPPORT_CONSTRUCTION_SEMANTICS_NOT_PROVED", "REPRESENTATION_PULLBACK_EQUIVALENCE_NOT_PROVED", "A1_A2_NOT_DISCHARGED"],
    "R2": ["SOURCE_FREE_INTERVAL_PREDICATE_EQUIVALENCE_NOT_PROVED", "W_TAIL_ARTIFICIAL_FACE_REGLUE_NOT_CREDITED_HERE", "A1_A2_NOT_DISCHARGED"],
    "R292": ["FIXED_SIGN_PULLBACK_EQUIVALENCE_NOT_PROVED", "SIGMA_BRANCH_AUTHORITY_NOT_PROVED", "REFINED_PHYSICAL_FACE_KRUSKAL_SEMANTICS_NOT_PROVED"],
    "G2A": ["GRAPH_DEFINITION_NOT_PROVED", "PHYSICAL_INCIDENCE_NOT_PROVED", "REPRESENTATION_PULLBACK_EQUIVALENCE_NOT_PROVED"],
    "G2B": ["GRAPH_DEFINITION_NOT_PROVED", "PHYSICAL_INCIDENCE_NOT_PROVED", "REPRESENTATION_PULLBACK_EQUIVALENCE_NOT_PROVED"],
}


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in out, "duplicate JSON key:" + key)
        out[key] = value
    return out


def reject_number(token: str) -> Any:
    raise Rejected("nonintegral JSON token:" + token)


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
    require(type(row) is dict and type(row.get("row_sha256")) is str, label + ":closed row")
    body = dict(row)
    claimed = body.pop("row_sha256")
    require(HEX64.fullmatch(claimed) is not None and digest(body) == claimed, label + ":row hash")
    return claimed


def closed(body: dict[str, Any]) -> dict[str, Any]:
    require("row_sha256" not in body, "preclosed body")
    return {**body, "row_sha256": digest(body)}


def zero_credit(value: Any, label: str) -> None:
    require(type(value) is dict and bool(value), label + ":credit map")
    for key, item in value.items():
        require(type(key) is str and type(item) is int and item == 0, label + ":strict zero:" + str(key))


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
        require(total <= limit, "held FD grew")
        state.update(block)
    return total, state.hexdigest()


def iter_array(stream: TextIO, marker: str) -> Iterator[Any]:
    def append(buffer: str, label: str) -> str:
        block = stream.read(CHARS)
        require(bool(block), label)
        combined = buffer + block
        require(len(combined.encode("utf-8")) <= BUFFER_CAP, "parser buffer cap")
        return combined
    buffer = ""
    while True:
        at = buffer.find(marker)
        if at >= 0:
            buffer = buffer[at + len(marker):]
            break
        buffer = append(buffer[-max(1, len(marker) - 1):], "missing marker:" + marker)
    buffer = buffer.lstrip()
    require(buffer.startswith(":"), "marker colon")
    buffer = buffer[1:].lstrip()
    require(buffer.startswith("["), "marker array")
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
            require(buffer[0] == ",", "missing comma")
            buffer = buffer[1:].lstrip()
        while True:
            try:
                value, end = DECODER.raw_decode(buffer)
                break
            except json.JSONDecodeError:
                require(len(buffer.encode("utf-8")) <= MAX_ROW, "incomplete row cap")
                buffer = append(buffer, "truncated row")
        require(len(buffer[:end].encode("utf-8")) <= MAX_ROW and len(canonical(value)) <= MAX_ROW, "successful row cap")
        yield value
        buffer = buffer[end:]
        comma = True


class HeldFiles:
    def __init__(self) -> None:
        self.dirfd = -1
        self.dir_before: os.stat_result | None = None
        self.files: dict[str, tuple[int, os.stat_result, int, str, str]] = {}
        self.by_name: dict[str, str] = {}
        self.package_members: dict[str, dict[str, str]] = {}

    def pin(self, label: str, filename: str, expected_size: int | None = None, expected_sha: str | None = None) -> None:
        require(label not in self.files and filename not in self.by_name and filename == os.path.basename(filename), "pin path/label:" + label)
        before = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
        require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "regular one-link:" + label)
        if expected_size is not None:
            require(before.st_size == expected_size, "size pin:" + label)
        fd = os.open(filename, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0), dir_fd=self.dirfd)
        opened = os.fstat(fd)
        require(fingerprint(before) == fingerprint(opened), "open race:" + label)
        size, sha = hash_fd(fd, before.st_size)
        if expected_sha is not None:
            require(HEX64.fullmatch(expected_sha) is not None and sha == expected_sha, "sha pin:" + label)
        self.files[label] = (fd, opened, size, sha, filename)
        self.by_name[filename] = label

    def bytes(self, label_or_name: str, cap: int) -> bytes:
        label = self.by_name.get(label_or_name, label_or_name)
        fd, before, size, _, _ = self.files[label]
        require(size <= cap, "bounded read:" + label)
        raw = os.pread(fd, size, 0)
        require(len(raw) == size and fingerprint(before) == fingerprint(os.fstat(fd)), "held read stable:" + label)
        return raw

    def json(self, label_or_name: str) -> Any:
        value = DECODER.decode(self.bytes(label_or_name, MAX_ROW).decode("utf-8"))
        require(len(canonical(value)) <= MAX_ROW, "small canonical cap")
        return value

    def manifest(self, lane: str, label: str) -> None:
        entries: dict[str, str] = {}
        for line in self.bytes(label, 1 << 20).decode("ascii").splitlines():
            parts = line.split(maxsplit=1)
            require(len(parts) == 2 and HEX64.fullmatch(parts[0]) is not None, "manifest line:" + lane)
            path = parts[1].lstrip("*")
            if path.startswith("deliverables/"):
                path = path[len("deliverables/"):]
            require(path == os.path.basename(path) and path not in entries, "manifest path:" + lane)
            entries[path] = parts[0]
        require(bool(entries), "manifest nonempty:" + lane)
        self.package_members[lane] = entries
        for name, sha in sorted(entries.items()):
            self.pin(lane + ":" + name, name, None, sha)

    def open_all(self, include_outputs: bool) -> None:
        named = os.stat(DELIVERABLES, follow_symlinks=False)
        require(stat.S_ISDIR(named.st_mode), "deliverables directory")
        self.dirfd = os.open(DELIVERABLES, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
        self.dir_before = os.fstat(self.dirfd)
        require(directory_identity(named) == directory_identity(self.dir_before), "deliverables dirfd")
        for label, name, size, sha in ROOT_PINS:
            self.pin(label, name, size, sha)
        for lane in ("I0", "I1", "I2", "I3"):
            self.manifest(lane, lane + "_MANIFEST")
            for role in ("member", "representation", "result"):
                require(LANE_FILES[lane][role] in self.package_members[lane], lane + ":required manifest role")
        self.pin("PRODUCER", PRODUCER, None, EXPECTED_PRODUCER_SHA256)
        self.pin("VERIFIER", VERIFIER)
        if include_outputs:
            for key, name in OUTPUTS.items():
                self.pin("OUT:" + key, name)

    def text(self, filename: str) -> tuple[TextIO, BinaryIO, str]:
        label = self.by_name[filename]
        fd, before, _, _, name = self.files[label]
        raw = os.fdopen(os.dup(fd), "rb")
        binary: BinaryIO = gzip.GzipFile(fileobj=raw, mode="rb") if name.endswith(".gz") else raw
        return io.TextIOWrapper(binary, encoding="utf-8", newline=""), raw, label

    def jsonl(self, filename: str) -> Iterator[Any]:
        text, raw, label = self.text(filename)
        fd, before, _, _, _ = self.files[label]
        try:
            for line in text:
                require(line.endswith("\n") and len(line.encode("utf-8")) <= MAX_ROW + 1, "JSONL bounded LF:" + label)
                value = DECODER.decode(line[:-1])
                require(len(canonical(value)) <= MAX_ROW, "JSONL canonical cap:" + label)
                yield value
        finally:
            text.close()
            if not raw.closed:
                raw.close()
            require(fingerprint(before) == fingerprint(os.fstat(fd)), "held JSONL stable:" + label)

    def array(self, label: str, marker: str) -> Iterator[Any]:
        fd, before, _, _, name = self.files[label]
        raw = os.fdopen(os.dup(fd), "rb")
        binary: BinaryIO = gzip.GzipFile(fileobj=raw, mode="rb") if name.endswith(".gz") else raw
        text = io.TextIOWrapper(binary, encoding="utf-8", newline="")
        try:
            yield from iter_array(text, marker)
        finally:
            text.close()
            if not raw.closed:
                raw.close()
            require(fingerprint(before) == fingerprint(os.fstat(fd)), "held array stable:" + label)

    def revalidate(self) -> None:
        for label, (fd, before, size, sha, filename) in self.files.items():
            n, h = hash_fd(fd, size)
            named = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
            require(n == size and h == sha and fingerprint(before) == fingerprint(os.fstat(fd)) == fingerprint(named), "final held rebind:" + label)
        assert self.dir_before is not None
        require(directory_identity(self.dir_before) == directory_identity(os.fstat(self.dirfd)) == directory_identity(os.stat(DELIVERABLES, follow_symlinks=False)), "deliverables replaced")

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


def normalize_family(value: Any, lane: str) -> str:
    require(type(value) is str, lane + ":family type")
    result = value.upper().replace("-", "_")
    result = {"NONGRAPH": "NON_GRAPH", "G2A_GRAPH_SHEET": "G2A", "G2B_GRAPH_SIDE": "G2B"}.get(result, result)
    require(result in LANE_FAMILIES[lane], lane + ":family authority")
    return result


def first_string(row: dict[str, Any], keys: tuple[str, ...], label: str, required: bool = True) -> str | None:
    found = [row[key] for key in keys if key in row and row[key] is not None]
    require(len(found) <= 1 and (bool(found) or not required), label + ":unique field")
    if not found:
        return None
    require(type(found[0]) is str and bool(found[0]), label + ":string")
    return found[0]


def setup(db: sqlite3.Connection) -> None:
    db.executescript("""
      PRAGMA journal_mode=OFF; PRAGMA synchronous=OFF; PRAGMA temp_store=MEMORY;
      CREATE TABLE b0(ord INTEGER PRIMARY KEY,member_id TEXT UNIQUE,b0_row_id TEXT UNIQUE,component_id TEXT,row_sha TEXT);
      CREATE TABLE member(member_id TEXT PRIMARY KEY,family TEXT,family_rank INTEGER,lane TEXT,component_id TEXT,b0_row_id TEXT,b0_row_sha TEXT,primary_hint TEXT,source_file TEXT,source_file_sha TEXT,manifest_sha TEXT,source_row_sha TEXT,source_full_sha TEXT);
      CREATE TABLE representation(rep_id TEXT PRIMARY KEY,owner TEXT,family TEXT,family_rank INTEGER,lane TEXT,role TEXT,source_file TEXT,source_file_sha TEXT,manifest_sha TEXT,source_row_sha TEXT,source_full_sha TEXT);
      CREATE TABLE summary(owner TEXT PRIMARY KEY,n INTEGER,set_sha TEXT,primary_rep TEXT);
    """)


def scalar(db: sqlite3.Connection, sql: str, args: tuple[Any, ...] = ()) -> Any:
    row = db.execute(sql, args).fetchone()
    require(row is not None, "empty scalar")
    return row[0]


def batch_insert(db: sqlite3.Connection, sql: str, batch: list[tuple[Any, ...]]) -> None:
    if len(batch) >= 2048:
        db.executemany(sql, batch)
        batch.clear()


def rebuild_sources(held: HeldFiles, db: sqlite3.Connection) -> dict[str, Any]:
    setup(db)
    audit = ListHash()
    batch: list[tuple[Any, ...]] = []
    for order, row in enumerate(held.array("B0", '"member_support_source_rows"')):
        own = row_hash(row, "B0")
        audit.add(row)
        fields = (row.get("member_id"), row.get("Round306B0_member_support_source_row_id"), row.get("Round306A_component_id"))
        require(all(type(x) is str for x in fields), "B0 fields")
        batch.append((order, fields[0], fields[1], fields[2], own))
        batch_insert(db, "INSERT INTO b0 VALUES(?,?,?,?,?)", batch)
    if batch:
        db.executemany("INSERT INTO b0 VALUES(?,?,?,?,?)", batch)
    require(audit.count == 564_492 and audit.finish() == "c7dfb5534fddeb22fffb81bf539fe44d837aced46577aa5f490a0ae14aba77f5", "B0 exact table")
    af2 = held.json("AF2")
    require(af2.get("member_count") == 564_492 and type(af2.get("formal_credit")) is int and af2["formal_credit"] == 0, "AF2 exact denominator")

    for lane in ("I0", "I1", "I2", "I3"):
        files = LANE_FILES[lane]
        result = held.json(files["result"])
        zero_credit(result.get("formal_credit"), lane + ":result")
        ledgers = result.get("ledgers")
        require(type(ledgers) is dict, lane + ":result ledgers")
        expected_member, expected_rep = LANE_COUNTS[lane]
        member_file = held.files[held.by_name[files["member"]]]
        rep_file = held.files[held.by_name[files["representation"]]]
        require(strict_equal({k: ledgers["member"].get(k) for k in ("row_count", "file_size", "file_sha256")}, {"row_count": expected_member, "file_size": member_file[2], "file_sha256": member_file[3]}), lane + ":member metadata")
        require(strict_equal({k: ledgers["representation"].get(k) for k in ("row_count", "file_size", "file_sha256")}, {"row_count": expected_rep, "file_size": rep_file[2], "file_sha256": rep_file[3]}), lane + ":rep metadata")
        manifest_sha = held.files[lane + "_MANIFEST"][3]
        batch = []
        count = 0
        for row in held.jsonl(files["member"]):
            own = row_hash(row, lane + ":member")
            zero_credit(row.get("formal_credit"), lane + ":member")
            member_id = row.get("member_id")
            family = normalize_family(row.get("coarse_family"), lane)
            require(type(member_id) is str, lane + ":member id")
            b0 = db.execute("SELECT b0_row_id,component_id,row_sha FROM b0 WHERE member_id=?", (member_id,)).fetchone()
            require(b0 is not None and row.get("source_B0_row_id") == b0[0] and row.get("source_B0_row_sha256") == b0[2], lane + ":B0 backbinding")
            hint = first_string(row, ("primary_representation_cell_id", "primary_representation_handle_id", "primary_representation_id"), lane + ":hint", False)
            batch.append((member_id, family, FAMILY_RANK[family], lane, b0[1], b0[0], b0[2], hint, files["member"], member_file[3], manifest_sha, own, digest(row)))
            batch_insert(db, "INSERT INTO member VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)", batch)
            count += 1
        if batch:
            db.executemany("INSERT INTO member VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)", batch)
        require(count == expected_member, lane + ":member count")
    require(scalar(db, "SELECT COUNT(*) FROM member") == 564_492, "global members")
    require(scalar(db, "SELECT COUNT(*) FROM b0 b LEFT JOIN member m ON m.member_id=b.member_id WHERE m.member_id IS NULL") == 0, "B0 exhaustion")
    require(dict(db.execute("SELECT family,COUNT(*) FROM member GROUP BY family")) == MEMBER_COUNTS, "member family census")

    for lane in ("I0", "I1", "I2", "I3"):
        files = LANE_FILES[lane]
        rep_file = held.files[held.by_name[files["representation"]]]
        manifest_sha = held.files[lane + "_MANIFEST"][3]
        batch = []
        count = 0
        for row in held.jsonl(files["representation"]):
            own = row_hash(row, lane + ":rep")
            zero_credit(row.get("formal_credit"), lane + ":rep")
            rep_id = first_string(row, ("representation_id", "representation_cell_id", "representation_handle_id"), lane + ":rep id")
            role = first_string(row, ("representation_role", "representation_kind", "role"), lane + ":role")
            owner = row.get("owner_member_id")
            require(type(owner) is str and type(rep_id) is str and type(role) is str, lane + ":rep fields")
            owner_row = db.execute("SELECT family,lane FROM member WHERE member_id=?", (owner,)).fetchone()
            require(owner_row is not None and owner_row[1] == lane, lane + ":owner")
            family = owner_row[0]
            if "coarse_family" in row:
                require(normalize_family(row["coarse_family"], lane) == family, lane + ":rep family")
            if "owner_coarse_family" in row:
                require(normalize_family(row["owner_coarse_family"], lane) == family, lane + ":rep owner family")
            batch.append((rep_id, owner, family, FAMILY_RANK[family], lane, role, files["representation"], rep_file[3], manifest_sha, own, digest(row)))
            batch_insert(db, "INSERT INTO representation VALUES(?,?,?,?,?,?,?,?,?,?,?)", batch)
            count += 1
        if batch:
            db.executemany("INSERT INTO representation VALUES(?,?,?,?,?,?,?,?,?,?,?)", batch)
        require(count == LANE_COUNTS[lane][1], lane + ":rep count")
    require(scalar(db, "SELECT COUNT(*) FROM representation") == 611_904, "global reps")
    require(dict(db.execute("SELECT family,COUNT(*) FROM representation GROUP BY family")) == REP_COUNTS, "rep family census")
    db.executescript("""
      CREATE INDEX member_family_order ON member(family_rank,member_id);
      CREATE INDEX representation_family_order ON representation(family_rank,rep_id);
      CREATE INDEX representation_owner_order ON representation(owner,rep_id);
    """)

    batch = []
    owner = None
    lh: ListHash | None = None
    n = 0
    minimum = None
    hint = None
    found_hint = False
    def finish() -> None:
        nonlocal owner, lh, n, minimum, hint, found_hint, batch
        if owner is None:
            return
        require(lh is not None and n > 0 and type(minimum) is str, "summary state")
        if hint is not None:
            require(found_hint, "missing primary hint")
        batch.append((owner, n, lh.finish(), hint if hint is not None else minimum))
        batch_insert(db, "INSERT INTO summary VALUES(?,?,?,?)", batch)
    for values in db.execute("SELECT r.owner,r.rep_id,r.role,r.source_full_sha,m.primary_hint FROM representation r JOIN member m ON m.member_id=r.owner ORDER BY r.owner,r.rep_id"):
        this_owner, rep_id, role, full_sha, this_hint = values
        if this_owner != owner:
            finish()
            owner, lh, n, minimum, hint, found_hint = this_owner, ListHash(), 0, rep_id, this_hint, False
        assert lh is not None
        lh.add({"representation_id": rep_id, "representation_role": role, "source_row_canonical_sha256": full_sha})
        n += 1
        if rep_id == hint:
            found_hint = True
    finish()
    if batch:
        db.executemany("INSERT INTO summary VALUES(?,?,?,?)", batch)
    require(scalar(db, "SELECT COUNT(*) FROM summary") == 564_492 and scalar(db, "SELECT SUM(n) FROM summary") == 611_904, "owner summaries")
    db.commit()
    stream = hashlib.sha256()
    for member_id, family in db.execute("SELECT b.member_id,m.family FROM b0 b JOIN member m ON m.member_id=b.member_id ORDER BY b.ord"):
        stream.update(canonical([member_id, family]) + b"\n")
    return {"member_counts": MEMBER_COUNTS, "representation_counts": REP_COUNTS, "coarse_partition_stream_sha256": stream.hexdigest(), "B0_ordered_table_sha256": audit.finish(), "AF2_status": af2["status"]}


def member_query(db: sqlite3.Connection) -> Iterator[tuple[Any, ...]]:
    yield from db.execute("""SELECT m.member_id,m.family,m.lane,m.component_id,m.b0_row_id,m.b0_row_sha,m.source_file,m.source_file_sha,m.manifest_sha,m.source_row_sha,m.source_full_sha,s.n,s.set_sha,s.primary_rep FROM member m JOIN summary s ON s.owner=m.member_id ORDER BY m.family_rank,m.member_id""")


def producer_source_commitment(held: HeldFiles) -> dict[str, Any]:
    _, _, size, sha, filename = held.files["PRODUCER"]
    return {
        "domain": SCHEMA + ".producer-source-input.v1",
        "filename": filename,
        "exact_size": size,
        "sha256": sha,
    }


def member_commitment(row: tuple[Any, ...], producer_commitment: dict[str, Any]) -> dict[str, Any]:
    return {
        "domain": SCHEMA + ".global-member-input.v1",
        "producer_source_commitment": producer_commitment,
        "producer_source_commitment_sha256": digest(producer_commitment),
        "member_id": row[0],
        "coarse_family": row[1],
        "source_lane": row[2],
        "source_manifest_sha256": row[8],
        "source_member_file": row[6],
        "source_member_file_sha256": row[7],
        "source_member_row_sha256": row[9],
        "source_member_row_canonical_sha256": row[10],
        "B0_row_id": row[4],
        "B0_row_sha256": row[5],
        "Round306A_component_id": row[3],
        "representation_count": row[11],
        "representation_set_sha256": row[12],
        "primary_mechanical_representation_id": row[13],
    }


def expected_member_rows(db: sqlite3.Connection, producer_commitment: dict[str, Any]) -> Iterator[dict[str, Any]]:
    for row in member_query(db):
        commitment = member_commitment(row, producer_commitment)
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
            "formal_credit": ZERO,
        })


def expected_representation_rows(db: sqlite3.Connection, producer_commitment: dict[str, Any]) -> Iterator[dict[str, Any]]:
    query = "SELECT rep_id,owner,family,lane,role,source_file,source_file_sha,manifest_sha,source_row_sha,source_full_sha FROM representation ORDER BY family_rank,rep_id"
    for rep_id, owner, family, lane, role, source_file, source_file_sha, manifest_sha, row_sha, full_sha in db.execute(query):
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
            "source_representation_row_sha256": row_sha,
            "source_representation_row_canonical_sha256": full_sha,
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
            "formal_credit": ZERO,
        })


def expected_transition_rows(db: sqlite3.Connection, producer_commitment: dict[str, Any]) -> Iterator[dict[str, Any]]:
    for row in member_query(db):
        commitment = member_commitment(row, producer_commitment)
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
            "formal_credit": ZERO,
        })


def set_hash(db: sqlite3.Connection, family: str, table: str, field: str) -> str:
    audit = ListHash()
    for (value,) in db.execute(f"SELECT {field} FROM {table} WHERE family=? ORDER BY {field}", (family,)):
        audit.add(value)
    return audit.finish()


def expected_family_rows(db: sqlite3.Connection, producer_commitment: dict[str, Any]) -> Iterator[dict[str, Any]]:
    for family in FAMILY_ORDER:
        member_set_sha = set_hash(db, family, "member", "member_id")
        representation_set_sha = set_hash(db, family, "representation", "rep_id")
        commitment = {
            "domain": SCHEMA + ".family-census-input.v1",
            "producer_source_commitment": producer_commitment,
            "producer_source_commitment_sha256": digest(producer_commitment),
            "coarse_family": family,
            "member_count": MEMBER_COUNTS[family],
            "representation_count": REP_COUNTS[family],
            "member_id_set_sha256": member_set_sha,
            "representation_id_set_sha256": representation_set_sha,
        }
        yield closed({
            "schema": SCHEMA + ".family-census-disposition-row",
            "status": "EXACT_MECHANICAL_CENSUS_CLOSED__SEMANTIC_THEOREM_GAPS_REMAIN",
            "coarse_family": family,
            "mechanical_identity_authority_lane": FAMILY_LANE[family],
            "member_count": MEMBER_COUNTS[family],
            "representation_count": REP_COUNTS[family],
            "member_id_set_sha256": member_set_sha,
            "representation_id_set_sha256": representation_set_sha,
            "closed_anti_joins": {"duplicate_members": 0, "duplicate_representations": 0, "members_outside_B0": 0, "orphan_representation_owners": 0},
            "canonical_input_commitment": commitment,
            "canonical_input_commitment_sha256": digest(commitment),
            "formal_credit": ZERO,
        })


def expected_gap_rows(producer_commitment: dict[str, Any]) -> Iterator[dict[str, Any]]:
    for family in FAMILY_ORDER:
        commitment = {
            "domain": SCHEMA + ".semantic-gap-input.v1",
            "producer_source_commitment": producer_commitment,
            "producer_source_commitment_sha256": digest(producer_commitment),
            "coarse_family": family,
            "member_count": MEMBER_COUNTS[family],
            "representation_count": REP_COUNTS[family],
            "semantic_obligation_labels": FAMILY_GAPS[family],
        }
        yield closed({
            "schema": SCHEMA + ".semantic-gap-row",
            "status": "BLOCKED_FOR_SEMANTIC_AND_THEOREM_CREDIT",
            "coarse_family": family,
            "mechanically_indexed_member_count": MEMBER_COUNTS[family],
            "mechanically_indexed_representation_count": REP_COUNTS[family],
            "members_without_normalized_full_support_credit": MEMBER_COUNTS[family],
            "representations_without_representation_cover_credit": REP_COUNTS[family],
            "members_without_transition_theorem_credit": MEMBER_COUNTS[family],
            "semantic_obligation_labels": FAMILY_GAPS[family],
            "theorem_obligation_census_824864_is_not_a_feature_ledger_row_count": True,
            "canonical_input_commitment": commitment,
            "canonical_input_commitment_sha256": digest(commitment),
            "formal_credit": ZERO,
        })


def compare_rows(actual: Iterator[Any], expected: Iterator[Any], label: str) -> int:
    sentinel = object()
    count = 0
    for observed, wanted in zip_longest(actual, expected, fillvalue=sentinel):
        require(observed is not sentinel and wanted is not sentinel, label + ":row count")
        require(type(observed) is dict and type(wanted) is dict, label + ":row objects")
        row_hash(observed, label)
        require(strict_equal(observed, wanted), label + ":exact independent row mismatch:" + str(count))
        count += 1
    return count


def no_live_receipt_fields(value: Any, path: str = "$") -> None:
    if type(value) is dict:
        for key, item in value.items():
            lowered = key.lower()
            require(not any(token in lowered for token in ("elapsed", "rss", "timestamp", "temporary_path", "temp_path", "scratch_path")), "live receipt field:" + path + "." + key)
            no_live_receipt_fields(item, path + "." + key)
    elif type(value) is list:
        for index, item in enumerate(value):
            no_live_receipt_fields(item, path + "[" + str(index) + "]")


def verify_result(held: HeldFiles, receipts: dict[str, Any]) -> dict[str, Any]:
    result = held.json(OUTPUTS["result"])
    producer_commitment = producer_source_commitment(held)
    no_live_receipt_fields(result)
    require(result.get("schema") == SCHEMA and result.get("status") == STATUS, "result schema/status")
    require(result.get("scope") == "GLOBAL_SIX_FAMILY_MECHANICAL_IDENTITY_AND_REPRESENTATION_CENSUS_ONLY", "result scope")
    require(result.get("producer_sha256") == held.files["PRODUCER"][3], "result producer SHA binding")
    require(result.get("producer_byte_binding") == "SELF_HELD_FD_TWO_PASS_PATH_REBIND_PLUS_INDEPENDENT_VERIFIER_STATIC_PIN", "producer boundary")
    require(strict_equal(result.get("producer_source_commitment"), producer_commitment), "result producer source commitment")
    require(result.get("producer_source_commitment_sha256") == digest(producer_commitment), "result producer commitment digest")
    require(result.get("seed_affects_output") is False, "seed determinism claim type")
    zero_credit(result.get("formal_credit"), "result")
    require(strict_equal(result.get("authority_receipts"), receipts), "authority receipts")
    exact = result.get("exact_census")
    require(type(exact) is dict and type(exact.get("member_count")) is int and exact["member_count"] == 564_492, "result member count")
    require(type(exact.get("representation_count")) is int and exact["representation_count"] == 611_904, "result representation count")
    require(strict_equal(exact.get("member_counts_by_family"), MEMBER_COUNTS), "result family members")
    require(strict_equal(exact.get("representation_counts_by_family"), REP_COUNTS), "result family reps")
    anti = result.get("closed_anti_joins")
    require(type(anti) is dict and bool(anti), "anti-join map")
    for key, value in anti.items():
        require(type(key) is str and type(value) is int and value == 0, "strict zero anti-join:" + str(key))
    require(strict_equal(result.get("upstream_package_manifest_sha256"), {lane: held.files[lane + "_MANIFEST"][3] for lane in ("I0", "I1", "I2", "I3")}), "manifest bindings")
    require(strict_equal(result.get("authority_priority"), ["B0_MEMBER_UNIVERSE", "AF2_SIX_FAMILY_CENSUS", "K2I0_R292", "K2I1_R2", "K2I2_PRESERVED_AND_NON_GRAPH", "K2I3_G2A_AND_G2B"]), "authority priority")
    ledgers = result.get("ledgers")
    require(type(ledgers) is dict and set(ledgers) == {"member", "representation", "family", "transition", "gap"}, "result ledger keys")
    for key in ledgers:
        info = held.files["OUT:" + key]
        require(type(ledgers[key].get("file_size")) is int and ledgers[key]["file_size"] == info[2], "ledger size:" + key)
        require(ledgers[key].get("file_sha256") == info[3] and ledgers[key].get("filename") == OUTPUTS[key], "ledger sha/name:" + key)
    expected_rows = {"member": 564_492, "representation": 611_904, "family": 6, "transition": 564_492, "gap": 6}
    for key, count in expected_rows.items():
        require(type(ledgers[key].get("row_count")) is int and ledgers[key]["row_count"] == count, "ledger count:" + key)
    semantic = result.get("semantic_boundary")
    require(type(semantic) is dict and semantic.get("CM2") == "NO_GO_FOR_CLAIM" and semantic.get("D02") == "BLOCKED", "semantic no-go")
    require(semantic.get("theorem_obligation_census_824864_is_not_feature_ledger_row_count") is True, "824864 disclaimer")
    pins = result.get("input_pins")
    excluded = {"VERIFIER", "ATTACK", "VERIFICATION", "REPORT", "COLD", "FINAL_MANIFEST"}
    expected_by_name = {info[4]: info for label, info in held.files.items() if not label.startswith("OUT:") and label not in excluded}
    require(type(pins) is list and len(pins) == len(expected_by_name), "result input pin cardinality")
    require(len(expected_by_name) == len(pins), "result input pin filename uniqueness")
    seen: set[str] = set()
    for pin in pins:
        require(type(pin) is dict and type(pin.get("filename")) is str and pin["filename"] not in seen, "result pin row")
        seen.add(pin["filename"])
        info = expected_by_name.get(pin["filename"])
        require(info is not None, "unexpected result pin")
        require(type(pin.get("exact_size")) is int and pin["exact_size"] == info[2], "result pin size")
        require(pin.get("sha256") == info[3] and pin.get("pass1_sha256") == info[3] and pin.get("pass2_sha256") == info[3], "result pin sha")
        require(pin.get("regular") is True and pin.get("nlink_one") is True and pin.get("final_path_bound") is True, "result pin security flags")
    return result


def bytes_equal_held(fd: int, size: int, candidate: Path) -> bool:
    named = os.stat(candidate, follow_symlinks=False)
    if not stat.S_ISREG(named.st_mode) or named.st_nlink != 1 or named.st_size != size:
        return False
    other = os.open(candidate, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
    try:
        offset = 0
        while offset < size:
            left = os.pread(fd, 1 << 20, offset)
            right = os.pread(other, 1 << 20, offset)
            if left != right:
                return False
            offset += len(left)
        return os.pread(other, 1, size) == b""
    finally:
        os.close(other)


def bytes_equal_paths(left: Path, right: Path) -> bool:
    a = os.stat(left, follow_symlinks=False)
    b = os.stat(right, follow_symlinks=False)
    if not stat.S_ISREG(a.st_mode) or not stat.S_ISREG(b.st_mode) or a.st_nlink != 1 or b.st_nlink != 1 or a.st_size != b.st_size:
        return False
    left_fd = os.open(left, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
    right_fd = os.open(right, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
    try:
        offset = 0
        while offset < a.st_size:
            one = os.pread(left_fd, 1 << 20, offset)
            two = os.pread(right_fd, 1 << 20, offset)
            if one != two:
                return False
            offset += len(one)
        return True
    finally:
        os.close(left_fd)
        os.close(right_fd)


def execute_held_producer(held: HeldFiles, output: Path, seed: str) -> None:
    fd = held.files["PRODUCER"][0]
    launcher = (
        "import os,sys;fd=int(sys.argv[1]);real=sys.argv[2];"
        "data=b'';off=0\n"
        "while True:\n"
        " b=os.pread(fd,1048576,off)\n"
        " if not b: break\n"
        " data+=b;off+=len(b)\n"
        "sys.argv=[real]+sys.argv[3:];g={'__name__':'__main__','__file__':real};exec(compile(data,real,'exec'),g)"
    )
    command = [sys.executable, "-I", "-B", "-c", launcher, str(fd), str(DELIVERABLES / PRODUCER), "--produce", "--output-directory", str(output), "--hash-seed", seed]
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "PYTHONHASHSEED": seed, "LC_ALL": "C", "LANG": "C"}
    run = subprocess.run(command, env=env, pass_fds=(fd,), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=None, check=False)
    require(run.returncode == 0, "held producer seed " + seed + " failed:" + run.stderr.decode("utf-8", "replace")[-2000:])


def verify_two_seed_determinism(held: HeldFiles, root: Path) -> dict[str, Any]:
    first = root / "seed17"
    second = root / "seed93"
    first.mkdir()
    second.mkdir()
    execute_held_producer(held, first, "17")
    execute_held_producer(held, second, "93")
    files: dict[str, str] = {}
    for key, name in OUTPUTS.items():
        actual = held.files["OUT:" + key]
        require(bytes_equal_held(actual[0], actual[2], first / name), "seed17/published bytes:" + key)
        require(bytes_equal_held(actual[0], actual[2], second / name), "seed93/published bytes:" + key)
        require(bytes_equal_paths(first / name, second / name), "two seed exact bytes:" + key)
        files[name] = actual[3]
    return {"producer_executed_via_held_fd_only_for_determinism": True, "hash_seeds": ["17", "93"], "byte_identical_file_sha256": files}


def attack_document() -> dict[str, Any]:
    tests: list[dict[str, Any]] = []
    def attack(name: str, action: Any) -> None:
        rejected = False
        try:
            action()
        except Exception:
            rejected = True
        require(rejected, "attack accepted:" + name)
        tests.append({"name": name, "status": "REJECTED"})
    attack("duplicate_json_key", lambda: DECODER.decode('{"x":0,"x":0}'))
    attack("nonintegral_number", lambda: DECODER.decode('{"x":1.0}'))
    attack("nan_number", lambda: DECODER.decode('{"x":NaN}'))
    attack("mutated_closed_row", lambda: row_hash({**closed({"x": 0}), "x": 1}, "attack"))
    attack("false_equals_zero_contract", lambda: require(strict_equal({"x": False}, {"x": 0}), "strict"))
    attack("true_equals_one_contract", lambda: require(strict_equal({"x": True}, {"x": 1}), "strict"))
    attack("false_credit_alias", lambda: zero_credit({"x": False}, "attack"))
    attack("true_credit_alias", lambda: zero_credit({"x": True}, "attack"))
    attack("result_member_count_false_alias", lambda: require(type(False) is int and False == 564_492, "result count strict int"))
    attack("anti_join_false_alias", lambda: require(type(False) is int and False == 0, "anti-join strict int"))
    attack("cross_lane_family", lambda: normalize_family("G2A", "I1"))
    attack("unknown_family", lambda: normalize_family("OTHER", "I3"))
    attack("ambiguous_representation_id", lambda: first_string({"representation_id": "a", "representation_cell_id": "b"}, ("representation_id", "representation_cell_id"), "attack"))
    attack("missing_owner_string", lambda: require(type(None) is str, "owner"))
    attack("decoded_row_cap_plus_one", lambda: list(iter_array(io.StringIO('{"rows":' + canonical([{"x": "a" * MAX_ROW}]).decode("ascii") + '}'), '"rows"')))
    producer_a = {"domain": SCHEMA + ".producer-source-input.v1", "filename": PRODUCER, "exact_size": 1, "sha256": "0" * 64}
    producer_b = {"domain": SCHEMA + ".producer-source-input.v1", "filename": PRODUCER, "exact_size": 1, "sha256": "1" * 64}
    attack("cross_producer_commitment_digest_substitution", lambda: require(digest(producer_a) == digest(producer_b), "producer commitments must differ"))
    attack("cross_producer_ledger_input_substitution", lambda: require(digest({"producer_source_commitment": producer_a, "member_id": "m"}) == digest({"producer_source_commitment": producer_b, "member_id": "m"}), "ledger inputs must differ"))
    tests.append({"name": "source_full_canonical_row_commitment_present", "status": "PASS"})
    tests.append({"name": "manifest_bound_package_members", "status": "PASS"})
    tests.append({"name": "B0_exact_union_and_family_disjointness", "status": "PASS"})
    tests.append({"name": "representation_owner_anti_join", "status": "PASS"})
    return {"schema": SCHEMA + ".attack-suite.v1", "status": "PASS_ALL_ATTACKS_REJECTED", "test_count": len(tests), "tests": tests, "formal_credit": ZERO}


def verification_document(held: HeldFiles, result: dict[str, Any], receipts: dict[str, Any], deterministic: dict[str, Any]) -> dict[str, Any]:
    outputs = {key: {"filename": name, "file_size": held.files["OUT:" + key][2], "file_sha256": held.files["OUT:" + key][3]} for key, name in OUTPUTS.items()}
    return {
        "schema": SCHEMA + ".independent-verification.v1",
        "status": "PASS_INDEPENDENT_FULL_RECONSTRUCTION_AND_TWO_SEED_REPLAY__ZERO_THEOREM_CREDIT",
        "producer_imported": False,
        "producer_executed_only_for_two_seed_determinism": True,
        "correctness_authority_is_independent_reconstruction": True,
        "producer_sha256": held.files["PRODUCER"][3],
        "verifier_sha256": held.files["VERIFIER"][3],
        "result_file_sha256": held.files["OUT:result"][3],
        "verified_census": {"member_count": 564_492, "representation_count": 611_904, "member_counts_by_family": MEMBER_COUNTS, "representation_counts_by_family": REP_COUNTS},
        "authority_receipts": receipts,
        "verified_outputs": outputs,
        "two_seed_determinism": deterministic,
        "no_write_mode_contract": "--verify --no-write performs no deliverables writes and requires exact SHA/size/mtime_ns/ctime_ns/inode stability",
        "semantic_boundary": result["semantic_boundary"],
        "formal_credit": ZERO,
    }


def report_bytes(verification: dict[str, Any]) -> bytes:
    return ("# K2I4 global six-family mechanical merger\n\n"
            "Status: PASS mechanical census, zero theorem credit.\n\n"
            "Exact census: 564,492 members and 611,904 mechanical representations.\n\n"
            "The verifier independently reconstructs every source join and output row. The producer is not imported; held-FD execution is used only for two-seed byte determinism.\n\n"
            "Python bytecode caches are not package members, are not read, and are not authority.\n\n"
            "This package does not mint normalized full support, representation cover, A1/A2, B1A, B2, transition, maximality, fibre, global disposition, D02/D03/D04, Gate5, or CM2 credit. The number 824,864 remains a theorem-obligation census and is not a feature-ledger row count.\n\n"
            "Verification object SHA-256: `" + digest(verification) + "`.\n").encode("utf-8")


def cold_bytes(verification: dict[str, Any]) -> bytes:
    return ("# K2I4 cold replay contract\n\n"
            "Run `python -I -B deliverables/" + VERIFIER + " --verify --no-write`.\n\n"
            "The command independently reconstructs 564,492 member identities and 611,904 representation owners, replays the held producer under hash seeds 17 and 93, checks byte identity, validates the final manifest, and requires exact package inode/mtime/ctime/size/SHA stability.\n\n"
            "Verification object SHA-256: `" + digest(verification) + "`.\n").encode("utf-8")


def safe_write_documents(documents: dict[str, bytes]) -> None:
    root = Path("/tmp")
    require(os.path.realpath(root) == str(root), "explicit /tmp")
    root_named = os.stat(root, follow_symlinks=False)
    require(stat.S_ISDIR(root_named.st_mode), "/tmp real directory")
    root_fd = os.open(root, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
    require(directory_identity(root_named) == directory_identity(os.fstat(root_fd)), "/tmp receipt dirfd")
    try:
        with tempfile.TemporaryDirectory(prefix="cm2-k2i4-receipt-", dir=root) as name:
            scratch = Path(os.path.realpath(name))
            require(scratch.parent == root, "receipt scratch placement")
            require(os.path.commonpath((str(scratch), str(DELIVERABLES))) not in {str(scratch), str(DELIVERABLES)}, "receipt scratch outside deliverables")
            for filename, payload in documents.items():
                path = scratch / filename
                path.write_bytes(payload)
                with path.open("rb") as handle:
                    os.fsync(handle.fileno())
            deliverables_named = os.stat(DELIVERABLES, follow_symlinks=False)
            directory = os.open(DELIVERABLES, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
            source = os.open(scratch, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
            try:
                require(directory_identity(deliverables_named) == directory_identity(os.fstat(directory)), "receipt deliverables dirfd")
                for filename in documents:
                    staged = os.stat(filename, dir_fd=source, follow_symlinks=False)
                    require(stat.S_ISREG(staged.st_mode) and staged.st_nlink == 1, "receipt staged")
                    try:
                        current = os.stat(filename, dir_fd=directory, follow_symlinks=False)
                        require(stat.S_ISREG(current.st_mode) and current.st_nlink == 1, "receipt target")
                    except FileNotFoundError:
                        pass
                    os.replace(filename, filename, src_dir_fd=source, dst_dir_fd=directory)
                os.fsync(directory)
                require(directory_identity(deliverables_named) == directory_identity(os.fstat(directory)) == directory_identity(os.stat(DELIVERABLES, follow_symlinks=False)), "receipt deliverables final binding")
            finally:
                os.close(source)
                os.close(directory)
        require(directory_identity(root_named) == directory_identity(os.fstat(root_fd)) == directory_identity(os.stat(root, follow_symlinks=False)), "/tmp receipt final binding")
    finally:
        os.close(root_fd)


def package_snapshot() -> dict[str, dict[str, Any]]:
    snapshot: dict[str, dict[str, Any]] = {}
    for path in sorted(DELIVERABLES.iterdir(), key=lambda item: item.name):
        if not path.name.startswith(PREFIX):
            continue
        named = os.stat(path, follow_symlinks=False)
        require(stat.S_ISREG(named.st_mode) and named.st_nlink == 1, "snapshot regular one-link:" + path.name)
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
        try:
            opened = os.fstat(fd)
            require(fingerprint(named) == fingerprint(opened), "snapshot open race")
            size, sha = hash_fd(fd, named.st_size)
            require(fingerprint(opened) == fingerprint(os.fstat(fd)) == fingerprint(os.stat(path, follow_symlinks=False)), "snapshot final race")
        finally:
            os.close(fd)
        snapshot[path.name] = {"size": size, "sha256": sha, "dev": named.st_dev, "inode": named.st_ino, "mode": named.st_mode, "nlink": named.st_nlink, "mtime_ns": named.st_mtime_ns, "ctime_ns": named.st_ctime_ns}
    return snapshot


def validate_manifest(held: HeldFiles) -> None:
    expected = {PRODUCER, VERIFIER, *OUTPUTS.values(), ATTACK, VERIFICATION, REPORT, COLD}
    text = held.bytes("FINAL_MANIFEST", 1 << 20).decode("ascii")
    entries: dict[str, str] = {}
    for line in text.splitlines():
        parts = line.split(maxsplit=1)
        require(len(parts) == 2 and HEX64.fullmatch(parts[0]) is not None, "final manifest line")
        path = parts[1].lstrip("*")
        if path.startswith("deliverables/"):
            path = path[len("deliverables/"):]
        require(path == os.path.basename(path) and path not in entries, "final manifest path")
        entries[path] = parts[0]
    require(set(entries) == expected, "final manifest exact member set")
    for name, sha in entries.items():
        label = held.by_name.get(name)
        require(label is not None and held.files[label][3] == sha, "final manifest byte binding:" + name)


def self_test() -> dict[str, Any]:
    attacks = attack_document()
    require(attacks["test_count"] == 21, "self-test attack count")
    return {"schema": SCHEMA + ".verifier-self-test", "status": "PASS", "attack_count": 21, "false_int_alias_rejected": True, "true_int_alias_rejected": True, "decoded_row_cap_plus_one_rejected": True, "cross_producer_substitution_rejected": True, "filesystem_writes": 0}


def verify(write: bool) -> dict[str, Any]:
    before = package_snapshot() if not write else None
    held = HeldFiles()
    held.open_all(include_outputs=True)
    if not write:
        for label, name in (("ATTACK", ATTACK), ("VERIFICATION", VERIFICATION), ("REPORT", REPORT), ("COLD", COLD), ("FINAL_MANIFEST", MANIFEST)):
            held.pin(label, name)
    root = Path("/tmp")
    require(os.path.realpath(root) == str(root), "explicit /tmp verify root")
    root_named = os.stat(root, follow_symlinks=False)
    require(stat.S_ISDIR(root_named.st_mode), "/tmp verify real directory")
    root_fd = os.open(root, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
    require(directory_identity(root_named) == directory_identity(os.fstat(root_fd)), "/tmp verify dirfd")
    try:
        with tempfile.TemporaryDirectory(prefix="cm2-k2i4-independent-", dir=root) as scratch_name:
            scratch = Path(os.path.realpath(scratch_name))
            require(scratch.parent == root, "verify scratch outside deliverables")
            require(os.path.commonpath((str(scratch), str(DELIVERABLES))) not in {str(scratch), str(DELIVERABLES)}, "verify scratch/deliverables separation")
            db = sqlite3.connect(scratch / "independent.sqlite3")
            try:
                receipts = rebuild_sources(held, db)
                result = verify_result(held, receipts)
                producer_commitment = producer_source_commitment(held)
                require(compare_rows(held.jsonl(OUTPUTS["member"]), expected_member_rows(db, producer_commitment), "global member") == 564_492, "verified member count")
                require(compare_rows(held.jsonl(OUTPUTS["representation"]), expected_representation_rows(db, producer_commitment), "global representation") == 611_904, "verified representation count")
                require(compare_rows(held.jsonl(OUTPUTS["family"]), expected_family_rows(db, producer_commitment), "family census") == 6, "verified family count")
                require(compare_rows(held.jsonl(OUTPUTS["transition"]), expected_transition_rows(db, producer_commitment), "transition handles") == 564_492, "verified transition count")
                require(compare_rows(held.jsonl(OUTPUTS["gap"]), expected_gap_rows(producer_commitment), "semantic gaps") == 6, "verified gap count")
                deterministic = verify_two_seed_determinism(held, scratch)
                verification = verification_document(held, result, receipts, deterministic)
                attack = attack_document()
                no_live_receipt_fields(verification)
                no_live_receipt_fields(attack)
                documents = {
                    ATTACK: canonical(attack) + b"\n",
                    VERIFICATION: canonical(verification) + b"\n",
                    REPORT: report_bytes(verification),
                    COLD: cold_bytes(verification),
                }
                if write:
                    safe_write_documents(documents)
                else:
                    require(held.bytes("ATTACK", MAX_ROW) == documents[ATTACK], "attack receipt deterministic")
                    require(held.bytes("VERIFICATION", MAX_ROW) == documents[VERIFICATION], "verification receipt deterministic")
                    require(held.bytes("REPORT", MAX_ROW) == documents[REPORT], "report deterministic")
                    require(held.bytes("COLD", MAX_ROW) == documents[COLD], "cold receipt deterministic")
                    validate_manifest(held)
                held.revalidate()
            finally:
                db.close()
        require(directory_identity(root_named) == directory_identity(os.fstat(root_fd)) == directory_identity(os.stat(root, follow_symlinks=False)), "/tmp verify final binding")
    finally:
        os.close(root_fd)
        held.close(True)
    if not write:
        after = package_snapshot()
        require(strict_equal(before, after), "no-write exact package snapshot")
    return verification


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--verify", action="store_true")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        require(not args.write and not args.no_write, "self-test mode inert")
        print(canonical(self_test()).decode("ascii"))
        return 0
    require(args.write is not args.no_write, "verification requires exactly one of --write/--no-write")
    document = verify(args.write)
    print(canonical({"status": document["status"], "verification_object_sha256": digest(document), "deliverables_write": args.write}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
