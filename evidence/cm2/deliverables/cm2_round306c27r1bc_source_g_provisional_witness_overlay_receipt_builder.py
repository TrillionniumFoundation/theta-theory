#!/usr/bin/env python3
"""Fail-closed receipt builder for the zero-credit C27R1-B/C overlay."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
PREFIX = "cm2_round306c27r1bc_source_g_provisional_witness_overlay"
FILES = [
    PREFIX + "_192_edge_promotion_ledger.jsonl.gz",
    PREFIX + "_502204_member_assignment_ledger.jsonl.gz",
    PREFIX + "_57684_component_census_ledger.jsonl.gz",
    PREFIX + "_120_affected_cluster_ledger.jsonl.gz",
    PREFIX + "_result.json",
]
SOURCES = [
    "cm2_round306c27r1bc_source_g_provisional_witness_overlay_producer.py",
    "cm2_round306c27r1bc_source_g_provisional_witness_overlay_independent_verifier.py",
    "cm2_round306c27r1bc_source_g_provisional_witness_overlay_attack_harness.py",
    "cm2_round306c27r1bc_source_g_provisional_witness_overlay_receipt_builder.py",
]


class Failure(RuntimeError): pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value: raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str: return hashlib.sha256(canonical(value)).hexdigest()


def fsha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 * 1024 * 1024): state.update(block)
    return state.hexdigest()


def load_canonical(path: Path) -> dict[str, Any]:
    raw = path.read_bytes(); value = json.loads(raw)
    need(type(value) is dict and canonical(value) + b"\n" == raw, "canonical json:" + path.name)
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-a", type=Path, required=True); parser.add_argument("--seed-b", type=Path, required=True)
    parser.add_argument("--seed-a-value", type=int, required=True); parser.add_argument("--seed-b-value", type=int, required=True)
    parser.add_argument("--verification", type=Path, required=True); parser.add_argument("--attacks", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True); args = parser.parse_args()
    need(args.seed_a_value != args.seed_b_value, "distinct seeds")
    for directory in (args.seed_a, args.seed_b):
        need(directory.is_dir() and not directory.is_symlink(), "regular seed directory")
        need(set(item.name for item in directory.iterdir()) == set(FILES), "exclusive overlay files")
    hashes_a = {name: fsha(args.seed_a / name) for name in FILES}
    hashes_b = {name: fsha(args.seed_b / name) for name in FILES}
    need(hashes_a == hashes_b, "dual-seed byte identity")
    result = load_canonical(args.seed_a / (PREFIX + "_result.json"))
    result_body = dict(result); claimed = result_body.pop("result_object_sha256", None)
    need(claimed == digest(result_body), "result closure")
    need(result.get("status") == "PASS_PROVISIONAL_UPPER_BOUND_ONLY__ZERO_FORMAL_CREDIT" and result.get("formal_credit") == 0, "result zero credit")
    need(result["partition_census"] == {"members": 502204, "old_C15_components": 57876, "provisional_components": 57684, "affected_old_component_vertices": 312, "affected_connected_clusters": 120, "forced_rank_reduction": 192, "newly_internalized_member_pairs": 691416, "provisional_cross_component_pair_denominator": 125615784254}, "result census")
    verification = load_canonical(args.verification); verify_body = dict(verification); verify_claim = verify_body.pop("verification_object_sha256", None)
    need(verify_claim == digest(verify_body), "verification closure")
    need(verification.get("status") == "PASS_INDEPENDENT_GRAPH_BFS_VERIFICATION__PROVISIONAL_UPPER_BOUND_ONLY" and verification.get("formal_credit") == 0, "independent verification")
    need(verification["candidate_files_sha256"] == hashes_a, "verifier candidate pins")
    attacks = load_canonical(args.attacks); attack_body = dict(attacks); attack_claim = attack_body.pop("result_object_sha256", None)
    need(attack_claim == digest(attack_body), "attack closure")
    need(attacks.get("status") == "PASS_ALL_COHERENT_ATTACKS_REJECTED" and attacks.get("attack_count") >= 20 and all(row.get("observed") == "REJECT" for row in attacks["receipts"]), "coherent attacks")
    witness_receipt = ROOT / "cm2_c27_same_chart_exact_equal_cross_component_final_receipt.json"
    witness = load_canonical(witness_receipt)
    need(witness.get("legal_cross_component_witness_found") is True and witness.get("C27_C28_C29") == "REJECT_AND_REBUILD_REQUIRED", "witness authority")
    receipt = {
        "schema": "cm2.round306c27r1-bc.provisional-witness-overlay-receipt.v1",
        "status": "PASS_PROVISIONAL_UPPER_BOUND_ONLY__APPEND_ONLY__ZERO_FORMAL_CREDIT",
        "formal_credit": 0,
        "authority_limit": "WITNESS_ONLY_PROVISIONAL_OVERLAY__NOT_A_FORMAL_C27R1_C28R1_OR_C29R1_SEAL",
        "double_seed": {"seeds": [args.seed_a_value, args.seed_b_value], "real_materializations": 2, "all_five_outputs_byte_identical": True, "output_sha256": hashes_a},
        "independent_verifier": {"implementation": "ADJACENCY_LIST_GRAPH_BFS_NOT_PRODUCER_DSU", "receipt_sha256": fsha(args.verification), "verification_object_sha256": verify_claim, "status": verification["status"]},
        "coherent_attacks": {"count": attacks["attack_count"], "all_rejected": True, "receipt_sha256": fsha(args.attacks), "result_object_sha256": attack_claim},
        "source_sha256": {name: fsha(ROOT / name) for name in SOURCES},
        "input_authority": {"witness_receipt_sha256": fsha(witness_receipt), "witness_ledger_sha256": result["input_sha256"]["witness"], "C15_member_ledger_sha256": result["input_sha256"]["member"], "C15_component_census_sha256": result["input_sha256"]["census"]},
        "census": {"witness_groups": 228, "certain_component_edges": 192, "all_edges_strictly_witnessed": True, "members": 502204, "old_components": 57876, "provisional_components": 57684, "affected_vertices": 312, "affected_clusters": 120, "forced_rank_reduction": 192, "newly_internalized_pairs": 691416, "provisional_cross_denominator": 125615784254},
        "qualification": {"partition": "PROVISIONAL_UPPER_BOUND_ONLY", "SAME_CHART_remaining": "OPEN", "support_terminals_remaining": ["SIGNED_BOUNDARY_FACES", "COMPLETE_BOUNDARY_FACES", "POSITIVE_VOLUME_CARRIERS"], "twenty_family_totality": "OPEN", "C28": "REJECT", "C29": "REJECT", "CM2": "NO-GO_FOR_CLAIM"},
        "forbidden_state_changes": {"old_C27_C28_C29_read_or_reused_by_producer": False, "old_C27_C28_C29_modified": False, "formal_seal_published": False, "C30c_touched": False},
    }
    receipt["receipt_object_sha256"] = digest(receipt)
    payload = canonical(receipt) + b"\n"; need(not args.out.exists(), "no-clobber receipt")
    fd = os.open(args.out, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try: os.write(fd, payload); os.fsync(fd)
    finally: os.close(fd)
    os.sys.stdout.buffer.write(payload); return 0


if __name__ == "__main__":
    try: raise SystemExit(main())
    except (Failure, OSError, KeyError, ValueError, TypeError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "FAIL_CLOSED", "error": str(error)}, sort_keys=True), file=os.sys.stderr); raise SystemExit(2)
