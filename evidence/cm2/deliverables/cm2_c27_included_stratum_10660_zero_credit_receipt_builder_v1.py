#!/usr/bin/env python3
"""Mint a fail-closed, zero-credit receipt for the 10,660 row authority."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
MATERIALIZER = ROOT / "deliverables/cm2_c27_included_stratum_10660_candidate_materializer_v1.py"
VERIFIER = ROOT / "deliverables/cm2_c27_included_stratum_10660_independent_verifier_v1.py"
ATTACKER = ROOT / "deliverables/cm2_c27_included_stratum_10660_attack_harness_v1.py"
ORIGINAL = ROOT / "deliverables/cm2_c27_included_stratum_attachments_subgate_receipt.json"


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
    body = dict(value); body.pop(key, None)
    need(type(claim) is str and claim == digest(body), label + ":closure")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-a", required=True)
    parser.add_argument("--seed-b", required=True)
    parser.add_argument("--verification-a", required=True)
    parser.add_argument("--verification-b", required=True)
    parser.add_argument("--attacks", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        dirs = [Path(args.seed_a), Path(args.seed_b)]
        results = [path / "result.json" for path in dirs]
        ledgers = [path / "included_stratum_10660_materialized_candidates.jsonl.gz"
                   for path in dirs]
        need(all(path.is_file() for path in results + ledgers), "seed artifacts")
        result_values = [json.loads(path.read_bytes()) for path in results]
        for index, value in enumerate(result_values):
            closed(value, "result_sha256", f"result:{index}")
            need(value["candidate_count"] == 10_660
                 and value["excluded_retained_count"] == 276
                 and value["candidate_excluded_intersection_count"] == 0
                 and value["formal_credit"] == 0
                 and value["manifest_authorized"] is False
                 and value["source_W_transition_authorized"] is False,
                 f"result:{index}:semantics")
            need(file_hash(ledgers[index]) == value["ledger"]["file_sha256"],
                 f"result:{index}:ledger")
        need(results[0].read_bytes() == results[1].read_bytes()
             and ledgers[0].read_bytes() == ledgers[1].read_bytes(),
             "dual seed byte identity")

        verification_paths = [Path(args.verification_a), Path(args.verification_b)]
        verifications = [json.loads(path.read_bytes()) for path in verification_paths]
        for index, value in enumerate(verifications):
            closed(value, "verification_sha256", f"verification:{index}")
            need(value["status"].startswith("PASS_NO_IMPORT_SQLITE_REBUILD")
                 and value["materializer_imported_or_executed"] is False
                 and value["independent_sqlite_implementation_executed"] is True
                 and value["candidate_count"] == 10_660
                 and value["formal_credit"] == 0
                 and value["manifest_authorized"] is False
                 and value["source_W_transition_authorized"] is False,
                 f"verification:{index}:semantics")
        need(verification_paths[0].read_bytes() == verification_paths[1].read_bytes(),
             "dual seed verifier byte identity")

        attacks_path = Path(args.attacks)
        attacks = json.loads(attacks_path.read_bytes())
        closed(attacks, "attack_result_sha256", "attacks")
        need(attacks["attack_count"] == 20 and attacks["all_rejected"] is True
             and attacks["formal_credit"] == 0
             and attacks["manifest_authorized"] is False
             and attacks["source_W_transition_authorized"] is False,
             "attack semantics")
        original = json.loads(ORIGINAL.read_bytes())
        commitment = original["candidate_commitment"]
        need(commitment["candidate_count"] == 10_660
             and commitment["candidate_representation_ids_sha256"]
                == result_values[0]["candidate_representation_ids_sha256"]
             and commitment["candidate_row_sequence_sha256"]
                == result_values[0]["semantic_body_sequence_sha256"]
             and original["formal_credit"] == 0,
             "original commitment binding")

        body = {
            "schema": "cm2.c27-independent.included-stratum-10660-materialized.zero-credit-receipt.v1",
            "status": "PASS_LOCAL_ZERO_CREDIT__10660_MATERIALIZED_CANDIDATES__DUAL_SEED__DUAL_NO_IMPORT_SQLITE_VERIFICATION__20_ATTACKS",
            "terminal": "INCLUDED_STRATUM_ATTACHMENTS",
            "candidate_count": 10_660,
            "excluded_retained_count": 276,
            "candidate_excluded_intersection_count": 0,
            "candidate_representation_ids_sha256": result_values[0]["candidate_representation_ids_sha256"],
            "semantic_body_sequence_sha256": result_values[0]["semantic_body_sequence_sha256"],
            "materialized_row_sequence_sha256": result_values[0]["ledger"]["row_sequence_sha256"],
            "dual_seed_materialization_byte_identical": True,
            "dual_seed_no_import_verification_byte_identical": True,
            "independent_sqlite_rebuild_executed_twice": True,
            "coherent_resigned_attacks_rejected": 20,
            "evidence": {
                "seed_A_result_file_sha256": file_hash(results[0]),
                "seed_B_result_file_sha256": file_hash(results[1]),
                "materialized_ledger_file_sha256": file_hash(ledgers[0]),
                "verification_file_sha256": file_hash(verification_paths[0]),
                "verification_object_sha256": verifications[0]["verification_sha256"],
                "attacks_file_sha256": file_hash(attacks_path),
                "attacks_object_sha256": attacks["attack_result_sha256"],
                "original_subgate_receipt_file_sha256": file_hash(ORIGINAL),
            },
            "script_pins": {
                "materializer": file_hash(MATERIALIZER),
                "independent_verifier": file_hash(VERIFIER),
                "attack_harness": file_hash(ATTACKER),
            },
            "old_C27_FAMILIES_imported_or_read": False,
            "old_transition_or_edge_ledger_used_as_candidate_universe": False,
            "formal_credit": 0,
            "manifest_authorized": False,
            "source_W_transition_authorized": False,
            "C27_C28_C29": "REJECT_PENDING_COMPLETE_PRIMITIVE_TWENTY_TERMINAL_GATE",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        value = {**body, "receipt_sha256": digest(body)}
        output = Path(args.output)
        need(not output.exists(), "fresh output")
        output.write_bytes(encode(value) + b"\n")
    except (Reject, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError) as error:
        print("REJECT:" + str(error))
        return 2
    print(encode({"status": value["status"],
                  "receipt_sha256": value["receipt_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
