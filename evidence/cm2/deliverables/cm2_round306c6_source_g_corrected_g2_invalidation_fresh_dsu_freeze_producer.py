#!/usr/bin/env python3
"""Rebuild the corrected Source-G member universe and DSU after the C5 G2 invalidations."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
import gzip
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
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
        for pin in PINS:
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
        for pin in reversed(PINS):
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


class CandidatePublisher:
    def __init__(self, directory: Path) -> None:
        self.directory = Path(os.path.abspath(directory))
        self.parent_fd = -1
        self.dirfd = -1

    def __enter__(self) -> "CandidatePublisher":
        resolved_parent = self.directory.parent.resolve()
        need(os.path.commonpath((str(resolved_parent), str(ROOT.resolve()))) != str(ROOT.resolve()), "candidate outside deliverables")
        parent_info = os.stat(self.directory.parent, follow_symlinks=False)
        need(stat.S_ISDIR(parent_info.st_mode), "candidate parent")
        self.parent_fd = os.open(self.directory.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
        need(identity(os.fstat(self.parent_fd)) == identity(parent_info), "candidate parent race")
        os.mkdir(self.directory.name, 0o700, dir_fd=self.parent_fd)
        self.dirfd = os.open(self.directory.name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=self.parent_fd)
        need(not os.listdir(self.dirfd), "candidate starts empty")
        return self

    def open_output(self, filename: str) -> int:
        return os.open(filename, os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC, 0o600, dir_fd=self.dirfd)

    def publish_json(self, filename: str, value: dict[str, Any]) -> dict[str, Any]:
        raw = canonical(value)
        fd = self.open_output(filename)
        try:
            offset = 0
            while offset < len(raw):
                offset += os.write(fd, raw[offset:])
            os.fsync(fd)
            info = os.fstat(fd)
            need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and info.st_size == len(raw), "published JSON identity:" + filename)
            digest = hash_fd(fd)
        finally:
            os.close(fd)
        return {"filename": filename, "size": len(raw), "sha256": digest}

    def final(self) -> None:
        need(set(os.listdir(self.dirfd)) == set(OUTPUT_ORDER), "candidate exact output set")
        for filename in reversed(OUTPUT_ORDER):
            info = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
            need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "candidate final identity:" + filename)
            fd = os.open(filename, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=self.dirfd)
            try:
                opened = os.fstat(fd)
                need(identity(opened) == identity(info) and hash_fd(fd) == hash_fd(fd), "candidate final digest:" + filename)
            finally:
                os.close(fd)

    def __exit__(self, *_: Any) -> None:
        if self.dirfd >= 0:
            os.close(self.dirfd)
        if self.parent_fd >= 0:
            os.close(self.parent_fd)


class LedgerWriter:
    def __init__(self, publisher: CandidatePublisher, filename: str, row_schema: str, row_id_field: str) -> None:
        self.publisher = publisher
        self.filename = filename
        self.row_schema = row_schema
        self.row_id_field = row_id_field
        self.fd = publisher.open_output(filename)
        self.raw_file = os.fdopen(os.dup(self.fd), "wb", closefd=True)
        self.gzip_file = gzip.GzipFile(filename="", mode="wb", compresslevel=9, fileobj=self.raw_file, mtime=0)
        self.uncompressed_hash = hashlib.sha256()
        self.uncompressed_size = 0
        self.row_count = 0
        self.ids = SequenceHash()
        self.hashes = SequenceHash()
        self.rows = SequenceHash()

    def add(self, body: dict[str, Any]) -> tuple[str, str, str]:
        need(body.get("schema") == self.row_schema and "row_sha256" not in body, "output row body:" + self.filename)
        row = {**body, "row_sha256": objsha(body)}
        raw = canonical(row)
        line = raw + b"\n"
        self.gzip_file.write(line)
        self.uncompressed_hash.update(line)
        self.uncompressed_size += len(line)
        self.ids.add(row[self.row_id_field])
        self.hashes.add(row["row_sha256"])
        self.rows.add_wire(raw)
        self.row_count += 1
        return row[self.row_id_field], row["row_sha256"], hashlib.sha256(raw).hexdigest()

    def close(self) -> dict[str, Any]:
        self.gzip_file.close()
        self.raw_file.close()
        os.fsync(self.fd)
        info = os.fstat(self.fd)
        need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "output ledger identity:" + self.filename)
        compressed_sha = hash_fd(self.fd)
        os.close(self.fd)
        return {
            "filename": self.filename,
            "compression": "gzip-stream-level9-mtime-zero",
            "row_schema": self.row_schema,
            "row_count": self.row_count,
            "compressed_size": info.st_size,
            "compressed_sha256": compressed_sha,
            "uncompressed_size": self.uncompressed_size,
            "uncompressed_sha256": self.uncompressed_hash.hexdigest(),
            "ordered_row_ids_sha256": self.ids.finish(),
            "ordered_row_hashes_sha256": self.hashes.finish(),
            "ordered_rows_sha256": self.rows.finish(),
        }


def source_ref(ordinal: int, row: dict[str, Any], wire_sha: str, row_id_field: str) -> list[Any]:
    return [ordinal, row[row_id_field], wire_sha, row["row_sha256"]]


def produce(candidate_directory: Path) -> dict[str, Any]:
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
        need(len(invalid_sources) == 66_688, "C5 invalid set")

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
        need(member_count == 564_460 and len(seen_members) == 564_460, "C0 member replay")
        need(len(root_members) == 367_948 and len(old_component_members) == 92_672, "C0 root/component replay")
        need(len(invalid_records) == len(invalid_sources) == 66_688, "invalid member join")
        need(objsha(sorted(invalid_sources)) == "53f50ece8f99c36c72768348291816e3362a72e1155c18177e44071eae89ebf7", "invalid member commitment")
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
        reverse_partition = reverse.partition()
        need(forward_partition == reverse_partition, "forward/reverse partition")
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

        with CandidatePublisher(candidate_directory) as publisher:
            ledgers: dict[str, dict[str, Any]] = {}
            invalid_writer = LedgerWriter(publisher, INVALIDATION_NAME, INVALIDATION_SCHEMA, "row_id")
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
                invalid_writer.add(body)
            ledgers["member_invalidation"] = invalid_writer.close()

            root_writer = LedgerWriter(publisher, ROOT_NAME, ROOT_SCHEMA, "row_id")
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
                row_id, row_sha, wire_sha = root_writer.add(body)
                root_references[old_root] = [ordinal, row_id, wire_sha, row_sha]
            ledgers["base_root_disposition"] = root_writer.close()

            edge_writer = LedgerWriter(publisher, EDGE_NAME, EDGE_SCHEMA, "row_id")
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
                edge_writer.add(body)
            ledgers["edge_application"] = edge_writer.close()

            member_writer = LedgerWriter(publisher, MEMBER_NAME, MEMBER_SCHEMA, "row_id")
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
                member_writer.add(body)
                output_member_ordinal += 1
            need(output_member_ordinal == 497_772, "output member census")
            ledgers["member_component"] = member_writer.close()

            root_component_writer = LedgerWriter(publisher, ROOT_COMPONENT_NAME, ROOT_COMPONENT_SCHEMA, "row_id")
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
                root_component_writer.add(body)
            ledgers["base_root_component"] = root_component_writer.close()

            component_writer = LedgerWriter(publisher, COMPONENT_NAME, COMPONENT_SCHEMA, "row_id")
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
                component_writer.add(body)
            ledgers["component_census"] = component_writer.close()

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
            cross_file = publisher.publish_json(CROSS_NAME, cross)

            source_pins = [pin.__dict__ for pin in PINS]
            result_body = {
                "schema": SCHEMA,
                "status": "PASS_66688_G2_MEMBER_INVALIDATIONS__476118_RETAINED_EDGES__61928_FRESH_COMPONENTS__ZERO_CREDIT_PENDING_INDEPENDENT_VERIFICATION",
                "source_pins": source_pins,
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
            result_file = publisher.publish_json(RESULT_NAME, result)
            publisher.final()
        snapshot.final()
    return {
        "status": result["status"],
        "result_filename": RESULT_NAME,
        "result_size": result_file["size"],
        "result_file_sha256": result_file["sha256"],
        "result_sha256": result["result_sha256"],
        "invalid_member_count": 66_688,
        "fresh_member_count": total_members,
        "fresh_base_root_count": len(surviving_roots),
        "fresh_component_count": len(component_roots),
        "retained_edge_count": 476_118,
        "cross_component_pair_denominator": cross_pairs,
    }


def main() -> int:
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "python -I -B")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-dir", required=True)
    args = parser.parse_args()
    result = produce(Path(args.candidate_dir))
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
