#!/usr/bin/env python3
"""No-import streaming outer verifier for the C27R2 release repair v5.

This independent source reopens the manifest-first package and current-byte
front-half receipts, streams all three quotient ledgers plus the actual-v2
edge ledger, rebuilds the quotient without importing or executing any core or
builder source, and emits only a conditional zero-credit outer receipt.
"""

from __future__ import annotations

import argparse
import ast
from collections import defaultdict
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
BASE = "cm2.round306c27r2.source-g-authority-v2.release-repair."
EVIDENCE_SCHEMA = BASE + "post-integrity-evidence-closure.v5"
EVIDENCE_STATUS = (
    "PASS_C27R2_RELEASE_REPAIR_V5_SNAPSHOT_BASELINE_VALIDATOR70_LOCK8_REAL_"
    "TRANSACTIONS_POST_REPLAY_FULL9STAT_AND_PRIVATE_CLEANUP_CLOSED__ZERO_"
    "CREDIT_PENDING_MANIFEST"
)
MANIFEST_SCHEMA = BASE + "manifest-receipt.v5"
MANIFEST_STATUS = (
    "PASS_C27R2_RELEASE_REPAIR_V5_EXACT_ROLE_MANIFESTS_POST_VALIDATOR70_LOCK8_"
    "ACTUAL_V2_PREDECESSOR_ONLY_AND_HISTORICAL_EXCLUSION_CLOSED__ZERO_"
    "CREDIT_PENDING_OUTER"
)
PLAN_SCHEMA = BASE + "chain-plan.v5"
PLAN_STATUS = (
    "FROZEN_C27R2_RELEASE_REPAIR_V5_EXACT70_PLUS_LOCK8_PLAN__EXECUTION_DISABLED_"
    "PENDING_INDEPENDENT_FULL_CHAIN_AUDIT"
)
OUTER_SCHEMA = BASE + "outer-verification.v5"
OUTER_STATUS = ("PASS_INDEPENDENT_C27R2_RELEASE_REPAIR_FULL_LEDGER_EDGE_DSU_"
                "FROZEN_C15_MEMBER_UNIVERSE_MANIFEST_VALIDATOR70_LOCK8_AND_CORE_OBJECT_"
                "REPLAY__CONDITIONAL_ZERO_CREDIT_PENDING_TERMINAL")
EXPECTED = {"frozen_C15_components": 57_876,
            "post_C27R2_components": 43_684,
            "proof_derived_component_edges": 14_860,
            "successful_DSU_merges": 14_192, "cycle_edges": 668,
            "frozen_C15_members": 502_204,
            "total_unordered_member_pairs": 126_104_177_706,
            "within_post_component_member_pairs": 542_179_508,
            "cross_post_component_member_pairs": 125_561_998_198}
RESULT_SCHEMA = ("cm2.round306c27r2.source-g-actual-v2-fresh-quotient-"
                 "rebuild.v2.producer-result.v1")
RESULT_STATUS = (
    "PASS_FRESH_ACTUAL_V2_SEED1_QUOTIENT_REBUILD_ZERO_CREDIT__PENDING_"
    "NO_IMPORT_SEED2_VERIFICATION_ATTACKS_COLD_REPLAY_AND_TERMINAL_SEAL"
)
OLD_SCHEMA = ("cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild."
              "v2.old-c15-component-to-post-component-row.v1")
MEMBER_SCHEMA = ("cm2.round306c27r2.source-g-actual-v2-fresh-quotient-"
                 "rebuild.v2.member-to-post-component-row.v1")
CENSUS_SCHEMA = ("cm2.round306c27r2.source-g-actual-v2-fresh-quotient-"
                 "rebuild.v2.post-component-census-row.v1")
EDGE_SCHEMA = ("cm2.c27-independent.primitive-twenty-family-gate-v5-actual."
               "full-component-edge-union.row.v2")
EDGE_PREFIX = "round306c27r2-v5-component-edge:"
C15_SCHEMA = ("cm2.round306c15.source-g-502204-member-fresh-dsu-freeze.v1."
              "member-component-row.v1")
C15_PATH = ("deliverables/cm2_round306c15_source_g_502204_member_fresh_dsu_"
            "freeze_member_component_ledger.jsonl.gz")
C15_SHA = "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a"
SEED1_EDGE_PATH = (".cm2-runtime/audit/c27-primitive-twenty-family-gate-v5-"
    "actual-v2-seed30660101-p0r2-20260808T1432/full_component_edge_union.jsonl.gz")
SEED2_EDGE_PATH = (".cm2-runtime/audit/c27-primitive-twenty-family-gate-v5-"
    "actual-v2-seed30660991-p0r2-20260808T1432/full_component_edge_union.jsonl.gz")
EDGE_SHA = "5bc29ef85bc57f467bee5ba94cd12e31950c2c940928cb57498421200c95bec0"
CORE_RECEIPT_FILE_SHA = "4104edc46bb130bae530a990609d5053bc9d7f675e4e3587e88b8327394c5796"
CORE_RECEIPT_OBJECT_SHA = "783d05cb9c01a2049a03112f9412bab787b5fad2c81fba1855d9cca4dabcb016"
BOUNDARY_VALIDATOR_PATH = (
    "deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_quotient_"
    "rebuild_v2_release_repair_boundary_independent_validator_v6.py")
