#!/usr/bin/env python3
"""No-import verifier for the append-only Source-G C28-v2 math core.

The verifier does not import or execute the producer.  It independently
validates the dynamic C27R2 terminal adapter, reconstructs the 43,684-component
partition from the terminal-pinned member and census ledgers, recomputes all
256 home blocks and 32,896 unordered block-pair shards, and byte-compares the
candidate semantics.  PASS remains zero-credit and cannot mint C28.
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
PRODUCER_BASENAME = (
    "cm2_round306c28_source_g_post_c27r2_125561998198_pair_routing_"
    "v2_producer.py"
)
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
VERIFICATION_SCHEMA = (
    "cm2.round306c28.source-g-post-c27r2-125561998198-pair-routing.v2."
    "independent-verification.v1"
)
VERIFICATION_STATUS = (
    "PASS_NO_IMPORT_C27R2_TERMINAL_PARTITION_AND_32896_PAIR_SHARDS_"
    "INDEPENDENTLY_REBUILT__ZERO_CREDIT_PENDING_ATTACKS_AND_RELEASE_CHAIN"
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
    "c27r2_terminal_passed", "c28_fresh_rebuild_only",
    "complete_actual_v2_edge_complement_after_quotient",
    "c28_formal_credit_zero", "c29_unauthorized", "cm2_no_go",
}


class Reject(RuntimeError):
    pass


def require(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def wire(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def object_sha(value: Any) -> str:
    return hashlib.sha256(wire(value)).hexdigest()


def sha_ok(value: Any) -> bool:
    return (
        type(value) is str and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def decode(payload: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in items:
            require(key not in output, "duplicate JSON key:" + key)
            output[key] = value
        return output

    def reject_constant(value: str) -> None:
        raise Reject("non-finite JSON:" + value)

    return json.loads(
        payload, object_pairs_hook=pairs, parse_constant=reject_constant
    )


def local_path(raw: str | Path, *, absent: bool = False) -> Path:
    supplied = Path(raw)
    value = (ROOT / supplied if not supplied.is_absolute() else supplied).absolute()
    try:
        relative = value.relative_to(ROOT)
    except ValueError as error:
        raise Reject("path outside workspace:" + str(raw)) from error
    require(all(piece not in {"", ".", ".."} for piece in relative.parts),
            "canonical workspace path:" + str(raw))
    cursor = ROOT
    for piece in relative.parts:
        cursor = cursor / piece
        if not cursor.exists():
            require(absent is True,
                    "missing path component:" + str(cursor))
            break
        require(not cursor.is_symlink(),
                "symlink path component:" + str(cursor))
    return value


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def stat_key(info: os.stat_result) -> list[int]:
    return [
        info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size,
        info.st_mtime_ns, info.st_ctime_ns, info.st_uid, info.st_gid,
    ]


class FileView:
    def __init__(self, path: Path, label: str):
        self.path = local_path(path)
        self.label = label
        self.fd = os.open(
            self.path,
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0),
        )
        self.initial = os.fstat(self.fd)
        require(stat.S_ISREG(self.initial.st_mode), label + ":regular")
        require(self.initial.st_nlink == 1, label + ":single-link")
        self.sha256 = self.hash()

    def rewind(self) -> None:
        os.lseek(self.fd, 0, os.SEEK_SET)

    def hash(self) -> str:
        self.rewind()
        state = hashlib.sha256()
        while block := os.read(self.fd, 4 << 20):
            state.update(block)
        self.rewind()
        require(stat_key(os.fstat(self.fd)) == stat_key(self.initial),
                self.label + ":stable hash")
        return state.hexdigest()

    def read(self) -> bytes:
        self.rewind()
        output: list[bytes] = []
        while block := os.read(self.fd, 4 << 20):
            output.append(block)
        self.rewind()
        require(stat_key(os.fstat(self.fd)) == stat_key(self.initial),
                self.label + ":stable read")
        return b"".join(output)

    def json(self, closure: str | None = None) -> Any:
        payload = self.read()
        require(payload.endswith(b"\n") and not payload.endswith(b"\n\n"),
                self.label + ":one newline")
        value = decode(payload[:-1])
        require(type(value) is dict and wire(value) == payload[:-1],
                self.label + ":canonical object")
        if closure is not None:
            body = dict(value)
            claimed = body.pop(closure, None)
            require(sha_ok(claimed) and claimed == object_sha(body),
                    self.label + ":closure")
        return value

    def rows(self) -> Iterator[tuple[int, dict[str, Any]]]:
        raw = self.read()
        require(len(raw) >= 10 and raw[:2] == b"\x1f\x8b"
                and int.from_bytes(raw[4:8], "little") == 0,
                self.label + ":gzip header/mtime0")
        try:
            with gzip.GzipFile(fileobj=io.BytesIO(raw), mode="rb") as source:
                for ordinal, line in enumerate(source):
                    require(line.endswith(b"\n"),
                            self.label + f":newline:{ordinal}")
                    value = decode(line[:-1])
                    require(type(value) is dict and wire(value) == line[:-1],
                            self.label + f":canonical row:{ordinal}")
                    body = dict(value)
                    claimed = body.pop("row_sha256", None)
                    require(sha_ok(claimed) and claimed == object_sha(body),
                            self.label + f":row closure:{ordinal}")
                    yield ordinal, value
        except (gzip.BadGzipFile, EOFError) as error:
            raise Reject(self.label + ":gzip") from error

    def attestation(self) -> dict[str, Any]:
        return {
            "path": rel(self.path), "sha256": self.sha256,
            "size": self.initial.st_size,
            "stat_fingerprint": stat_key(self.initial), "O_NOFOLLOW": True,
            "single_open_file_description_hash_parse_fstat": True,
        }

    def stable(self) -> None:
        require(self.hash() == self.sha256
                and stat_key(os.fstat(self.fd)) == stat_key(self.initial),
                self.label + ":pre/post SHA/stat")

    def close(self) -> None:
        os.close(self.fd)


def manifest(view: FileView) -> dict[str, str]:
    payload = view.read()
    require(payload.endswith(b"\n"), view.label + ":manifest newline")
    try:
        lines = payload.decode("ascii").splitlines()
    except UnicodeDecodeError as error:
        raise Reject(view.label + ":manifest ASCII") from error
    output: dict[str, str] = {}
    for ordinal, line in enumerate(lines):
        fields = line.split(None, 1)
        require(len(fields) == 2 and sha_ok(fields[0]),
                view.label + f":manifest line:{ordinal}")
        name = fields[1].strip()
        path = Path(name)
        require(name == fields[1] and name != "" and name not in output
                and not path.is_absolute()
                and all(piece not in {"", ".", ".."}
                        for piece in path.parts),
                view.label + f":manifest safe entry:{ordinal}")
        output[name] = fields[0]
    require(len(output) > 0, view.label + ":manifest nonempty")
    require(list(output) == sorted(output),
            view.label + ":manifest lexical order")
    return output


def lookup(value: Any, path: Any, label: str) -> Any:
    require(type(path) is list and len(path) > 0
            and all(type(piece) is str and piece != "" for piece in path),
            label + ":path")
    current = value
    for piece in path:
        require(type(current) is dict and piece in current,
                label + ":missing:" + piece)
        current = current[piece]
    return current


def contract_ok(value: Any) -> None:
    require(type(value) is dict and set(value) == {
        "schema", "status", "terminal", "payload", "semantic_bindings",
        "review", "contract_sha256",
    }, "adapter exact object")
    require(value["schema"] == CONTRACT_SCHEMA
            and value["status"] == CONTRACT_READY,
            "adapter finalized")
    terminal = value["terminal"]
    require(type(terminal) is dict and set(terminal) == {
        "terminal_dir", "root_manifest_filename", "payload_manifest_filename",
        "receipt_filename", "pass_lock_filename", "pass_lock_ascii",
        "root_payload_entry", "root_receipt_entry", "root_manifest_sha256",
        "payload_manifest_sha256", "receipt_file_sha256",
        "receipt_object_sha256", "receipt_closure_key", "receipt_schema",
        "receipt_status",
    }, "adapter terminal fields")
    string_fields = (
        "terminal_dir", "root_manifest_filename", "payload_manifest_filename",
        "receipt_filename", "pass_lock_filename", "pass_lock_ascii",
        "root_payload_entry", "root_receipt_entry", "receipt_closure_key",
        "receipt_schema", "receipt_status",
    )
    require(all(type(terminal[key]) is str and terminal[key] != ""
                for key in string_fields), "adapter terminal strings")
    file_fields = (
        "root_manifest_filename", "payload_manifest_filename",
        "receipt_filename", "pass_lock_filename",
    )
    require(all(Path(terminal[key]).name == terminal[key]
                for key in file_fields)
            and len({terminal[key] for key in file_fields}) == len(file_fields),
            "adapter distinct terminal basenames")
    require(terminal["root_payload_entry"]
                != terminal["root_receipt_entry"],
            "adapter distinct root entries")
    require(all(sha_ok(terminal[key]) for key in (
        "root_manifest_sha256", "payload_manifest_sha256",
        "receipt_file_sha256", "receipt_object_sha256",
    )), "adapter terminal hashes")
    require("\n" not in terminal["pass_lock_ascii"]
            and "\r" not in terminal["pass_lock_ascii"],
            "adapter PASS line")
    payload = value["payload"]
    require(type(payload) is dict and set(payload) == {
        "producer_result", "member_to_post_component", "post_component_census",
    }, "adapter payload roles")
    expected_rows = {
        "producer_result": 0,
        "member_to_post_component": EXPECTED["members"],
        "post_component_census": EXPECTED["post_components"],
    }
    for role, item in payload.items():
        require(type(item) is dict and set(item) == {
            "path", "sha256", "size", "row_count", "result_sha256",
        }, "adapter payload fields:" + role)
        require(type(item["path"]) is str and item["path"] != ""
                and sha_ok(item["sha256"])
                and type(item["size"]) is int and item["size"] > 0
                and item["row_count"] == expected_rows[role],
                "adapter payload descriptor:" + role)
        require(
            sha_ok(item["result_sha256"])
            if role == "producer_result"
            else item["result_sha256"] is None,
            "adapter result-object role:" + role,
        )
    require(len({item["path"] for item in payload.values()}) == 3,
            "adapter distinct selected payload paths")
    bindings = value["semantic_bindings"]
    require(type(bindings) is dict and set(bindings) == SEMANTIC_ROLES,
            "adapter semantic roles")
    paths: set[tuple[str, ...]] = set()
    for role, item in bindings.items():
        require(type(item) is dict and set(item) == {"path", "expected"},
                "adapter semantic fields:" + role)
        path = item["path"]
        require(type(path) is list and len(path) > 0
                and all(type(piece) is str and piece != "" for piece in path),
                "adapter semantic path:" + role)
        key = tuple(path)
        require(key not in paths, "adapter semantic unique paths")
        paths.add(key)
        wire(item["expected"])
    require(value["review"] == {
        "C27R2_terminal_authority_reviewed": True,
        "complete_actual_v2_edge_complement_reviewed": True,
        "C28_math_core_may_start": True,
        "C28_formal_credit_minted": False,
        "C29_authorized": False,
        "CM2": "NO-GO_FOR_CLAIM",
        "pending_fields_were_filled_only_after_terminal_mint": True,
    }, "adapter review boundary")


def descriptor_ok(
    descriptor: Any, view: FileView, schema: str, count: int,
    ordering: list[str], unique_key: str,
) -> None:
    require(type(descriptor) is dict
            and descriptor.get("filename") == view.path.name
            and descriptor.get("sha256") == view.sha256
            and descriptor.get("size") == view.initial.st_size
            and descriptor.get("row_count") == count
            and descriptor.get("row_schema") == schema
            and descriptor.get("ordering") == ordering
            and descriptor.get("unique_key") == unique_key
            and sha_ok(descriptor.get("row_sequence_sha256"))
            and descriptor.get("gzip_mtime") == 0
            and descriptor.get("canonical_jsonl") is True
            and descriptor.get("row_closure")
                == "row_sha256=SHA256(canonical row without row_sha256)",
            "C27R2 descriptor:" + view.label)


def authority(args: argparse.Namespace) -> tuple[
    dict[str, Any], dict[str, Any], FileView, FileView, list[FileView],
    dict[str, Any]
]:
    require(all(sha_ok(value) for value in (
        args.expect_authority_contract_sha256,
        args.expect_terminal_root_sha256,
        args.expect_terminal_receipt_file_sha256,
        args.expect_terminal_receipt_object_sha256,
    )), "external authority hashes")
    terminal_dir = local_path(args.c27r2_terminal_dir)
    contract_view = FileView(local_path(args.authority_contract),
                             "authority-contract")
    views: list[FileView] = [contract_view]
    try:
        require(contract_view.sha256 == args.expect_authority_contract_sha256,
                "adapter external pin")
        contract = contract_view.json("contract_sha256")
        contract_ok(contract)
        terminal = contract["terminal"]
        require(rel(terminal_dir) == terminal["terminal_dir"]
                and terminal["root_manifest_sha256"]
                    == args.expect_terminal_root_sha256
                and terminal["receipt_file_sha256"]
                    == args.expect_terminal_receipt_file_sha256
                and terminal["receipt_object_sha256"]
                    == args.expect_terminal_receipt_object_sha256,
                "adapter/external terminal binding")
        root = FileView(terminal_dir / terminal["root_manifest_filename"],
                        "c27r2-terminal-root")
        views.append(root)
        payload = FileView(terminal_dir / terminal["payload_manifest_filename"],
                           "c27r2-terminal-payload")
        views.append(payload)
        receipt = FileView(terminal_dir / terminal["receipt_filename"],
                           "c27r2-terminal-receipt")
        views.append(receipt)
        lock = FileView(terminal_dir / terminal["pass_lock_filename"],
                        "c27r2-terminal-PASS")
        views.append(lock)
        require(root.sha256 == args.expect_terminal_root_sha256
                and payload.sha256 == terminal["payload_manifest_sha256"]
                and receipt.sha256
                    == args.expect_terminal_receipt_file_sha256,
                "terminal file pins")
        require(lock.read()
                == (terminal["pass_lock_ascii"] + "\n").encode("ascii"),
                "terminal PASS lock")
        require(manifest(root) == {
            terminal["root_payload_entry"]: payload.sha256,
            terminal["root_receipt_entry"]: receipt.sha256,
        }, "terminal exact root")
        payload_entries = manifest(payload)
        receipt_value = receipt.json(terminal["receipt_closure_key"])
        require(receipt_value.get(terminal["receipt_closure_key"])
                    == args.expect_terminal_receipt_object_sha256
                and receipt_value.get("schema") == terminal["receipt_schema"]
                and receipt_value.get("status") == terminal["receipt_status"],
                "terminal dynamic receipt contract")
        for role, binding in contract["semantic_bindings"].items():
            require(lookup(receipt_value, binding["path"], role)
                    == binding["expected"],
                    "terminal semantic binding:" + role)
        selected: dict[str, FileView] = {}
        for role, item in contract["payload"].items():
            view = FileView(local_path(item["path"]), "c27r2-" + role)
            views.append(view)
            selected[role] = view
            require(view.sha256 == item["sha256"]
                    and view.initial.st_size == item["size"]
                    and payload_entries.get(item["path"]) == item["sha256"],
                    "terminal selected payload:" + role)
        result = selected["producer_result"].json("result_sha256")
        require(set(result) == {
            "C27R2", "C28_C29", "CM2", "Source_W", "authority",
            "canonical_post_component_id_formula", "derivation_closures",
            "edge_row_sequence_sha256", "exact_census", "formal_credit",
            "input_pre_post_attestations", "ledgers", "manifest_authorized",
            "producer_source_attestation", "producer_source_sha256",
            "result_sha256", "schema", "status",
        }, "C27R2 producer result exact keys")
        require(result["result_sha256"]
                    == contract["payload"]["producer_result"]["result_sha256"]
                and result.get("schema") == C27R2_RESULT_SCHEMA
                and result.get("status") == C27R2_RESULT_STATUS
                and result.get("exact_census") == EXPECTED_C27R2_CENSUS
                and result.get("formal_credit") == 0
                and result.get("manifest_authorized") is False
                and result.get("C27R2")
                    == "UNAUTHORIZED_PENDING_INDEPENDENT_VERIFICATION_AND_TERMINAL_SEAL"
                and result.get("C28_C29") == "UNAUTHORIZED"
                and result.get("CM2") == "NO-GO_FOR_CLAIM",
                "C27R2 result exact candidate contract")
        require(result.get("Source_W")
                    == "UNCHANGED_BY_SOURCE_G_REBUILD_CANDIDATE"
                and result.get("canonical_post_component_id_formula") == (
                    "round306c27r2-source-g-post-component:SHA256(canonical "
                    "JSON sorted list of old C15 component IDs)"
                )
                and result.get("derivation_closures") == {
                    "DSU_started_from_all_57876_frozen_C15_components": True,
                    "all_502204_members_rebound_through_frozen_C15": True,
                    "old_C27_C28_C29_partition_imported_or_read": False,
                    "only_terminal_pinned_actual_v2_seed1_edges_applied": True,
                    "pair_identity_total_equals_within_plus_cross": True,
                    "post_component_ID_never_uses_DSU_root": True,
                }
                and sha_ok(result.get("edge_row_sequence_sha256"))
                and sha_ok(result.get("producer_source_sha256"))
                and type(result.get("authority")) is dict
                and type(result.get("input_pre_post_attestations")) is dict
                and type(result.get("producer_source_attestation")) is dict
                and result["producer_source_attestation"].get("sha256")
                    == result["producer_source_sha256"],
                "C27R2 exact derivation/source contract")
        ledgers = result.get("ledgers")
        require(type(ledgers) is dict and set(ledgers) == {
            "old_C15_component_to_post_component", "member_to_post_component",
            "post_component_census",
        }, "C27R2 ledgers object")
        descriptor_ok(
            ledgers.get("member_to_post_component"),
            selected["member_to_post_component"], MEMBER_SCHEMA,
            EXPECTED["members"], ["member_ordinal"], "registry_member_id",
        )
        descriptor_ok(
            ledgers.get("post_component_census"),
            selected["post_component_census"], CENSUS_SCHEMA,
            EXPECTED["post_components"], ["post_C27R2_component_id"],
            "post_C27R2_component_id",
        )
        summary = {
            "adapter_contract_path": rel(contract_view.path),
            "adapter_contract_file_sha256": contract_view.sha256,
            "adapter_contract_object_sha256": contract["contract_sha256"],
            "c27r2_terminal_dir": rel(terminal_dir),
            "c27r2_terminal_root_manifest_sha256": root.sha256,
            "c27r2_terminal_payload_manifest_sha256": payload.sha256,
            "c27r2_terminal_receipt_file_sha256": receipt.sha256,
            "c27r2_terminal_receipt_object_sha256":
                receipt_value[terminal["receipt_closure_key"]],
            "c27r2_producer_result_sha256": result["result_sha256"],
            "member_to_post_component_sha256":
                selected["member_to_post_component"].sha256,
            "post_component_census_sha256":
                selected["post_component_census"].sha256,
            "terminal_semantic_roles_verified": sorted(SEMANTIC_ROLES),
        }
        return (
            contract, result, selected["member_to_post_component"],
            selected["post_component_census"], views, summary,
        )
    except BaseException:
        for view in views:
            view.close()
        raise


def choose_two(count: int) -> int:
    return count * (count - 1) // 2


def block_of(member: str) -> int:
    return hashlib.sha256(member.encode("ascii")).digest()[0]


def sequence(values: list[str]) -> str:
    state = hashlib.sha256()
    for value in values:
        state.update(value.encode("ascii") + b"\n")
    return state.hexdigest()


def rebuild(
    member: FileView, census: FileView, result: dict[str, Any]
) -> tuple[list[int], list[int], list[list[int]], dict[str, str]]:
    counts = [0] * EXPECTED["blocks"]
    per_component: dict[str, list[int]] = defaultdict(list)
    members_by_component: Counter[str] = Counter()
    identities: set[str] = set()
    identity_sequence = hashlib.sha256()
    member_hashes: list[str] = []
    for ordinal, row in member.rows():
        require(set(row) == {
            "schema", "ordinal", "member_ordinal", "registry_member_id",
            "old_C15_component_id", "post_C27R2_component_id",
            "formal_credit", "row_sha256",
        }, f"member exact keys:{ordinal}")
        require(row.get("schema") == MEMBER_SCHEMA
                and row.get("ordinal") == ordinal
                and row.get("member_ordinal") == ordinal
                and row.get("formal_credit") == 0,
                f"member row contract:{ordinal}")
        identity = row.get("registry_member_id")
        post = row.get("post_C27R2_component_id")
        require(type(identity) is str and identity != ""
                and identity not in identities,
                f"unique member:{ordinal}")
        require(type(post) is str and post != "", f"post ID:{ordinal}")
        require(type(row.get("old_C15_component_id")) is str
                and row["old_C15_component_id"] != "",
                f"historical old component binding:{ordinal}")
        identities.add(identity)
        home = block_of(identity)
        counts[home] += 1
        per_component[post].append(home)
        members_by_component[post] += 1
        identity_sequence.update(identity.encode("ascii") + b"\n")
        member_hashes.append(row["row_sha256"])
    require(len(identities) == EXPECTED["members"], "member census")
    require(sequence(member_hashes)
            == result["ledgers"]["member_to_post_component"]
                ["row_sequence_sha256"],
            "member row sequence")

    census_members: dict[str, int] = {}
    census_pairs: dict[str, int] = {}
    census_hashes: list[str] = []
    previous: str | None = None
    for ordinal, row in census.rows():
        require(set(row) == {
            "schema", "ordinal", "post_C27R2_component_id",
            "old_C15_component_count", "old_C15_component_ids_sha256",
            "member_count", "within_member_pair_count", "formal_credit",
            "row_sha256",
        }, f"census exact keys:{ordinal}")
        require(row.get("schema") == CENSUS_SCHEMA
                and row.get("ordinal") == ordinal
                and row.get("formal_credit") == 0,
                f"census contract:{ordinal}")
        post = row.get("post_C27R2_component_id")
        count = row.get("member_count")
        within = row.get("within_member_pair_count")
        require(type(post) is str and post != ""
                and (previous is None or previous < post)
                and post not in census_members,
                f"census ordering:{ordinal}")
        require(type(count) is int and count > 0
                and type(within) is int and within == choose_two(count),
                f"census pair closure:{ordinal}")
        require(type(row.get("old_C15_component_count")) is int
                and row["old_C15_component_count"] > 0
                and sha_ok(row.get("old_C15_component_ids_sha256")),
                f"census historical closure:{ordinal}")
        previous = post
        census_members[post] = count
        census_pairs[post] = within
        census_hashes.append(row["row_sha256"])
    require(len(census_members) == EXPECTED["post_components"]
            and sequence(census_hashes)
                == result["ledgers"]["post_component_census"]
                    ["row_sequence_sha256"],
            "census count/sequence")
    require(set(census_members) == set(members_by_component)
            and all(census_members[key] == members_by_component[key]
                    for key in census_members),
            "member/census closure")
    require(sum(census_members.values()) == EXPECTED["members"]
            and sum(census_pairs.values()) == EXPECTED["within_pairs"],
            "global component closure")

    presence = [0] * EXPECTED["blocks"]
    within_matrix = [
        [0] * EXPECTED["blocks"] for _ in range(EXPECTED["blocks"])
    ]
    vector = hashlib.sha256()
    for post in sorted(per_component):
        grouped: Counter[int] = Counter(per_component[post])
        items = sorted(grouped.items())
        vector.update(wire([post, items]) + b"\n")
        for index, (left, left_count) in enumerate(items):
            presence[left] += 1
            within_matrix[left][left] += choose_two(left_count)
            for right, right_count in items[index + 1:]:
                within_matrix[left][right] += left_count * right_count
    require(sum(counts) == EXPECTED["members"]
            and all(count > 0 for count in counts),
            "block coverage")
    commitments = {
        "member_id_sequence_sha256": identity_sequence.hexdigest(),
        "block_member_count_vector_sha256": object_sha(counts),
        "post_component_block_count_vector_sha256": vector.hexdigest(),
        "member_input_row_sequence_sha256": sequence(member_hashes),
        "census_input_row_sequence_sha256": sequence(census_hashes),
    }
    return counts, presence, within_matrix, commitments


def closed_row(body: dict[str, Any]) -> dict[str, Any]:
    return {**body, "row_sha256": object_sha(body)}


def block_row(
    ordinal: int, counts: list[int], presence: list[int],
    within: list[list[int]], authority_summary: dict[str, Any],
) -> dict[str, Any]:
    total = choose_two(counts[ordinal])
    internal = within[ordinal][ordinal]
    return closed_row({
        "schema": BLOCK_SCHEMA, "ordinal": ordinal,
        "home_block_ordinal": ordinal, "home_block_hex": f"{ordinal:02x}",
        "home_block_definition": "FIRST_BYTE_SHA256_ASCII_REGISTRY_MEMBER_ID",
        "member_count": counts[ordinal],
        "post_component_presence_count": presence[ordinal],
        "same_block_total_unordered_pairs": total,
        "same_block_within_post_component_pairs": internal,
        "same_block_cross_post_component_pairs": total - internal,
        "partition_authority": {
            "c27r2_terminal_receipt_object_sha256":
                authority_summary["c27r2_terminal_receipt_object_sha256"],
            "member_to_post_component_sha256":
                authority_summary["member_to_post_component_sha256"],
            "post_component_census_sha256":
                authority_summary["post_component_census_sha256"],
        },
        "formal_credit": 0,
        "C28": "UNAUTHORIZED_PENDING_RELEASE_TERMINAL",
        "CM2": "NO-GO_FOR_CLAIM",
    })


def route_row(
    ordinal: int, left: int, right: int, counts: list[int],
    within: list[list[int]], authority_summary: dict[str, Any],
) -> dict[str, Any]:
    total = choose_two(counts[left]) if left == right else counts[left] * counts[right]
    internal = within[left][right]
    cross = total - internal
    require(cross >= 0, f"route nonnegative:{ordinal}")
    return closed_row({
        "schema": ROUTE_SCHEMA, "ordinal": ordinal,
        "shard_ordinal": ordinal,
        "canonical_home_block_pair": [f"{left:02x}", f"{right:02x}"],
        "left_member_count": counts[left],
        "right_member_count": counts[right],
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
                authority_summary["c27r2_terminal_receipt_object_sha256"],
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


def ledger_descriptor(
    view: FileView, count: int, row_schema: str, ordering: list[str],
    unique_key: str, row_hashes: list[str],
) -> dict[str, Any]:
    return {
        "filename": view.path.name, "sha256": view.sha256,
        "size": view.initial.st_size, "row_count": count,
        "row_schema": row_schema, "ordering": ordering,
        "unique_key": unique_key,
        "row_sequence_sha256": sequence(row_hashes), "gzip_mtime": 0,
        "canonical_jsonl": True,
        "row_closure": "row_sha256=SHA256(canonical row without row_sha256)",
    }


def write_exclusive(path: Path, payload: bytes) -> None:
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
    require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1,
            "verification regular single-link")


def verify(args: argparse.Namespace) -> dict[str, Any]:
    require(sys.flags.isolated == 1 and sys.dont_write_bytecode is True,
            "isolated runtime")
    candidate = local_path(args.candidate_dir)
    out_file = local_path(args.out_file, absent=True)
    require(candidate.is_dir() and not candidate.is_symlink(),
            "candidate directory")
    require(not out_file.exists() and out_file.parent.is_dir()
            and out_file.parent != candidate,
            "fresh separate verification output")
    require(set(path.name for path in candidate.iterdir())
            == {BLOCK_FILE, ROUTE_FILE, RESULT_FILE},
            "candidate exact file set")
    views: list[FileView] = []
    authority_views: list[FileView] = []
    candidate_views: list[FileView] = []
    try:
        producer = FileView(local_path(args.producer), "producer-source")
        views.append(producer)
        verifier = FileView(SELF, "verifier-source")
        views.append(verifier)
        require(producer.path.name == PRODUCER_BASENAME
                and producer.sha256 == args.expect_producer_sha256
                and verifier.sha256 == args.expect_verifier_sha256,
                "producer/verifier external pins")
        contract, c27r2_result, member, census, authority_views, summary = authority(
            args
        )
        views.extend(authority_views)
        counts, presence, within, commitments = rebuild(
            member, census, c27r2_result
        )
        block = FileView(candidate / BLOCK_FILE, "candidate-block-ledger")
        candidate_views.append(block)
        views.append(block)
        route = FileView(candidate / ROUTE_FILE, "candidate-route-ledger")
        candidate_views.append(route)
        views.append(route)
        result_view = FileView(candidate / RESULT_FILE, "candidate-result")
        candidate_views.append(result_view)
        views.append(result_view)

        block_hashes: list[str] = []
        block_iter = block.rows()
        for ordinal in range(EXPECTED["blocks"]):
            item = next(block_iter, None)
            require(item is not None, f"block row present:{ordinal}")
            actual_ordinal, actual = item
            expected = block_row(ordinal, counts, presence, within, summary)
            require(actual_ordinal == ordinal and actual == expected,
                    f"block independent reconstruction:{ordinal}")
            block_hashes.append(actual["row_sha256"])
        require(next(block_iter, None) is None, "block exact exhaustion")

        route_hashes: list[str] = []
        route_iter = route.rows()
        totals = {"total": 0, "within": 0, "cross": 0}
        ordinal = 0
        for left in range(EXPECTED["blocks"]):
            for right in range(left, EXPECTED["blocks"]):
                item = next(route_iter, None)
                require(item is not None, f"route row present:{ordinal}")
                actual_ordinal, actual = item
                expected = route_row(
                    ordinal, left, right, counts, within, summary
                )
                require(actual_ordinal == ordinal and actual == expected,
                        f"route independent reconstruction:{ordinal}")
                route_hashes.append(actual["row_sha256"])
                totals["total"] += actual["total_unordered_member_pairs"]
                totals["within"] += actual[
                    "within_post_component_member_pairs_excluded"
                ]
                totals["cross"] += actual[
                    "cross_post_component_member_pairs_routed"
                ]
                ordinal += 1
        require(next(route_iter, None) is None
                and ordinal == EXPECTED["shards"],
                "route exact exhaustion")
        require(totals == {
            "total": EXPECTED["total_pairs"],
            "within": EXPECTED["within_pairs"],
            "cross": EXPECTED["cross_pairs"],
        }, "route global identity")

        block_descriptor = ledger_descriptor(
            block, EXPECTED["blocks"], BLOCK_SCHEMA, ["home_block_ordinal"],
            "home_block_hex", block_hashes,
        )
        route_descriptor = ledger_descriptor(
            route, EXPECTED["shards"], ROUTE_SCHEMA,
            ["canonical_home_block_pair"], "canonical_home_block_pair",
            route_hashes,
        )
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
        authority_attestations = {
            view.label: view.attestation() for view in authority_views
        }
        expected_body = {
            "schema": RESULT_SCHEMA, "status": RESULT_STATUS,
            "producer_source_sha256": producer.sha256,
            "authority": summary,
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
                "nonempty_blocks": sum(count > 0 for count in counts),
                "members_assigned": sum(counts), **commitments,
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
            "maximality_candidate_theorem_sha256": object_sha(theorem),
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
            "input_pre_post_attestations": authority_attestations,
            "formal_credit": 0, "manifest_authorized": False,
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
        expected_result = dict(expected_body)
        expected_result["result_sha256"] = object_sha(expected_result)
        actual_result = result_view.json("result_sha256")
        require(actual_result == expected_result,
                "candidate result byte-semantic reconstruction")
        for view in views:
            view.stable()
        verification_body = {
            "schema": VERIFICATION_SCHEMA,
            "status": VERIFICATION_STATUS,
            "verifier_source_sha256": verifier.sha256,
            "producer_source_sha256": producer.sha256,
            "candidate_result_sha256": actual_result["result_sha256"],
            "authority": summary,
            "verified_census": {
                "members": EXPECTED["members"],
                "post_components": EXPECTED["post_components"],
                "blocks": EXPECTED["blocks"],
                "shards": EXPECTED["shards"],
                "total_pairs": totals["total"],
                "within_pairs": totals["within"],
                "cross_pairs": totals["cross"],
            },
            "candidate_files": {
                BLOCK_FILE: block.attestation(),
                ROUTE_FILE: route.attestation(),
                RESULT_FILE: result_view.attestation(),
            },
            "independence": {
                "producer_imported": False,
                "producer_executed": False,
                "partition_rebuilt_from_terminal_pinned_ledgers": True,
                "all_candidate_rows_independently_reconstructed": True,
                "input_pre_post_SHA_stat_identical": True,
            },
            "formal_credit": 0,
            "manifest_authorized": False,
            "C28": "UNAUTHORIZED_PENDING_ATTACKS_AND_RELEASE_TERMINAL",
            "C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM",
        }
        verification = dict(verification_body)
        verification["verification_sha256"] = object_sha(verification)
        write_exclusive(out_file, wire(verification) + b"\n")
        return verification
    finally:
        closed: set[int] = set()
        for view in views:
            if view.fd not in closed:
                view.close()
                closed.add(view.fd)


def self_test() -> dict[str, Any]:
    identities = ["m0", "m1", "m2", "m3"]
    components = {"p0": identities[:2], "p1": identities[2:]}
    total = choose_two(len(identities))
    within = sum(choose_two(len(values)) for values in components.values())
    require(total == 6 and within == 2 and total - within == 4,
            "fixture pair identity")
    require(object_sha({"x": 1})
            == hashlib.sha256(b'{"x":1}').hexdigest(),
            "fixture independent hash")
    with tempfile.TemporaryDirectory(prefix="cm2-c28-v2-verifier-") as raw:
        path = Path(raw) / "verification.json"
        body = {"schema": VERIFICATION_SCHEMA, "formal_credit": 0}
        value = {**body, "verification_sha256": object_sha(body)}
        path.write_bytes(wire(value) + b"\n")
        require(path.read_bytes() == wire(value) + b"\n",
                "fixture canonical verification")
    zero = "0" * 64
    adapter = {
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
    adapter["contract_sha256"] = object_sha(adapter)
    contract_ok(adapter)
    pending = dict(adapter)
    pending["status"] = "PENDING_C27R2_TERMINAL"
    rejected_pending = False
    try:
        contract_ok(pending)
    except Reject:
        rejected_pending = True
    require(rejected_pending is True, "fixture pending adapter rejects")
    return {
        "schema": VERIFICATION_SCHEMA + ".self-test",
        "status": (
            "PASS_SMALL_FIXTURE_INDEPENDENT_PAIR_CLOSURE_AND_DYNAMIC_"
            "ADAPTER_FAIL_CLOSED_TESTS"
        ),
        "formal_credit": 0, "CM2": "NO-GO_FOR_CLAIM",
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
    value.add_argument("--producer")
    value.add_argument("--expect-producer-sha256")
    value.add_argument("--expect-verifier-sha256")
    value.add_argument("--candidate-dir")
    value.add_argument("--out-file")
    return value


def main() -> int:
    args = parser().parse_args()
    names = (
        "c27r2_terminal_dir", "authority_contract",
        "expect_authority_contract_sha256", "expect_terminal_root_sha256",
        "expect_terminal_receipt_file_sha256",
        "expect_terminal_receipt_object_sha256", "producer",
        "expect_producer_sha256", "expect_verifier_sha256", "candidate_dir",
        "out_file",
    )
    try:
        if args.self_test:
            require(all(getattr(args, name) is None for name in names),
                    "self-test accepts no authority/candidate/output arguments")
            result = self_test()
        else:
            require(all(getattr(args, name) is not None for name in names),
                    "all authority/source/candidate/output arguments required")
            result = verify(args)
        sys.stdout.buffer.write(wire({
            "status": result["status"], "formal_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        }) + b"\n")
        return 0
    except (Reject, OSError, ValueError, KeyError, TypeError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
