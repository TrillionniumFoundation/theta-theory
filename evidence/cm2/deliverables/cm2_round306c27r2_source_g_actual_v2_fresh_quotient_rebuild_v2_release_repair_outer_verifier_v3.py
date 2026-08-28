#!/usr/bin/env python3
"""No-import streaming outer verifier for the C27R2 release repair v3.

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
EVIDENCE_SCHEMA = BASE + "post-attack-evidence-closure.v3"
MANIFEST_SCHEMA = BASE + "manifest-receipt.v3"
OUTER_SCHEMA = BASE + "outer-verification.v3"
OUTER_STATUS = ("PASS_INDEPENDENT_C27R2_RELEASE_REPAIR_FULL_LEDGER_EDGE_DSU_"
                "MANIFEST_BOUNDARY_CASE_AND_TRUST_REPLAY__CONDITIONAL_ZERO_"
                "CREDIT_PENDING_TERMINAL")
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
OLD_SCHEMA = ("cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild."
              "v2.old-c15-component-to-post-component-row.v1")
MEMBER_SCHEMA = ("cm2.round306c27r2.source-g-actual-v2-fresh-quotient-"
                 "rebuild.v2.member-to-post-component-row.v1")
CENSUS_SCHEMA = ("cm2.round306c27r2.source-g-actual-v2-fresh-quotient-"
                 "rebuild.v2.post-component-census-row.v1")
EDGE_SCHEMA = ("cm2.c27-independent.primitive-twenty-family-gate-v5-actual."
               "full-component-edge-union.row.v2")
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


def record(path: Path) -> dict[str, Any]:
    need(path.is_file() and not path.is_symlink(), "regular current file")
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "single-link current file")
        state = hashlib.sha256()
        while block := os.read(fd, 4 << 20):
            state.update(block)
        need(fingerprint(os.stat(path, follow_symlinks=False))
             == fingerprint(before), "stable current file")
        return {"path": str(path.relative_to(ROOT)), "sha256": state.hexdigest(),
                "size": before.st_size, "stat_fingerprint": fingerprint(before)}
    finally:
        os.close(fd)


def document(path: Path, closure: str) -> tuple[dict[str, Any], dict[str, Any]]:
    item = record(path)
    raw = path.read_bytes()
    need(raw.endswith(b"\n"), "JSON newline")
    value = strict(raw[:-1])
    need(type(value) is dict and canonical(value) == raw[:-1], "canonical JSON")
    body = dict(value); claim = body.pop(closure, None)
    need(valid_sha(claim) and claim == digest(body), "object closure:" + closure)
    return value, item


def parse_manifest(path: Path) -> dict[str, dict[str, Any]]:
    raw = path.read_bytes()
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
    raw = SELF.read_bytes()
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


def gzip_rows(path: Path, schema: str) -> Iterator[tuple[dict[str, Any], str]]:
    raw_record = record(path)
    with path.open("rb") as source:
        header = source.read(10)
    need(len(header) == 10 and header[:3] == b"\x1f\x8b\x08"
         and header[4:8] == b"\x00\x00\x00\x00", "deterministic gzip header")
    del raw_record
    with gzip.open(path, "rb") as stream:
        ordinal = 0
        while line := stream.readline():
            need(line.endswith(b"\n"), "JSONL newline")
            row = strict(line[:-1])
            need(type(row) is dict and canonical(row) + b"\n" == line,
                 "canonical JSONL")
            body = dict(row); claim = body.pop("row_sha256", None)
            need(valid_sha(claim) and claim == digest(body)
                 and row.get("schema") == schema
                 and row.get("ordinal") == ordinal
                 and row.get("formal_credit") == 0,
                 "row schema/ordinal/closure")
            yield row, claim
            ordinal += 1


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
    need(type(value) is dict and value.get("filename") == path.name
         and value.get("sha256") == record(path)["sha256"]
         and value.get("size") == path.stat().st_size
         and value.get("row_count") == count
         and value.get("row_sequence_sha256") == sequence
         and value.get("gzip_mtime") == 0
         and value.get("canonical_jsonl") is True,
         "result ledger descriptor:" + key)


def verify_math(candidate: Path, edge_path: Path) -> dict[str, Any]:
    result, result_record = document(candidate / "result.json", "result_sha256")
    need(result.get("schema") == RESULT_SCHEMA
         and result.get("exact_census") == EXPECTED
         and result.get("formal_credit") == 0
         and result.get("manifest_authorized") is False,
         "candidate result exact semantics")

    old_path = candidate / "old_c15_component_to_post_component.jsonl.gz"
    old_to_post: dict[str, str] = {}
    old_sequence = hashlib.sha256(); prior = ""
    declared_old_counts: dict[str, int] = {}
    declared_old_hash: dict[str, str] = {}
    for row, claim in gzip_rows(old_path, OLD_SCHEMA):
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
    for row, claim in gzip_rows(edge_path, EDGE_SCHEMA):
        key = row.get("component_edge_key"); pair = row.get("ordered_C15_component_pair")
        need(type(key) is str and key > previous_key and type(pair) is list
             and len(pair) == 2 and all(type(x) is str for x in pair)
             and pair[0] < pair[1], "edge ordering/pair")
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
    member_ids: set[str] = set(); member_sequence = hashlib.sha256()
    member_count = 0
    for row, claim in gzip_rows(member_path, MEMBER_SCHEMA):
        old = row.get("old_C15_component_id"); post = row.get("post_C27R2_component_id")
        member = row.get("registry_member_id")
        need(row.get("member_ordinal") == member_count
             and type(member) is str and member not in member_ids
             and old_to_post.get(old) == post, "member rebinding")
        member_ids.add(member); members_by_post[post] += 1; member_count += 1
        member_sequence.update(claim.encode("ascii") + b"\n")
    need(member_count == EXPECTED["frozen_C15_members"], "member count")
    descriptor(result, "member_to_post_component", member_path, member_count,
               member_sequence.hexdigest())

    census_path = candidate / "post_component_census.jsonl.gz"
    census_sequence = hashlib.sha256(); census_count = total_members = within = 0
    seen_posts: set[str] = set(); previous_post = ""
    for row, claim in gzip_rows(census_path, CENSUS_SCHEMA):
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
    sha_args = (args.expect_self_sha256,
        args.expect_manifest_receipt_file_sha256,
        args.expect_manifest_receipt_object_sha256,
        args.expect_payload_manifest_sha256, args.expect_root_manifest_sha256,
        args.expect_evidence_file_sha256, args.expect_evidence_object_sha256,
        args.expect_boundary_file_sha256, args.expect_boundary_object_sha256,
        args.expect_case_file_sha256, args.expect_case_object_sha256,
        args.expect_post_file_sha256, args.expect_post_object_sha256,
        args.expect_decision_file_sha256, args.expect_decision_object_sha256)
    need(all(valid_sha(x) for x in sha_args), "all dynamic SHA pins")
    need(self_independence() == args.expect_self_sha256, "self/independence pin")
    dynamic_strings = (args.boundary_closure_key, args.expect_boundary_schema,
        args.expect_boundary_status, args.case_closure_key, args.expect_case_schema,
        args.expect_case_status, args.post_closure_key, args.expect_post_schema,
        args.expect_post_status, args.decision_closure_key,
        args.expect_decision_schema, args.expect_decision_status)
    need(all(type(x) is str and x for x in dynamic_strings), "dynamic strings")

    manifest_dir = inside(args.manifest_dir)
    need(manifest_dir.is_dir() and {x.name for x in manifest_dir.iterdir()}
         == {"manifest_receipt.json", "payload_manifest.sha256",
             "root_manifest.sha256"}, "manifest exact inventory")
    manifest_receipt, manifest_record = document(
        manifest_dir / "manifest_receipt.json", "manifest_receipt_sha256")
    payload_path = manifest_dir / "payload_manifest.sha256"
    root_path = manifest_dir / "root_manifest.sha256"
    payload = parse_manifest(payload_path); root = parse_manifest(root_path)
    need(manifest_record["sha256"] == args.expect_manifest_receipt_file_sha256
         and manifest_receipt["manifest_receipt_sha256"]
             == args.expect_manifest_receipt_object_sha256
         and manifest_receipt.get("schema") == MANIFEST_SCHEMA
         and record(payload_path)["sha256"] == args.expect_payload_manifest_sha256
         and record(root_path)["sha256"] == args.expect_root_manifest_sha256
         and manifest_receipt.get("payload_manifest_file_sha256")
             == args.expect_payload_manifest_sha256
         and manifest_receipt.get("root_manifest_file_sha256")
             == args.expect_root_manifest_sha256
         and manifest_receipt.get("payload_member_count") == len(payload)
         and manifest_receipt.get("root_member_count") == len(root)
         and manifest_receipt.get("exact_math") == EXPECTED
         and manifest_receipt.get("actual_v2_terminal_role")
             == "PREDECESSOR_EVIDENCE_ONLY"
         and manifest_receipt.get("actual_v2_terminal_authority_eligible") is False
         and manifest_receipt.get("historical_C27R2_terminal", {}).get(
             "authority_eligible") is False
         and manifest_receipt.get("historical_C27R2_terminal", {}).get(
             "included_in_authority_root") is False
         and manifest_receipt.get("formal_credit") == 0,
         "manifest receipt/root semantics")
    need(not any("c27r2-release-chain-v1-formal-r1-20260808T183910-terminal"
                 in path for path in set(payload) | set(root)),
         "historical terminal absent from manifests")

    evidence_dir = inside(args.evidence_dir)
    evidence, evidence_record = document(
        evidence_dir / "post_attack_evidence.json",
        "post_attack_evidence_sha256")
    inventory = parse_manifest(evidence_dir / "authority_inventory.sha256")
    need(evidence_record["sha256"] == args.expect_evidence_file_sha256
         and evidence["post_attack_evidence_sha256"]
             == args.expect_evidence_object_sha256
         and evidence.get("schema") == EVIDENCE_SCHEMA
         and evidence.get("authority_inventory_member_count") == len(inventory)
         and evidence.get("exact_math") == EXPECTED
         and evidence.get("real_case_count") == 44
         and evidence.get("real_cases_rejected") == 44
         and evidence.get("authority_pre_post_sha_stat_identical") is True
         and evidence.get("case_cleanup_complete") is True
         and set(inventory) <= set(payload), "evidence/current inventory closure")

    boundary_path = inside(args.boundary_receipt)
    boundary, boundary_record = document(boundary_path, args.boundary_closure_key)
    case_path = inside(args.case_receipt)
    cases, case_record = document(case_path, args.case_closure_key)
    post_path = inside(args.post_receipt)
    post, post_record = document(post_path, args.post_closure_key)
    decision_path = inside(args.trust_decision)
    decision, decision_record = document(decision_path, args.decision_closure_key)
    need(boundary_record["sha256"] == args.expect_boundary_file_sha256
         and boundary[args.boundary_closure_key] == args.expect_boundary_object_sha256
         and boundary.get("schema") == args.expect_boundary_schema
         and boundary.get("status") == args.expect_boundary_status
         and boundary.get("formal_credit") == 0
         and case_record["sha256"] == args.expect_case_file_sha256
         and cases[args.case_closure_key] == args.expect_case_object_sha256
         and cases.get("schema") == args.expect_case_schema
         and cases.get("status") == args.expect_case_status
         and cases.get("rejected_count", cases.get("rejected"))
             == cases.get("case_count", cases.get("total"))
         and cases.get("case_count", cases.get("total")) == 44
         and post_record["sha256"] == args.expect_post_file_sha256
         and post[args.post_closure_key] == args.expect_post_object_sha256
         and post.get("schema") == args.expect_post_schema
         and post.get("status") == args.expect_post_status
         and post.get("baseline_equivalent") is True
         and post.get("authority_pre_post_sha_stat_identical") is True
         and post.get("cleanup_complete") is True
         and post.get("formal_credit") == 0
         and decision_record["sha256"] == args.expect_decision_file_sha256
         and decision[args.decision_closure_key]
             == args.expect_decision_object_sha256
         and decision.get("schema") == args.expect_decision_schema
         and decision.get("status") == args.expect_decision_status
         and decision.get("eligible_as_predecessor_evidence") is True
         and decision.get("authority_eligible") is False
         and decision.get("old_C27R2_authority_eligible") is False
         and decision.get("process_and_cold_current_byte_closure_verified") is True
         and decision.get("formal_credit") == 0,
         "front-half exact receipts")
    need({record(boundary_path)["path"], record(case_path)["path"],
          record(post_path)["path"],
          record(decision_path)["path"], record(SELF)["path"]} <= set(payload),
         "front-half/outer sources in payload")

    candidate = inside(args.candidate_dir)
    need(candidate.is_dir() and {x.name for x in candidate.iterdir()}
         == CANDIDATE_NAMES, "candidate inventory")
    for name in CANDIDATE_NAMES:
        need(record(candidate / name)["path"] in payload, "candidate in payload")
    edge_path = inside(args.edge_ledger)
    need(record(edge_path)["path"] in payload, "edge ledger in payload")
    math = verify_math(candidate, edge_path)

    verification_path = inside(args.verification)
    verification, _ = document(verification_path, "verification_sha256")
    attacks_path = inside(args.core_attacks)
    attacks_raw = attacks_path.read_bytes()
    need(attacks_raw.endswith(b"\n"), "attacks newline")
    attacks = strict(attacks_raw[:-1])
    need(type(attacks) is dict and canonical(attacks) == attacks_raw[:-1]
         and verification.get("producer_imported_or_executed") is False
         and verification.get("formal_credit") == 0
         and attacks.get("attack_count") == 21 and attacks.get("rejected") == 21
         and attacks.get("accepted") == 0 and attacks.get("formal_credit") == 0
         and record(verification_path)["path"] in payload
         and record(attacks_path)["path"] in payload,
         "core independent verification/attacks")

    output = inside(args.output_file, absent=True)
    need(not output.exists() and output.parent.is_dir()
         and not output.parent.is_symlink(), "fresh outer output")
    body = {"schema": OUTER_SCHEMA, "status": OUTER_STATUS,
        "manifest_receipt_file_sha256": manifest_record["sha256"],
        "manifest_receipt_object_sha256":
            manifest_receipt["manifest_receipt_sha256"],
        "payload_manifest_file_sha256": record(payload_path)["sha256"],
        "root_manifest_file_sha256": record(root_path)["sha256"],
        "post_attack_evidence_file_sha256": evidence_record["sha256"],
        "post_attack_evidence_object_sha256":
            evidence["post_attack_evidence_sha256"],
        "boundary_receipt_object_sha256": boundary[args.boundary_closure_key],
        "case_receipt_object_sha256": cases[args.case_closure_key],
        "post_receipt_object_sha256": post[args.post_closure_key],
        "decision_object_sha256": decision[args.decision_closure_key],
        "payload_members_reopened": len(payload), "root_members_reopened": len(root),
        "authority_inventory_members_reopened": len(inventory),
        "no_core_or_builder_import_or_execution": True,
        "streamed_three_candidate_ledgers_and_actual_v2_edge_ledger": True,
        "independent_math_replay": math, "exact_math": EXPECTED,
        "actual_v2_terminal_role": "PREDECESSOR_EVIDENCE_ONLY",
        "historical_C27R2_terminal_authority_eligible": False,
        "outer_is_conditional_until_independent_terminal_byte_replay": True,
        "formal_credit": 0, "manifest_authorized": False,
        "authority_minted": False, "C27R2": "AUDIT_HOLD_UNAUTHORIZED",
        "C28_C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM"}
    receipt = {**body, "outer_verification_sha256": digest(body)}
    fd = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                 | getattr(os, "O_NOFOLLOW", 0), 0o400)
    try:
        os.write(fd, canonical(receipt) + b"\n"); os.fsync(fd)
    finally:
        os.close(fd)
    return receipt


def self_test() -> dict[str, Any]:
    need(self_independence() == hashlib.sha256(SELF.read_bytes()).hexdigest(),
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
        replay = list(gzip_rows(path, OLD_SCHEMA))
        need(len(replay) == 1 and replay[0][0] == row,
             "tiny canonical gzip ledger fixture")
    return {"status": "PASS_C27R2_RELEASE_REPAIR_OUTER_V3_SELF_TEST"}


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--self-test", action="store_true")
    names = ("manifest-dir", "evidence-dir", "candidate-dir", "verification",
        "core-attacks", "edge-ledger", "boundary-receipt", "case-receipt",
        "post-receipt", "trust-decision", "output-file", "boundary-closure-key",
        "case-closure-key", "post-closure-key", "decision-closure-key",
        "expect-boundary-schema",
        "expect-boundary-status", "expect-case-schema", "expect-case-status",
        "expect-post-schema", "expect-post-status",
        "expect-decision-schema", "expect-decision-status", "expect-self-sha256",
        "expect-manifest-receipt-file-sha256",
        "expect-manifest-receipt-object-sha256",
        "expect-payload-manifest-sha256", "expect-root-manifest-sha256",
        "expect-evidence-file-sha256", "expect-evidence-object-sha256",
        "expect-boundary-file-sha256", "expect-boundary-object-sha256",
        "expect-case-file-sha256", "expect-case-object-sha256",
        "expect-post-file-sha256", "expect-post-object-sha256",
        "expect-decision-file-sha256", "expect-decision-object-sha256")
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
