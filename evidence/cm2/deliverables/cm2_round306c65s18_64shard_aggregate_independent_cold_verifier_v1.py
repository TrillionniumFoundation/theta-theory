#!/usr/bin/env python3
"""Independent cold verifier for the complete C65s18 64-shard aggregate.

This program is intentionally not a shard or aggregate producer.  It never
imports or executes the C65 executor, controller, checker, or aggregate
producer.  Those programs are captured as inert bytes (and, where useful,
parsed as inert AST).  Numerical routing is reconstructed from the frozen C40
context through the independently frozen C41 auditor kernel.

The production entry point has a deliberately early completeness barrier: it
enumerates only v3 receipt names first.  Unless the exact set 00..63 exists it
fails before deriving, opening, or reading any shard ledger path.
"""

from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
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
from types import ModuleType
from typing import Any, Callable, Iterable, Iterator
import zlib


sys.dont_write_bytecode = True
SELF = Path(__file__).absolute()
OUT = SELF.parent
ROOT = OUT.parent
sys.path.insert(0, str(OUT))
C41_AUDITOR = OUT / "cm2_round306c41_d02_lower_strata_depth3_closure_independent_auditor_v1.py"
C41_MODULE = C41_AUDITOR.stem
C40_AUDITOR = OUT / "cm2_round306c40_d02_h1_endpoint_collision2_arrangement_independent_auditor_v1.py"
C39_KERNEL = OUT / "cm2_round306c39_d02_h1_c1_graph_cell_router_v1.py"
ROUND139 = OUT / "cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier.py"
ROUND166 = OUT / "cm2_round166_multi_candidate_refinement_prototype.py"
ROUND185 = OUT / "cm2_round185_preconditioned_c1_residual_refinement.py"
ROUND181 = OUT / "cm2_round181_parametric_collision2_graph_arrangement.py"
ROUND178 = OUT / "cm2_round178_later_return_exact_key_bridge.py"
_KERNEL: Any | None = None


SCHEMA = "cm2.round306c65s18.64shard-aggregate-independent-cold-verifier.v1"
CORE_SCHEMA = "cm2.round306c65s18.depth18-64shard.v3"
AGG_SCHEMA = "cm2.round306c65s18.depth18-64shard.aggregate.v1"
AGG_RESULT_SCHEMA = AGG_SCHEMA + ".aggregate-result"
AGG_STATUS = "PASS_COMPLETE_64_SHARD_DEPTH18_REPLACEMENT_AGGREGATE__ZERO_CREDIT"
DOMAIN = "cm2.round306c65s18.depth18-64shard.v2.assignment"
SHARDS = tuple(range(64))
PAIRS = (31, 188, 200, 270, 321, 410, 471, 474, 631, 711, 787, 853)
ADDITIONAL_DEPTH = 6
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
RECEIPT_RE = re.compile(
    r"cm2_round306c65s18_depth18_64shard_shard_(\d{2})_receipt_v3\.json\Z"
)
SHARD_LEDGER_RE = re.compile(
    r"cm2_round306c65s18_depth18_64shard_shard_(\d{2})_leaf_ledger_v3\.jsonl\.gz\Z"
)

EXECUTOR = OUT / "cm2_round306c65s18_depth18_64shard_executor_v3.py"
CONTROLLER = OUT / "cm2_round306c65s18_bulk_execution_controller_v1.py"
CHECKER = OUT / "cm2_round306c65s18_bulk_shard_readonly_checker_v1.py"
AGG_PRODUCER = OUT / "cm2_round306c65s18_64shard_zero_credit_aggregate_producer_v1.py"
CONTRACT = OUT / "cm2_round306c65s18_independent_contract_v2.json"
ASSIGNMENT = OUT / "cm2_round306c65s18_depth18_64shard_assignment_result_v2.json"
INVENTORY = OUT / "cm2_round306c65s18_depth18_64shard_assignment_inventory_v2.jsonl.gz"
AUTHORIZATION = OUT / "cm2_round306c65s18_assignment_authorization_seal_v2.json"
C61_RESULT = OUT / "cm2_round306c61s12_depth12_16shard_aggregate_result_v4.json"
C61_LEAVES = OUT / "cm2_round306c61s12_depth12_16shard_aggregate_leaf_ledger_v4.jsonl.gz"
C58_RESULT = OUT / "cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement_result_v1.json"
C58_LEAVES = OUT / "cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement_leaf_ledger_v1.jsonl.gz"
C40 = ROOT / ".cm2-runtime/candidates/c40-h1-endpoint-c2-arrangement-20260810T234000Z-c2f144e29bc1172f"
C40_RESULT = C40 / "result.json"
C40_ROUTED = C40 / "routed_leaf_cells.jsonl.gz"

AGG_RESULT = OUT / "cm2_round306c65s18_depth18_64shard_aggregate_result_v1.json"
AGG_LEAVES = OUT / "cm2_round306c65s18_depth18_64shard_aggregate_leaf_ledger_v1.jsonl.gz"
AGG_SOURCES = OUT / "cm2_round306c65s18_depth18_64shard_aggregate_source_summary_v1.jsonl.gz"
AGG_PARENTS = OUT / "cm2_round306c65s18_depth18_64shard_aggregate_parent_summary_v1.jsonl.gz"

CANONICAL = OUT / "CM2_LATEST_STATUS.md"
CANONICAL_COMPANION = OUT / "CM2_LATEST_STATUS.sha256"
GLOBAL_HEAD = ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"
GLOBAL_CLAIM = ROOT / ".cm2-runtime/cm2-global-successor-claims/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.claim"
C53_TOKEN = ROOT / ".cm2-runtime/c53-current-pair-successor-token"
C53_AUDIT_TOKEN = ROOT / ".cm2-runtime/c53-current-pair-successor-audit-token"

VERIFY_OUT = OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_verification_v1.json"
SELFTEST_OUT = OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_self_test_v2.json"
REJECTED_SELFTEST_V1 = OUT / (
    "cm2_round306c65s18_64shard_aggregate_independent_cold_self_test_v1.json"
)
REJECTED_SELFTEST_V1_MARKER = OUT / (
    "cm2_round306c65s18_64shard_aggregate_independent_cold_self_test_v1_"
    "REJECTED_PRE_CLOSE_SOURCE_DRIFT.md"
)
REPLAY_OUT = OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_postpublication_replay_v1.json"
MANIFEST_OUT = OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_manifest_v1.sha256"
COLD_RUN_A = OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_seed1_projection_v1.json"
COLD_RUN_A_RECEIPT = OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_seed1_receipt_v1.json"
COLD_RUN_B = OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_seed2_projection_v1.json"
COLD_RUN_B_RECEIPT = OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_seed2_receipt_v1.json"

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
    "C58_result_file": "ed4eb1e5ea64c61e4b85a710c1429a2f0b489048320badd4d9a8214bc38c05bc",
    "C58_result_object": "038503bd21505dacde4ce6dc59a320fa70a97cc0dccce33be210c60bbd7d0a30",
    "C58_leaf_file": "15a5b1c5c15f8528591bd80be040317590dadec70b4476d01eb3763ae64965df",
    "C40_result_file": "f721b08a4addb7c0369b27ea3af8546c9fad293b1a7808d015bbf783b3aa22d6",
    "C40_object": "397eda962e4bd20429d7cab1ffc53d82cccfdf59bdce8cd03b271a8ded0536ba",
    "C40_routed_file": "175293702adf1b76600321c1db326a1a6744dbc8caea439ddaeff9779d1f9b5a",
    "C41_independent_auditor_file": "537f3dea94c3743235df8984ba4922d37f82999ff3d8abbac59e5171ef38b74c",
    "C40_independent_auditor_file": "1cccec33cf7768b5797ca0b05f74812a300fb4b323859a10e9495f3e73d8a0be",
    "C39_kernel_file": "873a84cb150efc5649ffb5822457c510ab45c32f3e16a48914c8674dc93c0aae",
    "Round139_file": "462ffcb41ba24771ce655ddb3ad5f18d5a22c8d0cb443ec1791ea9272d3d512b",
    "Round166_file": "6479a78249a717169dea55ecabae98c05f240ea323fa0370037d43339158ae7c",
    "Round185_file": "7b48f3ee3417fcfdf5ef6c852e0ab591eb849b357e704e46ee3aaa259d20acc2",
    "Round181_file": "6e9d51229c209caacf3964d24600295375bd08e963b4e154774625707aa1524c",
    "Round178_file": "06075baac268e8e6c9deeeedae3e502b3a96630f3650c0b783c2b2a77dbd23f9",
    "canonical_file": "922fc5d01918b217556bc3f392c44efcc7c9c6345c881371e6cd34950eb99b57",
    "canonical_companion_file": "57d0c75a2dc774d312fc72a11c66e745cf9b7232531e469490bac492b0a91d6b",
    "global_head_file": "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3",
    "global_claim_file": "3801e452f218e330bc16faed5986146202a7d7026e46924bf7bc00167b05f77b",
    "C53_token_file": "dcad8792bb4bede7f97f9996d10b43497b6286704dbc8f1b8a4170a9e2416846",
    "C53_audit_token_file": "c3a9a3248b2ec3cb0887b62f4edade7664f73f1746593be1b69897404ae42eba",
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
    "filename", "order", "row_count", "row_hash_line_sequence_sha256", "sha256", "size"
}
RECEIPT_KEYS = {
    "D02_gate_credit", "additional_binary_depth", "assigned_input_count",
    "assignment_authorization_file_sha256", "assignment_authorization_object_sha256",
    "assignment_contract_file_sha256", "assignment_contract_object_sha256",
    "assignment_formula", "assignment_inventory_sha256", "assignment_preimage_schema",
    "assignment_result_file_sha256", "assignment_result_object_sha256",
    "authority_snapshot_after", "authority_snapshot_before", "authority_snapshot_object_sha256",
    "formal_credit", "input_assignment_rows", "object_sha256",
    "ordered_assignment_preimage_sha256_line_sequence_sha256", "output_disposition_census",
    "output_ledger", "partial_statistics_are_formal_credit", "raw_classification_census",
    "route_evaluation_count", "runner_file_sha256", "runtime_canonical_pointer_or_seal_writes",
    "schema", "shard_complete", "shard_count", "shard_id", "status", "whole_parent_credit",
}
SHARD_ROW_KEYS = {
    "C58_source_path", "D02_gate_credit", "additional_depth_from_C61",
    "assignment_preimage_sha256", "continuation", "disposition", "exact_reflected_box",
    "exact_representative_box", "formal_credit", "local_terminal_credit",
    "nominal_additional_depth_from_C58", "pair_index", "parent_volume_fraction", "path",
    "route_classification", "route_method", "route_witness", "row_sha256", "schema",
    "shard_id", "source_C58_leaf_row_sha256", "source_C61_aggregate_leaf_row_sha256",
    "source_C61_shard_row_sha256", "source_handoff_ordinal", "source_path",
    "whole_parent_credit",
}
AGG_LEAF_KEYS = (SHARD_ROW_KEYS - {"schema", "shard_id", "row_sha256"}) | {
    "schema", "source_C65_shard_id", "source_C65_shard_row_sha256", "row_sha256"
}
AGG_SOURCE_KEYS = {
    "schema", "source_inventory_ordinal", "source_assignment_row_sha256",
    "assignment_preimage_sha256", "source_C61_aggregate_leaf_row_sha256",
    "source_C61_shard_row_sha256", "source_handoff_ordinal", "source_path", "pair_index",
    "source_C65_shard_id", "output_leaf_count", "strict_terminal_leaf_count",
    "collision3_ready_leaf_count", "collision2_handoff_leaf_count", "route_evaluation_count",
    "source_shard_output_row_hash_line_sequence_sha256",
    "aggregate_output_row_hash_line_sequence_sha256", "path_prefix_free",
    "source_Kraft_conservation", "whole_source_terminal", "whole_source_terminal_or_C3_ready",
    "formal_credit", "whole_parent_credit", "D02_gate_credit", "row_sha256",
}
AGG_PARENT_KEYS = {
    "schema", "pair_index", "C61_carried_strict_terminal_leaf_count",
    "C61_selected_collision2_sources_replaced", "C65_replacement_leaf_count",
    "combined_leaf_count", "strict_terminal_leaf_count", "collision3_ready_leaf_count",
    "collision2_handoff_leaf_count", "path_prefix_free", "parent_Kraft_conservation",
    "whole_pair_terminal", "whole_pair_terminal_or_C3_ready", "formal_credit",
    "whole_parent_credit", "D02_gate_credit", "row_sha256",
}
AGG_RESULT_KEYS = {
    "schema", "status", "producer_file_sha256", "producer_independence", "frozen_inputs",
    "authority_snapshot", "shard_receipts", "coverage", "ledgers", "invariants",
    "candidate_is_authority", "formal_credit", "whole_parent_credit", "D02_gate_credit",
    "runtime_canonical_pointer_or_seal_writes", "object_sha256",
}


class Rejected(RuntimeError):
    pass


class AwaitingCompleteReceipts(Rejected):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                      allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def same_json(left: Any, right: Any) -> bool:
    """Type-sensitive JSON equality (unlike Python's True == 1)."""
    return canonical(left) == canonical(right)


