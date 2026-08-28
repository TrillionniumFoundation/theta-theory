#!/usr/bin/env python3
"""Cold manifest-first terminal replay for the sealed T04 authority."""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import json
import os
from pathlib import Path
import stat
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
EXPECTED = {"CROSS_CHART_QUOTIENT_RECHART": 1_361_424,
            "SAME_CHART_TRANSVERSE_1D": 448,
            "CROSS_CHART_GRAPH_SIDE_T0": 192,
            "CODIMENSION_TWO_LOWER_OWNER": 24}


class Reject(RuntimeError): pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value: raise Reject(label)


def enc(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str: return hashlib.sha256(enc(value)).hexdigest()


def sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""): state.update(block)
    return state.hexdigest()


def rel(path: Path) -> str: return str(path.resolve().relative_to(ROOT))


def parse_manifest(path: Path) -> dict[str, str]:
    output = {}
    for line in path.read_text("ascii").splitlines():
        pieces = line.split("  ", 1)
        need(len(pieces) == 2 and len(pieces[0]) == 64 and pieces[1] not in output,
             "manifest line")
        output[pieces[1]] = pieces[0]
    return output


def stable(path: Path) -> tuple[int, ...]:
    item = os.lstat(path)
    need(stat.S_ISREG(item.st_mode) and not path.is_symlink(), "regular:" + str(path))
    return (item.st_dev, item.st_ino, item.st_size, item.st_mtime_ns,
            item.st_ctime_ns, item.st_mode, item.st_nlink)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seal-dir", required=True); parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    seal, output = Path(args.seal_dir), Path(args.out_dir)
    need(not output.exists(), "fresh cold replay")
    payload_path, receipt_path, root_path = (seal / "payload_manifest.sha256",
                                             seal / "receipt.json",
                                             seal / "root_manifest.sha256")
    root = parse_manifest(root_path)
    need(root == {rel(payload_path): sha(payload_path), rel(receipt_path): sha(receipt_path)},
         "root manifest closure")
    payload = parse_manifest(payload_path)
    before = {}
    for name, expected in payload.items():
        path = ROOT / name; before[name] = stable(path)
        need(sha(path) == expected, "payload member:" + name)
    receipt = json.loads(receipt_path.read_bytes())
    body = dict(receipt); claim = body.pop("receipt_sha256", None)
    need(claim == digest(body)
         and receipt["terminal"] == "DOUBLE_GRAPHS"
         and receipt["terminal_ordinal"] == 4
         and receipt["authority_slot"] == "T04_DOUBLE_GRAPHS"
         and receipt["pair_contract"]["candidate_pairs"] == 1_362_088
         and receipt["pair_contract"]["unresolved"] == 0
         and receipt["pair_contract"]["legal_cross_component_witnesses"] == 0
         and receipt["formal_credit"] == 0
         and receipt["manifest_authorized"] is False,
         "sealed receipt semantics")
    need(receipt["payload_manifest"]["sha256"] == sha(payload_path)
         and receipt["payload_manifest"]["entry_count"] == len(payload),
         "receipt payload binding")
    ledger_name = next(name for name in payload
                       if name.endswith("seed-30627301/t04_double_graphs_1362088_pair_ownership.jsonl.gz"))
    witness_name = next(name for name in payload
                        if name.endswith("seed-30627301/t04_double_graphs_legal_cross_component_physical_witnesses.jsonl.gz"))
    census: Counter[str] = Counter(); seen: set[bytes] = set(); count = 0
    with gzip.open(ROOT / ledger_name, "rt", encoding="ascii") as stream:
        for line in stream:
            row = json.loads(line); row_body = dict(row); row_claim = row_body.pop("row_sha256", None)
            need(row_claim == digest(row_body), "cold row closure")
            candidate = row["candidate_id"].encode("ascii")
            candidate_digest = hashlib.sha256(candidate).digest()
            need(candidate_digest not in seen, "cold candidate uniqueness")
            seen.add(candidate_digest)
            need(row["pair_owner_count"] == 1 and row["resolved"] is True
                 and row["unresolved"] is False
                 and row["legal_cross_component_same_physical_point_witness"] is False,
                 "cold row disposition")
            census[row["bucket"]] += 1; count += 1
    need(count == 1_362_088 and dict(census) == EXPECTED, "cold exact census")
    with gzip.open(ROOT / witness_name, "rb") as stream:
        need(stream.read(1) == b"", "cold physical witness empty")
    for name in payload:
        path = ROOT / name
        need(stable(path) == before[name] and sha(path) == payload[name],
             "post replay stable:" + name)
    output.mkdir(parents=True)
    terminal_body = {
        "schema": "cm2.c27-independent.t04-double-graphs.postpublication-cold-terminal-replay-receipt.v1",
        "status": "PASS_COLD_MANIFEST_FIRST_1362088_PAIR_UNIQUENESS_ZERO_WITNESS_REPLAY__ZERO_CREDIT",
        "base_receipt_file_sha256": sha(receipt_path),
        "base_receipt_sha256": receipt["receipt_sha256"],
        "payload_manifest_file_sha256": sha(payload_path),
        "root_manifest_file_sha256": sha(root_path),
        "candidate_pairs": count, "bucket_census": dict(census),
        "unique_candidate_ids": len(seen), "unresolved": 0,
        "legal_cross_component_witnesses": 0,
        "manifest_first_terminal_replay": True,
        "pre_post_sha256_identical": True, "pre_post_stat_identical": True,
        "numeric_exit": 0, "signal": None, "stderr_empty": True,
        "formal_credit": 0, "manifest_authorized": False,
        "source_W_transition_authorized": False,
    }
    terminal = {**terminal_body, "receipt_sha256": digest(terminal_body)}
    terminal_path = output / "terminal_replay.json"
    terminal_path.write_bytes(enc(terminal) + b"\n")
    entries = [payload_path, receipt_path, root_path, terminal_path]
    manifest_path = output / "terminal_manifest.sha256"
    manifest_path.write_bytes(b"".join(sha(path).encode("ascii") + b"  "
                                        + rel(path).encode("ascii") + b"\n"
                                        for path in sorted(entries, key=rel)))
    print(enc({"status": terminal["status"], "terminal_file_sha256": sha(terminal_path),
               "terminal_receipt_sha256": terminal["receipt_sha256"],
               "terminal_manifest_sha256": sha(manifest_path)}).decode("ascii"))
    return 0


if __name__ == "__main__":
    try: raise SystemExit(main())
    except Reject as exc:
        print("T04_COLD_REPLAY_REJECT:" + str(exc)); raise SystemExit(2)
