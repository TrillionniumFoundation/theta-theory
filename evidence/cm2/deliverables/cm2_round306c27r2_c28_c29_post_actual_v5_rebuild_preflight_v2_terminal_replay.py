#!/usr/bin/env python3
"""Cold manifest-first terminal replay of the v2 truthful-REJECT seal."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
from typing import Any


WORKSPACE = Path(__file__).resolve().parent.parent
ACTUAL = (WORKSPACE / ".cm2-runtime/audit/"
          "c27-primitive-twenty-family-gate-v5-actual-zero-credit-receipt-v2/receipt.json")


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


def fsha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fp(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns,
            info.st_ctime_ns, info.st_mode, info.st_uid, info.st_gid)


def parse_manifest(path: Path) -> list[tuple[str, str]]:
    entries = []
    for ordinal, line in enumerate(path.read_text("utf-8").splitlines()):
        pieces = line.split("  ", 1)
        need(len(pieces) == 2 and len(pieces[0]) == 64, f"manifest:{ordinal}")
        entries.append((pieces[1], pieces[0]))
    return entries


def closed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_bytes())
    body = dict(value)
    claim = body.pop(field, None)
    need(type(claim) is str and claim == digest(body), path.name + ":closure")
    return value


def write_new(path: Path, value: dict[str, Any]) -> None:
    path = path.resolve()
    need(path.is_relative_to(WORKSPACE), "output:workspace")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                 | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        os.write(fd, canonical(value) + b"\n")
        os.fsync(fd)
    finally:
        os.close(fd)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seal-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        seal = Path(args.seal_dir).resolve()
        root = seal / "root_manifest.sha256"
        payload = seal / "payload_manifest.sha256"
        receipt_path = seal / "receipt.json"
        root_entries = dict(parse_manifest(root))
        need(root_entries == {
            "payload_manifest.sha256": fsha(payload),
            "receipt.json": fsha(receipt_path),
        }, "root:closure")
        entries = parse_manifest(payload)
        need(len(entries) == 21 and len({path for path, _ in entries}) == 21,
             "payload:21-unique")
        before = {}
        for relative, sha in entries:
            path = (WORKSPACE / relative).resolve()
            need(path.is_relative_to(WORKSPACE) and path.is_file(), "payload:path")
            info = path.stat()
            need(stat.S_ISREG(info.st_mode), "payload:regular")
            before[relative] = fp(info)
            need(fsha(path) == sha and fp(path.stat()) == before[relative],
                 "payload:hash-stat:" + relative)
        receipt = closed(receipt_path, "receipt_sha256")
        need(receipt["status"] ==
             "PASS_SEALED_TRUTHFUL_REJECT_ACTUAL_V5_V2_MISSING__NO_IMPORT_VERIFIER__42_ATTACKS__ZERO_CREDIT",
             "receipt:status")
        need(receipt["preflight"]["numeric_exit_code"] == 2
             and receipt["preflight"]["signal"] is None
             and receipt["preflight"]["stdout_empty"] is True
             and receipt["preflight"]["stderr_empty"] is True,
             "receipt:execution")
        need(receipt["coherent_resigned_attacks"] == {
            "file_sha256": receipt["coherent_resigned_attacks"]["file_sha256"],
            "object_sha256": receipt["coherent_resigned_attacks"]["object_sha256"],
            "attacks": 42, "rejected": 42, "accepted": 0,
        }, "receipt:attacks")
        need(receipt["exact_eventual_contract"] == {
            "candidate_count": 7_486_076, "proof_count": 65_064,
            "disposition_sum": 7_486_076,
            "dispositions": {
                "CROSS_COMPONENT__MATERIALIZED_PHYSICAL_PROOF_REQUIRED": 65_064,
                "SAME_FROZEN_C15_COMPONENT__NO_EDGE": 264_156,
                "NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS": 7_156_856,
            }}, "receipt:contract")
        need(receipt["diagnostics_never_authority"] == {
            "component_edge_expectation": 14_860,
            "fresh_DSU_component_expectation": 43_684,
            "historical_14772_or_14724_used": False,
        }, "receipt:diagnostics")
        need(not ACTUAL.exists() and receipt["actual_gate_v2_receipt_present"] is False
             and receipt["fresh_C27R2_C28_C29_producer_may_start"] is False,
             "receipt:blocker")
        need(receipt["formal_credit"] == 0 and receipt["manifest_authorized"] is False
             and receipt["C27R2"] == receipt["C28"] == receipt["C29"] == "UNAUTHORIZED"
             and receipt["Source_W_transition_authorized"] is False
             and receipt["Source_W_formal_remainder"] == 80
             and receipt["CM2"] == "NO-GO_FOR_CLAIM", "receipt:nonpromotion")
        for relative, _ in entries:
            need(fp((WORKSPACE / relative).resolve().stat()) == before[relative],
                 "payload:post-stat:" + relative)
        body = {
            "schema": "cm2.round306c27r2-c28-c29.post-actual-v5-rebuild-preflight-cold-terminal-replay.v1",
            "status": "PASS_COLD_MANIFEST_FIRST_21_PAYLOADS_TRUTHFUL_REJECT_REPLAY__PRE_POST_STAT_IDENTICAL__ZERO_CREDIT",
            "seal_receipt_file_sha256": fsha(receipt_path),
            "seal_receipt_object_sha256": receipt["receipt_sha256"],
            "payload_manifest_file_sha256": fsha(payload),
            "root_manifest_file_sha256": fsha(root),
            "payload_entries": 21, "pre_post_stat_identical": True,
            "all_payload_hashes_verified": True,
            "numeric_exit_code": 2, "signal": None,
            "actual_gate_v2_receipt_present": False,
            "formal_credit": 0, "manifest_authorized": False,
            "C27R2_C28_C29": "UNAUTHORIZED", "Source_W_formal_remainder": 80,
            "CM2": "NO-GO_FOR_CLAIM",
        }
        body["terminal_replay_sha256"] = digest(body)
        write_new(Path(args.output), body)
        return 0
    except (Failure, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError) as exc:
        print("REJECT:" + str(exc))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