BOUNDARY_VALIDATOR_SHA = "0" * 64  # Pending final boundary-v6 source pin.
INTEGRITY_RUNNER_PATH = (
    "deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_quotient_"
    "rebuild_v2_release_integrity_fixture_runner_v6.py")
INTEGRITY_RUNNER_SHA = "0" * 64  # Pending final boundary-v6 source pin.
ORDERED_VALIDATOR70_OBJECT_SHA = "12a18411f62ba091fad7a28af44fe6a2eea1e4befe211c0f58d16a30a1a434b8"
ORDERED_LOCK8_OBJECT_SHA = "92add6db3116e10fe54cda24ce5d61288bb47622e6956f1353898ba707811c5d"
COLD_RUNNER_PATH = (
    "deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_quotient_"
    "rebuild_v2_release_cold_replay_runner_v4.py"
)
COLD_RUNNER_SHA = "3d44ebbc37449192f975e3687284c6e74285f7d7f564e40ef12e37232f0ec838"
BOUNDARY_CONTRACT_FROZEN_GO = False  # boundary v5 historical NO-GO; v6 pending.
FORMAL_EXECUTION_AUTHORIZED = False  # Independent full-chain GO has not been minted.
VERIFICATION_SCHEMA = ("cm2.round306c27r2.source-g-actual-v2-fresh-quotient-"
    "rebuild.v2.independent-verification.v1")
VERIFICATION_STATUS = ("PASS_NO_IMPORT_ACTUAL_V2_SEED2_INDEPENDENT_QUOTIENT_"
    "AND_BYTE_EXACT_CANDIDATE_REPLAY__ZERO_CREDIT_PENDING_ATTACKS_COLD_"
    "REPLAY_AND_TERMINAL_SEAL")
ATTACK_SCHEMA = ("cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild."
    "v2.coherent-attack-harness.v1")
ATTACK_STATUS = ("PASS_BASELINE_AND_21_OF_21_COHERENT_ATTACKS_REJECTED_FAIL_"
    "CLOSED__ZERO_CREDIT_PENDING_RELEASE_CHAIN")
POST_PREFIX = "round306c27r2-source-g-post-component:"
CANDIDATE_NAMES = {"member_to_post_component.jsonl.gz",
                   "old_c15_component_to_post_component.jsonl.gz",
                   "post_component_census.jsonl.gz", "result.json"}


class Blocked(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Blocked(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
        ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def valid_sha(value: Any) -> bool:
    return type(value) is str and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def strict(raw: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in items:
            need(type(key) is str and key not in out, "duplicate JSON key")
            out[key] = value
        return out
    return json.loads(raw, object_pairs_hook=pairs,
        parse_constant=lambda x: (_ for _ in ()).throw(Blocked(x)))


def inside(raw: str | Path, *, absent: bool = False) -> Path:
    supplied = Path(raw)
    path = (supplied if supplied.is_absolute() else ROOT / supplied).absolute()
    try:
        relative = path.relative_to(ROOT)
    except ValueError as error:
        raise Blocked("path outside workspace") from error
    need(relative.parts and all(x not in {"", ".", ".."}
                                for x in relative.parts), "canonical path")
    cursor = ROOT
    for part in relative.parts:
        cursor /= part
        if not cursor.exists():
            need(absent, "missing path")
            break
        need(not cursor.is_symlink(), "symlink path component")
    return path


def fingerprint(info: os.stat_result) -> list[int]:
    return [info.st_dev, info.st_ino, info.st_mode, info.st_nlink,
            info.st_size, info.st_mtime_ns, info.st_ctime_ns,
            info.st_uid, info.st_gid]


def capture(path: Path, retain_bytes: bool = True) -> tuple[bytes, dict[str, Any]]:
    need(path.is_file() and not path.is_symlink(), "regular current file")
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "single-link current file")
        state = hashlib.sha256()
        chunks: list[bytes] = []
        while block := os.read(fd, 4 << 20):
            state.update(block)
            if retain_bytes: chunks.append(block)
        need(fingerprint(os.stat(path, follow_symlinks=False))
             == fingerprint(before)
             and fingerprint(os.fstat(fd)) == fingerprint(before),
             "stable current file")
        return b"".join(chunks), {"path": str(path.relative_to(ROOT)), "sha256": state.hexdigest(),
                "size": before.st_size, "stat_fingerprint": fingerprint(before)}
    finally:
        os.close(fd)


def record(path: Path) -> dict[str, Any]:
    return capture(path, False)[1]


def document(path: Path, closure: str) -> tuple[dict[str, Any], dict[str, Any]]:
    raw, item = capture(path)
    need(raw.endswith(b"\n"), "JSON newline")
    value = strict(raw[:-1])
    need(type(value) is dict and canonical(value) == raw[:-1], "canonical JSON")
    body = dict(value); claim = body.pop(closure, None)
    need(valid_sha(claim) and claim == digest(body), "object closure:" + closure)
    return value, item


def _write_all(descriptor: int, raw: bytes, writer: Any = os.write) -> None:
    offset = 0
    while offset < len(raw):
        count = writer(descriptor, raw[offset:])
        need(type(count) is int and count > 0, "write made positive progress")
        offset += count


def write_once(path: Path, raw: bytes) -> None:
    parent = os.open(path.parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
                     | getattr(os, "O_NOFOLLOW", 0)
                     | getattr(os, "O_CLOEXEC", 0))
    descriptor = -1
    try:
        descriptor = os.open(path.name, os.O_WRONLY | os.O_CREAT | os.O_EXCL
            | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0),
            0o400, dir_fd=parent)
        _write_all(descriptor, raw)
        os.fsync(descriptor)
        before = os.fstat(descriptor)
    finally:
        if descriptor >= 0:
            os.close(descriptor)
    reopened = os.open(path.name, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
                       | getattr(os, "O_CLOEXEC", 0), dir_fd=parent)
    try:
        chunks: list[bytes] = []
        while block := os.read(reopened, 1 << 20):
            chunks.append(block)
        after = os.fstat(reopened)
        current = os.stat(path.name, dir_fd=parent, follow_symlinks=False)
        observed = b"".join(chunks)
        need(observed == raw and stat.S_ISREG(after.st_mode) and after.st_nlink == 1
             and fingerprint(before) == fingerprint(after) == fingerprint(current)
             and hashlib.sha256(raw).digest() == hashlib.sha256(observed).digest(),
             "reopen exact bytes/SHA/full9stat/single-link")
        os.fsync(parent)
    finally:
        os.close(reopened)
        os.close(parent)


def parse_manifest(path: Path) -> dict[str, dict[str, Any]]:
    raw, _ = capture(path)
    need(raw.endswith(b"\n"), "manifest newline")
    result: dict[str, dict[str, Any]] = {}
    for line in raw.decode("ascii").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\x00\r\n]+)", line)
        need(match is not None, "manifest line")
        claim, shown = match.groups(); need(shown not in result, "duplicate path")
        item = record(inside(shown)); need(item["sha256"] == claim, "manifest SHA")
        result[shown] = item
    need(result and list(result) == sorted(result), "sorted nonempty manifest")
    return result


