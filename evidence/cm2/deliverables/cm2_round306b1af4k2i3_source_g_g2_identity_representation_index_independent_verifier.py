#!/usr/bin/env python3
"""Independent verifier and receipt minter for the K2I3 G2 index lane.

The verifier never imports the producer.  It pins all authorities and package
artifacts, independently reconstructs expected rows from B1G0/B0, executes two
cold producer processes through a held producer file descriptor, compares all
bytes, runs type/commitment/filesystem attacks, and writes the manifest last.
All theorem credit remains zero.
"""

from __future__ import annotations

import argparse
from collections import Counter
import copy
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
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
VERIFICATION_SCHEMA = SCHEMA + ".independent-verification.v1"
DATA = Path(__file__).resolve().parent
HEX64 = re.compile(r"^[0-9a-f]{64}$")
MAX_DECODED_CANONICAL_ROW_BYTES = 8 << 20
STREAM_READ_CHUNK_CHARACTERS = 1 << 18
MAX_READ_CHUNK_UTF8_BYTES = 4 * STREAM_READ_CHUNK_CHARACTERS
MAX_PARSER_BUFFER_UTF8_BYTES = MAX_DECODED_CANONICAL_ROW_BYTES + MAX_READ_CHUNK_UTF8_BYTES

PRODUCER = PREFIX + "producer.py"
VERIFIER = PREFIX + "independent_verifier.py"
OUTPUTS = {
    "member": PREFIX + "member_index.jsonl.gz",
    "representation": PREFIX + "representation_index.jsonl.gz",
    "duplicate_reference": PREFIX + "duplicate_reference_disposition.jsonl.gz",
    "semantic_gap": PREFIX + "semantic_obligation_gap_index.jsonl.gz",
    "transition_handle": PREFIX + "transition_ready_handle_index.jsonl.gz",
    "result": PREFIX + "result.json",
}
RECEIPTS = {
    "attack": PREFIX + "attack_suite.json",
    "verification": PREFIX + "verification.json",
    "report": PREFIX + "report.md",
    "cold": PREFIX + "cold_replay.md",
    "manifest": PREFIX + "manifest.sha256",
}

