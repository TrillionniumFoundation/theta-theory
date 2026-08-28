#!/usr/bin/env python3
"""C69c descriptor-repair supersession for the sealed C69b ledgers.

This wrapper never imports or executes the C69b producer and never rewrites or
numerically recomputes a ledger.  It authenticates the C69b publication
receipt, reads the three already-sealed gzip byte streams, validates every row
self-hash, and reconstructs descriptors from the final bytes.  The C69b result
tuple whose descriptors were captured before gzip close is terminally rejected.

Build output is permitted only in an empty staging directory.  Publication
requires two byte-identical stages and uses O_EXCL/no-replace creation.
"""
from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import io
import json
import os
import stat
import sys
from pathlib import Path
from typing import Any, Iterable

sys.dont_write_bytecode = True

SELF = Path(__file__).absolute()
ROOT = SELF.parents[1]
OUT = ROOT / "deliverables"
PREFIX = "cm2_round306c69c_descriptor_repair_supersession_v1"
SCHEMA = "cm2.round306c69c.descriptor-repair-supersession.v1"

CONTRACT = PREFIX + "_contract.json"
REJECTION = PREFIX + "_rejection.json"
RESULT = PREFIX + "_corrected_result.json"
REPORT = PREFIX + "_report.md"
RECEIPT = PREFIX + "_deterministic_two_stage_publication_receipt.json"
STAGE_NAMES = [CONTRACT, REJECTION, REPORT, RESULT]

C69B_PREFIX = "cm2_round306c69b_singleton_h1_graph_slab_decider_v2"
C69B_PRODUCER = OUT / (C69B_PREFIX + ".py")
C69B_CONTRACT = OUT / (C69B_PREFIX + "_contract.json")
C69B_COVERS = OUT / (C69B_PREFIX + "_parametric_newton_covers.jsonl.gz")
C69B_DECISIONS = OUT / (C69B_PREFIX + "_decisions.jsonl.gz")
C69B_BLOCKERS = OUT / (C69B_PREFIX + "_blockers.jsonl.gz")
C69B_REPORT = OUT / (C69B_PREFIX + "_report.md")
C69B_RESULT = OUT / (C69B_PREFIX + "_result.json")
C69B_RECEIPT = OUT / (C69B_PREFIX + "_deterministic_two_stage_publication_receipt.json")
CANON = OUT / "CM2_LATEST_STATUS.md"
HEAD = ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"

PINS = {
    "C69B_PRODUCER": "e45244027963f11f150127b83803416d516af166f030d192a32648e3ff15f549",
    "C69B_CONTRACT": "1d0da21eb1f6a658d0b072eb4ae56e7f1086e5c3c19c47252d8ba333cc13d36d",
    "C69B_CONTRACT_OBJECT": "3aa04ebd6ca8c7e7e07656817dd3c75366894014aba26a7d034782a553e23faf",
    "C69B_COVERS": "e8512d9f325e305e134400dac27c7c62ee374a1957d12f0acce797d00a7dd259",
    "C69B_DECISIONS": "b9bc1cd359c77ee6a5246011925090e5d5557cd88e90d1f5c67fa70a452d1eba",
    "C69B_BLOCKERS": "69b3ec294f95cb5ce377e553ae875daab10a5bdb33e860363f6bae122022e606",
    "C69B_REPORT": "328ac13b8d372002baa5a040e5532bbeb1bf030fe9c7fdf3e61327b508dc69df",
    "C69B_RESULT": "63a1faa4528e35a0bbbbe282befeaeb75eda1f8635634c22572bddfc91e953b3",
    "C69B_RESULT_OBJECT": "243776d4856652b307bd8dc9198992b1ac9bae9761017b4b764bbcd351c1da8b",
    "C69B_RECEIPT": "e849a5e3d03872657f7619c62831777dd5130f1801aed61d477d49e8e4505030",
    "C69B_RECEIPT_OBJECT": "ed5cb9200bd0ab71bf0cff5ffc484c2ab1daef978e34c4e91a621cfaba182418",
    "CANON": "922fc5d01918b217556bc3f392c44efcc7c9c6345c881371e6cd34950eb99b57",
    "HEAD": "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3",
    "AUTHORITY_SNAPSHOT": "cdb6f4be57b2732a6ad67f4113a41c338934358e8e3102f71e1a958c2c46e8c2",
}

PATHS = {
    "C69B_PRODUCER": C69B_PRODUCER,
    "C69B_CONTRACT": C69B_CONTRACT,
    "C69B_COVERS": C69B_COVERS,
    "C69B_DECISIONS": C69B_DECISIONS,
    "C69B_BLOCKERS": C69B_BLOCKERS,
    "C69B_REPORT": C69B_REPORT,
    "C69B_RESULT": C69B_RESULT,
    "C69B_RECEIPT": C69B_RECEIPT,
    "CANON": CANON,
    "HEAD": HEAD,
}