def self_independence() -> str:
    raw, _ = capture(SELF)
    tree = ast.parse(raw, filename=str(SELF))
    forbidden_modules = {"subprocess", "importlib", "runpy"}
    forbidden_calls = {"exec", "eval", "compile", "__import__"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            need(all(alias.name.split(".")[0] not in forbidden_modules
                     for alias in node.names), "forbidden import")
        if isinstance(node, ast.ImportFrom):
            need((node.module or "").split(".")[0] not in forbidden_modules,
                 "forbidden from-import")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            need(node.func.id not in forbidden_calls, "forbidden dynamic execution")
    return hashlib.sha256(raw).hexdigest()


def gzip_rows(path: Path, schema: str, keys: set[str],
              require_zero_credit: bool = True) -> Iterator[tuple[dict[str, Any], str]]:
    raw, _ = capture(path)
    header = raw[:10]
    need(len(header) == 10 and header[:3] == b"\x1f\x8b\x08"
         and header[4:8] == b"\x00\x00\x00\x00", "deterministic gzip header")
    with gzip.GzipFile(fileobj=io.BytesIO(raw), mode="rb") as stream:
        ordinal = 0
        while line := stream.readline():
            need(line.endswith(b"\n"), "JSONL newline")
            row = strict(line[:-1])
            need(type(row) is dict and canonical(row) + b"\n" == line,
                 "canonical JSONL")
            body = dict(row); claim = body.pop("row_sha256", None)
            need(set(row) == keys and valid_sha(claim) and claim == digest(body)
                 and row.get("schema") == schema
                 and row.get("ordinal") == ordinal
                 and (not require_zero_credit or row.get("formal_credit") == 0),
                 "row schema/ordinal/closure")
            yield row, claim
            ordinal += 1


C15_KEYS = {"schema", "member_ordinal", "registry_member_id",
    "fresh_component_id", "base_root_id", "official_key_id",
    "admission_source", "fresh_member_and_component_credit", "source_row_ref",
    "row_id", "row_sha256"}
OLD_KEYS = {"schema", "ordinal", "old_C15_component_id",
    "post_C27R2_component_id", "post_C27R2_old_component_count",
    "post_C27R2_old_component_ids_sha256", "formal_credit", "row_sha256"}
MEMBER_KEYS = {"schema", "ordinal", "member_ordinal", "registry_member_id",
    "old_C15_component_id", "post_C27R2_component_id", "formal_credit",
    "row_sha256"}
CENSUS_KEYS = {"schema", "ordinal", "post_C27R2_component_id",
    "member_count", "old_C15_component_count", "old_C15_component_ids_sha256",
    "within_member_pair_count", "formal_credit", "row_sha256"}
EDGE_KEYS = {"schema", "ordinal", "component_edge_key",
    "ordered_C15_component_pair", "supporting_physical_proof_row_count",
    "supporting_physical_proof_row_sequence_sha256", "formal_credit",
    "row_sha256"}


class DSU:
    def __init__(self, members: list[str]):
        self.parent = {x: x for x in members}
        self.size = {x: 1 for x in members}

    def find(self, x: str) -> str:
        need(x in self.parent, "edge component in frozen universe")
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: str, b: str) -> bool:
        a = self.find(a); b = self.find(b)
        if a == b:
            return False
        if self.size[a] < self.size[b] or (self.size[a] == self.size[b] and a > b):
            a, b = b, a
        self.parent[b] = a; self.size[a] += self.size[b]
        return True


def descriptor(result: dict[str, Any], key: str, path: Path,
               count: int, sequence: str) -> None:
    value = result.get("ledgers", {}).get(key)
    item = record(path)
    need(type(value) is dict and value.get("filename") == path.name
         and value.get("sha256") == item["sha256"]
         and value.get("size") == item["size"]
         and value.get("row_count") == count
         and value.get("row_sequence_sha256") == sequence
         and value.get("gzip_mtime") == 0
         and value.get("canonical_jsonl") is True,
         "result ledger descriptor:" + key)