SOURCE_PINS: tuple[tuple[str, str, int, str], ...] = (
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

PACKAGE_PINS: tuple[tuple[str, str, int, str], ...] = (
    ("PRODUCER", PRODUCER, 39_121, "e32f6cbd9f2fa164827c5fbe1d03c5be7d832031248a1b0553acdbe86566a542"),
    ("OUT_MEMBER", OUTPUTS["member"], 43_492_152, "e2b8b047cc5d6733825585f981f870db2cbcd9a977e96aa272e8ab74813d9575"),
    ("OUT_REPRESENTATION", OUTPUTS["representation"], 28_586_094, "f6b7b71a8cfef8e78f800ba2a4f5848f5f13d0fd6fc8c198dde92768e3f1fac3"),
    ("OUT_DUPLICATE", OUTPUTS["duplicate_reference"], 8_414, "e86d08a6ff5cd1d3bb1bb41f4309723e53f61e1fd6dca321cd5f269e2d5e67cb"),
    ("OUT_GAP", OUTPUTS["semantic_gap"], 30_054_605, "b8423f532a60880d2188d39047372c666173f49587053fa771722f6949617837"),
    ("OUT_TRANSITION", OUTPUTS["transition_handle"], 23_996_169, "27dfb6aeb0f6c336e16f12d5a3ca329ef1199f9c2ced1fbc2218ce4209ced725"),
    ("OUT_RESULT", OUTPUTS["result"], 8_648, "ad2b74c0d886513efdee1d7a0c0d6346f4dd5d13584ce98822556f19fdc5ae5a"),
)

EXPECTED_TABLES = {
    "B1G0_SHEET": (38_624, "9238a05af9a97002488576d3648ce06ee750858f156638c314ba2e0a24fe3e1f"),
    "B1G0_SIDE": (76_848, "43ee8ffd2b77231c43c0af10198bbcc1f1def12f2e6bfd28f82c66ea26a207b2"),
    "B1G0_MEMBER": (115_456, "35189ef67c69078e44bbd440be37ef870935a8fd67817501ae995cceae383ea6"),
    "B0_MEMBER": (564_492, "c7dfb5534fddeb22fffb81bf539fe44d837aced46577aa5f490a0ae14aba77f5"),
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
    result: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in result, "duplicate JSON key:" + key)
        result[key] = value
    return result


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


class Snapshot:
    def __init__(self, directory: Path) -> None:
        self.directory = str(directory)
        self.dirfd = -1
        self.dir_before: os.stat_result | None = None
        self.files: dict[str, tuple[int, os.stat_result, int, str, str]] = {}
        self.self_entry: tuple[int, os.stat_result, int, str, str] | None = None

    def __enter__(self) -> "Snapshot":
        named = os.stat(self.directory, follow_symlinks=False)
        need(stat.S_ISDIR(named.st_mode), "deliverables real directory")
        self.dirfd = os.open(self.directory, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
        self.dir_before = os.fstat(self.dirfd)
        need(directory_identity(named) == directory_identity(self.dir_before), "deliverables dirfd binding")
        try:
            for label, filename, size, sha in SOURCE_PINS + PACKAGE_PINS:
                before = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
                need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and before.st_size == size, "regular single-link size pin:" + label)
                fd = os.open(filename, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0), dir_fd=self.dirfd)
                opened = os.fstat(fd)
                need(stat_fingerprint(before) == stat_fingerprint(opened), "path/open race:" + label)
                n, h = hash_fd(fd, size)
                need(n == size and h == sha, "static byte pin:" + label)
                self.files[label] = (fd, opened, size, sha, filename)
            before = os.stat(VERIFIER, dir_fd=self.dirfd, follow_symlinks=False)
            need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "verifier regular single-link")
            fd = os.open(VERIFIER, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0), dir_fd=self.dirfd)
            opened = os.fstat(fd)
            need(stat_fingerprint(before) == stat_fingerprint(opened), "verifier path/open race")
            n, h = hash_fd(fd, before.st_size)
            self.self_entry = (fd, opened, n, h, VERIFIER)
            return self
        except Exception:
            self.close(False)
            raise

    def stream(self, label: str, marker: str) -> Iterator[Any]:
        fd, before, _, _, filename = self.files[label]
        raw = os.fdopen(os.dup(fd), "rb")
        binary: BinaryIO = gzip.GzipFile(fileobj=raw, mode="rb") if filename.endswith(".gz") else raw
        text = io.TextIOWrapper(binary, encoding="utf-8", newline="")
        try:
            yield from iter_array(text, marker)
        finally:
            text.close()
            if not raw.closed:
                raw.close()
            need(stat_fingerprint(os.fstat(fd)) == stat_fingerprint(before), "source stable after parse:" + label)

    def small_json(self, label: str) -> Any:
        fd, before, _, _, _ = self.files[label]
        need(before.st_size <= MAX_DECODED_CANONICAL_ROW_BYTES, "small JSON cap:" + label)
        raw = os.pread(fd, before.st_size, 0)
        value = DECODER.decode(raw.decode("utf-8"))
        if label == "OUT_RESULT":
            need(raw == canonical(value) + b"\n", "canonical small JSON wire:" + label)
        return value

    def output_rows(self, label: str) -> Iterator[Any]:
        fd, before, _, _, _ = self.files[label]
        raw = os.fdopen(os.dup(fd), "rb")
        zipped = gzip.GzipFile(fileobj=raw, mode="rb")
        try:
            for line in zipped:
                need(line.endswith(b"\n") and len(line) <= MAX_DECODED_CANONICAL_ROW_BYTES + 1, "JSONL row wire cap:" + label)
                row = DECODER.decode(line[:-1].decode("ascii"))
                need(line == canonical(row) + b"\n", "canonical JSONL wire:" + label)
                check_closed_row(row, label)
                yield row
        finally:
            zipped.close()
            raw.close()
            need(stat_fingerprint(os.fstat(fd)) == stat_fingerprint(before), "output stable after parse:" + label)

    def close(self, verify: bool = True) -> None:
        error: Exception | None = None
        for label, (fd, before, size, sha, filename) in list(self.files.items()):
            try:
                if verify:
                    n, h = hash_fd(fd, size)
                    named = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
                    need(n == size and h == sha, "final held-FD hash:" + label)
                    need(stat_fingerprint(before) == stat_fingerprint(os.fstat(fd)) == stat_fingerprint(named), "final path/FD binding:" + label)
            except Exception as exc:
                error = error or exc
            finally:
                os.close(fd)
        self.files.clear()
        if self.self_entry is not None:
            fd, before, size, sha, filename = self.self_entry
            try:
                if verify:
                    n, h = hash_fd(fd, size)
                    named = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
                    need(n == size and h == sha and stat_fingerprint(before) == stat_fingerprint(os.fstat(fd)) == stat_fingerprint(named), "verifier final binding")
            except Exception as exc:
                error = error or exc
            finally:
                os.close(fd)
            self.self_entry = None
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
    buffer = buffer.lstrip()
    if buffer.startswith(":"):
        buffer = buffer[1:].lstrip()
    need(buffer.startswith("["), "marker not array")
    buffer = buffer[1:]
    comma = False
    while True:
        buffer = buffer.lstrip()
        while not buffer:
            buffer = append(buffer, "truncated array").lstrip()
        if buffer[0] == "]":
            return
        if comma:
            need(buffer[0] == ",", "missing comma")
            buffer = buffer[1:].lstrip()
            while not buffer:
                buffer = append(buffer, "truncated row").lstrip()
            need(buffer[0] != "]", "trailing comma")
        while True:
            try:
                value, end = DECODER.raw_decode(buffer)
                break
            except json.JSONDecodeError:
                need(len(buffer.encode("utf-8")) <= MAX_DECODED_CANONICAL_ROW_BYTES, "incomplete row cap")
                buffer = append(buffer, "truncated JSON row")
        need(len(buffer[:end].encode("utf-8")) <= MAX_DECODED_CANONICAL_ROW_BYTES, "successful source cap")
        need(len(canonical(value)) <= MAX_DECODED_CANONICAL_ROW_BYTES, "successful canonical cap")
        yield value
        buffer = buffer[end:]
        comma = True


def table_finish(label: str, stream: ListHash) -> dict[str, Any]:
    expected_count, expected_sha = EXPECTED_TABLES[label]
    observed = stream.finish()
    need(stream.count == expected_count and observed == expected_sha, "table commitment:" + label)
    return {"table":label,"row_count":expected_count,"rows_sha256":observed,"all_rows_own_sha256_checked":True}


def zero_credit() -> dict[str, int]:
    return {"normalized_support":0,"representation_cover":0,"A1_A2":0,"physical_incidence":0,"pullback_equivalence":0,"graph_definition":0,"transition":0,"B1A":0,"B2":0,"maximality":0,"fibre":0,"global_disposition":0,"D02":0,"CM2":0}


