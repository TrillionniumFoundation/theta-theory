#!/usr/bin/env python3
"""Coherent re-signed attacks for the corrected T04 common-v2 adapter."""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import json
from pathlib import Path
from typing import Any, Callable, Iterator


CANDIDATE_SCHEMA = (
    "cm2.c27-independent.primitive-twenty-family-gate-v5-actual."
    "candidate-ownership.row.v2")
PROOF_SCHEMA = (
    "cm2.c27-independent.primitive-twenty-family-gate-v5-actual."
    "materialized-physical-proof-join.row.v2")
ABSENCE_SCHEMA = (
    "cm2.c27-independent.t04-double-graphs.common-v2-terminal-absence-"
    "authority.row.v2")
CP = "round306c27-v5-t04-double-graphs-candidate:"
AP = "round306c27-v5-t04-double-graphs-absence-authority:"
EMPTY = hashlib.sha256(b"").hexdigest()
DISPOSITION = "NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS"


class Reject(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def enc(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(enc(value)).hexdigest()


def rows(path: Path) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rt", encoding="ascii") as stream:
        for line in stream:
            yield json.loads(line)


def first(path: Path) -> dict[str, Any]:
    return next(rows(path))


def row_closure(row: dict[str, Any]) -> None:
    body = dict(row)
    claim = body.pop("row_sha256", None)
    need(claim == digest(body), "row closure")


def receipt_closure(row: dict[str, Any]) -> None:
    body = dict(row)
    claim = body.pop("receipt_sha256", None)
    need(claim == digest(body), "receipt closure")


def resign_row(row: dict[str, Any]) -> None:
    body = dict(row)
    body.pop("row_sha256", None)
    row["row_sha256"] = digest(body)


def resign_receipt(row: dict[str, Any]) -> None:
    body = dict(row)
    body.pop("receipt_sha256", None)
    row["receipt_sha256"] = digest(body)


def common_key(native: dict[str, Any]) -> str:
    return CP + digest({
        "native_candidate_id": native["candidate_id"],
        "native_candidate_key_sha256": native["candidate_key_sha256"],
        "terminal_ordinal": 4,
        "authority_slot": "T04_DOUBLE_GRAPHS",
    })


def validate_receipt(row: dict[str, Any]) -> None:
    receipt_closure(row)
    need(row["schema"] ==
         "cm2.c27-independent.t04-double-graphs.common-v2-typed-adapter-correction-receipt.v2",
         "receipt schema")
    need(row["terminal"] == "DOUBLE_GRAPHS" and row["terminal_ordinal"] == 4
         and row["authority_slot"] == "T04_DOUBLE_GRAPHS", "terminal")
    need(row["candidate_key_namespace"] == CP
         and row["absence_authority_key_namespace"] == AP, "namespaces")
    cd = row["candidate_ownership_ledger"]
    ad = row["terminal_absence_authority_ledger"]
    pd = row["materialized_physical_proof_join_ledger"]
    need(cd["row_count"] == 1_362_088 and cd["row_schema"] == CANDIDATE_SCHEMA
         and cd["unique_key"] == "candidate_key"
         and cd["ordering"] == ["candidate_key"], "candidate descriptor")
    need(ad["row_count"] == 1_362_088 and ad["row_schema"] == ABSENCE_SCHEMA
         and ad["unique_key"] == "absence_authority_row_key"
         and ad["ordering"] == ["candidate_key"], "absence descriptor")
    need(pd["row_count"] == 0 and pd["row_schema"] == PROOF_SCHEMA
         and pd["row_sequence_sha256"] == EMPTY, "empty proof descriptor")
    exact = row["exact_census"]
    need(exact["candidate_pairs"] == 1_362_088
         and exact["terminal_absence_authority_rows"] == 1_362_088
         and exact["physical_proof_rows"] == 0
         and exact["unresolved"] == 0
         and exact["legal_cross_component_witnesses"] == 0
         and exact["component_edges"] == 0, "exact census")
    contract = row["common_v2_contract"]
    need(contract["component_relation_disposition"] == DISPOSITION
         and contract["each_candidate_physical_proof_row_count"] == 0
         and contract["each_candidate_physical_proof_sequence_sha256"] == EMPTY
         and contract["common_physical_proof_join_is_empty"] is True
         and contract["native_exact_absence_is_terminal_authority_not_physical_proof"] is True
         and contract["absence_authority_join_exact"] is True,
         "corrected contract")
    need(row["correction_governance"]["quarantined_outputs_may_not_be_consumed"] is True
         and row["formal_credit"] == 0
         and row["manifest_authorized"] is False
         and row["source_W_transition_authorized"] is False,
         "fail closed")


def validate_binding(native: dict[str, Any], candidate: dict[str, Any],
                     absence: dict[str, Any]) -> None:
    for row in (native, candidate, absence):
        row_closure(row)
    key = common_key(native)
    absence_key = AP + digest([
        key, native["row_sha256"], native["exact_disposition_route"]])
    need(candidate["schema"] == CANDIDATE_SCHEMA
         and candidate["candidate_key"] == key
         and candidate["candidate_pair_key_or_null"] == key
         and candidate["terminal"] == "DOUBLE_GRAPHS"
         and candidate["terminal_ordinal"] == 4
         and candidate["authority_slot"] == "T04_DOUBLE_GRAPHS"
         and candidate["primitive_authority_row_sha256"] == absence["row_sha256"]
         and candidate["component_relation_disposition"] == DISPOSITION
         and candidate["physical_proof_row_count"] == 0
         and candidate["physical_proof_row_sequence_sha256"] == EMPTY
         and candidate["formal_credit"] == 0, "candidate binding")
    need(absence["schema"] == ABSENCE_SCHEMA
         and absence["absence_authority_row_key"] == absence_key
         and absence["candidate_key"] == key
         and absence["terminal"] == "DOUBLE_GRAPHS"
         and absence["terminal_ordinal"] == 4
         and absence["authority_slot"] == "T04_DOUBLE_GRAPHS"
         and absence["native_candidate_id"] == native["candidate_id"]
         and absence["native_candidate_key_sha256"] == native["candidate_key_sha256"]
         and absence["native_bucket"] == native["bucket"]
         and absence["native_authority_row_sha256"] == native["row_sha256"]
         and absence["exact_disposition_route"] == native["exact_disposition_route"]
         and absence["exact_physical_absence_evidence"] == native["exact_physical_proof"]
         and absence["resolved"] is True and absence["unresolved"] is False
         and absence["legal_cross_component_same_physical_point_witness"] is False
         and absence["component_relation_disposition"] == DISPOSITION
         and absence["formal_credit"] == 0, "absence binding")


def validate_proof_rows(receipt: dict[str, Any], proof_rows: list[dict[str, Any]]) -> None:
    validate_receipt(receipt)
    need(proof_rows == [], "common physical proof join must be empty")


def rejected(function: Callable[..., None], *values: Any) -> bool:
    try:
        function(*values)
    except (Reject, KeyError, TypeError, ValueError):
        return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--native-ledger", required=True)
    parser.add_argument("--adapter", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    adapter = Path(args.adapter).resolve()
    receipt = json.loads((adapter / "adapter_receipt.json").read_bytes())
    validate_receipt(receipt)
    candidate = first(adapter / "T04_DOUBLE_GRAPHS_candidate_ownership.jsonl.gz")
    absence = first(adapter / "T04_DOUBLE_GRAPHS_terminal_absence_authority.jsonl.gz")
    native = None
    for row in rows(Path(args.native_ledger).resolve()):
        if row["candidate_id"] == absence["native_candidate_id"]:
            native = row
            break
    need(native is not None, "native row for first canonical candidate")
    validate_binding(native, candidate, absence)
    proof_rows = list(rows(
        adapter / "T04_DOUBLE_GRAPHS_materialized_physical_proof_join.jsonl.gz"))
    validate_proof_rows(receipt, proof_rows)

    attacks: dict[str, bool] = {}
    receipt_mutations: dict[str, Callable[[dict[str, Any]], None]] = {
        "receipt_terminal_ordinal": lambda x: x.__setitem__("terminal_ordinal", 5),
        "receipt_authority_slot": lambda x: x.__setitem__("authority_slot", "T05"),
        "receipt_candidate_namespace": lambda x: x.__setitem__("candidate_key_namespace", CP + "x"),
        "receipt_absence_namespace": lambda x: x.__setitem__("absence_authority_key_namespace", AP + "x"),
        "receipt_candidate_count": lambda x: x["exact_census"].__setitem__("candidate_pairs", 1_362_087),
        "receipt_absence_count": lambda x: x["exact_census"].__setitem__("terminal_absence_authority_rows", 1_362_087),
        "receipt_physical_proof_count": lambda x: x["exact_census"].__setitem__("physical_proof_rows", 1),
        "receipt_proof_descriptor_count": lambda x: x["materialized_physical_proof_join_ledger"].__setitem__("row_count", 1),
        "receipt_unresolved": lambda x: x["exact_census"].__setitem__("unresolved", 1),
        "receipt_witness": lambda x: x["exact_census"].__setitem__("legal_cross_component_witnesses", 1),
        "receipt_component_edge": lambda x: x["exact_census"].__setitem__("component_edges", 1),
        "receipt_custom_disposition": lambda x: x["common_v2_contract"].__setitem__(
            "component_relation_disposition",
            "EXACT_EMPTY_SAME_POINT_SOLUTION__COMPONENT_EDGE_IMPOSSIBLE"),
        "receipt_per_candidate_one_proof": lambda x: x["common_v2_contract"].__setitem__(
            "each_candidate_physical_proof_row_count", 1),
        "receipt_nonempty_proof_sequence": lambda x: x["common_v2_contract"].__setitem__(
            "each_candidate_physical_proof_sequence_sha256", "0" * 64),
        "receipt_empty_join_false": lambda x: x["common_v2_contract"].__setitem__(
            "common_physical_proof_join_is_empty", False),
        "receipt_absence_as_proof": lambda x: x["common_v2_contract"].__setitem__(
            "native_exact_absence_is_terminal_authority_not_physical_proof", False),
        "receipt_formal_credit": lambda x: x.__setitem__("formal_credit", 1),
        "receipt_manifest_authorized": lambda x: x.__setitem__("manifest_authorized", True),
        "receipt_source_W_authorized": lambda x: x.__setitem__("source_W_transition_authorized", True),
        "receipt_unquarantine_old_outputs": lambda x: x["correction_governance"].__setitem__(
            "quarantined_outputs_may_not_be_consumed", False),
    }
    for name, mutate in receipt_mutations.items():
        item = copy.deepcopy(receipt)
        mutate(item)
        resign_receipt(item)
        attacks[name] = rejected(validate_receipt, item)

    def binding_attack(name: str, target: str,
                       mutate: Callable[[dict[str, Any]], None]) -> None:
        n, c, a = copy.deepcopy(native), copy.deepcopy(candidate), copy.deepcopy(absence)
        selected = {"native": n, "candidate": c, "absence": a}[target]
        mutate(selected)
        resign_row(selected)
        if target == "absence":
            c["primitive_authority_row_sha256"] = a["row_sha256"]
            resign_row(c)
        attacks[name] = rejected(validate_binding, n, c, a)

    binding_attack("candidate_key", "candidate", lambda x: x.__setitem__("candidate_key", CP + "0" * 64))
    binding_attack("candidate_pair_null", "candidate", lambda x: x.__setitem__("candidate_pair_key_or_null", None))
    binding_attack("candidate_terminal", "candidate", lambda x: x.__setitem__("terminal_ordinal", 5))
    binding_attack("candidate_slot", "candidate", lambda x: x.__setitem__("authority_slot", "T05"))
    binding_attack("candidate_authority", "candidate", lambda x: x.__setitem__("primitive_authority_row_sha256", "0" * 64))
    binding_attack("candidate_custom_disposition", "candidate", lambda x: x.__setitem__(
        "component_relation_disposition",
        "EXACT_TARGET_NONEDGE__COMPLETE_T0_OWNER_EQUALS_SOURCE_COMPONENT"))
    binding_attack("candidate_one_pseudo_proof", "candidate", lambda x: x.__setitem__("physical_proof_row_count", 1))
    binding_attack("candidate_forged_proof_sequence", "candidate", lambda x: x.__setitem__("physical_proof_row_sequence_sha256", "0" * 64))
    binding_attack("absence_key", "absence", lambda x: x.__setitem__("absence_authority_row_key", AP + "0" * 64))
    binding_attack("absence_route", "absence", lambda x: x.__setitem__("exact_disposition_route", "MUTATED"))
    binding_attack("absence_evidence", "absence", lambda x: x.__setitem__("exact_physical_absence_evidence", {}))
    binding_attack("absence_witness", "absence", lambda x: x.__setitem__("legal_cross_component_same_physical_point_witness", True))
    binding_attack("absence_native_bucket", "absence", lambda x: x.__setitem__("native_bucket", "MUTATED"))

    forged_body = {
        "schema": PROOF_SCHEMA,
        "ordinal": 0,
        "proof_row_key": "round306c27-v5-t04-double-graphs-physical-proof:" + "0" * 64,
        "candidate_key": candidate["candidate_key"],
        "atom_pair_incidence_key_or_null": None,
        "terminal": "DOUBLE_GRAPHS",
        "authority_slot": "T04_DOUBLE_GRAPHS",
        "primitive_authority_row_sha256": absence["row_sha256"],
        "ordered_C15_member_pair": None,
        "ordered_C15_component_pair": None,
        "component_edge_key": None,
        "physical_witness_key": None,
        "formal_credit": 0,
    }
    forged = {**forged_body, "row_sha256": digest(forged_body)}
    attacks["legacy_one_pseudo_proof_with_null_C15_component_edge_witness"] = rejected(
        validate_proof_rows, receipt, [forged])

    need(len(attacks) == 34 and all(attacks.values()), "34 coherent attacks")
    body = {
        "schema": (
            "cm2.c27-independent.t04-double-graphs.common-v2-typed-adapter-"
            "correction-coherent-attacks.v2"),
        "status": "PASS_34_OF_34_CORRECTION_V2_COHERENT_RESIGNED_ATTACKS_REJECTED",
        "attack_count": 34,
        "accepted": 0,
        "rejected": 34,
        "explicitly_rejects_quarantined_one_pseudo_proof_mode": True,
        "attacks": attacks,
        "formal_credit": 0,
        "manifest_authorized": False,
        "source_W_transition_authorized": False,
    }
    result = {**body, "attack_receipt_sha256": digest(body)}
    output = Path(args.output).resolve()
    need(not output.exists(), "fresh attack output")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(enc(result) + b"\n")
    print(enc(result).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Reject as exc:
        print("T04_COMMON_V2_CORRECTION_ATTACK_REJECT:" + str(exc))
        raise SystemExit(2)
