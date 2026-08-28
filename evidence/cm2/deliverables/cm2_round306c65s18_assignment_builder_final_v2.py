#!/usr/bin/env python3
"""Final C65s18 v2 20,879-to-64 assignment builder with exclusive publication.

This builder never evaluates a route and cannot emit shard artifacts.  Its
inventory and result are zero-credit inputs to a separately frozen executor.
"""

from __future__ import annotations

import copy
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import zlib
from typing import Any


SELF = Path(__file__).resolve()
OUT = SELF.parent
BASE = "cm2_round306c65s18_depth18_64shard"
SCHEMA = "cm2.round306c65s18.depth18-64shard.v2"
DOMAIN = SCHEMA + ".assignment"
CONTRACT = OUT / "cm2_round306c65s18_independent_contract_v2.json"
C61_RESULT = OUT / "cm2_round306c61s12_depth12_16shard_aggregate_result_v4.json"
C61_LEAVES = OUT / "cm2_round306c61s12_depth12_16shard_aggregate_leaf_ledger_v4.jsonl.gz"
C61_MANIFEST = OUT / "cm2_round306c61s12_depth12_16shard_manifest_v4.sha256"
C61_VERIFY = OUT / "cm2_round306c61s12_independent_postexecution_verification_v4.json"
C61_SELFTEST = OUT / "cm2_round306c61s12_independent_postexecution_self_test_v4.json"
C58_RESULT = OUT / "cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement_result_v1.json"
C58_LEAVES = OUT / "cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement_leaf_ledger_v1.jsonl.gz"
INVENTORY = OUT / (BASE + "_assignment_inventory_v2.jsonl.gz")
RESULT = OUT / (BASE + "_assignment_result_v2.json")
MAX_GZIP_OUTPUT = 512 * 1024 * 1024

PIN = {
    "contract_file": "e320ac48b1cf3675a3c152d0cb9e6084ba750433722fef716e4a8ab534fab287",
    "contract_object": "5d8a39432c2b02e807c5624ea26f56a12b58f66601ab391b52fee89d0ca604a4",
    "C61_result_file": "06b4146185cb6ef0c8d908d523369008481f7df4e6a05ad5956c001267b07f5e",
    "C61_result_object": "05bcb4301ac74aefd6744db2e633c2479c423fab881b33609bf7234a5537e584",
    "C61_leaf_file": "2656bc4d1b99d37da3733338d85c8d6301621563a400d5db40380078c001b1c2",
    "C61_manifest_file": "4c18c510367fc15b801fb6eff7901ad94a8fd53e47a6b7868ee876b554393545",
    "C61_verify_file": "2dc773d0051cc9668cdf7752fb61ac09f495044f566972faa335fffc509e9fc7",
    "C61_verify_object": "066e03be0c41600f5fb5cc2c157fe6e7eb04d1060896dd1acc910b06aab30b24",
    "C61_selftest_file": "b5a6ad21006d690637c797e7459363f2d6d8e55ad3abd5c112e817de5f915f32",
    "C61_selftest_object": "77a6091d60a883826fc4f9e8786128ae6dd9e79bcfc7d8662b9da1ed0262339e",
    "C58_result_file": "ed4eb1e5ea64c61e4b85a710c1429a2f0b489048320badd4d9a8214bc38c05bc",
    "C58_result_object": "038503bd21505dacde4ce6dc59a320fa70a97cc0dccce33be210c60bbd7d0a30",
    "C58_leaf_file": "15a5b1c5c15f8528591bd80be040317590dadec70b4476d01eb3763ae64965df",
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


def closed_stat(info: os.stat_result, label: str) -> tuple[int, int, int, int, int, int, int]:
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "regular single-link:" + label)
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size,
            info.st_mtime_ns, info.st_ctime_ns)


