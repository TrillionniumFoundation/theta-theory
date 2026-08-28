#!/usr/bin/env python3
"""Coherent re-signed attacks against the T04 common-v2 adapter contract."""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import json
from pathlib import Path
from typing import Any, Callable, Iterator


CANDIDATE_SCHEMA = "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.candidate-ownership.row.v2"
PROOF_SCHEMA = "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.materialized-physical-proof-join.row.v2"
CP = "round306c27-v5-t04-double-graphs-candidate:"
PP = "round306c27-v5-t04-double-graphs-physical-proof:"


class Reject(RuntimeError): pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value: raise Reject(label)


def enc(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
                      allow_nan=False).encode("ascii")


def digest(value: Any) -> str: return hashlib.sha256(enc(value)).hexdigest()


def sequence(value: str) -> str: return hashlib.sha256(value.encode() + b"\n").hexdigest()


def first(path: Path) -> dict[str, Any]:
    with gzip.open(path, "rt", encoding="ascii") as stream: row = json.loads(next(stream))
    return row


def validate_receipt(row: dict[str, Any]) -> None:
    need(row["terminal"] == "DOUBLE_GRAPHS" and row["terminal_ordinal"] == 4
         and row["authority_slot"] == "T04_DOUBLE_GRAPHS", "terminal")
    need(row["candidate_key_namespace"] == CP and row["proof_key_namespace"] == PP, "namespaces")
    need(row["candidate_ownership_ledger"]["row_count"] == 1_362_088
         and row["candidate_ownership_ledger"]["row_schema"] == CANDIDATE_SCHEMA
         and row["candidate_ownership_ledger"]["unique_key"] == "candidate_key", "candidate descriptor")
    need(row["materialized_physical_proof_join_ledger"]["row_count"] == 1_362_088
         and row["materialized_physical_proof_join_ledger"]["row_schema"] == PROOF_SCHEMA
         and row["materialized_physical_proof_join_ledger"]["unique_key"] == "proof_row_key", "proof descriptor")
    exact = row["exact_census"]
    need(exact["candidate_pairs"] == exact["physical_proof_rows"] == 1_362_088
         and exact["unresolved"] == exact["legal_cross_component_witnesses"] == exact["component_edges"] == 0,
         "exact census")
    common = row["common_v2_contract"]
    need(all(common.values()), "common-v2 booleans")
    need(row["formal_credit"] == 0 and row["manifest_authorized"] is False
         and row["source_W_transition_authorized"] is False, "zero credit")


def validate_triplet(native: dict[str, Any], candidate: dict[str, Any], proof: dict[str, Any]) -> None:
    for row in (native, candidate, proof):
        body = dict(row); claim = body.pop("row_sha256", None); need(claim == digest(body), "row closure")
    key = CP + digest({"native_candidate_id": native["candidate_id"],
                       "native_candidate_key_sha256": native["candidate_key_sha256"],
                       "terminal_ordinal": 4, "authority_slot": "T04_DOUBLE_GRAPHS"})
    pkey = PP + digest([key, native["row_sha256"]])
    need(candidate["schema"] == CANDIDATE_SCHEMA and candidate["candidate_key"] == key
         and candidate["terminal_ordinal"] == 4 and candidate["authority_slot"] == "T04_DOUBLE_GRAPHS"
         and candidate["primitive_authority_row_sha256"] == native["row_sha256"]
         and candidate["physical_proof_row_count"] == 1
         and candidate["physical_proof_row_sequence_sha256"] == sequence(proof["row_sha256"])
         and candidate["formal_credit"] == 0, "candidate binding")
    need(proof["schema"] == PROOF_SCHEMA and proof["proof_row_key"] == pkey
         and proof["candidate_key"] == key and proof["terminal_ordinal"] == 4
         and proof["authority_slot"] == "T04_DOUBLE_GRAPHS"
         and proof["primitive_authority_row_sha256"] == native["row_sha256"]
         and proof["native_candidate_id"] == native["candidate_id"]
         and proof["native_candidate_key"] == native["candidate_key"]
         and proof["absence_disposition_route"] == native["exact_disposition_route"]
         and proof["native_exact_physical_proof"] == native["exact_physical_proof"]
         and proof["component_edge_key"] is None and proof["physical_witness_key"] is None
         and proof["legal_cross_component_same_physical_point_witness"] is False
         and proof["formal_credit"] == 0, "proof binding")


def resign(row: dict[str, Any]) -> None:
    body = dict(row); body.pop("row_sha256", None); row["row_sha256"] = digest(body)


