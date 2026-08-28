#!/usr/bin/env python3
"""Manifest-first cold replay of the sealed six-terminal common-v2 adapter."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import stat
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
RECEIPT_FILE_SHA256 = "4fd0ae953336743384967c1f3a05712df5cdcae4076240b75f73863829ea9598"
RECEIPT_OBJECT_SHA256 = "e95bdbf3cd14a541f5b9f29b6c3c5c8b2907175b90c7313978bcd5a46967ba17"
PAYLOAD_MANIFEST_SHA256 = "bfadad9849859ce925473bd08f12e815ec716e5a053e9698acc1dea1b4591506"
ROOT_MANIFEST_SHA256 = "c0d05a3230898a3fa69d1468678d7133def6dfeb3eab3aaf9d362e68aeff0444"
CANDIDATE_SCHEMA = "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.candidate-ownership.row.v2"
PROOF_SCHEMA = "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.materialized-physical-proof-join.row.v2"


class Reject(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def enc(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def dig(value: Any) -> str:
    return hashlib.sha256(enc(value)).hexdigest()


def fsha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(8 << 20):
            state.update(block)
    return state.hexdigest()


def fingerprint(path: Path) -> list[int]:
    info = os.lstat(path)
    need(stat.S_ISREG(info.st_mode) and not path.is_symlink(),
         "regular non-symlink:" + str(path))
    return [info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns,
            info.st_ctime_ns, info.st_mode, info.st_uid, info.st_gid,
            info.st_nlink]


def workspace_path(relative: str) -> Path:
    path = (ROOT / relative).resolve()
    need(path != ROOT and ROOT in path.parents, "payload inside workspace")
    return path


def manifest(path: Path) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    previous = None
    for ordinal, line in enumerate(path.read_text("ascii").splitlines()):
        pieces = line.split("  ", 1)
        need(len(pieces) == 2 and len(pieces[0]) == 64,
             f"manifest wire:{ordinal}")
        need(previous is None or previous < line, f"manifest order:{ordinal}")
        previous = line
        rows.append((pieces[0], pieces[1]))
    return rows


def sequence(rows: list[dict[str, Any]]) -> str:
    state = hashlib.sha256()
    for row in rows:
        state.update(row["row_sha256"].encode("ascii") + b"\n")
    return state.hexdigest()


def replay_ledger(path: Path, descriptor: dict[str, Any], schema: str) -> int:
    need(fsha(path) == descriptor["file_sha256"]
         and path.stat().st_size == descriptor["file_size"],
         "ledger file descriptor:" + str(path))
    rows = []
    previous = None
    with gzip.open(path, "rb") as stream:
        for ordinal, line in enumerate(stream):
            need(line.endswith(b"\n"), "ledger newline")
            payload = line[:-1]
            row = json.loads(payload)
            need(enc(row) == payload and row["schema"] == schema
                 and row["ordinal"] == ordinal, "ledger wire")
            body = dict(row)
            claim = body.pop("row_sha256", None)
            need(type(claim) is str and claim == dig(body), "ledger closure")
            key = row["candidate_key"]
            if schema == CANDIDATE_SCHEMA:
                need(previous is None or previous < key, "candidate ordering")
            else:
                need(previous is None or previous <= key, "proof candidate ordering")
            previous = key
            rows.append(row)
    need(len(rows) == descriptor["row_count"]
         and sequence(rows) == descriptor["row_sequence_sha256"],
         "ledger count/sequence")
    return len(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seal-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    try:
        seal = Path(args.seal_dir).resolve()
        output = Path(args.output_dir).resolve()
        need(not output.exists(), "fresh output")
        receipt_path = seal / "receipt.json"
        payload_path = seal / "payload_manifest.sha256"
        root_path = seal / "root_manifest.sha256"

        # Manifest-first: the pinned root is the only initially trusted byte set.
        need(fsha(root_path) == ROOT_MANIFEST_SHA256, "root pin")
        root_rows = manifest(root_path)
        need(root_rows == sorted([
            (PAYLOAD_MANIFEST_SHA256, str(payload_path.relative_to(ROOT))),
            (RECEIPT_FILE_SHA256, str(receipt_path.relative_to(ROOT))),
        ], key=lambda row: f"{row[0]}  {row[1]}"), "exact root manifest")
        need(fsha(payload_path) == PAYLOAD_MANIFEST_SHA256
             and fsha(receipt_path) == RECEIPT_FILE_SHA256,
             "root members")

        payload_rows = manifest(payload_path)
        pre: dict[str, dict[str, Any]] = {}
        for pin, relative in payload_rows:
            path = workspace_path(relative)
            need(fsha(path) == pin, "payload pin:" + relative)
            pre[relative] = {"sha256": pin, "stat": fingerprint(path)}

        receipt = json.loads(receipt_path.read_bytes())
        receipt_body = dict(receipt)
        receipt_claim = receipt_body.pop("receipt_sha256", None)
        need(receipt_claim == RECEIPT_OBJECT_SHA256 == dig(receipt_body),
             "receipt closure")
        need(receipt["candidate_total"] == 52_064
             and receipt["materialized_physical_proof_join_total"] == 216
             and receipt["physical_component_edge_count"] == 88
             and receipt["coherent_resigned_attacks_rejected"] == 24
             and receipt["dual_seed_result_and_twelve_ledgers_byte_identical"] is True
             and receipt["formal_credit"] == 0
             and receipt["manifest_authorized"] is False
             and receipt["source_W_transition_authorized"] is False
             and receipt["global_atom_and_full_twenty_family_totality_closed"] is False,
             "receipt governance")
        need(receipt["payload_manifest"]["file_sha256"] == PAYLOAD_MANIFEST_SHA256
             and receipt["payload_manifest"]["entry_count"] == len(payload_rows),
             "receipt payload binding")

        result_relatives = [relative for pin, relative in payload_rows
                            if relative.endswith("/result.json")
                            and pin == receipt["evidence"]["result_file_sha256"]]
        need(len(result_relatives) == 2, "dual result discovery")
        candidate_rows = proof_rows = ledger_count = 0
        result_bytes = []
        ledger_bytes_by_slot: dict[tuple[str, str], list[bytes]] = {}
        for relative in result_relatives:
            result_path = workspace_path(relative)
            result = json.loads(result_path.read_bytes())
            body = dict(result)
            claim = body.pop("result_sha256", None)
            need(claim == receipt["evidence"]["result_object_sha256"] == dig(body),
                 "result closure")
            result_bytes.append(result_path.read_bytes())
            directory = result_path.parent
            for entry in result["adapter_entries"]:
                slot = entry["authority_slot"]
                for key, schema in (("candidate_ownership_ledger", CANDIDATE_SCHEMA),
                                    ("materialized_physical_proof_join_ledger", PROOF_SCHEMA)):
                    path = directory / entry[key]["path"]
                    count = replay_ledger(path, entry[key], schema)
                    if key == "candidate_ownership_ledger":
                        candidate_rows += count
                    else:
                        proof_rows += count
                    ledger_count += 1
                    ledger_bytes_by_slot.setdefault((slot, key), []).append(path.read_bytes())
        need(result_bytes[0] == result_bytes[1]
             and all(len(values) == 2 and values[0] == values[1]
                     for values in ledger_bytes_by_slot.values()),
             "cold dual-seed byte identity")
        need(ledger_count == 24 and candidate_rows == 104_128
             and proof_rows == 432, "cold dual-seed census")

        post: dict[str, dict[str, Any]] = {}
        for pin, relative in payload_rows:
            path = workspace_path(relative)
            post[relative] = {"sha256": fsha(path), "stat": fingerprint(path)}
            need(post[relative] == pre[relative], "pre/post identity:" + relative)

        output.mkdir(parents=True)
        replay_body = {
            "schema": "cm2.c27-independent.legacy-terminal.common-v2-adapter.postpublication-cold-terminal-replay.v1",
            "status": "PASS_MANIFEST_FIRST_COLD_ROOT_PAYLOAD_24_LEDGER_REPLAY__DUAL_SEED_104128_CANDIDATES_432_PROOFS__PRE_POST_SHA_STAT_IDENTICAL__ZERO_CREDIT",
            "base_receipt_file_sha256": RECEIPT_FILE_SHA256,
            "base_receipt_sha256": RECEIPT_OBJECT_SHA256,
            "payload_manifest_file_sha256": PAYLOAD_MANIFEST_SHA256,
            "root_manifest_file_sha256": ROOT_MANIFEST_SHA256,
            "payload_entry_count": len(payload_rows),
            "replayed_ledger_count": ledger_count,
            "dual_seed_candidate_rows_replayed": candidate_rows,
            "dual_seed_physical_proof_rows_replayed": proof_rows,
            "manifest_first_terminal_replay": True,
            "pre_post_sha256_identical": True,
            "pre_post_stat_identical": True,
            "numeric_exit": 0,
            "signal": None,
            "stderr_empty": True,
            "formal_credit": 0,
            "manifest_authorized": False,
            "source_W_transition_authorized": False,
            "global_atom_and_full_twenty_family_totality_closed": False,
            "C27_C28_C29": "REJECT_PENDING_COMPLETE_PRIMITIVE_TWENTY_TERMINAL_GATE",
            "CM2": "NO-GO_FOR_CLAIM",
            "replay_source_sha256": fsha(Path(__file__).resolve()),
        }
        replay = {**replay_body, "replay_sha256": dig(replay_body)}
        replay_path = output / "terminal_replay.json"
        replay_path.write_bytes(enc(replay) + b"\n")
        terminal_manifest = output / "terminal_manifest.sha256"
        members = sorted((payload_path, receipt_path, root_path, replay_path),
                         key=lambda path: str(path.relative_to(ROOT)))
        terminal_manifest.write_bytes(b"".join(
            fsha(path).encode("ascii") + b"  "
            + str(path.relative_to(ROOT)).encode("ascii") + b"\n"
            for path in members))
    except (Reject, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError) as error:
        print("REJECT:" + str(error))
        return 2
    print(enc({"status": replay["status"],
               "replay_sha256": replay["replay_sha256"],
               "terminal_manifest_file_sha256": fsha(terminal_manifest)}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
