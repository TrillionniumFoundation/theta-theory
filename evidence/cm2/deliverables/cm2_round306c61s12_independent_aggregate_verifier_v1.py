#!/usr/bin/env python3
"""Fail-closed C61s12 16-shard aggregate audit harness.

The pre-execution contract remains frozen, and this post-execution verifier
pins the final runner, all 16 receipts/ledgers, and aggregate v4 only.  It
independently reconstructs assignment, source and parent partitions plus all
v4 aggregate rows.  Producers are inert bytes/AST and never imported or run;
forensic failed aggregate stages v1--v3 are explicitly rejected.
"""

from __future__ import annotations

import argparse
import ast
import copy
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
from typing import Any, Callable, Iterable
import zlib


sys.dont_write_bytecode = True
SELF = Path(__file__).absolute()
OUT = SELF.parent
CONTRACT = OUT / "cm2_round306c61s12_independent_contract_v1.json"
SCHEMA = "cm2.round306c61s12.independent-16-shard-aggregate-verifier.v1"
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
SHARDS = tuple(range(16))
EXPECTED_CONTRACT_OBJECT = "68c6e8a0899c66056724ea29c42949100b2fc6a625865867fd30aacc16d36f7d"

# Deliberately fail-closed until the producer is frozen.  These are not
# wildcards and must never be filled from a live or partial shard run.
EXPECTED_PRODUCER_SCHEMA = "cm2.round306c61s12.depth12-16shard.v1"
EXPECTED_PRODUCER_SHA256 = "7788155920c088f769b4a61d66be0c7951495e88f2d3676acca8f93a2ca531e4"
EXPECTED_RESULT_SCHEMA = EXPECTED_PRODUCER_SCHEMA + ".assignment-result"
EXPECTED_RESULT_SHA256 = "7d6fae044bd194c790dfc5dba077481d47e3e6850455463bfd61c8832e29ca69"
EXPECTED_RESULT_OBJECT = "d1f9549826fa424bd2c29fc217e714527c2e56ac25361e48f31d95aa33536d19"
EXPECTED_INVENTORY_SHA256 = "6ad0fe4d52c468de31fb39f72eabd825320eee86b9738f52fb1142da8a1736b4"
EXPECTED_SHARD_LEDGER_PATTERN = "cm2_round306c61s12_depth12_16shard_shard_{shard:02d}_leaf_ledger_v1.jsonl.gz"
EXPECTED_RECEIPT_PATTERN = "cm2_round306c61s12_depth12_16shard_shard_{shard:02d}_receipt_v1.json"
PRODUCER = OUT / "cm2_round306c61s12_depth12_16shard_runner_v1.py"
ASSIGNMENT_RESULT = OUT / "cm2_round306c61s12_depth12_16shard_assignment_result_v1.json"
ASSIGNMENT_INVENTORY = OUT / "cm2_round306c61s12_depth12_16shard_assignment_inventory_v1.jsonl.gz"
C58_RESULT = OUT / "cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement_result_v1.json"
C58_LEAVES = OUT / "cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement_leaf_ledger_v1.jsonl.gz"
C57_RESULT = OUT / "cm2_round306c57s1_singleton_collision1_common_refinement_result_v1.json"
C57_LEAVES = OUT / "cm2_round306c57s1_singleton_collision1_common_refinement_leaf_ledger_v1.jsonl.gz"
EXPECTED_C58_RESULT_SHA256 = "ed4eb1e5ea64c61e4b85a710c1429a2f0b489048320badd4d9a8214bc38c05bc"
EXPECTED_C58_RESULT_OBJECT = "038503bd21505dacde4ce6dc59a320fa70a97cc0dccce33be210c60bbd7d0a30"
EXPECTED_C58_LEAF_SHA256 = "15a5b1c5c15f8528591bd80be040317590dadec70b4476d01eb3763ae64965df"
EXPECTED_C57_RESULT_SHA256 = "9881c22ac4a8630b90b8eb16d81c1670bb6f544e5f4666197d0e6047771d8c4c"
EXPECTED_C57_RESULT_OBJECT = "8cda7681bcbe93c065f1f336842e9fffa6bd3ea67268e96d95fcb3d1f8cbbb58"
EXPECTED_C57_LEAF_SHA256 = "918899a914ad4fbb05c1095cac9f42f6c46d02f0acdad366538a395021aeaee6"
AGGREGATE_PRODUCER = OUT / "cm2_round306c61s12_depth12_16shard_aggregate_v1.py"
AGGREGATE_RESULT = OUT / "cm2_round306c61s12_depth12_16shard_aggregate_result_v4.json"
AGGREGATE_LEAVES = OUT / "cm2_round306c61s12_depth12_16shard_aggregate_leaf_ledger_v4.jsonl.gz"
AGGREGATE_SOURCES = OUT / "cm2_round306c61s12_depth12_16shard_aggregate_source_summary_v4.jsonl.gz"
AGGREGATE_PARENTS = OUT / "cm2_round306c61s12_depth12_16shard_aggregate_parent_summary_v4.jsonl.gz"
EXPECTED_AGGREGATE_PRODUCER_SHA256 = "742e4fb66ff751f606203a90e3a2e9d3935909011444e2b346f11d1e63b18849"
EXPECTED_AGGREGATE_RESULT_SHA256 = "06b4146185cb6ef0c8d908d523369008481f7df4e6a05ad5956c001267b07f5e"
EXPECTED_AGGREGATE_RESULT_OBJECT = "05bcb4301ac74aefd6744db2e633c2479c423fab881b33609bf7234a5537e584"
EXPECTED_AGGREGATE_LEAF_SHA256 = "2656bc4d1b99d37da3733338d85c8d6301621563a400d5db40380078c001b1c2"
EXPECTED_AGGREGATE_SOURCE_SHA256 = "477a60ace952d70dd81f46a97cb6ebf38797a3ec90e72eda7f6a67455fb789d7"
EXPECTED_AGGREGATE_PARENT_SHA256 = "2206c817f49312c519a720e14bc2e152cde5362ed884cbe83d32349a7ff5bab2"
REJECTIONS = {
    OUT / "cm2_round306c61s12_depth12_16shard_aggregate_v1_REJECTED_INCOMPLETE_C57_CARRY.md":
        "9e1742b5f86240087c425e8888ae7f03db2cc104e7aa1d8e8118fd0b06d4fd25",
    OUT / "cm2_round306c61s12_depth12_16shard_aggregate_v2_REJECTED_C57_DISPOSITION_ACCESSOR.md":
        "5e2c43ef092cc938c44625631cb0c37aa46a24dfeaa566b60abc5ef217d6839a",
    OUT / "cm2_round306c61s12_depth12_16shard_aggregate_v3_REJECTED_RESULT_SERIALIZATION_NAME_COLLISION.md":
        "da7551d89733adeecbf237090a382b2f82d348b8fac7191e35b20dbb03470110",
}


