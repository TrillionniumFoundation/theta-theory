#!/usr/bin/env python3
"""Build manifest-first C29-v2 payload/root closure after release attacks."""

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
BASE = "cm2.round306c29.source-g-post-c27r2-member-rebound-fibre-exhaustion.v2."
CORE_SCHEMA = BASE + "gated-dual-terminal-seed-core-receipt.v1"
COLD_SCHEMA = BASE + "release-cold-replay-receipt.v1"
EVIDENCE_SCHEMA = BASE + "release-evidence-bundle.v1"
ATTACK_SCHEMA = BASE + "release-only-attack-harness.v1"
ATTACK_STATUS = "PASS_C29_V2_40_OF_40_DUAL_PREDECESSOR_RELEASE_ONLY_ATTACKS_REJECTED__ZERO_CREDIT"
MANIFEST_SCHEMA = BASE + "release-manifest-receipt.v1"
MANIFEST_STATUS = "PASS_C29_V2_MANIFEST_FIRST_PAYLOAD_AND_DUAL_PREDECESSOR_ROOT_CLOSURE__ZERO_CREDIT_PENDING_OUTER_TERMINAL"
C27_PINS = {
    "root": "1f65a624c889773e3104c4311788fc06be04d6ca92e033205074b8cc7f5b27fc",
    "receipt_file": "feccb0b9290bd82ac1d8e78e8e7a21d4f25e0ca3aa3556cc3f0bb6007f61c3dd",
    "receipt_object": "8afbd127c9518f569c2f7b3edcdbe9e0ebf77d88bcca855822e58d21e5cfe782",
    "replay_file": "b480df4b8caaf9876a48720f92a8fb6d86e2b1b5966bcc71b0022c5e49fc12ee",
    "replay_object": "216d2592c49b0302de0042677ce54c96cd5ad1fcb32231da02b39c003cb837e8",
    "pass": "5fe4140b3e8f38196e9ca68cd336ae29be1c8847c7685526f08aa4d7173d7348",
}


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
    return type(value) is str and len(value) == 64 and all(
        char in "0123456789abcdef" for char in value)


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace(
        "+00:00", "Z")


def strict(payload: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(type(key) is str and key not in result, "unique JSON key")
            result[key] = value
        return result
    return json.loads(payload, object_pairs_hook=pairs,
                      parse_constant=lambda token: (_ for _ in ()).throw(
                          ValueError(token)))


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns,
            value.st_uid, value.st_gid)


def file_sha(path: Path) -> str:
    path = path.absolute()
    need(path.resolve(strict=True) == path, "canonical path:" + str(path))
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                         | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular singleton:" + str(path))
        state = hashlib.sha256()
        while block := os.read(descriptor, 4 << 20):
            state.update(block)
        need(fingerprint(os.fstat(descriptor)) == fingerprint(before),
             "stable SHA/stat:" + str(path))
        return state.hexdigest()
    finally:
        os.close(descriptor)


def document(path: Path, closure: str) -> dict[str, Any]:
    payload = path.read_bytes()
    need(payload.endswith(b"\n") and not payload.endswith(b"\n\n"),
         "JSON newline")
    value = strict(payload[:-1])
    need(type(value) is dict and canonical(value) == payload[:-1],
         "canonical JSON")
    body = dict(value)
    claim = body.pop(closure, None)
    need(valid_sha(claim) and claim == digest(body), "object closure")
    return value


def parse_manifest(path: Path, verify: bool = True) -> dict[str, str]:
    payload = path.read_bytes()
    need(payload.endswith(b"\n"), "manifest newline")
    result: dict[str, str] = {}
    for line in payload.decode("ascii").splitlines():
        fields = line.split("  ", 1)
        need(len(fields) == 2 and valid_sha(fields[0])
             and fields[1] not in result and fields[1] != "", "manifest row")
        relative = Path(fields[1])
        need(not relative.is_absolute() and str(relative) == fields[1]
             and all(part not in {"", ".", ".."} for part in relative.parts),
             "canonical manifest path")
        result[fields[1]] = fields[0]
    need(list(result) == sorted(result), "sorted manifest")
    if verify:
        need(all(file_sha(ROOT / path) == sha for path, sha in result.items()),
             "manifest current members")
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


