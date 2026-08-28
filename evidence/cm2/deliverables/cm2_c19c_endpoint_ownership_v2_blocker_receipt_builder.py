#!/usr/bin/env python3
"""Build the append-only zero-credit receipt for the C19C endpoint blocker."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


PREFIX = "cm2_c19c_endpoint_ownership_v2"
RESULT = PREFIX + "_blocker_result.json"
LEDGER = PREFIX + "_unrecoverable_rows.jsonl.gz"


class Rejected(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def objsha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def filesha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def closed(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    value = json.loads(raw)
    need(canonical(value) == raw, "canonical:" + path.name)
    body = dict(value)
    need(body.pop("result_sha256", None) == objsha(body), "closure:" + path.name)
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-a", required=True)
    parser.add_argument("--run-b", required=True)
    parser.add_argument("--verification-a", required=True)
    parser.add_argument("--verification-b", required=True)
    parser.add_argument("--attacks", required=True)
    parser.add_argument("--producer", required=True)
    parser.add_argument("--verifier", required=True)
    parser.add_argument("--attack-harness", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    run_a, run_b = Path(args.run_a).resolve(), Path(args.run_b).resolve()
    result_a, result_b = closed(run_a / RESULT), closed(run_b / RESULT)
    verify_a, verify_b = closed(Path(args.verification_a).resolve()), closed(Path(args.verification_b).resolve())
    attacks = closed(Path(args.attacks).resolve())
    need(result_a["execution_seed"] != result_b["execution_seed"] and result_a["execution_seed"] > 0 and result_b["execution_seed"] > 0, "distinct real seeds")
    projection_a, projection_b = dict(result_a), dict(result_b)
    for projection in (projection_a, projection_b):
        projection.pop("execution_seed")
        projection.pop("result_sha256")
    need(projection_a == projection_b, "semantic double-seed identity")
    need(filesha(run_a / LEDGER) == filesha(run_b / LEDGER), "byte-identical ledgers")
    need(verify_a["status"] == verify_b["status"] == "PASS_INDEPENDENT_BLOCKER_RECONSTRUCTION", "dual verification")
    need(verify_a["verified_rows"] == verify_b["verified_rows"] == 33_344, "verified census")
    need(attacks["all_rejected"] is True and attacks["attack_count"] == attacks["rejected_count"] >= 12, "attacks")

    producer = Path(args.producer).resolve()
    verifier = Path(args.verifier).resolve()
    attack_harness = Path(args.attack_harness).resolve()
    body = {
        "schema": "cm2.c19c-endpoint-ownership-v2.minimal-unrecoverable-blocker-receipt.v1",
        "status": "PASS_BLOCKER_MATERIALIZED_ZERO_CREDIT",
        "finding": {
            "exact_bounds_and_R174_R179_R234_paths_reconstructed_for_all_rows": True,
            "C19C_row_count": 33_344,
            "requested_endpoint_bit_slots": 200_064,
            "materialized_endpoint_bit_slots": 0,
            "constructive_final_t_interface_nonidentifiability_rows": 33_344,
            "full_six_bit_vectors_recoverable": 0,
            "minimal_unrecoverable_commitment": "DYADIC_RECTANGULAR_FACE_OWNER_OR_EXPLICIT_SIX_ENDPOINT_INCLUSION_BITS",
        },
        "double_seed": {
            "seed_a": result_a["execution_seed"],
            "seed_b": result_b["execution_seed"],
            "semantic_projection_sha256": objsha(projection_a),
            "ledger_sha256": filesha(run_a / LEDGER),
            "ledger_byte_identical": True,
            "result_a_file_sha256": filesha(run_a / RESULT),
            "result_b_file_sha256": filesha(run_b / RESULT),
        },
        "independent_verification": {
            "run_a_file_sha256": filesha(Path(args.verification_a).resolve()),
            "run_b_file_sha256": filesha(Path(args.verification_b).resolve()),
            "both_pass": True,
        },
        "coherent_attacks": {
            "file_sha256": filesha(Path(args.attacks).resolve()),
            "attack_count": attacks["attack_count"],
            "rejected_count": attacks["rejected_count"],
            "all_rejected": True,
        },
        "implementation_pins": {
            producer.name: filesha(producer),
            verifier.name: filesha(verifier),
            attack_harness.name: filesha(attack_harness),
            Path(__file__).name: filesha(Path(__file__).resolve()),
        },
        "strict_nonpromotion": {
            "formal_credit": 0,
            "C19C_half_open_set_equality": "NOT_CLOSED",
            "SAME_CHART_RELATIVE_CELLS_totality": False,
            "twenty_family_gate": "OPEN",
            "C27": "REBUILD_REQUIRED_AND_NOT_AUTHORIZED",
            "C28": "REJECT",
            "C29": "REJECT",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": "APPEND_ONLY_UPSTREAM_ENDPOINT_OWNER_LEDGER_THEN_REPLAY_C19C_C25_C26",
    }
    result = {**body, "result_sha256": objsha(body)}
    raw = canonical(result)
    Path(args.output).resolve().write_bytes(raw)
    print(raw.decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