def raw_commitment(member_id: str, family: str, source: dict[str, Any], refs: list[dict[str, Any]]) -> dict[str, Any]:
    return {"domain":"CM2_ROUND306B1AF4K2I3_G2_RAW_INPUT_COMMITMENT_V1","coarse_family":family,"member_id":member_id,"B0":{"component_id":source["component_id"],"row_id":source["b0_row_id"],"row_sha256":source["b0_row_sha256"]},"B1G0_backbinding":{"row_id":source["b1_row_id"],"row_sha256":source["b1_row_sha256"]},"primitive_source":{"package":source["package"],"table":source["table"],"row_sha256":source["source_row_sha256"]},"graph_references":sorted(refs,key=lambda row:row["ref_row_id"].encode("ascii"))}


def expected_member(member_id: str, family: str, source: dict[str, Any], refs: list[dict[str, Any]]) -> dict[str, Any]:
    csha = digest(raw_commitment(member_id, family, source, refs))
    body = {"schema":SCHEMA+".member-row","status":"MECHANICAL_IDENTITY_JOINED__NO_FULL_SUPPORT_CREDIT","coarse_family":family,"member_id":member_id,"Round306A_component_id":source["component_id"],"source_B0_row_id":source["b0_row_id"],"source_B0_row_sha256":source["b0_row_sha256"],"source_B1G0_backbinding_row_id":source["b1_row_id"],"source_B1G0_backbinding_row_sha256":source["b1_row_sha256"],"primitive_source":{"package":source["package"],"table":source["table"],"row_sha256":source["source_row_sha256"]},"graph_reference_count":len(refs),"graph_reference_row_ids":sorted((r["ref_row_id"] for r in refs),key=lambda value:value.encode("ascii")),"canonical_raw_input_commitment_sha256":csha,"formal_credit":zero_credit()}
    return close_row(body)


def expected_representation(member_id: str, family: str, source: dict[str, Any], refs: list[dict[str, Any]]) -> dict[str, Any]:
    csha = digest(raw_commitment(member_id, family, source, refs))
    rid = "round306b1af4k2i3-g2-current-representation:" + digest({"domain":"CURRENT_REPRESENTATION_HANDLE_V1","raw_input_commitment_sha256":csha})
    body = {"schema":SCHEMA+".representation-row","status":"CURRENT_ONE_TO_ONE_IDENTITY_CANDIDATE__SET_EQUALITY_NOT_PROVED","coarse_family":family,"representation_id":rid,"owner_member_id":member_id,"representation_kind":"G2A_GRAPH_SHEET_IDENTITY" if family=="G2A" else "G2B_GRAPH_SIDE_IDENTITY","source_graph_ids":sorted({r["graph_id"] for r in refs},key=lambda value:value.encode("ascii")),"source_reference_row_ids":sorted((r["ref_row_id"] for r in refs),key=lambda value:value.encode("ascii")),"canonical_raw_input_commitment_sha256":csha,"coverage_semantics":"IDENTITY_INDEX_ONLY__NOT_NORMALIZED_SUPPORT_OR_REPRESENTATION_COVER","formal_credit":zero_credit()}
    return close_row(body)


def expected_duplicate(member_id: str, source: dict[str, Any], refs: list[dict[str, Any]]) -> dict[str, Any]:
    ordered = sorted(refs,key=lambda row:row["ref_row_id"].encode("ascii"))
    body = {"schema":SCHEMA+".duplicate-reference-disposition-row","status":"TWO_REFERENCES_TO_ONE_B0_IDENTITY__PHYSICAL_EQUIVALENCE_NOT_PROVED","member_id":member_id,"reference_count":2,"reference_rows":ordered,"same_primitive_source_row":len({r["source_row_sha256"] for r in ordered})==1,"identity_disposition":"EXPLICIT_ALIAS_REFERENCE_EXCESS_ONE","canonical_raw_input_commitment_sha256":digest(raw_commitment(member_id,"G2B",source,refs)),"physical_equivalence_credit":0,"formal_credit":zero_credit()}
    return close_row(body)


def expected_gap(member_id: str, family: str, source: dict[str, Any], refs: list[dict[str, Any]]) -> dict[str, Any]:
    kinds=["DISTINCT_MEMBER_FULL_SUPPORT_EQUALITY","REPRESENTATION_PULLBACK_EQUIVALENCE"]
    if family=="G2A": kinds += ["SOURCE_FREE_GRAPH_DEFINITION","GRAPH_SHEET_PHYSICAL_INCIDENCE"]
    else:
        kinds.append("GRAPH_SIDE_PHYSICAL_INCIDENCE_REFERENCE")
        if len(refs)==2: kinds.append("DUPLICATE_REFERENCE_PHYSICAL_EQUIVALENCE")
    csha=digest(raw_commitment(member_id,family,source,refs))
    handles=["round306b1af4k2i3-gap:"+digest({"domain":"SEMANTIC_GAP_HANDLE_V1","kind":kind,"raw_input_commitment_sha256":csha}) for kind in kinds]
    return close_row({"schema":SCHEMA+".semantic-gap-row","status":"SEMANTIC_OBLIGATIONS_ENUMERATED_NOT_DISCHARGED","member_id":member_id,"coarse_family":family,"physical_incidence_reference_count":len(refs),"obligation_kinds":kinds,"obligation_handles":handles,"canonical_raw_input_commitment_sha256":csha,"unresolved_semantic_gap":True,"formal_credit":zero_credit()})