def read_pinned(path: Path, pin: str) -> bytes:
    parent_fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try:
        flags = os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0)
        fd = os.open(path.name, flags, dir_fd=parent_fd)
        try:
            before = closed_stat(os.fstat(fd), path.name)
            parts: list[bytes] = []
            while True:
                block = os.read(fd, 1 << 20)
                if not block:
                    break
                parts.append(block)
            raw = b"".join(parts)
            need(closed_stat(os.fstat(fd), path.name) == before, "fd TOCTOU:" + path.name)
            named = os.stat(path.name, dir_fd=parent_fd, follow_symlinks=False)
            need(closed_stat(named, path.name) == before, "fd/path identity:" + path.name)
            need(hashlib.sha256(raw).hexdigest() == pin, "file pin:" + path.name)
            return raw
        finally:
            os.close(fd)
    finally:
        os.close(parent_fd)


def read_stable(path: Path) -> bytes:
    parent_fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try:
        fd = os.open(path.name, os.O_RDONLY | os.O_CLOEXEC |
                     getattr(os, "O_NOFOLLOW", 0), dir_fd=parent_fd)
        try:
            before = closed_stat(os.fstat(fd), path.name)
            parts: list[bytes] = []
            while True:
                block = os.read(fd, 1 << 20)
                if not block:
                    break
                parts.append(block)
            need(closed_stat(os.fstat(fd), path.name) == before and
                 closed_stat(os.stat(path.name, dir_fd=parent_fd, follow_symlinks=False),
                             path.name) == before, "stable self bytes:" + path.name)
            return b"".join(parts)
        finally:
            os.close(fd)
    finally:
        os.close(parent_fd)


def strict_loads(raw: bytes) -> Any:
    need(not raw.startswith(b"\xef\xbb\xbf"), "UTF-8 BOM forbidden")

    def hook(items: list[tuple[str, Any]]) -> dict[str, Any]:
        answer: dict[str, Any] = {}
        for key, value in items:
            need(key not in answer, "duplicate JSON key:" + key)
            answer[key] = value
        return answer

    return json.loads(raw, object_pairs_hook=hook,
                      parse_constant=lambda value: (_ for _ in ()).throw(
                          FailClosed("nonfinite JSON:" + value)))


def object_file(path: Path, file_pin: str, object_pin: str) -> dict[str, Any]:
    raw = read_pinned(path, file_pin)
    value = strict_loads(raw)
    need(type(value) is dict, "JSON object:" + path.name)
    body = copy.deepcopy(value)
    claim = body.pop("object_sha256", None)
    need(claim == object_pin and digest(body) == object_pin, "object closure:" + path.name)
    return value


def one_gzip_member(raw: bytes, label: str) -> bytes:
    inflater = zlib.decompressobj(16 + zlib.MAX_WBITS)
    plain = inflater.decompress(raw, MAX_GZIP_OUTPUT + 1)
    need(len(plain) <= MAX_GZIP_OUTPUT and not inflater.unconsumed_tail,
         "bounded gzip output:" + label)
    plain += inflater.flush()
    need(inflater.eof and not inflater.unused_data and len(plain) <= MAX_GZIP_OUTPUT,
         "exactly one gzip member/no trailing bytes:" + label)
    return plain


def ledger(path: Path, descriptor: dict[str, Any], pin: str) -> list[dict[str, Any]]:
    raw = read_pinned(path, pin)
    plain = one_gzip_member(raw, path.name)
    need(bool(plain) and plain.endswith(b"\n"), "newline-terminated JSONL:" + path.name)
    answer: list[dict[str, Any]] = []
    sequence = hashlib.sha256()
    for line in plain.splitlines(keepends=True):
        need(line.endswith(b"\n") and line != b"\n", "canonical JSONL line:" + path.name)
        row = strict_loads(line[:-1])
        need(type(row) is dict and canonical(row) == line[:-1], "canonical row bytes:" + path.name)
        body = copy.deepcopy(row)
        claim = body.pop("row_sha256", None)
        need(type(claim) is str and digest(body) == claim, "row closure:" + path.name)
        sequence.update((claim + "\n").encode("ascii"))
        answer.append(row)
    need(len(answer) == descriptor["row_count"] and
         sequence.hexdigest() == descriptor["row_hash_line_sequence_sha256"],
         "ledger descriptor:" + path.name)
    return answer


