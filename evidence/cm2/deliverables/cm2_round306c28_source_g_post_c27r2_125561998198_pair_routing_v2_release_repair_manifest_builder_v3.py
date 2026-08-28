#!/usr/bin/env python3
"""Build append-only manifest-first C28 release-repair package v3.

Only the C27R2 terminal is a predecessor authority.  The earlier C28 terminal
is recorded as historical audit evidence and is deliberately absent from the
authority root.  This builder cannot write a seal, terminal receipt or PASS.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
AUDIT = ROOT / ".cm2-runtime/audit"
BASE = "cm2.round306c28.source-g-post-c27r2-125561998198-pair-routing.v2."
EVIDENCE_SCHEMA = BASE + "release-repair-evidence-bundle.v2"
EVIDENCE_STATUS = ("PASS_C28_RELEASE_REPAIR_CORE_COLD_CURRENT_BOUNDARY_AND_"
    "52_REAL_CASE_PROCESS_TRANSCRIPTS_REOPENED__ZERO_CREDIT_PENDING_MANIFEST")
MANIFEST_SCHEMA = BASE + "release-repair-manifest-receipt.v3"
MANIFEST_STATUS = ("PASS_C28_RELEASE_REPAIR_MANIFEST_FIRST_CURRENT_CORE_COLD_"
    "BOUNDARY_52_CASE_EVIDENCE_AND_C27R2_ROOT_CLOSURE__ZERO_CREDIT_"
    "PENDING_INDEPENDENT_OUTER")
C27_STATUS = "PASS_C27R2_TERMINAL_BYTE_REPLAY__FORMAL_C27R2_AUTHORITY_MINTED"
C27_PASS = b"PASS_C27R2_AUTHORITY_V2_TERMINAL_BYTE_REPLAY__C28_C29_UNAUTHORIZED\n"
C27 = {"root": "1f65a624c889773e3104c4311788fc06be04d6ca92e033205074b8cc7f5b27fc",
    "receipt_file": "feccb0b9290bd82ac1d8e78e8e7a21d4f25e0ca3aa3556cc3f0bb6007f61c3dd",
    "receipt_object": "8afbd127c9518f569c2f7b3edcdbe9e0ebf77d88bcca855822e58d21e5cfe782",
    "replay_file": "b480df4b8caaf9876a48720f92a8fb6d86e2b1b5966bcc71b0022c5e49fc12ee",
    "replay_object": "216d2592c49b0302de0042677ce54c96cd5ad1fcb32231da02b39c003cb837e8",
    "pass": "5fe4140b3e8f38196e9ca68cd336ae29be1c8847c7685526f08aa4d7173d7348"}
HISTORICAL = {"root": "252964856f55584dc2fab6f7a1f0ac4cadd66fd6935b4063bdbe0eb455ba0982",
    "receipt_file": "bde9d40da7f5a548f75d0885b377d3f1a654786be5f748b14a2e1b0ea720ec73",
    "receipt_object": "53eca26fcfa87a6f8c4f557740dd4170b0f38ff54afec07f82af82a035ad7f13",
    "replay_file": "ad93a50c9871dd2cf771256ffb3ad4485c648de695453118956831f0e2c16750",
    "replay_object": "5bcaa87e88ebf2214bde5462bd3148f6600732c3d79394a234a7c447aba99079"}
EXPECTED = {"members": 502_204, "post_components": 43_684,
    "blocks": 256, "shards": 32_896, "total_pairs": 126_104_177_706,
    "within_pairs": 542_179_508, "cross_pairs": 125_561_998_198}


class Blocked(RuntimeError): pass


def need(v: bool, label: str) -> None:
    if type(v) is not bool or not v: raise Blocked(label)


def canonical(v: Any) -> bytes:
    return json.dumps(v, sort_keys=True, separators=(",", ":"),
        ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(v: Any) -> str: return hashlib.sha256(canonical(v)).hexdigest()


def valid_sha(v: Any) -> bool:
    return type(v) is str and re.fullmatch(r"[0-9a-f]{64}", v) is not None


def strict(raw: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for k, v in items: need(k not in out, "duplicate JSON key"); out[k] = v
        return out
    return json.loads(raw, object_pairs_hook=pairs)


def inside(raw: str | Path, absent: bool = False) -> Path:
    supplied = Path(raw)
    path = (supplied if supplied.is_absolute() else ROOT / supplied).absolute()
    try: relative = path.relative_to(ROOT)
    except ValueError as error: raise Blocked("outside workspace") from error
    need(relative.parts and all(p not in {"", ".", ".."} for p in relative.parts),
         "canonical path")
    cursor = ROOT
    for part in relative.parts:
        cursor /= part
        if not cursor.exists(): need(absent, "missing path"); break
        need(not cursor.is_symlink(), "symlink path")
    return path


def fp(info: os.stat_result) -> list[int]:
    return [info.st_dev, info.st_ino, info.st_mode, info.st_nlink,
        info.st_size, info.st_mtime_ns, info.st_ctime_ns, info.st_uid, info.st_gid]


def rec(path: Path) -> dict[str, Any]:
    need(path.is_file() and not path.is_symlink(), "regular file")
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd); need(stat.S_ISREG(before.st_mode)
            and before.st_nlink == 1, "single-link")
        h = hashlib.sha256()
        while block := os.read(fd, 4 << 20): h.update(block)
        need(fp(os.stat(path, follow_symlinks=False)) == fp(before), "stable file")
        return {"path": str(path.relative_to(ROOT)), "sha256": h.hexdigest(),
                "size": before.st_size, "stat_fingerprint": fp(before)}
    finally: os.close(fd)


def doc(path: Path, closure: str) -> tuple[dict[str, Any], dict[str, Any]]:
    r = rec(path); raw = path.read_bytes(); need(raw.endswith(b"\n"), "newline")
    v = strict(raw[:-1]); need(type(v) is dict and canonical(v) == raw[:-1],
        "canonical JSON")
    b = dict(v); claim = b.pop(closure, None)
    need(valid_sha(claim) and claim == digest(b), "object closure")
    return v, r


def parse_manifest(path: Path) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    raw = path.read_bytes(); need(raw.endswith(b"\n"), "manifest newline")
    for line in raw.decode("ascii").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\x00\r\n]+)", line)
        need(match is not None, "manifest line")
        claim, shown = match.groups(); need(shown not in result, "duplicate path")
        item = rec(inside(shown)); need(item["sha256"] == claim, "manifest SHA")
        result[shown] = item
    need(result and list(result) == sorted(result), "sorted nonempty manifest")
    return result


def manifest(paths: set[Path]) -> bytes:
    rows = []
    for path in sorted(paths):
        item = rec(path); rows.append(f"{item['sha256']}  {item['path']}\n")
    need(rows, "nonempty manifest")
    return "".join(rows).encode("ascii")


def write(path: Path, raw: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                 | getattr(os, "O_NOFOLLOW", 0), 0o400)
    try: os.write(fd, raw); os.fsync(fd)
    finally: os.close(fd)


def predecessor(path: Path) -> set[Path]:
    names = {"PASS.lock", "chain_status.json", "payload_manifest.sha256",
        "root_manifest.sha256", "terminal_receipt.json", "terminal_replay.json"}
    need(path.is_dir() and {p.name for p in path.iterdir()} == names,
         "C27 exact inventory")
    receipt, rr = doc(path / "terminal_receipt.json", "terminal_receipt_sha256")
    replay, rp = doc(path / "terminal_replay.json", "terminal_replay_sha256")
    need(rec(path / "root_manifest.sha256")["sha256"] == C27["root"]
         and rr["sha256"] == C27["receipt_file"]
         and receipt["terminal_receipt_sha256"] == C27["receipt_object"]
         and rp["sha256"] == C27["replay_file"]
         and replay["terminal_replay_sha256"] == C27["replay_object"]
         and rec(path / "PASS.lock")["sha256"] == C27["pass"]
         and (path / "PASS.lock").read_bytes() == C27_PASS
         and receipt.get("status") == C27_STATUS
         and receipt.get("authority_minted") is True,
         "C27 terminal pins")
    return {path / name for name in names}


def execute(args: argparse.Namespace) -> dict[str, Any]:
    pins = (args.expect_self_sha256, args.expect_evidence_file_sha256,
            args.expect_evidence_object_sha256)
    need(all(valid_sha(x) for x in pins) and rec(SELF)["sha256"]
         == args.expect_self_sha256, "dynamic pins/self")
    evidence_dir = inside(args.evidence_dir)
    evidence, er = doc(evidence_dir / "evidence_bundle.json",
                       "evidence_bundle_sha256")
    inventory_path = evidence_dir / "authority_inventory.sha256"
    inventory = parse_manifest(inventory_path)
    need(er["sha256"] == args.expect_evidence_file_sha256
         and evidence["evidence_bundle_sha256"]
             == args.expect_evidence_object_sha256
         and evidence.get("schema") == EVIDENCE_SCHEMA
         and evidence.get("status") == EVIDENCE_STATUS
         and evidence.get("authority_inventory_file_sha256")
             == rec(inventory_path)["sha256"]
         and evidence.get("authority_inventory_member_count") == len(inventory)
         and evidence.get("real_attack_cases_total") == 52
         and evidence.get("real_attack_cases_rejected") == 52
         and evidence.get("exact_math") == EXPECTED
         and evidence.get("formal_credit") == 0,
         "evidence exact closure")
    candidate = inside(args.candidate_dir)
    verification1 = inside(args.verification1)
    verification2 = inside(args.verification2)
    core_attacks = inside(args.core_attacks)
    files = {inside(path) for path in inventory}
    files |= {evidence_dir / "evidence_bundle.json", inventory_path, SELF,
              candidate / "member_home_block_census.jsonl.gz",
              candidate / "cross_component_pair_route_shard.jsonl.gz",
              candidate / "result.json", verification1, verification2,
              core_attacks}
    for raw in args.source_file:
        files.add(inside(raw))
    need(len({p.name for p in candidate.iterdir()}) == 3
         and all(p.is_file() and not p.is_symlink() for p in candidate.iterdir()),
         "candidate exact three files")
    result, _ = doc(candidate / "result.json", "result_sha256")
    need(result.get("post_C27R2_partition_census", {}).get("members")
             == EXPECTED["members"]
         and result.get("post_C27R2_partition_census", {}).get("components")
             == EXPECTED["post_components"]
         and result.get("pair_route_census", {}).get("closed_shards")
             == EXPECTED["shards"] and result.get("formal_credit") == 0,
         "candidate result math")
    predecessor_files = predecessor(inside(args.predecessor_terminal_dir))
    payload_raw = manifest(files)
    output = inside(args.output_dir, absent=True)
    need(not output.exists() and not output.is_symlink(), "fresh output")
    output.mkdir(parents=True, mode=0o700)
    payload_path = output / "payload_manifest.sha256"; write(payload_path, payload_raw)
    root_files = set(predecessor_files) | {payload_path, SELF}
    root_raw = manifest(root_files)
    root_path = output / "root_manifest.sha256"; write(root_path, root_raw)
    body = {"schema": MANIFEST_SCHEMA, "status": MANIFEST_STATUS,
        "completed_at_utc": datetime.now(timezone.utc).isoformat(
            timespec="microseconds").replace("+00:00", "Z"),
        "evidence_bundle_file_sha256": er["sha256"],
        "evidence_bundle_object_sha256": evidence["evidence_bundle_sha256"],
        "boundary_receipt_object_sha256": evidence["boundary_receipt_object_sha256"],
        "attack_receipt_object_sha256": evidence["attack_receipt_object_sha256"],
        "payload_manifest_file_sha256": rec(payload_path)["sha256"],
        "payload_member_count": len(files),
        "root_manifest_file_sha256": rec(root_path)["sha256"],
        "root_member_count": len(root_files),
        "C27R2_terminal_root_manifest_sha256": C27["root"],
        "predecessor_authority": "C27R2_TERMINAL_ONLY",
        "historical_C28_terminal": {**HISTORICAL, "role": "AUDIT_EVIDENCE_ONLY",
                                     "authority_eligible": False,
                                     "included_in_authority_root": False},
        "exact_math": EXPECTED, "real_attack_cases": 52,
        "formal_credit": 0, "manifest_authorized": False,
        "C28": "AUDIT_HOLD_UNAUTHORIZED", "C29": "UNAUTHORIZED",
        "CM2": "NO-GO_FOR_CLAIM"}
    receipt = {**body, "manifest_receipt_sha256": digest(body)}
    write(output / "manifest_receipt.json", canonical(receipt) + b"\n")
    need({p.name for p in output.iterdir()} == {"manifest_receipt.json",
         "payload_manifest.sha256", "root_manifest.sha256"}, "output inventory")
    return receipt


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__); p.add_argument("--self-test", action="store_true")
    names = ("evidence-dir", "candidate-dir", "verification1", "verification2",
        "core-attacks", "predecessor-terminal-dir", "output-dir",
        "expect-self-sha256", "expect-evidence-file-sha256",
        "expect-evidence-object-sha256")
    for name in names: p.add_argument("--" + name)
    p.add_argument("--source-file", action="append")
    args = p.parse_args()
    try:
        if args.self_test:
            need(all(getattr(args, n.replace("-", "_")) is None for n in names)
                 and args.source_file is None, "self-test no args")
            need(EXPECTED["total_pairs"] == EXPECTED["within_pairs"]
                 + EXPECTED["cross_pairs"] and HISTORICAL["root"] != C27["root"],
                 "manifest fixtures")
            result = {"status": "PASS_C28_RELEASE_REPAIR_MANIFEST_V3_SELF_TEST"}
        else:
            need(all(getattr(args, n.replace("-", "_")) is not None for n in names)
                 and type(args.source_file) is list and args.source_file,
                 "all manifest arguments")
            result = execute(args)
        sys.stdout.buffer.write(canonical({"CM2": "NO-GO_FOR_CLAIM",
            "formal_credit": 0, "status": result["status"]}) + b"\n"); return 0
    except (Blocked, OSError, ValueError, KeyError, TypeError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n"); return 2


if __name__ == "__main__": raise SystemExit(main())