def verify_math(candidate: Path, c15_path: Path, edge_path: Path) -> dict[str, Any]:
    result, result_record = document(candidate / "result.json", "result_sha256")
    need(result.get("schema") == RESULT_SCHEMA
         and result.get("status") == RESULT_STATUS
         and result.get("exact_census") == EXPECTED
         and result.get("formal_credit") == 0
         and result.get("manifest_authorized") is False,
         "candidate result exact semantics")

    old_path = candidate / "old_c15_component_to_post_component.jsonl.gz"
    old_to_post: dict[str, str] = {}
    old_sequence = hashlib.sha256(); prior = ""
    declared_old_counts: dict[str, int] = {}
    declared_old_hash: dict[str, str] = {}
    for row, claim in gzip_rows(old_path, OLD_SCHEMA, OLD_KEYS):
        old = row.get("old_C15_component_id"); post = row.get("post_C27R2_component_id")
        need(type(old) is str and old > prior and type(post) is str
             and post.startswith(POST_PREFIX), "old ledger ordering/IDs")
        need(type(row.get("post_C27R2_old_component_count")) is int
             and row["post_C27R2_old_component_count"] > 0
             and valid_sha(row.get("post_C27R2_old_component_ids_sha256")),
             "old ledger group declarations")
        old_to_post[old] = post; prior = old
        count = row["post_C27R2_old_component_count"]
        group_hash = row["post_C27R2_old_component_ids_sha256"]
        if post in declared_old_counts:
            need(declared_old_counts[post] == count
                 and declared_old_hash[post] == group_hash,
                 "old group declaration agreement")
        declared_old_counts[post] = count; declared_old_hash[post] = group_hash
        old_sequence.update(claim.encode("ascii") + b"\n")
    need(len(old_to_post) == EXPECTED["frozen_C15_components"], "old count")
    descriptor(result, "old_C15_component_to_post_component", old_path,
               len(old_to_post), old_sequence.hexdigest())

    dsu = DSU(sorted(old_to_post))
    edge_sequence = hashlib.sha256(); edge_count = merges = cycles = 0
    previous_key = ""
    seen_pairs: set[tuple[str, str]] = set()
    for row, claim in gzip_rows(edge_path, EDGE_SCHEMA, EDGE_KEYS):
        key = row.get("component_edge_key"); pair = row.get("ordered_C15_component_pair")
        need(type(key) is str and key > previous_key and type(pair) is list
             and len(pair) == 2 and all(type(x) is str for x in pair)
             and pair[0] < pair[1] and tuple(pair) not in seen_pairs
             and key == EDGE_PREFIX + digest(pair)
             and type(row.get("supporting_physical_proof_row_count")) is int
             and row["supporting_physical_proof_row_count"] > 0
             and valid_sha(row.get("supporting_physical_proof_row_sequence_sha256")),
             "edge ordering/key/pair/proof semantics")
        need(pair[0] in old_to_post and pair[1] in old_to_post,
             "edge pair in frozen component universe")
        seen_pairs.add(tuple(pair))
        if dsu.union(pair[0], pair[1]): merges += 1
        else: cycles += 1
        previous_key = key; edge_count += 1
        edge_sequence.update(claim.encode("ascii") + b"\n")
    need(edge_count == EXPECTED["proof_derived_component_edges"]
         and merges == EXPECTED["successful_DSU_merges"]
         and cycles == EXPECTED["cycle_edges"]
         and edge_sequence.hexdigest() == result.get("edge_row_sequence_sha256"),
         "edge/DSU exact closure")
    groups: dict[str, list[str]] = defaultdict(list)
    for old in sorted(old_to_post):
        groups[dsu.find(old)].append(old)
    need(len(groups) == EXPECTED["post_C27R2_components"], "DSU component count")
    expected_old_to_post: dict[str, str] = {}
    for old_ids in groups.values():
        ordered = sorted(old_ids)
        post = POST_PREFIX + hashlib.sha256(canonical(ordered)).hexdigest()
        group_hash = hashlib.sha256(canonical(ordered)).hexdigest()
        need(declared_old_counts.get(post) == len(ordered)
             and declared_old_hash.get(post) == group_hash,
             "canonical quotient declaration")
        for old in ordered: expected_old_to_post[old] = post
    need(expected_old_to_post == old_to_post, "canonical quotient exact mapping")

    member_path = candidate / "member_to_post_component.jsonl.gz"
    members_by_post: dict[str, int] = defaultdict(int)
    member_sequence = hashlib.sha256()
    member_count = 0
    c15_iter = gzip_rows(c15_path, C15_SCHEMA, C15_KEYS, False)
    member_iter = gzip_rows(member_path, MEMBER_SCHEMA, MEMBER_KEYS)
    for c15_pair, member_pair in zip(c15_iter, member_iter, strict=True):
        c15_row, _ = c15_pair
        row, claim = member_pair
        old = row.get("old_C15_component_id"); post = row.get("post_C27R2_component_id")
        member = row.get("registry_member_id")
        need(c15_row.get("member_ordinal") == member_count
             and row.get("member_ordinal") == member_count
             and row.get("ordinal") == member_count
             and type(member) is str
             and member == c15_row.get("registry_member_id")
             and old == c15_row.get("fresh_component_id")
             and old_to_post.get(old) == post,
             "frozen C15/member lockstep rebinding")
        members_by_post[post] += 1; member_count += 1
        member_sequence.update(claim.encode("ascii") + b"\n")
    need(member_count == EXPECTED["frozen_C15_members"], "member count")
    descriptor(result, "member_to_post_component", member_path, member_count,
               member_sequence.hexdigest())

    census_path = candidate / "post_component_census.jsonl.gz"
    census_sequence = hashlib.sha256(); census_count = total_members = within = 0
    seen_posts: set[str] = set(); previous_post = ""
    for row, claim in gzip_rows(census_path, CENSUS_SCHEMA, CENSUS_KEYS):
        post = row.get("post_C27R2_component_id")
        need(type(post) is str and post > previous_post and post not in seen_posts,
             "census ordering")
        need(row.get("member_count") == members_by_post.get(post)
             and row.get("old_C15_component_count") == declared_old_counts.get(post)
             and row.get("old_C15_component_ids_sha256") == declared_old_hash.get(post)
             and row.get("within_member_pair_count")
                 == row["member_count"] * (row["member_count"] - 1) // 2,
             "census independent aggregation")
        total_members += row["member_count"]
        within += row["within_member_pair_count"]
        census_count += 1; previous_post = post; seen_posts.add(post)
        census_sequence.update(claim.encode("ascii") + b"\n")
    need(census_count == EXPECTED["post_C27R2_components"]
         and total_members == EXPECTED["frozen_C15_members"]
         and sum(declared_old_counts[x] for x in seen_posts)
             == EXPECTED["frozen_C15_components"]
         and within == EXPECTED["within_post_component_member_pairs"],
         "census totals")
    descriptor(result, "post_component_census", census_path, census_count,
               census_sequence.hexdigest())
    total = member_count * (member_count - 1) // 2
    cross = total - within
    need(total == EXPECTED["total_unordered_member_pairs"]
         and cross == EXPECTED["cross_post_component_member_pairs"],
         "pair identity")
    return {"result_file_sha256": result_record["sha256"],
            "result_object_sha256": result["result_sha256"],
            "edge_file_sha256": record(edge_path)["sha256"],
            "old_rows": len(old_to_post), "member_rows": member_count,
            "census_rows": census_count, "edge_rows": edge_count,
            "merges": merges, "cycles": cycles, "within": within,
            "cross": cross}


