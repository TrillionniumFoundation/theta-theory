#!/usr/bin/env python3
"""Independent preexecution audit for the corrected C65s18 v3 executor.

The assignment builder, authorization sealer, and shard executor are consumed
only as pinned inert bytes and AST.  None is imported or executed here.
"""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile
import threading
from typing import Any, Callable
import zlib


SELF = Path(__file__).resolve()
OUT = SELF.parent
DOMAIN = "cm2.round306c65s18.depth18-64shard.v2.assignment"
CONTRACT = OUT / "cm2_round306c65s18_independent_contract_v2.json"
BUILDER = OUT / "cm2_round306c65s18_assignment_builder_final_v2.py"
ASSIGNMENT = OUT / "cm2_round306c65s18_depth18_64shard_assignment_result_v2.json"
INVENTORY = OUT / "cm2_round306c65s18_depth18_64shard_assignment_inventory_v2.jsonl.gz"
SEALER = OUT / "cm2_round306c65s18_assignment_authorization_sealer_v2.py"
SEAL = OUT / "cm2_round306c65s18_assignment_authorization_seal_v2.json"
EXECUTOR = OUT / "cm2_round306c65s18_depth18_64shard_executor_v3.py"
SMOKE = OUT / "cm2_round306c65s18_preexecution_smoke_v3.json"
C61_RESULT = OUT / "cm2_round306c61s12_depth12_16shard_aggregate_result_v4.json"
C61_LEAVES = OUT / "cm2_round306c61s12_depth12_16shard_aggregate_leaf_ledger_v4.jsonl.gz"
C58_RESULT = OUT / "cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement_result_v1.json"
C58_LEAVES = OUT / "cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement_leaf_ledger_v1.jsonl.gz"
VERIFY_OUT = OUT / "cm2_round306c65s18_independent_preexecution_verification_v3.json"
SELFTEST_OUT = OUT / "cm2_round306c65s18_independent_preexecution_self_test_v3.json"
MAX_GZIP_OUTPUT = 512 * 1024 * 1024

PIN = {
    "contract_file": "e320ac48b1cf3675a3c152d0cb9e6084ba750433722fef716e4a8ab534fab287",
    "contract_object": "5d8a39432c2b02e807c5624ea26f56a12b58f66601ab391b52fee89d0ca604a4",
    "builder_file": "700326aee68f423b8e03a9f8adda95a07b811bab60e95bd159c8e46cc290794b",
    "assignment_file": "0306fd12de7d73988a45bac84acf70e4615e8e3aaef7c3c42a66fc39dbef4baa",
    "assignment_object": "c7671985713c8cfd8a496931f1b2686fa545448ce0a434c89e943b178000407f",
    "inventory_file": "e2c4714f1f1a8aa470a393d25ff03aaa3228f08979c30c90fd5f297469d6ad30",
    "sealer_file": "ae122914853a234dfc8a44bd915700ab0fcec7823fab7e5c7f5061b50cb865df",
    "seal_file": "99788b913ee8b900c97e14b6b52d90b0ad83ef2c3fddda6d9f82ab0aacc39ca0",
    "seal_object": "d1b508a54553b8944b50e926e895b35a589fe6aca3a03440e416571b339ca228",
    "executor_file": "170df261ed9451fc3ecc1fca5e686c6f6d8eeb3d643126da09f30c634cda22ef",
    "smoke_file": "a7f7c1f8ee4ed186f871d2981307a865ddc9a17d2e66868ef7f2d261e1a0128e",
    "smoke_object": "41af8efe4211a807264860a6917bcc9091184151c783d5ca17451afad88e948e",
    "C61_result_file": "06b4146185cb6ef0c8d908d523369008481f7df4e6a05ad5956c001267b07f5e",
    "C61_result_object": "05bcb4301ac74aefd6744db2e633c2479c423fab881b33609bf7234a5537e584",
    "C61_leaf_file": "2656bc4d1b99d37da3733338d85c8d6301621563a400d5db40380078c001b1c2",
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


def closed_stat(info: os.stat_result, label: str) -> tuple[int, ...]:
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "regular single-link:" + label)
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size,
            info.st_mtime_ns, info.st_ctime_ns)


