#!/usr/bin/env python3
"""Cold terminal replay for the corrected T07/T08/T09 v2 zero-credit seal."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
RECEIPT_PIN = "6a9c5c28863948f2fb5c122b7d7139db6e774d328064e0c91d3c7a7172d17a1b"
RECEIPT_OBJECT = "22c439ea471d76b0efd4368a3408bd67e3bb8e207cb4b47443b065e26a48a777"
PAYLOAD_PIN = "6ec39202dd8d0eddc1d867c6172f788b64f1d120722b587e95013887022c78a4"
ROOT_PIN = "5ff8f8eaa02f96532802c35f1d14135908659185e56d7074a63536e46a91cca2"


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
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def stat_wire(path: Path) -> list[int]:
    info = path.stat()
    return [info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns,
            info.st_ctime_ns, info.st_mode, info.st_uid, info.st_gid]


def root_path(relative: str) -> Path:
    path = (ROOT / relative).resolve()
    need(ROOT in path.parents, "payload path inside workspace")
    return path


def parse_manifest(path: Path) -> list[tuple[str, str]]:
    rows = []
    previous = None
    for ordinal, line in enumerate(path.read_text("ascii").splitlines()):
        pieces = line.split("  ", 1)
        need(len(pieces) == 2 and len(pieces[0]) == 64,
             f"manifest row:{ordinal}")
        need(previous is None or previous < line, "manifest strict ordering")
        previous = line
        rows.append((pieces[0], pieces[1]))
    return rows


def verify_descriptor(desc: dict[str, Any]) -> dict[str, Any]:
    path = root_path(desc["path"])
    need(path.is_file() and path.stat().st_size == desc["size"]
         and fsha(path) == desc["sha256"], "descriptor file:" + path.name)
    count = 0
    sequence = hashlib.sha256()
    previous = None
    with gzip.open(path, "rb") as stream:
        for line in stream:
            need(line.endswith(b"\n"), "ledger newline:" + path.name)
            payload = line[:-1]
            row = json.loads(payload)
            need(canonical(row) == payload and row["schema"] == desc["row_schema"],
                 "ledger canonical/schema:" + path.name)
            body = dict(row)
            claim = body.pop("row_sha256", None)
            need(type(claim) is str and claim == digest(body),
                 "ledger closure:" + path.name)
            if desc["ordering"] == ["candidate_key"]:
                key = row["candidate_key"]
                need(previous is None or previous < key,
                     "candidate ordering:" + path.name)
                previous = key
            elif desc["ordering"] == ["primitive_support_atom_key"]:
                key = row["primitive_support_atom_key"]
                need(previous is None or previous < key,
                     "atom ordering:" + path.name)
                previous = key
            elif desc["ordering"] == ["primitive_support_atom_key",
                                      "candidate_pair_key"]:
                key = (row["primitive_support_atom_key"],
                       row["candidate_pair_key"])
                need(previous is None or previous < key,
                     "incidence ordering:" + path.name)
                previous = key
            sequence.update(claim.encode("ascii") + b"\n")
            count += 1
    need(count == desc["row_count"]
         and sequence.hexdigest() == desc["row_sequence_sha256"],
         "descriptor row census/sequence:" + path.name)
    return {"path": desc["path"], "rows": count, "sha256": desc["sha256"]}


def replay(seal: Path) -> dict[str, Any]:
    receipt_path = seal / "receipt.json"
    payload_path = seal / "payload_manifest.sha256"
    root_manifest = seal / "root_manifest.sha256"
    need(fsha(receipt_path) == RECEIPT_PIN
         and fsha(payload_path) == PAYLOAD_PIN
         and fsha(root_manifest) == ROOT_PIN, "seal file pins")
    receipt = json.loads(receipt_path.read_bytes())
    body = dict(receipt)
    claim = body.pop("receipt_sha256", None)
    need(claim == RECEIPT_OBJECT == digest(body), "receipt closure")
    need(receipt["formal_credit"] == 0
         and receipt["manifest_authorized"] is False
         and receipt["dual_seed"]["all_ledgers_byte_identical"] is True
         and receipt["dual_seed"]["ledger_pair_count"] == 8
         and receipt["coherent_attacks"]["attacks"]
            == receipt["coherent_attacks"]["rejected"] == 22,
         "receipt governance")
    exact = receipt["exact_census"]
    need(exact["candidate_pair_count"] == 101_080
         and exact["atom_pair_incidence_count"] == 206_632
         and exact["full_atom_rows"] == 483_232
         and exact["incident_atoms"] == 62_768
         and exact["exact_complement_atoms"] == 420_464
         and exact["multi_terminal_atoms"] == 3_896
         and exact["physical_proof_row_count"] == 32_608
         and exact["unique_component_edges"] == 14_724,
         "receipt exact census")
    payload_rows = parse_manifest(payload_path)
    need(len(payload_rows) == receipt["payload_manifest"]["entry_count"]
         and receipt["payload_manifest"]["file_sha256"] == PAYLOAD_PIN,
         "payload manifest receipt binding")
    root_expected = "".join(sorted((
        f"{PAYLOAD_PIN}  {payload_path.relative_to(ROOT)}\n",
        f"{RECEIPT_PIN}  {receipt_path.relative_to(ROOT)}\n",
    ))).encode("ascii")
    need(root_manifest.read_bytes() == root_expected, "exact root manifest")
    pre = {}
    for pin, relative in payload_rows:
        path = root_path(relative)
        need(path.is_file() and fsha(path) == pin, "payload member:" + relative)
        pre[relative] = {"sha256": pin, "stat": stat_wire(path)}
    verified = []
    for entry in receipt["terminal_adapters"]:
        verified.append(verify_descriptor(entry["candidate_ownership_ledger"]))
        verified.append(verify_descriptor(
            entry["materialized_physical_proof_fragment_ledger"]))
    verified.append(verify_descriptor(receipt["atom_pair_incidence_ledger"]))
    verified.append(verify_descriptor(receipt["atom_incidence_disposition_ledger"]))
    need(len(verified) == 8, "eight ledger replay")
    post = {}
    for pin, relative in payload_rows:
        path = root_path(relative)
        post[relative] = {"sha256": fsha(path), "stat": stat_wire(path)}
        need(post[relative] == pre[relative], "pre/post identity:" + relative)
    stable = {"payload_entry_count": len(payload_rows),
              "replayed_ledger_count": len(verified),
              "replayed_row_count": sum(item["rows"] for item in verified),
              "pre_post_sha256_identical": True,
              "pre_post_stat_identical": True}
    result_body = {
        "schema": "cm2.c27-independent.primitive-v5-actual-three-terminal-pair-atom-adapters-v2-terminal-replay.v1",
        "status": "PASS_COLD_ROOT_PAYLOAD_AND_EIGHT_LEDGER_REPLAY__PRE_POST_IDENTICAL__ZERO_CREDIT",
        "receipt_file_sha256": RECEIPT_PIN,
        "receipt_sha256": RECEIPT_OBJECT,
        "payload_manifest_file_sha256": PAYLOAD_PIN,
        "root_manifest_file_sha256": ROOT_PIN,
        "exact_census": stable, "verified_ledgers": verified,
        "formal_credit": 0, "manifest_authorized": False,
        "C27_C28_C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM",
        "replay_source_sha256": fsha(Path(__file__).resolve()),
    }
    result = dict(result_body)
    result["result_sha256"] = digest(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seal-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = Path(args.output).resolve()
    try:
        need(not output.exists(), "fresh replay output")
        result = replay(Path(args.seal_dir).resolve())
        output.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                     | getattr(os, "O_NOFOLLOW", 0), 0o600)
        try:
            os.write(fd, canonical(result) + b"\n")
            os.fsync(fd)
        finally:
            os.close(fd)
    except (Failure, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError) as error:
        print("FAIL:" + str(error))
        return 2
    print(canonical({"status": result["status"],
                     "exact_census": result["exact_census"],
                     "result_sha256": result["result_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