class Rejected(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def close(value: dict[str, Any]) -> dict[str, Any]:
    answer = copy.deepcopy(value)
    need("object_sha256" not in answer, "already closed")
    answer["object_sha256"] = digest(answer)
    return answer


def duplicate_guard(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in items:
        if key in result:
            raise Rejected("duplicate key:" + key)
        result[key] = value
    return result


def parse(raw: bytes, label: str, canonical_required: bool = False) -> Any:
    need(bool(raw) and not raw.startswith(b"\xef\xbb\xbf"), label + " strict bytes")
    try:
        value = json.loads(
            raw.decode("utf-8", "strict"), object_pairs_hook=duplicate_guard,
            parse_constant=lambda token: (_ for _ in ()).throw(Rejected(label + ":" + token)),
        )
    except Rejected:
        raise
    except Exception as exc:
        raise Rejected(label + " JSON:" + str(exc)) from exc
    if canonical_required:
        need(raw == canonical(value) + b"\n", label + " canonical bytes")
    return value


def closed(raw: bytes, object_pin: str, label: str) -> dict[str, Any]:
    value = parse(raw, label, canonical_required=True)
    need(type(value) is dict and value.get("object_sha256") == object_pin,
         label + " object claim")
    body = copy.deepcopy(value)
    body.pop("object_sha256")
    need(digest(body) == object_pin, label + " object reconstruction")
    return value


def ledger(raw: bytes, descriptor: dict[str, Any], file_pin: str,
           label: str) -> list[dict[str, Any]]:
    need(hashlib.sha256(raw).hexdigest() == descriptor.get("sha256") == file_pin,
         label + " file pin")
    decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
    try:
        expanded = decoder.decompress(raw, 768 << 20) + decoder.flush()
    except zlib.error as exc:
        raise Rejected(label + " gzip:" + str(exc)) from exc
    need(decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail,
         label + " one gzip member")
    lines = expanded.splitlines(keepends=True)
    need(len(lines) == descriptor.get("row_count"), label + " row count")
    sequence = hashlib.sha256()
    rows: list[dict[str, Any]] = []
    for line in lines:
        row = parse(line, label + " row", canonical_required=True)
        need(type(row) is dict and HEX64.fullmatch(str(row.get("row_sha256"))) is not None,
             label + " row claim")
        body = copy.deepcopy(row)
        claim = body.pop("row_sha256")
        need(digest(body) == claim, label + " row closure")
        sequence.update((claim + "\n").encode("ascii"))
        rows.append(row)
    need(sequence.hexdigest() == descriptor.get("row_hash_line_sequence_sha256"),
         label + " row sequence")
    return rows


def assignment_preimage(source_handoff_ordinal: int, path: str) -> bytes:
    need(type(source_handoff_ordinal) is int and source_handoff_ordinal >= 0,
         "assignment ordinal")
    need(type(path) is str and bool(path) and set(path) <= {"0", "1"},
         "assignment path")
    # canonical() supplies UTF-8, no trailing newline, sorted keys, exact compact
    # separators, and ensure_ascii=False.
    return canonical({"path": path, "source_handoff_ordinal": source_handoff_ordinal})


def assignment(source_handoff_ordinal: int, path: str) -> int:
    return int(hashlib.sha256(assignment_preimage(source_handoff_ordinal, path)).hexdigest(), 16) % 16


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink, value.st_size,
            value.st_mtime_ns, value.st_ctime_ns)


def capture(paths: Iterable[Path], maximum: int = 512 << 20,
            hook: Callable[[], None] | None = None) -> dict[Path, bytes]:
    ordered = tuple(paths)
    need(len(ordered) == len(set(ordered)), "duplicate capture path")
    descriptors: dict[Path, int] = {}
    before: dict[Path, os.stat_result] = {}
    try:
        for path in ordered:
            descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) |
                                 getattr(os, "O_NOFOLLOW", 0))
            state = os.fstat(descriptor)
            need(stat.S_ISREG(state.st_mode) and state.st_nlink == 1 and
                 0 < state.st_size <= maximum, "single-link frozen input:" + str(path))
            descriptors[path] = descriptor
            before[path] = state
        result: dict[Path, bytes] = {}
        for path in ordered:
            blocks: list[bytes] = []
            while block := os.read(descriptors[path], 4 << 20):
                blocks.append(block)
            result[path] = b"".join(blocks)
        if hook is not None:
            hook()
        for path in ordered:
            need(fingerprint(before[path]) == fingerprint(os.fstat(descriptors[path])) ==
                 fingerprint(os.stat(path, follow_symlinks=False)), "TOCTOU:" + str(path))
        return result
    finally:
        for descriptor in descriptors.values():
            os.close(descriptor)


def producer_independence(raw: bytes, path: Path,
                          expected_sha256: str = EXPECTED_PRODUCER_SHA256) -> None:
    need(hashlib.sha256(raw).hexdigest() == expected_sha256,
         "frozen producer source pin")
    tree = ast.parse(raw.decode("utf-8", "strict"), filename=path.name)
    dynamic: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {
            "exec", "eval", "compile", "__import__",
        }:
            dynamic.append(node.func.id)
    need(not dynamic and path.stem not in sys.modules, "producer no-import/no-execute")


