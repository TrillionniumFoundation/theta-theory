#!/usr/bin/env python3
"""Cold manifest-first replay for the corrected T04 common-v2 terminal seal."""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import json
import os
from pathlib import Path
import stat
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parent.parent
EMPTY = hashlib.sha256(b"").hexdigest()
DISPOSITION = "NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS"
EXPECTED = {
    "CROSS_CHART_QUOTIENT_RECHART": 1_361_424,
    "SAME_CHART_TRANSVERSE_1D": 448,
    "CROSS_CHART_GRAPH_SIDE_T0": 192,
    "CODIMENSION_TWO_LOWER_OWNER": 24,
}


class Reject(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def enc(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(enc(value)).hexdigest()


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            state.update(block)
    return state.hexdigest()


def document(path: Path, closure: str) -> dict[str, Any]:
    value = json.loads(path.read_bytes())
    body = dict(value)
    claim = body.pop(closure, None)
    need(claim == digest(body), "document closure:" + path.name)
    return value


def parse_manifest(path: Path) -> list[tuple[str, Path]]:
    entries: list[tuple[str, Path]] = []
    seen: set[str] = set()
    for line in path.read_text("ascii").splitlines():
        claim, relative = line.split("  ", 1)
        need(relative not in seen, "manifest duplicate")
        seen.add(relative)
        target = (ROOT / relative).resolve()
        need(target.is_relative_to(ROOT), "manifest escape")
        entries.append((claim, target))
    return entries


def snapshot(path: Path) -> tuple[int, int, int, int, int]:
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode) and not path.is_symlink(),
         "regular no-symlink member:" + str(path))
    return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns,
            stat.S_IMODE(info.st_mode))


def rows(path: Path) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rt", encoding="ascii") as stream:
        for ordinal, line in enumerate(stream):
            row = json.loads(line)
            body = dict(row)
            claim = body.pop("row_sha256", None)
            need(claim == digest(body), "row closure:" + path.name + ":" + str(ordinal))
            yield row


def next_required(stream: Iterator[dict[str, Any]], label: str,
                  ordinal: int) -> dict[str, Any]:
    try:
        return next(stream)
    except StopIteration as exc:
        raise Reject("omission:" + label + ":" + str(ordinal)) from exc


def no_extra(stream: Iterator[dict[str, Any]], label: str) -> None:
    try:
        next(stream)
    except StopIteration:
        return
    raise Reject("extra row:" + label)


