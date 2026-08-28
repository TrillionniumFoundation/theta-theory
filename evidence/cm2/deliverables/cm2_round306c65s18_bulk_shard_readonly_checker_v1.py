#!/usr/bin/env python3
"""Read-only first-layer verifier for one frozen C65s18 v3 shard.

This checker deliberately does not import or execute the shard producer.  It
checks byte/object closure, the compressed ledger, assignment grouping, local
prefix/Kraft conservation, zero-credit locks, and the live authority snapshot.
It is diagnostic only and mints no aggregate or formal credit.
"""

from __future__ import annotations

import argparse
import copy
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import stat
from typing import Any
import zlib


OUT = Path(__file__).resolve().parent
ROOT = OUT.parent
BASE = "cm2_round306c65s18_depth18_64shard"
RUNNER_SHA = "170df261ed9451fc3ecc1fca5e686c6f6d8eeb3d643126da09f30c634cda22ef"
AUTHORITY_OBJECT_SHA = "c9a8b97be4bed2008fa132f49e0d4ac0b384e973707ecdf48b27028b7d7e93cf"
ASSIGNMENT_DOMAIN = "cm2.round306c65s18.depth18-64shard.v2.assignment"
EXPECTED_AUTHORITY = {
    "C50d_global_claim": "3801e452f218e330bc16faed5986146202a7d7026e46924bf7bc00167b05f77b",
    "C50d_global_head": "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3",
    "C53_audit_token": "c3a9a3248b2ec3cb0887b62f4edade7664f73f1746593be1b69897404ae42eba",
    "C53_successor_token": "dcad8792bb4bede7f97f9996d10b43497b6286704dbc8f1b8a4170a9e2416846",
    "CM2_LATEST_STATUS.md": "922fc5d01918b217556bc3f392c44efcc7c9c6345c881371e6cd34950eb99b57",
    "CM2_LATEST_STATUS.sha256": "57d0c75a2dc774d312fc72a11c66e745cf9b7232531e469490bac492b0a91d6b",
}
AUTHORITY_PATHS = {
    "C50d_global_claim": ROOT / ".cm2-runtime/cm2-global-successor-claims/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.claim",
    "C50d_global_head": ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal",
    "C53_audit_token": ROOT / ".cm2-runtime/c53-current-pair-successor-audit-token",
    "C53_successor_token": ROOT / ".cm2-runtime/c53-current-pair-successor-token",
    "CM2_LATEST_STATUS.md": OUT / "CM2_LATEST_STATUS.md",
    "CM2_LATEST_STATUS.sha256": OUT / "CM2_LATEST_STATUS.sha256",
}