def contract() -> dict[str, Any]:
    raw = capture((CONTRACT,), maximum=1 << 20)[CONTRACT]
    value = closed(raw, EXPECTED_CONTRACT_OBJECT, "C61 independent contract")
    need(value["assignment"] == {
        "hash": "SHA256", "modulus": 16,
        "preimage": {
            "encoding": "UTF-8", "ensure_ascii": False,
            "json_separators": [",", ":"], "keys_lexicographically_sorted": True,
            "schema": {"path": "JSON string", "source_handoff_ordinal": "integer"},
            "trailing_newline": False,
        },
        "shard_id_formula": "int(SHA256(preimage),16)%16",
    }, "exact assignment contract")
    need(value["shard_count"] == 16 and
         value["audit_requirements"]["C58_exact_residual_input_count"] == 2599 and
         value["audit_requirements"]["shard_ids_exactly"] == list(SHARDS),
         "contract census")
    return value


def pins_ready() -> None:
    values = (
        EXPECTED_PRODUCER_SCHEMA, EXPECTED_PRODUCER_SHA256,
        EXPECTED_RESULT_SCHEMA, EXPECTED_RESULT_SHA256, EXPECTED_RESULT_OBJECT,
        EXPECTED_SHARD_LEDGER_PATTERN, EXPECTED_RECEIPT_PATTERN,
    )
    need(all(not value.startswith("PENDING_") for value in values),
         "awaiting exact frozen C61s12 producer/result/shard/receipt schema pins")
    need(HEX64.fullmatch(EXPECTED_PRODUCER_SHA256) is not None and
         HEX64.fullmatch(EXPECTED_RESULT_SHA256) is not None and
         HEX64.fullmatch(EXPECTED_RESULT_OBJECT) is not None,
         "frozen hash pins")


def assignment_verify() -> dict[str, Any]:
    paths = (PRODUCER, ASSIGNMENT_RESULT, ASSIGNMENT_INVENTORY, C58_RESULT, C58_LEAVES)
    raw = capture(paths, maximum=32 << 20)
    producer_independence(raw[PRODUCER], PRODUCER)
    result = closed(raw[ASSIGNMENT_RESULT], EXPECTED_RESULT_OBJECT, "assignment result")
    need(hashlib.sha256(raw[ASSIGNMENT_RESULT]).hexdigest() == EXPECTED_RESULT_SHA256 and
         result["schema"] == EXPECTED_RESULT_SCHEMA and result["input_count"] == 2599 and
         result["shard_count"] == 16 and result["assignment_complete"] is True and
         result["assignment_mutually_exclusive"] is True and
         result["formal_credit"] == result["whole_parent_credit"] ==
         result["D02_gate_credit"] == 0, "assignment result semantics")
    inventory = ledger(raw[ASSIGNMENT_INVENTORY], result["inventory"],
                       EXPECTED_INVENTORY_SHA256, "assignment inventory")
    c58 = closed(raw[C58_RESULT], EXPECTED_C58_RESULT_OBJECT, "C58 result")
    need(hashlib.sha256(raw[C58_RESULT]).hexdigest() == EXPECTED_C58_RESULT_SHA256,
         "C58 result file pin")
    c58_rows = ledger(raw[C58_LEAVES], c58["ledgers"]["leaves"],
                      EXPECTED_C58_LEAF_SHA256, "C58 leaves")
    residual = [row for row in c58_rows if row["disposition"] == "COLLISION2_HANDOFF"]
    by_hash = {row["row_sha256"]: row for row in residual}
    need(len(residual) == len(by_hash) == len(inventory) == 2599,
         "2599 source/inventory bijection census")
    seen: set[tuple[int, str]] = set()
    counts = [0] * 16
    preimage_sequence = hashlib.sha256()
    for row in inventory:
        source = by_hash.get(row["C58_leaf_row_sha256"])
        need(source is not None, "inventory C58 foreign key")
        key = (row["source_handoff_ordinal"], row["path"])
        need(key not in seen and key == (source["source_handoff_ordinal"], source["path"]),
             "inventory/source complete mutually exclusive key")
        seen.add(key)
        preimage = assignment_preimage(*key)
        claim = hashlib.sha256(preimage).hexdigest()
        shard = int(claim, 16) % 16
        need(row["assignment_preimage_sha256"] == claim and row["shard_id"] == shard and
             row["C58_handoff_object_sha256"] ==
             source["collision2_handoff"]["handoff_object_sha256"] and
             row["pair_index"] == source["pair_index"] and
             row["parent_volume_fraction"] == source["parent_volume_fraction"] and
             row["assignment_credit"] == row["D02_gate_credit"] == 0,
             "independent assignment row reconstruction")
        counts[shard] += 1
        preimage_sequence.update((claim + "\n").encode("ascii"))
    expected_counts = {str(index): count for index, count in enumerate(counts)}
    need(len(seen) == 2599 and set(row["C58_leaf_row_sha256"] for row in inventory) == set(by_hash) and
         all(counts) and sum(counts) == 2599 and
         result["per_shard_input_counts"] == expected_counts and
         preimage_sequence.hexdigest() ==
         result["ordered_preimage_sha256_line_sequence_sha256"],
         "assignment union/intersection/count/sequence")
    return {
        "producer_file_sha256": EXPECTED_PRODUCER_SHA256,
        "assignment_result_file_sha256": EXPECTED_RESULT_SHA256,
        "assignment_result_object_sha256": EXPECTED_RESULT_OBJECT,
        "assignment_inventory_sha256": EXPECTED_INVENTORY_SHA256,
        "input_count": 2599, "shard_count": 16,
        "per_shard_input_counts": expected_counts,
        "assignment_complete": True, "assignment_mutually_exclusive": True,
    }


def prefix_free(paths: list[str]) -> bool:
    ordered = sorted(paths, key=lambda value: (len(value), value))
    return all(not later.startswith(first) for index, first in enumerate(ordered)
               for later in ordered[index + 1:])