def expected_transition(member_id: str, family: str, source: dict[str, Any], refs: list[dict[str, Any]]) -> dict[str, Any]:
    graphs=sorted({r["graph_id"] for r in refs},key=lambda value:value.encode("ascii")); roles=sorted({r["role"] for r in refs},key=lambda value:value.encode("ascii")); csha=digest(raw_commitment(member_id,family,source,refs))
    payload={"domain":"TRANSITION_READY_HANDLE_V1","coarse_family":family,"graph_ids":graphs,"member_id":member_id,"raw_input_commitment_sha256":csha,"roles":roles}
    return close_row({"schema":SCHEMA+".transition-ready-handle-row","status":"CANONICAL_SYNTAX_HANDLE_ONLY__TRANSITION_SEMANTICS_NOT_PROVED","member_id":member_id,"coarse_family":family,"graph_ids":graphs,"side_or_sheet_roles":roles,"canonical_handle_sha256":digest(payload),"canonical_raw_input_commitment_sha256":csha,"transition_ready_syntax":True,"transition_semantics_ready":False,"formal_credit":zero_credit()})


def reconstruct_sources(snapshot: Snapshot) -> tuple[dict[str,list[dict[str,Any]]],dict[str,list[dict[str,Any]]],dict[str,dict[str,Any]],list[dict[str,Any]]]:
    k2g0=snapshot.small_json("K2G0_RESULT")
    need(k2g0["status"]=="PASS_EXACT_G2_AUTHORITY_FRONTIER__SEMANTIC_GAPS_NONZERO__ZERO_FORMAL_CREDIT" and k2g0["exact_census"]["G2_distinct_members"]==115456 and k2g0["semantic_gaps"]["unresolved_semantic_gap_zero"] is False,"K2G0 boundary")
    need(all(type(v) is int and not isinstance(v,bool) and v==0 for v in k2g0["formal_credit"].values()),"K2G0 type-strict zero")
    k2ledger=snapshot.small_json("K2G0_LEDGER"); need(k2ledger["status"]==k2g0["status"],"K2G0 ledger status")
    b1result=snapshot.small_json("B1G0_RESULT"); need(b1result["audit"]["distinct_B0_member_backbinding_count"]==115456 and b1result["audit"]["graph_sheet_join_count"]==38624 and b1result["audit"]["graph_side_join_count"]==76848,"B1G0 census")
    need(b1result["strict_boundary"]["all_output_formal_credit_zero"] is True,"B1G0 boundary")
    b0result=snapshot.small_json("B0_RESULT"); need(b0result["member_universe"]["member_count"]==564492,"B0 denominator")
    tables=[]; sheet={}; side={}; back={}; b0={}
    audit=ListHash()
    for row in snapshot.stream("B1G0_SHEET",'"graph_sheet_join_rows"'):
        check_closed_row(row,"sheet"); audit.add(row); mid=row["sheet_member_id"]; need(type(mid) is str and mid not in sheet,"sheet unique"); need(row["physical_incidence_proved"] is False and row["official_key_used_as_join_or_routing_filter"] is False,"sheet boundary")
        sheet[mid]=[{"ref_row_id":row["Round306B1G0_graph_sheet_join_row_id"],"ref_row_sha256":row["row_sha256"],"graph_id":row["graph_id"],"graph_family":row["graph_family"],"role":"SHEET","branch":row["endpoint_factor"],"source_package":row["sheet_source_package"],"source_row_sha256":row["sheet_source_row_sha256"],"b1_backbinding_row_id":row["B0_member_backbinding_row_id"],"b0_row_id":row["Round306B0_member_support_source_row_id"]}]
    tables.append(table_finish("B1G0_SHEET",audit))
    audit=ListHash()
    for row in snapshot.stream("B1G0_SIDE",'"graph_side_join_rows"'):
        check_closed_row(row,"side"); audit.add(row); mid=row["side_member_id"]; need(type(mid) is str,"side id"); need(row["physical_incidence_proved"] is False and row["official_key_used_as_join_or_routing_filter"] is False,"side boundary")
        side.setdefault(mid,[]).append({"ref_row_id":row["Round306B1G0_graph_side_join_row_id"],"ref_row_sha256":row["row_sha256"],"graph_id":row["graph_id"],"graph_family":row["graph_family"],"role":row["side_role"],"branch":row["side_branch_label"],"source_package":row["side_source_package"],"source_row_sha256":row["side_source_row_sha256"],"b1_backbinding_row_id":row["B0_member_backbinding_row_id"],"b0_row_id":row["Round306B0_member_support_source_row_id"]})
    tables.append(table_finish("B1G0_SIDE",audit)); need(len(sheet)==38624 and len(side)==76832 and set(sheet).isdisjoint(side),"family partition"); need(Counter(map(len,side.values()))==Counter({1:76816,2:16}),"side multiplicity")
    target=set(sheet)|set(side); audit=ListHash()
    zero={"fibre":0,"full_support":0,"global_disposition":0,"graph_definition":0,"maximality":0,"physical_incidence":0}
    for row in snapshot.stream("B1G0_MEMBER",'"b0_member_backbinding_rows"'):
        check_closed_row(row,"backbinding"); audit.add(row); mid=row["member_id"]; need(type(mid) is str and mid in target and mid not in back,"backbinding exact")
        refs=sheet.get(mid,side.get(mid)); assert refs is not None
        need(all(r["b1_backbinding_row_id"]==row["Round306B1G0_B0_member_backbinding_row_id"] and r["b0_row_id"]==row["Round306B0_member_support_source_row_id"] and r["source_package"]==row["feature_source_package"] and r["source_row_sha256"]==row["feature_source_row_sha256"] for r in refs),"reference/backbinding join")
        need(strict_equal(row["formal_credit"],zero),"B1G0 type-strict credit")
        back[mid]={"component_id":row["Round306A_component_id"],"b0_row_id":row["Round306B0_member_support_source_row_id"],"b0_row_sha256":row["Round306B0_member_support_source_row_sha256"],"b1_row_id":row["Round306B1G0_B0_member_backbinding_row_id"],"b1_row_sha256":row["row_sha256"],"package":row["feature_source_package"],"table":row["feature_source_table"],"source_row_sha256":row["feature_source_row_sha256"]}
    tables.append(table_finish("B1G0_MEMBER",audit)); need(set(back)==target,"backbinding anti-join")
    audit=ListHash()
    for row in snapshot.stream("B0_MEMBER",'"member_support_source_rows"'):
        check_closed_row(row,"B0"); audit.add(row); mid=row["member_id"]
        if mid not in target: continue
        need(mid not in b0,"B0 duplicate"); source=back[mid]; need(row["Round306B0_member_support_source_row_id"]==source["b0_row_id"] and row["row_sha256"]==source["b0_row_sha256"] and row["Round306A_component_id"]==source["component_id"],"B0 binding"); b0[mid]=True
    tables.append(table_finish("B0_MEMBER",audit)); need(set(b0)==target,"B0 anti-join")
    return sheet,side,back,tables