def rejected(fn: Callable[..., None], *values: dict[str, Any]) -> bool:
    try: fn(*values)
    except (Reject, KeyError, TypeError, ValueError): return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--native-ledger", required=True)
    parser.add_argument("--adapter", required=True); parser.add_argument("--output", required=True)
    args = parser.parse_args(); adapter = Path(args.adapter)
    receipt = json.loads((adapter / "adapter_receipt.json").read_bytes())
    body = dict(receipt); claim = body.pop("receipt_sha256", None); need(claim == digest(body), "receipt closure")
    validate_receipt(receipt)
    native = first(Path(args.native_ledger))
    candidate = first(adapter / "T04_DOUBLE_GRAPHS_candidate_ownership.jsonl.gz")
    proof = first(adapter / "T04_DOUBLE_GRAPHS_materialized_physical_proof_join.jsonl.gz")
    validate_triplet(native, candidate, proof)
    attacks: dict[str, bool] = {}
    receipt_mutations = {
        "terminal_ordinal": lambda x: x.__setitem__("terminal_ordinal", 5),
        "authority_slot": lambda x: x.__setitem__("authority_slot", "T05"),
        "candidate_namespace": lambda x: x.__setitem__("candidate_key_namespace", CP + "x"),
        "proof_namespace": lambda x: x.__setitem__("proof_key_namespace", PP + "x"),
        "candidate_count": lambda x: x["exact_census"].__setitem__("candidate_pairs", 1_362_087),
        "proof_count": lambda x: x["exact_census"].__setitem__("physical_proof_rows", 1_362_087),
        "unresolved": lambda x: x["exact_census"].__setitem__("unresolved", 1),
        "witness": lambda x: x["exact_census"].__setitem__("legal_cross_component_witnesses", 1),
        "component_edge": lambda x: x["exact_census"].__setitem__("component_edges", 1),
        "common_false": lambda x: x["common_v2_contract"].__setitem__("each_candidate_exactly_one_materialized_physical_proof", False),
        "formal_credit": lambda x: x.__setitem__("formal_credit", 1),
        "manifest_authorized": lambda x: x.__setitem__("manifest_authorized", True),
    }
    for name, mutate in receipt_mutations.items():
        item = copy.deepcopy(receipt); mutate(item); attacks[name] = rejected(validate_receipt, item)

    def triplet_attack(name: str, target: str, mutate: Callable[[dict[str, Any]], None], coherent_candidate=False) -> None:
        n, c, p = copy.deepcopy(native), copy.deepcopy(candidate), copy.deepcopy(proof)
        selected = {"native": n, "candidate": c, "proof": p}[target]; mutate(selected); resign(selected)
        if coherent_candidate and target == "proof":
            c["physical_proof_row_sequence_sha256"] = sequence(p["row_sha256"]); resign(c)
        attacks[name] = rejected(validate_triplet, n, c, p)

    triplet_attack("candidate_key", "candidate", lambda x: x.__setitem__("candidate_key", CP + "0"*64))
    triplet_attack("candidate_terminal", "candidate", lambda x: x.__setitem__("terminal_ordinal", 5))
    triplet_attack("candidate_slot", "candidate", lambda x: x.__setitem__("authority_slot", "T05"))
    triplet_attack("candidate_source_sha", "candidate", lambda x: x.__setitem__("primitive_authority_row_sha256", "0"*64))
    triplet_attack("candidate_proof_count", "candidate", lambda x: x.__setitem__("physical_proof_row_count", 0))
    triplet_attack("proof_key", "proof", lambda x: x.__setitem__("proof_row_key", PP + "0"*64), True)
    triplet_attack("proof_candidate_key", "proof", lambda x: x.__setitem__("candidate_key", CP + "0"*64), True)
    triplet_attack("proof_native_id", "proof", lambda x: x.__setitem__("native_candidate_id", "mutated"), True)
    triplet_attack("proof_native_key", "proof", lambda x: x.__setitem__("native_candidate_key", {}), True)
    triplet_attack("proof_route", "proof", lambda x: x.__setitem__("absence_disposition_route", "MUTATED"), True)
    triplet_attack("proof_payload", "proof", lambda x: x.__setitem__("native_exact_physical_proof", {}), True)
    triplet_attack("proof_edge", "proof", lambda x: x.__setitem__("component_edge_key", "forged"), True)
    triplet_attack("proof_witness", "proof", lambda x: x.__setitem__("legal_cross_component_same_physical_point_witness", True), True)
    need(len(attacks) == 25 and all(attacks.values()), "25 attacks")
    result_body = {"schema": "cm2.c27-independent.t04-double-graphs.common-v2-typed-adapter-coherent-attacks.v1",
                   "status": "PASS_25_OF_25_COMMON_V2_COHERENT_RESIGNED_ATTACKS_REJECTED",
                   "attack_count": 25, "accepted": 0, "rejected": 25,
                   "attacks": attacks, "formal_credit": 0, "manifest_authorized": False}
    output = {**result_body, "attack_receipt_sha256": digest(result_body)}
    path = Path(args.output); need(not path.exists(), "fresh output"); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(enc(output) + b"\n"); print(enc(output).decode()); return 0


if __name__ == "__main__":
    try: raise SystemExit(main())
    except Reject as exc:
        print("T04_COMMON_V2_ATTACK_REJECT:" + str(exc)); raise SystemExit(2)