def shard_paths() -> tuple[Path, ...]:
    return tuple(
        OUT / pattern.format(shard=shard)
        for shard in SHARDS
        for pattern in (EXPECTED_SHARD_LEDGER_PATTERN, EXPECTED_RECEIPT_PATTERN)
    )


def verify_shards() -> dict[str, Any]:
    # Refuse partial sets; exact 32-file capture is one TOCTOU snapshot.
    paths = shard_paths()
    need(all(path.exists() for path in paths), "awaiting all 16 shard ledgers and receipts")
    raw = capture(paths, maximum=128 << 20)
    assignment_raw = capture((ASSIGNMENT_RESULT, ASSIGNMENT_INVENTORY), maximum=32 << 20)
    assignment_result = closed(assignment_raw[ASSIGNMENT_RESULT], EXPECTED_RESULT_OBJECT,
                               "assignment result")
    inventory = ledger(assignment_raw[ASSIGNMENT_INVENTORY], assignment_result["inventory"],
                       EXPECTED_INVENTORY_SHA256, "assignment inventory")
    by_shard = {shard: [row for row in inventory if row["shard_id"] == shard]
                for shard in SHARDS}
    all_rows: list[dict[str, Any]] = []
    receipts: list[dict[str, Any]] = []
    global_disposition: dict[str, int] = {
        "STRICT_TERMINAL": 0, "COLLISION3_READY": 0, "COLLISION2_HANDOFF": 0,
    }
    global_route_count = 0
    for shard in SHARDS:
        ledger_path = OUT / EXPECTED_SHARD_LEDGER_PATTERN.format(shard=shard)
        receipt_path = OUT / EXPECTED_RECEIPT_PATTERN.format(shard=shard)
        receipt_value = parse(raw[receipt_path], f"shard {shard} receipt", canonical_required=True)
        need(type(receipt_value) is dict and type(receipt_value.get("object_sha256")) is str,
             "receipt object claim")
        body = copy.deepcopy(receipt_value)
        claim = body.pop("object_sha256")
        need(claim == digest(body), "receipt closure")
        receipt = receipt_value
        rows = ledger(raw[ledger_path], receipt["output_ledger"],
                      receipt["output_ledger"]["sha256"], f"shard {shard} ledger")
        assigned = by_shard[shard]
        need(receipt["schema"] == EXPECTED_PRODUCER_SCHEMA + ".shard-receipt" and
             receipt["status"] == "PASS_COMPLETE_NO_REPLACE_SHARD" and
             receipt["shard_id"] == shard and receipt["shard_count"] == 16 and
             receipt["assignment_contract_object_sha256"] == EXPECTED_CONTRACT_OBJECT and
             receipt["assignment_result_object_sha256"] == EXPECTED_RESULT_OBJECT and
             receipt["assignment_inventory_sha256"] == EXPECTED_INVENTORY_SHA256 and
             receipt["assigned_input_count"] == len(assigned) and
             receipt["shard_complete"] is True and
             receipt["partial_statistics_are_formal_credit"] is False and
             receipt["formal_credit"] == receipt["whole_parent_credit"] ==
             receipt["D02_gate_credit"] == 0 and
             receipt["runtime_canonical_pointer_or_seal_writes"] is False,
             "receipt schema/bindings/credit")
        assigned_hashes = [row["assignment_preimage_sha256"] for row in assigned]
        need(receipt["ordered_assignment_preimage_sha256_line_sequence_sha256"] ==
             hashlib.sha256("".join(value + "\n" for value in assigned_hashes).encode("ascii")).hexdigest(),
             "receipt assignment sequence")
        rows_by_source: dict[str, list[dict[str, Any]]] = {}
        for row in rows:
            need(row["schema"] == EXPECTED_PRODUCER_SCHEMA + ".shard-leaf-row" and
                 row["shard_id"] == shard and row["disposition"] in global_disposition and
                 row["formal_credit"] == row["whole_parent_credit"] ==
                 row["D02_gate_credit"] == 0, "shard row schema/disposition/credit")
            continuation = row["continuation"]
            if row["disposition"] == "STRICT_TERMINAL":
                need(continuation is None and row["local_terminal_credit"] == 1,
                     "strict terminal continuation")
            else:
                need(type(continuation) is dict and row["local_terminal_credit"] == 0,
                     "continuation object")
                open_continuation = copy.deepcopy(continuation)
                continuation_claim = open_continuation.pop("continuation_object_sha256", None)
                need(continuation_claim == digest(open_continuation) and
                     continuation["next_collision_index"] ==
                     (3 if row["disposition"] == "COLLISION3_READY" else 2) and
                     continuation["exact_representative_box"] == row["exact_representative_box"] and
                     continuation["exact_reflected_box"] == row["exact_reflected_box"] and
                     continuation["route_classification"] == row["route_classification"] and
                     continuation["route_witness"] == row["route_witness"] and
                     continuation["route_method"] == row["route_method"] and
                     continuation["continuation_credit"] == 0,
                     "continuation closure/index/exact binding")
            global_disposition[row["disposition"]] += 1
            rows_by_source.setdefault(row["source_C58_leaf_row_sha256"], []).append(row)
        need(set(rows_by_source) == {row["C58_leaf_row_sha256"] for row in assigned},
             "shard source coverage")
        summaries = receipt["input_assignment_rows"]
        need(len(summaries) == len(assigned), "receipt source summary count")
        for assignment_row, summary in zip(assigned, summaries):
            source_rows = rows_by_source[assignment_row["C58_leaf_row_sha256"]]
            need(all(row["assignment_preimage_sha256"] ==
                     assignment_row["assignment_preimage_sha256"] for row in source_rows),
                 "source assignment binding")
            paths_for_source = [row["path"] for row in source_rows]
            kraft = sum(Fraction(row["parent_volume_fraction"]) for row in source_rows)
            row_sequence = hashlib.sha256(
                "".join(row["row_sha256"] + "\n" for row in source_rows).encode("ascii")
            ).hexdigest()
            need(prefix_free(paths_for_source) and kraft == Fraction(assignment_row["parent_volume_fraction"]) and
                 summary == {
                     "assignment_preimage_sha256": assignment_row["assignment_preimage_sha256"],
                     "source_C58_leaf_row_sha256": assignment_row["C58_leaf_row_sha256"],
                     "source_output_row_count": len(source_rows),
                     "source_output_row_hash_line_sequence_sha256": row_sequence,
                     "source_Kraft_conservation": assignment_row["parent_volume_fraction"],
                     "source_prefix_free": True,
                 }, "per-source prefix/Kraft/summary")
        observed_census = {key: sum(row["disposition"] == key for row in rows)
                           for key in global_disposition}
        need(receipt["output_disposition_census"] == observed_census and
             receipt["route_evaluation_count"] >= len(rows), "receipt derived census/routes")
        global_route_count += receipt["route_evaluation_count"]
        all_rows.extend(rows)
        receipts.append(receipt)
    need(len(receipts) == 16 and sum(receipt["assigned_input_count"] for receipt in receipts) == 2599 and
         sum(global_disposition.values()) == len(all_rows), "global 16-receipt census")
    return {
        "receipt_count": 16, "input_count": 2599, "output_leaf_count": len(all_rows),
        "route_evaluation_count": global_route_count,
        "output_disposition_census": global_disposition,
        "all_per_source_prefix_free_and_Kraft_conserved": True,
        "all_continuations_closed_and_exactly_bound": True,
        "all_receipts_closed_complete_and_zero_credit": True,
        "rows": all_rows,
    }