def recursive(path: Path) -> set[Path]:
    path = path.absolute()
    if path.is_file():
        need(not path.is_symlink(), "payload file symlink")
        return {path}
    need(path.is_dir() and not path.is_symlink(), "payload directory")
    result: set[Path] = set()
    for current, directories, files in os.walk(path):
        base = Path(current)
        need(all(not (base / name).is_symlink() for name in directories),
             "payload directory symlink")
        for name in files:
            member = (base / name).absolute()
            need(member.is_file() and not member.is_symlink(),
                 "payload regular member")
            result.add(member)
    return result


def manifest(paths: set[Path]) -> bytes:
    rows: list[tuple[str, str]] = []
    for path in paths:
        path = path.absolute()
        need(path.is_relative_to(ROOT), "manifest workspace member")
        rows.append((str(path.relative_to(ROOT)), file_sha(path)))
    rows.sort()
    need(len(rows) == len({name for name, _ in rows}), "manifest unique")
    return ("\n".join(f"{sha}  {name}" for name, sha in rows) + "\n").encode("ascii")


def validate_terminal(directory: Path, pins: dict[str, str]) -> set[Path]:
    expected = {"PASS.lock", "chain_status.json", "payload_manifest.sha256",
                "root_manifest.sha256", "terminal_receipt.json",
                "terminal_replay.json"}
    need(directory.parent == AUDIT and directory.is_dir()
         and {entry.name for entry in directory.iterdir()} == expected,
         "source terminal inventory")
    need(file_sha(directory / "root_manifest.sha256") == pins["root"]
         and file_sha(directory / "terminal_receipt.json") == pins["receipt_file"]
         and file_sha(directory / "terminal_replay.json") == pins["replay_file"]
         and file_sha(directory / "PASS.lock") == pins["pass"],
         "source terminal file pins")
    receipt = document(directory / "terminal_receipt.json", "terminal_receipt_sha256")
    replay = document(directory / "terminal_replay.json", "terminal_replay_sha256")
    need(receipt["terminal_receipt_sha256"] == pins["receipt_object"]
         and replay["terminal_replay_sha256"] == pins["replay_object"],
         "source terminal object pins")
    members = recursive(directory)
    for name in ("payload_manifest.sha256", "root_manifest.sha256"):
        members.update(ROOT / path for path in parse_manifest(directory / name))
    return members


