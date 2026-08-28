#!/usr/bin/env python3
"""Manifest-first cold replay of the native/common-v2 T11--T19 seal."""

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
RECEIPT_FILE = "3a697d2e1e18aee57c3fed205193cf2b84fb9f305817544bf070e9741a8ac293"
RECEIPT_OBJECT = "c863e83dfec699e6f13408ca004b66ab32e9770f8c7e6acb9a49e41fa5eaeb46"
PAYLOAD_FILE = "556eb98ba3a677f60f5d343027bfdeb9876b276cc974b82cf1ad7dfac5acbf98"
ROOT_FILE = "89d5c35b291c02aeb4176b5b6cd1d3f7c0fb5572949d9e87bb3504e88f03961a"


class Reject(RuntimeError): pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value: raise Reject(label)


def enc(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def dig(value: Any) -> str: return hashlib.sha256(enc(value)).hexdigest()


def fsha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(8 << 20): state.update(block)
    return state.hexdigest()


def fp(path: Path) -> list[int]:
    info = os.lstat(path)
    need(stat.S_ISREG(info.st_mode) and not path.is_symlink(), "regular file")
    return [info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns,
            info.st_ctime_ns, info.st_mode, info.st_uid, info.st_gid,
            info.st_nlink]


def manifest(path: Path) -> list[tuple[str, str]]:
    rows = []; previous = None
    for ordinal, line in enumerate(path.read_text("ascii").splitlines()):
        pieces = line.split("  ", 1)
        need(len(pieces) == 2 and len(pieces[0]) == 64, f"manifest:{ordinal}")
        need(previous is None or previous < line, f"manifest order:{ordinal}")
        previous = line; rows.append((pieces[0], pieces[1]))
    return rows


def root_path(relative: str) -> Path:
    path = (ROOT / relative).resolve()
    need(path != ROOT and ROOT in path.parents, "inside workspace")
    return path


def replay_rows(path: Path, descriptor: dict[str, Any],
                sequence_mode: str) -> list[dict[str, Any]]:
    need(fsha(path) == descriptor["file_sha256"], "ledger file hash")
    rows = []
    with gzip.open(path, "rb") as stream:
        for ordinal, line in enumerate(stream):
            need(line.endswith(b"\n"), "newline")
            payload = line[:-1]; row = json.loads(payload)
            need(enc(row) == payload and row["ordinal"] == ordinal, "canonical/ordinal")
            body = dict(row); claim = body.pop("row_sha256", None)
            need(type(claim) is str and claim == dig(body), "row closure")
            rows.append(row)
    need(len(rows) == descriptor["row_count"], "row count")
    shas = [row["row_sha256"] for row in rows]
    if sequence_mode == "newline":
        state = hashlib.sha256()
        for value in shas: state.update(value.encode("ascii") + b"\n")
        observed = state.hexdigest()
    else:
        observed = dig(shas)
    need(observed == descriptor["row_sequence_sha256"], "row sequence")
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seal-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    try:
        seal = Path(args.seal_dir).resolve(); output = Path(args.output_dir).resolve()
        need(not output.exists(), "fresh output")
        receipt_path = seal / "receipt.json"
        payload_path = seal / "payload_manifest.sha256"
        root_manifest = seal / "root_manifest.sha256"
        need(fsha(root_manifest) == ROOT_FILE, "root pin")
        need(manifest(root_manifest) == sorted([
            (PAYLOAD_FILE, str(payload_path.relative_to(ROOT))),
            (RECEIPT_FILE, str(receipt_path.relative_to(ROOT)))],
            key=lambda row: f"{row[0]}  {row[1]}"), "exact root")
        need(fsha(payload_path) == PAYLOAD_FILE and fsha(receipt_path) == RECEIPT_FILE,
             "root members")
        payload_rows = manifest(payload_path); pre = {}
        for pin, relative in payload_rows:
            path = root_path(relative); need(fsha(path) == pin, "payload:" + relative)
            pre[relative] = {"sha256": pin, "stat": fp(path)}
        receipt = json.loads(receipt_path.read_bytes())
        body = dict(receipt); claim = body.pop("receipt_sha256", None)
        need(claim == RECEIPT_OBJECT == dig(body), "receipt closure")
        need(receipt["candidate_total"] == 4
             and receipt["materialized_physical_proof_join_total"] == 0
             and receipt["auxiliary_authority_row_total"] == 328
             and receipt["coherent_resigned_attacks"]
                == {"native": 24, "common_v2": 24, "total": 48, "all_rejected": True}
             and receipt["formal_credit"] == 0
             and receipt["manifest_authorized"] is False
             and receipt["source_W_transition_authorized"] is False
             and receipt["global_atom_and_full_twenty_family_totality_closed"] is False,
             "receipt governance")
        need(receipt["payload_manifest"]["file_sha256"] == PAYLOAD_FILE
             and receipt["payload_manifest"]["entry_count"] == len(payload_rows),
             "payload binding")

        common_relatives = [relative for pin, relative in payload_rows
                            if relative.endswith("/result.json")
                            and pin == receipt["evidence"]["common_result_file_sha256"]]
        native_relatives = [relative for pin, relative in payload_rows
                            if relative.endswith("/result.json")
                            and pin == receipt["evidence"]["native_result_file_sha256"]]
        need(len(common_relatives) == len(native_relatives) == 2, "dual result discovery")
        common_pairs: dict[tuple[str, str], list[bytes]] = {}
        common_candidate_rows = common_proof_rows = common_ledger_count = 0
        common_result_bytes = []
        for relative in common_relatives:
            path = root_path(relative); common_result_bytes.append(path.read_bytes())
            result = json.loads(path.read_bytes()); body = dict(result)
            claim = body.pop("result_sha256", None)
            need(claim == receipt["evidence"]["common_result_object_sha256"] == dig(body),
                 "common result closure")
            for entry in result["adapter_entries"]:
                for key in ("candidate_ownership_ledger",
                            "materialized_physical_proof_join_ledger"):
                    ledger = path.parent / entry[key]["path"]
                    rows = replay_rows(ledger, entry[key], "newline")
                    if key == "candidate_ownership_ledger": common_candidate_rows += len(rows)
                    else: common_proof_rows += len(rows)
                    common_ledger_count += 1
                    common_pairs.setdefault((entry["authority_slot"], key), []).append(ledger.read_bytes())
        need(common_result_bytes[0] == common_result_bytes[1]
             and all(len(values) == 2 and values[0] == values[1]
                     for values in common_pairs.values()), "common dual identity")
        need(common_ledger_count == 36 and common_candidate_rows == 8
             and common_proof_rows == 0, "common cold census")

        native_pairs: dict[str, list[bytes]] = {}; native_result_bytes = []
        native_counts = {"candidate": 0, "auxiliary": 0, "slot": 0}
        filenames = {"t11_t19_atlas_seam_candidate_ownership.jsonl.gz": "candidate",
                     "t11_t18_auxiliary_proof_rows.jsonl.gz": "auxiliary",
                     "t11_t19_slot_authority.jsonl.gz": "slot"}
        for relative in native_relatives:
            path = root_path(relative); native_result_bytes.append(path.read_bytes())
            result = json.loads(path.read_bytes()); body = dict(result)
            claim = body.pop("result_sha256", None)
            need(claim == receipt["evidence"]["native_result_object_sha256"] == dig(body),
                 "native result closure")
            for filename, label in filenames.items():
                ledger = path.parent / filename
                rows = replay_rows(ledger, result["ledgers"][filename], "json-list")
                native_counts[label] += len(rows)
                native_pairs.setdefault(filename, []).append(ledger.read_bytes())
        need(native_result_bytes[0] == native_result_bytes[1]
             and all(len(values) == 2 and values[0] == values[1]
                     for values in native_pairs.values()), "native dual identity")
        need(native_counts == {"candidate": 8, "auxiliary": 104, "slot": 18},
             "native cold census")
        for pin, relative in payload_rows:
            path = root_path(relative)
            need({"sha256": fsha(path), "stat": fp(path)} == pre[relative],
                 "pre/post identity:" + relative)
        output.mkdir(parents=True)
        replay_body = {
            "schema": "cm2.c27-independent.t11-t19.common-v2.postpublication-cold-terminal-replay.v1",
            "status": "PASS_MANIFEST_FIRST_NATIVE_AND_COMMON_T11_T19_COLD_REPLAY__42_LEDGERS__PRE_POST_SHA_STAT_IDENTICAL__ZERO_CREDIT",
            "base_receipt_file_sha256": RECEIPT_FILE,
            "base_receipt_sha256": RECEIPT_OBJECT,
            "payload_manifest_file_sha256": PAYLOAD_FILE,
            "root_manifest_file_sha256": ROOT_FILE,
            "payload_entry_count": len(payload_rows),
            "common_replayed_ledgers": common_ledger_count,
            "common_dual_seed_candidate_rows": common_candidate_rows,
            "common_dual_seed_physical_proof_rows": common_proof_rows,
            "native_replayed_ledgers": 6,
            "native_dual_seed_row_census": native_counts,
            "manifest_first_terminal_replay": True,
            "pre_post_sha256_identical": True, "pre_post_stat_identical": True,
            "numeric_exit": 0, "signal": None, "stderr_empty": True,
            "formal_credit": 0, "manifest_authorized": False,
            "source_W_transition_authorized": False,
            "global_atom_and_full_twenty_family_totality_closed": False,
            "C27_C28_C29": "REJECT_PENDING_COMPLETE_PRIMITIVE_TWENTY_TERMINAL_GATE",
            "CM2": "NO-GO_FOR_CLAIM", "replay_source_sha256": fsha(Path(__file__).resolve())}
        replay = {**replay_body, "replay_sha256": dig(replay_body)}
        replay_path = output / "terminal_replay.json"
        replay_path.write_bytes(enc(replay) + b"\n")
        terminal_manifest = output / "terminal_manifest.sha256"
        members = sorted((payload_path, receipt_path, root_manifest, replay_path),
                         key=lambda path: str(path.relative_to(ROOT)))
        terminal_manifest.write_bytes(b"".join(
            fsha(path).encode() + b"  " + str(path.relative_to(ROOT)).encode() + b"\n"
            for path in members))
    except (Reject, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError) as error:
        print("REJECT:" + str(error)); return 2
    print(enc({"status": replay["status"], "replay_sha256": replay["replay_sha256"],
               "terminal_manifest_file_sha256": fsha(terminal_manifest)}).decode("ascii"))
    return 0


if __name__ == "__main__": raise SystemExit(main())