def output_meta(snapshot: Snapshot, label: str, expected: Iterable[dict[str,Any]], expected_count: int) -> dict[str,Any]:
    state=hashlib.sha256(); size=0; count=0
    actual=snapshot.output_rows(label)
    for want in expected:
        try: got=next(actual)
        except StopIteration: raise Blocked(label+":missing row")
        need(strict_equal(got,want),label+":exact row mismatch:"+str(count))
        wire=canonical(got)+b"\n"; state.update(wire); size+=len(wire); count+=1
    try: next(actual); raise Blocked(label+":extra row")
    except StopIteration: pass
    need(count==expected_count,label+":row count")
    _,filename,file_size,file_sha=next((l,f,s,h) for l,f,s,h in PACKAGE_PINS if l==label)
    return {"filename":filename,"row_count":count,"uncompressed_jsonl_size":size,"uncompressed_jsonl_sha256":state.hexdigest(),"file_size":file_size,"file_sha256":file_sha,"order":"unsigned_bytewise_ASCII_by_member_id"}


def source_pin_rows() -> list[dict[str,Any]]:
    return [{"label":label,"filename":filename,"exact_size":size,"sha256":sha,"pass1_sha256":sha,"regular":True,"nlink_one":True,"pass2_sha256":sha,"final_path_bound":True} for label,filename,size,sha in SOURCE_PINS]


def expected_result(tables: list[dict[str,Any]],ledgers: dict[str,Any]) -> dict[str,Any]:
    return {"schema":SCHEMA,"status":STATUS,"scope":"G2A_G2B_MECHANICAL_PARTIAL_LANE","producer_sha256":None,"producer_byte_binding":"EXTERNAL_INDEPENDENT_VERIFIER_STATIC_PIN_ONLY","seed_affects_output":False,"input_pins":source_pin_rows(),"source_table_commitments":tables,"exact_census":{"G2a_members":38624,"G2a_references":38624,"G2b_members":76832,"G2b_references":76848,"G2_distinct_members":115456,"current_one_to_one_representation_candidates":115456,"duplicate_reference_members":16,"duplicate_reference_excess":16,"physical_incidence_references_pending":115472,"side_reference_multiplicity_histogram":{"1":76816,"2":16}},"ledgers":ledgers,"closed_anti_joins":{"sheet_duplicate_members":0,"sheet_side_member_intersection":0,"B1G0_references_without_B0_identity":0,"B0_G2_identities_without_B1G0_reference":0,"B1G0_backbindings_without_B0_row":0,"duplicate_reference_rows_lost":0,"orphan_representation_candidates":0,"orphan_transition_handles":0},"known_gaps":{"source_free_graph_definition_pending":38624,"graph_sheet_physical_incidence_pending":38624,"graph_side_physical_incidence_reference_pending":76848,"distinct_member_full_support_equalities_pending":115456,"representation_pullback_theorems_pending":115456,"duplicate_reference_physical_equivalence_pending":16,"A1_A2_not_discharged":80092,"transition_semantics_not_discharged":115456,"unresolved_semantic_gap_zero":False},"strict_boundary":{"graph_envelope_is_full_support":False,"B1G0_join_is_physical_incidence_theorem":False,"current_representation_candidate_is_representation_cover":False,"transition_handle_is_transition_theorem":False,"candidate_is_formal":False},"formal_credit":zero_credit()}


def compare_paths(left: Path,right: Path) -> None:
    a=os.stat(left,follow_symlinks=False); b=os.stat(right,follow_symlinks=False); need(stat.S_ISREG(a.st_mode) and stat.S_ISREG(b.st_mode) and a.st_nlink==b.st_nlink==1 and a.st_size==b.st_size,"replay file shape")
    with left.open("rb") as x,right.open("rb") as y:
        while True:
            xb=x.read(1<<20); yb=y.read(1<<20); need(xb==yb,"replay byte mismatch:"+left.name)
            if not xb: break


