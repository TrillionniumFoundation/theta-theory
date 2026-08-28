#!/usr/bin/env python3
"""Independently replay and seal the final C65s18 v2 assignment bytes.

The assignment builder is never imported or executed.  Its source is pinned
as inert bytes and AST-inspected.  The output is a zero-credit execution-input
seal, not a mathematical or D02 authority.
"""

from __future__ import annotations

import ast
import copy
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import stat
from typing import Any
import zlib


SELF = Path(__file__).resolve()
OUT = SELF.parent
DOMAIN = "cm2.round306c65s18.depth18-64shard.v2.assignment"
CONTRACT = OUT / "cm2_round306c65s18_independent_contract_v2.json"
BUILDER = OUT / "cm2_round306c65s18_assignment_builder_final_v2.py"
ASSIGNMENT = OUT / "cm2_round306c65s18_depth18_64shard_assignment_result_v2.json"
INVENTORY = OUT / "cm2_round306c65s18_depth18_64shard_assignment_inventory_v2.jsonl.gz"
C61_RESULT = OUT / "cm2_round306c61s12_depth12_16shard_aggregate_result_v4.json"
C61_LEAVES = OUT / "cm2_round306c61s12_depth12_16shard_aggregate_leaf_ledger_v4.jsonl.gz"
SEAL = OUT / "cm2_round306c65s18_assignment_authorization_seal_v2.json"
MAX_GZIP_OUTPUT = 512 * 1024 * 1024

PIN = {
    "contract_file": "e320ac48b1cf3675a3c152d0cb9e6084ba750433722fef716e4a8ab534fab287",
    "contract_object": "5d8a39432c2b02e807c5624ea26f56a12b58f66601ab391b52fee89d0ca604a4",
    "builder_file": "700326aee68f423b8e03a9f8adda95a07b811bab60e95bd159c8e46cc290794b",
    "assignment_file": "0306fd12de7d73988a45bac84acf70e4615e8e3aaef7c3c42a66fc39dbef4baa",
    "assignment_object": "c7671985713c8cfd8a496931f1b2686fa545448ce0a434c89e943b178000407f",
    "inventory_file": "e2c4714f1f1a8aa470a393d25ff03aaa3228f08979c30c90fd5f297469d6ad30",
    "C61_result_file": "06b4146185cb6ef0c8d908d523369008481f7df4e6a05ad5956c001267b07f5e",
    "C61_result_object": "05bcb4301ac74aefd6744db2e633c2479c423fab881b33609bf7234a5537e584",
    "C61_leaf_file": "2656bc4d1b99d37da3733338d85c8d6301621563a400d5db40380078c001b1c2",
}


class FailClosed(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if not value:
        raise FailClosed(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def closed_stat(info: os.stat_result, label: str) -> tuple[int, ...]:
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "regular single-link:" + label)
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size,
            info.st_mtime_ns, info.st_ctime_ns)


def read_pinned(path: Path, pin: str) -> bytes:
    directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try:
        fd = os.open(path.name, os.O_RDONLY | os.O_CLOEXEC |
                     getattr(os, "O_NOFOLLOW", 0), dir_fd=directory)
        try:
            before = closed_stat(os.fstat(fd), path.name)
            chunks: list[bytes] = []
            while True:
                chunk = os.read(fd, 1 << 20)
                if not chunk:
                    break
                chunks.append(chunk)
            raw = b"".join(chunks)
            need(closed_stat(os.fstat(fd), path.name) == before and
                 closed_stat(os.stat(path.name, dir_fd=directory, follow_symlinks=False),
                             path.name) == before, "input fd/path identity:" + path.name)
            need(hashlib.sha256(raw).hexdigest() == pin, "input pin:" + path.name)
            return raw
        finally:
            os.close(fd)
    finally:
        os.close(directory)


