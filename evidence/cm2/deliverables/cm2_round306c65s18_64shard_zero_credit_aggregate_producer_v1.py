#!/usr/bin/env python3
"""Build the C65s18 64/64 replacement aggregate without granting credit.

The production entry point has an intentionally narrow first phase: it only
enumerates receipt filenames and checks /proc for the frozen bulk controller.
No receipt, ledger, assignment, or authority file is opened unless receipt IDs
are exactly 00..63 and the controller has exited.  This matters while the
no-replace shard transaction is still active.

The executor, controller, and shard checker are never imported or executed.
Their source is captured as pinned inert bytes and parsed as AST only.  This
aggregate is a deterministic, zero-credit replacement view; an independent
cold numeric replay remains mandatory after publication.
"""

from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
import copy
import errno
from fractions import Fraction
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import sys
import tempfile
from typing import Any, Iterable, Iterator
import zlib


sys.dont_write_bytecode = True
SELF = Path(__file__).absolute()
ROOT = SELF.parent.parent
OUT = SELF.parent

SOURCE_BASE = "cm2_round306c65s18_depth18_64shard"
OUTPUT_BASE = "cm2_round306c65s18_depth18_64shard"
SCHEMA = "cm2.round306c65s18.depth18-64shard.aggregate.v1"
SHARD_SCHEMA = "cm2.round306c65s18.depth18-64shard.v3"
ASSIGNMENT_DOMAIN = "cm2.round306c65s18.depth18-64shard.v2.assignment"
SHARDS = tuple(range(64))
PAIRS = (31, 188, 200, 270, 321, 410, 471, 474, 631, 711, 787, 853)
DISPOSITIONS = ("STRICT_TERMINAL", "COLLISION3_READY", "COLLISION2_HANDOFF")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
RECEIPT_NAME = re.compile(
    rf"{re.escape(SOURCE_BASE)}_shard_(\d+)_receipt_v3\.json\Z"
)
LEDGER_NAME = re.compile(
    rf"{re.escape(SOURCE_BASE)}_shard_(\d+)_leaf_ledger_v3\.jsonl\.gz\Z"
)
CONTROLLER_BASENAME = "cm2_round306c65s18_bulk_execution_controller_v1.py"

LEAF_FILE = OUTPUT_BASE + "_aggregate_leaf_ledger_v1.jsonl.gz"
SOURCE_FILE = OUTPUT_BASE + "_aggregate_source_summary_v1.jsonl.gz"
PARENT_FILE = OUTPUT_BASE + "_aggregate_parent_summary_v1.jsonl.gz"
RESULT_FILE = OUTPUT_BASE + "_aggregate_result_v1.json"
OUTPUT_FILES = (LEAF_FILE, SOURCE_FILE, PARENT_FILE, RESULT_FILE)

CONTRACT = OUT / "cm2_round306c65s18_independent_contract_v2.json"
ASSIGNMENT_RESULT = OUT / (SOURCE_BASE + "_assignment_result_v2.json")
INVENTORY = OUT / (SOURCE_BASE + "_assignment_inventory_v2.jsonl.gz")
AUTHORIZATION = OUT / "cm2_round306c65s18_assignment_authorization_seal_v2.json"
C61_RESULT = OUT / "cm2_round306c61s12_depth12_16shard_aggregate_result_v4.json"
C61_LEAVES = OUT / "cm2_round306c61s12_depth12_16shard_aggregate_leaf_ledger_v4.jsonl.gz"
C61_PARENTS = OUT / "cm2_round306c61s12_depth12_16shard_aggregate_parent_summary_v4.jsonl.gz"
EXECUTOR = OUT / "cm2_round306c65s18_depth18_64shard_executor_v3.py"
CONTROLLER = OUT / CONTROLLER_BASENAME
CHECKER = OUT / "cm2_round306c65s18_bulk_shard_readonly_checker_v1.py"

CANONICAL = OUT / "CM2_LATEST_STATUS.md"
CANONICAL_COMPANION = OUT / "CM2_LATEST_STATUS.sha256"
GLOBAL_HEAD = ROOT / (
    ".cm2-runtime/cm2-global-authority-heads/"
    "predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"
)
GLOBAL_CLAIM = ROOT / (
    ".cm2-runtime/cm2-global-successor-claims/"
    "predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.claim"
)
C53_TOKEN = ROOT / ".cm2-runtime/c53-current-pair-successor-token"
C53_AUDIT_TOKEN = ROOT / ".cm2-runtime/c53-current-pair-successor-audit-token"

AUTHORITY_PATHS = (
    GLOBAL_CLAIM, GLOBAL_HEAD, C53_AUDIT_TOKEN, C53_TOKEN,
    CANONICAL, CANONICAL_COMPANION,
)

PIN = {
    "executor_file": "170df261ed9451fc3ecc1fca5e686c6f6d8eeb3d643126da09f30c634cda22ef",
    "controller_file": "1ee734f4bfca42ef17284e1de7225a5f5b0a88cff5167f0a9d33d7195caf0845",
    "checker_file": "f7e7db5590a52902e3e478b364a92c33e81508f90b52b4fe79f8a2b4cbce644d",
    "contract_file": "e320ac48b1cf3675a3c152d0cb9e6084ba750433722fef716e4a8ab534fab287",
    "contract_object": "5d8a39432c2b02e807c5624ea26f56a12b58f66601ab391b52fee89d0ca604a4",
    "assignment_file": "0306fd12de7d73988a45bac84acf70e4615e8e3aaef7c3c42a66fc39dbef4baa",
    "assignment_object": "c7671985713c8cfd8a496931f1b2686fa545448ce0a434c89e943b178000407f",
    "inventory_file": "e2c4714f1f1a8aa470a393d25ff03aaa3228f08979c30c90fd5f297469d6ad30",
    "authorization_file": "99788b913ee8b900c97e14b6b52d90b0ad83ef2c3fddda6d9f82ab0aacc39ca0",
    "authorization_object": "d1b508a54553b8944b50e926e895b35a589fe6aca3a03440e416571b339ca228",
    "C61_result_file": "06b4146185cb6ef0c8d908d523369008481f7df4e6a05ad5956c001267b07f5e",
    "C61_result_object": "05bcb4301ac74aefd6744db2e633c2479c423fab881b33609bf7234a5537e584",
    "C61_leaf_file": "2656bc4d1b99d37da3733338d85c8d6301621563a400d5db40380078c001b1c2",
    "C61_parent_file": "2206c817f49312c519a720e14bc2e152cde5362ed884cbe83d32349a7ff5bab2",
    "global_claim_file": "3801e452f218e330bc16faed5986146202a7d7026e46924bf7bc00167b05f77b",
    "global_head_file": "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3",
    "C53_audit_token_file": "c3a9a3248b2ec3cb0887b62f4edade7664f73f1746593be1b69897404ae42eba",
    "C53_token_file": "dcad8792bb4bede7f97f9996d10b43497b6286704dbc8f1b8a4170a9e2416846",
    "canonical_file": "922fc5d01918b217556bc3f392c44efcc7c9c6345c881371e6cd34950eb99b57",
    "canonical_companion_file": "57d0c75a2dc774d312fc72a11c66e745cf9b7232531e469490bac492b0a91d6b",
    "authority_snapshot_object": "c9a8b97be4bed2008fa132f49e0d4ac0b384e973707ecdf48b27028b7d7e93cf",
    "effective_checkpoint_object": "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab",
}

EXPECTED_AUTHORITY = {
    "C50d_global_claim": PIN["global_claim_file"],
    "C50d_global_head": PIN["global_head_file"],
    "C53_audit_token": PIN["C53_audit_token_file"],
    "C53_successor_token": PIN["C53_token_file"],
    "CM2_LATEST_STATUS.md": PIN["canonical_file"],
    "CM2_LATEST_STATUS.sha256": PIN["canonical_companion_file"],
}

DESCRIPTOR_KEYS = {
    "filename", "order", "row_count", "row_hash_line_sequence_sha256", "sha256", "size",
}
RECEIPT_KEYS = {
    "schema", "status", "runner_file_sha256", "shard_id", "shard_count",
    "additional_binary_depth", "assignment_contract_file_sha256",
    "assignment_contract_object_sha256", "assignment_authorization_file_sha256",
    "assignment_authorization_object_sha256", "assignment_result_file_sha256",
    "assignment_result_object_sha256", "assignment_inventory_sha256",
    "assignment_preimage_schema", "assignment_formula", "assigned_input_count",
    "ordered_assignment_preimage_sha256_line_sequence_sha256", "input_assignment_rows",
    "route_evaluation_count", "output_disposition_census", "raw_classification_census",
    "output_ledger", "authority_snapshot_before", "authority_snapshot_after",
    "authority_snapshot_object_sha256", "shard_complete",
    "partial_statistics_are_formal_credit", "formal_credit", "whole_parent_credit",
    "D02_gate_credit", "runtime_canonical_pointer_or_seal_writes", "object_sha256",
}
RECEIPT_SOURCE_KEYS = {
    "assignment_preimage_sha256", "source_C61_aggregate_leaf_row_sha256",
    "source_output_row_count", "source_output_row_hash_line_sequence_sha256",
    "source_Kraft_conservation", "source_prefix_free",
}
SHARD_ROW_KEYS = {
    "schema", "shard_id", "assignment_preimage_sha256",
    "source_C61_aggregate_leaf_row_sha256", "source_C61_shard_row_sha256",
    "source_C58_leaf_row_sha256", "source_handoff_ordinal", "C58_source_path",
    "source_path", "path", "additional_depth_from_C61",
    "nominal_additional_depth_from_C58", "pair_index", "parent_volume_fraction",
    "exact_representative_box", "exact_reflected_box", "route_classification",
    "route_witness", "route_method", "disposition", "continuation",
    "local_terminal_credit", "formal_credit", "whole_parent_credit", "D02_gate_credit",
    "row_sha256",
}
CONTINUATION_KEYS = {
    "next_collision_index", "prior_C61_aggregate_leaf_row_sha256",
    "prior_C61_shard_row_sha256", "prior_C61_continuation_object_sha256",
    "prior_C58_leaf_row_sha256", "prior_C58_handoff_object_sha256",
    "collision1_history_row_sha256", "collision1_original_owner",
    "collision1_event_order", "exact_representative_box", "exact_reflected_box",
    "route_classification", "route_witness", "route_method", "continuation_credit",
    "continuation_object_sha256",
}
ASSIGNMENT_ROW_KEYS = {
    "schema", "shard_id", "assignment_preimage_sha256",
    "source_C61_aggregate_leaf_row_sha256", "source_C61_continuation_object_sha256",
    "source_C61_disposition", "source_C61_next_collision_index",
    "source_C61_source_shard_row_sha256", "source_C58_leaf_row_sha256",
    "source_handoff_ordinal", "source_path", "path", "pair_index",
    "parent_volume_fraction", "assignment_credit", "formal_credit",
    "whole_parent_credit", "D02_gate_credit", "row_sha256",
}
C61_ROW_KEYS = {
    "schema", "shard_id", "assignment_preimage_sha256", "source_shard_row_sha256",
    "source_C58_leaf_row_sha256", "source_handoff_ordinal", "source_path", "path",
    "additional_depth_from_C58", "pair_index", "parent_volume_fraction",
    "exact_representative_box", "exact_reflected_box", "route_classification",
    "route_witness", "route_method", "disposition", "continuation",
    "local_terminal_credit", "formal_credit", "whole_parent_credit", "D02_gate_credit",
    "row_sha256",
}
CONTRACT_KEYS = {
    "schema", "status", "source", "selection", "refinement", "assignment",
    "audit_requirements", "formal_credit", "whole_parent_credit", "D02_gate_credit",
    "object_sha256",
}
ASSIGNMENT_RESULT_KEYS = {
    "schema", "status", "C61_source", "independent_contract", "assignment_builder_file_sha256",
    "assignment_domain", "assignment_formula", "assignment_preimage_schema", "shard_count",
    "input_count", "per_shard_input_counts", "assignment_complete",
    "assignment_mutually_exclusive", "inventory",
    "filtered_source_row_sha256_line_sequence_sha256",
    "filtered_continuation_object_sha256_line_sequence_sha256",
    "ordered_preimage_sha256_line_sequence_sha256", "candidate_is_authority",
    "partial_statistics_are_formal_credit", "formal_credit", "whole_parent_credit",
    "D02_gate_credit", "runtime_canonical_pointer_or_seal_writes", "object_sha256",
}
AUTHORIZATION_KEYS = {
    "schema", "status", "contract", "assignment_builder", "assignment_inventory",
    "assignment_result", "assignment", "source", "candidate_is_authority",
    "partial_shards_are_an_aggregate", "formal_credit", "whole_parent_credit",
    "D02_gate_credit", "runtime_canonical_pointer_or_seal_writes", "object_sha256",
}
C61_RESULT_KEYS = {
    "schema", "status", "frozen_inputs", "coverage", "ledgers", "invariants",
    "whole_pairs_closed", "whole_singletons_closed", "whole_singletons_remaining",
    "formal_credit", "whole_parent_credit", "D02_gate_credit",
    "runtime_canonical_pointer_or_seal_writes", "object_sha256",
}
C61_PARENT_ROW_KEYS = {
    "schema", "pair_index", "combined_leaf_count", "strict_terminal_leaf_count",
    "collision3_ready_leaf_count", "collision2_handoff_leaf_count", "path_prefix_free",
    "parent_Kraft_conservation", "whole_pair_terminal", "whole_pair_credit",
    "D02_gate_credit", "row_sha256",
}

