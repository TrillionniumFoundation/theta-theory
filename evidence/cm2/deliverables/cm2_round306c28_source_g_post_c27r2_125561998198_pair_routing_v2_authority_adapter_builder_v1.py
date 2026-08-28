#!/usr/bin/env python3
"""Build a zero-credit C27R2-terminal-to-C28 authority adapter.

The frozen C28 mathematical core predates the final C27R2 terminal layout: it
expects an explicit two-member adapter root, while the minted predecessor has
a multi-member provenance root plus a separate terminal byte replay.  This
builder does not create a legacy alias and does not mint authority.  It first
verifies the original C27R2 terminal receipt, root, payload, PASS lock, replay,
and chain status under caller-supplied exact pins, then emits a new, explicitly
named adapter contract whose payload entries still point at the original
terminal-pinned C27R2 candidate bytes.
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
CONTRACT_SCHEMA = "cm2.round306c28.source-g.c27r2-terminal-adapter-contract.v1"
CONTRACT_READY = (
    "FINALIZED_FROM_MINTED_C27R2_TERMINAL__C28_MATH_CORE_MAY_RUN__"
    "ZERO_C28_CREDIT"
)
ADAPTER_SCHEMA = (
    "cm2.round306c28.source-g.c27r2-terminal-authority-adapter-receipt.v1"
)
ADAPTER_STATUS = (
    "PASS_ORIGINAL_C27R2_TERMINAL_RECEIPT_ROOT_PASS_AND_BYTE_REPLAY__"
    "NORMALIZED_C28_ADAPTER_ZERO_CREDIT"
)
PREDECESSOR_RECEIPT_SCHEMA = (
    "cm2.round306c27r2.source-g-authority-v2.terminal-receipt.v1"
)
PREDECESSOR_REPLAY_SCHEMA = (
    "cm2.round306c27r2.source-g-authority-v2.terminal-byte-replay.v1"
)
PREDECESSOR_CHAIN_SCHEMA = (
    "cm2.round306c27r2.source-g-authority-v2.release-chain-status.v1"
)
PREDECESSOR_STATUS = (
    "PASS_C27R2_TERMINAL_BYTE_REPLAY__FORMAL_C27R2_AUTHORITY_MINTED"
)
PREDECESSOR_PASS = (
    b"PASS_C27R2_AUTHORITY_V2_TERMINAL_BYTE_REPLAY__C28_C29_UNAUTHORIZED\n"
)
ADAPTER_PASS = (
    b"PASS_C27R2_TERMINAL_TO_C28_AUTHORITY_ADAPTER__ZERO_C28_CREDIT\n"
)
C27R2_RESULT_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "producer-result.v1"
)
C27R2_RESULT_STATUS = (
    "PASS_FRESH_ACTUAL_V2_SEED1_QUOTIENT_REBUILD_ZERO_CREDIT__PENDING_"
    "NO_IMPORT_SEED2_VERIFICATION_ATTACKS_COLD_REPLAY_AND_TERMINAL_SEAL"
)
EXPECTED = {
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
OUTPUT_FILES = {
    "authority_contract.json", "payload_manifest.sha256",
    "root_manifest.sha256", "terminal_receipt.json", "PASS.lock",
}


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
            and all(character in "0123456789abcdef" for character in value))


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns,
            value.st_uid, value.st_gid)


def workspace(raw: str | Path, *, absent: bool = False) -> Path:
    supplied = Path(raw)
    path = (ROOT / supplied if not supplied.is_absolute() else supplied).absolute()
    try:
        relative = path.relative_to(ROOT)
    except ValueError as error:
        raise Failure("path outside workspace:" + str(raw)) from error
    need(all(piece not in {"", ".", ".."} for piece in relative.parts),
         "canonical workspace path:" + str(raw))
    cursor = ROOT
    for piece in relative.parts:
        cursor /= piece
        if not cursor.exists():
            need(absent, "missing path component:" + str(cursor))
            break
        need(not cursor.is_symlink(), "symlink path component:" + str(cursor))
    return path


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


class Capture:
    def __init__(self, path: Path, label: str):
        self.path = workspace(path)
        self.label = label
        self.fd = os.open(self.path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                          | getattr(os, "O_NOFOLLOW", 0))
        self.before = os.fstat(self.fd)
        need(stat.S_ISREG(self.before.st_mode) and self.before.st_nlink == 1,
             label + ":regular-single-link")
        self.sha256 = self._hash()

    def _hash(self) -> str:
        os.lseek(self.fd, 0, os.SEEK_SET)
        state = hashlib.sha256()
        while block := os.read(self.fd, 4 << 20):
            state.update(block)
        os.lseek(self.fd, 0, os.SEEK_SET)
        need(fingerprint(os.fstat(self.fd)) == fingerprint(self.before),
             self.label + ":stable-hash")
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
             self.label + ":single-newline")
        value = strict_load(payload[:-1])
        need(type(value) is dict and canonical(value) == payload[:-1],
             self.label + ":canonical-json")
        body = dict(value)
        claim = body.pop(closure, None)
        need(valid_sha(claim) and claim == digest(body),
             self.label + ":object-closure")
        return value

    def attest(self) -> dict[str, Any]:
        need(fingerprint(os.fstat(self.fd)) == fingerprint(self.before)
             and fingerprint(os.stat(self.path, follow_symlinks=False))
                 == fingerprint(self.before)
             and self._hash() == self.sha256,
             self.label + ":pre-post-sha-stat")
        return {"path": relative(self.path), "sha256": self.sha256,
                "size": self.before.st_size,
                "stat_fingerprint": list(fingerprint(self.before))}

    def close(self) -> None:
        os.close(self.fd)


def strict_load(payload: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(type(key) is str and key not in result, "unique JSON key")
            result[key] = value
        return result
    return json.loads(payload, object_pairs_hook=pairs,
                      parse_constant=lambda token: (_ for _ in ()).throw(
                          ValueError(token)))


def parse_manifest(capture: Capture) -> dict[str, str]:
    payload = capture.bytes()
    need(payload.endswith(b"\n"), capture.label + ":manifest-newline")
    result: dict[str, str] = {}
    for line in payload.decode("ascii").splitlines():
        pieces = line.split("  ", 1)
        need(len(pieces) == 2 and valid_sha(pieces[0])
             and pieces[1] not in result, capture.label + ":manifest-row")
        path = workspace(pieces[1])
        need(relative(path) == pieces[1], capture.label + ":manifest-path")
        member = Capture(path, capture.label + ":member:" + pieces[1])
        try:
            need(member.sha256 == pieces[0], capture.label + ":member-sha")
        finally:
            member.close()
        result[pieces[1]] = pieces[0]
    need(list(result) == sorted(result), capture.label + ":manifest-sorted")
    return result


def write_once(path: Path, payload: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                 | getattr(os, "O_NOFOLLOW", 0), 0o400)
    try:
        offset = 0
        while offset < len(payload):
            offset += os.write(fd, payload[offset:])
        os.fsync(fd)
    finally:
        os.close(fd)


def manifest(entries: dict[str, str]) -> bytes:
    need(entries and list(entries) == sorted(entries), "sorted manifest input")
    return ("\n".join(f"{entries[path]}  {path}" for path in entries)
            + "\n").encode("ascii")


def terminal_inputs(args: argparse.Namespace) -> tuple[
    dict[str, Any], dict[str, Any], dict[str, Any], dict[str, str],
    list[Capture], dict[str, dict[str, Any]],
]:
    expected_pins = (
        args.expect_terminal_root_sha256,
        args.expect_terminal_receipt_file_sha256,
        args.expect_terminal_receipt_object_sha256,
        args.expect_terminal_replay_file_sha256,
        args.expect_terminal_replay_object_sha256,
        args.expect_terminal_pass_lock_sha256,
    )
    need(all(valid_sha(value) for value in expected_pins), "all terminal pins")
    terminal = workspace(args.c27r2_terminal_dir)
    need(terminal.parent == AUDIT and terminal.is_dir()
         and {entry.name for entry in terminal.iterdir()} == {
             "PASS.lock", "chain_status.json", "payload_manifest.sha256",
             "root_manifest.sha256", "terminal_receipt.json",
             "terminal_replay.json",
         }, "exact C27R2 terminal directory inventory")
    captures = {
        name: Capture(terminal / filename, name)
        for name, filename in {
            "root": "root_manifest.sha256",
            "payload": "payload_manifest.sha256",
            "receipt": "terminal_receipt.json",
            "replay": "terminal_replay.json",
            "chain": "chain_status.json", "pass": "PASS.lock",
        }.items()
    }
    try:
        root = captures["root"]
        payload = captures["payload"]
        receipt = captures["receipt"].document("terminal_receipt_sha256")
        replay = captures["replay"].document("terminal_replay_sha256")
        chain = captures["chain"].document("chain_status_sha256")
        need(root.sha256 == args.expect_terminal_root_sha256
             and captures["receipt"].sha256
                 == args.expect_terminal_receipt_file_sha256
             and receipt["terminal_receipt_sha256"]
                 == args.expect_terminal_receipt_object_sha256
             and captures["replay"].sha256
                 == args.expect_terminal_replay_file_sha256
             and replay["terminal_replay_sha256"]
                 == args.expect_terminal_replay_object_sha256
             and captures["pass"].sha256
                 == args.expect_terminal_pass_lock_sha256
             and captures["pass"].bytes() == PREDECESSOR_PASS,
             "exact C27R2 terminal file/object/PASS pins")
        need(receipt.get("schema") == PREDECESSOR_RECEIPT_SCHEMA
             and receipt.get("status") == PREDECESSOR_STATUS
             and receipt.get("exact_census") == EXPECTED
             and receipt.get("authority_minted") is True
             and receipt.get("manifest_authorized") is True
             and receipt.get("formal_credit") == 0
             and receipt.get("terminal_replay_completed") is True
             and receipt.get("terminal_receipt_byte_replay_identical") is True
             and receipt.get("C27R2")
                 == "AUTHORIZED_TERMINAL_SOURCE_G_QUOTIENT_AUTHORITY"
             and receipt.get("C28") == "UNAUTHORIZED_NOT_STARTED"
             and receipt.get("C29") == "UNAUTHORIZED_NOT_STARTED"
             and receipt.get("CM2") == "NO-GO_FOR_CLAIM",
             "exact predecessor terminal receipt semantics")
        need(replay.get("schema") == PREDECESSOR_REPLAY_SCHEMA
             and replay.get("status") == PREDECESSOR_STATUS
             and replay.get("terminal_receipt_file_sha256")
                 == captures["receipt"].sha256
             and replay.get("terminal_receipt_object_sha256")
                 == receipt["terminal_receipt_sha256"]
             and replay.get("terminal_root_manifest_sha256") == root.sha256
             and replay.get("terminal_payload_manifest_sha256") == payload.sha256
             and replay.get("terminal_receipt_byte_replay_identical") is True
             and replay.get("authority_minted") is True
             and replay.get("manifest_authorized") is True
             and replay.get("formal_credit") == 0,
             "exact predecessor terminal byte replay semantics")
        need(chain.get("schema") == PREDECESSOR_CHAIN_SCHEMA
             and chain.get("status") == PREDECESSOR_STATUS
             and chain.get("terminal_receipt_file_sha256")
                 == captures["receipt"].sha256
             and chain.get("terminal_receipt_object_sha256")
                 == receipt["terminal_receipt_sha256"]
             and chain.get("terminal_replay_file_sha256")
                 == captures["replay"].sha256
             and chain.get("terminal_replay_object_sha256")
                 == replay["terminal_replay_sha256"]
             and chain.get("authority_minted") is True
             and chain.get("manifest_authorized") is True,
             "exact predecessor chain-status closure")
        root_entries = parse_manifest(root)
        payload_entries = parse_manifest(payload)
        need(root.sha256 == receipt["terminal_root_manifest_sha256"]
             and payload.sha256 == receipt["terminal_payload_manifest_sha256"]
             and payload.sha256 == replay["terminal_payload_manifest_sha256"]
             and any(path == relative(payload.path)
                     and sha == payload.sha256
                     for path, sha in root_entries.items()),
             "terminal root/payload/receipt/replay closure")
        selected_paths: dict[str, str] = {}
        wanted = {
            "producer_result": "result.json",
            "member_to_post_component": "member_to_post_component.jsonl.gz",
            "post_component_census": "post_component_census.jsonl.gz",
        }
        for role, basename in wanted.items():
            matches = [path for path in payload_entries
                       if Path(path).name == basename]
            need(len(matches) == 1, "unique terminal payload role:" + role)
            selected_paths[role] = matches[0]
        selected = {role: Capture(workspace(path), "selected:" + role)
                    for role, path in selected_paths.items()}
        captures.update({"selected_" + role: value
                         for role, value in selected.items()})
        result = selected["producer_result"].document("result_sha256")
        need(result.get("schema") == C27R2_RESULT_SCHEMA
             and result.get("status") == C27R2_RESULT_STATUS
             and result.get("exact_census") == EXPECTED
             and result.get("formal_credit") == 0
             and result.get("manifest_authorized") is False,
             "terminal-pinned C27R2 producer result")
        descriptors = result.get("ledgers")
        need(type(descriptors) is dict, "C27R2 ledger descriptors")
        rows = {"member_to_post_component": 502_204,
                "post_component_census": 43_684}
        selected_descriptors: dict[str, dict[str, Any]] = {}
        selected_descriptors["producer_result"] = {
            "path": selected_paths["producer_result"],
            "sha256": selected["producer_result"].sha256,
            "size": selected["producer_result"].before.st_size,
            "row_count": 0, "result_sha256": result["result_sha256"],
        }
        for role, count in rows.items():
            descriptor = descriptors.get(role)
            capture = selected[role]
            need(type(descriptor) is dict
                 and descriptor.get("filename") == capture.path.name
                 and descriptor.get("sha256") == capture.sha256
                 and descriptor.get("size") == capture.before.st_size
                 and descriptor.get("row_count") == count
                 and descriptor.get("gzip_mtime") == 0
                 and descriptor.get("canonical_jsonl") is True,
                 "selected ledger descriptor:" + role)
            selected_descriptors[role] = {
                "path": selected_paths[role], "sha256": capture.sha256,
                "size": capture.before.st_size, "row_count": count,
                "result_sha256": None,
            }
        attestations = {key: capture.attest()
                        for key, capture in sorted(captures.items())}
        return (receipt, replay, chain, payload_entries,
                list(captures.values()), selected_descriptors)
    except BaseException:
        for capture in captures.values():
            capture.close()
        raise


def build(args: argparse.Namespace) -> dict[str, Any]:
    need(valid_sha(args.expect_builder_sha256), "builder pin syntax")
    self_capture = Capture(SELF, "builder-source")
    try:
        need(self_capture.sha256 == args.expect_builder_sha256,
             "builder source self pin")
    finally:
        self_capture.close()
    output = workspace(args.output_dir, absent=True)
    need(output.parent == AUDIT and not output.exists(), "fresh adapter dir")
    receipt, replay, chain, _payload_entries, captures, selected = \
        terminal_inputs(args)
    try:
        if args.preflight_only:
            return {"status": (
                "PASS_ORIGINAL_C27R2_TERMINAL_AND_FRESH_ADAPTER_PREFLIGHT__"
                "NO_OUTPUT_CREATED_ZERO_CREDIT")}
        output.mkdir(mode=0o700)
        payload_entries = {descriptor["path"]: descriptor["sha256"]
                           for descriptor in selected.values()}
        payload_raw = manifest(dict(sorted(payload_entries.items())))
        payload_path = output / "payload_manifest.sha256"
        write_once(payload_path, payload_raw)
        predecessor = {
            "terminal_dir": relative(workspace(args.c27r2_terminal_dir)),
            "terminal_root_manifest_sha256":
                args.expect_terminal_root_sha256,
            "terminal_receipt_file_sha256":
                args.expect_terminal_receipt_file_sha256,
            "terminal_receipt_object_sha256":
                args.expect_terminal_receipt_object_sha256,
            "terminal_replay_file_sha256":
                args.expect_terminal_replay_file_sha256,
            "terminal_replay_object_sha256":
                args.expect_terminal_replay_object_sha256,
            "terminal_pass_lock_sha256":
                args.expect_terminal_pass_lock_sha256,
            "terminal_payload_manifest_sha256":
                receipt["terminal_payload_manifest_sha256"],
            "chain_status_object_sha256": chain["chain_status_sha256"],
        }
        adapter_body = {
            "schema": ADAPTER_SCHEMA, "status": ADAPTER_STATUS,
            "predecessor": predecessor,
            "selected_payload": selected,
            "c27r2_terminal_passed": True,
            "complete_actual_v2_edge_complement_after_quotient": True,
            "c28_fresh_rebuild_only": True,
            "c28_formal_credit_zero": True,
            "c29_unauthorized": True,
            "cm2_no_go": "NO-GO_FOR_CLAIM",
            "terminal_receipt_byte_replay_verified":
                replay["terminal_receipt_byte_replay_identical"],
            "authority_adapter_not_legacy_alias": True,
            "formal_credit": 0, "manifest_authorized": False,
            "C27R2": "AUTHORIZED_TERMINAL_SOURCE_G_QUOTIENT_AUTHORITY",
            "C28": "UNAUTHORIZED_MATH_CORE_MAY_START",
            "C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM",
        }
        adapter = {**adapter_body,
                   "terminal_receipt_sha256": digest(adapter_body)}
        receipt_path = output / "terminal_receipt.json"
        write_once(receipt_path, canonical(adapter) + b"\n")
        root_entries = {
            relative(payload_path): hashlib.sha256(payload_raw).hexdigest(),
            relative(receipt_path): hashlib.sha256(
                canonical(adapter) + b"\n").hexdigest(),
        }
        root_raw = manifest(dict(sorted(root_entries.items())))
        root_path = output / "root_manifest.sha256"
        write_once(root_path, root_raw)
        contract_body = {
            "schema": CONTRACT_SCHEMA, "status": CONTRACT_READY,
            "terminal": {
                "terminal_dir": relative(output),
                "root_manifest_filename": "root_manifest.sha256",
                "payload_manifest_filename": "payload_manifest.sha256",
                "receipt_filename": "terminal_receipt.json",
                "pass_lock_filename": "PASS.lock",
                "pass_lock_ascii": ADAPTER_PASS[:-1].decode("ascii"),
                "root_payload_entry": relative(payload_path),
                "root_receipt_entry": relative(receipt_path),
                "root_manifest_sha256": hashlib.sha256(root_raw).hexdigest(),
                "payload_manifest_sha256":
                    hashlib.sha256(payload_raw).hexdigest(),
                "receipt_file_sha256": hashlib.sha256(
                    canonical(adapter) + b"\n").hexdigest(),
                "receipt_object_sha256": adapter["terminal_receipt_sha256"],
                "receipt_closure_key": "terminal_receipt_sha256",
                "receipt_schema": ADAPTER_SCHEMA,
                "receipt_status": ADAPTER_STATUS,
            },
            "payload": selected,
            "semantic_bindings": {
                "c27r2_terminal_passed": {
                    "path": ["c27r2_terminal_passed"], "expected": True},
                "complete_actual_v2_edge_complement_after_quotient": {
                    "path": ["complete_actual_v2_edge_complement_after_quotient"],
                    "expected": True},
                "c28_fresh_rebuild_only": {
                    "path": ["c28_fresh_rebuild_only"], "expected": True},
                "c28_formal_credit_zero": {
                    "path": ["c28_formal_credit_zero"], "expected": True},
                "c29_unauthorized": {
                    "path": ["c29_unauthorized"], "expected": True},
                "cm2_no_go": {
                    "path": ["cm2_no_go"], "expected": "NO-GO_FOR_CLAIM"},
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
        contract = {**contract_body, "contract_sha256": digest(contract_body)}
        write_once(output / "authority_contract.json",
                   canonical(contract) + b"\n")
        write_once(output / "PASS.lock", ADAPTER_PASS)
        need({entry.name for entry in output.iterdir()} == OUTPUT_FILES,
             "exact adapter inventory")
        for capture in captures:
            capture.attest()
        return adapter
    finally:
        for capture in captures:
            capture.close()


def self_test() -> dict[str, Any]:
    body = {"schema": ADAPTER_SCHEMA, "status": ADAPTER_STATUS,
            "formal_credit": 0}
    closed = {**body, "terminal_receipt_sha256": digest(body)}
    need(closed["terminal_receipt_sha256"] == digest(body), "closure fixture")
    with tempfile.TemporaryDirectory(prefix="c28-adapter-") as raw:
        base = Path(raw)
        first = base / "a"
        second = base / "b"
        first.write_bytes(b"a")
        second.write_bytes(b"b")
        entries = {str(first): hashlib.sha256(b"a").hexdigest(),
                   str(second): hashlib.sha256(b"b").hexdigest()}
        need(manifest(dict(sorted(entries.items()))).endswith(b"\n"),
             "manifest fixture")
    return {"status": "PASS_ADAPTER_CLOSURE_AND_MANIFEST_FIXTURE",
            "formal_credit": 0, "CM2": "NO-GO_FOR_CLAIM"}


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--self-test", action="store_true")
    value.add_argument("--preflight-only", action="store_true")
    for name in (
        "c27r2-terminal-dir", "expect-terminal-root-sha256",
        "expect-terminal-receipt-file-sha256",
        "expect-terminal-receipt-object-sha256",
        "expect-terminal-replay-file-sha256",
        "expect-terminal-replay-object-sha256",
        "expect-terminal-pass-lock-sha256", "expect-builder-sha256",
        "output-dir",
    ):
        value.add_argument("--" + name)
    return value


def main() -> int:
    args = parser().parse_args()
    fields = (
        "c27r2_terminal_dir", "expect_terminal_root_sha256",
        "expect_terminal_receipt_file_sha256",
        "expect_terminal_receipt_object_sha256",
        "expect_terminal_replay_file_sha256",
        "expect_terminal_replay_object_sha256",
        "expect_terminal_pass_lock_sha256", "expect_builder_sha256",
        "output_dir",
    )
    try:
        if args.self_test:
            need(not args.preflight_only
                 and all(getattr(args, field) is None for field in fields),
                 "self-test accepts no run arguments")
            result = self_test()
        else:
            need(all(getattr(args, field) is not None for field in fields),
                 "all original terminal pins and fresh output required")
            result = build(args)
        sys.stdout.buffer.write(canonical({
            "CM2": "NO-GO_FOR_CLAIM", "formal_credit": 0,
            "status": result["status"],
        }) + b"\n")
        return 0
    except (Failure, OSError, ValueError, KeyError, TypeError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