def execute(args: argparse.Namespace) -> dict[str, Any]:
    values = (args.expect_builder_sha256, args.expect_core_receipt_file_sha256,
              args.expect_core_receipt_object_sha256,
              args.expect_cold_receipt_file_sha256,
              args.expect_cold_receipt_object_sha256,
              args.expect_evidence_file_sha256,
              args.expect_evidence_object_sha256,
              args.expect_release_attacks_file_sha256,
              args.expect_release_attacks_object_sha256)
    need(all(valid_sha(value) for value in values)
         and file_sha(SELF) == args.expect_builder_sha256, "all dynamic/self pins")
    control = Path(args.core_control_dir).absolute()
    cold_control = Path(args.cold_control_dir).absolute()
    cold_output = Path(args.cold_output_dir).absolute()
    cold_run = Path(args.cold_run_dir).absolute()
    evidence_dir = Path(args.evidence_dir).absolute()
    attack_work = Path(args.release_attack_work_dir).absolute()
    attacks_path = Path(args.release_attacks_file).absolute()
    output = Path(args.output_dir).absolute()
    need(output.parent == AUDIT and not output.exists(), "fresh manifest output")
    core_path = control / "core_receipt.json"
    cold_path = cold_control / "cold_replay_receipt.json"
    evidence_path = evidence_dir / "evidence_bundle.json"
    core = document(core_path, "core_receipt_sha256")
    cold = document(cold_path, "cold_replay_receipt_sha256")
    evidence = document(evidence_path, "evidence_bundle_sha256")
    attacks = document(attacks_path, "release_attacks_sha256")
    need(core.get("schema") == CORE_SCHEMA
         and cold.get("schema") == COLD_SCHEMA
         and evidence.get("schema") == EVIDENCE_SCHEMA
         and attacks.get("schema") == ATTACK_SCHEMA
         and attacks.get("status") == ATTACK_STATUS
         and attacks.get("attack_census")
             == {"required": 40, "rejected": 40, "accepted": 0}
         and file_sha(core_path) == args.expect_core_receipt_file_sha256
         and core["core_receipt_sha256"] == args.expect_core_receipt_object_sha256
         and file_sha(cold_path) == args.expect_cold_receipt_file_sha256
         and cold["cold_replay_receipt_sha256"]
             == args.expect_cold_receipt_object_sha256
         and file_sha(evidence_path) == args.expect_evidence_file_sha256
         and evidence["evidence_bundle_sha256"]
             == args.expect_evidence_object_sha256
         and file_sha(attacks_path) == args.expect_release_attacks_file_sha256
         and attacks["release_attacks_sha256"]
             == args.expect_release_attacks_object_sha256
         and all(item.get("formal_credit") == 0
                 and item.get("manifest_authorized") is False
                 for item in (core, cold, evidence, attacks)),
         "release receipt chain")
    pinset = document(control / "pinset.json", "pinset_sha256")
    c27pins = {key: pinset["C27R2_terminal"][key] for key in C27_PINS}
    need(c27pins == C27_PINS, "C27 exact fixed pins")
    c28pins = {key: pinset["C28_terminal"][key]
               for key in ("root", "receipt_file", "receipt_object",
                           "replay_file", "replay_object", "pass")}
    need(all(valid_sha(value) for value in c28pins.values()), "C28 dynamic pins")
    c27_dir = Path(pinset["C27R2_terminal"]["dir"]).absolute()
    c28_dir = Path(pinset["C28_terminal"]["dir"]).absolute()
    paths: set[Path] = {SELF}
    for item in (control, cold_control, cold_output, cold_run, evidence_dir,
                 attack_work, attacks_path):
        paths.update(recursive(item))
    for raw in pinset["targets"].values():
        paths.update(recursive(ROOT / raw))
    paths.update(validate_terminal(c27_dir, c27pins))
    paths.update(validate_terminal(c28_dir, c28pins))
    # Command specs name every external input and frozen source used by the core.
    for path in list(paths):
        if path.name.endswith("_command_spec.json"):
            spec = document(path, "command_spec_sha256")
            for raw in spec.get("input_paths", []):
                member = ROOT / raw
                need(member.exists() and not member.is_symlink(),
                     "command-spec input")
                paths.add(member)
            source = Path(spec.get("source_path", "")).absolute()
            need(source.is_file() and source.is_relative_to(ROOT),
                 "command-spec source")
            paths.add(source)
    if args.preflight_only:
        return {"status": "PASS_C29_V2_RELEASE_RECEIPTS_TERMINALS_AND_FRESH_MANIFEST_PREFLIGHT__NO_OUTPUT_ZERO_CREDIT"}
    output.mkdir(mode=0o700)
    payload_raw = manifest(paths)
    payload_path = output / "payload_manifest.sha256"
    write_once(payload_path, payload_raw)
    root_members = {payload_path, core_path, control / "PASS.lock", cold_path,
                    cold_control / "PASS.lock", evidence_path, attacks_path,
                    c27_dir / "root_manifest.sha256",
                    c27_dir / "terminal_receipt.json",
                    c27_dir / "terminal_replay.json", c27_dir / "PASS.lock",
                    c28_dir / "root_manifest.sha256",
                    c28_dir / "terminal_receipt.json",
                    c28_dir / "terminal_replay.json", c28_dir / "PASS.lock", SELF}
    root_raw = manifest(root_members)
    root_path = output / "root_manifest.sha256"
    write_once(root_path, root_raw)
    body = {"schema": MANIFEST_SCHEMA, "status": MANIFEST_STATUS,
            "built_at_utc": now(), "payload_manifest_sha256": file_sha(payload_path),
            "payload_member_count": len(parse_manifest(payload_path)),
            "root_manifest_sha256": file_sha(root_path),
            "root_member_count": len(parse_manifest(root_path)),
            "core_receipt_file_sha256": args.expect_core_receipt_file_sha256,
            "core_receipt_object_sha256": args.expect_core_receipt_object_sha256,
            "cold_replay_receipt_file_sha256": args.expect_cold_receipt_file_sha256,
            "cold_replay_receipt_object_sha256": args.expect_cold_receipt_object_sha256,
            "evidence_bundle_file_sha256": args.expect_evidence_file_sha256,
            "evidence_bundle_object_sha256": args.expect_evidence_object_sha256,
            "release_attacks_file_sha256": args.expect_release_attacks_file_sha256,
            "release_attacks_object_sha256": args.expect_release_attacks_object_sha256,
            "C27R2_terminal_pins": c27pins, "C28_terminal_pins": c28pins,
            "dual_predecessor_root_closure": True,
            "formal_credit": 0, "manifest_authorized": False,
            "C29": "UNAUTHORIZED_PENDING_INDEPENDENT_OUTER_SEAL_TERMINAL_REPLAY",
            "Source_W": "UNCHANGED", "CM2": "NO-GO_FOR_CLAIM"}
    receipt = dict(body)
    receipt["manifest_receipt_sha256"] = digest(receipt)
    write_once(output / "manifest_receipt.json", canonical(receipt) + b"\n")
    return receipt


