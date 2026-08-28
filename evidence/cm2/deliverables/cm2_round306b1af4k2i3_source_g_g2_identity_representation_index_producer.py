#!/usr/bin/env python3
"""Strict zero-credit G2a/G2b mechanical identity/representation index.

This producer consumes only byte-pinned, already frozen G1/K2G0/B1G0/B0
authorities.  It emits exact identity and current one-to-one representation
candidates, keeps all sixteen duplicate G2b references explicitly, and emits
semantic-gap plus transition-handle ledgers.  It does not promote graph
envelopes, joins, or handles to full-support, incidence, pullback, transition,
B1A, B2, maximality, or CM2 theorem credit.
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
import stat
import tempfile
from typing import Any, BinaryIO, Iterable, Iterator, TextIO


class Blocked(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise Blocked(label)


PREFIX = "cm2_round306b1af4k2i3_source_g_g2_identity_representation_index_"
SCHEMA = "cm2.round306b1af4k2i3.source-g-g2-identity-representation-index.v1"
STATUS = "PASS_G2_MECHANICAL_IDENTITY_REPRESENTATION_INDEX__SEMANTIC_GAPS_NONZERO__ZERO_FORMAL_CREDIT"
DELIVERABLES = Path(__file__).resolve().parent
HEX64 = re.compile(r"^[0-9a-f]{64}$")
MAX_DECODED_CANONICAL_ROW_BYTES = 8 << 20
STREAM_READ_CHUNK_CHARACTERS = 1 << 18
MAX_READ_CHUNK_UTF8_BYTES = 4 * STREAM_READ_CHUNK_CHARACTERS
MAX_PARSER_BUFFER_UTF8_BYTES = MAX_DECODED_CANONICAL_ROW_BYTES + MAX_READ_CHUNK_UTF8_BYTES

INPUT_PINS: tuple[tuple[str, str, int, str], ...] = (
    ("K2G0_RESULT", "cm2_round306b1af4k2g0_source_g_g2_semantic_authority_frontier_result.json", 1_523, "eb1e2fdf2985b142eb6c4c53a585757d74ce787f7b74d8ba95c652de80b291d1"),
    ("K2G0_LEDGER", "cm2_round306b1af4k2g0_source_g_g2_semantic_authority_frontier_ledger.json", 18_862, "af0d3a52c916224826d766388d585b02e35a8ea20597fe78e72eb0e9fbfa9ccd"),
    ("G1_PREFLIGHT", "cm2_round306b1af4g1_source_g_g2_exact_join_preflight.py", 92_288, "fce556387520b6e27af9ba5d6e816e91325a629750855af0fffae36dfdba765d"),
    ("B1G0_RESULT", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_result.json", 5_006, "3f494ebc9f046bfe9f42aef16edeadaece099d7ba7547b11f07484e3f6d81b9e"),
    ("B1G0_SHEET", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_sheet_join.json.gz", 13_922_080, "041328aa135a1a67cbbdc8c5d84fe2c1a9bef2231a6cb33668ab05ecd6b227e3"),
    ("B1G0_SIDE", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_side_join.json.gz", 25_932_945, "d79af13182f99cdb2df6d39731e762b0d145baf79772b99be5069669c5b80ee1"),
    ("B1G0_MEMBER", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_b0_member_backbinding.json.gz", 32_731_854, "79382a6d8c3d086aeb29eff9fcb8653f2a73d85d79aab27e71e72cc8b1165a0b"),
    ("B0_RESULT", "cm2_round306b0_source_g_r306a_universe_support_source_freeze_result.json", 9_450, "badc000c6fadd8807b26a7c3511edc51796c962f150b438956e4c549fd0d5735"),
    ("B0_MEMBER", "cm2_round306b0_source_g_r306a_universe_support_source_freeze_member_support_source_index.json.gz", 162_499_140, "c9a8649c8473bb6a170187e7f803e95748d2ff2198b1b846d97383dd5f0581af"),
)

EXPECTED_TABLES = {
    "B1G0_SHEET": (38_624, "9238a05af9a97002488576d3648ce06ee750858f156638c314ba2e0a24fe3e1f"),
    "B1G0_SIDE": (76_848, "43ee8ffd2b77231c43c0af10198bbcc1f1def12f2e6bfd28f82c66ea26a207b2"),
    "B1G0_MEMBER": (115_456, "35189ef67c69078e44bbd440be37ef870935a8fd67817501ae995cceae383ea6"),
    "B0_MEMBER": (564_492, "c7dfb5534fddeb22fffb81bf539fe44d837aced46577aa5f490a0ae14aba77f5"),
}

OUTPUTS = {
    "member": PREFIX + "member_index.jsonl.gz",
    "representation": PREFIX + "representation_index.jsonl.gz",
    "duplicate_reference": PREFIX + "duplicate_reference_disposition.jsonl.gz",
    "semantic_gap": PREFIX + "semantic_obligation_gap_index.jsonl.gz",
    "transition_handle": PREFIX + "transition_ready_handle_index.jsonl.gz",
    "result": PREFIX + "result.json",
}


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def strict_equal(left: Any, right: Any) -> bool:
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return left.keys() == right.keys() and all(strict_equal(left[key], right[key]) for key in left)
    if type(left) is list:
        return len(left) == len(right) and all(strict_equal(a, b) for a, b in zip(left, right))
    return left == right


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in out, "duplicate JSON key:" + key)
        out[key] = value
    return out


def reject_number(token: str) -> Any:
    raise Blocked("nonintegral JSON token:" + token)


DECODER = json.JSONDecoder(object_pairs_hook=unique_object, parse_float=reject_number, parse_constant=reject_number)


def check_closed_row(row: Any, label: str) -> str:
    need(type(row) is dict and type(row.get("row_sha256")) is str, label + ":closed row")
    body = dict(row)
    claimed = body.pop("row_sha256")
    need(HEX64.fullmatch(claimed) is not None and digest(body) == claimed, label + ":row sha")
    return claimed


def close_row(body: dict[str, Any]) -> dict[str, Any]:
    need("row_sha256" not in body, "preclosed output row")
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


def stat_fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink, value.st_size, value.st_mtime_ns, value.st_ctime_ns)


def directory_identity(value: os.stat_result) -> tuple[int, int, int]:
    return (value.st_dev, value.st_ino, value.st_mode)


def hash_fd(fd: int, expected_size: int) -> tuple[int, str]:
    state = hashlib.sha256()
    offset = 0
    while True:
        block = os.pread(fd, 1 << 20, offset)
        if not block:
            break
        offset += len(block)
        need(offset <= expected_size, "held FD grew")
        state.update(block)
    return offset, state.hexdigest()


def path_within(path: str, directory: str) -> bool:
    try:
        return os.path.commonpath((path, directory)) == directory
    except ValueError:
        return False


class PinnedInputs:
    def __init__(self, directory: Path) -> None:
        self.directory = str(directory)
        self.dirfd = -1
        self.dir_before: os.stat_result | None = None
        self.files: dict[str, tuple[int, os.stat_result, int, str, str]] = {}
        self.pin_rows: list[dict[str, Any]] = []

    def __enter__(self) -> "PinnedInputs":
        named = os.stat(self.directory, follow_symlinks=False)
        need(stat.S_ISDIR(named.st_mode), "deliverables real directory")
        self.dirfd = os.open(self.directory, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
        self.dir_before = os.fstat(self.dirfd)
        need(directory_identity(named) == directory_identity(self.dir_before), "deliverables held-dirfd binding")
        try:
            for label, filename, size, sha in INPUT_PINS:
                before = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
                need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and before.st_size == size, "single-link size pin:" + label)
                fd = os.open(filename, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0), dir_fd=self.dirfd)
                opened = os.fstat(fd)
                need(stat_fingerprint(before) == stat_fingerprint(opened), "path/open race:" + label)
                observed_size, observed_sha = hash_fd(fd, size)
                need(observed_size == size and observed_sha == sha, "first byte pin:" + label)
                self.files[label] = (fd, opened, size, sha, filename)
                self.pin_rows.append({"label": label, "filename": filename, "exact_size": size, "sha256": sha, "pass1_sha256": observed_sha, "regular": True, "nlink_one": True})
            return self
        except Exception:
            self.close(False)
            raise

    def stream(self, label: str, marker: str) -> Iterator[Any]:
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
            need(stat_fingerprint(os.fstat(fd)) == stat_fingerprint(before), "held FD stable after parse:" + label)

    def small_json(self, label: str) -> Any:
        fd, before, _, _, _ = self.files[label]
        need(before.st_size <= MAX_DECODED_CANONICAL_ROW_BYTES, "small JSON cap:" + label)
        raw = os.pread(fd, before.st_size, 0)
        need(len(raw) == before.st_size, "small JSON short read:" + label)
        value = DECODER.decode(raw.decode("utf-8"))
        need(len(canonical(value)) <= MAX_DECODED_CANONICAL_ROW_BYTES, "small JSON canonical cap:" + label)
        return value

    def close(self, verify: bool = True) -> None:
        error: Exception | None = None
        for label, (fd, before, size, sha, filename) in list(self.files.items()):
            try:
                if verify:
                    n2, h2 = hash_fd(fd, size)
                    named = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
                    need(n2 == size and h2 == sha, "final held-FD rehash:" + label)
                    need(stat_fingerprint(before) == stat_fingerprint(os.fstat(fd)) == stat_fingerprint(named), "final path/FD binding:" + label)
                    for pin in self.pin_rows:
                        if pin["label"] == label:
                            pin["pass2_sha256"] = h2
                            pin["final_path_bound"] = True
            except Exception as exc:
                error = error or exc
            finally:
                os.close(fd)
        self.files.clear()
        if self.dirfd >= 0:
            try:
                if verify:
                    assert self.dir_before is not None
                    need(directory_identity(self.dir_before) == directory_identity(os.fstat(self.dirfd)) == directory_identity(os.stat(self.directory, follow_symlinks=False)), "deliverables directory replaced")
            except Exception as exc:
                error = error or exc
            finally:
                os.close(self.dirfd)
                self.dirfd = -1
        if error is not None:
            raise error

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.close(exc_type is None)


def iter_array(stream: TextIO, marker: str) -> Iterator[Any]:
    def append(buffer: str, label: str) -> str:
        block = stream.read(STREAM_READ_CHUNK_CHARACTERS)
        need(bool(block), label)
        combined = buffer + block
        need(len(combined.encode("utf-8")) <= MAX_PARSER_BUFFER_UTF8_BYTES, "parser buffer cap")
        return combined

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
        buffer = buffer[-max(len(marker) - 1, 1):]
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
                need(len(buffer.encode("utf-8")) <= MAX_DECODED_CANONICAL_ROW_BYTES, "incomplete row cap")
                buffer = append(buffer, "truncated JSON row")
        need(len(buffer[:end].encode("utf-8")) <= MAX_DECODED_CANONICAL_ROW_BYTES, "successful source row cap")
        need(len(canonical(value)) <= MAX_DECODED_CANONICAL_ROW_BYTES, "successful canonical row cap")
        yield value
        buffer = buffer[end:]
        comma = True


def table_finish(label: str, stream: ListHash) -> dict[str, Any]:
    count, sha = EXPECTED_TABLES[label]
    observed = stream.finish()
    need(stream.count == count and observed == sha, label + ":ordered table commitment")
    return {"table": label, "row_count": count, "rows_sha256": observed, "all_rows_own_sha256_checked": True}


def zero_credit() -> dict[str, int]:
    return {"normalized_support": 0, "representation_cover": 0, "A1_A2": 0, "physical_incidence": 0, "pullback_equivalence": 0, "graph_definition": 0, "transition": 0, "B1A": 0, "B2": 0, "maximality": 0, "fibre": 0, "global_disposition": 0, "D02": 0, "CM2": 0}


def raw_input_commitment(member_id: str, family: str, source: dict[str, Any], refs: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "domain": "CM2_ROUND306B1AF4K2I3_G2_RAW_INPUT_COMMITMENT_V1",
        "coarse_family": family,
        "member_id": member_id,
        "B0": {"component_id": source["component_id"], "row_id": source["b0_row_id"], "row_sha256": source["b0_row_sha256"]},
        "B1G0_backbinding": {"row_id": source["b1_row_id"], "row_sha256": source["b1_row_sha256"]},
        "primitive_source": {"package": source["package"], "table": source["table"], "row_sha256": source["source_row_sha256"]},
        "graph_references": sorted(refs, key=lambda row: row["ref_row_id"].encode("ascii")),
    }


def member_body(member_id: str, family: str, source: dict[str, Any], refs: list[dict[str, Any]]) -> dict[str, Any]:
    commitment = raw_input_commitment(member_id, family, source, refs)
    return {
        "schema": SCHEMA + ".member-row",
        "status": "MECHANICAL_IDENTITY_JOINED__NO_FULL_SUPPORT_CREDIT",
        "coarse_family": family,
        "member_id": member_id,
        "Round306A_component_id": source["component_id"],
        "source_B0_row_id": source["b0_row_id"],
        "source_B0_row_sha256": source["b0_row_sha256"],
        "source_B1G0_backbinding_row_id": source["b1_row_id"],
        "source_B1G0_backbinding_row_sha256": source["b1_row_sha256"],
        "primitive_source": {"package": source["package"], "table": source["table"], "row_sha256": source["source_row_sha256"]},
        "graph_reference_count": len(refs),
        "graph_reference_row_ids": sorted((ref["ref_row_id"] for ref in refs), key=lambda value: value.encode("ascii")),
        "canonical_raw_input_commitment_sha256": digest(commitment),
        "formal_credit": zero_credit(),
    }


def representation_body(member_id: str, family: str, source: dict[str, Any], refs: list[dict[str, Any]]) -> dict[str, Any]:
    commitment_sha = digest(raw_input_commitment(member_id, family, source, refs))
    representation_id = "round306b1af4k2i3-g2-current-representation:" + digest({"domain":"CURRENT_REPRESENTATION_HANDLE_V1","raw_input_commitment_sha256":commitment_sha})
    return {
        "schema": SCHEMA + ".representation-row",
        "status": "CURRENT_ONE_TO_ONE_IDENTITY_CANDIDATE__SET_EQUALITY_NOT_PROVED",
        "coarse_family": family,
        "representation_id": representation_id,
        "owner_member_id": member_id,
        "representation_kind": "G2A_GRAPH_SHEET_IDENTITY" if family == "G2A" else "G2B_GRAPH_SIDE_IDENTITY",
        "source_graph_ids": sorted({ref["graph_id"] for ref in refs}, key=lambda value: value.encode("ascii")),
        "source_reference_row_ids": sorted((ref["ref_row_id"] for ref in refs), key=lambda value: value.encode("ascii")),
        "canonical_raw_input_commitment_sha256": commitment_sha,
        "coverage_semantics": "IDENTITY_INDEX_ONLY__NOT_NORMALIZED_SUPPORT_OR_REPRESENTATION_COVER",
        "formal_credit": zero_credit(),
    }


def duplicate_body(member_id: str, source: dict[str, Any], refs: list[dict[str, Any]]) -> dict[str, Any]:
    ordered = sorted(refs, key=lambda row: row["ref_row_id"].encode("ascii"))
    commitment_sha = digest(raw_input_commitment(member_id, "G2B", source, refs))
    return {
        "schema": SCHEMA + ".duplicate-reference-disposition-row",
        "status": "TWO_REFERENCES_TO_ONE_B0_IDENTITY__PHYSICAL_EQUIVALENCE_NOT_PROVED",
        "member_id": member_id,
        "reference_count": 2,
        "reference_rows": ordered,
        "same_primitive_source_row": len({row["source_row_sha256"] for row in ordered}) == 1,
        "identity_disposition": "EXPLICIT_ALIAS_REFERENCE_EXCESS_ONE",
        "canonical_raw_input_commitment_sha256": commitment_sha,
        "physical_equivalence_credit": 0,
        "formal_credit": zero_credit(),
    }


def gap_body(member_id: str, family: str, source: dict[str, Any], refs: list[dict[str, Any]]) -> dict[str, Any]:
    kinds = ["DISTINCT_MEMBER_FULL_SUPPORT_EQUALITY", "REPRESENTATION_PULLBACK_EQUIVALENCE"]
    if family == "G2A":
        kinds.extend(["SOURCE_FREE_GRAPH_DEFINITION", "GRAPH_SHEET_PHYSICAL_INCIDENCE"])
    else:
        kinds.append("GRAPH_SIDE_PHYSICAL_INCIDENCE_REFERENCE")
        if len(refs) == 2:
            kinds.append("DUPLICATE_REFERENCE_PHYSICAL_EQUIVALENCE")
    commitment_sha = digest(raw_input_commitment(member_id, family, source, refs))
    handles = ["round306b1af4k2i3-gap:" + digest({"domain":"SEMANTIC_GAP_HANDLE_V1","kind":kind,"raw_input_commitment_sha256":commitment_sha}) for kind in kinds]
    return {
        "schema": SCHEMA + ".semantic-gap-row",
        "status": "SEMANTIC_OBLIGATIONS_ENUMERATED_NOT_DISCHARGED",
        "member_id": member_id,
        "coarse_family": family,
        "physical_incidence_reference_count": len(refs),
        "obligation_kinds": kinds,
        "obligation_handles": handles,
        "canonical_raw_input_commitment_sha256": commitment_sha,
        "unresolved_semantic_gap": True,
        "formal_credit": zero_credit(),
    }


def transition_body(member_id: str, family: str, source: dict[str, Any], refs: list[dict[str, Any]]) -> dict[str, Any]:
    graph_ids = sorted({ref["graph_id"] for ref in refs}, key=lambda value: value.encode("ascii"))
    roles = sorted({ref["role"] for ref in refs}, key=lambda value: value.encode("ascii"))
    commitment_sha = digest(raw_input_commitment(member_id, family, source, refs))
    handle_payload = {"domain":"TRANSITION_READY_HANDLE_V1","coarse_family":family,"graph_ids":graph_ids,"member_id":member_id,"raw_input_commitment_sha256":commitment_sha,"roles":roles}
    return {
        "schema": SCHEMA + ".transition-ready-handle-row",
        "status": "CANONICAL_SYNTAX_HANDLE_ONLY__TRANSITION_SEMANTICS_NOT_PROVED",
        "member_id": member_id,
        "coarse_family": family,
        "graph_ids": graph_ids,
        "side_or_sheet_roles": roles,
        "canonical_handle_sha256": digest(handle_payload),
        "canonical_raw_input_commitment_sha256": commitment_sha,
        "transition_ready_syntax": True,
        "transition_semantics_ready": False,
        "formal_credit": zero_credit(),
    }


def checked_scratch() -> tuple[str, str, tuple[int, int, int], int]:
    deliverables_real = os.path.realpath(DELIVERABLES)
    root = "/tmp"
    need(os.path.realpath(root) == root and not path_within(root, deliverables_real), "explicit scratch root")
    info = os.stat(root, follow_symlinks=False)
    need(stat.S_ISDIR(info.st_mode), "scratch root directory")
    fd = os.open(root, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
    need(directory_identity(info) == directory_identity(os.fstat(fd)), "scratch root held-dirfd binding")
    return root, deliverables_real, directory_identity(info), fd


def write_jsonl_gzip(path: Path, rows: Iterable[dict[str, Any]], expected_count: int) -> dict[str, Any]:
    raw_sha = hashlib.sha256()
    raw_size = 0
    count = 0
    with path.open("xb") as target:
        with gzip.GzipFile(filename="", mode="wb", fileobj=target, compresslevel=9, mtime=0) as zipped:
            for row in rows:
                wire = canonical(row) + b"\n"
                raw_sha.update(wire)
                raw_size += len(wire)
                count += 1
                zipped.write(wire)
        target.flush()
        os.fsync(target.fileno())
    need(count == expected_count, "output row count:" + path.name)
    named = os.stat(path, follow_symlinks=False)
    need(stat.S_ISREG(named.st_mode) and named.st_nlink == 1, "staged ledger regular single-link")
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
    try:
        opened = os.fstat(fd)
        need(stat_fingerprint(named) == stat_fingerprint(opened), "staged ledger path/open")
        file_size, file_sha = hash_fd(fd, named.st_size)
        need(stat_fingerprint(opened) == stat_fingerprint(os.fstat(fd)) == stat_fingerprint(os.stat(path, follow_symlinks=False)), "staged ledger final binding")
    finally:
        os.close(fd)
    return {"filename": path.name, "row_count": count, "uncompressed_jsonl_size": raw_size, "uncompressed_jsonl_sha256": raw_sha.hexdigest(), "file_size": file_size, "file_sha256": file_sha, "order": "unsigned_bytewise_ASCII_by_member_id"}


def produce(output_directory: Path, _seed: str) -> dict[str, Any]:
    output_directory = Path(os.path.abspath(output_directory))
    output_named = os.stat(output_directory, follow_symlinks=False)
    need(stat.S_ISDIR(output_named.st_mode), "real output directory")
    output_dirfd = os.open(output_directory, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
    output_held = os.fstat(output_dirfd)
    need(directory_identity(output_named) == directory_identity(output_held), "output held-dirfd binding")
    sheet: dict[str, list[dict[str, Any]]] = {}
    side: dict[str, list[dict[str, Any]]] = {}
    backbinding: dict[str, dict[str, Any]] = {}
    b0: dict[str, dict[str, Any]] = {}
    source_tables: list[dict[str, Any]] = []

    with PinnedInputs(DELIVERABLES) as pins:
        k2g0 = pins.small_json("K2G0_RESULT")
        need(type(k2g0) is dict and k2g0.get("status") == "PASS_EXACT_G2_AUTHORITY_FRONTIER__SEMANTIC_GAPS_NONZERO__ZERO_FORMAL_CREDIT", "K2G0 status")
        need(strict_equal(k2g0.get("exact_census"), {"G2_distinct_members":115456,"G2_representations_current_exact_index_candidate":115456,"G2a_R245":264,"G2a_R248":38360,"G2a_members":38624,"G2b_R245_distinct_members":528,"G2b_R245_references":528,"G2b_R248_distinct_members":76304,"G2b_R248_references":76320,"G2b_distinct_members":76832,"G2b_references":76848,"duplicate_side_reference_excess":16}), "K2G0 exact census")
        need(k2g0.get("semantic_gaps", {}).get("unresolved_semantic_gap_zero") is False, "K2G0 gap boundary")
        need(all(type(value) is int and not isinstance(value, bool) and value == 0 for value in k2g0.get("formal_credit", {}).values()), "K2G0 zero credits")
        k2g0_ledger = pins.small_json("K2G0_LEDGER")
        need(k2g0_ledger.get("status") == "PASS_EXACT_G2_AUTHORITY_FRONTIER__SEMANTIC_GAPS_NONZERO__ZERO_FORMAL_CREDIT", "K2G0 ledger status")
        b1result = pins.small_json("B1G0_RESULT")
        need(b1result.get("audit", {}).get("distinct_B0_member_backbinding_count") == 115_456, "B1G0 member census")
        need(b1result.get("audit", {}).get("graph_sheet_join_count") == 38_624 and b1result.get("audit", {}).get("graph_side_join_count") == 76_848, "B1G0 join census")
        need(b1result.get("strict_boundary", {}).get("all_output_formal_credit_zero") is True, "B1G0 zero-credit boundary")
        b0result = pins.small_json("B0_RESULT")
        need(b0result.get("member_universe", {}).get("member_count") == 564_492 and b0result.get("member_universe", {}).get("virtual_sheet_count") == 38_624, "B0 denominator")

        audit = ListHash()
        for row in pins.stream("B1G0_SHEET", '"graph_sheet_join_rows"'):
            check_closed_row(row, "B1G0 sheet")
            audit.add(row)
            member_id = row.get("sheet_member_id")
            need(type(member_id) is str and member_id not in sheet, "unique sheet member")
            need(row.get("physical_incidence_proved") is False and row.get("official_key_used_as_join_or_routing_filter") is False, "sheet semantic boundary")
            sheet[member_id] = [{"ref_row_id": row["Round306B1G0_graph_sheet_join_row_id"], "ref_row_sha256": row["row_sha256"], "graph_id": row["graph_id"], "graph_family": row["graph_family"], "role": "SHEET", "branch": row["endpoint_factor"], "source_package": row["sheet_source_package"], "source_row_sha256": row["sheet_source_row_sha256"], "b1_backbinding_row_id": row["B0_member_backbinding_row_id"], "b0_row_id": row["Round306B0_member_support_source_row_id"]}]
        source_tables.append(table_finish("B1G0_SHEET", audit))

        audit = ListHash()
        for row in pins.stream("B1G0_SIDE", '"graph_side_join_rows"'):
            check_closed_row(row, "B1G0 side")
            audit.add(row)
            member_id = row.get("side_member_id")
            need(type(member_id) is str, "side member id")
            need(row.get("physical_incidence_proved") is False and row.get("official_key_used_as_join_or_routing_filter") is False, "side semantic boundary")
            side.setdefault(member_id, []).append({"ref_row_id": row["Round306B1G0_graph_side_join_row_id"], "ref_row_sha256": row["row_sha256"], "graph_id": row["graph_id"], "graph_family": row["graph_family"], "role": row["side_role"], "branch": row["side_branch_label"], "source_package": row["side_source_package"], "source_row_sha256": row["side_source_row_sha256"], "b1_backbinding_row_id": row["B0_member_backbinding_row_id"], "b0_row_id": row["Round306B0_member_support_source_row_id"]})
        source_tables.append(table_finish("B1G0_SIDE", audit))
        need(len(sheet) == 38_624 and len(side) == 76_832 and set(sheet).isdisjoint(side), "G2a/G2b exact partition")
        multiplicities = Counter(len(refs) for refs in side.values())
        need(multiplicities == Counter({1: 76_816, 2: 16}), "G2b multiplicity histogram")
        duplicate_members = {member_id for member_id, refs in side.items() if len(refs) == 2}
        need(len(duplicate_members) == 16, "duplicate member census")

        target_members = set(sheet) | set(side)
        audit = ListHash()
        for row in pins.stream("B1G0_MEMBER", '"b0_member_backbinding_rows"'):
            check_closed_row(row, "B1G0 member")
            audit.add(row)
            member_id = row.get("member_id")
            need(type(member_id) is str and member_id in target_members and member_id not in backbinding, "B1G0 exact member identity")
            refs = sheet.get(member_id, side.get(member_id))
            assert refs is not None
            need(all(ref["b1_backbinding_row_id"] == row["Round306B1G0_B0_member_backbinding_row_id"] and ref["b0_row_id"] == row["Round306B0_member_support_source_row_id"] for ref in refs), "reference/backbinding join")
            need(all(ref["source_package"] == row["feature_source_package"] and ref["source_row_sha256"] == row["feature_source_row_sha256"] for ref in refs), "primitive source join")
            need(row.get("formal_credit") == {"fibre":0,"full_support":0,"global_disposition":0,"graph_definition":0,"maximality":0,"physical_incidence":0}, "B1G0 member zero credit")
            backbinding[member_id] = {"component_id": row["Round306A_component_id"], "b0_row_id": row["Round306B0_member_support_source_row_id"], "b0_row_sha256": row["Round306B0_member_support_source_row_sha256"], "b1_row_id": row["Round306B1G0_B0_member_backbinding_row_id"], "b1_row_sha256": row["row_sha256"], "package": row["feature_source_package"], "table": row["feature_source_table"], "source_row_sha256": row["feature_source_row_sha256"]}
        source_tables.append(table_finish("B1G0_MEMBER", audit))
        need(set(backbinding) == target_members, "B1G0 member anti-join")

        audit = ListHash()
        for row in pins.stream("B0_MEMBER", '"member_support_source_rows"'):
            check_closed_row(row, "B0 member")
            audit.add(row)
            member_id = row.get("member_id")
            if member_id not in target_members:
                continue
            need(member_id not in b0, "duplicate B0 G2 member")
            source = backbinding[member_id]
            need(row["Round306B0_member_support_source_row_id"] == source["b0_row_id"] and row["row_sha256"] == source["b0_row_sha256"], "B0/B1G0 row binding")
            need(row["Round306A_component_id"] == source["component_id"], "B0 component binding")
            b0[member_id] = {"row_id": row["Round306B0_member_support_source_row_id"], "row_sha256": row["row_sha256"]}
        source_tables.append(table_finish("B0_MEMBER", audit))
        need(set(b0) == target_members, "B0 G2 exact anti-join")
        pin_rows = pins.pin_rows

    ordered_members = sorted(target_members, key=lambda value: value.encode("ascii"))
    ordered_duplicates = sorted(duplicate_members, key=lambda value: value.encode("ascii"))
    def family_refs(member_id: str) -> tuple[str, list[dict[str, Any]]]:
        return ("G2A", sheet[member_id]) if member_id in sheet else ("G2B", side[member_id])

    scratch_root, deliverables_real, root_identity, scratch_root_fd = checked_scratch()
    try:
        with tempfile.TemporaryDirectory(prefix="cm2-k2i3-g2-", dir=scratch_root) as scratch_name:
            scratch_real = os.path.realpath(scratch_name)
            need(os.path.dirname(scratch_real) == scratch_root and not path_within(scratch_real, deliverables_real), "scratch placement")
            need(directory_identity(os.fstat(scratch_root_fd)) == root_identity == directory_identity(os.stat(scratch_root, follow_symlinks=False)), "scratch root changed")
            scratch = Path(scratch_real)
            scratch_named = os.stat(scratch, follow_symlinks=False)
            scratch_dirfd = os.open(scratch, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
            need(directory_identity(scratch_named) == directory_identity(os.fstat(scratch_dirfd)), "staging held-dirfd binding")
            ledger_meta = {
                "member": write_jsonl_gzip(scratch / OUTPUTS["member"], (close_row(member_body(mid, family_refs(mid)[0], backbinding[mid], family_refs(mid)[1])) for mid in ordered_members), 115_456),
                "representation": write_jsonl_gzip(scratch / OUTPUTS["representation"], (close_row(representation_body(mid, family_refs(mid)[0], backbinding[mid], family_refs(mid)[1])) for mid in ordered_members), 115_456),
                "duplicate_reference": write_jsonl_gzip(scratch / OUTPUTS["duplicate_reference"], (close_row(duplicate_body(mid, backbinding[mid], side[mid])) for mid in ordered_duplicates), 16),
                "semantic_gap": write_jsonl_gzip(scratch / OUTPUTS["semantic_gap"], (close_row(gap_body(mid, family_refs(mid)[0], backbinding[mid], family_refs(mid)[1])) for mid in ordered_members), 115_456),
                "transition_handle": write_jsonl_gzip(scratch / OUTPUTS["transition_handle"], (close_row(transition_body(mid, family_refs(mid)[0], backbinding[mid], family_refs(mid)[1])) for mid in ordered_members), 115_456),
            }
            result = {
                "schema": SCHEMA,
                "status": STATUS,
                "scope": "G2A_G2B_MECHANICAL_PARTIAL_LANE",
                "producer_sha256": None,
                "producer_byte_binding": "EXTERNAL_INDEPENDENT_VERIFIER_STATIC_PIN_ONLY",
                "seed_affects_output": False,
                "input_pins": pin_rows,
                "source_table_commitments": source_tables,
                "exact_census": {"G2a_members":38_624,"G2a_references":38_624,"G2b_members":76_832,"G2b_references":76_848,"G2_distinct_members":115_456,"current_one_to_one_representation_candidates":115_456,"duplicate_reference_members":16,"duplicate_reference_excess":16,"physical_incidence_references_pending":115_472,"side_reference_multiplicity_histogram":{"1":76_816,"2":16}},
                "ledgers": ledger_meta,
                "closed_anti_joins": {"sheet_duplicate_members":0,"sheet_side_member_intersection":0,"B1G0_references_without_B0_identity":0,"B0_G2_identities_without_B1G0_reference":0,"B1G0_backbindings_without_B0_row":0,"duplicate_reference_rows_lost":0,"orphan_representation_candidates":0,"orphan_transition_handles":0},
                "known_gaps": {"source_free_graph_definition_pending":38_624,"graph_sheet_physical_incidence_pending":38_624,"graph_side_physical_incidence_reference_pending":76_848,"distinct_member_full_support_equalities_pending":115_456,"representation_pullback_theorems_pending":115_456,"duplicate_reference_physical_equivalence_pending":16,"A1_A2_not_discharged":80_092,"transition_semantics_not_discharged":115_456,"unresolved_semantic_gap_zero":False},
                "strict_boundary": {"graph_envelope_is_full_support":False,"B1G0_join_is_physical_incidence_theorem":False,"current_representation_candidate_is_representation_cover":False,"transition_handle_is_transition_theorem":False,"candidate_is_formal":False},
                "formal_credit": zero_credit(),
            }
            result_path = scratch / OUTPUTS["result"]
            with result_path.open("xb") as handle:
                handle.write(canonical(result) + b"\n")
                handle.flush()
                os.fsync(handle.fileno())
            for key in ("member", "representation", "duplicate_reference", "semantic_gap", "transition_handle", "result"):
                source_info = os.stat(OUTPUTS[key], dir_fd=scratch_dirfd, follow_symlinks=False)
                need(stat.S_ISREG(source_info.st_mode) and source_info.st_nlink == 1, "staged regular single-link:" + key)
                os.replace(OUTPUTS[key], OUTPUTS[key], src_dir_fd=scratch_dirfd, dst_dir_fd=output_dirfd)
                published = os.stat(OUTPUTS[key], dir_fd=output_dirfd, follow_symlinks=False)
                need(stat.S_ISREG(published.st_mode) and published.st_nlink == 1 and published.st_size == source_info.st_size, "published regular single-link:" + key)
            os.fsync(output_dirfd)
            need(directory_identity(os.fstat(output_dirfd)) == directory_identity(output_named) == directory_identity(os.stat(output_directory, follow_symlinks=False)), "output directory final binding")
            need(directory_identity(os.fstat(scratch_dirfd)) == directory_identity(scratch_named), "staging final binding")
            os.close(scratch_dirfd)
        need(directory_identity(os.fstat(scratch_root_fd)) == root_identity == directory_identity(os.stat(scratch_root, follow_symlinks=False)), "scratch root final binding")
        return result
    finally:
        os.close(scratch_root_fd)
        os.close(output_dirfd)


def self_test() -> dict[str, Any]:
    need(strict_equal(False, 0) is False and strict_equal(True, 1) is False, "bool/int strictness")
    row = close_row({"x": "a"})
    need(check_closed_row(row, "self") == row["row_sha256"], "row closure")
    bad = dict(row)
    bad["x"] = "b"
    rejected = False
    try:
        check_closed_row(bad, "mutation")
    except Blocked:
        rejected = True
    need(rejected, "mutation rejected")
    exact_body = {"x": "a" * (MAX_DECODED_CANONICAL_ROW_BYTES - len(canonical({"x": ""})))}
    exact_wire = canonical(exact_body)
    need(len(exact_wire) == MAX_DECODED_CANONICAL_ROW_BYTES, "exact cap fixture")
    need(list(iter_array(io.StringIO('{"rows":' + b"[".decode() + exact_wire.decode("ascii") + "]}"), '"rows"')) == [exact_body], "cap accepted")
    rejected_cap = False
    try:
        overflow = {"x": exact_body["x"] + "a"}
        list(iter_array(io.StringIO('{"rows":[' + canonical(overflow).decode("ascii") + "]}"), '"rows"'))
    except Blocked:
        rejected_cap = True
    need(rejected_cap, "cap plus one rejected")
    source = {"component_id":"c","b0_row_id":"b0","b0_row_sha256":"0"*64,"b1_row_id":"b1","b1_row_sha256":"1"*64,"package":"P","table":"T","source_row_sha256":"2"*64}
    ref1 = {"ref_row_id":"r1","ref_row_sha256":"3"*64,"graph_id":"g","graph_family":"F","role":"SHEET","branch":"x","source_package":"P","source_row_sha256":"2"*64,"b1_backbinding_row_id":"b1","b0_row_id":"b0"}
    ref2 = dict(ref1)
    ref2["ref_row_sha256"] = "4" * 64
    h1 = transition_body("m", "G2A", source, [ref1])["canonical_handle_sha256"]
    h2 = transition_body("m", "G2A", source, [ref2])["canonical_handle_sha256"]
    need(h1 != h2, "raw input commitment must change handle")
    return {"schema":SCHEMA+".self-test","status":"PASS","false_equals_zero_rejected":True,"true_equals_one_rejected":True,"decoded_row_cap":MAX_DECODED_CANONICAL_ROW_BYTES,"cap_plus_one_rejected":True,"different_raw_inputs_produce_different_handles":True,"candidate_is_formal":False}


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
    need(type(args.output_directory) is str, "output directory required")
    result = produce(Path(args.output_directory), args.hash_seed)
    print(canonical({"status":result["status"],"result_object_sha256":digest(result)}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