def verify() -> dict[str, Any]:
    frozen = contract()
    pins_ready()
    assignment_result = assignment_verify()
    shard_result = verify_shards()
    c58_raw = capture((C58_RESULT, C58_LEAVES, C57_RESULT, C57_LEAVES), maximum=32 << 20)
    c58_result = closed(c58_raw[C58_RESULT], EXPECTED_C58_RESULT_OBJECT, "C58 result")
    c58_rows = ledger(c58_raw[C58_LEAVES], c58_result["ledgers"]["leaves"],
                      EXPECTED_C58_LEAF_SHA256, "C58 leaves")
    carried = [row for row in c58_rows if row["disposition"] == "STRICT_TERMINAL"]
    need(len(carried) == 2949, "C58 carried terminal census")
    c57_result = closed(c58_raw[C57_RESULT], EXPECTED_C57_RESULT_OBJECT, "C57 result")
    need(hashlib.sha256(c58_raw[C57_RESULT]).hexdigest() == EXPECTED_C57_RESULT_SHA256,
         "C57 result file pin")
    c57_rows = ledger(c58_raw[C57_LEAVES], c57_result["ledgers"]["leaves"],
                      EXPECTED_C57_LEAF_SHA256, "C57 leaves")
    c57_carried = [row for row in c57_rows if row["leaf_disposition"] == "STRICT_TERMINAL"]
    need(len(c57_carried) == 462, "C57 carried terminal census")
    pairs = (31, 188, 200, 270, 321, 410, 471, 474, 631, 711, 787, 853)
    combined_by_pair: dict[int, list[dict[str, Any]]] = {pair: [] for pair in pairs}
    for row in c57_carried:
        combined_by_pair[row["pair_index"]].append(row)
    for row in carried:
        combined_by_pair[row["pair_index"]].append(row)
    for row in shard_result["rows"]:
        combined_by_pair[row["pair_index"]].append(row)
    parent_census: dict[str, dict[str, Any]] = {}
    whole_pairs_terminal = 0
    for pair in pairs:
        rows = combined_by_pair[pair]
        paths = [row["path"] for row in rows]
        kraft = sum(Fraction(row["parent_volume_fraction"]) for row in rows)
        def disposition_of(row: dict[str, Any]) -> str:
            return row.get("disposition", row.get("leaf_disposition"))
        disposition = {
            "STRICT_TERMINAL": sum(disposition_of(row) == "STRICT_TERMINAL" for row in rows),
            "COLLISION3_READY": sum(disposition_of(row) == "COLLISION3_READY" for row in rows),
            "COLLISION2_HANDOFF": sum(disposition_of(row) == "COLLISION2_HANDOFF" for row in rows),
        }
        whole = disposition["COLLISION3_READY"] == disposition["COLLISION2_HANDOFF"] == 0
        whole_pairs_terminal += int(whole)
        need(prefix_free(paths) and kraft == 1, f"combined parent prefix/Kraft:{pair}")
        parent_census[str(pair)] = {
            "combined_leaf_count": len(rows), "disposition_census": disposition,
            "path_prefix_free": True, "Kraft_conservation": "1",
            "whole_pair_terminal": whole, "whole_pair_credit": 0,
            "D02_gate_credit": 0,
        }
    shard_rows = shard_result.pop("rows")
    need(len(shard_rows) == sum(shard_result["output_disposition_census"].values()),
         "shard row derived census")
    global_disposition = {
        "STRICT_TERMINAL": 462 + 2949 + shard_result["output_disposition_census"]["STRICT_TERMINAL"],
        "COLLISION3_READY": shard_result["output_disposition_census"]["COLLISION3_READY"],
        "COLLISION2_HANDOFF": shard_result["output_disposition_census"]["COLLISION2_HANDOFF"],
    }
    need(global_disposition == {"STRICT_TERMINAL": 27408, "COLLISION3_READY": 0,
                                "COLLISION2_HANDOFF": 20879},
         "global C57/C58/C61 disposition census")

    # Audit only the terminal v4 aggregate transaction.  Reconstruct all three
    # v4 ledgers independently from shard/C57/C58 rows and reject the forensic
    # v1/v2/v3 stages by exact marker pins; none is an input here.
    aggregate_paths = (
        AGGREGATE_PRODUCER, AGGREGATE_RESULT, AGGREGATE_LEAVES,
        AGGREGATE_SOURCES, AGGREGATE_PARENTS, *REJECTIONS,
    )
    aggregate_raw = capture(aggregate_paths, maximum=32 << 20)
    producer_independence(aggregate_raw[AGGREGATE_PRODUCER], AGGREGATE_PRODUCER,
                          EXPECTED_AGGREGATE_PRODUCER_SHA256)
    need(hashlib.sha256(aggregate_raw[AGGREGATE_PRODUCER]).hexdigest() ==
         EXPECTED_AGGREGATE_PRODUCER_SHA256, "aggregate producer source pin")
    aggregate_result = closed(aggregate_raw[AGGREGATE_RESULT],
                              EXPECTED_AGGREGATE_RESULT_OBJECT, "aggregate v4 result")
    need(hashlib.sha256(aggregate_raw[AGGREGATE_RESULT]).hexdigest() ==
         EXPECTED_AGGREGATE_RESULT_SHA256 and
         aggregate_result["schema"] == EXPECTED_PRODUCER_SCHEMA + ".aggregate-result.v4" and
         aggregate_result["status"] ==
         "PASS_COMPLETE_16_SHARD_DEPTH12_AGGREGATE_V4__SCHEMA_SPECIFIC_PARENT_CENSUS__ZERO_FORMAL_CREDIT",
         "aggregate v4 result pin/schema/status")
    v4_leaves = ledger(aggregate_raw[AGGREGATE_LEAVES],
                       aggregate_result["ledgers"]["aggregate_leaves"],
                       EXPECTED_AGGREGATE_LEAF_SHA256, "aggregate v4 leaves")
    v4_sources = ledger(aggregate_raw[AGGREGATE_SOURCES],
                        aggregate_result["ledgers"]["source_summaries"],
                        EXPECTED_AGGREGATE_SOURCE_SHA256, "aggregate v4 sources")
    v4_parents = ledger(aggregate_raw[AGGREGATE_PARENTS],
                        aggregate_result["ledgers"]["parent_summaries"],
                        EXPECTED_AGGREGATE_PARENT_SHA256, "aggregate v4 parents")
    need((len(v4_leaves), len(v4_sources), len(v4_parents)) == (44876, 2599, 12),
         "aggregate v4 ledger census")
    expected_v4_leaves: list[dict[str, Any]] = []
    for row in sorted(shard_rows, key=lambda value: (
        value["source_handoff_ordinal"], value["source_path"], value["path"],
    )):
        body = copy.deepcopy(row)
        source_hash = body.pop("row_sha256")
        source_schema = body.pop("schema")
        need(source_schema == EXPECTED_PRODUCER_SCHEMA + ".shard-leaf-row",
             "aggregate leaf source schema")
        expected_v4_leaves.append({
            "schema": EXPECTED_PRODUCER_SCHEMA + ".aggregate-leaf-row",
            "source_shard_row_sha256": source_hash, **body,
        })
    need(all({**expected, "row_sha256": digest(expected)} == observed
             for expected, observed in zip(expected_v4_leaves, v4_leaves)),
         "aggregate v4 exact leaf reconstruction")

    inventory_raw = capture((ASSIGNMENT_INVENTORY, ASSIGNMENT_RESULT), maximum=32 << 20)
    inv_result = closed(inventory_raw[ASSIGNMENT_RESULT], EXPECTED_RESULT_OBJECT,
                        "assignment result")
    inv = ledger(inventory_raw[ASSIGNMENT_INVENTORY], inv_result["inventory"],
                 EXPECTED_INVENTORY_SHA256, "assignment inventory")
    inv_by_source = {row["C58_leaf_row_sha256"]: row for row in inv}
    shard_by_source: dict[str, list[dict[str, Any]]] = {}
    for row in shard_rows:
        shard_by_source.setdefault(row["source_C58_leaf_row_sha256"], []).append(row)
    expected_source_rows: list[dict[str, Any]] = []
    whole_inputs = 0
    for source_hash, output in sorted(shard_by_source.items(), key=lambda item: (
        inv_by_source[item[0]]["source_handoff_ordinal"], inv_by_source[item[0]]["path"],
    )):
        source = inv_by_source[source_hash]
        terminal = sum(row["disposition"] == "STRICT_TERMINAL" for row in output)
        c3 = sum(row["disposition"] == "COLLISION3_READY" for row in output)
        c2 = len(output) - terminal - c3
        whole_inputs += int(terminal == len(output))
        expected = {
            "schema": EXPECTED_PRODUCER_SCHEMA + ".aggregate-source-row",
            "source_handoff_ordinal": source["source_handoff_ordinal"],
            "source_C58_leaf_row_sha256": source_hash,
            "source_path": source["path"], "pair_index": source["pair_index"],
            "output_leaf_count": len(output), "strict_terminal_leaf_count": terminal,
            "collision3_ready_leaf_count": c3, "collision2_handoff_leaf_count": c2,
            "path_prefix_free": True, "Kraft_conservation": source["parent_volume_fraction"],
            "whole_source_terminal": terminal == len(output),
            "whole_source_terminal_or_C3_ready": c2 == 0,
            "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
        }
        expected_source_rows.append({**expected, "row_sha256": digest(expected)})
    need(whole_inputs == 362 and expected_source_rows == v4_sources,
         "aggregate v4 exact source summaries/362 whole inputs")

    expected_parent_rows: list[dict[str, Any]] = []
    for pair in pairs:
        census = parent_census[str(pair)]
        expected = {
            "schema": EXPECTED_PRODUCER_SCHEMA + ".aggregate-parent-row",
            "pair_index": pair, "combined_leaf_count": census["combined_leaf_count"],
            "strict_terminal_leaf_count": census["disposition_census"]["STRICT_TERMINAL"],
            "collision3_ready_leaf_count": census["disposition_census"]["COLLISION3_READY"],
            "collision2_handoff_leaf_count": census["disposition_census"]["COLLISION2_HANDOFF"],
            "path_prefix_free": True, "parent_Kraft_conservation": "1",
            "whole_pair_terminal": census["whole_pair_terminal"],
            "whole_pair_credit": 0, "D02_gate_credit": 0,
        }
        expected_parent_rows.append({**expected, "row_sha256": digest(expected)})
    need(expected_parent_rows == v4_parents and
         sum(row["strict_terminal_leaf_count"] for row in v4_parents) == 27408 and
         sum(row["collision2_handoff_leaf_count"] for row in v4_parents) == 20879 and
         sum(row["collision3_ready_leaf_count"] for row in v4_parents) == 0,
         "aggregate v4 exact parent rows/global census")
    need(aggregate_result["coverage"] == {
        "input_C58_residuals": 2599, "shard_receipts": 16,
        "assignment_complete": True, "assignment_mutually_exclusive": True,
        "route_evaluations": 87153, "output_leaf_count": 44876,
        "disposition_census": {"STRICT_TERMINAL": 23997, "COLLISION3_READY": 0,
                               "COLLISION2_HANDOFF": 20879},
        "whole_input_handoffs_terminal": 362,
        "whole_input_handoffs_terminal_or_C3_ready": 362,
        "carried_C57_terminal_leaves": 462, "carried_C58_terminal_leaves": 2949,
        "raw_classification_census": {
            "EXCLUDED_C39_C1_ENHANCED_W_SIDE_COLLISION1_WORD_MISMATCH": 5819,
            "EXCLUDED_C39_C1_ENHANCED_W_SIDE_COLLISION2_OWNER_MISMATCH": 4433,
            "EXCLUDED_C39_C1_OUTGOING_CHART_MISMATCH": 12084,
            "EXCLUDED_C39_C1_UNIQUE_FIRST_OWNER_MISMATCH": 1661,
            "UNRESOLVED_C39_C1_ENHANCED_W_SIDE_COLLISION1_OUTGOING_STATE": 3222,
            "UNRESOLVED_C39_C1_H1_GRAPH_OR_BOUNDARY": 11556,
            "UNRESOLVED_C39_C1_REGULAR_MULTI_GRAPH_ARRANGEMENT": 6101,
        },
    } and aggregate_result["invariants"] == {
        "all_2599_source_partitions_prefix_free_and_Kraft_conserved": True,
        "all_12_combined_parents_prefix_free_and_Kraft_one": True,
        "all_16_receipts_complete": True, "C57_C58_C61_parent_carry_complete": True,
        "schema_specific_disposition_accessors_used": True,
        "incomplete_v1_stage_ledgers_reused": False,
        "rejected_v2_stage_ledgers_reused": False,
        "rejected_v3_stage_ledgers_reused": False,
        "partial_statistics_used_for_credit": False,
    } and aggregate_result["whole_pairs_closed"] == aggregate_result["whole_singletons_closed"] == 0 and
         aggregate_result["whole_singletons_remaining"] == 24 and
         aggregate_result["formal_credit"] == aggregate_result["whole_parent_credit"] ==
         aggregate_result["D02_gate_credit"] == 0 and
         aggregate_result["runtime_canonical_pointer_or_seal_writes"] is False,
         "aggregate v4 result exact semantics/nonpromotion")
    rejection_statuses = {
        1: "REJECTED_INCOMPLETE_C57_CARRY__NO_RESULT_OBJECT__ZERO_CREDIT",
        2: "REJECTED_C57_LEAF_DISPOSITION_ACCESSOR__ZERO_CREDIT",
        3: "REJECTED_RESULT_SERIALIZATION_NAME_COLLISION__NO_RESULT_OBJECT__ZERO_CREDIT",
    }
    for stage, (path, claim) in enumerate(REJECTIONS.items(), start=1):
        text = aggregate_raw[path].decode("utf-8", "strict")
        need(hashlib.sha256(aggregate_raw[path]).hexdigest() == claim and
             rejection_statuses[stage] in text and "zero" in text.lower() and
             (f"aggregate_result_v{stage}.json" not in aggregate_result["ledgers"].values()),
             f"rejected v{stage} exact marker/exclusion")
    return close({
        "schema": SCHEMA + ".verification",
        "status": "PASS_INDEPENDENT_V4_ONLY_COMPLETE_16_SHARD_AGGREGATE__2599_INPUTS__44876_OUTPUTS__362_WHOLE_INPUTS__12_PARENT_KRAFT_ONE__27408_T__0_C3__20879_C2__ZERO_CREDIT",
        "frozen_contract": {
            "file_sha256": hashlib.sha256(CONTRACT.read_bytes()).hexdigest(),
            "object_sha256": frozen["object_sha256"],
        },
        "assignment": assignment_result,
        "shards": shard_result,
        "combined_parent_census": parent_census,
        "aggregate_v4": {
            "producer_file_sha256": EXPECTED_AGGREGATE_PRODUCER_SHA256,
            "result_file_sha256": EXPECTED_AGGREGATE_RESULT_SHA256,
            "result_object_sha256": EXPECTED_AGGREGATE_RESULT_OBJECT,
            "leaf_ledger_sha256": EXPECTED_AGGREGATE_LEAF_SHA256,
            "source_summary_sha256": EXPECTED_AGGREGATE_SOURCE_SHA256,
            "parent_summary_sha256": EXPECTED_AGGREGATE_PARENT_SHA256,
        },
        "rejected_stages": {
            "v1": {"excluded": True, "marker_sha256": list(REJECTIONS.values())[0]},
            "v2": {"excluded": True, "marker_sha256": list(REJECTIONS.values())[1]},
            "v3": {"excluded": True, "marker_sha256": list(REJECTIONS.values())[2]},
        },
        "global_disposition_census_including_C57_and_C58_carried_terminals": global_disposition,
        "whole_pairs_terminal": whole_pairs_terminal,
        "whole_singletons_terminal": 2 * whole_pairs_terminal,
        "whole_singletons_remaining": 24 - 2 * whole_pairs_terminal,
        "candidate_is_authority": False,
        "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
        "runtime_canonical_pointer_or_seal_writes": False,
        "independence": {
            "producer_imported": False, "producer_executed": False,
            "producer_consumed_as_pinned_inert_bytes_and_AST_only": True,
        },
    })