def exact_int(value: Any, expected: int, label: str) -> None:
    need(type(value) is int and value == expected, label + ": exact integer")


def zero_credits(value: dict[str, Any], label: str) -> None:
    for key in ("formal_credit", "whole_parent_credit", "D02_gate_credit"):
        exact_int(value.get(key), 0, label + ":" + key)


def close(value: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(value)
    need("object_sha256" not in result, "object already closed")
    result["object_sha256"] = digest(result)
    return result


def parse(raw: bytes, label: str, canonical_required: bool = False) -> Any:
    need(bool(raw) and not raw.startswith(b"\xef\xbb\xbf"), label + ": nonempty/no BOM")

    def hook(items: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in items:
            need(key not in value, label + ": duplicate key:" + key)
            value[key] = item
        return value

    try:
        value = json.loads(
            raw.decode("utf-8", "strict"), object_pairs_hook=hook,
            parse_float=lambda token: (_ for _ in ()).throw(
                Rejected(label + ": JSON float forbidden:" + token)),
            parse_constant=lambda token: (_ for _ in ()).throw(
                Rejected(label + ": nonfinite:" + token)),
        )
    except Rejected:
        raise
    except Exception as error:
        raise Rejected(label + ": JSON:" + str(error)) from error
    if canonical_required:
        need(raw == canonical(value) + b"\n", label + ": canonical compact bytes/newline")
    return value


def parse_closed(raw: bytes, label: str, file_pin: str | None = None,
                 object_pin: str | None = None) -> dict[str, Any]:
    if file_pin is not None:
        need(hashlib.sha256(raw).hexdigest() == file_pin, label + ": file pin")
    value = parse(raw, label, canonical_required=True)
    need(type(value) is dict and HEX64.fullmatch(str(value.get("object_sha256"))) is not None,
         label + ": closed object claim")
    body = copy.deepcopy(value)
    claim = body.pop("object_sha256")
    need(digest(body) == claim and (object_pin is None or claim == object_pin),
         label + ": object closure/pin")
    return value


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink, value.st_size,
            value.st_mtime_ns, value.st_ctime_ns)


def capture(paths: Iterable[Path], maximum: int = 768 << 20,
            hook: Callable[[], None] | None = None) -> dict[Path, bytes]:
    """Capture regular single-link files through dirfd/openat, then recapture identity."""
    ordered = tuple(paths)
    need(len(ordered) == len(set(ordered)), "duplicate capture path")
    dirfds: dict[Path, int] = {}
    fds: dict[Path, int] = {}
    states: dict[Path, os.stat_result] = {}
    try:
        for path in ordered:
            parent = Path(os.path.abspath(os.fspath(path.parent)))
            need(parent.resolve(strict=True) == parent, "canonical parent:" + str(parent))
            if parent not in dirfds:
                dirfds[parent] = os.open(parent, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
            fd = os.open(path.name, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NONBLOCK", 0) |
                         getattr(os, "O_NOFOLLOW", 0), dir_fd=dirfds[parent])
            state = os.fstat(fd)
            need(stat.S_ISREG(state.st_mode) and state.st_nlink == 1 and
                 0 < state.st_size <= maximum, "regular single-link bounded:" + str(path))
            current = os.stat(path.name, dir_fd=dirfds[parent], follow_symlinks=False)
            need(fingerprint(state) == fingerprint(current), "open/path identity:" + str(path))
            fds[path] = fd
            states[path] = state
        result: dict[Path, bytes] = {}
        for path in ordered:
            pieces: list[bytes] = []
            while block := os.read(fds[path], 4 << 20):
                pieces.append(block)
            result[path] = b"".join(pieces)
        if hook is not None:
            hook()
        for path in ordered:
            parent = Path(os.path.abspath(os.fspath(path.parent)))
            current = os.stat(path.name, dir_fd=dirfds[parent], follow_symlinks=False)
            need(fingerprint(states[path]) == fingerprint(os.fstat(fds[path])) ==
                 fingerprint(current), "TOCTOU:" + str(path))
        return result
    finally:
        for fd in fds.values():
            os.close(fd)
        for fd in dirfds.values():
            os.close(fd)


def descriptor_exact(value: Any, filename: str, order: str, label: str) -> dict[str, Any]:
    need(type(value) is dict and set(value) == DESCRIPTOR_KEYS and
         value["filename"] == filename and value["order"] == order and
         type(value["row_count"]) is int and value["row_count"] >= 0 and
         type(value["size"]) is int and value["size"] > 0 and
         HEX64.fullmatch(str(value["sha256"])) is not None and
         HEX64.fullmatch(str(value["row_hash_line_sequence_sha256"])) is not None,
         label + ": exact descriptor")
    need(type(value["row_count"]) is int and not isinstance(value["row_count"], bool) and
         type(value["size"]) is int and not isinstance(value["size"], bool),
         label + ": integer descriptor types")
    return value


def validate_credit_types(value: dict[str, Any], label: str,
                          include_local: bool = False) -> None:
    zero_credits(value, label)
    if include_local:
        need(type(value.get("local_terminal_credit")) is int and
             value["local_terminal_credit"] in {0, 1}, label + ": local credit integer")


def iter_ledger(raw: bytes, descriptor: dict[str, Any], label: str,
                file_pin: str | None = None, expanded_limit: int = 3 << 30) -> Iterator[dict[str, Any]]:
    """Strict, bounded, streaming single-member gzip JSONL reader."""
    claim = hashlib.sha256(raw).hexdigest()
    need(len(raw) == descriptor["size"] and claim == descriptor["sha256"] and
         (file_pin is None or claim == file_pin), label + ": descriptor bytes")
    need(len(raw) >= 18 and raw[:3] == b"\x1f\x8b\x08" and raw[3] == 0 and
         raw[4:8] == b"\0\0\0\0", label + ": deterministic gzip header")
    decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
    buffer = b""
    count = 0
    expanded = 0
    sequence = hashlib.sha256()
    for offset in range(0, len(raw), 1 << 20):
        try:
            block = decoder.decompress(raw[offset:offset + (1 << 20)])
        except zlib.error as error:
            raise Rejected(label + ": gzip:" + str(error)) from error
        expanded += len(block)
        need(expanded <= expanded_limit, label + ": bounded inflate")
        buffer += block
        while b"\n" in buffer:
            line, buffer = buffer.split(b"\n", 1)
            row = parse(line + b"\n", label + ":row", canonical_required=True)
            need(type(row) is dict and HEX64.fullmatch(str(row.get("row_sha256"))) is not None,
                 label + ": row claim")
            body = copy.deepcopy(row)
            row_claim = body.pop("row_sha256")
            need(digest(body) == row_claim, label + ": row closure")
            sequence.update((row_claim + "\n").encode("ascii"))
            count += 1
            yield row
    try:
        tail = decoder.flush()
    except zlib.error as error:
        raise Rejected(label + ": gzip flush:" + str(error)) from error
    expanded += len(tail)
    need(expanded <= expanded_limit, label + ": bounded final inflate")
    buffer += tail
    need(decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail and
         buffer == b"", label + ": one member/no trailing/framed newline")
    need(count == descriptor["row_count"] and
         sequence.hexdigest() == descriptor["row_hash_line_sequence_sha256"],
         label + ": count/row sequence")


def q(value: Any) -> Fraction:
    return Fraction(str(value))


def prefix_free(paths: list[str]) -> bool:
    ordered = sorted(paths)
    return len(ordered) == len(set(ordered)) and all(
        not later.startswith(first) for first, later in zip(ordered, ordered[1:])
    )


def assignment_preimage(source_sha: str, path: str) -> bytes:
    need(HEX64.fullmatch(source_sha) is not None and type(path) is str and len(path) == 21 and
         set(path) <= {"0", "1"}, "assignment exact source/path")
    return canonical({"assignment_domain": DOMAIN, "path": path,
                      "source_C61_aggregate_leaf_row_sha256": source_sha})


def receipt_path(shard: int) -> Path:
    return OUT / f"cm2_round306c65s18_depth18_64shard_shard_{shard:02d}_receipt_v3.json"


def shard_ledger_path(shard: int) -> Path:
    return OUT / f"cm2_round306c65s18_depth18_64shard_shard_{shard:02d}_leaf_ledger_v3.jsonl.gz"


def receipt_barrier(directory: Path = OUT) -> tuple[str, ...]:
    """Enumerate receipt names only.  Never derive or touch a ledger on failure."""
    names = tuple(sorted(entry.name for entry in os.scandir(directory)
                         if RECEIPT_RE.fullmatch(entry.name)))
    ids = [int(RECEIPT_RE.fullmatch(name).group(1)) for name in names]  # type: ignore[union-attr]
    if ids != list(SHARDS):
        raise AwaitingCompleteReceipts(
            f"receipt-first barrier: expected exact 00..63, observed {len(ids)} ids={ids[:4]}...{ids[-4:]}"
        )
    return names


def shard_name_snapshot(directory: Path = OUT) -> tuple[tuple[str, ...], tuple[str, ...]]:
    names = tuple(entry.name for entry in os.scandir(directory))
    receipts = tuple(sorted(name for name in names if RECEIPT_RE.fullmatch(name)))
    ledgers = tuple(sorted(name for name in names if SHARD_LEDGER_RE.fullmatch(name)))
    need(receipts == tuple(receipt_path(i).name for i in SHARDS) and
         ledgers == tuple(shard_ledger_path(i).name for i in SHARDS),
         "exact 64 receipt/ledger name sets; no orphan/extra")
    return receipts, ledgers


def controller_running() -> bool:
    needle = CONTROLLER.name.encode("utf-8")
    proc = Path("/proc")
    try:
        need(proc.is_dir(), "/proc required for fail-closed controller audit")
        entries = tuple(proc.iterdir())
    except (OSError, Rejected) as error:
        raise Rejected("cannot audit /proc controller state:" + str(error)) from error
    for entry in entries:
        if not entry.name.isdigit():
            continue
        try:
            raw = (entry / "cmdline").read_bytes()
        except (FileNotFoundError, ProcessLookupError):
            continue
        except PermissionError as error:
            raise Rejected("permission denied auditing /proc/" + entry.name + "/cmdline") from error
        except OSError as error:
            if error.errno in {2, 3}:
                continue
            raise Rejected("cannot audit /proc/" + entry.name + "/cmdline:" + str(error)) from error
        if needle in raw:
            return True
    return False


def authenticated_kernel(raw: dict[Path, bytes]) -> Any:
    """Load C41's independent auditor only after its captured source is pinned."""
    global _KERNEL
    sources = {
        C41_AUDITOR: PIN["C41_independent_auditor_file"],
        C40_AUDITOR: PIN["C40_independent_auditor_file"],
        C39_KERNEL: PIN["C39_kernel_file"], ROUND139: PIN["Round139_file"],
        ROUND166: PIN["Round166_file"], ROUND185: PIN["Round185_file"],
        ROUND181: PIN["Round181_file"], ROUND178: PIN["Round178_file"],
    }
    need(all(hashlib.sha256(raw[path]).hexdigest() == pin for path, pin in sources.items()),
         "C41 independent auditor and all downstream numeric source pre-load pins")
    source = raw[C41_AUDITOR]
    tree = ast.parse(source.decode("utf-8", "strict"), filename=C41_AUDITOR.name)
    producer_stem = "cm2_round306c41_d02_lower_strata_depth3_closure_v1"
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names if alias.name == producer_stem)
        elif isinstance(node, ast.ImportFrom) and node.module == producer_stem:
            imports.append(str(node.module))
    need(not imports, "C41 independent auditor AST excludes C41 producer")
    if _KERNEL is None:
        isolated = ModuleType(C41_MODULE + "__isolated_c65_cold")
        isolated.__file__ = str(C41_AUDITOR)
        isolated.__package__ = ""
        isolated.__loader__ = None
        isolated.__spec__ = None
        code = compile(source, str(C41_AUDITOR), "exec", dont_inherit=True, optimize=0)
        exec(code, isolated.__dict__)
        _KERNEL = isolated
    need(_KERNEL.__name__ not in sys.modules and
         Path(_KERNEL.__file__).resolve() == C41_AUDITOR.resolve() and
         hashlib.sha256(capture((C41_AUDITOR,))[C41_AUDITOR]).hexdigest() ==
         PIN["C41_independent_auditor_file"],
         "C41 isolated source-byte execution/no sys.modules/post-load byte pin")
    # This validates the C39/C40 independent auditor and Round139/166/185
    # dependency hashes before any numerical replay is accepted.
    _KERNEL.source_pins()
    return _KERNEL


def program_independence(raw: dict[Path, bytes], aggregate_result: dict[str, Any]) -> dict[str, Any]:
    programs = {
        "executor": (EXECUTOR, PIN["executor_file"]),
        "controller": (CONTROLLER, PIN["controller_file"]),
        "checker": (CHECKER, PIN["checker_file"]),
    }
    observed: dict[str, str] = {}
    for label, (path, pin) in programs.items():
        claim = hashlib.sha256(raw[path]).hexdigest()
        need(claim == pin, label + ": frozen source pin")
        ast.parse(raw[path].decode("utf-8", "strict"), filename=path.name)
        need(path.stem not in sys.modules, label + ": not imported")
        observed[label + "_file_sha256"] = claim

    producer_sha = hashlib.sha256(raw[AGG_PRODUCER]).hexdigest()
    need(aggregate_result["producer_file_sha256"] == producer_sha,
         "aggregate producer observed self-pin")
    producer_tree = ast.parse(raw[AGG_PRODUCER].decode("utf-8", "strict"),
                              filename=AGG_PRODUCER.name)
    forbidden_modules = {EXECUTOR.stem, CONTROLLER.stem, CHECKER.stem}
    forbidden_dynamic: list[str] = []
    forbidden_imports: list[str] = []
    for node in ast.walk(producer_tree):
        if isinstance(node, ast.Import):
            forbidden_imports.extend(alias.name for alias in node.names
                                     if alias.name in forbidden_modules)
        elif isinstance(node, ast.ImportFrom) and node.module in forbidden_modules:
            forbidden_imports.append(str(node.module))
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in {
                "exec", "eval", "compile", "__import__",
            }:
                forbidden_dynamic.append(node.func.id)
            elif isinstance(node.func, ast.Attribute) and node.func.attr in {
                "system", "popen", "run", "Popen", "call", "check_call", "check_output",
            }:
                forbidden_dynamic.append(node.func.attr)
    source_text = raw[AGG_PRODUCER].decode("utf-8", "strict")
    need(not forbidden_imports and not forbidden_dynamic and
         "O_EXCL" in source_text and "O_NOFOLLOW" in source_text and "fsync" in source_text,
         "aggregate producer inert AST/no subprocess/atomic no-replace protocol")
    need(AGG_PRODUCER.stem not in sys.modules, "aggregate producer not imported")

    self_tree = ast.parse(raw[SELF].decode("utf-8", "strict"), filename=SELF.name)
    self_imports: list[str] = []
    for node in ast.walk(self_tree):
        if isinstance(node, ast.Import):
            self_imports.extend(alias.name for alias in node.names if alias.name in forbidden_modules)
        elif isinstance(node, ast.ImportFrom) and node.module in forbidden_modules:
            self_imports.append(str(node.module))
    need(not self_imports and all(name not in sys.modules for name in forbidden_modules),
         "cold verifier no executor/controller/checker import")
    return {
        **observed,
        "cold_verifier_file_sha256": hashlib.sha256(raw[SELF]).hexdigest(),
        "aggregate_producer_file_sha256": producer_sha,
        "programs_consumed_as_inert_bytes_or_AST_only": True,
        "executor_controller_checker_or_producer_imported": False,
        "executor_controller_checker_or_producer_executed": False,
        "aggregate_no_replace_protocol_AST_verified": True,
    }


def authority_snapshot(raw: dict[Path, bytes]) -> dict[str, str]:
    observed = {
        "C50d_global_claim": hashlib.sha256(raw[GLOBAL_CLAIM]).hexdigest(),
        "C50d_global_head": hashlib.sha256(raw[GLOBAL_HEAD]).hexdigest(),
        "C53_audit_token": hashlib.sha256(raw[C53_AUDIT_TOKEN]).hexdigest(),
        "C53_successor_token": hashlib.sha256(raw[C53_TOKEN]).hexdigest(),
        "CM2_LATEST_STATUS.md": hashlib.sha256(raw[CANONICAL]).hexdigest(),
        "CM2_LATEST_STATUS.sha256": hashlib.sha256(raw[CANONICAL_COMPANION]).hexdigest(),
    }
    need(same_json(observed, EXPECTED_AUTHORITY) and
         digest(observed) == PIN["authority_snapshot_object"],
         "exact authority snapshot/object")
    need(raw[CANONICAL_COMPANION] ==
         (PIN["canonical_file"] + "  CM2_LATEST_STATUS.md\n").encode("ascii"),
         "canonical companion content")
    head = parse_closed(raw[GLOBAL_HEAD], "global head")
    need(head["authority_seal_object_sha256"] ==
         "cb90ab914c3b6518384669f42d05df33c21a717596190131c6a0f5683934cbfb" and
         head["post_seal_effective_checkpoint_object_sha256"] ==
         PIN["effective_checkpoint_object"] and
         head["successor_checkpoint_object_sha256"] == PIN["effective_checkpoint_object"],
         "global head semantic/effective checkpoint")
    return observed


def all_capture_paths() -> tuple[Path, ...]:
    return (
        SELF, C41_AUDITOR, C40_AUDITOR, C39_KERNEL, ROUND139, ROUND166,
        ROUND185, ROUND181, ROUND178, EXECUTOR, CONTROLLER, CHECKER, AGG_PRODUCER,
        CONTRACT, ASSIGNMENT, INVENTORY, AUTHORIZATION,
        C61_RESULT, C61_LEAVES, C58_RESULT, C58_LEAVES, C40_RESULT, C40_ROUTED,
        AGG_RESULT, AGG_LEAVES, AGG_SOURCES, AGG_PARENTS,
        CANONICAL, CANONICAL_COMPANION, GLOBAL_HEAD, GLOBAL_CLAIM,
        C53_TOKEN, C53_AUDIT_TOKEN,
        *(receipt_path(shard) for shard in SHARDS),
        *(shard_ledger_path(shard) for shard in SHARDS),
    )


def capture_formal_inputs() -> dict[Path, bytes]:
    # Mandatory ordering: receipts only first.  No ledger path is even derived
    # by this function until receipt_barrier has returned successfully.
    receipt_barrier(OUT)
    need(not controller_running(), "bulk controller must have exited before aggregate capture")
    before = shard_name_snapshot(OUT)
    raw = capture(all_capture_paths())
    after = shard_name_snapshot(OUT)
    need(same_json(before, after), "shard directory receipt/ledger set stable across capture")
    return raw


def validate_frozen_objects(raw: dict[Path, bytes]) -> tuple[
        dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]
    ]:
    contract = parse_closed(raw[CONTRACT], "contract", PIN["contract_file"],
                            PIN["contract_object"])
    assignment = parse_closed(raw[ASSIGNMENT], "assignment", PIN["assignment_file"],
                              PIN["assignment_object"])
    authorization = parse_closed(raw[AUTHORIZATION], "authorization",
                                 PIN["authorization_file"], PIN["authorization_object"])
    c61_result = parse_closed(raw[C61_RESULT], "C61 result", PIN["C61_result_file"],
                              PIN["C61_result_object"])
    c58_result = parse_closed(raw[C58_RESULT], "C58 result", PIN["C58_result_file"],
                              PIN["C58_result_object"])
    need(contract["selection"]["exact_count"] == 20879 and
         contract["selection"]["pair_indices_exactly"] == list(PAIRS) and
         contract["assignment"]["shard_ids_exactly"] == list(SHARDS) and
         contract["assignment"]["modulus"] == 64 and
         contract["source"]["C40_context_object_sha256"] == PIN["C40_object"],
         "contract exact selection/assignment/source")
    exact_int(contract["selection"]["exact_count"], 20879, "contract selection count")
    exact_int(contract["assignment"]["modulus"], 64, "contract assignment modulus")
    exact_int(assignment["input_count"], 20879, "assignment input count")
    exact_int(assignment["shard_count"], 64, "assignment shard count")
    need(assignment["schema"] == CORE_SCHEMA.rsplit(".v3", 1)[0] + ".v2.assignment-result" and
         assignment["status"] ==
         "FROZEN_V2_COMPLETE_MUTUALLY_EXCLUSIVE_20879_TO_64_CANONICAL_JSON_ASSIGNMENT" and
         assignment["input_count"] == 20879 and assignment["shard_count"] == 64 and
         assignment["assignment_domain"] == DOMAIN and assignment["assignment_complete"] is True and
         assignment["assignment_mutually_exclusive"] is True and
         assignment["candidate_is_authority"] is False and
         assignment["partial_statistics_are_formal_credit"] is False and
         assignment["formal_credit"] == assignment["whole_parent_credit"] ==
         assignment["D02_gate_credit"] == 0 and
         assignment["runtime_canonical_pointer_or_seal_writes"] is False,
         "assignment exact status/noncredit")
    zero_credits(assignment, "assignment")
    exact_int(authorization["assignment"]["input_count"], 20879, "authorization input count")
    exact_int(authorization["assignment"]["shard_count"], 64, "authorization shard count")
    need(authorization["status"] ==
         "PASS_INDEPENDENT_FROZEN_ASSIGNMENT_BYTES_FOR_SHARD_EXECUTION__ZERO_CREDIT" and
         authorization["assignment"]["input_count"] == 20879 and
         authorization["assignment"]["shard_count"] == 64 and
         authorization["assignment"]["complete"] is True and
         authorization["assignment"]["mutually_exclusive"] is True and
         authorization["assignment"]["source_identity_bijection"] is True and
         authorization["partial_shards_are_an_aggregate"] is False and
         authorization["candidate_is_authority"] is False and
         authorization["formal_credit"] == authorization["whole_parent_credit"] ==
         authorization["D02_gate_credit"] == 0 and
         authorization["runtime_canonical_pointer_or_seal_writes"] is False,
         "authorization exact semantics/noncredit")
    zero_credits(authorization, "authorization")
    need(c61_result["schema"] ==
         "cm2.round306c61s12.depth12-16shard.v1.aggregate-result.v4" and
         c61_result["status"].startswith("PASS_COMPLETE_16_SHARD_DEPTH12_AGGREGATE_V4") and
         c61_result["formal_credit"] == c61_result["whole_parent_credit"] ==
         c61_result["D02_gate_credit"] == 0,
         "C61 frozen v4 zero-credit source")
    zero_credits(c61_result, "C61 result")
    need(hashlib.sha256(raw[C40_RESULT]).hexdigest() == PIN["C40_result_file"],
         "C40 result file pin")
    c40_result = parse_closed(raw[C40_RESULT], "C40 result", object_pin=PIN["C40_object"])
    descriptor_exact(c40_result["ledgers"]["routed_leaf_cells"], C40_ROUTED.name,
                     "C39_ROW_ORDER_THEN_PATH", "C40 routed descriptor")
    need(hashlib.sha256(raw[C40_ROUTED]).hexdigest() == PIN["C40_routed_file"],
         "C40 routed ledger file pin")
    return contract, assignment, authorization, c61_result, c58_result