def execute(args: argparse.Namespace) -> dict[str, Any]:
    need(FORMAL_EXECUTION_AUTHORIZED and BOUNDARY_CONTRACT_FROZEN_GO,
         "boundary v5 NO-GO; append-only boundary v6 independent GO required")
    pins = (args.expect_self_sha256, args.expect_plan_file_sha256,
        args.expect_plan_object_sha256, args.expect_manifest_receipt_file_sha256,
        args.expect_manifest_receipt_object_sha256,
        args.expect_payload_manifest_sha256, args.expect_root_manifest_sha256,
        args.expect_evidence_file_sha256, args.expect_evidence_object_sha256,
        args.expect_verification_file_sha256,
        args.expect_verification_object_sha256,
        args.expect_attacks_file_sha256, args.expect_attacks_object_sha256,
        args.expect_core_pinset_file_sha256, args.expect_core_pinset_object_sha256)
    need(all(valid_sha(value) for value in pins), "all exact SHA pins")
    need(self_independence() == args.expect_self_sha256,
         "self/no-import independence pin")

    plan_path = inside(args.plan)
    plan, plan_record = document(plan_path, "plan_sha256")
    need(plan_record["sha256"] == args.expect_plan_file_sha256
         and plan["plan_sha256"] == args.expect_plan_object_sha256
         and plan.get("schema") == PLAN_SCHEMA and plan.get("status") == PLAN_STATUS
         and plan.get("validator_negative_case_count") == 70
         and plan.get("publication_lock_preflight_case_count") == 8
         and plan.get("total_integrity_check_count") == 78
         and "case_count" not in plan
         and plan.get("ordered_validator70_object_sha256")
             == ORDERED_VALIDATOR70_OBJECT_SHA
         and plan.get("ordered_lock8_object_sha256") == ORDERED_LOCK8_OBJECT_SHA
         and plan.get("sources", {}).get("boundary_validator") == {
             "path": BOUNDARY_VALIDATOR_PATH, "sha256": BOUNDARY_VALIDATOR_SHA}
         and plan.get("sources", {}).get("integrity70_plus_lock8_runner") == {
             "path": INTEGRITY_RUNNER_PATH, "sha256": INTEGRITY_RUNNER_SHA}
         and plan.get("sources", {}).get("cold_runner") == {
             "path": COLD_RUNNER_PATH, "sha256": COLD_RUNNER_SHA}
         and record(inside(BOUNDARY_VALIDATOR_PATH))["sha256"]
             == BOUNDARY_VALIDATOR_SHA
         and record(inside(INTEGRITY_RUNNER_PATH))["sha256"]
             == INTEGRITY_RUNNER_SHA
         and record(inside(COLD_RUNNER_PATH))["sha256"] == COLD_RUNNER_SHA
         and plan.get("exact_math") == EXPECTED
         and plan.get("execution_enabled") is False
         and plan.get("formal_credit") == 0
         and plan.get("manifest_authorized") is False
         and plan.get("authority_minted") is False,
         "frozen v5 plan")

    manifest_dir = inside(args.manifest_dir)
    need(manifest_dir.is_dir() and {path.name for path in manifest_dir.iterdir()}
         == {"manifest_receipt.json", "payload_manifest.sha256",
             "root_manifest.sha256"}, "manifest exact inventory")
    manifest_receipt, manifest_record = document(
        manifest_dir / "manifest_receipt.json", "manifest_receipt_sha256")
    payload_path = manifest_dir / "payload_manifest.sha256"
    root_path = manifest_dir / "root_manifest.sha256"
    payload = parse_manifest(payload_path)
    root = parse_manifest(root_path)
    need(manifest_record["sha256"] == args.expect_manifest_receipt_file_sha256
         and manifest_receipt["manifest_receipt_sha256"]
             == args.expect_manifest_receipt_object_sha256
         and manifest_receipt.get("schema") == MANIFEST_SCHEMA
         and manifest_receipt.get("status") == MANIFEST_STATUS
         and manifest_receipt.get("plan_file_sha256")
             == args.expect_plan_file_sha256
         and manifest_receipt.get("plan_object_sha256")
             == args.expect_plan_object_sha256
         and record(payload_path)["sha256"] == args.expect_payload_manifest_sha256
         and record(root_path)["sha256"] == args.expect_root_manifest_sha256
         and manifest_receipt.get("payload_manifest_file_sha256")
             == args.expect_payload_manifest_sha256
         and manifest_receipt.get("root_manifest_file_sha256")
             == args.expect_root_manifest_sha256
         and manifest_receipt.get("payload_member_count") == len(payload)
         and manifest_receipt.get("root_member_count") == len(root)
         and manifest_receipt.get("validator_negative_case_count") == 70
         and manifest_receipt.get("validator_rejected_count") == 70
         and manifest_receipt.get("publication_lock_preflight_case_count") == 8
         and manifest_receipt.get("publication_lock_preflight_rejected_count") == 8
         and manifest_receipt.get("total_integrity_check_count") == 78
         and "case_count" not in manifest_receipt
         and manifest_receipt.get("accepted_count") == 0
         and manifest_receipt.get("exact_math") == EXPECTED
         and manifest_receipt.get("actual_v2_terminal_role")
             == "PREDECESSOR_EVIDENCE_ONLY"
         and manifest_receipt.get("actual_v2_terminal_authority_eligible") is False
         and manifest_receipt.get("historical_C27R2_terminal", {}).get(
             "authority_eligible") is False
         and manifest_receipt.get("historical_C27R2_terminal", {}).get(
             "included_in_authority_root") is False
         and manifest_receipt.get("formal_credit") == 0
         and manifest_receipt.get("manifest_authorized") is False
         and manifest_receipt.get("authority_minted") is False,
         "manifest exact status/crosslinks/governance")
    historical = manifest_receipt["historical_C27R2_terminal"]["path"]
    need(not any(path == historical or path.startswith(historical + "/")
                 for path in set(payload) | set(root)),
         "historical terminal absent from authority manifests")

    evidence_dir = inside(args.evidence_dir)
    evidence, evidence_record = document(
        evidence_dir / "post_integrity_evidence.json",
        "post_integrity_evidence_sha256")
    evidence_rows_raw, _ = capture(evidence_dir / "authority_records.jsonl")
    need(evidence_rows_raw.endswith(b"\n"), "evidence ledger newline")
    evidence_paths: set[str] = set()
    for ordinal, line in enumerate(evidence_rows_raw.splitlines()):
        row = strict(line); body = dict(row); claim = body.pop("row_sha256", None)
        need(type(row) is dict and canonical(row) == line
             and row.get("schema") == BASE + "post-authority-member-row.v5"
             and row.get("ordinal") == ordinal
             and valid_sha(claim) and claim == digest(body), "evidence row")
        current = record(inside(row["path"]))
        need(current["sha256"] == row["sha256"]
             and current["size"] == row["size"]
             and current["stat_fingerprint"] == row["stat_fingerprint"],
             "evidence current full9stat")
        evidence_paths.add(row["path"])
    need(evidence_record["sha256"] == args.expect_evidence_file_sha256
         and evidence["post_integrity_evidence_sha256"]
             == args.expect_evidence_object_sha256
         and evidence.get("schema") == EVIDENCE_SCHEMA
         and evidence.get("status") == EVIDENCE_STATUS
         and evidence.get("validator_negative_case_count") == 70
         and evidence.get("validator_rejected_count") == 70
         and evidence.get("publication_lock_preflight_case_count") == 8
         and evidence.get("publication_lock_preflight_rejected_count") == 8
         and evidence.get("total_integrity_check_count") == 78
         and "case_count" not in evidence
         and evidence.get("accepted_count") == 0
         and evidence.get("real_validator_wrapper_process_count") == 70
         and evidence.get("real_lock_preflight_process_count") == 8
         and evidence.get("case_process_transcripts_reopened") == 70
         and evidence.get("fixture_top_entry_count") == 73
         and evidence.get("fixture_control_member_count") == 5
         and evidence.get("fixture_top_and_control_exact_inventories_reopened")
             is True
         and evidence.get("authority_pre_post_sha_full9stat_identical") is True
         and evidence.get("private_fixture_root_count") == 0
         and evidence.get("case_cleanup_complete") is True
         and evidence.get("authority_record_count") == len(evidence_paths)
         and evidence.get("exact_math") == EXPECTED
         and evidence.get("formal_credit") == 0
         and evidence.get("manifest_authorized") is False
         and evidence_paths <= set(payload), "post validator70/lock8 closure")

    core_pinset_path = inside(args.core_pinset)
    core_pinset, core_pinset_record = document(core_pinset_path, "pinset_sha256")
    need(core_pinset_record["sha256"] == args.expect_core_pinset_file_sha256
         and core_pinset["pinset_sha256"] == args.expect_core_pinset_object_sha256,
         "core pinset file/object")
    authority = core_pinset.get("actual_v2_authority")
    need(type(authority) is dict
         and authority.get("frozen_C15_path") == C15_PATH
         and authority.get("frozen_C15_sha256") == C15_SHA
         and authority.get("seed1_edge_path") == SEED1_EDGE_PATH
         and authority.get("seed1_edge_sha256") == EDGE_SHA
         and authority.get("seed2_edge_path") == SEED2_EDGE_PATH
         and authority.get("seed2_edge_sha256") == EDGE_SHA,
         "core pinset exact C15/dual-edge authority")
    need(manifest_receipt.get("core_receipt_file_sha256")
             == CORE_RECEIPT_FILE_SHA
         and manifest_receipt.get("core_receipt_object_sha256")
             == CORE_RECEIPT_OBJECT_SHA
         and manifest_receipt.get("core_pinset_file_sha256")
             == args.expect_core_pinset_file_sha256
         and manifest_receipt.get("core_pinset_object_sha256")
             == args.expect_core_pinset_object_sha256,
         "manifest/core exact anchors")
    c15_path = inside(C15_PATH)
    seed1_edge = inside(SEED1_EDGE_PATH)
    seed2_edge = inside(SEED2_EDGE_PATH)
    c15_raw, c15_item = capture(c15_path)
    seed1_raw, seed1_item = capture(seed1_edge)
    seed2_raw, seed2_item = capture(seed2_edge)
    del c15_raw
    need(c15_item["sha256"] == C15_SHA
         and seed1_item["sha256"] == EDGE_SHA
         and seed2_item["sha256"] == EDGE_SHA
         and seed1_raw == seed2_raw
         and {c15_item["path"], seed1_item["path"], seed2_item["path"],
              record(core_pinset_path)["path"]}
             <= set(payload), "current dual-edge/C15 payload pins")

    candidate = inside(args.candidate_dir)
    need(candidate.is_dir() and {path.name for path in candidate.iterdir()}
         == CANDIDATE_NAMES, "candidate inventory")
    for name in CANDIDATE_NAMES:
        need(record(candidate / name)["path"] in payload, "candidate payload")
    math = verify_math(candidate, c15_path, seed1_edge)

    verification_path = inside(args.verification)
    verification, verification_record = document(verification_path,
                                                   "verification_sha256")
    attacks_path = inside(args.core_attacks)
    attacks_raw, attacks_record = capture(attacks_path)
    need(attacks_raw.endswith(b"\n"), "attacks newline")
    attacks = strict(attacks_raw[:-1])
    attacks_body = dict(attacks) if type(attacks) is dict else {}
    attacks_claim = attacks_body.pop("attack_harness_sha256", None)
    need(type(attacks) is dict and canonical(attacks) == attacks_raw[:-1]
         and valid_sha(attacks_claim) and attacks_claim == digest(attacks_body)
         and verification_record["sha256"]
             == args.expect_verification_file_sha256
         and verification["verification_sha256"]
             == args.expect_verification_object_sha256
         and verification.get("schema") == VERIFICATION_SCHEMA
         and verification.get("status") == VERIFICATION_STATUS
         and verification.get("producer_imported_or_executed") is False
         and verification.get("candidate_result_file_sha256")
             == math["result_file_sha256"]
         and verification.get("candidate_result_object_sha256")
             == math["result_object_sha256"]
         and verification.get("formal_credit") == 0
         and attacks_record["sha256"] == args.expect_attacks_file_sha256
         and attacks_claim == args.expect_attacks_object_sha256
         and attacks.get("schema") == ATTACK_SCHEMA
         and attacks.get("status") == ATTACK_STATUS
         and attacks.get("attack_count") == 21 and attacks.get("rejected") == 21
         and attacks.get("accepted") == 0
         and attacks.get("baseline_verification_file_sha256")
             == args.expect_verification_file_sha256
         and attacks.get("baseline_verification_object_sha256")
             == args.expect_verification_object_sha256
         and attacks.get("formal_credit") == 0
         and {record(verification_path)["path"], record(attacks_path)["path"]}
             <= set(payload), "verification/attacks exact object closure")

    output = inside(args.output_file, absent=True)
    need(not output.exists() and output.parent.is_dir()
         and not output.parent.is_symlink(), "fresh outer output")
    body = {"schema": OUTER_SCHEMA, "status": OUTER_STATUS,
        "plan_file_sha256": plan_record["sha256"],
        "plan_object_sha256": plan["plan_sha256"],
        "manifest_receipt_file_sha256": manifest_record["sha256"],
        "manifest_receipt_object_sha256":
            manifest_receipt["manifest_receipt_sha256"],
        "payload_manifest_file_sha256": record(payload_path)["sha256"],
        "root_manifest_file_sha256": record(root_path)["sha256"],
        "post_evidence_file_sha256": evidence_record["sha256"],
        "post_evidence_object_sha256":
            evidence["post_integrity_evidence_sha256"],
        "core_receipt_file_sha256": CORE_RECEIPT_FILE_SHA,
        "core_receipt_object_sha256": CORE_RECEIPT_OBJECT_SHA,
        "core_pinset_file_sha256": core_pinset_record["sha256"],
        "core_pinset_object_sha256": core_pinset["pinset_sha256"],
        "verification_file_sha256": verification_record["sha256"],
        "verification_object_sha256": verification["verification_sha256"],
        "attacks_file_sha256": record(attacks_path)["sha256"],
        "attacks_object_sha256": attacks["attack_harness_sha256"],
        "payload_members_reopened": len(payload),
        "root_members_reopened": len(root),
        "authority_evidence_members_reopened": len(evidence_paths),
        "no_core_or_builder_import_or_execution": True,
        "streamed_frozen_C15_and_candidate_members_in_lockstep": True,
        "streamed_three_candidate_ledgers_and_dual_identical_actual_v2_edges": True,
        "independent_math_replay": math, "exact_math": EXPECTED,
        "validator_negative_case_count": 70, "validator_rejected_count": 70,
        "publication_lock_preflight_case_count": 8,
        "publication_lock_preflight_rejected_count": 8,
        "total_integrity_check_count": 78, "accepted_count": 0,
        "actual_v2_terminal_role": "PREDECESSOR_EVIDENCE_ONLY",
        "historical_C27R2_terminal_authority_eligible": False,
        "outer_is_conditional_until_finalizer_service_clean_success": True,
        "formal_credit": 0, "manifest_authorized": False,
        "authority_minted": False, "C27R2": "AUDIT_HOLD_UNAUTHORIZED",
        "C28_C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM"}
    receipt = {**body, "outer_verification_sha256": digest(body)}
    write_once(output, canonical(receipt) + b"\n")
    return receipt


