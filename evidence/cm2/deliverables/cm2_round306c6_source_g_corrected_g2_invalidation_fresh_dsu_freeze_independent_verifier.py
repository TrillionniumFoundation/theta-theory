#!/usr/bin/env python3
"""Independently replay the C6 corrected G2 invalidation and fresh DSU freeze."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
import gzip
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import tempfile
from typing import Any, Final, Iterable, Iterator


class Blocked(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Blocked(label)


ROOT: Final = Path(__file__).parent
PREFIX: Final = "cm2_round306c6_source_g_corrected_g2_invalidation_fresh_dsu_freeze"
SCHEMA: Final = "cm2.round306c6.source-g-corrected-g2-invalidation-fresh-dsu-freeze.v1"
INVALIDATION_SCHEMA: Final = SCHEMA + ".member-invalidation-row.v1"
ROOT_SCHEMA: Final = SCHEMA + ".base-root-disposition-row.v1"
EDGE_SCHEMA: Final = SCHEMA + ".edge-application-row.v1"
MEMBER_SCHEMA: Final = SCHEMA + ".member-component-row.v1"
ROOT_COMPONENT_SCHEMA: Final = SCHEMA + ".base-root-component-row.v1"
COMPONENT_SCHEMA: Final = SCHEMA + ".component-census-row.v1"
NEW_ROOT_NAMESPACE: Final = "round306c6-corrected-g2-base-root:"
COMPONENT_NAMESPACE: Final = "round306c6-corrected-g2-component:"
RESULT_NAME: Final = PREFIX + "_result.json"
INVALIDATION_NAME: Final = PREFIX + "_member_invalidation_ledger.jsonl.gz"
ROOT_NAME: Final = PREFIX + "_base_root_disposition_ledger.jsonl.gz"
EDGE_NAME: Final = PREFIX + "_edge_application_ledger.jsonl.gz"
MEMBER_NAME: Final = PREFIX + "_member_component_ledger.jsonl.gz"
ROOT_COMPONENT_NAME: Final = PREFIX + "_base_root_component_ledger.jsonl.gz"
COMPONENT_NAME: Final = PREFIX + "_component_census.jsonl.gz"
CROSS_NAME: Final = PREFIX + "_cross_component_pair_denominator.json"
OUTPUT_ORDER: Final = (INVALIDATION_NAME, ROOT_NAME, EDGE_NAME, MEMBER_NAME, ROOT_COMPONENT_NAME, COMPONENT_NAME, CROSS_NAME, RESULT_NAME)


@dataclass(frozen=True)
class Pin:
    role: str
    filename: str
    size: int
    sha256: str


PINS: Final = (
    Pin("C0_MANIFEST", "cm2_round306c0_source_g_r235d_corrected_fresh_freeze_manifest.sha256", 2_182, "9ddb6e0ad37b634de8b2edf8573247e7c1263a5c3693c77a7d001241712b25f8"),
    Pin("C0_RESULT", "cm2_round306c0_source_g_r235d_corrected_fresh_freeze_result.json", 10_689, "4adcc91dd6bcaf71853d429e16f91d7ed93d04641097d12abe0ebc5a7e8864a1"),
    Pin("C0_MEMBER", "cm2_round306c0_source_g_r235d_corrected_fresh_freeze_fresh_member_component_ledger.jsonl.gz", 188_288_564, "81c5a772b12dfb0cf9196b13319bbdff7b07806f6df22d9966a4fc9399bed12e"),
    Pin("C0_EDGE", "cm2_round306c0_source_g_r235d_corrected_fresh_freeze_edge_remap_application_ledger.jsonl.gz", 165_250_881, "26c941631a839d757fb764486f5334fb913146a5cfaa8f65622e9b71b204b907"),
    Pin("C5_MANIFEST", "cm2_round306c5_source_g_corrected_g2_graph_semantic_classification_manifest.sha256", 1_193, "aefe82ef88c2ddf5f241d76e0f0f7483e230d68219ace6639f7389adbcb14134"),
    Pin("C5_RESULT", "cm2_round306c5_source_g_corrected_g2_graph_semantic_classification_result.json", 6_975, "0da7931e1a46d68ae8da69a7de1534a3955c83a8d6f5d8ab0170be7a34dc6320"),
    Pin("C5_LEDGER", "cm2_round306c5_source_g_corrected_g2_graph_semantic_classification_row_ledger.jsonl.gz", 78_082_824, "8f28efab9465440a0d6549f99a91d9b3997266f98a9c2eb06eda61ecdc42f333"),
)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def objsha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def identity(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def hash_fd(fd: int) -> str:
    os.lseek(fd, 0, os.SEEK_SET)
    digest = hashlib.sha256()
    while True:
        block = os.read(fd, 1_048_576)
        if not block:
            return digest.hexdigest()
        digest.update(block)


class Snapshot:
    def __init__(self) -> None:
        self.dirfd = -1
        self.fds: dict[str, int] = {}
        self.identities: dict[str, tuple[int, ...]] = {}

    def __enter__(self) -> "Snapshot":
        before = os.stat(ROOT, follow_symlinks=False)
        need(stat.S_ISDIR(before.st_mode) and not ROOT.is_symlink(), "deliverables directory")
        self.dirfd = os.open(ROOT, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
        for pin in (*PINS, PRODUCER_PIN):
            info = os.stat(pin.filename, dir_fd=self.dirfd, follow_symlinks=False)
            need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and info.st_size == pin.size, "pin identity:" + pin.role)
            fd = os.open(pin.filename, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=self.dirfd)
            opened = os.fstat(fd)
            need(identity(opened) == identity(info), "pin race:" + pin.role)
            need(hash_fd(fd) == hash_fd(fd) == pin.sha256, "pin digest:" + pin.role)
            self.fds[pin.role] = fd
            self.identities[pin.role] = identity(opened)
        return self

    def read(self, role: str) -> bytes:
        fd = self.fds[role]
        os.lseek(fd, 0, os.SEEK_SET)
        blocks: list[bytes] = []
        while True:
            block = os.read(fd, 1_048_576)
            if not block:
                return b"".join(blocks)
            blocks.append(block)

    def gzip_lines(self, role: str) -> Iterator[bytes]:
        duplicate = os.dup(self.fds[role])
        os.lseek(duplicate, 0, os.SEEK_SET)
        with os.fdopen(duplicate, "rb", closefd=True) as source:
            with gzip.GzipFile(fileobj=source, mode="rb") as stream:
                for line in stream:
                    yield line

    def final(self) -> None:
        for pin in reversed((*PINS, PRODUCER_PIN)):
            fd = self.fds[pin.role]
            need(identity(os.fstat(fd)) == self.identities[pin.role], "final pin fd:" + pin.role)
            need(identity(os.stat(pin.filename, dir_fd=self.dirfd, follow_symlinks=False)) == self.identities[pin.role], "final pin path:" + pin.role)
            need(hash_fd(fd) == pin.sha256, "final pin digest:" + pin.role)

    def __exit__(self, *_: Any) -> None:
        for fd in self.fds.values():
            try:
                os.close(fd)
            except OSError:
                pass
        if self.dirfd >= 0:
            os.close(self.dirfd)


def direct(snapshot: Snapshot, role: str) -> dict[str, Any]:
    raw = snapshot.read(role)
    value = json.loads(raw)
    need(type(value) is dict and raw == canonical(value), "canonical direct:" + role)
    if "result_sha256" in value:
        body = dict(value)
        need(body.pop("result_sha256") == objsha(body), "result closure:" + role)
    return value


def manifest_map(snapshot: Snapshot, role: str) -> dict[str, str]:
    raw = snapshot.read(role)
    need(raw.endswith(b"\n"), "manifest newline:" + role)
    result: dict[str, str] = {}
    for line in raw.decode("ascii").splitlines():
        digest, filename = line.split("  ")
        need(len(digest) == 64 and filename not in result, "manifest row:" + role)
        result[filename] = digest
    return result


def closed_row(line: bytes, schema: str, ordinal_field: str | None, ordinal: int, label: str) -> tuple[dict[str, Any], str]:
    need(line.endswith(b"\n"), "row newline:" + label)
    raw = line[:-1]
    row = json.loads(raw)
    need(type(row) is dict and canonical(row) == raw and row.get("schema") == schema, "canonical row:" + label)
    if ordinal_field is not None:
        need(row.get(ordinal_field) == ordinal, "row ordinal:" + label)
    body = dict(row)
    need(body.pop("row_sha256", None) == objsha(body), "row closure:" + label)
    return row, hashlib.sha256(raw).hexdigest()


class DSU:
    def __init__(self, items: Iterable[str]) -> None:
        self.items = sorted(items)
        self.index = {item: ordinal for ordinal, item in enumerate(self.items)}
        need(len(self.index) == len(self.items), "DSU duplicate item")
        self.parent = list(range(len(self.items)))
        self.size = [1] * len(self.items)
        self.rank_reduction = 0

    def find(self, ordinal: int) -> int:
        while self.parent[ordinal] != ordinal:
            self.parent[ordinal] = self.parent[self.parent[ordinal]]
            ordinal = self.parent[ordinal]
        return ordinal

    def union(self, left: str, right: str) -> int:
        try:
            a = self.find(self.index[left])
            b = self.find(self.index[right])
        except KeyError as error:
            raise Blocked("edge references missing root") from error
        if a == b:
            return 0
        if self.size[a] < self.size[b] or (self.size[a] == self.size[b] and self.items[a] > self.items[b]):
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        self.rank_reduction += 1
        return 1

    def partition(self) -> list[list[str]]:
        groups: dict[int, list[str]] = defaultdict(list)
        for ordinal, item in enumerate(self.items):
            groups[self.find(ordinal)].append(item)
        return sorted(sorted(group) for group in groups.values())


class SequenceHash:
    def __init__(self) -> None:
        self.digest = hashlib.sha256()
        self.digest.update(b"[")
        self.first = True

    def add_wire(self, raw: bytes) -> None:
        if not self.first:
            self.digest.update(b",")
        self.digest.update(raw)
        self.first = False

    def add(self, value: Any) -> None:
        self.add_wire(canonical(value))

    def finish(self) -> str:
        copy = self.digest.copy()
        copy.update(b"]")
        return copy.hexdigest()



PRODUCER_PIN: Final = Pin("PRODUCER", "cm2_round306c6_source_g_corrected_g2_invalidation_fresh_dsu_freeze_producer.py", 38_788, "f44e2f77f000ae34e3b0a4355d1a10c77c69c2fbef5746374d81b03e0460d7d1")
PRODUCER_NAME: Final = PRODUCER_PIN.filename
VERIFIER_NAME: Final = PREFIX + "_independent_verifier.py"
ATTACK_NAME: Final = PREFIX + "_attack_suite.json"
VERIFICATION_NAME: Final = PREFIX + "_verification.json"
REPORT_NAME: Final = PREFIX + "_report.md"
COLD_NAME: Final = PREFIX + "_cold_replay.md"
MANIFEST_NAME: Final = PREFIX + "_manifest.sha256"
PACKAGE_MEMBERS: Final = (PRODUCER_NAME, *OUTPUT_ORDER, VERIFIER_NAME, ATTACK_NAME, VERIFICATION_NAME, REPORT_NAME, COLD_NAME)
CANDIDATE_PINS: Final = {
    INVALIDATION_NAME: (37_615_714, "7f4c361b5039b9adac60cdb08405f384dc4a05bbe66b4ae2eac49ac02204e3db"),
    ROOT_NAME: (87_593_940, "42873309e86486edb03a45bb365735d4c9d94b7f6af49f09cf003a8663b6a9e0"),
    EDGE_NAME: (161_025_678, "9d0421e5e01a14b67a005894ce6b73b3abe2443d95a9194ca52b55d6314554cb"),
    MEMBER_NAME: (213_125_489, "730a1501402d29f9689655b0093edd4d7e499f3a34c6b65e9f21ee6f3f5ffce2"),
    ROOT_COMPONENT_NAME: (86_425_898, "6ba4dcaf45c125c7afbfd5cdf9ad60ef5fa16f26ba123d443cbc3d2f2d905165"),
    COMPONENT_NAME: (10_691_452, "a5aea01409ae3678fdc6b86fc3f1edfdfa41da013809dbadd217dda7e2eaf389"),
    CROSS_NAME: (505, "24b05554613dff1b4615a927d26fb5b15859b2ce59355421fde844243d60d2de"),
    RESULT_NAME: (9_329, "3f4e3e666dfe0b5b3a163c866057031b42dac09000175f4bc0b32ec353c5e4c5"),
}


def source_ref(ordinal: int, row: dict[str, Any], wire_sha: str, row_id_field: str) -> list[Any]:
    return [ordinal, row[row_id_field], wire_sha, row["row_sha256"]]


class CandidateFiles:
    def __init__(self, directory: Path, pinned: bool = True) -> None:
        self.directory = Path(os.path.abspath(directory))
        self.pinned = pinned
        self.dirfd = -1
        self.directory_identity: tuple[int, ...] = ()
        self.fds: dict[str, int] = {}
        self.identities: dict[str, tuple[int, ...]] = {}

    def __enter__(self) -> "CandidateFiles":
        resolved = self.directory.resolve()
        need(os.path.commonpath((str(resolved), str(ROOT.resolve()))) != str(ROOT.resolve()), "candidate outside deliverables")
        before = os.stat(self.directory, follow_symlinks=False)
        need(stat.S_ISDIR(before.st_mode), "candidate directory identity")
        self.dirfd = os.open(self.directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
        opened_directory = os.fstat(self.dirfd)
        need(identity(opened_directory) == identity(before), "candidate directory race")
        self.directory_identity = identity(opened_directory)
        need(set(os.listdir(self.dirfd)) == set(OUTPUT_ORDER), "candidate exact set")
        for filename in OUTPUT_ORDER:
            expected_size, expected_sha = CANDIDATE_PINS[filename]
            info = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
            need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "candidate identity:" + filename)
            if self.pinned:
                need(info.st_size == expected_size, "candidate size:" + filename)
            fd = os.open(filename, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=self.dirfd)
            opened = os.fstat(fd)
            need(identity(opened) == identity(info), "candidate race:" + filename)
            first = hash_fd(fd)
            need(first == hash_fd(fd), "candidate digest stability:" + filename)
            if self.pinned:
                need(first == expected_sha, "candidate digest:" + filename)
            self.fds[filename] = fd
            self.identities[filename] = identity(opened)
        return self

    def read(self, filename: str) -> bytes:
        fd = self.fds[filename]
        os.lseek(fd, 0, os.SEEK_SET)
        blocks: list[bytes] = []
        while True:
            block = os.read(fd, 1_048_576)
            if not block:
                return b"".join(blocks)
            blocks.append(block)

    def gzip_lines(self, filename: str) -> Iterator[bytes]:
        duplicate = os.dup(self.fds[filename])
        os.lseek(duplicate, 0, os.SEEK_SET)
        with os.fdopen(duplicate, "rb", closefd=True) as source:
            with gzip.GzipFile(fileobj=source, mode="rb") as stream:
                for line in stream:
                    yield line

    def final(self) -> None:
        for filename in reversed(OUTPUT_ORDER):
            fd = self.fds[filename]
            need(identity(os.fstat(fd)) == self.identities[filename], "candidate final fd:" + filename)
            need(identity(os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)) == self.identities[filename], "candidate final path:" + filename)
            current = hash_fd(fd)
            need(current == hash_fd(fd), "candidate final digest stability:" + filename)
            if self.pinned:
                need(current == CANDIDATE_PINS[filename][1], "candidate final digest:" + filename)
        need(identity(os.fstat(self.dirfd)) == self.directory_identity, "candidate final directory fd")
        need(identity(os.stat(self.directory, follow_symlinks=False)) == self.directory_identity, "candidate final directory path")
        need(set(os.listdir(self.dirfd)) == set(OUTPUT_ORDER), "candidate final exact set")

    def __exit__(self, *_: Any) -> None:
        for fd in self.fds.values():
            try:
                os.close(fd)
            except OSError:
                pass
        if self.dirfd >= 0:
            os.close(self.dirfd)


class LedgerComparator:
    def __init__(self, candidate: CandidateFiles, filename: str, row_schema: str, row_id_field: str) -> None:
        self.candidate = candidate
        self.filename = filename
        self.row_schema = row_schema
        self.row_id_field = row_id_field
        self.iterator = iter(candidate.gzip_lines(filename))
        self.uncompressed_hash = hashlib.sha256()
        self.uncompressed_size = 0
        self.row_count = 0
        self.ids = SequenceHash()
        self.hashes = SequenceHash()
        self.rows = SequenceHash()

    def add(self, body: dict[str, Any]) -> tuple[str, str, str]:
        need(body.get("schema") == self.row_schema and "row_sha256" not in body, "expected row body:" + self.filename)
        row = {**body, "row_sha256": objsha(body)}
        raw = canonical(row)
        line = next(self.iterator, None)
        need(line == raw + b"\n", "candidate row comparator:" + self.filename + ":" + str(self.row_count))
        self.uncompressed_hash.update(line)
        self.uncompressed_size += len(line)
        self.ids.add(row[self.row_id_field])
        self.hashes.add(row["row_sha256"])
        self.rows.add_wire(raw)
        self.row_count += 1
        return row[self.row_id_field], row["row_sha256"], hashlib.sha256(raw).hexdigest()

    def close(self) -> dict[str, Any]:
        need(next(self.iterator, None) is None, "candidate extra row:" + self.filename)
        compressed_size, compressed_sha = CANDIDATE_PINS[self.filename]
        return {
            "filename": self.filename,
            "compression": "gzip-stream-level9-mtime-zero",
            "row_schema": self.row_schema,
            "row_count": self.row_count,
            "compressed_size": compressed_size,
            "compressed_sha256": compressed_sha,
            "uncompressed_size": self.uncompressed_size,
            "uncompressed_sha256": self.uncompressed_hash.hexdigest(),
            "ordered_row_ids_sha256": self.ids.finish(),
            "ordered_row_hashes_sha256": self.hashes.finish(),
            "ordered_rows_sha256": self.rows.finish(),
        }


def verify_json(candidate: CandidateFiles, filename: str, expected: dict[str, Any]) -> None:
    raw = candidate.read(filename)
    need(raw == canonical(expected), "candidate JSON comparator:" + filename)


def rebuild(candidate: CandidateFiles) -> dict[str, Any]:
    with Snapshot() as snapshot:
        c0_manifest = manifest_map(snapshot, "C0_MANIFEST")
        c5_manifest = manifest_map(snapshot, "C5_MANIFEST")
        by_role = {pin.role: pin for pin in PINS}
        for role in ("C0_RESULT", "C0_MEMBER", "C0_EDGE"):
            pin = by_role[role]
            need(c0_manifest.get(pin.filename) == pin.sha256, "C0 manifest binding:" + role)
        for role in ("C5_RESULT", "C5_LEDGER"):
            pin = by_role[role]
            need(c5_manifest.get(pin.filename) == pin.sha256, "C5 manifest binding:" + role)
        c0_result = direct(snapshot, "C0_RESULT")
        c5_result = direct(snapshot, "C5_RESULT")
        need(c0_result["corrected_member_and_root_universe"]["member_count"] == 564_460, "C0 member census")
        need(c0_result["corrected_member_and_root_universe"]["base_root_count"] == 367_948, "C0 root census")
        need(c0_result["fresh_forward_application"]["edge_application_count"] == 478_718, "C0 edge census")
        need(c0_result["fresh_forward_application"]["component_count"] == 92_672, "C0 component census")
        need(c5_result["semantic_effect"]["new_invalid_distinct_member_candidates"] == 66_688, "C5 invalid member census")
        need(c5_result["semantic_effect"]["projected_member_universe_before_fresh_DSU"] == 497_772, "C5 projected member census")

        invalid_sources: dict[str, dict[str, Any]] = {}
        classifications = Counter()
        c5_rows = 0
        for ordinal, line in enumerate(snapshot.gzip_lines("C5_LEDGER")):
            row, wire_sha = closed_row(line, "cm2.round306c5.source-g-corrected-g2-graph-semantic-classification.v1.row.v1", None, ordinal, "C5")
            semantic = row["semantic_classification"]
            classification = semantic["classification"]
            classifications[classification] += 1
            if classification == "EMPTY_GRAPH":
                for role, field in (("EMPTY_GRAPH_SHEET", "invalid_sheet_member_candidate"), ("EMPTY_GRAPH_SIDE", "invalid_side_member_candidate")):
                    member_id = semantic[field]
                    need(type(member_id) is str and member_id not in invalid_sources, "C5 duplicate invalid member")
                    invalid_sources[member_id] = {
                        "invalidation_role": role,
                        "C5_semantic_row": source_ref(ordinal, row, wire_sha, "semantic_row_id"),
                        "C5_graph_id": row["graph_id"],
                        "C5_graph_inventory_row_id": row["graph_inventory_row_id"],
                    }
            c5_rows += 1
        need(c5_rows == 38_608 and classifications == {"POSITIVE_GRAPH": 5_264, "EMPTY_GRAPH": 33_344}, "C5 classification replay")
        need(len(invalid_sources) == 66_688 and objsha(sorted(invalid_sources)) == "53f50ece8f99c36c72768348291816e3362a72e1155c18177e44071eae89ebf7", "C5 invalid set")

        root_members: dict[str, list[tuple[str, str]]] = defaultdict(list)
        root_metadata: dict[str, tuple[str, str]] = {}
        old_component_members = Counter()
        seen_members: set[str] = set()
        invalid_records: dict[str, dict[str, Any]] = {}
        member_count = 0
        for ordinal, line in enumerate(snapshot.gzip_lines("C0_MEMBER")):
            row, wire_sha = closed_row(line, "cm2.round306c0.source-g-r235d-corrected-fresh-freeze.v1.fresh-member-component-row.v1", None, ordinal, "C0 member")
            member_id = row["registry_member_id"]
            old_root = row["corrected_base_root_id"]
            old_component = row["corrected_component_id"]
            official_key = row["official_key_id"]
            need(row["member_identity_preserved"] is True and member_id not in seen_members, "C0 member semantics")
            seen_members.add(member_id)
            root_members[old_root].append((member_id, row["row_sha256"]))
            old_component_members[old_component] += 1
            observed = root_metadata.setdefault(old_root, (official_key, old_component))
            need(observed == (official_key, old_component), "C0 root metadata")
            if member_id in invalid_sources:
                invalid_records[member_id] = {
                    **invalid_sources[member_id],
                    "C0_member_row": source_ref(ordinal, row, wire_sha, "row_id"),
                    "old_base_root_id": old_root,
                    "old_component_id": old_component,
                    "official_key_id": official_key,
                }
            member_count += 1
        need(member_count == len(seen_members) == 564_460, "C0 member replay")
        need(len(root_members) == 367_948 and len(old_component_members) == 92_672, "C0 root/component replay")
        need(len(invalid_records) == len(invalid_sources) == 66_688, "invalid member join")
        for members in root_members.values():
            members.sort()

        invalid_by_root: dict[str, list[str]] = defaultdict(list)
        for member_id, record in invalid_records.items():
            invalid_by_root[record["old_base_root_id"]].append(member_id)
        for members in invalid_by_root.values():
            members.sort()
        new_root_by_old: dict[str, str | None] = {}
        disposition_by_old: dict[str, str] = {}
        retained_members_by_old: dict[str, list[str]] = {}
        root_inputs: dict[str, dict[str, Any]] = {}
        disposition_histogram = Counter()
        for old_root in sorted(root_members):
            members = [item[0] for item in root_members[old_root]]
            invalid = invalid_by_root.get(old_root, [])
            invalid_set = set(invalid)
            retained = [member for member in members if member not in invalid_set]
            if not invalid:
                disposition = "KEEP_ROOT"
                new_root: str | None = old_root
            elif not retained:
                disposition = "DELETE_ROOT"
                new_root = None
            else:
                disposition = "REKEY_ROOT"
                rekey_input = {
                    "schema": SCHEMA + ".rekey-input.v1",
                    "old_base_root_id": old_root,
                    "official_key_id": root_metadata[old_root][0],
                    "old_member_count": len(members),
                    "invalid_member_ids": invalid,
                    "invalid_member_count": len(invalid),
                    "retained_member_count": len(retained),
                    "retained_member_ids_sha256": objsha(retained),
                    "retained_source_row_hashes_sha256": objsha([row_sha for member, row_sha in root_members[old_root] if member not in invalid_set]),
                }
                root_inputs[old_root] = rekey_input
                new_root = NEW_ROOT_NAMESPACE + objsha(rekey_input)
            new_root_by_old[old_root] = new_root
            disposition_by_old[old_root] = disposition
            retained_members_by_old[old_root] = retained
            disposition_histogram[disposition] += 1
        need(len(invalid_by_root) == 42_196, "affected root census")
        need(disposition_histogram == {"KEEP_ROOT": 325_752, "DELETE_ROOT": 33_344, "REKEY_ROOT": 8_852}, "root disposition census")
        surviving_roots = sorted(root for root in new_root_by_old.values() if root is not None)
        need(len(surviving_roots) == len(set(surviving_roots)) == 334_604, "surviving root census")

        forward = DSU(surviving_roots)
        projected_pairs: list[tuple[str, str] | None] = []
        forward_flags: list[int | None] = []
        drop_channels = Counter()
        invalid_occurrence_hits = 0
        edge_count = 0
        for ordinal, line in enumerate(snapshot.gzip_lines("C0_EDGE")):
            row, _ = closed_row(line, "cm2.round306c0.source-g-r235d-corrected-fresh-freeze.v1.edge-remap-application-row.v1", "application_index", ordinal, "C0 edge")
            old_pair = row["corrected_projected_base_root_pair"]
            occurrence_pair = row["corrected_canonical_occurrence_endpoint_pair"]
            need(type(old_pair) is list and len(old_pair) == 2 and old_pair == sorted(old_pair), "C0 projected pair")
            invalid_occurrence_hits += sum(endpoint in invalid_sources for endpoint in occurrence_pair)
            mapped = [new_root_by_old[root] for root in old_pair]
            if any(root is None for root in mapped):
                projected_pairs.append(None)
                forward_flags.append(None)
                drop_channels[row["source_channel"]] += 1
            else:
                pair = tuple(sorted((mapped[0], mapped[1])))
                projected_pairs.append(pair)
                forward_flags.append(forward.union(*pair))
            edge_count += 1
        need(edge_count == 478_718 and invalid_occurrence_hits == 0, "edge input census")
        need(sum(pair is None for pair in projected_pairs) == 2_600, "dropped edge census")
        need(drop_channels == {"R300E_HALF_OPEN_OWNER": 2_600}, "dropped edge channel")
        reverse = DSU(surviving_roots)
        reverse_flags: list[int | None] = [None] * len(projected_pairs)
        for ordinal in range(len(projected_pairs) - 1, -1, -1):
            pair = projected_pairs[ordinal]
            if pair is not None:
                reverse_flags[ordinal] = reverse.union(*pair)
        forward_partition = forward.partition()
        need(forward_partition == reverse.partition(), "forward/reverse partition")
        need(forward.rank_reduction == reverse.rank_reduction == 272_676, "fresh rank reduction")
        need(len(forward_partition) == 61_928, "fresh component census")

        component_by_root: dict[str, str] = {}
        component_roots: dict[str, list[str]] = {}
        for roots in forward_partition:
            component_id = COMPONENT_NAMESPACE + objsha(roots)
            need(component_id not in component_roots, "component id collision")
            component_roots[component_id] = roots
            for root in roots:
                component_by_root[root] = component_id
        old_root_by_new = {new: old for old, new in new_root_by_old.items() if new is not None}
        retained_count_by_new = {new: len(retained_members_by_old[old]) for old, new in new_root_by_old.items() if new is not None}
        component_member_count = {component: sum(retained_count_by_new[root] for root in roots) for component, roots in component_roots.items()}
        component_sizes = sorted(component_member_count.values())
        total_members = sum(component_sizes)
        all_pairs = total_members * (total_members - 1) // 2
        within_pairs = sum(size * (size - 1) // 2 for size in component_sizes)
        cross_pairs = all_pairs - within_pairs
        need(total_members == 497_772 and cross_pairs == 123_410_984_634, "fresh member/pair denominator")

        ledgers: dict[str, dict[str, Any]] = {}
        invalid_comparator = LedgerComparator(candidate, INVALIDATION_NAME, INVALIDATION_SCHEMA, "row_id")
        for ordinal, member_id in enumerate(sorted(invalid_records)):
            record = invalid_records[member_id]
            body = {
                "schema": INVALIDATION_SCHEMA,
                "row_id": PREFIX + ":member-invalidation:" + objsha([member_id, record["invalidation_role"]]),
                "invalidation_ordinal": ordinal,
                "registry_member_id": member_id,
                **record,
                "formal_member_invalidation_credit_without_independent_verification": 0,
            }
            invalid_comparator.add(body)
        ledgers["member_invalidation"] = invalid_comparator.close()

        root_comparator = LedgerComparator(candidate, ROOT_NAME, ROOT_SCHEMA, "row_id")
        root_references: dict[str, list[Any]] = {}
        for ordinal, old_root in enumerate(sorted(root_members)):
            members = [item[0] for item in root_members[old_root]]
            invalid = invalid_by_root.get(old_root, [])
            retained = retained_members_by_old[old_root]
            disposition = disposition_by_old[old_root]
            body = {
                "schema": ROOT_SCHEMA,
                "row_id": PREFIX + ":base-root-disposition:" + objsha(old_root),
                "root_ordinal": ordinal,
                "old_base_root_id": old_root,
                "old_component_id": root_metadata[old_root][1],
                "official_key_id": root_metadata[old_root][0],
                "old_member_count": len(members),
                "invalid_member_count": len(invalid),
                "invalid_member_ids": invalid,
                "retained_member_count": len(retained),
                "retained_member_ids_sha256": objsha(retained),
                "disposition": disposition,
                "new_base_root_id": new_root_by_old[old_root],
                "rekey_input": root_inputs.get(old_root),
                "formal_root_disposition_credit_without_independent_verification": 0,
            }
            row_id, row_sha, wire_sha = root_comparator.add(body)
            root_references[old_root] = [ordinal, row_id, wire_sha, row_sha]
        ledgers["base_root_disposition"] = root_comparator.close()

        edge_comparator = LedgerComparator(candidate, EDGE_NAME, EDGE_SCHEMA, "row_id")
        for ordinal, line in enumerate(snapshot.gzip_lines("C0_EDGE")):
            row, wire_sha = closed_row(line, "cm2.round306c0.source-g-r235d-corrected-fresh-freeze.v1.edge-remap-application-row.v1", "application_index", ordinal, "C0 edge replay")
            pair = projected_pairs[ordinal]
            kept = pair is not None
            body = {
                "schema": EDGE_SCHEMA,
                "row_id": PREFIX + ":edge-application:" + objsha([ordinal, row["row_id"]]),
                "application_index": ordinal,
                "source_C0_edge_row": source_ref(ordinal, row, wire_sha, "row_id"),
                "source_channel": row["source_channel"],
                "source_row_id": row["source_row_id"],
                "old_projected_base_root_pair": row["corrected_projected_base_root_pair"],
                "new_projected_base_root_pair": list(pair) if pair is not None else None,
                "old_canonical_occurrence_endpoint_pair": row["corrected_canonical_occurrence_endpoint_pair"],
                "disposition": "KEEP_AND_APPLY" if kept else "DROP_INVALIDATED_BASE_ROOT",
                "fed_to_new_empty_DSU": kept,
                "forward_rank_reduction": forward_flags[ordinal],
                "reverse_rank_reduction": reverse_flags[ordinal],
                "formal_edge_application_credit_without_independent_verification": 0,
            }
            edge_comparator.add(body)
        ledgers["edge_application"] = edge_comparator.close()

        member_comparator = LedgerComparator(candidate, MEMBER_NAME, MEMBER_SCHEMA, "row_id")
        output_member_ordinal = 0
        for source_ordinal, line in enumerate(snapshot.gzip_lines("C0_MEMBER")):
            row, wire_sha = closed_row(line, "cm2.round306c0.source-g-r235d-corrected-fresh-freeze.v1.fresh-member-component-row.v1", None, source_ordinal, "C0 member replay")
            member_id = row["registry_member_id"]
            if member_id in invalid_sources:
                continue
            old_root = row["corrected_base_root_id"]
            new_root = new_root_by_old[old_root]
            need(new_root is not None, "retained member under deleted root")
            body = {
                "schema": MEMBER_SCHEMA,
                "row_id": PREFIX + ":member-component:" + objsha(member_id),
                "member_ordinal": output_member_ordinal,
                "registry_member_id": member_id,
                "source_C0_member_row": source_ref(source_ordinal, row, wire_sha, "row_id"),
                "source_C6_root_disposition_row": root_references[old_root],
                "old_base_root_id": old_root,
                "new_base_root_id": new_root,
                "fresh_component_id": component_by_root[new_root],
                "official_key_id": row["official_key_id"],
                "member_identity_preserved": True,
                "formal_member_universe_or_DSU_credit_without_independent_verification": 0,
            }
            member_comparator.add(body)
            output_member_ordinal += 1
        need(output_member_ordinal == 497_772, "output member census")
        ledgers["member_component"] = member_comparator.close()

        root_component_comparator = LedgerComparator(candidate, ROOT_COMPONENT_NAME, ROOT_COMPONENT_SCHEMA, "row_id")
        for ordinal, new_root in enumerate(sorted(component_by_root)):
            old_root = old_root_by_new[new_root]
            body = {
                "schema": ROOT_COMPONENT_SCHEMA,
                "row_id": PREFIX + ":base-root-component:" + objsha(new_root),
                "base_root_ordinal": ordinal,
                "source_C6_root_disposition_row": root_references[old_root],
                "old_base_root_id": old_root,
                "new_base_root_id": new_root,
                "fresh_component_id": component_by_root[new_root],
                "retained_member_count": retained_count_by_new[new_root],
                "formal_DSU_credit_without_independent_verification": 0,
            }
            root_component_comparator.add(body)
        ledgers["base_root_component"] = root_component_comparator.close()

        component_comparator = LedgerComparator(candidate, COMPONENT_NAME, COMPONENT_SCHEMA, "row_id")
        for ordinal, component_id in enumerate(sorted(component_roots)):
            roots = component_roots[component_id]
            old_components = sorted({root_metadata[old_root_by_new[root]][1] for root in roots})
            body = {
                "schema": COMPONENT_SCHEMA,
                "row_id": PREFIX + ":component-census:" + objsha(component_id),
                "component_ordinal": ordinal,
                "fresh_component_id": component_id,
                "base_root_count": len(roots),
                "base_root_ids_sha256": objsha(roots),
                "member_count": component_member_count[component_id],
                "source_C0_component_count": len(old_components),
                "source_C0_component_ids_sha256": objsha(old_components),
                "formal_DSU_credit_without_independent_verification": 0,
            }
            component_comparator.add(body)
        ledgers["component_census"] = component_comparator.close()

        cross_body = {
            "schema": SCHEMA + ".cross-component-pair-denominator.v1",
            "member_count": total_members,
            "component_count": len(component_roots),
            "component_member_size_vector_sha256": objsha(component_sizes),
            "all_unordered_member_pairs": all_pairs,
            "within_component_unordered_member_pairs": within_pairs,
            "cross_component_pair_denominator": cross_pairs,
        }
        cross = {**cross_body, "cross_denominator_sha256": objsha(cross_body)}
        verify_json(candidate, CROSS_NAME, cross)
        cross_file = {"filename": CROSS_NAME, "size": CANDIDATE_PINS[CROSS_NAME][0], "sha256": CANDIDATE_PINS[CROSS_NAME][1]}

        result_body = {
            "schema": SCHEMA,
            "status": "PASS_66688_G2_MEMBER_INVALIDATIONS__476118_RETAINED_EDGES__61928_FRESH_COMPONENTS__ZERO_CREDIT_PENDING_INDEPENDENT_VERIFICATION",
            "source_pins": [pin.__dict__ for pin in PINS],
            "upstream_seal_bindings": {"C0_manifest_sha256": by_role["C0_MANIFEST"].sha256, "C5_manifest_sha256": by_role["C5_MANIFEST"].sha256},
            "member_invalidation_census": {
                "invalid_sheet_members": 33_344,
                "invalid_side_members": 33_344,
                "invalid_distinct_members": 66_688,
                "invalid_member_ids_sha256": objsha(sorted(invalid_sources)),
                "affected_old_base_roots": len(invalid_by_root),
                "affected_old_components": len({record["old_component_id"] for record in invalid_records.values()}),
            },
            "root_disposition_census": dict(sorted(disposition_histogram.items())),
            "edge_application_census": {
                "source_edges": 478_718,
                "retained_edges": 476_118,
                "dropped_edges": 2_600,
                "dropped_edge_source_channels": dict(sorted(drop_channels.items())),
                "invalid_occurrence_endpoint_hits": invalid_occurrence_hits,
                "forward_rank_reduction": forward.rank_reduction,
                "reverse_rank_reduction": reverse.rank_reduction,
            },
            "fresh_freeze_census": {
                "members": total_members,
                "base_roots": len(surviving_roots),
                "components": len(component_roots),
                "partition_sha256": objsha(forward_partition),
                "component_member_size_vector_sha256": objsha(component_sizes),
                "cross_component_pair_denominator": cross_pairs,
            },
            "output_ledgers": ledgers,
            "cross_component_pair_denominator_file": cross_file,
            "publication_order_before_result": list(OUTPUT_ORDER[:-1]),
            "result_committed_last_without_clobber": True,
            "required_next": {
                "independent_full_replay": True,
                "coherent_attacks": True,
                "cold_replay": True,
                "manifest_first_no_write": True,
                "replay_C1_C2_C3_C4_C5_on_fresh_freeze": True,
                "normalized_support": "NOT_AUTHORIZED",
                "B1A": "NOT_AUTHORIZED",
                "B2": "NOT_AUTHORIZED",
            },
            "formal_credit_without_independent_verification": {"fresh_member_universe": 0, "fresh_DSU": 0, "normalized_support": 0, "B1A": 0, "B2": 0, "maximality": 0, "CM2": 0},
            "CM2": "NO-GO_FOR_CLAIM",
        }
        result = {**result_body, "result_sha256": objsha(result_body)}
        verify_json(candidate, RESULT_NAME, result)
        snapshot.final()
    return {
        "status": "PASS_INDEPENDENT_66688_INVALIDATIONS__476118_EDGES__61928_FRESH_COMPONENTS_REPLAY",
        "candidate_result_file_sha256": CANDIDATE_PINS[RESULT_NAME][1],
        "result_sha256": result["result_sha256"],
        "invalid_member_count": 66_688,
        "fresh_member_count": total_members,
        "fresh_base_root_count": len(surviving_roots),
        "fresh_component_count": len(component_roots),
        "retained_edge_count": 476_118,
        "cross_component_pair_denominator": cross_pairs,
        "producer_imported_or_executed_or_parsed": False,
        "formal_credit": {"fresh_member_universe": 1, "fresh_DSU": 1, "normalized_support": 0, "B1A": 0, "B2": 0, "maximality": 0, "CM2": 0},
        "CM2": "NO-GO_FOR_CLAIM",
    }


def publish_from_fd(candidate: CandidateFiles, filename: str) -> None:
    output = ROOT / filename
    need(not output.exists(), "publish no-clobber:" + filename)
    destination = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC, 0o600)
    source = candidate.fds[filename]
    try:
        os.lseek(source, 0, os.SEEK_SET)
        while True:
            block = os.read(source, 1_048_576)
            if not block:
                break
            offset = 0
            while offset < len(block):
                offset += os.write(destination, block[offset:])
        os.fsync(destination)
    finally:
        os.close(destination)
    info = os.stat(output, follow_symlinks=False)
    expected_size, expected_sha = CANDIDATE_PINS[filename]
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and info.st_size == expected_size, "published identity:" + filename)
    fd = os.open(output, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        need(hash_fd(fd) == expected_sha, "published digest:" + filename)
    finally:
        os.close(fd)


def replay(directory: Path, promote: bool = False, pinned: bool = True) -> dict[str, Any]:
    with CandidateFiles(directory, pinned=pinned) as candidate:
        receipt = rebuild(candidate)
        if promote:
            for filename in OUTPUT_ORDER:
                publish_from_fd(candidate, filename)
        candidate.final()
    if promote:
        for filename in reversed(OUTPUT_ORDER):
            info = os.stat(ROOT / filename, follow_symlinks=False)
            fd = os.open(ROOT / filename, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
            try:
                need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and identity(os.fstat(fd)) == identity(info), "reverse promoted identity:" + filename)
                need(hash_fd(fd) == CANDIDATE_PINS[filename][1], "reverse promoted digest:" + filename)
            finally:
                os.close(fd)
        receipt = {**receipt, "status": "PASS_CANDIDATE_PROMOTED_SEVEN_PAYLOADS_FIRST_RESULT_LAST_WITH_REVERSE_IDENTITY_NLINK_SHA256_VERIFICATION"}
    return receipt


def verifier_sha256() -> str:
    path = Path(__file__)
    before = os.stat(path, follow_symlinks=False)
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "verifier identity")
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        need(identity(os.fstat(fd)) == identity(before), "verifier race")
        value = hash_fd(fd)
        need(value == hash_fd(fd), "verifier digest stability")
        return value
    finally:
        os.close(fd)


def publish_bytes(filename: str, raw: bytes) -> None:
    path = ROOT / filename
    need(not path.exists(), "publish no-clobber:" + filename)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC, 0o600)
    try:
        offset = 0
        while offset < len(raw):
            offset += os.write(fd, raw[offset:])
        os.fsync(fd)
    finally:
        os.close(fd)
    info = os.stat(path, follow_symlinks=False)
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and info.st_size == len(raw), "published identity:" + filename)


def mutate_result(path: Path, mutation: Any) -> None:
    value = json.loads(path.read_bytes())
    mutation(value)
    body = dict(value)
    body.pop("result_sha256", None)
    path.write_bytes(canonical({**body, "result_sha256": objsha(body)}))


def mutate_cross(path: Path, mutation: Any) -> None:
    value = json.loads(path.read_bytes())
    mutation(value)
    body = dict(value)
    body.pop("cross_denominator_sha256", None)
    path.write_bytes(canonical({**body, "cross_denominator_sha256": objsha(body)}))


def mutate_first_invalidation_row(directory: Path) -> None:
    path = directory / INVALIDATION_NAME
    plain = gzip.decompress(path.read_bytes())
    lines = plain.splitlines()
    need(len(lines) == 66_688, "attack invalidation row census")
    row = json.loads(lines[0])
    row["formal_member_invalidation_credit_without_independent_verification"] = 1
    body = dict(row)
    body.pop("row_sha256", None)
    lines[0] = canonical({**body, "row_sha256": objsha(body)})
    path.write_bytes(gzip.compress(b"\n".join(lines) + b"\n", compresslevel=9, mtime=0))


def coherent_attacks(candidate_directory: Path) -> dict[str, Any]:
    baseline = replay(candidate_directory)
    work = Path(tempfile.mkdtemp(prefix="cm2-c6-fresh-dsu-attacks-"))
    attacks: list[dict[str, Any]] = []

    def restore() -> None:
        for path in work.iterdir():
            if path.is_dir() and not path.is_symlink():
                shutil.rmtree(path)
            else:
                path.unlink()
        for filename in OUTPUT_ORDER:
            shutil.copyfile(candidate_directory / filename, work / filename)

    def execute(attack_id: str, mutation: Any, semantic: bool = False, cleanup: Any | None = None) -> None:
        restore()
        rejection = None
        try:
            mutation()
            replay(work, pinned=not semantic)
        except (Blocked, OSError, EOFError, json.JSONDecodeError, KeyError, ValueError) as error:
            rejection = type(error).__name__ + ":" + str(error)
        finally:
            if cleanup is not None:
                cleanup()
        need(rejection is not None, "attack accepted:" + attack_id)
        body = {"attack_id": attack_id, "rejected": True, "rejection_boundary": rejection}
        attacks.append({**body, "row_sha256": objsha(body)})

    try:
        execute("A01_EXTRA_FILE", lambda: (work / "foreign").write_bytes(b"x"))
        execute("A02_MISSING_RESULT", lambda: (work / RESULT_NAME).unlink())
        execute("A03_MISSING_MEMBER_LEDGER", lambda: (work / MEMBER_NAME).unlink())
        execute("A04_SYMLINK_RESULT", lambda: ((work / RESULT_NAME).unlink(), (work / RESULT_NAME).symlink_to(candidate_directory / RESULT_NAME)))
        hard_target = work.parent / (work.name + "-hard-target")

        def hardlink_edge() -> None:
            (work / EDGE_NAME).unlink()
            shutil.copyfile(candidate_directory / EDGE_NAME, hard_target)
            os.link(hard_target, work / EDGE_NAME)

        execute("A05_HARDLINK_EDGE_LEDGER", hardlink_edge, cleanup=lambda: hard_target.unlink(missing_ok=True))
        execute("A06_MEMBER_COUNT", lambda: mutate_result(work / RESULT_NAME, lambda value: value["fresh_freeze_census"].__setitem__("members", 497_773)))
        execute("A07_COMPONENT_COUNT", lambda: mutate_result(work / RESULT_NAME, lambda value: value["fresh_freeze_census"].__setitem__("components", 61_929)))
        execute("A08_CROSS_DENOMINATOR", lambda: mutate_result(work / RESULT_NAME, lambda value: value["fresh_freeze_census"].__setitem__("cross_component_pair_denominator", 123_410_984_633)))
        execute("A09_FRESH_DSU_CREDIT", lambda: mutate_result(work / RESULT_NAME, lambda value: value["formal_credit_without_independent_verification"].__setitem__("fresh_DSU", 1)))
        execute("A10_CROSS_FILE_REWRITE", lambda: mutate_cross(work / CROSS_NAME, lambda value: value.__setitem__("component_count", 61_929)))
        execute("A11_TRUNCATE_INVALIDATION", lambda: (work / INVALIDATION_NAME).write_bytes((work / INVALIDATION_NAME).read_bytes()[:-1]))

        def corrupt_edge() -> None:
            raw = bytearray((work / EDGE_NAME).read_bytes())
            raw[len(raw) // 2] ^= 1
            (work / EDGE_NAME).write_bytes(raw)

        execute("A12_CORRUPT_EDGE_LEDGER", corrupt_edge)
        execute("A13_LEDGER_SUBSTITUTION", lambda: (work / COMPONENT_NAME).write_bytes((work / ROOT_COMPONENT_NAME).read_bytes()))
        execute("A14_NONCANONICAL_RESULT", lambda: (work / RESULT_NAME).write_bytes((work / RESULT_NAME).read_bytes() + b"\n"))
        execute("A15_RESULT_SUBSTITUTION", lambda: (work / RESULT_NAME).write_bytes((work / CROSS_NAME).read_bytes()))
        execute("A16_RECLOSED_INVALIDATION_ROW", lambda: mutate_first_invalidation_row(work), semantic=True)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    need(len(attacks) == 16, "attack census")
    body = {
        "schema": SCHEMA + ".coherent-attack-suite.v1",
        "status": "PASS_16_OF_16_COHERENT_ATTACKS_REJECTED",
        "verifier_filename": VERIFIER_NAME,
        "verifier_file_sha256": verifier_sha256(),
        "attack_count": 16,
        "rejected_count": 16,
        "all_rejected": True,
        "baseline_result_file_sha256": baseline["candidate_result_file_sha256"],
        "attacks": attacks,
    }
    return {**body, "attack_suite_sha256": objsha(body)}


def closed_json(raw: bytes, closure: str, label: str) -> dict[str, Any]:
    value = json.loads(raw)
    need(type(value) is dict and canonical(value) == raw, "closed JSON canonical:" + label)
    body = dict(value)
    need(body.pop(closure, None) == objsha(body), "closed JSON closure:" + label)
    return value


def verification_document(receipt: dict[str, Any], attack_raw: bytes | None = None) -> dict[str, Any]:
    raw = (ROOT / ATTACK_NAME).read_bytes() if attack_raw is None else attack_raw
    suite = closed_json(raw, "attack_suite_sha256", "attack suite")
    need(suite["verifier_file_sha256"] == verifier_sha256(), "attack verifier binding")
    need((suite["attack_count"], suite["rejected_count"], suite["all_rejected"]) == (16, 16, True), "attack suite census")
    body = {
        "schema": SCHEMA + ".verification.v1",
        **receipt,
        "attack_suite": {
            "filename": ATTACK_NAME,
            "file_sha256": hashlib.sha256(raw).hexdigest(),
            "object_self_sha256": suite["attack_suite_sha256"],
            "attack_count": 16,
            "rejected_count": 16,
            "all_rejected": True,
        },
        "formal_credit_marker": {"fresh_member_universe": 1, "fresh_DSU": 1, "normalized_support": 0, "B1A": 0, "B2": 0, "maximality": 0, "CM2": 0},
    }
    return {**body, "verification_sha256": objsha(body)}


class ManifestPackage:
    def __init__(self) -> None:
        self.dirfd = -1
        self.manifest_fd = -1
        self.manifest_identity: tuple[int, ...] = ()
        self.fds: dict[str, int] = {}
        self.identities: dict[str, tuple[int, ...]] = {}
        self.hashes: dict[str, str] = {}

    def __enter__(self) -> "ManifestPackage":
        self.dirfd = os.open(ROOT, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
        before = os.stat(MANIFEST_NAME, dir_fd=self.dirfd, follow_symlinks=False)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "manifest identity")
        self.manifest_fd = os.open(MANIFEST_NAME, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=self.dirfd)
        opened = os.fstat(self.manifest_fd)
        need(identity(opened) == identity(before), "manifest race")
        self.manifest_identity = identity(opened)
        os.lseek(self.manifest_fd, 0, os.SEEK_SET)
        raw = os.read(self.manifest_fd, before.st_size)
        lines = raw.decode("ascii").splitlines()
        need(raw.endswith(b"\n") and len(lines) == len(PACKAGE_MEMBERS), "manifest structure")
        for line, filename in zip(lines, PACKAGE_MEMBERS, strict=True):
            declared_hash, declared_name = line.split("  ")
            need(declared_name == filename and len(declared_hash) == 64, "manifest order:" + filename)
            info = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
            need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "manifest member identity:" + filename)
            if filename in CANDIDATE_PINS:
                expected_size, expected_sha = CANDIDATE_PINS[filename]
                need(info.st_size == expected_size and declared_hash == expected_sha, "manifest payload pin:" + filename)
            fd = os.open(filename, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=self.dirfd)
            member = os.fstat(fd)
            need(identity(member) == identity(info) and hash_fd(fd) == hash_fd(fd) == declared_hash, "manifest member digest:" + filename)
            self.fds[filename] = fd
            self.identities[filename] = identity(member)
            self.hashes[filename] = declared_hash
        return self

    def read(self, filename: str) -> bytes:
        fd = self.fds[filename]
        os.lseek(fd, 0, os.SEEK_SET)
        blocks: list[bytes] = []
        while True:
            block = os.read(fd, 1_048_576)
            if not block:
                return b"".join(blocks)
            blocks.append(block)

    def gzip_lines(self, filename: str) -> Iterator[bytes]:
        duplicate = os.dup(self.fds[filename])
        os.lseek(duplicate, 0, os.SEEK_SET)
        with os.fdopen(duplicate, "rb", closefd=True) as source:
            with gzip.GzipFile(fileobj=source, mode="rb") as stream:
                for line in stream:
                    yield line

    def final(self) -> None:
        for filename in reversed(PACKAGE_MEMBERS):
            need(identity(os.fstat(self.fds[filename])) == self.identities[filename], "manifest final fd:" + filename)
            need(identity(os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)) == self.identities[filename], "manifest final path:" + filename)
            need(hash_fd(self.fds[filename]) == self.hashes[filename], "manifest final digest:" + filename)
        need(identity(os.fstat(self.manifest_fd)) == self.manifest_identity, "manifest final fd")
        need(identity(os.stat(MANIFEST_NAME, dir_fd=self.dirfd, follow_symlinks=False)) == self.manifest_identity, "manifest final path")

    def __exit__(self, *_: Any) -> None:
        for fd in self.fds.values():
            try:
                os.close(fd)
            except OSError:
                pass
        if self.manifest_fd >= 0:
            os.close(self.manifest_fd)
        if self.dirfd >= 0:
            os.close(self.dirfd)


def manifest_first_replay() -> dict[str, Any]:
    with ManifestPackage() as package:
        need(package.hashes[VERIFIER_NAME] == verifier_sha256(), "manifest verifier binding")
        receipt = rebuild(package)
        need(package.read(VERIFICATION_NAME) == canonical(verification_document(receipt, package.read(ATTACK_NAME))), "manifest verification byte identity")
        package.final()
    return {
        "status": "PASS_MANIFEST_FIRST_HELD_FD_66688_INVALIDATIONS__476118_EDGES__61928_COMPONENTS_REPLAY__ZERO_WRITES",
        "manifest_filename": MANIFEST_NAME,
        "manifest_member_count": len(PACKAGE_MEMBERS),
        "result_sha256": receipt["result_sha256"],
        "fresh_member_count": 497_772,
        "fresh_component_count": 61_928,
        "deliverables_write_syscalls": 0,
        "CM2": "NO-GO_FOR_CLAIM",
    }


def main() -> int:
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "python -I -B")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-dir")
    parser.add_argument("--verify-no-write", action="store_true")
    parser.add_argument("--promote", action="store_true")
    parser.add_argument("--attack-publish", action="store_true")
    parser.add_argument("--verify-publish", action="store_true")
    parser.add_argument("--manifest-first-no-write", action="store_true")
    args = parser.parse_args()
    need(sum((args.verify_no_write, args.promote, args.attack_publish, args.verify_publish, args.manifest_first_no_write)) == 1, "exactly one mode")
    if args.manifest_first_no_write:
        result = manifest_first_replay()
    else:
        need(args.candidate_dir is not None, "candidate required")
        candidate_directory = Path(args.candidate_dir)
        if args.promote:
            result = replay(candidate_directory, promote=True)
        elif args.attack_publish:
            suite = coherent_attacks(candidate_directory)
            publish_bytes(ATTACK_NAME, canonical(suite))
            result = {"status": suite["status"], "attack_count": 16, "attack_suite_sha256": suite["attack_suite_sha256"]}
        else:
            result = replay(candidate_directory)
            if args.verify_publish:
                publish_bytes(VERIFICATION_NAME, canonical(verification_document(result)))
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