def write_new(path: Path, payload: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                 | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        os.write(fd, payload)
        os.fsync(fd)
    finally:
        os.close(fd)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seal-dir", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    seal = Path(args.seal_dir).resolve()
    output = Path(args.out_dir).resolve()
    need(not output.exists(), "fresh cold replay output")
    receipt_path = seal / "receipt.json"
    payload_manifest_path = seal / "payload_manifest.sha256"
    root_manifest_path = seal / "root_manifest.sha256"
    receipt = document(receipt_path, "receipt_sha256")
    need(receipt["candidate_pairs"] == 1_362_088
         and receipt["terminal_absence_authority_rows"] == 1_362_088
         and receipt["materialized_physical_proof_rows"] == 0
         and receipt["component_relation_disposition"] == DISPOSITION
         and receipt["legal_cross_component_witnesses"] == 0
         and receipt["component_edges"] == 0 and receipt["unresolved"] == 0
         and receipt["formal_credit"] == 0
         and receipt["manifest_authorized"] is False
         and receipt["source_W_transition_authorized"] is False,
         "seal receipt contract")
    root_entries = parse_manifest(root_manifest_path)
    need(len(root_entries) == 2, "root manifest count")
    root_map = {path: claim for claim, path in root_entries}
    need(root_map == {
        payload_manifest_path: file_sha(payload_manifest_path),
        receipt_path: file_sha(receipt_path),
    }, "root manifest exact")
    payload_entries = parse_manifest(payload_manifest_path)
    need(len(payload_entries) == receipt["payload_manifest"]["entry_count"],
         "payload entry count")
    all_members = [path for _, path in payload_entries]
    pre_hashes = {path: file_sha(path) for path in all_members}
    pre_stats = {path: snapshot(path) for path in all_members}
    for claim, path in payload_entries:
        need(pre_hashes[path] == claim, "payload member hash:" + path.name)

    candidates = sorted(path for path in all_members
                        if path.name == "T04_DOUBLE_GRAPHS_candidate_ownership.jsonl.gz")
    absences = sorted(path for path in all_members
                      if path.name == "T04_DOUBLE_GRAPHS_terminal_absence_authority.jsonl.gz")
    proofs = sorted(path for path in all_members
                    if path.name == "T04_DOUBLE_GRAPHS_materialized_physical_proof_join.jsonl.gz")
    adapter_receipts = sorted(path for path in all_members
                              if path.name == "adapter_receipt.json")
    need(len(candidates) == len(absences) == len(proofs) == len(adapter_receipts) == 2,
         "dual adapter members")
    for paths in (candidates, absences, proofs, adapter_receipts):
        need(file_sha(paths[0]) == file_sha(paths[1]),
             "dual byte identity:" + paths[0].name)
    adapter_receipt = document(adapter_receipts[0], "receipt_sha256")
    need(adapter_receipt["exact_census"]["physical_proof_rows"] == 0
         and adapter_receipt["common_v2_contract"]
             ["common_physical_proof_join_is_empty"] is True,
         "adapter empty proof contract")

    candidate_stream = rows(candidates[0])
    absence_stream = rows(absences[0])
    previous: str | None = None
    census: Counter[str] = Counter()
    count = 0
    candidate_sequence = hashlib.sha256()
    absence_sequence = hashlib.sha256()
    for ordinal in range(1_362_088):
        candidate = next_required(candidate_stream, "candidate", ordinal)
        absence = next_required(absence_stream, "absence", ordinal)
        key = candidate["candidate_key"]
        need(previous is None or previous < key, "strict candidate key order")
        previous = key
        need(candidate["ordinal"] == ordinal
             and candidate["candidate_pair_key_or_null"] == key
             and candidate["terminal"] == "DOUBLE_GRAPHS"
             and candidate["terminal_ordinal"] == 4
             and candidate["authority_slot"] == "T04_DOUBLE_GRAPHS"
             and candidate["primitive_authority_row_sha256"] == absence["row_sha256"]
             and candidate["component_relation_disposition"] == DISPOSITION
             and candidate["physical_proof_row_count"] == 0
             and candidate["physical_proof_row_sequence_sha256"] == EMPTY
             and candidate["formal_credit"] == 0, "candidate cold contract")
        need(absence["ordinal"] == ordinal and absence["candidate_key"] == key
             and absence["terminal"] == "DOUBLE_GRAPHS"
             and absence["terminal_ordinal"] == 4
             and absence["authority_slot"] == "T04_DOUBLE_GRAPHS"
             and absence["native_bucket"] in EXPECTED
             and type(absence["exact_physical_absence_evidence"]) is dict
             and bool(absence["exact_physical_absence_evidence"])
             and absence["resolved"] is True and absence["unresolved"] is False
             and absence["legal_cross_component_same_physical_point_witness"] is False
             and absence["component_relation_disposition"] == DISPOSITION
             and absence["formal_credit"] == 0, "absence cold contract")
        census[absence["native_bucket"]] += 1
        candidate_sequence.update(candidate["row_sha256"].encode("ascii") + b"\n")
        absence_sequence.update(absence["row_sha256"].encode("ascii") + b"\n")
        count += 1
    no_extra(candidate_stream, "candidate")
    no_extra(absence_stream, "absence")
    no_extra(rows(proofs[0]), "physical proof")
    need(count == 1_362_088 and dict(census) == EXPECTED, "cold exact census")
    cd = adapter_receipt["candidate_ownership_ledger"]
    ad = adapter_receipt["terminal_absence_authority_ledger"]
    pd = adapter_receipt["materialized_physical_proof_join_ledger"]
    need(cd["row_count"] == count
         and cd["row_sequence_sha256"] == candidate_sequence.hexdigest()
         and ad["row_count"] == count
         and ad["row_sequence_sha256"] == absence_sequence.hexdigest()
         and pd["row_count"] == 0 and pd["row_sequence_sha256"] == EMPTY,
         "cold descriptor replay")

    post_hashes = {path: file_sha(path) for path in all_members}
    post_stats = {path: snapshot(path) for path in all_members}
    need(pre_hashes == post_hashes, "pre/post payload hashes")
    need(pre_stats == post_stats, "pre/post payload stats")
    output.mkdir(parents=True)
    body = {
        "schema": (
            "cm2.c27-independent.t04-double-graphs.common-v2-correction-"
            "postpublication-cold-terminal-replay-receipt.v2"),
        "status": (
            "PASS_COLD_MANIFEST_FIRST_1362088_CANDIDATES_1362088_ABSENCE_"
            "AUTHORITIES_ZERO_PHYSICAL_PROOFS__ZERO_CREDIT"),
        "manifest_first_terminal_replay": True,
        "base_receipt_file_sha256": file_sha(receipt_path),
        "base_receipt_sha256": receipt["receipt_sha256"],
        "payload_manifest_file_sha256": file_sha(payload_manifest_path),
        "root_manifest_file_sha256": file_sha(root_manifest_path),
        "candidate_pairs": 1_362_088,
        "unique_strictly_ordered_candidate_keys": 1_362_088,
        "terminal_absence_authority_rows": 1_362_088,
        "materialized_physical_proof_rows": 0,
        "bucket_census": EXPECTED,
        "component_relation_disposition": DISPOSITION,
        "unresolved": 0,
        "legal_cross_component_witnesses": 0,
        "component_edges": 0,
        "dual_seed_files_byte_identical": True,
        "pre_post_sha256_identical": True,
        "pre_post_stat_identical": True,
        "numeric_exit": 0,
        "signal": None,
        "stderr_empty": True,
        "formal_credit": 0,
        "manifest_authorized": False,
        "source_W_transition_authorized": False,
    }
    replay = {**body, "receipt_sha256": digest(body)}
    replay_path = output / "terminal_replay.json"
    write_new(replay_path, enc(replay) + b"\n")
    manifest_path = output / "terminal_manifest.sha256"
    manifest_members = [receipt_path, payload_manifest_path,
                        root_manifest_path, Path(__file__).resolve(), replay_path]
    lines = [file_sha(path) + "  " + str(path.relative_to(ROOT))
             for path in sorted(manifest_members)]
    write_new(manifest_path, ("\n".join(lines) + "\n").encode("ascii"))
    print(enc({
        "status": replay["status"],
        "terminal_replay_file_sha256": file_sha(replay_path),
        "terminal_replay_sha256": replay["receipt_sha256"],
        "terminal_manifest_sha256": file_sha(manifest_path),
    }).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Reject as exc:
        print("T04_COMMON_V2_CORRECTION_COLD_REPLAY_REJECT:" + str(exc))
        raise SystemExit(2)