def self_test() -> dict[str, Any]:
    need(FORMAL_EXECUTION_AUTHORIZED is False
         and BOUNDARY_CONTRACT_FROZEN_GO is False,
         "development source remains launch-blocked on boundary v6 audit")
    try:
        _write_all(-1, b"x", lambda _fd, _raw: 0)
        raise Blocked("zero-progress writer unexpectedly accepted")
    except Blocked as error:
        need(str(error) == "write made positive progress",
             "zero-progress write fixture")
    need(self_independence() == record(SELF)["sha256"],
         "independence fixture")
    dsu = DSU(["a", "b", "c"])
    need(dsu.union("a", "b") and not dsu.union("b", "a")
         and dsu.union("b", "c") and len({dsu.find(x) for x in "abc"}) == 1,
         "DSU fixture")
    need(EXPECTED["frozen_C15_components"]
         - EXPECTED["successful_DSU_merges"]
         == EXPECTED["post_C27R2_components"]
         and EXPECTED["proof_derived_component_edges"]
         - EXPECTED["successful_DSU_merges"] == EXPECTED["cycle_edges"],
         "math fixture")
    with tempfile.TemporaryDirectory(dir=ROOT / ".cm2-runtime",
            prefix="c27r2-outer-v3-fixture-") as raw:
        path = Path(raw) / "tiny.jsonl.gz"
        body = {"schema": OLD_SCHEMA, "ordinal": 0,
                "old_C15_component_id": "old:a",
                "post_C27R2_component_id": POST_PREFIX + "0" * 64,
                "post_C27R2_old_component_count": 1,
                "post_C27R2_old_component_ids_sha256": "1" * 64,
                "formal_credit": 0}
        row = {**body, "row_sha256": digest(body)}
        with path.open("wb") as target:
            with gzip.GzipFile(filename="", mode="wb", fileobj=target,
                               mtime=0) as stream:
                stream.write(canonical(row) + b"\n")
        replay = list(gzip_rows(path, OLD_SCHEMA, OLD_KEYS))
        need(len(replay) == 1 and replay[0][0] == row,
             "tiny canonical gzip ledger fixture")
    return {"status": "PASS_C27R2_RELEASE_REPAIR_OUTER_V5_SELF_TEST"}


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--self-test", action="store_true")
    names = ("plan", "manifest-dir", "evidence-dir", "candidate-dir",
        "verification", "core-attacks", "core-pinset", "output-file",
        "expect-self-sha256", "expect-plan-file-sha256",
        "expect-plan-object-sha256",
        "expect-manifest-receipt-file-sha256",
        "expect-manifest-receipt-object-sha256",
        "expect-payload-manifest-sha256", "expect-root-manifest-sha256",
        "expect-evidence-file-sha256", "expect-evidence-object-sha256",
        "expect-verification-file-sha256",
        "expect-verification-object-sha256",
        "expect-attacks-file-sha256", "expect-attacks-object-sha256",
        "expect-core-pinset-file-sha256",
        "expect-core-pinset-object-sha256")
    for name in names:
        value.add_argument("--" + name)
    return value


def main() -> int:
    p = parser(); args = p.parse_args()
    names = [x.dest for x in p._actions if x.dest not in {"help", "self_test"}]
    try:
        if args.self_test:
            need(all(getattr(args, x) is None for x in names),
                 "self-test no arguments")
            result = self_test()
        else:
            need(all(getattr(args, x) is not None for x in names),
                 "all dynamic pins and paths required")
            result = execute(args)
        sys.stdout.buffer.write(canonical({"CM2": "NO-GO_FOR_CLAIM",
            "formal_credit": 0, "status": result["status"]}) + b"\n")
        return 0
    except (Blocked, OSError, ValueError, KeyError, TypeError,
            gzip.BadGzipFile) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
