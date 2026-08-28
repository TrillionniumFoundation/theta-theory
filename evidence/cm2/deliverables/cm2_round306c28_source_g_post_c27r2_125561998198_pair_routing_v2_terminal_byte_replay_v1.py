#!/usr/bin/env python3
"""Independently replay terminal bytes and mint only C28-v2 authority.

This is the sole C28 release source allowed to change the authorization bit.
It independently revalidates the zero-credit seal, outer receipt, manifests,
formal core and the immutable C27R2 predecessor; constructs the terminal body
twice; and requires canonical byte identity.  C29 stays unauthorized and CM2
stays NO-GO.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
AUDIT = ROOT / ".cm2-runtime/audit"
PREFIX = (
    "cm2.round306c28.source-g-post-c27r2-125561998198-pair-routing.v2."
)
SEAL_SCHEMA = PREFIX + "release-terminal-seal-candidate.v1"
SEAL_STATUS = (
    "PASS_CONDITIONAL_C28_TERMINAL_SEAL_CANDIDATE__ZERO_CREDIT_PENDING_"
    "INDEPENDENT_BYTE_REPLAY"
)
OUTER_SCHEMA = PREFIX + "release-outer-verification.v1"
OUTER_STATUS = (
    "PASS_INDEPENDENT_C28_FULL_PAIR_LEDGER_MANIFEST_COLD_AND_32_RELEASE_"
    "ATTACK_CHECK__CONDITIONAL_ZERO_CREDIT"
)
MANIFEST_SCHEMA = PREFIX + "release-manifest-receipt.v1"
TERMINAL_STATUS = (
    "PASS_C28_TERMINAL_BYTE_REPLAY__FORMAL_C28_PAIR_ROUTING_AUTHORITY_MINTED"
)
RESULT_SCHEMA = PREFIX + "producer-result.v1"
RESULT_STATUS = (
    "PASS_POST_C27R2_PARTITION_502204_MEMBERS_43684_COMPONENTS_AND_"
    "32896_PAIR_SHARDS_REBUILT__125561998198_EXACT_NONEDGE_CANDIDATE_"
    "ZERO_CREDIT__C28_UNAUTHORIZED_PENDING_RELEASE_TERMINAL"
)
EXPECTED = {
    "members": 502_204, "post_components": 43_684, "blocks": 256,
    "shards": 32_896, "total_pairs": 126_104_177_706,
    "within_pairs": 542_179_508, "cross_pairs": 125_561_998_198,
}
C27 = {
    "root": "1f65a624c889773e3104c4311788fc06be04d6ca92e033205074b8cc7f5b27fc",
    "receipt_file": "feccb0b9290bd82ac1d8e78e8e7a21d4f25e0ca3aa3556cc3f0bb6007f61c3dd",
    "receipt_object": "8afbd127c9518f569c2f7b3edcdbe9e0ebf77d88bcca855822e58d21e5cfe782",
    "replay_file": "b480df4b8caaf9876a48720f92a8fb6d86e2b1b5966bcc71b0022c5e49fc12ee",
    "replay_object": "216d2592c49b0302de0042677ce54c96cd5ad1fcb32231da02b39c003cb837e8",
    "pass": "5fe4140b3e8f38196e9ca68cd336ae29be1c8847c7685526f08aa4d7173d7348",
}
C27_STATUS = "PASS_C27R2_TERMINAL_BYTE_REPLAY__FORMAL_C27R2_AUTHORITY_MINTED"
C27_PASS = b"PASS_C27R2_AUTHORITY_V2_TERMINAL_BYTE_REPLAY__C28_C29_UNAUTHORIZED\n"
PASS_BYTES = b"PASS_C28_PAIR_ROUTING_V2_TERMINAL_BYTE_REPLAY__C29_UNAUTHORIZED\n"


class Blocked(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Blocked(label)


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


def file_sha(path: Path) -> str:
    absolute = path.absolute()
    need(absolute.resolve(strict=True) == absolute,
         "canonical path:" + str(path))
    fd = os.open(absolute, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                 | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular singleton:" + str(path))
        state = hashlib.sha256()
        while block := os.read(fd, 4 << 20):
            state.update(block)
        need(fingerprint(before) == fingerprint(os.fstat(fd))
             == fingerprint(os.stat(absolute, follow_symlinks=False)),
             "stable fd/path SHA/stat:" + str(path))
        return state.hexdigest()
    finally:
        os.close(fd)


def strict_load(payload: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(type(key) is str and key not in result,
                 "unique JSON key:" + str(key))
            result[key] = value
        return result
    return json.loads(payload, object_pairs_hook=pairs,
                      parse_constant=lambda token: (_ for _ in ()).throw(
                          ValueError(token)))


def document(path: Path, closure: str) -> dict[str, Any]:
    payload = path.read_bytes()
    need(payload.endswith(b"\n") and not payload.endswith(b"\n\n"),
         "JSON newline:" + str(path))
    value = strict_load(payload[:-1])
    need(type(value) is dict and canonical(value) == payload[:-1],
         "canonical JSON:" + str(path))
    body = dict(value)
    claim = body.pop(closure, None)
    need(valid_sha(claim) and claim == digest(body),
         "object closure:" + str(path))
    return value


def parse_manifest(path: Path) -> dict[str, str]:
    payload = path.read_bytes()
    need(payload.endswith(b"\n") and payload != b"\n", "manifest nonempty")
    result: dict[str, str] = {}
    for line in payload.decode("ascii").splitlines():
        fields = line.split("  ", 1)
        need(len(fields) == 2 and valid_sha(fields[0])
             and fields[1] not in result and fields[1] != "",
             "manifest row syntax/unique")
        relative = Path(fields[1])
        need(not relative.is_absolute()
             and all(part not in {"", ".", ".."} for part in relative.parts)
             and str(relative) == fields[1], "canonical manifest path")
        result[fields[1]] = fields[0]
    need(list(result) == sorted(result), "manifest path ordering")
    for relative, expected in result.items():
        need(file_sha(ROOT / relative) == expected,
             "manifest current member:" + relative)
    return result


def manifest(paths: set[Path]) -> bytes:
    rows = sorted((str(path.absolute().relative_to(ROOT)), file_sha(path))
                  for path in paths)
    need(rows and len(rows) == len({path for path, _ in rows}),
         "nonempty unique manifest paths")
    return ("\n".join(f"{sha256}  {path}" for path, sha256 in rows)
            + "\n").encode("ascii")


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


def validate_predecessor(path: Path) -> None:
    need(path.parent == AUDIT and path.is_dir() and not path.is_symlink()
         and {entry.name for entry in path.iterdir()} == {
             "PASS.lock", "chain_status.json", "payload_manifest.sha256",
             "root_manifest.sha256", "terminal_receipt.json",
             "terminal_replay.json"}, "exact C27R2 terminal inventory")
    receipt = document(path / "terminal_receipt.json", "terminal_receipt_sha256")
    replay = document(path / "terminal_replay.json", "terminal_replay_sha256")
    need(file_sha(path / "root_manifest.sha256") == C27["root"]
         and file_sha(path / "terminal_receipt.json") == C27["receipt_file"]
         and receipt["terminal_receipt_sha256"] == C27["receipt_object"]
         and file_sha(path / "terminal_replay.json") == C27["replay_file"]
         and replay["terminal_replay_sha256"] == C27["replay_object"]
         and file_sha(path / "PASS.lock") == C27["pass"]
         and (path / "PASS.lock").read_bytes() == C27_PASS
         and receipt.get("status") == C27_STATUS
         and receipt.get("authority_minted") is True,
         "immutable C27R2 terminal boundary")
    parse_manifest(path / "payload_manifest.sha256")
    parse_manifest(path / "root_manifest.sha256")


def terminal_body(seal: dict[str, Any], outer: dict[str, Any],
                  result_object: str, terminal_payload_sha: str,
                  terminal_root_sha: str) -> dict[str, Any]:
    return {
        "schema": PREFIX + "terminal-receipt.v1", "status": TERMINAL_STATUS,
        "seal_candidate_object_sha256": seal["seal_candidate_sha256"],
        "manifest_receipt_object_sha256":
            seal["manifest_receipt_object_sha256"],
        "payload_manifest_sha256": seal["payload_manifest_sha256"],
        "root_manifest_sha256": seal["root_manifest_sha256"],
        "outer_verification_object_sha256":
            outer["outer_verification_sha256"],
        "terminal_payload_manifest_sha256": terminal_payload_sha,
        "terminal_root_manifest_sha256": terminal_root_sha,
        "C27R2_terminal_root_manifest_sha256": C27["root"],
        "C27R2_terminal_receipt_file_sha256": C27["receipt_file"],
        "C27R2_terminal_receipt_object_sha256": C27["receipt_object"],
        "C27R2_terminal_replay_file_sha256": C27["replay_file"],
        "C27R2_terminal_replay_object_sha256": C27["replay_object"],
        "C28_producer_result_object_sha256": result_object,
        "exact_census": EXPECTED,
        "terminal_replay_completed": True,
        "terminal_receipt_byte_replay_identical": True,
        "authority_minted": True, "formal_credit": 0,
        "manifest_authorized": True,
        "C27R2": "AUTHORIZED_TERMINAL_PREDECESSOR_UNCHANGED",
        "C28": "AUTHORIZED_TERMINAL_SOURCE_G_PAIR_ROUTING_AUTHORITY",
        "C29": "UNAUTHORIZED_NOT_STARTED", "Source_W": "UNCHANGED",
        "D02": "BLOCKED_COMPOSITE", "D03": "UNAUTHORIZED",
        "D04": "NOT_MINTED", "Gate5": "10/18",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def execute(args: argparse.Namespace) -> dict[str, Any]:
    pins = (
        args.expect_replay_sha256, args.expect_seal_candidate_file_sha256,
        args.expect_seal_candidate_object_sha256,
        args.expect_seal_payload_manifest_sha256,
        args.expect_seal_root_manifest_sha256,
        args.expect_outer_file_sha256, args.expect_outer_object_sha256,
        args.expect_manifest_receipt_file_sha256,
        args.expect_manifest_receipt_object_sha256,
        args.expect_core_receipt_file_sha256,
        args.expect_core_receipt_object_sha256, args.expect_core_pass_sha256,
    )
    need(all(valid_sha(value) for value in pins)
         and file_sha(SELF) == args.expect_replay_sha256,
         "terminal replay self/all dynamic pins")
    seal_dir = Path(args.seal_dir).absolute()
    manifest_dir = Path(args.manifest_dir).absolute()
    outer_path = Path(args.outer_file).absolute()
    control = Path(args.core_control_dir).absolute()
    predecessor = Path(args.predecessor_terminal_dir).absolute()
    output = Path(args.output_dir).absolute()
    need(all(path.parent == AUDIT and path.is_dir() and not path.is_symlink()
             for path in (seal_dir, manifest_dir, control, predecessor)),
         "direct audit input directories")
    need(output.parent == AUDIT and not output.exists()
         and not output.is_symlink(), "fresh terminal output")
    need({entry.name for entry in seal_dir.iterdir()} == {
        "seal_candidate.json", "seal_payload_manifest.sha256",
        "seal_root_manifest.sha256"}, "seal exact inventory")
    validate_predecessor(predecessor)
    seal_path = seal_dir / "seal_candidate.json"
    seal_payload_path = seal_dir / "seal_payload_manifest.sha256"
    seal_root_path = seal_dir / "seal_root_manifest.sha256"
    manifest_receipt_path = manifest_dir / "manifest_receipt.json"
    manifest_payload_path = manifest_dir / "payload_manifest.sha256"
    manifest_root_path = manifest_dir / "root_manifest.sha256"
    core_path = control / "core_receipt.json"
    seal = document(seal_path, "seal_candidate_sha256")
    outer = document(outer_path, "outer_verification_sha256")
    manifest_receipt = document(manifest_receipt_path,
                                "manifest_receipt_sha256")
    core = document(core_path, "core_receipt_sha256")
    need(file_sha(seal_path) == args.expect_seal_candidate_file_sha256
         and seal["seal_candidate_sha256"]
             == args.expect_seal_candidate_object_sha256
         and file_sha(seal_payload_path)
             == args.expect_seal_payload_manifest_sha256
         and file_sha(seal_root_path) == args.expect_seal_root_manifest_sha256
         and file_sha(outer_path) == args.expect_outer_file_sha256
         and outer["outer_verification_sha256"]
             == args.expect_outer_object_sha256
         and file_sha(manifest_receipt_path)
             == args.expect_manifest_receipt_file_sha256
         and manifest_receipt["manifest_receipt_sha256"]
             == args.expect_manifest_receipt_object_sha256
         and file_sha(core_path) == args.expect_core_receipt_file_sha256
         and core["core_receipt_sha256"]
             == args.expect_core_receipt_object_sha256
         and file_sha(control / "PASS.lock") == args.expect_core_pass_sha256
         and seal.get("schema") == SEAL_SCHEMA and seal.get("status") == SEAL_STATUS
         and seal.get("expected_terminal_status") == TERMINAL_STATUS
         and seal.get("exact_census") == EXPECTED
         and seal.get("C27R2_terminal_root_manifest_sha256") == C27["root"]
         and seal.get("terminal_replay_completed") is False
         and seal.get("authority_minted") is False
         and seal.get("manifest_authorized") is False
         and outer.get("schema") == OUTER_SCHEMA
         and outer.get("status") == OUTER_STATUS
         and outer.get("exact_census") == EXPECTED
         and outer.get("formal_credit") == 0
         and manifest_receipt.get("schema") == MANIFEST_SCHEMA
         and manifest_receipt.get("formal_credit") == 0
         and manifest_receipt.get("manifest_authorized") is False,
         "conditional seal/outer/manifest/core boundary")
    parse_manifest(seal_payload_path)
    parse_manifest(seal_root_path)
    package_payload = parse_manifest(manifest_payload_path)
    parse_manifest(manifest_root_path)
    result_matches: list[tuple[Path, dict[str, Any]]] = []
    for relative in package_payload:
        path = ROOT / relative
        if path.name != "result.json":
            continue
        try:
            value = document(path, "result_sha256")
        except (Blocked, OSError, ValueError, KeyError, TypeError):
            continue
        if value.get("schema") == RESULT_SCHEMA and value.get("status") == RESULT_STATUS:
            result_matches.append((path, value))
    need(len(result_matches) == 1,
         "unique selected C28 producer result in package payload")
    result_path, result = result_matches[0]
    need(result.get("formal_credit") == 0
         and result.get("manifest_authorized") is False,
         "producer result remains zero credit")
    terminal_payload_paths = {ROOT / relative for relative in package_payload}
    terminal_payload_paths.update({
        seal_path, seal_payload_path, seal_root_path, manifest_receipt_path,
        manifest_payload_path, manifest_root_path, outer_path, core_path,
        control / "PASS.lock", result_path, SELF,
    })
    terminal_payload_raw = manifest(terminal_payload_paths)
    if args.preflight_only:
        return {"status":
                "PASS_C28_SEAL_OUTER_MANIFEST_AND_FRESH_TERMINAL_PREFLIGHT__"
                "NO_OUTPUT_CREATED_ZERO_CREDIT"}
    output.mkdir(mode=0o700)
    terminal_payload_path = output / "payload_manifest.sha256"
    write_once(terminal_payload_path, terminal_payload_raw)
    terminal_root_raw = manifest({
        terminal_payload_path, seal_root_path, manifest_root_path, core_path,
        control / "PASS.lock", predecessor / "root_manifest.sha256",
        predecessor / "terminal_receipt.json",
        predecessor / "terminal_replay.json", predecessor / "PASS.lock", SELF,
    })
    terminal_root_path = output / "root_manifest.sha256"
    write_once(terminal_root_path, terminal_root_raw)
    first = terminal_body(
        seal, outer, result["result_sha256"],
        hashlib.sha256(terminal_payload_raw).hexdigest(),
        hashlib.sha256(terminal_root_raw).hexdigest())
    second = terminal_body(
        dict(seal), dict(outer), result["result_sha256"],
        file_sha(terminal_payload_path), file_sha(terminal_root_path))
    need(first == second and canonical(first) == canonical(second),
         "independent terminal body canonical byte replay")
    receipt = {**first, "terminal_receipt_sha256": digest(first)}
    receipt_raw = canonical(receipt) + b"\n"
    receipt_path = output / "terminal_receipt.json"
    write_once(receipt_path, receipt_raw)
    need(receipt_path.read_bytes() == receipt_raw,
         "terminal receipt exact written bytes")
    replay_body = {
        "schema": PREFIX + "terminal-byte-replay.v1", "status": TERMINAL_STATUS,
        "terminal_receipt_file_sha256": file_sha(receipt_path),
        "terminal_receipt_object_sha256": receipt["terminal_receipt_sha256"],
        "terminal_receipt_byte_replay_identical": True,
        "terminal_payload_manifest_sha256": file_sha(terminal_payload_path),
        "terminal_root_manifest_sha256": file_sha(terminal_root_path),
        "C27R2_terminal_root_manifest_sha256": C27["root"],
        "authority_minted": True, "formal_credit": 0,
        "manifest_authorized": True,
        "C27R2": "AUTHORIZED_TERMINAL_PREDECESSOR_UNCHANGED",
        "C28": "AUTHORIZED_TERMINAL_SOURCE_G_PAIR_ROUTING_AUTHORITY",
        "C29": "UNAUTHORIZED_NOT_STARTED", "Source_W": "UNCHANGED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    replay = {**replay_body, "terminal_replay_sha256": digest(replay_body)}
    replay_path = output / "terminal_replay.json"
    write_once(replay_path, canonical(replay) + b"\n")
    chain_body = {
        "schema": PREFIX + "release-chain-status.v1", "status": TERMINAL_STATUS,
        "terminal_receipt_file_sha256": file_sha(receipt_path),
        "terminal_receipt_object_sha256": receipt["terminal_receipt_sha256"],
        "terminal_replay_file_sha256": file_sha(replay_path),
        "terminal_replay_object_sha256": replay["terminal_replay_sha256"],
        "authority_minted": True, "formal_credit": 0,
        "manifest_authorized": True,
        "C27R2": "AUTHORIZED_TERMINAL_PREDECESSOR_UNCHANGED",
        "C28": "AUTHORIZED_TERMINAL_SOURCE_G_PAIR_ROUTING_AUTHORITY",
        "C29": "UNAUTHORIZED_NOT_STARTED", "Source_W": "UNCHANGED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    chain = {**chain_body, "chain_status_sha256": digest(chain_body)}
    write_once(output / "chain_status.json", canonical(chain) + b"\n")
    write_once(output / "PASS.lock", PASS_BYTES)
    need({entry.name for entry in output.iterdir()} == {
        "PASS.lock", "chain_status.json", "payload_manifest.sha256",
        "root_manifest.sha256", "terminal_receipt.json",
        "terminal_replay.json"}, "exact six-file terminal inventory")
    return replay


def self_test() -> dict[str, Any]:
    seal = {"seal_candidate_sha256": "0" * 64,
            "manifest_receipt_object_sha256": "1" * 64,
            "payload_manifest_sha256": "2" * 64,
            "root_manifest_sha256": "3" * 64}
    outer = {"outer_verification_sha256": "4" * 64}
    first = terminal_body(seal, outer, "5" * 64, "6" * 64, "7" * 64)
    second = terminal_body(dict(seal), dict(outer), "5" * 64,
                           "6" * 64, "7" * 64)
    need(canonical(first) == canonical(second)
         and first["C28"].startswith("AUTHORIZED_TERMINAL")
         and first["C29"] == "UNAUTHORIZED_NOT_STARTED",
         "independent terminal byte fixture")
    return {"status": "PASS_C28_INDEPENDENT_TERMINAL_BYTE_REPLAY_SELF_TEST",
            "formal_credit": 0, "C28": "UNAUTHORIZED_SELF_TEST_ONLY",
            "CM2": "NO-GO_FOR_CLAIM"}


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--self-test", action="store_true")
    value.add_argument("--preflight-only", action="store_true")
    for name in (
        "seal-dir", "manifest-dir", "outer-file", "core-control-dir",
        "predecessor-terminal-dir", "output-dir", "expect-replay-sha256",
        "expect-seal-candidate-file-sha256",
        "expect-seal-candidate-object-sha256",
        "expect-seal-payload-manifest-sha256",
        "expect-seal-root-manifest-sha256",
        "expect-outer-file-sha256", "expect-outer-object-sha256",
        "expect-manifest-receipt-file-sha256",
        "expect-manifest-receipt-object-sha256",
        "expect-core-receipt-file-sha256",
        "expect-core-receipt-object-sha256", "expect-core-pass-sha256",
    ):
        value.add_argument("--" + name)
    return value


def main() -> int:
    args = parser().parse_args()
    fields = tuple(name for name in vars(args)
                   if name not in {"self_test", "preflight_only"})
    try:
        if args.self_test:
            need(not args.preflight_only
                 and all(getattr(args, field) is None for field in fields),
                 "self-test accepts no run arguments")
            result = self_test()
        else:
            need(all(getattr(args, field) is not None for field in fields),
                 "all run arguments")
            result = execute(args)
        sys.stdout.buffer.write(canonical({
            "CM2": "NO-GO_FOR_CLAIM", "formal_credit": 0,
            "status": result["status"],
        }) + b"\n")
        return 0
    except (Blocked, OSError, ValueError, KeyError, TypeError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