def expected_assignment_row(source: dict[str, Any], c58: dict[str, Any]) -> dict[str, Any]:
    claim = hashlib.sha256(assignment_preimage(source["row_sha256"], source["path"])).hexdigest()
    shard = int(claim, 16) % 64
    body = {
        "schema": "cm2.round306c65s18.depth18-64shard.v2.assignment-row",
        "assignment_preimage_sha256": claim, "shard_id": shard,
        "source_C61_aggregate_leaf_row_sha256": source["row_sha256"],
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
    }
    # Ensure lineage to C58 before admitting the assignment row.
    need(c58["row_sha256"] == source["source_C58_leaf_row_sha256"] and
         c58["disposition"] == "COLLISION2_HANDOFF" and
         c58["source_handoff_ordinal"] == source["source_handoff_ordinal"] and
         c58["path"] == source["source_path"] and source["path"].startswith(c58["path"]) and
         c58["pair_index"] == source["pair_index"] and
         source["continuation"]["prior_C58_leaf_row_sha256"] == c58["row_sha256"] and
         source["continuation"]["prior_C58_handoff_object_sha256"] ==
         c58["collision2_handoff"]["handoff_object_sha256"],
         "C61/C58 exact lineage")
    return {**body, "row_sha256": digest(body)}


def load_source_universe(
    raw: dict[Path, bytes], assignment: dict[str, Any], authorization: dict[str, Any],
    c61_result: dict[str, Any], c58_result: dict[str, Any],
) -> tuple[
    list[dict[str, Any]], list[dict[str, Any]], dict[str, dict[str, Any]],
    dict[int, list[dict[str, Any]]], dict[int, list[dict[str, Any]]]
]:
    c58_descriptor = descriptor_exact(
        c58_result["ledgers"]["leaves"], C58_LEAVES.name,
        "SOURCE_HANDOFF_ORDINAL_THEN_PATH", "C58 leaves descriptor",
    )
    c58_rows = list(iter_ledger(raw[C58_LEAVES], c58_descriptor, "C58 leaves",
                                PIN["C58_leaf_file"], expanded_limit=256 << 20))
    c58_by_hash = {row["row_sha256"]: row for row in c58_rows}
    need(len(c58_rows) == len(c58_by_hash) == 5548, "C58 exact unique leaf universe")

    c61_descriptor = descriptor_exact(
        c61_result["ledgers"]["aggregate_leaves"], C61_LEAVES.name,
        "SOURCE_HANDOFF_ORDINAL_THEN_PATH", "C61 aggregate leaves descriptor",
    )
    selected: list[dict[str, Any]] = []
    carried_by_pair: dict[int, list[dict[str, Any]]] = defaultdict(list)
    c61_census: Counter[str] = Counter()
    source_sequence = hashlib.sha256()
    continuation_sequence = hashlib.sha256()
    for row in iter_ledger(raw[C61_LEAVES], c61_descriptor, "C61 aggregate leaves",
                           PIN["C61_leaf_file"], expanded_limit=512 << 20):
        need(type(row["pair_index"]) is int and row["pair_index"] in PAIRS,
             "C61 pair/credit")
        zero_credits(row, "C61 aggregate leaf")
        disposition = row["disposition"]
        c61_census[disposition] += 1
        if disposition == "STRICT_TERMINAL":
            need(row["continuation"] is None, "C61 carried strict terminal")
            exact_int(row["local_terminal_credit"], 1, "C61 carried local credit")
            carried_by_pair[row["pair_index"]].append(row)
        elif disposition == "COLLISION2_HANDOFF":
            continuation = row["continuation"]
            need(type(continuation) is dict and len(row["path"]) == 21 and
                 set(row["path"]) <= {"0", "1"} and
                 row["parent_volume_fraction"] == "1/2097152",
                 "C61 exact selected collision2 predicate")
            exact_int(continuation["next_collision_index"], 2, "C61 next collision index")
            exact_int(row["additional_depth_from_C58"], 6, "C61 additional depth")
            exact_int(row["local_terminal_credit"], 0, "C61 selected local credit")
            exact_int(continuation["continuation_credit"], 0,
                      "C61 selected continuation credit")
            open_continuation = copy.deepcopy(continuation)
            continuation_claim = open_continuation.pop("continuation_object_sha256")
            need(digest(open_continuation) == continuation_claim,
                 "C61 selected continuation closure")
            selected.append(row)
            source_sequence.update((row["row_sha256"] + "\n").encode("ascii"))
            continuation_sequence.update((continuation_claim + "\n").encode("ascii"))
        else:
            raise Rejected("C61 unexpected pre-C65 disposition:" + str(disposition))
    need(c61_census == Counter({"STRICT_TERMINAL": 23997, "COLLISION2_HANDOFF": 20879}) and
         len(selected) == len({row["row_sha256"] for row in selected}) == 20879 and
         set(carried_by_pair) == set(PAIRS), "C61 exact carry/selection census")
    need(source_sequence.hexdigest() ==
         assignment["filtered_source_row_sha256_line_sequence_sha256"] and
         continuation_sequence.hexdigest() ==
         assignment["filtered_continuation_object_sha256_line_sequence_sha256"],
         "C61 filtered source/continuation sequences")

    inventory_descriptor = descriptor_exact(
        assignment["inventory"], INVENTORY.name,
        "C61_V4_AGGREGATE_LEDGER_ORDER_FILTERED_COLLISION2_HANDOFF",
        "assignment inventory descriptor",
    )
    need(assignment["inventory"]["sha256"] == PIN["inventory_file"],
         "assignment inventory result pin")
    observed_inventory = iter_ledger(raw[INVENTORY], inventory_descriptor,
                                     "assignment inventory", PIN["inventory_file"],
                                     expanded_limit=256 << 20)
    expected_inventory: list[dict[str, Any]] = []
    by_shard: dict[int, list[dict[str, Any]]] = {shard: [] for shard in SHARDS}
    preimages = hashlib.sha256()
    shard_counts: Counter[int] = Counter()
    for source, observed in zip(selected, observed_inventory, strict=True):
        c58 = c58_by_hash.get(source["source_C58_leaf_row_sha256"])
        need(c58 is not None, "C61 source present in C58")
        expected = expected_assignment_row(source, c58)
        need(set(observed) == set(expected) and same_json(observed, expected),
             "exact independently rebuilt assignment row")
        expected_inventory.append(expected)
        by_shard[expected["shard_id"]].append(expected)
        shard_counts[expected["shard_id"]] += 1
        preimages.update((expected["assignment_preimage_sha256"] + "\n").encode("ascii"))
    try:
        next(observed_inventory)
    except StopIteration:
        pass
    else:
        raise Rejected("assignment inventory has rows beyond selected C61 sources")
    counts = {str(shard): shard_counts[shard] for shard in SHARDS}
    need(len(expected_inventory) == 20879 and all(shard_counts.values()) and
         same_json(counts, assignment["per_shard_input_counts"]) and
         same_json(counts, authorization["assignment"]["per_shard_input_counts"]) and
         preimages.hexdigest() == assignment["ordered_preimage_sha256_line_sequence_sha256"] ==
         authorization["assignment"]["ordered_preimage_sha256_line_sequence_sha256"],
         "assignment global/per-shard exact closure")
    return selected, expected_inventory, c58_by_hash, carried_by_pair, by_shard