def cold_replay(snapshot: Snapshot) -> dict[str,Any]:
    producer_fd=snapshot.files["PRODUCER"][0]
    with tempfile.TemporaryDirectory(prefix="cm2-k2i3-verify-a-",dir="/tmp") as a, tempfile.TemporaryDirectory(prefix="cm2-k2i3-verify-b-",dir="/tmp") as b:
        dirs=[Path(a),Path(b)]; procs=[]
        for seed,target in (("17",dirs[0]),("93",dirs[1])):
            command=[sys.executable,"-I","-B",f"/proc/self/fd/{producer_fd}","--produce","--output-directory",str(target),"--hash-seed",seed]
            procs.append((seed,subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,pass_fds=(producer_fd,),text=False)))
        receipts=[]
        for seed,proc in procs:
            stdout,stderr=proc.communicate(); need(proc.returncode==0,"cold producer rc:"+seed); need(stderr==b"","cold producer stderr:"+seed)
            summary=DECODER.decode(stdout.decode("ascii")); need(summary["status"]==STATUS and summary["result_object_sha256"]=="34cc51c60b992890d1ccfdf784ed807c382dfaf34e82e84389e891ab1f598b81","cold producer stdout:"+seed)
            receipts.append({"seed":seed,"rc":proc.returncode,"stdout_sha256":hashlib.sha256(stdout).hexdigest(),"stderr_bytes":0})
        for filename in OUTPUTS.values():
            compare_paths(dirs[0]/filename,dirs[1]/filename); compare_paths(dirs[0]/filename,DATA/filename)
        return {"status":"PASS_TWO_SEED_BYTE_IDENTICAL_COLD_REPLAY","runs":receipts,"all_six_outputs_byte_identical":True,"producer_executed_via_held_fd":True,"producer_imported":False,"runtime_and_rss_measurements_in_canonical_receipt":False}


def attacks(result: dict[str,Any],first_member: dict[str,Any],first_transition: dict[str,Any],duplicate: dict[str,Any],source: dict[str,Any],refs: list[dict[str,Any]]) -> dict[str,Any]:
    cases: dict[str,bool]={}
    cases["recursive_false_not_zero"]=not strict_equal(False,0)
    cases["recursive_true_not_one"]=not strict_equal(True,1)
    mutated=copy.deepcopy(first_member); mutated["formal_credit"]["CM2"]=False; cases["ledger_false_for_zero_rejected"]=not strict_equal(mutated,first_member)
    mutated=copy.deepcopy(first_transition); mutated["transition_semantics_ready"]=0; cases["ledger_zero_for_false_rejected"]=not strict_equal(mutated,first_transition)
    mutated=copy.deepcopy(first_transition); mutated["transition_ready_syntax"]=1; cases["ledger_one_for_true_rejected"]=not strict_equal(mutated,first_transition)
    mutated=copy.deepcopy(duplicate); mutated["physical_equivalence_credit"]=False; cases["duplicate_false_for_zero_rejected"]=not strict_equal(mutated,duplicate)
    mutated=copy.deepcopy(result); mutated["strict_boundary"]["candidate_is_formal"]=0; cases["result_zero_for_false_rejected"]=not strict_equal(mutated,result)
    mutated=copy.deepcopy(result); mutated["input_pins"][0]["regular"]=1; cases["result_one_for_true_rejected"]=not strict_equal(mutated,result)
    mutated=copy.deepcopy(result); mutated["formal_credit"]["CM2"]=False; cases["result_false_for_zero_rejected"]=not strict_equal(mutated,result)
    bad_ref=copy.deepcopy(refs); bad_ref[0]["ref_row_sha256"]="f"*64
    cases["raw_input_change_changes_commitment"]=digest(raw_commitment(first_member["member_id"],first_member["coarse_family"],source,refs))!=digest(raw_commitment(first_member["member_id"],first_member["coarse_family"],source,bad_ref))
    mutated=dict(first_member); mutated["row_sha256"]="0"*64
    try: check_closed_row(mutated,"attack"); cases["row_hash_mutation_rejected"]=False
    except Blocked: cases["row_hash_mutation_rejected"]=True
    try: DECODER.decode('{"x":0,"x":0}'); cases["duplicate_json_key_rejected"]=False
    except Blocked: cases["duplicate_json_key_rejected"]=True
    try: DECODER.decode('{"x":0.0}'); cases["nonintegral_json_rejected"]=False
    except Blocked: cases["nonintegral_json_rejected"]=True
    exact={"x":"a"*(MAX_DECODED_CANONICAL_ROW_BYTES-len(canonical({"x":""})))}; need(len(canonical(exact))==MAX_DECODED_CANONICAL_ROW_BYTES,"cap fixture")
    cases["final_canonical_cap_exact_accepted"]=list(iter_array(io.StringIO('{"rows":['+canonical(exact).decode("ascii")+']}'),'"rows"'))==[exact]
    try: list(iter_array(io.StringIO('{"rows":['+canonical({"x":exact["x"]+"a"}).decode("ascii")+']}'),'"rows"')); cases["final_canonical_cap_plus_one_rejected"]=False
    except Blocked: cases["final_canonical_cap_plus_one_rejected"]=True
    with tempfile.TemporaryDirectory(prefix="cm2-k2i3-fs-attack-",dir="/tmp") as root:
        base=Path(root)/"base"; base.write_bytes(b"x"); hard=Path(root)/"hard"; sym=Path(root)/"sym"; os.link(base,hard); os.symlink(base,sym)
        cases["hardlink_nlink_rejected"]=os.stat(base,follow_symlinks=False).st_nlink!=1
        cases["symlink_mode_rejected"]=not stat.S_ISREG(os.stat(sym,follow_symlinks=False).st_mode)
    need(all(cases.values()),"attack suite")
    return {"schema":SCHEMA+".attack-suite.v1","status":"PASS_ALL_COHERENT_MUTATIONS_REJECTED","attack_count":len(cases),"all_rejected":True,"cases":cases,"formal_credit":zero_credit()}


