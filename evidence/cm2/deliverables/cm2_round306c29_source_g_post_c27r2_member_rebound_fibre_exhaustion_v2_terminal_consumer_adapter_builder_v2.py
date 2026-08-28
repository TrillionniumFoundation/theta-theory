#!/usr/bin/env python3
"""Normalize one minted C27R2/C28 terminal for the C29-v2 core.

This is an explicit consumer view, not a legacy alias and not new authority.
It verifies the original six-file terminal, every root/payload manifest member,
the receipt/replay/PASS pins, and the terminal-pinned producer payload before
writing an acyclic five-file adapter.  The adapter projection names only the
original terminal pins; its own root is externally pinned by downstream run
control, so no SHA fixed point exists.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
AUDIT = ROOT / ".cm2-runtime/audit"
ADAPTER_SCHEMA = (
    "cm2.round306c29.source-g-post-c27r2-member-rebound-fibre-exhaustion."
    "v2.terminal-consumer-adapter-receipt.v3"
)
C27_PROJECTION_SCHEMA = "cm2.round306c27r2.c29-consumer-projection.v1"
C28_PROJECTION_SCHEMA = "cm2.round306c28-v2.c29-consumer-projection.v1"
C27_RECEIPT_SCHEMA = "cm2.round306c27r2.source-g-authority-v2.terminal-receipt.v1"
C27_REPLAY_SCHEMA = "cm2.round306c27r2.source-g-authority-v2.terminal-byte-replay.v1"
C27_CHAIN_SCHEMA = "cm2.round306c27r2.source-g-authority-v2.release-chain-status.v1"
C27_STATUS = "PASS_C27R2_TERMINAL_BYTE_REPLAY__FORMAL_C27R2_AUTHORITY_MINTED"
C27_PASS = b"PASS_C27R2_AUTHORITY_V2_TERMINAL_BYTE_REPLAY__C28_C29_UNAUTHORIZED\n"
C27_ROOT = "1f65a624c889773e3104c4311788fc06be04d6ca92e033205074b8cc7f5b27fc"
C27_RECEIPT_FILE = "feccb0b9290bd82ac1d8e78e8e7a21d4f25e0ca3aa3556cc3f0bb6007f61c3dd"
C27_RECEIPT_OBJECT = "8afbd127c9518f569c2f7b3edcdbe9e0ebf77d88bcca855822e58d21e5cfe782"
C27_REPLAY_FILE = "b480df4b8caaf9876a48720f92a8fb6d86e2b1b5966bcc71b0022c5e49fc12ee"
C27_REPLAY_OBJECT = "216d2592c49b0302de0042677ce54c96cd5ad1fcb32231da02b39c003cb837e8"
C27_PASS_SHA = "5fe4140b3e8f38196e9ca68cd336ae29be1c8847c7685526f08aa4d7173d7348"
C28_BASE = "cm2.round306c28.source-g-post-c27r2-125561998198-pair-routing.v2."
C28_RECEIPT_SCHEMA = C28_BASE + "terminal-receipt.v1"
C28_REPLAY_SCHEMA = C28_BASE + "terminal-byte-replay.v1"
C28_CHAIN_SCHEMA = C28_BASE + "release-chain-status.v1"
C28_STATUS = "PASS_C28_TERMINAL_BYTE_REPLAY__FORMAL_C28_PAIR_ROUTING_AUTHORITY_MINTED"
C28_PASS = b"PASS_C28_PAIR_ROUTING_V2_TERMINAL_BYTE_REPLAY__C29_UNAUTHORIZED\n"
C27_RESULT_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "producer-result.v1"
)
C27_RESULT_STATUS = (
    "PASS_FRESH_ACTUAL_V2_SEED1_QUOTIENT_REBUILD_ZERO_CREDIT__PENDING_"
    "NO_IMPORT_SEED2_VERIFICATION_ATTACKS_COLD_REPLAY_AND_TERMINAL_SEAL"
)
C28_RESULT_SCHEMA = C28_BASE + "producer-result.v1"
C28_RESULT_STATUS = (
    "PASS_POST_C27R2_PARTITION_502204_MEMBERS_43684_COMPONENTS_AND_"
    "32896_PAIR_SHARDS_REBUILT__125561998198_EXACT_NONEDGE_CANDIDATE_"
    "ZERO_CREDIT__C28_UNAUTHORIZED_PENDING_RELEASE_TERMINAL"
)
C27_CENSUS = {
    "frozen_C15_members": 502_204, "frozen_C15_components": 57_876,
    "proof_derived_component_edges": 14_860, "successful_DSU_merges": 14_192,
    "cycle_edges": 668, "post_C27R2_components": 43_684,
    "total_unordered_member_pairs": 126_104_177_706,
    "within_post_component_member_pairs": 542_179_508,
    "cross_post_component_member_pairs": 125_561_998_198,
}
C28_CENSUS = {
    "members": 502_204, "post_C27R2_components": 43_684,
    "total_unordered_member_pairs": 126_104_177_706,
    "within_post_component_member_pairs": 542_179_508,
    "cross_post_component_member_pairs": 125_561_998_198,
    "blocks": 256, "shards": 32_896,
}
OUTPUTS = {"PASS.lock", "c29_consumer_projection.json",
           "payload_manifest.sha256", "root_manifest.sha256",
           "terminal_receipt.json"}


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def valid_sha(value: Any) -> bool:
    return (type(value) is str and len(value) == 64
            and all(char in "0123456789abcdef" for char in value))


def strict(payload: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(key not in result, "duplicate JSON key:" + key)
            result[key] = value
        return result
    return json.loads(payload, object_pairs_hook=pairs,
                      parse_constant=lambda token: (_ for _ in ()).throw(
                          Failure("non-finite JSON:" + token)))


def workspace(raw: str | Path, *, absent: bool = False) -> Path:
    supplied = Path(raw)
    path = (ROOT / supplied if not supplied.is_absolute() else supplied).absolute()
    try:
        relative = path.relative_to(ROOT)
    except ValueError as error:
        raise Failure("outside workspace:" + str(raw)) from error
    need(relative.parts and all(part not in {"", ".", ".."}
                                for part in relative.parts), "canonical path")
    cursor = ROOT
    for part in relative.parts:
        cursor /= part
        if not cursor.exists():
            need(absent, "missing path:" + str(cursor))
            break
        need(not cursor.is_symlink(), "symlink path:" + str(cursor))
    return path


def relative(path: Path) -> str:
    return path.absolute().relative_to(ROOT).as_posix()


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns,
            value.st_uid, value.st_gid)


class Capture:
    def __init__(self, path: Path, label: str):
        self.path = workspace(path)
        self.label = label
        self.fd = os.open(self.path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                          | getattr(os, "O_NOFOLLOW", 0))
        self.before = os.fstat(self.fd)
        need(stat.S_ISREG(self.before.st_mode) and self.before.st_nlink == 1,
             label + ":regular-single-link")
        self.sha256 = self._sha()

    def _sha(self) -> str:
        os.lseek(self.fd, 0, os.SEEK_SET)
        state = hashlib.sha256()
        while block := os.read(self.fd, 4 << 20):
            state.update(block)
        os.lseek(self.fd, 0, os.SEEK_SET)
        need(fingerprint(os.fstat(self.fd)) == fingerprint(self.before),
             self.label + ":stable-fd")
        return state.hexdigest()

    def bytes(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        blocks: list[bytes] = []
        while block := os.read(self.fd, 4 << 20):
            blocks.append(block)
        os.lseek(self.fd, 0, os.SEEK_SET)
        need(fingerprint(os.fstat(self.fd)) == fingerprint(self.before),
             self.label + ":stable-read")
        return b"".join(blocks)

    def document(self, closure: str) -> dict[str, Any]:
        payload = self.bytes()
        need(payload.endswith(b"\n") and not payload.endswith(b"\n\n"),
             self.label + ":newline")
        value = strict(payload[:-1])
        need(type(value) is dict and canonical(value) == payload[:-1],
             self.label + ":canonical")
        body = dict(value)
        claim = body.pop(closure, None)
        need(valid_sha(claim) and claim == digest(body), self.label + ":closure")
        return value

    def attest(self) -> dict[str, Any]:
        need(fingerprint(os.fstat(self.fd)) == fingerprint(self.before)
             and fingerprint(os.stat(self.path, follow_symlinks=False))
                 == fingerprint(self.before)
             and self._sha() == self.sha256,
             self.label + ":pre-post-sha-stat")
        return {"path": relative(self.path), "sha256": self.sha256,
                "size": self.before.st_size,
                "stat_fingerprint": list(fingerprint(self.before))}

    def close(self) -> None:
        os.close(self.fd)


def parse_manifest(capture: Capture) -> dict[str, str]:
    payload = capture.bytes()
    need(payload.endswith(b"\n") and not payload.endswith(b"\n\n"),
         capture.label + ":manifest newline")
    result: dict[str, str] = {}
    for line in payload.decode("ascii").splitlines():
        fields = line.split("  ", 1)
        need(len(fields) == 2 and valid_sha(fields[0])
             and fields[1] not in result, capture.label + ":manifest row")
        path = workspace(fields[1])
        need(relative(path) == fields[1], capture.label + ":manifest path")
        member = Capture(path, capture.label + ":member")
        try:
            need(member.sha256 == fields[0], capture.label + ":member SHA")
        finally:
            member.close()
        result[fields[1]] = fields[0]
    need(result and list(result) == sorted(result), capture.label + ":sorted")
    return result


def manifest(entries: dict[str, str], *, basenames: bool = False) -> bytes:
    rows = []
    for path, sha in sorted(entries.items()):
        need(valid_sha(sha), "manifest SHA")
        rows.append(sha + "  " + (Path(path).name if basenames else path) + "\n")
    return "".join(rows).encode("ascii")


def write_once(path: Path, payload: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                         | getattr(os, "O_NOFOLLOW", 0), 0o400)
    try:
        offset = 0
        while offset < len(payload):
            offset += os.write(descriptor, payload[offset:])
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def deep_values(value: Any, key: str) -> list[Any]:
    result: list[Any] = []
    if type(value) is dict:
        for name, item in value.items():
            if name == key:
                result.append(item)
            result.extend(deep_values(item, key))
    elif type(value) is list:
        for item in value:
            result.extend(deep_values(item, key))
    return result


def terminal(args: argparse.Namespace) -> tuple[dict[str, Any], list[Capture],
                                                 dict[str, dict[str, Any]]]:
    kind = args.kind
    need(kind in {"C27R2", "C28"}, "authority kind")
    supplied = (args.expect_source_root_sha256,
                args.expect_source_receipt_file_sha256,
                args.expect_source_receipt_object_sha256,
                args.expect_source_replay_file_sha256,
                args.expect_source_replay_object_sha256,
                args.expect_source_pass_lock_sha256)
    need(all(valid_sha(value) for value in supplied), "source pins")
    if kind == "C27R2":
        need(supplied == (C27_ROOT, C27_RECEIPT_FILE, C27_RECEIPT_OBJECT,
                          C27_REPLAY_FILE, C27_REPLAY_OBJECT, C27_PASS_SHA),
             "immutable C27R2 exact pins")
    base = workspace(args.source_terminal_dir)
    need(base.parent == AUDIT and base.is_dir()
         and {entry.name for entry in base.iterdir()} == {
             "PASS.lock", "chain_status.json", "payload_manifest.sha256",
             "root_manifest.sha256", "terminal_receipt.json",
             "terminal_replay.json"}, "exact source terminal inventory")
    captures = {name: Capture(base / filename, "source-" + name)
                for name, filename in {
                    "root": "root_manifest.sha256",
                    "payload": "payload_manifest.sha256",
                    "receipt": "terminal_receipt.json",
                    "replay": "terminal_replay.json",
                    "chain": "chain_status.json", "pass": "PASS.lock"}.items()}
    try:
        receipt = captures["receipt"].document("terminal_receipt_sha256")
        replay = captures["replay"].document("terminal_replay_sha256")
        chain = captures["chain"].document("chain_status_sha256")
        need(captures["root"].sha256 == supplied[0]
             and captures["receipt"].sha256 == supplied[1]
             and receipt["terminal_receipt_sha256"] == supplied[2]
             and captures["replay"].sha256 == supplied[3]
             and replay["terminal_replay_sha256"] == supplied[4]
             and captures["pass"].sha256 == supplied[5], "source exact pins")
        status = C27_STATUS if kind == "C27R2" else C28_STATUS
        receipt_schema = C27_RECEIPT_SCHEMA if kind == "C27R2" else C28_RECEIPT_SCHEMA
        replay_schema = C27_REPLAY_SCHEMA if kind == "C27R2" else C28_REPLAY_SCHEMA
        chain_schema = C27_CHAIN_SCHEMA if kind == "C27R2" else C28_CHAIN_SCHEMA
        pass_bytes = C27_PASS if kind == "C27R2" else C28_PASS
        need(captures["pass"].bytes() == pass_bytes, "source exact PASS bytes")
        need(receipt.get("schema") == receipt_schema
             and receipt.get("status") == status
             and receipt.get("authority_minted") is True
             and receipt.get("manifest_authorized") is True
             and receipt.get("terminal_replay_completed") is True
             and receipt.get("terminal_receipt_byte_replay_identical") is True
             and receipt.get("formal_credit") == 0
             and receipt.get("CM2") == "NO-GO_FOR_CLAIM", "source receipt semantics")
        need(replay.get("schema") == replay_schema
             and replay.get("status") == status
             and replay.get("terminal_receipt_file_sha256") == supplied[1]
             and replay.get("terminal_receipt_object_sha256") == supplied[2]
             and replay.get("terminal_root_manifest_sha256") == supplied[0]
             and replay.get("terminal_payload_manifest_sha256")
                 == captures["payload"].sha256
             and replay.get("terminal_receipt_byte_replay_identical") is True
             and replay.get("authority_minted") is True
             and replay.get("manifest_authorized") is True
             and replay.get("formal_credit") == 0, "source replay semantics")
        need(chain.get("schema") == chain_schema and chain.get("status") == status
             and chain.get("terminal_receipt_file_sha256") == supplied[1]
             and chain.get("terminal_receipt_object_sha256") == supplied[2]
             and chain.get("terminal_replay_file_sha256") == supplied[3]
             and chain.get("terminal_replay_object_sha256") == supplied[4]
             and chain.get("authority_minted") is True
             and chain.get("manifest_authorized") is True, "source chain semantics")
        root_entries = parse_manifest(captures["root"])
        payload_entries = parse_manifest(captures["payload"])
        need(receipt.get("terminal_root_manifest_sha256") == supplied[0]
             and receipt.get("terminal_payload_manifest_sha256")
                 == captures["payload"].sha256
             and root_entries.get(relative(captures["payload"].path))
                 == captures["payload"].sha256, "source root/payload closure")
        if kind == "C28":
            values = deep_values(receipt, "C27R2_terminal_root_manifest_sha256")
            need(values and all(value == C27_ROOT for value in values),
                 "C28 binds exact C27R2 terminal root")
        result_schema = C27_RESULT_SCHEMA if kind == "C27R2" else C28_RESULT_SCHEMA
        result_status = C27_RESULT_STATUS if kind == "C27R2" else C28_RESULT_STATUS
        result_matches: list[tuple[str, dict[str, Any], Capture]] = []
        for path in payload_entries:
            if Path(path).name not in {"result.json",
                    "cm2_round306c27r2_source_g_actual_v2_fresh_quotient_rebuild_v2_result.json"}:
                continue
            capture = Capture(workspace(path), "source-result-candidate")
            try:
                value = capture.document("result_sha256")
            except (Failure, OSError, ValueError, KeyError, TypeError):
                capture.close()
                continue
            if value.get("schema") == result_schema and value.get("status") == result_status:
                result_matches.append((path, value, capture))
            else:
                capture.close()
        need(len(result_matches) == 1, "unique source producer result")
        result_path, result, result_capture = result_matches[0]
        captures["selected-result"] = result_capture
        need(result.get("formal_credit") == 0
             and result.get("manifest_authorized") is False, "source result zero credit")
        selected: dict[str, dict[str, Any]] = {
            "producer_result": {"path": result_path,
                "file_sha256": result_capture.sha256,
                "object_sha256": result["result_sha256"]}}
        if kind == "C27R2":
            need(result.get("exact_census") == C27_CENSUS, "C27 result census")
            ledgers = result.get("ledgers")
            need(type(ledgers) is dict, "C27 ledgers")
            for role, basename, count in (
                ("member_to_post_component", "member_to_post_component.jsonl.gz", 502_204),
                ("post_component_census", "post_component_census.jsonl.gz", 43_684)):
                matches = [path for path in payload_entries if Path(path).name == basename]
                need(len(matches) == 1, "unique C27 payload:" + role)
                capture = Capture(workspace(matches[0]), "selected-" + role)
                captures["selected-" + role] = capture
                descriptor = ledgers.get(role)
                need(type(descriptor) is dict and descriptor.get("sha256") == capture.sha256
                     and descriptor.get("row_count") == count
                     and descriptor.get("gzip_mtime") == 0
                     and descriptor.get("canonical_jsonl") is True,
                     "C27 descriptor:" + role)
                selected[role] = {"path": matches[0], "file_sha256": capture.sha256}
        else:
            partition = result.get("post_C27R2_partition_census", {})
            routes = result.get("pair_route_census", {})
            need(receipt.get("C28_producer_result_object_sha256")
                     == result["result_sha256"]
                 and partition.get("members") == C28_CENSUS["members"]
                 and partition.get("components") == C28_CENSUS["post_C27R2_components"]
                 and partition.get("total_unordered_member_pairs") == C28_CENSUS["total_unordered_member_pairs"]
                 and partition.get("within_post_component_member_pairs") == C28_CENSUS["within_post_component_member_pairs"]
                 and partition.get("cross_post_component_member_pairs") == C28_CENSUS["cross_post_component_member_pairs"]
                 and routes.get("unordered_block_pair_shards") == C28_CENSUS["shards"]
                 and routes.get("cross_post_component_pairs_routed") == C28_CENSUS["cross_post_component_member_pairs"]
                 and routes.get("new_legal_cross_post_component_pairs") == 0
                 and routes.get("unresolved_pairs") == 0, "C28 exact result census")
            ledgers = result.get("ledgers")
            need(type(ledgers) is dict, "C28 result ledger descriptors")
            for role, basename, count in (
                ("member_home_block_census", "member_home_block_census.jsonl.gz", 256),
                ("cross_component_pair_route_shard",
                 "cross_component_pair_route_shard.jsonl.gz", 32_896)):
                matches = [path for path in payload_entries
                           if Path(path).name == basename]
                need(len(matches) == 1, "unique C28 payload ledger:" + role)
                capture = Capture(workspace(matches[0]), "selected-C28-" + role)
                captures["selected-C28-" + role] = capture
                descriptor = ledgers.get(role)
                need(type(descriptor) is dict
                     and descriptor.get("filename") == basename
                     and descriptor.get("sha256") == capture.sha256
                     and descriptor.get("size") == capture.before.st_size
                     and descriptor.get("row_count") == count
                     and valid_sha(descriptor.get("row_sequence_sha256"))
                     and descriptor.get("gzip_mtime") == 0
                     and descriptor.get("canonical_jsonl") is True,
                     "C28 terminal-pinned ledger descriptor:" + role)
            values = deep_values(result, "terminal_root_manifest_sha256")
            need(C27_ROOT in values, "C28 result binds original C27R2 terminal")
        source = {"root": supplied[0], "receipt_file": supplied[1],
                  "receipt_object": supplied[2], "replay_file": supplied[3],
                  "replay_object": supplied[4], "pass_sha": supplied[5],
                  "status": status, "payload_sha": captures["payload"].sha256,
                  "chain_object": chain["chain_status_sha256"]}
        return source, list(captures.values()), selected
    except BaseException:
        for capture in captures.values():
            capture.close()
        raise


def build(args: argparse.Namespace) -> dict[str, Any]:
    need(valid_sha(args.expect_builder_sha256), "builder pin")
    source_capture = Capture(SELF, "builder-source")
    try:
        need(source_capture.sha256 == args.expect_builder_sha256, "builder self pin")
    finally:
        source_capture.close()
    output = workspace(args.output_dir, absent=True)
    need(output.parent == AUDIT and not output.exists(), "fresh adapter output")
    source, captures, selected = terminal(args)
    try:
        if args.preflight_only:
            return {"status": "PASS_C29_V2_SOURCE_TERMINAL_CONSUMER_ADAPTER_PREFLIGHT__NO_OUTPUT_ZERO_CREDIT"}
        output.mkdir(mode=0o700)
        kind = args.kind
        pass_bytes = (b"PASS_C29_V2_C27R2_TERMINAL_CONSUMER_ADAPTER__ZERO_CREDIT\n"
                      if kind == "C27R2" else
                      b"PASS_C29_V2_C28_TERMINAL_CONSUMER_ADAPTER__ZERO_CREDIT\n")
        write_once(output / "PASS.lock", pass_bytes)
        projection_body = {
            "schema": C27_PROJECTION_SCHEMA if kind == "C27R2" else C28_PROJECTION_SCHEMA,
            "status": ("PASS_C27R2_TERMINAL_AUTHORITY_FOR_C29_CONSUMER"
                       if kind == "C27R2" else
                       "PASS_C28_V2_TERMINAL_AUTHORITY_FOR_C29_CONSUMER"),
            "terminal_replay_passed": True, "authority_minted": True,
            "terminal_root_manifest_sha256": source["root"],
            "terminal_receipt_file_sha256": source["receipt_file"],
            "terminal_receipt_object_sha256": source["receipt_object"],
            "terminal_replay_file_sha256": source["replay_file"],
            "terminal_replay_object_sha256": source["replay_object"],
            "terminal_status": source["status"],
            "PASS_lock_sha256": hashlib.sha256(pass_bytes).hexdigest(),
            "payload_members": selected,
            "exact_census": C27_CENSUS if kind == "C27R2" else C28_CENSUS,
            "authority_adapter_not_legacy_alias": True,
            "source_terminal_fully_replayed": True,
            "formal_credit": 0, "C29": "UNAUTHORIZED",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        if kind == "C28":
            projection_body.update({
                "C27R2_terminal_root_manifest_sha256": C27_ROOT,
                "B2_pair_routing_complete": True,
                "component_maximality_complete": True,
                "new_legal_cross_component_pairs": 0, "unresolved_pairs": 0})
        projection = dict(projection_body)
        projection["projection_sha256"] = digest(projection)
        projection_path = output / "c29_consumer_projection.json"
        write_once(projection_path, canonical(projection) + b"\n")
        payload_entries = {item["path"]: item["file_sha256"]
                           for item in selected.values()}
        payload_entries[relative(projection_path)] = hashlib.sha256(
            canonical(projection) + b"\n").hexdigest()
        payload_raw = manifest(payload_entries)
        write_once(output / "payload_manifest.sha256", payload_raw)
        status = ("PASS_C29_V2_C27R2_TERMINAL_CONSUMER_ADAPTER__ZERO_CREDIT"
                  if kind == "C27R2" else
                  "PASS_C29_V2_C28_TERMINAL_CONSUMER_ADAPTER__ZERO_CREDIT")
        receipt_body = {
            "schema": ADAPTER_SCHEMA, "status": status,
            "authority_kind": kind, "terminal_replay_passed": True,
            "authority_minted": True,
            "source_terminal_dir": relative(workspace(args.source_terminal_dir)),
            "source_terminal_root_manifest_sha256": source["root"],
            "source_terminal_receipt_file_sha256": source["receipt_file"],
            "source_terminal_receipt_object_sha256": source["receipt_object"],
            "source_terminal_replay_file_sha256": source["replay_file"],
            "source_terminal_replay_object_sha256": source["replay_object"],
            "source_terminal_pass_lock_sha256": source["pass_sha"],
            "source_terminal_payload_manifest_sha256": source["payload_sha"],
            "source_terminal_chain_status_object_sha256": source["chain_object"],
            "source_terminal_status": source["status"],
            "consumer_projection_file_sha256": hashlib.sha256(
                canonical(projection) + b"\n").hexdigest(),
            "consumer_projection_object_sha256": projection["projection_sha256"],
            "payload_manifest_sha256": hashlib.sha256(payload_raw).hexdigest(),
            "authority_adapter_not_legacy_alias": True,
            "formal_credit": 0, "manifest_authorized": False,
            "C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM"}
        receipt = dict(receipt_body)
        receipt["terminal_receipt_sha256"] = digest(receipt)
        receipt_raw = canonical(receipt) + b"\n"
        write_once(output / "terminal_receipt.json", receipt_raw)
        root_raw = manifest({"payload_manifest.sha256": hashlib.sha256(payload_raw).hexdigest(),
                             "terminal_receipt.json": hashlib.sha256(receipt_raw).hexdigest()},
                            basenames=True)
        write_once(output / "root_manifest.sha256", root_raw)
        need({entry.name for entry in output.iterdir()} == OUTPUTS,
             "exact adapter inventory")
        for capture in captures:
            capture.attest()
        return receipt
    finally:
        for capture in captures:
            capture.close()


def self_test() -> dict[str, Any]:
    body = {"schema": ADAPTER_SCHEMA, "formal_credit": 0}
    closed = dict(body)
    closed["terminal_receipt_sha256"] = digest(closed)
    need(closed["terminal_receipt_sha256"] == digest(body), "closure fixture")
    with tempfile.TemporaryDirectory(prefix="c29-adapter-v1-") as raw:
        path = Path(raw) / "x"
        path.write_bytes(b"x")
        need(hashlib.sha256(path.read_bytes()).hexdigest()
             == hashlib.sha256(b"x").hexdigest(), "file fixture")
    return {"status": "PASS_C29_V2_TERMINAL_ADAPTER_BUILDER_SELF_TEST",
            "formal_credit": 0, "C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM"}


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--self-test", action="store_true")
    value.add_argument("--preflight-only", action="store_true")
    value.add_argument("--kind", choices=("C27R2", "C28"))
    for name in ("source-terminal-dir", "expect-source-root-sha256",
                 "expect-source-receipt-file-sha256",
                 "expect-source-receipt-object-sha256",
                 "expect-source-replay-file-sha256",
                 "expect-source-replay-object-sha256",
                 "expect-source-pass-lock-sha256", "expect-builder-sha256",
                 "output-dir"):
        value.add_argument("--" + name)
    return value


def main() -> int:
    args = parser().parse_args()
    fields = ("kind", "source_terminal_dir", "expect_source_root_sha256",
              "expect_source_receipt_file_sha256",
              "expect_source_receipt_object_sha256",
              "expect_source_replay_file_sha256",
              "expect_source_replay_object_sha256",
              "expect_source_pass_lock_sha256", "expect_builder_sha256",
              "output_dir")
    try:
        if args.self_test:
            need(not args.preflight_only
                 and all(getattr(args, field) is None for field in fields),
                 "self-test arguments")
            result = self_test()
        else:
            need(all(getattr(args, field) is not None for field in fields),
                 "all adapter arguments")
            result = build(args)
        sys.stdout.buffer.write(canonical({"CM2": "NO-GO_FOR_CLAIM",
            "formal_credit": 0, "status": result["status"]}) + b"\n")
        return 0
    except (Failure, OSError, ValueError, KeyError, TypeError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