def validate_continuation(row: dict[str, Any]) -> None:
    continuation = row["continuation"]
    disposition = row["disposition"]
    exact_int(row["local_terminal_credit"], 1 if disposition == "STRICT_TERMINAL" else 0,
              "row local terminal credit")
    if disposition == "STRICT_TERMINAL":
        need(continuation is None, "strict terminal exact continuation")
        return
    need(type(continuation) is dict,
         "nonterminal continuation object")
    open_value = copy.deepcopy(continuation)
    claim = open_value.pop("continuation_object_sha256", None)
    need(claim == digest(open_value) and continuation["next_collision_index"] ==
         (3 if disposition == "COLLISION3_READY" else 2) and
         continuation["exact_representative_box"] == row["exact_representative_box"] and
         continuation["exact_reflected_box"] == row["exact_reflected_box"] and
         continuation["route_classification"] == row["route_classification"] and
         continuation["route_witness"] == row["route_witness"] and
         continuation["route_method"] == row["route_method"] and
         continuation["continuation_credit"] == 0,
         "continuation closure/index/route/box binding")
    exact_int(continuation["next_collision_index"],
              3 if disposition == "COLLISION3_READY" else 2,
              "continuation next collision index")
    exact_int(continuation["continuation_credit"], 0, "continuation credit")


def aggregate_leaf_from_shard(row: dict[str, Any]) -> dict[str, Any]:
    body = {key: copy.deepcopy(value) for key, value in row.items()
            if key not in {"schema", "shard_id", "row_sha256"}}
    aggregate_body = {
        "schema": AGG_SCHEMA + ".aggregate-leaf-row",
        "source_C65_shard_id": row["shard_id"],
        "source_C65_shard_row_sha256": row["row_sha256"],
        **body,
    }
    return {**aggregate_body, "row_sha256": digest(aggregate_body)}


def route_evaluation_count(source_path: str, leaf_paths: list[str]) -> int:
    nodes = {source_path}
    for path in leaf_paths:
        need(path.startswith(source_path), "leaf descends from source")
        nodes.update(path[:length] for length in range(len(source_path) + 1, len(path) + 1))
    return len(nodes)


def validate_receipts_and_shard_ledgers(
    raw: dict[Path, bytes], by_shard: dict[int, list[dict[str, Any]]],
    authority: dict[str, str],
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], dict[str, int], dict[str, int]]:
    receipts: list[dict[str, Any]] = []
    source_observed: dict[str, dict[str, Any]] = {}
    global_disposition: Counter[str] = Counter()
    global_raw: Counter[str] = Counter()
    global_routes = 0
    for shard in SHARDS:
        receipt_raw = raw[receipt_path(shard)]
        receipt = parse_closed(receipt_raw, f"shard {shard:02d} receipt")
        need(set(receipt) == RECEIPT_KEYS and
             receipt["schema"] == CORE_SCHEMA + ".shard-receipt" and
             receipt["status"] == "PASS_COMPLETE_NO_REPLACE_DEPTH18_SHARD__ZERO_CREDIT" and
             receipt["runner_file_sha256"] == PIN["executor_file"] and
             receipt["shard_id"] == shard and receipt["shard_count"] == 64 and
             receipt["additional_binary_depth"] == 6 and
             receipt["assignment_contract_file_sha256"] == PIN["contract_file"] and
             receipt["assignment_contract_object_sha256"] == PIN["contract_object"] and
             receipt["assignment_authorization_file_sha256"] == PIN["authorization_file"] and
             receipt["assignment_authorization_object_sha256"] == PIN["authorization_object"] and
             receipt["assignment_result_file_sha256"] == PIN["assignment_file"] and
             receipt["assignment_result_object_sha256"] == PIN["assignment_object"] and
             receipt["assignment_inventory_sha256"] == PIN["inventory_file"] and
             receipt["assigned_input_count"] == len(by_shard[shard]) and
             same_json(receipt["authority_snapshot_before"], authority) and
             same_json(receipt["authority_snapshot_after"], authority) and
             receipt["authority_snapshot_object_sha256"] == PIN["authority_snapshot_object"] and
             receipt["shard_complete"] is True and
             receipt["partial_statistics_are_formal_credit"] is False and
             receipt["formal_credit"] == receipt["whole_parent_credit"] ==
             receipt["D02_gate_credit"] == 0 and
             receipt["runtime_canonical_pointer_or_seal_writes"] is False,
             f"shard {shard:02d} exact receipt protocol")
        exact_int(receipt["shard_id"], shard, f"shard {shard:02d} receipt id")
        exact_int(receipt["shard_count"], 64, f"shard {shard:02d} receipt count")
        exact_int(receipt["additional_binary_depth"], 6,
                  f"shard {shard:02d} receipt depth")
        exact_int(receipt["assigned_input_count"], len(by_shard[shard]),
                  f"shard {shard:02d} receipt assigned count")
        need(type(receipt["route_evaluation_count"]) is int and
             receipt["route_evaluation_count"] >= 0,
             f"shard {shard:02d} receipt route count integer")
        for label, census in (("disposition", receipt["output_disposition_census"]),
                              ("raw", receipt["raw_classification_census"])):
            need(type(census) is dict and all(type(count) is int and count >= 0
                                              for count in census.values()),
                 f"shard {shard:02d} {label} census integer counts")
        zero_credits(receipt, f"shard {shard:02d} receipt")
        descriptor = descriptor_exact(
            receipt["output_ledger"], shard_ledger_path(shard).name,
            "ASSIGNMENT_INVENTORY_ORDER_THEN_PATH", f"shard {shard:02d} ledger descriptor",
        )
        assigned = by_shard[shard]
        assigned_index = {row["source_C61_aggregate_leaf_row_sha256"]: index
                          for index, row in enumerate(assigned)}
        need(len(assigned_index) == len(assigned), f"shard {shard:02d} assignment uniqueness")
        assignment_sequence = hashlib.sha256()
        for assignment_row in assigned:
            assignment_sequence.update(
                (assignment_row["assignment_preimage_sha256"] + "\n").encode("ascii"))
        need(assignment_sequence.hexdigest() ==
             receipt["ordered_assignment_preimage_sha256_line_sequence_sha256"],
             f"shard {shard:02d} assignment sequence")

        groups: dict[str, dict[str, Any]] = {}
        previous_group = -1
        previous_path = ""
        shard_disposition: Counter[str] = Counter()
        shard_raw: Counter[str] = Counter()
        for row in iter_ledger(raw[shard_ledger_path(shard)], descriptor,
                               f"shard {shard:02d} ledger", expanded_limit=512 << 20):
            need(set(row) == SHARD_ROW_KEYS and row["schema"] == CORE_SCHEMA + ".shard-leaf-row" and
                 row["shard_id"] == shard and row["disposition"] in {
                     "STRICT_TERMINAL", "COLLISION3_READY", "COLLISION2_HANDOFF"} and
                 row["formal_credit"] == row["whole_parent_credit"] ==
                 row["D02_gate_credit"] == 0,
                 f"shard {shard:02d} row schema/disposition/credit")
            exact_int(row["shard_id"], shard, f"shard {shard:02d} row id")
            need(type(row["additional_depth_from_C61"]) is int and
                 0 <= row["additional_depth_from_C61"] <= 6,
                 f"shard {shard:02d} row exact integer depth")
            validate_credit_types(row, f"shard {shard:02d} row", include_local=True)
            source_hash = row["source_C61_aggregate_leaf_row_sha256"]
            need(source_hash in assigned_index, f"shard {shard:02d} row assigned source")
            group_index = assigned_index[source_hash]
            need(group_index >= previous_group and
                 (group_index != previous_group or row["path"] > previous_path),
                 f"shard {shard:02d} assignment/path order")
            if group_index != previous_group:
                previous_path = ""
            previous_group, previous_path = group_index, row["path"]
            assignment_row = assigned[group_index]
            need(row["assignment_preimage_sha256"] ==
                 assignment_row["assignment_preimage_sha256"] and
                 row["source_C61_shard_row_sha256"] ==
                 assignment_row["source_C61_source_shard_row_sha256"] and
                 row["source_C58_leaf_row_sha256"] ==
                 assignment_row["source_C58_leaf_row_sha256"] and
                 row["source_handoff_ordinal"] == assignment_row["source_handoff_ordinal"] and
                 row["pair_index"] == assignment_row["pair_index"] and
                 row["source_path"] == assignment_row["path"] and
                 row["C58_source_path"] == assignment_row["source_path"],
                 f"shard {shard:02d} row static lineage")
            validate_continuation(row)
            group = groups.setdefault(source_hash, {
                "row_hashes": [], "aggregate_hashes": [], "paths": [], "volumes": [],
                "dispositions": Counter(), "raw": Counter(), "shard_id": shard,
            })
            group["row_hashes"].append(row["row_sha256"])
            group["aggregate_hashes"].append(aggregate_leaf_from_shard(row)["row_sha256"])
            group["paths"].append(row["path"])
            group["volumes"].append(q(row["parent_volume_fraction"]))
            group["dispositions"][row["disposition"]] += 1
            group["raw"][row["route_classification"]] += 1
            shard_disposition[row["disposition"]] += 1
            shard_raw[row["route_classification"]] += 1
        need(set(groups) == set(assigned_index), f"shard {shard:02d} exact source coverage")
        summaries: list[dict[str, Any]] = []
        for assignment_row in assigned:
            source_hash = assignment_row["source_C61_aggregate_leaf_row_sha256"]
            group = groups[source_hash]
            need(prefix_free(group["paths"]) and
                 sum(group["volumes"], Fraction(0)) == q(assignment_row["parent_volume_fraction"]),
                 f"shard {shard:02d} source prefix/Kraft")
            row_sequence = hashlib.sha256(
                "".join(value + "\n" for value in group["row_hashes"]).encode("ascii")
            ).hexdigest()
            summaries.append({
                "assignment_preimage_sha256": assignment_row["assignment_preimage_sha256"],
                "source_C61_aggregate_leaf_row_sha256": source_hash,
                "source_output_row_count": len(group["row_hashes"]),
                "source_output_row_hash_line_sequence_sha256": row_sequence,
                "source_Kraft_conservation": assignment_row["parent_volume_fraction"],
                "source_prefix_free": True,
            })
            need(source_hash not in source_observed, "cross-shard duplicate source")
            group["row_sequence"] = row_sequence
            group["aggregate_sequence"] = hashlib.sha256(
                "".join(value + "\n" for value in group["aggregate_hashes"]).encode("ascii")
            ).hexdigest()
            source_observed[source_hash] = group
        need(same_json(summaries, receipt["input_assignment_rows"]) and
             {key: shard_disposition[key] for key in
              ("STRICT_TERMINAL", "COLLISION3_READY", "COLLISION2_HANDOFF")} ==
             receipt["output_disposition_census"] and
             dict(sorted(shard_raw.items())) == receipt["raw_classification_census"],
             f"shard {shard:02d} derived receipt summaries/census")
        global_routes += receipt["route_evaluation_count"]
        global_disposition.update(shard_disposition)
        global_raw.update(shard_raw)
        receipts.append(receipt)
    need(len(receipts) == 64 and len(source_observed) == 20879 and
         sum(global_disposition.values()) ==
         sum(receipt["output_ledger"]["row_count"] for receipt in receipts),
         "64-shard global source/leaf census")
    return (receipts, source_observed,
            {key: global_disposition[key] for key in
             ("STRICT_TERMINAL", "COLLISION3_READY", "COLLISION2_HANDOFF")},
            dict(sorted(global_raw.items())))


