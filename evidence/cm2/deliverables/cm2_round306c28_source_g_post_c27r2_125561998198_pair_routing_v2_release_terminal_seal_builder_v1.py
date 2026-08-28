#!/usr/bin/env python3
"""Build a conditional, non-authorizing C28-v2 terminal seal candidate.

The seal binds the manifest-first package and independent outer receipt.  It
emits no PASS lock and cannot authorize C28.  Only the separately frozen
terminal byte replay source may consume this candidate and mint authority.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
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
MANIFEST_SCHEMA = PREFIX + "release-manifest-receipt.v1"
MANIFEST_STATUS = (
    "PASS_C28_MANIFEST_FIRST_PAYLOAD_AND_C27R2_ROOT_CLOSURE__ZERO_"
    "CREDIT_PENDING_OUTER_SEAL_AND_TERMINAL_REPLAY"
)
OUTER_SCHEMA = PREFIX + "release-outer-verification.v1"
OUTER_STATUS = (
    "PASS_INDEPENDENT_C28_FULL_PAIR_LEDGER_MANIFEST_COLD_AND_32_RELEASE_"
    "ATTACK_CHECK__CONDITIONAL_ZERO_CREDIT"
)
SEAL_SCHEMA = PREFIX + "release-terminal-seal-candidate.v1"
SEAL_STATUS = (
    "PASS_CONDITIONAL_C28_TERMINAL_SEAL_CANDIDATE__ZERO_CREDIT_PENDING_"
    "INDEPENDENT_BYTE_REPLAY"
)
TERMINAL_STATUS = (
    "PASS_C28_TERMINAL_BYTE_REPLAY__FORMAL_C28_PAIR_ROUTING_AUTHORITY_MINTED"
)
EXPECTED = {
    "members": 502_204, "post_components": 43_684, "blocks": 256,
    "shards": 32_896, "total_pairs": 126_104_177_706,
    "within_pairs": 542_179_508, "cross_pairs": 125_561_998_198,
}
C27_ROOT = "1f65a624c889773e3104c4311788fc06be04d6ca92e033205074b8cc7f5b27fc"


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


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace(
        "+00:00", "Z")


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


def execute(args: argparse.Namespace) -> dict[str, Any]:
    pins = (
        args.expect_builder_sha256, args.expect_outer_file_sha256,
        args.expect_outer_object_sha256,
        args.expect_manifest_receipt_file_sha256,
        args.expect_manifest_receipt_object_sha256,
        args.expect_payload_manifest_sha256, args.expect_root_manifest_sha256,
    )
    need(all(valid_sha(value) for value in pins)
         and file_sha(SELF) == args.expect_builder_sha256,
         "seal builder self/all dynamic pins")
    manifest_dir = Path(args.manifest_dir).absolute()
    outer_path = Path(args.outer_file).absolute()
    output = Path(args.output_dir).absolute()
    need(manifest_dir.parent == AUDIT and manifest_dir.is_dir()
         and not manifest_dir.is_symlink()
         and {entry.name for entry in manifest_dir.iterdir()} == {
             "manifest_receipt.json", "payload_manifest.sha256",
             "root_manifest.sha256"}, "manifest exact inventory")
    need(outer_path.parent == AUDIT and outer_path.is_file()
         and not outer_path.is_symlink(), "outer direct audit file")
    need(output.parent == AUDIT and not output.exists()
         and not output.is_symlink(), "fresh seal output")
    receipt_path = manifest_dir / "manifest_receipt.json"
    payload_path = manifest_dir / "payload_manifest.sha256"
    root_path = manifest_dir / "root_manifest.sha256"
    receipt = document(receipt_path, "manifest_receipt_sha256")
    outer = document(outer_path, "outer_verification_sha256")
    need(file_sha(receipt_path) == args.expect_manifest_receipt_file_sha256
         and receipt["manifest_receipt_sha256"]
             == args.expect_manifest_receipt_object_sha256
         and receipt.get("schema") == MANIFEST_SCHEMA
         and receipt.get("status") == MANIFEST_STATUS
         and file_sha(payload_path) == args.expect_payload_manifest_sha256
         and file_sha(root_path) == args.expect_root_manifest_sha256
         and file_sha(outer_path) == args.expect_outer_file_sha256
         and outer["outer_verification_sha256"]
             == args.expect_outer_object_sha256
         and outer.get("schema") == OUTER_SCHEMA
         and outer.get("status") == OUTER_STATUS
         and outer.get("exact_census") == EXPECTED
         and outer.get("C27R2_terminal_root_manifest_sha256") == C27_ROOT
         and outer.get("cold_replay_byte_identical") is True
         and outer.get("core_attacks_rejected") == 26
         and outer.get("release_attacks_rejected") == 32
         and outer.get("outer_is_conditional_until_independent_terminal_"
                       "byte_replay") is True
         and outer.get("formal_credit") == 0
         and outer.get("manifest_authorized") is False
         and outer.get("C28") == "UNAUTHORIZED_PENDING_TERMINAL_BYTE_REPLAY",
         "exact conditional manifest/outer boundary")
    parse_manifest(payload_path)
    parse_manifest(root_path)
    if args.preflight_only:
        return {"status":
                "PASS_C28_MANIFEST_OUTER_AND_FRESH_SEAL_PREFLIGHT__NO_"
                "OUTPUT_CREATED_ZERO_CREDIT"}
    output.mkdir(mode=0o700)
    seal_payload_raw = manifest({receipt_path, payload_path, root_path,
                                 outer_path, SELF})
    seal_payload_path = output / "seal_payload_manifest.sha256"
    write_once(seal_payload_path, seal_payload_raw)
    seal_root_raw = manifest({seal_payload_path, root_path, outer_path,
                              receipt_path, SELF})
    seal_root_path = output / "seal_root_manifest.sha256"
    write_once(seal_root_path, seal_root_raw)
    body = {
        "schema": SEAL_SCHEMA, "status": SEAL_STATUS,
        "built_at_utc": now(),
        "manifest_receipt_file_sha256":
            args.expect_manifest_receipt_file_sha256,
        "manifest_receipt_object_sha256":
            args.expect_manifest_receipt_object_sha256,
        "payload_manifest_sha256": args.expect_payload_manifest_sha256,
        "root_manifest_sha256": args.expect_root_manifest_sha256,
        "outer_verification_file_sha256": args.expect_outer_file_sha256,
        "outer_verification_object_sha256": args.expect_outer_object_sha256,
        "seal_payload_manifest_sha256": file_sha(seal_payload_path),
        "seal_root_manifest_sha256": file_sha(seal_root_path),
        "C27R2_terminal_root_manifest_sha256": C27_ROOT,
        "exact_census": EXPECTED, "expected_terminal_status": TERMINAL_STATUS,
        "terminal_replay_completed": False, "authority_minted": False,
        "formal_credit": 0, "manifest_authorized": False,
        "C27R2": "AUTHORIZED_PREDECESSOR_ONLY",
        "C28": "UNAUTHORIZED_PENDING_INDEPENDENT_TERMINAL_BYTE_REPLAY",
        "C29": "UNAUTHORIZED", "Source_W": "UNCHANGED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    seal = {**body, "seal_candidate_sha256": digest(body)}
    write_once(output / "seal_candidate.json", canonical(seal) + b"\n")
    return seal


def self_test() -> dict[str, Any]:
    body = {"authority_minted": False, "formal_credit": 0,
            "C28": "UNAUTHORIZED"}
    need(digest(body) == hashlib.sha256(canonical(body)).hexdigest(),
         "conditional seal closure fixture")
    return {"status": "PASS_C28_RELEASE_TERMINAL_SEAL_BUILDER_SELF_TEST",
            "formal_credit": 0, "C28": "UNAUTHORIZED",
            "CM2": "NO-GO_FOR_CLAIM"}


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--self-test", action="store_true")
    value.add_argument("--preflight-only", action="store_true")
    for name in (
        "manifest-dir", "outer-file", "output-dir",
        "expect-builder-sha256", "expect-outer-file-sha256",
        "expect-outer-object-sha256",
        "expect-manifest-receipt-file-sha256",
        "expect-manifest-receipt-object-sha256",
        "expect-payload-manifest-sha256", "expect-root-manifest-sha256",
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