def self_test() -> dict[str, Any]:
    need(all(valid_sha(value) for value in C27_PINS.values()), "C27 pins")
    return {"status": "PASS_C29_V2_RELEASE_MANIFEST_BUILDER_SELF_TEST",
            "formal_credit": 0, "C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--preflight-only", action="store_true")
    for name in ("core-control-dir", "cold-control-dir", "cold-output-dir",
                 "cold-run-dir", "evidence-dir", "release-attack-work-dir",
                 "release-attacks-file", "output-dir",
                 "expect-core-receipt-file-sha256",
                 "expect-core-receipt-object-sha256",
                 "expect-cold-receipt-file-sha256",
                 "expect-cold-receipt-object-sha256",
                 "expect-evidence-file-sha256", "expect-evidence-object-sha256",
                 "expect-release-attacks-file-sha256",
                 "expect-release-attacks-object-sha256",
                 "expect-builder-sha256"):
        parser.add_argument("--" + name)
    args = parser.parse_args()
    fields = tuple(name.replace("-", "_") for name in (
        "core-control-dir", "cold-control-dir", "cold-output-dir",
        "cold-run-dir", "evidence-dir", "release-attack-work-dir",
        "release-attacks-file", "output-dir",
        "expect-core-receipt-file-sha256", "expect-core-receipt-object-sha256",
        "expect-cold-receipt-file-sha256", "expect-cold-receipt-object-sha256",
        "expect-evidence-file-sha256", "expect-evidence-object-sha256",
        "expect-release-attacks-file-sha256",
        "expect-release-attacks-object-sha256", "expect-builder-sha256"))
    try:
        if args.self_test:
            need(not args.preflight_only
                 and all(getattr(args, field) is None for field in fields),
                 "self-test arguments")
            result = self_test()
        else:
            need(all(getattr(args, field) is not None for field in fields),
                 "run arguments")
            result = execute(args)
        sys.stdout.buffer.write(canonical({"CM2": "NO-GO_FOR_CLAIM",
            "formal_credit": 0, "status": result["status"]}) + b"\n")
        return 0
    except (Blocked, OSError, ValueError, KeyError, TypeError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