def numeric_context(kernel: Any) -> tuple[
        dict[str, tuple[int, dict[str, Any]]], dict[str, dict[str, Any]],
        dict[str, dict[str, Any]], dict[str, Any]
    ]:
    need(hashlib.sha256(C40_RESULT.read_bytes()).hexdigest() == PIN["C40_result_file"],
         "C40 result stable before numeric context")
    c40_result = kernel.c40a.pinned_result(C40, PIN["C40_object"], "C40 result")
    authority = c40_result["C39_authority"]
    c39_path = (ROOT / authority["path"]).resolve()
    c39_audit = (ROOT / authority["independent_audit_path"]).resolve()
    c39_result, _audit, _rows, _parents = kernel.c40a.load_c39_authority(c39_path, c39_audit)
    c38_index, cells, config = kernel.c40a.load_geometry_authority(c39_result)
    config["cores"] = tuple(kernel.round139.lower.core_cert.physical_cores())
    c40_rows = kernel.c40a.pinned_ledger(C40, c40_result, "routed_leaf_cells",
                                         "C40 routed leaves")
    c40_index = {row["row_sha256"]: (ordinal, row)
                 for ordinal, row in enumerate(c40_rows)}
    need(len(c40_rows) == len(c40_index) == 35009, "C40 routed row census/uniqueness")
    kernel.install_complete_cache()
    return c40_index, c38_index, cells, config


def independent_expected_row(
    kernel: Any, assignment_row: dict[str, Any], source: dict[str, Any],
    c58_source: dict[str, Any], path: str, depth: int, volume: Fraction,
    task: dict[str, Any], config: dict[str, Any], route: dict[str, Any],
) -> dict[str, Any]:
    family = kernel.disposition_family(route["classification"])
    if family == "TERMINAL_EXCLUDED":
        disposition, next_collision = "STRICT_TERMINAL", None
    elif family == "COLLISION3_READY":
        disposition, next_collision = "COLLISION3_READY", 3
    else:
        need(family == "RESIDUAL_OUTER" and depth == ADDITIONAL_DEPTH,
             "only depth6 residual becomes collision2 handoff")
        disposition, next_collision = "COLLISION2_HANDOFF", 2
    exact_box = kernel.box_payload(route["box"])
    reflected = kernel.reflected_box(
        task["c38_source"]["representative_origin_key"], route["box"])
    continuation: dict[str, Any] | None = None
    if next_collision is not None:
        continuation = {
            "next_collision_index": next_collision,
            "prior_C61_aggregate_leaf_row_sha256": source["row_sha256"],
            "prior_C61_shard_row_sha256": source["source_shard_row_sha256"],
            "prior_C61_continuation_object_sha256":
                source["continuation"]["continuation_object_sha256"],
            "prior_C58_leaf_row_sha256": c58_source["row_sha256"],
            "prior_C58_handoff_object_sha256":
                c58_source["collision2_handoff"]["handoff_object_sha256"],
            "collision1_history_row_sha256":
                source["continuation"]["collision1_history_row_sha256"],
            "collision1_original_owner":
                source["continuation"]["collision1_original_owner"],
            "collision1_event_order": source["continuation"]["collision1_event_order"],
            "exact_representative_box": exact_box,
            "exact_reflected_box": reflected,
            "route_classification": route["classification"],
            "route_witness": route["witness"],
            "route_method": route["route_method"],
            "continuation_credit": 0,
        }
        continuation["continuation_object_sha256"] = digest(continuation)
    body = {
        "schema": CORE_SCHEMA + ".shard-leaf-row",
        "shard_id": assignment_row["shard_id"],
        "assignment_preimage_sha256": assignment_row["assignment_preimage_sha256"],
        "source_C61_aggregate_leaf_row_sha256": source["row_sha256"],
        "source_C61_shard_row_sha256": source["source_shard_row_sha256"],
        "source_C58_leaf_row_sha256": c58_source["row_sha256"],
        "source_handoff_ordinal": source["source_handoff_ordinal"],
        "C58_source_path": source["source_path"], "source_path": source["path"],
        "path": path, "additional_depth_from_C61": depth,
        "nominal_additional_depth_from_C58": source["additional_depth_from_C58"] + depth,
        "pair_index": source["pair_index"], "parent_volume_fraction": str(volume),
        "exact_representative_box": exact_box, "exact_reflected_box": reflected,
        "route_classification": route["classification"],
        "route_witness": route["witness"], "route_method": route["route_method"],
        "disposition": disposition, "continuation": continuation,
        "local_terminal_credit": int(disposition == "STRICT_TERMINAL"),
        "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
    }
    return {**body, "row_sha256": digest(body)}


def independent_numeric_replay(
    kernel: Any, selected: list[dict[str, Any]], inventory: list[dict[str, Any]],
    c58_by_hash: dict[str, dict[str, Any]],
    source_observed: dict[str, dict[str, Any]],
    observed_aggregate: Iterator[dict[str, Any]], observed_sources: Iterator[dict[str, Any]],
) -> tuple[
    dict[int, list[tuple[str, Fraction, str]]], dict[str, int], dict[str, int], int,
    int, int, int,
]:
    c40_index, c38_index, cells, config = numeric_context(kernel)
    compact_replacements: dict[int, list[tuple[str, Fraction, str]]] = defaultdict(list)
    disposition_total: Counter[str] = Counter()
    raw_total: Counter[str] = Counter()
    route_total = 0
    leaf_total = 0
    whole_terminal = 0
    whole_terminal_or_c3 = 0
    task_cache: dict[str, dict[str, Any]] = {}
    for ordinal, (source, assignment_row) in enumerate(zip(selected, inventory, strict=True)):
        c58_source = c58_by_hash[source["source_C58_leaf_row_sha256"]]
        c40_hash = c58_source["C40_source_row_sha256"]
        if c40_hash not in task_cache:
            c40_ordinal, c40_source = c40_index[c40_hash]
            task_cache[c40_hash] = kernel.task_for_source(
                c40_ordinal, c40_source, c38_index, cells, config["source_chart_seams"]
            )
        task = task_cache[c40_hash]
        stack: list[tuple[str, int, Fraction]] = [
            (source["path"], 0, q(source["parent_volume_fraction"]))
        ]
        expected_shard_rows: list[dict[str, Any]] = []
        source_routes = 0
        while stack:
            path, depth, volume = stack.pop()
            route = kernel.independent_route_at_path(task, path, config)
            source_routes += 1
            route_total += 1
            family = kernel.disposition_family(route["classification"])
            if family == "RESIDUAL_OUTER" and depth < ADDITIONAL_DEPTH:
                stack.append((path + "1", depth + 1, volume / 2))
                stack.append((path + "0", depth + 1, volume / 2))
                continue
            row = independent_expected_row(kernel, assignment_row, source, c58_source,
                                           path, depth, volume, task, config, route)
            expected_shard_rows.append(row)
            compact_replacements[row["pair_index"]].append(
                (row["path"], q(row["parent_volume_fraction"]), row["disposition"])
            )
            disposition_total[row["disposition"]] += 1
            raw_total[row["route_classification"]] += 1
        paths = [row["path"] for row in expected_shard_rows]
        need(paths == sorted(paths) and prefix_free(paths) and
             sum((q(row["parent_volume_fraction"]) for row in expected_shard_rows), Fraction(0)) ==
             q(source["parent_volume_fraction"]), "numeric source DFS/prefix/Kraft")
        aggregate_rows = [aggregate_leaf_from_shard(row) for row in expected_shard_rows]
        for aggregate_row in aggregate_rows:
            try:
                observed_aggregate_row = next(observed_aggregate)
            except StopIteration as error:
                raise Rejected("aggregate leaf ledger ended before numeric replay") from error
            need(set(observed_aggregate_row) == AGG_LEAF_KEYS and
                 observed_aggregate_row == aggregate_row,
                 "aggregate leaf exact independent numeric reconstruction")
            leaf_total += 1
        counts = Counter(row["disposition"] for row in expected_shard_rows)
        source_body = {
            "schema": AGG_SCHEMA + ".aggregate-source-row",
            "source_inventory_ordinal": ordinal,
            "source_assignment_row_sha256": assignment_row["row_sha256"],
            "assignment_preimage_sha256": assignment_row["assignment_preimage_sha256"],
            "source_C61_aggregate_leaf_row_sha256": source["row_sha256"],
            "source_C61_shard_row_sha256": source["source_shard_row_sha256"],
            "source_handoff_ordinal": source["source_handoff_ordinal"],
            "source_path": source["path"], "pair_index": source["pair_index"],
            "source_C65_shard_id": assignment_row["shard_id"],
            "output_leaf_count": len(expected_shard_rows),
            "strict_terminal_leaf_count": counts["STRICT_TERMINAL"],
            "collision3_ready_leaf_count": counts["COLLISION3_READY"],
            "collision2_handoff_leaf_count": counts["COLLISION2_HANDOFF"],
            "route_evaluation_count": source_routes,
            "source_shard_output_row_hash_line_sequence_sha256": hashlib.sha256(
                "".join(row["row_sha256"] + "\n" for row in expected_shard_rows).encode("ascii")
            ).hexdigest(),
            "aggregate_output_row_hash_line_sequence_sha256": hashlib.sha256(
                "".join(row["row_sha256"] + "\n" for row in aggregate_rows).encode("ascii")
            ).hexdigest(),
            "path_prefix_free": True,
            "source_Kraft_conservation": source["parent_volume_fraction"],
            "whole_source_terminal": counts["STRICT_TERMINAL"] == len(expected_shard_rows),
            "whole_source_terminal_or_C3_ready": counts["COLLISION2_HANDOFF"] == 0,
            "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
        }
        expected_source = {**source_body, "row_sha256": digest(source_body)}
        try:
            observed_source = next(observed_sources)
        except StopIteration as error:
            raise Rejected("aggregate source ledger ended before numeric replay") from error
        need(set(observed_source) == AGG_SOURCE_KEYS and
             same_json(observed_source, expected_source),
             "aggregate source exact independent numeric reconstruction")
        structural = source_observed[source["row_sha256"]]
        need(structural["row_hashes"] == [row["row_sha256"] for row in expected_shard_rows] and
             structural["aggregate_hashes"] == [row["row_sha256"] for row in aggregate_rows] and
             structural["row_sequence"] ==
             expected_source["source_shard_output_row_hash_line_sequence_sha256"] and
             structural["aggregate_sequence"] ==
             expected_source["aggregate_output_row_hash_line_sequence_sha256"],
             "producer shard rows exact independent numeric reconstruction")
        whole_terminal += int(expected_source["whole_source_terminal"])
        whole_terminal_or_c3 += int(expected_source["whole_source_terminal_or_C3_ready"])
    for iterator, label in ((observed_aggregate, "aggregate leaf"),
                            (observed_sources, "aggregate source")):
        try:
            next(iterator)
        except StopIteration:
            pass
        else:
            raise Rejected(label + " ledger has rows beyond independent universe")
    return (
        compact_replacements,
        {key: disposition_total[key] for key in
         ("STRICT_TERMINAL", "COLLISION3_READY", "COLLISION2_HANDOFF")},
        dict(sorted(raw_total.items())), route_total, leaf_total,
        whole_terminal, whole_terminal_or_c3,
    )


