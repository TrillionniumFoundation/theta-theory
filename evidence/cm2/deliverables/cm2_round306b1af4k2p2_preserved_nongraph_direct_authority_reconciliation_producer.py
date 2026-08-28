#!/usr/bin/env python3
"""Round306B1AF4K2P2 preserved/non-graph direct-authority reconciliation.

This producer is deliberately a zero-theorem-credit reconciliation.  It
joins sealed mechanical identity rows to sealed narrow local-authority
receipts, and keeps three notions separate:

* a receipt can be attached to a member/representation/obligation;
* a receipt can carry a narrow local authority for a row or owner;
* neither fact proves normalized full support, representation equality or
  pullback, A1/A2, B1A, B2, or CM2.

No upstream Python module is imported or executed.  Every consumed byte is
held through one directory descriptor and held file descriptors, hashed
twice before parsing and once after all parsing, with final path/FD identity
revalidation.  Temporary output is rooted explicitly at /tmp and never
consults TMPDIR.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass, field
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import stat
import tempfile
from typing import Any, Final, Iterable, Iterator
import zlib


class ReconciliationError(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise ReconciliationError(label)


SCHEMA: Final = (
    "cm2.round306b1af4k2p2.preserved-nongraph-direct-authority-"
    "reconciliation.v1"
)
INPUT_DIRECTORY: Final = Path(__file__).parent
ROW_CAP: Final = 8_388_608
IO_CHUNK: Final = 1 << 20
TMP_ROOT: Final = "/tmp"
ZERO_CREDIT: Final = {
    "normalized_full_support": 0,
    "representation_set_equality": 0,
    "representation_pullback": 0,
    "A1_A2": 0,
    "B1A": 0,
    "B2": 0,
    "maximality": 0,
    "fibre": 0,
    "global_disposition": 0,
    "D02": 0,
    "D03": 0,
    "D04": 0,
    "Gate5": 0,
    "CM2": 0,
}


@dataclass(frozen=True)
class Pin:
    label: str
    filename: str
    exact_size: int
    sha256: str
    role: str


# The exact table is inserted only after I4 and R235D both report FINAL
# SEALED.  Production is impossible while this tuple is empty.
PINS: Final[tuple[Pin, ...]] = ()
FINAL_PIN_GATE: Final = (
    "PENDING_R235D_TARGET_ZERO_SET_AND_FRESH_FREEZE_DECISION__"
    "I4_53B84967_NOT_AUTHORIZED_AS_FORMAL_PIN__NO_PRODUCTION_AUTHORIZED"
)
OLD_FREEZE_INVALIDATION_AUDIT: Final = {
    "status": "CONFIRMED_OLD_B0_I2_I4_INVALIDATED__FRESH_FREEZE_REQUIRED",
    "R235D_target_zero_set_empty_rows": 16,
    "old_B1G0_R236_source_graph_rows": 16,
    "old_B1G0_R236_target_graph_rows": 16,
    "invalid_target_sheet_member_count": 16,
    "invalid_target_sheet_member_ids_sha256": "0163d9c564b74b8cff5a9d5f309a25037d461b3874ca4805161cf639aeec73f4",
    "invalid_target_only_side_member_count": 16,
    "invalid_target_only_side_member_ids_sha256": "f6f5acf3a89bb0a09f83b7f0ac783019fddc5b36ca7d8df833d6c052cc20e957",
    "invalid_old_B0_member_count": 32,
    "invalid_old_B0_member_ids_sha256": "9c95eae730d5a033d65dadf2d27828b9876325e943049dd788ac1ed740687e52",
    "old_B0_backbinding_row_count": 32,
    "old_B0_source_row_ids_sha256": "d21beb9e651d1d8d4903e304c8c458c2b9d47fe1c026661b33a743567f2d5a0b",
    "affected_old_Round306A_component_count": 20,
    "affected_old_Round306A_component_ids_sha256": "605d3cb3bbc139625ac7c847e29e7139fc0dc94fdf2caa584ffa88abbd9d8060",
    "forecast_only_not_frozen": {
        "G2A_member_count": 38_608,
        "G2B_reference_count": 76_816,
        "G2B_distinct_member_count": 76_816,
        "global_member_count": 564_460,
        "global_representation_count": 611_872,
    },
    "component_count_and_cross_component_pair_denominator": "MUST_BE_RECOMPUTED_BY_FRESH_DSU__NO_FORECAST_CREDIT",
}


OUTPUT_NAMES: Final = {
    "member": "cm2_round306b1af4k2p2_preserved_nongraph_direct_authority_reconciliation_member_ledger.jsonl.gz",
    "representation": "cm2_round306b1af4k2p2_preserved_nongraph_direct_authority_reconciliation_representation_ledger.jsonl.gz",
    "obligation": "cm2_round306b1af4k2p2_preserved_nongraph_direct_authority_reconciliation_A1_A2_ledger.jsonl.gz",
    "delta": "cm2_round306b1af4k2p2_preserved_nongraph_direct_authority_reconciliation_direct_receipt_frontier_delta.jsonl.gz",
    "gap": "cm2_round306b1af4k2p2_preserved_nongraph_direct_authority_reconciliation_gap_ledger.jsonl.gz",
    "result": "cm2_round306b1af4k2p2_preserved_nongraph_direct_authority_reconciliation_result.json",
}


def canonical_bytes(value: Any) -> bytes:
    raw = json.dumps(
        value, ensure_ascii=True, allow_nan=False, sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")
    need(len(raw) <= ROW_CAP, "post-canonical 8MiB row cap")
    return raw


def sha(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def file_sha(path: str | os.PathLike[str]) -> tuple[int, str]:
    h = hashlib.sha256()
    size = 0
    with open(path, "rb") as stream:
        while True:
            block = stream.read(IO_CHUNK)
            if not block:
                break
            size += len(block)
            h.update(block)
    return size, h.hexdigest()


def row_sha(row: dict[str, Any]) -> str:
    need(type(row) is dict, "row object")
    expected = row.get("row_sha256")
    need(type(expected) is str and len(expected) == 64, "row SHA field")
    body = dict(row)
    del body["row_sha256"]
    actual = sha(body)
    need(actual == expected, "row SHA mismatch")
    return actual


def typed_zero_credit(value: Any, path: str = "") -> None:
    if type(value) is dict:
        for key, child in value.items():
            here = path + "." + key if path else key
            if key.endswith("_credit") or key.endswith("_credit_count"):
                need(type(child) is int, "credit must be strict int:" + here)
            typed_zero_credit(child, here)
    elif type(value) is list:
        for index, child in enumerate(value):
            typed_zero_credit(child, f"{path}[{index}]")


def strict_json_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in result, "duplicate JSON key:" + key)
        result[key] = value
    return result


def reject_constant(token: str) -> Any:
    raise ReconciliationError("nonfinite JSON constant:" + token)


STRICT_DECODER: Final = json.JSONDecoder(
    object_pairs_hook=strict_json_pairs,
    parse_constant=reject_constant,
)


def strict_load_text(text: str) -> Any:
    value, end = STRICT_DECODER.raw_decode(text)
    need(text[end:].strip() == "", "JSON trailing bytes")
    return value


def stat_fp(info: os.stat_result) -> tuple[int, ...]:
    return (
        info.st_dev, info.st_ino, info.st_mode, info.st_nlink,
        info.st_uid, info.st_gid, info.st_size,
        info.st_mtime_ns, info.st_ctime_ns,
    )


def dir_fp(info: os.stat_result) -> tuple[int, int, int]:
    return (info.st_dev, info.st_ino, info.st_mode)


def hash_fd(fd: int) -> tuple[int, str]:
    os.lseek(fd, 0, os.SEEK_SET)
    h = hashlib.sha256()
    size = 0
    while True:
        block = os.read(fd, IO_CHUNK)
        if not block:
            break
        size += len(block)
        h.update(block)
    os.lseek(fd, 0, os.SEEK_SET)
    return size, h.hexdigest()


class HeldPins:
    def __init__(self) -> None:
        self.dir_fd = -1
        self.dir_initial: os.stat_result | None = None
        self.fds: dict[str, int] = {}
        self.initial: dict[str, os.stat_result] = {}
        self.receipts: list[dict[str, Any]] = []

    def __enter__(self) -> "HeldPins":
        need(bool(PINS), FINAL_PIN_GATE)
        need(len({p.label for p in PINS}) == len(PINS), "pin label uniqueness")
        need(len({p.filename for p in PINS}) == len(PINS), "pin filename uniqueness")
        before = os.stat(INPUT_DIRECTORY, follow_symlinks=False)
        need(stat.S_ISDIR(before.st_mode), "input directory")
        flags = (
            os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) |
            getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
        )
        self.dir_fd = os.open(os.fspath(INPUT_DIRECTORY), flags)
        held_dir = os.fstat(self.dir_fd)
        need(dir_fp(before) == dir_fp(held_dir), "input directory open race")
        self.dir_initial = held_dir
        try:
            for pin in PINS:
                need(
                    pin.filename == os.path.basename(pin.filename)
                    and pin.filename not in ("", ".", ".."),
                    "pin basename:" + pin.label,
                )
                path_info = os.stat(
                    pin.filename, dir_fd=self.dir_fd, follow_symlinks=False
                )
                need(stat.S_ISREG(path_info.st_mode), "pin regular:" + pin.label)
                need(path_info.st_nlink == 1, "pin nlink:" + pin.label)
                need(path_info.st_size == pin.exact_size, "pin size:" + pin.label)
                fflags = (
                    os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) |
                    getattr(os, "O_NOFOLLOW", 0)
                )
                fd = os.open(pin.filename, fflags, dir_fd=self.dir_fd)
                opened = os.fstat(fd)
                need(stat_fp(opened) == stat_fp(path_info), "pin open race:" + pin.label)
                size1, sha1 = hash_fd(fd)
                middle = os.fstat(fd)
                size2, sha2 = hash_fd(fd)
                after = os.fstat(fd)
                need(stat_fp(opened) == stat_fp(middle) == stat_fp(after), "pin changed:" + pin.label)
                need(size1 == size2 == pin.exact_size, "pin two-pass size:" + pin.label)
                need(sha1 == sha2 == pin.sha256, "pin two-pass SHA:" + pin.label)
                self.fds[pin.label] = fd
                self.initial[pin.label] = opened
                self.receipts.append({
                    "label": pin.label,
                    "filename": pin.filename,
                    "exact_size": pin.exact_size,
                    "sha256": pin.sha256,
                    "role": pin.role,
                    "two_pass_held_fd_sha256": [sha1, sha2],
                })
            return self
        except BaseException:
            self.close()
            raise

    def _dup_stream(self, label: str) -> io.BufferedReader:
        need(label in self.fds, "unknown pin:" + label)
        fd = os.dup(self.fds[label])
        os.lseek(fd, 0, os.SEEK_SET)
        return os.fdopen(fd, "rb", closefd=True)

    def json(self, label: str) -> Any:
        with self._dup_stream(label) as stream:
            raw = stream.read()
        need(len(raw) <= next(p.exact_size for p in PINS if p.label == label), "JSON size")
        return strict_load_text(raw.decode("ascii"))

    def text(self, label: str) -> str:
        with self._dup_stream(label) as stream:
            return stream.read().decode("utf-8")

    def iter_jsonl_gzip(self, label: str) -> Iterator[dict[str, Any]]:
        """Decode exactly one gzip member and strict JSONL rows."""
        with self._dup_stream(label) as stream:
            decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
            pending = b""
            finished = False
            while True:
                block = stream.read(IO_CHUNK)
                if not block:
                    break
                need(not finished, "gzip trailing bytes:" + label)
                out = decoder.decompress(block)
                if decoder.unused_data:
                    raise ReconciliationError("gzip multimember/trailing:" + label)
                pending += out
                while b"\n" in pending:
                    line, pending = pending.split(b"\n", 1)
                    need(line != b"", "blank JSONL row:" + label)
                    need(len(line) <= ROW_CAP, "decoded JSONL row cap:" + label)
                    value = strict_load_text(line.decode("ascii"))
                    need(type(value) is dict, "JSONL object:" + label)
                    canonical_bytes(value)
                    yield value
                need(len(pending) <= ROW_CAP, "pending JSONL row cap:" + label)
                finished = decoder.eof
            pending += decoder.flush()
            need(decoder.eof, "truncated gzip:" + label)
            need(not decoder.unused_data and not decoder.unconsumed_tail, "gzip boundary:" + label)
            if pending:
                need(len(pending) <= ROW_CAP, "final JSONL row cap:" + label)
                value = strict_load_text(pending.decode("ascii"))
                need(type(value) is dict, "final JSONL object:" + label)
                canonical_bytes(value)
                yield value

    def final(self) -> None:
        need(self.dir_fd >= 0 and self.dir_initial is not None, "pins active")
        pin_map = {pin.label: pin for pin in PINS}
        for label, fd in self.fds.items():
            pin = pin_map[label]
            held = os.fstat(fd)
            path = os.stat(pin.filename, dir_fd=self.dir_fd, follow_symlinks=False)
            need(stat_fp(held) == stat_fp(self.initial[label]), "held pin changed:" + label)
            need(stat_fp(path) == stat_fp(self.initial[label]), "pin path replaced:" + label)
            size3, sha3 = hash_fd(fd)
            need(size3 == pin.exact_size and sha3 == pin.sha256, "final pin SHA:" + label)
            next(row for row in self.receipts if row["label"] == label)[
                "final_post_parse_held_fd_sha256"
            ] = sha3
        d_held = os.fstat(self.dir_fd)
        d_path = os.stat(INPUT_DIRECTORY, follow_symlinks=False)
        need(dir_fp(d_held) == dir_fp(self.dir_initial), "held input directory changed")
        need(dir_fp(d_path) == dir_fp(self.dir_initial), "input directory replaced")

    def close(self) -> None:
        for fd in self.fds.values():
            try:
                os.close(fd)
            except OSError:
                pass
        self.fds.clear()
        if self.dir_fd >= 0:
            try:
                os.close(self.dir_fd)
            except OSError:
                pass
            self.dir_fd = -1

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.close()


class ExplicitTmp:
    def __init__(self) -> None:
        self.path = ""
        self.root_fd = -1
        self.root_fp: tuple[int, int, int] | None = None

    def __enter__(self) -> str:
        deliverables = os.path.realpath(INPUT_DIRECTORY)
        need(os.path.realpath(TMP_ROOT) == TMP_ROOT, "literal /tmp realpath")
        root_l = os.lstat(TMP_ROOT)
        root_s = os.stat(TMP_ROOT)
        need(stat.S_ISDIR(root_l.st_mode) and not stat.S_ISLNK(root_l.st_mode), "/tmp directory")
        need(dir_fp(root_l) == dir_fp(root_s), "/tmp identity")
        need(os.path.commonpath((TMP_ROOT, deliverables)) != deliverables, "/tmp outside deliverables")
        flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
        self.root_fd = os.open(TMP_ROOT, flags)
        self.root_fp = dir_fp(os.fstat(self.root_fd))
        need(self.root_fp == dir_fp(root_s), "/tmp open race")
        self.path = tempfile.mkdtemp(prefix="cm2-k2p2-", dir=TMP_ROOT)
        made = os.lstat(self.path)
        need(stat.S_ISDIR(made.st_mode) and not stat.S_ISLNK(made.st_mode), "temp directory")
        need(os.path.dirname(os.path.realpath(self.path)) == TMP_ROOT, "temp parent")
        return self.path

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        try:
            need(self.root_fp is not None and dir_fp(os.fstat(self.root_fd)) == self.root_fp, "held /tmp changed")
            need(dir_fp(os.stat(TMP_ROOT)) == self.root_fp, "/tmp path replaced")
        finally:
            if self.path:
                shutil.rmtree(self.path)
            if self.root_fd >= 0:
                os.close(self.root_fd)
        need(not os.path.lexists(self.path), "temp cleanup")


class GzipLedger:
    def __init__(self, directory: str, filename: str, id_field: str) -> None:
        self.filename = filename
        self.id_field = id_field
        self.path = os.path.join(directory, filename)
        self.raw = open(self.path, "xb")
        self.gz = gzip.GzipFile(filename="", mode="wb", fileobj=self.raw, mtime=0)
        self.rows = 0
        self.ids: set[str] = set()
        self.plain_hash = hashlib.sha256()
        self.plain_size = 0

    def add(self, row: dict[str, Any]) -> None:
        key = row.get(self.id_field)
        need(type(key) is str and key != "", "ledger row key:" + self.filename)
        need(key not in self.ids, "duplicate ledger row key:" + key)
        self.ids.add(key)
        row_sha(row)
        line = canonical_bytes(row) + b"\n"
        self.gz.write(line)
        self.plain_hash.update(line)
        self.plain_size += len(line)
        self.rows += 1

    def close(self) -> dict[str, Any]:
        self.gz.close()
        self.raw.close()
        size, digest = file_sha(self.path)
        return {
            "filename": self.filename,
            "compression": "single-gzip-member-mtime-zero-empty-header-name",
            "row_count": self.rows,
            "row_id_field": self.id_field,
            "file_size": size,
            "file_sha256": digest,
            "uncompressed_jsonl_size": self.plain_size,
            "uncompressed_jsonl_sha256": self.plain_hash.hexdigest(),
        }


@dataclass
class Evidence:
    receipt_ids: dict[str, list[str]] = field(default_factory=lambda: defaultdict(list))
    local_ids: dict[str, list[str]] = field(default_factory=lambda: defaultdict(list))
    incidence_ids: list[str] = field(default_factory=list)

    def receipt(self, lane: str, row_id: str) -> None:
        self.receipt_ids[lane].append(row_id)

    def local(self, lane: str, row_id: str) -> None:
        self.local_ids[lane].append(row_id)

    def summary(self) -> dict[str, Any]:
        receipt = {
            lane: {
                "row_count": len(set(ids)),
                "sorted_row_ids_sha256": sha(sorted(set(ids))),
            }
            for lane, ids in sorted(self.receipt_ids.items())
        }
        local = {
            lane: {
                "row_count": len(set(ids)),
                "sorted_row_ids_sha256": sha(sorted(set(ids))),
            }
            for lane, ids in sorted(self.local_ids.items())
        }
        return {
            "receipt_lanes": receipt,
            "narrow_local_authority_lanes": local,
            "local_incidence_attachment_count": len(set(self.incidence_ids)),
            "local_incidence_attachment_ids_sha256": sha(sorted(set(self.incidence_ids))),
        }


def get_rows(document: dict[str, Any], *path: str) -> list[Any]:
    value: Any = document
    for key in path:
        need(type(value) is dict and key in value, "missing JSON path:" + ".".join(path))
        value = value[key]
    need(type(value) is list, "row table path:" + ".".join(path))
    return value


def get_nested_rows(document: dict[str, Any], ledger: str, rows_key: str = "rows") -> list[Any]:
    return get_rows(document, "result", ledger, rows_key)


def table_stat(label: str, rows: Iterable[dict[str, Any]], id_field: str) -> dict[str, Any]:
    ids: list[str] = []
    body_hashes: list[str] = []
    canonical_hashes: list[str] = []
    for row in rows:
        typed_zero_credit(row)
        row_sha(row)
        key = row.get(id_field)
        need(type(key) is str, "table key:" + label)
        ids.append(key)
        body_hashes.append(row["row_sha256"])
        canonical_hashes.append(hashlib.sha256(canonical_bytes(row)).hexdigest())
    need(len(ids) == len(set(ids)), "duplicate table IDs:" + label)
    return {
        "table_label": label,
        "row_id_field": id_field,
        "row_count": len(ids),
        "ordered_row_ids_sha256": sha(ids),
        "unordered_row_ids_sha256": sha(sorted(ids)),
        "ordered_declared_row_sha256s_sha256": sha(body_hashes),
        "ordered_canonical_row_sha256s_sha256": sha(canonical_hashes),
    }


def raw_table_stat(
    label: str,
    rows: Iterable[dict[str, Any]],
    id_field: str,
) -> dict[str, Any]:
    """Commit a legacy table even when per-row hashes were absent."""
    ids: list[str] = []
    canonical_hashes: list[str] = []
    declared: list[str] = []
    declared_count = 0
    for row in rows:
        need(type(row) is dict, "raw table row:" + label)
        typed_zero_credit(row)
        key = row.get(id_field)
        need(type(key) is str and key != "", "raw table key:" + label)
        ids.append(key)
        canonical_hashes.append(hashlib.sha256(canonical_bytes(row)).hexdigest())
        if "row_sha256" in row:
            declared.append(row_sha(row))
            declared_count += 1
        else:
            declared.append("NO_DECLARED_ROW_SHA256")
    need(len(ids) == len(set(ids)), "duplicate raw table IDs:" + label)
    return {
        "table_label": label,
        "row_id_field": id_field,
        "row_count": len(ids),
        "ordered_row_ids_sha256": sha(ids),
        "unordered_row_ids_sha256": sha(sorted(ids)),
        "ordered_canonical_row_sha256s_sha256": sha(canonical_hashes),
        "ordered_declared_row_sha256s_or_missing_sha256": sha(declared),
        "declared_row_sha256_count": declared_count,
        "missing_declared_row_sha256_count": len(ids) - declared_count,
    }


def commitment_row(schema_suffix: str, key_field: str, key: str, payload: dict[str, Any]) -> dict[str, Any]:
    canonical_input = {
        "domain": SCHEMA + "." + schema_suffix + ".canonical-input.v1",
        **payload,
    }
    body = {
        "schema": SCHEMA + "." + schema_suffix + ".row.v1",
        key_field: key,
        "canonical_input_commitment": canonical_input,
        "canonical_input_commitment_sha256": sha(canonical_input),
    }
    body["row_sha256"] = sha(body)
    return body


def assert_manifest(held: HeldPins, manifest_label: str, expected_labels: Iterable[str]) -> dict[str, Any]:
    pin_by_label = {pin.label: pin for pin in PINS}
    rows: list[dict[str, str]] = []
    for raw_line in held.text(manifest_label).splitlines():
        parts = raw_line.split("  ", 1)
        need(len(parts) == 2 and len(parts[0]) == 64, "manifest line:" + manifest_label)
        rows.append({"sha256": parts[0], "filename": parts[1]})
    expected = [
        {"sha256": pin_by_label[label].sha256, "filename": pin_by_label[label].filename}
        for label in expected_labels
    ]
    need(rows == expected, "manifest exact ordered membership:" + manifest_label)
    return {
        "manifest_label": manifest_label,
        "entry_count": len(rows),
        "ordered_entries_sha256": sha(rows),
        "exact_ordered_membership": True,
    }


def validate_envelope(document: dict[str, Any], label: str) -> dict[str, Any]:
    need(type(document) is dict, "envelope object:" + label)
    if "result" in document and "result_sha256" in document:
        need(type(document["result"]) is dict, "result object:" + label)
        need(sha(document["result"]) == document["result_sha256"], "result digest:" + label)
        return document["result"]
    return document


def attach(evidence: dict[str, Evidence], member_id: str, kind: str, lane: str, row_id: str) -> None:
    need(member_id in evidence, "authority/member anti-join:" + member_id)
    if kind == "receipt":
        evidence[member_id].receipt(lane, row_id)
    elif kind == "local":
        evidence[member_id].local(lane, row_id)
    elif kind == "incidence":
        evidence[member_id].incidence_ids.append(row_id)
    else:
        raise ReconciliationError("unknown attachment kind")


P1_BLOCKERS: Final = (
    (
        "B01_WIRE_SHAPE_KERNEL_ZERO_THEOREM_CREDIT",
        "the sealed 13-kernel bundle is mostly wire-shape validation; equivalence, graph existence, incidence, backbinding, sheet/boundary ownership, and source exhaustion remain unproved",
    ),
    (
        "B02_NO_INDEPENDENT_SYMBOLIC_DIFFERENTIATION",
        "no pinned independent symbolic differentiation and derivative-identity primitive exists",
    ),
    (
        "B03_R211_NOT_SELF_CONTAINED",
        "R211 rows omit a self-contained chart/target/box/equation/derivative AST and require multi-hop R208/probe reconstruction plus independent interval proof",
    ),
    (
        "B04_ALIAS_SET_EQUALITY_NOT_DISCHARGED",
        "720 TPS inclusion rows, 1600 T2PS subcover rows, and 276 R295A adjacent continuation boxes cannot claim per-row complete-support set equality",
    ),
    (
        "B05_TPS_INTERCHART_THEOREM_MISSING",
        "canonical TPS inter-chart forward/inverse AST and theorem are absent; generic CHART_PULLBACK and fixed-sign T2PS are insufficient",
    ),
    (
        "B06_DIRECT_THEOREM_EVIDENCE_FRONTIER_INCOMPLETE",
        "independent theorem replay still needs direct row-level R231/R233/R230/R235/Gate5/R209 evidence; promotion summaries do not suffice",
    ),
)


def make_row(
    suffix: str,
    key_field: str,
    key: str,
    canonical_input: dict[str, Any],
    conclusion: dict[str, Any],
) -> dict[str, Any]:
    need(key_field not in conclusion and "row_sha256" not in conclusion, "reserved conclusion key")
    bound = {
        "domain": SCHEMA + "." + suffix + ".canonical-input.v1",
        **canonical_input,
    }
    body = {
        "schema": SCHEMA + "." + suffix + ".row.v1",
        key_field: key,
        "canonical_input_commitment": bound,
        "canonical_input_commitment_sha256": sha(bound),
        **conclusion,
    }
    typed_zero_credit(body)
    body["row_sha256"] = sha(body)
    return body


def validate_exact_envelope(document: dict[str, Any], body_key: str, digest_key: str, label: str) -> dict[str, Any]:
    need(type(document) is dict and type(document.get(body_key)) is dict, "receipt envelope:" + label)
    need(type(document.get(digest_key)) is str, "receipt digest field:" + label)
    need(sha(document[body_key]) == document[digest_key], "receipt object digest:" + label)
    return document[body_key]


def validate_latest_receipts(held: HeldPins) -> dict[str, Any]:
    """Validate every latest package object actually used by this join."""
    receipt_specs = (
        ("P0_LEDGER", "ledger", "ledger_sha256"),
        ("P0_RESULT", None, None),
        ("K1_RESULT", "result", "result_sha256"),
        ("K1_VERIFICATION", None, None),
        ("I2_RESULT", None, None),
        ("I4_RESULT", None, None),
        ("R209_RESULT", "result", "result_sha256"),
        ("R209_VERIFICATION", None, None),
        ("R230_LEDGER", "ledger", "ledger_sha256"),
        ("R230_VERIFICATION", None, None),
        ("R231_LEDGER", "ledger", "ledger_sha256"),
        ("R231_VERIFICATION", None, None),
        ("R233_LEDGER", "ledger", "ledger_sha256"),
        ("R233_VERIFICATION", None, None),
        ("R235_RESULT", "result", "result_sha256"),
        ("R235_VERIFICATION", None, None),
        ("R235D_RESULT", "result", "result_sha256"),
        ("R235D_VERIFICATION", None, None),
    )
    receipts: dict[str, Any] = {}
    for label, body_key, digest_key in receipt_specs:
        document = held.json(label)
        need(type(document) is dict, "receipt JSON object:" + label)
        if body_key is not None and digest_key is not None:
            validate_exact_envelope(document, body_key, digest_key, label)
        typed_zero_credit(document)
        receipts[label] = {
            "canonical_document_sha256": sha(document),
            "envelope_digest_checked": body_key is not None,
        }

    p0 = held.json("P0_LEDGER")
    need(p0["ledger"]["selected_table_summary"]["table_count"] == 17, "P0 table count")
    need(p0["ledger"]["selected_table_summary"]["row_count"] == 204_162, "P0 row count")
    need(held.json("P0_RESULT").get("status", "").startswith("PASS_ENGINEERING"), "P0 status")

    i2 = held.json("I2_RESULT")
    need(i2["exact_census"]["member_count"] == 144_296, "I2 result members")
    need(i2["exact_census"]["representation_count"] == 183_572, "I2 result representations")
    i4 = held.json("I4_RESULT")
    need(i4["exact_census"]["member_count"] == 564_492, "I4 result members")
    need(i4["exact_census"]["representation_count"] == 611_904, "I4 result representations")
    need(all(type(v) is int and v == 0 for v in i4["formal_credit"].values()), "I4 zero credit")

    r235 = held.json("R235_RESULT")["result"]
    need(r235["census"]["single_endpoint_local_authority_count"] == 38_328, "R235 single census")
    need(r235["census"]["double_endpoint_factor_deferred_count"] == 16, "R235 deferred census")
    return receipts


def delta_row(
    context_sha: str,
    stats: dict[str, Any],
    source_family: str,
    receipt_count: int,
    narrow_count: int,
    authority_kind: str,
    disposition: str,
) -> dict[str, Any]:
    need(receipt_count == stats["row_count"], "delta receipt/table count:" + stats["table_label"])
    return make_row(
        "direct-receipt-frontier-delta",
        "delta_row_id",
        "direct-receipt-frontier:" + stats["table_label"],
        {
            "global_context_sha256": context_sha,
            "source_family": source_family,
            "raw_table_commitment": stats,
            "latest_receipt_attachment_count": receipt_count,
            "narrow_local_authority_row_count": narrow_count,
            "authority_kind": authority_kind,
        },
        {
            "source_family": source_family,
            "table_label": stats["table_label"],
            "raw_row_count": stats["row_count"],
            "receipt_attachment_count": receipt_count,
            "narrow_local_authority_row_count": narrow_count,
            "authority_kind": authority_kind,
            "direct_receipt_frontier_disposition": disposition,
            "normalized_full_support_credit": 0,
            "representation_pullback_credit": 0,
            "A1_A2_theorem_credit": 0,
            "B1A_credit": 0,
            "B2_credit": 0,
            "CM2_credit": 0,
        },
    )


def load_i2_and_i4_members(
    held: HeldPins,
) -> tuple[dict[str, dict[str, Any]], dict[str, Evidence], dict[str, dict[str, Any]]]:
    members: dict[str, dict[str, Any]] = {}
    evidence: dict[str, Evidence] = {}
    fine = Counter()
    for row in held.iter_jsonl_gzip("I2_MEMBER"):
        row_sha(row)
        member_id = row.get("member_id")
        need(type(member_id) is str and member_id not in members, "I2 member key")
        need(row.get("coarse_family") in ("PRESERVED", "NON_GRAPH_BULK"), "I2 coarse family")
        members[member_id] = row
        evidence[member_id] = Evidence()
        fine[row["fine_family"]] += 1
    need(len(members) == 144_296, "I2 member count")
    expected_fine = Counter({
        "ROUND174_RESOLVED": 72_500,
        "ROUND179_RESOLVED": 17_192,
        "ROUND204_REGION": 736,
        "ROUND208_REGION": 36_040,
        "R245_WHOLE_ROOT_ZERO_ABSENCE_BULK": 2_872,
        "R246_WHOLE_ORIGIN_SINGLE_SIGNATURE_RETAINED_BULK": 2_220,
        "R247_CROSSING_TIME_WHOLE_SIGNATURE_RETAINED_BULK": 240,
        "R247_SOURCE_CHART_SEAM_WHOLE_SIGNATURE_RETAINED_BULK": 264,
        "R248_ROUND234_RESOLVED_DESCENDANT": 12_200,
        "R248_ROUND236_CROSSING_DISCHARGE_BULK": 32,
    })
    need(fine == expected_fine, "I2 fine census")

    i4_rows: dict[str, dict[str, Any]] = {}
    non_i2_seen = False
    for row in held.iter_jsonl_gzip("I4_MEMBER"):
        row_sha(row)
        lane = row.get("source_lane")
        if lane != "I2":
            non_i2_seen = True
            continue
        need(not non_i2_seen, "I4 I2 member lane order")
        member_id = row.get("member_id")
        source = members.get(member_id)
        need(source is not None and member_id not in i4_rows, "I2/I4 member anti-join")
        commitment = row.get("canonical_input_commitment")
        need(type(commitment) is dict, "I4 member input commitment")
        need(commitment.get("source_member_row_sha256") == source["row_sha256"], "I4/I2 member row SHA")
        need(
            commitment.get("source_member_row_canonical_sha256")
            == hashlib.sha256(canonical_bytes(source)).hexdigest(),
            "I4/I2 member canonical SHA",
        )
        need(row.get("coarse_family") == source["coarse_family"], "I4/I2 member family")
        need(
            row.get("primary_mechanical_representation_id")
            == source["primary_representation_id"],
            "I4/I2 primary representation",
        )
        i4_rows[member_id] = row
    need(set(i4_rows) == set(members), "I2/I4 member exact anti-join")
    return members, evidence, i4_rows


def load_non_graph_backlinks(
    held: HeldPins,
    members: dict[str, dict[str, Any]],
) -> tuple[dict[str, str], dict[str, str], dict[str, str]]:
    direct = {row["direct_construction_row_id"]: member_id for member_id, row in members.items()}
    retained_to_member: dict[str, str] = {}
    r234_to_member: dict[str, str] = {}
    r236_to_member: dict[str, str] = {}

    r245 = validate_envelope(held.json("R245_CERT"), "R245_CERT")
    rows245 = get_nested_rows({"result": r245}, "formal_retained_stratum_node_ledger")
    used245 = 0
    for row in rows245:
        row_sha(row)
        member_id = direct.get(row["retained_stratum_node_id"])
        if member_id is None:
            continue
        need(members[member_id]["fine_family"] == "R245_WHOLE_ROOT_ZERO_ABSENCE_BULK", "R245 family")
        need(row["Round179_retained_child_row_id"] not in retained_to_member, "R245 retained uniqueness")
        retained_to_member[row["Round179_retained_child_row_id"]] = member_id
        used245 += 1
    need(used245 == 2_872, "R245 backlink count")
    del r245, rows245

    r246 = validate_envelope(held.json("R246_CERT"), "R246_CERT")
    rows246 = get_nested_rows({"result": r246}, "formal_new_whole_signature_retained_stratum_node_ledger")
    used246 = 0
    for row in rows246:
        row_sha(row)
        member_id = direct.get(row["retained_stratum_node_id"])
        if member_id is None:
            continue
        need(members[member_id]["fine_family"] == "R246_WHOLE_ORIGIN_SINGLE_SIGNATURE_RETAINED_BULK", "R246 family")
        need(row["Round179_retained_child_row_id"] not in retained_to_member, "R246 retained uniqueness")
        retained_to_member[row["Round179_retained_child_row_id"]] = member_id
        used246 += 1
    need(used246 == 2_220, "R246 backlink count")
    del r246, rows246

    r248 = validate_envelope(held.json("R248_CERT"), "R248_CERT")
    rows248 = get_nested_rows({"result": r248}, "formal_wall_positive_volume_bulk_ledger")
    used248 = Counter()
    for row in rows248:
        row_sha(row)
        member_id = direct.get(row["wall_bulk_node_id"])
        if member_id is None:
            continue
        kind = row["source_partition_kind"]
        if kind == "ROUND234_RESOLVED_DESCENDANT":
            need(row["source_partition_row_id"] not in r234_to_member, "R234 backlink uniqueness")
            r234_to_member[row["source_partition_row_id"]] = member_id
        elif kind == "ROUND236_CROSSING_DISCHARGE_BULK":
            need(row["source_partition_row_id"] not in r236_to_member, "R236 backlink uniqueness")
            r236_to_member[row["source_partition_row_id"]] = member_id
        else:
            raise ReconciliationError("unexpected I2 R248 source kind")
        used248[kind] += 1
    need(used248 == Counter({"ROUND234_RESOLVED_DESCENDANT": 12_200, "ROUND236_CROSSING_DISCHARGE_BULK": 32}), "R248 backlink census")
    need(len(retained_to_member) == 5_092, "non-graph retained backlink total")
    del r248, rows248
    return retained_to_member, r234_to_member, r236_to_member


def reconcile_r209_and_obligations(
    held: HeldPins,
    members: dict[str, dict[str, Any]],
    evidence: dict[str, Evidence],
    context_sha: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    r209_specs = (
        ("R209_SHEET", "R209_SHEET", "sheet_row_id", "A1_R211_OWNER_SHEET"),
        ("R209_CURVE", "R209_CURVE", "curve_row_id", "A2_R211_OWNER_CURVE"),
        ("R209_ENDPOINT", "R209_ENDPOINT", "endpoint_row_id", "A2_R211_OWNER_ENDPOINT"),
    )
    probe_maps: dict[str, dict[str, dict[str, Any]]] = {}
    delta_rows: list[dict[str, Any]] = []
    for table_label, pin_label, id_field, obligation_kind in r209_specs:
        rows = list(held.iter_jsonl_gzip(pin_label))
        stats = table_stat(table_label, rows, id_field)
        probes: dict[str, dict[str, Any]] = {}
        for row in rows:
            probe = row["source_probe_row_id"]
            need(probe not in probes, "R209 probe uniqueness")
            probes[probe] = row
            owner = row["owner_region_row_id"]
            need(owner in members and members[owner]["fine_family"] == "ROUND208_REGION", "R209 owner/I2 join")
            attach(evidence, owner, "receipt", table_label, row[id_field])
            attach(evidence, owner, "local", table_label, row[id_field])
        probe_maps[obligation_kind] = probes
        delta_rows.append(delta_row(
            context_sha, stats, "R209", len(rows), len(rows),
            "LOCAL_DIMENSIONAL_OWNER_AUTHORITY_ONLY",
            "DIRECT_INPUT_BOUND_LOCAL_OWNER_RECEIPT_ATTACHED__A1_A2_THEOREM_NOT_DISCHARGED",
        ))

    r211 = validate_envelope(held.json("R211_CERT"), "R211_CERT")
    obligation_rows: list[dict[str, Any]] = []
    r211_specs = (
        ("A1_R211_OWNER_SHEET", "formal_2D_sheet_owner_ledger", "sheet_row_id", "probe_sheet_row_id", "probe_sheet_row_sha256", "sheet_row_id"),
        ("A2_R211_OWNER_CURVE", "formal_1D_curve_incidence_owner_ledger", "curve_row_id", "probe_curve_row_id", "probe_curve_row_sha256", "curve_row_id"),
        ("A2_R211_OWNER_ENDPOINT", "formal_0D_endpoint_incidence_owner_ledger", "endpoint_row_id", "probe_endpoint_row_id", "probe_endpoint_row_sha256", "endpoint_row_id"),
    )
    for kind, ledger_name, source_id_field, probe_id_field, probe_sha_field, authority_id_field in r211_specs:
        rows = get_nested_rows({"result": r211}, ledger_name)
        probe_map = probe_maps[kind]
        for row in rows:
            row_sha(row)
            authority = probe_map.get(row[probe_id_field])
            need(authority is not None, "R211/R209 probe anti-join")
            need(authority["source_probe_row_sha256"] == row[probe_sha_field], "R211/R209 probe SHA")
            key = kind + "\0" + row[source_id_field]
            obligation_rows.append(make_row(
                "A1-A2-obligation", "obligation_id", key,
                {
                    "global_context_sha256": context_sha,
                    "obligation_kind": kind,
                    "source_package": "R211",
                    "source_row_id": row[source_id_field],
                    "source_row_sha256": row["row_sha256"],
                    "R209_authority_row_id": authority[authority_id_field],
                    "R209_authority_row_sha256": authority["row_sha256"],
                    "R209_source_probe_row_id": authority["source_probe_row_id"],
                    "R209_source_probe_row_sha256": authority["source_probe_row_sha256"],
                },
                {
                    "obligation_kind": kind,
                    "source_package": "R211",
                    "source_row_id": row[source_id_field],
                    "local_dimensional_owner_authority_attachment": True,
                    "A1_A2_theorem_credit": 0,
                    "normalized_full_support_credit": 0,
                    "status": "LOCAL_DIMENSIONAL_OWNER_AUTHORITY_ATTACHED__A1_A2_THEOREM_NOT_DISCHARGED",
                },
            ))
    del r211, probe_maps

    r204 = validate_envelope(held.json("R204_CERT"), "R204_CERT")
    r204_specs: list[tuple[str, list[dict[str, Any]], str]] = [
        ("A1_R204_TARGET_SHEET", get_rows(r204, "formal_2D_sheet_lineage", "target_sheet_rows"), "sheet_row_id"),
        (
            "A2_R204_SOURCE_TARGET_CURVE",
            [row for row in get_rows(r204, "formal_1D_boundary_and_intersection_lineage", "rows") if row["geometry_kind"].startswith("TARGET_GRAPH_")],
            "edge_row_id",
        ),
        (
            "A2_R204_SOURCE_TARGET_ENDPOINT",
            [row for row in get_rows(r204, "formal_0D_endpoint_and_corner_lineage", "rows") if row["geometry_kind"] == "TARGET_GRAPH_P_S_POINT"],
            "point_row_id",
        ),
    ]
    for kind, rows, id_field in r204_specs:
        for row in rows:
            row_sha(row)
            key = kind + "\0" + row[id_field]
            obligation_rows.append(make_row(
                "A1-A2-obligation", "obligation_id", key,
                {
                    "global_context_sha256": context_sha,
                    "obligation_kind": kind,
                    "source_package": "R204",
                    "source_row_id": row[id_field],
                    "source_row_sha256": row["row_sha256"],
                    "local_authority_receipt": None,
                },
                {
                    "obligation_kind": kind,
                    "source_package": "R204",
                    "source_row_id": row[id_field],
                    "local_dimensional_owner_authority_attachment": False,
                    "A1_A2_theorem_credit": 0,
                    "normalized_full_support_credit": 0,
                    "status": "EXACT_R204_OBLIGATION_UNATTACHED__A1_A2_THEOREM_NOT_DISCHARGED",
                },
            ))
    del r204
    obligation_rows.sort(key=lambda row: row["obligation_id"].encode("ascii"))
    need(len(obligation_rows) == 80_092, "A1/A2 total")
    attached = sum(row["local_dimensional_owner_authority_attachment"] is True for row in obligation_rows)
    need(attached == 79_084 and len(obligation_rows) - attached == 1_008, "A1/A2 attachment split")
    return obligation_rows, delta_rows


def reconcile_r230(
    held: HeldPins,
    members: dict[str, dict[str, Any]],
    evidence: dict[str, Evidence],
    context_sha: str,
) -> list[dict[str, Any]]:
    direct = {row["direct_construction_row_id"]: member_id for member_id, row in members.items()}
    need(len(direct) == len(members), "I2 direct construction uniqueness")
    result = validate_envelope(held.json("R230_OLD_CERT"), "R230_OLD_CERT")
    specs = (
        ("R230_ABSENCE", "formal_resolved_child_event_zero_set_absence_ledger", "event_zero_set_absence_row_id", 0, "INPUT_BOUND_EVENT_ZERO_ABSENCE_RECEIPT_ONLY"),
        ("R230_FACE_CANDIDATE", "formal_exact_face_candidate_ledger", "face_candidate_row_id", 0, "INPUT_BOUND_FACE_CANDIDATE_RECEIPT_ONLY"),
        ("R230_EDGE", "formal_certified_local_bulk_continuation_edge_ledger", "certified_local_bulk_bridge_edge_id", 784, "LOCAL_PATCH_AUTHORITY_ONLY"),
        ("R230_REJECT", "formal_rejected_local_bulk_candidate_ledger", "reject_row_id", 0, "REJECTION_RECEIPT_ONLY"),
        ("R230_STAR", "formal_certified_local_bulk_bridge_star_ledger", "bridge_star_row_id", 0, "LOCAL_STAR_GROUPING_RECEIPT__MEMBER_ATTACHMENTS_DERIVED_FROM_EDGE_ROWS"),
        ("R230_INCIDENCE_DELTA", "formal_occurrence_known_block_incidence_delta_ledger", "incidence_delta_row_id", 464, "LOCAL_INCIDENCE_ATTACHMENT_ONLY__NOT_MEMBER_AUTHORITY"),
        ("R230_POST_OCCURRENCE", "formal_post_Round230_occurrence_known_block_frontier_ledger", "post_frontier_row_id", 0, "POST_FRONTIER_RECEIPT_ATTACHMENT_ONLY"),
        ("R230_POST_KEY", "formal_post_Round230_key_frontier_ledger", "key_frontier_row_id", 0, "POST_KEY_RECEIPT_ONLY__KEY_IS_NOT_WHOLE_SUPPORT"),
    )
    rows_by_label: dict[str, list[dict[str, Any]]] = {}
    delta: list[dict[str, Any]] = []
    for label, ledger_name, id_field, narrow, kind in specs:
        rows = get_rows(result, ledger_name, "rows")
        stats = raw_table_stat(label, rows, id_field)
        rows_by_label[label] = rows
        delta.append(delta_row(
            context_sha, stats, "R230", len(rows), narrow, kind,
            "LATEST_HARDENED_R230_RECEIPT_ATTACHED__BRIDGE_TO_FULL_SUPPORT_MISSING",
        ))
    expected = {
        "R230_ABSENCE": 8_976,
        "R230_FACE_CANDIDATE": 1_512,
        "R230_EDGE": 784,
        "R230_REJECT": 740,
        "R230_STAR": 448,
        "R230_INCIDENCE_DELTA": 464,
        "R230_POST_OCCURRENCE": 53_968,
        "R230_POST_KEY": 116,
    }
    need({k: len(v) for k, v in rows_by_label.items()} == expected, "R230 raw table census")

    post_members: set[str] = set()
    for row in rows_by_label["R230_POST_OCCURRENCE"]:
        member_id = direct.get(row["local_occurrence_row_id"])
        need(member_id is not None, "R230 post occurrence/I2 anti-join")
        attach(evidence, member_id, "receipt", "R230_POST_OCCURRENCE", row["post_frontier_row_id"])
        post_members.add(member_id)
    need(len(post_members) == 53_968, "R230 post member uniqueness")

    resolved_edge_members: set[str] = set()
    region_edge_members: set[str] = set()
    for row in rows_by_label["R230_EDGE"]:
        resolved_member = direct.get(row["resolved_child_row_id"])
        region_member = direct.get(row["Round208_region_row_id"])
        need(resolved_member is not None and region_member is not None, "R230 edge/I2 anti-join")
        attach(evidence, resolved_member, "local", "R230_EDGE_RESOLVED_CHILD", row["certified_local_bulk_bridge_edge_id"])
        attach(evidence, region_member, "local", "R230_EDGE_ROUND208_REGION", row["certified_local_bulk_bridge_edge_id"])
        resolved_edge_members.add(resolved_member)
        region_edge_members.add(region_member)
    need(len(resolved_edge_members) == 448, "R230 resolved edge owner count")
    need(len(region_edge_members) == 784, "R230 region edge owner count")
    need(not (resolved_edge_members & region_edge_members), "R230 edge family disjointness")

    incidence_members: set[str] = set()
    for row in rows_by_label["R230_INCIDENCE_DELTA"]:
        member_id = direct.get(row["local_occurrence_row_id"])
        need(member_id is not None, "R230 incidence/I2 anti-join")
        attach(evidence, member_id, "incidence", "R230_INCIDENCE_DELTA", row["incidence_delta_row_id"])
        incidence_members.add(member_id)
    need(len(incidence_members) == 464, "R230 incidence member count")
    need(incidence_members <= (resolved_edge_members | region_edge_members), "R230 incidence must not add member authority")
    return delta


def reconcile_r231_r233(
    held: HeldPins,
    members: dict[str, dict[str, Any]],
    evidence: dict[str, Evidence],
    retained_to_member: dict[str, str],
    context_sha: str,
) -> list[dict[str, Any]]:
    direct = {row["direct_construction_row_id"]: member_id for member_id, row in members.items()}
    delta: list[dict[str, Any]] = []
    r231 = validate_envelope(held.json("R231_OLD_CERT"), "R231_OLD_CERT")
    specs231 = (
        ("R231_RESOLVED", "resolved_descendant_rows", "materialized_row_id"),
        ("R231_GUARD", "guard_descendant_rows", "guard_row_id"),
        ("R231_FRONTIER", "depth6_frontier_rows", "frontier_row_id"),
        ("R231_ROOT", "root_summary_rows", "root_summary_id"),
    )
    r231_tables: dict[str, list[dict[str, Any]]] = {}
    for label, table_name, id_field in specs231:
        rows = get_rows(r231, table_name)
        stats = raw_table_stat(label, rows, id_field)
        r231_tables[label] = rows
        delta.append(delta_row(
            context_sha, stats, "R231", len(rows), 0,
            "INPUT_BOUND_ENGINEERING_ROW_COMMITMENT__NO_SEMANTIC_AUTHORITY",
            "RECEIPT_ATTACHED__R231_ENGINEERING_ROWS_DO_NOT_PROVE_SUPPORT",
        ))
    need([len(r231_tables[x]) for x in ("R231_RESOLVED", "R231_GUARD", "R231_FRONTIER", "R231_ROOT")] == [22_348, 0, 67_924, 5_368], "R231 census")
    mapped_roots = 0
    missing_roots = 0
    for row in r231_tables["R231_ROOT"]:
        member_id = retained_to_member.get(row["Round179_retained_child_row_id"])
        if member_id is None:
            missing_roots += 1
            continue
        attach(evidence, member_id, "receipt", "R231_ROOT_ENGINEERING_RECEIPT", row["root_summary_id"])
        mapped_roots += 1
    need((mapped_roots, missing_roots) == (5_092, 276), "R231 root I2/alias split")

    r233 = validate_envelope(held.json("R233_OLD_CERT"), "R233_OLD_CERT")
    rows233 = get_rows(r233, "parametric_graph_key_partition_rows")
    stats233 = raw_table_stat("R233_PARTITION", rows233, "parametric_graph_partition_row_id")
    delta.append(delta_row(
        context_sha, stats233, "R233", len(rows233), len(rows233),
        "LOCAL_PARAMETRIC_GRAPH_KEY_PARTITION_ROW_AUTHORITY_ONLY",
        "LOCAL_GRAPH_KEY_AUTHORITY_ATTACHED__OWNER_OR_KEY_IS_NOT_WHOLE_SUPPORT",
    ))
    resolved_count = retained_count = retained_missing = 0
    for row in rows233:
        authority_id = row["parametric_graph_partition_row_id"]
        resolved_member = direct.get(row["Round179_resolved_sibling_row_id"])
        need(resolved_member is not None, "R233 resolved sibling/I2 anti-join")
        attach(evidence, resolved_member, "receipt", "R233_PARTITION", authority_id)
        attach(evidence, resolved_member, "local", "R233_RESOLVED_SIBLING_LOCAL_GRAPH_KEY", authority_id)
        resolved_count += 1
        retained_member = retained_to_member.get(row["Round179_retained_child_row_id"])
        if retained_member is None:
            retained_missing += 1
        else:
            attach(evidence, retained_member, "receipt", "R233_PARTITION", authority_id)
            attach(evidence, retained_member, "local", "R233_RETAINED_ROOT_LOCAL_GRAPH_KEY", authority_id)
            retained_count += 1
    need((resolved_count, retained_count, retained_missing) == (3_148, 2_872, 276), "R233 I2/alias split")
    return delta


def reconcile_r235(
    held: HeldPins,
    evidence: dict[str, Evidence],
    r234_to_member: dict[str, str],
    context_sha: str,
) -> list[dict[str, Any]]:
    old = validate_envelope(held.json("R235_OLD_CERT"), "R235_OLD_CERT")
    old_single = get_rows(old, "single_endpoint_graph_partition_rows")
    old_double = get_rows(old, "double_endpoint_deferred_rows")
    single_stat = raw_table_stat("R235_SINGLE", old_single, "endpoint_graph_partition_row_id")
    double_stat = raw_table_stat("R235_DOUBLE_DEFERRED", old_double, "deferred_row_id")
    need((len(old_single), len(old_double)) == (38_328, 16), "R235 old census")
    old_by_frontier: dict[str, dict[str, Any]] = {}
    for row in old_single + old_double:
        frontier = row["Round234_frontier_row_id"]
        need(frontier not in old_by_frontier, "R235 old frontier uniqueness")
        old_by_frontier[frontier] = row

    current_rows = list(held.iter_jsonl_gzip("R235_LEDGER"))
    need(len(current_rows) == 38_344, "R235 hardened row count")
    current_by_frontier: dict[str, dict[str, Any]] = {}
    kinds = Counter()
    for row in current_rows:
        typed_zero_credit(row)
        commitment = row.get("canonical_input_commitment")
        need(type(commitment) is dict and sha(commitment) == row.get("canonical_input_commitment_sha256"), "R235 input commitment")
        frontier = row.get("Round234_frontier_row_id")
        need(type(frontier) is str and frontier not in current_by_frontier, "R235 hardened frontier uniqueness")
        source = old_by_frontier.get(frontier)
        need(source is not None, "R235 hardened/old anti-join")
        need(hashlib.sha256(canonical_bytes(source)).hexdigest() == row["old_output_row_sha256"], "R235 old row binding")
        current_by_frontier[frontier] = row
        kinds[row["kind"]] += 1
    need(kinds == Counter({
        "SINGLE_ENDPOINT_LOCAL_GRAPH_WORD_KEY_PARTITION_AUTHORITY": 38_328,
        "DOUBLE_ENDPOINT_TWO_FACTOR_ARRANGEMENT_DEFERRED_NO_AUTHORITY": 16,
    }), "R235 hardened kinds")
    need(set(current_by_frontier) == set(old_by_frontier), "R235 hardened/old exact join")

    d_rows = list(held.iter_jsonl_gzip("R235D_LEDGER"))
    need(len(d_rows) == 16, "R235D row count")
    d_by_frontier: dict[str, dict[str, Any]] = {}
    old_deferred = {row["Round234_frontier_row_id"]: row for row in old_double}
    for row in d_rows:
        typed_zero_credit(row)
        if "row_sha256" in row:
            row_sha(row)
        commitment = row.get("canonical_input_commitment")
        need(type(commitment) is dict and sha(commitment) == row.get("canonical_input_commitment_sha256"), "R235D input commitment")
        need(type(row.get("local_source_only_endpoint_graph_key_authority_credit")) is int and row["local_source_only_endpoint_graph_key_authority_credit"] == 1, "R235D strict local credit")
        frontier = row.get("Round234_frontier_row_id")
        need(type(frontier) is str and frontier in old_deferred and frontier not in d_by_frontier, "R235D deferred anti-join")
        need(row.get("deferred_row_id") == old_deferred[frontier]["deferred_row_id"], "R235D deferred ID")
        need(row.get("source_R235_deferred_row_sha256") == hashlib.sha256(canonical_bytes(old_deferred[frontier])).hexdigest(), "R235D old row binding")
        current = current_by_frontier[frontier]
        need(row.get("R234_released_descendants") == current["canonical_input_commitment"]["R234_released_descendants"], "R235D released descendants binding")
        d_by_frontier[frontier] = row
    need(set(d_by_frontier) == set(old_deferred), "R235D exact deferred set")

    receipt_members: set[str] = set()
    local_members: set[str] = set()
    d_members: set[str] = set()
    for frontier, row in current_by_frontier.items():
        refs = row["canonical_input_commitment"]["R234_released_descendants"]
        need(type(refs) is list and refs, "R235 released descendants")
        is_single = row["kind"] == "SINGLE_ENDPOINT_LOCAL_GRAPH_WORD_KEY_PARTITION_AUTHORITY"
        for ref in refs:
            need(type(ref) is list and len(ref) == 3, "R235 released reference shape")
            member_id = r234_to_member.get(ref[1])
            need(member_id is not None, "R235 released descendant/I2 anti-join")
            attach(evidence, member_id, "receipt", "R235_AUTHORITY_ROW", row["authority_row_id"])
            receipt_members.add(member_id)
            if is_single:
                attach(evidence, member_id, "local", "R235_SINGLE_LOCAL_GRAPH_KEY", row["authority_row_id"])
                local_members.add(member_id)
            else:
                drow = d_by_frontier[frontier]
                attach(evidence, member_id, "local", "R235D_SOURCE_ONLY_LOCAL_GRAPH_KEY", drow["authority_row_id"])
                local_members.add(member_id)
                d_members.add(member_id)
    need(len(receipt_members) == 10_832, "R235 unique receipt member union")
    need(len(local_members) == 10_832, "R235D must not change unique local member union")
    need(len(d_members) == 112, "R235D deferred reference appearance union")

    return [
        delta_row(
            context_sha, single_stat, "R235_PRESERVED_NONGRAPH", 38_328, 38_328,
            "LOCAL_SINGLE_ENDPOINT_GRAPH_WORD_KEY_AUTHORITY_ONLY",
            "LOCAL_ROW_AUTHORITY_ATTACHED__NOT_WHOLE_SUPPORT",
        ),
        delta_row(
            context_sha, double_stat, "R235_PRESERVED_NONGRAPH", 16, 16,
            "LOCAL_SOURCE_ONLY_DOUBLE_ENDPOINT_GRAPH_KEY_AUTHORITY_ONLY",
            "R235D_REPLACES_DEFERRED_ROW_AUTHORITY_DISPOSITION__UNIQUE_MEMBER_UNION_UNCHANGED",
        ),
    ]


def reconcile_gate5(held: HeldPins, context_sha: str) -> list[dict[str, Any]]:
    result = validate_envelope(held.json("R147_CERT"), "R147_CERT")
    field_rows = get_rows(result, "gate5_field_rows")
    frontier_rows = get_rows(result, "executable_upgrade_frontier")
    fields = raw_table_stat("R147_GATE5_FIELDS", field_rows, "field")
    frontier = raw_table_stat("R147_EXECUTABLE_FRONTIER", frontier_rows, "target")
    need(len(field_rows) == 18 and len(frontier_rows) == 4, "Gate5 raw census")
    satisfied = sum(type(row.get("global_field_credit")) is bool and row["global_field_credit"] for row in field_rows)
    blocked = sum(type(row.get("global_field_credit")) is bool and not row["global_field_credit"] for row in field_rows)
    need((satisfied, blocked) == (10, 8), "Gate5 10/18 split")
    return [
        delta_row(
            context_sha, fields, "GATE5_R147", 18, 0,
            "GLOBAL_FIELD_STATUS_RECEIPT__EIGHT_FIELDS_STRICTLY_BLOCKED",
            "TEN_OF_EIGHTEEN_FIELDS_SATISFIED__NO_COMPLETE_18_FIELD_GLOBAL_BLOCK",
        ),
        delta_row(
            context_sha, frontier, "GATE5_R147", 4, 0,
            "EXECUTABLE_UPGRADE_FRONTIER_RECEIPT_ONLY",
            "ZERO_AUTOMATIC_GATE5_UPGRADES",
        ),
    ]


def materialize_member_rows(
    members: dict[str, dict[str, Any]],
    i4_rows: dict[str, dict[str, Any]],
    evidence: dict[str, Evidence],
    context_sha: str,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    receipt_members: set[str] = set()
    local_members: set[str] = set()
    incidence_members: set[str] = set()
    receipt_fine = Counter()
    local_fine = Counter()
    for member_id in sorted(members, key=lambda x: x.encode("ascii")):
        source = members[member_id]
        global_row = i4_rows[member_id]
        ev = evidence[member_id]
        summary = ev.summary()
        has_receipt = any(summary["receipt_lanes"][lane]["row_count"] for lane in summary["receipt_lanes"])
        has_local = any(summary["narrow_local_authority_lanes"][lane]["row_count"] for lane in summary["narrow_local_authority_lanes"])
        has_incidence = bool(summary["local_incidence_attachment_count"])
        if has_receipt:
            receipt_members.add(member_id)
            receipt_fine[source["fine_family"]] += 1
        if has_local:
            local_members.add(member_id)
            local_fine[source["fine_family"]] += 1
        if has_incidence:
            incidence_members.add(member_id)
        rows.append(make_row(
            "member-reconciliation", "member_id", member_id,
            {
                "global_context_sha256": context_sha,
                "I2_member_row_sha256": source["row_sha256"],
                "I2_member_row_canonical_sha256": hashlib.sha256(canonical_bytes(source)).hexdigest(),
                "I4_global_member_row_sha256": global_row["row_sha256"],
                "I4_global_member_row_canonical_sha256": hashlib.sha256(canonical_bytes(global_row)).hexdigest(),
                "receipt_and_narrow_local_evidence": summary,
            },
            {
                "coarse_family": source["coarse_family"],
                "fine_family": source["fine_family"],
                "direct_construction_package": source["direct_construction_package"],
                "direct_construction_row_id": source["direct_construction_row_id"],
                "primary_representation_id": source["primary_representation_id"],
                "receipt_attachment": has_receipt,
                "narrow_local_authority_attachment": has_local,
                "local_incidence_attachment": has_incidence,
                "receipt_attachment_is_normalized_full_support": False,
                "narrow_local_authority_is_whole_support": False,
                "normalized_full_support_credit": 0,
                "representation_pullback_credit": 0,
                "A1_A2_theorem_credit": 0,
                "B1A_credit": 0,
                "B2_credit": 0,
                "CM2_credit": 0,
                "status": (
                    "NARROW_LOCAL_AUTHORITY_ATTACHED__FULL_SUPPORT_NOT_PROVED"
                    if has_local else
                    "RECEIPT_ATTACHED_ONLY__FULL_SUPPORT_NOT_PROVED"
                    if has_receipt else
                    "NO_DIRECT_RECEIPT_ATTACHMENT__FULL_SUPPORT_NOT_PROVED"
                ),
            },
        ))
    need(len(rows) == 144_296, "member output count")
    need((len(receipt_members), len(rows) - len(receipt_members)) == (69_892, 74_404), "member receipt split")
    need((len(local_members), len(rows) - len(local_members)) == (35_356, 108_940), "member narrow-local split")
    need(len(incidence_members) == 464, "member local incidence count")
    return rows, {
        "member_count": len(rows),
        "receipt_attached_member_count": len(receipt_members),
        "receipt_unattached_member_count": len(rows) - len(receipt_members),
        "narrow_local_authority_member_count": len(local_members),
        "narrow_local_authority_unattached_member_count": len(rows) - len(local_members),
        "local_incidence_attachment_member_count": len(incidence_members),
        "receipt_attached_fine_family_counts": dict(sorted(receipt_fine.items())),
        "narrow_local_authority_fine_family_counts": dict(sorted(local_fine.items())),
        "receipt_attached_member_ids_sha256": sha(sorted(receipt_members)),
        "narrow_local_authority_member_ids_sha256": sha(sorted(local_members)),
    }


def materialize_representation_rows(
    held: HeldPins,
    members: dict[str, dict[str, Any]],
    evidence: dict[str, Evidence],
    context_sha: str,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    source_rows: dict[str, dict[str, Any]] = {}
    for row in held.iter_jsonl_gzip("I2_REP"):
        row_sha(row)
        rep_id = row.get("representation_id")
        need(type(rep_id) is str and rep_id not in source_rows, "I2 representation key")
        owner = row.get("owner_member_id")
        need(owner in members, "I2 representation owner anti-join")
        source_rows[rep_id] = row
    need(len(source_rows) == 183_572, "I2 representation count")

    global_rows: dict[str, dict[str, Any]] = {}
    non_i2_seen = False
    for row in held.iter_jsonl_gzip("I4_REP"):
        row_sha(row)
        if row.get("source_lane") != "I2":
            non_i2_seen = True
            continue
        need(not non_i2_seen, "I4 I2 representation lane order")
        rep_id = row.get("representation_id")
        source = source_rows.get(rep_id)
        need(source is not None and rep_id not in global_rows, "I2/I4 representation anti-join")
        commitment = row.get("canonical_input_commitment")
        need(type(commitment) is dict, "I4 representation input commitment")
        need(commitment.get("source_representation_row_sha256") == source["row_sha256"], "I4/I2 representation SHA")
        need(commitment.get("source_representation_row_canonical_sha256") == hashlib.sha256(canonical_bytes(source)).hexdigest(), "I4/I2 representation canonical SHA")
        need(row.get("owner_member_id") == source["owner_member_id"], "I4/I2 representation owner")
        global_rows[rep_id] = row
    need(set(global_rows) == set(source_rows), "I2/I4 representation exact anti-join")

    rows: list[dict[str, Any]] = []
    receipt_reps: set[str] = set()
    local_reps: set[str] = set()
    for rep_id in sorted(source_rows, key=lambda x: x.encode("ascii")):
        source = source_rows[rep_id]
        global_row = global_rows[rep_id]
        owner = source["owner_member_id"]
        ev = evidence[owner]
        has_receipt = any(ev.receipt_ids.values())
        has_local = any(ev.local_ids.values())
        if has_receipt:
            receipt_reps.add(rep_id)
        if has_local:
            local_reps.add(rep_id)
        rows.append(make_row(
            "representation-reconciliation", "representation_id", rep_id,
            {
                "global_context_sha256": context_sha,
                "I2_representation_row_sha256": source["row_sha256"],
                "I2_representation_row_canonical_sha256": hashlib.sha256(canonical_bytes(source)).hexdigest(),
                "I4_global_representation_row_sha256": global_row["row_sha256"],
                "I4_global_representation_row_canonical_sha256": hashlib.sha256(canonical_bytes(global_row)).hexdigest(),
                "owner_member_id": owner,
                "owner_receipt_attachment": has_receipt,
                "owner_narrow_local_authority_attachment": has_local,
            },
            {
                "owner_member_id": owner,
                "owner_coarse_family": source["owner_coarse_family"],
                "representation_role": source["representation_role"],
                "source_kind": source["source_kind"],
                "owner_receipt_attachment": has_receipt,
                "owner_narrow_local_authority_attachment": has_local,
                "representation_set_equality_credit": 0,
                "representation_pullback_credit": 0,
                "normalized_full_support_credit": 0,
                "B1A_credit": 0,
                "B2_credit": 0,
                "CM2_credit": 0,
                "status": "OWNER_RECEIPT_AXIS_RECONCILED__REPRESENTATION_EQUALITY_AND_PULLBACK_NOT_PROVED",
            },
        ))
    need((len(receipt_reps), len(rows) - len(receipt_reps)) == (108_416, 75_156), "representation receipt split")
    need((len(local_reps), len(rows) - len(local_reps)) == (53_980, 129_592), "representation narrow-local split")
    return rows, {
        "representation_count": len(rows),
        "receipt_attached_representation_count": len(receipt_reps),
        "receipt_unattached_representation_count": len(rows) - len(receipt_reps),
        "narrow_owner_representation_count": len(local_reps),
        "narrow_owner_unattached_representation_count": len(rows) - len(local_reps),
        "representation_set_equality_credit_count": 0,
        "representation_pullback_credit_count": 0,
        "receipt_attached_representation_ids_sha256": sha(sorted(receipt_reps)),
        "narrow_owner_representation_ids_sha256": sha(sorted(local_reps)),
    }


def make_gap_rows(context_sha: str, axis: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for blocker_id, statement in P1_BLOCKERS:
        is_b06 = blocker_id.startswith("B06_")
        rows.append(make_row(
            "gap", "gap_id", blocker_id,
            {
                "global_context_sha256": context_sha,
                "P1_blocker_id": blocker_id,
                "P1_blocker_statement": statement,
                "axis_census_sha256": sha(axis),
            },
            {
                "blocker_statement": statement,
                "status": (
                    "DIRECT_RECEIPT_FRONTIER_DELTA_PUBLISHED__B06_NOT_DISCHARGED"
                    if is_b06 else "UNCHANGED_STRICT_BLOCKER"
                ),
                "receipt_frontier_delta_row_count": 20 if is_b06 else 0,
                "receipt_attachment_is_theorem_evidence": False,
                "normalized_full_support_credit": 0,
                "representation_set_equality_credit": 0,
                "representation_pullback_credit": 0,
                "A1_A2_theorem_credit": 0,
                "B1A_credit": 0,
                "B2_credit": 0,
                "CM2_credit": 0,
            },
        ))
    return rows


def install_outputs(temp_dir: str, output_dir: Path, filenames: Iterable[str]) -> None:
    before = os.stat(output_dir, follow_symlinks=False)
    need(stat.S_ISDIR(before.st_mode), "output directory")
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(os.fspath(output_dir), flags)
    try:
        need(dir_fp(os.fstat(fd)) == dir_fp(before), "output directory open race")
        for filename in filenames:
            src = os.path.join(temp_dir, filename)
            staging = filename + ".k2p2-staging"
            try:
                os.unlink(staging, dir_fd=fd)
            except FileNotFoundError:
                pass
            with open(src, "rb") as incoming:
                out_fd = os.open(
                    staging,
                    os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_CLOEXEC", 0),
                    0o644,
                    dir_fd=fd,
                )
                try:
                    with os.fdopen(out_fd, "wb", closefd=False) as outgoing:
                        shutil.copyfileobj(incoming, outgoing, IO_CHUNK)
                        outgoing.flush()
                        os.fsync(outgoing.fileno())
                finally:
                    os.close(out_fd)
            os.replace(staging, filename, src_dir_fd=fd, dst_dir_fd=fd)
        os.fsync(fd)
        need(dir_fp(os.fstat(fd)) == dir_fp(before), "output directory changed")
        need(dir_fp(os.stat(output_dir, follow_symlinks=False)) == dir_fp(before), "output directory path replaced")
    finally:
        os.close(fd)


def build_artifacts(seed: int, output_dir: Path | None, no_write: bool) -> dict[str, Any]:
    del seed  # Deliberately irrelevant; byte identity across seeds is required.
    source_size1, source_sha1 = file_sha(__file__)
    p1_baseline = {
        "member_AST_row_count": 144_296,
        "member_AST_commitment_sha256": "5f47287e601eeb2b56d2b390b04086f192c29fb3d15043ee1e34deb664316cf4",
        "alias_row_count": 46_564,
        "alias_commitment_sha256": "47a514ba806e8235be7a48db776de7d9f8c155360572bfac35a5c43d03dec50c",
        "A1_A2_obligation_count": 80_092,
        "A1_A2_obligation_commitment_sha256": "efe1f28d2789d3a23024439a23522450dd1fbc200a9cfb1b4e79c27a94a5e146",
        "replay_digest_sha256": "c93084485d1231118fc50e9d54f39da05714e23d9929feba6235ce61b8c1646c",
        "interpretation": "INDEPENDENT_P1_REPLAY_BASELINE__OBLIGATION_CENSUS_IS_NOT_FEATURE_LEDGER_ROW_COUNT",
    }
    with HeldPins() as held:
        receipt_documents = validate_latest_receipts(held)
        global_context = {
            "domain": SCHEMA + ".global-input-context.v1",
            "producer": {
                "filename": os.path.basename(__file__),
                "exact_size": source_size1,
                "sha256": source_sha1,
            },
            "exact_input_pins": [
                {
                    "label": pin.label,
                    "filename": pin.filename,
                    "exact_size": pin.exact_size,
                    "sha256": pin.sha256,
                    "role": pin.role,
                }
                for pin in PINS
            ],
            "P1_independent_replay_baseline": p1_baseline,
            "authority_axes": {
                "receipt_attachment": "BYTE_BOUND_RECEIPT_OR_ROW_COMMITMENT_ATTACHED_TO_IDENTITY_ONLY",
                "narrow_local_authority": "LOCAL_PATCH_INCIDENCE_OWNER_OR_KEY_SCOPE_ONLY",
                "theorem_credit": "ZERO_UNLESS_COMPLETE_INPUT_BOUND_SUPPORT_OR_EQUIVALENCE_THEOREM_EXISTS",
            },
        }
        context_sha = sha(global_context)
        members, evidence, i4_member_rows = load_i2_and_i4_members(held)
        retained_to_member, r234_to_member, _r236_to_member = load_non_graph_backlinks(held, members)
        obligation_rows, delta_rows = reconcile_r209_and_obligations(held, members, evidence, context_sha)
        delta_rows.extend(reconcile_r230(held, members, evidence, context_sha))
        delta_rows.extend(reconcile_r231_r233(held, members, evidence, retained_to_member, context_sha))
        delta_rows.extend(reconcile_r235(held, evidence, r234_to_member, context_sha))
        delta_rows.extend(reconcile_gate5(held, context_sha))
        need(len(delta_rows) == 20, "direct-receipt-frontier delta row count")
        delta_rows.sort(key=lambda row: row["delta_row_id"].encode("ascii"))

        member_rows, member_axis = materialize_member_rows(members, i4_member_rows, evidence, context_sha)
        representation_rows, representation_axis = materialize_representation_rows(held, members, evidence, context_sha)
        obligation_axis = {
            "A1_A2_obligation_count": len(obligation_rows),
            "local_dimensional_owner_authority_attachment_count": sum(row["local_dimensional_owner_authority_attachment"] is True for row in obligation_rows),
            "R204_unattached_obligation_count": sum(row["local_dimensional_owner_authority_attachment"] is False for row in obligation_rows),
            "A1_A2_theorem_credit_count": 0,
        }
        need(obligation_axis == {
            "A1_A2_obligation_count": 80_092,
            "local_dimensional_owner_authority_attachment_count": 79_084,
            "R204_unattached_obligation_count": 1_008,
            "A1_A2_theorem_credit_count": 0,
        }, "obligation axis")
        axis = {
            "member_axis": member_axis,
            "representation_axis": representation_axis,
            "A1_A2_axis": obligation_axis,
            "full_support_theorem_axis": {
                "normalized_full_support_member_credit_count": 0,
                "representation_set_equality_credit_count": 0,
                "representation_pullback_credit_count": 0,
                "A1_A2_theorem_credit_count": 0,
            },
        }
        gap_rows = make_gap_rows(context_sha, axis)
        source_size2, source_sha2 = file_sha(__file__)
        need((source_size2, source_sha2) == (source_size1, source_sha1), "producer changed during replay")
        held.final()

        with ExplicitTmp() as temp_dir:
            ledger_specs = (
                ("member", member_rows, "member_id"),
                ("representation", representation_rows, "representation_id"),
                ("obligation", obligation_rows, "obligation_id"),
                ("delta", delta_rows, "delta_row_id"),
                ("gap", gap_rows, "gap_id"),
            )
            ledger_results: dict[str, dict[str, Any]] = {}
            for label, rows, id_field in ledger_specs:
                writer = GzipLedger(temp_dir, OUTPUT_NAMES[label], id_field)
                for row in rows:
                    writer.add(row)
                ledger_results[label] = writer.close()

            result = {
                "schema": SCHEMA + ".result-body.v1",
                "status": "PASS_DIRECT_RECEIPT_FRONTIER_RECONCILED__ZERO_FULL_SUPPORT_THEOREM_CREDIT",
                "artifact_kind": "THREE_AXIS_ZERO_CREDIT_RECONCILIATION",
                "seed_affects_output": False,
                "producer_byte_binding": {
                    "filename": os.path.basename(__file__),
                    "exact_size": source_size1,
                    "sha256": source_sha1,
                    "pre_and_post_replay_equal": True,
                },
                "global_input_context": global_context,
                "global_input_context_sha256": context_sha,
                "receipt_document_checks": receipt_documents,
                "held_input_pins": held.receipts,
                "exact_three_axis_census": axis,
                "direct_receipt_frontier_delta": {
                    "row_count": len(delta_rows),
                    "ordered_row_ids_sha256": sha([row["delta_row_id"] for row in delta_rows]),
                    "B06_disposition": "DELTA_PUBLISHED__NOT_DISCHARGED_OR_CLOSED",
                    "P0_B01_through_B05": "RETAINED_UNCHANGED",
                },
                "Gate5": {
                    "maturity": "10/18",
                    "strictly_blocked_field_count": 8,
                    "complete_independently_verified_18_field_global_block_count": 0,
                    "Gate5_credit": 0,
                },
                "semantic_firewall": {
                    "receipt_attachment_is_support_coverage": False,
                    "narrow_local_authority_is_whole_support": False,
                    "local_patch_incidence_owner_or_key_is_member_full_support": False,
                    "R231_engineering_receipt_is_semantic_authority": False,
                    "R235D_16_authority_rows_are_112_unique_member_gap": False,
                    "R235D_unique_member_union_changed": False,
                    "formal_credit": dict(ZERO_CREDIT),
                },
                "P1_baseline": p1_baseline,
                "ledgers": ledger_results,
                "gap_count": len(gap_rows),
                "normalized_full_support_status": "ZERO_OF_144296_IN_THIS_SCOPE",
                "representation_equality_and_pullback_status": "ZERO_OF_183572_IN_THIS_SCOPE",
                "A1_A2_theorem_status": "ZERO_OF_80092__79084_LOCAL_OWNER_ATTACHMENTS_ONLY",
                "B1A_credit": 0,
                "B2_credit": 0,
                "CM2_credit": 0,
            }
            typed_zero_credit(result)
            envelope = {
                "schema": SCHEMA + ".result.v1",
                "result": result,
                "result_sha256": sha(result),
            }
            result_path = os.path.join(temp_dir, OUTPUT_NAMES["result"])
            with open(result_path, "xb") as stream:
                stream.write(canonical_bytes(envelope) + b"\n")
            result_size, result_file_sha = file_sha(result_path)
            envelope["result_file_size"] = result_size
            envelope["result_file_sha256"] = result_file_sha
            if not no_write:
                destination = output_dir if output_dir is not None else INPUT_DIRECTORY
                install_outputs(temp_dir, destination, OUTPUT_NAMES.values())
            return envelope


def contract() -> dict[str, Any]:
    return {
        "schema": SCHEMA + ".contract.v1",
        "status": FINAL_PIN_GATE if not PINS else "READY_EXACT_PIN_TABLE",
        "old_freeze_invalidation_audit": dict(OLD_FREEZE_INVALIDATION_AUDIT),
        "scope": {
            "count_authority": "OLD_B0_I2_I4_FREEZE_RECONCILIATION_EXPECTATION_ONLY__MUST_RECOMPUTE_AFTER_ANY_FRESH_FREEZE",
            "members": 144_296,
            "representations": 183_572,
            "A1_A2_obligations": 80_092,
            "receipt_attached_members_expected": 69_892,
            "receipt_unattached_members_expected": 74_404,
            "narrow_local_authority_members_expected": 35_356,
            "narrow_local_authority_unattached_members_expected": 108_940,
            "receipt_attached_representations_expected": 108_416,
            "narrow_owner_representations_expected": 53_980,
            "local_dimensional_owner_authority_obligations_expected": 79_084,
            "R204_unattached_obligations_expected": 1_008,
        },
        "semantic_firewall": {
            "receipt_attachment_is_support_coverage": False,
            "narrow_local_authority_is_whole_support": False,
            "local_patch_is_member": False,
            "local_incidence_is_member": False,
            "owner_or_key_is_whole_support": False,
            "R231_engineering_receipt_is_semantic_authority": False,
            "R235_authority_row_gap_is_unique_member_gap": False,
            "R235D_target_sheet_or_target_only_side_conflict_may_be_silently_absorbed": False,
            "I4_manifest_53b84967_is_currently_authorized_as_formal_pin": False,
            "fresh_B0_I2_I4_replay_required_if_target_zero_set_is_empty": True,
            "formal_credit": dict(ZERO_CREDIT),
        },
        "input_security": {
            "held_directory_and_file_descriptors": True,
            "two_initial_and_one_final_full_sha256_passes": True,
            "path_fd_identity_before_after_and_final": True,
            "O_NOFOLLOW": True,
            "nlink_must_equal_one": True,
            "post_canonical_row_cap_bytes": ROW_CAP,
            "temporary_root_literal": TMP_ROOT,
            "TMPDIR_consulted": False,
        },
        "outputs": dict(OUTPUT_NAMES),
        "pin_count": len(PINS),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", action="store_true")
    parser.add_argument("--seed", type=int)
    parser.add_argument("--output-dir")
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args(argv)
    if args.contract:
        print(json.dumps(contract(), sort_keys=True, separators=(",", ":")))
        return 0
    need(type(args.seed) is int, "explicit integer seed required")
    need(bool(PINS), FINAL_PIN_GATE)
    if args.no_write:
        need(args.output_dir is None, "--no-write forbids --output-dir")
        destination = None
    else:
        destination = Path(args.output_dir) if args.output_dir else INPUT_DIRECTORY
    envelope = build_artifacts(args.seed, destination, args.no_write)
    print(json.dumps(envelope, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