def self_test() -> dict[str, Any]:
    frozen = contract()
    tests: dict[str, bool] = {}
    vectors = (
        (0, "0"), (0, "1"), (1, "000001011"),
        (318, "111111111111"), (2598, "010101010101010"),
    )
    for ordinal, path in vectors:
        preimage = assignment_preimage(ordinal, path)
        expected = json.dumps(
            {"path": path, "source_handoff_ordinal": ordinal}, sort_keys=True,
            separators=(",", ":"), ensure_ascii=False, allow_nan=False,
        ).encode("utf-8")
        tests[f"assignment_vector_{ordinal}_{path}"] = (
            preimage == expected and not preimage.endswith(b"\n") and
            assignment(ordinal, path) == int(hashlib.sha256(expected).hexdigest(), 16) % 16
        )
    attacks = (
        ("negative_ordinal", -1, "0"), ("boolean_ordinal", True, "0"),
        ("empty_path", 0, ""), ("nonbinary_path", 0, "02"),
    )
    for name, ordinal, path in attacks:
        try:
            assignment_preimage(ordinal, path)
        except Rejected:
            tests[name + "_rejected"] = True
    malformed = (
        ("duplicate_key", b'{"a":1,"a":2}\n'),
        ("NaN", b'{"a":NaN}\n'), ("BOM", b'\xef\xbb\xbf{"a":1}\n'),
        ("trailing", b'{"a":1}\nX'),
    )
    for name, raw in malformed:
        try:
            parse(raw, name, canonical_required=True)
        except Rejected:
            tests[name + "_rejected"] = True
    with tempfile.TemporaryDirectory(prefix="cm2-c61s12-independent-") as temporary:
        root = Path(temporary)
        target = root / "target"
        target.write_bytes(canonical(frozen) + b"\n")
        link = root / "link"
        link.symlink_to(target.name)
        try:
            capture((link,))
        except OSError:
            tests["symlink_rejected"] = True
        hard = root / "hard"
        os.link(target, hard)
        try:
            capture((target,))
        except Rejected:
            tests["hardlink_rejected"] = True
        hard.unlink()
        replacement = root / "replacement"
        replacement.write_bytes(canonical(frozen) + b"\n")
        try:
            capture((target,), hook=lambda: os.replace(replacement, target))
        except Rejected:
            tests["TOCTOU_replacement_rejected"] = True
    tests["frozen_schema_pins_ready"] = all(not value.startswith("PENDING_") for value in (
        EXPECTED_PRODUCER_SCHEMA, EXPECTED_PRODUCER_SHA256, EXPECTED_RESULT_SCHEMA,
        EXPECTED_RESULT_SHA256, EXPECTED_RESULT_OBJECT, EXPECTED_SHARD_LEDGER_PATTERN,
        EXPECTED_RECEIPT_PATTERN,
    ))
    tests["assignment_inventory_independently_reconstructed"] = (
        assignment_verify()["input_count"] == 2599)
    synthetic = close({
        "schema": "synthetic.c61s12.aggregate-v4", "inputs": 2599,
        "shards": 16, "route_evaluations": 87153, "outputs": 44876,
        "terminal": 23997, "C3": 0, "C2": 20879, "whole_inputs": 362,
        "C57_carried": 462, "C58_carried": 2949, "combined_leaves": 48287,
        "combined_terminal": 27408, "parents": 12, "parent_Kraft_one": True,
        "source_Kraft_conserved": True, "v1_excluded": True, "v2_excluded": True,
        "v3_excluded": True, "formal_credit": 0, "whole_parent_credit": 0,
        "D02_gate_credit": 0,
    })
    def validate_synthetic(value: dict[str, Any]) -> None:
        need(type(value) is dict and set(value) == set(synthetic), "synthetic schema")
        body = copy.deepcopy(value)
        claim = body.pop("object_sha256", None)
        need(claim == digest(body) and value == synthetic, "synthetic exact v4 contract")
    validate_synthetic(synthetic)
    tests["synthetic_v4_baseline_valid"] = True
    coherent_attacks: tuple[tuple[str, Any], ...] = (
        ("inputs", 2598), ("shards", 15), ("route_evaluations", 87152),
        ("outputs", 44875), ("terminal", 23996), ("C3", 1), ("C2", 20878),
        ("whole_inputs", 361), ("C57_carried", 461), ("C58_carried", 2948),
        ("combined_leaves", 48286), ("combined_terminal", 27407),
        ("parents", 11), ("parent_Kraft_one", False),
        ("source_Kraft_conserved", False), ("v1_excluded", False),
        ("v2_excluded", False), ("v3_excluded", False),
        ("formal_credit", 1), ("whole_parent_credit", 1), ("D02_gate_credit", 1),
    )
    for field, replacement in coherent_attacks:
        attacked = copy.deepcopy(synthetic)
        attacked.pop("object_sha256")
        attacked[field] = replacement
        attacked = close(attacked)
        try:
            validate_synthetic(attacked)
        except Rejected:
            tests["coherent_" + field + "_rejected"] = True
    need(len(tests) == 40 and all(tests.values()), "40/40 hostile tests")
    return close({
        "schema": SCHEMA + ".contract-self-test",
        "status": "PASS_40_OF_40_FROZEN_SCHEMA_ASSIGNMENT_V4_AGGREGATE_TOCTOU_AND_COHERENT_HOSTILE_TESTS",
        "contract_object_sha256": frozen["object_sha256"],
        "tests": tests, "test_count": 40,
        "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
        "runtime_canonical_pointer_or_seal_writes": False,
    })


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--verify", action="store_true")
    group.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        value = verify() if args.verify else self_test()
        sys.stdout.buffer.write(canonical(value) + b"\n")
        return 0
    except (Rejected, OSError, KeyError, ValueError, zlib.error) as exc:
        value = close({
            "schema": SCHEMA + ".fail-closed", "status": "FAIL_CLOSED_REJECTED",
            "reason": str(exc), "formal_credit": 0, "whole_parent_credit": 0,
            "D02_gate_credit": 0, "runtime_canonical_pointer_or_seal_writes": False,
        })
        sys.stdout.buffer.write(canonical(value) + b"\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