def expected_parent_rows(
    carried_by_pair: dict[int, list[dict[str, Any]]], selected: list[dict[str, Any]],
    compact_replacements: dict[int, list[tuple[str, Fraction, str]]],
) -> list[dict[str, Any]]:
    selected_count: Counter[int] = Counter(row["pair_index"] for row in selected)
    result: list[dict[str, Any]] = []
    for pair in PAIRS:
        carry = carried_by_pair[pair]
        children = compact_replacements[pair]
        paths = [row["path"] for row in carry] + [path for path, _volume, _disposition in children]
        need(prefix_free(paths) and
             sum((q(row["parent_volume_fraction"]) for row in carry), Fraction(0)) +
             sum((volume for _path, volume, _disposition in children), Fraction(0)) == 1,
             f"pair {pair} replacement prefix/Kraft one")
        census = Counter({"STRICT_TERMINAL": len(carry)})
        census.update(disposition for _path, _volume, disposition in children)
        body = {
            "schema": AGG_SCHEMA + ".aggregate-parent-row", "pair_index": pair,
            "C61_carried_strict_terminal_leaf_count": len(carry),
            "C61_selected_collision2_sources_replaced": selected_count[pair],
            "C65_replacement_leaf_count": len(children),
            "combined_leaf_count": len(carry) + len(children),
            "strict_terminal_leaf_count": census["STRICT_TERMINAL"],
            "collision3_ready_leaf_count": census["COLLISION3_READY"],
            "collision2_handoff_leaf_count": census["COLLISION2_HANDOFF"],
            "path_prefix_free": True, "parent_Kraft_conservation": "1",
            "whole_pair_terminal": census["COLLISION3_READY"] ==
                                   census["COLLISION2_HANDOFF"] == 0,
            "whole_pair_terminal_or_C3_ready": census["COLLISION2_HANDOFF"] == 0,
            "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
        }
        result.append({**body, "row_sha256": digest(body)})
    return result


def expected_shard_receipt_vector(
    raw: dict[Path, bytes], receipts: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    receipt_files: set[str] = set()
    receipt_objects: set[str] = set()
    ledger_files: set[str] = set()
    for shard, receipt in zip(SHARDS, receipts, strict=True):
        receipt_file = hashlib.sha256(raw[receipt_path(shard)]).hexdigest()
        receipt_object = receipt["object_sha256"]
        ledger_file = receipt["output_ledger"]["sha256"]
        need(receipt_file not in receipt_files and receipt_object not in receipt_objects and
             ledger_file not in ledger_files, "unique receipt/object/ledger byte identities")
        receipt_files.add(receipt_file)
        receipt_objects.add(receipt_object)
        ledger_files.add(ledger_file)
        result.append({
            "shard_id": shard, "receipt_filename": receipt_path(shard).name,
            "receipt_file_sha256": receipt_file,
            "receipt_object_sha256": receipt_object,
            "assigned_input_count": receipt["assigned_input_count"],
            "route_evaluation_count": receipt["route_evaluation_count"],
            "output_ledger": copy.deepcopy(receipt["output_ledger"]),
        })
    need(len(receipt_files) == len(receipt_objects) == len(ledger_files) == 64,
         "64 unique receipt/ledger identities")
    return result


def aggregate_descriptors(result: dict[str, Any]) -> tuple[
        dict[str, Any], dict[str, Any], dict[str, Any]
    ]:
    need(type(result["ledgers"]) is dict and
         set(result["ledgers"]) == {"aggregate_leaves", "source_summaries", "parent_summaries"},
         "aggregate exact ledger descriptor map")
    leaves = descriptor_exact(
        result["ledgers"]["aggregate_leaves"], AGG_LEAVES.name,
        "C61_V4_FILTERED_C2_ORDER_THEN_CHILD_PATH", "aggregate leaves descriptor",
    )
    sources = descriptor_exact(
        result["ledgers"]["source_summaries"], AGG_SOURCES.name,
        "C61_V4_FILTERED_C2_ORDER", "aggregate sources descriptor",
    )
    parents = descriptor_exact(
        result["ledgers"]["parent_summaries"], AGG_PARENTS.name,
        "PAIR_INDEX_ASCENDING", "aggregate parents descriptor",
    )
    need(sources["row_count"] == 20879 and parents["row_count"] == 12,
         "aggregate source/parent descriptor census")
    exact_int(sources["row_count"], 20879, "aggregate source descriptor count")
    exact_int(parents["row_count"], 12, "aggregate parent descriptor count")
    return leaves, sources, parents


def exact_result_projection(
    aggregate_result: dict[str, Any], program: dict[str, Any], authority: dict[str, str],
    assignment: dict[str, Any], raw: dict[Path, bytes], receipts: list[dict[str, Any]],
    leaves_descriptor: dict[str, Any], sources_descriptor: dict[str, Any],
    parents_descriptor: dict[str, Any], disposition: dict[str, int],
    raw_census: dict[str, int], routes: int, leaf_count: int,
    whole_terminal: int, whole_terminal_or_c3: int,
) -> None:
    expected_program = {
        "executor_file_sha256": PIN["executor_file"],
        "controller_file_sha256": PIN["controller_file"],
        "checker_file_sha256": PIN["checker_file"],
        "consumed_as_pinned_inert_bytes_and_AST_only": True,
        "imported": False, "executed": False,
    }
    need(program["executor_file_sha256"] == PIN["executor_file"] and
         program["controller_file_sha256"] == PIN["controller_file"] and
         program["checker_file_sha256"] == PIN["checker_file"],
         "program verifier pins agree")
    expected_complete = {
        "STRICT_TERMINAL": 23997 + disposition["STRICT_TERMINAL"],
        "COLLISION3_READY": disposition["COLLISION3_READY"],
        "COLLISION2_HANDOFF": disposition["COLLISION2_HANDOFF"],
    }
    expected_body = {
        "schema": AGG_RESULT_SCHEMA, "status": AGG_STATUS,
        "producer_file_sha256": program["aggregate_producer_file_sha256"],
        "producer_independence": expected_program,
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
            "assignment_ordered_preimage_sha256_line_sequence_sha256":
                assignment["ordered_preimage_sha256_line_sequence_sha256"],
            "post_seal_effective_checkpoint_object_sha256": PIN["effective_checkpoint_object"],
            "C69b_consumed": False, "C69c_consumed": False,
        },
        "authority_snapshot": {
            "files": authority, "object_sha256": PIN["authority_snapshot_object"],
            "post_seal_effective_checkpoint_object_sha256": PIN["effective_checkpoint_object"],
        },
        "shard_receipts": expected_shard_receipt_vector(raw, receipts),
        "coverage": {
            "input_C61_selected_collision2_sources": 20879,
            "shard_receipt_count": 64,
            "assignment_complete": True, "assignment_mutually_exclusive": True,
            "route_evaluation_count": routes,
            "replacement_output_leaf_count": leaf_count,
            "replacement_disposition_census": disposition,
            "raw_classification_census": raw_census,
            "whole_sources_terminal": whole_terminal,
            "whole_sources_terminal_or_C3_ready": whole_terminal_or_c3,
            "C61_carried_strict_terminal_leaves": 23997,
            "complete_parent_leaf_count": 23997 + leaf_count,
            "complete_parent_disposition_census": expected_complete,
            "parent_count": 12,
        },
        "ledgers": {
            "aggregate_leaves": leaves_descriptor,
            "source_summaries": sources_descriptor,
            "parent_summaries": parents_descriptor,
        },
        "invariants": {
            "receipt_ids_exactly_00_through_63_before_any_ledger_open": True,
            "controller_exited_before_any_receipt_or_ledger_open": True,
            "all_frozen_inputs_single_snapshot_TOCTOU_checked": True,
            "all_64_receipt_and_ledger_descriptors_closed": True,
            "all_20879_assignment_sources_unique_and_exactly_once": True,
            "assignment_formula_and_global_per_shard_sequences_rebuilt": True,
            "all_shard_rows_and_continuation_objects_self_hash_closed": True,
            "all_20879_source_partitions_prefix_free_and_Kraft_conserved": True,
            "C61_selected_collision2_parents_removed_before_children_inserted": True,
            "C61_parent_and_C65_children_not_double_counted": True,
            "all_12_replacement_parents_prefix_free_and_Kraft_one": True,
            "two_isolated_staging_builds_byte_identical": True,
            "gzip_descriptors_computed_after_close_and_reopen": True,
            "publication_no_replace_O_EXCL_O_NOFOLLOW_and_fsync": True,
            "C69b_or_C69c_capability_injected": False,
            "numeric_routes_independently_recomputed_by_this_aggregate_producer": False,
            "post_publication_no_producer_cold_numeric_replay_required": True,
            "partial_statistics_used_for_credit": False,
        },
        "candidate_is_authority": False, "formal_credit": 0,
        "whole_parent_credit": 0, "D02_gate_credit": 0,
        "runtime_canonical_pointer_or_seal_writes": False,
    }
    body = copy.deepcopy(aggregate_result)
    claim = body.pop("object_sha256")
    need(set(aggregate_result) == AGG_RESULT_KEYS and same_json(body, expected_body) and
         claim == digest(expected_body), "aggregate result exact independently derived projection")


def verify() -> dict[str, Any]:
    raw = capture_formal_inputs()
    contract, assignment, authorization, c61_result, c58_result = validate_frozen_objects(raw)
    aggregate_result = parse_closed(raw[AGG_RESULT], "aggregate result")
    need(set(aggregate_result) == AGG_RESULT_KEYS and
         aggregate_result["schema"] == AGG_RESULT_SCHEMA and
         aggregate_result["status"] == AGG_STATUS,
         "aggregate result top schema/status")
    leaves_descriptor, sources_descriptor, parents_descriptor = aggregate_descriptors(
        aggregate_result)
    authority = authority_snapshot(raw)
    program = program_independence(raw, aggregate_result)
    selected, inventory, c58_by_hash, carried_by_pair, by_shard = load_source_universe(
        raw, assignment, authorization, c61_result, c58_result)
    receipts, source_observed, receipt_disposition, receipt_raw = (
        validate_receipts_and_shard_ledgers(raw, by_shard, authority)
    )
    kernel = authenticated_kernel(raw)
    observed_leaves = iter_ledger(raw[AGG_LEAVES], leaves_descriptor, "aggregate leaves",
                                  expanded_limit=3 << 30)
    observed_sources = iter_ledger(raw[AGG_SOURCES], sources_descriptor, "aggregate sources",
                                   expanded_limit=256 << 20)
    (compact_replacements, numeric_disposition, numeric_raw, numeric_routes, leaf_count,
     whole_terminal, whole_terminal_or_c3) = independent_numeric_replay(
        kernel, selected, inventory, c58_by_hash, source_observed,
        observed_leaves, observed_sources,
    )
    need(numeric_disposition == receipt_disposition and numeric_raw == receipt_raw and
         numeric_routes == sum(receipt["route_evaluation_count"] for receipt in receipts) and
         leaf_count == leaves_descriptor["row_count"],
         "numeric replay equals 64 receipt/global census")
    parents = expected_parent_rows(carried_by_pair, selected, compact_replacements)
    observed_parents = iter_ledger(raw[AGG_PARENTS], parents_descriptor, "aggregate parents",
                                   expanded_limit=4 << 20)
    for expected in parents:
        try:
            observed = next(observed_parents)
        except StopIteration as error:
            raise Rejected("aggregate parent ledger ended early") from error
        need(set(observed) == AGG_PARENT_KEYS and same_json(observed, expected),
             "aggregate parent exact replacement/Kraft reconstruction")
    try:
        next(observed_parents)
    except StopIteration:
        pass
    else:
        raise Rejected("aggregate parent ledger has extra rows")
    exact_result_projection(
        aggregate_result, program, authority, assignment, raw, receipts,
        leaves_descriptor, sources_descriptor, parents_descriptor,
        numeric_disposition, numeric_raw, numeric_routes, leaf_count,
        whole_terminal, whole_terminal_or_c3,
    )

    # The numerical replay is long.  Re-establish the controller/name barriers
    # and byte-compare a fresh capture before accepting the result.
    need(not controller_running(), "controller absent after numeric replay")
    shard_name_snapshot(OUT)
    replay_raw = capture(all_capture_paths())
    need(raw.keys() == replay_raw.keys() and all(raw[path] == replay_raw[path] for path in raw),
         "all captured bytes stable across full numeric replay")
    need(not controller_running(), "controller absent after final capture")
    shard_name_snapshot(OUT)

    parent_terminal = sum(row["whole_pair_terminal"] for row in parents)
    return close({
        "schema": SCHEMA + ".cold-run-projection",
        "status": (
            "PASS_COLD_RUN_PROJECTION_64_OF_64__20879_ASSIGNMENTS__EXACT_DEPTH6_NUMERIC_REPLAY__"
            "C61_REPLACEMENT_PARENT_KRAFT__ZERO_CREDIT__NOT_FORMAL_UNTIL_DUAL_RUN_INSTALL"
        ),
        "aggregate": {
            "result_file_sha256": hashlib.sha256(raw[AGG_RESULT]).hexdigest(),
            "result_object_sha256": aggregate_result["object_sha256"],
            "leaf_ledger_sha256": leaves_descriptor["sha256"],
            "source_summary_sha256": sources_descriptor["sha256"],
            "parent_summary_sha256": parents_descriptor["sha256"],
            "producer_file_sha256": program["aggregate_producer_file_sha256"],
        },
        "coverage": {
            "shard_receipts": 64, "assigned_sources": 20879,
            "numeric_route_evaluations": numeric_routes,
            "replacement_leaf_count": leaf_count,
            "replacement_disposition_census": numeric_disposition,
            "complete_parent_leaf_count": 23997 + leaf_count,
            "complete_parent_disposition_census": {
                "STRICT_TERMINAL": 23997 + numeric_disposition["STRICT_TERMINAL"],
                "COLLISION3_READY": numeric_disposition["COLLISION3_READY"],
                "COLLISION2_HANDOFF": numeric_disposition["COLLISION2_HANDOFF"],
            },
            "whole_sources_terminal": whole_terminal,
            "whole_sources_terminal_or_C3_ready": whole_terminal_or_c3,
            "whole_pairs_terminal": parent_terminal,
        },
        "invariants": {
            "receipt_first_barrier_before_any_shard_ledger_open": True,
            "controller_absent_before_and_after_capture_and_numeric_replay": True,
            "all_program_and_input_bytes_pinned_or_result_bound": True,
            "all_20879_assignments_recomputed_from_C61_order": True,
            "all_depth6_DFS_routes_boxes_witnesses_methods_and_rows_recomputed": True,
            "all_shard_and_aggregate_rows_byte_semantically_exact": True,
            "all_source_partitions_prefix_free_and_Kraft_conserved": True,
            "all_12_C61_replacement_parents_prefix_free_and_Kraft_one": True,
            "C61_selected_parents_removed_not_double_counted": True,
            "effective_checkpoint_b58d68a0_bound": True,
            "authority_snapshot_unchanged": True,
            "no_C69b_or_C69c_capability_consumed": True,
            "aggregate_no_replace_protocol_AST_verified": True,
        },
        "independence": program,
        "candidate_is_authority": False, "formal_credit": 0,
        "whole_parent_credit": 0, "D02_gate_credit": 0,
        "runtime_canonical_pointer_or_seal_writes": False,
    })