LEDGER_SPECS = {
    "parametric_newton_covers": {
        "path_key": "C69B_COVERS",
        "filename": C69B_COVERS.name,
        "order": "DECISION_ORDER_THEN_COVER_PREFIX",
        "row_count": 2,
        "row_hash_line_sequence_sha256": "bd9b02cd7d27e55158b4dd964ce42cf0603f4725ba16f07f47e4b2d4623f442d",
        "schema": "cm2.round306c69b.singleton-h1-graph-slab-decider.v2.parametric-newton-cover-row",
        "size": 850,
    },
    "decisions": {
        "path_key": "C69B_DECISIONS",
        "filename": C69B_DECISIONS.name,
        "order": "C68_C61_FILTERED_ORDER",
        "row_count": 2356,
        "row_hash_line_sequence_sha256": "706e6d15b3cf5a9f010c20e77974528399696dd2df18f4c65ceabfe1c4a4c040",
        "schema": "cm2.round306c69b.singleton-h1-graph-slab-decider.v2.decision-row",
        "size": 1280359,
    },
    "blockers": {
        "path_key": "C69B_BLOCKERS",
        "filename": C69B_BLOCKERS.name,
        "order": "C68_C61_FILTERED_ORDER",
        "row_count": 18523,
        "row_hash_line_sequence_sha256": "7b14e43030218bb448a3192e1e27a03e48ebf0a1627f8cd59a6167c7fb39e7e7",
        "schema": "cm2.round306c69b.singleton-h1-graph-slab-decider.v2.blocker-row",
        "size": 3179863,
    },
}

REJECTED_DESCRIPTORS = {
    "parametric_newton_covers": {
        "filename": C69B_COVERS.name,
        "order": "DECISION_ORDER_THEN_COVER_PREFIX",
        "row_count": 2,
        "row_hash_line_sequence_sha256": "bd9b02cd7d27e55158b4dd964ce42cf0603f4725ba16f07f47e4b2d4623f442d",
        "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "size": 0,
    },
    "decisions": {
        "filename": C69B_DECISIONS.name,
        "order": "C68_C61_FILTERED_ORDER",
        "row_count": 2356,
        "row_hash_line_sequence_sha256": "706e6d15b3cf5a9f010c20e77974528399696dd2df18f4c65ceabfe1c4a4c040",
        "sha256": "57ff475399d1684bb6881f76666e7d155003411599a96fc559b461e2ade2a956",
        "size": 1265219,
    },
    "blockers": {
        "filename": C69B_BLOCKERS.name,
        "order": "C68_C61_FILTERED_ORDER",
        "row_count": 18523,
        "row_hash_line_sequence_sha256": "7b14e43030218bb448a3192e1e27a03e48ebf0a1627f8cd59a6167c7fb39e7e7",
        "sha256": "2107f233ac736aac9e83f1c26ee0cd32df81f1f3675d20d11796afdafa2e44c5",
        "size": 3160775,
    },
}

SEMANTIC_KEYS = (
    "acceptance_layer_census",
    "decision_axis_census",
    "decision_face_orientation_census",
    "decision_pair_census",
    "decision_pair_source_volume_fraction",
    "global_invariants",
    "input_category_census",
    "input_file_identities",
    "input_file_sha256",
    "input_object_sha256",
    "layer_B_cover_depth_census",
    "numeric_environment",
    "scope",
)


class FailClosed(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise FailClosed(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode()


def digest(value: Any) -> str:
    blob = value if isinstance(value, bytes) else canonical(value)
    return hashlib.sha256(blob).hexdigest()


def sequence_hash(values: Iterable[str]) -> str:
    state = hashlib.sha256()
    for value in values:
        state.update(value.encode("ascii") + b"\n")
    return state.hexdigest()


def identity(st: os.stat_result) -> dict[str, int]:
    return {
        "dev": st.st_dev,
        "ino": st.st_ino,
        "mode": st.st_mode,
        "size": st.st_size,
        "mtime_ns": st.st_mtime_ns,
        "nlink": st.st_nlink,
    }


def stable_bytes(path: Path) -> tuple[bytes, dict[str, int]]:
    before = os.lstat(path)
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "regular-single-link:" + path.name)
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    try:
        opened = os.fstat(fd)
        need(identity(before) == identity(opened), "path-fd-identity:" + path.name)
        chunks: list[bytes] = []
        while True:
            chunk = os.read(fd, 1 << 20)
            if not chunk:
                break
            chunks.append(chunk)
        after_fd = os.fstat(fd)
    finally:
        os.close(fd)
    after_path = os.lstat(path)
    need(identity(before) == identity(after_fd) == identity(after_path), "stable-input:" + path.name)
    blob = b"".join(chunks)
    need(len(blob) == before.st_size, "complete-input:" + path.name)
    return blob, identity(before)


def secure_bytes(path: Path, expected: str) -> tuple[bytes, dict[str, int]]:
    blob, file_identity = stable_bytes(path)
    need(digest(blob) == expected, "input-sha256:" + path.name)
    return blob, file_identity


def json_object(blob: bytes, label: str) -> dict[str, Any]:
    value = json.loads(blob, parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)))
    need(type(value) is dict, "json-object:" + label)
    return value


def close_object(value: dict[str, Any], expected: str, label: str) -> None:
    body = dict(value)
    claimed = body.pop("object_sha256", None)
    need(claimed == expected and digest(body) == expected, "object-closure:" + label)