def read_pinned(path: Path, pin: str) -> bytes:
    directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try:
        descriptor = os.open(path.name, os.O_RDONLY | os.O_CLOEXEC |
                             getattr(os, "O_NOFOLLOW", 0), dir_fd=directory)
        try:
            before = closed_stat(os.fstat(descriptor), path.name)
            chunks: list[bytes] = []
            while True:
                chunk = os.read(descriptor, 1 << 20)
                if not chunk:
                    break
                chunks.append(chunk)
            raw = b"".join(chunks)
            need(closed_stat(os.fstat(descriptor), path.name) == before and
                 closed_stat(os.stat(path.name, dir_fd=directory, follow_symlinks=False),
                             path.name) == before, "input fd/path identity:" + path.name)
            need(hashlib.sha256(raw).hexdigest() == pin, "input pin:" + path.name)
            return raw
        finally:
            os.close(descriptor)
    finally:
        os.close(directory)


def strict(raw: bytes) -> Any:
    need(not raw.startswith(b"\xef\xbb\xbf"), "BOM forbidden")

    def hook(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(key not in result, "duplicate JSON key:" + key)
            result[key] = value
        return result

    return json.loads(raw, object_pairs_hook=hook,
                      parse_constant=lambda value: (_ for _ in ()).throw(
                          FailClosed("nonfinite JSON:" + value)))


def object_file(path: Path, file_pin: str, object_pin: str) -> dict[str, Any]:
    value = strict(read_pinned(path, file_pin))
    need(type(value) is dict, "JSON object:" + path.name)
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
        need(line.endswith(b"\n") and line != b"\n", "JSONL framing:" + path.name)
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


def source_audit(raw: bytes, role: str) -> dict[str, Any]:
    text = raw.decode("utf-8")
    tree = ast.parse(text, filename=role)
    functions = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
    attributes = {node.attr for node in ast.walk(tree) if isinstance(node, ast.Attribute)}
    calls = []
    argparse_options: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            calls.append(node.func.attr if isinstance(node.func, ast.Attribute) else
                         (node.func.id if isinstance(node.func, ast.Name) else ""))
            if (isinstance(node.func, ast.Attribute) and node.func.attr == "add_argument" and
                    node.args and isinstance(node.args[0], ast.Constant) and
                    isinstance(node.args[0].value, str)):
                argparse_options.append(node.args[0].value)
    need("write_bytes" not in attributes and "write_text" not in attributes and
         "exists" not in attributes and "is_symlink" not in attributes,
         role + ":check-then-write/path convenience APIs forbidden")
    need(not ({"unlink", "remove", "rename", "replace", "rmdir", "rmtree",
               "system", "popen", "Popen", "run", "check_call", "check_output"} & set(calls)),
         role + ":destructive/process calls forbidden")
    need("O_EXCL" in text and "O_NOFOLLOW" in text and "dir_fd=" in text and
         "fstat" in calls and "fsync" in calls and "follow_symlinks=False" in text,
         role + ":exclusive fd/path publication primitives")
    if role == "executor":
        need("make_inventory" not in functions and "contract_check" not in functions,
             "executor read-only assignment boundary")
        need(argparse_options == ["--smoke", "--shard"] and
             "_leaf_ledger_v3.jsonl.gz" in text and "_receipt_v3.json" in text and
             'SCHEMA = "cm2.round306c65s18.depth18-64shard.v3"' in text and
             'ASSIGNMENT_DOMAIN = "cm2.round306c65s18.depth18-64shard.v2.assignment"' in text,
             "executor smoke/shard explicit-v3 targets with frozen-v2 assignment domain")
        need("zip(sources, inventory, strict=True)" in text and
             "global exact source/inventory bijection" in text and
             PIN["assignment_file"] in text and PIN["assignment_object"] in text and
             PIN["inventory_file"] in text and PIN["seal_file"] in text and
             PIN["seal_object"] in text and PIN["builder_file"] in text and
             PIN["sealer_file"] in text,
             "executor global replay and hard pins")
    return {"parsed": True, "functions": sorted(functions),
            "write_bytes_present": False, "write_text_present": False,
            "exists_present": False, "is_symlink_present": False,
            "O_EXCL_present": True, "O_NOFOLLOW_present": True,
            "dirfd_present": True, "fstat_present": True, "fsync_present": True,
            "argparse_options": argparse_options,
            "source_imported": False, "source_executed": False}


def verify() -> dict[str, Any]:
    contract = object_file(CONTRACT, PIN["contract_file"], PIN["contract_object"])
    builder_ast = source_audit(read_pinned(BUILDER, PIN["builder_file"]), "builder")
    sealer_ast = source_audit(read_pinned(SEALER, PIN["sealer_file"]), "sealer")
    executor_ast = source_audit(read_pinned(EXECUTOR, PIN["executor_file"]), "executor")
    assignment = object_file(ASSIGNMENT, PIN["assignment_file"], PIN["assignment_object"])
    seal = object_file(SEAL, PIN["seal_file"], PIN["seal_object"])
    need(assignment["assignment_builder_file_sha256"] == PIN["builder_file"] and
         assignment["inventory"]["sha256"] == PIN["inventory_file"] and
         assignment["independent_contract"] == {
             "file_sha256": PIN["contract_file"], "object_sha256": PIN["contract_object"]
         }, "assignment hard pins")
    need(seal["status"] ==
         "PASS_INDEPENDENT_FROZEN_ASSIGNMENT_BYTES_FOR_SHARD_EXECUTION__ZERO_CREDIT" and
         seal["assignment_result"] == {
             "file_sha256": PIN["assignment_file"], "object_sha256": PIN["assignment_object"]
         } and seal["assignment_inventory"]["file_sha256"] == PIN["inventory_file"] and
         seal["contract"] == {
             "file_sha256": PIN["contract_file"], "object_sha256": PIN["contract_object"]
         } and seal["candidate_is_authority"] is False,
         "authorization seal hard pins")
    smoke = object_file(SMOKE, PIN["smoke_file"], PIN["smoke_object"])
    expected_authority = {
        "C50d_global_claim": "3801e452f218e330bc16faed5986146202a7d7026e46924bf7bc00167b05f77b",
        "C50d_global_head": "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3",
        "C53_audit_token": "c3a9a3248b2ec3cb0887b62f4edade7664f73f1746593be1b69897404ae42eba",
        "C53_successor_token": "dcad8792bb4bede7f97f9996d10b43497b6286704dbc8f1b8a4170a9e2416846",
        "CM2_LATEST_STATUS.md": "922fc5d01918b217556bc3f392c44efcc7c9c6345c881371e6cd34950eb99b57",
        "CM2_LATEST_STATUS.sha256": "57d0c75a2dc774d312fc72a11c66e745cf9b7232531e469490bac492b0a91d6b",
    }
    need(smoke["schema"] ==
         "cm2.round306c65s18.depth18-64shard.v3.preexecution-smoke.v3" and
         smoke["status"] ==
         "PASS_REAL_INPUT_LOAD_GLOBAL_20879_BIJECTION_AND_ONE_EXACT_ROUTE__ZERO_WRITES_ZERO_CREDIT" and
         smoke["source_input_count"] == smoke["inventory_input_count"] == 20879 and
         smoke["shard_count"] == 64 and smoke["shard0_input_count"] == 330 and
         smoke["assignment_result_object_sha256"] == PIN["assignment_object"] and
         smoke["assignment_authorization_object_sha256"] == PIN["seal_object"] and
         smoke["shard_files_before"] == smoke["shard_files_after"] == [] and
         smoke["authority_snapshot_before"] == smoke["authority_snapshot_after"] ==
         expected_authority and smoke["authority_snapshot_object_sha256"] ==
         digest(expected_authority) ==
         "c9a8b97be4bed2008fa132f49e0d4ac0b384e973707ecdf48b27028b7d7e93cf" and
         smoke["candidate_is_authority"] is False and
         smoke["formal_credit"] == smoke["whole_parent_credit"] ==
         smoke["D02_gate_credit"] == 0 and
         smoke["runtime_canonical_pointer_or_seal_writes"] is False,
         "exact real v3 smoke and authority snapshot")

    inventory = rows(INVENTORY, PIN["inventory_file"], assignment["inventory"])
    c61_result = object_file(C61_RESULT, PIN["C61_result_file"], PIN["C61_result_object"])
    c61_rows = rows(C61_LEAVES, PIN["C61_leaf_file"],
                    c61_result["ledgers"]["aggregate_leaves"])
    sources = [row for row in c61_rows if row["disposition"] == "COLLISION2_HANDOFF"]
    c58_result = object_file(C58_RESULT, PIN["C58_result_file"], PIN["C58_result_object"])
    c58_rows = rows(C58_LEAVES, PIN["C58_leaf_file"], c58_result["ledgers"]["leaves"])
    c58_by_hash = {row["row_sha256"]: row for row in c58_rows}
    need(len(c58_by_hash) == len(c58_rows) and len(sources) == len(inventory) == 20879,
         "exact source/inventory cardinality")

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
        c58 = c58_by_hash.get(source["source_C58_leaf_row_sha256"])
        need(c58 is not None and c58["disposition"] == "COLLISION2_HANDOFF" and
             c58["source_handoff_ordinal"] == source["source_handoff_ordinal"] and
             c58["path"] == source["source_path"] and source["path"].startswith(c58["path"]) and
             c58["pair_index"] == source["pair_index"] and
             source["continuation"]["prior_C58_leaf_row_sha256"] == c58["row_sha256"] and
             source["continuation"]["prior_C58_handoff_object_sha256"] ==
             c58["collision2_handoff"]["handoff_object_sha256"],
             "exact C61/C58 lineage")
        need(assigned["source_C61_aggregate_leaf_row_sha256"] == source_sha and
             assigned["source_C61_continuation_object_sha256"] ==
             source["continuation"]["continuation_object_sha256"] and
             assigned["source_C61_source_shard_row_sha256"] == source["source_shard_row_sha256"] and
             assigned["source_C58_leaf_row_sha256"] == source["source_C58_leaf_row_sha256"] and
             assigned["source_handoff_ordinal"] == source["source_handoff_ordinal"] and
             assigned["source_path"] == source["source_path"] and
             assigned["path"] == source["path"] and assigned["pair_index"] == source["pair_index"] and
             assigned["parent_volume_fraction"] == source["parent_volume_fraction"] and
             assigned["source_C61_disposition"] == "COLLISION2_HANDOFF" and
             assigned["source_C61_next_collision_index"] == 2 and
             assigned["assignment_preimage_sha256"] == claim and assigned["shard_id"] == shard,
             "exact source/inventory row replay")
        need(assigned["assignment_credit"] == assigned["formal_credit"] ==
             assigned["whole_parent_credit"] == assigned["D02_gate_credit"] == 0,
             "inventory zero credit")
        counts[shard] += 1
        claims.update((claim + "\n").encode("ascii"))
        source_sequence.update((source_sha + "\n").encode("ascii"))
        continuation_sequence.update(
            (source["continuation"]["continuation_object_sha256"] + "\n").encode("ascii"))
    expected_counts = {str(index): count for index, count in enumerate(counts)}
    need(len(seen) == sum(counts) == 20879 and all(counts) and
         assignment["per_shard_input_counts"] == seal["assignment"]["per_shard_input_counts"] ==
         expected_counts and assignment["ordered_preimage_sha256_line_sequence_sha256"] ==
         seal["assignment"]["ordered_preimage_sha256_line_sequence_sha256"] ==
         claims.hexdigest(), "global assignment replay")
    need(assignment["filtered_source_row_sha256_line_sequence_sha256"] ==
         seal["source"]["filtered_source_row_sha256_line_sequence_sha256"] ==
         contract["selection"]["filtered_source_row_sha256_line_sequence_sha256"] ==
         source_sequence.hexdigest() and
         assignment["filtered_continuation_object_sha256_line_sequence_sha256"] ==
         seal["source"]["filtered_continuation_object_sha256_line_sequence_sha256"] ==
         contract["selection"]["filtered_continuation_object_sha256_line_sequence_sha256"] ==
         continuation_sequence.hexdigest(), "filtered source sequences")
    need(assignment["formal_credit"] == assignment["whole_parent_credit"] ==
         assignment["D02_gate_credit"] == seal["formal_credit"] ==
         seal["whole_parent_credit"] == seal["D02_gate_credit"] == 0 and
         assignment["candidate_is_authority"] is False and
         assignment["runtime_canonical_pointer_or_seal_writes"] is False and
         seal["runtime_canonical_pointer_or_seal_writes"] is False,
         "strict zero-credit/no-runtime boundary")
    value: dict[str, Any] = {
        "schema": "cm2.round306c65s18.independent-preexecution-verifier.v3.verification",
        "status": "PASS_INDEPENDENT_FINAL_V3_EXECUTION_CHAIN__REAL_SMOKE__20879_TO_64_GLOBAL_BIJECTION__ATOMIC_NO_REPLACE_AST__ZERO_CREDIT",
        "contract": {"file_sha256": PIN["contract_file"],
                     "object_sha256": PIN["contract_object"]},
        "assignment_builder": {"file_sha256": PIN["builder_file"],
                               "consumed_as_inert_bytes_and_AST_only": True,
                               "imported": False, "executed": False, "AST_audit": builder_ast},
        "assignment": {"result_file_sha256": PIN["assignment_file"],
                       "result_object_sha256": PIN["assignment_object"],
                       "inventory_file_sha256": PIN["inventory_file"],
                       "input_count": 20879, "shard_count": 64,
                       "per_shard_input_counts": expected_counts,
                       "minimum_shard_input_count": min(counts),
                       "maximum_shard_input_count": max(counts),
                       "complete": True, "mutually_exclusive": True,
                       "source_identity_bijection": True,
                       "ordered_preimage_sha256_line_sequence_sha256": claims.hexdigest()},
        "authorization_sealer": {"file_sha256": PIN["sealer_file"],
                                 "consumed_as_inert_bytes_and_AST_only": True,
                                 "imported": False, "executed": False, "AST_audit": sealer_ast},
        "authorization_seal": {"file_sha256": PIN["seal_file"],
                               "object_sha256": PIN["seal_object"]},
        "executor": {"file_sha256": PIN["executor_file"],
                     "consumed_as_inert_bytes_and_AST_only": True,
                     "imported": False, "executed": False, "AST_audit": executor_ast,
                     "shards_executed_before_authorization": 0},
        "real_smoke": {"file_sha256": PIN["smoke_file"],
                       "object_sha256": PIN["smoke_object"],
                       "source_input_count": 20879, "shard0_input_count": 330,
                       "one_exact_route_replayed": True,
                       "zero_shard_outputs": True,
                       "authority_snapshot_object_sha256":
                           smoke["authority_snapshot_object_sha256"],
                       "authority_snapshot_unchanged": True},
        "partial_shards_are_an_aggregate": False,
        "candidate_is_authority": False,
        "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
        "runtime_canonical_pointer_or_seal_writes": False,
    }
    value["object_sha256"] = digest(value)
    return value


def atomic_publish(path: Path, raw: bytes) -> None:
    directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try:
        flags = os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(path.name, flags, 0o644, dir_fd=directory)
        try:
            view = memoryview(raw)
            while view:
                count = os.write(descriptor, view)
                need(count > 0, "short atomic write")
                view = view[count:]
            os.fsync(descriptor)
            expected = closed_stat(os.fstat(descriptor), path.name)
            need(closed_stat(os.stat(path.name, dir_fd=directory, follow_symlinks=False),
                             path.name) == expected, "atomic fd/path identity")
            os.lseek(descriptor, 0, os.SEEK_SET)
            replay = b""
            while True:
                block = os.read(descriptor, 1 << 20)
                if not block:
                    break
                replay += block
            need(replay == raw and closed_stat(os.fstat(descriptor), path.name) == expected,
                 "atomic byte replay")
            os.fsync(directory)
        finally:
            os.close(descriptor)
    finally:
        os.close(directory)


def expect_fail(name: str, action: Callable[[], Any], tests: list[dict[str, Any]]) -> None:
    try:
        action()
    except (FailClosed, FileExistsError, OSError, TypeError, ValueError, zlib.error):
        tests.append({"name": name, "status": "PASS_FAIL_CLOSED"})
        return
    raise FailClosed("hostile test accepted:" + name)


def self_test() -> dict[str, Any]:
    baseline = verify()
    tests: list[dict[str, Any]] = []

    def passed(name: str, condition: bool) -> None:
        need(condition, "self-test:" + name)
        tests.append({"name": name, "status": "PASS"})

    sample_sha = "0" * 64
    exact = (b'{"assignment_domain":"cm2.round306c65s18.depth18-64shard.v2.assignment",'
             b'"path":"000000000000000000000","source_C61_aggregate_leaf_row_sha256":'
             b'"0000000000000000000000000000000000000000000000000000000000000000"}')
    passed("canonical_preimage_exact", preimage(sample_sha, "0" * 21) == exact)
    passed("canonical_preimage_no_newline", not exact.endswith(b"\n"))
    passed("preimage_deterministic", preimage(sample_sha, "0" * 21) ==
           preimage(sample_sha, "0" * 21))
    passed("source_mutation_changes_claim", hashlib.sha256(preimage(sample_sha, "0" * 21)).hexdigest() !=
           hashlib.sha256(preimage("1" + "0" * 63, "0" * 21)).hexdigest())
    passed("path_mutation_changes_claim", hashlib.sha256(preimage(sample_sha, "0" * 21)).hexdigest() !=
           hashlib.sha256(preimage(sample_sha, "1" + "0" * 20)).hexdigest())
    expect_fail("uppercase_hash", lambda: preimage("A" * 64, "0" * 21), tests)
    expect_fail("short_hash", lambda: preimage("0" * 63, "0" * 21), tests)
    expect_fail("short_path", lambda: preimage(sample_sha, "0" * 20), tests)
    expect_fail("long_path", lambda: preimage(sample_sha, "0" * 22), tests)
    expect_fail("nonbinary_path", lambda: preimage(sample_sha, "0" * 20 + "2"), tests)
    expect_fail("duplicate_JSON_key", lambda: strict(b'{"a":1,"a":2}'), tests)
    expect_fail("NaN_JSON", lambda: strict(b'{"a":NaN}'), tests)
    expect_fail("Infinity_JSON", lambda: strict(b'{"a":Infinity}'), tests)
    expect_fail("BOM_JSON", lambda: strict(b'\xef\xbb\xbf{}'), tests)
    expect_fail("truncated_gzip", lambda: gunzip(b"\x1f\x8b", "test"), tests)

    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        good = root / "good.json"
        raw = b'{"ok":true}\n'
        atomic_publish(good, raw)
        passed("atomic_success_bytes", good.read_bytes() == raw)
        passed("atomic_success_regular", stat.S_ISREG(good.lstat().st_mode))
        passed("atomic_success_single_link", good.stat().st_nlink == 1)
        expect_fail("preexisting_regular", lambda: atomic_publish(good, raw), tests)
        symlink = root / "symlink.json"
        symlink.symlink_to(good)
        expect_fail("preexisting_symlink", lambda: atomic_publish(symlink, raw), tests)
        hardlink = root / "hardlink.json"
        os.link(good, hardlink)
        expect_fail("preexisting_hardlink", lambda: atomic_publish(hardlink, raw), tests)
        fifo = root / "fifo.json"
        os.mkfifo(fifo)
        expect_fail("preexisting_FIFO", lambda: atomic_publish(fifo, raw), tests)
        directory = root / "directory.json"
        directory.mkdir()
        expect_fail("preexisting_directory", lambda: atomic_publish(directory, raw), tests)
        race = root / "race.json"
        outcomes: list[str] = []

        def contender(index: int) -> None:
            try:
                atomic_publish(race, canonical({"winner": index}) + b"\n")
                outcomes.append("winner")
            except FileExistsError:
                outcomes.append("blocked")

        threads = [threading.Thread(target=contender, args=(index,)) for index in range(8)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        passed("race_exact_one_winner", outcomes.count("winner") == 1)
        passed("race_seven_blocked", outcomes.count("blocked") == 7)
        passed("race_output_regular", stat.S_ISREG(race.lstat().st_mode))
        passed("race_output_single_link", race.stat().st_nlink == 1)

    passed("verification_object_closes", baseline["object_sha256"] ==
           digest({key: value for key, value in baseline.items() if key != "object_sha256"}))
    passed("input_count", baseline["assignment"]["input_count"] == 20879)
    passed("shard_count", baseline["assignment"]["shard_count"] == 64)
    passed("count_sum", sum(baseline["assignment"]["per_shard_input_counts"].values()) == 20879)
    passed("all_shards_nonempty", all(baseline["assignment"]["per_shard_input_counts"].values()))
    passed("minimum_shard_count", baseline["assignment"]["minimum_shard_input_count"] == 295)
    passed("maximum_shard_count", baseline["assignment"]["maximum_shard_input_count"] == 379)
    passed("assignment_complete", baseline["assignment"]["complete"] is True)
    passed("assignment_mutually_exclusive", baseline["assignment"]["mutually_exclusive"] is True)
    passed("source_identity_bijection", baseline["assignment"]["source_identity_bijection"] is True)
    passed("executor_not_imported", baseline["executor"]["imported"] is False)
    passed("executor_not_executed", baseline["executor"]["executed"] is False)
    passed("executor_zero_shards_before_auth", baseline["executor"]["shards_executed_before_authorization"] == 0)
    passed("real_smoke_object", baseline["real_smoke"]["object_sha256"] == PIN["smoke_object"])
    passed("real_smoke_20879", baseline["real_smoke"]["source_input_count"] == 20879)
    passed("real_smoke_shard0_330", baseline["real_smoke"]["shard0_input_count"] == 330)
    passed("real_smoke_one_route", baseline["real_smoke"]["one_exact_route_replayed"] is True)
    passed("real_smoke_zero_outputs", baseline["real_smoke"]["zero_shard_outputs"] is True)
    passed("real_smoke_authority_unchanged", baseline["real_smoke"]["authority_snapshot_unchanged"] is True)
    passed("executor_no_write_bytes", baseline["executor"]["AST_audit"]["write_bytes_present"] is False)
    passed("executor_no_exists_gate", baseline["executor"]["AST_audit"]["exists_present"] is False)
    passed("executor_O_EXCL", baseline["executor"]["AST_audit"]["O_EXCL_present"] is True)
    passed("executor_O_NOFOLLOW", baseline["executor"]["AST_audit"]["O_NOFOLLOW_present"] is True)
    passed("executor_fsync", baseline["executor"]["AST_audit"]["fsync_present"] is True)
    passed("builder_not_executed", baseline["assignment_builder"]["executed"] is False)
    passed("sealer_not_executed", baseline["authorization_sealer"]["executed"] is False)
    passed("candidate_not_authority", baseline["candidate_is_authority"] is False)
    passed("partial_not_aggregate", baseline["partial_shards_are_an_aggregate"] is False)
    passed("formal_credit_zero", baseline["formal_credit"] == 0)
    passed("whole_parent_credit_zero", baseline["whole_parent_credit"] == 0)
    passed("D02_gate_credit_zero", baseline["D02_gate_credit"] == 0)
    passed("no_runtime_writes", baseline["runtime_canonical_pointer_or_seal_writes"] is False)
    need(len(tests) == 59, "exactly 59 self-tests")
    value: dict[str, Any] = {
        "schema": "cm2.round306c65s18.independent-preexecution-verifier.v3.self-test",
        "status": "PASS_59_OF_59_REAL_SMOKE_ATOMIC_RACE_SYMLINK_LINK_SCHEMA_AND_INVARIANT_TESTS",
        "verification_object_sha256": baseline["object_sha256"],
        "tests": tests, "passed": 59, "failed": 0,
        "builder_imported": False, "builder_executed": False,
        "sealer_imported": False, "sealer_executed": False,
        "executor_imported": False, "executor_executed": False,
        "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
        "runtime_canonical_pointer_or_seal_writes": False,
    }
    value["object_sha256"] = digest(value)
    return value


def publish(path: Path, value: dict[str, Any]) -> None:
    atomic_publish(path, canonical(value) + b"\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--verify", action="store_true")
    group.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        value = verify() if args.verify else self_test()
        publish(VERIFY_OUT if args.verify else SELFTEST_OUT, value)
        print(json.dumps({"status": value["status"], "object_sha256": value["object_sha256"]},
                         sort_keys=True, separators=(",", ":")))
        return 0
    except (FailClosed, KeyError, OSError, TypeError, ValueError, zlib.error) as error:
        print(json.dumps({"status": "FAIL_CLOSED", "reason": str(error)},
                         sort_keys=True, separators=(",", ":")))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