def cold_run_receipt(projection_path: Path, projection_raw: bytes, projection: dict[str, Any],
                     seed: str) -> dict[str, Any]:
    need(seed in {"1", "2"}, "cold run seed is exactly 1 or 2")
    return close({
        "schema": SCHEMA + ".cold-run-receipt",
        "status": "PASS_ISOLATED_FULL_COLD_RUN_PROJECTION__ZERO_CREDIT",
        "pythonhashseed": seed,
        "verifier_file_sha256": hashlib.sha256(SELF.read_bytes()).hexdigest(),
        "projection_filename": projection_path.name,
        "projection_file_sha256": hashlib.sha256(projection_raw).hexdigest(),
        "projection_object_sha256": projection["object_sha256"],
        "candidate_is_authority": False, "formal_credit": 0,
        "whole_parent_credit": 0, "D02_gate_credit": 0,
        "runtime_canonical_pointer_or_seal_writes": False,
    })


def install_dual_run_verification() -> dict[str, Any]:
    receipt_barrier(OUT)
    need(not controller_running(), "controller absent during dual-run verification install")
    before_names = shard_name_snapshot(OUT)
    paths = (*all_capture_paths(), COLD_RUN_A, COLD_RUN_A_RECEIPT,
             COLD_RUN_B, COLD_RUN_B_RECEIPT)
    raw = capture(paths)
    need(before_names == shard_name_snapshot(OUT) and not controller_running(),
         "controller/name set stable during dual-run verification install")
    verifier_sha = hashlib.sha256(raw[SELF]).hexdigest()
    first = parse_closed(raw[COLD_RUN_A], "seed1 cold projection")
    second = parse_closed(raw[COLD_RUN_B], "seed2 cold projection")
    first_receipt = parse_closed(raw[COLD_RUN_A_RECEIPT], "seed1 cold receipt")
    second_receipt = parse_closed(raw[COLD_RUN_B_RECEIPT], "seed2 cold receipt")
    need(raw[COLD_RUN_A] == raw[COLD_RUN_B] and same_json(first, second) and
         first["schema"] == SCHEMA + ".cold-run-projection" and
         first["status"].startswith("PASS_COLD_RUN_PROJECTION_64_OF_64") and
         first["independence"]["cold_verifier_file_sha256"] == verifier_sha and
         first["aggregate"]["producer_file_sha256"] ==
         hashlib.sha256(raw[AGG_PRODUCER]).hexdigest() and
         first["aggregate"]["result_file_sha256"] == hashlib.sha256(raw[AGG_RESULT]).hexdigest() and
         first["aggregate"]["leaf_ledger_sha256"] == hashlib.sha256(raw[AGG_LEAVES]).hexdigest() and
         first["aggregate"]["source_summary_sha256"] == hashlib.sha256(raw[AGG_SOURCES]).hexdigest() and
         first["aggregate"]["parent_summary_sha256"] == hashlib.sha256(raw[AGG_PARENTS]).hexdigest() and
         same_json(first["aggregate"], second["aggregate"]) and
         same_json(authority_snapshot(raw), EXPECTED_AUTHORITY),
         "two isolated full cold projections byte-identical and source bound")
    for seed, path, receipt in (("1", COLD_RUN_A, first_receipt),
                                ("2", COLD_RUN_B, second_receipt)):
        need(same_json(receipt, cold_run_receipt(path, raw[path], first, seed)),
             "exact seed-specific cold run receipt:" + seed)
    body = copy.deepcopy(first)
    body.pop("object_sha256")
    body["schema"] = SCHEMA + ".verification"
    body["status"] = (
        "PASS_INDEPENDENT_DUAL_COLD_64_OF_64__20879_ASSIGNMENTS__EXACT_DEPTH6_NUMERIC_REPLAY__"
        "C61_REPLACEMENT_PARENT_KRAFT__AUTHORITY_UNCHANGED__ZERO_CREDIT"
    )
    body["dual_cold_run_evidence"] = {
        "byte_identical": True,
        "projection_file_sha256": hashlib.sha256(raw[COLD_RUN_A]).hexdigest(),
        "projection_object_sha256": first["object_sha256"],
        "seed1_receipt_object_sha256": first_receipt["object_sha256"],
        "seed2_receipt_object_sha256": second_receipt["object_sha256"],
        "pythonhashseeds": ["1", "2"],
        "verifier_file_sha256": verifier_sha,
    }
    return close(body)


def synthetic_baseline() -> dict[str, Any]:
    body = {
        "schema": SCHEMA + ".synthetic-contract", "receipt_ids": list(SHARDS),
        "controller_absent": True, "receipt_ledgers_bijective": True,
        "assignment_sources": 20879, "assignment_unique": True,
        "assignment_formula": True, "DFS_depth": 6, "numeric_rows_exact": True,
        "source_prefix_free": True, "source_Kraft": True,
        "C61_carry": 23997, "selected_removed_before_children": True,
        "parent_count": 12, "parent_prefix_free": True, "parent_Kraft": True,
        "authority_snapshot_object_sha256": PIN["authority_snapshot_object"],
        "effective_checkpoint_object_sha256": PIN["effective_checkpoint_object"],
        "C69_consumed": False, "formal_credit": 0, "whole_parent_credit": 0,
        "D02_gate_credit": 0, "runtime_write": False,
    }
    return close(body)


def validate_synthetic(value: dict[str, Any], baseline: dict[str, Any]) -> None:
    need(type(value) is dict and set(value) == set(baseline), "synthetic exact key set")
    body = copy.deepcopy(value)
    claim = body.pop("object_sha256", None)
    need(claim == digest(body) and same_json(value, baseline), "synthetic exact closed baseline")


def expect_reject(tests: dict[str, bool], name: str, action: Callable[[], Any]) -> None:
    try:
        action()
    except (Rejected, OSError, ValueError, zlib.error):
        tests[name] = True
    else:
        tests[name] = False


def gzip_fixture(rows: list[dict[str, Any]]) -> tuple[bytes, dict[str, Any]]:
    import gzip  # stdlib fixture writer only; never used for production verification
    payload = b"".join(canonical(row) + b"\n" for row in rows)
    compressed = gzip.compress(payload, compresslevel=6, mtime=0)
    sequence = hashlib.sha256(
        "".join(row["row_sha256"] + "\n" for row in rows).encode("ascii")
    ).hexdigest()
    return compressed, {
        "filename": "fixture.jsonl.gz", "order": "FIXTURE_ORDER", "row_count": len(rows),
        "row_hash_line_sequence_sha256": sequence,
        "sha256": hashlib.sha256(compressed).hexdigest(), "size": len(compressed),
    }


