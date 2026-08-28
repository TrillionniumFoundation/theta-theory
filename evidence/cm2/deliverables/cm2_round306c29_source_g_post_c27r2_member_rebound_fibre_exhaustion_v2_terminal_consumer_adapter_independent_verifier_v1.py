#!/usr/bin/env python3
"""No-import independent verifier for a C29-v2 terminal consumer adapter."""

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
C27_PROJECTION = "cm2.round306c27r2.c29-consumer-projection.v1"
C28_PROJECTION = "cm2.round306c28-v2.c29-consumer-projection.v1"
C27_BASE = "cm2.round306c27r2.source-g-authority-v2."
C28_BASE = "cm2.round306c28.source-g-post-c27r2-125561998198-pair-routing.v2."
C27_STATUS = "PASS_C27R2_TERMINAL_BYTE_REPLAY__FORMAL_C27R2_AUTHORITY_MINTED"
C28_STATUS = "PASS_C28_TERMINAL_BYTE_REPLAY__FORMAL_C28_PAIR_ROUTING_AUTHORITY_MINTED"
C27_PASS = b"PASS_C27R2_AUTHORITY_V2_TERMINAL_BYTE_REPLAY__C28_C29_UNAUTHORIZED\n"
C28_PASS = b"PASS_C28_PAIR_ROUTING_V2_TERMINAL_BYTE_REPLAY__C29_UNAUTHORIZED\n"
C27_ROOT = "1f65a624c889773e3104c4311788fc06be04d6ca92e033205074b8cc7f5b27fc"
C27_PINS = (
    C27_ROOT,
    "feccb0b9290bd82ac1d8e78e8e7a21d4f25e0ca3aa3556cc3f0bb6007f61c3dd",
    "8afbd127c9518f569c2f7b3edcdbe9e0ebf77d88bcca855822e58d21e5cfe782",
    "b480df4b8caaf9876a48720f92a8fb6d86e2b1b5966bcc71b0022c5e49fc12ee",
    "216d2592c49b0302de0042677ce54c96cd5ad1fcb32231da02b39c003cb837e8",
    "5fe4140b3e8f38196e9ca68cd336ae29be1c8847c7685526f08aa4d7173d7348",
)
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
C27_CENSUS = {"frozen_C15_members": 502204, "frozen_C15_components": 57876,
    "proof_derived_component_edges": 14860, "successful_DSU_merges": 14192,
    "cycle_edges": 668, "post_C27R2_components": 43684,
    "total_unordered_member_pairs": 126104177706,
    "within_post_component_member_pairs": 542179508,
    "cross_post_component_member_pairs": 125561998198}
C28_CENSUS = {"members": 502204, "post_C27R2_components": 43684,
    "total_unordered_member_pairs": 126104177706,
    "within_post_component_member_pairs": 542179508,
    "cross_post_component_member_pairs": 125561998198,
    "blocks": 256, "shards": 32896}
ADAPTER_FILES = {"PASS.lock", "c29_consumer_projection.json",
                 "payload_manifest.sha256", "root_manifest.sha256",
                 "terminal_receipt.json"}


class Failure(RuntimeError):
    pass