class ExclusiveFile:
    def __init__(self, path: Path):
        self.path = path
        self.dir_fd = -1
        self.fd = -1

    def __enter__(self) -> "ExclusiveFile":
        self.dir_fd = os.open(self.path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
        flags = os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0)
        self.fd = os.open(self.path.name, flags, 0o644, dir_fd=self.dir_fd)
        closed_stat(os.fstat(self.fd), self.path.name)
        return self

    def write(self, raw: bytes) -> None:
        view = memoryview(raw)
        while view:
            count = os.write(self.fd, view)
            need(count > 0, "short output write:" + self.path.name)
            view = view[count:]

    def seal(self) -> bytes:
        os.fsync(self.fd)
        expected = closed_stat(os.fstat(self.fd), self.path.name)
        named = closed_stat(os.stat(self.path.name, dir_fd=self.dir_fd,
                                    follow_symlinks=False), self.path.name)
        need(named == expected, "output fd/path identity:" + self.path.name)
        os.lseek(self.fd, 0, os.SEEK_SET)
        parts: list[bytes] = []
        while True:
            block = os.read(self.fd, 1 << 20)
            if not block:
                break
            parts.append(block)
        need(closed_stat(os.fstat(self.fd), self.path.name) == expected,
             "output fd stable reread:" + self.path.name)
        os.fsync(self.dir_fd)
        return b"".join(parts)

    def __exit__(self, *_args: Any) -> None:
        if self.fd >= 0:
            os.close(self.fd)
        if self.dir_fd >= 0:
            os.close(self.dir_fd)


class LedgerWriter:
    def __init__(self, path: Path):
        self.atomic = ExclusiveFile(path)
        self.file: ExclusiveFile | None = None
        self.sink: Any = None
        self.gzip_stream: gzip.GzipFile | None = None
        self.count = 0
        self.sequence = hashlib.sha256()
        self.raw = b""

    def __enter__(self) -> "LedgerWriter":
        self.file = self.atomic.__enter__()
        self.sink = os.fdopen(os.dup(self.file.fd), "wb", closefd=True)
        self.gzip_stream = gzip.GzipFile(filename="", mode="wb", fileobj=self.sink, mtime=0)
        return self

    def write(self, row: dict[str, Any]) -> None:
        claim = digest(row)
        closed = {**row, "row_sha256": claim}
        assert self.gzip_stream is not None
        self.gzip_stream.write(canonical(closed) + b"\n")
        self.sequence.update((claim + "\n").encode("ascii"))
        self.count += 1

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        try:
            if self.gzip_stream is not None:
                self.gzip_stream.close()
            if self.sink is not None:
                self.sink.close()
            if exc_type is None and self.file is not None:
                self.raw = self.file.seal()
                one_gzip_member(self.raw, self.file.path.name)
        finally:
            self.atomic.__exit__(exc_type, exc, tb)

    def descriptor(self) -> dict[str, Any]:
        need(bool(self.raw), "sealed ledger required")
        return {"filename": INVENTORY.name,
                "order": "C61_V4_AGGREGATE_LEDGER_ORDER_FILTERED_COLLISION2_HANDOFF",
                "row_count": self.count,
                "row_hash_line_sequence_sha256": self.sequence.hexdigest(),
                "sha256": hashlib.sha256(self.raw).hexdigest(), "size": len(self.raw)}


def publish_json(path: Path, value: dict[str, Any]) -> None:
    raw = canonical(value) + b"\n"
    with ExclusiveFile(path) as target:
        target.write(raw)
        need(target.seal() == raw, "published JSON byte replay:" + path.name)


