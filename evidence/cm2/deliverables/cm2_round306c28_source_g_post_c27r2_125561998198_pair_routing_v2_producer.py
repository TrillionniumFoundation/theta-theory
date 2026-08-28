#!/usr/bin/env python3
"""Build the append-only C28-v2 mathematical pair-routing candidate.

This core deliberately does not mint C28.  It consumes only a future,
externally pinned C27R2 terminal graph and the two terminal-pinned quotient
ledgers ``member_to_post_component`` and ``post_component_census``.  It never
reads the historical C15 partition authority, the old C27 frontier/family, or
the old C28 result.

The exact C27R2 terminal receipt schema is intentionally not guessed here.
At release time an independently reviewed, externally SHA-pinned adapter
contract must bind the minted terminal receipt fields and payload paths.  A
missing or still-pending terminal therefore rejects before the output
directory is created.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()

CONTRACT_SCHEMA = (
    "cm2.round306c28.source-g.c27r2-terminal-adapter-contract.v1"
)
CONTRACT_READY = (
    "FINALIZED_FROM_MINTED_C27R2_TERMINAL__C28_MATH_CORE_MAY_RUN__"
    "ZERO_C28_CREDIT"
)
C27R2_RESULT_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "producer-result.v1"
)
C27R2_RESULT_STATUS = (
    "PASS_FRESH_ACTUAL_V2_SEED1_QUOTIENT_REBUILD_ZERO_CREDIT__PENDING_"
    "NO_IMPORT_SEED2_VERIFICATION_ATTACKS_COLD_REPLAY_AND_TERMINAL_SEAL"
)
MEMBER_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "member-to-post-component-row.v1"
)
CENSUS_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "post-component-census-row.v1"
)
BLOCK_SCHEMA = (
    "cm2.round306c28.source-g-post-c27r2-125561998198-pair-routing.v2."
    "member-home-block-census-row.v1"
)
ROUTE_SCHEMA = (
    "cm2.round306c28.source-g-post-c27r2-125561998198-pair-routing.v2."
    "cross-component-pair-route-shard-row.v1"
)
RESULT_SCHEMA = (
    "cm2.round306c28.source-g-post-c27r2-125561998198-pair-routing.v2."
    "producer-result.v1"
)
RESULT_STATUS = (
    "PASS_POST_C27R2_PARTITION_502204_MEMBERS_43684_COMPONENTS_AND_"
    "32896_PAIR_SHARDS_REBUILT__125561998198_EXACT_NONEDGE_CANDIDATE_"
    "ZERO_CREDIT__C28_UNAUTHORIZED_PENDING_RELEASE_TERMINAL"
)
BLOCK_FILE = "member_home_block_census.jsonl.gz"
ROUTE_FILE = "cross_component_pair_route_shard.jsonl.gz"
RESULT_FILE = "result.json"
EXPECTED = {
    "members": 502_204,
    "post_components": 43_684,
    "total_pairs": 126_104_177_706,
    "within_pairs": 542_179_508,
    "cross_pairs": 125_561_998_198,
    "blocks": 256,
    "shards": 32_896,
}
EXPECTED_C27R2_CENSUS = {
    "frozen_C15_members": 502_204,
    "frozen_C15_components": 57_876,
    "proof_derived_component_edges": 14_860,
    "successful_DSU_merges": 14_192,
    "cycle_edges": 668,
    "post_C27R2_components": 43_684,
    "total_unordered_member_pairs": 126_104_177_706,
    "within_post_component_member_pairs": 542_179_508,
    "cross_post_component_member_pairs": 125_561_998_198,
}
SEMANTIC_ROLES = {
    "c27r2_terminal_passed",
    "complete_actual_v2_edge_complement_after_quotient",
    "c28_fresh_rebuild_only",
    "c28_formal_credit_zero",
    "c29_unauthorized",
    "cm2_no_go",
}


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def valid_sha(value: Any) -> bool:
    return (
        type(value) is str and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def strict_load(payload: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in items:
            need(key not in output, "duplicate JSON key:" + key)
            output[key] = value
        return output

    def constant(value: str) -> None:
        raise Failure("non-finite JSON:" + value)

    return json.loads(payload, object_pairs_hook=pairs, parse_constant=constant)


def workspace_path(raw: str | Path, *, may_not_exist: bool = False) -> Path:
    supplied = Path(raw)
    value = (ROOT / supplied if not supplied.is_absolute() else supplied).absolute()
    try:
        relative = value.relative_to(ROOT)
    except ValueError as error:
        raise Failure("path outside workspace:" + str(raw)) from error
    need(all(piece not in {"", ".", ".."} for piece in relative.parts),
         "canonical workspace path:" + str(raw))
    current = ROOT
    for piece in relative.parts:
        current = current / piece
        if not current.exists():
            need(may_not_exist is True,
                 "missing path component:" + str(current))
            break
        need(not current.is_symlink(), "symlink path component:" + str(current))
    return value


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fingerprint(info: os.stat_result) -> list[int]:
    return [
        info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size,
        info.st_mtime_ns, info.st_ctime_ns, info.st_uid, info.st_gid,
    ]


class Capture:
    """A stable single-open-file-description input capture."""

    def __init__(self, path: Path, label: str):
        self.path = workspace_path(path)
        self.label = label
        self.fd = os.open(
            self.path,
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0),
        )
        self.before = os.fstat(self.fd)
        need(stat.S_ISREG(self.before.st_mode), label + ":regular")
        need(self.before.st_nlink == 1, label + ":single-link")
        self.sha256 = self._hash()

    def _rewind(self) -> None:
        os.lseek(self.fd, 0, os.SEEK_SET)

    def _hash(self) -> str:
        self._rewind()
        state = hashlib.sha256()
        while block := os.read(self.fd, 4 << 20):
            state.update(block)
        self._rewind()
        need(fingerprint(os.fstat(self.fd)) == fingerprint(self.before),
             self.label + ":stable-after-hash")
        return state.hexdigest()

    def bytes(self) -> bytes:
        self._rewind()
        blocks: list[bytes] = []
        while block := os.read(self.fd, 4 << 20):
            blocks.append(block)
        self._rewind()
        need(fingerprint(os.fstat(self.fd)) == fingerprint(self.before),
             self.label + ":stable-after-read")
        return b"".join(blocks)

    def document(self, closure_key: str | None = None) -> Any:
        payload = self.bytes()
        need(payload.endswith(b"\n") and not payload.endswith(b"\n\n"),
             self.label + ":one terminal newline")
        value = strict_load(payload[:-1])
        need(type(value) is dict and canonical(value) == payload[:-1],
             self.label + ":canonical object")
        if closure_key is not None:
            body = dict(value)
            claimed = body.pop(closure_key, None)
            need(valid_sha(claimed) and claimed == digest(body),
                 self.label + ":object closure")
        return value

    def gzip_rows(self) -> Iterator[tuple[int, dict[str, Any]]]:
        raw = self.bytes()
        need(len(raw) >= 10 and raw[:2] == b"\x1f\x8b"
             and int.from_bytes(raw[4:8], "little") == 0,
             self.label + ":gzip header/mtime0")
        try:
            with gzip.GzipFile(fileobj=io.BytesIO(raw), mode="rb") as stream:
                for ordinal, line in enumerate(stream):
                    need(line.endswith(b"\n"), self.label + ":row newline")
                    value = strict_load(line[:-1])
                    need(type(value) is dict and canonical(value) == line[:-1],
                         self.label + f":canonical row:{ordinal}")
                    body = dict(value)
                    claimed = body.pop("row_sha256", None)
                    need(valid_sha(claimed) and claimed == digest(body),
                         self.label + f":row closure:{ordinal}")
                    yield ordinal, value
        except (gzip.BadGzipFile, EOFError) as error:
            raise Failure(self.label + ":gzip") from error

    def attestation(self) -> dict[str, Any]:
        return {
            "path": relative(self.path),
            "sha256": self.sha256,
            "size": self.before.st_size,
            "stat_fingerprint": fingerprint(self.before),
            "O_NOFOLLOW": True,
            "single_open_file_description_hash_parse_fstat": True,
        }

    def assert_stable(self) -> None:
        need(self._hash() == self.sha256
             and fingerprint(os.fstat(self.fd)) == fingerprint(self.before),
             self.label + ":pre/post SHA/stat")

    def close(self) -> None:
        os.close(self.fd)


def parse_manifest(capture: Capture) -> dict[str, str]:
    entries: dict[str, str] = {}
    payload = capture.bytes()
    need(payload.endswith(b"\n"), capture.label + ":manifest newline")
    try:
        text = payload.decode("ascii")
    except UnicodeDecodeError as error:
        raise Failure(capture.label + ":manifest ASCII") from error
    for ordinal, line in enumerate(text.splitlines()):
        pieces = line.split(None, 1)
        need(len(pieces) == 2 and valid_sha(pieces[0]),
             capture.label + f":manifest line:{ordinal}")
        name = pieces[1].strip()
        need(name == pieces[1] and name not in entries and name != "",
             capture.label + f":manifest entry:{ordinal}")
        path = Path(name)
        need(not path.is_absolute()
             and all(piece not in {"", ".", ".."} for piece in path.parts),
             capture.label + f":manifest safe path:{ordinal}")
        entries[name] = pieces[0]
    need(len(entries) > 0, capture.label + ":nonempty manifest")
    need(list(entries) == sorted(entries),
         capture.label + ":manifest lexical order")
    return entries


def json_path(value: Any, path: Any, label: str) -> Any:
    need(type(path) is list and len(path) > 0
         and all(type(piece) is str and piece != "" for piece in path),
         label + ":JSON path")
    current = value
    for piece in path:
        need(type(current) is dict and piece in current,
             label + ":missing JSON path segment:" + piece)
        current = current[piece]
    return current


def validate_contract(value: Any) -> None:
    need(type(value) is dict, "adapter contract object")
    need(set(value) == {
        "schema", "status", "terminal", "payload", "semantic_bindings",
        "review", "contract_sha256",
    }, "adapter contract exact keys")
    need(value.get("schema") == CONTRACT_SCHEMA
         and value.get("status") == CONTRACT_READY,
         "adapter contract finalized status")
    terminal = value.get("terminal")
    payload = value.get("payload")
    bindings = value.get("semantic_bindings")
    review = value.get("review")
    need(type(terminal) is dict and set(terminal) == {
        "terminal_dir", "root_manifest_filename", "payload_manifest_filename",
        "receipt_filename", "pass_lock_filename", "pass_lock_ascii",
        "root_payload_entry", "root_receipt_entry", "root_manifest_sha256",
        "payload_manifest_sha256", "receipt_file_sha256",
        "receipt_object_sha256", "receipt_closure_key", "receipt_schema",
        "receipt_status",
    }, "adapter terminal exact keys")
    for key in (
        "terminal_dir", "root_manifest_filename", "payload_manifest_filename",
        "receipt_filename", "pass_lock_filename", "pass_lock_ascii",
        "root_payload_entry", "root_receipt_entry", "receipt_closure_key",
        "receipt_schema", "receipt_status",
    ):
        need(type(terminal[key]) is str and terminal[key] != "",
             "adapter terminal string:" + key)
    file_fields = (
        "root_manifest_filename", "payload_manifest_filename",
        "receipt_filename", "pass_lock_filename",
    )
    need(all(Path(terminal[key]).name == terminal[key]
             for key in file_fields)
         and len({terminal[key] for key in file_fields}) == len(file_fields),
         "adapter distinct terminal basenames")
    need(terminal["root_payload_entry"]
             != terminal["root_receipt_entry"],
         "adapter distinct terminal root entries")
    for key in (
        "root_manifest_sha256", "payload_manifest_sha256",
        "receipt_file_sha256", "receipt_object_sha256",
    ):
        need(valid_sha(terminal[key]), "adapter terminal hash:" + key)
    need("\n" not in terminal["pass_lock_ascii"]
         and "\r" not in terminal["pass_lock_ascii"],
         "adapter PASS lock single line")
    need(type(payload) is dict and set(payload) == {
        "producer_result", "member_to_post_component", "post_component_census",
    }, "adapter payload exact roles")
    for role, descriptor in payload.items():
        need(type(descriptor) is dict and set(descriptor) == {
            "path", "sha256", "size", "row_count", "result_sha256",
        }, "adapter payload descriptor keys:" + role)
        need(type(descriptor["path"]) is str and descriptor["path"] != ""
             and valid_sha(descriptor["sha256"])
             and type(descriptor["size"]) is int and descriptor["size"] > 0,
             "adapter payload descriptor:" + role)
        expected_rows = {
            "producer_result": 0,
            "member_to_post_component": EXPECTED["members"],
            "post_component_census": EXPECTED["post_components"],
        }[role]
        need(descriptor["row_count"] == expected_rows,
             "adapter payload row count:" + role)
        if role == "producer_result":
            need(valid_sha(descriptor["result_sha256"]),
                 "adapter producer result object")
        else:
            need(descriptor["result_sha256"] is None,
                 "adapter ledger no result object:" + role)
    need(len({descriptor["path"] for descriptor in payload.values()}) == 3,
         "adapter distinct selected payload paths")
    need(type(bindings) is dict and set(bindings) == SEMANTIC_ROLES,
         "adapter semantic roles")
    seen_paths: set[tuple[str, ...]] = set()
    for role, binding in bindings.items():
        need(type(binding) is dict and set(binding) == {"path", "expected"},
             "adapter semantic binding keys:" + role)
        path = binding["path"]
        need(type(path) is list and len(path) > 0
             and all(type(piece) is str and piece != "" for piece in path),
             "adapter semantic path:" + role)
        key = tuple(path)
        need(key not in seen_paths, "adapter semantic distinct paths")
        seen_paths.add(key)
        canonical(binding["expected"])
    need(review == {
        "C27R2_terminal_authority_reviewed": True,
        "complete_actual_v2_edge_complement_reviewed": True,
        "C28_math_core_may_start": True,
        "C28_formal_credit_minted": False,
        "C29_authorized": False,
        "CM2": "NO-GO_FOR_CLAIM",
        "pending_fields_were_filled_only_after_terminal_mint": True,
    }, "adapter exact review boundary")


def validate_c27r2_result(
    result: dict[str, Any], member: Capture, census: Capture,
    contract: dict[str, Any],
) -> None:
    need(set(result) == {
        "C27R2", "C28_C29", "CM2", "Source_W", "authority",
        "canonical_post_component_id_formula", "derivation_closures",
        "edge_row_sequence_sha256", "exact_census", "formal_credit",
        "input_pre_post_attestations", "ledgers", "manifest_authorized",
        "producer_source_attestation", "producer_source_sha256",
        "result_sha256", "schema", "status",
    }, "C27R2 producer result exact keys")
    need(result.get("schema") == C27R2_RESULT_SCHEMA
         and result.get("status") == C27R2_RESULT_STATUS,
         "C27R2 producer result contract")
    need(result.get("exact_census") == EXPECTED_C27R2_CENSUS,
         "C27R2 exact quotient census")
    need(result.get("formal_credit") == 0
         and result.get("manifest_authorized") is False
         and result.get("C27R2")
             == "UNAUTHORIZED_PENDING_INDEPENDENT_VERIFICATION_AND_TERMINAL_SEAL"
         and result.get("C28_C29") == "UNAUTHORIZED"
         and result.get("CM2") == "NO-GO_FOR_CLAIM",
         "C27R2 candidate nonpromotion boundary")
    need(result.get("Source_W")
             == "UNCHANGED_BY_SOURCE_G_REBUILD_CANDIDATE"
         and result.get("canonical_post_component_id_formula") == (
             "round306c27r2-source-g-post-component:SHA256(canonical JSON "
             "sorted list of old C15 component IDs)"
         )
         and result.get("derivation_closures") == {
             "DSU_started_from_all_57876_frozen_C15_components": True,
             "all_502204_members_rebound_through_frozen_C15": True,
             "old_C27_C28_C29_partition_imported_or_read": False,
             "only_terminal_pinned_actual_v2_seed1_edges_applied": True,
             "pair_identity_total_equals_within_plus_cross": True,
             "post_component_ID_never_uses_DSU_root": True,
         }
         and valid_sha(result.get("edge_row_sequence_sha256"))
         and valid_sha(result.get("producer_source_sha256"))
         and type(result.get("authority")) is dict
         and type(result.get("input_pre_post_attestations")) is dict
         and type(result.get("producer_source_attestation")) is dict
         and result["producer_source_attestation"].get("sha256")
             == result["producer_source_sha256"],
         "C27R2 exact derivation/source contract")
    ledgers = result.get("ledgers")
    need(type(ledgers) is dict and set(ledgers) == {
        "old_C15_component_to_post_component", "member_to_post_component",
        "post_component_census",
    }, "C27R2 ledger descriptors")
    selected = {
        "member_to_post_component": (member, MEMBER_SCHEMA, EXPECTED["members"],
                                      ["member_ordinal"], "registry_member_id"),
        "post_component_census": (census, CENSUS_SCHEMA,
                                  EXPECTED["post_components"],
                                  ["post_C27R2_component_id"],
                                  "post_C27R2_component_id"),
    }
    for role, (capture, schema, count, ordering, unique_key) in selected.items():
        descriptor = ledgers.get(role)
        adapter = contract["payload"][role]
        need(type(descriptor) is dict
             and descriptor.get("filename") == capture.path.name
             and descriptor.get("sha256") == capture.sha256
             and descriptor.get("size") == capture.before.st_size
             and descriptor.get("row_count") == count
             and descriptor.get("row_schema") == schema
             and descriptor.get("ordering") == ordering
             and descriptor.get("unique_key") == unique_key
             and descriptor.get("gzip_mtime") == 0
             and descriptor.get("canonical_jsonl") is True
             and descriptor.get("row_closure")
                 == "row_sha256=SHA256(canonical row without row_sha256)"
             and valid_sha(descriptor.get("row_sequence_sha256")),
             "C27R2 ledger descriptor:" + role)
        need(adapter["path"] == relative(capture.path)
             and adapter["sha256"] == capture.sha256
             and adapter["size"] == capture.before.st_size,
             "adapter/C27R2 ledger descriptor:" + role)


def load_authority(args: argparse.Namespace) -> tuple[
    dict[str, Any], dict[str, Any], Capture, Capture, list[Capture], dict[str, Any]
]:
    need(all(valid_sha(value) for value in (
        args.expect_authority_contract_sha256,
        args.expect_terminal_root_sha256,
        args.expect_terminal_receipt_file_sha256,
        args.expect_terminal_receipt_object_sha256,
    )), "all external authority hashes")
    terminal_dir = workspace_path(args.c27r2_terminal_dir)
    contract_cap = Capture(workspace_path(args.authority_contract),
                           "authority-contract")
    captures: list[Capture] = [contract_cap]
    try:
        need(contract_cap.sha256 == args.expect_authority_contract_sha256,
             "external adapter contract pin")
        contract = contract_cap.document("contract_sha256")
        validate_contract(contract)
        terminal = contract["terminal"]
        need(relative(terminal_dir) == terminal["terminal_dir"],
             "adapter terminal directory")
        need(terminal["root_manifest_sha256"]
                 == args.expect_terminal_root_sha256
             and terminal["receipt_file_sha256"]
                 == args.expect_terminal_receipt_file_sha256
             and terminal["receipt_object_sha256"]
                 == args.expect_terminal_receipt_object_sha256,
             "adapter/external terminal pins")
        root = Capture(terminal_dir / terminal["root_manifest_filename"],
                       "c27r2-terminal-root")
        captures.append(root)
        payload = Capture(terminal_dir / terminal["payload_manifest_filename"],
                          "c27r2-terminal-payload")
        captures.append(payload)
        receipt = Capture(terminal_dir / terminal["receipt_filename"],
                          "c27r2-terminal-receipt")
        captures.append(receipt)
        lock = Capture(terminal_dir / terminal["pass_lock_filename"],
                       "c27r2-terminal-PASS")
        captures.append(lock)
        need(root.sha256 == args.expect_terminal_root_sha256
             and payload.sha256 == terminal["payload_manifest_sha256"]
             and receipt.sha256 == args.expect_terminal_receipt_file_sha256,
             "terminal exact file pins")
        need(lock.bytes()
             == (terminal["pass_lock_ascii"] + "\n").encode("ascii"),
             "terminal exact PASS lock")
        root_entries = parse_manifest(root)
        need(root_entries == {
            terminal["root_payload_entry"]: payload.sha256,
            terminal["root_receipt_entry"]: receipt.sha256,
        }, "terminal exact root manifest")
        payload_entries = parse_manifest(payload)
        receipt_value = receipt.document(terminal["receipt_closure_key"])
        need(receipt_value.get(terminal["receipt_closure_key"])
                 == args.expect_terminal_receipt_object_sha256
             and receipt_value.get("schema") == terminal["receipt_schema"]
             and receipt_value.get("status") == terminal["receipt_status"],
             "terminal receipt dynamic schema/status/object")
        for role, binding in contract["semantic_bindings"].items():
            need(json_path(receipt_value, binding["path"], role)
                 == binding["expected"],
                 "terminal semantic binding:" + role)

        selected: dict[str, Capture] = {}
        for role, descriptor in contract["payload"].items():
            capture = Capture(workspace_path(descriptor["path"]),
                              "c27r2-" + role)
            captures.append(capture)
            selected[role] = capture
            need(capture.sha256 == descriptor["sha256"]
                 and capture.before.st_size == descriptor["size"]
                 and payload_entries.get(descriptor["path"])
                     == descriptor["sha256"],
                 "terminal payload selected member:" + role)
        result_value = selected["producer_result"].document("result_sha256")
        need(result_value["result_sha256"]
                 == contract["payload"]["producer_result"]["result_sha256"],
             "adapter C27R2 result object")
        validate_c27r2_result(
            result_value, selected["member_to_post_component"],
            selected["post_component_census"], contract,
        )
        summary = {
            "adapter_contract_path": relative(contract_cap.path),
            "adapter_contract_file_sha256": contract_cap.sha256,
            "adapter_contract_object_sha256": contract["contract_sha256"],
            "c27r2_terminal_dir": relative(terminal_dir),
            "c27r2_terminal_root_manifest_sha256": root.sha256,
            "c27r2_terminal_payload_manifest_sha256": payload.sha256,
            "c27r2_terminal_receipt_file_sha256": receipt.sha256,
            "c27r2_terminal_receipt_object_sha256":
                receipt_value[terminal["receipt_closure_key"]],
            "c27r2_producer_result_sha256": result_value["result_sha256"],
            "member_to_post_component_sha256":
                selected["member_to_post_component"].sha256,
            "post_component_census_sha256":
                selected["post_component_census"].sha256,
            "terminal_semantic_roles_verified": sorted(SEMANTIC_ROLES),
        }
        return (
            contract, result_value, selected["member_to_post_component"],
            selected["post_component_census"], captures, summary,
        )
    except BaseException:
        for capture in captures:
            capture.close()
        raise


def choose2(value: int) -> int:
    return value * (value - 1) // 2


def home_block(member_id: str) -> int:
    return hashlib.sha256(member_id.encode("ascii")).digest()[0]


def row_sequence(values: list[str]) -> str:
    state = hashlib.sha256()
    for value in values:
        state.update(value.encode("ascii") + b"\n")
    return state.hexdigest()


def reconstruct_partition(
    member: Capture, census: Capture, result: dict[str, Any]
) -> tuple[list[int], list[int], list[list[int]], dict[str, str]]:
    block_members = [0] * EXPECTED["blocks"]
    component_blocks: dict[str, dict[int, int]] = defaultdict(dict)
    component_members: Counter[str] = Counter()
    seen_members: set[str] = set()
    member_ids_sequence = hashlib.sha256()
    member_row_hashes: list[str] = []
    for ordinal, row in member.gzip_rows():
        need(set(row) == {
            "schema", "ordinal", "member_ordinal", "registry_member_id",
            "old_C15_component_id", "post_C27R2_component_id",
            "formal_credit", "row_sha256",
        }, f"member exact keys:{ordinal}")
        need(row.get("schema") == MEMBER_SCHEMA
             and row.get("ordinal") == ordinal
             and row.get("member_ordinal") == ordinal
             and row.get("formal_credit") == 0,
             f"member row contract:{ordinal}")
        member_id = row.get("registry_member_id")
        post = row.get("post_C27R2_component_id")
        need(type(member_id) is str and member_id != ""
             and member_id not in seen_members,
             f"unique member:{ordinal}")
        need(type(post) is str and post != "",
             f"post component ID:{ordinal}")
        need(type(row.get("old_C15_component_id")) is str
             and row["old_C15_component_id"] != "",
             f"historical old component binding:{ordinal}")
        seen_members.add(member_id)
        block = home_block(member_id)
        block_members[block] += 1
        counts = component_blocks[post]
        counts[block] = counts.get(block, 0) + 1
        component_members[post] += 1
        member_ids_sequence.update(member_id.encode("ascii") + b"\n")
        member_row_hashes.append(row["row_sha256"])
    need(len(seen_members) == EXPECTED["members"], "exact member census")
    member_descriptor = result["ledgers"]["member_to_post_component"]
    need(row_sequence(member_row_hashes)
             == member_descriptor["row_sequence_sha256"],
         "member row sequence descriptor")

    census_members: dict[str, int] = {}
    census_within: dict[str, int] = {}
    previous: str | None = None
    census_row_hashes: list[str] = []
    for ordinal, row in census.gzip_rows():
        need(set(row) == {
            "schema", "ordinal", "post_C27R2_component_id",
            "old_C15_component_count", "old_C15_component_ids_sha256",
            "member_count", "within_member_pair_count", "formal_credit",
            "row_sha256",
        }, f"census exact keys:{ordinal}")
        need(row.get("schema") == CENSUS_SCHEMA
             and row.get("ordinal") == ordinal
             and row.get("formal_credit") == 0,
             f"census row contract:{ordinal}")
        post = row.get("post_C27R2_component_id")
        count = row.get("member_count")
        within = row.get("within_member_pair_count")
        need(type(post) is str and post != ""
             and (previous is None or previous < post)
             and post not in census_members,
             f"census strict post ID:{ordinal}")
        need(type(count) is int and count > 0
             and type(within) is int and within == choose2(count),
             f"census count/pairs:{ordinal}")
        need(type(row.get("old_C15_component_count")) is int
             and row["old_C15_component_count"] > 0
             and valid_sha(row.get("old_C15_component_ids_sha256")),
             f"census historical closure:{ordinal}")
        previous = post
        census_members[post] = count
        census_within[post] = within
        census_row_hashes.append(row["row_sha256"])
    need(len(census_members) == EXPECTED["post_components"],
         "exact post-component census")
    census_descriptor = result["ledgers"]["post_component_census"]
    need(row_sequence(census_row_hashes)
             == census_descriptor["row_sequence_sha256"],
         "census row sequence descriptor")
    need(set(census_members) == set(component_members)
         and all(component_members[key] == census_members[key]
                 for key in census_members),
         "member-to-census component closure")
    need(sum(census_members.values()) == EXPECTED["members"]
         and sum(census_within.values()) == EXPECTED["within_pairs"],
         "global member/within closure")

    presence = [0] * EXPECTED["blocks"]
    within_matrix = [
        [0] * EXPECTED["blocks"] for _ in range(EXPECTED["blocks"])
    ]
    vector = hashlib.sha256()
    for post in sorted(component_blocks):
        items = sorted(component_blocks[post].items())
        vector.update(canonical([post, items]) + b"\n")
        for left_index, (left, left_count) in enumerate(items):
            presence[left] += 1
            within_matrix[left][left] += choose2(left_count)
            for right, right_count in items[left_index + 1:]:
                within_matrix[left][right] += left_count * right_count
    need(sum(block_members) == EXPECTED["members"]
         and all(count > 0 for count in block_members),
         "home-block coverage")
    commitments = {
        "member_id_sequence_sha256": member_ids_sequence.hexdigest(),
        "block_member_count_vector_sha256": digest(block_members),
        "post_component_block_count_vector_sha256": vector.hexdigest(),
        "member_input_row_sequence_sha256": row_sequence(member_row_hashes),
        "census_input_row_sequence_sha256": row_sequence(census_row_hashes),
    }
    return block_members, presence, within_matrix, commitments


def close_row(body: dict[str, Any]) -> dict[str, Any]:
    return {**body, "row_sha256": digest(body)}


def expected_block_row(
    ordinal: int, block_members: list[int], presence: list[int],
    within: list[list[int]], authority: dict[str, Any],
) -> dict[str, Any]:
    count = block_members[ordinal]
    total = choose2(count)
    internal = within[ordinal][ordinal]
    return close_row({
        "schema": BLOCK_SCHEMA,
        "ordinal": ordinal,
        "home_block_ordinal": ordinal,
        "home_block_hex": f"{ordinal:02x}",
        "home_block_definition": "FIRST_BYTE_SHA256_ASCII_REGISTRY_MEMBER_ID",
        "member_count": count,
        "post_component_presence_count": presence[ordinal],
        "same_block_total_unordered_pairs": total,
        "same_block_within_post_component_pairs": internal,
        "same_block_cross_post_component_pairs": total - internal,
        "partition_authority": {
            "c27r2_terminal_receipt_object_sha256":
                authority["c27r2_terminal_receipt_object_sha256"],
            "member_to_post_component_sha256":
                authority["member_to_post_component_sha256"],
            "post_component_census_sha256":
                authority["post_component_census_sha256"],
        },
        "formal_credit": 0,
        "C28": "UNAUTHORIZED_PENDING_RELEASE_TERMINAL",
        "CM2": "NO-GO_FOR_CLAIM",
    })


def expected_route_row(
    ordinal: int, left: int, right: int, block_members: list[int],
    within: list[list[int]], authority: dict[str, Any],
) -> dict[str, Any]:
    total = (
        choose2(block_members[left]) if left == right
        else block_members[left] * block_members[right]
    )
    internal = within[left][right]
    cross = total - internal
    need(cross >= 0, f"nonnegative route shard:{ordinal}")
    return close_row({
        "schema": ROUTE_SCHEMA,
        "ordinal": ordinal,
        "shard_ordinal": ordinal,
        "canonical_home_block_pair": [f"{left:02x}", f"{right:02x}"],
        "left_member_count": block_members[left],
        "right_member_count": block_members[right],
        "same_home_block": left == right,
        "total_unordered_member_pairs": total,
        "within_post_component_member_pairs_excluded": internal,
        "cross_post_component_member_pairs_routed": cross,
        "pair_classification": {
            "EXACT_NONEDGE_BY_COMPLETE_ACTUAL_V2_EDGE_COMPLEMENT_AFTER_"
            "C27R2_QUOTIENT": cross,
            "KNOWN_LEGAL_CROSS_POST_COMPONENT": 0,
            "NEW_LEGAL_CROSS_POST_COMPONENT": 0,
            "UNRESOLVED": 0,
        },
        "proof_binding": {
            "c27r2_terminal_receipt_object_sha256":
                authority["c27r2_terminal_receipt_object_sha256"],
            "canonical_pair_home_rule":
                "SORTED_FIRST_BYTE_SHA256_ASCII_REGISTRY_MEMBER_ID",
            "within_pairs_removed_by_exact_post_component_block_convolution":
                True,
            "remaining_pairs_are_cross_post_component": True,
            "actual_v2_edge_complement_complete_after_C27R2_quotient": True,
        },
        "formal_credit": 0,
        "C28": "UNAUTHORIZED_PENDING_RELEASE_TERMINAL",
        "CM2": "NO-GO_FOR_CLAIM",
    })


class LedgerWriter:
    def __init__(self, path: Path, schema: str, ordering: list[str],
                 unique_key: str):
        self.path = path
        self.schema = schema
        self.ordering = ordering
        self.unique_key = unique_key
        descriptor = os.open(
            path,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL
            | getattr(os, "O_NOFOLLOW", 0),
            0o600,
        )
        self.raw = os.fdopen(descriptor, "wb")
        self.stream = gzip.GzipFile(
            filename="", mode="wb", compresslevel=9, fileobj=self.raw, mtime=0,
        )
        self.count = 0
        self.sequence = hashlib.sha256()

    def write(self, row: dict[str, Any]) -> None:
        need(row.get("schema") == self.schema
             and row.get("ordinal") == self.count,
             "output ledger schema/ordinal")
        body = dict(row)
        claimed = body.pop("row_sha256", None)
        need(valid_sha(claimed) and claimed == digest(body),
             "output row closure")
        self.stream.write(canonical(row) + b"\n")
        self.sequence.update(claimed.encode("ascii") + b"\n")
        self.count += 1

    def finish(self) -> dict[str, Any]:
        self.stream.close()
        self.raw.flush()
        os.fsync(self.raw.fileno())
        self.raw.close()
        info = self.path.stat()
        need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1,
             "output regular single-link ledger")
        state = hashlib.sha256()
        with self.path.open("rb") as stream:
            while block := stream.read(4 << 20):
                state.update(block)
        return {
            "filename": self.path.name,
            "sha256": state.hexdigest(),
            "size": info.st_size,
            "row_count": self.count,
            "row_schema": self.schema,
            "ordering": self.ordering,
            "unique_key": self.unique_key,
            "row_sequence_sha256": self.sequence.hexdigest(),
            "gzip_mtime": 0,
            "canonical_jsonl": True,
            "row_closure": "row_sha256=SHA256(canonical row without row_sha256)",
        }


def write_once(path: Path, payload: bytes) -> None:
    descriptor = os.open(
        path,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL
        | getattr(os, "O_NOFOLLOW", 0),
        0o600,
    )
    try:
        offset = 0
        while offset < len(payload):
            offset += os.write(descriptor, payload[offset:])
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    info = path.stat()
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1,
         "output regular single-link document")


def build(args: argparse.Namespace) -> dict[str, Any]:
    out_dir = workspace_path(args.out_dir, may_not_exist=True)
    terminal_dir = workspace_path(args.c27r2_terminal_dir)
    need(not out_dir.exists(), "fresh output directory")
    need(out_dir != terminal_dir and terminal_dir not in out_dir.parents,
         "output directory outside terminal authority tree")
    contract, c27r2_result, member, census, captures, authority = load_authority(
        args
    )
    source: Capture | None = None
    try:
        source = Capture(SELF, "producer-source")
        block_members, presence, within, commitments = reconstruct_partition(
            member, census, c27r2_result
        )
        out_dir.mkdir(parents=True, mode=0o700)
        block_writer = LedgerWriter(
            out_dir / BLOCK_FILE, BLOCK_SCHEMA, ["home_block_ordinal"],
            "home_block_hex",
        )
        for ordinal in range(EXPECTED["blocks"]):
            block_writer.write(expected_block_row(
                ordinal, block_members, presence, within, authority
            ))
        block_descriptor = block_writer.finish()

        route_writer = LedgerWriter(
            out_dir / ROUTE_FILE, ROUTE_SCHEMA,
            ["canonical_home_block_pair"], "canonical_home_block_pair",
        )
        totals = {"total": 0, "within": 0, "cross": 0}
        ordinal = 0
        for left in range(EXPECTED["blocks"]):
            for right in range(left, EXPECTED["blocks"]):
                row = expected_route_row(
                    ordinal, left, right, block_members, within, authority
                )
                route_writer.write(row)
                totals["total"] += row["total_unordered_member_pairs"]
                totals["within"] += row[
                    "within_post_component_member_pairs_excluded"
                ]
                totals["cross"] += row[
                    "cross_post_component_member_pairs_routed"
                ]
                ordinal += 1
        route_descriptor = route_writer.finish()
        need(block_descriptor["row_count"] == EXPECTED["blocks"]
             and route_descriptor["row_count"] == EXPECTED["shards"],
             "output ledger counts")
        need(totals == {
            "total": EXPECTED["total_pairs"],
            "within": EXPECTED["within_pairs"],
            "cross": EXPECTED["cross_pairs"],
        }, "exact global pair identity")

        theorem = {
            "kind": (
                "EXACT_NONEDGE_BY_COMPLETE_ACTUAL_V2_EDGE_COMPLEMENT_AFTER_"
                "C27R2_QUOTIENT"
            ),
            "every_terminal_pinned_member_has_one_home_block": True,
            "every_unordered_member_pair_has_one_unordered_block_pair_shard":
                True,
            "all_32896_shards_are_disjoint_and_exhaustive": True,
            "within_post_component_pairs_removed_by_exact_convolution": True,
            "cross_post_component_pair_denominator": EXPECTED["cross_pairs"],
            "complete_actual_v2_edge_union_consumed_by_C27R2_terminal": True,
            "new_legal_cross_post_component_pairs": 0,
            "unresolved_cross_post_component_pairs": 0,
            "post_C27R2_components_are_maximal_under_complete_actual_v2_edges":
                True,
            "candidate_math_only_until_C28_terminal_release": True,
        }
        input_attestations = {
            capture.label: capture.attestation() for capture in captures
        }
        body = {
            "schema": RESULT_SCHEMA,
            "status": RESULT_STATUS,
            "producer_source_sha256": source.sha256,
            "authority": authority,
            "post_C27R2_partition_census": {
                "members": EXPECTED["members"],
                "components": EXPECTED["post_components"],
                "total_unordered_member_pairs": EXPECTED["total_pairs"],
                "within_post_component_member_pairs": EXPECTED["within_pairs"],
                "cross_post_component_member_pairs": EXPECTED["cross_pairs"],
            },
            "home_block_census": {
                "definition": "FIRST_BYTE_SHA256_ASCII_REGISTRY_MEMBER_ID",
                "blocks": EXPECTED["blocks"],
                "nonempty_blocks": sum(count > 0 for count in block_members),
                "members_assigned": sum(block_members),
                **commitments,
            },
            "pair_route_census": {
                "unordered_block_pair_shards": EXPECTED["shards"],
                "closed_shards": route_descriptor["row_count"],
                "total_unordered_member_pairs": totals["total"],
                "within_post_component_pairs_excluded": totals["within"],
                "cross_post_component_pairs_routed": totals["cross"],
                "exact_nonedge_pairs": totals["cross"],
                "known_legal_cross_post_component_pairs": 0,
                "new_legal_cross_post_component_pairs": 0,
                "unresolved_pairs": 0,
            },
            "maximality_candidate_theorem": theorem,
            "maximality_candidate_theorem_sha256": digest(theorem),
            "ledgers": {
                "member_home_block_census": block_descriptor,
                "cross_component_pair_route_shard": route_descriptor,
            },
            "derivation_closures": {
                "only_terminal_pinned_member_to_post_consumed": True,
                "only_terminal_pinned_post_census_consumed": True,
                "old_C15_partition_authority_read": False,
                "old_C27_frontier_or_family_read": False,
                "old_C28_result_or_manifest_read": False,
                "pair_identity_total_equals_within_plus_cross": True,
                "input_pre_post_SHA_stat_identical": True,
            },
            "input_pre_post_attestations": input_attestations,
            "formal_credit": 0,
            "manifest_authorized": False,
            "C27R2": "CONSUMED_ONLY_THROUGH_PINNED_TERMINAL_ADAPTER",
            "C28": "UNAUTHORIZED_PENDING_RELEASE_TERMINAL",
            "C29": "UNAUTHORIZED",
            "Source_W": "UNCHANGED_BY_SOURCE_G_C28_CANDIDATE",
            "CM2": "NO-GO_FOR_CLAIM",
            "required_next": (
                "NO_IMPORT_VERIFIER_THEN_COHERENT_AND_RELEASE_ATTACKS_COLD_"
                "TOCTOU_MANIFEST_OUTER_AND_TERMINAL_REPLAY"
            ),
        }
        for capture in captures:
            capture.assert_stable()
        source.assert_stable()
        result = dict(body)
        result["result_sha256"] = digest(result)
        write_once(out_dir / RESULT_FILE, canonical(result) + b"\n")
        need(set(path.name for path in out_dir.iterdir())
             == {BLOCK_FILE, ROUTE_FILE, RESULT_FILE},
             "exact output file set")
        return result
    finally:
        if source is not None:
            source.close()
        for capture in captures:
            capture.close()


def self_test() -> dict[str, Any]:
    members = ["m0", "m1", "m2", "m3", "m4"]
    components = {"p0": members[:3], "p1": members[3:]}
    block_members = [0] * 256
    component_blocks: dict[str, dict[int, int]] = defaultdict(dict)
    for post, values in components.items():
        for member in values:
            block = home_block(member)
            block_members[block] += 1
            component_blocks[post][block] = (
                component_blocks[post].get(block, 0) + 1
            )
    within = [[0] * 256 for _ in range(256)]
    for values in component_blocks.values():
        items = sorted(values.items())
        for index, (left, left_count) in enumerate(items):
            within[left][left] += choose2(left_count)
            for right, right_count in items[index + 1:]:
                within[left][right] += left_count * right_count
    total = sum(
        choose2(block_members[left]) if left == right
        else block_members[left] * block_members[right]
        for left in range(256) for right in range(left, 256)
    )
    internal = sum(
        within[left][right]
        for left in range(256) for right in range(left, 256)
    )
    need(total == choose2(5) and internal == choose2(3) + choose2(2),
         "fixture pair convolution")
    with tempfile.TemporaryDirectory(prefix="cm2-c28-v2-selftest-") as raw:
        path = Path(raw) / "rows.jsonl.gz"
        writer = LedgerWriter(path, BLOCK_SCHEMA, ["ordinal"], "ordinal")
        writer.write(close_row({
            "schema": BLOCK_SCHEMA, "ordinal": 0, "fixture": True,
            "formal_credit": 0,
        }))
        descriptor = writer.finish()
        need(descriptor["row_count"] == 1
             and descriptor["gzip_mtime"] == 0,
             "fixture deterministic gzip")
    zero = "0" * 64
    contract_fixture = {
        "schema": CONTRACT_SCHEMA, "status": CONTRACT_READY,
        "terminal": {
            "terminal_dir": ".cm2-runtime/audit/future-c27r2-terminal",
            "root_manifest_filename": "root_manifest.sha256",
            "payload_manifest_filename": "payload_manifest.sha256",
            "receipt_filename": "terminal_receipt.json",
            "pass_lock_filename": "PASS.lock",
            "pass_lock_ascii": "PASS_FUTURE_C27R2_TERMINAL",
            "root_payload_entry": "payload_manifest.sha256",
            "root_receipt_entry": "terminal_receipt.json",
            "root_manifest_sha256": zero,
            "payload_manifest_sha256": zero,
            "receipt_file_sha256": zero,
            "receipt_object_sha256": zero,
            "receipt_closure_key": "terminal_receipt_sha256",
            "receipt_schema": "future.schema.supplied.after.mint",
            "receipt_status": "future.status.supplied.after.mint",
        },
        "payload": {
            "producer_result": {
                "path": ".cm2-runtime/audit/future/result.json",
                "sha256": zero, "size": 1, "row_count": 0,
                "result_sha256": zero,
            },
            "member_to_post_component": {
                "path": ".cm2-runtime/audit/future/member.jsonl.gz",
                "sha256": zero, "size": 1,
                "row_count": EXPECTED["members"], "result_sha256": None,
            },
            "post_component_census": {
                "path": ".cm2-runtime/audit/future/census.jsonl.gz",
                "sha256": zero, "size": 1,
                "row_count": EXPECTED["post_components"],
                "result_sha256": None,
            },
        },
        "semantic_bindings": {
            role: {"path": ["future", role], "expected": role}
            for role in SEMANTIC_ROLES
        },
        "review": {
            "C27R2_terminal_authority_reviewed": True,
            "complete_actual_v2_edge_complement_reviewed": True,
            "C28_math_core_may_start": True,
            "C28_formal_credit_minted": False,
            "C29_authorized": False, "CM2": "NO-GO_FOR_CLAIM",
            "pending_fields_were_filled_only_after_terminal_mint": True,
        },
    }
    contract_fixture["contract_sha256"] = digest(contract_fixture)
    validate_contract(contract_fixture)
    pending = dict(contract_fixture)
    pending["status"] = "PENDING_C27R2_TERMINAL"
    rejected_pending = False
    try:
        validate_contract(pending)
    except Failure:
        rejected_pending = True
    need(rejected_pending is True, "fixture pending adapter rejects")
    return {
        "schema": RESULT_SCHEMA + ".self-test",
        "status": (
            "PASS_SMALL_FIXTURE_PAIR_CONVOLUTION_GZIP_AND_DYNAMIC_ADAPTER_"
            "FAIL_CLOSED_TESTS"
        ),
        "fixture_total_pairs": total,
        "fixture_within_pairs": internal,
        "fixture_cross_pairs": total - internal,
        "formal_credit": 0,
        "CM2": "NO-GO_FOR_CLAIM",
    }


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--self-test", action="store_true")
    value.add_argument("--c27r2-terminal-dir")
    value.add_argument("--authority-contract")
    value.add_argument("--expect-authority-contract-sha256")
    value.add_argument("--expect-terminal-root-sha256")
    value.add_argument("--expect-terminal-receipt-file-sha256")
    value.add_argument("--expect-terminal-receipt-object-sha256")
    value.add_argument("--out-dir")
    return value


def main() -> int:
    args = parser().parse_args()
    names = (
        "c27r2_terminal_dir", "authority_contract",
        "expect_authority_contract_sha256", "expect_terminal_root_sha256",
        "expect_terminal_receipt_file_sha256",
        "expect_terminal_receipt_object_sha256", "out_dir",
    )
    try:
        if args.self_test:
            need(all(getattr(args, name) is None for name in names),
                 "self-test accepts no authority/output arguments")
            result = self_test()
        else:
            need(all(getattr(args, name) is not None for name in names),
                 "all dynamic terminal adapter pins and fresh output required")
            result = build(args)
        sys.stdout.buffer.write(canonical({
            "status": result["status"], "formal_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        }) + b"\n")
        return 0
    except (Failure, OSError, ValueError, KeyError, TypeError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