def authority_snapshot() -> str:
    state = hashlib.sha256()
    for path in (CANON, HEAD):
        blob, file_identity = stable_bytes(path)
        state.update(
            (
                str(path.relative_to(ROOT))
                + "\0"
                + json.dumps(file_identity, sort_keys=True)
            ).encode()
            + b"\n"
        )
        state.update(hashlib.sha256(blob).digest())
    return state.hexdigest()


def exclusive(path: Path, blob: bytes) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags, 0o644)
    try:
        view = memoryview(blob)
        while view:
            written = os.write(fd, view)
            need(written > 0, "exclusive-write:" + path.name)
            view = view[written:]
        os.fsync(fd)
    finally:
        os.close(fd)
    after, _ = stable_bytes(path)
    need(after == blob, "exclusive-post:" + path.name)


def secure_empty_stage(stage: Path) -> None:
    st = os.lstat(stage)
    need(stat.S_ISDIR(st.st_mode) and not stat.S_ISLNK(st.st_mode), "stage-directory")
    need(stage != OUT and not any(stage.iterdir()), "empty-stage")


def rebuilt_descriptor(blob: bytes, ledger_name: str, spec: dict[str, Any]) -> dict[str, Any]:
    hashes: list[str] = []
    row_count = 0
    with gzip.GzipFile(fileobj=io.BytesIO(blob), mode="rb") as stream:
        for index, line in enumerate(stream):
            need(line.endswith(b"\n") and line != b"\n", f"{ledger_name}-line:{index}")
            row = json_object(line, f"{ledger_name}-row:{index}")
            need(line == canonical(row) + b"\n", f"{ledger_name}-canonical-row-bytes:{index}")
            need(row.get("schema") == spec["schema"], f"{ledger_name}-schema:{index}")
            body = dict(row)
            claimed = body.pop("row_sha256", None)
            need(type(claimed) is str and len(claimed) == 64, f"{ledger_name}-row-hash-shape:{index}")
            need(digest(body) == claimed, f"{ledger_name}-row-self-hash:{index}")
            # C69b row schemas do not all carry the same optional credit keys.
            # Every credit field that is present must be exactly zero, while
            # formal and D02 credit are mandatory in all three row types.
            need(row.get("formal_credit") == 0, f"{ledger_name}-zero-formal-credit:{index}")
            need(row.get("D02_gate_credit") == 0, f"{ledger_name}-zero-D02-credit:{index}")
            credit_keys = [key for key in row if key == "credit" or key.endswith("_credit")]
            need(all(row[key] == 0 for key in credit_keys), f"{ledger_name}-all-present-credits-zero:{index}")
            hashes.append(claimed)
            row_count += 1
    descriptor = {
        "filename": spec["filename"],
        "order": spec["order"],
        "row_count": row_count,
        "row_hash_line_sequence_sha256": sequence_hash(hashes),
        "sha256": digest(blob),
        "size": len(blob),
    }
    need(row_count == spec["row_count"], ledger_name + "-row-count")
    need(descriptor["row_hash_line_sequence_sha256"] == spec["row_hash_line_sequence_sha256"], ledger_name + "-row-sequence")
    need(descriptor["size"] == spec["size"], ledger_name + "-size")
    return descriptor