def require(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def encode(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def object_sha(value: Any) -> str:
    return hashlib.sha256(encode(value)).hexdigest()


def valid_sha(value: Any) -> bool:
    return (type(value) is str and len(value) == 64
            and all(char in "0123456789abcdef" for char in value))


def decode(payload: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            require(key not in result, "duplicate JSON key")
            result[key] = value
        return result
    return json.loads(payload, object_pairs_hook=pairs,
                      parse_constant=lambda token: (_ for _ in ()).throw(
                          Failure("non-finite JSON:" + token)))


def path_in(raw: str | Path, *, absent: bool = False) -> Path:
    supplied = Path(raw)
    path = (ROOT / supplied if not supplied.is_absolute() else supplied).absolute()
    try:
        relative = path.relative_to(ROOT)
    except ValueError as error:
        raise Failure("outside workspace") from error
    require(relative.parts and all(part not in {"", ".", ".."}
                                   for part in relative.parts), "canonical path")
    cursor = ROOT
    for part in relative.parts:
        cursor /= part
        if not cursor.exists():
            require(absent, "missing path")
            break
        require(not cursor.is_symlink(), "symlink path")
    return path


def rel(path: Path) -> str:
    return path.absolute().relative_to(ROOT).as_posix()


def fingerprint(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink,
            info.st_size, info.st_mtime_ns, info.st_ctime_ns,
            info.st_uid, info.st_gid)


def hash_file(path: Path) -> str:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                         | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
                "regular single-link")
        state = hashlib.sha256()
        while block := os.read(descriptor, 4 << 20):
            state.update(block)
        require(fingerprint(os.fstat(descriptor)) == fingerprint(before),
                "stable file hash")
        return state.hexdigest()
    finally:
        os.close(descriptor)


def document(path: Path, closure: str) -> dict[str, Any]:
    payload = path.read_bytes()
    require(payload.endswith(b"\n") and not payload.endswith(b"\n\n"),
            "document newline")
    value = decode(payload[:-1])
    require(type(value) is dict and encode(value) == payload[:-1],
            "canonical document")
    body = dict(value)
    claim = body.pop(closure, None)
    require(valid_sha(claim) and claim == object_sha(body), "document closure")
    return value


def manifest(path: Path, *, local: bool = False) -> dict[str, str]:
    payload = path.read_bytes()
    require(payload.endswith(b"\n") and not payload.endswith(b"\n\n"),
            "manifest newline")
    result: dict[str, str] = {}
    for line in payload.decode("ascii").splitlines():
        fields = line.split("  ", 1)
        require(len(fields) == 2 and valid_sha(fields[0])
                and fields[1] not in result, "manifest row")
        if not local:
            member = path_in(fields[1])
            require(rel(member) == fields[1] and hash_file(member) == fields[0],
                    "manifest member")
        result[fields[1]] = fields[0]
    require(result and list(result) == sorted(result), "manifest sorted")
    return result


def deep(value: Any, key: str) -> list[Any]:
    result: list[Any] = []
    if type(value) is dict:
        for name, item in value.items():
            if name == key:
                result.append(item)
            result.extend(deep(item, key))
    elif type(value) is list:
        for item in value:
            result.extend(deep(item, key))
    return result


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


def source_terminal(args: argparse.Namespace) -> tuple[dict[str, Any],
                                                        dict[str, str]]:
    kind = args.kind
    pins = (args.expect_source_root_sha256,
            args.expect_source_receipt_file_sha256,
            args.expect_source_receipt_object_sha256,
            args.expect_source_replay_file_sha256,
            args.expect_source_replay_object_sha256,
            args.expect_source_pass_lock_sha256)
    require(all(valid_sha(value) for value in pins), "source pin syntax")
    if kind == "C27R2":
        require(pins == C27_PINS, "immutable C27 pins")
    base = path_in(args.source_terminal_dir)
    require(base.parent == AUDIT and base.is_dir()
            and {entry.name for entry in base.iterdir()} == {
                "PASS.lock", "chain_status.json", "payload_manifest.sha256",
                "root_manifest.sha256", "terminal_receipt.json",
                "terminal_replay.json"}, "source terminal inventory")
    files = {name: base / filename for name, filename in {
        "pass": "PASS.lock", "chain": "chain_status.json",
        "payload": "payload_manifest.sha256", "root": "root_manifest.sha256",
        "receipt": "terminal_receipt.json", "replay": "terminal_replay.json"}.items()}
    receipt = document(files["receipt"], "terminal_receipt_sha256")
    replay = document(files["replay"], "terminal_replay_sha256")
    chain = document(files["chain"], "chain_status_sha256")
    require((hash_file(files["root"]), hash_file(files["receipt"]),
             receipt["terminal_receipt_sha256"], hash_file(files["replay"]),
             replay["terminal_replay_sha256"], hash_file(files["pass"])) == pins,
            "source exact pins")
    status = C27_STATUS if kind == "C27R2" else C28_STATUS
    base_schema = C27_BASE if kind == "C27R2" else C28_BASE
    expected_pass = C27_PASS if kind == "C27R2" else C28_PASS
    require(files["pass"].read_bytes() == expected_pass, "source PASS bytes")
    require(receipt.get("schema") == base_schema + "terminal-receipt.v1"
            and receipt.get("status") == status
            and receipt.get("authority_minted") is True
            and receipt.get("manifest_authorized") is True
            and receipt.get("terminal_replay_completed") is True
            and receipt.get("terminal_receipt_byte_replay_identical") is True
            and receipt.get("formal_credit") == 0, "source receipt")
    require(replay.get("schema") == base_schema + "terminal-byte-replay.v1"
            and replay.get("status") == status
            and replay.get("terminal_receipt_file_sha256") == pins[1]
            and replay.get("terminal_receipt_object_sha256") == pins[2]
            and replay.get("terminal_root_manifest_sha256") == pins[0]
            and replay.get("terminal_payload_manifest_sha256") == hash_file(files["payload"])
            and replay.get("terminal_receipt_byte_replay_identical") is True
            and replay.get("authority_minted") is True, "source replay")
    require(chain.get("schema") == base_schema + "release-chain-status.v1"
            and chain.get("status") == status
            and chain.get("terminal_receipt_file_sha256") == pins[1]
            and chain.get("terminal_receipt_object_sha256") == pins[2]
            and chain.get("terminal_replay_file_sha256") == pins[3]
            and chain.get("terminal_replay_object_sha256") == pins[4]
            and chain.get("authority_minted") is True, "source chain")
    root_entries = manifest(files["root"])
    payload_entries = manifest(files["payload"])
    require(receipt.get("terminal_root_manifest_sha256") == pins[0]
            and receipt.get("terminal_payload_manifest_sha256") == hash_file(files["payload"])
            and root_entries.get(rel(files["payload"])) == hash_file(files["payload"]),
            "source root/payload")
    if kind == "C28":
        values = deep(receipt, "C27R2_terminal_root_manifest_sha256")
        require(values and all(value == C27_ROOT for value in values),
                "C28 binds exact C27 root")
    return {"root": pins[0], "receipt_file": pins[1],
            "receipt_object": pins[2], "replay_file": pins[3],
            "replay_object": pins[4], "pass_sha": pins[5],
            "payload_sha": hash_file(files["payload"]),
            "chain_object": chain["chain_status_sha256"],
            "status": status, "dir": rel(base)}, payload_entries


def verify(args: argparse.Namespace) -> dict[str, Any]:
    require(valid_sha(args.expect_verifier_sha256)
            and hash_file(SELF) == args.expect_verifier_sha256, "verifier self pin")
    source, source_payload = source_terminal(args)
    adapter = path_in(args.adapter_dir)
    require(adapter.parent == AUDIT and adapter.is_dir()
            and {entry.name for entry in adapter.iterdir()} == ADAPTER_FILES,
            "adapter inventory")
    pins = (args.expect_adapter_root_sha256,
            args.expect_adapter_receipt_file_sha256,
            args.expect_adapter_receipt_object_sha256)
    require(all(valid_sha(value) for value in pins), "adapter pin syntax")
    paths = {name: adapter / filename for name, filename in {
        "pass": "PASS.lock", "projection": "c29_consumer_projection.json",
        "payload": "payload_manifest.sha256", "root": "root_manifest.sha256",
        "receipt": "terminal_receipt.json"}.items()}
    receipt = document(paths["receipt"], "terminal_receipt_sha256")
    projection = document(paths["projection"], "projection_sha256")
    require((hash_file(paths["root"]), hash_file(paths["receipt"]),
             receipt["terminal_receipt_sha256"]) == pins, "adapter pins")
    kind = args.kind
    adapter_status = ("PASS_C29_V2_C27R2_TERMINAL_CONSUMER_ADAPTER__ZERO_CREDIT"
                      if kind == "C27R2" else
                      "PASS_C29_V2_C28_TERMINAL_CONSUMER_ADAPTER__ZERO_CREDIT")
    projection_status = ("PASS_C27R2_TERMINAL_AUTHORITY_FOR_C29_CONSUMER"
                         if kind == "C27R2" else
                         "PASS_C28_V2_TERMINAL_AUTHORITY_FOR_C29_CONSUMER")
    adapter_pass = (b"PASS_C29_V2_C27R2_TERMINAL_CONSUMER_ADAPTER__ZERO_CREDIT\n"
                    if kind == "C27R2" else
                    b"PASS_C29_V2_C28_TERMINAL_CONSUMER_ADAPTER__ZERO_CREDIT\n")
    require(paths["pass"].read_bytes() == adapter_pass, "adapter PASS")
    require(receipt.get("schema") == ADAPTER_SCHEMA
            and receipt.get("status") == adapter_status
            and receipt.get("authority_kind") == kind
            and receipt.get("terminal_replay_passed") is True
            and receipt.get("authority_minted") is True
            and receipt.get("source_terminal_root_manifest_sha256") == source["root"]
            and receipt.get("source_terminal_receipt_file_sha256") == source["receipt_file"]
            and receipt.get("source_terminal_receipt_object_sha256") == source["receipt_object"]
            and receipt.get("source_terminal_replay_file_sha256") == source["replay_file"]
            and receipt.get("source_terminal_replay_object_sha256") == source["replay_object"]
            and receipt.get("source_terminal_pass_lock_sha256") == source["pass_sha"]
            and receipt.get("source_terminal_payload_manifest_sha256") == source["payload_sha"]
            and receipt.get("source_terminal_chain_status_object_sha256") == source["chain_object"]
            and receipt.get("source_terminal_status") == source["status"]
            and receipt.get("formal_credit") == 0
            and receipt.get("manifest_authorized") is False,
            "adapter receipt")
    require(projection.get("schema") == (C27_PROJECTION if kind == "C27R2" else C28_PROJECTION)
            and projection.get("status") == projection_status
            and projection.get("terminal_replay_passed") is True
            and projection.get("authority_minted") is True
            and projection.get("terminal_root_manifest_sha256") == source["root"]
            and projection.get("terminal_receipt_file_sha256") == source["receipt_file"]
            and projection.get("terminal_receipt_object_sha256") == source["receipt_object"]
            and projection.get("terminal_replay_file_sha256") == source["replay_file"]
            and projection.get("terminal_replay_object_sha256") == source["replay_object"]
            and projection.get("terminal_status") == source["status"]
            and projection.get("PASS_lock_sha256") == hash_file(paths["pass"])
            and projection.get("exact_census") == (C27_CENSUS if kind == "C27R2" else C28_CENSUS)
            and projection.get("formal_credit") == 0,
            "adapter projection")
    members = projection.get("payload_members")
    required = ({"producer_result", "member_to_post_component", "post_component_census"}
                if kind == "C27R2" else {"producer_result"})
    require(type(members) is dict and set(members) == required, "projection members")
    result_schema = C27_RESULT_SCHEMA if kind == "C27R2" else C28_RESULT_SCHEMA
    result_status = C27_RESULT_STATUS if kind == "C27R2" else C28_RESULT_STATUS
    for role, item in members.items():
        require(type(item) is dict and set(item) >= {"path", "file_sha256"},
                "member descriptor")
        member = path_in(item["path"])
        require(source_payload.get(item["path"]) == item["file_sha256"]
                and hash_file(member) == item["file_sha256"], "source payload member")
        if role == "producer_result":
            value = document(member, "result_sha256")
            require(value.get("schema") == result_schema
                    and value.get("status") == result_status
                    and item.get("object_sha256") == value["result_sha256"],
                    "producer result descriptor")
    payload_expected = {item["path"]: item["file_sha256"] for item in members.values()}
    payload_expected[rel(paths["projection"])] = hash_file(paths["projection"])
    require(manifest(paths["payload"], local=True) == dict(sorted(payload_expected.items())),
            "adapter payload")
    require(manifest(paths["root"], local=True) == {
        "payload_manifest.sha256": hash_file(paths["payload"]),
        "terminal_receipt.json": hash_file(paths["receipt"])}, "acyclic adapter root")
    require(receipt.get("consumer_projection_file_sha256") == hash_file(paths["projection"])
            and receipt.get("consumer_projection_object_sha256") == projection["projection_sha256"]
            and receipt.get("payload_manifest_sha256") == hash_file(paths["payload"]),
            "adapter closure")
    if kind == "C28":
        require(projection.get("C27R2_terminal_root_manifest_sha256") == C27_ROOT
                and projection.get("B2_pair_routing_complete") is True
                and projection.get("component_maximality_complete") is True
                and projection.get("new_legal_cross_component_pairs") == 0
                and projection.get("unresolved_pairs") == 0, "C28 projection")
    out = path_in(args.out_file, absent=True)
    require(out.parent == AUDIT and not out.exists(), "fresh verification")
    body = {"schema": ADAPTER_SCHEMA + ".independent-verification.v1",
            "status": "PASS_NO_IMPORT_C29_V2_TERMINAL_CONSUMER_ADAPTER_INDEPENDENT_VERIFICATION__ZERO_CREDIT",
            "authority_kind": kind, "source_terminal": source,
            "adapter_root_manifest_sha256": pins[0],
            "adapter_receipt_file_sha256": pins[1],
            "adapter_receipt_object_sha256": pins[2],
            "projection_object_sha256": projection["projection_sha256"],
            "acyclic_root_payload_projection_binding": True,
            "no_import_or_execution_of_builder": True,
            "formal_credit": 0, "manifest_authorized": False,
            "C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM"}
    result = dict(body)
    result["verification_sha256"] = object_sha(result)
    write_once(out, encode(result) + b"\n")
    return result


def self_test() -> dict[str, Any]:
    require(object_sha({"a": 1}) == hashlib.sha256(b'{"a":1}').hexdigest(),
            "canonical fixture")
    with tempfile.TemporaryDirectory(prefix="c29-adapter-verifier-") as raw:
        path = Path(raw) / "manifest.sha256"
        path.write_text(hashlib.sha256(b"x").hexdigest() + "  x\n", encoding="ascii")
        require(manifest(path, local=True) == {
            "x": hashlib.sha256(b"x").hexdigest()}, "manifest fixture")
    return {"status": "PASS_C29_V2_ADAPTER_INDEPENDENT_VERIFIER_SELF_TEST",
            "formal_credit": 0, "C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM"}


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--self-test", action="store_true")
    value.add_argument("--kind", choices=("C27R2", "C28"))
    for name in ("source-terminal-dir", "expect-source-root-sha256",
                 "expect-source-receipt-file-sha256",
                 "expect-source-receipt-object-sha256",
                 "expect-source-replay-file-sha256",
                 "expect-source-replay-object-sha256",
                 "expect-source-pass-lock-sha256", "adapter-dir",
                 "expect-adapter-root-sha256",
                 "expect-adapter-receipt-file-sha256",
                 "expect-adapter-receipt-object-sha256",
                 "expect-verifier-sha256", "out-file"):
        value.add_argument("--" + name)
    return value


def main() -> int:
    args = parser().parse_args()
    fields = ("kind", "source_terminal_dir", "expect_source_root_sha256",
              "expect_source_receipt_file_sha256",
              "expect_source_receipt_object_sha256",
              "expect_source_replay_file_sha256",
              "expect_source_replay_object_sha256",
              "expect_source_pass_lock_sha256", "adapter_dir",
              "expect_adapter_root_sha256", "expect_adapter_receipt_file_sha256",
              "expect_adapter_receipt_object_sha256", "expect_verifier_sha256",
              "out_file")
    try:
        if args.self_test:
            require(all(getattr(args, field) is None for field in fields),
                    "self-test arguments")
            result = self_test()
        else:
            require(all(getattr(args, field) is not None for field in fields),
                    "all verifier arguments")
            result = verify(args)
        sys.stdout.buffer.write(encode({"CM2": "NO-GO_FOR_CLAIM",
            "formal_credit": 0, "status": result["status"]}) + b"\n")
        return 0
    except (Failure, OSError, ValueError, KeyError, TypeError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
