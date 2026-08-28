#!/usr/bin/env python3
"""No-import verifier for the 10,660 attachment candidate ledger."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SQLITE = ROOT / "deliverables/cm2_c27_included_stratum_attachments_sqlite_probe.py"
SQLITE_SHA256 = "a43fdc6f8d028279e142a47633489a9bead62ee64070b6defed38501f247b744"
RECEIPT = ROOT / "deliverables/cm2_c27_included_stratum_attachments_subgate_receipt.json"
RECEIPT_SHA256 = "d66d8aacb517a642684f3ddbe184e270936346726b73fa518c76f29076c184f5"


class Reject(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def encode(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(encode(value)).hexdigest()


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def closed(value: dict[str, Any], key: str, label: str) -> None:
    claim = value.get(key)
    body = dict(value)
    body.pop(key, None)
    need(type(claim) is str and claim == digest(body), label + ":closure")


def verify(result_path: Path, ledger_path: Path, sqlite_seed: int) -> dict[str, Any]:
    need(file_hash(SQLITE) == SQLITE_SHA256, "SQLite source pin")
    need(file_hash(RECEIPT) == RECEIPT_SHA256, "receipt pin")
    result = json.loads(result_path.read_bytes())
    closed(result, "result_sha256", "result")
    need(result["schema"] ==
         "cm2.c27-independent.included-stratum-10660-candidate-materialization.result.v1"
         and result["status"].startswith("PASS_10660_INCLUDED_STRATUM")
         and result["candidate_count"] == 10_660
         and result["excluded_retained_count"] == 276
         and result["candidate_excluded_intersection_count"] == 0
         and result["independent_sqlite_verification_required"] is True
         and result["formal_credit"] == 0
         and result["manifest_authorized"] is False
         and result["source_W_transition_authorized"] is False,
         "result semantics")
    need(file_hash(ledger_path) == result["ledger"]["file_sha256"],
         "ledger file binding")

    identifiers = hashlib.sha256()
    semantic_sequence = hashlib.sha256()
    row_hashes = []
    seen: set[str] = set()
    kind_count: dict[str, int] = {}
    kernel_count: dict[str, int] = {}
    count = 0
    with gzip.open(ledger_path, "rt", encoding="ascii") as handle:
        for ordinal, line in enumerate(handle):
            value = json.loads(line)
            closed(value, "row_sha256", f"row:{ordinal}")
            need(value["schema"] ==
                 "cm2.c27-independent.included-stratum-attachment.materialized-candidate-row.v1"
                 and value["ordinal"] == ordinal
                 and value["terminal"] == "INCLUDED_STRATUM_ATTACHMENTS"
                 and value["terminal_disposition"] ==
                    "UNIQUE_INCLUDED_STRATUM_ATTACHMENT__NOT_RETAINED_CONTINUATION"
                 and value["retained_continuation_candidate"] is False
                 and value["cross_component"] is False
                 and value["formal_credit"] == 0
                 and value["source_W_transition_authorized"] is False,
                 f"row:{ordinal}:governance")
            representation = value["representation_id"]
            need(representation not in seen, f"row:{ordinal}:unique")
            if seen:
                need(representation > previous, f"row:{ordinal}:order")
            seen.add(representation)
            previous = representation
            semantic = {key: value[key] for key in (
                "representation_id", "owner_member_id", "fresh_component_id",
                "base_root_id", "official_key_id", "representation_semantic_kind",
                "semantic_kernel", "owner_normalized_support_ast_sha256",
                "representation_semantic_certificate_sha256",
                "C15_member_row_sha256", "C25_representation_row_sha256",
                "C26_handle_row_sha256", "C20D_source_semantics",
                "C20D_row_sha256", "cross_component", "formal_credit")}
            semantic_sha = digest(semantic)
            need(semantic_sha == value["semantic_body_sha256"],
                 f"row:{ordinal}:semantic closure")
            identifiers.update(representation.encode("ascii") + b"\n")
            semantic_sequence.update(bytes.fromhex(semantic_sha))
            row_hashes.append(value["row_sha256"])
            kind_count[value["representation_semantic_kind"]] = (
                kind_count.get(value["representation_semantic_kind"], 0) + 1)
            kernel_count[value["semantic_kernel"]] = (
                kernel_count.get(value["semantic_kernel"], 0) + 1)
            count += 1
    need(count == len(seen) == result["ledger"]["row_count"] == 10_660,
         "ledger count")
    need(identifiers.hexdigest() == result["candidate_representation_ids_sha256"]
         == "3c18dda4883dcc9a357d898ffa7c0f126b7a1ffde985bc77a879369b2978c511",
         "candidate ID commitment")
    need(semantic_sequence.hexdigest() == result["semantic_body_sequence_sha256"]
         == "a9c47fa8c6321c8f6a14a85a2f52734d1f2667652b2d4d1f1732c1fc00630263",
         "semantic sequence commitment")
    need(digest(row_hashes) == result["ledger"]["row_sequence_sha256"],
         "normalized sequence commitment")
    need(kind_count == {"EXACT_SUBCOVER_INCLUSION_DISPOSITION": 8_416,
                        "TYPED_NONFULL_REPRESENTATION_DISPOSITION": 2_244}
         and kernel_count == {"C20D": 2_244, "C22B": 7_288, "C23B": 1_128},
         "semantic census")

    receipt = json.loads(RECEIPT.read_bytes())
    commitment = receipt["candidate_commitment"]
    need(commitment["candidate_count"] == count
         and commitment["candidate_representation_ids_sha256"]
             == identifiers.hexdigest()
         and commitment["candidate_row_sequence_sha256"]
             == semantic_sequence.hexdigest()
         and commitment["candidate_excluded_intersection_count"] == 0
         and receipt["formal_credit"] == 0,
         "receipt commitment")

    completed = subprocess.run(
        [sys.executable, "-I", "-B", str(SQLITE), "--seed", str(sqlite_seed)],
        cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    need(completed.returncode == 0 and completed.stderr == b"",
         "independent SQLite execution")
    sqlite_result = json.loads(completed.stdout)
    sqlite_universe = sqlite_result["candidate_universe"]
    need(sqlite_result["status"].startswith("PASS_ZERO_CREDIT__10660_INCLUDED")
         and sqlite_result["implementation"] == "ORDER_INDEPENDENT_SQLITE_RELATIONAL_JOIN"
         and sqlite_universe["candidate_count"] == count
         and sqlite_universe["candidate_representation_ids_sha256"]
             == identifiers.hexdigest()
         and sqlite_universe["candidate_row_sequence_sha256"]
             == semantic_sequence.hexdigest()
         and sqlite_universe["candidate_excluded_intersection_count"] == 0
         and sqlite_result["formal_credit"] == 0,
         "independent SQLite agreement")

    body = {
        "schema": "cm2.c27-independent.included-stratum-10660-candidate-materialization.verification.v1",
        "status": "PASS_NO_IMPORT_SQLITE_REBUILD__10660_ROWS_EXACT_COMMITMENT_MATCH__ZERO_CREDIT",
        "materializer_imported_or_executed": False,
        "independent_sqlite_implementation_executed": True,
        "candidate_count": count, "excluded_retained_count": 276,
        "semantic_kind_census": dict(sorted(kind_count.items())),
        "semantic_kernel_census": dict(sorted(kernel_count.items())),
        "candidate_representation_ids_sha256": identifiers.hexdigest(),
        "semantic_body_sequence_sha256": semantic_sequence.hexdigest(),
        "result_file_sha256": file_hash(result_path),
        "ledger_file_sha256": file_hash(ledger_path),
        "sqlite_source_sha256": SQLITE_SHA256,
        "sqlite_result_sha256": sqlite_result["result_sha256"],
        "formal_credit": 0, "manifest_authorized": False,
        "source_W_transition_authorized": False,
    }
    return {**body, "verification_sha256": digest(body)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", required=True)
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--sqlite-seed", type=int, required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        value = verify(Path(args.result), Path(args.ledger), args.sqlite_seed)
        output = Path(args.output)
        need(not output.exists(), "fresh verification output")
        output.write_bytes(encode(value) + b"\n")
    except (Reject, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError) as error:
        print("REJECT:" + str(error))
        return 2
    print(encode({"status": value["status"],
                  "verification_sha256": value["verification_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