def sha_path(path: Path) -> tuple[int,str]:
    named=os.stat(path,follow_symlinks=False); need(stat.S_ISREG(named.st_mode) and named.st_nlink==1,"manifest member shape:"+path.name); fd=os.open(path,os.O_RDONLY|getattr(os,"O_CLOEXEC",0)|getattr(os,"O_NOFOLLOW",0))
    try:
        opened=os.fstat(fd); need(stat_fingerprint(named)==stat_fingerprint(opened),"manifest open binding"); n,h=hash_fd(fd,named.st_size); need(stat_fingerprint(opened)==stat_fingerprint(os.fstat(fd))==stat_fingerprint(os.stat(path,follow_symlinks=False)),"manifest final binding"); return n,h
    finally: os.close(fd)


def receipt_payloads(attack: dict[str,Any],verification: dict[str,Any],report: str,cold: str) -> dict[str,bytes]:
    return {RECEIPTS["attack"]:canonical(attack)+b"\n",RECEIPTS["verification"]:canonical(verification)+b"\n",RECEIPTS["report"]:report.encode("utf-8"),RECEIPTS["cold"]:cold.encode("utf-8")}


def expected_manifest(payloads: dict[str,bytes],snapshot: Snapshot) -> bytes:
    assert snapshot.self_entry is not None
    hashes={filename:sha for _,filename,_,sha in PACKAGE_PINS}
    hashes[VERIFIER]=snapshot.self_entry[3]
    for filename,payload in payloads.items():
        hashes[filename]=hashlib.sha256(payload).hexdigest()
    package_names=[PRODUCER,VERIFIER,*OUTPUTS.values(),*payloads.keys()]
    need(set(package_names)==set(hashes),"exact manifest member set")
    return "".join(f"{hashes[filename]}  {filename}\n" for filename in sorted(package_names,key=lambda value:value.encode("ascii"))).encode("ascii")


def publish_receipts(payloads: dict[str,bytes],manifest: bytes) -> str:
    output_named=os.stat(DATA,follow_symlinks=False); output_fd=os.open(DATA,os.O_RDONLY|getattr(os,"O_DIRECTORY",0)|getattr(os,"O_CLOEXEC",0)|getattr(os,"O_NOFOLLOW",0)); need(directory_identity(output_named)==directory_identity(os.fstat(output_fd)),"receipt output binding")
    try:
        with tempfile.TemporaryDirectory(prefix="cm2-k2i3-receipt-",dir="/tmp") as tmp:
            stage=Path(tmp); stage_named=os.stat(stage,follow_symlinks=False); stage_fd=os.open(stage,os.O_RDONLY|getattr(os,"O_DIRECTORY",0)|getattr(os,"O_CLOEXEC",0)|getattr(os,"O_NOFOLLOW",0)); need(directory_identity(stage_named)==directory_identity(os.fstat(stage_fd)),"receipt stage binding")
            for filename,payload in payloads.items():
                with (stage/filename).open("xb") as handle: handle.write(payload); handle.flush(); os.fsync(handle.fileno())
            for filename in payloads:
                info=os.stat(filename,dir_fd=stage_fd,follow_symlinks=False); need(stat.S_ISREG(info.st_mode) and info.st_nlink==1,"receipt staged shape"); os.replace(filename,filename,src_dir_fd=stage_fd,dst_dir_fd=output_fd)
            os.fsync(output_fd)
            for filename,payload in payloads.items():
                size,sha=sha_path(DATA/filename); need(size==len(payload) and sha==hashlib.sha256(payload).hexdigest(),"published receipt bytes:"+filename)
            with (stage/RECEIPTS["manifest"]).open("xb") as handle: handle.write(manifest); handle.flush(); os.fsync(handle.fileno())
            info=os.stat(RECEIPTS["manifest"],dir_fd=stage_fd,follow_symlinks=False); need(stat.S_ISREG(info.st_mode) and info.st_nlink==1,"manifest staged shape")
            os.replace(RECEIPTS["manifest"],RECEIPTS["manifest"],src_dir_fd=stage_fd,dst_dir_fd=output_fd); os.fsync(output_fd)
            manifest_sha=hashlib.sha256(manifest).hexdigest()
            os.close(stage_fd)
        need(directory_identity(os.fstat(output_fd))==directory_identity(output_named)==directory_identity(os.stat(DATA,follow_symlinks=False)),"receipt output final binding")
        return manifest_sha
    finally: os.close(output_fd)


def verify_receipts_no_write(payloads: dict[str,bytes],manifest: bytes) -> str:
    expected={**payloads,RECEIPTS["manifest"]:manifest}
    named_dir=os.stat(DATA,follow_symlinks=False)
    dirfd=os.open(DATA,os.O_RDONLY|getattr(os,"O_DIRECTORY",0)|getattr(os,"O_CLOEXEC",0)|getattr(os,"O_NOFOLLOW",0))
    held_dir=os.fstat(dirfd); need(directory_identity(named_dir)==directory_identity(held_dir),"no-write receipt dir binding")
    opened: list[tuple[str,int,os.stat_result,bytes]]=[]
    try:
        for filename,want in expected.items():
            before=os.stat(filename,dir_fd=dirfd,follow_symlinks=False); need(stat.S_ISREG(before.st_mode) and before.st_nlink==1 and before.st_size==len(want),"no-write receipt shape:"+filename)
            fd=os.open(filename,os.O_RDONLY|getattr(os,"O_CLOEXEC",0)|getattr(os,"O_NOFOLLOW",0),dir_fd=dirfd); current=os.fstat(fd); need(stat_fingerprint(before)==stat_fingerprint(current),"no-write receipt open binding:"+filename)
            raw=os.pread(fd,before.st_size,0); need(raw==want,"no-write receipt exact bytes:"+filename)
            opened.append((filename,fd,current,want))
        for filename,fd,before,want in opened:
            raw=os.pread(fd,len(want),0); named=os.stat(filename,dir_fd=dirfd,follow_symlinks=False); need(raw==want and stat_fingerprint(before)==stat_fingerprint(os.fstat(fd))==stat_fingerprint(named),"no-write receipt final binding:"+filename)
        need(directory_identity(held_dir)==directory_identity(os.fstat(dirfd))==directory_identity(os.stat(DATA,follow_symlinks=False)),"no-write receipt directory final binding")
        return hashlib.sha256(manifest).hexdigest()
    finally:
        for _,fd,_,_ in opened: os.close(fd)
        os.close(dirfd)


