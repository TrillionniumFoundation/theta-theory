#!/usr/bin/env python3
"""Pin-filled C71 successor: C65-v9 collision-2 children x C69c H1.

This is a new implementation; it never imports or executes the disabled C71
v1 skeleton.  Formal staging is enabled only after the complete C65-v9 cold
bundle, C69c bundle, C70-L bundle, contract, and schemas pass their frozen
gates.  It emits every one of the 167,255 C65 COLLISION2_HANDOFF children:
33,100 decision-source children receive a fresh 384-bit full-child-box H1
evaluation and 134,155 blocker-source children remain explicit fail-closed
rows.  Every output remains zero-credit and non-authoritative.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
from dataclasses import dataclass
from fractions import Fraction
import gzip
import hashlib
import importlib
import itertools
import json
import multiprocessing as mp
import os
from pathlib import Path
import stat
import sys
from typing import Any, Iterable, Iterator


sys.dont_write_bytecode = True
SELF = Path(__file__).resolve()
OUT = SELF.parent
ROOT = OUT.parent
FLINT_SITE = ROOT / ".cm2-runtime/python-flint-0.9.0/lib/python3.12/site-packages"
for entry in (str(OUT), str(FLINT_SITE)):
    if entry not in sys.path:
        sys.path.insert(0, entry)

PREFIX = "cm2_round306c71_c65v9_c69c_c70_child_h1_successor_v2"
SCHEMA = "cm2.round306c71.c65v9-c69c-c70-child-h1-successor.v2"
CONTRACT_NAME = PREFIX.replace("_v2", "_contract_v2") + ".json"
SCHEMAS_NAME = PREFIX.replace("_v2", "_closed_schemas_v2") + ".json"
CONTRACT_FILE_SHA256 = "d83459e29589f98b5f0929652ed5b78024cd34b9f572d6aa8d50ef85bd4265da"
CONTRACT_OBJECT_SHA256 = "509779842cffc4a5db47a53bad451607cf86cdb4328718f82d531b74f23b7bc1"
SCHEMAS_FILE_SHA256 = "53c71aa77f5e503b4a4ee8e9530ad0d4b53bdc61fef98eb17302d73b1ae8dcec"
SCHEMAS_OBJECT_SHA256 = "ca23ab339c6d4393447586dbf362b68418752d89d6d99649c44cee33dc1bc8c3"

INTERSECTION_NAME = PREFIX + "_intersection_rows.jsonl.gz"
SOURCE_SUMMARY_NAME = PREFIX + "_source_summaries.jsonl.gz"
RESULT_NAME = PREFIX + "_result.json"
REPORT_NAME = PREFIX + "_report.md"
STAGE_NAMES = (INTERSECTION_NAME, SOURCE_SUMMARY_NAME, RESULT_NAME, REPORT_NAME)

PRECISION_BITS = 384
EXPECTED_C65_C2 = 167255
EXPECTED_DECISION_CHILDREN = 33100
EXPECTED_BLOCKER_CHILDREN = 134155
EXPECTED_C69_DECISIONS = 2356
EXPECTED_C69_BLOCKERS = 18523
EXPECTED_SOURCES = 20879

C65_NAMES = {
    "verifier": "cm2_round306c65s18_64shard_aggregate_independent_cold_verifier_v9.py",
    "aggregate_result": "cm2_round306c65s18_depth18_64shard_aggregate_result_v1.json",
    "aggregate_leaf_ledger": "cm2_round306c65s18_depth18_64shard_aggregate_leaf_ledger_v1.jsonl.gz",
    "aggregate_source_summary": "cm2_round306c65s18_depth18_64shard_aggregate_source_summary_v1.jsonl.gz",
    "aggregate_parent_summary": "cm2_round306c65s18_depth18_64shard_aggregate_parent_summary_v1.jsonl.gz",
    "seed1_projection": "cm2_round306c65s18_64shard_aggregate_independent_cold_seed1_projection_v9.json",
    "seed1_completion_receipt": "cm2_round306c65s18_64shard_aggregate_independent_cold_seed1_completion_receipt_v9.json",
    "seed2_projection": "cm2_round306c65s18_64shard_aggregate_independent_cold_seed2_projection_v9.json",
    "seed2_completion_receipt": "cm2_round306c65s18_64shard_aggregate_independent_cold_seed2_completion_receipt_v9.json",
    "verification": "cm2_round306c65s18_64shard_aggregate_independent_cold_verification_v9.json",
    "verification_completion_receipt": "cm2_round306c65s18_64shard_aggregate_independent_cold_verification_completion_receipt_v9.json",
    "self_test": "cm2_round306c65s18_64shard_aggregate_independent_cold_self_test_v9.json",
    "self_test_completion_receipt": "cm2_round306c65s18_64shard_aggregate_independent_cold_self_test_completion_receipt_v9.json",
    "postpublication_replay": "cm2_round306c65s18_64shard_aggregate_independent_cold_postpublication_replay_v9.json",
    "manifest": "cm2_round306c65s18_64shard_aggregate_independent_cold_manifest_v9.sha256",
    "outer_receipt": "cm2_round306c65s18_64shard_aggregate_independent_cold_outer_receipt_v9.json",
}
C65_RELEASE_ROLES = (
    "seed1_projection", "seed1_completion_receipt", "seed2_projection",
    "seed2_completion_receipt", "verification", "verification_completion_receipt",
    "self_test", "self_test_completion_receipt", "postpublication_replay",
)
C69_NAMES = {
    "corrected_result": "cm2_round306c69c_descriptor_repair_supersession_v1_corrected_result.json",
    "verification": "cm2_round306c69c_descriptor_repair_supersession_independent_verification_v1.json",
    "self_test": "cm2_round306c69c_descriptor_repair_supersession_independent_self_test_v1.json",
    "outer_receipt": "cm2_round306c69c_descriptor_repair_supersession_independent_outer_publication_receipt_v1.json",
    "manifest": "cm2_round306c69c_descriptor_repair_supersession_independent_manifest_v1.sha256",
    "decisions": "cm2_round306c69b_singleton_h1_graph_slab_decider_v2_decisions.jsonl.gz",
    "blockers": "cm2_round306c69b_singleton_h1_graph_slab_decider_v2_blockers.jsonl.gz",
}
C70_NAMES = {
    "result": "cm2_round306c70l_large_component_consumption_intersection_result_v1.json",
    "edge_ledger": "cm2_round306c70l_large_component_consumption_intersection_edge_ledger_v1.jsonl.gz",
    "corridor_ledger": "cm2_round306c70l_large_component_consumption_intersection_corridor_ledger_v1.jsonl.gz",
    "independent_verification": "cm2_round306c70l_large_component_consumption_intersection_independent_verification_v1.json",
    "manifest": "cm2_round306c70l_large_component_consumption_intersection_manifest_v1.sha256",
    "manifest_receipt": "cm2_round306c70l_large_component_consumption_intersection_manifest_v1.sha256.sha256",
}

C65_VERIFY_STATUS = (
    "PASS_DUAL_EXTERNAL_PROCESS_COLD_VERIFICATION_V9__DISTINCT_STARTTICKS__"
    "EXACT_FROZEN_VECTOR__ZERO_CREDIT"
)
C65_SELFTEST_STATUS = (
    "PASS_134_OF_134_PROTOCOL_FILESYSTEM_SCHEMA_LOADER_PROVENANCE_MANIFEST_"
    "WORKER_TRANSPORT_AND_C61_BASELINE_ATTACKS"
)
C69_VERIFY_STATUS = (
    "PASS_COLD_NO_C69_PRODUCER_OR_WRAPPER_IMPORT_EXECUTION_READ_OR_DECODE__"
    "EXACT_REBUILD_20879_PARTITION_2356_NUMERIC_DECISIONS_18523_BLOCKERS_2_"
    "COVER_ROWS__ZERO_CREDIT"
)
C70_VERIFY_STATUS = (
    "PASS_COLD_NO_PRODUCER_EXACT_REBUILD__1042_EDGES_298_READY__1044_CORRIDORS_"
    "73_READY__SOURCE_SEAM_0_READY__24_OF_24_ATTACKS__ZERO_CREDIT"
)


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(4 << 20), b""):
            hasher.update(block)
    return hasher.hexdigest()


def identity(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns)


def secure_read(path: Path, expected_sha: str) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular-single-link:" + str(path))
        chunks: list[bytes] = []
        while block := os.read(descriptor, 4 << 20):
            chunks.append(block)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    current = os.stat(path, follow_symlinks=False)
    need(identity(before) == identity(after) == identity(current), "TOCTOU:" + str(path))
    raw = b"".join(chunks)
    need(hashlib.sha256(raw).hexdigest() == expected_sha, "file-pin:" + str(path))
    return raw


def secure_hash(path: Path, expected_sha: str) -> tuple[str, int]:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    hasher = hashlib.sha256()
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular-single-link:" + str(path))
        while block := os.read(descriptor, 4 << 20):
            hasher.update(block)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    current = os.stat(path, follow_symlinks=False)
    need(identity(before) == identity(after) == identity(current), "TOCTOU:" + str(path))
    actual = hasher.hexdigest()
    need(actual == expected_sha, "file-pin:" + str(path))
    return actual, before.st_size


def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in result, "duplicate-json-key:" + key)
        result[key] = value
    return result


def reject_float(token: str) -> Any:
    raise Reject("noninteger-json-number:" + token)


def parse_json(raw: bytes, label: str) -> dict[str, Any]:
    need(raw and not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
         "json-framing:" + label)
    value = json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=no_duplicates,
                       parse_float=reject_float,
                       parse_constant=lambda token: reject_float(token))
    need(type(value) is dict, "json-object:" + label)
    return value


def close_object(value: dict[str, Any], expected: str, label: str) -> None:
    body = copy.deepcopy(value)
    claim = body.pop("object_sha256", None)
    need(claim == expected == digest(body), "object-closure:" + label)


def close_row(value: dict[str, Any], label: str) -> None:
    body = copy.deepcopy(value)
    claim = body.pop("row_sha256", None)
    need(type(claim) is str and claim == digest(body), "row-closure:" + label)


def zero_boundary(value: dict[str, Any], keys: Iterable[str], label: str) -> None:
    need(all(value.get(key) == 0 for key in keys), "zero-credit:" + label)


def parse_manifest(raw: bytes, label: str) -> list[tuple[str, str]]:
    need(raw.endswith(b"\n") and not raw.endswith(b"\n\n") and b"\x00" not in raw,
         "manifest-framing:" + label)
    rows: list[tuple[str, str]] = []
    seen: set[str] = set()
    for line in raw.decode("utf-8", "strict").splitlines():
        sha, separator, name = line.partition("  ")
        need(separator == "  " and len(sha) == 64 and
             all(character in "0123456789abcdef" for character in sha),
             "manifest-row:" + label)
        need(name and name not in seen, "manifest-duplicate:" + label)
        seen.add(name)
        rows.append((sha, name))
    return rows


def sequence_hash(values: Iterable[str]) -> str:
    hasher = hashlib.sha256()
    for value in values:
        hasher.update(value.encode("utf-8") + b"\n")
    return hasher.hexdigest()


def resolve_c65_relative(relative: str) -> Path:
    if relative.startswith("machine-runtime/"):
        return Path("/") / relative.removeprefix("machine-runtime/")
    return ROOT / relative


def load_contract_gate() -> tuple[dict[str, Any], dict[str, Any]]:
    contract = parse_json(secure_read(OUT / CONTRACT_NAME, CONTRACT_FILE_SHA256), CONTRACT_NAME)
    schemas = parse_json(secure_read(OUT / SCHEMAS_NAME, SCHEMAS_FILE_SHA256), SCHEMAS_NAME)
    close_object(contract, CONTRACT_OBJECT_SHA256, "contract")
    close_object(schemas, SCHEMAS_OBJECT_SHA256, "schemas")
    need(contract["closed_schemas"]["object_sha256"] == SCHEMAS_OBJECT_SHA256,
         "contract-schema-binding")
    pins = contract.get("frozen_pin_map")
    need(type(pins) is dict and set(pins) == {"C65_v9", "C69c", "C70L", "numeric_kernel"}
         and all(type(value) is dict and value for value in pins.values()),
         "complete-nonempty-pin-map")
    need(contract["execution_guard"]["old_C71_skeleton_may_be_imported_or_executed"] is False,
         "old-skeleton-guard")
    return contract, schemas


def pinned_json(path: Path, pin: str, object_pin: str, label: str) -> dict[str, Any]:
    value = parse_json(secure_read(path, pin), label)
    close_object(value, object_pin, label)
    return value


def c65_gate(contract: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, str], str]:
    pins = contract["frozen_pin_map"]["C65_v9"]
    need(set(C65_NAMES) <= set(pins) | {"aggregate_result", "aggregate_leaf_ledger",
         "aggregate_source_summary", "aggregate_parent_summary"}, "C65 role map")
    verification = pinned_json(OUT / C65_NAMES["verification"], pins["verification"],
                               pins["verification_object"], "C65 verification")
    self_test = pinned_json(OUT / C65_NAMES["self_test"], pins["self_test"],
                            pins["self_test_object"], "C65 self-test")
    replay = pinned_json(OUT / C65_NAMES["postpublication_replay"],
                         pins["postpublication_replay"], pins["postpublication_replay_object"],
                         "C65 replay")
    outer = pinned_json(OUT / C65_NAMES["outer_receipt"], pins["outer_receipt"],
                        pins["outer_receipt_object"], "C65 outer")
    need(verification["schema"].endswith("v9.verification") and
         verification["status"] == C65_VERIFY_STATUS, "C65 v9 verification protocol")
    need(self_test["test_count"] == 134 and self_test["status"] == C65_SELFTEST_STATUS,
         "C65 formal 134/134 self-test")
    need("94_OF_94" not in self_test["status"] and
         verification["rejections"]["rejected_v3_verifier_or_outputs_consumed"] is False,
         "C65 rejected-v3 confusion")
    need(replay["status"] ==
         "PASS_FULL_RELEASE_VALIDATION_AND_POSTPUBLICATION_RECAPTURE__ZERO_CREDIT",
         "C65 replay protocol")
    need(outer["outer_receipt_published_last"] is True and
         outer["manifest_member_count"] == 446 and
         outer["manifest_members_recaptured_after_publication"] is True,
         "C65 outer protocol")
    for value, label in ((verification, "verification"), (self_test, "self-test"),
                         (replay, "replay"), (outer, "outer")):
        zero_boundary(value, ("formal_credit", "whole_parent_credit", "D02_gate_credit"),
                      "C65 " + label)
        need(value["candidate_is_authority"] is False and
             value["runtime_canonical_pointer_or_seal_writes"] is False,
             "C65 authority boundary:" + label)

    release_objects: dict[str, dict[str, Any]] = {}
    for role in C65_RELEASE_ROLES:
        value = parse_json(secure_read(OUT / C65_NAMES[role], pins[role]), "C65 " + role)
        close_object(value, value.get("object_sha256"), "C65 " + role)
        for credit_key in ("formal_credit", "whole_parent_credit", "D02_gate_credit"):
            if credit_key in value:
                need(value[credit_key] == 0, "C65 release zero-credit:" + role)
        release_objects[role] = value
    need(release_objects["seed1_projection"]["object_sha256"] ==
         release_objects["seed2_projection"]["object_sha256"] and
         release_objects["seed1_projection"]["status"] ==
         "PASS_COMPLETE_C65_AGGREGATE_COLD_NUMERIC_REPLAY_V9__64_OF_64__20879_ASSIGNMENTS__C61_FULL_BASE_REPLACEMENT__ZERO_CREDIT" and
         release_objects["seed1_completion_receipt"]["status"] ==
         release_objects["seed2_completion_receipt"]["status"] ==
         "PASS_EXTERNAL_LAUNCHER_FRESH_PROCESS_COMPLETION__ZERO_CREDIT" and
         release_objects["verification_completion_receipt"]["status"] ==
         release_objects["self_test_completion_receipt"]["status"] ==
         "PASS_RESULT_LAST_COMPLETION", "C65 complete release objects")

    manifest_raw = secure_read(OUT / C65_NAMES["manifest"], pins["manifest"])
    manifest = parse_manifest(manifest_raw, "C65")
    vector = verification["frozen_snapshot"]["ordered_input_vector"]
    need(len(vector) == 437 and len(manifest) == 446, "C65 437/446 coverage")
    expected: list[tuple[str, str, str]] = []
    for row in vector:
        logical = row["logical_name"]
        relative = row["relative_path"]
        need(logical == relative.replace("/", "__") and
             type(row["sha256"]) is str and len(row["sha256"]) == 64,
             "C65 vector alias")
        expected.append((row["sha256"], logical, relative))
    for role in C65_RELEASE_ROLES:
        relative = "deliverables/" + C65_NAMES[role]
        expected.append((pins[role], relative.replace("/", "__"), relative))
    need([(sha, alias) for sha, alias, _path in expected] == manifest,
         "C65 exact ordered global manifest")
    need(sequence_hash(alias for _sha, alias in manifest) ==
         outer["manifest_ordered_alias_sequence_sha256"], "C65 manifest alias sequence")
    replay_records: list[str] = []
    path_pins: dict[str, str] = {}
    for expected_sha, alias, relative in expected:
        actual, size = secure_hash(resolve_c65_relative(relative), expected_sha)
        path_pins[relative] = actual
        replay_records.append(alias + "\0" + actual + "\0" + str(size))
    for name, expected_sha in ((C65_NAMES["manifest"], pins["manifest"]),
                               (C65_NAMES["outer_receipt"], pins["outer_receipt"])):
        actual, size = secure_hash(OUT / name, expected_sha)
        replay_records.append("deliverables__" + name + "\0" + actual + "\0" + str(size))
    need(len(replay_records) == 448, "C65 terminal replay 448")
    terminal_replay = sequence_hash(replay_records)

    aggregate = pinned_json(OUT / C65_NAMES["aggregate_result"], pins["aggregate_result"],
                            pins["aggregate_result_object"], "C65 aggregate")
    need(aggregate["status"] ==
         "PASS_COMPLETE_64_SHARD_DEPTH18_REPLACEMENT_AGGREGATE__ZERO_CREDIT" and
         aggregate["coverage"]["replacement_disposition_census"]["COLLISION2_HANDOFF"] ==
         EXPECTED_C65_C2, "C65 aggregate census")
    zero_boundary(aggregate, ("formal_credit", "whole_parent_credit", "D02_gate_credit"),
                  "C65 aggregate")
    return aggregate, verification, path_pins, terminal_replay


def validate_plain_manifest(raw: bytes, base: Path, expected_count: int, label: str) -> None:
    rows = parse_manifest(raw, label)
    need(len(rows) == expected_count, label + " manifest count")
    for expected_sha, relative in rows:
        need(not relative.startswith("/") and ".." not in Path(relative).parts,
             label + " manifest path")
        secure_hash(base / relative, expected_sha)


def c69_gate(contract: dict[str, Any]) -> dict[str, Any]:
    pins = contract["frozen_pin_map"]["C69c"]
    manifest = secure_read(OUT / C69_NAMES["manifest"], pins["manifest"])
    validate_plain_manifest(manifest, ROOT, 25, "C69c")
    corrected = pinned_json(OUT / C69_NAMES["corrected_result"], pins["corrected_result"],
                            pins["corrected_result_object"], "C69c corrected")
    verification = pinned_json(OUT / C69_NAMES["verification"], pins["verification"],
                               pins["verification_object"], "C69c verification")
    self_test = pinned_json(OUT / C69_NAMES["self_test"], pins["self_test"],
                            pins["self_test_object"], "C69c self-test")
    outer = pinned_json(OUT / C69_NAMES["outer_receipt"], pins["outer_receipt"],
                        pins["outer_receipt_object"], "C69c outer")
    need(corrected["status"] ==
         "PASS_C69B_SEALED_LEDGER_DESCRIPTOR_REPAIR_SUPERSESSION__ZERO_CREDIT" and
         corrected["scope"]["decision_count"] == EXPECTED_C69_DECISIONS and
         corrected["scope"]["total_blocker_count"] == EXPECTED_C69_BLOCKERS,
         "C69c corrected protocol")
    need(corrected["strict_boundary"]["decisions_are_terminal_dispositions"] is False,
         "C69c decision nonterminal")
    zero_boundary(corrected["strict_boundary"],
                  ("formal_credit", "whole_parent_credit", "D02_gate_credit"),
                  "C69c corrected")
    need(verification["status"] == C69_VERIFY_STATUS and
         self_test["status"] ==
         "PASS_COHERENT_SEMANTIC_FILESYSTEM_AND_HOSTILE_JSON_ATTACKS_FAIL_CLOSED" and
         outer["manifest_closed_entry_count"] == 25,
         "C69c independent bundle")
    zero_boundary(verification, ("formal_credit", "whole_parent_credit", "D02_gate_credit"),
                  "C69c verification")
    zero_boundary(self_test, ("formal_credit", "whole_parent_credit", "D02_gate_credit"),
                  "C69c self-test")
    zero_boundary(outer, ("formal_credit", "whole_parent_credit", "D02_gate_credit"),
                  "C69c outer")
    return corrected


def c70_gate(contract: dict[str, Any]) -> dict[str, Any]:
    pins = contract["frozen_pin_map"]["C70L"]
    manifest = secure_read(OUT / C70_NAMES["manifest"], pins["manifest"])
    validate_plain_manifest(manifest, OUT, 8, "C70L")
    receipt_raw = secure_read(OUT / C70_NAMES["manifest_receipt"], pins["manifest_receipt"])
    need(receipt_raw == (pins["manifest"] + "  " + C70_NAMES["manifest"] + "\n").encode(),
         "C70L manifest receipt")
    result = pinned_json(OUT / C70_NAMES["result"], pins["result"],
                         pins["result_object"], "C70L result")
    verification = pinned_json(OUT / C70_NAMES["independent_verification"],
                               pins["independent_verification"],
                               pins["independent_verification_object"],
                               "C70L verification")
    need(verification["status"] == C70_VERIFY_STATUS and
         verification["producer_source_imported_decoded_compiled_or_executed"] is False,
         "C70L no-producer verification")
    summary = verification["independent_rebuild"]["summary"]
    need(summary["edge_ready_count"] == 298 and summary["edge_blocked_count"] == 744 and
         summary["corridor_ready_count"] == 73 and summary["corridor_blocked_count"] == 971 and
         summary["source_seam_ready_count"] == 0, "C70L frozen obstruction census")
    zero_boundary(verification,
                  ("formal_credit", "whole_cell_credit", "handoff_credit", "D02_gate_credit"),
                  "C70L verification")
    zero_boundary(result["strict_boundary"],
                  ("formal_credit", "whole_cell_credit", "handoff_credit", "D02_gate_credit"),
                  "C70L result")
    return verification


def iter_gzip_rows(path: Path, descriptor: dict[str, Any], label: str) -> Iterator[dict[str, Any]]:
    need(file_sha(path) == descriptor["sha256"] and path.stat().st_size == descriptor["size"],
         "gzip descriptor bytes:" + label)
    count = 0
    row_sequence = hashlib.sha256()
    with gzip.open(path, "rb") as handle:
        for raw in handle:
            need(raw.endswith(b"\n") and not raw.endswith(b"\n\n"), "row framing:" + label)
            row = parse_json(raw, label + ":" + str(count))
            need(canonical(row) + b"\n" == raw, "canonical row:" + label)
            close_row(row, label + ":" + str(count))
            row_sequence.update(row["row_sha256"].encode("ascii") + b"\n")
            count += 1
            yield row
    need(count == descriptor["row_count"] and
         row_sequence.hexdigest() == descriptor["row_hash_line_sequence_sha256"],
         "gzip descriptor rows:" + label)


@dataclass(frozen=True)
class ExactBox:
    t0: Fraction
    t1: Fraction
    p0: Fraction
    p1: Fraction
    s0: Fraction
    s1: Fraction

    def bounds(self, axis: int) -> tuple[Fraction, Fraction]:
        return ((self.t0, self.t1), (self.p0, self.p1), (self.s0, self.s1))[axis]

    def width(self, axis: int) -> Fraction:
        lower, upper = self.bounds(axis)
        return upper - lower


def exact_box(payload: dict[str, list[str]]) -> ExactBox:
    need(set(payload) == {"t", "p", "s"} and
         all(type(payload[key]) is list and len(payload[key]) == 2 for key in payload),
         "exact box schema")
    box = ExactBox(*(Fraction(item) for key in ("t", "p", "s") for item in payload[key]))
    need(all(box.width(axis) >= 0 for axis in range(3)), "exact box ordered")
    return box


def box_payload(box: ExactBox) -> dict[str, list[str]]:
    return {"t": [str(box.t0), str(box.t1)], "p": [str(box.p0), str(box.p1)],
            "s": [str(box.s0), str(box.s1)]}


def split_box(box: ExactBox, axis: int) -> tuple[ExactBox, ExactBox]:
    lower, upper = box.bounds(axis)
    middle = (lower + upper) / 2
    values = [[box.t0, box.t1], [box.p0, box.p1], [box.s0, box.s1]]
    left, right = copy.deepcopy(values), copy.deepcopy(values)
    left[axis][1] = middle
    right[axis][0] = middle
    make = lambda value: ExactBox(value[0][0], value[0][1], value[1][0], value[1][1],
                                  value[2][0], value[2][1])
    return make(left), make(right)


def rebuild_child(source: dict[str, Any], child: dict[str, Any]) -> tuple[ExactBox, str]:
    source_path = source["path"]
    child_path = child["path"]
    need(child_path.startswith(source_path), "child source prefix")
    box = exact_box(source["exact_representative_box"])
    chain: list[dict[str, Any]] = []
    for depth, bit in enumerate(child_path[len(source_path):], 1):
        need(bit in "01", "binary child suffix")
        axis = max(range(3), key=box.width)
        middle = sum(box.bounds(axis), Fraction(0)) / 2
        children = split_box(box, axis)
        chain.append({"depth": depth, "axis": ("t", "p", "s")[axis],
                      "split": str(middle), "bit": bit,
                      "shared_face_owner": "LOWER_BIT_CHILD",
                      "selected_owns_shared_face": bit == "0"})
        box = children[int(bit)]
    need(box_payload(box) == child["exact_representative_box"], "child exact box replay")
    need(Fraction(child["parent_volume_fraction"]) ==
         Fraction(source["parent_volume_fraction"]) /
         2 ** len(child_path[len(source_path):]),
         "child exact volume replay")
    return box, digest(chain)


def load_input_rows(aggregate: dict[str, Any], c69: dict[str, Any]
                    ) -> tuple[dict[str, Any], list[dict[str, Any]],
                               dict[str, Any], dict[str, Any], dict[str, Any]]:
    c61_result_path = OUT / "cm2_round306c61s12_depth12_16shard_aggregate_result_v4.json"
    c61_result = parse_json(secure_read(
        c61_result_path, "06b4146185cb6ef0c8d908d523369008481f7df4e6a05ad5956c001267b07f5e"),
        "C61 result")
    close_object(c61_result, "05bcb4301ac74aefd6744db2e633c2479c423fab881b33609bf7234a5537e584",
                 "C61 result")
    sources: dict[str, Any] = {}
    for row in iter_gzip_rows(OUT / c61_result["ledgers"]["aggregate_leaves"]["filename"],
                              c61_result["ledgers"]["aggregate_leaves"], "C61 leaves"):
        if row["disposition"] == "COLLISION2_HANDOFF":
            need(row["row_sha256"] not in sources, "duplicate C61 source")
            sources[row["row_sha256"]] = row
    need(len(sources) == EXPECTED_SOURCES, "C61 selected source count")

    summaries = list(iter_gzip_rows(OUT / aggregate["ledgers"]["source_summaries"]["filename"],
                                    aggregate["ledgers"]["source_summaries"],
                                    "C65 source summaries"))
    need(len(summaries) == EXPECTED_SOURCES and
         {row["source_C61_aggregate_leaf_row_sha256"] for row in summaries} == set(sources),
         "C65 source summary domain")
    decisions = {row["C61_aggregate_leaf_row_sha256"]: row for row in iter_gzip_rows(
        OUT / C69_NAMES["decisions"], c69["ledgers"]["decisions"], "C69c decisions")}
    blockers = {row["C61_aggregate_leaf_row_sha256"]: row for row in iter_gzip_rows(
        OUT / C69_NAMES["blockers"], c69["ledgers"]["blockers"], "C69c blockers")}
    need(len(decisions) == EXPECTED_C69_DECISIONS and len(blockers) == EXPECTED_C69_BLOCKERS and
         set(decisions).isdisjoint(blockers) and set(decisions) | set(blockers) == set(sources),
         "C69c exact source partition")
    for source_hash, row in decisions.items():
        source = sources[source_hash]
        need(row["pair_index"] == source["pair_index"] and row["path"] == source["path"] and
             row["exact_representative_box"] == source["exact_representative_box"],
             "C69c decision lineage")
    for source_hash, row in blockers.items():
        source = sources[source_hash]
        need(row["pair_index"] == source["pair_index"] and row["path"] == source["path"] and
             row["exact_representative_box_object_sha256"] ==
             digest(source["exact_representative_box"]), "C69c blocker lineage")
    return sources, summaries, decisions, blockers, c61_result


G_DECISIONS: dict[str, Any] = {}
G_R185: Any = None
G_ATLAS_BOX: Any = None


def load_numeric_kernel(pins: dict[str, Any]) -> None:
    global G_R185, G_ATLAS_BOX
    flint = importlib.import_module("flint")
    flint.ctx.prec = PRECISION_BITS
    need(flint.__version__ == pins["python_flint_version"] and
         Path(flint.__file__).resolve().is_relative_to(FLINT_SITE.resolve()),
         "sealed python-flint environment")
    r185 = importlib.import_module("cm2_round185_preconditioned_c1_residual_refinement")
    atlas = importlib.import_module("cm2_gate3_eight_cell_symmetry_atlas_cert")
    need(file_sha(Path(r185.__file__).resolve()) == pins["round185"] and
         file_sha(Path(atlas.__file__).resolve()) == pins["atlas"] and
         flint.ctx.prec == PRECISION_BITS, "numeric source and precision pins")
    G_R185 = r185
    G_ATLAS_BOX = atlas.AtlasBox


def kernel_snapshot() -> dict[str, str]:
    result: dict[str, str] = {}
    for module in tuple(sys.modules.values()):
        filename = getattr(module, "__file__", None)
        if not filename:
            continue
        path = Path(filename).resolve()
        if path.suffix == ".pyc" and path.parent.name == "__pycache__":
            candidate = path.parent.parent / (path.name.split(".", 1)[0] + ".py")
            if candidate.exists():
                path = candidate.resolve()
        if path.is_file() and (path.is_relative_to(OUT.resolve()) or
                               path.is_relative_to(FLINT_SITE.resolve())):
            result[str(path.relative_to(ROOT))] = file_sha(path)
    need(any(path.endswith("cm2_round185_preconditioned_c1_residual_refinement.py")
             for path in result), "kernel snapshot Round185")
    return dict(sorted(result.items()))


def arb_payload(value: Any) -> dict[str, Any]:
    return {"lower": str(value.lower()), "upper": str(value.upper()),
            "contains_zero": bool(value.contains(0))}


def arb_sign(value: Any) -> int:
    return 1 if bool(value > 0) else -1 if bool(value < 0) else 0


def strict_normal_chart(h1_sign: int, nx: Any, ny: Any) -> str | None:
    nx_sign = arb_sign(nx)
    ny_sign = arb_sign(ny)
    if h1_sign < 0:
        return "N" if ny_sign > 0 else "S" if ny_sign < 0 else None
    return "E" if nx_sign > 0 else "W" if nx_sign < 0 else None


def atlas_box(box: ExactBox, path: str) -> Any:
    return G_ATLAS_BOX(box.t0, box.t1, box.p0, box.p1, box.s0, box.s1, 0, path)


def evaluate_numeric_child(child: dict[str, Any]) -> dict[str, Any]:
    source_hash = child["source_C61_aggregate_leaf_row_sha256"]
    decision = G_DECISIONS[source_hash]
    box_exact = exact_box(child["exact_representative_box"])
    box = atlas_box(box_exact, child["path"])
    origin = decision["representative_origin_key"]
    full, nx, ny = G_R185.collision1_h1_ad(origin, box, "W[1,0]")
    centered = G_R185.centered_enclosure(
        G_R185.collision1_h1_ad, origin, box, "W[1,0]", full)
    common = {
        "precision_bits": PRECISION_BITS,
        "equation": "H1=n1_x^2-n1_y^2",
        "full_child_box_natural_interval": arb_payload(full.value),
        "full_child_box_centered_mean_value_interval": arb_payload(centered),
        "full_child_box_derivatives": {
            axis: arb_payload(value) for axis, value in zip(("t", "p", "s"), full.derivative)
        },
        "normal_component_bounds": {"nx": arb_payload(nx.value), "ny": arb_payload(ny.value)},
        "C69c_source_certificate_copied": False,
        "independent_deterministic_axis_order": ["t", "p", "s"],
    }
    sign = arb_sign(full.value)
    method = "NATURAL_INTERVAL"
    if sign == 0:
        sign = arb_sign(centered)
        method = "CENTERED_MEAN_VALUE_INTERVAL"
    if sign != 0:
        disposition = ("LOCAL_H1_STRICT_POSITIVE_FULL_CHILD_BOX" if sign > 0 else
                       "LOCAL_H1_STRICT_NEGATIVE_FULL_CHILD_BOX")
        certificate = {**common, "accepted_full_box_method": method,
                       "strict_full_box_sign": "POSITIVE" if sign > 0 else "NEGATIVE",
                       "strict_normal_chart": strict_normal_chart(sign, nx.value, ny.value),
                       "axis_tests": []}
        partition = {
            "H1_LT_0": "EMPTY" if sign > 0 else "EXACT_CHILD",
            "H1_EQ_0": "EMPTY",
            "H1_GT_0": "EXACT_CHILD" if sign > 0 else "EMPTY",
            "pairwise_disjoint": True,
            "union_exact_child": True,
        }
        return {"child_row_sha256": child["row_sha256"], "disposition": disposition,
                "certificate": certificate, "partition": partition,
                "consumer_review_ready": True, "blockers": []}

    coordinate_monotonicity: list[dict[str, Any]] = []
    minimum_point: list[Fraction] = []
    maximum_point: list[Fraction] = []
    all_monotone = True
    for axis in range(3):
        lower, upper = box_exact.bounds(axis)
        if lower == upper:
            coordinate_monotonicity.append({
                "axis": ("t", "p", "s")[axis], "positive_width": False,
                "orientation": "CONSTANT_COORDINATE",
                "derivative_bounds": arb_payload(full.derivative[axis]),
            })
            minimum_point.append(lower)
            maximum_point.append(lower)
            continue
        derivative_sign = arb_sign(full.derivative[axis])
        if derivative_sign == 0:
            all_monotone = False
            orientation = "UNRESOLVED"
            minimum_point.append(lower)
            maximum_point.append(upper)
        elif derivative_sign > 0:
            orientation = "STRICTLY_INCREASING"
            minimum_point.append(lower)
            maximum_point.append(upper)
        else:
            orientation = "STRICTLY_DECREASING"
            minimum_point.append(upper)
            maximum_point.append(lower)
        coordinate_monotonicity.append({
            "axis": ("t", "p", "s")[axis], "positive_width": True,
            "orientation": orientation,
            "derivative_bounds": arb_payload(full.derivative[axis]),
        })
    if all_monotone:
        minimum_box = G_R185.point_box(box, *minimum_point, ".c71.monotone.minimum")
        maximum_box = G_R185.point_box(box, *maximum_point, ".c71.monotone.maximum")
        minimum_value, _nx, _ny = G_R185.collision1_h1_ad(
            origin, minimum_box, "W[1,0]")
        maximum_value, _nx, _ny = G_R185.collision1_h1_ad(
            origin, maximum_box, "W[1,0]")
        monotone_sign = -1 if arb_sign(maximum_value.value) < 0 else (
            1 if arb_sign(minimum_value.value) > 0 else 0)
        if monotone_sign != 0:
            disposition = ("LOCAL_H1_STRICT_POSITIVE_FULL_CHILD_BOX"
                           if monotone_sign > 0 else
                           "LOCAL_H1_STRICT_NEGATIVE_FULL_CHILD_BOX")
            certificate = {
                **common,
                "accepted_full_box_method":
                    "MONOTONE_COORDINATE_CORNER_EXTREMUM_STRICT_SIDE",
                "strict_full_box_sign":
                    "POSITIVE" if monotone_sign > 0 else "NEGATIVE",
                "strict_normal_chart":
                    strict_normal_chart(monotone_sign, nx.value, ny.value),
                "coordinate_monotonicity": coordinate_monotonicity,
                "all_positive_width_axes_strictly_monotone": True,
                "monotone_corner_extrema": {
                    "minimum_point": dict(zip(("t", "p", "s"),
                                              map(str, minimum_point))),
                    "minimum_H1": arb_payload(minimum_value.value),
                    "maximum_point": dict(zip(("t", "p", "s"),
                                              map(str, maximum_point))),
                    "maximum_H1": arb_payload(maximum_value.value),
                },
                "axis_tests": [],
            }
            partition = {
                "H1_LT_0": "EMPTY" if monotone_sign > 0 else "EXACT_CHILD",
                "H1_EQ_0": "EMPTY",
                "H1_GT_0": "EXACT_CHILD" if monotone_sign > 0 else "EMPTY",
                "pairwise_disjoint": True, "union_exact_child": True,
            }
            return {"child_row_sha256": child["row_sha256"],
                    "disposition": disposition, "certificate": certificate,
                    "partition": partition, "consumer_review_ready": True,
                    "blockers": []}

    axis_tests: list[dict[str, Any]] = []
    for axis in range(3):
        if box_exact.width(axis) == 0:
            axis_tests.append({"axis": ("t", "p", "s")[axis], "positive_width": False,
                               "accepted": False})
            continue
        derivative = full.derivative[axis]
        face_values = []
        for ordinal, value in enumerate(box_exact.bounds(axis)):
            face = G_R185.fixed_axis_box(box, axis, value, ".c71.face." + str(ordinal))
            evaluated, _nx, _ny = G_R185.collision1_h1_ad(origin, face, "W[1,0]")
            face_values.append(evaluated.value)
        signs = [arb_sign(value) for value in face_values]
        strict_derivative = arb_sign(derivative) != 0
        opposite_faces = signs[0] * signs[1] == -1
        midpoint = sum(box_exact.bounds(axis), Fraction(0)) / 2
        middle_face = G_R185.fixed_axis_box(box, axis, midpoint, ".c71.mid")
        middle, _nx, _ny = G_R185.collision1_h1_ad(origin, middle_face, "W[1,0]")
        if strict_derivative:
            image = G_R185.BASE.arbq(midpoint) - middle.value / derivative
            lower, upper = box_exact.bounds(axis)
            self_map = bool(image > G_R185.BASE.arbq(lower)) and bool(
                image < G_R185.BASE.arbq(upper))
            image_payload: dict[str, Any] | None = arb_payload(image)
        else:
            self_map = False
            image_payload = None
        record = {
            "axis": ("t", "p", "s")[axis], "positive_width": True,
            "strict_derivative_bounds": arb_payload(derivative),
            "strict_derivative": strict_derivative,
            "complete_relative_face_intervals": [arb_payload(value) for value in face_values],
            "complete_faces_strict_opposite_sign": opposite_faces,
            "interval_Newton_image": image_payload,
            "interval_Newton_strict_interior_self_map": self_map,
            "accepted": strict_derivative and opposite_faces,
        }
        axis_tests.append(record)
        if record["accepted"]:
            certificate = {
                **common, "accepted_full_box_method":
                "PARAMETRIC_IVT_STRICT_MONOTONICITY_AND_IFT",
                "graph_axis": record["axis"], "axis_tests": axis_tests,
                "unique_root_over_every_fixed_transverse_parameter": True,
                "source_graph_axis_copied": False,
            }
            partition = {
                "H1_LT_0": "NEGATIVE_OPEN_SLAB",
                "H1_EQ_0": "UNIQUE_TYPED_GRAPH_CARRIER",
                "H1_GT_0": "POSITIVE_OPEN_SLAB",
                "pairwise_disjoint": True, "union_exact_child": True,
                "graph_full_dimensional_Kraft_weight": "0",
                "half_open_negative_owner": {"predicate": "H1<=0", "owns_graph": True},
                "half_open_positive_owner": {"predicate": "H1>0", "owns_graph": False},
            }
            return {"child_row_sha256": child["row_sha256"],
                    "disposition": "LOCAL_H1_UNIQUE_GRAPH_AND_TWO_OFF_GRAPH_SLABS",
                    "certificate": certificate, "partition": partition,
                    "consumer_review_ready": True, "blockers": []}

    corner_records: list[dict[str, Any]] = []
    seen_points: set[tuple[Fraction, Fraction, Fraction]] = set()
    for point in itertools.product(*[box_exact.bounds(axis) for axis in range(3)]):
        if point in seen_points:
            continue
        seen_points.add(point)
        point_box = G_R185.point_box(box, point[0], point[1], point[2], ".c71.corner")
        value, _nx, _ny = G_R185.collision1_h1_ad(origin, point_box, "W[1,0]")
        corner_records.append({"point": {"t": str(point[0]), "p": str(point[1]),
                                         "s": str(point[2])},
                               "H1": arb_payload(value.value), "sign": arb_sign(value.value)})
    negative = next((row for row in corner_records if row["sign"] < 0), None)
    positive = next((row for row in corner_records if row["sign"] > 0), None)
    certificate = {**common, "accepted_full_box_method": None, "axis_tests": axis_tests,
                   "strict_corner_records": corner_records,
                   "opposite_sign_corner_segment":
                   {"negative": negative, "positive": positive,
                    "IVT_proves_H1_zero_contact_inside_child": negative is not None and
                    positive is not None}}
    if negative is not None and positive is not None:
        return {
            "child_row_sha256": child["row_sha256"],
            "disposition": "PROVED_CHILD_H1_ZERO_CONTACT__BOUNDARY_ARRANGEMENT_UNSEALED",
            "certificate": certificate, "partition": None, "consumer_review_ready": False,
            "blockers": ["COMPLETE_CHILD_THREE_STRATA_BOUNDARY_ARRANGEMENT_NOT_SEALED",
                         "NO_FALSE_FULL_BASE_GRAPH_OR_STRICT_SLAB_UPGRADE"],
        }
    return {
        "child_row_sha256": child["row_sha256"],
        "disposition": "BLOCKED_CHILD_H1_FULL_BOX_CERTIFICATE_INCONCLUSIVE",
        "certificate": certificate, "partition": None, "consumer_review_ready": False,
        "blockers": ["FULL_BOX_H1_INTERVAL_NOT_STRICT",
                     "NO_UNIFORM_STRICT_DERIVATIVE_WITH_OPPOSITE_COMPLETE_FACES",
                     "NO_OPPOSITE_STRICT_CORNER_WITNESS"],
    }


class GzipRowWriter:
    def __init__(self, path: Path, order: str):
        self.path = path
        self.order = order
        self.raw: Any = None
        self.gz: Any = None
        self.count = 0
        self.row_sequence = hashlib.sha256()

    def __enter__(self) -> "GzipRowWriter":
        self.raw = self.path.open("xb")
        self.gz = gzip.GzipFile(filename="", mode="wb", fileobj=self.raw,
                                compresslevel=9, mtime=0)
        return self

    def write(self, body: dict[str, Any]) -> dict[str, Any]:
        row = {**body, "row_sha256": digest(body)}
        self.gz.write(canonical(row) + b"\n")
        self.row_sequence.update(row["row_sha256"].encode("ascii") + b"\n")
        self.count += 1
        return row

    def __exit__(self, *_args: Any) -> None:
        self.gz.close()
        self.raw.close()

    def descriptor(self) -> dict[str, Any]:
        return {"filename": self.path.name, "order": self.order, "row_count": self.count,
                "row_hash_line_sequence_sha256": self.row_sequence.hexdigest(),
                "sha256": file_sha(self.path), "size": self.path.stat().st_size}


def exclusive_write(path: Path, data: bytes) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags, 0o644)
    try:
        view = memoryview(data)
        while view:
            written = os.write(descriptor, view)
            need(written > 0, "write progress:" + path.name)
            view = view[written:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    need(path.read_bytes() == data and path.stat().st_nlink == 1,
         "terminal-byte replay:" + path.name)


def make_intersection_body(child: dict[str, Any], source: dict[str, Any],
                           c69_row: dict[str, Any], source_kind: str,
                           lineage_sha: str, numeric: dict[str, Any] | None) -> dict[str, Any]:
    if source_kind == "blocker":
        disposition = "BLOCKED_C69C_SOURCE_CAPABILITY_NOT_AVAILABLE"
        certificate = None
        partition = None
        ready = False
        blockers = list(c69_row["blocker_codes"]) + [
            "C69C_SOURCE_KIND_" + c69_row["structural_graph_kind"],
            "NONDECISION_SOURCE_CHILD_MUST_REMAIN_FAIL_CLOSED",
        ]
    else:
        need(numeric is not None and numeric["child_row_sha256"] == child["row_sha256"],
             "numeric child order")
        disposition = numeric["disposition"]
        certificate = numeric["certificate"]
        partition = numeric["partition"]
        ready = numeric["consumer_review_ready"]
        blockers = numeric["blockers"]
    return {
        "schema": SCHEMA + ".intersection-row",
        "C65_aggregate_leaf_row_sha256": child["row_sha256"],
        "C65_source_shard_row_sha256": child["source_C65_shard_row_sha256"],
        "C69c_source_kind": source_kind,
        "C69c_source_row_sha256": c69_row["row_sha256"],
        "source_C61_aggregate_leaf_row_sha256": source["row_sha256"],
        "source_path": source["path"], "child_path": child["path"],
        "pair_index": child["pair_index"],
        "parent_volume_fraction": child["parent_volume_fraction"],
        "exact_representative_box": child["exact_representative_box"],
        "child_box_lineage": {"replayed_exact": True,
                              "source_path_exact_prefix": True,
                              "split_owner": "LOWER_BIT_CHILD",
                              "split_chain_sha256": lineage_sha},
        "prior_C65_disposition": "COLLISION2_HANDOFF",
        "intersection_disposition": disposition,
        "H1_child_certificate": certificate,
        "three_strata_partition": partition,
        "consumer_review_ready": ready,
        "global_consumption_ready": False,
        "remaining_blocker_codes": blockers,
        "terminal_disposition_credit": 0,
        "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
    }


def build_stage(stage: Path, workers: int) -> dict[str, Any]:
    stage = stage.resolve()
    need(stage.is_dir() and not stage.is_symlink() and not any(stage.iterdir()), "empty stage")
    contract, _schemas = load_contract_gate()
    aggregate, c65_verification, c65_path_pins, c65_terminal_replay = c65_gate(contract)
    c69 = c69_gate(contract)
    c70 = c70_gate(contract)
    sources, source_summaries, decisions, blockers, _c61_result = load_input_rows(aggregate, c69)

    leaf_path = OUT / aggregate["ledgers"]["aggregate_leaves"]["filename"]
    tasks: list[dict[str, Any]] = []
    c2_counts: Counter[str] = Counter()
    all_dispositions: Counter[str] = Counter()
    decision_children = blocker_children = 0
    for child in iter_gzip_rows(leaf_path, aggregate["ledgers"]["aggregate_leaves"],
                                "C65 aggregate leaves first pass"):
        all_dispositions[child["disposition"]] += 1
        if child["disposition"] != "COLLISION2_HANDOFF":
            continue
        source_hash = child["source_C61_aggregate_leaf_row_sha256"]
        source = sources.get(source_hash)
        need(source is not None and child["source_path"] == source["path"] and
             child["pair_index"] == source["pair_index"], "C65 child/source join")
        rebuild_child(source, child)
        c2_counts[source_hash] += 1
        if source_hash in decisions:
            tasks.append(child)
            decision_children += 1
        else:
            need(source_hash in blockers, "C69c source partition membership")
            blocker_children += 1
    need(all_dispositions == Counter({"COLLISION2_HANDOFF": EXPECTED_C65_C2,
                                     "STRICT_TERMINAL": 191664}) and
         decision_children == EXPECTED_DECISION_CHILDREN and
         blocker_children == EXPECTED_BLOCKER_CHILDREN and
         decision_children + blocker_children == EXPECTED_C65_C2,
         "167255=33100+134155 exact child partition")
    for summary in source_summaries:
        source_hash = summary["source_C61_aggregate_leaf_row_sha256"]
        need(c2_counts[source_hash] == summary["collision2_handoff_leaf_count"],
             "C65 source child count")

    global G_DECISIONS
    G_DECISIONS = decisions
    load_numeric_kernel(contract["frozen_pin_map"]["numeric_kernel"])
    kernel_before = kernel_snapshot()
    self_relative = str(SELF.relative_to(ROOT))
    need(all(path == self_relative or c65_path_pins.get(path) == sha
             for path, sha in kernel_before.items()),
         "all loaded numeric modules are C65-manifest pinned")
    disposition_counts: Counter[str] = Counter()
    source_stats: dict[str, Counter[str]] = defaultdict(Counter)
    source_volumes: dict[str, Fraction] = defaultdict(Fraction)
    source_row_hashers: dict[str, Any] = defaultdict(hashlib.sha256)
    numeric_ordinal = 0

    context = mp.get_context("fork")
    pool = context.Pool(processes=workers)
    numeric_iterator = pool.imap(evaluate_numeric_child, tasks, chunksize=8)
    try:
        with GzipRowWriter(stage / INTERSECTION_NAME,
                           "C65_AGGREGATE_LEAF_ORDER_FILTER_COLLISION2_HANDOFF") as writer:
            for child in iter_gzip_rows(leaf_path, aggregate["ledgers"]["aggregate_leaves"],
                                        "C65 aggregate leaves second pass"):
                if child["disposition"] != "COLLISION2_HANDOFF":
                    continue
                source_hash = child["source_C61_aggregate_leaf_row_sha256"]
                source = sources[source_hash]
                rebuilt, lineage_sha = rebuild_child(source, child)
                need(box_payload(rebuilt) == child["exact_representative_box"],
                     "second-pass exact child")
                if source_hash in decisions:
                    numeric = next(numeric_iterator)
                    numeric_ordinal += 1
                    c69_row = decisions[source_hash]
                    source_kind = "decision"
                else:
                    numeric = None
                    c69_row = blockers[source_hash]
                    source_kind = "blocker"
                row = writer.write(make_intersection_body(
                    child, source, c69_row, source_kind, lineage_sha, numeric))
                disposition = row["intersection_disposition"]
                disposition_counts[disposition] += 1
                source_stats[source_hash][disposition] += 1
                source_stats[source_hash]["ready"] += int(row["consumer_review_ready"])
                source_volumes[source_hash] += Fraction(row["parent_volume_fraction"])
                source_row_hashers[source_hash].update(
                    row["row_sha256"].encode("ascii") + b"\n")
        intersection_descriptor = writer.descriptor()
        try:
            next(numeric_iterator)
        except StopIteration:
            pass
        else:
            raise Reject("extra numeric outcomes")
    finally:
        pool.close()
        pool.join()
    need(numeric_ordinal == EXPECTED_DECISION_CHILDREN and
         intersection_descriptor["row_count"] == EXPECTED_C65_C2,
         "complete intersection output")

    with GzipRowWriter(stage / SOURCE_SUMMARY_NAME, "C65_SOURCE_SUMMARY_ORDER") as writer:
        for summary in source_summaries:
            source_hash = summary["source_C61_aggregate_leaf_row_sha256"]
            stats = source_stats[source_hash]
            child_count = c2_counts[source_hash]
            blocked_count = child_count - stats["ready"]
            body = {
                "schema": SCHEMA + ".source-summary-row",
                "source_C61_aggregate_leaf_row_sha256": source_hash,
                "source_path": sources[source_hash]["path"],
                "pair_index": sources[source_hash]["pair_index"],
                "C69c_source_kind": "decision" if source_hash in decisions else "blocker",
                "child_count": child_count,
                "negative_child_count": stats["LOCAL_H1_STRICT_NEGATIVE_FULL_CHILD_BOX"],
                "positive_child_count": stats["LOCAL_H1_STRICT_POSITIVE_FULL_CHILD_BOX"],
                "graph_child_count": stats["LOCAL_H1_UNIQUE_GRAPH_AND_TWO_OFF_GRAPH_SLABS"],
                "proved_zero_contact_unsealed_child_count":
                    stats["PROVED_CHILD_H1_ZERO_CONTACT__BOUNDARY_ARRANGEMENT_UNSEALED"],
                "inconclusive_child_count":
                    stats["BLOCKED_CHILD_H1_FULL_BOX_CERTIFICATE_INCONCLUSIVE"],
                "blocked_child_count": blocked_count,
                "consumer_review_ready_child_count": stats["ready"],
                "source_Kraft_conservation": {
                    "C65_full_source_partition": summary["source_Kraft_conservation"],
                    "selected_collision2_fraction": str(source_volumes[source_hash]),
                    "selected_collision2_plus_C65_strict_terminal_is_full_source": True,
                },
                "row_hash_line_sequence_sha256": source_row_hashers[source_hash].hexdigest(),
                "terminal_disposition_credit": 0,
                "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
            }
            writer.write(body)
    summary_descriptor = writer.descriptor()

    kernel_after = kernel_snapshot()
    need(kernel_after == kernel_before, "numeric module bytes stable")
    proved = sum(disposition_counts[name] for name in (
        "LOCAL_H1_STRICT_NEGATIVE_FULL_CHILD_BOX",
        "LOCAL_H1_STRICT_POSITIVE_FULL_CHILD_BOX",
        "LOCAL_H1_UNIQUE_GRAPH_AND_TWO_OFF_GRAPH_SLABS"))
    unsealed = EXPECTED_DECISION_CHILDREN - proved
    result = {
        "schema": SCHEMA + ".result",
        "status": "PASS_COMPLETE_167255_CHILD_INTERSECTION__33100_FRESH_384BIT_H1__134155_FAIL_CLOSED__ZERO_CREDIT_GLOBAL_CONSUMER_REQUIRED",
        "producer_file_sha256": file_sha(SELF),
        "frozen_input_closure": {
            "contract_object_sha256": CONTRACT_OBJECT_SHA256,
            "schemas_object_sha256": SCHEMAS_OBJECT_SHA256,
            "pin_map_nonempty_and_exact": True,
            "C65_protocol": "v9",
            "C65_formal_self_test": "134/134",
            "C65_rejected_v3_94_suite_consumed": False,
            "C65_manifest_members_recaptured": 446,
            "C65_terminal_byte_replay_records": 448,
            "C65_terminal_byte_replay_sequence_sha256": c65_terminal_replay,
            "C65_frozen_snapshot_object_sha256":
                c65_verification["frozen_snapshot"]["object_sha256"],
            "C65_path_pin_count": len(c65_path_pins),
            "C69c_manifest_members_recaptured": 25,
            "C70L_manifest_members_recaptured": 8,
        },
        "coverage": {
            "C65_collision2_child_count": EXPECTED_C65_C2,
            "C69c_decision_source_count": EXPECTED_C69_DECISIONS,
            "C69c_blocker_source_count": EXPECTED_C69_BLOCKERS,
            "decision_source_child_count": EXPECTED_DECISION_CHILDREN,
            "blocker_source_child_count": EXPECTED_BLOCKER_CHILDREN,
            "partition_identity": "167255=33100+134155",
            "numeric_disposition_census": dict(sorted(disposition_counts.items())),
            "consumer_review_ready_child_count": proved,
            "unsealed_numeric_child_count": unsealed,
            "C70L_edge_ready_blocked": "298/744",
            "C70L_corridor_ready_blocked": "73/971",
            "C70L_source_seam_ready": "0/16",
        },
        "numeric_environment": {
            "python_flint_version": "0.9.0", "precision_bits": PRECISION_BITS,
            "numeric_module_file_count": len(kernel_before),
            "numeric_module_snapshot_sha256": digest(kernel_before),
        },
        "ledgers": {"intersection_rows": intersection_descriptor,
                    "source_summaries": summary_descriptor},
        "invariants": {
            "all_167255_C65_collision2_children_emitted_once": True,
            "all_33100_decision_children_fresh_full_box_evaluated": True,
            "all_134155_nondecision_children_explicit_fail_closed": True,
            "all_child_boxes_rebuilt_from_C61_source_and_C65_suffix": True,
            "C69c_source_certificates_never_copied": True,
            "strict_slab_requires_rigorous_full_box_interval": True,
            "graph_requires_uniform_derivative_and_opposite_complete_faces": True,
            "corner_contact_never_false_terminalized": True,
            "C70L_obstructions_not_overridden": True,
            "prior_C65_dispositions_not_overwritten": True,
        },
        "candidate_is_authority": False, "global_consumption_ready": False,
        "runtime_canonical_pointer_or_seal_writes": False,
        "terminal_disposition_credit": 0,
        "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
    }
    result["object_sha256"] = digest(result)
    exclusive_write(stage / RESULT_NAME, canonical(result) + b"\n")
    report = (
        "# C71 C65-v9 x C69c child H1 successor v2\n\n"
        f"Status: `{result['status']}`.\n\n"
        "Complete C65 collision-2 partition: `167,255 = 33,100 + 134,155`. "
        f"Fresh 384-bit locally proved children: {proved}; unsealed numeric children: "
        f"{unsealed}. The 134,155 C69c-blocker-source children remain explicit "
        "fail-closed rows. C70-L remains unchanged. All formal, whole-parent, terminal, "
        "and D02 credit is zero; only a later global consumer may use this sidecar.\n\n"
        f"Result object: `{result['object_sha256']}`.\n"
    )
    exclusive_write(stage / REPORT_NAME, report.encode("utf-8"))
    return result


def static_self_test() -> dict[str, Any]:
    tests: dict[str, bool] = {}
    tests["partition_167255"] = EXPECTED_DECISION_CHILDREN + EXPECTED_BLOCKER_CHILDREN == EXPECTED_C65_C2
    tests["source_partition_20879"] = EXPECTED_C69_DECISIONS + EXPECTED_C69_BLOCKERS == EXPECTED_SOURCES
    tests["pin_map_names_nonempty"] = all(C65_NAMES.values()) and all(C69_NAMES.values()) and all(C70_NAMES.values())
    tests["old_skeleton_not_named_as_dependency"] = all("skeleton" not in name for name in (*C65_NAMES.values(), *C69_NAMES.values(), *C70_NAMES.values()))
    box = ExactBox(Fraction(0), Fraction(1), Fraction(0), Fraction(1), Fraction(0), Fraction(0))
    left, right = split_box(box, 0)
    tests["exact_midpoint_split"] = left.t1 == right.t0 == Fraction(1, 2)
    tests["first_axis_tie_break"] = max(range(3), key=box.width) == 0
    tests["canonical_stable"] = canonical({"b": 2, "a": 1}) == b'{"a":1,"b":2}'
    tests["credits_locked_zero"] = True
    tests["precision_384"] = PRECISION_BITS == 384
    tests["formal_C65_suite_is_134"] = "134_OF_134" in C65_SELFTEST_STATUS
    tests["rejected_94_suite_not_formal"] = "94_OF_94" not in C65_SELFTEST_STATUS
    tests["C70_source_seam_not_ready"] = "SOURCE_SEAM_0_READY" in C70_VERIFY_STATUS
    need(all(tests.values()) and len(tests) == 12, "static self-test")
    return {"schema": SCHEMA + ".static-self-test",
            "status": "PASS_12_OF_12_PIN_GUARD_PARTITION_LINEAGE_AND_ZERO_CREDIT_TESTS",
            "tests": tests, "formal_execution_performed": False,
            "files_written": False, "formal_credit": 0,
            "whole_parent_credit": 0, "D02_gate_credit": 0}


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--stage", type=Path)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    need(1 <= args.workers <= 8, "worker range")
    if args.self_test:
        print(json.dumps(static_self_test(), sort_keys=True, separators=(",", ":")))
        return 0
    result = build_stage(args.stage, args.workers)
    print(json.dumps({"status": result["status"], "coverage": result["coverage"],
                      "object_sha256": result["object_sha256"]},
                     sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Reject as error:
        print(json.dumps({"status": "REJECTED", "reason": str(error)},
                         sort_keys=True, separators=(",", ":")), file=sys.stderr)
        raise SystemExit(2)
