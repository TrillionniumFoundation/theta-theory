#!/usr/bin/env python3
"""Publish the dual-seed C19C v3 authority receipt and append-only bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any


PREFIX = "cm2_c19c_endpoint_ownership_v3"
LEDGER_NAMES = [
    PREFIX + "_authority_ledger.jsonl.gz",
    PREFIX + "_face_atom_ledger.jsonl.gz",
    PREFIX + "_codimension1_in_face_junction_1d_ledger.jsonl.gz",
    PREFIX + "_codimension2_in_face_junction_0d_ledger.jsonl.gz",
    PREFIX + "_c19c_additive_replay_ledger.jsonl.gz",
    PREFIX + "_c25_additive_replay_ledger.jsonl.gz",
    PREFIX + "_c26_additive_replay_ledger.jsonl.gz",
]
RESULT_NAME = PREFIX + "_result.json"
VERIFICATION_NAME = PREFIX + "_independent_verification.json"
ATTACK_NAME = PREFIX + "_attack_result.json"
RECEIPT_NAME = PREFIX + "_terminal_receipt.json"
MANIFEST_NAME = PREFIX + "_manifest.sha256"


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def objsha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def filesha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def closed_json(path: Path, closure_key: str) -> dict[str, Any]:
    value = json.loads(path.read_bytes())
    body = dict(value)
    claimed = body.pop(closure_key, None)
    if claimed != objsha(body):
        raise RuntimeError("JSON closure:" + path.name)
    return value


def publish(source: Path, destination: Path) -> None:
    if destination.exists():
        if filesha(source) != filesha(destination):
            raise RuntimeError("no-replace publication conflict:" + destination.name)
        return
    shutil.copy2(source, destination)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-a", required=True)
    parser.add_argument("--candidate-b", required=True)
    parser.add_argument("--verification-a", required=True)
    parser.add_argument("--verification-b", required=True)
    parser.add_argument("--attack-result", required=True)
    parser.add_argument("--producer", required=True)
    parser.add_argument("--verifier", required=True)
    parser.add_argument("--attack-harness", required=True)
    parser.add_argument("--publish-dir", required=True)
    args = parser.parse_args()
    candidate_a = Path(args.candidate_a).resolve()
    candidate_b = Path(args.candidate_b).resolve()
    verification_a_path = Path(args.verification_a).resolve()
    verification_b_path = Path(args.verification_b).resolve()
    attack_path = Path(args.attack_result).resolve()
    publish_dir = Path(args.publish_dir).resolve()
    publish_dir.mkdir(parents=True, exist_ok=True)

    result_a = closed_json(candidate_a / RESULT_NAME, "result_sha256")
    result_b = closed_json(candidate_b / RESULT_NAME, "result_sha256")
    if result_a["status"] != result_b["status"] or result_a["status"] != "PASS_APPEND_ONLY_ENDPOINT_OWNER_AUTHORITY__ZERO_FORMAL_CREDIT":
        raise RuntimeError("producer statuses")
    if result_a["execution_seed"] == result_b["execution_seed"]:
        raise RuntimeError("producer seeds not distinct")
    if result_a["execution_order_attestation"] == result_b["execution_order_attestation"]:
        raise RuntimeError("producer seeds did not alter execution order")
    if result_a["ledgers"] != result_b["ledgers"]:
        raise RuntimeError("dual-seed ledgers not byte-identical")
    for name in LEDGER_NAMES:
        if filesha(candidate_a / name) != filesha(candidate_b / name):
            raise RuntimeError("dual-seed file mismatch:" + name)

    verification_a = closed_json(verification_a_path, "verification_sha256")
    verification_b = closed_json(verification_b_path, "verification_sha256")
    if verification_a["status"] != verification_b["status"] or verification_a["status"] != "PASS":
        raise RuntimeError("verification status")
    if verification_a["verification_seed"] == verification_b["verification_seed"]:
        raise RuntimeError("verification seeds not distinct")
    if verification_a["verified_result_sha256"] != result_a["result_sha256"]:
        raise RuntimeError("verification A binding")
    if verification_b["verified_result_sha256"] != result_b["result_sha256"]:
        raise RuntimeError("verification B binding")
    if verification_a["verified_ledgers"] != verification_b["verified_ledgers"] or verification_a["verified_ledgers"] != result_a["ledgers"]:
        raise RuntimeError("verification ledger binding")

    attack = closed_json(attack_path, "result_sha256")
    if attack["status"] != "PASS_ALL_COHERENT_RESIGNED_ATTACKS_REJECTED" or attack["attack_count"] != 12 or attack["rejected_attack_count"] != 12:
        raise RuntimeError("attack gate")
    if attack["candidate_result_sha256"] != result_a["result_sha256"] or attack["candidate_ledgers"] != result_a["ledgers"]:
        raise RuntimeError("attack candidate binding")

    producer = Path(args.producer).resolve()
    verifier = Path(args.verifier).resolve()
    harness = Path(args.attack_harness).resolve()
    source_pins = {
        producer.name: filesha(producer),
        verifier.name: filesha(verifier),
        harness.name: filesha(harness),
        Path(__file__).name: filesha(Path(__file__).resolve()),
    }
    if attack["independent_verifier_sha256"] != source_pins[verifier.name]:
        raise RuntimeError("attack verifier binding")

    semantic = {
        "schema": "cm2.c19c-endpoint-ownership-v3.terminal-receipt.v1",
        "status": "PASS_APPEND_ONLY_V3_AUTHORITY_DUAL_SEED_DUAL_VERIFIER_ATTACK_SEALED",
        "formal_credit": 0,
        "C27_C28_C29": "UNAUTHORIZED_PENDING_REBUILD",
        "CM2": "NO-GO_FOR_CLAIM",
        "source_W_transition_authorized": False,
        "producer_runs": [
            {
                "execution_seed": result_a["execution_seed"],
                "result_sha256": result_a["result_sha256"],
                "execution_order_attestation": result_a["execution_order_attestation"],
            },
            {
                "execution_seed": result_b["execution_seed"],
                "result_sha256": result_b["result_sha256"],
                "execution_order_attestation": result_b["execution_order_attestation"],
            },
        ],
        "independent_verifier_runs": [
            {
                "verification_seed": verification_a["verification_seed"],
                "verification_sha256": verification_a["verification_sha256"],
                "randomized_authority_order_sha256": verification_a["randomized_authority_order_sha256"],
            },
            {
                "verification_seed": verification_b["verification_seed"],
                "verification_sha256": verification_b["verification_sha256"],
                "randomized_authority_order_sha256": verification_b["randomized_authority_order_sha256"],
            },
        ],
        "byte_identical_dual_seed_ledgers": result_a["ledgers"],
        "authority": result_a["authority"],
        "forest_proofs": result_a["forest_proofs"],
        "face_and_junction_gluing": result_a["face_gluing"],
        "additive_replay": result_a["additive_replay"],
        "coherent_resigned_attacks": {
            "attack_count": attack["attack_count"],
            "rejected_attack_count": attack["rejected_attack_count"],
            "attack_result_sha256": attack["result_sha256"],
            "attack_names": [row["attack_name"] for row in attack["attacks"]],
        },
        "source_pins": source_pins,
        "strict_nonpromotion": result_a["strict_nonpromotion"],
        "required_next": "CONSUME_THIS_V3_AUTHORITY_IN_THE_APPEND_ONLY_SAME_CHART_LOWER_DIMENSIONAL_CONTACT_SUBGATE",
    }
    receipt = {**semantic, "receipt_sha256": objsha(semantic)}

    # Publish candidate A as the canonical append-only bundle.
    for name in LEDGER_NAMES + [RESULT_NAME]:
        publish(candidate_a / name, publish_dir / name)
    publish(verification_a_path, publish_dir / VERIFICATION_NAME)
    publish(attack_path, publish_dir / ATTACK_NAME)
    receipt_path = publish_dir / RECEIPT_NAME
    if receipt_path.exists() and receipt_path.read_bytes() != canonical(receipt):
        raise RuntimeError("no-replace receipt conflict")
    if not receipt_path.exists():
        with receipt_path.open("xb") as stream:
            stream.write(canonical(receipt))

    members = [
        *LEDGER_NAMES,
        RESULT_NAME,
        VERIFICATION_NAME,
        ATTACK_NAME,
        RECEIPT_NAME,
        producer.name,
        verifier.name,
        harness.name,
        Path(__file__).name,
    ]
    manifest_lines = [f"{filesha(publish_dir / name)}  {name}\n" for name in sorted(members)]
    manifest_path = publish_dir / MANIFEST_NAME
    manifest_bytes = "".join(manifest_lines).encode("ascii")
    if manifest_path.exists() and manifest_path.read_bytes() != manifest_bytes:
        raise RuntimeError("no-replace manifest conflict")
    if not manifest_path.exists():
        with manifest_path.open("xb") as stream:
            stream.write(manifest_bytes)
    print(canonical({"status": receipt["status"], "receipt_sha256": receipt["receipt_sha256"], "manifest_sha256": filesha(manifest_path)}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