def self_test() -> dict[str, Any]:
    baseline = synthetic_baseline()
    validate_synthetic(baseline, baseline)
    tests: dict[str, bool] = {"baseline_valid": True}
    mutations: list[tuple[str, Any]] = [
        ("receipt_ids", list(range(63))), ("controller_absent", False),
        ("receipt_ledgers_bijective", False), ("assignment_sources", 20878),
        ("assignment_unique", False), ("assignment_formula", False), ("DFS_depth", 5),
        ("numeric_rows_exact", False), ("source_prefix_free", False),
        ("source_Kraft", False), ("C61_carry", 23996),
        ("selected_removed_before_children", False), ("parent_count", 11),
        ("parent_prefix_free", False), ("parent_Kraft", False),
        ("authority_snapshot_object_sha256", "0" * 64),
        ("effective_checkpoint_object_sha256", "0" * 64), ("C69_consumed", True),
        ("formal_credit", 1), ("whole_parent_credit", 1), ("D02_gate_credit", 1),
        ("runtime_write", True),
    ]
    for field, replacement in mutations:
        attacked = copy.deepcopy(baseline)
        attacked.pop("object_sha256")
        attacked[field] = replacement
        attacked = close(attacked)
        expect_reject(tests, "coherent_" + field + "_rejected",
                      lambda attacked=attacked: validate_synthetic(attacked, baseline))

    # Python normally accepts bool as an int; these attacks exercise the
    # verifier's explicit type-sensitive integer boundaries.
    for name, expected in (
        ("credit", 0), ("row_count", 1), ("depth", 6),
        ("shard_id", 0), ("next_collision_index", 2),
    ):
        expect_reject(tests, "coherent_bool_for_int_" + name + "_rejected",
                      lambda expected=expected, name=name: exact_int(True, expected, name))
    tests["type_sensitive_JSON_bool_differs_from_int"] = not same_json({"x": True}, {"x": 1})

    malformed = {
        "BOM": b"\xef\xbb\xbf{}\n", "duplicate_key": b'{"a":1,"a":2}\n',
        "NaN": b'{"a":NaN}\n', "Infinity": b'{"a":Infinity}\n',
        "float": b'{"a":1.25}\n', "trailing": b'{}\nX', "missing_newline": b'{}',
        "noncanonical": b'{ "a" : 1 }\n',
    }
    for name, payload in malformed.items():
        expect_reject(tests, name + "_rejected",
                      lambda payload=payload, name=name: parse(payload, name, True))

    row_body = {"schema": "fixture.row", "value": 1}
    fixture_row = {**row_body, "row_sha256": digest(row_body)}
    gzip_raw, descriptor = gzip_fixture([fixture_row])
    need(list(iter_ledger(gzip_raw, descriptor, "valid fixture", expanded_limit=1 << 20)) ==
         [fixture_row], "valid gzip fixture")
    tests["valid_single_member_gzip"] = True

    def attacked_ledger(payload: bytes, changed: dict[str, Any] | None = None,
                        limit: int = 1 << 20) -> list[dict[str, Any]]:
        candidate = copy.deepcopy(descriptor if changed is None else changed)
        candidate["sha256"] = hashlib.sha256(payload).hexdigest()
        candidate["size"] = len(payload)
        return list(iter_ledger(payload, candidate, "attacked fixture", expanded_limit=limit))

    for name, payload in {
        "truncated_gzip": gzip_raw[:-3], "concatenated_gzip": gzip_raw + gzip_raw,
        "gzip_trailing_junk": gzip_raw + b"JUNK",
    }.items():
        expect_reject(tests, name + "_rejected",
                      lambda payload=payload: attacked_ledger(payload))
    oversized_raw, oversized_desc = gzip_fixture([
        {**{"schema": "fixture.row", "value": "x" * 4096},
         "row_sha256": digest({"schema": "fixture.row", "value": "x" * 4096})}
    ])
    expect_reject(tests, "oversized_gzip_rejected",
                  lambda: list(iter_ledger(oversized_raw, oversized_desc, "oversized", expanded_limit=64)))
    wrong_descriptor = copy.deepcopy(descriptor)
    wrong_descriptor["row_count"] = 2
    expect_reject(tests, "descriptor_count_rejected",
                  lambda: attacked_ledger(gzip_raw, wrong_descriptor))
    wrong_descriptor = copy.deepcopy(descriptor)
    wrong_descriptor["row_hash_line_sequence_sha256"] = "0" * 64
    expect_reject(tests, "descriptor_sequence_rejected",
                  lambda: attacked_ledger(gzip_raw, wrong_descriptor))

    with tempfile.TemporaryDirectory(prefix="cm2-c65-aggregate-cold-") as temporary:
        root = Path(temporary)
        target = root / "target"
        target.write_bytes(canonical(baseline) + b"\n")
        link = root / "link"
        link.symlink_to(target.name)
        expect_reject(tests, "symlink_rejected", lambda: capture((link,)))
        hard = root / "hard"
        os.link(target, hard)
        expect_reject(tests, "hardlink_rejected", lambda: capture((target,)))
        hard.unlink()
        fifo = root / "fifo"
        os.mkfifo(fifo)
        expect_reject(tests, "FIFO_rejected", lambda: capture((fifo,)))
        replacement = root / "replacement"
        replacement.write_bytes(canonical(baseline) + b"\n")
        expect_reject(tests, "TOCTOU_inode_replacement_rejected",
                      lambda: capture((target,), hook=lambda: os.replace(replacement, target)))
        missing = root / "missing"
        expect_reject(tests, "missing_file_rejected", lambda: capture((missing,)))

        receipt_dir = root / "receipts"
        receipt_dir.mkdir()
        for shard in range(63):
            (receipt_dir /
             f"cm2_round306c65s18_depth18_64shard_shard_{shard:02d}_receipt_v3.json").write_text(
                 "{}\n", encoding="utf-8")
        ledger_sentinel = receipt_dir / "ledger-sentinel"
        ledger_sentinel.write_text("must-not-open\n", encoding="utf-8")
        expect_reject(tests, "63_receipt_barrier_rejected",
                      lambda: receipt_barrier(receipt_dir))
        tests["63_receipt_barrier_did_not_open_ledger"] = ledger_sentinel.read_text(
            encoding="utf-8") == "must-not-open\n"
        final = receipt_dir / "cm2_round306c65s18_depth18_64shard_shard_63_receipt_v3.json"
        final.write_text("{}\n", encoding="utf-8")
        tests["64_receipt_barrier_accepts_exact_ids"] = len(receipt_barrier(receipt_dir)) == 64
        extra = receipt_dir / "cm2_round306c65s18_depth18_64shard_shard_64_receipt_v3.json"
        extra.write_text("{}\n", encoding="utf-8")
        expect_reject(tests, "65_receipt_barrier_rejected", lambda: receipt_barrier(receipt_dir))

        output = root / "exclusive.json"
        publish_json(output, baseline)
        expect_reject(tests, "no_replace_existing_output_rejected",
                      lambda: publish_json(output, baseline))

    # Static policy tests guard against future accidental producer imports or
    # execution even before a formal 64/64 run exists.
    self_source = SELF.read_bytes()
    self_tree = ast.parse(self_source.decode("utf-8", "strict"), filename=SELF.name)
    imported = {
        alias.name for node in ast.walk(self_tree) if isinstance(node, ast.Import)
        for alias in node.names
    } | {
        str(node.module) for node in ast.walk(self_tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    forbidden = {EXECUTOR.stem, CONTROLLER.stem, CHECKER.stem, AGG_PRODUCER.stem}
    tests["no_C65_program_import_in_verifier_AST"] = not (imported & forbidden)
    tests["formal_output_absent_before_64_of_64"] = not VERIFY_OUT.exists()
    tests["aggregate_outputs_not_required_by_selftest"] = True
    tests["controller_checker_executor_pins_concrete"] = all(
        HEX64.fullmatch(PIN[key]) is not None
        for key in ("executor_file", "controller_file", "checker_file")
    )
    tests["C41_auditor_delayed_until_authenticated_kernel"] = C41_MODULE not in sys.modules

    need(all(tests.values()) and len(tests) >= 50,
         f"hostile self-test completeness:{sum(tests.values())}/{len(tests)}")
    return close({
        "schema": SCHEMA + ".self-test",
        "status": f"PASS_{len(tests)}_OF_{len(tests)}_EXECUTED_COHERENT_FILE_TOCTOU_GZIP_AND_RECEIPT_BARRIER_ATTACKS",
        "verifier_file_sha256": hashlib.sha256(SELF.read_bytes()).hexdigest(),
        "supersedes_terminally_rejected_self_test_v1": {
            "file_sha256": "babd294faeaea9db0e5433527ad3a4688f3b22ae8ab053fbd0400feb10c3ce2b",
            "object_sha256": "90f1b65d2b0361b3116919235d081430603cfff53e7aa63d646c7a8dc7422dca",
            "rejection_marker": REJECTED_SELFTEST_V1_MARKER.name,
        },
        "tests": tests, "test_count": len(tests),
        "synthetic_is_authority": False, "formal_credit": 0,
        "whole_parent_credit": 0, "D02_gate_credit": 0,
        "runtime_canonical_pointer_or_seal_writes": False,
    })


def publish_json(path: Path, value: dict[str, Any]) -> None:
    raw = canonical(value) + b"\n"
    parent = Path(os.path.abspath(os.fspath(path.parent)))
    directory = os.open(parent, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try:
        flags = (os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
        fd = os.open(path.name, flags, 0o644, dir_fd=directory)
        try:
            view = memoryview(raw)
            while view:
                written = os.write(fd, view)
                need(written > 0, "short publication write")
                view = view[written:]
            os.fsync(fd)
            state = os.fstat(fd)
            current = os.stat(path.name, dir_fd=directory, follow_symlinks=False)
            need(stat.S_ISREG(state.st_mode) and state.st_nlink == 1 and
                 fingerprint(state) == fingerprint(current), "publication fd/path identity")
            os.lseek(fd, 0, os.SEEK_SET)
            replay = b""
            while block := os.read(fd, 1 << 20):
                replay += block
            need(replay == raw and fingerprint(os.fstat(fd)) == fingerprint(state),
                 "publication terminal-byte replay")
            os.fsync(directory)
        finally:
            os.close(fd)
    finally:
        os.close(directory)


def release_manifest_members() -> tuple[Path, ...]:
    return (
        SELF, AGG_PRODUCER, AGG_RESULT, AGG_LEAVES, AGG_SOURCES, AGG_PARENTS,
        CONTRACT, ASSIGNMENT, INVENTORY, AUTHORIZATION, C61_RESULT, C61_LEAVES,
        C58_RESULT, C58_LEAVES, C40_RESULT, C40_ROUTED,
        C41_AUDITOR, C40_AUDITOR, C39_KERNEL, ROUND139, ROUND166, ROUND185, ROUND181, ROUND178,
        EXECUTOR, CONTROLLER, CHECKER,
        CANONICAL, CANONICAL_COMPANION, GLOBAL_HEAD, GLOBAL_CLAIM, C53_TOKEN, C53_AUDIT_TOKEN,
        *(receipt_path(shard) for shard in SHARDS),
        *(shard_ledger_path(shard) for shard in SHARDS),
        COLD_RUN_A, COLD_RUN_A_RECEIPT, COLD_RUN_B, COLD_RUN_B_RECEIPT,
        VERIFY_OUT, SELFTEST_OUT, REPLAY_OUT, REJECTED_SELFTEST_V1,
        REJECTED_SELFTEST_V1_MARKER,
    )


def publish_manifest(path: Path, members: Iterable[Path]) -> None:
    ordered = tuple(members)
    payloads = capture(ordered)
    lines: list[str] = []
    for member in ordered:
        lines.append(hashlib.sha256(payloads[member]).hexdigest() + "  " + member.name + "\n")
    raw = "".join(lines).encode("ascii")
    parent = Path(os.path.abspath(os.fspath(path.parent)))
    directory = os.open(parent, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try:
        fd = os.open(path.name, os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC |
                     getattr(os, "O_NOFOLLOW", 0), 0o644, dir_fd=directory)
        try:
            view = memoryview(raw)
            while view:
                written = os.write(fd, view)
                need(written > 0, "short manifest write")
                view = view[written:]
            os.fsync(fd)
            before = os.fstat(fd)
            current = os.stat(path.name, dir_fd=directory, follow_symlinks=False)
            need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and
                 fingerprint(before) == fingerprint(current), "manifest fd/path identity")
            os.lseek(fd, 0, os.SEEK_SET)
            replay = b""
            while block := os.read(fd, 1 << 20):
                replay += block
            need(replay == raw, "manifest byte replay")
            os.fsync(directory)
        finally:
            os.close(fd)
    finally:
        os.close(directory)


def postpublication_replay(verification: dict[str, Any], selftest: dict[str, Any]) -> dict[str, Any]:
    verification_raw = capture((VERIFY_OUT,), maximum=32 << 20)[VERIFY_OUT]
    selftest_raw = capture((SELFTEST_OUT,), maximum=32 << 20)[SELFTEST_OUT]
    observed_verification = parse_closed(verification_raw, "published verification")
    observed_selftest = parse_closed(selftest_raw, "published self-test")
    need(same_json(observed_verification, verification) and same_json(observed_selftest, selftest),
         "published verification/self-test semantic byte replay")
    need(observed_verification["status"].startswith("PASS_INDEPENDENT_DUAL_COLD_64_OF_64") and
         observed_selftest["status"].startswith("PASS_") and
         observed_verification["formal_credit"] ==
         observed_verification["whole_parent_credit"] ==
         observed_verification["D02_gate_credit"] == 0 and
         observed_selftest["formal_credit"] == observed_selftest["whole_parent_credit"] ==
         observed_selftest["D02_gate_credit"] == 0 and
         observed_selftest["verifier_file_sha256"] == hashlib.sha256(SELF.read_bytes()).hexdigest(),
         "published PASS status/zero credit")
    zero_credits(observed_verification, "published verification")
    zero_credits(observed_selftest, "published self-test")
    need(not controller_running(), "controller absent during post-publication replay")
    shard_name_snapshot(OUT)
    return close({
        "schema": SCHEMA + ".postpublication-replay",
        "status": "PASS_POSTPUBLICATION_TERMINAL_BYTE_REPLAY__CONTROLLER_ABSENT__ZERO_CREDIT",
        "verification_file_sha256": hashlib.sha256(verification_raw).hexdigest(),
        "verification_object_sha256": verification["object_sha256"],
        "self_test_file_sha256": hashlib.sha256(selftest_raw).hexdigest(),
        "self_test_object_sha256": selftest["object_sha256"],
        "manifest_published_after_this_replay": True,
        "candidate_is_authority": False, "formal_credit": 0,
        "whole_parent_credit": 0, "D02_gate_credit": 0,
        "runtime_canonical_pointer_or_seal_writes": False,
    })


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--compute", action="store_true")
    group.add_argument("--install-verification", action="store_true")
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--publish-self-test", action="store_true")
    group.add_argument("--release", action="store_true")
    args = parser.parse_args()
    try:
        if args.compute:
            value = verify()
            seed = os.environ.get("PYTHONHASHSEED")
            need(seed in {"1", "2"}, "--compute requires PYTHONHASHSEED exactly 1 or 2")
            projection_path = COLD_RUN_A if seed == "1" else COLD_RUN_B
            receipt_path_for_seed = COLD_RUN_A_RECEIPT if seed == "1" else COLD_RUN_B_RECEIPT
            projection_raw = canonical(value) + b"\n"
            publish_json(projection_path, value)
            publish_json(receipt_path_for_seed,
                         cold_run_receipt(projection_path, projection_raw, value, seed))
        elif args.install_verification:
            value = install_dual_run_verification()
            publish_json(VERIFY_OUT, value)
        elif args.self_test or args.publish_self_test:
            value = self_test()
            if args.publish_self_test:
                publish_json(SELFTEST_OUT, value)
        else:
            # Release deliberately requires separately published verification
            # and self-test outputs, then freezes replay followed by manifest.
            verification = parse_closed(capture((VERIFY_OUT,), maximum=32 << 20)[VERIFY_OUT],
                                        "release verification")
            selftest = parse_closed(capture((SELFTEST_OUT,), maximum=32 << 20)[SELFTEST_OUT],
                                    "release self-test")
            value = postpublication_replay(verification, selftest)
            publish_json(REPLAY_OUT, value)
            publish_manifest(MANIFEST_OUT, release_manifest_members())
        print(json.dumps({"status": value["status"], "object_sha256": value["object_sha256"]},
                         sort_keys=True, separators=(",", ":")))
        return 0
    except (AwaitingCompleteReceipts, Rejected, OSError, KeyError, TypeError, ValueError,
            zlib.error) as error:
        print(json.dumps({"status": "FAIL_CLOSED", "reason": str(error)},
                         sort_keys=True, separators=(",", ":")))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