def validate_source() -> tuple[dict[str, bytes], dict[str, Any], dict[str, Any], dict[str, dict[str, Any]]]:
    blobs: dict[str, bytes] = {}
    for key, path in PATHS.items():
        blobs[key], _ = secure_bytes(path, PINS[key])

    old_contract = json_object(blobs["C69B_CONTRACT"], "C69b-contract")
    old_result = json_object(blobs["C69B_RESULT"], "C69b-result")
    old_receipt = json_object(blobs["C69B_RECEIPT"], "C69b-receipt")
    close_object(old_contract, PINS["C69B_CONTRACT_OBJECT"], "C69b-contract")
    close_object(old_result, PINS["C69B_RESULT_OBJECT"], "C69b-result")
    close_object(old_receipt, PINS["C69B_RECEIPT_OBJECT"], "C69b-receipt")

    need(old_result["producer_file_sha256"] == PINS["C69B_PRODUCER"], "C69b-result-producer")
    need(old_result["contract_file_sha256"] == PINS["C69B_CONTRACT"], "C69b-result-contract-file")
    need(old_result["contract_object_sha256"] == PINS["C69B_CONTRACT_OBJECT"], "C69b-result-contract-object")
    need(old_result["object_sha256"] == old_receipt["result_object_sha256"], "C69b-receipt-result-object")
    need(old_receipt["producer_file_sha256"] == PINS["C69B_PRODUCER"], "C69b-receipt-producer")
    need(old_receipt["status"] == "PASS_TWO_BYTE_IDENTICAL_STAGES__EXCLUSIVE_NO_REPLACE_PUBLICATION__ZERO_CREDIT", "C69b-receipt-status")
    need(old_receipt["all_stage_bytes_identical"] is True, "C69b-receipt-stage-identity")
    need(old_receipt["publication_O_EXCL_no_replace"] is True, "C69b-receipt-no-replace")
    need(old_receipt["result_published_last"] is True, "C69b-receipt-result-last")
    need(old_receipt["runtime_or_canonical_written"] is False, "C69b-receipt-runtime")
    need(old_receipt["formal_credit"] == old_receipt["D02_gate_credit"] == 0, "C69b-receipt-zero-credit")
    need(old_receipt["published_files"][C69B_RESULT.name] == {"sha256": PINS["C69B_RESULT"], "size": len(blobs["C69B_RESULT"])}, "C69b-receipt-result-file")
    old_stage_order = [
        ("C69B_CONTRACT", C69B_CONTRACT.name),
        ("C69B_COVERS", C69B_COVERS.name),
        ("C69B_DECISIONS", C69B_DECISIONS.name),
        ("C69B_BLOCKERS", C69B_BLOCKERS.name),
        ("C69B_REPORT", C69B_REPORT.name),
        ("C69B_RESULT", C69B_RESULT.name),
    ]
    for key, filename in old_stage_order:
        need(
            old_receipt["published_files"][filename]
            == {"sha256": PINS[key], "size": len(blobs[key])},
            "C69b-receipt-published-file:" + filename,
        )
    old_stage_sequence = sequence_hash(PINS[key] for key, _ in old_stage_order)
    need(old_receipt["stage_1_file_hash_sequence_sha256"] == old_stage_sequence, "C69b-receipt-stage1-sequence")
    need(old_receipt["stage_2_file_hash_sequence_sha256"] == old_stage_sequence, "C69b-receipt-stage2-sequence")
    need(old_receipt["authority_snapshot_before_sha256"] == PINS["AUTHORITY_SNAPSHOT"], "C69b-receipt-authority-before")
    need(old_receipt["authority_snapshot_after_sha256"] == PINS["AUTHORITY_SNAPSHOT"], "C69b-receipt-authority-after")
    need(old_result["authority_snapshot_before_sha256"] == PINS["AUTHORITY_SNAPSHOT"], "C69b-result-authority-before")
    need(old_result["authority_snapshot_after_sha256"] == PINS["AUTHORITY_SNAPSHOT"], "C69b-result-authority-after")
    need(old_result["ledgers"] == REJECTED_DESCRIPTORS, "exact-rejected-descriptor-tuple")

    scope = old_result["scope"]
    need(scope["input_task_count"] == 20879, "C69b-input-task-count")
    need(scope["decision_count"] == 2356 and scope["total_blocker_count"] == 18523, "C69b-disposition-counts")
    need(scope["parametric_cover_row_count"] == 2, "C69b-cover-count")
    need(scope["formal_credit"] == scope["D02_gate_credit"] == 0, "C69b-scope-zero-credit")
    boundary = old_result["strict_boundary"]
    need(boundary["runtime_or_canonical_written"] is False, "C69b-runtime-boundary")
    need(boundary["formal_credit"] == boundary["whole_parent_credit"] == boundary["D02_gate_credit"] == 0, "C69b-boundary-zero-credit")

    corrected: dict[str, dict[str, Any]] = {}
    for ledger_name, spec in LEDGER_SPECS.items():
        key = spec["path_key"]
        receipt_entry = old_receipt["published_files"][spec["filename"]]
        need(receipt_entry == {"sha256": PINS[key], "size": spec["size"]}, ledger_name + "-receipt-final-bytes")
        corrected[ledger_name] = rebuilt_descriptor(blobs[key], ledger_name, spec)
        need(corrected[ledger_name]["sha256"] == PINS[key], ledger_name + "-actual-file-pin")
        old = REJECTED_DESCRIPTORS[ledger_name]
        for field in ("filename", "order", "row_count", "row_hash_line_sequence_sha256"):
            need(old[field] == corrected[ledger_name][field], ledger_name + "-unchanged-" + field)
        need(old["sha256"] != corrected[ledger_name]["sha256"] and old["size"] != corrected[ledger_name]["size"], ledger_name + "-preclose-defect-witness")

    need(corrected["decisions"]["row_count"] + corrected["blockers"]["row_count"] == scope["input_task_count"], "corrected-disposition-partition")
    need(corrected["parametric_newton_covers"]["row_count"] == scope["parametric_cover_row_count"], "corrected-cover-census")
    return blobs, old_result, old_receipt, corrected