class FailClosed(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if not value:
        raise FailClosed(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def strict_loads(raw: bytes) -> Any:
    need(not raw.startswith(b"\xef\xbb\xbf"), "BOM forbidden")

    def hook(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(key not in result, "duplicate JSON key:" + key)
            result[key] = value
        return result

    return json.loads(raw, object_pairs_hook=hook,
                      parse_constant=lambda value: (_ for _ in ()).throw(
                          FailClosed("nonfinite JSON:" + value)))


def read_regular(path: Path) -> bytes:
    before = path.lstat()
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
         "regular single-link:" + path.name)
    flags = os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    try:
        opened = os.fstat(fd)
        need((opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns) ==
             (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns),
             "open identity:" + path.name)
        parts: list[bytes] = []
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            parts.append(block)
        after = os.fstat(fd)
        current = path.lstat()
        need((after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns) ==
             (opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns) and
             (current.st_dev, current.st_ino, current.st_size, current.st_mtime_ns) ==
             (opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns),
             "stable fd/path identity:" + path.name)
        return b"".join(parts)
    finally:
        os.close(fd)


def authority_snapshot() -> dict[str, str]:
    return {key: sha(read_regular(path)) for key, path in AUTHORITY_PATHS.items()}


def inflate_exact(raw: bytes, limit: int = 512 * 1024 * 1024) -> bytes:
    inflater = zlib.decompressobj(16 + zlib.MAX_WBITS)
    plain = inflater.decompress(raw, limit + 1)
    need(len(plain) <= limit and not inflater.unconsumed_tail, "bounded gzip")
    plain += inflater.flush()
    need(inflater.eof and not inflater.unused_data and not inflater.unconsumed_tail,
         "one complete gzip member/no trailing bytes")
    need(plain and plain.endswith(b"\n"), "nonempty newline-framed ledger")
    return plain


def verify(shard: int) -> dict[str, Any]:
    need(0 <= shard < 64, "shard range")
    receipt_path = OUT / f"{BASE}_shard_{shard:02d}_receipt_v3.json"
    ledger_path = OUT / f"{BASE}_shard_{shard:02d}_leaf_ledger_v3.jsonl.gz"
    receipt_raw = read_regular(receipt_path)
    receipt = strict_loads(receipt_raw)
    need(type(receipt) is dict and receipt_raw == canonical(receipt) + b"\n",
         "canonical receipt bytes")
    body = copy.deepcopy(receipt)
    object_claim = body.pop("object_sha256", None)
    need(type(object_claim) is str and digest(body) == object_claim,
         "receipt object closure")
    need(receipt.get("schema") ==
         "cm2.round306c65s18.depth18-64shard.v3.shard-receipt" and
         receipt.get("status") ==
         "PASS_COMPLETE_NO_REPLACE_DEPTH18_SHARD__ZERO_CREDIT",
         "receipt schema/status")
    need(receipt.get("runner_file_sha256") == RUNNER_SHA and
         receipt.get("shard_id") == shard and receipt.get("shard_count") == 64 and
         receipt.get("additional_binary_depth") == 6 and
         receipt.get("shard_complete") is True,
         "runner/shard/depth closure")
    need(receipt.get("formal_credit") == receipt.get("whole_parent_credit") ==
         receipt.get("D02_gate_credit") == 0 and
         receipt.get("partial_statistics_are_formal_credit") is False and
         receipt.get("runtime_canonical_pointer_or_seal_writes") is False,
         "receipt zero-credit boundary")
    current = authority_snapshot()
    need(current == EXPECTED_AUTHORITY and digest(current) == AUTHORITY_OBJECT_SHA and
         receipt.get("authority_snapshot_before") == current and
         receipt.get("authority_snapshot_after") == current and
         receipt.get("authority_snapshot_object_sha256") == AUTHORITY_OBJECT_SHA,
         "authority snapshot closure")

    descriptor = receipt.get("output_ledger")
    need(type(descriptor) is dict and descriptor.get("filename") == ledger_path.name and
         descriptor.get("order") == "ASSIGNMENT_INVENTORY_ORDER_THEN_PATH",
         "ledger descriptor name/order")
    ledger_raw = read_regular(ledger_path)
    need(descriptor.get("sha256") == sha(ledger_raw) and
         descriptor.get("size") == len(ledger_raw), "ledger byte closure")
    plain = inflate_exact(ledger_raw)
    sequence = hashlib.sha256()
    rows: list[dict[str, Any]] = []
    dispositions = {"STRICT_TERMINAL": 0, "COLLISION3_READY": 0,
                    "COLLISION2_HANDOFF": 0}
    raw_census: dict[str, int] = {}
    grouped: dict[str, list[dict[str, Any]]] = {}
    group_order: list[str] = []
    preimage_by_source: dict[str, str] = {}
    for framed in plain.splitlines(keepends=True):
        need(framed.endswith(b"\n") and framed != b"\n", "ledger row framing")
        line = framed[:-1]
        row = strict_loads(line)
        need(type(row) is dict and line == canonical(row), "canonical ledger row")
        row_body = copy.deepcopy(row)
        row_claim = row_body.pop("row_sha256", None)
        need(type(row_claim) is str and digest(row_body) == row_claim,
             "ledger row object closure")
        sequence.update((row_claim + "\n").encode("ascii"))
        need(row.get("schema") ==
             "cm2.round306c65s18.depth18-64shard.v3.shard-leaf-row" and
             row.get("shard_id") == shard, "ledger row schema/shard")
        disposition = row.get("disposition")
        need(disposition in dispositions, "known disposition")
        dispositions[disposition] += 1
        route = row.get("route_classification")
        need(type(route) is str, "route classification")
        raw_census[route] = raw_census.get(route, 0) + 1
        need(row.get("formal_credit") == row.get("whole_parent_credit") ==
             row.get("D02_gate_credit") == 0 and
             row.get("local_terminal_credit") ==
             (1 if disposition == "STRICT_TERMINAL" else 0),
             "row credit lock")
        continuation = row.get("continuation")
        if continuation is not None:
            need(type(continuation) is dict and
                 continuation.get("continuation_credit") == 0,
                 "continuation zero credit")
            continuation_body = copy.deepcopy(continuation)
            continuation_claim = continuation_body.pop("continuation_object_sha256", None)
            need(type(continuation_claim) is str and
                 digest(continuation_body) == continuation_claim,
                 "continuation object closure")
        else:
            need(disposition == "STRICT_TERMINAL", "terminal-only null continuation")
        source = row.get("source_C61_aggregate_leaf_row_sha256")
        path = row.get("source_path")
        preimage_claim = row.get("assignment_preimage_sha256")
        need(type(source) is str and len(source) == 64 and type(path) is str and
             len(path) == 21 and set(path) <= {"0", "1"}, "source identity")
        preimage = canonical({"assignment_domain": ASSIGNMENT_DOMAIN, "path": path,
                              "source_C61_aggregate_leaf_row_sha256": source})
        need(sha(preimage) == preimage_claim and int(preimage_claim, 16) % 64 == shard,
             "assignment replay")
        if source not in grouped:
            grouped[source] = []
            group_order.append(source)
            preimage_by_source[source] = preimage_claim
        need(preimage_by_source[source] == preimage_claim,
             "stable source assignment preimage")
        grouped[source].append(row)
        rows.append(row)
    need(len(rows) == descriptor.get("row_count") and
         sequence.hexdigest() == descriptor.get("row_hash_line_sequence_sha256"),
         "ledger count/sequence closure")
    need(dispositions == receipt.get("output_disposition_census") and
         dict(sorted(raw_census.items())) == receipt.get("raw_classification_census"),
         "ledger census closure")

    summaries = receipt.get("input_assignment_rows")
    need(type(summaries) is list and len(summaries) ==
         receipt.get("assigned_input_count") == len(group_order),
         "assignment summary count")
    assignment_sequence = hashlib.sha256()
    for index, summary in enumerate(summaries):
        source = group_order[index]
        need(summary.get("source_C61_aggregate_leaf_row_sha256") == source and
             summary.get("assignment_preimage_sha256") == preimage_by_source[source],
             "assignment summary order/identity")
        assignment_sequence.update((preimage_by_source[source] + "\n").encode("ascii"))
        source_rows = grouped[source]
        source_sequence = sha("".join(row["row_sha256"] + "\n"
                                      for row in source_rows).encode("ascii"))
        need(summary.get("source_output_row_count") == len(source_rows) and
             summary.get("source_output_row_hash_line_sequence_sha256") == source_sequence and
             summary.get("source_prefix_free") is True,
             "source summary row closure")
        paths = [row["path"] for row in source_rows]
        ordered = sorted(paths, key=lambda value: (len(value), value))
        need(len(paths) == len(set(paths)) and
             all(not later.startswith(first) for pos, first in enumerate(ordered)
                 for later in ordered[pos + 1:]), "source prefix-free replay")
        total = sum((Fraction(row["parent_volume_fraction"]) for row in source_rows),
                    Fraction(0))
        need(total == Fraction(summary["source_Kraft_conservation"]),
             "source Kraft replay")
    need(assignment_sequence.hexdigest() ==
         receipt.get("ordered_assignment_preimage_sha256_line_sequence_sha256"),
         "assignment sequence closure")
    return {
        "status": "PASS_READ_ONLY_FIRST_LAYER_ZERO_CREDIT",
        "shard_id": shard,
        "receipt_file_sha256": sha(receipt_raw),
        "receipt_object_sha256": object_claim,
        "ledger_file_sha256": descriptor["sha256"],
        "ledger_row_count": len(rows),
        "assigned_input_count": len(summaries),
        "output_disposition_census": dispositions,
        "authority_snapshot_object_sha256": AUTHORITY_OBJECT_SHA,
        "formal_credit": 0,
        "whole_parent_credit": 0,
        "D02_gate_credit": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shard", type=int, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args.shard), sort_keys=True,
                         separators=(",", ":")))
        return 0
    except (FailClosed, KeyError, TypeError, ValueError, OSError) as error:
        print(json.dumps({"status": "FAIL_CLOSED", "reason": str(error)},
                         sort_keys=True, separators=(",", ":")))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
