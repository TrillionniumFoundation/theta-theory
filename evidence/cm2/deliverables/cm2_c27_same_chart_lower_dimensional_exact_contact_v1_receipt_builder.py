#!/usr/bin/env python3
"""Publish the dual-seed lower-contact zero-credit evidence bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any


PREFIX = "cm2_c27_same_chart_lower_dimensional_exact_contact_v1"
BUCKET_LEDGER = PREFIX + "_complete_candidate_bucket_commitments.jsonl.gz"
C19C_LEDGER = PREFIX + "_c19c_endpoint_dependent_contacts.jsonl.gz"
RESULT = PREFIX + "_result.json"
VERIFY_A = PREFIX + "_independent_verification_seed30636201.json"
VERIFY_B = PREFIX + "_independent_verification_seed30636891.json"
ATTACK = PREFIX + "_attack_result.json"
RECEIPT = PREFIX + "_terminal_receipt.json"
MANIFEST = PREFIX + "_manifest.sha256"


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def objsha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def filesha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 << 20), b""):
            state.update(block)
    return state.hexdigest()


def closed_json(path: Path, key: str) -> dict[str, Any]:
    raw = path.read_bytes()
    value = json.loads(raw)
    if canonical(value) != raw:
        raise RuntimeError("canonical JSON:" + path.name)
    body = dict(value)
    claimed = body.pop(key, None)
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
    a, b = Path(args.candidate_a).resolve(), Path(args.candidate_b).resolve()
    va_path, vb_path = Path(args.verification_a).resolve(), Path(args.verification_b).resolve()
    attack_path = Path(args.attack_result).resolve()
    publish_dir = Path(args.publish_dir).resolve()
    publish_dir.mkdir(parents=True, exist_ok=True)

    ra, rb = closed_json(a / RESULT, "result_sha256"), closed_json(b / RESULT, "result_sha256")
    expected_status = "PASS_COMPLETE_SAME_CHART_LOWER_DIMENSIONAL_EXACT_CONTACT_SUBGATE__ZERO_LEGAL_WITNESSES__ZERO_FORMAL_CREDIT"
    if ra["status"] != expected_status or rb["status"] != expected_status:
        raise RuntimeError("producer status")
    if ra["execution_seed"] == rb["execution_seed"] or ra["execution_order_attestation"] == rb["execution_order_attestation"]:
        raise RuntimeError("producer seed/order independence")
    if ra["semantic_projection_sha256"] != rb["semantic_projection_sha256"] or ra["census"] != rb["census"]:
        raise RuntimeError("cross-seed semantic mismatch")
    if ra["formal_credit"] != 0 or rb["formal_credit"] != 0 or ra["source_W_transition_authorized"] is not False or rb["source_W_transition_authorized"] is not False:
        raise RuntimeError("producer nonpromotion")
    for name in (BUCKET_LEDGER, C19C_LEDGER):
        if filesha(a / name) != filesha(b / name):
            raise RuntimeError("dual-seed ledger mismatch:" + name)

    va, vb = closed_json(va_path, "verification_sha256"), closed_json(vb_path, "verification_sha256")
    expected_verify = "PASS_INDEPENDENT_NONSQLITE_EXACT_T_SWEEP_MATCHES_ALL_5783708_LOWER_CONTACTS_AND_76000_ENDPOINT_ROWS__ZERO_FORMAL_CREDIT"
    if va["status"] != expected_verify or vb["status"] != expected_verify:
        raise RuntimeError("verifier status")
    if va["verification_seed"] == vb["verification_seed"]:
        raise RuntimeError("verifier seeds distinct")
    if va["candidate_result_sha256"] != ra["result_sha256"] or vb["candidate_result_sha256"] != rb["result_sha256"]:
        raise RuntimeError("verifier candidate binding")
    for key in ("candidate_semantic_projection_sha256", "complete_closure_pair_count", "lower_dimensional_candidate_pair_count", "strict_dimension3_pair_count_crosscheck", "C19C_endpoint_dependent_contact_count", "other_fully_open_rejection_count", "legal_cross_component_lower_dimensional_witness_count", "global_pair_commitment", "bucket_ledger_sha256", "C19C_ledger_sha256"):
        if va[key] != vb[key]:
            raise RuntimeError("cross-verifier semantic mismatch:" + key)
    if va["formal_credit"] != 0 or vb["formal_credit"] != 0 or va["source_W_transition_authorized"] is not False or vb["source_W_transition_authorized"] is not False:
        raise RuntimeError("verifier nonpromotion")

    attack = closed_json(attack_path, "result_sha256")
    if attack["status"] != "PASS_ALL_18_COHERENT_RESIGNED_MUTATIONS_REJECTED" or attack["attack_count"] != 18 or attack["rejected_count"] != 18:
        raise RuntimeError("attack gate")
    if attack["candidate_result_sha256"] != ra["result_sha256"] or attack["candidate_semantic_projection_sha256"] != ra["semantic_projection_sha256"]:
        raise RuntimeError("attack candidate binding")
    if attack["authority_projection_sha256"] != attack["candidate_projection_sha256"]:
        raise RuntimeError("attack baseline authority mismatch")

    producer, verifier, harness = Path(args.producer).resolve(), Path(args.verifier).resolve(), Path(args.attack_harness).resolve()
    source_pins = {
        producer.name: filesha(producer), verifier.name: filesha(verifier), harness.name: filesha(harness),
        Path(__file__).name: filesha(Path(__file__).resolve()),
    }
    if attack["independent_verifier_sha256"] != source_pins[verifier.name]:
        raise RuntimeError("attack verifier source binding")

    census = ra["census"]
    semantic = {
        "schema": "cm2.c27.same-chart-lower-dimensional-exact-contact.v1.terminal-receipt.v1",
        "status": "PASS_DUAL_SEED_DUAL_IMPLEMENTATION_COMPLETE_5783708_LOWER_CONTACT_SUBGATE__ZERO_LEGAL_WITNESSES__ZERO_FORMAL_CREDIT",
        "scope": "SAME_CHART_LOWER_DIMENSIONAL_EXACT_CONTACT_SUBGATE_ONLY",
        "full_20_family_totality_authorized": False,
        "other_primitive_terminals_still_required": True,
        "candidate_universe": "DIRECT_SIX_PRIMITIVE_KERNELS_PLUS_C15_C25_C26_PRIMITIVE_CHART_LINEAGE_AND_PUBLISHED_C19C_V3_COLD_AUTHORITY",
        "forbidden_inputs": ra["forbidden_inputs"],
        "producer_runs": [
            {"execution_seed": ra["execution_seed"], "execution_order_attestation": ra["execution_order_attestation"], "result_sha256": ra["result_sha256"]},
            {"execution_seed": rb["execution_seed"], "execution_order_attestation": rb["execution_order_attestation"], "result_sha256": rb["result_sha256"]},
        ],
        "independent_verifier_runs": [
            {"verification_seed": va["verification_seed"], "algorithm": va["algorithm"], "verification_sha256": va["verification_sha256"]},
            {"verification_seed": vb["verification_seed"], "algorithm": vb["algorithm"], "verification_sha256": vb["verification_sha256"]},
        ],
        "byte_identical_dual_seed_ledgers": census["ledgers"],
        "complete_closure_pair_count": census["all_closure_intersection_pair_count"],
        "strict_dimension3_pair_count_crosscheck": census["strict_dimension3_pair_count_crosscheck"],
        "lower_dimensional_candidate_pair_count": census["lower_dimensional_candidate_pair_count"],
        "dimension_census": census["dimension_census"],
        "component_relation_census": census["component_relation_census"],
        "global_pair_commitment": census["global_canonical_sorted_pair_digest_sequence_sha256"],
        "endpoint_dependent_C19C_x_C19C": {
            "candidate_count": census["C19C_endpoint_dependent_contact_count"], "dimension1_count": census["C19C_dim1_count"],
            "dimension2_count": census["C19C_dim2_count"], "cross_component_count": census["C19C_cross_component_count"],
            "same_component_count": census["C19C_same_component_count"], "legal_witness_count": census["legal_cross_component_lower_dimensional_witness_count"],
            "endpoint_pattern_census": census["C19C_endpoint_pattern_census"],
            "every_zero_axis_has_exactly_one_closed_and_one_open_factor": True,
            "disposition": "ALL_REJECTED_BY_PUBLISHED_V3_EXACT_PRODUCT_ENDPOINT_AUTHORITY",
        },
        "other_fully_open_kernels": {"candidate_count": census["open_kernel_uniform_rejection_candidate_count"], "disposition": "ALL_REJECTED_BECAUSE_AT_LEAST_ONE_ZERO_AXIS_FACTOR_IS_OPEN"},
        "C26_role": {"full_rows_read": ra["authority_joins"]["C26_full_rows"], "absence_used_as_negative_geometry_theorem": False},
        "coherent_resigned_attacks": {"attack_count": attack["attack_count"], "rejected_count": attack["rejected_count"], "attack_result_sha256": attack["result_sha256"], "attack_names": [row["attack"] for row in attack["attacks"]]},
        "source_pins": source_pins,
        "formal_credit": 0, "C27_C28_C29": "REBUILD_REQUIRED_AND_NOT_AUTHORIZED", "CM2": "NO-GO_FOR_CLAIM", "source_W_transition_authorized": False,
        "required_next": "COMBINE_WITH_ALL_OTHER_PRIMITIVE_TOTALITY_SUBGATES_BEFORE_ANY_C27_REBUILD_AUTHORIZATION",
    }
    receipt = {**semantic, "receipt_sha256": objsha(semantic)}

    for name in (BUCKET_LEDGER, C19C_LEDGER, RESULT):
        publish(a / name, publish_dir / name)
    publish(va_path, publish_dir / VERIFY_A)
    publish(vb_path, publish_dir / VERIFY_B)
    publish(attack_path, publish_dir / ATTACK)
    receipt_path = publish_dir / RECEIPT
    if receipt_path.exists() and receipt_path.read_bytes() != canonical(receipt):
        raise RuntimeError("no-replace receipt conflict")
    if not receipt_path.exists():
        with receipt_path.open("xb") as stream:
            stream.write(canonical(receipt))
    members = [BUCKET_LEDGER, C19C_LEDGER, RESULT, VERIFY_A, VERIFY_B, ATTACK, RECEIPT, producer.name, verifier.name, harness.name, Path(__file__).name]
    manifest_bytes = "".join(f"{filesha(publish_dir / name)}  {name}\n" for name in sorted(members)).encode("ascii")
    manifest_path = publish_dir / MANIFEST
    if manifest_path.exists() and manifest_path.read_bytes() != manifest_bytes:
        raise RuntimeError("no-replace manifest conflict")
    if not manifest_path.exists():
        with manifest_path.open("xb") as stream:
            stream.write(manifest_bytes)
    print(canonical({"status": receipt["status"], "receipt_sha256": receipt["receipt_sha256"], "manifest_sha256": filesha(manifest_path)}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