def mathematical_contract(blobs: dict[str, bytes], old_receipt: dict[str, Any]) -> dict[str, Any]:
    contract = {
        "schema": SCHEMA + ".contract",
        "status": "FROZEN_SEALED_LEDGER_DESCRIPTOR_REPAIR_SUPERSESSION_PROTOCOL__ZERO_CREDIT",
        "producer_file_sha256": digest(SELF.read_bytes()),
        "defect": {
            "code": "C69B_RESULT_CAPTURED_GZIP_DESCRIPTORS_BEFORE_GZIP_WRITER_CLOSE",
            "effect": "RECORDED_LEDGER_SHA256_AND_SIZE_DESCRIBED_PRE_FOOTER_BYTES_AND_DO_NOT_BIND_THE_PUBLISHED_GZIP_STREAMS",
            "unaffected_fields": ["filename", "order", "row_count", "row_hash_line_sequence_sha256"],
        },
        "terminal_rejection_rule": {
            "rejected_result_file_sha256": PINS["C69B_RESULT"],
            "rejected_result_object_sha256": PINS["C69B_RESULT_OBJECT"],
            "rejected_descriptor_tuple": REJECTED_DESCRIPTORS,
            "disposition": "TERMINAL_REJECTED_NEVER_CONSUME_AS_A_DESCRIPTOR_AUTHORITY",
            "sealed_ledger_bytes_remain_reusable": True,
        },
        "sealed_input_binding": {
            "C69b_producer_file_sha256": PINS["C69B_PRODUCER"],
            "C69b_mathematical_contract_file_sha256": PINS["C69B_CONTRACT"],
            "C69b_mathematical_contract_object_sha256": PINS["C69B_CONTRACT_OBJECT"],
            "C69b_publication_receipt_file_sha256": PINS["C69B_RECEIPT"],
            "C69b_publication_receipt_object_sha256": old_receipt["object_sha256"],
            "authority_snapshot_sha256": PINS["AUTHORITY_SNAPSHOT"],
            "published_ledger_files": {
                name: copy.deepcopy(old_receipt["published_files"][spec["filename"]])
                for name, spec in LEDGER_SPECS.items()
            },
        },
        "repair_algorithm": [
            "AUTHENTICATE_C69B_RECEIPT_RESULT_CONTRACT_PRODUCER_AND_AUTHORITY_SNAPSHOT",
            "READ_EACH_ALREADY_SEALED_GZIP_FILE_BY_STABLE_NOFOLLOW_SINGLE_LINK_FD",
            "VERIFY_RECEIPT_BOUND_FINAL_GZIP_SHA256_AND_SIZE",
            "DECOMPRESS_FINAL_GZIP_BYTES_WITHOUT_IMPORTING_OR_EXECUTING_THE_C69B_PRODUCER",
            "RECOMPUTE_EVERY_CANONICAL_JSON_ROW_SELF_HASH",
            "RECOMPUTE_ROW_COUNT_AND_NEWLINE_DELIMITED_ROW_HASH_SEQUENCE_SHA256",
            "REBUILD_DESCRIPTOR_USING_FINAL_GZIP_SHA256_AND_SIZE",
            "PRESERVE_THE_SEALED_LEDGER_BYTES_EXACTLY_AND_WRITE_NO_LEDGER",
        ],
        "forbidden_operations": {
            "numeric_ledger_recomputation": True,
            "ledger_rewrite_or_copy_as_successor_bytes": True,
            "accept_rejected_C69b_result_tuple": True,
            "runtime_or_canonical_write": True,
            "formal_whole_parent_or_D02_credit": True,
        },
        "publication_protocol": {
            "two_isolated_stages_required": True,
            "all_stage_files_byte_identical_required": True,
            "exclusive_O_EXCL_no_replace_required": True,
            "corrected_result_published_last_among_staged_files": True,
            "publication_receipt_published_after_corrected_result": True,
        },
        "strict_boundary": {
            "candidate_is_installed_authority": False,
            "runtime_or_canonical_written": False,
            "formal_credit": 0,
            "whole_parent_credit": 0,
            "D02_gate_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    need(digest(blobs["C69B_CONTRACT"]) == PINS["C69B_CONTRACT"], "contract-old-math-binding")
    contract["object_sha256"] = digest(contract)
    return contract


def terminal_rejection(contract: dict[str, Any], corrected: dict[str, dict[str, Any]]) -> dict[str, Any]:
    rejection = {
        "schema": SCHEMA + ".terminal-rejection",
        "status": "TERMINAL_REJECTED_C69B_PRE_GZIP_CLOSE_DESCRIPTOR_RESULT_TUPLE__ZERO_CREDIT__NEVER_CONSUME",
        "reason": "C69B_RESULT_RECORDED_ALL_THREE_GZIP_SHA256_AND_SIZE_FIELDS_BEFORE_GZIP_CLOSE; THE_VALUES_DO_NOT_BIND_THE_FINAL_PUBLISHED_BYTES",
        "rejected_tuple": {
            "producer_file_sha256": PINS["C69B_PRODUCER"],
            "result_file_sha256": PINS["C69B_RESULT"],
            "result_object_sha256": PINS["C69B_RESULT_OBJECT"],
            "descriptors": REJECTED_DESCRIPTORS,
        },
        "surviving_sealed_ledgers": corrected,
        "scope": {
            "old_result_tuple_rejected": True,
            "sealed_ledger_bytes_rejected": False,
            "sealed_ledger_bytes_rewritten": False,
            "sealed_ledger_numeric_content_recomputed": False,
        },
        "accepted_successor_protocol": {
            "producer_file_sha256": digest(SELF.read_bytes()),
            "contract_object_sha256": contract["object_sha256"],
            "required_result_schema": SCHEMA + ".corrected-result",
        },
        "authority_snapshot_sha256": PINS["AUTHORITY_SNAPSHOT"],
        "strict_boundary": {
            "runtime_or_canonical_written": False,
            "formal_credit": 0,
            "whole_parent_credit": 0,
            "D02_gate_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    rejection["object_sha256"] = digest(rejection)
    return rejection


def validate_capsule(capsule: dict[str, Any], corrected: dict[str, dict[str, Any]]) -> None:
    need(capsule["old_result_tuple_rejected"] is True, "capsule-old-result-rejection")
    need(capsule["sealed_ledgers_reused"] is True, "capsule-ledger-reuse")
    need(capsule["numeric_recomputation_performed"] is False, "capsule-no-numeric-recompute")
    need(capsule["ledger_bytes_written"] is False, "capsule-no-ledger-write")
    need(capsule["C69b_receipt_file_sha256"] == PINS["C69B_RECEIPT"], "capsule-receipt-file")
    need(capsule["C69b_receipt_object_sha256"] == PINS["C69B_RECEIPT_OBJECT"], "capsule-receipt-object")
    need(capsule["C69b_result_object_sha256"] == PINS["C69B_RESULT_OBJECT"], "capsule-old-result-object")
    need(capsule["authority_snapshot_sha256"] == PINS["AUTHORITY_SNAPSHOT"], "capsule-authority")
    need(capsule["corrected_descriptors"] == corrected, "capsule-corrected-descriptors")
    need(capsule["runtime_or_canonical_written"] is False, "capsule-runtime")
    need(capsule["formal_credit"] == capsule["whole_parent_credit"] == capsule["D02_gate_credit"] == 0, "capsule-zero-credit")


def protocol_self_test(corrected: dict[str, dict[str, Any]]) -> dict[str, Any]:
    capsule = {
        "old_result_tuple_rejected": True,
        "sealed_ledgers_reused": True,
        "numeric_recomputation_performed": False,
        "ledger_bytes_written": False,
        "C69b_receipt_file_sha256": PINS["C69B_RECEIPT"],
        "C69b_receipt_object_sha256": PINS["C69B_RECEIPT_OBJECT"],
        "C69b_result_object_sha256": PINS["C69B_RESULT_OBJECT"],
        "authority_snapshot_sha256": PINS["AUTHORITY_SNAPSHOT"],
        "corrected_descriptors": corrected,
        "runtime_or_canonical_written": False,
        "formal_credit": 0,
        "whole_parent_credit": 0,
        "D02_gate_credit": 0,
    }
    validate_capsule(capsule, corrected)
    mutations: list[tuple[str, tuple[str, ...], Any]] = [
        ("accept-old-result", ("old_result_tuple_rejected",), False),
        ("disable-ledger-reuse", ("sealed_ledgers_reused",), False),
        ("claim-numeric-recompute", ("numeric_recomputation_performed",), True),
        ("claim-ledger-write", ("ledger_bytes_written",), True),
        ("receipt-file-retarget", ("C69b_receipt_file_sha256",), "0" * 64),
        ("receipt-object-retarget", ("C69b_receipt_object_sha256",), "0" * 64),
        ("old-result-object-retarget", ("C69b_result_object_sha256",), "0" * 64),
        ("authority-retarget", ("authority_snapshot_sha256",), "0" * 64),
        ("decision-file-retarget", ("corrected_descriptors", "decisions", "sha256"), "0" * 64),
        ("decision-size-retarget", ("corrected_descriptors", "decisions", "size"), 1),
        ("blocker-row-count-retarget", ("corrected_descriptors", "blockers", "row_count"), 1),
        ("cover-row-sequence-retarget", ("corrected_descriptors", "parametric_newton_covers", "row_hash_line_sequence_sha256"), "0" * 64),
        ("runtime-write", ("runtime_or_canonical_written",), True),
        ("formal-credit", ("formal_credit",), 1),
        ("whole-parent-credit", ("whole_parent_credit",), 1),
        ("D02-credit", ("D02_gate_credit",), 1),
    ]
    attacks: dict[str, str] = {}
    for label, path, replacement in mutations:
        forged = copy.deepcopy(capsule)
        target: Any = forged
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = replacement
        try:
            validate_capsule(forged, corrected)
        except FailClosed:
            attacks[label] = "FAIL_CLOSED"
        else:
            raise FailClosed("protocol-attack-escaped:" + label)
    return {
        "status": f"PASS_{len(attacks)}_OF_{len(mutations)}_EXECUTED_PROTOCOL_ATTACKS_FAIL_CLOSED",
        "attack_count": len(attacks),
        "attacks": attacks,
    }


def corrected_result(
    old_result: dict[str, Any],
    old_receipt: dict[str, Any],
    corrected: dict[str, dict[str, Any]],
    contract: dict[str, Any],
    rejection: dict[str, Any],
    rejection_file_sha256: str,
) -> dict[str, Any]:
    semantic_payload = {key: copy.deepcopy(old_result[key]) for key in SEMANTIC_KEYS}
    result: dict[str, Any] = {
        "schema": SCHEMA + ".corrected-result",
        "status": "PASS_C69B_SEALED_LEDGER_DESCRIPTOR_REPAIR_SUPERSESSION__ZERO_CREDIT",
        "producer_file_sha256": digest(SELF.read_bytes()),
        "contract_file_sha256": None,
        "contract_object_sha256": contract["object_sha256"],
        "terminal_rejection_file_sha256": rejection_file_sha256,
        "terminal_rejection_object_sha256": rejection["object_sha256"],
        "predecessor_binding": {
            "C69b_producer_file_sha256": PINS["C69B_PRODUCER"],
            "C69b_mathematical_contract_file_sha256": PINS["C69B_CONTRACT"],
            "C69b_mathematical_contract_object_sha256": PINS["C69B_CONTRACT_OBJECT"],
            "C69b_result_file_sha256": PINS["C69B_RESULT"],
            "C69b_result_object_sha256": PINS["C69B_RESULT_OBJECT"],
            "C69b_publication_receipt_file_sha256": PINS["C69B_RECEIPT"],
            "C69b_publication_receipt_object_sha256": old_receipt["object_sha256"],
            "C69b_sealed_ledger_file_sha256": {
                name: descriptor["sha256"] for name, descriptor in corrected.items()
            },
            "C69b_result_status": old_result["status"],
            "C69b_semantic_payload_sha256": digest(semantic_payload),
        },
        "repair_scope": {
            "defect": "PRE_GZIP_CLOSE_DESCRIPTOR_SHA256_AND_SIZE_ONLY",
            "old_result_tuple_terminally_rejected": True,
            "sealed_ledgers_reused_in_place": True,
            "sealed_ledger_bytes_rewritten": False,
            "sealed_ledger_numeric_content_recomputed": False,
            "every_actual_gzip_row_self_hash_recomputed": True,
            "every_descriptor_row_count_and_sequence_recomputed": True,
            "actual_final_gzip_sha256_and_size_recomputed": True,
        },
        "ledgers": corrected,
        "predecessor_producer_attacks": copy.deepcopy(old_result["producer_attacks"]),
        "protocol_self_test": protocol_self_test(corrected),
        "authority_snapshot_before_sha256": PINS["AUTHORITY_SNAPSHOT"],
        "authority_snapshot_after_sha256": PINS["AUTHORITY_SNAPSHOT"],
        "strict_boundary": {
            "candidate_is_installed_authority": False,
            "decisions_are_terminal_dispositions": False,
            "runtime_or_canonical_written": False,
            "formal_credit": 0,
            "whole_parent_credit": 0,
            "D02_gate_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": [
            "INDEPENDENT_NO_PRODUCER_COLD_REPLAY_OF_ACTUAL_GZIP_ROWS_AND_CORRECTED_DESCRIPTORS",
            "COHERENT_DESCRIPTOR_RESULT_RECEIPT_AND_FILESYSTEM_ATTACK_AUDIT",
            "CONSUME_ONLY_THE_C69C_CORRECTED_DESCRIPTOR_TUPLE_AFTER_INDEPENDENT_PASS_AND_MANIFEST",
        ],
        **semantic_payload,
    }
    return result


def build_stage(stage: Path) -> dict[str, Any]:
    secure_empty_stage(stage)
    before = authority_snapshot()
    need(before == PINS["AUTHORITY_SNAPSHOT"], "authority-before-stage")
    blobs, old_result, old_receipt, corrected = validate_source()

    contract = mathematical_contract(blobs, old_receipt)
    contract_blob = canonical(contract) + b"\n"
    exclusive(stage / CONTRACT, contract_blob)

    rejection = terminal_rejection(contract, corrected)
    rejection_blob = canonical(rejection) + b"\n"
    exclusive(stage / REJECTION, rejection_blob)

    result = corrected_result(
        old_result,
        old_receipt,
        corrected,
        contract,
        rejection,
        digest(rejection_blob),
    )
    result["contract_file_sha256"] = digest(contract_blob)
    result["object_sha256"] = digest(result)
    result_blob = canonical(result) + b"\n"

    report = (
        "# C69c sealed-ledger descriptor repair supersession v1\n\n"
        f"Status: `{result['status']}`\n\n"
        "C69b's numerical run and its three gzip ledgers are not recomputed or rewritten. "
        "The old result captured each ledger descriptor before gzip close, so all three recorded "
        "`sha256`/`size` pairs are terminally rejected. Filename, order, row count, and row-hash "
        "sequence were unaffected.\n\n"
        "C69c authenticates the C69b deterministic publication receipt and authority snapshot, "
        "then reads the final sealed gzip bytes, validates every canonical JSON row self-hash, "
        "and rebuilds the descriptors from the actual rows and final file bytes.\n\n"
        "Corrected descriptors:\n\n"
        f"- decisions: 2,356 rows, `{corrected['decisions']['sha256']}`, {corrected['decisions']['size']} bytes\n"
        f"- blockers: 18,523 rows, `{corrected['blockers']['sha256']}`, {corrected['blockers']['size']} bytes\n"
        f"- parametric Newton covers: 2 rows, `{corrected['parametric_newton_covers']['sha256']}`, {corrected['parametric_newton_covers']['size']} bytes\n\n"
        f"Rejected C69b result object: `{PINS['C69B_RESULT_OBJECT']}`.\n\n"
        f"Corrected result object: `{result['object_sha256']}`.\n\n"
        "Runtime and canonical authority are unchanged. Formal, whole-parent, and D02 credit remain zero.\n"
    ).encode()
    exclusive(stage / REPORT, report)
    exclusive(stage / RESULT, result_blob)

    need(set(path.name for path in stage.iterdir()) == set(STAGE_NAMES), "stage-file-set")
    after = authority_snapshot()
    need(after == before, "authority-after-stage")
    return result


def read_complete_stage(stage: Path) -> dict[str, bytes]:
    st = os.lstat(stage)
    need(stat.S_ISDIR(st.st_mode) and not stat.S_ISLNK(st.st_mode), "publish-stage-directory")
    need(set(path.name for path in stage.iterdir()) == set(STAGE_NAMES), "publish-stage-file-set")
    data: dict[str, bytes] = {}
    for name in STAGE_NAMES:
        data[name], _ = stable_bytes(stage / name)
    return data


def publish(stage_a: Path, stage_b: Path) -> dict[str, Any]:
    need(stage_a != stage_b, "distinct-stages")
    left = read_complete_stage(stage_a)
    right = read_complete_stage(stage_b)
    for name in STAGE_NAMES:
        need(left[name] == right[name], "two-stage-byte-identity:" + name)

    contract = json_object(left[CONTRACT], "stage-contract")
    rejection = json_object(left[REJECTION], "stage-rejection")
    result = json_object(left[RESULT], "stage-result")
    close_object(contract, contract["object_sha256"], "stage-contract")
    close_object(rejection, rejection["object_sha256"], "stage-rejection")
    close_object(result, result["object_sha256"], "stage-result")
    producer_hash = digest(SELF.read_bytes())
    need(contract["producer_file_sha256"] == rejection["accepted_successor_protocol"]["producer_file_sha256"] == result["producer_file_sha256"] == producer_hash, "stage-producer-binding")
    need(result["contract_file_sha256"] == digest(left[CONTRACT]), "stage-contract-file-binding")
    need(result["contract_object_sha256"] == contract["object_sha256"], "stage-contract-object-binding")
    need(result["terminal_rejection_file_sha256"] == digest(left[REJECTION]), "stage-rejection-file-binding")
    need(result["terminal_rejection_object_sha256"] == rejection["object_sha256"], "stage-rejection-object-binding")

    before = authority_snapshot()
    need(before == PINS["AUTHORITY_SNAPSHOT"], "authority-before-publication")
    targets = [OUT / name for name in STAGE_NAMES] + [OUT / RECEIPT]
    need(all(not os.path.lexists(str(path)) for path in targets), "fresh-publication-targets")
    for name in (CONTRACT, REJECTION, REPORT, RESULT):
        exclusive(OUT / name, left[name])

    after_files = authority_snapshot()
    need(after_files == before, "authority-after-staged-file-publication")
    receipt = {
        "schema": SCHEMA + ".deterministic-two-stage-publication-receipt",
        "status": "PASS_TWO_BYTE_IDENTICAL_STAGES__C69B_SEALED_LEDGERS_REUSED__O_EXCL_NO_REPLACE__ZERO_CREDIT",
        "producer_file_sha256": producer_hash,
        "contract_object_sha256": contract["object_sha256"],
        "terminal_rejection_object_sha256": rejection["object_sha256"],
        "corrected_result_object_sha256": result["object_sha256"],
        "C69b_publication_receipt_file_sha256": PINS["C69B_RECEIPT"],
        "C69b_publication_receipt_object_sha256": PINS["C69B_RECEIPT_OBJECT"],
        "C69b_rejected_result_file_sha256": PINS["C69B_RESULT"],
        "C69b_rejected_result_object_sha256": PINS["C69B_RESULT_OBJECT"],
        "reused_sealed_ledgers": copy.deepcopy(result["ledgers"]),
        "published_files": {
            name: {"sha256": digest(left[name]), "size": len(left[name])}
            for name in STAGE_NAMES
        },
        "stage_1_file_hash_sequence_sha256": sequence_hash(digest(left[name]) for name in STAGE_NAMES),
        "stage_2_file_hash_sequence_sha256": sequence_hash(digest(right[name]) for name in STAGE_NAMES),
        "all_stage_bytes_identical": True,
        "publication_O_EXCL_no_replace": True,
        "corrected_result_published_last_among_staged_files": True,
        "publication_receipt_published_after_corrected_result": True,
        "sealed_ledger_bytes_rewritten": False,
        "sealed_ledger_numeric_content_recomputed": False,
        "authority_snapshot_before_sha256": before,
        "authority_snapshot_after_sha256": authority_snapshot(),
        "runtime_or_canonical_written": False,
        "formal_credit": 0,
        "whole_parent_credit": 0,
        "D02_gate_credit": 0,
    }
    need(receipt["authority_snapshot_after_sha256"] == before, "authority-after-receipt-prewrite")
    receipt["object_sha256"] = digest(receipt)
    receipt_blob = canonical(receipt) + b"\n"
    exclusive(OUT / RECEIPT, receipt_blob)
    need(authority_snapshot() == before, "authority-after-publication")
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--stage", type=Path)
    mode.add_argument("--publish", nargs=2, type=Path)
    args = parser.parse_args()
    if args.stage is not None:
        stage = args.stage.absolute()
        result = build_stage(stage)
        print(
            json.dumps(
                {
                    "status": result["status"],
                    "object_sha256": result["object_sha256"],
                    "protocol_self_test": result["protocol_self_test"]["status"],
                },
                sort_keys=True,
            )
        )
    else:
        assert args.publish is not None
        receipt = publish(args.publish[0].absolute(), args.publish[1].absolute())
        print(json.dumps({"status": receipt["status"], "object_sha256": receipt["object_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FailClosed, OSError, ValueError, KeyError, TypeError, IndexError, gzip.BadGzipFile) as error:
        print(f"FAIL_CLOSED:{type(error).__name__}:{error}", file=sys.stderr)
        raise SystemExit(2)