def assignment_preimage(source_sha: str, path: str) -> bytes:
    need(type(source_sha) is str and len(source_sha) == 64 and
         set(source_sha) <= set("0123456789abcdef"), "source row SHA")
    need(type(path) is str and len(path) == 21 and set(path) <= {"0", "1"},
         "exact 21-bit source path")
    return canonical({"assignment_domain": DOMAIN, "path": path,
                      "source_C61_aggregate_leaf_row_sha256": source_sha})


def main() -> int:
    try:
        contract = object_file(CONTRACT, PIN["contract_file"], PIN["contract_object"])
        c61_result = object_file(C61_RESULT, PIN["C61_result_file"], PIN["C61_result_object"])
        read_pinned(C61_MANIFEST, PIN["C61_manifest_file"])
        c61_verify = object_file(C61_VERIFY, PIN["C61_verify_file"], PIN["C61_verify_object"])
        c61_selftest = object_file(C61_SELFTEST, PIN["C61_selftest_file"], PIN["C61_selftest_object"])
        need(c61_result["schema"] == contract["source"]["C61_aggregate_result"]["schema"] and
             c61_result["status"] == contract["source"]["C61_aggregate_result"]["status"] and
             c61_result["frozen_inputs"] == contract["source"]["C61_aggregate_result"]["frozen_inputs"],
             "C61 exact result contract")
        need(c61_verify["status"] == contract["source"]["C61_independent_verification"]["status"] and
             c61_selftest["status"] == contract["source"]["C61_independent_self_test"]["status"],
             "C61 audit statuses")
        c61_rows = ledger(C61_LEAVES, c61_result["ledgers"]["aggregate_leaves"], PIN["C61_leaf_file"])
        selected = [row for row in c61_rows if row["disposition"] == "COLLISION2_HANDOFF"]
        need(len(selected) == contract["selection"]["exact_count"] == 20879,
             "C61 exact residual count")
        source_seq = hashlib.sha256()
        continuation_seq = hashlib.sha256()
        for row in selected:
            source_seq.update((row["row_sha256"] + "\n").encode("ascii"))
            continuation_seq.update(
                (row["continuation"]["continuation_object_sha256"] + "\n").encode("ascii"))
        need(source_seq.hexdigest() ==
             contract["selection"]["filtered_source_row_sha256_line_sequence_sha256"] and
             continuation_seq.hexdigest() ==
             contract["selection"]["filtered_continuation_object_sha256_line_sequence_sha256"],
             "C61 filtered sequences")
        predicate = contract["selection"]["predicate"]
        need(all(row["schema"] == predicate["schema"] and
                 row["continuation"]["next_collision_index"] == 2 and
                 row["additional_depth_from_C58"] == 6 and len(row["path"]) == 21 and
                 set(row["path"]) <= {"0", "1"} and
                 row["parent_volume_fraction"] == "1/2097152" and
                 row["formal_credit"] == row["whole_parent_credit"] ==
                 row["D02_gate_credit"] == row["local_terminal_credit"] ==
                 row["continuation"]["continuation_credit"] == 0 for row in selected),
             "exact residual predicate")
        need(len({row["row_sha256"] for row in selected}) == 20879,
             "source identities unique")

        c58_result = object_file(C58_RESULT, PIN["C58_result_file"], PIN["C58_result_object"])
        c58_rows = ledger(C58_LEAVES, c58_result["ledgers"]["leaves"], PIN["C58_leaf_file"])
        c58_by_hash = {row["row_sha256"]: row for row in c58_rows}
        need(len(c58_by_hash) == len(c58_rows), "C58 identities unique")

        counts = [0] * 64
        claims = hashlib.sha256()
        seen: set[str] = set()
        writer = LedgerWriter(INVENTORY)
        with writer:
            for source in selected:
                source_sha = source["row_sha256"]
                need(source_sha not in seen, "duplicate source identity")
                seen.add(source_sha)
                c58 = c58_by_hash.get(source["source_C58_leaf_row_sha256"])
                need(c58 is not None and c58["disposition"] == "COLLISION2_HANDOFF" and
                     c58["source_handoff_ordinal"] == source["source_handoff_ordinal"] and
                     c58["path"] == source["source_path"] and
                     source["path"].startswith(c58["path"]) and
                     c58["pair_index"] == source["pair_index"] and
                     source["continuation"]["prior_C58_leaf_row_sha256"] == c58["row_sha256"] and
                     source["continuation"]["prior_C58_handoff_object_sha256"] ==
                     c58["collision2_handoff"]["handoff_object_sha256"],
                     "exact C61/C58 lineage")
                claim = hashlib.sha256(assignment_preimage(source_sha, source["path"])).hexdigest()
                shard = int(claim, 16) % 64
                counts[shard] += 1
                claims.update((claim + "\n").encode("ascii"))
                writer.write({
                    "schema": SCHEMA + ".assignment-row",
                    "assignment_preimage_sha256": claim, "shard_id": shard,
                    "source_C61_aggregate_leaf_row_sha256": source_sha,
                    "source_C61_continuation_object_sha256":
                        source["continuation"]["continuation_object_sha256"],
                    "source_C61_source_shard_row_sha256": source["source_shard_row_sha256"],
                    "source_C58_leaf_row_sha256": source["source_C58_leaf_row_sha256"],
                    "source_handoff_ordinal": source["source_handoff_ordinal"],
                    "source_path": source["source_path"], "path": source["path"],
                    "pair_index": source["pair_index"],
                    "parent_volume_fraction": source["parent_volume_fraction"],
                    "source_C61_disposition": source["disposition"],
                    "source_C61_next_collision_index": source["continuation"]["next_collision_index"],
                    "assignment_credit": 0, "formal_credit": 0,
                    "whole_parent_credit": 0, "D02_gate_credit": 0,
                })
        need(len(seen) == sum(counts) == 20879 and all(counts), "complete nonempty assignment")
        result: dict[str, Any] = {
            "schema": SCHEMA + ".assignment-result",
            "status": "FROZEN_V2_COMPLETE_MUTUALLY_EXCLUSIVE_20879_TO_64_CANONICAL_JSON_ASSIGNMENT",
            "assignment_builder_file_sha256": hashlib.sha256(read_stable(SELF)).hexdigest(),
            "independent_contract": {"file_sha256": PIN["contract_file"],
                                     "object_sha256": PIN["contract_object"]},
            "C61_source": {"aggregate_result_object_sha256": PIN["C61_result_object"],
                           "aggregate_leaf_ledger_sha256": PIN["C61_leaf_file"],
                           "manifest_sha256": PIN["C61_manifest_file"],
                           "verification_object_sha256": PIN["C61_verify_object"],
                           "self_test_object_sha256": PIN["C61_selftest_object"]},
            "assignment_domain": DOMAIN,
            "assignment_preimage_schema": contract["assignment"]["preimage"],
            "assignment_formula": "int(SHA256(preimage),16)%64",
            "inventory": writer.descriptor(),
            "input_count": 20879, "shard_count": 64,
            "per_shard_input_counts": {str(i): n for i, n in enumerate(counts)},
            "ordered_preimage_sha256_line_sequence_sha256": claims.hexdigest(),
            "filtered_source_row_sha256_line_sequence_sha256": source_seq.hexdigest(),
            "filtered_continuation_object_sha256_line_sequence_sha256":
                continuation_seq.hexdigest(),
            "assignment_complete": True, "assignment_mutually_exclusive": True,
            "partial_statistics_are_formal_credit": False, "candidate_is_authority": False,
            "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
            "runtime_canonical_pointer_or_seal_writes": False,
        }
        result["object_sha256"] = digest(result)
        publish_json(RESULT, result)
        print(json.dumps({"status": result["status"], "object_sha256": result["object_sha256"]},
                         sort_keys=True, separators=(",", ":")))
        return 0
    except (FailClosed, KeyError, OSError, TypeError, ValueError, zlib.error) as error:
        print(json.dumps({"status": "FAIL_CLOSED", "reason": str(error)},
                         sort_keys=True, separators=(",", ":")))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