C61_PARENT_DESCRIPTOR = {
    "filename": C61_PARENTS.name,
    "order": "PAIR_INDEX_ASCENDING",
    "row_count": 12,
    "row_hash_line_sequence_sha256":
        "48077d4a72d4688083e669994734ea3b3b1d800dd6259c207a8e3dcbf85cd8ba",
    "sha256": PIN["C61_parent_file"],
    "size": 947,
}

C61_LEDGER_TERMINAL = 23997
C61_EARLIER_TERMINAL_CARRY = 3411
C61_FULL_BASE_TERMINAL = 27408
C61_FULL_BASE_C2 = 20879
C61_FULL_BASE_LEAVES = 48287
C65_REPLACEMENT_LEAVES = 358919
C65_REPLACEMENT_TERMINAL = 191664
C65_REPLACEMENT_C3 = 0
C65_REPLACEMENT_C2 = 167255
C65_COMPLETE_LEAVES = 386327
C65_COMPLETE_TERMINAL = 219072


class Reject(RuntimeError):
    """A fail-closed protocol or mathematical rejection."""


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False,
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def close_object(value: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(value)
    need("object_sha256" not in result, "object already closed")
    result["object_sha256"] = digest(result)
    return result


def strict_keys(value: Any, expected: set[str], label: str) -> dict[str, Any]:
    need(type(value) is dict and set(value) == expected, label + " exact key set")
    return value


def strict_json(raw: bytes, label: str, canonical_required: bool = True) -> Any:
    need(bool(raw) and not raw.startswith(b"\xef\xbb\xbf"), label + " nonempty/no BOM")

    def hook(items: list[tuple[str, Any]]) -> dict[str, Any]:
        answer: dict[str, Any] = {}
        for key, value in items:
            need(key not in answer, label + " duplicate key:" + key)
            answer[key] = value
        return answer

    value = json.loads(
        raw.decode("utf-8", "strict"), object_pairs_hook=hook,
        parse_float=lambda token: (_ for _ in ()).throw(Reject(label + " float:" + token)),
        parse_constant=lambda token: (_ for _ in ()).throw(Reject(label + " nonfinite:" + token)),
    )
    if canonical_required:
        need(raw == canonical(value) + b"\n", label + " canonical compact bytes")
    return value


def closed_json(raw: bytes, file_pin: str, object_pin: str, label: str,
                canonical_required: bool = True) -> dict[str, Any]:
    need(hashlib.sha256(raw).hexdigest() == file_pin, label + " file pin")
    # Historical frozen objects are accepted only at their exact file hash.
    # The C65 v2 contract predates compact serialization; its pinned pretty
    # JSON bytes remain strict UTF-8/duplicate-free/nonfinite-free JSON and its
    # semantic object hash is still independently closed below.
    value = strict_json(raw, label, canonical_required=canonical_required)
    need(type(value) is dict and value.get("object_sha256") == object_pin,
         label + " object claim")
    body = copy.deepcopy(value)
    claim = body.pop("object_sha256")
    need(digest(body) == claim, label + " object closure")
    return value


def fraction(value: Any) -> Fraction:
    return Fraction(str(value))


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev, value.st_ino, value.st_mode, value.st_nlink, value.st_size,
        value.st_mtime_ns, value.st_ctime_ns,
    )