def strict(raw: bytes) -> Any:
    need(not raw.startswith(b"\xef\xbb\xbf"), "BOM forbidden")

    def hook(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(key not in result, "duplicate key:" + key)
            result[key] = value
        return result

    return json.loads(raw, object_pairs_hook=hook,
                      parse_constant=lambda value: (_ for _ in ()).throw(
                          FailClosed("nonfinite JSON:" + value)))


def object_file(path: Path, file_pin: str, object_pin: str) -> dict[str, Any]:
    value = strict(read_pinned(path, file_pin))
    need(type(value) is dict, "object file:" + path.name)
    body = copy.deepcopy(value)
    claim = body.pop("object_sha256", None)
    need(claim == object_pin and digest(body) == object_pin, "object closure:" + path.name)
    return value


def gunzip(raw: bytes, label: str) -> bytes:
    inflater = zlib.decompressobj(16 + zlib.MAX_WBITS)
    plain = inflater.decompress(raw, MAX_GZIP_OUTPUT + 1)
    need(len(plain) <= MAX_GZIP_OUTPUT and not inflater.unconsumed_tail,
         "bounded gzip:" + label)
    plain += inflater.flush()
    need(inflater.eof and not inflater.unused_data and len(plain) <= MAX_GZIP_OUTPUT,
         "single gzip member/no trailing data:" + label)
    return plain


def rows(path: Path, pin: str, descriptor: dict[str, Any]) -> list[dict[str, Any]]:
    plain = gunzip(read_pinned(path, pin), path.name)
    need(bool(plain) and plain.endswith(b"\n"), "JSONL final newline:" + path.name)
    result: list[dict[str, Any]] = []
    sequence = hashlib.sha256()
    for line in plain.splitlines(keepends=True):
        need(line.endswith(b"\n") and line != b"\n", "JSONL row framing:" + path.name)
        row = strict(line[:-1])
        need(type(row) is dict and canonical(row) == line[:-1], "canonical JSONL row:" + path.name)
        body = copy.deepcopy(row)
        claim = body.pop("row_sha256", None)
        need(type(claim) is str and digest(body) == claim, "row closure:" + path.name)
        sequence.update((claim + "\n").encode("ascii"))
        result.append(row)
    need(len(result) == descriptor["row_count"] and
         sequence.hexdigest() == descriptor["row_hash_line_sequence_sha256"],
         "ledger descriptor:" + path.name)
    return result


def preimage(source_sha: str, path: str) -> bytes:
    need(type(source_sha) is str and len(source_sha) == 64 and
         set(source_sha) <= set("0123456789abcdef"), "source SHA")
    need(type(path) is str and len(path) == 21 and set(path) <= {"0", "1"}, "source path")
    return canonical({"assignment_domain": DOMAIN, "path": path,
                      "source_C61_aggregate_leaf_row_sha256": source_sha})


def audit_builder(raw: bytes) -> dict[str, Any]:
    tree = ast.parse(raw.decode("utf-8"), filename=BUILDER.name)
    calls: list[str] = []
    attributes: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            name = node.func.attr if isinstance(node.func, ast.Attribute) else (
                node.func.id if isinstance(node.func, ast.Name) else "")
            calls.append(name)
        if isinstance(node, ast.Attribute):
            attributes.add(node.attr)
    need("write_bytes" not in attributes and "write_text" not in attributes,
         "builder check-then-write APIs forbidden")
    need("open" in calls and "fsync" in calls and
         b"O_EXCL" in raw and b"O_NOFOLLOW" in raw and b"dir_fd=" in raw,
         "builder exclusive dirfd publication primitives")
    return {"parsed": True, "write_bytes_present": False, "write_text_present": False,
            "O_EXCL_present": True, "O_NOFOLLOW_present": True,
            "dirfd_present": True, "fsync_present": True,
            "builder_imported": False, "builder_executed": False}


def publish(value: dict[str, Any]) -> None:
    raw = canonical(value) + b"\n"
    directory = os.open(SEAL.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try:
        flags = (os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
        fd = os.open(SEAL.name, flags, 0o644, dir_fd=directory)
        try:
            view = memoryview(raw)
            while view:
                count = os.write(fd, view)
                need(count > 0, "short seal write")
                view = view[count:]
            os.fsync(fd)
            expected = closed_stat(os.fstat(fd), SEAL.name)
            need(closed_stat(os.stat(SEAL.name, dir_fd=directory, follow_symlinks=False),
                             SEAL.name) == expected, "seal fd/path identity")
            os.lseek(fd, 0, os.SEEK_SET)
            replay = b""
            while True:
                chunk = os.read(fd, 1 << 20)
                if not chunk:
                    break
                replay += chunk
            need(replay == raw and closed_stat(os.fstat(fd), SEAL.name) == expected,
                 "seal byte replay")
            os.fsync(directory)
        finally:
            os.close(fd)
    finally:
        os.close(directory)


def main() -> int:
    try:
        contract = object_file(CONTRACT, PIN["contract_file"], PIN["contract_object"])
        builder_ast = audit_builder(read_pinned(BUILDER, PIN["builder_file"]))
        assignment = object_file(ASSIGNMENT, PIN["assignment_file"], PIN["assignment_object"])
        need(assignment["assignment_builder_file_sha256"] == PIN["builder_file"] and
             assignment["inventory"]["sha256"] == PIN["inventory_file"] and
             assignment["input_count"] == 20879 and assignment["shard_count"] == 64 and
             assignment["assignment_complete"] is True and
             assignment["assignment_mutually_exclusive"] is True,
             "assignment header")
        inventory = rows(INVENTORY, PIN["inventory_file"], assignment["inventory"])
        c61_result = object_file(C61_RESULT, PIN["C61_result_file"], PIN["C61_result_object"])
        source_rows = rows(C61_LEAVES, PIN["C61_leaf_file"],
                           c61_result["ledgers"]["aggregate_leaves"])
        sources = [row for row in source_rows if row["disposition"] == "COLLISION2_HANDOFF"]
        need(len(sources) == len(inventory) == 20879, "source/inventory count")
        counts = [0] * 64
        claims = hashlib.sha256()
        source_sequence = hashlib.sha256()
        continuation_sequence = hashlib.sha256()
        seen: set[str] = set()
        for source, assigned in zip(sources, inventory, strict=True):
            source_sha = source["row_sha256"]
            need(source_sha not in seen, "duplicate source identity")
            seen.add(source_sha)
            claim = hashlib.sha256(preimage(source_sha, source["path"])).hexdigest()
            shard = int(claim, 16) % 64
            need(assigned["source_C61_aggregate_leaf_row_sha256"] == source_sha and
                 assigned["source_C61_continuation_object_sha256"] ==
                 source["continuation"]["continuation_object_sha256"] and
                 assigned["source_C61_source_shard_row_sha256"] ==
                 source["source_shard_row_sha256"] and
                 assigned["source_C58_leaf_row_sha256"] == source["source_C58_leaf_row_sha256"] and
                 assigned["source_handoff_ordinal"] == source["source_handoff_ordinal"] and
                 assigned["source_path"] == source["source_path"] and
                 assigned["path"] == source["path"] and
                 assigned["pair_index"] == source["pair_index"] and
                 assigned["parent_volume_fraction"] == source["parent_volume_fraction"] and
                 assigned["source_C61_disposition"] == "COLLISION2_HANDOFF" and
                 assigned["source_C61_next_collision_index"] == 2 and
                 assigned["assignment_preimage_sha256"] == claim and
                 assigned["shard_id"] == shard,
                 "exact source/inventory bijection")
            need(assigned["assignment_credit"] == assigned["formal_credit"] ==
                 assigned["whole_parent_credit"] == assigned["D02_gate_credit"] == 0,
                 "inventory zero credit")
            counts[shard] += 1
            claims.update((claim + "\n").encode("ascii"))
            source_sequence.update((source_sha + "\n").encode("ascii"))
            continuation_sequence.update(
                (source["continuation"]["continuation_object_sha256"] + "\n").encode("ascii"))
        need(len(seen) == sum(counts) == 20879 and all(counts), "complete 64-shard bijection")
        need(assignment["per_shard_input_counts"] ==
             {str(index): count for index, count in enumerate(counts)} and
             assignment["ordered_preimage_sha256_line_sequence_sha256"] == claims.hexdigest() and
             assignment["filtered_source_row_sha256_line_sequence_sha256"] ==
             source_sequence.hexdigest() ==
             contract["selection"]["filtered_source_row_sha256_line_sequence_sha256"] and
             assignment["filtered_continuation_object_sha256_line_sequence_sha256"] ==
             continuation_sequence.hexdigest() ==
             contract["selection"]["filtered_continuation_object_sha256_line_sequence_sha256"],
             "assignment aggregate sequences")
        need(assignment["formal_credit"] == assignment["whole_parent_credit"] ==
             assignment["D02_gate_credit"] == 0 and
             assignment["candidate_is_authority"] is False and
             assignment["runtime_canonical_pointer_or_seal_writes"] is False,
             "assignment zero-credit boundary")
        seal: dict[str, Any] = {
            "schema": "cm2.round306c65s18.assignment-authorization-seal.v2",
            "status": "PASS_INDEPENDENT_FROZEN_ASSIGNMENT_BYTES_FOR_SHARD_EXECUTION__ZERO_CREDIT",
            "candidate_is_authority": False,
            "contract": {"file_sha256": PIN["contract_file"],
                         "object_sha256": PIN["contract_object"]},
            "assignment_builder": {"file_sha256": PIN["builder_file"],
                                   "consumed_as_inert_bytes_and_AST_only": True,
                                   "imported": False, "executed": False,
                                   "AST_audit": builder_ast},
            "assignment_result": {"file_sha256": PIN["assignment_file"],
                                  "object_sha256": PIN["assignment_object"]},
            "assignment_inventory": {"file_sha256": PIN["inventory_file"],
                                     "row_count": 20879,
                                     "row_hash_line_sequence_sha256":
                                         assignment["inventory"]["row_hash_line_sequence_sha256"]},
            "source": {"C61_result_object_sha256": PIN["C61_result_object"],
                       "C61_leaf_ledger_sha256": PIN["C61_leaf_file"],
                       "filtered_source_row_sha256_line_sequence_sha256":
                           source_sequence.hexdigest(),
                       "filtered_continuation_object_sha256_line_sequence_sha256":
                           continuation_sequence.hexdigest()},
            "assignment": {"domain": DOMAIN, "input_count": 20879, "shard_count": 64,
                           "per_shard_input_counts":
                               {str(index): count for index, count in enumerate(counts)},
                           "ordered_preimage_sha256_line_sequence_sha256": claims.hexdigest(),
                           "complete": True, "mutually_exclusive": True,
                           "source_identity_bijection": True},
            "partial_shards_are_an_aggregate": False,
            "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
            "runtime_canonical_pointer_or_seal_writes": False,
        }
        seal["object_sha256"] = digest(seal)
        publish(seal)
        print(json.dumps({"status": seal["status"], "object_sha256": seal["object_sha256"]},
                         sort_keys=True, separators=(",", ":")))
        return 0
    except (FailClosed, KeyError, OSError, TypeError, ValueError, zlib.error) as error:
        print(json.dumps({"status": "FAIL_CLOSED", "reason": str(error)},
                         sort_keys=True, separators=(",", ":")))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