def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--verify",action="store_true",required=True)
    mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write",action="store_true")
    mode.add_argument("--no-write",action="store_true")
    args=parser.parse_args()
    with Snapshot(DATA) as snapshot:
        sheet,side,back,tables=reconstruct_sources(snapshot)
        members=sorted(set(sheet)|set(side),key=lambda value:value.encode("ascii")); duplicates=sorted((mid for mid,refs in side.items() if len(refs)==2),key=lambda value:value.encode("ascii"))
        def fr(mid: str) -> tuple[str,list[dict[str,Any]]]: return ("G2A",sheet[mid]) if mid in sheet else ("G2B",side[mid])
        ledgers={
            "member":output_meta(snapshot,"OUT_MEMBER",(expected_member(mid,fr(mid)[0],back[mid],fr(mid)[1]) for mid in members),115456),
            "representation":output_meta(snapshot,"OUT_REPRESENTATION",(expected_representation(mid,fr(mid)[0],back[mid],fr(mid)[1]) for mid in members),115456),
            "duplicate_reference":output_meta(snapshot,"OUT_DUPLICATE",(expected_duplicate(mid,back[mid],side[mid]) for mid in duplicates),16),
            "semantic_gap":output_meta(snapshot,"OUT_GAP",(expected_gap(mid,fr(mid)[0],back[mid],fr(mid)[1]) for mid in members),115456),
            "transition_handle":output_meta(snapshot,"OUT_TRANSITION",(expected_transition(mid,fr(mid)[0],back[mid],fr(mid)[1]) for mid in members),115456),
        }
        result=snapshot.small_json("OUT_RESULT"); want_result=expected_result(tables,ledgers); need(strict_equal(result,want_result),"exact result contract")
        need(digest(result)=="34cc51c60b992890d1ccfdf784ed807c382dfaf34e82e84389e891ab1f598b81","result object digest")
        cold=cold_replay(snapshot)
        first_mid=members[0]; first_family,first_refs=fr(first_mid); first_member=expected_member(first_mid,first_family,back[first_mid],first_refs); first_transition=expected_transition(first_mid,first_family,back[first_mid],first_refs); duplicate=expected_duplicate(duplicates[0],back[duplicates[0]],side[duplicates[0]])
        attack=attacks(result,first_member,first_transition,duplicate,back[first_mid],first_refs)
        assert snapshot.self_entry is not None
        verification={"schema":VERIFICATION_SCHEMA,"status":"PASS_INDEPENDENT_FULL_REPLAY__ZERO_THEOREM_CREDIT","verifier_sha256":snapshot.self_entry[3],"producer_static_pin":{"filename":PRODUCER,"size":39121,"sha256":"e32f6cbd9f2fa164827c5fbe1d03c5be7d832031248a1b0553acdbe86566a542"},"source_pin_count":len(SOURCE_PINS),"source_table_commitments":tables,"exact_census":result["exact_census"],"ledgers":ledgers,"cold_replay":cold,"attack_suite":{"attack_count":attack["attack_count"],"all_rejected":True},"independent_verifier_imported_producer":False,"manifest_written_last":True,"availability_boundary":"No runtime or RSS upper bound is claimed; exhaustion before completion yields no receipt or credit.","formal_credit":zero_credit()}
        report=("# Round306B1AF4K2I3 independent verification\n\nPASS for the exact G2 mechanical identity/representation partial lane only.\n\n- G2a: 38,624 identities/references.\n- G2b: 76,848 references to 76,832 identities; all 16 duplicate-reference excess rows are explicit.\n- Member and current representation candidates: 115,456 each.\n- Semantic gaps and transition syntax handles: 115,456 each.\n- Every handle binds the complete canonical raw input commitment.\n- Two cold seeds produced six byte-identical outputs.\n\nGraph definition, physical incidence, full support, representation cover, A1/A2, B1A, B2, maximality, D02, and CM2 credits remain zero.\n")
        cold_md=("# Cold replay\n\nStatus: `"+cold["status"]+"`\n\nSeeds: `17`, `93`; all six outputs matched each other and the sealed package byte for byte. Producer execution used the held producer file descriptor and the verifier did not import producer code. Runtime and RSS measurements are intentionally excluded from canonical receipts.\n")
        payloads=receipt_payloads(attack,verification,report,cold_md)
        manifest=expected_manifest(payloads,snapshot)
        manifest_sha=publish_receipts(payloads,manifest) if args.write else verify_receipts_no_write(payloads,manifest)
    print(canonical({"status":verification["status"],"mode":"WRITE" if args.write else "NO_WRITE","manifest_sha256":manifest_sha,"formal_credit":zero_credit()}).decode("ascii"))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