def stable_file_identity(path: Path) -> tuple[int, ...]:
    descriptor = os.open(
        path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        state = os.fstat(descriptor)
        current = os.stat(path, follow_symlinks=False)
        need(stat.S_ISREG(state.st_mode) and state.st_nlink == 1 and
             fingerprint(state) == fingerprint(current), "stable file identity:" + str(path))
        return fingerprint(state)
    finally:
        os.close(descriptor)


def exclusive_test_bytes(path: Path, raw: bytes) -> None:
    """No-replace byte helper used only inside isolated synthetic tests."""
    flags = (
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_CLOEXEC", 0) |
        getattr(os, "O_NOFOLLOW", 0)
    )
    descriptor = os.open(path, flags, 0o600)
    try:
        view = memoryview(raw)
        while view:
            written = os.write(descriptor, view)
            need(written > 0, "short synthetic write")
            view = view[written:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def capture(paths: Iterable[Path], maximum_each: int = 1 << 30,
            maximum_total: int = 3 << 30) -> dict[Path, bytes]:
    """Capture regular single-link files through stable O_NOFOLLOW descriptors."""
    ordered = tuple(paths)
    need(len(ordered) == len(set(ordered)), "capture paths unique")
    descriptors: dict[Path, int] = {}
    before: dict[Path, os.stat_result] = {}
    total = 0
    try:
        for path in ordered:
            pre = os.stat(path, follow_symlinks=False)
            need(stat.S_ISREG(pre.st_mode) and pre.st_nlink == 1 and
                 0 < pre.st_size <= maximum_each, "frozen regular single-link:" + str(path))
            descriptor = os.open(
                path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) |
                getattr(os, "O_NOFOLLOW", 0),
            )
            current = os.fstat(descriptor)
            need(fingerprint(pre) == fingerprint(current), "open TOCTOU:" + str(path))
            total += current.st_size
            need(total <= maximum_total, "capture total bound")
            descriptors[path] = descriptor
            before[path] = current
        result: dict[Path, bytes] = {}
        for path in ordered:
            chunks: list[bytes] = []
            while block := os.read(descriptors[path], 4 << 20):
                chunks.append(block)
            result[path] = b"".join(chunks)
            need(len(result[path]) == before[path].st_size, "captured size:" + str(path))
        for path in ordered:
            need(
                fingerprint(before[path]) == fingerprint(os.fstat(descriptors[path])) ==
                fingerprint(os.stat(path, follow_symlinks=False)),
                "read/path TOCTOU:" + str(path),
            )
        return result
    finally:
        for descriptor in descriptors.values():
            os.close(descriptor)


def receipt_names(directory: Path) -> tuple[str, ...]:
    """Only enumerate names; do not stat or open any shard artifact."""
    names: list[str] = []
    with os.scandir(directory) as entries:
        for entry in entries:
            candidate = (entry.name.startswith(SOURCE_BASE + "_shard_") and
                         entry.name.endswith("_receipt_v3.json"))
            if candidate:
                need(RECEIPT_NAME.fullmatch(entry.name) is not None,
                     "malformed v3 receipt filename:" + entry.name)
                names.append(entry.name)
    return tuple(sorted(names))


def receipt_ids(names: Iterable[str]) -> tuple[int, ...]:
    result: list[int] = []
    for name in names:
        match = RECEIPT_NAME.fullmatch(name)
        need(match is not None, "receipt name syntax")
        result.append(int(match.group(1)))
    return tuple(sorted(result))


def ledger_names(directory: Path) -> tuple[str, ...]:
    """Enumerate ledger names only; called only after the receipt/controller gate."""
    names: list[str] = []
    with os.scandir(directory) as entries:
        for entry in entries:
            candidate = (entry.name.startswith(SOURCE_BASE + "_shard_") and
                         entry.name.endswith("_leaf_ledger_v3.jsonl.gz"))
            if candidate:
                need(LEDGER_NAME.fullmatch(entry.name) is not None,
                     "malformed v3 ledger filename:" + entry.name)
                names.append(entry.name)
    return tuple(sorted(names))


def active_controllers(proc_root: Path = Path("/proc")) -> tuple[int, ...]:
    active: list[int] = []
    try:
        processes = tuple(proc_root.iterdir())
    except OSError as exc:
        raise Reject("cannot enumerate process table:" + str(exc)) from exc
    for process in processes:
        if not process.name.isdigit():
            continue
        try:
            raw = (process / "cmdline").read_bytes()
        except OSError as exc:
            if exc.errno in {errno.ENOENT, errno.ESRCH}:
                continue
            raise Reject("cannot inspect process cmdline:" + str(process) + ":" + str(exc)) from exc
        arguments = [part.decode("utf-8", "surrogateescape") for part in raw.split(b"\0") if part]
        if any(Path(argument).name == CONTROLLER_BASENAME for argument in arguments):
            active.append(int(process.name))
    return tuple(sorted(active))


def preflight_gate(directory: Path = OUT, proc_root: Path = Path("/proc")) -> tuple[str, ...]:
    names = receipt_names(directory)
    expected_names = tuple(
        SOURCE_BASE + f"_shard_{shard:02d}_receipt_v3.json" for shard in SHARDS
    )
    need(names == expected_names and receipt_ids(names) == SHARDS,
         f"receipt universe incomplete or non-exact:{len(names)}/64")
    active = active_controllers(proc_root)
    need(not active, "bulk controller active:" + ",".join(map(str, active)))
    return names


def complete_name_gate(directory: Path = OUT, proc_root: Path = Path("/proc")
                      ) -> tuple[tuple[str, ...], tuple[str, ...]]:
    receipts = preflight_gate(directory, proc_root)
    ledgers = ledger_names(directory)
    expected = tuple(SOURCE_BASE + f"_shard_{shard:02d}_leaf_ledger_v3.jsonl.gz"
                     for shard in SHARDS)
    need(ledgers == expected and not active_controllers(proc_root),
         f"ledger universe incomplete/non-exact or controller restarted:{len(ledgers)}/64")
    return receipts, ledgers


def authority_snapshot(raw: dict[Path, bytes]) -> dict[str, str]:
    result = {
        "C50d_global_claim": hashlib.sha256(raw[GLOBAL_CLAIM]).hexdigest(),
        "C50d_global_head": hashlib.sha256(raw[GLOBAL_HEAD]).hexdigest(),
        "C53_audit_token": hashlib.sha256(raw[C53_AUDIT_TOKEN]).hexdigest(),
        "C53_successor_token": hashlib.sha256(raw[C53_TOKEN]).hexdigest(),
        "CM2_LATEST_STATUS.md": hashlib.sha256(raw[CANONICAL]).hexdigest(),
        "CM2_LATEST_STATUS.sha256": hashlib.sha256(raw[CANONICAL_COMPANION]).hexdigest(),
    }
    need(result == EXPECTED_AUTHORITY and digest(result) == PIN["authority_snapshot_object"],
         "authority snapshot exact frozen map")
    head = strict_json(raw[GLOBAL_HEAD], "global head")
    need(type(head) is dict and
         head.get("post_seal_effective_checkpoint_object_sha256") ==
         PIN["effective_checkpoint_object"] and
         head.get("successor_checkpoint_object_sha256") == PIN["effective_checkpoint_object"],
         "global head effective checkpoint")
    return result


def parse_gzip_rows(raw: bytes, descriptor: dict[str, Any], label: str,
                    expected_file_sha: str | None = None,
                    maximum_expanded: int = 768 << 20) -> list[dict[str, Any]]:
    strict_keys(descriptor, DESCRIPTOR_KEYS, label + " descriptor")
    actual_sha = hashlib.sha256(raw).hexdigest()
    need(actual_sha == descriptor["sha256"] and
         (expected_file_sha is None or actual_sha == expected_file_sha) and
         len(raw) == descriptor["size"], label + " descriptor bytes")
    decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
    expanded = decoder.decompress(raw, maximum_expanded + 1)
    need(len(expanded) <= maximum_expanded and not decoder.unconsumed_tail,
         label + " bounded inflate")
    expanded += decoder.flush(maximum_expanded + 1 - len(expanded))
    need(decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail and
         expanded.endswith(b"\n"), label + " one gzip member/newline framed")
    lines = expanded.splitlines(keepends=True)
    need(len(lines) == descriptor["row_count"], label + " row count")
    sequence = hashlib.sha256()
    result: list[dict[str, Any]] = []
    for ordinal, line in enumerate(lines):
        row = strict_json(line, f"{label} row {ordinal}")
        need(type(row) is dict and HEX64.fullmatch(str(row.get("row_sha256"))) is not None,
             label + " row hash shape")
        body = copy.deepcopy(row)
        claim = body.pop("row_sha256")
        need(digest(body) == claim, label + " row closure")
        sequence.update((claim + "\n").encode("ascii"))
        result.append(row)
    need(sequence.hexdigest() == descriptor["row_hash_line_sequence_sha256"],
         label + " row hash sequence")
    return result


def assignment_preimage(source_sha: str, path: str) -> bytes:
    need(HEX64.fullmatch(source_sha) is not None and len(path) == 21 and
         set(path) <= {"0", "1"}, "assignment source/path")
    return canonical({
        "assignment_domain": ASSIGNMENT_DOMAIN,
        "path": path,
        "source_C61_aggregate_leaf_row_sha256": source_sha,
    })


def prefix_free(paths: list[str]) -> bool:
    # In lexicographic order, whenever one binary word is a prefix of any
    # later word, it is also a prefix of its immediate successor.  Checking
    # adjacent words is therefore equivalent to the quadratic all-pairs
    # predicate while keeping the full-parent replacement audit tractable.
    ordered = sorted(paths)
    return all(not later.startswith(first)
               for first, later in zip(ordered, ordered[1:]))


def route_evaluations(source_path: str, leaves: list[str]) -> int:
    nodes: set[str] = set()
    for leaf in leaves:
        need(leaf.startswith(source_path), "route trie source prefix")
        for length in range(len(source_path), len(leaf) + 1):
            nodes.add(leaf[:length])
    return len(nodes)


def row_sequence(rows: Iterable[dict[str, Any]]) -> str:
    sequence = hashlib.sha256()
    for row in rows:
        sequence.update((row["row_sha256"] + "\n").encode("ascii"))
    return sequence.hexdigest()


def validate_programs(raw: dict[Path, bytes]) -> dict[str, Any]:
    expected = {EXECUTOR: PIN["executor_file"], CONTROLLER: PIN["controller_file"],
                CHECKER: PIN["checker_file"]}
    for path, claim in expected.items():
        need(hashlib.sha256(raw[path]).hexdigest() == claim, path.name + " source pin")
        ast.parse(raw[path].decode("utf-8", "strict"), filename=path.name)
        need(path.stem not in sys.modules, path.name + " not imported")
    return {
        "executor_file_sha256": PIN["executor_file"],
        "controller_file_sha256": PIN["controller_file"],
        "checker_file_sha256": PIN["checker_file"],
        "consumed_as_pinned_inert_bytes_and_AST_only": True,
        "imported": False,
        "executed": False,
    }


def receipt_path(shard: int) -> Path:
    return OUT / (SOURCE_BASE + f"_shard_{shard:02d}_receipt_v3.json")


def expected_ledger_path(shard: int) -> Path:
    return OUT / (SOURCE_BASE + f"_shard_{shard:02d}_leaf_ledger_v3.jsonl.gz")


def parse_receipts(first_raw: dict[Path, bytes], authority: dict[str, str] | None = None
                   ) -> list[dict[str, Any]]:
    receipts: list[dict[str, Any]] = []
    receipt_file_hashes: set[str] = set()
    receipt_object_hashes: set[str] = set()
    ledger_hashes: set[str] = set()
    for shard in SHARDS:
        path = receipt_path(shard)
        raw = first_raw[path]
        value = strict_json(raw, f"receipt {shard:02d}")
        strict_keys(value, RECEIPT_KEYS, f"receipt {shard:02d}")
        body = copy.deepcopy(value)
        claim = body.pop("object_sha256")
        need(HEX64.fullmatch(str(claim)) is not None and digest(body) == claim,
             f"receipt {shard:02d} closure")
        strict_keys(value["output_ledger"], DESCRIPTOR_KEYS,
                    f"receipt {shard:02d} output ledger")
        need(
            value["schema"] == SHARD_SCHEMA + ".shard-receipt" and
            value["status"] == "PASS_COMPLETE_NO_REPLACE_DEPTH18_SHARD__ZERO_CREDIT" and
            value["runner_file_sha256"] == PIN["executor_file"] and
            value["shard_id"] == shard and value["shard_count"] == 64 and
            value["additional_binary_depth"] == 6 and
            value["assignment_contract_file_sha256"] == PIN["contract_file"] and
            value["assignment_contract_object_sha256"] == PIN["contract_object"] and
            value["assignment_authorization_file_sha256"] == PIN["authorization_file"] and
            value["assignment_authorization_object_sha256"] == PIN["authorization_object"] and
            value["assignment_result_file_sha256"] == PIN["assignment_file"] and
            value["assignment_result_object_sha256"] == PIN["assignment_object"] and
            value["assignment_inventory_sha256"] == PIN["inventory_file"] and
            value["assignment_formula"] == "int(SHA256(preimage),16)%64" and
            value["shard_complete"] is True and
            value["partial_statistics_are_formal_credit"] is False and
            value["formal_credit"] == value["whole_parent_credit"] ==
            value["D02_gate_credit"] == 0 and
            value["runtime_canonical_pointer_or_seal_writes"] is False and
            value["output_ledger"]["filename"] == expected_ledger_path(shard).name and
            value["output_ledger"]["order"] == "ASSIGNMENT_INVENTORY_ORDER_THEN_PATH",
            f"receipt {shard:02d} frozen protocol",
        )
        for summary in value["input_assignment_rows"]:
            strict_keys(summary, RECEIPT_SOURCE_KEYS, f"receipt {shard:02d} source summary")
        if authority is not None:
            need(value["authority_snapshot_before"] == value["authority_snapshot_after"] ==
                 authority and value["authority_snapshot_object_sha256"] ==
                 PIN["authority_snapshot_object"], f"receipt {shard:02d} authority")
        file_hash = hashlib.sha256(raw).hexdigest()
        need(file_hash not in receipt_file_hashes and claim not in receipt_object_hashes and
             value["output_ledger"]["sha256"] not in ledger_hashes,
             f"receipt {shard:02d} unique receipt/ledger identity")
        receipt_file_hashes.add(file_hash)
        receipt_object_hashes.add(claim)
        ledger_hashes.add(value["output_ledger"]["sha256"])
        receipts.append(value)
    return receipts


def validate_c61_parent_summaries(c61_result: dict[str, Any],
                                  rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    need(c61_result["ledgers"]["parent_summaries"] == C61_PARENT_DESCRIPTOR,
         "C61 parent summary frozen descriptor")
    need(len(rows) == len(PAIRS), "C61 parent summary exact 12 rows")
    totals: Counter[str] = Counter()
    for pair, row in zip(PAIRS, rows, strict=True):
        strict_keys(row, C61_PARENT_ROW_KEYS, "C61 parent summary row")
        body = copy.deepcopy(row)
        claim = body.pop("row_sha256")
        need(
            row["schema"] ==
            "cm2.round306c61s12.depth12-16shard.v1.aggregate-parent-row" and
            row["pair_index"] == pair and digest(body) == claim and
            type(row["combined_leaf_count"]) is int and row["combined_leaf_count"] > 0 and
            type(row["strict_terminal_leaf_count"]) is int and
            row["strict_terminal_leaf_count"] >= 0 and
            type(row["collision3_ready_leaf_count"]) is int and
            row["collision3_ready_leaf_count"] >= 0 and
            type(row["collision2_handoff_leaf_count"]) is int and
            row["collision2_handoff_leaf_count"] >= 0 and
            row["combined_leaf_count"] == row["strict_terminal_leaf_count"] +
            row["collision3_ready_leaf_count"] + row["collision2_handoff_leaf_count"] and
            row["path_prefix_free"] is True and row["parent_Kraft_conservation"] == "1" and
            row["whole_pair_terminal"] is
            (row["collision3_ready_leaf_count"] == row["collision2_handoff_leaf_count"] == 0) and
            row["whole_pair_credit"] == row["D02_gate_credit"] == 0,
            f"C61 parent {pair} schema/closure/census/prefix/Kraft",
        )
        totals["combined"] += row["combined_leaf_count"]
        totals["terminal"] += row["strict_terminal_leaf_count"]
        totals["c3"] += row["collision3_ready_leaf_count"]
        totals["c2"] += row["collision2_handoff_leaf_count"]
    need(
        totals == Counter({"combined": C61_FULL_BASE_LEAVES,
                           "terminal": C61_FULL_BASE_TERMINAL,
                           "c2": C61_FULL_BASE_C2}) and
        c61_result["coverage"]["carried_C57_terminal_leaves"] == 462 and
        c61_result["coverage"]["carried_C58_terminal_leaves"] == 2949 and
        c61_result["coverage"]["disposition_census"] == {
            "STRICT_TERMINAL": C61_LEDGER_TERMINAL,
            "COLLISION3_READY": 0,
            "COLLISION2_HANDOFF": C61_FULL_BASE_C2,
        } and
        c61_result["coverage"]["output_leaf_count"] ==
        C61_LEDGER_TERMINAL + C61_FULL_BASE_C2 and
        c61_result["invariants"]["C57_C58_C61_parent_carry_complete"] is True and
        c61_result["invariants"]["all_12_combined_parents_prefix_free_and_Kraft_one"] is True,
        "C61 full parent base census/carry certificate",
    )
    return rows


def validate_core(raw: dict[Path, bytes]) -> tuple[
    dict[str, Any], list[dict[str, Any]], list[dict[str, Any]],
    list[dict[str, Any]], dict[str, Any]
]:
    contract = closed_json(raw[CONTRACT], PIN["contract_file"], PIN["contract_object"],
                           "contract", canonical_required=False)
    assignment_result = closed_json(raw[ASSIGNMENT_RESULT], PIN["assignment_file"],
                                    PIN["assignment_object"], "assignment result")
    authorization = closed_json(raw[AUTHORIZATION], PIN["authorization_file"],
                                PIN["authorization_object"], "authorization")
    c61_result = closed_json(raw[C61_RESULT], PIN["C61_result_file"],
                            PIN["C61_result_object"], "C61 result")
    strict_keys(contract, CONTRACT_KEYS, "contract")
    strict_keys(assignment_result, ASSIGNMENT_RESULT_KEYS, "assignment result")
    strict_keys(authorization, AUTHORIZATION_KEYS, "authorization")
    strict_keys(c61_result, C61_RESULT_KEYS, "C61 result")
    need(
        contract["selection"]["exact_count"] == assignment_result["input_count"] ==
        authorization["assignment"]["input_count"] == 20879 and
        contract["assignment"]["shard_ids_exactly"] == list(SHARDS) and
        contract["refinement"]["additional_binary_depth"] == 6 and
        contract["source"]["C61_aggregate_result"]["object_sha256"] ==
        PIN["C61_result_object"] and
        assignment_result["shard_count"] == authorization["assignment"]["shard_count"] == 64 and
        assignment_result["assignment_complete"] is True and
        assignment_result["assignment_mutually_exclusive"] is True and
        authorization["assignment"]["complete"] is True and
        authorization["assignment"]["mutually_exclusive"] is True and
        assignment_result["inventory"]["sha256"] == PIN["inventory_file"] and
        c61_result["ledgers"]["aggregate_leaves"]["sha256"] == PIN["C61_leaf_file"] and
        c61_result["ledgers"]["parent_summaries"] == C61_PARENT_DESCRIPTOR and
        all(value[key] == 0 for value in (contract, assignment_result, authorization, c61_result)
            for key in ("formal_credit", "whole_parent_credit", "D02_gate_credit")),
        "frozen core protocol",
    )
    inventory = parse_gzip_rows(
        raw[INVENTORY], assignment_result["inventory"], "assignment inventory",
        PIN["inventory_file"],
    )
    c61_rows = parse_gzip_rows(
        raw[C61_LEAVES], c61_result["ledgers"]["aggregate_leaves"], "C61 leaves",
        PIN["C61_leaf_file"],
    )
    c61_parent_rows = parse_gzip_rows(
        raw[C61_PARENTS], c61_result["ledgers"]["parent_summaries"],
        "C61 parent summaries", PIN["C61_parent_file"],
    )
    need(len(inventory) == 20879 and len(c61_rows) == 44876, "core ledger counts")
    validate_c61_parent_summaries(c61_result, c61_parent_rows)
    return assignment_result, inventory, c61_rows, c61_parent_rows, c61_result


def validate_assignment(assignment_result: dict[str, Any], inventory: list[dict[str, Any]],
                        c61_rows: list[dict[str, Any]]) -> tuple[
                            list[dict[str, Any]], dict[str, dict[str, Any]],
                            dict[str, dict[str, Any]], list[dict[str, Any]]
                        ]:
    c61_by_hash: dict[str, dict[str, Any]] = {}
    selected: list[dict[str, Any]] = []
    carried: list[dict[str, Any]] = []
    filtered_rows = hashlib.sha256()
    filtered_continuations = hashlib.sha256()
    for row in c61_rows:
        strict_keys(row, C61_ROW_KEYS, "C61 aggregate leaf row")
        need(row["schema"] == "cm2.round306c61s12.depth12-16shard.v1.aggregate-leaf-row",
             "C61 row schema")
        need(row["row_sha256"] not in c61_by_hash, "C61 row identity unique")
        c61_by_hash[row["row_sha256"]] = row
        need(row["formal_credit"] == row["whole_parent_credit"] == row["D02_gate_credit"] == 0,
             "C61 row credit lock")
        if row["disposition"] == "COLLISION2_HANDOFF":
            need(
                row["continuation"]["next_collision_index"] == 2 and
                row["additional_depth_from_C58"] == 6 and len(row["path"]) == 21 and
                set(row["path"]) <= {"0", "1"} and
                fraction(row["parent_volume_fraction"]) == Fraction(1, 1 << 21),
                "selected C61 predicate",
            )
            selected.append(row)
            filtered_rows.update((row["row_sha256"] + "\n").encode("ascii"))
            filtered_continuations.update(
                (row["continuation"]["continuation_object_sha256"] + "\n").encode("ascii")
            )
        else:
            need(row["disposition"] == "STRICT_TERMINAL" and row["continuation"] is None and
                 row["local_terminal_credit"] == 1, "C61 carry is strict terminal")
            carried.append(row)
    need(len(selected) == C61_FULL_BASE_C2 and len(carried) == C61_LEDGER_TERMINAL,
         "C61 selected/carry replacement census")
    need(
        filtered_rows.hexdigest() ==
        assignment_result["filtered_source_row_sha256_line_sequence_sha256"] and
        filtered_continuations.hexdigest() ==
        assignment_result["filtered_continuation_object_sha256_line_sequence_sha256"],
        "C61 filtered sequences",
    )

    inventory_by_source: dict[str, dict[str, Any]] = {}
    preimage_sequence = hashlib.sha256()
    per_shard: Counter[int] = Counter()
    for ordinal, (assignment, source) in enumerate(zip(inventory, selected, strict=True)):
        strict_keys(assignment, ASSIGNMENT_ROW_KEYS, "assignment row")
        need(assignment["schema"] == ASSIGNMENT_DOMAIN + "-row", "assignment row schema")
        body = copy.deepcopy(assignment)
        claim = body.pop("row_sha256")
        need(digest(body) == claim, "assignment row closure")
        preimage_sha = hashlib.sha256(
            assignment_preimage(source["row_sha256"], source["path"])
        ).hexdigest()
        shard = int(preimage_sha, 16) % 64
        need(
            assignment["source_C61_aggregate_leaf_row_sha256"] == source["row_sha256"] and
            assignment["source_C61_continuation_object_sha256"] ==
            source["continuation"]["continuation_object_sha256"] and
            assignment["source_C61_source_shard_row_sha256"] ==
            source["source_shard_row_sha256"] and
            assignment["source_C58_leaf_row_sha256"] == source["source_C58_leaf_row_sha256"] and
            assignment["source_handoff_ordinal"] == source["source_handoff_ordinal"] and
            assignment["source_path"] == source["source_path"] and
            assignment["path"] == source["path"] and
            assignment["pair_index"] == source["pair_index"] and
            fraction(assignment["parent_volume_fraction"]) ==
            fraction(source["parent_volume_fraction"]) and
            assignment["source_C61_disposition"] == "COLLISION2_HANDOFF" and
            assignment["source_C61_next_collision_index"] == 2 and
            assignment["assignment_preimage_sha256"] == preimage_sha and
            assignment["shard_id"] == shard and
            assignment["assignment_credit"] == assignment["formal_credit"] ==
            assignment["whole_parent_credit"] == assignment["D02_gate_credit"] == 0 and
            source["row_sha256"] not in inventory_by_source,
            f"assignment/C61 binding {ordinal}",
        )
        inventory_by_source[source["row_sha256"]] = assignment
        preimage_sequence.update((preimage_sha + "\n").encode("ascii"))
        per_shard[shard] += 1
    need(
        len(inventory_by_source) == 20879 and
        preimage_sequence.hexdigest() ==
        assignment_result["ordered_preimage_sha256_line_sequence_sha256"] and
        {str(key): value for key, value in sorted(per_shard.items())} ==
        assignment_result["per_shard_input_counts"],
        "global assignment bijection/order/shard census",
    )
    return selected, c61_by_hash, inventory_by_source, carried


def validate_shard_row(row: dict[str, Any], shard: int, source: dict[str, Any],
                       assignment: dict[str, Any]) -> None:
    strict_keys(row, SHARD_ROW_KEYS, f"shard {shard:02d} row")
    body = copy.deepcopy(row)
    claim = body.pop("row_sha256")
    need(digest(body) == claim, f"shard {shard:02d} row closure")
    path = row["path"]
    depth = row["additional_depth_from_C61"]
    need(
        row["schema"] == SHARD_SCHEMA + ".shard-leaf-row" and row["shard_id"] == shard and
        row["assignment_preimage_sha256"] == assignment["assignment_preimage_sha256"] and
        row["source_C61_aggregate_leaf_row_sha256"] == source["row_sha256"] and
        row["source_C61_shard_row_sha256"] == source["source_shard_row_sha256"] and
        row["source_C58_leaf_row_sha256"] == source["source_C58_leaf_row_sha256"] and
        row["source_handoff_ordinal"] == source["source_handoff_ordinal"] and
        row["C58_source_path"] == source["source_path"] and
        row["source_path"] == source["path"] and
        type(path) is str and path.startswith(source["path"]) and
        type(depth) is int and 0 <= depth <= 6 and len(path) == len(source["path"]) + depth and
        set(path) <= {"0", "1"} and
        row["nominal_additional_depth_from_C58"] ==
        source["additional_depth_from_C58"] + depth and
        row["pair_index"] == source["pair_index"] and
        fraction(row["parent_volume_fraction"]) ==
        fraction(source["parent_volume_fraction"]) / (1 << depth) and
        type(row["route_classification"]) is str and type(row["route_witness"]) is str and
        type(row["route_method"]) is str and row["disposition"] in DISPOSITIONS and
        row["formal_credit"] == row["whole_parent_credit"] == row["D02_gate_credit"] == 0,
        f"shard {shard:02d} row source/path/credit binding",
    )
    continuation = row["continuation"]
    if row["disposition"] == "STRICT_TERMINAL":
        need(continuation is None and row["local_terminal_credit"] == 1,
             f"shard {shard:02d} terminal semantics")
        return
    strict_keys(continuation, CONTINUATION_KEYS, f"shard {shard:02d} continuation")
    continuation_body = copy.deepcopy(continuation)
    continuation_claim = continuation_body.pop("continuation_object_sha256")
    prior = source["continuation"]
    expected_next = 3 if row["disposition"] == "COLLISION3_READY" else 2
    need(
        digest(continuation_body) == continuation_claim and
        continuation["next_collision_index"] == expected_next and
        continuation["prior_C61_aggregate_leaf_row_sha256"] == source["row_sha256"] and
        continuation["prior_C61_shard_row_sha256"] == source["source_shard_row_sha256"] and
        continuation["prior_C61_continuation_object_sha256"] ==
        prior["continuation_object_sha256"] and
        continuation["prior_C58_leaf_row_sha256"] == source["source_C58_leaf_row_sha256"] and
        continuation["prior_C58_handoff_object_sha256"] ==
        prior["prior_C58_handoff_object_sha256"] and
        continuation["collision1_history_row_sha256"] == prior["collision1_history_row_sha256"] and
        continuation["collision1_original_owner"] == prior["collision1_original_owner"] and
        continuation["collision1_event_order"] == prior["collision1_event_order"] and
        continuation["exact_representative_box"] == row["exact_representative_box"] and
        continuation["exact_reflected_box"] == row["exact_reflected_box"] and
        continuation["route_classification"] == row["route_classification"] and
        continuation["route_witness"] == row["route_witness"] and
        continuation["route_method"] == row["route_method"] and
        continuation["continuation_credit"] == 0 and row["local_terminal_credit"] == 0,
        f"shard {shard:02d} continuation closure/lineage",
    )


def aggregate_rows(receipts: list[dict[str, Any]], raw: dict[Path, bytes],
                   selected: list[dict[str, Any]], c61_by_hash: dict[str, dict[str, Any]],
                   inventory: list[dict[str, Any]],
                   inventory_by_source: dict[str, dict[str, Any]]) -> tuple[
                       list[dict[str, Any]], list[dict[str, Any]], dict[str, int],
                       dict[str, int], int
                   ]:
    selected_order = {row["row_sha256"]: ordinal for ordinal, row in enumerate(selected)}
    outputs_by_source: dict[str, list[dict[str, Any]]] = defaultdict(list)
    all_original_rows: list[dict[str, Any]] = []
    raw_total: Counter[str] = Counter()
    disposition_total: Counter[str] = Counter()
    total_routes = 0
    seen_output_hashes: set[str] = set()

    for shard, receipt in zip(SHARDS, receipts, strict=True):
        ledger_path = expected_ledger_path(shard)
        rows = parse_gzip_rows(raw[ledger_path], receipt["output_ledger"],
                               f"shard {shard:02d} ledger")
        assigned = [row for row in inventory if row["shard_id"] == shard]
        need(len(assigned) == receipt["assigned_input_count"],
             f"shard {shard:02d} assigned count")
        assignment_sequence = hashlib.sha256()
        expected_order: list[str] = []
        observed_summaries: list[dict[str, Any]] = []
        shard_dispositions: Counter[str] = Counter()
        shard_raw: Counter[str] = Counter()
        shard_routes = 0
        rows_by_source: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in rows:
            source_hash = row.get("source_C61_aggregate_leaf_row_sha256")
            need(source_hash in c61_by_hash and source_hash in inventory_by_source,
                 f"shard {shard:02d} output known source")
            source = c61_by_hash[source_hash]
            assignment = inventory_by_source[source_hash]
            need(assignment["shard_id"] == shard, f"shard {shard:02d} source exclusivity")
            validate_shard_row(row, shard, source, assignment)
            need(row["row_sha256"] not in seen_output_hashes,
                 f"shard {shard:02d} output identity unique")
            seen_output_hashes.add(row["row_sha256"])
            rows_by_source[source_hash].append(row)
            outputs_by_source[source_hash].append(row)
            all_original_rows.append(row)
            shard_dispositions[row["disposition"]] += 1
            shard_raw[row["route_classification"]] += 1
        need(set(rows_by_source) == {row["source_C61_aggregate_leaf_row_sha256"] for row in assigned},
             f"shard {shard:02d} exact source coverage")
        for assignment in assigned:
            source_hash = assignment["source_C61_aggregate_leaf_row_sha256"]
            source = c61_by_hash[source_hash]
            source_rows = rows_by_source[source_hash]
            paths = [row["path"] for row in source_rows]
            need(paths == sorted(paths) and prefix_free(paths) and
                 sum((fraction(row["parent_volume_fraction"]) for row in source_rows),
                     Fraction(0)) == fraction(source["parent_volume_fraction"]),
                 f"shard {shard:02d} source prefix/Kraft/order")
            assignment_sequence.update(
                (assignment["assignment_preimage_sha256"] + "\n").encode("ascii")
            )
            source_route_count = route_evaluations(source["path"], paths)
            shard_routes += source_route_count
            expected_order.extend(row["row_sha256"] for row in source_rows)
            observed_summaries.append({
                "assignment_preimage_sha256": assignment["assignment_preimage_sha256"],
                "source_C61_aggregate_leaf_row_sha256": source_hash,
                "source_output_row_count": len(source_rows),
                "source_output_row_hash_line_sequence_sha256": row_sequence(source_rows),
                "source_Kraft_conservation": source["parent_volume_fraction"],
                "source_prefix_free": True,
            })
        need(
            expected_order == [row["row_sha256"] for row in rows] and
            assignment_sequence.hexdigest() ==
            receipt["ordered_assignment_preimage_sha256_line_sequence_sha256"] and
            observed_summaries == receipt["input_assignment_rows"] and
            shard_routes == receipt["route_evaluation_count"] and
            {key: shard_dispositions[key] for key in DISPOSITIONS} ==
            receipt["output_disposition_census"] and
            dict(sorted(shard_raw.items())) == receipt["raw_classification_census"],
            f"shard {shard:02d} reconstructed receipt census/order",
        )
        total_routes += shard_routes
        disposition_total.update(shard_dispositions)
        raw_total.update(shard_raw)

    need(set(outputs_by_source) == set(selected_order) and len(outputs_by_source) == 20879,
         "64-shard exact source union")
    ordered_original: list[dict[str, Any]] = []
    source_rows_out: list[dict[str, Any]] = []
    aggregate_rows_out: list[dict[str, Any]] = []
    for ordinal, source in enumerate(selected):
        source_hash = source["row_sha256"]
        assignment = inventory_by_source[source_hash]
        source_outputs = outputs_by_source[source_hash]
        source_outputs.sort(key=lambda row: row["path"])
        ordered_original.extend(source_outputs)
        aggregate_source_rows: list[dict[str, Any]] = []
        for row in source_outputs:
            body = {key: copy.deepcopy(value) for key, value in row.items()
                    if key not in {"schema", "shard_id", "row_sha256"}}
            aggregate_body = {
                "schema": SCHEMA + ".aggregate-leaf-row",
                "source_C65_shard_id": row["shard_id"],
                "source_C65_shard_row_sha256": row["row_sha256"],
                **body,
            }
            aggregate_row = {**aggregate_body, "row_sha256": digest(aggregate_body)}
            aggregate_rows_out.append(aggregate_row)
            aggregate_source_rows.append(aggregate_row)
        counts = Counter(row["disposition"] for row in source_outputs)
        paths = [row["path"] for row in source_outputs]
        source_body = {
            "schema": SCHEMA + ".aggregate-source-row",
            "source_inventory_ordinal": ordinal,
            "source_assignment_row_sha256": assignment["row_sha256"],
            "assignment_preimage_sha256": assignment["assignment_preimage_sha256"],
            "source_C61_aggregate_leaf_row_sha256": source_hash,
            "source_C61_shard_row_sha256": source["source_shard_row_sha256"],
            "source_handoff_ordinal": source["source_handoff_ordinal"],
            "source_path": source["path"],
            "pair_index": source["pair_index"],
            "source_C65_shard_id": assignment["shard_id"],
            "output_leaf_count": len(source_outputs),
            "strict_terminal_leaf_count": counts["STRICT_TERMINAL"],
            "collision3_ready_leaf_count": counts["COLLISION3_READY"],
            "collision2_handoff_leaf_count": counts["COLLISION2_HANDOFF"],
            "route_evaluation_count": route_evaluations(source["path"], paths),
            "source_shard_output_row_hash_line_sequence_sha256": row_sequence(source_outputs),
            "aggregate_output_row_hash_line_sequence_sha256": row_sequence(aggregate_source_rows),
            "path_prefix_free": True,
            "source_Kraft_conservation": source["parent_volume_fraction"],
            "whole_source_terminal": counts["STRICT_TERMINAL"] == len(source_outputs),
            "whole_source_terminal_or_C3_ready": counts["COLLISION2_HANDOFF"] == 0,
            "formal_credit": 0,
            "whole_parent_credit": 0,
            "D02_gate_credit": 0,
        }
        source_rows_out.append({**source_body, "row_sha256": digest(source_body)})
    need(ordered_original == all_original_rows or
         sorted(ordered_original, key=lambda row: (selected_order[row[
             "source_C61_aggregate_leaf_row_sha256"]], row["path"])) == ordered_original,
         "global replacement order reconstructible")
    need(len({row["row_sha256"] for row in aggregate_rows_out}) == len(aggregate_rows_out),
         "aggregate row identities unique")
    return (
        aggregate_rows_out, source_rows_out,
        {key: disposition_total[key] for key in DISPOSITIONS},
        dict(sorted(raw_total.items())), total_routes,
    )


def parent_summaries(base_parents: list[dict[str, Any]], carried: list[dict[str, Any]],
                     selected: list[dict[str, Any]],
                     aggregate_leaves: list[dict[str, Any]],
                     expected_counts: dict[str, int] | None = None) -> list[dict[str, Any]]:
    expected = expected_counts or {
        "ledger_terminal": C61_LEDGER_TERMINAL,
        "earlier_terminal": C61_EARLIER_TERMINAL_CARRY,
        "base_terminal": C61_FULL_BASE_TERMINAL,
        "base_c2": C61_FULL_BASE_C2,
        "replacement": C65_REPLACEMENT_LEAVES,
        "complete": C65_COMPLETE_LEAVES,
        "terminal": C65_COMPLETE_TERMINAL,
        "c3": C65_REPLACEMENT_C3,
        "c2": C65_REPLACEMENT_C2,
    }
    carried_by_pair: dict[int, list[dict[str, Any]]] = defaultdict(list)
    selected_by_pair: Counter[int] = Counter()
    replacements_by_pair: dict[int, list[dict[str, Any]]] = defaultdict(list)
    selected_by_hash: dict[str, dict[str, Any]] = {}
    replacements_by_source: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in carried:
        carried_by_pair[row["pair_index"]].append(row)
    for row in selected:
        selected_by_pair[row["pair_index"]] += 1
        selected_by_hash[row["row_sha256"]] = row
    for row in aggregate_leaves:
        replacements_by_pair[row["pair_index"]].append(row)
        replacements_by_source[row["source_C61_aggregate_leaf_row_sha256"]].append(row)
    need(set(replacements_by_source) == set(selected_by_hash),
         "parent replacement exact selected-source universe")
    for source_hash, source in selected_by_hash.items():
        descendants = replacements_by_source[source_hash]
        paths = [row["path"] for row in descendants]
        need(
            bool(paths) and all(path.startswith(source["path"]) for path in paths) and
            prefix_free(paths) and
            sum((fraction(row["parent_volume_fraction"]) for row in descendants), Fraction(0)) ==
            fraction(source["parent_volume_fraction"]),
            "parent replacement exact descendant prefix/Kraft:" + source_hash,
        )
    result: list[dict[str, Any]] = []
    for pair, base in zip(PAIRS, base_parents, strict=True):
        carry = carried_by_pair[pair]
        replacements = replacements_by_pair[pair]
        replacement_census = Counter(row["disposition"] for row in replacements)
        earlier_carry = base["strict_terminal_leaf_count"] - len(carry)
        need(
            base["pair_index"] == pair and base["path_prefix_free"] is True and
            base["parent_Kraft_conservation"] == "1" and
            base["collision3_ready_leaf_count"] == 0 and
            selected_by_pair[pair] == base["collision2_handoff_leaf_count"] and
            earlier_carry >= 0 and sum(replacement_census.values()) == len(replacements),
            f"pair {pair} full-base replacement certificate",
        )
        combined_count = base["strict_terminal_leaf_count"] + len(replacements)
        strict_count = (base["strict_terminal_leaf_count"] +
                        replacement_census["STRICT_TERMINAL"])
        body = {
            "schema": SCHEMA + ".aggregate-parent-row",
            "pair_index": pair,
            "C61_full_base_parent_row_sha256": base["row_sha256"],
            "C61_full_base_combined_leaf_count": base["combined_leaf_count"],
            "C61_full_base_strict_terminal_leaf_count": base["strict_terminal_leaf_count"],
            "C61_full_base_collision3_ready_leaf_count":
                base["collision3_ready_leaf_count"],
            "C61_full_base_collision2_sources_replaced":
                base["collision2_handoff_leaf_count"],
            "C61_aggregate_ledger_strict_terminal_leaf_count": len(carry),
            "C57_C58_earlier_terminal_carry_leaf_count": earlier_carry,
            "C65_replacement_leaf_count": len(replacements),
            "combined_leaf_count": combined_count,
            "strict_terminal_leaf_count": strict_count,
            "collision3_ready_leaf_count": replacement_census["COLLISION3_READY"],
            "collision2_handoff_leaf_count": replacement_census["COLLISION2_HANDOFF"],
            "path_prefix_free": True,
            "parent_Kraft_conservation": "1",
            "parent_prefix_Kraft_preserved_by_base_certificate_and_exact_source_partitions":
                True,
            "whole_pair_terminal":
                replacement_census["COLLISION3_READY"] ==
                replacement_census["COLLISION2_HANDOFF"] == 0,
            "whole_pair_terminal_or_C3_ready":
                replacement_census["COLLISION2_HANDOFF"] == 0,
            "formal_credit": 0,
            "whole_parent_credit": 0,
            "D02_gate_credit": 0,
        }
        result.append({**body, "row_sha256": digest(body)})
    need(
        len(result) == 12 and
        sum(row["C61_aggregate_ledger_strict_terminal_leaf_count"] for row in result) ==
        expected["ledger_terminal"] and
        sum(row["C57_C58_earlier_terminal_carry_leaf_count"] for row in result) ==
        expected["earlier_terminal"] and
        sum(row["C61_full_base_strict_terminal_leaf_count"] for row in result) ==
        expected["base_terminal"] and
        sum(row["C61_full_base_collision2_sources_replaced"] for row in result) ==
        expected["base_c2"] and
        sum(row["C65_replacement_leaf_count"] for row in result) ==
        expected["replacement"] and
        sum(row["combined_leaf_count"] for row in result) == expected["complete"] and
        sum(row["strict_terminal_leaf_count"] for row in result) == expected["terminal"] and
        sum(row["collision3_ready_leaf_count"] for row in result) == expected["c3"] and
        sum(row["collision2_handoff_leaf_count"] for row in result) == expected["c2"],
        "12 parent summaries full replacement census",
    )
    return result


def write_gzip_rows(path: Path, rows: Iterable[dict[str, Any]], order: str) -> dict[str, Any]:
    flags = (
        os.O_RDWR | os.O_CREAT | os.O_EXCL | getattr(os, "O_CLOEXEC", 0) |
        getattr(os, "O_NOFOLLOW", 0)
    )
    descriptor = os.open(path, flags, 0o600)
    count = 0
    sequence = hashlib.sha256()
    try:
        with os.fdopen(os.dup(descriptor), "wb", closefd=True) as raw_stream:
            with gzip.GzipFile(filename="", mode="wb", fileobj=raw_stream, mtime=0) as stream:
                for row in rows:
                    strict_keys(row, set(row), "output row object")
                    claim = row.get("row_sha256")
                    need(HEX64.fullmatch(str(claim)) is not None, "output row hash shape")
                    body = copy.deepcopy(row)
                    body.pop("row_sha256")
                    need(digest(body) == claim, "output row closure before write")
                    stream.write(canonical(row) + b"\n")
                    sequence.update((claim + "\n").encode("ascii"))
                    count += 1
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    # Descriptor capture deliberately happens only after gzip close and a new open.
    final = capture((path,), maximum_each=1 << 30, maximum_total=1 << 30)[path]
    return {
        "filename": path.name,
        "order": order,
        "row_count": count,
        "row_hash_line_sequence_sha256": sequence.hexdigest(),
        "sha256": hashlib.sha256(final).hexdigest(),
        "size": len(final),
    }


def write_closed_json(path: Path, value: dict[str, Any]) -> None:
    raw = canonical(value) + b"\n"
    flags = (
        os.O_RDWR | os.O_CREAT | os.O_EXCL | getattr(os, "O_CLOEXEC", 0) |
        getattr(os, "O_NOFOLLOW", 0)
    )
    descriptor = os.open(path, flags, 0o600)
    try:
        view = memoryview(raw)
        while view:
            written = os.write(descriptor, view)
            need(written > 0, "short JSON write")
            view = view[written:]
        os.fsync(descriptor)
        os.lseek(descriptor, 0, os.SEEK_SET)
        replay = b""
        while block := os.read(descriptor, 1 << 20):
            replay += block
        need(replay == raw, "JSON fd replay")
    finally:
        os.close(descriptor)


def receipt_vector(receipts: list[dict[str, Any]], raw: dict[Path, bytes]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for shard, receipt in zip(SHARDS, receipts, strict=True):
        result.append({
            "shard_id": shard,
            "receipt_filename": receipt_path(shard).name,
            "receipt_file_sha256": hashlib.sha256(raw[receipt_path(shard)]).hexdigest(),
            "receipt_object_sha256": receipt["object_sha256"],
            "assigned_input_count": receipt["assigned_input_count"],
            "route_evaluation_count": receipt["route_evaluation_count"],
            "output_ledger": copy.deepcopy(receipt["output_ledger"]),
        })
    return result


def build_result(producer_sha: str, independence: dict[str, Any], authority: dict[str, str],
                 receipts: list[dict[str, Any]], raw: dict[Path, bytes],
                 assignment_result: dict[str, Any], c61_result: dict[str, Any],
                 aggregate_leaves: list[dict[str, Any]],
                 source_summaries_rows: list[dict[str, Any]], parent_rows: list[dict[str, Any]],
                 disposition: dict[str, int], raw_census: dict[str, int], routes: int,
                 descriptors: dict[str, dict[str, Any]]) -> dict[str, Any]:
    whole_terminal = sum(row["whole_source_terminal"] for row in source_summaries_rows)
    whole_terminal_or_c3 = sum(
        row["whole_source_terminal_or_C3_ready"] for row in source_summaries_rows
    )
    base_terminal = sum(
        row["C61_full_base_strict_terminal_leaf_count"] for row in parent_rows
    )
    complete = {
        "STRICT_TERMINAL": base_terminal + disposition["STRICT_TERMINAL"],
        "COLLISION3_READY": disposition["COLLISION3_READY"],
        "COLLISION2_HANDOFF": disposition["COLLISION2_HANDOFF"],
    }
    need(
        len(aggregate_leaves) == C65_REPLACEMENT_LEAVES and
        disposition == {
            "STRICT_TERMINAL": C65_REPLACEMENT_TERMINAL,
            "COLLISION3_READY": C65_REPLACEMENT_C3,
            "COLLISION2_HANDOFF": C65_REPLACEMENT_C2,
        } and base_terminal == C61_FULL_BASE_TERMINAL and
        complete == {
            "STRICT_TERMINAL": C65_COMPLETE_TERMINAL,
            "COLLISION3_READY": C65_REPLACEMENT_C3,
            "COLLISION2_HANDOFF": C65_REPLACEMENT_C2,
        } and sum(row["combined_leaf_count"] for row in parent_rows) ==
        C65_COMPLETE_LEAVES,
        "complete C61-base/C65-replacement census",
    )
    value = {
        "schema": SCHEMA + ".aggregate-result",
        "status": "PASS_COMPLETE_64_SHARD_DEPTH18_REPLACEMENT_AGGREGATE__ZERO_CREDIT",
        "producer_file_sha256": producer_sha,
        "producer_independence": independence,
        "frozen_inputs": {
            "contract_file_sha256": PIN["contract_file"],
            "contract_object_sha256": PIN["contract_object"],
            "assignment_result_file_sha256": PIN["assignment_file"],
            "assignment_result_object_sha256": PIN["assignment_object"],
            "assignment_inventory_file_sha256": PIN["inventory_file"],
            "authorization_file_sha256": PIN["authorization_file"],
            "authorization_object_sha256": PIN["authorization_object"],
            "C61_result_file_sha256": PIN["C61_result_file"],
            "C61_result_object_sha256": PIN["C61_result_object"],
            "C61_leaf_ledger_file_sha256": PIN["C61_leaf_file"],
            "C61_full_parent_summary_file_sha256": PIN["C61_parent_file"],
            "C61_full_parent_summary_descriptor":
                copy.deepcopy(c61_result["ledgers"]["parent_summaries"]),
            "assignment_ordered_preimage_sha256_line_sequence_sha256":
                assignment_result["ordered_preimage_sha256_line_sequence_sha256"],
            "post_seal_effective_checkpoint_object_sha256":
                PIN["effective_checkpoint_object"],
            "C69b_consumed": False,
            "C69c_consumed": False,
        },
        "authority_snapshot": {
            "files": authority,
            "object_sha256": PIN["authority_snapshot_object"],
            "post_seal_effective_checkpoint_object_sha256":
                PIN["effective_checkpoint_object"],
        },
        "shard_receipts": receipt_vector(receipts, raw),
        "coverage": {
            "input_C61_selected_collision2_sources": 20879,
            "shard_receipt_count": 64,
            "assignment_complete": True,
            "assignment_mutually_exclusive": True,
            "route_evaluation_count": routes,
            "replacement_output_leaf_count": len(aggregate_leaves),
            "replacement_disposition_census": disposition,
            "raw_classification_census": raw_census,
            "whole_sources_terminal": whole_terminal,
            "whole_sources_terminal_or_C3_ready": whole_terminal_or_c3,
            "C61_aggregate_leaf_ledger_strict_terminal_leaves": C61_LEDGER_TERMINAL,
            "C57_C58_earlier_terminal_carry_leaves": C61_EARLIER_TERMINAL_CARRY,
            "C61_full_base_strict_terminal_leaves": C61_FULL_BASE_TERMINAL,
            "C61_full_base_collision2_sources_replaced": C61_FULL_BASE_C2,
            "C61_full_base_leaf_count": C61_FULL_BASE_LEAVES,
            "complete_parent_leaf_count": C65_COMPLETE_LEAVES,
            "complete_parent_disposition_census": complete,
            "parent_count": 12,
        },
        "ledgers": descriptors,
        "invariants": {
            "receipt_ids_exactly_00_through_63_before_any_ledger_open": True,
            "controller_exited_before_any_receipt_or_ledger_open": True,
            "all_frozen_inputs_single_snapshot_TOCTOU_checked": True,
            "all_64_receipt_and_ledger_descriptors_closed": True,
            "all_20879_assignment_sources_unique_and_exactly_once": True,
            "assignment_formula_and_global_per_shard_sequences_rebuilt": True,
            "all_shard_rows_and_continuation_objects_self_hash_closed": True,
            "all_20879_source_partitions_prefix_free_and_Kraft_conserved": True,
            "C61_full_parent_summary_descriptor_rows_and_object_closure_pinned": True,
            "C57_C58_earlier_terminal_carry_preserved": True,
            "C61_selected_collision2_parents_removed_before_children_inserted": True,
            "C61_parent_and_C65_children_not_double_counted": True,
            "all_12_replacement_parents_preserve_prefix_Kraft_via_C61_base_certificate_and_exact_source_partitions": True,
            "two_isolated_staging_builds_byte_identical": True,
            "gzip_descriptors_computed_after_close_and_reopen": True,
            "publication_no_replace_O_EXCL_O_NOFOLLOW_and_fsync": True,
            "C69b_or_C69c_capability_injected": False,
            "numeric_routes_independently_recomputed_by_this_aggregate_producer": False,
            "post_publication_no_producer_cold_numeric_replay_required": True,
            "partial_statistics_used_for_credit": False,
        },
        "candidate_is_authority": False,
        "formal_credit": 0,
        "whole_parent_credit": 0,
        "D02_gate_credit": 0,
        "runtime_canonical_pointer_or_seal_writes": False,
    }
    return close_object(value)


def stage_build(directory: Path, producer_sha: str, independence: dict[str, Any],
                authority: dict[str, str], receipts: list[dict[str, Any]],
                raw: dict[Path, bytes], assignment_result: dict[str, Any],
                c61_result: dict[str, Any],
                leaves: list[dict[str, Any]], sources: list[dict[str, Any]],
                parents: list[dict[str, Any]], disposition: dict[str, int],
                raw_census: dict[str, int], routes: int) -> dict[str, Any]:
    leaf_descriptor = write_gzip_rows(
        directory / LEAF_FILE, leaves, "C61_V4_FILTERED_C2_ORDER_THEN_CHILD_PATH",
    )
    source_descriptor = write_gzip_rows(
        directory / SOURCE_FILE, sources, "C61_V4_FILTERED_C2_ORDER",
    )
    parent_descriptor = write_gzip_rows(
        directory / PARENT_FILE, parents, "PAIR_INDEX_ASCENDING",
    )
    descriptors = {
        "aggregate_leaves": leaf_descriptor,
        "source_summaries": source_descriptor,
        "parent_summaries": parent_descriptor,
    }
    result = build_result(
        producer_sha, independence, authority, receipts, raw, assignment_result,
        c61_result, leaves, sources, parents, disposition, raw_census, routes, descriptors,
    )
    write_closed_json(directory / RESULT_FILE, result)
    return result


def directory_bytes(directory: Path) -> dict[str, bytes]:
    return {name: capture((directory / name,))[directory / name] for name in OUTPUT_FILES}


def publish_no_replace(source_directory: Path) -> None:
    directory_fd = os.open(OUT, os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_CLOEXEC", 0))
    try:
        for name in OUTPUT_FILES:
            source = capture((source_directory / name,))[source_directory / name]
            flags = (
                os.O_RDWR | os.O_CREAT | os.O_EXCL | getattr(os, "O_CLOEXEC", 0) |
                getattr(os, "O_NOFOLLOW", 0)
            )
            descriptor = os.open(name, flags, 0o644, dir_fd=directory_fd)
            try:
                view = memoryview(source)
                while view:
                    written = os.write(descriptor, view)
                    need(written > 0, "short publication write:" + name)
                    view = view[written:]
                os.fsync(descriptor)
                state = os.fstat(descriptor)
                current = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
                need(stat.S_ISREG(state.st_mode) and state.st_nlink == 1 and
                     fingerprint(state) == fingerprint(current), "publication fd/path:" + name)
                os.lseek(descriptor, 0, os.SEEK_SET)
                replay = b""
                while block := os.read(descriptor, 4 << 20):
                    replay += block
                need(replay == source, "publication byte replay:" + name)
            finally:
                os.close(descriptor)
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)


def production() -> dict[str, Any]:
    # Gate 1: filename enumeration only.  Gate 2: /proc only.  No input file
    # path is opened before both gates pass.
    initial_names, initial_ledger_names = complete_name_gate()

    first_receipt_raw = capture(tuple(receipt_path(shard) for shard in SHARDS))
    preliminary_receipts = parse_receipts(first_receipt_raw)
    ledger_paths = tuple(
        OUT / receipt["output_ledger"]["filename"] for receipt in preliminary_receipts
    )
    need(ledger_paths == tuple(expected_ledger_path(shard) for shard in SHARDS),
         "receipt ledger filenames exact 00..63")

    core_paths = (CONTRACT, ASSIGNMENT_RESULT, INVENTORY, AUTHORIZATION, C61_RESULT,
                  C61_LEAVES, C61_PARENTS, EXECUTOR, CONTROLLER, CHECKER,
                  *AUTHORITY_PATHS)
    all_paths = tuple(receipt_path(shard) for shard in SHARDS) + ledger_paths + core_paths
    raw = capture(all_paths)
    need(all(raw[receipt_path(shard)] == first_receipt_raw[receipt_path(shard)]
             for shard in SHARDS), "receipt bytes stable across full capture")
    need(receipt_names(OUT) == initial_names and ledger_names(OUT) == initial_ledger_names and
         not active_controllers(), "receipt/ledger/controller stable after full capture")

    authority = authority_snapshot(raw)
    receipts = parse_receipts(raw, authority)
    independence = validate_programs(raw)
    assignment_result, inventory, c61_rows, c61_parent_rows, c61_result = validate_core(raw)
    selected, c61_by_hash, inventory_by_source, carried = validate_assignment(
        assignment_result, inventory, c61_rows,
    )
    leaves, sources, disposition, raw_census, routes = aggregate_rows(
        receipts, raw, selected, c61_by_hash, inventory, inventory_by_source,
    )
    parents = parent_summaries(c61_parent_rows, carried, selected, leaves)

    need(all(not os.path.lexists(OUT / name) for name in OUTPUT_FILES),
         "aggregate output no-replace preflight")
    # SELF is not in the shard/core snapshot because it is not a frozen input;
    # capture it now with the same single-link protocol and then hold its hash.
    producer_identity = stable_file_identity(SELF)
    producer_bytes = capture((SELF,))[SELF]
    need(stable_file_identity(SELF) == producer_identity, "producer identity at capture")
    producer_sha = hashlib.sha256(producer_bytes).hexdigest()
    with tempfile.TemporaryDirectory(prefix="cm2-c65-aggregate-stage-a-", dir=OUT) as stage_a_raw, \
         tempfile.TemporaryDirectory(prefix="cm2-c65-aggregate-stage-b-", dir=OUT) as stage_b_raw:
        stage_a = Path(stage_a_raw)
        stage_b = Path(stage_b_raw)
        result_a = stage_build(
            stage_a, producer_sha, independence, authority, receipts, raw, assignment_result,
            c61_result, leaves, sources, parents, disposition, raw_census, routes,
        )
        result_b = stage_build(
            stage_b, producer_sha, independence, authority, receipts, raw, assignment_result,
            c61_result, leaves, sources, parents, disposition, raw_census, routes,
        )
        need(directory_bytes(stage_a) == directory_bytes(stage_b),
             "two-stage deterministic byte identity")

        # Full byte recapture immediately before publication.  Any changed
        # receipt, ledger, core input, program, authority file, process state,
        # or producer source aborts without creating a formal output.
        final_raw = capture(all_paths)
        need(final_raw == raw and capture((SELF,))[SELF] == producer_bytes and
             stable_file_identity(SELF) == producer_identity and
             receipt_names(OUT) == initial_names and ledger_names(OUT) == initial_ledger_names and
             not active_controllers() and
             authority_snapshot(final_raw) == authority,
             "final frozen input/controller/authority replay")
        publish_no_replace(stage_a)
        published = {name: capture((OUT / name,))[OUT / name] for name in OUTPUT_FILES}
        need(published == directory_bytes(stage_a), "post-publication terminal-byte replay")
        need(capture((SELF,))[SELF] == producer_bytes and
             stable_file_identity(SELF) == producer_identity,
             "producer identity/bytes stable after publication")
        return {
            "status": result_a["status"],
            "aggregate_result_object_sha256": result_a["object_sha256"],
            "published_artifacts": {
                name: {"sha256": hashlib.sha256(published[name]).hexdigest(),
                       "size": len(published[name])}
                for name in OUTPUT_FILES
            },
            "formal_credit": 0,
            "whole_parent_credit": 0,
            "D02_gate_credit": 0,
        }


def self_test() -> dict[str, Any]:
    tests: dict[str, bool] = {}
    with tempfile.TemporaryDirectory(prefix="cm2-c65-aggregate-selftest-") as temporary:
        root = Path(temporary)
        receipts_dir = root / "receipts"
        proc_dir = root / "proc"
        receipts_dir.mkdir()
        proc_dir.mkdir()
        for shard in range(63):
            (receipts_dir / (SOURCE_BASE + f"_shard_{shard:02d}_receipt_v3.json")).touch()
        # A ledger FIFO proves the 63-receipt preflight does not open ledgers.
        os.mkfifo(receipts_dir / (SOURCE_BASE + "_shard_00_leaf_ledger_v3.jsonl.gz"))
        try:
            preflight_gate(receipts_dir, proc_dir)
        except Reject:
            tests["63_receipts_rejected_before_ledger_open"] = True
        (receipts_dir / (SOURCE_BASE + "_shard_63_receipt_v3.json")).touch()
        process = proc_dir / "123"
        process.mkdir()
        exclusive_test_bytes(
            process / "cmdline",
            b"python\0/tmp/" + CONTROLLER_BASENAME.encode("ascii") + b"\0--first\00\0",
        )
        try:
            preflight_gate(receipts_dir, proc_dir)
        except Reject:
            tests["active_controller_rejected_after_exact_receipt_enumeration"] = True
        shutil.rmtree(process)
        need(len(preflight_gate(receipts_dir, proc_dir)) == 64, "synthetic exact64 gate")
        tests["exact_64_controller_absent_passes_preflight"] = True
        try:
            complete_name_gate(receipts_dir, proc_dir)
        except Reject:
            tests["incomplete_ledger_universe_rejected_without_open"] = True
        (receipts_dir / (SOURCE_BASE + "_shard_64_receipt_v3.json")).touch()
        try:
            preflight_gate(receipts_dir, proc_dir)
        except Reject:
            tests["65_receipts_rejected"] = True

        rows = []
        for path, value in (("0", "1/2"), ("1", "1/2")):
            body = {"schema": "synthetic.row", "path": path,
                    "parent_volume_fraction": value, "formal_credit": 0}
            rows.append({**body, "row_sha256": digest(body)})
        stage_a = root / "a"
        stage_b = root / "b"
        stage_a.mkdir()
        stage_b.mkdir()
        descriptor_a = write_gzip_rows(stage_a / "rows.jsonl.gz", rows, "PATH")
        descriptor_b = write_gzip_rows(stage_b / "rows.jsonl.gz", rows, "PATH")
        need((stage_a / "rows.jsonl.gz").read_bytes() ==
             (stage_b / "rows.jsonl.gz").read_bytes() and descriptor_a == descriptor_b,
             "synthetic deterministic gzip")
        tests["gzip_two_stage_byte_identical"] = True
        tests["descriptor_after_close_reopen"] = (
            descriptor_a["sha256"] ==
            hashlib.sha256((stage_a / "rows.jsonl.gz").read_bytes()).hexdigest()
        )
        tests["prefix_free_Kraft_and_route_trie"] = (
            prefix_free(["0", "1"]) and
            sum((fraction(row["parent_volume_fraction"]) for row in rows), Fraction(0)) == 1 and
            route_evaluations("", ["0", "1"]) == 3
        )
        synthetic_carry = [
            {"pair_index": pair, "path": "00", "parent_volume_fraction": "1/4"}
            for pair in PAIRS
        ]
        synthetic_selected = [
            {"pair_index": pair, "path": "1", "parent_volume_fraction": "1/2",
             "row_sha256": digest({"synthetic_source_pair": pair})}
            for pair in PAIRS
        ]
        synthetic_children = [
            {"pair_index": pair, "path": path, "parent_volume_fraction": "1/4",
             "disposition": disposition,
             "source_C61_aggregate_leaf_row_sha256": source["row_sha256"]}
            for pair, source in zip(PAIRS, synthetic_selected, strict=True)
            for path, disposition in (("10", "STRICT_TERMINAL"),
                                      ("11", "COLLISION2_HANDOFF"))
        ]
        synthetic_base_parents = []
        for pair in PAIRS:
            base_body = {
                "schema": "synthetic.C61-full-parent-row",
                "pair_index": pair,
                "combined_leaf_count": 3,
                "strict_terminal_leaf_count": 2,
                "collision3_ready_leaf_count": 0,
                "collision2_handoff_leaf_count": 1,
                "path_prefix_free": True,
                "parent_Kraft_conservation": "1",
            }
            synthetic_base_parents.append(
                {**base_body, "row_sha256": digest(base_body)}
            )
        synthetic_parents = parent_summaries(
            synthetic_base_parents, synthetic_carry, synthetic_selected, synthetic_children,
            {
                "ledger_terminal": 12, "earlier_terminal": 12,
                "base_terminal": 24, "base_c2": 12, "replacement": 24,
                "complete": 48, "terminal": 36, "c3": 0, "c2": 12,
            },
        )
        tests["parent_replacement_preserves_omitted_earlier_carry_without_double_count"] = all(
            row["C61_full_base_strict_terminal_leaf_count"] == 2 and
            row["C61_aggregate_ledger_strict_terminal_leaf_count"] == 1 and
            row["C57_C58_earlier_terminal_carry_leaf_count"] == 1 and
            row["C61_full_base_collision2_sources_replaced"] == 1 and
            row["C65_replacement_leaf_count"] == 2 and row["combined_leaf_count"] == 4 and
            row["strict_terminal_leaf_count"] == 3 and
            row["collision2_handoff_leaf_count"] == 1 and
            row["parent_Kraft_conservation"] == "1" and
            row["parent_prefix_Kraft_preserved_by_base_certificate_and_exact_source_partitions"]
            is True
            for row in synthetic_parents
        )
        for name, malformed in (
            ("duplicate_key", b'{"a":1,"a":2}\n'),
            ("NaN", b'{"a":NaN}\n'),
            ("BOM", b'\xef\xbb\xbf{"a":1}\n'),
            ("noncanonical", b'{"b":2, "a":1}\n'),
            ("trailing", b'{"a":1}\nX'),
            ("missing_newline", b'{"a":1}'),
            ("extra_newline", b'{"a":1}\n\n'),
            ("float", b'{"a":64.0}\n'),
        ):
            try:
                strict_json(malformed, "synthetic " + name)
            except (Reject, ValueError, UnicodeError):
                tests[name + "_rejected"] = True

        publish_source = root / "publish-source"
        publish_target = root / "publish-target"
        publish_source.mkdir()
        publish_target.mkdir()
        exclusive_test_bytes(publish_source / "x", b"sealed\n")
        target_fd = os.open(publish_target, os.O_RDONLY | os.O_DIRECTORY)
        try:
            flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
            fd = os.open("x", flags, 0o600, dir_fd=target_fd)
            os.write(fd, b"sealed\n")
            os.fsync(fd)
            os.close(fd)
            try:
                os.open("x", flags, 0o600, dir_fd=target_fd)
            except FileExistsError:
                tests["no_replace_second_publish_rejected"] = True
            need((publish_target / "x").read_bytes() == b"sealed\n",
                 "no-replace preserved bytes")
        finally:
            os.close(target_fd)

    source = capture((SELF,))[SELF].decode("utf-8", "strict")
    tree = ast.parse(source, filename=SELF.name)
    imported = {
        alias.name for node in ast.walk(tree) if isinstance(node, ast.Import)
        for alias in node.names
    } | {
        (node.module or "") for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)
    }
    tests["no_executor_controller_checker_import"] = not any(
        name in " ".join(imported) for name in ("executor_v3", "controller_v1", "checker_v1")
    )
    tests["production_output_absent_during_selftest"] = all(
        not os.path.lexists(OUT / name) for name in OUTPUT_FILES
    )
    need(len(tests) == 20 and all(tests.values()), "20/20 synthetic/static self-tests")
    return close_object({
        "schema": SCHEMA + ".synthetic-static-self-test",
        "status": "PASS_20_OF_20_SYNTHETIC_STATIC_FAIL_CLOSED_TESTS__NO_FORMAL_PUBLICATION",
        "tests": tests,
        "test_count": len(tests),
        "synthetic_is_authority": False,
        "formal_credit": 0,
        "whole_parent_credit": 0,
        "D02_gate_credit": 0,
        "runtime_canonical_pointer_or_seal_writes": False,
    })


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--aggregate", action="store_true")
    group.add_argument("--preflight", action="store_true")
    group.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        if args.preflight:
            names = preflight_gate()
            value: dict[str, Any] = {
                "status": "PASS_EXACT_64_RECEIPTS_AND_CONTROLLER_EXITED__NO_LEDGER_OPENED",
                "receipt_count": len(names), "formal_credit": 0,
            }
        elif args.self_test:
            value = self_test()
        else:
            value = production()
        print(json.dumps(value, sort_keys=True, separators=(",", ":")))
        return 0
    except (Reject, FileExistsError, OSError, KeyError, TypeError, ValueError,
            UnicodeError, zlib.error) as exc:
        print(json.dumps({"status": "FAIL_CLOSED", "reason": str(exc)},
                         sort_keys=True, separators=(",", ":")))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
